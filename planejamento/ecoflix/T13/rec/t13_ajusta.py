#!/usr/bin/env python3
"""T13 · ajuste de um capítulo antes da regravação: respiros nos vãos REAIS (pausas.py) escolhidos por simulação + antecipação (t13_retime.py).
Para cada passo atrasado (>= --lim no previsto, com as durações medidas em _med/), testa cada vão de silêncio real (áudio < -55 dB, entre duas
palavras) antes dele com respiro de atraso+0,1 s e fica com o que mais baixa o pior atraso. Imprime os pontos T:DUR (tempo ORIGINAL).
Uso: python3 -I rec/t13/t13_ajusta.py NN [--lim 0.55] [--max 8] [--zerar]"""
import json, os, shutil, subprocess, sys
import numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__)); TUT = os.path.normpath(os.path.join(HERE, '..', '..'))
NARR = os.path.join(TUT, 't13', 'narracao')
sys.path.insert(0, HERE)
import t13_plano_pausas as PL  # noqa

nn = f'{int(sys.argv[1]):02d}'
lim = float(sys.argv[sys.argv.index('--lim') + 1]) if '--lim' in sys.argv else 0.55
maxit = int(sys.argv[sys.argv.index('--max') + 1]) if '--max' in sys.argv else 8
orig_p = os.path.join(NARR, 'emendas', f'cap{nn}.orig.json')
os.makedirs(os.path.dirname(orig_p), exist_ok=True)
if not os.path.exists(orig_p):
    shutil.copy2(os.path.join(NARR, f'cap{nn}.json'), orig_p)
orig = json.load(open(orig_p)); W = orig['words']


def silencios():
    x, sr = sf.read(os.path.join(orig['pasta'].rstrip('/'), 'audio48k.wav'), dtype='float32')
    x = x.mean(1) if x.ndim == 2 else x
    q = int(sr * 0.01); n = len(x) // q
    db = 20 * np.log10(np.sqrt((x[:n * q].reshape(n, q) ** 2).mean(1)) + 1e-9); mudo = db < -55
    g, i = [], 0
    while i < n:
        if mudo[i]:
            j = i
            while j < n and mudo[j]: j += 1
            lo, hi = i * 0.01, j * 0.01
            if hi - lo >= 0.08:
                for w in W:
                    if w['s'] < hi and w['e'] > lo:
                        if w['s'] <= lo: lo = max(lo, w['e'])
                        elif w['e'] >= hi: hi = min(hi, w['s'])
                        else: lo, hi = 1, 0
                if hi - lo >= 0.03: g.append(round((lo + hi) / 2, 3))
            i = j
        else:
            i += 1
    return g


GAPS = silencios()


def roda(pts):
    if pts:
        PL.abre_vao(nn, orig_p, list(pts))
    PL.aplica(nn, pts, orig_p)
    subprocess.run(['python3', '-I', os.path.join(HERE, 'gerar.py'), nn], check=True, capture_output=True)
    subprocess.run(['python3', '-I', os.path.join(HERE, 't13_retime.py'), nn], check=True, capture_output=True)
    sim, fim = PL.simula(nn)
    return sim, fim


pts = {}
sim, fim = roda(pts)
sem = set()
for _ in range(maxit):
    pior = max(s[3] for s in sim)
    ruins = [i for i, s in enumerate(sim) if s[3] >= lim and i not in sem]
    if not ruins:
        break
    i = ruins[0]; at = sim[i][2]; atr = sim[i][3]
    mp = lambda x, p: x + sum(b for a, b in p.items() if x >= a - 1e-9)
    melhor = None
    for g in GAPS:
        if not (at - 10 < mp(g, pts) <= at + 0.7): continue
        p2 = dict(pts); p2[g] = round(p2.get(g, 0) + atr + 0.1, 2)
        try:
            s2, f2 = roda(p2)
        except SystemExit:
            continue
        v = (round(max(s[3] for s in s2), 2), -g)   # menor pior atraso; empate: o vão mais tardio
        if melhor is None or v < melhor[0]:
            melhor = (v, p2, s2, f2)
    if melhor is None or melhor[0][0] >= pior - 0.05:
        sem.add(i); sim, fim = roda(pts); print(f'cap{nn}: sem vão que ajude em {sim[i][0].get("label") or sim[i][0].get("name")!r} (at {at}, atraso {atr:.2f})')
        continue
    pts, sim, fim = melhor[1], melhor[2], melhor[3]
sim, fim = roda(pts)
print(f'cap{nn}: respiros ' + (' '.join(f'{a}:{b}' for a, b in sorted(pts.items())) or '-') + f' | pior atraso previsto {max(s[3] for s in sim):.2f} | fim da fala {fim:.1f} s')
