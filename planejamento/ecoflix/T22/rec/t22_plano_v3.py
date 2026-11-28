#!/usr/bin/env python3
"""T22 · 2ª rodada de respiros: lê a gravação ATUAL (actions.json, narração já com respiros) e acha onde o atraso do gesto SALTA; o silêncio vai
num vão entre palavras (>= 0,12 s) ANTES do passo (janela: do `at` do passo de 2 atrás até o `at` do passo atrasado; prefere vão com pontuação,
senão o último vão). Imprime TODOS os pontos (os que já existem + os novos) em tempo ORIGINAL, prontos para o pausas_fino.py.
uso: python3 -I rec/t22/t22_plano_v3.py NN [--salto 0.3]"""
import json, os, re, sys
H = os.path.dirname(os.path.abspath(__file__)); TUT = os.path.dirname(os.path.dirname(H))
nn = f'{int(sys.argv[1]):02d}'; salto = float(sys.argv[sys.argv.index('--salto') + 1]) if '--salto' in sys.argv else 0.3
D = json.load(open(os.path.join(TUT, 't22/narracao', f'cap{nn}.json'))); W = D['words']
lim = []
for a, b in zip(W, W[1:]):
    if b['s'] - a['e'] >= 0.12: lim.append((round((a['e'] + b['s']) / 2, 2), bool(re.search(r'[.,:;!?]$', a['w']))))
A = json.load(open(os.path.join(H, f't22-cap{nn}.actions.json')))['actions']
P = [(x['at'], max(0.0, x['tStart'] - x['at'])) for x in A if x.get('at') is not None]
novos = []; pl = 0.0
for i, (at, late) in enumerate(P):
    j = late - pl
    if j > salto:
        dur = round(j - 0.1, 1)
        ini = P[i - 2][0] if i >= 2 else 0.0
        jan = [(g, p) for g, p in lim if ini < g < at - 0.05]
        pont = [g for g, p in jan if p]
        g = pont[-1] if pont else (jan[-1][0] if jan else next((g for g, p in lim if g >= at), None))
        if g is not None and dur >= 0.3: novos.append((g, dur))
    pl = late
ex = sorted([list(x) for x in D.get('pausas', [])]); acum = 0.0; blocos = []
for a, b in ex: blocos.append((a + acum, a + acum + b)); acum += b
res = [list(x) for x in ex]
for g, dur in novos:
    em = next((k for k, (x0, x1) in enumerate(blocos) if x0 - 0.15 <= g <= x1 + 0.15), None)
    if em is not None: res[em][1] = round(res[em][1] + dur, 1); continue
    desl = sum(b for (x0, x1), (_, b) in zip(blocos, ex) if x1 <= g + 0.01)
    res.append([round(g - desl, 2), dur])
res.sort()
m = {}
for t, d in res: m[t] = round(m.get(t, 0) + d, 1)
res = sorted([t, d] for t, d in m.items())
print(' '.join(f'{t}:{d}' for t, d in res) if novos else '')
