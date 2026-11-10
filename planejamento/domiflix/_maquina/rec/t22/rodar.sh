#!/usr/bin/env bash
# T22 · Uso: rec/t22/rodar.sh NN [--ensaio] [--rapido] [--seed]
#   NN         capítulo (0 a 12): gera o roteiro do robô, valida (--check), grava sob a trava (flock + nice -n 10) e resume
#   --ensaio   só captura + telemetria (--no-encode): não gera o .mp4 (ensaio de seletores e de ritmo)
#   --rapido   ensaio sem esperar a fala (tira os `at`; rec/t22/_ens/): acha seletor errado e confere o estado; NÃO mede o ritmo
#   --seed     depois da gravação/ensaio, NA MESMA trava, grava seeds-extra/t22/apos-capNN.json (snap.mjs diff NN): é a semente do capítulo seguinte
# Instância própria do Supabase falso (porta 54337, `FAKE_NOW=... FAKE_PORT=54337 rec/run.sh fake`); o app (8080) é compartilhado.
# Link na tela: APP_ORIGIN=https://www.dominex.app. QUALQUER execução de navegador só sob `flock $TUT_HOME/.heavy.lock` (uma trava por capítulo).
set -uo pipefail
cd /home/claude/domiflix
export TUT_HOME=/home/claude/domiflix FAKE_URL=http://127.0.0.1:54337 FAKE_NOW="${FAKE_NOW:-2026-11-12T10:00:00-03:00}"
export APP_ORIGIN="${APP_ORIGIN:-https://www.dominex.app}"
NN=$(printf '%02d' "$((10#$1))")
shift
ENSAIO=""; RAPIDO=""; SEED=""
for a in "$@"; do
  case "$a" in
    --ensaio) ENSAIO="--no-encode" ;;
    --rapido) ENSAIO="--no-encode"; RAPIDO=1 ;;
    --seed) echo "fase 2: as sementes seeds-extra/t22/apos-capNN.json de 05/11 valem; --seed está desligado"; exit 2 ;;
    *) echo "opção desconhecida: $a"; exit 2 ;;
  esac
done
# a instância tem de ser a minha e estar com o FAKE_NOW certo
if ! grep -qz "^FAKE_NOW=$FAKE_NOW\$" /proc/$(cat rec/.runtime/fake54337.pid 2>/dev/null || echo 0)/environ 2>/dev/null; then   # (sem pipe: `tr | grep -q` com pipefail falhava por SIGPIPE de vez em quando)
  echo "INSTÂNCIA 54337 AUSENTE OU SEM O FAKE_NOW CERTO: suba com  FAKE_NOW=$FAKE_NOW FAKE_PORT=54337 rec/run.sh fake"; exit 4
fi
# fase 2 (05/11): disco mínimo 1,5 GiB e o app 8080 respondendo 200, conferidos ANTES e de novo DENTRO da trava (a espera pela trava pode ser longa)
CONFERE='livre=$(df -k --output=avail /home/claude | tail -1); if [ "$livre" -lt $((1536 * 1024)) ]; then echo "DISCO BAIXO (< 1,5 GiB): paro"; exit 3; fi; cod=$(curl -s -o /dev/null -w "%{http_code}" --max-time 8 http://127.0.0.1:8080/); if [ "$cod" != 200 ]; then echo "APP 8080 NAO RESPONDE 200 ($cod): paro"; exit 5; fi'
bash -c "$CONFERE" || exit $?
python3 -I rec/t22/gerar.py "$((10#$NN))" | tail -3
node rec/record.mjs rec/t22/cap$NN.json --check | tail -2
SAIDA=rec/t22; ROT=rec/t22/cap$NN.json
if [ -n "$RAPIDO" ]; then python3 -I rec/t22/ensaio.py "$NN"; SAIDA=rec/t22/_ens; ROT=rec/t22/_ens/cap$NN.json; fi
# fase 2 (06/11 00:1x): os quadros JPEG da captura (~150-250 MB por capítulo) vão para a RAM (/dev/shm/t22_rec/_frames): no disco eles
# baixavam o espaço livre de ~1,56 GiB para ~1,40 GiB durante a gravação. Depois do encode, as saídas vão para $SAIDA (rec/t22 ou rec/t22/_ens).
TMPREC=/dev/shm/t22_rec
CMD="$CONFERE; mkdir -p $TMPREC; node rec/record.mjs $ROT --out $TMPREC --name t22-cap$NN $ENSAIO > rec/t22/.rec-$NN.log 2>&1; rc=\$?; mv -f $TMPREC/t22-cap$NN.* $SAIDA/ 2>/dev/null; rm -rf /dev/shm/t22_rec/_frames"
if [ -n "$SEED" ]; then CMD="$CMD; node rec/t22/snap.mjs diff $((10#$NN)) > rec/t22/.snap-$NN.log 2>&1"; fi
CMD="$CMD; exit \$rc"
if [ -n "${TUT_LOCKED:-}" ]; then run() { nice -n 10 bash -c "$CMD"; }; else run() { flock "$TUT_HOME/.heavy.lock" nice -n 10 bash -c "$CMD"; }; fi
if ! run; then
  echo "=== GRAVAÇÃO FALHOU (cauda do log) ==="; tail -25 rec/t22/.rec-$NN.log
fi
python3 -I rec/t22/resumo.py "$((10#$NN))" ${RAPIDO:+--ens} 2>&1 | head -140
if [ -n "$SEED" ]; then echo "--- snapshot:"; tail -6 rec/t22/.snap-$NN.log; fi
