# Texto enviado ao ElevenLabs (eleven_v4, Fernanda) por capítulo do T13 "Financeiro".
# Gerado do roteiro.md (coluna Fala) pelo gerador do lote 4: cada linha do texto é uma linha da tabela Tela × Fala.
# Trocas de pronúncia em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   Contas a Pagar/Receber -> "Contas a Pagar e Receber" | R-410A -> "érre quatrocentos e dez á" | Asaas -> "asas" | PMOC -> "pê-móqui" | PDF -> "pê-dê-éfe" | DRE -> "dê érri ê" | CSP -> "cê-ésse-pê" | CSV -> "cê-ésse-vê" | Excel -> "ékisel" | PIX -> "pix"
CAPS = {
0: """Oi! Neste tutorial a gente vai cuidar do dinheiro da sua empresa na Dominex: o que entra, o que sai e o que ainda vai vencer, tudo num lugar só.
Com o Financeiro em dia, você sabe quanto tem em cada conta, o que vai pagar no mês e quanto ainda vai receber dos clientes.
Se você ainda não viu o tutorial Portal do Cliente e Portal do Contrato, dá uma olhada antes. [pause] Vamos começar pelo menu.""",
1: """O Financeiro fica aqui no menu, num grupo só, com cinco telas.
A Visão Geral é o resumo do período. Movimentações Financeiras guarda as contas e os cartões da empresa, com o extrato de cada um. E em Contas a Pagar e Receber fica tudo o que ainda vai vencer.
Cobranças é o módulo de cobrar o cliente por pix, boleto ou cartão, e em Relatórios ficam o dê érri ê e o fluxo de caixa. Cada um tem o seu tutorial.
Lá em cima ficam o filtro de período, que começa em Este mês, e o botão Configurações Financeiras, onde moram as categorias.
Uma dica: o período vale pra tela inteira. Então, antes de ler qualquer número, confere qual período está escolhido.""",
2: """Antes de lançar qualquer coisa, o sistema precisa saber de onde o dinheiro sai e pra onde ele vai. Isso fica em Movimentações Financeiras, nesta coluna, Contas e cartões.
Duas contas já vêm com a empresa: o Caixa, que é o dinheiro em espécie do escritório, e a Conta Principal, que é o banco. No alto da tela, ao lado do título, o botão Conciliação bancária é onde você importa o extrato do banco pra conferir com o sistema.
As duas começam com saldo zero, então o primeiro passo é acertar o saldo inicial. No menu da Conta Principal, clico em Editar e, no Saldo Inicial, coloco o que tem no banco hoje: dezoito mil e quinhentos reais.
Repara no Faz parte do caixa da empresa. Ligado, o dinheiro dessa conta entra no fluxo de caixa dos próximos dias. Já uma poupança ou um investimento você cria em Nova conta, no mais do grupo Contas, com essa opção desligada.
No Caixa, do mesmo jeito, os oitocentos reais em espécie. Pronto, as duas contas já mostram o saldo.""",
3: """Conta criada, agora o primeiro dinheiro entrando. Abro a Conta Principal: em cima o saldo, e embaixo o extrato, ainda vazio.
Clico em Nova movimentação, e escolho entre Receita, Despesa ou Transferência. Imagina que a equipe terminou a instalação de um split no Mercado Vila Nova, e o cliente pagou na hora. É uma Receita.
Em O que é, a Categoria é Vendas de Serviços, e na Descrição eu conto o que foi. No Cliente vinculado, o Mercado Vila Nova, e assim a receita aparece também no financeiro da ficha dele.
Do lado fica a Ordem de serviço, pra quando a receita é de uma ordem. E lembra do Faturar OS, do tutorial de Ordens de Serviço? Ele abre este mesmo formulário, já com a ordem e o cliente preenchidos.
Em Dinheiro vai o valor, mil oitocentos e cinquenta reais, a conta onde ele entrou, a Conta Principal, e a forma de pagamento, pix.
Repara nas duas datas. A Data do lançamento é quando o serviço aconteceu. E, com o Já foi recebido ligado, a Data do recebimento é quando o dinheiro entrou. Hoje são iguais, mas cada uma conta num tipo de relatório, que a gente vê no tutorial do dê érri ê.
Salvo, e a receita entra no extrato. Embaixo de cada valor aparece o Saldo, que mostra como ficou a conta depois daquela movimentação.""",
4: """Agora o dinheiro saindo. A gente comprou gás érre quatrocentos e dez á e tubos de cobre na Ventura, pra pagar no boleto. Nova movimentação, Despesa.
A Categoria é cê-ésse-pê Materiais, o custo do material usado nos serviços. E no Fornecedor vinculado, a Ventura Gás e Tubos. Lembra do Histórico de Gastos, na ficha do fornecedor? É escolhendo o fornecedor aqui que a despesa aparece lá.
Seiscentos e quarenta reais, saindo da Conta Principal, no boleto.
Como o boleto ainda vai ser pago, eu desligo o Já foi pago. Repara no aviso: irá para contas a pagar. E aparece o Vencimento, onde vai a data do boleto.
Em Mais detalhes dá pra guardar o boleto e a nota fiscal, no campo de Comprovantes e Notas Fiscais. Aceita imagem e pê-dê-éfe, e dá pra anexar vários.
Salvo. Ela não entra no extrato, porque o dinheiro ainda não saiu: fica esperando em Contas a Pagar, com o vencimento, até você dar a baixa.""",
5: """E quando a compra é de material que vai pro estoque? Aí o caminho é a compra direta, que o tutorial de Estoque deixou pra cá. Ela fica no Estoque, na aba Compras de Material.
Clico em Registrar compra direta. Ela dá entrada no estoque e lança a despesa numa operação só. Escrevo Reposição de dreno, escolho a Distribuidora Aurora e deixo o Estoque Principal, com a data de hoje.
Em Materiais, a mangueira de dreno: trinta metros, a três reais e cinquenta. O total da compra sai dos itens: cento e cinco reais.
Embaixo vem o lado do Financeiro. A categoria já vem em cê-ésse-pê Materiais. Escolho a Conta Principal, deixo como Pago, no pix, hoje.
Registrar compra. Pronto: a mangueira entrou no Estoque Principal, e a despesa já foi pro Financeiro, como paga.""",
6: """De volta em Movimentações, o extrato da Conta Principal já mostra a compra direta, junto da receita.
Cada linha tem o Editar e o Excluir. Quem pode excluir lançamento você define nos cargos, pela permissão Excluir Lançamento Financeiro.
E quando o dinheiro só muda de lugar? Por exemplo, tirei trezentos reais do banco pra deixar de troco no caixa. No menu da conta, clico em Transferir.
Na Origem, a Conta Principal, e no Destino, o Caixa. Trezentos reais, com a descrição Troco do caixa. E Transferir.
A transferência aparece nas duas contas: saiu do banco e entrou no caixa. E ela fica fora das receitas e das despesas, porque o dinheiro continua dentro da empresa.
E se a contagem do caixa não bater com o sistema? No menu da conta tem o Ajustar saldo: você informa quanto a conta realmente tem, e o sistema lança a diferença.""",
7: """Agora o cartão de crédito, que funciona diferente. Clico em Novo cartão e dou o nome: Cartão Empresarial.
O cartão tem duas datas: o Dia de fechamento, cinco, e o Dia de vencimento, quinze. E a frase embaixo confirma a regra: a fatura que fecha no dia cinco vence no dia quinze do mesmo mês.
Uma dica: compra feita no próprio dia do fechamento já entra na fatura seguinte.
O Limite de crédito é opcional, e eu coloco dez mil reais. Criar Cartão, e ele aparece no grupo Cartões, com a fatura em aberto.""",
8: """Cartão criado. As faturas aparecem sozinhas, conforme as compras entram nele.
Vou lançar uma compra que já estava no cartão. Nova movimentação, Despesa, e na conta eu escolho o Cartão Empresarial. Repara que aparece o bloco Despesa no Cartão de Crédito.
Na categoria, a Ferramentas e Equipamentos, que já vem com a empresa. Se faltar alguma, o botão de mais do lado do campo cria na hora.
Na descrição, a bomba de vácuo e o vacuômetro, de mil duzentos e noventa reais. E a data é a da compra, que foi no mês passado.
Em Parcelas, três vezes. E olha que útil: o bloco mostra em qual fatura cai cada parcela de quatrocentos e trinta reais. A primeira cai na fatura deste mês.
A compra não sai do caixa nem do banco agora: ela entra na fatura, e o dinheiro só sai quando você paga a fatura. Salvar.""",
9: """Compra lançada, agora a fatura. No cartão aparecem as três faturas, uma por parcela. A de novembro já fechou, no dia cinco, e por isso o Pagar Fatura está liberado. As outras liberam o pagamento quando chegar o fechamento delas.
Clico em Pagar Fatura. Escolho de onde sai o dinheiro, a Conta Principal, e a data. O Valor a pagar já vem com o total, e o aviso confirma: fatura será completamente quitada.
Pagando a fatura inteira, as compras dela ficam quitadas e o limite do cartão volta. Dá pra pagar só uma parte também: aí, no regime de caixa, as compras entram no resultado quando a fatura for quitada por inteiro.
Confirmar Pagamento. Pronto: fatura quitada, e o limite do cartão foi liberado.
Repara que, na lista geral, aparece o pagamento da fatura, e não cada compra, porque foi o pagamento que tirou o dinheiro do banco.
E lembra do cartão Movimentações financeiras, do tutorial de Configurações? Ele tem o Incluir compras no cartão. Ligado, as compras também aparecem na lista geral, e a escolha vale só pra você, em qualquer aparelho.""",
10: """Fatura em dia. E o que ainda vai vencer? Isso mora em Contas a Pagar e Receber, que abre na aba Todas, com tudo o que vence no período.
Dá pra separar em A Pagar e A Receber. E essa faixa mostra o horizonte: o que já venceu, o que vence nos próximos sete dias e o que vence de oito a trinta dias.
Olha o boleto do gás, que a gente lançou agora há pouco. E a primeira das três parcelas do orçamento do hotel, que nasceram quando a gente aprovou o orçamento, no tutorial de Orçamentos.
Também dá pra ver tudo num calendário, e o Exportar leva a lista pra ékisel, pê-dê-éfe ou cê-ésse-vê.
Agora uma conta que se repete: o aluguel do galpão. Clico em Nova Conta, deixo o Tipo em A Pagar e escrevo a descrição.
A categoria Aluguel já vem pronta. O valor é dois mil e oitocentos reais, vence todo dia dez, e sai da Conta Principal.
Em Parcelar ou repetir, a Recorrência é Mensal, com doze parcelas. Criar Conta.
Repara: o sistema já cria as doze de uma vez, cada uma com o seu vencimento. E, buscando por aluguel, aparecem todas, porque a busca procura em todos os meses.""",
11: """Bom, agora a baixa: o que foi pago e o que foi recebido. O boleto do gás foi pago hoje. Na aba A Pagar, no menu da linha, clico em Marcar como pago.
Escolho de onde saiu o dinheiro, a Conta Principal, a forma, boleto, e a data. Confirmar, e a conta fica como Pago.
Agora o outro lado. O hotel já pagou a primeira mensalidade do pê-móqui. Na aba A Receber, eu busco por pê-móqui, e aparecem as doze mensalidades que o contrato lançou, lá no tutorial de Contratos e pê-móqui.
No menu da primeira, Marcar como recebido. Repara no Valor recebido: informando um valor menor, você registra só uma parte, e o restante continua a receber, com um novo vencimento.
Aqui o hotel pagou o valor inteiro, no pix, na Conta Principal. Se tivesse tarifa da maquininha, ela ia neste campo, e o sistema lança como despesa em Tarifas e Taxas.
Confirmar recebimento. Pronto, primeira mensalidade recebida.""",
12: """Pra tudo isso virar relatório, as categorias contam muito. Elas ficam em Configurações Financeiras, na aba Categorias, separadas em receita e despesa, e a empresa já nasce com uma lista pronta.
As que têm o cadeado são as Categorias do sistema, que os lançamentos automáticos usam. Nelas dá pra mudar o nome, a cor e o ícone.
Falta uma pras peças que a equipe troca no serviço. Vou criar a Peças e componentes, do tipo Despesa, como categoria principal.
O campo mais importante é o Onde aparece no dê érri ê. Peça trocada no serviço é custo direto, então escolho Custos diretos. E a Prévia no dê érri ê já mostra o efeito: essa categoria reduz o lucro bruto.
É a categoria que decide em que linha do dê érri ê cada valor aparece. Criar, e pronto.
No menu de cada categoria dá pra adicionar subcategorias, por exemplo, compressor e capacitor dentro de Peças e componentes.
Do lado, o Centro de Custo separa receitas e despesas por obra, projeto ou setor. E os Grupos do dê érri ê ficam pro tutorial do Relatório Financeiro.""",
13: """Agora a Visão Geral faz mais sentido. No cartão escuro, o Saldo do Período: o que entrou menos o que saiu, só o que já foi pago ou recebido. E daqui também dá pra lançar e transferir.
Do lado, o que ainda vai entrar e o que ainda vai sair no período. Clicando, você vai direto pra Contas a Pagar e Receber.
Em Saldo por Conta, quanto tem em cada conta e no caixa, e quanto falta pagar nas faturas do cartão.
Embaixo vêm os gráficos: o fluxo do que já entrou e saiu, a projeção do caixa com os vencimentos do período e a agenda de vencimentos, que mostra quando o caixa vai ser mais pressionado.
E ainda as despesas que mais pesam, a evolução do resultado e as últimas movimentações. Tudo isso respeita o período lá de cima.""",
14: """Pronto! Recapitulando: a gente acertou o saldo inicial do caixa e do banco, lançou uma receita e uma despesa, fez a compra direta de material e passou dinheiro de uma conta pra outra.
Cadastrou o cartão da empresa, lançou uma compra parcelada, viu cada parcela na sua fatura e pagou a fatura que fechou.
Em Contas a Pagar e Receber, criou o aluguel do ano de uma vez, deu baixa no boleto e recebeu a primeira mensalidade do pê-móqui.
E organizou as categorias, que decidem onde cada valor aparece no dê érri ê, e viu o mês inteiro na Visão Geral.
Com as contas organizadas, dá pra cobrar o cliente por pix, boleto ou cartão e ver o pagamento entrar sozinho aqui. No próximo tutorial, a gente vê a integração com o asas. Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "Onde fica cada coisa.",
           2: "O caixa e o banco.",
           3: "Entrou dinheiro.",
           4: "Saiu dinheiro.",
           5: "A compra direta.",
           6: "De uma conta pra outra.",
           7: "O cartão da empresa.",
           8: "Compra parcelada.",
           9: "Pagar a fatura.",
           10: "O que vai vencer.",
           11: "Pagar e receber.",
           12: "Organizar as categorias.",
           13: "A visão geral do mês.",
           14: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "Financeiro",
           2: "Contas",
           3: "Lançamentos",
           4: "Lançamentos",
           5: "Lançamentos",
           6: "Lançamentos",
           7: "Cartão",
           8: "Cartão",
           9: "Cartão",
           10: "Contas a pagar",
           11: "Contas a pagar",
           12: "Categorias",
           13: "Resumo",
           14: "Resumo"}

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
