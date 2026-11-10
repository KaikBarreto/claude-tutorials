# Texto para o ElevenLabs (eleven_v4, voz Kaik Barreto) por capítulo do T7 "Comprar e vender sucata".
# Gerado do roteiro.md (coluna Fala): cada linha do texto é uma linha da tabela Tela × Fala.
# Trocas de pronúncia em relação ao roteiro (a legenda segue o roteiro, ver config_narracao.json):
#   Ctrl+K -> "contról-cá" | Shift+C -> "xífti-cê" | Shift+V -> "xífti-vê" | EcoTray -> "Ecotrêi" | PDF -> "pê-dê-éfe" | Tara/Imp. -> "tara-ímp" | AO VIVO -> "ao vivo"
# A voz não é gerada agora: revisão geral e ensaio gravado antes (PRODUCAO.md, "Fila").
CAPS = {
0: """Oi! Neste tutorial a gente vai fazer o que a Recicla Vale Metais faz o dia inteiro: pesar, comprar, pagar e imprimir o comprovante. E depois vender.
A sucata chega no portão e vai pra balança. Daí o peso tem que virar valor certo e pagamento na hora, sem anotar nada no papel.
Se você ainda não viu o tutorial Caixa: abrir, fechar e o cofre, dá uma olhada antes. É do caixa aberto que saem as compras e as vendas. [pause] Vamos lá.""",
1: """Tudo começa no caixa. No menu, Financeiro, Caixa. Com o caixa aberto, aparecem os botões Nova Compra e Nova Venda.
Clicando em Nova Compra, a tela abre já ligada ao seu caixa. É o selo aqui em cima.
Também dá pra ir pelo teclado. xífti-cê abre a compra, e xífti-vê abre a venda.
E o contról-cá abre a busca em qualquer tela. Em Ações Rápidas estão a Nova Compra e a Nova Venda.
Na tela da compra, em cima ficam o fornecedor e a tabela de preços. À esquerda, o cartão da pesagem, por onde entra cada material. À direita, os itens do pedido. E embaixo, o total e o botão Finalizar.""",
2: """Primeiro, quem está vendendo pra gente. Clicando no fornecedor, abre a lista, e a primeira opção é Não informado.
Ela serve pro pedido avulso, de quem passou uma vez e não quer cadastro. O estoque e o caixa mexem do mesmo jeito.
Só que esse pedido não entra no histórico nem no portal de ninguém. Uma dica: com Não informado, o pagamento não pode ir pro saldo, que é o fiado. Pra isso, o pedido precisa de um fornecedor.
Repara que alguns nomes têm um aviso com número. Ele mostra o que falta no cadastro: no Valdir, o CPF e o endereço. É só um lembrete, e não trava o pedido.
O Valdir não tem telefone, e isso não aparece aqui porque o cadastro dele está marcado com Não possui telefone. Uma dica: quando a pessoa não tem telefone mesmo, marque essa opção em Editar, em vez de inventar um número.
E o alfinete do lado fixa um fornecedor como padrão, pra ele já vir escolhido nos próximos pedidos.
Hoje chegou um carroceiro novo, o Zé Moreira. Na busca, ninguém. Então a gente cadastra ele agora.""",
3: """Sem sair da compra, é só clicar no mais. Abre o mesmo cadastro da tela de Clientes e Fornecedores.
O único campo obrigatório é o nome: José Carlos Moreira. No apelido, Zé Moreira, que é como o pátio chama ele. E o telefone.
A chave Pix dele é o telefone. Aqui também dá pra escolher a tabela de preços do fornecedor e marcar se ele também é cliente.
Salvar. Pronto: o Zé já vem escolhido no pedido. O CPF e o endereço, você completa depois, com calma, na tela de Clientes e Fornecedores.""",
4: """Agora o preço. Do lado do fornecedor fica a tabela de preços do pedido. Ela vem do cadastro do fornecedor, e quando ele não tem uma, vem a principal, a da estrela.
Quando você escolhe o material, o sistema procura o preço nesta ordem. Primeiro, o preço especial combinado com aquele fornecedor. Depois, a tabela do pedido. E por último, o preço do próprio material.
Uma dica: a tela sempre avisa quando valeu um preço especial ou o da tabela. E o preço é só uma sugestão: dá pra mudar na hora.
O Zé é novo e está na tabela principal, então vale o preço de cada material. E escolha sempre o fornecedor antes dos materiais, porque o preço entra na hora em que você escolhe o material.""",
5: """Agora o primeiro material: o cobre misto do Zé. O preço veio do cadastro do material: trinta e seis reais o quilo. E repara no peso: doze quilos e quatrocentos, direto da balança.
Quem traz esse peso é o Ecotrêi, o programa que fica aberto no computador, ligado na balança. O selo ao vivo quer dizer que o peso está chegando agora.
O botão azul dentro do campo puxa o peso de novo, quando você precisar. A leitura da balança faz parte do módulo de balança, que depende do plano contratado. Sem ele, é só digitar o peso.
Embaixo, o estoque disponível desse material e o valor do item: quatrocentos e quarenta e seis reais e quarenta. Incluir Item, e o cobre entra na lista.
Agora a latinha, em três sacos de ráfia: vinte e um quilos e seiscentos. Cada saco pesa duzentos gramas. Então, no campo tara-ímp, vai zero vírgula seis.
A balança nunca preenche esse campo sozinha: a tara é você que informa. O valor sai pelo peso sem os sacos: vinte e um quilos, a seis e vinte, dá cento e trinta reais e vinte. Incluir Item.""",
6: """Antes de seguir, três palavras do pátio. Tara é o peso do que não é material, como o saco, o tambor ou a caçamba. Impureza é a sujeira que vem junto: terra, borracha, plástico.
E o peso líquido é o que sobra: o bruto, menos a tara, menos a impureza. É pelo líquido que o material entra no estoque.
E quando a sucata vem numa carroça ou num caminhão, tem a dupla pesagem. Pesa cheio, descarrega e pesa vazio. A diferença é a carga.
O ferro do Zé veio na carroça. Escolho o ferro misto e clico em Pesagem avançada, logo embaixo do peso.
Carroça cheia na balança: primeira pesagem, quatrocentos e doze quilos. Carroça vazia: segunda pesagem, noventa e seis. O peso bruto sai sozinho: trezentos e dezesseis quilos.
O ferro tem um pouco de terra, e o Rafael combinou três por cento de impureza. A tela converte: nove vírgula quarenta e oito quilos. O líquido fica trezentos e seis vírgula cinquenta e dois quilos.
O campo Tara fica pra embalagem, e a impureza também pode ir em quilos, na chave do lado. O valor estimado já vem pelo líquido: duzentos e vinte e nove reais e oitenta e nove.
Aqui você escolhe o que sai no comprovante. No Completo, o Zé vê as duas pesagens. Motorista e placa ficam pra quando vem caminhão. Confirmar, e o item já entra no pedido.
Uma dica: o estoque recebe o líquido. Pesou trezentos e dezesseis quilos, e entram no estoque trezentos e seis vírgula cinquenta e dois. Não é erro: é a impureza que você informou.""",
7: """O Zé trouxe mais dois sacos de latinha: dezoito quilos e quatrocentos, com quatrocentos gramas de tara. Agora a latinha está duas vezes na lista.
Quando o mesmo material aparece mais de uma vez, surge o botão de mesclar. A janela mostra cada pesagem e o total: quarenta quilos, com um quilo de tara, a seis e vinte o quilo.
Mesclar Todas. Os pesos e as taras se somam, o valor total continua o mesmo, e o comprovante sai com uma linha por material.
E se precisar conferir as pesagens separadas, esse botão desfaz a mescla e devolve cada uma como era.""",
8: """Agora a conferência. O Rafael combinou com o Zé fechar o ferro em duzentos e vinte e cinco reais. Pelo menu da linha, a pesagem avançada do ferro abre de novo, do jeito que estava.
Em vez de fazer a conta, eu digito o valor final: duzentos e vinte e cinco, vírgula, zero zero. O desconto se calcula sozinho: quatro reais e oitenta e nove.
Uma dica: em qualquer campo de valor, os centavos vêm depois da vírgula. O campo apaga o ponto, então zero ponto setenta e cinco vira setenta e cinco reais. Digite com calma e confira.
Confirmar. O ferro fechou em duzentos e vinte e cinco, e o total da compra ficou novecentos e treze reais e vinte.
Clicando na linha, abre o detalhe da pesagem: as duas pesagens, o bruto, a impureza e o desconto. É assim que você confere antes de finalizar.
E se o combinado for o valor do pedido inteiro, o lápis do lado deixa digitar o total fechado. A tela continua mostrando embaixo o valor calculado, pra conferência.""",
9: """Conferido, é hora de pagar. Finalizar abre o pagamento, com o resumo do pedido do lado: o fornecedor, os itens e o total.
São três formas. Dinheiro sai do caixa. Pix ou transferência sai da conta do banco. E o saldo é o fiado: na compra, a Recicla Vale fica devendo ao fornecedor. Na venda, é o cliente que fica devendo.
No Pix, você escolhe de qual conta sai o dinheiro, e a chave Pix do Zé aparece aqui, pra copiar.
No saldo, o resumo mostra como fica a conta com ele: Você deverá a ele.
Mas o Zé quer dinheiro. Em Dinheiro, a tela mostra quanto tem no caixa agora.
Confirmar pagamento. Compra registrada: o material entrou no estoque, o dinheiro saiu do caixa, e a compra já está no histórico do Zé. O cupom sai na impressora, e daqui a pouco a gente vê ele com calma.""",
10: """Agora uma compra maior. Chegou a picape da Auto Peças Vale Forte, com a sucata da oficina.
Repara no aviso: Preço especial aplicado. A oficina tem um preço combinado na bateria: três e quarenta o quilo, e não os três e dez de sempre.
São cento e oitenta e seis quilos de bateria e sessenta e quatro de cobre misto. Total: dois mil novecentos e trinta e seis reais e quarenta.
O dono combinou assim: duzentos em dinheiro, que o motorista leva, dois mil no saldo, e o resto no Pix. Pra isso, eu ligo Múltiplas formas de pagamento.
Escolho as três formas. Duzentos no dinheiro, dois mil no saldo, e o Pix completa a diferença sozinho: setecentos e trinta e seis reais e quarenta. No Pix, escolho a conta.
A soma fecha com o total. Se não fechar, aparece Faltam ou Excesso em vermelho, e o botão de confirmar só libera quando bate.""",
11: """Os dois mil do saldo, a Recicla Vale paga depois. Se for numa data só, é só preencher o Vencimento.
Aqui vão ser duas parcelas. Configurar faturamento divide o saldo em partes, cada uma com a sua data.
Duas parcelas de mil reais. A primeira, eu mudo pra vinte e cinco de novembro, e a segunda fica pra dez de dezembro. A soma fecha com o saldo e fica verde.
Assim, cada parcela tem o seu dia, e você sabe quanto paga e quando.
Aplicar faturamento. Com as parcelas, o vencimento único sai da tela: quem manda nas datas são elas. Uma dica: se o valor do saldo mudar depois, a tela avisa pra refazer as parcelas.
Confirmar pagamento. Dinheiro, Pix e fiado em duas parcelas, tudo numa compra só.""",
12: """Depois de confirmar, a tela pergunta do comprovante. Imprimir direto manda pra impressora térmica, pelo Ecotrêi. E em Visualizar, o comprovante abre em pê-dê-éfe na tela.
Imprimir direto.
Pronto. O cupom sai com o material, o peso, o preço e como foi pago. Esse papel fica com o fornecedor.
E quando o papel vai na mão do motorista, sem mostrar preço? É o Comprovante sem valores, aqui em Opções avançadas, do lado do Finalizar.
O pedido guarda todos os valores. Eles só ficam escondidos no comprovante e no portal. Uma dica: ligue antes de finalizar, porque vale só pra aquele pedido. O próximo já nasce com os valores. A gente usa isso já já, na venda.""",
13: """Agora o outro lado: vender. A tela da venda é igual à da compra. Só que aqui vem o cliente, e o preço que entra é o de venda.
A Fundição Bandeira do Vale leva cento e cinquenta e dois quilos de latão, a trinta e um e noventa. Repara na coluna nova: o lucro de cada item. E embaixo do total, o lucro estimado da venda: seiscentos e sessenta e oito reais e oitenta.
O lucro estimado compara o preço de venda com o preço de compra do material. No latão, são quatro e quarenta por quilo. E o olho do lado esconde o valor, se tiver alguém olhando a tela.
Uma dica: o Estoque Disponível já desconta o que está nesta venda. Tinha duzentos e catorze quilos de latão. Com os cento e cinquenta e dois da venda, a tela mostra sessenta e dois. Não sumiu nada.
Quem busca a carga é o motorista da Fundição. Então, em Opções avançadas, eu ligo o Comprovante sem valores.""",
14: """A Fundição também quer sessenta quilos de cobre mel, mas no sistema tem quarenta e dois. Ao incluir, a tela avisa: faltam dezoito quilos, e propõe de onde puxar.
Na origem, a lista mostra os outros materiais desta unidade que têm saldo. Uma dica: quem tem filial vê aqui também as outras unidades, o que depende do plano contratado, e aí a venda só fecha com internet.
A equipe já limpou parte do cobre misto, que agora é cobre mel. Então eu puxo dezoito quilos do cobre misto.
O cobre mel fica com os sessenta quilos que a venda precisa.
Transferir e Adicionar. A transferência fica agendada e acontece junto com a venda: se alguma parte falhar, nada é gravado. A venda fecha em sete mil setecentos e vinte e dois reais e oitenta, com novecentos e noventa e dois e oitenta de lucro estimado.
Se você preferir não transferir, no Cancelar a tela pergunta, e dá pra Inserir mesmo assim. Aí o estoque fica negativo até você lançar a compra que faltou.
A Fundição paga no Pix. Confirmar pagamento, e venda registrada. Como o Comprovante sem valores está ligado, o comprovante sai só com o material e o peso. É esse papel que o motorista leva.""",
15: """E se a internet cair no meio do dia? A faixa no topo avisa, e o trabalho continua. A compra, a venda e o caixa funcionam sem internet.
Chegou a Dona Cida com a latinha. A balança continua funcionando, porque o Ecotrêi está aqui no computador: catorze quilos e seiscentos. Finalizo em dinheiro, e a compra fica guardada no computador, com um número provisório.
No caixa, ela aparece em Pendências de Sincronização, esperando a internet.
Quando a internet volta, a fila sobe sozinha. Pronto: operação sincronizada, e a compra ganha o número de verdade.
Uma dica: se uma operação ficar com Erro, ela não vai de novo sozinha, pra não lançar em dobro. Use o Tentar novamente, o ícone de atualizar do lado: ele reenvia sem duplicar. Sem esse botão, remova pela lixeira e refaça a operação normalmente.""",
16: """Pronto! Recapitulando: a gente abriu a compra pelo caixa, pelo atalho e pelo contról-cá, viu o Não informado e cadastrou o Zé na hora.
Viu qual preço vale, puxou o peso da balança, descontou a tara e a impureza, e fez a dupla pesagem da carroça.
Mesclou a latinha, fechou o valor do ferro e pagou o Zé em dinheiro. Na compra da oficina, pagou em dinheiro, Pix e fiado em duas parcelas.
Imprimiu o cupom, vendeu com o lucro estimado na tela e o cupom sem valor pro motorista, cobriu o estoque que faltava e comprou sem internet.
No próximo tutorial, o caminhão que chega na balança antes de o preço estar fechado: o Ticket de Pesagem. Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "Onde ficam a compra e a venda.",
           2: "Escolher o fornecedor.",
           3: "Cadastrar o fornecedor na hora.",
           4: "Qual preço vale.",
           5: "O peso da balança.",
           6: "Tara, impureza e dupla pesagem.",
           7: "Mesclar pesagens.",
           8: "Desconto e conferência.",
           9: "Finalizar o pedido.",
           10: "Até três formas de pagamento.",
           11: "Fiado com parcelas.",
           12: "O cupom e o cupom sem valor.",
           13: "A tela de venda.",
           14: "Estoque insuficiente.",
           15: "Sem internet.",
           16: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "Caixa",
           2: "Fornecedor",
           3: "Fornecedor",
           4: "Preço",
           5: "Balança",
           6: "Pesagem",
           7: "Pesagem",
           8: "Valor",
           9: "Pagamento",
           10: "Pagamento",
           11: "Pagamento",
           12: "Comprovante",
           13: "Venda",
           14: "Venda",
           15: "Sem internet",
           16: "Resumo"}

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
