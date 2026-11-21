#!/usr/bin/env python3
"""T26 · semente dos caps 15 e 16 (apos-cap14-dia): o apos-cap14 (rec/t26/aux/t26_cadeia.mjs) mais as cinco oportunidades que Rafael e
Juliana criaram durante o dia no "Sucata industrial" (10:00 a 17:00), como o plano manda (planejamento/ecoflix/T26/plano.md, "Semente do
cap12", hoje cap15). A Esquadrias Horizonte nasce em "Em contato": a automação "Agendar a visita" roda no INSERT (o banco faz isso) e cria a tarefa
dela para o dia útil seguinte, com o responsável do cartão; a semente traz essa tarefa, a execução e a linha do Histórico.
Uso: python3 -I rec/t26/aux/t26_dia.py   (lê e grava em rec/mundo/seeds-extra/t26/)"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SX = os.path.normpath(os.path.join(HERE, '..', '..', 'mundo', 'seeds-extra', 't26'))
base = json.load(open(os.path.join(SX, 'apos-cap14.json'), encoding='utf8'))

suc = next(p for p in base['crm_pipelines'] if p['name'] == 'Sucata industrial')
etapa = {s['name']: s for s in base['crm_stages'] if s['pipeline_id'] == suc['id']}
cid = suc['company_id']
regra = next(r for r in base['crm_automation_rules'] if r['name'] == 'Agendar a visita')
assert regra['trigger_stage_id'] == etapa['Em contato']['id'] and regra['enabled']

RAFAEL, JULIANA = '@id:user.rafael', '@id:user.juliana'
# título, etapa, valor, responsável, criado por, material (id, nome), quantidade, transporte, empresa, hora (BRT)
DIA = [
    ('Baterias da frota da Transportadora Caminho Firme', 'Proposta', 4650, JULIANA, JULIANA, ('@id:material.bateria', 'Bateria automotiva'), 1500,
     'Por conta do fornecedor', 'Transportadora Caminho Firme', '10:05'),
    ('Perfis de alumínio da Esquadrias Horizonte', 'Em contato', 17800, RAFAEL, RAFAEL, ('@id:material.al_perfil', 'Alumínio perfil'), 2000,
     'Transportadora', 'Esquadrias Horizonte', '11:20'),
    ('Cobre de manutenção da Elétrica Ponto Certo', 'Novo', 10800, None, JULIANA, ('@id:material.cobre_misto', 'Cobre misto'), 300,
     'A definir', 'Elétrica Ponto Certo', '13:40'),
    ('Ferro de demolição da Construtora Pilar', 'Ganho', 19000, RAFAEL, RAFAEL, ('@id:material.ferro_pesado', 'Ferro pesado'), 20000,
     'Frota própria', 'Construtora Pilar', '15:10'),
    ('Papelão do Mercado Bom Preço', 'Perdido', 1650, JULIANA, JULIANA, ('@id:material.papelao', 'Papelão'), 3000,
     'Por conta do fornecedor', 'Mercado Bom Preço', '16:55'),
]
NOTAS = {'Papelão do Mercado Bom Preço': 'Perdeu: o Mercado Bom Preço fechou com outro comprador, por preço.'}   # o motivo da perda vai nas observações (cap15)
utc = lambda hhmm, seg=0: f"2026-11-10T{int(hhmm[:2]) + 3:02d}:{hhmm[3:]}:{seg:02d}.000Z"

out = {k: list(v) if isinstance(v, list) else v for k, v in base.items()}
out['_doc'] = ('T26 · caps 15 e 16 (FAKE_NOW 17:30): apos-cap14 + as cinco oportunidades do dia (rec/t26/aux/t26_dia.py). Totais: 6 oportunidades, '
               'R$ 62.300,00; Ganhos R$ 19.000,00; Em negociação R$ 41.650,00; Em negociação + Rafael = R$ 26.200,00.')
for k, (titulo, et, valor, resp, autor, (mid, mnome), qtd, transp, empresa, hora) in enumerate(DIA):
    oid = f'@id:t26.dia.opp{k}'
    out['crm_opportunities'].append({
        'id': oid, 'company_id': cid, 'pipeline_id': suc['id'], 'stage_id': etapa[et]['id'], 'title': titulo, 'contact_name': None,
        'contact_email': None, 'contact_phone': None, 'value': valor, 'notes': NOTAS.get(titulo), 'position': 0, 'expected_close_date': None,
        'assigned_to': resp, 'created_by': autor, 'created_at': utc(hora), 'updated_at': utc(hora), 'customer_id': None, 'supplier_id': None,
        'company_name': empresa, 'contact_role': None, 'material_id': mid, 'material_name': mnome, 'estimated_quantity': qtd,
        'estimated_unit': 'Kg', 'transport_mode': transp, 'start_date': None, 'label_ids': [], 'checklists': [], 'probability': 50,
        'source': None, 'loss_reason': None,
    })
    if et == 'Em contato':   # "Ao entrar nesta etapa" no INSERT: Criar tarefa "Agendar visita na {CLIENTE}", 1 dia útil, responsável do cartão
        out['schedule_tasks'].append({
            'id': f'@id:t26.dia.tarefa{k}', 'company_id': cid, 'created_by': autor, 'assigned_to': resp, 'title': f'Agendar visita na {empresa}',
            'description': None, 'category': 'crm', 'scheduled_date': '2026-11-11', 'scheduled_time': None, 'status': 'pendente', 'priority': 'media',
            'crm_opportunity_id': oid, 'crm_automation_rule_id': regra['id'], 'crm_checklist_id': None, 'notify_on_day': True,
            'notify_push': False, 'notify_minutes_before': 0, 'created_at': utc(hora, 1), 'updated_at': utc(hora, 1),
        })
        out['crm_automation_executions'].append({
            'id': f'@id:t26.dia.exec{k}', 'company_id': cid, 'rule_id': regra['id'], 'opportunity_id': oid, 'event_key': f'stage:t26.dia.opp{k}',
            'status': 'completed', 'error_message': None, 'created_at': utc(hora, 1), 'executed_at': utc(hora, 1),
        })
        out['crm_opportunity_activities'].append({
            'id': f'@id:t26.dia.ativ{k}', 'company_id': cid, 'opportunity_id': oid, 'user_id': autor, 'kind': 'system', 'body': None,
            'metadata': {'event': 'automation_executed', 'rule_id': regra['id'], 'rule_name': regra['name']}, 'created_at': utc(hora, 1),
        })
json.dump(out, open(os.path.join(SX, 'apos-cap14-dia.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
abertas = [o for o in out['crm_opportunities'] if o['pipeline_id'] == suc['id']]
print(f"apos-cap14-dia: {len(abertas)} oportunidades no Sucata industrial, R$ {sum(o['value'] for o in abertas):,.2f}")
