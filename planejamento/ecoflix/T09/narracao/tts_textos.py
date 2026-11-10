# Texto enviado ao ElevenLabs (eleven_v4, voz Kaik Barreto) por capítulo do T9 "Pedidos e histórico do caixa".
# Gerado do roteiro.md (coluna Fala): cada linha do texto é uma linha da tabela Tela × Fala.
# Trocas de pronúncia em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   PDF -> "pê-dê-éfe" | Pop-ups -> "pópâps" | Popup -> "pópâp"
CAPS = {
0: """Oi! Neste tutorial a gente vai achar aquele pedido de três semanas atrás, corrigir o que saiu errado e imprimir o comprovante de novo.
Na Recicla Vale Metais, a Auto Peças Vale Forte ligou pedindo o comprovante da bateria que vendeu em vinte e um de outubro. E o pedido não aparece no nome dela.
Pra resolver, a gente usa duas telas: Pedidos, no menu lateral, e Histórico do Caixa, dentro de Financeiro.
Se você ainda não viu o tutorial Ticket de Pesagem, dá uma olhada antes. [pause] Primeiro, o trabalho de cada tela.""",
1: """Pedidos mostra cada compra e cada venda, uma por linha, de todos os caixas. É a tela pra achar um pedido, corrigir e imprimir de novo.
O Histórico do Caixa mostra os caixas já fechados: o dia de cada operador, com quanto abriu e quanto fechou. É a tela pra rever um dia inteiro e, se precisar, reabrir aquele caixa.
Todo pedido nasce dentro de um caixa. Por isso as duas telas andam juntas.
Vamos começar pelos pedidos.""",
2: """A tela abre no mês atual, com todas as compras e vendas, de todos os caixas e de todos os operadores.
Em cima, o resumo do período: quanto saiu em compras e quanto entrou em vendas, separado em dinheiro, Pix e saldo.
Cada linha tem quem lançou, a data, se é compra ou venda, o número, o cliente ou fornecedor, como foi pago e o valor.
Clicando na linha, ela abre com os materiais, o peso, o preço e como foi pago. Aqui, a latinha da Aparecida, de hoje cedo: vinte e quatro quilos. Guarda esse número.
No fim de cada linha fica o menu do pedido. Daqui a pouco a gente usa ele.""",
3: """A bateria da Auto Peças é de vinte e um de outubro. Então, primeiro o período: Mês passado.
Em Filtros, a busca acha pelo nome do cliente ou fornecedor, pelo número do pedido, pelo operador ou pela placa. Digito Vale Forte.
No nome da Auto Peças, nenhuma compra de bateria em outubro. A bateria não está aqui.
Então eu procuro pelo que eu sei da compra. Tipo, Compras. Material, Bateria automotiva. E a forma de pagamento, Pix.
Achou: vinte e um de outubro, duzentos e quarenta quilos de bateria, setecentos e quarenta e quatro reais. Só que no nome do Depósito Irmãos Siqueira.
O pedido saiu no fornecedor errado. Repara que cada filtro vira uma etiqueta aqui em cima, e o Limpar todos tira tudo de uma vez.""",
4: """Achado o pedido, vem a correção. Em Editar, a janela avisa: se o pedido é de um caixa já fechado, o acerto vai pro caixa de hoje, e o pedido antigo fica marcado como estornado.
Uma dica: pra pedido de caixa fechado, o caminho mais tranquilo é reabrir o caixa daquele dia, corrigir lá dentro e fechar de novo. Assim não nasce estorno nem lançamento no caixa de hoje. É o que a gente faz no fim do tutorial.
Então eu cancelo e começo pelo que é de hoje. Lembra da latinha da Aparecida? Ela trouxe quarenta e dois quilos, não vinte e quatro.
O caixa de hoje está aberto, então é só editar. A compra abre do jeito que foi lançada, com o selo de edição em cima. Dá pra mudar o fornecedor, os itens, o peso, o preço e a forma de pagamento.
No item, Editar. Ele volta pro formulário, eu troco o peso pra quarenta e dois quilos, e o total vai pra duzentos e sessenta reais e quarenta.
Incluir Item, e o item volta pra lista com o peso certo.
Agora, o que o sistema faz ao salvar. Ele não soma por cima. Primeiro desfaz o pedido antigo inteiro: tira os vinte e quatro quilos do estoque e devolve o dinheiro pro caixa.
Depois grava o pedido certo como se fosse a primeira vez: quarenta e dois quilos no estoque, e duzentos e sessenta e quarenta saindo do caixa.
No fim, o estoque ganha só os dezoito quilos que faltavam, e do caixa sai só a diferença que a Aparecida recebe. Nada duplica.
Finalizar Compra, em dinheiro, Confirmar pagamento. Os avisos mostram as duas etapas: reverte o original e cria o editado.
Uma dica: não lance uma compra nova só com a diferença. Edite o pedido: o sistema desfaz o antigo e grava o certo, e o estoque fica correto.""",
5: """E quando o pedido nem devia existir? A compra do Valdir saiu duas vezes, com um minuto de diferença.
Em Excluir, antes de apagar, o sistema mostra tudo que vai desfazer: os duzentos e oitenta quilos de ferro misto saem do estoque, e os duzentos e dez reais voltam pro caixa.
Excluir pedido. Como o caixa de hoje está aberto, o pedido sai de vez.
Agora repara nesta compra de três de novembro, da Aparecida. Ela também saiu duas vezes, e a cópia foi excluída no dia cinco, com o caixa do dia três já fechado.
Aí o sistema não mexe no caixa antigo. Ele lança a correção no caixa do dia em que excluiu, e deixa o pedido na lista, com o selo Estornado e a data.
O pedido estornado não entra nos totais, e não dá mais pra editar nem excluir. Ele fica como o rastro de que existiu.
E quem excluiu o quê, e quando, fica no Histórico de Exclusões. Só o administrador abre: em Configurações, Empresa, Ver histórico.""",
6: """A Aparecida quer o comprovante novo, com os quarenta e dois quilos. No menu do pedido, Ver comprovante. Repara no aviso: pópâp bloqueado.
Todo pê-dê-éfe do sistema abre numa aba nova, e alguns navegadores bloqueiam isso na primeira vez.
Uma dica: pra liberar, clique no cadeado ao lado do endereço do site, procure pópâps e marque Permitir. É uma vez só.
Pronto: o comprovante abre na aba nova, com o peso certo. Daqui você imprime ou manda pra ela.
Agora o Valdir. Ele quer o comprovante pra mostrar o peso na obra de onde veio a sucata, sem mostrar quanto recebeu. No menu, Cupom sem valor.
A linha ganha o selo Comprovante sem valores.
E o comprovante sai só com o material e o peso. O pedido continua com o valor no sistema; só o papel sai sem.
Pra voltar ao normal, a mesma opção vira Mostrar valores no comprovante.""",
7: """E o caixa de vinte e um de outubro? Ele está no Histórico do Caixa, em Financeiro. Aqui fica cada caixa fechado, um por linha.
Cada linha tem o número do caixa, quando abriu e quando fechou, quem abriu, o saldo inicial e o final.
Essa correntinha junta os caixas fechados no mesmo dia, como o meu e o do Marcos, de ontem.
Clicando na linha, abre o resumo daquele caixa: compras, vendas, receitas, despesas e o lucro projetado.
A busca acha por nome, data ou número. Digito vinte e um barra dez, e aparecem os caixas daquele dia. O do Marcos é este aqui.
Em Filtros, dá pra escolher o operador e o período, quando a lista fica grande.""",
8: """Nas ações do caixa, Ver comprovante abre o relatório de fechamento daquele dia, o mesmo que sai quando o caixa fecha.
Ele traz com quanto abriu, o que entrou e saiu em cada forma de pagamento, e com quanto fechou.
Já o Relatório de estoque mostra, material por material, o que esse caixa comprou e vendeu, com o preço médio.
Olha a bateria aqui: duzentos e quarenta quilos, setecentos e quarenta e quatro reais. É um bom jeito de conferir o dia de um operador.
Os dois relatórios abrem em aba nova, igual ao comprovante do pedido.""",
9: """Agora a correção do jeito tranquilo. Nas ações do caixa de vinte e um de outubro, Reabrir caixa.
Pra reabrir, o dono do caixa não pode estar com outro caixa aberto. O Marcos não abriu caixa hoje, então a opção está liberada. Se estivesse, ela aparece apagada e explica que é preciso fechar o caixa atual dele primeiro.
O sistema confirma que o caixa volta exatamente como estava. Reabrir Caixa, e ele já leva pra tela do Caixa.
Em cima aparece a aba do caixa do Marcos, de vinte e um de outubro, do lado do meu de hoje. Dentro dele está a compra da bateria.
Editar. Como o caixa está aberto de novo, a edição é normal. No fornecedor, eu troco pra Auto Peças Vale Forte. O resto fica igual: duzentos e quarenta quilos, setecentos e quarenta e quatro reais.
Finalizar, Pix na conta principal, Confirmar pagamento. E o comprovante já sai certo, no nome da Auto Peças.
Repara: a compra corrigida ficou no caixa daquele dia, o do Marcos. O meu caixa de hoje não mudou.
Uma dica: se a correção ainda não aparece na aba Todas do histórico, recarregue a página antes de achar que sumiu.
Agora é fechar de novo. O valor de fechamento já vem com os seiscentos e doze e cinquenta daquele dia, porque a correção não mexeu no dinheiro da gaveta.
E como o caixa é de outro dia, eu ajusto a data e a hora do fechamento pro fim daquele dia: vinte e um de outubro, dezessete e trinta e um.
Confirmar Fechamento. Pronto: reabriu, corrigiu lá dentro e fechou de novo, sem estorno e sem mexer no caixa de hoje.
Uma dica: o mesmo vale pra qualquer lançamento com data de outro dia. Ele vai pro caixa daquele dia, não pro de hoje, e quando o caixa do dia é outro, o sistema pergunta em qual caixa lançar.""",
10: """Recapitulando: na tela Pedidos, a gente achou a bateria de três semanas atrás pelos filtros de período, tipo, material e pagamento, mesmo no nome errado.
Corrigiu o peso da latinha da Aparecida editando o pedido, sem duplicar estoque nem caixa.
Excluiu a compra duplicada do Valdir e entendeu o selo de estornado.
Reimprimiu o comprovante, liberou a aba nova no navegador e usou o cupom sem valor.
No Histórico do Caixa, abriu o resumo, o relatório de fechamento e o de estoque.
E reabriu o caixa de vinte e um de outubro com segurança, corrigiu o fornecedor lá dentro e fechou de novo.
No próximo tutorial, o estoque: quanto tem, de onde veio e quanto valia. Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "Duas telas, dois trabalhos.",
           2: "A tela Pedidos.",
           3: "Filtrar até achar.",
           4: "Editar um pedido.",
           5: "Excluir e o selo de estornado.",
           6: "Reimprimir e cupom sem valor.",
           7: "O Histórico do Caixa.",
           8: "Relatórios do caixa.",
           9: "Reabrir um caixa antigo.",
           10: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "Pedidos",
           2: "Pedidos",
           3: "Pedidos",
           4: "Correções",
           5: "Correções",
           6: "Comprovantes",
           7: "Histórico",
           8: "Histórico",
           9: "Histórico",
           10: "Resumo"}

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
