#!/usr/bin/env python3
"""T11 · tira o PDF REAL do relatório (passo "PDF do relatório" do actions.json da gravação final do cap12), grava em rec/t11/pdfs/ e
rasteriza para a cena pdf.html: $TUT_HOME/t11/edit/out/comprovantes/cap12-relatorio.{pdf,png,bbox.html} (A4 deitado, -r 400).
uso: nice -n 19 python3 -I rec/t11/t11_papel.py"""
import base64, json, os, subprocess
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, 'pdfs'); C = os.path.normpath(os.path.join(HERE, '..', '..', 't11', 'edit', 'out', 'comprovantes'))
os.makedirs(P, exist_ok=True); os.makedirs(C, exist_ok=True)
a = json.load(open(os.path.join(HERE, 't11-cap12.actions.json'), encoding='utf8'))['actions']
v = next((x.get('value') for x in a if (x.get('label') or '').startswith('PDF do relat')), None)
assert isinstance(v, str) and v.startswith('PDF:'), f'sem PDF no actions.json: {str(v)[:60]}'
pdf = os.path.join(P, 'cap12-relatorio.pdf'); open(pdf, 'wb').write(base64.b64decode(v[4:]))
open(os.path.join(C, 'cap12-relatorio.pdf'), 'wb').write(base64.b64decode(v[4:]))
base = os.path.join(C, '.tmp_rel')
subprocess.run(['nice', '-n', '19', 'pdftoppm', '-r', '400', '-png', '-singlefile', '-f', '1', '-l', '1', pdf, base], check=True)
im = Image.open(base + '.png'); im.save(os.path.join(C, 'cap12-relatorio.png')); os.remove(base + '.png'); print('png', im.size)
subprocess.run(['pdftotext', '-bbox', '-f', '1', '-l', '1', pdf, os.path.join(C, 'cap12-relatorio.bbox.html')], check=True)
print(subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout[:1500])
