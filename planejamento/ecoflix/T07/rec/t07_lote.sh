#!/usr/bin/env bash
# T07 · lote de ensaios RÁPIDOS (um flock por capítulo): gera o roteiro, prepara o ensaio, grava com --rapido na MINHA instância
# (54307), resume, grava a semente apos-capNN dos capítulos que mudam o banco e apaga o MP4. Uso: bash rec/t07/t07_lote.sh 02 03 05 ...
# Não edite este arquivo com um lote rodando (lição 75): copie para outro nome.
set -u
cd "$(dirname "$0")/../.."
export FAKE_NOW=2026-11-10T08:35:00-03:00 FAKE_URL=http://127.0.0.1:54307
export TUT_USER="${TUT_USER:-rafael@reciclavalemetais.example}"
[ -n "${TUT_SENHA:-}" ] || export TUT_SENHA="$(head -c 12 /dev/urandom | base64 | tr -dc 'A-Za-z0-9')"   # só na memória
SEMENTES=" 03 09 11 12 14 15 "
for nn in "$@"; do
  pid=$(cat rec/.runtime/fake54307.pid 2>/dev/null)
  if ! tr '\0' '\n' < /proc/$pid/environ 2>/dev/null | grep -q "^FAKE_NOW=$FAKE_NOW"; then
    echo "##### cap$nn: a instância 54307 não é a minha (ou caiu): parei"; exit 2
  fi
  python3 -I rec/t07/gerar.py "$nn" >/dev/null || { echo "##### cap$nn: gerar.py falhou"; continue; }
  python3 -I rec/t07/ensaio.py "$nn" >/dev/null
  echo "##### cap$nn $(date +%H:%M:%S) na fila"
  sem=0; case "$SEMENTES" in *" $nn "*) sem=1 ;; esac
  # a semente sai dentro da MESMA trava da gravação (lição 45): ninguém reseta a instância entre a gravação e a leitura
  flock .heavy.lock bash -c "timeout 900 node rec/record.mjs rec/t07/_ens/cap$nn.json --rapido > rec/t07/_ens/cap$nn.out 2>&1; echo saida=\$?; \
    [ $sem = 1 ] && python3 -I rec/t07/t07_semente.py $nn > rec/t07/_ens/cap$nn.semente.txt 2>&1; true"
  echo "##### cap$nn $(date +%H:%M:%S) gravado"
  python3 -I rec/t07/resumo.py "$nn" --ens > "rec/t07/_ens/cap$nn.resumo.txt" 2>&1
  head -12 "rec/t07/_ens/cap$nn.resumo.txt"
  grep -h "SEM ALVO\|DIFERENTE" "rec/t07/_ens/cap$nn.resumo.txt" | head -8
  [ $sem = 1 ] && tail -14 "rec/t07/_ens/cap$nn.semente.txt"
  rm -f "/home/claude/ecoflix/rec/t07/_ens/t07-cap$nn.mp4"
done
echo "##### lote fim $(date +%H:%M:%S)"
