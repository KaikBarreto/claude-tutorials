#!/usr/bin/env bash
# T07 · ensaio rápido + gravação completa do MESMO capítulo dentro de UMA trava (um capítulo por trava; a fila passou de 50 jobs):
# gera o roteiro, grava o ensaio --rapido, grava a semente apos-capNN (se o capítulo muda o banco e o ensaio teve 0 falho) e, se o
# ensaio teve 0 falho, grava a versão completa com os tempos da voz estimada; fora da trava, resume os dois e apaga os MP4.
# Uso: bash rec/t07/t07_par.sh 05 06 01c ...   (NNc = só a gravação completa: capítulo com o ensaio rápido já aprovado)
# Não edite este arquivo com um lote rodando (lição 75): copie para outro nome. (par2: --check antes da fila e ensaio --no-encode.)
set -u
cd "$(dirname "$0")/../.."
export FAKE_NOW=2026-11-10T08:35:00-03:00 FAKE_URL=http://127.0.0.1:54307
export TUT_USER="${TUT_USER:-rafael@reciclavalemetais.example}"
[ -n "${TUT_SENHA:-}" ] || export TUT_SENHA="$(head -c 12 /dev/urandom | base64 | tr -dc 'A-Za-z0-9')"   # só na memória
SEMENTES=" 03 09 11 12 14 15 "
for arg in "$@"; do
  nn=${arg%c}; so_completo=0; [ "$arg" != "$nn" ] && so_completo=1
  pid=$(cat rec/.runtime/fake54307.pid 2>/dev/null)
  if ! tr '\0' '\n' < /proc/$pid/environ 2>/dev/null | grep -q "^FAKE_NOW=$FAKE_NOW"; then
    echo "##### cap$nn: a instância 54307 não é a minha (ou caiu): parei"; exit 2
  fi
  python3 -I rec/t07/gerar.py "$nn" >/dev/null || { echo "##### cap$nn: gerar.py falhou"; continue; }
  python3 -I rec/t07/ensaio.py "$nn" >/dev/null
  falta=$(python3 -I -c "import json,os;d=json.load(open('rec/t07/cap$nn.json'));print(' '.join(s for s in d.get('seedExtra',[]) if not os.path.exists('rec/mundo/seeds-extra/'+s+'.json')))")
  [ -n "$falta" ] && { echo "##### cap$nn: falta a semente $falta: pulei"; continue; }
  node rec/record.mjs "rec/t07/cap$nn.json" --check > "rec/t07/_ens/cap$nn.check" 2>&1 || { echo "##### cap$nn: --check falhou: $(tail -3 rec/t07/_ens/cap$nn.check | tr '\n' ' ')"; continue; }
  sem=0; case "$SEMENTES" in *" $nn "*) sem=1 ;; esac
  dur=$(python3 -I -c "import json;print(int(json.load(open('t07/narracao/cap$nn.json'))['dur']*3+120))")
  echo "##### cap$nn $(date +%H:%M:%S) na fila (só completa: $so_completo)"
  flock .heavy.lock bash -c "
    ok=1
    if [ $so_completo = 0 ]; then
      timeout 900 node rec/record.mjs rec/t07/_ens/cap$nn.json --rapido --no-encode > rec/t07/_ens/cap$nn.out 2>&1
      python3 -I -c \"import json,sys;a=json.load(open('rec/t07/_ens/t07-cap$nn.actions.json'))['actions'];sys.exit(1 if [x for x in a if x.get('error') or x.get('ok') is False] else 0)\" 2>/dev/null || ok=0
      [ $sem = 1 ] && [ \$ok = 1 ] && python3 -I rec/t07/t07_semente.py $nn > rec/t07/_ens/cap$nn.semente.txt 2>&1
    fi
    [ \$ok = 1 ] && timeout $dur node rec/record.mjs rec/t07/cap$nn.json > rec/t07/cap$nn.out 2>&1
    true"
  echo "##### cap$nn $(date +%H:%M:%S) gravado"
  if [ $so_completo = 0 ]; then
    python3 -I rec/t07/resumo.py "$nn" --ens > "rec/t07/_ens/cap$nn.resumo.txt" 2>&1
    echo "ensaio: $(head -1 rec/t07/_ens/cap$nn.resumo.txt)"; grep -h "SEM ALVO\|ERRO\|DIFERENTE" "rec/t07/_ens/cap$nn.resumo.txt" | head -5
    [ $sem = 1 ] && tail -3 "rec/t07/_ens/cap$nn.semente.txt"
  fi
  if [ -f "rec/t07/t07-cap$nn.actions.json" ] && [ "rec/t07/t07-cap$nn.actions.json" -nt "rec/t07/cap$nn.json" ]; then
    python3 -I rec/t07/resumo.py "$nn" > "rec/t07/cap$nn.resumo.txt" 2>&1
    echo "completa: $(head -1 rec/t07/cap$nn.resumo.txt)"; sed -n 2p "rec/t07/cap$nn.resumo.txt"
    grep -h "SEM ALVO\|ERRO\|DIFERENTE" "rec/t07/cap$nn.resumo.txt" | head -5
  else
    echo "completa: não gravada"
  fi
  rm -f "/home/claude/ecoflix/rec/t07/_ens/t07-cap$nn.mp4" "/home/claude/ecoflix/rec/t07/_ens/t07-cap$nn.contact.jpg" "/home/claude/ecoflix/rec/t07/t07-cap$nn.mp4"
done
echo "##### lote fim $(date +%H:%M:%S)"
