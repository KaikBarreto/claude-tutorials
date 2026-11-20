#!/usr/bin/env python3
"""T10 · tira do actions.json do ensaio/gravação os PDFs/HTML que o app abre em aba nova (cap07 Kardex, cap13 Posição e Relatório),
grava em rec/t10/pdfs/ e mostra o texto (pdftotext) para conferir o `mostra` das ilustrações. Uso: python3 -I rec/t10/t10_pdfs.py [--ens]"""
import base64
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
pasta = os.path.join(HERE, '_ens') if '--ens' in sys.argv else HERE
os.makedirs(os.path.join(HERE, 'pdfs'), exist_ok=True)
for cap in ('07', '13'):
    try:
        a = json.load(open(os.path.join(pasta, f't10-cap{cap}.actions.json'), encoding='utf8'))
    except OSError as e:
        print(f'cap{cap}: sem actions.json ({e})')
        continue
    for x in a['actions']:
        lab, v = (x.get('label') or ''), x.get('value')
        if not (lab.startswith('PDF') or lab.startswith('HTML')) or v is None:
            continue
        if isinstance(v, dict):
            v = json.dumps(v)
        if v.startswith('HTML:'):
            nome, dados = f'cap{cap}-relatorio.html', base64.b64decode(v[5:])
        elif v.startswith('PDF:'):
            nome, dados = f'cap{cap}-kardex.pdf', base64.b64decode(v[4:])
        else:
            try:
                j = json.loads(v)
            except ValueError:
                j = None
            if j and j.get('b64'):
                nome, dados = f"cap{cap}-{j.get('pdf', 'posicao')}.pdf", base64.b64decode(j['b64'])
            elif j and j.get('html'):
                nome, dados = f'cap{cap}-relatorio.html', j['html'].encode('utf8')
            else:
                print(f'cap{cap}: {lab[:50]}: formato não reconhecido: {v[:80]}')
                continue
        saida = os.path.join(HERE, 'pdfs', nome)
        open(saida, 'wb').write(dados)
        print(f'== {saida} ({len(dados)} bytes)')
        if nome.endswith('.pdf'):
            print(subprocess.run(['pdftotext', '-layout', saida, '-'], capture_output=True, text=True, timeout=30).stdout[:1800])
        else:
            print(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', dados.decode('utf8')))[:1500])
