#!/usr/bin/env python3
"""T11 · Produção: gera as sementes extras da aula em rec/mundo/seeds-extra/t11/ (determinístico; rodar de novo refaz igual).

Cadeia (cada capítulo abre um navegador novo e parte da lista acumulada; ver SEMENTE no gerar.py):
  inicio       estado de 10/11 08:30 (caps 0 a 3): Fardo de alumínio cadastrado (código 16, estoque 0), Cláudio e Diego (RH),
               quadro com "A fazer", "Em produção" e "Concluída", a ficha do Cobre mel (1,6 kg de fio por kg) e as ordens #1 e #2
               de 03/11 (a #2 é a mesma produção lançada duas vezes), com os lançamentos, o custo e o Kardex; tolerância 2 % e meta 250.
  apos-cap03   + a ficha do Fardo de alumínio (Alumínio latinha 1 kg por kg, unidade Kg), sem coproduto
  apos-cap04   + o coproduto Chaparia na ficha do fardo
  apos-cap05   + a ordem #3 (500 kg, 10/11, responsável Marcos Antunes, equipe Cláudio e Diego, coluna "A fazer", rascunho)
  apos-cap06   "Em produção" renomeada "Na prensa" e a #3 nela
  apos-cap09   + o lançamento de 10/11 (Cláudio 260, Diego 220, Chaparia 14, latinha real 498 com "Material reaproveitável"),
               o estoque ajustado (latinha -498, fardo +480, chaparia +14) e a #3 "em andamento" com R$ 3.087,60
  apos-cap10   a #3 finalizada, na "Concluída"
  apos-cap12   "Bloquear finalização quando faltar matéria-prima em estoque" ligado
  apos-cap13   a #2 excluída, com o estorno no Kardex (fio +80, cobre mel -50)

O histórico do mundo base não tem fio de cobre para duas produções de 80 kg em 03/11. Para o Kardex de novembro fechar sem saldo
negativo, esta semente desloca o saldo dos movimentos ANTERIORES à produção de 03/11 (fio +160 kg; cobre mel -50 kg, só a ordem #1),
no saldo inicial de 01/08 e nas colunas "Estoque inicial"/"Estoque final" até 03/11 16:00. A #2 (a ordem duplicada) fica por cima do
mundo base no cobre mel: os movimentos POSTERIORES somam +50 kg e o cobre mel de hoje é o do mundo base + 50 kg; a exclusão do cap13
devolve o do mundo base (a #2 inflava o estoque, e o mundo base tem menos de 50 kg de cobre mel). O fio de hoje é o do mundo base.
Os saldos do mundo base são lidos do histórico e conferidos com o cadastro (nada fixo aqui).
Uso: python3 -I rec/t11/t11_sementes.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
MUNDO = os.path.normpath(os.path.join(HERE, '..', 'mundo'))
SAIDA = os.path.join(MUNDO, 'seeds-extra', 't11')

CID = '@id:company.reciclavale'
RAFAEL = '@id:user.rafael'
LATINHA, CHAPARIA, COBRE_MEL, FIO = '@id:material.al_latinha', '@id:material.chaparia', '@id:material.cobre_mel', '@id:material.fio_cobre'
FARDO = '@id:t11.material.fardo'
CLAUDIO, DIEGO = '@id:employee.claudio', '@id:employee.diego'
COL_AFAZER, COL_EMPROD, COL_CONCLUIDA = '@id:t11.kanban.a_fazer', '@id:t11.kanban.em_producao', '@id:t11.kanban.concluida'
REC_COBRE, REC_FARDO = '@id:t11.recipe.cobre_mel', '@id:t11.recipe.fardo'
OP = {n: f'@id:t11.order.{n}' for n in (1, 2, 3)}
ENT = {n: f'@id:t11.entry.{n}' for n in (1, 2, 3)}

CORTE = '2026-11-03T19:00:00.000Z'   # 03/11 16:00 em Brasília: a produção #1 (a #2 às 16:05)


def base():
    return json.load(open(os.path.join(MUNDO, 'seeds', '03-historico.json'), encoding='utf8'))


def movs(h, mat):
    return sorted([m for m in h['stock_movements'] if m['material_id'] == mat], key=lambda m: m['transaction_at'])


def chave(m):
    """o movimento do mundo base pelo id (sm.N é a posição na semente base) E pelo material e a hora: se a semente base mudar e
    esta não for refeita, o _patch não acha a linha em vez de mexer na linha errada. Refaça sempre que o mundo base mudar."""
    return {'id': m['id'], 'material_id': m['material_id'], 'transaction_at': m['transaction_at']}


def desloca(h, mat, delta):
    """_patch dos movimentos do material antes do CORTE: saldo inicial (quantidade) e as colunas de estoque somam `delta`."""
    out = []
    for m in movs(h, mat):
        if m['transaction_at'] >= CORTE:
            continue
        s = {'stock_after': round(m['stock_after'] + delta, 3)}
        if m['type'] == 'SALDO_INICIAL':
            s['quantity'] = round(m['quantity'] + delta, 3)
        else:
            s['stock_before'] = round(m['stock_before'] + delta, 3)
        if min(s.get('stock_before', 0), s['stock_after']) < 0:
            raise SystemExit(f'{mat}: saldo negativo depois do deslocamento em {m["id"]}')
        out.append({'match': chave(m), 'set': s})
    return out


def desloca_depois(h, mat, delta):
    """_patch dos movimentos do material a partir do CORTE: as colunas de estoque somam `delta`."""
    return [{'match': chave(m), 'set': {'stock_before': round(m['stock_before'] + delta, 3), 'stock_after': round(m['stock_after'] + delta, 3)}}
            for m in movs(h, mat) if m['transaction_at'] >= CORTE]


def estoque_b(h, mat):
    """Saldo do material no mundo base: o último movimento do histórico, conferido com o cadastro."""
    saldo = round(movs(h, mat)[-1]['stock_after'], 3)
    cad = json.load(open(os.path.join(MUNDO, 'seeds', '02-cadastros.json'), encoding='utf8'))['materials']
    atual = [float(m['current_stock']) for m in cad if m['id'] == mat]
    if atual and abs(atual[0] - saldo) > 0.0005:
        raise SystemExit(f'{mat}: o histórico termina em {saldo} e o cadastro diz {atual[0]}')
    return saldo


def saldo_no_corte(h, mat, delta):
    ant = [m for m in movs(h, mat) if m['transaction_at'] < CORTE]
    return round(ant[-1]['stock_after'] + delta, 3)


def dia(iso):
    return iso[:10] if iso[11:13] >= '03' else None   # todas as horas usadas aqui são diurnas (BRT = UTC-3, sem virar o dia)


def mov(id_, mat, qtd, antes, at, desc, ordem, entrada, rel=None):
    return {'id': id_, 'company_id': CID, 'material_id': mat, 'type': 'PRODUCAO', 'quantity': qtd, 'stock_before': antes,
            'stock_after': round(antes + qtd, 3), 'description': desc, 'order_id': ordem, 'order_type': 'production', 'entry_id': entrada,
            'related_movement_id': rel, 'created_by': RAFAEL, 'transaction_at': at, 'transaction_date': at[:10], 'created_at': at}


def inicio(h):
    fio0 = saldo_no_corte(h, FIO, 160)          # as duas ordens saem do saldo deslocado
    cobre0 = saldo_no_corte(h, COBRE_MEL, -50)  # a #1 absorvida; a #2 fica por cima
    d = {
        'materials': [{
            'id': FARDO, 'company_id': CID, 'code': '16', 'name': 'Fardo de alumínio', 'fiscal_name': None, 'group_id': '@id:grupo.aluminio',
            'unit': 'Kg', 'ncm': '7602.00.00', 'purchase_price': 6.2, 'sale_price': 7.9, 'purchase_price_currency': 'BRL', 'sale_price_currency': 'BRL',
            'current_stock': 0, 'is_archived': False, 'created_by': RAFAEL, 'created_at': '2026-11-01T12:00:00.000Z', 'updated_at': '2026-11-01T12:00:00.000Z'}],
        # os dois ajudantes do pátio com os dados do T19/plano.md (a T11 só mostra nome e cargo)
        'employees': [
            {'id': CLAUDIO, 'company_id': CID, 'name': 'Cláudio Ferraz', 'position': 'Ajudante de pátio', 'cpf': '334.095.127-64', 'phone': '(12) 90000-4105',
             'hire_date': '2022-01-11', 'salary': 2100, 'employment_regime': 'clt', 'is_active': True, 'archived_at': None, 'created_by': RAFAEL,
             'created_at': '2026-08-01T12:00:00.000Z', 'updated_at': '2026-08-01T12:00:00.000Z'},
            {'id': DIEGO, 'company_id': CID, 'name': 'Diego Morais', 'position': 'Ajudante de pátio', 'cpf': '447.103.682-36', 'phone': '(12) 90000-4106',
             'hire_date': '2025-07-07', 'salary': 1980, 'employment_regime': 'informal', 'is_active': True, 'archived_at': None, 'created_by': RAFAEL,
             'created_at': '2026-08-01T12:00:00.000Z', 'updated_at': '2026-08-01T12:00:00.000Z'}],
        'production_kanban_columns': [
            {'id': COL_AFAZER, 'company_id': CID, 'name': 'A fazer', 'position': 0, 'color': '#EF4444', 'is_done': False, 'created_by': RAFAEL,
             'created_at': '2026-11-01T12:30:00.000Z', 'updated_at': '2026-11-01T12:30:00.000Z'},
            {'id': COL_EMPROD, 'company_id': CID, 'name': 'Em produção', 'position': 1, 'color': '#F59E0B', 'is_done': False, 'created_by': RAFAEL,
             'created_at': '2026-11-01T12:30:00.000Z', 'updated_at': '2026-11-01T12:30:00.000Z'},
            {'id': COL_CONCLUIDA, 'company_id': CID, 'name': 'Concluída', 'position': 2, 'color': '#10B981', 'is_done': True, 'created_by': RAFAEL,
             'created_at': '2026-11-01T12:30:00.000Z', 'updated_at': '2026-11-01T12:30:00.000Z'}],
        'production_recipes': [
            {'id': REC_COBRE, 'company_id': CID, 'name': None, 'output_material_id': COBRE_MEL, 'production_unit': 'Kg', 'output_qty_per_batch': 1,
             'pieces_per_commercial_unit': None, 'is_active': True, 'created_by': RAFAEL, 'created_at': '2026-11-01T13:00:00.000Z',
             'updated_at': '2026-11-01T13:00:00.000Z'}],
        'production_recipe_inputs': [
            {'id': '@id:t11.recipe_input.cobre_mel.fio', 'recipe_id': REC_COBRE, 'company_id': CID, 'material_id': FIO, 'qty_per_output': 1.6,
             'loss_pct': None, 'scrap_material_id': None, 'created_at': '2026-11-01T13:00:00.000Z'}],
        'production_orders': [], 'production_order_entries': [], 'production_order_consumption': [], 'production_order_outputs': [],
        'production_order_workers': [], 'stock_movements': [],
    }
    for n, criada, mov_at, fim in ((1, '2026-11-03T12:10:00.000Z', '2026-11-03T19:00:00.000Z', '2026-11-03T19:01:00.000Z'),
                                   (2, '2026-11-03T19:03:00.000Z', '2026-11-03T19:05:00.000Z', '2026-11-03T19:06:00.000Z')):
        d['production_orders'].append({
            'id': OP[n], 'company_id': CID, 'order_number': n, 'recipe_id': REC_COBRE, 'output_material_id': COBRE_MEL, 'planned_qty': 50, 'produced_qty': 50,
            'status': 'completed', 'production_date': '2026-11-03', 'responsible': 'Rafael Nogueira', 'notes': None, 'created_by': RAFAEL, 'employee_id': None,
            'kanban_column_id': COL_CONCLUIDA, 'machine_id': None, 'total_material_cost': 1440, 'cost_per_unit': 28.8, 'completed_at': fim,
            'client_request_id': None, 'created_at': criada, 'updated_at': fim})
        d['production_order_entries'].append({
            'id': ENT[n], 'production_order_id': OP[n], 'company_id': CID, 'entry_date': '2026-11-03', 'produced_qty': 50, 'posted': True,
            'total_material_cost': 1440, 'note': None, 'client_request_id': None, 'created_by': RAFAEL, 'created_at': mov_at, 'updated_at': mov_at})
        d['production_order_consumption'].append({
            'id': f'@id:t11.cons.{n}.fio', 'production_order_id': OP[n], 'entry_id': ENT[n], 'company_id': CID, 'material_id': FIO, 'theoretical_qty': 80,
            'actual_qty': 80, 'unit_cost': 18, 'line_cost': 1440, 'loss_qty': 0, 'loss_reason': None, 'created_at': mov_at})
        d['production_order_outputs'].append({
            'id': f'@id:t11.out.{n}.cobre_mel', 'production_order_id': OP[n], 'entry_id': ENT[n], 'company_id': CID, 'material_id': COBRE_MEL,
            'is_primary': True, 'qty': 50, 'created_at': mov_at})
        d['production_order_workers'] += [
            {'id': f'@id:t11.worker.{n}.diego.equipe', 'order_id': OP[n], 'entry_id': None, 'employee_id': DIEGO, 'company_id': CID, 'produced_qty': None,
             'created_at': criada},
            {'id': f'@id:t11.worker.{n}.diego.dia', 'order_id': OP[n], 'entry_id': ENT[n], 'employee_id': DIEGO, 'company_id': CID, 'produced_qty': 50,
             'created_at': mov_at}]
        d['stock_movements'] += [
            mov(f'@id:t11.sm.{n}.fio', FIO, -80, fio0, mov_at, 'Consumo de produção (lançamento)', OP[n], ENT[n]),
            mov(f'@id:t11.sm.{n}.cobre_mel', COBRE_MEL, 50, cobre0, mov_at, 'Produto de produção (lançamento)', OP[n], ENT[n])]
        fio0 -= 80
        cobre0 += 50
    d['_patch'] = {
        'companies': [{'match': {'id': CID}, 'set': {'production_loss_tolerance_pct': 2, 'production_daily_goal': 250}}],
        'stock_movements': desloca(h, FIO, 160) + desloca(h, COBRE_MEL, -50) + desloca_depois(h, COBRE_MEL, 50),
        'materials': [{'match': {'id': COBRE_MEL}, 'set': {'current_stock': round(estoque_b(h, COBRE_MEL) + 50, 3)}}],
    }
    return d


def apos_cap03():
    return {
        'production_recipes': [
            {'id': REC_FARDO, 'company_id': CID, 'name': None, 'output_material_id': FARDO, 'production_unit': 'Kg', 'output_qty_per_batch': 1,
             'pieces_per_commercial_unit': None, 'is_active': True, 'created_by': RAFAEL, 'created_at': '2026-11-10T11:36:00.000Z',
             'updated_at': '2026-11-10T11:36:00.000Z'}],
        'production_recipe_inputs': [
            {'id': '@id:t11.recipe_input.fardo.latinha', 'recipe_id': REC_FARDO, 'company_id': CID, 'material_id': LATINHA, 'qty_per_output': 1,
             'loss_pct': None, 'scrap_material_id': None, 'created_at': '2026-11-10T11:36:00.000Z'}],
    }


def apos_cap04():
    return {
        'production_recipe_outputs': [
            {'id': '@id:t11.recipe_output.fardo.chaparia', 'recipe_id': REC_FARDO, 'company_id': CID, 'material_id': CHAPARIA, 'qty_per_output': 0,
             'created_at': '2026-11-10T11:38:00.000Z'}],
        '_patch': {'production_recipes': [{'match': {'id': REC_FARDO}, 'set': {'updated_at': '2026-11-10T11:38:00.000Z'}}]},
    }


def apos_cap05():
    criada = '2026-11-10T11:42:00.000Z'
    return {
        'production_orders': [{
            'id': OP[3], 'company_id': CID, 'order_number': 3, 'recipe_id': REC_FARDO, 'output_material_id': FARDO, 'planned_qty': 500, 'produced_qty': None,
            'status': 'draft', 'production_date': '2026-11-10', 'responsible': 'Marcos Antunes', 'notes': None, 'created_by': RAFAEL, 'employee_id': None,
            'kanban_column_id': COL_AFAZER, 'machine_id': None, 'total_material_cost': None, 'cost_per_unit': None, 'completed_at': None,
            'client_request_id': None, 'created_at': criada, 'updated_at': criada}],
        'production_order_workers': [
            {'id': '@id:t11.worker.3.claudio.equipe', 'order_id': OP[3], 'entry_id': None, 'employee_id': CLAUDIO, 'company_id': CID, 'produced_qty': None, 'created_at': criada},
            {'id': '@id:t11.worker.3.diego.equipe', 'order_id': OP[3], 'entry_id': None, 'employee_id': DIEGO, 'company_id': CID, 'produced_qty': None, 'created_at': criada}],
    }


def apos_cap06():
    return {'_patch': {
        'production_kanban_columns': [{'match': {'id': COL_EMPROD}, 'set': {'name': 'Na prensa', 'updated_at': '2026-11-10T11:45:00.000Z'}}],
        'production_orders': [{'match': {'id': OP[3]}, 'set': {'kanban_column_id': COL_EMPROD, 'updated_at': '2026-11-10T11:46:00.000Z'}}],
    }}


def apos_cap09(h):
    lat, chap = estoque_b(h, LATINHA), estoque_b(h, CHAPARIA)
    at = '2026-11-10T20:33:00.000Z'   # 17:33 em Brasília (FAKE_NOW 17:30 do cap07 em diante)
    return {
        'production_order_entries': [{
            'id': ENT[3], 'production_order_id': OP[3], 'company_id': CID, 'entry_date': '2026-11-10', 'produced_qty': 480, 'posted': True,
            'total_material_cost': 3087.6, 'note': None, 'client_request_id': None, 'created_by': RAFAEL, 'created_at': at, 'updated_at': at}],
        'production_order_consumption': [{
            'id': '@id:t11.cons.3.latinha', 'production_order_id': OP[3], 'entry_id': ENT[3], 'company_id': CID, 'material_id': LATINHA, 'theoretical_qty': 480,
            'actual_qty': 498, 'unit_cost': 6.2, 'line_cost': 3087.6, 'loss_qty': 18, 'loss_reason': 'reaproveitavel', 'created_at': at}],
        'production_order_outputs': [
            {'id': '@id:t11.out.3.fardo', 'production_order_id': OP[3], 'entry_id': ENT[3], 'company_id': CID, 'material_id': FARDO, 'is_primary': True,
             'qty': 480, 'created_at': at},
            {'id': '@id:t11.out.3.chaparia', 'production_order_id': OP[3], 'entry_id': ENT[3], 'company_id': CID, 'material_id': CHAPARIA, 'is_primary': False,
             'qty': 14, 'created_at': at}],
        'production_order_workers': [
            {'id': '@id:t11.worker.3.claudio.dia', 'order_id': OP[3], 'entry_id': ENT[3], 'employee_id': CLAUDIO, 'company_id': CID, 'produced_qty': 260, 'created_at': at},
            {'id': '@id:t11.worker.3.diego.dia', 'order_id': OP[3], 'entry_id': ENT[3], 'employee_id': DIEGO, 'company_id': CID, 'produced_qty': 220, 'created_at': at}],
        'stock_movements': [
            mov('@id:t11.sm.3.latinha', LATINHA, -498, lat, at, 'Consumo de produção (lançamento)', OP[3], ENT[3]),
            mov('@id:t11.sm.3.fardo', FARDO, 480, 0, at, 'Produto de produção (lançamento)', OP[3], ENT[3]),
            mov('@id:t11.sm.3.chaparia', CHAPARIA, 14, chap, at, 'Coproduto de produção (lançamento)', OP[3], ENT[3])],
        '_patch': {
            'materials': [{'match': {'id': LATINHA}, 'set': {'current_stock': round(lat - 498, 3), 'updated_at': at}},
                          {'match': {'id': FARDO}, 'set': {'current_stock': 480, 'updated_at': at}},
                          {'match': {'id': CHAPARIA}, 'set': {'current_stock': round(chap + 14, 3), 'updated_at': at}}],
            'production_orders': [{'match': {'id': OP[3]}, 'set': {'status': 'in_progress', 'produced_qty': 480, 'total_material_cost': 3087.6,
                                                                  'cost_per_unit': 6.4325, 'updated_at': at}}],
        },
    }


def apos_cap10():
    fim = '2026-11-10T20:36:00.000Z'
    return {'_patch': {'production_orders': [{'match': {'id': OP[3]}, 'set': {
        'status': 'completed', 'completed_at': fim, 'kanban_column_id': COL_CONCLUIDA, 'client_request_id': '7d1c2a40-3b8e-4f51-9a0d-2e6f8b5c4a13',
        'updated_at': fim}}]}}


def apos_cap12():
    return {'_patch': {'companies': [{'match': {'id': CID}, 'set': {'production_block_on_insufficient_stock': True}}]}}


def apos_cap13(h):
    at = '2026-11-10T20:40:00.000Z'
    cobre, fio = round(estoque_b(h, COBRE_MEL) + 50, 3), estoque_b(h, FIO)   # o cobre mel com a #2 por cima
    return {
        'stock_movements': [
            mov('@id:t11.sm.2.cobre_mel.estorno', COBRE_MEL, -50, cobre, at, 'Estorno de produção (exclusão da OP)', OP[2], ENT[2], '@id:t11.sm.2.cobre_mel'),
            mov('@id:t11.sm.2.fio.estorno', FIO, 80, fio, at, 'Estorno de produção (exclusão da OP)', OP[2], ENT[2], '@id:t11.sm.2.fio')],
        '_remove': {
            'production_orders': [{'id': OP[2]}], 'production_order_entries': [{'id': ENT[2]}],
            'production_order_consumption': [{'production_order_id': OP[2]}], 'production_order_outputs': [{'production_order_id': OP[2]}],
            'production_order_workers': [{'order_id': OP[2]}]},
        '_patch': {'materials': [{'match': {'id': FIO}, 'set': {'current_stock': round(fio + 80, 3), 'updated_at': at}},
                                 {'match': {'id': COBRE_MEL}, 'set': {'current_stock': round(cobre - 50, 3), 'updated_at': at}}]},
    }


def main():
    h = base()
    os.makedirs(SAIDA, exist_ok=True)
    arquivos = {'inicio': inicio(h), 'apos-cap03': apos_cap03(), 'apos-cap04': apos_cap04(), 'apos-cap05': apos_cap05(), 'apos-cap06': apos_cap06(),
                'apos-cap09': apos_cap09(h), 'apos-cap10': apos_cap10(), 'apos-cap12': apos_cap12(), 'apos-cap13': apos_cap13(h)}
    for nome, d in arquivos.items():
        d = {'_doc': f'T11 · Produção: {nome} (gerado por rec/t11/t11_sementes.py; não editar à mão)', **d}
        alvo = os.path.join(SAIDA, f'{nome}.json')
        with open(alvo + '.tmp', 'w', encoding='utf8') as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
        os.replace(alvo + '.tmp', alvo)   # troca atômica: a instância pode estar lendo
        n = sum(len(v) for k, v in d.items() if isinstance(v, list))
        print(f'{nome}: {n} linhas{", _patch " + ",".join(d["_patch"]) if "_patch" in d else ""}{", _remove" if "_remove" in d else ""}')


if __name__ == '__main__':
    main()
