#!/usr/bin/env python3
"""Resumo de uma gravação do robô (ou do ensaio rápido, com --ens): falhas, atrasos e, para cada passo, o instante do gesto (tAct) ao lado
da palavra falada naquele momento (coluna `voz:`: âncora errada aparece aqui). Molde da Domiflix (T14/T22).
Uso: python3 -I rec/<id>/resumo.py NN [--tudo] [--ens]   (a cópia fica em rec/<id>/: o id da aula é o nome da pasta)
Ruído esperado, contado à parte (e não escondido): o WebSocket do realtime e os 406 de leitura com `.single()` (o PostgREST responde 406
quando a linha ainda não existe; T14/T22: `form_responses`). Valor devolvido por `eval` aparece no fim da linha (`=> ...`): o topo final
de uma rolagem tem de chegar perto do pedido (T14) e `confere*` (texto da tela x fala) acusa DIFERENTE. Depois de cada ensaio e de cada
gravação: `grep "SEM ALVO" rec/<id>/.*.out` (o `eval` não falha sozinho)."""
import json, sys, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
TUT = os.path.basename(HERE)   # rec/<id>/resumo.py
a_ = sys.argv[1]
nn = f'{int(a_[:-1]):02d}b' if a_.endswith('b') else f'{int(a_):02d}'
tudo = '--tudo' in sys.argv
pasta = f'{HERE}/_ens' if '--ens' in sys.argv else HERE
a = json.load(open(f'{pasta}/{TUT}-cap{nn}.actions.json'))
# a voz que o gerar.py usou: a ESTIMADA (rec/<id>/_voz/) quando o capítulo ainda tem linha sem voz nova; senão a processada (T14)
_prov = f'{HERE}/_voz/cap{nn[:2]}.json'
nar = json.load(open(_prov if os.path.exists(_prov) else f'{HERE}/../../{TUT}/narracao/cap{nn[:2]}.json'))
words = nar['words']


def palavra(t):
    ant = [w for w in words if w['s'] <= t + 0.05]
    return ant[-1]['w'] if ant else ''


E406 = re.compile(r'\b406\b')   # .single() sem linha (PostgREST); a tabela aparece no texto
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
print(f"cap{nn}: {len(acts)} passos, vídeo {vid.get('durationS', '?')}s, narração {nar['dur']:.1f}s, falhos {len(fails)}, atrasos>=0.3: {len(late)}, maxLate {maxlate:.2f}")
print(f"        pageErrors {len(pi.get('pageErrors', []))}, failed {len(pi.get('failed', []))}, bad {len(bad)} (+{len(e406b)} 406 de .single() sem linha), "
      f"console {len(cons)} (+{len(e406c)} 406 e {len(ws)} do WebSocket do realtime, ignorados)")
for c in cons[:4]:
    print('        console:', str(c.get('text', ''))[:200])
for b in bad[:4]:
    print('        bad:', str(b)[:200])
for b in (e406b + e406c)[:3]:   # esperado só onde o app lê com .single() uma linha que ainda não existe
    print('        406:', str(b)[:160])
for b in pi.get('pageErrors', [])[:3]:
    print('        pageError:', str(b)[:200])
for b in pi.get('failed', [])[:3]:
    print('        failed:', str(b)[:200])
dif = []
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
    if x.get('do') == 'eval' and x.get('value') not in (None, 'ok'):   # números também: topo final das rolagens, nº de linhas (T21/T22)
        if (x.get('label') or '').startswith('confere'):
            v = str(x.get('value'))
            val = '  => ' + v[:300]
            if v.startswith('DIFERENTE'):
                flag += ' !!TELA DIFERENTE DA FALA'
                dif.append((x.get('label'), v))
        else:
            val = '  => ' + json.dumps(x.get('value'), ensure_ascii=False)[:60]
    print(f"{x.get('i',''):>3} {x.get('do',''):7} {ts:6.2f}->{te:6.2f} act {ta:6.2f} late {('%.2f' % lb) if lb is not None else '  -  '} | {lab:46} | voz: {pw}{flag}{val}")

confs = [x for x in acts if (x.get('label') or '').startswith('confere')]
print(f'conferências tela x fala: {len(confs)} feitas, {len(dif)} DIFERENTE(S)')
for l, v in dif:
    print('   !!', l, '->', v[:400])
