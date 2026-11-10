#!/usr/bin/env python3
"""T15 · gera o mundo de partida do tutorial Funcionários (rec/fakebase/seeds-extra/t15/) e rec/t15/cadeia.json.

Estado de partida = fim do T20 (cadeia do T20 + semente final dele, `T20_FINAL`; a ordem de exibição pula o T14) + o fim do T2 (a Tatiane Ribeiro
como usuária, `t2/apos-cap10`) + `t15/inicio` (este arquivo). Arquivos gerados:
  inicio.json    os seis funcionários do T9 ficam "Informal", mensal, 5º dia útil, salário 0 (a Tatiane ainda não existe: nasce no cap. 5)
  salarios.json  o "corte" entre os caps. 5 e 6: salário dos técnicos (Rafael R$ 3.080,00 ... Paulo R$ 2.640,00)
  folhas.json    as sete folhas que o cron generate-payroll cria às 04:00 de 12/11 (cap. 11): "Folha {nome} — 2026-12", vencimento 07/12/2026,
                 categoria "Folha de Pagamento" (criada junto). A da Tatiane só sai se `apos-cap05.json` já existir (o id dela nasce no robô)
Rodar:  python3 -I rec/t15/semear.py          (semente final do T20 diferente:  T20_FINAL=t20/apos-cap12 python3 -I rec/t15/semear.py)
"""
import json
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
EXTRA = os.path.normpath(os.path.join(HERE, '..', 'fakebase', 'seeds-extra'))
OUT = os.path.join(EXTRA, 't15')
SCHEMA = json.load(open(os.path.join(HERE, '..', 'fakebase', 'schema.json'), encoding='utf8'))['tables']
EMP = '9c307966-79f1-567c-ac4d-d5fd3c1a2f40'
FAKE_NOW = '2026-11-11T09:00:00-03:00'
T20_FINAL = os.environ.get('T20_FINAL', '')

C20 = json.load(open(os.path.join(HERE, '..', 't20', 'cadeia.json'), encoding='utf8'))
BASE = list(C20['inicio'])           # já traz t20/inicio
if T20_FINAL and T20_FINAL not in BASE:
    BASE.append(T20_FINAL)

TEC = {  # id do T9 -> (nome, salário)
    '@id:t9.func.rafael': ('Rafael Lima', 3080.00), '@id:t9.func.bruno': ('Bruno Alves', 2860.00), '@id:t9.func.julia': ('Júlia Santos', 2860.00),
    '@id:t9.func.lucas': ('Lucas Ferreira', 2640.00), '@id:t9.func.marina': ('Marina Costa', 2640.00), '@id:t9.func.paulo': ('Paulo Souza', 2640.00),
}
CAT_FOLHA = '@id:t15.cat.folha'
DRE_PESSOAL = '27a5eb3c-d190-5e2e-9405-86ba4dbfd960'   # "Despesas com pessoal" (t13/inicio)


def linha_vazia(tabela):
    return {c: None for c in SCHEMA[tabela]['columns']}


def inicio():
    return {
        '_comentario': 'T15 · funcionários do T9 como "Informal", mensal, 5º dia útil, salário 0 (o corte dos salários é t15/salarios). Gerado por rec/t15/semear.py: não edite à mão.',
        '_patch': {'employees': [{'match': {'company_id': EMP}, 'set': {
            'employment_regime': 'informal', 'payment_frequency': 'monthly', 'payment_day_type': 'business', 'payment_day': 5}}]},
        # tabelas que o app lê e que começam vazias (sem isto o falso registra TABELA_SEM_SEED)
        **{t: [] for t in ('time_settings', 'org_charts', 'processes', 'employee_contracts', 'employee_movements', 'time_records', 'time_sheets', 'time_schedules', 'company_fiscal_settings')},
    }


def salarios():
    return {
        '_comentario': 'T15 · corte entre os caps. 5 e 6: salário dos técnicos (Informal, mensal, 5º dia útil). Gerado por rec/t15/semear.py.',
        '_patch': {'employees': [{'match': {'id': i}, 'set': {'salary': s}} for i, (n, s) in TEC.items()]},
    }


def folhas():
    cat = linha_vazia('financial_categories')
    cat.update({'id': CAT_FOLHA, 'company_id': EMP, 'name': 'Folha de Pagamento', 'type': 'saida', 'color': '#f59e0b', 'icon': 'Users', 'dre_group': 'opex',
                'is_system': True, 'is_active': True, 'sort_order': 0, 'dre_group_id': DRE_PESSOAL, 'created_at': '2026-11-12T07:00:00.000Z',
                'updated_at': '2026-11-12T07:00:00.000Z'})
    quem = [(i, n, s) for i, (n, s) in TEC.items()]
    arq5 = os.path.join(OUT, 'apos-cap05.json')
    if os.path.exists(arq5):
        d5 = json.load(open(arq5, encoding='utf8'))
        for e in d5.get('employees', []):
            if e.get('name') == 'Tatiane Ribeiro':
                quem.insert(0, (e['id'], 'Tatiane Ribeiro', 2800.00))
    rows = []
    for k, (eid, nome, sal) in enumerate(quem):
        r = linha_vazia('financial_transactions')
        r.update({'id': f'@id:t15.folha.{k}', 'company_id': EMP, 'transaction_type': 'saida', 'description': f'Folha {nome} — 2026-12', 'amount': sal,
                  'amount_received': 0, 'transaction_date': '2026-12-07', 'due_date': '2026-12-07', 'is_paid': False, 'category': 'Folha de Pagamento',
                  'employee_id': eid, 'payroll_period': '2026-12', 'payroll_kind': 'salary', 'created_at': '2026-11-12T07:00:00.000Z',
                  'updated_at': '2026-11-12T07:00:00.000Z'})
        rows.append(r)
    return {'_comentario': 'T15 · folhas do cron generate-payroll de 12/11 (cap. 11). Gerado por rec/t15/semear.py.', 'financial_categories': [cat], 'financial_transactions': rows}, len(rows)


def main():
    os.makedirs(OUT, exist_ok=True)
    for nome, dado in (('inicio', inicio()), ('salarios', salarios())):
        json.dump(dado, open(os.path.join(OUT, nome + '.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    f, n = folhas()
    json.dump(f, open(os.path.join(OUT, 'folhas.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    cad = {'fake_now': FAKE_NOW, 'fake_now_cap11': '2026-11-12T08:30:00-03:00', 't20_final': T20_FINAL or 'PROVISÓRIO: só t20/inicio (aguardando "T15: base pronta")',
           'base': BASE, 'inicio': BASE + ['t2/apos-cap10', 't15/inicio'],
           'nota': 'mundo do T15 = fim do T20 + fim do T2 (Tatiane como usuária) + t15/inicio; apos-capNN do T15 são cumulativos sobre essa base (salários: t15/salarios entra a partir do cap. 6; folhas: t15/folhas só nos caps. 11 e 12)'}
    json.dump(cad, open(os.path.join(HERE, 'cadeia.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print(f'seeds-extra/t15/{{inicio,salarios,folhas}}.json e rec/t15/cadeia.json gerados (T20_FINAL = {T20_FINAL or "provisório"}); folhas: {n}')


if __name__ == '__main__':
    main()
