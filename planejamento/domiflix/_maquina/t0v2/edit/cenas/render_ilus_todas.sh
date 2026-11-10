#!/usr/bin/env bash
# Renderiza as 15 ilustrações do T0 v2 (as duas proporções), cada trecho = a linha da fala da cena (de -0,2 a +0,4 s). Uma trava por render.
cd "$(dirname "$0")" || exit 1
for c in "6 1 0 4.8" "2 0 0 10.3" "3 0 10.0 18.7" "4 0 18.4 28.7" "16 2 5.5 11.2" "17 2 10.9 20.3" "18 2 19.7 29.6" "20 3 0 11.6" "29 5 0 8.8" "31 5 20.4 29.7" "32 5 29.3 36.7" "33 5 36.3 43.3" "35 6 0 6.7" "36 6 6.3 11.2" "37 6 10.8 14.4"; do
  set -- $c; echo "cena $1"; ./render_ilus_v2.sh "$@" 2>&1 | grep -E "^ok|ERRO|AVISOS|rror" ; done; echo FIM
