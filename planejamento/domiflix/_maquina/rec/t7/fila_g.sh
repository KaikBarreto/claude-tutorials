#!/usr/bin/env bash
# T7 · fase 2 na 1.38.24: gravação (G) dos capítulos pedidos, um por vez; cada um pega e solta a própria trava (o rodar.sh faz
# `flock $TUT_HOME/.heavy.lock nice -n 10`). Antes de cada capítulo: o 8080 e o falso deste agente respondem 200, o falso é o meu
# (FAKE_NOW do T7) e o disco tem >= 1,5 GB; senão para e deixa o motivo em _progresso.txt. Depois: resumo e /__dev/unknowns.
# Uso: FAKE_URL=http://127.0.0.1:54334 bash rec/t7/fila_g.sh 0 1 2 ...   (saída em rec/t7/.g-1.38.24/NN.out)
set -uo pipefail
cd /home/claude/domiflix
: "${FAKE_URL:?defina FAKE_URL (ex.: http://127.0.0.1:54334)}"
OUT=rec/t7/.g-1.38.24; mkdir -p "$OUT"
PORTA="${FAKE_URL##*:}"
for n in "$@"; do
  NN=$(printf '%02d' "$((10#$n))")
  a=$(curl -s -o /dev/null -w '%{http_code}' --max-time 5 http://127.0.0.1:8080/)
  f=$(curl -s -o /dev/null -w '%{http_code}' --max-time 3 "$FAKE_URL/health")
  if [ "$a" != 200 ] || [ "$f" != 200 ]; then echo "cap$NN PARADO: 8080=$a falso=$f" >> "$OUT/_progresso.txt"; exit 3; fi
  pid=$(cat "rec/.runtime/fake$PORTA.pid" 2>/dev/null)
  if ! tr '\0' '\n' < "/proc/$pid/environ" 2>/dev/null | grep -q '^FAKE_NOW=2026-11-11T08:50:00-03:00$'; then
    echo "cap$NN PARADO: o falso $PORTA não é o do T7 (pid ${pid:-?})" >> "$OUT/_progresso.txt"; exit 5
  fi
  livre=$(df --output=avail -k /home/claude | tail -1)
  if [ "$livre" -lt 1572864 ]; then echo "cap$NN PARADO: disco $((livre / 1024)) MB" >> "$OUT/_progresso.txt"; exit 4; fi
  curl -s -XPOST "$FAKE_URL/__dev/unknowns/clear" >/dev/null
  bash rec/t7/rodar.sh "$n" > "$OUT/$NN.out" 2>&1
  curl -s "$FAKE_URL/__dev/unknowns" > "$OUT/$NN.unk.json"
  echo "cap$NN fim $(date +%H:%M) | $(grep -m1 'maxLate' "$OUT/$NN.out" | grep -o 'falhos.*')" >> "$OUT/_progresso.txt"
done
echo "LOTE FIM $(date +%H:%M): $*" >> "$OUT/_progresso.txt"
