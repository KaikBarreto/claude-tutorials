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
Embaixo fica a Data e Hora de Abertura, que já vem com a hora de agora. Ela só aparece pra quem tem a permissão de data retroativa, e serve pro dia em que o caixa ficou sem abrir no sistema.
Uma dica: no primeiro caixa da vida da empresa não tem limite. O valor que você digitar é o que inaugura o cofre.
Abrir Caixa. Pronto: o caixa abriu com mil e quinhentos reais.""",
3: """Lá embaixo, no Histórico de Transações, o sistema lançou sozinho a linha Abertura do Caixa, com os mil e quinhentos. Isso acontece sempre que o caixa abre com dinheiro.
E se você digitou o valor errado na abertura? Não precisa fechar e abrir de novo. Nos três pontinhos dessa linha tem o Editar saldo de abertura.
Você informa o valor certo, o Dinheiro em Caixa se ajusta pela diferença, e a mudança fica registrada. Aqui está certo, então eu cancelo.
Nesse histórico dá pra buscar, filtrar e corrigir cada lançamento do dia. Isso a gente vê no tutorial Pedidos e histórico do caixa.
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
Embaixo desse texto tem um link pro tutorial do dinheiro do caixa, que abre em outra aba.
Tem duas saídas. Como o cofre tem saldo, a primeira se chama Usar disponível, e preenche o campo com os dezessete mil do cofre.
E Ajustar saldo do dinheiro é pra quando tem dinheiro na empresa que nunca foi lançado. Você corrige o cofre, e o caixa abre sozinho com o valor que tentou.
Uma dica: se o aviso aparece e o dinheiro está na sua mão, conte tudo o que a empresa tem em espécie e ajuste o cofre uma vez só.
Aqui não é o caso: o Marcos começa com os dezessete mil, e o resto vem do banco mais tarde. Usar disponível, Abrir Caixa, e pronto: o caixa do Marcos está aberto.""",
6: """Agora o contrário. Com o meu caixa e o do Marcos abertos, todo o dinheiro do cofre está dentro de caixas. O disponível é zero, de dezoito mil e quinhentos no total.
Vou abrir um terceiro caixa, o da Juliana, com quinhentos reais de troco. Digito quinhentos e clico em Abrir Caixa.
O aviso é o de antes: tentei quinhentos, e o disponível é zero, porque os dezoito mil e quinhentos já estão nos dois caixas abertos.
Repara no botão. Sem saldo no cofre, ele não é mais o Usar disponível: vira Abrir zerado. E o Ajustar saldo do dinheiro continua pro dinheiro da empresa que nunca foi lançado.
Agora imagina que o cofre ficou negativo, com mil e duzentos reais a menos do que estava registrado. Clico em Abrir Caixa de novo.
Agora o aviso diz que o cofre está negativo em mil e duzentos reais e que não há dinheiro disponível. O botão é o mesmo: Abrir zerado.
Quem pode ajustar contas vê esse texto e o botão Ajustar saldo do dinheiro. Quem não pode vê, no lugar, um recado pedindo ao responsável que ajuste o saldo, ou que abra o caixa zerado.
Clico em Abrir zerado. Ele só preenche o campo com zero e fecha o aviso, e eu ainda clico em Abrir Caixa. E o caixa abre: abrir zerado nunca é barrado pelo cofre, nem com ele negativo.
Uma dica: zerado não tira nada do cofre. Quando entrar dinheiro de verdade nesse caixa, o caminho é o saque do banco, que a gente vê daqui a pouco.""",
7: """Com o caixa aberto, a tela tem dois cartões no topo. O primeiro é o Dinheiro em Caixa: o dinheiro vivo deste caixa, os meus mil e quinhentos.
Embaixo, a hora em que ele abriu e o Dinheiro total da empresa, que é o cofre: dezoito mil e quinhentos.
Clicando nele, o sistema abre o cofre.
A barra mostra onde está cada real: mil e quinhentos no meu caixa, dezessete mil no caixa do Marcos, e nada sobrando no cofre.
De volta ao caixa, o segundo cartão é o Saldo Bancário: o dinheiro das contas do banco, onde caem o Pix e a transferência. Os botões dele a gente usa daqui a pouco.
No olhinho, você esconde o valor da tela, e ele vira pontinhos.
Uma dica: se alguém da equipe vê esses pontinhos sem ter clicado no olho, não é erro. É a permissão Ver Dinheiro Total em Caixa, desligada pra essa pessoa em Usuários e Permissões.""",
8: """Repara nas abas lá em cima: uma pro meu caixa e outra pro do Marcos. Cada operador tem o seu.
Isso é o multi-caixa. Cada um abre, opera e fecha o próprio caixa. Se faltar dinheiro numa gaveta, você sabe de quem é.
No ponto de interrogação, o sistema explica as regras. A principal: compra, venda, despesa e receita em dinheiro mexem só no caixa selecionado.
Já o saldo do banco e o saldo de clientes e fornecedores são da empresa toda.
Na aba Início fica o Painel Gerencial, com o resumo do dia somando os caixas. Daqui também sai o Abrir Caixa pra outro usuário, como eu fiz com o Marcos.
E se a empresa preferir um caixa só pra todo mundo, dá pra desligar em Configurações, Usabilidade, na opção Multi-Caixas.
O painel não mostra só hoje. No calendário, eu escolho ontem e vejo os caixas e o resumo daquele dia.
Mais embaixo, as transações do dia com o nome de quem lançou, e os gráficos: quanto foi em dinheiro e quanto foi por Pix, e quanto cada caixa movimentou. E no botão Hoje, eu volto pro dia de hoje.
Dentro de cada caixa tem o Resumo do Caixa Atual: o que comprou, o que vendeu, a projeção de lucro, as receitas e as despesas só deste caixa. O olhinho esconde os valores, se tiver gente por perto.
E esse botão lança um recebimento ou um pagamento no saldo de um cliente ou fornecedor, sem sair do caixa. A janela é a mesma do tutorial Clientes, fornecedores e a ficha do parceiro.""",
9: """Pra ver o caixa do Marcos, é só clicar na aba dele. Aqui estão os dezessete mil da gaveta dele e a hora em que abriu.
O que eu lançar com essa aba aberta vai pro caixa do Marcos, não pro meu. Então, antes de lançar no caixa de outra pessoa, confira a aba.
Quem pode ver e operar o caixa dos outros? O administrador e quem tem a permissão Ver e Operar Todos os Caixas.
Abrir e fechar caixa também são permissões. Quem não tem vê o botão com um cadeado.
Já o Marcos, no computador da balança, vê só o caixa dele, sem as abas.
E todo caixa fechado, de todo operador, fica guardado no Histórico do Caixa, com o nome de quem abriu.""",
10: """Lembra que o Marcos queria vinte mil e abriu com dezessete? Os três mil que faltam vêm do banco.
Pôr dinheiro na gaveta durante o dia é o que muita gente chama de suprimento. Quando ele vem do banco, aqui no sistema é um Saque.
A sangria é o caminho contrário: o dinheiro sai de um caixa, ou do cofre, e vai pro banco.
Nos dois casos não é receita nem despesa: é o mesmo dinheiro da empresa mudando de lugar. Só a tarifa do banco é despesa de verdade.
No botão do saque, a janela abre com a opção Saque marcada.
A conta de origem é a principal do banco. No destino, eu escolho o caixa do Marcos.
Valor do saque: três mil reais, o que falta pro Marcos.
O banco cobrou tarifa? Aqui, sim: seis reais e cinquenta.
Embaixo, os efeitos: a conta do banco diminui três mil e seis reais e cinquenta, e o caixa do Marcos aumenta três mil.
Uma dica: nunca lance um saque como Nova Receita. Ele entraria no relatório como se a empresa tivesse faturado mais. A tarifa o sistema já lança separada, como despesa.
Confirmar Saque. Pronto: o caixa do Marcos chegou nos vinte mil.
Uma dica: se o destino for o cofre e tiver caixa aberto, o sistema pergunta antes de gravar, porque esse dinheiro não aparece na gaveta de ninguém.
E esqueceu de lançar o saque de ontem? Quem tem a permissão de data retroativa escolhe o dia aqui. A sangria de verdade, a gente faz no fim do dia.
Já a Nova Movimentação Bancária é pra entrada ou saída direto no banco, que não vem de pedido. Por exemplo, a tarifa mensal da conta.
Saída, a descrição, trinta e nove e noventa, e a categoria Tarifas.
Salvar. Essa sim entra no resultado como despesa.""",
11: """Nem tudo que sai do caixa é compra de sucata. O gás da empilhadeira, o almoço da equipe, um conserto: isso é despesa, e aqui no caixa ela tem botão próprio.
Nova Despesa. A janela pergunta o que é, de onde sai o dinheiro, e guarda os detalhes mais embaixo.
Começo pela descrição, e o sistema reconhece: essa despesa já foi lançada outras vezes. Ele mostra o padrão encontrado, com a categoria, o centro de custo e a forma de pagamento.
Clico em Preencher e os campos vêm prontos, inclusive o nome completo. Se não era isso, tem o Desfazer preenchimento logo embaixo. Agora o valor: cinquenta reais.
Em Pagou com, você diz de onde saiu o dinheiro. Dinheiro, Caixa, sai da gaveta deste caixa. Se você escolher uma conta do banco, a gaveta não muda.
Em Mais detalhes dá pra escrever uma observação e anexar o comprovante. Parcelar e repetir a gente vê no tutorial Contas a Pagar e Receber.
Confirmar Despesa. Repara no Dinheiro em Caixa: caiu de mil e quinhentos pra mil quatrocentos e cinquenta. E a despesa já está no histórico.
A Nova Receita é o mesmo caminho, pro dinheiro que entra e não é venda de sucata. Aqui, o aluguel de uma caçamba: cento e vinte reais, recebidos por Pix na conta do banco.
Confirmar Receita. Como caiu no banco, a gaveta não mudou.
Uma dica: receita é dinheiro novo que a empresa ganhou. Troco que vem do banco pra gaveta não é receita, é saque, como a gente acabou de ver.""",
12: """Fim da tarde, e o caixa do Marcos ainda está com muito dinheiro vivo. Dinheiro parado na gaveta é risco. A saída é uma sangria.
Em Saque, Sangria, opção Sangria. A origem pode ser o cofre ou um caixa aberto, cada um com o saldo do lado. Escolho o caixa do Marcos.
O destino é a conta principal, e o valor, cinco mil reais, que o Marcos vai depositar no banco.
Embaixo, os efeitos: o caixa do Marcos diminui cinco mil, e a conta do banco aumenta cinco mil.
Confirmar Sangria. Não é despesa: o dinheiro só trocou a gaveta pelo banco.""",
13: """Fim do dia. No meu caixa entrou a venda pra Aços Quiririm, por transferência, e saíram duas compras em dinheiro, a latinha da Aparecida e o ferro misto do Valdir, mais o gás da empilhadeira que lancei de manhã.
Antes de liberar o Fechar Caixa, o sistema confere se ficou algum pedido não finalizado neste caixa.
Se ficou, olha o painel Pedidos Não Finalizados. Aqui, uma compra do Valdir pela metade.
Enquanto ela estiver aí, o Fechar Caixa fica com cadeado, e passando o mouse ele diz qual pedido está travando.
Clicando no pedido, o sistema abre ele pra você finalizar ou descartar. Resolvido isso, o cadeado some. No nosso dia está tudo finalizado, e o botão está livre.
Clico em Fechar Caixa. A janela faz a conta do dia.
Abriu com mil e quinhentos, e saíram quatrocentos e noventa e dois e noventa em compras e cinquenta reais de despesa, em dinheiro. A venda, a tarifa e a receita foram pelo banco, então não mexem na gaveta.
Restante em caixa: novecentos e cinquenta e sete reais e dez centavos. É o que o sistema espera achar na gaveta.
Cada cartão separa o que foi em dinheiro do que foi por Pix ou transferência. Só a coluna do dinheiro mexe na gaveta: as compras e o gás da empilhadeira.
Abrindo a Projeção de Lucro, você confere o dia material por material: quanto comprou e quanto vendeu de cada um.
Agora vem a conferência. De um lado, o que o sistema espera. Do outro, o que você conta na gaveta.
Se os dois batem, o caixa fecha sem diferença. Se não batem, a diferença fica registrada, pra mais ou pra menos.
O Valor de Fechamento já vem com o esperado. Mesmo assim, conte a gaveta e digite o que contou.
Olha o que acontece se eu contar novecentos e cinquenta: o sistema mostra a diferença, sete reais e dez centavos a menos.
A chave Registrar diferença no dê-érri-ê decide se essa falta entra no resultado como prejuízo. Se fosse sobra, entraria como ganho. O cofre fica sempre com o valor que você contou.
Contei de novo, e tinha uma nota dobrada: novecentos e cinquenta e sete e dez. Bateu, então não aparece diferença.
Uma dica: o campo aceita valor negativo. É pro dia em que saiu mais dinheiro do que tinha, e alguém completou com dinheiro de fora. O sistema não impede: ele registra.
Com a mesma permissão de data retroativa, dá pra fechar com a data e a hora em que o caixa parou de verdade.
Confirmar Fechamento. O dinheiro contado volta pro cofre, e o sistema oferece imprimir o relatório do fechamento.
Desta vez, não, obrigado. O relatório fica guardado no Histórico do Caixa, pra imprimir quando quiser.""",
14: """Fechei e lembrei de uma compra que ficou sem lançar. O caminho é reabrir o caixa.
Reabrir é pra lançar o que ficou de fora. Pra corrigir uma compra ou venda de um caixa já fechado, não precisa: a edição do pedido deixa manter o caixa original ou escolher um caixa aberto. Isso está no tutorial Pedidos e histórico do caixa.
Olha o cartão amarelo de novo: agora ele mostra o caixa que eu acabei de fechar, com o valor e o horário.
No link reabrir outro caixa aparecem os últimos caixas fechados, de todos os operadores, com o nome de quem abriu.
Dá pra reabrir o caixa de outra pessoa, desde que ela não esteja com outro caixa aberto. Cada operador fica com um caixa aberto por vez.
O meu já vem marcado. Clico em reabrir, e o sistema confirma: o caixa volta exatamente como estava, com tudo que foi lançado nele.
Reabrir Caixa. Pronto: o caixa está aberto de novo. Agora é só lançar o que faltou e fechar outra vez.""",
15: """Recapitulando: a gente viu a tela com o caixa fechado, o cartão amarelo de reabrir, e que sem caixa aberto a compra não sai.
Abriu o caixa com o dinheiro contado, sem copiar a dica, e viu quando faz sentido abrir com zero.
Entendeu o cofre, que é todo o dinheiro vivo da empresa, o aviso de saldo insuficiente com as duas saídas, e que abrir zerado nunca é barrado, nem com o cofre negativo.
Conheceu os dois cartões, abriu o caixa do Marcos, viu cada operador com a sua aba e o painel do dia.
Lançou uma despesa em dinheiro e uma receita no banco, com o preenchimento que o sistema sugere.
Fez um saque do banco pro caixa do Marcos, com a tarifa, lançou a tarifa mensal direto no banco, e no fim do dia fez a sangria do caixa dele pro banco.
Viu a diferença aparecer no fechamento, antes de acertar a contagem.
E fechou o caixa batendo com a contagem, e reabriu pelo cartão amarelo.
No próximo tutorial, a parte que a Recicla Vale faz o dia inteiro: comprar e vender sucata. Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "O caixa fechado.",
           2: "Abrir o caixa.",
           3: "Abrir com zero.",
           4: "O cofre da empresa.",
           5: "Saldo insuficiente.",
           6: "Cofre zerado ou negativo.",
           7: "Os dois cartões.",
           8: "Cada um com o seu caixa.",
           9: "O caixa dos outros.",
           10: "Saque e sangria.",
           11: "Despesa e receita do dia.",
           12: "Sangria no fim do dia.",
           13: "Fechar o caixa.",
           14: "Reabrir um caixa.",
           15: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "Caixa",
           2: "Abertura",
           3: "Abertura",
           4: "Cofre",
           5: "Cofre",
           6: "Cofre",
           7: "Caixa",
           8: "Multi-caixa",
           9: "Multi-caixa",
           10: "Movimentações",
           11: "Movimentações",
           12: "Movimentações",
           13: "Fechamento",
           14: "Fechamento",
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
