# Texto do TTS (ElevenLabs, eleven_v4, voz Kaik Barreto) por capítulo do T15 "Relatório Financeiro e DRE".
# Gerado do roteiro.md (coluna Fala): cada linha do texto é uma linha da tabela Tela | Fala.
# Trocas de pronúncia em relação ao roteiro (a legenda segue o roteiro; ver config_narracao.json):
#   EcoSistema -> "Ecossistema" | Cato -> "Cáto" | DRE -> "dê-érri-ê" | PDF -> "pê-dê-éfe" | CMV -> "cê-ême-vê" | Excel -> "ékisel" | OPEX -> "ópecs"
CAPS = {
0: """Oi! Neste tutorial a gente vai responder a pergunta que todo dono faz no fim do mês: eu ganhei ou perdi dinheiro? E por quê?
Em outubro, a Recicla Vale Metais vendeu bem e ainda encheu o pátio de ferro. Mesmo assim, saiu mais dinheiro do que entrou. Afinal, ela ganhou ou perdeu?
Pra responder, a gente vai arrumar as categorias e os centros de custo, ler o Relatório Financeiro e o dê-érri-ê, e exportar tudo pro contador.
Se você ainda não viu o tutorial Bancos, cofre e conciliação bancária, dá uma olhada antes. [pause] Tudo começa pelas categorias.""",
1: """No menu, Financeiro, Categorias Financeiras.
As categorias são o plano de contas da empresa: a lista que diz de onde vem e pra onde vai cada real. Em cima ficam as de receita, como o aluguel de caçamba. Embaixo, as de despesa, como a folha, a energia e o combustível.
É pela categoria que o relatório separa o dinheiro. Despesa lançada sem categoria cai num monte só, e aí ninguém sabe o que ela é.
Repara que as despesas ficam separadas pelo lugar onde entram no dê-érri-ê. dê-érri-ê é o relatório do resultado do mês, que a gente lê daqui a pouco.
O Frete que já existe é o frete de compra, o de buscar a sucata no fornecedor. Ele entra como custo do material. Agora vou criar uma subcategoria nele: o frete de entrega.
A subcategoria herda tudo da principal, mas pode mudar de lugar no dê-érri-ê. Levar o material até o cliente é gasto do dia a dia da operação. Então eu escolho Despesas operacionais, o ópecs. A prévia embaixo já mostra onde ela vai entrar.
Uma dica: cada subcategoria tem o seu lugar no dê-érri-ê. Os lançamentos do frete de entrega vão pras despesas operacionais, mesmo com a principal em Custos adicionais. E a tela marca com um selo quando os dois são diferentes.
Agora, uma categoria que pede cuidado: a compra de máquina ou de caminhão.
Uma dica: comprar uma prensa ou um caminhão não é despesa do mês. O dinheiro vira um bem da empresa.
Com empréstimo é parecido. Receber não é receita, e devolver o valor emprestado não é despesa. Só os juros entram no resultado. Se a parcela mistura os dois, são dois lançamentos.
E a distribuição de lucro pros sócios também fica fora da despesa.
Por isso, essa categoria vai em Não compõe o dê-érri-ê: o dinheiro sai do caixa, mas o resultado não muda. E no fluxo de caixa ela fica em Atividades de investimento.
Pronto. O Ecossistema registra a compra. A depreciação da máquina, e o ganho ou a perda quando ela for vendida, ficam com o contador. Na dúvida sobre onde uma categoria entra, é ele quem orienta.""",
2: """Com as categorias certas, dá pra saber em que o dinheiro foi gasto. O centro de custo responde onde: em qual frente da empresa.
Na Recicla Vale Metais, o pátio fica com a energia e o aluguel, e a coleta fica com o combustível e a manutenção do caminhão. Assim, cada frente mostra quanto custa.
A terceira frente vai ser a produção, a prensa que enfarda latinha e papelão. Coloco o nome, uma cor pra achar rápido nos gráficos e uma descrição.
Uma dica: quando uma frente parar, é só desligar o Ativo. Ela sai dos formulários e continua nos lançamentos antigos. Excluir não apaga lançamento nenhum, só tira a marcação, e eles ficam sem centro de custo.
Salvei. Daqui pra frente, o Centro de custo aparece como opção nos lançamentos de despesa e de receita, no caixa, no banco e nas contas a pagar e receber.""",
3: """Agora o relatório. No menu, Financeiro, Relatório Financeiro.
Em cima fica o período. A tela sempre abre em Este mês, e novembro mal começou. Então eu escolho Mês passado, e a tela inteira passa a mostrar outubro.
Se um dia o relatório parecer vazio, confere o período primeiro.
Embaixo ficam as abas. Nesta aula, a gente passa pelo Dashboard, pelo dê-érri-ê, pelos Centros de Custo e pelo Histórico. E a tela volta sempre na última aba que você abriu.
Nos Centros de Custo aparece o resultado de cada frente. Em outubro, quem mais gastou foi o pátio, com a folha, o aluguel e a energia. A coleta gastou menos, e ainda trouxe a receita do aluguel de caçamba.
Repara no aviso: aqui entram as receitas e as despesas lançadas no financeiro. A compra e a venda de material ficam fora desta conta.
Uma dica: pra ver os valores do relatório, a pessoa precisa da permissão Ver Totais e Valores Financeiros. Sem ela, a tela abre só com o aviso Acesso Restrito. Quem libera é o administrador, em Usuários e Permissões.""",
4: """O Dashboard é a aba pra bater o olho. Em cima vem o Resultado do Período: outubro fechou com seis mil e quinhentos reais positivos, um superávit.
Quando o mês fecha negativo, o bloco fica vermelho e mostra déficit. E esse número é o mesmo do fim do dê-érri-ê.
Logo abaixo, as despesas por categoria, da maior pra menor. A folha salarial vem primeiro, com dezenove mil e oitocentos reais.
E olha a energia elétrica: sete mil e setecentos reais, o dobro de um mês normal. Guarda essa, que a gente volta nela no Histórico.
Do lado ficam as receitas por categoria, o que entrou fora das vendas. Em outubro, o aluguel de caçamba: dois mil e oitocentos reais.
A compra e a venda de material não entram nesses gráficos. Elas têm linha própria no dê-érri-ê.""",
5: """Mais embaixo ficam os números do movimento do pátio. Primeiro, o ticket médio.
O Ticket Médio Compra é quanto vale, em média, cada compra do mês: o total comprado dividido pelo número de compras. O Ticket Médio Venda faz a mesma conta com as vendas.
Com ele, dá pra ver se você está comprando em lotes maiores ou menores que nos outros meses.
No Top Fornecedores, o primeiro de outubro é o Depósito Irmãos Siqueira, que vendeu o lote grande de ferro.
No Top Clientes, a Fundição Bandeira do Vale lidera em reais, com o cobre, o metal amarelo e o bronze.
Trocando pra quilos, quem vai pro topo é a Aços Quiririm, com o ferro e a chaparia. Um cliente traz valor, o outro traz volume.
E o Ver todos abre a lista completa.
Nos materiais, o ferro pesado lidera as compras de outubro: cinquenta mil quilos, por quarenta e sete mil e quinhentos reais.
Já nos mais vendidos, ele nem aparece entre os cinco primeiros. Isso vai explicar o resultado do mês.""",
6: """Agora, o dê-érri-ê, o demonstrativo do resultado. É o relatório que o contador pede, e ele mostra, passo a passo, como as vendas viram resultado.
Ele se lê de cima pra baixo, como uma escada. Começa na Receita Bruta, que são as vendas. Tira os impostos e deduções, e chega na Receita Líquida. Tira os custos do material, e chega no Lucro Bruto.
Depois saem as despesas operacionais, entram as outras receitas e despesas, e o que sobra é o Resultado do Período.
Na tela é igual: cada degrau numa faixa, com o valor de outubro.
Clicando num grupo, ele abre as categorias, com o valor de cada uma.
E do lado de cada valor vem quanto ele pesa na receita do mês.
No fim, o resultado de outubro: seis mil e quinhentos reais, na faixa verde.
E lembra da categoria das máquinas? O que fica em Não compõe o dê-érri-ê não aparece aqui.""",
7: """Agora, o botão que mais gera dúvida: Regime de Caixa ou Regime de Competência. O dê-érri-ê abre em competência.
No caixa, conta todo o dinheiro que entrou e saiu no mês. O material comprado já vira custo, mesmo que ainda esteja no pátio.
Na competência, conta só o custo do material que foi vendido. O que está parado no estoque espera a venda.
Pensa no ferro pesado de outubro. A Recicla Vale Metais comprou cinquenta toneladas, a noventa e cinco centavos o quilo. Saíram quarenta e sete mil e quinhentos reais.
E vendeu só dez toneladas, a um real e vinte e cinco o quilo. Entraram doze mil e quinhentos.
No caixa, a conta é o que entrou menos o que saiu: um prejuízo de trinta e cinco mil reais. É a verdade do bolso.
Na competência, o custo é só o das dez toneladas vendidas: nove mil e quinhentos. Sobra um lucro de três mil. E as outras quarenta toneladas continuam no pátio, valendo trinta e oito mil reais como estoque.
Nenhum dos dois está errado. O caixa responde quanto dinheiro sobrou. A competência responde se você está ganhando no que vende.
Agora no dê-érri-ê de verdade, com o mês inteiro. Em competência, outubro deu seis mil e quinhentos reais de lucro.
Clico em Regime de Caixa, e o mesmo mês vira um prejuízo de trinta e um mil e quinhentos reais.
A diferença está na linha cê-ême-vê, Compras de materiais. cê-ême-vê é o custo da mercadoria vendida. Em competência, a linha traz só o custo do que saiu. Em caixa, traz tudo o que foi comprado no mês.
E a diferença entre os dois resultados é de trinta e oito mil reais: o ferro que ficou no pátio, pelo preço de compra.
Quem compra muito e segura o material esperando preço vê prejuízo no caixa e lucro na competência. É normal, e é pra isso que existem os dois.""",
8: """No pé do dê-érri-ê fica o Patrimônio Operacional Atual. Clico pra abrir. Ele mostra do que a empresa é feita hoje.
Ele soma o dinheiro em caixa, o saldo dos bancos, o que os clientes devem, como o fiado da Fundição Bandeira do Vale, e o estoque. E tira o que a empresa deve aos fornecedores.
O estoque entra pela projeção de venda: quanto o material do pátio renderia, vendido hoje pelo preço de venda cadastrado.
Uma dica: o patrimônio não segue o filtro de período. Ele é a foto de agora, e trocar o mês não muda nada aqui.
E ele é uma projeção. O estoque só vira dinheiro quando for vendido, e pelo preço do dia.
No canto, o Exportar Patrimônio abre esse bloco numa aba nova, pra imprimir ou guardar.""",
9: """Mais embaixo fica a Evolução Mensal, com os últimos seis meses. Ela não segue o filtro de período, porque a ideia é comparar um mês com o outro.
Repara em outubro: as compras foram as maiores dos seis meses, e o resultado caiu. É o ferro do pátio de novo.
Pra comparar o dê-érri-ê inteiro, tem o Comparar períodos. Escolho Período anterior, que aqui é setembro.
Aplico, e os dois meses ficam lado a lado, linha por linha.
Uma dica: o dê-érri-ê monta cada linha pelo nome da categoria. Por isso, renomear uma categoria muda o que entra na linha dela, até na comparação com os outros meses.""",
10: """Agora o Histórico, com os lançamentos do mês, um por um, separados em receitas, despesas e compras.
Uma dica: o relatório não inventa número nenhum. Se um resultado parece estranho, a causa está num lançamento: uma categoria faltando, uma despesa esquecida, um saque lançado como despesa. Por isso, comece sempre por aqui.
Lembra da energia de outubro? Em Filtros, escolho a categoria Energia elétrica. Dá pra filtrar também por cliente ou fornecedor, por centro de custo e pela fonte.
Duas contas de energia, no mesmo dia e com o mesmo valor: três mil, oitocentos e cinquenta reais. A conta foi lançada em dobro.
Clico na lixeira da segunda e em Excluir. Pronto: ficou uma conta só, e o dê-érri-ê e o patrimônio já recalcularam sozinhos.
A lixeira aparece nas despesas lançadas no banco. E o lápis do lado troca a categoria de um lançamento do caixa ou do banco.
Uma dica: o Histórico não repete o dinheiro de uma compra ou de uma venda que já está na lista. Assim, nada é contado duas vezes. Pra ver o caixa linha por linha, o lugar é o Histórico do Caixa.""",
11: """Pra levar tudo pro contador, tem o Exportar.
O histórico sai em pê-dê-éfe ou em ékisel, com o período e os filtros da tela. Aqui eu escolho o que entra: receitas, despesas e compras.
O ékisel é pra você mexer nos números. O pê-dê-éfe é pra mandar pro contador ou guardar.
E o Fechamento completo, em ékisel, monta o pacote do mês pro contador: os lançamentos, as contas em aberto e o estoque no fim do período.
E o dê-érri-ê tem o Exportar dele, em Planilha ékisel ou Documento pê-dê-éfe, do jeito que está na tela, com o período e o regime.""",
12: """Pronto! Recapitulando: a gente montou o plano de contas, com o frete de entrega em outro lugar do dê-érri-ê e as máquinas fora do resultado. E criou o centro de custo da produção.
Abriu o relatório em outubro, leu o resultado e as despesas no Dashboard, e viu os maiores fornecedores e clientes do mês.
Leu o dê-érri-ê nos dois regimes e viu, com o ferro do pátio, por que outubro deu lucro na competência e prejuízo no caixa.
Viu o patrimônio de hoje, a evolução dos últimos seis meses e a comparação com setembro.
E achou a energia lançada em dobro no Histórico, excluiu, e exportou o histórico pro contador.
No próximo tutorial, a gente pergunta pro Cáto em português e recebe a resposta pronta. Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "O plano de contas.",
           2: "Centros de custo.",
           3: "O Relatório Financeiro.",
           4: "O Dashboard do mês.",
           5: "Fornecedores, clientes e ticket médio.",
           6: "Lendo o dê-érri-ê.",
           7: "Caixa ou competência.",
           8: "O patrimônio de hoje.",
           9: "Mês a mês.",
           10: "O Histórico.",
           11: "ékisel e pê-dê-éfe.",
           12: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "Categorias",
           2: "Centros de custo",
           3: "Relatório",
           4: "Dashboard",
           5: "Dashboard",
           6: "DRE",
           7: "DRE",
           8: "Patrimônio",
           9: "Evolução",
           10: "Histórico",
           11: "Exportar",
           12: "Resumo"}

if __name__ == "__main__":
    tot = 0
    pal = 0
    for k, v in CAPS.items():
        w = len(v.replace("[pause]", "").split())
        tot += len(v)
        pal += w
        print(f"cap {k:2d}: {len(v):5d} chars, {w:4d} palavras, ~{w/2.6:5.1f} s")
    tit = sum(len(v) for v in TITULOS.values())
    print("total chars CAPS", tot, "| TITULOS", tit, "| soma", tot + tit, "| palavras", pal, f"| ~{pal/2.6/60:.1f} min de fala")
