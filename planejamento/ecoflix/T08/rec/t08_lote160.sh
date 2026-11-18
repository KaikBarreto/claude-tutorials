#!/bin/bash
# T08 · lote de ensaios do 1.60.10 (18/11): cada capítulo pela fila (t08_grava.sh, que religa a instância 54308 no FAKE_NOW do
# capítulo), no modo dado (padrão --rapido, com MP4 ultrafast e folha de contato). Depois dos capítulos da cadeia (07, 08, 10, 11),
# com 0 passo falho, grava a semente apos-capNN (t08_semente.py) que o capítulo seguinte usa; se falhar, os que dependem dele são
# pulados. Guarda a folha de contato em rec/t08/_folhas/ e apaga o MP4. Uma linha por capítulo em rec/t08/lote160.txt.
# Uso: bash rec/t08/t08_lote160.sh 00 01 ... 13        ou 08:--os-dois (rápido + completa) / 08: (só a completa)
cd /home/claude/ecoflix
export TUT_USER=rafael@reciclavalemetais.example
[ -n "${TUT_SENHA:-}" ] || export TUT_SENHA="$(head -c 12 /dev/urandom | base64)"
mkdir -p rec/t08/_folhas
declare -A DEP=([08]=07 [09]=08 [10]=08 [11]=10 [12]=11 [13]=11)
declare -A FALHOU
for ITEM in "$@"; do
  NN=${ITEM%%:*}; M=--rapido; [ "$NN" != "$ITEM" ] && M=${ITEM#*:}
  D=${DEP[$NN]:-}
  if [ -n "$D" ] && [ -n "${FALHOU[$D]:-}" ]; then FALHOU[$NN]=1; echo "cap$NN PULADO (depende do cap$D)" | tee -a rec/t08/lote160.txt; continue; fi
  python3 -I rec/t08/gerar.py "$NN" > /dev/null || { FALHOU[$NN]=1; echo "cap$NN gerar.py falhou" | tee -a rec/t08/lote160.txt; continue; }
  bash rec/t08/t08_grava.sh "$NN" $M > "rec/t08/_ens/.grava$NN.log" 2>&1; RC=$?
  R=rec/t08/_ens/cap$NN.resumo; [ "$M" = "--rapido" ] || [ "$M" = "--os-dois" ] || R=rec/t08/cap$NN.resumo
  FE=$(grep -c '!!ERRO\|DIFERENTE:\|SEM ALVO' "$R" 2>/dev/null); S=$(cat "rec/t08/_ens/.cap$NN.out" 2>/dev/null | grep -c 'SEM ALVO')
  for f in rec/t08/_ens/t08-cap$NN.contact.jpg rec/t08/t08-cap$NN.contact.jpg; do [ -f "$f" ] && mv "$f" "rec/t08/_folhas/$(basename "$(dirname "$f")")-cap$NN.jpg"; done
  rm -f "/home/claude/ecoflix/rec/t08/_ens/t08-cap$NN.mp4" "/home/claude/ecoflix/rec/t08/t08-cap$NN.mp4"
  OK=1; { [ "$RC" != 0 ] || [ "${FE:-1}" != 0 ] || [ ! -s "$R" ]; } && OK=0
  if [ $OK = 1 ]; then
    case $NN in 07|08|10|11) python3 -I rec/t08/t08_semente.py "apos-cap$NN" > "rec/t08/_ens/.semente$NN.log" 2>&1 || OK=0;; esac
  fi
  [ $OK = 1 ] || FALHOU[$NN]=1
  echo "cap$NN modo=${M:-completa} rc=$RC falhos=$FE semalvo=$S ok=$OK | $(head -1 "$R" 2>/dev/null | cut -c1-160)" | tee -a rec/t08/lote160.txt
done
python3 -I rec/t08/t08_pdf.py --ens > rec/t08/_ens/pdf.txt 2>&1
echo "lote fim $(date +%H:%M:%S)" | tee -a rec/t08/lote160.txt
