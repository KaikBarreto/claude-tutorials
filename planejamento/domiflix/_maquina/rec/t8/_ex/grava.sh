#!/usr/bin/env bash
# uso: grava.sh NN... (gravação final de cada capítulo, uma trava por capítulo; para no primeiro com falha, atraso >= 0,8 s ou aviso na tela)
cd /home/claude/domiflix
export TUT_HOME=/home/claude/domiflix FAKE_URL=http://127.0.0.1:54325 FAKE_NOW=2026-11-03T09:00:00-03:00
rm -f rec/t8/_ex/grava.done
for n in "$@"; do
  livre=$(df --output=avail -BG /home/claude | tail -1 | tr -dc 0-9)
  if [ "$livre" -lt 3 ]; then echo "disco baixo ($livre G) antes do $n" > rec/t8/_ex/grava.done; exit 0; fi
  bash rec/t8/rodar.sh $n --seed > rec/t8/_ex/grava-$n.txt 2>&1
  l=$(grep -E "^cap[0-9]+: [0-9]+ passos, v" rec/t8/_ex/grava-$n.txt)
  ml=$(echo "$l" | sed -n 's/.*maxLate \([0-9.]*\).*/\1/p')
  if ! echo "$l" | grep -q "falhos 0," || ! grep -q 'avisos de erro na tela.*\[\]' rec/t8/_ex/grava-$n.txt || awk "BEGIN{exit !(${ml:-9} >= 0.8)}"; then echo "revisar $n (maxLate=$ml)" > rec/t8/_ex/grava.done; exit 0; fi
done
echo fim > rec/t8/_ex/grava.done
