

def passar_pela_barra(c, at, label='a barra de cinco etapas', passo=0.45):
    """o cursor passa pelos nomes das cinco etapas do assistente"""
    for k, nome in enumerate(['Dados do contrato', 'Escopo técnico', 'Agenda', 'Operação e cobrança', 'Revisão']):
        c.hover(SEL(f'{DLG} button', hasText=nome, nth=0), 0.1, at=round(at + k * passo, 2), label=f'{label}: {nome}')


def abrir_assistente(c, at, label='Novo Contrato'):
    c.click(BTN('Novo Contrato'), at=at, label=label)
    c.waitfor(text='Dados do contrato', timeout=15)


def escolher_cliente(c, nome, busca, at_abre, at_busca, at_escolhe):
    c.click(TXT('Selecione o cliente', within=DLG), at=at_abre, label='abre a lista de Cliente')
    c.type({'placeholder': 'Buscar cliente...'}, busca, at=at_busca, cps=14, label=f'busca "{busca}"')
    c.click(CLIENTE(nome), at=at_escolhe, label=f'escolhe {nome}')


NOME_CONTRATO = SEL(f'{DLG} input', nth=0)
CHAVE_PMOC = SEL(f'{DLG} [role=switch]', nth=0)
PROXIMO = BTN('Próximo')


def cap03():
    """Um contrato comum: Novo Contrato > Dados > Escopo técnico (Hi-Wall do colégio) > Agenda (Trimestral) > Operação e cobrança > Revisão > Criar Contrato."""
    c = Cap(3, pace=0.5, start=(760, 420), prewarm=PREWARM, setup=SETUP_LISTA)
    c.mark(1)
    abrir_assistente(c, c.A(1, 'Clico', 1.6))
    c.mark(2)
    c.type(NOME_CONTRATO, 'Manutenção preventiva trimestral - Colégio Monte Verde', at=c.A(2, 'escrevo', 0.9), cps=22, label='Nome do Contrato')
    escolher_cliente(c, 'Colégio Monte Verde', 'Colégio', c.A(2, 'Cliente', 1.0), c.A(2, 'escolho', 0.3), c.A(2, 'colégio.', 0.6))
    c.hover(CHAVE_PMOC, 1.4, at=c.A(2, 'chave', 0.9), label='chave É um contrato PMOC? (desligada)')
    passar_pela_barra(c, c.A(2, 'cinco', 0.7))
    c.click(PROXIMO, at=round(c.L(3) - 1.3, 2), label='Próximo (Escopo técnico)')
    c.mark(3)
    c.waitfor(text='Equipamentos e escopo', timeout=10)
    c.click(BTN('Adicionar equipamento sem ambiente'), at=c.A(3, 'Adicionar', 0.9), label='Adicionar equipamento sem ambiente')
    c.waitfor(text='Adicionar equipamento ao contrato', timeout=10)
    c.click(TXT('Hi-Wall 18.000 BTUs - Sala dos professores'), at=c.A(3, 'Hi-Wall', 0.9), label='marca o Hi-Wall 18.000 BTUs da sala dos professores')
    c.click(BTN('Adicionar 1 equipamento'), at=c.A(3, 'professores.', 0.8), label='Adicionar 1 equipamento')
    c.waitfor(text='Equipamentos não atribuídos', timeout=10)
    c.click(PROXIMO, at=round(c.L(4) - 1.3, 2), label='Próximo (Agenda)')
    c.mark(4)
    c.waitfor(text='Defina a cadência', timeout=10)
    c.click(BTN('Trimestral'), at=c.A(4, 'Trimestral', 0.9), label='atalho Trimestral')
    c.click(SEL(f'{DLG} button', hasText='/2026', nth=0), at=c.A(4, 'Escolho', 0.9), label='Data de Início (abre o calendário)')
    c.click(SEL(f'{POP} button', nth=1), at=c.A(4, 'Data', 1.0), label='próximo mês no calendário')
    c.click({'role': 'gridcell', 'name': '15', 'exact': True}, at=c.A(4, 'Início', 0.4), label='escolhe o dia 15')
    c.hover(PD('Prévia das datas'), 2.2, at=c.A(4, 'Prévia', 0.8), label='Prévia das datas')
    c.click(PROXIMO, at=round(c.L(5) - 1.3, 2), label='Próximo (Operação e cobrança)')
    c.mark(5)
    c.waitfor(text='Técnicos Executores', timeout=10)
    c.ev("(()=>JSON.stringify({dump:'executores', html:(document.querySelector('[data-contract-validation=executors]')||{}).innerHTML?.slice(0,900)}))()", label='dump executores')
    c.click(SEL(f'{DLG} [data-contract-validation=executors] button', nth=0), at=c.A(5, 'Executor', 0.9), label='abre Técnicos Executores')
    c.click({'selector': f'{POP} [cmdk-item], {POP} [role=option]', 'hasText': 'Rafael Lima'}, at=c.A(5, 'Rafael', 0.9), label='marca Rafael Lima')
    c.press('Escape', at=c.A(5, 'Lima.', 0.2), label='fecha a lista de técnicos')
    c.click(SEL(f'{DLG} button[role=combobox]', hasText='Selecione', nth=0), at=c.A(5, 'Tipo', 0.9), label='abre Tipo de Serviço')
    c.click(OPT('Manutenção Preventiva', exact=False), at=c.A(5, 'Preventiva,', 0.9), label='Manutenção Preventiva')
    # o Checklist Padrão mora na etapa anterior (Escopo técnico): volta pela barra, escolhe e retorna
    c.click(SEL(f'{DLG} button', hasText='Escopo técnico', nth=0), at=c.A(5, 'Checklist', 1.4), label='volta ao Escopo técnico (onde mora o Checklist Padrão)')
    c.click(SEL(f'{DLG} button[role=combobox]', hasText='Nenhum', nth=0), at=c.A(5, 'Padrão,', 0.4), label='abre Checklist Padrão')
    c.click(OPT('Manutenção preventiva de split', exact=False), at=c.A(5, 'manutenção', 0.7), label='Manutenção preventiva de split')
    c.click(SEL(f'{DLG} button', hasText='Operação e cobrança', nth=0), at=c.A(5, 'tutorial', 0.9), label='volta a Operação e cobrança')
    c.hover(P('Contrato Ativo', within=DLG), 1.6, at=c.A(5, 'Ativo', 0.9), label='chave Contrato Ativo')
    c.mark(6)
    c.rolar(520, at=c.A(6, 'embaixo,', 0.9), label='desce até a Configuração financeira', ponto=(760, 480))
    c.hover(PD('Já gerar as parcelas a receber'), 2.2, at=c.A(6, 'Já', 0.9), label='Já gerar as parcelas a receber (desligado)')
    c.click(PROXIMO, at=round(c.L(7) - 1.3, 2), label='Próximo (Revisão)')
    c.mark(7)
    c.waitfor(text='Revisão do Contrato', timeout=10)
    c.hover(PD('Revisão do Contrato'), 1.6, at=c.A(7, 'confiro', 0.9), label='Revisão do Contrato')
    c.click(BTN('Criar Contrato'), at=c.A(7, 'Criar', 0.9), label='Criar Contrato')
    c.waitfor(text='Contrato criado', timeout=20)
    c.hover(P('Pronto', within='body'), 0.2, at=c.A(7, 'Pronto:', 0.9), label='aviso de contrato criado', optional=True)
    c.fim()
    return c
