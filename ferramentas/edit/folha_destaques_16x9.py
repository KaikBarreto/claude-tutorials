#!/usr/bin/env python3
"""Folha dos DESTAQUES (spots) e AVISOS (callouts) do 16:9 (computador), tirada do MP4 renderizado de cada capítulo: um quadro no meio de
cada um, com o rótulo/texto ao lado e a faixa da legenda do player (y 800-930 de 1080) marcada em vermelho, para conferir que o destaque
cai no alvo certo e não contorna a legenda (T0 v2: um destaque contornou a legenda; T12).
uso: python3 -I folha_destaques_16x9.py [saida.jpg] [NN ...]   (padrão: out/folha_destaques.jpg e todos os caps/capNN.chapter.json)
Rode na pasta <tutorial>/edit, depois do render dos capítulos (o MP4 sai de "output.dir" do JSON do capítulo, como no render_chapter.py)."""
import glob
import io
import json
import os
import re
import subprocess
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.environ.get('TUT_HOME') or os.path.dirname(os.path.dirname(HERE)), 'kit'))
import ui  # noqa: E402

saida = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'out', 'folha_destaques.jpg')
todos = sorted(m.group(1) for p in glob.glob(os.path.join(HERE, 'caps', 'cap*.chapter.json'))
               if (m := re.fullmatch(r'cap(\d\d[a-z]?)\.chapter\.json', os.path.basename(p))))
caps = [f'{int(m[1]):02d}{m[2]}' for a in sys.argv[2:] if (m := re.fullmatch(r'(\d+)([a-z]?)', a))] or todos  # 3 -> 03, 9b -> 09b
itens = []
for nn in caps:
    cj = os.path.join(HERE, 'caps', f'cap{nn}.chapter.json')
    ch = json.load(open(cj))
    outd = os.path.normpath(os.path.join(os.path.dirname(cj), ch.get('output', {}).get('dir', os.path.join(HERE, 'out', f'cap{nn}'))))
    mp4 = os.path.join(outd, f'{ch.get("name", f"cap{nn}")}.mp4')
    if not os.path.exists(mp4):
        print(f'cap{nn}: sem render ({mp4})')
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
    r = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.2f}', '-i', mp4, '-frames:v', '1', '-f', 'image2pipe', '-vcodec', 'png', '-'],
                       capture_output=True)
    im = Image.open(io.BytesIO(r.stdout)).convert('RGB').resize((W, H)) if r.stdout else Image.new('RGB', (W, H), (90, 0, 0))
    dd = ImageDraw.Draw(im, 'RGBA')
    y0, y1 = int(H * 800 / 1080), int(H * 930 / 1080)
    dd.rectangle([0, y0, W, y1], outline=(255, 60, 60, 255), width=2)
    x = 20 + (i % cols) * (W + 20)
    y = 20 + (i // cols) * (H + 60)
    folha.paste(im, (x, y + 40))
    d.text((x, y + 8), f'cap{nn} · {tipo} · {t:.1f} s · {rot}'[:110], font=ui.font(600, 22), fill=(255, 255, 255))
os.makedirs(os.path.dirname(os.path.abspath(saida)), exist_ok=True)
folha.save(saida, quality=88)
print('ok', saida, len(itens), 'itens')
