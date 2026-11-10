#!/usr/bin/env python3
"""T18 · mostra, por linha da narração, cada palavra com o tempo de início (para escolher as âncoras `A(linha, palavra)` do robô).
Uso: python3 -I rec/t12/palavras.py 03 [04 ...]"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
for a in sys.argv[1:]:
    d = json.load(open(os.path.join(HERE, '..', '..', 't12', 'narracao', f'cap{int(a):02d}.json'), encoding='utf8'))
    print(f'=== cap{int(a):02d}  dur {d["dur"]:.1f}s')
    for l in d['linhas']:
        ws = [w for w in d['words'] if w['linha'] == l['i']]
        print(f'L{l["i"] + 1} ({l["s"]:.2f}-{l["e"]:.2f}): ' + ' '.join(f'{w["w"]}[{w["s"]:.1f}]' for w in ws))
