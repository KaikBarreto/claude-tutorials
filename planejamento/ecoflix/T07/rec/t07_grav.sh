#!/usr/bin/env bash
# T07 · gravação COMPLETA (com os tempos da voz estimada) de cada capítulo, um flock por capítulo, na MINHA instância (54307): gera o
# roteiro, mostra a previsão de atraso (prever.py --ens), grava, resume (resumo.py) e apaga o MP4 (fica a folha de contato para olhar).
# Uso: bash rec/t07/t07_grav.sh 00 01 ...   Não edite com um lote rodando (lição 75).
set -u
cd "$(dirname "$0")/../.."
export FAKE_NOW=2026-11-10T08:35:00-03:00 FAKE_URL=http://127.0.0.1:54307
export TUT_USER="${TUT_USER:-rafael@reciclavalemetais.example}"
[ -n "${TUT_SENHA:-}" ] || export TUT_SENHA="$(head -c 12 /dev/urandom | base64 | tr -dc 'A-Za-z0-9')"   # só na memória
for nn in "$@"; do
  pid=$(cat rec/.runtime/fake54307.pid 2>/dev/null)
  if ! tr '\0' '\n' < /proc/$pid/environ 2>/dev/null | grep -q "^FAKE_NOW=$FAKE_NOW"; then
    echo "##### cap$nn: a instância 54307 não é a minha (ou caiu): parei"; exit 2
  fi
  python3 -I rec/t07/gerar.py "$nn" >/dev/null || { echo "##### cap$nn: gerar.py falhou"; continue; }
  falta=$(python3 -I -c "import json,os;d=json.load(open('rec/t07/cap$nn.json'));print(' '.join(s for s in d.get('seedExtra',[]) if not os.path.exists('rec/mundo/seeds-extra/'+s+'.json')))")
  [ -n "$falta" ] && { echo "##### cap$nn: falta a semente $falta: pulei"; continue; }
  python3 -I rec/t07/prever.py "$nn" --ens 2>&1 | tail -4
  dur=$(python3 -I -c "import json;print(int(json.load(open('t07/narracao/cap$nn.json'))['dur']*3+120))")
  echo "##### cap$nn $(date +%H:%M:%S) na fila (prazo ${dur}s)"
  flock .heavy.lock timeout "$dur" node rec/record.mjs "rec/t07/cap$nn.json" > "rec/t07/cap$nn.out" 2>&1
  echo "##### cap$nn $(date +%H:%M:%S) gravado (saída $?)"
  python3 -I rec/t07/resumo.py "$nn" > "rec/t07/cap$nn.resumo.txt" 2>&1
  head -3 "rec/t07/cap$nn.resumo.txt"; grep -h "SEM ALVO\|DIFERENTE\|ERRO" "rec/t07/cap$nn.resumo.txt" | head -6
  rm -f "/home/claude/ecoflix/rec/t07/t07-cap$nn.mp4"
done
echo "##### lote fim $(date +%H:%M:%S)"
