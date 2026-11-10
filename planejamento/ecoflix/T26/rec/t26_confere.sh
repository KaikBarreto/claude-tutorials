#!/usr/bin/env bash
# T26 · depois de um ensaio/gravação: resumo.py (falhas, atrasos, voz:), SEM ALVO, avisos de erro na tela e conferências tela x fala.
#   bash rec/t26/t26_confere.sh NN [--ens] [--tudo]
set -uo pipefail
TUT_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$TUT_HOME"
NN=$(printf %02d "$((10#$1))"); shift
python3 -I rec/t26/resumo.py "$NN" "$@" | grep -vE "^ +[0-9]+ (mark|wait|pause) " 
OUT="rec/t26/.cap$NN.$([[ " $* " == *" --ens "* ]] && echo ens || echo final).out"
grep -c "SEM ALVO" "$OUT" 2>/dev/null | sed 's/^/SEM ALVO no log: /'
ACT="rec/t26/$([[ " $* " == *" --ens "* ]] && echo _ens/)t26-cap$NN.actions.json"
python3 - "$ACT" <<'PY'
import json, sys
a = json.load(open(sys.argv[1]))
av = [x for x in a['actions'] if x.get('label') == 'avisos de erro na tela']
print('avisos na tela:', av[0].get('value') if av else '(sem o passo final)')
print('SEM ALVO nos eval:', [x.get('label') for x in a['actions'] if x.get('do') == 'eval' and 'SEM ' in str(x.get('value'))])
print('video', a['video'].get('durationS'), 's; late', a['late'])
PY
