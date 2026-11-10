#!/usr/bin/env python3
"""T9 · gera o mundo de partida da aula (rec/fakebase/seeds-extra/t9/inicio.json) e rec/t9/cadeia.json.

Estado de partida = "Estado inicial" do T09/roteiro.md (fim do T8): Glacial Cold Brasil, OS #1 a #16, tipos de serviço do T4, estoque do T8
(12 materiais, Estoque Principal + Van 01), Financeiro padrão do cadastro (Caixa, Conta Principal, 14 + 14 categorias) e, de bastidor do T9:
Precificação ZERADA, as 4 linhas de proposal_templates, funcionários com custo mensal (salário 0, o T15 completa), 8 orçamentos históricos.

Decisão de numeração (a fala diz "a OS número dezessete"): o mundo do T9 usa só as OS #1 a #15 do `t5/inicio` + a OS #16 do T7 (já concluída),
SEM as OS #17 a #22 que o T5 criou ao vivo (a cadeia "de verdade" daria #23). Por isso a cadeia aqui NÃO inclui `t5/apos-capNN` nem `t7/inicio`.
Do T5 só entra o que não depende dessas OS: os dois `_patch.service_orders` do fim do T5 (status de #1 a #15) e as linhas da OS #16.

Os ids vêm SEMPRE lidos da cadeia (nunca copiados à mão). Rodar de qualquer pasta:  python3 -I rec/t9/semear.py
"""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EXTRA = os.path.normpath(os.path.join(HERE, '..', 'fakebase', 'seeds-extra'))
CHAIN_BASE = ['t3/apos-cap10', 't1/apos-cap13', 't4/inicio', 't4/apos-cap14', 't5/inicio']
FAKE_NOW = '2026-11-03T09:00:00-03:00'   # terça-feira; o mesmo no backend falso e no robô
EMP = '9c307966-79f1-567c-ac4d-d5fd3c1a2f40'   # company.glacial (stableId)
CAMILA = '@id:user.camila'

# ids fixos dos tipos de serviço do T4 (seeds-extra/t4/apos-cap14.json)
ST = {
    'preventiva': '49db63cb-1737-415d-b795-187297148790', 'corretiva': '7597518c-45a4-4fbd-971c-f7297445bb6c',
    'instalacao': '0dc4bf2b-53c7-49ad-9c66-01e938c311d7', 'higienizacao': '10113e22-97c6-46e6-bcc5-f411f62f6935',
    'gas': 'd84b0c8f-efc9-4934-8bb6-fc2bc4911f39', 'visita': '0ec08cc1-1ebd-4ec2-ae38-f7d345cfe63f',
}
NOME_ST = {'preventiva': 'Manutenção Preventiva', 'corretiva': 'Manutenção Corretiva', 'instalacao': 'Instalação de Split',
           'higienizacao': 'Higienização de Split', 'gas': 'Carga de Gás', 'visita': 'Visita Técnica'}
PRECO_ST = {'preventiva': 180, 'corretiva': 220, 'instalacao': 650, 'higienizacao': 180, 'gas': 350, 'visita': 120}


def token_quote(n):
    """mesma conta de rec/fakebase/hooks/quotes.mjs (tokenDoOrcamento)"""
    return hashlib.sha256(f'dominex-fake-quote-{n}'.encode()).hexdigest()


def load(rel):
    with open(os.path.join(EXTRA, rel + '.json'), encoding='utf8') as f:
        return json.load(f)


def exists(rel):
    return os.path.exists(os.path.join(EXTRA, rel + '.json'))


def ultimo_t5():
    for n in range(40, 0, -1):
        rel = f't5/apos-cap{n:02d}'
        if exists(rel):
            return rel
    raise SystemExit('não achei nenhum t5/apos-capNN')


def linhas(chain, tabela):
    por_id = {}
    for rel in chain:
        if exists(rel):
            for r in load(rel).get(tabela, []):
                por_id[r.get('id') or id(r)] = r
    return list(por_id.values())


# ------------------------------------------------------------------ estoque do T8 (T08/roteiro.md, "Estado final")
# chave, nome, sku, unidade, grupo, saldo Estoque Principal, saldo Van 01 (None = sem linha), mínimo, custo, venda
MATERIAIS = [
    ('r410a', 'Gás refrigerante R-410A', 'EST-001', 'kg', 'gases', 16, 2, 10, 90.00, 150.00),
    ('r32', 'Gás refrigerante R-32', 'EST-002', 'kg', 'gases', 6, 0, 4, 98.00, 160.00),
    ('tubo14', 'Tubo de cobre 1/4"', 'EST-003', 'm', 'cobre', 45, None, 30, 16.00, 28.00),
    ('tubo38', 'Tubo de cobre 3/8"', 'EST-004', 'm', 'cobre', 22, None, 20, 26.00, 42.00),
    ('mangueira', 'Mangueira de dreno', 'EST-005', 'm', 'cobre', 60, None, 25, 3.50, 8.00),
    ('cap35', 'Capacitor 35 µF', 'EST-006', 'un', 'eletrica', 8, None, 4, 34.00, 62.00),
    ('limpa-evaporador', 'Limpa-evaporador em spray', 'EST-007', 'un', 'consumiveis', 10, None, 6, 20.00, 38.00),
    ('fita-isolante', 'Fita isolante', 'EST-008', 'rolos', 'consumiveis', 38, 0, 12, 6.50, 11.00),
    ('suporte', 'Suporte para condensadora', 'EST-009', 'un', 'consumiveis', 8, None, 4, 48.00, 85.00),
    ('cap40', 'Capacitor 40 µF', 'EST-010', 'un', 'eletrica', 13, None, 4, 38.90, 70.00),
    ('contator', 'Contator 25 A', 'EST-011', 'un', 'eletrica', 4, None, 2, 58.00, None),
    ('filtro', 'Filtro secador', 'EST-012', 'un', 'cobre', 6, None, 3, 21.50, None),
]
GRUPOS = [('gases', 'Gases', '#0EA5E9', 0), ('cobre', 'Cobre e tubos', '#F97316', 1), ('eletrica', 'Elétrica', '#EAB308', 2),
          ('consumiveis', 'Consumíveis', '#F59E0B', 3)]
CUSTO = {m[0]: m[8] for m in MATERIAIS}
VENDA = {m[0]: m[9] for m in MATERIAIS}
NOME_MAT = {m[0]: m[1] for m in MATERIAIS}


def estoque():
    out = {}
    out['stocks'] = [
        {'id': '@id:estoque.principal', 'company_id': EMP, 'name': 'Estoque Principal', 'is_default': True, 'sort_order': 0, 'customer_id': None,
         'created_at': '@now-90d', 'updated_at': '@now-90d'},
        {'id': '@id:estoque.van01', 'company_id': EMP, 'name': 'Van 01', 'is_default': False, 'sort_order': 1, 'customer_id': None,
         'created_at': '@now-12d', 'updated_at': '@now-12d'},
    ]
    out['material_groups'] = [{'id': f'@id:grupo.{k}', 'company_id': EMP, 'name': n, 'color': c, 'sort_order': o,
                               'created_at': '@now-90d', 'updated_at': '@now-90d'} for k, n, c, o in GRUPOS]
    inv, niveis = [], []
    for k, nome, sku, un, grupo, principal, van, minimo, custo, venda in MATERIAIS:
        total = principal + (van or 0)
        inv.append({'id': f'@id:material.{k}', 'company_id': EMP, 'name': nome, 'sku': sku, 'unit': un, 'quantity': total,
                    'min_quantity': minimo, 'cost_price': custo, 'sale_price': venda, 'group_id': f'@id:grupo.{grupo}',
                    'is_sellable': False, 'customer_id': None, 'created_at': '@now-90d', 'updated_at': '@now-5d'})
        niveis.append({'id': f'@id:nivel.{k}.principal', 'company_id': EMP, 'inventory_id': f'@id:material.{k}', 'stock_id': '@id:estoque.principal',
                       'quantity': principal, 'min_quantity': minimo, 'is_present': True, 'created_at': '@now-90d', 'updated_at': '@now-5d'})
        if van is not None:
            niveis.append({'id': f'@id:nivel.{k}.van01', 'company_id': EMP, 'inventory_id': f'@id:material.{k}', 'stock_id': '@id:estoque.van01',
                           'quantity': van, 'min_quantity': None, 'is_present': True, 'created_at': '@now-12d', 'updated_at': '@now-5d'})
    out['inventory'] = inv
    out['inventory_stock_levels'] = niveis
    return out


# ------------------------------------------------------------------ Financeiro padrão do cadastro
CATEGORIAS = [
    # nome, tipo, cor, ícone, dre_group, dfc_group, is_system   (self-register/index.ts:997-1015 + 20261020223000_...sql:18-45)
    ('Serviços Prestados', 'entrada', '#10b981', 'Wrench', 'opex', None, False),
    ('Vendas de Peças/Materiais', 'entrada', '#3b82f6', 'Package', 'opex', None, False),
    ('Contratos PMOC', 'entrada', '#8b5cf6', 'FileText', 'opex', None, False),
    ('Impostos e Taxas', 'saida', '#ef4444', 'Receipt', 'impostos', None, True),
    ('Custo de Materiais', 'saida', '#f59e0b', 'ShoppingCart', 'cmv', None, False),
    ('Fornecedores e Insumos', 'saida', '#6366f1', 'Truck', 'cmv', None, False),
    ('Alimentação', 'saida', '#ec4899', 'Coffee', 'opex', None, False),
    ('Luz/Energia', 'saida', '#eab308', 'Zap', 'opex', None, False),
    ('Aluguel', 'saida', '#14b8a6', 'Home', 'opex', None, False),
    ('Combustível/Transporte', 'saida', '#f97316', 'Car', 'opex', None, False),
    ('Salários e Encargos', 'saida', '#0ea5e9', 'Users', 'opex', None, False),
    ('Marketing e Publicidade', 'saida', '#a855f7', 'Megaphone', 'opex', None, False),
    ('Ferramentas e Equipamentos', 'saida', '#64748b', 'Hammer', 'opex', None, False),
    ('Outros', 'ambos', '#6b7280', 'Tag', 'opex', None, False),
    ('Tarifas e Taxas', 'saida', '#f59e0b', 'Receipt', 'impostos', None, True),
    ('CSP - Materiais', 'saida', '#8b5cf6', 'Package', 'cmv', None, True),
    ('CSP - Mão de Obra Avulsa', 'saida', '#06b6d4', 'Wrench', 'cmv', None, True),
    ('Vendas de Serviços', 'entrada', '#10b981', 'Briefcase', 'opex', None, True),
    ('Pagamento de Fatura', 'saida', '#6366f1', 'CreditCard', None, None, True),
    ('Transferência entre contas', 'saida', '#64748b', 'RefreshCw', None, None, True),
    ('Aporte de sócios', 'entrada', '#0ea5e9', 'HandCoins', 'outros', 'financiamento', True),
    ('Distribuição de lucros', 'saida', '#f97316', 'Handshake', 'outros', 'financiamento', True),
    ('Aplicação financeira', 'saida', '#0d9488', 'Landmark', 'outros', 'investimento', True),
    ('Resgate de aplicação', 'entrada', '#14b8a6', 'TrendingUp', 'outros', 'investimento', True),
    ('Aquisição de ativos', 'saida', '#7c3aed', 'Building2', 'outros', 'investimento', True),
    ('Venda de ativos', 'entrada', '#16a34a', 'BadgeDollarSign', 'outros', 'investimento', True),
    ('Empréstimos recebidos', 'entrada', '#2563eb', 'Banknote', 'outros', 'financiamento', True),
    ('Amortização de empréstimos', 'saida', '#dc2626', 'Landmark', 'outros', 'financiamento', True),
]


def financeiro():
    cats = []
    for i, (nome, tipo, cor, icone, dre, dfc, sis) in enumerate(CATEGORIAS):
        cats.append({'id': f'@id:fincat.{i:02d}', 'company_id': EMP, 'name': nome, 'type': tipo, 'color': cor, 'icon': icone,
                     'dre_group': dre, 'dfc_group': dfc, 'is_system': sis, 'is_active': True, 'sort_order': i,
                     'created_at': '@now-120d', 'updated_at': '@now-120d'})
    contas = [
        {'id': '@id:finacc.caixa', 'company_id': EMP, 'name': 'Caixa', 'type': 'caixa', 'color': '#10b981', 'icon': 'Wallet',
         'initial_balance': 0, 'sort_order': 0, 'is_active': True, 'created_at': '@now-120d', 'updated_at': '@now-120d'},
        {'id': '@id:finacc.principal', 'company_id': EMP, 'name': 'Conta Principal', 'type': 'banco', 'color': '#3b82f6', 'icon': 'Landmark',
         'initial_balance': 0, 'sort_order': 1, 'is_active': True, 'created_at': '@now-120d', 'updated_at': '@now-120d'},
    ]
    return {'financial_categories': cats, 'financial_accounts': contas}


# ------------------------------------------------------------------ funcionários (custo mensal fictício, salário 0)
FUNC = [
    ('rafael', 'Rafael Lima', 4480.00, '2023-02-06'), ('bruno', 'Bruno Alves', 4120.00, '2023-08-14'),
    ('julia', 'Júlia Santos', 4350.00, '2024-01-08'), ('lucas', 'Lucas Ferreira', 3980.00, '2024-05-20'),
    ('marina', 'Marina Costa', 4210.00, '2024-09-02'), ('paulo', 'Paulo Souza', 3760.00, '2025-03-17'),
]


def funcionarios():
    out = []
    for k, nome, custo, adm in FUNC:
        out.append({'id': f'@id:t9.func.{k}', 'company_id': EMP, 'name': nome, 'user_id': f'@id:user.{k}', 'position': 'Técnico de refrigeração',
                    'email': f'{nome.lower().split()[0].replace("ú", "u")}.{nome.lower().split()[1]}@glacialcold.example',
                    'monthly_cost': custo, 'salary': 0, 'is_active': True, 'employment_regime': 'clt', 'hire_date': adm,
                    'created_at': '@now-60d', 'updated_at': '@now-60d'})
    return {'employees': out}


# ------------------------------------------------------------------ propostas
TEMPLATES = [('clean', 'Clean', '#0f172a'), ('vanguarda', 'Vanguarda', '#22d3ee'), ('aurora', 'Aurora', '#ec4899'), ('prisma', 'Prisma', '#c084fc')]

# n, status, cliente (chave de customer.* | None), prospecto, criado (dias atrás), validade (dias a partir de hoje),
# itens [(tipo, chave, qtd, preço unit.)], desconto R$, visualizações [(quando)], parcelas
ORC = [
    (1, 'aprovado', 'padaria', None, 34, -19, [('s', 'higienizacao', 2, 180), ('s', 'preventiva', 1, 180), ('m', 'limpa-evaporador', 2, 38), ('m', 'mangueira', 3, 8)], 0, [], 1),
    (2, 'enviado', 'hotel', None, 29, 9, [('s', 'instalacao', 4, 650), ('m', 'tubo14', 10, 28), ('m', 'tubo38', 5, 42), ('m', 'fita-isolante', 10, 11)], 0,
     ['@now-4d', '@now-2d', '@at:-1d 16:20'], 3),
    (3, 'rascunho', 'clinica', None, 24, 6, [('s', 'preventiva', 2, 180), ('s', 'higienizacao', 1, 180)], 0, [], 1),
    (4, 'rejeitado', 'academia', None, 19, -4, [('s', 'instalacao', 2, 650), ('s', 'gas', 1, 350), ('m', 'r410a', 1, 150), ('m', 'tubo14', 1, 28), ('m', 'fita-isolante', 2, 11)], 0,
     ['@now-17d'], 1),
    (5, 'aprovado', 'restaurante', None, 14, -2, [('s', 'corretiva', 1, 220), ('s', 'gas', 1, 350), ('m', 'r410a', 1, 150), ('m', 'limpa-evaporador', 1, 38), ('m', 'fita-isolante', 2, 11)], 0, [], 1),
    (6, 'enviado', 'mercado', None, 9, 5, [('s', 'instalacao', 2, 650), ('m', 'r410a', 1, 150)], 0, ['@now-3d'], 1),
    (7, 'enviado', None, 'Casa de Repouso Vida Mansa', 6, 12, [('s', 'preventiva', 2, 180), ('s', 'higienizacao', 3, 180), ('m', 'limpa-evaporador', 2, 38), ('m', 'mangueira', 3, 8)], 20, [], 1),
    (8, 'rascunho', 'escritorio', None, 3, 14, [('s', 'instalacao', 3, 650), ('m', 'r410a', 1, 150)], 0, [], 1),
]


def orcamentos():
    qs, its, vs = [], [], []
    for n, status, cli, prosp, dias, valid, itens, desc, views, parcelas in ORC:
        subtotal = 0
        custo = 0.0
        for k, (tp, chave, qtd, preco) in enumerate(itens):
            total = round(qtd * preco, 2)
            subtotal += total
            ctot = round(qtd * CUSTO[chave], 2) if tp == 'm' else 0
            custo += ctot
            its.append({
                'id': f'@id:t9.qi.{n}.{k}', 'quote_id': f'@id:t9.quote.{n}', 'position': k, 'item_type': 'servico' if tp == 's' else 'material',
                'description': NOME_ST[chave] if tp == 's' else NOME_MAT[chave], 'details': None, 'quantity': qtd, 'unit_price': preco,
                'total_price': total, 'service_type_id': ST[chave] if tp == 's' else None,
                'inventory_id': None if tp == 's' else f'@id:material.{chave}', 'unit_labor_cost': 0, 'unit_materials_cost': 0,
                'unit_extras_cost': 0, 'unit_total_cost': 0 if tp == 's' else CUSTO[chave], 'unit_hourly_rate': 0, 'unit_hours': 0,
                'bdi': 1, 'profit_rate': 0, 'created_at': f'@now-{dias}d'})
        total_value = round(subtotal - desc, 2)
        q = {
            'id': f'@id:t9.quote.{n}', 'company_id': EMP, 'quote_number': n, 'token': token_quote(n), 'status': status,
            'customer_id': f'@id:customer.{cli}' if cli else None, 'prospect_name': prosp,
            'prospect_phone': '(21) 93000-4412' if prosp else None, 'prospect_email': 'contato@vidamansa.example' if prosp else None,
            'subtotal': round(subtotal, 2), 'discount_type': 'value' if desc else None, 'discount_value': desc or None, 'discount_amount': desc or None,
            'total_cost': round(custo, 2), 'total_price': total_value, 'total_value': total_value,
            'use_bdi': False, 'tax_rate': 0, 'admin_indirect_rate': 0, 'profit_rate': 0, 'bdi': 1, 'km_cost': 0, 'card_discount_rate': 0, 'card_installments': 0,
            'displacement_cost': 0, 'distance_km': 0, 'include_gifts': True, 'notes': None, 'terms': None,
            'valid_until': f'@today{valid:+d}d', 'proposal_template_id': '@id:t9.tpl.clean', 'receivable_installments': parcelas,
            'receivable_first_due_date': None, 'view_count': len(views), 'last_viewed_at': views[-1] if views else None,
            'financial_generated_at': None, 'financial_transaction_id': None, 'converted_to_os_id': None, 'assigned_to': None,
            'created_by': CAMILA, 'created_at': f'@now-{dias}d', 'updated_at': f'@now-{dias}d',
        }
        qs.append(q)
        for j, quando in enumerate(views):
            vs.append({'id': f'@id:t9.qv.{n}.{j}', 'quote_id': f'@id:t9.quote.{n}', 'company_id': EMP, 'fingerprint': f'fp-{n}-{j}',
                       'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36',
                       'viewed_at': quando})
    return {'quotes': qs, 'quote_items': its, 'quote_views': vs}


# ------------------------------------------------------------------ OS #16 (a do T5/T7, já concluída no T7) e o consumo dela
def os16_rows(chain_t5):
    todas = linhas(chain_t5, 'service_orders')
    achadas = [r for r in todas if r.get('order_number') == 16]
    if len(achadas) != 1:
        raise SystemExit(f'esperava uma OS #16, achei {len(achadas)}')
    base = dict(achadas[0])
    oid, tec = base['id'], base['technician_id']
    base.update({
        'status': 'concluida', 'scheduled_date': '@today-2d', 'scheduled_time': '09:00:00', 'duration_minutes': 120,
        'schedule_plan': [{'date': '@today-2d', 'time': '09:00', 'duration_minutes': 120}],
        'check_in_time': '@at:-2d 09:05', 'check_in_by': tec, 'started_at': '@at:-2d 09:05',
        'check_out_time': '@at:-2d 10:30', 'check_out_by': tec, 'completed_at': '@at:-2d 10:31', 'partial_finish': False,
        'created_at': '@now-6d', 'updated_at': '@at:-2d 10:31',
    })
    out = {'service_orders': [base]}
    for tab in ('service_order_assignees', 'service_order_service_types', 'service_order_equipment', 'service_order_equipment_service_types',
                'service_order_budget_items'):
        rs = [dict(r) for r in linhas(chain_t5, tab) if r.get('service_order_id') == oid]
        out[tab] = rs
    if not out['service_order_service_types']:
        out['service_order_service_types'] = [{'service_order_id': oid, 'service_type_id': base['service_type_id'], 'company_id': EMP, 'position': 0}]
    if not out['service_order_equipment_service_types']:
        out['service_order_equipment_service_types'] = [{'service_order_id': oid, 'equipment_id': base['equipment_id'],
                                                           'service_type_id': base['service_type_id'], 'company_id': EMP, 'position': 0}]
    out['service_order_materials'] = [
        {'id': '@id:t9.osmat.limpa', 'company_id': EMP, 'service_order_id': oid, 'inventory_id': '@id:material.limpa-evaporador',
         'stock_id': '@id:estoque.principal', 'quantity': 2, 'unit_cost': 20.0, 'created_at': '@at:-2d 09:05'},
        {'id': '@id:t9.osmat.fita', 'company_id': EMP, 'service_order_id': oid, 'inventory_id': '@id:material.fita-isolante',
         'stock_id': '@id:estoque.principal', 'quantity': 2, 'unit_cost': 6.5, 'created_at': '@at:-2d 09:05'},
    ]
    out['inventory_movements'] = [
        {'id': '@id:t9.mov.limpa', 'company_id': EMP, 'inventory_id': '@id:material.limpa-evaporador', 'stock_id': '@id:estoque.principal',
         'movement_type': 'consumo', 'quantity': -2, 'stock_before': 12, 'stock_after': 10, 'service_order_id': oid, 'unit_cost': 20.0,
         'notes': 'Consumo na OS #16', 'created_at': '@at:-2d 10:31'},
        {'id': '@id:t9.mov.fita', 'company_id': EMP, 'inventory_id': '@id:material.fita-isolante', 'stock_id': '@id:estoque.principal',
         'movement_type': 'consumo', 'quantity': -2, 'stock_before': 30, 'stock_after': 28, 'service_order_id': oid, 'unit_cost': 6.5,
         'notes': 'Consumo na OS #16', 'created_at': '@at:-2d 10:31'},
    ]
    return out, base


# ------------------------------------------------------------------ estados de ENSAIO (não entram na aula): servem para explorar a tela
# de um capítulo sem ter gravado os anteriores. As sementes de verdade (t9/apos-capNN) vêm das gravações (rec/t9/snap.mjs).
def dev_estados():
    van = '@id:t9.res.van01'
    itens_van = [('Depreciação mensal', 1400, True, None), ('Manutenção + Combustível', 1620, True, None),
                 ('Seguro', 300, False, 3600), ('Documentação / IPVA', 200, False, 2400)]
    mats = [('limpa-evaporador', 1), ('fita-isolante', 1), ('mangueira', 1)]
    a04 = {
        '_comentario': 'ENSAIO · estado depois do cap. 4 (Precificação 6/12/22, Van 01, custos da Higienização). Gerado por rec/t9/semear.py --dev.',
        '_patch': {'pricing_settings': [{'match': {'company_id': EMP}, 'set': {
            'tax_rate': 6, 'admin_indirect_rate': 12, 'default_profit_rate': 22, 'km_cost': 1.5, 'card_discount_rate': 5, 'card_installments': 10}}]},
        'cost_resources': [{'id': van, 'company_id': EMP, 'category': 'vehicle', 'name': 'Van 01', 'monthly_hours': 176, 'is_active': True,
                            'notes': None, 'photo_url': None, 'created_at': '@now-0m', 'updated_at': '@now-0m'}],
        'cost_resource_items': [{'id': f'@id:t9.resitem.{i}', 'resource_id': van, 'name': n, 'value': v, 'is_monthly': m, 'annual_value': a, 'sort_order': i}
                                for i, (n, v, m, a) in enumerate(itens_van)],
        'service_costs': [{'id': '@id:t9.svccost.hig', 'company_id': EMP, 'service_id': ST['higienizacao'], 'hourly_rate': 32, 'hours': 1.5,
                           'labor_cost': 48, 'extra_costs': [], 'notes': None, 'created_at': '@now-0m', 'updated_at': '@now-0m'}],
        'service_materials': [{'id': f'@id:t9.svcmat.{k}', 'company_id': EMP, 'service_id': ST['higienizacao'], 'stock_item_id': f'@id:material.{k}',
                               'item_name': NOME_MAT[k], 'quantity': q, 'purchase_price': CUSTO[k], 'subtotal': round(q * CUSTO[k], 2),
                               'unit': next(m[3] for m in MATERIAIS if m[0] == k), 'sort_order': i, 'created_at': '@now-0m'}
                              for i, (k, q) in enumerate(mats)],
        'service_cost_resources': [{'id': '@id:t9.svcres.van', 'service_id': ST['higienizacao'], 'resource_id': van, 'override_value': None}],
    }
    q9 = {
        '_comentario': 'ENSAIO · estado depois do cap. 9 (orçamento #9 da Pousada, Rascunho, R$ 1.000,00). Gerado por rec/t9/semear.py --dev.',
        'quotes': [{
            'id': '@id:t9.quote.9', 'company_id': EMP, 'quote_number': 9, 'token': token_quote(9), 'status': 'rascunho',
            'customer_id': '@id:customer.pousada', 'subtotal': 1040, 'discount_type': 'value', 'discount_value': 67, 'discount_amount': 67,
            'total_cost': 441, 'total_price': 735, 'total_value': 1000, 'tax_rate': 6, 'admin_indirect_rate': 12, 'profit_rate': 22, 'bdi': 0.6,
            'km_cost': 1.5, 'card_discount_rate': 5, 'card_installments': 10, 'displacement_cost': 27, 'distance_km': 18, 'include_gifts': True,
            'notes': 'Atendimento de segunda a sexta, das 8h às 17h.', 'terms': 'Serviço executado após a aprovação, com data combinada com o cliente.',
            'valid_until': '@today+15d', 'proposal_template_id': '@id:t9.tpl.clean', 'receivable_installments': 1, 'view_count': 0,
            'created_by': CAMILA, 'created_at': '@now-0m', 'updated_at': '@now-0m'}],
        'quote_items': [
            {'id': '@id:t9.qi.9.0', 'quote_id': '@id:t9.quote.9', 'position': 0, 'item_type': 'servico', 'description': 'Higienização de Split',
             'details': None, 'quantity': 3, 'unit_price': 180, 'total_price': 540, 'service_type_id': ST['higienizacao'], 'inventory_id': None,
             'unit_hourly_rate': 32, 'unit_hours': 1.5, 'unit_labor_cost': 48, 'unit_materials_cost': 30, 'unit_extras_cost': 30,
             'unit_total_cost': 108, 'profit_rate': 22, 'bdi': 0.6, 'created_at': '@now-0m'},
            {'id': '@id:t9.qi.9.1', 'quote_id': '@id:t9.quote.9', 'position': 1, 'item_type': 'servico', 'description': 'Carga de Gás',
             'details': None, 'quantity': 1, 'unit_price': 350, 'total_price': 350, 'service_type_id': ST['gas'], 'inventory_id': None,
             'unit_hourly_rate': 0, 'unit_hours': 0, 'unit_labor_cost': 0, 'unit_materials_cost': 0, 'unit_extras_cost': 0,
             'unit_total_cost': 0, 'profit_rate': 22, 'bdi': 0.6, 'price_override': 350, 'created_at': '@now-0m'},
            {'id': '@id:t9.qi.9.2', 'quote_id': '@id:t9.quote.9', 'position': 2, 'item_type': 'material', 'description': 'Gás refrigerante R-410A',
             'details': None, 'quantity': 1, 'unit_price': 150, 'total_price': 150, 'service_type_id': None, 'inventory_id': '@id:material.r410a',
             'unit_hourly_rate': 0, 'unit_hours': 0, 'unit_labor_cost': 0, 'unit_materials_cost': 90, 'unit_extras_cost': 0,
             'unit_total_cost': 90, 'profit_rate': 0, 'bdi': 1, 'created_at': '@now-0m'}],
    }
    a03 = {'_comentario': 'ENSAIO · estado depois do cap. 3 (Precificação 6/12/22 e a Van 01; ainda sem custos do serviço). Gerado por rec/t9/semear.py --dev.',
           '_patch': a04['_patch'], 'cost_resources': a04['cost_resources'], 'cost_resource_items': a04['cost_resource_items']}
    return {'apos-cap03': a03, 'apos-cap04': a04, 'apos-cap09': q9}


VAZIAS = ['tenant_tasks', 'financial_transactions', 'cost_centers', 'tenant_charges', 'cost_resources', 'cost_resource_items', 'service_costs',
          'service_materials', 'service_cost_resources', 'service_gifts', 'company_fiscal_settings', 'time_settings', 'cost_resources_with_rate',
          'os_sla_config', 'os_required_fields', 'os_photos', 'service_order_activities', 'form_responses']


def montar():
    t5 = ultimo_t5()
    chain_t5 = CHAIN_BASE + [t5]
    ini = {'_comentario': 'T9 · estado de partida = fim do T8 (OS #1 a #16, estoque do T8, Financeiro padrão) + bastidor do T9 (Precificação zerada, '
                          'modelos de proposta, funcionários, 8 orçamentos). Gerado por rec/t9/semear.py: não edite à mão.'}
    # status finais de #1 a #15 (os 2 patches do fim do T5; os outros patches de lá corrompem tabelas de ligação e ficam de fora)
    patches = [p for p in load(t5).get('_patch', {}).get('service_orders', [])]
    # G1 (1.38.19): trilha Domiflix sem tela escura de introdução nem faixa de lembrete. A linha já existe na base
    # (seeds/gen-03-domiflix.json, is_onboarding true): semente com o mesmo id DUPLICA, então vai por _patch no mesmo id (como o T12).
    ini['_patch'] = {'service_orders': patches,
                     'domiflix_learning_paths': [{'match': {'id': 'c0000000-0000-4000-8000-000000000001'}, 'set': {'is_onboarding': False}}]}
    # tabelas que o app consulta e que ficam vazias de propósito: sem linha de semente o /__dev/unknowns acusa TABELA_SEM_SEED
    for nome in VAZIAS:
        ini.setdefault(nome, [])
    os16, os16row = os16_rows(chain_t5)
    for k, v in os16.items():
        ini[k] = v
    for k, v in estoque().items():
        ini[k] = v
    for k, v in financeiro().items():
        ini[k] = v
    ini.update(funcionarios())
    ini['pricing_settings'] = [{'id': '@id:t9.pricing', 'company_id': EMP, 'tax_rate': 0, 'admin_indirect_rate': 0, 'default_profit_rate': 0,
                                'km_cost': 0, 'card_discount_rate': 0, 'card_installments': 1, 'created_at': '@now-90d', 'updated_at': '@now-90d'}]
    ini['proposal_templates'] = [{'id': f'@id:t9.tpl.{slug}', 'name': nome, 'slug': slug, 'preview_color': cor, 'description': None,
                                  'created_at': '@now-300d'} for slug, nome, cor in TEMPLATES]
    ini.update(orcamentos())
    return ini, os16row, t5


def verificar(ini):
    ids = set()
    for rel in CHAIN_BASE:
        ids |= set(re.findall(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', json.dumps(load(rel))))
    ids |= set(re.findall(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', json.dumps(load(ultimo_t5()))))
    ref = set(re.findall(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', json.dumps(ini)))
    faltam = sorted(ref - ids - {EMP})
    # ids literais que o inicio usa e a cadeia/base não traz (a base gen-* traz os da empresa, clientes etc. por @id:)
    print('ids literais fora da cadeia:', faltam if faltam else 'nenhum')
    return not faltam


def main():
    ini, os16row, t5 = montar()
    os.makedirs(os.path.join(EXTRA, 't9'), exist_ok=True)
    with open(os.path.join(EXTRA, 't9', 'inicio.json'), 'w', encoding='utf8') as f:
        json.dump(ini, f, ensure_ascii=False, indent=1)
    cad = {
        'fake_now': FAKE_NOW, 'inicio': CHAIN_BASE + ['t9/inicio'], 't5_usado': t5, 'os16': os16row['id'],
        'token9': token_quote(9), 'token2': token_quote(2), 'token6': token_quote(6),
        'nota': 'a OS gerada no cap. 15 sai #17 porque a cadeia não inclui as OS #17 a #22 do T5 (ver semear.py)',
    }
    with open(os.path.join(HERE, 'cadeia.json'), 'w', encoding='utf8') as f:
        json.dump(cad, f, ensure_ascii=False, indent=1)
    print('t9/inicio.json e rec/t9/cadeia.json gerados.')
    print('  OS #16:', os16row['id'], '| T5 usado:', t5)
    print('  tabelas:', {k: len(v) for k, v in ini.items() if isinstance(v, list)})
    print('  token do orçamento #9:', token_quote(9))
    verificar(ini)
    if '--dev' in sys.argv:
        os.makedirs(os.path.join(EXTRA, 't9', '_dev'), exist_ok=True)
        for nome, d in dev_estados().items():
            with open(os.path.join(EXTRA, 't9', '_dev', nome + '.json'), 'w', encoding='utf8') as f:
                json.dump(d, f, ensure_ascii=False, indent=1)
        print('  estados de ensaio em seeds-extra/t9/_dev/:', list(dev_estados()))


if __name__ == '__main__':
    main()
