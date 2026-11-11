#!/usr/bin/env python3
"""T27 · versão clara do logo FICTÍCIO da Recicla Vale (o do T1, recicla-vale-logo.png): o mesmo desenho, recortado justo e posto
sobre uma placa branca de cantos arredondados. Lê no menu escuro do app (o logo do T1 tem letra azul-escura e some no fundo quase
preto) e continua igual nos fundos brancos (prévia do "Logo da Empresa", que é bg-white, e o papel do comprovante).
Uso: python3 -I rec/t27/t27_logo_claro.py   -> rec/t27/assets/recicla-vale-logo-claro.png e rec/mundo/storage/avatars/ (mesmo arquivo)"""
import os
import shutil
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
MUNDO = os.path.normpath(os.path.join(HERE, '..', 'mundo'))
orig = Image.open(os.path.join(MUNDO, 'storage', 'avatars', 'recicla-vale-logo.png')).convert('RGBA')
caixa = orig.split()[3].point(lambda v: 255 if v > 10 else 0).getbbox()
desenho = orig.crop(caixa)
pad, raio = 18, 30
w, h = desenho.size[0] + 2 * pad, desenho.size[1] + 2 * pad
placa = Image.new('RGBA', (w, h), (0, 0, 0, 0))
ImageDraw.Draw(placa).rounded_rectangle((0, 0, w - 1, h - 1), radius=raio, fill=(255, 255, 255, 255))
placa.alpha_composite(desenho, (pad, pad))
saida = os.path.join(HERE, 'assets', 'recicla-vale-logo-claro.png')
os.makedirs(os.path.dirname(saida), exist_ok=True)
placa.save(saida, optimize=True)
shutil.copyfile(saida, os.path.join(MUNDO, 'storage', 'avatars', 'recicla-vale-logo-claro.png'))
print(saida, placa.size, os.path.getsize(saida), 'bytes')
