#!/usr/bin/env python3
"""T16 · tira do actions.json do cap20 os PDFs que o app abre na aba nova (o passo `eval` com rótulo "PDF do ..." devolve
'PDF:<base64>') e grava rec/t16/arquivos/ para a cena do comprovante (cenas/ilustracoes.json, "tipo": "comprovante"). Mostra o texto
de cada PDF (pdftotext). Uso: python3 -I rec/t16/t16_pdf.py [--ens]"""
import base64
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
pasta = os.path.join(HERE, '_ens') if '--ens' in sys.argv else HERE
os.makedirs(os.path.join(HERE, 'arquivos'), exist_ok=True)
# (capítulo, começo do rótulo do passo, arquivo)
PDFS = (('20', 'PDF do Comprovante (Notinha)', 'cap20-comprovante-notinha-1250.pdf'),
        ('20', 'PDF do DANFE da 1250', 'cap20-danfe-1250.pdf'))
for cap, rotulo, nome in PDFS:
    try:
        a = json.load(open(os.path.join(pasta, f't16-cap{cap}.actions.json'), encoding='utf8'))
    except OSError as e:
        print(f'cap{cap}: sem actions.json ({e})')
        continue
    v = next((x.get('value') for x in a['actions'] if (x.get('label') or '').startswith(rotulo)), None)
    if not isinstance(v, str) or not v.startswith('PDF:'):
        print(f'cap{cap} {rotulo}: sem PDF no actions.json: {str(v)[:80]}')
        continue
    saida = os.path.join(HERE, 'arquivos', nome)
    open(saida, 'wb').write(base64.b64decode(v[4:]))
    print(f'{saida} ({os.path.getsize(saida)} bytes)')
    try:
        print(subprocess.run(['pdftotext', '-layout', saida, '-'], capture_output=True, text=True, timeout=30).stdout[:3000])
    except Exception as e:  # noqa: BLE001
        print('pdftotext:', e)
