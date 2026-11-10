# Texto enviado ao ElevenLabs (eleven_v4, Kaik Barreto) por capítulo do T8 "Ticket de Pesagem".
# Gerado do roteiro.md (coluna Fala): cada linha do texto é uma linha da tabela Tela × Fala.
# Trocas de pronúncia em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   A4 -> "á-quatro" | EcoTray -> "Ecotrêi"
CAPS = {
0: """Oi! Neste tutorial a gente resolve a situação clássica do pátio: o caminhão chegou, precisa pesar agora, mas o preço ainda não está fechado.
Na Recicla Vale Metais, a Cooperativa Recomeço mandou um caminhão de latinha, e o preço só vai ser combinado depois.
Com o Ticket de Pesagem, você registra o peso agora e resolve o valor depois.
Se você ainda não viu o tutorial Comprar e vender sucata, dá uma olhada antes. [pause] Vamos ver quando usar o ticket.""",
1: """O ticket fica no menu Materiais, em Ticket de Pesagem.
Com o preço fechado, você faz a compra direto, como no tutorial anterior. Com o preço em aberto, você pesa no ticket e transforma em compra ou venda depois.
Ticket salvo é peso registrado, e só. Nenhum quilo entra no estoque e nenhum centavo entra ou sai do caixa por causa dele. Isso só acontece quando o pedido que nasce dele é finalizado.
Os tickets ficam aqui. Em Aguardando valorização, o que ainda espera o preço. Em Valorizados, o que já virou pedido.
Na aba Pesagens avulsas fica outro caso: quem só quer saber o peso, como o caminhão de areia de um vizinho.
A pesagem avulsa é só um comprovante de peso. Ela não vira pedido, não mexe no estoque, e o comprovante sai marcado sem valor comercial.""",
2: """O caminhão da cooperativa chegou. Clico em Novo Ticket de Pesagem.
Em cima ficam três chaves: ticket padrão; compra, porque a gente vai comprar a latinha; e sem valores, porque o preço ainda não fechou.
Quando o preço já está combinado, dá pra fazer o ticket com valores, e ele já guarda o preço de cada material.
O fornecedor é a Cooperativa Recomeço.
No card Pesagem, o material: alumínio latinha.
E, aqui dentro, o motorista e a placa. O Edson Moura e o caminhão dele já estão cadastrados, então é só escolher na lista.
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
Se alguém fechar uma aba no x, o sistema pergunta antes de descartar o ticket.""",
7: """No fim do dia, o preço com a cooperativa fechou. É hora de valorizar: transformar o peso em pedido.
Em Ações, Valorizar. O sistema abre uma compra já preenchida: a cooperativa, a latinha, o peso e a impureza.
O preço vem da tabela: seis e vinte o quilo. Dá dezoito mil setecentos e catorze reais e oito centavos.
Se o preço combinado for outro, é só mudar o valor do quilo aqui, antes de finalizar. Num ticket de venda, abre uma venda do mesmo jeito.
Repara: até aqui, nada entrou no estoque e nada saiu do caixa. A compra está em rascunho, e o efeito só acontece quando ela for finalizada.""",
8: """O motorista leva o comprovante do ticket. Em Ações, Ver comprovante, e o formato: Térmico, o cupom, ou á-quatro, a folha.
Repara no papel: ticket de pesagem, não valorizado. É o comprovante do peso, ainda sem valor de compra.
Com o modo Completo, sai a conta inteira: o motorista, a placa, as duas pesagens, o bruto, a impureza e o líquido.
E se quiser que o cupom saia sozinho na impressora ao salvar cada ticket, ligue Imprimir comprovante do Ticket de Pesagem, em Configurações, Integrações.
Uma dica: se o ticket tiver pesagens do mesmo material mescladas numa linha, o comprovante mostra só a soma. Pra conferir cada pesagem no papel, use o Desmesclar pesagens antes de imprimir.""",
9: """E quando o ticket sai de Aguardando valorização? Mesmo com a compra em rascunho, ele continua aqui.
Valorizando de novo, o sistema retoma a mesma compra, sem duplicar.
Finalizo como no tutorial anterior: Pix, e confirmar pagamento. Agora sim, a latinha entrou no estoque e o pagamento saiu da conta.
E o sistema volta sozinho pro Ticket de Pesagem. O ticket passou pra Valorizados, com o número da compra.
Na lista, cada ticket mostra a situação. São três: Aguardando valorização, em amarelo; Valorizado, em verde; e Cancelado, em vermelho.
E o ticket do Jair continua no rascunho. Ele entra na lista quando for salvo.""",
10: """Pronto! Recapitulando: a gente criou o ticket da cooperativa com o fornecedor, o material, o motorista e a placa.
Fez a primeira pesagem na entrada, viu o rascunho salvo sozinho e fez a segunda na saída, com o bruto saindo sozinho.
Aplicou a impureza em porcentagem, atendeu um segundo caminhão em outra aba e salvou o ticket.
Valorizou o ticket, que virou uma compra já preenchida, imprimiu o comprovante e viu o ticket ir pra Valorizados quando a compra foi finalizada.
No próximo tutorial, a gente acha e corrige um pedido antigo. Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "Quando usar o ticket.",
           2: "Criar o ticket.",
           3: "A primeira pesagem e o rascunho.",
           4: "Descarregar e a segunda pesagem.",
           5: "Impureza em porcentagem ou em quilos.",
           6: "Vários veículos ao mesmo tempo.",
           7: "Valorizar o ticket.",
           8: "Imprimir o comprovante.",
           9: "Quando o ticket sai da lista de pendentes.",
           10: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "Ticket",
           2: "Ticket",
           3: "Pesagem",
           4: "Pesagem",
           5: "Pesagem",
           6: "Abas",
           7: "Valorizar",
           8: "Comprovante",
           9: "Valorizar",
           10: "Resumo"}

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
