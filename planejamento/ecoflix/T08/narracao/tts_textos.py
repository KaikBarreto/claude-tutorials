# Texto enviado ao ElevenLabs (eleven_v4, Kaik Barreto) por capítulo do T8 "Ticket de Pesagem".
# Gerado do roteiro.md (coluna Fala): cada linha do texto é uma linha da tabela Tela × Fala.
# Trocas de pronúncia em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   A4 -> "á-quatro" | EcoTray -> "Ecotrêi" | PDF -> "pê-dê-éfe"
# 18/11 (app 1.60.10): capítulos novos 7 (ticket com valores), 11 (pesagem avulsa com cobrança) e 12 (sem internet); os antigos 7, 8, 9 e 10
# viraram 8, 9, 10 e 13.
CAPS = {
0: """Oi! Neste tutorial a gente resolve a situação clássica do pátio: o caminhão chegou, precisa pesar agora, mas o preço ainda não está fechado.
Na Recicla Vale Metais, a Cooperativa Recomeço mandou um caminhão de latinha, e o preço só vai ser combinado depois.
Com o Ticket de Pesagem, você registra o peso agora e resolve o valor depois.
Se você ainda não viu o tutorial Comprar e vender sucata, dá uma olhada antes. [pause] Vamos ver quando usar o ticket.""",
1: """O ticket fica no menu Materiais, em Ticket de Pesagem.
Com o preço fechado, você faz a compra direto, como no tutorial anterior. Com o preço em aberto, você pesa no ticket e transforma em compra ou venda depois.
Ticket salvo é peso registrado, e só. Nenhum quilo entra no estoque e nenhum centavo entra ou sai do caixa por causa dele. Isso só acontece quando o pedido que nasce dele é finalizado.
Os tickets ficam aqui. Em Aguardando valorização, o que ainda espera o preço. Em Valorizados, o que já virou pedido.
Na aba Pesagens avulsas fica outro caso: quem só quer usar a balança, como o caminhão de areia de um vizinho.
A pesagem avulsa não vira pedido e não mexe no estoque. E, se você cobra pelo serviço, ela já lança o recebimento. A gente faz uma mais adiante.""",
2: """O caminhão da cooperativa chegou. Clico em Novo Ticket de Pesagem.
Em cima ficam três chaves: ticket padrão; compra, porque a gente vai comprar a latinha; e sem valores, porque o preço ainda não fechou.
Quando o preço já está combinado, dá pra fazer o ticket com valores, e ele já guarda o preço de cada material. A gente faz um assim mais adiante.
Agora o fornecedor. Se ele não quiser se identificar, existe a opção Não informado. E o pino, ao lado do nome, deixa um fornecedor fixo para os próximos tickets.
Aqui, o fornecedor é a Cooperativa Recomeço.
No card Pesagem, o material: alumínio latinha.
E, aqui dentro, o motorista e a placa. O Edson Moura e o caminhão dele já estão cadastrados, então é só escolher na lista.
Motorista novo? O botão de mais, ao lado do campo, abre o cadastro de motoristas sem sair do ticket. O mesmo vale para a placa.
Do lado direito fica a aba deste ticket, com o número, o peso e o fornecedor.""",
3: """O Edson sobe na balança com o caminhão cheio. A primeira pesagem vai na Pesagem avançada.
Na primeira pesagem, nove mil quatrocentos e sessenta quilos. Por enquanto, ela conta como bruto.
Com a balança ligada no Ecotrêi, o botão dentro do campo puxa esse peso sozinho.
E a dica embaixo mostra os três jeitos: as duas pesagens, só a primeira, ou o bruto digitado direto.
Em Como exibir no comprovante, eu marco Completo, pra sair a conta inteira no papel.
Confirmar. Agora o caminhão vai descarregar.
E não precisa fazer mais nada: o ticket fica salvo sozinho, como rascunho, a cada mudança.
Não existe um status de esperando a segunda pesagem. O ticket fica aqui, aberto, até o caminhão voltar. E esse número é só a previsão: o ticket ganha número quando é salvo.
Mesmo saindo da tela, o rascunho continua lá, em Rascunhos abertos.
Uma dica: quando o rascunho é reaberto, confira o que já estava preenchido antes de salvar.""",
4: """O caminhão descarregou e voltou vazio pra balança. A diferença entre as duas pesagens é a latinha que ficou no pátio.
No item, em Adicionar tara, pesagem avançada. O peso da entrada está no bruto.
A gente passa ele pra primeira pesagem e põe a segunda, com o caminhão vazio: seis mil trezentos e oitenta quilos.
Pronto: o bruto sai sozinho, a diferença das duas. Três mil e oitenta quilos de latinha.
A tara é o peso do que vem junto e não é material, como uma caçamba. Aqui o caminhão já saiu na segunda pesagem, então a tara fica em branco.
Confirmar, e a pesagem do item está atualizada.
Na linha, a setinha abre o detalhe, com as duas pesagens e o bruto.""",
5: """Falta a impureza. Na latinha sempre vem um pouco de sujeira e de água, e isso sai do peso.
Aqui ela vai em porcentagem: dois por cento. O sistema mostra quanto isso dá: sessenta e um quilos e seiscentos.
Se preferir, troca pra quilos e digita direto o peso da impureza.
E o líquido fecha a conta: o bruto, menos a tara, menos a impureza.
Três mil e dezoito quilos e quatrocentos. É esse peso que vale na compra.
Confirmar, e o ticket da cooperativa está pesado.""",
6: """Enquanto isso, chega o Jair Lopes, com o caminhão três quartos, trazendo bateria da Auto Peças Vale Forte.
Cada caminhão ganha a sua aba. Em Novo ticket, abre uma aba em branco.
Fornecedor, material, motorista, placa e a primeira pesagem: cinco mil seiscentos e quarenta quilos.
Na barra de cima, a gente troca de um caminhão pro outro. Cada aba guarda o seu rascunho, e nada se mistura.
O ticket da cooperativa está pronto, então eu salvo. Agora sim, ele ganha o número de verdade.
O valor a gente resolve depois. E a aba do Jair continua aberta, esperando ele descarregar.
Se alguém fechar uma aba no x, o sistema pergunta antes de descartar o ticket.
E se descartar sem querer, o rascunho vai para Rascunhos apagados, na tela dos tickets. Dali dá pra recuperar.""",
7: """O Jair descarregou. E com a Auto Peças o preço da bateria já está combinado. Então este ticket pode ser feito com valores.
Mudo a chave para Com valores. Aparecem a Tabela de Preços, embaixo do fornecedor, e as colunas de valor nos itens.
No item, eu completo a pesagem: a segunda deu quatro mil cento e oitenta quilos. E ponho o preço combinado: três e quarenta o quilo.
Confirmar. São mil quatrocentos e sessenta quilos de bateria, e o total do ticket aparece embaixo: quatro mil novecentos e sessenta e quatro reais.
Atenção: mesmo com valores, o ticket não paga ninguém. Ele só guarda o preço. O dinheiro continua saindo só quando a compra é finalizada.
Salvo o ticket do Jair. Ele vai para Aguardando valorização, já com o valor.
E, se quiser, o balanceiro já deixa a forma de pagamento escolhida no ticket com valores. É só ligar esta opção em Configurações, Usabilidade.""",
8: """Pouco depois, o preço com a cooperativa fechou. É hora de valorizar: transformar o peso em pedido.
Uma dica: se o mesmo fornecedor tem mais de um ticket esperando, marque Selecionar em cada um e use Valorizar dois tickets. Vira uma compra só. Precisa ser o mesmo fornecedor e o mesmo tipo.
Hoje eu valorizo só o ticket de hoje. Em Ações, Valorizar. O sistema abre uma compra já preenchida: a cooperativa, a latinha, o peso e a impureza.
O preço vem da tabela: seis e vinte o quilo. Dá dezoito mil setecentos e catorze reais e oito centavos.
O sistema procura o preço nesta ordem: o preço especial do fornecedor, se existir; depois a tabela dele; e por último a tabela padrão.
Se o preço combinado for outro, é só mudar o valor do quilo aqui, antes de finalizar. Num ticket de venda, abre uma venda do mesmo jeito.
Repara: até aqui, nada entrou no estoque e nada saiu do caixa. A compra está em rascunho, e o efeito só acontece quando ela for finalizada.""",
9: """O motorista leva o comprovante do ticket. Em Ações, Ver comprovante, e o formato: Térmico, o cupom, ou á-quatro, a folha.
Repara no papel: ticket de pesagem, não valorizado. É o comprovante do peso, ainda sem valor de compra.
Com o modo Completo, sai a conta inteira: o motorista, a placa, as duas pesagens, o bruto, a impureza e o líquido.
E se quiser que o cupom saia sozinho na impressora ao salvar cada ticket, ligue Imprimir comprovante do Ticket de Pesagem, em Configurações, Integrações.
Quer que o motorista assine o peso? Em Usabilidade, ligue Assinaturas no comprovante e escolha quem assina: os dois, só o fornecedor, ou só o operador.
No ticket de pesagem, o lado do operador sai escrito Empresa.
Aqui também ficam duas regras do ticket: tirar do papel a marca de não valorizado, e exigir o fornecedor para salvar.
Uma dica: se o ticket tiver pesagens do mesmo material mescladas numa linha, o comprovante mostra só a soma. Pra conferir cada pesagem no papel, use o Desmesclar pesagens antes de imprimir.""",
10: """E quando o ticket sai de Aguardando valorização? Mesmo com a compra em rascunho, ele continua aqui.
Enquanto ele espera, dá pra corrigir em Editar ou apagar em Excluir. Depois de valorizado, ele trava, e a correção passa a ser no pedido.
Valorizando de novo, o sistema retoma a mesma compra, sem duplicar.
Finalizo como no tutorial anterior: Pix, e confirmar pagamento. Agora sim, a latinha entrou no estoque e o pagamento saiu da conta.
E o sistema volta sozinho pro Ticket de Pesagem. O ticket passou pra Valorizados, com o número da compra. E, em Ações, o Ver pedido abre essa compra.
Na lista, cada ticket mostra a situação. São três: Aguardando valorização, em amarelo; Valorizado, em verde; e Cancelado.
O período, lá no alto, vale para a lista inteira. E os filtros separam por tipo, situação e usuário.
Em Exportar sai o relatório dos tickets, em pê-dê-éfe ou Excel, com o período, o tipo, a situação e o usuário que você escolher.
Um detalhe: o dono pode limitar um balanceiro a ver só os tickets que ele mesmo criou. Isso fica em Usuários e Permissões.
E o ticket do Jair segue em Aguardando valorização, já com o valor, esperando a vez dele.""",
11: """Agora o outro caso: um caminhão de areia, que não é fornecedor nem cliente da Recicla Vale, só quer usar a balança. E a empresa cobra por esse serviço.
Em Pesagens avulsas, Nova Pesagem Avulsa. O tipo já vem como Serviço ao cliente: aqui a empresa não compra nem vende, ela presta um serviço.
O dono do caminhão ainda não tem cadastro. Eu busco pelo nome, o sistema não acha, e oferece cadastrar com o que eu digitei.
O nome já vem preenchido. Dá pra completar telefone, CPF ou CNPJ e a chave Pix, que é novidade no cadastro rápido. Eu crio só com o nome, e o cliente já volta escolhido. Esse atalho vale também para o fornecedor, no ticket padrão.
Na pesagem avulsa não tem material cadastrado. Eu escrevo o que é: areia média.
E peso do mesmo jeito, entrada e saída: catorze mil setecentos e vinte quilos.
Depois a placa, o tipo de caminhão e o valor cobrado pela pesagem: sessenta reais.
Como tem valor, ao salvar o sistema pergunta como o cliente pagou: dinheiro, Pix, ou saldo do cliente, que é pôr na conta dele.
Foi no Pix. A conta que recebe já vem escolhida, e eu confirmo o pagamento.
Pronto. Os sessenta reais já entraram na conta, como receita de serviço de pesagem. Sem pedido e sem mexer no estoque. E repara: aqui não tem o botão Valorizar. Pesagem avulsa nunca vira compra ou venda.
O comprovante sai marcado como pesagem avulsa, sem valor comercial, com o peso e o valor da pesagem.
Atenção: depois de cobrada, o valor fica travado. E a pesagem não pode ser excluída sem antes estornar o recebimento.
Se fosse no saldo, o cliente ficava devendo, e nascia uma conta a receber. Dá pra dividir entre as três formas. E, sem valor nenhum, a avulsa é só o comprovante de peso.""",
12: """E se a internet cair com o caminhão em cima da balança? O ticket continua funcionando.
O sistema avisa que está sem internet, e você pesa e salva normalmente. O ticket fica guardado neste computador.
O comprovante do motorista sai como provisório, sem o número oficial. Quando a conexão volta, o ticket sobe sozinho e ganha o número de verdade.
Só três coisas esperam a internet: valorizar, editar um ticket já salvo e anexar foto.""",
13: """Pronto! Recapitulando: a gente criou o ticket da cooperativa com o fornecedor, o material, o motorista e a placa.
Fez a primeira pesagem na entrada, viu o rascunho salvo sozinho e fez a segunda na saída, com o bruto saindo sozinho.
Aplicou a impureza em porcentagem, atendeu um segundo caminhão em outra aba e salvou o ticket dele com valores.
Valorizou o ticket da cooperativa, que virou uma compra já preenchida, imprimiu o comprovante e viu o ticket ir pra Valorizados quando a compra foi finalizada.
E ainda fez uma pesagem avulsa, cobrando pelo serviço, e viu que o ticket continua funcionando sem internet.
No próximo tutorial, a gente acha e corrige um pedido antigo. Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "Quando usar o ticket.",
           2: "Criar o ticket.",
           3: "A primeira pesagem e o rascunho.",
           4: "Descarregar e a segunda pesagem.",
           5: "Impureza em porcentagem ou em quilos.",
           6: "Vários veículos ao mesmo tempo.",
           7: "Ticket com valores.",
           8: "Valorizar o ticket.",
           9: "Imprimir o comprovante.",
           10: "Quando o ticket sai da lista de pendentes.",
           11: "Pesagem avulsa com cobrança.",
           12: "Sem internet.",
           13: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "Ticket",
           2: "Ticket",
           3: "Pesagem",
           4: "Pesagem",
           5: "Pesagem",
           6: "Abas",
           7: "Valores",
           8: "Valorizar",
           9: "Comprovante",
           10: "Valorizar",
           11: "Avulsa",
           12: "Offline",
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
