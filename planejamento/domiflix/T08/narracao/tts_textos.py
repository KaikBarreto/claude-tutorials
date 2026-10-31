# Texto enviado ao ElevenLabs (eleven_v4, Fernanda) por capítulo do T8 "Estoque, compras e inventário".
# Gerado do roteiro.md (coluna Fala): cada linha do texto é uma linha da tabela Tela × Fala.
# Trocas de pronúncia em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   Excel -> "ékisel" | Kardex -> "cárdex" | NF-e -> "ene-éfe-é" | PDF -> "pê-dê-éfe" | PDV -> "pê-dê-vê" | XML -> "xis-eme-éle" | ticket -> "tíquete" | 25 A -> "vinte e cinco ampères" | 35 µF -> "trinta e cinco microfarads" | 40 µF -> "quarenta microfarads" | R-32 -> "érre trinta e dois" | R-410A -> "érre quatrocentos e dez á" | Van 01 -> "van zero um"
CAPS = {
0: """Oi! Neste tutorial a gente vai cuidar do que a Glaciál Côude Brasil tem guardado: os materiais, os locais onde eles ficam, as compras para repor e a contagem.
Quando o técnico usa um gás, quando chega uma entrega, quando uma peça está acabando, tudo passa por aqui. Você sabe o que tem, onde está e quanto custou.
Se você ainda não viu o tutorial Área do Técnico: Refrigeração e Climatização, dá uma olhada antes. [pause] Vamos conhecer a tela.""",
1: """A tela tem seis abas: Estoque Atual, Histórico de Materiais, que é o cárdex, Compras de Material, Inventários, Posição de Estoque e Relatório. Lá em cima ficam também os botões Importar xis-eme-éle da ene-éfe-é e Configurações, que a gente usa mais à frente.
Começo pelo Estoque Atual. Os três cartões resumem o estoque: o total de itens, o valor investido, que é a quantidade vezes o custo de cada material, e quantos itens estão com estoque baixo.
Pra achar um material, é só buscar pelo nome ou pelo código. Em Filtros, dá pra ver só o que está abaixo do mínimo, ou só um grupo.
Cada linha traz o nome, o código, o grupo, a quantidade, a quantidade mínima e o custo unitário. Repara nestas duas, com o triângulo vermelho: estão abaixo do mínimo. O gás tem oito vírgula cinco, e o mínimo é dez.
Pra levar o estoque pra fora, o Exportar gera um pê-dê-éfe ou uma planilha do ékisel, com os materiais que você escolher.""",
2: """Vamos cadastrar um material do zero. Clico em Cadastrar Material e dou o nome: Capacitor quarenta microfarads.
O código já vem preenchido, no próximo número da sequência. Uma dica: se você tem um código seu, é só digitar por cima.
Em Grupo, escolho Elétrica. O Fornecedor vem da lista dos fornecedores cadastrados: a Polar Distribuidora de Peças.
A quantidade inicial é seis, em unidade. O preço de custo é o que a empresa paga: trinta e oito reais e noventa centavos. O preço de venda, setenta reais, é o que aparece quando o material entra num orçamento.
Em Locais deste material, marco o Estoque Principal e coloco o mínimo em quatro. É esse mínimo que dispara o alerta de estoque baixo, e ele vale para cada local. Sem mínimo, o material não avisa quando está acabando.
Tem ainda a foto, o código de barras e a chave Vendável na loja, que coloca o material no caixa do pê-dê-vê. São opcionais, e hoje ficam como estão.
Salvo, e o capacitor entra na lista com seis unidades. A quantidade inicial já fica registrada no histórico, como cadastro inicial.""",
3: """Quando chega material, registro a entrada. No menu da linha da Fita isolante, clico em Registrar entrada, digito dez e escrevo, em Observação, Compra no balcão. Repara no Saldo após, que mostra quanto vai ficar: trinta e oito. Confirmo.
A saída é igual. No capacitor, clico em Registrar saída e tiro três. Olho o Saldo após antes de confirmar, porque a Dominex não aceita uma saída maior do que o saldo.
O capacitor ficou com três, abaixo do mínimo de quatro. A linha fica vermelha, e o cartão Estoque baixo passa de dois para três.
Em Filtros, marco Estoque abaixo do mínimo e vejo só os três que precisam de reposição. Esse alerta olha o mínimo de cada local, e daqui a pouco isso vai fazer sentido.
Uma dica: no mesmo menu existe o Excluir. Para encerrar um material, zere o saldo e tire dos locais, porque ao excluir o histórico dele também é apagado.""",
4: """Quando a empresa tem uma van, ou mais de um depósito, entram os locais. Tudo começa em Configurações, que tem duas abas. Em Grupos de material ficam as famílias do estoque, cada uma com a sua cor: Gases, Cobre e tubos, Elétrica e Consumíveis.
Em Locais de estoque, já existe o Estoque Principal, o local padrão da empresa. Vou criar o da van do técnico: digito van zero um e clico no botão de mais.
Fechando a janela, cada local ganha a sua aba, e o principal leva uma estrela.
Agora digo o que existe na van. Na engrenagem da aba, em Adicionar por grupo, escolho Gases, e os gases já entram. Marco também a Fita isolante e salvo.
Uma dica: para tirar um material de um local, transfira o saldo antes, porque com saldo a Dominex não deixa remover e oferece o botão Transferir saldo.""",
5: """Com a van criada, vamos carregá-la. No Estoque Principal, no menu do Gás refrigerante érre quatrocentos e dez á, clico em Transferir.
A origem já vem preenchida, com oito vírgula cinco disponíveis. Escolho a van zero um como destino, digito dois quilos e anoto: Carga da van do Rafael.
Clico em Transferir. Na aba da van zero um, o érre quatrocentos e dez á aparece com dois quilos, e no Estoque Principal sobram seis vírgula cinco. A transferência tira de um local e põe no outro, e o histórico guarda os dois lados.""",
6: """Dá para escolher quem enxerga cada local. Na engrenagem da van, abro a aba Acesso. Por padrão, todos os usuários da empresa veem o local.
Ligo Restringir acesso a este local, e aparece a lista de pessoas. A Camila, que é administradora, mostra Sempre tem acesso: quem administra enxerga todos os locais.
Marco o Rafael Lima, que é quem usa a van, e clico em Salvar acesso. Agora só ele e a gestão veem e movimentam a van zero um.
Uma dica: marque sempre alguém, porque sem ninguém marcado o local continua aberto a todos.""",
7: """E tudo isso fica registrado no cárdex, o histórico dos movimentos do estoque. A coluna da esquerda lista os materiais, e a da direita traz o cárdex geral, com os movimentos de todos eles.
Cada linha diz quando foi, o tipo do movimento, o material e quem lançou, o local, o estoque antes, a alteração e o estoque depois. Aqui estão a entrada da fita, o capacitor que cadastramos e a saída dele. E a transferência mostra os dois locais na mesma linha.
Estas duas linhas de Consumo vêm da OS número dezesseis, que o técnico finalizou no tutorial dele. A baixa aconteceu porque a empresa ligou a opção Consumo de estoque na OS e o técnico anotou o que usou. Sem essa opção e sem os materiais anotados, concluir a ordem não mexe no estoque.
Nos Filtros, escolho o período, que começa no mês atual, o tipo de movimento e o local. Filtrando por Consumo, ficam só essas duas linhas.
E se eu clico num material, como o Gás refrigerante érre quatrocentos e dez á, vejo só o histórico dele. Todo movimento deixa rastro: quem fez, quando e de onde.""",
8: """Agora, o que fazer quando o material está acabando: as compras. Na aba Compras de Material, uma faixa vermelha já avisa que três materiais estão abaixo do mínimo.
Aqui em cima, o Fornecedores abre o cadastro dos fornecedores. O Registrar compra direta lança a entrada no estoque e a despesa de uma vez. Ele só aparece para quem administra estoque e financeiro, e fica para o tutorial Financeiro.
Vou fazer uma requisição, que é a lista do que precisa ser comprado. Clico em Criar requisição e dou o título: Reposição de gás, cobre e capacitor. O destino é o Estoque Principal, porque é pra lá que o material vai quando chegar.
Em vez de procurar um por um, uso o Adicionar itens abaixo do mínimo. Escolho o local, e a lista mostra o déficit de cada material, ou seja, quanto falta para chegar ao mínimo. Adiciono todos à requisição.
As quantidades entram em branco, porque quem decide quanto comprar é você. Peço dez quilos de érre quatrocentos e dez á, vinte metros de tubo de cobre de três oitavos e seis capacitores.
Salvo, e a requisição está criada.""",
9: """Com a requisição criada, o próximo passo é pedir preço aos fornecedores. Clico nela e abre a tela da requisição, com três blocos: Materiais, Cotações e Ordens de compra.
Em Cotações, clico em Nova cotação e escolho o fornecedor, a Ventura Gás e Tubos. Digito o valor de cada material: noventa e quatro reais o quilo do gás, vinte e nove reais e cinquenta centavos o metro do tubo e trinta e nove reais o capacitor. A Dominex soma o total.
Salvo, e faço o mesmo com a Cobre Sul e com a Polar, cada uma com os seus preços.
Cada cartão mostra quantos materiais têm preço e o total. O selo Mais barata marca o menor total, mas o melhor preço de cada material pode estar em outro fornecedor.
Por isso a escolha é por material. Em Materiais, o campo Fornecedor escolhido lista as opções em ordem de preço. O gás fica com a Ventura, o tubo com a Cobre Sul e o capacitor com a Polar.
Uma dica: até aqui o estoque não mudou. Ele só sobe quando o material chega e você registra o recebimento.""",
10: """Com o fornecedor escolhido em cada material, é hora de gerar as ordens de compra. Clico em Gerar ordens de compra, e a Dominex cria uma por fornecedor, todas em Rascunho.
Na ordem da Ventura, clico em Marcar como enviada, e o selo muda para Enviada. No menu também aparece o Baixar pê-dê-éfe, que gera o documento da ordem para você mandar ao fornecedor.
Chegou o gás. Em Registrar recebimento, vejo o que foi pedido, o que já chegou e o que está pendente. Como veio tudo, clico em Receber tudo e confirmo.
O tubo da Cobre Sul chegou pela metade: dez metros dos vinte. Informo só o que chegou agora. O resto continua pendente, e a ordem fica como Recebida parcial.
A ordem da Polar continua em rascunho, esperando o envio.
De volta ao Estoque Atual, o gás subiu para dezesseis vírgula cinco, e o tubo para vinte e dois. O cartão de estoque baixo caiu para um: só o capacitor, que ainda não chegou.""",
11: """E quando o fornecedor manda a nota fiscal em xis-eme-éle? Clico em Importar xis-eme-éle da ene-éfe-é e escolho o arquivo da nota. A Dominex lê tudo na hora.
Primeiro aparece o fornecedor, a Gelo Norte Componentes, com o selo Vinculado, porque o CNPJ da nota já está no cadastro. Se fosse um fornecedor novo, a Dominex cadastraria junto.
Em Produtos da nota, cada item traz o nome, a quantidade, a unidade e o custo. O Destino no estoque diz onde cada um entra. O capacitor a Dominex reconheceu pelo nome e ligou ao que a gente cadastrou. O contator de vinte e cinco ampères e o filtro secador são novos e vão ser criados.
Confirmo a entrada. Três itens importados, dois deles novos.
A nota dá entrada no estoque principal e cadastra o fornecedor se ele for novo. Para levar algum item pra van, é só transferir depois. E se a mesma nota for importada de novo, a Dominex avisa antes de repetir a entrada.""",
12: """Agora, a conferência: o inventário, que é a contagem física do estoque. Na aba Inventários, clico em Novo inventário. A primeira etapa é Locais, e eu marco o Estoque Principal.
Em Escopo, posso contar tudo, só alguns grupos ou itens específicos. Hoje vou por grupo: Gases e Elétrica.
Na última etapa, vejo o resumo e escrevo uma observação: Contagem do mês. Clico em Criar inventário.
A lista mostra o que era esperado de cada material, o saldo na hora em que criei o inventário, e o campo Contado fica por minha conta.
Agora é só contar o que está na prateleira e digitar. A contagem salva sozinha quando eu saio do campo, e a diferença aparece na hora. Contei dezesseis quilos de érre quatrocentos e dez á, seis de érre trinta e dois, oito capacitores de trinta e cinco microfarads e treze de quarenta microfarads. Dois itens deram diferença.
Na aba Divergências ficam só os dois itens que não bateram, com o valor de cada diferença.
Antes de finalizar, confira essa aba: ao finalizar, o estoque é ajustado para o valor contado e não volta atrás. Clico em Finalizar, e os dois itens são ajustados.
O inventário fica Finalizado, e os ajustes entram no cárdex. Uma dica: evite movimentar o estoque enquanto conta.""",
13: """Terminada a contagem, dá para voltar no tempo com a Posição de Estoque. Ela mostra o saldo de cada material em cada local, com o valor pelo custo, a projeção de venda e o total no fim. Por padrão, é a posição de agora.
Mas posso escolher qualquer dia no calendário. Escolho o de um mês atrás, e os saldos e os valores se recalculam sozinhos: é como o estoque estava naquele dia.
A busca ajuda a seguir um material só, e o Exportar leva a posição para pê-dê-éfe ou ékisel. Uma dica: o valor usa o custo cadastrado hoje, e não o custo daquele dia.""",
14: """E para saber quanto a empresa paga pelos materiais, o Relatório. O Total comprado soma as compras do período, e abrindo o cartão dá para ver o tíquete médio de cada compra.
Total vendido e Lucro bruto dependem das vendas do pê-dê-vê. A Projeção de lucro é uma estimativa, feita com o preço de venda cadastrado.
Aqui embaixo, a Evolução do preço de compra compara cada material com a compra anterior dele, e mostra as maiores altas e quedas.
No érre quatrocentos e dez á, o último preço foi noventa e quatro reais o quilo, o menor foi oitenta e seis reais, e o maior, noventa e quatro. A média é ponderada pela quantidade comprada, e a variação compara o último preço com o da compra anterior.
Na lista por material, a coluna Média paga mostra o que a empresa pagou em média. Clicando na linha do érre quatrocentos e dez á, vejo cada compra: data, fornecedor, ordem de compra, quantidade e preço.
Uma dica: a média paga considera as compras recebidas por ordem de compra e as compras diretas. As entradas rápidas e as notas importadas não entram.""",
15: """Pronto! Recapitulando: você cadastrou um material, com grupo, custo, preço de venda e mínimo por local, e registrou entradas e saídas, com o alerta de estoque baixo.
Criou a van zero um, transferiu material para ela, escolheu quem enxerga o local e acompanhou tudo no cárdex.
Para repor, fez a requisição, pediu cotações, escolheu o fornecedor de cada material e recebeu pelas ordens de compra. A nota fiscal em xis-eme-éle também deu entrada. A compra direta fica para o tutorial Financeiro.
Fechou com o inventário, a posição numa data e o relatório de compras e de preço.
Com o estoque em ordem, o próximo passo é montar orçamentos e propostas para os seus clientes. Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "A tela e as seis abas.",
           2: "Cadastrar um material.",
           3: "Entrada, saída e estoque baixo.",
           4: "Locais e grupos de material.",
           5: "Transferir para a van.",
           6: "Quem enxerga cada local.",
           7: "Todo movimento no cárdex.",
           8: "Requisição de compra.",
           9: "Cotações e fornecedor por material.",
           10: "Ordem de compra e recebimento.",
           11: "A nota fiscal em xis-eme-éle.",
           12: "Contar e ajustar.",
           13: "O saldo numa data.",
           14: "Compras, média paga e preço.",
           15: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "Estoque",
           2: "Estoque",
           3: "Estoque",
           4: "Locais",
           5: "Locais",
           6: "Locais",
           7: "Histórico",
           8: "Compras",
           9: "Compras",
           10: "Compras",
           11: "Nota fiscal",
           12: "Inventário",
           13: "Posição",
           14: "Relatório",
           15: "Resumo"}

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
