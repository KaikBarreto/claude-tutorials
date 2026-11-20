# Texto para o ElevenLabs (eleven_v4, voz Kaik Barreto) por capítulo do T11 "Produção".
# Gerado da coluna Fala do roteiro.md: cada linha do texto é uma linha da tabela Tela × Fala (a vinheta de
# abertura não tem fala). Trocas de pronúncia em relação ao roteiro (a legenda segue o roteiro, ver
# config_narracao.json): Kardex -> "cardécs" | PDF -> "pê-dê-éfe" | Kanban -> "canban" | CRM -> "cê-érre-ême"
# Números por extenso; na legenda viram algarismo pelo `numeros` do config_narracao.json.
# 1.60.18 (20/11): 19 capítulos. Novos: 10 (mexer na ordem), 15 (Conversão), 16 (perda padrão), 17 (Máquinas). O que era
# 10 a 14 virou 11 a 14 e 18. Nomes das sementes do robô (apos-cap09 etc.) seguem a numeração antiga.
CAPS = {
0: """Oi! Neste tutorial a gente vai transformar o que entrou no pátio em produto de maior valor, e descobrir quanto custou cada quilo de verdade.
Na Recicla Vale Metais, a latinha chega solta, com terra, água e até lata de aço no meio. Prensada, ela vira fardo e vende melhor. Mas quanto custou cada quilo desse fardo?
É isso que a Produção responde. Ela fica aqui, em Materiais, Produção, e depende do plano contratado.
Se você ainda não viu o tutorial Estoque: saldo, histórico e posição, dá uma olhada antes. [pause] Vamos ver o que a Produção resolve.""",
1: """As abas ficam aqui em cima. São seis, e a gente passa por todas: Ordens de Produção, Conversão, Fichas Técnicas, Máquinas, Relatório e Configurações.
O caminho é este. Primeiro, a ficha técnica: a receita, com o que entra e o que sai. Depois, a ordem: quanto produzir e quem vai produzir.
No fim do dia, o lançamento: quanto cada um produziu e quanta latinha foi usada de verdade. Aí o estoque se mexe sozinho: a latinha sai, e o fardo entra.
E quando a ordem é finalizada, o sistema fecha o custo de cada quilo.
Uma dica: se a sua empresa ainda não tem a Produção, a tela abre desfocada, com o aviso Ainda não está no seu plano e o botão Ativar produção.""",
2: """Tudo começa pela ficha técnica. Ela é a receita do produto: o que entra e o que sai.
Na receita do fardo, entra latinha e sai fardo de alumínio. Uma ficha por produto, e ela vale pra todas as ordens dele.
Clico em Nova. A tela já mostra a receita do jeito que ela é: as matérias-primas entram, e o produto final sai.
Do lado esquerdo, a matéria-prima. Escolho o Alumínio latinha.
Do lado direito, o produto final: o Fardo de alumínio. Ele precisa estar cadastrado como material, igual a qualquer outro do estoque.
Se ainda não estiver, o botão Cadastrar novo produto cria o material sem sair da ficha.
E o nome da ficha, aqui no alto, é opcional. Em branco, ela usa o nome do produto.""",
3: """Agora as quantidades. Primeiro, a unidade produzida, aqui em cima: o fardo é pesado na balança, então ele sai em quilo.
Na matéria-prima vai a quantidade pra um quilo de fardo, e não pro lote inteiro. Na prensa, um quilo de latinha vira um quilo de fardo, então aqui é um.
O que se perde na prensa aparece depois, no lançamento do dia.
Peças por jogo serve pra quem produz por peça e vende em conjunto, como um jogo de quatro. O fardo sai em quilo, então fica vazio.
Salvar ficha. Pronto, a ficha do fardo já está na lista.
Repara na ficha do Cobre mel, que a Recicla Vale já usa pra descascar fio. Pra cada quilo de cobre, entram um quilo e seiscentos gramas de fio encapado.
É sempre assim: a ficha leva a quantidade de um quilo, e a ordem multiplica. Quinhentos quilos de fardo pedem quinhentos quilos de latinha. Cinquenta quilos de cobre pedem oitenta quilos de fio.""",
4: """E quando sai mais de uma coisa do mesmo processo? Isso é o coproduto, e ele fica aqui embaixo, em Outros resultados da produção.
Quando a latinha passa no ímã, as latas de aço que vieram no meio saem. Elas viram chaparia, que também tem valor. Mas quanto sai, só dá pra saber depois de separar.
Por isso o coproduto entra na ficha sem quantidade. Adiciono a Chaparia, e o cartão já avisa: a quantidade é digitada no lançamento do dia.
Salvar ficha. A receita do fardo está completa.
Uma dica: o botão Excluir ficha, aqui no alto, tira a ficha da lista. As ordens que já foram feitas com ela continuam com o histórico.""",
5: """Receita pronta, agora a ordem de produção.
A ordem é o plano: quanto produzir, quando e com quem. Quem mexe no estoque é o lançamento do dia.
Clico em Nova produção. A ordem sempre sai de uma ficha, e eu escolho a do Fardo de alumínio.
Na quantidade planejada, quinhentos quilos. É a meta do lote, que serve de referência.
A data já vem com hoje. No responsável, o Marcos, que cuida da balança.
Na equipe, quem vai prensar: o Cláudio e o Diego. É essa equipe que aparece no lançamento do dia, um por um.
Embaixo vem o consumo teórico estimado: quinhentos quilos de latinha. E o custo estimado, seis reais e vinte por quilo, que é a média do que a Recicla Vale pagou na latinha.
Como o fardo sai em quilo, onde a tela diz peça, vale quilo.
Criar ordem. Pronto, a ordem três está em A fazer, ainda como rascunho.
Uma dica: criar, lançar e finalizar ordem pede a permissão Registrar Produção. Ficha técnica e configurações pedem Gerenciar Fichas Técnicas. São separadas: o encarregado lança a produção sem mexer na receita. E tem uma terceira, Ver Custos na Produção. Sem ela, a pessoa lança tudo e vê as quantidades, mas nenhum valor em reais.""",
6: """As ordens ficam neste quadro, o canban: cada coluna é uma etapa, e cada cartão anda de uma pra outra. Ele já vem com três: A fazer, Em produção e Concluída.
Na Recicla Vale, a coluna de conclusão é a Concluída. Repara no sinal de check do lado do nome.
As colunas são suas. Clicando no nome, você muda o nome e a cor. Aqui, Em produção vira Na prensa.
Nessa janela fica também a chave Coluna de conclusão. É pra coluna marcada que vão as ordens finalizadas, e só uma pode ter.
Salvar. Pronto, a coluna mudou de nome.
Precisa de mais uma etapa? O botão Coluna cria outra no fim do quadro.
E o menu de três pontos da coluna tem o Excluir coluna. As ordens dela vão pra primeira coluna, e nenhuma produção é apagada.
Pra andar com a ordem, é só arrastar o cartão. O Cláudio e o Diego começaram a prensar, então ela vai pra Na prensa.
Arrastar pra coluna de conclusão é diferente: abre a janela de finalizar, porque lá só fica ordem fechada de verdade. A gente faz isso daqui a pouco.""",
7: """Fim do dia, hora de lançar o que a equipe prensou. Clico no cartão, e a ordem abre com a meta e o que já foi produzido.
Lançar produção do dia. O dia já vem com hoje.
Em Produzido, a equipe da ordem, um por linha. O Cláudio prensou duzentos e sessenta quilos, e o Diego, duzentos e vinte. O sistema soma: quatrocentos e oitenta quilos no dia.
Agora os subprodutos. É aqui que entra o coproduto da ficha: catorze quilos de chaparia, as latas de aço que saíram no ímã.""",
8: """Embaixo fica a matéria-prima usada. O sistema sugere quatrocentos e oitenta quilos de latinha: a ficha vezes o que foi produzido. Esse é o teórico.
Só que na balança, a latinha usada deu quatrocentos e noventa e oito quilos. Esse é o real. A diferença são dezoito quilos: as latas de aço, a terra e a água que saíram.
No campo Real, eu corrijo pra quatrocentos e noventa e oito. Repara que a diferença aparece na hora, em vermelho: gastou mais do que a receita previa.
Se der menos, ela aparece em verde: rendeu mais que a receita.
Uma dica: quem baixa do estoque é o real, não o teórico. Saem quatrocentos e noventa e oito quilos de latinha, e não os quatrocentos e oitenta da ficha.""",
9: """Com a diferença, apareceu o campo Motivo da perda, e o botão Salvar lançamento ficou apagado. O sistema pede o motivo antes de salvar.
É a tolerância de perda. Na Recicla Vale ela é de dois por cento: em quatrocentos e oitenta quilos, até nove quilos e seiscentos gramas de diferença passam sem motivo.
Os dezoito quilos passaram disso, então o motivo é obrigatório. Dentro da tolerância, a linha só avisa e não pede nada. O valor da tolerância fica nas Configurações, que a gente vê no fim.
Escolho o motivo. Aqui, a maior parte da diferença virou chaparia, então é Material reaproveitável. O motivo fica guardado no lançamento, e o botão acende.
Uma dica: com o Salvar lançamento apagado, desce até a matéria-prima usada. É lá que o motivo da perda fica esperando.
No fim da janela tem também a Observação, que é opcional. Dá pra deixar um recado do dia, e ele fica guardado no lançamento.
Salvar lançamento. O estoque já foi ajustado: saiu a latinha, e entraram o fardo e a chaparia. E o dia aparece na ordem, com quem produziu.""",
10: """A ordem já tem um dia lançado, e mesmo assim dá pra mexer nela. O lápis do cartão abre Editar ordem em andamento: a equipe, a meta, a data, o responsável e a coluna continuam livres.
Só a ficha técnica fica travada, porque o que já foi consumido foi calculado por ela.
Faltou alguém, ou entrou outro no lugar? É só trocar na equipe. Quem sai continua no relatório dos dias em que produziu, e só deixa de aparecer nos próximos lançamentos.
Dentro da ordem, cada dia lançado tem o seu menu. Editar este dia reabre o lançamento do jeito que ficou, com a observação e tudo, pra corrigir um número.
E Excluir este dia tira só aquele lançamento: o total é recalculado, e o estoque daquele dia volta. Os outros dias ficam como estão. Aqui eu cancelo.
Se a produção leva mais de um dia, é só lançar de novo amanhã. Cada dia vira uma linha, e o produzido até agora vai somando.
O quadro também vira lista. Na Lista aparecem os filtros de período, produto e status, bons pra achar uma ordem antiga.
O menu de cada linha tem as mesmas ações do cartão. E uma dica: excluir uma ordem que já tem lançamento estorna todos os dias de uma vez. O sistema avisa antes.""",
11: """Lote prensado, hora de fechar a ordem. Arrasto o cartão pra Concluída, e abre a janela de finalizar.
A meta era de quinhentos quilos, e saíram quatrocentos e oitenta: noventa e seis por cento da meta. Como a meta é referência, a ordem fecha assim mesmo. Só não fecha ordem sem nenhum dia lançado: o sistema pede pelo menos um lançamento.
No resumo do lote fica tudo junto: o fardo, a chaparia, a latinha usada e os dezoito quilos de perda.
E o custo real fecha aqui: três mil e oitenta e sete reais e sessenta no lote, e seis reais e quarenta e três por quilo de fardo.
Na ordem, o estimado era seis e vinte. A diferença vem dos dezoito quilos a mais de latinha: eles também entram no custo do fardo.
Finalizar ordem. Pronto, o cartão foi pra Concluída, já com o custo do lote e o de cada quilo.
Ordem finalizada fica de vez na coluna de conclusão. Pra desfazer, só excluindo, como a gente vê no fim.""",
12: """Agora o relatório. Em cima ficam os filtros: período, produto, funcionário e máquina. Escolho o Fardo de alumínio, neste mês.
Os cartões resumem o mês do fardo: as ordens concluídas, o custo da matéria-prima, a perda média e o rendimento médio.
Rendimento é quanto saiu pelo que entrou: quatrocentos e oitenta quilos de fardo pra quatrocentos e noventa e oito de latinha. Dá noventa e seis vírgula quatro por cento.
E a perda é o que passou da ficha: os dezoito quilos sobre os quatrocentos e oitenta, três vírgula oito por cento.
O gráfico mostra a produção no tempo, e os botões trocam entre diário, semanal e mensal.
Na aba Por produto, primeiro o ranking, que compara por quantidade ou por custo.
Embaixo, a tabela traz a mesma conta por produto, com o teórico, o real e o custo por peça, que aqui é por quilo. E clicando numa linha, ela abre quem produziu aquele produto.
E o botão Exportar tira o relatório em pê-dê-éfe ou em planilha.
Em Por funcionário fica o ranking da equipe. E na produção do dia aparece a meta, de duzentos e cinquenta quilos por pessoa: o Cláudio bateu, e pro Diego faltaram trinta quilos.
Mais abaixo, o detalhamento: clicando no nome, aparecem os produtos daquela pessoa. E em Ver matriz completa, o cruzamento de cada funcionário com cada produto.
A terceira aba, Lançamentos, lista a produção dia a dia, com data, produto, quantidade, máquina e responsável.""",
13: """Agora as configurações da Produção. Cada uma grava na hora, assim que você muda.
O custo de produção em cadeia, o multinível, é pra quando um material que você mesmo produziu vira matéria-prima de outro. Ligado, ele entra com o custo de produção, e não com o de compra.
Descontar o valor das sobras do custo de produção. Desligado, toda a matéria-prima entra no custo do produto principal, e a sobra entra no estoque sem valor. Ligado, a sobra deixa de pesar no custo, e isso vale só da próxima produção em diante.
Qual preço de compra vira o custo do produto: a média de todas as compras, que é o padrão, a média de um período, como os últimos trinta dias, ou o preço da última compra. Se faltar compra pra regra escolhida, o sistema usa a próxima fonte e avisa na tela.
Exigir funcionário na ordem obriga a informar a equipe antes de criar a ordem.
Quem produz por peça e vende em conjunto escolhe aqui o nome do agrupamento: jogo, caixa, fardo. E com Lançar produção em jogos ligado, a quantidade é digitada em jogos, e o sistema converte pra peças.
Em Quando dar baixa no estoque, a Recicla Vale usa o padrão: cada dia lançado já mexe no estoque.
Desligado, os dias vão se acumulando, e o estoque só mexe quando a ordem é finalizada.
Bloquear finalização quando faltar matéria-prima em estoque: a Recicla Vale liga. Assim, a produção não fecha sem matéria-prima no estoque, e o saldo não fica negativo.
A tolerância de perda é aquela dos dois por cento. Com zero, o sistema pede o motivo pra qualquer diferença.
E a meta de produção por dia, por funcionário, é a do relatório: duzentos e cinquenta quilos.
Por fim, os padrões: a unidade que já vem nas fichas novas, e um prefixo pra numeração das ordens.""",
14: """E quando uma ordem foi lançada errada? Repara nas ordens um e dois do Cobre mel: são a mesma produção, lançada duas vezes.
Ordem concluída fica na coluna de conclusão. Pra corrigir, o caminho é excluir. Na lixeira do cartão, o sistema avisa que o estoque é estornado. Estornar é desfazer o movimento: a matéria-prima volta, e o produto sai.
Excluir ordem. Pronto: os oitenta quilos de fio voltaram pro estoque, e os cinquenta quilos de cobre saíram.
No histórico do material, o cardécs, dá pra ver tudo. As duas saídas da produção continuam lá, e o estorno entra como uma linha nova, devolvendo os oitenta quilos.
Nada é apagado: o histórico conta o que aconteceu, até o que foi desfeito.
Uma dica: no cardécs, a produção tem tipo próprio, Produção. Quem olha só o que foi comprado e vendido acha que o saldo não bate. É a produção que explica a diferença.""",
15: """Nem toda produção precisa de ordem, equipe e lançamento. Pra transformar um material em outro num passo só, existe a aba Conversão.
Escolho o produto, que vem da ficha técnica, e digito a quantidade: dez quilos de Cobre mel. Do lado, o resultado aparece antes de gravar: vão sair dezesseis quilos de fio, e o custo fica em vinte e oito reais e oitenta por quilo.
Confirmar. O estoque mexe na hora: o fio baixa, e o cobre entra. E a tela continua pronta, com o produto escolhido, pra lançar o próximo.
Embaixo fica o histórico do período, com o que saiu, o que entrou e o custo.
Lançou errado? O botão de estornar devolve tudo: o fio volta, e o cobre sai.
Uma dica: a Conversão não tem equipe, nem real contra teórico, nem motivo de perda. Ela baixa exatamente o que a ficha manda. Precisa desse controle? Use a ordem de produção.""",
16: """Tem sobra que se repete em toda produção. No fio de cobre, a capa sai sempre na mesma proporção. Dá pra deixar isso na ficha, em Perda padrão, dentro do cartão da matéria-prima.
Em Quanto se perde deste insumo, trinta e sete e meio por cento: de um quilo e seiscentos de fio, seiscentos gramas são capa.
Depois, pra onde ela vai. Perda pura some, e não volta pro estoque. Aqui ela vira outro material, a Capa de fio. E a tela já confere a conta: de cem quilos de fio, trinta e sete e meio viram capa.
Repara embaixo: a Capa de fio apareceu sozinha, com o selo Vem da perda. Salvar ficha.
Pra ver funcionando, crio uma ordem de quarenta quilos de Cobre mel, com o Diego.
No lançamento do dia, o Diego descascou quarenta quilos. E a capa já veio preenchida em Subprodutos: vinte e quatro quilos, calculados sobre o fio usado de verdade. Se a balança disser outro valor, é só corrigir.
Na matéria-prima, o sistema lembra que a ficha já conta essa perda. Como o fio usado bateu com a ficha, ele não pede motivo.
Salvar lançamento. O fio saiu, e o cobre e a capa entraram no estoque, sem ninguém digitar a sobra.""",
17: """Se o pátio tem mais de uma máquina, vale cadastrar em Máquinas. Nova máquina, o nome, e pronto: Prensa zero um.
A partir daí, a ordem de produção ganha o campo Máquina.
E o relatório passa a filtrar por máquina e a mostrar o ranking de máquinas, na aba Lançamentos.
Uma dica: máquina que saiu de uso é desativada, e não apagada. Ela some das ordens novas e continua nas antigas.""",
18: """Pronto! Recapitulando: a gente montou a ficha técnica do fardo, com a latinha que entra, o fardo que sai e a chaparia como coproduto.
Criou a ordem de quinhentos quilos com a equipe, mudou o nome de uma coluna do canban e arrastou a ordem.
Lançou a produção do dia por funcionário, corrigiu a latinha pro real da balança e deu o motivo da perda acima da tolerância.
Finalizou a ordem com o custo real de cada quilo, leu o rendimento no relatório, passou pelas configurações e excluiu uma ordem lançada em dobro, com o estorno do estoque.
E ainda viu como mexer numa ordem em andamento, a Conversão em um passo, a perda padrão que já calcula a sobra e o cadastro de máquinas.
No próximo tutorial, nenhuma oportunidade se perde no caminho: contatos e negociações organizados no cê-érre-ême. Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "O que a Produção resolve.",
           2: "A receita do produto.",
           3: "Quanto entra por unidade.",
           4: "Coprodutos.",
           5: "Criar a ordem de produção.",
           6: "O canban.",
           7: "A produção do dia.",
           8: "O real contra o teórico.",
           9: "Perda acima da tolerância.",
           10: "Mexer na ordem em andamento.",
           11: "Finalizar e fechar o custo.",
           12: "Relatório de Produção.",
           13: "Os ajustes da Produção.",
           14: "Excluir uma ordem concluída.",
           15: "Conversão: produzir em um passo.",
           16: "Perda padrão: a sobra já sai calculada.",
           17: "Máquinas.",
           18: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "Produção",
           2: "Ficha técnica",
           3: "Ficha técnica",
           4: "Ficha técnica",
           5: "Ordens",
           6: "Ordens",
           7: "Lançamento",
           8: "Lançamento",
           9: "Lançamento",
           10: "Ordens",
           11: "Ordens",
           12: "Relatório",
           13: "Configurações",
           14: "Ordens",
           15: "Conversão",
           16: "Ficha técnica",
           17: "Máquinas",
           18: "Resumo"}

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
