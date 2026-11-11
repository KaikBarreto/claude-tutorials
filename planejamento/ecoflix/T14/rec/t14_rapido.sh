#!/usr/bin/env bash
# T14 · ensaio RÁPIDO de um capítulo numa trava (regra de 11/11 18:46): gravado com a montagem do MP4 para a folha de contato,
# o MP4 apagado logo e a folha guardada para olhar; resumo e prever.py no fim. Desiste da fila depois de 100 min (o fundo morre em 2 h).
#   bash rec/t14/t14_rapido.sh NN
set -u
cd "$(dirname "$0")/../.."
export FAKE_PORT=54314 FAKE_URL=http://127.0.0.1:54314 FAKE_NOW=2026-11-10T08:30:00-03:00
: "${TUT_USER:=rafael@reciclavalemetais.example}"; export TUT_USER
[ -n "${TUT_SENHA:-}" ] || { TUT_SENHA="ensaio-$RANDOM$RANDOM"; export TUT_SENHA; }
nn=$(printf '%02d' "$((10#$1))")
pid=$(cat rec/.runtime/fake54314.pid 2>/dev/null)
tr '\0' '\n' < /proc/$pid/environ 2>/dev/null | grep -qx 'FAKE_PORT=54314' && tr '\0' '\n' < /proc/$pid/environ | grep -qx "FAKE_NOW=$FAKE_NOW" \
  || { echo "cap$nn: instância 54314 ausente ou de outro"; exit 3; }
python3 -I rec/t14/gerar.py "$nn" >/dev/null || exit 2
python3 -I rec/t14/ensaio.py "$nn" >/dev/null
flock -w 6000 .heavy.lock bash -c '
  nn=$1
  timeout 600 node rec/record.mjs rec/t14/_ens/cap$nn.json --rapido > rec/t14/.ens-$nn.out 2>&1
  rm -f rec/t14/_ens/t14-cap$nn.mp4
' _ "$nn" || { echo "cap$nn: SEM TRAVA (fila) ou erro $?"; exit 4; }
echo "RAPIDO $(python3 -I rec/t14/resumo.py $nn --ens 2>&1 | head -1)"
python3 -I rec/t14/prever.py $nn --ens 2>&1 | grep "maior atraso"
grep -h "SEM ALVO" "rec/t14/.ens-$nn.out" | head -2
ls rec/t14/_ens/t14-cap$nn.contact.jpg 2>/dev/null
