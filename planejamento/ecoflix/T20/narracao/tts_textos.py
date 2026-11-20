# Texto enviado ao ElevenLabs (eleven_v4, voz Kaik Barreto) por capítulo do T20 "Portal do Cliente e Fornecedor" (EcoSistema 1.60.18, 16 capítulos).
# Cada linha do texto é uma linha da tabela Tela × Fala do roteiro.md (mesma ordem).
# Trocas de pronúncia em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   QR Code -> "quê-érre côde" | XML -> "xis-ême-éle" | DANFE -> "dânfi" | PDF -> "pê-dê-éfe" | A4 -> "á-quatro" (T3)
#   PET -> "pét" (T4) | WhatsApp -> "uatsápe" (T9)
# A testar no ensaio: "Siqueira" na escrita normal.
CAPS = {
0: """Oi! Neste tutorial a gente vai parar de mandar print pro parceiro no uatsápe.
Toda semana, a Cooperativa Recomeço pergunta quanto tem pra receber da Recicla Vale Metais. E alguém do escritório para tudo pra tirar print.
Com o portal, ela abre um link e vê tudo sozinha: os pedidos, o saldo, as notas e o relatório.
O link fica na ficha de cada parceiro. Em Clientes e Fornecedores, eu abro a cooperativa, e ele está aqui, em Acesso ao portal.
O portal faz parte do módulo Portal do Cliente, que depende do plano contratado.
Se você ainda não viu o tutorial Clientes, fornecedores e a ficha do parceiro, dá uma olhada antes. [pause] Vamos ver o que a cooperativa enxerga.""",
1: """É isso que a cooperativa vê quando abre o link. Em cima, o logo, o nome e o contato da Recicla Vale, com o título Portal do Fornecedor. Pra um cliente, o título é Portal do Cliente.
Logo abaixo, o nome dela. O portal é o mesmo pra cliente e pra fornecedor, e cada um vê só o que é dele.
Se você usa etiquetas ou campos personalizados no cadastro, só aparece aqui o que você liberou pro portal, nas Configurações de Clientes e Fornecedores.
Do lado ficam as abas: Histórico, Saldo, Notas Fiscais, Relatório e Coletas. A gente vê cada uma daqui a pouco.
No celular, que é onde quase todo parceiro abre o link, as abas viram uma lista no alto da página.
E até onde vai o acesso dele? O portal é só pra ver. O parceiro não muda nada no seu sistema.
A única coisa que ele manda é um pedido de coleta. E quem marca o dia, o horário, o motorista e o caminhão é você.
Uma dica: se um parceiro avisar que o link mostrou Portal indisponível, confere o plano da empresa. É ele que libera o portal. E se aparecer Link inválido, o endereço chegou errado ou pela metade. É só copiar de novo na ficha e mandar outra vez.""",
2: """Agora, o link. Na ficha da cooperativa, em Visão geral, fica o Acesso ao portal.
Clico em Copiar, e pronto, o link está copiado. Aí é só colar na conversa com a cooperativa.
O mesmo link também sai aqui no menu, em Portal do Fornecedor.
Repara no fim do endereço. Esse código é só da cooperativa. Cada parceiro tem o seu, então o link de um nunca abre os dados de outro.
Uma dica: quem tem o link, entra. Então manda só pro contato certo da cooperativa, e evita mandar em grupo.
O link também fica no Editar, na aba Portal. E é aqui que a gente escolhe o que a cooperativa vê.
Este ícone, Abrir portal, abre o portal numa aba nova, pra você conferir do jeito que o parceiro vai ver.
Em cadastro antigo, pode aparecer o aviso de que ainda não tem link de portal. Aí é só clicar em Gerar link. E na página cheia do parceiro, o botão Copiar link do portal faz a mesma coisa.""",
3: """Em O que exibir no portal, tudo já vem ligado. Você desliga só o que não quiser mostrar.
No Histórico, dá pra escolher os cartões de resumo, o gráfico dos materiais, os valores e as fotos dos pedidos.
Com Valores financeiros desligado, o parceiro vê os pesos dos pedidos, mas não os preços.
Depois vêm o Saldo, as Notas Fiscais, o Relatório e as Coletas, cada um com a sua chave. Com o Permitir solicitar coleta desligado, o parceiro acompanha as coletas, mas não pede uma nova. Na cooperativa, fica tudo ligado.
Embaixo fica o formato do comprovante que o parceiro imprime. O Automático segue o formato da sua empresa, e o Térmico serve pra quem imprime em bobina. A cooperativa imprime em folha comum, então eu marco á-quatro.
Clico em Salvar exibição, e pronto. O Salvar de baixo também grava essas escolhas.
Vamos ver na prática, com a Aços Quiririm. Eu desligo os Valores financeiros e a aba Saldo, e salvo.
No portal dela, sobram os cartões sem os valores, os pedidos aparecem zerados com um cadeado, e a aba Saldo sumiu.
Uma dica: tem parceiro que é cliente e fornecedor ao mesmo tempo, como o Depósito Irmãos Siqueira. Os dois cadastros mostram o mesmo portal, com as compras e as vendas juntas.
Então, desligar uma aba num cadastro desliga nos dois links. Vale sempre o que esconde mais.""",
4: """Agora, a proteção. Pra deixar o portal mais seguro, ele pode pedir usuário e senha.
Ligo Pedir login no portal. Em Usuário, um nome fácil pra cooperativa lembrar. A senha, eu combino com ela.
Clico em Salvar acesso.
Repara que as abas mudaram. Agora cada uma tem três jeitos: Oculto, Livre ou Com senha. E todas começam Com senha.
Oculto, a aba some do portal. Livre, ela abre pra quem tem o link. Com senha, só depois do login. Na cooperativa, fica tudo com senha.
Agora, quando a cooperativa abre o link, aparece o Acesso restrito.
Ela digita o usuário e a senha, clica em Entrar, e o portal abre. Nesse navegador, ela fica conectada, sem digitar a senha toda vez.
Pra sair, é esse ícone. E no parceiro que é cliente e fornecedor, o mesmo usuário e a mesma senha valem pros dois links.
Se a cooperativa esquecer a senha, não tem recuperação pelo portal: você digita uma nova aqui e salva. Deixando em branco, a senha continua a mesma. E pra tirar o login, é desligar a chave e clicar em Remover login.""",
5: """Nem tudo precisa de senha. No Depósito Irmãos Siqueira, eu ligo o login, escolho o usuário e a senha, e salvo o acesso. Repara no aviso: como ele é cliente e fornecedor, o acesso vale pros dois links.
Agora, no Histórico, eu marco Livre. Saldo, Notas Fiscais, Relatório e Coletas continuam Com senha. Salvar exibição.
Quando o Depósito abre o link, o Histórico aparece direto, sem pedir nada. E as outras abas ganham um cadeado.
Clicando em Saldo, o portal pede o usuário e a senha só pra essa parte. O resto continua aberto.
Uma dica: o que está com senha nem chega no navegador de quem abriu o link sem entrar. E o comprovante, o relatório e o pedido de coleta seguem a mesma trava.""",
6: """Repara no selo do Depósito: Cliente mais Fornecedor. Cada cadastro tem o seu link, mas os dois abrem o mesmo portal.
Em cima, o que a Recicla Vale comprou dele e o que vendeu pra ele, cada um no seu cartão, e o gráfico dos materiais.
Na lista, ele filtra: Todos, Compras ou Vendas. Clicando em Vendas, os cartões e o gráfico acompanham.
E o saldo é um só, já com as compras e as vendas na mesma conta.""",
7: """Com o portal aberto, a primeira aba é o Histórico. Nos cartões, a cooperativa vê quanto a Recicla Vale já comprou dela.
São setenta e um mil seiscentos e cinquenta e um reais e cinquenta e oito, em quinze entregas.
No gráfico, os materiais que ela mais entrega, pelo peso. O papelão passa da metade, e depois vêm o pét e a latinha.
Embaixo, cada pedido. Clicando na entrega de sexta, abrem os materiais, com o peso e o valor de cada um. Quando o pedido tem tara ou desconto, aparecem embaixo do material o peso bruto e a tara, igual ao comprovante.
E as fotos da carga, que a Recicla Vale anexou no pedido. Só imagem vai pro portal: se o pedido tiver um pê-dê-éfe anexado, ele fica só no sistema.
Agora, o portal de um cliente, a Fundição Bandeira do Vale. Aqui, os pedidos são as vendas.
Uma dica: a venda de hoje saiu com o Comprovante sem valores. Então, no portal, ela aparece com zero e um cadeado.
O pedido está certo no sistema. Pro parceiro, só os valores ficam escondidos: ele vê o latão e o cobre, com o peso. E o valor do pedido sem valor não sai em lugar nenhum do portal, nem no saldo, nem na nota fiscal, nem no comprovante.""",
8: """Agora, o saldo. A cooperativa vê aqui que tem mil trezentos e cinquenta reais pra receber da Recicla Vale.
No sistema, esse valor aparece em vermelho, porque a Recicla Vale deve. No portal, em verde, porque é a cooperativa que recebe. É o mesmo saldo, visto de cada lado.
Embaixo, o extrato dos últimos noventa dias: cada entrega e cada pagamento, com o saldo depois de cada um.
No extrato, além de Pedido e Pagamento, aparece Ajuste, quando você lança um crédito ou um débito na conta do parceiro, com o motivo que você escreveu. E passando de vinte linhas, tem o Ver todas as movimentações.
Agora a Recicla Vale acerta o resto. No sistema, em Movimentação, eu pago os mil trezentos e cinquenta reais no Pix.
Confirmar, e o saldo da cooperativa zerou no sistema.
E no portal, sem mandar link nenhum, o saldo já está em dia.
Uma dica: o saldo do portal é o mesmo da tela de Saldo do sistema, da mesma conta-corrente da ficha. Com o portal aberto, ele se atualiza sozinho em até trinta segundos, e esse botão atualiza na hora.
E quando é o parceiro que deve? O Valdir Pereira ficou com um vale de trezentos reais. No portal dele, o saldo aparece em vermelho, com Você tem a pagar, e a frase diz quem deve pra quem.""",
9: """Na aba Notas Fiscais, o parceiro vê as notas emitidas pra ele. Na Fundição, aparece a nota mil duzentos e cinquenta, do cobre mel que saiu hoje, autorizada.
E tem a nota mil duzentos e cinquenta e três, com o selo Entrada: é a devolução que a Fundição fez, e a nota de entrada quem emite é a Recicla Vale.
Ele confere o número, a série, a data, o valor e a situação. O arquivo da nota, o xis-ême-éle ou o dânfi, você manda pelo caminho de sempre, nas Notas Fiscais do sistema.
Nota cancelada continua na lista, marcada como Cancelada. Aqui, a da Serra Fina. Só chegam ao portal as notas autorizadas e as canceladas: nota rejeitada ou ainda em digitação não aparece.
Já o Relatório soma os pedidos do parceiro, material por material.
Na cooperativa, eu escolho o mês passado. Em outubro, foram oito mil e quatrocentos quilos de papelão e dois mil e seiscentos de pét, entre outros.
No total, dezoito mil setecentos e cinquenta e cinco reais.
Dá pra filtrar por material, e o período tem outras opções, como o Personalizado, pra escolher as datas do seu jeito.
Pedido estornado fica fora do relatório. E o pedido sem valor entra só com o peso, sem o dinheiro.
No Baixar pê-dê-éfe, o relatório abre pronto pra salvar. E se você não quiser mostrar os valores aqui, é só desligar Mostrar valores, na aba Portal.""",
10: """Seu fornecedor vive perguntando quanto está o material? Dá pra mostrar a tabela de preços no portal dele. É a única aba que nasce oculta, pra ninguém ver preço sem você decidir.
Na cooperativa, eu mudo de Oculto pra Com senha, e salvo.
No portal, apareceu a aba Preços. Primeiro, os materiais que a cooperativa já entrega. Depois, os outros que a Recicla Vale compra.
E o aviso protege você: os valores podem mudar, e vale o preço do momento da pesagem.
No Baixar em pê-dê-éfe, ela leva a tabela pronta.
Uma dica: cada fornecedor vê o preço dele. Se a cooperativa tem preço combinado ou uma tabela própria, é esse que aparece, sem nenhuma marca de preço especial. E essa aba só existe no cadastro de fornecedor.""",
11: """A aba Coletas é do módulo de coletas, que também depende do plano contratado. Com ela, a cooperativa pede a coleta sozinha e acompanha as que já tem.
Essa semana, o galpão dela encheu antes de sexta. Então ela clica em Solicitar coleta.
Ela escreve o material, papelão e pét prensados, e a quantidade, uns dois mil e quinhentos quilos.
Escolhe o dia que prefere, quinta de manhã. O endereço já vem do cadastro, e se a coleta for em outro lugar, ela troca ali mesmo. E nas observações, onde estão os fardos.
Solicitar coleta, e pronto. O pedido entra como Solicitada.
E no sistema, o aviso chega no sino: nova solicitação de coleta.
A cooperativa sugeriu o dia, mas quem confirma o dia, o horário, o motorista e o caminhão é a Recicla Vale, na tela de Coletas. Isso fica pro tutorial de Coletas e Logística.
Quando a coleta é concluída, o cartão vira um atalho. Em Ver relatório da coleta, ela vê o que foi recolhido e entregue, e volta pelo Voltar ao portal. E se você recusar ou cancelar um pedido, ela vê o motivo no cartão.
Uma dica: se ela escolher um dia que a Recicla Vale não atende, ou pedir em cima da hora, o portal explica o motivo e pede outra data. E se você tirar a exigência de aprovação, o pedido já entra como Agendada. Essas regras ficam nas Configurações de Coletas.""",
12: """E se a cooperativa precisar do comprovante de uma entrega? Ela mesma imprime, aqui na impressora do pedido.
Abre o comprovante em á-quatro, como a gente escolheu na aba Portal, com os materiais, os pesos e os valores da entrega.
E como esse pedido tem fotos, o comprovante sai com um quê-érre côde: Escaneie para ver fotos.
Num pedido com o Comprovante sem valores, o papel sai sem os preços, igual ao portal. O valor nem passa pelo navegador do parceiro.
Se a sua empresa imprime linha de assinatura no comprovante, ela sai aqui também, do jeito que você escolheu nas Configurações, em Usabilidade. No celular, se o navegador bloquear a janela, o comprovante abre por cima do portal.""",
13: """Em vez de esperar o parceiro abrir o portal, você pode mandar o pedido pra ele. Nos Pedidos, no menu da compra, tem o Enviar pelo uatsápe.
O uatsápe abre com a mensagem pronta, no telefone do cadastro: o número do pedido, a data, o valor e o link.
E esse link já abre o portal em cima daquele pedido, com os materiais e, se o pedido tiver, as fotos.
Uma dica: precisa do telefone no cadastro do parceiro. Num pedido com Comprovante sem valores, a mensagem avisa que o cupom é sem valor, e não mostra o total. O mesmo botão aparece no histórico da ficha do parceiro.""",
14: """Agora, as fotos. Elas entram na compra ou na venda, em Opções avançadas, no Anexar. Dá pra escolher várias de uma vez, e tirar uma foto errada no X antes de salvar. Precisa estar com internet, e vale também no Ticket de Pesagem. Depois, nos Pedidos, o Ver fotos anexadas mostra as fotos daquela linha.
E quem aponta o celular pro quê-érre côde do comprovante cai numa página só com as fotos daquele pedido.
É essa página. Em cima, a Recicla Vale e o número do pedido. Embaixo, as fotos da carga.
Dá pra passar de uma foto pra outra e abrir cada uma em tela cheia.
Em Dados do Pedido ficam o fornecedor, a data, os materiais e o total: três mil e setecentos reais. Se o pedido tiver motorista, placa ou observação, aparecem aqui também.
Uma dica: são dois links diferentes. O de fotos mostra só aquele pedido. O do portal mostra o histórico inteiro do parceiro, então cuida mais dele.
E no comprovante que sai no caixa, o quê-érre côde leva o parceiro pro portal dele, já aberto naquele pedido.""",
15: """Pronto! Recapitulando: a gente viu o que o parceiro enxerga no portal e copiou o link da cooperativa na ficha.
Escolheu as abas e o comprovante em á-quatro, e protegeu o portal com usuário e senha.
Deixou o histórico do Depósito livre e o resto com senha, viu o portal de quem é cliente e fornecedor, conferiu o histórico, o saldo, que ficou em dia sozinho depois do pagamento, as notas e o relatório de outubro.
Liberou a tabela de preços pra cooperativa, que pediu uma coleta e imprimiu o comprovante.
Mandou um pedido pelo uatsápe, e as fotos do pedido abriram pelo link público.
No próximo tutorial, a matriz enxerga todas as unidades de uma vez. Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "O que o parceiro vê.",
           2: "Pegar o link do portal.",
           3: "Escolher as abas.",
           4: "Usuário e senha.",
           5: "Senha só no que é sensível.",
           6: "Cliente e fornecedor no mesmo portal.",
           7: "Histórico de pedidos.",
           8: "O saldo do parceiro.",
           9: "Notas e relatório.",
           10: "A tabela de preços do fornecedor.",
           11: "O parceiro pede a coleta.",
           12: "O comprovante do portal.",
           13: "Mandar o pedido pelo uatsápe.",
           14: "As fotos do pedido.",
           15: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "Portal",
           2: "Link",
           3: "Exibição",
           4: "Senha",
           5: "Senha",
           6: "Portal",
           7: "Histórico",
           8: "Saldo",
           9: "Notas e relatório",
           10: "Preços",
           11: "Coletas",
           12: "Comprovante",
           13: "Link",
           14: "Fotos",
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
