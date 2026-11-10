#!/usr/bin/env python3
"""Lista as palavras de uma linha da narração: python3 -I rec/t11/palavras.py CAP LINHA  (com o tempo de cada uma)"""
import json, sys, os
n, l = int(sys.argv[1]), int(sys.argv[2])
d = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 't11', 'narracao', f'cap{n:02d}.json'), encoding='utf8'))
print(f'cap{n:02d} L{l} ({d["linhas"][l-1]["s"]:.1f}-{d["linhas"][l-1]["e"]:.1f}):', ' '.join(f'{w["w"]}@{w["s"]:.1f}' for w in d['words'] if w['linha'] == l - 1))
