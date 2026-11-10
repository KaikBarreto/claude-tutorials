#!/usr/bin/env bash
# T21 · fase 2 (06/11, app 1.38.24) · Uso: rec/t21/rodar.sh NN [--ensaio] [--rapido]
#   NN         capítulo (0 a 10): gera o roteiro do robô, valida (--check), grava sob a trava (flock + nice -n 10) e resume
#   --ensaio   só captura + telemetria (--no-encode): não gera o .mp4 (ensaio de seletores e de ritmo)
#   --rapido   ensaio sem esperar a fala (tira os `at`; rec/t21/_ens/): acha seletor errado e confere o estado; NÃO mede o ritmo
#   --seed     DESLIGADO na fase 2: as seeds-extra/t21/apos-capNN.json de 05/11 valem (já alimentaram o T14 e o T17)
# Instância própria do Supabase falso (porta 54340). FAKE_NOW do capítulo: 12/11 14:00 nos caps 0 a 7 e 9; 13/11 15:00 nos caps 8 e 10.
# Se a instância estiver parada ou com outro FAKE_NOW, este script reinicia SÓ a 54340, FORA da trava. O app (8080) é compartilhado: não o reinicia.
# Gravação em /dev/shm/t21_rec (quadros e saídas na RAM; o disco está curto) e `mv` para rec/t21 (ou rec/t21/_ens) ao fim de cada capítulo.
# Disco >= 1,5 GiB, app 8080 respondendo 200 e a 54340 com o FAKE_NOW certo, conferidos antes e de novo DENTRO da trava (a espera pode ser longa).
# Link na tela: APP_ORIGIN=https://www.dominex.app. QUALQUER execução de navegador só sob `flock $TUT_HOME/.heavy.lock` (uma trava por capítulo).
set -uo pipefail
cd /home/claude/domiflix
export TUT_HOME=/home/claude/domiflix FAKE_URL=http://127.0.0.1:54340
export APP_ORIGIN="${APP_ORIGIN:-https://www.dominex.app}"
NN=$(printf '%02d' "$((10#$1))")
shift
case "$NN" in 08|10) FAKE_NOW="2026-11-13T15:00:00-03:00" ;; *) FAKE_NOW="2026-11-12T14:00:00-03:00" ;; esac
export FAKE_NOW
ENSAIO=""; RAPIDO=""
for a in "$@"; do
  case "$a" in
    --ensaio) ENSAIO="--no-encode" ;;
    --rapido) ENSAIO="--no-encode"; RAPIDO=1 ;;
    --seed) echo "fase 2: as sementes seeds-extra/t21/apos-capNN.json de 05/11 valem (T14 e T17 partem delas); --seed está desligado"; exit 2 ;;
    *) echo "opção desconhecida: $a"; exit 2 ;;
  esac
done
# a instância tem de ser a minha, de pé e com o FAKE_NOW do capítulo (sem pipe: `tr | grep -q` com pipefail falhava por SIGPIPE de vez em quando)
FAKE_OK='grep -qz "^FAKE_NOW=$FAKE_NOW\$" /proc/$(cat rec/.runtime/fake54340.pid 2>/dev/null || echo 0)/environ 2>/dev/null && curl -s -o /dev/null --max-time 5 http://127.0.0.1:54340/health'
if ! bash -c "$FAKE_OK"; then
  FAKE_NOW="$FAKE_NOW" FAKE_PORT=54340 rec/run.sh fake > /dev/null 2>&1; sleep 2
  if ! bash -c "$FAKE_OK"; then echo "INSTÂNCIA 54340 NÃO SUBIU COM FAKE_NOW=$FAKE_NOW"; exit 4; fi
fi
CONFERE='livre=$(df -k --output=avail /home/claude | tail -1); if [ "$livre" -lt $((1536 * 1024)) ]; then echo "DISCO BAIXO (< 1,5 GiB): paro"; exit 3; fi; cod=$(curl -s -o /dev/null -w "%{http_code}" --max-time 8 http://127.0.0.1:8080/); if [ "$cod" != 200 ]; then echo "APP 8080 NAO RESPONDE 200 ($cod): paro"; exit 5; fi; if ! { '"$FAKE_OK"'; }; then echo "INSTANCIA 54340 AUSENTE OU SEM FAKE_NOW=$FAKE_NOW: paro"; exit 4; fi'
bash -c "$CONFERE" || exit $?
python3 -I rec/t21/gerar.py "$((10#$NN))" | tail -3
node rec/record.mjs rec/t21/cap$NN.json --check | tail -2
SAIDA=rec/t21; ROT=rec/t21/cap$NN.json
if [ -n "$RAPIDO" ]; then python3 -I rec/t21/ensaio.py "$NN"; SAIDA=rec/t21/_ens; ROT=rec/t21/_ens/cap$NN.json; fi
TMPREC=/dev/shm/t21_rec
CMD="$CONFERE; mkdir -p $TMPREC; node rec/record.mjs $ROT --out $TMPREC --name t21-cap$NN $ENSAIO > rec/t21/.rec-$NN.log 2>&1; rc=\$?; mv -f $TMPREC/t21-cap$NN.* $SAIDA/ 2>/dev/null; rm -rf /dev/shm/t21_rec/_frames; exit \$rc"
if [ -n "${TUT_LOCKED:-}" ]; then run() { nice -n 10 bash -c "$CMD"; }; else run() { flock "$TUT_HOME/.heavy.lock" nice -n 10 bash -c "$CMD"; }; fi
if ! run; then
  echo "=== GRAVAÇÃO FALHOU (cauda do log) ==="; tail -25 rec/t21/.rec-$NN.log
fi
python3 -I rec/t21/resumo.py "$((10#$NN))" ${RAPIDO:+--ens} 2>&1 | head -140
