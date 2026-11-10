# Texto enviado ao ElevenLabs (eleven_v4, voz Kaik Barreto) por capítulo do T25 "Dashboard, Agenda e rotina".
# Gerado do roteiro.md (coluna Fala): cada linha do texto é uma linha da tabela Tela × Fala.
# Trocas de pronúncia em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   EcoSistema -> "Ecossistema" | Cato -> "Cáto" | Ctrl+K -> "contról-cá" | DRE -> "dê-érri-ê" | MTR -> "ême-tê-érre"
#   CDF -> "cê-dê-éfe" | Vence em 7 dias -> "Vence em sete dias" (o rótulo do cartão; a legenda volta ao 7)
#   Shift -> "xífti" e Shift+C/V/X/A/D/E -> "xífti-cê" / "xífti-vê" / "xífti-xis" / "xífti-á" / "xífti-dê" / "xífti-é" (novas, testar)
#   Números e "Contas a Pagar e Receber" já vão como se fala; a legenda volta à grafia da tela pelo "numeros" do config.
CAPS = {
0: """Oi! Esta é a última aula da Formação básica. Neste tutorial, a gente lê os números do Dashboard e monta a rotina que mantém o sistema vivo.
Na Recicla Vale Metais, o Rafael começa o dia com três perguntas: como vai o mês, que conta vence e o que tem pra amanhã.
As respostas ficam em duas telas do menu: o Dashboard, no alto, e a Agenda, no fim.
Se você ainda não viu o tutorial do Cáto, o assistente, dá uma olhada antes. [pause] Vamos aos números.""",
1: """Lá em cima ficam três cartões: Total Compras, Total Vendas e a Margem. Eles seguem o filtro de período, que abre em Este mês.
Repara na margem: é só as vendas menos as compras do período. Em novembro, até hoje, a Recicla Vale comprou mais do que vendeu, e ela aparece negativa, em vermelho.
Uma dica: margem não é lucro. Esse vermelho é material comprado que ainda está no pátio, esperando a venda. O lucro de verdade, com custo, imposto e despesa, fica no Relatório Financeiro.
Agora, outubro inteiro. As vendas passaram as compras, e a margem ficou positiva: doze mil trezentos e oitenta reais.
Em Ver detalhes, a conta aparece aberta: o total de vendas, menos o total de compras, dá a margem.""",
2: """Mais abaixo, os gráficos. Em Compras versus Vendas, cada mês tem duas barras: o que a empresa comprou e o que vendeu.
Do lado, a Evolução da Margem mostra como a margem andou, mês a mês.
Uma dica: esses gráficos mostram sempre seis meses, mesmo com o filtro num mês só. O filtro manda nos cartões e nos rankings.
Embaixo, o Comparativo Mensal põe o mês passado inteiro contra o mês atual, até hoje.
Uma dica: como hoje é dia dez, a queda aparece grande. É normal no começo do mês: são dez dias contra trinta e um. Até o fim do mês, a comparação vai ficando justa.""",
3: """E quantos quilos entram por semana? O Volume Semanal de Compras mostra as últimas oito semanas, em quilos.
Passando o mouse, aparece o peso de cada semana. São sempre as mesmas oito semanas, seja qual for o filtro.
Nos rankings, o filtro volta a valer. Em outubro, o material mais comprado foi o ferro pesado, em reais e em quilos: cinquenta mil quilos.
Em Principais Fornecedores, o primeiro é o Depósito Irmãos Siqueira, que trouxe a maior parte desse ferro.
Em Principais Clientes, a Fundição Bandeira do Vale lidera em reais, com o cobre. Em quilos, quem lidera é a Aços Quiririm, com o ferro.
E em Ver todos os clientes aparece a lista completa do período.""",
4: """E dá pra deixar o painel do seu jeito. No botão Configurações, ao lado do filtro, ficam todas as partes do Dashboard.
Cada parte tem a sua chave. Desligo Métodos de Pagamento, e ele sai do painel.
Pra mudar a ordem, é só segurar o cantinho do cartão e arrastar. Trago o Volume Semanal pra perto do topo.
Se quiser desfazer, o Voltar ordem ao normal põe o painel como era. E a arrumação fica salva no seu usuário, neste navegador.""",
5: """Agora, a Agenda, no fim do menu. Ela abre no mês, com o dia de hoje marcado, e do lado ficam as tarefas do dia.
Pra marcar uma tarefa, é em Nova Tarefa. A revisão do caminhão truck, na quinta, dia doze, às nove da manhã.
Com Lembrar no dia ligado, ela avisa no dia. Salvo, e ela já está no calendário.
A oficina só pode na sexta? É só arrastar a tarefa pro dia treze.
E os feriados aparecem sozinhos, com uma estrela: a Proclamação da República, no dia quinze, e a Consciência Negra, no dia vinte.
Pra esconder os feriados, é em Configurações, Usabilidade, Exibir Feriados.""",
6: """Além das tarefas, a Agenda mostra sozinha os avisos do dinheiro: as contas a pagar em vermelho e as a receber em verde, no dia do vencimento.
No dia dezessete, por exemplo, tem quatro mil setecentos e noventa reais a receber: a primeira parcela da Fundição Bandeira do Vale.
E no dia vinte e três, dois mil trezentos e sessenta reais a pagar: a parcela dos pneus, na Auto Peças Vale Forte.
O fiado com vencimento entra do mesmo jeito, uma vez só: cada parcela no seu dia.
Clicando no aviso, você vai direto pra Contas a Pagar e Receber, pra conferir ou dar baixa.
E o vencimento da assinatura do Ecossistema também entra, em laranja: aqui, no sábado, cinco de dezembro.
E as tarefas com Lembrar no dia aparecem no alto do Dashboard, no dia certo.""",
7: """Pra andar mais rápido, tem os atalhos de teclado. Apertando a interrogação, aparece a lista inteira.
É sempre xífti mais uma letra: xífti-cê abre a compra, xífti-vê a venda, xífti-xis o caixa e xífti-á a agenda.
Olha: xífti-xis, e o caixa abre. xífti-dê, e volto pro Dashboard.
Os atalhos valem fora dos campos de texto. Com o cursor num campo, a letra vai pro campo.
E o contról-cá abre a busca de tudo: telas, clientes, fornecedores, materiais e funcionários.
Digito cobre, e os materiais aparecem na hora. No Cobre mel, o painel mostra o estoque e os preços: quarenta e dois e cinquenta na compra e quarenta e sete e noventa na venda.
Com Enter, você vai direto pra ele. É o jeito mais rápido de achar qualquer coisa.""",
8: """Bom, números lidos e agenda em uso. Agora, a rotina que mantém o sistema vivo, começando pela diária: uns dez minutos, logo cedo.
Ao abrir o sistema de manhã, ele já mostra as tarefas de hoje, como a cotação do cobre com a Fundição, às duas da tarde.
Primeiro, o caixa. No Histórico do Caixa, você confere se os caixas de ontem fecharam, com o saldo final de cada um. Depois, é só abrir o caixa do dia.
Depois, as contas. Em Contas a Pagar e Receber, os cartões Vencidas e Vence em sete dias mostram o que pede atenção agora.
E, na Agenda, o que tem pra amanhã: a coleta na Auto Peças Vale Forte, às oito da manhã.
Quem tem o módulo de Coletas confere também as ordens de coleta do dia seguinte. Ele depende do plano contratado.""",
9: """Uma vez por semana, meia hora pra duas conferências: o estoque e o fiado.
xífti-é abre o Estoque. Aqui você confere se o saldo bate com o que tem no pátio, pelo menos nos materiais que mais giram, como o cobre e a latinha.
Pra acertar uma diferença, o caminho está na aula do estoque.
Depois, o fiado. Em Contas a Pagar e Receber, na aba A Receber, ficam as parcelas e o fiado de cada cliente.
O que passar da data aparece como Vencida, e é hora de cobrar. Assim, nenhum fiado fica esquecido.""",
10: """E uma vez por mês, o fechamento: umas duas horas, em quatro passos.
Conciliar o extrato do banco com o sistema e conferir o dê-érri-ê do mês, no Relatório Financeiro.
Mandar o pacote das notas pro contador e ver se ficou algum ême-tê-érre ou cê-dê-éfe pendente. Esses dois dependem do módulo de notas fiscais, do plano contratado.
Pra não esquecer, a gente marca o fechamento na Agenda, no primeiro dia útil: terça, primeiro de dezembro.
Nova Tarefa: Fechamento de novembro, com os quatro passos na descrição, às oito da manhã, e Lembrar no dia ligado. No dia, ela aparece logo cedo.""",
11: """Pronto! Recapitulando: a gente leu o Dashboard sem confundir margem com lucro, com os gráficos de seis meses, o comparativo e os rankings.
Deixou o painel do seu jeito, escondendo e trocando os cartões de lugar.
Marcou e mudou uma tarefa de dia na Agenda e viu os avisos que aparecem sozinhos.
Usou os atalhos e a busca do contról-cá.
E montou as três rotinas: a diária, a semanal e a mensal.
A Formação básica acabou. No próximo tutorial, começam as aulas dos módulos que fazem parte do seu plano. Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "Comprado, vendido e margem.",
           2: "Seis meses e o comparativo.",
           3: "Semanas e rankings.",
           4: "O painel do seu jeito.",
           5: "Tarefas no calendário.",
           6: "Os avisos automáticos.",
           7: "Atalhos e o contról-cá.",
           8: "A rotina diária.",
           9: "A rotina semanal.",
           10: "A rotina mensal.",
           11: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "Dashboard",
           2: "Dashboard",
           3: "Dashboard",
           4: "Dashboard",
           5: "Agenda",
           6: "Agenda",
           7: "Atalhos",
           8: "Rotina",
           9: "Rotina",
           10: "Rotina",
           11: "Resumo"}

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
