#!/usr/bin/env python3
"""T14 · gera o mundo de partida das Notas Fiscais (rec/fakebase/seeds-extra/t14/inicio.json), o corte do capítulo 12
(seeds-extra/t14/corte-cap12.json) e rec/t14/cadeia.json.

Estado de partida = fim do T21 (cadeia do T21 + a semente final dele, só leitura) + `t14/inicio`:
  - `company_fiscal_settings` com UMA linha "em branco" e `fiscal_ambiente = 'homologacao'` (decisão do PRODUCAO.md: a aula
    grava em Homologação; sem linha o app abre em Produção, o padrão da 1.38.21+). Sem IM, sem município, sem certificado,
    recebimento de NF-e desligado: a tela continua em "Configure seus dados fiscais";
  - `companies.nfse_tier = 1` (DEFAULT do banco; a base traz 0) e o catálogo `nfse_tiers` da migration;
  - a "Receita" do mundo fictício (`fake_sefaz_dfe`, tabela só do backend falso): a NF-e nº 4512 da Cobre Sul Suprimentos
    Ltda (R$ 1.180,00, emitida em 09/11/2026), primeiro o resumo (resNFe) e, depois da ciência, a nota completa (procNFe,
    com uma duplicata vencendo em 24/11/2026).
`t14/corte-cap12` (aplicada pelo robô no meio do capítulo 12, depois de "Enviar manifestação"): o worker registrou a ciência
na Receita (16:23); a nota completa chega no "Sincronizar" seguinte, pelo dfe-sync falso (fila `fake_sefaz_dfe`).
Relógio: caps 0 a 11 em 13/11 15:10; caps 12 e 13 em 13/11 16:20 (a Receita só aceita uma consulta de NF-e por CNPJ a cada
65 min: a do cap11 é às 15:10, a próxima pode às 16:15), antes do T17 (16:30).
Datas LITERAIS (o backend pode estar em outro FAKE_NOW).

Uso:  python3 -I rec/t14/semear.py [semente-final-do-T21 ...]
      (sem argumento: base PROVISÓRIA = cadeia do T21 + t21/corte-dia13, até o T21 ficar pronto)
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EXTRA = os.path.normpath(os.path.join(HERE, '..', 'fakebase', 'seeds-extra'))
FAKE_NOW = '2026-11-13T15:10:00-03:00'
FAKE_NOW_CAP12 = '2026-11-13T16:20:00-03:00'   # caps 12 e 13 (depois da janela de 65 min da Receita)
EMP = '9c307966-79f1-567c-ac4d-d5fd3c1a2f40'
CNPJ_GLACIAL = '91520340000107'
CNPJ_COBRE = '91345603000180'
NSU_RES = '000000000000101'
NSU_PROC = '000000000000102'


def dv_mod11(base):
    soma, peso = 0, 2
    for ch in reversed(base):
        soma += int(ch) * peso
        peso = 2 if peso == 9 else peso + 1
    r = soma % 11
    return 0 if r < 2 else 11 - r


# chave da NF-e (44 dígitos): UF 33 (RJ) + AAMM 2611 + CNPJ do emitente + modelo 55 + série 001 + nº 000004512 + tpEmis 1 + cNF + DV
_base = '33' + '2611' + CNPJ_COBRE + '55' + '001' + '000004512' + '1' + '40451226'
CHAVE = _base + str(dv_mod11(_base))
assert len(CHAVE) == 44

ITENS = [  # (código, descrição, NCM, qtd, unitário)
    ('TC14', 'Tubo de cobre 1/4 pol, rolo 15 m', '74111010', 2, 290.00),
    ('TC38', 'Tubo de cobre 3/8 pol, rolo 15 m', '74111010', 1, 420.00),
    ('ESP12', 'Isolamento térmico elastomérico 1/2 pol, barra 2 m', '40169990', 6, 30.00),
]
TOTAL = round(sum(q * u for _, _, _, q, u in ITENS), 2)
assert abs(TOTAL - 1180.00) < 0.001


def xml_proc():
    det = ''.join(
        f'<det nItem="{i}"><prod><cProd>{c}</cProd><cEAN>SEM GTIN</cEAN><xProd>{d}</xProd><NCM>{ncm}</NCM><CFOP>5102</CFOP><uCom>UN</uCom>'
        f'<qCom>{q:.4f}</qCom><vUnCom>{u:.2f}</vUnCom><vProd>{q * u:.2f}</vProd></prod></det>'
        for i, (c, d, ncm, q, u) in enumerate(ITENS, 1))
    return ('<?xml version="1.0" encoding="UTF-8"?>'
            '<nfeProc versao="4.00" xmlns="http://www.portalfiscal.inf.br/nfe"><NFe><infNFe Id="NFe' + CHAVE + '" versao="4.00">'
            '<ide><cUF>33</cUF><natOp>Venda de mercadoria</natOp><mod>55</mod><serie>1</serie><nNF>4512</nNF>'
            '<dhEmi>2026-11-09T14:20:00-03:00</dhEmi><tpNF>1</tpNF><finNFe>1</finNFe></ide>'
            '<emit><CNPJ>' + CNPJ_COBRE + '</CNPJ><xNome>Cobre Sul Suprimentos Ltda</xNome><enderEmit><xLgr>Avenida Brasil</xLgr><nro>12000</nro>'
            '<xBairro>Penha</xBairro><xMun>Rio de Janeiro</xMun><UF>RJ</UF></enderEmit></emit>'
            '<dest><CNPJ>' + CNPJ_GLACIAL + '</CNPJ><xNome>Glacial Cold Brasil</xNome><enderDest><xLgr>Rua Moreira César</xLgr><nro>200</nro>'
            '<xBairro>Icaraí</xBairro><xMun>Niterói</xMun><UF>RJ</UF></enderDest></dest>'
            + det +
            f'<total><ICMSTot><vProd>{TOTAL:.2f}</vProd><vNF>{TOTAL:.2f}</vNF></ICMSTot></total>'
            f'<cobr><fat><nFat>4512</nFat><vOrig>{TOTAL:.2f}</vOrig><vLiq>{TOTAL:.2f}</vLiq></fat>'
            f'<dup><nDup>001</nDup><dVenc>2026-11-24</dVenc><vDup>{TOTAL:.2f}</vDup></dup></cobr>'
            f'<pag><detPag><tPag>15</tPag><vPag>{TOTAL:.2f}</vPag></detPag></pag>'
            '</infNFe></NFe><protNFe versao="4.00"><infProt><chNFe>' + CHAVE + '</chNFe><dhRecbto>2026-11-09T14:20:31-03:00</dhRecbto>'
            '<nProt>333260000045121</nProt><cStat>100</cStat><xMotivo>Autorizado o uso da NF-e</xMotivo></infProt></protNFe></nfeProc>')


NOTA_RESUMO = {
    'chave': CHAVE, 'numero': 4512, 'serie': 1, 'emitente_cnpj': CNPJ_COBRE, 'emitente_nome': 'Cobre Sul Suprimentos Ltda',
    'valor': TOTAL, 'data_emissao': '2026-11-09T17:20:00.000Z', 'natureza': None, 'cfop_principal': None, 'fin_nfe': None,
    'situacao_sefaz': 'autorizada', 'resumo': True, 'xml_content': None,
}
NOTA_COMPLETA = {**NOTA_RESUMO, 'natureza': 'Venda de mercadoria', 'cfop_principal': '5102', 'fin_nfe': 1, 'resumo': False, 'xml_content': xml_proc()}


def inicio():
    return {
        '_comentario': 'T14 · fim do T21 + configuração fiscal em branco (Homologação) + nível 1 da cota + a NF-e da Cobre Sul na "Receita". '
                       'Gerado por rec/t14/semear.py: não edite à mão.',
        'company_fiscal_settings': [{
            'id': '@id:t14.fiscal', 'company_id': EMP, 'fiscal_ambiente': 'homologacao', 'regime_tributario': None, 'reg_ap_trib_sn': '1',
            'inscricao_municipal': None, 'inscricao_estadual': None, 'municipio_ibge': None, 'pode_emitir': False, 'percentual_trib_sn': None,
            'certificado_ref': None, 'certificate_expires_at': None, 'dfe_nfe_ativo': False, 'dfe_nfse_ativo': False, 'serie_dps': '1',
            'ultimo_numero_dps': 0, 'provedor': 'sefin', 'created_at': '2026-11-13T18:00:00.000Z', 'updated_at': '2026-11-13T18:00:00.000Z',
        }],
        'nfse_tiers': [
            {'tier': 1, 'name': 'Nível 1', 'monthly_limit': 200, 'price': 100},
            {'tier': 2, 'name': 'Nível 2', 'monthly_limit': 500, 'price': 200},
            {'tier': 3, 'name': 'Nível 3', 'monthly_limit': 1000, 'price': 300},
            {'tier': 4, 'name': 'Nível 4 (Ilimitado)', 'monthly_limit': None, 'price': 400},
        ],
        'nfse_emissions': [], 'nfse_events': [], 'fiscal_certificate_audit': [], 'inbound_nfe': [], 'inbound_nfse': [], 'dfe_sync_state': [],
        'nfse_auto_jobs': [],
        'fake_sefaz_dfe': [
            {'id': '@id:t14.sefaz.res4512', 'company_id': EMP, 'tipo': 'nfe', 'nsu': NSU_RES, 'schema': 'resNFe', 'nota': NOTA_RESUMO},
            {'id': '@id:t14.sefaz.proc4512', 'company_id': EMP, 'tipo': 'nfe', 'nsu': NSU_PROC, 'schema': 'procNFe', 'requer_ciencia': True, 'nota': NOTA_COMPLETA},
        ],
        '_patch': {'companies': [{'match': {'id': EMP}, 'set': {'nfse_tier': 1}}]},
    }


def corte_cap12():
    ciencia = '2026-11-13T19:23:00.000Z'   # 16:23 em Brasília: o worker (cron) transmitiu a ciência à Receita
    return {
        '_comentario': 'T14 · corte do capítulo 12 (FAKE_NOW 16:20): o worker da fila de manifestação registrou a ciência na Receita. '
                       'Aplicada pelo robô (POST /__dev/seed) depois de "Enviar manifestação", com o relógio do navegador 4 min à frente; '
                       'a nota completa chega no "Sincronizar" seguinte (a trava de 65 min da consulta das 15:10 já passou). Gerado por rec/t14/semear.py.',
        'fiscal_certificate_audit': [
            {'id': '@id:t14.audit.manifestar', 'company_id': EMP, 'operacao': 'decifra', 'contexto': f'dfe_manifestar:{CHAVE}',
             'origem': 'edge:dfe-manifestar-worker', 'created_at': ciencia},
        ],
        '_patch': {
            'inbound_nfe': [{'match': {'chave': CHAVE}, 'set': {
                'manifestacao': 'ciencia', 'manifestacao_data': ciencia, 'manifestacao_pendente': None, 'manifestacao_pendente_em': None,
                'manifestacao_erro': None, 'updated_at': ciencia}}],
            'dfe_manifestacao_jobs': [{'match': {'chave': CHAVE}, 'set': {'status': 'concluida', 'tentativas': 1, 'updated_at': ciencia}}],
        },
    }


def main():
    final_t21 = sys.argv[1:]
    os.makedirs(os.path.join(EXTRA, 't14'), exist_ok=True)
    for nome, dado in (('inicio', inicio()), ('corte-cap12', corte_cap12())):
        with open(os.path.join(EXTRA, 't14', nome + '.json'), 'w', encoding='utf8') as f:
            json.dump(dado, f, ensure_ascii=False, indent=1)
    t21 = json.load(open(os.path.join(HERE, '..', 't21', 'cadeia.json'), encoding='utf8'))
    provisoria = not final_t21
    base_t21 = list(t21['inicio']) + (final_t21 if final_t21 else [t21['corte']])
    cad = {
        'fake_now': FAKE_NOW,
        'fake_now_cap12': FAKE_NOW_CAP12,
        'inicio': base_t21 + ['t14/inicio'],
        't21_final': final_t21 or None,
        'corte_cap12': 't14/corte-cap12',
        'chave_nfe_cobre_sul': CHAVE,
        'modo': 'provisoria' if provisoria else 'real',
        'nota': ('mundo do T14 = fim do T21 (' + ('PROVISÓRIO: cadeia do T21 + t21/corte-dia13' if provisoria else ' + '.join(final_t21)) +
                 ', só leitura) + t14/inicio; apos-capNN do T14 são cumulativos sobre t14/inicio. FAKE_NOW 13/11 15:10 (não 15:30): '
                 'a Receita só aceita uma consulta de NF-e por CNPJ a cada 65 min, então os caps 12 e 13 rodam às 16:20 '
                 '(a nota completa chega no Sincronizar do cap12), antes do T17 (16:30).'),
    }
    with open(os.path.join(HERE, 'cadeia.json'), 'w', encoding='utf8') as f:
        json.dump(cad, f, ensure_ascii=False, indent=1)
    print(f't14/inicio.json, t14/corte-cap12.json e rec/t14/cadeia.json gerados ({cad["modo"]}; chave da NF-e {CHAVE}).')


if __name__ == '__main__':
    main()
