#!/usr/bin/env python3
"""T16 · sementes novas da passada 1.60.10 (além das do t16_sementes.py; a Metalúrgica Pinhal e o cache da consulta de IE entram no
`inicio` de lá).

  python3 -I rec/t16/t16_sementes_160.py rejeitada
      escreve seeds-extra/t16/rejeitada-1252.json: a NF-e 1252 da Serra Fina (150 kg de Alumínio perfil a R$ 10,40 = R$ 1.560,00,
      JUNCAO_160) já enviada e RECUSADA pela SEFAZ (cStat 778, NCM 7602.00.99 inexistente no item), com os dois eventos do Histórico
      (envio e rejeição). Entra só na partida do capítulo da rejeição (SEMENTE do gerar.py); a captura do capítulo a leva adiante
      (created_at >= FAKE_NOW). O modelo das linhas é a 1249 gravada pelo app no apos-cap09 (mesmas colunas).
Nada de dado real: chave fictícia com dígito válido (mesma conta do lib/nfe.mjs)."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.normpath(os.path.join(HERE, '..', 'mundo', 'seeds-extra', 't16'))
Z = '2026-11-10T11:30:00.000Z'          # 08:30 em Brasília (FAKE_NOW)
MSG = 'Rejeição 778: Informado NCM inexistente [nItem:1]'


def dv11(base):
    soma, peso = 0, 2
    for ch in reversed(base):
        soma += int(ch) * peso
        peso = 2 if peso == 9 else peso + 1
    r = soma % 11
    return '0' if r < 2 else str(11 - r)


def rejeitada():
    base = json.load(open(os.path.join(SAIDA, 'apos-cap09.json'), encoding='utf8'))
    nota = dict(next(n for n in base['invoices'] if n['invoice_number'] == 1249))
    item = dict(next(i for i in base['invoice_items'] if i['invoice_id'] == nota['id']))
    chave = '3526114731850600010755001000001252' + '1' + '52771252'
    chave += dv11(chave)
    nid, iid = '@id:t16.nota1252', '@id:t16.nota1252.item1'
    nota.update({
        'id': nid, 'invoice_number': 1252, 'status': 'rejeitada', 'total_products': 1560, 'total_amount': 1560,
        'created_at': Z, 'updated_at': Z, 'issue_date': Z, 'authorized_at': None, 'nfe_key': None, 'nfe_protocol': None,
        'xml_content': None, 'plugnotas_id': 'pn-001252', 'error_message': MSG,
        'fiscal_status_confirmation': {'status': 'rejected', 'key': chave, 'environment': '1', 'cstat': '778', 'source': 'sefaz_xml',
                                       'observed_at': Z},
    })
    item.update({'id': iid, 'invoice_id': nid, 'ncm': '76020099', 'quantity': 150, 'total_price': 1560, 'created_at': Z})
    emp = nota['company_id']
    ev = [
        {'id': '@id:t16.nota1252.ev1', 'company_id': emp, 'invoice_id': nid, 'event_type': 'emissao', 'status': 'enviado',
         'message': 'Nota enviada para processamento na SEFAZ', 'payload': None, 'plugnotas_response': None, 'created_at': Z},
        {'id': '@id:t16.nota1252.ev2', 'company_id': emp, 'invoice_id': nid, 'event_type': 'rejeicao', 'status': 'error',
         'message': MSG, 'payload': None, 'plugnotas_response': None, 'created_at': '2026-11-10T11:30:00.500Z'},
    ]
    return {'_doc': 'T16 (1.60.10) · a NF-e 1252 da Serra Fina já recusada pela SEFAZ (778, NCM 7602.00.99 no item), com o Histórico. '
                    'Partida do capítulo da rejeição. Gerado por rec/t16/t16_sementes_160.py rejeitada.',
            'invoices': [nota], 'invoice_items': [item], 'nfe_events': ev}


if __name__ == '__main__':
    if sys.argv[1:2] != ['rejeitada']:
        sys.exit(__doc__)
    d = rejeitada()
    p = os.path.join(SAIDA, 'rejeitada-1252.json')
    json.dump(d, open(p, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print(p, {k: len(v) for k, v in d.items() if isinstance(v, list)})
