#!/usr/bin/env python3
"""T12 · folha só dos DESTAQUES (spots) e AVISOS (callouts) de cada capítulo, tirada do MP4 renderizado: um quadro no meio de cada um, com o
rótulo/texto ao lado e a faixa da legenda do player (y 800-930 de 1080) marcada em vermelho, para conferir que o destaque cai no alvo certo e
não contorna a legenda (T0 v2: um destaque contornou a legenda). uso: python3 -I folha_destaques.py out/folha_destaques.jpg [NN ...]"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'kit'))
import ui  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
saida = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'out', 'folha_destaques.jpg')
caps = [f'{int(a):02d}' for a in sys.argv[2:]] or [f'{i:02d}' for i in range(12)]
itens = []
for nn in caps:
    ch = json.load(open(os.path.join(HERE, 'caps', f'cap{nn}.chapter.json')))
    mp4 = os.path.join(HERE, 'out', f'cap{nn}', f'cap{nn}.mp4')
    if not os.path.exists(mp4):
        continue
    for tipo, lista in (('destaque', ch.get('spots', [])), ('aviso', ch.get('callouts', []))):
        for x in lista:
            t = x['at'] + min(1.0, x.get('dur', 2) / 2)
            rot = x.get('label') or x.get('text') or ''
            itens.append((nn, tipo, t, rot, mp4))
if not itens:
    raise SystemExit('nenhum destaque/aviso com capítulo renderizado')
W, H = 800, 450
cols = 2
linhas = (len(itens) + cols - 1) // cols
folha = Image.new('RGB', (cols * (W + 20) + 20, linhas * (H + 60) + 20), (30, 30, 30))
d = ImageDraw.Draw(folha)
for i, (nn, tipo, t, rot, mp4) in enumerate(itens):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.2f}', '-i', mp4, '-frames:v', '1', '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True)
    im = Image.open(__import__('io').BytesIO(r.stdout)).convert('RGB').resize((W, H))
    dd = ImageDraw.Draw(im, 'RGBA')
    y0, y1 = int(H * 800 / 1080), int(H * 930 / 1080)
    dd.rectangle([0, y0, W, y1], outline=(255, 60, 60, 255), width=2)
    x = 20 + (i % cols) * (W + 20)
    y = 20 + (i // cols) * (H + 60)
    folha.paste(im, (x, y + 40))
    d.text((x, y + 8), f'cap{nn} · {tipo} · {t:.1f} s · {rot}'[:110], font=ui.font(600, 22), fill=(255, 255, 255))
folha.save(saida, quality=88)
print('ok', saida, len(itens), 'itens')
