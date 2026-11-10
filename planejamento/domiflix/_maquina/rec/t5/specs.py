#!/usr/bin/env python3
"""T5 · especificação de edição por capítulo -> t5/edit/caps/specs.json.

Cada capítulo: título/kicker da vinheta, zooms e destaques que apontam para os RÓTULOS (`label`) dos passos do robô
(rec/t5/gerar.py), avisos ancorados numa palavra da fala e ilustrações. Formato e regras: docs/05-edicao.md.
Uso: python3 rec/t5/specs.py   (reescreve t5/edit/caps/specs.json com todos os capítulos definidos aqui)
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, '..', '..', 't5', 'edit', 'caps', 'specs.json'))
OS_ = 'Ordens de Serviço'
ILU_POSICAO = os.path.normpath(os.path.join(HERE, '..', '..', 't5', 'edit', 'out', 'ilu_posicao'))   # sequência PNG da ilustração do cap. 16 (t5/edit/ilustra_posicao.py)


def z(de, ate=None, fim='+0.4', min_w=1300, **kw):
    d = {'de': de, 'fim': fim, 'min_w': min_w, **kw}
    if ate: d['ate'] = ate
    return d


def sp(passo, antes=0.8, dur=1.6, rotulo=None):
    d = {'passo': passo, 'antes': antes, 'dur': dur}
    if rotulo: d['rotulo'] = rotulo
    return d


SPECS = {
    '00': {'titulo': 'Abertura', 'kicker': 'Introdução', 'sem_titulo': True,
           'zooms': [z('abre o grupo Operacional', 'menu: Mapa e Rastreamento', '+0.6', 1300)],
           'callouts': [{'palavra': [2, 'Tipos'], 'dur': 5.0, 'texto': 'Antes: Tipos de Serviço, Tipos de Tarefa e Checklists', 'pos': 'bottom'}]},
    '01': {'titulo': 'A tela de Ordens de Serviço', 'kicker': OS_,
           'spots': [sp('menu: Operacional, Ordens de Serviço', 0.6, 1.6, OS_)],
           'zooms': [z('aba Ordens de Serviço', 'aba NPS e Satisfação', '+0.5', 1500),
                     z('cartão OS Abertas', 'cartão Próximos 7 dias', '+0.4', 1500),
                     z('filtro de período', None, '+0.8', 1300),
                     z('código do cartão: prefixo, ano e número', 'código do cartão: MP-2026-12', '+0.8', 1300),
                     z('coluna OS', 'coluna Ações', '+0.5', 1500)]},
    '02': {'titulo': 'Abrindo uma nova OS', 'kicker': OS_,
           'spots': [sp('Nova OS', 1.0, 1.6, 'Nova OS')],
           'zooms': [z('as quatro etapas', 'etapa Cliente e Serviço', '+0.5', 1300),
                     z('aviso: o cliente é criado com estes dados', None, '+0.5', 1300),
                     z('o serviço principal, com a cor', None, '+0.8', 1300),
                     z('campos do endereço de serviço', None, '+0.6', 1300)]},
    '03': {'titulo': 'Orçamento e rascunho', 'kicker': OS_,
           'zooms': [z('etapa Orçamento', 'materiais', '+0.5', 1300),
                     z('Qtd: 1', 'Valor Unit.: 180', '+0.5', 1300),
                     z('Total para faturamento', None, '+0.6', 1300)]},
    '04': {'titulo': 'Equipamentos e checklists', 'kicker': OS_,
           'zooms': [z('o aparelho marcado', 'serviço vinculado a equipamento', '+0.5', 1300),
                     z('serviços neste equipamento', 'o checklist entrou sozinho', '+0.5', 1300),
                     z('Checklists avulsos', None, '+0.8', 1300)]},
    '05': {'titulo': 'Agendamento e detalhes', 'kicker': OS_,
           'zooms': [z('Revisão do escopo da OS', 'serviços e checklists de cada aparelho', '+0.5', 1300),
                     z('técnicos e equipes no mesmo seletor', None, '+0.5', 1300),
                     z('Período do atendimento', None, '+0.4', 1300),
                     z('Gerar Pesquisa de Satisfação', 'pesquisa ligada', '+0.5', 1300),
                     z('cartão MP-2026-16 na coluna Pendente', None, '+0.8', 1300)]},
    '06': {'titulo': 'Recorrência', 'kicker': OS_,
           'spots': [sp('liga a Recorrência', 0.9, 1.8, 'Recorrência')],   # o passo `type noClick` do clicar_fixo guarda o retângulo da chave
           'zooms': [z('campo Frequência', 'campo Até', '+0.5', 1300),
                     z('dia 3 de fevereiro', 'prévia: serão criadas 4 OS', '+0.8', 1300),
                     z('cartão da série: novembro', 'cartão da série: fevereiro', '+0.8', 1300)]},
    '07': {'titulo': 'Acompanhando no Kanban', 'kicker': OS_,
           'zooms': [z('arrasta MC-2026-11 de Pendente para Em Andamento', 'o cartão já está em Em Andamento', '+0.8', 1400),
                     z('o "+" da coluna Pendente', None, '+0.6', 1000),
                     z('cartão Cliente', 'cartão Check-in / Check-out', '+0.5', 1300),
                     z('Preencher OS', None, '+0.6', 1300),
                     z('Manter o preenchimento', 'Apagar o preenchimento', '+0.4', 1300)]},
    '08': {'titulo': 'Status, filtros e busca', 'kicker': OS_,
           'zooms': [z('nome e cor', None, '+0.6', 1300),
                     z('filtros pausados', None, '+0.8', 1300)]},
    '09': {'titulo': 'Concluir e faturar', 'kicker': OS_,
           'zooms': [z('a pergunta sobre a receita', 'Valor da OS sugerido', '+0.5', 1300),
                     z('Faturar OS', None, '+1.0', 1300)]},
    '10': {'titulo': 'Chamados e relatório', 'kicker': OS_,
           'zooms': [z('aba Chamados (cursor)', 'aba Relatório (cursor)', '+0.4', 1500),
                     z('origem: Portal do Cliente', None, '+0.6', 1300),
                     z('Abrir chamado', None, '+0.6', 1300),
                     z('coluna Chamados do Portal', 'o chamado vira uma OS normal', '+0.6', 1300),
                     z('KPI Total de OS', 'KPI Faturamento', '+0.6', 1500),
                     z('gráfico por status', 'gráfico por tipo de serviço', '+0.5', 1300),
                     z('gráfico por dia da semana', 'Concluídas no prazo', '+0.8', 1300)]},
    '11': {'titulo': 'Satisfação do cliente', 'kicker': OS_,
           'zooms': [z('KPI NPS Score', 'KPI Taxa de Resposta', '+0.6', 1500),
                     z('gráfico Distribuição NPS', 'Detratores', '+0.5', 1300),
                     z('Ranking de Técnicos', 'selo Atenção', '+0.5', 1300),
                     z('Feed de Feedbacks', None, '+1.0', 1300),
                     z('Pergunta da escala', 'critério Profissionalismo', '+0.4', 1300),
                     z('Avaliação no Google', 'link da avaliação do Google', '+0.6', 1300)]},
    '12': {'titulo': 'As visões da Agenda', 'kicker': 'Agenda',
           'zooms': [z('visão Mês', 'feriado: Finados', '+0.5', 1300),
                     z('visão Semana', 'Hoje', '+0.5', 1300),
                     z('seção Atrasado', None, '+0.8', 1300),
                     z('filtro Técnico', 'filtro Tipo', '+0.5', 1300),
                     z('legenda: ver todos os tipos', None, '+0.8', 1300)]},
    '13': {'titulo': 'Criar e reagendar', 'kicker': 'Agenda',
           'zooms': [z('opção Ordem de Serviço', 'opção Tarefa', '+0.5', 1300),
                     z('a tarefa no dia 9', 'uma OS no mesmo dia', '+0.6', 1300),
                     z('arrasta a OS #16 da terça para a quarta', 'a OS #16 agora na quarta', '+0.8', 1300)]},
    '14': {'titulo': 'Pausadas, busca e resumo', 'kicker': 'Agenda',
           'zooms': [z('a OS pausada na lista', 'o tempo que está parada', '+0.5', 1300),
                     z('resultado: o número da OS', 'resultado: o técnico', '+0.5', 1300),
                     z('Responsáveis', 'Linha do tempo', '+0.5', 1300),
                     z('menu Ações', 'Ações: Copiar link de acompanhamento', '+0.8', 1300),
                     z('botão Preencher OS', None, '+0.6', 1300)]},
    '15': {'titulo': 'Montando uma equipe', 'kicker': 'Equipes',
           'zooms': [z('cor da equipe', 'Lucas Ferreira', '+0.6', 1300),
                     z('a seção Equipes', 'os dois membros marcados', '+0.6', 1300),
                     z('Quando começa: 14:00', None, '+0.8', 1300),
                     z('Equipe Alfa no resumo', None, '+0.8', 1300)]},
    '16': {'titulo': 'Onde está cada técnico', 'kicker': 'Mapa ao Vivo',
           'zooms': [z('marcador do Bruno', 'marcador do Lucas', '+0.6', 1300),
                     z('legenda: A Caminho', 'legenda: Check-out', '+0.5', 1300),
                     z('popup: OS vinculada', 'a linha até o destino do cliente', '+0.6', 1300),
                     z('os deslocamentos do dia', 'Tempo em campo', '+0.6', 1300)],
           # o celular do técnico envia a posição e ela aparece no Mapa: 13,2 s a partir de "A posição vem do celular dele" (2,4 s)
           'ilustracoes': [{'at': 2.4, 'dur': 13.2, 'src': ILU_POSICAO, 'box': [166, 44, 1587, 992], 'scale_in': 0.0}],
           # sob a ilustração a câmera fica parada: os cliques de menu (sob a ilustração) puxariam um zoom 1,3x que aparece em volta do cartão
           'repouso': [[1.6, 16.6]]},
    '17': {'titulo': 'Recapitulando', 'kicker': 'Resumo',
           'callouts': [{'palavra': [2, 'No'], 'dur': 6.0, 'texto': 'Próximo: O técnico em campo', 'pos': 'bottom'}]},
}

# ---------------------------------------------------------------- avisos na tela ("Dica: ...") do plano (T05/plano.md), por palavra da fala
# `linha` = 1ª linha = 1; o montar_cap.py procura pela linha de índice 0 (linha - 1) e pela palavra exata (sem pontuação nas pontas)
def dica(linha, palavra, texto, dur=4.5):
    return {'palavra': [linha - 1, palavra], 'dur': dur, 'texto': 'Dica: ' + texto, 'pos': 'bottom'}


DICAS = {
    '01': [dica(4, 'dica:', 'Kanban ou Lista, a escolha fica salva neste navegador', 3.4)],
    '02': [dica(2, 'cadastro', 'cliente avulso já nasce no cadastro de clientes'),
           dica(5, 'vale', 'o endereço de serviço vale só para esta OS', 4.2)],
    '03': [dica(2, 'Preço', 'o valor sugerido vem do Preço padrão do serviço'),
           dica(3, 'rascunho', 'o rascunho guarda cliente, serviços e valores')],
    '04': [dica(2, 'Olha:', 'o checklist acompanha o serviço do equipamento')],
    '05': [dica(2, 'Técnicos', 'técnicos e equipes ficam no mesmo seletor'),
           dica(5, 'Satisfação', 'a pesquisa segue as Configurações de NPS')],
    '06': [dica(2, 'prévia', 'a prévia diz quantas OS serão criadas antes de salvar')],
    '07': [dica(1, 'arrastar', 'arrastar muda o status na hora'),
           dica(4, 'Resetar', 'Resetar OS devolve a OS para Agendada')],
    '08': [dica(3, 'olha', 'a busca olha todas as OS, mesmo fora do período', 3.8)],
    '09': [dica(1, 'houve', 'ao concluir, o sistema pergunta se houve receita')],
    '10': [dica(1, 'chegam', 'pedidos feitos pelos portais chegam em Chamados')],
    '11': [dica(3, 'critérios', 'os critérios de estrela são seus; edite em Configurações')],
    '12': [dica(1, 'computador', 'no celular a Agenda abre em Dia')],
    '13': [dica(2, 'compromisso', 'tarefa é interna; só a OS vai pro cliente'),
           dica(3, 'hora,', 'reagendar vale na hora, sem confirmação')],
    '14': [dica(1, 'continua', 'OS pausada continua à vista até ser retomada')],
    '15': [dica(1, 'módulo', 'Equipes ficam em Funcionários, no módulo RH'),
           dica(3, 'membros', 'marcar a equipe marca todos os membros')],
    '16': [dica(2, 'posição', 'o técnico aparece quando o celular envia a posição', 4.0)],   # no mapa; na ilustração (início) o aviso cobria a legenda dela
}
for _k, _v in DICAS.items():
    SPECS[_k].setdefault('callouts', []).extend(_v)


if __name__ == '__main__':
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    old = {}
    if os.path.exists(OUT):
        old = json.load(open(OUT, encoding='utf8'))
    # descarta o modelo copiado ("_leia" e capítulos de exemplo que não estão aqui)
    out = {k: v for k, v in SPECS.items()}
    with open(OUT, 'w', encoding='utf8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print('specs.json:', ', '.join(sorted(out)), '->', os.path.relpath(OUT, HERE))
