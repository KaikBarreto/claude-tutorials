

# ---------------------------------------------------------------- trechos comuns deste tutorial
CHAVE = '$aact_exemplo_glacial_0000'   # chave FICTÍCIA (campo de senha: só pontos); a chave real nunca entra aqui
SETUP_COBRANCAS = SETUP_DASH + [{'do': 'goto', 'url': '/financeiro/cobrancas'}, {'do': 'waitFor', 'text': 'Cobranças e recorrências', 'timeout': 25}, AGUARDA]
ASAAS_URL = '/configuracoes?tab=integracoes&integration=asaas'
SETUP_ASAAS = SETUP_DASH + [{'do': 'goto', 'url': ASAAS_URL}, {'do': 'waitFor', 'text': 'Recebimentos (Asaas)', 'timeout': 25}, AGUARDA]
ROLA_PARA = ("(()=>{const t=%s;const el=[...document.querySelectorAll('main p, main h2, main h3, main label, main span')].find(e=>e.innerText&&e.innerText.trim().startsWith(t));"
             "if(!el)return 'sem '+t;el.scrollIntoView({behavior:'smooth',block:%s});return 'rolou'})()")


def rola_para(c, texto, at, label, bloco='center'):
    """rolagem suave (~1,6 s) da tela até o bloco que começa com `texto`; `at` = instante em que o `eval` dispara (antes da palavra)"""
    return c.ev(ROLA_PARA % (json.dumps(texto, ensure_ascii=False), json.dumps(bloco)), at=at, label=label)


# ================================================================ capítulos
def cap00():
    """Abertura: Dashboard, grupo Financeiro, item Cobranças: "Ative os recebimentos primeiro"."""
    c = Cap(0, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/financeiro/cobrancas'], setup=SETUP_DASH)
    c.mark(1)
    c.hover(LINK('Agenda'), 0.1, at=0.3, label='o cursor passa pelo menu lateral')
    c.click(BTN('Financeiro'), at=c.A(1, 'Financeiro.', 3.6), label='abre o grupo Financeiro do menu')
    c.mark(2)
    c.click(LINK('Cobranças'), at=c.A(2, 'Enquanto', 1.0), label='item Cobranças do grupo Financeiro')
    c.waitfor(text='Ative os recebimentos primeiro', timeout=20)
    c.hover(BTN('Ir para Integrações'), 1.4, at=c.A(2, 'ativar', 1.0), label='botão Ir para Integrações (sem clicar)')
    c.mark(3)
    c.hover(LINK('Cobranças'), 1.6, at=c.A(3, 'item', 0.9), label='o item Cobranças dentro do Financeiro')
    c.mark(4)
    c.fim()
    return c


def cap01():
    """Como o dinheiro chega: a ilustração entra na edição; por baixo, a tela Cobranças parada, com o cursor no item do menu."""
    c = Cap(1, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/financeiro/cobrancas'], setup=SETUP_COBRANCAS)
    c.mark(1)
    c.hover(BTN('Financeiro'), 1.0, at=c.A(1, 'cobrança', 0.9), label='o grupo Financeiro do menu')
    c.mark(2)
    c.mark(3)
    c.fim()
    return c


def cap02():
    """Conectar a conta: Configurações > Integrações > Cobranças (Asaas); a chave fictícia (só pontos); Ativar recebimentos; selo Ativo."""
    # a página de Configurações leva de 10 a 20 s para abrir com a máquina carregada (o clique no menu travava a tela e atrasava a voz toda): o capítulo já começa
    # nela (setup, não filmado) e o robô só passa o cursor pelo botão Configurações do menu
    c = Cap(2, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/configuracoes'],
            setup=SETUP_DASH + [{'do': 'goto', 'url': '/configuracoes'}, {'do': 'waitFor', 'text': 'Gerencie as configurações do sistema', 'timeout': 60}, AGUARDA])
    c.mark(1)
    c.hover(BTN('Configurações'), 0.2, at=c.A(1, 'Em', 3.5), label='Configurações, no rodapé do menu (a tela já está aberta: ver nota no cabeçalho; o 1º gesto custa ~7 s com a máquina carregada)')
    c.click(TAB('Integrações'), at=c.A(1, 'Integrações', 2.4), label='aba Integrações')
    c.click(TAB('Cobranças (Asaas)'), at=c.A(1, 'Cobranças.', 1.5), label='subaba Cobranças (Asaas)')
    c.waitfor(text='Recebimentos (Asaas)', timeout=15)
    c.confere('main', ['Cobre seus clientes por Pix, boleto e cartão usando sua própria conta Asaas.', 'Cole a chave de API da sua conta Asaas para ativar os recebimentos.',
                       'Como obter sua chave de API da Asaas', 'Ativar recebimentos'], 'o cartão pede a chave (sem selo de status)')
    c.mark(2)
    c.hover(P('Cole a chave de API da sua conta Asaas'), 1.8, at=c.A(2, 'ligação', 0.9), label='texto: cole a chave de API')
    c.hover(P('Como obter sua chave de API da Asaas'), 1.4, at=c.A(2, 'quadro', 0.9), label='quadro Como obter sua chave, com os quatro passos')
    c.mark(3)
    c.click({'placeholder': 'Cole aqui sua chave de API'}, at=c.A(3, 'colo', 1.2), label='campo Chave de API da Asaas')
    c.colar(CHAVE, at=c.A(3, 'colo', 0.3), label='cola a chave fictícia (campo de senha: só pontos)')
    c.ev("(()=>{const e=document.querySelector('#asaas-api-key');return e?e.type+' '+e.value.length+' caracteres':'sem campo'})()", label='o campo é de senha e recebeu a chave')
    c.hover(P('Chave de API da Asaas'), 1.4, at=c.A(3, 'pontinhos.', 1.2), label='o campo mostra só pontinhos')
    c.mark(4)
    c.click(BTN('Ativar recebimentos'), at=c.A(4, 'Ativar', 0.9), label='Ativar recebimentos')
    c.waitfor(text='Recebimentos ativos. Já é possível cobrar seus clientes.', timeout=15)
    c.confere('main', ['Ativo', 'Recebimentos ativos. Já é possível cobrar seus clientes.'], 'selo Ativo e a mensagem de recebimentos ativos')
    # no app real o cartão de taxas continua em "referência" depois de ativar (consulta guardada por 10 min, lida antes da ativação): a câmera não o filma assim;
    # o robô recarrega a página (corte na edição) e o cartão passa a mostrar as taxas da conta
    c.ev('location.reload()', at=c.A(4, 'Pronto,', 0.2), label='recarrega a página (o cartão de taxas só atualiza depois de recarregar)')
    c.waitfor(text='Taxas da sua conta Asaas, atualizadas em', timeout=25)
    c.waitfor(idle=True)
    c.confere('main', ['Ativo', 'Taxas da sua conta Asaas, atualizadas em'], 'depois de recarregar, o cartão mostra as taxas da conta (sem "referência")')
    c.confere_ausente('main', 'Taxas de referência', 'sem o aviso de taxas de referência')
    c.fim()
    return c


def cap03():
    """Para onde vai o dinheiro: aviso amarelo > Escolher agora > Conta Principal, Vendas de Serviços, Tarifas e Taxas > Salvar > os dois interruptores."""
    c = Cap(3, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/configuracoes'], setup=SETUP_ASAAS)
    c.mark(1)
    c.hover(P('Falta escolher a conta que recebe o dinheiro'), 1.6, at=c.A(1, 'aviso', 0.9), label='aviso amarelo: falta escolher a conta')
    c.click(TXT('Escolher agora'), at=c.A(1, 'Clico', 0.9), label='Escolher agora (a tela desce até o Lançamento no Financeiro)')
    c.mark(2)
    c.confere('main', ['Lançamento no Financeiro', 'Conta bancária de destino', 'Categoria da receita', 'Categoria da taxa (Asaas)'], 'a seção Lançamento no Financeiro')
    c.select({'selector': 'main button[role=combobox]', 'hasText': 'Escolha a conta'}, 'Conta Principal', at=c.A(2, 'Conta', 0.9), label='conta de destino: Conta Principal')
    # 1.38.19: "Categoria da receita" é um CAMPO DE TEXTO (placeholder "Nenhuma"), não uma lista: o filtro do app compara `type === 'income'` e o banco grava 'entrada'
    c.type({'selector': 'main input[placeholder="Nenhuma"]'}, 'Vendas de Serviços', at=c.A(2, 'receita', 1.0), cps=14, label='categoria da receita: Vendas de Serviços (campo de texto)')
    c.hover(P('Categoria da taxa (Asaas)'), 1.6, at=c.A(2, 'taxa', 0.9), label='categoria da taxa: Tarifas e Taxas')
    c.confere_campos('Tarifas e Taxas', 'categoria da taxa já vem em Tarifas e Taxas', escopo='main')
    c.mark(3)
    c.click(BTN('Salvar', nth='last'), at=c.A(3, 'Salvar.', 0.9), label='Salvar a seção Lançamento no Financeiro')
    c.waitfor(text='Configuração de lançamento salva.', timeout=8, optional=True)
    c.mark(4)
    rola_para(c, 'Lançar cobranças no Financeiro automaticamente', c.A(4, 'Repara', 1.6), 'a câmera sobe até os interruptores', bloco='center')
    c.hover(SW('Lançar cobranças no Financeiro automaticamente'), 1.4, at=c.A(4, 'primeiro', 0.9), label='interruptor: lançar cobranças no Financeiro')
    c.hover(SW('Lançar a taxa da Asaas como despesa'), 1.4, at=c.A(4, 'segundo', 0.9), label='interruptor: lançar a taxa da Asaas como despesa')
    c.fim()
    return c


def cap04():
    """Taxas e preferências: cartão Taxas da Asaas > Atualizar taxas > Multa e juros por atraso > Preferências de cobrança e Desconto por antecipação."""
    c = Cap(4, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/configuracoes'], setup=SETUP_ASAAS)
    c.mark(1)
    rola_para(c, 'Taxas da Asaas', c.A(1, 'Conta', 0.2), 'a câmera para no cartão Taxas da Asaas', bloco='start')
    c.confere('main', ['Taxas da Asaas', 'Pix', 'Boleto', 'Cartão de crédito', 'À vista (1x)', '2 a 6x', '7 a 12x', '13 a 21x', 'Antecipação',
                       'Prazo para o dinheiro cair', 'Taxas da sua conta Asaas, atualizadas em'], 'o cartão Taxas da Asaas com as faixas e o prazo')
    c.confere_ausente('main', 'não pagam tarifa', 'sem a nota de franquia do Pix (desmentiria a taxa do cap. 8)')
    c.hover(P('Taxas da Asaas'), 2.0, at=c.A(1, 'taxas', 0.9), label='cartão Taxas da Asaas')
    c.hover(P('Prazo para o dinheiro cair'), 0.6, at=c.A(1, 'prazo', 2.3), label='prazo pro dinheiro cair')
    c.mark(2)
    c.hover(P('As taxas são cobradas pela Asaas diretamente na sua conta.'), 1.8, at=c.A(2, 'sai', 0.9), label='nota: a Dominex não retém nada por transação')
    c.click(BTN('Atualizar taxas'), at=c.A(2, 'Atualizar', 2.0), label='Atualizar taxas')
    c.waitfor(text='Taxas atualizadas com a Asaas.', timeout=10, optional=True)
    c.mark(3)
    rola_para(c, 'Multa e juros por atraso', round(c.L(3) - 1.0, 2), 'a câmera desce até Multa e juros por atraso', bloco='center')
    c.confere_campos(['2', '1'], 'multa 2 e juros 1 ao mês', escopo='main')
    c.hover(P('Multa por atraso (%)'), 1.2, at=c.A(3, 'dois', 0.9), label='Multa por atraso (%) com 2')
    c.hover(P('Juros ao mês (%)'), 1.2, at=c.A(3, 'um', 0.9, nth=0), label='Juros ao mês (%) com 1')
    # 1.38.19: a dica "O limite máximo da Asaas é 10% ao mês." só aparece com juros acima de 10 (não com o 1 da conta): a câmera mostra o Salvar da seção
    c.hover(BTN('Salvar', nth=0), 0.4, at=c.A(3, 'salvar', 1.9), label='Salvar da seção Multa e juros por atraso (sem clicar)')
    c.mark(4)
    rola_para(c, 'Preferências de cobrança', round(c.L(4) - 1.0, 2), 'a câmera desce até Preferências de cobrança', bloco='start')
    c.hover(P('Meios de pagamento habilitados'), 1.6, at=c.A(4, 'meios', 0.9), label='Meios de pagamento habilitados')
    c.confere('main', ['Meios de pagamento habilitados', 'Pix', 'Boleto', 'Cartão de crédito'], 'Pix, boleto e cartão de crédito')
    rola_para(c, 'Desconto por antecipação', c.A(4, 'Desconto', 1.7), 'a câmera segue para Desconto por antecipação', bloco='center')
    c.hover(P('Desconto por antecipação'), 1.6, at=c.A(4, 'Desconto', 0.5), label='Desconto por antecipação')
    c.hover(P('Deixe em branco para não aplicar desconto.'), 1.6, at=c.A(4, 'Em', 0.9), label='em branco, não tem desconto')
    c.fim()
    return c


def cap05():
    """O simulador: botão Simulador > R$ 1.200,00 no cartão em 3x > resultado > Repassar ao cliente > Pix."""
    c = Cap(5, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/configuracoes'], setup=SETUP_ASAAS)
    c.mark(1)
    c.click(TAB('Simulador'), at=c.A(1, 'Simulador,', 0.9), label='botão Simulador, ao lado de Configurações')
    c.waitfor(text='Simulador de venda', timeout=10)
    c.mark(2)
    # 1.38.19: "Valor da venda" é um campo de texto SEM máscara (abre com 1000): digita "1200,00" por cima (com "120000" viraria R$ 120.000,00)
    c.digitar_num({'selector': '#sim-amount'}, '1200,00', at=c.A(2, 'mil', 0.9), label='Valor da venda: 1200,00')
    c.click(BTN('Cartão'), at=c.A(2, 'cartão,', 0.9), label='forma de pagamento: Cartão')
    c.select({'selector': 'main button[role=combobox]'}, '3x', at=c.A(2, 'três', 0.9), label='parcelas: 3x')
    c.mark(3)
    rola_para(c, 'Resultado da simulação', max(c.L(3) - 0.3, 0), 'a câmera desce até o Resultado da simulação', bloco='start')
    c.confere('main', ['Resultado da simulação', 'Valor bruto', 'R$ 1.200,00', 'Taxa da Asaas', 'Valor líquido na sua conta', 'R$ 1.157,63', 'Cada parcela para o cliente', 'R$ 400,00',
                       'Quando o dinheiro cai na sua conta', 'Parcela 3'], 'resultado: líquido R$ 1.157,63 e as três parcelas com a data')
    c.hover(P('Valor líquido na sua conta'), 0.5, at=c.A(3, 'valor', 1.2), label='Valor líquido na sua conta')
    rola_para(c, 'Quando o dinheiro cai na sua conta', c.A(3, 'embaixo,', 1.6), 'desce até Quando o dinheiro cai na sua conta (as três parcelas)', bloco='center')
    c.mark(4)
    rola_para(c, 'Valor da venda', round(c.L(4) - 1.5, 2), 'a câmera sobe até Quem paga a taxa', bloco='start')
    c.click(TXT('Repassar ao cliente'), at=round(c.L(4) + 0.1, 2), label='Repassar ao cliente')
    c.confere('main', ['O cliente paga', 'R$ 1.243,90', 'R$ 1.200,00'], 'no repasse o cliente paga mais e o líquido fica R$ 1.200,00')
    rola_para(c, 'Resultado da simulação', round(c.L(4) + 1.6, 2), 'a câmera desce até o resultado do repasse', bloco='start')
    c.hover(P('Valor líquido na sua conta'), 1.0, at=c.A(4, 'empresa', 0.5), label='o líquido fica igual ao valor da venda')
    c.mark(5)
    rola_para(c, 'Valor da venda', round(c.L(5) - 0.9, 2), 'sobe até Quem paga a taxa e a Forma de pagamento', bloco='start')
    c.click(TXT('A empresa absorve'), at=round(c.L(5) + 0.3, 2), label='volta para A empresa absorve')
    c.click(BTN('Pix'), at=round(c.L(5) + 1.3, 2), label='forma de pagamento: Pix')
    rola_para(c, 'Resultado da simulação', round(c.L(5) + 2.4, 2), 'desce até o resultado do Pix', bloco='start')
    c.confere('main', ['na hora', 'R$ 1.198,01'], 'no Pix o dinheiro cai na hora, líquido R$ 1.198,01')
    c.hover(P('Valor líquido na sua conta'), 0.3, at=round(c.L(5) + 2.7, 2), label='Valor líquido na sua conta (Pix) e na hora')
    c.hover(P('Estimativa. O valor final é calculado pela Asaas no momento da cobrança.'), 1.8, at=c.A(5, 'estimativa,', 1.6), label='dica: simulador é estimativa')
    c.fim()
    return c
