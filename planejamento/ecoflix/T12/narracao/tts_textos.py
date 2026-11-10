# Texto enviado ao ElevenLabs (eleven_v4, voz Kaik Barreto) por capítulo do T12 "Coletas e Logística".
# Gerado da coluna Fala do roteiro.md: cada linha do texto é uma linha da tabela Tela × Fala.
# Trocas de pronúncia em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   Coletas & Logística -> "Coletas e Logística" | Caçamba 03/05/06 -> "Caçamba zero três/zero cinco/zero seis"
#   bag/bags -> "bégue"/"bégues" (nova) | PET -> "pét" (nova) | CNH -> "cê-ene-agá" (nova) | Ticket -> "Tíquete" (nova)
#   categoria C -> "categoria cê" (a letra da CNH)
#   As novas vão no ensaio de pronúncia antes da voz.
CAPS = {
0: """Oi! Neste tutorial o caminhão sai do pátio: a gente agenda a coleta, manda o motorista e fecha o serviço.
Na Recicla Vale Metais, buscar material vivia no caderno e na troca de mensagens. Aqui, cada coleta vira uma ordem, com o parceiro, o dia, o motorista e o caminhão.
Essa parte depende do plano contratado: ela vem no módulo de Coletas.
Se você ainda não viu o tutorial de clientes e fornecedores, dá uma olhada antes.
Tudo fica no menu Coletas e Logística, a começar pelas Ordens de Coleta. [pause] Antes de clicar em qualquer coisa, o que o módulo resolve.""",
1: """O módulo é pra quem vai buscar o material: quem tem caminhão, quem deixa caçamba no parceiro, quem combina de passar na empresa dele.
Cada coleta vira uma ordem, que passa por etapas: alguém pede, a gente agenda o dia e o período, escala o motorista e o caminhão, ele sai, e a coleta é concluída.
Uma coisa importante: a ordem de coleta organiza o serviço. Quem mexe no estoque e no caixa é a compra.
Quando o caminhão volta, você registra a compra do material como sempre, ou faz um Tíquete de Pesagem. Concluir a coleta fecha o serviço, e a compra entra por lá.""",
2: """Agora, o quadro. Cada coluna é uma etapa: Solicitada, Agendada, A caminho e Concluídas. E do lado ficam as canceladas.
A Solicitada recebe os pedidos que esperam aprovação, como os que chegam pelo portal. Daqui a pouco a gente vê um.
Cada cartão mostra o número da ordem, o parceiro, o período, o motorista e a placa. Hoje de manhã tem a troca de caçamba do Depósito Irmãos Siqueira.
E o Tiago já está a caminho de uma reforma, do Marcelo Tavares, que pediu coleta uma vez só e não tem cadastro.
Em cima ficam os filtros, o botão que troca o quadro por uma lista e o Nova ordem.
Uma dica: a ordem anda sempre pra frente, uma etapa de cada vez. Concluída ou cancelada, ela fica no quadro como registro. Se cancelou por engano, é só criar uma nova.""",
3: """A Auto Peças Vale Forte ligou: tem radiador e bateria pra buscar. Clico em Nova ordem. São três etapas: Parceiro, Coleta e Frota.
Quem já tem cadastro fica em Cadastrado. Pra quem pede coleta de vez em quando, como o Marcelo, tem o Sem cadastro, com nome, telefone e endereço.
O Tipo é Fornecedor, porque é de quem a gente compra. No Parceiro, busco a Auto Peças Vale Forte.
Repara: o endereço veio do cadastro dela. Se a coleta for em outro lugar, é só mudar aqui.
Avançar. Na etapa Coleta, o Material estimado: uns quatrocentos quilos de radiadores e baterias.
E nas Observações, o que ajuda o motorista a achar e a carregar: retirar pelo portão lateral.""",
4: """Agora, o dia e o período. Ainda na etapa Coleta, ficam a Data agendada e o Período.
A Auto Peças pediu pra quinta, doze de novembro.
O Período é a janela do dia: manhã, tarde ou dia todo. Assim o motorista sabe quando passar, e o parceiro, quando esperar.
Escolho manhã. E as janelas que aparecem aqui você define nas Configurações, no fim da aula.
Avanço pra última etapa.""",
5: """Falta quem vai buscar. Na etapa Frota ficam o Motorista e o Veículo, os mesmos da pesagem.
O Jair vai com o caminhão três quartos, que leva os quatrocentos quilos com folga.
Embaixo, a Revisão mostra tudo antes de criar: o parceiro, a cidade, o material, a data e o período.
Criar ordem. Pronto: a ordem nove já está agendada, com o Jair e o caminhão três quartos.
Motorista e veículo também podem ficar pra depois. Quem quiser exigir os dois antes de agendar tem a opção nas Configurações.""",
6: """O caminhão saiu. O Edson foi trocar a caçamba do Depósito Irmãos Siqueira, então eu clico em A caminho, e o cartão anda pra próxima coluna.
Pra fechar o serviço, o botão é o Preencher. Abre a tela da ordem, com tudo o que foi combinado.
No bloco Equipamentos, eu digo o que aconteceu com as caçambas. O Edson recolheu a Caçamba zero três, cheia de ferro.
E deixou a Caçamba zero cinco vazia no lugar. Nessa lista só aparecem as que estão na base.
Concluir coleta. Pronto: a ordem fechou, e a tela já mostra o relatório da coleta.
Uma dica: concluir a coleta fecha o serviço, e só. O ferro que chegou entra no estoque quando você registra a compra, na tela de compra ou num Tíquete de Pesagem.
De volta ao quadro, a ordem oito está em Concluídas. Clicando no cartão, abre a ficha dela.
Aqui ficam as caçambas que andaram nessa coleta.
E o Histórico guarda cada mudança de etapa, com a data e a hora. Assim dá pra saber o que aconteceu com cada coleta.""",
7: """E quando o próprio parceiro pede? Ele usa o portal, o link que a Recicla Vale mandou pra ele. Do outro lado, o pedido cai no quadro pra aprovação.
Pedir pelo portal depende também do Portal do Cliente no plano.
Este é o portal da Cooperativa Recomeço, do jeito que ela vê. Na aba Coletas, ela acompanha as coletas dela e pede uma nova.
A cooperativa tem oitocentos quilos de pét prensado pra sair. Ela preenche o material e a quantidade.
Escolhe o dia que prefere, sexta, e o período da tarde. O endereço já vem do cadastro.
Solicitar coleta. O pedido saiu, com o número dez.
Agora, do lado da Recicla Vale. O menu ganhou um pontinho vermelho de aviso. E na coluna Solicitada está o pedido da cooperativa, marcado como via portal.
Quem decide é a Recicla Vale. Dá pra aprovar ou recusar, e na recusa você escreve o motivo, que fica no histórico da ordem.
Aprovar. A data e a janela vêm do pedido, mas quem confirma é você.
Agendar. Pronto: a coleta da cooperativa está marcada pra sexta à tarde.""",
8: """Quem faz tudo isso é a frota. Em Frota ficam os veículos e os motoristas, os mesmos da pesagem de compra e venda.
No caminhão truck, a ficha mostra a tara e a capacidade.
A tara é o peso do caminhão vazio. Quando ele passa carregado na balança, o que passa da tara é o peso do material.
A Recicla Vale comprou um caminhão poliguindaste, o que leva e busca caçamba. Em Novo veículo, eu digito a placa e um apelido.
Os dados de transporte servem pros documentos de transporte. Aqui, São Paulo, veículo único e toco.
A tara dele é sete mil e cem quilos, e a capacidade, oito mil e quinhentos.
Cadastrar. Pronto, o poliguindaste já está na frota.
Agora o motorista dele. Na aba Motoristas, clico em Novo motorista.
O Rogério Batista foi contratado pro poliguindaste. Nome, CPF e telefone.
E a carteira de motorista, a cê-ene-agá: o número, a categoria cê, que é a de caminhão, e a validade.
Cadastrar. Agora ele já pode ser escalado nas ordens.""",
9: """E as caçambas. Elas ficam em Equipamentos, junto com bégues, caixas e paletes.
Primeiro vem o tipo. A caçamba é uma a uma: cada uma tem número e lugar próprios. O bégue é por quantidade: só interessa quantos tem em cada lugar.
Embaixo ficam as caçambas, uma por uma. Repara: a Caçamba zero cinco está no Depósito Irmãos Siqueira, onde o Edson deixou hoje.
Chegou uma caçamba nova. Em Nova unidade, eu dou a identificação, Caçamba zero seis, e o tipo. Cadastrar.
Ela ainda não tem lugar, porque o lugar vem das movimentações.
Clico em Movimentar. Ela veio de fora, de uma compra nova, então vai de Externo pra Minha base. Registrar. Pronto, a Caçamba zero seis está na base.
Uma dica: a caçamba só muda de lugar quando alguém registra. Na coleta, é o Entreguei e o Recolhi da ordem, que valem quando ela é concluída. Fora da coleta, é o Movimentar, aqui.
Em Onde tudo está agora fica o resumo: quanto está na base, quanto está em campo e com quantos parceiros.
E a aba Movimentações guarda cada ida e volta, com a data e quem registrou. As da troca de hoje mostram a ordem oito.""",
10: """No fim do mês, o relatório. Ele abre no mês atual, com o total de coletas, as concluídas, as canceladas e a taxa de conclusão.
Em outubro foram seis coletas: cinco concluídas e uma cancelada. E a taxa de conclusão deu cem por cento.
Uma dica: a coleta cancelada sai da conta. Das cinco que ficaram, as cinco foram concluídas.
Embaixo, as coletas por status, por motorista, por veículo e por parceiro. Dá pra ver quem rodou mais e onde a Recicla Vale mais busca.
Uma dica: cada coleta entra no mês em que foi concluída. A que ainda não foi conta pelo dia agendado, e a que não tem data, pelo dia em que foi pedida.""",
11: """Por último, as regras. Em Configurações, o primeiro bloco é o da operação.
O Prefixo da numeração vai na frente do número de cada ordem. Coloco COL e um traço, e as ordens passam a aparecer com ele.
Nas Janelas de coleta oferecidas, você escolhe os períodos que aparecem pra agendar. E aqui dá pra exigir motorista e veículo antes de agendar.
No bloco do portal, o Exigir aprovação faz o pedido do parceiro esperar na coluna Solicitada, como o da cooperativa. Desligado, ele já entra agendado.
A Antecedência mínima diz com quantas horas o parceiro precisa pedir: coloco vinte e quatro. E nos Dias aceitos, ele pede de segunda a sábado.
Uma dica: essas regras valem só pro que o parceiro pede pelo portal. Aqui dentro, a Recicla Vale agenda pra qualquer dia, até pra hoje.""",
12: """Pronto! Recapitulando: a gente conheceu o quadro e criou a coleta da Auto Peças Vale Forte, com data, período, motorista e caminhão.
Mandou o caminhão pro Depósito Irmãos Siqueira, registrou a troca de caçamba e concluiu a coleta, com o histórico de cada etapa.
Recebeu o pedido da cooperativa pelo portal e aprovou.
Cadastrou o poliguindaste, o motorista novo e a Caçamba zero seis, e viu onde cada caçamba está.
E conferiu o relatório do mês e ajustou as regras do portal.
No próximo tutorial, a gente transforma o que entrou no pátio em produto de maior valor. Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "O que o módulo de Coletas resolve.",
           2: "O quadro das ordens.",
           3: "Criar uma ordem.",
           4: "Data e janela.",
           5: "Motorista e veículo.",
           6: "Acompanhar até concluir.",
           7: "A coleta pedida pelo portal.",
           8: "Veículos e motoristas.",
           9: "As caçambas e onde estão.",
           10: "O relatório das coletas.",
           11: "As regras das coletas.",
           12: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "Coletas",
           2: "Ordens",
           3: "Ordens",
           4: "Agenda",
           5: "Agenda",
           6: "Acompanhamento",
           7: "Portal",
           8: "Frota",
           9: "Equipamentos",
           10: "Relatório",
           11: "Configurações",
           12: "Resumo"}

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
