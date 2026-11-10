# Texto enviado ao ElevenLabs (eleven_v4, voz Kaik Barreto) por capítulo do T14 "Bancos, cofre e conciliação bancária".
# Gerado do roteiro.md (coluna Fala) por T14_gera_tts.py: cada linha do texto é uma linha da tabela Tela × Fala
# ("(sem fala)" não entra). Trocas de pronúncia em relação ao roteiro (a legenda segue o roteiro, ver
# config_narracao.json):
#   OFX -> "ó-éfe-xis" | DRE -> "dê-érri-ê" | PDF -> "pê-dê-éfe"
# Números por extenso já no roteiro. A testar no ensaio: "Quiririm" (Aços Quiririm), escrita normal.
CAPS = {
0: """Oi! Neste tutorial a gente vai fazer o extrato do banco bater com o sistema da Recicla Vale Metais, linha por linha, até a diferença zerar.
Sabe quando o banco mostra um saldo, o sistema mostra outro, e ninguém sabe de onde vem a diferença? É isso que a gente resolve aqui.
No caminho, a gente cadastra uma conta nova, acerta o cofre e registra o dinheiro que só muda de lugar.
Se você ainda não viu o tutorial Contas a Pagar e Receber, dá uma olhada antes. [pause] Vamos começar pela tela.""",
1: """Tudo começa em Financeiro, Movimentações Financeiras. Com o cofre ligado, a tela tem esse nome. Sem o cofre, ela aparece como Movimentações Bancárias.
Aqui do lado ficam as contas da empresa, com o saldo embaixo de cada nome. Primeiro vem o cofre, depois a conta principal e as outras.
Clicando numa conta, abre o cartão dela, com o saldo e os botões do dia a dia: Saque, Sangria, Nova Movimentação e Extrato.
Embaixo, o histórico do mês, com a busca por descrição ou valor.
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
3: """Agora o cofre. Ele é todo o dinheiro vivo da empresa: o que está guardado e o que está nos caixas abertos. O banco é o dinheiro nas contas. Os dois juntos dão o total da empresa.
Este é o cofre da Recicla Vale: dezoito mil e quinhentos reais. Ainda não tem caixa aberto hoje, então está tudo no cofre.
Hoje cedo, o Rafael contou o cofre e deu dezoito mil quinhentos e sessenta. Sessenta reais a mais do que o sistema mostra.
Pra acertar, é nos três pontinhos do cofre: Ajustar saldo. É a única opção dele, porque o cofre não se edita nem se arquiva.
Em Novo saldo, o valor contado. A Diferença aparece na hora: mais sessenta reais, em verde.
O motivo é obrigatório: contagem do cofre. Confirmar ajuste.
O ajuste fica no histórico com a etiqueta Ajuste. É acerto de contagem: não entra como receita nem como despesa.""",
4: """Hoje cedo, o Rafael também fez três coisas no banco: pagou o combustível da picape por Pix, trouxe dinheiro da Conta Secundária e sacou no caixa eletrônico. Cada uma tem o seu jeito de registrar.
O combustível é gasto de verdade. Nova Movimentação, tipo Saída, na Conta Principal.
Descrição, combustível da picape. Valor, trezentos e cinquenta reais. Categoria Combustível e centro de custo Frota.
Essa opção de não contar na dê-érri-ê é pra saldo herdado de outro sistema. Combustível é despesa, então ela fica desmarcada. Salvar.
Uma dica: transferência entre contas suas, saque e depósito só mudam o dinheiro de lugar. A empresa não fica mais rica nem mais pobre, então nada disso entra na dê-érri-ê.
Por isso a transferência tem tipo próprio. De onde saiu, a Conta Secundária. Pra onde foi, a Conta Principal. Oito mil reais, e a prévia mostra a saída e a entrada.
Transferir. Repara que nem pediu categoria: é dinheiro da empresa trocando de conta.
Agora o saque, que vai da Conta Principal pro cofre.
Dois mil reais. O banco cobrou tarifa? Sim, seis reais e cinquenta.
Antes de confirmar, os efeitos: o banco perde o saque mais a tarifa, e o cofre ganha só o saque. A tarifa, essa sim, vira uma despesa separada.
Confirmar Saque. O caminho contrário, levar dinheiro do cofre pro banco, é a Sangria, aqui do lado. Também só muda o dinheiro de lugar.
Uma dica: sem o cofre ligado, o saque vai pra um caixa aberto. Nesse caso, abra o caixa antes de sacar.""",
5: """Com as contas em dia, a conciliação. Conciliar é conferir cada linha do extrato do banco com um lançamento do sistema.
Quando toda linha tem par, a diferença entre o saldo do banco e o do sistema chega a zero.
E a linha que sobra mostra o que ficou sem lançar, como uma tarifa que ninguém viu. É isso que deixa o fechamento do mês certo.
Na tela, é a aba Conciliação. A conta já vem escolhida: a Conta Principal.
E se bater dúvida, o Como funciona explica cada passo e cada botão. Primeiro, o extrato do banco.""",
6: """O extrato sai do site ou do app do banco. Você abre o extrato, escolhe o período e exporta no formato ó-éfe-xis. O pê-dê-éfe serve pra ler; pra conciliar, é o ó-éfe-xis.
Em Importar novo extrato, o próprio sistema ensina a achar o arquivo. Em alguns bancos ele tem outro nome, como Gerenciador Financeiro ou Conciliação bancária.
Escolho o arquivo que baixei, de um a dez de novembro.
Antes de importar, a prévia: o período, dezessete transações e o saldo final que o banco informou.
Importar. Se um dia você subir o mesmo período de novo, o sistema reconhece o que já entrou e não duplica.
Pronto. À esquerda, cada linha do banco, com a data e o valor. À direita, o que fazer com ela.
Uma dica: repara no sinal. Entrada vem em verde, com mais. Saída, em vermelho, com menos. Se alguma linha vier com o sinal trocado, confira com o banco antes de casar.
No rodapé ficam os três números do fechamento. A gente volta neles no fim.""",
7: """Começa pelo mais fácil. Nesta linha, o Pix de dois mil duzentos e cinquenta reais pro Depósito Irmãos Siqueira, o sistema já achou o par: a compra do dia três.
Confiro a data e o parceiro, e caso. A linha fica como Casada.
As outras sugestões vão do mesmo jeito: o aluguel, a energia, o Pix da Aços Quiririm, o combustível, o saque e a tarifa dele. Cada uma eu confiro antes de casar.
Agora, os oito mil que vieram da Conta Secundária. Esse dinheiro já está no sistema: é a transferência que a gente registrou.
Então é em Mais ações, Casar com transferência. Aparece a transferência certa, da Conta Secundária pra Conta Principal.
Casar transferência. Isso só liga a linha à transferência: não cria nada novo e o saldo não muda.
Uma dica: pra dinheiro que veio de outra conta sua, o caminho é sempre esse. Criar receita lançaria o valor de novo, e o saldo ficaria em dobro.""",
8: """Esta linha é o boleto da água, duzentos e trinta e oito reais e quarenta. Lembra da conta de água que estava vencida? Ela foi paga no banco, mas a baixa ficou pra trás.
Baixar conta. A lista traz só as contas em aberto do mesmo valor: a água e esgoto de outubro.
Dar baixa. A linha fica como Baixada, e em Contas a Pagar e Receber a água já aparece como Paga.
Por aqui, a baixa é sempre do valor inteiro. Pagamento em parte, você faz na tela de Contas a Pagar e Receber.""",
9: """Esta outra linha não existe em lugar nenhum do sistema: a tarifa do pacote do banco, sessenta e quatro reais e noventa.
Em Mais ações ficam todos os destinos de uma linha. O Funcionário, por exemplo, é pro vale pago por Pix.
Uma dica: vale que já foi lançado na tela de Funcionários se casa com o Buscar lançamento, sem criar de novo. O próprio painel do Funcionário lembra disso.
Pra tarifa, é Criar despesa. A descrição já vem do extrato. E a chave Não é receita nem despesa fica desligada, porque tarifa é gasto de verdade.
A categoria é obrigatória: Tarifas. E o botão já mostra o valor.
Criar. A linha fica como Criada, e a tarifa entra no histórico da conta como despesa.""",
10: """Este Pix da Serra Fina Alumínio caiu no dia nove: quatro mil oitocentos e quinze reais. E o sistema não sugeriu nada.
É que a venda foi registrada no dia três, por quatro mil oitocentos e quinze reais e vinte. A Serra Fina pagou depois e deixou os centavos de fora.
Em vez de criar outra receita, a gente procura a venda que já existe. Mais ações, Buscar lançamento.
Digito Serra. A busca aceita até dois reais de diferença e casa mesmo com a data diferente. Olha a venda, com vinte centavos a menos.
Casar com selecionado. O sistema confirma: casar com valor diferente?
Casar assim. A diferença não vira lançamento. Ela fica guardada no rodapé, em Diferenças casadas, pra quem quiser conferir.""",
11: """Estas duas linhas se anulam: o banco cobrou doze reais de tarifa por engano e devolveu no mesmo dia.
Nenhuma das duas precisa virar lançamento. Pra isso existe o Ignorar: a linha sai da fila sem criar nada.
Marco as duas. A soma dá zero.
Ignorar. O sistema confirma, e as duas ficam como Ignorada. Dá pra desfazer depois, se precisar.
Uma dica: ignorar conta como resolvido. Ignore só o que não mexeu no dinheiro da empresa, como esse par. Uma tarifa de verdade ignorada deixa a diferença aberta, e o fechamento não libera.""",
12: """Agora, duas linhas parecidas: dois Pix de trezentos e oitenta reais no mesmo dia. Um foi pra Cooperativa Recomeço; o outro, pra Auto Peças Vale Forte.
Aqui o sistema pede que você escolha. Casar com a compra errada deixaria a outra pendente pra sempre.
Escolher lançamento. A lista mostra as duas compras, e o nome no extrato diz qual é: a da Cooperativa Recomeço.
Marco a compra da cooperativa, e Casar com o selecionado.
Repara: a outra linha ficou com um par só, e a sugestão já vem certa. É só casar.
Uma dica: quando aparecer esse aviso, escolha pelo nome e pela data do extrato. Assim nenhuma compra fica pendente nem vira lançamento em dobro.""",
13: """Errou alguma? Toda linha resolvida tem o Desfazer, que devolve a linha pra pendente. Casada e Ignorada desfazem na hora.
Aqui eu só desfiz pra mostrar, então caso de novo.
Já a Criada e a Baixada mexem em dinheiro. O Desfazer delas pede confirmação, porque apaga o lançamento criado ou estorna a baixa.
E o Cancelar conciliação desfaz o arquivo inteiro de uma vez: os vínculos, os lançamentos criados e as baixas. Por segurança, pede pra digitar a palavra cancelar. Aqui eu mantenho a conciliação.
Já o Voltar só sai da tela. O progresso fica salvo, e o Continuar retoma de onde parou, até no dia seguinte.
Uma dica: lançamento conciliado não sai pelo Excluir das movimentações. Primeiro você desfaz a linha aqui, e depois exclui lá.""",
14: """Hora de fechar. No rodapé, o Saldo do banco é o saldo final que veio no arquivo. O Saldo conciliado é o que o sistema soma com as linhas resolvidas.
A Diferença é a distância entre os dois. Agora ela está em zero, em verde, e não sobrou nenhuma linha pendente.
Os vinte centavos da Serra Fina ficam aqui, só pra conferência. Eles não travam o fechamento.
Uma dica: se a diferença não zerar, falta lançamento, sobra lançamento ou alguma linha foi ignorada sem motivo. Cada linha se resolve de verdade, sem lançamento pra forçar o zero, e é isso que deixa o fechamento confiável.
Finalizar conciliação. Pronto: esse extrato fica selado, só pra leitura.
Ele vai pra Conciliações anteriores, com o selo Conciliado. No próximo extrato, é só importar e seguir do mesmo jeito.""",
15: """Pronto! Recapitulando: a gente cadastrou a Conta Cooperativa com o saldo inicial e arquivou a poupança que ninguém usava.
Ajustou o cofre pelo caminho certo e registrou o combustível, a transferência e o saque, cada um do seu jeito.
Importou o extrato do banco e casou as linhas com os lançamentos, inclusive a transferência entre as contas.
Deu baixa na conta de água pelo extrato, criou a tarifa, aceitou a diferença de centavos e ignorou o par de tarifa e estorno.
Escolheu o lançamento certo entre os valores repetidos e finalizou a conciliação com diferença zero.
No próximo tutorial, a gente responde a pergunta que todo dono faz: eu ganhei ou perdi dinheiro esse mês? Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: 'A tela e as contas.',
           2: 'Cadastrar e arquivar contas.',
           3: 'O cofre e o ajuste de saldo.',
           4: 'Movimentação, transferência e saque.',
           5: 'O que é conciliar.',
           6: 'Importar o extrato.',
           7: 'Casar com o sistema.',
           8: 'Baixar uma conta.',
           9: 'Criar um lançamento.',
           10: 'Buscar e aceitar centavos.',
           11: 'Ignorar uma linha.',
           12: 'Valores repetidos.',
           13: 'Desfazer e cancelar.',
           14: 'Fechar a conciliação.',
           15: 'Recapitulando.'}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: 'Bancos',
           2: 'Bancos',
           3: 'Cofre',
           4: 'Movimentações',
           5: 'Conciliação',
           6: 'Conciliação',
           7: 'Conciliação',
           8: 'Conciliação',
           9: 'Conciliação',
           10: 'Conciliação',
           11: 'Conciliação',
           12: 'Conciliação',
           13: 'Conciliação',
           14: 'Fechamento',
           15: 'Resumo'}

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
