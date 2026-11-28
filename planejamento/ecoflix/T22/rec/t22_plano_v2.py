#!/usr/bin/env python3
"""T22 · planeja respiros (pausas_fino.py) a partir do resumo da gravação final: onde o atraso do gesto SALTA (passo lento), põe o silêncio no
último limite de frase (vão entre duas palavras >= 0,08 s) ANTES do passo atrasado, para a fala esperar o passo lento. Sem limite nesse
intervalo, usa o primeiro depois. uso: python3 -I rec/t22/t22_plano_v2.py NN [--salto 0.4] -> 'T:DUR T:DUR' (tempos da narração ORIGINAL)"""
import json, os, re, sys
H = os.path.dirname(os.path.abspath(__file__)); TUT = os.path.dirname(os.path.dirname(H))
nn = f'{int(sys.argv[1]):02d}'; salto = float(sys.argv[sys.argv.index('--salto') + 1]) if '--salto' in sys.argv else 0.4
orig = os.path.join(TUT, 't22/narracao/emendas', f'cap{nn}.orig.json'); cur = os.path.join(TUT, 't22/narracao', f'cap{nn}.json')
D = json.load(open(orig if os.path.exists(orig) else cur))
W = D['words']
lim = []   # limites de frase: ponto no meio do vão entre duas palavras
for a, b in zip(W, W[1:]):
    if b['s'] - a['e'] >= 0.08 and re.search(r'[.,:;!?]$', a['w']):
        lim.append(round((a['e'] + b['s']) / 2, 2))
A = json.load(open(os.path.join(H, f't22-cap{nn}.actions.json')))['actions']
passos = [(x['at'], max(0.0, x['tStart'] - x['at'])) for x in A if x.get('at') is not None]
saida = []; prev_late = 0.0; prev_at = 0.0
for at, late in passos:
    j = late - prev_late
    if j > salto:
        dur = round(j - 0.2, 1)
        antes = [g for g in lim if prev_at < g < at - 0.05]
        g = antes[-1] if antes else next((g for g in lim if g >= at), None)
        if g is not None and dur >= 0.4: saida.append((g, dur))
    prev_late = late; prev_at = at
# junta pontos iguais
acc = {}
for g, d in saida: acc[g] = round(acc.get(g, 0) + d, 1)
print(' '.join(f'{g}:{d}' for g, d in sorted(acc.items())))
