"""Ilustração do cap. 11 do T7 ("O relatório e o PDF"): o relatório vira um arquivo PDF e segue ao cliente por e-mail ou WhatsApp.
Motivo: o download do PDF não aparece na gravação (o robô não captura downloads). Fundo branco, Montserrat, verde #00C597,
objetos genéricos (folha, arquivo, envelope e balão de conversa sem marca, nenhum dado real).
Sai como sequência PNG com alfa (cartão de cantos arredondados com sombra), para o editor colocar em "illustrations".
Tempos em segundos locais (a ilustração entra em 38,2 s do capítulo = início da linha 5 da fala), casados com a fala do cap. 11
(tempo do capítulo - 38,2):
  0,3 "Com o PDF baixado"   2,1 "é só enviar ao cliente"   4,8 "como e-mail"   5,5 "ou WhatsApp"
uso: python3 ilustra_pdf.py <pasta_saida> [duração=6.3] [--teste t1,t2,...]  (--teste grava só esses quadros, em segundos)"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "kit"))
import ui  # noqa: E402

argv = list(sys.argv[1:])
TESTE = None
if "--teste" in argv:
    i = argv.index("--teste")
    TESTE = [float(x) for x in argv[i + 1].split(",")]
    del argv[i:i + 2]
args = [a for a in argv if not a.startswith("--")]
OUT = args[0]
DUR = float(args[1]) if len(args) > 1 else 6.3
W, H, S, FPS, PAD = 640, 720, 2, 30, 36          # tamanho final do PNG (com a margem da sombra), supersampling e quadros por segundo
VERDE, VERDE_ESC = (0, 197, 151), (0, 150, 115)
TXT, CINZA, CLARO, BORDA = (24, 24, 27), (113, 113, 122), (244, 244, 245), (228, 228, 231)
CX0, CY0, CW, CH = PAD, PAD, W - 2 * PAD, H - 2 * PAD   # o cartão


def io(t):
    t = min(1.0, max(0.0, t))
    return t * t * (3 - 2 * t)


def oc(t):
    t = min(1.0, max(0.0, t))
    return 1 - (1 - t) ** 3


def jan(t, a, b, fi=0.3, fo=0.25):
    return io((t - a) / fi) * (1 - io((t - (b - fo)) / fo))


def f(w, px):
    return ui.font(w, int(px * S))


def rr(d, box, r, **kw):
    x0, y0, x1, y1 = box
    d.rounded_rectangle([x0 * S, y0 * S, x1 * S, y1 * S], radius=r * S, **kw)


def txt(d, x, y, s, w, px, fill, anchor="la"):
    d.text((x * S, y * S), s, font=f(w, px), fill=fill, anchor=anchor)


def camada():
    return Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))


def cola(dst, src, a=1.0):
    if a <= 0.003:
        return
    if a < 0.999:
        al = src.getchannel("A").point(lambda v: int(v * a))
        src = src.copy()
        src.putalpha(al)
    dst.alpha_composite(src)


def sombra(box, r, dy=10, blur=12, alfa=46):
    lay = camada()
    d = ImageDraw.Draw(lay)
    x0, y0, x1, y1 = box
    rr(d, (x0 + 4, y0 + dy, x1 - 4, y1 + dy - 2), r, fill=(0, 40, 30, alfa))
    return lay.filter(ImageFilter.GaussianBlur(blur * S))


# ------------------------------------------------------------------ cartão de fundo (estático)
def cartao():
    yy, xx = np.mgrid[0:H * S, 0:W * S].astype(np.float32)
    g = np.exp(-(((xx / S - W / 2) / 360) ** 2 + ((yy / S - H / 2 + 30) / 360) ** 2))
    arr = np.full((H * S, W * S, 3), 255, np.float32)
    arr -= (np.array([255, 255, 255]) - np.array([231, 248, 243])) * (0.55 * g)[..., None]
    base = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")
    mask = Image.new("L", base.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([CX0 * S, CY0 * S, (CX0 + CW) * S, (CY0 + CH) * S], radius=26 * S, fill=255)
    out = camada()
    out.alpha_composite(sombra((CX0, CY0, CX0 + CW, CY0 + CH), 26, dy=14, blur=14, alfa=60))
    base.putalpha(mask)
    out.alpha_composite(base)
    return out


CARTAO = cartao()

TITULO = "O relatório em arquivo"
LEGENDAS = [  # (início, fim, texto)
    (0.35, 2.0, "Baixar PDF gera o arquivo"),
    (2.1, 4.6, "Pronto para enviar ao cliente"),
    (4.7, 6.3, "Por e-mail ou WhatsApp"),
]


def confere():
    linhas = [("título", ui.font(800, 30 * S).getlength(TITULO) / S, CW - 80)]
    for i, (_, _, t) in enumerate(LEGENDAS):
        linhas.append((f"legenda {i + 1}", ui.font(700, 24 * S).getlength(t) / S, CW - 80))
    linhas.append(("arquivo", ui.font(600, 15 * S).getlength("Relatorio-OS-16.pdf") / S, 190))
    for nome, larg, lim in linhas:
        assert larg <= lim, f"{nome}: {larg:.0f} > {lim}"
    return {n: round(l) for n, l, _ in linhas}


# ------------------------------------------------------------------ objetos
def folha(d_img, x, y, w, h, esc=1.0, selo=False, dobra=True):
    """folha de relatório genérica (cabeçalho verde, linhas, quadro de assinatura); `esc` escala em torno do centro"""
    lay = camada()
    d = ImageDraw.Draw(lay)
    cx, cy = x + w / 2, y + h / 2
    w2, h2 = w * esc, h * esc
    x0, y0 = cx - w2 / 2, cy - h2 / 2
    lay.alpha_composite(sombra((x0, y0, x0 + w2, y0 + h2), 8 * esc, dy=7, blur=7, alfa=50))
    d = ImageDraw.Draw(lay)
    rr(d, (x0, y0, x0 + w2, y0 + h2), 8 * esc, fill=(255, 255, 255), outline=BORDA, width=S)
    rr(d, (x0, y0, x0 + w2, y0 + 34 * esc), 8 * esc, fill=VERDE)
    d.rectangle([x0 * S, (y0 + 20 * esc) * S, (x0 + w2) * S, (y0 + 34 * esc) * S], fill=VERDE)
    if esc > 0.8:
        txt(d, x0 + 12 * esc, y0 + 10 * esc, "Relatório de Serviço", 700, 11 * esc, (255, 255, 255))
    for i in range(7):
        ww = (0.82 if i % 3 else 0.62) * w2 - 24 * esc
        rr(d, (x0 + 12 * esc, y0 + (50 + i * 17) * esc, x0 + 12 * esc + ww, y0 + (56 + i * 17) * esc), 3 * esc, fill=(228, 228, 231))
    rr(d, (x0 + 12 * esc, y0 + (h - 58) * esc, x0 + w2 - 12 * esc, y0 + (h - 14) * esc), 6 * esc, outline=(190, 190, 196), width=S)
    pts = [(x0 + (24 + 8 * k) * esc, y0 + (h - 36 + 9 * math.sin(k * 0.9)) * esc) for k in range(11)]
    d.line([(px * S, py * S) for px, py in pts], fill=(40, 40, 46), width=int(2 * S * esc), joint="curve")
    if selo:   # etiqueta PDF no canto
        rr(d, (x0 + w2 - 58 * esc, y0 + h2 - 30 * esc, x0 + w2 - 8 * esc, y0 + h2 - 8 * esc), 5 * esc, fill=VERDE_ESC)
        txt(d, x0 + w2 - 33 * esc, y0 + h2 - 19 * esc, "PDF", 800, 12 * esc, (255, 255, 255), "mm")
    if dobra:
        d.polygon([((x0 + w2 - 22 * esc) * S, y0 * S), ((x0 + w2) * S, (y0 + 22 * esc) * S), ((x0 + w2 - 22 * esc) * S, (y0 + 22 * esc) * S)], fill=(214, 240, 232))
    cola(d_img, lay)


def pilula(d_img, x, y, w, h, rotulo, a=1.0, anel=0.0):
    lay = camada()
    d = ImageDraw.Draw(lay)
    rr(d, (x, y, x + w, y + h), h / 2, fill=(30, 30, 30))
    txt(d, x + w / 2, y + h / 2, rotulo, 700, 15, (255, 255, 255), "mm")
    if anel > 0:   # anel do toque
        r = 18 + 26 * anel
        d.ellipse([(x + w * 0.62 - r) * S, (y + h / 2 - r) * S, (x + w * 0.62 + r) * S, (y + h / 2 + r) * S], outline=VERDE + (int(255 * (1 - anel)),), width=3 * S)
    cola(d_img, lay, a)


def arquivo(d_img, cx, cy, esc=1.0, a=1.0, nome=True, ok=False):
    lay = camada()
    d = ImageDraw.Draw(lay)
    w, h = 74 * esc, 94 * esc
    x0, y0 = cx - w / 2, cy - h / 2
    lay.alpha_composite(sombra((x0, y0, x0 + w, y0 + h), 7 * esc, dy=6, blur=6, alfa=50))
    d = ImageDraw.Draw(lay)
    rr(d, (x0, y0, x0 + w, y0 + h), 7 * esc, fill=(255, 255, 255), outline=VERDE_ESC, width=int(2 * S))
    d.polygon([((x0 + w - 20 * esc) * S, y0 * S), ((x0 + w) * S, (y0 + 20 * esc) * S), ((x0 + w - 20 * esc) * S, (y0 + 20 * esc) * S)], fill=(214, 240, 232))
    rr(d, (x0 + 8 * esc, y0 + h * 0.46, x0 + w - 8 * esc, y0 + h * 0.46 + 26 * esc), 5 * esc, fill=VERDE_ESC)
    txt(d, cx, y0 + h * 0.46 + 13 * esc, "PDF", 800, 15 * esc, (255, 255, 255), "mm")
    for i in range(3):
        rr(d, (x0 + 10 * esc, y0 + (12 + i * 7) * esc, x0 + w - (26 if i == 0 else 14) * esc, y0 + (15 + i * 7) * esc), 1.5 * esc, fill=(205, 205, 210))
    if nome:
        txt(d, cx, y0 + h + 16 * esc, "Relatorio-OS-16.pdf", 600, 15, CINZA, "ma")
    if ok:
        d.ellipse([(x0 + w - 14 * esc) * S, (y0 - 10 * esc) * S, (x0 + w + 14 * esc) * S, (y0 + 18 * esc) * S], fill=VERDE)
        d.line([((x0 + w - 8 * esc) * S, (y0 + 4 * esc) * S), ((x0 + w - 1 * esc) * S, (y0 + 10 * esc) * S), ((x0 + w + 9 * esc) * S, (y0 - 3 * esc) * S)], fill=(255, 255, 255), width=int(3 * S))
    cola(d_img, lay, a)


def canal(d_img, x, y, w, h, tipo, rotulo, a=1.0, realce=0.0):
    lay = camada()
    d = ImageDraw.Draw(lay)
    lay.alpha_composite(sombra((x, y, x + w, y + h), 16, dy=8, blur=8, alfa=40))
    d = ImageDraw.Draw(lay)
    borda = tuple(int(c1 + (c2 - c1) * realce) for c1, c2 in zip(BORDA, VERDE))
    rr(d, (x, y, x + w, y + h), 16, fill=(255, 255, 255), outline=borda, width=int((1 + 3 * realce) * S))
    ix, iy, isz = x + 22, y + (h - 54) / 2, 54
    if tipo == "email":
        rr(d, (ix, iy + 8, ix + isz, iy + isz - 8), 8, fill=(231, 248, 243), outline=VERDE_ESC, width=2 * S)
        d.line([((ix + 3) * S, (iy + 12) * S), ((ix + isz / 2) * S, (iy + isz / 2 + 4) * S), ((ix + isz - 3) * S, (iy + 12) * S)], fill=VERDE_ESC, width=int(2.5 * S))
    else:
        rr(d, (ix, iy + 2, ix + isz, iy + isz - 10), 16, fill=VERDE)
        d.polygon([((ix + 10) * S, (iy + isz - 12) * S), ((ix + 10) * S, (iy + isz + 2) * S), ((ix + 24) * S, (iy + isz - 12) * S)], fill=VERDE)
        for k in range(3):
            cxp = ix + isz / 2 + (k - 1) * 11
            d.ellipse([(cxp - 3.5) * S, (iy + 20) * S, (cxp + 3.5) * S, (iy + 27) * S], fill=(255, 255, 255))
    txt(d, x + 94, y + h / 2, rotulo, 700, 22, TXT, "lm")
    cola(d_img, lay, a)


def check(d_img, cx, cy, a=1.0):
    lay = camada()
    d = ImageDraw.Draw(lay)
    d.ellipse([(cx - 15) * S, (cy - 15) * S, (cx + 15) * S, (cy + 15) * S], fill=VERDE)
    d.line([((cx - 7) * S, cy * S), ((cx - 2) * S, (cy + 6) * S), ((cx + 8) * S, (cy - 6) * S)], fill=(255, 255, 255), width=int(3.5 * S))
    cola(d_img, lay, a)


def quadro(t):
    img = camada()
    img.alpha_composite(CARTAO)
    d = ImageDraw.Draw(img)
    txt(d, W / 2, CY0 + 52, TITULO, 800, 30, TXT, "ma")
    rr(d, (W / 2 - 34, CY0 + 96, W / 2 + 34, CY0 + 100), 2, fill=VERDE)
    # --- coluna esquerda: a folha do relatório, o botão e o arquivo
    a_folha = io((t - 0.0) / 0.4)
    enc = io((t - 1.35) / 0.5)            # a folha encolhe e vira o arquivo
    if enc < 1.0:
        folha(img, 76, 190, 188, 252, esc=(0.94 + 0.06 * a_folha) * (1 - 0.92 * enc), selo=enc > 0.4)
    if t < 2.0:
        rot = "Gerando PDF..." if 1.05 <= t < 1.45 else "Baixar PDF"
        pilula(img, 78, 468, 184, 46, rot, a=io((t - 0.35) / 0.3) * (1 - io((t - 1.8) / 0.3)), anel=max(0.0, min(1.0, (t - 0.95) / 0.5)) if 0.95 <= t < 1.45 else 0.0)
    # o arquivo: nasce na posição da folha, "viaja" para o meio (entre os dois canais) e depois sai uma cópia para cada canal
    if t >= 1.35:
        v = io((t - 2.3) / 0.9)
        ax, ay = 170 + (300 - 170) * v, 316 + (335 - 316) * v - 36 * math.sin(math.pi * v)
        arquivo(img, ax, ay, esc=0.85 + 0.15 * (1 - v) if t < 3.3 else 0.85, a=io((t - 1.35) / 0.35) * (1 - io((t - 4.1) / 0.35)),
                nome=t < 2.9, ok=1.9 < t < 2.9)
    # --- coluna da direita: os canais
    aco = io((t - 2.7) / 0.5)
    if aco > 0:
        dxs = 24 * (1 - aco)
        canal(img, 330 + dxs, 218, 250, 104, "email", "E-mail", a=aco, realce=jan(t, 4.4, 5.4, 0.25, 0.3))
        canal(img, 330 + dxs, 348, 250, 104, "whats", "WhatsApp", a=aco, realce=jan(t, 5.1, 6.3, 0.25, 0.3))
    for t0, (tx, ty) in ((4.3, (448, 270)), (5.0, (448, 400))):   # uma cópia voa para cada canal
        u = (t - t0) / 0.5
        if 0 < u < 1:
            u = io(u)
            arquivo(img, 300 + (tx - 300) * u, 335 + (ty - 335) * u - 30 * math.sin(math.pi * u), esc=0.46 * (1 - 0.25 * u), a=1 - 0.7 * u, nome=False)
    for t0, yy in ((4.8, 270), (5.5, 400)):   # a cópia chega: o "ok"
        if t >= t0:
            check(img, 560, yy - 38, a=io((t - t0) / 0.25))
    # --- legenda
    for a, b, tx in LEGENDAS:
        al = jan(t, a, b)
        if al > 0.003:
            lay = camada()
            ld = ImageDraw.Draw(lay)
            w = ui.font(700, 24 * S).getlength(tx) / S + 44
            rr(ld, (W / 2 - w / 2, CY0 + CH - 100, W / 2 + w / 2, CY0 + CH - 48), 26, fill=(30, 30, 30, 235))
            txt(ld, W / 2, CY0 + CH - 74, tx, 700, 24, (255, 255, 255), "mm")
            cola(img, lay, al)
    return img.resize((W, H), Image.LANCZOS)


if __name__ == "__main__":
    print("larguras (px):", confere())
    os.makedirs(OUT, exist_ok=True)
    if TESTE:
        for t in TESTE:
            quadro(t).save(os.path.join(OUT, f"teste_{t:05.2f}.png"))
        print("quadros de teste em", OUT)
    else:
        n = int(round(DUR * FPS))
        for i in range(n):
            quadro(i / FPS).save(os.path.join(OUT, f"{i:04d}.png"))
        print(f"{n} quadros ({DUR} s) em {OUT}")
