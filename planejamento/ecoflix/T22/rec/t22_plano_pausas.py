#!/usr/bin/env python3
"""T22 · propõe respiros (pausas.py) a partir do resumo de uma gravação: onde o atraso do gesto cresce, um silêncio DEPOIS do trecho denso, num vão
real da fala (>= 0,2 s entre palavras) logo antes do passo atrasado. Lê rec/t22/capNN.resumo e t22/narracao/emendas/capNN.orig.json (ou capNN.json).
uso: python3 -I rec/t22/t22_plano_pausas.py NN [--alvo 0.3]  -> imprime 'T:DUR T:DUR ...' (vazio = nada a fazer)"""
import json, os, re, sys
H = os.path.dirname(os.path.abspath(__file__)); TUT = os.path.dirname(os.path.dirname(H))
nn = f'{int(sys.argv[1]):02d}'; alvo = float(sys.argv[sys.argv.index('--alvo') + 1]) if '--alvo' in sys.argv else 0.3
orig = os.path.join(TUT, 't22/narracao/emendas', f'cap{nn}.orig.json'); cur = os.path.join(TUT, 't22/narracao', f'cap{nn}.json')
D = json.load(open(cur))   # a linha do tempo da gravação = a atual (com os respiros já aplicados, se houver)
vad = D['vad']; gaps = [(round((a[1] + b[0]) / 2, 2), b[0] - a[1]) for a, b in zip(vad, vad[1:]) if b[0] - a[1] >= 0.12 and not any(w['s'] < (a[1] + b[0]) / 2 < w['e'] for w in D['words'])]   # vãos REAIS de silêncio, sem palavra no meio
R = re.compile(r'^\s*(\d+)\s+(\w+)\s+([\d.]+)->\s*([\d.]+) act\s+([\d.]+) late\s+([\d.]+)')
passos = []
for l in open(os.path.join(H, f'cap{nn}.resumo'), encoding='utf8'):
    m = R.match(l)
    if m: passos.append((float(m.group(3)) - float(m.group(6)), float(m.group(6))))   # (at original, atraso)
S = 0.0; saida = []
for g, _ in gaps:   # o atraso que o trecho acumulou ATÉ o vão sai no vão (o respiro vem DEPOIS do trecho denso)
    ant = [late for at, late in passos if at <= g]
    debito = (ant[-1] if ant else 0.0) - S
    if debito > 0.5:
        dur = round(debito - alvo, 1); saida.append((g, dur)); S += dur
# converte para a linha do tempo ORIGINAL (pausas.py recomeça sempre do original) e junta aos respiros que já existem
P = sorted([list(x) for x in D.get('pausas', [])]); acum = 0.0; blocos = []
for a, b in P: blocos.append((a + acum, a + acum + b, a)); acum += b
novos = [list(x) for x in P]
for g, dur in saida:
    em = next((i for i, (x0, x1, a) in enumerate(blocos) if x0 - 0.15 <= g <= x1 + 0.15), None)
    if em is not None: novos[em][1] = round(novos[em][1] + dur, 1); continue
    desl = sum(b for (x0, x1, a), (_, b) in zip(blocos, P) if x1 <= g + 0.01)
    novos.append([round(g - desl, 2), dur])
novos.sort()
print(' '.join(f'{t}:{d}' for t, d in novos) if saida else '')
