#!/usr/bin/env python3
"""T27 · grava o PDF do comprovante que o app gerou no cap05 (passo "captura o PDF ..." do actions.json, em base64) em
rec/t27/t27-cap05.comprovante.pdf, para a edição mostrar o comprovante como ilustração (a janela nova não entra no vídeo).
Uso: python3 -I rec/t27/t27_pdf.py [--ens] [--png /dev/shm/x.png]   (--png desenha a página para conferir: logo em cima, sem rodapé)"""
import base64
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
pasta = os.path.join(HERE, '_ens') if '--ens' in sys.argv else HERE
acts = json.load(open(os.path.join(pasta, 't27-cap05.actions.json'), encoding='utf8'))['actions']
cap = [a for a in acts if (a.get('label') or '').startswith('captura o PDF')]
if not cap or not isinstance(cap[-1].get('value'), dict):
    sys.exit('sem PDF no actions.json: ' + (str(cap[-1].get('value'))[:200] if cap else 'passo não achado'))
v = cap[-1]['value']
dados = base64.b64decode(v['b64'])
destino = os.path.join(HERE, v.get('pdf') or 't27-cap05.comprovante.pdf')
open(destino, 'wb').write(dados)
print(f"PDF {len(dados)} bytes (de {v.get('pdfs')} gerados; janela: {v.get('janela')}) -> {destino}")
txt = subprocess.run(['pdftotext', '-layout', destino, '-'], capture_output=True, text=True).stdout
print(txt.strip()[-1500:])
print('rodapé do EcoSistema no PDF:', 'SIM' if 'ecosistema' in txt.lower() else 'não')
if '--png' in sys.argv:
    png = sys.argv[sys.argv.index('--png') + 1]
    subprocess.run(['pdftoppm', '-png', '-r', '110', '-singlefile', destino, png[:-4] if png.endswith('.png') else png], check=True)
    print('página ->', png)
