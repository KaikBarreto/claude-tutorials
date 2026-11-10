"""T20 cap. 11 · "Fechar o mês": a lista de conferência do fechamento. "Antes de exportar": contas do mês baixadas, fatura do cartão paga e extrato
conferido com o banco, marcados um a um nas palavras da L2; "Na hora de exportar": período e regime conferidos e relatório exportado ficam por
marcar, porque a L3 volta à tela e confere o período e o regime de verdade. Fundo branco, Montserrat, verde, objetos genéricos.
A ilustração cobre a L2 (do fim da L1 ao começo da L3); tempos de t20/narracao/cap11.json.
uso: python3 -I ilustra_fechamento.py <saida.mp4> [--stills t1,t2,...]   (tempos do capítulo)"""
import json
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ilu_comum import BRANCO, CINZA, CLARO, DOMI, LINHA, TXT, VERDE, W, S, centro, check, f, finaliza, fundo, gravar, oc, q, rgba, rr, sombra, texto  # noqa: E402

NARR = json.load(open(os.path.join(DOMI, 't20', 'narracao', 'cap11.json'), encoding='utf8'))


def T(linha, palavra, nth=0):
    ws = [w for w in NARR['words'] if w['linha'] == linha and w['w'].lower().strip('.,:;!?') == palavra.lower()]
    return ws[nth]['s']


T0 = round(NARR['linhas'][0]['e'] - 0.05, 2)        # entra no fim da L1 ("...do jeito que está na tela.")
T_FIM = round(NARR['linhas'][2]['s'] - 0.04, 2)     # sai no começo da L3 ("Depois confere o período e o regime")
DUR = round(T_FIM - T0, 2)
T_MARCA = [T(1, 'baixa'), T(1, 'paga'), T(1, 'confere')]
ITENS = [('Antes de exportar', ['Contas do mês baixadas', 'Fatura do cartão paga', 'Extrato conferido com o banco']),
         ('Na hora de exportar', ['Período e regime conferidos', 'Relatório exportado em Excel ou PDF'])]

BASE = fundo()
PW, PX = 980, (W - 980) // 2
PY, PH = 196, 650


def estado(t):
    e = dict(tit=q(oc((t - T0 - 0.05) / 0.5)), pap=q(oc((t - T0 - 0.1) / 0.5)))
    k = 0
    for _, itens in ITENS:
        for _ in itens:
            e[f'i{k}'] = q(oc((t - T0 - 0.2 - 0.09 * k) / 0.45))
            k += 1
    for j, tm in enumerate(T_MARCA):
        e[f'm{j}'] = q(oc((t - tm) / 0.3))
    return e


def caixinha(d, x, y, lado, marca, a):
    if marca > 0:
        pop = 1 + 0.18 * (1 - marca) * marca * 4   # leve "pulo" ao marcar
        c = lado / 2
        r0 = c * pop
        rr(d, (x + c - r0, y + c - r0, x + c + r0, y + c + r0), 10, fill=rgba(VERDE, a * marca))
        if marca < 1:
            rr(d, (x, y, x + lado, y + lado), 10, outline=rgba(LINHA, a * (1 - marca)), width=3 * S)
        check(d, x + c, y + c, lado * 0.42, a * marca, cor=BRANCO, w=5.5)
    else:
        rr(d, (x, y, x + lado, y + lado), 10, fill=rgba(BRANCO, a), outline=rgba(LINHA, a), width=3 * S)


def desenha(e):
    im = BASE.copy()
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    ta = e['tit']
    if ta > 0:
        centro(d, W / 2, 62 - (1 - ta) * 16, 'Roteiro de fechamento do mês', f(800, 50), TXT, ta, W - 200)
    pa = e['pap']
    if pa > 0:
        y0 = PY + (1 - pa) * 24
        box = (PX, y0, PX + PW, y0 + PH)
        sombra(lay, box, 28, pa)
        d = ImageDraw.Draw(lay)
        rr(d, box, 28, fill=rgba(BRANCO, pa), outline=rgba(LINHA, pa), width=2 * S)
        y = y0 + 44
        k = 0
        for s, (titulo, itens) in enumerate(ITENS):
            if s:
                d.line([(PX + 56) * S, (y + 6) * S, (PX + PW - 56) * S, (y + 6) * S], fill=rgba(LINHA, pa), width=2 * S)
                y += 34
            texto(d, PX + 56, y, titulo, f(800, 28), VERDE if s == 0 else CINZA, pa, PW - 112)
            y += 62
            for item in itens:
                ia = e[f'i{k}'] * pa
                if ia > 0:
                    marca = e.get(f'm{k}', 0.0) if s == 0 else 0.0
                    dx = (1 - e[f'i{k}']) * 18
                    caixinha(d, PX + 56 + dx, y, 52, marca, ia)
                    cor = TXT if s == 0 else CINZA
                    texto(d, PX + 56 + 52 + 28 + dx, y + 6, item, f(700, 34), cor, ia, PW - 112 - 80)
                y += 84
                k += 1
    im.alpha_composite(lay)
    return finaliza(im)


if __name__ == '__main__':
    saida = sys.argv[1]
    if '--stills' in sys.argv:
        os.makedirs(saida, exist_ok=True)
        for tt in [float(x) for x in sys.argv[sys.argv.index('--stills') + 1].split(',')]:
            desenha(estado(tt)).convert('RGB').save(os.path.join(saida, f'fechamento_{tt:05.2f}.png'))
        print('stills ok', saida)
        sys.exit(0)
    print('tempos:', dict(t0=T0, fim=T_FIM, dur=DUR, marcas=T_MARCA))
    gravar(saida, T0, DUR, estado, desenha)
