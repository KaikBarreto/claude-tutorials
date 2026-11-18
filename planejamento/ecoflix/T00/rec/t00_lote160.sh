#!/usr/bin/env bash
# T0 · lote de ensaios, um capítulo por vez pela fila. uso: bash rec/t00/t00_lote160.sh [--completo] NN[b] ...
# Resultado de cada um em rec/t00/_ens/lote/<cap>.txt (ou .completo.txt); o MP4 é apagado, a folha de contato fica até ser olhada.
set -u
cd "$(dirname "$0")/../.."
modo=""; [ "${1:-}" = "--completo" ] && { modo="--completo"; shift; }
mkdir -p rec/t00/_ens/lote
for a in "$@"; do
  f="rec/t00/_ens/lote/$a${modo:+.completo}.txt"
  bash rec/t00/t00_um.sh "$a" $modo >"$f" 2>&1
  n="${a%b}"; [ -z "$modo" ] && python3 -I rec/t00/prever.py "$a" --ens >>"$f.prever" 2>&1
  if [ -z "$modo" ]; then rm -f "rec/t00/_ens/t00-cap$a.mp4"; else rm -f "rec/t00/t00-cap$a.mp4"; fi
  echo "$a: $(head -n 1 "$f")"
done
echo LOTE-FIM
