# Texto enviado ao ElevenLabs (eleven_v4, voz Kaik Barreto) por capítulo do T3 "Materiais e tabelas de preço".
# Gerado do roteiro.md (coluna Fala): cada linha do texto é uma linha da tabela Tela × Fala.
# Trocas de pronúncia em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   NCM -> "ene-cê-ême" | PDF -> "pê-dê-éfe" | CFOP -> "cê-éfe-ó-pê" | CST -> "cê-ésse-tê"
#   ICMS -> "/iˈseˈɛmiˈɛːsːi/" (IPA do PERFIL, provisório) | A4 -> "á-quatro" (nova); números já vêm por extenso no roteiro.
CAPS = {
0: """Oi! Neste tutorial a gente vai montar o cardápio da Recicla Vale Metais: cada material que entra no pátio, com o preço de compra e o preço de venda.
É desse cadastro que a compra, a venda e a nota fiscal puxam os dados. Por isso ele vem primeiro.
Tudo isso fica no menu Materiais, em Estoque.
Se você ainda não viu o tutorial Usuários e permissões, dá uma olhada antes. [pause] Vamos conhecer a tela.""",
1: """A tela tem quatro partes. Na coluna da esquerda ficam as tabelas de preço. Por enquanto, só a principal, com a estrela. Daqui a pouco a gente cria outra. O botão de interrogação, ali em cima, explica os tipos de tabela.
Em cima, os botões do dia a dia: Movimentar estoque, Editar Preços, Grupos, Exportar e Zerar Estoque. Cada um tem a sua vez neste tutorial.
Os três cartões resumem o pátio. O primeiro é o peso total em estoque.
O Total Pago é esse estoque vezes o preço médio que você pagou nas compras. E a Projeção de Vendas é o mesmo estoque vezes o preço de venda: quanto entraria se você vendesse tudo hoje.
Embaixo, a lista de materiais: o código, o nome, o estoque atual e os preços de cada um. O preço médio pago vem marcado como estimativa, porque é uma média das compras. Clicando no título de uma coluna, a lista ordena por ela.
Uma dica: quem não tem permissão de ver valores, como o Marcos, que é balanceiro, continua vendo os pesos. No lugar do dinheiro, aparece um cadeado.
Em cima da lista ficam o filtro, a importação por planilha, o botão Novo Material e a busca. É pelo Novo Material que a gente começa.""",
2: """Vamos cadastrar um material novo. A Recicla Vale começou a comprar radiador das oficinas, e ele ainda não está na lista.
A aba Produção aparece pra quem tem o módulo de produção no plano, e tem um tutorial só dela. Aqui a gente fica em Dados.
No nome, vai o jeito que a equipe fala no pátio: Radiador de cobre. A unidade já vem em quilo. Se o material for por peça ou por fardo, é só trocar aqui.
No preço de compra, vinte e um reais o quilo. No de venda, vinte e quatro e cinquenta.
Na quantidade em estoque vai o que já tem no pátio hoje: cento e vinte quilos. Se não tiver nada, deixa em zero, e as compras vão enchendo o saldo.
Do lado direito, o resumo mostra como o material vai ficar.
Criar, e pronto: material criado. Ele entra no fim da lista, e pra achar rápido é só buscar pelo nome.
E se você tem muitos materiais pra cadastrar, dá pra trazer todos de uma vez: baixa o modelo, preenche uma linha por material e envia a planilha.
Uma dica: a importação é tudo ou nada. Se uma linha tiver erro, nenhum material daquele arquivo entra; é só corrigir e mandar de novo. E se a internet cair no meio, pode mandar o mesmo arquivo: ele não duplica nada.""",
3: """Agora, o código. O radiador ganhou o dezesseis porque eu deixei o campo em branco: o sistema pegou o maior número da lista e somou um.
É o atalho do dia a dia: na compra e na venda, o operador digita o número e o material aparece.
Se você já tem os seus códigos, do caderno ou de outro sistema, pode usar os mesmos. No caderno do Rafael, o radiador sempre foi o setenta.
Abro o Editar e digito zero, sete, zero. Olha só: o zero da frente não fica.
Uma dica: o código é só número, e zero na frente não é guardado. Se no caderno era zero zero sete, aqui fica só o sete.
Ao lado do código fica o Prefixo, pra quem separa os materiais por letra. Digito pê, e a linha embaixo mostra pê setenta.
O prefixo aparece na tela, no comprovante e na nota fiscal. O número no banco não muda. Aqui eu não preciso dele, então apago.
Atualizar, e o radiador agora é o setenta. Cada número vale pra um material só: se ele já estiver em uso, o sistema avisa na hora de salvar.""",
4: """Pra quem emite nota fiscal, cada material precisa do ene-cê-ême. É um código de oito dígitos que diz pra Receita que mercadoria é aquela, e ele vai dentro da nota.
No cadastro, ele fica no campo ene-cê-ême. Dá pra digitar, ou clicar na interrogação do lado pra buscar.
A janela traz os códigos comuns da reciclagem. Busco cobre e escolho o de resíduos de cobre.
Uma dica: o ene-cê-ême certo de cada material é decisão do contador da empresa. A lista ajuda a achar rápido, mas quem confirma é a contabilidade.
Outro campo da nota é a Identificação, Produto Fiscal. Ele serve pra quando o nome que sai na nota é diferente do nome que vocês usam no pátio.
Por exemplo: latinha, perfil e bloco podem sair na nota como sucata de alumínio.
Uma dica: esse campo muda só a nota. A tela, os pedidos e os comprovantes continuam com o nome normal, de propósito: senão os três alumínios virariam linhas iguais.
No radiador, eu deixo vazio, e a nota sai com o nome normal. Atualizar.
No material, e na planilha de importação também, vão o ene-cê-ême e o nome da nota. Os impostos, como cê-éfe-ó-pê, cê-ésse-tê e /iˈseˈɛmiˈɛːsːi/, ficam nos cenários fiscais. Eles mudam conforme a operação, o regime da empresa e o parceiro, e quem define é o contador. Isso a gente vê no tutorial de nota fiscal.""",
5: """Agora, os grupos. A Recicla Vale já separa os materiais em cinco: ferrosos, cobre, alumínio, metais e outros.
Grupo é como uma gaveta: junta os materiais parecidos. Com o radiador vão chegar outros, de alumínio e misto, então vale uma gaveta nova.
No grupo novo vão o nome, a cor e o ícone. Escolho o carro, porque radiador sai de carro.
Adicionar, e o grupo está criado.
Agora é só pôr o radiador nele, no campo Grupo. E repara no botão de mais, do lado: por ele dá pra criar um grupo sem sair do cadastro.
Atualizar. O grupo aparece embaixo do nome, com a cor dele.
E por que agrupar ajuda? No filtro, deixo marcado só o cobre.
Os cartões lá em cima passam a mostrar o peso e o valor só do cobre que está no pátio. A exportação do estoque segue esse mesmo filtro.
Pra voltar, é só marcar Todos os Materiais.""",
6: """O preço da sucata mexe toda semana. Hoje, o cobre subiu cinquenta centavos o quilo, na compra e na venda. Em vez de abrir material por material, a gente usa o Editar Preços.
Ele abre em tela cheia. À esquerda ficam as tabelas, por enquanto só a principal. No meio, todos os materiais, com a compra e a venda lado a lado. À direita, o resumo da tabela. Pra fechar sem salvar, é o Sair ou o Cancelar.
Busco cobre, e ficam só os cobres.
No cobre mel, a compra vai pra quarenta e dois e cinquenta, e a venda pra quarenta e sete e noventa.
Faço o mesmo no cobre misto e no fio encapado. O radiador eu cadastrei hoje, já no preço novo, então ele fica como está.
As células alteradas ganham uma marca, e o aviso lá embaixo conta três materiais com alteração.
Uma dica: se a venda ficar menor que a compra, o sistema avisa. No bronze, ponho a venda em vinte e oito, abaixo dos vinte e nove da compra. O resumo, à direita, já conta um material com a venda abaixo da compra.
Se eu clicar em Salvar, ele pergunta antes, porque isso registra prejuízo nesse material. Quase sempre é erro de digitação, então eu cancelo e volto a venda pra trinta e três e cinquenta. Se for de propósito, é só confirmar em Salvar mesmo assim.
Agora, Salvar. Os preços novos já valem pra próxima compra e pra próxima venda. O aviso fala das tabelas vinculadas: elas acompanham sozinhas, e a gente já chega nelas. Antes, uma novidade do Editar Preços: a margem automática.""",
7: """Toda vez que a compra de um material muda, a venda precisa acompanhar, e fazer isso na mão, linha por linha, dá trabalho. A margem automática resolve: o sistema amarra a venda à compra por uma margem. Ela fica no Editar Preços, num cartão na coluna da direita.
Ligo a chave. Primeiro, o alcance: Tabela toda, com uma margem só pra todos os materiais, ou Por material, que a gente vê no próximo capítulo. Escolho Tabela toda.
A margem é sempre sobre a compra: dez reais de compra com trinta por cento viram treze reais de venda. Aqui eu ponho quinze por cento. Do lado, o botão de reais troca pra margem em reais por quilo.
Falta dizer qual preço fica como está. Se for a compra, a venda é recalculada. Se for a venda, é a compra que se ajusta. Deixo a compra e clico em Aplicar.
Pronto: a venda de todos os materiais foi recalculada. O cobre misto, de compra a trinta e seis reais, vai pra quarenta e um e quarenta de venda. Os preços guardam até três casas decimais, então alguns materiais mostram o milésimo. E lá embaixo o aviso lembra: a margem também tem alteração pendente.
Agora, o dia a dia. Se a compra do cobre misto for pra trinta e oito, a venda acompanha sozinha: quarenta e três e setenta.
E o contrário também funciona. Se eu digito a venda, quarenta e seis reais, é a compra que se ajusta: quarenta reais.
Pra mudar a margem de todo mundo, abro o Editar margem e troco o quinze por vinte. A venda de todos os materiais que seguem a tabela é recalculada na hora.
E um material pode fugir da regra. O ferro misto sempre teve margem maior, então abro o cadeado dele e ponho quarenta por cento. O selo diz personalizada, e os outros seguem a margem da tabela. Fechando o cadeado de novo, ele volta a seguir a tabela.
Uma dica: nada disso vale até clicar em Salvar. Como aqui é só demonstração, eu clico em Cancelar. Salvando, a margem fica gravada na tabela, e da próxima vez que você abrir o Editar Preços ela já vem ligada.""",
8: """Nem todo material tem a mesma margem: o ferro rende uma coisa, o cobre outra. Pra isso, o outro alcance: Por material. Abro o Editar Preços e ligo a chave.
O cartão pergunta em que unidade manter a margem que cada material já tem hoje: porcentagem ou reais. Deixo em porcentagem e clico em Aplicar. Repara que nenhum preço muda.
A coluna Margem passa a mostrar a margem de cada um. O cobre mel está em doze e setenta e um por cento, e o ferro misto, em quarenta.
Cada margem dá pra editar. No cobre misto, que está em quinze e vinte e oito, ponho quinze: a venda vai pra quarenta e um e quarenta.
A margem também pode ser em reais por quilo. No bronze, clico no botão de reais da linha, e o sistema converte: quatro e cinquenta por quilo, a mesma diferença de antes. Se eu digito cinco reais, a venda vira trinta e quatro.
E se a compra do bronze for pra trinta, a venda vai pra trinta e cinco: a compra mais os cinco reais.
Pra dar a mesma margem a vários materiais, busco alumínio e abro o Editar margem. Em Mesma margem em vários materiais, digito vinte, e o botão diz Aplicar em três materiais exibidos: só esses três mudam. Sem busca, ele aplicaria em todos.
Uma dica: desligar a chave desfaz só a configuração da margem; os preços que você já mexeu ficam como estão até salvar ou cancelar. Aqui eu só mostro, então clico em Cancelar. E se uma tabela independente com margem for vinculada à principal, a margem dela é desligada, porque a vinculada segue os preços da principal.""",
9: """Quando a margem já está gravada, o Editar Preços abre com ela ligada: o cartão diz Por material, cada material com a sua margem sobre a compra. E o resumo, à direita, conta como a tabela está.
Venda abaixo da compra conta os materiais que você vende por menos do que paga. Quando tem algum, fica vermelho. Vou provocar um: no bronze, ponho a margem em menos cinco por cento. A venda cai abaixo da compra, e o resumo já avisa.
Sem preço conta os materiais sem compra e sem venda, comuns depois de importar uma planilha. Zerando a compra e a venda do plástico PET, ele entra aqui. Esses números também viram filtros: clicando neles, a lista mostra só aqueles materiais.
Margem típica é a do meio da tabela: metade dos materiais tem margem acima dela, e metade abaixo.
Tem também o Fora da margem. Esse selo aparece quando o preço de um material não bate mais com a margem dele. Acontece quando o preço entra por outro caminho: a planilha, o Cato ou as filiais gravam o preço sem recalcular pela margem.
No alumínio latinha, a margem é de dezenove e trinta e cinco por cento, mas a venda está em sete e oitenta. Clicando no selo fora da margem, o sistema recalcula a venda pela compra: ela volta pra sete e quarenta. Aqui eu só mostro, então cancelo.""",
10: """A margem também aparece no cadastro do material. Abro o radiador pelo Editar. Como a tabela Principal está com a margem automática ligada, a compra e a venda ficam amarradas aqui também, e uma linha embaixo avisa.
Do lado do preço de venda tem uma calculadora: Calcular venda pela margem. Ponho vinte por cento, e a janela mostra a conta: compra de vinte e um reais, venda de vinte e cinco e vinte. Aplicar.
Agora a margem do radiador é essa. Mudo a compra pra vinte e dois, e a venda vai junto, sozinha: vinte e seis e quarenta.
Na calculadora tem ainda o Tirar a margem deste material, que deixa ele sem margem. E, quando a margem é da tabela toda, o Voltar à margem da tabela.
Uma dica: a calculadora só aparece quando a tabela tem a margem automática ligada. No Novo Material vale a da principal. Eu não vou salvar, então fecho em Cancelar; clicando em Atualizar, a margem do radiador fica gravada junto com os preços.""",
11: """A maioria dos pátios trabalha só com a tabela principal. Mas a Recicla Vale paga um pouco mais pros depósitos, que trazem material separado e em volume. Uma dica: se a coluna de tabelas não aparece pra você, ligue Múltiplas Tabelas de Preço em Configurações, Usabilidade.
Então, Nova Tabela, com o nome Tabela Depósitos. Marco Vincular à tabela principal e ponho quatro por cento a mais.
O exemplo embaixo mostra a conta: o que custa dez reais na principal sai por dez e quarenta nesta tabela.
Vinculada quer dizer que ela acompanha a principal sozinha: quando o preço muda lá, como a gente fez com o cobre, muda aqui também.
Criar Tabela. Com ela selecionada, a lista mostra o preço dos depósitos: o cobre mel sai a quarenta e quatro e vinte. O preço de venda, nesta tela, continua o da principal.
Dá pra ver como a tabela é montada no Editar Preços. Escolho a Tabela Depósitos na lista da esquerda, e a grade ganha a coluna Variação, com um cadeado em cada material. Fechado, o material segue os quatro por cento. Abrindo o do fio de cobre encapado, ele ganha uma variação só dele, em porcentagem ou em reais, e os outros continuam na regra.
Repara que o cartão da margem automática não aparece aqui: tabela vinculada não tem margem própria, ela acompanha a principal. Se a principal usa margem, a vinculada sobe e desce junto. Na criação, dá pra variar em reais em vez de porcentagem, pra baixo em vez de pra cima, ou desmarcar o Vincular: aí é uma tabela independente, com os preços digitados um a um e, se quiser, a própria margem.
Agora, ligar a tabela a quem vende pra gente. Em Clientes e Fornecedores, abro o Depósito Irmãos Siqueira e clico em Editar.
Em Tabela de Preços Padrão, escolho a Tabela Depósitos e salvo. Agora toda compra do depósito já começa nessa tabela.
E quando um material tem mais de um preço possível, qual vale? Uma dica: essa é a dúvida clássica, então vale guardar a ordem. Primeiro, o preço personalizado daquele cliente ou fornecedor. Depois, a tabela escolhida no pedido. E por último, o preço do material.
Pra ver na prática, abro uma compra só pra olhar o preço; a compra em si fica pro tutorial de compra e venda. Escolho o depósito, e a tabela dele já vem selecionada.
No cobre mel, entra o preço da tabela: quarenta e quatro e vinte.
Já no bronze, o depósito tem um preço personalizado: trinta e cinquenta. Olha o aviso: Preço especial aplicado. O personalizado ganha da tabela. E se você trocar a tabela com itens já lançados, o sistema pergunta se atualiza os preços desses itens ou se vale só pros próximos. Isso a gente vê no tutorial de compra e venda.""",
12: """Cada tabela tem um menu nos três pontinhos. É por ele que você ajusta, copia, fixa ou apaga uma tabela.
Em Configurações, dá pra trocar o nome e a variação. Se os depósitos passarem a ganhar cinco por cento, é aqui que muda.
O Duplicar tabela cria uma cópia com os preços de hoje. Repara que a cópia não tem a corrente: ela nasce independente, e não acompanha mais a principal. Serve de ponto de partida pra uma tabela nova, que pode até ter a própria margem automática.
Como era só um exemplo, eu excluo a cópia. Uma dica: excluir tabela não tem volta, e a principal nunca pode ser excluída.
Agora, o Fixar. Ele vale só pro seu usuário: os seus pedidos e tickets novos passam a abrir nessa tabela, e os dos colegas continuam como estavam.
A ordem é esta: se o cliente ou fornecedor tem tabela no cadastro, vale a dele. Senão, a que você fixou. E se não fixou nenhuma, a principal.
O Rafael trabalha na principal, então eu removo.
Por último, Definir como principal da empresa. Os preços dessa tabela viram a base de tudo, a principal antiga fica guardada como independente e as vinculadas são recalculadas. É uma troca grande, pra quando a empresa muda a política de preço. Aqui eu só mostro e cancelo.""",
13: """O estoque normalmente se mexe sozinho, pelas compras e pelas vendas. Mas às vezes ele precisa de um ajuste na mão: na contagem de hoje, o radiador deu cento e dezoito quilos, e não cento e vinte.
Em Movimentar estoque, escolho Saída, o radiador e dois quilos. A janela mostra o antes e o depois: de cento e vinte pra cento e dezoito quilos.
Na observação, eu escrevo o motivo. Fica tudo no histórico do material, com quem fez e quando. Registrar saída.
Agora, transferir. Na desmontagem dos radiadores saíram oito quilos de ferro, das cintas e dos suportes. Esse peso entrou como radiador, mas é ferro misto.
Nos três pontinhos do radiador, Transferir estoque. Destino, ferro misto; quantidade, oito quilos.
Transferir: sai de um e entra no outro, sem mudar o peso total do pátio.
E o Zerar Estoque é pra virada de inventário, quando você recomeça a contagem do zero. Todos os materiais já vêm marcados, e você desmarca os que ficam.
Pra confirmar, tem que digitar a frase da tela, porque não tem volta. Uma dica: antes de zerar, exporte o estoque, pra guardar o retrato do que tinha. Aqui eu só mostro e cancelo.""",
14: """Pra levar o estoque pro papel ou pra planilha, é o Exportar. Tem o estoque em pê-dê-éfe e em Excel, e a tabela de preços em pê-dê-éfe.
No estoque, você escolhe os materiais e as colunas do arquivo. Exportar, e o pê-dê-éfe abre numa aba nova, pronto pra salvar ou imprimir. No Excel, o arquivo baixa direto.
A tabela de preços sai da tabela escolhida na coluna da esquerda. Seleciono a Tabela Depósitos, escolho os materiais e o formato: folha á-quatro ou o papel da impressora térmica.
Pronto: a tabela com o preço de compra de cada material, do jeito que se entrega pro depósito.""",
15: """Por último, o Excluir. Ele parece apagar, mas na verdade arquiva. O material sai da lista e das buscas do pedido, e as compras, as vendas e o histórico dele continuam lá.
Repara no aviso: o radiador ainda tem cento e dez quilos. Excluindo, o sistema registra a saída desse saldo, como exclusão, e o estoque dele zera.
Sim, Excluir. Saiu da lista, e o aviso traz um Desfazer.
Clicando nele, o material volta com o saldo que tinha. Como a Recicla Vale vai continuar comprando radiador, ele fica.
Quando precisa mexer em vários materiais de uma vez, é só marcar as caixinhas da esquerda. Marquei dois, e sobe uma barra com Transferir Estoque, Definir prefixo e Excluir.
O Definir prefixo põe o mesmo prefixo no código de todos os selecionados. Desmarco, e a barra some.""",
16: """Pronto! Recapitulando: a gente conheceu a tela Estoque, cadastrou o radiador de cobre, com os preços e o estoque inicial, e trocou o código pelo do caderno.
Escolheu o ene-cê-ême, que o contador confirma, e criou o grupo Radiadores.
Reajustou o cobre de uma vez no Editar Preços, ligou a margem automática, pra tabela toda e por material, em porcentagem e em reais, e viu o resumo, o selo fora da margem e a calculadora no cadastro.
Criou a Tabela Depósitos, ligou ela ao Depósito Irmãos Siqueira e viu a ordem do preço: o personalizado, a tabela do pedido e o preço do material. E viu o menu da tabela: duplicar, fixar pro seu usuário e trocar a principal.
Ajustou o estoque na mão, transferiu entre materiais, exportou o estoque e a tabela, e viu que excluir é arquivar, com o Desfazer.
No próximo tutorial, a gente cadastra quem traz a sucata e quem leva: os clientes e os fornecedores. Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "A tela Estoque.",
           2: "Cadastrar um material.",
           3: "O código do material.",
           4: "O ene-cê-ême e a nota fiscal.",
           5: "Grupos de material.",
           6: "Editar preços em massa.",
           7: "Margem automática: a tabela toda.",
           8: "Margem automática: uma por material.",
           9: "O resumo e a margem fora da regra.",
           10: "A margem no cadastro do material.",
           11: "Várias tabelas de preço.",
           12: "Duplicar, fixar e trocar a principal.",
           13: "Movimentar, transferir e zerar.",
           14: "Exportar estoque e tabela.",
           15: "Excluir um material.",
           16: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "Estoque",
           2: "Materiais",
           3: "Materiais",
           4: "Nota fiscal",
           5: "Grupos",
           6: "Preços",
           7: "Preços",
           8: "Preços",
           9: "Preços",
           10: "Materiais",
           11: "Preços",
           12: "Preços",
           13: "Estoque",
           14: "Exportar",
           15: "Materiais",
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
