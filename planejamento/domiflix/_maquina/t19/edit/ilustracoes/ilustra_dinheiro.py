"""T19 cap. 1 · "Como o dinheiro chega": quatro quadros da esquerda para a direita (1 a empresa gera a cobrança na Dominex; 2 o cliente recebe o link e paga
por Pix, boleto ou cartão; 3 o dinheiro cai na conta Asaas da empresa e a taxa sai dela; 4 o aviso volta e a conta a receber vira "Pago" no Financeiro).
O Asaas aparece só pelo nome (sem logo nem marca de banco), sem valor de plano. Fundo branco, Montserrat, verde #00C597, objetos genéricos.
Sequência PNG com alfa 1587x992 (cantos de 16 px) para o editor (box = janela em repouso, scale_in 0). Tempos lidos de t19/narracao/cap01.json.
uso: python3 ilustra_dinheiro.py <pasta_saida> [duração] [--stills t1,t2,...]"""
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
DOMI = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(DOMI, 'kit'))
import ui  # noqa: E402

NARR = json.load(open(os.path.join(DOMI, 't19', 'narracao', 'cap01.json'), encoding='utf8'))
OUT = sys.argv[1]
DUR = float(sys.argv[2]) if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else NARR['dur']
W, H, S, FPS = 1587, 992, 2, 30
VERDE = (0, 197, 151)
TXT = (24, 24, 27)
CINZA = (113, 113, 122)
LINHA = (222, 224, 228)


def T(linha, palavra, nth=0):
    ws = [w for w in NARR['words'] if w['linha'] == linha and w['w'].lower().strip('.,') == palavra.lower()]
    return ws[nth]['s']


def oc(t):
    t = min(1.0, max(0.0, t))
    return 1 - (1 - t) ** 3


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
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).resize((W * S, H * S), Image.BICUBIC).convert('RGBA')


BASE = fundo()
CW, CH, GAP = 336, 560, 52
X0 = (W - 4 * CW - 3 * GAP) // 2
Y0 = 250
# instantes (s do capítulo) presos às palavras
T_CARD = [T(0, 'Você'), T(0, 'cliente'), T(1, 'dinheiro'), T(2, 'Quando')]
T_CHIP = [T(1, 'Pix'), T(1, 'boleto'), T(1, 'cartão')]
T_TAXA = T(1, 'taxa')
T_PAGO = T(2, 'paga')
T_BAIXA = T(2, 'baixa')
T_TIT = 0.3
CARDS = [
    dict(n='1', t='Você gera a cobrança', s='na Dominex', ic=0),
    dict(n='2', t='O cliente recebe o link e paga', s='', ic=1),
    dict(n='3', t='O dinheiro cai na conta Asaas da empresa', s='', ic=2),
    dict(n='4', t='O Asaas avisa a Dominex', s='', ic=3),
]


def enfase(i, t):
    """destaque do quadro `i`: 1º sozinho; depois o 2º e o 3º; por fim o 4º"""
    if t < T_CARD[2]:
        return 1.0
    if t < T_CARD[3]:
        return 0.55 if i == 0 else 1.0
    return 1.0 if i == 3 else 0.55


def icone(d, cx, cy, k, a):
    c = VERDE + (int(255 * a),)
    w = 4 * S
    if k == 0:   # documento com linhas
        rr(d, (cx - 34, cy - 44, cx + 34, cy + 44), 8, outline=c, width=w)
        for i in range(3):
            d.line([(cx - 20) * S, (cy - 18 + i * 20) * S, (cx + 20) * S, (cy - 18 + i * 20) * S], fill=c, width=3 * S)
    elif k == 1:  # celular com link
        rr(d, (cx - 28, cy - 46, cx + 28, cy + 46), 10, outline=c, width=w)
        d.line([(cx - 10) * S, (cy + 30) * S, (cx + 10) * S, (cy + 30) * S], fill=c, width=3 * S)
        rr(d, (cx - 16, cy - 8, cx - 2, cy + 6), 7, outline=c, width=3 * S)
        rr(d, (cx + 2, cy - 8, cx + 16, cy + 6), 7, outline=c, width=3 * S)
    elif k == 2:  # banco genérico (colunas)
        d.polygon([((cx - 44) * S, (cy - 14) * S), (cx * S, (cy - 46) * S), ((cx + 44) * S, (cy - 14) * S)], outline=c, width=w)
        for i in range(3):
            d.line([(cx - 28 + i * 28) * S, (cy - 6) * S, (cx - 28 + i * 28) * S, (cy + 30) * S], fill=c, width=5 * S)
        d.line([(cx - 44) * S, (cy + 40) * S, (cx + 44) * S, (cy + 40) * S], fill=c, width=w)
    else:  # sino
        d.arc([(cx - 30) * S, (cy - 40) * S, (cx + 30) * S, (cy + 24) * S], 180, 360, fill=c, width=w)
        d.line([(cx - 30) * S, (cy - 8) * S, (cx - 30) * S, (cy + 26) * S], fill=c, width=w)
        d.line([(cx + 30) * S, (cy - 8) * S, (cx + 30) * S, (cy + 26) * S], fill=c, width=w)
        d.line([(cx - 40) * S, (cy + 28) * S, (cx + 40) * S, (cy + 28) * S], fill=c, width=w)
        d.ellipse([(cx - 7) * S, (cy + 34) * S, (cx + 7) * S, (cy + 48) * S], fill=c)


def quebra(d, txt, fonte, larg):
    linhas, cur = [], ''
    for p in txt.split():
        if d.textlength((cur + ' ' + p).strip(), font=fonte) / S <= larg:
            cur = (cur + ' ' + p).strip()
        else:
            linhas.append(cur)
            cur = p
    linhas.append(cur)
    return linhas


def chip(d, x, y, txt, a):
    fo = f(700, 26)
    w = d.textlength(txt, font=fo) / S + 40
    rr(d, (x, y, x + w, y + 52), 26, fill=(231, 248, 243, int(255 * a)), outline=VERDE + (int(255 * a),), width=2 * S)
    d.text(((x + 20) * S, (y + 11) * S), txt, font=fo, fill=TXT + (int(255 * a),))
    return w


def quadro(t):
    im = BASE.copy()
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    ta = oc((t - T_TIT) / 0.6)
    if ta > 0:
        tx = 'O caminho do dinheiro'
        tw = d.textlength(tx, font=f(800, 52)) / S
        d.text(((W - tw) / 2 * S, (110 - (1 - ta) * 20) * S), tx, font=f(800, 52), fill=TXT + (int(255 * ta),))
        rr(d, (W / 2 - 40, 186, W / 2 + 40, 192), 3, fill=VERDE + (int(255 * ta),))
    for i, cd in enumerate(CARDS):
        a0 = oc((t - T_CARD[i]) / 0.5)
        if a0 <= 0:
            continue
        a = a0 * enfase(i, t)
        x, y = X0 + i * (CW + GAP), Y0 + (1 - a0) * 26
        box = (x, y, x + CW, y + CH)
        sh = Image.new('RGBA', im.size, (0, 0, 0, 0))
        rr(ImageDraw.Draw(sh), (box[0] + 6, box[1] + 16, box[2] - 6, box[3] + 16), 28, fill=(0, 40, 30, int(55 * a)))
        lay.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18 * S)))
        d = ImageDraw.Draw(lay)
        rr(d, box, 28, fill=(255, 255, 255, int(255 * a)), outline=LINHA + (int(255 * a),), width=2 * S)
        d.ellipse([(x + 24) * S, (y + 24) * S, (x + 72) * S, (y + 72) * S], fill=VERDE + (int(255 * a),))
        nw = d.textlength(cd['n'], font=f(800, 30)) / S
        d.text(((x + 48 - nw / 2) * S, (y + 31) * S), cd['n'], font=f(800, 30), fill=(255, 255, 255, int(255 * a)))
        icone(d, x + CW / 2, y + 150, cd['ic'], a)
        fo = f(800, 32)
        yy = y + 232
        for ln in quebra(d, cd['t'], fo, CW - 60):
            assert d.textlength(ln, font=fo) / S < CW - 48, ln
            d.text(((x + 30) * S, yy * S), ln, font=fo, fill=TXT + (int(255 * a),))
            yy += 44
        if cd['s']:
            d.text(((x + 30) * S, (yy + 4) * S), cd['s'], font=f(600, 28), fill=CINZA + (int(255 * a),))
        if i == 1:   # formas de pagamento
            cx, cy = x + 30, y + 374
            for k, nome in enumerate(['Pix', 'Boleto', 'Cartão']):
                ca = oc((t - T_CHIP[k]) / 0.35) * enfase(i, t)
                if ca > 0:
                    chip(d, cx, cy + k * 56, nome, ca)
        if i == 2:   # taxa sai dessa conta
            ca = oc((t - T_TAXA) / 0.4) * enfase(i, t)
            if ca > 0:
                rr(d, (x + 30, y + 440, x + CW - 30, y + 520), 16, fill=(255, 244, 229, int(255 * ca)))
                for k, tx in enumerate(['A taxa do Asaas', 'sai dessa conta']):
                    assert d.textlength(tx, font=f(700, 26)) / S < CW - 60 - 40, tx
                    d.text(((x + 52) * S, (y + 452 + k * 32) * S), tx, font=f(700, 26), fill=TXT + (int(255 * ca),))
        if i == 3:   # Pago e baixa
            pa = oc((t - T_PAGO - 2.2) / 0.4) * enfase(i, t)
            if pa > 0:
                rr(d, (x + 30, y + 400, x + 30 + 120, y + 452), 26, fill=VERDE + (int(255 * pa),))
                d.text(((x + 30 + 60 - d.textlength('Pago', font=f(800, 28)) / S / 2) * S, (y + 411) * S), 'Pago', font=f(800, 28), fill=(255, 255, 255, int(255 * pa)))
            ba = oc((t - T_BAIXA) / 0.4) * enfase(i, t)
            if ba > 0:
                for k, tx in enumerate(['Baixa no', 'Financeiro']):
                    d.text(((x + 30) * S, (y + 468 + k * 32) * S), tx, font=f(700, 26), fill=TXT + (int(255 * ba),))
        if i < 3:   # seta para o próximo quadro
            na = oc((t - T_CARD[i + 1]) / 0.4)
            if na > 0:
                ax, ay = x + CW + GAP / 2, Y0 + CH / 2
                c = VERDE + (int(255 * na),)
                d.line([(ax - 14) * S, ay * S, (ax + 10) * S, ay * S], fill=c, width=5 * S)
                d.polygon([((ax + 18) * S, ay * S), ((ax + 6) * S, (ay - 12) * S), ((ax + 6) * S, (ay + 12) * S)], fill=c)
    im.alpha_composite(lay)
    return im.resize((W, H), Image.LANCZOS)


def mascara():
    a, _ = ui.rrect_alpha(W, H, 0, 0, W, H, 16)
    return (a * 255).astype(np.uint8)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    if '--stills' in sys.argv:
        for tt in [float(x) for x in sys.argv[sys.argv.index('--stills') + 1].split(',')]:
            quadro(tt).save(os.path.join(OUT, f'still_{tt:05.1f}.png'))
        print('stills ok')
        sys.exit(0)
    m = mascara()
    n = int(round(DUR * FPS))
    for i in range(n):
        fr = np.array(quadro(i / FPS).convert('RGB'))
        Image.fromarray(np.dstack([fr, m]), 'RGBA').save(os.path.join(OUT, f'{i:04d}.png'), optimize=False, compress_level=1)
    print('ok', OUT, n, 'quadros')
