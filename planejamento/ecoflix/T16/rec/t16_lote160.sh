#!/usr/bin/env bash
# T16 (1.60.39 desde 28/11; era 1.60.22; 1600x900) · lote de ensaios em sequência, um capítulo por vez pela fila (rec/fila.sh --prio 16), com MP4 ultrafast só
# para a folha de contato. Capítulo que mexe no banco e sai com 0 passo falho no rápido captura a semente apos-capNN na MESMA trava.
#   bash rec/t16/t16_lote160.sh [--junto] 0 1 2 ... [--completo 15 16 ...]   (antes de --completo: rápido; depois: completo; --junto: a
#   lista inteira numa senha só da fila, para a espera da fila não se repetir a cada capítulo)
# Depois do cap20, o t16_pdf.py grava em rec/t16/arquivos/ os PDFs que o robô devolveu (comprovante e DANFE).
# Saídas por capítulo em rec/t16/_ens/ (rápido) ou rec/t16/ (completo): t16-capNN.resumo.txt, .prever.txt, .contact.jpg; linha em _lote.txt.
# A senha do login é aleatória, só no ambiente (nunca em arquivo).
set -u
cd "$(dirname "$0")/../.."
MODO=rapido
PORTA=54316
export FAKE_NOW=2026-11-10T08:30:00-03:00 FAKE_URL=http://127.0.0.1:$PORTA TUT_USER=rafael@reciclavalemetais.example
TUT_SENHA=$(head -c 12 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 14); export TUT_SENHA
export T16_VERSAO=1.60.39   # a versão do build (app/dist/.versao-app) que o gerar.py espera (VERSAO)
MUTA=" 3 4 5 6 7 9 11 12 14 15 16 17 18 19 21 22 23 "
PID=$(cat rec/.runtime/fake$PORTA.pid 2>/dev/null)
tr '\0' '\n' < /proc/$PID/environ 2>/dev/null | grep -qx "FAKE_PORT=$PORTA" || { echo "instância $PORTA fora do ar"; exit 3; }
python3 -I rec/t16/gerar.py > rec/t16/_ens/.gerar.out 2>&1 || { echo "gerar.py falhou"; tail -3 rec/t16/_ens/.gerar.out; exit 2; }
# --junto: UMA senha da fila para a lista inteira (20/11: com uma senha por capítulo, cada um esperava ~50 min e 2 h davam 2 capítulos)
FILA="bash rec/fila.sh --prio 16 --"
[ "${1:-}" = --junto ] && { shift; exec bash rec/fila.sh --prio 16 -- bash rec/t16/t16_lote160.sh --dentro "$@"; }
[ "${1:-}" = --dentro ] && { shift; FILA=; }
for C in "$@"; do
  [ "$C" = --completo ] && { MODO=completo; continue; }
  NN=$(printf '%02d' "$((10#$C))")
  if [ "$MODO" = rapido ]; then
    python3 -I rec/t16/ensaio.py "$NN" > /dev/null || continue
    [ -e rec/t16/_ens/assets ] || ln -s ../assets rec/t16/_ens/assets
    ROT=rec/t16/_ens/cap$NN.json; DIR=rec/t16/_ens; EXTRA=--rapido; RES=--ens
  else
    ROT=rec/t16/cap$NN.json; DIR=rec/t16; EXTRA=; RES=
  fi
  SEM=0; case "$MUTA" in *" $((10#$C)) "*) [ "$MODO" = rapido ] && SEM=1 ;; esac
  rm -f "$DIR/t16-cap$NN.actions.json"
  $FILA bash -c '
    [ "$(cat app/dist/.versao-app 2>/dev/null)" = "$T16_VERSAO" ] || { echo "app nao e $T16_VERSAO: $(cat app/dist/.versao-app)" > "$3/.t16-cap$4.out"; echo "9 versao" > "$3/.t16-cap$4.rc"; exit 0; }
    timeout 900 node rec/record.mjs "$1" $2 --preset ultrafast --crf 30 > "$3/.t16-cap$4.out" 2>&1; rc=$?
    f=$(python3 -I -c "import json;a=json.load(open(\"$3/t16-cap$4.actions.json\"))[\"actions\"];print(sum(1 for x in a if x.get(\"error\") or x.get(\"ok\") is False))" 2>/dev/null || echo x)
    if [ "$5" = 1 ] && [ $rc = 0 ] && [ "$f" = 0 ]; then python3 -I rec/t16/t16_sementes.py captura "$((10#$4))" --porta 54316 > "$3/.t16-cap$4.semente" 2>&1; fi
    echo "$rc $f" > "$3/.t16-cap$4.rc"' _ "$ROT" "$EXTRA" "$DIR" "$NN" "$SEM"
  python3 -I rec/t16/resumo.py "$NN" $RES > "$DIR/t16-cap$NN.resumo.txt" 2>&1
  [ "$MODO" = rapido ] && python3 -I rec/t16/prever.py "$NN" --ens > "$DIR/t16-cap$NN.prever.txt" 2>&1
  rm -f "$DIR/t16-cap$NN.mp4"
  [ "$NN" = 20 ] && python3 -I rec/t16/t16_pdf.py $RES > "$DIR/t16-cap20.pdfs.txt" 2>&1
  echo "cap$NN $MODO rc_falhos=$(cat "$DIR/.t16-cap$NN.rc" 2>/dev/null) semente=$(cat "$DIR/.t16-cap$NN.semente" 2>/dev/null | tail -1 | cut -c1-90) $(date +%T)" | tee -a "$DIR/_lote.txt"
done
