#!/usr/bin/env python3
"""T20 · gera o mundo de partida do Relatório Financeiro e DRE (rec/fakebase/seeds-extra/t20/inicio.json) e rec/t20/cadeia.json.

Estado de partida = fim do T19 (cadeia do T19 + a semente final dele, `T19_FINAL`) + o histórico de agosto a outubro de 2026 do roteiro
(T20/roteiro.md, "Estado inicial"): receitas "Vendas de Serviços" com cliente, custos diretos com o mesmo cliente, aluguel, combustível, tarifas e o
Simples Nacional ("Impostos e Taxas"). Tudo na Conta Principal. O saldo inicial dela cai pelo líquido pago do histórico, de modo que o saldo de hoje
continue o do fim do T13/T19 (o histórico "já estava" na conta). As 28 categorias, os 6 grupos do DRE e o `dre_group_id` de cada categoria vêm do
`t13/inicio`; este arquivo não cria categoria nem grupo.
Rodar de qualquer pasta:  python3 -I rec/t20/semear.py        (semente final do T19 diferente: T19_FINAL=t19/apos-cap13 python3 -I rec/t20/semear.py)
"""
import json
import os
import re
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
EXTRA = os.path.normpath(os.path.join(HERE, '..', 'fakebase', 'seeds-extra'))
FAKE_NOW = '2026-11-10T10:00:00-03:00'
EMP = '9c307966-79f1-567c-ac4d-d5fd3c1a2f40'
CAMILA = 'd40f5787-1779-501f-900c-ddb2b90a36e5'
PRINCIPAL = '@id:finacc.principal'
T19_FINAL = os.environ.get('T19_FINAL', 't19/apos-cap12')

C19 = json.load(open(os.path.join(HERE, '..', 't19', 'cadeia.json'), encoding='utf8'))
CADEIA = list(C19['inicio']) + [T19_FINAL]

CL = {'hotel': '@id:customer.hotel', 'condominio': '@id:customer.condominio', 'clinica': '@id:customer.clinica', 'padaria': '@id:customer.padaria',
      'farmacia': '@id:customer.farmacia', 'mercado': '@id:customer.mercado', 'escritorio': '@id:customer.escritorio',
      'restaurante': '@id:customer.restaurante', 'academia': '@id:customer.academia', 'pousada': '@id:customer.pousada'}
NOME = {'hotel': 'Hotel Mirante do Mar', 'condominio': 'Condomínio Jardim Azul', 'clinica': 'Clínica Sorriso Leve', 'padaria': 'Padaria Bom Grão',
        'farmacia': 'Farmácia Vida Plena', 'mercado': 'Mercado Vila Nova', 'escritorio': 'Escritório Lemos & Prado',
        'restaurante': 'Restaurante Sabor da Serra', 'academia': 'Academia Ponto Forte', 'pousada': 'Pousada Brisa do Mar'}
MAT, MOA, PECAS = 'CSP - Materiais', 'CSP - Mão de Obra Avulsa', 'Peças e componentes'
SERV = ['Instalação de split', 'Manutenção preventiva', 'Higienização de equipamentos', 'Reparo em sistema de refrigeração', 'Instalação de câmara fria']

# (data, cliente, valor, recebida em (None = no dia)) · custos: (data, cliente, valor, categoria) · estrutura: (data, descrição, categoria, valor)
MESES = {
    '2026-08': {
        'rec': [('03', 'hotel', 2400), ('12', 'condominio', 2300), ('07', 'clinica', 1080), ('14', 'padaria', 950), ('18', 'farmacia', 1650),
                ('20', 'mercado', 780), ('24', 'hotel', 4200), ('26', 'escritorio', 720), ('28', 'restaurante', 2320)],
        'custo': [('03', 'hotel', 1640, MAT), ('03', 'hotel', 600, MOA), ('12', 'condominio', 820, MAT), ('18', 'farmacia', 540, MAT),
                  ('20', 'mercado', 260, MAT), ('28', 'restaurante', 690, PECAS)],
        'estr': [('10', 'Aluguel do galpão', 'Aluguel', 2800), ('15', 'Combustível das visitas', 'Combustível/Transporte', 760),
                 ('30', 'Tarifa bancária', 'Tarifas e Taxas', 38.90)],
        'simples': ('31', 984.00),
    },
    '2026-09': {
        'rec': [('02', 'hotel', 4800), ('09', 'academia', 4600), ('11', 'padaria', 540), ('15', 'clinica', 1260), ('17', 'condominio', 1850),
                ('19', 'farmacia', 360), ('23', 'mercado', 2150), ('25', 'pousada', 1590), ('29', 'restaurante', 2700)],
        'custo': [('02', 'hotel', 2650, PECAS), ('02', 'hotel', 700, MOA), ('09', 'academia', 1380, MAT), ('15', 'clinica', 120, MAT), ('19', 'farmacia', 60, MAT), ('23', 'mercado', 640, PECAS), ('25', 'pousada', 480, MAT),
                  ('29', 'restaurante', 980, PECAS)],
        'estr': [('10', 'Aluguel do galpão', 'Aluguel', 2800), ('16', 'Combustível das visitas', 'Combustível/Transporte', 820),
                 ('30', 'Tarifa bancária', 'Tarifas e Taxas', 42.50)],
        'simples': ('30', 1191.00),
    },
    '2026-10': {
        'rec': [('01', 'hotel', 1900), ('08', 'padaria', 950), ('13', 'clinica', 1080), ('16', 'mercado', 690), ('20', 'farmacia', 480),
                ('22', 'escritorio', 1780), ('24', 'restaurante', 720), ('28', 'condominio', 2300, '2026-11-03'), ('30', 'hotel', 4050)],
        'custo': [('01', 'hotel', 1610, MAT), ('30', 'hotel', 720, PECAS), ('22', 'escritorio', 320, MAT), ('22', 'escritorio', 200, MOA), ('28', 'condominio', 760, MAT),
                  ('16', 'mercado', 210, MAT), ('13', 'clinica', 110, MAT), ('08', 'padaria', 90, MAT)],
        'estr': [('10', 'Aluguel do galpão', 'Aluguel', 2800), ('14', 'Combustível das visitas', 'Combustível/Transporte', 690),
                 ('30', 'Tarifa bancária', 'Tarifas e Taxas', 35.20)],
        'simples': ('31', 837.00),
    },
}


def t(dia, hora='13:00:00'):
    return f'{dia}T{hora}.000Z'


def prox_mes(ym, dia):
    a, m = int(ym[:4]), int(ym[5:])
    a, m = (a + 1, 1) if m == 12 else (a, m + 1)
    return f'{a:04d}-{m:02d}-{dia}'


def linha(n, tipo, ym, dia, desc, cat, valor, cliente=None, paga_em='mesmo', venc=None):
    """uma transação do histórico: lançada em `ym-dia`, paga na mesma data (ou em `paga_em`; None = a pagar)"""
    d = f'{ym}-{dia}'
    pago = paga_em is not None
    pd = d if paga_em == 'mesmo' else paga_em
    r = {'accrual_amount': None, 'amount_received': 0, 'asaas_payment_id': None, 'bill_id': None, 'billing_reminder_resolved_at': None,
         'billing_reminder_resolved_by': None, 'cancelled_at': None, 'cancelled_reason': None, 'card_installments': None, 'contract_id': None,
         'cost_center_id': None, 'credit_card_bill_date': None, 'employee_id': None, 'notes': None, 'origin': None, 'parent_transaction_id': None,
         'payment_group_id': None, 'payroll_kind': None, 'payroll_period': None, 'receipt_url': None, 'service_order_id': None, 'supplier_id': None,
         'tenant_charge_id': None, 'transfer_pair_id': None, 'installment_group_id': None, 'installment_number': None, 'installment_total': None,
         'company_id': EMP, 'created_by': CAMILA, 'account_id': PRINCIPAL,
         'id': f'@id:t20.h.{n:03d}', 'transaction_type': tipo, 'amount': valor, 'description': desc, 'category': cat,
         'customer_id': CL[cliente] if cliente else None, 'transaction_date': d, 'due_date': venc or d,
         'is_paid': pago, 'paid_date': pd if pago else None, 'payment_method': 'pix' if pago else None,
         'created_at': t(d), 'updated_at': t(d)}
    return r


def historico():
    rows, n = [], 0
    for ym, m in MESES.items():
        for i, r in enumerate(m['rec']):
            dia, cli, valor = r[0], r[1], r[2]
            recebida = r[3] if len(r) > 3 else 'mesmo'
            n += 1
            rows.append(linha(n, 'entrada', ym, dia, f'{SERV[(n + i) % len(SERV)]} - {NOME[cli]}', 'Vendas de Serviços', valor, cli, recebida))
        for dia, cli, valor, cat in m['custo']:
            n += 1
            desc = {MAT: 'Gás e tubos de cobre', MOA: 'Ajudante avulso', PECAS: 'Compressor e capacitores'}[cat]
            rows.append(linha(n, 'saida', ym, dia, f'{desc} - {NOME[cli]}', cat, valor, cli))
        for dia, desc, cat, valor in m['estr']:
            n += 1
            rows.append(linha(n, 'saida', ym, dia, desc, cat, valor))
        dia, valor = m['simples']
        n += 1
        venc = prox_mes(ym, '20')
        # o Simples do mês é lançado no último dia e pago no dia 20 do mês seguinte (o de outubro vence em 20/11/2026, ainda a pagar)
        paga = venc if venc <= '2026-11-10' else None
        rows.append(linha(n, 'saida', ym, dia, 'Simples Nacional - DAS', 'Impostos e Taxas', valor, None, paga, venc))
    return rows


def montar():
    ini = {'_comentario': 'T20 · fim do T19 + histórico de ago a out/2026 na Conta Principal (todo fictício). Gerado por rec/t20/semear.py: não edite à mão.'}
    rows = historico()
    liquido = round(sum((r['amount'] if r['transaction_type'] == 'entrada' else -r['amount']) for r in rows if r['is_paid']), 2)
    inicial = round(18500 - liquido, 2)
    ini['financial_transactions'] = rows
    # o saldo de hoje da Conta Principal continua o do fim do T13 (initial_balance 18.500,00 sem histórico): o histórico "já estava" lá
    ini['_patch'] = {'financial_accounts': [{'match': {'id': PRINCIPAL}, 'set': {'initial_balance': inicial, 'updated_at': t('2026-11-10')}}]}
    return ini, liquido, inicial


def resumo(rows, inicial):
    print('--- conferência do histórico (competência = data do lançamento; caixa = data da baixa)')
    saldo = inicial
    for ym in MESES:
        rec = sum(r['amount'] for r in rows if r['transaction_type'] == 'entrada' and r['transaction_date'].startswith(ym))
        rec_cx = sum(r['amount'] for r in rows if r['transaction_type'] == 'entrada' and r['is_paid'] and r['paid_date'].startswith(ym))
        desp = sum(r['amount'] for r in rows if r['transaction_type'] == 'saida' and r['transaction_date'].startswith(ym))
        desp_cx = sum(r['amount'] for r in rows if r['transaction_type'] == 'saida' and r['is_paid'] and r['paid_date'].startswith(ym))
        ent = sum(r['amount'] for r in rows if r['transaction_type'] == 'entrada' and r['is_paid'] and r['paid_date'].startswith(ym))
        print(f'{ym}: receita competência {rec:,.2f} (caixa {rec_cx:,.2f}) · despesa competência {desp:,.2f} (caixa {desp_cx:,.2f}) · saldo no início do mês {saldo:,.2f}')
        saldo += ent - desp_cx


def verificar(ini):
    ids = set()
    faltam = []
    for rel in CADEIA:
        arq = os.path.join(EXTRA, rel + '.json')
        if not os.path.exists(arq):
            faltam.append(rel)
            continue
        with open(arq, encoding='utf8') as f:
            ids |= set(re.findall(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', f.read()))
    ref = set(re.findall(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', json.dumps(ini)))
    print('ids literais fora da cadeia:', sorted(ref - ids - {EMP, CAMILA}) or 'nenhum')
    if faltam:
        print('SEMENTES DA CADEIA QUE AINDA NÃO EXISTEM:', faltam)


def main():
    ini, liquido, inicial = montar()
    os.makedirs(os.path.join(EXTRA, 't20'), exist_ok=True)
    with open(os.path.join(EXTRA, 't20', 'inicio.json'), 'w', encoding='utf8') as f:
        json.dump(ini, f, ensure_ascii=False, indent=1)
    cad = {'fake_now': FAKE_NOW, 'inicio': CADEIA + ['t20/inicio'], 't19_final': T19_FINAL,
           'nota': 'mundo do T20 = fim do T19 (cadeia do T19 + semente final) + t20/inicio; apos-capNN do T20 são cumulativos sobre t20/inicio (só o apos-cap03 muda o banco)'}
    with open(os.path.join(HERE, 'cadeia.json'), 'w', encoding='utf8') as f:
        json.dump(cad, f, ensure_ascii=False, indent=1)
    print(f't20/inicio.json e rec/t20/cadeia.json gerados (T19_FINAL = {T19_FINAL}).')
    print(f'  transações do histórico: {len(ini["financial_transactions"])} · líquido pago {liquido:,.2f} · saldo inicial novo da Conta Principal {ini["_patch"]["financial_accounts"][0]["set"]["initial_balance"]:,.2f}')
    resumo(ini['financial_transactions'], inicial)
    verificar(ini)


if __name__ == '__main__':
    main()
