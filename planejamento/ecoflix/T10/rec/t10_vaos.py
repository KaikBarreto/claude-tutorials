#!/usr/bin/env python3
"""T10 · lista os vãos entre palavras (>= 0,12 s) da narração ORIGINAL de um capítulo: python3 -I t10_vaos.py NN [t0 t1]"""
import json, os, sys
nn = f'{int(sys.argv[1]):02d}'
R = '/home/claude/ecoflix/t10/narracao'
p = os.path.join(R, 'emendas', f'cap{nn}.orig.json')
if not os.path.exists(p): p = os.path.join(R, f'cap{nn}.json')
d = json.load(open(p, encoding='utf8'))
t0, t1 = (float(sys.argv[2]), float(sys.argv[3])) if len(sys.argv) > 3 else (0, 1e9)
w = d['words']
for a, b in zip(w, w[1:]):
    g = b['s'] - a['e']
    if g >= 0.12 and t0 <= a['e'] <= t1:
        print(f"{a['e']:7.2f}-{b['s']:7.2f} gap {g:.2f}  {a['w']} | {b['w']}")
