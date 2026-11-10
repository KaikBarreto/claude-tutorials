#!/usr/bin/env python3
"""T11 · guarda o rascunho do assistente "Novo Contrato" que o capítulo NN deixou no sessionStorage (eval rotulado "rascunho", último passo do capítulo)
em rec/t11/_rascunhos/capNN.json. O `setup` do capítulo seguinte o devolve ao navegador (setup_retomar do gerar.py).
Uso: python3 -I rec/t11/colher.py NN [--ens]   (--ens: do ensaio rápido, rec/t11/_ens/)"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
n = int(sys.argv[1])
pasta = os.path.join(HERE, '_ens') if '--ens' in sys.argv else HERE
a = json.load(open(os.path.join(pasta, f't11-cap{n:02d}.actions.json'), encoding='utf8'))
vals = [x.get('value') for x in a['actions'] if x.get('label') == 'rascunho' and isinstance(x.get('value'), str)]
if not vals:
    raise SystemExit(f'cap{n:02d}: sem eval "rascunho" com valor (o assistente fechou ou o capítulo falhou antes do fim)')
d = json.loads(vals[-1])
os.makedirs(os.path.join(HERE, '_rascunhos'), exist_ok=True)
with open(os.path.join(HERE, '_rascunhos', f'cap{n:02d}.json'), 'w', encoding='utf8') as f:
    json.dump({'draft': vals[-1]}, f, ensure_ascii=False)
print(f'cap{n:02d}: rascunho guardado (etapa {d.get("stepKey")}, ambientes {len(d.get("environments", []))}, nome "{d.get("name")}", PMOC {d.get("isPmoc")})')
