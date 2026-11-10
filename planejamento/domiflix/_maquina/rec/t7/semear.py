#!/usr/bin/env python3
"""T7 · gera o mundo de partida da aula (rec/fakebase/seeds-extra/t7/inicio.json) e rec/t7/cadeia.json.

Estado de partida = fim do T5 (o ÚLTIMO t5/apos-capNN que existe no disco, acumulado) por cima de T3, T1 e T4, e por cima
disso só o que a tela do técnico precisa e o T5 não deixa:
  - a OS #16 na quarta-feira do T7, 09:00, Pendente (o T5 já a deixa assim; aqui é conferido e reafirmado por `_patch`);
  - as ligações "Serviços desta OS" (chip do cabeçalho) e "serviço do equipamento", se o T5 não as trouxe;
  - o estoque que a janela "Consumir do estoque" lista: local "Estoque Principal" (padrão), 2 grupos e 3 materiais com saldo.
    Nomes, códigos (EST-nnn), unidades, mínimos, custos e preços são os do roteiro do T8 (que parte do fim do T7).

Os ids vêm SEMPRE lidos da cadeia (nunca copiados à mão): se o T5 regravar e a OS #16 mudar de id, basta rodar de novo.

Uso:  python3 rec/t7/semear.py             (gera inicio.json e rec/t7/cadeia.json)
      python3 rec/t7/semear.py --verificar (só confere o que o inicio.json referencia)
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EXTRA = os.path.normpath(os.path.join(HERE, '..', 'fakebase', 'seeds-extra'))

CHAIN_BASE = ['t3/apos-cap10', 't1/apos-cap13', 't4/inicio', 't4/apos-cap14']
DIA = '2026-11-11'      # quarta-feira da OS #16 (FAKE_NOW = DIA 08:50, no fuso de Brasília)
HORA = '09:00'
DURACAO = 120

# Materiais do roteiro do T8 (T08/roteiro.md, "Estado inicial"). Saldo ANTES da baixa da OS #16.
GRUPOS = [
    ('gases', 'Gases', '#0EA5E9', 0),
    ('consumiveis', 'Consumíveis', '#F59E0B', 3),
]
LOCAL_PRINCIPAL = 'estoque.principal'
MATERIAIS = [
    # chave, nome, sku, unidade, saldo, mínimo, custo, venda, grupo
    ('r410a', 'Gás refrigerante R-410A', 'EST-001', 'kg', 8.5, 10, 90.00, 150.00, 'gases'),
    ('limpa-evaporador', 'Limpa-evaporador em spray', 'EST-007', 'un', 12, 6, 20.00, 38.00, 'consumiveis'),
    ('fita-isolante', 'Fita isolante', 'EST-008', 'rolos', 30, 12, 6.50, 11.00, 'consumiveis'),
]


def load(rel):
    with open(os.path.join(EXTRA, rel + '.json'), encoding='utf8') as f:
        return json.load(f)


def exists(rel):
    return os.path.exists(os.path.join(EXTRA, rel + '.json'))


def ultimo_t5():
    for n in range(40, 0, -1):
        rel = f't5/apos-cap{n:02d}'
        if exists(rel):
            return rel
    raise SystemExit('não achei nenhum t5/apos-capNN: o T5 ainda não gravou nada')


def cadeia():
    return CHAIN_BASE + ['t5/inicio', ultimo_t5()]


def linhas(chain, tabela):
    """linhas da tabela na cadeia (a última versão de cada id vence; `_patch` não é aplicado aqui)."""
    por_id = {}
    for rel in chain:
        if exists(rel):
            for r in load(rel).get(tabela, []):
                por_id[r.get('id') or id(r)] = r
    return list(por_id.values())


def achar_os16(chain):
    achadas = [r for r in linhas(chain, 'service_orders') if r.get('order_number') == 16]
    if len(achadas) != 1:
        raise SystemExit(f'esperava uma OS #16 na cadeia, achei {len(achadas)}')
    return achadas[0]


def montar(chain):
    os16 = achar_os16(chain)
    oid, emp, eq, st = os16['id'], os16['company_id'], os16['equipment_id'], os16['service_type_id']
    tecnico = os16['technician_id']
    ini = {
        '_comentario': 'T7 · estado de partida = fim do T5 + estoque do Consumo na OS. Gerado por rec/t7/semear.py: não edite à mão.',
    }

    # --- OS #16: quarta-feira, 09:00, Pendente, ninguém mexeu ainda (o T5 deixa assim; reafirmado) ---
    patch = {
        'status': 'pendente', 'scheduled_date': DIA, 'scheduled_time': HORA + ':00', 'duration_minutes': DURACAO,
        'schedule_plan': [{'date': DIA, 'time': HORA, 'duration_minutes': DURACAO}],
        'check_in_time': None, 'check_in_by': None, 'check_in_location': None,
        'check_out_time': None, 'check_out_by': None, 'check_out_location': None,
        'started_at': None, 'paused_at': None, 'resumed_at': None, 'completed_at': None, 'partial_finish': False,
    }
    ini['_patch'] = {'service_orders': [{'match': {'id': oid}, 'set': patch}]}

    # --- "Serviços desta OS" (chip do cabeçalho) e serviço do equipamento: só se o T5 não trouxe ---
    tem_st = any(r.get('service_order_id') == oid for r in linhas(chain, 'service_order_service_types'))
    tem_est = any(r.get('service_order_id') == oid for r in linhas(chain, 'service_order_equipment_service_types'))
    if not tem_st:
        ini['service_order_service_types'] = [
            {'service_order_id': oid, 'service_type_id': st, 'position': 0, 'created_at': os16.get('created_at')}]
    if not tem_est:
        ini['service_order_equipment_service_types'] = [
            {'service_order_id': oid, 'equipment_id': eq, 'service_type_id': st, 'position': 0, 'created_at': os16.get('created_at')}]

    # --- estoque: local padrão, grupos, materiais e saldo por local ---
    ini['stocks'] = [{'id': f'@id:{LOCAL_PRINCIPAL}', 'company_id': emp, 'name': 'Estoque Principal', 'is_default': True,
                      'sort_order': 0, 'customer_id': None}]
    ini['material_groups'] = [{'id': f'@id:grupo.{k}', 'company_id': emp, 'name': nome, 'color': cor, 'sort_order': ordem}
                              for k, nome, cor, ordem in GRUPOS]
    inv, niveis = [], []
    for k, nome, sku, un, saldo, minimo, custo, venda, grupo in MATERIAIS:
        inv.append({'id': f'@id:material.{k}', 'company_id': emp, 'name': nome, 'sku': sku, 'unit': un, 'quantity': saldo,
                    'min_quantity': minimo, 'cost_price': custo, 'sale_price': venda, 'group_id': f'@id:grupo.{grupo}',
                    'is_sellable': False, 'customer_id': None, 'created_at': '@now-90d', 'updated_at': '@now-90d'})
        niveis.append({'id': f'@id:nivel.{k}.principal', 'company_id': emp, 'inventory_id': f'@id:material.{k}',
                       'stock_id': f'@id:{LOCAL_PRINCIPAL}', 'quantity': saldo, 'min_quantity': minimo, 'is_present': True,
                       'created_at': '@now-90d', 'updated_at': '@now-90d'})
    ini['inventory'] = inv
    ini['inventory_stock_levels'] = niveis
    return ini, os16, tecnico


def verificar(chain, ini, os16):
    ok = True
    ids = set()
    for rel in chain:
        if exists(rel):
            ids |= set(re.findall(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', json.dumps(load(rel))))
    # ids que o inicio referencia e que NÃO são criados por ele
    proprios = set(re.findall(r'@id:[\w.\-]+', json.dumps(ini)))
    ref = set(re.findall(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', json.dumps(ini)))
    faltam = sorted(ref - ids)
    if faltam:
        ok = False
        print('ids que o inicio.json usa e a cadeia não tem:', faltam)
    tpl = [t for t in linhas(chain, 'form_templates') if t['id'] == os16['form_template_id']]
    perg = [q for q in linhas(chain, 'form_questions') if q.get('template_id') == os16['form_template_id']]
    print(f"checklist da OS #16: {tpl[0]['name'] if tpl else '??'} com {len(perg)} perguntas")
    if not tpl or len(perg) != 13:
        ok = False
    cli = [c for c in linhas(chain, 'customers') if c['id'] == os16['customer_id']]
    print('cliente da OS #16:', cli[0]['name'] if cli else '(vem do T3/base; conferir no falso)')
    print(f'{len(proprios)} ids próprios no inicio.json;', 'OK' if ok else 'COM PROBLEMA')
    return ok


def main():
    chain = cadeia()
    ini, os16, tecnico = montar(chain)
    if '--verificar' in sys.argv:
        sys.exit(0 if verificar(chain, ini, os16) else 1)
    os.makedirs(os.path.join(EXTRA, 't7'), exist_ok=True)
    with open(os.path.join(EXTRA, 't7', 'inicio.json'), 'w', encoding='utf8') as f:
        json.dump(ini, f, ensure_ascii=False, indent=1)
    with open(os.path.join(HERE, 'cadeia.json'), 'w', encoding='utf8') as f:
        json.dump({'t5_final': chain[-1], 'cadeia_t5': chain, 'inicio': chain + ['t7/inicio'],
                   'os16': os16['id'], 'public_short_code': os16.get('public_short_code'), 'tecnico': tecnico,
                   'dia': DIA}, f, ensure_ascii=False, indent=1)
    print('t7/inicio.json e rec/t7/cadeia.json gerados.')
    print('  fim do T5 usado:', chain[-1])
    print('  OS #16:', os16['id'], '| código curto', os16.get('public_short_code'), '| dia', DIA, HORA)
    print('  extras:', [k for k in ini if not k.startswith('_')])
    verificar(chain, ini, os16)


if __name__ == '__main__':
    main()
