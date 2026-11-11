#!/usr/bin/env bash
# T15: ensaio de UM capítulo sob a trava pesada (uma trava por capítulo). Uso:
#   bash rec/t15/t15_ens.sh NN            ensaio rápido (sem `at`, sem MP4) -> rec/t15/_ens/  (+ resumo --ens)
#   bash rec/t15/t15_ens.sh NN completo   gravação com os tempos estimados -> rec/t15/       (+ resumo)
# Os capítulos 01, 02 e 10 regravam a semente apos-capNN a partir do que o app gravou (dentro da mesma trava).
# A senha vem do ambiente (TUT_SENHA); se faltar, usa uma aleatória (o Supabase falso aceita qualquer uma) e nunca a grava.
set -u
cd "$(dirname "$0")/../.."
NN=$(printf '%02d' "$((10#$1))"); MODO=${2:-rapido}
export FAKE_URL=http://127.0.0.1:54315 FAKE_NOW=2026-11-10T08:30:00-03:00 TUT_USER=rafael@reciclavalemetais.example
[ -n "${TUT_SENHA:-}" ] || export TUT_SENHA="$(head -c 9 /dev/urandom | base64)"
PID=$(cat rec/.runtime/fake54315.pid 2>/dev/null)
tr '\0' '\n' < /proc/$PID/environ 2>/dev/null | grep -q '^FAKE_PORT=54315$' || { echo "instância 54315 não é a minha ou está fora do ar"; exit 3; }
tr '\0' '\n' < /proc/$PID/environ | grep -q "^FAKE_NOW=$FAKE_NOW$" || { echo "FAKE_NOW da instância diferente"; exit 3; }
if [ "$MODO" = completo ]; then
  ROT=rec/t15/cap$NN.json; OUT=rec/t15/.cap$NN.out; EXTRA=""; RES=""
else
  python3 -I rec/t15/ensaio.py "$NN" >/dev/null; ROT=rec/t15/_ens/cap$NN.json; OUT=rec/t15/_ens/.cap$NN.out; EXTRA="--rapido"; RES="--ens"
fi
SEM=""
case "$NN" in 01|02|10) SEM="python3 -I rec/t15/t15_sementes.py $NN";; esac
flock .heavy.lock bash -c "timeout 900 node rec/record.mjs $ROT $EXTRA > $OUT 2>&1; echo saida=\$? >> $OUT; if ! grep -q 'FALHOU no passo' $OUT; then $SEM >> $OUT 2>&1; fi"
echo "== cap$NN $MODO: $(grep -c 'SEM ALVO' $OUT) SEM ALVO; $(tail -1 $OUT)"
python3 -I rec/t15/resumo.py "$NN" $RES 2>&1 | head -60
