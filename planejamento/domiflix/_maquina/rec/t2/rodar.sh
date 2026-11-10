#!/usr/bin/env bash
# T2 · Uso: rec/t2/rodar.sh NN [--ensaio]  -> gera o roteiro do robô, confere (--check), grava o capítulo NN (flock + nice), resume.
# O Supabase falso do T2 é a instância da porta 54324 (FAKE_PORT=54324 FAKE_SEEDS_DIR=<seeds-extra/t2/_base> rec/run.sh fake); o app (8080) é compartilhado.
# Uma trava por capítulo. Depois da gravação (ainda dentro da trava) imprime o estado do banco que o robô deixou (usuários, permissões,
# cargos), para conferir com a semente apos-capNN. TUT_SENHA precisa estar no ambiente (a senha de demonstração digitada no formulário).
set -uo pipefail
cd /home/claude/domiflix
export TUT_HOME=/home/claude/domiflix FAKE_URL=http://127.0.0.1:54324 FAKE_NOW="2026-11-03T09:00:00-03:00"
: "${TUT_SENHA:?defina TUT_SENHA no ambiente (senha de demonstração; nunca em arquivo)}"
NN=$(printf '%02d' "$((10#$1))")
# a instância 54324 precisa ser a minha: com o relógio e a base do T2
PIDF=rec/.runtime/fake54324.pid
if [ ! -r "$PIDF" ] || ! tr '\0' '\n' < "/proc/$(cat "$PIDF")/environ" 2>/dev/null | grep -q '^FAKE_SEEDS_DIR=.*seeds-extra/t2/_base$'; then
  echo "A instância 54324 não está de pé com a base do T2 (FAKE_SEEDS_DIR): suba com FAKE_PORT=54324 FAKE_NOW=... FAKE_SEEDS_DIR=... rec/run.sh fake"; exit 4
fi
tr '\0' '\n' < "/proc/$(cat "$PIDF")/environ" | grep -q '^FAKE_NOW=2026-11-03T09:00:00-03:00$' || { echo "A instância 54324 está sem FAKE_NOW=2026-11-03T09:00:00-03:00"; exit 4; }
python3 -I rec/t2/gerar.py "$((10#$NN))" | tail -3
node rec/record.mjs rec/t2/cap$NN.json --check | tail -3
CMD="node rec/record.mjs rec/t2/cap$NN.json --out rec/t2 --name t2-cap$NN > rec/t2/.rec-$NN.log 2>&1; rc=\$?; node rec/t2/estado.mjs > rec/t2/.estado-$NN.log 2>&1; exit \$rc"
livre=$(df -k --output=avail /home/claude | tail -1)
if [ "$livre" -lt $((3 * 1024 * 1024)) ]; then echo "DISCO BAIXO (< 3 GiB): paro"; exit 3; fi
if [ -n "${TUT_LOCKED:-}" ]; then run() { nice -n 10 bash -c "$CMD"; }; else run() { flock "$TUT_HOME/.heavy.lock" nice -n 10 bash -c "$CMD"; }; fi
if ! run; then
  echo "=== GRAVAÇÃO FALHOU (cauda do log) ==="; tail -25 rec/t2/.rec-$NN.log
fi
python3 -I rec/t2/resumo.py "$((10#$NN))" 2>&1 | head -140
echo "--- estado do banco:"; cat rec/t2/.estado-$NN.log 2>/dev/null | head -40
