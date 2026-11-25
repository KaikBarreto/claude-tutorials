#!/bin/bash
# T10 · ajuste de ritmo: aj NN [T:DUR ...] -> pausas.py (recomeça do original) + gerar.py NN + prever.py NN --ens (maiores atrasos)
cd /home/claude/ecoflix || exit 2
nn=$(printf %02d $((10#$1))); shift
if [ $# -gt 0 ]; then python3 -I t10/narracao/pausas.py $nn "$@" >/dev/null || { echo "pausas falhou"; exit 3; }; fi
python3 -I rec/t10/gerar.py $nn | grep -v "^cap" 
python3 -I rec/t10/prever.py $nn --ens | grep -E "ATRASO|maior atraso"
