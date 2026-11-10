

# ---------------------------------------------------------------- assistente do PMOC (capítulos 4 a 9): retomada do rascunho (sem filmar)
def rascunho_de(n):
    """rascunho que o capítulo `n` deixou no sessionStorage (rec/t11/colher.py n); sem ele o setup avisa e o ensaio falha de propósito"""
    p = os.path.join(RASC, f'cap{n:02d}.json')
    if not os.path.exists(p):
        print(f'  AVISO: falta {os.path.relpath(p, HERE)}: rode o capítulo {n} (--rapido) e `python3 -I rec/t11/colher.py {n}`')
        return None
    return json.load(open(p, encoding='utf8'))['draft']


def setup_retomar(n_anterior, avancar=0):
    """lista de Contratos > Novo Contrato > Retomar rascunho (o que o capítulo anterior deixou) > `avancar` cliques em Próximo"""
    raw = rascunho_de(n_anterior)
    passos = list(SETUP_LISTA)
    passos.append({'do': 'eval', 'js': f"(() => {{ sessionStorage.setItem('form-draft:contract-form', {json.dumps(raw if raw else '{}')}); return 'rascunho gravado'; }})()"})
    passos += [{'do': 'click', 'target': BTN('Novo Contrato')}, {'do': 'waitFor', 'text': 'Rascunho encontrado', 'timeout': 15},
               {'do': 'click', 'target': BTN('Retomar rascunho')}, {'do': 'waitFor', 'text': 'Dados do contrato', 'timeout': 15}, AGUARDA,
               {'do': 'pause', 'seconds': 1.0}]
    for _ in range(avancar):
        passos += [{'do': 'click', 'target': PROXIMO}, {'do': 'pause', 'seconds': 1.2}]
    return passos


def rascunho_fim(c):
    """último passo de um capítulo da cadeia do assistente: devolve o rascunho (rec/t11/colher.py o guarda)"""
    c.s_rascunho = True
    return c.ev(RASCUNHO, label='rascunho')


def cap04():
    """Ligando o PMOC: Novo Contrato > nome e cliente do hotel > chave "É um contrato PMOC?" > a Unidade e o RT aparecem em Dados do contrato (não avança)."""
    c = Cap(4, pace=0.5, start=(760, 420), prewarm=PREWARM, setup=SETUP_LISTA)
    c.mark(1)
    abrir_assistente(c, c.A(1, 'Clico', 1.6))
    c.mark(2)
    c.type(NOME_CONTRATO, 'PMOC - Hotel Mirante do Mar', at=c.A(2, 'PMOC,', 0.9), cps=18, label='Nome do Contrato')
    escolher_cliente(c, 'Hotel Mirante do Mar', 'Hotel', c.A(2, 'Cliente.', 1.0), c.A(2, 'próprio', 0.3), c.A(2, 'Mirante', 0.6, nth=1))
    c.mark(3)
    c.hover(CHAVE_PMOC, 1.2, at=c.A(3, 'chave', 0.9), label='chave É um contrato PMOC?')
    c.click(CHAVE_PMOC, at=c.A(3, 'Ligando,', 0.9), label='liga É um contrato PMOC?')
    c.mark(4)
    c.rolar(430, at=c.A(4, 'Repara', 0.6), label='desce até o RT e a Identificação da Unidade', ponto=(640, 470), duration=0.7)
    c.hover(PD('Identificação da Unidade'), 2.2, at=c.A(4, 'Unidade', 0.8), label='Identificação da Unidade')
    c.hover(SEL(f'{DLG} button', hasText='Revisão', nth=0), 1.2, at=c.A(4, 'cinco', 0.9), label='a barra segue com as cinco etapas')
    rascunho_fim(c)
    c.fim()
    return c


def cap05():
    """Unidade e RT: escolhe o Ricardo, a dica do ícone, o nome da unidade, o selo da lei e "O que o PMOC desbloqueia"; Próximo (Escopo técnico)."""
    c = Cap(5, pace=0.5, start=(760, 420), prewarm=PREWARM, setup=setup_retomar(4))
    c.mark(1)
    c.rolar(430, at=0.3, label='desce até o RT e a Identificação da Unidade', ponto=(640, 470), duration=0.7)
    c.click({'selector': f'{DLG} button[role=combobox]', 'hasText': 'Selecione o RT'}, at=c.A(1, 'escolho', 0.9), label='abre Responsável Técnico (RT)')
    c.click(OPT('Ricardo', exact=False), at=c.A(1, 'Ricardo,', 0.8), label='escolhe o Ricardo')
    c.hover(BTN('Cadastrar novo Responsável Técnico'), 1.4, at=c.A(1, 'botão', 0.8), label='botão + (Cadastrar novo Responsável Técnico, sem clicar)')
    c.mark(2)
    c.hover(BTN('O que é Responsável Técnico?'), 3.6, at=c.A(2, 'Passando', 0.9), label='ícone de informação do RT (a dica)')
    c.mark(3)
    c.rolar(260, at=c.A(3, 'Embaixo,', 0.8), label='desce até a Identificação da Unidade', ponto=(640, 470), duration=0.6)
    c.hover(PD('Endereço (logradouro)'), 1.6, at=c.A(3, 'endereço', 0.9), label='endereço da unidade')
    c.type({'placeholder': 'Ex: Loja Centro, Galpão 2…'}, 'Hotel Mirante do Mar - São Francisco', at=c.A(3, 'nome', 0.8, nth=0), cps=16, label='Nome da unidade / local')
    c.mark(4)
    c.rolar(300, at=c.A(4, 'Conforme', 1.0), label='desce até o selo da lei', ponto=(640, 470), duration=0.6)
    c.hover(PD('Conforme Lei Federal 13.589/2018'), 2.2, at=c.A(4, 'Conforme', 0.6), label='selo Conforme Lei Federal 13.589/2018')
    c.hover(PD('O que o PMOC desbloqueia'), 3.0, at=c.A(4, 'quadro', 0.9), label='quadro O que o PMOC desbloqueia')
    c.click(PROXIMO, at=round(c.dur - 1.6, 2), label='Próximo (Escopo técnico)')
    c.waitfor(text='Ambientes e equipamentos', timeout=10)
    rascunho_fim(c)
    c.fim()
    return c
