#!/usr/bin/env python3
"""T13 · conferência de um ensaio/gravação pelo actions.json: valor devolvido pelos `eval` (SEM ALVO, SEM ROLAGEM, DIFERENTE, avisos de
erro na tela), passos falhos, passos lentos (gesto > 1,3 s depois do início: rolagem que o robô fez sozinho) e, na gravação completa, os
atrasos (lateBy >= 0,3 s) com a palavra falada no instante do gesto.
Uso: python3 -I rec/t13/t13_confere.py NN [--ens]"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
nn = f'{int(sys.argv[1]):02d}'
pasta = os.path.join(HERE, '_ens') if '--ens' in sys.argv else HERE
a = json.load(open(os.path.join(pasta, f't13-cap{nn}.actions.json'), encoding='utf8'))
acts = a['actions']
nar = json.load(open(os.path.join(HERE, '..', '..', 't13', 'narracao', f'cap{nn}.json'), encoding='utf8'))


def voz(t):
    ant = [w for w in nar['words'] if w['s'] <= t + 0.05]
    return ant[-1]['w'] if ant else ''


ruins = 0
for x in acts:
    lab = x.get('label') or x.get('name') or ''
    if x.get('error') or x.get('ok') is False:
        ruins += 1
        print(f'FALHO  {x.get("do")} {lab}: {str(x.get("error"))[:160]}')
    if x.get('do') == 'eval':
        v = str(x.get('value'))
        if any(k in v for k in ('SEM ALVO', 'SEM ROLAGEM', 'DIFERENTE')) or (lab == 'avisos de erro na tela' and v not in ('[]', '"[]"')):
            ruins += 1
            print(f'VALOR  {lab} => {v[:200]}')
    if x.get('do') not in ('mark', 'eval', 'wait', 'pause', 'waitFor') and x.get('tAct') and x['tAct'] - x['tStart'] > 1.3:
        print(f'lento  {x.get("do")} {lab}: {x["tAct"] - x["tStart"]:.2f} s')
    if (x.get('lateBy') or 0) >= 0.3:
        print(f'atraso {x.get("lateBy"):.2f} s  {x.get("do")} {lab}  (voz: {voz(x.get("tAct") or x["tStart"])})')
pi = a.get('pageIssues') or {}
problemas = {k: len(v) for k, v in pi.items() if v}
print(f'cap{nn}: {len(acts)} passos, falhos/valores ruins {ruins}, maxLate {max([x.get("lateBy") or 0 for x in acts] or [0]):.2f}, pageIssues {problemas or "vazio"}')
