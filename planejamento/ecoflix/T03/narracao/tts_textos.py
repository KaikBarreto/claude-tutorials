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
1: """A tela tem quatro partes. Na coluna da esquerda ficam as tabelas de preço. Por enquanto, só a principal, com a estrela. Daqui a pouco a gente cria outra.
Em cima, os botões do dia a dia: Movimentar estoque, Editar Tabela, Grupos, Exportar e Zerar Estoque. Cada um tem a sua vez neste tutorial.
Os três cartões resumem o pátio. O primeiro é o peso total em estoque.
O Total Pago é esse estoque vezes o preço médio que você pagou nas compras. E a Projeção de Vendas é o mesmo estoque vezes o preço de venda: quanto entraria se você vendesse tudo hoje.
Embaixo, a lista de materiais: o código, o nome, o estoque atual e os preços de cada um. O preço médio pago vem marcado como estimativa, porque é uma média das compras.
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
6: """O preço da sucata mexe toda semana. Hoje, o cobre subiu cinquenta centavos o quilo, na compra e na venda. Em vez de abrir material por material, a gente usa o Editar Tabela.
Abre uma lista com todos os materiais, com a compra e a venda lado a lado. À esquerda você escolhe a tabela; aqui, a principal.
Busco cobre, e ficam só os cobres.
No cobre mel, a compra vai pra quarenta e dois e cinquenta, e a venda pra quarenta e sete e noventa.
Faço o mesmo no cobre misto e no fio encapado. O radiador eu cadastrei hoje, já no preço novo, então ele fica como está.
As células alteradas ficam destacadas, e o aviso em cima conta três materiais com alteração.
Salvar, e os preços novos já valem pra próxima compra e pra próxima venda. O aviso fala das tabelas vinculadas: elas acompanham sozinhas, e esse é o nosso próximo assunto.""",
7: """A maioria dos pátios trabalha só com a tabela principal. Mas a Recicla Vale paga um pouco mais pros depósitos, que trazem material separado e em volume.
Então, Nova Tabela, com o nome Tabela Depósitos. Marco Vincular à tabela principal e ponho quatro por cento a mais.
O exemplo embaixo mostra a conta: o que custa dez reais na principal sai por dez e quarenta nesta tabela.
Vinculada quer dizer que ela acompanha a principal sozinha: quando o preço muda lá, como a gente fez com o cobre, muda aqui também.
Criar Tabela. Com ela selecionada, a lista mostra o preço dos depósitos: o cobre mel sai a quarenta e quatro e vinte. O preço de venda, nesta tela, continua o da principal.
Agora, ligar a tabela a quem vende pra gente. Em Clientes e Fornecedores, abro o Depósito Irmãos Siqueira e clico em Editar.
Em Tabela de Preços Padrão, escolho a Tabela Depósitos e salvo. Agora toda compra do depósito já começa nessa tabela.
E quando um material tem mais de um preço possível, qual vale? Uma dica: essa é a dúvida clássica, então vale guardar a ordem. Primeiro, o preço personalizado daquele cliente ou fornecedor. Depois, a tabela escolhida no pedido. E por último, o preço do material.
Pra ver na prática, abro uma compra só pra olhar o preço; a compra em si fica pro tutorial de compra e venda. Escolho o depósito, e a tabela dele já vem selecionada.
No cobre mel, entra o preço da tabela: quarenta e quatro e vinte.
Já no bronze, o depósito tem um preço personalizado: trinta e cinquenta. Olha o aviso: Preço especial aplicado. O personalizado ganha da tabela.""",
8: """O estoque normalmente se mexe sozinho, pelas compras e pelas vendas. Mas às vezes ele precisa de um ajuste na mão: na contagem de hoje, o radiador deu cento e dezoito quilos, e não cento e vinte.
Em Movimentar estoque, escolho Saída, o radiador e dois quilos. A janela mostra o antes e o depois: de cento e vinte pra cento e dezoito quilos.
Na observação, eu escrevo o motivo. Fica tudo no histórico do material, com quem fez e quando. Registrar saída.
Agora, transferir. Na desmontagem dos radiadores saíram oito quilos de ferro, das cintas e dos suportes. Esse peso entrou como radiador, mas é ferro misto.
Nos três pontinhos do radiador, Transferir estoque. Destino, ferro misto; quantidade, oito quilos.
Transferir: sai de um e entra no outro, sem mudar o peso total do pátio.
E o Zerar Estoque é pra virada de inventário, quando você recomeça a contagem do zero. Todos os materiais já vêm marcados, e você desmarca os que ficam.
Pra confirmar, tem que digitar a frase da tela, porque não tem volta. Uma dica: antes de zerar, exporte o estoque, pra guardar o retrato do que tinha. Aqui eu só mostro e cancelo.""",
9: """Pra levar o estoque pro papel ou pra planilha, é o Exportar. Tem o estoque em pê-dê-éfe e em Excel, e a tabela de preços em pê-dê-éfe.
No estoque, você escolhe os materiais e as colunas do arquivo. Exportar, e o pê-dê-éfe abre numa aba nova, pronto pra salvar ou imprimir. No Excel, o arquivo baixa direto.
A tabela de preços sai da tabela escolhida na coluna da esquerda. Seleciono a Tabela Depósitos, escolho os materiais e o formato: folha á-quatro ou o papel da impressora térmica.
Pronto: a tabela com o preço de compra de cada material, do jeito que se entrega pro depósito.""",
10: """Por último, o Excluir. Ele parece apagar, mas na verdade arquiva. O material sai da lista e das buscas do pedido, e as compras, as vendas e o histórico dele continuam lá.
Repara no aviso: o radiador ainda tem cento e dez quilos. Excluindo, o sistema registra a saída desse saldo, como exclusão, e o estoque dele zera.
Sim, Excluir. Saiu da lista, e o aviso traz um Desfazer.
Clicando nele, o material volta com o saldo que tinha. Como a Recicla Vale vai continuar comprando radiador, ele fica.""",
11: """Pronto! Recapitulando: a gente conheceu a tela Estoque, cadastrou o radiador de cobre, com os preços e o estoque inicial, e trocou o código pelo do caderno.
Escolheu o ene-cê-ême, que o contador confirma, e criou o grupo Radiadores.
Reajustou o cobre de uma vez, criou a Tabela Depósitos, ligou ela ao Depósito Irmãos Siqueira e viu a ordem do preço: o personalizado, a tabela do pedido e o preço do material.
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
           7: "Várias tabelas de preço.",
           8: "Movimentar, transferir e zerar.",
           9: "Exportar estoque e tabela.",
           10: "Excluir um material.",
           11: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "Estoque",
           2: "Materiais",
           3: "Materiais",
           4: "Nota fiscal",
           5: "Grupos",
           6: "Preços",
           7: "Preços",
           8: "Estoque",
           9: "Exportar",
           10: "Materiais",
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
