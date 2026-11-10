#!/usr/bin/env python3
"""T7 · gera seeds-extra/t7/pesquisa-oculta.json e pesquisa-visivel.json (cap12): o link do cliente só abre a pesquisa "Como foi seu
atendimento?" quando existe a linha de avaliação da OS (survey_enabled = EXISTS no get_public_os, igual ao banco real). Para a pesquisa
abrir "sozinha" no meio da fala, a linha de avaliação da #16 é posta de lado (service_order_id aponta para uma OS que não existe) antes
do capítulo e devolvida no instante certo. Mesmo formato dos outros seeds (`_patch`). Uso: python3 -I rec/t7/semear_pesquisa.py"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
OS16 = json.load(open(os.path.join(HERE, 'cadeia.json'), encoding='utf8'))['os16']
VAZIA = '00000000-0000-4000-8000-000000000016'
DEST = os.path.join(HERE, '..', 'fakebase', 'seeds-extra', 't7')


def grava(nome, de, para, nota):
    d = {'_comentario': nota, '_patch': {'service_ratings': [{'match': {'service_order_id': de}, 'set': {'service_order_id': para}}]}}
    with open(os.path.join(DEST, nome + '.json'), 'w', encoding='utf8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    print('gravado', nome)


grava('pesquisa-oculta', OS16, VAZIA, 'T7 · cap12: esconde a avaliação da OS #16 (a pesquisa do link do cliente fica fechada). Gerado por rec/t7/semear_pesquisa.py.')
grava('pesquisa-visivel', VAZIA, OS16, 'T7 · cap12: devolve a avaliação da OS #16 (a pesquisa do link do cliente abre). Gerado por rec/t7/semear_pesquisa.py.')
