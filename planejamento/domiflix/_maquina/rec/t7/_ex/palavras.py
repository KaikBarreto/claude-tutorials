#!/usr/bin/env python3
"""Mostra as palavras de um capítulo com o instante de cada uma (para escolher as âncoras do gerar.py).
Uso: python3 -I rec/t7/_ex/palavras.py NN [linha]"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
n = int(sys.argv[1])
so = int(sys.argv[2]) if len(sys.argv) > 2 else None
d = json.load(open(os.path.join(HERE, '..', '..', '..', 't7', 'narracao', f'cap{n:02d}.json')))
por = {}
for w in d['words']:
    por.setdefault(w['linha'], []).append(w)
for li in sorted(por):
    if so is not None and li + 1 != so:
        continue
    print(f'L{li + 1} ({d["linhas"][li]["s"]:.2f}s):', '  '.join(f'{w["w"]}@{w["s"]:.1f}' for w in por[li]))
