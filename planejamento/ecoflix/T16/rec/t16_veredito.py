#!/usr/bin/env python3
"""T16 · veredito do ensaio rápido de um capítulo (lido do actions.json, do resumo e do prever): falhos, SEM ALVO, pageIssues,
avisos do observador, confere DIFERENTE e o maior atraso previsto. `precisa=1` quando o completo é obrigatório pela regra de 11/11
(prever >= 0,4 s ou qualquer aviso no rápido). Uso: python3 -I rec/t16/t16_veredito.py NN"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
nn = f'{int(sys.argv[1]):02d}'
a = json.load(open(f'{HERE}/_ens/t16-cap{nn}.actions.json'))
acts = a['actions']
falhos = sum(1 for x in acts if x.get('error') or x.get('ok') is False)
txt = json.dumps(acts, ensure_ascii=False)
sem_alvo = txt.count('SEM ALVO')
dif = txt.count('DIFERENTE')
pi = a.get('pageIssues') or {}
cons = [c for c in pi.get('console', []) if 'realtime/v1/websocket' not in c.get('text', '') and not re.search(r'\b406\b', c.get('text', ''))]
bad = [b for b in pi.get('bad', []) if not re.search(r'\b406\b', str(b))]
pag = len(pi.get('pageErrors', []) or []) + len(cons) + len(bad) + len(pi.get('failed', []) or [])
av = next((x.get('result') or x.get('value') for x in reversed(acts) if x.get('label') == 'avisos de erro na tela'), None)
avisos = 0 if av in (None, '[]', '"[]"') or str(av).strip('"') == '[]' else 1
prev = open(f'{HERE}/_ens/t16-cap{nn}.prever.txt', encoding='utf8').read()
m = re.search(r'maior atraso ([\d.]+) s', prev)
atraso = float(m.group(1)) if m else 99.0
precisa = int(atraso >= 0.4 or sem_alvo or dif or pag or avisos)
print(f'falhos={falhos} semalvo={sem_alvo} diferente={dif} pagina={pag} avisos={avisos} prever={atraso:.2f} precisa={precisa}')
