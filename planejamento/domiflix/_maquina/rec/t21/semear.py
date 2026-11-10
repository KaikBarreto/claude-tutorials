#!/usr/bin/env python3
"""T21 · gera o mundo de partida da Integração com WhatsApp (rec/fakebase/seeds-extra/t21/inicio.json + corte-dia13.json) e rec/t21/cadeia.json.

Estado de partida = fim do T22 (cadeia do T22 + `t22/apos-cap11`, só leitura) + `t21/inicio`:
  - nenhuma linha em `company_whatsapp_settings`, `whatsapp_connections` e `whatsapp_send_jobs` (o T1 só olhou a tela; tabelas vazias de propósito);
  - a Academia Ponto Forte SEM autorização (`whatsapp_notifications_enabled` false, opt-out carimbado); o Hotel Mirante do Mar segue autorizado.
`t21/corte-dia13` (capítulos 8 a 10, FAKE_NOW 13/11 15:00): a OS #34 do hotel atendida pelo Rafael Lima (a caminho 09:10, iniciada 09:42, concluída 11:05),
uma OS nova da Academia (#35) a caminho com o Lucas Ferreira às 15:00 e os quatro `whatsapp_send_jobs` do histórico. Datas LITERAIS (o backend pode estar em outro FAKE_NOW).
Rodar de qualquer pasta:  python3 -I rec/t21/semear.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
EXTRA = os.path.normpath(os.path.join(HERE, '..', 'fakebase', 'seeds-extra'))
FAKE_NOW = '2026-11-12T14:00:00-03:00'
EMP = '9c307966-79f1-567c-ac4d-d5fd3c1a2f40'
HOTEL = 'cbed8554-3919-5fa8-b9c6-5d13ef24cf37'
ACADEMIA = 'f9505970-93cd-5360-8c93-1e473d33952e'
OS34 = 'c62bf5ec-f3e5-57c6-be8b-e0556f64572a'
RAFAEL = '34c36c63-0890-5e89-8963-7c77b7996908'    # user_id (service_orders.technician_id)
LUCAS = '10b0daa2-5924-5a9c-9510-93101d7b1a07'
CAMILA = 'd40f5787-1779-501f-900c-ddb2b90a36e5'
EQ_ACADEMIA = 'a238a905-b0d9-57e8-8a40-0191dc9a340b'   # Cassete 36.000 BTUs - Sala de musculação
SERVICO = 'd84b0c8f-efc9-4934-8bb6-fc2bc4911f39'      # o mesmo da OS #7 da academia


def utc(dia, hhmm):
    """horário de Brasília (-03:00) -> ISO UTC literal"""
    h, m = map(int, hhmm.split(':'))
    d, mo, y = dia[8:10], dia[5:7], dia[0:4]
    from datetime import datetime, timedelta
    t = datetime(int(y), int(mo), int(d), h, m) + timedelta(hours=3)
    return t.strftime('%Y-%m-%dT%H:%M:00.000Z')


def inicio():
    return {
        '_comentario': 'T21 · fim do T22 + WhatsApp sem conexão nem configuração + Academia Ponto Forte sem autorização. Gerado por rec/t21/semear.py: não edite à mão.',
        'company_whatsapp_settings': [], 'whatsapp_connections': [], 'whatsapp_send_jobs': [],
        '_patch': {'customers': [{'match': {'id': ACADEMIA}, 'set': {'whatsapp_notifications_enabled': False, 'whatsapp_opt_in_at': None, 'whatsapp_opt_out_at': '2026-11-09T13:00:00.000Z'}}]},
    }


def job(n, evento, cliente, os_id, status, criado, enviado, erro=None, codigo=None):
    return {
        'id': f'@id:t21.job.{n}', 'company_id': EMP, 'connection_id': '@id:t21.conexao', 'customer_id': cliente, 'provider': 'evolution_qr',
        'event_key': evento, 'source_type': 'service_order', 'source_id': os_id, 'dedupe_key': f'{evento}:{os_id}', 'status': status, 'attempts': 0 if status == 'skipped' else 1,
        'defers': 0, 'last_error': erro, 'last_error_code': codigo, 'created_at': criado, 'updated_at': enviado or criado, 'sent_at': enviado,
        'next_attempt_at': criado, 'provider_message_id': None if status == 'skipped' else f'demo-{n}',
    }


def corte():
    d = '2026-11-13'
    os35 = {
        'id': '@id:t21.os.academia', 'company_id': EMP, 'entry_type': 'os', 'origin': 'manual', 'status': 'a_caminho', 'os_type': 'manutencao_preventiva',
        'customer_id': ACADEMIA, 'equipment_id': EQ_ACADEMIA, 'service_type_id': SERVICO, 'technician_id': LUCAS, 'created_by': CAMILA,
        'description': 'Higienização mensal do Cassete da sala de musculação', 'duration_minutes': 90, 'generate_nps_survey': True,
        'scheduled_date': d, 'scheduled_time': '15:00:00', 'schedule_plan': [{'date': d, 'time': '15:00', 'duration_minutes': 90}],
        'created_at': utc('2026-11-10', '09:00'), 'updated_at': utc(d, '15:00'), 'show_in_schedule': True, 'public_short_code': 'wa2academia1',
    }
    patch34 = {'status': 'concluida', 'technician_id': RAFAEL, 'scheduled_date': d, 'scheduled_time': '09:00:00', 'duration_minutes': 120,
               'schedule_plan': [{'date': d, 'time': '09:00', 'duration_minutes': 120}], 'started_at': utc(d, '09:42'), 'check_in_time': utc(d, '09:42'),
               'check_in_by': RAFAEL, 'check_out_time': utc(d, '11:05'), 'check_out_by': RAFAEL, 'completed_at': utc(d, '11:05'), 'updated_at': utc(d, '11:05'),
               'solution': 'Dreno desobstruído e bandeja limpa.'}
    jobs = [
        job(1, 'os.a_caminho', HOTEL, OS34, 'read', utc(d, '09:10'), utc(d, '09:10')),
        job(2, 'os.em_andamento', HOTEL, OS34, 'read', utc(d, '09:42'), utc(d, '09:42')),
        job(3, 'os.concluida', HOTEL, OS34, 'delivered', utc(d, '11:05'), utc(d, '11:05')),
        job(4, 'os.a_caminho', ACADEMIA, '@id:t21.os.academia', 'skipped', utc(d, '15:00'), None, 'O cliente não autorizou mensagens pelo WhatsApp.', 'customer_opt_out'),
    ]
    return {'_comentario': 'T21 · corte do dia 13/11 (caps 8 a 10): OS #34 atendida, OS #35 da academia a caminho, 4 avisos no histórico. Gerado por rec/t21/semear.py.',
            'service_orders': [os35], 'whatsapp_send_jobs': jobs, '_patch': {'service_orders': [{'match': {'id': OS34}, 'set': patch34}]}}


def main():
    os.makedirs(os.path.join(EXTRA, 't21'), exist_ok=True)
    for nome, dado in (('inicio', inicio()), ('corte-dia13', corte())):
        with open(os.path.join(EXTRA, 't21', nome + '.json'), 'w', encoding='utf8') as f:
            json.dump(dado, f, ensure_ascii=False, indent=1)
    t22 = json.load(open(os.path.join(HERE, '..', 't22', 'cadeia.json'), encoding='utf8'))
    cad = {'fake_now': FAKE_NOW, 'fake_now_dia13': '2026-11-13T15:00:00-03:00', 'inicio': list(t22['inicio']) + ['t22/apos-cap11', 't21/inicio'],
           'corte': 't21/corte-dia13', 'modo': 'real',
           'nota': 'mundo do T21 = fim do T22 (t22/apos-cap11, só leitura) + t21/inicio; apos-capNN do T21 são cumulativos sobre t21/inicio. Caps 8 a 10: apos-cap05 + corte-dia13 (= apos-cap07) com FAKE_NOW do dia 13.'}
    with open(os.path.join(HERE, 'cadeia.json'), 'w', encoding='utf8') as f:
        json.dump(cad, f, ensure_ascii=False, indent=1)
    print('t21/inicio.json, t21/corte-dia13.json e rec/t21/cadeia.json gerados.')


if __name__ == '__main__':
    main()
