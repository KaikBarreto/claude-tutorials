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
a = json.load(open(os.path.join(pasta, 't08-cap08.actions.json'), encoding='utf8'))
v = next((x.get('value') for x in a['actions'] if (x.get('label') or '').startswith('PDF do comprovante')), None)
if not isinstance(v, str) or not v.startswith('PDF:'):
    raise SystemExit(f'sem PDF no actions.json: {str(v)[:80]}')
os.makedirs(os.path.join(HERE, 'arquivos'), exist_ok=True)
saida = os.path.join(HERE, 'arquivos', 'cap08-comprovante-termico.pdf')
open(saida, 'wb').write(base64.b64decode(v[4:]))
print(f'{saida} ({os.path.getsize(saida)} bytes)')
try:
    print(subprocess.run(['pdftotext', '-layout', saida, '-'], capture_output=True, text=True, timeout=30).stdout)
except Exception as e:  # noqa: BLE001
    print('pdftotext:', e)
