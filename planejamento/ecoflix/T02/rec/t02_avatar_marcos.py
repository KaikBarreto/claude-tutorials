#!/usr/bin/env python3
"""T2 · desenha a foto do Marcos Antunes (avatar por código, sem rosto real, sem logo nem texto) e grava:
  rec/t02/assets/marcos-antunes.jpg            o arquivo que o robô sobe no cap05 ("Selecionar foto" do Editar)
  rec/mundo/storage/avatars/marcos-antunes.jpg a foto que a semente t02/apos-cap05 aponta (caps 6 a 10: o Supabase falso
                                               guarda o que é enviado só na memória, e o capítulo seguinte parte da semente)
512x512, no estilo da marca: fundo verde (o acento #50D088 escurecendo para #2E7D57), busto estilizado com o colete laranja
de pátio e o capacete amarelo de quem trabalha na balança. Rodar de novo refaz os dois arquivos iguais (determinístico).
Uso: python3 -I rec/t02/t02_avatar_marcos.py"""
import os

from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
REC = os.path.dirname(HERE)
SAIDAS = [os.path.join(HERE, 'assets', 'marcos-antunes.jpg'), os.path.join(REC, 'mundo', 'storage', 'avatars', 'marcos-antunes.jpg')]
S = 512
K = 4   # desenha em 4x e reduz (bordas suaves)


def mistura(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def desenha():
    W = S * K
    img = Image.new('RGB', (W, W))
    px = ImageDraw.Draw(img)
    topo, base = (0x50, 0xD0, 0x88), (0x2E, 0x7D, 0x57)
    for y in range(W):   # gradiente vertical do fundo
        px.line([(0, y), (W, y)], fill=mistura(topo, base, y / (W - 1)))
    d = ImageDraw.Draw(img)
    c = W // 2
    # sombra suave atrás do busto
    sombra = Image.new('L', (W, W), 0)
    ImageDraw.Draw(sombra).ellipse([c - 150 * K, 300 * K, c + 150 * K, 620 * K], fill=90)
    sombra = sombra.filter(ImageFilter.GaussianBlur(18 * K))
    img.paste(Image.new('RGB', (W, W), (0x1F, 0x5E, 0x40)), (0, 0), sombra)
    # ombros e camiseta
    d.rounded_rectangle([c - 175 * K, 368 * K, c + 175 * K, 620 * K], radius=150 * K, fill=(0x3B, 0x4A, 0x5C))
    # colete laranja com faixas refletivas
    d.rounded_rectangle([c - 150 * K, 385 * K, c - 40 * K, 620 * K], radius=60 * K, fill=(0xF2, 0x8C, 0x28))
    d.rounded_rectangle([c + 40 * K, 385 * K, c + 150 * K, 620 * K], radius=60 * K, fill=(0xF2, 0x8C, 0x28))
    for y0 in (455, 500):
        d.rectangle([c - 150 * K, y0 * K, c - 40 * K, (y0 + 16) * K], fill=(0xE8, 0xEC, 0xEF))
        d.rectangle([c + 40 * K, y0 * K, c + 150 * K, (y0 + 16) * K], fill=(0xE8, 0xEC, 0xEF))
    # pescoço e cabeça (formas simples, sem traços de rosto)
    d.rounded_rectangle([c - 34 * K, 300 * K, c + 34 * K, 392 * K], radius=24 * K, fill=(0xC6, 0x8B, 0x63))
    d.ellipse([c - 86 * K, 150 * K, c + 86 * K, 340 * K], fill=(0xD9, 0x9C, 0x72))
    # capacete amarelo: cúpula, aba e friso
    d.chord([c - 104 * K, 112 * K, c + 104 * K, 300 * K], start=180, end=360, fill=(0xFF, 0xC7, 0x2C))
    d.rounded_rectangle([c - 122 * K, 196 * K, c + 122 * K, 222 * K], radius=13 * K, fill=(0xF0, 0xB0, 0x10))
    d.rounded_rectangle([c - 14 * K, 118 * K, c + 14 * K, 204 * K], radius=12 * K, fill=(0xF5, 0xBA, 0x1A))
    return img.resize((S, S), Image.LANCZOS)


def main():
    img = desenha()
    for p in SAIDAS:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        img.save(p, 'JPEG', quality=88, optimize=True)
        print(f'{os.path.relpath(p, REC)}: {os.path.getsize(p)} bytes')


if __name__ == '__main__':
    main()
