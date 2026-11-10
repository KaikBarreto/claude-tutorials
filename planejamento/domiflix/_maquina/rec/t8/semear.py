#!/usr/bin/env python3
"""T8 · gera o mundo de partida da aula: rec/fakebase/seeds-extra/t8/inicio.json e rec/t8/cadeia.json.

Estado de partida = FIM DO T2 (o T18 não altera dado; o T7 deixa a OS #16 concluída com a baixa de Limpa-evaporador e Fita isolante).
Cadeia = a do T7/T18 SEM `t7/inicio` e SEM `t18/fim-t7-provisorio` (t3, t1, t4, t5) + `t8/inicio`, que traz sozinho todo o estoque:
  - o local "Estoque Principal" (padrão), os grupos Gases, Cobre e tubos, Elétrica e Consumíveis e os nove materiais EST-001 a EST-009
    (mesmos ids `@id:material.*` do T7: R-410A, Limpa-evaporador e Fita isolante), com saldo, mínimo, custo e venda do roteiro;
  - o histórico: "Cadastro inicial" de ~90 dias antes, duas compras recebidas de R-410A (20 kg a 86,00 há 60 dias e 15 kg a 90,00 há 25
    dias, como requisições concluídas com ordem "Recebida") e as saídas de R-410A no meio (saldo bate com 8,5 hoje);
  - o "Estado final" do T7 no estoque: OS #16 concluída ontem (relógio do T8), com as duas linhas de Consumo (2 un de Limpa-evaporador e
    2 de Fita isolante) no Kardex e nas linhas de material da OS. A unidade da Fita é "un" (a lista do app: un, kg, l, m, cx, pc).
Tudo com datas RELATIVAS ao `FAKE_NOW` do T8 (2026-11-03T09:00-03:00): tokens @at/@today, nada literal.
Os ids dos fornecedores vêm da cadeia (o Ventura do T3 tem id literal): rodar de novo se a cadeia mudar (ex.: quando o T3 v2 fechar).

Uso:  python3 -I rec/t8/semear.py            (gera os JSON)
      python3 -I rec/t8/semear.py --conferir (confere: saldo = soma do Kardex, mínimo, ids dos fornecedores na cadeia)
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EXTRA = os.path.normpath(os.path.join(HERE, '..', 'fakebase', 'seeds-extra'))
SAIDA = os.path.join(EXTRA, 't8', 'inicio.json')
CADEIA = ['t3/apos-cap10', 't1/apos-cap13', 't4/inicio', 't4/apos-cap14', 't5/inicio', 't5/apos-cap15']

CO = '9c307966-79f1-567c-ac4d-d5fd3c1a2f40'            # Glacial Cold Brasil
CAMILA = 'd40f5787-1779-501f-900c-ddb2b90a36e5'
RAFAEL = '34c36c63-0890-5e89-8963-7c77b7996908'
OS16 = '2c9dc476-c5ca-412f-90fe-6c38a67f125e'
PRINCIPAL = '@id:estoque.principal'


def stable_id(key):
    """Mesmo UUID de `stableId` do fakebase (core/util.mjs): sha1('domiflix-fake:' + chave), versão 5."""
    h = bytearray(hashlib.sha1(('domiflix-fake:' + key).encode()).digest())
    h[6] = (h[6] & 0x0F) | 0x50
    h[8] = (h[8] & 0x3F) | 0x80
    x = bytes(h[:16]).hex()
    return f'{x[:8]}-{x[8:12]}-{x[12:16]}-{x[16:20]}-{x[20:32]}'


def fornecedores():
    """nome -> id, lendo a cadeia (token @id:chave vira o UUID estável; id literal fica como está)."""
    out = {}
    base = os.path.join(EXTRA, '..', 'seeds')
    arquivos = [os.path.join(base, 'gen-02-cadastros.json')] + [os.path.join(EXTRA, c + '.json') for c in CADEIA]
    for f in arquivos:
        d = json.load(open(f, encoding='utf8'))
        if isinstance(d, dict):
            for r in d.get('suppliers', []) or []:
                i = r.get('id')
                if isinstance(i, str) and i.startswith('@id:'):
                    i = stable_id(i[4:])
                if i:
                    out[r['name']] = i
    return out


FORN = fornecedores()
VENTURA = FORN['Ventura Gás e Tubos']
POLAR = FORN['Polar Distribuidora de Peças Ltda']

GRUPOS = [  # chave, nome, cor, ordem
    ('gases', 'Gases', '#0EA5E9', 0),
    ('cobre', 'Cobre e tubos', '#B45309', 1),
    ('eletrica', 'Elétrica', '#8B5CF6', 2),
    ('consumiveis', 'Consumíveis', '#F59E0B', 3),
]

# chave, nome, SKU, unidade, saldo de hoje, mínimo, custo, venda, grupo
MATERIAIS = [
    ('r410a', 'Gás refrigerante R-410A', 'EST-001', 'kg', 8.5, 10, 90.0, 150.0, 'gases'),
    ('r32', 'Gás refrigerante R-32', 'EST-002', 'kg', 6, 4, 98.0, 160.0, 'gases'),
    ('cobre14', 'Tubo de cobre 1/4"', 'EST-003', 'm', 45, 30, 16.0, 28.0, 'cobre'),
    ('cobre38', 'Tubo de cobre 3/8"', 'EST-004', 'm', 12, 20, 26.0, 42.0, 'cobre'),
    ('dreno', 'Mangueira de dreno', 'EST-005', 'm', 60, 25, 3.5, 8.0, 'cobre'),
    ('cap35', 'Capacitor 35 µF', 'EST-006', 'un', 9, 4, 34.0, 62.0, 'eletrica'),
    ('limpa-evaporador', 'Limpa-evaporador em spray', 'EST-007', 'un', 10, 6, 20.0, 38.0, 'consumiveis'),
    ('fita-isolante', 'Fita isolante', 'EST-008', 'un', 28, 12, 6.5, 11.0, 'consumiveis'),
    ('suporte', 'Suporte para condensadora', 'EST-009', 'un', 8, 4, 48.0, 85.0, 'consumiveis'),
]
MIN_POR_CHAVE = {m[0]: m for m in MATERIAIS}

# Kardex antigo: (dias, hora, tipo, quantidade assinada, extras). A soma de cada material fecha no saldo de hoje.
OS16_NOTA = 'Consumo na OS #16'
HISTORICO = {
    'r410a': [
        (-90, '08:20', 'entrada', 10, dict(notes='Cadastro inicial')),
        (-60, '10:10', 'entrada', 20, dict(notes='Recebimento da O.C. #1', supplier=VENTURA, cost=86.0)),
        (-45, '14:30', 'saida', -12, dict(notes='Carga de gás em instalação')),
        (-25, '09:40', 'entrada', 15, dict(notes='Recebimento da O.C. #2', supplier=VENTURA, cost=90.0)),
        (-18, '15:05', 'saida', -14.5, dict(notes='Carga de gás em manutenção')),
        (-9, '11:25', 'saida', -10, dict(notes='Complemento de carga')),
    ],
    'r32': [(-90, '08:21', 'entrada', 6, dict(notes='Cadastro inicial'))],
    'cobre14': [(-90, '08:22', 'entrada', 45, dict(notes='Cadastro inicial'))],
    'cobre38': [(-90, '08:23', 'entrada', 12, dict(notes='Cadastro inicial'))],
    'dreno': [(-90, '08:24', 'entrada', 60, dict(notes='Cadastro inicial'))],
    'cap35': [(-90, '08:25', 'entrada', 9, dict(notes='Cadastro inicial'))],
    'limpa-evaporador': [
        (-90, '08:26', 'entrada', 12, dict(notes='Cadastro inicial')),
        (-1, '10:31', 'consumo', -2, dict(notes=OS16_NOTA, os=OS16, por=RAFAEL, cost=20.0)),
    ],
    'fita-isolante': [
        (-90, '08:27', 'entrada', 30, dict(notes='Cadastro inicial')),
        (-1, '10:31', 'consumo', -2, dict(notes=OS16_NOTA, os=OS16, por=RAFAEL, cost=6.5)),
    ],
    'suporte': [(-90, '08:28', 'entrada', 8, dict(notes='Cadastro inicial'))],
}

# Compras antigas de R-410A (requisições concluídas, ordem Recebida): numero, título, dias (criação, envio, recebimento), qtd, preço
COMPRAS = [
    (1, 'Reposição de gás R-410A de setembro', (-62, -61, -60), 20, 86.0),
    (2, 'Reposição de gás R-410A de outubro', (-27, -26, -25), 15, 90.0),
]


# (inventory_low_stock e inventory_count_divergences são VIEWS calculadas por handlers/views: a lista vazia só cria a tabela para o aviso
#  TABELA_SEM_SEED calar, o provider da view tem precedência na leitura; nfe_imports é tabela de verdade, vazia até o cap. 11)
VAZIAS = ['inventory_low_stock', 'inventory_count_divergences', 'nfe_imports', 'tenant_tasks', 'financial_transactions', 'inventory_counts', 'leads', 'crm_stages', 'crm_pipelines', 'pricing_settings',
          'cost_centers', 'tenant_charges', 'os_sla_config', 'os_required_fields', 'os_photos', 'contract_health_status', 'tenant_subscriptions']


def at(dias, hhmm):
    return f'@at:{dias:+d}d {hhmm}'


def montar():
    d = {'_comentario': 'T8 · estado de partida (estoque, histórico, compras antigas e o fim do T7 na OS #16). Gerado por rec/t8/semear.py: não edite à mão.'}
    d['stocks'] = [{'id': PRINCIPAL, 'company_id': CO, 'name': 'Estoque Principal', 'is_default': True, 'sort_order': 0, 'purpose': 'operacional',
                    'customer_id': None, 'created_at': at(-90, '08:00'), 'updated_at': at(-90, '08:00')}]
    d['material_groups'] = [{'id': f'@id:grupo.{k}', 'company_id': CO, 'name': n, 'color': c, 'sort_order': o,
                             'created_at': at(-90, '08:00'), 'updated_at': at(-90, '08:00')} for k, n, c, o in GRUPOS]
    inv, niv, mov, mat_os = [], [], [], []
    for chave, nome, sku, un, saldo, minimo, custo, venda, grupo in MATERIAIS:
        mid = f'@id:material.{chave}'
        inv.append({'id': mid, 'company_id': CO, 'name': nome, 'sku': sku, 'unit': un, 'quantity': saldo, 'min_quantity': minimo,
                    'cost_price': custo, 'sale_price': venda, 'group_id': f'@id:grupo.{grupo}', 'is_sellable': False, 'customer_id': None,
                    'created_at': at(-90, '08:19'), 'updated_at': at(-90, '08:19')})
        niv.append({'id': f'@id:nivel.{chave}.principal', 'company_id': CO, 'inventory_id': mid, 'stock_id': PRINCIPAL, 'quantity': saldo,
                    'min_quantity': minimo, 'is_present': True, 'created_at': at(-90, '08:19'), 'updated_at': at(-1, '10:31') if chave in ('limpa-evaporador', 'fita-isolante') else at(-90, '08:19')})
        acumulado = 0.0
        for n, (dias, hora, tipo, qtd, ex) in enumerate(HISTORICO[chave]):
            antes, depois = round(acumulado, 6), round(acumulado + qtd, 6)
            acumulado = depois
            linha = {'id': f'@id:t8.mov.{chave}.{n}', 'company_id': CO, 'inventory_id': mid, 'stock_id': PRINCIPAL, 'movement_type': tipo,
                     'quantity': qtd, 'stock_before': antes, 'stock_after': depois, 'notes': ex.get('notes'), 'unit_cost': ex.get('cost'),
                     'supplier_id': ex.get('supplier'), 'service_order_id': ex.get('os'), 'created_by': ex.get('por', CAMILA),
                     'created_at': at(dias, hora)}
            mov.append(linha)
            if ex.get('os'):
                mat_os.append({'id': f'@id:t8.osmat.{chave}', 'company_id': CO, 'service_order_id': ex['os'], 'inventory_id': mid,
                               'stock_id': PRINCIPAL, 'quantity': -qtd, 'committed_quantity': -qtd, 'unit_cost': ex['cost'],
                               'created_by': ex.get('por', CAMILA), 'created_at': at(dias, '09:05'), 'updated_at': at(dias, hora)})
        assert abs(acumulado - saldo) < 1e-9, f'{chave}: o Kardex fecha em {acumulado}, o saldo é {saldo}'
    d['inventory'], d['inventory_stock_levels'], d['inventory_movements'], d['service_order_materials'] = inv, niv, mov, mat_os

    compras, cmat, cot, preco, ordens, itens = [], [], [], [], [], []
    r = MIN_POR_CHAVE['r410a']
    for numero, titulo, (dc, de, dr), qtd, pu in COMPRAS:
        base = f't8.compra.{numero}'
        compras.append({'id': f'@id:{base}', 'company_id': CO, 'numero': numero, 'title': titulo, 'status': 'concluida', 'flow_type': 'requisicao',
                        'stock_id': PRINCIPAL, 'created_by': CAMILA, 'created_at': at(dc, '09:15'), 'updated_at': at(dr, '10:10')})
        cmat.append({'id': f'@id:{base}.mat', 'company_id': CO, 'compra_id': f'@id:{base}', 'inventory_id': '@id:material.r410a',
                     'material_name': r[1], 'unit': r[3], 'quantity': qtd, 'chosen_cotacao_id': f'@id:{base}.cot', 'created_at': at(dc, '09:15')})
        cot.append({'id': f'@id:{base}.cot', 'company_id': CO, 'compra_id': f'@id:{base}', 'supplier_id': VENTURA, 'status': 'aceita',
                    'decided_at': at(de, '08:40'), 'created_at': at(dc, '15:30'), 'updated_at': at(de, '08:40')})
        preco.append({'id': f'@id:{base}.preco', 'company_id': CO, 'cotacao_id': f'@id:{base}.cot', 'compra_material_id': f'@id:{base}.mat',
                      'unit_price': pu, 'created_at': at(dc, '15:30')})
        ordens.append({'id': f'@id:{base}.oc', 'company_id': CO, 'compra_id': f'@id:{base}', 'supplier_id': VENTURA, 'numero': numero,
                       'status': 'recebida', 'sent_at': at(de, '08:45'), 'received_at': at(dr, '10:10'), 'created_by': CAMILA,
                       'created_at': at(de, '08:41'), 'updated_at': at(dr, '10:10')})
        itens.append({'id': f'@id:{base}.item', 'company_id': CO, 'ordem_id': f'@id:{base}.oc', 'compra_material_id': f'@id:{base}.mat',
                      'inventory_id': '@id:material.r410a', 'material_name': r[1], 'unit': r[3], 'quantity_ordered': qtd, 'quantity_received': qtd,
                      'unit_price': pu, 'created_at': at(de, '08:41')})
    d['compras'], d['compra_materiais'], d['compra_cotacoes'], d['compra_cotacao_precos'] = compras, cmat, cot, preco
    d['compra_ordens'], d['compra_ordem_itens'] = ordens, itens

    # Financeiro padrão do cadastro (PRODUCAO.md, alinhamento: contas Caixa e Conta Principal + categorias), mesmo conteúdo do T9
    # (seeds-extra/t9/inicio.json); o Dashboard consulta e a compra direta (só mostrada no menu) lançaria nelas.
    t9 = json.load(open(os.path.join(EXTRA, 't9', 'inicio.json'), encoding='utf8'))
    d['financial_accounts'], d['financial_categories'] = t9['financial_accounts'], t9['financial_categories']
    # Tabelas que as telas do T8 consultam e que ficam VAZIAS de propósito (mantém /__dev/unknowns limpo)
    for nome in VAZIAS:
        d[nome] = []

    # fim do T7 na OS #16 (relógio do T8): concluída ontem pelo Rafael, depois do check-in das 8h05
    d['_patch'] = {'service_orders': [{'match': {'id': OS16}, 'set': {
        'status': 'concluida', 'scheduled_date': '@today-1d', 'check_in_time': at(-1, '08:05'), 'check_in_by': RAFAEL, 'started_at': at(-1, '08:05'),
        'check_out_time': at(-1, '10:30'), 'check_out_by': RAFAEL, 'completed_at': at(-1, '10:31'), 'updated_at': at(-1, '10:31'),
        'partial_finish': False}}],
        # G1 (1.38.19): trilha Domiflix sem tela escura de introdução nem faixa de lembrete. A linha já existe na base
        # (seeds/gen-03-domiflix.json, is_onboarding true): semente com o mesmo id DUPLICA, então vai por _patch.
        'domiflix_learning_paths': [{'match': {'id': 'c0000000-0000-4000-8000-000000000001'}, 'set': {'is_onboarding': False}}]}
    return d


def conferir(d):
    """Confere a coerência do mundo: Kardex = saldo, mínimo por local, fornecedor existente na cadeia."""
    soma = {}
    for m in d['inventory_movements']:
        soma[m['inventory_id']] = round(soma.get(m['inventory_id'], 0) + m['quantity'], 6)
    for i in d['inventory']:
        assert abs(soma[i['id']] - i['quantity']) < 1e-9, (i['name'], soma[i['id']], i['quantity'])
    for n in d['inventory_stock_levels']:
        assert n['quantity'] == next(i['quantity'] for i in d['inventory'] if i['id'] == n['inventory_id'])
    baixos = [i['name'] for i in d['inventory'] if i['quantity'] < i['min_quantity']]
    assert baixos == ['Gás refrigerante R-410A', 'Tubo de cobre 3/8"'], baixos
    assert VENTURA and POLAR
    total = sum(i['quantity'] * i['cost_price'] for i in d['inventory'])
    print('ok: Kardex = saldo em', len(d['inventory']), 'materiais; abaixo do mínimo:', baixos, '; valor investido R$', f'{total:.2f}')
    print('Ventura =', VENTURA, '· Polar =', POLAR)


if __name__ == '__main__':
    d = montar()
    conferir(d)
    if '--conferir' in sys.argv:
        sys.exit(0)
    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    json.dump(d, open(SAIDA, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    json.dump({'inicio': CADEIA + ['t8/inicio']}, open(os.path.join(HERE, 'cadeia.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print('gravado', os.path.relpath(SAIDA, os.path.join(HERE, '..', '..')), 'e rec/t8/cadeia.json')
