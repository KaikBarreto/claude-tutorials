

# ================================================================ capítulos
def cap_novo(n, **kw):
    return Cap(n, pace=0.5, start=(760, 420), **kw)


def cap00():
    """Abertura: Dashboard, menu lateral, grupo Gestão, "Funcionários (RH)"."""
    c = cap_novo(0, setup=SETUP_DASH)
    c.mark(1)
    c.hover(LINK('Agenda'), 0.1, at=0.3, label='o cursor passa pelo menu lateral')
    c.click(BTN('Gestão'), at=c.A(1, 'cadastro', 1.5), label='abre o grupo Gestão do menu')   # 1º clique do capítulo: ~2,5 s (app ainda carregando)
    c.click(MENU_FUNC, at=c.A(1, 'dinheiro', 0.9), label='abre Funcionários')
    c.waitfor(text='Lista de Funcionários', timeout=20)
    c.mark(2)
    c.hover(P('Funcionários (RH)'), 1.0, at=c.A(2, 'Com', 0.2), label='o cabeçalho Funcionários (RH)')
    c.mark(3)
    c.hover(MENU_FUNC, 1.2, at=c.A(3, 'item', 0.9), label='o item Funcionários (RH) do menu, em Gestão')
    c.mark(4)
    c.hover(P('Funcionários (RH)'), 1.0, at=c.A(4, 'Vamos', 0.9), label='volta ao cabeçalho')
    c.fim()
    return c


def cap01():
    """A tela de Funcionários: abas da lateral, lista com os seis técnicos."""
    c = cap_novo(1, setup=SETUP_FUNC)
    c.mark(1)
    c.hover(ABA_FUNC('Funcionários'), 0.5, at=c.A(1, 'Funcionários', 0.9), label='aba Funcionários')
    c.hover(ABA_FUNC('PJ/MEI'), 0.6, at=c.A(1, 'PJ', 0.9), label='aba PJ/MEI')
    c.mark(2)
    c.hover(ABA_FUNC('Equipes'), 0.6, at=c.A(2, 'Equipes', 0.9), label='aba Equipes')
    c.hover(ABA_FUNC('Controle de Ponto'), 0.6, at=c.A(2, 'Controle', 0.9), label='aba Controle de Ponto')
    c.mark(3)
    c.hover(ABA_FUNC('Perfil Comportamental'), 0.5, at=c.A(3, 'ferramentas', 0.9), label='aba Perfil Comportamental')
    c.hover(ABA_FUNC('Organograma'), 0.4, label='aba Organograma')
    c.hover(ABA_FUNC('Fluxograma'), 0.4, label='aba Fluxograma')
    c.mark(4)
    c.hover(P('Bruno Alves'), 1.0, at=c.A(4, 'lista', 0.9), label='a lista de funcionários')
    c.confere('main', ['Lista de Funcionários', 'Bruno Alves', 'Júlia Santos', 'Lucas Ferreira', 'Marina Costa', 'Paulo Souza', 'Rafael Lima',
                       'Selecione um funcionário', 'Técnico de refrigeração'], 'a lista tem os seis técnicos e nenhuma ficha aberta')
    c.mark(5)
    c.hover(NOVO_FUNC, 0.9, at=c.A(5, 'bora', 0.9), label='botão Novo Funcionário')
    c.fim()
    return c


def cap02():
    """Os dados da funcionária: janela "Novo Funcionário", aba Dados (o e-mail mora na aba Acesso desde a 1.38.19)."""
    c = cap_novo(2, setup=SETUP_FUNC)
    c.mark(1)
    c.hover(P('Lista de Funcionários'), 0.3, at=0.3, label='o cursor passa pela lista')
    c.click(NOVO_FUNC, at=c.A(1, 'cadastro', 1.0), label='Novo Funcionário')
    c.waitfor(text='Nome Completo', timeout=10)
    c.mark(2)
    for palavra, nome in [('Dados,', 'Dados'), ('Pagamento,', 'Pagamento'), ('Acesso,', 'Acesso'), ('Ponto', 'Ponto eletrônico'), ('Perfil.', 'Perfil')]:
        c.hover(ABA_FORM(nome), 0.15, at=c.A(2, palavra, 0.9), label=f'aba {nome}')
    c.hover(FOTO, 1.2, at=c.A(2, 'foto', 0.9), label='foto vazia (opcional)')
    c.mark(3)
    # sem o "e-mail" na fala (1.38.21), telefone e cargo ficam a ~1 s um do outro: a cadeia começa mais cedo (nome 1,8 s antes da palavra)
    c.type(CAMPO_NOME, 'Tatiane Ribeiro', at=c.A(3, 'nome', 1.8), cps=30, label='Nome Completo')
    c.type(CAMPO_CPF, '41837290687', at=c.A(3, 'CPF,', 1.4), cps=30, label='CPF')
    c.type(CAMPO_TEL, '2130001008', at=c.A(3, 'telefone', 1.4), cps=30, label='Telefone')
    c.type(CAMPO_CARGO, 'Assistente administrativa', at=c.A(3, 'cargo,', 1.3), cps=30, label='Cargo')
    c.mark(4)
    c.click(CAMPO_END, at=c.A(4, 'endereço', 1.0), label='campo Endereço')
    c.colar('Rua Gavião Peixoto, 120, apto 302, Icaraí, Niterói - RJ', at=c.A(4, 'endereço', 0.1), label='cola o endereço')
    c.click(DATA_ADM, at=c.A(4, 'data', 0.9), label='abre o calendário da Data de Admissão')
    c.click(DIA(3), at=c.A(4, 'admissão.', 0.9), label='escolhe o dia 3 de novembro')
    c.mark(5)
    c.type(CAMPO_PIX, 'tatiane.ribeiro@glacialcold.example', at=c.A(5, 'chave', 0.9), cps=22, label='Chave PIX')
    c.confere_campos(['Tatiane Ribeiro', '418.372.906-87', '(21) 3000-1008', 'Assistente administrativa', 'Rua Gavião Peixoto, 120, apto 302, Icaraí, Niterói - RJ', 'tatiane.ribeiro@glacialcold.example'], 'campos da aba Dados')
    c.confere('dlg', ['03/11/2026'], 'Data de Admissão 03/11/2026')
    c.fim()
    return c


def cap03():
    """Salário e contrato: aba Pagamento, calculadora do custo mensal, regime CLT, CBO, matrícula, vale-transporte."""
    c = cap_novo(3, setup=setup_dados())
    c.mark(1)
    c.click(ABA_FORM('Pagamento'), at=c.A(1, 'Pagamento.', 0.9), label='aba Pagamento')
    c.type(CAMPO_SAL, '280000', at=c.A(1, 'dois', 1.1), cps=14, label='Salário R$ 2.800,00')
    c.mark(2)
    c.hover({'text': 'Custo mensal total', 'within': DLG}, 0.8, at=c.A(2, 'custo', 0.9), label='Custo mensal total')
    c.click(BTN('Calcular', within=DLG), at=c.A(2, 'Calcular', 0.9), label='Calcular')
    c.waitfor(text='Calcular Custo Mensal', timeout=10)
    c.type(CAMPO_TRANSP, '22000', at=c.A(2, 'benefícios,', 1.3), cps=14, label='Transporte R$ 220,00')
    # fase 2: o cursor leva ~1,4 s até o "Custo Total Mensal" (janela da calculadora): sai logo depois da digitação, e o Aplicar pousa no "Aplico"
    c.hover({'text': 'Custo Total Mensal'}, 0.5, at=c.A(2, 'como', 0.9), label='Custo Total Mensal e Hora Homem')
    c.confere('dlg', ['Calcular Custo Mensal', 'Custo Total Mensal', 'Hora Homem'], 'a calculadora mostra o custo total e a hora homem')
    c.mark(3)
    c.click(APLICAR, at=c.A(3, 'Aplico,', 0.6), label='Aplicar o custo')
    c.waitfor(gone={'text': 'Calcular Custo Mensal'}, timeout=8)
    c.confere_campos(['R$ 2.800,00'], 'salário R$ 2.800,00 e custo mensal preenchido')
    c.mark(4)
    c.hover({'text': 'Regime', 'within': DLG, 'exact': True}, 0.6, at=c.A(4, 'regime.', 0.9), label='Regime')
    c.click(BTN('CLT', within=DLG), at=c.A(4, 'CLT.', 0.9), label='CLT')
    c.mark(5)
    c.type(CAMPO_CBO, '4110-10', at=c.A(5, 'CBO', 1.0), cps=22, label='CBO')
    c.type(CAMPO_MAT, '00008', at=c.A(5, 'matrícula', 1.0), cps=22, label='Matrícula')
    c.hover({'text': 'Dependentes (IRRF)', 'within': DLG}, 0.8, at=c.A(5, 'dependentes', 0.9), label='Dependentes (IRRF)')
    c.mark(6)
    c.click(BTN('Sim', within=DLG), at=c.A(6, 'vale-transporte', 0.9), label='Vale-transporte Sim')
    c.type({'selector': f"{DLG} div:has(> label:has-text('Valor mensal do VT')) input"}, '22000', at=c.A(6, 'duzentos', 1.1), cps=14, label='Valor mensal do VT')
    c.confere('dlg', ['Valor mensal do VT', 'CLT', 'CBO', 'Matrícula', 'Dependentes (IRRF)'], 'campos CLT e VT na tela')
    c.fim()
    return c


def cap04():
    """O dia do pagamento: Configuração de Pagamento (mensal, dia útil, 5º dia útil) e a dica."""
    c = cap_novo(4, setup=setup_pagamento())
    c.mark(1)
    c.ev(ROLA_DLG % 420, at=0.1, label='desce até a Configuração de Pagamento')
    c.hover({'text': 'Configuração de Pagamento', 'within': DLG}, 1.0, at=c.A(1, 'configuração', 0.9), label='Configuração de Pagamento')
    c.mark(2)
    c.click(COMBO('Mensal'), at=c.A(2, 'pagar', 0.9), label='abre Frequência (Mensal, Quinzenal, Semanal)')
    c.click(OPT('Mensal'), at=c.A(2, 'semana.', 0.7), label='fica em Mensal')
    c.mark(3)
    c.hover({'selector': f"{DLG} div:has(> label:text-is('N° dia útil do mês')) input"}, 0.9, at=c.A(3, 'quinto', 0.9), label='N° dia útil do mês (5)')
    c.click(COMBO('Dia útil'), at=c.A(3, 'corrido', 1.3), label='abre Tipo de dia (Dia útil, Dia corrido)')
    c.click(OPT('Dia útil'), at=c.A(3, 'mês.', 0.6), label='volta para Dia útil')
    c.mark(4)
    c.hover({'text': 'Valor da folha aparece automaticamente', 'within': DLG}, 1.4, at=c.A(4, 'dica:', 0.9), label='a dica da folha automática')
    c.confere('dlg', ['Frequência', 'Mensal', 'Tipo de dia', 'Dia útil', 'N° dia útil do mês', 'Valor da folha aparece automaticamente em Contas a Pagar conforme essa configuração.'], 'configuração de pagamento na tela')
    c.fim()
    return c


def cap05():
    """Acesso ao sistema (fala nova, 1.38.21; voz `T15 emendas 1.38.21`): aba Acesso SEM vínculo, e-mail, liga "Criar acesso ao sistema"
    (Papel no sistema e Permissões), desliga, vincula a Tatiane, Criar Funcionário."""
    c = cap_novo(5, setup=setup_acesso())
    CHAVE_ACESSO = {'role': 'switch', 'name': 'Criar acesso ao sistema', 'within': DLG}
    c.mark(1)
    c.click(ABA_FORM('Acesso'), at=c.A(1, 'aba', 0.9), label='aba Acesso')
    c.hover(CAMPO_EMAIL, 1.5, at=c.A(1, 'e-mail', 0.9), label='e-mail dela, que serve de login')
    c.confere_campos(['tatiane.ribeiro@glacialcold.example'], 'e-mail preenchido na aba Acesso')
    c.mark(2)
    c.hover({'text': 'Criar acesso ao sistema', 'within': DLG, 'exact': True}, 1.0, at=c.A(2, 'Criar', 0.9), label='Criar acesso ao sistema')
    c.click(CHAVE_ACESSO, at=c.A(2, 'Ligado,', 1.1), label='liga Criar acesso ao sistema')
    c.confere('dlg', ['Papel no sistema', 'Permissões'], 'ligada, a chave mostra Papel no sistema e Permissões')
    c.hover({'text': 'Papel no sistema', 'within': DLG}, 2.0, at=c.A(2, 'Papel', 0.9), label='Papel no sistema e Permissões')
    c.click(CHAVE_ACESSO, at=c.A(2, 'desligo', 0.9), label='desliga Criar acesso ao sistema')
    c.confere_ausente('dlg', 'Papel no sistema', 'desligada, a chave esconde Papel no sistema e Permissões (nenhum acesso criado)', espera=1.5)
    c.click({'selector': f"{DLG} button[role=combobox]", 'nth': 0}, at=c.A(2, 'vinculo:', 0.9), label='abre a lista de usuários')
    c.click(OPT('Tatiane Ribeiro'), at=c.A(2, 'nome', 0.9), label='escolhe Tatiane Ribeiro')
    c.confere('dlg', ['Usuário vinculado: Tatiane Ribeiro'], 'usuária vinculada')
    c.mark(3)
    c.click(BTN('Criar Funcionário'), at=c.A(3, 'Funcionário.', 0.9), label='Criar Funcionário')
    c.waitfor(gone={'role': 'dialog'}, timeout=15)
    c.confere('body', ['Funcionário criado!'], 'aviso Funcionário criado!')
    c.confere('main', ['Tatiane Ribeiro', 'Assistente administrativa'], 'a Tatiane entrou na lista')
    c.fim()
    return c


def cap06():
    """Vale, bônus e falta do Rafael: ficha, três janelas de movimentação, saldo atual."""
    c = cap_novo(6, setup=SETUP_FUNC)
    c.mark(1)
    c.hover(FUNC('Tatiane Ribeiro'), 0.8, at=c.A(1, 'Tatiane', 0.9), label='a lista agora tem a Tatiane')
    c.hover(FUNC('Bruno Alves'), 0.8, at=c.A(1, 'salário', 0.9), label='salário de cada técnico na lista')
    c.confere('main', ['R$ 3.080,00', 'R$ 2.860,00', 'R$ 2.640,00', 'R$ 2.800,00', 'Tatiane Ribeiro'], 'a lista mostra o salário de cada um (Tatiane R$ 2.800,00; técnicos R$ 2.640 a 3.080)')
    c.mark(2)
    c.click(FUNC('Rafael Lima'), at=c.A(2, 'Rafael,', 0.9), label='Rafael Lima')
    c.hover(P('Movimentações'), 1.0, at=c.A(2, 'movimentações,', 0.9), label='faixa Movimentações')
    c.hover(P('Saldo atual'), 1.2, at=c.A(2, 'saldo', 0.9), label='salário e saldo atual')
    c.confere('main', ['Rafael Lima', 'Informal', 'Vale', 'Bônus', 'Falta', 'Pagamento', 'Salário', 'R$ 3.080,00', 'Saldo atual'], 'ficha do Rafael: salário R$ 3.080,00')
    c.mark(3)
    c.click(MOV('Vale'), at=c.A(3, 'Vale,', 0.9), label='Vale')
    c.click(COMBO('Caixa'), at=c.A(3, 'conta', 0.9), label='abre "De qual conta sai o vale?"')
    c.click(OPT('Caixa (em dinheiro)'), at=c.A(3, 'caixa,', 0.9), label='escolhe Caixa (em dinheiro)')
    c.type(MOEDA(0), '30000', at=c.A(3, 'valor.', 2.0), cps=14, label='valor R$ 300,00')
    c.click(TEXTAREA, at=c.A(3, 'valor.', 0.8), label='campo Descrição')
    c.colar('Adiantamento', at=c.A(3, 'valor.', 0.5), label='descrição Adiantamento')
    c.confere('dlg', ['Registrar Vale', 'Saldo atual: R$ 3.080,00', 'De qual conta sai o vale?', 'Caixa (em dinheiro)'], 'janela Registrar Vale com saldo R$ 3.080,00')
    c.mark(4)
    c.click(BTN('Registrar Vale'), at=c.A(4, 'Registrar', 1.0), label='Registrar Vale')
    c.confere('body', ['Vale registrado!'], 'aviso Vale registrado!')
    c.waitfor(gone={'role': 'dialog'}, timeout=10)
    c.hover(P('Vales'), 1.2, at=c.A(4, 'caixa', 0.9), label='Vales na ficha')
    c.mark(5)
    c.click(MOV('Bônus'), at=c.A(5, 'bônus', 0.9), label='Bônus')
    c.type(MOEDA(0), '15000', at=c.A(5, 'cento', 1.2), cps=14, label='valor R$ 150,00')
    c.click(TEXTAREA, at=c.A(5, 'cinquenta', 0.9), label='campo Descrição')
    c.colar('Bônus por produtividade', at=c.A(5, 'produtividade.', 1.3), label='descrição Bônus por produtividade')
    c.click(BTN('Registrar Bônus'), at=c.A(5, 'produtividade.', 0.4), label='Registrar Bônus')
    c.confere('body', ['Movimentação registrada!'], 'aviso Movimentação registrada! (bônus)')
    c.waitfor(gone={'role': 'dialog'}, timeout=10)
    c.mark(6)
    c.click(MOV('Falta'), at=c.A(6, 'falta.', 0.9), label='Falta')
    c.hover(P('Descontar do salário', within=DLG), 1.0, at=c.A(6, 'Descontar', 0.9), label='Descontar do salário')
    c.hover(MOEDA(0), 1.2, at=c.A(6, 'valor', 0.9), label='valor de um dia já calculado')
    c.confere_campos(['R$ 140,00'], 'a falta já vem com R$ 140,00')
    c.confere('dlg', ['Sugestão: R$ 140,00/dia', 'Descontar do salário'], 'sugestão R$ 140,00/dia')
    c.click(TEXTAREA, at=c.A(6, 'quarenta', 1.0), label='campo Descrição')
    c.colar('Falta em 06/11', at=c.A(6, 'quarenta', 0.3), label='descrição Falta em 06/11')
    c.click(BTN('Registrar Falta'), at=c.A(6, 'reais.', 0.3), label='Registrar Falta')
    c.confere('body', ['Movimentação registrada!'], 'aviso Movimentação registrada! (falta)')
    c.waitfor(gone={'role': 'dialog'}, timeout=10)
    c.mark(7, antecipa=0.3)   # o "Registrar Falta" fecha o "reais." da linha 6 e o aviso termina ~0,3 s depois do início da linha 7
    c.hover(P('Saldo atual'), 1.4, at=c.A(7, 'saldo', 0.9), label='Saldo atual')
    c.hover(P('Faltas'), 0.8, at=c.A(7, 'falta', 0.9), label='Vales, Bônus e Faltas')
    c.confere('main', ['Saldo atual', 'R$ 2.790,00', 'Vales', 'R$ 300,00', 'Bônus', 'R$ 150,00', 'Faltas', 'R$ 140,00'], 'saldo atual R$ 2.790,00 = 3.080 - 300 + 150 - 140')
    c.fim()
    return c


def cap07():
    """O pagamento: informal do Rafael (R$ 2.790,00), Extrato, CLT da Tatiane (cancelado)."""
    c = cap_novo(7, setup=SETUP_FUNC + [{'do': 'click', 'target': FUNC('Rafael Lima')}, {'do': 'waitFor', 'text': 'Movimentações', 'timeout': 10}, {'do': 'pause', 'seconds': 0.6}])
    c.mark(1)
    c.click(MOV('Pagamento'), at=c.A(1, 'Pagamento.', 0.9), label='Pagamento')
    c.hover({'text': 'Tipo de pagamento', 'within': DLG}, 1.0, at=c.A(1, 'regime', 0.9), label='abre no regime Normal / Informal')
    c.hover({'text': 'Descontar dos Vales', 'within': DLG}, 1.0, at=c.A(1, 'vale', 0.9), label='Descontar dos Vales (100%)')
    c.hover({'text': 'Pagar com', 'within': DLG}, 1.0, at=c.A(1, 'Conta', 0.9), label='Pagar com Conta Principal')
    c.confere('dlg', ['Pagamento, Rafael Lima', 'Normal / Informal', 'Total de vales: R$ 300,00, Padrão: 100%', 'Conta Principal', 'R$ 20.525,00'], 'janela Pagamento do Rafael: vales R$ 300,00 e Conta Principal R$ 20.525,00')
    c.mark(2)
    c.hover({'text': 'Subtotal', 'within': DLG}, 1.0, at=c.A(2, 'resumo:', 0.9), label='resumo do pagamento')
    c.hover({'text': 'Valor a Pagar', 'within': DLG}, 1.2, at=c.A(2, 'Ficam', 0.9), label='Valor a Pagar')
    c.confere('dlg', ['Salário', 'R$ 3.080,00', 'Total de Bônus', 'R$ 150,00', 'Vales', 'R$ 300,00', 'Faltas', 'R$ 140,00', 'Subtotal', 'R$ 2.790,00', 'Valor a Pagar'], 'resumo: valor a pagar R$ 2.790,00')
    c.mark(3)
    c.click(BTN('Confirmar Pagamento'), at=c.A(3, 'Confirmo,', 0.9), label='Confirmar Pagamento')
    c.waitfor(text='Deseja gerar Recibo?', timeout=10)
    c.click(BTN('Não'), at=c.A(3, 'Agora', 0.9), label='Recibo: Não')
    c.waitfor(gone={'text': 'Deseja gerar Recibo?'}, timeout=10)
    c.mark(4)
    c.click(MOV('Extrato'), at=c.A(4, 'Extrato', 0.9), label='Extrato')
    c.waitfor(text='Saldo após', timeout=10)
    c.hover({'text': 'Saldo após', 'within': DLG}, 1.0, at=c.A(4, 'saldo', 0.9), label='Saldo após de cada movimento')
    c.hover({'text': 'Gerar Recibo', 'within': DLG}, 1.2, at=c.A(4, 'Gerar', 0.9), label='Gerar Recibo no pagamento')
    c.confere('dlg', ['Extrato, Rafael Lima', 'Vale', 'Bônus', 'Falta', 'Pagamento', 'Ajuste', 'Saldo após', 'Gerar Recibo'], 'extrato com vale, bônus, falta, pagamento e ajuste')
    fechar_janela(c, at=c.A(4, 'quiser.', 0.6))
    c.mark(5)
    c.click(FUNC('Tatiane Ribeiro'), at=c.A(5, 'Tatiane,', 0.9), label='Tatiane Ribeiro')
    c.click(MOV('Pagamento'), at=c.A(5, 'janela', 1.0), label='Pagamento (modo CLT)')
    c.hover({'text': 'Proventos', 'within': DLG}, 0.8, at=c.A(5, 'modo', 0.9), label='Proventos')
    c.hover({'text': 'INSS', 'within': DLG, 'exact': True}, 0.5, at=c.A(5, 'INSS,', 0.9), label='INSS')
    c.hover({'text': 'IRRF', 'within': DLG, 'exact': True}, 0.5, at=c.A(5, 'imposto', 0.9), label='IRRF')
    c.hover({'text': 'Vale-transporte', 'within': DLG, 'exact': True}, 0.5, at=c.A(5, 'vale-transporte', 0.9), label='Vale-transporte')
    c.hover({'text': 'Líquido a pagar', 'within': DLG}, 1.0, at=c.A(5, 'líquido', 0.9), label='Líquido a pagar')
    c.confere('dlg', ['Pagamento, Tatiane Ribeiro', 'CLT', 'Proventos', 'Descontos', 'INSS', 'IRRF', 'Vale-transporte', 'Líquido a pagar', 'Conta Principal', 'R$ 17.735,00'], 'modo CLT da Tatiane; Conta Principal R$ 17.735,00')
    c.mark(6)
    c.hover({'text': 'Valores calculados com base nas tabelas vigentes', 'within': DLG}, 1.5, at=c.A(6, 'dica:', 0.9), label='aviso: confira com o contador')
    c.click(BTN('Cancelar'), at=c.A(6, 'cancelo.', 0.9), label='Cancelar o pagamento da Tatiane')
    c.waitfor(gone={'role': 'dialog'}, timeout=10)
    c.fim()
    return c


def cap08():
    """As regras do ponto: Controle de Ponto > Config, selfie desligada, salvar, quiosque, Jornada Individual."""
    c = cap_novo(8, setup=SETUP_FUNC)
    c.mark(1)
    c.click(ABA_FUNC('Controle de Ponto'), at=c.A(1, 'Controle', 0.9), label='Controle de Ponto')
    c.click(TAB('Config'), at=c.A(1, 'Config,', 0.9), label='Config')
    c.hover(P('Jornada Padrão da Empresa'), 0.8, at=c.A(1, 'jornada', 0.9), label='Jornada Padrão da Empresa')
    c.hover(P('Entrada padrão'), 0.5, at=c.A(1, 'oito', 0.9), label='Entrada padrão')
    c.hover(P('Saída padrão'), 0.5, at=c.A(1, 'cinco,', 0.9), label='Saída padrão')
    c.hover(P('Intervalo (min)'), 0.6, at=c.A(1, 'hora', 0.9), label='Intervalo 60 min')
    c.mark(2)
    c.hover(P('Exigir selfie'), 0.7, at=c.A(2, 'selfie', 0.9), label='Exigir selfie')
    c.hover(P('Exigir geolocalização'), 0.7, at=c.A(2, 'localização.', 0.9), label='Exigir geolocalização')
    c.click(CHAVE('Exigir selfie'), at=c.A(2, 'Glacial', 0.9), label='desliga Exigir selfie')
    c.mark(3)
    c.rolar(260, at=c.A(3, 'pra', 0.9), label='desce até a madrugada')
    c.hover(P('Batidas da madrugada'), 1.2, at=c.A(3, 'madrugada', 0.9), label='Batidas da madrugada')
    c.mark(4)
    c.click(BTN('Salvar configurações'), at=c.A(4, 'Salvar', 0.9), label='Salvar configurações')
    c.confere('body', ['Configurações salvas!'], 'aviso Configurações salvas!')
    c.mark(5)
    c.rolar(600, at=c.A(5, 'Se', 0.9), label='desce até o ponto em grupo')
    c.hover(P('Ponto em grupo (quiosque)'), 1.5, at=c.A(5, 'grupo:', 0.9), label='Ponto em grupo (quiosque)')
    c.mark(6)
    c.rolar(600, at=c.A(6, 'E', 0.9), label='desce até a Jornada Individual')
    c.hover(P('Jornada Individual'), 1.0, at=c.A(6, 'Jornada', 0.9), label='Jornada Individual')
    c.hover(TBTN('Bruno Alves', 0), 1.0, at=c.A(6, 'horário,', 0.9), label='lápis de uma linha da jornada', optional=True)
    c.fim()
    return c


def cap09():
    """O ponto no celular, parte 1 (computador): Editar a Tatiane > Ponto eletrônico > Ativado > Salvar > link de ativação copiado.
    A parte do celular (linhas 4 a 7) é o `cap09b`. Este trecho acaba no início da linha 4."""
    c = cap_novo(9, setup=SETUP_FUNC + [{'do': 'eval', 'js': "navigator.clipboard && (navigator.clipboard.writeText = () => Promise.resolve()); 1"}])
    c.mark(1)
    c.click(FUNC('Tatiane Ribeiro'), at=c.A(1, 'Tatiane.', 1.0), label='Tatiane Ribeiro')
    c.click(MOV('Editar'), at=c.A(1, 'Editar', 0.9), label='Editar')
    c.click(ABA_FORM('Ponto eletrônico'), at=c.A(1, 'Ponto', 0.9, nth=1), label='aba Ponto eletrônico')
    c.click(BTN('Ativado', within=DLG), at=c.A(1, 'ativar.', 0.9), label='Ativado')
    c.mark(2)
    c.hover({'text': 'PIN do ponto', 'within': DLG}, 1.2, at=c.A(2, 'PIN,', 0.9), label='PIN do ponto')
    c.hover({'text': 'Acesso individual ao ponto', 'within': DLG}, 1.2, at=c.A(2, 'acesso', 0.9), label='Acesso individual ao ponto')
    c.confere('dlg', ['PIN do ponto', 'Acesso individual ao ponto'], 'blocos PIN e acesso individual depois de ativar')
    c.mark(3)
    c.click(BTN('Salvar', within=DLG), at=c.A(3, 'Salvo,', 0.9), label='Salvar')
    c.confere('body', ['Link de ativação copiado!'], 'aviso Link de ativação copiado!')
    c.dur = c.L(4)      # a edição junta este trecho (até o início da linha 4) com o cap09b (celular)
    c.fim()
    return c


TOKEN_TATIANE = hashlib.sha256('t15-ativacao:Tatiane Ribeiro'.encode()).hexdigest()   # o mesmo token que o RPC create_employee_face_enrollment_link devolve


def cap09b():
    """O ponto no celular, parte 2 (celular, sem login): cadastro facial > Continuar sem biometria > ponto > Registrar Entrada > Confirmar registro.
    É a voz do cap. 9 a partir da linha 4: aqui as linhas se chamam L1..L4 (= L4..L7 do cap. 9) e os tempos são contados do início da linha 4."""
    c = Cap(9, pace=0.5, start=(195, 420), nome='cap09b', device='phone', anonymous=True, sem=['apos-cap09'], setup=[
        {'do': 'geo', 'lat': -22.90240, 'lng': -43.11094},
        {'do': 'clock', 'set': '2026-11-11T09:02:00-03:00'},
        {'do': 'goto', 'url': f'/ativar-ponto/{TOKEN_TATIANE}'}, {'do': 'waitFor', 'text': 'Cadastro facial', 'timeout': 25}, AGUARDA,
    ])
    off = c.L(4)
    c.voz_inicio = off
    c.words = [dict(w, s=round(w['s'] - off, 2), linha=w['linha'] - 3) for w in c.words if w['linha'] >= 3]
    c.linhas = [dict(l, s=round(l['s'] - off, 2), e=round(l['e'] - off, 2)) for l in c.linhas[3:]]
    c.dur = round(c.dur - off, 2)
    c.mark(1)
    c.hover(P('Olá, Tatiane', within='body'), 1.0, at=c.A(1, 'cadastro', 0.9), label='Cadastro facial: Olá, Tatiane')
    c.click(BTN('Continuar sem biometria', noScroll=True), at=c.A(1, 'Continuar', 0.9), label='Continuar sem biometria')
    c.waitfor(text='Você ainda não bateu o ponto hoje', timeout=20)
    c.mark(2)
    c.hover(P('Tatiane Ribeiro', within='body'), 1.2, at=c.A(2, 'nome,', 0.9), label='nome, cargo e marca da empresa')
    c.mark(3)
    c.click(BTN('Registrar Entrada', noScroll=True), at=c.A(3, 'Registrar', 0.9), label='Registrar Entrada')
    c.waitfor(text='Confirmar registro', timeout=15)
    c.confere('body', ['Tipo', 'Horário', 'Local', 'Confirmar registro'], 'resumo da batida: tipo, horário e local')
    c.hover(P('Local', within='body'), 1.2, at=c.A(3, 'local.', 0.9), label='Local da batida')
    c.mark(4)
    c.click(BTN('Confirmar registro', noScroll=True), at=c.A(4, 'Confirmar', 0.9), label='Confirmar registro')
    c.confere('body', ['Entrada registrada'], 'aviso Entrada registrada')
    c.confere('body', ['Registros de hoje', 'Iniciar Intervalo'], 'registros de hoje e botão Iniciar Intervalo')
    c.fim()
    return c


def cap10():
    """Acompanhando o ponto: Hoje (olho e lápis), Histórico (Filtros e CSV), Relatório."""
    c = cap_novo(10, setup=SETUP_FUNC + [{'do': 'clock', 'set': '2026-11-11T09:10:00-03:00'}, {'do': 'pause', 'seconds': 0.4}])
    c.mark(1)
    c.click(ABA_FUNC('Controle de Ponto'), at=c.A(1, 'escritório,', 0.9), label='Controle de Ponto')
    c.waitfor(text='Presentes', timeout=15)
    c.hover(FUNC('Tatiane Ribeiro'), 1.4, at=c.A(1, 'Tatiane', 0.9), label='linha da Tatiane: entrada e Presente')
    c.confere('main', ['Presentes', 'Tatiane Ribeiro', 'Presente', '09:02'], 'Hoje: Tatiane presente, entrada 09:02')
    c.mark(2)
    c.click(TBTN('Tatiane', 0), at=c.A(2, 'olho', 0.9), label='olho da linha')
    c.waitfor(text='Registros do dia', timeout=10)
    c.hover({'text': 'Rua Moreira César', 'within': DLG}, 0.7, at=c.A(2, 'endereço', 0.9), label='endereço da batida')
    c.confere('dlg', ['Registros do dia, Tatiane Ribeiro', 'Entrada', 'Trabalhado', 'Intervalo', 'Saldo'], 'registros do dia com o endereço')
    fechar_janela(c, at=c.A(2, 'batida.', 0.2))
    c.mark(3)
    c.click(TBTN('Tatiane', 1), at=c.A(3, 'lápis', 0.9), label='lápis da linha')
    c.waitfor(text='Registro manual', timeout=10)
    # fase 2: nesta tela cada gesto leva 1,3 a 2 s até o alvo (o "Histórico" ~2 s): justificativa e Cancelar saem mais cedo, para o Histórico não atrasar
    c.hover({'text': 'Justificativa', 'within': DLG}, 0.9, at=c.A(3, 'escreve', 0.9), label='Justificativa (obrigatória)')
    c.confere('dlg', ['Registro manual, Tatiane Ribeiro', 'Tipo de registro', 'Horário', 'Justificativa *'], 'registro manual: tipo, horário e justificativa (sem campo Data)')
    c.click(BTN('Cancelar'), at=c.A(3, 'obrigatória.', 0.9), label='Cancelar o registro manual')
    c.waitfor(gone={'role': 'dialog'}, timeout=10)
    c.mark(4)
    c.click(TAB('Histórico'), at=c.A(4, 'Histórico', 0.9), label='Histórico')
    c.waitfor(text='registro', timeout=10)
    c.click(BTNX('Filtros'), at=c.A(4, 'filtro', 0.9), label='Filtros (funcionário, período e status)')
    c.confere('body', ['Funcionário', 'Período', 'Status'], 'painel de filtros')
    c.press('Escape', at=c.A(4, 'período,', 0.5), label='fecha os filtros')
    c.hover(BTN('CSV'), 1.2, at=c.A(4, 'CSV', 0.9), label='botão CSV (sem baixar)')
    c.mark(5)
    c.click(TAB('Relatório'), at=c.A(5, 'Relatório', 0.9), label='Relatório')
    c.waitfor(text='Calendário', timeout=10)
    c.hover(P('Calendário'), 0.6, at=c.A(5, 'calendário,', 0.9), label='Calendário do mês')
    c.hover(P('Horas por dia'), 1.0, at=c.A(5, 'horas', 0.9), label='Horas por dia')
    c.confere('main', ['Calendário', 'Horas por dia'], 'relatório: calendário e horas por dia')
    c.click(BTNX('Filtros'), at=c.A(5, 'Filtrando', 0.9), label='Filtros do relatório')
    c.click({'text': 'Tatiane Ribeiro', 'within': DLG}, at=c.A(5, 'pessoa,', 1.1), label='filtra a Tatiane')
    c.press('Escape', at=c.A(5, 'você', 0.3), label='fecha os filtros')
    c.hover(P('Saldo do mês'), 1.4, at=c.A(5, 'saldo', 0.9), label='saldo do mês da Tatiane')
    c.confere('main', ['Relatório de Tatiane Ribeiro', 'Dias trabalhados', 'Total trabalhado', 'Saldo do mês'], 'filtrando a Tatiane aparece o saldo do mês')
    c.fim()
    return c


def cap11():
    """A folha em Contas a Pagar (12/11, de manhã): Financeiro > Contas a Pagar/Receber > A Pagar > busca "Folha" > Marcar como pago > Cancelar."""
    c = cap_novo(11, setup=SETUP_DASH, prewarm=['/dashboard', '/financeiro/contas'])
    c.mark(1)
    c.click(BTN('Financeiro'), at=c.A(1, 'folha', 0.9), label='grupo Financeiro do menu')
    c.click(MENU_CONTAS, at=c.A(1, 'Contas', 0.9), label='Contas a Pagar/Receber')
    c.waitfor(text='Contas a pagar e a receber', timeout=20)
    # fase 2: Contas a Pagar/Receber fica clicável entre 5,6 e 6,0 s (duas tomadas): a aba e a busca ancoram no que a tela permite
    c.click(TAB('A Pagar'), at=c.A(1, 'Procuro', 0.3), label='aba A Pagar')
    c.type({'placeholder': 'Buscar por nome, descrição, categoria ou valor...'}, 'Folha', at=c.A(1, 'folha', 0.2, nth=1), cps=12, label='busca "Folha"')
    c.waitfor(text='Folha Rafael Lima', timeout=10)
    c.mark(2)
    c.hover(P('Folha Rafael Lima'), 1.0, at=c.A(2, 'folha', 0.9), label='folha de cada um')
    c.hover(P('07/12/2026'), 1.2, at=c.A(2, 'quinto', 0.9), label='vencimento 07/12/2026')
    c.confere('main', ['Folha Rafael Lima — 2026-12', 'Folha de Pagamento', '07/12/2026', 'R$ 3.080,00', 'Pendente', 'Folha Tatiane Ribeiro — 2026-12', 'R$ 2.800,00'], 'as folhas de dezembro, vencimento 07/12/2026')
    c.mark(3)
    c.abrir_menu('Rafael Lima', 'Marcar como pago', at=c.A(3, 'Marcar', 1.4), label='menu ⋮ da folha do Rafael')
    c.click(ITEM('Marcar como pago'), at=c.A(3, 'pago', 0.9), label='Marcar como pago')
    c.waitfor(text='Quitando folha pendente', timeout=10)
    c.hover({'text': 'Quitando folha pendente', 'within': DLG}, 0.8, at=c.A(3, 'quitando', 0.5), label='Quitando folha pendente, período 2026-12')
    c.confere('dlg', ['Pagamento, Rafael Lima', 'Quitando folha pendente, período 2026-12'], 'janela de pagamento quitando a folha de 2026-12')
    c.mark(4)
    c.click(BTN('Cancelar'), at=c.A(4, 'cancelo.', 0.9), label='Cancelar')
    c.waitfor(gone={'role': 'dialog'}, timeout=10)
    c.fim()
    return c


def cap12():
    """Recapitulando (12/11): passa pelas telas do tutorial, só leitura."""
    # aquece também Contas a Pagar/Receber (fora do vídeo), como o cap. 11: a frio, o "A Pagar" levou 3 s para ficar clicável (fase 2)
    c = cap_novo(12, setup=SETUP_FUNC, prewarm=['/dashboard', '/financeiro/contas', '/funcionarios'])
    c.mark(1)
    c.click(FUNC('Tatiane Ribeiro'), at=c.A(1, 'Tatiane', 0.9), label='ficha da Tatiane (CLT, Controle de Ponto)')
    c.click(MOV('Editar'), at=c.A(1, 'salário,', 1.2), label='Editar')
    c.click(ABA_FORM('Pagamento'), at=c.A(1, 'custo', 0.9), label='aba Pagamento')
    c.hover({'text': 'Regime', 'within': DLG, 'exact': True}, 0.8, at=c.A(1, 'regime', 0.9), label='regime CLT')
    fechar_janela(c, at=c.A(1, 'vinculou', 0.4))
    c.mark(2)
    c.click(FUNC('Rafael Lima'), at=c.A(2, 'Rafael,', 0.9), label='ficha do Rafael')
    c.hover(P('Saldo atual'), 1.0, at=c.A(2, 'vale,', 0.9), label='vale, bônus e falta')
    c.click(MOV('Extrato'), at=c.A(2, 'extrato.', 1.0), label='Extrato')
    c.waitfor(text='Saldo após', timeout=10)
    fechar_janela(c, at=c.A(2, 'extrato.', 0.1))
    c.mark(3)
    c.click(ABA_FUNC('Controle de Ponto'), at=c.A(3, 'regras', 0.9), label='Controle de Ponto')
    c.click(TAB('Config'), at=c.A(3, 'ponto,', 0.9), label='Config')
    c.click(TAB('Hoje'), at=c.A(3, 'Hoje,', 0.9), label='Hoje')
    c.click(TAB('Histórico'), at=c.A(3, 'Histórico', 0.9), label='Histórico')
    c.click(TAB('Relatório'), at=c.A(3, 'Relatório.', 0.9), label='Relatório')
    c.mark(4)
    c.ev("(()=>{history.pushState({},'','/financeiro/contas');window.dispatchEvent(new PopStateEvent('popstate'));return location.pathname})()", at=c.A(4, 'folha', 1.2), label='vai para Contas a Pagar')
    c.waitfor(text='Contas a pagar e a receber', timeout=20)
    c.click(TAB('A Pagar'), at=c.A(4, 'sozinha', 0.9), label='aba A Pagar')
    c.type({'placeholder': 'Buscar por nome, descrição, categoria ou valor...'}, 'Folha', at=c.A(4, 'Contas', 0.9), cps=10, label='busca "Folha"')
    c.mark(5)
    c.hover(P('Folha Rafael Lima'), 1.2, at=c.A(5, 'Com', 0.9), label='as folhas, fim do tutorial')
    c.fim()
    return c
