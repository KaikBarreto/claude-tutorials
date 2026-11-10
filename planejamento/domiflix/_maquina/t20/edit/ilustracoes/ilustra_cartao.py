"""T20 cap. 5 · "A compra no cartão": a mesma compra (Bomba de vácuo e vacuômetro, 3x no Cartão Empresarial do T13) em três marcos numa linha do
tempo, 1 Compra (dia 20, parcela 1/3), 2 Fatura (fecha no dia 5, vence no dia 15) e 3 Pagamento (dia 10); embaixo, "Competência" sai da compra
(cada parcela no mês dela: mês 1, 2 e 3) e "Caixa" sai do pagamento (no mês em que a fatura foi paga); por fim a fatura ganha o selo "só marca o
vencimento". Sem valores nem nomes de mês (a fala não cita). Fundo branco, Montserrat, verde, objetos genéricos. Tempos de t20/narracao/cap05.json.
uso: python3 -I ilustra_cartao.py <saida.mp4> [--stills t1,t2,...] [--resumo <saida.png>]
  --resumo: um quadro com tudo aceso (para a recapitulação do cap. 12)"""
import json
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ilu_comum import (AMBAR, AMBAR_TXT, BRANCO, CINZA, CLARO, DOMI, FPS, LINHA, TXT, VERDE, W, S, centro, chip, check, f, finaliza, fundo,  # noqa: E402
                       gravar, larg, oc, q, rgba, rr, seta, sombra, texto)

NARR = json.load(open(os.path.join(DOMI, 't20', 'narracao', 'cap05.json'), encoding='utf8'))


def T(linha, palavra, nth=0):
    ws = [w for w in NARR['words'] if w['linha'] == linha and w['w'].lower().strip('.,:;!?') == palavra.lower()]
    return ws[nth]['s']


T_TIT = 0.12
T_LINHA = T(0, 'datas') - 0.3
T_CARD = [T(0, 'dia') - 0.15, T(0, 'fechamento') - 0.2, T(0, 'dia', 1) - 0.15]
T_COMP = NARR['linhas'][1]['s']                                   # "Em competência"
T_PARC = [T(1, 'parcela'), T(1, 'parcela') + 0.45, T(1, 'parcela') + 0.9]
T_CAIXA = T(1, 'caixa') - 0.24                                     # "Em caixa"
T_CAIXA_CHIP = T(1, 'mês', 2)
T_FAT = NARR['linhas'][2]['s']                                     # "E o mês da fatura"
T_SELO = T(2, 'conta') - 0.3                                       # "não conta pro resultado"
DUR = round(NARR['linhas'][3]['s'] + 0.13, 2)                      # até a L4 ("Por isso a bomba de vácuo aparece aqui")

BASE = fundo()
CW, CH, GAP = 400, 270, 93
X0 = (W - 3 * CW - 2 * GAP) // 2
YC = 290                                  # topo dos cartões
YL = 250                                  # linha do tempo
CX = [X0 + i * (CW + GAP) + CW / 2 for i in range(3)]
BW, BY, BH = 660, 640, 262                # caixas de resultado (Competência à esquerda, Caixa à direita)
BX = [X0, W - X0 - BW]
CARDS = [
    dict(n='1', t='Compra', l=['dia 20'], chip='parcela 1/3', ic='cartao'),
    dict(n='2', t='Fatura', l=['fecha no dia 5', 'vence no dia 15'], chip=None, ic='doc'),
    dict(n='3', t='Pagamento', l=['da fatura, no dia 10'], chip=None, ic='ok'),
]


def mistura(t, a, b, t0, dur=0.4):
    """valor que vai de `a` para `b` a partir de t0 (suave)"""
    return a + (b - a) * oc((t - t0) / dur)


def estado(t, resumo=False):
    if resumo:
        return dict(tit=1.0, lin=1.0, c0=1.0, c1=1.0, c2=1.0, e0=1.0, e1=1.0, e2=1.0, ca=1.0, cb=1.0, ea=1.0, eb=1.0,
                    p0=1.0, p1=1.0, p2=1.0, pc=1.0, selo=1.0)
    e = dict(tit=q(oc((t - T_TIT) / 0.6)), lin=q(oc((t - T_LINHA) / 0.8)))
    for i in range(3):
        e[f'c{i}'] = q(oc((t - T_CARD[i]) / 0.5))
    # ênfase: todos acesos; Competência acende o 1; Caixa acende o 3; a fatura acende o 2
    for i in range(3):
        v = 1.0
        if t >= T_COMP:
            v = mistura(t, 1.0, 1.0 if i == 0 else 0.5, T_COMP)
        if t >= T_CAIXA:
            v = mistura(t, 1.0 if i == 0 else 0.5, 1.0 if i == 2 else 0.5, T_CAIXA)
        if t >= T_FAT:
            v = mistura(t, 1.0 if i == 2 else 0.5, 1.0 if i == 1 else 0.5, T_FAT)
        e[f'e{i}'] = q(v)
    e['ca'] = q(oc((t - T_COMP) / 0.5))
    e['cb'] = q(oc((t - T_CAIXA) / 0.5))
    e['ea'] = q(mistura(t, 1.0, 0.5, T_CAIXA) if t < T_FAT else mistura(t, 0.5, 0.5, T_FAT))
    e['eb'] = q(1.0 if t < T_FAT else mistura(t, 1.0, 0.5, T_FAT))
    for k in range(3):
        e[f'p{k}'] = q(oc((t - T_PARC[k]) / 0.35))
    e['pc'] = q(oc((t - T_CAIXA_CHIP) / 0.35))
    e['selo'] = q(oc((t - T_SELO) / 0.4))
    return e


def icone(d, cx, cy, k, a):
    c = rgba(VERDE, a)
    w = 4 * S
    if k == 'cartao':      # cartão genérico com tarja
        rr(d, (cx - 30, cy - 20, cx + 30, cy + 20), 6, outline=c, width=w)
        d.line([(cx - 30) * S, (cy - 8) * S, (cx + 30) * S, (cy - 8) * S], fill=c, width=6 * S)
        d.line([(cx - 20) * S, (cy + 9) * S, (cx - 4) * S, (cy + 9) * S], fill=c, width=3 * S)
    elif k == 'doc':       # documento com linhas
        rr(d, (cx - 22, cy - 28, cx + 22, cy + 28), 6, outline=c, width=w)
        for i in range(3):
            d.line([(cx - 12) * S, (cy - 12 + i * 12) * S, (cx + 12) * S, (cy - 12 + i * 12) * S], fill=c, width=3 * S)
    else:                  # círculo com conferido
        d.ellipse([(cx - 26) * S, (cy - 26) * S, (cx + 26) * S, (cy + 26) * S], outline=c, width=w)
        check(d, cx, cy, 24, a, cor=VERDE, w=4.5)


def cartao(lay, d, i, e):
    a0 = e[f'c{i}']
    if a0 <= 0:
        return d
    a = a0 * e[f'e{i}']
    x = X0 + i * (CW + GAP)
    y = YC + (1 - a0) * 24
    box = (x, y, x + CW, y + CH)
    sombra(lay, box, 26, a)
    d = ImageDraw.Draw(lay)
    rr(d, box, 26, fill=rgba(BRANCO, a), outline=rgba(VERDE if e[f'e{i}'] > 0.99 and e['ca'] > 0 else LINHA, a), width=2 * S)
    cd = CARDS[i]
    d.ellipse([(x + 24) * S, (y + 22) * S, (x + 70) * S, (y + 68) * S], fill=rgba(VERDE, a))
    nw = larg(d, cd['n'], f(800, 28))
    d.text(((x + 47 - nw / 2) * S, (y + 29) * S), cd['n'], font=f(800, 28), fill=rgba(BRANCO, a))
    icone(d, x + CW - 62, y + 46, cd['ic'], a)
    texto(d, x + 28, y + 84, cd['t'], f(800, 36), TXT, a, CW - 28)
    yy = y + 136
    for ln in cd['l']:
        texto(d, x + 28, yy, ln, f(600, 27), CINZA, a, CW - 28)
        yy += 36
    if cd['chip']:
        chip(d, x + 28, y + 182, cd['chip'], a, fonte=f(700, 24))
    if i == 1 and e['selo'] > 0:
        sa = e['selo'] * (0.55 + 0.45 * e['e1'])
        fo = f(700, 24)
        w = larg(d, 'só marca o vencimento', fo) + 40
        assert w <= CW - 56, 'selo não cabe'
        chip(d, x + 28, y + 212, 'só marca o vencimento', sa, fonte=fo, fill=AMBAR, contorno=None, cor=AMBAR_TXT)
    return d


def caixa_resultado(lay, d, k, e):
    """k = 0: Competência (sai do cartão 1); k = 1: Caixa (sai do cartão 3)"""
    a0 = e['ca'] if k == 0 else e['cb']
    if a0 <= 0:
        return d
    a = a0 * (e['ea'] if k == 0 else e['eb'])
    x = BX[k]
    y = BY + (1 - a0) * 20
    sx = CX[0] if k == 0 else CX[2]
    seta(d, sx, YC + CH + 10, sx, y - 8, a)
    box = (x, y, x + BW, y + BH)
    sombra(lay, box, 26, a)
    d = ImageDraw.Draw(lay)
    rr(d, box, 26, fill=rgba(BRANCO, a), outline=rgba(VERDE, a), width=2 * S)
    nome = 'Competência' if k == 0 else 'Caixa'
    fo = f(800, 26)
    w = larg(d, nome, fo) + 44
    rr(d, (x + 28, y + 26, x + 28 + w, y + 74), 24, fill=rgba(VERDE, a))
    asc, desc = fo.getmetrics()
    d.text(((x + 50) * S, (y + 50) * S - (asc + desc) / 2 + desc * 0.15), nome, font=fo, fill=rgba(BRANCO, a))
    linhas = (['Cada parcela entra no mês dela,', 'a partir do mês da compra.'] if k == 0 else
              ['Entra no mês em que', 'a fatura foi paga.'])
    yy = y + 96
    for ln in linhas:
        texto(d, x + 28, yy, ln, f(700, 30), TXT, a, BW - 28)
        yy += 40
    if k == 0:
        cx = x + 28
        for j, s in enumerate(['mês 1 · 1/3', 'mês 2 · 2/3', 'mês 3 · 3/3']):
            pa = e[f'p{j}'] * a
            if pa > 0:
                cx += chip(d, cx, y + 190, s, pa, fonte=f(700, 24)) + 16
        assert cx - 16 <= x + BW - 24, 'fichas da competência não cabem'
    elif e['pc'] > 0:
        w = chip(d, x + 28, y + 190, 'mês do pagamento da fatura', e['pc'] * a, fonte=f(700, 24))
        assert x + 28 + w <= x + BW - 24, 'ficha do caixa não cabe'
    return d


def desenha(e):
    im = BASE.copy()
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    ta = e['tit']
    if ta > 0:
        centro(d, W / 2, 52 - (1 - ta) * 16, 'Três datas da compra no cartão', f(800, 50), TXT, ta, W - 200)
        centro(d, W / 2, 124, 'Bomba de vácuo e vacuômetro, em 3x no cartão', f(600, 27), CINZA, ta, W - 200)
    la = e['lin']
    if la > 0:
        x0, x1 = 80, W - 80
        xe = x0 + (x1 - x0) * la
        d.line([x0 * S, YL * S, xe * S, YL * S], fill=rgba(LINHA, 1.0), width=6 * S)
        xm = (CX[0] + CX[1]) / 2   # virada do mês, entre a compra e a fatura
        if xe > xm:
            d.line([xm * S, (YL - 26) * S, xm * S, (YL + 26) * S], fill=rgba(CINZA, la), width=3 * S)
        centro(d, CX[0], YL - 62, 'mês da compra', f(600, 24), CINZA, la, 2 * (xm - 80))
        centro(d, (xm + x1) / 2, YL - 62, 'mês seguinte', f(600, 24), CINZA, la, x1 - xm)
    for i in range(3):
        a0 = e[f'c{i}']
        if a0 > 0:   # marco na linha + haste até o cartão
            a = a0 * e[f'e{i}']
            r = 12 + 4 * (1 - a0)
            d.line([CX[i] * S, (YL + 12) * S, CX[i] * S, (YC - 4) * S], fill=rgba(VERDE, a), width=3 * S)
            d.ellipse([(CX[i] - r) * S, (YL - r) * S, (CX[i] + r) * S, (YL + r) * S], fill=rgba(VERDE, a), outline=rgba(BRANCO, a), width=3 * S)
    for i in range(3):
        d = cartao(lay, d, i, e)
    for k in range(2):
        d = caixa_resultado(lay, d, k, e)
    im.alpha_composite(lay)
    return finaliza(im)


if __name__ == '__main__':
    saida = sys.argv[1]
    if '--resumo' in sys.argv:
        desenha(estado(0, resumo=True)).convert('RGB').save(sys.argv[sys.argv.index('--resumo') + 1])
        print('resumo ok')
        sys.exit(0)
    if '--stills' in sys.argv:
        os.makedirs(saida, exist_ok=True)
        for tt in [float(x) for x in sys.argv[sys.argv.index('--stills') + 1].split(',')]:
            desenha(estado(tt)).convert('RGB').save(os.path.join(saida, f'cartao_{tt:05.2f}.png'))
        print('stills ok', saida)
        sys.exit(0)
    print('tempos:', dict(tit=T_TIT, linha=round(T_LINHA, 2), cards=[round(x, 2) for x in T_CARD], comp=T_COMP, parc=[round(x, 2) for x in T_PARC],
                          caixa=round(T_CAIXA, 2), caixa_chip=T_CAIXA_CHIP, fat=T_FAT, selo=round(T_SELO, 2), dur=DUR, fps=FPS))
    gravar(saida, 0.0, DUR, estado, desenha)
