
# ---------------------------------------------------------------- alvos próprios do T20 (relatórios)
POPW = '[data-radix-popper-content-wrapper]'
OPC = lambda txt: SEL(f'{POPW} button', hasText=txt)                       # opção do filtro de período (popover)
ABA = lambda n: TAB(n)                                                      # abas do Relatórios
ESTA = BTN('Este mês')
MES_PASSADO = BTN('Mês passado')
CAIXA = TAB('Regime de Caixa')
COMPET = TAB('Regime de Competência')
LINHA = lambda txt: SEL('main button', hasText=txt)                         # linha clicável do DRE (grupo ou categoria)
DIA_ESQ = lambda d: SEL(f'{POPW} table >> nth=0 >> button:text-is("{d}") >> nth=0')   # dia do 1º mês do calendário de intervalo
MES_ANT = {'role': 'button', 'name': 'Go to previous month'}
MES_PROX = {'role': 'button', 'name': 'Go to next month'}
ESPERA_TAB = {'visao-geral': 'Visão geral dos relatórios', 'dre': 'Demonstrativo de Resultado', 'dfc': 'Saldo atual',
              'contabilidade': 'Pacote para Contabilidade', 'analise': 'Compara períodos'}


def setup_rel(tab='visao-geral', preset=None, regime=None, menu_aberto=False):
    """não filmado: abre Relatórios na aba, recolhe o menu lateral, escolhe o período e o regime que o capítulo anterior deixou"""
    s = SETUP_DASH + [{'do': 'goto', 'url': f'/financeiro/relatorios?tab={tab}'},
                      {'do': 'waitFor', 'text': ESPERA_TAB[tab], 'timeout': 25}, AGUARDA]
    if not menu_aberto:
        s += [{'do': 'click', 'target': MENU_LATERAL}, {'do': 'pause', 'seconds': 0.8}]
    if preset:
        s += [{'do': 'click', 'target': ESTA}, {'do': 'click', 'target': OPC(preset)}, AGUARDA, {'do': 'pause', 'seconds': 1.0}]
    if regime:
        s += [{'do': 'click', 'target': TAB(regime)}, AGUARDA, {'do': 'pause', 'seconds': 0.8}]
    return s


def periodo(c, de, para, at, label):
    c.click(BTN(de), at=at, label=f'abre o filtro de período ({label})')
    c.click(OPC(para), label=f'escolhe {para}')
    c.add({'do': 'waitFor', 'idle': True})


def intervalo(c, ini_voltas, dia_ini, fim_avancos, dia_fim, at, label, de='Este mês', tab_fim=0):
    """Personalizado: volta `ini_voltas` meses, marca `dia_ini` no 1º mês; avança `fim_avancos`, marca `dia_fim` (no mês `tab_fim` da tela); Aplicar"""
    c.click(BTN(de), at=at, label=f'abre o filtro de período ({label})')
    c.click(OPC('Personalizado'), label='Personalizado')
    c.waitfor(text='Selecione o período', timeout=8)
    for k in range(ini_voltas):
        c.click(MES_ANT, label=f'mês anterior ({k + 1})')
    c.click(DIA_ESQ(dia_ini), label=f'dia inicial {dia_ini}')
    for k in range(fim_avancos):
        c.click(MES_PROX, label=f'mês seguinte ({k + 1})')
    alvo = DIA_ESQ(dia_fim) if tab_fim == 0 else SEL(f'{POPW} table >> nth={tab_fim} >> button:text-is("{dia_fim}") >> nth=0')
    c.click(alvo, label=f'dia final {dia_fim}')
    c.click(BTN('Aplicar'), label='Aplicar o período')
    c.add({'do': 'waitFor', 'idle': True})


# Fase 2 (05/11, Opus): navegar meses do calendário sem cursor. Os 5 cliques de "mês anterior/seguinte" custavam ~3,7 s e atrasavam a L2
# do cap. 1 em 1,7 s (lição 40: etapas "aceleradas" por eval; o vídeo mostra o calendário pulando e só os dias levam cursor).
NAV_MES = ("(async()=>{const P='[data-radix-popper-content-wrapper]';const lab=%s;for(let i=0;i<%d;i++){"
           "const b=document.querySelector(P+' button[aria-label=\"'+lab+'\"]');if(!b)return 'sem botao '+lab;b.click();"
           "await new Promise(r=>setTimeout(r,170));}const p=document.querySelector(P);return p?p.innerText.replace(/\\s+/g,' ').slice(0,70):'sem calendario'})()")


def js_botao_dlg(texto):
    """clica, por eval, o botão da janela aberta cujo texto é exatamente `texto` (botão do rodapé fixo, fora da faixa do click)"""
    return ("(()=>{const b=[...document.querySelectorAll('[role=dialog] button')].find(x=>x.textContent.trim()===%s);"
            "if(!b)return 'sem botao';b.click();return 'clicou'})()") % json.dumps(texto, ensure_ascii=False)


def intervalo_rapido(c, ini_voltas, dia_ini, fim_avancos, dia_fim, at, label, de='Este mês', at_ini=None, at_fim=None, at_aplicar=None):
    """como `intervalo`, mas a troca de mês é por eval (sem cursor); os dias e o Aplicar levam cursor e `at` próprios"""
    c.click(BTN(de), at=at, label=f'abre o filtro de período ({label})')
    c.click(OPC('Personalizado'), label='Personalizado')
    c.waitfor(text='Selecione o período', timeout=8)
    if ini_voltas:
        c.ev(NAV_MES % (json.dumps('Go to previous month'), ini_voltas), label=f'volta {ini_voltas} meses no calendário (sem cursor)')
    c.click(DIA_ESQ(dia_ini), at=at_ini, label=f'dia inicial {dia_ini}')
    if fim_avancos:
        c.ev(NAV_MES % (json.dumps('Go to next month'), fim_avancos), label=f'avança {fim_avancos} meses no calendário (sem cursor)')
    c.click(DIA_ESQ(dia_fim), at=at_fim, label=f'dia final {dia_fim}')
    c.click(BTN('Aplicar'), at=at_aplicar, label='Aplicar o período')
    c.add({'do': 'waitFor', 'idle': True})


MOVER = lambda cat: SEL(f'{DLG} button[role=combobox][aria-label="Mover {cat} para outro grupo DRE"]')
NATUREZA = SEL(f'{DLG} button[role=combobox][aria-label="Natureza na DRE"]', nth=0)
PONTO_DLG = (700, 420)   # meio do corpo rolável da janela Configurar DRE (div.overflow-y-auto do ResponsiveModal)


def cap_novo(n, **kw):
    kw.setdefault('prewarm', ['/dashboard', '/financeiro/relatorios'])
    return Cap(n, pace=0.5, start=(760, 420), **kw)


# ================================================================ capítulos
def cap00():
    """Abertura: Dashboard, menu Financeiro > Relatórios, a câmera passa pelas cinco abas."""
    c = cap_novo(0, setup=SETUP_DASH)
    c.mark(1)
    c.hover(LINK('Agenda'), 0.1, at=0.3, label='o cursor passa pelo menu lateral')
    c.click(BTN('Financeiro'), at=c.A(1, 'Financeiro', 0.9), label='abre o grupo Financeiro do menu')
    c.click(LINK('Relatórios'), at=c.A(1, 'resultado', 0.9), label='abre Relatórios')
    c.waitfor(text='Visão geral dos relatórios', timeout=20)
    c.mark(2)
    for palavra, nome, nth in [('Visão', 'Visão Geral', 0), ('Resultado.', 'DRE - Resultado', 0), ('DFC', 'DFC - Fluxo de Caixa', 0),
                               ('Contabilidade', 'Contabilidade', 0), ('Análise.', 'Análise', 0)]:
        c.hover(ABA(nome), 0.5, at=c.A(2, palavra, 0.9, nth=1 if palavra == 'Visão' and False else 0), label=f'aba {nome}')
    c.mark(3)
    c.hover(ABA('Visão Geral'), 1.0, at=c.A(3, 'Vamos', 0.9), label='volta à Visão Geral')
    c.fim()
    return c


def cap01():
    """A visão geral: período Personalizado (ago a out), regime, cartões, gráfico e categorias."""
    c = cap_novo(1, setup=setup_rel('visao-geral'))
    c.mark(1)
    intervalo_rapido(c, 3, 1, 2, 31, at=0.4, label='ago a out', at_ini=c.A(1, 'escolho,', 0.4), at_fim=c.A(1, 'três', 0.9),
                     at_aplicar=c.A(1, 'fecharam.', 0.9))
    c.confere('main', ['01/08/2026', '31/10/2026'], 'período 01/08 a 31/10')
    c.mark(2)
    c.hover(P('Visão geral dos relatórios'), 0.8, at=c.A(2, 'Repara', 0.8), label='título Visão geral dos relatórios')
    c.hover(CAIXA, 1.0, at=c.A(2, 'Caixa,', 0.9), label='Regime de Caixa (marcado)')
    c.hover(COMPET, 0.8, at=c.A(2, 'competência.', 1.2), label='Regime de Competência')
    c.mark(3)
    c.confere('main', ['Margem', 'Faturamento', 'Resultado', 'R$ 47.900,00'], 'cartões do período (faturamento ago a out em Caixa)')
    c.hover(TXT('Faturamento'), 1.0, at=c.A(3, 'faturamento,', 0.9), label='cartões Margem, Faturamento e Resultado')
    c.hover(TXT('Margem'), 0.8, at=c.A(3, 'margem', 0.9, nth=0), label='cartão Margem')
    c.mark(4)
    c.rolar(380, at=c.A(4, 'gráfico', 0.9), label='desce até o gráfico Receita × despesa', duration=1.4)
    c.hover(P('Receita × despesa'), 0.8, at=c.A(4, 'dá', 0.9), label='gráfico Receita × despesa')
    c.mark(5)
    c.rolar(520, at=c.A(5, 'embaixo,', 0.9), label='desce até as categorias', duration=1.6)
    c.hover(P('Receitas por categoria'), 1.0, at=c.A(5, 'receita', 0.9), label='Receitas por categoria')
    c.hover(P('Despesas por categoria'), 1.0, at=c.A(5, 'despesa,', 0.9), label='Despesas por categoria')
    c.fim()
    return c


def cap02():
    """O resultado do mês: aba DRE, Mês passado, cartões, tabela, grupo Custos diretos aberto, % da receita."""
    c = cap_novo(2, setup=setup_rel('visao-geral'))
    c.mark(1)
    c.click(ABA('DRE - Resultado'), at=c.A(1, 'Agora', 0.9), label='aba DRE - Resultado')
    c.waitfor(text='Demonstrativo de Resultado', timeout=20)
    periodo(c, 'Este mês', 'Mês passado', c.A(1, 'escolho', 1.0), 'Mês passado')
    c.confere('main', ['Outubro de 2026', '(+) Receita Bruta', 'R$ 13.950,00'], 'DRE de outubro: receita bruta 13.950,00')
    c.mark(2)
    # a DRE desta versão não tem cartões nem gráfico no alto: a fala (emenda 1.38.21) cita o que existe em cima da tabela
    c.hover(BTN('Configurar DRE'), 0.4, at=c.A(2, 'Configurar', 0.9), label='Configurar DRE')
    c.hover(CAIXA, 0.4, at=c.A(2, 'regime,', 0.9), label='escolha do regime')
    c.hover(SEL('main label', hasText='Incluir projeções'), 0.4, at=c.A(2, 'Incluir', 0.9), label='Incluir projeções')
    c.hover(BTN('Exportar'), 0.4, at=c.A(2, 'Exportar.', 0.9), label='Exportar')
    c.mark(3)
    c.rolar(300, at=c.A(3, 'tabela', 0.9), label='a câmera desce pela tabela do DRE', duration=1.5)
    c.confere('main', ['= Receita Líquida', '= Lucro Bruto', '= Resultado Líquido'], 'linhas de resultado da tabela')
    c.rolar(260, at=c.A(3, 'Menos', 0.9, nth=0), label='continua descendo', duration=1.5)
    c.rolar(260, at=c.A(3, 'E,', 0.9), label='até o resultado líquido', duration=1.5)
    c.mark(4)
    c.rolar(-700, at=c.A(4, 'Clicando', 1.6), label='sobe até o custo dos serviços', duration=1.2)
    c.click(LINHA('Custos diretos'), at=c.A(4, 'grupo,', 0.9), label='abre Custos diretos')
    c.confere('main', ['CSP - Materiais', 'CSP - Mão de Obra Avulsa', 'Peças e componentes'], 'categorias de Custos diretos')
    c.hover(P('Peças e componentes'), 1.0, at=c.A(4, 'peças', 0.9, nth=0), label='Peças e componentes')
    c.mark(5)
    c.hover(P('% receita'), 1.4, at=c.A(5, 'coluna', 0.9), label='coluna % da receita')
    c.fim()
    return c


def cap03():
    """Organizar os grupos: Configurar DRE, Novo subgrupo (Despesas administrativas e Despesas com veículos), mover categorias."""
    c = cap_novo(3, setup=setup_rel('dre', preset='Mês passado'))
    c.mark(1)
    c.click(BTN('Configurar DRE'), at=c.A(1, 'Configurar', 0.9), label='abre Configurar DRE')
    c.waitfor(text='Novo subgrupo', timeout=15)
    c.confere('dlg', ['Organize os grupos', 'Novo subgrupo', 'Despesa operacional'], 'janela Configurar DRE')
    c.mark(2)
    c.hover(P('Despesas com pessoal', within=DLG), 1.4, at=c.A(2, 'Repara', 0.9), label='subgrupo Despesas com pessoal')
    c.hover(BTN('Editar Despesas com pessoal'), 1.2, at=c.A(2, 'lápis,', 0.9), label='lápis do subgrupo (sem clicar)')
    # Fase 2 (05/11): a janela rola por inteiro e cada alvo fora da parte visível custava ~2 s de rolagem automática; agora a roda
    # (rolar, ~1,1 s) vai antes da palavra, os nomes entram por "colar" (eram 2,1 a 4,6 s de digitação) e a L5 (3,65 s de fala) ganhou
    # um respiro de 2,6 s na voz (pausas.py 03 49.2:2.6): criar o 2º subgrupo e mover o combustível não cabem na frase.
    c.mark(3)
    c.rolar(-2400, at=round(c.L(3) - 0.85, 2), label='volta ao topo da janela', ponto=PONTO_DLG)
    c.select(NATUREZA, 'Despesa operacional', at=c.A(3, 'natureza', 1.2), label='natureza Despesa operacional')
    c.click(SEL('#new-dre-group-name'), at=c.A(3, 'nome,', 0.9), label='campo do nome do subgrupo')
    c.colar('Despesas administrativas', c.A(3, 'Despesas', 0.0), 'nome do subgrupo (colado)')
    c.click(BTN('Adicionar', within=DLG), at=c.A(3, 'Adicionar.', 0.8), label='Adicionar')
    c.waitfor(text='Nenhuma categoria neste grupo', timeout=10)
    c.mark(4)
    c.rolar(800, at=round(c.L(4) - 0.85, 2), label='desce até as despesas operacionais', ponto=PONTO_DLG)
    for cat, palavra, folga in [('Aluguel', 'aluguel', 0.9), ('Luz/Energia', 'categoria', 0.0), ('Ferramentas e Equipamentos', 'ferramentas', 1.1)]:
        c.select(MOVER(cat), 'Despesas administrativas', at=c.A(4, palavra, folga), label=f'move {cat} para Despesas administrativas')
    c.mark(5)
    c.rolar(-2400, at=round(c.L(5) - 0.85, 2), label='volta ao topo da janela (2º subgrupo)', ponto=PONTO_DLG)
    c.click(SEL('#new-dre-group-name'), at=round(c.L(5) - 0.85 + 1.0, 2), label='campo do nome do 2º subgrupo')
    c.colar('Despesas com veículos', c.A(5, 'Despesas', 0.05), 'nome do 2º subgrupo (colado)')
    c.click(BTN('Adicionar', within=DLG), at=c.A(5, 'veículos,', 0.5), label='Adicionar o 2º subgrupo')
    c.waitfor(text='Nenhuma categoria neste grupo', timeout=10)
    c.rolar(800, label='desce até o combustível', ponto=PONTO_DLG)
    c.select(MOVER('Combustível/Transporte'), 'Despesas com veículos', label='move Combustível/Transporte para Despesas com veículos')
    c.mark(6)
    c.rolar(640, at=c.A(6, 'Repara', 0.6), label='mostra os subgrupos novos', ponto=PONTO_DLG)
    c.rolar(3000, at=c.A(6, 'E,', 1.3), label='desce até o fim da janela', ponto=PONTO_DLG)
    c.hover(P('Precisa de outra forma de ver o DRE?', within=DLG), 0.4, at=c.A(6, 'precisar,', 0.6), label='quadro Precisa de outra forma de ver o DRE?')
    c.hover(BTN('Outras visões', within=DLG), 1.6, at=c.A(6, 'Outras', 0.8), label='botão Outras visões (sem clicar)')
    fechar_janela(c, c.L(7) - 1.3, 0.4)
    c.mark(7)
    c.confere('main', ['Despesas administrativas', 'Despesas com veículos'], 'subgrupos no DRE')
    c.hover(P('Despesas administrativas'), 0.8, at=c.A(7, 'dois', 1.4), label='Despesas administrativas')
    c.hover(P('Despesas com veículos'), 1.2, at=c.A(7, 'operacionais.', 1.2), label='Despesas com veículos')
    c.fim()
    return c


def cap04():
    """Caixa ou competência: dicas dos regimes, o mês passado nos dois regimes e Este mês em caixa."""
    c = cap_novo(4, setup=setup_rel('dre', preset='Mês passado'))
    c.mark(1)
    c.hover(CAIXA, 0.8, at=c.A(1, 'Agora', 0.9), label='botões dos regimes')
    # Fase 2 (05/11): o W() casa por prefixo e sem pontuação, então "Competência," (nth 0) era o "competência." da 1ª frase e
    # "caixa," (nth 0) era o "Caixa." de "Regime de Caixa." (a rolagem marcada para 22,8 s saiu 3,2 s atrasada): nth=1 nos dois.
    c.hover(COMPET, 2.4, at=c.A(1, 'Competência,', 0.9, nth=1), label='dica do Regime de Competência')
    c.mark(2)
    c.click(LINHA('Despesas administrativas'), at=c.A(2, 'competência,', 0.9), label='abre Despesas administrativas')
    c.confere('main', ['Ferramentas e Equipamentos', 'R$ 430,00'], 'Ferramentas e Equipamentos (parcela 1/3) no mês passado em competência')
    c.hover(P('(+) Receita Bruta'), 1.2, at=c.A(2, 'Condomínio', 0.9), label='Receita Bruta com a instalação do Condomínio')
    c.hover(P('Ferramentas e Equipamentos'), 1.0, at=c.A(2, 'bomba', 0.9), label='Ferramentas e Equipamentos')
    c.mark(3)
    c.click(CAIXA, at=c.A(3, 'Agora,', 0.9), label='Regime de Caixa')
    c.confere('main', ['Regime de Caixa: cada lançamento entra no mês em que o dinheiro entrou ou saiu da conta'], 'rodapé do Regime de Caixa')
    c.hover(P('(+) Receita Bruta'), 0.8, at=c.A(3, 'receita', 0.9), label='Receita Bruta em caixa (diminuiu)')
    c.hover(P('Despesas administrativas'), 1.0, at=c.A(3, 'bomba', 0.9), label='Despesas administrativas sem a bomba de vácuo')
    c.rolar(900, at=c.A(3, 'caixa,', 0.9, nth=1), label='até o rodapé', duration=1.6)
    c.hover(P('* Regime de Caixa'), 1.8, label='rodapé do Regime de Caixa')
    c.mark(4)
    c.rolar(-1200, at=c.A(4, 'foram', 0.9), label='volta ao topo', duration=1.0)
    periodo(c, 'Mês passado', 'Este mês', c.A(4, 'Este', 0.9), 'Este mês')
    c.click(LINHA('Despesas administrativas'), label='abre Despesas administrativas (se fechou)', optional=True, unless=P('Ferramentas e Equipamentos'))
    c.confere('main', ['Ferramentas e Equipamentos', 'R$ 430,00'], 'Este mês em caixa: a parcela paga com a fatura')
    c.hover(P('(+) Receita Bruta'), 1.2, at=c.A(4, 'condomínio', 0.9), label='Receita Bruta de Este mês com o Condomínio')
    c.hover(P('Ferramentas e Equipamentos'), 1.0, at=c.A(4, 'cartão', 1.2, nth=0), label='Ferramentas e Equipamentos em Este mês')
    c.mark(5)
    c.hover(CAIXA, 1.2, at=c.A(5, 'visões', 0.9), label='as duas visões')
    c.hover(COMPET, 1.2, at=c.A(5, 'Competência', 0.9, nth=0), label='Competência')
    c.hover(CAIXA, 1.2, at=c.A(5, 'caixa', 0.9), label='Caixa')
    c.fim()
    return c


def cap05():
    """A compra no cartão: três linhas de ilustração; na tela, o DRE de Este mês em caixa com Ferramentas e Equipamentos."""
    c = cap_novo(5, setup=setup_rel('dre', regime='Regime de Caixa'))
    c.mark(1)
    c.mark(2)
    c.mark(3)
    c.mark(4)
    # Fase 2 (05/11): o clique (1,7 s) ia a L(4) - 1,4 e atrasava a L4 em 1,2 s; agora sai 3 s antes, ainda sob a ilustração (repouso)
    c.click(LINHA('Despesas administrativas'), at=round(c.L(4) - 3.0, 2), label='abre Despesas administrativas')
    c.hover(P('Ferramentas e Equipamentos'), 1.6, at=c.A(4, 'bomba', 0.5), label='Ferramentas e Equipamentos')
    c.mark(5)
    c.rolar(520, at=c.A(5, 'transferência', 0.9), label='desce pela tabela: nada de transferência nem de fatura', duration=2.5)
    c.confere_ausente('main', 'Pagamento de Fatura', 'sem Pagamento de Fatura no DRE')
    c.confere_ausente('main', 'Transferência entre contas', 'sem Transferência entre contas no DRE')
    c.fim()
    return c


def cap06():
    """Comparar e projetar: Comparar períodos (Período anterior), depois Personalizado até o fim do mês seguinte com Incluir projeções."""
    c = cap_novo(6, setup=setup_rel('dre'))
    c.mark(1)
    periodo(c, 'Este mês', 'Mês passado', c.A(1, 'Volto', 0.9), 'Mês passado')
    c.click(BTN('Comparar períodos'), at=c.A(1, 'Comparar', 0.9), label='Comparar períodos')
    c.waitfor(text='Comparar com', timeout=10)
    # Fase 2 (05/11): "Período" (nth 0) era o "períodos." de "Comparar períodos." (o clique saía 1,6 s antes da fala); "Aplicar comparação"
    # e "Remover comparações" ficam no rodapé fixo da janela (y CSS ~723, fora da faixa 96..730): 2,2 a 2,4 s de rolagem em vão por
    # clique. Agora vão por clicar_fixo (cursor + eval). A comparação sai no "E agora pra frente" (L3), e não durante a L2, que fala dela.
    c.click(SEL(f'{DLG} button', hasText='Período anterior'), at=c.A(1, 'Período', 0.9, nth=1), label='Período anterior')
    c.clicar_fixo(BTN('Aplicar comparação'), (968, 723), js_botao_dlg('Aplicar comparação'), c.A(1, 'Aplicar', 0.2), 'Aplicar comparação')
    c.waitfor(gone={'role': 'dialog'}, timeout=10)
    c.confere('main', ['Setembro de 2026', 'Outubro de 2026', 'R$ 19.850,00', 'R$ 13.950,00'], 'colunas de setembro e outubro (receita bruta)')
    c.mark(2)
    c.hover(P('(+) Receita Bruta'), 1.8, at=c.A(2, 'Assim', 0.9), label='as duas colunas lado a lado')
    c.mark(3)
    # a comparação continua na tela e bagunça a projeção: tira antes de seguir (Comparar períodos > Remover comparações)
    c.click(BTN('Comparar períodos'), at=c.A(3, 'E', 0.2), label='Comparar períodos de novo')
    c.waitfor(text='Remover comparações', timeout=10)
    c.clicar_fixo(BTN('Remover comparações'), (323, 723), js_botao_dlg('Remover comparações'), round(c.L(3) + 1.4, 2), 'Remover comparações')
    c.waitfor(gone={'role': 'dialog'}, timeout=10)
    c.type(COMPET, '', noClick=True, label='Regime de Competência', optional=True, timeout=4)   # só o retângulo (destaque na edição)
    intervalo(c, 0, 1, 0, 31, at=round(c.L(3) + 1.7, 2), label='01/11 a 31/12', de='Personalizado', tab_fim=1)
    c.click({'role': 'switch', 'name': 'Incluir projeções'}, at=c.A(3, 'Ligado', 0.9), label='liga Incluir projeções')
    c.confere('main', ['1 ciclo(s) previsto(s)', 'R$ 380,00'], 'projeção de um ciclo de R$ 380,00')
    c.mark(4)
    c.rolar(900, at=c.A(4, 'rodapé,', 0.9), label='até o rodapé', duration=1.6)
    c.confere('main', ['Inclui R$ 380,00 de assinaturas identificadas como previstas; nenhuma transação foi criada.'], 'rodapé das projeções')
    c.hover(P('Inclui R$ 380,00'), 1.8, label='rodapé das projeções')
    c.fim()
    return c


def cap07():
    """O caixa dos próximos dias: DFC previsto, 30 dias, valor do dia, coluna Dívida."""
    c = cap_novo(7, setup=setup_rel('visao-geral'))
    c.mark(1)
    c.click(ABA('DFC - Fluxo de Caixa'), at=c.A(1, 'DFC,', 0.9), label='aba DFC - Fluxo de Caixa')
    c.waitfor(text='Saldo atual', timeout=20)
    c.confere('main', ['Saldo atual', 'A receber · 15 dias', 'A pagar · 15 dias', 'Dívidas a receber', 'Dívidas a pagar'], 'cartões do DFC previsto')
    c.hover(P('Saldo atual'), 1.2, at=c.A(1, 'saldo', 0.9, nth=0), label='Saldo atual')
    c.hover(P('A receber · 15 dias'), 1.2, at=c.A(1, 'entrar', 0.9), label='A receber e A pagar em 15 dias')
    c.mark(2)
    c.click(BTN('30 dias'), at=c.A(2, 'trinta', 0.9), label='30 dias')
    c.confere('main', ['Saldo inicial', 'Recebimentos', 'Total de saídas', 'Saldo final', 'Dívida'], 'matriz dia a dia')
    c.hover(P('Saldo inicial'), 1.0, at=c.A(2, 'saldo', 0.9, nth=0), label='Saldo inicial')
    c.hover(P('Recebimentos'), 1.0, at=c.A(2, 'entra,', 0.9), label='Recebimentos')
    c.hover(P('Total de saídas'), 1.0, at=c.A(2, 'sai,', 0.9), label='Total de saídas')
    c.mark(3)
    c.click(SEL('main td[role=button]', hasText='R$ 2.800,00'), at=c.A(3, 'valor,', 0.9), label='valor das saídas de hoje (aluguel)')
    c.waitfor(text='Total do dia', timeout=10)
    c.confere('dlg', ['Aluguel do galpão', 'R$ 2.800,00'], 'lista do dia com o aluguel')
    fechar_janela(c, c.A(3, 'Assim', 0.9))
    c.mark(4)
    c.hover(SEL('main thead th', hasText='Dívida'), 1.4, at=c.A(4, 'separado,', 0.9), label='coluna Dívida (vazia)')
    c.hover(P('Previsão otimista'), 2.0, at=c.A(4, 'vazia,', 0.9), label='texto Previsão otimista')
    c.fim()
    return c


def cap08():
    """O que de fato entrou e saiu: DFC Realizado, Mês passado, atividades, Exportar."""
    c = cap_novo(8, setup=setup_rel('dfc'))
    c.mark(1)
    c.click(BTN('Realizado'), at=0.2, label='Realizado')
    periodo(c, 'Este mês', 'Mês passado', 0.4, 'Mês passado')
    c.confere('main', ['Saldo inicial', 'Variação líquida', 'Saldo final'], 'cartões do DFC realizado')
    c.hover(P('Saldo inicial'), 0.4, at=c.A(1, 'saldo', 0.9, nth=0), label='Saldo inicial')
    c.hover(P('Variação líquida'), 0.4, at=c.A(1, 'variação', 0.9), label='Variação líquida')
    c.hover(P('Saldo final'), 0.4, at=c.A(1, 'fim.', 0.9), label='Saldo final')
    c.mark(2)
    c.rolar(420, at=c.A(2, 'entradas', 0.9), label='a câmera desce pelas atividades operacionais', duration=3.0)
    c.mark(3)
    c.rolar(-420, at=c.A(3, 'Exportar', 2.0), label='volta ao topo', duration=1.0)
    c.click(BTN('Exportar'), at=c.A(3, 'Exportar', 0.9), label='Exportar')
    c.waitfor(text='CSV', timeout=8)
    c.hover(ITEM('CSV'), 1.2, at=c.A(3, 'CSV.', 1.0), label='Excel, PDF e CSV')
    c.press('Escape', at=c.A(3, 'Uma', 0.6), label='fecha o menu sem escolher')
    c.fim()
    return c


def cap09():
    """O pacote do contador: aba Contabilidade em Mês passado, os quatro cartões, Exportar pacote."""
    c = cap_novo(9, setup=setup_rel('dfc', preset='Mês passado'))
    c.mark(1)
    c.click(ABA('Contabilidade'), at=c.A(1, 'aba', 0.9), label='aba Contabilidade')
    c.waitfor(text='Pacote para Contabilidade', timeout=20)
    c.confere('main', ['Pacote para Contabilidade', 'Excel multiabas', 'Período selecionado'], 'faixa do pacote')
    c.hover(P('Excel multiabas'), 1.4, at=c.A(1, 'Excel,', 0.9), label='selo Excel multiabas')
    c.mark(2)
    for texto, palavra in [('Lançamentos completos', 'lançamentos'), ('DRE e DFC reconciliados', 'DFC,'), ('Saldos e obrigações', 'saldos'), ('Plano gerencial', 'plano')]:
        c.hover(P(texto), 0.9, at=c.A(2, palavra, 0.9), label=texto)
    c.mark(3)
    c.hover(P('Período selecionado'), 1.0, at=c.A(3, 'período', 0.9), label='período selecionado')
    c.click(BTN('Exportar pacote'), at=c.A(3, 'clico', 0.9), label='Exportar pacote')
    c.waitfor(text='Pacote para Contabilidade exportado!', timeout=20)
    c.pause(2.0)
    c.fim()
    return c


def cap10():
    """Comparar meses e clientes: aba Análise, tabela, ranking por faturamento e por margem."""
    c = cap_novo(10, setup=setup_rel('dre'))
    c.mark(1)
    c.click(ABA('Análise'), at=c.A(1, 'última', 0.9), label='aba Análise')
    c.waitfor(text='Compara períodos', timeout=20)
    c.confere('main', ['Mês a mês', '3 meses', 'set/26', 'out/26', 'nov/26', 'Variação'], 'tabela de meses')
    c.hover(P('Período'), 1.4, at=c.A(1, 'mês', 0.9), label='tabela mês a mês')
    c.mark(2)
    c.rolar(520, at=c.A(2, 'Embaixo,', 0.9), label='desce até os clientes', duration=1.6)
    c.confere('main', ['Maior faturamento', 'Top 5', 'Hotel Mirante do Mar'], 'ranking por faturamento')
    c.hover(P('Hotel Mirante do Mar'), 1.4, at=c.A(2, 'Hotel', 0.9), label='Hotel Mirante do Mar em primeiro')
    c.mark(3)
    c.click(SEL('main button[role=combobox][aria-label="Ordenar clientes por"]'), at=c.A(3, 'trocando', 0.9), label='ordenar clientes por')
    c.click(OPT('Melhor margem'), at=c.A(3, 'margem,', 0.9), label='Melhor margem')
    c.confere('main', ['Padaria Bom Grão'], 'Padaria Bom Grão no ranking por margem')
    c.confere_ausente('main', 'Hotel Mirante do Mar', 'o hotel fora do Top 5 por margem')
    c.hover(P('Padaria Bom Grão'), 1.4, at=c.A(3, 'Padaria', 0.9), label='Padaria Bom Grão no topo')
    c.mark(4)
    c.hover(P('Custo direto'), 1.4, at=c.A(4, 'receita', 0.9), label='coluna Custo direto')
    c.fim()
    return c


def cap11():
    """Fechar o mês: DRE em Mês passado e Competência, zoom no período, no regime e em Exportar (Excel e PDF)."""
    c = cap_novo(11, setup=setup_rel('dre', preset='Mês passado'))
    c.mark(1)
    c.hover(MES_PASSADO, 0.3, at=0.0, label='período Mês passado')
    c.hover(COMPET, 0.3, at=max(0.6, c.A(1, 'fechar,', 0.9)), label='Regime de Competência')
    c.click(BTN('Exportar'), at=c.A(1, 'sai', 0.9), label='Exportar')
    c.waitfor(text='PDF', timeout=8)
    c.hover(ITEM('PDF'), 1.4, at=c.A(1, 'PDF,', 0.9), label='Excel e PDF')
    c.press('Escape', at=c.A(1, 'tela.', 0.4), label='fecha o menu sem escolher')
    c.mark(2)
    c.mark(3)
    c.hover(MES_PASSADO, 0.5, at=c.A(3, 'período', 0.9), label='período')
    c.hover(COMPET, 0.5, at=c.A(3, 'regime', 0.9), label='regime')
    c.fim()
    return c


def cap12():
    """Recapitulando: montagem pelas abas (Visão Geral, DRE, troca de regime, DFC, Contabilidade, Análise)."""
    c = cap_novo(12, setup=setup_rel('visao-geral'))
    c.mark(1)
    c.hover(P('Margem'), 1.2, at=c.A(1, 'visão', 0.9), label='Visão Geral')
    c.click(ABA('DRE - Resultado'), at=c.A(1, 'resultado,', 0.9), label='aba DRE')
    c.waitfor(text='Demonstrativo de Resultado', timeout=20)
    c.mark(2)
    c.click(CAIXA, at=c.A(2, 'caixa', 0.9, nth=0), label='Regime de Caixa')
    c.click(COMPET, at=c.A(2, 'aconteceu,', -0.6), label='Regime de Competência')
    c.mark(3)
    c.click(ABA('DFC - Fluxo de Caixa'), at=c.A(3, 'DFC', 0.9), label='aba DFC')
    c.waitfor(text='Saldo atual', timeout=20)
    c.click(ABA('Contabilidade'), at=c.A(3, 'pacote', 0.9), label='aba Contabilidade')
    c.mark(4)
    c.click(ABA('Análise'), at=c.A(4, 'Análise', 0.9), label='aba Análise')
    c.waitfor(text='Compara períodos', timeout=20)
    c.mark(5)
    c.hover(P('Maior faturamento'), 1.2, at=c.A(5, 'fiscal', 0.4), label='ranking de clientes', optional=True)
    c.fim()
    return c


CAPS = {n: globals()[f'cap{n:02d}'] for n in range(13)}

if __name__ == '__main__':
    quais = [int(a) for a in sys.argv[1:]] or sorted(CAPS)
    for n in quais:
        c = CAPS[n]()
        if os.environ.get('ANCHORS'):
            for i, w, t in c.anchors:
                print(f'   anchor L{i} "{w}" -> {t}')
        d = c.out()
        last = -1
        for stp in d['steps']:   # o `at` precisa ser crescente
            if 'at' in stp:
                if stp['at'] < last:
                    print(f'  aviso cap{n:02d}: at {stp["at"]} < {last} em "{stp.get("label") or stp.get("name")}"')
                last = max(last, stp['at'])
        path = os.path.join(HERE, f'cap{n:02d}.json')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
        print(f'cap{n:02d}: {len(d["steps"])} passos, narração {c.dur:.1f} s -> {os.path.relpath(path, HERE)}')
