#!/usr/bin/env python3
"""Estilo saturado nas cenas da EcoFlix (pedido do Kaik, 11/11): selo, chip, etiqueta, quadrado atrás de ícone e círculo de
etapa com FUNDO CHEIO e ícone/texto BRANCO (cores da marca, escolha do Kaik às 13:03: verde #50D088) (antes: fundo claro com ícone ou texto colorido, e ícone escuro sobre o verde).
Põe um bloco <style id="saturado"> no fim do <head> de cada cenas.html (vale sobre as classes do kit .ico, .ico.a, .tag.v,
.tag.a e sobre o que usar var(--vs)/var(--as)/var(--rs); estilo inline da aula continua valendo) e lista o que ainda usa
tom claro com conteúdo colorido, para conferir à mão.
uso: python3 -I planejamento/ecoflix/estilo_saturado.py [--verde #50D088] [--ambar #F2B63D] [--vermelho #EF4444] [T00 T01 ...]
     sem aulas: o kit (perfis/ecoflix/cenas/cenas_ecoflix.html) e todas as Tnn/cenas/cenas.html"""
import glob
import os
import re
import sys

SKILL = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
args = sys.argv[1:]
opt = lambda k, d: args[args.index(k) + 1] if k in args else d  # noqa: E731
VERDE, AMBAR, VERM = opt('--verde', '#50D088'), opt('--ambar', '#F2B63D'), opt('--vermelho', '#EF4444')
aulas = [a for i, a in enumerate(args) if re.fullmatch(r'[Tt]\d\d', a)]
BLOCO = ('<style id="saturado">/* estilo saturado (Kaik, 11/11): selo, chip, etiqueta, quadrado de ícone e círculo de etapa\n'
         '   com fundo cheio e ícone/texto branco; nunca fundo claro com conteúdo colorido, nunca ícone escuro sobre o verde */\n'
         f':root{{--vs:{VERDE};--as:{AMBAR};--rs:{VERM}}}\n'
         '.ico{background:var(--vs);color:#fff}.ico.a{background:var(--as);color:#fff}\n'
         '.tag.v{background:var(--vs);color:#fff}.tag.a{background:var(--as);color:#fff}\n</style>')
CLARO = re.compile(r'var\(--(?:vc|ac|vm)\)|#(?:EAF8F0|FFF5DF|E8F7EF|FDECEC|FEF3F2|ECFDF3|F0FDF4|FFF7E6|FEF6E7)\b', re.I)

arquivos = ([os.path.join(SKILL, 'planejamento', 'ecoflix', 'T' + a[1:], 'cenas', 'cenas.html') for a in aulas] if aulas else
            [os.path.join(SKILL, 'perfis', 'ecoflix', 'cenas', 'cenas_ecoflix.html')] +
            sorted(glob.glob(os.path.join(SKILL, 'planejamento', 'ecoflix', 'T*', 'cenas', 'cenas.html'))))
for f in arquivos:
    s = open(f, encoding='utf-8').read()
    s = re.sub(r'<style id="saturado">.*?</style>', '', s, flags=re.S)
    if s.count('</head>') != 1:
        print(f'{f}: sem </head> único, pulado'); continue
    s = s.replace('</head>', BLOCO + '</head>')
    open(f, 'w', encoding='utf-8').write(s)
    corpo = s.split('<style id="saturado">')[0]
    resto = [i + 1 for i, l in enumerate(corpo.split('\n')) if CLARO.search(l) and not re.search(r':root\{|^\.ico|^\.tag', l.strip())]
    print(f'{os.path.relpath(f, SKILL)}: bloco saturado posto; tom claro a conferir nas linhas {resto[:25]}{" ..." if len(resto) > 25 else ""}')
