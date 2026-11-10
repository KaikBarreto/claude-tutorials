"""T12 cap. 10 · "Qual link mandar": dois cartões lado a lado, "Portal do Cliente" (dono ou gestor: ordens de serviço, aparelhos,
contratos e cobranças do cliente) e "Portal do Contrato" (portaria, síndico e fiscalização: plano, cronograma e documentos de uma
unidade, com o QR Code no quadro). Fundo branco, Montserrat, verde #00C597, objetos genéricos, sem marca de terceiros e sem preço.
Sequência PNG com alfa 1587x992 (cantos de 16 px) para o editor (box = janela em repouso, scale_in 0). Tempos locais (s), casados com a fala
do cap. 10 (a ilustração começa em 11,7 s do capítulo):
  2,6 "Portal do Cliente"  4,0 "dono ou gestor"  7,8 "ordens de serviço"  9,2 "aparelhos"  10,2 "contratos"  11,1 "cobranças"
 12,0 "Portal do Contrato"  13,9 "portaria"  14,9 "síndico"  15,7 "fiscalização"  17,0 "só aquela unidade"  19,3 "QR Code"  20,6 "no quadro"
uso: python3 ilustra_portais.py <pasta_saida> [duração=21.1]"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.abspath(os.path.join(HERE, '..', '..', '..')), 'kit'))
import ui  # noqa: E402

OUT = sys.argv[1]
DUR = float(sys.argv[2]) if len(sys.argv) > 2 else 21.1
W, H, S, FPS = 1587, 992, 2, 30
VERDE = (0, 197, 151)
TXT = (24, 24, 27)
CINZA = (113, 113, 122)
LINHA = (222, 224, 228)


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


def fundo():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    g = np.exp(-(((xx - W / 2) / 700) ** 2 + ((yy - 420) / 420) ** 2))
    arr = np.full((H, W, 3), 255, np.float32)
    arr -= (np.array([255, 255, 255]) - np.array([231, 248, 243])) * (0.5 * g)[..., None]
    v = np.clip(((xx - W / 2) / (W * 0.7)) ** 2 + ((yy - H / 2) / (H * 0.8)) ** 2, 0, 1)
    arr -= 10 * v[..., None]
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).resize((W * S, H * S), Image.BICUBIC)
    return im.convert("RGBA")


BASE = fundo()
CW, CH, GAP = 640, 700, 70
X1 = (W - 2 * CW - GAP) // 2
X2 = X1 + CW + GAP
Y0 = 150
CARTOES = [
    dict(x=X1, t=2.6, titulo="Portal do Cliente", quem="Dono ou gestor", sub="Tudo o que é do cliente",
         itens=[("Ordens de serviço", 7.8), ("Aparelhos", 9.2), ("Contratos", 10.2), ("Cobranças", 11.1)], quem_t=4.0),
    dict(x=X2, t=12.0, titulo="Portal do Contrato", quem="Portaria, síndico e fiscalização", sub="Só aquela unidade",
         itens=[("Plano de manutenção", 17.0), ("Cronograma", 17.9), ("Documentos", 18.6)], quem_t=13.9),
]


def sombra(im, box):
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    rr(ImageDraw.Draw(sh), (box[0] + 6, box[1] + 18, box[2] - 6, box[3] + 18), 30, fill=(0, 40, 30, 60))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(20 * S)))


def icone(d, x, y, k, a):
    """ícone genérico de 34 px: 0 lista, 1 aparelho, 2 documento, 3 cifrão (sem texto de preço), 4 calendário"""
    c = VERDE + (int(255 * a),)
    if k == 0:
        for i in range(3):
            rr(d, (x, y + 4 + i * 11, x + 34, y + 10 + i * 11), 3, fill=c)
    elif k == 1:
        rr(d, (x, y + 6, x + 34, y + 22), 6, outline=c, width=3 * S)
        d.line([(x + 6) * S, (y + 28) * S, (x + 28) * S, (y + 28) * S], fill=c, width=3 * S)
    elif k == 2:
        rr(d, (x + 5, y, x + 29, y + 34), 4, outline=c, width=3 * S)
        d.line([(x + 11) * S, (y + 12) * S, (x + 23) * S, (y + 12) * S], fill=c, width=2 * S)
        d.line([(x + 11) * S, (y + 20) * S, (x + 23) * S, (y + 20) * S], fill=c, width=2 * S)
    elif k == 3:
        rr(d, (x, y + 5, x + 34, y + 29), 5, outline=c, width=3 * S)
        d.line([x * S, (y + 14) * S, (x + 34) * S, (y + 14) * S], fill=c, width=3 * S)
        d.line([(x + 6) * S, (y + 23) * S, (x + 14) * S, (y + 23) * S], fill=c, width=3 * S)
    else:
        rr(d, (x + 1, y + 4, x + 33, y + 33), 5, outline=c, width=3 * S)
        d.line([(x + 1) * S, (y + 13) * S, (x + 33) * S, (y + 13) * S], fill=c, width=3 * S)


ICONES = {"Ordens de serviço": 0, "Aparelhos": 1, "Contratos": 2, "Cobranças": 3, "Plano de manutenção": 2, "Cronograma": 4, "Documentos": 2}
QRM = np.random.default_rng(12).random((15, 15)) < 0.5


def quadro_qr(d, x, y, a):
    """quadro da casa de máquinas com o QR Code colado (15x15 módulos, 3 marcas de canto)"""
    c = int(255 * a)
    rr(d, (x, y, x + 150, y + 150), 12, fill=(250, 250, 250, c), outline=(150, 154, 160, c), width=3 * S)
    q = 8.4
    ox, oy = x + 12, y + 12
    for i in range(15):
        for j in range(15):
            canto = (i < 5 and j < 5) or (i < 5 and j > 9) or (i > 9 and j < 5)
            if QRM[i, j] and not canto:
                d.rectangle([(ox + j * q) * S, (oy + i * q) * S, (ox + (j + 1) * q) * S - 1, (oy + (i + 1) * q) * S - 1], fill=(24, 24, 27, c))
    for (i, j) in ((0, 0), (0, 10), (10, 0)):
        px, py = ox + j * q, oy + i * q
        d.rectangle([px * S, py * S, (px + 5 * q) * S - 1, (py + 5 * q) * S - 1], fill=(24, 24, 27, c))
        d.rectangle([(px + q) * S, (py + q) * S, (px + 4 * q) * S - 1, (py + 4 * q) * S - 1], fill=(250, 250, 250, c))
        d.rectangle([(px + 2 * q) * S, (py + 2 * q) * S, (px + 3 * q) * S - 1, (py + 3 * q) * S - 1], fill=(24, 24, 27, c))


def quadro(t):
    im = BASE.copy()
    for cd in CARTOES:
        a = oc((t - cd["t"]) / 0.5)
        if a <= 0:
            continue
        x, y = cd["x"], Y0 + (1 - a) * 26
        box = (x, y, x + CW, y + CH)
        lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
        sombra(lay, box)
        d = ImageDraw.Draw(lay)
        rr(d, box, 30, fill=(255, 255, 255, 255), outline=LINHA + (255,), width=2 * S)
        # faixa verde com o título
        rr(d, (x, y, x + CW, y + 150), 30, fill=VERDE + (255,))
        d.rectangle([x * S, (y + 100) * S, (x + CW) * S, (y + 150) * S], fill=VERDE + (255,))
        d.text(((x + 40) * S, (y + 30) * S), cd["titulo"], font=f(800, 44), fill=(255, 255, 255, 255))
        d.text(((x + 40) * S, (y + 92) * S), cd["sub"], font=f(500, 26), fill=(235, 255, 249, 255))
        # quem abre
        qa = oc((t - cd["quem_t"]) / 0.4)
        if qa > 0:
            rr(d, (x + 40, y + 180, x + CW - 40, y + 246), 33, fill=(231, 248, 243, int(255 * qa)))
            tw = d.textlength(cd["quem"], font=f(600, 26)) / S
            assert tw < CW - 80 - 40, tw
            d.text(((x + 64) * S, (y + 198) * S), cd["quem"], font=f(600, 26), fill=TXT + (int(255 * qa),))
        # itens
        for i, (nome, ti) in enumerate(cd["itens"]):
            ia = oc((t - ti) / 0.4)
            if ia <= 0:
                continue
            yy = y + 290 + i * 78 + (1 - ia) * 14
            icone(d, x + 44, yy + 4, ICONES[nome], ia)
            d.text(((x + 100) * S, yy * S), nome, font=f(600, 32), fill=TXT + (int(255 * ia),))
            d.line([(x + 40) * S, (yy + 56) * S, (x + CW - 40) * S, (yy + 56) * S], fill=LINHA + (int(255 * ia),), width=S)
        # QR Code no quadro (só no cartão do contrato)
        if cd["titulo"] == "Portal do Contrato":
            qa2 = oc((t - 19.3) / 0.5)
            if qa2 > 0:
                qx, qy = x + 40, y + CH - 40 - 150
                quadro_qr(d, qx, qy, qa2)
                ta = oc((t - 20.6) / 0.4)
                if ta > 0:
                    for k, tx in enumerate(["QR Code colado", "no quadro da unidade"]):
                        assert d.textlength(tx, font=f(600, 28)) / S < CW - 40 - 190 - 12
                        d.text(((qx + 176) * S, (qy + 50 + k * 40) * S), tx, font=f(600, 28), fill=TXT + (int(255 * ta),))
        im.alpha_composite(lay)
    return im.resize((W, H), Image.LANCZOS)


def mascara():
    a, _ = ui.rrect_alpha(W, H, 0, 0, W, H, 16)
    return (a * 255).astype(np.uint8)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    m = mascara()
    n = int(round(DUR * FPS))
    for i in range(n):
        fr = np.array(quadro(i / FPS).convert("RGB"))
        Image.fromarray(np.dstack([fr, m]), "RGBA").save(os.path.join(OUT, f"{i:04d}.png"), optimize=False, compress_level=1)
    print("ok", OUT, n, "quadros")
