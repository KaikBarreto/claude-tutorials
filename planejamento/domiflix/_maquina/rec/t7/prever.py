#!/usr/bin/env python3
"""T7 · prévia do ritmo de um roteiro (sem abrir o navegador): estima quando cada passo começa/termina e avisa onde o
robô tende a se atrasar em relação ao `at`. Uso: python3 rec/t7/prever.py 03 [05 ...]  (estimativa; a verdade é o actions.json)."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))

def dur(st, cps_default, pace):
    d = st['do']
    if d == 'mark': return 0.0
    # medido no cap. 1 (celular, pace 0,4): click 0,52 a 0,56 s; hover = ~0,7 s de deslocamento (0,3 a 1,0: depende da distância) + `seconds`;
    # apontar = scroll com `point` ~0,55 s + type sem clique ~0,3 s
    if d in ('click', 'dblclick'): return 0.75 * (0.6 + 0.4 * pace)
    if d == 'hover': return 0.9 * (0.6 + 0.4 * pace) + st.get('seconds', 0.9)
    if d == 'type':
        cps = st.get('cps') or cps_default
        if st.get('noClick'): return 0.3 + len(st['text']) / cps
        mv = 0.9 * (0.6 + 0.4 * pace) + 0.2 + 0.25
        return mv + (0.4 if st.get('clear') else 0) + len(st['text']) / cps
    if d == 'select': return 1.8
    if d == 'drag': return 2.4
    if d == 'press': return 0.35
    if d in ('pause', 'wait'): return st.get('seconds', 1)
    if d == 'waitFor': return 0.35
    if d == 'scroll': return 0.55
    if d == 'eval': return 0.4
    return 0.5

for n in sys.argv[1:]:
    s = json.load(open(os.path.join(HERE, f'cap{int(n):02d}.json')))
    t = 0.0
    print(f'=== cap{int(n):02d}  pace {s["pace"]} cps {s["cps"]}')
    for st in s['steps']:
        at = st.get('at')
        ini = max(t, at) if at is not None else t
        atraso = (ini - at) if at is not None and ini > at + 1e-9 else 0.0
        fim = ini + dur(st, s['cps'], s['pace'])
        flag = f'  <-- ATRASO {atraso:.1f}s' if atraso > 0.5 else ''
        print(f'  {ini:6.2f}->{fim:6.2f}  at={at if at is not None else "-":>6}  {st["do"]:7} {(st.get("label") or st.get("name") or "")[:58]}{flag}')
        t = fim
