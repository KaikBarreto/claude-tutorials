"""Fundo escuro original do palco (pedido do Kaik, 30/10 15:02: "algo dark", no espírito dos fundos do Recordly e do
Screen Studio). Folhas curvas quase pretas iluminadas de lado: cada folha tem uma borda acesa na cor da marca
(#00C597, com um fio ciano) e a luz escorre para dentro dela em degradê longo. Desenho próprio, gerado por código.
Como a gravação cobre o centro, as bordas acesas cruzam as margens (esquerda, direita, alto e baixo).
uso: python3 fundo_escuro.py [saida.png]   (1920x1080)"""
import os
import sys

import cv2
import numpy as np

W, H = 1920, 1080
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "fundo_escuro.png")
y, x = np.mgrid[0:H, 0:W].astype(np.float32)
u, v = x / W, y / H
C = lambda *c: np.array(c, np.float32)  # noqa: E731


def smooth(a, b, t):
    t = np.clip((t - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def mix(a, b, t):
    return a + (b - a) * np.asarray(t, np.float32)[..., None]


def folha(img, d, L, lit, dark, rim, gain=1.0, sombra=0.0):
    """d = distância assinada à borda (px), positiva DENTRO da folha. Pinta a folha por cima de img."""
    dentro = smooth(-1.0, 1.0, d)
    lum = np.exp(-np.clip(d, 0, None) / L) * gain
    cor = mix(dark, lit, np.clip(lum, 0, 1))
    if sombra:  # sombra suave que a folha joga do lado de fora da borda
        img = img * (1 - sombra * np.exp(-np.clip(-d, 0, None) / 45.0) * (d < 0))[..., None]
    img = img * (1 - dentro[..., None]) + cor * dentro[..., None]
    luz = C(*rim) * (np.exp(-(d / 1.3) ** 2) * 0.9)[..., None]
    luz += C(70, 200, 255) * (np.exp(-((d - 3.2) / 1.5) ** 2) * 0.35)[..., None]  # fio ciano logo dentro da borda
    return img, luz * gain


img = mix(C(12, 19, 17), C(3, 5, 5), np.clip(0.45 * u + 0.65 * v, 0, 1))
img += C(0, 30, 23) * np.exp(-(((u - 0.05) / 0.30) ** 2 + ((v - 0.15) / 0.40) ** 2))[..., None]
img += C(0, 22, 30) * np.exp(-(((u - 0.98) / 0.25) ** 2 + ((v - 0.95) / 0.35) ** 2))[..., None]
luz = np.zeros_like(img)

# folha de trás, à direita: borda desce do alto (x~0.79W) até a direita embaixo, acesa por dentro
gR = W * (0.79 + 0.19 * v ** 0.85)
dR = (x - gR) / np.sqrt(1 + (W * 0.19 * 0.85 * np.maximum(v, 1e-3) ** -0.15 / H) ** 2)
img, l = folha(img, dR, 260, C(34, 170, 135), C(5, 9, 9), (175, 255, 228), gain=0.95)
luz += l

# folha do alto: faixa que nasce no canto de cima à esquerda e cai para a direita (borda de baixo acesa)
hT = H * (0.04 + 0.30 * u ** 1.7)
dT = (hT - y) / np.sqrt(1 + (H * 0.30 * 1.7 * np.maximum(u, 1e-3) ** 0.7 / W) ** 2)
img, l = folha(img, dT, 140, C(30, 120, 98), C(6, 10, 10), (150, 245, 215), gain=0.75, sombra=0.35)
luz += l

# folha da frente, à esquerda embaixo: borda curva que cruza a margem esquerda e sai pelo pé da tela
gL = W * (-0.07 + 0.27 * v ** 1.25)
dL = (gL - x) / np.sqrt(1 + (W * 0.27 * 1.25 * np.maximum(v, 1e-3) ** 0.25 / H) ** 2)
img, l = folha(img, dL, 220, C(52, 205, 165), C(4, 8, 8), (195, 255, 236), gain=1.0, sombra=0.45)
luz += l

img += luz
img += cv2.GaussianBlur(luz, (0, 0), 18) * 0.45 + cv2.GaussianBlur(luz, (0, 0), 60) * 0.30
img *= (1 - 0.30 * np.clip(((u - 0.5) / 0.65) ** 2 + ((v - 0.5) / 0.8) ** 2, 0, 1))[..., None]
img += np.random.default_rng(7).normal(0, 2.4, (H, W, 1)).astype(np.float32)
img = np.clip(img, 0, 255).astype(np.uint8)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
cv2.imwrite(OUT, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
print(OUT, "média", img.mean().round(1))
