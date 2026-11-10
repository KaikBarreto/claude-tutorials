# Texto enviado ao ElevenLabs (eleven_v4, voz Kaik Barreto) por capítulo do T22 "Gerencial: matriz e filiais".
# Gerado do roteiro.md (coluna Fala): cada linha do texto é uma linha da tabela Tela × Fala.
# Trocas de pronúncia em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   DRE -> "dê-érri-ê" | CMV -> "cê-ême-vê"
# Números por extenso nos dois lados (como na Domiflix).
CAPS = {
0: """Oi! Neste tutorial a gente vai fazer a matriz da Recicla Vale Metais, em Taubaté, enxergar a filial de Pindamonhangaba sem precisar entrar no sistema dela.
Com duas unidades, pra saber quanto o grupo vendeu no mês, alguém precisava abrir os dois sistemas e somar na mão. Aqui, os números das duas chegam juntos numa tela só.
Isso é o Gerencial. Ele depende do plano contratado, e quem contrata é a matriz.
Como ele junta a dê-érri-ê das unidades, se você ainda não viu o tutorial Relatório Financeiro e dê-érri-ê, dá uma olhada antes. [pause] Vamos entender como ele funciona.""",
1: """Sem grupo, o Gerencial começa assim, pedindo pra criar um.
O grupo junta as unidades. Cada unidade é uma empresa própria no sistema, com login e assinatura próprios. A matriz é a dona do grupo, e a filial entra nele.
A matriz enxerga os números de todas, manda o mesmo padrão de cadastro pras filiais e transfere material entre elas.
Uma dica: o Gerencial junta e padroniza, mas quem opera a filial é a filial. O caixa, as compras e as notas dela continuam com quem trabalha lá.""",
2: """Começando pela matriz. No Configurar Grupo, a gente cria o grupo.
Dou o nome, Grupo Recicla Vale, e clico em Criar Grupo.
Pronto. Aqui ficam as abas do grupo e um passo a passo do que falta configurar.
E esse é o código de convite. É ele que liga a filial ao grupo, e vale por trinta dias. Se vencer, o botão do lado gera outro.
Copio o código e mando pra quem cuida da filial, por mensagem.
Por enquanto, a lista de unidades tem só a matriz.""",
3: """Agora do lado da filial. A Sandra, gerente em Pindamonhangaba, entra no sistema da filial, em Configurações, na aba Empresa.
Lá embaixo fica o cartão Filial. Ela liga o É Filial.
E cola o código que recebeu da matriz.
Vincular. Pronto, a filial está no Grupo Recicla Vale.
Do lado dela, o dia a dia segue igual: a filial continua usando o próprio sistema, e a matriz passa a enxergar os números.""",
4: """De volta à matriz. Com a filial no grupo, o Dashboard Gerencial já mostra as duas unidades.
Vou olhar outubro inteiro: em cima, Mês passado. E aqui dá pra ver todas as unidades juntas, ou uma de cada vez.
Os cartões somam o grupo. Em outubro, a receita foi de duzentos e cinquenta e oito mil reais, e a despesa, de duzentos e cinquenta e um mil.
A setinha compara com o mês anterior. E o Estoque Total soma o estoque das duas unidades.
No gráfico, cada unidade aparece com a receita e a despesa lado a lado. A estrela marca a matriz.""",
5: """E o ranking ordena as unidades pelo lucro. Em outubro, a matriz ficou na frente.
Embaixo vem o resumo por unidade, em números.
A matriz vendeu cento e oitenta e seis mil, gastou cento e oitenta mil e lucrou seis mil reais. Margem de três vírgula dois por cento.
A filial vendeu setenta e dois mil, gastou setenta e um mil e lucrou mil reais.
Repara que a margem é pequena. É que aqui entra a compra inteira do mês, até o material que ainda está no pátio esperando venda. Isso fica claro na dê-érri-ê, com o regime de competência.""",
6: """Agora o Financeiro. Na aba dê-érri-ê, com outubro escolhido, fica a dê-érri-ê do grupo inteiro.
Começo pelo regime de caixa, o dinheiro que entrou e saiu. O grupo vendeu duzentos e cinquenta e oito mil e comprou duzentos e vinte mil em material.
Tirando as despesas da operação, trinta e um mil, sobram sete mil reais no mês.
E no Comparativo fica a mesma dê-érri-ê, unidade por unidade.
Os sete mil do grupo são seis mil da matriz e mil da filial. Assim você vê de onde vem o resultado.""",
7: """Agora o mesmo outubro em regime de competência. No lugar das compras entra o cê-ême-vê, o custo só do material que foi vendido: cento e noventa e quatro mil.
E o resultado do mês sobe pra trinta e três mil reais.
A diferença, vinte e seis mil, é o material que a gente comprou em outubro e ainda está no pátio. No caixa, ele já pesa no mês. Na competência, ele só vira custo quando for vendido.
O caixa mostra o dinheiro do mês. A competência mostra o lucro do que foi vendido. Os dois estão certos: cada um responde uma pergunta.
Uma dica: se aparecer aqui o aviso de material em estoque sem custo de compra, o lucro em competência pode estar maior do que é. Confira as entradas do período antes de decidir em cima do número.""",
8: """Agora o estoque. No Estoque Gerencial, a Visão Geral junta o estoque das duas unidades.
Na tabela, cada material numa linha e cada unidade numa coluna. O alumínio latinha: quatro mil e trezentos quilos na matriz e mil oitocentos e cinquenta na filial. No total, seis mil cento e cinquenta.
Na Posição de Estoque, você vê o saldo de cada material numa data, com o custo médio e o valor.
No Histórico de Materiais, cada entrada e cada saída, com a unidade de onde veio.
E no Relatório de Estoque, quanto o grupo comprou e vendeu de cada material, com o lucro e a margem.""",
9: """Agora a padronização. A matriz monta o padrão do grupo, e a filial recebe. Começa pelo catálogo de materiais.
Com um clique, o Importar do Estoque da Matriz traz os materiais que a matriz já usa.
As tabelas de preço da matriz entram sozinhas, assim que você abre a aba.
Nos clientes e fornecedores, você marca quem a filial também atende. A Fundição Bandeira do Vale compra das duas, então eu marco.
E as categorias financeiras também vêm prontas da matriz.
Com tudo pronto, na aba Unidades, o Enviar Ativos manda o padrão pra filial. O que ela já tinha fica como está, e o que faltava entra. Os preços dela só mudam se você ligar o Sobrescrever preços existentes.
Confirmar Envio. Agora as duas unidades falam a mesma língua: o mesmo material, com o mesmo nome.
Uma dica: se tirar uma filial do grupo por engano, nenhum dado dela se perde. Pra voltar, é só a filial colar o código de novo.""",
10: """Agora as transferências. A filial juntou alumínio latinha, e a matriz vai vender um lote grande. Primeiro, eu ligo o Exigir aprovação em transferências.
Assim, nenhum estoque se move sem confirmação. Em Nova, a origem é a filial e o destino, a matriz.
O material é o alumínio latinha: mil e duzentos quilos.
Repara no aviso do resumo: com a aprovação ligada, o estoque ainda não se move. Clico em Solicitar.
A transferência fica pendente. Quando o caminhão chega na matriz e o material é conferido, aí sim, Executar. A tela pede pra confirmar que o destino está de acordo.
Confirmar e Executar. Pronto: a matriz fica com cinco mil e quinhentos quilos, e a filial com seiscentos e cinquenta. O total do grupo continua o mesmo.
Uma dica: um material do grupo pode juntar mais de um material de uma unidade. O total do grupo soma todos, e a transferência tira de um só. Se o número do grupo parecer estranho, confira material por material.""",
11: """Por último, as assinaturas. Cada unidade tem a sua, e aqui a matriz vê todas: o plano, se está ativa e quando vence.
E dá pra pagar tudo de uma vez, numa fatura só, na matriz.
Repara no aviso: ao pagar, a cobrança de cada unidade é cancelada e vira uma fatura única, na matriz.
Uma dica importante: se a filial tinha um boleto ou um Pix da assinatura dela em aberto, ela não deve mais pagar aquele documento. Quem paga agora é a matriz, nessa fatura.
Escolho o Pix, e a cobrança única aparece.
Pagou, e pronto: as cobranças das unidades passam a vir nessa fatura da matriz.""",
12: """Pronto! Recapitulando: a gente criou o grupo na matriz, gerou o código de convite e vinculou a filial de Pindamonhangaba.
Leu o Dashboard Gerencial, com o ranking e o resumo de cada unidade.
Leu a dê-érri-ê do grupo nos dois regimes e comparou unidade por unidade.
Conferiu o estoque do grupo e mandou o mesmo catálogo pra filial.
Transferiu o alumínio com aprovação e pagou as assinaturas numa fatura só.
No próximo tutorial, o caminhão sai do pátio pra buscar material. Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "Como o Gerencial funciona.",
           2: "Criar o grupo e o código.",
           3: "Do lado da filial.",
           4: "O Dashboard Gerencial.",
           5: "Ranking e resumo por unidade.",
           6: "A dê-érri-ê do grupo.",
           7: "Caixa e competência.",
           8: "O estoque do grupo.",
           9: "Enviar Ativos.",
           10: "Transferência com aprovação.",
           11: "Assinaturas numa fatura só.",
           12: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "Gerencial",
           2: "Grupo",
           3: "Filial",
           4: "Dashboard",
           5: "Dashboard",
           6: "Financeiro",
           7: "Financeiro",
           8: "Estoque",
           9: "Padronização",
           10: "Transferências",
           11: "Assinaturas",
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
