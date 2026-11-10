#!/usr/bin/env python3
"""T5 · gera as sementes do mundo de partida da aula (rec/fakebase/seeds-extra/t5/inicio.json).

Estado de partida = fim do T4 (t4/apos-cap14) por cima do T3 e da identidade do T1, mais as 15 OS "de bastidor"
(order_number 1 a 15), avaliações, posições dos técnicos, status de fábrica etc.
Enquanto t4/apos-cap14.json não existe, usa o T4 parcial que já foi gravado (t4/apos-cap07) + um complemento
interino de checklists (t5/_interino-t4.json), só para desenvolver; depois que o T4 termina, rodar de novo
(os ids dos tipos de serviço e dos checklists são lidos pelo NOME na cadeia, nunca copiados à mão).

Uso:  python3 rec/t5/semear.py            (gera inicio.json e rec/t5/cadeia.json)
      python3 rec/t5/semear.py --verificar (só confere se os ids de inicio.json existem na cadeia do T4)
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
EXTRA = os.path.normpath(os.path.join(HERE, '..', 'fakebase', 'seeds-extra'))
BASE_SEEDS = os.path.normpath(os.path.join(HERE, '..', 'fakebase', 'seeds'))

CHAIN_BASE = ['t3/apos-cap10', 't1/apos-cap13', 't4/inicio']
CHECKLISTS = ('Manutenção preventiva de split', 'Higienização de split')


def load(rel):
    with open(os.path.join(EXTRA, rel + '.json'), encoding='utf8') as f:
        return json.load(f)


def exists(rel):
    return os.path.exists(os.path.join(EXTRA, rel + '.json'))


def t4_chain():
    """(cadeia do T4, 'real' | 'parcial' | 'interino')
    real     = t4/apos-cap14 existe (o T4 terminou);
    parcial  = usa o último t4/apos-capNN já gravado, que já traz os dois checklists;
    interino = o último apos-capNN ainda não traz algum checklist: completa com t5/_interino-t4 (só o que falta)."""
    if exists('t4/apos-cap14'):
        return CHAIN_BASE + ['t4/apos-cap14'], 'real'
    ultimo = None
    for n in range(14, 0, -1):
        if exists(f't4/apos-cap{n:02d}'):
            ultimo = f't4/apos-cap{n:02d}'
            break
    base = CHAIN_BASE + ([ultimo] if ultimo else [])
    tem = {r['name'] for r in rows_of(base, 'form_templates')}
    if set(CHECKLISTS) <= tem:
        return base, 'parcial'
    return base + ['t5/_interino-t4'], 'interino'


def rows_of(chain, table):
    out = []
    for rel in chain:
        if exists(rel):
            out += load(rel).get(table, [])
    return out


def by_name(rows):
    return {r['name']: r for r in rows}


# ---------------------------------------------------------------------------- complemento interino (checklists do T4)
def interino_t4(chain_sem_interino):
    st = by_name(rows_of(chain_sem_interino, 'service_types'))
    tem = {r['name'] for r in rows_of(chain_sem_interino, 'form_templates')}
    defs = {
        'Manutenção preventiva de split': ('mp', st['Manutenção Preventiva']['id'], 'Roteiro da visita de manutenção preventiva', [
            ('boolean', 'Filtros limpos / em bom estado?'), ('boolean', 'Serpentinas (evap/cond) sem sujeira excessiva?'), ('boolean', 'Dreno desobstruído e escoando?'),
            ('boolean', 'Fixações e suportes firmes?'), ('boolean', 'Conexões elétricas reapertadas e sem aquecimento?'), ('number', 'Corrente do compressor medida'),
            ('number', 'Pressão de baixa'), ('number', 'Pressão de alta'), ('number', 'Temperatura de insuflamento'), ('text', 'Recomendações ao cliente')]),
        'Higienização de split': ('hig', st['Higienização de Split']['id'], 'Roteiro da higienização do aparelho', [
            ('boolean', 'Filtros lavados e secos?'), ('boolean', 'Evaporadora higienizada com produto apropriado?'), ('boolean', 'Bandeja e dreno limpos?'),
            ('boolean', 'Condensadora limpa por fora?'), ('text', 'Observações do técnico')]),
    }
    ft, fq, link = [], [], []
    for nome, (k, svc, desc, qs) in defs.items():
        if nome in tem:
            continue
        tid = f'@id:t5.interino.ft.{k}'
        ft.append({'id': tid, 'name': nome, 'description': desc, 'is_active': True})
        for i, (tipo, q) in enumerate(qs):
            fq.append({'id': f'@id:t5.interino.fq.{k}.{i}', 'template_id': tid, 'question': q, 'question_type': tipo, 'position': i, 'is_required': tipo == 'boolean'})
        link.append({'id': f'@id:t5.interino.ftst.{k}', 'template_id': tid, 'service_type_id': svc})
    return {'_comentario': 'INTERINO: só enquanto t4/apos-cap14 não existe. Completa os checklists do T4 que ainda faltam na cadeia. Não use na gravação final.',
            'form_templates': ft, 'form_questions': fq, 'form_template_service_types': link}


# ---------------------------------------------------------------------------- mundo do T5
def mundo(chain):
    st = by_name(rows_of(chain, 'service_types'))
    tt = by_name(rows_of(chain, 'task_types'))
    ft = by_name(rows_of(chain, 'form_templates'))
    cust = by_name(rows_of(chain, 'customers'))
    T = {k: st[n]['id'] for k, n in dict(MP='Manutenção Preventiva', MC='Manutenção Corretiva', INS='Instalação de Split',
                                         HIG='Higienização de Split', GAS='Carga de Gás', VT='Visita Técnica').items()}
    PRECO = {k: float(st[n]['default_price']) for k, n in dict(MP='Manutenção Preventiva', MC='Manutenção Corretiva', INS='Instalação de Split',
                                                              HIG='Higienização de Split', GAS='Carga de Gás', VT='Visita Técnica').items()}
    NOME = {k: st[n]['name'] for k, n in dict(MP='Manutenção Preventiva', MC='Manutenção Corretiva', INS='Instalação de Split',
                                              HIG='Higienização de Split', GAS='Carga de Gás', VT='Visita Técnica').items()}
    CHK = {'MP': ft['Manutenção preventiva de split']['id'], 'HIG': ft['Higienização de split']['id']}
    OS_TYPE = {'MP': 'manutencao_preventiva', 'HIG': 'manutencao_preventiva', 'MC': 'manutencao_corretiva', 'GAS': 'manutencao_corretiva',
               'INS': 'instalacao', 'VT': 'visita_tecnica'}

    # (n, tipo, cliente, equipamento, técnico, status, dia, hora, duração, descrição, criada_em)
    # dia = deslocamento em dias a partir de "hoje" (terça 03/11); None = chamado do portal sem data
    OS = [
        (1, 'INS', 'padaria', 'padaria.3', 'paulo', 'concluida', -6, '09:00', 120, 'Instalação de split Hi-Wall 9.000 BTUs no escritório da padaria', -14),
        (2, 'HIG', 'farmacia', 'farmacia.1', 'bruno', 'concluida', -5, '14:00', 120, 'Higienização completa do split do balcão', -13),
        (3, 'MP', 'roberto', 'roberto.1', 'julia', 'concluida', 0, '06:30', 120, 'Manutenção preventiva do split da sala', -12),
        (4, 'INS', 'roberto', 'roberto.1', 'rafael', 'cancelada', -4, '10:00', 180, 'Instalação de um segundo split. Cancelada: o cliente adiou a obra', -11),
        (5, 'MP', 'pousada', 'pousada.3', 'rafael', 'concluida', -1, '09:00', 120, 'Manutenção preventiva do split da recepção da pousada', -8),
        (6, 'MC', 'mercado', 'mercado.2', 'marina', 'concluida', -1, '14:00', 120, 'Split do escritório administrativo parou de gelar', -7),
        (7, 'GAS', 'academia', 'academia.1', 'lucas', 'concluida', 0, '07:30', 90, 'Recarga de gás do Cassete da sala de musculação', -6),
        (8, 'MC', 'restaurante', 'restaurante.1', 'paulo', 'pausada', -1, '13:00', 180, 'Falha no compressor do Hi-Wall do salão principal. Aguardando a peça do fornecedor', -5),
        (9, 'HIG', 'clinica', 'clinica.1', 'julia', 'em_andamento', 0, '08:30', 120, 'Higienização do split do consultório 1', -4),
        (10, 'MC', 'hotel', 'hotel.3', 'bruno', 'a_caminho', 0, '09:15', 120, 'Split da recepção com ruído e pingando água', -4),
        (11, 'MC', 'padaria', 'padaria.1', 'marina', 'pendente', 0, '14:00', 120, 'Ar-condicionado do salão de atendimento não está gelando', -3),
        (12, 'MP', 'escritorio', 'escritorio.1', 'rafael', 'agendada', 2, '10:00', 120, 'Manutenção preventiva do split da sala de reuniões', -3),
        (13, 'MP', 'condominio', 'condominio.1', 'marina', 'agendada', 6, '08:00', 120, 'Manutenção preventiva do Piso-Teto do salão de festas', -2),
        (14, 'HIG', 'pousada', 'pousada.1', 'lucas', 'pendente', 3, '09:00', 120, 'Higienização dos splits das suítes', -2),
        (15, 'MC', 'mariana', 'mariana.1', None, 'pendente', None, None, 120, 'Chamado pelo portal: o ar-condicionado do quarto está pingando água', 0),
    ]
    # tempos reais de execução das concluídas/andamento (check-in, check-out) em "HH:MM"
    EXEC = {1: ('09:10', '11:25'), 2: ('14:05', '15:30'), 3: ('06:48', '07:52'), 5: ('09:05', '10:40'), 6: ('14:10', '15:30'), 7: ('07:30', '08:25'),
            8: ('13:20', None), 9: ('08:31', None)}
    PAUSA = {8: ('-1d', '16:40')}  # paused_at

    eq_nome = {}
    for e in rows_of(['t3/apos-cap10'], 'equipment'):
        eq_nome[e['id']] = e['name']
    out = {k: [] for k in ('os_statuses', 'os_config', 'nps_settings', 'nps_criteria', 'service_orders', 'service_order_assignees',
                           'service_order_service_types', 'service_order_equipment', 'service_order_equipment_service_types',
                           'service_order_budget_items', 'service_ratings', 'service_rating_criteria', 'technician_locations')}

    # --- status de fábrica (20260606170000_catalog_tenant_isolation_hardening.sql:129-135)
    for pos, (key, label, color, dflt) in enumerate([
            ('agendada', 'Agendada', '#8b5cf6', True), ('pendente', 'Pendente', '#f59e0b', True), ('a_caminho', 'A Caminho', '#6366f1', True),
            ('em_andamento', 'Em Andamento', '#3b82f6', True), ('concluida', 'Concluída', '#22c55e', True), ('pausada', 'Pausada', '#d97706', False),
            ('cancelada', 'Cancelada', '#ef4444', True)]):
        out['os_statuses'].append({'id': f'@id:t5.status.{key}', 'key': key, 'label': label, 'color': color, 'position': pos, 'is_default': dflt,
                                   'created_at': '@now-300d', 'updated_at': '@now-300d'})
    out['os_config'].append({'id': '@id:t5.os_config', 'number_prefix': 'OS', 'number_format': '{prefix}-{year}-{number}'})
    out['nps_settings'].append({'id': '@id:t5.nps_settings', 'generate_on_finish': True, 'require_stars': False,
                                'question': 'De 0 a 10, o quão satisfeito(a) você ficou com o nosso serviço?'})
    crit_id = {}
    for pos, label in enumerate(['Qualidade', 'Pontualidade', 'Profissionalismo']):
        crit_id[label] = f'@id:t5.nps_crit.{pos}'
        out['nps_criteria'].append({'id': crit_id[label], 'label': label, 'active': True, 'position': pos, 'created_at': '@now-300d', 'updated_at': '@now-300d'})

    def dia(d):
        return f'@today{d:+d}d' if d else '@today'

    def at(d, hhmm):
        return f'@at:{d:+d}d {hhmm}'

    def soma(hhmm, minutos):
        h, m = map(int, hhmm.split(':'))
        t = h * 60 + m + minutos
        return f'{t // 60:02d}:{t % 60:02d}'

    for (n, tipo, cl, eq, tec, status, d, hora, dur, desc, criada) in OS:
        oid = f'@id:t5.os.{n:02d}'
        preco = PRECO[tipo] if tipo != 'INS' else PRECO['INS']
        valor = preco
        row = {
            'id': oid, 'order_number': n, 'entry_type': 'os', 'origin': 'portal' if n == 15 else 'manual', 'status': status,
            'os_type': OS_TYPE[tipo], 'customer_id': f'@id:customer.{cl}', 'equipment_id': f'@id:equipment.{eq}', 'service_type_id': T[tipo],
            'form_template_id': CHK.get(tipo), 'technician_id': f'@id:user.{tec}' if tec else None,
            'created_by': None if n == 15 else '@id:user.camila', 'description': desc, 'generate_nps_survey': True,
            'duration_minutes': dur, 'total_value': 0 if n == 15 else valor, 'labor_value': 0 if n == 15 else valor, 'parts_value': 0,
            'created_at': at(criada, '10:00' if n != 15 else '19:40') if n != 15 else '@now-14h',
        }
        row['updated_at'] = row['created_at']
        if d is not None:
            row['scheduled_date'] = dia(d)
            row['scheduled_time'] = hora + ':00'
            row['schedule_plan'] = [{'date': dia(d), 'time': hora, 'duration_minutes': dur}]
        if n in EXEC:
            cin, cout = EXEC[n]
            row['started_at'] = at(d, cin)
            row['check_in_time'] = at(d, cin)
            row['check_in_by'] = f'@id:user.{tec}'
            row['updated_at'] = at(d, cin)
            if cout:
                row['check_out_time'] = at(d, cout)
                row['check_out_by'] = f'@id:user.{tec}'
                row['completed_at'] = at(d, cout)
                row['updated_at'] = at(d, cout)
            if status == 'em_andamento':
                row['started_at'] = at(d, cin)
        if n in PAUSA:
            row['paused_at'] = at(-1, PAUSA[n][1])
            row['updated_at'] = at(-1, PAUSA[n][1])
        if status == 'a_caminho':
            row['updated_at'] = '@now-22m'
        out['service_orders'].append(row)

        if tec:
            out['service_order_assignees'].append({'id': f'@id:t5.assg.{n:02d}', 'service_order_id': oid, 'user_id': f'@id:user.{tec}', 'created_at': row['created_at']})
        out['service_order_service_types'].append({'service_order_id': oid, 'service_type_id': T[tipo], 'position': 0, 'created_at': row['created_at']})
        out['service_order_equipment'].append({'id': f'@id:t5.soe.{n:02d}', 'service_order_id': oid, 'equipment_id': f'@id:equipment.{eq}', 'form_template_id': CHK.get(tipo), 'created_at': row['created_at']})
        out['service_order_equipment_service_types'].append({'service_order_id': oid, 'equipment_id': f'@id:equipment.{eq}', 'service_type_id': T[tipo], 'position': 0, 'created_at': row['created_at']})
        if n != 15:
            out['service_order_budget_items'].append({'id': f'@id:t5.bud.{n:02d}', 'service_order_id': oid, 'position': 0, 'item_type': 'servico',
                                                      'description': NOME[tipo], 'quantity': 1, 'unit_price': valor, 'total_price': valor,
                                                      'service_type_id': T[tipo], 'created_at': row['created_at'], 'updated_at': row['created_at']})

    # --- avaliações respondidas (uma por OS concluída; notas 6 a 10, 2 comentários) ---------------------------------
    # (os, nps, qualidade, pontualidade, profissionalismo, respondeu em (dia, hora), quem, comentário)
    AV = [
        (1, 8, 4, 4, 5, (-2, '16:20'), 'Dona Neide Barros', None),
        (2, 10, 5, 5, 5, (-2, '10:05'), 'Fábio Couto', 'Atendimento rápido e o técnico explicou tudo o que fez. Recomendo!'),
        (3, 9, 5, 4, 5, (0, '08:20'), 'Roberto Nunes', None),
        (5, 10, 5, 5, 5, (-1, '18:15'), 'Luciana Reis', None),
        (6, 6, 3, 2, 4, (-1, '17:30'), 'Adriana Teixeira', 'O técnico chegou quase uma hora depois do combinado e não avisou.'),
        (7, 10, 5, 5, 5, (0, '08:50'), 'Ricardo Pimenta', None),
    ]
    for (n, nps, q, p, pr, (rd, rh), quem, com) in AV:
        rid = f'@id:t5.rating.{n:02d}'
        d = next(x[6] for x in OS if x[0] == n)
        cout = EXEC[n][1]
        out['service_ratings'].append({'id': rid, 'service_order_id': f'@id:t5.os.{n:02d}', 'nps_score': nps, 'quality_rating': q, 'punctuality_rating': p,
                                       'professionalism_rating': pr, 'comment': com, 'rated_by_name': quem, 'rated_at': at(rd, rh),
                                       'created_at': at(d, cout)})
        for label, val in (('Qualidade', q), ('Pontualidade', p), ('Profissionalismo', pr)):
            out['service_rating_criteria'].append({'rating_id': rid, 'criterion_id': crit_id[label], 'label_snapshot': label, 'value': val})

    # --- posições dos técnicos de hoje (BRT). Mapa ao Vivo lê as últimas 2 h; Histórico lê o dia todo -----------------
    def loc(tec, hhmm, ev, lat, lng, osn=None, addr=None, tag=''):
        out['technician_locations'].append({'id': f'@id:t5.loc.{tec}.{hhmm.replace(":", "")}{tag}', 'user_id': f'@id:user.{tec}',
                                            'service_order_id': f'@id:t5.os.{osn:02d}' if osn else None, 'event_type': ev, 'lat': lat, 'lng': lng,
                                            'address': addr, 'created_at': at(0, hhmm)})

    # Júlia: OS #3 (Roberto Nunes) de manhã cedo, depois OS #9 (Clínica Sorriso Leve) em andamento
    loc('julia', '06:20', 'en_route', -22.9040, -43.1090, 3)
    loc('julia', '06:34', 'tracking', -22.9012, -43.1162, 3)
    loc('julia', '06:48', 'check_in', -22.8963, -43.1218, 3, 'Rua Doutor Celestino, 75 - Centro, Niterói')
    loc('julia', '07:52', 'check_out', -22.8963, -43.1218, 3, 'Rua Doutor Celestino, 75 - Centro, Niterói')
    loc('julia', '08:08', 'en_route', -22.8970, -43.1210, 9)
    loc('julia', '08:20', 'tracking', -22.9004, -43.1142, 9)
    loc('julia', '08:31', 'check_in', -22.9042, -43.1081, 9, 'Rua Miguel de Frias, 90 - Icaraí, Niterói')
    # Lucas: OS #7 (Academia Ponto Forte) já concluída: o último evento é o check-out
    loc('lucas', '07:05', 'en_route', -22.9000, -43.1170, 7)
    loc('lucas', '07:30', 'check_in', -22.9059, -43.1105, 7, 'Rua Lopes Trovão, 88 - Icaraí, Niterói')
    loc('lucas', '08:25', 'check_out', -22.9059, -43.1105, 7, 'Rua Lopes Trovão, 88 - Icaraí, Niterói')
    # Bruno: a caminho do Hotel Mirante do Mar (OS #10); ~1,8 km do destino na última posição
    loc('bruno', '08:38', 'en_route', -22.9035, -43.1085, 10)
    loc('bruno', '08:44', 'tracking', -22.9062, -43.1068, 10)
    loc('bruno', '08:50', 'tracking', -22.9095, -43.1050, 10)
    loc('bruno', '08:55', 'tracking', -22.9120, -43.1035, 10)
    loc('bruno', '08:59', 'tracking', -22.9145, -43.1020, 10)

    # --- tarefas já na agenda (a aula cria a "Reunião de alinhamento da equipe" ao vivo) ----------------------------
    tarefas = [
        ('t1', 'Entregar material no Hotel Mirante do Mar', 'Entrega de material', 1, '15:00', 60, 'bruno'),
        ('t2', 'Comprar peças na distribuidora', 'Compra de peças', 3, '10:00', 90, 'paulo'),
    ]
    tar = {'service_orders': [], 'service_order_assignees': []}
    for (k, titulo, tipo_t, d, hora, dur, tec) in tarefas:
        tid = f'@id:t5.task.{k}'
        tar['service_orders'].append({
            'id': tid, 'order_number': 0, 'entry_type': 'tarefa', 'origin': 'manual', 'status': 'pendente', 'os_type': 'visita_tecnica',
            'task_title': titulo, 'task_type_id': tt[tipo_t]['id'], 'show_in_schedule': True, 'technician_id': f'@id:user.{tec}', 'created_by': '@id:user.camila',
            'scheduled_date': dia(d), 'scheduled_time': hora + ':00', 'duration_minutes': dur,
            'schedule_plan': [{'date': dia(d), 'time': hora, 'duration_minutes': dur}],
            'created_at': '@now-2d', 'updated_at': '@now-2d'})
        tar['service_order_assignees'].append({'id': f'@id:t5.assg.{k}', 'service_order_id': tid, 'user_id': f'@id:user.{tec}', 'created_at': '@now-2d'})
    tar['_comentario'] = ('T5 · as 2 tarefas que já estão na Agenda. Ficam FORA do inicio.json porque o contador "Mostrando N de M OS" do app conta a tarefa e '
                          'não a mostra (ServiceOrders.tsx:1079-1085). Só entram nos capítulos da Agenda (12 e 13). Gerado por rec/t5/semear.py.')

    mv = cust['Colégio Monte Verde']
    out['_comentario'] = ('T5 · estado de partida = fim do T4 + as 15 OS de bastidor (order_number 1 a 15), 7 status de fábrica, os_config, nps_settings, 3 critérios de NPS, '
                          '6 avaliações respondidas e posições de hoje dos técnicos. Gerado por rec/t5/semear.py: não edite à mão.')
    out['_patch'] = {'customers': [{'match': {'id': mv['id']}, 'set': {'lat': mv['latitude'], 'lng': mv['longitude']}}]}
    return out, tar


def verificar(chain, inicio):
    """Todo id literal (UUID) de inicio.json tem de existir na cadeia do T4 (serviço, tipo de tarefa, checklist, cliente)."""
    import re
    texto = json.dumps(inicio)
    achados = set(re.findall(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', texto))
    conhecidos = set()
    for rel in chain:
        if exists(rel):
            conhecidos |= set(re.findall(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', json.dumps(load(rel))))
    faltam = sorted(achados - conhecidos)
    return faltam


if __name__ == '__main__':
    chain, modo = t4_chain()
    if '--verificar' in sys.argv:
        ini = load('t5/inicio')
        faltam = verificar(chain, ini)
        print('cadeia', modo, chain)
        print('ids de inicio.json que não existem na cadeia:', faltam or 'nenhum')
        sys.exit(1 if faltam else 0)
    os.makedirs(os.path.join(EXTRA, 't5'), exist_ok=True)
    p_int = os.path.join(EXTRA, 't5', '_interino-t4.json')
    if modo == 'interino':
        sem = [c for c in chain if c != 't5/_interino-t4']
        with open(p_int, 'w', encoding='utf8') as f:
            json.dump(interino_t4(sem), f, ensure_ascii=False, indent=1)
    elif os.path.exists(p_int):
        os.remove(p_int)
    ini, tar = mundo(chain)
    with open(os.path.join(EXTRA, 't5', 'inicio.json'), 'w', encoding='utf8') as f:
        json.dump(ini, f, ensure_ascii=False, indent=1)
    with open(os.path.join(EXTRA, 't5', 'tarefas-agenda.json'), 'w', encoding='utf8') as f:
        json.dump(tar, f, ensure_ascii=False, indent=1)
    # cap00 mostra o Dashboard: OS de hoje ainda aberta aparece "Atrasada 0 dias" (bug de fuso, Dashboard.tsx:169,193,221).
    # Só na gravação da abertura, as 3 OS de hoje ainda abertas (#9, #10, #11) passam para amanhã; os demais capítulos não usam este arquivo.
    painel = {'_comentario': 'T5 cap00: tira do dia de hoje as OS ainda abertas (bug de fuso do Dashboard). Só entra na cadeia do cap00.',
              '_patch': {'service_orders': []}}
    for n, hora, dur in ((9, '08:30', 120), (10, '09:15', 120), (11, '14:00', 120)):
        painel['_patch']['service_orders'].append({
            'match': {'id': f'@id:t5.os.{n:02d}'},
            'set': {'scheduled_date': '@today+1d', 'schedule_plan': [{'date': '@today+1d', 'time': hora, 'duration_minutes': dur}]}})
    with open(os.path.join(EXTRA, 't5', 'cap00-painel.json'), 'w', encoding='utf8') as f:
        json.dump(painel, f, ensure_ascii=False, indent=1)
    with open(os.path.join(HERE, 'cadeia.json'), 'w', encoding='utf8') as f:
        json.dump({'modo': modo, 'cadeia_t4': chain, 'inicio': chain + ['t5/inicio']}, f, ensure_ascii=False, indent=1)
    faltam = verificar(chain, ini)
    n = {k: len(v) for k, v in ini.items() if isinstance(v, list)}
    print('modo T4:', modo, '| cadeia:', chain + ['t5/inicio'])
    print('linhas:', n)
    print('ids sem origem na cadeia:', faltam or 'nenhum')
