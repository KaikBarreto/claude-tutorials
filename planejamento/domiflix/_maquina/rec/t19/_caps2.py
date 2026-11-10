

SETUP_COBR_MENU = SETUP_COBRANCAS + [{'do': 'click', 'target': MENU_LATERAL}, {'do': 'pause', 'seconds': 0.8}]
NOVA_COBRANCA = BTN('Nova cobrança', nth=0)
ACOES_COBRANCA = {'selector': 'main button[aria-label="Ações da cobrança"]', 'nth': 0}
ACOES_ASSINATURA = {'selector': 'main button[aria-label="Ações da assinatura"]', 'nth': 0}
CLIENTE_COMBO = {'selector': f'{DLG} button[role=combobox]', 'nth': 0}
BUSCA_CLIENTE = {'placeholder': 'Buscar por cliente, telefone ou documento…'}


def escolhe_cliente(c, busca, nome, at, label):
    """abre o seletor de cliente da janela, busca e escolhe (clique + espera da lista)"""
    c.click(CLIENTE_COMBO, at=at, label=f'abre a lista de clientes ({label})')
    c.waitfor(target={'text': nome}, timeout=8)   # (o seletor da assinatura não tem campo de busca)
    # (sem digitar na busca: com teclado de verdade a lista filtrada não devolveu a opção no ensaio; a lista cheia traz o cliente e o clique rola até ele)
    c.pause(0.8)
    c.click({'text': nome}, label=f'cliente: {nome}')   # a opção traz o documento junto (texto exato não casa)


def dia_do_calendario(c, botao, dia, meses_a_frente, at, label):
    """abre o calendário do campo de data (`botao` = seletor), avança `meses_a_frente` meses e escolhe o `dia`"""
    c.click(botao, at=at, label=f'abre o calendário ({label})')
    for _ in range(meses_a_frente):
        c.click({'role': 'button', 'name': 'Go to next month'}, label=f'próximo mês ({label})')
    c.click(SEL(f'{POP} button:text-is("{dia}")'), label=f'escolhe o dia {dia} ({label})')


def cap06():
    """Uma cobrança avulsa: Nova cobrança (4 abas), Restaurante Sabor da Serra, R$ 450,00, vence em 13/11, Pagamento, Encargos, Financeiro, resumo, Gerar cobrança, copiar o link."""
    c = Cap(6, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/financeiro/cobrancas'], setup=SETUP_COBR_MENU)
    c.mark(1)
    c.hover(P('A RECEBER'), 0.8, at=c.A(1, 'totais', 0.9), label='cartões A receber, Recebido e Vencido')
    c.hover(P('Nenhuma cobrança'), 0.3, at=c.A(1, 'ainda', 2.2), label='a lista ainda vazia')
    c.mark(2)
    c.click(NOVA_COBRANCA, at=c.A(2, 'Clico', 1.6), label='Nova cobrança')
    c.waitfor(text='Gere um link de pagamento para enviar ao seu cliente.', timeout=10)
    c.hover(TAB('Encargos', within=DLG), 0.6, at=c.A(2, 'quatro', 0.9), label='as quatro abas da janela')
    escolhe_cliente(c, 'Sabor', 'Restaurante Sabor da Serra', c.A(2, 'Restaurante', 2.4), 'Restaurante Sabor da Serra')
    c.confere('dlg', ['Restaurante Sabor da Serra'], 'cliente escolhido')
    c.mark(3)
    c.confere_ausente('dlg', 'ainda não tem CPF ou CNPJ', 'sem aviso de documento (o restaurante tem CNPJ)')
    c.hover(CLIENTE_COMBO, 1.8, at=c.A(3, 'CPF', 0.9), label='campo Cliente preenchido, sem aviso de documento')
    c.mark(4)
    c.click({'selector': '#charge-amount'}, at=c.A(4, 'quatrocentos', 1.0), label='campo Valor')
    c.type({'selector': '#charge-amount'}, '45000', cps=8, noClick=True, label='Valor: 450,00')
    c.confere_campos('450,00', 'valor 450,00', escopo=DLG)
    c.confere('dlg', ['Resumo do recebimento'], 'o resumo do recebimento aparece embaixo (depois do cliente e do valor)')
    dia_do_calendario(c, {'selector': '#charge-due'}, 13, 0, c.A(4, 'vencimento', 0.9), 'vencimento 13/11/2026')
    c.confere('dlg', ['13/11/2026', 'a receita entra em 10/11/2026, o dia de hoje'], 'vencimento 13/11/2026 e a dica da competência em 10/11/2026')
    c.hover(P('Esta é a data em que o cliente deve pagar.', within=DLG), 0.5, at=c.A(4, 'dica:', 1.8), label='dica do regime de competência')
    c.click({'selector': '#charge-desc'}, at=c.A(4, 'Na', 4.6, nth=1), label='campo Descrição')
    c.type({'selector': '#charge-desc'}, 'Limpeza e higienização de 2 splits da cozinha', cps=16, noClick=True, label='Descrição: Limpeza e higienização de 2 splits da cozinha')
    c.mark(5)
    c.click(BTN('Avançar'), at=c.A(5, 'Avanço', 0.9), label='Avançar: aba Pagamento')
    c.waitfor(text='Forma de pagamento', timeout=8)
    c.click(COMBO('Cliente escolhe'), at=c.A(5, 'Deixo', 0.9), label='abre Forma de pagamento')
    c.waitfor(target=OPT('Cartão de crédito'), timeout=8)
    c.confere('body', ['Pix', 'Boleto', 'Cartão de crédito'], 'a lista traz Pix, Boleto e Cartão de crédito')
    c.press('Escape', at=c.A(5, 'decide', 0.9), label='fecha a lista sem trocar')
    c.pause(0.5)
    c.mark(6)
    c.click(BTN('Avançar'), at=c.A(6, 'Em', 0.9), label='Avançar: aba Encargos')
    c.waitfor(text='Multa (%)', timeout=8)
    c.confere_campos(['2', '1'], 'multa 2 e juros 1 já preenchidos', escopo=DLG)
    c.hover(P('Multa (%)', within=DLG), 1.6, at=c.A(6, 'multa', 0.9), label='Multa (%) e Juros ao mês (%) já preenchidos')
    c.mark(7)
    c.click(BTN('Avançar'), at=c.A(7, 'Na', 0.9), label='Avançar: aba Financeiro')
    c.waitfor(text='Lançar no financeiro', timeout=8)
    c.hover(P('Lançar no financeiro', within=DLG), 1.8, at=c.A(7, 'Lançar', 0.9), label='Lançar no financeiro: Sim')
    c.mark(8)
    c.click(P('Resumo do recebimento', within=DLG), at=c.A(8, 'Antes', 0.9), label='abre o Resumo do recebimento')
    c.confere('dlg', ['O cliente escolhe como pagar. Veja quanto sobra em cada forma:', 'R$ 448,01', 'R$ 436,05', 'Quanto o cliente paga', 'Pagando 30 dias depois do vencimento'],
              'resumo: Pix e boleto R$ 448,01, cartão à vista R$ 436,05 e o cenário de atraso')
    c.hover(P('Quanto o cliente paga', within=DLG), 1.8, at=c.A(8, 'quanto', 0.9, nth=1), label='Quanto o cliente paga, se atrasar')
    c.mark(9)
    c.click(BTN('Gerar cobrança'), at=c.A(9, 'Clico', 0.9), label='Gerar cobrança')
    c.waitfor(text='Aponte a câmera para pagar', timeout=15)
    c.confere('dlg', ['Cobrança gerada', 'Aponte a câmera para pagar', 'Link de pagamento', 'Enviar por WhatsApp'], 'cobrança gerada com o QR Code e o link de pagamento')
    c.confere_campos(f'/pagar/{CODIGO_COBRANCA}', 'o link de pagamento traz o código da cobrança', escopo=DLG)
    c.hover(P('Aponte a câmera para pagar', within=DLG), 1.6, at=c.A(9, 'QR', 0.9), label='QR Code da cobrança')
    c.mark(10)
    c.click(BTN('Copiar link'), at=c.A(10, 'copio', 0.9), label='Copiar link')
    c.waitfor(text='Link copiado!', timeout=6, optional=True)
    c.hover(BTN('Enviar por WhatsApp'), 2.0, at=c.A(10, 'WhatsApp,', 1.2), label='Enviar por WhatsApp (sem clicar)')
    c.fim()
    return c


def cap07():
    """A cobrança na lista: linha A receber, menu da cobrança (Copiar link, Editar, Excluir)."""
    c = Cap(7, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/financeiro/cobrancas'], setup=SETUP_COBR_MENU)
    c.mark(1)
    c.confere('main', ['Restaurante Sabor da Serra', '450,00', 'A receber', '13/11/2026', 'Cliente escolhe'], 'a linha da cobrança: A receber, 13/11/2026, Cliente escolhe')
    c.hover(SEL('main tbody tr', hasText='Restaurante Sabor da Serra'), 1.6, at=c.A(1, 'lista', 0.9), label='a linha do Restaurante Sabor da Serra, A receber')
    c.mark(2)
    c.click(ACOES_COBRANCA, at=c.A(2, 'menu', 0.9), label='menu ⋯ da cobrança')
    c.waitfor(target=ITEM('Copiar link'), timeout=8)
    c.click(ITEM('Copiar link'), at=c.A(2, 'Copiar', 0.9), label='Copiar link')
    c.waitfor(text='Link copiado!', timeout=6, optional=True)
    c.pause(0.8)
    c.mark(3)
    c.click(ACOES_COBRANCA, at=c.A(3, 'Editar', 1.6), label='menu ⋯ de novo')
    c.waitfor(target=ITEM('Editar'), timeout=8)
    c.click(ITEM('Editar'), at=c.A(3, 'Editar', 0.9), label='Editar')
    c.waitfor(text='As alterações são aplicadas na cobrança gerada.', timeout=8)
    c.hover(P('Vencimento', within=DLG), 1.2, at=c.A(3, 'valor,', 0.9), label='Editar cobrança: Valor, Vencimento e Descrição')
    c.click(BTN('Cancelar', within=DLG), at=c.A(3, 'Excluir', 2.2), label='Cancelar (fecha sem salvar)')
    c.pause(0.6)
    c.click(ACOES_COBRANCA, at=c.A(3, 'apaga', 1.4), label='menu ⋯ para mostrar o Excluir')
    c.waitfor(target=ITEM('Excluir'), timeout=8)
    c.hover(ITEM('Excluir'), 1.6, at=c.A(3, 'apaga', 0.2), label='Excluir (sem clicar)')
    c.press('Escape', label='fecha o menu')
    c.fim()
    return c


def cap08():
    """O que o cliente vê: link da cobrança SEM login (/pagar/<código>); Pix, Boleto, Cartão (sem pagar); corte: o pagamento é simulado fora da tela e a página mostra Pagamento confirmado."""
    link = f'/pagar/{CODIGO_COBRANCA}'
    setup = [{'do': 'goto', 'url': link}, {'do': 'waitFor', 'text': 'Valor a pagar', 'timeout': 25}, AGUARDA]
    c = Cap(8, pace=0.5, start=(760, 420), prewarm=['/dashboard'], setup=setup, anonymous=True)
    c.mark(1)
    c.confere('body', ['Glacial Cold Brasil', 'Valor a pagar', 'R$ 450,00', 'Vencimento', '13/11/2026', 'Limpeza e higienização de 2 splits da cozinha',
                       'Forma de pagamento', 'Pix', 'Aprovação na hora', 'Boleto', '1 a 2 dias úteis', 'Cartão', 'Aprovação imediata'], 'a página do cliente: marca, valor, vencimento, descrição e as três formas')
    c.hover(TXT('Valor a pagar'), 1.4, at=c.A(1, 'valor,', 0.9), label='Valor a pagar')
    c.hover({'text': 'Limpeza e higienização de 2 splits da cozinha'}, 1.4, at=c.A(1, 'descrição.', 0.9), label='a descrição do serviço (a página não traz o rótulo Descrição)')
    c.mark(2)
    c.click(TXT('Pix'), at=c.A(2, 'Pix,', 0.9), label='Pix')
    c.waitfor(text='Pague com Pix', timeout=8)
    c.confere('body', ['Escaneie o QR Code com o app do seu banco ou use o Pix copia e cola abaixo.', 'Copiar código Pix'], 'Pix: QR Code, copia e cola e o botão Copiar código Pix')
    c.click(BTN('Copiar código Pix'), at=c.A(2, 'copia', 0.9, nth=1), label='Copiar código Pix')
    c.waitfor(text='Código copiado!', timeout=6, optional=True)
    c.mark(3)
    c.click(TXT('Voltar'), at=round(c.L(3) - 1.7, 2), label='Voltar')
    c.click(TXT('Boleto'), at=c.A(3, 'boleto,', 1.0), label='Boleto')
    c.waitfor(text='Boleto bancário', timeout=8)
    c.hover({'text': 'Abrir boleto'}, 0.2, at=c.A(3, 'abre', 1.1), label='Abrir boleto (sem clicar)')
    c.click(TXT('Voltar'), at=c.A(3, 'cartão,', 3.0), label='Voltar')
    c.click(TXT('Cartão'), at=c.A(3, 'cartão,', 1.9), label='Cartão')
    c.waitfor(text='Pagamento com cartão', timeout=8)
    c.hover(SEL('button', hasText='Pagar R$ 450,00'), 0.4, at=c.A(3, 'preenche', 1.7), label='Pagar R$ 450,00 (sem preencher)')
    c.mark(4)
    c.ev("fetch(%s,{method:'POST',headers:{'content-type':'application/json'},body:'{}'}).then(r=>r.text())" % json.dumps(os.environ.get('FAKE_URL', 'http://127.0.0.1:54333') + '/functions/v1/asaas-simular-pagamento'),
         at=round(c.L(4) - 0.5, 2), label='CORTE: o Pix é pago fora da tela (o aviso do Asaas simulado)')
    # o robô navega por pushState (o `goto` na mesma rota não remonta a página nem consulta de novo): o foco do navegador (visibilitychange) refaz a consulta
    # (vale com a consulta já vencida, 15 s); se ainda não mostrou o pagamento, recarrega o mesmo link
    c.ev("document.dispatchEvent(new Event('visibilitychange'));window.dispatchEvent(new Event('focus'));'foco'", at=c.A(4, 'Abrindo', 2.4), label='volta ao mesmo link (a página consulta de novo)')
    c.pause(1.5)
    c.ev("(()=>{if(!document.body.innerText.includes('Pagamento confirmado')){location.reload();return 'recarregou'}return 'já mostra'})()", label='recarrega o link se ainda não mostrou o pagamento')
    c.waitfor(text='Pagamento confirmado', timeout=15)
    c.confere('body', ['Pagamento confirmado', 'Recebemos seu pagamento. Obrigado!'], 'Pagamento confirmado')
    c.hover(TXT('Pagamento confirmado'), 1.2, at=c.A(4, 'Pagamento', 1.6, nth=0), label='Pagamento confirmado')
    c.fim()
    return c


def cap09():
    """Pago e baixado: Cobranças com Pago e Recebido; Contas a Pagar/Receber (A Receber): bruto, taxa e líquido; Movimentações; menu da cobrança paga (Estornar)."""
    c = Cap(9, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/financeiro/cobrancas', '/financeiro/contas'], setup=SETUP_COBR_MENU)
    c.mark(1)
    c.confere('main', ['Pago', '450,00', 'RECEBIDO'], 'a cobrança está Pago e o Recebido soma 450,00')
    c.hover(SEL('main tbody tr', hasText='Restaurante Sabor da Serra'), 1.4, at=c.A(1, 'Pago,', 0.9), label='a linha Pago')
    c.hover(P('RECEBIDO'), 1.4, at=c.A(1, 'total', 0.9), label='cartão Recebido com R$ 450,00')
    c.mark(2)
    c.add({'do': 'goto', 'url': '/financeiro/contas', 'at': c.A(2, 'Em', 1.0), 'label': 'abre Contas a Pagar/Receber'})
    c.waitfor(target=TAB('A Receber'), timeout=20)
    c.click(TAB('A Receber'), label='aba A Receber')
    c.waitfor(text='Limpeza e higienização de 2 splits da cozinha', timeout=15)
    c.confere('main', ['Limpeza e higienização de 2 splits da cozinha', 'Bruto: R$ 450,00', 'Taxa: − R$ 1,99', 'Líquido: R$ 448,01', 'Pago'], 'a conta a receber paga com bruto, taxa e líquido')
    c.hover(P('Bruto: R$ 450,00'), 2.4, at=c.A(2, 'linha', 0.9), label='Bruto, Taxa e Líquido da conta a receber')
    c.mark(3)
    c.add({'do': 'goto', 'url': '/financeiro/movimentacoes', 'at': c.A(3, 'Nas', 1.0), 'label': 'abre Movimentações Financeiras'})
    c.waitfor(text='Tarifa de recebimento (Asaas)', timeout=20)
    c.confere('main', ['Limpeza e higienização de 2 splits da cozinha', 'Vendas de Serviços', 'Conta Principal', '+ R$ 450,00', 'Tarifa de recebimento (Asaas)', 'Tarifas e Taxas', '- R$ 1,99'],
              'a receita em Vendas de Serviços e a tarifa em Tarifas e Taxas')
    c.hover(SEL('main tr', hasText='Limpeza e higienização'), 0.7, at=c.A(3, 'receita', 1.1), label='a receita em Vendas de Serviços')
    c.hover(SEL('main tr', hasText='Tarifa de recebimento'), 1.6, at=c.A(3, 'taxa', 0.9, nth=0), label='a tarifa em Tarifas e Taxas')
    c.mark(4)
    c.add({'do': 'goto', 'url': '/financeiro/cobrancas', 'at': round(c.L(4) - 1.2, 2), 'label': 'volta para Cobranças'})
    c.waitfor(text='Restaurante Sabor da Serra', timeout=20)
    c.click(ACOES_COBRANCA, at=c.A(4, 'menu', 0.9), label='menu ⋯ da cobrança paga')
    c.waitfor(target=ITEM('Estornar'), timeout=8)
    c.hover(ITEM('Estornar'), 1.8, at=c.A(4, 'Estornar,', 0.9), label='Estornar (sem clicar)')
    c.press('Escape', label='fecha o menu')
    c.fim()
    return c


def cap10():
    """Cobrança todo mês: aba Assinaturas > Nova assinatura (Academia Ponto Forte, R$ 380,00, Mensal, 1º vencimento 10/12, Contínua) > resumo > Criar assinatura > MRR."""
    c = Cap(10, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/financeiro/cobrancas'], setup=SETUP_COBR_MENU)
    c.mark(1)
    c.click(TAB('Assinaturas'), at=c.A(1, 'Assinaturas,', 0.9), label='aba Assinaturas')
    c.waitfor(text='Nenhuma assinatura', timeout=10)
    c.click(BTN('Nova assinatura', nth=0), at=c.A(1, 'Clico', 1.9), label='Nova assinatura')
    c.waitfor(text='Configure uma cobrança recorrente para o seu cliente.', timeout=10)
    c.mark(2)
    escolhe_cliente(c, 'Academia', 'Academia Ponto Forte', c.A(2, 'Academia', 2.6), 'Academia Ponto Forte')
    c.click({'selector': f'{DLG} input[placeholder="0,00"]'}, at=c.A(2, 'trezentos', 1.2), label='campo Valor')
    c.type({'selector': f'{DLG} input[placeholder="0,00"]'}, '38000', cps=8, noClick=True, label='Valor: 380,00')
    c.click(COMBO('Mensal'), at=c.A(2, 'frequência', 0.9), label='abre Frequência')
    c.waitfor(target=OPT('Semanal'), timeout=8)
    c.hover(OPT('Anual'), 1.0, at=c.A(2, 'semanal', 0.9), label='a lista vai de Semanal a Anual')
    c.press('Escape', label='fecha a lista (fica em Mensal)')
    c.pause(0.5)
    c.mark(3)
    c.click(COMBO('Cliente escolhe'), at=c.A(3, 'forma', 0.9), label='abre Forma de pagamento')
    c.waitfor(target=OPT('Pix Automático'), timeout=8)
    c.hover(OPT('Cartão de crédito (recorrente)'), 0.8, at=c.A(3, 'cartão', 0.9), label='Cartão de crédito (recorrente)')
    c.hover(OPT('Pix Automático'), 1.2, at=c.A(3, 'Pix', 0.9, nth=0), label='Pix Automático')
    c.press('Escape', label='fecha a lista (fica em Cliente escolhe)')
    c.pause(0.5)
    c.mark(4)
    dia_do_calendario(c, SEL(f'{DLG} button[aria-haspopup]', hasText='/2026'), 10, 1, c.A(4, 'primeiro', 0.9), '1º vencimento 10/12/2026')
    c.confere('dlg', ['10/12/2026', 'Contínua', 'A assinatura segue gerando cobranças até você cancelar.', 'Número de ciclos'], '1º vencimento 10/12/2026, Duração Contínua e Número de ciclos')
    c.click({'placeholder': 'Ex.: Contrato de manutenção mensal'}, at=c.A(4, 'Duração,', 0.9), label='campo Descrição')
    c.type({'placeholder': 'Ex.: Contrato de manutenção mensal'}, 'Manutenção mensal dos splits', cps=16, noClick=True, label='Descrição: Manutenção mensal dos splits')
    c.hover(P('Número de ciclos', within=DLG), 0.4, at=c.A(4, 'ciclos', 1.4), label='Número de ciclos')
    c.mark(5)
    c.click(P('Resumo por cobrança', within=DLG), at=c.A(5, 'resumo', 0.9), label='abre o Resumo por cobrança')
    c.confere('dlg', ['Valores de UMA cobrança (Mensal), não o total da assinatura.', 'A assinatura não tem fim definido, então não existe total fechado.'], 'resumo por cobrança')
    c.hover(P('Valores de UMA cobrança', within=DLG), 1.8, at=c.A(5, 'cobrança,', 0.5), label='Valores de UMA cobrança')
    c.mark(6)
    c.click(BTN('Criar assinatura'), at=c.A(6, 'Clico', 0.9), label='Criar assinatura')
    c.waitfor(text='Receita recorrente mensal (MRR)', timeout=15)
    c.confere('main', ['Academia Ponto Forte', '380,00', 'Mensal', '10/12/2026', 'Cliente escolhe', 'Ativa', '1 assinatura ativa', 'Receita recorrente mensal (MRR): 380,00'],
              'a lista: Ativa, 1 assinatura ativa e MRR 380,00')
    c.hover(SEL('main tbody tr', hasText='Academia Ponto Forte'), 1.4, at=c.A(6, 'academia', 0.9), label='a assinatura Ativa na lista')
    c.hover(P('Receita recorrente mensal (MRR)'), 2.0, at=c.A(6, 'lá', 0.9), label='Receita recorrente mensal (MRR)')
    c.fim()
    return c


SETUP_ASSINATURAS = SETUP_COBR_MENU + [{'do': 'click', 'target': TAB('Assinaturas')}, {'do': 'waitFor', 'text': 'Academia Ponto Forte', 'timeout': 20}, AGUARDA]


def cap11():
    """Editar e cancelar: menu da assinatura > Editar (cliente travado) > Cancelar > Cancelar assinatura > Voltar; a assinatura segue Ativa."""
    c = Cap(11, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/financeiro/cobrancas'], setup=SETUP_ASSINATURAS)
    c.mark(1)
    c.click(ACOES_ASSINATURA, at=c.A(1, 'Editar', 1.6), label='menu ⋯ da assinatura')
    c.waitfor(target=ITEM('Editar'), timeout=8)
    c.click(ITEM('Editar'), at=c.A(1, 'Editar', 0.8), label='Editar')
    c.waitfor(text='O cliente não pode ser trocado depois que a recorrência é criada.', timeout=8)
    c.hover(P('O cliente não pode ser trocado', within=DLG), 0.4, at=c.A(1, 'cliente', 0.9), label='Cliente travado')
    c.mark(2)
    c.click(BTN('Cancelar', within=DLG), at=round(c.L(2) - 3.1, 2), label='Cancelar (fecha sem salvar)')
    c.pause(0.6)
    c.click(ACOES_ASSINATURA, at=c.A(2, 'Cancelar.', 1.4), label='menu ⋯ da assinatura')
    c.waitfor(target=ITEM('Cancelar'), timeout=8)
    c.click(ITEM('Cancelar'), at=c.A(2, 'Cancelar.', 0.5), label='Cancelar (abre a janela Cancelar assinatura)')
    c.waitfor(text='Esta ação não pode ser desfeita.', timeout=8)
    c.confere('body', ['Cancelar assinatura', 'as próximas cobranças desta assinatura deixam de ser geradas na Asaas', 'O histórico de cobranças já realizadas continua disponível no Financeiro'],
              'a janela Cancelar assinatura')
    c.hover(P('Ao cancelar, as próximas cobranças', within='[role=alertdialog],[role=dialog]'), 1.8, at=c.A(2, 'deixam', 0.9), label='aviso: as próximas cobranças deixam de ser geradas')
    c.mark(3)
    c.hover(BTN('Cancelar assinatura'), 0.3, at=round(c.L(3) - 0.4, 2), label='botões Cancelar assinatura e Voltar')
    c.click(BTN('Voltar'), at=c.A(3, 'Voltar', 0.9), label='Voltar')
    c.waitfor(gone={'text': 'Esta ação não pode ser desfeita.'}, timeout=8)
    c.confere('main', ['Academia Ponto Forte', 'Ativa'], 'a assinatura continua Ativa')
    c.mark(4)
    c.hover(SEL('main tbody tr', hasText='Academia Ponto Forte'), 2.0, at=c.A(4, 'lista', 0.5), label='a linha da assinatura (o selo de autorização ativa só aparece no Pix Automático)')
    c.fim()
    return c


SETUP_CONTRATO = SETUP_DASH + [{'do': 'goto', 'url': '/contratos'}, {'do': 'waitFor', 'text': 'PMOC - Hotel Mirante do Mar', 'timeout': 25}, AGUARDA,
                               {'do': 'click', 'target': MENU_LATERAL}, {'do': 'pause', 'seconds': 0.6},
                               {'do': 'click', 'target': TXT('PMOC - Hotel Mirante do Mar')}, {'do': 'waitFor', 'target': TAB('Financeiro'), 'timeout': 25}, AGUARDA,
                               {'do': 'click', 'target': TAB('Financeiro')}, {'do': 'waitFor', 'text': 'Mensalidade PMOC - jan/2027 (2/12)', 'timeout': 25}, AGUARDA]
COBRAR_ONLINE = {'selector': 'main button[aria-label="Cobrar online"]', 'nth': 0}   # a 1ª pendente é a jan/2027 (2/12): a dez/2026 já foi recebida (T13)


def cap12():
    """A parcela do contrato: Contratos > PMOC > Financeiro > Cobrar online da 2ª mensalidade > Gerar agora > selo Cobrança gerada; Cobrar o saldo em Contas a Receber."""
    c = Cap(12, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/contratos', '/financeiro/contas'], setup=SETUP_CONTRATO)
    c.mark(1)
    c.confere('main', ['Mensalidade PMOC - dez/2026 (1/12)', 'Pago', 'Mensalidade PMOC - jan/2027 (2/12)', 'Pendente'], 'a 1ª mensalidade paga e as seguintes Pendente')
    c.hover(COBRAR_ONLINE, 1.6, at=c.A(1, 'botão', 0.9), label='botão Cobrar online (só o ícone) ao lado da parcela')
    c.mark(2)
    c.click(COBRAR_ONLINE, at=c.A(2, 'Clico', 0.9), label='Cobrar online da 2ª mensalidade')
    c.waitfor(text='Esta cobrança é da parcela do contrato.', timeout=10)
    c.confere('dlg', ['Hotel Mirante do Mar', '1.200,00', 'O valor é o da parcela e não pode ser alterado.', '10/01/2027', 'Esta cobrança é da parcela do contrato. Quando o cliente pagar, a parcela é baixada automaticamente no seu financeiro, sem lançamento novo.'],
              'a janela já vem com o hotel, R$ 1.200,00 e o vencimento 10/01/2027')
    c.confere_ausente('dlg', 'Lançar no financeiro', 'sem a aba Financeiro')
    c.hover(P('Esta cobrança é da parcela do contrato.', within=DLG), 2.2, at=c.A(2, 'aviso:', 0.9), label='aviso: a própria parcela é baixada')
    c.mark(3)
    c.click(BTN('Gerar agora'), at=c.A(3, 'Gerar', 0.9), label='Gerar agora')
    c.waitfor(text='Aponte a câmera para pagar', timeout=15)
    c.click(BTN('Fechar'), at=c.A(3, 'selo', 1.0), label='Fechar o quadro com o link')
    c.waitfor(text='Cobrança gerada', timeout=10)
    c.confere('main', ['Cobrança gerada'], 'a parcela ganhou o selo Cobrança gerada')
    c.hover(P('Cobrança gerada'), 1.4, at=c.A(3, 'Cobrança', 1.3), label='selo Cobrança gerada na parcela')
    c.mark(4)
    c.add({'do': 'goto', 'url': '/financeiro/contas', 'at': round(c.L(4) - 0.4, 2), 'label': 'abre Contas a Pagar/Receber'})
    c.click(TAB('A Receber'), label='aba A Receber')
    c.waitfor(text='Orçamento #2 (1/3)', timeout=20)
    kebab = SEL("main tr:has-text('Orçamento #2 (1/3)') button[aria-haspopup='menu']")
    c.click(kebab, at=c.A(4, 'conta', 2.5), label='menu ⋮ da Orçamento #2 (1/3)')
    c.pause(0.6)
    c.click(kebab, label='menu ⋮ de novo (só se não abriu)', unless=ITEM('Cobrar o saldo'))
    c.waitfor(target=ITEM('Cobrar o saldo'), timeout=8)
    c.hover(ITEM('Cobrar o saldo'), 2.0, at=c.A(4, 'Cobrar', 0.9, nth=0), label='Cobrar o saldo (sem clicar)')
    c.press('Escape', label='fecha o menu')
    c.fim()
    return c


def cap13():
    """Recapitulando: base simples (Cobranças com a cobrança paga e a aba Assinaturas); os trechos da recapitulação entram na edição."""
    c = Cap(13, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/financeiro/cobrancas'], setup=SETUP_COBR_MENU)
    c.mark(1)
    c.hover(P('RECEBIDO'), 1.4, at=c.A(1, 'Recapitulando', 0.0), label='o quadro de Cobranças')
    c.mark(2)
    c.hover(SEL('main tbody tr', hasText='Restaurante Sabor da Serra'), 1.6, at=c.A(2, 'Gerou', 0.9), label='a cobrança Pago')
    c.mark(3)
    c.click(TAB('Assinaturas'), at=c.A(3, 'assinatura', 0.9), label='aba Assinaturas')
    c.hover(SEL('main tbody tr', hasText='Academia Ponto Forte'), 1.6, at=c.A(3, 'mensal', 0.9), label='a assinatura Ativa')
    c.mark(4)
    c.fim()
    return c
