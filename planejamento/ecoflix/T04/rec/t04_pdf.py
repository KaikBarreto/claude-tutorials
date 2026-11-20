#!/usr/bin/env python3
"""T04 · tira do actions.json dos caps 12 e 16 o conteúdo do "PDF" que o app abre em aba nova (o passo `eval` "PDF DO ..." devolve
'HTML:<base64>': o extrato e o relatório de saldos são HTML escrito na aba, não o #pdf-frame do T08) e grava em rec/t04/arquivos/.
Mostra o texto da página, para conferir o `mostra` do cenas/ilustracoes.json. Uso: python3 -I rec/t04/t04_pdf.py [--ens]"""
import base64
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
pasta = os.path.join(HERE, '_ens') if '--ens' in sys.argv else HERE
os.makedirs(os.path.join(HERE, 'arquivos'), exist_ok=True)
for cap, nome, rotulo in (('12', 'cap12-extrato-detalhado.html', 'PDF DO EXTRATO'), ('16', 'cap16-relatorio-saldos.html', 'PDF DO RELATÓRIO')):
    try:
        a = json.load(open(os.path.join(pasta, f't04-cap{cap}.actions.json'), encoding='utf8'))
    except OSError as e:
        print(f'cap{cap}: sem actions.json ({e})')
        continue
    v = next((x.get('value') for x in a['actions'] if (x.get('label') or '').startswith(rotulo)), None)
    if not isinstance(v, str) or not v.startswith('HTML:'):
        print(f'cap{cap}: sem HTML no actions.json: {str(v)[:80]}')
        continue
    saida = os.path.join(HERE, 'arquivos', nome)
    open(saida, 'wb').write(base64.b64decode(v[5:]))
    print(f'{saida} ({os.path.getsize(saida)} bytes)')
    t = open(saida, encoding='utf8').read()
    t = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', t, flags=re.S)
    t = html.unescape(re.sub(r'<[^>]+>', ' ', t))
    print(re.sub(r'\s+', ' ', t).strip()[:2500])
