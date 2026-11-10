#!/usr/bin/env bash
# T17 · fase 2 (06/11, app 1.38.24) · Uso: rec/t17/rodar.sh NN [--ensaio] [--rapido]
#   NN         capítulo (0 a 11): gera o roteiro do robô, valida (--check), grava sob a trava (flock + nice -n 10) e resume
#   --ensaio   só captura + telemetria (--no-encode): não gera o .mp4 (ensaio de seletores e de ritmo)
#   --rapido   ensaio sem esperar a fala (tira os `at`; rec/t17/_ens/): acha seletor errado e confere o estado; NÃO mede o ritmo
# Instância própria do Supabase falso (porta 54342, FAKE_NOW 13/11 16:30 em todos os capítulos). Se ela estiver parada ou com outro
# FAKE_NOW, este script reinicia SÓ a 54342, FORA da trava. O app (8080) é compartilhado: não o reinicia (para e avisa).
# Nenhum capítulo grava no banco (a aula só lê e filtra): todos partem de `t17/inicio` pela cadeia. Sem link na tela: sem APP_ORIGIN.
# Fase 2 (molde do rec/t21/rodar.sh): gravação em /dev/shm/t17_rec (quadros e saídas na RAM; o disco está curto) e `mv` para rec/t17
# (ou rec/t17/_ens) ao fim de cada capítulo: um reinício do container apaga o /dev/shm. Disco >= 0,8 GiB (piso do coordenador, 06/11 06:3x: a gravação vai para o /dev/shm e cada capítulo põe só alguns MB no disco), app 8080 respondendo 200 e a
# 54342 com o FAKE_NOW certo, conferidos antes e de novo DENTRO da trava (a espera pela trava pode ser longa: o render do T22 usa a mesma).
set -uo pipefail
cd /home/claude/domiflix
export TUT_HOME=/home/claude/domiflix FAKE_URL=http://127.0.0.1:54342
NN=$(printf '%02d' "$((10#$1))")
shift
FAKE_NOW="2026-11-13T16:30:00-03:00"
export FAKE_NOW
ENSAIO=""; RAPIDO=""
for a in "$@"; do
  case "$a" in
    --ensaio) ENSAIO="--no-encode" ;;
    --rapido) ENSAIO="--no-encode"; RAPIDO=1 ;;
    *) echo "opção desconhecida: $a"; exit 2 ;;
  esac
done
# a instância tem de ser a minha, de pé e com o FAKE_NOW do capítulo (sem pipe: `tr | grep -q` com pipefail falhava por SIGPIPE de vez em quando)
FAKE_OK='grep -qz "^FAKE_NOW=$FAKE_NOW\$" /proc/$(cat rec/.runtime/fake54342.pid 2>/dev/null || echo 0)/environ 2>/dev/null && curl -s -o /dev/null --max-time 5 http://127.0.0.1:54342/health'
if ! bash -c "$FAKE_OK"; then
  FAKE_NOW="$FAKE_NOW" FAKE_PORT=54342 rec/run.sh fake > /dev/null 2>&1; sleep 2
  if ! bash -c "$FAKE_OK"; then echo "INSTÂNCIA 54342 NÃO SUBIU COM FAKE_NOW=$FAKE_NOW"; exit 4; fi
  echo "instância 54342 religada (FAKE_NOW=$FAKE_NOW)"
fi
CONFERE='livre=$(df -k --output=avail /home/claude | tail -1); if [ "$livre" -lt 838860 ]; then echo "DISCO BAIXO (< 0,8 GiB): paro"; exit 3; fi; cod=$(curl -s -o /dev/null -w "%{http_code}" --max-time 8 http://127.0.0.1:8080/); if [ "$cod" != 200 ]; then echo "APP 8080 NAO RESPONDE 200 ($cod): paro"; exit 5; fi; if ! { '"$FAKE_OK"'; }; then echo "INSTANCIA 54342 AUSENTE OU SEM FAKE_NOW=$FAKE_NOW: paro"; exit 4; fi'
bash -c "$CONFERE" || exit $?
echo "disco livre: $(df -h --output=avail /home/claude | tail -1 | tr -d ' ')"
# fase 2 (06/11 07:0x): o gerar.py é montado de _head.py + _caps.py; sem remontar, uma edição no _caps.py não chega ao roteiro (aconteceu no cap05)
bash rec/t17/montar.sh
python3 -I rec/t17/gerar.py "$((10#$NN))" | tail -3
node rec/record.mjs rec/t17/cap$NN.json --check | tail -2
SAIDA=rec/t17; ROT=rec/t17/cap$NN.json
if [ -n "$RAPIDO" ]; then python3 -I rec/t17/ensaio.py "$NN"; SAIDA=rec/t17/_ens; ROT=rec/t17/_ens/cap$NN.json; fi
TMPREC=/dev/shm/t17_rec
CMD="$CONFERE; echo \"trava: \$(date +%H:%M:%S)\"; mkdir -p $TMPREC; node rec/record.mjs $ROT --out $TMPREC --name t17-cap$NN $ENSAIO > rec/t17/.rec-$NN.log 2>&1; rc=\$?; mv -f $TMPREC/t17-cap$NN.* $SAIDA/ 2>/dev/null; if [ -d $TMPREC/_debug ]; then mkdir -p $SAIDA/_debug; mv -f $TMPREC/_debug/* $SAIDA/_debug/ 2>/dev/null; fi; rm -rf /dev/shm/t17_rec/_frames; exit \$rc"
if [ -n "${TUT_LOCKED:-}" ]; then run() { nice -n 10 bash -c "$CMD"; }; else run() { flock "$TUT_HOME/.heavy.lock" nice -n 10 bash -c "$CMD"; }; fi
if ! run; then
  echo "=== GRAVAÇÃO FALHOU (cauda do log) ==="; tail -25 rec/t17/.rec-$NN.log
fi
python3 -I rec/t17/resumo.py "$((10#$NN))" ${RAPIDO:+--ens} 2>&1 | head -140
echo "--- unknowns:"; curl -s http://127.0.0.1:54342/__dev/unknowns | head -c 600; echo
