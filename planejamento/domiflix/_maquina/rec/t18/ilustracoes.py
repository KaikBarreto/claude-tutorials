#!/usr/bin/env python3
"""T18 · desenhos SVG simples e genéricos (sem logo, sem marca real) para as fotos do catálogo fictício.

Cada função devolve um `data:` URI (o app põe em <img src>, sem passar por storage). Cores de acento por marca fictícia.
Os desenhos ficam sobre o fundo branco do cartão (object-contain), por isso o corpo dos aparelhos é cinza-claro com contorno.
"""
import urllib.parse

CINZA, BORDA, SOMBRA = '#f3f5f7', '#c9d1d9', '#e1e6ea'


def _uri(corpo, w=400, h=260):
    svg = (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} {h}'>"
           f"{corpo}</svg>")
    return 'data:image/svg+xml;utf8,' + urllib.parse.quote(svg, safe="/:=,;'()- ")


def hiwall(acento):
    return _uri(
        "<ellipse cx='200' cy='226' rx='150' ry='9' fill='#000' opacity='.07'/>"
        f"<rect x='34' y='44' width='332' height='112' rx='28' fill='{CINZA}' stroke='{BORDA}' stroke-width='3'/>"
        f"<rect x='34' y='122' width='332' height='44' rx='22' fill='{SOMBRA}' stroke='{BORDA}' stroke-width='3'/>"
        "<rect x='56' y='140' width='288' height='10' rx='5' fill='#b9c3cd'/>"
        f"<rect x='64' y='72' width='84' height='13' rx='6.5' fill='{BORDA}'/>"
        f"<circle cx='334' cy='78' r='6.5' fill='{acento}'/>"
        f"<g stroke='{acento}' stroke-width='4' stroke-linecap='round' fill='none' opacity='.55'>"
        "<path d='M110 184q-14 14 0 28'/><path d='M200 184q-14 14 0 28'/><path d='M290 184q-14 14 0 28'/></g>")


def cassete(acento):
    return _uri(
        "<ellipse cx='200' cy='238' rx='120' ry='9' fill='#000' opacity='.07'/>"
        f"<rect x='88' y='20' width='224' height='216' rx='26' fill='{CINZA}' stroke='{BORDA}' stroke-width='3'/>"
        f"<rect x='116' y='48' width='168' height='160' rx='16' fill='{SOMBRA}' stroke='{BORDA}' stroke-width='2'/>"
        "<g fill='#b9c3cd'><rect x='132' y='62' width='136' height='9' rx='4.5'/><rect x='132' y='185' width='136' height='9' rx='4.5'/>"
        "<rect x='128' y='88' width='9' height='82' rx='4.5'/><rect x='263' y='88' width='9' height='82' rx='4.5'/></g>"
        f"<circle cx='200' cy='128' r='24' fill='white' stroke='{BORDA}' stroke-width='3'/><circle cx='200' cy='128' r='8' fill='{acento}' opacity='.8'/>")


def pisoteto(acento):
    return _uri(
        "<ellipse cx='200' cy='214' rx='160' ry='9' fill='#000' opacity='.07'/>"
        f"<rect x='24' y='64' width='352' height='136' rx='20' fill='{CINZA}' stroke='{BORDA}' stroke-width='3'/>"
        + ''.join(f"<rect x='{52 + i * 22}' y='88' width='10' height='88' rx='5' fill='#b9c3cd'/>" for i in range(9)) +
        f"<rect x='262' y='88' width='92' height='88' rx='12' fill='{SOMBRA}' stroke='{BORDA}' stroke-width='2'/>"
        f"<circle cx='308' cy='132' r='20' fill='white' stroke='{BORDA}' stroke-width='3'/><circle cx='308' cy='132' r='6' fill='{acento}' opacity='.8'/>")


def compressor(acento):
    return _uri(
        "<ellipse cx='200' cy='232' rx='110' ry='9' fill='#000' opacity='.08'/>"
        "<rect x='108' y='40' width='184' height='184' rx='70' fill='#46525e' stroke='#2f3a44' stroke-width='3'/>"
        "<rect x='128' y='62' width='28' height='140' rx='14' fill='white' opacity='.14'/>"
        "<rect x='176' y='18' width='70' height='34' rx='8' fill='#2f3a44'/>"
        f"<rect x='186' y='24' width='50' height='10' rx='5' fill='{acento}'/>"
        "<rect x='140' y='8' width='14' height='44' rx='7' fill='#c58a4a'/><rect x='262' y='8' width='14' height='44' rx='7' fill='#c58a4a'/>"
        "<rect x='92' y='214' width='56' height='14' rx='5' fill='#2f3a44'/><rect x='252' y='214' width='56' height='14' rx='5' fill='#2f3a44'/>"
        f"<rect x='150' y='118' width='100' height='40' rx='8' fill='white' opacity='.9'/><rect x='162' y='132' width='76' height='7' rx='3.5' fill='{acento}' opacity='.8'/>")


def geladeira(acento):
    return _uri(
        "<ellipse cx='200' cy='244' rx='90' ry='8' fill='#000' opacity='.07'/>"
        f"<rect x='128' y='8' width='144' height='232' rx='16' fill='{CINZA}' stroke='{BORDA}' stroke-width='3'/>"
        f"<line x1='128' y1='92' x2='272' y2='92' stroke='{BORDA}' stroke-width='3'/>"
        f"<rect x='140' y='38' width='8' height='38' rx='4' fill='{acento}' opacity='.8'/>"
        f"<rect x='140' y='114' width='8' height='78' rx='4' fill='{acento}' opacity='.8'/>"
        "<rect x='176' y='22' width='70' height='8' rx='4' fill='#d4dae0'/>", 400, 252)


def freezer(acento):
    return _uri(
        "<ellipse cx='200' cy='244' rx='80' ry='8' fill='#000' opacity='.07'/>"
        f"<rect x='140' y='8' width='120' height='232' rx='14' fill='{CINZA}' stroke='{BORDA}' stroke-width='3'/>"
        + ''.join(f"<line x1='140' y1='{y}' x2='260' y2='{y}' stroke='{BORDA}' stroke-width='3'/>" for y in (80, 152)) +
        ''.join(f"<rect x='178' y='{y}' width='44' height='8' rx='4' fill='{acento}' opacity='.8'/>" for y in (38, 110, 190)), 400, 252)


def controle(acento):
    return _uri(
        "<ellipse cx='200' cy='238' rx='60' ry='7' fill='#000' opacity='.07'/>"
        f"<rect x='158' y='8' width='84' height='228' rx='26' fill='{CINZA}' stroke='{BORDA}' stroke-width='3'/>"
        "<rect x='172' y='24' width='56' height='36' rx='7' fill='#2b3640'/>"
        "<rect x='182' y='34' width='26' height='6' rx='3' fill='#8fd3ff'/><rect x='182' y='46' width='16' height='5' rx='2.5' fill='#8fd3ff' opacity='.6'/>"
        f"<circle cx='200' cy='88' r='13' fill='{acento}'/>"
        "<g fill='#d4dae0'><circle cx='178' cy='128' r='10'/><circle cx='222' cy='128' r='10'/><circle cx='178' cy='162' r='10'/>"
        "<circle cx='222' cy='162' r='10'/><rect x='172' y='192' width='56' height='16' rx='8'/></g>", 400, 246)


DESENHO = {'hiwall': hiwall, 'cassete': cassete, 'pisoteto': pisoteto, 'compressor': compressor,
           'geladeira': geladeira, 'freezer': freezer, 'controle': controle}

if __name__ == '__main__':
    import sys
    # uso: python3 ilustracoes.py PASTA  -> grava os SVGs de cada desenho para conferir (convert/navegador)
    import os, urllib.parse as up
    pasta = sys.argv[1] if len(sys.argv) > 1 else '.'
    os.makedirs(pasta, exist_ok=True)
    for nome, fn in DESENHO.items():
        uri = fn('#2563eb')
        svg = up.unquote(uri.split(',', 1)[1])
        with open(os.path.join(pasta, f'{nome}.svg'), 'w', encoding='utf8') as f:
            f.write(svg)
        print(nome, len(uri), 'bytes')
