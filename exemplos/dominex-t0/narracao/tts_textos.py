# Texto enviado ao ElevenLabs (eleven_v4, Fernanda) por capítulo do T0 "Boas-vindas à Dominex" (aula ilustrada).
# Roteiro aprovado pelo Kaik em 30/10 22:02 (doc https://claude.ai/artifact/UQjsgSUXMRz34vCAh2qW3w, rev 7).
# Cada linha = uma linha da tabela Ilustração × Fala (a cena muda junto com a linha).
# Trocas de pronúncia (a legenda segue o roteiro, ver config_narracao.json):
#   "ép" -> "app"  |  "dominex ponto app barra guia técnico" -> "dominex.app/guia-tecnico"  |  "vinte por cento" -> "20%"
CAPS = {
0: """Oi! Boas-vindas à Dominex. A partir de agora, a sua empresa tem um lugar só pra organizar o trabalho, do chamado do cliente até o dinheiro na conta. Neste vídeo rápido, eu te mostro como a gente vai caminhar junto.""",
1: """Os tutoriais da Domiflix são o seu caminho pra dominar o sistema. Cada aula mostra uma área inteira, na prática, dividida em capítulos, pra você voltar direto no ponto que precisar.
Eles seguem uma ordem, e cada aula aproveita o que você viu antes: primeiro as configurações da empresa, a sua equipe e os cadastros, depois as ordens de serviço e o técnico em campo, e aí orçamentos, contratos, financeiro e por aí vai.
Pra encontrar, é só abrir o menu da sua conta e clicar em Tutoriais Domiflix.
E aqui vai o combinado mais importante: assiste aos tutoriais, na ordem. É neles que você descobre os recursos que fazem o sistema render de verdade no seu dia a dia.""",
2: """Bateu uma dúvida? Volta direto no capítulo daquele assunto.
E se você preferir ler, tem o Guia Técnico, no endereço dominex ponto ép barra guia técnico. Ali está cada função do sistema explicada por escrito, tela por tela, na mesma ordem dos tutoriais.
É só digitar na busca o que você procura, e um clique te leva direto no trecho que explica.
E sempre que precisar, o nosso suporte atende pelo WhatsApp: no menu da sua conta, é só clicar em Falar com o Suporte.
Uma dica: quando você já assistiu à aula daquele assunto, a conversa fica bem mais rápida, porque a gente já parte do mesmo ponto.""",
3: """Tudo sobre o seu plano fica na tela Assinatura, também no menu da sua conta. Ali você vê o status, o plano, o vencimento e o valor, acompanha o uso da conta e o histórico de pagamentos.
Pra pagar, é só clicar em Pagar Agora: dá pra usar Pix, boleto ou cartão. No plano anual, o Pix e o boleto têm vinte por cento de desconto; no cartão, a cobrança é mensal e renova sozinha.""",
4: """No período de teste, todos os módulos ficam liberados pra você conhecer; ao ativar a assinatura, ficam os do plano que você escolheu.
E quando a sua empresa crescer, o plano cresce junto. Em Gerenciar Meu Plano, você escolhe um dos Planos Prontos ou monta o seu no Personalizado, com os módulos e os usuários que precisar.
E funciona assim: se você aumenta o plano no meio do caminho, paga hoje só a diferença, proporcional aos dias que faltam até o vencimento.
Os recursos novos entram assim que o pagamento é confirmado, e a renovação seguinte já vem com o valor do plano novo.
E se você reduzir, continua com tudo até o vencimento, e o valor menor começa no próximo ciclo.""",
5: """Pronto, agora você já sabe como a gente vai trabalhar junto. O próximo passo é deixar a Dominex com a cara da sua empresa: no próximo tutorial, a gente coloca a logo, os dados da empresa e as preferências do dia a dia. Te vejo lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 e cap05 sem vinheta.
TITULOS = {1: "Como funcionam os tutoriais.", 2: "Quando bater uma dúvida.", 3: "A sua assinatura.",
           4: "Quando a empresa cresce."}
# Rótulo de área em cima do título (vinheta), como no T3 ("Equipamentos").
KICKERS = {1: "Começando", 2: "Ajuda", 3: "Assinatura", 4: "Assinatura"}
