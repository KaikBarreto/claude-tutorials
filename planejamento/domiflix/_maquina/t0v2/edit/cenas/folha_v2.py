#!/usr/bin/env python3
"""Folha de contato das ilustrações do T0 v2: para cada cena, 4 instantes (do início ao fim da linha da fala) nas duas proporções.
uso: python3 folha_v2.py 2 3 4 [--saida /tmp/folha.jpg] [--est DIR]   (usa est/capNN.json; passe --real DIR para os capNN.json da voz)"""
import json, os, subprocess, sys, glob
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); TUT = os.path.abspath(os.path.join(H, '..', '..', '..'))
CAP = {2: 0, 3: 0, 4: 0, 6: 1, 16: 2, 17: 2, 18: 2, 20: 3, 29: 5, 31: 5, 32: 5, 33: 5, 35: 6, 36: 6, 37: 6}
LIN = {2: 0, 3: 1, 4: 2, 6: 0, 16: 1, 17: 2, 18: 3, 20: 0, 29: 0, 31: 2, 32: 3, 33: 4, 35: 0, 36: 1, 37: 2}
a = sys.argv[1:]; saida = '/tmp/folha_v2.jpg'; est = os.path.join(H, 'est'); guias = '--guias' in a
if '--saida' in a: saida = a[a.index('--saida') + 1]
if '--real' in a: est = a[a.index('--real') + 1]
cenas = [int(x) for x in a if x.isdigit()]
rows = []
for c in cenas:
    j = json.load(open(os.path.join(est, f'cap{CAP[c]:02d}.json'))); l = j['linhas'][LIN[c]]
    ts = [l['s'] + (l['e'] - l['s']) * f for f in (.35, .65, .9)] + [l['e'] + .6]
    if c in (2, 17): ts = [l['s'] + (l['e'] - l['s']) * f for f in (.6, .8, .95)] + [l['e'] + 1.2]
    tt = ','.join(f'{x:.2f}' for x in ts)
    for fmt, html, rend in (('h', 'cenas_v2.html', 'render_cenas.cjs'), ('v', 'cenas_v2_vertical.html', 'render_cenas_vertical.cjs')):
        out = f'/tmp/stv2/{fmt}{c}'; import shutil; shutil.rmtree(out, ignore_errors=True); os.makedirs(out, exist_ok=True)
        cmd = ['flock', os.path.join(TUT, '..', '.heavy.lock'), 'nice', '-n', '10', 'node', os.path.join(H, rend), str(c), os.path.join(est, f'cap{CAP[c]:02d}.json'), out, '--stills', tt, '--html', os.path.join(H, html)] + (['--guias'] if guias and fmt == 'v' else [])
        r = subprocess.run(cmd, capture_output=True, text=True); 
        if r.stdout.strip() or r.returncode: print(c, fmt, r.stdout.strip()[-300:], r.stderr.strip()[-300:])
    rows.append(c)
W = 4 * 330
sheet = Image.new('RGB', (W, len(rows) * (206 + 480)), 'white')
for ri, c in enumerate(rows):
    for fmt, y, hh, ww in (('h', ri * 686, 206, 330), ('v', ri * 686 + 206, 480, 270)):
        fs = sorted(glob.glob(f'/tmp/stv2/{fmt}{c}/cap{c:02d}_*.*'), key=lambda f: float(os.path.basename(f).split('_')[1].rsplit('.', 1)[0]))
        for i, f in enumerate(fs[-4:]):
            im = Image.open(f).convert('RGB').resize((ww, hh)); sheet.paste(im, (i * 330, y))
sheet.save(saida, quality=85); print('folha', saida, rows)
