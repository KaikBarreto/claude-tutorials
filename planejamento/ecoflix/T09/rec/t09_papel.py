#!/usr/bin/env python3
"""T09 · rasteriza o papel REAL capturado na gravação final (rec/t09/pdfs/) para a edição mostrar nas cenas `pdf.html`:
$TUT_HOME/t09/edit/out/comprovantes/{cap04,cap06-aparecida,cap06-valdir,cap07-relatorio,cap09-fechamento,cap09-estoque}.png
Parâmetros do cabeçalho de planejamento/ecoflix/T09/cenas_v3/pdf.html (pdftoppm -r 720/500/400; HTML impresso pelo Chromium).
uso: python3 -I rec/t09/t09_papel.py [--so cap04 ...]   (leve: nice -n 19)"""
import os, subprocess, sys, shutil
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, 'pdfs'); C = os.path.normpath(os.path.join(HERE, '..', '..', 't09', 'edit', 'out', 'comprovantes'))
os.makedirs(C, exist_ok=True)
so = sys.argv[sys.argv.index('--so') + 1:] if '--so' in sys.argv else None
def quer(n): return so is None or n in so
def ppm(pdf, dst, r, alt_pt=None):
    base = os.path.join(C, '.tmp_' + os.path.basename(dst)[:-4])
    subprocess.run(['nice', '-n', '19', 'pdftoppm', '-r', str(r), '-png', '-singlefile', '-f', '1', '-l', '1', pdf, base], check=True)
    im = Image.open(base + '.png')
    if alt_pt: im = im.crop((0, 0, im.width, round(alt_pt * r / 72)))
    im.save(dst); os.remove(base + '.png'); print(os.path.basename(dst), im.size)
def imprime(html, pdf, css_page):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        pg.set_content(open(html, encoding='utf8').read(), wait_until='load'); pg.emulate_media(media='print')
        pg.pdf(path=pdf, format=None if css_page else 'A4', prefer_css_page_size=css_page, print_background=True); b.close()
if quer('cap04'): ppm(f'{P}/cap04-comprovante-vale-forte-21-10.pdf', f'{C}/cap04.png', 720); shutil.copy(f'{P}/cap04-comprovante-vale-forte-21-10.pdf', f'{C}/cap04.pdf')
if quer('cap06-aparecida'): ppm(f'{P}/cap06-comprovante-aparecida.pdf', f'{C}/cap06-aparecida.png', 720); shutil.copy(f'{P}/cap06-comprovante-aparecida.pdf', f'{C}/cap06-aparecida.pdf')
if quer('cap06-valdir'): ppm(f'{P}/cap06-comprovante-valdir-sem-valores.pdf', f'{C}/cap06-valdir.png', 720); shutil.copy(f'{P}/cap06-comprovante-valdir-sem-valores.pdf', f'{C}/cap06-valdir.pdf')
if quer('cap07-relatorio'):
    imprime(f'{P}/cap07-relatorio-pedidos-outubro.html', f'{C}/cap07-relatorio.pdf', False); ppm(f'{C}/cap07-relatorio.pdf', f'{C}/cap07-relatorio.png', 300)
if quer('cap09-fechamento'): ppm(f'{P}/cap09-relatorio-fechamento-70.pdf', f'{C}/cap09-fechamento.png', 500, 690)
if quer('cap09-estoque'):
    imprime(f'{P}/cap09-relatorio-estoque-70.html', f'{C}/cap09-estoque.pdf', True); ppm(f'{C}/cap09-estoque.pdf', f'{C}/cap09-estoque.png', 400, 310)
