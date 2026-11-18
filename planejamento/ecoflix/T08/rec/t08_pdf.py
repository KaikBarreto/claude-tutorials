#!/usr/bin/env python3
"""T08 · tira do actions.json do cap08 o PDF do comprovante térmico (o passo `eval` "PDF do comprovante..." devolve 'PDF:<base64>')
e grava rec/t08/arquivos/cap08-comprovante-termico.pdf (a ilustração da edição usa o PDF do app). Mostra o texto do PDF (pdftotext).
Uso: python3 -I rec/t08/t08_pdf.py [--ens]"""
import base64
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
pasta = os.path.join(HERE, '_ens') if '--ens' in sys.argv else HERE
os.makedirs(os.path.join(HERE, 'arquivos'), exist_ok=True)
# 18/11 (1.60.10): o comprovante do ticket é do cap09 e o da pesagem avulsa, do cap11
for cap, nome in (('09', 'cap09-comprovante-termico.pdf'), ('11', 'cap11-comprovante-avulsa.pdf')):
    try:
        a = json.load(open(os.path.join(pasta, f't08-cap{cap}.actions.json'), encoding='utf8'))
    except OSError as e:
        print(f'cap{cap}: sem actions.json ({e})')
        continue
    v = next((x.get('value') for x in a['actions'] if (x.get('label') or '').startswith('PDF do comprovante')), None)
    if not isinstance(v, str) or not v.startswith('PDF:'):
        print(f'cap{cap}: sem PDF no actions.json: {str(v)[:80]}')
        continue
    saida = os.path.join(HERE, 'arquivos', nome)
    open(saida, 'wb').write(base64.b64decode(v[4:]))
    print(f'{saida} ({os.path.getsize(saida)} bytes)')
    try:
        print(subprocess.run(['pdftotext', '-layout', saida, '-'], capture_output=True, text=True, timeout=30).stdout)
    except Exception as e:  # noqa: BLE001
        print('pdftotext:', e)
