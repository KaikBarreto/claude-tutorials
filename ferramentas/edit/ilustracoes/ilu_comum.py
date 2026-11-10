"""Utilitários das ilustrações em vídeo (T19/T20/T14): fundo branco com brilho na cor da marca, fonte da marca, objetos genéricos.
Saída em MP4 1586x992 (a janela do app em repouso; largura par para o libx264): o editor arredonda os cantos ("radius": 16, "shadow":
false no JSON do capítulo) e não precisa de alfa. Quadro igual ao anterior (mesma chave de estado) é reaproveitado, sem desenhar de novo:
22,5 s de ilustração saem em ~1,7 MB (a sequência PNG com alfa do mesmo desenho passava de 100 MB). Todo texto é medido antes de
desenhar (`texto(..., larg_max=)` falha se não couber, com 12 px de folga). As cores foram desenhadas para o verde de referência
(#00C597) e seguem o acento da marca (`ui.tom`): com a marca Domiflix saem iguais às do T20.
Uso (molde: uma ilustração por arquivo em <tutorial>/edit/ilustracoes/ilustra_<assunto>.py):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from ilu_comum import DOMI, W, H, S, f, fundo, texto, chip, gravar, finaliza, oc, q, palavra
    NARR = json.load(open(os.path.join(DOMI, '<tutorial>', 'narracao', 'capNN.json')))
    T1 = palavra(NARR, 0, 'datas') - 0.3                          # tempos casados com a fala (s do capítulo)
    def estado(t): return {'a': q(oc((t - T1) / 0.4))}             # tudo o que muda no quadro, arredondado com q()
    def desenha(e): im = fundo(); ...; return finaliza(im)          # desenha em W*S x H*S e reduz para W x H
    gravar(saida_mp4, t0, dur, estado, desenha)
No specs.json: "ilustracoes": [{"at": t0, "dur": dur, "src": "<saida.mp4>", "box": [166, 44, 1587, 992], "radius": 16, "shadow": false,
"scale_in": 0.0}] (box = janela do app em repouso, como no T14/T20; confira 1 quadro 1:1 de cada cena antes do render)."""
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
DOMI = os.environ.get('TUT_HOME') or os.path.abspath(os.path.join(HERE, '..', '..', '..'))   # <TUT_HOME>/<tutorial>/edit/ilustracoes
_KIT = os.path.join(DOMI, 'kit')
sys.path.insert(0, _KIT if os.path.isdir(_KIT) else os.path.abspath(os.path.join(HERE, '..', '..', 'kit')))   # ou o kit da skill
import ui  # noqa: E402

W, H, S, FPS = 1586, 992, 2, 30


def _tom(c):
    return tuple(int(round(v)) for v in ui.tom(c))


VERDE = _tom((0, 197, 151))          # acento da marca (Domiflix: #00C597)
TXT = (24, 24, 27)
CINZA = (113, 113, 122)
LINHA = (222, 224, 228)
CLARO = _tom((231, 248, 243))        # fundo claro do acento (chips, brilho do fundo)
AMBAR = (255, 244, 229)
AMBAR_TXT = (150, 82, 0)
BRANCO = (255, 255, 255)


def palavra(narr, linha, p, nth=0):
    """início (s) da `nth`-ésima ocorrência da palavra `p` na linha `linha` (contada a partir de 0) do capNN.json da narração"""
    ws = [w for w in narr['words'] if w['linha'] == linha and w['w'].lower().strip('.,:;!?…') == p.lower().strip('.,:;!?…')]
    if len(ws) <= nth:
        raise SystemExit(f'palavra {p!r} (ocorrência {nth}) não achada na linha {linha}')
    return ws[nth]['s']


def oc(t):
    t = min(1.0, max(0.0, t))
    return 1 - (1 - t) ** 3


def f(w, px):
    return ui.font(w, int(px * S))


def rgba(c, a):
    return tuple(c) + (int(round(255 * max(0.0, min(1.0, a)))),)


def rr(d, box, r, **kw):
    x0, y0, x1, y1 = box
    d.rounded_rectangle([x0 * S, y0 * S, x1 * S, y1 * S], radius=r * S, **kw)


def larg(d, s, fonte):
    return d.textlength(s, font=fonte) / S


def texto(d, x, y, s, fonte, cor, a, larg_max=None):
    if larg_max is not None:
        w = larg(d, s, fonte)
        assert w <= larg_max - 12, f'texto não cabe ({w:.0f} > {larg_max - 12:.0f}): {s!r}'
    d.text((x * S, y * S), s, font=fonte, fill=rgba(cor, a))


def centro(d, cx, y, s, fonte, cor, a, larg_max=None):
    w = larg(d, s, fonte)
    if larg_max is not None:
        assert w <= larg_max - 12, f'texto não cabe ({w:.0f} > {larg_max - 12:.0f}): {s!r}'
    d.text(((cx - w / 2) * S, y * S), s, font=fonte, fill=rgba(cor, a))


def chip(d, x, y, s, a, fonte=None, fill=CLARO, contorno=VERDE, cor=TXT, h=46, pad=20):
    fonte = fonte or f(700, 24)
    w = larg(d, s, fonte) + 2 * pad
    rr(d, (x, y, x + w, y + h), h / 2, fill=rgba(fill, a), outline=rgba(contorno, a) if contorno else None, width=2 * S)
    asc, desc = fonte.getmetrics()
    d.text(((x + pad) * S, (y + h / 2) * S - (asc + desc) / 2 + desc * 0.15), s, font=fonte, fill=rgba(cor, a))
    return w


def sombra(lay, box, r, a, blur=18, dy=16, cor=None, op=55):
    cor = cor or _tom((0, 40, 30))   # sombra levemente puxada para o acento
    sh = Image.new('RGBA', lay.size, (0, 0, 0, 0))
    rr(ImageDraw.Draw(sh), (box[0] + 6, box[1] + dy, box[2] - 6, box[3] + dy), r, fill=cor + (int(op * a),))
    lay.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur * S)))


def seta(d, x0, y0, x1, y1, a, cor=VERDE, w=5, cab=14):
    """seta reta de (x0,y0) a (x1,y1), com a ponta em (x1,y1)"""
    v = np.array([x1 - x0, y1 - y0], float)
    n = np.hypot(*v) or 1.0
    u = v / n
    p = np.array([-u[1], u[0]])
    base = np.array([x1, y1]) - u * cab
    d.line([x0 * S, y0 * S, base[0] * S, base[1] * S], fill=rgba(cor, a), width=w * S)
    pts = [tuple(np.array([x1, y1]) * S), tuple((base + p * cab * 0.75) * S), tuple((base - p * cab * 0.75) * S)]
    d.polygon(pts, fill=rgba(cor, a))


def check(d, cx, cy, r, a, cor=BRANCO, w=5):
    """sinal de conferido centrado em (cx, cy) num quadrado de lado ~2r"""
    pts = [(cx - r * 0.55, cy + r * 0.02), (cx - r * 0.12, cy + r * 0.45), (cx + r * 0.6, cy - r * 0.42)]
    d.line([(x * S, y * S) for x, y in pts], fill=rgba(cor, a), width=int(w * S), joint='curve')


def fundo():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    g = np.exp(-(((xx - W / 2) / 700) ** 2 + ((yy - 420) / 420) ** 2))
    arr = np.full((H, W, 3), 255, np.float32)
    arr -= (np.array([255, 255, 255]) - np.array(CLARO)) * (0.5 * g)[..., None]
    v = np.clip(((xx - W / 2) / (W * 0.7)) ** 2 + ((yy - H / 2) / (H * 0.8)) ** 2, 0, 1)
    arr -= 10 * v[..., None]
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).resize((W * S, H * S), Image.BICUBIC).convert('RGBA')


def q(x, passo=1 / 160):
    """arredonda um parâmetro de animação para a chave do quadro (valores iguais = quadro igual)"""
    return round(round(x / passo) * passo, 5)


def gravar(saida, t0, dur, estado, desenha):
    """`estado(t)` devolve um dict com tudo o que muda no quadro (já arredondado com q); `desenha(estado)` devolve a imagem W x H.
    Escreve o MP4 em `saida` (bt709, faixa TV, CRF 14, 30 q/s) e imprime quantos quadros foram desenhados de fato."""
    os.makedirs(os.path.dirname(os.path.abspath(saida)), exist_ok=True)
    tmp = saida + '.tmp.mp4'
    cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
           '-vf', 'scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p',
           '-c:v', 'libx264', '-preset', 'medium', '-crf', '14', '-g', '60', '-colorspace', 'bt709', '-color_primaries', 'bt709',
           '-color_trc', 'bt709', '-color_range', 'tv', '-movflags', '+faststart', tmp]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = int(round(dur * FPS))
    chave_ant, buf, novos = None, None, 0
    for i in range(n):
        e = estado(t0 + i / FPS)
        ch = tuple(sorted(e.items()))
        if ch != chave_ant:
            buf = np.asarray(desenha(e).convert('RGB'), dtype=np.uint8).tobytes()
            chave_ant, novos = ch, novos + 1
        p.stdin.write(buf)
    p.stdin.close()
    if p.wait() != 0:
        raise SystemExit('ffmpeg falhou')
    os.replace(tmp, saida)
    print(f'ok {saida}: {n} quadros ({dur:.2f} s a partir de {t0:.2f} s), {novos} desenhados')


def finaliza(im):
    return im.resize((W, H), Image.LANCZOS)
