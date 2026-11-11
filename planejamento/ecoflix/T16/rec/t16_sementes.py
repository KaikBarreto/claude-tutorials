#!/usr/bin/env python3
"""T16 · sementes extras em rec/mundo/seeds-extra/t16/ e os arquivos do seletor de arquivo (rec/t16/assets/).

  python3 -I rec/t16/t16_sementes.py inicio
      escreve t16/inicio.json: a "demonstração fiscal sobre B" (MUNDO_LINHA_DO_TEMPO, seção 1): a configuração fiscal da matriz
      volta ao estado de antes do certificado (mesma linha, @id:fiscal.matriz, com os campos que a aula preenche em branco), sem
      série, sem notas, sem transportadora e sem cenário; e as duas notas recebidas (2157 da Auto Peças Vale Forte, 05/11, com XML;
      884 do Depósito Irmãos Siqueira, 06/11, três itens, só o resumo), que aparecem quando a aula liga as Notas Recebidas (cap15).
  python3 -I rec/t16/t16_sementes.py assets
      escreve rec/t16/assets/recicla-vale-metais-a1.pfx (bytes falsos, 2 KB) e NFe-3871-Cooperativa-Recomeco.xml (NF-e 4.00 fictícia).
  python3 -I rec/t16/t16_sementes.py captura NN [--porta 54316]
      logo DEPOIS de um ensaio do capítulo NN com 0 passo falho, lê a instância do Supabase falso e escreve t16/apos-capNN.json: as
      linhas criadas na aula (created_at >= FAKE_NOW) e, como _patch, os campos que a aula mudou nas linhas do mundo. Cumulativo: o
      capítulo seguinte parte de ["t16/inicio", "t16/apos-capNN"]. Molde: rec/t13/t13_sementes.py.
Nada de credencial (a chave anônima é a pública do build falso) e nenhum dado real: CNPJ e chaves fictícios, com dígito válido.
"""
import hashlib
import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
TUT_HOME = os.path.normpath(os.path.join(HERE, '..', '..'))
MUNDO = os.path.join(TUT_HOME, 'rec', 'mundo')
SAIDA = os.path.join(MUNDO, 'seeds-extra', 't16')
ASSETS = os.path.join(HERE, 'assets')
FAKE_NOW_Z = '2026-11-10T11:30:00'   # 08:30 em Brasília
EMP = '@id:company.reciclavale'
CFG = '@id:fiscal.matriz'
RECICLA = {'cnpj': '47318506000107', 'nome': 'RECICLA VALE METAIS LTDA', 'ie': '688123456117', 'lgr': 'Rua das Oficinas', 'nro': '1250',
           'bairro': 'Parque Industrial', 'mun': 'Taubate', 'cmun': '3554102', 'uf': 'SP', 'cep': '12086410'}
EMITENTES = {
    'valeforte': {'cnpj': '96384120000109', 'nome': 'Auto Peças Vale Forte', 'fant': 'Auto Peças Vale Forte', 'ie': '6892416508',
                  'lgr': 'Avenida Brasil', 'nro': '1290', 'bairro': 'Centro', 'mun': 'Taubate', 'cmun': '3554102', 'uf': 'SP', 'cep': '12080010'},
    'siqueira': {'cnpj': '95127438000141', 'nome': 'Depósito Irmãos Siqueira', 'fant': 'Depósito Irmãos Siqueira', 'ie': '6819312381',
                 'lgr': 'Estrada do Pinheirinho', 'nro': '2730', 'bairro': 'Pinheirinho', 'mun': 'Tremembe', 'cmun': '3554805', 'uf': 'SP',
                 'cep': '12091500'},
    'recomeco': {'cnpj': '97250936000102', 'nome': 'Cooperativa Recomeço', 'fant': 'Cooperativa Recomeço', 'ie': '6865520635',
                 'lgr': 'Rua do Trabalho', 'nro': '57', 'bairro': 'Vila Nossa Senhora das Gracas', 'mun': 'Taubate', 'cmun': '3554102',
                 'uf': 'SP', 'cep': '12060640'},
}
# notas recebidas (MUNDO_LINHA_DO_TEMPO, seções 7 e 11): (emitente, número, data/hora de Brasília, natureza, itens, protocolo)
NOTAS = {
    'valeforte': ('valeforte', 2157, '2026-11-05T09:40:00-03:00', 'Venda de mercadoria', '5102',
                  [('BAT-SUC', 'SUCATA DE BATERIA AUTOMOTIVA', '85491100', 640, 3.10)], '135260512783416'),
    'siqueira': ('siqueira', 884, '2026-11-06T09:50:00-03:00', 'Venda de mercadoria', '5102',
                 [('FE-PES', 'FERRO PESADO', '72044900', 1200, 0.95), ('FE-MIS', 'FERRO MISTO', '72044900', 320, 0.75),
                  ('CU-MIS', 'COBRE MISTO', '74040000', 20, 36.00)], '135260611904528'),
    'recomeco': ('recomeco', 3871, '2026-11-09T16:20:00-03:00', 'Venda de mercadoria', '5102',
                 [('ALU-LAT', 'ALUMINIO LATINHA', '76020000', 850, 6.20), ('PET-PRE', 'PLASTICO PET PRENSADO', '39159000', 1200, 1.90)],
                 '135260934417285'),
}
XML_COOP = 'NFe-3871-Cooperativa-Recomeco.xml'
PFX = 'recicla-vale-metais-a1.pfx'


def dv11(base):
    soma, peso = 0, 2
    for ch in reversed(base):
        soma += int(ch) * peso
        peso = 2 if peso == 9 else peso + 1
    r = soma % 11
    return '0' if r < 2 else str(11 - r)


def chave(cnpj, numero, data, serie=1, uf='35'):
    cnf = str(int(hashlib.sha1(f'{cnpj}{numero}'.encode()).hexdigest(), 16) % 10 ** 8).zfill(8)
    base = f'{uf}{data[2:4]}{data[5:7]}{cnpj}55{serie:03d}{numero:09d}1{cnf}'
    return base + dv11(base), cnf


def fmt(v, n=2):
    return f'{v:.{n}f}'


def nfe_xml(chave_id):
    em_k, numero, data, nat, cfop, itens, prot = NOTAS[chave_id]
    em = EMITENTES[em_k]
    ch, cnf = chave(em['cnpj'], numero, data)
    total = round(sum(q * v for _, _, _, q, v in itens), 2)
    det = ''
    for i, (cp, xp, ncm, q, v) in enumerate(itens, 1):
        det += (f'<det nItem="{i}"><prod><cProd>{cp}</cProd><cEAN>SEM GTIN</cEAN><xProd>{xp}</xProd><NCM>{ncm}</NCM><CFOP>{cfop}</CFOP>'
                f'<uCom>KG</uCom><qCom>{fmt(q, 4)}</qCom><vUnCom>{fmt(v, 10)}</vUnCom><vProd>{fmt(q * v)}</vProd><cEANTrib>SEM GTIN</cEANTrib>'
                f'<uTrib>KG</uTrib><qTrib>{fmt(q, 4)}</qTrib><vUnTrib>{fmt(v, 10)}</vUnTrib><indTot>1</indTot></prod>'
                '<imposto><ICMS><ICMS51><orig>0</orig><CST>51</CST></ICMS51></ICMS><PIS><PISNT><CST>09</CST></PISNT></PIS>'
                '<COFINS><COFINSNT><CST>09</CST></COFINSNT></COFINS></imposto></det>')
    end = lambda p, tag: (f'<{tag}><xLgr>{p["lgr"]}</xLgr><nro>{p["nro"]}</nro><xBairro>{p["bairro"]}</xBairro><cMun>{p["cmun"]}</cMun>'
                          f'<xMun>{p["mun"]}</xMun><UF>{p["uf"]}</UF><CEP>{p["cep"]}</CEP><cPais>1058</cPais><xPais>BRASIL</xPais></{tag}>')
    return ('<?xml version="1.0" encoding="UTF-8"?>'
            '<nfeProc xmlns="http://www.portalfiscal.inf.br/nfe" versao="4.00"><NFe xmlns="http://www.portalfiscal.inf.br/nfe">'
            f'<infNFe versao="4.00" Id="NFe{ch}"><ide><cUF>35</cUF><cNF>{cnf}</cNF><natOp>{nat}</natOp><mod>55</mod><serie>1</serie>'
            f'<nNF>{numero}</nNF><dhEmi>{data}</dhEmi><tpNF>1</tpNF><idDest>1</idDest><cMunFG>{em["cmun"]}</cMunFG><tpImp>1</tpImp>'
            f'<tpEmis>1</tpEmis><cDV>{ch[-1]}</cDV><tpAmb>1</tpAmb><finNFe>1</finNFe><indFinal>0</indFinal><indPres>1</indPres>'
            '<procEmi>0</procEmi><verProc>1.0</verProc></ide>'
            f'<emit><CNPJ>{em["cnpj"]}</CNPJ><xNome>{em["nome"]}</xNome>' + end(em, 'enderEmit') + f'<IE>{em["ie"]}</IE><CRT>3</CRT></emit>'
            f'<dest><CNPJ>{RECICLA["cnpj"]}</CNPJ><xNome>{RECICLA["nome"]}</xNome>' + end(RECICLA, 'enderDest')
            + f'<indIEDest>1</indIEDest><IE>{RECICLA["ie"]}</IE></dest>' + det
            + f'<total><ICMSTot><vBC>0.00</vBC><vICMS>0.00</vICMS><vICMSDeson>0.00</vICMSDeson><vFCP>0.00</vFCP><vBCST>0.00</vBCST>'
            f'<vST>0.00</vST><vFCPST>0.00</vFCPST><vFCPSTRet>0.00</vFCPSTRet><vProd>{fmt(total)}</vProd><vFrete>0.00</vFrete>'
            '<vSeg>0.00</vSeg><vDesc>0.00</vDesc><vII>0.00</vII><vIPI>0.00</vIPI><vIPIDevol>0.00</vIPIDevol><vPIS>0.00</vPIS>'
            f'<vCOFINS>0.00</vCOFINS><vOutro>0.00</vOutro><vNF>{fmt(total)}</vNF></ICMSTot></total>'
            '<transp><modFrete>9</modFrete></transp>'
            f'<pag><detPag><tPag>{"17" if em_k != "siqueira" else "99"}</tPag><vPag>{fmt(total)}</vPag></detPag></pag>'
            '<infAdic><infCpl>Documento ficticio (tutorial EcoFlix).</infCpl></infAdic></infNFe></NFe>'
            f'<protNFe versao="4.00"><infProt><tpAmb>1</tpAmb><verAplic>SP_NFE_PL009_V4</verAplic><chNFe>{ch}</chNFe>'
            f'<dhRecbto>{data}</dhRecbto><nProt>{prot}</nProt><digVal>ZmljdGljaW8=</digVal><cStat>100</cStat>'
            '<xMotivo>Autorizado o uso da NF-e</xMotivo></infProt></protNFe></nfeProc>'), ch, total


def _utc(data):
    from datetime import datetime, timezone
    return datetime.fromisoformat(data).astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z')


def recebida(k, nsu, com_xml):
    em_k, numero, data, nat, cfop, itens, prot = NOTAS[k]
    xml, ch, total = nfe_xml(k)
    em = EMITENTES[em_k]
    criada = _utc(data)
    return {'id': f'@id:inbound_nfe.{k}', 'company_id': EMP, 'fiscal_config_id': CFG, 'chave': ch, 'numero': str(numero), 'serie': '1',
            'emitente_cnpj': em['cnpj'], 'emitente_nome': em['nome'], 'data_emissao': criada, 'valor': total, 'natureza': nat,
            'cfop_principal': cfop, 'situacao_sefaz': 'autorizada', 'manifestacao': 'ciencia', 'manifestacao_data': criada,
            'manifestacao_pendente': None, 'manifestacao_pendente_em': None, 'manifestacao_erro': None, 'fin_nfe': 1,
            'resumo': not com_xml, 'xml_content': xml if com_xml else None, 'pdf_url': None, 'nsu': str(nsu), 'plugnotas_id': None,
            # bastidor: o XML que a "SEFAZ" entrega no Buscar documento (plugnotas-dfe-fetch-doc) e a prova oficial do status
            # (sem ela o selo SEFAZ seria "Aguardando confirmação oficial": lib/fiscal/statusConfirmation.ts)
            'xml_pendente': None if com_xml else xml,
            'fiscal_status_confirmation': {'status': 'authorized', 'key': ch, 'environment': '1', 'cstat': '100', 'protocol': prot,
                                           'source': 'sefaz_distribution_xml', 'observed_at': criada},
            'purchase_id': None, 'financial_bill_id': None, 'balance_movement_id': None, 'ref_nfe_key': None,
            'created_at': criada, 'updated_at': criada}


VAZIO_CFG = {   # o que a aula preenche na tela volta a vazio (o resto da linha, inclusive NFS-e e endereço, fica como em B)
    'razao_social': None, 'nome_fantasia': None, 'cnpj': None, 'inscricao_estadual': None, 'telefone': None, 'email': None,
    'regime_tributario': None, 'is_simples_nacional': True, 'pis_cofins_regime': None, 'pis_aliquota': None, 'cofins_aliquota': None,
    'cst_pis': None, 'cst_cofins': None, 'cst_pis_saida': None, 'cst_pis_entrada': None, 'cst_cofins_saida': None,
    'cst_cofins_entrada': None, 'icms_aliquota_interna': None, 'is_icms_contributor': None,
    'cfop_saida_interna': None, 'cfop_saida_interestadual': None, 'cfop_entrada_interna': None, 'cfop_entrada_interestadual': None,
    'calcular_ibs_cbs_auto': False, 'cst_ibscbs_saida': None, 'cclasstrib_saida': None, 'cst_ibscbs_entrada': None,
    'cclasstrib_entrada': None, 'has_previous_invoices': False, 'last_invoice_number': None, 'last_invoice_serie': None,
    'plugnotas_company_registered': False, 'plugnotas_company_registered_at': None, 'plugnotas_certificate_uploaded': False,
    'dfe_ativo': False, 'dfe_count_start_at': None, 'dfe_last_sync_at': None,
}


def inicio():
    return {
        '_doc': ('T16 · estado de partida por cima do mundo base B ("demonstração fiscal", MUNDO_LINHA_DO_TEMPO seção 1): a configuração '
                 'fiscal da matriz sem certificado nem dados (a mesma linha, campos da aula em branco), sem série, notas, transportadora '
                 'e cenário; as notas recebidas 2157 (Auto Peças Vale Forte, 05/11, R$ 1.984,00, com XML) e 884 (Depósito Irmãos '
                 'Siqueira, 06/11, R$ 2.100,00, três itens, só o resumo), que só aparecem depois que a aula liga as Notas Recebidas '
                 '(cap15). Gerado por rec/t16/t16_sementes.py inicio.'),
        '_remove': {'nfe_series': [{}], 'invoices': [{}], 'invoice_items': [{}], 'invoice_orders': [{}], 'nfe_events': [{}],
                    'nfe_inutilized_numbers': [{}], 'transportadoras': [{}], 'fiscal_scenarios': [{}], 'inbound_nfe': [{}]},
        '_patch': {'company_fiscal_config': [{'match': {'id': CFG}, 'set': VAZIO_CFG}]},
        'inbound_nfe': [recebida('valeforte', 81247, True), recebida('siqueira', 81302, False)],
    }


def assets():
    os.makedirs(ASSETS, exist_ok=True)
    xml, ch, total = nfe_xml('recomeco')
    open(os.path.join(ASSETS, XML_COOP), 'w', encoding='utf8').write(xml)
    # .pfx falso: 2 KB pseudoaleatórios fixos (o handler confere só o nome do arquivo, docs/08 T14)
    b = b''.join(hashlib.sha256(f'recicla-a1-{i}'.encode()).digest() for i in range(64))
    open(os.path.join(ASSETS, PFX), 'wb').write(b)
    print(f'assets: {XML_COOP} (chave {ch}, R$ {total:.2f}) e {PFX} ({len(b)} bytes)')


def _get(porta, caminho):
    k = json.load(open(os.path.join(MUNDO, 'mundo.json'), encoding='utf8'))['env']['anonKey']
    req = urllib.request.Request(f'http://127.0.0.1:{porta}/rest/v1/{caminho}', headers={'apikey': k, 'Authorization': f'Bearer {k}'})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode('utf8'))


def _post(porta, caminho, corpo):
    req = urllib.request.Request(f'http://127.0.0.1:{porta}{caminho}', data=json.dumps(corpo).encode(), method='POST',
                                 headers={'content-type': 'application/json'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


IGNORA = {'active_sessions', 'usage_events', 'user_sessions', 'audit_log', 'activity_logs'}


def captura(nn, porta):
    schema = json.load(open(os.path.join(MUNDO, 'schema.json'), encoding='utf8'))['tables']
    novas, patch = {}, {}
    for tab, info in sorted(schema.items()):
        cols = info.get('columns') or info
        if not isinstance(cols, dict) or 'id' not in cols or tab in IGNORA:
            continue
        if 'created_at' in cols:
            try:
                rows = _get(porta, f'{tab}?select=*&created_at=gte.{FAKE_NOW_Z}')
            except Exception:
                rows = []
            if rows:
                novas[tab] = rows
        if 'updated_at' in cols:
            try:
                rows = _get(porta, f'{tab}?select=*&updated_at=gte.{FAKE_NOW_Z}' + (f'&created_at=lt.{FAKE_NOW_Z}' if 'created_at' in cols else ''))
            except Exception:
                rows = []
            if rows:
                patch[tab] = [{'match': {'id': r['id']}, 'set': {k: v for k, v in r.items() if k not in ('id', 'created_at')}} for r in rows]
    _post(porta, '/__dev/reset', {})
    _post(porta, '/__dev/seed', {'files': ['t16/inicio']})
    for tab in list(novas):
        ids = ','.join(r['id'] for r in novas[tab])
        ja = {r['id'] for r in _get(porta, f'{tab}?select=id&id=in.({ids})')}
        novas[tab] = [r for r in novas[tab] if r['id'] not in ja]
        if not novas[tab]:
            del novas[tab]
    for tab, itens in list(patch.items()):
        novos = []
        for it in itens:
            antes = _get(porta, f"{tab}?select=*&id=eq.{it['match']['id']}")
            antes = antes[0] if antes else {}
            mud = {k: v for k, v in it['set'].items() if antes.get(k) != v}
            if mud:
                novos.append({'match': it['match'], 'set': mud})
        if novos:
            patch[tab] = novos
        else:
            del patch[tab]
    d = {'_doc': f'T16 · estado depois do cap{nn:02d} (cumulativo sobre t16/inicio), capturado do Supabase falso logo depois do ensaio '
                 f'do capítulo (o que o app gravou). Gerado por rec/t16/t16_sementes.py captura {nn}.'}
    d.update(novas)
    if patch:
        d['_patch'] = patch
    return d


if __name__ == '__main__':
    os.makedirs(SAIDA, exist_ok=True)
    if sys.argv[1:2] == ['assets']:
        assets()
        sys.exit(0)
    if sys.argv[1:2] == ['inicio']:
        nome, d = 'inicio', inicio()
    elif sys.argv[1:2] == ['captura']:
        nn = int(sys.argv[2])
        porta = int(sys.argv[sys.argv.index('--porta') + 1]) if '--porta' in sys.argv else 54316
        nome, d = f'apos-cap{nn:02d}', captura(nn, porta)
    else:
        sys.exit(__doc__)
    caminho = os.path.join(SAIDA, f'{nome}.json')
    json.dump(d, open(caminho, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    resumo = {k: len(v) for k, v in d.items() if isinstance(v, list)}
    if '_patch' in d:
        resumo['_patch'] = {k: len(v) for k, v in d['_patch'].items()}
    print(f'{os.path.relpath(caminho, TUT_HOME)}: {resumo}')
