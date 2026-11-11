#!/usr/bin/env python3
"""Prévia do ritmo na GRAVAÇÃO com a máquina cheia (T1, novembro: ~30 tarefas na fila da trava). O prever.py --ens usa as durações
do ensaio rápido, que saem bem menores que as da gravação: na gravação do T1 cap00/cap01 o deslocamento do cursor levou 0,8 a 1,9 s
(ensaio: 0,5 a 0,9), o clique 1,2 a 2,4 s e cada letra ~0,1 s a mais que o `cps` pede. Aqui a duração de cada passo é a do ensaio
rápido esticada por esses custos (ou a da última gravação, com --grav). Mostra os passos com atraso previsto >= LIMIAR.
Uso: python3 -I rec/t01/t01_carga.py 02 03 ... [--grav] [--tudo]"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LETRAS = {'$TUT_USER': 31, '$TUT_SENHA': 13}
LIMIAR = 0.5


def medidas(nn, grav):
    p = f'{HERE}/t01-cap{nn}.actions.json' if grav else f'{HERE}/_ens/t01-cap{nn}.actions.json'
    if not os.path.exists(p):
        return {}
    a = json.load(open(p))
    m = {}
    for x in a['actions'] if isinstance(a, dict) else a:
        m.setdefault((x.get('do'), x.get('label')), []).append(x)
    return m


def custo(st, med, grav):
    d = st.get('do')
    if d == 'mark':
        return 0.0
    x = med.get((d, st.get('label')), [None]).pop(0) if med.get((d, st.get('label'))) else None
    if grav and x and x.get('tEnd') is not None:
        return x['tEnd'] - x['tStart']
    mov = (x['tAct'] - x['tStart']) if x and x.get('tAct') is not None else None
    tot = (x['tEnd'] - x['tStart']) if x and x.get('tEnd') is not None else None
    if d == 'hover':
        return max(1.0, (mov or 0.6) + 0.55) + st.get('seconds', 0.9)
    if d in ('click', 'dblclick', 'rightclick'):
        return max(1.45, (tot or 0.9) + 0.5)
    if d == 'type':
        n = LETRAS.get(st.get('text', ''), len(st.get('text', '')))
        cps = st.get('cps') or 9
        pre = 0.35 if st.get('noClick') or not st.get('target') else max(1.6, (mov or 1.1) + 0.5)
        return pre + n * (1.45 / cps + 0.11) + (0.45 if st.get('clear') else 0)
    if d == 'scroll':
        return max(1.0, (tot or 0.8) * 1.3)
    if d == 'press':
        return max(0.4, (tot or 0.3) * 1.3)
    return (tot or 0.1) * 1.3   # eval, waitFor, upload...


def simula(nn, grav, tudo):
    s = json.load(open(f'{HERE}/cap{nn}.json'))
    med = medidas(nn, grav)
    t = 0.0
    pior = (0.0, '')
    linhas = []
    for st in s['steps']:
        at = st.get('at')
        ini = max(t, at) if at is not None else t
        dur = custo(st, med, grav)
        late = ini - at if at is not None else 0.0
        if late > pior[0]:
            pior = (late, st.get('label') or st.get('name') or st.get('do'))
        if tudo or late >= LIMIAR:
            linhas.append(f'  {ini:7.2f}->{ini + dur:7.2f} at={at if at is not None else "-":>6} {st.get("do"):7} '
                          f'{(st.get("label") or st.get("name") or "")[:52]}' + (f'  <-- {late:.2f}' if late >= LIMIAR else ''))
        t = ini + dur
    print(f'cap{nn}: pior atraso {pior[0]:.2f} s em "{pior[1]}"')
    for l in linhas:
        print(l)


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    for nn in args:
        simula(f'{int(nn):02d}', '--grav' in sys.argv, '--tudo' in sys.argv)
