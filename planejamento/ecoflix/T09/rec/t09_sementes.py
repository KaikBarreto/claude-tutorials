#!/usr/bin/env python3
"""T09 · Pedidos e histórico do caixa: gera as sementes extras da aula em rec/mundo/seeds-extra/t09/ (determinístico; rodar de
novo refaz igual). FAKE_NOW da aula: 2026-11-11T08:30:00-03:00 (quarta).

Cadeia (cada capítulo abre um navegador novo e parte da lista acumulada; ver SEMENTE no gerar.py):
  inicio      o dia 10/11 que a T6 e a T8 contam, já fechado (o #85 do Rafael: abertura de R$ 1.500,00, a compra do ticket #58 da
              Cooperativa por Pix, a venda de 1.600 kg de ferro pesado à Aços Quiririm por Pix e as compras da Aparecida e do Valdir
              em dinheiro, fecha com R$ 1.007,10; o #86 do Marcos: R$ 17.000,00 + o saque de R$ 3.000,00, fecha com R$ 20.000,00)
              e a manhã de 11/11: o #87 do Rafael aberto às 07:10 com R$ 1.200,00 e três compras em dinheiro (07:22 Aparecida,
              24 kg de latinha, R$ 148,80; 07:41 e 07:42 Valdir, 280 kg de ferro misto, R$ 210,00 cada: a 2ª é a duplicada).
              O Marcos sem caixa aberto em 11/11.
  apos-cap04  a latinha da Aparecida corrigida: 42 kg, R$ 260,40 (mesmo número e mesma hora, no #87; estoque +18 kg)
  apos-cap05  a compra duplicada do Valdir (07:42) excluída (estoque -280 kg) e a linha do Histórico de Exclusões
  apos-cap06  "Cupom sem valor" ligado na compra do Valdir (07:41)

O mundo base (seção 16 da MUNDO_LINHA_DO_TEMPO) traz o #70 de 21/10 só com as duas compras da T9, o #83/#84 de 09/11 e a cópia
de 03/11 da Aparecida, estornada em 05/11. Enquanto o mundo base antigo não tiver o estorno de 03/11, esta semente o põe por conta
própria (PROVISÓRIO, avisado na saída); quando o mundo base novo chegar, rode de novo e ele sai daqui.
Números do mundo base (último pedido, último caixa, estoque, saldo da Conta Principal) são lidos das sementes, nada fixo.
Uso: python3 -I rec/t09/t09_sementes.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
MUNDO = os.path.normpath(os.path.join(HERE, '..', 'mundo'))
SAIDA = os.path.join(MUNDO, 'seeds-extra', 't09')

CID = '@id:company.reciclavale'
RAFAEL, MARCOS = '@id:user.rafael', '@id:user.marcos'
LATINHA, F_PESADO, F_MISTO, PAPELAO = '@id:material.al_latinha', '@id:material.ferro_pesado', '@id:material.ferro_misto', '@id:material.papelao'
CIDA, VALDIR, RECOMECO = '@id:fornecedor.cida', '@id:fornecedor.valdir', '@id:fornecedor.recomeco'
QUIRIRIM = '@id:cliente.quiririm'
PRINCIPAL = '@id:banco.principal'
CX = {n: f'@id:t09.caixa.{n}' for n in (85, 86, 87)}


def base():
    tabs = {}
    for f in sorted(os.listdir(os.path.join(MUNDO, 'seeds'))):
        if f.endswith('.json'):
            for k, v in json.load(open(os.path.join(MUNDO, 'seeds', f), encoding='utf8')).items():
                if isinstance(v, list):
                    tabs.setdefault(k, []).extend(v)
    return tabs


B = base()
ULT_PEDIDO = max(int(p['order_number']) for t in ('purchases', 'sales') for p in B.get(t, []))
ULT_CAIXA = max(int(c['register_number']) for c in B['cash_register'])
assert ULT_CAIXA == 84, f'o mundo base termina no caixa #{ULT_CAIXA}, a aula espera #84'
ESTOQUE = {m['id']: float(m.get('current_stock') or 0) for m in B['materials']}
NOME_MAT = {m['id']: m['name'] for m in B['materials']}
CONTA = {b['id']: b for b in B['bank_accounts']}


def z(dia, hora):
    """'2026-11-10', '08:31' (Brasília) -> ISO em UTC"""
    h, m = map(int, hora.split(':'))
    h += 3
    d = int(dia[-2:])
    if h >= 24:
        h -= 24
        d += 1
    return f'{dia[:-2]}{d:02d}T{h:02d}:{m:02d}:00.000Z'


def r2(x):
    return round(x + 1e-9, 2)


class Estado:
    def __init__(s):
        s.t = {}
        s.estoque = dict(ESTOQUE)
        s.banco = {k: float(v.get('balance') or 0) for k, v in CONTA.items()}
        ult = sorted([b for b in B['bank_transactions'] if b['bank_account_id'] == PRINCIPAL], key=lambda b: b['created_at'])
        s.saldo_extrato = {PRINCIPAL: float(ult[-1].get('balance_after') or 0) if ult else 0.0}
        s.n = 0

    def add(s, tab, row):
        s.t.setdefault(tab, []).append(row)
        return row

    def ct(s, chave, caixa, tipo, valor, desc, quando, por, order=None, **kw):
        r = {'id': f'@id:t09.ct.{chave}', 'company_id': CID, 'cash_register_id': caixa, 'type': tipo, 'amount': valor, 'description': desc,
             'transaction_at': quando, 'transaction_date': dia_br(quando), 'created_at': quando,
             'created_by': por, 'excluded_from_dre': False}
        if order:
            r['order_id'] = order
        r.update(kw)
        return s.add('cash_transactions', r)

    def bt(s, chave, conta, tipo, valor, desc, quando, por, order=None, **kw):
        s.saldo_extrato[conta] = r2(s.saldo_extrato.get(conta, 0) + valor)
        s.banco[conta] = r2(s.banco[conta] + valor)
        r = {'id': f'@id:t09.bt.{chave}', 'company_id': CID, 'bank_account_id': conta, 'type': tipo, 'amount': valor, 'description': desc,
             'transaction_at': quando, 'transaction_date': dia_br(quando), 'created_at': quando, 'created_by': por, 'source': 'manual',
             'excluded_from_dre': False, 'balance_after': s.saldo_extrato[conta]}
        if order:
            r['order_id'] = order
        r.update(kw)
        return s.add('bank_transactions', r)

    def caixa(s, n, por, abre, valor):
        s.add('cash_register', {'id': CX[n], 'company_id': CID, 'register_number': n, 'status': 'open', 'opened_at': abre, 'opened_by': por,
                                'initial_opening_balance': valor, 'opening_balance': valor, 'closing_balance': None, 'closed_at': None,
                                'currency': 'BRL', 'created_at': abre})
        s.ct(f'abre{n}', CX[n], 'opening', valor, f'Abertura do Caixa #{n}', abre, por)

    def pedido(s, chave, tipo, parceiro, itens, quando, por, caixa, forma, numero):
        """tipo 'purchase'/'sale'; itens [(material, qtd, preço, impureza)]; forma 'cash'/'transfer'"""
        isc = tipo == 'purchase'
        pid = f'@id:t09.{"compra" if isc else "venda"}.{chave}'
        total = r2(sum(r2((q - imp) * pr) for _, q, pr, imp in itens))
        head = {'id': pid, 'company_id': CID, 'order_number': numero, 'order_seq': numero, 'order_period': None, 'order_ref': f'#{numero}',
                'status': 'completed', 'total_amount': total, 'paid_amount': total, 'payment_method': forma, 'created_by': por,
                'transaction_at': quando, 'transaction_date': dia_br(quando), 'created_at': quando, 'currency': 'BRL', 'notes': None,
                'driver_name': None, 'vehicle_plate': None, 'driver_id': None, 'vehicle_id': None,
                ('supplier_id' if isc else 'customer_id'): parceiro}
        if isc:
            head['hide_financial_details'] = False
        s.add('purchases' if isc else 'sales', head)
        rot = 'Compra' if isc else 'Venda'
        for k, (mat, q, pr, imp) in enumerate(itens):
            liq = q - imp
            item = {'id': f'@id:t09.{"pi" if isc else "si"}.{chave}.{k}', ('purchase_id' if isc else 'sale_id'): pid, 'material_id': mat,
                    'material_name': NOME_MAT[mat], 'quantity': q, 'unit_price': pr, 'total_price': r2(liq * pr), 'impurity': imp,
                    'impurity_kg': imp or None, 'impurity_pct': (round(imp / q * 100, 2) if imp else None), 'item_discount': 0,
                    'tare_weight': None, 'first_weight': None, 'second_weight': None, 'weighing_mode': None, 'weight_source': 'manual'}
            s.add('purchase_items' if isc else 'sale_items', item)
            antes = s.estoque[mat]
            depois = round(antes + (liq if isc else -liq), 3)
            s.estoque[mat] = depois
            s.add('stock_movements', {'id': f'@id:t09.sm.{chave}.{k}', 'company_id': CID, 'material_id': mat, 'type': 'COMPRA' if isc else 'VENDA',
                                      'quantity': liq if isc else -liq, 'stock_before': antes, 'stock_after': depois, 'order_id': pid,
                                      'order_type': tipo, 'description': f'{rot} #{numero}' + (f' ({imp}kg impureza)' if imp else ''),
                                      'created_by': por, 'transaction_at': quando, 'transaction_date': dia_br(quando), 'created_at': quando})
        if forma == 'cash':
            s.ct(f'{chave}', caixa, tipo, total, f'{rot} #{numero}', quando, por, order=pid)
        else:
            s.ct(f'{chave}', caixa, tipo, 0, f'{rot} #{numero} (PIX/Transferência)', quando, por, order=pid)
            s.bt(f'{chave}', PRINCIPAL, 'withdrawal' if isc else 'deposit', -total if isc else total, f'{rot} #{numero}', quando, por,
                 order=pid, payment_method='transfer')
        return pid, total

    def fecha(s, n, quando, valor, por):
        s.ct(f'fecha{n}', CX[n], 'closing', valor, 'Fechamento de caixa', quando, por)
        for c in s.t['cash_register']:
            if c['id'] == CX[n]:
                c.update(status='closed', closed_at=quando, closing_balance=valor, opening_balance=valor)


def dia_br(iso):
    """dia em Brasília de um ISO em UTC"""
    from datetime import datetime, timedelta
    d = datetime.strptime(iso[:19], '%Y-%m-%dT%H:%M:%S') - timedelta(hours=3)
    return d.strftime('%Y-%m-%d')


def patch_materiais(e, mats):
    return [{'match': {'id': m}, 'set': {'current_stock': e.estoque[m]}} for m in mats]


def grava(nome, doc, dados):
    os.makedirs(SAIDA, exist_ok=True)
    out = {'_doc': doc}
    out.update(dados)
    with open(os.path.join(SAIDA, f'{nome}.json'), 'w', encoding='utf8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    n = sum(len(v) for k, v in dados.items() if isinstance(v, list))
    print(f'{nome}: {n} linhas' + (f' + patch {sorted(dados["_patch"])}' if '_patch' in dados else '') + (f' + remove {sorted(dados["_remove"])}' if '_remove' in dados else ''))


def main():
    e = Estado()
    num = ULT_PEDIDO
    # ---------------------------------------------------------------- 10/11 (T6 + T8), fechado no fim do dia
    D10 = '2026-11-10'
    e.caixa(85, RAFAEL, z(D10, '08:31'), 1500.0)
    e.caixa(86, MARCOS, z(D10, '08:45'), 17000.0)
    quando = z(D10, '08:50')
    e.ct('saque86', CX[86], 'transfer', 3000.0, '↓ SAQUE · Conta Principal → Caixa #86', quando, RAFAEL)
    e.bt('saque86', PRINCIPAL, 'transfer', -3000.0, '↑ SAQUE · Conta Principal → Caixa #86', quando, RAFAEL, cash_register_id=CX[86])
    e.bt('tarifa86', PRINCIPAL, 'expense', -6.5, 'Tarifa de Saque para o Caixa #86', quando, RAFAEL, cash_register_id=CX[86])
    num += 1
    e.pedido('t8', 'purchase', RECOMECO, [(LATINHA, 3080, 6.2, 61.6)], z(D10, '09:00'), RAFAEL, CX[85], 'transfer', num)
    num += 1
    e.pedido('quiririm', 'sale', QUIRIRIM, [(F_PESADO, 1600, 1.25, 0)], z(D10, '10:15'), RAFAEL, CX[85], 'transfer', num)
    num += 1
    e.pedido('cida10', 'purchase', CIDA, [(LATINHA, 42, 6.2, 0)], z(D10, '11:20'), RAFAEL, CX[85], 'cash', num)
    num += 1
    e.pedido('valdir10', 'purchase', VALDIR, [(F_MISTO, 310, 0.75, 0)], z(D10, '15:05'), RAFAEL, CX[85], 'cash', num)
    e.fecha(85, z(D10, '17:44'), 1007.1, RAFAEL)
    e.fecha(86, z(D10, '17:36'), 20000.0, MARCOS)
    # ---------------------------------------------------------------- 11/11 de manhã: o #87 do Rafael
    D11 = '2026-11-11'
    e.caixa(87, RAFAEL, z(D11, '07:10'), 1200.0)
    num += 1
    cida, _ = e.pedido('cida', 'purchase', CIDA, [(LATINHA, 24, 6.2, 0)], z(D11, '07:22'), RAFAEL, CX[87], 'cash', num)
    n_cida = num
    num += 1
    valdir, _ = e.pedido('valdir', 'purchase', VALDIR, [(F_MISTO, 280, 0.75, 0)], z(D11, '07:41'), RAFAEL, CX[87], 'cash', num)
    num += 1
    dup, _ = e.pedido('valdir_dup', 'purchase', VALDIR, [(F_MISTO, 280, 0.75, 0)], z(D11, '07:42'), RAFAEL, CX[87], 'cash', num)
    n_dup = num
    for c in e.t['cash_register']:
        if c['id'] == CX[87]:
            c['opening_balance'] = r2(1200 - 148.8 - 210 - 210)
    # ---------------------------------------------------------------- o estorno de 03/11 (só se o mundo base ainda não tiver)
    tem_estorno = any(p.get('reverted_at') and p.get('supplier_id') == CIDA and p.get('transaction_date') == '2026-11-03' for p in B['purchases'])
    if not tem_estorno:
        cx03 = next(c for c in B['cash_register'] if c['opened_at'][:10] == '2026-11-03' and c['opened_by'] == MARCOS)
        cx05 = next(c for c in B['cash_register'] if c['opened_at'][:10] == '2026-11-05' and c['opened_by'] == MARCOS)
        itens = [(LATINHA, 38, 6.2, 0), (PAPELAO, 280, 0.55, 0)]
        orig, _ = e.pedido('cida03', 'purchase', CIDA, itens, z('2026-11-03', '09:40'), MARCOS, cx03['id'], 'cash', ULT_PEDIDO + 90)
        copia, tot = e.pedido('cida03b', 'purchase', CIDA, itens, z('2026-11-03', '09:41'), MARCOS, cx03['id'], 'cash', ULT_PEDIDO + 91)
        quando = z('2026-11-05', '08:12')
        for p in e.t['purchases']:
            if p['id'] == copia:
                p.update(reverted_at=quando, reverted_compensation_register_id=cx05['id'])
        e.ct('estorno03', cx05['id'], 'adjustment', tot, f'Estorno da Compra #{ULT_PEDIDO + 91}', quando, MARCOS, reversal_for_order_id=copia)
        print('PROVISÓRIO: o mundo base ainda não tem a cópia estornada de 03/11 da Aparecida; vai nesta semente')
    tem_audit = any(a.get('entity_type') == 'purchase' for a in B.get('destructive_actions_audit', []))
    if not tem_audit:
        copia_b = next((p for p in B['purchases'] if p.get('reverted_at') and p.get('supplier_id') == CIDA), None) or next(p for p in e.t['purchases'] if p.get('reverted_at'))
        e.add('destructive_actions_audit', {
            'id': '@id:t09.audit.05nov', 'company_id': CID, 'action_type': 'delete_entity', 'entity_type': 'purchase', 'entity_id': copia_b['id'],
            'entity_label': 'Aparecida Ramos', 'performed_by': MARCOS, 'performed_by_email': 'marcos.antunes@reciclavalemetais.example',
            'performed_by_role': 'operator', 'company_name_snapshot': 'Recicla Vale Metais', 'company_email_snapshot': None,
            'entity_snapshot': {'order_number': copia_b['order_number'], 'total_amount': copia_b['total_amount']},
            'payload': {'mode': 'compensated', 'order_type': 'purchase'}, 'ip_address': None, 'user_agent': None,
            'created_at': copia_b.get('reverted_at') or z('2026-11-05', '08:12')})
    dados = dict(e.t)
    dados['_patch'] = {'materials': patch_materiais(e, [LATINHA, F_PESADO, F_MISTO, PAPELAO]),
                       'bank_accounts': [{'match': {'id': PRINCIPAL}, 'set': {'balance': e.banco[PRINCIPAL]}}]}
    grava('inicio', 'T09 · estado de 11/11 08:30: o dia 10/11 (T6 e T8) fechado e o caixa #87 do Rafael com as três compras da manhã '
          '(latinha da Aparecida com 24 kg; a compra do Valdir lançada duas vezes). Gerado por rec/t09/t09_sementes.py.', dados)

    # ---------------------------------------------------------------- apos-cap04: latinha 24 -> 42 kg
    st = e.estoque[LATINHA] + 18
    grava('apos-cap04', 'T09 · depois do cap04: a compra da Aparecida editada para 42 kg de latinha (R$ 260,40, mesmo número e hora, no #87).', {'_patch': {
        'purchases': [{'match': {'id': cida}, 'set': {'total_amount': 260.4, 'paid_amount': 260.4}}],
        'purchase_items': [{'match': {'id': '@id:t09.pi.cida.0'}, 'set': {'quantity': 42, 'total_price': 260.4}}],
        'stock_movements': [{'match': {'id': '@id:t09.sm.cida.0'}, 'set': {'quantity': 42, 'stock_after': e.estoque[LATINHA] - 24 + 42}}],
        'cash_transactions': [{'match': {'id': '@id:t09.ct.cida'}, 'set': {'amount': 260.4}}],
        'materials': [{'match': {'id': LATINHA}, 'set': {'current_stock': st}}],
        'cash_register': [{'match': {'id': CX[87]}, 'set': {'opening_balance': r2(1200 - 260.4 - 420)}}],
    }})
    # ---------------------------------------------------------------- apos-cap05: a duplicada do Valdir excluída
    grava('apos-cap05', 'T09 · depois do cap05: a compra duplicada do Valdir (07:42) excluída, com a linha do Histórico de Exclusões.', {
        '_remove': {'purchases': [{'id': dup}], 'purchase_items': [{'id': '@id:t09.pi.valdir_dup.0'}], 'stock_movements': [{'id': '@id:t09.sm.valdir_dup.0'}],
                    'cash_transactions': [{'id': '@id:t09.ct.valdir_dup'}]},
        '_patch': {'materials': [{'match': {'id': F_MISTO}, 'set': {'current_stock': e.estoque[F_MISTO] - 280}}],
                   'cash_register': [{'match': {'id': CX[87]}, 'set': {'opening_balance': r2(1200 - 260.4 - 210)}}]},
        'destructive_actions_audit': [{
            'id': '@id:t09.audit.valdir', 'company_id': CID, 'action_type': 'delete_entity', 'entity_type': 'purchase', 'entity_id': dup,
            'entity_label': 'Valdir Pereira', 'performed_by': RAFAEL, 'performed_by_email': 'rafael@reciclavalemetais.example',
            'performed_by_role': 'company_admin', 'company_name_snapshot': 'Recicla Vale Metais', 'company_email_snapshot': None,
            'entity_snapshot': {'order_number': n_dup, 'total_amount': 210}, 'payload': {'mode': 'hard_delete', 'order_type': 'purchase'},
            'ip_address': None, 'user_agent': None, 'created_at': z(D11, '08:33')}],
    })
    # ---------------------------------------------------------------- apos-cap06: cupom sem valor no Valdir
    grava('apos-cap06', 'T09 · depois do cap06: "Cupom sem valor" ligado na compra do Valdir (07:41).', {'_patch': {
        'purchases': [{'match': {'id': valdir}, 'set': {'hide_financial_details': True}}]}})
    print(f'pedidos #{ULT_PEDIDO + 1}..#{num} (latinha #{n_cida}, duplicada #{n_dup}); caixas #85 a #87')


if __name__ == '__main__':
    main()
