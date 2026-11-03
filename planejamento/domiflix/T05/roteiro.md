# Roteiro T5 · Ordens de Serviço, Agenda, Equipes e Mapa ao Vivo

> **Atualização Dominex 1.38.19 (aula já entregue na 1.38.6).** Regravar **cap02, cap03, cap04, cap05 e cap06**. Passos novos: (cap02) etapa "Atendimento e orçamento" e a linha do serviço já nasce ao escolher o tipo; (cap03) sem etapa "Orçamento" nem botão "+", o orçamento fica abaixo na mesma etapa e o "Próximo" é um só; (cap04) só a tela, a etapa agora é "Escopo técnico" (fala igual); (cap05) "Equipe e agenda" e depois a etapa "Revisão" ("Confira antes de salvar") antes de "Criar OS"; (cap06) Recorrência em "Equipe e agenda". Kanban, Lista, Filtros, Configurações de OS, detalhe, Resetar OS e Agenda não mudam. Falas: `T05/narracao/emendas_1.38.19.txt`.


Roteiro pronto para gerar a voz e gravar (molde T3; sem etapa de aprovação, pedido do Kaik de 30/10 22:44). Coluna Fala = texto
da narração (voz Fernanda, ElevenLabs), na grafia da legenda; a grafia de pronúncia do TTS é aplicada em `narracao/tts_textos.py`.
Coluna Tela = o que o robô faz e onde a câmera foca, com os rótulos entre aspas como na tela (`T05/inventario.md`).
Todos os nomes, valores e datas são fictícios; as datas são relativas ao dia da gravação (terça, quarta, segunda).

- **Título final:** Ordens de Serviço, Agenda, Equipes e Mapa ao Vivo
- **Vinhetas (áreas):** ORDENS DE SERVIÇO · AGENDA · EQUIPES · MAPA AO VIVO · RESUMO (todos os capítulos, menos o 0, têm vinheta, como no T3)
- **Antes:** Tipos de Serviço, Tipos de Tarefa e Checklists (T4)
- **Próximo:** O técnico em campo (T7)
- **Duração estimada:** ~13 min de vídeo (1.902 palavras de fala, ~12,2 min de voz a 2,6 palavras/s, mais vinhetas e pausas do robô)
- **Estado inicial (fim do T4):** Glacial Cold Brasil com 16 clientes (os 12 da base têm coordenadas), 27 equipamentos, tipos de serviço MP, MC, INS, HIG, GAS e VT,
  tipos de tarefa (Reunião, Entrega de material, Compra de peças, Treinamento da equipe), checklists "Manutenção preventiva de split" (13 perguntas) e "Higienização de split";
  módulos RH e Contratos ligados; "Consumo de estoque na OS" e "Perguntar sobre receita ao finalizar OS" ligados (T1). Nenhuma OS, equipe, avaliação ou posição.
- **Entra por seed "de bastidor", antes do cap01:** 15 OS (`order_number` 1 a 15, datas relativas ao dia da gravação): 6 concluídas nos últimos 30 dias (180 a 650), 1 em andamento
  (Júlia Santos, Clínica Sorriso Leve), 1 a caminho (Bruno Alves, Hotel Mirante do Mar), 1 pausada (Paulo Souza, Restaurante Sabor da Serra), 2 agendadas (Condomínio Jardim Azul,
  Escritório Lemos & Prado), 2 pendentes na semana, 1 cancelada e 1 chamado do portal sem data (Mariana Lopes); os 7 `os_statuses` de fábrica; `os_config`; `nps_settings` e
  `nps_criteria` (Qualidade, Pontualidade, Profissionalismo); cerca de 10 `service_ratings` respondidas (notas 6 a 10, 2 comentários); `technician_locations` dos últimos 40 min
  (Bruno `en_route`, Júlia `check_in`, Lucas `check_out`), regravadas com `@now-Nm` logo antes do cap16.
- **Criado ao vivo:** OS #16 Manutenção Preventiva (Colégio Monte Verde, Hi-Wall 18.000 BTUs - Sala dos professores, Rafael Lima, próxima terça 09:00 a 11:00, R$ 180,00, pesquisa Sim),
  que **fica Pendente** (não é arrastada: o T7 a executa) e depois é reagendada para a quarta; série mensal de Higienização de Split (Academia Ponto Forte, Lucas Ferreira, 4 OS);
  tarefa "Reunião de alinhamento da equipe" (Reunião, próxima segunda 08:00, 60 min); **Equipe Alfa** (Bruno Alves e Lucas Ferreira, `#3B82F6`); OS de Carga de Gás (Pousada Sol Nascente,
  Cassete 36.000 BTUs - Recepção, Equipe Alfa, quarta 14:00); retoma a OS pausada; conclui uma OS pendente da semana e responde "Não" à receita.
- **Estado final:** `seeds-extra/t5/apos-cap17.json`; o T7 parte dele (OS #16 Pendente, com coordenadas do cliente para o mapa).
- Decisões padrão: etapa "Orçamento" mostrada (sem linha o valor da OS fica 0); sem criar status próprio (só nome, cor e ordem dos 7 existentes); "Faturar OS" só apontado;
  conflito de agenda só falado; "Avaliação no Google" só lida; "Link OS" só mostra "Copiado!"; "Preencher OS" só apontado (a navegação é do T7).
- Marcas na coluna Tela: `[BACKEND: ...]` (o que o backend falso ainda não tem), `[TESTAR ...]` (o robô testa antes de gravar), `[ILUSTRAÇÃO: ...]`.

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta Domiflix com o título "Ordens de Serviço, Agenda, Equipes e Mapa ao Vivo". | (sem fala) |
| Dashboard da Dominex, logado como Camila Duarte (Glacial Cold Brasil); a câmera desliza pelo menu lateral até o grupo Operacional. | Oi! Neste tutorial a gente vai abrir, distribuir, agendar e acompanhar as ordens de serviço da sua empresa, com a equipe, a agenda e o mapa funcionando juntos. |
| A câmera passa por "Agenda", "Ordens de Serviço" e "Mapa e Rastreamento" no menu. | É aqui que o trabalho do dia a dia acontece: você abre a ordem, escolhe quem vai, marca o horário e acompanha o técnico até o fim. Com o cadastro pronto, tudo fica bem mais rápido. |
| Cartão discreto: "Antes: Tipos de Serviço, Tipos de Tarefa e Checklists". | Se você ainda não viu o tutorial de Tipos de Serviço, Tipos de Tarefa e Checklists, dá uma olhada antes. [pause] Vamos começar pela tela de Ordens de Serviço. |

### cap01 · A tela de Ordens de Serviço (vinheta: ORDENS DE SERVIÇO)

| Tela | Fala |
| --- | --- |
| Clique em "Ordens de Serviço" no grupo Operacional; abre a tela com o título "Ordens de Serviço", o subtítulo "Gerencie suas ordens de serviço" e o menu lateral de abas: "Ordens de Serviço", "Chamados", "Relatório" e "NPS e Satisfação". | As ordens de serviço ficam no menu da esquerda, em Operacional, Ordens de Serviço. Do lado esquerdo da tela ficam as abas: Ordens de Serviço, Chamados, Relatório e NPS e Satisfação. |
| Zoom no filtro de período ("Todo o período") e nos quatro cartões "OS Abertas", "Concluídas", "Atrasadas" e "Próximos 7 dias". | No alto, os indicadores: OS Abertas, Concluídas, Atrasadas e Próximos sete dias. O período mostra todas as OS, e dá pra filtrar quando precisar. |
| Kanban com as colunas AGENDADA, PENDENTE, A CAMINHO, EM ANDAMENTO, CONCLUÍDA, PAUSADA e CANCELADA; a câmera percorre as colunas e para num cartão com o código, por exemplo "MP-2026-12". | A tela abre em Kanban, com uma coluna por status: Agendada, Pendente, A Caminho, Em Andamento, Concluída, Pausada e Cancelada. Cada cartão traz o código da OS: o prefixo do serviço, o ano e o número, como MP, dois mil e vinte e seis, doze. |
| Clique no botão de lista (ícone, ao lado do título "OS por Status"): a tabela aparece com as colunas "OS", "Criador", "Cliente", "Tipo", "Data", "Status" e "Ações"; volta ao Kanban. | Se você prefere uma lista, é só trocar aqui: a OS, o criador, o cliente, o tipo, a data, o status e as ações. Uma dica: a escolha fica guardada neste navegador. |

### cap02 · Abrindo uma nova OS (vinheta: ORDENS DE SERVIÇO)

| Tela | Fala |
| --- | --- |
| Clique em "Nova OS": abre a janela "Nova Ordem de Serviço", com as etapas numeradas e a etapa "Atendimento e orçamento" (1.38.19; eram "Cliente e Serviço", "Orçamento", "Equipamentos e Checklists" e "Agendamento e Detalhes"; agora "Atendimento e orçamento", "Escopo técnico", "Equipe e agenda" e "Revisão"). | Vamos abrir a primeira ordem de serviço. Clico em Nova OS. A janela tem quatro etapas, e a primeira é Atendimento e orçamento. |
| Clique em "Cliente avulso": aparece "O cliente será criado automaticamente com os dados abaixo."; volta para "Cliente cadastrado". | O cliente pode ser cadastrado ou avulso. No avulso, você digita os dados na hora, e ele já entra no cadastro de clientes. |
| Em "Cliente *" (placeholder "Selecione o cliente"), busca "Colégio" e escolhe "Colégio Monte Verde". | Aqui é o Colégio Monte Verde, que a gente cadastrou no tutorial de clientes. |
| Em "Tipos de Serviço" ("Selecione"), escolhe "Manutenção Preventiva" (o tipo principal primeiro): **a linha do orçamento já é criada** com "Qtd" 1 e o preço cadastrado ("O serviço entra abaixo com quantidade 1 e o preço cadastrado."), sem botão "+". | Em Tipos de Serviço, a Manutenção Preventiva. Dá pra escolher mais de um serviço na mesma ordem, e o primeiro vira o principal, que dá a cor e o prefixo do código. |
| Liga "Endereço de serviço (diferente do cliente)": aparecem "CEP", "Número", "Endereço", "Bairro" e "UF / Cidade" e o texto "O atendimento será feito neste endereço (filial, obra, evento). Quando vazio, usa o endereço do cliente."; desliga. | E se o atendimento for em outro lugar, como uma filial ou uma obra, é só ligar o Endereço de serviço, que vale só pra essa ordem. Aqui é no colégio mesmo, então eu desligo. |

### cap03 · Orçamento e rascunho (vinheta: ORDENS DE SERVIÇO)

| Tela | Fala |
| --- | --- |
| **Sem "Próximo"** (1.38.19): na mesma etapa "Atendimento e orçamento", desce até o bloco do orçamento (chave "Precificar com BDI" desligada, "Preço livre"; totais "Serviços e mão de obra", "Materiais" e "Total para faturamento"). | Aqui embaixo, no orçamento, ficam os valores da ordem: serviços, mão de obra e materiais. |
| A câmera para na linha "Manutenção Preventiva" já criada, com "Qtd" 1 e "Valor Unit." 180; **sem clicar em "+"** (não existe mais); o rodapé "Total para faturamento" mostra R$ 180,00. [BACKEND: RPC `sync_service_order_budget` atualiza `total_value`; sem linha o valor da OS fica 0] | A Manutenção Preventiva já entrou na linha, com a quantidade um e cento e oitenta reais, que é o Preço padrão que a gente cadastrou. E o Total para faturamento mostra cento e oitenta reais. |
| Fecha a janela; clique em "Nova OS": aparece "Rascunho encontrado" com "Começar do zero" e "Retomar rascunho"; clique em "Retomar rascunho": a janela reabre na etapa 1 ("Atendimento e orçamento") com cliente, serviço e valor de volta. [Interromper na etapa 2: o rascunho não guarda equipamentos, checklists nem responsáveis] | Se precisar sair no meio, o rascunho guarda o cliente, os serviços e os valores. Fecho a janela, abro a Nova OS de novo, e é só clicar em Retomar rascunho. |
| Clique em **"Próximo" uma vez** (1.38.19) até a etapa "Escopo técnico" (antes "Equipamentos e Checklists"). | Pronto, está tudo de volta. Vamos pra próxima etapa. |

### cap04 · Equipamentos e checklists (vinheta: ORDENS DE SERVIÇO)

| Tela | Fala |
| --- | --- |
| Etapa "Escopo técnico" (antes "Equipamentos e Checklists"): bloco "Equipamentos" com os aparelhos do colégio; marca "Hi-Wall 18.000 BTUs - Sala dos professores". | Agora o equipamento: marco o Hi-Wall dezoito mil BTUs da sala dos professores. Como a Manutenção Preventiva é vinculada a equipamento, a Dominex pede o aparelho. |
| Abre a setinha do equipamento: "Serviços neste equipamento" e "Checklists aplicados" com "Manutenção preventiva de split", "13 perguntas" e "Pré-visualizar checklist". [BACKEND: RPC `sync_service_order_scope_with_services`; sem ela a OS nasce sem equipamento nem checklist e o T7 abre vazio] | Abrindo o aparelho, aparecem os serviços que vão ser feitos nele e os checklists aplicados. Olha: o da manutenção preventiva já entrou sozinho, com as treze perguntas, porque a gente ligou ele a esse serviço no tutorial anterior. |
| Zoom em "Copiar para outros"; a câmera passa pelo bloco "Checklists avulsos" ("Checklists a nível de OS, sem equipamento vinculado."). | Dá pra pré-visualizar o checklist e copiar os serviços e checklists pra outros aparelhos da mesma ordem. Tem ainda os checklists avulsos, que valem pra ordem toda. |

### cap05 · Agendamento e detalhes (vinheta: ORDENS DE SERVIÇO)

| Tela | Fala |
| --- | --- |
| Clique em "Próximo": etapa "Equipe e agenda" (antes "Agendamento e Detalhes"; sem o quadro "Revisão do escopo da OS", que foi para a etapa final). | Agora a etapa Equipe e agenda, é aqui que a gente escolhe quem vai atender, o dia e o horário. |
| Abre "Responsáveis" e marca "Rafael Lima"; fecha o seletor. | Em Responsáveis, escolho quem vai: o Rafael Lima. Técnicos e equipes ficam no mesmo seletor, e as equipes a gente vê daqui a pouco. |
| Zoom em "Período do atendimento": "Data inicial" na próxima terça; no quadro "Jornadas por dia", "Quando começa" 09:00 e "Quando termina" 11:00. | No Período do atendimento, a data é na terça, e a jornada vai das nove às onze da manhã. Se o serviço dura mais de um dia, dá pra marcar o período inteiro, com o horário de cada dia. |
| Digita em "Descrição do Serviço": "Manutenção preventiva do Hi-Wall da sala dos professores". | Na descrição, vai o que precisa ser feito. |
| Zoom em "Gerar Pesquisa de Satisfação ao finalizar?" (Sim). | Em Gerar Pesquisa de Satisfação ao finalizar, deixo Sim: assim o cliente pode avaliar o atendimento depois que a ordem for concluída. |
| A câmera volta ao seletor "Responsáveis" (sem abrir aviso). | Uma dica: se o técnico já tiver outro atendimento naquele horário, o sistema avisa, e quem tem permissão pode autorizar com uma justificativa. |
| Clique em "Próximo": etapa "Revisão" com o resumo "Confira antes de salvar" (a câmera mostra serviços e checklists por aparelho). Clique em "Criar OS": toast "OS #16 criada" com "Agendada para ... às 09:00"; o cartão "MP-2026-16" aparece na coluna PENDENTE. [BACKEND: hook de `service_orders`: `status` `pendente`, `order_number` a partir de 16, `entry_type` `os`, `origin` `manual`] | Pra fechar, a etapa Revisão, o Confira antes de salvar, com o resumo da ordem. Conferido, Criar OS. Pronto: a OS número dezesseis foi criada, e aparece na coluna Pendente, já com a data marcada. |

### cap06 · Recorrência (vinheta: ORDENS DE SERVIÇO)

| Tela | Fala |
| --- | --- |
| Clique em "Nova OS": cliente "Academia Ponto Forte", tipo "Higienização de Split", responsável "Lucas Ferreira" (etapas aceleradas); na etapa "Equipe e agenda", liga o interruptor "Recorrência". | Agora uma ordem que se repete. Pra Academia Ponto Forte, a higienização dos splits todo mês, com o Lucas Ferreira. Preencho como antes e, em Equipe e agenda, ligo a Recorrência. |
| Em "Frequência" escolhe "Mensal", "A cada" 1; em "Até *" põe a data de daqui a três meses; aparece a prévia "Serão criadas N OS, de X até Y." | Em Frequência, escolho Mensal, a cada um mês, e em Até a data final. A prévia já diz quantas ordens vão ser criadas, antes de salvar. |
| Clique em "Criar OS Recorrentes"; toast "4 OS criadas com recorrência!"; as quatro aparecem no Kanban. [BACKEND: o hook grava `recurrence_group_id` e status `pendente` nas OS da série; `order_number` 17 a 20] | Criar OS Recorrentes. Pronto, a série inteira foi criada de uma vez. |
| Zoom nos cartões da série no Kanban (sem editar). | Se você mudar a data de uma ordem da série, o sistema pergunta se vale só pra ela ou também pras próximas; é só escolher o que faz sentido. |

### cap07 · Acompanhando no Kanban (vinheta: ORDENS DE SERVIÇO)

| Tela | Fala |
| --- | --- |
| Arrasta o cartão de uma OS pendente da semana de "PENDENTE" para "EM ANDAMENTO"; o cartão muda de coluna na hora. [TESTAR: `drag` HTML5 no Kanban; se falhar, trocar o status pelo seletor da linha na Lista. Não arrastar a OS #16] | Com as ordens criadas, acompanhar é no Kanban. Pra mudar o status, é só arrastar o cartão pra outra coluna. A mudança vale na hora. |
| Passa o mouse na coluna PENDENTE: zoom no "+" do cabeçalho (título "Criar OS em "Pendente""). | E o mais de cada coluna cria uma ordem já naquele status. |
| Clique no cartão da OS #16: abre o detalhe "OS #16" com a etiqueta de status; cartões "Cliente", "Equipamento" e "Check-in / Check-out"; no rodapé, ícones de ação, "Link OS" (clica e vira "Copiado!") e o botão "Preencher OS". [Não abrir o link copiado] | Clicando num cartão, abre o detalhe da ordem: o cliente, o equipamento, os registros de chegada e saída do técnico. Embaixo ficam as ações. O Link OS copia o link pro cliente acompanhar, e o Preencher OS abre a ordem como o técnico vê, que é o assunto do tutorial O técnico em campo. |
| Fecha o detalhe; abre a OS em andamento da Júlia Santos (Clínica Sorriso Leve); clique em "Resetar OS": janela "Resetar OS #N?" com "Manter o preenchimento" e "Apagar o preenchimento"; clique em "Cancelar". [BACKEND: RPC `reset_service_order`; sem ela o toast diz que resetou e nada muda] | Pra recomeçar uma ordem que já foi iniciada, tem o Resetar OS: ela volta pra Agendada, e você escolhe se mantém ou apaga o que foi preenchido. |

### cap08 · Status, filtros e busca (vinheta: ORDENS DE SERVIÇO)

| Tela | Fala |
| --- | --- |
| Clique em "Configurações": janela "Configurações de OS" com os sete status, cada um com cor e nome; menu da linha de "Pausada": "Editar"; mostra o campo de nome e a cor; clique em "Cancelar"; fecha a janela. [A cor é `<input type="color">` sem campo de texto; só mostrar, não alterar. Não usar "Novo status": o banco aceita só os 7 status de fábrica] | Agora, pra deixar o quadro do jeito da sua empresa: em Configurações você vê os status. Dá pra mudar o nome e a cor de cada um, e arrastar pra mudar a ordem das colunas. |
| Clique em "Filtros", dentro do campo de busca: grupo "Status" com uma caixa por status; marca "Em Andamento"; o quadro filtra; desmarca. | Em Filtros, você escolhe os status que quer ver. |
| Digita "Monte Verde" em "Buscar por OS, cliente, telefone, endereço ou serviço..."; aparece "Mostrando resultados de todas as OS (filtros pausados)"; limpa a busca. | E a busca procura por OS, cliente, telefone, endereço ou serviço. Quando você digita, ela olha todas as ordens, mesmo as fora do período ou do filtro. |

### cap09 · Concluir e faturar (vinheta: ORDENS DE SERVIÇO)

| Tela | Fala |
| --- | --- |
| Arrasta a OS que está em "EM ANDAMENTO" (a do cap07) para "CONCLUÍDA": abre "Receita da Ordem de Serviço" ("Houve alguma receita nesta Ordem de Serviço?"), com OS, Cliente e "Valor da OS"; clique em "Não". [BACKEND: o hook grava `completed_at` e cria a linha em `service_ratings` ao concluir] | Pra fechar o ciclo da ordem: ao concluir uma OS, arrastando pra coluna Concluída, a Dominex pergunta: houve alguma receita nesta ordem de serviço? É aquele Perguntar sobre receita ao finalizar OS, das Configurações. Se entrou dinheiro, você lança agora, e o valor já fica ligado à ordem. Aqui eu respondo Não. |
| Na Lista, menu "Ações" da linha da OS concluída: zoom em "Faturar OS" (sem clicar). | Dá pra faturar depois também, pelo Faturar OS. O lançamento da receita e a cobrança a gente vê nos tutoriais do Financeiro e de Cobranças. |

### cap10 · Chamados e relatório (vinheta: ORDENS DE SERVIÇO)

| Tela | Fala |
| --- | --- |
| Clique na aba "Chamados": busca "Buscar por chamado, cliente, equipamento ou contrato...", filtro "Chamados abertos" e a ação "Abrir chamado"; lista com o chamado de Mariana Lopes. [BACKEND: seed de 1 OS com `origin` `portal` e sem data] | Agora duas abas do lado esquerdo, Chamados e Relatório. Na aba Chamados chegam os pedidos que os clientes abrem pelos portais. Você filtra os abertos e abre o chamado pra dar andamento. |
| Volta à aba "Ordens de Serviço" em Kanban: zoom na coluna azul "Chamados do Portal". | No Kanban, eles ficam na coluna azul Chamados do Portal, até receberem uma data. Aí seguem como uma OS normal. |
| Clique na aba "Relatório": período "Este mês"; KPIs "Total de OS", "Taxa de conclusão", "Tempo médio" e "Faturamento"; gráficos; quadro "Saúde do agendamento" ("Concluídas no prazo", "Concluídas após a data", "Abertas em atraso"). [BACKEND: seed de OS do mês com `started_at`, `completed_at` e `total_value`] | Na aba Relatório você acompanha o mês: total de OS, taxa de conclusão, tempo médio e faturamento, com gráficos por status, por tipo de serviço e por dia da semana. E o quadro Saúde do agendamento mostra quantas ordens foram concluídas no prazo. |

### cap11 · Satisfação do cliente (vinheta: ORDENS DE SERVIÇO)

| Tela | Fala |
| --- | --- |
| Clique na aba "NPS e Satisfação": KPIs "NPS Score", "Média Geral", "Respostas" e "Taxa de Resposta"; zoom no gráfico "Distribuição NPS" (Promotores, Neutros, Detratores). [BACKEND: seed de `service_ratings` respondidas no mês] | Depois da visita, o cliente avalia o atendimento, e as respostas aparecem em NPS e Satisfação. No alto, o NPS Score, a média geral, as respostas e a taxa de resposta. A distribuição separa os clientes em promotores, neutros e detratores. |
| Zoom em "Ranking de Técnicos", "Detratores em Aberto" (selo "Atenção") e "Feed de Feedbacks". [BACKEND: RPCs `get_nps_technician_ranking`, `get_nps_open_detractors` e `get_nps_criteria_averages`] | Mais embaixo, o ranking de técnicos, os detratores em aberto, que pedem uma atenção, e o feed com os comentários dos clientes. |
| Clique em "Configurações": janela "Configurações de NPS" com "Pergunta da escala", "Critérios de avaliação" (Qualidade, Pontualidade, Profissionalismo) e a seção "Avaliação no Google" (só leitura); clique em "Cancelar". [Não usar "Gerar link de avaliação"] | Em Configurações você define a pergunta da escala e os critérios de estrela, como Qualidade, Pontualidade e Profissionalismo. E tem a Avaliação no Google, com o link da sua empresa, que a página pública da ordem usa pra convidar o cliente. |

### cap12 · As visões da Agenda (vinheta: AGENDA)

| Tela | Fala |
| --- | --- |
| Clique em "Agenda" no menu lateral (item de topo): título "Agenda", subtítulo "Visualize e gerencie os agendamentos de ordens de serviço"; abre em Mês, no Calendário, com os feriados pintados. [TESTAR: feriados do mês para Niterói/RJ; semear datas por dia da semana] | Agora a Agenda, no menu, logo abaixo do Dashboard. No computador ela abre no mês, com as ordens e as tarefas nos dias, e os feriados já marcados. |
| Alterna "Semana" e "Dia", volta a "Mês"; clique em "Hoje". | Em cima você troca entre Mês, Semana e Dia, e o Hoje volta pra data de hoje. |
| Alterna "Lista" e volta a "Calendário". | Também dá pra ver em Lista, que mostra o que está por vir e o que está atrasado. |
| Clique em "Filtros": "Técnico", "Cliente", "Status" e "Tipo" (Ordem de Serviço ou Tarefa); fecha; zoom na "Legenda". | Os filtros separam por técnico, cliente, status e tipo. E a legenda mostra a cor de cada tipo de serviço. |

### cap13 · Criar e reagendar (vinheta: AGENDA)

| Tela | Fala |
| --- | --- |
| Clique em "Nova Tarefa/OS": janela "O que deseja criar?" com "Ordem de Serviço" ("Atendimento técnico com cliente e equipamento") e "Tarefa" ("Atividade interna, reunião ou compromisso"); clique em "Tarefa". | Pra criar direto da agenda, é o botão Nova Tarefa ou OS. Ele pergunta o que você quer criar: uma ordem de serviço ou uma tarefa. Também dá pra dar dois cliques num dia. |
| Janela "Nova Tarefa": "Título da Tarefa *" "Reunião de alinhamento da equipe"; "Tipo de Tarefa" "Reunião"; "Responsáveis"; "Data" na próxima segunda; "Horário" 08:00; "Duração (min)" 60; clique em "Criar Tarefa". | Vou criar uma tarefa: Reunião de alinhamento da equipe. O tipo é Reunião, que a gente cadastrou, e eu escolho os responsáveis, a data, o horário e a duração. Criar Tarefa. Ela é um compromisso interno e aparece só na Agenda, enquanto a lista de Ordens de Serviço mostra apenas OS. |
| Na Semana ou no Mês, arrasta o cartão da OS #16 da terça para a quarta; toast "OS reagendada com sucesso!"; o cartão fica na quarta, às 09:00. [BACKEND: RPCs `schedule_book_service_order` e `schedule_book_service_order_plan`; sem elas o toast aparece e a OS não se move. TESTAR: `drag` HTML5 na Agenda; no Mês a hora se mantém] | Pra reagendar, é só arrastar a OS pro novo dia. A mudança vale na hora, então vale conferir o destino antes de soltar. Pronto: a OS número dezesseis agora é na quarta. |

### cap14 · Pausadas, busca e resumo (vinheta: AGENDA)

| Tela | Fala |
| --- | --- |
| Clique em "OS Pausadas" (com a contagem): lista com "Pausada há ..." e o botão "Retomar agora"; clique em "Retomar agora" na OS do Restaurante Sabor da Serra; toast "OS retomada". | Uma ordem pausada continua à vista até ser retomada. No botão OS Pausadas aparece a lista de todas, com o tempo que cada uma está parada. É só clicar em Retomar agora, e ela volta pra agenda. |
| Clique em "Pesquisar": janela "Buscar OS / Tarefa" ("Número da OS, cliente, descrição, técnico..."); digita "Monte Verde"; aparece a OS #16; fecha. | Pra achar uma ordem ou uma tarefa, é só pesquisar pelo número, pelo cliente, pela descrição ou pelo técnico. |
| Clique na OS #16 na agenda: abre o painel "Resumo da OS" com os responsáveis, a descrição e a "Linha do tempo"; zoom no menu "Ações" e no botão "Preencher OS" (sem clicar). | Clicando numa ordem, abre o resumo, com os responsáveis, a descrição e a linha do tempo. No menu Ações ficam editar, pausar, faturar e copiar o link de acompanhamento. E o botão Preencher OS leva pra tela do técnico, que a gente vê no próximo tutorial. |

### cap15 · Montando uma equipe (vinheta: EQUIPES)

| Tela | Fala |
| --- | --- |
| Menu Gestão, "Funcionários", aba "Equipes" (módulo RH): "Nenhuma equipe cadastrada" ("Cadastre sua primeira equipe para organizar os técnicos."). [Sem `?tab=`: clicar na aba "Equipes"] | Pra escalar um grupo de técnicos de uma vez, a gente cria uma equipe. Elas ficam em Gestão, Funcionários, na aba Equipes, que faz parte do módulo de RH. |
| Clique em "Nova Equipe": "Nome *" "Equipe Alfa"; "Descrição"; em "Visual da Equipe", cor azul `#3B82F6` e um ícone; em "Membros", marca "Bruno Alves" e "Lucas Ferreira"; clique em "Criar Equipe". [A cor é `<input type="color">` sem campo de texto: definir por `eval`. Não excluir equipe: usa o `confirm()` do navegador] | Clico em Nova Equipe e dou o nome: Equipe Alfa. Escolho uma cor e um ícone, marco os membros, o Bruno Alves e o Lucas Ferreira, e clico em Criar Equipe. |
| Nova OS: "Pousada Sol Nascente", "Carga de Gás", "Cassete 36.000 BTUs - Recepção" (etapas aceleradas); em "Responsáveis", seção "Equipes": marca "Equipe Alfa" e os dois membros ficam marcados; data na quarta, às 14:00; clique em "Criar OS". | Agora, numa nova ordem, a Carga de Gás da Pousada Sol Nascente, no Cassete trinta e seis mil BTUs da recepção. Em Responsáveis aparece a seção Equipes. Marco a Equipe Alfa, e os dois membros entram juntos. Na quarta, às duas da tarde. |
| Vai à Agenda e mostra a OS na quarta, às 14:00, com a equipe. | Na agenda, a ordem já aparece pra equipe toda. |

### cap16 · Onde está cada técnico (vinheta: MAPA AO VIVO)

| Tela | Fala |
| --- | --- |
| [ILUSTRAÇÃO: o celular do técnico envia a posição e ela aparece no Mapa ao Vivo; fundo branco, Montserrat, verde, objetos genéricos] | Falta saber onde cada técnico está. A posição vem do celular dele: o app envia durante o atendimento, e ela aparece aqui no mapa. É só pedir pro técnico liberar a localização no celular na primeira vez: é ela que coloca o ponto dele no mapa. |
| Menu Operacional, "Mapa e Rastreamento": título e subtítulo "Posição em tempo real e histórico de deslocamentos"; aba "Mapa ao Vivo" com os marcadores de Bruno, Júlia e Lucas, a legenda e o marcador "Base" da empresa. [BACKEND: regravar `technician_locations` com `@now-Nm` logo antes deste capítulo; clientes das OS com coordenadas; TESTAR: o mapa renderiza no Chromium headless, com tiles de Niterói em `/__tiles`, e a rota do OSRM] | No menu Operacional, Mapa e Rastreamento. Na aba Mapa ao Vivo, cada marcador é um técnico que enviou a posição nas últimas horas, e a cor mostra o que ele está fazendo: a caminho, executando a ordem ou já de saída. |
| Clique no marcador do Bruno Alves: popup com "OS vinculada", "Última atualização" e "Chegada em ~N min"; aparece a linha até o destino do cliente. | Clicando no técnico, aparece a OS dele, a última atualização e quanto falta pra chegar. A linha liga ele ao endereço do cliente. |
| Clique em "Atualizar". | O Atualizar busca as posições mais recentes. |
| Clique na aba "Histórico": filtros "Técnico" (Júlia Santos) e "Data" (hoje); estatísticas "Check-ins", "Check-outs", "Distância" e "Tempo em campo". [BACKEND: eventos de `technician_locations` do dia] | Na aba Histórico você escolhe o técnico e o dia, e vê os deslocamentos, a distância e o tempo em campo. |

### cap17 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: Kanban com a OS #16, o formulário da Nova OS, a série recorrente e a aba NPS e Satisfação. | Pronto! Recapitulando: a gente abriu uma ordem de serviço com cliente, serviço, orçamento, equipamento e checklist, e criou uma série que se repete todo mês. Acompanhou tudo no Kanban, com status, filtros e busca, e viu a satisfação dos clientes. |
| Montagem rápida: a Agenda com a tarefa e a OS reagendada, a Equipe Alfa e o Mapa ao Vivo. | Depois montou a agenda, com tarefas e reagendamento, criou a Equipe Alfa pra escalar mais de um técnico de uma vez e acompanhou a operação no mapa. |
| Cartão "Próximo: O técnico em campo"; cartela final. | No próximo tutorial, a gente vê tudo isso pelos olhos do técnico, no celular: da chegada ao cliente até o relatório pronto. Até lá! |
