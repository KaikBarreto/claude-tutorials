# Texto enviado ao ElevenLabs (eleven_v4, Fernanda) por capítulo do T5 "Ordens de Serviço, Agenda, Equipes e Mapa ao Vivo".
# Gerado do roteiro.md (coluna Fala): cada linha do texto é uma linha da tabela Tela × Fala.
# Trocas de pronúncia em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   BTUs -> "bê-tê-ús" | Hi-Wall -> "rai-uól" | MP -> "ême-pê" | NPS -> "ene-pê-ésse" | RH -> "érre-agá" | Score -> "escór"
CAPS = {
0: """Oi! Neste tutorial a gente vai abrir, distribuir, agendar e acompanhar as ordens de serviço da sua empresa, com a equipe, a agenda e o mapa funcionando juntos.
É aqui que o trabalho do dia a dia acontece: você abre a ordem, escolhe quem vai, marca o horário e acompanha o técnico até o fim. Com o cadastro pronto, tudo fica bem mais rápido.
Se você ainda não viu o tutorial de Tipos de Serviço, Tipos de Tarefa e Checklists, dá uma olhada antes. [pause] Vamos começar pela tela de Ordens de Serviço.""",
1: """As ordens de serviço ficam no menu da esquerda, em Operacional, Ordens de Serviço. Do lado esquerdo da tela ficam as abas: Ordens de Serviço, Chamados, Relatório e ene-pê-ésse e Satisfação.
No alto, os indicadores: OS Abertas, Concluídas, Atrasadas e Próximos sete dias. O período mostra todas as OS, e dá pra filtrar quando precisar.
A tela abre em Kanban, com uma coluna por status: Agendada, Pendente, A Caminho, Em Andamento, Concluída, Pausada e Cancelada. Cada cartão traz o código da OS: o prefixo do serviço, o ano e o número, como ême-pê, dois mil e vinte e seis, doze.
Se você prefere uma lista, é só trocar aqui: a OS, o criador, o cliente, o tipo, a data, o status e as ações. Uma dica: a escolha fica guardada neste navegador.""",
2: """Vamos abrir a primeira ordem de serviço. Clico em Nova OS. A janela tem quatro etapas, e a primeira é Cliente e Serviço.
O cliente pode ser cadastrado ou avulso. No avulso, você digita os dados na hora, e ele já entra no cadastro de clientes.
Aqui é o Colégio Monte Verde, que a gente cadastrou no tutorial de clientes.
Em Tipos de Serviço, a Manutenção Preventiva. Dá pra escolher mais de um serviço na mesma ordem, e o primeiro vira o principal, que dá a cor e o prefixo do código.
E se o atendimento for em outro lugar, como uma filial ou uma obra, é só ligar o Endereço de serviço, que vale só pra essa ordem. Aqui é no colégio mesmo, então eu desligo.""",
3: """Agora a etapa Orçamento, onde ficam os valores da ordem: serviços, mão de obra e materiais.
Escolho a Manutenção Preventiva, e a quantidade e o valor já vêm: um, e cento e oitenta reais, que é o Preço padrão que a gente cadastrou. Clico no mais, e o Total para faturamento mostra cento e oitenta reais.
Se precisar sair no meio, o rascunho guarda o cliente, os serviços e os valores. Fecho a janela, abro a Nova OS de novo, e é só clicar em Retomar rascunho.
Pronto, está tudo de volta. Vamos pra próxima etapa.""",
4: """Agora o equipamento: marco o rai-uól dezoito mil bê-tê-ús da sala dos professores. Como a Manutenção Preventiva é vinculada a equipamento, a Dominex pede o aparelho.
Abrindo o aparelho, aparecem os serviços que vão ser feitos nele e os checklists aplicados. Olha: o da manutenção preventiva já entrou sozinho, com as treze perguntas, porque a gente ligou ele a esse serviço no tutorial anterior.
Dá pra pré-visualizar o checklist e copiar os serviços e checklists pra outros aparelhos da mesma ordem. Tem ainda os checklists avulsos, que valem pra ordem toda.""",
5: """Última etapa: Agendamento e Detalhes. Primeiro, uma revisão do escopo, pra você conferir os serviços e os checklists de cada aparelho antes de salvar.
Em Responsáveis, escolho quem vai: o Rafael Lima. Técnicos e equipes ficam no mesmo seletor, e as equipes a gente vê daqui a pouco.
No Período do atendimento, a data é na terça, e a jornada vai das nove às onze da manhã. Se o serviço dura mais de um dia, dá pra marcar o período inteiro, com o horário de cada dia.
Na descrição, vai o que precisa ser feito.
Em Gerar Pesquisa de Satisfação ao finalizar, deixo Sim: assim o cliente pode avaliar o atendimento depois que a ordem for concluída.
Uma dica: se o técnico já tiver outro atendimento naquele horário, o sistema avisa, e quem tem permissão pode autorizar com uma justificativa.
Criar OS. Pronto: a OS número dezesseis foi criada, e aparece na coluna Pendente, já com a data marcada.""",
6: """Agora uma ordem que se repete. Pra Academia Ponto Forte, a higienização dos splits todo mês, com o Lucas Ferreira. Preencho como antes e, na última etapa, ligo a Recorrência.
Em Frequência, escolho Mensal, a cada um mês, e em Até a data final. A prévia já diz quantas ordens vão ser criadas, antes de salvar.
Criar OS Recorrentes. Pronto, a série inteira foi criada de uma vez.
Se você mudar a data de uma ordem da série, o sistema pergunta se vale só pra ela ou também pras próximas; é só escolher o que faz sentido.""",
7: """Com as ordens criadas, acompanhar é no Kanban. Pra mudar o status, é só arrastar o cartão pra outra coluna. A mudança vale na hora.
E o mais de cada coluna cria uma ordem já naquele status.
Clicando num cartão, abre o detalhe da ordem: o cliente, o equipamento, os registros de chegada e saída do técnico. Embaixo ficam as ações. O Link OS copia o link pro cliente acompanhar, e o Preencher OS abre a ordem como o técnico vê, que é o assunto do tutorial O técnico em campo.
Pra recomeçar uma ordem que já foi iniciada, tem o Resetar OS: ela volta pra Agendada, e você escolhe se mantém ou apaga o que foi preenchido.""",
8: """Agora, pra deixar o quadro do jeito da sua empresa: em Configurações você vê os status. Dá pra mudar o nome e a cor de cada um, e arrastar pra mudar a ordem das colunas.
Em Filtros, você escolhe os status que quer ver.
E a busca procura por OS, cliente, telefone, endereço ou serviço. Quando você digita, ela olha todas as ordens, mesmo as fora do período ou do filtro.""",
9: """Pra fechar o ciclo da ordem: ao concluir uma OS, arrastando pra coluna Concluída, a Dominex pergunta: houve alguma receita nesta ordem de serviço? É aquele Perguntar sobre receita ao finalizar OS, das Configurações. Se entrou dinheiro, você lança agora, e o valor já fica ligado à ordem. Aqui eu respondo Não.
Dá pra faturar depois também, pelo Faturar OS. O lançamento da receita e a cobrança a gente vê nos tutoriais do Financeiro e de Cobranças.""",
10: """Agora duas abas do lado esquerdo, Chamados e Relatório. Na aba Chamados chegam os pedidos que os clientes abrem pelos portais. Você filtra os abertos e abre o chamado pra dar andamento.
No Kanban, eles ficam na coluna azul Chamados do Portal, até receberem uma data. Aí seguem como uma OS normal.
Na aba Relatório você acompanha o mês: total de OS, taxa de conclusão, tempo médio e faturamento, com gráficos por status, por tipo de serviço e por dia da semana. E o quadro Saúde do agendamento mostra quantas ordens foram concluídas no prazo.""",
11: """Depois da visita, o cliente avalia o atendimento, e as respostas aparecem em ene-pê-ésse e Satisfação. No alto, o ene-pê-ésse escór, a média geral, as respostas e a taxa de resposta. A distribuição separa os clientes em promotores, neutros e detratores.
Mais embaixo, o ranking de técnicos, os detratores em aberto, que pedem uma atenção, e o feed com os comentários dos clientes.
Em Configurações você define a pergunta da escala e os critérios de estrela, como Qualidade, Pontualidade e Profissionalismo. E tem a Avaliação no Google, com o link da sua empresa, que a página pública da ordem usa pra convidar o cliente.""",
12: """Agora a Agenda, no menu, logo abaixo do Dashboard. No computador ela abre no mês, com as ordens e as tarefas nos dias, e os feriados já marcados.
Em cima você troca entre Mês, Semana e Dia, e o Hoje volta pra data de hoje.
Também dá pra ver em Lista, que mostra o que está por vir e o que está atrasado.
Os filtros separam por técnico, cliente, status e tipo. E a legenda mostra a cor de cada tipo de serviço.""",
13: """Pra criar direto da agenda, é o botão Nova Tarefa ou OS. Ele pergunta o que você quer criar: uma ordem de serviço ou uma tarefa. Também dá pra dar dois cliques num dia.
Vou criar uma tarefa: Reunião de alinhamento da equipe. O tipo é Reunião, que a gente cadastrou, e eu escolho os responsáveis, a data, o horário e a duração. Criar Tarefa. Ela é um compromisso interno e aparece só na Agenda, enquanto a lista de Ordens de Serviço mostra apenas OS.
Pra reagendar, é só arrastar a OS pro novo dia. A mudança vale na hora, então vale conferir o destino antes de soltar. Pronto: a OS número dezesseis agora é na quarta.""",
14: """Uma ordem pausada continua à vista até ser retomada. No botão OS Pausadas aparece a lista de todas, com o tempo que cada uma está parada. É só clicar em Retomar agora, e ela volta pra agenda.
Pra achar uma ordem ou uma tarefa, é só pesquisar pelo número, pelo cliente, pela descrição ou pelo técnico.
Clicando numa ordem, abre o resumo, com os responsáveis, a descrição e a linha do tempo. No menu Ações ficam editar, pausar, faturar e copiar o link de acompanhamento. E o botão Preencher OS leva pra tela do técnico, que a gente vê no próximo tutorial.""",
15: """Pra escalar um grupo de técnicos de uma vez, a gente cria uma equipe. Elas ficam em Gestão, Funcionários, na aba Equipes, que faz parte do módulo de érre-agá.
Clico em Nova Equipe e dou o nome: Equipe Alfa. Escolho uma cor e um ícone, marco os membros, o Bruno Alves e o Lucas Ferreira, e clico em Criar Equipe.
Agora, numa nova ordem, a Carga de Gás da Pousada Sol Nascente, no Cassete trinta e seis mil bê-tê-ús da recepção. Em Responsáveis aparece a seção Equipes. Marco a Equipe Alfa, e os dois membros entram juntos. Na quarta, às duas da tarde.
Na agenda, a ordem já aparece pra equipe toda.""",
16: """Falta saber onde cada técnico está. A posição vem do celular dele: o app envia durante o atendimento, e ela aparece aqui no mapa. É só pedir pro técnico liberar a localização no celular na primeira vez: é ela que coloca o ponto dele no mapa.
No menu Operacional, Mapa e Rastreamento. Na aba Mapa ao Vivo, cada marcador é um técnico que enviou a posição nas últimas horas, e a cor mostra o que ele está fazendo: a caminho, executando a ordem ou já de saída.
Clicando no técnico, aparece a OS dele, a última atualização e quanto falta pra chegar. A linha liga ele ao endereço do cliente.
O Atualizar busca as posições mais recentes.
Na aba Histórico você escolhe o técnico e o dia, e vê os deslocamentos, a distância e o tempo em campo.""",
17: """Pronto! Recapitulando: a gente abriu uma ordem de serviço com cliente, serviço, orçamento, equipamento e checklist, e criou uma série que se repete todo mês. Acompanhou tudo no Kanban, com status, filtros e busca, e viu a satisfação dos clientes.
Depois montou a agenda, com tarefas e reagendamento, criou a Equipe Alfa pra escalar mais de um técnico de uma vez e acompanhou a operação no mapa.
No próximo tutorial, a gente vê tudo isso pelos olhos do técnico, no celular: da chegada ao cliente até o relatório pronto. Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "A tela de Ordens de Serviço.",
           2: "Abrindo uma nova OS.",
           3: "Orçamento e rascunho.",
           4: "Equipamentos e checklists.",
           5: "Agendamento e detalhes.",
           6: "Recorrência.",
           7: "Acompanhando no Kanban.",
           8: "Status, filtros e busca.",
           9: "Concluir e faturar.",
           10: "Chamados e relatório.",
           11: "Satisfação do cliente.",
           12: "As visões da Agenda.",
           13: "Criar e reagendar.",
           14: "Pausadas, busca e resumo.",
           15: "Montando uma equipe.",
           16: "Onde está cada técnico.",
           17: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "Ordens de serviço",
           2: "Ordens de serviço",
           3: "Ordens de serviço",
           4: "Ordens de serviço",
           5: "Ordens de serviço",
           6: "Ordens de serviço",
           7: "Ordens de serviço",
           8: "Ordens de serviço",
           9: "Ordens de serviço",
           10: "Ordens de serviço",
           11: "Ordens de serviço",
           12: "Agenda",
           13: "Agenda",
           14: "Agenda",
           15: "Equipes",
           16: "Mapa ao vivo",
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
