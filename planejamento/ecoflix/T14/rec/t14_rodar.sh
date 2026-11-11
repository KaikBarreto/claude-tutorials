#!/usr/bin/env bash
# T14 · roda um capítulo por vez, cada um sob a sua trava: gera o roteiro, confere a instância 54314 e grava.
#   bash rec/t14/t14_rodar.sh NN [NN ...] [--ens]   (--ens: ensaio rápido sem `at`; sem ele, a gravação com os tempos da fala)
# O vídeo do ensaio rápido é apagado logo (fica o actions.json/telemetry.json); o da gravação fica para olhar a folha de contato.
set -u
cd "$(dirname "$0")/../.."
export FAKE_PORT=54314 FAKE_URL=http://127.0.0.1:54314 FAKE_NOW=2026-11-10T08:30:00-03:00
: "${TUT_USER:=rafael@reciclavalemetais.example}"; export TUT_USER
[ -n "${TUT_SENHA:-}" ] || { TUT_SENHA="ensaio-$RANDOM$RANDOM"; export TUT_SENHA; }
ENS=0; CAPS=()
for a in "$@"; do [ "$a" = "--ens" ] && ENS=1 || CAPS+=("$a"); done
pid=$(cat rec/.runtime/fake54314.pid 2>/dev/null)
if ! tr '\0' '\n' < /proc/$pid/environ 2>/dev/null | grep -qx 'FAKE_PORT=54314' || ! tr '\0' '\n' < /proc/$pid/environ | grep -qx "FAKE_NOW=$FAKE_NOW"; then
  echo "instância 54314 ausente ou de outro: suba com FAKE_NOW=$FAKE_NOW FAKE_PORT=54314 bash rec/run.sh fake"; exit 3
fi
python3 -I rec/t14/gerar.py "${CAPS[@]}" >/dev/null || exit 2
for nn in "${CAPS[@]}"; do
  nn=$(printf '%02d' "$((10#$nn))")
  if [ $ENS = 1 ]; then
    python3 -I rec/t14/ensaio.py "$nn" >/dev/null
    flock .heavy.lock timeout 1500 node rec/record.mjs "rec/t14/_ens/cap$nn.json" --rapido > "rec/t14/.ens-$nn.out" 2>&1
    rm -f "rec/t14/_ens/t14-cap$nn.mp4"
    python3 -I rec/t14/resumo.py "$nn" --ens | head -3
  else
    flock .heavy.lock timeout 1800 node rec/record.mjs "rec/t14/cap$nn.json" > "rec/t14/.rec-$nn.out" 2>&1
    python3 -I rec/t14/resumo.py "$nn" | head -3
  fi
  grep -h "SEM ALVO" "rec/t14/.ens-$nn.out" "rec/t14/.rec-$nn.out" 2>/dev/null | head -3
done
curl -s "$FAKE_URL/__dev/unknowns" | head -c 400; echo
