#!/usr/bin/env python3
"""T1 · gera o logo (600x240) e o ícone (128x128) FICTÍCIOS da Recicla Vale Metais, PNG transparente: símbolo próprio (vale entre
duas serras sobre uma barra de metal, num escudo arredondado azul-aço) + "Recicla Vale" / "METAIS". Nada do símbolo de reciclagem
do EcoSistema (sem setas), nenhuma marca real. Uso: python3 -I rec/t01/t01_logo.py  (escreve rec/t01/assets/ e rec/mundo/storage/avatars/)"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
AZUL, AZUL2, COBRE, BRANCO = (30, 58, 95, 255), (52, 92, 140, 255), (196, 106, 46, 255), (255, 255, 255, 255)
F_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
F_COND = '/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf'


def simbolo(lado):
    """escudo arredondado com o vale (duas serras brancas) e a barra de cobre embaixo; desenhado a 4x e reduzido"""
    s = 4
    L = lado * s
    im = Image.new('RGBA', (L, L), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    r = int(L * 0.22)
    d.rounded_rectangle([0, 0, L - 1, L - 1], radius=r, fill=AZUL)
    d.rounded_rectangle([int(L * 0.06), int(L * 0.06), L - 1 - int(L * 0.06), int(L * 0.52)], radius=int(r * 0.7), fill=AZUL2)
    # duas serras formando o vale (um "V" largo), brancas
    base = int(L * 0.66)
    d.polygon([(int(L * 0.12), base), (int(L * 0.34), int(L * 0.22)), (int(L * 0.50), int(L * 0.50)), (int(L * 0.66), int(L * 0.22)),
               (int(L * 0.88), base)], fill=BRANCO)
    d.polygon([(int(L * 0.27), base), (int(L * 0.50), int(L * 0.40)), (int(L * 0.73), base)], fill=AZUL)
    # barra de metal (lingote) de cobre
    d.rounded_rectangle([int(L * 0.16), int(L * 0.72), int(L * 0.84), int(L * 0.84)], radius=int(L * 0.04), fill=COBRE)
    d.rectangle([int(L * 0.22), int(L * 0.745), int(L * 0.78), int(L * 0.765)], fill=(226, 150, 92, 255))
    return im.resize((lado, lado), Image.LANCZOS)


def logo(w=600, h=240):
    """símbolo à esquerda e o nome à direita, com o texto medido para caber na largura (nada cortado)"""
    s = 4
    im = Image.new('RGBA', (w * s, h * s), (0, 0, 0, 0))
    lado = 184
    m = (h - lado) // 2
    im.alpha_composite(simbolo(lado * s), (12 * s, m * s))
    d = ImageDraw.Draw(im)
    x = (12 + lado + 22) * s
    livre = w * s - x - 10 * s
    tam = 64
    while ImageFont.truetype(F_BOLD, tam * s).getlength('Recicla Vale') > livre:
        tam -= 1
    f1 = ImageFont.truetype(F_BOLD, tam * s)
    larg = int(f1.getlength('Recicla Vale'))
    f2 = ImageFont.truetype(F_COND, int(tam * 0.62) * s)
    # METAIS espaçado em cobre, com a mesma largura do nome
    letras = 'METAIS'
    lw = [f2.getlength(c) for c in letras]
    esp = (larg - sum(lw)) / (len(letras) - 1)
    y1 = m * s + int(lado * 0.10) * s
    d.text((x, y1), 'Recicla Vale', font=f1, fill=AZUL)
    y2 = y1 + int(tam * 1.22) * s
    cx = x
    for c, l in zip(letras, lw):
        d.text((cx, y2), c, font=f2, fill=COBRE)
        cx += l + esp
    y3 = y2 + int(tam * 0.62 * 1.35) * s
    d.rectangle([x, y3, x + larg, y3 + 6 * s], fill=AZUL2)
    out = im.resize((w, h), Image.LANCZOS)
    return out, out.getbbox()


if __name__ == '__main__':
    lg, bb = logo()
    ic = simbolo(128)
    alvos = [os.path.join(HERE, 'assets'), os.path.normpath(os.path.join(HERE, '..', 'mundo', 'storage', 'avatars'))]
    for a in alvos:
        os.makedirs(a, exist_ok=True)
        lg.save(os.path.join(a, 'recicla-vale-logo.png'), optimize=True)
        ic.save(os.path.join(a, 'recicla-vale-icone.png'), optimize=True)
    print('logo', lg.size, 'conteúdo', bb, '| ícone', ic.size, '->', ', '.join(alvos))
