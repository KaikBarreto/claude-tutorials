#!/usr/bin/env python3
"""T17 · gera o mundo de partida de "Dashboard, relatórios e exportações" (rec/fakebase/seeds-extra/t17/inicio.json) e rec/t17/cadeia.json.

Estado de partida = fim do T14 (cadeia do T14 + `t14/apos-cap12`, só leitura) + `t17/inicio`. A aula só lê e filtra: nenhum capítulo grava no banco.
`t17/inicio` (bastidor, FAKE_NOW 13/11/2026 16:30, sexta):
  - a OS da Academia (#35, que o T21 deixou "A caminho" às 15:00) CONCLUÍDA: check-in 15:05, check-out 16:10 (entra em "Desempenho da Equipe");
  - nenhuma OS do dia 13 aberta às 16:30 (P2: o Dashboard lê data sem hora como o dia anterior e mostraria "Atrasada 0 dias"): as OS #9, #10 e #11,
    que as sementes antigas deixam abertas "hoje", são concluídas durante o dia;
  - nenhum lançamento no primeiro dia de "Mês passado" (01/10) nem no de "Este mês" (01/11): P2 descarta o primeiro dia do período no "Fluxo de Caixa"
    (os dois lançamentos de 01/10 vão para 02/10);
  - nenhuma posição em `technician_locations` nas últimas 2 h (já é assim: a última é das 08:59);
  - o ponto da Tatiane (T15 deixou a jornada de 11/11 "Em andamento"): a de 11/11 encerra às 18:05 e entra a de 12/11 (08:55 às 17:50), duas jornadas
    completas no Histórico (a de hoje não existe: ela ainda não bateu o ponto).
Datas LITERAIS (o backend pode estar em outro FAKE_NOW). Rodar de qualquer pasta:  python3 -I rec/t17/semear.py
"""
import json
import os
from datetime import datetime, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
EXTRA = os.path.normpath(os.path.join(HERE, '..', 'fakebase', 'seeds-extra'))
FAKE_NOW = '2026-11-13T16:30:00-03:00'
LUCAS = '10b0daa2-5924-5a9c-9510-93101d7b1a07'
EMP = '9c307966-79f1-567c-ac4d-d5fd3c1a2f40'
TATIANE = 'ccb84cb1-aa84-4b68-bba3-7bc7d8724107'


def utc(dia, hhmm):
    h, m = map(int, hhmm.split(':'))
    t = datetime(int(dia[0:4]), int(dia[5:7]), int(dia[8:10]), h, m) + timedelta(hours=3)
    return t.strftime('%Y-%m-%dT%H:%M:00.000Z')


def inicio(ft_out):
    d = '2026-11-13'
    def concl(chave, valor, ent, sai, tecnico=None, extra=None):
        s = {'status': 'concluida', 'started_at': utc(d, ent), 'check_in_time': utc(d, ent), 'check_out_time': utc(d, sai), 'completed_at': utc(d, sai), 'updated_at': utc(d, sai)}
        if tecnico:
            s['check_in_by'] = tecnico
            s['check_out_by'] = tecnico
        s.update(extra or {})
        return {'match': {chave: valor}, 'set': s}
    patch_os = [
        concl('public_short_code', 'wa2academia1', '15:05', '16:10', LUCAS, {'solution': 'Higienização concluída e filtros limpos.'}),
        concl('order_number', 9, '08:31', '10:35'),
        concl('order_number', 10, '09:30', '11:05'),
        concl('order_number', 11, '14:05', '15:25'),
    ]
    return {
        '_comentario': 'T17 · fim do T14 + dia 13 encerrado (nenhuma OS aberta hoje) + OS da Academia concluída às 16:10 + nenhum lançamento em 01/10. Gerado por rec/t17/semear.py: não edite à mão.',
        # tabelas que a aula consulta e que ficam vazias de propósito (sem isto entram no /__dev/unknowns): Inventários (T8 não criou contagem) e Materiais das OS (Exportar meus dados)
        'inventory_counts': [], 'service_materials': [],
        'time_records': [
            {'id': '@id:t17.ponto.saida11', 'company_id': EMP, 'employee_id': TATIANE, 'type': 'clock_out', 'recorded_at': utc('2026-11-11', '18:05'), 'date': '2026-11-11', 'is_valid': True,
             'latitude': -22.9024, 'longitude': -43.11094, 'address': 'Rua Moreira César - Icaraí - Niterói', 'photo_url': None, 'source': 'link_publico', 'notes': None, 'face_match': False,
             'created_at': utc('2026-11-11', '18:05')},
            {'id': '@id:t17.ponto.entrada12', 'company_id': EMP, 'employee_id': TATIANE, 'type': 'clock_in', 'recorded_at': utc('2026-11-12', '08:55'), 'date': '2026-11-12', 'is_valid': True,
             'latitude': -22.9024, 'longitude': -43.11094, 'address': 'Rua Moreira César - Icaraí - Niterói', 'photo_url': None, 'source': 'link_publico', 'notes': None, 'face_match': False,
             'created_at': utc('2026-11-12', '08:55')},
            {'id': '@id:t17.ponto.saida12', 'company_id': EMP, 'employee_id': TATIANE, 'type': 'clock_out', 'recorded_at': utc('2026-11-12', '17:50'), 'date': '2026-11-12', 'is_valid': True,
             'latitude': -22.9024, 'longitude': -43.11094, 'address': 'Rua Moreira César - Icaraí - Niterói', 'photo_url': None, 'source': 'link_publico', 'notes': None, 'face_match': False,
             'created_at': utc('2026-11-12', '17:50')},
        ],
        'time_sheets': [
            {'id': '@id:t17.folha12', 'company_id': EMP, 'employee_id': TATIANE, 'date': '2026-11-12', 'first_clock_in': utc('2026-11-12', '08:55'), 'last_clock_out': utc('2026-11-12', '17:50'),
             'total_worked_min': 475, 'total_break_min': 60, 'expected_min': 480, 'balance_min': -5, 'status': 'complete', 'created_at': utc('2026-11-12', '17:50'), 'justification': None, 'justified_by': None},
        ],
        '_patch': {'service_orders': patch_os, 'financial_transactions': ft_out,
                   'time_sheets': [{'match': {'id': 'c2ed3a26-d84b-480f-b16e-948fc2083e3f'}, 'set': {'last_clock_out': utc('2026-11-11', '18:05'), 'total_worked_min': 483, 'total_break_min': 60, 'balance_min': 3, 'status': 'complete'}}]},
    }


# os dois lançamentos da base gerada em 01/10 (uma entrada de 1.900,00 e uma saída de 1.610,00)
LANC_0110 = ['e4e4a165-66d4-5608-8a3f-f46ac46a995a', '3dd83ae3-3cda-57d7-9aa4-bc0284afbbe5']


def main():
    mover = [{'match': {'id': i}, 'set': {'transaction_date': '2026-10-02', 'paid_date': '2026-10-02'}} for i in LANC_0110]
    os.makedirs(os.path.join(EXTRA, 't17'), exist_ok=True)
    with open(os.path.join(EXTRA, 't17', 'inicio.json'), 'w', encoding='utf8') as f:
        json.dump(inicio(mover), f, ensure_ascii=False, indent=1)
    t14 = json.load(open(os.path.join(HERE, '..', 't14', 'cadeia.json'), encoding='utf8'))
    cad = {'fake_now': FAKE_NOW, 'inicio': list(t14['inicio']) + ['t14/apos-cap12', 't17/inicio'], 'modo': 'real',
           'nota': 'mundo do T17 = fim do T14 (t14/apos-cap12, só leitura) + t17/inicio. Nenhum capítulo grava: todos partem do mesmo `inicio`. FAKE_NOW 13/11 16:30 (sexta).'}
    with open(os.path.join(HERE, 'cadeia.json'), 'w', encoding='utf8') as f:
        json.dump(cad, f, ensure_ascii=False, indent=1)
    print(f't17/inicio.json ({len(mover)} lançamentos movidos) e rec/t17/cadeia.json gerados.')


if __name__ == '__main__':
    main()
