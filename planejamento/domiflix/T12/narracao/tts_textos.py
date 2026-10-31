# Texto enviado ao ElevenLabs (eleven_v4, Fernanda) por capítulo do T12 "Portal do Cliente e Portal do Contrato".
# Gerado do roteiro.md (coluna Fala): cada linha do texto é uma linha da tabela Tela × Fala.
# Trocas de pronúncia em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   BTUs -> "bê-tê-ús" | Hi-Wall -> "rai-uól" | PDF -> "pê-dê-éfe" | PMOC -> "pê-móqui" | QR Code -> "quê-érre côde" | 36.000 BTUs -> "trinta e seis mil btus"
CAPS = {
0: """Oi! Neste tutorial a gente vai deixar o cliente acompanhar as ordens de serviço, os aparelhos e o pê-móqui dele por um link e por um quê-érre côde, sem precisar ligar pra perguntar.
São dois portais: o do cliente, com tudo o que é dele, e o do contrato, pensado para uma unidade. O cliente ainda abre chamados por lá, e cada chamado chega aqui como ordem de serviço.
Se você ainda não viu o tutorial Contratos e pê-móqui, dá uma olhada antes. [pause] Vamos começar pelo link do cliente.""",
1: """Todo cliente da Dominex tem o próprio portal. Pra ver como ele é configurado, abro a ficha do Hotel Mirante do Mar e vou em Ações, Editar, e na aba Portal.
A primeira chave é o Portal ativo. Todo cliente já nasce com ele ligado, e é ele que faz o link e o quê-érre côde do equipamento funcionarem. Logo abaixo fica o Link do portal, exclusivo de cada cliente.
Se você quiser proteger o portal, é só ligar o Exigir senha para entrar. Aparecem os campos Senha e Confirmar senha, e cada seção ganha três opções: Oculto, Sem senha e Com senha.
Assim dá pra proteger só uma parte e deixar o resto aberto. A senha é uma por cliente, e a mesma vale no portal do contrato. Aqui o hotel fica sem senha, então eu desligo de novo.
Embaixo, você escolhe o que o cliente enxerga: Ordens de serviço, Equipamentos, Contratos, Cobranças, Notas fiscais, Documentos e Abrir chamados. Notas fiscais e Documentos vêm desligados, e você liga quando quiser.
Não mudei nada, então fecho em Cancelar. Pra mandar o link ao cliente, abro Ações e clico em Copiar link do portal. Ele vai pra área de transferência, pronto pra colar numa mensagem.""",
2: """Link copiado. Agora, olha o que o hotel vê quando abre. Eu abro sem entrar na minha conta, do jeito que o cliente faria. No alto, o nome da sua empresa e a saudação: Olá, Hotel Mirante do Mar.
No menu ficam só as seções que você liberou: Ordens de Serviço, Equipamentos e Contratos. O Contratos aparece porque o hotel tem um contrato ativo.
Em Ordens de Serviço, ele acompanha todas as ordens do hotel, as visitas do pê-móqui inclusive, e ainda pode buscar. Quando o técnico está a caminho ou em atendimento, o cartão ganha o botão Acompanhar. Nas concluídas, ele abre o relatório e avalia o atendimento.
Em Equipamentos, os quatro aparelhos do hotel, cada um com o próprio histórico de manutenção. A gente abre um deles mais à frente.
Em Contratos, o pê-móqui do hotel, com o selo pê-móqui. Clicando nele, o cliente chega na página da unidade, que a gente vê mais pra frente.
No canto, o Falar com a empresa: o cliente escolhe entre Ligar, WhatsApp e E-mail, com os contatos da sua empresa.
Repara que eu abri o link sem estar logado. Pra conferir o que o cliente vê, abra o link numa janela anônima: logado na sua conta, o portal mostra tudo pra sua equipe. E lá embaixo fica o Abrir Chamado, que é o próximo passo.""",
3: """E quando o ar dá problema, o próprio cliente avisa por aqui. Ele clica em Abrir Chamado, e abre uma janela simples.
No Descreva o problema, ele escreve do jeito dele: o ar do restaurante está pingando água perto da janela.
Se quiser, ele escolhe o aparelho. É opcional, mas ajuda o técnico a chegar sabendo qual é: o Cassete trinta e seis mil bê-tê-ús do restaurante.
Ele clica em Enviar Chamado, e pronto: chamado aberto com sucesso. A ordem de serviço já aparece no topo da lista dele, como Pendente.
O chamado já nasce como uma ordem de serviço de verdade, no seu sistema, e o cliente acompanha o andamento por aqui mesmo.""",
4: """E do lado de cá, onde os chamados aparecem? Assim que você abre o Dashboard, a Dominex avisa quantos chamados de cliente estão aguardando. Aqui são dois: o do hotel, que acabou de chegar, e o da Mariana Lopes, que já estava na fila.
Clico em Ver chamados e chego na aba Chamados, das Ordens de Serviço. Aqui está o do hotel. Cada linha traz a ordem, o cliente com o aparelho embaixo, a descrição, a origem, quando foi aberto e o status.
Os filtros separam os chamados abertos de todos os outros, e também o portal de onde cada um veio, o do cliente ou o do contrato.
Clicando na linha, abre a ordem de serviço. Pra marcar a data e escolher o técnico, é só usar o Editar, como a gente viu no tutorial de Ordens de Serviço.
No Kanban, os chamados esperam numa coluna só deles, a Chamados do Portal, até ganharem uma data. Assim que você marca a data, o chamado sai dessa coluna e segue o fluxo normal da ordem de serviço.
Uma dica: o chamado também aparece na aba Chamados da ficha do cliente e na do equipamento, então quem está olhando o cadastro já vê o que está aberto.""",
5: """Lembra do quê-érre côde do equipamento, do tutorial de Clientes, Fornecedores e Equipamentos? Agora dá pra ver aonde ele leva. Este é o rai-uól dezoito mil bê-tê-ús da sala dos professores, no Colégio Monte Verde.
Quando o cliente aponta a câmera do celular para o quê-érre côde colado no aparelho, abre o portal do cliente já nesse aparelho, com o histórico de manutenção.
O Copiar link guarda esse mesmo endereço, o que o quê-érre côde abre. Vou usar ele pra ver do lado do cliente.
É isso que o cliente vê quando escaneia. O portal do colégio abre direto na seção Equipamentos, já no rai-uól da sala dos professores. Na Visão geral, a marca Aerovento, o modelo, a capacidade e os campos que você deixou visíveis.
Em Histórico, as ordens de serviço feitas nesse aparelho, inclusive as visitas do contrato. Nas concluídas, o cliente abre o relatório da manutenção.
Em Anexos, o manual que a gente guardou na ficha do aparelho. Tudo o que você anexa lá, o cliente consegue abrir aqui.
E o Voltar para lista leva o cliente de volta aos aparelhos dele.""",
6: """Agora o outro portal, o do contrato, pensado para uma unidade. Em Gestão, Contratos, abro o pê-móqui do hotel. Na Visão Geral, fica o cartão Portal do Contrato.
Todo contrato já nasce com o link da unidade. Com o Portal Público ligado, qualquer pessoa com o link vê a página, só pra leitura. É isso que faz o quê-érre côde do quadro abrir.
Aqui ficam o quê-érre côde e o link da unidade. Clico em Copiar link, e o aviso diz: cole onde quiser compartilhar.
O Imprimir quê-érre côde é do contrato pê-móqui: ele baixa a folha pronta pra colar no quadro da unidade, com o nome da empresa, o quê-érre côde e o responsável técnico. Quem passa pelo quadro aponta o celular e acompanha o plano.""",
7: """Logo abaixo, o Quem vê o quê no portal. O mesmo link serve para a portaria e para o síndico, porque cada seção tem três opções: Oculto, Sem senha e Com senha.
São oito seções: Visão geral, Equipamentos, Cronograma, Ocorrências, Documentos, Histórico, Histórico pê-móqui e Cobranças.
Por exemplo: a portaria não precisa ver as cobranças do hotel. Em Cobranças, clico em Oculto, e pronto. Cada clique já grava, sem botão de salvar, e vale na hora pra quem abrir o link.
O Com senha usa a senha do Portal do Cliente, aquela da aba Portal do cadastro. Cadastrando a senha lá, ela passa a valer nos dois portais, e o Abrir cadastro do cliente leva direto pra essa tela.
Assim, o que está Sem senha abre direto, e o que está Com senha pede a senha. Dá pra liberar o plano pra portaria e deixar os documentos só pro síndico.""",
8: """Falta liberar os documentos do pê-móqui. Na aba Documentos, o cartão Documentos no portal do cliente mostra o selo Oculto: sem liberar, os documentos ficam só com a sua equipe.
Pra eles aparecerem pro hotel, é só clicar em Liberar documentos no portal do cliente. O selo vira Liberado, e o botão passa a ser Ocultar documentos do portal, se um dia você quiser voltar atrás.
O hotel passa a baixar o Dossiê, o Termo, o Certificado e o Cronograma da unidade, sem precisar pedir pra ninguém.""",
9: """Tudo configurado. Agora a visão de quem escaneia o quê-érre côde no quadro do hotel. A página abre sem pedir login. No alto, o nome da empresa, o Plano de Manutenção e o selo Em dia. E a aba Cobranças, que eu ocultei, não aparece.
Na Visão Geral, o plano, a frequência mensal, o início do contrato e a conformidade com a lei do pê-móqui. Embaixo, o Responsável Técnico, o Ricardo Tavares Albuquerque, com o registro e a modalidade.
Em Equipamentos, os aparelhos da unidade.
No Cronograma, o calendário das visitas. Avanço até o mês em que o plano começa, e lá está a primeira visita. Quem lê o quê-érre côde vê quando o técnico vai passar na unidade, mês a mês.
Em Ocorrências, cada visita do contrato com o status dela, como Agendada. Quando o técnico sai pra visita, aparece também o Acompanhar ao vivo.
Em Documentos, o que a gente acabou de liberar: Dossiê, Termo, Certificado e Cronograma, cada um com a validade, no Válido até, e o botão Baixar pê-dê-éfe.
Conforme o técnico conclui as visitas, a aba Histórico vai guardando o que foi feito em cada uma.
E no rodapé, o Abrir chamado nesta unidade. Um chamado aberto aqui cai direto no contrato, e chega na Dominex igual ao do portal do cliente.""",
10: """Então, qual link mandar? Repara que, no portal do cliente, o contrato do pê-móqui aparece na seção Contratos. Clicando nele, o cliente chega na página da unidade.
Pra escolher, pensa em quem vai abrir. O Portal do Cliente é do dono ou do gestor: mostra tudo do cliente, as ordens de serviço, os aparelhos, os contratos e as cobranças. O Portal do Contrato é da portaria, do síndico e da fiscalização: mostra só aquela unidade, e o quê-érre côde vai no quadro.
Os dois se completam, e a mesma senha vale nos dois.""",
11: """Pronto! Recapitulando: cada cliente tem o seu portal, com um link que você copia na ficha, a senha opcional e a escolha do que ele pode ver.
O cliente acompanha as ordens de serviço e os aparelhos, e abre chamados que chegam pra você como ordem de serviço, no aviso do Dashboard e na aba Chamados.
O quê-érre côde do equipamento abre o portal já no aparelho, com o histórico e os anexos.
E o Portal do Contrato dá à unidade um link e um quê-érre côde próprios. Você decide quem vê o quê, libera os documentos do pê-móqui, e o hotel acompanha o plano inteiro.
Com o cliente acompanhando tudo, falta cuidar do dinheiro que entra e sai. No próximo tutorial, a gente vê o Financeiro. Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "O link de cada cliente.",
           2: "O que o hotel vê.",
           3: "O cliente abre um chamado.",
           4: "Onde o chamado cai.",
           5: "O quê-érre côde do equipamento.",
           6: "O link da unidade.",
           7: "Quem vê o quê.",
           8: "Os documentos no portal.",
           9: "A página da unidade.",
           10: "Qual link mandar.",
           11: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "Portal do cliente",
           2: "Portal do cliente",
           3: "Chamados",
           4: "Chamados",
           5: "QR Code",
           6: "Portal do contrato",
           7: "Portal do contrato",
           8: "Documentos",
           9: "Portal do contrato",
           10: "Portal do cliente",
           11: "Resumo"}

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
