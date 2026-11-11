#!/usr/bin/env bash
# T14 · um capítulo numa trava só: ensaio rápido (sem `at`) e, se ele sair limpo (0 falho, nenhum "SEM ALVO"), a gravação completa
# com os tempos da fala. O MP4 da gravação é apagado logo (ficam actions/telemetry e a folha de contato para olhar).
#   bash rec/t14/t14_capitulo.sh NN [--so-rapido|--so-completo]
set -u
cd "$(dirname "$0")/../.."
export FAKE_PORT=54314 FAKE_URL=http://127.0.0.1:54314 FAKE_NOW=2026-11-10T08:30:00-03:00
: "${TUT_USER:=rafael@reciclavalemetais.example}"; export TUT_USER
[ -n "${TUT_SENHA:-}" ] || { TUT_SENHA="ensaio-$RANDOM$RANDOM"; export TUT_SENHA; }
nn=$(printf '%02d' "$((10#$1))"); modo="${2:-}"
pid=$(cat rec/.runtime/fake54314.pid 2>/dev/null)
tr '\0' '\n' < /proc/$pid/environ 2>/dev/null | grep -qx 'FAKE_PORT=54314' && tr '\0' '\n' < /proc/$pid/environ | grep -qx "FAKE_NOW=$FAKE_NOW" \
  || { echo "cap$nn: instância 54314 ausente ou de outro"; exit 3; }
python3 -I rec/t14/gerar.py "$nn" >/dev/null || exit 2
python3 -I rec/t14/ensaio.py "$nn" >/dev/null
flock .heavy.lock bash -c '
  nn=$1; modo=$2
  if [ "$modo" != "--so-completo" ]; then
    timeout 600 node rec/record.mjs rec/t14/_ens/cap$nn.json --rapido > rec/t14/.ens-$nn.out 2>&1
    rm -f rec/t14/_ens/t14-cap$nn.mp4 rec/t14/_ens/t14-cap$nn.contact.jpg
    r=$(python3 -I rec/t14/resumo.py $nn --ens 2>&1 | head -1); echo "RAPIDO $r"
    echo "$r" | grep -q "falhos 0," && ! grep -q "SEM ALVO" rec/t14/.ens-$nn.out || { echo "cap$nn: rápido com falha, sem gravação"; exit 0; }
    python3 -I rec/t14/prever.py $nn --ens 2>&1 | grep -iE "máx|max|prev" | tail -2
  fi
  [ "$modo" = "--so-rapido" ] && exit 0
  timeout 900 node rec/record.mjs rec/t14/cap$nn.json > rec/t14/.rec-$nn.out 2>&1
  rm -f rec/t14/t14-cap$nn.mp4
  echo "COMPLETO $(python3 -I rec/t14/resumo.py $nn 2>&1 | head -1)"
' _ "$nn" "$modo"
grep -h "SEM ALVO" "rec/t14/.ens-$nn.out" "rec/t14/.rec-$nn.out" 2>/dev/null | head -2
