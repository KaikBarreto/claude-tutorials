#!/usr/bin/env python3
"""T13 · gera o mundo de partida do Financeiro (rec/fakebase/seeds-extra/t13/inicio.json) e rec/t13/cadeia.json.

Estado de partida = fim do T12 (cadeia do T12: t12/inicio + t12/apos-cap11) + o que o T13 exige e o T8/T9/T11 deixam:
  - estoque do T8 (Estoque Principal + Van 01, Mangueira de dreno com 60 m, custo 3,50) e Financeiro padrão do cadastro (Caixa, Conta Principal,
    14 + 14 categorias) e os 6 grupos do DRE, com `dre_group_id` das categorias (imitam os gatilhos do app; o fakebase não tem gatilho);
  - T9: as 3 parcelas da aprovação do Orçamento #2 (Hotel Mirante do Mar), vencimentos 20/11/2026, 20/12/2026 e 20/01/2027;
  - T11: as 12 "Mensalidade PMOC" do contrato do hotel (R$ 1.200,00, dia 10, de 10/12/2026 a 10/11/2027, Contratos PMOC, Conta Principal).
O T10 e o T11 ainda não foram gravados; nada do T13 depende de dado novo deles além do que está acima (o contrato do hotel vem do t12/inicio).
Os ids de cliente/contrato vêm da cadeia do T12. Rodar de qualquer pasta:  python3 -I rec/t13/semear.py
"""
import importlib.util
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
EXTRA = os.path.normpath(os.path.join(HERE, '..', 'fakebase', 'seeds-extra'))
FAKE_NOW = '2026-11-10T10:00:00-03:00'
EMP = '9c307966-79f1-567c-ac4d-d5fd3c1a2f40'
CAMILA = 'd40f5787-1779-501f-900c-ddb2b90a36e5'
HOTEL = 'cbed8554-3919-5fa8-b9c6-5d13ef24cf37'
CONTRATO_HOTEL = '@id:t12.contrato.hotel'
PRINCIPAL = '@id:finacc.principal'

spec = importlib.util.spec_from_file_location('t9semear', os.path.join(HERE, '..', 't9', 'semear.py'))
t9 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t9)

C12 = json.load(open(os.path.join(HERE, '..', 't12', 'cadeia.json'), encoding='utf8'))
CADEIA = list(C12['inicio']) + ['t12/apos-cap11']

# grupos do DRE do sistema (seed_system_dre_groups, 20261021110000_renomeia_grupo_receita_dre.sql:35-50)
GRUPOS = [('revenue', 'Receitas de serviços', 10), ('deduction', 'Impostos sobre vendas', 20), ('cost', 'Custos diretos', 30),
          ('operating_expense', 'Despesas com pessoal', 40), ('non_operating', 'Resultado financeiro', 50), ('excluded', 'Excluídos do DRE', 60)]


def natureza(cat):
    """mesma regra do gatilho sync_financial_category_dre_group (20261021090000_dre_groups_configuraveis.sql)"""
    g, tipo = cat['dre_group'], cat['type']
    if g == 'opex' and tipo == 'entrada':
        return 'revenue'
    if g == 'impostos':
        return 'deduction'
    if g == 'cmv':
        return 'cost'
    if g == 'opex' or g is None:
        return 'operating_expense'
    if g == 'nao_operacional':
        return 'non_operating'
    return 'excluded'


def t(dia, hora='13:00:00'):
    return f'{dia}T{hora}.000Z'


def parcela(base, **kw):
    r = {'accrual_amount': None, 'amount_received': 0, 'asaas_payment_id': None, 'bill_id': None, 'billing_reminder_resolved_at': None,
         'billing_reminder_resolved_by': None, 'cancelled_at': None, 'cancelled_reason': None, 'card_installments': None, 'contract_id': None,
         'cost_center_id': None, 'credit_card_bill_date': None, 'employee_id': None, 'notes': None, 'origin': None, 'parent_transaction_id': None,
         'payment_group_id': None, 'payment_method': None, 'payroll_kind': None, 'payroll_period': None, 'receipt_url': None,
         'service_order_id': None, 'supplier_id': None, 'tenant_charge_id': None, 'transfer_pair_id': None, 'paid_date': None, 'is_paid': False,
         'company_id': EMP, 'created_by': CAMILA, 'transaction_type': 'entrada', 'customer_id': HOTEL, 'account_id': PRINCIPAL}
    r.update(base)
    r.update(kw)
    return r


def montar():
    ini = {'_comentario': 'T13 · fim do T12 + estoque do T8, Financeiro padrão do cadastro, 3 parcelas do Orçamento #2 (T9) e 12 mensalidades do PMOC (T11). '
                          'Gerado por rec/t13/semear.py: não edite à mão.'}
    # G1 (1.38.19): trilha Domiflix sem tela escura de introdução nem faixa de lembrete (a linha existe na base com is_onboarding true; _patch no id)
    ini['_patch'] = {'domiflix_learning_paths': [{'match': {'id': 'c0000000-0000-4000-8000-000000000001'}, 'set': {'is_onboarding': False}}]}
    for k, v in t9.estoque().items():
        ini[k] = v
    fin = t9.financeiro()
    ini['dre_groups'] = [{'id': f'@id:t13.dre.{nat}', 'company_id': EMP, 'name': nome, 'nature': nat, 'sort_order': ordem, 'is_system': True,
                          'is_active': True, 'created_at': '@now-120d', 'updated_at': '@now-120d'} for nat, nome, ordem in GRUPOS]
    for cat in fin['financial_categories']:
        cat['sort_order'] = 0   # DEFAULT 0 do banco (os gatilhos/cadastro não definem): as listas saem em ordem alfabética (`order sort_order, name`), como no app real
        cat['dre_group_id'] = f'@id:t13.dre.{natureza(cat)}'
    ini['financial_categories'] = fin['financial_categories']
    for conta in fin['financial_accounts']:
        conta['is_cash_account'] = True   # o cadastro cria as duas "dentro do caixa" (self-register/index.ts:1031-1037)
    ini['financial_accounts'] = fin['financial_accounts']
    # tabelas que o Financeiro consulta e que ficam vazias de propósito (o que aparecer em /__dev/unknowns a mais é falha de verdade)
    for nome in ['credit_card_bills', 'cost_centers', 'financial_transactions', 'user_preferences', 'compras', 'compra_materiais', 'compra_cotacoes',
                 'compra_cotacao_precos', 'compra_ordens', 'compra_ordem_itens', 'inventory_movements', 'tenant_charges', 'financial_transaction_attachments', 'inventory_low_stock']:
        ini.setdefault(nome, [])

    trans = []
    # --- T9: aprovação do Orçamento #2 (3 parcelas)
    grupo = '1e769453-03d1-40bf-8937-b7112359f2c7'
    for i, (valor, dia) in enumerate([(1066.67, '2026-11-20'), (1066.67, '2026-12-20'), (1066.66, '2027-01-20')], 1):
        trans.append(parcela({'id': f'@id:t13.orc2.{i}', 'amount': valor, 'description': f'Orçamento #2 ({i}/3)', 'category': 'Vendas de Serviços',
                              'transaction_date': dia, 'due_date': dia, 'installment_group_id': grupo, 'installment_number': i, 'installment_total': 3,
                              'created_at': t('2026-11-03', '12:00:00'), 'updated_at': t('2026-11-03', '12:00:00')}))
    # --- T11: 12 mensalidades do contrato PMOC do hotel (dez/2026 a nov/2027)
    meses = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
    for i in range(12):
        a, m = 2026 + (11 + i) // 12, (11 + i) % 12 + 1
        dia = f'{a:04d}-{m:02d}-10'
        # o contrato grava as parcelas SEM installment_* (pages/ContractDetail.tsx:1005-1033): a numeração "(n/12)" só vai na descrição, e o
        # recebimento parcial (ReceivePaymentModal, `installmentTotal > 1` o desliga) fica liberado, como o roteiro mostra no cap. 11
        trans.append(parcela({'id': f'@id:t13.pmoc.{i + 1}', 'amount': 1200.0, 'description': f'Mensalidade PMOC - {meses[m - 1]}/{a} ({i + 1}/12)',
                              'category': 'Contratos PMOC', 'transaction_date': dia, 'due_date': dia, 'contract_id': CONTRATO_HOTEL,
                              'notes': 'Vinculado ao contrato: PMOC - Hotel Mirante do Mar',
                              'created_at': t('2026-11-10', '12:30:00'), 'updated_at': t('2026-11-10', '12:30:00')}))
    ini['financial_transactions'] = trans
    # funcionários que o T9 semeia para a calculadora de mão de obra (só `monthly_cost`, salário 0; o T15 completa): a janela "Nova Conta" os consulta
    ini.update(t9.funcionarios())
    return ini


def verificar(ini):
    ids = set()
    for rel in CADEIA:
        with open(os.path.join(EXTRA, rel + '.json'), encoding='utf8') as f:
            ids |= set(re.findall(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', f.read()))
    ref = set(re.findall(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', json.dumps(ini)))
    print('ids literais fora da cadeia:', sorted(ref - ids - {EMP}) or 'nenhum')


def main():
    ini = montar()
    os.makedirs(os.path.join(EXTRA, 't13'), exist_ok=True)
    with open(os.path.join(EXTRA, 't13', 'inicio.json'), 'w', encoding='utf8') as f:
        json.dump(ini, f, ensure_ascii=False, indent=1)
    cad = {'fake_now': FAKE_NOW, 'inicio': CADEIA + ['t13/inicio'], 'hotel': HOTEL, 'contrato_hotel': CONTRATO_HOTEL,
           'nota': 'mundo do T13 = fim do T12 (t12/apos-cap11) + t13/inicio; apos-capNN do T13 são cumulativos sobre t13/inicio'}
    with open(os.path.join(HERE, 'cadeia.json'), 'w', encoding='utf8') as f:
        json.dump(cad, f, ensure_ascii=False, indent=1)
    print('t13/inicio.json e rec/t13/cadeia.json gerados.')
    print('  tabelas:', {k: len(v) for k, v in ini.items() if isinstance(v, list)})
    verificar(ini)


if __name__ == '__main__':
    main()
