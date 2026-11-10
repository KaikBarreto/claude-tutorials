# Texto enviado ao ElevenLabs (eleven_v4, voz Kaik Barreto) por capítulo do T20 "Portal do Cliente e Fornecedor".
# Cada linha do texto é uma linha da tabela Tela × Fala do roteiro.md (mesma ordem).
# Trocas de pronúncia em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   QR Code -> "quê-érre côde" | XML -> "xis-ême-éle" | DANFE -> "dânfi" | PDF -> "pê-dê-éfe" | A4 -> "á-quatro" (T3)
#   PET -> "pét" (T4)
# A testar no ensaio: "WhatsApp" e "Siqueira" na escrita normal.
CAPS = {
0: """Oi! Neste tutorial a gente vai parar de mandar print pro parceiro no WhatsApp.
Toda semana, a Cooperativa Recomeço pergunta quanto tem pra receber da Recicla Vale Metais. E alguém do escritório para tudo pra tirar print.
Com o portal, ela abre um link e vê tudo sozinha: os pedidos, o saldo, as notas e o relatório.
O link fica na ficha de cada parceiro. Em Clientes e Fornecedores, eu abro a cooperativa, e ele está aqui, em Acesso ao portal.
O portal faz parte do módulo Portal do Cliente, que depende do plano contratado.
Se você ainda não viu o tutorial Clientes, fornecedores e a ficha do parceiro, dá uma olhada antes. [pause] Vamos ver o que a cooperativa enxerga.""",
1: """É isso que a cooperativa vê quando abre o link. Em cima, o logo, o nome e o contato da Recicla Vale.
Logo abaixo, o nome dela. O portal é o mesmo pra cliente e pra fornecedor, e cada um vê só o que é dele.
Do lado ficam as abas: Histórico, Saldo, Notas Fiscais, Relatório e Coletas. A gente vê cada uma daqui a pouco.
E até onde vai o acesso dele? O portal é só pra ver. O parceiro não muda nada no seu sistema.
A única coisa que ele manda é um pedido de coleta. E quem marca o dia, o horário, o motorista e o caminhão é você.
Uma dica: se um parceiro avisar que o link mostrou Portal indisponível, confere o plano da empresa. É ele que libera o portal.""",
2: """Agora, o link. Na ficha da cooperativa, em Visão geral, fica o Acesso ao portal.
Clico em Copiar, e pronto, o link está copiado. Aí é só colar na conversa com a cooperativa.
O mesmo link também sai aqui no menu, em Portal do Fornecedor.
Repara no fim do endereço. Esse código é só da cooperativa. Cada parceiro tem o seu, então o link de um nunca abre os dados de outro.
Uma dica: quem tem o link, entra. Então manda só pro contato certo da cooperativa, e evita mandar em grupo.
O link também fica no Editar, na aba Portal. E é aqui que a gente escolhe o que a cooperativa vê.""",
3: """Em O que exibir no portal, tudo já vem ligado. Você desliga só o que não quiser mostrar.
No Histórico, dá pra escolher os cartões de resumo, o gráfico dos materiais, os valores e as fotos dos pedidos.
Com Valores financeiros desligado, o parceiro vê os pesos dos pedidos, mas não os preços.
Depois vêm o Saldo, as Notas Fiscais, o Relatório e as Coletas, cada um com a sua chave. Na cooperativa, fica tudo ligado.
Embaixo fica o formato do comprovante que o parceiro imprime. A cooperativa imprime em folha comum, então eu marco á-quatro.
Clico em Salvar exibição, e pronto.
Uma dica: tem parceiro que é cliente e fornecedor ao mesmo tempo, como o Depósito Irmãos Siqueira. Os dois cadastros mostram o mesmo portal, com as compras e as vendas juntas.
Então, desligar uma aba num cadastro desliga nos dois links. Vale sempre o que esconde mais.""",
4: """Agora, a proteção. Pra deixar o portal mais seguro, ele pode pedir usuário e senha.
Ligo Pedir login no portal. Em Usuário, um nome fácil pra cooperativa lembrar. A senha, eu combino com ela.
Clico em Salvar acesso.
Repara que as abas mudaram. Agora cada uma tem três jeitos: Oculto, Livre ou Com senha. E todas começam Com senha.
Oculto, a aba some do portal. Livre, ela abre pra quem tem o link. Com senha, só depois do login. Na cooperativa, fica tudo com senha.
Agora, quando a cooperativa abre o link, aparece o Acesso restrito.
Ela digita o usuário e a senha, clica em Entrar, e o portal abre. Nesse navegador, ela fica conectada, sem digitar a senha toda vez.
Pra sair, é esse ícone. E no parceiro que é cliente e fornecedor, o mesmo usuário e a mesma senha valem pros dois links.""",
5: """Com o portal aberto, a primeira aba é o Histórico. Nos cartões, a cooperativa vê quanto a Recicla Vale já comprou dela.
São setenta e um mil seiscentos e cinquenta e um reais e cinquenta e oito, em quinze entregas.
No gráfico, os materiais que ela mais entrega, pelo peso. O papelão passa da metade, e depois vêm o pét e a latinha.
Embaixo, cada pedido. Clicando na entrega de sexta, abrem os materiais, com o peso e o valor de cada um.
E as fotos da carga, que a Recicla Vale anexou no pedido.
Agora, o portal de um cliente, a Fundição Bandeira do Vale. Aqui, os pedidos são as vendas.
Uma dica: a venda de hoje saiu com o Comprovante sem valores. Então, no portal, ela aparece com zero e um cadeado.
O pedido está certo no sistema. Pro parceiro, só os valores ficam escondidos: ele vê o latão e o cobre, com o peso.""",
6: """Agora, o saldo. A cooperativa vê aqui que tem mil trezentos e cinquenta reais pra receber da Recicla Vale.
No sistema, esse valor aparece em vermelho, porque a Recicla Vale deve. No portal, em verde, porque é a cooperativa que recebe. É o mesmo saldo, visto de cada lado.
Embaixo, o extrato dos últimos noventa dias: cada entrega e cada pagamento, com o saldo depois de cada um.
Agora a Recicla Vale acerta o resto. No sistema, em Movimentação, eu pago os mil trezentos e cinquenta reais no Pix.
Confirmar, e o saldo da cooperativa zerou no sistema.
E no portal, sem mandar link nenhum, o saldo já está em dia.
Uma dica: o saldo do portal vem da mesma conta-corrente da ficha. Com o portal aberto, ele se atualiza sozinho em até trinta segundos, e esse botão atualiza na hora.""",
7: """Na aba Notas Fiscais, o parceiro vê as notas emitidas pra ele. Na Fundição, aparece a nota mil duzentos e cinquenta, do cobre mel que saiu hoje, autorizada.
Ele confere o número, a série, a data, o valor e a situação. O arquivo da nota, o xis-ême-éle ou o dânfi, você manda pelo caminho de sempre, nas Notas Fiscais do sistema.
Já o Relatório soma os pedidos do parceiro, material por material.
Na cooperativa, eu escolho o mês passado. Em outubro, foram oito mil e quatrocentos quilos de papelão e dois mil e seiscentos de pét, entre outros.
No total, dezoito mil setecentos e cinquenta e cinco reais.
No Baixar pê-dê-éfe, o relatório abre pronto pra salvar. E se você não quiser mostrar os valores aqui, é só desligar Mostrar valores, na aba Portal.""",
8: """A aba Coletas é do módulo de coletas, que também depende do plano contratado. Com ela, a cooperativa pede a coleta sozinha.
Essa semana, o galpão dela encheu antes de sexta. Então ela clica em Solicitar coleta.
Ela escreve o material, papelão e pét prensados, e a quantidade, uns dois mil e quinhentos quilos.
Escolhe o dia que prefere, quinta de manhã. O endereço já vem do cadastro. E nas observações, onde estão os fardos.
Solicitar coleta, e pronto. O pedido entra como Solicitada.
E no sistema, o aviso chega no sino: nova solicitação de coleta.
A cooperativa sugeriu o dia, mas quem confirma o dia, o horário, o motorista e o caminhão é a Recicla Vale, na tela de Coletas. Isso fica pro tutorial de Coletas e Logística.""",
9: """E se a cooperativa precisar do comprovante de uma entrega? Ela mesma imprime, aqui na impressora do pedido.
Abre o comprovante em á-quatro, como a gente escolheu na aba Portal, com os materiais, os pesos e os valores da entrega.
E como esse pedido tem fotos, o comprovante sai com um quê-érre côde: Escaneie para ver fotos.
Num pedido com o Comprovante sem valores, o papel sai sem os preços, igual ao portal.""",
10: """Agora, as fotos. Elas entram na compra ou na venda, em Opções avançadas, no Anexar.
E quem aponta o celular pro quê-érre côde do comprovante cai numa página só com as fotos daquele pedido.
É essa página. Em cima, a Recicla Vale e o número do pedido. Embaixo, as fotos da carga.
Dá pra passar de uma foto pra outra e abrir cada uma em tela cheia.
Em Dados do Pedido ficam o fornecedor, a data, os materiais e o total: três mil e setecentos reais.
Uma dica: são dois links diferentes. O de fotos mostra só aquele pedido. O do portal mostra o histórico inteiro do parceiro, então cuida mais dele.
E no comprovante que sai no caixa, o quê-érre côde leva o parceiro pro portal dele, já aberto naquele pedido.""",
11: """Pronto! Recapitulando: a gente viu o que o parceiro enxerga no portal e copiou o link da cooperativa na ficha.
Escolheu as abas e o comprovante em á-quatro, e protegeu o portal com usuário e senha.
Conferiu o histórico, o saldo, que ficou em dia sozinho depois do pagamento, a nota da Fundição e o relatório de outubro.
A cooperativa pediu uma coleta e imprimiu o comprovante, e as fotos do pedido abriram pelo link público.
No próximo tutorial, a matriz enxerga todas as unidades de uma vez. Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "O que o parceiro vê.",
           2: "Pegar o link do portal.",
           3: "Escolher as abas.",
           4: "Usuário e senha.",
           5: "Histórico de pedidos.",
           6: "O saldo do parceiro.",
           7: "Notas e relatório.",
           8: "O parceiro pede a coleta.",
           9: "O comprovante do portal.",
           10: "As fotos do pedido.",
           11: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "Portal",
           2: "Link",
           3: "Exibição",
           4: "Senha",
           5: "Histórico",
           6: "Saldo",
           7: "Notas e relatório",
           8: "Coletas",
           9: "Comprovante",
           10: "Fotos",
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
