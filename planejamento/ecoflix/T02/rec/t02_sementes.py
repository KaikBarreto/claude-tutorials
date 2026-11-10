#!/usr/bin/env python3
"""T2 · escreve as sementes extras da aula em rec/mundo/seeds-extra/t02/ (estado de partida de cada capítulo).

Cadeia (o `seedExtra` de cada capítulo no gerar.py soma as sementes em ordem, por cima do mundo base):
  inicio      caps 0 a 3  só o Rafael: tira do mundo base a Juliana e o Marcos (a aula os cria na tela) e põe a sessão do
                          Rafael em active_sessions ("Online agora"). Escrita à mão (inicio.json), não por este script.
  apos-cap03  cap 4       + Marcos como o "Criar Usuário" do cap03 o deixa: perfil "Operador Padrão" (32 permissões), papel
                          operator, SEM permission_preset (a edge create-company-user não grava o perfil rápido), sem tela
                          inicial e sem foto (a criação não grava as duas: achado 1 do inventário).
  apos-cap04  cap 5       + Juliana como o cap04 a cria: 7 telas e 8 ações (15), papel operator.
  apos-cap05  caps 6 a 10 Marcos depois do "Atualizar" do cap05: tela inicial /caixa, foto, sem "Ver Projeção de Lucro" (31).
                          A foto é o arquivo rec/mundo/storage/avatars/marcos-antunes.jpg (t02_avatar_marcos.py): o Supabase
                          falso guarda o que se envia só na memória, e o capítulo seguinte parte desta semente.
O estado final (apos-cap05) é o do mundo base (permissões do T2 conferidas no gerar/sementes.mjs), mais a foto do Marcos.
Uso: python3 -I rec/t02/t02_sementes.py   (conferir depois de um ensaio: /__dev/state?table=user_permissions etc.)"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.join(os.path.dirname(HERE), 'mundo', 'seeds-extra', 't02')
EMPRESA = '@id:company.reciclavale'

# "Operador Padrão" do app 1.59.154 (src/config/routes.ts, PERMISSION_PRESETS), todos os módulos contratados: 12 telas + 20 ações
OPERADOR_PADRAO = [
    'screen_caixa', 'screen_historico_caixa', 'screen_pedidos', 'screen_estoque', 'screen_historico_materiais', 'screen_weighing_ticket',
    'screen_producao', 'screen_coletas', 'screen_clientes_fornecedores', 'screen_funcionarios', 'screen_agenda', 'screen_contas_pagar_receber',
    'action_register_purchase', 'action_register_sale', 'action_ticket_pesagem_compra', 'action_ticket_pesagem_venda',
    'action_ticket_pesagem_ver_valorizados', 'action_register_expense', 'action_register_income', 'action_open_cash', 'action_close_cash',
    'action_view_total_cash', 'action_use_bank_accounts', 'action_view_financial_values', 'action_view_profit_projection',
    'action_view_production_costs', 'action_view_partner_balance', 'action_adjust_partner_balance', 'action_create_bill', 'action_pay_bill',
    'action_manage_recurring', 'action_delete_bill',
]
# Juliana (plano.md do T2): 7 telas e 8 ações, na ordem em que o cap04 liga
JULIANA = [
    'screen_contas_pagar_receber', 'action_create_bill', 'action_pay_bill', 'screen_notas_fiscais', 'action_emit_nfe', 'action_emit_nfse',
    'action_view_financial_values', 'screen_dashboard', 'screen_movimentacoes_bancarias', 'action_manage_bank_accounts', 'action_reconcile_bank',
    'screen_relatorio_financeiro', 'screen_pedidos', 'screen_clientes_fornecedores', 'action_view_partner_balance',
]
assert len(OPERADOR_PADRAO) == 32 and len(set(OPERADOR_PADRAO)) == 32
assert len(JULIANA) == 15 and sum(p.startswith('screen_') for p in JULIANA) == 7


def usuario(chave, email, nome, quando, perms):
    uid = f'@id:user.{chave}'
    return {
        'profiles': [{'id': uid, 'email': email, 'full_name': nome, 'company_id': EMPRESA, 'is_active': True,
                      'created_at': quando, 'updated_at': quando}],
        'user_roles': [{'id': f'@id:role.{chave}', 'user_id': uid, 'role': 'operator', 'created_at': quando}],
        'user_permissions': [{'id': f'@id:t02.perm.{chave}.{p}', 'user_id': uid, 'permission': p, 'created_at': quando} for p in perms],
    }


def grava(nome, dados):
    os.makedirs(DEST, exist_ok=True)
    p = os.path.join(DEST, f'{nome}.json')
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print(f'{os.path.relpath(p, os.path.dirname(os.path.dirname(HERE)))}')


def main():
    grava('apos-cap03', {'_doc': 'T2: estado depois do cap03 (Marcos criado com o Operador Padrão; gerado por rec/t02/t02_sementes.py).',
                         **usuario('marcos', 'marcos.antunes@reciclavalemetais.example', 'Marcos Antunes', '@now-40m', OPERADOR_PADRAO)})
    grava('apos-cap04', {'_doc': 'T2: estado depois do cap04 (Juliana criada na mão; gerado por rec/t02/t02_sementes.py).',
                         **usuario('juliana', 'juliana.prado@reciclavalemetais.example', 'Juliana Prado', '@now-30m', JULIANA)})
    grava('apos-cap05', {
        '_doc': 'T2: estado depois do cap05 (Marcos com foto, tela inicial Caixa e sem Ver Projeção de Lucro; gerado por rec/t02/t02_sementes.py). '
                'A foto: rec/mundo/storage/avatars/marcos-antunes.jpg (rec/t02/t02_avatar_marcos.py).',
        '_patch': {'profiles': [{'match': {'id': '@id:user.marcos'},
                                 'set': {'initial_screen_path': '/caixa', 'avatar_url': '@storage:avatars/marcos-antunes.jpg', 'updated_at': '@now-20m'}}]},
        '_remove': {'user_permissions': [{'user_id': '@id:user.marcos', 'permission': 'action_view_profit_projection'}]},
    })


if __name__ == '__main__':
    main()
