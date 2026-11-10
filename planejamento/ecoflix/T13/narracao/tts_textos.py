# Texto enviado ao ElevenLabs (eleven_v4, voz Kaik Barreto) por capítulo do T13 "Contas a Pagar e Receber".
# Gerado da coluna Fala do roteiro.md: cada linha do texto é uma linha da tabela Tela × Fala.
# Trocas de pronúncia em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   Contas a Pagar/Receber -> "Contas a Pagar e Receber" | Cliente/Fornecedor -> "Cliente ou Fornecedor"
#   DRE -> "dê-érri-ê" | PDF -> "pê-dê-éfe" | Moretti -> "Moréti" (nova, testar no ensaio de pronúncia)
#   Vence em 7 dias -> "Vence em sete dias" (o rótulo do cartão; a legenda volta ao 7)
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
Pra lançar uma conta nova, o botão é este: Nova conta.""",
2: """Antes da lista, os quatro cartões lá de cima. Eles mostram quanto a empresa deve, quanto tem pra receber e o que está apertando.
O Total a Pagar soma as contas que a empresa ainda deve, mais o que ela deve no saldo, o fiado. O Total a Receber é o contrário: as contas a receber, mais o que devem pra ela no saldo.
Vencidas é o que passou do vencimento e não foi pago, como a água. Vence em sete dias é o que vence de hoje até daqui a sete dias, como a energia.
Esses dois somam só contas, as a pagar e as a receber. O saldo não tem data de vencimento, então fica de fora deles.
Uma dica: repara que eu troquei de aba e os números não mudaram. Os cartões mostram sempre a empresa inteira, com ou sem filtro.""",
3: """E dá pra ver as mesmas contas num calendário. A tela abre na Lista, e do lado fica o Calendário.
No calendário, cada dia mostra as contas que vencem nele. Vermelho é conta a pagar, e verde, a receber.
O triângulo avisa que tem conta vencida naquele dia. É a água, do dia cinco.
Clicando no dia, aparecem as contas dele, já com os botões de pagar e de editar.
Uma dica: o calendário mostra só conta com vencimento. O saldo dos clientes e fornecedores não tem data, então ele fica na Lista, como a própria tela avisa.
Pra voltar, é só clicar em Lista.""",
4: """Agora, lançar uma conta nova. A Hidráulica Moréti vai fazer a manutenção da prensa, e o serviço vence dia dezenove. Clico em Nova conta.
O Tipo já vem como A pagar. Se fosse dinheiro entrando, seria A receber.
No Valor, três mil quatrocentos e oitenta reais.
Na Descrição, o que é a conta: manutenção da prensa enfardadeira. E o Vencimento, dezenove de novembro.
A Categoria diz que tipo de gasto é esse. Aqui, Manutenção de máquinas.
Como é conta a pagar, o campo já vem em Fornecedor. É só escolher a Hidráulica Moréti.
O Centro de custo diz qual parte da empresa gastou. A prensa fica no pátio, então, Pátio.
No Pagamento previsto, eu digo de onde esse dinheiro deve sair: da Conta Principal. É só uma previsão, mas na hora de pagar ela já vem sugerida.
Criar conta. Pronto: a manutenção entrou na lista, pendente, com a data, a categoria e o fornecedor.""",
5: """E quando a conta chega já paga? Ontem, o conserto do pneu da empilhadeira foi pago na hora, por Pix: cento e oitenta reais.
Preencho como qualquer conta: o valor, a descrição, a data de ontem, a categoria e o centro de custo.
No Pagamento previsto, a conta de onde o Pix saiu: a Conta Principal.
Agora o que muda: ligo o Já paguei essa conta. Ele registra o pagamento junto, e a conta já nasce quitada. Na Data do pagamento, ontem.
Criar conta. Ela já entra como Paga, e o dinheiro já saiu da Conta Principal. Nada fica pendente pra lembrar depois.
Numa conta a receber, a opção vira Já recebi essa conta.""",
6: """Agora uma compra dividida em vezes. Os pneus novos do caminhão truck saíram por sete mil e oitenta reais na Auto Peças Vale Forte, em três vezes.
No Valor vai o total da compra, sete mil e oitenta, e não o valor da parcela.
No Vencimento, a data da primeira parcela: vinte e três de novembro. Categoria e fornecedor, como antes.
Embaixo, em Parcelar ou repetir, ligo o Parcelar.
Escolho três parcelas. O sistema divide o valor e põe uma por mês, no mesmo dia: dois mil trezentos e sessenta reais cada. A soma fecha com o total, por isso a faixa fica verde.
Aplicar faturamento. O resumo mostra as três vezes, a primeira data e o total.
Criar conta. Pronto, três parcelas criadas.
Cada parcela vira uma conta separada. Dá pra pagar uma sem mexer nas outras.
Parcelar é pra dívida com fim, como esses pneus. Pro gasto que volta todo mês, é o Repetir, que vem agora.""",
7: """A empilhadeira da Recicla Vale é alugada: dois mil e trezentos reais todo dia doze, num contrato até abril.
Valor, descrição e categoria, como sempre. O Vencimento é o da primeira: doze de novembro.
Em Parcelar ou repetir, agora eu ligo o Repete. Ele gera as contas sozinho, na frequência que você escolher.
Pode ser semanal, mensal ou anual. Aqui é mensal, a cada um mês.
E no Repetir até, a data de parar: doze de abril, o fim do contrato. Sem data, ele repete sem fim.
Criar conta. Repara: já entraram as contas de novembro, dezembro e janeiro.
O sistema guarda um molde da conta e mantém sempre os próximos três meses na lista. Conforme o tempo passa, ele cria a seguinte sozinho, até a data de parar.""",
8: """E se uma delas mudar? A locadora pediu pra passar o vencimento pro dia quinze, a partir de dezembro.
Clico em editar na de dezembro. Como ela faz parte de uma recorrência, o sistema pergunta antes: só esta conta, ou esta e as futuras?
Só esta conta mexe só na de dezembro. Esta e as futuras muda esta, as próximas que ainda não foram pagas e o molde, pras novas já nascerem certas.
Escolho Esta e as futuras e mudo o vencimento pra quinze de dezembro. Repara no aviso: as próximas andam o mesmo tanto.
Salvar. Novembro ficou no dia doze, e dezembro e janeiro foram pro dia quinze.
Excluir faz a mesma pergunta. Esta e as futuras encerra a recorrência daqui pra frente, e as contas já pagas ficam no histórico. Aqui eu só cancelo.""",
9: """Chegou a hora de pagar. Dar baixa é registrar que a conta foi paga. A energia vence hoje: mil oitocentos e setenta e quatro reais e trinta.
Clico em Marcar pago. A janela já vem com o Pix e a Conta Principal, que estavam no previsto, e com o valor inteiro.
Uma dica: quem não tem permissão pra mexer no banco não vê o Pix aqui. A baixa sai do caixa, e um aviso amarelo explica isso.
Embaixo, a tela confirma que esse valor quita a conta.
A data é hoje. Confirmar pagamento. Pronto, a energia está Paga.
Uma dica: dar baixa mexe em dinheiro de verdade. No Pix, o valor sai da conta do banco; em dinheiro, sai do caixa aberto. E o lançamento leva a categoria da conta, por isso aparece certinho na dê-érri-ê, o relatório do resultado da empresa.
E é tudo junto: ou a baixa grava inteira, ou nada muda.
Agora um pagamento em parte. A Hidráulica Moréti pediu metade na entrega das peças, e o resto no fim do mês.
No valor, mil setecentos e quarenta reais. A tela mostra quanto falta pra quitar.
Como sobrou uma parte, aparece o Novo vencimento do restante. Coloco trinta de novembro.
Confirmar. A conta ficou Parcial: mostra quanto já foi pago e quanto era, e agora vence dia trinta.""",
10: """Agora, o fiado. Ele aparece na mesma lista, com a etiqueta roxa Saldo. A Aços Quiririm levou três mil quilos de ferro misto a prazo: três mil cento e cinquenta reais.
A linha de saldo não tem vencimento nem categoria. É o total que o cliente deve, como o caderninho do balcão.
A baixa dele é própria. Clico em Receber. A Aços Quiririm mandou um Pix, então troco pro Pix e escolho a Conta Principal.
Ela pagou dois mil reais. Embaixo, a tela já mostra o saldo depois da baixa: mil cento e cinquenta.
Confirmar recebimento. O saldo da Aços Quiririm caiu pra mil cento e cinquenta.
Agora repara na Fundição Bandeira do Vale. Ela comprou trezentos quilos de cobre mel a prazo, em três vezes. E aqui só aparecem as parcelas.
Uma dica: se o saldo de um cliente sumir da lista, olha se a venda foi parcelada. Na venda a prazo em parcelas, o mesmo dinheiro fica no saldo e nas parcelas. Pra não cobrar duas vezes, a lista desconta do saldo o que já virou parcela.
Se tudo virou parcela, a linha de saldo some. Se só uma parte virou, ela mostra só o que sobra.
Uma dica: essas parcelas vieram do pedido de venda. Aqui dá pra mudar a descrição, o vencimento e a categoria; o valor e o cliente se mudam no próprio pedido.""",
11: """E o comprovante daquele Pix da energia? Ele fica guardado na própria conta.
Clico em editar e abro o Mais detalhes. Aqui ficam as observações e os anexos.
Anexar, e escolho o comprovante. Pode ser pê-dê-éfe ou foto, até do celular.
Salvar. O comprovante já está na conta.
E onde ele aparece depois? Aqui mesmo: é só abrir a conta e o Mais detalhes. Clicando na miniatura, o arquivo abre.
Uma dica: se o comprovante já estiver com você na hora de dar baixa, anexa ali mesmo, no campo Comprovante. Aí ele fica na conta e também no lançamento do banco ou do caixa.""",
12: """Com a lista cheia, os filtros ajudam a achar o que você procura. Na aba A Receber, repara nas linhas de saldo, lá no fim.
Clico em Filtros. Dá pra filtrar por status, categoria, Cliente ou Fornecedor, centro de custo, banco previsto e período de vencimento.
No Status, marco Pendente e aplico. A lista mostra só as pendentes, e o botão Filtros avisa que tem um filtro ligado.
Uma dica: repara que as linhas de saldo saíram. O saldo não tem status nem vencimento. Então, com filtro de status, período, categoria, centro de custo ou banco, ele fica de fora.
E os cartões lá em cima continuam iguais, como a gente viu.
Junto com o status, escolho a Fundição Bandeira do Vale. Pronto: as três parcelas dela.
Pra ver tudo de novo, Limpar filtros. E as linhas de saldo voltam.""",
13: """Pronto! Recapitulando: a gente conheceu as abas, os quatro cartões e o calendário.
Lançou a manutenção da prensa, o conserto do pneu já pago e os pneus do caminhão em três vezes.
Montou o aluguel da empilhadeira todo mês, até abril, e mudou o vencimento desta e das futuras.
Deu baixa na energia inteira e em metade da prensa, com o resto pro fim do mês.
Recebeu parte do saldo da Aços Quiririm e viu por que o fiado parcelado aparece só nas parcelas.
E anexou o comprovante e filtrou a lista.
No próximo tutorial, a gente faz o extrato do banco bater com o sistema. Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "A tela e as abas.",
           2: "Os quatro cartões do topo.",
           3: "Lista e calendário.",
           4: "Lançar uma conta.",
           5: "A conta que já nasce paga.",
           6: "Parcelar uma conta.",
           7: "A conta que se repete.",
           8: "Só esta ou esta e as futuras.",
           9: "Dar baixa.",
           10: "O fiado na mesma lista.",
           11: "Anexar o comprovante.",
           12: "Filtrar a lista.",
           13: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "Contas",
           2: "Contas",
           3: "Contas",
           4: "Lançamento",
           5: "Lançamento",
           6: "Lançamento",
           7: "Recorrência",
           8: "Recorrência",
           9: "Baixa",
           10: "Fiado",
           11: "Comprovante",
           12: "Filtros",
           13: "Resumo"}

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
