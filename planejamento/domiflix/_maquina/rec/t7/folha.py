#!/usr/bin/env python3
"""T7 · folha de contato de uma gravação BRUTA do celular (780x1688): quadros nos tempos pedidos, lado a lado, com o tempo escrito.
Serve para conferir o que o robô filmou (sem dados reais na tela, rodapé com a versão do app, estados certos) antes de editar.
uso: python3 -I rec/t7/folha.py NN t1,t2,t3,... [--cols 6] [--esc 0.28] [--saida arquivo.png]
Sem tempos: usa os instantes das marcas Ln (início de cada linha da fala). Leve: só extrai quadros (ffmpeg -ss), sem trava."""
import json, os, subprocess, sys, tempfile

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
av = sys.argv[1:]
opt = lambda k, d=None: av[av.index(k) + 1] if k in av else d
pos = [a for i, a in enumerate(av) if not a.startswith('--') and (i == 0 or not av[i - 1].startswith('--'))]
n = int(pos[0])
base = os.path.join(HERE, f't7-cap{n:02d}')
A = json.load(open(base + '.actions.json'))
if len(pos) > 1:
    ts = [float(x) for x in pos[1].split(',')]
else:
    ts = [a['tStart'] for a in A['actions'] if a.get('do') == 'mark' and str(a.get('name', '')).startswith('L')] or [1, 5, 10]
cols, esc = int(opt('--cols', 6)), float(opt('--esc', 0.28))
saida = opt('--saida', os.path.join(HERE, f'.folha-{n:02d}.png'))
W0, H0 = int(A['video'].get('width', 780)), int(A['video'].get('height', 1688))
w, h = int(W0 * esc), int(H0 * esc)
fonte = ImageFont.load_default()
tmp = tempfile.mkdtemp(prefix='folha-t7-', dir=os.path.join(HERE, '_ex'))
quadros = []
for i, t in enumerate(ts):
    p = os.path.join(tmp, f'q{i:02d}.png')
    subprocess.run(['nice', '-n', '10', 'ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.3f}', '-i', base + '.mp4', '-frames:v', '1',
                    '-vf', f'scale={w}:{h}', p], check=False)
    quadros.append((t, p))
lin = (len(quadros) + cols - 1) // cols
folha = Image.new('RGB', (cols * (w + 6) + 6, lin * (h + 26) + 6), (24, 24, 27))
d = ImageDraw.Draw(folha)
for i, (t, p) in enumerate(quadros):
    x, y = 6 + (i % cols) * (w + 6), 6 + (i // cols) * (h + 26)
    if os.path.exists(p):
        folha.paste(Image.open(p).convert('RGB'), (x, y + 20))
    d.text((x + 2, y + 4), f'{t:.1f}s', fill=(240, 240, 240), font=fonte)
folha.save(saida)
for _, p in quadros:
    if os.path.exists(p):
        os.remove(p)
os.rmdir(tmp)
print(saida, folha.size)
