#!/usr/bin/env python3
"""T2 · resumo curto das gravações completas (rec/t02/t02-capNN.actions.json): falhos, maior atraso, pageIssues, avisos de erro,
conferências DIFERENTE e, para cada passo preso a uma palavra (`note` "Ln palavra" que o gerar.py põe), o instante do gesto (tAct)
menos o início da palavra na fala: perto de 0 = o gesto chega na palavra. Lista só o que passa de -0,6 s ou +0,6 s.
Uso: python3 -I rec/t02/t02_confere.py [NN ...] [--ens]"""
import json
import os
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
NARR = os.path.join(HERE, '..', '..', 't02', 'narracao')


def norm(x):
    x = unicodedata.normalize('NFD', x).encode('ascii', 'ignore').decode().lower()
    return ''.join(ch for ch in x if ch.isalnum())


ens = '--ens' in sys.argv
caps = [a for a in sys.argv[1:] if not a.startswith('--')] or [f'{n:02d}' for n in range(11)]
for c in caps:
    c = f'{int(c):02d}'
    p = os.path.join(HERE, '_ens' if ens else '', f't02-cap{c}.actions.json')
    if not os.path.exists(p):
        print(f'cap{c}: sem gravação')
        continue
    a = json.load(open(p))
    acts = a['actions']
    nar = json.load(open(os.path.join(NARR, f'cap{c}.json')))
    fails = [x for x in acts if x.get('error') or x.get('ok') is False]
    late = max([x.get('lateBy') or 0 for x in acts] or [0])
    pior = max(acts, key=lambda x: x.get('lateBy') or 0)
    pi = a.get('pageIssues') or {}
    ruido = lambda t: 'realtime/v1/websocket' in t or ' 406 ' in f' {t} '
    cons = [x for x in pi.get('console', []) if not ruido(x.get('text', ''))]
    bad = [b for b in pi.get('bad', []) if not ruido(str(b))]
    av = [x.get('value') for x in acts if x.get('label') == 'avisos de erro na tela']
    dif = [(x.get('label'), str(x.get('value'))[:160]) for x in acts if str(x.get('value', '')).startswith('DIFERENTE')]
    sem = [x.get('label') for x in acts if 'SEM ALVO' in str(x.get('value', ''))]
    print(f"cap{c}: {len(acts)} passos, vídeo {a.get('video', {}).get('durationS', '?')} s, falhos {len(fails)}, maior atraso {late:.2f} "
          f"({(pior.get('label') or pior.get('name') or '')[:40]}), pageErrors {len(pi.get('pageErrors', []))}, failed {len(pi.get('failed', []))}, "
          f"bad {len(bad)}, console {len(cons)}, avisos {av}, DIFERENTE {len(dif)}, SEM ALVO {len(sem)}")
    for x in fails:
        print('   FALHOU', x.get('i'), x.get('label'), str(x.get('error'))[:150])
    for l, v in dif:
        print('   DIFERENTE', l, v)
    for b in (cons + bad + pi.get('pageErrors', []) + pi.get('failed', []))[:4]:
        print('   pageIssue', str(b)[:160])
    for x in acts:
        n = x.get('note')
        if not n or x.get('skipped'):
            continue
        partes = n.split(' ')
        li, pal = int(partes[0][1:]), partes[1]
        nth = int(partes[2][1:]) if len(partes) > 2 else 0
        hits = [w for w in nar['words'] if w['linha'] == li - 1 and norm(w['w']) == norm(pal)]
        if len(hits) <= nth:
            print(f'   ? {n}: palavra fora da fala de hoje')
            continue
        t = x.get('tAct') or x.get('tEnd') or x.get('tStart')
        d = t - hits[nth]['s']
        if d < -0.6 or d > 0.6:
            print(f"   gesto {d:+.2f} s da palavra  {n:28} {x.get('do'):6} {(x.get('label') or '')[:50]}")
