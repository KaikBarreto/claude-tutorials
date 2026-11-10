#!/usr/bin/env python3
"""T03 · confere o estado do Supabase falso (a MINHA instância, 54303) depois de um ensaio contra a semente apos-capNN que o capítulo
seguinte usa (lição 142: semente só sai de ensaio com 0 passo falho e com o estado conferido). Lê /__dev/state; não muda nada.
Uso: python3 -I rec/t03/t03_estado.py NN      (logo depois do ensaio do capítulo NN; NN = 02..08)"""
import json
import os
import sys
import urllib.request

FAKE = os.environ.get('FAKE_URL', 'http://127.0.0.1:54303')
HERE = os.path.dirname(os.path.abspath(__file__))
SEED_DIR = os.path.normpath(os.path.join(HERE, '..', 'mundo', 'seeds-extra', 't03'))


def tabela(t):
    with urllib.request.urlopen(f'{FAKE}/__dev/state?table={t}') as r:
        return json.load(r)


def resumo_tela():
    mats = {m['name']: m for m in tabela('materials')}
    grupos = {g['id']: g['name'] for g in tabela('material_groups')}
    tabs = {t['id']: t for t in tabela('price_tables')}
    r = mats.get('Radiador de cobre')
    out = {
        'radiador': None if not r else {
            'code': r['code'], 'estoque': r['current_stock'], 'compra': r['purchase_price'], 'venda': r['sale_price'],
            'ncm': (r.get('ncm') or '').replace('.', '') or None, 'grupo': grupos.get(r.get('group_id')), 'arquivado': r.get('is_archived')},
        'cobre': {k: (mats[k]['purchase_price'], mats[k]['sale_price']) for k in ('Cobre mel', 'Cobre misto', 'Fio de cobre encapado')},
        'ferro_misto': mats['Ferro misto']['current_stock'],
        'grupos': sorted(grupos.values()),
        'tabelas': sorted((t['name'], bool(t.get('is_linked')), t.get('variation_amount'), t.get('variation_direction')) for t in tabs.values()),
        'siqueira': {
            'fornecedor': (tabs.get(next(s for s in tabela('suppliers') if s['name'] == 'Depósito Irmãos Siqueira').get('default_price_table_id')) or {}).get('name'),
            'cliente': (tabs.get(next(s for s in tabela('customers') if s['name'] == 'Depósito Irmãos Siqueira').get('default_price_table_id')) or {}).get('name')},
        'precos_personalizados': len(tabela('entity_custom_prices')),
    }
    if r:
        out['movimentos_radiador'] = sorted((m['type'], m['quantity'], m.get('description')) for m in tabela('stock_movements') if m['material_id'] == r['id'])
    return out


def main():
    nn = int(sys.argv[1])
    agora = resumo_tela()
    print(json.dumps(agora, ensure_ascii=False, indent=1))
    # o que a semente apos-capNN promete (o capítulo seguinte parte dela)
    sem = json.load(open(os.path.join(SEED_DIR, f'apos-cap{nn:02d}.json'), encoding='utf8'))
    rad = sem['materials'][0]
    esperado = {'code': rad['code'], 'estoque': rad['current_stock'], 'compra': rad['purchase_price'], 'venda': rad['sale_price'],
                'ncm': rad['ncm'], 'grupo': 'Radiadores' if rad['group_id'] else None}
    dif = [k for k, v in esperado.items() if agora['radiador'] is None or str(agora['radiador'].get(k)) != str(v) and not (
        isinstance(v, float) and abs(float(agora['radiador'].get(k) or 0) - v) < 1e-6)]
    print('semente apos-cap%02d x tela:' % nn, 'OK' if not dif else 'DIFERENTE em ' + ', '.join(dif))


if __name__ == '__main__':
    main()
