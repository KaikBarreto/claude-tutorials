# Texto enviado ao ElevenLabs (eleven_v4, voz Kaik Barreto) por capítulo do T12 "Coletas e Logística", app 1.60.18.
# Gerado da coluna Fala do roteiro.md: cada linha do texto é uma linha da tabela Tela × Fala.
# Trocas de pronúncia em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   Coletas & Logística -> "Coletas e Logística" | Caçamba 02/03/05/06 -> "Caçamba zero dois/três/cinco/seis"
#   bag/bags -> "bégue"/"bégues" | PET -> "pét" | CNH -> "cê-ene-agá" | Ticket -> "Tíquete"
#   categoria C -> "categoria cê" (a letra da CNH) | GPS -> "gê-pê-ésse" | WhatsApp -> "uatsápe"
#   As novas (gê-pê-ésse, uatsápe) vão no ensaio de pronúncia antes da voz.
# Renumeração de 20/11 (1.60.18): capítulos novos 7 (editar, cancelar e excluir), 8 (relatório para o parceiro), 12 (movimentações e a
# ficha do parceiro), 13 (rastreamento) e 16 (checklist e assinaturas). Os antigos 7 a 12 viraram 9, 10, 11, 14, 15 e 17.
CAPS = {
0: """Oi! Neste tutorial o caminhão sai do pátio: a gente agenda a coleta, manda o motorista e fecha o serviço.
Na Recicla Vale Metais, buscar material vivia no caderno e na troca de mensagens. Aqui, cada coleta vira uma ordem, com o parceiro, o dia, o motorista e o caminhão.
Essa parte depende do plano contratado: ela vem no módulo de Coletas.
Se você ainda não viu o tutorial de clientes e fornecedores, dá uma olhada antes.
Tudo fica no menu Coletas e Logística, a começar pelas Ordens de Coleta. [pause] Antes de clicar em qualquer coisa, vamos ver o que o módulo resolve.""",
1: """O módulo é pra quem vai buscar o material: quem tem caminhão, quem deixa caçamba no parceiro, quem combina de passar na empresa dele.
Cada coleta vira uma ordem, que passa por etapas: alguém pede, a gente agenda o dia e o período, escala o motorista e o caminhão, ele sai, e a coleta é concluída.
Uma coisa importante: a ordem de coleta organiza o serviço. Quem mexe no estoque e no caixa é a compra.
Quando o caminhão volta, você registra a compra do material como sempre, ou faz um Tíquete de Pesagem. Concluir a coleta fecha o serviço, e a compra entra por lá.""",
2: """Agora, o quadro. Cada coluna é uma etapa: Solicitada, Agendada, A caminho e Concluídas. E do lado ficam as canceladas.
A Solicitada recebe os pedidos que esperam aprovação, como os que chegam pelo portal. Daqui a pouco a gente vê um.
Cada cartão mostra a data numa folhinha, o número da ordem, o parceiro, o período, o motorista e a placa. Hoje de manhã tem a troca de caçamba do Depósito Irmãos Siqueira, e o selo Hoje marca as coletas do dia.
E o Tiago já está a caminho de uma reforma, do Marcelo Tavares, que pediu coleta uma vez só e não tem cadastro.
Prefere uma tabela? Clico em Lista. As mesmas ordens, uma por linha, e clicando no título da coluna eu ordeno por data, por motorista ou por parceiro. O sistema lembra a visão que você escolheu.
Tem também o Calendário, que põe cada coleta no dia agendado. Dá pra ver o dia, a semana ou o mês, e o botão Hoje volta pra data de hoje. A ordem que ainda não tem dia fica numa faixa à parte, no alto.
Nos Filtros, eu escolho o período, o status e o parceiro. Repara no aviso: as solicitadas aparecem sempre, pra nenhum pedido ficar escondido. Depois, Limpar Filtros.
E o botão Nova ordem fica aqui em cima.
Uma dica: a ordem anda sempre pra frente, uma etapa de cada vez. Concluída ou cancelada, ela fica no quadro como registro. Se cancelou por engano, é só criar uma nova.""",
3: """A Auto Peças Vale Forte ligou: tem radiador e bateria pra buscar. Clico em Nova ordem. São três etapas: Parceiro, Coleta e Frota.
Quem já tem cadastro fica em Cadastrado. Pra quem pede coleta de vez em quando, como o Marcelo, tem o Sem cadastro. Aí basta o nome de quem pediu, o telefone e o endereço completo, que nesse caso é obrigatório, porque é o único jeito do motorista chegar.
O Tipo é Fornecedor, porque é de quem a gente compra. Se o material estiver com quem compra de você, o Tipo pode ser Cliente. No Parceiro, busco a Auto Peças Vale Forte.
Repara: o endereço veio do cadastro dela. Se a coleta for em outro lugar, é só mudar aqui.
Avançar. Na etapa Coleta, o Material estimado: uns quatrocentos quilos de radiadores e baterias.
E nas Observações, o que ajuda o motorista a achar e a carregar: retirar pelo portão lateral.""",
4: """Agora, o dia e o período. Ainda na etapa Coleta, ficam a Data agendada e o Período.
A Auto Peças pediu pra amanhã, quarta, onze de novembro.
O Período é a janela do dia: manhã, tarde ou dia todo. Assim o motorista sabe quando passar, e o parceiro, quando esperar. E se o dia ainda não está combinado, tem o Não definido: a ordem fica sem data.
Escolho manhã. E as janelas que aparecem aqui você define nas Configurações, no fim da aula.
Avanço pra última etapa.""",
5: """Falta quem vai buscar. Na etapa Frota ficam o Motorista e o Veículo, os mesmos da pesagem. Se faltar alguém no cadastro, o botão de mais ao lado cadastra na hora, sem sair da ordem.
O Jair vai com o caminhão três quartos, que leva os quatrocentos quilos com folga.
Embaixo, a Revisão mostra tudo antes de criar: o parceiro, a cidade, o material, a data e o período.
Criar ordem. Pronto: a ordem nove já está agendada, com o Jair e o caminhão três quartos.
Motorista e veículo também podem ficar pra depois. Quem quiser exigir os dois antes de agendar tem a opção nas Configurações.""",
6: """O caminhão saiu. O Edson foi trocar a caçamba do Depósito Irmãos Siqueira. Pra avisar o sistema, dá pra clicar em A caminho ou arrastar o cartão pra coluna do lado, como eu faço agora.
Pra fechar o serviço, o botão é o Preencher. Abre a tela da ordem, com tudo o que foi combinado. Se a ordem ainda estiver agendada, o motorista também começa por aqui, no Iniciar coleta, direto do celular.
No bloco Equipamentos, eu digo o que aconteceu com as caçambas. O Edson recolheu a Caçamba zero três, cheia de ferro.
E deixou a Caçamba zero cinco vazia no lugar. Nessa lista só aparecem as que estão na base.
O Depósito também pediu bégues. Como o bégue é por quantidade, eu só escolho o tipo e digo quantos ficaram: dez.
Concluir coleta. Pronto: a ordem fechou, e a tela já mostra o relatório da coleta.
Uma dica: concluir a coleta fecha o serviço, e só. O ferro que chegou entra no estoque quando você registra a compra, na tela de compra ou num Tíquete de Pesagem.
De volta ao quadro, a ordem oito está em Concluídas. Clicando no cartão, abre a ficha dela.
Aqui ficam os equipamentos que andaram nessa coleta: as caçambas e os bégues.
E o Histórico guarda cada mudança de etapa, com a data e a hora. Assim dá pra saber o que aconteceu com cada coleta.
E a coleta do Marcelo, que não tem cadastro? Na tela dela, o sistema avisa que sem fornecedor ligado não dá pra deixar nem recolher caçamba, porque ele precisa saber com quem ela ficou. Se o Marcelo virar parceiro fixo, o botão Cadastrar como fornecedor cria o cadastro e já liga nesta ordem.""",
7: """Nem toda coleta sai como combinado. No menu de três pontinhos de cada cartão ficam o Visualizar, o Editar e o Excluir.
Esqueci de avisar uma coisa ao motorista da Auto Peças. Em Editar, abre a mesma janela, numa página só, e acrescento nas observações: ligar antes de chegar. Aqui também dá pra trocar o motorista, o dia e o endereço. Salvar.
Se o parceiro desmarcar, o botão Cancelada pede confirmação antes. A ordem cancelada fica no quadro, como registro. Eu volto, porque a Auto Peças vai manter a coleta.
E o Excluir apaga de vez, mas só a ordem que não mexeu em nada. Esta já movimentou caçamba, então o sistema explica o motivo e não apaga.
Uma dica: criou por engano, sem ter mexido em nada, exclui. Combinou e não aconteceu, cancela. Assim o relatório mostra o que foi desmarcado.""",
8: """Toda coleta concluída vira um relatório. No cartão da ordem oito, o botão Relatório abre essa página, e em cima ficam três botões: Copiar link, Compartilhar no uatsápe e Imprimir.
Mais embaixo, o relatório mostra o que foi recolhido e o que foi entregue, e também o checklist, as fotos e as assinaturas, quando você usa. Quem abre o link não precisa de senha.
Na ficha da ordem, o mesmo link aparece em Relatório do Fornecedor, com o botão Abrir link do Fornecedor.
Uma dica: o link é público. Nas Configurações, o Mostrar valores no relatório que o cliente abre decide se os valores em reais aparecem nele.
E ele depende do Portal do Cliente no plano. Sem o portal, o sistema não mostra os botões: avisa que o cliente ainda não consegue abrir o link.""",
9: """E quando o próprio parceiro pede? Ele usa o portal, o link que a Recicla Vale mandou pra ele. Do outro lado, o pedido cai no quadro pra aprovação.
Pedir pelo portal depende também do Portal do Cliente no plano.
Este é o portal da Cooperativa Recomeço, do jeito que ela vê. Na aba Coletas, ela acompanha as coletas dela, abre o relatório das concluídas e pede uma nova.
A cooperativa tem oitocentos quilos de pét prensado pra sair. Ela preenche o material e a quantidade.
Escolhe o dia que prefere, sexta, e o período da tarde. O endereço já vem do cadastro.
Solicitar coleta. O pedido saiu, com o número dez.
Agora, do lado da Recicla Vale. O menu ganhou um pontinho vermelho de aviso. E na coluna Solicitada está o pedido da cooperativa, marcado como via portal.
Quem decide é a Recicla Vale. Dá pra aprovar ou recusar. Na recusa, abre uma janela pedindo o motivo, que fica no histórico da ordem, e o parceiro lê no portal dele.
Eu volto e aprovo. A data e a janela vêm do pedido, mas quem confirma é você.
Agendar. Pronto: a coleta da cooperativa está marcada pra sexta à tarde.""",
10: """Quem faz tudo isso é a frota. Em Frota ficam os veículos e os motoristas, os mesmos da pesagem de compra e venda. Na lista, dá pra buscar, filtrar por tipo de veículo e ordenar.
No caminhão truck, a ficha mostra a tara e a capacidade. E cada veículo e cada motorista tem Editar e Excluir no menu de três pontinhos.
A tara é o peso do caminhão vazio. Carregado, ele pesa mais na balança, e essa diferença é o peso do material.
A Recicla Vale comprou um caminhão poliguindaste, o que leva e busca caçamba. Em Novo veículo, eu digito a placa e um apelido.
Os dados de transporte servem pros documentos de transporte. Aqui, São Paulo, veículo único e toco.
Uma dica: a tara e a capacidade vão sempre em quilos. Se eu digitar só sete, o sistema avisa que o valor parece estar em toneladas. A tara dele é sete mil e cem quilos, e a capacidade, oito mil e quinhentos.
Cadastrar. Pronto, o poliguindaste já está na frota. E a capacidade em metros cúbicos vai até novecentos e noventa e nove, que é o limite da nota de transporte.
Agora o motorista dele. Na aba Motoristas, clico em Novo motorista.
O Sérgio Paiva foi contratado pro poliguindaste. Nome, CPF e telefone.
E a carteira de motorista, a cê-ene-agá: o número, a categoria cê, que é a de caminhão, e a validade.
Cadastrar. Agora ele já pode ser escalado nas ordens.""",
11: """E as caçambas. Elas ficam em Equipamentos, junto com bégues, caixas e paletes.
Primeiro vem o tipo. A caçamba é uma a uma: cada uma tem número e lugar próprios. O bégue é por quantidade: só interessa quantos tem em cada lugar.
Pra criar um tipo, Novo tipo. O palete eu conto por quantidade, então deixo desligada a opção de identificação própria. Com ela ligada, cada unidade ganha número, como a caçamba.
Embaixo ficam as caçambas, uma por uma. Repara: a Caçamba zero cinco está no Depósito Irmãos Siqueira, onde o Edson deixou hoje.
Caçamba furada? Em Editar, mudo a condição pra Em manutenção. E a que não volta mais fica como Baixada.
Chegou uma caçamba nova. Em Nova unidade, eu dou a identificação, Caçamba zero seis, e o tipo. Cadastrar.
Ela ainda não tem lugar, porque o lugar vem das movimentações.
Clico em Movimentar. Ela veio de fora, de uma compra nova, então vai de Externo pra Minha base. Registrar. Pronto, a Caçamba zero seis está na base.
Uma dica: a caçamba só muda de lugar quando alguém registra. Na coleta, é o Entreguei e o Recolhi da ordem, que valem quando ela é concluída. Fora da coleta, é o Movimentar, aqui.
Em Onde tudo está agora fica o resumo: quanto está na base, quanto está em campo e com quantos parceiros.
Os bégues aparecem em Contados por quantidade. Em Ver saldo por fornecedor, eu vejo quantos estão com cada parceiro.
E a aba Movimentações guarda cada ida e volta, com a data e quem registrou. As da troca de hoje mostram a ordem oito.""",
12: """Fora de uma coleta, eu lanço direto. Na aba Movimentações, Nova movimentação: dez bégues da minha base pra Cooperativa Recomeço. Registrar.
Errou? O menu da linha tem Editar e Excluir. O Editar corrige quantidade, data, origem, destino ou observação. Pra mudar o tipo, anula e lança de novo.
A excluída não some: fica como anulada, com o motivo, e dá pra restaurar. Em Filtros, o Mostrar anuladas traz elas de volta pra lista. As que vieram de uma ordem, você corrige na própria ordem.
E na ficha do parceiro tem a aba Coletas: o que está com ele agora, as coletas dele e as movimentações. Dali mesmo dá pra agendar outra coleta ou movimentar equipamento.""",
13: """Com a coleta a caminho, o Rastreamento mostra no mapa onde está cada motorista. Na lista do lado, o Tiago aparece com o selo Ao vivo.
A posição vem do celular do motorista, enquanto ele está com a ordem aberta. O círculo em volta do ponto é o raio de incerteza do gê-pê-ésse: quanto maior, menos exata é a posição.
O selo muda pra Visto há pouco e depois pra Sem sinal recente, conforme o tempo sem notícia. E pra aparecer no mapa, o motorista precisa ter login no sistema.
Em Trajeto de uma coleta, dá pra rever o caminho de uma ordem. Eu escolho a ordem sete.
Na tela da ordem, o motorista sempre vê o aviso de que a localização está sendo registrada. Sem sinal de gê-pê-ésse, a coleta segue normal, só a posição não é gravada. O menu também tem Rotas, a roteirização, mas ela chega numa próxima atualização.""",
14: """No fim do mês, o relatório. Ele abre no mês atual, com o total de coletas, as concluídas, as canceladas e a taxa de conclusão.
Em outubro foram seis coletas: cinco concluídas e uma cancelada. E a taxa de conclusão deu cem por cento.
Uma dica: a coleta cancelada sai da conta. Das cinco que ficaram, as cinco foram concluídas.
Embaixo, as coletas por status, por motorista, por veículo e por parceiro. Dá pra ver quem rodou mais e onde a Recicla Vale mais busca.
Uma dica: cada coleta entra no mês em que foi concluída. A que ainda não foi conta pelo dia agendado, e a que não tem data, pelo dia em que foi pedida.""",
15: """Por último, as regras. Em Configurações, o primeiro bloco é o da operação.
O Prefixo da numeração vai na frente do número de cada ordem. Aqui eu coloco um prefixo de coleta, e as ordens passam a aparecer com ele na frente.
Nas Janelas de coleta oferecidas, você escolhe os períodos que aparecem pra agendar. O sistema não deixa desmarcar todas: sempre sobra uma. E aqui dá pra exigir motorista e veículo antes de agendar.
No bloco do portal, o Exigir aprovação faz o pedido do parceiro esperar na coluna Solicitada, como o da cooperativa. Desligado, ele já entra agendado.
O Avisar quando chegar solicitação manda uma notificação pra você a cada pedido novo do portal.
A Antecedência mínima diz com quantas horas o parceiro precisa pedir: coloco vinte e quatro. E nos Dias aceitos, ele pede de segunda a sábado, e sempre sobra pelo menos um dia.
Uma dica: essas regras valem só pro que o parceiro pede pelo portal. Se ele pedir fora da regra, o portal explica o motivo e pede outra data. Aqui dentro, a Recicla Vale agenda pra qualquer dia, até pra hoje.""",
16: """Quer que o motorista confira alguma coisa em toda coleta? É o checklist. Em Modelos de checklist, clico em Novo modelo e dou o nome: Coleta com caçamba. Criar modelo.
Em Gerenciar perguntas, Nova pergunta. A primeira é de sim ou não, e obrigatória: o local estava acessível pro veículo?
Também dá pra pedir foto, número, texto livre, uma escolha entre opções, ou conformidade: conforme, não conforme ou não se aplica. E a ordem das perguntas você arrasta.
Agora escolho esse modelo como o checklist padrão da empresa, que vale pra toda coleta nova, e passo a exigir a assinatura de quem recebeu o motorista no local. Também dá pra exigir a assinatura do motorista.
Na tela da ordem, o checklist e a assinatura já aparecem. Enquanto faltar alguma coisa obrigatória, o sistema mostra o que falta pra concluir.
O motorista responde pelo celular, o responsável assina na tela, e tudo isso sai no relatório da coleta.""",
17: """Pronto! Recapitulando: a gente conheceu o quadro e criou a coleta da Auto Peças Vale Forte, com data, período, motorista e caminhão.
Mandou o caminhão pro Depósito Irmãos Siqueira, registrou a troca de caçamba e de bégues e concluiu a coleta, com o histórico de cada etapa.
Aprendeu a editar, cancelar e excluir uma ordem, e a mandar o relatório da coleta pro parceiro.
Recebeu o pedido da cooperativa pelo portal e aprovou.
Cadastrou o poliguindaste, o motorista novo e a Caçamba zero seis, lançou movimentações e viu onde cada equipamento está, e onde o motorista está no mapa.
E conferiu o relatório do mês, ajustou as regras do portal e montou o checklist com assinatura.
No próximo tutorial, a gente transforma o que entrou no pátio em produto de maior valor. Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "O que o módulo de Coletas resolve.",
           2: "O quadro das ordens.",
           3: "Criar uma ordem.",
           4: "Data e janela.",
           5: "Motorista e veículo.",
           6: "Acompanhar até concluir.",
           7: "Editar, cancelar e excluir.",
           8: "O relatório para o parceiro.",
           9: "A coleta pedida pelo portal.",
           10: "Veículos e motoristas.",
           11: "As caçambas e onde estão.",
           12: "Movimentações e a ficha do parceiro.",
           13: "Onde está o caminhão.",
           14: "O relatório das coletas.",
           15: "As regras das coletas.",
           16: "Checklist e assinaturas.",
           17: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "Coletas",
           2: "Ordens",
           3: "Ordens",
           4: "Agenda",
           5: "Agenda",
           6: "Acompanhamento",
           7: "Ordens",
           8: "Acompanhamento",
           9: "Portal",
           10: "Frota",
           11: "Equipamentos",
           12: "Equipamentos",
           13: "Frota",
           14: "Relatório",
           15: "Configurações",
           16: "Configurações",
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
