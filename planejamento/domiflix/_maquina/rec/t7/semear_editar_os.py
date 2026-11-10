#!/usr/bin/env python3
"""T7 · cap14 "Editar OS": gera rec/fakebase/seeds-extra/t7/inicio-editar-os.json (estado de partida do capítulo).

A OS de bastidor: Pousada Sol Nascente, Manutenção Preventiva, Rafael Lima, quarta 08:00 a 09:00, Em Andamento (check-in 08:15),
com o checklist "Manutenção preventiva de split" SEM equipamento e 5 respostas Sim/Não (equipment_id nulo). O equipamento nasce na
gaveta "Editar OS" (criação rápida). Aplica-se por cima de BASE (cadeia.json "inicio"); não entra na cadeia apos-capNN (cap14 é remendo).
Não mexe na OS #16. Rodar: python3 -I rec/t7/semear_editar_os.py
"""
import json, os, uuid

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, '..', 'fakebase', 'seeds-extra', 't7', 'inicio-editar-os.json'))
NS = uuid.UUID('7a1e0014-0000-4000-8000-000000000014')
sid = lambda k: str(uuid.uuid5(NS, k))

COMPANY = '9c307966-79f1-567c-ac4d-d5fd3c1a2f40'
CRIADOR = 'd40f5787-1779-501f-900c-ddb2b90a36e5'      # Camila Duarte (gestora)
RAFAEL = '34c36c63-0890-5e89-8963-7c77b7996908'
POUSADA = 'a8e2168a-2060-4456-a804-ac69a2032a15'       # Pousada Sol Nascente
SERVICO = '49db63cb-1737-415d-b795-187297148790'       # Manutenção Preventiva
TEMPLATE = 'd5a900b6-960f-438e-973c-9844ececa223'      # Manutenção preventiva de split
PERGUNTAS = ['b7307997-1bf7-454d-93ba-e9f723fd17a9', 'fd97f6a6-25a2-4919-850b-28cb1b3860b6', '81e87273-1293-4307-8489-9725ab11cf49',
             '29dfbdcf-2dee-4813-84f7-ce04b05885d9', 'a0432b58-2d97-48fd-bf4d-4ad5d405265b']   # as 5 Sim/Não do checklist (T4)
OS = sid('os')
CRIADA = '2026-11-03T12:00:00.000Z'
CHECKIN = '2026-11-11T11:15:00.000Z'                   # 08:15 -03:00 (antes do FAKE_NOW 08:50)
ENDERECO = {'lat': -22.9035, 'lng': -43.1040, 'address': 'Rua da Praia - Icaraí - Niterói - RJ'}

os_row = {
    'id': OS, 'order_number': 23, 'public_short_code': 'sn7ed4tqs9kv', 'company_id': COMPANY, 'created_by': CRIADOR,
    'customer_id': POUSADA, 'equipment_id': None, 'form_template_id': None, 'technician_id': RAFAEL, 'team_id': None,
    'os_type': 'manutencao_corretiva', 'service_type_id': SERVICO, 'status': 'em_andamento', 'entry_type': 'os', 'origin': 'manual',
    'scheduled_date': '2026-11-11', 'scheduled_time': '08:00:00', 'duration_minutes': 60,
    'schedule_plan': [{'date': '2026-11-11', 'time': '08:00', 'duration_minutes': 60}],
    'description': 'Manutenção preventiva', 'notes': '', 'show_in_schedule': True, 'generate_nps_survey': True,
    'require_tech_signature': False, 'require_client_signature': False,
    'check_in_time': CHECKIN, 'check_in_by': RAFAEL, 'check_in_location': ENDERECO, 'started_at': CHECKIN,
    'created_at': CRIADA, 'updated_at': CHECKIN, 'labor_value': 0, 'total_value': 0, 'parts_value': 0,
}

def tl(evento, k, quando, endereco=None):
    return {'id': sid('tl' + k), 'user_id': RAFAEL, 'company_id': COMPANY, 'service_order_id': OS, 'lat': ENDERECO['lat'],
            'lng': ENDERECO['lng'], 'event_type': evento, 'created_at': quando, 'address': endereco}

seed = {
    '_comentario': 'T7 cap14 (Editar OS): OS de bastidor da Pousada Sol Nascente, checklist sem equipamento com 5 respostas. Gerado por rec/t7/semear_editar_os.py: não edite à mão.',
    'service_orders': [os_row],
    'service_order_assignees': [{'id': sid('as'), 'service_order_id': OS, 'user_id': RAFAEL, 'created_at': CRIADA}],
    'service_order_service_types': [{'id': sid('sst'), 'service_order_id': OS, 'service_type_id': SERVICO, 'company_id': COMPANY, 'position': 0, 'created_at': CRIADA}],
    'service_order_equipment': [{'id': sid('soe'), 'service_order_id': OS, 'equipment_id': None, 'form_template_id': TEMPLATE,
                                 'equipment_position': 0, 'checklist_position': 0, 'created_at': CRIADA}],
    'technician_locations': [tl('check_in', 'ci', CHECKIN, ENDERECO['address']), tl('tracking', 'tr', CHECKIN)],
    'form_responses': [
        {'id': sid(f'fr{i}'), 'service_order_id': OS, 'question_id': q, 'equipment_id': None, 'response_value': 'true',
         'response_photo_url': None, 'response_video_url': None, 'responded_at': f'2026-11-11T11:{20 + i}:00.000Z', 'responded_by': RAFAEL}
        for i, q in enumerate(PERGUNTAS)],
}
json.dump(seed, open(OUT, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print('ok', OUT)
