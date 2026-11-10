#!/usr/bin/env python3
"""T10 · gera o mundo de partida da aula (rec/fakebase/seeds-extra/t10/inicio.json) e rec/t10/cadeia.json.

Estado de partida = fim do T9 (roteiro.md, "Estado inicial"): a cadeia do T9 (`rec/t9/cadeia.json`, sem a OS #17 do T5) + `t9/apos-cap16`
(orçamentos #1 a #9, o #9 Convertido, o #2 Aprovado, OS #17 Agendada) + `t2/apos-cap10` (Tatiane Ribeiro, os cargos e as permissões; a cadeia do T9
não os traz, e o roteiro do T10 usa a Tatiane como vendedora do hotel).
Em cima disso, `t10/inicio` (este arquivo) faz o bastidor do T10:
 - CRM VAZIO de propósito (nenhum funil, etapa, oportunidade, etiqueta, modelo de checklist, webhook nem projeto): as tabelas entram como listas
   vazias para a tela abrir no cartão "Configure seu funil" e para /__dev/unknowns ficar vazio (TABELA_SEM_SEED);
 - G1 (IMPACTO_1.38.19.md): `_patch` na trilha `tutoriais-do-sistema` com `is_onboarding: false` (sem tela escura de introdução nem faixa de lembrete).
   Atualiza a linha que já existe (id da base); não cria linha nova.
Os ids vêm SEMPRE lidos da cadeia. Rodar de qualquer pasta:  python3 -I rec/t10/semear.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
EXTRA = os.path.normpath(os.path.join(HERE, '..', 'fakebase', 'seeds-extra'))
T9 = json.load(open(os.path.join(HERE, '..', 't9', 'cadeia.json'), encoding='utf8'))
FAKE_NOW = '2026-11-03T09:00:00-03:00'   # terça-feira; o mesmo no backend falso e no robô (roteiro.md)
TRILHA = 'c0000000-0000-4000-8000-000000000001'   # domiflix_learning_paths.id da base (slug tutoriais-do-sistema)

# tabelas do CRM/Projetos que o T10 lê ou grava: vazias na partida
VAZIAS = ['leads', 'crm_stages', 'crm_pipelines', 'lead_assignees', 'lead_interactions', 'crm_labels', 'crm_checklist_templates',
          'crm_pipeline_access', 'crm_webhooks', 'projects']
EXTRAS_VAZIAS = []   # preenchido com o que o /__dev/unknowns acusar na exploração

INICIO = ['t2/apos-cap10'] + [x for x in T9['inicio']] + ['t9/apos-cap16']


def main():
    d = {'_comentario': 'T10 · estado de partida = fim do T9 (cadeia do T9 + t9/apos-cap16 + t2/apos-cap10 para a Tatiane) com o CRM e Projetos VAZIOS. '
                        'Gerado por rec/t10/semear.py: não edite à mão.'}
    for t in VAZIAS + EXTRAS_VAZIAS:
        d[t] = []
    d['_patch'] = {'domiflix_learning_paths': [{'match': {'id': TRILHA}, 'set': {'is_onboarding': False}}],
                   # a origem "Site" criada no T3 ficou com is_active nulo na semente; o app (e o hook customer_origins) grava true. Sem isso o seletor
                   # "Origem padrão" do webhook (só origens ativas) não lista o Site.
                   'customer_origins': [{'match': {'name': 'Site'}, 'set': {'is_active': True}}]}
    os.makedirs(os.path.join(EXTRA, 't10'), exist_ok=True)
    with open(os.path.join(EXTRA, 't10', 'inicio.json'), 'w', encoding='utf8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    cad = {'fake_now': FAKE_NOW, 'inicio': INICIO + ['t10/inicio'], 'base': INICIO,
           'nota': 'cadeia do capítulo NN = inicio + t10/apos-capNN do último capítulo anterior que mexeu no banco (SEMENTE em rec/t10/gerar.py)'}
    with open(os.path.join(HERE, 'cadeia.json'), 'w', encoding='utf8') as f:
        json.dump(cad, f, ensure_ascii=False, indent=1)
    print('t10/inicio.json + cadeia.json:', ' + '.join(cad['inicio']))


if __name__ == '__main__':
    main()
