#!/usr/bin/env python3
"""T18 · gera rec/mundo/seeds-extra/t18/inicio.json: o estado de partida da aula (10/11 09:30), por cima do mundo base.

O T18 parte do fim do T17 (MUNDO_LINHA_DO_TEMPO.md, seção 14). Traz só o que aparece nas telas do T18 (T18/plano.md, "Mundo: o que
esta aula precisa"): as NF-e do dia 1249 a 1253 (a lista de Saída do cap09, iguais às do T16 e do T17) e a **NF-e 1254** das 09:20
(Aços Quiririm, chaparia 3.600 kg x R$ 0,98 = R$ 3.528,00, autorizada, com chave). Nada de MTR, CDF, acesso ao SIGOR, parceiros ou
resíduo salvo: o cap03 e o cap04 criam isso na tela. O Ambiental já vem do mundo base (UF SP, `mtr_uf_sistema` SP -> `sigor_sp`,
`mtr_sistemas` ativo, protocolo sinir).
`--cadeia`: gera `apos-cap03` .. `apos-cap07` (cumulativas, sintéticas: o que a aula cria na tela, linha a linha; o cap05 já traz o MTR
2611000325 da carga da tarde, emitido às 09:40 pelo modelo, que o cap06 cancela). Depois do ensaio, `t18_semente.py apos-capNN --ver`
compara a semente com o que o robô de fato criou.
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
    notas = [
        nota(1249, hoje, '08:41', 'saida', '6102', [('al_perfil', nomes['al_perfil'], 320, 10.40)], 52714093, cliente='@id:cliente.serrafina',
             status='cancelada', cancelada=(utc(hoje, '08:57'), 'Pedido alterado pelo cliente antes de a mercadoria sair do pátio')),
        nota(1250, hoje, '08:46', 'saida', '5102', [('cobre_mel', nomes['cobre_mel'], 500, 47.90)], 61830257, cliente='@id:cliente.bandeira'),
        nota(1251, hoje, '08:51', 'entrada', '1102', [('al_latinha', nomes['al_latinha'], 64, 6.20), ('papelao', nomes['papelao'], 180, 0.55),
                                                       ('ferro_misto', nomes['ferro_misto'], 410, 0.75)], 70493618,
             avulso={'name': 'Consumidor Final'}, natureza='Entrada de sucata para revenda (pessoa física)', final=True),
        nota(1252, hoje, '09:05', 'saida', '6102', [('al_perfil', nomes['al_perfil'], 3200, 10.40)], 38160542, cliente='@id:cliente.serrafina'),
        nota(1253, hoje, '09:12', 'saida', '6102', [('al_bloco', nomes['al_bloco'], 2600, 8.50)], 49271653, cliente='@id:cliente.serrafina'),
        # T18: a carga de chaparia para a Aços Quiririm (SP), emitida às 09:20 sem pedido (o pedido fecha na entrega)
        nota(1254, hoje, '09:20', 'saida', '5102', [('chaparia', nomes['chaparia'], 3600, 0.98)], 57204913, cliente='@id:cliente.quiririm'),
    ]
    inv = [n[0] for n in notas]
    its = [i for n in notas for i in n[1]]
    assert inv[-1]['total_amount'] == 3528.0, inv[-1]['total_amount']
    out = {
        '_doc': 'T18 · estado de partida (10/11 09:30): as NF-e do dia 1249 a 1253 (T16 e T17) + NF-e 1254 da chaparia para a Aços Quiririm. '
                'Gerado por rec/t18/t18_sementes.py.',
        'invoices': inv, 'invoice_items': its,
        '_patch': {
            'company_fiscal_config': [{'match': {'id': FISCAL}, 'set': {'last_invoice_number': 1254, 'updated_at': utc(hoje, '09:21')}}],
            'nfe_series': [{'match': {'id': '@id:nfe_serie.1'}, 'set': {'last_invoice_number': 1254, 'updated_at': utc(hoje, '09:21')}}],
        },
    }
    os.makedirs(PASTA, exist_ok=True)
    json.dump(out, open(os.path.join(PASTA, 'inicio.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print('-> rec/mundo/seeds-extra/t18/inicio.json:', len(inv), 'notas,', len(its), 'itens; chave 1254:', inv[-1]['nfe_key'])


# ---------------------------------------------------------------- cadeia de sementes (sintética; conferida contra o ensaio)
USER = '@id:user.rafael'
SIS = 'sigor_sp'
CNPJ_QUIRIRIM = '98463027000115'
CNPJ_VALEFORTE = '96384120000109'


def listas_sigor():
    """as seis listas que o "Sincronizar dados do SIGOR" grava (as mesmas de rec/mundo/lib/mtr_sigor.mjs)"""
    import subprocess
    js = ("import('" + os.path.join(MUNDO, 'lib', 'mtr_sigor.mjs') + "').then(m=>console.log(JSON.stringify(m.REF)))")
    return json.loads(subprocess.check_output(['node', '-e', js]))


def chain():
    """apos-cap03 .. apos-cap07, cumulativas desde `inicio` (o que a aula cria na tela, na ordem dos capítulos)."""
    hoje = '2026-11-10'
    base = base_mundo()
    key1254 = chave(hoje, 1254, 57204913)
    ini = json.load(open(os.path.join(PASTA, 'inicio.json'), encoding='utf8'))
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
    # cap04: transportador, destinador e o MTR 2611000318 (chaparia, 3,6 TON, Jair Lopes, GHT7B19) com a tentativa autorizada
    mid = '@id:t18.mtr.318'
    em = utc(hoje, '09:29')
    cap04 = {
        'mtr_parceiros': [
            {'id': '@id:t18.parc.transp', 'company_id': COMPANY, 'sistema': SIS, 'tipo': 'transportador', 'cnpj': CNPJ, 'razao_social': 'Recicla Vale Metais Ltda',
             'cod_unidade': 203918, 'created_at': utc(hoje, '09:27'), 'updated_at': utc(hoje, '09:27')},
            {'id': '@id:t18.parc.dest', 'company_id': COMPANY, 'sistema': SIS, 'tipo': 'destinador', 'cnpj': CNPJ_QUIRIRIM, 'razao_social': 'Aços Quiririm Ltda',
             'cod_unidade': 187402, 'created_at': utc(hoje, '09:27'), 'updated_at': utc(hoje, '09:27')}],
        'mtr_manifests': [{'id': mid, 'company_id': COMPANY, 'sistema': SIS, 'manifesto_codigo': '2611000318', 'status': 'emitido',
                           'transportador_cnpj': CNPJ, 'transportador_cod_unidade': 203918, 'transportador_razao': 'Recicla Vale Metais Ltda',
                           'nome_motorista': 'Jair Lopes', 'placa': 'GHT7B19', 'data_expedicao': hoje, 'destinador_cnpj': CNPJ_QUIRIRIM,
                           'destinador_cod_unidade': 187402, 'destinador_razao': 'Aços Quiririm Ltda', 'responsavel_nome': 'Rafael Nogueira',
                           'responsavel_cargo': 'Sócio-administrador', 'observacao': f'NF-e 1254: {key1254}', 'pdf_url': f'mtr/{COMPANY}/{mid}.pdf',
                           'error_message': None, 'emitted_at': em, 'created_by': USER, 'created_at': utc(hoje, '09:28'), 'updated_at': em,
                           'raw_response': {'objetoResposta': {'manifestoNumeroNacional': '2611000318'}, 'mensagem': 'Manifesto emitido (simulado).'}}],
        'mtr_manifest_items': [{'id': '@id:t18.mtr.318.item', 'manifest_id': mid, 'residuo_ibama': '19 12 02', 'codigo_classe': 2, 'codigo_estado_fisico': 1,
                                'codigo_acondicionamento': 5, 'codigo_tratamento': 1, 'quantidade': 3.6, 'codigo_unidade': 1, 'observacao': None,
                                'densidade': None}],
        'mtr_manifest_attempts': [{'id': '@id:t18.mtr.318.tent', 'company_id': COMPANY, 'manifest_id': mid, 'state': 'authorized', 'stage': 'complete',
                                   'error_code': None, 'error_message': None, 'provider_request_started_at': em, 'finished_at': em, 'created_at': em}],
    }
    # cap05 (10:40): o MTR 2611000325 emitido às 09:40 pelo modelo, que o cap06 cancela
    m2 = '@id:t18.mtr.325'
    e2 = utc(hoje, '09:40')
    cap05 = {
        'mtr_manifests': [{**{k: v for k, v in cap04['mtr_manifests'][0].items() if k != 'raw_response'}, 'id': m2, 'manifesto_codigo': '2611000325',
                           'observacao': None, 'pdf_url': f'mtr/{COMPANY}/{m2}.pdf', 'emitted_at': e2, 'created_at': utc(hoje, '09:39'), 'updated_at': e2,
                           'raw_response': {'objetoResposta': {'manifestoNumeroNacional': '2611000325'}, 'mensagem': 'Manifesto emitido (simulado).'}}],
        'mtr_manifest_items': [{**cap04['mtr_manifest_items'][0], 'id': '@id:t18.mtr.325.item', 'manifest_id': m2, 'quantidade': 3.2}],
        'mtr_manifest_attempts': [{**cap04['mtr_manifest_attempts'][0], 'id': '@id:t18.mtr.325.tent', 'manifest_id': m2, 'provider_request_started_at': e2,
                                   'finished_at': e2, 'created_at': e2}],
    }
    # cap06: o 2611000325 cancelado
    cap06 = {'_patch': {'mtr_manifests': [{'match': {'id': m2}, 'set': {'status': 'cancelado', 'updated_at': utc(hoje, '10:41'),
                                                                       'raw_response': {'mensagem': 'Manifesto cancelado (simulado).'}}}]}}
    # cap07: o CDF de outubro da Auto Peças Vale Forte (três MTR recebidos e baixados no portal)
    cdf = '@id:t18.cdf'
    cap07 = {'mtr_cdf': [{'id': cdf, 'company_id': COMPANY, 'sistema': SIS, 'cer_data_inicial': '2026-10-01', 'cer_data_final': '2026-10-31',
                          'cer_observacao': None, 'parceiro_destinador': 203918, 'cnpj_destinador': CNPJ, 'nome_responsavel': 'Rafael Nogueira',
                          'gerador_unidade': 184527, 'gerador_cnpj': CNPJ_VALEFORTE,
                          'lista_manifestos': [{'manNumero': n} for n in ('2610001542', '2610001877', '2610002203')], 'status': 'emitido',
                          'numero_cdf': '2611000041', 'pdf_url': f'cdf/{COMPANY}/{cdf}.pdf', 'erro_mensagem': None, 'emitted_at': utc(hoje, '10:52'),
                          'created_by': USER, 'created_at': utc(hoje, '10:51'), 'updated_at': utc(hoje, '10:52'),
                          'raw_response': {'numeroCDF': '2611000041', 'mensagem': 'Certificado emitido (simulado).'}}]}

    def soma(*partes):
        out = {'_doc': 'T18 · estado cumulativo desde o início da aula (sintético, conferido contra o ensaio). Gerado por rec/t18/t18_sementes.py --cadeia.'}
        for p in partes:
            for t, v in p.items():
                if t == '_patch':
                    for tt, vv in v.items():
                        out.setdefault('_patch', {}).setdefault(tt, []).extend(vv)
                elif t != '_doc':
                    out.setdefault(t, []).extend(v)
        # o `_patch` de apos-cap06 muda uma linha criada pela cadeia: aplica direto na linha (a semente não aplica _patch a linha da própria semente)
        for mm in out.get('_patch', {}).pop('mtr_manifests', []):
            for r in out['mtr_manifests']:
                if r['id'] == mm['match']['id']:
                    r.update(mm['set'])
        if not out.get('_patch', {}):
            out.pop('_patch', None)
        return out

    jogo = {'apos-cap03': (cap03,), 'apos-cap04': (cap03, cap04), 'apos-cap05': (cap03, cap04, cap05), 'apos-cap06': (cap03, cap04, cap05, cap06),
            'apos-cap07': (cap03, cap04, cap05, cap06, cap07)}
    for nome, partes in jogo.items():
        json.dump(soma(*partes), open(os.path.join(PASTA, nome + '.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
        print('->', nome)


if __name__ == '__main__':
    chain() if '--cadeia' in sys.argv else inicio()
