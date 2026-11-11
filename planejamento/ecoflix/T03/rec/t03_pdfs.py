#!/usr/bin/env python3
"""T03 · grava os PDFs que o app gerou na gravação do cap09 (o robô grava uma aba só e o Chromium sem janela não tem leitor de PDF: "a aba
nova" do roteiro vira ilustração na edição, com o PDF de verdade). O roteiro do cap09 guarda cada PDF (base64) na tabela de bastidor
t03_pdfs da MINHA instância do Supabase falso; rode LOGO DEPOIS da gravação (a próxima gravação reinicia o falso e apaga a tabela).
Saída: $TUT_HOME/t03/pdf/<nome>.pdf e a 1ª página em PNG (pdftoppm, 150 dpi), fora de rec/ (PDF não vai para o git).
Uso: python3 -I rec/t03/t03_pdfs.py"""
import base64
import json
import os
import shutil
import subprocess
import urllib.request

FAKE = os.environ.get('FAKE_URL', 'http://127.0.0.1:54303')
HERE = os.path.dirname(os.path.abspath(__file__))
saida = os.path.normpath(os.path.join(HERE, '..', '..', 't03', 'pdf'))
os.makedirs(saida, exist_ok=True)
with urllib.request.urlopen(f'{FAKE}/__dev/state?table=t03_pdfs') as r:
    linhas = json.load(r)
for ln in linhas:
    arq = os.path.join(saida, ln['nome'] + '.pdf')
    with open(arq, 'wb') as f:
        f.write(base64.b64decode(ln['b64']))
    png = ''
    if shutil.which('pdftoppm'):
        subprocess.run(['pdftoppm', '-png', '-r', '150', '-f', '1', '-l', '1', '-singlefile', arq, arq[:-4]], check=False)
        png = f' + {os.path.basename(arq[:-4])}.png'
    print(f'{arq} ({ln.get("bytes")} bytes){png}')
print(f'{len(linhas)} PDF(s) em {saida}')
