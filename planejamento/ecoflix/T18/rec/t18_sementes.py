#!/usr/bin/env python3
"""T18 · gera rec/mundo/seeds-extra/t18/inicio.json: o estado de partida da aula (10/11 09:30), por cima do mundo base (app 1.60.22, 21/11).

O T18 parte do fim do T17 (MUNDO_LINHA_DO_TEMPO.md, seção 14). Traz só o que aparece nas telas do T18 (T18/plano.md, "Mundo: o que
esta aula precisa"): as NF-e do dia 1249 a 1253 (a lista de Saída do cap09, iguais às do T16 e do T17) e a **NF-e 1254** das 09:20
(Aços Quiririm, chaparia 3.600 kg x R$ 0,98 = R$ 3.528,00, autorizada, com chave). Nada de MTR, CDF, acesso ao SIGOR, parceiros ou
resíduo salvo: o cap03 e o cap04 criam isso na tela. O Ambiental já vem do mundo base (UF SP, `mtr_uf_sistema` SP -> `sigor_sp`,
`mtr_sistemas` ativo, protocolo sinir).
`--cadeia`: gera `apos-cap03`, `04`, `06`, `07`, `09` e `10` (cumulativas, sintéticas: o que a aula cria na tela; ver `chain()`). O MTR 2611000325 sai na tela do
cap06 (modelo); os três MTR de 04/11 (erro, confirmar no órgão, rascunho) entram na `apos-cap07`; os CDF com erro, rascunho e sem PDF, na `apos-cap10`.
Uso: python3 -I rec/t18/t18_sementes.py [--cadeia]"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MUNDO = os.path.normpath(os.path.join(HERE, '..', 'mundo'))
PASTA = os.path.join(MUNDO, 'seeds-extra', 't18')
CNPJ = '47318506000107'
COMPANY = '@id:company.reciclavale'
FISCAL = '@id:fiscal.matriz'


def utc(dia, hhmm):
    """hora de Brasília -> ISO UTC"""
    h, m = map(int, hhmm.split(':'))
    return f'{dia}T{h + 3:02d}:{m:02d}:00.000Z'


def chave(dia, num, cnf):
    base = f'35{dia[2:4]}{dia[5:7]}{CNPJ}55001{num:09d}1{cnf:08d}'
    s, w = 0, 2
    for ch in reversed(base):
        s += int(ch) * w
        w = 2 if w == 9 else w + 1
    r = s % 11
    return base + str(0 if r < 2 else 11 - r)


def nota(num, dia, hhmm, tipo, cfop, itens, cnf, *, cliente=None, fornecedor=None, avulso=None, natureza=None, status='emitida',
         cancelada=None, final=False):
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
        'computa_estoque_fiscal': True, 'baixa_estoque_ao_emitir': False, 'created_by': '@id:user.rafael', 'created_at': em, 'updated_at': aut,
    }
    if cancelada:
        inv.update({'cancelled_at': cancelada[0], 'cancellation_reason': cancelada[1], 'updated_at': cancelada[0]})
    its = [{'id': f'@id:nfe_item.{num}.{j}', 'invoice_id': iid, 'material_id': f'@id:material.{k}', 'material_name': nome,
            'ncm': NCM[k], 'cfop': cfop, 'unit': 'KG', 'quantity': q, 'unit_price': p, 'total_price': round(q * p, 2),
            'nfe_item_number': j + 1, 'origem': 0, 'impurity': 0, 'valor_desconto': 0, 'created_at': em}
           for j, (k, nome, q, p) in enumerate(itens)]
    return inv, its


def base_mundo():
    base = {}
    for f in sorted(os.listdir(os.path.join(MUNDO, 'seeds'))):
        for t, rows in json.load(open(os.path.join(MUNDO, 'seeds', f), encoding='utf8')).items():
            if isinstance(rows, list):
                base.setdefault(t, []).extend(rows)
    return base


def inicio():
    global NCM
    base = base_mundo()
    NCM = {m['id'].split('.', 1)[1]: m['ncm'].replace('.', '') for m in base['materials']}
    nomes = {m['id'].split('.', 1)[1]: m['name'] for m in base['materials']}
    hoje = '2026-11-10'
    # junção (JUNCAO_160): a T18 recebe da T17 as notas até a 1256 (as mesmas do `t17/inicio`) e cria a 1257 (chaparia, 3.600 kg x R$ 0,98)
    t17 = json.load(open(os.path.join(PASTA, '..', 't17', 'inicio.json'), encoding='utf8'))
    inv = [r for r in t17['invoices'] if r['invoice_number'] <= 1256]
    its = [r for r in t17['invoice_items'] if r['invoice_id'] in {i['id'] for i in inv}]
    n1257 = nota(1257, hoje, '09:20', 'saida', '5102', [('chaparia', nomes['chaparia'], 3600, 0.98)], 57204913, cliente='@id:cliente.quiririm')
    inv.append(n1257[0])
    its += n1257[1]
    assert inv[-1]['total_amount'] == 3528.0, inv[-1]['total_amount']
    out = {
        '_doc': 'T18 · estado de partida (10/11 09:30): as NF-e do dia 1249 a 1256 (T16 e T17, copiadas do t17/inicio) + NF-e 1257 da chaparia para a '
                'Aços Quiririm. Gerado por rec/t18/t18_sementes.py.',
        'invoices': inv, 'invoice_items': its,
        '_patch': {
            'company_fiscal_config': [{'match': {'id': FISCAL}, 'set': {'last_invoice_number': 1257, 'updated_at': utc(hoje, '09:21')}}],
            'nfe_series': [{'match': {'id': '@id:nfe_serie.1'}, 'set': {'last_invoice_number': 1257, 'updated_at': utc(hoje, '09:21')}}],
        },
    }
    os.makedirs(PASTA, exist_ok=True)
    json.dump(out, open(os.path.join(PASTA, 'inicio.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print('-> rec/mundo/seeds-extra/t18/inicio.json:', len(inv), 'notas,', len(its), 'itens; chave 1257:', inv[-1]['nfe_key'])


# ---------------------------------------------------------------- cadeia de sementes (sintética; conferida contra o ensaio)
USER = '@id:user.rafael'
SIS = 'sigor_sp'
CNPJ_QUIRIRIM = '98463027000115'
CNPJ_VALEFORTE = '96384120000109'
# a lupa do CNPJ (handler cnpj-lookup, T4) devolve esta razão social para a Aços Quiririm: é a que o robô cadastra no destinador
RAZAO_QUIRIRIM = 'AÇOS QUIRIRIM INDUSTRIA E COMERCIO LTDA'


def listas_sigor():
    """as seis listas que o "Sincronizar dados do SIGOR" grava (as mesmas de rec/mundo/lib/mtr_sigor.mjs)"""
    import subprocess
    js = ("import('" + os.path.join(MUNDO, 'lib', 'mtr_sigor.mjs') + "').then(m=>console.log(JSON.stringify(m.REF)))")
    return json.loads(subprocess.check_output(['node', '-e', js]))


def chain():
    """apos-cap03, 04, 06, 07, 09 e 10, cumulativas desde `inicio` (o que a aula cria na tela, na ordem dos capítulos de 21/11):
    03 acesso+resíduo | 04 parceiros e MTR 318 | 06 MTR 325 (o modelo, emitido na tela do cap06) | 07 325 cancelado + os três MTR de 04/11
    (erro, confirmar no órgão, rascunho: o cap08) | 09 CDF 2611000041 (o cap09 emite) | 10 os CDF com erro, rascunho e sem PDF (o cap11).
    Os capítulos 5, 8, 10 e 12 só leem; o 6 e o 9 partem da semente anterior e CRIAM o que a seguinte traz."""
    hoje = '2026-11-10'
    key1257 = chave(hoje, 1257, 57204913)
    # cap03: acesso, listas do órgão, resíduo salvo e os três ferros ligados a ele
    ref = {t: [{'sistema': SIS, 'codigo': c, 'descricao': d} for c, d in linhas] for t, linhas in listas_sigor().items()}
    preset = '@id:t18.preset.sucata_ferro'
    cap03 = {
        'mtr_credentials': [{'id': '@id:t18.cred', 'company_id': COMPANY, 'sistema': SIS, 'usuario_cpf': '27491350879', 'cod_unidade_gerador': 203918,
                             'ambiente': 'prod', 'cnpj_unidade': None, 'senha_secret_id': 'cofre-fictício', 'created_at': utc(hoje, '09:24'),
                             'updated_at': utc(hoje, '09:24'), 'last_validated_at': utc(hoje, '09:25'), 'last_validation_status': 'success',
                             'last_validation_message': 'Acesso ao SIGOR aceito. A emissão ainda depende de a unidade possuir perfil Gerador no portal.'}],
        **ref,
        'mtr_residuo_presets': [{'id': preset, 'company_id': COMPANY, 'sistema': SIS, 'apelido': 'Sucata de ferro', 'residuo_ibama': '19 12 02',
                                 'codigo_classe': 2, 'codigo_estado_fisico': 1, 'codigo_acondicionamento': 5, 'codigo_tratamento': 1,
                                 'codigo_unidade': 1, 'densidade': None, 'created_by': USER, 'created_at': utc(hoje, '09:26'),
                                 'updated_at': utc(hoje, '09:26')}],
        '_patch': {'materials': [{'match': {'id': f'@id:material.{k}'}, 'set': {'mtr_residuo_preset_id': preset}} for k in ('ferro_pesado', 'ferro_misto', 'chaparia')]},
    }
    # cap04: transportador, destinador (razão social vinda da lupa) e o MTR 2611000318 (chaparia, 3,6 TON, Jair Lopes, GHT7B19) com a tentativa autorizada
    mid = '@id:t18.mtr.318'
    em = utc(hoje, '09:29')
    base_mtr = {'company_id': COMPANY, 'sistema': SIS, 'transportador_cnpj': CNPJ, 'transportador_cod_unidade': 203918,
                'transportador_razao': 'Recicla Vale Metais Ltda', 'nome_motorista': 'Jair Lopes', 'placa': 'GHT7B19',
                'destinador_cnpj': CNPJ_QUIRIRIM, 'destinador_cod_unidade': 187402, 'destinador_razao': RAZAO_QUIRIRIM,
                'responsavel_nome': 'Rafael Nogueira', 'responsavel_cargo': 'Sócio-administrador', 'created_by': USER}
    item_mtr = {'residuo_ibama': '19 12 02', 'codigo_classe': 2, 'codigo_estado_fisico': 1, 'codigo_acondicionamento': 5, 'codigo_tratamento': 1,
                'codigo_unidade': 1, 'observacao': None, 'densidade': None}
    cap04 = {
        'mtr_parceiros': [
            {'id': '@id:t18.parc.transp', 'company_id': COMPANY, 'sistema': SIS, 'tipo': 'transportador', 'cnpj': CNPJ, 'razao_social': 'Recicla Vale Metais Ltda',
             'cod_unidade': 203918, 'created_at': utc(hoje, '09:27'), 'updated_at': utc(hoje, '09:27')},
            {'id': '@id:t18.parc.dest', 'company_id': COMPANY, 'sistema': SIS, 'tipo': 'destinador', 'cnpj': CNPJ_QUIRIRIM, 'razao_social': RAZAO_QUIRIRIM,
             'cod_unidade': 187402, 'created_at': utc(hoje, '09:27'), 'updated_at': utc(hoje, '09:27')}],
        'mtr_manifests': [{**base_mtr, 'id': mid, 'manifesto_codigo': '2611000318', 'status': 'emitido', 'data_expedicao': hoje,
                           'observacao': f'NF-e 1257: {key1257}', 'pdf_url': 't18/mtr-2611000318.pdf', 'error_message': None, 'emitted_at': em,
                           'created_at': utc(hoje, '09:28'), 'updated_at': em,
                           'raw_response': {'objetoResposta': {'manifestoNumeroNacional': '2611000318'}, 'mensagem': 'Manifesto emitido (simulado).'}}],
        'mtr_manifest_items': [{**item_mtr, 'id': '@id:t18.mtr.318.item', 'manifest_id': mid, 'quantidade': 3.6}],
        'mtr_manifest_attempts': [{'id': '@id:t18.mtr.318.tent', 'company_id': COMPANY, 'manifest_id': mid, 'state': 'authorized', 'stage': 'complete',
                                   'error_code': None, 'error_message': None, 'provider_request_started_at': em, 'finished_at': em, 'created_at': em}],
    }
    # cap06: o MTR 2611000325 da carga de ferro misto, emitido na tela pelo modelo (a observação foi apagada)
    m2 = '@id:t18.mtr.325'
    e2 = utc(hoje, '09:40')
    cap06 = {
        'mtr_manifests': [{**base_mtr, 'id': m2, 'manifesto_codigo': '2611000325', 'status': 'emitido', 'data_expedicao': hoje, 'observacao': None,
                           'pdf_url': 't18/mtr-2611000325.pdf', 'error_message': None, 'emitted_at': e2, 'created_at': utc(hoje, '09:39'), 'updated_at': e2,
                           'raw_response': {'objetoResposta': {'manifestoNumeroNacional': '2611000325'}, 'mensagem': 'Manifesto emitido (simulado).'}}],
        'mtr_manifest_items': [{**item_mtr, 'id': '@id:t18.mtr.325.item', 'manifest_id': m2, 'quantidade': 3.2}],
        'mtr_manifest_attempts': [{'id': '@id:t18.mtr.325.tent', 'company_id': COMPANY, 'manifest_id': m2, 'state': 'authorized', 'stage': 'complete',
                                   'error_code': None, 'error_message': None, 'provider_request_started_at': e2, 'finished_at': e2, 'created_at': e2}],
    }
    # cap07 (10:40): o 2611000325 cancelado na tela + os três manifestos de 04/11 da Aços Quiririm (cap08): um com erro, um para confirmar no órgão, um rascunho
    msg_erro = 'O órgão recusou o envio: a classe informada não é aceita para este resíduo.'
    msg_incerto = 'Este envio pode ter chegado ao órgão. Consulte o portal antes de qualquer nova tentativa.'
    antigo = {**base_mtr, 'data_expedicao': '2026-11-04', 'observacao': None, 'pdf_url': None, 'emitted_at': None, 'manifesto_codigo': None}

    def antigos(chave_, status, hora, erro, estado, tent):
        i = f'@id:t18.mtr.{chave_}'
        crt = f'2026-11-04T{hora}:00.000Z'
        linhas = {'mtr_manifests': [{**antigo, 'id': i, 'status': status, 'error_message': erro, 'created_at': crt, 'updated_at': crt,
                                     'raw_response': None}],
                  'mtr_manifest_items': [{**item_mtr, 'id': i + '.item', 'manifest_id': i, 'quantidade': 2.8}]}
        if tent:
            linhas['mtr_manifest_attempts'] = [{'id': i + '.tent', 'company_id': COMPANY, 'manifest_id': i, 'state': estado, 'stage': 'provider',
                                                'error_code': None, 'error_message': erro, 'provider_request_started_at': crt, 'finished_at': crt, 'created_at': crt}]
        return linhas
    a1 = antigos('erro', 'erro', '17:05', msg_erro, 'rejected', True)
    a2 = antigos('incerto', 'incerto', '17:40', msg_incerto, 'uncertain', True)
    a3 = antigos('rascunho', 'rascunho', '18:10', None, None, False)
    cap07 = {'_patch': {'mtr_manifests': [{'match': {'id': m2}, 'set': {'status': 'cancelado', 'updated_at': utc(hoje, '10:41'),
                                                                       'raw_response': {'mensagem': 'Manifesto cancelado (simulado).'}}}]}}
    for a in (a1, a2, a3):
        for t, v in a.items():
            cap07.setdefault(t, []).extend(v)
    # cap09: o CDF de outubro da Auto Peças Vale Forte (três MTR recebidos e baixados no portal), emitido na tela
    cdf = '@id:t18.cdf'
    cap09 = {'mtr_cdf': [{'id': cdf, 'company_id': COMPANY, 'sistema': SIS, 'cer_data_inicial': '2026-10-01', 'cer_data_final': '2026-10-31',
                          'cer_observacao': None, 'parceiro_destinador': 203918, 'cnpj_destinador': CNPJ, 'nome_responsavel': 'Rafael Nogueira',
                          'gerador_unidade': 184527, 'gerador_cnpj': CNPJ_VALEFORTE,
                          'lista_manifestos': [{'manNumero': n} for n in ('2610001542', '2610001877', '2610002203')], 'status': 'emitido',
                          'numero_cdf': '2611000041', 'pdf_url': 't18/cdf-2611000041.pdf', 'erro_mensagem': None, 'emitted_at': utc(hoje, '10:52'),
                          'created_by': USER, 'created_at': utc(hoje, '10:51'), 'updated_at': utc(hoje, '10:52'),
                          'raw_response': {'numeroCDF': '2611000041', 'mensagem': 'Certificado emitido (simulado).'}}]}
    # cap10 (cap11 da aula): um CDF com erro (MTR sem baixa no portal), um rascunho e um emitido sem PDF (setembro)
    base_cdf = {'company_id': COMPANY, 'sistema': SIS, 'cer_observacao': None, 'parceiro_destinador': 203918, 'cnpj_destinador': CNPJ,
                'nome_responsavel': 'Rafael Nogueira', 'gerador_unidade': 184527, 'gerador_cnpj': CNPJ_VALEFORTE, 'created_by': USER}
    cap10 = {'mtr_cdf': [
        {**base_cdf, 'id': '@id:t18.cdf.erro', 'cer_data_inicial': '2026-11-01', 'cer_data_final': '2026-11-07', 'lista_manifestos': [{'manNumero': '2611000102'}],
         'status': 'erro', 'numero_cdf': None, 'pdf_url': None, 'emitted_at': None, 'created_at': utc('2026-11-08', '10:20'), 'updated_at': utc('2026-11-08', '10:21'),
         'erro_mensagem': 'Um ou mais MTRs ainda não foram recebidos no SIGOR. Dê baixa no recebimento do MTR no portal do órgão antes de emitir o CDF.',
         'raw_response': None},
        {**base_cdf, 'id': '@id:t18.cdf.rascunho', 'cer_data_inicial': '2026-11-08', 'cer_data_final': '2026-11-09', 'lista_manifestos': [{'manNumero': '2611000110'}],
         'status': 'rascunho', 'numero_cdf': None, 'pdf_url': None, 'emitted_at': None, 'created_at': utc('2026-11-09', '16:30'), 'updated_at': utc('2026-11-09', '16:30'),
         'erro_mensagem': None, 'raw_response': None},
        {**base_cdf, 'id': '@id:t18.cdf.semPdf', 'cer_data_inicial': '2026-09-01', 'cer_data_final': '2026-09-30',
         'lista_manifestos': [{'manNumero': n} for n in ('2609001655', '2609002014')], 'status': 'emitido', 'numero_cdf': '2611000037', 'pdf_url': None,
         'emitted_at': utc('2026-10-05', '09:10'), 'created_at': utc('2026-10-05', '09:09'), 'updated_at': utc('2026-10-05', '09:10'), 'erro_mensagem': None,
         'raw_response': {'numeroCDF': '2611000037', 'mensagem': 'Certificado emitido (simulado).'}}]}

    def soma(*partes):
        out = {'_doc': 'T18 · estado cumulativo desde o início da aula (sintético, conferido contra o ensaio). Gerado por rec/t18/t18_sementes.py --cadeia.'}
        for p in partes:
            for t, v in p.items():
                if t == '_patch':
                    for tt, vv in v.items():
                        out.setdefault('_patch', {}).setdefault(tt, []).extend(vv)
                elif t != '_doc':
                    out.setdefault(t, []).extend(v)
        # o `_patch` do cancelamento muda uma linha criada pela cadeia: aplica direto na linha (a semente não aplica _patch a linha da própria semente)
        for mm in out.get('_patch', {}).pop('mtr_manifests', []):
            for r in out['mtr_manifests']:
                if r['id'] == mm['match']['id']:
                    r.update(mm['set'])
        if not out.get('_patch', {}):
            out.pop('_patch', None)
        return out

    jogo = {'apos-cap03': (cap03,), 'apos-cap04': (cap03, cap04), 'apos-cap06': (cap03, cap04, cap06),
            'apos-cap07': (cap03, cap04, cap06, cap07), 'apos-cap09': (cap03, cap04, cap06, cap07, cap09),
            'apos-cap10': (cap03, cap04, cap06, cap07, cap09, cap10)}
    for nome, partes in jogo.items():
        json.dump(soma(*partes), open(os.path.join(PASTA, nome + '.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
        print('->', nome)


if __name__ == '__main__':
    chain() if '--cadeia' in sys.argv else inicio()
