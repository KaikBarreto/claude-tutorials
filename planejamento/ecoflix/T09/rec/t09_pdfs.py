#!/usr/bin/env python3
"""T09 · grava os PDFs e relatórios que o app abriu em aba nova numa gravação (o vídeo grava uma aba só): os passos `eval` de
js_pdf/js_aba_html (gerar.py) devolvem o arquivo em base64 no actions.json; aqui ele vira rec/t09/pdfs/capNN-<nome>.pdf|.html, para
a edição mostrar o PDF/relatório do próprio app como ilustração (PERFIL: "Comprovante: o PDF do app").
Uso: python3 -I rec/t09/t09_pdfs.py NN [--ens]"""
import base64
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
nn = f'{int(sys.argv[1]):02d}'
pasta = os.path.join(HERE, '_ens') if '--ens' in sys.argv else HERE
acts = json.load(open(os.path.join(pasta, f't09-cap{nn}.actions.json'), encoding='utf8'))['actions']
saida = os.path.join(HERE, 'pdfs')
os.makedirs(saida, exist_ok=True)
achou = 0
for a in acts:
    r = a.get('value')
    if isinstance(r, str) and r.startswith('{'):
        try:
            r = json.loads(r)
        except ValueError:
            pass
    if not isinstance(r, dict) or 'b64' not in r:
        continue
    nome, ext = (r['pdf'], 'pdf') if 'pdf' in r else (r['html'], 'html')
    arq = os.path.join(saida, f'cap{nn}-{nome}.{ext}')
    with open(arq, 'wb') as f:
        f.write(base64.b64decode(r['b64']))
    achou += 1
    print(f'{os.path.relpath(arq, HERE)}: {os.path.getsize(arq)} bytes (passo "{a.get("label")}", t={a.get("tAct") or a.get("tStart")})')
if not achou:
    print('nenhum PDF/relatório no actions.json')
