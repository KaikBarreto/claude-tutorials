#!/usr/bin/env bash
# T10 · Uso: rec/t10/rodar.sh NN [--ensaio] [--rapido] [--seed]
#   NN         capítulo (0 a 10): gera o roteiro do robô, valida (--check), grava sob a trava (flock + nice -n 10) e resume
#   --ensaio   só captura + telemetria (--no-encode): não gera o .mp4 (ensaio de seletores e de ritmo)
#   --rapido   ensaio sem esperar a fala (tira os `at`; rec/t10/_ens/): acha seletor errado e confere o estado; NÃO mede o ritmo
#   --seed     depois da gravação/ensaio, NA MESMA trava, grava seeds-extra/t10/apos-capNN.json (snap.mjs diff NN): é a semente do capítulo seguinte
# Instância própria do Supabase falso (porta 54328, `FAKE_NOW=... FAKE_PORT=54328 rec/run.sh fake`); o app (8080) é compartilhado.
# T10 não mostra link público do app (o endereço do webhook é do servidor): sem APP_ORIGIN, o `eval fetch` local do cap. 8 não é desviado. QUALQUER execução de navegador só sob `flock $TUT_HOME/.heavy.lock` (uma trava por capítulo).
set -uo pipefail
cd /home/claude/domiflix
export TUT_HOME=/home/claude/domiflix FAKE_URL=http://127.0.0.1:54328 FAKE_NOW="${FAKE_NOW:-2026-11-03T09:00:00-03:00}"
NN=$(printf '%02d' "$((10#$1))")
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
if ! tr '\0' '\n' < /proc/$(cat rec/.runtime/fake54328.pid 2>/dev/null || echo 0)/environ 2>/dev/null | grep -cx "FAKE_NOW=$FAKE_NOW" | grep -qx 1; then
  echo "INSTÂNCIA 54328 AUSENTE OU SEM O FAKE_NOW CERTO: suba com  FAKE_NOW=$FAKE_NOW FAKE_PORT=54328 rec/run.sh fake"; exit 4
fi
livre=$(df -k --output=avail /home/claude | tail -1)
if [ "$livre" -lt $((3 * 1024 * 1024)) ]; then echo "DISCO BAIXO (< 3 GiB): paro"; exit 3; fi
python3 -I rec/t10/gerar.py "$((10#$NN))" | tail -3
node rec/record.mjs rec/t10/cap$NN.json --check | tail -2
SAIDA=rec/t10; ROT=rec/t10/cap$NN.json
if [ -n "$RAPIDO" ]; then python3 -I rec/t10/ensaio.py "$NN"; SAIDA=rec/t10/_ens; ROT=rec/t10/_ens/cap$NN.json; fi
CMD="timeout 900 node rec/record.mjs $ROT --out $SAIDA --name t10-cap$NN $ENSAIO > rec/t10/.rec-$NN.log 2>&1; rc=\$?"
if [ -n "$SEED" ]; then CMD="$CMD; node rec/t10/snap.mjs diff $((10#$NN)) > rec/t10/.snap-$NN.log 2>&1"
  # cap. 3: as três oportunidades do corte (hotel, Marcos, Luana) entram no apos-cap03 (usa o fakebase vivo)
  if [ "$NN" = "03" ]; then CMD="$CMD; python3 -I rec/t10/corte.py >> rec/t10/.snap-$NN.log 2>&1"; fi; fi
CMD="$CMD; exit \$rc"
if [ -n "${TUT_LOCKED:-}" ]; then run() { nice -n 10 bash -c "$CMD"; }; else run() { flock "$TUT_HOME/.heavy.lock" nice -n 10 bash -c "$CMD"; }; fi
if ! run; then
  echo "=== GRAVAÇÃO FALHOU (cauda do log) ==="; tail -25 rec/t10/.rec-$NN.log
fi
python3 -I rec/t10/resumo.py "$((10#$NN))" ${RAPIDO:+--ens} 2>&1 | head -140
if [ -n "$SEED" ]; then echo "--- snapshot:"; tail -6 rec/t10/.snap-$NN.log; fi
