CARD_MENU = lambda num: SEL(f"{CARTAO(num)} button[aria-label='Ações da ordem']")
ALERTA = '[role=alertdialog]'
VIEW = lambda nome: SEL(f"button[aria-label='{nome}']")                                # Quadro / Lista / Calendário (ícones da barra)
COLUNA_CORPO = lambda t: SEL(f"main div.flex-col.rounded-xl:has(h3:text-is('{t}')) > div.p-2")   # área onde o cartão é solto
NEUTRO = (760, 470)


def ap(c, alvo, at, label, seg=0.25):
    """passeio por um elemento: hover curto (os menus que abrem no hover fecham quando o cursor sai: use `c.cursor(NEUTRO)` depois)"""
    return c.hover(alvo, seg, at=at, label=label)


@capitulo
def cap00():
    """Abertura: ilustração e cartões sobre o Dashboard; depois o menu Coletas & Logística > Ordens de Coleta."""
    c = Cap(0, start=(700, 430), setup=setup_em('/dashboard', aquece=['/coletas/ordens']))
    c.mark(1)
    c.cursor((720, 440), at=0.5, label='cursor em repouso no Dashboard')
    for i in (2, 3, 4):
        c.mark(i)
        c.flush(1e9)
    c.mark(5)
    c.click(GRUPO, at=c.A(5, 'Coletas', 0.9), label='abre Coletas & Logística', unless=ORDENS_MENU)
    c.click(ORDENS_MENU, at=c.A(5, 'Ordens', 0.8), label='Ordens de Coleta')
    c.waitfor(text=PAGINAS['/coletas/ordens'], timeout=15)
    c.cursor((760, 470), at=c.A(5, 'Antes', 0.2), label='cursor sai do menu (o quadro abre)')
    c.fim()
    return c


@capitulo
def cap01():
    """O que o módulo resolve: a câmera passa pelo quadro, sem clicar; as ilustrações cobrem as linhas 2 a 4."""
    c = Cap(1, start=(760, 420), setup=setup_em('/coletas/ordens'))
    c.mark(1)
    c.hover(COL_T('Agendada'), 0.6, at=c.A(1, 'buscar', 0.5), label='quadro: coluna Agendada')
    c.hover(CARD_TXT(8, 'Depósito Irmãos Siqueira'), 0.8, at=c.A(1, 'caçamba', 0.5), label='cartão da troca de caçamba (#8)')
    c.hover(CARD_TXT(7, 'Marcelo Tavares'), 0.8, at=c.A(1, 'combina', 0.5), label='cartão do Marcelo (#7)')
    c.cursor((760, 460), at=c.A(1, 'dele', 1.3), label='cursor em repouso')
    for i in (2, 3, 4):
        c.mark(i)
        c.flush(1e9)
    c.fim()
    return c


@capitulo
def cap02():
    """O quadro: colunas, cartões #8 e #7 (folhinha da data, selo Hoje), Lista, Calendário, Filtros, Nova ordem e a dica das concluídas."""
    c = Cap(2, start=NEUTRO, setup=setup_em('/coletas/ordens'))
    c.mark(1)
    for pal, col in (('Solicitada', 'Solicitada'), ('Agendada', 'Agendada'), ('caminho', 'A caminho'), ('Concluídas', 'Concluídas'), ('canceladas', 'Cancelada')):
        ap(c, COL_T(col), c.A(1, pal, FH), f'coluna {col}')
    c.confere_kpi([['Solicitada', '0'], ['Agendada', '1'], ['A caminho', '1'], ['Concluídas', '5'], ['Cancelada', '1']], 'contagem das colunas', rotulos='main h3')
    c.mark(2)
    c.hover(TXT('Nenhuma ordem', within='main'), 1.5, at=c.L(2) - 0.2, label='Solicitada vazia (Nenhuma ordem)')
    c.mark(3)
    ap(c, SEL(f"{CARTAO(8)} div[aria-label^='Ter']"), c.A(3, 'folhinha', FH), 'cartão #8: a folhinha da data')
    ap(c, CARD_TXT(8, '#8'), c.A(3, 'número', FH), 'cartão #8: número')
    ap(c, CARD_TXT(8, 'Depósito Irmãos Siqueira'), c.A(3, 'parceiro', FH), 'cartão #8: parceiro')
    ap(c, CARD_TXT(8, 'Manhã'), c.A(3, 'período', FH), 'cartão #8: período')
    ap(c, CARD_TXT(8, 'Edson Moura'), c.A(3, 'motorista', FH), 'cartão #8: motorista')
    ap(c, CARD_TXT(8, 'FKD2E41'), c.A(3, 'placa', FH), 'cartão #8: placa')
    c.hover(CARD_TXT(8, 'Hoje'), 1.0, at=c.A(3, 'Hoje', FH), label='cartão #8: selo Hoje')
    c.mark(4)
    ap(c, CARD_TXT(7, 'Tiago Freitas'), c.A(4, 'Tiago', FH), 'cartão #7: Tiago Freitas')
    ap(c, CARD_TXT(7, 'Marcelo Tavares'), c.A(4, 'Marcelo', FH), 'cartão #7: Marcelo Tavares')
    ap(c, CARD_TXT(7, 'Sem cadastro'), c.A(4, 'cadastro', FH), 'cartão #7: Sem cadastro')
    c.mark(5)
    c.click(VIEW('Lista'), at=c.A(5, 'Lista', FC), label='Lista')
    c.waitfor(selector='main table', timeout=10)
    c.hover(SEL("main th:has-text('Data / Janela')"), 0.3, at=c.A(5, 'título', FH), label='cabeçalho Data / Janela')
    c.click(SEL("main th:has-text('Data / Janela')"), at=c.A(5, 'data', FC), label='ordena por data')
    c.hover(SEL("main th:has-text('Origem')"), 0.8, at=c.A(5, 'sistema', FH), label='coluna Origem (Portal / Interna)')
    c.mark(6)
    c.click(VIEW('Calendário'), at=c.A(6, 'Calendário', FC), label='Calendário')
    c.waitfor(text='Hoje', timeout=10)
    c.click(TXT('Semana', within='main'), at=c.A(6, 'semana', FC), label='Calendário: Semana')
    c.click(TXT('Mês', within='main'), at=c.A(6, 'mês', FC), label='Calendário: Mês')
    c.hover(BTN('Hoje', within='main'), 1.0, at=c.A(6, 'Hoje', FH), label='botão Hoje')
    c.mark(7)
    c.click(VIEW('Quadro'), at=c.L(7) - 1.4, label='volta ao Quadro')
    c.waitfor(text='Solicitada', timeout=10)
    c.click(BTNX('Filtros', within='main'), at=c.A(7, 'Filtros', FC), label='Filtros')
    c.waitfor(text='Limpar Filtros', timeout=10)
    c.hover(TXTX('As solicitadas aparecem sempre, independente da data.', exact=True), 1.0, at=c.A(7, 'aviso', FH), label='aviso: as solicitadas aparecem sempre')
    c.hover(BTN('Limpar Filtros'), 0.8, at=c.A(7, 'Limpar', FH), label='Limpar Filtros')
    c.mark(8)
    c.press('Escape', at=c.L(8) - 0.3, label='fecha os Filtros')
    c.hover(NOVA_ORDEM, 0.8, at=c.A(8, 'Nova', FC), label='Nova ordem')
    c.mark(9)
    c.cursor(NEUTRO, at=c.A(9, 'anda', 0.35), label='cursor em repouso (a dica)')
    ap(c, COL_T('Concluídas'), c.A(9, 'Concluída', FH), 'dica: coluna Concluídas')
    ap(c, COL_T('Cancelada'), c.A(9, 'cancelada', FH), 'dica: coluna Cancelada')
    c.cursor(NEUTRO, at=c.A(9, 'registro', 0.35), label='cursor em repouso')
    c.fim()
    return c


@capitulo
def cap03():
    """Criar uma ordem: Nova ordem, as etapas, Cadastrado/Sem cadastro (campos), Tipo, Parceiro (Auto Peças Vale Forte), endereço do cadastro,
    Avançar, Material estimado e Observações."""
    c = Cap(3, start=(900, 300), setup=setup_em('/coletas/ordens'))
    c.mark(1)
    c.click(NOVA_ORDEM, at=c.A(1, 'Nova', F1), label='Nova ordem')
    c.waitfor(text='Nova ordem de coleta', timeout=10)
    ap(c, PASSO('Parceiro'), c.A(1, 'Parceiro', FH), 'etapa Parceiro')
    ap(c, PASSO('Coleta'), c.A(1, 'Coleta', FH), 'etapa Coleta')
    ap(c, PASSO('Frota'), c.A(1, 'Frota', FH), 'etapa Frota')
    c.mark(2)
    c.hover(TXTX('Cadastrado', within=DLG, exact=True), 0.5, at=c.A(2, 'Cadastrado', FH), label='Cadastrado')
    c.click(TXTX('Sem cadastro', within=DLG, exact=True), at=c.A(2, 'Sem', FC), label='Sem cadastro')
    c.waitfor(target=SEL('#ordem-nome-avulsa'), timeout=8)
    c.hover(TXTX('Nome do solicitante *', within=DLG, exact=True), 0.5, at=c.A(2, 'nome', FH), label='Nome do solicitante *')
    c.hover(TXTX('Telefone', within=DLG, exact=True), 0.5, at=c.A(2, 'telefone', FH), label='Telefone')
    c.hover(TXTX('Endereço completo', within=DLG), 1.2, at=c.A(2, 'endereço', FH), label='Endereço completo * obrigatório sem cadastro')
    c.click(TXTX('Cadastrado', within=DLG, exact=True), at=c.A(2, 'único', 0.2), label='volta para Cadastrado')
    c.mark(3)
    c.hover(SEL('#ordem-tipo'), 0.8, at=c.L(3) - 0.2, label='Tipo: Fornecedor')
    c.click(SEL('#ordem-tipo'), at=c.A(3, 'Se', 0.3), label='abre o Tipo (Fornecedor e Cliente)')
    c.hover(OPT('Cliente'), 0.9, at=c.A(3, 'Tipo', FH, nth=1), label='Tipo: a opção Cliente')
    c.press('Escape', at=c.A(3, 'No', 0.25), label='fecha o Tipo (continua Fornecedor)')
    c.click(SEL(f"{DLG} button:has-text('Selecionar')"), at=c.A(3, 'Parceiro', FJ), label='Parceiro: Selecionar…')
    c.waitfor(target=BUSCA_PARC, timeout=10)
    c.type(BUSCA_PARC, 'Vale Forte', label='busca Vale Forte', cps=40, noClick=True)
    c.click(BTNX('Auto Peças Vale Forte', within=f'{DLG} >> nth=-1'), at=c.A(3, 'Vale', FC), label='escolhe Auto Peças Vale Forte')
    c.mark(4)
    c.hover(PH('Rua, Avenida, etc.'), 1.0, at=c.A(4, 'endereço', FH), label='endereço do cadastro')
    c.hover(SEL(f"{DLG} button[role=combobox] >> nth=2"), 0.8, at=c.A(4, 'mudar', FH), label='endereço do cadastro (cidade)')
    c.mark(5)
    c.click(AVANCAR, at=c.A(5, 'Avançar', FC), label='Avançar')
    c.click(SEL('#ordem-material'), at=c.A(5, 'Material', FC), label='Material estimado (campo)')
    c.type(SEL('#ordem-material'), '~400 kg de radiadores e baterias', at=c.A(5, 'uns', 0.05), label='Material estimado', cps=40, noClick=True)
    c.mark(6)
    c.click(SEL('#ordem-obs'), at=c.A(6, 'Observações', FC), label='Observações (campo)')
    c.type(SEL('#ordem-obs'), 'Retirar pelo portão lateral', at=c.A(6, 'retirar', 0.05), label='Observações', cps=40, noClick=True)
    c.fim()
    return c


@capitulo
def cap04():
    """Data e janela: Data agendada 11/11/2026, Período (Não definido, Manhã, Tarde, Dia todo) -> Manhã, Avançar."""
    c = Cap(4, start=(900, 300), setup=setup_em('/coletas/ordens', extra=setup_nova_ordem(2)))
    c.mark(1)
    ap(c, TXTX('Data agendada', within=DLG), c.A(1, 'Data', FH), 'Data agendada')
    ap(c, SEL('#ordem-janela'), c.A(1, 'Período', FH, nth=1), 'Período')
    c.mark(2)
    c.click(SEL('#ordem-data'), at=c.A(2, 'amanhã', FC), label='Data agendada (campo)')
    c.type(SEL('#ordem-data'), '11112026', at=c.A(2, 'onze', 0.3), label='Data agendada 11/11/2026', cps=40, noClick=True)
    c.mark(3)
    c.click(SEL('#ordem-janela'), at=c.L(3) - 0.2, label='abre Período')
    c.hover(OPT('Tarde'), 2.2, at=c.A(3, 'tarde', FH), label='as janelas: Manhã, Tarde e Dia todo')
    c.hover(OPT('Não definido'), 1.5, at=c.A(3, 'Não', FH), label='Não definido: a ordem fica sem data')
    c.mark(4)
    c.click(OPT('Manhã'), at=c.L(4) - 0.2, label='escolhe Manhã')
    c.hover(SEL('#ordem-janela'), 1.5, at=c.A(4, 'Configurações', FH), label='Período: Manhã (as janelas vêm das Configurações)')
    c.mark(5)
    c.click(AVANCAR, at=c.L(5) - 0.2, label='Avançar para a Frota')
    c.waitfor(target=MOTORISTA, timeout=10)
    c.fim()
    return c


@capitulo
def cap05():
    """Motorista e veículo: o botão de mais, Jair Lopes e GHT7B19, a Revisão, Criar ordem e o cartão #9 em Agendada."""
    c = Cap(5, start=(900, 300), setup=setup_em('/coletas/ordens', extra=setup_nova_ordem(3)))
    c.mark(1)
    c.hover(MOTORISTA, 0.3, at=c.A(1, 'Motorista', FH), label='Motorista')
    c.hover(VEICULO, 0.6, at=c.A(1, 'Veículo', 0.8), label='Veículo')
    c.hover(SEL(f"{DLG} button:has(svg.lucide-plus) >> nth=0"), 1.2, at=c.A(1, 'mais', FH), label='o botão de mais (cadastra na hora)')
    c.mark(2)
    c.click(MOTORISTA, at=c.L(2) - 0.2, label='Motorista (campo)')
    c.type(MOTORISTA, 'Jair', label='digita Jair', cps=40, noClick=True)
    c.click(OPT('Jair Lopes'), label='escolhe Jair Lopes')
    c.click(VEICULO, label='Veículo (campo)')
    c.type(VEICULO, 'GHT', label='digita GHT', cps=40, noClick=True)
    c.click(OPT('GHT7B19'), label='escolhe GHT7B19')
    c.mark(3)
    c.hover(SEL(f"{DLG} div.rounded-md:has(> :text-is('Revisão'))"), 6.0, at=c.A(3, 'Revisão', FH), label='Revisão: parceiro, cidade, material, data e período')
    c.mark(4)
    c.click(BTN('Criar ordem'), at=c.L(4) - 0.2, label='Criar ordem')
    c.waitfor(text='Ordem de coleta criada', timeout=10)
    c.confere_item('main div.cursor-pointer.rounded-2xl', '#9', ['Auto Peças Vale Forte', 'Manhã', 'Jair Lopes', 'GHT7B19'], 'cartão #9 (fala: ordem nove, Jair, três quartos)')
    c.hover(CARD(9), 2.5, label='cartão #9 em Agendada (Jair e o GHT7B19)')
    c.mark(5)
    c.hover(CARD_TXT(9, 'Jair Lopes'), 2.0, at=c.L(5) - 0.2, label='cartão #9: motorista e veículo')
    c.fim()
    return c


def escolhe_teclado(c, trigger, letras, at=None, label=None, idx=0):
    """seletor Radix sem cursor (passo sem graça para a fala): foco por eval (o `idx`-ésimo `trigger`), Enter abre, a letra procura a opção,
    Enter escolhe (~0,5 s)"""
    c.ev(f"(()=>{{const t=[...document.querySelectorAll({json.dumps(trigger)})][{int(idx)}];if(!t)return 'SEM ALVO';t.focus();return 'foco'}})()", at=at,
         label=(label or trigger) + ' (foco)')
    c.press('Enter', label=(label or trigger) + ' (abre)')
    c.waitfor(selector='[role=listbox]', timeout=5)
    c.type(SEL('[role=listbox]'), letras, label=(label or trigger) + ' (procura)', cps=40, noClick=True)
    return c.press('Enter', label=label or trigger)


@capitulo
def cap06():
    """Acompanhar até concluir: #8 arrastado para A caminho, Preencher, Recolhi Caçamba 03, Entreguei Caçamba 05 e 10 bags, Concluir coleta,
    o relatório, Voltar às ordens, a ficha (Equipamentos movimentados e Histórico) e a ordem sem cadastro (#7)."""
    c = Cap(6, start=(760, 420), setup=setup_em('/coletas/ordens', extra=[{'do': 'eval', 'js': GPS_FICTICIO}]))
    c.mark(1)
    c.add({'do': 'drag', 'target': CARD_TXT(8, 'Depósito Irmãos Siqueira'), 'to': COLUNA_CORPO('A caminho'), 'at': c.A(1, 'arrastar', 2.2), 'label': 'arrasta o cartão #8 para A caminho'})
    c.waitfor(text='Status alterado para A caminho', timeout=10)
    c.waitfor(gone=CARD_BTN(8, 'A caminho'), timeout=10)   # o cartão já mudou de coluna (sem o botão A caminho)
    c.mark(2)
    c.click(CARD_BTN(8, 'Preencher'), at=c.A(2, 'Preencher', FJ), label='#8: Preencher')
    c.waitfor(text='Ordem #8', timeout=15)
    c.hover(TXTX('Agendamento', exact=True), 1.0, at=c.A(2, 'combinado', FH), label='tela da ordem: o combinado')
    c.mark(3)
    c.hover(TXTX('Equipamentos', exact=True), 0.3, at=c.L(3) - 0.2, label='bloco Equipamentos (Entreguei e Recolhi)')
    escolhe_teclado(c, 'button[role=combobox]', 'C', label='Recolhi: Caçamba 5 m³', idx=1)   # 2º seletor = Tipo do Recolhi
    c.click(SEL('button[role=combobox] >> nth=2'), at=c.A(3, 'Edson', FC), label='Recolhi: Unidade')
    c.click(OPT('Caçamba 03'), at=c.A(3, 'Caçamba', FC, nth=1), label='Recolhi: Caçamba 03')
    c.click(SEL("button:has-text('Adicionar') >> nth=1"), label='Recolhi: Adicionar')
    c.mark(4)
    escolhe_teclado(c, 'button[role=combobox]', 'C', label='Entreguei: Caçamba 5 m³', idx=0)   # 1º = Tipo do Entreguei
    c.click(SEL('button[role=combobox] >> nth=1'), at=c.L(4) - 0.2, label='Entreguei: Unidade (só as da base)')
    c.click(OPT('Caçamba 05'), at=c.A(4, 'base', FC), label='Entreguei: Caçamba 05')
    c.ev(js_clicar('button', 'Adicionar'), label='Entreguei: Adicionar (sem cursor)')
    c.mark(5)
    escolhe_teclado(c, 'button[role=combobox]', 'B', at=c.A(5, 'Depósito', 0.1), label='Entreguei: Bag 1 m³', idx=0)
    c.click(SEL("input[type=number]"), at=c.A(5, 'dez', 0.9), label='Quantidade (campo)')
    c.type(SEL("input[type=number]"), '10', at=c.A(5, 'dez', 0.3), label='Quantidade: 10', cps=40, noClick=True, clear=True)
    c.ev(js_clicar('button', 'Adicionar'), label='Entreguei: Adicionar os bags (sem cursor)')
    c.mark(6)
    c.clicar_fixo(SEL("div.fixed button:has-text('Concluir coleta')"), (800, 866), js_clicar('div.fixed button', 'Concluir coleta'),
                  c.A(6, 'Concluir', -0.9), 'Concluir coleta')
    c.waitfor(text='Relatório de Coleta 8', timeout=15)
    c.hover(TXTX('Relatório de Coleta 8', exact=True), 1.5, at=c.A(6, 'relatório', FH), label='Relatório de Coleta 8')
    c.mark(7)
    c.cursor((760, 460), at=c.A(7, 'concluir', 0.3), label='cursor em repouso (a dica)')
    c.mark(8)
    c.click(LINK('Voltar às ordens'), at=c.L(8) - 0.2, label='Voltar às ordens', noScroll=True)   # no topo: sem rolar
    c.waitfor(text=PAGINAS['/coletas/ordens'], timeout=15)
    c.hover(CARD_TXT(8, '#8'), 0.8, at=c.A(8, 'oito', FH), label='#8 em Concluídas')
    c.click(CARD_TXT(8, 'Depósito Irmãos Siqueira'), at=c.A(8, 'cartão', FC), label='abre a ficha da ordem 8')
    c.waitfor(text='Detalhes da ordem de coleta.', timeout=10)
    c.mark(9)
    c.hover(TXTX('Equipamentos movimentados', within=DLG, exact=True), 1.5, at=c.A(9, 'equipamentos', FH), label='Equipamentos movimentados')
    c.confere('dlg', ['Recolhido', 'Caçamba 03', 'Entregue', 'Caçamba 05', 'Bag 1 m³', 'A caminho → Concluída'], 'ficha da ordem 8 (caçambas 03 e 05 e bags)')
    c.mark(10)
    rola_ate(c, 'Histórico', c.L(10) - 0.2, 'ficha: Histórico', y=300, dur_ms=800, escopo=DLG)
    c.hover(TXTX('Histórico', within=DLG, exact=True), 2.0, at=c.A(10, 'mudança', FH), label='Histórico (cada mudança de etapa)')
    c.mark(11)
    c.press('Escape', at=c.L(11) - 0.3, label='fecha a ficha')
    c.click(CARD_BTN(7, 'Preencher'), at=c.A(11, 'coleta', FJ), label='#7: Preencher')
    c.waitfor(text='Ordem #7', timeout=15)
    c.hover(TXTX('Sem cadastro — ', within='body'), 2.2, at=c.A(11, 'avisa', FH), label='aviso: sem fornecedor ligado, sem caçamba')
    c.hover(BTNX('Cadastrar como fornecedor'), 1.5, at=c.A(11, 'botão', FH), label='botão Cadastrar como fornecedor')
    c.fim()
    return c


@capitulo
def cap07():
    """Editar, cancelar e excluir: menu Ações da ordem (#9), Editar (observação) e Salvar, Cancelada (Cancelar coleta? e Voltar), Excluir da #8 e
    a recusa (Não deu para excluir)."""
    c = Cap(7, start=NEUTRO, setup=setup_em('/coletas/ordens'))
    c.mark(1)
    c.click(CARD_MENU(9), at=c.A(1, 'três', FC), label='#9: Ações da ordem')
    c.hover({'role': 'menuitem', 'name': 'Visualizar'}, 0.3, at=c.A(1, 'Visualizar', FH), label='menu: Visualizar')
    c.hover({'role': 'menuitem', 'name': 'Editar'}, 0.3, at=c.A(1, 'Editar', FH), label='menu: Editar')
    c.hover({'role': 'menuitem', 'name': 'Excluir'}, 0.3, at=c.A(1, 'Excluir', FH), label='menu: Excluir')
    c.mark(2)
    c.click({'role': 'menuitem', 'name': 'Editar'}, at=c.A(2, 'Editar', FC), label='Editar')
    c.waitfor(target=SEL('#ordem-obs'), timeout=10)
    c.click(SEL('#ordem-obs'), at=c.A(2, 'observações', 1.3), label='Observações (campo)')
    c.press('End', label='vai ao fim do texto')
    c.type(SEL('#ordem-obs'), ' Ligar antes de chegar.', at=c.A(2, 'ligar', 0.05), label='Observações: Ligar antes de chegar', cps=40, noClick=True)
    c.hover(SEL('#ordem-janela'), 0.8, at=c.A(2, 'motorista', FH, nth=1), label='o resto também se edita')
    c.click(BTN('Salvar', within=DLG), at=c.A(2, 'Salvar', FC), label='Salvar')
    c.waitfor(text='Ordem de coleta atualizada', timeout=10)
    c.mark(3)
    c.click(CARD_BTN(9, 'Cancelada'), at=c.A(3, 'Cancelada', FC), label='#9: Cancelada')
    c.waitfor(text='Cancelar coleta?', timeout=8)
    c.hover(TXTX('Essa ação não pode ser desfeita.', within=ALERTA), 1.2, at=c.A(3, 'confirmação', FH), label='Cancelar coleta? (confirmação)')
    c.click(BTN('Voltar', within=ALERTA), at=c.A(3, 'volto', FC), label='Voltar (não cancela)')
    c.mark(4)
    c.click(CARD_MENU(8), at=c.A(4, 'Excluir', FC), label='#8: Ações da ordem')
    c.click({'role': 'menuitem', 'name': 'Excluir'}, label='Excluir')
    c.waitfor(text='Excluir ordem de coleta?', timeout=8)
    c.click(BTN('Excluir', within=ALERTA), at=c.A(4, 'Esta', FC), label='confirma o Excluir')
    c.waitfor(text='Não deu para excluir', timeout=10)
    c.hover(TXTX('Não dá para excluir a ordem de coleta', within=ALERTA), 1.0, at=c.A(4, 'explica', FH), label='Não deu para excluir: o motivo')
    c.click(BTN('Fechar', within=ALERTA), at=c.L(5) - 1.1, label='Fechar')
    c.mark(5)
    c.cursor(NEUTRO, at=c.A(5, 'dica', 0.3), label='cursor em repouso (a dica)')
    c.fim()
    return c


@capitulo
def cap08():
    """O relatório para o parceiro: Relatório da #8 (Copiar link, WhatsApp, Imprimir), Equipamentos, Relatório do Fornecedor na ficha, e o
    "Mostrar valores no relatório que o cliente abre" nas Configurações."""
    c = Cap(8, start=NEUTRO, setup=setup_em('/coletas/ordens'))
    c.mark(1)
    c.click(CARD_BTN(8, 'Relatório'), at=c.A(1, 'Relatório', F1), label='#8: Relatório')
    c.waitfor(text='Relatório de Coleta 8', timeout=15)
    c.hover(BTN('Copiar link'), 0.4, at=c.A(1, 'Copiar', FH), label='Copiar link')
    c.hover(BTNX('Compartilhar no WhatsApp'), 0.4, at=c.A(1, 'WhatsApp', FH), label='Compartilhar no WhatsApp (não clica)')
    c.hover(BTN('Imprimir'), 0.6, at=c.A(1, 'Imprimir', FH), label='Imprimir (não clica)')
    c.mark(2)
    c.click(BTN('Copiar link'), at=c.L(2) - 0.1, label='Copiar link (clica)')
    rola_ate(c, 'Equipamentos', c.A(2, 'recolhido', 0.6), 'desce a Equipamentos', y=260, dur_ms=800, escopo='body')
    c.hover(TXTX('Equipamentos', exact=True), 1.5, at=c.A(2, 'entregue', FH), label='Equipamentos do relatório')
    c.mark(3)
    rola_ate(c, 'Relatório de Coleta 8', c.L(3) - 3.4, 'sobe ao topo do relatório', y=140, dur_ms=800, escopo='body')   # a rolagem de volta ao topo dentro do clique custava ~5 s
    c.hover(LINK('Voltar às ordens'), 0.2, at=c.L(3) - 2.5, label='Voltar às ordens')
    c.ev('history.back()', at=c.L(3) - 1.6, label='volta ao quadro (sem recarregar o app)')   # voltar recarrega o app: ~5 s até o quadro aparecer   # a página foi rolada até Equipamentos: sem noScroll, o robô rola de volta ao topo
    c.waitfor(text=PAGINAS['/coletas/ordens'], timeout=15)
    c.click(CARD_TXT(8, 'Depósito Irmãos Siqueira'), label='abre a ficha da ordem 8')
    c.waitfor(text='Detalhes da ordem de coleta.', timeout=10)
    rola_ate(c, 'Relatório do fornecedor', c.L(3) + 0.2, 'ficha: Relatório do Fornecedor', y=280, dur_ms=800, escopo=DLG, prefixo=True)
    c.hover(BTNX('Abrir link do Fornecedor'), 0.8, at=c.A(3, 'Abrir', FH), label='Abrir link do Fornecedor (não clica)')
    c.mark(4)
    c.press('Escape', at=c.L(4) - 0.3, label='fecha a ficha')
    c.click(GRUPO, label='abre Coletas & Logística', unless=ITEM_MENU('Configurações'))
    c.click(ITEM_MENU('Configurações'), at=c.A(4, 'Configurações', 1.3), label='menu Configurações (Coletas)')
    c.waitfor(text=PAGINAS['/coletas/configuracoes'], timeout=15)
    rola_ate(c, 'Relatório público', c.A(4, 'Mostrar', 0.9), 'desce a Relatório público', y=200, dur_ms=800)
    c.hover(TXTX('Mostrar valores no relatório que o cliente abre', exact=True), 1.2, at=c.A(4, 'Mostrar', 0.1), label='Mostrar valores no relatório que o cliente abre')
    c.mark(5)
    c.hover(TXTX('O link do relatório é público', within='main'), 2.5, at=c.L(5) - 0.2, label='o aviso do link público')
    c.fim()
    return c
