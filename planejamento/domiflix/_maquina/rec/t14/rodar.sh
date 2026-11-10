#!/usr/bin/env bash
# T14 · fase 2 · Uso: rec/t14/rodar.sh NN [--ensaio] [--rapido]
#   NN         capítulo (0 a 13): gera o roteiro do robô, valida (--check), grava sob a trava (flock + nice -n 10) e resume
#   --ensaio   só captura + telemetria (--no-encode): não gera o .mp4 (ensaio de seletores e de ritmo)
#   --rapido   ensaio sem esperar a fala (tira os `at`; rec/t14/_ens/): acha seletor errado e confere o estado; NÃO mede o ritmo
#   (--seed foi desligado na fase 2: as seeds-extra/t14/apos-capNN.json de 05/11 valem, e a t14/apos-cap12 é a base do T17)
# Instância própria do Supabase falso (porta 54341, `FAKE_NOW=... FAKE_PORT=54341 rec/run.sh fake`); o app (8080) é compartilhado.
# FAKE_NOW do capítulo (rec/t14/cadeia.json): 13/11 15:10 nos caps 0 a 11 e 16:20 nos caps 12 e 13 (a Receita só aceita uma consulta de NF-e
# por CNPJ a cada 65 min); com o relógio errado, reinicio SÓ a minha instância (54341).
# Senha do certificado fictício: só por $TUT_SENHA (sorteada aqui quando não vier de fora; nunca vai para log nem roteiro).
# Link na tela: APP_ORIGIN=https://www.dominex.app. QUALQUER execução de navegador só sob `flock $TUT_HOME/.heavy.lock` (uma trava por capítulo).
# Fase 2 (06/11): disco mínimo 1,5 GiB e o app 8080 respondendo 200, conferidos ANTES e de novo DENTRO da trava (a espera pode ser longa);
# os quadros da captura vão para a RAM (/dev/shm/t14_rec) e as saídas são movidas para rec/t14 (ou rec/t14/_ens) no fim de cada capítulo.
set -uo pipefail
cd /home/claude/domiflix
export TUT_HOME=/home/claude/domiflix FAKE_URL=http://127.0.0.1:54341
export APP_ORIGIN="${APP_ORIGIN:-https://www.dominex.app}"
if [ -z "${TUT_SENHA:-}" ]; then TUT_SENHA="$(python3 -I -c 'import secrets; print(secrets.token_urlsafe(6))')"; fi
export TUT_SENHA
NN=$(printf '%02d' "$((10#$1))")
shift
CHAVE=fake_now; case "$NN" in 12|13) CHAVE=fake_now_cap12 ;; esac
FAKE_NOW="$(python3 -I -c "import json,sys; print(json.load(open('rec/t14/cadeia.json'))[sys.argv[1]])" "$CHAVE")"
export FAKE_NOW
ENSAIO=""; RAPIDO=""
for a in "$@"; do
  case "$a" in
    --ensaio) ENSAIO="--no-encode" ;;
    --rapido) ENSAIO="--no-encode"; RAPIDO=1 ;;
    --seed) echo "fase 2: as sementes seeds-extra/t14/apos-capNN.json de 05/11 valem (a apos-cap12 é a base do T17); --seed está desligado"; exit 2 ;;
    *) echo "opção desconhecida: $a"; exit 2 ;;
  esac
done
PIDF=rec/.runtime/fake54341.pid
# a instância tem de ser a MINHA (FAKE_PORT=54341 no ambiente do processo), estar com o FAKE_NOW do capítulo e responder no /health
# (sem pipe: `tr | grep -q` com pipefail falhava por SIGPIPE de vez em quando). Depois de reiniciar o container o .pid fica velho e o número
# pode ser de outro processo: um .pid que não aponta para um processo meu sai antes do `run.sh fake` (que mataria qualquer server.mjs com aquele pid).
minha() { local p; p=$(cat $PIDF 2>/dev/null || echo 0); grep -qz "^FAKE_PORT=54341\$" /proc/$p/environ 2>/dev/null; }
certa() { minha && grep -qz "^FAKE_NOW=$FAKE_NOW\$" /proc/$(cat $PIDF)/environ 2>/dev/null && curl -s -o /dev/null --max-time 3 http://127.0.0.1:54341/health; }
if ! certa; then
  if [ -f $PIDF ] && ! minha; then rm -f /home/claude/domiflix/rec/.runtime/fake54341.pid; fi
  FAKE_NOW="$FAKE_NOW" FAKE_PORT=54341 rec/run.sh fake > /dev/null 2>&1; sleep 2
  if ! certa; then echo "INSTÂNCIA 54341 NÃO SUBIU COM FAKE_NOW=$FAKE_NOW"; exit 4; fi
  echo "instância 54341 (re)iniciada com FAKE_NOW=$FAKE_NOW"
fi
CONFERE='livre=$(df -k --output=avail /home/claude | tail -1); if [ "$livre" -lt $((1536 * 1024)) ]; then echo "DISCO BAIXO (< 1,5 GiB): paro"; exit 3; fi; cod=$(curl -s -o /dev/null -w "%{http_code}" --max-time 8 http://127.0.0.1:8080/); if [ "$cod" != 200 ]; then echo "APP 8080 NAO RESPONDE 200 ($cod): paro"; exit 5; fi'
bash -c "$CONFERE" || exit $?
python3 -I rec/t14/gerar.py "$((10#$NN))" | tail -3
node rec/record.mjs rec/t14/cap$NN.json --check | tail -2
SAIDA=rec/t14; ROT=rec/t14/cap$NN.json
if [ -n "$RAPIDO" ]; then python3 -I rec/t14/ensaio.py "$NN"; SAIDA=rec/t14/_ens; ROT=rec/t14/_ens/cap$NN.json; fi
TMPREC=/dev/shm/t14_rec
CMD="$CONFERE; mkdir -p $TMPREC; node rec/record.mjs $ROT --out $TMPREC --name t14-cap$NN $ENSAIO > rec/t14/.rec-$NN.log 2>&1; rc=\$?; mv -f $TMPREC/t14-cap$NN.* $SAIDA/ 2>/dev/null; rm -rf /dev/shm/t14_rec/_frames; exit \$rc"
if [ -n "${TUT_LOCKED:-}" ]; then run() { nice -n 10 bash -c "$CMD"; }; else run() { flock "$TUT_HOME/.heavy.lock" nice -n 10 bash -c "$CMD"; }; fi
if ! run; then
  echo "=== GRAVAÇÃO FALHOU (cauda do log) ==="; tail -25 rec/t14/.rec-$NN.log
fi
python3 -I rec/t14/resumo.py "$((10#$NN))" ${RAPIDO:+--ens} 2>&1 | head -160
