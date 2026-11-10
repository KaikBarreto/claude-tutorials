

# ---------------------------------------------------------------- o contrato do hotel (capítulos 10 a 13)
SETUP_CONTRATO = SETUP_LISTA + [
    {'do': 'click', 'target': LINHA('PMOC - Hotel Mirante do Mar')}, {'do': 'waitFor', 'text': 'Visão Geral', 'timeout': 25}, AGUARDA]


def abrir_contrato_hotel(c, at, label='abre o contrato PMOC - Hotel Mirante do Mar'):
    c.click(LINHA('PMOC - Hotel Mirante do Mar'), at=at, label=label)
    c.waitfor(text='Visão Geral', timeout=20)


def cap10():
    """O contrato por dentro: Filtros > Tipo PMOC; a linha do hotel (Saúde); o detalhe: abas, Visão Geral, Ocorrências, Ambientes e Equipamentos, Histórico PMOC, Financeiro."""
    c = Cap(10, pace=0.5, start=(760, 420), prewarm=PREWARM + ['/contratos'], setup=SETUP_LISTA)
    c.mark(1)
    c.click(BTNX('Filtros'), at=c.A(1, 'Filtros', 1.2), label='abre o painel Filtros')
    c.waitfor(text='Aplicar', timeout=8)
    c.click(SEL(f'{DLG} button, {DLG} label, {DLG} [role=checkbox]', hasText='PMOC', nth=0), at=c.A(1, 'PMOC:', 1.0), label='marca PMOC em Tipo')
    c.click(BTN('Aplicar'), at=c.A(1, 'sobra', 1.2), label='Aplicar')
    c.hover(LINHA('PMOC - Hotel Mirante do Mar'), 1.4, at=c.A(1, 'contrato', 0.9, nth=1), label='sobra só o contrato do hotel')
    c.hover(SEL('main thead th', hasText='Saúde'), 2.6, at=c.A(1, 'Saúde', 0.9), label='coluna Saúde')
    c.mark(2)
    abrir_contrato_hotel(c, c.A(2, 'Abro', 0.9))
    c.hover(BTNX('Editar contrato'), 0.8, at=c.A(2, 'Editar', 0.9), label='botão Editar contrato (sem clicar)')
    c.hover(BTNX('Excluir contrato'), 0.8, at=c.A(2, 'Excluir', 0.9), label='botão Excluir contrato (sem clicar)')
    for k, aba in enumerate(['Visão Geral', 'Ocorrências', 'Ambientes e Equipamentos', 'Histórico PMOC', 'Financeiro', 'Documentos', 'Cronograma']):
        c.hover(TAB(aba), 0.1, at=round(c.A(2, 'abas.', 0.2) + k * 0.4, 2) if k == 0 else None, label=f'aba {aba}', optional=True)
    c.mark(3)
    c.hover(TXT('Informações', within='main'), 1.2, at=c.A(3, 'Informações', 0.9), label='cartão Informações')
    c.hover(TXT('Resumo', within='main'), 1.4, at=c.A(3, 'Resumo,', 0.9), label='cartão Resumo')
    c.hover(TXT('Portal do Contrato', within='main'), 1.4, at=c.A(3, 'Portal', 0.9), label='cartão Portal do Contrato (só passa)')
    c.hover(TXT('Progresso', within='main'), 1.6, at=c.A(3, 'Progresso', 0.9), label='cartão Progresso')
    c.mark(4)
    c.click(TAB('Ocorrências'), at=c.A(4, 'Ocorrências,', 0.9), label='aba Ocorrências')
    c.hover(SEL('main tbody tr', nth=2), 1.6, at=c.A(4, 'Cada', 0.9), label='uma visita da lista (OS normal)')
    c.mark(5)
    c.click(TAB('Ambientes e Equipamentos'), at=c.A(5, 'Ambientes', 0.9), label='aba Ambientes e Equipamentos')
    c.mark(6)
    c.click(TAB('Histórico PMOC'), at=c.A(6, 'Histórico', 0.9), label='aba Histórico PMOC')
    c.mark(7)
    c.click(TAB('Financeiro'), at=c.A(7, 'Financeiro,', 0.9), label='aba Financeiro')
    c.hover(P('Marcar como pago'), 2.0, at=c.A(7, 'Marcar', 0.9), label='Marcar como pago (sem clicar)', optional=True)
    c.fim()
    return c


def cap11():
    """O cronograma do ano: aba Cronograma, Próximo período, etiquetas laranja, clique no dia, Dia/Semana/Mês, Imprimir PDF Anual (sem clicar)."""
    c = Cap(11, pace=0.5, start=(760, 420), prewarm=PREWARM + ['/contratos'], setup=SETUP_CONTRATO)
    c.mark(1)
    c.click(TAB('Cronograma'), at=c.A(1, 'Cronograma,', 0.9), label='aba Cronograma')
    c.click(BTN('Próximo período'), at=c.A(1, 'Avanço', 0.9), label='Próximo período (a primeira visita é em dezembro)')
    c.mark(2)
    c.hover(SEL('main [class*=bg-orange], main [class*=orange]', nth=0), 2.4, at=c.A(2, 'laranja', 0.9), label='etiqueta laranja (visita a fazer)', optional=True)
    c.mark(3)
    c.click(SEL('main [class*=bg-orange], main [class*=orange]', nth=0), at=c.A(3, 'Clicando', 0.9), label='clica no dia da visita', optional=True)
    c.click(TAB('Semana'), at=c.A(3, 'Semana', 0.9), label='Semana')
    c.click(TAB('Mês'), at=c.A(3, 'Mês.', 0.9), label='Mês')
    c.mark(4)
    c.hover(BTNX('Imprimir PDF Anual'), 3.4, at=c.A(4, 'Imprimir', 0.9), label='Imprimir PDF Anual (sem clicar)')
    c.fim()
    return c


def cap12():
    """Os documentos da norma: aba Documentos, Dossiê PMOC, Válido até, Gerar TRT individual, Histórico de versões, Planilha PMOC, Editar texto, Liberar documentos (sem clicar)."""
    c = Cap(12, pace=0.5, start=(760, 420), prewarm=PREWARM + ['/contratos'], setup=SETUP_CONTRATO)
    c.mark(1)
    c.click(TAB('Documentos'), at=c.A(1, 'aba', 0.9), label='aba Documentos')
    c.waitfor(text='Dossiê PMOC', timeout=15)
    c.hover(TXT('Documentos no portal do cliente', within='main'), 1.2, at=c.A(1, 'Pra', 0.8), label='cartão Documentos no portal do cliente')
    c.rolar(260, at=c.A(1, 'completar.', 1.2), label='desce pela aba', ponto=(760, 470), duration=0.7)
    c.mark(2)
    c.hover(P('Dossiê PMOC'), 2.2, at=c.A(2, 'Dossiê', 0.9), label='cartão Dossiê PMOC')
    c.hover(P('Assinado'), 1.6, at=c.A(2, 'Assinado', 0.9), label='selo Assinado', optional=True)
    c.mark(3)
    c.hover(P('Válido até'), 1.8, at=c.A(3, 'Válido', 0.9), label='Válido até do Termo e do Certificado', optional=True)
    c.click(BTN('Gerar TRT individual'), at=c.A(3, 'Gerar', 0.9), label='Gerar TRT individual')
    c.waitfor(text='TRT gerado!', timeout=15)
    c.mark(4)
    c.click(BTNX('Histórico de versões'), at=c.A(4, 'Histórico', 0.9), label='Histórico de versões', optional=True)
    c.hover(P('Planilha PMOC'), 2.4, at=c.A(4, 'Planilha', 0.9), label='Planilha PMOC (sem clicar)')
    c.mark(5)
    c.hover(BTNX('Editar texto', nth=0), 1.6, at=c.A(5, 'Editar', 0.9), label='Editar texto (sem clicar)', optional=True)
    c.mark(6)
    c.rolar(-900, at=c.A(6, 'Liberar', 1.8), label='volta ao topo da aba', ponto=(760, 470), duration=0.7)
    c.hover(BTNX('Liberar documentos no portal do cliente'), 3.0, at=c.A(6, 'Liberar', 0.9), label='Liberar documentos no portal do cliente (sem clicar)')
    c.fim()
    return c


def cap13():
    """Renovar, pausar e excluir: menu da linha (Pausar), Renovar / Estender (+6 meses > Cancelar), Excluir contrato (a lista do que sai > Cancelar)."""
    c = Cap(13, pace=0.5, start=(760, 420), prewarm=PREWARM + ['/contratos'], setup=SETUP_LISTA)
    c.mark(1)
    c.hover(LINHA('PMOC - Hotel Mirante do Mar'), 0.6, at=c.A(1, 'menu', 1.4), label='a linha do hotel')
    c.click(ACOES('PMOC - Hotel Mirante do Mar'), at=c.A(1, 'linha,', 1.0), label='menu da linha')
    c.pause(0.6)
    c.click(ACOES('PMOC - Hotel Mirante do Mar'), label='menu da linha de novo (só se não abriu)', unless=ITEM('Pausar'))
    c.hover(ITEM('Pausar'), 1.8, at=c.A(1, 'Pausar', 0.9), label='Pausar (sem clicar)')
    c.press('Escape', at=round(c.L(2) - 0.6, 2), label='fecha o menu')
    c.pause(0.5)
    c.mark(2)
    abrir_contrato_hotel(c, c.A(2, 'abro', 0.9))
    c.hover(BTNX('Renovar / Estender'), 0.8, at=c.A(2, 'Renovar', 1.0), label='botão Renovar / Estender')
    c.click(BTNX('Renovar / Estender'), at=c.A(2, 'Estender.', 0.9), label='abre Renovar / Estender')
    c.waitfor(text='Estender por', timeout=10)
    c.click(BTNX('+6 meses'), at=c.A(2, 'seis', 0.9), label='+6 meses', optional=True)
    c.click(BTNX('+12 meses'), at=c.A(2, 'doze', 0.9), label='+12 meses', optional=True)
    c.hover(PD('Horizonte atual'), 1.6, at=c.A(2, 'gera', 0.9), label='Horizonte atual e novo horizonte', optional=True)
    c.click(BTN('Cancelar'), at=c.A(2, 'Cancelar.', 0.9), label='Cancelar (fecha sem renovar)')
    c.mark(3)
    c.click(BTNX('Excluir contrato'), at=c.A(3, 'Excluir', 0.9, nth=1), label='abre Excluir contrato')
    c.waitfor(text='Serão excluídos junto com o contrato', timeout=10)
    c.hover(PD('ordens de serviço vinculadas'), 2.4, at=c.A(3, 'ordens', 0.9), label='a lista do que sai junto')
    c.hover(PD('Tenho certeza que desejo excluir'), 2.2, at=c.A(3, 'marcar', 0.9), label='caixa de confirmação (sem marcar)')
    c.click(BTN('Cancelar'), at=c.A(3, 'cancelo.', 0.9), label='Cancelar (fecha sem excluir)')
    c.fim()
    return c


def cap14():
    """Recapitulando: base simples (a lista de Contratos com os dois contratos); os trechos da recapitulação vêm da edição (montagem)."""
    c = Cap(14, pace=0.5, start=(760, 420), prewarm=PREWARM, setup=SETUP_LISTA)
    c.mark(1)
    c.hover(LINHA('PMOC - Hotel Mirante do Mar'), 1.6, at=c.A(1, 'PMOC', 0.9), label='a lista de Contratos (os dois contratos)')
    c.mark(2)
    c.hover(BTN('Novo Contrato'), 1.4, at=c.A(2, 'Um', 0.9), label='Novo Contrato')
    c.mark(3)
    c.mark(4)
    c.mark(5)
    c.fim()
    return c
