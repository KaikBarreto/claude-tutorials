#!/usr/bin/env python3
"""T03 · sementes da Margem automática (cap07 a cap10; 1.60.18). Escreve em rec/mundo/seeds-extra/t03/:
  margem-material.json  principal com a margem LIGADA, alcance "Por material", cada material com a margem que os preços de hoje já têm (é o
                        que "Por material > Aplicar" grava: nenhum preço muda). Entrada do cap10 (calculadora no cadastro).
  margem-fora.json      o mesmo, mas a venda do Alumínio latinha foi mexida por fora (planilha): 7,80 em vez de 7,40 -> "fora da margem".
                        Entrada do cap09 (resumo). Só nesses capítulos; o mundo seguinte volta ao apos-cap06.
Preços = mundo base + o cobre reajustado do cap06 (apos-cap06) + o radiador (código 70, 21,00 / 24,50). Uso: python3 -I rec/t03/t03_sementes_margem.py"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, '..', 'mundo', 'seeds-extra', 't03'))
base = json.load(open(os.path.join(HERE, '..', 'mundo', 'seeds', '02-cadastros.json')))['materials']
preco = {m['id']: (m['purchase_price'], m['sale_price']) for m in base}
preco['@id:material.cobre_mel'] = (42.5, 47.9)
preco['@id:material.cobre_misto'] = (36.0, 41.5)
preco['@id:material.fio_cobre'] = (18.0, 22.0)
preco['@id:material.radiador'] = (21.0, 24.5)
ordem = [m['id'] for m in base] + ['@id:material.radiador']
PRINCIPAL = '@id:tabela.padrao'


def semente(fora):
    linhas = []
    for mid in ordem:
        c, v = preco[mid]
        linhas.append({'price_table_id': PRINCIPAL, 'material_id': mid, 'margin_type': 'percentage',
                       'margin_amount': round((v / c - 1) * 100, 6), 'created_at': '2026-11-10T11:30:00.000Z', 'updated_at': '2026-11-10T11:30:00.000Z'})
    d = {'_doc': 'T03 · Margem automática da Principal ligada, por material (' + ('com o Alumínio latinha fora da margem' if fora else 'preços batendo com a margem') +
         '). Gerado por rec/t03/t03_sementes_margem.py.',
         '_patch': {'price_tables': [{'match': {'id': PRINCIPAL}, 'set': {'auto_margin_enabled': True, 'auto_margin_scope': 'material',
                                                                          'auto_margin_type': None, 'auto_margin_amount': None}}]},
         'price_table_material_margins': linhas}
    if fora:
        d['_patch']['materials'] = [{'match': {'id': '@id:material.al_latinha'}, 'set': {'sale_price': 7.8}}]
        d['_patch']['price_table_items'] = [{'match': {'id': '@id:pti.padrao.al_latinha'}, 'set': {'sale_price': 7.8}}]
    return d


for nome, fora in (('margem-material', False), ('margem-fora', True)):
    with open(os.path.join(OUT, nome + '.json'), 'w', encoding='utf8') as f:
        json.dump(semente(fora), f, ensure_ascii=False, indent=1)
    print('escrito', nome)
