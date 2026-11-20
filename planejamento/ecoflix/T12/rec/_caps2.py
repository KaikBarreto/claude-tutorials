@capitulo
def cap09():
    """A coleta pedida pelo portal: o portal da Cooperativa Recomeço (aba Coletas, Ver relatório da coleta, Solicitar coleta de PET prensado,
    800 kg, 13/11, Tarde); de volta ao sistema, o ponto vermelho no menu, o cartão #10 "via portal", Recusar (só a janela), Aprovar e Agendar."""
    portal = f'/portal/{TOKEN_COOP}'
    c = Cap(9, start=(760, 420), setup=setup_em('/coletas/frota', extra=[{'do': 'goto', 'url': portal},
                                                                          {'do': 'waitFor', 'text': 'Cooperativa Recomeço', 'timeout': 30},
                                                                          {'do': 'waitFor', 'idle': True, 'timeout': 25}, {'do': 'wait', 'seconds': 0.8}]))
    c.mark(1)
    c.cursor((760, 440), at=0.5, label='cursor em repouso (ilustração)')
    c.mark(2)
    c.flush(1e9)
    c.mark(3)
    c.hover(TXTX('Cooperativa Recomeço', exact=True), 0.6, at=c.L(3) - 0.2, label='portal: Cooperativa Recomeço')
    c.click(SEL('#tab-btn-coletas'), at=c.A(3, 'aba', FC), label='aba Coletas')
    c.hover(TXTX('Minhas coletas', exact=True), 0.4, at=c.A(3, 'acompanha', 1.0), label='Minhas coletas')
    c.hover(TXTX('Ver relatório da coleta'), 0.9, at=c.A(3, 'relatório', FH), label='Ver relatório da coleta (das concluídas)')
    c.hover(BTN('Solicitar coleta'), 0.8, at=c.A(3, 'pede', FH), label='Solicitar coleta')
    c.mark(4)
    c.click(BTN('Solicitar coleta'), at=c.L(4) - 0.2, label='abre Solicitar coleta')
    c.waitfor(target=SEL('#coleta-material'), timeout=10)
    c.click(SEL('#coleta-material'), at=c.A(4, 'PET', FJ), label='Material (campo)')
    c.type(SEL('#coleta-material'), 'PET prensado', at=c.A(4, 'PET', 0.05), label='Material: PET prensado', cps=40, noClick=True)
    c.click(SEL('#coleta-qtd'), at=c.A(4, 'quantidade', FC), label='Quantidade estimada (campo)')
    c.type(SEL('#coleta-qtd'), '800 kg', at=c.A(4, 'quantidade', 0.05), label='Quantidade estimada: 800 kg', cps=40, noClick=True)
    c.mark(5)
    c.click(SEL('#coleta-data'), at=c.L(5) - 0.2, label='Data preferida (campo)')
    c.type(SEL('#coleta-data'), '13112026', at=c.A(5, 'sexta', 0.3), label='Data preferida 13/11/2026', cps=40, noClick=True)
    c.click(SEL('#coleta-janela'), label='abre Período')
    c.type(SEL('[role=listbox]'), 'T', label='Período: procura Tarde', cps=40, noClick=True)
    c.press('Enter', label='Período: Tarde')
    rola_ate(c, 'Endereço da coleta', c.A(5, 'endereço', 0.4), 'desce ao Endereço da coleta (do cadastro)', y=150, dur_ms=700, escopo=DLG)
    c.registra(SEL(f"{DLG} input[placeholder='Rua, Avenida, etc.']"), label='Endereço da coleta: Rua do Trabalho, 57 (do cadastro)')
    c.mark(6)
    c.click(BTN('Solicitar coleta', within=DLG), at=c.A(6, 'Solicitar', FC), label='Solicitar coleta (enviar)')
    c.waitfor(text='Solicitação enviada (#10)', timeout=10)
    c.mark(7)
    c.add({'do': 'goto', 'url': '/coletas/frota', 'at': round(c.L(7) - 0.2, 2), 'label': 'de volta ao sistema (Frota)'})
    c.waitfor(text=PAGINAS['/coletas/frota'], timeout=15)
    c.hover(GRUPO, 1.4, at=c.A(7, 'menu', FH), label='o ponto vermelho no menu Coletas & Logística')
    c.click(GRUPO, label='abre Coletas & Logística', unless=ORDENS_MENU)
    c.click(ORDENS_MENU, at=c.A(7, 'coluna', FC), label='Ordens de Coleta')
    c.waitfor(text=PAGINAS['/coletas/ordens'], timeout=15)
    c.hover(CARD(10), 1.0, at=c.A(7, 'pedido', FH), label='#10 na Solicitada')
    c.hover(CARD_TXT(10, 'via portal'), 0.8, at=c.A(7, 'via', FH), label='#10: via portal')
    c.mark(8)
    c.hover(CARD_BTN(10, 'Aprovar'), 0.3, at=c.A(8, 'aprovar', FH), label='Aprovar')
    c.click(CARD_BTN(10, 'Recusar'), at=c.A(8, 'recusa', FC, nth=1), label='Recusar #10')
    c.waitfor(text='Recusar solicitação?', timeout=8)
    c.hover(SEL('#reject-motivo'), 2.2, at=c.A(8, 'motivo', FH), label='Recusar solicitação: o Motivo')
    c.mark(9)
    c.click(BTN('Voltar', within=ALERTA), at=c.A(9, 'volto', FC), label='Voltar (não recusa)')
    c.click(CARD_BTN(10, 'Aprovar'), at=c.A(9, 'aprovo', FC), label='Aprovar #10')
    c.waitfor(text='Agendar coleta', timeout=10)
    c.hover(TXTX('Data da coleta *', within=DLG, exact=True), 2.0, label='Agendar coleta: a data e a janela do pedido')
    c.mark(10)
    c.click(BTN('Agendar', within=DLG), at=c.A(10, 'Agendar', FC), label='Agendar')
    c.waitfor(text='Status alterado para Agendada', timeout=10)
    c.hover(CARD(10), 1.5, at=c.A(10, 'marcada', FH), label='#10 em Agendada')
    c.fim()
    return c


# o grupo da página atual pode já vir aberto (o clique o fecharia): só clica se o link filho ainda não aparece (08-licoes, T5 cap. 17)
JS_ABRE_GRUPO = ("(()=>{if([...document.querySelectorAll('a')].some(a=>a.textContent.trim()==='Frota'&&a.offsetParent))return 'ja aberto';"
                 "const b=[...document.querySelectorAll('button')].find(b=>b.textContent.trim().startsWith('Coletas & Logística'));"
                 "if(!b)return 'SEM ALVO';b.click();return 'aberto'})()")
ABRE_GRUPO = [{'do': 'eval', 'js': JS_ABRE_GRUPO}, {'do': 'waitFor', 'target': ITEM_MENU('Frota'), 'timeout': 8}, {'do': 'wait', 'seconds': 0.5}]
LINHA_MENU = SEL("main tbody tr button:visible >> nth=0")   # 1.60.18: o menu da linha de Movimentações não tem aria-label
ACOES = lambda placa: SEL(f"main button[aria-label='Ações de {placa}']")


@capitulo
def cap10():
    """Veículos e motoristas: Frota (busca, filtros), o FKD2E41 (tara, capacidade, menu Editar/Excluir), Novo veículo FVL8A52 (aviso de toneladas)
    e Novo motorista Sérgio Paiva."""
    c = Cap(10, start=NEUTRO, setup=setup_em('/coletas/ordens', aquece=['/coletas/frota'], extra=ABRE_GRUPO))
    c.mark(1)
    c.click(ITEM_MENU('Frota'), at=c.A(1, 'Frota', F1, nth=1), label='menu Frota')
    c.waitfor(text=PAGINAS['/coletas/frota'], timeout=15)
    ap(c, TAB('Veículos'), c.A(1, 'veículos', FH), 'aba Veículos')
    ap(c, TAB('Motoristas'), c.A(1, 'motoristas', FH), 'aba Motoristas')
    c.hover(TXTX('Mesma frota usada na pesagem de compra/venda.', exact=True), 0.6, at=c.A(1, 'pesagem', FH), label='mesma frota da pesagem')
    c.hover(PH('Buscar placa, descrição ou RNT'), 1.4, at=c.A(1, 'buscar', FH), label='busca, filtro e ordenação da lista')
    c.mark(2)
    c.click(SEL("main button:has-text('FKD2E41'):has-text('Caminhão truck')"), at=c.A(2, 'caminhão', FC), label='FKD2E41')
    c.confere('main', ['6.380', '14.000'], 'FKD2E41: tara 6.380 e capacidade 14.000 (ilustração)')
    c.hover(SEL("main div:has(> h3:text-is('Capacidade operacional')) + div.grid"), 1.5, at=c.A(2, 'tara', FH), label='Tara e Capacidade do FKD2E41')
    c.hover(ACOES('FKD2E41'), 2.0, at=c.A(2, 'Editar', FH), label='menu de três pontinhos: Editar e Excluir')
    c.cursor(NEUTRO, at=c.A(2, 'pontinhos', -0.6), label='tira o cursor do menu')
    c.press('Escape', label='fecha o menu da linha')   # o menu abre por hover e o cursor teleportado não o fecha: sem isso ele cobre o Novo veículo
    c.mark(3)
    c.flush(1e9)
    c.mark(4)
    c.click(BTN('Novo veículo'), at=c.A(4, 'Novo', FC), label='Novo veículo')
    c.waitfor(target=SEL('#veiculo-placa'), timeout=10)
    c.click(SEL('#veiculo-placa'), label='Placa (campo)')
    c.type(SEL('#veiculo-placa'), 'FVL8A52', at=c.A(4, 'placa', 0.05), label='Placa FVL8A52', cps=40, noClick=True)
    c.click(SEL('#veiculo-descricao'), label='Descrição / Apelido (campo)')
    c.type(SEL('#veiculo-descricao'), 'Caminhão poliguindaste', label='Descrição: Caminhão poliguindaste', cps=40, noClick=True)
    c.mark(5)
    c.click(SEL('#veiculo-uf'), at=c.A(5, 'São', FC), label='abre UF de licenciamento')
    c.type(SEL('[role=listbox]'), 'SP', label='UF: procura SP', cps=40, noClick=True)
    c.press('Enter', label='UF: SP')
    rola_ate(c, 'Tipo de rodado', None, 'desce a janela do veículo', y=420, dur_ms=500, escopo=DLG)
    escolhe_teclado(c, '#veiculo-categoria', 'V', at=c.A(5, 'único', 0.3), label='Tipo: Veículo único')
    escolhe_teclado(c, '#veiculo-rodado', 'To', at=c.A(5, 'toco', 0.3), label='Tipo de rodado: Toco')
    c.mark(6)
    c.click(SEL('#veiculo-tara'), at=c.A(6, 'tara', FC), label='Tara (campo)')
    c.type(SEL('#veiculo-tara'), '7', at=c.A(6, 'sete', 0.05), label='Tara (kg) 7 (o aviso das toneladas)', cps=40, noClick=True)
    c.hover(TXTX('Valor parece estar em toneladas', within=DLG), 2.0, at=c.A(6, 'avisa', FH), label='aviso: o valor parece estar em toneladas')
    c.click(SEL('#veiculo-tara'), at=c.A(6, 'sete', FC, nth=1), label='Tara (campo, de novo)')
    c.type(SEL('#veiculo-tara'), '7100', at=c.A(6, 'sete', 0.05, nth=1), label='Tara (kg) 7100', cps=40, noClick=True, clear=True)
    c.click(SEL('#veiculo-cap-kg'), at=c.A(6, 'oito', FC), label='Capacidade (campo)')
    c.type(SEL('#veiculo-cap-kg'), '8500', at=c.A(6, 'oito', 0.05), label='Capacidade (kg) 8500', cps=40, noClick=True)
    c.mark(7)
    c.clicar_fixo(SEL(f"{DLG} button:has-text('Cadastrar')"), (1000, 800), js_clicar(f'{DLG} button', 'Cadastrar'), c.A(7, 'Cadastrar', 0.1),
                  'Cadastrar veículo')
    c.waitfor(text='Veículo cadastrado', timeout=10)
    c.hover(SEL("main button:has-text('FVL8A52')"), 1.0, at=c.A(7, 'poliguindaste', FH), label='FVL8A52 na frota')
    c.mark(8)
    c.click(TAB('Motoristas'), at=c.A(8, 'aba', FC), label='aba Motoristas')
    c.click(BTN('Novo motorista'), at=c.A(8, 'Novo', FC), label='Novo motorista')
    c.waitfor(target=SEL('#motorista-nome'), timeout=10)
    c.mark(9)
    c.click(SEL('#motorista-nome'), at=c.L(9) - 0.2, label='Nome (campo)')
    c.type(SEL('#motorista-nome'), 'Sérgio Paiva', label='Nome: Sérgio Paiva', cps=40, noClick=True)
    c.click(SEL('#motorista-doc'), at=c.A(9, 'CPF', FC), label='CPF (campo)')
    c.type(SEL('#motorista-doc'), '46371820508', label='CPF', cps=40, noClick=True)
    c.press('Tab', label='vai ao Telefone')
    c.type(SEL('#motorista-tel'), '12900004417', label='Telefone', cps=40, noClick=True)
    c.mark(10)
    c.click(SEL('#motorista-cnh'), at=c.A(10, 'CNH', FC), label='CNH (campo)')
    c.type(SEL('#motorista-cnh'), '04581273671', at=c.A(10, 'número', 0.05), label='CNH', cps=40, noClick=True)
    c.click(SEL('#motorista-cnh-cat'), label='abre Categoria')
    c.type(SEL('[role=listbox]'), 'C', label='Categoria: procura C', cps=40, noClick=True)
    c.press('Enter', label='Categoria C')
    c.click(SEL('#motorista-cnh-val'), at=c.A(10, 'validade', FC), label='Validade da CNH (campo)')
    c.type(SEL('#motorista-cnh-val'), '18062030', label='Validade da CNH 18/06/2030', cps=40, noClick=True)
    c.mark(11)
    c.click(BTN('Cadastrar', within=DLG), at=c.A(11, 'Cadastrar', 1.0), label='Cadastrar motorista')
    c.waitfor(text='Motorista cadastrado', timeout=10)
    c.hover(SEL("main button:has-text('Sérgio Paiva')"), 1.5, at=c.A(11, 'escalado', FH), label='Sérgio Paiva na lista')
    c.fim()
    return c


@capitulo
def cap11():
    """As caçambas e onde estão: Equipamentos, tipos, Novo tipo (Palete), unidades, Caçamba 02 em manutenção, Nova unidade Caçamba 06, Movimentar
    (Externo -> Minha base), Onde tudo está agora (saldo dos bags) e a aba Movimentações."""
    c = Cap(11, start=NEUTRO, setup=setup_em('/coletas/ordens', aquece=['/coletas/equipamentos'], extra=ABRE_GRUPO))
    c.mark(1)
    c.click(ITEM_MENU('Equipamentos'), at=c.A(1, 'Equipamentos', F1), label='menu Equipamentos')
    c.waitfor(text=PAGINAS['/coletas/equipamentos'], timeout=15)
    c.hover(TXTX(PAGINAS['/coletas/equipamentos'], exact=True), 0.6, at=c.A(1, 'bags', FH), label='caçambas, bags, caixas e paletes')
    c.mark(2)
    c.hover(TXTX('Tipos de equipamento', within='main', exact=True), 0.3, at=c.L(2) - 0.2, label='Tipos de equipamento')
    c.hover(SEL("main tr:has-text('Caçamba 5 m³')"), 2.0, label='Caçamba 5 m³: uma a uma')
    c.hover(SEL("main tr:has-text('Bag 1 m³')"), 2.0, at=c.A(2, 'bag', FH), label='Bag 1 m³: por quantidade')
    c.mark(3)
    c.click(BTN('Novo tipo'), at=c.A(3, 'tipo', FC), label='Novo tipo')
    c.waitfor(target=SEL('#tipo-nome'), timeout=10)
    c.click(SEL('#tipo-nome'), label='Nome (campo)')
    c.type(SEL('#tipo-nome'), 'Palete de madeira', at=c.A(3, 'palete', 0.1), label='Nome: Palete de madeira', cps=40, noClick=True)
    c.hover(SEL('#tipo-identificavel'), 2.0, at=c.A(3, 'desligada', FH), label='chave: Cada unidade tem identificação própria (desligada)')
    c.click(BTN('Cadastrar', within=DLG), at=c.A(3, 'caçamba', FC, nth=1), label='Cadastrar o tipo')
    c.waitfor(gone=SEL(DLG), timeout=10)
    c.mark(4)
    rola_ate(c, 'Unidades identificáveis', c.L(4) - 0.2, 'desce às Unidades identificáveis', y=140)
    c.confere_item('main [role=listitem]', 'Caçamba 05', ['Depósito Irmãos Siqueira'], 'Caçamba 05 no Depósito Irmãos Siqueira')
    c.hover(SEL("main [role=listitem]:has-text('Caçamba 05')"), 0.6, at=c.A(4, 'Caçamba', FH), label='Caçamba 05')
    c.hover(SEL("main [role=listitem]:has-text('Caçamba 05') :text-is('Depósito Irmãos Siqueira')"), 1.5, at=c.A(4, 'Depósito', FH),
            label='Caçamba 05 no Depósito Irmãos Siqueira')
    c.mark(5)
    c.click(SEL("main [role=listitem]:has-text('Caçamba 02')"), at=c.A(5, 'Caçamba', FC), label='Caçamba 02')
    c.click(BTN('Editar', within='main'), at=c.A(5, 'Editar', FC), label='Editar a unidade')
    c.waitfor(target=SEL('#equipamento-condicao'), timeout=10)
    c.click(SEL('#equipamento-condicao'), at=c.A(5, 'condição', FC), label='abre Condição')
    c.hover(OPT('Em manutenção'), 0.6, at=c.A(5, 'manutenção', FH), label='Condição: Em manutenção')
    c.hover(OPT('Baixada'), 1.0, at=c.A(5, 'Baixada', FH), label='Condição: Baixada')
    c.mark(6)
    c.click(OPT('Em manutenção'), at=c.L(6) - 0.5, label='escolhe Em manutenção')
    c.click(BTN('Salvar', within=DLG), at=c.L(6) + 0.1, label='Salvar a unidade')
    c.waitfor(gone=SEL(DLG), timeout=10)
    c.click(BTN('Nova unidade'), at=c.A(6, 'Nova', FC), label='Nova unidade')
    c.waitfor(target=SEL('#equipamento-id'), timeout=10)
    c.click(SEL('#equipamento-id'), label='Identificação (campo)')
    c.type(SEL('#equipamento-id'), 'Caçamba 06', at=c.A(6, 'Caçamba', 0.05, nth=1), label='Identificação: Caçamba 06', cps=40, noClick=True)
    c.press('Tab', label='vai ao Tipo de equipamento')
    c.press('Enter', label='abre Tipo de equipamento')
    c.waitfor(selector='[role=listbox]', timeout=5)
    c.type(SEL('[role=listbox]'), 'Caçamba', label='Tipo: procura Caçamba 5 m³', cps=40, noClick=True)
    c.press('Enter', label='Tipo: Caçamba 5 m³')
    c.click(BTN('Cadastrar', within=DLG), at=c.A(6, 'Cadastrar', FC), label='Cadastrar unidade')
    c.waitfor(text='Unidade cadastrada', timeout=10)
    c.mark(7)
    rola_ate(c, 'Unidades identificáveis', c.L(7) - 0.4, 'sobe a lista (Caçamba 06 à vista)', y=24, dur_ms=600)
    c.click(SEL("main [role=listitem]:has-text('Caçamba 06')"), label='Caçamba 06 na lista')
    c.hover(TXTX('Ainda sem movimentação registrada', within='main', exact=False), 1.2, label='sem lugar (sem movimentação)')
    c.mark(8)
    c.click(BTN('Movimentar', within='main'), at=c.A(8, 'Movimentar', FC), label='Movimentar')
    c.waitfor(text='Nova movimentação', timeout=10)
    c.hover(SEL(f"{DLG} button[aria-pressed=true]:has-text('Externo')"), 0.6, at=c.A(8, 'fora', FH), label='De: Externo (compra nova)')
    c.click(SEL(f"{DLG} button[aria-pressed]:has-text('Minha base') >> nth=1"), at=c.A(8, 'Minha', FJ), label='Para: Minha base')
    c.click(BTN('Registrar', within=DLG), label='Registrar')
    c.waitfor(text='Movimentação registrada', timeout=10)
    c.hover(TXTX('Posição atual', within='main', exact=True), 1.2, at=c.A(8, 'base', FH, nth=1), label='Posição atual: Minha base')
    c.mark(9)
    c.cursor((760, 460), at=c.A(9, 'dica', 0.3), label='cursor em repouso (ilustração)')
    c.mark(10)
    rola_ate(c, 'Onde tudo está agora', c.L(10) - 0.2, 'desce a Onde tudo está agora', y=120)
    c.hover(TXTX('Na base', within='main', exact=True), 0.3, at=c.A(10, 'base', FH), label='Na base')
    c.hover(TXTX('Em campo', within='main', exact=True), 0.3, at=c.A(10, 'campo', FH), label='Em campo')
    c.hover(TXTX('Com parceiros', within='main', exact=True), 0.3, at=c.A(10, 'parceiros', FH), label='Com parceiros')
    c.mark(11)
    rola_ate(c, 'Contados por quantidade', c.L(11) - 0.2, 'desce a Contados por quantidade', y=150)
    c.click(BTNX('Ver saldo por'), at=c.A(11, 'Ver', FC), label='Ver saldo por fornecedor')
    c.hover(TXTX('Ocultar saldos', within='main'), 1.8, at=c.A(11, 'parceiro', FH), label='o saldo de bags com cada parceiro')
    c.mark(12)
    rola_topo_js = ("(async()=>{" + ACHA_ROLAGEM + "const c=rolagem(document.querySelector('main [role=tab]'));if(!c)return 'SEM ROLAGEM';"
                    "const y0=c.scrollTop,t0=performance.now();if(y0<3)return 'ok';" + SUAVE.replace('DUR', '600').replace('DESTINO', 'y0*(1-e)') +
                    "return 'topo:'+Math.round(c.scrollTop)})()")
    c.ev(rola_topo_js, at=c.L(12) - 0.6, label='sobe às abas')
    c.click(TAB('Movimentações'), label='aba Movimentações')
    c.hover(TXTX('Ordem 8', within='main', exact=False), 1.2, at=c.A(12, 'ordem', FH), label='as da troca de hoje: Ordem 8')
    c.fim()
    return c


@capitulo
def cap12():
    """Movimentações e a ficha do parceiro: Nova movimentação (10 bags da base para a Cooperativa), menu da linha (Editar, Excluir), Mostrar
    anuladas e a aba Coletas da ficha do Depósito Irmãos Siqueira."""
    c = Cap(12, start=NEUTRO, setup=setup_em('/coletas/equipamentos', extra=[{'do': 'click', 'target': TAB('Movimentações')}, {'do': 'wait', 'seconds': 1.0}]))
    c.mark(1)
    c.hover(TAB('Movimentações'), 0.4, at=c.A(1, 'aba', FH), label='aba Movimentações')
    c.click(BTN('Nova movimentação'), at=c.A(1, 'Nova', FC, nth=1), label='Nova movimentação')
    c.waitfor(text='Nova movimentação', timeout=10)
    c.click(SEL(f"{DLG} button[aria-pressed]:has-text('Minha base') >> nth=0"), at=c.A(1, 'minha', FC), label='De: Minha base')
    c.click(SEL(f"{DLG} button[aria-pressed]:has-text('Parceiro') >> nth=1"), at=c.A(1, 'Cooperativa', 1.2), label='Para: Parceiro')
    c.click(BTNX('Selecionar parceiro'), label='Selecionar parceiro…')
    c.waitfor(target=BUSCA_PARC, timeout=10)
    c.type(BUSCA_PARC, 'Recomeço', label='busca Recomeço', cps=40, noClick=True)
    c.click(BTNX('Cooperativa Recomeço', within=f'{DLG} >> nth=-1'), at=c.A(1, 'Recomeço', FC), label='escolhe Cooperativa Recomeço')
    c.click(SEL(f"{DLG} button[role=combobox]:has-text('Tipo de equipamento')"), label='Tipo de equipamento')
    c.click(OPT('Bag 1 m³'), label='Tipo: Bag 1 m³')
    c.click(PH('Quantidade'), label='Quantidade (campo)')
    c.type(PH('Quantidade'), '10', label='Quantidade: 10', cps=40, noClick=True, clear=True)
    c.click(BTN('Registrar', within=DLG), at=c.A(1, 'Registrar', FC), label='Registrar')
    c.waitfor(text='Movimentação registrada', timeout=10)
    c.mark(2)
    c.hover(LINHA_MENU, 1.0, at=c.A(2, 'menu', FH), label='menu da linha')   # o menu abre por hover; clicar de novo o fecharia
    c.click({'role': 'menuitem', 'name': 'Editar'}, at=c.A(2, 'Editar', FC), label='Editar movimentação')
    c.waitfor(text='Editar movimentação', timeout=8)
    c.hover(TXTX('Tipo e unidade não mudam aqui', within=DLG), 2.0, at=c.A(2, 'Pra', FH), label='Editar movimentação: o que muda e o que não muda')
    c.press('Escape', label='fecha o Editar')
    c.hover(LINHA_MENU, 0.6, label='abre o menu da linha')
    c.click({'role': 'menuitem', 'name': 'Excluir'}, label='Excluir')
    c.waitfor(text='Excluir movimentação?', timeout=8)
    c.mark(3)
    c.hover(TXTX('Motivo (opcional)', within=ALERTA), 1.4, at=c.A(3, 'motivo', FH), label='Excluir movimentação?: Motivo (opcional)')
    c.click(BTN('Cancelar', within=ALERTA), label='Cancelar (não exclui)')
    c.click(BTNX('Filtros', within='main'), at=c.A(3, 'Filtros', FC), label='Filtros')
    c.hover(TXTX('Mostrar anuladas'), 1.2, at=c.A(3, 'Mostrar', FH), label='Mostrar anuladas')
    c.press('Escape', label='fecha os Filtros')
    c.mark(4)
    c.click(ITEM_MENU('Clientes e Fornecedores'), at=c.A(4, 'ficha', FC), label='menu Clientes e Fornecedores')
    c.waitfor(text='Depósito Irmãos Siqueira', timeout=15)
    c.click(TXTX('Depósito Irmãos Siqueira', within='main'), label='ficha do Depósito Irmãos Siqueira')
    # 1.60.18: a lista abre só o painel resumido (sem aba Coletas); a ficha completa é a rota /cliente/<nome>-<código>, aberta aqui sem recarregar
    c.ev("(()=>{history.pushState({},'','/cliente/deposito-irmaos-siqueira-4');window.dispatchEvent(new PopStateEvent('popstate'));return location.pathname})()", label='abre a ficha completa do parceiro')
    c.waitfor(text='Histórico de Pedidos', timeout=15)
    c.click(SEL("main button:text-is('Coletas')"), at=c.A(4, 'Coletas', FC), label='aba Coletas')   # as abas da ficha completa são botões, não role=tab
    c.waitfor(text='Com este parceiro agora', timeout=10)
    c.hover(TXTX('Com este parceiro agora', within='main'), 1.0, at=c.A(4, 'agora', FH), label='Com este parceiro agora')
    c.hover(BTNX('Agendar coleta'), 1.2, at=c.A(4, 'agendar', FH), label='Agendar coleta')
    c.fim()
    return c


# o navegador do robô é de mesa e não dá permissão de GPS: a tela da ordem mostraria "Sem sinal de GPS". O celular do motorista tem sinal; o robô
# responde ao watchPosition do app com a posição de Niterói do mundo (a mesma do navegador do robô), como o celular faria.
GPS_FALSO = ("(()=>{const pos={coords:{latitude:-22.9035,longitude:-43.1038,accuracy:15,altitude:null,altitudeAccuracy:null,heading:null,speed:null},timestamp:Date.now()};"
             "const g=navigator.geolocation;g.watchPosition=(ok)=>{setTimeout(()=>ok(pos),50);return 1};g.getCurrentPosition=(ok)=>setTimeout(()=>ok(pos),50);g.clearWatch=()=>{};return 'gps'})()")


@capitulo
def cap13():
    """Onde está o caminhão: Rastreamento (mapa, Tiago ao vivo, raio do GPS, selos), Trajeto de uma coleta (ordem 7) e a ordem 7 com o aviso
    de localização; o item Rotas no menu."""
    c = Cap(13, start=NEUTRO, setup=setup_em('/coletas/ordens', aquece=['/coletas/rastreamento'], extra=ABRE_GRUPO + [{'do': 'eval', 'js': GPS_FALSO}]))
    c.mark(1)
    c.click(ITEM_MENU('Rastreamento'), at=c.A(1, 'Rastreamento', F1), label='menu Rastreamento')
    c.waitfor(text=PAGINAS['/coletas/rastreamento'], timeout=15)
    c.waitfor(text='Tiago Freitas', timeout=20)
    c.hover(TXTX('Tiago Freitas', within='main'), 1.2, at=c.A(1, 'Tiago', FH), label='Tiago Freitas na lista')
    c.mark(2)
    c.hover(TXTX('Ao vivo', within='main', exact=True), 1.0, at=c.A(2, 'celular', FH), label='selo Ao vivo')
    c.hover(TXTX('O círculo ao redor do ponto é o raio de incerteza do GPS', within='main'), 2.5, at=c.A(2, 'círculo', FH), label='o raio de incerteza do GPS')
    c.mark(3)
    c.cursor(NEUTRO, at=c.A(3, 'selo', 0.3), label='cursor em repouso (os selos)')
    c.mark(4)
    c.click(SEL("main button[role=combobox]"), at=c.A(4, 'Trajeto', FC), label='Trajeto de uma coleta')
    c.click(OPT('Ordem #7 · a_caminho'), at=c.A(4, 'sete', FC), label='escolhe a ordem 7')
    c.hover(SEL('main .leaflet-container'), 2.5, label='o trajeto da ordem 7 no mapa')
    c.mark(5)
    c.click(ORDENS_MENU, at=c.L(5) - 0.4, label='Ordens de Coleta')
    c.waitfor(text=PAGINAS['/coletas/ordens'], timeout=15)
    c.click(CARD_BTN(7, 'Preencher'), label='#7: Preencher')
    c.waitfor(text='Ordem #7', timeout=15)
    c.hover(TXTX('Localização em registro', within='body'), 2.2, at=c.A(5, 'aviso', FH), label='aviso: Localização em registro')
    c.ev('history.back()', at=c.A(5, 'Rotas', FH + 3.0), label='volta ao quadro (a tela da ordem não tem menu)')   # a tela da ordem não tem o link Voltar às ordens
    c.waitfor(text=PAGINAS['/coletas/ordens'], timeout=15)
    c.click(GRUPO, label='abre Coletas & Logística', unless=ITEM_MENU('Rotas'))
    c.hover(ITEM_MENU('Rotas'), 1.2, at=c.A(5, 'Rotas', FH), label='item Rotas do menu (Em breve)')
    c.fim()
    return c


@capitulo
def cap14():
    """O relatório: Este mês (4 coletas, 1 concluída, 25%), Mês passado (6, 5, 1, 100%), por status, motorista, veículo e parceiro."""
    c = Cap(14, start=(760, 420), setup=setup_em('/coletas/ordens', aquece=['/coletas/relatorio'], extra=ABRE_GRUPO))
    KPIS = SEL("main div.grid:has(:text-is('Total de coletas')) >> nth=-1")   # a grade mais interna (os quatro cartões)
    c.mark(1)
    c.click(ITEM_MENU('Relatório'), at=c.A(1, 'relatório', F1), label='menu Relatório')
    c.waitfor(text=PAGINAS['/coletas/relatorio'], timeout=15)
    c.confere_kpi([['Total de coletas', '4'], ['Concluídas', '1'], ['Canceladas', '0'], ['Taxa de conclusão', '25%']], 'Este mês: 4, 1, 0, 25%')
    c.hover(SEL('main button[role=combobox]'), 0.3, at=c.A(1, 'mês', FH, nth=1), label='Período: Este mês')
    c.hover(KPIS, 3.5, at=c.A(1, 'total', 1.0), label='Este mês: os quatro números')
    c.mark(2)
    c.click(SEL('main button[role=combobox]'), at=c.A(2, 'outubro', FC), label='abre Período')
    c.click(OPT('Mês passado'), label='Período: Mês passado')
    c.confere_kpi([['Total de coletas', '6'], ['Concluídas', '5'], ['Canceladas', '1'], ['Taxa de conclusão', '100%']], 'outubro: seis, cinco, uma, cem por cento')
    c.hover(KPIS, 4.0, label='outubro: os quatro números')
    c.mark(3)
    c.cursor((760, 460), at=c.A(3, 'dica', 0.3), label='cursor em repouso (ilustração)')
    c.mark(4)
    rola_ate(c, 'Por status', c.L(4) - 0.2, 'desce às tabelas', y=130)
    c.hover(TXTX('Por status', within='main', exact=True), 0.6, at=c.A(4, 'status', FH), label='Por status')
    c.hover(TXTX('Por parceiro', within='main', exact=True), 1.5, at=c.A(4, 'parceiro', FH), label='Por motorista, veículo e parceiro')
    c.mark(5)
    rola_ate(c, 'Período', c.L(5) - 0.2, 'sobe ao Período', y=160, prefixo=True)
    c.hover(SEL('main button[role=combobox]'), 3.0, label='Período (em que mês cada coleta entra)')
    c.fim()
    return c


@capitulo
def cap15():
    """As regras: Configurações, Prefixo "COL-", Janelas, Exigir motorista e veículo, Exigir aprovação, Avisar quando chegar solicitação,
    Antecedência mínima 24 e Dias aceitos."""
    c = Cap(15, start=(760, 420), setup=setup_em('/coletas/ordens', aquece=['/coletas/configuracoes'], extra=ABRE_GRUPO))
    c.mark(1)
    c.click(ITEM_MENU('Configurações'), at=c.A(1, 'Configurações', F1), label='menu Configurações (Coletas)')
    c.waitfor(text=PAGINAS['/coletas/configuracoes'], timeout=15)
    c.hover(TXTX('Operação', within='main', exact=True), 0.8, at=c.A(1, 'operação', FH), label='bloco Operação')
    c.mark(2)
    c.hover(SEL('#col-prefix'), 1.0, at=c.L(2) - 0.2, label='Prefixo da numeração')
    c.click(SEL('#col-prefix'), at=c.A(2, 'coloco', FC), label='Prefixo (campo)')
    c.type(SEL('#col-prefix'), 'COL-', at=c.A(2, 'prefixo', 0.05, nth=1), label='Prefixo: COL-', cps=40, noClick=True)
    c.press('Tab', at=c.A(2, 'ordens', 0.2), label='sai do campo (salva o prefixo)')
    c.waitfor(text='Prefixo da numeração salvo', timeout=8)
    c.mark(3)
    c.hover(TXTX('Janelas de coleta oferecidas', within='main', exact=True), 0.6, at=c.L(3) - 0.2, label='Janelas de coleta oferecidas')
    c.hover(SEL("main button:text-is('Dia todo')"), 1.2, at=c.A(3, 'períodos', FH), label='as janelas: Manhã, Tarde e Dia todo')
    c.hover(TXTX('Exigir motorista e veículo para agendar', within='main', exact=True), 1.5, at=c.A(3, 'exigir', FH), label='Exigir motorista e veículo para agendar')
    c.mark(4)
    rola_ate(c, 'Portal e solicitações', c.L(4) - 0.2, 'desce ao bloco Portal e solicitações', y=120)
    c.hover(TXTX('Exigir aprovação da solicitação', within='main', exact=True), 2.0, label='Exigir aprovação da solicitação')
    c.mark(5)
    c.hover(TXTX('Avisar quando chegar solicitação', within='main', exact=True), 2.2, at=c.L(5) - 0.2, label='Avisar quando chegar solicitação')
    c.mark(6)
    c.hover(SEL('#col-lead'), 1.0, at=c.L(6) - 0.2, label='Antecedência mínima (horas)')
    c.click(SEL('#col-lead'), at=c.A(6, 'coloco', FC), label='Antecedência (campo)')
    c.type(SEL('#col-lead'), '24', at=c.A(6, 'vinte', 0.4), label='Antecedência: 24', cps=40, noClick=True, clear=True)
    c.press('Tab', label='sai do campo (salva a antecedência)')
    c.waitfor(text='Antecedência mínima salva', timeout=8)
    c.hover(TXTX('Dias aceitos para coleta', within='main', exact=True), 0.3, at=c.A(6, 'aceitos', FH), label='Dias aceitos para coleta')
    c.hover(SEL("main button:text-is('Seg')"), 0.3, at=c.A(6, 'segunda', FH), label='Seg')
    c.hover(SEL("main button:text-is('Sáb')"), 0.3, at=c.A(6, 'sábado', FH), label='Sáb')
    c.mark(7)
    c.cursor((760, 460), at=c.A(7, 'dica', 0.3), label='cursor em repouso (ilustração)')
    c.fim()
    return c


@capitulo
def cap16():
    """Checklist e assinaturas: Modelos de checklist (Coleta com caçamba), perguntas (sim ou não; foto), checklist padrão e assinatura do
    responsável, e a tela da ordem #7 com Checklist e Assinatura."""
    c = Cap(16, start=NEUTRO, setup=setup_em('/coletas/configuracoes', aquece=['/coletas/ordens'], extra=[]))
    c.mark(1)
    rola_ate(c, 'Checklist da coleta', 0.5, 'desce ao bloco Checklist da coleta', y=140, dur_ms=700)
    c.click(BTN('Novo modelo'), at=c.A(1, 'Novo', FC), label='Novo modelo')
    c.waitfor(text='Nome *', timeout=10)
    c.click(SEL(f"{DLG} input >> nth=0"), label='Nome (campo)')
    c.type(SEL(f"{DLG} input >> nth=0"), 'Coleta com caçamba', at=c.A(1, 'Coleta', 0.05, nth=1), label='Nome: Coleta com caçamba', cps=40, noClick=True)
    c.click(BTN('Criar modelo', within=DLG), at=c.A(1, 'Criar', FC), label='Criar modelo')
    c.waitfor(gone=SEL(DLG), timeout=10)
    c.mark(2)
    c.hover(SEL("main tbody tr button:visible >> nth=0"), 0.4, at=c.A(2, 'Gerenciar', FC + 1.0), label='menu da linha do modelo')   # menu por hover
    c.click({'role': 'menuitem', 'name': 'Gerenciar perguntas'}, at=c.A(2, 'Gerenciar', FC), label='Gerenciar perguntas')
    c.click(BTN('Nova pergunta', within=DLG), at=c.A(2, 'Nova', FC), label='Nova pergunta')
    c.waitfor(text='Pergunta *', timeout=10)
    c.click(SEL(f"{DLG} textarea, {DLG} input[placeholder*='Pergunta'] >> nth=0"), label='Pergunta (campo)')
    c.type(SEL(f"{DLG} textarea, {DLG} input[placeholder*='Pergunta'] >> nth=0"), 'Local estava acessível para o veículo?', at=c.A(2, 'local', 0.1),
           label='Pergunta: Local estava acessível para o veículo?', cps=40, noClick=True)
    c.hover(TXTX('Tipo de resposta', within=DLG), 0.8, at=c.A(2, 'sim', FH), label='Tipo de resposta: Sim ou não')
    c.hover(TXTX('Pergunta obrigatória', within=DLG), 0.8, at=c.A(2, 'obrigatória', FH), label='Pergunta obrigatória')
    c.click(BTN('Adicionar pergunta', within=DLG), label='Adicionar pergunta')
    c.waitfor(text='Local estava acessível para o veículo?', timeout=10)
    c.mark(3)
    c.click(BTN('Nova pergunta', within=DLG), at=c.A(3, 'foto', FC + 1.0), label='Nova pergunta (para mostrar os tipos)')   # o tipo só aparece no formulário
    c.waitfor(target=SEL('#pergunta-tipo'), timeout=10)
    c.click(SEL('#pergunta-tipo'), at=c.A(3, 'foto', FC), label='abre Tipo de resposta')
    c.hover(OPT('Foto'), 0.6, label='tipo Foto')
    c.hover(OPT('Número'), 0.5, at=c.A(3, 'número', FH), label='tipo Número')
    c.hover(OPT('Texto livre'), 0.5, at=c.A(3, 'texto', FH), label='tipo Texto livre')
    c.hover(OPT('Escolher uma opção'), 0.5, at=c.A(3, 'escolha', FH), label='tipo Escolher uma opção')
    c.hover(OPT('Conforme / Não conforme / Não se aplica'), 0.8, at=c.A(3, 'conformidade', FH), label='tipo Conforme / Não conforme / Não se aplica')
    c.press('Escape', label='fecha a lista de tipos')
    c.click(BTN('Cancelar', within=DLG), label='Cancelar (volta à lista de perguntas)')
    c.mark(4)
    c.click(BTN('Fechar', within=DLG), at=c.L(4) - 0.5, label='Fechar as perguntas')
    c.click(SEL("main button[role=combobox]:has-text('Nenhum')"), at=c.A(4, 'padrão', FC), label='Checklist padrão da empresa')
    c.click(OPT('Coleta com caçamba'), label='escolhe Coleta com caçamba')
    c.hover(TXTX('Usado em toda coleta nova.', within='main'), 1.2, at=c.A(4, 'nova', FH), label='ajuda: usado em toda coleta nova')
    c.click(SEL("main div:has(> div > p:text-is('Exigir assinatura do responsável no local')) > [role=switch]"), at=c.A(4, 'assinatura', FC), label='Exigir assinatura do responsável no local')
    c.hover(TXTX('Exigir assinatura do motorista', within='main'), 1.2, at=c.A(4, 'motorista', FH), label='Exigir assinatura do motorista')
    c.mark(5)
    c.click(ORDENS_MENU, at=c.L(5) - 0.4, label='Ordens de Coleta')
    c.waitfor(text=PAGINAS['/coletas/ordens'], timeout=15)
    c.click(CARD_BTN('COL-7', 'Preencher'), label='#COL-7: Preencher')
    c.waitfor(text='Checklist', timeout=15)
    c.hover(TXTX('Falta para concluir', within='body'), 2.0, at=c.A(5, 'falta', FH), label='Falta para concluir')
    c.mark(6)
    c.hover(TXTX('Assinatura', within='body', exact=True), 1.0, at=c.L(6) - 0.2, label='bloco Assinatura')
    c.fim()
    return c


def main():
    quais = [int(a) for a in sys.argv[1:] if not a.startswith('-')] or sorted(CAPS_ROBO)
    json.dump({f'{n:02d}': FAKE_NOW[n] for n in FAKE_NOW}, open(os.path.join(HERE, 'fake_now.json'), 'w', encoding='utf8'), indent=1)
    for n in quais:
        c = CAPS_ROBO[n]()
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
        marcas = [s['name'] for s in d['steps'] if s.get('do') == 'mark']
        faltam = [f'L{i}' for i in range(1, len(c.linhas) + 1) if f'L{i}' not in marcas]
        if faltam:
            print(f'  aviso cap{n:02d}: sem marca {",".join(faltam)}')
        path = os.path.join(HERE, f'cap{n:02d}.json')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
        print(f'cap{n:02d}: {len(d["steps"])} passos, narração {c.dur:.1f} s{" (voz ESTIMADA)" if c.estimada else ""} -> {os.path.relpath(path, HERE)}')


if __name__ == '__main__':
    main()
