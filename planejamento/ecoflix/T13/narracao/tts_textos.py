# Texto enviado ao ElevenLabs (eleven_v4, voz Kaik Barreto) por capítulo do T13 "Contas a Pagar e Receber".
# Gerado da coluna Fala do roteiro.md: cada linha do texto é uma linha da tabela Tela × Fala.
# Trocas de pronúncia em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   Contas a Pagar/Receber -> "Contas a Pagar e Receber" | Cliente/Fornecedor -> "Cliente ou Fornecedor"
#   DRE -> "dê-érri-ê" | PDF -> "pê-dê-éfe" | Moretti -> "Moréti" (nova, testar no ensaio de pronúncia)
#   Vence em 7 dias -> "Vence em sete dias" (o rótulo do cartão; a legenda volta ao 7) | Próximos 7 dias -> "Próximos sete dias"
#   Juros / multa -> "Juros ou multa" | app 1.60.18: capítulos renumerados (0 a 19), ver plano.md
CAPS = {
0: """Oi! Neste tutorial a gente vai organizar o que a Recicla Vale Metais tem pra pagar e pra receber.
Sabe a conta de luz que só aparece no dia do vencimento? E o cliente que levou a prazo, e ninguém lembra quando paga?
Aqui, tudo entra com data, categoria e de quem é. O que a empresa paga e o que ela recebe, numa tela só.
Se você ainda não viu o tutorial do Estoque, dá uma olhada antes.
A tela fica no menu, em Financeiro, Contas a Pagar e Receber. [pause] Vamos conhecer a tela.""",
1: """Esta é a tela das contas. Ela abre na aba Todas, com o que a empresa paga e o que recebe, juntos.
Na aba A Pagar fica só o que sai, em vermelho, pra não confundir com dinheiro entrando. Na A Receber, só o que entra.
Cada linha é uma conta, com a descrição, a categoria, o vencimento, o valor e o status.
A água de outubro venceu dia cinco e não foi paga. Por isso ela está Vencida, com a data em vermelho.
A energia vence hoje e está Pendente. E o aluguel do galpão foi pago no dia cinco: está Paga.
Parando o mouse em cima do status, o sistema conta mais: há quantos dias a conta venceu, ou quanto já foi pago.
E clicando na linha, abrem os Detalhes da conta: tipo, valor, vencimento, categoria, de quem é, a parcela e a observação.
Parando o mouse em cima do status, o sistema conta mais: há quantos dias a conta venceu, ou quanto já foi pago.
E clicando na linha, abrem os Detalhes da conta: tipo, valor, vencimento, categoria, de quem é, a parcela e a observação.
Pra lançar uma conta nova, o botão é este: Nova conta.""",
2: """Antes da lista, os quatro cartões lá de cima. Eles mostram quanto a empresa deve, quanto tem pra receber e o que está apertando.
O Total a Pagar soma as contas que a empresa ainda deve, mais o que ela deve no saldo, o fiado. O Total a Receber é o contrário: as contas a receber, mais o que devem pra ela no saldo.
Vencidas é o que passou do vencimento e não foi pago, como a água. Vence em sete dias é o que vence de hoje até daqui a sete dias, como a energia.
Esses dois somam só contas, as a pagar e as a receber. O saldo não tem data de vencimento, então fica de fora deles.
Uma dica: os cartões acompanham o que está na lista. Na aba A Pagar, eles mostram o Total a Pagar e o Total pago. Na A Receber, o Total a Receber e o Total recebido. E com busca ou filtro ligado, somam só o que apareceu.""",
3: """E dá pra ver as mesmas contas num calendário. A tela abre na Lista, e do lado fica o Calendário.
No calendário, cada dia mostra as contas que vencem nele. Vermelho é conta a pagar, e verde, a receber.
O triângulo avisa que tem conta vencida naquele dia. É a água, do dia cinco.
Clicando no dia, aparecem as contas dele, já com os botões de pagar e de editar.
Uma dica: o calendário mostra só conta com vencimento. O saldo dos clientes e fornecedores não tem data, então ele fica na Lista, como a própria tela avisa.
Pra voltar, é só clicar em Lista.""",
4: """Agora, lançar uma conta nova. A Hidráulica Moréti vai fazer a manutenção da prensa, com vencimento no dia dezenove. Clico em Nova conta.
O Tipo já vem como A pagar. Se fosse dinheiro entrando, seria A receber.
Na Descrição, o que é a conta: manutenção da prensa enfardadeira. E o Vencimento, dezenove de novembro.
No Valor, três mil quatrocentos e oitenta reais.
A Categoria diz que tipo de gasto é esse. Aqui, Manutenção de máquinas.
Como é conta a pagar, o campo já vem em Fornecedor. É só escolher a Hidráulica Moréti.
O Centro de custo diz qual parte da empresa gastou. A prensa fica no pátio, então, Pátio.
No Pagamento previsto, eu digo de onde esse dinheiro deve sair: da Conta Principal. É só uma previsão, mas na hora de pagar ela já vem sugerida. Do lado aparece a Forma de pagamento: Pix ou transferência, boleto ou cheque. Deixo no Pix.
Criar conta. Pronto: a manutenção entrou na lista, pendente, com a data, a categoria e o fornecedor.
Uma dica: se faltar uma categoria ou um fornecedor, o botão de mais, do lado do campo, cadastra na hora, sem sair daqui. E se você lançar a mesma conta duas vezes, o sistema avisa antes: Conta igual já cadastrada.""",
5: """E quando a conta chega já paga? Ontem, o conserto do pneu da empilhadeira foi pago na hora, por Pix: cento e oitenta reais.
Preencho como qualquer conta: a descrição, a data de ontem, o valor, a categoria e o centro de custo.
No Pagamento previsto, a conta de onde o Pix saiu: a Conta Principal.
Agora o que muda: ligo o Já paguei essa conta. Ele registra o pagamento junto, e a conta já nasce quitada. Na Data do pagamento, ontem.
Criar conta. Ela já entra como Paga, e o dinheiro já saiu da Conta Principal. Nada fica pendente pra lembrar depois.
Numa conta a receber, a opção vira Já recebi essa conta.""",
6: """Tem conta que volta todo mês com os mesmos dados. A internet do escritório, por exemplo. Pra essas, o sistema ajuda a preencher.
Começo pela Descrição: Internet do escritório. Repara que, depois de três letras, aparece um Padrão encontrado.
Ele mostra o que a empresa usou das outras vezes: o fornecedor, a categoria, a conta do banco e a forma de pagamento. E quantas vezes esse padrão já foi usado.
Clico em Preencher. Pronto: categoria, fornecedor e pagamento previsto, tudo de uma vez. E o cursor já pula pro Valor.
Digito duzentos e oitenta e nove e noventa, e ajusto o Vencimento pro dia quinze.
Uma dica: o padrão só preenche campo vazio. O que você já escolheu, ele não troca. E se não era isso, tem o Desfazer preenchimento, logo embaixo.
Dá pra fazer tudo pelo teclado: as setas escolhem o padrão, e o Enter ou o Tab preenchem.
Criar conta. E de onde vêm os padrões? Das contas e dos lançamentos do último ano com a mesma descrição. Vale também nas contas a receber e nas entradas e saídas do caixa e do banco.""",
7: """Tem conta que volta todo mês com os mesmos dados. A internet do escritório, por exemplo. Pra essas, o sistema ajuda a preencher.
Primeiro a descrição e o Vencimento: a data da primeira parcela, vinte e três de novembro.
No Valor vai o total da compra, sete mil e oitenta, e não o valor da parcela. Categoria e fornecedor, como antes.
Clico em Preencher. Pronto: categoria, fornecedor e pagamento previsto, tudo de uma vez. E o cursor já pula pro Valor.
Digito duzentos e oitenta e nove e noventa, e ajusto o Vencimento pro dia quinze.
Uma dica: o padrão só preenche campo vazio. O que você já escolheu, ele não troca. E se não era isso, tem o Desfazer preenchimento, logo embaixo.
Dá pra fazer tudo pelo teclado: as setas escolhem o padrão, e o Enter ou o Tab preenchem.
Criar conta. E de onde vêm os padrões? Das contas e dos lançamentos do último ano com a mesma descrição. Vale também nas contas a receber e nas entradas e saídas do caixa e do banco.""",
8: """Agora uma compra dividida em vezes. Os pneus novos do caminhão truck saíram por sete mil e oitenta reais na Auto Peças Vale Forte, em três vezes.
No Valor vai o total da compra, sete mil e oitenta, e não o valor da parcela.
No Vencimento, a data da primeira parcela: vinte e três de novembro. Categoria e fornecedor, como antes.
Embaixo, em Parcelar ou repetir, ligo o Parcelar.
Escolho três parcelas. O sistema divide o valor e põe uma por mês, no mesmo dia: dois mil trezentos e sessenta reais cada. A soma fecha com o total, por isso a faixa fica verde.
Criar conta. Repara: já entraram todas, de novembro até abril.
O sistema guarda um molde da conta. Com data de parar, ele já cria todas até ela. Sem data, ele mantém sempre os próximos três meses na lista e cria a seguinte sozinho, conforme o tempo passa.
Cada parcela vira uma conta separada. Dá pra pagar uma sem mexer nas outras.
Parcelar é pra dívida com fim, como esses pneus. Pro gasto que volta todo mês, é o Repetir, que vem agora.""",
9: """A empilhadeira da Recicla Vale é alugada: dois mil e trezentos reais todo dia doze, num contrato até abril.
Clico em editar na de dezembro. Como ela faz parte de uma recorrência, o sistema pergunta antes: só esta conta, ou esta e as próximas?
Só esta conta mexe só na de dezembro. Esta e as próximas muda esta, as seguintes que ainda não foram pagas e o molde, pras novas já nascerem certas.
Escolho Esta e as próximas e mudo o vencimento pra quinze de dezembro. Repara no aviso: as próximas andam o mesmo tanto.
Salvar. Novembro ficou no dia doze, e de dezembro em diante foi tudo pro dia quinze.
Excluir faz a mesma pergunta. Esta e as próximas encerra a recorrência daqui pra frente, e as contas já pagas ficam no histórico. Aqui eu só cancelo.
O sistema guarda um molde da conta. Com data de parar, ele já cria todas até ela. Sem data, ele mantém sempre os próximos três meses na lista e cria a seguinte sozinho, conforme o tempo passa.""",
10: """As parcelas dos pneus funcionam parecido. A Auto Peças pediu pra passar o vencimento pro dia vinte e oito, a partir da segunda.
Clico em editar na parcela dois. Aqui são três opções: Só esta conta, Esta e as próximas, ou Todas as parcelas pendentes.
Escolho Esta e as próximas e troco o vencimento pra vinte e oito de dezembro.
Salvar. A segunda e a terceira andaram juntas, e a primeira ficou como estava.
Uma dica: nessa edição em grupo, o valor e os outros campos da tela vão pra todas as parcelas escolhidas. Se as parcelas têm valores diferentes, mude uma de cada vez, com Só esta conta.
Excluir faz a mesma pergunta. E parcela que já foi paga não é apagada: fica no histórico.""",
11: """E se uma delas mudar? A locadora pediu pra passar o vencimento pro dia quinze, a partir de dezembro.
Clico em editar na de dezembro. Como ela faz parte de uma recorrência, o sistema pergunta antes: só esta conta, ou esta e as próximas?
Só esta conta mexe só na de dezembro. Esta e as próximas muda esta, as seguintes que ainda não foram pagas e o molde, pras novas já nascerem certas.
Escolho Esta e as próximas e mudo o vencimento pra quinze de dezembro. Repara no aviso: as próximas andam o mesmo tanto.
Salvar. Novembro ficou no dia doze, e de dezembro em diante foi tudo pro dia quinze.
Excluir faz a mesma pergunta. Esta e as próximas encerra a recorrência daqui pra frente, e as contas já pagas ficam no histórico. Aqui eu só cancelo.
E a conta que atrasou? A água venceu dia cinco e veio com multa. Clico em Marcar pago.
O valor da conta continua o mesmo. A multa vai no campo Juros ou multa: quatro reais e setenta e sete. Ela entra como uma despesa separada, na categoria Juros e Multas.
Tem também o campo Tarifa, pra quando o banco cobra pelo boleto ou pela transferência.
E se você paga uma parte em dinheiro e outra por Pix, liga o Múltiplas formas de pagamento e coloca o valor de cada uma.
Uma dica: se pagar a mais numa conta com fornecedor, a sobra vira crédito dele, e a tela avisa antes de confirmar. Aqui eu só cancelo.""",
12: """Nem toda conta que se repete vem sempre igual. Este mês, o aluguel da empilhadeira veio com horas a mais: dois mil quatrocentos e quinze reais, em vez de dois mil e trezentos.
Clico em Marcar pago na de novembro. Como ela é de uma recorrência, aparece um campo lá em cima: Valor desta ocorrência.
Troco pra dois mil quatrocentos e quinze. O valor do pagamento acompanha sozinho.
Embaixo, o resumo mostra o previsto e o valor deste mês. E avisa: as próximas contas mantêm o valor previsto.
Se fosse um reajuste do contrato, era só ligar o Atualizar o valor previsto das próximas contas. Aí as próximas, que ainda estão abertas no valor antigo, passam pro valor novo.
Aqui foi só este mês, então deixo desligado. Escolho o Pix, a Conta Secundária, e confirmo.
Pronto. Novembro ficou paga por dois mil quatrocentos e quinze, e dezembro continua com dois mil e trezentos.
Uma dica: isso é diferente de pagar em parte. Aqui você corrige quanto a conta vale. O pagamento parcial é quando você paga menos do que ela vale.""",
13: """E quando um Pix só paga várias contas? A Recicla Vale vai adiantar duas parcelas dos pneus de uma vez.
Marco a caixinha das duas. Embaixo aparece uma barra com duas linhas selecionadas e o total: quatro mil setecentos e vinte reais.
Clico em Quitar em lote. As duas viram um lançamento só, do jeito que vai aparecer no extrato do banco.
Escolho o Pix, a Conta Secundária, confiro a descrição do lançamento e a data, e confirmo.
Pronto: as duas parcelas estão pagas, com um único lançamento no banco.
Uma dica: junte contas da mesma categoria. Com categorias diferentes, o pagamento entra no relatório sem categoria, e a tela avisa antes.
E dá pra marcar linha de saldo também: o fiado entra no lote, e você ainda escolhe quanto abater de cada um.""",
14: """Deu baixa na conta errada? Dá pra desfazer. Na conta paga, clico em Mais ações e em Estornar pagamento.
A tela mostra de onde o dinheiro saiu e avisa que ele volta pra lá: os cento e oitenta reais voltam pra Conta Principal, e a conta fica pendente de novo.
Excluir uma conta paga faz o mesmo caminho: o botão vira Excluir e estornar, e o dinheiro volta antes de a conta sumir.
Uma dica: se o pagamento já foi conciliado com o extrato do banco, desfaça a conciliação primeiro. Aqui eu só cancelo.""",
15: """As parcelas dos pneus funcionam parecido. A Auto Peças pediu pra passar o vencimento pro dia vinte e oito, a partir da segunda.
Clico em editar na parcela dois. Aqui são três opções: Só esta conta, Esta e as próximas, ou Todas as parcelas pendentes.
Escolho Esta e as próximas e troco o vencimento pra vinte e oito de dezembro.
Salvar. A segunda e a terceira andaram juntas, e a primeira ficou como estava.
Uma dica: nessa edição em grupo, o valor e os outros campos da tela vão pra todas as parcelas escolhidas. Se as parcelas têm valores diferentes, mude uma de cada vez, com Só esta conta.
Excluir faz a mesma pergunta. E parcela que já foi paga não é apagada: fica no histórico.""",
16: """Chegou a hora de pagar. Dar baixa é registrar que a conta foi paga. A energia vence hoje: mil oitocentos e setenta e quatro reais e trinta.
Clico em Marcar pago. A janela já vem com o Pix e a Conta Principal, que estavam no previsto, e com o valor inteiro.
Anexar, e escolho o comprovante. O arquivo sobe na hora, com o aviso Anexo adicionado. Pode ser pê-dê-éfe ou foto, até do celular.
Embaixo, a tela confirma que esse valor quita a conta.
A data é hoje. Confirmar pagamento. Pronto, a energia está Paga.
Uma dica: dar baixa mexe em dinheiro de verdade. No Pix, o valor sai da conta do banco; em dinheiro, sai do caixa aberto. E o lançamento leva a categoria da conta, por isso aparece certinho na dê-érri-ê, o relatório do resultado da empresa.
E é tudo junto: ou a baixa grava inteira, ou nada muda.
Agora um pagamento em parte. A Hidráulica Moréti pediu metade na entrega das peças, e o resto no fim do mês.
No valor, mil setecentos e quarenta reais. A tela mostra quanto falta pra quitar.
Como sobrou uma parte, aparece o Novo vencimento do restante. Coloco trinta de novembro.
Confirmar. A conta ficou Parcial: mostra quanto já foi pago e quanto era, e agora vence dia trinta.
E a conta que atrasou? A água venceu dia cinco e veio com multa. Clico em Marcar pago.
O valor da conta continua o mesmo. A multa vai no campo Juros ou multa: quatro reais e setenta e sete. Ela entra como uma despesa separada, na categoria Juros e Multas.
Tem também o campo Tarifa, pra quando o banco cobra pelo boleto ou pela transferência.
E se você paga uma parte em dinheiro e outra por Pix, liga o Múltiplas formas de pagamento e coloca o valor de cada uma.
Uma dica: se pagar a mais numa conta com fornecedor, a sobra vira crédito dele, e a tela avisa antes de confirmar. Aqui eu só cancelo.""",
17: """Nem toda conta que se repete vem sempre igual. Este mês, o aluguel da empilhadeira veio com horas a mais: dois mil quatrocentos e quinze reais, em vez de dois mil e trezentos.
Clico em Marcar pago na de novembro. Como ela é de uma recorrência, aparece um campo lá em cima: Valor desta ocorrência.
Troco pra dois mil quatrocentos e quinze. O valor do pagamento acompanha sozinho.
Embaixo, o resumo mostra o previsto e o valor deste mês. E avisa: as próximas contas mantêm o valor previsto.
E os cartões lá em cima mudaram junto: agora somam só as pendentes.
Aqui foi só este mês, então deixo desligado. Escolho o Pix, a Conta Secundária, e confirmo.
Pronto. Novembro ficou paga por dois mil quatrocentos e quinze, e dezembro continua com dois mil e trezentos.
No período de vencimento, tem três atalhos: Este mês, Próximos sete dias e Até o fim do mês.
Com um período ligado, os cartões mudam de nome: A receber no período e Recebido no período.
Uma dica: isso é diferente de pagar em parte. Aqui você corrige quanto a conta vale. O pagamento parcial é quando você paga menos do que ela vale.""",
18: """Precisa mandar essa lista pro contador ou imprimir? O botão Exportar gera um pê-dê-éfe ou uma planilha do Excel.
A janela já vem com os filtros que você está usando na tela, e dá pra mudar ali mesmo.
Em Opções do arquivo, você escolhe se o saldo dos clientes e fornecedores entra, e como agrupar: por status, por categoria ou por mês.
Aqui eu só fecho.""",
19: """Pronto! Recapitulando: a gente conheceu as abas, os quatro cartões e o calendário.
Lançou a manutenção da prensa, o conserto do pneu já pago e os pneus do caminhão em três vezes. E deixou o sistema preencher a internet do escritório pelo padrão.
Montou o aluguel da empilhadeira todo mês, até abril, e mudou o vencimento desta e das próximas. E fez o mesmo nas parcelas dos pneus.
Deu baixa na energia inteira e em metade da prensa, com o resto pro fim do mês. Pagou o aluguel da empilhadeira pelo valor real do mês e duas parcelas dos pneus num lançamento só.
Pronto: as duas parcelas estão pagas, com um único lançamento no banco. E viu como estornar uma baixa e exportar a lista.
Uma dica: junte contas da mesma categoria. Com categorias diferentes, o pagamento entra no relatório sem categoria, e a tela avisa antes.
E dá pra marcar linha de saldo também: o fiado entra no lote, e você ainda escolhe quanto abater de cada um.""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "A tela e as abas.",
           2: "Os quatro cartões do topo.",
           3: "Lista e calendário.",
           4: "Lançar uma conta.",
           5: "A conta que já nasce paga.",
           6: "O sistema preenche pra você.",
           7: "Parcelar uma conta.",
           8: "A conta que se repete.",
           9: "Só esta ou esta e as próximas.",
           10: "E as parcelas?",
           11: "Dar baixa.",
           12: "O valor real do mês.",
           13: "Pagar várias de uma vez.",
           14: "Desfazer uma baixa.",
           15: "O fiado na mesma lista.",
           16: "Anexar o comprovante.",
           17: "Filtrar a lista.",
           18: "Exportar a lista.",
           19: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "Contas",
           2: "Contas",
           3: "Contas",
           4: "Lançamento",
           5: "Lançamento",
           6: "Lançamento",
           7: "Lançamento",
           8: "Recorrência",
           9: "Recorrência",
           10: "Lançamento",
           11: "Baixa",
           12: "Baixa",
           13: "Baixa",
           14: "Baixa",
           15: "Fiado",
           16: "Comprovante",
           17: "Filtros",
           18: "Filtros",
           19: "Resumo"}

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
