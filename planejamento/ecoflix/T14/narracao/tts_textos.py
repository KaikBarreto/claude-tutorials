# Texto enviado ao ElevenLabs (eleven_v4, voz Kaik Barreto) por capítulo do T14 "Bancos, cofre e conciliação bancária".
# Aplicado ao app 1.60.18 (20/11/2026): 19 capítulos (novos: 3 cartão de crédito, 6 corrigir e excluir lançamentos, 17 outros casos do
# extrato; os antigos 3 a 14 viraram 4, 5, 7 a 16). Cada linha do texto é uma linha da tabela Tela × Fala do roteiro.md
# ("(sem fala)" não entra). Trocas de pronúncia em relação ao roteiro (a legenda segue o roteiro, ver config_narracao.json):
#   OFX -> "ó-éfe-xis" | DRE -> "dê-érri-ê" | PDF -> "pê-dê-éfe"
# Números por extenso já no roteiro. A testar no ensaio: "Quiririm" (Aços Quiririm), escrita normal.
CAPS = {
0: """Oi! Neste tutorial a gente vai fazer o extrato do banco bater com o sistema da Recicla Vale Metais, linha por linha, até a diferença zerar.
Sabe quando o banco mostra um saldo, o sistema mostra outro, e ninguém sabe de onde vem a diferença? É isso que a gente resolve aqui.
No caminho, a gente cadastra uma conta nova e o cartão de crédito da empresa, acerta o cofre, corrige lançamentos errados e registra o dinheiro que só muda de lugar.
Se você ainda não viu o tutorial Contas a Pagar e Receber, dá uma olhada antes. [pause] Vamos começar pela tela.""",
1: """Tudo começa em Financeiro, Movimentações Financeiras. Com o cofre ligado, a tela tem esse nome. Sem o cofre, ela aparece como Movimentações Bancárias.
Aqui do lado ficam as contas da empresa, com o saldo embaixo de cada nome. Primeiro vem o cofre, depois a conta principal e as outras.
Clicando numa conta, abre o cartão dela, com o saldo e os botões do dia a dia: Saque, Sangria, Nova Movimentação e Extrato.
Embaixo, o histórico do mês. Dá pra trocar o período, buscar por descrição ou valor e, no Selecionar lançamentos, mexer em vários de uma vez. A gente usa ele daqui a pouco.
Linha que veio de pedido abre e mostra os itens. E o olho, aqui em cima, esconde os valores quando tem gente por perto.
O Extrato gera o movimento da conta em pê-dê-éfe ou em Excel, no período que você escolher. É o arquivo pra mandar pro contador ou guardar no fechamento.
Um detalhe: em Usuários e Permissões, o administrador pode liberar só algumas contas pra uma pessoa. Quem tem essa restrição só enxerga aqui as contas liberadas. O cofre e os cartões não mudam.
No Resumo, você vê o total da empresa: o dinheiro do cofre somado com o das contas do banco.
E lá em cima ficam duas abas. Nesta, você cuida das contas. Na Conciliação, confere o extrato do banco. Vamos começar pelas contas.""",
2: """A Recicla Vale abriu uma conta numa cooperativa de crédito. Pra ela entrar aqui, é Nova Conta.
O nome é do jeito que a empresa chama a conta: Conta Cooperativa. A instituição é opcional.
Em Valor em conta, o saldo que ela tem hoje no banco: cinco mil reais. A data desse saldo fica em hoje.
Escolho uma cor pra reconhecer a conta de longe.
Criar Conta. Repara no histórico: o saldo entrou como Ajuste de saldo, Saldo inicial. Ele acerta o saldo da conta, mas não conta como receita nem como despesa.
Uma dica: se o saldo ficar torto, edite a conta e corrija o Valor em conta. A diferença entra como Correção manual, também fora da dê-érri-ê. Assim o resultado do mês fica limpo, sem receita inventada.
Nesse menu também fica o Tornar principal. A principal é a conta que já vem escolhida nos pedidos e nos pagamentos. Aqui, ela continua sendo a Conta Principal.
Agora a poupança antiga, que ninguém usa mais. No Excluir, o sistema pergunta como fazer: Arquivar ou Migrar e Excluir.
Uma dica: arquivar não tem volta. A conta sai das listas e o histórico fica guardado. Já o Migrar e Excluir passa os lançamentos pra outra conta e apaga esta de vez. Na dúvida, arquive.
Arquivar. Pronto, a lista ficou só com as contas que a empresa usa.""",
3: """Além das contas, dá pra cadastrar o cartão de crédito da empresa. É no Novo Cartão.
O nome, o dia em que a fatura fecha e o dia em que ela vence: fecha no dia vinte e cinco e vence no dia cinco. O sistema já explica em qual fatura cada compra cai.
O limite é opcional: com ele, o sistema mostra quanto ainda dá pra gastar. Criar Cartão.
Ele fica separado das contas, com a fatura em aberto e o limite disponível.
Compra no cartão é Nova despesa. E repara: comecei a digitar e o sistema lembrou de um lançamento parecido, com a categoria e o centro de custo.
Preencher. Ele completa o que estava vazio e respeita o que eu já escolhi: o pagamento continua no cartão. Quando o campo está livre, ele sugere também a conta e a forma de pagamento mais usadas.
Cento e oitenta reais, Confirmar Despesa. A compra não sai de conta nenhuma agora: ela entra na fatura.
Na hora de pagar, é Pagar Fatura: você escolhe de qual conta sai o dinheiro. Pode pagar tudo ou uma parte, e se errar, o pagamento tem o Estornar. Aqui eu só mostrei.
Uma dica: pagar a fatura não cria despesa nova. As compras já são as despesas; o pagamento só tira o dinheiro da conta e quita a fatura.""",
4: """Agora o cofre. Ele é todo o dinheiro vivo da empresa: o que está guardado e o que está nos caixas abertos. O banco é o dinheiro nas contas. Os dois juntos dão o total da empresa.
Este é o cofre da Recicla Vale: dezoito mil e quinhentos reais. Ainda não tem caixa aberto hoje, então está tudo no cofre.
Hoje cedo, o Rafael contou o cofre e deu dezoito mil quinhentos e sessenta. Sessenta reais a mais do que o sistema mostra.
Pra acertar, é nos três pontinhos do cofre: Ajustar saldo. É a única opção dele, porque o cofre não se edita nem se arquiva.
Em Novo saldo, o valor contado. A Diferença aparece na hora: mais sessenta reais, em verde.
O motivo é obrigatório: contagem do cofre. Confirmar ajuste.
O ajuste fica no histórico com a etiqueta Ajuste. É acerto de contagem: não entra como receita nem como despesa.""",
5: """Hoje cedo, o Rafael também fez três coisas no banco: pagou o combustível da picape por Pix, trouxe dinheiro da Conta Secundária e sacou no caixa eletrônico. Cada uma tem o seu jeito de registrar.
O combustível é gasto de verdade. Nova Movimentação, tipo Saída, na Conta Principal.
Descrição, combustível da picape. Valor, trezentos e cinquenta reais. Categoria Combustível e centro de custo Frota.
Essa opção de não contar na dê-érri-ê é pra saldo herdado de outro sistema. Combustível é despesa, então ela fica desmarcada. Salvar.
A Entrada funciona do mesmo jeito, pra dinheiro que chegou sem pedido, como um rendimento. Dá pra acertar a data e a hora do lançamento e, se quiser, vincular a um cliente ou fornecedor.
Uma dica: transferência entre contas suas, saque e depósito só mudam o dinheiro de lugar. A empresa não fica mais rica nem mais pobre, então nada disso entra na dê-érri-ê.
Por isso a transferência tem tipo próprio. De onde saiu, a Conta Secundária. Pra onde foi, a Conta Principal. Oito mil reais, e a prévia mostra a saída e a entrada.
Transferir. Repara que nem pediu categoria: é dinheiro da empresa trocando de conta.
Agora o saque, que vai da Conta Principal pro cofre.
Dois mil reais. O banco cobrou tarifa? Sim, seis reais e cinquenta.
Antes de confirmar, os efeitos: o banco perde o saque mais a tarifa, e o cofre ganha só o saque. A tarifa, essa sim, vira uma despesa separada.
Confirmar Saque. O caminho contrário, levar dinheiro do cofre pro banco, é a Sangria, aqui do lado. Também só muda o dinheiro de lugar.
Uma dica: sem o cofre ligado, o saque só vai pra um caixa aberto, então o caixa precisa estar aberto antes. Com o cofre ligado e algum caixa aberto, o sistema ainda pergunta se o dinheiro vai mesmo pro cofre.""",
6: """Ontem, treinando a equipe, o Rafael lançou três despesas de teste na Conta Principal. Elas não existem de verdade, e o saldo ficou menor do que devia.
Todo lançamento feito à mão tem esses três pontinhos, com Editar e Excluir.
O Editar corrige o valor ou a conta. Digitou cento e cinquenta no lugar de quinze, ou lançou na conta errada? É aqui.
Esse ícone do lado faz só a troca de conta, num clique.
O Excluir apaga o lançamento e devolve o valor pro saldo. Dá pra fazer um por um. Mas são três, então vamos de uma vez.
Primeiro eu filtro: busco por teste, e ficam só as três.
Agora, Selecionar lançamentos. Cada linha ganha uma caixinha, e aparece essa barra. Dá pra marcar até cem de uma vez, sempre da mesma conta.
Marco todas pela caixinha de cima. Três lançamentos selecionados.
Antes de excluir, repara nesse outro botão. O Alterar categoria troca a categoria de todos os marcados de uma vez. É o jeito rápido de arrumar despesa que caiu na categoria errada. Só não mistura entrada com saída no mesmo lote.
Agora sim, Excluir selecionados. O sistema mostra o total do que vai sair: quinhentos e cinquenta e dois reais e vinte. Confiro antes de confirmar.
Excluir. Os três saem juntos, e o saldo da conta volta pro lugar.
Uma dica: Pix de compra e de venda não tem caixinha, porque pedido se corrige no próprio pedido. E o lote é tudo ou nada: se um dos marcados estiver conciliado ou protegido, o sistema avisa e não apaga nenhum.""",
7: """Com as contas em dia, a conciliação. Conciliar é conferir cada linha do extrato do banco com um lançamento do sistema.
Quando toda linha tem par, a diferença entre o saldo do banco e o do sistema chega a zero.
E a linha que sobra mostra o que ficou sem lançar, como uma tarifa que ninguém viu. É isso que deixa o fechamento do mês certo.
Na tela, é a aba Conciliação. A conta já vem escolhida: a Conta Principal.
E se bater dúvida, o Como funciona explica cada passo e cada botão. Primeiro, o extrato do banco.""",
8: """O extrato sai do site ou do app do banco. Você abre o extrato, escolhe o período e exporta no formato ó-éfe-xis. O pê-dê-éfe serve pra ler; pra conciliar, é o ó-éfe-xis.
Em Importar novo extrato, o próprio sistema ensina a achar o arquivo. Em alguns bancos ele tem outro nome, como Gerenciador Financeiro ou Conciliação bancária.
Escolho o arquivo que baixei, de um a dez de novembro.
Antes de importar, a prévia: o período, dezessete transações e o saldo final que o banco informou.
Importar. Se um dia você subir o mesmo período de novo, o sistema reconhece o que já entrou e não duplica.
Pronto. À esquerda, cada linha do banco, com a data e o valor. À direita, o que fazer com ela.
Uma dica: repara no sinal. Entrada vem em verde, com mais. Saída, em vermelho, com menos. Se alguma linha vier com o sinal trocado, confira com o banco antes de casar.
No rodapé ficam os três números do fechamento. A gente volta neles no fim.""",
9: """Começa pelo mais fácil. Nesta linha, o Pix de dois mil duzentos e cinquenta reais pro Depósito Irmãos Siqueira, o sistema já achou o par: a compra do dia três.
Confiro a data e o parceiro, e caso. A linha fica como Casada.
As outras sugestões vão do mesmo jeito: o aluguel, a energia, o Pix da Aços Quiririm, o combustível, o saque e a tarifa dele. Cada uma eu confiro antes de casar.
Agora, os oito mil que vieram da Conta Secundária. Esse dinheiro já está no sistema: é a transferência que a gente registrou.
Então é em Mais ações, Casar com transferência. Aparece a transferência certa, da Conta Secundária pra Conta Principal.
Casar transferência. Isso só liga a linha à transferência: não cria nada novo e o saldo não muda.
Uma dica: pra dinheiro que veio de outra conta sua, o caminho é sempre esse. Criar receita lançaria o valor de novo, e o saldo ficaria em dobro.""",
10: """Esta linha é o boleto da água, duzentos e trinta e oito reais e quarenta. Lembra da conta de água que estava vencida? Ela foi paga no banco, mas a baixa ficou pra trás.
Baixar conta. A lista traz só as contas em aberto do mesmo valor: a água e esgoto de outubro.
Dar baixa. A linha fica como Baixada, e em Contas a Pagar e Receber a água já aparece como Paga.
Por aqui, a baixa é sempre do valor inteiro. Pagamento em parte, você faz na tela de Contas a Pagar e Receber.""",
11: """Esta outra linha não existe em lugar nenhum do sistema: a tarifa do pacote do banco, sessenta e quatro reais e noventa.
Em Mais ações ficam todos os destinos de uma linha. O Funcionário, por exemplo, é pro vale pago por Pix. O Ajuste abre o mesmo lançamento com a opção de não contar na dê-érri-ê, pra linha que só acerta saldo. E o Saldo do cliente ou fornecedor é pro acerto de fiado.
Uma dica: vale que já foi lançado na tela de Funcionários se casa com o Buscar lançamento, sem criar de novo. O próprio painel do Funcionário lembra disso.
Pra tarifa, é Criar despesa. A descrição já vem do extrato. E a chave Não é receita nem despesa fica desligada, porque tarifa é gasto de verdade.
A categoria é obrigatória: Tarifas. E o botão já mostra o valor.
Criar. A linha fica como Criada, e a tarifa entra no histórico da conta como despesa.""",
12: """Este Pix da Serra Fina Alumínio caiu no dia nove: quatro mil oitocentos e quinze reais. E o sistema não sugeriu nada.
É que a venda foi registrada no dia três, por quatro mil oitocentos e quinze reais e vinte. A Serra Fina pagou depois e deixou os centavos de fora.
Em vez de criar outra receita, a gente procura a venda que já existe. Mais ações, Buscar lançamento.
Digito Serra. A busca aceita até dois reais de diferença e casa mesmo com a data diferente. Olha a venda, com vinte centavos a menos.
Casar com selecionado. O sistema confirma: casar com valor diferente?
Casar assim. A diferença não vira lançamento. Ela fica guardada no rodapé, em Diferenças casadas, pra quem quiser conferir.
Uma dica: quando muda só a data, ou só uns centavos no mesmo dia, o sistema já mostra o lançamento num aviso, com o botão de casar. A busca fica pra quando mudam a data e o valor juntos, como aqui.""",
13: """Estas duas linhas se anulam: o banco cobrou doze reais de tarifa por engano e devolveu no mesmo dia.
Nenhuma das duas precisa virar lançamento. Pra isso existe o Ignorar: a linha sai da fila sem criar nada.
Marco as duas. A soma dá zero.
Ignorar. O sistema confirma, e as duas ficam como Ignorada. Dá pra desfazer depois, se precisar.
Uma dica: ignorar conta como resolvido. Ignore só o que não mexeu no dinheiro da empresa, como esse par. Uma tarifa de verdade ignorada deixa a diferença aberta, e o fechamento não libera.""",
14: """Agora, duas linhas parecidas: dois Pix de trezentos e oitenta reais no mesmo dia. Um foi pra Aparecida Ramos; o outro, pra Auto Peças Vale Forte.
Aqui o sistema pede que você escolha. Casar com a compra errada deixaria a outra pendente pra sempre.
Escolher lançamento. A lista mostra as duas compras, e o nome no extrato diz qual é: a da Aparecida Ramos.
Marco a compra da Aparecida, e Casar com o selecionado.
Repara: a outra linha ficou com um par só, e a sugestão já vem certa. É só casar.
Uma dica: quando aparecer esse aviso, escolha pelo nome e pela data do extrato. Assim nenhuma compra fica pendente nem vira lançamento em dobro.""",
15: """Errou alguma? Toda linha resolvida tem o Desfazer, que devolve a linha pra pendente. Casada e Ignorada desfazem na hora.
Aqui eu só desfiz pra mostrar, então caso de novo.
Já a Criada e a Baixada mexem em dinheiro. O Desfazer delas pede confirmação, porque apaga o lançamento criado ou estorna a baixa.
E o Cancelar conciliação desfaz o arquivo inteiro de uma vez: os vínculos, os lançamentos criados e as baixas. Por segurança, pede pra digitar a palavra cancelar. Aqui eu mantenho a conciliação.
Já o Voltar só sai da tela. O progresso fica salvo, e o Continuar retoma de onde parou, até no dia seguinte.
Uma dica: lançamento conciliado não sai pelo Excluir das movimentações. Primeiro você desfaz a linha aqui, e depois exclui lá.""",
16: """Hora de fechar. No rodapé, o Saldo do banco é o saldo final que veio no arquivo. O Saldo conciliado é o que o sistema soma com as linhas resolvidas.
A Diferença é a distância entre os dois. Ela está em zero, em verde, e não sobrou nenhuma linha pendente.
Os vinte centavos da Serra Fina ficam aqui, só pra conferência. Eles não travam o fechamento.
Uma dica: o fechamento só libera com todas as linhas resolvidas e a diferença em zero. Se ela não zerar, alguma linha foi ignorada sem motivo. Cada linha se resolve de verdade, sem lançamento pra forçar o zero, e é isso que deixa o fechamento confiável.
Finalizar conciliação. Pronto: esse extrato fica selado, só pra leitura.
Ele vai pra Conciliações anteriores, com o selo Conciliado. No próximo extrato, é só importar e seguir do mesmo jeito.""",
17: """Na Conta Secundária, o extrato é pequeno, mas tem casos que aparecem bastante. Eu importo o arquivo e já casei as linhas que têm par certo. Sobram os casos diferentes.
O primeiro é o acerto de fiado: a empresa devia ao Depósito Irmãos Siqueira e pagou uma parte por Pix. É em Mais ações, Saldo do cliente ou fornecedor. Escolho o Depósito, e o sistema mostra o saldo dele.
Dar baixa. Não precisa bater com o valor do pedido: cada Pix abate o que ele vale, até zerar a dívida.
O segundo: um Pix só pagou duas vendas do mesmo cliente. Em Mais ações, Casar com vários lançamentos, marco as duas vendas. Quando a soma fecha com o valor da linha, o botão libera.
O terceiro é o contrário: o banco mostra duas linhas, e no sistema é um lançamento só, a folha de pagamento. Marco as duas, confiro a soma, e Casar duas linhas com um lançamento.
E quando o Pix foi lançado na conta errada, o sistema avisa na própria linha: achamos este lançamento em outra conta. Um botão move o lançamento pra conta certa e já casa.
Entrada que não existe no sistema, como um rendimento, é Criar receita, igual à tarifa que a gente criou. O resto segue como no extrato anterior.""",
18: """Pronto! Recapitulando: a gente cadastrou a Conta Cooperativa com o saldo inicial, arquivou a poupança que ninguém usava e cadastrou o cartão de crédito da empresa.
Ajustou o cofre pelo caminho certo e registrou o combustível, a transferência e o saque, cada um do seu jeito.
Corrigiu e excluiu lançamentos, um por um e vários de uma vez.
Importou o extrato do banco e casou as linhas com os lançamentos, inclusive a transferência entre as contas.
Deu baixa na conta de água pelo extrato, criou a tarifa, aceitou a diferença de centavos e ignorou o par de tarifa e estorno.
Escolheu o lançamento certo entre os valores repetidos e finalizou a conciliação com diferença zero.
E, no extrato de outra conta, resolveu o acerto de fiado, o Pix que pagou duas vendas e as duas linhas do banco que são um lançamento só.
No próximo tutorial, a gente responde a pergunta que todo dono faz: eu ganhei ou perdi dinheiro esse mês? Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {          1: 'A tela e as contas.',
           2: 'Cadastrar e arquivar contas.',
           3: 'O cartão de crédito da empresa.',
           4: 'O cofre e o ajuste de saldo.',
           5: 'Movimentação, transferência e saque.',
           6: 'Corrigir e excluir lançamentos.',
           7: 'O que é conciliar.',
           8: 'Importar o extrato.',
           9: 'Casar com o sistema.',
           10: 'Baixar uma conta.',
           11: 'Criar um lançamento.',
           12: 'Buscar e aceitar centavos.',
           13: 'Ignorar uma linha.',
           14: 'Valores repetidos.',
           15: 'Desfazer e cancelar.',
           16: 'Fechar a conciliação.',
           17: 'Outros casos do extrato.',
           18: 'Recapitulando.'}
# Rótulo de área em cima do título (vinheta).
KICKERS = {          1: 'Bancos',
           2: 'Bancos',
           3: 'Bancos',
           4: 'Cofre',
           5: 'Movimentações',
           6: 'Movimentações',
           7: 'Conciliação',
           8: 'Conciliação',
           9: 'Conciliação',
           10: 'Conciliação',
           11: 'Conciliação',
           12: 'Conciliação',
           13: 'Conciliação',
           14: 'Conciliação',
           15: 'Conciliação',
           16: 'Fechamento',
           17: 'Conciliação',
           18: 'Resumo'}

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
