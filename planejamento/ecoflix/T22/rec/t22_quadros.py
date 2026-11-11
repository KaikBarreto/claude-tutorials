#!/usr/bin/env python3
"""T22 · "storyboard" de um ensaio: um quadro logo depois de cada passo com rótulo (o que a câmera vai mostrar), com o rótulo e o instante.
Uso: python3 -I rec/t22/t22_quadros.py NN [--ens] [--quadros PASTA]   (PASTA padrão: /dev/shm/t22rec/_frames_capNN)
Precisa da gravação com --keep-frames (o t22_ens.sh faz). O quadro de cada passo = o último quadro gravado até tEnd + 0,4 s (a hora do
arquivo; o Chrome só manda quadro quando a tela muda). Saída: /dev/shm/t22rec/t22-capNN.quadros-K.jpg (até 6 quadros por folha).
Depois de olhar: apagar as folhas e a pasta dos quadros (o t22_ens.sh apaga a pasta)."""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
n = int(sys.argv[1])
nn = f'{n:02d}'
ens = '--ens' in sys.argv
pasta = sys.argv[sys.argv.index('--quadros') + 1] if '--quadros' in sys.argv else f'/dev/shm/t22rec/_frames_cap{nn}'
a = json.load(open(os.path.join(HERE, '_ens' if ens else '', f't22-cap{nn}.actions.json')))
t0 = a['t0EpochMs'] / 1000.0
quadros = sorted((os.path.getmtime(os.path.join(pasta, f)), os.path.join(pasta, f)) for f in os.listdir(pasta) if f.endswith('.jpg'))
if not quadros:
    sys.exit('sem quadros em ' + pasta)
tempos = [q[0] for q in quadros]


def quadro(t):
    import bisect
    i = bisect.bisect_right(tempos, t0 + t) - 1
    return quadros[max(0, i)][1]


itens = []
for x in a['actions']:
    if x.get('do') == 'mark' or not x.get('label'):
        continue
    t = (x.get('tEnd') or x.get('tAct') or x.get('tStart') or 0) + 0.4
    ok = '' if x.get('ok', True) and not x.get('error') else ' FALHOU'
    itens.append((t, f"{x['i']:02d} {x['do']} {t:5.1f}s{ok}: {x['label'][:90]}", quadro(t)))
itens.append((a['video'].get('durationS') or tempos[-1] - t0, 'FIM', quadros[-1][1]))
W, H, COL, POR = 960, 600, 2, 6
try:
    fonte = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 15)
except Exception:
    fonte = ImageFont.load_default()
os.makedirs('/dev/shm/t22rec', exist_ok=True)
folhas = []
for k in range(0, len(itens), POR):
    lote = itens[k:k + POR]
    linhas = (len(lote) + COL - 1) // COL
    folha = Image.new('RGB', (W * COL, (H + 24) * linhas), 'white')
    d = ImageDraw.Draw(folha)
    for j, (t, rot, arq) in enumerate(lote):
        im = Image.open(arq).convert('RGB').resize((W, H))
        x, y = (j % COL) * W, (j // COL) * (H + 24)
        folha.paste(im, (x, y + 24))
        d.rectangle([x, y, x + W, y + 24], fill='black')
        d.text((x + 4, y + 4), rot, fill='yellow' if 'FALHOU' not in rot else 'red', font=fonte)
    saida = f'/dev/shm/t22rec/t22-cap{nn}.quadros-{k // POR + 1}.jpg'
    folha.save(saida, quality=80)
    folhas.append(saida)
print('\n'.join(folhas))
