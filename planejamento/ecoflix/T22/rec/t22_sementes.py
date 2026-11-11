#!/usr/bin/env python3
"""T22 · sementes da aula (rec/mundo/seeds-extra/t22/): a FILIAL de Pindamonhangaba e o estado de partida de cada capítulo.

  python3 -I rec/t22/t22_sementes.py            -> inicio.json, apos-cap02.json e apos-cap03.json (determinístico)

`inicio` = mundo base + a filial (plano.md, "Mundo: o que esta aula precisa"): empresa "Filial Pindamonhangaba" (CNPJ 47.318.506/0002-98,
plano Avançado, Mensal, Ativa, vence em 15/11/2026), a usuária Sandra Pires (MASTER da filial), cadastro próprio (os 15 materiais do mundo
com os mesmos nomes, tabela Principal, categorias, contas), e o histórico dela de 01/09 a 09/11 montado por plano: setembro com vendas de
R$ 66.000,00 e compras de R$ 57.000,00; OUTUBRO com vendas de R$ 72.000,00, compras de R$ 62.000,00 e CMV de R$ 55.000,00 (o estoque sobe
R$ 7.000,00 a custo); R$ 9.000,00 de despesas da operação por mês (folha, aluguel, energia e combustível); novembro com algumas compras e
vendas; latinha 1.850 kg em 10/11. Preço de compra único por material (o custo médio é o preço de compra em qualquer data: CMV por estoque
= CMV por venda). O grupo NÃO existe aqui (company_groups vazio).
`apos-cap02` = o grupo criado na tela (GRP-7C4E9A: o gerador do app só usa 0-9 e A-F; válido até 10/12/2026); `apos-cap03` = a filial vinculada.
Os números do GRUPO não são escritos em lugar nenhum: saem das RPCs (handlers) somando as unidades.
O script confere os totais da filial e para se algum não bater."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.normpath(os.path.join(HERE, '..', 'mundo', 'seeds-extra', 't22'))
F = '@id:company.filial_pinda'
SANDRA = '@id:user.sandra'
BANCO = '@id:t22.banco.principal'
COFRE = '@id:t22.banco.cofre'


def utc(dia, hhmm):
    """dia AAAA-MM-DD + HH:MM de Brasília -> ISO UTC"""
    h, m = int(hhmm[:2]), int(hhmm[3:])
    h += 3
    d = dia
    if h >= 24:   # não acontece nos horários usados (até 17:59)
        raise SystemExit('hora fora do dia')
    return f'{d}T{h:02d}:{m:02d}:00.000Z'


# ---------------------------------------------------------------- materiais (os 15 do mundo, mesmos nomes e preços)
MATS = [  # chave, código, nome, grupo, compra, venda
    ('ferro_pesado', '1', 'Ferro pesado', 'ferrosos', 0.95, 1.25),
    ('ferro_misto', '2', 'Ferro misto', 'ferrosos', 0.75, 1.05),
    ('chaparia', '3', 'Chaparia', 'ferrosos', 0.70, 0.98),
    ('cobre_mel', '4', 'Cobre mel', 'cobre', 42.50, 47.90),
    ('cobre_misto', '5', 'Cobre misto', 'cobre', 36.00, 41.50),
    ('fio_cobre', '6', 'Fio de cobre encapado', 'cobre', 18.00, 22.00),
    ('al_latinha', '7', 'Alumínio latinha', 'aluminio', 6.20, 7.40),
    ('al_perfil', '8', 'Alumínio perfil', 'aluminio', 8.90, 10.40),
    ('al_bloco', '9', 'Alumínio bloco', 'aluminio', 7.10, 8.50),
    ('latao', '10', 'Metal amarelo (latão)', 'metais', 27.50, 31.90),
    ('bronze', '11', 'Bronze', 'metais', 29.00, 33.50),
    ('inox', '12', 'Inox', 'metais', 5.80, 7.20),
    ('bateria', '13', 'Bateria automotiva', 'outros', 3.10, 3.90),
    ('papelao', '14', 'Papelão', 'outros', 0.55, 0.80),
    ('pet', '15', 'Plástico PET', 'outros', 1.90, 2.60),
]
M = {k: dict(code=c, nome=n, grupo=g, compra=pc, venda=pv) for k, c, n, g, pc, pv in MATS}
CENT_C = {k: int(round(M[k]['compra'] * 100)) for k in M}
CENT_V = {k: int(round(M[k]['venda'] * 100)) for k in M}
# NCM igual ao da matriz (o "Enviar Ativos" só mexe em material da filial sem NCM, sem código ou sem preço)
NCM = {'ferro_pesado': '7204.49.00', 'ferro_misto': '7204.49.00', 'chaparia': '7204.49.00', 'cobre_mel': '7404.00.00', 'cobre_misto': '7404.00.00',
       'fio_cobre': '7404.00.00', 'al_latinha': '7602.00.00', 'al_perfil': '7602.00.00', 'al_bloco': '7602.00.00', 'latao': '7404.00.00',
       'bronze': '7404.00.00', 'inox': '7204.21.00', 'bateria': '8549.11.00', 'papelao': '4707.10.00', 'pet': '3915.90.00'}
GRUPOS = [('ferrosos', 'Ferrosos', '#64748B'), ('cobre', 'Cobre', '#C2410C'), ('aluminio', 'Alumínio', '#0EA5E9'),
          ('metais', 'Metais', '#CA8A04'), ('outros', 'Outros', '#16A34A')]

# estoque da filial em 10/11 08:30 (latinha 1.850 kg: plano.md)
FINAL = {'ferro_pesado': 4200, 'ferro_misto': 6800, 'chaparia': 2100, 'cobre_mel': 35, 'cobre_misto': 120, 'fio_cobre': 80,
         'al_latinha': 1850, 'al_perfil': 260, 'al_bloco': 140, 'latao': 60, 'bronze': 25, 'inox': 180, 'bateria': 640,
         'papelao': 3900, 'pet': 520}

# ---------------------------------------------------------------- quantidades do mês (kg), resolvidas para os totais no centavo
# Vendas: dois "ajustadores" (papelão e ferro misto) fecham receita e custo exatos: 80X + 105Y = R, 55X + 75Y = C (centavos).
# Compras: ferro pesado e ferro misto fecham o custo exato: 95X + 75Y = R.


def fecha_vendas(base, receita, custo, aj=('papelao', 'ferro_misto')):
    a, b = aj
    R = receita * 100 - sum(q * CENT_V[k] for k, q in base.items())
    C = custo * 100 - sum(q * CENT_C[k] for k, q in base.items())
    det = CENT_V[a] * CENT_C[b] - CENT_V[b] * CENT_C[a]
    x_num = R * CENT_C[b] - CENT_V[b] * C
    y_num = CENT_V[a] * C - CENT_C[a] * R
    if x_num % det or y_num % det:
        return None
    x, y = x_num // det, y_num // det
    if x < 0 or y < 0:
        return None
    out = dict(base)
    out[a] = out.get(a, 0) + x
    out[b] = out.get(b, 0) + y
    return out


def resolve_vendas(base, receita, custo, mexe='ferro_pesado', passo=1, faixa=400):
    for d in range(0, faixa):
        for s in (d, -d):
            b = dict(base)
            b[mexe] = b.get(mexe, 0) + s * passo
            r = fecha_vendas(b, receita, custo)
            if r and r['papelao'] >= 1500 and r['ferro_misto'] >= 2000:
                return r
    raise SystemExit(f'vendas sem solução: {receita} / {custo}')


def resolve_compras(base, custo, a='ferro_pesado', b='ferro_misto', alvo_b=20000):
    """fecha o custo exato com `a` e `b`; entre as soluções, a de `b` mais perto de `alvo_b` kg"""
    R = custo * 100 - sum(q * CENT_C[k] for k, q in base.items())
    ca, cb = CENT_C[a], CENT_C[b]
    melhor = None
    for x in range(1000, R // ca + 1):
        resto = R - x * ca
        if resto >= 0 and resto % cb == 0 and resto // cb >= 1000:
            y = resto // cb
            if melhor is None or abs(y - alvo_b) < abs(melhor[1] - alvo_b):
                melhor = (x, y)
    if not melhor:
        raise SystemExit(f'compras sem solução: {custo}')
    out = dict(base)
    out[a] = out.get(a, 0) + melhor[0]
    out[b] = out.get(b, 0) + melhor[1]
    return out


# OUTUBRO: vendas R$ 72.000,00 com CMV R$ 55.000,00; compras R$ 62.000,00
VEND_OUT = resolve_vendas({'al_latinha': 1000, 'ferro_pesado': 6000, 'chaparia': 4200, 'cobre_misto': 100, 'cobre_mel': 50, 'latao': 80,
                           'al_perfil': 200, 'inox': 500, 'bateria': 800, 'pet': 600, 'fio_cobre': 120}, 72000, 55000)
COMP_OUT = resolve_compras({'al_latinha': 1900, 'chaparia': 5000, 'cobre_misto': 110, 'cobre_mel': 60, 'latao': 80, 'al_perfil': 340,
                            'al_bloco': 70, 'inox': 600, 'bateria': 1000, 'papelao': 6000, 'pet': 700, 'fio_cobre': 150, 'bronze': 10},
                           62000)
# SETEMBRO: vendas R$ 66.000,00; compras R$ 57.000,00 (o custo do vendido em setembro não é falado: R$ 50.500,00)
VEND_SET = resolve_vendas({'al_latinha': 900, 'ferro_pesado': 5600, 'chaparia': 3800, 'cobre_misto': 90, 'cobre_mel': 45, 'latao': 70,
                           'al_perfil': 180, 'inox': 450, 'bateria': 700, 'pet': 500, 'fio_cobre': 100}, 66000, 50500)
COMP_SET = resolve_compras({'al_latinha': 1500, 'chaparia': 4300, 'cobre_misto': 100, 'cobre_mel': 50, 'latao': 70, 'al_perfil': 300,
                            'al_bloco': 60, 'inox': 520, 'bateria': 800, 'papelao': 5200, 'pet': 600, 'fio_cobre': 120, 'bronze': 10},
                           57000)
# NOVEMBRO (03 a 09/11): algumas compras e vendas (sem total falado)
COMP_NOV = {'al_latinha': 420, 'ferro_pesado': 2600, 'ferro_misto': 1800, 'papelao': 1500, 'chaparia': 900, 'bateria': 300, 'pet': 200}
VEND_NOV = {'ferro_pesado': 3000, 'chaparia': 1500, 'al_latinha': 300, 'cobre_mel': 20, 'papelao': 2400}

# ---------------------------------------------------------------- calendário (dias úteis; 12/10 e 02/11 são feriado)
FERIADOS = {'2026-09-07', '2026-10-12', '2026-11-02'}


def dias_uteis(ini, fim):
    import datetime as dt
    d = dt.date.fromisoformat(ini)
    f = dt.date.fromisoformat(fim)
    out = []
    while d <= f:
        if d.weekday() < 5 and d.isoformat() not in FERIADOS:
            out.append(d.isoformat())
        d += dt.timedelta(days=1)
    return out


def reparte(total, n):
    """n partes inteiras quase iguais (as primeiras levam o resto)"""
    return [total // n + (1 if i < total % n else 0) for i in range(n)]


FORNECEDORES = [  # chave, nome, PF/PJ, documento, telefone
    ('joaquim', 'Joaquim Batista', 'PF', None, '(12) 90000-2201'),
    ('rosa', 'Rosa Medeiros', 'PF', None, '(12) 90000-2202'),
    ('mutirao', 'Cooperativa Mutirão Verde', 'PJ', '63.184.590/0001-70', '(12) 90000-2203'),
]
CLIENTES = [  # chave, nome, razão social, CNPJ, cidade, cobre/latão/alumínio x ferrosos
    ('bandeira', 'Fundição Bandeira do Vale', 'Fundição Bandeira do Vale Ltda', '94.716.352/0001-91'),
    ('toledo', 'Laminação Toledo Prado Ltda', 'Laminação Toledo Prado Ltda', '28.645.913/0001-84'),
]
DESPESAS = [  # categoria, valor do mês, dia útil do mês (índice), descrição
    ('folha', 5200.00, 4, 'Folha de pagamento da equipe da filial'),
    ('aluguel', 2400.00, 2, 'Aluguel do galpão de Pindamonhangaba'),
    ('energia', 980.00, 9, 'Conta de energia da filial'),
    ('combustivel', 420.00, 12, 'Diesel do caminhão da filial'),
]


def cnpj_ok(c):
    d = [int(x) for x in c if x.isdigit()]
    def dv(base, pesos):
        s = sum(a * b for a, b in zip(base, pesos)) % 11
        return 0 if s < 2 else 11 - s
    p1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    p2 = [6] + p1
    return dv(d[:12], p1) == d[12] and dv(d[:13], p2) == d[13]


def main():
    for _, _, _, doc, _ in FORNECEDORES:
        if doc and not cnpj_ok(doc):
            raise SystemExit(f'CNPJ inválido: {doc}')
    for _, _, _, doc in CLIENTES:
        if not cnpj_ok(doc):
            raise SystemExit(f'CNPJ inválido: {doc}')
    if not cnpj_ok('47.318.506/0002-98'):
        raise SystemExit('CNPJ da filial inválido')

    rows = {k: [] for k in ('companies', 'profiles', 'user_roles', 'user_shortcuts', 'company_modules', 'material_groups', 'materials',
                            'price_tables', 'price_table_items', 'suppliers', 'customers', 'bank_accounts', 'dre_groups',
                            'financial_categories', 'cost_centers', 'purchases', 'purchase_items', 'sales', 'sale_items',
                            'stock_movements', 'bank_transactions')}
    criado = '2026-08-25T13:00:00.000Z'
    rows['companies'].append({
        'id': F, 'name': 'Filial Pindamonhangaba', 'cnpj': '47.318.506/0002-98', 'email': 'pinda@reciclavalemetais.example',
        'phone': '(12) 90000-2200', 'address': 'Avenida das Indústrias, 1480 - Distrito Industrial, Pindamonhangaba - SP, 12412-220',
        'contact_name': 'Sandra Pires', 'timezone': 'America/Sao_Paulo', 'base_currency': 'BRL', 'subscription_status': 'active',
        'subscription_plan': 'avancado', 'subscription_value': 225, 'base_subscription_value': 225,
        'subscription_expires_at': '2026-11-15T23:59:59.000Z', 'billing_cycle': 'monthly', 'payment_method': 'boleto', 'ltv': 450,
        'max_users': 3, 'nfe_tier': 0, 'extra_users': 0, 'plan_locked': False, 'is_test_account': False, 'cash_account_enabled': True,
        'cash_account_opt_out': False, 'cash_account_seeded_at': '2026-09-01T10:30:00.000Z', 'multi_cash_enabled': False,
        'onboarding_completed_at': '2026-08-28T18:00:00.000Z', 'onboarding_state': {}, 'cato_enabled': False, 'white_label_enabled': False,
        'show_name_in_documents': True, 'show_cnpj_in_documents': True, 'show_address_in_documents': True, 'show_phone_in_documents': True,
        'show_email_in_documents': False, 'show_receipt_phrase': False, 'lat': -22.9246, 'lng': -45.4613, 'geocode_status': 'ok',
        'origin': 'site', 'allow_branch_stock_on_sale': False, 'created_at': criado, 'updated_at': '2026-11-01T12:00:00.000Z'})
    rows['profiles'].append({
        'id': SANDRA, 'email': 'sandra.pires@reciclavalemetais.example', 'full_name': 'Sandra Pires', 'company_id': F,
        'role': 'company_admin', 'permission_preset': 'full_access', 'is_active': True, 'must_change_password': False,
        'terms_accepted_at': '2026-08-25T13:01:00.000Z', 'preferred_language': 'pt-BR', 'preferred_currency': 'BRL',
        'default_payment_method': 'cash', 'balanca_ativada': False, 'direct_print_enabled': False, 'auto_print_receipts': False,
        'show_profit_on_receipt': False, 'multiple_price_tables_enabled': False, 'origin': 'cadastro', 'created_at': criado,
        'updated_at': '2026-11-01T12:00:00.000Z', 'cato_invite_seen_at': '2026-08-26T12:00:00.000Z'})
    rows['user_roles'].append({'id': '@id:t22.role.sandra', 'user_id': SANDRA, 'role': 'company_admin', 'created_at': criado})
    rows['user_shortcuts'].append({'id': '@id:t22.atalhos.sandra', 'user_id': SANDRA, 'shortcuts_enabled': True, 'custom_shortcuts': None,
                                   'created_at': criado, 'updated_at': criado})
    for mod in ('kit_basico', 'funcionarios'):
        rows['company_modules'].append({'id': f'@id:t22.company_module.{mod}', 'company_id': F, 'module_code': mod, 'added_at': criado,
                                        'removed_at': None, 'effective_until': None, 'price_override': None})
    for k, nome, cor in GRUPOS:
        rows['material_groups'].append({'id': f'@id:t22.grupo.{k}', 'company_id': F, 'name': nome, 'color': cor, 'icon': 'circle',
                                        'created_at': '2026-08-26T12:00:00.000Z', 'updated_at': '2026-08-26T12:00:00.000Z'})
    rows['price_tables'].append({'id': '@id:t22.tabela.principal', 'company_id': F, 'name': 'Principal', 'is_default': True,
                                 'is_linked': False, 'linked_to_table_id': None, 'created_at': '2026-08-26T12:20:00.000Z',
                                 'updated_at': '2026-08-26T12:20:00.000Z'})
    for k, c, n, g, pc, pv in MATS:
        rows['materials'].append({'id': f'@id:t22.material.{k}', 'company_id': F, 'code': c, 'name': n, 'fiscal_name': None,
                                  'group_id': f'@id:t22.grupo.{g}', 'unit': 'Kg', 'ncm': NCM[k], 'purchase_price': pc, 'sale_price': pv,
                                  'purchase_price_currency': 'BRL', 'sale_price_currency': 'BRL', 'current_stock': FINAL[k],
                                  'is_archived': False, 'created_by': SANDRA, 'created_at': '2026-08-26T12:10:00.000Z',
                                  'updated_at': '2026-11-09T12:00:00.000Z'})
        rows['price_table_items'].append({'id': f'@id:t22.pti.{k}', 'price_table_id': '@id:t22.tabela.principal',
                                          'material_id': f'@id:t22.material.{k}', 'purchase_price': pc, 'sale_price': pv,
                                          'is_override': False, 'created_at': '2026-08-26T12:20:00.000Z',
                                          'updated_at': '2026-08-26T12:20:00.000Z'})
    for i, (k, nome, tipo, doc, tel) in enumerate(FORNECEDORES):
        rows['suppliers'].append({'id': f'@id:t22.fornecedor.{k}', 'company_id': F, 'name': nome, 'nome_fantasia': None,
                                  'razao_social': nome, 'cpf_cnpj': doc, 'phone': tel, 'phone_unavailable': False, 'email': None,
                                  'contact_name': None, 'address': None, 'cidade': 'Pindamonhangaba', 'uf': 'SP', 'code': str(i + 1),
                                  'is_mei': False, 'created_by': SANDRA, 'created_at': '2026-08-27T12:00:00.000Z',
                                  'updated_at': '2026-08-27T12:00:00.000Z', 'indicador_ie': 9, 'inscricao_estadual': None,
                                  'linked_customer_id': None, 'is_industry': False, 'default_price_table_id': None})
    for i, (k, nome, razao, doc) in enumerate(CLIENTES):
        rows['customers'].append({'id': f'@id:t22.cliente.{k}', 'company_id': F, 'name': nome, 'nome_fantasia': None,
                                  'razao_social': razao, 'cpf_cnpj': doc, 'phone': f'(12) 90000-23{i + 1:02d}', 'phone_unavailable': False,
                                  'email': None, 'contact_name': None, 'address': None, 'cidade': 'Pindamonhangaba', 'uf': 'SP',
                                  'code': str(i + 1), 'is_mei': False, 'created_by': SANDRA, 'created_at': '2026-08-27T12:00:00.000Z',
                                  'updated_at': '2026-08-27T12:00:00.000Z', 'indicador_ie': 1, 'inscricao_estadual': None,
                                  'linked_supplier_id': None, 'is_industry': True, 'is_intermediary': False,
                                  'default_price_table_id': None, 'regime_tributario': 'lucro_real'})
    rows['bank_accounts'].append({'id': BANCO, 'company_id': F, 'name': 'Conta Principal', 'kind': 'bank', 'is_default': True,
                                  'is_protected': False, 'is_archived': False, 'institution_name': None, 'institution_code': None,
                                  'institution_ispb': None, 'color': '#2563EB', 'currency': 'BRL', 'balance': 0,
                                  'created_at': '2026-08-25T13:00:00.000Z', 'updated_at': '2026-08-25T13:00:00.000Z'})
    rows['bank_accounts'].append({'id': COFRE, 'company_id': F, 'name': 'DINHEIRO (COFRE)', 'kind': 'cash', 'is_default': False,
                                  'is_protected': True, 'is_archived': False, 'institution_name': 'Conta DINHEIRO (COFRE)',
                                  'institution_code': None, 'institution_ispb': None, 'color': '#22C55E', 'currency': 'BRL', 'balance': 0,
                                  'created_at': '2026-09-01T10:30:00.000Z', 'updated_at': '2026-09-01T10:30:00.000Z'})
    for i, (k, nome, nat) in enumerate((('receita_bruta', 'Receita de vendas', 'receita_bruta'), ('deducoes', 'Impostos e deduções', 'deducoes'),
                                         ('custos', 'Custos dos materiais vendidos', 'custos'),
                                         ('despesas_operacionais', 'Despesas operacionais', 'despesas_operacionais'),
                                         ('outras_receitas_despesas', 'Outras receitas e despesas', 'outras_receitas_despesas'))):
        rows['dre_groups'].append({'id': f'@id:t22.dre.{k}', 'company_id': F, 'name': nome, 'nature': nat, 'is_system': True,
                                   'sort_order': i, 'created_at': criado, 'updated_at': criado})
    CATS = [  # chave, nome, tipo, cor, dre_group, dre_group_id, sistema
        ('outras_receitas', 'Outras Receitas', 'income', '#000000', 'outros', 'outras_receitas_despesas', True),
        ('folha', 'Folha salarial', 'expense', '#EC4899', 'opex', 'despesas_operacionais', False),
        ('aluguel', 'Aluguel', 'expense', '#8B5CF6', 'opex', 'despesas_operacionais', False),
        ('energia', 'Energia elétrica', 'expense', '#F59E0B', 'opex', 'despesas_operacionais', False),
        ('combustivel', 'Combustível', 'expense', '#EF4444', 'opex', 'despesas_operacionais', False),
        ('tarifas', 'Tarifas', 'expense', '#000000', 'opex', 'despesas_operacionais', True),
        ('juros', 'Juros e Multas', 'expense', '#000000', 'nao_operacionais', 'outras_receitas_despesas', True),
        ('outras_despesas', 'Outras Despesas', 'expense', '#000000', 'opex', 'despesas_operacionais', True),
    ]
    for i, (k, nome, tipo, cor, dg, dgid, sis) in enumerate(CATS):
        rows['financial_categories'].append({'id': f'@id:t22.categoria.{k}', 'company_id': F, 'name': nome, 'type': tipo, 'color': cor,
                                             'icon': None, 'parent_id': None, 'dre_group': dg, 'dre_group_id': f'@id:t22.dre.{dgid}',
                                             'cash_flow_group': 'operacional', 'is_system': sis, 'sort_order': i, 'created_at': criado,
                                             'updated_at': criado})
    rows['cost_centers'].append({'id': '@id:t22.cc.patio', 'company_id': F, 'name': 'Pátio', 'color': '#F59E0B',
                                 'description': 'Balança, separação e armazenagem', 'icon': None, 'is_active': True, 'created_at': criado,
                                 'updated_at': criado})

    # ------------------------------------------------------------ histórico: pedidos, estoque e banco, em ordem cronológica
    eventos = []   # (instante ISO, tipo, dados)
    # saldo inicial em 01/09 08:00 = final - compras + vendas do período
    tot_c = {k: COMP_SET.get(k, 0) + COMP_OUT.get(k, 0) + COMP_NOV.get(k, 0) for k in M}
    tot_v = {k: VEND_SET.get(k, 0) + VEND_OUT.get(k, 0) + VEND_NOV.get(k, 0) for k in M}
    inicial = {k: FINAL[k] - tot_c[k] + tot_v[k] for k in M}
    neg = {k: v for k, v in inicial.items() if v < 0}
    if neg:
        raise SystemExit(f'saldo inicial negativo: {neg}')

    def pedidos_do_mes(qtd, dias, por_pedido, tipo, hora0, parceiros):
        """reparte as quantidades do mês em pedidos (1 a 3 materiais cada) pelos dias; devolve [(dia, hora, parceiro, [(mat, kg)])]"""
        mats = [k for k in M if qtd.get(k, 0) > 0]
        n = max(1, len(dias) // por_pedido)
        escolhidos = [dias[int(i * len(dias) / n)] for i in range(n)]
        cestas = [[] for _ in range(n)]
        for j, k in enumerate(mats):   # cada material em 2 pedidos do mês (1 se for pouco)
            partes = 2 if qtd[k] >= 200 else 1
            q = reparte(qtd[k], partes)
            for p in range(partes):
                cestas[(j * 2 + p * (n // 2 + 1)) % n].append((k, q[p]))
        out = []
        for i, cesta in enumerate(cestas):
            if not cesta:
                continue
            mins = hora0 + (i * 37) % 300
            out.append((escolhidos[i], f'{mins // 60:02d}:{mins % 60:02d}', parceiros[i % len(parceiros)], cesta))
        return out

    sete = dias_uteis('2026-09-01', '2026-09-30')
    outu = dias_uteis('2026-10-01', '2026-10-31')
    nove = dias_uteis('2026-11-03', '2026-11-09')
    forn = ['@id:t22.fornecedor.joaquim', None, '@id:t22.fornecedor.mutirao', '@id:t22.fornecedor.rosa', None]
    cli_metais = '@id:t22.cliente.bandeira'
    cli_ferro = '@id:t22.cliente.toledo'
    plano = []
    for qc, qv, dias in ((COMP_SET, VEND_SET, sete), (COMP_OUT, VEND_OUT, outu), (COMP_NOV, VEND_NOV, nove)):
        cedo = dias[:max(2, int(len(dias) * 0.6))]   # compras na primeira parte do mês, vendas na segunda (estoque nunca negativo)
        for d, h, p, cesta in pedidos_do_mes(qc, cedo, 1, 'purchase', 8 * 60 + 40, forn):
            plano.append((d, h, 'purchase', p, cesta))
        # vendas: metais não ferrosos para a Fundição, ferrosos/papel/plástico para a Laminação (dias da tarde)
        vm = {k: q for k, q in qv.items() if M[k]['grupo'] in ('cobre', 'aluminio', 'metais')}
        vf = {k: q for k, q in qv.items() if k not in vm}
        meio = dias[len(dias) // 2:] if len(dias) > 3 else dias
        for d, h, p, cesta in pedidos_do_mes(vm, meio, 2, 'sale', 15 * 60 + 10, [cli_metais]):
            plano.append((d, h, 'sale', p, cesta))
        for d, h, p, cesta in pedidos_do_mes(vf, meio, 3, 'sale', 16 * 60 + 5, [cli_ferro]):
            plano.append((d, h, 'sale', p, cesta))
    plano.sort(key=lambda x: (x[0], x[1]))

    saldo = dict(inicial)
    sm_n = [0]
    banco = [0.0]
    bt_n = [0]

    def mov(k, q, tipo, dia, hora, desc, oid=None, otipo=None):
        sm_n[0] += 1
        antes = saldo[k]
        saldo[k] = antes + q
        if saldo[k] < 0:
            raise SystemExit(f'estoque negativo: {k} em {dia} {hora}')
        rows['stock_movements'].append({'id': f'@id:t22.sm.{sm_n[0]}', 'company_id': F, 'material_id': f'@id:t22.material.{k}', 'type': tipo,
                                        'quantity': q, 'stock_before': antes, 'stock_after': saldo[k], 'order_id': oid, 'order_type': otipo,
                                        'description': desc, 'created_by': SANDRA, 'transaction_at': utc(dia, hora),
                                        'transaction_date': dia, 'created_at': utc(dia, hora)})

    def lanc_banco(valor, tipo, dia, hora, desc, oid=None, cat=None):
        bt_n[0] += 1
        banco[0] = round(banco[0] + valor, 2)
        r = {'id': f'@id:t22.bt.{bt_n[0]}', 'company_id': F, 'bank_account_id': BANCO, 'type': tipo, 'amount': round(valor, 2),
             'description': desc, 'transaction_at': utc(dia, hora), 'transaction_date': dia, 'created_at': utc(dia, hora),
             'created_by': SANDRA, 'source': 'manual', 'excluded_from_dre': False, 'payment_method': 'transfer', 'balance_after': banco[0]}
        if oid:
            r['order_id'] = oid
        if cat:
            r['category_id'] = cat
            r['cost_center_id'] = '@id:t22.cc.patio' if cat.endswith(('energia', 'aluguel')) else None
        rows['bank_transactions'].append(r)

    # saldo inicial do banco e do estoque (01/09)
    lanc_banco(85000.00, 'deposit', '2026-09-01', '08:05', 'Saldo inicial da conta')
    for k in M:
        if inicial[k] > 0:
            sm_n[0] += 1
            saldo[k] = inicial[k]
            rows['stock_movements'].append({'id': f'@id:t22.sm.{sm_n[0]}', 'company_id': F, 'material_id': f'@id:t22.material.{k}',
                                            'type': 'SALDO_INICIAL', 'quantity': inicial[k], 'stock_before': 0, 'stock_after': inicial[k],
                                            'order_id': None, 'order_type': None, 'description': 'Saldo inicial de estoque',
                                            'created_by': SANDRA, 'transaction_at': utc('2026-09-01', '08:00'),
                                            'transaction_date': '2026-09-01', 'created_at': utc('2026-09-01', '08:00')})
        else:
            saldo[k] = 0
    # despesas do mês (banco, com categoria)
    desp = []
    for mes, dias in (('09', sete), ('10', outu)):
        for cat, valor, idx, desc in DESPESAS:
            desp.append((dias[idx], '10:15', cat, valor, desc))
    num = 300
    for d, h, tipo, parc, cesta in plano + [(d, h, 'despesa', cat, (v, desc)) for d, h, cat, v, desc in desp]:
        pass
    agenda = sorted([(d, h, 'pedido', (tipo, parc, cesta)) for d, h, tipo, parc, cesta in plano] +
                    [(d, h, 'despesa', (cat, v, desc)) for d, h, cat, v, desc in desp], key=lambda x: (x[0], x[1]))
    for d, h, kind, dados in agenda:
        if kind == 'despesa':
            cat, v, desc = dados
            lanc_banco(-v, 'withdrawal', d, h, desc, cat=f'@id:t22.categoria.{cat}')
            continue
        tipo, parc, cesta = dados
        num += 1
        is_c = tipo == 'purchase'
        oid = f'@id:t22.{"compra" if is_c else "venda"}.{num}'
        itens = []
        total = 0
        for j, (k, q) in enumerate(cesta):
            preco = M[k]['compra'] if is_c else M[k]['venda']
            tp = round(q * preco, 2)
            total = round(total + tp, 2)
            itens.append({'id': f'@id:t22.{"pi" if is_c else "si"}.{num}.{j}', ('purchase_id' if is_c else 'sale_id'): oid,
                          'material_id': f'@id:t22.material.{k}', 'material_name': M[k]['nome'], 'quantity': q, 'unit_price': preco,
                          'total_price': tp, 'impurity': 0, 'impurity_kg': None, 'impurity_pct': None, 'item_discount': 0,
                          'tare_weight': None, 'first_weight': None, 'second_weight': None, 'weighing_mode': None,
                          'weight_source': 'manual'})
        ped = {'id': oid, 'company_id': F, 'order_number': num, 'order_seq': num, 'order_period': None, 'order_ref': f'#{num}',
               'status': 'completed', 'total_amount': total, 'paid_amount': total, 'payment_method': 'transfer', 'created_by': SANDRA,
               'transaction_at': utc(d, h), 'transaction_date': d, 'created_at': utc(d, h), 'currency': 'BRL',
               'hide_financial_details': False, 'notes': None, 'driver_name': None, 'vehicle_plate': None, 'driver_id': None,
               'vehicle_id': None, ('supplier_id' if is_c else 'customer_id'): parc}
        rows['purchases' if is_c else 'sales'].append(ped)
        rows['purchase_items' if is_c else 'sale_items'].extend(itens)
        for k, q in cesta:
            mov(k, q if is_c else -q, 'COMPRA' if is_c else 'VENDA', d, h, f'{"Compra" if is_c else "Venda"} #{num}', oid,
                'purchase' if is_c else 'sale')
        lanc_banco(-total if is_c else total, 'withdrawal' if is_c else 'deposit', d, h, f'{"Compra" if is_c else "Venda"} #{num}', oid)

    rows['bank_accounts'][0]['balance'] = banco[0]

    # ------------------------------------------------------------ conferências
    def soma(tab, mes):
        return round(sum(p['total_amount'] for p in rows[tab] if p['transaction_date'].startswith(mes)), 2)

    def custo_vendido(mes):
        ids = {p['id'] for p in rows['sales'] if p['transaction_date'].startswith(mes)}
        return round(sum(i['quantity'] * M[i['material_id'].split('.')[-1]]['compra'] for i in rows['sale_items'] if i['sale_id'] in ids), 2)

    conf = [('vendas de outubro', soma('sales', '2026-10'), 72000.00), ('compras de outubro', soma('purchases', '2026-10'), 62000.00),
            ('CMV de outubro', custo_vendido('2026-10'), 55000.00), ('vendas de setembro', soma('sales', '2026-09'), 66000.00),
            ('compras de setembro', soma('purchases', '2026-09'), 57000.00)]
    for nome, tem, quer in conf:
        if abs(tem - quer) > 0.004:
            raise SystemExit(f'sementes t22: {nome} = {tem}, esperado {quer}')
    for mes in ('2026-09', '2026-10'):
        d = round(sum(-b['amount'] for b in rows['bank_transactions'] if b.get('category_id') and b['transaction_date'].startswith(mes)), 2)
        if abs(d - 9000.00) > 0.004:
            raise SystemExit(f'despesas de {mes} = {d}')
    for k in M:
        if saldo[k] != FINAL[k]:
            raise SystemExit(f'estoque final de {k}: {saldo[k]} != {FINAL[k]}')
        if not any(i['material_id'].endswith('.' + k) for i in rows['purchase_items']
                   if next(p for p in rows['purchases'] if p['id'] == i['purchase_id'])['transaction_date'] <= '2026-09-30'):
            raise SystemExit(f'{k} sem compra em setembro (o custo médio de 30/09 sairia zero)')
    os.makedirs(SAIDA, exist_ok=True)
    json.dump(rows, open(os.path.join(SAIDA, 'inicio.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)

    grupo = {'company_groups': [{'id': '@id:t22.grupo', 'name': 'Grupo Recicla Vale', 'owner_company_id': '@id:company.reciclavale',
                                 'invite_code': 'GRP-7C4E9A', 'invite_code_expires_at': '2026-12-10T11:34:00.000Z', 'max_members': 10,
                                 'require_transfer_approval': False, 'asaas_subscription_id': None,
                                 'created_at': '2026-11-10T11:34:00.000Z'}]}
    json.dump(grupo, open(os.path.join(SAIDA, 'apos-cap02.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    membro = {'company_group_members': [{'id': '@id:t22.membro.filial', 'group_id': '@id:t22.grupo', 'company_id': F,
                                         'joined_at': '2026-11-10T11:41:00.000Z', 'status': 'active'}]}
    json.dump(membro, open(os.path.join(SAIDA, 'apos-cap03.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)

    print(f"filial: {len(rows['purchases'])} compras, {len(rows['sales'])} vendas, {len(rows['stock_movements'])} movimentos, "
          f"{len(rows['bank_transactions'])} lançamentos; banco R$ {banco[0]:,.2f}")
    for nome, tem, quer in conf:
        print(f'  ok {nome}: {tem:,.2f}')
    print('  saldo inicial 01/09:', {k: v for k, v in inicial.items()})
    print('  vendas out:', VEND_OUT)
    print('  compras out:', COMP_OUT)


if __name__ == '__main__':
    main()
