#!/usr/bin/env python3
"""T07 · grava rec/mundo/seeds-extra/t07/apos-capNN.json a partir do estado da MINHA instância (FAKE_URL, 54307) logo depois do ensaio do
capítulo NN. Só grava se o ensaio teve 0 passo falho (lição 142). apos-capNN = a semente apos-* de partida do capítulo + o que o capítulo
mudou no banco: linhas novas, `_patch` das alteradas (instantes ISO não contam) e `_remove` das que sumiram. Ficam de fora os rascunhos
do pedido (order_drafts, draft_editors) e o log de pesagens.
Uso (logo depois do ensaio, antes de outro ensaio na mesma instância): python3 -I rec/t07/t07_semente.py NN [--grav] [--seco]
(--grav: confere as falhas na gravação completa em rec/t07/ em vez do ensaio rápido em rec/t07/_ens/; --seco: só mostra o que mudou)."""
import json
import os
import re
import sys
import urllib.request

FAKE = os.environ.get('FAKE_URL', 'http://127.0.0.1:54307')
HERE = os.path.dirname(os.path.abspath(__file__))
SEEDS = os.path.normpath(os.path.join(HERE, '..', 'mundo', 'seeds-extra'))
FORA = {'order_drafts', 'draft_editors', 'log_pesagens'}
INTERESSE = ['suppliers', 'customers', 'purchases', 'purchase_items', 'sales', 'sale_items', 'stock_movements', 'materials', 'cash_register',
             'cash_transactions', 'bank_transactions', 'balances', 'balance_movements', 'financial_bills']
ISO = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}')

n = int(sys.argv[1])
seco = '--seco' in sys.argv
pasta = HERE if '--grav' in sys.argv else os.path.join(HERE, '_ens')
roteiro = json.load(open(os.path.join(HERE, f'cap{n:02d}.json'), encoding='utf8'))
acts = json.load(open(os.path.join(pasta, f"{roteiro['name']}.actions.json"), encoding='utf8'))['actions']
falhos = [a for a in acts if a.get('error') or a.get('ok') is False]
if falhos and not seco:
    raise SystemExit(f'cap{n:02d}: {len(falhos)} passo(s) falho(s): semente NÃO gravada')


def get(url):
    with urllib.request.urlopen(FAKE + url) as r:
        return json.load(r)


def post(url, body=None):
    req = urllib.request.Request(FAKE + url, data=json.dumps(body or {}).encode(), headers={'content-type': 'application/json'}, method='POST')
    with urllib.request.urlopen(req) as r:
        return r.read()


def le(tabs):
    return {t: {r['id']: r for r in get(f'/__dev/state?table={t}') if isinstance(r, dict) and 'id' in r} for t in tabs}


# 1) o FIM (o banco como o capítulo deixou) e 2) o INÍCIO (reset + as sementes do capítulo), nas mesmas tabelas
cont_fim = get('/__dev/state')
fim = le([t for t, c in cont_fim.items() if t not in FORA and (c or t in INTERESSE)])
post('/__dev/reset')
post('/__dev/seed', {'files': roteiro.get('seedExtra', [])})
ini = le(list(fim))

prev_nome = next((s for s in roteiro.get('seedExtra', []) if s.startswith('t07/apos-')), None)
prev = json.load(open(os.path.join(SEEDS, prev_nome + '.json'), encoding='utf8')) if prev_nome else {}
novas = {t: list(v) for t, v in prev.items() if not t.startswith('_')}
patch = {t: {p['match']['id']: dict(p['set']) for p in ps} for t, ps in prev.get('_patch', {}).items()}
remov = {t: list(v) for t, v in prev.get('_remove', {}).items()}
ids_prev = {t: {r['id'] for r in rows} for t, rows in novas.items()}


def igual(a, b):
    if isinstance(a, str) and isinstance(b, str) and ISO.match(a) and ISO.match(b):
        return True   # instante recalculado a cada reset (sementes relativas): não é alteração do capítulo
    return a == b


resumo = []
for t in sorted(fim):
    a, b = ini.get(t, {}), fim[t]
    nov = [b[i] for i in b if i not in a]
    alt = {i: {k: v for k, v in b[i].items() if not igual(a[i].get(k), v)} for i in b if i in a}
    alt = {i: d for i, d in alt.items() if d}
    sum_ = [i for i in a if i not in b]
    if not (nov or alt or sum_):
        continue
    resumo.append(f'{t}: +{len(nov)} ~{len(alt)} -{len(sum_)}')
    if nov:
        novas.setdefault(t, []).extend(nov)
    for i, d in alt.items():
        if i in ids_prev.get(t, set()):
            for r in novas[t]:
                if r['id'] == i:
                    r.update(d)
        else:
            patch.setdefault(t, {}).setdefault(i, {}).update(d)
    for i in sum_:
        if i in ids_prev.get(t, set()):
            novas[t] = [r for r in novas[t] if r['id'] != i]
        else:
            remov.setdefault(t, []).append({'id': i})

print(f'cap{n:02d} (partida {roteiro.get("seedExtra")}):\n  ' + ('\n  '.join(resumo) or 'nada mudou'))
if seco:
    raise SystemExit(0)
out = {'_doc': f'T07 · estado depois do cap{n:02d} (acumulado desde t07/inicio): gerado por rec/t07/t07_semente.py do ensaio com 0 falho; '
               'não editar à mão.'}
out.update({t: rows for t, rows in sorted(novas.items()) if rows})
if any(patch.values()):
    out['_patch'] = {t: [{'match': {'id': i}, 'set': d} for i, d in ps.items()] for t, ps in sorted(patch.items()) if ps}
if any(remov.values()):
    out['_remove'] = {t: v for t, v in sorted(remov.items()) if v}
os.makedirs(os.path.join(SEEDS, 't07'), exist_ok=True)
dest = os.path.join(SEEDS, 't07', f'apos-cap{n:02d}.json')
json.dump(out, open(dest, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print(f'  -> {os.path.relpath(dest, os.path.join(HERE, "..", ".."))}')
