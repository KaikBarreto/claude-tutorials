# Texto enviado ao ElevenLabs (eleven_v4, voz Kaik Barreto) por capítulo do T17 "Transporte, serviço e o contador" (app 1.60.39 desde 28/11; era 1.60.10).
# Gerado do roteiro.md (coluna Fala): cada linha do texto é uma linha da tabela Tela × Fala. 21 capítulos (0 a 20) depois do 1.60.39
# (28/11): novo 11 (a NF-e recebida vira compra), renumerados 11..19 -> 12..20; trocadas cap00 L3, cap04 L7..L13, cap09 L5,
# cap12 L1 e L8, cap13 L1, cap17 (tela nova do Fiscal × operacional) e cap20 L2 (andamento_160.md). 18/11 (1.60.10): novos 6, 14 e 16.
# Trocas de pronúncia em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   Fiscal & Ambiental -> "Fiscal e Ambiental" | NFS-e -> "/ˈẽːniˈɛːfiˈɛːsiˈeː/" | NF-e -> "/ˈẽniˈɛfiˈe/" | MDF-e -> "/ˈẽmiˈdeˈɛfiˈe/" | SEFAZ -> "sefás" | PDF -> "pê-dê-éfe" | XML -> "xis-ême-éle" | ISS -> "/iˈɛsiˈɛːsːi/" | Kardex -> "cardécs" | truck -> "trúqui"
#   novas no 1.60.10 (TESTAR num trecho curto antes da voz): CFOP -> "cê-éfe-ó-pê" | NCM -> "ene-cê-ême" | CIOT -> "ciót" | ANTT -> "a-ene-tê-tê" | Carreta / Reboque -> "Carreta ou Reboque"
CAPS = {
0: """Oi! Neste tutorial a gente vai cuidar dos outros documentos da Recicla Vale Metais: o que acompanha a carga na estrada, o que cobra um serviço e o pacote que o contador pede todo mês.
Hoje sai um caminhão de alumínio pra Minas Gerais, a coleta com caçamba na Aços Quiririm vira cobrança, e outubro fecha com o contador.
Tudo isso fica no menu Fiscal e Ambiental: em Transporte, em Notas de Serviço e no Relatório e Estoque Fiscal.
Essas telas fazem parte do módulo de Notas Fiscais, então dependem do plano contratado.
Se você ainda não viu o tutorial da nota fiscal de mercadoria, dá uma olhada antes. [pause] Vamos começar pelo manifesto.""",
1: """O manifesto fica aqui, em Transporte, na aba Manifestos. A Recicla Vale ainda não emitiu nenhum.
Imagina o caminhão saindo com alumínio de duas vendas. Cada venda tem a sua nota fiscal. O manifesto, o /ˈẽmiˈdeˈɛfiˈe/, é o documento da viagem: ele junta as notas da carga, o caminhão e o motorista.
Ele é emitido antes de o caminhão sair e encerrado quando a viagem termina.
Aqui em cima, os cartões contam os manifestos autorizados, pendentes, rejeitados e encerrados.
Uma dica: quem precisa emitir o manifesto depende da operação e do estado. Confirme com a sua contabilidade, principalmente quando a carga atravessa estado. O sistema entrega a ferramenta, e quem interpreta a regra é o contador.""",
2: """Antes do primeiro manifesto, o caminhão e o motorista precisam estar na Frota. Os caminhões da Recicla Vale já estão aqui: é a mesma frota da pesagem.
Pro manifesto, faltam os dados de transporte do caminhão trúqui. Clico em Editar.
Ele é emplacado em São Paulo. No Tipo, é um veículo único, sem carreta. O rodado é trúqui, e a carroceria é aberta.
A tara, o peso do caminhão vazio, já veio da frota: seis mil trezentos e oitenta quilos. E ele leva até catorze mil quilos de carga.
Uma dica: peso aqui é sempre em quilos. Se o número parecer tonelada, a própria tela avisa.
Salvar, e o caminhão está pronto pro manifesto.
Agora o motorista. O Edson Moura já está na lista. Clico em Editar.
O manifesto leva o CPF do motorista, então eu completo o CPF, a CNH, a categoria e a validade.
Salvar. Caminhão e motorista prontos.""",
3: """Com a frota pronta, uma olhada nas Configurações do /ˈẽmiˈdeˈɛfiˈe/. Aqui ficam a série e o próximo número do manifesto.
A Recicla Vale nunca emitiu manifesto, então começa no número um. Se a sua empresa já emitia em outro sistema, é aqui que você continua a sequência.
E o caminhão e o motorista ficam na Frota, que a gente acabou de ver.
Agora, o percurso. Hoje o caminhão leva alumínio pra Serra Fina, em Itamonte, Minas Gerais.
Ele sai de Taubaté, passa pelo Rio de Janeiro e sobe pra Minas. São Paulo é a origem, Minas Gerais é o destino, e o Rio de Janeiro é o estado do meio do caminho.
O estado do meio do caminho vai no Percurso. E isso a gente preenche em cada manifesto, na hora de emitir.""",
4: """Hora de emitir. Clico em Novo /ˈẽmiˈdeˈɛfiˈe/, e o primeiro passo são as notas da carga.
Busco a Serra Fina e marco as duas notas de hoje: o alumínio perfil e o alumínio bloco. Juntas, dão cinquenta e cinco mil, trezentos e oitenta reais.
E quando o seu caminhão leva carga com nota de outra empresa? Por exemplo, buscar no fornecedor o material que você comprou. Aí a nota entra pela chave de acesso.
Colo os quarenta e quatro dígitos e clico em Adicionar. Como essa nota já estava nas Notas Recebidas, o sistema preencheu quem emitiu e o valor.
Se a nota não estiver lá, ela entra do mesmo jeito, só com a chave, e o valor você digita se quiser.
Hoje a carga é só da Recicla Vale, então eu tiro essa nota e sigo com as duas.
Continuar. Primeiro, a natureza da viagem: carga própria, porque a mercadoria é da Recicla Vale. E na categoria do transportador fica Próprio, porque o caminhão também é dela.
No veículo, o caminhão trúqui, e no motorista, o Edson. Como a Frota está completa, não falta nenhum dado.
Se o caminhão puxa carreta, ela entra aqui, em Reboques, até três. Pra isso, a carreta precisa estar na Frota como Carreta ou Reboque.
Embaixo fica o ciót e a contratação do frete. O ciót é um código exigido quando o transporte é pago: você contrata um caminhoneiro, ou leva a carga de outra empresa cobrando frete.
Nesse caso, a resposta aqui é Sim. Aí a tela pede o código do ciót, com doze dígitos, o CPF ou CNPJ de quem gerou o código, quem contratou o frete e o registro do transportador na a-ene-tê-tê.
O código é gerado antes da viagem, numa instituição autorizada pela a-ene-tê-tê. Na dúvida se a sua viagem precisa, pergunte ao contador.
Hoje a carga é da própria Recicla Vale, no caminhão dela, sem cobrar frete. Então fica no Não, e a tela confirma: o ciót não se aplica a esta viagem.
Continuar. A origem já vem com a cidade da empresa: Taubaté.
No Percurso, eu adiciono o Rio de Janeiro, o estado do meio do caminho.
E no destino, Minas Gerais, cidade de Itamonte.
O peso já vem somado das notas: cinco mil e oitocentos quilos. E o valor da carga vem sugerido pelas notas. Se o valor real for outro, dá pra ajustar.
Embaixo ficam as observações, que saem impressas no papel do manifesto.
Na revisão, o jeito de emitir fica no Normal, que envia pra sefás na hora.
Uma dica: a contingência é só pra quando a sefás estiver fora do ar. Ela pede o motivo, o tipo de carga, o ene-cê-ême e o produto principal da carga.
Nesse caso, o motorista só sai com o manifesto impresso em papel. E o prazo pra regularizar com a sefás é de até cento e sessenta e oito horas, sete dias.
Hoje a sefás está no ar, então eu volto pro Normal.
Tudo pronto. Criar /ˈẽmiˈdeˈɛfiˈe/. O manifesto número um foi criado e já foi enviado pra autorização.
Pronto, autorizado. Na linha aparecem o motorista, a placa, o trajeto, o valor e o peso.
E pelo menu de ações você baixa o pê-dê-éfe do manifesto, que vai com o motorista na viagem.""",
5: """À tarde, a carga foi entregue em Itamonte. Agora falta encerrar o manifesto.
Uma dica: encerrar não é cancelar. Encerrar é o fim normal da viagem. Cancelar é anular um manifesto que não deveria existir, e tem prazo curto.
Olha o cancelamento: ele não tem volta, pede um motivo com pelo menos quinze letras, e o prazo costuma ser de vinte e quatro horas depois da autorização.
Não é o caso aqui. Voltar.
No menu de ações, Encerrar. O pedido vai pra sefás, e o selo mostra que o encerramento foi enviado.
Pronto, encerrado. A viagem está fechada, e o manifesto passa a contar nos encerrados.""",
6: """E quando a sefás não aceita? Olha o manifesto número dois, da viagem de amanhã: ele ficou como rejeitado, e conta aqui em cima, nos rejeitados.
No menu de ações, Ver Erro. O sistema mostra o motivo. Aqui, o CPF do motorista está errado.
Fechar. No mesmo menu ficam Reemitir e Excluir.
Se a recusa foi uma falha de momento, é só Reemitir. Se o erro está num dado do manifesto, o caminho é excluir, corrigir o cadastro na Frota e criar outro.
E se a sefás recusar um encerramento ou um cancelamento, o manifesto continua valendo. É só ver o erro e pedir de novo.
Pra achar um manifesto antigo, tem a busca por número, placa ou motorista. E clicando na linha, abrem os detalhes dele.""",
7: """Agora, a nota de serviço. Ela fica em Notas de Serviço.
Pensa assim: quando a Recicla Vale vende sucata, a mercadoria sai do pátio. A nota dessa venda é a nota fiscal de mercadoria, a /ˈẽniˈɛfiˈe/.
Quando ela cobra um trabalho, como a coleta com caçamba, não sai mercadoria nenhuma. Essa é a nota de serviço, a /ˈẽːniˈɛːfiˈɛːsiˈeː/, que é da prefeitura.
Na lista ficam as notas de serviço emitidas: o número, quem contratou, que aqui se chama tomador, o valor e o status.
E os dados da empresa que a nota de serviço usa, como a inscrição municipal, ficam nas Configurações Fiscais. Quem confere esses dados é o contador.""",
8: """Vou cobrar a coleta com caçamba que a Recicla Vale fez na Aços Quiririm. Nova /ˈẽːniˈɛːfiˈɛːsiˈeː/.
Na data de competência vai o dia do serviço: seis de novembro. A série e o próximo número já aparecem aqui: esta vai ser a catorze.
No tomador, quem contratou, eu escolho a Aços Quiririm no cadastro. Se ele não tiver cadastro, dá pra buscar pelo CNPJ.
Avançar. O município já vem como Taubaté. O código do serviço é o seu contador que passa. Aqui, coleta e remoção de resíduos.
Se a empresa emite sempre o mesmo serviço, ele pode ficar salvo, e aí é só puxar por aqui.
Na descrição, o que foi feito, do jeito que vai aparecer na nota.
Avançar. O valor do serviço: mil oitocentos e cinquenta reais.
Na alíquota do /iˈɛsiˈɛːsːi/, eu coloco três por cento, o número da lista do município. Quem confirma esse número é o contador.
Repara nestas opções. Se quem contratou é quem recolhe o /iˈɛsiˈɛːsːi/, você liga o /iˈɛsiˈɛːsːi/ retido na fonte. E embaixo ficam as retenções federais, em reais: o valor que o cliente descontou de cada imposto.
Isso acontece bastante quando o cliente é empresa, como a Aços Quiririm, que está no Lucro Real. Se tem retenção e de quanto, quem diz é o contador. Nesta nota não tem, então fica tudo zerado.
Na pré-visualização, a nota aparece como vai sair, já com a série e o número. E o selo mostra que ela está pronta pra emitir.
Se ainda faltar alguma informação do contador, dá pra salvar o rascunho e continuar depois.
Emitir /ˈẽːniˈɛːfiˈɛːsiˈeː/. Ela foi enviada, e entra na lista como processando.
E em instantes fica autorizada: nota de serviço número catorze.
Pelo menu, você baixa o pê-dê-éfe pra mandar pra Aços Quiririm, acompanha tudo no Histórico e, se a nota saiu errada, pede o cancelamento.""",
9: """E quando é a Recicla Vale que contrata um serviço? A nota chega em Notas Fiscais, nas Notas Recebidas, na aba /ˈẽːniˈɛːfiˈɛːsiˈeː/.
São as notas que outras empresas emitem contra o seu CNPJ: o contador, a manutenção, um frete. Elas entram aqui sozinhas, prontas pra virar despesa.
Clico em Ativar /ˈẽːniˈɛːfiˈɛːsiˈeː/ Recebidas. Repara no aviso: cada nota recebida conta na cota mensal de documentos fiscais, a mesma das notas que você emite.
Ativar mesmo assim. Pronto, ativado. A busca roda sozinha, e as notas chegam em alguns minutos.
Uma dica: só chega aqui a nota de cidade que já entrou no sistema nacional. Se uma nota não aparecer, peça o xis-ême-éle ao prestador: ela entra pelo Importar xis-ême-éle, que a gente vê daqui a pouco.""",
10: """Um pouco depois, chegaram duas notas.
Os honorários do escritório de contabilidade, de mil seiscentos e cinquenta reais, e a aferição da balança rodoviária, de novecentos e oitenta.
Aqui em cima aparece quando foi a última busca. E se você quiser adiantar, é só clicar em Sincronizar agora.
Serviço não entra no estoque, então aqui o caminho é a despesa. Na linha da balança, Lançar despesa ou conta.
A conta já vem com o valor e os dados da nota. Falta o vencimento, dia vinte, e a categoria. Criar conta. E a nota fica marcada como lançada.
Se você tentar lançar a mesma nota de novo, o sistema avisa antes, pra despesa não entrar duas vezes.""",
11: """E a nota de mercadoria que chega de um fornecedor? No tutorial anterior, a gente importou o xis-ême-éle da Cooperativa Recomeço. A carga de latinha e PET chegou ontem, e a compra ainda não foi lançada.
Ela entrou por este Importar xis-ême-éle. Por ele entra também a nota de serviço de uma cidade que ainda não está no sistema nacional. Com o recurso ativo, ela vai pra aba de serviço e vira despesa como as outras.
Serviço vira despesa, mercadoria vira compra. Na linha da cooperativa, Lançar compra.
Em cima, a conferência separa o que veio dos produtos, os encargos e descontos, como frete e impostos, e o total da nota. Aqui não tem encargo: sete mil quinhentos e cinquenta reais.
Os itens já vêm casados com os materiais, como a gente viu no tutorial anterior: a latinha e o PET.
Repara nesta opção, que já vem marcada: registrar também no estoque fiscal. A nota entra no estoque pelas notas, e o estoque do pátio fica por conta da compra.
Conferir na tela de compra. Os itens chegam prontos, sem redigitar a nota: oitocentos e cinquenta quilos de latinha e mil e duzentos de PET.
Aqui você confere os valores e escolhe como pagou. A Recicla Vale pagou por Pix. Finalizar, Pix, e confirmo o pagamento.
De volta às notas recebidas, a nota fica marcada como lançada como compra. Se alguém tentar lançar de novo, o sistema avisa antes, pra mesma nota não entrar duas vezes no estoque.""",
12: """Antes de mandar o mês pro contador, vale conferir os números. No menu, em Relatório e Estoque Fiscal, fica a aba /ˈẽniˈɛfiˈe/, das notas de mercadoria. Escolho o mês passado, outubro.
Aqui em cima, o que entrou e o que saiu em notas no mês.
O saldo é a saída menos a entrada. Em outubro, ficou positivo: setenta e um mil, seiscentos e vinte e cinco reais.
E o último cartão junta as notas pendentes e as rejeitadas. Aqui está tudo em dia. Se aparecer um número, resolve antes de fechar o mês.
Clicando na Entrada, ela se abre. Em outubro, as nove notas foram emitidas pela própria Recicla Vale, nas compras de pessoa física. As notas que os fornecedores emitem contra ela aparecem aqui, numa linha separada.
No Lucro Real, é nessas notas de fornecedor que o contador costuma buscar os créditos de imposto.
Embaixo, o gráfico do mês, a divisão por status e o ranking dos fornecedores e dos clientes.
A aba do lado, /ˈẽːniˈɛːfiˈɛːsiˈeː/, é o mesmo relatório pras notas de serviço: quanto foi autorizado, o /iˈɛsiˈɛːsːi/ do período e as retenções.
E embaixo, quem mais contratou e quais serviços mais saíram.""",
13: """Agora, o estoque fiscal: o estoque contado só pelas notas. Ele fica na mesma tela, na primeira aba, Saldo atual, com o saldo fiscal de cada material.
Esse saldo se atualiza sozinho. As notas do alumínio que saíram hoje de manhã já estão descontadas aqui.
Pra achar um material, é só buscar pelo nome ou pelo código.
Se algum saldo aparecer em vermelho, é porque ficou negativo: saiu mais nota do que entrou.
Repara no aviso amarelo: tem material sem saldo inicial. Nesse caso, o sistema conta só pelas notas que ele conhece.""",
14: """Quando a empresa começa a usar o sistema, ela já tem material no pátio. Esse ponto de partida é o saldo inicial. Aqui, falta o da bateria. Na linha dela, Informar saldo inicial.
Escolho a data-base, que é o dia em que esse número valia: trinta e um de outubro. E a quantidade: três mil trezentos e vinte quilos.
Uma dica: esse número é fiscal. No Lucro Real, o estoque entra no balanço, então combine o valor com o contador.
Pra informar vários materiais de uma vez, tem a planilha: você baixa o modelo, preenche código e quantidade e envia. O sistema confere linha por linha antes de gravar.
Confirmar saldo inicial. O aviso amarelo some, e daqui pra frente as notas somam e descontam a partir desse saldo.
A bateria passa a três mil novecentos e sessenta quilos: o saldo inicial mais a nota que entrou em novembro.""",
15: """Pra ver um dia do passado, a aba é a Posição em uma data. Escolho a data e a hora, aqui o fim de outubro, e clico em Ver posição.
É o número que o contador costuma pedir no fechamento do mês e do ano.
Uma dica: essa posição é só consulta. Ela não muda saldo, nota nem o estoque de hoje. E a data é sempre do passado.
Em Movimentações fica o cardécs fiscal. Escolho o metal amarelo: cada linha é uma nota, com o cê-éfe-ó-pê, a quantidade e o saldo antes e depois.
Nos filtros, dá pra fechar num período, num tipo de movimento, ou buscar por nota, chave ou parceiro.
E em Geral aparecem as movimentações de todos os materiais juntas.""",
16: """E quando uma nota é cancelada? Lembra da nota mil duzentos e quarenta e nove, cancelada hoje cedo? Eu busco por ela aqui, nos filtros.
A saída de trezentos e vinte quilos continua no cardécs, e logo acima entra o estorno, com o motivo do cancelamento.
O sistema não apaga a nota. Ele devolve a quantidade na hora em que o cancelamento aconteceu. Assim, uma posição consultada entre os dois momentos mostra o saldo como era.
O mesmo vale pra nota de fornecedor que foi cancelada depois de chegar: ela sai do saldo sozinha.
E a devolução? A Fundição Bandeira do Vale devolveu quarenta quilos de cobre mel. A nota de devolução, a mil duzentos e cinquenta e três, entra no estoque fiscal como entrada.
Devolução de venda, o material volta. Devolução de compra, o material sai. E vale igual pra dentro e pra fora do estado.
Uma dica: no Lucro Real, a devolução também mexe nos impostos da nota original. Essa parte é com o contador. Aqui você confere a quantidade.""",
17: """Agora, a aba que compara o fiscal com o operacional: as notas e os pedidos ficam lado a lado, material por material. Escolho o mês passado, outubro.
Aqui em cima, o sistema separa as entradas e as saídas: quantos materiais deram diferença nas compras, quantos nas vendas, quantos conferem e os alertas.
Repara no metal amarelo. Nas entradas, quinhentos quilos comprados e nenhuma nota: a tela marca sem nota.
É o caso mais comum no ferro-velho: compra de pessoa física sem nota. O material entra no pátio, mas não entra no fiscal.
Nas saídas, seiscentos quilos de nota a mais. Foi uma venda pra Fundição Bandeira do Vale: a nota saiu no dia trinta de outubro, mas o pedido só foi finalizado no dia três de novembro.
O fiscal segue as notas. O operacional segue as compras, os pedidos e o pátio. Por isso, os dois podem dar diferente.
Uma dica: um não corrige o outro. Este quadro, Como ler a diferença, ajuda a achar o motivo de cada caso.
E dá pra exportar essa comparação em pê-dê-éfe ou em Excel e mandar junto pro contador.""",
18: """Agora, o pacote que o contador pede todo mês. Ele fica em Notas Fiscais, no botão de três pontinhos: Exportação Contábil.
Ele junta num arquivo só os xis-ême-éle das notas, uma planilha e um pê-dê-éfe de resumo.
Se a empresa tem mais de um CNPJ, dá pra gerar um pacote pra cada um.
No período, o mês passado.
Aqui tem uma opção importante pra quem está no Lucro Real: incluir as notas que os fornecedores emitiram contra o seu CNPJ. É com o xis-ême-éle delas que o contador aproveita os créditos.
Saída e entrada, e todos os status, já vêm marcados. Assim o contador recebe o mês inteiro.
Nos extras, entram também o pê-dê-éfe de cada nota e os manifestos do período.
A prévia conta vinte e uma notas em outubro: doze de saída e nove de entrada. E as destinadas vêm zeradas, porque em outubro a Recicla Vale ainda não recebia essas notas pelo sistema. No pacote de novembro, elas já entram.
Baixar Pacote. Ele monta tudo aqui no navegador e baixa o arquivo zip no computador.""",
19: """E o que vai dentro dele? Pastas com os xis-ême-éle de saída e de entrada, o pê-dê-éfe de cada nota, a planilha com a relação das notas, o resumo em pê-dê-éfe e, se você marcou, as notas dos fornecedores.
Você manda o pacote pro contador do jeito que vocês já combinam, por e-mail ou numa pasta compartilhada.
Com ele, o contador confere as notas do mês, lança na contabilidade e te chama se alguma coisa não bater.
Uma dica: guardar os xis-ême-éle é responsabilidade da empresa, e não do sistema. Baixe o pacote todo mês e guarde uma cópia com você, além da que fica com o contador.""",
20: """Pronto! Recapitulando: a gente completou a frota com o caminhão e o motorista, emitiu o manifesto da carga de alumínio pra Minas, com o Rio de Janeiro no percurso, encerrou no fim da viagem e viu o que fazer quando a sefás recusa.
Emitiu a nota de serviço da coleta com caçamba, ativou as notas de serviço recebidas, lançou uma delas como despesa e levou a nota da cooperativa até a compra.
Conferiu os relatórios fiscais de outubro, informou um saldo inicial, viu o cancelamento e a devolução no cardécs, comparou o estoque fiscal com o do pátio e exportou o pacote do mês pro contador.
No próximo tutorial, a gente cuida da parte que mantém a licença da sua empresa de pé. Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "O que é o /ˈẽmiˈdeˈɛfiˈe/.",
           2: "Veículo e motorista.",
           3: "Numeração e percurso.",
           4: "Emitir o manifesto.",
           5: "Encerrar no fim da viagem.",
           6: "Quando o manifesto não passa.",
           7: "A nota de serviço.",
           8: "Emitir e acompanhar.",
           9: "O serviço que você tomou.",
           10: "Da nota recebida à despesa.",
           11: "Da nota recebida à compra.",
           12: "Entrada, saída e saldo.",
           13: "O estoque pelas notas.",
           14: "O saldo inicial.",
           15: "Um dia do passado e as movimentações.",
           16: "Cancelamento e devolução.",
           17: "Fiscal e operacional.",
           18: "O pacote do mês.",
           19: "O que o contador faz.",
           20: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "Transporte",
           2: "Frota",
           3: "Transporte",
           4: "Manifesto",
           5: "Manifesto",
           6: "Manifesto",
           7: "Serviço",
           8: "Serviço",
           9: "Serviço",
           10: "Serviço",
           11: "Compra",
           12: "Relatório fiscal",
           13: "Estoque fiscal",
           14: "Estoque fiscal",
           15: "Estoque fiscal",
           16: "Estoque fiscal",
           17: "Estoque fiscal",
           18: "Contador",
           19: "Contador",
           20: "Resumo"}

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
