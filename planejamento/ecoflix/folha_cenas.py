#!/usr/bin/env python3
"""Folha para o Kaik revisar as ilustrações de uma aula: o quadro final de cada cena (tudo já na tela), grande, com o
capítulo e o resumo da cena. Usa os tempos estimados da aula e o render_cenas.cjs (trava leve .stills.lock + nice 19, um capítulo por vez).
uso: python3 -I planejamento/ecoflix/folha_cenas.py T07 [T04 ...]   ->  /home/claude/ecoflix/previa_ilustracoes/Tnn_cenas.jpg"""
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata

from PIL import Image, ImageDraw, ImageFont

SKILL = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
RENDER = os.path.join(SKILL, 'ferramentas', 'edit', 'cenas', 'render_cenas.cjs')
FONTES = os.path.join(SKILL, 'ferramentas', 'kit', 'fonts')
TRAVA = '/home/claude/ecoflix/.stills.lock'  # quadros: trava leve própria + nice 19 (não disputa com a gravação)
SAIDA = '/home/claude/ecoflix/previa_ilustracoes'
TW, TH, COLS, PAD, LEG = 960, 600, 2, 24, 64


def norm(s):
    s = unicodedata.normalize('NFC', s.lower())
    return re.sub(r'[^\w]', '', s)


def fim_da_palavra(cap, linha, palavra, ocorr):
    alvo, n = norm(palavra), 0
    for w in cap['words']:
        if w['linha'] == linha and norm(w['w']) == alvo:
            n += 1
            if n == ocorr:
                return w['e']
    linhas = [l for l in cap['linhas'] if l['i'] == linha]
    return linhas[0]['e'] if linhas else cap['dur'] - 0.5


def fonte(peso, px):
    return ImageFont.truetype(os.path.join(FONTES, f'Montserrat-{peso}.ttf'), px)


def aula(A):
    N = A[1:] if A[0] in 'Tt' else A
    pasta = os.path.join(SKILL, 'planejamento', 'ecoflix', 'T' + N, 'cenas')
    cenas = json.load(open(os.path.join(pasta, 'ilustracoes.json'), encoding='utf-8'))
    tmp = f'/dev/shm/folha_cenas_T{N}'
    os.makedirs(tmp, exist_ok=True)
    quadros = []  # (cena, caminho do jpg)
    por_cap = {}
    for c in cenas:
        por_cap.setdefault(c['cap'], []).append(c)
    for cap_n, lista in sorted(por_cap.items()):
        tempos = os.path.join(pasta, 'tempos', f'cap{cap_n:02d}.json')
        cap = json.load(open(tempos, encoding='utf-8'))
        ts = []
        for c in lista:
            l, p, o = (c['ate'] + [1])[:3]
            t = fim_da_palavra(cap, l, p, o) + min(float(c.get('cauda', 0.6)), 0.5) - 0.05
            ts.append(round(t, 2))
        cmd = ['flock', TRAVA, 'nice', '-n', '19', 'timeout', '300', 'node', RENDER, str(cap_n), tempos, 'q', '--html',
               os.path.join(pasta, 'cenas.html'), '--stills', ','.join(f'{t:.2f}' for t in ts)]
        r = subprocess.run(cmd, cwd=tmp, capture_output=True, text=True)
        if r.returncode:
            print(f'T{N} cap{cap_n:02d}: render falhou ({r.returncode}) {r.stderr[-300:]}', file=sys.stderr)
            continue
        for c, t in zip(lista, ts):
            quadros.append((c, os.path.join(tmp, 'q', f'cap{cap_n:02d}_{t:.2f}.jpg')))
    linhas = (len(quadros) + COLS - 1) // COLS
    W = COLS * TW + (COLS + 1) * PAD
    H = 90 + linhas * (TH + LEG + PAD) + PAD
    folha = Image.new('RGB', (W, H), '#121212')
    d = ImageDraw.Draw(folha)
    d.text((PAD, 28), f'EcoFlix · T{N} · {len(quadros)} cenas (quadro final de cada uma)', font=fonte(700, 34), fill='#F3F4F6')
    f_leg, f_cap = fonte(500, 21), fonte(700, 21)
    for i, (c, img) in enumerate(quadros):
        x = PAD + (i % COLS) * (TW + PAD)
        y = 90 + (i // COLS) * (TH + LEG + PAD)
        rotulo = f"cap{c['cap']:02d}"
        d.text((x, y + 6), rotulo, font=f_cap, fill='#50D088')
        resumo = c.get('resumo', '')
        larg = TW - d.textlength(rotulo + '  ', font=f_cap)
        while resumo and d.textlength(resumo, font=f_leg) > larg:
            resumo = resumo[:-2].rstrip() + '…' if not resumo.endswith('…') else resumo[:-3].rstrip() + '…'
        d.text((x + d.textlength(rotulo + '  ', font=f_cap), y + 6), resumo, font=f_leg, fill='#C9CDD2')
        if os.path.exists(img):
            folha.paste(Image.open(img).convert('RGB').resize((TW, TH), Image.LANCZOS), (x, y + LEG - 22))
    os.makedirs(SAIDA, exist_ok=True)
    out = os.path.join(SAIDA, f'T{N}_cenas.jpg')
    folha.save(out, quality=82, optimize=True)
    shutil.rmtree(tmp, ignore_errors=True)
    print(f'{out}: {len(quadros)} cenas, {os.path.getsize(out) / 1e6:.1f} MB')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for a in sys.argv[1:]:
        aula(a)
