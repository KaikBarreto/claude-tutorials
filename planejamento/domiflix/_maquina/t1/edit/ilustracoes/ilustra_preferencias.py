"""Ilustração do cap. 8 do T1 (roteiro, linha 5): "cada preferência vale pra quem deve". A tela vira um fundo branco com três
cartões (Da empresa, Deste aparelho, Só sua), cada um com um exemplo real da aba Usabilidade (Consumo de estoque na OS,
Tabelas Compactas, Incluir compras no cartão); depois volta ao sistema. Desenho próprio e genérico, Montserrat, verde #00C597.
Sai como sequência PNG com alfa no tamanho da janela do app em repouso (1587x992, cantos de 16 px), para o editor
colocar em "illustrations" (box = janela, scale_in 0). Tempos em segundos locais (0 = "Uma coisa importante"), casados com a fala:
  1,5 "cada preferência vale pra quem deve"   4,1 "O consumo de estoque vale pra empresa inteira"
  6,8 "A maioria dos outros interruptores vale só neste aparelho"   10,8 "E algumas são só suas, em qualquer aparelho"
Todo texto é medido com getlength antes de desenhar e termina pelo menos 12 px antes da borda do cartão (docs/05-edicao.md).
uso: python3 ilustra_preferencias.py <pasta_saida> [duração=13.9]   |   --teste <pasta> t1 t2 ...  (só quadros soltos)"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = HERE
while KIT != "/" and not os.path.exists(os.path.join(KIT, "kit", "ui.py")):
    KIT = os.path.dirname(KIT)
sys.path.insert(0, os.path.join(KIT, "kit"))
import ui  # noqa: E402

W, H, S, FPS = 1587, 992, 2, 30
VERDE = (0, 197, 151)
TXT = (24, 24, 27)
CINZA = (113, 113, 122)
LINHA = (228, 228, 231)
MARGEM_TXT = 12  # o texto termina pelo menos 12 px antes da borda do cartão

CARTOES = [
    dict(titulo="Da empresa", sub="Vale para a empresa inteira", exemplo="Consumo de estoque na OS", icone="empresa", t0=4.0, t1=6.75),
    dict(titulo="Deste aparelho", sub="Vale só neste aparelho", exemplo="Tabelas Compactas", icone="aparelho", t0=6.8, t1=10.65),
    dict(titulo="Só sua", sub="Em qualquer aparelho", exemplo="Incluir compras no cartão", icone="pessoa", t0=10.7, t1=99.0),
]
CW, CH, GAP = 441, 530, 36
CX0 = (W - (3 * CW + 2 * GAP)) / 2
CY0 = 286


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


def larg(texto, fonte):
    return fonte.getlength(texto) / S


def quebra(texto, fonte, maxw):
    """quebra em até 2 linhas que cabem em maxw (px do quadro); erro se não couber (nada de texto passando da borda)"""
    if larg(texto, fonte) <= maxw:
        return [texto]
    palavras = texto.split()
    opcoes = []
    for k in range(1, len(palavras)):
        a, b = " ".join(palavras[:k]), " ".join(palavras[k:])
        if larg(a, fonte) <= maxw and larg(b, fonte) <= maxw:
            opcoes.append((abs(larg(a, fonte) - larg(b, fonte)), [a, b]))
    if opcoes:
        return min(opcoes, key=lambda o: o[0])[1]  # a quebra mais equilibrada
    raise SystemExit(f"texto não cabe em {maxw}px: {texto!r}")


def centro(d, cx, y, texto, fonte, fill):
    w = larg(texto, fonte)
    assert w <= CW - 2 * MARGEM_TXT, (texto, w)
    d.text(((cx - w / 2) * S, y * S), texto, font=fonte, fill=fill)


def fundo():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    g = np.exp(-(((xx - W * 0.5) / 700) ** 2 + ((yy - 420) / 420) ** 2))
    arr = np.full((H, W, 3), 255, np.float32)
    arr -= (np.array([255, 255, 255]) - np.array([231, 248, 243])) * (0.55 * g)[..., None]
    v = np.clip(((xx - W / 2) / (W * 0.7)) ** 2 + ((yy - H / 2) / (H * 0.8)) ** 2, 0, 1)
    arr -= 10 * v[..., None]
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).resize((W * S, H * S), Image.BICUBIC)
    return im.convert("RGBA")


BASE = fundo()


def icone(d, kind, cx, cy, r):
    """glifos genéricos brancos dentro do círculo verde"""
    br = (255, 255, 255)
    if kind == "empresa":  # prédio com janelas
        d.rounded_rectangle([(cx - 20) * S, (cy - 26) * S, (cx + 20) * S, (cy + 26) * S], radius=4 * S, fill=br)
        for i in range(3):
            for j in range(2):
                x = cx - 11 + j * 14
                y = cy - 18 + i * 14
                d.rectangle([x * S, y * S, (x + 7) * S, (y + 7) * S], fill=VERDE)
        d.rectangle([(cx - 5) * S, (cy + 14) * S, (cx + 5) * S, (cy + 26) * S], fill=VERDE)
    elif kind == "aparelho":  # monitor
        d.rounded_rectangle([(cx - 28) * S, (cy - 22) * S, (cx + 28) * S, (cy + 12) * S], radius=5 * S, fill=br)
        d.rectangle([(cx - 23) * S, (cy - 17) * S, (cx + 23) * S, (cy + 7) * S], fill=VERDE)
        d.rectangle([(cx - 4) * S, (cy + 12) * S, (cx + 4) * S, (cy + 22) * S], fill=br)
        d.rounded_rectangle([(cx - 16) * S, (cy + 20) * S, (cx + 16) * S, (cy + 26) * S], radius=3 * S, fill=br)
    else:  # pessoa
        d.ellipse([(cx - 11) * S, (cy - 26) * S, (cx + 11) * S, (cy - 4) * S], fill=br)
        d.pieslice([(cx - 26) * S, (cy + 2) * S, (cx + 26) * S, (cy + 54) * S], 180, 360, fill=br)


def cartao(c, idx, tau):
    """camada RGBA (tamanho do quadro) com um cartão no estado do instante tau"""
    lay = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    ent = oc((tau - (3.2 + 0.18 * idx)) / 0.55)
    if ent <= 0:
        return lay
    x0 = CX0 + idx * (CW + GAP)
    y0 = CY0 + 26 * (1 - ent)
    x1, y1 = x0 + CW, y0 + CH
    ativo = io((tau - c["t0"]) / 0.35) * (1 - io((tau - c["t1"]) / 0.35))
    d = ImageDraw.Draw(lay)
    # sombra
    sh = Image.new("RGBA", lay.size, (0, 0, 0, 0))
    ds = ImageDraw.Draw(sh)
    rr(ds, (x0 + 6, y0 + 16, x1 - 6, y1 + 16), 30, fill=(0, 40, 30, int(46 + 30 * ativo)))
    lay.alpha_composite(sh.filter(ImageFilter.GaussianBlur(20 * S)))
    d = ImageDraw.Draw(lay)
    rr(d, (x0, y0, x1, y1), 30, fill=(255, 255, 255), outline=LINHA, width=2 * S)
    if ativo > 0:
        gl = Image.new("RGBA", lay.size, (0, 0, 0, 0))
        rr(ImageDraw.Draw(gl), (x0, y0, x1, y1), 30, outline=VERDE + (int(120 * ativo),), width=12 * S)
        lay.alpha_composite(gl.filter(ImageFilter.GaussianBlur(6 * S)))
        d = ImageDraw.Draw(lay)
        rr(d, (x0, y0, x1, y1), 30, outline=VERDE + (int(255 * ativo),), width=4 * S)
    cx = (x0 + x1) / 2
    # ícone num círculo verde
    rad = 54 + 4 * ativo
    cy = y0 + 106
    d.ellipse([(cx - rad) * S, (cy - rad) * S, (cx + rad) * S, (cy + rad) * S], fill=VERDE)
    icone(d, c["icone"], cx, cy, rad)
    centro(d, cx, y0 + 188, c["titulo"], f(700, 38), TXT)
    centro(d, cx, y0 + 244, c["sub"], f(500, 23), CINZA)
    d.line([(x0 + 28) * S, (y0 + 306) * S, (x1 - 28) * S, (y0 + 306) * S], fill=LINHA, width=2 * S)
    d.text(((x0 + 28) * S, (y0 + 334) * S), "Exemplo no sistema", font=f(600, 19), fill=CINZA)
    # linha do interruptor
    ry0, ry1 = y0 + 378, y0 + 498
    rr(d, (x0 + 24, ry0, x1 - 24, ry1), 20, fill=(244, 244, 245))
    TW, TH = 64, 36
    tx1 = x1 - 24 - 20
    tx0 = tx1 - TW
    fonte = f(600, 22)
    linhas = quebra(c["exemplo"], fonte, tx0 - 14 - (x0 + 24 + 20))
    h_l = 30
    ty = (ry0 + ry1) / 2 - h_l * len(linhas) / 2
    for k, ln in enumerate(linhas):
        d.text(((x0 + 24 + 20) * S, (ty + k * h_l) * S), ln, font=fonte, fill=TXT)
    lig = io((tau - (c["t0"] + 0.45)) / 0.35)  # o interruptor liga quando a fala chega nele
    cor = tuple(int(a + (b - a) * lig) for a, b in zip((196, 198, 204), VERDE))
    tcy = (ry0 + ry1) / 2
    rr(d, (tx0, tcy - TH / 2, tx1, tcy + TH / 2), TH / 2, fill=cor)
    kx = tx0 + TH / 2 + (TW - TH) * lig
    d.ellipse([(kx - 14) * S, (tcy - 14) * S, (kx + 14) * S, (tcy + 14) * S], fill=(255, 255, 255))
    # opacidade geral: cartões que ainda não são a vez ficam um pouco apagados
    algum_ativo = any(io((tau - k["t0"]) / 0.35) * (1 - io((tau - k["t1"]) / 0.35)) > 0.05 for k in CARTOES)
    dim = 0.62 if (algum_ativo and ativo < 0.05) else 1.0
    a = lay.getchannel("A").point(lambda v: int(v * ent * dim))
    lay.putalpha(a)
    return lay


def quadro(tau):
    im = BASE.copy()
    d = ImageDraw.Draw(im)
    # título
    a = oc((tau - 1.2) / 0.6)
    if a > 0:
        tit = "Cada preferência vale para quem deve"
        fo = f(800, 46)
        w = larg(tit, fo)
        assert w <= W - 160, w
        ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
        do = ImageDraw.Draw(ov)
        do.text((((W - w) / 2) * S, (96 + 10 * (1 - a)) * S), tit, font=fo, fill=TXT + (int(255 * a),))
        sub = "Cada interruptor tem o seu alcance"
        fs = f(500, 26)
        ws = larg(sub, fs)
        do.text((((W - ws) / 2) * S, (168 + 10 * (1 - a)) * S), sub, font=fs, fill=CINZA + (int(255 * a),))
        im.alpha_composite(ov)
    for i, c in enumerate(CARTOES):
        im.alpha_composite(cartao(c, i, tau))
    return im.resize((W, H), Image.LANCZOS)


def mascara():
    a, _ = ui.rrect_alpha(W, H, 0, 0, W, H, 16)
    return (a * 255).astype(np.uint8)


def salvar(tau, caminho, m):
    fr = np.array(quadro(tau).convert("RGB"))
    Image.fromarray(np.dstack([fr, m]), "RGBA").save(caminho, optimize=False, compress_level=1)


if __name__ == "__main__":
    args = sys.argv[1:]
    m = mascara()
    if args and args[0] == "--teste":
        out = args[1]
        os.makedirs(out, exist_ok=True)
        for t in args[2:]:
            salvar(float(t), os.path.join(out, f"q_{float(t):05.2f}.png"), m)
            print("quadro", t)
        sys.exit()
    OUT = args[0]
    DUR = float(args[1]) if len(args) > 1 else 13.9
    os.makedirs(OUT, exist_ok=True)
    n = int(round(DUR * FPS))
    for i in range(n):
        salvar(i / FPS, os.path.join(OUT, f"{i:04d}.png"), m)
        if i % 30 == 0:
            print(f"{i}/{n}", flush=True)
    print("ok", OUT, n, "quadros")
