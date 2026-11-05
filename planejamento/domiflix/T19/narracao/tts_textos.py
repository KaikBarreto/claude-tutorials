# Texto enviado ao ElevenLabs (eleven_v4, Fernanda) por capítulo do T19 "Integração com Asaas, Assinaturas e Cobranças".
# Gerado do roteiro.md (coluna Fala) pelo gerador do lote 4: cada linha do texto é uma linha da tabela Tela × Fala.
# Trocas de pronúncia em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   API -> "á-pê-í" | MRR -> "ême-érre-érre" | Contas a Pagar/Receber -> "Contas a Pagar e Receber" | Asaas -> "asas" | PMOC -> "pê-móqui" | DRE -> "dê érri ê" | Pix -> "pix" | QR Code -> "quê-érre côde"
CAPS = {
0: """Oi! Neste tutorial a gente vai cobrar o cliente por um link. Ele paga por pix, boleto ou cartão, e o pagamento entra sozinho no Financeiro.
Dá pra cobrar uma vez só, todo mês ou a parcela de um contrato. Enquanto a integração não está ligada, a tela de Cobranças pede pra ativar os recebimentos primeiro.
As cobranças fazem parte do módulo Cobranças online. Com ele contratado, o item Cobranças aparece aqui no menu, dentro do Financeiro.
Se você ainda não viu o tutorial Financeiro, dá uma olhada antes. [pause] Vamos entender o caminho do dinheiro.""",
1: """Antes de configurar, vale entender o caminho do dinheiro. Você gera a cobrança na Dominex, e o cliente recebe um link pra pagar.
O dinheiro vai direto pra conta asas da sua empresa. É o asas que processa o pix, o boleto e o cartão, e a taxa dele sai dessa conta.
Quando o cliente paga, o asas avisa a Dominex, e a cobrança fica paga aqui sozinha, já com a baixa no Financeiro.""",
2: """Pra começar, a gente liga a conta asas da empresa. Em Configurações, aqui embaixo no menu, abro a aba Integrações e escolho Cobranças.
Se na sua empresa a integração já está ativa, pode pular pro próximo capítulo. A ligação é feita com a chave de á-pê-í, que você gera no painel do asas. Este quadro mostra o caminho em quatro passos.
Copio a chave no painel do asas e colo aqui. Ela é secreta, então o campo mostra só pontinhos.
Clico em Ativar recebimentos. Pronto, os recebimentos estão ativos, e já dá pra cobrar os clientes.""",
3: """Integração ligada, falta dizer pra onde vai o dinheiro. O aviso amarelo lembra disso. Clico em Escolher agora, e a tela desce até o Lançamento no Financeiro.
Na conta bancária de destino, a Conta Principal, que é o banco da empresa. A receita entra em Vendas de Serviços, e a taxa do asas já vem em Tarifas e Taxas.
Clico em Salvar. Com a conta escolhida, toda cobrança paga entra direto no Financeiro.
Repara nos dois interruptores, que já vêm ligados. O primeiro transforma cada cobrança numa conta a receber, que baixa sozinha quando o cliente paga. O segundo lança a taxa do asas como despesa, pro caixa bater certinho.""",
4: """Conta escolhida, agora as condições de cada cobrança. Aqui ficam as taxas da sua conta no asas, no pix, no boleto e no cartão, à vista ou parcelado, e o prazo pro dinheiro cair.
A taxa sai da sua conta no asas, e a Dominex não fica com nada por transação. Se o asas mudar as taxas, é só clicar em Atualizar taxas.
Em Multa e juros por atraso, a integração já vem com dois por cento de multa e um por cento de juros ao mês. Isso vale pras próximas cobranças, e dá pra mudar e salvar aqui.
Nas Preferências de cobrança ficam os meios de pagamento habilitados: pix, boleto e cartão de crédito, todos ligados. E o Desconto por antecipação premia quem paga antes do vencimento. Em branco, não tem desconto.""",
5: """Antes de cobrar, dá pra fazer a conta. Ao lado das configurações fica o Simulador, que mostra quanto sobra de uma venda depois da taxa e quando o dinheiro cai.
Imagina uma instalação de mil e duzentos reais no cartão, em três vezes, com a empresa absorvendo a taxa.
O resultado mostra o valor líquido que fica na sua conta e, embaixo, quando cai cada parcela.
No Repassar ao cliente, a taxa entra no que o cliente paga, e a empresa recebe o valor cheio.
No pix, o dinheiro cai na hora. Uma dica: o simulador é uma estimativa, e o valor final quem calcula é o asas, na hora da cobrança.""",
6: """Hora de cobrar de verdade. Com a integração ativa, a tela de Cobranças mostra os totais a receber, recebido e vencido, e a lista, ainda vazia.
Clico em Nova cobrança. A janela tem quatro abas e, com o cliente e o valor preenchidos, mostra embaixo o resumo do recebimento. O cliente é o Restaurante Sabor da Serra, que pediu a limpeza dos splits da cozinha.
Pra gerar a cobrança, o cliente precisa ter CPF ou CNPJ no cadastro, que é o dado que o asas pede. O restaurante já tem.
O valor é quatrocentos e cinquenta reais, com vencimento daqui a três dias. Repara na dica: no regime de competência, a receita entra hoje, que é quando a venda é registrada. Na descrição, o serviço.
Avanço pra aba Pagamento. Deixo o Cliente escolhe, e no link ele decide entre pix, boleto e cartão.
Em Encargos, a multa e os juros já vieram da configuração, e dá pra mudar só nesta cobrança.
Na aba Financeiro, o Lançar no financeiro está em Sim. A cobrança já entra como conta a receber, na categoria que a gente escolheu na integração.
Antes de gerar, o resumo mostra quanto sobra em cada forma de pagamento e quanto o cliente paga se atrasar.
Clico em Gerar cobrança. Pronto, a cobrança foi gerada, com um link de pagamento e um quê-érre côde. Com o cliente do seu lado, ele aponta a câmera e paga ali mesmo.
No botão do lado, copio o link pra mandar por e-mail ou mensagem. Ou clico em Enviar por WhatsApp, que abre o WhatsApp com a mensagem pronta, o valor e o link.""",
7: """Fechada a janela, a cobrança fica na lista como A receber, com a forma Cliente escolhe.
E o link fica sempre à mão. No menu da cobrança, o Copiar link pega o mesmo link de novo, pra reenviar quando precisar.
Enquanto ela está a receber, o Editar muda o valor, o vencimento e a descrição. Já o Excluir apaga a cobrança, e o link deixa de funcionar pro cliente.""",
8: """E do lado do cliente, o que aparece? Esta é a página que abre pelo link, com a marca da sua empresa, o valor, o vencimento e a descrição. Do outro lado, ele escolhe como pagar.
No pix, aparece o quê-érre côde e o código copia e cola. O cliente copia o código e paga no aplicativo do banco.
No boleto, ele abre o boleto numa nova aba. E no cartão, preenche os dados ali mesmo, sem sair da página.
Quando o cliente paga, o asas avisa o sistema, e a baixa vem desse aviso. Abrindo o mesmo link depois, a página mostra Pagamento confirmado.""",
9: """De volta ao sistema. A cobrança do restaurante está como Pago, e o valor foi pro total recebido. Ninguém precisou dar baixa à mão.
Em Contas a Pagar e Receber, a conta a receber da cobrança também ficou paga, e a linha mostra o valor cheio, a taxa do asas e o líquido.
Nas Movimentações, a receita entrou em Vendas de Serviços, e a taxa do asas virou uma despesa em Tarifas e Taxas.
Na cobrança paga, o menu traz o Estornar, que devolve o valor ao cliente pelo asas.""",
10: """E pra quem paga todo mês? Na aba Assinaturas, a cobrança se repete sozinha. Clico em Nova assinatura.
A Academia Ponto Forte fechou a manutenção mensal dos splits por trezentos e oitenta reais. A frequência é Mensal, mas vai de semanal a anual.
Na forma de pagamento, deixo o Cliente escolhe. A lista também tem o cartão de crédito recorrente e o pix Automático, em que o cliente autoriza o débito no banco.
O primeiro vencimento é no dia dez do mês que vem. Na Duração, a Contínua segue cobrando até você cancelar. Se o acordo tiver fim, o Número de ciclos diz quantas cobranças são.
O resumo mostra os valores de uma cobrança, e não da assinatura inteira.
Clico em Criar assinatura. A academia entrou na lista como Ativa, e lá em cima aparece a receita recorrente mensal, o ême-érre-érre, que soma as assinaturas ativas.""",
11: """Se o valor ou o vencimento mudar, o Editar resolve. Só o cliente fica travado depois que a assinatura é criada.
E quando o cliente desiste, é o Cancelar. As próximas cobranças deixam de ser geradas, e o que já foi cobrado continua no histórico do Financeiro.
A academia continua com a gente, então clico em Voltar.
Uma dica: no pix Automático, o cliente autoriza o débito no banco. Se uma assinatura dessas for cancelada e a autorização continuar ativa, a lista mostra o selo Autorização ativa no banco, com a opção Cancelar de novo.""",
12: """Lembra das parcelas do contrato pê-móqui? Com a integração ativa, cada mensalidade a receber ganhou o botão Cobrar online, aqui do lado.
Clico na segunda mensalidade. A janela já vem com o hotel, os mil e duzentos reais e o vencimento da parcela. Repara no aviso: quando o hotel pagar, a própria parcela é baixada, sem lançamento novo. Por isso não tem a aba Financeiro.
Como o resto já está certo, clico em Gerar agora, que pula as outras abas. A parcela ganhou o selo Cobrança gerada, e o link já pode ir pro hotel.
Essa janela de cobrança aparece em outros lugares. Numa conta a receber, é o Cobrar o saldo. No orçamento e no Faturar da ordem de serviço, é o Gerar cobrança.""",
13: """Pronto! Recapitulando: você ligou a conta asas da empresa pela chave de á-pê-í, escolheu a conta que recebe o dinheiro e conferiu as taxas, os encargos e o simulador.
Gerou uma cobrança, mandou o link, viu a página do cliente e acompanhou a baixa chegar sozinha no Financeiro, com a taxa lançada.
Criou uma assinatura mensal e cobrou online a parcela do contrato, que baixa sozinha quando o hotel pagar.
Com o dinheiro entrando e saindo, falta ler o resultado. No próximo tutorial, a gente vê o Relatório Financeiro e o dê érri ê. Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "Como o dinheiro chega.",
           2: "Conectar a conta.",
           3: "Para onde vai o dinheiro.",
           4: "Taxas e preferências.",
           5: "O simulador.",
           6: "Uma cobrança avulsa.",
           7: "A cobrança na lista.",
           8: "O que o cliente vê.",
           9: "Pago e baixado.",
           10: "Cobrança todo mês.",
           11: "Editar e cancelar.",
           12: "A parcela do contrato.",
           13: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "Cobranças",
           2: "Asaas",
           3: "Asaas",
           4: "Asaas",
           5: "Asaas",
           6: "Cobranças",
           7: "Cobranças",
           8: "Cobranças",
           9: "Cobranças",
           10: "Assinaturas",
           11: "Assinaturas",
           12: "Contratos",
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
