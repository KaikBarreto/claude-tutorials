"""T14 cap. 1 · "Esta tela cuida de duas notas": dois caminhos, um em cima do outro (roteiro, [ILUSTRAÇÃO]).
Em cima (NFS-e, nota de serviço): o serviço feito vira a NFS-e, que a Dominex envia à prefeitura, e o cliente recebe.
Embaixo (NF-e, nota de produto): o fornecedor emite a NF-e da compra contra o CNPJ da empresa, e ela chega sozinha na Dominex.
Os dois aparecem juntos ("duas notas"); o de cima fica em destaque na L1 e o de baixo na L2; a nota (ficha verde) anda pelas setas do
caminho em destaque, presa às palavras da fala. Sem brasão nem marca de órgão público; só objetos genéricos, Montserrat e o verde da marca.
MP4 1586x992 (janela do app em repouso; o editor arredonda os cantos). Tempos de t14/narracao/cap01.json.
uso: python3 -I ilustra_caminhos.py <saida.mp4> [--stills t1,t2,...]"""
import json
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ilu_comum import (BRANCO, CINZA, CLARO, DOMI, LINHA, TXT, VERDE, W, S, centro, chip, f, finaliza, fundo, gravar, larg, oc, q,  # noqa: E402
                       rgba, rr, seta, sombra)

NARR = json.load(open(os.path.join(DOMI, 't14', 'narracao', 'cap01.json'), encoding='utf8'))


def T(linha, palavra, nth=0):
    ws = [w for w in NARR['words'] if w['linha'] == linha and w['w'].lower().strip('.,:;!?') == palavra.lower()]
    return ws[nth]['s']


T0 = 0.0
T_FIM = round(NARR['linhas'][1]['e'] + 0.15, 2)      # sai logo depois de "...pelo CNPJ da empresa." (a L3 volta à tela)
DUR = round(T_FIM - T0, 2)
T_TIT = 0.15
T_CIMA = T(0, 'nfs-e') - 0.25                         # "A NFS-e é a nota fiscal de serviço": o caminho de cima em destaque
T_BAIXO = NARR['linhas'][1]['s'] - 0.1                # "A NF-e é a nota de produto": o de baixo
# a ficha da nota anda pelas setas: (parte, chega) em s, presas à fala
VIAGEM = {0: [(T(0, 'serviço'), T(0, 'emite') + 0.2), (T(0, 'cliente') - 0.3, T(0, 'atendimento') + 0.3)],
          1: [(T(1, 'emite'), T(1, 'compra') + 0.2), (T(1, 'chega'), T(1, 'sozinha') + 0.35)]}
T_CNPJ = T(1, 'cnpj')                                # "pelo CNPJ da empresa": o CNPJ pisca

CAMINHOS = [
    dict(tag='NFS-e · nota de serviço', ficha='NFS-e',
         nos=[('Serviço feito', 'a sua empresa emite', 'chave'), ('Prefeitura', 'a Dominex envia', 'predio'), ('Cliente', 'recebe a nota', 'pessoa')]),
    dict(tag='NF-e · nota de produto', ficha='NF-e',
         nos=[('Fornecedor', 'emite na sua compra', 'caixa'), ('CNPJ da empresa', 'a nota vem por ele', 'cartao'), ('Dominex', 'chega sozinha', 'tela')]),
]
BASE = fundo()
NW, NH, GAP = 360, 236, 150                           # nó (cartão) e o vão da seta
X0 = (W - 3 * NW - 2 * GAP) // 2
Y_TAG = [196, 594]
Y_NO = [258, 656]


def estado(t):
    e = dict(tit=q(oc((t - T_TIT) / 0.5)))
    for k in range(2):
        e[f'ap{k}'] = q(oc((t - 0.35 - 0.25 * k) / 0.5))                       # os dois caminhos aparecem juntos
        if t < T_CIMA:
            en = 1.0
        elif t < T_BAIXO:
            en = 1.0 if k == 0 else 0.32 + 0.68 * (1 - oc((t - T_CIMA) / 0.45))
        else:
            en = (1.0 if k == 1 else 0.32) if t >= T_BAIXO + 0.45 else (
                0.32 + 0.68 * oc((t - T_BAIXO) / 0.45) if k == 1 else 1.0 - 0.68 * oc((t - T_BAIXO) / 0.45))
        e[f'en{k}'] = q(en)
        # ficha da nota em cada seta j: anda de um nó ao seguinte (progresso) e some ao chegar (o nó "recebe" a nota)
        for j, (a, b) in enumerate(VIAGEM[k]):
            e[f'f{k}{j}'] = q(oc((t - a) / max(0.3, b - a)), 1 / 120)
            e[f'v{k}{j}'] = q(min(oc((t - a + 0.15) / 0.25), 1 - oc((t - b) / 0.3)))
        e[f'che{k}'] = (q(oc((t - VIAGEM[k][0][0]) / 0.3)),) + tuple(q(oc((t - b) / 0.3)) for _, b in VIAGEM[k])   # nó alcançado: verde
    e['cnpj'] = q(max(0.0, 1 - abs(t - T_CNPJ - 0.25) / 0.6))
    return e


def icone(d, cx, cy, k, a, cor):
    c = rgba(cor, a)
    w = 4 * S
    if k == 'chave':      # serviço feito: círculo com o sinal de conferido
        d.ellipse([(cx - 40) * S, (cy - 40) * S, (cx + 40) * S, (cy + 40) * S], outline=c, width=w)
        pts = [(cx - 19, cy + 1), (cx - 5, cy + 16), (cx + 21, cy - 14)]
        d.line([(x * S, y * S) for x, y in pts], fill=c, width=6 * S, joint='curve')
    elif k == 'predio':   # prédio público genérico (colunas, sem brasão)
        d.polygon([((cx - 46) * S, (cy - 14) * S), (cx * S, (cy - 46) * S), ((cx + 46) * S, (cy - 14) * S)], outline=c, width=w)
        for i in range(4):
            x = cx - 33 + i * 22
            d.line([x * S, (cy - 4) * S, x * S, (cy + 30) * S], fill=c, width=5 * S)
        d.line([(cx - 46) * S, (cy + 40) * S, (cx + 46) * S, (cy + 40) * S], fill=c, width=w)
    elif k == 'pessoa':
        d.ellipse([(cx - 17) * S, (cy - 46) * S, (cx + 17) * S, (cy - 12) * S], outline=c, width=w)
        d.arc([(cx - 38) * S, (cy - 2) * S, (cx + 38) * S, (cy + 74) * S], 180, 360, fill=c, width=w)
        d.line([(cx - 38) * S, (cy + 36) * S, (cx + 38) * S, (cy + 36) * S], fill=c, width=w)
    elif k == 'caixa':    # caixa de material (a compra)
        d.polygon([((cx - 40) * S, (cy - 22) * S), (cx * S, (cy - 40) * S), ((cx + 40) * S, (cy - 22) * S), (cx * S, (cy - 4) * S)], outline=c, width=w)
        d.line([(cx - 40) * S, (cy - 22) * S, (cx - 40) * S, (cy + 24) * S], fill=c, width=w)
        d.line([(cx + 40) * S, (cy - 22) * S, (cx + 40) * S, (cy + 24) * S], fill=c, width=w)
        d.line([cx * S, (cy - 4) * S, cx * S, (cy + 42) * S], fill=c, width=w)
        d.line([(cx - 40) * S, (cy + 24) * S, cx * S, (cy + 42) * S], fill=c, width=w)
        d.line([(cx + 40) * S, (cy + 24) * S, cx * S, (cy + 42) * S], fill=c, width=w)
    elif k == 'cartao':   # cartão de identificação (o CNPJ)
        rr(d, (cx - 48, cy - 32, cx + 48, cy + 32), 9, outline=c, width=w)
        d.ellipse([(cx - 36) * S, (cy - 16) * S, (cx - 12) * S, (cy + 8) * S], outline=c, width=3 * S)
        for i, ww in enumerate((40, 30, 36)):
            d.line([(cx - 2) * S, (cy - 14 + i * 13) * S, (cx - 2 + ww) * S, (cy - 14 + i * 13) * S], fill=c, width=3 * S)
    else:                 # 'tela': monitor genérico (o sistema)
        rr(d, (cx - 50, cy - 40, cx + 50, cy + 22), 8, outline=c, width=w)
        d.line([cx * S, (cy + 22) * S, cx * S, (cy + 36) * S], fill=c, width=w)
        d.line([(cx - 24) * S, (cy + 38) * S, (cx + 24) * S, (cy + 38) * S], fill=c, width=w)
        for i, ww in enumerate((54, 38)):
            d.line([(cx - 32) * S, (cy - 22 + i * 16) * S, (cx - 32 + ww) * S, (cy - 22 + i * 16) * S], fill=c, width=3 * S)


def ficha(d, cx, cy, txt, a):
    fo = f(800, 24)
    w = larg(d, txt, fo) + 34
    rr(d, (cx - w / 2, cy - 22, cx + w / 2, cy + 22), 11, fill=rgba(VERDE, a))
    asc, desc = fo.getmetrics()
    d.text(((cx - (w - 34) / 2) * S, cy * S - (asc + desc) / 2 + desc * 0.15), txt, font=fo, fill=rgba(BRANCO, a))


def desenha(e):
    im = BASE.copy()
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    ta = e['tit']
    if ta > 0:
        centro(d, W / 2, 86 - (1 - ta) * 14, 'Duas notas nesta tela', f(800, 46), TXT, ta, W - 200)
    for k, cm in enumerate(CAMINHOS):
        ap, en = e[f'ap{k}'], e[f'en{k}']
        if ap <= 0:
            continue
        a = ap * en
        dy = (1 - ap) * 22
        cor = VERDE if en > 0.66 else CINZA
        chip(d, X0, Y_TAG[k] + dy, cm['tag'], a, fonte=f(700, 24), fill=CLARO if en > 0.66 else BRANCO, contorno=cor)
        y = Y_NO[k] + dy
        for j, (tit, sub, ic) in enumerate(cm['nos']):
            x = X0 + j * (NW + GAP)
            box = (x, y, x + NW, y + NH)
            sombra(lay, box, 26, a * 0.9)
            d = ImageDraw.Draw(lay)
            che = e[f'che{k}'][j]
            borda = VERDE if (che > 0.5 and en > 0.66) else LINHA
            if k == 1 and j == 1 and e['cnpj'] > 0:
                rr(d, (x - 7, y - 7, x + NW + 7, y + NH + 7), 31, outline=rgba(VERDE, a * e['cnpj']), width=4 * S)
            rr(d, box, 26, fill=rgba(BRANCO, a), outline=rgba(borda, a), width=(3 if borda == VERDE else 2) * S)
            icone(d, x + NW / 2, y + 78, ic, a, VERDE if en > 0.66 else CINZA)
            centro(d, x + NW / 2, y + 140, tit, f(800, 30), TXT, a, NW)
            centro(d, x + NW / 2, y + 184, sub, f(600, 22), CINZA, a, NW)
            if j < 2:   # seta para o próximo nó
                ya = y + NH / 2
                seta(d, x + NW + 18, ya, x + NW + GAP - 18, ya, a, cor=cor, w=5, cab=14)
        # a ficha da nota anda pelas setas do caminho em destaque
        for j in range(2):
            vis = e[f'v{k}{j}'] * ap * en
            if vis > 0.003:
                xa = X0 + j * (NW + GAP) + NW - 8
                xb = X0 + (j + 1) * (NW + GAP) + 8
                ficha(d, xa + (xb - xa) * e[f'f{k}{j}'], y + NH / 2 - 50, cm['ficha'], vis)
    im.alpha_composite(lay)
    return finaliza(im)


if __name__ == '__main__':
    saida = sys.argv[1]
    if '--stills' in sys.argv:
        os.makedirs(saida, exist_ok=True)
        for tt in [float(x) for x in sys.argv[sys.argv.index('--stills') + 1].split(',')]:
            desenha(estado(tt)).convert('RGB').save(os.path.join(saida, f'caminhos_{tt:05.2f}.png'))
        print('stills ok', saida)
        sys.exit(0)
    print('tempos:', dict(t0=T0, fim=T_FIM, dur=DUR, cima=round(T_CIMA, 2), baixo=round(T_BAIXO, 2), viagem=VIAGEM, cnpj=T_CNPJ))
    gravar(saida, T0, DUR, estado, desenha)
