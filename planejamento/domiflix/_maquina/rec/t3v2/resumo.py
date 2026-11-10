#!/usr/bin/env python3
"""Resumo de uma gravação do T3 v2: falhas, atrasos e, para cada passo, o instante do gesto (tAct) ao lado da palavra falada
naquele momento. Uso: python3 rec/t3v2/resumo.py NN [--tudo]"""
import json, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
n = int(sys.argv[1]); tudo = '--tudo' in sys.argv
a = json.load(open(f'{HERE}/t3v2-cap{n:02d}.actions.json'))
nar = json.load(open(f'{HERE}/../../t3v2/narracao/cap{n:02d}.json'))
words = nar['words']
def palavra(t):
    ant = [w for w in words if w['s'] <= t + 0.05]
    return ant[-1]['w'] if ant else ''
acts = a['actions']
fails = [x for x in acts if x.get('error') or x.get('ok') is False]
late = [x for x in acts if (x.get('lateBy') or 0) >= 0.3]
pi = a.get('pageIssues') or {}
cons = [c for c in pi.get('console', []) if 'realtime/v1/websocket' not in c.get('text', '')]
ws = len(pi.get('console', [])) - len(cons)
print(f"cap{n:02d}: {len(acts)} passos, vídeo {a['video'].get('durationS', a['video'].get('dur','?'))}s, narração {nar['dur']:.1f}s, falhos {len(fails)}, atrasos>=0.3: {len(late)}, maxLate {max([x.get('lateBy') or 0 for x in acts]):.2f}")
print(f"        pageErrors {len(pi.get('pageErrors', []))}, failed {len(pi.get('failed', []))}, bad {len(pi.get('bad', []))}, console (fora o WS do realtime, {ws} ignorados): {cons[:3]}")
for x in acts:
    ts, te = x.get('tStart', 0), x.get('tEnd', 0)
    ta = x.get('tAct') or 0
    lb = x.get('lateBy')
    flag = ''
    if x.get('error'): flag = ' !!ERRO ' + str(x['error'])[:90]
    elif (lb or 0) >= 0.8: flag = ' !!ATRASO'
    elif (lb or 0) >= 0.3: flag = ' ~atraso'
    if not tudo and x.get('do') in ('waitFor',) and not flag: continue
    lab = (x.get('label') or x.get('name') or '')[:46]
    pw = palavra(ta or ts) if x.get('do') != 'mark' else ''
    print(f"{x.get('i',''):>3} {x.get('do',''):7} {ts:6.2f}->{te:6.2f} act {ta:6.2f} late {('%.2f' % lb) if lb is not None else '  -  '} | {lab:46} | voz: {pw}{flag}")
