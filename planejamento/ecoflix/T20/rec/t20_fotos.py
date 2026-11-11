#!/usr/bin/env python3
"""T20 · gera as três fotos fictícias da compra de 06/11 da Cooperativa Recomeço (1600x1200, desenhadas por código: pátio com fardos de
papelão, bags de PET prensado e bags de latinha; sem pessoa, sem placa, sem marca) em rec/mundo/storage/order-attachments/t20/.
Uso: python3 -I rec/t20/t20_fotos.py"""
import os
import random
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.normpath(os.path.join(HERE, '..', 'mundo', 'storage', 'order-attachments', 't20'))
W, H = 1600, 1200


def fundo(rng, horizonte=430):
    im = Image.new('RGB', (W, H))
    d = ImageDraw.Draw(im)
    for y in range(H):
        if y < horizonte:
            t = y / horizonte
            c = (int(150 + 70 * t), int(185 + 50 * t), int(225 + 20 * t))
        else:
            t = (y - horizonte) / (H - horizonte)
            c = (int(128 - 40 * t), int(122 - 38 * t), int(112 - 36 * t))
        d.line([(0, y), (W, y)], fill=c)
    # galpão ao fundo (parede e portão), sem letreiro
    d.rectangle([0, 250, W, horizonte + 20], fill=(168, 172, 176))
    for x in range(0, W, 80):
        d.line([(x, 250), (x, horizonte + 20)], fill=(150, 154, 158), width=3)
    d.rectangle([980, 300, 1420, horizonte + 20], fill=(104, 112, 120))
    d.rectangle([0, 240, W, 262], fill=(120, 124, 130))
    return im


def ruido(im, rng, forca=14):
    px = im.load()
    for _ in range(W * H // 6):
        x, y = rng.randrange(W), rng.randrange(H)
        r, g, b = px[x, y]
        n = rng.randint(-forca, forca)
        px[x, y] = (max(0, min(255, r + n)), max(0, min(255, g + n)), max(0, min(255, b + n)))
    return im.filter(ImageFilter.GaussianBlur(0.8))


def fardo(d, x, y, w, h, cor, rng, fitas=2):
    sombra = tuple(int(c * 0.55) for c in cor)
    d.rectangle([x + 10, y + h - 6, x + w + 18, y + h + 12], fill=(60, 56, 50))
    d.rectangle([x, y, x + w, y + h], fill=cor, outline=sombra, width=3)
    for k in range(int(h / 12)):
        yy = y + 8 + k * 12
        tom = tuple(max(0, min(255, c + rng.randint(-26, 22))) for c in cor)
        d.line([(x + 3, yy), (x + w - 3, yy + rng.randint(-2, 2))], fill=tom, width=rng.randint(3, 6))
    for k in range(fitas):
        fx = x + w * (k + 1) / (fitas + 1)
        d.rectangle([fx - 3, y, fx + 3, y + h], fill=(52, 54, 58))


def bag(d, x, y, w, h, cor, rng):
    sombra = tuple(int(c * 0.6) for c in cor)
    d.rectangle([x + 10, y + h - 6, x + w + 16, y + h + 10], fill=(60, 56, 50))
    d.rounded_rectangle([x, y, x + w, y + h], radius=34, fill=cor, outline=sombra, width=4)
    for k in range(5):
        yy = y + 30 + k * (h - 60) / 5
        d.arc([x + 8, yy, x + w - 8, yy + 40], 200, 340, fill=sombra, width=3)
    for dx in (0.22, 0.78):
        d.rectangle([x + w * dx - 8, y - 18, x + w * dx + 8, y + 12], fill=sombra)
    for _ in range(26):  # retalhos do material aparecendo
        px, py = x + rng.randint(18, w - 30), y + rng.randint(26, h - 40)
        d.ellipse([px, py, px + rng.randint(10, 24), py + rng.randint(6, 16)], fill=tuple(max(0, min(255, c + rng.randint(-50, 50))) for c in cor))


def cena(nome, semente, desenha):
    rng = random.Random(semente)
    im = fundo(rng)
    d = ImageDraw.Draw(im)
    desenha(d, rng)
    ruido(im, rng).save(os.path.join(SAIDA, nome), quality=88)


def papelao(d, rng):
    cor = (176, 138, 92)
    for fila, (y, n, w) in enumerate([(700, 4, 320), (520, 3, 330)]):
        x0 = 120 + fila * 130
        for i in range(n):
            fardo(d, x0 + i * (w + 14), y, w, 190, tuple(c + rng.randint(-10, 8) for c in cor), rng)
    for i in range(2):
        fardo(d, 220 + i * 340, 330, 330, 190, tuple(c + rng.randint(-8, 6) for c in cor), rng)
    fardo(d, 1180, 760, 300, 200, cor, rng)


def pet(d, rng):
    for fila, (y, n) in enumerate([(640, 4), (390, 3)]):
        x0 = 140 + fila * 120
        for i in range(n):
            bag(d, x0 + i * 330, y, 300, 330 if fila == 0 else 250, tuple(c + rng.randint(-8, 8) for c in (178, 198, 206)), rng)
    bag(d, 1320, 760, 240, 300, (170, 190, 200), rng)


def latinha(d, rng):
    for fila, (y, n) in enumerate([(690, 4), (440, 3)]):
        x0 = 130 + fila * 150
        for i in range(n):
            bag(d, x0 + i * 340, y, 310, 300 if fila == 0 else 260, tuple(max(0, min(255, c + rng.randint(-8, 8))) for c in (196, 198, 204)), rng)
    bag(d, 1290, 780, 250, 290, (186, 190, 198), rng)


if __name__ == '__main__':
    os.makedirs(SAIDA, exist_ok=True)
    cena('t20-carga-papelao.jpg', 20011, papelao)
    cena('t20-carga-pet.jpg', 20012, pet)
    cena('t20-carga-latinha.jpg', 20013, latinha)
    for f in sorted(os.listdir(SAIDA)):
        print(f, os.path.getsize(os.path.join(SAIDA, f)))
