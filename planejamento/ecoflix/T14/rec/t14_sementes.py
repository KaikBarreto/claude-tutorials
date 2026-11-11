#!/usr/bin/env python3
"""T14 · escreve o estado de partida de cada capítulo em rec/mundo/seeds-extra/t14/ (deltas aplicados em ordem pelo `seedExtra`):
inicio (o fim do T13 que o T14 usa) → apos-cap02 → apos-cap03 → apos-cap04 → apos-cap06 → apos-cap07 → ... → apos-cap12 → apos-cap14.
Cada arquivo traz só o que o capítulo fez na tela (linhas novas e `_patch`), com os saldos gravados das contas recalculados aqui (as
sementes entram cruas, sem os "triggers"). Os lançamentos do mundo base são achados por conta, dia e valor: rode de novo sempre que o
mundo base mudar (`python3 -I rec/t14/t14_sementes.py`). Os campos de cada linha são os que o app 1.59.154 grava (inventario.md) e o
que os handlers da conciliação (rec/mundo/lib/conciliacao.mjs) gravam; as linhas do extrato vêm do rec/t14/arquivos/linhas.json
(t14_ofx.py), com posted_at e dedup_key no formato do parser do app (parseOfx/computeDedupKey, conferidos na importação ao vivo).
Horários: os do MUNDO_LINHA_DO_TEMPO.md (T13 às 08:05–08:15 e o pneu em 09/11 11:00; o T14 às 08:10–08:25)."""
import glob
import json
import os
import sys
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
TUT = os.path.normpath(os.path.join(HERE, '..', '..'))
MUNDO = os.path.join(TUT, 'rec', 'mundo')
OUT = os.path.join(MUNDO, 'seeds-extra', 't14')
EMP, RAFA = '@id:company.reciclavale', '@id:user.rafael'
PRINC, SEC, POUP, COFRE = '@id:banco.principal', '@id:banco.secundaria', '@id:banco.poupanca', '@id:banco.cofre'
COOP = '@id:t14.conta.cooperativa'
IMP = '@id:t14.extrato'

B = {}
for f in sorted(glob.glob(os.path.join(MUNDO, 'seeds', '*.json'))):
    for k, v in json.load(open(f, encoding='utf8')).items():
        if isinstance(v, list) and not k.startswith('_'):
            B.setdefault(k, []).extend(v)

r2 = lambda v: round(float(v) + 0.0, 2)
BRT = timezone(timedelta(hours=-3))


def iso(dia_hora):
    """'2026-11-10 08:10' (Brasília) -> ISO UTC"""
    d = datetime.strptime(dia_hora, '%Y-%m-%d %H:%M:%S' if dia_hora.count(':') == 2 else '%Y-%m-%d %H:%M').replace(tzinfo=BRT)
    return d.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z')


def dia_brt(iso_utc):
    return (datetime.strptime(iso_utc[:19], '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone.utc).astimezone(BRT)).strftime('%Y-%m-%d')


def acha(tabela, **kw):
    for r in B.get(tabela, []):
        if all(r.get(k) == v for k, v in kw.items()):
            return r
    raise SystemExit(f'mundo base sem {tabela} {kw}')


# ---------------------------------------------------------------- saldos correntes (seed crua: o saldo gravado e o balance_after são nossos)
CONTAS = {c['id']: c for c in B['bank_accounts']}
saldo = {cid: r2(c.get('balance') or 0) for cid, c in CONTAS.items()}
ultimo = {}   # conta -> (created_at, balance_after) do último lançamento
for t in B['bank_transactions']:
    k = t['bank_account_id']
    if k not in ultimo or str(t.get('created_at')) > ultimo[k][0]:
        ultimo[k] = (str(t.get('created_at')), r2(t.get('balance_after') or 0))
soma_bt = {}
for t in B['bank_transactions']:
    soma_bt[t['bank_account_id']] = r2(soma_bt.get(t['bank_account_id'], 0) + float(t['amount']))
avisos = [f"{CONTAS[k]['name']}: saldo gravado {saldo[k]} ≠ soma dos lançamentos {soma_bt.get(k, 0)}" for k in saldo
          if CONTAS[k].get('kind') != 'cash' and abs(saldo[k] - soma_bt.get(k, 0)) > 0.005]

SINAL = {'withdrawal': -1, 'expense': -1, 'deposit': 1}


def bt(chave, conta, tipo, valor, desc, quando, **extra):
    """bank_transactions como o trigger deixaria: sinal canônico, transaction_date (dia BRT), balance_after corrido, saldo da conta"""
    v = r2(abs(valor) * SINAL[tipo]) if tipo in SINAL else r2(valor)
    ant = ultimo.get(conta, ('', 0.0))[1]
    linha = {'id': f'@id:t14.{chave}', 'company_id': EMP, 'bank_account_id': conta, 'type': tipo, 'amount': v, 'description': desc,
             'transaction_at': quando, 'transaction_date': dia_brt(quando), 'created_at': extra.pop('created_at', quando), 'created_by': RAFA,
             'source': 'manual', 'excluded_from_dre': False, 'balance_after': r2(ant + v), 'origin_company_id': None, **extra}
    ultimo[conta] = (linha['created_at'], linha['balance_after'])
    saldo[conta] = r2(saldo[conta] + v)
    return linha


def patch_saldos(*contas):
    return [{'match': {'id': c}, 'set': {'balance': saldo[c]}} for c in contas]


# ---------------------------------------------------------------- inicio: o fim do T13 que o T14 vê
CAT = {c['name']: c['id'] for c in B['financial_categories']}
CC = {c['name']: c['id'] for c in B['cost_centers']}
energia = acha('financial_bills', description='Energia elétrica de outubro')
quiririm = next(b for b in B['balances'] if b['entity_id'] == '@id:cliente.quiririm')
modelo_forn = dict(B['suppliers'][0])
moretti = {**{k: None for k in modelo_forn}, 'id': '@id:t14.fornecedor.moretti', 'company_id': EMP, 'name': 'Hidráulica Moretti Ltda',
           'razao_social': 'Hidráulica Moretti Ltda', 'cpf_cnpj': '41.739.625/0001-57', 'email': 'contato@hidraulicamoretti.example',
           'phone': '(12) 90000-3131', 'phone_unavailable': False, 'cidade': 'Taubaté', 'uf': 'SP', 'is_mei': False, 'is_industry': False,
           'indicador_ie': 9, 'code': str(len(B['suppliers']) + 1), 'created_by': RAFA, 'created_at': iso('2026-11-10 07:50'), 'updated_at': iso('2026-11-10 07:50')}
manut = CAT.get('Manutenção de máquinas')
prensa = {'id': '@id:t14.conta.prensa', 'company_id': EMP, 'direction': 'payable', 'description': 'Manutenção da prensa enfardadeira', 'amount': 3480,
          'currency': 'BRL', 'due_date': '2026-11-30', 'status': 'partial', 'paid_amount': 1740, 'partner_id': moretti['id'], 'partner_type': 'supplier',
          'category_id': manut, 'cost_center_id': CC.get('Pátio'), 'expected_bank_account_id': PRINC, 'is_projection': False, 'created_by': RAFA,
          'created_at': iso('2026-11-10 07:52'), 'updated_at': iso('2026-11-10 08:10'), 'paid_at': iso('2026-11-10 08:10')}
pneu = {'id': '@id:t14.conta.pneu', 'company_id': EMP, 'direction': 'payable', 'description': 'Conserto do pneu da empilhadeira', 'amount': 180,
        'currency': 'BRL', 'due_date': '2026-11-09', 'status': 'paid', 'paid_amount': 180, 'category_id': manut, 'cost_center_id': CC.get('Pátio'),
        'expected_bank_account_id': PRINC, 'is_projection': False, 'created_by': RAFA, 'created_at': iso('2026-11-10 07:55'),
        'updated_at': iso('2026-11-10 07:55'), 'paid_at': iso('2026-11-09 11:00')}
t13 = [
    bt('t13.pneu', PRINC, 'withdrawal', 180, 'Pagamento: Conserto do pneu da empilhadeira', iso('2026-11-09 11:00'), category_id=manut,
       cost_center_id=CC.get('Pátio'), payment_method='transfer', created_at=iso('2026-11-10 07:55')),
    bt('t13.energia', PRINC, 'withdrawal', 1874.30, 'Pagamento: Energia elétrica de outubro', iso('2026-11-10 08:05'), category_id=energia.get('category_id'),
       cost_center_id=energia.get('cost_center_id'), payment_method='transfer'),
    bt('t13.prensa', PRINC, 'withdrawal', 1740, 'Pagamento: Manutenção da prensa enfardadeira', iso('2026-11-10 08:10'), category_id=manut,
       cost_center_id=CC.get('Pátio'), payment_method='transfer', partner_id=moretti['id'], partner_type='supplier'),
    bt('t13.quiririm', PRINC, 'deposit', 2000, 'Recebimento de saldo', iso('2026-11-10 08:15'), partner_id='@id:cliente.quiririm',
       partner_type='customer', payment_method='transfer'),
]
inicio = {
    'suppliers': [moretti], 'financial_bills': [prensa, pneu], 'bank_transactions': t13,
    '_patch': {'financial_bills': [{'match': {'id': energia['id']}, 'set': {'status': 'paid', 'paid_amount': energia['amount'], 'paid_at': iso('2026-11-10 08:05'),
                                                                        'updated_at': iso('2026-11-10 08:05')}}],
               'balances': [{'match': {'id': quiririm['id']}, 'set': {'balance': r2(quiririm['balance'] - 2000), 'updated_at': iso('2026-11-10 08:15')}}],
               'bank_accounts': patch_saldos(PRINC)},
}
NUM = {'inicio': {k: saldo[k] for k in (PRINC, SEC, COFRE)}}

# ---------------------------------------------------------------- cap02: Conta Cooperativa (R$ 5.000,00) e a Poupança antiga arquivada
CRIA = iso('2026-11-10 08:31')
CONTAS[COOP] = {'id': COOP, 'kind': 'bank'}
saldo[COOP] = 0.0
coop = {'id': COOP, 'company_id': EMP, 'name': 'Conta Cooperativa', 'kind': 'bank', 'is_default': False, 'is_protected': False, 'is_archived': False,
        'institution_name': None, 'institution_code': None, 'institution_ispb': None, 'color': '#14B8A6', 'currency': 'BRL', 'balance': 0,
        'created_at': CRIA, 'updated_at': CRIA}
aj = bt('bt.saldo_inicial', COOP, 'deposit', 5000, 'Ajuste de saldo - Saldo inicial', iso('2026-11-10 08:31:20'), excluded_from_dre=True)
coop['balance'] = saldo[COOP]
cap02 = {'bank_accounts': [coop], 'bank_transactions': [aj],
         '_patch': {'bank_accounts': [{'match': {'id': POUP}, 'set': {'is_archived': True, 'updated_at': iso('2026-11-10 08:32')}}]}}

# ---------------------------------------------------------------- cap03: ajuste do cofre (+R$ 60,00, "Contagem do cofre")
cap03 = {'cash_transactions': [{'id': '@id:t14.ct.ajuste_cofre', 'company_id': EMP, 'type': 'adjustment', 'amount': 60, 'description': 'Ajuste de saldo — Contagem do cofre',
                                'created_by': RAFA, 'excluded_from_dre': True, 'cash_register_id': None, 'transaction_at': iso('2026-11-10 08:33'),
                                'transaction_date': '2026-11-10', 'created_at': iso('2026-11-10 08:33')}]}
saldo[COFRE] = r2(saldo[COFRE] + 60)
cap03['_patch'] = {'bank_accounts': patch_saldos(COFRE)}

# ---------------------------------------------------------------- cap04: combustível, transferência e saque com tarifa (horários da linha do tempo)
GT, GS = '@id:t14.grupo.transferencia', '@id:t14.grupo.saque'
TDESC = 'Transferência: Conta Secundária → Conta Principal'
cap04_bt = [
    bt('bt.combustivel', PRINC, 'withdrawal', 350, 'Combustível da picape', iso('2026-11-10 08:10'), category_id=CAT.get('Combustível'),
       cost_center_id=CC.get('Frota'), payment_method='transfer'),
    bt('bt.transf_saida', SEC, 'withdrawal', 8000, TDESC, iso('2026-11-10 08:20'), group_id=GT, excluded_from_dre=True),
    bt('bt.transf_entrada', PRINC, 'deposit', 8000, TDESC, iso('2026-11-10 08:20'), group_id=GT, excluded_from_dre=True),
    bt('bt.saque_banco', PRINC, 'withdrawal', 2000, '↑ SAQUE · Conta Principal → Cofre (DINHEIRO)', iso('2026-11-10 08:25'), group_id=GS,
       source='cash_to_bank', excluded_from_dre=True),
    bt('bt.saque_cofre', COFRE, 'deposit', 2000, '↓ SAQUE · Conta Principal → Cofre', iso('2026-11-10 08:25'), group_id=GS, source='bank_to_cash',
       excluded_from_dre=True),
    bt('bt.tarifa_saque', PRINC, 'expense', 6.50, 'Tarifa de Saque para o Cofre', iso('2026-11-10 08:25:10'), group_id=GS),
]
cap04 = {'bank_transactions': cap04_bt, '_patch': {'bank_accounts': patch_saldos(PRINC, SEC, COFRE)}}
NUM['apos-cap04'] = {k: saldo[k] for k in (PRINC, SEC, COFRE, COOP)}

# ---------------------------------------------------------------- cap06: o extrato importado (17 linhas pendentes)
LINHAS = json.load(open(os.path.join(HERE, 'arquivos', 'linhas.json'), encoding='utf8'))
FMT = json.load(open(os.path.join(HERE, 'arquivos', 'formato_parser.json'), encoding='utf8')) if os.path.exists(os.path.join(HERE, 'arquivos', 'formato_parser.json')) else {}
IMPORTADO = iso('2026-11-10 08:36')
ledger, soma = 44933.47, r2(sum(l['valor'] for l in LINHAS))


def posted(l):
    return FMT.get(l['fitid'], {}).get('posted_at') or iso(f"{l['dt'][:4]}-{l['dt'][4:6]}-{l['dt'][6:8]} {l['dt'][8:10]}:{l['dt'][10:12]}:{l['dt'][12:14]}")


ENT = {l['n']: f'@id:t14.linha.{l["n"]:02d}' for l in LINHAS}
entradas = [{'id': ENT[l['n']], 'company_id': EMP, 'bank_account_id': PRINC, 'import_id': IMP, 'dedup_key': FMT.get(l['fitid'], {}).get('dedup_key') or f"fitid:{l['fitid']}",
             'original_dedup_key': FMT.get(l['fitid'], {}).get('dedup_key') or f"fitid:{l['fitid']}", 'fitid': l['fitid'], 'posted_at': posted(l), 'amount': l['valor'],
             'trn_type': l['trn'], 'memo': l['memo'], 'name': None, 'status': 'pending', 'created_at': IMPORTADO} for l in LINHAS]
cap06 = {'bank_statement_imports': [{'id': IMP, 'company_id': EMP, 'bank_account_id': PRINC, 'file_name': 'Extrato_20261101_20261110.ofx',
                                     'file_hash': FMT.get('_file_hash'), 'bank_id': '0999', 'acct_id': '40218-7', 'period_start': '2026-11-01',
                                     'period_end': '2026-11-10', 'ledger_balance': ledger, 'ledger_balance_date': '2026-11-10',
                                     'opening_balance': r2(ledger - soma), 'entry_count': len(LINHAS), 'status': 'open', 'created_by': RAFA, 'created_at': IMPORTADO}],
         'bank_statement_entries': entradas}

# lançamentos que cada linha casa (mundo base achado por conta, dia BRT e valor; os do T13 e do T14 pelas chaves daqui)
def do_base(dia, valor, conta=PRINC, ordem=None):
    ach = [t for t in B['bank_transactions'] if t['bank_account_id'] == conta and dia_brt(t['transaction_at']) == dia and abs(float(t['amount']) - valor) < 0.005]
    if ordem:
        ach = [t for t in ach if t.get('order_id') and ordem(t['order_id'])]
    if len(ach) != 1:
        raise SystemExit(f'mundo base: {len(ach)} lançamento(s) de {valor} em {dia} na {CONTAS[conta]["name"]} (esperado 1): ' + json.dumps(ach, ensure_ascii=False)[:600])
    return ach[0]['id']


def forn_da_compra(nome):
    sid = next((s['id'] for s in B['suppliers'] if s['name'] == nome), None)
    return lambda oid: any(p['id'] == oid and p.get('supplier_id') == sid for p in B.get('purchases', []))


TX = {1: lambda: do_base('2026-11-03', -2250), 2: lambda: do_base('2026-11-05', -6800), 7: lambda: '@id:t14.t13.pneu', 11: lambda: '@id:t14.t13.energia',
      12: lambda: '@id:t14.t13.prensa', 13: lambda: '@id:t14.t13.quiririm', 14: lambda: '@id:t14.bt.combustivel', 15: lambda: '@id:t14.bt.transf_entrada',
      16: lambda: '@id:t14.bt.saque_banco', 17: lambda: '@id:t14.bt.tarifa_saque',
      3: lambda: do_base('2026-11-06', -380, ordem=forn_da_compra('Aparecida Ramos')), 4: lambda: do_base('2026-11-06', -380, ordem=forn_da_compra('Auto Peças Vale Forte')),
      6: lambda: do_base('2026-11-03', 4815.20)}
VAL = {l['n']: l['valor'] for l in LINHAS}


def casa(n, quando, conf='manual', tipo='existing', tx=None, dif=0.0, bill=None):
    return {'id': f'@id:t14.casamento.{n:02d}', 'company_id': EMP, 'entry_id': ENT[n], 'bank_transaction_id': tx or TX[n](), 'match_type': tipo, 'bill_id': bill,
            'confidence': conf, 'value_difference': r2(dif), 'group_id': None, 'created_by': RAFA, 'created_at': quando}


def status(ns, st):
    return [{'match': {'id': ENT[n]}, 'set': {'status': st}} for n in ns]


def depois_do_import():
    global cap07, cap08, cap09, cap10, cap11, cap12, cap14
    t = iso('2026-11-10 08:38')
    cap07 = {'reconciliation_matches': [casa(n, t) for n in (1, 2, 7, 11, 12, 14, 13, 16, 17, 15)],
             '_patch': {'bank_statement_entries': status((1, 2, 7, 11, 12, 14, 13, 16, 17, 15), 'matched')}}

    # cap08: água e esgoto baixada pela linha 5 (pay_financial_bill na data da linha: 09/11 12:00)
    agua = acha('financial_bills', description='Água e esgoto de outubro')
    tx_agua = bt('bt.agua', PRINC, 'withdrawal', 238.40, 'Pagamento: Água e esgoto de outubro', iso('2026-11-09 12:00'), category_id=agua.get('category_id'),
                 cost_center_id=agua.get('cost_center_id'), group_id='@id:t14.grupo.agua', payment_method='transfer', created_at=iso('2026-11-10 08:40'))
    cap08 = {'bank_transactions': [tx_agua],
             'bill_payments': [{'id': '@id:t14.pagamento.agua', 'company_id': EMP, 'bill_id': agua['id'], 'amount': 238.40, 'paid_date': '2026-11-09', 'payment_method': 'transfer',
                                'bank_account_id': PRINC, 'bank_transaction_id': tx_agua['id'], 'group_id': '@id:t14.grupo.agua', 'created_by': RAFA, 'currency': 'BRL',
                                'fee_amount': 0, 'interest_amount': 0, 'created_at': iso('2026-11-10 08:40')}],
             'reconciliation_matches': [casa(5, iso('2026-11-10 08:40'), 'manual', 'bill_settlement', tx=tx_agua['id'], bill=agua['id'])],
             '_patch': {'bank_statement_entries': status((5,), 'matched'), 'bank_accounts': patch_saldos(PRINC),
                        'financial_bills': [{'match': {'id': agua['id']}, 'set': {'status': 'paid', 'paid_amount': 238.40, 'paid_at': iso('2026-11-09 12:00'),
                                                                                  'updated_at': iso('2026-11-10 08:40')}}]}}

    # cap09: a tarifa do pacote criada pela linha 8 (categoria "Tarifas", na data da linha)
    l8 = next(e for e in entradas if e['id'] == ENT[8])
    tx_tarifa = bt('bt.tarifa_pacote', PRINC, 'expense', 64.90, 'TARIFA PACOTE SERVICOS', l8['posted_at'], category_id=CAT['Tarifas'], created_at=iso('2026-11-10 08:42'))
    cap09 = {'bank_transactions': [tx_tarifa], 'reconciliation_matches': [casa(8, iso('2026-11-10 08:42'), 'manual', 'created', tx=tx_tarifa['id'])],
             '_patch': {'bank_statement_entries': status((8,), 'matched'), 'bank_accounts': patch_saldos(PRINC)}}

    # cap10: Pix da Serra Fina (4.815,00) casado com a venda de 03/11 (4.815,20): diferença −0,20 no resumo
    cap10 = {'reconciliation_matches': [casa(6, iso('2026-11-10 08:44'), 'manual', dif=VAL[6] - 4815.20)],
             '_patch': {'bank_statement_entries': status((6,), 'matched')}}
    # cap11: tarifa avulsa e estorno ignorados
    cap11 = {'_patch': {'bank_statement_entries': status((9, 10), 'ignored')}}
    # cap12: os dois Pix de 380,00 (Aparecida e Auto Peças Vale Forte)
    cap12 = {'reconciliation_matches': [casa(3, iso('2026-11-10 08:47'), 'manual'), casa(4, iso('2026-11-10 08:47:30'))],
             '_patch': {'bank_statement_entries': status((3, 4), 'matched')}}
    # cap14: finalizada
    cap14 = {'_patch': {'bank_statement_imports': [{'match': {'id': IMP}, 'set': {'status': 'finalized'}}]}}
    NUM['apos-cap12'] = {k: saldo[k] for k in (PRINC, SEC, COFRE, COOP)}


ESTADOS = [('inicio', 'inicio'), ('apos-cap02', 'cap02'), ('apos-cap03', 'cap03'), ('apos-cap04', 'cap04'), ('apos-cap06', 'cap06')]
try:
    depois_do_import()
    ESTADOS += [('apos-cap07', 'cap07'), ('apos-cap08', 'cap08'), ('apos-cap09', 'cap09'), ('apos-cap10', 'cap10'), ('apos-cap11', 'cap11'), ('apos-cap12', 'cap12'), ('apos-cap14', 'cap14')]
except SystemExit as e:
    print('AVISO: estados depois do import NÃO escritos (mundo base antigo?):', str(e)[:300])

os.makedirs(OUT, exist_ok=True)
for nome, var in ESTADOS:
    d = globals()[var]
    json.dump(d, open(os.path.join(OUT, f'{nome}.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
nm = {PRINC: 'Principal', SEC: 'Secundária', COFRE: 'cofre(gravado)', COOP: 'Cooperativa'}
for k, v in NUM.items():
    print(f'{k:11}', '  '.join(f'{nm[c]} {s:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.') for c, s in v.items()))
print('abertura do extrato', r2(ledger - soma), '| formato do parser:', 'conferido' if FMT else 'AINDA NÃO (posted_at/dedup_key estimados)')
for a in avisos:
    print('AVISO mundo base:', a)
