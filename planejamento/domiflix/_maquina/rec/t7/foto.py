#!/usr/bin/env python3
"""T7 · gera a foto de teste genérica (sem marca) que o técnico "anexa" no checklist: uma unidade interna de ar-condicionado
(Hi-Wall) numa parede, desenhada por código. Saída: rec/t7/assets/foto-equipamento.jpg (1200x900)."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1200, 900
rng = np.random.default_rng(7)


def grad(w, h, top, bot):
    t = np.linspace(0, 1, h)[:, None, None]
    a = np.array(top, np.float32)[None, None, :]
    b = np.array(bot, np.float32)[None, None, :]
    return np.repeat(a + (b - a) * t, w, axis=1)


# parede: gradiente suave + textura fina de reboco
wall = grad(W, H, (232, 227, 217), (214, 207, 194))
wall += rng.normal(0, 2.4, (H, W, 1))
img = Image.fromarray(np.clip(wall, 0, 255).astype(np.uint8))

# sombra projetada da unidade (desfocada), em camada separada
sh = Image.new('L', (W, H), 0)
ImageDraw.Draw(sh).rounded_rectangle((165, 215, 1045, 465), 60, fill=150)
sh = sh.filter(ImageFilter.GaussianBlur(26))
img = Image.composite(Image.new('RGB', (W, H), (92, 86, 76)), img, sh.point(lambda v: int(v * 0.55)))

# tubulação isolada e mangueira do dreno descendo pela parede (atrás da unidade)
d = ImageDraw.Draw(img)
d.rounded_rectangle((940, 400, 1000, 860), 26, fill=(238, 238, 235), outline=(196, 196, 190), width=3)
d.rounded_rectangle((1012, 400, 1050, 860), 18, fill=(150, 156, 160), outline=(120, 126, 130), width=2)
for y in range(430, 850, 70):  # fitas de acabamento no isolamento
    d.rectangle((940, y, 1000, y + 7), fill=(205, 206, 200))

# corpo da unidade: branco com leve gradiente vertical
body = Image.fromarray(np.clip(grad(880, 250, (250, 250, 248), (226, 228, 227)), 0, 255).astype(np.uint8))
mask = Image.new('L', (880, 250), 0)
ImageDraw.Draw(mask).rounded_rectangle((0, 0, 879, 249), 58, fill=255)
img.paste(body, (160, 190), mask)
d = ImageDraw.Draw(img)
d.rounded_rectangle((160, 190, 1040, 440), 58, outline=(206, 208, 206), width=3)
# grade de entrada de ar (topo)
for i in range(9):
    y = 214 + i * 7
    d.line((230, y, 970, y), fill=(214, 216, 215), width=2)
# painel frontal: friso e saída de ar (aletas)
d.line((200, 338, 1000, 338), fill=(218, 220, 219), width=3)
d.rounded_rectangle((196, 362, 1004, 414), 24, fill=(176, 180, 182))
d.rounded_rectangle((204, 372, 996, 408), 18, fill=(138, 143, 146))
d.rounded_rectangle((204, 396, 996, 412), 8, fill=(236, 237, 236))  # aleta aberta
# visor com um ponto verde (sem marca nem texto)
d.rounded_rectangle((900, 300, 970, 322), 8, fill=(40, 44, 46))
d.ellipse((912, 305, 922, 315), fill=(70, 214, 120))

img = img.filter(ImageFilter.GaussianBlur(0.8))
arr = np.asarray(img).astype(np.float32) + rng.normal(0, 2.0, (H, W, 1))  # grão de câmera
# vinheta leve nas bordas
yy, xx = np.mgrid[0:H, 0:W]
v = 1 - 0.20 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) ** 1.2
arr *= v[..., None]
out = os.path.join(HERE, 'assets', 'foto-equipamento.jpg')
os.makedirs(os.path.dirname(out), exist_ok=True)
Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(out, quality=88)
print(out, os.path.getsize(out) // 1024, 'KB')
