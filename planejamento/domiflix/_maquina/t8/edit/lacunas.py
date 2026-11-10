#!/usr/bin/env python3
"""T12 · maior trecho de cada capítulo SEM zoom (z >= 1,2), destaque ou ilustração (regra de 04/11: nada parado > ~20 s). Lê out/capNN/capNN.edit.json
(regiões de câmera do render) e caps/capNN.chapter.json. uso: python3 -I lacunas.py [NN ...]"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
caps = [f'{int(a):02d}' for a in sys.argv[1:]] or [f'{i:02d}' for i in range(16)]
for nn in caps:
    p = os.path.join(HERE, 'out', f'cap{nn}', f'cap{nn}.edit.json')
    if not os.path.exists(p):
        print(f'cap{nn}: sem render'); continue
    e = json.load(open(p)); ch = json.load(open(os.path.join(HERE, 'caps', f'cap{nn}.chapter.json')))
    iv = [(r['s'], r['e']) for r in e['regions'] if r.get('z', 1) >= 1.2]
    iv += [(s['at'], s['at'] + s.get('dur', 2)) for s in ch.get('spots', [])]
    iv += [(s['at'], s['at'] + s.get('dur', 2)) for s in ch.get('illustrations', [])]
    iv.sort()
    t, pior, onde = 0.0, 0.0, 0.0
    for a, b in iv:
        if a - t > pior: pior, onde = a - t, t
        t = max(t, b)
    if e['dur'] - t > pior: pior, onde = e['dur'] - t, t
    print(f'cap{nn}: maior trecho sem zoom/destaque {pior:.1f} s (a partir de {onde:.1f} s) de {e["dur"]:.1f} s' + ('   <-- ACIMA DE 20 s' if pior > 20 else ''))
