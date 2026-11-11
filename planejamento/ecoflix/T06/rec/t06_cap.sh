#!/usr/bin/env bash
# T06 · UM capítulo, numa trava só: ensaio rápido (ensaio.py + --rapido + resumo --ens) e, se ele fechar (0 falho, nenhum
# "SEM ALVO"), a gravação completa com os tempos estimados (+ resumo). Uso: bash rec/t06/t06_cap.sh NN|8b [--so-completo|--so-rapido]
# A instância 54306 sobe FORA da trava, com o FAKE_NOW do capítulo (o mesmo de FAKE_NOW em gerar.py). TUT_USER/TUT_SENHA do ambiente.
set -uo pipefail
cd "$(dirname "$0")/../.."          # $TUT_HOME
CAP="$1"; MODO="${2:-}"
PORTA=54306
N="${CAP%b}"; N=$((10#$N))
case "$N" in
  0|1) NOW=2026-11-10T08:30:00-03:00 ;;
  2) NOW=2026-11-10T08:30:55-03:00 ;;
  3|4|5) NOW=2026-11-10T08:41:50-03:00 ;;
  6|7|8|9) NOW=2026-11-10T08:45:00-03:00 ;;
  10) NOW=2026-11-10T17:40:00-03:00 ;;
  11) NOW=2026-11-10T17:42:40-03:00 ;;
  *) NOW=2026-11-10T17:44:00-03:00 ;;
esac
NN=$(printf '%02d' "$N"); [ "${CAP: -1}" = b ] && NN="${NN}b"
PIDF=rec/.runtime/fake${PORTA}.pid
atual=""
if [ -f "$PIDF" ] && [ -r "/proc/$(cat "$PIDF")/environ" ]; then
  env_=$(tr '\0' '\n' < "/proc/$(cat "$PIDF")/environ")
  [ "$(sed -n 's/^FAKE_PORT=//p' <<<"$env_")" = "$PORTA" ] && atual=$(sed -n 's/^FAKE_NOW=//p' <<<"$env_")
fi
if [ "$atual" != "$NOW" ] || [ -n "${REINICIA:-}" ]; then
  echo "== instância $PORTA com FAKE_NOW=$NOW (era: ${atual:-nenhuma})"
  FAKE_NOW=$NOW FAKE_PORT=$PORTA bash rec/run.sh fake 9>&- | tail -1
fi
export FAKE_URL=http://127.0.0.1:$PORTA FAKE_NOW=$NOW
: "${TUT_USER:?defina TUT_USER}"; : "${TUT_SENHA:?defina TUT_SENHA}"
python3 -I rec/t06/gerar.py "$CAP" >/dev/null && python3 -I rec/t06/ensaio.py "$CAP" >/dev/null || { echo "gerar/ensaio falhou"; exit 1; }
export CAP NN MODO
flock .heavy.lock bash -c '
  if [ "$MODO" != "--so-completo" ]; then
    node rec/record.mjs "rec/t06/_ens/cap$NN.json" --rapido > "rec/t06/_ens/.cap$NN.out" 2>&1
    python3 -I rec/t06/resumo.py "$CAP" --ens --tudo > "rec/t06/_ens/cap$NN.resumo.txt" 2>&1
    rm -f "rec/t06/_ens/t06-cap$NN.mp4" "rec/t06/_ens/t06-cap$NN.contact.jpg"
    falhos=$(sed -n "1s/.*falhos \([0-9]*\).*/\1/p" "rec/t06/_ens/cap$NN.resumo.txt")
    semalvo=$(grep -c "SEM ALVO" "rec/t06/_ens/.cap$NN.out")
    echo "rápido: falhos=${falhos:-?} SEM_ALVO=$semalvo"
    [ "${falhos:-1}" = 0 ] && [ "$semalvo" = 0 ] || exit 0
    [ "$MODO" = "--so-rapido" ] && exit 0
  fi
  node rec/record.mjs "rec/t06/cap$NN.json" > "rec/t06/.cap$NN.out" 2>&1
  python3 -I rec/t06/resumo.py "$CAP" > "rec/t06/cap$NN.resumo.txt" 2>&1
  echo "completo: $(head -1 rec/t06/cap$NN.resumo.txt) SEM_ALVO=$(grep -c "SEM ALVO" rec/t06/.cap$NN.out)"
'
curl -s "$FAKE_URL/__dev/unknowns" | python3 -c "import json,sys; d=json.load(sys.stdin); print('desconhecidos:', [i['kind']+' '+i['name'] for i in d['items'] if i['kind']!='TABELA_SEM_SEED'])"
