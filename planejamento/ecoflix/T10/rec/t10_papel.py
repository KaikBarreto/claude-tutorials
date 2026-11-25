#!/usr/bin/env python3
"""T10 · rasteriza o papel REAL capturado na gravação final (rec/t10/pdfs/) para a cena `pdf.html`:
$TUT_HOME/t10/edit/out/comprovantes/{cap07-kardex,cap13-posicao,cap13-relatorio}.png (+ .bbox.html de cada um, pdftotext -bbox).
Parâmetros do cabeçalho de planejamento/ecoflix/T10/cenas_v3/pdf.html: Kardex -r 400 (A4 deitado, 1 página), Posição -r 350 (página 1 de 2),
Relatório = HTML impresso pelo Chromium na mídia de impressão (@page da página), -r 400.
uso: nice -n 19 python3 -I rec/t10/t10_papel.py"""
import os, subprocess
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, 'pdfs'); C = os.path.normpath(os.path.join(HERE, '..', '..', 't10', 'edit', 'out', 'comprovantes'))
os.makedirs(C, exist_ok=True)


def ppm(pdf, nome, r):
    base = os.path.join(C, '.tmp_' + nome)
    subprocess.run(['nice', '-n', '19', 'pdftoppm', '-r', str(r), '-png', '-singlefile', '-f', '1', '-l', '1', pdf, base], check=True)
    im = Image.open(base + '.png'); im.save(os.path.join(C, nome + '.png')); os.remove(base + '.png'); print(nome + '.png', im.size)
    subprocess.run(['pdftotext', '-bbox', '-f', '1', '-l', '1', pdf, os.path.join(C, nome + '.bbox.html')], check=True)


def imprime(html, pdf):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        pg.set_content(open(html, encoding='utf8').read(), wait_until='load'); pg.emulate_media(media='print')
        pg.pdf(path=pdf, prefer_css_page_size=True, print_background=True); b.close()


ppm(f'{P}/cap07-kardex.pdf', 'cap07-kardex', 400)
ppm(f'{P}/cap13-posicao-estoque-31-10-pdf.pdf', 'cap13-posicao', 350)
pdf_rel = os.path.join(C, 'cap13-relatorio.pdf')
imprime(f'{P}/cap13-relatorio.html', pdf_rel)
ppm(pdf_rel, 'cap13-relatorio', 400)
