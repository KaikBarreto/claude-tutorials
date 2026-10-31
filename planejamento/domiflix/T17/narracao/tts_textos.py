# Texto enviado ao ElevenLabs (eleven_v4, Fernanda) por capítulo do T17 "Dashboard, relatórios e exportações".
# Gerado do roteiro.md (coluna Fala) pelo gerador do lote 5: cada linha do texto é uma linha da tabela Tela × Fala.
# Trocas de pronúncia em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   Contas a Pagar/Receber -> "Contas a Pagar e Receber" | Funcionários / RH -> "Funcionários e érre-agá" | check-out -> "tchécaut" | check-in -> "tchéquin" | PDF -> "pê-dê-éfe" | DRE -> "dê érri ê" | DFC -> "dê-éfe-cê" | CSV -> "cê-ésse-vê" | Excel -> "ékisel" | RH -> "érre-agá" | NPS -> "ene-pê-ésse" | Shift -> "chift"
CAPS = {
0: """Oi! Neste último tutorial da trilha, a gente vai ler o Dashboard, encontrar o relatório de cada área e levar os dados pra pê-dê-éfe, ékisel ou cê-ésse-vê.
O Dashboard é a primeira tela do dia. Ele junta o que aconteceu nas ordens de serviço, no caixa e na equipe, e cada número leva pra tela de onde veio.
Uma dica: com os atalhos ligados, o chift mais D volta pro Dashboard de qualquer tela.
Se você ainda não viu o tutorial Integração com WhatsApp, dá uma olhada antes. [pause] Vamos começar pelos números do topo.""",
1: """Lá em cima ficam três números. OS Abertas conta as ordens do período que estão em aberto, e embaixo, quantas estão pendentes.
A Taxa de Conclusão mostra quanto do trabalho do período já foi concluído.
E o Faturamento soma o que já entrou e foi pago no período. Quando aparece uma setinha, ela compara com o período anterior.
O que ainda vai entrar fica em Contas a Pagar e Receber.
E cada cartão leva pra tela de origem. Clico em OS Abertas e caio nas ordens de serviço.""",
2: """Logo abaixo, o dia em movimento. Em Equipe em Campo, o mapa mostra ao vivo quem está a caminho ou em atendimento. No fim da tarde a equipe já voltou, e o Abrir Mapa ao Vivo leva pro mapa completo.
Entra no mapa o técnico que abriu a ordem com a localização do celular liberada.
No Fluxo de Caixa ficam as entradas, as saídas e o saldo do período.
Ele e o faturamento contam o dinheiro que entrou de fora. Transferência entre as suas contas e pagamento da fatura do cartão ficam de fora, porque o dinheiro só trocou de bolso.
E a Evolução de OS mostra o total e as concluídas. No Diário, dá pra ver o ritmo de cada dia.""",
3: """Agora a coluna da direita. O OS por Status mostra quantas ordens estão em cada status, e a porcentagem de cada um.
Em OS por Tipo de Serviço, a rosca mostra que serviço a equipe mais fez no período.
E no Desempenho da Equipe estão os técnicos que mais concluíram, com a nota média das avaliações e o tempo médio de cada atendimento, do tchéquin ao tchécaut.""",
4: """E agora, o que precisa de você. O Requer Atenção junta as ordens com a data vencida que ainda estão abertas, da mais atrasada pra menos atrasada.
Ele e os chamados aparecem sempre, seja qual for o período, assim o que é antigo continua à vista.
Em Chamados abertos ficam os pedidos que os clientes abriram pelo portal.
Clicando, você vai direto pro chamado, na aba Chamados das ordens de serviço.""",
5: """Tudo isso obedece a um filtro só, aqui em cima, que começa em Este mês. Escolho Mês passado, e a tela inteira muda junto.
No Personalizado, você escolhe as datas de início e de fim. Eu volto pro Este mês.
Os blocos também levam pra origem. Clico em Concluída, e a lista de ordens de serviço já abre nesse status.
E o Faturamento leva pra Visão Geral do Financeiro, o painel do dinheiro da empresa.""",
6: """Pra ir além do resumo, cada área tem o seu relatório. O das ordens de serviço fica na aba Relatório, com o total, a taxa de conclusão, o tempo médio, o faturamento e a evolução no tempo.
Mais embaixo, os clientes que mais pedem, os técnicos que mais concluem e a saúde do agendamento, que mostra o que foi feito no prazo.
Do lado fica a aba ene-pê-ésse e Satisfação. O ene-pê-ésse nasce da avaliação que o cliente faz depois da visita, e aqui ficam a nota, a distribuição, o ranking dos técnicos e os comentários.""",
7: """E no Financeiro, os relatórios ficam no item Relatórios, em cinco abas: a visão geral, o dê érri ê, o dê-éfe-cê, o pacote pra contabilidade e a análise dos períodos.
A leitura de cada um está no tutorial Relatório Financeiro e dê érri ê.
No Estoque, a Posição de Estoque mostra o saldo numa data, os Inventários guardam as contagens, e o Relatório mostra as compras de material.""",
8: """E das pessoas, o ponto. Em Funcionários, Controle de Ponto, o Histórico tem as jornadas de cada um, e o cê-ésse-vê leva tudo pra uma planilha, com a entrada, a saída, as horas e o saldo de cada dia.
E o Relatório mostra o mês num calendário, com as horas e o saldo. O ponto faz parte do módulo Funcionários e érre-agá.""",
9: """E quando precisar levar os dados pra fora? Em Contas a Pagar e Receber, eu fico na aba A Receber e filtro só as pendentes.
O Exportar leva a lista pra ékisel, pê-dê-éfe ou cê-ésse-vê.
Uma dica: ajusta o período e os filtros antes, porque o arquivo sai exatamente com o que está na tela.
O mesmo Exportar aparece nas movimentações, no dê érri ê e no estoque.""",
10: """E pra levar tudo de uma vez, tem o Exportar meus dados, no fim da aba Empresa, nas Configurações. Ele gera uma planilha do ékisel com os dados da empresa, e serve de cópia de segurança.
Você escolhe os grupos. Aqui, os clientes, as ordens de serviço e o financeiro.
Uma dica: esse arquivo pode levar os dados da empresa inteira. Guarda num lugar seguro e libera essa opção só pra quem precisa.
No Exportar, ele junta cada parte e baixa a planilha, com uma aba pra cada assunto.""",
11: """Pronto! Recapitulando: no Dashboard, você viu o que cada número quer dizer, como o período comanda a tela e como cada cartão leva pra origem.
Depois encontrou o relatório de cada área: ordens de serviço, satisfação, financeiro, estoque e ponto.
E levou os dados pra fora, com o Exportar de cada lista e o Exportar meus dados.
Esse foi o último tutorial da trilha. Volte em qualquer um pelo capítulo que precisar. Até a próxima!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "Os números do topo.",
           2: "Equipe, caixa e evolução.",
           3: "Status, tipos e equipe.",
           4: "O que pede atenção.",
           5: "O período e a origem.",
           6: "Ordens de serviço e satisfação.",
           7: "Financeiro e estoque.",
           8: "Pessoas: o ponto.",
           9: "pê-dê-éfe, ékisel e cê-ésse-vê.",
           10: "Exportar meus dados.",
           11: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "Dashboard",
           2: "Dashboard",
           3: "Dashboard",
           4: "Dashboard",
           5: "Dashboard",
           6: "Relatórios",
           7: "Relatórios",
           8: "Relatórios",
           9: "Exportações",
           10: "Exportações",
           11: "Resumo"}

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
