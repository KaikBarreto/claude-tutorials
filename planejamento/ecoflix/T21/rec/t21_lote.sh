#!/usr/bin/env bash
# T21 · vários capítulos em sequência, UMA trava por capítulo (t21_rodar.sh pega a trava a cada um). Não edite durante a execução.
# Uso: TUT_USER=... TUT_SENHA=... bash rec/t21/t21_lote.sh "0 1 2 2b 3" [--ens]   (log em /dev/shm/t21lote.log)
cd /home/claude/ecoflix
for n in $1; do
  echo "##### cap $n ${2:-gravação} $(date +%H:%M:%S)"
  bash rec/t21/t21_rodar.sh "$n" "${2:-}" 2>&1 | grep -v "^\s*$"
done
echo "##### fim $(date +%H:%M:%S)"
