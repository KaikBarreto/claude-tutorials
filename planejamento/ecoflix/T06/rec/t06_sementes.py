#!/usr/bin/env python3
"""T06 · sementes do estado de partida dos capítulos (rec/mundo/seeds-extra/t06/*.json), sobre o mundo base (rec/mundo/seeds/).

Determinístico: os valores que dependem do mundo base (número dos pedidos, estoque, saldos das contas, saldo do cofre) são lidos de
rec/mundo/seeds/*.json na hora; os horários são os da linha do tempo (MUNDO_LINHA_DO_TEMPO.md, seções 1 e 9). As colunas das linhas que o
app grava (caixa, abertura, saque, tarifa, fechamento) são as que o app 1.59.154 mandou ao Supabase falso nas explorações/ensaios
(`capturar`). Rode de novo sempre que o mundo base mudar:  python3 -I rec/t06/t06_sementes.py [todas|apos-cap02 ...]
  python3 -I rec/t06/t06_sementes.py capturar     # mostra as linhas de hoje (10/11) da instância 54306 (depois de um ensaio)

Sementes (cada uma soma só o que o capítulo fez; o roteiro empilha: SEMENTE em gerar.py):
  apos-cap02  #85 do Rafael aberto às 08:31 com R$ 1.500,00 (+ a linha "Abertura do Caixa #85")
  apos-cap05  #86 do Marcos aberto pelo Rafael às 08:42 com R$ 17.000,00 ("Usar disponível")
  apos-cap09  saque de R$ 3.000,00 da Conta Principal para o #86 com tarifa de R$ 6,50 (08:46) e a saída "Tarifa mensal do pacote de
              serviços" de R$ 39,90 da Conta Secundária, categoria "Tarifas", no #85 (08:47)
  dia-10      no #85: venda à Aços Quiririm (1.600 kg de ferro pesado a R$ 1,25 = R$ 2.000,00, Pix na Conta Principal, 10:15); compra da
              Aparecida Ramos (42 kg de alumínio latinha a R$ 6,20 = R$ 260,40, dinheiro, 11:20); compra do Valdir Pereira (310 kg de ferro
              misto a R$ 0,75 = R$ 232,50, dinheiro, 15:05). Esperado no fechamento: 1.500,00 - 492,90 = R$ 1.007,10
  apos-cap10  #85 fechado às 17:41 com R$ 1.007,10 (sem diferença)
  apos-cap11  #85 reaberto às 17:42
"""
import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
TUT_HOME = os.path.normpath(os.path.join(HERE, '..', '..'))
MUNDO = os.path.join(TUT_HOME, 'rec', 'mundo')
SAIDA = os.path.join(MUNDO, 'seeds-extra', 't06')
FAKE = os.environ.get('FAKE_URL', 'http://127.0.0.1:54306')
EMP = '@id:company.reciclavale'
RAFAEL, MARCOS = '@id:user.rafael', '@id:user.marcos'
PRINCIPAL, SECUNDARIA, COFRE = '@id:banco.principal', '@id:banco.secundaria', '@id:banco.cofre'
C85, C86 = '@id:caixa.85', '@id:caixa.86'      # como os do histórico (@id:caixa.83, @id:caixa.84)


def utc(hhmm, dia='2026-11-10'):
    """hora de Brasília (UTC-3) -> ISO UTC"""
    h, m = map(int, hhmm.split(':'))
    return f'{dia}T{h + 3:02d}:{m:02d}:00.000Z'


def base():
    out = {}
    for f in sorted(os.listdir(os.path.join(MUNDO, 'seeds'))):
        if f.endswith('.json'):
            for t, rows in json.load(open(os.path.join(MUNDO, 'seeds', f), encoding='utf8')).items():
                if isinstance(rows, list):
                    out.setdefault(t, []).extend(rows)
    return out


B = base()
r2 = lambda x: round(x + 1e-9, 2)


def conta(cid):
    return next(b for b in B['bank_accounts'] if b['id'] == cid)


def material(mid):
    return next(m for m in B['materials'] if m['id'] == mid)


def categoria(nome):
    return next(c['id'] for c in B['financial_categories'] if c['name'] == nome)


def numero_caixa():
    return max(r['register_number'] for r in B['cash_register']) + 1


def proximo_pedido():
    return max(int(p['order_number']) for p in B['purchases'] + B['sales'] if p.get('order_number') is not None) + 1


def ultimo_saldo(cid):
    bt = sorted((b for b in B['bank_transactions'] if b['bank_account_id'] == cid), key=lambda b: b['created_at'])
    return bt[-1]['balance_after'] if bt else conta(cid)['balance']


def ct(id_, caixa, tipo, valor, desc, quando, quem=RAFAEL, **kw):
    return {'id': id_, 'company_id': EMP, 'cash_register_id': caixa, 'type': tipo, 'amount': valor, 'description': desc,
            'transaction_at': quando, 'transaction_date': '2026-11-10', 'created_at': quando, 'created_by': quem,
            'excluded_from_dre': False, **kw}


def bt(id_, contaid, tipo, valor, desc, quando, saldo_depois, **kw):
    return {'id': id_, 'company_id': EMP, 'bank_account_id': contaid, 'type': tipo, 'amount': valor, 'description': desc,
            'transaction_at': quando, 'transaction_date': '2026-11-10', 'created_at': quando, 'created_by': RAFAEL,
            'source': 'manual', 'excluded_from_dre': False, 'balance_after': saldo_depois, 'origin_company_id': EMP, **kw}


# ---------------------------------------------------------------- as sementes
N85 = numero_caixa()            # 85 no mundo base
N86 = N85 + 1
ABRE85, ABRE86, SAQUE, TARIFA_MES, FECHA85, REABRE85 = utc('08:31'), utc('08:42'), utc('08:46'), utc('08:47'), utc('17:41'), utc('17:42')
SAQ, TAR_SAQUE, TAR_MES = 3000.0, 6.5, 39.9


def apos_cap02():
    return {
        '_doc': f'T06 · depois do cap02: caixa #{N85} do Rafael aberto às 08:31 com R$ 1.500,00 (rec/t06/t06_sementes.py).',
        'cash_register': [{'id': C85, 'company_id': EMP, 'register_number': N85, 'status': 'open', 'opened_at': ABRE85, 'opened_by': RAFAEL,
                           'initial_opening_balance': 1500, 'opening_balance': 1500, 'closing_balance': None, 'closed_at': None,
                           'currency': 'BRL', 'created_at': ABRE85}],
        'cash_transactions': [ct('@id:ct.t06.abre85', C85, 'opening', 1500, f'Abertura do Caixa #{N85}', ABRE85)],
    }


def apos_cap05():
    return {
        '_doc': f'T06 · depois do cap05: caixa #{N86} do Marcos aberto pelo Rafael às 08:42 com R$ 17.000,00 ("Usar disponível").',
        'cash_register': [{'id': C86, 'company_id': EMP, 'register_number': N86, 'status': 'open', 'opened_at': ABRE86, 'opened_by': MARCOS,
                           'initial_opening_balance': 17000, 'opening_balance': 17000, 'closing_balance': None, 'closed_at': None,
                           'currency': 'BRL', 'created_at': ABRE86}],
        'cash_transactions': [ct('@id:ct.t06.abre86', C86, 'opening', 17000, f'Abertura do Caixa #{N86}', ABRE86)],
    }


def efeitos_cap09():
    """saldos das contas depois do cap09 (o dia-10 parte deles)"""
    p = r2(conta(PRINCIPAL)['balance'] - SAQ - TAR_SAQUE)
    s = r2(conta(SECUNDARIA)['balance'] - TAR_MES)
    c = r2(conta(COFRE)['balance'] + SAQ)
    return p, s, c


def apos_cap09():
    p0, s0 = ultimo_saldo(PRINCIPAL), ultimo_saldo(SECUNDARIA)
    c0 = sum(b['amount'] for b in B['bank_transactions'] if b['bank_account_id'] == COFRE)
    p, s, c = efeitos_cap09()
    grupo = '@id:grupo.t06.saque'
    nome = conta(PRINCIPAL)['name']
    return {
        '_doc': (f'T06 · depois do cap09: saque de R$ 3.000,00 da {nome} para o caixa #{N86} com tarifa de R$ 6,50 (08:46) e a saída '
                 f'"Tarifa mensal do pacote de serviços" de R$ 39,90 da Conta Secundária, categoria "Tarifas", no caixa #{N85} (08:47).'),
        'bank_transactions': [
            bt('@id:bt.t06.saque', PRINCIPAL, 'transfer', -SAQ, f'↑ SAQUE · {nome} → Caixa #{N86}', SAQUE, r2(p0 - SAQ),
               group_id=grupo, cash_register_id=C86),
            bt('@id:bt.t06.tarifa_saque', PRINCIPAL, 'expense', -TAR_SAQUE, f'Tarifa de Saque para o Caixa #{N86}', SAQUE, r2(p0 - SAQ - TAR_SAQUE),
               group_id=grupo, cash_register_id=C86),
            bt('@id:bt.t06.espelho_cofre', COFRE, 'transfer', SAQ, f'↑ Crédito do Cofre · Saque {nome} → Caixa #{N86}', SAQUE, r2(c0 + SAQ),
               group_id=grupo, cash_register_id=C86),
            bt('@id:bt.t06.tarifa_mes', SECUNDARIA, 'expense', -TAR_MES, 'Tarifa mensal do pacote de serviços', TARIFA_MES, r2(s0 - TAR_MES),
               category_id=categoria('Tarifas'), cash_register_id=C85),
        ],
        'cash_transactions': [ct('@id:ct.t06.saque86', C86, 'transfer', SAQ, f'↓ SAQUE · {nome} → Caixa #{N86}', SAQUE, group_id=grupo)],
        '_patch': {
            'bank_accounts': [{'match': {'id': PRINCIPAL}, 'set': {'balance': p}}, {'match': {'id': SECUNDARIA}, 'set': {'balance': s}},
                              {'match': {'id': COFRE}, 'set': {'balance': c}}],
            'cash_register': [{'match': {'id': C86}, 'set': {'opening_balance': r2(17000 + SAQ)}}],
        },
    }


VENDA = ('@id:cliente.quiririm', '@id:material.ferro_pesado', 1600, 1.25, utc('10:15'))
COMPRAS = [('@id:fornecedor.cida', '@id:material.al_latinha', 42, 6.20, utc('11:20')),
           ('@id:fornecedor.valdir', '@id:material.ferro_misto', 310, 0.75, utc('15:05'))]


def pedido(tipo, num, parceiro, quando, total, metodo):
    d = {'id': f'@id:{"venda" if tipo == "sale" else "compra"}.{num}', 'company_id': EMP, 'order_number': num, 'order_seq': num,
         'order_period': None, 'order_ref': f'#{num}', 'status': 'completed', 'total_amount': total, 'paid_amount': total,
         'payment_method': metodo, 'created_by': RAFAEL, 'transaction_at': quando, 'transaction_date': '2026-11-10', 'created_at': quando,
         'currency': 'BRL', 'hide_financial_details': False, 'notes': None, 'driver_name': None, 'vehicle_plate': None, 'driver_id': None,
         'vehicle_id': None}
    d['customer_id' if tipo == 'sale' else 'supplier_id'] = parceiro
    return d


def item(tipo, num, mid, qtd, preco):
    return {'id': f'@id:{"si" if tipo == "sale" else "pi"}.{num}.0', ('sale_id' if tipo == 'sale' else 'purchase_id'): f'@id:{"venda" if tipo == "sale" else "compra"}.{num}',
            'material_id': mid, 'material_name': material(mid)['name'], 'quantity': qtd, 'unit_price': preco, 'total_price': r2(qtd * preco),
            'impurity': 0, 'impurity_kg': None, 'impurity_pct': None, 'item_discount': 0, 'tare_weight': None, 'first_weight': None,
            'second_weight': None, 'weighing_mode': None, 'weight_source': 'manual'}


def dia_10():
    p, s, c = efeitos_cap09()
    n = proximo_pedido()
    out = {'_doc': (f'T06 · o dia 10/11 no caixa #{N85} (entre o cap09 e o cap10): venda #{n} à Aços Quiririm, compras #{n + 1} (Aparecida) e '
                    f'#{n + 2} (Valdir); esperado no fechamento R$ 1.007,10.'),
           'sales': [], 'sale_items': [], 'purchases': [], 'purchase_items': [], 'stock_movements': [], 'cash_transactions': [],
           'bank_transactions': [], '_patch': {'materials': [], 'bank_accounts': [], 'cash_register': []}}
    estoque = {}
    # venda (Pix na Conta Principal; a gaveta não muda: linha de valor 0 no caixa, como o app grava)
    cli, mid, qtd, preco, quando = VENDA
    total = r2(qtd * preco)
    out['sales'].append(pedido('sale', n, cli, quando, total, 'transfer'))
    out['sale_items'].append(item('sale', n, mid, qtd, preco))
    antes = estoque.get(mid, material(mid)['current_stock'])
    estoque[mid] = r2(antes - qtd)
    out['stock_movements'].append({'id': f'@id:sm.t06.{n}', 'company_id': EMP, 'material_id': mid, 'type': 'VENDA', 'quantity': -qtd,
                                   'stock_before': antes, 'stock_after': estoque[mid], 'order_id': f'@id:venda.{n}', 'order_type': 'sale',
                                   'description': f'Venda #{n}', 'created_by': RAFAEL, 'transaction_at': quando,
                                   'transaction_date': '2026-11-10', 'created_at': quando})
    out['cash_transactions'].append(ct(f'@id:ct.t06.v{n}', C85, 'sale', 0, f'Venda #{n} (PIX/Transferência)', quando, order_id=f'@id:venda.{n}'))
    principal = r2(p + total)
    out['bank_transactions'].append(bt(f'@id:bt.t06.v{n}', PRINCIPAL, 'deposit', total, f'Venda #{n}', quando, principal,
                                       order_id=f'@id:venda.{n}', payment_method='transfer'))
    # compras em dinheiro (saem da gaveta do #85)
    gaveta = 0.0
    for k, (forn, mid, qtd, preco, quando) in enumerate(COMPRAS, 1):
        num = n + k
        total = r2(qtd * preco)
        out['purchases'].append(pedido('purchase', num, forn, quando, total, 'cash'))
        out['purchase_items'].append(item('purchase', num, mid, qtd, preco))
        antes = estoque.get(mid, material(mid)['current_stock'])
        estoque[mid] = r2(antes + qtd)
        out['stock_movements'].append({'id': f'@id:sm.t06.{num}', 'company_id': EMP, 'material_id': mid, 'type': 'COMPRA', 'quantity': qtd,
                                       'stock_before': antes, 'stock_after': estoque[mid], 'order_id': f'@id:compra.{num}',
                                       'order_type': 'purchase', 'description': f'Compra #{num}', 'created_by': RAFAEL, 'transaction_at': quando,
                                       'transaction_date': '2026-11-10', 'created_at': quando})
        out['cash_transactions'].append(ct(f'@id:ct.t06.c{num}', C85, 'purchase', total, f'Compra #{num}', quando, order_id=f'@id:compra.{num}'))
        gaveta += total
    for mid, q in estoque.items():
        out['_patch']['materials'].append({'match': {'id': mid}, 'set': {'current_stock': q}})
    out['_patch']['bank_accounts'] += [{'match': {'id': PRINCIPAL}, 'set': {'balance': principal}},
                                       {'match': {'id': COFRE}, 'set': {'balance': r2(c - gaveta)}}]
    out['_patch']['cash_register'].append({'match': {'id': C85}, 'set': {'opening_balance': r2(1500 - gaveta)}})
    assert r2(1500 - gaveta) == 1007.10, gaveta
    return out


def apos_cap10():
    return {
        '_doc': f'T06 · depois do cap10: caixa #{N85} fechado às 17:41 com R$ 1.007,10, sem diferença (o dinheiro contado volta ao cofre).',
        'cash_transactions': [ct('@id:ct.t06.fecha85', C85, 'closing', 1007.1, 'Fechamento de caixa', FECHA85)],
        '_patch': {'cash_register': [{'match': {'id': C85}, 'set': {'status': 'closed', 'closing_balance': 1007.1, 'closed_at': FECHA85}}]},
    }


def apos_cap11():
    return {
        '_doc': f'T06 · depois do cap11: caixa #{N85} reaberto às 17:42 (volta como estava antes do fechamento).',
        '_remove': {'cash_transactions': [{'id': '@id:ct.t06.fecha85'}]},
        '_patch': {'cash_register': [{'match': {'id': C85}, 'set': {'status': 'open', 'closing_balance': None, 'closed_at': None,
                                                                     'reopened_at': REABRE85}}]},
    }


SEMENTES = {'apos-cap02': apos_cap02, 'apos-cap05': apos_cap05, 'apos-cap09': apos_cap09, 'dia-10': dia_10, 'apos-cap10': apos_cap10,
            'apos-cap11': apos_cap11}


def capturar():
    """linhas de 10/11 (a partir das 08:30) da instância: o que o app gravou no ensaio"""
    for t in ('cash_register', 'cash_transactions', 'bank_transactions', 'bank_accounts'):
        rows = json.load(urllib.request.urlopen(f'{FAKE}/__dev/state?table={t}'))
        novos = [r for r in rows if str(r.get('created_at') or '') >= '2026-11-10T11:30' or str(r.get('updated_at') or '') >= '2026-11-10T11:30'
                 or str(r.get('closed_at') or '') >= '2026-11-10T11:30']
        print(f'== {t}: {len(novos)}')
        for r in novos:
            print('  ', json.dumps(r, ensure_ascii=False)[:900])


if __name__ == '__main__':
    args = sys.argv[1:] or ['todas']
    if args[0] == 'capturar':
        capturar()
        sys.exit(0)
    quais = list(SEMENTES) if args == ['todas'] else args
    os.makedirs(SAIDA, exist_ok=True)
    for q in quais:
        d = SEMENTES[q]()
        json.dump(d, open(os.path.join(SAIDA, f'{q}.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
        print(f'{q}: ' + ', '.join(f'{k} {len(v)}' for k, v in d.items() if isinstance(v, list)))
