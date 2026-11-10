# Texto enviado ao ElevenLabs (eleven_v4, voz Kaik Barreto) por capítulo do T6 "Caixa: abrir, fechar e o cofre".
# Gerado do roteiro.md (coluna Fala): cada linha do texto é uma linha da tabela Tela × Fala.
# Trocas de pronúncia em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   DRE -> "dê-érri-ê" | EcoTray -> "Ecotrêi"
CAPS = {
0: """Oi! Neste tutorial a gente vai cuidar do dinheiro do dia na Recicla Vale Metais.
No ferro-velho, quase toda compra de sucata é paga em dinheiro vivo. Se o caixa não bate no fim do dia, ninguém sabe onde foi parar a diferença.
Então a gente vai ver com quanto o caixa abre, com quanto ele fecha, e onde fica o dinheiro da empresa quando não tem caixa aberto.
Tudo isso fica no menu lateral, em Financeiro, Caixa.
Se você ainda não viu o tutorial Balança e impressora, o Ecotrêi, dá uma olhada antes. [pause] Vamos começar pela tela com o caixa fechado.""",
1: """Essa é a tela do caixa logo cedo, antes de abrir. Em Meu Caixa fica o botão Abrir Caixa.
E esse cartão amarelo é o último caixa que eu fechei, o de ontem, com o valor e o horário. Ele serve pra reabrir, se precisar corrigir alguma coisa.
Mais embaixo, o Painel Gerencial mostra os caixas abertos no dia. Por enquanto, nenhum.
Quem não tem acesso aos caixas da equipe toda vê, no lugar disso, um cartão grande escrito Caixa Fechado, com o mesmo botão.
Repara o que acontece se alguém tenta lançar uma compra agora: o sistema avisa Abra o caixa antes de realizar compras e volta pra cá.
Uma dica: venda, despesa e receita também precisam de caixa aberto. Então o dia começa por aqui: vamos abrir.""",
2: """Clico em Abrir Caixa. A janela pede o saldo inicial em dinheiro: quanto dinheiro vivo tem na gaveta agora.
O campo vem vazio de propósito. Embaixo tem uma dica: mil duzentos e cinquenta reais foi o que sobrou no último caixa.
Uma dica: esse número é só uma referência. Conte o dinheiro da gaveta e digite o que contou. Copiar a dica sem contar é o motivo mais comum de diferença no fechamento.
Hoje cedo eu pus mais troco na gaveta e contei mil e quinhentos reais. É isso que eu digito.
Abrir Caixa. Pronto: o caixa abriu com mil e quinhentos reais.""",
3: """Lá embaixo, no Histórico de Transações, o sistema lançou sozinho a linha Abertura do Caixa, com os mil e quinhentos. Isso acontece sempre que o caixa abre com dinheiro.
Agora imagina um dia em que a Recicla Vale só entrega carga pros clientes, e eles pagam por Pix ou transferência. Nenhum dinheiro vivo passa pela gaveta.
Aí faz sentido abrir o caixa com zero. É só deixar o campo vazio ou digitar zero.
Agora, o caixa do Marcos, o balanceiro. No Início, o administrador abre caixa pra outra pessoa: em Abrir para o usuário, escolho o Marcos.
Repara no aviso amarelo: com o campo vazio, o caixa abre sem dinheiro em espécie. Uma dica: aberto com zero, o caixa não ganha a linha de abertura no histórico. Não está faltando nada.
Mas o Marcos paga os fornecedores em dinheiro na balança. Então o caixa dele precisa de dinheiro, e quem diz quanto dá é o cofre.""",
4: """Embaixo do campo, o sistema mostra o disponível no cofre: dezessete mil reais, de dezoito mil e quinhentos no total. Mil e quinhentos estão dentro de caixas abertos.
O cofre é todo o dinheiro vivo da empresa: dezoito mil e quinhentos reais. No sistema, ele também aparece como Conta Dinheiro.
Quando eu abri o meu caixa com mil e quinhentos, esse dinheiro foi pra minha gaveta. Ele continua sendo da empresa, só mudou de lugar.
O que não está em nenhum caixa aberto é o disponível no cofre: dezessete mil. É desse dinheiro que sai um caixa novo.
Por isso o caixa só abre com o dinheiro que já está registrado no cofre. E quando ele fecha, o dinheiro contado volta pro cofre. Assim, todo real tem um lugar.
E se alguém tentar abrir com mais do que tem? É o que a gente vê agora.""",
5: """Hoje o Marcos tem compra grande na balança e quer começar com vinte mil reais. Digito vinte mil no saldo de abertura.
Clico em Abrir Caixa, e aparece o aviso: Saldo insuficiente em dinheiro.
O caixa só abre com o dinheiro registrado no cofre. A gente tentou vinte mil, e o disponível é dezessete mil, porque mil e quinhentos já estão no meu caixa.
Tem duas saídas. Usar disponível preenche o campo com os dezessete mil do cofre.
E Ajustar saldo do dinheiro é pra quando tem dinheiro na empresa que nunca foi lançado. Você corrige o cofre, e o caixa abre sozinho com o valor que tentou.
Uma dica: se o aviso aparece e o dinheiro está na sua mão, conte tudo o que a empresa tem em espécie e ajuste o cofre uma vez só.
Aqui não é o caso: o Marcos começa com os dezessete mil, e o resto vem do banco mais tarde. Usar disponível, Abrir Caixa, e pronto: o caixa do Marcos está aberto.""",
6: """Com o caixa aberto, a tela tem dois cartões no topo. O primeiro é o Dinheiro em Caixa: o dinheiro vivo deste caixa, os meus mil e quinhentos.
Embaixo, a hora em que ele abriu e o Dinheiro total da empresa, que é o cofre: dezoito mil e quinhentos.
Clicando nele, o sistema abre o cofre.
A barra mostra onde está cada real: mil e quinhentos no meu caixa, dezessete mil no caixa do Marcos, e nada sobrando no cofre.
De volta ao caixa, o segundo cartão é o Saldo Bancário: o dinheiro das contas do banco, onde caem o Pix e a transferência. Os botões dele a gente usa daqui a pouco.
No olhinho, você esconde o valor da tela, e ele vira pontinhos.
Uma dica: se alguém da equipe vê esses pontinhos sem ter clicado no olho, não é erro. É a permissão Ver Dinheiro Total em Caixa, desligada pra essa pessoa em Usuários e Permissões.""",
7: """Repara nas abas lá em cima: uma pro meu caixa e outra pro do Marcos. Cada operador tem o seu.
Isso é o multi-caixa. Cada um abre, opera e fecha o próprio caixa. Se faltar dinheiro numa gaveta, você sabe de quem é.
No ponto de interrogação, o sistema explica as regras. A principal: compra, venda, despesa e receita em dinheiro mexem só no caixa selecionado.
Já o saldo do banco e o saldo de clientes e fornecedores são da empresa toda.
Na aba Início fica o Painel Gerencial, com o resumo do dia somando os caixas. Daqui também sai o Abrir Caixa pra outro usuário, como eu fiz com o Marcos.
E se a empresa preferir um caixa só pra todo mundo, dá pra desligar em Configurações, Usabilidade, na opção Multi-Caixas.""",
8: """Pra ver o caixa do Marcos, é só clicar na aba dele. Aqui estão os dezessete mil da gaveta dele e a hora em que abriu.
O que eu lançar com essa aba aberta vai pro caixa do Marcos, não pro meu. Então, antes de lançar no caixa de outra pessoa, confira a aba.
Quem pode ver e operar o caixa dos outros? O administrador e quem tem a permissão Ver e Operar Todos os Caixas.
Já o Marcos, no computador da balança, vê só o caixa dele, sem as abas.
E todo caixa fechado, de todo operador, fica guardado no Histórico do Caixa, com o nome de quem abriu.""",
9: """Lembra que o Marcos queria vinte mil e abriu com dezessete? Os três mil que faltam vêm do banco.
Pôr dinheiro na gaveta durante o dia é o que muita gente chama de suprimento. Quando ele vem do banco, aqui no sistema é um Saque.
A sangria é o caminho contrário: o dinheiro sai de um caixa, ou do cofre, e vai pro banco.
Nos dois casos não é receita nem despesa: é o mesmo dinheiro da empresa mudando de lugar. Só a tarifa do banco é despesa de verdade.
No botão do saque, a janela abre com a opção Saque marcada.
A conta de origem é a principal do banco. No destino, eu escolho o caixa do Marcos.
Valor do saque: três mil reais.
O banco cobrou tarifa? Aqui, sim: seis reais e cinquenta.
Embaixo, os efeitos: a conta do banco diminui três mil e seis reais e cinquenta, e o caixa do Marcos aumenta três mil.
Uma dica: nunca lance um saque como Nova Receita. Ele entraria no relatório como se a empresa tivesse faturado mais. A tarifa o sistema já lança separada, como despesa.
Confirmar Saque. Pronto: o caixa do Marcos chegou nos vinte mil.
Na opção Sangria, você escolhe de onde sai o dinheiro, o cofre ou um caixa aberto, e a conta do banco que recebe.
Já a Nova Movimentação Bancária é pra entrada ou saída direto no banco, que não vem de pedido. Por exemplo, a tarifa mensal da conta.
Saída, a descrição, trinta e nove e noventa, e a categoria Tarifas bancárias.
Salvar. Essa sim entra no resultado como despesa.""",
10: """Fim do dia. No meu caixa entrou a venda pra Aços Quiririm, por transferência, e saíram duas compras em dinheiro: a latinha da Aparecida e o ferro misto do Valdir.
Antes de liberar o Fechar Caixa, o sistema confere se ficou algum pedido não finalizado neste caixa.
Se ficou, o botão aparece com um cadeado, e passando o mouse ele mostra qual pedido falta finalizar ou cancelar. Aqui está tudo finalizado.
Clico em Fechar Caixa. A janela faz a conta do dia.
Abriu com mil e quinhentos, e saíram quatrocentos e noventa e dois e noventa em compras, em dinheiro. A venda e a tarifa foram pelo banco, então não mexem na gaveta.
Restante em caixa: mil e sete reais e dez centavos. É o que o sistema espera achar na gaveta.
Agora vem a conferência. De um lado, o que o sistema espera. Do outro, o que você conta na gaveta.
Se os dois batem, o caixa fecha sem diferença. Se não batem, a diferença fica registrada, pra mais ou pra menos.
O Valor de Fechamento já vem com o esperado. Mesmo assim, conte a gaveta e digite o que contou.
Contei mil e sete e dez. Bateu, então não aparece diferença.
Se não batesse, a diferença apareceria em amarelo, com a chave Registrar diferença no dê-érri-ê. Ela decide se a falta ou a sobra entra no resultado da empresa. O cofre fica sempre com o valor que você contou.
Uma dica: o campo aceita valor negativo. É pro dia em que saiu mais dinheiro do que tinha, e alguém completou com dinheiro de fora. O sistema não impede: ele registra.
Confirmar Fechamento. O dinheiro contado volta pro cofre, e o sistema oferece imprimir o relatório do fechamento.
Desta vez, não, obrigado. O relatório fica guardado no Histórico do Caixa, pra imprimir quando quiser.""",
11: """Fechei e lembrei de uma compra que ficou sem lançar. O caminho é reabrir o caixa.
Olha o cartão amarelo de novo: agora ele mostra o caixa que eu acabei de fechar, com o valor e o horário.
No link reabrir outro caixa aparecem os últimos caixas fechados, de todos os operadores, com o nome de quem abriu.
Dá pra reabrir o caixa de outra pessoa, desde que ela não esteja com outro caixa aberto. Cada operador fica com um caixa aberto por vez.
O meu já vem marcado. Clico em reabrir, e o sistema confirma: o caixa volta exatamente como estava, com tudo que foi lançado nele.
Reabrir Caixa. Pronto: o caixa está aberto de novo. Agora é só lançar o que faltou e fechar outra vez.""",
12: """Recapitulando: a gente viu a tela com o caixa fechado, o cartão amarelo de reabrir, e que sem caixa aberto a compra não sai.
Abriu o caixa com o dinheiro contado, sem copiar a dica, e viu quando faz sentido abrir com zero.
Entendeu o cofre, que é todo o dinheiro vivo da empresa, e o aviso de saldo insuficiente, com as duas saídas.
Conheceu os dois cartões, abriu o caixa do Marcos e viu cada operador com a sua aba.
Fez um saque do banco pro caixa do Marcos, com a tarifa, conheceu a sangria e lançou a tarifa mensal direto no banco.
E fechou o caixa sem diferença, e reabriu pelo cartão amarelo.
No próximo tutorial, a parte que a Recicla Vale faz o dia inteiro: comprar e vender sucata. Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "O caixa fechado.",
           2: "Abrir o caixa.",
           3: "Abrir com zero.",
           4: "O cofre da empresa.",
           5: "Saldo insuficiente.",
           6: "Os dois cartões.",
           7: "Cada um com o seu caixa.",
           8: "O caixa dos outros.",
           9: "Saque e sangria.",
           10: "Fechar o caixa.",
           11: "Reabrir um caixa.",
           12: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "Caixa",
           2: "Abertura",
           3: "Abertura",
           4: "Cofre",
           5: "Cofre",
           6: "Caixa",
           7: "Multi-caixa",
           8: "Multi-caixa",
           9: "Movimentações",
           10: "Fechamento",
           11: "Fechamento",
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
