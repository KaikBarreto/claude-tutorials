# Texto enviado ao ElevenLabs (eleven_v4, voz Kaik Barreto) por capítulo do T22 "Gerencial: matriz e filiais" (aplicado ao app 1.60.18).
# Gerado do roteiro.md (coluna Fala): cada linha do texto é uma linha da tabela Tela × Fala.
# Trocas de pronúncia em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   DRE -> "dê-érri-ê" | CMV -> "cê-ême-vê"
# Números por extenso nos dois lados (como na Domiflix).
# Renumeração de 20/11 (1.60.18): 4 Quando o código não entra (novo) | 5 Dashboard (era 4) | 6 Ranking (era 5) | 7 DRE (era 6) |
# 8 Competência (era 7) | 9 Além da DRE (novo) | 10 Estoque (era 8) | 11 Corrigir o estoque (novo) | 12 Enviar Ativos (era 9) |
# 13 Preço por unidade (novo) | 14 Transferência com aprovação (era 10) | 15 Lote, fila e pedido da filial (novo) |
# 16 Vender com o estoque da outra unidade (novo) | 17 Assinaturas (era 11) | 18 Recapitulando (era 12).
CAPS = {
0: """Oi! Neste tutorial a gente vai fazer a matriz da Recicla Vale Metais, em Taubaté, enxergar a filial de Pindamonhangaba sem precisar entrar no sistema dela.
Com duas unidades, pra saber quanto o grupo vendeu no mês, alguém precisava abrir os dois sistemas e somar na mão. Aqui, os números das duas chegam juntos numa tela só.
Isso é o Gerencial. Ele depende do plano contratado, e quem contrata é a matriz. E quem pode abrir cada tela dele, você decide nas permissões de cada usuário.
Como ele junta a dê-érri-ê das unidades, se você ainda não viu o tutorial Relatório Financeiro e dê-érri-ê, dá uma olhada antes. [pause] Vamos entender como ele funciona.""",
1: """Sem grupo, o Gerencial começa assim, pedindo pra criar um.
O grupo junta as unidades. Cada unidade é uma empresa própria no sistema, com login e assinatura próprios. A matriz é a dona do grupo, e a filial entra nele.
A matriz enxerga os números de todas, manda o mesmo padrão de cadastro pras filiais e transfere material entre elas.
Uma dica: o Gerencial junta e padroniza, mas quem opera a filial é a filial. O caixa, as compras e as notas dela continuam com quem trabalha lá.""",
2: """Começando pela matriz. Clico em Configurar Grupo pra criar o grupo.
Dou o nome, Grupo Recicla Vale, e clico em Criar Grupo.
Pronto. Aqui ficam as abas do grupo e um passo a passo do que falta configurar.
Se bater dúvida no caminho, o botão Como funciona abre um resumo dos cinco passos, do convite até os resultados.
E esse é o código de convite. É ele que liga a filial ao grupo, e vale por trinta dias. Se vencer, o botão do lado gera outro.
Copio o código e mando pra quem cuida da filial, por mensagem.
Por enquanto, a lista de unidades tem só a matriz. E repara no contador: um de onze, a matriz mais até dez filiais.""",
3: """Agora do lado da filial. A Sandra, gerente em Pindamonhangaba, entra no sistema da filial, em Configurações, na aba Empresa.
Lá embaixo fica o cartão Filial. Ela liga o É Filial.
E cola o código que recebeu da matriz.
Vincular. Pronto, a filial está no Grupo Recicla Vale.
Do lado dela, o dia a dia segue igual: a filial continua usando o próprio sistema, e a matriz passa a enxergar os números.""",
4: """E se o código não entrar? O caso mais comum é esse: o código passou dos trinta dias, e o sistema avisa que ele expirou.
As outras recusas são três. Código inválido: confira letra por letra. Empresa que já está em outro grupo: ela precisa sair de lá antes. E grupo cheio: cada grupo aceita até dez filiais.
Na matriz, o aviso também aparece em vermelho, embaixo do código.
Um clique nesse botão gera um código novo, com mais trinta dias. O antigo deixa de valer, então mande o novo pra filial.""",
5: """De volta à matriz. Com a filial no grupo, o Dashboard Gerencial já mostra as duas unidades.
Vou olhar outubro inteiro: em cima, Mês passado. Além dos atalhos, o Personalizado aceita qualquer intervalo de datas.
E o seletor de unidades aceita marcar uma, duas ou todas. Marcando só a filial, os cartões e os gráficos passam a mostrar só ela. Esse mesmo seletor aparece no Financeiro e no Estoque.
Os cartões somam o grupo. Em outubro, a receita foi de trezentos e quarenta e quatro mil e quarenta reais, e a despesa, de trezentos e setenta mil, seiscentos e noventa.
O Lucro Líquido é o resultado da dê-érri-ê do grupo, em competência: o mesmo número que você vai encontrar no Financeiro.
A setinha compara com o período anterior do mesmo tamanho, no caso, setembro. E o Estoque Total soma o estoque das duas unidades.
No gráfico, cada unidade aparece com a receita e a despesa lado a lado. A estrela marca a matriz.""",
6: """E o ranking ordena as unidades pelo saldo, a receita menos a despesa. Em outubro, a filial ficou na frente, e a matriz, no vermelho.
Embaixo vem o resumo por unidade, em números.
A matriz teve duzentos e setenta e dois mil e quarenta de receita e duzentos e noventa e nove mil, seiscentos e noventa de despesa. Ficou negativa em vinte e sete mil, seiscentos e cinquenta reais.
A filial vendeu setenta e dois mil, gastou setenta e um mil e ficou com mil reais de saldo.
Repara no vermelho da matriz. É que aqui entra a compra inteira do mês, até o material que ainda está no pátio esperando venda. Por isso esse saldo não é igual ao Lucro Líquido do cartão, que segue a dê-érri-ê em competência.""",
7: """Agora o Financeiro. Na aba dê-érri-ê, com outubro escolhido, fica a dê-érri-ê do grupo inteiro.
Começo pelo regime de caixa, o dinheiro que entrou e saiu. O grupo vendeu trezentos e quarenta e um mil, duzentos e quarenta, e comprou trezentos e dezoito mil, oitocentos e sessenta em material.
Tirando os impostos e as despesas da operação, e somando o aluguel de caçamba, o mês fecha no vermelho: menos vinte e seis mil, seiscentos e cinquenta reais.
E no Comparativo fica a mesma dê-érri-ê, unidade por unidade.
O vermelho do grupo vem da matriz, menos vinte e sete mil, seiscentos e cinquenta, contra mil positivos da filial. Assim você vê de onde vem o resultado.""",
8: """Agora o mesmo outubro em regime de competência. No lugar das compras entra o cê-ême-vê, o custo só do material que foi vendido: duzentos e setenta e três mil, oitocentos e setenta e três reais e trinta centavos.
E o resultado do mês vira positivo: dezoito mil, trezentos e trinta e seis reais e setenta centavos.
A diferença, quase quarenta e cinco mil, é o material que a gente comprou em outubro e ainda está no pátio. No caixa, ele já pesa no mês. Na competência, ele só vira custo quando for vendido.
O caixa mostra o dinheiro do mês. A competência mostra o lucro do que foi vendido. Os dois estão certos: cada um responde uma pergunta.
E o Comparativo, em competência, mostra o cê-ême-vê de cada unidade, o custo só do que ela vendeu.
Uma dica: se aparecer aqui o aviso de material em estoque sem custo de compra, o lucro em competência pode estar maior do que é. Confira as entradas do período antes de decidir em cima do número.""",
9: """Ainda no Financeiro, três coisas rápidas. Na dê-érri-ê, as linhas de custos, impostos e despesas abrem, e mostram do que o total é feito.
Pelo botão Exportar, a dê-érri-ê vai pro contador ou pro sócio, com as unidades que você escolheu. E embaixo, o Patrimônio Operacional soma o caixa, o banco, o que tem a receber, o estoque e o que tem a pagar, do grupo inteiro.
A aba Dashboard mostra onde o grupo gasta e de onde vem a receita, por categoria.
E a aba Histórico lista os lançamentos das unidades, um por um. Dá pra filtrar por categoria e até pela conta bancária de onde o dinheiro saiu. Essas telas funcionam como no tutorial Relatório Financeiro e dê-érri-ê.""",
10: """Agora o estoque. No Estoque Gerencial, a Visão Geral junta o estoque das duas unidades.
Na tabela, cada material numa linha e cada unidade numa coluna. O alumínio latinha: seiscentos e quarenta quilos na matriz e mil oitocentos e cinquenta na filial. No total, dois mil quatrocentos e noventa.
A Posição de Estoque é uma foto do estoque numa data. Escolho trinta e um de outubro e clico em Ver posição: o saldo, o custo médio e o valor de cada material no fim daquele dia.
Clicando no material, ele abre unidade por unidade. E o botão Por unidade muda a tabela inteira pra esse jeito.
No Histórico de Materiais, o botão Filtros escolhe o período e o material. Cada linha mostra o tipo do movimento, a unidade e quem fez.
No Relatório de Estoque, os cartões de cima abrem. O Total Comprado mostra o preço médio e quanto saiu em dinheiro, em Pix, pelo saldo do parceiro e o que ficou em aberto.
E a linha do material abre por unidade. É aqui que você descobre se uma unidade está pagando mais caro que a outra no mesmo material.
Dá pra filtrar por usuário, esconder o que não teve movimento e exportar o relatório.""",
11: """Agora um caso do dia a dia. A filial contou o papelão no pátio e achou trinta quilos a menos que o sistema. A matriz resolve daqui, no menu de ações da linha.
Corrigir saldo. Escolho a unidade, a filial.
É uma saída de trinta quilos. A janela mostra o saldo de agora e como ele fica depois.
Escrevo o motivo. E repara: a correção fica no histórico da filial, marcada como ajuste feito pela matriz. Ninguém fica sem saber.
Registrar saída. Pronto, o estoque da filial está certo.
No mesmo menu, o Transferir entre materiais passa saldo de um material pra outro dentro da mesma unidade. Serve quando a filial lançou a compra no material errado.
Uma dica: essa tela soma as movimentações de cada unidade. Se um material tiver saldo no cadastro sem movimentação que explique, aparece um aviso embaixo, com a diferença material por material. O sistema não mexe sozinho: a conferência é sua.""",
12: """Agora a padronização. A matriz monta o padrão do grupo, e a filial recebe. Na aba Unidades, o passo a passo lá de cima mostra o que falta, e cada etapa leva à aba certa. Começa pelo catálogo de materiais.
Com um clique, o Importar do Estoque da Matriz traz os materiais que a matriz já usa.
Material que a matriz não trabalha também entra: é só dar o nome e a unidade. Ele aparece sem vínculos até alguma unidade usar. Foi engano? A lixeira tira do catálogo.
As tabelas de preço da matriz entram sozinhas, assim que você abre a aba.
Em Clientes e Fornecedores, você marca quem também faz negócio com a filial. A Fundição Bandeira do Vale compra das duas unidades, então eu marco.
Os fornecedores ficam na outra aba, com busca. Marcou, está disponível. Desmarcou, sai da lista das filiais.
E as categorias financeiras também vêm prontas da matriz. Dá pra desmarcar as que são só da matriz. As de cadeado vão sempre, porque a dê-érri-ê precisa delas.
Com tudo pronto, na aba Unidades, o Enviar Ativos manda o padrão pra filial. E não precisa mandar tudo sempre: dá pra desmarcar o que você não quer. Aqui eu mando tudo.
O que ela já tinha fica como está, e o que faltava entra. O preço que a filial já tem fica protegido, a não ser que você ligue o Sobrescrever preços existentes.
Confirmar Envio. Agora as duas unidades falam a mesma língua: o mesmo material, com o mesmo nome.
Lá embaixo, o Histórico de Envios guarda pra qual filial foi, o que foi enviado e quando.
Uma dica: se tirar uma filial do grupo por engano, nenhum dado dela se perde. Pra voltar, é só a filial colar o código de novo.""",
13: """O padrão do grupo inclui o preço. Abrindo uma tabela, aparecem os materiais do catálogo com o preço de compra e o de venda.
Dá pra ajustar aqui mesmo. Subo a compra da latinha pra seis e trinta e salvo.
Embaixo fica a Vinculação por Unidade. É ela que diz como cada unidade recebe esses preços. Ligo a filial.
A filial fica mais longe do comprador e tem frete, então ela trabalha cinco por cento abaixo da tabela. Tipo, porcentagem. Direção, abaixo. Valor, cinco. Salvar.
E o Aplicar grava os preços na filial, já com o desconto.
Uma dica: essa variação vale para os dois preços, o de compra e o de venda. Se a diferença for em reais por quilo, troque o tipo pra valor fixo.
Nessa barra você também puxa os preços de uma tabela da matriz ou exclui a tabela. O Excluir não pede confirmação, então cuidado com o clique.""",
14: """Agora as transferências. A filial juntou alumínio latinha, e a matriz vai vender um lote grande. Primeiro, eu ligo o Exigir aprovação em transferências.
Assim, nenhum estoque se move sem confirmação. Em Nova, a origem é a filial e o destino, a matriz.
O material é o alumínio latinha: mil e duzentos quilos.
Repara no aviso do resumo: com a aprovação ligada, o estoque ainda não se move. Clico em Solicitar uma transferência.
A transferência fica pendente. Quando o caminhão chega na matriz e o material é conferido, aí sim, Executar. A tela pede pra confirmar que o destino está de acordo.
Confirmar e Executar. Pronto: a matriz fica com mil oitocentos e quarenta quilos, e a filial com seiscentos e cinquenta. O total do grupo continua o mesmo.
Uma dica: um material do grupo pode juntar mais de um material de uma unidade. O total do grupo soma todos, e a transferência tira de um só. Se o número do grupo parecer estranho, confira material por material.""",
15: """A filial também pode pedir. No estoque dela, a Sandra marca os materiais e clica em Transferir Estoque.
Escolhe o destino e as quantidades. A tela mostra quanto tem em cada unidade e quanto vai ficar. O pedido segue pra matriz, e o estoque ainda não se move.
Esse pedido cai numa fila porque o grupo exige aprovação. Com o Exigir aprovação desligado, não existe fila: a transferência feita pela matriz move o estoque na hora.
Na matriz, o Estoque Gerencial tem uma aba Transferências, com o número de pedidos esperando.
Em Nova, a matriz monta um lote com vários materiais de uma vez. O Selecionar todos com saldo marca tudo que a origem tem. Se a quantidade passar do estoque, a linha avisa e o sistema não deixa seguir.
Corrijo e solicito. Agora são três na fila.
Uma delas não vai mais sair: Cancelar. Ela fica na lista, marcada como cancelada.
E as outras duas eu executo juntas, no Executar todas. Se alguma não tiver saldo na origem, as demais seguem, e a tela lista qual falhou e por quê.
Tem também um atalho na Visão Geral: no menu da linha, Transferir entre unidades já abre a transferência com o material escolhido.""",
16: """Último recurso das transferências. Nessa mesma aba fica o Usar estoque de outras unidades na venda, com uma chave por unidade. Ligo na matriz.
Agora, numa venda da matriz, faltam duzentos quilos de alumínio perfil. Em vez de travar, a janela pergunta de onde vem o resto.
Na lista aparece a filial, com o saldo que ela tem. Escolho, e a quantidade fica coberta.
Transferir e Adicionar. O item entra na venda, e a transferência da filial pra matriz acontece junto, quando a venda é finalizada.
Uma dica importante: isso só funciona com o Exigir aprovação desligado. Com a aprovação ligada, a venda avisa que o grupo exige aprovação e só deixa usar o estoque da própria unidade. É uma escolha do grupo: ou o controle da aprovação, ou a agilidade na venda.""",
17: """Por último, as assinaturas. Cada unidade tem a sua, e aqui a matriz vê todas: o plano, se está ativa e quando vence.
O Gerenciar de cada linha deixa a matriz mudar o plano daquela unidade, sem precisar do login dela.
E dá pra pagar tudo de uma vez, numa fatura só, na matriz.
Repara no aviso: ao pagar, a cobrança de cada unidade é cancelada e vira uma fatura única, na matriz.
Uma dica importante: se a filial tinha um boleto ou um Pix da assinatura dela em aberto, ela não deve mais pagar aquele documento. Quem paga agora é a matriz, nessa fatura.
Repara na Cobrança recorrente, que já vem ligada: o total do grupo é cobrado sozinho todo mês. Se quiser pagar só este mês, desligue antes de escolher a forma de pagamento.
As formas são cartão, sempre recorrente, Pix ou boleto. Escolho o Pix, e o quê-érre côde do grupo aparece.
Pagou, e pronto: as cobranças das unidades passam a vir nessa fatura da matriz.
Uma dica: pra pagar junto, todas as unidades precisam estar no mesmo ciclo, mensal ou anual. Se uma for anual e a outra mensal, o sistema avisa e não gera a fatura. Acerte o ciclo no Gerenciar e tente de novo.""",
18: """Pronto! Recapitulando: a gente criou o grupo na matriz, gerou o código de convite e vinculou a filial de Pindamonhangaba.
Viu o que fazer quando o código vence ou não entra.
Leu o Dashboard Gerencial, com o ranking e o resumo de cada unidade.
Viu a dê-érri-ê do grupo nos dois regimes, comparou unidade por unidade e foi além, até o histórico e o patrimônio.
Conferiu o estoque do grupo, corrigiu o saldo da filial e mandou o mesmo catálogo, com o preço certo de cada unidade.
Transferiu material com aprovação, montou um lote, executou a fila e vendeu com o estoque da outra unidade.
E pagou as assinaturas numa fatura só.
No próximo tutorial, o caminhão sai do pátio pra buscar material. Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "Como o Gerencial funciona.",
           2: "Criar o grupo e o código.",
           3: "Do lado da filial.",
           4: "Quando o código não entra.",
           5: "O Dashboard Gerencial.",
           6: "Ranking e resumo por unidade.",
           7: "A dê-érri-ê do grupo.",
           8: "Caixa e competência.",
           9: "Além da dê-érri-ê.",
           10: "O estoque do grupo.",
           11: "Corrigir o estoque de uma unidade.",
           12: "Enviar Ativos.",
           13: "Preço diferente por unidade.",
           14: "Transferência com aprovação.",
           15: "Lote, fila e o pedido da filial.",
           16: "Vender com o estoque da outra unidade.",
           17: "Assinaturas numa fatura só.",
           18: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "Gerencial",
           2: "Grupo",
           3: "Filial",
           4: "Filial",
           5: "Dashboard",
           6: "Dashboard",
           7: "Financeiro",
           8: "Financeiro",
           9: "Financeiro",
           10: "Estoque",
           11: "Estoque",
           12: "Padronização",
           13: "Padronização",
           14: "Transferências",
           15: "Transferências",
           16: "Transferências",
           17: "Assinaturas",
           18: "Resumo"}

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
