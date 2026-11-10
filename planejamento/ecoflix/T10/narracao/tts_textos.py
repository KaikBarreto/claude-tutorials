# Texto para o ElevenLabs (eleven_v4, voz Kaik Barreto) por capítulo do T10 "Estoque: saldo, histórico e posição".
# Gerado do roteiro.md (coluna Fala): cada linha do texto é uma linha da tabela Tela × Fala ("(sem fala)" fica de fora).
# Trocas de pronúncia em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   Kardex -> "cardécs" | PDF -> "pê-dê-éfe" | Excel -> "ékisel" (nova: testar) | Lucro s/ Vendas -> "Lucro sobre vendas"
# Números por extenso, como se fala; a legenda volta para kg e R$ pelo "numeros" do config.
CAPS = {
0: """Oi! Neste tutorial a gente vai responder as três perguntas que o contador da Recicla Vale Metais faz todo fim de mês.
Quanto material tem hoje no pátio, de onde ele veio e quanto tinha no dia trinta e um.
As respostas ficam no menu Materiais, em quatro telas que conversam entre si.
Se você ainda não viu o tutorial Pedidos e histórico do caixa, dá uma olhada antes. É de lá que vêm os pedidos que mexem no estoque.""",
1: """Vamos às quatro portas. Clicando em Materiais, aparecem as três primeiras: Estoque, Histórico e Relatório.
A quarta fica dentro do Estoque, aqui na coluna das tabelas de preço: a Posição de Estoque.
O Estoque mostra quanto tem agora. O Histórico conta cada entrada e cada saída. O Relatório soma o que você comprou e vendeu num período. E a Posição mostra quanto tinha numa data.
A gente começa pelo saldo de agora.""",
2: """Esta é a tela do saldo. Os três cartões de cima somam o pátio inteiro.
O Peso Total em Estoque é a soma do saldo de todos os materiais.
O Total Pago é quanto esse estoque custou, pelo preço médio que você pagou. E a Projeção de Vendas é quanto ele vale pela tabela de venda.
Olha o cobre mel: quarenta e dois quilos no Estoque Atual, pagos em média a quarenta e dois e cinquenta o quilo.
Esse é o preço médio do material que você tem hoje. Por isso ele vem com o selo de estimativa.
O Estoque Atual é o saldo de verdade. Ele muda com tudo o que entra e sai: compra, venda, transferência, ajuste manual, exclusão e produção.
Então, quando alguém pergunta quanto tem, a resposta é aqui. O ferro misto, por exemplo, está com seis mil quatrocentos e vinte quilos.""",
3: """Agora, a transferência. Ontem, na separação, o Marcos tirou trezentos e vinte quilos de ferro pesado do meio do ferro misto.
O peso é o mesmo, só mudou de material. A transferência registra isso: sai de um, entra no outro.
Na linha do ferro misto, eu abro o menu e clico em Transferir estoque.
A janela mostra o estoque atual do ferro misto: seis mil quatrocentos e vinte quilos.
No material de destino, escolho o ferro pesado. E na quantidade, trezentos e vinte quilos.
Transferir. Pronto: o ferro misto ficou com seis mil e cem quilos, e o ferro pesado, com dois mil e quinhentos.
E quando você marca vários materiais, a barra de baixo traz o Transferir Estoque. Esse botão é outra coisa: ele leva material entre a matriz e a filial, e faz parte do Gerencial, que depende do plano contratado.""",
4: """Agora o Histórico, de onde veio cada quilo. É o cardécs do estoque.
O cardécs é a ficha de cada material, como um extrato de banco. Cada linha é uma entrada ou uma saída, com o saldo antes e depois.
Escolho o ferro pesado aqui na coluna dos materiais. Repara que a transferência que a gente fez já está em cima.
É só ler da esquerda pra direita: tinha dois mil cento e oitenta quilos, entraram trezentos e vinte, ficou com dois mil e quinhentos.
A linha de baixo veio antes: uma compra de ontem, de oitocentos e sessenta quilos. O estoque final dela, dois mil cento e oitenta, é o inicial da transferência.
É uma corrente: o final de uma linha é o começo da seguinte. Assim dá pra seguir o material quilo a quilo.
Uma dica: o Histórico abre em Este mês. Hoje é dia dez, então ele mostra dez dias.
Pra ver mais, é só trocar o período pra Este ano ou Todos os tempos. Assim, quem abre a tela no dia dois não acha que o histórico sumiu: só estava vendo dois dias.""",
5: """Cada linha tem um tipo, com uma cor.
No filtro de tipo aparecem todos os sete.
Compra é material que entrou porque você comprou. Venda é o que saiu porque você vendeu. Transferência tira de um material e põe em outro.
Edição Manual é um ajuste feito direto no estoque, sem compra nem venda. Exclusão é quando um pedido é excluído, ou um material com estoque sai do cadastro: o saldo volta.
Produção aparece pra quem usa a Produção, que depende do plano contratado: é a latinha que vira fardo, por exemplo. E o Saldo inicial é a quantidade com que o material entrou no sistema.
Vou deixar só esses dois tipos. No sábado, dia trinta e um, o Rafael contou o pátio e ajustou o ferro pesado: menos catorze quilos.
Abrindo a linha, aparece a observação que ele escreveu, o estoque antes e depois, quem fez e a hora.
E aqui, uma compra de cento e oitenta quilos que tinha entrado duas vezes. A repetida foi excluída, e o estoque voltou.
Uma dica sobre os filtros de Fornecedores e de Clientes: o de fornecedor mexe nas compras, e o de cliente, nas vendas.
Com um deles marcado, a transferência, o ajuste manual e a exclusão saem da lista, porque não têm fornecedor nem cliente. Não é erro.
Pra ver tudo de novo, é só limpar os filtros.""",
6: """Toda linha de compra ou de venda abre o pedido que gerou ela. Clicando na compra de ontem, aparece o que veio.
Oitocentos e sessenta quilos de ferro pesado, a noventa e cinco centavos, deu oitocentos e dezessete reais.
Embaixo, o fornecedor, o Depósito Irmãos Siqueira, como foi pago, no Pix, e o total do pedido.
E as fotos tiradas na hora da compra. Clicando, a foto amplia.
Quando o contador pergunta de onde veio o ferro, a resposta está aqui: o pedido, o pagamento e as fotos, na mesma linha.""",
7: """Agora o Relatório de Estoque: tudo o que você comprou e vendeu num período.
Ele também abre em Este mês. Pra fechar outubro, escolho Mês passado.
Uma dica: o Relatório conta só os pedidos finalizados, pela data de cada pedido. Pedido excluído ou estornado fica de fora.
Em cima, quatro cartões: Total Comprado, Total Vendido, Lucro e Projeção de Lucro.
Clicando num cartão, ele abre os detalhes, como o preço médio de compra e o material que mais comprou.
A Projeção de Lucro é uma estimativa.
Ela imagina que você vendeu tudo o que comprou no mês, pelo preço médio de venda, ou pelo da tabela se o material não teve venda. É lucro bruto, sem as despesas.
Uma dica: o saldo da tela de Estoque não é o comprado menos o vendido daqui.
O Relatório só soma compras e vendas do período. O saldo vem acumulado desde o começo e muda também com transferência, ajuste manual, exclusão e produção. Quando os números não batem, é quase sempre isso.""",
8: """Embaixo dos cartões fica o detalhamento, material por material.
Olha o cobre mel em outubro: comprou novecentos e oitenta quilos, por quarenta e um mil seiscentos e cinquenta reais. Dividindo o valor pelos quilos, dá o preço médio de compra: quarenta e dois e cinquenta.
Uma dica: a quantidade comprada daqui é a líquida, já sem a tara e a impureza. A Dona Cida pôs oitenta e seis quilos de latinha na balança. Tirando o saco e a sujeira, seis quilos, entraram oitenta quilos. Por isso esse número pode ser menor que o peso que você lembra de ter pesado.
E o cobre mel vendeu mil quilos, por quarenta e sete mil e novecentos reais, a quarenta e sete e noventa em média.
O Resultado é o vendido menos o comprado no mês: seis mil duzentos e cinquenta reais. E a Margem é esse resultado em porcentagem do que foi vendido: uns treze por cento.
Já o Lucro sobre vendas olha só o que foi vendido: a diferença entre os dois preços médios, vezes os mil quilos. Dá cinco mil e quatrocentos. Também é estimativa.
Uma dica: material com muita compra e nenhuma venda, como a bateria automotiva, mil trezentos e vinte quilos comprados, não é erro. É material que entrou e ainda não saiu do pátio.""",
9: """Agora repara o que acontece quando eu filtro por um fornecedor, o Depósito Irmãos Siqueira. Ficam só as compras. O Total Vendido, o Lucro e as colunas de venda saem.
É de propósito. O cobre misto do Siqueira foi pra mesma pilha do cobre do Valdir. Quando a Fundição compra, não tem como saber de quem era cada quilo.
Então, com esse filtro, o relatório responde uma pergunta: quanto você comprou do Siqueira, de cada material, e a que preço.
Pra ver venda, lucro e margem, é só tirar o filtro.""",
10: """E a terceira pergunta do contador: quanto tinha no dia trinta e um. A Posição de Estoque abre no dia de hoje, no fim do dia.
Hoje, o ferro pesado está com dois mil e quinhentos quilos.
A Posição é uma foto do estoque. Você escolhe a data e a hora, e ela mostra o saldo de cada material naquele instante. O que entrou ou saiu depois fica fora da foto.
Eu volto o calendário pra outubro e clico no dia trinta e um. A hora fica em vinte e três e cinquenta e nove, então entra tudo o que aconteceu no sábado.
Ver posição.
No dia trinta e um, o ferro pesado tinha quarenta e um mil oitocentos e sessenta quilos. A diferença pra hoje são as compras, as vendas e a transferência de novembro.
Do lado, o valor desse estoque, pelo custo médio das compras até aquela data, e a projeção, pelo preço de venda de hoje. Embaixo, o total geral.""",
11: """Com a foto do dia trinta e um na tela, é só exportar. No Exportar, escolho pê-dê-éfe.
Aqui você escolhe as colunas e os materiais do arquivo. A tela guarda essa escolha pra próxima vez.
Exportar, e o pê-dê-éfe abre numa aba nova, pronto pra baixar e mandar pro contador.
Se o contador preferir planilha, o mesmo caminho em ékisel baixa o arquivo.
O Histórico e o Relatório também exportam, cada um pelo seu botão.""",
12: """Pronto! Recapitulando: a gente conferiu o saldo de cada material na tela de Estoque e transferiu trezentos e vinte quilos do ferro misto pro ferro pesado.
Leu o cardécs linha a linha, conheceu os tipos de movimentação e abriu uma compra pra ver o pedido, o pagamento e as fotos.
No Relatório, viu o comprado, o vendido, o resultado e a margem do mês, e por que o filtro de fornecedor mostra só as compras.
E tirou a foto do estoque do dia trinta e um, exportada em pê-dê-éfe e ékisel pro contador.
No próximo tutorial, a gente cuida das contas que vencem: as que você paga e as que você recebe. Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "As quatro portas do estoque.",
           2: "O saldo de cada material.",
           3: "Transferir entre materiais.",
           4: "O cardécs, linha a linha.",
           5: "Os tipos de movimentação.",
           6: "O pedido por trás da linha.",
           7: "Comprado, vendido e lucro.",
           8: "Material por material.",
           9: "O filtro de fornecedor.",
           10: "A foto do estoque numa data.",
           11: "Exportar para o contador.",
           12: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "Estoque",
           2: "Estoque",
           3: "Estoque",
           4: "Histórico",
           5: "Histórico",
           6: "Histórico",
           7: "Relatório",
           8: "Relatório",
           9: "Relatório",
           10: "Posição",
           11: "Posição",
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
