"""Ilustração do cap. 4 do T4 (plano T04: "efeito de Vinculado a equipamento na OS"): duas colunas, fundo branco,
"Ligado: escolhe o aparelho do cliente" x "Desligado: só o serviço". Motivo: a tela de Nova OS só entra no T5 e não vale
abri-la aqui. Desenho próprio e genérico (aparelho sem marca, serviços do mundo fictício), Montserrat, verde #00C597.
Sai como sequência PNG com alfa no tamanho da janela do app em repouso (1587x992, cantos de 16 px), para o editor
colocar em "illustrations" (box = janela, scale_in 0). Tempos em segundos locais, casados com a fala do cap. 4
(a ilustração entra em 35,0 s do capítulo; a fala "Na hora de abrir a ordem..." começa em 35,19 s):
  0,2 "Na hora de abrir a ordem"   1,9 "ligado"   2,5 "a Dominex pede o aparelho do cliente"
  5,1 "Desligado"   6,0 "pede só o serviço"
uso: python3 ilustra_vinculo.py <pasta_saida> [duração=8.0] [--teste t1,t2,...]  (--teste grava só esses quadros, em segundos)"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "kit"))
import ui  # noqa: E402

args = [a for a in sys.argv[1:] if not a.startswith("--")]
OUT = args[0]
DUR = float(args[1]) if len(args) > 1 else 8.0
TESTE = None
if "--teste" in sys.argv:
    TESTE = [float(x) for x in sys.argv[sys.argv.index("--teste") + 1].split(",")]
    OUT = args[0]
W, H, S, FPS = 1587, 992, 2, 30
VERDE = (0, 197, 151)
TXT = (24, 24, 27)
CINZA = (113, 113, 122)
CLARO = (244, 244, 245)
BORDA = (228, 228, 231)
TRILHA = (203, 203, 208)
MUDO = (156, 163, 175)

CW, CH = 660, 620            # cartão
CX = (112, 815)              # x dos cartões (esquerda = ligado, direita = desligado)
CY = 262
PAD = 44                     # folga em volta do cartão (sombra e anel)
INNER = 36                   # margem interna do cartão


def oc(t):
    t = min(1.0, max(0.0, t))
    return 1 - (1 - t) ** 3


def io(t):
    t = min(1.0, max(0.0, t))
    return t * t * (3 - 2 * t)


def janela(t, a, b, fi=0.3, fo=0.3):
    """0 -> 1 em a..a+fi, fica em 1 e volta a 0 em b-fo..b"""
    return io((t - a) / fi) * (1 - io((t - (b - fo)) / fo))


def f(w, px):
    return ui.font(w, int(px * S))


def tw(txt, w, px):
    """largura do texto em px de projeto"""
    return f(w, px).getlength(txt) / S


def rr(d, box, r, **kw):
    x0, y0, x1, y1 = box
    d.rounded_rectangle([x0 * S, y0 * S, x1 * S, y1 * S], radius=r * S, **kw)


def texto(d, x, y, s, w, px, fill):
    d.text((x * S, y * S), s, font=f(w, px), fill=fill)


def camada(w, h):
    return Image.new("RGBA", (int(w * S), int(h * S)), (0, 0, 0, 0))


def cola(dst, src, x, y, a=1.0):
    """cola src (RGBA) em dst na posição (x, y) de projeto, com opacidade extra a (0..1)"""
    if a <= 0.003:
        return
    if a < 0.999:
        al = src.getchannel("A").point(lambda v: int(v * a))
        src = src.copy()
        src.putalpha(al)
    dst.alpha_composite(src, (int(round(x * S)), int(round(y * S))))


def tracejado(d, box, r, cor, larg=3, traco=16, vao=11):
    """retângulo arredondado tracejado (projeto px)"""
    x0, y0, x1, y1 = box
    pts = []
    n = 14

    def arco(cx, cy, a0):
        for i in range(n + 1):
            a = np.radians(a0 + 90 * i / n)
            pts.append((cx + r * np.cos(a), cy + r * np.sin(a)))
    arco(x1 - r, y0 + r, -90)   # canto superior direito
    arco(x1 - r, y1 - r, 0)     # inferior direito
    arco(x0 + r, y1 - r, 90)    # inferior esquerdo
    arco(x0 + r, y0 + r, 180)   # superior esquerdo
    pts.append(pts[0])
    # amostra o contorno de 1 em 1 px e liga só os trechos "cheios" do tracejado
    acum = 0.0
    prev = pts[0]
    for (bx, by) in pts[1:]:
        ax, ay = prev
        seg = float(np.hypot(bx - ax, by - ay))
        passos = max(1, int(seg))
        for i in range(passos):
            p0 = (ax + (bx - ax) * i / passos, ay + (by - ay) * i / passos)
            p1 = (ax + (bx - ax) * (i + 1) / passos, ay + (by - ay) * (i + 1) / passos)
            if (acum + i * seg / passos) % (traco + vao) < traco:
                d.line([p0[0] * S, p0[1] * S, p1[0] * S, p1[1] * S], fill=cor, width=larg * S)
        acum += seg
        prev = (bx, by)


# ------------------------------------------------------------------ fundo (estático)
def fundo():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    g = np.exp(-(((xx - 470) / 560) ** 2 + ((yy - 400) / 400) ** 2))
    arr = np.full((H, W, 3), 255, np.float32)
    arr -= (np.array([255, 255, 255]) - np.array([231, 248, 243])) * (0.55 * g)[..., None]
    v = np.clip(((xx - W / 2) / (W * 0.7)) ** 2 + ((yy - H / 2) / (H * 0.8)) ** 2, 0, 1)
    arr -= 10 * v[..., None]
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).resize((W * S, H * S), Image.BICUBIC)
    return im.convert("RGBA")


BASE = fundo()

# ------------------------------------------------------------------ textos e medidas (conferidas antes de desenhar)
TITULO = "Ao abrir a ordem de serviço"
SUBTIT = "O interruptor Vinculado a equipamento muda o que ela pede"
LAB_VINC = "Vinculado a equipamento"
SERV = ("Manutenção Preventiva", "Visita Técnica")
COR_SERV = ((34, 197, 94), (107, 114, 128))
APAR = "Hi-Wall 18.000 BTUs"
LOCAL = "Sala dos professores"
CAP_A = ("Ligado:", " escolhe o aparelho do cliente")
CAP_B = ("Desligado:", " só o serviço")


def tam_legenda():
    """maior tamanho em que as duas legendas cabem no cartão com folga"""
    util = CW - 2 * INNER - 12
    for px in range(32, 17, -1):
        l = max(tw(a, 800, px) + tw(b, 600, px) for a, b in (CAP_A, CAP_B))
        if l <= util:
            return px
    raise SystemExit("legenda não cabe")


CAP_PX = tam_legenda()


def confere():
    util = CW - 2 * INNER
    linhas = [
        ("título", tw(TITULO, 800, 44), W - 160),
        ("subtítulo", tw(SUBTIT, 500, 26), W - 160),
        ("rótulo Vinculado", tw(LAB_VINC, 600, 23), 0),
        ("serviço A", tw(SERV[0], 600, 25) + 62, util),
        ("serviço B", tw(SERV[1], 600, 25) + 62, util),
        ("aparelho", tw(APAR, 700, 25) + 168, util),
        ("local", tw(LOCAL, 500, 21) + 168, util),
        ("legenda A", tw(CAP_A[0], 800, CAP_PX) + tw(CAP_A[1], 600, CAP_PX), util - 12),
        ("legenda B", tw(CAP_B[0], 800, CAP_PX) + tw(CAP_B[1], 600, CAP_PX), util - 12),
    ]
    for nome, larg, lim in linhas:
        if lim:
            assert larg <= lim, f"{nome}: {larg:.0f} > {lim}"
    # faixa do topo: interruptor + rótulo + selo "Desligado" sem encostar
    chip_w = tw("Desligado", 700, 21) + 40
    fim_rot = INNER + 84 + 20 + tw(LAB_VINC, 600, 23)
    ini_chip = CW - INNER - chip_w
    assert fim_rot + 20 <= ini_chip, f"faixa do topo: rótulo termina em {fim_rot:.0f}, selo começa em {ini_chip:.0f}"
    return {n: round(l) for n, l, _ in linhas} | {"legenda px": CAP_PX, "folga faixa": round(ini_chip - fim_rot)}


# ------------------------------------------------------------------ partes
def aparelho_icone(d, x, y):
    rr(d, (x, y, x + 100, y + 44), 14, fill=(252, 252, 252), outline=(200, 203, 210), width=2 * S)
    rr(d, (x + 12, y + 30, x + 88, y + 36), 3, fill=(214, 216, 222))
    d.ellipse([(x + 12) * S, (y + 9) * S, (x + 20) * S, (y + 17) * S], fill=VERDE)


def cartao_estatico(k):
    """sombra, corpo, faixa do topo e campo 'Serviço' do cartão k (camada com folga PAD)"""
    lay = camada(CW + 2 * PAD, CH + 2 * PAD)
    sh = camada(CW + 2 * PAD, CH + 2 * PAD)
    ds = ImageDraw.Draw(sh)
    rr(ds, (PAD + 6, PAD + 16, PAD + CW - 6, PAD + CH + 14), 30, fill=(0, 40, 30, 52))
    sh = sh.filter(ImageFilter.GaussianBlur(18 * S))
    lay.alpha_composite(sh)
    d = ImageDraw.Draw(lay)
    o = PAD
    rr(d, (o, o, o + CW, o + CH), 28, fill=(255, 255, 255), outline=BORDA, width=2 * S)
    # faixa do topo (cantos de cima arredondados)
    d.rounded_rectangle([(o + 2) * S, (o + 2) * S, (o + CW - 2) * S, (o + 96) * S], radius=26 * S, fill=CLARO)
    d.rectangle([(o + 2) * S, (o + 60) * S, (o + CW - 2) * S, (o + 96) * S], fill=CLARO)
    d.line([(o + 2) * S, (o + 96) * S, (o + CW - 2) * S, (o + 96) * S], fill=BORDA, width=2 * S)
    texto(d, o + INNER + 84 + 20, o + 48 - 17, LAB_VINC, 600, 23, TXT)
    # campo Serviço
    texto(d, o + INNER, o + 124, "Serviço", 500, 21, CINZA)
    rr(d, (o + INNER, o + 156, o + CW - INNER, o + 224), 16, fill=(255, 255, 255), outline=BORDA, width=2 * S)
    cx, cy = o + INNER + 30, o + 190
    d.ellipse([(cx - 10) * S, (cy - 10) * S, (cx + 10) * S, (cy + 10) * S], fill=COR_SERV[k])
    texto(d, o + INNER + 54, o + 190 - 18, SERV[k], 600, 25, TXT)
    # divisória da legenda
    d.line([(o + INNER) * S, (o + 448) * S, (o + CW - INNER) * S, (o + 448) * S], fill=BORDA, width=2 * S)
    return lay


def interruptor(p):
    """interruptor 84x48 com a bolinha em p (0 = desligado, 1 = ligado); camada local"""
    lay = camada(84, 48)
    d = ImageDraw.Draw(lay)
    cor = tuple(int(TRILHA[i] + (VERDE[i] - TRILHA[i]) * p) for i in range(3))
    rr(d, (0, 0, 84, 48), 24, fill=cor)
    x = 4 + 36 * p
    d.ellipse([(x + 1) * S, 5 * S, (x + 39) * S, 43 * S + 0], fill=(255, 255, 255))
    return lay


def selo(txt, ligado):
    larg = tw(txt, 700, 21) + 40
    lay = camada(larg + 2, 42)
    d = ImageDraw.Draw(lay)
    if ligado:
        rr(d, (0, 0, larg, 40), 20, fill=VERDE)
        texto(d, 20, 8, txt, 700, 21, (255, 255, 255))
    else:
        rr(d, (0, 0, larg, 40), 20, fill=(229, 231, 235))
        texto(d, 20, 8, txt, 700, 21, (63, 63, 70))
    return lay, larg


def linha_aparelho(destaque):
    """rótulo + campo do aparelho do cliente (cartão da esquerda); camada local"""
    lay = camada(CW - 2 * INNER, 140)
    d = ImageDraw.Draw(lay)
    texto(d, 0, 0, "Aparelho do cliente", 500, 21, CINZA)
    borda = VERDE if destaque > 0.01 else BORDA
    larg = 3 if destaque > 0.01 else 2
    rr(d, (0, 32, CW - 2 * INNER, 140), 16, fill=(255, 255, 255), outline=borda, width=larg * S)
    aparelho_icone(d, 24, 32 + (108 - 44) / 2)
    texto(d, 148, 32 + 24, APAR, 700, 25, TXT)
    texto(d, 148, 32 + 62, LOCAL, 500, 21, CINZA)
    if destaque > 0.01:
        g = camada(CW - 2 * INNER, 140)
        dg = ImageDraw.Draw(g)
        rr(dg, (-2, 30, CW - 2 * INNER + 2, 142), 18, outline=VERDE + (int(120 * destaque),), width=6 * S)
        g = g.filter(ImageFilter.GaussianBlur(5 * S))
        g.alpha_composite(lay)
        lay = g
    return lay


def slot_vazio():
    """rótulo apagado + campo tracejado 'Sem aparelho' (cartão da direita); camada local"""
    lay = camada(CW - 2 * INNER, 140)
    d = ImageDraw.Draw(lay)
    texto(d, 0, 0, "Aparelho do cliente", 500, 21, (196, 196, 204))
    tracejado(d, (1, 33, CW - 2 * INNER - 1, 139), 16, (209, 213, 219))
    msg = "Sem aparelho"
    l = tw(msg, 500, 24)
    texto(d, (CW - 2 * INNER - l) / 2, 32 + 54 - 15, msg, 500, 24, MUDO)
    return lay


def legenda(k):
    """'Ligado: escolhe o aparelho do cliente' / 'Desligado: só o serviço' centrada no cartão; camada local"""
    a, b = (CAP_A, CAP_B)[k]
    cor = (VERDE, (82, 82, 91))[k]
    l1, l2 = tw(a, 800, CAP_PX), tw(b, 600, CAP_PX)
    larg = CW - 2 * INNER
    lay = camada(larg, 60)
    d = ImageDraw.Draw(lay)
    x = (larg - (l1 + l2)) / 2
    texto(d, x, 8, a, 800, CAP_PX, cor)
    texto(d, x + l1, 8, b, 600, CAP_PX, TXT)
    return lay


def anel(emb):
    lay = camada(CW + 2 * PAD, CH + 2 * PAD)
    d = ImageDraw.Draw(lay)
    o = PAD
    rr(d, (o - 6, o - 6, o + CW + 6, o + CH + 6), 33, outline=VERDE + (int(110 * emb),), width=6 * S)
    lay = lay.filter(ImageFilter.GaussianBlur(6 * S))
    d2 = ImageDraw.Draw(lay)
    rr(d2, (o - 5, o - 5, o + CW + 5, o + CH + 5), 33, outline=VERDE + (int(255 * emb),), width=3 * S)
    return lay


ESTATICO = [cartao_estatico(0), cartao_estatico(1)]
TITULO_LAY = None


def titulo_layer():
    lay = camada(W, 150)
    d = ImageDraw.Draw(lay)
    l1 = tw(TITULO, 800, 44)
    texto(d, (W - l1) / 2, 0, TITULO, 800, 44, TXT)
    l2 = tw(SUBTIT, 500, 26)
    texto(d, (W - l2) / 2, 72, SUBTIT, 500, 26, CINZA)
    # barra verde curta embaixo do título (assinatura da marca)
    rr(d, (W / 2 - 36, 128, W / 2 + 36, 134), 3, fill=VERDE)
    return lay


TITULO_LAY = titulo_layer()


def cartao(k, tau, alfa, emb, dy):
    lay = ESTATICO[k].copy()
    o = PAD
    # faixa do topo: interruptor e selo
    if k == 0:
        p = io((tau - 1.75) / 0.3)
        sel_a = io((tau - 1.95) / 0.3)
    else:
        p = 0.0
        sel_a = io((tau - 5.05) / 0.3)
    cola(lay, interruptor(p), o + INNER, o + 24)
    sl, sw = selo(("Ligado", "Desligado")[k], k == 0)
    cola(lay, sl, o + CW - INNER - sw, o + 28, sel_a)
    # aparelho do cliente / campo vazio
    if k == 0:
        a = oc((tau - 2.5) / 0.5)
        dest = janela(tau, 3.1, 4.9, 0.3, 0.3)
        cola(lay, linha_aparelho(dest), o + INNER, o + 258 + 14 * (1 - a), a)
        ca = oc((tau - 3.1) / 0.45)
    else:
        a = oc((tau - 5.85) / 0.45)
        cola(lay, slot_vazio(), o + INNER, o + 258 + 14 * (1 - a), a)
        ca = oc((tau - 6.05) / 0.45)
    cola(lay, legenda(k), o + INNER, o + 448 + 62 + 12 * (1 - ca), ca)
    if emb > 0.01:
        lay.alpha_composite(anel(emb))
    # entrada + esmaecer quando o outro cartão fala
    if alfa < 0.999:
        al = lay.getchannel("A").point(lambda v: int(v * alfa))
        lay.putalpha(al)
    return lay, CX[k] - PAD, CY - PAD + dy


def quadro(tau):
    im = BASE.copy()
    ta = oc((tau - 0.15) / 0.45)
    cola(im, TITULO_LAY, 0, 96 + 14 * (1 - ta), ta)
    ent = oc((tau - 0.45) / 0.5)
    embL = janela(tau, 1.6, 4.9, 0.3, 0.3)
    embR = janela(tau, 4.9, 7.4, 0.3, 0.4)
    alL = ent * (1 - 0.5 * embR)
    alR = ent * (1 - 0.5 * embL)
    for k, (al, emb) in enumerate(((alL, embL), (alR, embR))):
        if ent <= 0.003:
            continue
        lay, x, y = cartao(k, tau, al, emb, 26 * (1 - ent))
        cola(im, lay, x, y)
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
