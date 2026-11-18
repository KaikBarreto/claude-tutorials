# Cobertura 1.60.10 · T26 · CRM/Kanban

Auditoria só de leitura (18/11/2026). Código lido em `/dev/shm/ecoflix-src/src` (1.60.10); diferença contra o roteiro com
`git diff f37573ea0 5290be4cd`. Caminhos relativos a `src/`. Não existe varredura do robô para a T26
(`/home/claude/ecoflix/rec/varredura/` só vai até `t05`).

## 1. Mudou no app

**Nada mudou nas telas desta aula entre a 1.59.154 e a 1.60.10.** Conferido:

- `git diff --name-only f37573ea0 5290be4cd` não traz nenhum arquivo de `pages/Crm.tsx`, `components/crm/**`,
  `hooks/useTenantCrm.ts`, `hooks/useCrm*.ts`, `lib/crm*.ts`, `components/agenda/**`, `pages/Agenda.tsx` nem dos textos de
  `i18n/locales/pt-BR/agenda.json`. Os únicos "crm" do diff são do painel interno (`components/admin/crm/*`,
  `hooks/useAdminCrmLeads.tsx`), fora da aula.
- Nenhuma migration nova toca `crm_opportunities`, `crm_stages`, `crm_pipelines`, `crm_automation_rules`, `crm_labels` ou
  `crm_checklist_templates`: a regra do banco continua a da `20261106170000_crm_regras_automacoes.sql`.
- `config/routes.ts` e `App.tsx` mudaram, mas sem linha de CRM nem de Agenda (entraram permissões de banco, parceiros e
  materiais, e as restrições por usuário: assunto da T2).
- `config/version.ts`, de 1.59.155 a 1.60.10: nenhuma nota cita CRM, funil ou oportunidade.
- Componentes comuns: `ui/dialog.tsx` ganhou `hideCloseButton` (padrão desligado, o X das janelas continua) e
  `ui/responsive-dialog.tsx` ganhou o modo "inline" por contexto, que o CRM não usa. Sem efeito visual nas janelas da aula.

Consequência: os rótulos do `roteiro.md` e do `inventario.md` continuam exatos. O trabalho desta aula é todo de cobertura.

### 1.1 Roteiro × app que já divergiam na 1.59.154 (continuam valendo na 1.60.10)

| Cap. | O roteiro diz | O app faz | Onde |
| --- | --- | --- | --- |
| 08 | "Responsável" fica em "Sem responsável"; fala "O responsável fica em branco por enquanto." | Na criação o campo já abre com o usuário logado. A correção está em `propostas_fala.md` e ainda não foi aplicada. | `components/crm/opportunity/OpportunityFormDialog.tsx:124-125` |
| 12 | "Aplicar, e ficam dois cartões" | Os filtros valem na hora, a cada escolha; "Aplicar" só fecha a janela. A fala não está errada, mas o quadro muda antes do clique. | `pages/Crm.tsx:756` |
| 10 | Lista o que há em "Detalhes" sem o botão | Entre "Estágio"/"Responsável" e os cartões existe o botão **"Criar Tarefa"** (fora do inventário). | `components/crm/detail/OpportunityDetailsTab.tsx:281-283` |
| 08 | "Meio de transporte" com cinco opções | Existe uma sexta, a primeira da lista: **"— Não definido —"**. | `OpportunityFormDialog.tsx:332` |
| 11 | Selo "CRM" na Agenda | Certo no cartão do dia (categoria "CRM"), que ainda traz o link **"Abrir oportunidade →"**; no balão do calendário mensal o selo é **"Tarefa de CRM"**. | `components/agenda/TaskCard.tsx:108`, `:194`, `:205`, `i18n/locales/pt-BR/agenda.json:39-40` |

## 2. Falta cobrir

Só o que está no código. "Vale" = sim (trecho ou capítulo na seção 3), só citar (uma frase), ou não (com o motivo).

### Quadro e cartão (`pages/Crm.tsx`, `components/crm/OpportunityCard.tsx`)

| # | O que é | Quando o cliente usa | Vale |
| --- | --- | --- | --- |
| 1 | **"Probabilidade"** com barra, em todo cartão (nasce em 50%; verde a partir de 70, amarela de 40 a 69, vermelha abaixo) (`OpportunityCard.tsx:42-46`, `:146-157`). Aparece em todas as tomadas do quadro e a aula nunca explica. | Priorizar o que tem mais chance de fechar. | **sim** (P6) |
| 2 | Selo de **origem** no cartão (megafone) e progresso de checklist "feitos/total" (`:159-171`). | Saber de onde veio o contato; ver o andamento sem abrir a ficha. | **sim** (P5, P6) |
| 3 | **Ordem dentro da coluna**: o cartão fica onde foi solto e a ordem se mantém (`Crm.tsx:452-480`; nota 1.59.x "O cartão arrastado agora fica onde você soltou"). | Deixar em cima o que vai atacar primeiro. | **sim** (P8) |
| 4 | **Fechar o negócio**: arrastar para "Ganho" ou "Perdido" e ver "Ganhos" e "Em negociação" mudarem (`Crm.tsx:316-323`). A aula só mostra cartões que já estavam lá. | O caso de uso principal do funil. | **sim** (P8) |
| 5 | Trocar de funil na barra; cada funil tem seus cartões e seus totais (`Crm.tsx:614-625`). | Empresa com mais de um funil. | **sim** (P1) |
| 6 | Atalhos da barra: engrenagem **"Configurar estágios"** (abre as configurações com o funil já aberto) e **"+"** **"Criar funil"** (`Crm.tsx:626-631`); **"+"** do cabeçalho da coluna, "Adicionar em <etapa>" (`:149`). | Chegar mais rápido; criar o cartão já na etapa certa. | só citar (P1, P4) |
| 7 | **Excluir oportunidade** pelo cartão (lixeira no passar do mouse, confirmação do navegador `Excluir a oportunidade “<título>”?`, toast "Oportunidade excluída") (`Crm.tsx:493-501`). | Cartão criado por engano. | **sim**, pela ficha (P7) |
| 8 | Telefone e e-mail como selos no rodapé do cartão (`OpportunityCard.tsx:190-203`). | Ligar sem abrir a ficha. | só citar (P4) |
| 9 | Filtros "Valor mínimo", "Valor máximo", "Material", "Meio de transporte" e o status "Perdidos"/"Ganhos": a aula lista e só usa dois (`Crm.tsx:684-739`). | Rever o que perdeu; separar os negócios grandes. | **sim**, mais um exemplo (P8) |
| 10 | Tela de erro "Não foi possível carregar o CRM" · "Tentar novamente"; funil sem estágio "Este funil ainda não tem estágios" · "Criar primeiro estágio" (`Crm.tsx:523-531`, `:634-639`). | Queda de conexão; quem apagou todas as colunas. | não (erro de rede e caso raro; a dica de excluir estágio já cobre) |

### Configurações (`components/crm/settings/`)

| # | O que é | Quando o cliente usa | Vale |
| --- | --- | --- | --- |
| 11 | **Editar funil** (lápis, janela "Editar funil", toast "Funil atualizado") e **excluir funil**: "Excluir este funil?" · `O funil "<nome>" e todas as oportunidades dele serão removidos definitivamente.`; a lixeira fica apagada quando só existe um funil (`CrmPipelinesSection.tsx:307-327`, `:456-474`, `:543`). | Renomear; desistir de um funil. Excluir leva os cartões junto. | **sim** (P1) |
| 12 | Confirmação de excluir estágio: "Excluir este estágio?" · `O estágio "<nome>" será removido. Se houver oportunidades nele, mova-as para outro estágio antes.` (`:477-494`). | A dica do cap04 fala disso sem mostrar a janela. | só citar (mostrar a janela e "Cancelar" no cap04, sem fala nova) |
| 13 | Campos de **cada ação** da automação, hoje só lidos pelo nome: "Aplicar checklist" ("Modelo de checklist *", "Nome no cartão", chave **"Criar tarefa vinculada"** · "Concluir a tarefa marca o checklist e vice-versa."); "Definir prazo do cartão" ("Prazo em dias", "Contagem"; grava a **previsão de fechamento**); "Atribuir responsável" ("Responsável *"); "Adicionar etiqueta" ("Etiqueta *"); "Mover cartão" e "Copiar cartão" ("Funil de destino *", "Etapa de destino *", "Título da cópia"; o destino nunca é uma etapa de perdido; aviso "Mover encerra esta automação. Regras da etapa de destino continuam o fluxo.") (`CrmStageConfigurationDialog.tsx:121-159`). | Montar um fluxo de verdade, não só "criar tarefa". | **sim**, capítulo (P3) |
| 14 | **Várias ações** numa automação: "Adicionar ação" (até 20), setas "Mover ação para cima"/"Mover ação para baixo", "Remover ação" (`:116-118`, `:282`). | Encadear checklist, etiqueta e prazo. | **sim** (P3) |
| 15 | **Avisos ao salvar** a automação (o primeiro erro vira toast): "Dê um nome para a automação.", "Adicione ao menos uma ação.", "Ação N: escolha um modelo de checklist.", "Ação N: escolha um responsável.", "Ação N: escolha uma etiqueta.", "Ação N: escolha o funil e a etapa de destino.", "Ação N: mover o cartão precisa ser a última ação.", "Informe qual tarefa dispara a automação.", "Informe qual checklist dispara a automação." (`lib/crmAutomation.ts:47-80`). | Entender por que não salvou. | **sim**, um exemplo (P3) |
| 16 | **Gerenciar a lista** de automações: "Editar" ("Editar automação"), botão de pausar/ativar ("Pausar automação"/"Ativar automação") e lixeira "Excluir automação", que apaga **sem pedir confirmação** (toast "Automação excluída") (`CrmStageConfigurationDialog.tsx:289`). | Desligar um fluxo sem apagar; corrigir um título. | **sim** (P3) |
| 17 | Os outros três gatilhos, hoje só citados: "Ao concluir uma tarefa" pede "Nome exato da tarefa *"; "Ao concluir um checklist" pede "Nome exato do checklist *"; "Quando tudo estiver concluído" roda quando todas as tarefas do cartão estão encerradas e todos os itens de checklist marcados (migration `20261106170000`, `:523-556`, `:875-884`, `:929-938`). | "Quando terminar a papelada, anda sozinho." | **sim**, uma frase para cada (P3) |
| 18 | Cartão que volta e entra de novo na etapa **não duplica** a tarefa nem o checklist da automação (reaproveita os que a regra já criou) (migration, `:424-435`, `:605-611`). | Evita a dúvida "vai encher de tarefa repetida?". | só citar (P3) |
| 19 | Regras "por nome": aceita **uma por linha ou separadas por vírgula** (`lib/crmAutomation.ts:83-85`). | Quem cola uma lista. | só citar (P2) |
| 20 | "Salvar automação" grava na hora; cor, orientação e regras só gravam em **"Salvar etapa"**; "Fechar" descarta o que não foi salvo (`CrmStageConfigurationDialog.tsx:190-225`, `:235`). | Evita perder as chaves de regra ligadas e não salvas. | só citar (P2) |
| 21 | Modelos de checklist: lápis "Editar checklist <nome>" ("Checklist atualizada"), setas "Mover item para cima/baixo", "Remover item", e excluir: "Excluir este modelo de checklist?" · `O modelo "<nome>" será removido. Oportunidades que já aplicaram esta checklist não serão afetadas.` (`CrmChecklistsSection.tsx:83-117`, `:234-261`). | Ajustar a lista padrão. | **sim** (P4b) |
| 22 | Etiquetas: lápis "Editar etiqueta <nome>" ("Etiqueta atualizada") e excluir: "Excluir esta etiqueta?" · `A etiqueta "<nome>" será removida de todas as oportunidades que a usam.` (`CrmLabelsSection.tsx:80-113`). O contrário do modelo de checklist. | Trocar a cor; limpar etiqueta velha. | **sim** (P4b) |
| 23 | Setas de reordenar funis e estágios no celular (`CrmPipelinesSection.tsx:237-259`). | Só no celular. | não (a aula é no computador) |

### Nova oportunidade e ficha (`components/crm/opportunity/`, `components/crm/detail/`)

| # | O que é | Quando o cliente usa | Vale |
| --- | --- | --- | --- |
| 24 | "Empresa" com parceiro do cadastro: a lista mostra o selo Cliente ou Fornecedor e, ao escolher, **contato, telefone e e-mail se preenchem sozinhos**, sem passar por cima do que já foi digitado (`OpportunityFormDialog.tsx:241-249`; `CompanyPartnerField.tsx:90-110`). | Negócio com quem já é cadastrado (o mais comum). | só citar no cap08 (P4) |
| 25 | "Tipo de material": 'Usar "<texto>" como material avulso' e o botão "+" **"Novo material"** (só para quem pode cadastrar material); unidade ao lado da quantidade, que vem do material (`MaterialPickerField.tsx:191`, `:208`; `OpportunityFormDialog.tsx:302`, `:315-321`). | Material que ainda não está no cadastro. | só citar (P4); cadastro de material é da T3 |
| 26 | Campo "Data inicial" (vira "Data de início" na ficha) (`OpportunityFormDialog.tsx:349`). | Registrar quando a conversa começou. | só citar (P4) |
| 27 | **"Editar"** na ficha: abre "Editar oportunidade", o mesmo formulário com o bloco "Tarefas" no fim; toast "Oportunidade atualizada" (`OpportunityDetailModal.tsx:131-141`; `OpportunityFormDialog.tsx:377-382`; `Crm.tsx:401`). | Corrigir valor, contato, material. | **sim** (P7) |
| 28 | **Checklist na ficha de verdade**: "Aplicar modelo" lista os modelos com "<n> itens"; marcar item (salva na hora), barra e "feitos/total", lixeira "Remover checklist <nome>" (sem confirmação); vazio "Nenhum modelo cadastrado. Crie em Configurações do CRM/Kanban." (`OpportunityChecklistsSection.tsx`). A aula só passa o mouse. | Conferir a papelada do fornecedor antes de fechar. | **sim** (P5) |
| 29 | **"Probabilidade"** (0 a 100, grava ao sair do campo) e **"Origem"** (texto livre com as sugestões "WhatsApp", "Indicação", "Telefone", "Site"; exemplo "Ex.: WhatsApp") (`OpportunityDetailsTab.tsx:290-328`). | Ver item 1 e 2. | **sim** (P6) |
| 30 | **Comentários**: "Comentários e atividades", "Escreva um comentário…", "Comentar"; o comentário fica com o autor e o tempo, misturado com as mudanças do sistema (`OpportunityActivityFeed.tsx`). A aula só enquadra. | Registrar o que foi conversado, por quem. | **sim** (P6) |
| 31 | Trocar **"Estágio"** pela ficha (passa pela mesma trava) e **"Funil"** (só aparece com mais de um funil): "Trocar o funil move a oportunidade para a primeira etapa dele." · toast "Funil atualizado" (`OpportunityDetailsTab.tsx:162-187`, `:211-229`). | Mover sem arrastar; mandar o cartão para outro funil. | **sim** (P7) |
| 32 | Botão **"Criar Tarefa"** em Detalhes e o menu **"Mais ações da tarefa"** na aba Tarefas: "Editar", "Marcar em andamento", "Concluir"/"Reabrir", "Cancelar tarefa", "Excluir" (`OpportunityDetailsTab.tsx:281`; `tasks/OpportunityTasksSection.tsx:190-232`). Tarefa cancelada conta como encerrada para a trava. | Criar a tarefa sem sair da ficha; cancelar a que não faz mais sentido. | **sim** (P6) |
| 33 | **Excluir pela ficha**: "Excluir esta oportunidade?" · `A oportunidade "<título>" será excluída permanentemente, junto com as tarefas e o histórico vinculados a ela. Essa ação não pode ser desfeita.` (`OpportunityDetailModal.tsx:183-200`). | Ver item 7. | **sim** (P7) |
| 34 | Botão **"WhatsApp"** quando o cartão tem telefone (abre conversa fora do sistema) (`OpportunityDetailsTab.tsx:345-354`). | Chamar o contato direto da ficha. | só citar (P7); mostrar exige telefone fictício no cartão e um link para fora: **decisão** |
| 35 | Rodapé "Criado em: … · Atualizado: …" (`:401-404`). | Saber a idade do cartão. | não (informativo, lê-se sozinho) |

### Aba Tarefas e Agenda (`components/crm/CrmTasksTab.tsx`, `components/crm/tasks/`)

| # | O que é | Quando o cliente usa | Vale |
| --- | --- | --- | --- |
| 36 | **Arrastar a tarefa** entre as colunas troca a situação (`CrmTaskKanbanBoard.tsx:138-146`; toast "Tarefa atualizada"). | Marcar "em andamento" ou concluir sem abrir. | **sim** (P9) |
| 37 | Clicar na tarefa (nas três visões) abre **"Editar tarefa"**, com excluir: "Excluir tarefa?" · "Esta ação não pode ser desfeita. A tarefa será removida também da Agenda." (`CrmTasksTab.tsx:89-92`; `CrmTaskFormDialog.tsx:461-467`). O cap11 manda editar "na aba Tarefas" e não mostra. | Mudar a data ou o dono da tarefa. | **sim** (P9) |
| 38 | **"Filtrar"**: "Responsável", "Status", "Prioridade", "Oportunidade" (várias escolhas em cada), "Limpar filtros"; a bolinha laranja avisa que há filtro; busca "Buscar por título..." (`CrmTaskFilters.tsx`; `CrmTasksTab.tsx:122-159`). | "O que está comigo e ainda pendente?" | **sim** (P9) |
| 39 | Janela da tarefa: "Descrição", "Hora", **"Lembrar no dia"**, **"Notificação push"** e "Avisar quantos minutos antes" (`CrmTaskFormDialog.tsx:300-452`). | Ser avisado na hora da ligação. | só citar (P9); lembrete e push são da T25 (Agenda) |
| 40 | Lista: ordenar clicando no cabeçalho; Calendário: "Mês", "Semana", "Dia", setas "Período anterior"/"Próximo período", selo "Hoje" (`CrmTaskListView.tsx:118-123`; `CrmTaskCalendarView.tsx:183-212`). | Ver a semana de tarefas. | só citar (P9) |
| 41 | A visão escolhida (Kanban, Lista ou Calendário) fica guardada no navegador (`CrmTasksTab.tsx:35-44`). | Abre sempre do jeito preferido. | só citar (P9) |

## 3. Proposta

Tom do roteiro atual. Os trechos entram nos capítulos existentes; os capítulos novos recebem número próprio na
renumeração (aqui: `07b`, `10b`, `10c`). Nomes e valores do `plano.md` → "Mundo".

### P1 · cap03, depois de "Arrastando a linha…" (trecho · editar, excluir e trocar de funil)

| Tela | Fala |
| --- | --- |
| Clique no lápis "Editar funil Funil de vendas": janela "Editar funil" com "Nome *" e "Cor *"; clique em "Cancelar". | No lápis, dá pra trocar o nome e a cor de um funil. |
| Clique na lixeira "Excluir funil Funil de vendas": "Excluir este funil?" · `O funil "Funil de vendas" e todas as oportunidades dele serão removidos definitivamente.`; [ZOOM: a frase]; clique em "Cancelar". | E na lixeira, excluir. Uma dica: excluir o funil apaga todas as oportunidades dele, e não tem volta. Se ele for o único funil, a lixeira fica apagada. |
| (no fim do capítulo, depois da ilustração) "Fechar"; no quadro, clique em "Funil de vendas" na barra (quadro vazio) e de volta em "Sucata industrial"; o mouse passa pela engrenagem "Configurar estágios" e pelo "+" "Criar funil". | No quadro, eu troco de funil clicando no nome, aqui na barra. Cada funil tem os seus cartões e os seus totais. E a engrenagem e o mais são atalhos pras configurações. |

Mundo: nenhum dado novo (os dois funis já existem no cap03; nada é salvo).

### P2 · cap05 e cap06 (frases)

| Tela | Fala |
| --- | --- |
| cap05, no zoom de "Tarefas obrigatórias por nome": o texto de exemplo "Uma por linha". | (acrescentar à dica) Pra exigir mais de uma, é uma por linha. |
| cap06, depois de "Salvar automação, e ela aparece ativa na lista.": [ZOOM: o rodapé "Fechar" e "Salvar etapa"]. | A automação já ficou salva. Agora, o nome, a cor e as regras só valem depois de Salvar etapa. Saindo pelo Fechar, o que não foi salvo se perde. |

### P3 · capítulo novo `cap07b` · Automação com várias ações (vinheta: AUTOMAÇÕES), logo depois do cap07

Motivo de vir depois do cap07: usa o modelo de checklist e a etiqueta criados nele. Semente `apos-cap07`; termina em
`apos-cap07b`.

| Tela | Fala |
| --- | --- |
| "Configurações do CRM/Kanban" › "Funis" › "Sucata industrial"; lápis "Editar estágio Visita técnica"; aba "Automações"; clique em "Nova automação". | Com os modelos prontos, dá pra montar uma automação mais completa. Vou criar uma na Visita técnica. |
| "Nome *": "Preparar a proposta"; "Gatilho" fica em "Ao entrar nesta etapa". No seletor da ação 1 escolhe "Aplicar checklist": aparecem "Modelo de checklist *", "Nome no cartão" e "Criar tarefa vinculada". | O nome é Preparar a proposta, e o gatilho, Ao entrar nesta etapa. A primeira ação agora é Aplicar checklist. |
| Em "Modelo de checklist *" escolhe "Documentos do fornecedor"; em "Nome no cartão" troca "Checklist de {NOME}" por "Documentos da {CLIENTE}". | Eu escolho o modelo Documentos do fornecedor. E no nome que vai pro cartão, uso de novo o marcador CLIENTE. |
| Liga "Criar tarefa vinculada"; [ZOOM: a chave e a frase "Concluir a tarefa marca o checklist e vice-versa."] | Ligando Criar tarefa vinculada, o checklist ganha uma tarefa com o mesmo nome. Concluiu a tarefa, o checklist fica marcado. Marcou o checklist inteiro, a tarefa fica concluída. |
| Clique em "Adicionar ação"; na ação 2 escolhe "Definir prazo do cartão"; "Prazo em dias" "15"; "Contagem" "Dias corridos". | Adicionar ação. A segunda é Definir prazo do cartão: quinze dias corridos. Esse prazo é a previsão de fechamento, e ela é trocada quando a automação roda. |
| Clique em "Adicionar ação"; na ação 3 escolhe "Mover cartão": "Funil de destino *", "Etapa de destino *" e a frase "Mover encerra esta automação. Regras da etapa de destino continuam o fluxo."; [ZOOM: a frase] | As ações Mover cartão e Copiar cartão pedem o funil e a etapa de destino. Uma dica: Mover cartão tem que ser sempre a última ação, e o destino nunca é a coluna de perdido. |
| Na ação 3, clique em "Remover ação"; o mouse passa pelas setas "Mover ação para cima" e "Mover ação para baixo" da ação 2. | Aqui eu não vou mover nada, então removo essa ação. E com as setas, eu troco a ordem das ações. |
| Liga a chave ("Ativa"); apaga o "Nome *" e clica em "Salvar automação": toast "Dê um nome para a automação."; digita de novo "Preparar a proposta"; "Salvar automação": toast "Automação salva e ativa". [TESTAR: o toast de erro some antes do segundo clique] | Ligo pra Ativa. Se faltar alguma coisa, o sistema avisa o quê, como o nome aqui. Preenchido, Salvar automação. |
| Na lista: "Preparar a proposta", selo "Ativa", "Ao entrar nesta etapa · 2 ações"; o mouse passa por "Editar", pelo botão "Pausar automação" e pela lixeira "Excluir automação", sem clicar. | Na lista, cada automação tem o Editar, o botão de pausar, que desliga sem apagar, e a lixeira. Uma dica: a lixeira apaga na hora, sem perguntar. |
| Clique em "Nova automação"; abre "Gatilho" e escolhe "Ao concluir uma tarefa": aparece "Nome exato da tarefa *"; depois "Ao concluir um checklist": "Nome exato do checklist *"; depois "Quando tudo estiver concluído". Clique em "Voltar para lista". | E os outros gatilhos. Ao concluir uma tarefa e Ao concluir um checklist pedem o nome exato, letra por letra. E Quando tudo estiver concluído roda quando todas as tarefas do cartão estão encerradas e todos os itens de checklist, marcados. |
| A câmera fica na lista. | Uma dica: se o cartão voltar e entrar de novo na etapa, a automação não cria tudo em dobro. Ela aproveita a tarefa e o checklist que já tinha criado. |

Mundo/backend: insert em `crm_automation_rules` para a etapa "Visita técnica", `trigger_type` `stage_enter`, ações
`apply_checklist` (`templateId` do "Documentos do fornecedor", `name` "Documentos da {CLIENTE}", `createTask` true,
`reentry` "reuse") e `set_due` (`dueDays` 15, `dayMode` "calendar"), `enabled` true. O handler do backend falso precisa,
quando o cartão entrar em "Visita técnica" (fim do cap10): acrescentar em `crm_opportunities.checklists` o checklist
"Documentos da Metalúrgica Jequitibá" com os três itens do modelo e `linked_task_id`; criar em `schedule_tasks` a tarefa
"Documentos da Metalúrgica Jequitibá" (pendente, responsável Rafael, `crm_checklist_id`); trocar `expected_close_date`
de 30/11/2026 para **25/11/2026** (10/11 + 15 dias corridos). [TESTAR: a data da tarefa vinculada, que sai de
`crm_automation_due_date` sem `dueDays` na ação.]

### P4 · cap08 (frases) e P4b · cap07 (trecho)

| Tela | Fala |
| --- | --- |
| cap08, no campo "Empresa", antes de escolher a empresa avulsa: a lista aberta com os parceiros do cadastro e os selos "Cliente"/"Fornecedor". | (acrescentar) Escolhendo alguém do cadastro, o contato, o telefone e o e-mail já vêm preenchidos. |
| cap08, em "Tipo de material": o mouse passa pelo "+" "Novo material" e pela unidade "Kg". | Se o material ainda não existe, dá pra usar o nome avulso, ou cadastrar ali no mais. A unidade vem do material. |
| cap08, depois de salvar: [ZOOM: o "+" "Adicionar em Novo" no cabeçalho da coluna]. | E o mais de cada coluna cria a oportunidade direto naquela etapa. |
| **P4b** · cap07, depois de "Nova etiqueta… Salvar.": lápis "Editar etiqueta Indústria" (abre "Editar etiqueta", "Cancelar"); lixeira "Excluir etiqueta Indústria": "Excluir esta etiqueta?" · `A etiqueta "Indústria" será removida de todas as oportunidades que a usam.`; "Cancelar". | Pra mudar o nome ou a cor, é o lápis. Agora, cuidado com a lixeira: excluir uma etiqueta tira ela de todos os cartões. |
| "Checklists": lápis "Editar checklist Documentos do fornecedor": janela "Editar checklist" com as setas "Mover item para cima"/"Mover item para baixo" e "Remover item"; "Cancelar". | No checklist é diferente: editar ou excluir o modelo não mexe nos cartões que já receberam a lista. |

A frase da correção do cap08 ("O responsável já vem preenchido com quem está criando…") continua pendente em
`propostas_fala.md` e entra junto.

### P5 · capítulo novo `cap10b` · Checklist na oportunidade (vinheta: OPORTUNIDADES), depois do cap10

Semente `apos-cap10` (com os efeitos da automação "Preparar a proposta"); termina em `apos-cap10b`.

| Tela | Fala |
| --- | --- |
| O quadro: o cartão da Jequitibá em "Visita técnica" com "0/3", o selo de tarefas "1" e a data "25/11/2026". [ZOOM: "0/3" e a data] | Repara no cartão. Quando ele entrou na Visita técnica, a automação Preparar a proposta aplicou o checklist e mudou a previsão pra vinte e cinco de novembro. |
| Clique no título: ficha, aba "Detalhes"; a câmera desce até "Checklists": "Documentos da Metalúrgica Jequitibá", barra em "0/3". | Na ficha, o checklist veio com o nome da empresa: Documentos da Metalúrgica Jequitibá. |
| Marca "CNPJ conferido": o item fica riscado, "1/3". Marca "Local de retirada combinado" e "Frequência da coleta combinada": "3/3". | Na visita, o Rafael vai marcando. CNPJ conferido, local de retirada, frequência da coleta. Cada clique já salva. |
| Clique em "Tarefas (2)": "Documentos da Metalúrgica Jequitibá" com o selo "Concluída". [TESTAR: a aba recarrega a situação da tarefa vinculada sem remontar a ficha] | E a tarefa vinculada ficou concluída sozinha, porque o checklist foi todo marcado. |
| Volta para "Detalhes"; clique em "Aplicar modelo": a lista com "Documentos do fornecedor" · "3 itens"; clica: entra um segundo checklist, "0/3". | Sem automação, o caminho é o Aplicar modelo: escolhe o modelo, e a lista entra no cartão. |
| Clique na lixeira "Remover checklist Documentos do fornecedor": o segundo checklist sai. | Aplicou a mais? A lixeira remove o checklist do cartão. Ela remove na hora, sem perguntar. |
| Fecha a ficha: o cartão mostra "3/3". | E o cartão mostra quantos itens já foram feitos. |

Mundo/backend: update de `crm_opportunities.checklists` (itens `done`); a sincronização do banco conclui a tarefa
vinculada (`schedule_tasks.status` "concluida"); `apply`/`remove` são o mesmo update de `checklists`. Sem automação nos
gatilhos "checklist concluído" nesta etapa.

### P6 · capítulo novo `cap10c` · Probabilidade, origem, comentários e tarefas (vinheta: OPORTUNIDADES)

Semente `apos-cap10b`; termina em `apos-cap10c`.

| Tela | Fala |
| --- | --- |
| Ficha da Jequitibá, "Detalhes": os quatro cartões "Valor Estimado", "Probabilidade", "Previsão Fechamento" e "Origem". [ZOOM: "Probabilidade" com "50"] | Ainda na ficha, dois campos que valem ouro. A Probabilidade é a chance de fechar. Todo cartão nasce com cinquenta por cento. |
| Em "Probabilidade" digita "80" e aperta Enter. | A visita foi boa, então eu subo pra oitenta. |
| Em "Origem" clica, aparecem "WhatsApp", "Indicação", "Telefone" e "Site"; escolhe "Telefone". | E a Origem diz de onde veio o contato. Tem as sugestões, e dá pra escrever outra. Esse veio por telefone. |
| [ILUSTRAÇÃO: a barra de probabilidade: três cartões lado a lado; na palavra "verde", a barra do primeiro enche até 80 e fica verde; na palavra "amarela", a do segundo para em 50; na palavra "vermelha", a do terceiro fica em 20] | No cartão, a probabilidade vira uma barra: verde de setenta pra cima, amarela de quarenta a sessenta e nove, vermelha abaixo disso. Dá pra bater o olho e ver onde insistir. |
| À direita, "Comentários e atividades": em "Escreva um comentário…" digita "Paulo pediu a proposta até sexta."; clique em "Comentar": o comentário aparece com "Rafael Nogueira" e o tempo. | Do lado direito ficam os comentários. Eu anoto o que foi combinado: Paulo pediu a proposta até sexta. Comentar. Fica com o meu nome e a hora, junto com as mudanças do cartão. |
| Clique em "Criar Tarefa": janela "Nova tarefa" com a oportunidade já preenchida; "Título *" "Ligar pro Paulo"; "Data *" 13/11/2026; "Salvar": toast "Tarefa criada". | Pra não esquecer, Criar Tarefa, aqui mesmo. A oportunidade já vem ligada. Ligar pro Paulo, dia treze. Salvar. |
| Aba "Tarefas (3)": na linha "Ligar pro Paulo", clique em "Mais ações da tarefa": "Editar", "Marcar em andamento", "Concluir", "Cancelar tarefa", "Excluir". Fecha o menu sem escolher. | Na aba Tarefas, os três pontinhos trazem as ações: editar, marcar em andamento, concluir, cancelar ou excluir. Uma dica: pra regra da etapa, tarefa cancelada conta como encerrada. |
| Fecha a ficha: o cartão com "80%" em verde e o selo "Telefone". [ZOOM: a barra e o selo] | Fechando, o cartão já mostra os oitenta por cento e a origem. |

Mundo/backend: updates de `probability` (80) e `source` ("Telefone") em `crm_opportunities`; insert em
`crm_opportunity_activities` (`kind` "comment"); insert em `schedule_tasks` ("Ligar pro Paulo", 13/11/2026, Rafael,
categoria "crm"). O cap11 passa a mostrar essa tarefa e a vinculada: ver "Efeito nos capítulos seguintes".

### P7 · cap10c, continuação, ou fim do cap10 se o P6 não entrar (trecho · editar, mover pela ficha e excluir)

| Tela | Fala |
| --- | --- |
| Na ficha, [ZOOM: "Funil" e a frase "Trocar o funil move a oportunidade para a primeira etapa dele."], sem trocar; o mouse abre "Estágio" (as seis etapas com a bolinha de cor) e fecha. | Pela ficha também dá pra mudar o estágio, sem arrastar, e a regra da etapa vale do mesmo jeito. E trocar o funil manda a oportunidade pra primeira etapa do outro funil. |
| Clique em "Editar": a ficha fecha e abre "Editar oportunidade", o mesmo formulário; a câmera desce até o bloco "Tarefas"; clique em "Cancelar". | O Editar abre o cadastro completo, pra corrigir valor, contato ou material, com as tarefas no fim. Com telefone no cadastro, a ficha ganha um botão de WhatsApp. |
| Reabre a ficha; clique na lixeira "Excluir oportunidade": "Excluir esta oportunidade?" · `A oportunidade "Retalho de chapa da Metalúrgica Jequitibá" será excluída permanentemente, junto com as tarefas e o histórico vinculados a ela. Essa ação não pode ser desfeita.`; [ZOOM: a frase]; "Cancelar". | E a lixeira exclui a oportunidade. Uma dica: vão junto as tarefas e o histórico, e não tem volta. Negócio que não deu certo vai pro Perdido, não pra lixeira. |

Mundo: nada é salvo.

### P8 · cap12 (trechos · ordem na coluna, mais um filtro e fechar o negócio)

| Tela | Fala |
| --- | --- |
| Depois de "Pra ver tudo de novo, é Limpar filtros.": "Filtros" › "Status" "Perdidos": fica "Papelão do Mercado Bom Preço"; "Limpar filtros". | Outro uso: em Status, Perdidos, pra rever o que não fechou e por quê. O motivo está nas observações do cartão. |
| Pega "Cobre de manutenção da Elétrica Ponto Certo" pela alça, em "Novo", e solta em "Em contato" **acima** de "Perfis de alumínio da Esquadrias Horizonte". [BACKEND: a automação "Agendar a visita" cria a tarefa "Agendar visita na Elétrica Ponto Certo"] | O cartão fica onde eu soltar. Levo o da Elétrica Ponto Certo pra Em contato, em cima do outro, e a ordem se mantém. Assim, o mais urgente fica no topo. |
| Pega "Baterias da frota da Transportadora Caminho Firme", em "Proposta", e solta em "Ganho". [ZOOM: "Ganhos" "R$ 23.650,00" e "Em negociação" "R$ 37.000,00"] | E quando fecha? A Transportadora Caminho Firme aceitou a proposta. Arrasto pra Ganho, e os cartões de cima acompanham: vinte e três mil seiscentos e cinquenta reais ganhos, trinta e sete mil em negociação. |

Mundo/backend: `reorder_company_crm_opportunities` com a ordem nova de "Em contato"; `stage_id` da Caminho Firme para
"Ganho" ("Proposta" não tem regra). Contas: 19.000 + 4.650 = 23.650; 41.650 − 4.650 = 37.000; o total continua 62.300.
"Elétrica Ponto Certo" está sem responsável e sem tarefa: a trava do "Novo" não existe, então o arrasto passa.

### P9 · cap11 (trechos · arrastar, editar, filtrar)

| Tela | Fala |
| --- | --- |
| Depois de "Ela entra em Pendente.": arrasta "Enviar proposta" de "Pendente" para "Em andamento": toast "Tarefa atualizada". | No Kanban, eu mudo a situação arrastando. Comecei a proposta, levo pra Em andamento. |
| Clique na tarefa: janela "Editar tarefa"; a câmera passa por "Descrição", "Hora", "Lembrar no dia" e "Notificação push"; clique em "Cancelar". | Clicando na tarefa, abre a edição: dá pra pôr hora, descrição e lembrete. É aqui também que ela é excluída, e sai da Agenda junto. |
| Clique em "Filtrar": "Responsável", "Status", "Prioridade" e "Oportunidade"; em "Status" marca "Pendente": ficam as pendentes; "Limpar filtros". | Em Filtrar, dá pra separar por responsável, situação, prioridade e oportunidade. E a busca acha pelo título. |
| Na "Lista", clique no cabeçalho "Data"; no "Calendário", clique em "Semana" e na seta "Próximo período". | Na Lista, clicando no cabeçalho, eu ordeno. E o Calendário mostra por mês, semana ou dia. O sistema lembra a visão que você escolheu. |

Mundo/backend: update de `schedule_tasks.status` para `em_andamento`. A fala "pra editar ou excluir, é na aba Tarefas"
do fim do cap11 passa a ter a tela correspondente.

### Efeito nos capítulos seguintes (se P3, P5 e P6 entrarem)

- cap10, última linha: ao entrar em "Visita técnica", o cartão ganha checklist, tarefa vinculada e previsão 25/11. A fala
  pode ganhar "e a automação da Visita técnica já entra em ação".
- cap11: a aba Tarefas abre com "Agendar visita…" e "Documentos da Metalúrgica Jequitibá" em "Concluída" e "Ligar pro
  Paulo" em "Pendente"; o Calendário mostra os dias 11, 12 e 13 (a fala "cada tarefa no seu dia" não muda).
- cap12: valores iguais. O cartão da Jequitibá mostra 25/11, "3/3", "80%" e "Telefone". A semente `apos-cap11-dia`
  precisa refletir isso.
- cap13: acrescentar uma frase: "Montou uma automação com checklist e prazo, marcou o checklist na ficha, ajustou a
  probabilidade e a origem, comentou, e fechou um negócio arrastando pra Ganho."

## 4. Estimativa

A 2,6 palavras por segundo (a conta do roteiro):

| Proposta | Onde | Palavras | Segundos de fala |
| --- | --- | --- | --- |
| P1 | cap03 | 73 | 28 |
| P2 | cap05, cap06 | 41 | 16 |
| P3 | **cap07b** (novo) | 284 | 109 |
| P4 + P4b | cap08, cap07 | 92 | 35 |
| P5 | **cap10b** (novo) | 114 | 44 |
| P6 | **cap10c** (novo) | 174 | 67 |
| P7 | cap10c | 90 | 35 |
| P8 | cap12 | 86 | 33 |
| P9 | cap11 | 80 | 31 |
| cap13 | recapitulação | 30 | 12 |
| **Total** | | **≈ 1.064** | **≈ 410 s (6,8 min)** |

- **Capítulos novos: 3** (`cap07b`, `cap10b`, `cap10c`), mais 3 vinhetas e 1 ilustração (barra de probabilidade).
- A aula vai de ~15 min para ~23 min de vídeo (fala de 11,6 para ~18,4 min, mais o tempo das ações e das vinhetas).
- Mudanças do app a aplicar: **0**. Divergências antigas a acertar: 5 (seção 1.1; só a do responsável mexe na fala).
- Lacunas levantadas: 41 (20 "sim", 15 "só citar", 6 "não").

## 5. Depende de decisão

1. **Tamanho**: +6,8 min de fala numa aula de 15. Se for demais, a ordem de corte sugerida é P9, P4b, P7, P2 (a
   aula perde detalhe, não perde função principal). P3, P5, P6 e P8 são o que hoje mais falta.
2. **"Definir prazo do cartão" troca a previsão de 30/11 para 25/11** no cartão da história. Alternativa sem efeito
   colateral: trocar a segunda ação por "Adicionar etiqueta" com uma etiqueta nova (pede criar a etiqueta no cap07).
3. **WhatsApp na ficha**: mostrar pede telefone fictício no cartão da Jequitibá e deixa na tela um link para fora do
   sistema. Proposta: só citar (como está no P7).
4. **Excluir funil e excluir oportunidade**: a proposta abre a confirmação e cancela. Mostrar a exclusão de verdade
   pediria um funil e um cartão descartáveis no mundo.
5. **Uma aula ou duas**: com 17 capítulos, dá para partir em "CRM: funil, regras e automações" (cap00 a cap07b) e
   "CRM: oportunidades, tarefas e filtros" (cap08 a cap13).
