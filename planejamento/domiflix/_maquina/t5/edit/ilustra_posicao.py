"""Ilustração do cap. 16 do T5 ("Onde está cada técnico"): o celular do técnico envia a posição e ela aparece no Mapa ao Vivo.
Fundo branco, Montserrat, verde #00C597, objetos genéricos (celular e mapa sem marca, sem dado real).
Sai como sequência PNG com alfa no tamanho da janela do app em repouso (1587x992, cantos de 16 px), para o editor colocar
em "illustrations" (box = janela, scale_in 0). Tempos em segundos locais (a ilustração entra em 2,4 s do capítulo), casados
com a fala do cap. 16 (tempo do capítulo - 2,4):
  0,2 "A posição vem do celular dele"   2,4 "o app envia durante o atendimento"   4,7 "e ela aparece aqui no mapa"
  6,4 "É só pedir pro técnico liberar a localização"   9,9 "na primeira vez"   10,8 "é ela que coloca o ponto dele no mapa"
uso: python3 ilustra_posicao.py <pasta_saida> [duração=13.2] [--teste t1,t2,...]  (--teste grava só esses quadros, em segundos)"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "kit"))
import ui  # noqa: E402

args = [a for a in sys.argv[1:] if not a.startswith("--")]
OUT = args[0]
DUR = float(args[1]) if len(args) > 1 else 13.2
TESTE = None
if "--teste" in sys.argv:
    TESTE = [float(x) for x in sys.argv[sys.argv.index("--teste") + 1].split(",")]
W, H, S, FPS = 1587, 992, 2, 30
VERDE = (0, 197, 151)
VERDE_ESC = (0, 150, 115)
TXT = (24, 24, 27)
CINZA = (113, 113, 122)
CLARO = (244, 244, 245)
BORDA = (228, 228, 231)

PH = (150, 292, 300, 600)       # celular: x, y, largura, altura
MP = (770, 292, 680, 600)       # cartão do mapa
PAD = 40


def oc(t):
    t = min(1.0, max(0.0, t))
    return 1 - (1 - t) ** 3


def io(t):
    t = min(1.0, max(0.0, t))
    return t * t * (3 - 2 * t)


def janela(t, a, b, fi=0.3, fo=0.3):
    return io((t - a) / fi) * (1 - io((t - (b - fo)) / fo))


def f(w, px):
    return ui.font(w, int(px * S))


def tw(txt, w, px):
    return f(w, px).getlength(txt) / S


def rr(d, box, r, **kw):
    x0, y0, x1, y1 = box
    d.rounded_rectangle([x0 * S, y0 * S, x1 * S, y1 * S], radius=r * S, **kw)


def texto(d, x, y, s, w, px, fill):
    d.text((x * S, y * S), s, font=f(w, px), fill=fill)


def camada(w, h):
    return Image.new("RGBA", (int(w * S), int(h * S)), (0, 0, 0, 0))


def cola(dst, src, x, y, a=1.0):
    if a <= 0.003:
        return
    if a < 0.999:
        al = src.getchannel("A").point(lambda v: int(v * a))
        src = src.copy()
        src.putalpha(al)
    dst.alpha_composite(src, (int(round(x * S)), int(round(y * S))))


def sombra(w, h, r, dy=14, blur=18, alfa=50):
    lay = camada(w + 2 * PAD, h + 2 * PAD)
    d = ImageDraw.Draw(lay)
    rr(d, (PAD + 6, PAD + dy, PAD + w - 6, PAD + h + dy - 2), r, fill=(0, 40, 30, alfa))
    return lay.filter(ImageFilter.GaussianBlur(blur * S))


# ------------------------------------------------------------------ fundo (estático)
def fundo():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    g = np.exp(-(((xx - 800) / 700) ** 2 + ((yy - 560) / 420) ** 2))
    arr = np.full((H, W, 3), 255, np.float32)
    arr -= (np.array([255, 255, 255]) - np.array([231, 248, 243])) * (0.5 * g)[..., None]
    v = np.clip(((xx - W / 2) / (W * 0.7)) ** 2 + ((yy - H / 2) / (H * 0.8)) ** 2, 0, 1)
    arr -= 10 * v[..., None]
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).resize((W * S, H * S), Image.BICUBIC)
    return im.convert("RGBA")


BASE = fundo()

TITULO = "Do celular do técnico ao mapa"
SUBTIT = "A posição chega pelo aplicativo, durante o atendimento"
LEGENDAS = [  # (início, fim, texto)
    (0.5, 2.5, "O aplicativo no celular do técnico"),
    (2.6, 4.7, "Envia a posição durante o atendimento"),
    (4.8, 6.9, "E ela aparece no Mapa ao Vivo"),
    (7.0, 10.6, "Na primeira vez, o técnico libera a localização"),
    (10.8, 13.0, "É a localização que coloca o ponto no mapa"),
]
SENT = "posição enviada"


def confere():
    linhas = [("título", tw(TITULO, 800, 44), W - 160), ("subtítulo", tw(SUBTIT, 500, 26), W - 160),
              ("posição enviada", tw(SENT, 600, 21) + 36, 280)]
    for i, (_, _, t) in enumerate(LEGENDAS):
        linhas.append((f"legenda {i + 1}", tw(t, 700, 32), W - 200))
    for nome, larg, lim in linhas:
        assert larg <= lim, f"{nome}: {larg:.0f} > {lim}"
    return {n: round(l) for n, l, _ in linhas}


# ------------------------------------------------------------------ celular
def celular_corpo():
    x, y, w, h = PH
    lay = camada(w + 2 * PAD, h + 2 * PAD)
    lay.alpha_composite(sombra(w, h, 44))
    d = ImageDraw.Draw(lay)
    o = PAD
    rr(d, (o, o, o + w, o + h), 44, fill=(28, 28, 33))
    rr(d, (o + 12, o + 12, o + w - 12, o + h - 12), 34, fill=(255, 255, 255))
    rr(d, (o + w / 2 - 44, o + 20, o + w / 2 + 44, o + 38), 9, fill=(28, 28, 33))  # ilha da câmera
    return lay


CORPO = celular_corpo()


def pino(cx, cy, r, cor=VERDE, borda=(255, 255, 255)):
    """marcador em gota (ponta em baixo) como camada com folga; devolve (camada, ox, oy) da ponta"""
    lay = camada(r * 4, r * 5)
    d = ImageDraw.Draw(lay)
    x0, y0 = r * 2, r * 2
    pts = [(x0 - r * 0.86, y0 + r * 0.5), (x0, y0 + r * 2.15), (x0 + r * 0.86, y0 + r * 0.5)]
    d.polygon([(px * S, py * S) for px, py in pts], fill=cor)
    d.ellipse([(x0 - r) * S, (y0 - r) * S, (x0 + r) * S, (y0 + r) * S], fill=cor)
    d.ellipse([(x0 - r * 0.42) * S, (y0 - r * 0.42) * S, (x0 + r * 0.42) * S, (y0 + r * 0.42) * S], fill=borda)
    return lay, x0, y0 + r * 2.15


def tela_celular(tau):
    """conteúdo da tela (276x576) do celular"""
    sw, sh = PH[2] - 24, PH[3] - 24
    lay = camada(sw, sh)
    d = ImageDraw.Draw(lay)
    texto(d, 22, 20, "09:41", 700, 15, TXT)
    for i in range(3):
        rr(d, (sw - 64 + i * 14, 24 - i * 3, sw - 56 + i * 14, 34), 2, fill=(82, 82, 91))
    texto(d, 22, 74, "Atendimento", 800, 24, TXT)
    chip = "Em andamento"
    cw = tw(chip, 700, 14) + 24
    rr(d, (22, 112, 22 + cw, 138), 13, fill=(220, 252, 231))
    texto(d, 34, 117, chip, 700, 14, (21, 128, 61))
    # cartão da visita
    rr(d, (22, 160, sw - 22, 292), 18, fill=CLARO, outline=BORDA, width=2 * S)
    texto(d, 40, 176, "Visita técnica", 700, 18, TXT)
    texto(d, 40, 204, "Cliente do dia", 500, 15, CINZA)
    rr(d, (40, 238, sw - 40, 262), 12, fill=(229, 231, 235))
    rr(d, (40, 238, 40 + (sw - 80) * 0.55, 262), 12, fill=VERDE)
    texto(d, 40, 268, "Check-in feito", 600, 13, CINZA)
    # localização ativa (depois do toque em "Permitir")
    a = io((tau - 10.55) / 0.35)
    if a > 0.003:
        ch = camada(sw - 44, 54)
        dc = ImageDraw.Draw(ch)
        rr(dc, (0, 0, sw - 44, 54), 16, fill=(232, 250, 244), outline=VERDE, width=2 * S)
        dc.ellipse([18 * S, 19 * S, 34 * S, 35 * S], fill=VERDE)
        texto(dc, 46, 15, "Localização ativa", 700, 17, VERDE_ESC)
        cola(lay, ch, 22, 318 + 10 * (1 - a), a)
    # folha "Permitir localização?"
    p = oc((tau - 7.0) / 0.45) * (1 - io((tau - 10.15) / 0.35))
    if p > 0.003:
        fl = camada(sw, 250)
        dl = ImageDraw.Draw(fl)
        rr(dl, (10, 0, sw - 10, 250), 26, fill=(255, 255, 255), outline=BORDA, width=2 * S)
        texto(dl, 32, 26, "Permitir a localização?", 800, 18, TXT)
        texto(dl, 32, 58, "Assim a posição aparece", 500, 15, CINZA)
        texto(dl, 32, 80, "no mapa da empresa.", 500, 15, CINZA)
        press = janela(tau, 9.55, 9.95, 0.12, 0.2)
        bw = sw - 64
        rr(dl, (32, 124 - 2 * press, 32 + bw, 178 - 2 * press), 16, fill=VERDE_ESC if press > 0.5 else VERDE)
        t1 = "Permitir"
        texto(dl, 32 + (bw - tw(t1, 700, 19)) / 2, 138, t1, 700, 19, (255, 255, 255))
        rr(dl, (32, 190, 32 + bw, 232), 16, fill=(244, 244, 245))
        t2 = "Agora não"
        texto(dl, 32 + (bw - tw(t2, 600, 17)) / 2, 200, t2, 600, 17, (82, 82, 91))
        cola(lay, fl, 0, sh - 250 * p - 8 + 0, p)
    return lay


def celular(tau, alfa, dy):
    lay = CORPO.copy()
    cola(lay, tela_celular(tau), PAD + 12, PAD + 12)
    # corta o conteúdo no arredondado da tela (máscara)
    return lay, PH[0] - PAD, PH[1] - PAD + dy, alfa


# ------------------------------------------------------------------ mapa
def mapa_estatico():
    x, y, w, h = MP
    lay = camada(w + 2 * PAD, h + 2 * PAD)
    lay.alpha_composite(sombra(w, h, 28))
    d = ImageDraw.Draw(lay)
    o = PAD
    rr(d, (o, o, o + w, o + h), 28, fill=(255, 255, 255), outline=BORDA, width=2 * S)
    # faixa do topo
    d.rounded_rectangle([(o + 2) * S, (o + 2) * S, (o + w - 2) * S, (o + 86) * S], radius=26 * S, fill=CLARO)
    d.rectangle([(o + 2) * S, (o + 56) * S, (o + w - 2) * S, (o + 86) * S], fill=CLARO)
    d.line([(o + 2) * S, (o + 86) * S, (o + w - 2) * S, (o + 86) * S], fill=BORDA, width=2 * S)
    texto(d, o + 34, o + 24, "Mapa ao Vivo", 700, 26, TXT)
    # área do mapa
    mx0, my0, mx1, my1 = o + 24, o + 108, o + w - 24, o + h - 24
    mapa = camada(mx1 - mx0, my1 - my0)
    dm = ImageDraw.Draw(mapa)
    mw, mh = mx1 - mx0, my1 - my0
    rr(dm, (0, 0, mw, mh), 18, fill=(238, 244, 240))
    # quarteirões
    cols = [0, 170, 360, 520, mw]
    lins = [0, 150, 300, mh]
    cores = [(226, 236, 229), (232, 240, 233), (222, 233, 226)]
    k = 0
    for i in range(len(cols) - 1):
        for j in range(len(lins) - 1):
            rr(dm, (cols[i] + 12, lins[j] + 12, cols[i + 1] - 12, lins[j + 1] - 12), 10, fill=cores[k % 3])
            k += 1
    # rio (faixa inclinada): máscara própria multiplicada pelo arredondado do mapa
    ma = Image.new("L", mapa.size, 0)
    ImageDraw.Draw(ma).rounded_rectangle([0, 0, mw * S, mh * S], radius=18 * S, fill=255)
    rm = Image.new("L", mapa.size, 0)
    ImageDraw.Draw(rm).polygon([(mw * 0.62 * S, 0), (mw * 0.76 * S, 0), (mw * 0.40 * S, mh * S), (mw * 0.26 * S, mh * S)], fill=230)
    rm = Image.fromarray((np.array(rm, np.float32) * np.array(ma, np.float32) / 255).astype(np.uint8))
    rio = Image.new("RGBA", mapa.size, (205, 228, 241, 0))
    rio.putalpha(rm)
    mapa.alpha_composite(rio)
    dm = ImageDraw.Draw(mapa)
    # ruas
    for cx in cols[1:-1]:
        dm.line([cx * S, 0, cx * S, mh * S], fill=(255, 255, 255), width=14 * S)
    for ly in lins[1:-1]:
        dm.line([0, ly * S, mw * S, ly * S], fill=(255, 255, 255), width=14 * S)
    mapa.putalpha(ma)
    lay.alpha_composite(mapa, (int(mx0 * S), int(my0 * S)))
    return lay, (mx0, my0, mw, mh)


MAPA, MAPA_BOX = mapa_estatico()
PINO_XY = (MP[0] + 410, MP[1] + 108 + 290)        # ponta do marcador, em coordenadas do quadro
PIN, PIN_OX, PIN_OY = pino(0, 0, 26)


def sinal(tau, alfa):
    """linha pontilhada celular -> mapa, com pontos que viajam e o selo 'posição enviada'"""
    x0 = PH[0] + PH[2] + 10
    x1 = MP[0] - 14
    yc = PH[1] + 300
    lay = camada(W, H)
    d = ImageDraw.Draw(lay)
    cor = VERDE + (int(255 * alfa),)
    n = 14
    for i in range(n):
        xa = x0 + (x1 - x0) * i / n
        xb = xa + (x1 - x0) / n * 0.55
        d.line([xa * S, yc * S, xb * S, yc * S], fill=VERDE + (int(120 * alfa),), width=5 * S)
    # pontos viajando (um a cada 0,9 s)
    for k in range(4):
        u = ((tau - 2.5) / 1.8 + k * 0.25) % 1.0
        if (2.5 <= tau <= 6.4) or (10.8 <= tau <= 12.9):
            xx = x0 + (x1 - x0) * u
            r = 9
            a = alfa * math_sin(u)
            d.ellipse([(xx - r) * S, (yc - r) * S, (xx + r) * S, (yc + r) * S], fill=VERDE + (int(255 * a),))
    # seta na ponta
    d.polygon([((x1 + 4) * S, yc * S), ((x1 - 18) * S, (yc - 14) * S), ((x1 - 18) * S, (yc + 14) * S)], fill=cor)
    # selo
    sw_ = tw(SENT, 600, 21) + 36
    sa = io((tau - 2.7) / 0.3) * alfa
    if sa > 0.003:
        rr(d, ((x0 + x1) / 2 - sw_ / 2, yc - 74, (x0 + x1) / 2 + sw_ / 2, yc - 36), 19, fill=(232, 250, 244, int(255 * sa)))
        d.text((((x0 + x1) / 2 - sw_ / 2 + 18) * S, (yc - 68) * S), SENT, font=f(600, 21), fill=VERDE_ESC + (int(255 * sa),))
    return lay


def math_sin(u):
    return float(np.sin(np.pi * u))


def pulso(tau, alfa):
    """anel que se expande em volta do marcador (quando a posição chega)"""
    lay = camada(W, H)
    d = ImageDraw.Draw(lay)
    cx, cy = PINO_XY
    for t0 in (5.9, 11.7):
        u = (tau - t0) / 1.3
        if 0 <= u <= 1:
            r = 22 + 70 * oc(u)
            a = (1 - u) * 0.8 * alfa
            d.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S], outline=VERDE + (int(255 * a),), width=5 * S)
    return lay


def legenda(tau):
    for (a, b, t) in LEGENDAS:
        v = janela(tau, a, b, 0.3, 0.3)
        if v > 0.003:
            larg = tw(t, 700, 32)
            lay = camada(larg + 60, 70)
            d = ImageDraw.Draw(lay)
            rr(d, (0, 0, larg + 60, 62), 31, fill=(255, 255, 255, 235), outline=BORDA + (255,), width=2 * S)
            d.ellipse([22 * S, 24 * S, 36 * S, 38 * S], fill=VERDE)
            texto(d, 46, 12, t, 700, 32, TXT)
            return lay, (W - (larg + 60)) / 2, 898 + 10 * (1 - v), v
    return None


def titulo_layer():
    lay = camada(W, 150)
    d = ImageDraw.Draw(lay)
    l1 = tw(TITULO, 800, 44)
    texto(d, (W - l1) / 2, 0, TITULO, 800, 44, TXT)
    l2 = tw(SUBTIT, 500, 26)
    texto(d, (W - l2) / 2, 72, SUBTIT, 500, 26, CINZA)
    rr(d, (W / 2 - 36, 128, W / 2 + 36, 134), 3, fill=VERDE)
    return lay


TITULO_LAY = titulo_layer()


def quadro(tau):
    im = BASE.copy()
    ta = oc((tau - 0.1) / 0.45) * (1 - io((tau - 12.7) / 0.5))
    cola(im, TITULO_LAY, 0, 70 + 14 * (1 - ta), ta)
    sai = 1 - io((tau - 12.8) / 0.4)
    # celular
    ent_c = oc((tau - 0.25) / 0.55)
    if ent_c > 0.003:
        lay, x, y, a = celular(tau, ent_c, 24 * (1 - ent_c))
        cola(im, lay, x, y, ent_c * sai)
    # linha de sinal
    sa = io((tau - 2.4) / 0.4) * sai
    if sa > 0.003:
        cola(im, sinal(tau, sa), 0, 0)
    # mapa
    ent_m = oc((tau - 4.4) / 0.55)
    if ent_m > 0.003:
        cola(im, MAPA, MP[0] - PAD, MP[1] - PAD + 24 * (1 - ent_m), ent_m * sai)
        cola(im, pulso(tau, sai), 0, 0)
        # marcador (cai do alto em 5,7 s); o anel de pulso fica por baixo do marcador e do selo
        u = oc((tau - 5.7) / 0.45)
        if u > 0.003:
            cx, cy = PINO_XY
            drop = (1 - u) * 60
            cola(im, PIN, cx - PIN_OX, cy - PIN_OY - drop, u * sai)
            lab = "Técnico"
            lw = tw(lab, 700, 20) + 32
            sl = camada(lw, 40)
            ds = ImageDraw.Draw(sl)
            rr(ds, (0, 0, lw, 38), 19, fill=(255, 255, 255), outline=BORDA, width=2 * S)
            texto(ds, 16, 7, lab, 700, 20, TXT)
            cola(im, sl, cx - lw / 2, cy + 14, io((tau - 6.1) / 0.3) * sai)
    lg = legenda(tau)
    if lg:
        lay, x, y, a = lg
        cola(im, lay, x, y, a)
    return im.resize((W, H), Image.LANCZOS)


def mascara():
    a, _ = ui.rrect_alpha(W, H, 0, 0, W, H, 16)
    return (a * 255).astype(np.uint8)


if __name__ == "__main__":
    print("medidas (px de projeto):", confere())
    os.makedirs(OUT, exist_ok=True)
    m = mascara()
    if TESTE:
        for t in TESTE:
            fr = np.array(quadro(t).convert("RGB"))
            Image.fromarray(np.dstack([fr, m]), "RGBA").save(os.path.join(OUT, f"teste_{t:05.2f}.png"))
        print("ok", OUT, len(TESTE), "quadros de teste")
        sys.exit(0)
    n = int(round(DUR * FPS))
    for i in range(n):
        tau = i / FPS
        fr = np.array(quadro(tau).convert("RGB"))
        Image.fromarray(np.dstack([fr, m]), "RGBA").save(os.path.join(OUT, f"{i:04d}.png"), optimize=False, compress_level=1)
        if i % 30 == 0:
            print(f"{i}/{n}", flush=True)
    print("ok", OUT, n, "quadros")
