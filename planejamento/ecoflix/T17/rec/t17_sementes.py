#!/usr/bin/env python3
"""T17 · gera rec/mundo/seeds-extra/t17/inicio.json: o estado de partida da aula (10/11 09:30), por cima do mundo base.

O T17 parte do fim do T16 (JUNCAO_160.md, seções 3 e 6). Como a T16 ainda não deixou a semente final, este arquivo traz o mínimo
do T16 que aparece nas telas do T17: NF-e 1249 (Serra Fina, cancelada), 1250 (Fundição, cobre mel 500 kg), 1251 (entrada do caixa
de 09/11, R$ 803,30), 1252 (Serra Fina, 150 kg de Alumínio perfil, R$ 1.560,00: a que foi rejeitada e corrigida), 1253 (entrada,
a Fundição devolve 40 kg de Cobre mel da 1250, R$ 1.916,00, CFOP 1202) e 1254 (complementar de preço da 1250, R$ 250,00, sem
efeito no estoque fiscal); 1246 e 1247 inutilizadas; Notas Recebidas (NF-e) ligado com as notas 2157 (com o lançamento fiscal dos
640 kg de bateria) e 884.
E o que é do T17 (T17/plano.md, "Mundo: o que esta aula precisa"; JUNCAO_160.md):
 - NF-e 1255 (09:05, Alumínio perfil 3.200 kg x R$ 10,40 = R$ 33.280,00) e 1256 (09:12, Alumínio bloco 2.600 kg x R$ 8,50 =
   R$ 22.100,00) para a Serra Fina (Itamonte, MG, CFOP 6102), autorizadas, com chave e protocolo; soma R$ 55.380,00 e 5.800 kg.
 - Saldo inicial fiscal em 01/08/2026 por material (`fiscal_inventory_entries`, opening_balance): a base do Kardex fiscal. A
   quantidade de cada material é a menor que mantém o saldo fiscal >= 0 em todo o período (agosto a hoje), arredondada para
   cima em 500 kg, mais 500 kg (nenhum material fica negativo no Saldo atual nem no Kardex). A BATERIA fica SEM saldo inicial
   (a faixa amarela do "Saldo atual"): a aula informa 3.320 kg em 31/10/2026 no capítulo do saldo inicial.
 - Série 1 da NFS-e (`nfse_series`, último número 13) e `nfse_dfe_fonte` = "sefin" (o motor próprio busca as NFS-e recebidas).
Também escreve as sementes laterais: t17/mdfe2-rejeitado (o MDF-e nº 2 recusado, só à tarde), t17/nfse-recebidas (as duas NFS-e
que o motor trouxe depois de ativar o recurso) e, desde 28/11 (1.60.39), t17/compra-coop (o caixa #85 aberto, só no capítulo 11).
28/11: a inicio ganhou a NF-e 3871 da Cooperativa Recomeço, importada pelo XML na T16 (cap23).
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
         cancelada=None, criador='@id:user.rafael', final=False, finalidade=1, estoque=True, total=None, ref=None):
    iid = f'@id:nfe.{num}'
    total = total if total is not None else round(sum(q * p for _, _, q, p in itens), 2)
    em = utc(dia, hhmm)
    h, m = map(int, hhmm.split(':'))
    aut = utc(dia, f'{h:02d}:{m + 1:02d}')
    inv = {
        'id': iid, 'company_id': COMPANY, 'fiscal_config_id': FISCAL, 'invoice_number': num, 'serie': 1, 'modelo': 55,
        'invoice_type': tipo, 'status': status, 'environment': 'producao', 'finalidade': finalidade,
        'nature_operation': natureza or ('Venda de mercadorias' if tipo == 'saida' else 'Compra de mercadorias'), 'cfop_default': cfop,
        'modalidade_frete': 9, 'is_consumer_final': final, 'customer_id': cliente, 'supplier_id': fornecedor,
        'destinatario_avulso': avulso, 'order_id': None, 'order_type': None, 'issue_date': em, 'authorized_at': aut,
        'nfe_key': chave(dia, num, cnf), 'nfe_protocol': f'1352600{num:04d}{cnf % 10000:04d}', 'plugnotas_id': f'pn-{num:06d}',
        'total_products': total, 'total_amount': total, 'total_freight': 0, 'other_expenses': 0, 'valor_desconto_total': 0,
        'computa_estoque_fiscal': estoque, 'baixa_estoque_ao_emitir': False, 'created_by': criador, 'created_at': em, 'updated_at': aut,
    }
    if ref:
        inv['nfe_referenciada'] = ref
    if cancelada:
        inv.update({'cancelled_at': cancelada[0], 'cancellation_reason': cancelada[1], 'updated_at': cancelada[0]})
    its = [{'id': f'@id:nfe_item.{num}.{j}', 'invoice_id': iid, 'material_id': f'@id:material.{k}', 'material_name': nome,
            'ncm': NCM[k], 'cfop': cfop, 'unit': 'KG', 'quantity': q, 'unit_price': p, 'total_price': round(q * p, 2) if q else total,
            'nfe_item_number': j + 1, 'origem': 0, 'impurity': 0, 'valor_desconto': 0, 'created_at': em}
           for j, (k, nome, q, p) in enumerate(itens)]
    return inv, its


def laterais(porn, hoje):
    """sementes laterais: o MDF-e nº 2 recusado (só à tarde, 14:20) e as duas NFS-e recebidas que o motor fiscal trouxe"""
    n1252 = porn[1252]
    mdfe2 = {
        'id': '@id:t17.mdfe.2', 'company_id': COMPANY, 'fiscal_config_id': FISCAL, 'mdfe_number': 2, 'serie': 1, 'status': 'rejeitado',
        'environment': 'producao', 'modal': 'rodoviario', 'tipo_emitente': 2, 'emission_mode': 'normal', 'placa_veiculo': 'GHT7B19',
        'uf_veiculo': 'SP', 'condutor_nome': 'Jair Lopes', 'condutor_cpf': '00000000000', 'tara_veiculo': 3900, 'capacidade_kg': 4000,
        'capacidade_m3': None, 'tipo_rodado': '02', 'tipo_carroceria': '02', 'reboques': [], 'uf_carregamento': 'SP',
        'cidade_carregamento': 'Taubaté', 'codigo_ibge_carregamento': '3554102', 'uf_descarregamento': 'MG', 'cidade_descarregamento': 'Itamonte',
        'codigo_ibge_descarregamento': '3133006', 'percurso_ufs': ['RJ'], 'peso_bruto_total': 150, 'valor_total_carga': 1560.0,
        'observacoes': None, 'plugnotas_id': 'pn-mdfe-000002', 'mdfe_key': None, 'mdfe_protocol': None, 'authorized_at': None, 'enclosed_at': None,
        'error_message': 'A SEFAZ recusou o MDF-e — CPF do condutor: número inválido',
        'created_by': '@id:user.rafael', 'created_at': utc(hoje, '13:52'), 'updated_at': utc(hoje, '13:53')}
    lat1 = {'_doc': 'T17 · lateral (só à tarde): o MDF-e nº 2 da viagem de amanhã (NF-e 1252, Caminhão 3/4, Jair Lopes), recusado pela SEFAZ '
                    'simulada por causa do CPF do motorista. A T18 não herda. Gerado por rec/t17/t17_sementes.py.',
            'mdfe_manifests': [mdfe2],
            'mdfe_invoices': [{'id': '@id:t17.mdfe.2.nfe', 'mdfe_id': mdfe2['id'], 'invoice_id': n1252['id'], 'nfe_key': n1252['nfe_key'],
                               'created_at': utc(hoje, '13:52')}],
            '_patch': {'company_fiscal_config': [{'match': {'id': FISCAL}, 'set': {'last_mdfe_number': 2}}]}}
    json.dump(lat1, open(os.path.join(os.path.dirname(SAIDA), 'mdfe2-rejeitado.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)

    def dv11(b):
        t, w = 0, 2
        for ch in reversed(b):
            t += int(ch) * w
            w = 2 if w == 9 else w + 1
        r = t % 11
        return str(0 if r < 2 else 11 - r)
    recebidas = []
    for x in ({'numero': '318', 'prestador_nome': 'Contabilidade Manacá Ltda', 'prestador_documento': '47291836000156', 'prestador_municipio_ibge': '3554102',
               'prestador_im': '38.214', 'data_emissao': '2026-11-05T13:40:00.000Z', 'competencia': '2026-10-01', 'valor_servico': 1650, 'valor_iss': 33,
               'codigo_tributacao_nacional': '171901', 'discriminacao': 'Honorários contábeis de outubro de 2026', 'nsu': '1022', 'cnum': 318204},
              {'numero': '1207', 'prestador_nome': 'Balanças Tremembé Manutenção Ltda', 'prestador_documento': '39506417000166', 'prestador_municipio_ibge': '3554805',
               'prestador_im': '9.471', 'data_emissao': '2026-11-07T14:15:00.000Z', 'competencia': '2026-11-01', 'valor_servico': 980, 'valor_iss': 29.4,
               'codigo_tributacao_nacional': '140101', 'discriminacao': 'Aferição e manutenção preventiva da balança rodoviária', 'nsu': '1023', 'cnum': 120779}):
        cnum = x.pop('cnum')
        b = f"{x['prestador_municipio_ibge']}21{x['prestador_documento']}{int(x['numero']):013d}{x['data_emissao'][2:4]}{x['data_emissao'][5:7]}{cnum:09d}"
        ch = b + dv11(b)
        recebidas.append({**x, 'id': f"@id:t17.inbound_nfse.{x['numero']}", 'company_id': COMPANY, 'fiscal_config_id': FISCAL, 'chave_acesso': ch,
                          'chave_natural': ch, 'serie': '1', 'tomador_documento': CNPJ, 'tomador_nome': 'Recicla Vale Metais Ltda',
                          'municipio_incidencia_ibge': x['prestador_municipio_ibge'], 'iss_retido': False, 'valor_liquido': x['valor_servico'],
                          'situacao': 'autorizada', 'fonte': 'sefin', 'fonte_ref': f"sefin-{x['nsu']}", 'resumo': False,
                          'created_at': utc(hoje, '14:24'), 'updated_at': utc(hoje, '14:24')})
    lat2 = {'_doc': 'T17 · lateral do capítulo "Da nota recebida à despesa": as duas NFS-e que o motor fiscal trouxe do Ambiente Nacional alguns '
                    'minutos depois de o recurso ser ativado (Contabilidade Manacá R$ 1.650,00 e Balanças Tremembé R$ 980,00). Entra por cima '
                    'da t17/apos-cap09. Gerado por rec/t17/t17_sementes.py.',
            'inbound_nfse': recebidas,
            '_patch': {'company_fiscal_config': [{'match': {'id': FISCAL}, 'set': {'nfse_dfe_last_sync_at': utc(hoje, '14:24'), 'nfse_dfe_ultimo_erro': None}}]}}
    json.dump(lat2, open(os.path.join(os.path.dirname(SAIDA), 'nfse-recebidas.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    # 28/11 (1.60.39): o caixa #85 do Rafael aberto às 08:31 com R$ 1.500,00 (o mesmo da T06, apos-cap02): a tela de Compra do
    # capítulo 11 pede caixa aberto. Só no 11 (a compra da Cooperativa sai por Pix, sem mexer no dinheiro do caixa).
    lat3 = {'_doc': 'T17 · lateral (só no capítulo 11): o caixa #85 do Rafael aberto às 08:31 com R$ 1.500,00, como na T06. A NF-e 3871 da '
                    'Cooperativa Recomeço vem da t17/inicio. Gerado por rec/t17/t17_sementes.py.',
            'cash_register': [{'id': '@id:caixa.85', 'company_id': COMPANY, 'register_number': 85, 'status': 'open', 'opened_at': utc(hoje, '08:31'),
                               'opened_by': '@id:user.rafael', 'initial_opening_balance': 1500, 'opening_balance': 1500, 'closing_balance': None,
                               'closed_at': None, 'currency': 'BRL', 'created_at': utc(hoje, '08:31')}],
            'cash_transactions': [{'id': '@id:ct.t17.abre85', 'company_id': COMPANY, 'cash_register_id': '@id:caixa.85', 'type': 'opening', 'amount': 1500,
                                   'description': 'Abertura do Caixa #85', 'transaction_at': utc(hoje, '08:31'), 'transaction_date': hoje,
                                   'created_at': utc(hoje, '08:31'), 'created_by': '@id:user.rafael', 'excluded_from_dre': False}]}
    json.dump(lat3, open(os.path.join(os.path.dirname(SAIDA), 'compra-coop.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)


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
             cliente='@id:cliente.serrafina', status='cancelada', cancelada=(utc(hoje, '08:57'), 'Pedido alterado pelo cliente antes de a mercadoria sair do pátio')),
        nota(1250, hoje, '08:46', 'saida', '5102', [('cobre_mel', nomes['cobre_mel'], 500, 47.90)], 61830257, cliente='@id:cliente.bandeira'),
        nota(1251, hoje, '08:51', 'entrada', '1102', [('al_latinha', nomes['al_latinha'], 64, 6.20), ('papelao', nomes['papelao'], 180, 0.55),
                                                       ('ferro_misto', nomes['ferro_misto'], 410, 0.75)], 70493618,
             avulso={'name': 'Consumidor Final'}, natureza='Entrada de sucata para revenda (pessoa física)', final=True),
        # T16 no 1.60.10 (JUNCAO_160.md): 1252 (a rejeitada, corrigida e autorizada), 1253 (devolução da Fundição) e 1254 (complementar)
        nota(1252, hoje, '08:59', 'saida', '6102', [('al_perfil', nomes['al_perfil'], 150, 10.40)], 52771252, cliente='@id:cliente.serrafina'),
        nota(1253, hoje, '09:01', 'entrada', '1202', [('cobre_mel', nomes['cobre_mel'], 40, 47.90)], 63881253, cliente='@id:cliente.bandeira',
             natureza='Devolução de venda de mercadoria', finalidade=4),
        nota(1254, hoje, '09:03', 'saida', '5102', [('cobre_mel', nomes['cobre_mel'], 0, 0)], 74991254, cliente='@id:cliente.bandeira',
             natureza='Complemento de preço', finalidade=2, estoque=False, total=250.0),
        # T17: a carga de alumínio para a Serra Fina (Itamonte, MG), emitida às 09:05 e 09:12
        nota(1255, hoje, '09:05', 'saida', '6102', [('al_perfil', nomes['al_perfil'], 3200, 10.40)], 38160542, cliente='@id:cliente.serrafina'),
        nota(1256, hoje, '09:12', 'saida', '6102', [('al_bloco', nomes['al_bloco'], 2600, 8.50)], 49271653, cliente='@id:cliente.serrafina'),
    ]
    porn = {n[0]['invoice_number']: n[0] for n in notas}
    inv = [n[0] for n in notas]
    its = [i for n in notas for i in n[1]]
    assert round(porn[1255]['total_amount'] + porn[1256]['total_amount'], 2) == 55380 and porn[1251]['total_amount'] == 803.3
    assert porn[1249]['total_amount'] == 3328 and porn[1250]['total_amount'] == 23950
    assert porn[1252]['total_amount'] == 1560 and porn[1253]['total_amount'] == 1916 and porn[1254]['total_amount'] == 250

    # saldo inicial fiscal em 01/08 (00:00 de Brasília): o menor que mantém o saldo >= 0, + 500 kg, em múltiplos de 500
    efeito = {'1102': 1, '2102': 1, '1202': 1, '5102': -1, '6102': -1, '6101': -1, '5502': -1, '6502': -1}
    todas = {i['id']: i for i in base['invoices'] + inv}
    mov = []
    for it in base['invoice_items'] + its:
        n = todas[it['invoice_id']]
        if n['status'] not in ('emitida', 'cancelada') or n.get('computa_estoque_fiscal') is False:
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
        'created_by': '@id:user.rafael', 'created_at': '2026-08-03T12:10:00.000Z'} for k in nomes if k != 'bateria']
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

    # 1.60.39 (28/11): a NF-e 3871 da Cooperativa Recomeço, importada na T16 (cap23) pelo "Importar XML". Mesmas colunas que a edge
    # inbound-xml-import grava (sem número nem série: a edge não grava) + o fiscal_config_id do gatilho e a manifestação padrão.
    # A compra dela é o capítulo 11 (lateral compra-coop).
    xml_coop = open(os.path.join(HERE, '..', 't16', 'assets', 'NFe-3871-Cooperativa-Recomeco.xml'), encoding='utf8').read()
    recebidas.append({
        'id': '@id:t17.inbound_nfe.3871', 'company_id': COMPANY, 'fiscal_config_id': FISCAL, 'chave': '35261197250936000102550010000038711640291473',
        'origem': 'manual', 'emitente_cnpj': '97250936000102', 'emitente_nome': 'Cooperativa Recomeço', 'valor': 7550.0,
        'data_emissao': '2026-11-09T16:20:00-03:00', 'natureza': 'Venda de mercadoria', 'situacao_sefaz': 'autorizada', 'xml_content': xml_coop,
        'resumo': False, 'manifestacao': 'nenhuma', 'purchase_id': None, 'created_at': utc(hoje, '09:02'), 'updated_at': utc(hoje, '09:02')})

    # a nota 2157 (bateria da Auto Peças Vale Forte, 640 kg a R$ 3,10) já foi lançada no estoque fiscal na T16
    lanc = [{'id': '@id:t17.inbound_fiscal.2157', 'company_id': COMPANY, 'inbound_nfe_id': '@id:t17.inbound_nfe.2157',
             'material_id': '@id:material.bateria', 'quantity': 640, 'unit': 'KG', 'valor': 1984.0, 'effect': 'entry',
             'created_by': '@id:user.rafael', 'created_at': utc(hoje, '08:59')}]
    out = {
        '_doc': 'T17 · estado de partida (10/11 09:30, app 1.60.39): o fim do T16 que aparece no T17 (NF-e 1249 cancelada, 1250 a 1254, 1246 e '
                '1247 inutilizadas, Notas Recebidas ligado, a 2157 lançada no estoque fiscal, a 3871 da Cooperativa importada pelo XML) + NF-e '
                '1255 e 1256 da Serra Fina + saldo inicial '
                'fiscal de 01/08 (menos a bateria) + série 1 da NFS-e. Gerado por rec/t17/t17_sementes.py.',
        'inbound_nfe_fiscal_entries': lanc,
        'nfse_series': [{'id': '@id:t17.nfse_serie.1', 'company_id': COMPANY, 'fiscal_config_id': FISCAL, 'serie_number': 1,
                         'last_nfse_number': 13, 'created_at': '2026-07-30T14:00:00.000Z', 'updated_at': '2026-10-29T17:31:00.000Z'}],
        'invoices': inv, 'invoice_items': its,
        'nfe_inutilized_numbers': [{'id': '@id:t17.inutil.1246', 'company_id': COMPANY, 'fiscal_config_id': FISCAL, 'serie': 1, 'ano': 2026,
                                    'numero_inicial': 1246, 'numero_final': 1247, 'invoice_type': 'saida', 'status': 'inutilizada', 'cstat': '102',
                                    'justificativa': 'Numeração pulada por ajuste incorreto do último número da série em outubro',
                                    'protocolo_sefaz': '135260000412873', 'homologated_at': utc(hoje, '08:54'), 'created_by': '@id:user.rafael',
                                    'created_at': utc(hoje, '08:53')}],
        'inbound_nfe': recebidas,
        'fiscal_inventory_entry_batches': lotes, 'fiscal_inventory_entries': entradas,
        '_patch': {
            'company_fiscal_config': [{'match': {'id': FISCAL}, 'set': {'last_invoice_number': 1256, 'dfe_ativo': True, 'nfse_dfe_fonte': 'sefin',
                                                                       'dfe_count_start_at': utc(hoje, '08:58'), 'updated_at': utc(hoje, '09:13')}}],
            'nfe_series': [{'match': {'id': '@id:nfe_serie.1'}, 'set': {'last_invoice_number': 1256, 'updated_at': utc(hoje, '09:13')}}],
        },
    }
    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    json.dump(out, open(SAIDA, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    laterais(porn, hoje)
    print('saldo inicial fiscal (kg):', ', '.join(f'{nomes[k]} {abertura[k]}' for k in nomes if k != 'bateria'))
    print('->', os.path.relpath(SAIDA, os.path.join(HERE, '..', '..')))


if __name__ == '__main__':
    main()
