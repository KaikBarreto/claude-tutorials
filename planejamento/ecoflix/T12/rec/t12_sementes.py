#!/usr/bin/env python3
"""T12 · escreve rec/mundo/seeds-extra/t12/inicio.json: o mundo das coletas em 10/11/2026 07:00 (plano.md, "Mundo: o que esta aula precisa";
MUNDO_LINHA_DO_TEMPO.md, seções 3 e 12). Por cima do mundo base (B): configurações padrão do módulo, os tipos "Caçamba 5 m³" (uma a uma,
Caçamba 01 a 05) e "Bag 1 m³" (por quantidade, 40), as movimentações de 01/08, 23/10 (ordem 5) e 27/10 (ordem 6), as ordens 1 a 8 com o
histórico (só mudanças de etapa: o app não grava evento de criação) e o portal da Cooperativa Recomeço (token fictício, sem senha).
A frota (taras, motoristas) é do mundo base: esta semente não mexe nela.
Uso: python3 -I rec/t12/t12_sementes.py"""
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.normpath(os.path.join(HERE, '..', 'mundo', 'seeds-extra', 't12'))
CO, RAFAEL = '@id:company.reciclavale', '@id:user.rafael'
COOP, VALE, SIQ = '@id:fornecedor.recomeco', '@id:fornecedor.valeforte', '@id:fornecedor.siqueira'
FROTA = {'edson': ('@id:motorista.truck', 'Edson Moura', '@id:veiculo.truck', 'FKD2E41'),
         'jair': ('@id:motorista.34', 'Jair Lopes', '@id:veiculo.34', 'GHT7B19'),
         'tiago': ('@id:motorista.picape', 'Tiago Freitas', '@id:veiculo.picape', 'EZR4C63')}
# endereço do cadastro de cada parceiro (seeds/02-cadastros.json)
END = {COOP: ('Cooperativa Recomeço', 'Rua do Trabalho', '57', 'Vila Nossa Senhora das Graças', 'Taubaté', 'SP', '12060-640'),
       VALE: ('Auto Peças Vale Forte', 'Avenida Brasil', '1290', 'Centro', 'Taubaté', 'SP', '12080-010'),
       SIQ: ('Depósito Irmãos Siqueira', 'Estrada do Pinheirinho', '2730', 'Pinheirinho', 'Tremembé', 'SP', '12091-500')}
ALFA = 'abcdefghjkmnpqrstuvwxyz23456789'
TOKEN_COOP = '@id:t12.portal.recomeco'   # portal_token é uuid (utils/portalSlug.ts aceita o uuid puro no fim do link)


def z(data, hora):
    """data e hora de Brasília (UTC-3) -> ISO em UTC"""
    h, m = map(int, hora.split(':'))
    from datetime import datetime, timedelta
    t = datetime.fromisoformat(f'{data}T{h:02d}:{m:02d}:00') + timedelta(hours=3)
    return t.strftime('%Y-%m-%dT%H:%M:%S.000Z')


def codigo(n):
    h = hashlib.sha1(f'ecoflix-t12-ordem-{n}'.encode()).digest()
    return ''.join(ALFA[b % len(ALFA)] for b in h[:12])


TIPO_CACAMBA, TIPO_BAG = '@id:t12.tipo.cacamba', '@id:t12.tipo.bag'
CACAMBA = {i: f'@id:t12.cacamba.{i:02d}' for i in range(1, 6)}

# (nº, parceiro, criada, data, janela, frota, material, status, eventos [(de, para, data, hora, nota)], concluída)
ORDENS = [
    (1, COOP, ('2026-09-30', '10:00'), '2026-10-02', 'manha', 'tiago', '~500 kg de latinha', 'coletada',
     [('agendada', 'a_caminho', '2026-10-02', '07:30', None), ('a_caminho', 'coletada', '2026-10-02', '09:40', None)]),
    (2, VALE, ('2026-10-06', '14:00'), '2026-10-08', 'manha', 'jair', '~850 kg de chaparia', 'coletada',
     [('agendada', 'a_caminho', '2026-10-08', '07:20', None), ('a_caminho', 'coletada', '2026-10-08', '09:10', None)]),
    (3, SIQ, ('2026-10-14', '11:00'), '2026-10-16', 'dia_todo', 'edson', '~3 t de ferro misto', 'coletada',
     [('agendada', 'a_caminho', '2026-10-16', '07:10', None), ('a_caminho', 'coletada', '2026-10-16', '15:30', None)]),
    (4, VALE, ('2026-10-19', '10:30'), '2026-10-21', 'manha', 'jair', '~200 kg de baterias', 'cancelada',
     [('agendada', 'cancelada', '2026-10-20', '16:00', 'Material ainda não separado')]),
    (5, COOP, ('2026-10-21', '09:00'), '2026-10-23', 'tarde', 'tiago', '~700 kg de PET', 'coletada',
     [('agendada', 'a_caminho', '2026-10-23', '13:20', None), ('a_caminho', 'coletada', '2026-10-23', '15:40', None)]),
    (6, SIQ, ('2026-10-23', '11:00'), '2026-10-27', 'manha', 'edson', 'Entrega de caçamba', 'coletada',
     [('agendada', 'a_caminho', '2026-10-27', '07:30', None), ('a_caminho', 'coletada', '2026-10-27', '09:15', None)]),
    (7, None, ('2026-11-09', '15:20'), '2026-11-10', 'manha', 'tiago', '~300 kg de ferro de demolição', 'a_caminho',
     [('agendada', 'a_caminho', '2026-11-10', '06:40', None)]),
    (8, SIQ, ('2026-11-05', '10:00'), '2026-11-10', 'manha', 'edson', 'Troca da Caçamba 03: ferro misto, ~2 t', 'agendada', []),
]


def main():
    out = {'_doc': 'T12 · mundo das coletas em 10/11/2026 07:00 (gerado por rec/t12/t12_sementes.py; não editar à mão).'}
    out['collection_settings'] = [{
        'company_id': CO, 'order_number_prefix': None, 'time_windows': ['manha', 'tarde', 'dia_todo'], 'require_driver_vehicle': False,
        'portal_require_approval': True, 'portal_min_lead_hours': 0, 'portal_accepted_weekdays': [1, 2, 3, 4, 5, 6], 'notify_on_request': True,
        'require_driver_signature': False, 'require_responsible_signature': False, 'public_report_show_values': False,
        'checklist_template_id': None, 'created_at': z('2026-08-01', '09:00'), 'updated_at': z('2026-08-01', '09:00')}]
    out['collection_equipment_types'] = [
        {'id': TIPO_CACAMBA, 'company_id': CO, 'nome': 'Caçamba 5 m³', 'identificavel': True, 'ativo': True,
         'created_at': z('2026-08-01', '08:50'), 'updated_at': z('2026-08-01', '08:50')},
        {'id': TIPO_BAG, 'company_id': CO, 'nome': 'Bag 1 m³', 'identificavel': False, 'ativo': True,
         'created_at': z('2026-08-01', '08:52'), 'updated_at': z('2026-08-01', '08:52')}]
    out['collection_containers'] = [
        {'id': CACAMBA[i], 'company_id': CO, 'identificacao': f'Caçamba {i:02d}', 'equipment_type_id': TIPO_CACAMBA, 'condicao': 'ok',
         'ativo': True, 'status': 'disponivel', 'created_at': z('2026-08-01', f'08:{54 + i:02d}'), 'updated_at': z('2026-08-01', f'08:{54 + i:02d}')}
        for i in range(1, 6)]

    def mov(k, tipo, cont, qtd, de, para, quando, ordem=None):
        o_kind, o_pid = ('partner', de) if de not in ('base', 'externo') else (de, None)
        d_kind, d_pid = ('partner', para) if para not in ('base', 'externo') else (para, None)
        return {'id': f'@id:t12.mov.{k}', 'company_id': CO, 'equipment_type_id': tipo, 'container_id': cont, 'quantidade': qtd,
                'origem_kind': o_kind, 'origem_partner_type': 'supplier' if o_pid else None, 'origem_partner_id': o_pid,
                'origem_partner_nome': END[o_pid][0] if o_pid else None,
                'destino_kind': d_kind, 'destino_partner_type': 'supplier' if d_pid else None, 'destino_partner_id': d_pid,
                'destino_partner_nome': END[d_pid][0] if d_pid else None,
                'moved_at': quando, 'created_at': quando, 'updated_at': quando, 'created_by': RAFAEL, 'collection_order_id': ordem,
                'observacao': None, 'voided': False, 'edit_history': []}
    ini = z('2026-08-01', '09:00')
    movs = [mov(f'inicial.cacamba{i:02d}', TIPO_CACAMBA, CACAMBA[i], 1, 'externo', 'base', ini) for i in range(1, 6)]
    movs.append(mov('inicial.bags', TIPO_BAG, None, 40, 'externo', 'base', ini))
    movs.append(mov('ordem5.bags', TIPO_BAG, None, 10, 'base', COOP, z('2026-10-23', '15:40'), '@id:t12.ordem.5'))
    movs.append(mov('ordem6.cacamba03', TIPO_CACAMBA, CACAMBA[3], 1, 'base', SIQ, z('2026-10-27', '09:15'), '@id:t12.ordem.6'))
    out['collection_equipment_movements'] = movs

    ordens, eventos = [], []
    for n, parc, (cd, ch), data, janela, quem, material, status, evs in ORDENS:
        did, dnome, vid, placa = FROTA[quem]
        if parc:
            nome, lg, num, bai, cid, uf, cep = END[parc]
        else:   # ordem 7: "Sem cadastro" (Marcelo Tavares, reforma em Taubaté)
            nome, lg, num, bai, cid, uf, cep = 'Marcelo Tavares', 'Rua das Paineiras', '215', None, 'Taubaté', 'SP', None
        fim = [e for e in evs if e[1] == 'coletada']
        ultimo = z(evs[-1][2], evs[-1][3]) if evs else z(cd, ch)
        ordens.append({
            'id': f'@id:t12.ordem.{n}', 'company_id': CO, 'numero': n, 'status': status, 'origem': 'interna',
            'partner_type': 'supplier', 'partner_id': parc, 'partner_nome': nome, 'contato_telefone': None if parc else '(12) 90000-5821',
            'logradouro': lg, 'numero_end': num, 'bairro': bai, 'cidade': cid, 'uf': uf, 'cep': cep,
            'scheduled_date': data, 'scheduled_window': janela, 'driver_id': did, 'driver_name': dnome, 'vehicle_id': vid, 'vehicle_plate': placa,
            'material_estimado': material, 'observacoes': None, 'completed_at': z(fim[0][2], fim[0][3]) if fim else None,
            'public_short_code': codigo(n), 'created_at': z(cd, ch), 'updated_at': ultimo})
        for k, (de, para, d, h, nota) in enumerate(evs):
            eventos.append({'id': f'@id:t12.evento.{n}.{k}', 'company_id': CO, 'order_id': f'@id:t12.ordem.{n}', 'event_type': 'status_change',
                            'from_status': de, 'to_status': para, 'nota': nota, 'created_by': RAFAEL, 'created_at': z(d, h)})
    out['collection_orders'] = ordens
    out['collection_order_events'] = eventos
    out['_patch'] = {'suppliers': [{'match': {'id': COOP}, 'set': {
        'portal_token': TOKEN_COOP, 'portal_password_enabled': False, 'portal_config': {'coletas': True, 'solicitar_coleta': True}}}]}
    os.makedirs(SAIDA, exist_ok=True)
    caminho = os.path.join(SAIDA, 'inicio.json')
    json.dump(out, open(caminho, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print(f'{caminho}: {len(ordens)} ordens, {len(eventos)} eventos, {len(movs)} movimentações')


if __name__ == '__main__':
    main()
