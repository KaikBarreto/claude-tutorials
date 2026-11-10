

# ================================================================ capítulos
def cap00():
    """Abertura: o Dashboard; o cursor desce pelo menu lateral, abre o grupo Gestão e para em Contratos (sem clicar)."""
    c = Cap(0, pace=0.5, start=(760, 420), prewarm=PREWARM, setup=SETUP_DASH)
    c.mark(1)
    c.hover(LINK('Agenda'), 0.1, at=0.2, label='o cursor desce pelo menu lateral')
    c.click(BTN('Gestão'), at=c.A(1, 'receita', 0.6), label='grupo Gestão do menu')
    c.hover(LINK('Contratos'), 3.0, at=c.A(1, 'contratos', 0.8), label='o cursor para em Contratos (sem clicar)')
    c.mark(2)
    c.hover(LINK('Contratos'), 2.0, at=c.A(2, 'PMOC,', 0.9), label='Contratos no grupo Gestão (PMOC)')
    c.mark(3)
    c.hover(LINK('Contratos'), 2.0, at=c.A(3, 'Contratos', 0.9, nth=1), label='Contratos no menu (módulo Gestão de Contratos e PMOC)')
    c.mark(4)
    c.fim()
    return c


def cap01():
    """Onde fica o PMOC: Gestão > Contratos (lista vazia); botões do topo e busca; Filtros: Tipo (PMOC e Comum), Saúde e Status; Aplicar."""
    c = Cap(1, pace=0.5, start=(760, 420), prewarm=PREWARM, setup=SETUP_DASH)
    c.mark(1)
    c.click(BTN('Gestão'), at=c.A(1, 'Gestão,', 1.1), label='grupo Gestão do menu')
    c.click(LINK('Contratos'), at=c.A(1, 'Contratos.', 1.0), label='menu Contratos')
    c.waitfor(text='Nenhum contrato cadastrado', timeout=20)
    c.mark(2)
    c.hover(BTN('Configurações de Contrato'), 0.5, at=c.A(2, 'Configurações', 0.8), label='botão Configurações de Contrato')
    c.hover(BTN('Novo Contrato'), 0.5, at=c.A(2, 'Novo', 0.8), label='botão Novo Contrato')
    c.hover({'placeholder': 'Buscar por nome, cliente ou telefone...'}, 0.5, at=c.A(2, 'busca', 0.8), label='campo de busca')
    c.mark(3)
    c.click(BTNX('Filtros'), at=c.A(3, 'Filtros', 1.4), label='abre o painel Filtros')
    c.waitfor(text='Aplicar', timeout=8)
    c.hover(PD('Tipo', exact=True), 1.2, at=c.A(3, 'Tipo,', 0.9), label='filtro Tipo (PMOC e Comum)')
    c.mark(4)
    c.hover(PD('Saúde', exact=True), 0.9, at=c.A(4, 'Saúde', 0.9), label='filtro Saúde')
    c.hover(PD('Status', exact=True), 0.9, at=c.A(4, 'Status', 0.9), label='filtro Status')
    c.click(BTN('Aplicar'), at=round(c.dur - 2.4, 2), label='Aplicar (fecha o painel sem filtrar)')
    c.fim()
    return c


def cap02():
    """O Responsável Técnico: Configurações de Contrato (Documentos), aba Responsáveis Técnicos, Novo Responsável, assinatura desenhada, carimbo, Cadastrar."""
    c = Cap(2, pace=0.5, start=(760, 420), prewarm=PREWARM + ['/contratos'], setup=SETUP_LISTA)
    c.mark(1)
    c.click(BTN('Configurações de Contrato'), at=c.A(1, 'Abro', 0.9), label='Configurações de Contrato')
    c.waitfor(text='Documentos e responsáveis técnicos', timeout=15)
    c.hover(TXT('Modelos padrão de documentos PMOC'), 1.4, at=c.A(1, 'modelos', 0.9), label='Modelos padrão de documentos PMOC')
    c.scroll(TXT('Validade dos documentos'), at=c.A(1, 'Validade', 1.8), label='desce até Validade dos documentos', duration=1.0)
    c.hover(TXT('Validade dos documentos'), 1.6, at=c.A(1, 'Validade', 0.5), label='Validade dos documentos (12 meses)')
    c.mark(2)
    c.click(TAB('Responsáveis Técnicos'), at=c.A(2, 'segunda', 1.0), label='aba Responsáveis Técnicos')
    c.waitfor(text='Nenhum responsável técnico cadastrado', timeout=10)
    c.hover(BTN('Novo Responsável'), 1.4, at=c.A(2, 'engenheiro', 0.9), label='botão Novo Responsável')
    c.mark(3)
    c.click(BTN('Novo Responsável'), at=c.A(3, 'Clico', 1.0), label='Novo Responsável')
    c.waitfor(text='Novo Responsável Técnico', timeout=10)
    CAMPO = lambda ph: {'selector': f"{DLG} input[placeholder='{ph}']"}
    c.type(CAMPO('Ex: João da Silva'), 'Ricardo Tavares Albuquerque', at=c.A(3, 'Nome', 0.5), cps=15, label='Nome completo')
    c.type(CAMPO('Ex: CREA-SP 1234567'), 'CREA-RJ 9000012345', at=c.A(3, 'CFT', 0.4), cps=14, label='CFT/CREA')
    c.type(CAMPO('Ex: Engenheiro Mecânico'), 'Engenheiro Mecânico', at=c.A(3, 'Modalidade', 0.4), cps=16, label='Modalidade')
    c.type(CAMPO('Ex: ART 1234567/2026'), 'ART 9000001234/2026', at=c.A(3, 'Número', 0.4), cps=14, label='Número de registro')
    c.type(CAMPO('email@exemplo.com.br'), 'ricardo.tavares@glacialcold.example', at=c.A(3, 'Email', 0.4), cps=20, label='Email')
    c.type(CAMPO('(21) 99999-9999'), '2130001009', at=c.A(3, 'Telefone', 0.4), cps=10, label='Telefone')
    c.mark(4)
    c.hover(TAB('Enviar imagem'), 1.0, at=c.A(4, 'Assinatura', 0.9), label='aba Enviar imagem (recomendada)')
    c.click(TAB('Desenhar'), at=c.A(4, 'Desenhar', 1.0), label='aba Desenhar')
    c.waitfor(text='Desenhe acima usando o dedo, mouse ou caneta.', timeout=8)
    # assinatura: alguns arrastos curtos sobre o quadro (cada um parte de um ponto perto do centro)
    CANVAS = SEL(f'{DLG} canvas')
    for k, (x, y) in enumerate([(560, 508), (840, 524), (700, 490), (790, 536)]):
        c.drag(CANVAS, {'x': x, 'y': y}, at=round(c.A(4, 'assino', 0.7) + k * 0.5, 2) if k == 0 else None, label=f'assina no quadro ({k + 1})')
    c.click(BTN('Salvar imagem'), at=c.A(4, 'Salvar', 1.0), label='Salvar imagem')
    c.mark(5)
    c.upload(SEL(f'{DLG} button', hasText='Selecionar', nth=0), CARIMBO, at=c.A(5, 'envio', 1.0), label='Carimbo do responsável (Selecionar)')
    c.click(BTN('Cadastrar responsável'), at=c.A(5, 'Cadastrar', 1.0), label='Cadastrar responsável')
    c.waitfor(text='Ricardo Tavares Albuquerque', timeout=15)
    c.mark(6)
    c.hover(TXT('Ricardo Tavares Albuquerque', within='main'), 1.6, at=c.A(6, 'Ricardo', 0.9), label='o Ricardo na lista')
    c.fim()
    return c
