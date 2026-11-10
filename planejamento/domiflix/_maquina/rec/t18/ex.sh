#!/usr/bin/env bash
# T18 · UMA exploração por trava (navegador só sob `flock $TUT_HOME/.heavy.lock nice -n 10`): rec/t18/ex.sh NOME
#   lê rec/t18/_ex/NOME.json, grava fotos/log em rec/t18/_ex/out-NOME/ e rec/t18/_ex/NOME.log.
# Instância própria do Supabase falso do agente B (porta 54322, FAKE_NOW igual ao do robô).
set -uo pipefail
cd /home/claude/domiflix
export TUT_HOME=/home/claude/domiflix FAKE_URL=http://127.0.0.1:54322 FAKE_NOW="2026-11-11T11:00:00-03:00"
NOME="${1:?uso: rec/t18/ex.sh NOME}"
OUT="rec/t18/_ex/out-${NOME}"
mkdir -p "$OUT"
flock "$TUT_HOME/.heavy.lock" nice -n 10 node rec/t18/explorar.mjs "rec/t18/_ex/${NOME}.json" --out "$OUT" > "rec/t18/_ex/${NOME}.log" 2>&1
echo "exploração ${NOME} rc=$? ($(date +%H:%M:%S))"
