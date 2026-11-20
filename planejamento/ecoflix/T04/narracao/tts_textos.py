# Texto para o ElevenLabs (eleven_v4, voz Kaik Barreto) por capítulo do T4 "Clientes, fornecedores e a ficha do parceiro".
# Uma linha do texto = uma linha da tabela Tela | Fala do roteiro.md, na grafia de pronúncia do PERFIL.
# Trocas em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   SEFAZ -> "sefás" | PDF -> "pê-dê-éfe" | EcoTray -> "Ecotrêi" | ICMS -> IPA do PERFIL
#   Cliente+Fornecedor -> "Cliente-mais-Fornecedor" | PET -> "pét" (testar as duas num trecho curto)
# 20/11 (app 1.60.18): 18 capítulos (0 a 17). Novos: 5 (Empresa do Lucro Real), 6 (Os avisos da consulta), 9 (Organizar a lista) e
# 13 (Ajustes na conta-corrente); o 4 foi refeito (O que falta pra emitir nota). Os antigos 5 a 13 viraram 7, 8, 10, 11, 12, 14, 15, 16, 17.
CAPS = {
0: """Oi! Neste tutorial a gente vai montar a base de quem entra e sai do pátio da Recicla Vale Metais.
De um lado, quem traz sucata: o carroceiro, a cooperativa, a oficina. Do outro, quem leva: a siderúrgica, a fundição.
E entre os dois fica o saldo: quem está te devendo, e quem tem crédito com você. É isso que a gente vai aprender a ler.
Se você ainda não viu o tutorial Materiais e tabelas de preço, dá uma olhada antes.
Tudo isso fica no menu, em Clientes e Fornecedores. Eu recolho o menu do lado, pra lista ficar mais larga. [pause] Vamos ver como a tela está organizada.""",
1: """A tela tem duas listas, nas abas Clientes e Fornecedores.
Cliente é pra quem a Recicla Vale vende: sai material, entra dinheiro. Fornecedor é de quem ela compra: entra material, sai dinheiro.
Em cada linha ficam o nome, o documento e, na direita, o saldo, numa etiqueta colorida. Daqui a pouco a gente aprende a ler essa cor.
Em cima, a busca, que acha por nome, apelido, documento ou telefone. Do lado, os filtros e a ordem da lista.
Clicando num parceiro, a ficha dele abre do lado. Ela tem um capítulo só dela, mais pra frente.
Lá em cima ficam o Relatório, com quem te deve e a quem você deve, e o botão de cadastrar, Novo Cliente.
Na aba Fornecedores, repara nesse telefone pequeno do lado do nome. É o aviso de mesmo telefone em outro cadastro.
Uma dica: muitas vezes é a mesma pessoa cadastrada duas vezes, com nomes diferentes. Buscando pelo telefone, os dois aparecem juntos, e você confere. E na hora de cadastrar, a tela já avisa quando o telefone ou o documento que você digitou já existem.
E na Visão geral fica o resumo: quem mais comprou da Recicla, de quem ela mais comprou, e quanto há pra receber e pra pagar.""",
2: """Agora, cadastrar. Chegou um fornecedor novo: o Rogério, eletricista, que traz fio de cobre e sucata de obra. Em Fornecedores, Novo Fornecedor.
O único campo obrigatório é o Nome. Eu escrevo Rogério Alves Costa.
Em Pessoa de Contato ou Apelido vai o jeito que o pátio chama ele: Rogério Eletricista. O apelido também entra na busca.
Depois, o telefone. Se a pessoa não tem telefone, como muito carroceiro, é só marcar Não possui telefone.
E a chave Pix dele, pra pagar as compras.
E repara nas caixinhas de Mostrar no comprovante: elas decidem se o telefone e a chave Pix do parceiro saem impressos no comprovante.
Lá embaixo fica o Saldo inicial. Se o parceiro já chega com um valor do caderno antigo, você escolhe o lado, eu devo a ele ou ele me deve, e põe o valor. O Rogério começa do zero, então eu deixo sem.
Na aba Dados Fiscais, o tipo já vem em Pessoa Física, que é quem tem CPF, como o Rogério. Eu digito o CPF dele.
Salvar. Pronto, o Rogério já está na lista.
Pra empresa, é o mesmo cadastro, com Pessoa Jurídica. Aí aparecem o CNPJ, a razão social e a inscrição estadual. E o CNPJ tem um atalho.""",
3: """O atalho é a busca pelo CNPJ. Chegou mais um fornecedor: a Serralheria Bem-Te-Vi, que vende sobra de ferro e de alumínio pra Recicla Vale.
Em Dados Fiscais, Pessoa Jurídica, e eu preencho o CNPJ.
Do lado do CNPJ fica uma lupa: Buscar dados da empresa pelo CNPJ. Um clique, e o sistema consulta a Receita e o cadastro de inscrição estadual.
Pronto. A tela pede pra conferir antes de salvar. Vieram a razão social e o nome fantasia.
E o endereço: CEP, cidade, rua e bairro.
Em Dados de Contato entraram o telefone e o e-mail. E o nome que eu digitei ficou do jeito que estava.
E repara nesse aviso amarelo, em cima: falta um campo pra emitir nota fiscal.""",
4: """O aviso amarelo lista o que a nota fiscal exige e a consulta não trouxe. Aqui, só o Número.
Clicando no nome do campo, a tela me leva direto pra ele. E a linha vermelha explica: o Número é obrigatório pra emitir nota fiscal.
A nota leva o endereço completo do parceiro. Sem o número, a sefás pode recusar a nota. Por isso a tela já cobra o que falta.
Eu completo com o número, quatrocentos e dezoito, e o aviso some.
Agora, a inscrição estadual. A consulta também foi buscar esse número no cadastro do estado, e achou.
Um clique em Usar a da Sintegra preenche a inscrição e já marca a serralheria como contribuinte de /iˈseˈɛmiˈɛːsːi/. Os dois campos andam juntos, do jeito que a nota pede.
O regime também veio: Simples Nacional. E é o regime da serralheria, não o da Recicla Vale.
Uma dica: a consulta adianta o trabalho, mas quem confirma inscrição e regime é o contador. Na dúvida, manda a ficha pra ele antes da primeira nota.
Salvar. Na lista, a serralheria ganha o sinal verde: pronta pra emitir nota fiscal.
Já o Rogério, que a gente cadastrou sem endereço, aparece com o triângulo de incompleto. O aviso mostra o que falta pra nota.
Pra completar, é só editar. Eu digito o CEP, e a cidade, a rua e o bairro vêm sozinhos. Ponho o número, salvo, e o Rogério também fica pronto pra nota.
E o botão de incompletos, lá em cima, mostra só quem ainda está com o cadastro pela metade.
Uma dica: quem não emite nota pode deixar a aba Dados Fiscais de lado. Só com o nome, o parceiro já tem histórico e saldo, e o aviso não trava compra nem venda.""",
5: """Agora, um cliente grande. A Aços Quiririm é uma siderúrgica, e a Recicla Vale emite nota fiscal pra ela. Em empresa assim, três campos decidem se a nota sai certa. Vou abrir o cadastro dela, no Editar, em Dados Fiscais.
A lupa também serve pra conferir um cadastro antigo. Um clique, e o sistema consulta de novo.
Primeiro, a inscrição estadual. Olha o aviso: o número que estava na ficha é diferente do que o estado informa. Alguém digitou errado lá atrás.
Repara que o sistema não trocou nada sozinho. Ele mostra os dois números e deixa a escolha com você.
Eu clico em Usar a da Sintegra, e a ficha fica com o número certo. Inscrição errada pode fazer a nota ser recusada.
Segundo, o Indicador. Contribuinte de /iˈseˈɛmiˈɛːsːi/ é a empresa que tem inscrição estadual, como a siderúrgica. Isento de Inscrição é a empresa que o estado dispensou. E Não Contribuinte é quem não tem inscrição, como a pessoa física.
Só o contribuinte leva o número da inscrição. Nos outros dois, o campo fica travado, e tem que ficar vazio mesmo.
Terceiro, o regime tributário do cliente. A consulta preencheu Lucro Real, e disse de onde tirou: da escrituração de dois mil e vinte e quatro.
Esse dado vem com atraso. Por isso a tela pede: confirma com o contador se mudou desde então.
As opções são Simples Nacional, MEI, Lucro Presumido e Lucro Real. E tem o Não informado: se você não sabe, deixa assim. O sistema não chuta regime.
Uma dica: aqui vai o regime da Aços Quiririm, não o da Recicla Vale. O da sua empresa fica na Configuração Fiscal, e a gente vê no tutorial de nota fiscal.
No cadastro de cliente tem mais dois botões. É Indústria: ligado, ele ativa o diferimento de /iˈseˈɛmiˈɛːsːi/ automático nas vendas pra esse cliente. A siderúrgica é indústria, então eu ligo.
E É uma Reciclagem, pra quando o cliente é outro pátio. Quem diz qual dos dois vale pra cada cliente é o contador.
Salvar. A Aços Quiririm está com a inscrição, o regime e o tipo certos. Quando chegar a hora da nota, o sistema já sabe com quem está falando.
E cliente novo é a mesma janela do fornecedor, em Novo Cliente, com esses dois botões a mais.""",
6: """A consulta também avisa quando tem problema. Chegou a Oficina do Tonho, querendo vender sucata com nota. Eu ponho o CNPJ e clico na lupa.
Olha o aviso vermelho: a Receita informa que esse CNPJ está baixado. A empresa foi encerrada.
Nota fiscal pra CNPJ baixado costuma ser recusada pela sefás. Melhor descobrir aqui do que depois de emitir.
Embaixo, outro aviso: o estado não tem inscrição ativa pra esse CNPJ. Se a empresa for isenta, você marca Isento de Inscrição, em vez de deixar o campo vazio.
E se você digitou o CNPJ errado? É só corrigir. Quando o CNPJ muda, o sistema apaga o que tinha trazido da empresa anterior, pra não misturar dado de duas empresas. O que você digitou à mão, ele mantém. E se esse CNPJ já está cadastrado, a tela avisa na hora.
Uma dica: se a consulta da inscrição disser que atingiu o limite, é só esperar um minuto e clicar de novo. Ela aceita três consultas por minuto.""",
7: """Agora, um caso comum no pátio. A serralheria vende sobra pra Recicla Vale, e também compra tubo e chapa usados aqui. Ela é fornecedora e cliente ao mesmo tempo.
Pra isso, é só editar e marcar Também é cliente.
Salvar. A serralheria ganha o selo roxo, Cliente-mais-Fornecedor, e passa a aparecer nas duas abas.
Se marcou por engano, o botão Desvincular, aqui no Editar, separa os dois de novo. E se o cliente já existia com o mesmo CNPJ, o sistema só liga um cadastro no outro.
E o saldo? Olha o Depósito Irmãos Siqueira, que já é cliente e fornecedor faz tempo.
Na semana passada, a Recicla comprou dois mil e cem reais de sucata dele, sem pagar na hora. E vendeu pra ele mil duzentos e sessenta reais de papelão e pét, também pra acertar depois.
Em vez de dois saldos, fica um só, com a conta das duas coisas: a Recicla deve oitocentos e quarenta reais pro depósito.
Na aba Clientes, ele aparece do mesmo jeito: o mesmo valor, o mesmo vermelho. É um saldo só, e a Recicla deve.""",
8: """Agora, a tabela de preço. No tutorial de materiais, a gente criou a Tabela Depósitos. Vou ligar ela ao Depósito Irmãos Siqueira.
No Editar, em Tabela de Preços Padrão, ele estava na Principal. Eu troco pra Tabela Depósitos.
Como o depósito também é cliente, o aviso azul lembra: a tabela vale pro cadastro de cliente dele também.
Salvar. Daqui pra frente, quando você escolher o depósito numa compra, os preços já vêm da Tabela Depósitos.
E se tiver preço especial? Na compra, vale primeiro o preço especial do parceiro. Se não tiver, a tabela dele. E por último, o preço do material.
O preço especial de cada parceiro fica na ficha dele, na aba Preços. Tem um lado pra compra e outro pra venda.
O filtro Já comprados mostra só o que esse fornecedor já trouxe. Fica fácil achar o material.
Cada material tem um estado. Herda segue a tabela do parceiro. Fixo é um preço combinado, que não muda quando a tabela muda. Eu combino o ferro pesado do depósito a um real o quilo.
E Vinculado acompanha uma tabela com uma diferença, pra cima ou pra baixo.
Salvar preços. Em Personalizados ficam só os combinados desse parceiro.""",
9: """Com a lista crescendo, vale organizar. Em Configurações ficam as etiquetas e os campos personalizados.
Etiqueta é uma marca colorida pra separar os parceiros. Eu crio a etiqueta Carroceiro, escolho uma cor e salvo.
Nos campos personalizados, você cria uma informação sua, como a placa do veículo, e ela entra no cadastro do parceiro.
No cadastro do Valdir, em Etiqueta, eu marco Carroceiro.
Nos Filtros, dá pra ver só quem está com saldo, ou só uma etiqueta. Com saldo, sobram os três fornecedores com conta aberta.
E no Ordenar, a lista vai por código, nome, saldo, documento ou telefone.
Nos três pontinhos de cada linha ficam os atalhos: editar, excluir, o portal e a movimentação. A exclusão não tem volta, então confere antes.""",
10: """Agora, a ficha. Vou abrir a Cooperativa Recomeço, que traz papelão, pét e latinha toda sexta.
No topo ficam o nome, o saldo e os botões de editar e de lançar uma movimentação.
Embaixo, as abas: Visão geral, Pedidos, Conta-corrente, Lucro estimado, Financeiro, Notas fiscais e Preços.
Na Visão geral ficam os dados do cadastro, o contato e o endereço.
E o link do portal, pra cooperativa acompanhar o saldo de onde estiver. O portal depende do plano contratado.
O Lucro estimado só aparece pra quem é fornecedor, porque ele parte das compras.""",
11: """Em Pedidos fica o resumo das compras. Desde agosto, a Recicla fez catorze pedidos com a cooperativa.
O gráfico mostra os cinco materiais que ela mais traz. E ele conta o peso, em quilos.
O papelão sozinho é cinquenta e nove por cento de tudo que chega da cooperativa.
Já a latinha é só nove por cento do peso. Mas o quilo da latinha vale seis e vinte, e o do papelão, cinquenta e cinco centavos.
No Período, dá pra olhar um mês só. E embaixo fica cada pedido, com o valor e a data.""",
12: """Agora, a conta-corrente. A cooperativa entregou na sexta, e a Recicla ainda não acertou tudo: deve dois mil quinhentos e cinquenta reais pra ela.
Por isso o valor está em vermelho, com a frase: Você deve a Cooperativa Recomeço.
Uma dica: pra ler qualquer saldo, pensa sempre do lado da Recicla Vale. Verde é dinheiro pra receber. Vermelho é dinheiro pra pagar.
No cliente, saldo positivo é verde: ele te deve. Saldo negativo é vermelho: ele adiantou dinheiro, e você deve a ele.
No fornecedor é ao contrário. Positivo é vermelho: você deve a ele, como aqui. Negativo é verde: você adiantou, e ele te deve.
Embaixo fica o extrato: cada pedido que ficou pra acertar e cada pagamento, com o saldo depois de cada um.
Hoje a Recicla vai acertar uma parte. Em Movimentação, o tipo já vem em Pagar.
O valor: mil e duzentos reais.
A forma de pagamento é Pix ou transferência, saindo da conta da empresa. Em Observação, eu anoto o motivo.
Confirmar. O saldo cai pra mil trezentos e cinquenta reais, e o pagamento entra no extrato.
E no Exportar, o extrato sai em pê-dê-éfe, resumido ou detalhado, ou em planilha, pra mandar pro parceiro.
O pê-dê-éfe detalhado mostra, em cada pedido, os materiais, o peso e o preço.""",
13: """Na Movimentação tem mais duas coisas. O tipo Receber, pra quando o fornecedor te devolve dinheiro. E a forma Dinheiro, que sai do caixa e só funciona com um caixa aberto.
E quando o acerto não envolve dinheiro? A cooperativa aceitou um desconto de cinquenta reais, porque o papelão de sexta veio molhado. Pra isso existe o Crédito/débito.
Eu escolho a direção que abate o que eu devo a ele. Ponho cinquenta reais, e a tela já mostra a conta: o saldo de hoje e como fica depois.
O motivo é obrigatório. Confirmo, e o saldo cai pra mil e trezentos. Esse lançamento mexe só no saldo: não passa pelo caixa nem pelo banco.
Lancei errado? Cada linha do extrato tem um lápis, pra corrigir, e uma lixeira, pra excluir.
A cooperativa mudou de ideia, então eu excluo. A tela mostra o que vai ser desfeito, eu confirmo, e o saldo volta pra mil trezentos e cinquenta reais.
Uma dica: excluir um pagamento desfaz tudo junto, o saldo do parceiro e a saída do banco. Se ele já estiver conciliado com o extrato do banco, o sistema pede pra desfazer a conciliação antes.
E o lápis do lado do Saldo Atual é só pra correção: ele define o valor final do saldo, direto. No dia a dia, use a Movimentação e o Crédito/débito, que deixam o histórico explicado.
No filtro Data, você olha um período só. E clicando num pedido, os materiais dele abrem ali mesmo.""",
14: """Agora, o Lucro estimado: quanto cada material dessa cooperativa deixa pra Recicla Vale. Eu escolho o Mês passado, outubro inteiro.
Olha a latinha: a Recicla pagou seis e vinte o quilo e vendeu, em média, a sete e quarenta. Sobra um e vinte por quilo, e essa diferença é a margem.
E o papelão, que vale pouco, dá a maior margem no total, porque vem muito: dois mil e cem reais no mês.
Somando tudo, a margem estimada da cooperativa em outubro foi de cinco mil novecentos e noventa e oito reais.
Uma dica: esse número é uma estimativa, não é dinheiro no bolso. O aviso da tela diz: sucata é fungível.
Fungível quer dizer que se mistura. A latinha da cooperativa vai pro mesmo fardo da latinha da Dona Cida e de todo mundo. Na venda, ninguém separa de quem era cada lata.
Por isso a margem usa o preço médio de venda do material no mês. Ela não vai bater com o extrato, e tudo bem: ela mostra quanto cada material desse fornecedor rende.""",
15: """Agora, o Financeiro. Aqui ficam as despesas e as receitas avulsas ligadas ao parceiro, o que não é compra nem venda.
Na cooperativa, o frete das entregas de outubro, quatrocentos e cinquenta reais, e uma venda de sacos de ráfia usados, cento e vinte.
Elas aparecem aqui quando a despesa ou a receita é lançada com o nome do parceiro.
E em Notas fiscais ficam as notas desse parceiro. A cooperativa ainda não tem nenhuma. A emissão de nota depende do plano contratado e tem um tutorial só dela.""",
16: """Pra fechar, a pergunta do dia a dia: quem te deve, e quanto? Lá em cima, Relatório.
Em A Receber fica tudo que vai entrar: dezenove mil quinhentos e quarenta reais. A maior parte é da Fundição Bandeira do Vale, que comprou cobre em três vezes.
A Aços Quiririm é cliente, com saldo positivo e verde: ela te deve quatro mil oitocentos e setenta reais.
O Valdir é fornecedor, com saldo negativo, também verde. A Recicla adiantou trezentos reais pra ele, e ele paga em sucata.
Em A Pagar fica o que vai sair: três mil seiscentos e noventa reais.
A cooperativa é fornecedora, com saldo positivo e vermelho: são os mil trezentos e cinquenta reais que ficaram do acerto de hoje.
O depósito aparece uma vez só, como Cliente-mais-Fornecedor, com o saldo único.
E a Serra Fina é cliente, com saldo negativo e vermelho. Ela adiantou mil e quinhentos reais pela próxima carga de alumínio, e agora a Recicla deve essa carga pra ela.
No Exportar Relatório, a lista sai em pê-dê-éfe ou em planilha.
E no olho, você abre a conta-corrente do parceiro, com o extrato completo.""",
17: """Pronto! Recapitulando: a gente viu como a tela de clientes e fornecedores está organizada e cadastrou o Rogério, pessoa física.
Cadastrou a serralheria com a busca pelo CNPJ, que trouxe o endereço, a inscrição estadual e o regime, e completou o que faltava pra nota fiscal.
Conferiu o cadastro de um cliente do Lucro Real e viu os avisos que a consulta dá.
Marcou a serralheria como cliente e fornecedor, entendeu o saldo único, ligou a Tabela Depósitos ao depósito e organizou a lista com etiquetas e filtros.
Abriu a ficha da cooperativa, leu o gráfico de materiais, lançou um pagamento na conta-corrente, fez um ajuste de saldo e viu o lucro estimado.
E fechou com o relatório de quem te deve e a quem você deve.
No próximo tutorial, a balança e a impressora passam a conversar com o sistema, pelo Ecotrêi. Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "Como a tela está organizada.",
           2: "Pessoa física e pessoa jurídica.",
           3: "Buscar dados pelo CNPJ.",
           4: "O que falta pra emitir nota.",
           5: "Empresa do Lucro Real.",
           6: "Os avisos da consulta.",
           7: "Cliente e fornecedor ao mesmo tempo.",
           8: "Tabela de preço do parceiro.",
           9: "Organizar a lista.",
           10: "A ficha do parceiro.",
           11: "Os materiais que ele mais movimenta.",
           12: "Conta-corrente: saldo e extrato.",
           13: "Ajustes na conta-corrente.",
           14: "Lucro estimado.",
           15: "Financeiro e notas fiscais.",
           16: "Relatório de saldos.",
           17: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "Parceiros",
           2: "Cadastro",
           3: "Cadastro",
           4: "Fiscal",
           5: "Fiscal",
           6: "Fiscal",
           7: "Saldo",
           8: "Preços",
           9: "Parceiros",
           10: "Ficha",
           11: "Ficha",
           12: "Saldo",
           13: "Saldo",
           14: "Ficha",
           15: "Ficha",
           16: "Saldo",
           17: "Resumo"}

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
