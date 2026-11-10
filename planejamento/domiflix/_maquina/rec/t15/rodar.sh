#!/usr/bin/env bash
# T15 · Uso: rec/t15/rodar.sh NN [--ensaio] [--rapido] [--seed]
#   NN         capítulo (0 a 12): gera o roteiro do robô, valida (--check), grava sob a trava (flock + nice -n 10) e resume
#   --ensaio   só captura + telemetria (--no-encode): não gera o .mp4 (ensaio de seletores e de ritmo)
#   --rapido   ensaio sem esperar a fala (tira os `at`; rec/t15/_ens/): acha seletor errado e confere o estado; NÃO mede o ritmo
#   --seed     depois da gravação/ensaio, NA MESMA trava, grava seeds-extra/t15/apos-capNN.json (snap.mjs diff NN): é a semente do capítulo seguinte
# Instância própria do Supabase falso (porta 54336, `FAKE_NOW=... FAKE_PORT=54336 rec/run.sh fake`); o app (8080) é compartilhado.
# Link na tela: APP_ORIGIN=https://www.dominex.app. QUALQUER execução de navegador só sob `flock $TUT_HOME/.heavy.lock` (uma trava por capítulo).
set -uo pipefail
cd /home/claude/domiflix
export TUT_HOME=/home/claude/domiflix FAKE_URL=http://127.0.0.1:54336 FAKE_NOW="${FAKE_NOW:-2026-11-11T09:00:00-03:00}"
export APP_ORIGIN="${APP_ORIGIN:-https://www.dominex.app}"
ARG="$1"; SUF=""; case "$ARG" in *b) SUF="b"; ARG="${ARG%b}";; esac   # "9b" = o trecho do celular do cap. 9 (cap09b)
N=$((10#$ARG)); NN=$(printf '%02d' "$N")$SUF
shift
ENSAIO=""; RAPIDO=""; SEED=""
for a in "$@"; do
  case "$a" in
    --ensaio) ENSAIO="--no-encode" ;;
    --rapido) ENSAIO="--no-encode"; RAPIDO=1 ;;
    --seed) SEED=1 ;;
    *) echo "opção desconhecida: $a"; exit 2 ;;
  esac
done
# a instância tem de ser a minha e estar com o FAKE_NOW certo
if ! grep -qz "^FAKE_NOW=$FAKE_NOW\$" /proc/$(cat rec/.runtime/fake54336.pid 2>/dev/null || echo 0)/environ 2>/dev/null; then   # (sem pipe: `tr | grep -q` com pipefail falhava por SIGPIPE de vez em quando)
  echo "INSTÂNCIA 54336 AUSENTE OU SEM O FAKE_NOW CERTO: suba com  FAKE_NOW=$FAKE_NOW FAKE_PORT=54336 rec/run.sh fake"; exit 4
fi
livre=$(df -k --output=avail /home/claude | tail -1)
if [ "$livre" -lt $((1536 * 1024)) ]; then echo "DISCO BAIXO (< 1,5 GiB): paro"; exit 3; fi
# o app (8080) tem de estar de pé: ensaio com o app fora do ar não vale (e não pode gravar semente)
cod=$(curl -s -o /dev/null -w '%{http_code}' --max-time 10 http://127.0.0.1:8080/ || true)
if [ "$cod" != "200" ]; then echo "APP 8080 NÃO RESPONDE 200 (http $cod): paro"; exit 5; fi
python3 -I rec/t15/gerar.py "$N$SUF" | tail -3
node rec/record.mjs rec/t15/cap$NN.json --check | tail -2
SAIDA=rec/t15; ROT=rec/t15/cap$NN.json
if [ -n "$RAPIDO" ]; then python3 -I rec/t15/ensaio.py "$NN"; SAIDA=rec/t15/_ens; ROT=rec/t15/_ens/cap$NN.json; fi
CMD="node rec/record.mjs $ROT --out $SAIDA --name t15-cap$NN $ENSAIO > rec/t15/.rec-$NN.log 2>&1; rc=\$?"
if [ -n "$SEED" ]; then CMD="$CMD; node rec/t15/snap.mjs diff $NN > rec/t15/.snap-$NN.log 2>&1"; fi
CMD="$CMD; exit \$rc"
if [ -n "${TUT_LOCKED:-}" ]; then run() { nice -n 10 bash -c "$CMD"; }; else run() { flock "$TUT_HOME/.heavy.lock" nice -n 10 bash -c "$CMD"; }; fi
if ! run; then
  echo "=== GRAVAÇÃO FALHOU (cauda do log) ==="; tail -25 rec/t15/.rec-$NN.log
fi
python3 -I rec/t15/resumo.py "$NN" ${RAPIDO:+--ens} 2>&1 | head -140
if [ -n "$SEED" ]; then echo "--- snapshot:"; tail -6 rec/t15/.snap-$NN.log; fi
