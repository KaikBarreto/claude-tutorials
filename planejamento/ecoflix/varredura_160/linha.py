import json, sys, os, re
T, C, RC = sys.argv[1:4]
b = f'/home/claude/ecoflix/rec/{T}/_ens'
out = open(f'{b}/cap{C}.out', errors='replace').read() if os.path.exists(f'{b}/cap{C}.out') else ''
p = f'{b}/{T}-cap{C}.actions.json'
if not os.path.exists(p):
    print(f'{C} rc={RC} SEM-ACTIONS {out.strip().splitlines()[-1][:160] if out.strip() else ""}'); sys.exit()
a = json.load(open(p)); acts = a['actions']
f = [x for x in acts if x.get('error') or x.get('ok') is False]
pi = a.get('pageIssues') or {}
cons = [c for c in pi.get('console', []) if 'realtime/v1/websocket' not in c.get('text', '') and not re.search(r'\b406\b', c.get('text', ''))]
net = pi.get('network', []) if isinstance(pi.get('network'), list) else []
sem = out.count('SEM ALVO')
p1 = ''
if f:
    x = f[0]; p1 = f" 1a_falha=#{acts.index(x)} {x.get('do')} {str(x.get('label') or x.get('sel') or x.get('text') or '')[:50]!r}: {str(x.get('error'))[:110]!r}"
print(f"{C} rc={RC} passos={len(acts)} falhos={len(f)} semalvo={sem} console={len(cons)} rede={len(net)}{p1}")
