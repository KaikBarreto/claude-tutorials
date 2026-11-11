#!/usr/bin/env bash
# T16 · exploração sob a trava (uma por vez). Uso: bash rec/t16/t16_ex.sh eN   (lê rec/t16/_ex/eN.json, escreve rec/t16/_ex/eN/ e eN.out)
set -u
cd "$(dirname "$0")/../.."
export FAKE_NOW=2026-11-10T08:30:00-03:00 FAKE_URL=http://127.0.0.1:54316
PID=$(cat rec/.runtime/fake54316.pid 2>/dev/null)
tr '\0' '\n' < /proc/$PID/environ 2>/dev/null | grep -qx "FAKE_PORT=54316" || { echo "instância 54316 fora do ar"; exit 3; }
flock .heavy.lock timeout 900 node rec/t16/explorar.mjs rec/t16/_ex/$1.json --out rec/t16/_ex/$1 > rec/t16/_ex/$1.out 2>&1
echo "rc=$? $(date +%T)"
