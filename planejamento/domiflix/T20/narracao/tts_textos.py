# Texto enviado ao ElevenLabs (eleven_v4, Fernanda) por capítulo do T20 "Relatório Financeiro e DRE".
# Gerado do roteiro.md (coluna Fala) pelo gerador do lote 4: cada linha do texto é uma linha da tabela Tela × Fala.
# Trocas de pronúncia em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   Asaas -> "asas" | PDF -> "pê-dê-éfe" | DRE -> "dê érri ê" | DFC -> "dê-éfe-cê" | CSV -> "cê-ésse-vê" | Excel -> "ékisel"
CAPS = {
0: """Oi! Neste tutorial a gente vai ler o que o dinheiro lançado no Financeiro está dizendo: o resultado do mês, o caixa dos próximos dias e o pacote pro contador.
Tudo isso fica em Relatórios, no menu Financeiro, em cinco abas: Visão Geral, dê érri ê Resultado, dê-éfe-cê Fluxo de Caixa, Contabilidade e Análise. Pra ficar mais claro, a Glaciál já tem lançados os três meses anteriores.
Se você ainda não viu os tutoriais do Financeiro e da integração com o asas, dá uma olhada antes. [pause] Vamos começar pela visão geral.""",
1: """A visão geral fica melhor com mais de um mês, então eu escolho, no período Personalizado, os três meses que já fecharam.
Repara que essa aba abre no Regime de Caixa, que mostra o que de fato entrou e saiu da conta. Daqui a pouco a gente vê a diferença pro de competência.
Os três números de cima resumem o período: o faturamento, o resultado e a margem. A margem diz quanto sobra de cada cem reais que entram.
No gráfico de receita e despesa, mês a mês, dá pra ver qual mês foi mais fraco.
E embaixo, de onde veio a receita e pra onde foi a despesa, por categoria.""",
2: """Agora o dê érri ê, o demonstrativo de resultado. Ele explica de onde veio o resultado do mês, linha por linha. Pra ler um mês fechado, escolho Mês passado.
Em cima da tabela ficam o Configurar dê érri ê, a escolha do regime, o Incluir projeções e o Exportar.
A tabela segue uma ordem. A receita bruta, menos os impostos, dá a receita líquida. Menos o custo dos serviços prestados, dá o lucro bruto. E, menos as despesas operacionais, o resultado líquido.
Clicando num grupo, aparecem as categorias dele. No custo dos serviços estão o material, a mão de obra avulsa e as peças e componentes, que a gente criou no tutorial do Financeiro.
E a coluna da direita mostra o peso de cada linha sobre o faturamento. Assim você vê, por exemplo, quanto do que entrou foi gasto em material.""",
3: """E os grupos do dê érri ê você organiza do seu jeito. Em Configurar dê érri ê fica a estrutura inteira, separada pela natureza de cada grupo: receita, dedução, custo e despesa operacional.
Repara: a empresa já nasce com um subgrupo de despesa operacional, o Despesas com pessoal, e todas as despesas do dia a dia caem nele, do salário ao aluguel. Dá pra mudar o nome no lápis, mas aqui eu vou separar as despesas.
Em Novo subgrupo, a natureza é Despesa operacional, e o nome, Despesas administrativas. Adicionar.
Agora é só levar o aluguel pra lá. Dá pra arrastar, ou usar o seletor da categoria e escolher o grupo novo. A energia e as ferramentas vão do mesmo jeito.
E crio mais um, Despesas com veículos, pro combustível.
Repara que só a apresentação muda: os lançamentos continuam iguais. E, se precisar, em Outras visões dá pra montar formas diferentes de ver o mesmo dê érri ê.
De volta ao dê érri ê, os dois subgrupos já aparecem nas despesas operacionais.""",
4: """Agora o botão que mais gera dúvida: caixa ou competência. O dê érri ê abre no Regime de Competência, em que cada lançamento entra no mês em que aconteceu, pago ou não.
Em competência, o mês passado tem a instalação do Condomínio Jardim Azul, que foi feita no fim do mês, e a primeira parcela da bomba de vácuo, comprada no cartão.
Agora, no Regime de Caixa. Repara que a receita diminuiu e a bomba de vácuo saiu do mês. No caixa, só entra o que já foi pago ou recebido, no mês em que o dinheiro se mexeu.
E onde elas foram parar? Em Este mês. O condomínio pagou a instalação no começo deste mês, e a parcela do cartão entrou quando a fatura foi paga.
As duas visões estão certas, cada uma responde uma pergunta. Competência mostra se o mês deu lucro, e caixa mostra o dinheiro que de fato passou pela conta. Uma dica: combina com o seu contador qual dos dois ele usa.""",
5: """Com o cartão, são três datas: o dia da compra, o fechamento da fatura e o dia em que você paga a fatura.
Em competência, cada parcela entra no mês dela, a partir do mês da compra. Em caixa, ela entra no mês em que a fatura foi paga, por inteiro.
E o mês da fatura não conta pro resultado: ele só diz quando o pagamento vence.
Por isso a bomba de vácuo aparece aqui, no mês em que a fatura foi paga.
E a transferência entre contas e o pagamento da fatura ficam fora do dê érri ê nos dois regimes. É dinheiro mudando de lugar, e não resultado.""",
6: """E dá pra olhar um mês ao lado do outro. Volto pro mês passado e clico em Comparar períodos. Escolho Período anterior e clico em Aplicar comparação. A tabela ganha a coluna do mês anterior, ao lado do atual.
Assim você vê na hora o que cresceu e o que caiu de um mês pro outro.
E agora pra frente. Em competência, com um período que vai até o fim do mês que vem, aparece o Incluir projeções. Ligado, ele soma as próximas mensalidades das assinaturas: aqui, um ciclo de trezentos e oitenta reais, da assinatura da Academia Ponto Forte.
Repara no rodapé: a projeção só aparece no relatório. Nenhum lançamento é criado.""",
7: """O dê érri ê conta o passado. Pro caixa dos próximos dias tem o dê-éfe-cê, o fluxo de caixa. Ele abre no Previsto, com o saldo de hoje e o que vai entrar e sair nos próximos quinze dias.
Em Próximos, dá pra ver trinta dias. A tabela vai dia a dia: o saldo que começa, o que entra, o que sai e o saldo que fica.
Clicando num valor, aparecem as contas daquele dia, como o aluguel do galpão. Assim dá pra ver o dia em que a conta aperta, antes de chegar nele.
A previsão considera tudo pago no vencimento. E o que já venceu sem baixa aparece separado, na coluna Dívida. Aqui ela está vazia, porque nada ficou em atraso.""",
8: """No Realizado, o que de fato entrou e saiu no período: o saldo do começo, a variação e o saldo do fim.
As entradas e saídas aparecem separadas pelo grupo dê-éfe-cê de cada categoria. Aqui é tudo da operação: os serviços, o material, o aluguel.
E o Exportar leva o fluxo pra ékisel, pê-dê-éfe ou cê-ésse-vê. Uma dica: lucro e dinheiro em caixa são perguntas diferentes, e um mês com lucro pode fechar com pouco caixa.""",
9: """No fim do mês, o contador pede tudo isso num arquivo só. É a aba Contabilidade, com o Pacote para Contabilidade, uma planilha de ékisel com várias abas.
Vão juntos os lançamentos completos, o dê érri ê e o dê-éfe-cê, os saldos e as contas em aberto, e o plano das categorias.
Confiro o período lá em cima e clico em Exportar pacote. Pronto, é só mandar o arquivo pro contador.""",
10: """A última aba é a Análise. Ela tem os próprios períodos: aqui, mês a mês, os últimos três meses, com a variação de um pro outro.
Embaixo, os clientes. No Maior faturamento, o Hotel Mirante do Mar vem na frente.
Agora, trocando pra Melhor margem, quem sobe é a Padaria Bom Grão. O hotel fatura muito, mas gasta mais com material e peças pra entregar.
É por isso que vale ligar o cliente na receita e no custo: quem fatura mais nem sempre é quem deixa mais dinheiro.""",
11: """Pra fechar, um roteiro de fechamento do mês. No fim, o dê érri ê sai em ékisel ou pê-dê-éfe, do jeito que está na tela.
Antes de exportar, dá baixa nas contas do mês, paga a fatura do cartão e confere o extrato com o banco.
Depois confere o período e o regime: o arquivo sai exatamente com o que está na tela.""",
12: """Pronto! Recapitulando: a visão geral dá o tamanho do período, e o dê érri ê mostra de onde veio o resultado, linha por linha, com os grupos organizados do seu jeito.
Competência conta o mês em que aconteceu, caixa conta o mês em que o dinheiro se mexeu, e a compra no cartão segue essa mesma regra.
O dê-éfe-cê mostra o caixa dos próximos dias, e o pacote leva tudo pro contador num arquivo só.
E a Análise compara os meses e mostra quais clientes deixam mais dinheiro.
Resultado lido, falta a nota fiscal do serviço. No próximo tutorial, a gente vê as notas fiscais. Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "A visão geral.",
           2: "O resultado do mês.",
           3: "Organizar os grupos.",
           4: "Caixa ou competência.",
           5: "A compra no cartão.",
           6: "Comparar e projetar.",
           7: "O caixa dos próximos dias.",
           8: "O que de fato entrou e saiu.",
           9: "O pacote do contador.",
           10: "Comparar meses e clientes.",
           11: "Fechar o mês.",
           12: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "Relatórios",
           2: "DRE",
           3: "DRE",
           4: "DRE",
           5: "DRE",
           6: "DRE",
           7: "DFC",
           8: "DFC",
           9: "Contabilidade",
           10: "Análise",
           11: "Resumo",
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
