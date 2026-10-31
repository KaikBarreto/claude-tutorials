# Texto enviado ao ElevenLabs (eleven_v4, Fernanda) por capítulo do T10 "CRM: funil, leads e captação".
# Gerado do roteiro.md (coluna Fala): cada linha do texto é uma linha da tabela Tela × Fala.
# Trocas de pronúncia em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   BTUs -> "bê-tê-ús" | CRM -> "cê-érre-ême" | Lead -> "Lide" | PMOC -> "pê-móqui" | URL -> "u-érre-éle" | Webhook -> "Uébruque" | Webhooks -> "Uébruques" | webhook -> "uébruque" | R$ 18.600,00 -> "dezoito mil e seiscentos reais" | 60% -> "sessenta por cento" | CRM/Kanban -> "crm kanban" | Fechado (Ganho) -> "fechado ganho" | Fechado (Perdido) -> "fechado perdido"
CAPS = {
0: """Oi! Neste tutorial a gente vai montar o funil de vendas da empresa, acompanhar cada oportunidade até o fechamento e receber contatos de fora sem digitar nada.
Cliente que pede orçamento por mensagem, outro que liga, outro que vem por indicação: é fácil alguém ficar esquecido. No cê-érre-ême, cada oportunidade tem dono, valor e próximo passo.
O cê-érre-ême faz parte do módulo cê-érre-ême Kanban. Com ele contratado, o grupo cê-érre-ême e Projetos aparece aqui no menu.
Se você ainda não viu o tutorial Orçamentos, Precificação e Proposta, dá uma olhada antes. [pause] Vamos abrir o cê-érre-ême.""",
1: """Primeiro, o funil. No menu, cê-érre-ême e Projetos, e depois cê-érre-ême Kanban. A tela tem duas abas, Funil e Tarefas, e os indicadores aparecem no alto.
Como a empresa ainda não tem funil, aparece o cartão Configure seu funil. Funil é o caminho que toda oportunidade percorre, da primeira conversa até o fechamento, e cada parada desse caminho é uma etapa.
Pra começar rápido, clico em Começar com estágios padrão. Pronto: nasceu o Funil de Vendas, com cinco colunas: Lide, Proposta, Negociação, Fechado Ganho e Fechado Perdido.
Em cima, o Total no funil conta as oportunidades, e o Valor Total soma quanto elas valem. O Fechado Ganho e o Lide mostram o valor dessas duas etapas.
Uma dica: o botão de mais, ao lado do nome do funil, serve pra criar outros funis. Dá pra ter um pra cada processo, como vendas e pós-venda.""",
2: """O padrão já ajuda, mas dá pra deixar o funil com a cara da sua empresa. Clico em Configurações do cê-érre-ême Kanban. A janela tem quatro seções: Funis, Checklists, Etiquetas e Uébruques. A gente fica em Funis, com o Funil de Vendas aberto e as cinco etapas.
Quero uma etapa para a visita técnica, que vem antes da proposta. Clico em Novo estágio, escrevo o nome, escolho uma cor e clico em Adicionar estágio.
Ela entrou no fim da lista. Pra mudar a ordem, é só arrastar a linha pela alça e soltar no lugar: coloco a Visita técnica logo depois do Lide.
Olha o que o Editar mostra: os interruptores Ganho e Perdido. É por eles que a Dominex sabe o que é venda ganha e o que é venda perdida. No Fechado Ganho, o Ganho já vem ligado, e é essa etapa que alimenta o indicador e a oferta de receita. Numa etapa nova, é só abrir o Editar e marcar Ganho ou Perdido.
Fechando a janela, o quadro já mostra as seis colunas na nova ordem. Dá pra reordenar também por aqui, arrastando o nome da coluna.""",
3: """Funil pronto, bora colocar a primeira oportunidade. Clico em Nova oportunidade.
No Título da Oportunidade, escrevo o negócio: instalação de seis splits no Colégio Monte Verde. No Cliente, escolho quem já está cadastrado. Se ainda não existir, o botão de mais cadastra na hora.
No Vendedor Responsável, escolho a Camila. Dá pra marcar mais de um vendedor, e o primeiro vira o Principal, que é quem entra nos filtros e nos relatórios.
A Origem diz de onde veio o cliente: este veio por Indicação. No Estágio, escolho Visita técnica, porque o primeiro passo é ir ver os aparelhos.
No Valor Estimado, dezoito mil e seiscentos reais. A Probabilidade é a chance de fechar: coloco sessenta por cento. Na Previsão Fechamento, a data em que eu espero fechar. E as Observações guardam qualquer detalhe.
Salvar, e o card já está no funil, na Visita técnica. Ele mostra o cliente, quem cuida, o valor, a barra de Probabilidade e a origem. Em cima, os indicadores já contam essa primeira oportunidade.""",
4: """Pra ver o funil andando, eu já deixei mais três oportunidades cadastradas do mesmo jeito: a do hotel, a do Marcos e a da Luana. Cada uma está numa etapa.
O Marcos aceitou conversar sobre o split de doze mil bê-tê-ús do quarto. Pra mudar a etapa, é só arrastar o card pra coluna seguinte. Os valores das colunas se atualizam na hora.
Já a Luana achou o valor alto e não vai seguir. Arrasto o card pra Fechado Perdido, e a Dominex pede o motivo da perda. Escolho Preço alto, escrevo um detalhe e clico em Confirmar Perda.
O motivo fica gravado nas observações da oportunidade, pra você consultar depois. E cada mudança de etapa também fica registrada no histórico.""",
5: """E quando o cliente fecha? Arrasto a instalação do colégio pra Fechado Ganho. A Dominex pergunta: Quer lançar a receita desta venda? Ela já traz o cliente e o Valor a lançar, dezoito mil e seiscentos reais, e dá pra corrigir se o cliente fechou por outro valor.
Com o Sim, lançar receita, abre a conta a receber já preenchida, e você confere antes de salvar. Eu clico em Agora não, porque o Financeiro é assunto de outro tutorial. A receita também pode ser lançada depois, direto pelo Financeiro.
Repara no indicador Fechado Ganho: ele soma o valor das vendas ganhas. Por isso vale deixar uma etapa marcada como Ganho: é ela que o funil usa pra somar o que você vendeu.""",
6: """Agora, o que fica guardado dentro de cada oportunidade. Abro a do pê-móqui anual do Hotel Mirante do Mar. Aqui estão a etapa em que ela está e quem cuida dela, a Tatiane.
Pra tirar uma oportunidade do funil, é a lixeira aqui no alto, e ela pede confirmação antes de apagar.
Daqui, dá pra criar uma ordem de serviço, no Criar OS, ou uma tarefa, no Criar Tarefa. Logo abaixo, o valor estimado, a probabilidade, a previsão de fechamento e a origem.
No Contato do Cliente, ficam o telefone e o e-mail, e o botão verde WhatsApp já abre a conversa.
Nas Observações, eu escrevo o que combinei: o hotel quer o contrato anual, com visita mensal. Não tem botão de salvar: aparece Salvando e depois Salvo.
Mais abaixo, ficam as Etiquetas e os Checklists da oportunidade, que você prepara nas Configurações do cê-érre-ême Kanban. Nos Comentários e atividades, a equipe deixa recados rápidos: escrevo e clico em Comentar.
Na aba Histórico, a Nova Interação guarda cada contato com o cliente. Escolho o tipo, Reunião, conto o que foi conversado e deixo a Próxima Ação: enviar a minuta do contrato, com a data. Clico em Registrar.
A próxima ação fica registrada com a data, e cada mudança de etapa também entra no histórico, com o De e o Para. Assim, qualquer pessoa da equipe sabe o que já foi combinado.""",
7: """Com o funil cheio, achar uma oportunidade tem que ser rápido. Na busca, escrevo Mirante. A Dominex procura no título, no cliente, no telefone e no documento, e esconde as etapas sem resultado.
Se quiser ver todas as colunas de novo, é o Mostrar todas. Apago a busca, e o funil volta inteiro.
No botão de filtro, ficam Origem, Vendedor, Valor Mínimo e Valor Máximo. Marco a Tatiane em Vendedor, e sobram só as oportunidades dela.
Na lista de vendedores, a opção Sem responsável mostra as oportunidades que ainda não têm dono. Uma dica: no catálogo de origens, use os mesmos nomes do filtro, como Indicação, Site e Google, que aí o filtro encontra tudo.""",
8: """E tem contato que chega sem ninguém digitar. Quando alguém pede orçamento pelo formulário do seu site, o contato pode cair direto no funil. Pra isso, abro as Configurações do cê-érre-ême Kanban, na seção Uébruques.
Uébruque é um endereço seguro que recebe oportunidades de outros sistemas, como o site ou uma campanha de anúncios.
O formulário de captação, que a gente viu no tutorial de Clientes, Fornecedores e Equipamentos, cadastra o cliente direto na lista. Pra entrar como oportunidade no funil, o caminho é o uébruque ou a Nova oportunidade.
Dou um nome: Site, Pedido de orçamento. Em Origem padrão, escolho Site. No Funil de destino, o Funil de Vendas, e na Etapa de destino, o Lide, que é onde cada contato novo vai entrar. Clico em Criar uébruque.
Ele aparece em Uébruques configurados, Ativo, com um endereço só dele. Clico no botão de copiar, e aparece u-érre-éle copiada. É esse endereço que você entrega pra quem cuida do site.
Mais embaixo, o Como usar o uébruque mostra o que o site precisa mandar: o nome e o telefone do contato e, se quiser, e-mail, título, observações e valor.
Quando o site manda um contato, ele cai aqui, na coluna Lide, com a origem Site e a etiqueta Sem responsável, porque ainda não tem dono.
Abro o card. O nome, o telefone e o e-mail de quem pediu vão para as Observações. Quem for cuidar do contato clica em Assumir oportunidade e vira o responsável. Pronto: ela sai da fila compartilhada e já tem dono.""",
9: """Venda fechada vira obra, e obra também se acompanha em Kanban. No grupo cê-érre-ême e Projetos, abro Projetos. Um projeto reúne as frentes de trabalho de uma obra, e cada frente é um quadro, igual ao do cê-érre-ême.
Clico em Novo projeto. Dou o nome, escolho o cliente e o responsável, o Status já vem como Em andamento, e marco o Início previsto e o Prazo final. Salvar, e o projeto ganha o código número um.
Abro o projeto. Na Visão geral, ficam o cliente, o responsável, o prazo e o Progresso da obra. Ainda não tem nenhuma frente, então vou criar a primeira.
Uma frente é uma parte da obra, como Infraestrutura, Elétrica ou Dutos. Escrevo o nome e salvo, e a frente já nasce com as etapas A fazer, Em execução, Concluído e Cancelado.
Cada trabalho da frente é um card. Clico em Novo card, escrevo Tubulação de cobre do Bloco B, escolho o Rafael como responsável e salvo.
Conforme o trabalho anda, é só arrastar o card: pra Em execução quando começa, e pra Concluído quando termina.
Na Visão geral, o Progresso da obra sobe sozinho, contando os cards que chegaram em Concluído. Cada frente aparece com a quantidade de cards, e um clique leva direto pro quadro dela. Quem cria e edita projetos é quem tem a permissão Gerenciar Configurações.""",
10: """Pronto! Recapitulando: você montou o funil de vendas, com as etapas padrão e uma etapa sua, a Visita técnica, e viu como marcar o que é Ganho e Perdido.
Cadastrou oportunidades, arrastou cada uma pelas etapas, registrou o motivo de uma perda e viu o que acontece quando o cliente fecha.
Guardou tudo do negócio dentro da oportunidade, com observações, comentários e o histórico de interações, e achou cada uma pela busca e pelos filtros.
Criou um uébruque pra receber contatos do site, e quem assume a oportunidade vira o responsável.
E acompanhou uma obra em Projetos, com frentes de trabalho em Kanban e o Progresso da obra.
O hotel está quase fechando o pê-móqui. No próximo tutorial, a gente monta esse contrato. Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "O funil começa aqui.",
           2: "Ajustando as etapas.",
           3: "A primeira oportunidade.",
           4: "Andando no funil.",
           5: "Quando o cliente fecha.",
           6: "Tudo do negócio num lugar.",
           7: "Achando rápido.",
           8: "Contatos que chegam sozinhos.",
           9: "Acompanhando a obra.",
           10: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "CRM",
           2: "CRM",
           3: "Oportunidades",
           4: "Oportunidades",
           5: "Oportunidades",
           6: "Oportunidades",
           7: "CRM",
           8: "Captação",
           9: "Projetos",
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
