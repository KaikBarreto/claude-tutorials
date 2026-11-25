"""T04 · propõe os respiros (pausas.py) de um capítulo a partir da gravação final: cada trecho em que o gesto atrasa (lateBy >= LIM) vira um
respiro no vão de silêncio (vad) imediatamente ANTES do primeiro passo atrasado (T na linha do tempo ORIGINAL), com DUR = maior atraso do
trecho + folga. Só imprime os argumentos de `pausas.py NN T:DUR ...`. Uso: python3 -I rec/t04/t04_respiros.py NN [LIM=0.5]"""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); TUT = os.path.dirname(os.path.dirname(H))
nn = f'{int(sys.argv[1]):02d}'; LIM = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5
a = json.load(open(os.path.join(H, f't04-cap{nn}.actions.json')))['actions']
d = json.load(open(os.path.join(TUT, 't04', 'narracao', f'cap{nn}.json'))); vad = d['vad']
gaps = [((vad[i][1] + vad[i + 1][0]) / 2, vad[i + 1][0] - vad[i][1]) for i in range(len(vad) - 1)]
out = []; prev = 0.0; soma = {}
for x in a:
    L = x.get('lateBy')
    if x.get('at') is None or L is None: continue
    inc = L - prev
    if L >= LIM and inc >= 0.4:
        cand = [g for g in gaps if g[0] <= x['at'] + 0.05]
        if not cand: out.append(f'# passo {x["i"]} (at {x["at"]:.2f}, atraso {L:.2f}): sem vão antes (início do capítulo)')
        else:
            g = cand[-1]; soma[g[0]] = soma.get(g[0], 0) + inc + 0.15
            out.append(f'#   passo {x["i"]} (at {x["at"]:.2f}) atraso {L:.2f} (+{inc:.2f}) -> vão {g[0]:.2f} ({g[1]:.2f} s)')
    prev = L
out.append(' '.join(f'{t:.2f}:{dur:.2f}' for t, dur in sorted(soma.items())))
print('\n'.join(out))
