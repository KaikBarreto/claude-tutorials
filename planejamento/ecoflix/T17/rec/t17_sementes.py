#!/usr/bin/env python3
"""T17 · gera rec/mundo/seeds-extra/t17/inicio.json: o estado de partida da aula (10/11 09:30), por cima do mundo base.

O T17 parte do fim do T16 (MUNDO_LINHA_DO_TEMPO.md, seção 14). Como a T16 ainda não deixou semente, este arquivo traz o mínimo
do T16 que aparece nas telas do T17 (T16/plano.md): NF-e 1249 (Serra Fina, cancelada), 1250 (Fundição, cobre mel 500 kg) e 1251
(entrada do caixa de 09/11, R$ 803,30); 1246 e 1247 inutilizadas; Notas Recebidas (NF-e) ligado com as notas 2157 e 884.
E o que é do T17 (T17/plano.md, "Mundo: o que esta aula precisa"; junção, seção 11):
 - NF-e 1252 (09:05, Alumínio perfil 3.200 kg x R$ 10,40 = R$ 33.280,00) e 1253 (09:12, Alumínio bloco 2.600 kg x R$ 8,50 =
   R$ 22.100,00) para a Serra Fina (Itamonte, MG, CFOP 6102), autorizadas, com chave e protocolo; soma R$ 55.380,00 e 5.800 kg.
 - Saldo inicial fiscal em 01/08/2026 por material (`fiscal_inventory_entries`, opening_balance): a base do Kardex fiscal. A
   quantidade de cada material é a menor que mantém o saldo fiscal >= 0 em todo o período (agosto a hoje), arredondada para
   cima em 500 kg, mais 500 kg (nenhum material fica negativo na Posição nem no Kardex).
Frota (FKD2E41 com tara 6.380 kg, motoristas só com nome e telefone), configuração fiscal (Taubaté, IM, certificado, MDF-e 0,
NFS-e recebidas desligado) e as NFS-e 12 e 13 já vêm do mundo base.
Uso: python3 -I rec/t17/t17_sementes.py"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
MUNDO = os.path.normpath(os.path.join(HERE, '..', 'mundo'))
SAIDA = os.path.join(MUNDO, 'seeds-extra', 't17', 'inicio.json')
CNPJ = '47318506000107'
COMPANY = '@id:company.reciclavale'
FISCAL = '@id:fiscal.matriz'


def utc(dia, hhmm):
    """hora de Brasília -> ISO UTC"""
    h, m = map(int, hhmm.split(':'))
    h += 3
    return f'{dia}T{h:02d}:{m:02d}:00.000Z'


def chave(dia, num, cnf):
    base = f'35{dia[2:4]}{dia[5:7]}{CNPJ}55001{num:09d}1{cnf:08d}'
    s, w = 0, 2
    for ch in reversed(base):
        s += int(ch) * w
        w = 2 if w == 9 else w + 1
    r = s % 11
    return base + str(0 if r < 2 else 11 - r)


def nota(num, dia, hhmm, tipo, cfop, itens, cnf, *, cliente=None, fornecedor=None, avulso=None, natureza=None, status='emitida',
         cancelada=None, criador='@id:user.rafael', final=False):
    iid = f'@id:nfe.{num}'
    total = round(sum(q * p for _, _, q, p in itens), 2)
    em = utc(dia, hhmm)
    h, m = map(int, hhmm.split(':'))
    aut = utc(dia, f'{h:02d}:{m + 1:02d}')
    inv = {
        'id': iid, 'company_id': COMPANY, 'fiscal_config_id': FISCAL, 'invoice_number': num, 'serie': 1, 'modelo': 55,
        'invoice_type': tipo, 'status': status, 'environment': 'producao', 'finalidade': 1,
        'nature_operation': natureza or ('Venda de mercadorias' if tipo == 'saida' else 'Compra de mercadorias'), 'cfop_default': cfop,
        'modalidade_frete': 9, 'is_consumer_final': final, 'customer_id': cliente, 'supplier_id': fornecedor,
        'destinatario_avulso': avulso, 'order_id': None, 'order_type': None, 'issue_date': em, 'authorized_at': aut,
        'nfe_key': chave(dia, num, cnf), 'nfe_protocol': f'1352600{num:04d}{cnf % 10000:04d}', 'plugnotas_id': f'pn-{num:06d}',
        'total_products': total, 'total_amount': total, 'total_freight': 0, 'other_expenses': 0, 'valor_desconto_total': 0,
        'computa_estoque_fiscal': True, 'baixa_estoque_ao_emitir': False, 'created_by': criador, 'created_at': em, 'updated_at': aut,
    }
    if cancelada:
        inv.update({'cancelled_at': cancelada[0], 'cancellation_reason': cancelada[1], 'updated_at': cancelada[0]})
    its = [{'id': f'@id:nfe_item.{num}.{j}', 'invoice_id': iid, 'material_id': f'@id:material.{k}', 'material_name': nome,
            'ncm': NCM[k], 'cfop': cfop, 'unit': 'KG', 'quantity': q, 'unit_price': p, 'total_price': round(q * p, 2),
            'nfe_item_number': j + 1, 'origem': 0, 'impurity': 0, 'valor_desconto': 0, 'created_at': em}
           for j, (k, nome, q, p) in enumerate(itens)]
    return inv, its


def main():
    base = {}
    for f in sorted(os.listdir(os.path.join(MUNDO, 'seeds'))):
        for t, rows in json.load(open(os.path.join(MUNDO, 'seeds', f), encoding='utf8')).items():
            if isinstance(rows, list):
                base.setdefault(t, []).extend(rows)
    global NCM
    NCM = {m['id'].split('.', 1)[1]: m['ncm'].replace('.', '') for m in base['materials']}
    nomes = {m['id'].split('.', 1)[1]: m['name'] for m in base['materials']}
    hoje = '2026-11-10'
    notas = [
        # T16 (cap09 a cap12): 1249 cancelada (a Serra Fina mudou o pedido), 1250 com carta de correção, 1251 do caixa de 09/11
        nota(1249, hoje, '08:41', 'saida', '6102', [('al_perfil', nomes['al_perfil'], 320, 10.40)], 52714093,
             cliente='@id:cliente.serrafina', cancelada=(utc(hoje, '08:57'), 'Pedido alterado pelo cliente antes de a mercadoria sair do pátio')),
        nota(1250, hoje, '08:46', 'saida', '5102', [('cobre_mel', nomes['cobre_mel'], 500, 47.90)], 61830257, cliente='@id:cliente.bandeira'),
        nota(1251, hoje, '08:51', 'entrada', '1102', [('al_latinha', nomes['al_latinha'], 64, 6.20), ('papelao', nomes['papelao'], 180, 0.55),
                                                       ('ferro_misto', nomes['ferro_misto'], 410, 0.75)], 70493618,
             avulso={'name': 'Consumidor Final'}, natureza='Entrada de sucata para revenda (pessoa física)', final=True),
        # T17: a carga de alumínio para a Serra Fina (Itamonte, MG), emitida às 09:05 e 09:12
        nota(1252, hoje, '09:05', 'saida', '6102', [('al_perfil', nomes['al_perfil'], 3200, 10.40)], 38160542, cliente='@id:cliente.serrafina'),
        nota(1253, hoje, '09:12', 'saida', '6102', [('al_bloco', nomes['al_bloco'], 2600, 8.50)], 49271653, cliente='@id:cliente.serrafina'),
    ]
    inv = [n[0] for n in notas]
    its = [i for n in notas for i in n[1]]
    assert round(inv[3]['total_amount'] + inv[4]['total_amount'], 2) == 55380 and inv[2]['total_amount'] == 803.3
    assert inv[0]['total_amount'] == 3328 and inv[1]['total_amount'] == 23950

    # saldo inicial fiscal em 01/08 (00:00 de Brasília): o menor que mantém o saldo >= 0, + 500 kg, em múltiplos de 500
    efeito = {'1102': 1, '2102': 1, '1202': 1, '5102': -1, '6102': -1, '6101': -1, '5502': -1, '6502': -1}
    todas = {i['id']: i for i in base['invoices'] + inv}
    mov = []
    for it in base['invoice_items'] + its:
        n = todas[it['invoice_id']]
        if n['status'] not in ('emitida', 'cancelada'):
            continue
        k = it['material_id'].split('.', 1)[1]
        q = it['quantity'] * efeito.get(it['cfop'], 0)
        mov.append((n['issue_date'], k, q))
        if n['status'] == 'cancelada':
            mov.append((n['cancelled_at'], k, -q))
    mov.sort()
    minimo = {k: 0.0 for k in nomes}
    saldo = {k: 0.0 for k in nomes}
    for _, k, q in mov:
        saldo[k] += q
        minimo[k] = min(minimo[k], saldo[k])
    abertura = {k: int(math.ceil(-minimo[k] / 500.0) * 500 + 500) for k in nomes}
    lote = '@id:t17.fiscal_opening_batch'
    entradas = [{
        'id': f'@id:t17.fiscal_opening.{k}', 'company_id': COMPANY, 'fiscal_config_id': FISCAL, 'material_id': f'@id:material.{k}',
        'entry_type': 'opening_balance', 'quantity_delta': abertura[k], 'effective_at': '2026-08-01T03:00:00.000Z',
        'reason': 'Saldo inicial fiscal (inventário de 31/07 informado pela contabilidade)', 'source': 'manual',
        'import_batch_id': lote, 'client_request_id': '@id:t17.fiscal_opening_req', 'reverses_entry_id': None,
        'created_by': '@id:user.rafael', 'created_at': '2026-08-03T12:10:00.000Z'} for k in nomes]
    lotes = [{'id': lote, 'company_id': COMPANY, 'fiscal_config_id': FISCAL, 'operation_type': 'record_entries',
              'entry_type': 'opening_balance', 'effective_at': '2026-08-01T03:00:00.000Z', 'source': 'manual',
              'reason': 'Saldo inicial fiscal', 'item_count': len(entradas), 'client_request_id': '@id:t17.fiscal_opening_req',
              'request_fingerprint': 't17-opening', 'created_by': '@id:user.rafael', 'created_at': '2026-08-03T12:10:00.000Z'}]

    # Notas Recebidas (NF-e) do T16: ligado às 08:58, as notas da Auto Peças Vale Forte (confirmada) e do Depósito Irmãos Siqueira
    recebidas = []
    for num, dia, emit, cnpj, valor, manif, cnf in ((2157, '2026-11-05', 'Auto Peças Vale Forte', '96384120000109', 1984.0, 'confirmada', 18273645),
                                                     (884, '2026-11-06', 'Depósito Irmãos Siqueira', '95127438000141', 2100.0, 'ciencia', 29384756)):
        b = f'35{dia[2:4]}{dia[5:7]}{cnpj}55001{num:09d}1{cnf:08d}'
        s, w = 0, 2
        for ch in reversed(b):
            s += int(ch) * w
            w = 2 if w == 9 else w + 1
        r = s % 11
        recebidas.append({
            'id': f'@id:t17.inbound_nfe.{num}', 'company_id': COMPANY, 'fiscal_config_id': FISCAL, 'chave': b + str(0 if r < 2 else 11 - r),
            'numero': str(num), 'serie': '1', 'emitente_cnpj': cnpj, 'emitente_nome': emit, 'data_emissao': utc(dia, '10:20'), 'valor': valor,
            'situacao_sefaz': 'autorizada', 'manifestacao': manif, 'manifestacao_data': utc(hoje, '08:59'), 'natureza': 'Venda de mercadorias',
            'cfop_principal': '5102', 'resumo': False, 'nsu': str(4180 + len(recebidas)), 'created_at': utc(hoje, '08:58'), 'updated_at': utc(hoje, '08:59')})

    out = {
        '_doc': 'T17 · estado de partida (10/11 09:30): o fim do T16 que aparece no T17 (NF-e 1249 cancelada, 1250, 1251, 1246 e 1247 '
                'inutilizadas, Notas Recebidas ligado) + NF-e 1252 e 1253 da Serra Fina + saldo inicial fiscal de 01/08. Gerado por rec/t17/t17_sementes.py.',
        'invoices': inv, 'invoice_items': its,
        'nfe_inutilized_numbers': [{'id': '@id:t17.inutil.1246', 'company_id': COMPANY, 'fiscal_config_id': FISCAL, 'serie': 1, 'ano': 2026,
                                    'numero_inicial': 1246, 'numero_final': 1247, 'invoice_type': 'saida', 'status': 'inutilizada', 'cstat': '102',
                                    'justificativa': 'Numeração pulada por ajuste incorreto do último número da série em outubro',
                                    'protocolo_sefaz': '135260000412873', 'homologated_at': utc(hoje, '08:54'), 'created_by': '@id:user.rafael',
                                    'created_at': utc(hoje, '08:53')}],
        'inbound_nfe': recebidas,
        'fiscal_inventory_entry_batches': lotes, 'fiscal_inventory_entries': entradas,
        '_patch': {
            'company_fiscal_config': [{'match': {'id': FISCAL}, 'set': {'last_invoice_number': 1253, 'dfe_ativo': True,
                                                                       'dfe_count_start_at': utc(hoje, '08:58'), 'updated_at': utc(hoje, '09:13')}}],
            'nfe_series': [{'match': {'id': '@id:nfe_serie.1'}, 'set': {'last_invoice_number': 1253, 'updated_at': utc(hoje, '09:13')}}],
        },
    }
    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    json.dump(out, open(SAIDA, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print('saldo inicial fiscal (kg):', ', '.join(f'{nomes[k]} {abertura[k]}' for k in nomes))
    print('->', os.path.relpath(SAIDA, os.path.join(HERE, '..', '..')))


if __name__ == '__main__':
    main()
