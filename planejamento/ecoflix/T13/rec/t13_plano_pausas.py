#!/usr/bin/env python3
"""T13 · planeja os respiros (pausas.py) de um capítulo a partir das durações MEDIDAS na gravação final (rec/t13/_med/).
Simula o robô como o prever.py (início = max(fim do anterior, at)), acha o primeiro passo com atraso >= LIM e põe um respiro de
atraso+0,1 s no último vão REAL de silêncio da voz original antes da palavra do passo (e depois do último passo pontual); repete até
nenhum passo passar do limite. Imprime os pontos T:DUR (tempo ORIGINAL) e, com --aplicar, roda pausas.py e gerar.py.
Uso: python3 -I rec/t13/t13_plano_pausas.py NN [--lim 0.5] [--aplicar]"""
import json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); TUT = os.path.normpath(os.path.join(HERE, '..', '..'))
NARR = os.path.join(TUT, 't13', 'narracao')
sys.path.insert(0, HERE)
import prever as P


def med_de(nn):
    return json.load(open(os.path.join(HERE, '_med', f't13-cap{nn}.actions.json')))['actions']


def simula(nn):
    rot = json.load(open(os.path.join(HERE, f'cap{nn}.json'), encoding='utf8'))
    med = [m for m in med_de(nn) if m.get('do') != 'mark']
    j, t, out = 0, 0.0, []
    for st in rot['steps']:
        at = st.get('at'); ini = max(t, at) if at is not None else t
        if st.get('do') == 'mark':
            dur = 0.0
        else:
            m = None
            for k in range(j, min(len(med), j + 8)):
                if med[k].get('do') == st.get('do') and (med[k].get('label') or '') == (st.get('label') or ''):
                    m, j = med[k], k + 1; break
            if m is None or st.get('do') in ('pause', 'wait'):
                dur = P.modelo(st, rot.get('cps') or 9)
            elif st.get('do') == 'type':
                dur = ((m.get('tAct') or m['tStart']) - m['tStart']) + P.digitacao(st, rot.get('cps') or 9)
            elif st.get('do') == 'hover' and m.get('tAct') is not None:
                dur = (m['tAct'] - m['tStart']) + st.get('seconds', 0.9)
            else:
                dur = m['tEnd'] - m['tStart']
        out.append((st, ini, at, (ini - at) if at is not None else 0.0))
        t = ini + dur
    return out, t


def aplica(nn, pts, orig_p):
    pa = os.path.join(NARR, 'pausas.py')
    if pts:
        r = subprocess.run(['python3', '-I', pa, nn] + [f'{a}:{b}' for a, b in sorted(pts.items())], capture_output=True, text=True)
    elif os.path.exists(orig_p):
        r = subprocess.run(['python3', '-I', pa, nn, '--desfazer'], capture_output=True, text=True)
    else:
        return
    if r.returncode != 0:
        sys.exit(f'pausas.py cap{nn} falhou (código {r.returncode}): {r.stdout[-300:]} {r.stderr[-300:]}')


def main():
    nn = f'{int(sys.argv[1]):02d}'
    lim = float(sys.argv[sys.argv.index('--lim') + 1]) if '--lim' in sys.argv else 0.5
    aplicar = '--aplicar' in sys.argv
    orig_p = os.path.join(NARR, 'emendas', f'cap{nn}.orig.json')
    orig = json.load(open(orig_p if os.path.exists(orig_p) else os.path.join(NARR, f'cap{nn}.json')))
    vad = orig['vad']; frases = orig['frases']
    gaps = [((a1 + b0) / 2, b0 - a1) for (a0, a1), (b0, b1) in zip(vad, vad[1:]) if b0 - a1 >= 0.1]
    fr_fins = [f['e'] for f in frases]
    pts = {}
    for _ in range(12):
        aplica(nn, pts, orig_p)
        subprocess.run(['python3', '-I', os.path.join(HERE, 'gerar.py'), nn], check=True, capture_output=True)
        sim, fim = simula(nn)
        mp = lambda x: x + sum(b for a, b in pts.items() if x >= a - 1e-9)
        ruim = next((i for i, (st, ini, at, atr) in enumerate(sim) if atr >= lim), None)
        if ruim is None:
            break
        st, ini, at, atr = sim[ruim]
        ant = max([s[2] for s in sim[:ruim] if s[2] is not None and s[3] < 0.15 and s[0].get('do') != 'mark'] or [0])
        # janela: depois do último passo pontual, até um pouco depois do `at` do passo ruim
        cand = [(g, w) for g, w in gaps if mp(g) > ant + 0.05 and mp(g) <= at + 0.7]
        if not cand:
            print(f'cap{nn}: SEM VÃO para o passo {st.get("label") or st.get("name")!r} (at {at}, atraso {atr:.2f}); janela ({ant:.2f}, {at + 0.7:.2f}]')
            break
        fr = [(g, w) for g, w in cand if min(abs(g - e) for e in fr_fins) < 0.4]
        g, w = (fr or cand)[-1]
        g = round(g, 3); pts[g] = round(pts.get(g, 0) + atr + 0.1, 2)
    print(f'cap{nn}: pontos ' + ' '.join(f'{a}:{b}' for a, b in sorted(pts.items())) + f' | previsto: pior atraso {max(s[3] for s in sim):.2f}, fim {fim:.1f} s')
    if not aplicar:
        aplica(nn, {}, orig_p)
        subprocess.run(['python3', '-I', os.path.join(HERE, 'gerar.py'), nn], check=True, capture_output=True)


main()
