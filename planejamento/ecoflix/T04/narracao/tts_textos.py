# Texto para o ElevenLabs (eleven_v4, voz Kaik Barreto) por capítulo do T4 "Clientes, fornecedores e a ficha do parceiro".
# Uma linha do texto = uma linha da tabela Tela | Fala do roteiro.md, na grafia de pronúncia do PERFIL.
# Trocas em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   SEFAZ -> "sefás" | PDF -> "pê-dê-éfe" | EcoTray -> "Ecotrêi"
#   novas: Cliente+Fornecedor -> "Cliente-mais-Fornecedor" | PET -> "pét" (testar as duas num trecho curto)
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
Uma dica: muitas vezes é a mesma pessoa cadastrada duas vezes, com nomes diferentes. Buscando pelo telefone, os dois aparecem juntos, e você confere.
E na Visão geral fica o resumo: quem mais comprou da Recicla, de quem ela mais comprou, e quanto há pra receber e pra pagar.""",
2: """Agora, cadastrar. Chegou um fornecedor novo: o Rogério, eletricista, que traz fio de cobre e sucata de obra. Em Fornecedores, Novo Fornecedor.
O único campo obrigatório é o Nome.
Em Pessoa de Contato ou Apelido vai o jeito que o pátio chama ele: Rogério Eletricista. O apelido também entra na busca.
Depois, o telefone. Se a pessoa não tem telefone, como muito carroceiro, é só marcar Não possui telefone.
E a chave Pix dele, pra pagar as compras.
Lá embaixo fica o Saldo inicial. Se o parceiro já chega com um valor do caderno antigo, você registra aqui. O Rogério começa do zero.
Na aba Dados Fiscais, o tipo já vem em Pessoa Física, que é quem tem CPF, como o Rogério. Eu digito o CPF dele.
Salvar. Pronto, o Rogério já está na lista.
Pra empresa, é o mesmo cadastro, com Pessoa Jurídica. Aí aparecem o CNPJ, a razão social e a inscrição estadual. E o CNPJ tem um atalho.""",
3: """O atalho é a busca pelo CNPJ. Chegou mais um fornecedor: a Serralheria Bem-Te-Vi, que vende sobra de ferro e de alumínio pra Recicla Vale.
Em Dados Fiscais, Pessoa Jurídica, e eu digito o CNPJ.
Do lado do CNPJ fica uma lupa: Buscar dados da empresa pelo CNPJ. Um clique, e o sistema consulta a Receita.
Pronto. Vieram a razão social e o nome fantasia.
E o endereço: CEP, cidade, rua e bairro.
Em Dados de Contato entraram o telefone e o e-mail. E o nome que eu digitei ficou do jeito que estava.
A tela pede pra conferir antes de salvar. E repara que um campo ficou vermelho.""",
4: """O campo vermelho é o Número. A Receita não trouxe o número da serralheria.
E o aviso explica: ele é obrigatório pra emitir nota fiscal.
A nota leva o endereço completo do parceiro. Sem o número, a sefás pode recusar a nota. Por isso a tela já cobra o que falta.
Eu completo com o número, quatrocentos e dezoito, e o vermelho some.
Aqui em cima ficam a inscrição estadual, o indicador e o regime do fornecedor. Quem define o que vai nesses campos é o contador. Eu preencho o que ele passou.
O regime até veio na consulta: Simples Nacional. E é o regime da serralheria, não o da Recicla Vale.
Salvar. Na lista, a serralheria ganha o sinal verde: pronta pra emitir nota fiscal.
Já o Rogério, que a gente cadastrou sem endereço, aparece com o triângulo de incompleto. O aviso mostra o que falta pra nota.
E o botão de incompletos, lá em cima, mostra só quem está com o cadastro pela metade.
Uma dica: quem não emite nota pode deixar a aba Dados Fiscais de lado. Só com o nome, o parceiro já tem histórico e saldo, e o aviso não trava compra nem venda.""",
5: """Agora, um caso comum no pátio. A serralheria vende sobra pra Recicla Vale, e também compra tubo e chapa usados aqui. Ela é fornecedora e cliente ao mesmo tempo.
Pra isso, é só editar e marcar Também é cliente.
Salvar. A serralheria ganha o selo roxo, Cliente-mais-Fornecedor, e passa a aparecer nas duas abas.
E o saldo? Olha o Depósito Irmãos Siqueira, que já é cliente e fornecedor faz tempo.
Na semana passada, a Recicla comprou dois mil e cem reais de sucata dele, sem pagar na hora. E vendeu pra ele mil duzentos e sessenta reais de papelão e pét, também pra acertar depois.
Em vez de dois saldos, fica um só, com a conta das duas coisas: a Recicla deve oitocentos e quarenta reais pro depósito.
Na aba Clientes, ele aparece com esse mesmo saldo. O sinal muda de uma aba pra outra, mas a cor continua vermelha: a Recicla deve.""",
6: """Agora, a tabela de preço. No tutorial de materiais, a gente criou a Tabela Depósitos. Vou ligar ela ao Depósito Irmãos Siqueira.
No Editar, em Tabela de Preços Padrão, ele estava na Principal. Eu troco pra Tabela Depósitos.
Como o depósito também é cliente, o aviso azul lembra: a tabela vale pro cadastro de cliente dele também.
Salvar. Daqui pra frente, quando você escolher o depósito numa compra, os preços já vêm da Tabela Depósitos.
E se tiver preço especial? Na compra, vale primeiro o preço especial do parceiro. Se não tiver, a tabela dele. E por último, o preço do material.
O preço especial de cada parceiro fica na ficha dele, na aba Preços.""",
7: """Agora, a ficha. Vou abrir a Cooperativa Recomeço, que traz papelão, pét e latinha toda sexta.
No topo ficam o nome, o saldo e os botões de editar e de lançar uma movimentação.
Embaixo, as abas: Visão geral, Pedidos, Conta-corrente, Lucro estimado, Financeiro, Notas fiscais e Preços.
Na Visão geral ficam os dados do cadastro, o contato e o endereço.
E o link do portal, pra cooperativa acompanhar o saldo de onde estiver. O portal depende do plano contratado.
O Lucro estimado só aparece pra quem é fornecedor, porque ele parte das compras.""",
8: """Em Pedidos fica o resumo das compras. Desde agosto, a Recicla fez catorze pedidos com a cooperativa.
O gráfico mostra os cinco materiais que ela mais traz. E ele conta o peso, em quilos.
O papelão sozinho é cinquenta e nove por cento de tudo que chega da cooperativa.
Já a latinha é só nove por cento do peso. Mas o quilo da latinha vale seis e vinte, e o do papelão, cinquenta e cinco centavos.
No Período, dá pra olhar um mês só. E embaixo fica cada pedido, com o valor e a data.""",
9: """Agora, a conta-corrente. A cooperativa entregou na sexta, e a Recicla ainda não acertou tudo: deve dois mil quinhentos e cinquenta reais pra ela.
Por isso o valor está em vermelho, com a frase: Você deve a Cooperativa Recomeço.
Uma dica: pra ler qualquer saldo, pensa sempre do lado da Recicla Vale. Verde é dinheiro pra receber. Vermelho é dinheiro pra pagar.
No cliente, saldo positivo é verde: ele te deve. Saldo negativo é vermelho: ele adiantou dinheiro, e você deve a ele.
No fornecedor é ao contrário. Positivo é vermelho: você deve a ele, como aqui. Negativo é verde: você adiantou, e ele te deve.
Embaixo fica o extrato: cada pedido que ficou pra acertar e cada pagamento, com o saldo depois de cada um.
Hoje a Recicla vai acertar uma parte. Em Movimentação, o tipo já vem em Pagar.
O valor: mil e duzentos reais.
A forma de pagamento é Pix ou transferência, saindo da conta da empresa. Em Observação, eu anoto o motivo.
Confirmar. O saldo cai pra mil trezentos e cinquenta reais, e o pagamento entra no extrato.
E no Exportar, o extrato sai em pê-dê-éfe ou em planilha, pra mandar pro parceiro.""",
10: """Agora, o Lucro estimado: quanto cada material dessa cooperativa deixa pra Recicla Vale. Eu escolho o Mês passado, outubro inteiro.
Olha a latinha: a Recicla pagou seis e vinte o quilo e vendeu, em média, a sete e quarenta. Sobra um e vinte por quilo, e essa diferença é a margem.
E o papelão, que vale pouco, dá a maior margem no total, porque vem muito: dois mil e cem reais no mês.
Somando tudo, a margem estimada da cooperativa em outubro foi de cinco mil novecentos e noventa e oito reais.
Uma dica: esse número é uma estimativa, não é dinheiro no bolso. O aviso da tela diz: sucata é fungível.
Fungível quer dizer que se mistura. A latinha da cooperativa vai pro mesmo fardo da latinha da Dona Cida e de todo mundo. Na venda, ninguém separa de quem era cada lata.
Por isso a margem usa o preço médio de venda do material no mês. Ela não vai bater com o extrato, e tudo bem: ela mostra quanto cada material desse fornecedor rende.""",
11: """Agora, o Financeiro. Aqui ficam as despesas e as receitas avulsas ligadas ao parceiro, o que não é compra nem venda.
Na cooperativa, o frete das entregas de outubro, quatrocentos e cinquenta reais, e uma venda de sacos de ráfia usados, cento e vinte.
Elas aparecem aqui quando a despesa ou a receita é lançada com o nome do parceiro.
E em Notas fiscais ficam as notas desse parceiro. A cooperativa ainda não tem nenhuma. A emissão de nota depende do plano contratado e tem um tutorial só dela.""",
12: """Pra fechar, a pergunta do dia a dia: quem te deve, e quanto? Lá em cima, Relatório.
Em A Receber fica tudo que vai entrar: dezenove mil quinhentos e quarenta reais. A maior parte é da Fundição Bandeira do Vale, que comprou cobre em três vezes.
A Aços Quiririm é cliente, com saldo positivo e verde: ela te deve quatro mil oitocentos e setenta reais.
O Valdir é fornecedor, com saldo negativo, também verde. A Recicla adiantou trezentos reais pra ele, e ele paga em sucata.
Em A Pagar fica o que vai sair: três mil seiscentos e noventa reais.
A cooperativa é fornecedora, com saldo positivo e vermelho: são os mil trezentos e cinquenta reais que ficaram do acerto de hoje.
O depósito aparece uma vez só, como Cliente-mais-Fornecedor, com o saldo único.
E a Serra Fina é cliente, com saldo negativo e vermelho. Ela adiantou mil e quinhentos reais pela próxima carga de alumínio, e agora a Recicla deve essa carga pra ela.
No Exportar Relatório, a lista sai em pê-dê-éfe ou em planilha.
E no olho, você abre a conta-corrente do parceiro, com o extrato completo.""",
13: """Pronto! Recapitulando: a gente viu como a tela de clientes e fornecedores está organizada e cadastrou o Rogério, pessoa física.
Cadastrou a serralheria com a busca pelo CNPJ e completou o campo vermelho que a nota fiscal pede.
Marcou a serralheria como cliente e fornecedor, entendeu o saldo único e ligou a Tabela Depósitos ao depósito.
Abriu a ficha da cooperativa, leu o gráfico de materiais, lançou um pagamento na conta-corrente e viu o lucro estimado.
E fechou com o relatório de quem te deve e a quem você deve.
No próximo tutorial, a balança e a impressora passam a conversar com o sistema, pelo Ecotrêi. Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "Como a tela está organizada.",
           2: "Pessoa física e pessoa jurídica.",
           3: "Buscar dados pelo CNPJ.",
           4: "Dados fiscais e o campo vermelho.",
           5: "Cliente e fornecedor ao mesmo tempo.",
           6: "Tabela de preço do parceiro.",
           7: "A ficha do parceiro.",
           8: "Os materiais que ele mais movimenta.",
           9: "Conta-corrente: saldo e extrato.",
           10: "Lucro estimado.",
           11: "Financeiro e notas fiscais.",
           12: "Relatório de saldos.",
           13: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "Parceiros",
           2: "Cadastro",
           3: "Cadastro",
           4: "Fiscal",
           5: "Saldo",
           6: "Preços",
           7: "Ficha",
           8: "Ficha",
           9: "Saldo",
           10: "Ficha",
           11: "Ficha",
           12: "Saldo",
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
