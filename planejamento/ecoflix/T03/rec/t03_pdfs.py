#!/usr/bin/env python3
"""T03 · tira do actions.json do cap09 os PDFs que o app gerou na gravação (o robô grava uma aba só e o Chromium sem janela não tem leitor de
PDF: "a aba nova" do roteiro vira ilustração na edição, com o PDF de verdade). Grava rec/t03/cap09_pdf/<nome>.pdf e a 1ª página em PNG
(pdftoppm, 150 dpi) para a edição montar a cena (zoom no título e na linha do Cobre mel, R$ 44,20).
Uso: python3 -I rec/t03/t03_pdfs.py [--ens]"""
import base64
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
pasta = os.path.join(HERE, '_ens') if '--ens' in sys.argv else HERE
acts = json.load(open(os.path.join(pasta, 't03-cap09.actions.json'), encoding='utf8'))['actions']
saida = os.path.join(HERE, 'cap09_pdf')
os.makedirs(saida, exist_ok=True)
n = 0
for a in acts:
    v = a.get('value')
    if isinstance(v, dict) and v.get('b64'):
        arq = os.path.join(saida, v['pdf'] + '.pdf')
        with open(arq, 'wb') as f:
            f.write(base64.b64decode(v['b64']))
        n += 1
        png = ''
        if shutil.which('pdftoppm'):
            subprocess.run(['pdftoppm', '-png', '-r', '150', '-f', '1', '-l', '1', '-singlefile', arq, arq[:-4]], check=False)
            png = f' + {os.path.basename(arq[:-4])}.png'
        print(f'{os.path.relpath(arq, HERE)} ({v.get("bytes")} bytes){png}')
    elif isinstance(v, str) and v.startswith('SEM PDF'):
        print(f'passo {a.get("i")}: SEM PDF ({a.get("label")})')
print(f'{n} PDF(s) em {os.path.relpath(saida, HERE)}')
