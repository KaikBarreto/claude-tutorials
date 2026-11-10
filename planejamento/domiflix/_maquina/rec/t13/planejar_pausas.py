#!/usr/bin/env python3
"""T13 · planeja as pausas de voz (pausas.py) a partir dos atrasos medidos na gravação: para cada linha da fala, o maior atraso de passo dentro dela
(menos o que as pausas anteriores já cobrem + 0,3 s de folga) vira silêncio no vão entre a linha anterior e ela. Só entre frases.
uso: python3 -I rec/t13/planejar_pausas.py NN [NN ...] [--aplicar]   (lê rec/t13/t13-capNN.actions.json e t13/narracao/capNN.json; não mexa depois de aplicar sem --desfazer)"""
import json, os, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); NARR = os.path.join(H, '..', '..', 't13', 'narracao')
aplicar = '--aplicar' in sys.argv
for n in [int(a) for a in sys.argv[1:] if a.isdigit()]:
    d = json.load(open(f'{NARR}/cap{n:02d}.json')); L = d['linhas']
    a = json.load(open(f'{H}/t13-cap{n:02d}.actions.json'))['actions']
    por_linha = {}
    for x in a:
        late = x.get('lateBy') or 0
        if late < 0.5 or x.get('do') == 'eval':
            continue
        nm = x.get('name') or ''
        if x.get('do') == 'mark' and nm[:1] == 'L' and nm[1:].isdigit():
            k = int(nm[1:]) - 1
        else:
            at = (x.get('tAct') or x.get('tStart') or 0) - late
            k = max([i for i, l in enumerate(L) if l['s'] - 0.4 <= at] or [0])
        por_linha[k] = max(por_linha.get(k, 0), late)
    cum, plano = 0.0, []
    for k in sorted(por_linha):
        if k == 0:
            continue
        need = por_linha[k] - cum + 0.3
        if need <= 0.3:
            continue
        need = round(need, 1)
        fim_ant = max(w['e'] for w in d['words'] if w['linha'] == k - 1)
        ini = min(w['s'] for w in d['words'] if w['linha'] == k)
        T = round((fim_ant + ini) / 2, 2)
        plano.append((k + 1, T, need)); cum += need
    print(f'cap{n:02d}: ' + (' '.join(f'L{k}@{T}:{D}' for k, T, D in plano) or 'sem pausa'))
    if aplicar and plano:
        subprocess.run(['python3', '-I', 'pausas.py', f'{n:02d}'] + [f'{T}:{D}' for _, T, D in plano], cwd=NARR, check=True)
