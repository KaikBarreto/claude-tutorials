# Texto enviado ao ElevenLabs (eleven_v4, voz Kaik Barreto) por capítulo do T17 "Transporte, serviço e o contador".
# Gerado do roteiro.md (coluna Fala): cada linha do texto é uma linha da tabela Tela × Fala.
# Trocas de pronúncia em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   Fiscal & Ambiental -> "Fiscal e Ambiental" | NFS-e -> "ene-éfe-ésse-ê" | NF-e -> "ene-éfe-ê" | MDF-e -> "ême-dê-éfe-ê" | SEFAZ -> "sefás" | PDF -> "pê-dê-éfe" | XML -> "xis-ême-éle" | ISS -> "i-ésse-ésse" | Kardex -> "cardécs" | truck -> "trúqui"
CAPS = {
0: """Oi! Neste tutorial a gente vai cuidar dos outros documentos da Recicla Vale Metais: o que acompanha a carga na estrada, o que cobra um serviço e o pacote que o contador pede todo mês.
Hoje sai um caminhão de alumínio pra Minas Gerais, a coleta com caçamba na Aços Quiririm vira cobrança, e outubro fecha com o contador.
Tudo isso fica no menu Fiscal e Ambiental: em Transporte, em Notas de Serviço e no Estoque Fiscal.
Essas telas fazem parte do módulo de Notas Fiscais, então dependem do plano contratado.
Se você ainda não viu o tutorial da nota fiscal de mercadoria, dá uma olhada antes. [pause] Vamos começar pelo manifesto.""",
1: """O manifesto fica aqui, em Transporte, na aba Manifestos. A Recicla Vale ainda não emitiu nenhum.
Imagina o caminhão saindo com alumínio de duas vendas. Cada venda tem a sua nota fiscal. O manifesto, o ême-dê-éfe-ê, é o documento da viagem: ele junta as notas da carga, o caminhão e o motorista.
Ele é emitido antes de o caminhão sair e encerrado quando a viagem termina.
Aqui em cima, os cartões contam os manifestos autorizados, pendentes, rejeitados e encerrados.
Uma dica: quem precisa emitir o manifesto depende da operação e do estado. Confirme com a sua contabilidade, principalmente quando a carga atravessa estado. O sistema entrega a ferramenta, e quem interpreta a regra é o contador.""",
2: """Antes do primeiro manifesto, o caminhão e o motorista precisam estar na Frota. Os caminhões da Recicla Vale já estão aqui: é a mesma frota da pesagem.
Pro manifesto, faltam os dados de transporte do caminhão trúqui. Clico em Editar.
Ele é emplacado em São Paulo. No Tipo, é um veículo único, sem carreta. O rodado é trúqui, e a carroceria é aberta.
A tara é o peso do caminhão vazio: sete mil e oitocentos quilos. E ele leva até catorze mil quilos de carga.
Uma dica: peso aqui é sempre em quilos. Se o número parecer tonelada, a própria tela avisa.
Salvar, e o caminhão está pronto pro manifesto.
Agora o motorista. O Edson Moura já está na lista. Clico em Editar.
O manifesto leva o CPF do motorista, então eu completo o CPF, a CNH e a categoria.
Salvar. Caminhão e motorista prontos.""",
3: """Com a frota pronta, uma olhada nas Configurações do ême-dê-éfe-ê. Aqui ficam a série e o próximo número do manifesto.
A Recicla Vale nunca emitiu manifesto, então começa no número um. Se a sua empresa já emitia em outro sistema, é aqui que você continua a sequência.
E o caminhão e o motorista ficam na Frota, que a gente acabou de ver.
Agora, o percurso. Hoje o caminhão leva alumínio pra Serra Fina, em Itamonte, Minas Gerais.
Ele sai de Taubaté, passa pelo Rio de Janeiro e sobe pra Minas. São Paulo é a origem, Minas Gerais é o destino, e o Rio de Janeiro é o estado do meio do caminho.
O estado do meio do caminho vai no Percurso. E isso a gente preenche em cada manifesto, na hora de emitir.""",
4: """Hora de emitir. Clico em Novo ême-dê-éfe-ê, e o primeiro passo são as notas da carga.
Busco a Serra Fina e marco as duas notas de hoje: o alumínio perfil e o alumínio bloco. Juntas, dão cinquenta e cinco mil, trezentos e oitenta reais.
Continuar. No veículo, o caminhão trúqui, e no motorista, o Edson. Como a Frota está completa, não falta nenhum dado.
Continuar. A origem já vem com a cidade da empresa: Taubaté.
No Percurso, eu adiciono o Rio de Janeiro, o estado do meio do caminho.
E no destino, Minas Gerais, cidade de Itamonte.
O peso já vem somado das notas: cinco mil e oitocentos quilos. E o valor da carga também.
Na revisão, o jeito de emitir fica no Normal, que envia pra sefás na hora.
Uma dica: a contingência é só pra quando a sefás estiver fora do ar. Nesse caso, o motorista só sai com o pê-dê-éfe do manifesto impresso em papel.
Tudo pronto. Criar ême-dê-éfe-ê. O manifesto número um foi criado e já foi enviado pra sefás.
Pronto, autorizado. Na linha aparecem o motorista, a placa, o trajeto, o valor e o peso.
E pelo menu de ações você baixa o pê-dê-éfe do manifesto, que vai com o motorista na viagem.""",
5: """À tarde, a carga foi entregue em Itamonte. Agora falta encerrar o manifesto.
Uma dica: encerrar não é cancelar. Encerrar é o fim normal da viagem. Cancelar é anular um manifesto que não deveria existir, e tem prazo curto.
No menu de ações, Encerrar. O pedido vai pra sefás, e o selo mostra que o encerramento foi enviado.
Pronto, encerrado. A viagem está fechada, e o manifesto passa a contar nos encerrados.""",
6: """Agora, a nota de serviço. Ela fica em Notas de Serviço.
Pensa assim: quando a Recicla Vale vende sucata, a mercadoria sai do pátio. A nota dessa venda é a nota fiscal de mercadoria, a ene-éfe-ê.
Quando ela cobra um trabalho, como a coleta com caçamba, não sai mercadoria nenhuma. Essa é a nota de serviço, a ene-éfe-ésse-ê, que é da prefeitura.
Na lista ficam as notas de serviço emitidas: o número, quem contratou, que aqui se chama tomador, o valor e o status.
E os dados da empresa que a nota de serviço usa, como a inscrição municipal, ficam nas Configurações Fiscais. Quem confere esses dados é o contador.""",
7: """Vou cobrar a coleta com caçamba que a Recicla Vale fez na Aços Quiririm. Nova ene-éfe-ésse-ê.
Na data de competência vai o dia do serviço: sete de novembro. No tomador, quem contratou, eu escolho a Aços Quiririm no cadastro.
Avançar. O município já vem como Taubaté. O código do serviço é o seu contador que passa. Aqui, coleta e remoção de resíduos.
Se a empresa emite sempre o mesmo serviço, ele pode ficar salvo, e aí é só puxar por aqui.
Na descrição, o que foi feito, do jeito que vai aparecer na nota.
Avançar. O valor do serviço: mil oitocentos e cinquenta reais.
A alíquota do i-ésse-ésse veio da lista do município. Quem confirma esse número é o contador.
Na pré-visualização, a nota aparece como vai sair. E o selo mostra que ela está pronta pra emitir.
Emitir ene-éfe-ésse-ê. Ela entra na lista como processando.
E em instantes fica autorizada: nota de serviço número catorze.
Pelo menu, você baixa o pê-dê-éfe pra mandar pra Aços Quiririm e acompanha tudo no Histórico.""",
8: """E quando é a Recicla Vale que contrata um serviço? A nota chega em Notas Fiscais, nas Notas Recebidas, na aba ene-éfe-ésse-ê.
São as notas que outras empresas emitem contra o seu CNPJ: o contador, a manutenção, um frete. Elas entram aqui sozinhas, prontas pra virar despesa.
Clico em Ativar ene-éfe-ésse-ê Recebidas. Repara no aviso: cada nota recebida conta na cota mensal de documentos fiscais, a mesma das notas que você emite.
Ativar mesmo assim. Pronto, ele já buscou as notas, e chegaram duas.
Os honorários do escritório de contabilidade, de mil seiscentos e cinquenta reais, e a aferição da balança rodoviária, de novecentos e oitenta.
Uma dica: só chega aqui a nota de cidade que já entrou no sistema nacional. Se uma nota não aparecer, peça o pê-dê-éfe ao prestador e lance a despesa na mão.
Serviço não entra no estoque, então aqui o caminho é a despesa. Na linha da balança, Lançar despesa ou conta.
A conta já vem com o valor e os dados da nota. Falta o vencimento, dia vinte, e a categoria. Criar conta. E a nota fica marcada como lançada.""",
9: """Antes de mandar o mês pro contador, vale conferir os números. No Estoque Fiscal, a primeira aba é o Relatório fiscal. Escolho o mês passado, outubro.
Aqui em cima, o que entrou e o que saiu em notas no mês.
O saldo é a saída menos a entrada. Em outubro, ficou positivo: setenta e um mil, seiscentos e vinte e cinco reais.
E o último cartão junta as notas pendentes e as rejeitadas. Aqui está tudo em dia. Se aparecer um número, resolve antes de fechar o mês.
Embaixo, o gráfico do mês, a divisão por status e o ranking dos fornecedores e dos clientes.""",
10: """Agora, o estoque fiscal: o estoque contado só pelas notas. Na Posição do estoque, aparece o saldo fiscal de cada material, agora.
Pra ver um dia do passado, escolho a data e a hora, aqui o fim de outubro, e clico em Ver posição.
Uma dica: essa posição é só consulta. Ela não muda saldo, nota, movimentação nem o estoque de hoje. E a data é sempre do passado, nunca do futuro.
No Histórico fiscal fica o cardécs fiscal de cada material. Escolho o metal amarelo: cada linha é uma entrada ou uma saída, com o saldo antes e depois.
Na última aba, o fiscal e o operacional ficam lado a lado. Repara no metal amarelo: seiscentos quilos de diferença.
Foi uma venda pra Fundição Bandeira do Vale. A nota saiu no dia trinta de outubro, mas o pedido só foi finalizado no dia três de novembro.
O fiscal segue as notas. O operacional segue as compras, os pedidos e o pátio. Por isso, os dois podem dar diferente.
Uma dica: um não corrige o outro. Quando aparece diferença, este quadro, Como ler o Delta, ajuda a achar o motivo.""",
11: """Agora, o pacote que o contador pede todo mês. Ele fica em Notas Fiscais, no botão de três pontinhos: Exportação Contábil.
Ele junta num arquivo só os xis-ême-éle das notas, uma planilha e um pê-dê-éfe de resumo.
No período, o mês passado.
Saída e entrada, e todos os status, já vêm marcados. Assim o contador recebe o mês inteiro.
Nos extras, entram também o pê-dê-éfe de cada nota e os manifestos do período.
A prévia conta vinte e uma notas em outubro: doze de saída e nove de entrada.
Baixar Pacote. Ele monta tudo aqui no navegador e baixa o arquivo zip no computador.""",
12: """E o que vai dentro dele? Pastas com os xis-ême-éle de saída e de entrada, o pê-dê-éfe de cada nota, a planilha com a relação das notas e o resumo em pê-dê-éfe.
Você manda o pacote pro contador do jeito que vocês já combinam, por e-mail ou numa pasta compartilhada.
Com ele, o contador confere as notas do mês, lança na contabilidade e te chama se alguma coisa não bater.
Uma dica: guardar os xis-ême-éle é responsabilidade da empresa, e não do sistema. Baixe o pacote todo mês e guarde uma cópia com você, além da que fica com o contador.""",
13: """Pronto! Recapitulando: a gente completou a frota com o caminhão e o motorista, emitiu o manifesto da carga de alumínio pra Minas, com o Rio de Janeiro no percurso, e encerrou no fim da viagem.
Emitiu a nota de serviço da coleta com caçamba e lançou como despesa uma nota de serviço recebida.
Conferiu o relatório fiscal de outubro, comparou o estoque fiscal com o operacional e exportou o pacote do mês pro contador.
No próximo tutorial, a gente cuida da parte que mantém a licença da sua empresa de pé. Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "O que é o ême-dê-éfe-ê.",
           2: "Veículo e motorista.",
           3: "Numeração e percurso.",
           4: "Emitir o manifesto.",
           5: "Encerrar no fim da viagem.",
           6: "A nota de serviço.",
           7: "Emitir e acompanhar.",
           8: "O serviço que você tomou.",
           9: "Entrada, saída e saldo.",
           10: "O estoque pelas notas.",
           11: "O pacote do mês.",
           12: "O que o contador faz.",
           13: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "Transporte",
           2: "Frota",
           3: "Transporte",
           4: "Manifesto",
           5: "Manifesto",
           6: "Serviço",
           7: "Serviço",
           8: "Serviço",
           9: "Relatório fiscal",
           10: "Estoque fiscal",
           11: "Contador",
           12: "Contador",
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
