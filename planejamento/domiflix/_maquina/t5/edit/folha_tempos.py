#!/usr/bin/env python3
"""Folha de quadros de um MP4 em instantes dados (remendo 1.38.19). Cada quadro leva o tempo ao lado.
uso: python3 -I folha_tempos.py video.mp4 saida.jpg "titulo" t0:t1:passo [t0:t1:passo ...] [--cols 4] [--w 480]
  cada grupo gera os instantes t0, t0+passo, ... até t1 (inclusive); grupos separados por faixa de título."""
import subprocess, sys, io
from PIL import Image, ImageDraw, ImageFont
a = sys.argv[1:]
mp4, out, titulo = a[0], a[1], a[2]
cols = int(a[a.index('--cols') + 1]) if '--cols' in a else 4
W = int(a[a.index('--w') + 1]) if '--w' in a else 480
grupos = [g for g in a[3:] if ':' in g and not g.startswith('--')]
ts = []
for g in grupos:
    t0, t1, p = [float(x) for x in g.split(':')]
    t = t0
    while t <= t1 + 1e-6:
        ts.append(round(t, 2)); t += p
H = W * 9 // 16
try: f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 15)
except Exception: f = ImageFont.load_default()
tiles = []
for t in ts:
    r = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{max(t,0):.3f}', '-i', mp4, '-frames:v', '1', '-vf', f'scale={W}:{H}', '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True)
    im = Image.open(io.BytesIO(r.stdout)).convert('RGB') if r.stdout else Image.new('RGB', (W, H), (60, 0, 0))
    d = ImageDraw.Draw(im); d.rectangle([0, 0, 118, 22], fill=(0, 0, 0)); d.text((4, 3), f'{int(t//60)}:{t%60:05.2f}', fill=(255, 255, 255), font=f)
    tiles.append(im)
rows = (len(tiles) + cols - 1) // cols
sh = Image.new('RGB', (cols * (W + 4) + 4, rows * (H + 4) + 34), (30, 30, 30))
ImageDraw.Draw(sh).text((8, 8), titulo, fill=(255, 255, 255), font=f)
for i, im in enumerate(tiles):
    sh.paste(im, (4 + (i % cols) * (W + 4), 34 + (i // cols) * (H + 4)))
sh.save(out, quality=82)
print(out, len(tiles), 'quadros', sh.size)
