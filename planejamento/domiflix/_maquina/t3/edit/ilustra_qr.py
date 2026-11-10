"""Ilustração do cap. 10 (pedido do Kaik, 30/10 15:59): a tela do sistema vira um fundo branco, o celular aponta para o
QR Code colado no aparelho e o portal do cliente abre já nesse aparelho, com o histórico de manutenção; depois volta
para o sistema. Desenho próprio e genérico (aparelho e celular sem marca), Montserrat, verde #00C597.
Sai como sequência PNG com alfa no tamanho da janela do app em repouso (1587x992, cantos de 16 px), para o editor
colocar em "illustrations" (box = janela, scale_in 0). Tempos em segundos locais, casados com a fala:
  0,2 "Quando o cliente..."  1,9 "aponta a câmera do celular"  3,5 "abre o portal do cliente"
  5,0 "já nesse aparelho"  6,0 "com o histórico de manutenção"
uso: python3 ilustra_qr.py <pasta_saida> [duração=8.1]"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "kit"))
import ui  # noqa: E402

OUT = sys.argv[1]
DUR = float(sys.argv[2]) if len(sys.argv) > 2 else 8.1
W, H, S, FPS = 1587, 992, 2, 30
VERDE = (0, 197, 151)
ESCURO = (30, 30, 30)
TXT = (24, 24, 27)
CINZA = (113, 113, 122)


def oc(t):
    t = min(1.0, max(0.0, t))
    return 1 - (1 - t) ** 3


def io(t):
    t = min(1.0, max(0.0, t))
    return t * t * (3 - 2 * t)


def f(w, px):
    return ui.font(w, int(px * S))


def rr(d, box, r, **kw):
    x0, y0, x1, y1 = box
    d.rounded_rectangle([x0 * S, y0 * S, x1 * S, y1 * S], radius=r * S, **kw)


def qr_modulos(seed=26, n=25):
    rng = np.random.default_rng(seed)
    m = rng.random((n, n)) < 0.48
    for (r, c) in ((0, 0), (0, n - 7), (n - 7, 0)):
        m[r:r + 7, c:c + 7] = False
        m[r, c:c + 7] = m[r + 6, c:c + 7] = True
        m[r:r + 7, c] = m[r:r + 7, c + 6] = True
        m[r + 2:r + 5, c + 2:c + 5] = True
        m[max(0, r - 1):r + 8, c + 7 if c == 0 else c - 1] = False
        m[r + 7 if r == 0 else r - 1, max(0, c - 1):c + 8] = False
    return m


QR = qr_modulos()


def desenha_qr(d, x, y, lado, cor=TXT, fundo=(255, 255, 255), borda=0.12):
    rr(d, (x, y, x + lado, y + lado), lado * 0.08, fill=fundo)
    n = QR.shape[0]
    q = lado * (1 - 2 * borda) / n
    ox, oy = x + lado * borda, y + lado * borda
    for i in range(n):
        for j in range(n):
            if QR[i, j]:
                d.rectangle([(ox + j * q) * S, (oy + i * q) * S, (ox + (j + 1) * q) * S - 1, (oy + (i + 1) * q) * S - 1], fill=cor)


# ------------------------------------------------------------------ fundo e aparelho (estáticos)
def fundo():
    im = Image.new("RGB", (W * S, H * S), (255, 255, 255))
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    g = np.exp(-(((xx - 470) / 520) ** 2 + ((yy - 440) / 360) ** 2))
    arr = np.full((H, W, 3), 255, np.float32)
    arr -= (np.array([255, 255, 255]) - np.array([231, 248, 243])) * (0.55 * g)[..., None]
    v = np.clip(((xx - W / 2) / (W * 0.7)) ** 2 + ((yy - H / 2) / (H * 0.8)) ** 2, 0, 1)
    arr -= 10 * v[..., None]
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).resize((W * S, H * S), Image.BICUBIC)
    return im.convert("RGBA")


AC = (150, 330, 770, 520)  # corpo do Hi-Wall
STK = (628, 362, 742, 476)  # adesivo do QR no aparelho


def aparelho(base):
    sh = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ds = ImageDraw.Draw(sh)
    rr(ds, (AC[0] + 10, AC[1] + 26, AC[2] - 10, AC[3] + 26), 44, fill=(0, 40, 30, 70))
    sh = sh.filter(ImageFilter.GaussianBlur(22 * S))
    base.alpha_composite(sh)
    d = ImageDraw.Draw(base)
    rr(d, AC, 44, fill=(252, 252, 252), outline=(222, 224, 228), width=2 * S)
    rr(d, (AC[0] + 34, AC[3] - 46, AC[2] - 34, AC[3] - 22), 12, fill=(214, 216, 222))
    for k in range(5):
        y = AC[3] - 42 + k * 4
        d.line([(AC[0] + 46) * S, y * S, (AC[2] - 46) * S, y * S], fill=(196, 199, 206), width=S)
    d.ellipse([(AC[0] + 40) * S, (AC[1] + 34) * S, (AC[0] + 52) * S, (AC[1] + 46) * S], fill=VERDE)
    desenha_qr(d, STK[0], STK[1], STK[2] - STK[0])
    rr(d, STK, 9, outline=(30, 30, 30), width=2 * S)
    t1, t2 = "Hi-Wall 18.000 BTUs", "Sala dos professores"
    w1 = d.textlength(t1, font=f(700, 30)) / S
    w2 = d.textlength(t2, font=f(500, 24)) / S
    cx = (AC[0] + AC[2]) / 2
    d.text(((cx - w1 / 2) * S, 568 * S), t1, font=f(700, 30), fill=TXT)
    d.text(((cx - w2 / 2) * S, 610 * S), t2, font=f(500, 24), fill=CINZA)
    return base


BASE = aparelho(fundo())

# ------------------------------------------------------------------ celular
PW, PH = 350, 700
PX, PY = 1050, 146  # posição final


def tela_camera(d, x, y, w, h, tau):
    rr(d, (x, y, x + w, y + h), 34, fill=(36, 38, 42))
    lado = 190
    qx, qy = x + (w - lado) / 2, y + h * 0.40 - lado / 2
    desenha_qr(d, qx, qy, lado, cor=(20, 20, 22), fundo=(236, 236, 236))
    c = 26
    for (ax, ay, sx, sy) in ((qx - 16, qy - 16, 1, 1), (qx + lado + 16, qy - 16, -1, 1),
                             (qx - 16, qy + lado + 16, 1, -1), (qx + lado + 16, qy + lado + 16, -1, -1)):
        d.line([ax * S, ay * S, (ax + sx * c) * S, ay * S], fill=VERDE, width=5 * S)
        d.line([ax * S, ay * S, ax * S, (ay + sy * c) * S], fill=VERDE, width=5 * S)
    p = (tau - 2.3) / 0.9
    if 0 <= p <= 1:
        k = p * 2 if p < 0.5 else (1 - p) * 2  # desce e sobe
        ly = qy - 10 + (lado + 20) * k
        for gl, a in ((14, 40), (7, 90), (2, 255)):
            d.rectangle([(qx - 18) * S, (ly - gl / 2) * S, (qx + lado + 18) * S, (ly + gl / 2) * S], fill=VERDE + (a,))
    d.ellipse([(x + w / 2 - 34) * S, (y + h - 96) * S, (x + w / 2 + 34) * S, (y + h - 28) * S], outline=(240, 240, 240), width=5 * S)


def tela_portal(d, x, y, w, h, tau):
    rr(d, (x, y, x + w, y + h), 34, fill=(255, 255, 255))
    a = oc((tau - 3.5) / 0.4)
    d.text(((x + 26) * S, (y + 58 - 8 * (1 - a)) * S), "Portal do cliente", font=f(700, 28), fill=TXT + (int(255 * a),))
    d.line([(x + 26) * S, (y + 102) * S, (x + w - 26) * S, (y + 102) * S], fill=(228, 228, 231, int(255 * a)), width=2 * S)
    b = oc((tau - 3.85) / 0.45)
    if b > 0:
        cy = y + 124 + 20 * (1 - b)
        hl = io((tau - 5.0) / 0.35) * (1 - io((tau - 6.3) / 0.6))
        if hl > 0:
            rr(d, (x + 14, cy - 8, x + w - 14, cy + 102), 22, outline=VERDE + (int(255 * hl),), width=4 * S)
        rr(d, (x + 22, cy, x + w - 22, cy + 94), 18, fill=(244, 244, 245, int(255 * b)))
        # ícone 42 px e título 19 px: com 21 px o nome passava 20 px da borda do cartão (Kaik viu na parte 3, 30/10)
        d.ellipse([(x + 34) * S, (cy + 26) * S, (x + 76) * S, (cy + 68) * S], fill=VERDE + (int(255 * b),))
        for k in range(3):
            yy = cy + 38 + k * 9
            d.line([(x + 45) * S, yy * S, (x + 65) * S, yy * S], fill=(255, 255, 255, int(255 * b)), width=3 * S)
        d.text(((x + 90) * S, (cy + 22) * S), "Hi-Wall 18.000 BTUs", font=f(700, 19), fill=TXT + (int(255 * b),))
        d.text(((x + 90) * S, (cy + 50) * S), "Sala dos professores", font=f(500, 17), fill=CINZA + (int(255 * b),))
    c = oc((tau - 6.0) / 0.35)
    if c > 0:
        sy = y + 262
        d.text(((x + 26) * S, (sy + 8 * (1 - c)) * S), "Histórico de manutenção", font=f(700, 22), fill=TXT + (int(255 * c),))
        for i in range(3):
            e = oc((tau - 6.2 - 0.25 * i) / 0.35)
            if e <= 0:
                continue
            ry = sy + 50 + i * 80 + 14 * (1 - e)
            al = int(255 * e)
            rr(d, (x + 22, ry, x + w - 22, ry + 68), 14, outline=(228, 228, 231, al), width=2 * S)
            d.ellipse([(x + 38) * S, (ry + 18) * S, (x + 66) * S, (ry + 46) * S], fill=VERDE + (al,))
            d.line([(x + 45) * S, (ry + 32) * S, (x + 51) * S, (ry + 38) * S, (x + 60) * S, (ry + 26) * S],
                   fill=(255, 255, 255, al), width=3 * S, joint="curve")
            d.text(((x + 80) * S, (ry + 11) * S), "Ordem de serviço", font=f(600, 19), fill=TXT + (al,))
            rr(d, (x + 80, ry + 44, x + 80 + [150, 120, 170][i], ry + 54), 5, fill=(228, 228, 231, al))


def celular(tau):
    lay = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    k = oc((tau - 0.9) / 0.8)
    if k <= 0:
        return lay, None
    x = PX + 560 * (1 - k)
    y = PY + 30 * (1 - k)
    d = ImageDraw.Draw(lay)
    rr(d, (x - 4, y + 18, x + PW + 4, y + PH + 30), 52, fill=(0, 30, 22, 60))
    lay = lay.filter(ImageFilter.GaussianBlur(18 * S))
    d = ImageDraw.Draw(lay)
    rr(d, (x, y, x + PW, y + PH), 50, fill=(34, 36, 40))
    rr(d, (x + 4, y + 4, x + PW - 4, y + PH - 4), 46, outline=(70, 73, 80), width=2 * S)
    sx, sy, sw, sh = x + 14, y + 14, PW - 28, PH - 28
    if tau < 3.45:
        tela_camera(d, sx, sy, sw, sh, tau)
    else:
        tela_portal(d, sx, sy, sw, sh, tau)
    fl = 1 - abs((tau - 3.42) / 0.12) if abs(tau - 3.42) < 0.12 else 0
    if fl > 0:
        rr(d, (sx, sy, sx + sw, sy + sh), 34, fill=(255, 255, 255, int(230 * fl)))
    rr(d, (x + PW / 2 - 52, y + 24, x + PW / 2 + 52, y + 50), 13, fill=(12, 12, 14))
    return lay, (x, y)


def quadro(tau):
    im = BASE.copy()
    d = ImageDraw.Draw(im)
    # o adesivo brilha quando o celular lê e quando a fala diz "já nesse aparelho"
    g = max(io((tau - 2.3) / 0.3) * (1 - io((tau - 3.6) / 0.4)), io((tau - 5.0) / 0.3) * (1 - io((tau - 6.2) / 0.5)))
    if g > 0:
        gl = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dg = ImageDraw.Draw(gl)
        rr(dg, (STK[0] - 10, STK[1] - 10, STK[2] + 10, STK[3] + 10), 16, outline=VERDE + (int(230 * g),), width=5 * S)
        im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(2 * S)))
        rr(ImageDraw.Draw(im), (STK[0] - 10, STK[1] - 10, STK[2] + 10, STK[3] + 10), 16, outline=VERDE + (int(255 * g),), width=3 * S)
    lay, pos = celular(tau)
    # linha tracejada do adesivo até o celular enquanto "aponta"
    a = io((tau - 1.9) / 0.5) * (1 - io((tau - 3.5) / 0.4))
    if a > 0 and pos is not None:
        x0, y0 = STK[2] + 16, (STK[1] + STK[3]) / 2
        x1, y1 = pos[0] - 18, pos[1] + PH * 0.40
        n = 26
        prog = io((tau - 1.9) / 0.6)
        for i in range(n):
            if i % 2 or i / n > prog:
                continue
            t0, t1 = i / n, (i + 1) / n
            p0 = (x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0 - 60 * np.sin(np.pi * t0))
            p1 = (x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1 - 60 * np.sin(np.pi * t1))
            d.line([p0[0] * S, p0[1] * S, p1[0] * S, p1[1] * S], fill=VERDE + (int(255 * a),), width=4 * S)
    im.alpha_composite(lay)
    # o aparelho entra com um leve "pop" no começo
    out = im.resize((W, H), Image.LANCZOS)
    return out


def mascara():
    a, _ = ui.rrect_alpha(W, H, 0, 0, W, H, 16)
    return (a * 255).astype(np.uint8)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    m = mascara()
    n = int(round(DUR * FPS))
    for i in range(n):
        tau = i / FPS
        fr = np.array(quadro(tau).convert("RGB"))
        # entrada: o aparelho e o rótulo surgem (o painel branco em si entra pelo fade do editor)
        rgba = np.dstack([fr, m])
        Image.fromarray(rgba, "RGBA").save(os.path.join(OUT, f"{i:04d}.png"), optimize=False, compress_level=1)
        if i % 30 == 0:
            print(f"{i}/{n}", flush=True)
    print("ok", OUT, n, "quadros")
