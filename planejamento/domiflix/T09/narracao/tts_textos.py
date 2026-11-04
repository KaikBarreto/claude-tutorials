# Texto enviado ao ElevenLabs (eleven_v4, Fernanda) por capítulo do T9 "Orçamentos, Precificação e Proposta".
# Gerado do roteiro.md (coluna Fala): cada linha do texto é uma linha da tabela Tela × Fala.
# Trocas de pronúncia em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   BDI -> "bê-dê-i" | CRM -> "cê-érre-ême" | Clean -> "clin" | EPI -> "é-pê-i" | HH -> "agá-agá" | IPVA -> "i-pê-vê-á" | PDF -> "pê-dê-éfe" | Ticket -> "Tíquete" | spray -> "isprei" | R-410A -> "érre quatrocentos e dez á" | Van 01 -> "van zero um"
CAPS = {
0: """Oi! Neste tutorial a gente vai montar um orçamento com o preço certo e mandar uma proposta que fecha negócio.
Primeiro, a gente ensina a Dominex a calcular o preço com os custos da empresa. Depois, monta o orçamento, entrega a proposta, aprova e transforma tudo em ordem de serviço.
Se você ainda não viu o tutorial Estoque, compras e inventário, dá uma olhada antes. [pause] Vamos olhar a tela.""",
1: """A tela tem quatro abas no topo: Orçamentos, Custos dos Serviços, Custos Globais e Precificação. A primeira é a lista dos orçamentos, e as outras três cuidam de calcular o preço. À direita ficam o Configurar Proposta e o Novo Orçamento.
Em cima, três cartões. O Em Aberto soma o valor das propostas enviadas que ainda esperam resposta. O Tíquete Médio mostra o valor médio dos aprovados. E a Conversão compara os aprovados com os enviados, aprovados e rejeitados: o orçamento que já virou ordem de serviço sai dessa conta.
Clicando no Em Aberto, a lista mostra só os enviados, e a Conversão faz o mesmo com os aprovados. Para voltar, tiro a marca do filtro de Status.
Cada linha traz o número, o cliente, a data, o custo, o valor, a margem e o status. Dá para buscar por cliente, número ou telefone.""",
2: """Tudo começa pelo preço. Na aba Precificação, a Dominex usa o método do bê-dê-i: o preço é o custo total dividido pelo bê-dê-i, e assim imposto e despesas da empresa nunca ficam de fora.
Uma empresa nova começa com tudo zerado, e por isso o bê-dê-i vale um. Preencha e salve as taxas antes do primeiro orçamento, porque é delas que o preço sai. Imposto, seis por cento. Administração Indireta, doze por cento. Lucro Padrão, vinte e dois por cento.
O bê-dê-i atual vira zero vírgula seis: um menos quarenta por cento, que é a soma das três taxas. A barra mostra como o preço se compõe.
Embaixo, o deslocamento e o pagamento: um real e cinquenta centavos por quilômetro, cinco por cento de desconto à vista e até dez parcelas no cartão. Clico em Salvar. A partir daí, todo orçamento novo já nasce com essas taxas.
À direita, o Simulador de Preço. Se um serviço custa mil reais, o preço final é mil seiscentos e sessenta e seis reais e sessenta e sete centavos, que é mil dividido por zero vírgula seis. Ele usa as taxas que já estão salvas.""",
3: """Agora, quanto custa o que você usa para trabalhar. Na aba Custos Globais, que na tela se chama Centro de Custos, a gente cadastra veículos, ferramentas e outros recursos, e a Dominex rateia o custo por hora, sozinha.
Em Novo Recurso, a janela pergunta qual recurso eu quero cadastrar: veículos, ferramentas, brindes, é-pê-is ou outros. Vou de veículo.
Dou o nome, van zero um. As horas de uso por mês: cento e setenta e seis, que são vinte e dois dias de oito horas. A depreciação é de mil e quatrocentos reais por mês, e a manutenção com combustível, mil seiscentos e vinte reais.
O seguro, de três mil e seiscentos reais, e o i-pê-vê-á, de dois mil e quatrocentos reais, são valores anuais: a Dominex divide cada um por doze. No resumo, o total mensal fica em três mil quinhentos e vinte reais, e o custo por hora da van, em vinte reais.
Salvo. No alto, o custo por hora dos veículos já mostra vinte reais. E, clicando na van, vejo a composição do custo, item por item.""",
4: """Agora, o custo de cada serviço. Na aba Custos dos Serviços, escolho o tipo de serviço, a Higienização de Split. A tela tem quatro partes: mão de obra, recursos, materiais e resumo.
Na mão de obra, o técnico custa trinta e dois reais por hora, e o serviço leva uma hora e meia. O Custo agá-agá, ou hora-homem, fica em quarenta e oito reais. A tela salva sozinha.
Se você prefere calcular a hora a partir da equipe, o botão Calcular abre uma calculadora com o custo mensal de cada funcionário. Como eu já sei o valor, fecho.
Em Recursos, vinculo a van zero um. Ela custa vinte reais por hora, e o serviço dura uma hora e meia: trinta reais.
Em Materiais, escolho do estoque um limpa-evaporador em isprei, uma fita isolante e uma mangueira de dreno, um de cada. Aqui o material entra pelo preço de custo, e o total é trinta reais.
No Resumo, a soma: quarenta e oito reais de mão de obra, trinta reais de recurso e trinta reais de material, ou seja, cento e oito reais de custo. Dividido pelo bê-dê-i, o preço sugerido é cento e oitenta reais.
Isso se faz uma vez só. Daí em diante, o preço sai calculado em todo orçamento.""",
5: """Com o motor de preço pronto, vamos montar o orçamento. Em Novo Orçamento, o assistente tem três etapas, e a primeira é a Montagem, que começa pelo destinatário.
Posso orçar para um cliente cadastrado ou para um prospecto, alguém que ainda não é cliente e só precisa de um nome. Ainda não é cliente? Orce como prospecto.
Hoje é cliente cadastrado: a Pousada Brisa do Mar.""",
6: """Descendo na mesma tela, chegam os serviços. No bloco Configurações bê-dê-i, o Ajustar taxas e entender o bê-dê-i mostra as taxas que salvei na Precificação. Elas valem só para este orçamento, e posso ajustar se precisar.
Escolho a Higienização de Split e a quantidade, três, que são os três splits da pousada. O preço unitário já sai calculado: cento e oitenta reais, que é o custo de cento e oito reais dividido pelo bê-dê-i.
Clicando no nome do serviço, vejo de onde vem o preço: a mão de obra, os materiais, os recursos e extras, e o custo total de cada unidade.
Agora a Carga de Gás. Esse serviço ainda não tem custo cadastrado, e a Dominex avisa com o selo Sem custos configurados. Nesse caso, o preço vem do preço padrão do tipo de serviço: trezentos e cinquenta reais.
O subtotal dos serviços fecha em oitocentos e noventa reais.
Uma dica: se você digita o preço na mão, ou muda a quantidade depois, aquela linha deixa de acompanhar as taxas do bê-dê-i.""",
7: """Logo abaixo ficam os materiais. Em Adicionar materiais, busco gás e escolho o Gás refrigerante érre quatrocentos e dez á. O preço que aparece, cento e cinquenta reais por quilo, é o preço de venda cadastrado no estoque.
Coloco um quilo e adiciono ao orçamento. O material do estoque entra pelo preço de venda, sem bê-dê-i, e a lista não mostra saldo, porque orçar não consome estoque.
Embaixo, o deslocamento: dezoito quilômetros. A Dominex multiplica pelo custo por quilômetro, que dá vinte e sete reais de custo, e, na modalidade Custo por quilômetro mais bê-dê-i, o preço resultante é de quarenta e cinco reais.""",
8: """No Próximo, entram as Condições comerciais, com o desconto em reais ou em porcentagem. Dou oitenta e cinco reais, e o Preço praticado, aqui do lado, vai fechar em mil reais.
A caixa de brindes e o número de parcelas, em À vista, eu deixo como estão.
Em Observações, escrevo o horário de atendimento. Em Condições e Termos, a regra do serviço: executado depois da aprovação, em data combinada com o cliente.
Repara que os dois textos saem na proposta do cliente: Condições e Termos aparece como Informações adicionais, e Observações aparece com o mesmo nome. Então escrevo pensando nele.""",
9: """Agora a última etapa, Revisão e envio. Em Válido até, marco quinze dias à frente: é a data que o cliente vê na proposta. O modelo é o clin, com a Capa da proposta ao lado.
No resumo, aqui do lado, o Preço sugerido, mil e oitenta e cinco reais, é só uma referência para você. Logo abaixo, o guia O que entra no bê-dê-i mostra o que o bê-dê-i calcula sozinho e o que fica de fora, como a Carga de Gás e o gás, que entram pelo preço cadastrado.
O que vale é o Preço praticado, mil reais: os preços das linhas, mais o deslocamento, menos o desconto. É o valor da proposta e da ordem de serviço.
Embaixo, as opções de pagamento: novecentos e cinquenta reais à vista, com cinco por cento de desconto, ou dez parcelas de cem reais no cartão.
Clico em Criar Orçamento. Ele entra na lista como Rascunho, e ainda não foi para o cliente.""",
10: """Agora, o documento que o cliente recebe. Em Configurar Proposta, o primeiro passo é o modelo: clin, Vanguarda, Aurora ou Prisma, cada um com uma capa diferente.
Aqui é só a prévia. O modelo de cada proposta, a gente escolhe dentro do orçamento, como acabei de fazer. Eu fico com o clin.
Em Personalização, ajusto o tamanho do logo, que vem da empresa. Mais abaixo ficam as cores, a de destaque e a do cabeçalho, e as chaves para mostrar a paginação e o deslocamento.
Nas Seções da proposta, ligo, desligo e mudo a ordem de cada parte pelas setas, no modelo clin. Ligo a Garantia e escrevo: Garantia de noventa dias sobre o serviço. Esse texto vira o padrão de todos os orçamentos.
Na Revisão, folheio as páginas e vejo como a proposta chega ao cliente. É um exemplo, e não o orçamento da pousada.
Salvo. O que eu salvo aqui vale para todas as propostas da empresa. A janela continua aberta, e eu fecho.""",
11: """Antes de mandar, eu confiro. No menu da linha, Visualizar abre a proposta como o cliente vai ver, no modelo clin. A primeira linha avisa que ele ainda não abriu.
No canto ficam o WhatsApp, que abre a conversa com a mensagem pronta, o pê-dê-éfe, que gera o arquivo, e o Gerar cobrança, assunto de outro tutorial. O envio é manual, e esses botões não mudam o status do orçamento.
Para mandar de verdade, uso Gerar link da proposta. Ele copia o link, pronto para colar numa mensagem, e muda o orçamento para Enviado. É a partir daí que o cliente vê os botões Aprovar e Rejeitar.
Repara no cartão Em Aberto, que subiu: ele soma justamente as propostas enviadas.""",
12: """Vamos ver do lado do cliente. Ele recebe o link e abre a proposta no navegador, sem precisar entrar no sistema. No alto, a empresa, o número do orçamento e a validade.
Mais abaixo, os dados do cliente, os serviços e os materiais, com valor unitário, quantidade e subtotal, e os totais, com o deslocamento e o desconto. O total é o que a gente viu: mil reais.
Depois, as formas de pagamento, à vista no pix ou parcelado no cartão, as informações adicionais, as observações e a garantia que configurei. Tudo o que escrevi no orçamento está aqui.
O cliente pode baixar a proposta em pê-dê-éfe. E, no fim, ficam dois botões, Aprovar e Rejeitar, que só aparecem porque o orçamento está como Enviado.
Se ele aprova, basta um clique, sem precisar entrar nem se cadastrar.
De volta à Dominex, o orçamento da Pousada já está Aprovado. Uma dica: quando o cliente aprova pelo link, a conta a receber só nasce sozinha se a opção Aprovação pelo link da proposta já gera conta a receber estiver ligada, em Configurações.""",
13: """Outra informação útil fica na lista. Embaixo do nome do cliente, o olho mostra quantas vezes ele abriu a proposta e há quanto tempo. No Hotel Mirante do Mar, foram três vezes, e, passando o mouse, aparece o dia e a hora da última.
Já a proposta da Casa de Repouso Vida Mansa, que é um prospecto, ainda não foi aberta: o olho está apagado, com Não visualizada.
Quando você mesmo abre pelo item Abrir proposta em nova guia, a olhada do dono não conta. E a mesma pessoa, no mesmo navegador, só conta de novo depois de trinta minutos.""",
14: """E se o cliente fechar por telefone ou pelo WhatsApp, você aprova por dentro. Neste outro orçamento, o do Hotel Mirante do Mar, que está como Enviado, abro o menu e clico em Aprovar orçamento.
A janela mostra o valor, três mil e duzentos reais, e pergunta como o cliente vai pagar: Já recebi ou Vou receber depois.
No Vou receber depois, as três parcelas já vêm do orçamento. Escolho o primeiro vencimento, e a lista mostra cada parcela que será criada, nos mesmos dias dos meses seguintes.
Se o cliente já tivesse pago, o Já recebi pede a forma de pagamento, a data, a conta onde o dinheiro entrou e a tarifa, se houve. Aqui é a receber, então volto.
Clico em Aprovar e gerar conta a receber. Pronto: três parcelas criadas em Contas a Receber, e a linha ganha o selo No financeiro. No menu, passa a existir o Ver lançamento no financeiro.
Repara que a aprovação lança só a receita. O custo do orçamento serve para você enxergar a margem, e não vira despesa.""",
15: """Voltando à Pousada, que aprovou pelo link: hora de gerar a ordem de serviço. No menu da linha, clico em Gerar OS. Antes, a Dominex pergunta em qual equipamento cada serviço será feito, e já aplica os checklists ligados a cada um.
A higienização é nos três splits da pousada, e o botão Todos marca os três de uma vez. A Carga de Gás é só no split da recepção.
Clico em Gerar OS. A ordem nasce com os serviços, os equipamentos, os checklists e o valor do orçamento, e o orçamento passa para Convertido.
Na tela de Ordens de Serviço, a OS número dezessete já está lá, agendada, no valor de mil reais. Falta só escolher o técnico e a data, como no tutorial de Ordens de Serviço.
Uma dica: o Gerar OS não mexe no estoque. O consumo de material é lançado na própria ordem, quando o técnico a executa.""",
16: """Pronto! Recapitulando: você ensinou a Dominex a calcular o preço. Salvou as taxas na Precificação, cadastrou a van zero um nos Custos Globais e montou o custo da higienização, que virou preço pelo bê-dê-i.
Montou o orçamento em três etapas, com serviços, materiais, deslocamento e desconto, e viu a diferença entre o Preço sugerido e o Preço praticado.
Configurou a proposta, gerou o link, viu o que o cliente vê, aprovou com um clique e acompanhou as visualizações.
Aprovou outro orçamento por dentro, com as parcelas, e transformou o aprovado em ordem de serviço, distribuída pelos equipamentos.
Com o orçamento fechado, o próximo passo é encher o funil de novos clientes. No próximo tutorial, a gente vê o cê-érre-ême. Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "A tela e as quatro abas.",
           2: "O bê-dê-i da empresa.",
           3: "O custo da van zero um.",
           4: "Quanto custa executar um serviço.",
           5: "O destinatário.",
           6: "Serviços e preço.",
           7: "Materiais e deslocamento.",
           8: "Desconto e condições.",
           9: "Validade e revisão.",
           10: "Configurar a proposta.",
           11: "Visualizar e gerar o link.",
           12: "O que o cliente vê.",
           13: "Quem abriu a proposta.",
           14: "Aprovar por dentro.",
           15: "Gerar a ordem de serviço.",
           16: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "Orçamentos",
           2: "Precificação",
           3: "Custos globais",
           4: "Custos dos serviços",
           5: "Orçamentos",
           6: "Orçamentos",
           7: "Orçamentos",
           8: "Orçamentos",
           9: "Orçamentos",
           10: "Proposta",
           11: "Proposta",
           12: "Proposta",
           13: "Proposta",
           14: "Aprovação",
           15: "Ordem de serviço",
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
