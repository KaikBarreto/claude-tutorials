"""T21 cap03 · ilustração da leitura do QR (roteiro: "um celular genérico, sem marca nem a interface do aplicativo de mensagens, com a
câmera apontada para um QR Code na tela de um computador; fundo branco, Montserrat, o verde da marca"; molde
exemplos/dominex-t3/ilustracoes/ilustra_qr.py). Desenho próprio e genérico: um monitor com o QR na tela, o celular entra, a câmera
enquadra o código (cantos verdes e a linha de leitura) e o celular mostra um "pronto" genérico (círculo verde com o visto), sem texto
nem tela de aplicativo. Tempos locais casados com a fala da L2 do cap03 (13,2 s do capítulo = 0 s aqui):
  0,0 "Aí, no celular da empresa"  1,9 "é só apontar a câmera pro código"  4,0 "na opção de conectar um aparelho"
Sai como sequência PNG com alfa no tamanho da janela do app em repouso (1587x992, cantos de 16 px).
uso: python3 -I ilustra_qr_wa.py <pasta_saida> [duração=6.0] [--so 0.5,2.9,5.0] (--so: só esses instantes, para conferir 1:1)"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
TUT_HOME = os.environ.get("TUT_HOME") or os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(TUT_HOME, "kit"))
import ui  # noqa: E402

args = [a for a in sys.argv[1:]]
SO = None
if "--so" in args:
    k = args.index("--so")
    SO = [float(x) for x in args[k + 1].split(",")]
    del args[k:k + 2]
OUT = args[0]
DUR = float(args[1]) if len(args) > 1 else 6.0
W, H, S, FPS = 1587, 992, 2, 30
VERDE = (0, 197, 151)
TXT = (24, 24, 27)


def oc(t):
    t = min(1.0, max(0.0, t))
    return 1 - (1 - t) ** 3


def io(t):
    t = min(1.0, max(0.0, t))
    return t * t * (3 - 2 * t)


def rr(d, box, r, **kw):
    x0, y0, x1, y1 = box
    d.rounded_rectangle([x0 * S, y0 * S, x1 * S, y1 * S], radius=r * S, **kw)


def qr_modulos(seed=21, n=25):
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
    rr(d, (x, y, x + lado, y + lado), lado * 0.06, fill=fundo)
    n = QR.shape[0]
    q = lado * (1 - 2 * borda) / n
    ox, oy = x + lado * borda, y + lado * borda
    for i in range(n):
        for j in range(n):
            if QR[i, j]:
                d.rectangle([(ox + j * q) * S, (oy + i * q) * S, (ox + (j + 1) * q) * S - 1, (oy + (i + 1) * q) * S - 1], fill=cor)


# ------------------------------------------------------------------ fundo e monitor (estáticos)
def fundo():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    g = np.exp(-(((xx - 520) / 560) ** 2 + ((yy - 430) / 380) ** 2))
    arr = np.full((H, W, 3), 255, np.float32)
    arr -= (np.array([255, 255, 255]) - np.array([231, 248, 243])) * (0.55 * g)[..., None]
    v = np.clip(((xx - W / 2) / (W * 0.7)) ** 2 + ((yy - H / 2) / (H * 0.8)) ** 2, 0, 1)
    arr -= 10 * v[..., None]
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).resize((W * S, H * S), Image.BICUBIC)
    return im.convert("RGBA")


MON = (150, 196, 870, 646)       # moldura do monitor
TELA = (172, 218, 848, 624)      # tela
QRL = 230                        # lado do QR na tela
QRX, QRY = (TELA[0] + TELA[2]) / 2 - QRL / 2, 276  # QR centrado na tela (cartão de 254 a 598, abaixo da barra da janela)


def monitor(base):
    sh = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ds = ImageDraw.Draw(sh)
    rr(ds, (MON[0] + 14, MON[1] + 28, MON[2] - 14, MON[3] + 30), 26, fill=(0, 40, 30, 70))
    sh = sh.filter(ImageFilter.GaussianBlur(22 * S))
    base.alpha_composite(sh)
    d = ImageDraw.Draw(base)
    # pé do monitor
    d.polygon([((MON[0] + MON[2]) / 2 * S - 46 * S, MON[3] * S), ((MON[0] + MON[2]) / 2 * S + 46 * S, MON[3] * S),
               ((MON[0] + MON[2]) / 2 * S + 62 * S, 728 * S), ((MON[0] + MON[2]) / 2 * S - 62 * S, 728 * S)], fill=(206, 209, 215))
    rr(d, ((MON[0] + MON[2]) / 2 - 150, 724, (MON[0] + MON[2]) / 2 + 150, 746), 11, fill=(196, 199, 206))
    # moldura e tela
    rr(d, MON, 26, fill=(40, 42, 47))
    rr(d, TELA, 12, fill=(250, 250, 251))
    # barra de janela genérica (três pontos e uma faixa cinza, sem marca nem texto)
    rr(d, (TELA[0], TELA[1], TELA[2], TELA[1] + 30), 12, fill=(238, 239, 242))
    d.rectangle([TELA[0] * S, (TELA[1] + 18) * S, TELA[2] * S, (TELA[1] + 30) * S], fill=(238, 239, 242))
    for k, cor in enumerate(((232, 104, 94), (238, 190, 80), (98, 196, 120))):
        cx = TELA[0] + 22 + k * 20
        d.ellipse([(cx - 6) * S, (TELA[1] + 9) * S, (cx + 6) * S, (TELA[1] + 21) * S], fill=cor)
    # cartão com o QR e linhas cinza no lugar do texto
    rr(d, (QRX - 30, QRY - 22, QRX + QRL + 30, QRY + QRL + 92), 16, fill=(255, 255, 255), outline=(226, 228, 232), width=2 * S)
    desenha_qr(d, QRX, QRY, QRL)
    cx = QRX + QRL / 2
    rr(d, (cx - 120, QRY + QRL + 24, cx + 120, QRY + QRL + 38), 7, fill=(220, 222, 227))
    rr(d, (cx - 80, QRY + QRL + 50, cx + 80, QRY + QRL + 62), 6, fill=(232, 233, 237))
    return base


BASE = monitor(fundo())

# ------------------------------------------------------------------ celular
PW, PH = 350, 700
PX, PY = 1060, 146  # posição final
T_LEITURA = 3.95    # instante em que o código é lido (flash)


def tela_camera(d, x, y, w, h, tau):
    rr(d, (x, y, x + w, y + h), 34, fill=(36, 38, 42))
    lado = 196
    qx, qy = x + (w - lado) / 2, y + h * 0.42 - lado / 2
    desenha_qr(d, qx, qy, lado, cor=(20, 20, 22), fundo=(236, 236, 236))
    c = 28
    for (ax, ay, sx, sy) in ((qx - 18, qy - 18, 1, 1), (qx + lado + 18, qy - 18, -1, 1),
                             (qx - 18, qy + lado + 18, 1, -1), (qx + lado + 18, qy + lado + 18, -1, -1)):
        d.line([ax * S, ay * S, (ax + sx * c) * S, ay * S], fill=VERDE, width=5 * S)
        d.line([ax * S, ay * S, ax * S, (ay + sy * c) * S], fill=VERDE, width=5 * S)
    p = (tau - 2.7) / 1.1
    if 0 <= p <= 1:
        k = p * 2 if p < 0.5 else (1 - p) * 2  # desce e sobe
        ly = qy - 10 + (lado + 20) * k
        for gl, a in ((14, 40), (7, 90), (2, 255)):
            d.rectangle([(qx - 20) * S, (ly - gl / 2) * S, (qx + lado + 20) * S, (ly + gl / 2) * S], fill=VERDE + (a,))
    d.ellipse([(x + w / 2 - 34) * S, (y + h - 96) * S, (x + w / 2 + 34) * S, (y + h - 28) * S], outline=(240, 240, 240), width=5 * S)


def tela_pronto(d, x, y, w, h, tau):
    rr(d, (x, y, x + w, y + h), 34, fill=(255, 255, 255))
    a = oc((tau - T_LEITURA - 0.05) / 0.45)
    cx, cy, r = x + w / 2, y + h * 0.40, 74 * (0.75 + 0.25 * a)
    d.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S], fill=VERDE + (int(255 * a),))
    b = oc((tau - T_LEITURA - 0.30) / 0.35)  # o visto se desenha
    if b > 0:
        p0, p1, p2 = (cx - 32, cy + 2), (cx - 8, cy + 26), (cx + 36, cy - 24)
        if b < 0.45:
            u = b / 0.45
            pts = [p0, (p0[0] + (p1[0] - p0[0]) * u, p0[1] + (p1[1] - p0[1]) * u)]
        else:
            u = (b - 0.45) / 0.55
            pts = [p0, p1, (p1[0] + (p2[0] - p1[0]) * u, p1[1] + (p2[1] - p1[1]) * u)]
        d.line([(px * S, py * S) for px, py in pts], fill=(255, 255, 255, 255), width=12 * S, joint="curve")
    e = oc((tau - T_LEITURA - 0.55) / 0.45)  # linhas cinza no lugar de texto (sem tela de aplicativo)
    if e > 0:
        for k, (lw, yy) in enumerate(((180, cy + r + 52), (130, cy + r + 80))):
            al = int(255 * e)
            rr(d, (cx - lw / 2, yy, cx + lw / 2, yy + 12), 6, fill=(226, 228, 232, al))


def celular(tau):
    lay = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    k = oc((tau - 0.35) / 0.85)
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
    if tau < T_LEITURA:
        tela_camera(d, sx, sy, sw, sh, tau)
    else:
        tela_pronto(d, sx, sy, sw, sh, tau)
    fl = 1 - abs((tau - T_LEITURA) / 0.12) if abs(tau - T_LEITURA) < 0.12 else 0
    if fl > 0:
        rr(d, (sx, sy, sx + sw, sy + sh), 34, fill=(255, 255, 255, int(230 * fl)))
    rr(d, (x + PW / 2 - 52, y + 24, x + PW / 2 + 52, y + 50), 13, fill=(12, 12, 14))
    return lay, (x, y)


def quadro(tau):
    im = BASE.copy()
    d = ImageDraw.Draw(im)
    # o QR da tela brilha quando a câmera lê e fica com o contorno verde depois de ler
    g = max(io((tau - 2.7) / 0.3) * (1 - io((tau - T_LEITURA) / 0.3)), 0.85 * io((tau - T_LEITURA) / 0.4))
    if g > 0:
        box = (QRX - 30 - 10, QRY - 22 - 10, QRX + QRL + 30 + 10, QRY + QRL + 92 + 10)
        gl = Image.new("RGBA", im.size, (0, 0, 0, 0))
        rr(ImageDraw.Draw(gl), box, 22, outline=VERDE + (int(230 * g),), width=5 * S)
        im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(2 * S)))
        rr(ImageDraw.Draw(im), box, 22, outline=VERDE + (int(255 * g),), width=3 * S)
    lay, pos = celular(tau)
    # linha tracejada do QR da tela até o celular enquanto "aponta"
    a = io((tau - 1.9) / 0.5) * (1 - io((tau - T_LEITURA) / 0.4))
    if a > 0 and pos is not None:
        x0, y0 = QRX + QRL + 46, QRY + QRL / 2
        x1, y1 = pos[0] - 18, pos[1] + PH * 0.42
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
    return im.resize((W, H), Image.LANCZOS)


def mascara():
    a, _ = ui.rrect_alpha(W, H, 0, 0, W, H, 16)
    return (a * 255).astype(np.uint8)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    m = mascara()
    tempos = SO if SO is not None else [i / FPS for i in range(int(round(DUR * FPS)))]
    for i, tau in enumerate(tempos):
        fr = np.array(quadro(tau).convert("RGB"))
        nome = f"so_{tau:.2f}.png" if SO is not None else f"{i:04d}.png"
        Image.fromarray(np.dstack([fr, m]), "RGBA").save(os.path.join(OUT, nome), optimize=False, compress_level=1)
        if SO is None and i % 30 == 0:
            print(f"{i}/{len(tempos)}", flush=True)
    print("ok", OUT, len(tempos), "quadros")
