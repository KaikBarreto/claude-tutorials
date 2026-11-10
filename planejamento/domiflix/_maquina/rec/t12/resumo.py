#!/usr/bin/env python3
"""Resumo de uma gravação do T18: falhas, atrasos e, para cada passo, o instante do gesto (tAct) ao lado da palavra falada
naquele momento. Uso: python3 -I rec/t12/resumo.py NN [--tudo]
Ruído esperado e filtrado (e contado à parte, para constar do relatório): o 406 de `GET form_responses` (o app lê a resposta com
`.single()` e o PostgREST responde 406 quando ainda não existe linha) e o WebSocket do realtime."""
import json, sys, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
n = int(sys.argv[1]); tudo = '--tudo' in sys.argv
pasta = f'{HERE}/_ens' if '--ens' in sys.argv else HERE
a = json.load(open(f'{pasta}/t12-cap{n:02d}.actions.json'))
nar = json.load(open(f'{HERE}/../../t12/narracao/cap{n:02d}.json'))
words = nar['words']


def palavra(t):
    ant = [w for w in words if w['s'] <= t + 0.05]
    return ant[-1]['w'] if ant else ''


E406 = re.compile(r'406.*form_responses|form_responses.*406|status of 406')
acts = a['actions']
fails = [x for x in acts if x.get('error') or x.get('ok') is False]
late = [x for x in acts if (x.get('lateBy') or 0) >= 0.3]
pi = a.get('pageIssues') or {}
cons_all = pi.get('console', [])
ws = [c for c in cons_all if 'realtime/v1/websocket' in c.get('text', '')]
e406c = [c for c in cons_all if E406.search(c.get('text', ''))]
cons = [c for c in cons_all if c not in ws and c not in e406c]
bad_all = pi.get('bad', [])
e406b = [b for b in bad_all if E406.search(str(b))]
bad = [b for b in bad_all if b not in e406b]
vid = a.get('video', {})
maxlate = max([x.get('lateBy') or 0 for x in acts] or [0])
print(f"cap{n:02d}: {len(acts)} passos, vídeo {vid.get('durationS', '?')}s, narração {nar['dur']:.1f}s, falhos {len(fails)}, atrasos>=0.3: {len(late)}, maxLate {maxlate:.2f}")
print(f"        pageErrors {len(pi.get('pageErrors', []))}, failed {len(pi.get('failed', []))}, bad {len(bad)} (+{len(e406b)} 406 de form_responses esperados), "
      f"console {len(cons)} (+{len(e406c)} 406 e {len(ws)} do WebSocket do realtime, ignorados)")
for c in cons[:4]:
    print('        console:', str(c.get('text', ''))[:200])
for b in bad[:4]:
    print('        bad:', str(b)[:200])
for b in pi.get('pageErrors', [])[:3]:
    print('        pageError:', str(b)[:200])
for b in pi.get('failed', [])[:3]:
    print('        failed:', str(b)[:200])
for x in acts:
    ts, te = x.get('tStart', 0), x.get('tEnd', 0)
    ta = x.get('tAct') or 0
    lb = x.get('lateBy')
    flag = ''
    if x.get('error'):
        flag = ' !!ERRO ' + str(x['error'])[:110]
    elif (lb or 0) >= 0.8:
        flag = ' !!ATRASO'
    elif (lb or 0) >= 0.3:
        flag = ' ~atraso'
    if x.get('warn'):
        flag += ' [aviso: ' + str(x['warn'])[:60] + ']'
    if not tudo and x.get('do') in ('waitFor',) and not flag:
        continue
    lab = (x.get('label') or x.get('name') or '')[:46]
    pw = palavra(ta or ts) if x.get('do') != 'mark' else ''
    val = ''
    if x.get('do') == 'eval' and x.get('value') not in (None, 'ok') and not isinstance(x.get('value'), (int, float)):
        val = '  => ' + json.dumps(x.get('value'), ensure_ascii=False)[:60]
    print(f"{x.get('i',''):>3} {x.get('do',''):7} {ts:6.2f}->{te:6.2f} act {ta:6.2f} late {('%.2f' % lb) if lb is not None else '  -  '} | {lab:46} | voz: {pw}{flag}{val}")
