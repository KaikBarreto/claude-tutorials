# T5 · Ordens de Serviço, Agenda, Equipes e Mapa ao Vivo · inventário do app 1.38.6

Levantamento feito em 30/10/2026 sobre `/home/claude/domiflix/src-1.38.6` (somente leitura; só análise estática, o app e o
backend falso não foram executados). Convenções:

- Caminhos `arquivo:linha` são relativos a `src/` da 1.38.6 (ex.: `pages/ServiceOrders.tsx:147`). `rec/...` = `/home/claude/domiflix/rec/`.
  `supabase/...` = raiz do repositório extraído (migrations).
- `os.ts` = `lib/i18n/messages/app/os.ts` (pt-br vai até a linha ~1762; as outras línguas vêm depois). `schedule.ts` = `lib/i18n/messages/app/schedule.ts`
  (pt-br até a linha ~203). `finance.ts` = `lib/i18n/messages/app/finance.ts`.
- Rótulos entre aspas estão EXATOS como aparecem na tela. Onde o texto é fixo no componente (fora do i18n), a linha do componente é a fonte.
- O app que o robô usa é a 1.38.5; as telas de T5 (`ServiceOrders.tsx`, `ServiceOrderFormDialog.tsx`, `Schedule.tsx`, `LiveMap.tsx`, `TeamsPanel`)
  não foram comparadas byte a byte com a 1.38.5. Dúvida 7.1.
- O guia técnico do app (`docs/guia-tecnico/`) e a trilha embutida em `docs/domiflix/trilha-de-tutoriais.md` são idênticos à 1.22.5 (`diff` sem saída):
  não servem de verificação do que mudou. O código manda.

---

## 0. Resumo para o roteiro

### 0.1 Capítulos da trilha (1.22.5) × código de hoje

| # | Capítulo da trilha 1.22.5 | Situação na 1.38.6 | Evidência |
|---|---|---|---|
| 1 | Tela Ordens de Serviço: kanban × lista e 4 indicadores | **Bate, com ajustes.** A tela abre em **Kanban** (preferência guardada no navegador: `os-view-mode`), com período **"Todo o período"** (antes era o mês). Os 4 indicadores continuam: "OS Abertas", "Concluídas", "Atrasadas", "Próximos 7 dias". Agora a tela tem menu lateral de 4 abas: "Ordens de Serviço", **"Chamados"** (nova), "Relatório", "NPS e Satisfação". | `ServiceOrders.tsx:147-168, 448-458, 489-494`; `os.ts:11-70` |
| 2 | Criar OS · Etapa 1: cliente cadastrado × avulso e tipo de serviço | **Mudou.** O assistente agora tem **4 etapas** (a 2ª é nova: "Orçamento"). A etapa 1 é "Cliente e Serviço": alternância "Cliente cadastrado"/"Cliente avulso", "Tipos de Serviço" (**vários**), botão "Criar cliente" ao lado do campo e o **"Endereço de serviço"** (era capítulo 6). | `ServiceOrderFormDialog.tsx:1150-1155, 1938-1976, 2205-2325`; `os.ts:152-197` |
| 3 | Etapa 2: equipamentos e checklists (e quando a etapa nem aparece) | **Não bate.** A etapa "Equipamentos e Checklists" **sempre aparece** (guarda os "Checklists avulsos"). O que some é só o bloco "Equipamentos", quando **nenhum** dos serviços escolhidos é "Vinculado a equipamento". Novos desde a 1.36.22: serviços por equipamento, "Copiar para outros" e "Revisão do escopo da OS". | `ServiceOrderFormDialog.tsx:289-292, 1157-1160, 1442-1520`; `os.ts:199-275` |
| 4 | Etapa 3: técnico e/ou equipe, data, duração, descrição | **Mudou.** Vira a etapa 4, "Agendamento e Detalhes": "Responsáveis" (técnicos e **Equipes** no mesmo seletor), **"Período do atendimento"** (data inicial/final, até 31 dias, "Jornadas por dia", desde 1.37.10) no lugar de data+horário+duração soltos, "Descrição do Serviço", "Observações". Conflito de horário abre um aviso com justificativa (1.36.0). | `ServiceOrderFormDialog.tsx:1342-1383, 1990-2032`; `os.ts:210-235, 279-282`; `Schedule.tsx:774-809` |
| 5 | Recorrência (diária, semanal, quinzenal, mensal, anual, personalizada) | **Bate, e ganhou prévia.** Só na criação. Campo "Até" obrigatório; mostra "Serão criadas N OS, de X até Y."; o botão final vira "Criar OS Recorrentes". | `ServiceOrderFormDialog.tsx:350-367, 2352-2432, 2136`; `os.ts:285-309` |
| 6 | Endereço de serviço diferente do cliente | **Bate**, mas fica na etapa 1. Alternância "Sim/Não" em "Endereço de serviço (diferente do cliente)". | `ServiceOrderFormDialog.tsx:1265-1337`; `os.ts:192-197` |
| 7 | Toggle "gerar Pesquisa de Satisfação ao finalizar" | **Bate.** "Gerar Pesquisa de Satisfação ao finalizar?" Sim/Não; o padrão vem da configuração de NPS da empresa. | `ServiceOrderFormDialog.tsx:549-561, 2017-2030, 2440-2450`; `os.ts:312` |
| 8 | Mover status arrastando e o "+" da coluna | **Bate.** Arrastar o cartão muda o status na hora, sem confirmação. Soltar em "Concluída" pode abrir a pergunta de receita. Sem "+" em "Concluída"/"Cancelada". Nova: coluna fixa **"Chamados do Portal"**, só quando existe chamado sem data. | `ServiceOrders.tsx:372-393, 402-446, 1160-1164, 1181-1195`; `os.ts:116-118` |
| 9 | Configurar Status: status próprio, cor e ordem | **Reduzido.** O botão "Configurações" abre "Configurações de OS" só com: criar status (nome + cor), editar, reordenar arrastando, excluir. Prefixo/formato do número, SLA por tipo e campos obrigatórios por status **existem no código mas não aparecem** na janela. | `OsStatusManagerDialog.tsx:142-303` (UI) × `:32-137, 164-169, 218-241` (sem tela) |
| 10 | Filtros, busca e por que a busca ignora o período | **Bate.** Com texto digitado a busca olha todas as OS e mostra "Mostrando resultados de todas as OS (filtros pausados)". Filtro "Status" fica num botão "Filtros" dentro do campo de busca. | `ServiceOrders.tsx:193-261, 696-740`; `os.ts:43-56` |
| 11 | Abrir a OS no app do técnico sendo gestor, e compartilhar o link | **Mudou nos nomes.** No detalhe: botão grande "Preencher OS" (ou "Relatório de Serviço" se concluída) e ação "Link OS" que copia o endereço público. Na tabela: "Visualizar OS", "Abrir checklist" (abre o app do técnico em **nova aba**). O link copiado tem endereço fixo `https://dominex.app/...`. | `ServiceOrderViewDialog.tsx:706-730, 786-793`; `ServiceOrders.tsx:1005-1013`; `utils/shareLinks.ts:27-45` |
| 12 | Aba Relatório | **Bate**, com bloco novo "Saúde do agendamento". Calculado no navegador com as OS carregadas, período padrão "Este mês". | `OsReportDashboard.tsx:45-54`; `os.ts:762-794` |
| 13 | Aba NPS: promotores, neutros, detratores, estrelas, comentário | **Mudou.** Critérios de estrela agora são **configuráveis** (lista que o gestor edita), há "Ranking de Técnicos", "Detratores em Aberto" com selo "Atenção" e "Feed de Feedbacks" com filtros. | `NpsDashboard.tsx:64-120`; `os.ts:660-727` |
| 14 | Nota mínima + convite para avaliar no Google | **Mudou de lugar e de jeito.** Dentro de "Configurações de NPS": "Link do Google Maps" + "Gerar link de avaliação" (consulta a edge `resolve-google-maps-link`) e "Quando convidar o cliente" = "Mostrar sempre" ou "A partir de uma nota". | `NpsSettingsModal.tsx:51, 115`; `hooks/useResolveGoogleMapsLink.ts:28`; `os.ts:729-758` |
| 15 | Tela Agenda: Dia, Semana, Mês (e por que o celular abre em Dia) | **Bate** (computador abre em **Mês**, celular em **Dia**). Novo: seletor **"Calendário"/"Lista"** (1.24.38). | `Schedule.tsx:131-183, 925-1010`; `schedule.ts:24-47` |
| 16 | Criar pelo "+": Nova OS × Nova Tarefa | **Bate.** O botão chama-se "Nova Tarefa/OS" e abre "O que deseja criar?" com "Ordem de Serviço" e "Tarefa". Duplo clique no dia e clique no horário também abrem. | `Schedule.tsx:655-676`; `schedule.ts:29-35, 96-102` |
| 17 | Reagendar arrastando, legenda de cores e feriados | **Mudou por dentro.** Arrastar uma OS com responsável passa pela reserva atômica do servidor (RPC) e pode abrir o aviso de conflito; tarefa e OS sem responsável só atualizam a data. Legenda por tipo de serviço e "Feriado"; feriados calculados no navegador. | `Schedule.tsx:678-733, 227-250`; `schedule.ts:78-84` |
| 18 | Ordens Pausadas e a retomada em duas datas | **Bate.** Botão "OS Pausadas" abre a lista com "Retomar agora"; a OS retomada reaparece nos dias seguintes com selo "Retomada". | `Schedule.tsx:310-347`; `schedule.ts:62-77, 187-189` |
| 19 | Equipes: time com cor, ícone, foto e membros | **Bate**, ainda como aba **"Equipes"** dentro de **Funcionários** (exige o módulo RH). "Membros" lista **qualquer colaborador ativo** (1.37.55). | `Employees.tsx:373-388, 1499-1500`; `App.tsx:868-869`; `TeamFormDialog.tsx:143-251`; `os.ts:1621-1636` |
| 20 | Escalar equipe inteira numa OS | **Bate.** No seletor "Responsáveis" há a seção "Equipes"; marcar a equipe marca todos os membros. A OS grava a **primeira** equipe marcada como `team_id`. | `AssigneeMultiSelect.tsx:77-92`; `ServiceOrderFormDialog.tsx:656-657, 723`; `os.ts:1640-1646` |
| 21 | Mapa e Rastreamento: cores dos marcadores, posição em tempo real | **Bate.** Título "Mapa e Rastreamento", aba "Mapa ao Vivo", legenda ("Executando OS", "A Caminho", "Check-out", "Destino cliente", "Base da empresa"). Posição ao vivo vem de carga inicial + canal em tempo real. | `LiveMap.tsx:443-509`; `os.ts:1095-1119` |
| 22 | Aba Histórico | **Bate.** Filtros "Técnico" e "Data", estatísticas "Check-ins", "Check-outs", "Distância", "Tempo em campo". | `components/tracking/TrackingHistoryTab.tsx`; `os.ts:1122-1148` |

### 0.2 O que mudou desde a 1.22.5 (datado pelo changelog embutido em `pages/Changelog.tsx`)
- **1.23.0** número da OS sem zeros à esquerda ("OS #123"); consumo de estoque dentro da OS (T7/T8).
- **1.24.23** pergunta "Houve alguma receita nesta Ordem de Serviço?" ao concluir (opção da empresa + permissão). **1.24.38** Agenda em Lista + filtro Tarefa×OS. **1.24.40** permissão "Gerenciar Tarefas".
- **1.32.4 / 1.36.1** botão **"Faturar OS"** (lista, detalhe, agenda). **1.28.22** "Converter orçamento em OS" volta a funcionar; **1.36.22** "Gerar OS" leva serviços, materiais e valores do orçamento.
- **1.35.0** avisos de WhatsApp ao cliente (a caminho/início/fim). **1.35.8, 1.37.28, 1.37.30** aba **Chamados** e coluna "Chamados do Portal".
- **1.36.0** agendamentos protegidos contra conflito (reserva atômica, também usada pela API pública). **1.36.3 / 1.36.5** **"Resetar OS"** / "Reabrir OS". **1.36.22-24** serviço e checklist **por equipamento**, "Copiar para outros", revisão do escopo.
- **1.37.10** OS com **vários dias** e horário por jornada. **1.37.28** agenda navega até a OS criada, aviso diz número e data, OS abre em "Todo o período", OS sem data não some. **1.37.48** conflito autorizado por quem tem permissão, com justificativa. **1.37.55** equipes aceitam colaboradores de qualquer área.
- **Sem entrada exata no changelog:** a etapa "Orçamento" e "Tipos de Serviço" em vários (a primeira pista é o texto de 1.36.23 "Em uma OS com vários serviços").

### 0.3 O que o roteiro precisa saber antes de escrever
1. **O formulário de Nova OS mudou de forma (4 etapas, vários serviços, orçamento, período).** O capítulo da trilha ("3 etapas") não vale: o roteiro novo é "Cliente e Serviço" → "Orçamento" → "Equipamentos e Checklists" → "Agendamento e Detalhes". Dá para pular a etapa "Orçamento" (tudo é opcional) mas ela existe e o botão "Próximo" passa por ela.
2. **Só "Cliente" é obrigatório** para avançar (etapa 1) e para salvar; tipo de serviço, equipamento, responsável e data **não** são. Sem data/hora a OS nasce com os valores de "agora" (data de hoje e hora atual). (`ServiceOrderFormDialog.tsx:300-317, 1164-1170`).
3. **A OS criada sem escolher status nasce "Pendente"** no banco real; só a criação pelo "+" da coluna do Kanban grava o status da coluna (`ServiceOrderFormDialog.tsx:120-122, 823`; default do banco em `supabase/migrations/20260131190034_d842ab49-6aeb-4fcb-ab46-1b86a7a5ce92.sql`, `status os_status NOT NULL DEFAULT 'pendente'`). No backend falso nasce "Agendada" por falta de default (ver seção 4). Já a recorrência grava `'pendente'` explicitamente (`:738`).
4. **Arrastar no Kanban e trocar o status na linha da lista não pedem confirmação**; só o "Excluir" e o "Resetar OS" confirmam (`ServiceOrders.tsx:372-393, 1160-1164`).
5. **"Reabrir OS" × "Resetar OS" é o mesmo botão:** o rótulo muda com o status ("Reabrir OS" se concluída; "Resetar OS" se a caminho/em andamento/pausada) e a ação sempre devolve a OS para **Agendada**, perguntando se mantém ou apaga o preenchimento (`types/database.ts:20-26`; `ResetServiceOrderDialog.tsx:44-105`).
6. **Equipes não são uma tela própria:** estão em Funcionários › "Equipes", e o menu "Gestão › Funcionários" some sem o módulo RH (Glacial tem; o roteiro precisa avisar com "🔒"). Resposta à pendência 4 da trilha: **sem RH a aba não existe** (`App.tsx:869`, `SidebarMenuContent.tsx:117`); a criação de OS continua mostrando equipes já cadastradas (`useTeams` não checa módulo).
7. **Tarefas e OS moram na mesma tabela**; a tela de OS esconde as tarefas (`serviceOrderAccess.ts:11-16`, `ServiceOrders.tsx:201`) e a Agenda mostra as duas.
8. **Mapa: o técnico só aparece com posição enviada pelo celular** (carga dos últimos 120 minutos): sem dados o mapa fica só com a "Base da empresa" (`useLiveTechnicianLocations.ts:63-72`). A gravação precisa de posições semeadas (seção 4).

---

## 1. Rotas e navegação

| Tela | Caminho no menu | URL (pt-br) | Componente | Guarda |
|---|---|---|---|---|
| Ordens de Serviço | Operacional › Ordens de Serviço | `/ordens-servico` (`?aba=chamados`, `?os=<id>` abre o detalhe) | `pages/ServiceOrders.tsx` | `screen:service_orders` (`App.tsx:790`) |
| Agenda | Agenda (item de topo) | `/agenda` | `pages/Schedule.tsx` | `screen:schedule` (`App.tsx:797`) |
| Mapa e Rastreamento | Operacional › Mapa e Rastreamento | `/mapa-ao-vivo` (`/rastreamento` redireciona) | `pages/LiveMap.tsx` | `screen:tracking` (`App.tsx:884-885`) |
| Equipes | Gestão › Funcionários › aba "Equipes" | `/funcionarios` (`/equipes` redireciona) | `components/teams/TeamsPanel.tsx` dentro de `pages/Employees.tsx` | `screen:employees` + módulo `rh` (`App.tsx:868-869`) |
| App do técnico (T7) | botões "Preencher OS", "Abrir checklist", "Relatório de Serviço" | `/os-tecnico/:id` | `pages/TechnicianOS.tsx` | rota pública (`App.tsx:742`) |

- Menu: `components/layout/SidebarMenuContent.tsx:98-105, 117`. Ordem: Dashboard › **Agenda** › **Operacional** (Ordens de Serviço, Mapa e Rastreamento) › Área do Técnico™ › Orçamentos › **Gestão** (Serviços, Clientes e Fornecedores, Equipamentos, Contratos, Funcionários, Estoque).
- Deep-links úteis para a gravação: `/ordens-servico?aba=chamados` (`ServiceOrders.tsx:115-117`) e `/ordens-servico?os=<id>` (`:118-122`) abrem direto a aba e o detalhe.
- A Agenda abre já em Lista ou Calendário e no período do último uso: a preferência é gravada **por aparelho** (`hooks/useUserPreferences.ts:116`, `Schedule.tsx:140-183`); só a escolha manual grava, o padrão não. Na Glacial existe 1 linha em `user_preferences` (`rec/fakebase/seeds/gen-01-tenant.json`).
- A tela de OS tem **menu lateral de abas** (`SettingsSidebarLayout`, `ServiceOrders.tsx:607`) no computador; no celular as abas viram o seletor padrão. Não existe `?aba=` para Relatório/NPS (só `chamados`).
- Tarefa (compromisso interno) abre pelo botão "Nova Tarefa/OS" da Agenda; não há tela de lista de tarefas (a lista de OS as esconde).

---

## 2. Permissões e módulos

| Chave | Rótulo em Configurações › Usuários | O que muda nesta aula |
|---|---|---|
| `screen:service_orders` | "Ordens de Serviço" (Serviços) | Sem ela, a rota não abre (`usePermissions.ts:58`). |
| `fn:create_os` | "Criar OS" | Botão "Nova OS", "+" das colunas e FAB mobile (`ServiceOrders.tsx:182, 727, 1181, 1299`). |
| `fn:edit_os` | "Editar OS" | Ações "Editar" (lista, cartão, detalhe) (`:183, 806, 1019, 1214`). |
| `fn:delete_os` | "Excluir OS" | Ações "Excluir" (`:184, 825, 1038, 1236`). |
| `fn:reopen_os` | "Resetar OS" | Ação "Reabrir OS"/"Resetar OS" (`:185, 813, 1025`; `usePermissions.ts:130`). Admin/gestor sempre têm. |
| `fn:os_finish_revenue` | "Lançar Receita ao Finalizar OS" | Controla a pergunta de receita ao concluir e a ação "Faturar OS", que ainda exige `screen:finance` (`hooks/useOsBillingAction.ts:37-38`, `usePermissions.ts:118`). |
| `screen:schedule` | "Agenda" (Geral) | Sem ela, nem a própria agenda aparece (`usePermissions.ts:57`). |
| `fn:override_schedule_conflict` | "Sobrescrever Conflito de Agenda" | Só quem tem o registro **explícito** vê o campo "Justificativa obrigatória"; admin sem registro não vale (`Schedule.tsx:109-112`; `usePermissions.ts:122`). |
| `fn:manage_tasks` | "Gerenciar Tarefas" | Quem tem vê tarefas de todos; os demais só as próprias, as que são do seu time ou as atribuídas a eles (`Schedule.tsx:255-272`; `lib/taskVisibility.ts:24, 41-49`; `usePermissions.ts:138`). Admin vê tudo. |
| `fn:view_all_schedule` | "Ver Toda a Agenda" | Dá o mesmo acesso total às tarefas (`lib/taskVisibility.ts:24`; `usePermissions.ts:131`). |
| `screen:tracking` | "Mapa e Rastreamento" (Operacional) | Mapa ao Vivo e Histórico (`usePermissions.ts:69`). |
| `screen:employees` + módulo **rh** | "Funcionários" | Dá acesso à aba "Equipes". Sem módulo: menu e rota bloqueados (`App.tsx:869`). |

- Papel **técnico** (`hasRole('tecnico')`): a Agenda mostra só as OS em que ele é responsável (direto ou pela equipe) (`Schedule.tsx:274-279`). Tarefas dele seguem a regra de "Gerenciar Tarefas".
- Módulos: `rh` (Equipes), `cobrancas` (opção "Gerar cobrança" no "Faturar OS", `OsBillingDialog.tsx:120-123`), `contracts` (OS de contrato/PMOC aparece com selo "PMOC" e aviso extra no campo Descrição). A Glacial tem todos ligados (`MUNDO_FICTICIO.md`).
- Configurações da empresa que mudam a tela (seed `company_settings` da Glacial): `os_finish_revenue_prompt_enabled = true` (pergunta de receita ao concluir) e `os_stock_consumption_enabled = true` (T7) — `rec/fakebase/seeds/gen-01-tenant.json`.
- Configurações de NPS (`nps_settings`): só a gestão edita; para os demais a janela mostra "Somente a gestão pode alterar estas configurações." (`os.ts:682`, `NpsSettingsModal.tsx:236`). A tabela `nps_settings` está **vazia** no seed (`rec/fakebase/seeds/00-vazias.json`), então vale o padrão do hook.

---

## 3. Por tela / janela / aba

### 3.1 Ordens de Serviço (`pages/ServiceOrders.tsx`)
**Cabeçalho e abas.** Título "Ordens de Serviço", subtítulo "Gerencie suas ordens de serviço" (`os.ts:11-14`; `ServiceOrders.tsx:591-605`). No computador o filtro de período
(`DateRangeFilter`, padrão **"Todo o período"**, `:168`) fica à direita do título e só aparece na aba "Ordens de Serviço". Menu lateral de abas (`:448-458`):
"Ordens de Serviço" · "Chamados" (com contador de chamados abertos ao lado) · "Relatório" · "NPS e Satisfação".

**Aba "Ordens de Serviço" (computador).**
- Barra: campo de busca com texto "Buscar por OS, cliente, telefone, endereço ou serviço..." e, dentro dele, o botão **"Filtros"** (grupo "Status": uma caixa por status
  do cadastro, com a cor) (`:696-717`; `os.ts:44, 48-51`); botão **"Configurações"** (engrenagem; o texto some em tela estreita, `:720-726`); botão **"Nova OS"** só com
  `fn:create_os` (`:727-732`).
- Quando há texto na busca aparece a linha "Mostrando resultados de todas as OS (filtros pausados)" (`:736-740`; `os.ts:46`).
- 4 cartões (KPI): "OS Abertas", "Concluídas", "Atrasadas", "Próximos 7 dias" (`:489-494, 742-750`). Contam o que passou pelo filtro de período/status. "Atrasadas"
  = não concluída/cancelada com data anterior a hoje; "Próximos 7 dias" = de hoje até +7 (`:468-487`).
- Alternador **Lista/Kanban**: dois botões só com ícone (lista, grade) à direita do título da seção ("Lista de OS" ou "OS por Status"); a escolha fica gravada no navegador
  (`:147-161, 754-777, 1067-1100`). Padrão Kanban. Em Kanban com recorte ativo aparece "Mostrando N de M OS" (`:1079-1085`; `os.ts:85`).
- Código mostrado da OS: `<prefixo do tipo de serviço>-<ano>-<número>`, ex.: `MP-2026-12`; sem tipo usa o prefixo `OS`; o ano vem da data agendada (ou da criação) (`:187-191`).
  A prévia "-2026-0001" do cadastro do tipo (T4, pegadinha P4) **não** é o que a lista mostra.

**Lista (tabela).** Colunas "OS", "Criador" (avatar com dica "Criador da OS"), "Cliente" (2ª linha: nome do equipamento), "Tipo" (bolinha de cor + nome), "Data", "Status",
"Ações" (`:918-924`; `os.ts:87-95`). Selos: "PMOC" (contrato PMOC) e "Faturada"/"Cobrança enviada" (`:938-946`; `finance.ts:1553-1558`). **Status é um seletor colorido na própria
linha: trocar já grava** (`:982-999`). Paginação ao pé (`:1049-1058`). Menu de ações da linha (`:1003-1040`): "Visualizar OS", "Abrir checklist" (abre `/os-tecnico/<id>` em **nova aba**),
"Editar", "Reabrir OS"/"Resetar OS" (só `fn:reopen_os` e status a caminho/em andamento/pausada/concluída), "Faturar OS" (só quem pode faturar), "Excluir".
Vazio: "Nenhuma OS cadastrada" + "Clique em "Nova OS" para começar"; com filtro: "Nenhuma OS encontrada" + "Tente filtros diferentes" (`os.ts:98-106`).

**Kanban.** Uma coluna por status do cadastro (`os_statuses`, na ordem `position`): cabeçalho com barra colorida, nome em maiúsculas, contagem e **"+"**
(título "Criar OS em "{status}""; some em "Concluída" e "Cancelada") (`:402-446, 1147-1198`). Cartão: código, selo "Faturada", cliente, tipo, data e avatar do criador; ao passar o mouse
aparecem lápis (Editar), seta circular (Reabrir/Resetar) e lixeira (Excluir) (`:1204-1295`). **Clicar abre o detalhe; arrastar para outra coluna muda o status na hora** (`:1160-1164, 1206-1207`).
Coluna vazia: "Nenhuma OS". Coluna **"Chamados do Portal"** (primeira, azul) só existe se houver chamado de portal **sem data**; esvazia sozinha quando a OS ganha data (`:395-425`;
`os.ts:83-84, 104-105`; changelog 1.37.28/30). Não dá para arrastar para dentro dela nem tirar cartões dela arrastando (`:1159, 1206`).

**Pergunta de receita (ao concluir).** Depois que a OS é gravada como concluída (arrastando, no seletor da lista, ou "Finalizar" no detalhe/Agenda) abre "Receita da Ordem de Serviço":
"Houve alguma receita nesta Ordem de Serviço?", dica "Se entrou (ou vai entrar) dinheiro por este serviço, lance agora e o valor já fica vinculado a esta OS.", mostra OS, Cliente e
"Valor da OS", botões "Não" e "Sim, lançar receita" (`finance.ts:1517-1531`; `ServiceOrders.tsx:372-393, 1376-1378`). Só aparece se a empresa ligou a opção (`os_finish_revenue_prompt_enabled`,
**ligada no seed**), a pessoa tem `fn:os_finish_revenue` e a OS ainda não tem receita (`hooks/useOsFinishRevenuePrompt.ts:60-70`). Nunca bloqueia o fechamento.

**Excluir OS.** Confirmação "Excluir OS #N" + "Tem certeza que deseja excluir? Esta ação não pode ser desfeita." com "Cancelar"/"Excluir". Se a OS faz parte de recorrência ou contrato
pergunta antes: "Esta OS faz parte de uma recorrência. O que deseja fazer?" com "Excluir apenas esta" / "Excluir todas da recorrência" (`:1316-1347`; `os.ts:119-127`). Toast "OS excluída com sucesso!"
(`useServiceOrders.ts:751-756`).

**Celular** (não gravar): busca "Buscar OS...", botão "Filtros" (folha com período, status, "Visualização" Lista/Kanban e "Gerenciar status de OS"), cartões em carrossel e FAB "OS"
(`:654-694, 778-905, 1298-1305`).

### 3.2 Nova OS / Editar OS (`components/service-orders/ServiceOrderFormDialog.tsx`)
Janela "Nova Ordem de Serviço" (ou "Editar OS"), 920 px, com indicador numerado de etapas e rodapé "Voltar" · "Cancelar" · "Próximo" (último passo: "Criar OS", ou "Criar OS Recorrentes"
com recorrência ligada; na edição, "Salvar") (`:1907, 2149, 2119-2145`; `os.ts:153-168`). Só a etapa 1 tem trava: "Próximo" fica desligado sem cliente (`:1164-1170`).
Se existir rascunho de um preenchimento interrompido, antes de tudo aparece **"Rascunho encontrado"** com "Começar do zero" e "Retomar rascunho" (`components/ui/DraftResumeDialog.tsx:58-70`).
O rascunho é salvo a cada mudança, **só em criação**, em `sessionStorage` (`form-draft:service-order-form`) e guarda: campos do formulário (datas, descrição, notas, plano), cliente escolhido, tipos
de serviço e itens do orçamento; **não** guarda equipamentos, checklists, responsáveis, recorrência, NPS nem endereço de serviço (`:337-378, 2150-2177`; `hooks/useFormDraft.ts:53, 79, 118`).

**Etapa "Cliente e Serviço"** (`:1938-1976` edição; `:2205-2325` criação)
- Alternância **"Cliente cadastrado" / "Cliente avulso"** (só na criação). Cadastrado: campo "Cliente *" (placeholder "Selecione o cliente", busca "Buscar cliente...") com botão **"Criar cliente"**
  ao lado (`:2221-2240, 2483-2492`; `os.ts:171-176`). Avulso: "O cliente será criado automaticamente com os dados abaixo." + "Nome *", "Telefone", "CEP", "Endereço", "Bairro", "UF / Cidade" (`os.ts:177-184`).
  Cliente avulso vira registro de cliente de verdade (`createCustomer`, `:631-645`).
- **"Endereço de serviço (diferente do cliente)"** com alternância Sim/Não; ligado revela "CEP", "Número", "Endereço", "Bairro", "UF / Cidade" e o texto "O atendimento será feito neste endereço (filial, obra, evento). Quando vazio, usa o endereço do cliente." (`:1265-1337`;
  `os.ts:192-197`). Ao salvar, o endereço é geocodificado sem travar (`:563-575`).
- **"Tipos de Serviço"**: seletor múltiplo ("Selecione", busca "Buscar tipo de serviço...", opção "Nenhum"; só tipos **ativos**) com atalho para criar tipo na hora; um serviço que já tem linha no orçamento fica
  travado (`:1960-1974`; `components/service-orders/ServiceTypesMultiSelect.tsx`; `os.ts:185-188`).

**Etapa "Orçamento"** (`:1978-1983`; `ServiceOrderBudgetSection.tsx:35-82`)
- Título "Serviços, mão de obra e materiais" e texto "Estes valores formam o orçamento da OS e serão sugeridos ao faturar. O consumo real de estoque é registrado separadamente na execução." (texto fixo, fora do i18n).
- Tabela de itens (`quotes/QuoteItemsTable.tsx:250-420`): bloco "Serviços e Mão de Obra" (colunas "Serviço", "Qtd", "Valor Unit.", "Total"; seletor "Selecionar serviço...", vazio "Nenhum serviço adicionado.")
  e bloco de materiais ("Selecionar material...", "Nenhum material adicionado."). Rodapé: "Serviços e mão de obra", "Materiais", "Ajustes e descontos do orçamento" (se houver) e **"Total para faturamento"**.
- Escolher serviços na etapa 1 **não cria linhas** aqui; adicionar uma linha de serviço aqui **inclui o serviço** no escopo da OS (`:1254-1261`). Materiais vêm do estoque (`inventory`, vazio no seed).

**Etapa "Equipamentos e Checklists"** (`:1442-1850`)
- Bloco **"Equipamentos"** só aparece se algum serviço escolhido é "Vinculado a equipamento" (ou se nenhum serviço foi escolhido) (`:289-292, 1445`). Texto "Selecione um ou mais equipamentos para esta OS." (ou "Selecione o equipamento." com 1),
  botões "Selecionar todos"/"Desmarcar todos" e "+" ("Criar equipamento"); mensagens "Nenhum equipamento cadastrado para este cliente.", "Selecione um cliente primeiro para ver equipamentos.", e para avulso "Salve a OS para depois cadastrar equipamentos deste cliente." (`:1451-1518`; `os.ts:199-209`).
- Cada equipamento é uma linha com caixa de seleção, foto, nome/marca/modelo e setinha que abre: **"Serviços neste equipamento"** ("Escolha o que será executado aqui. Os checklists abaixo acompanham essa seleção.", "Adicionar serviço neste equipamento...",
  "O equipamento precisa manter pelo menos um serviço da OS."), **"Copiar para outros"** (janela "Copiar serviços e checklists"; botão "Copiar para N") e **"Checklists aplicados"** com "Adicionar checklist...", "Pré-visualizar checklist" e "{n} perguntas"
  (`:1532-1760`; `os.ts:238-266`). Só entram checklists cujos "Serviços habilitados" combinam com os serviços do equipamento (vazio = todos) (`lib/serviceOrderServices`, `:1526-1531`).
- Bloco **"Checklists avulsos"** ("Checklists a nível de OS, sem equipamento vinculado.", "Buscar checklist...") (`:1770-1830`; `os.ts:247-249`).
- Ao salvar com mudança de escopo que apague respostas já preenchidas: "Existem respostas preenchidas" · "Remover e salvar" (só edição) (`:2084-2114`; `os.ts:272-276`).

**Etapa "Agendamento e Detalhes"** (`:1990-2032`; criação `:2336-2450`)
- Se a OS tem checklists/equipamentos aparece antes o quadro **"Revisão do escopo da OS"** ("Confira os serviços e checklists de cada equipamento antes de salvar.") (`:1385-1441`; `os.ts:267-271`).
- **"Responsáveis"** (`AssigneeMultiSelect`): botão com "Selecione..." (ou nomes escolhidos), busca, "Marcar todos"/"Desmarcar todos", seção "Equipes" e lista de técnicos. Marcar uma equipe marca todos os membros; a OS guarda a **primeira** equipe
  em `team_id` e os usuários em `service_order_assignees` (`components/schedule/AssigneeMultiSelect.tsx:44-130`; `ServiceOrderFormDialog.tsx:656-657, 818-819`; `hooks/useServiceOrders.ts:370-390`). A lista traz **todos** os perfis (inclui a admin), não só técnicos (`hooks/useProfiles.ts:6-19`).
- **"Período do atendimento"** (`ServiceOrderSchedulePlanner.tsx`): "Data inicial", "Data final", e quadro **"Jornadas por dia"** ("Selecione o período e ajuste quando cada jornada começa e termina. Máximo de 31 dias."), por dia "Quando começa"/"Quando termina",
  "Aplicar a todos", contador "N dia(s) agendado(s)". Regra: término entre 15 minutos e 8 horas depois do início ("O término deve ficar entre 15 minutos e 8 horas após o início.") (`os.ts:211-235`; `lib/serviceOrderSchedule`). Padrão: hoje, hora atual, 2 h (`:300-317, 329`).
- "Descrição do Serviço" (placeholder "Descreva o serviço a ser realizado"; em OS de contrato PMOC mostra aviso amarelo sobre o portal público) e "Observações" (`:1996-2008`; `os.ts:279-282, 334`).
- **Recorrência** (**só na criação**): interruptor "Recorrência"; ligado mostra "Frequência" (Diária, Semanal, Quinzenal, Mensal, Anual, Personalizado), "A cada" + unidade, "Até *", "Repetir em:" com D S T Q Q S S (semanal/personalizada) e a prévia
  "Serão criadas N OS, de X até Y." ou aviso vermelho ("Informe até quando a recorrência vai...", "Escolha pelo menos um dia da semana...", "Com essas opções só uma OS seria criada...") (`:2352-2432`; `os.ts:285-307`). Cria todas as OS de uma vez, com o mesmo `recurrence_group_id`, status "pendente", e a mesma lista de responsáveis; toast "{n} OS(s) criada(s) com recorrência!" (`:695-798`).
- Na **edição** de OS de recorrência/contrato, mudar data pergunta: "Editar recorrência" (Apenas esta/Todas da recorrência) ou "Alterar data da recorrência?" (Apenas esta/Esta e futuras) (`:2038-2082`; `os.ts:315-323`).
- **"Gerar Pesquisa de Satisfação ao finalizar?"** com Sim/Não (`:2017-2030`).
- Em edição aparece também o bloco de materiais consumidos da OS ("somente leitura", some se vazio) (`:2010-2015`; `OsMaterialsSection`). Não há campo de assinatura obrigatória (estado só zerado em `:199-200, 456`).

**Ao salvar (criação, sem recorrência).** `service_orders.insert` (status só vai se veio de uma coluna do Kanban), depois `service_order_assignees.insert` e **três RPCs em sequência**: `sync_service_order_service_types(p_service_order_id, p_service_type_ids)`,
`sync_service_order_scope_with_services(_service_order_id, _items, _confirm_response_deletion)` (equipamentos × checklists) e `sync_service_order_budget(p_service_order_id, p_items)` — as duas de serviço/orçamento gravam
`service_order_service_types` e `service_order_budget_items` (`hooks/useServiceOrders.ts:362-407`; `hooks/useServiceOrderBudget.ts:24-46`; assinaturas em `rec/fakebase/schema.json`, todas devolvem `json`). Toast: título "OS #N criada", descrição "Agendada para {data} às {hora}" ou "Sem data marcada"
(`:409-429`; `os.ts:71-79`). A Agenda, se estiver aberta, navega até o dia da OS (`Schedule.tsx:641-652, 746-760`). Com conflito e permissão explícita: RPC `schedule_create_service_order_with_override` (ou `..._plan_with_override`) com justificativa de ao menos 10 caracteres
(`useServiceOrders.ts:321-359`). Aviso "OS criada pela metade" se responsáveis ou equipamentos falharem (`os.ts:75-77`).

### 3.3 Detalhe da OS (`components/service-orders/ServiceOrderViewDialog.tsx`)
Abre ao clicar numa OS do Kanban/lista/Agenda (ou `?os=<id>`). Título "OS #N" (sem zeros) com a etiqueta de status ao lado (`:800-816`). Cartões: "Cliente" (com atalho do WhatsApp ao lado do telefone, 1.33.4), "Equipamento" (S/N), "Check-in / Check-out", "Fotos (N)",
respostas dos checklists por equipamento (Sim/Não/N/A, "Faixa esperada:", "Valor fora da faixa esperada."), "Conformidade PMOC", "Detalhes do Serviço" ("Diagnóstico", "Solução Aplicada", "Observações"), "Mão de Obra"/"Peças"/"Total" e
"Receita lançada: R$ …" (só com permissão financeira) (`:339-672`; `os.ts:338-401`). Rodapé com **ações em ícones** (`:678-795`): "Retomar" (pausada), "Pausar" (a caminho/em andamento), "Finalizar" (qualquer status menos concluída/cancelada), "Reabrir OS"/"Resetar OS",
"Editar", "Excluir", **"Link OS"** (copia o endereço público; vira "Copiado!") e "Faturar OS"; botão principal grande **"Preencher OS"** (ou "Relatório de Serviço" se concluída) que **navega na mesma aba** para `/os-tecnico/<id>` (T7). Cancelada não mostra o botão grande.

### 3.4 "Reabrir OS" / "Resetar OS" (`ResetServiceOrderDialog.tsx`)
Título "{Reabrir OS|Resetar OS} #N?" · "A OS voltará para Agendada e poderá ser marcada como A caminho e receber um novo check-in." · opções "Manter o preenchimento" (padrão) e "Apagar o preenchimento"
(com os textos "Preserva respostas, fotos, assinaturas e informações registradas na execução anterior." / "Remove respostas, fotos, assinaturas, medições e registros de localização desta execução.") · nota "Materiais, estoque, faturamento e dados administrativos da OS não serão alterados." · "Cancelar" e botão âmbar com o mesmo nome da ação (`:44-105`).
Textos fixos no componente (fora do i18n). Toast "OS resetada com sucesso!" + "A OS voltou para Agendada e o preenchimento anterior foi mantido/apagado." (`useServiceOrders.ts:776-788`). Por baixo: RPC `reset_service_order(_service_order_id, _clear_responses)` (`:766-775`).

### 3.5 Botão "Configurações" → "Configurações de OS" (`OsStatusManagerDialog.tsx`)
Janela só com: bloco "Novo status" ("Nome do status", seletor de cor nativo, botão "Criar"; Enter cria), e a lista dos status: bolinha de cor, nome, a chave (ex.: `em_andamento`) e menu "Editar"/"Excluir"; editando vira campo de nome + cor + "Salvar"/"Cancelar";
arrastar a linha reordena (HTML5 drag) (`:244-303`). Excluir confirma: "Excluir status" · "Tem certeza? OS com este status podem ser afetadas." (`:305-316`; `os.ts:404-416`). Toasts: "Status criado!", "Status atualizado!", "Status excluído!" (`hooks/useOsStatuses.ts:50-81`).
A chave do novo status nasce do nome sem acento (`:171-179`). Os 7 status de fábrica (Agendada `#8b5cf6`, Pendente `#f59e0b`, A Caminho `#6366f1`, Em Andamento `#3b82f6`, Concluída `#22c55e`, Pausada `#d97706`, Cancelada `#ef4444`)
vêm de função do banco (`supabase/migrations/20260606170000_catalog_tenant_isolation_hardening.sql:129-135`). Os hooks de prefixo/formato do número (`os_config`), SLA (`os_sla_config`) e campos obrigatórios (`os_required_fields`) estão no arquivo (`:32-137`) mas **nenhuma parte da janela os usa**.

### 3.6 "Faturar OS" (`components/service-orders/OsBillingDialog.tsx`)
Título "Faturar Ordem de Serviço" · "OS #N · Escolha como registrar o faturamento." · duas opções: **"Lançar receita"** ("Dinheiro que já entrou por este serviço.") e **"Gerar cobrança"** ("PIX, boleto ou link de pagamento pelo Asaas, com vencimento.") — esta **só aparece com o módulo `cobrancas` e conta Asaas ativa** (`:120-123, 246-269`; `finance.ts:1549-1573`).
Se já houver receita ou cobrança, mostra "Receita de {valor} já lançada…"/"Cobrança de {valor} vence em {data}." com "Ver lançamento"/"Ver cobrança". Leva ao formulário de recebimento (T13) ou ao `ChargeDialog` (T19). Valor sugerido = `total_value` da OS (`hooks/useOsBillingAction.ts:41-60`).
Fora de escopo detalhado aqui: o roteiro de T5 só aponta o botão.

### 3.7 Aba "Chamados" (`components/service-orders/PortalCallsPanel.tsx`)
Lista os pedidos que o cliente abriu pelos portais (origem `portal`): busca "Buscar por chamado, cliente, equipamento ou contrato...", filtro "Chamados abertos"/"Todos os chamados", origem "Todos os portais"/"Portal do Cliente"/"Portal do Contrato"; colunas "OS", "Cliente", "Descrição", "Origem", "Aberto em", "Status", "Ações"; ação "Abrir chamado" (abre o detalhe)
(`os.ts:21-42`). Vazio: "Nenhum chamado recebido" · "Os chamados abertos pelos portais aparecerão aqui." "Aberto" = origem portal e status fora dos encerrados (`lib/portalCalls.ts:11-15`). No seed não há OS: a aba aparece vazia.

### 3.8 Aba "Relatório" (`OsReportDashboard.tsx`)
Período no topo (padrão "Este mês"). KPIs "Total de OS", "Taxa de conclusão" ("{n} concluídas"), "Tempo médio", "Faturamento"; gráficos "OS por Status", "OS por Tipo de Serviço", "Volume de OS ao Longo do Tempo", "Faturamento ao Longo do Tempo", "OS por Dia da Semana"; rankings "Top 10 Clientes" e "Top Técnicos (Concluídas)"; quadro **"Saúde do agendamento"**
("Concluídas no prazo", "Concluídas após a data", "Abertas em atraso") (`os.ts:762-794`). Tudo calculado no navegador a partir de `useServiceOrders` (`:45-54`); sem OS no período mostra "Sem dados".

### 3.9 Aba "NPS e Satisfação" (`NpsDashboard.tsx` + `NpsSettingsModal.tsx`)
- Painel (período padrão "Este mês", `:69`): KPIs "NPS Score", "Média Geral", "Respostas", "Taxa de Resposta"; gráficos "Distribuição NPS" (Promotores 9-10 / Neutros 7-8 / Detratores 0-6), "Média por Categoria" (os critérios), "Tendência NPS" (por mês); "Ranking de Técnicos" ("Sem avaliações por técnico no período"),
  "Detratores em Aberto" ("Nenhum detrator em aberto no período.", selo "Atenção"), "Feed de Feedbacks" com filtros "Classificação" e "Técnico" (`os.ts:696-727`; `:64-120`). Botão **"Configurações"** abre a janela abaixo.
- **"Configurações de NPS"** (`NpsSettingsModal.tsx`): "Pergunta da escala 0–10"; "Avaliação por estrelas" (Opcional/Obrigatória); "Critérios de avaliação" (lista editável: "Adicionar", subir/descer, remover, "Inativo"); "Gerar pesquisa ao finalizar OS (padrão)" (Sim/Não); seção **"Avaliação no Google"**:
  "Link de avaliação do Google", "Quando convidar o cliente" ("Mostrar sempre" / "A partir de uma nota" + "Nota mínima (0 a 10)"), "Link do Google Maps" + "Gerar link de avaliação" e o guia "Como pegar o link?" (5 passos). Rodapé "Somente a gestão pode alterar estas configurações." para os demais. "Cancelar"/"Salvar" (`os.ts:660-759`).
- Quem **responde** a pesquisa é o cliente, na página pública da OS (T7, `components/technician/OSRatingSurvey.tsx:327`, RPC `submit_public_os_rating`). Ao concluir uma OS o sistema cria a linha de avaliação (`service_ratings.insert`, `hooks/useServiceOrders.ts:555-566`).

### 3.10 Agenda (`pages/Schedule.tsx`)
**Cabeçalho** (`components/schedule/ScheduleHeader.tsx`; `schedule.ts:13-47`): título "Agenda", subtítulo "Visualize e gerencie os agendamentos de ordens de serviço"; navegação anterior/próximo, **"Hoje"**; seletor **Dia · Semana · Mês** e **Calendário · Lista**; botão de busca ("Pesquisar"); botões **"OS Pausadas"** (com contagem) e **"Nova Tarefa/OS"**;
filtros (botão "Filtros") **Técnico**, **Cliente**, **Status** (só: Pendente, Em andamento, Pausada, Concluída, Cancelada) e **Tipo** (Ordem de Serviço × Tarefa) (`Schedule.tsx:925-985`). Computador abre em **Mês/Calendário** (`:133, 140`).
- **Mês/Semana/Dia**: cartões de evento coloridos pelo tipo de serviço (EventCard), selo "PMOC", "Retomada"; no Dia há "Resumo do Dia:" com a data; legenda **"Legenda:"** / botão "Legenda" ("Legenda, Tipos de Serviço", "Feriado", "Ver todos (N)"); feriados nacionais/estaduais/municipais calculados localmente e pintados no calendário
  (`utils/holidays`, `Schedule.tsx:227-250`; `schedule.ts:78-84, 89-91`). O calendário estica a faixa de horas para caber OS antes das 7h ou depois das 20h (1.37.28).
- **Lista**: `ScheduleListView` com seção "Atrasado" e vazio "Nada por aqui" / "Nenhuma tarefa ou OS neste período." (`schedule.ts:49-53`).
- **Criar**: botão "Nova Tarefa/OS", **duplo clique num dia** ou **clique num horário** → "O que deseja criar?" com "Ordem de Serviço" ("Atendimento técnico com cliente e equipamento") e "Tarefa" ("Atividade interna, reunião ou compromisso") (`Schedule.tsx:655-676`; `schedule.ts:96-102`). OS abre o mesmo formulário de 3.2 com data/hora pré-preenchidas.
- **Arrastar** um cartão para outro dia/horário reagenda: tarefa e OS sem responsável só atualizam a data; OS com técnico/equipe vai para a RPC de reserva (`schedule_book_service_order` ou `_plan`) e, se houver conflito, abre o aviso de conflito (3.11). Toast "OS reagendada com sucesso!" (`Schedule.tsx:678-733`; `useServiceOrders.ts:798-821`; `lib/scheduleBooking.ts:76-114`).
  No celular o arraste vira "Toque no horário para mover a OS" (`schedule.ts:85-88`).
- **Painel de resumo** (clique no cartão; lateral no computador): "Resumo da OS"/"Resumo da Tarefa", cliente, data/hora, "Responsáveis" (técnicos e equipe), "Descrição", atalhos "Abrir com Maps"/"Abrir com Waze", materiais consumidos, "Linha do tempo" (Iniciada em, Pausada em, Retomada em, Finalizada em), botão **"Preencher OS"** (ou "Relatório de Serviço"; **navega na mesma aba** para `/os-tecnico/<id>`),
  para tarefa **"Finalizar Tarefa"**/**"Reabrir Tarefa"**, e menu **"Ações"** (texto fixo): "Finalizar OS" (confirma: "…independentemente do preenchimento ou status atual."), "Reabrir OS"/"Resetar OS", "Pausar OS", "Retomar OS", "Faturar OS", "Editar", **"Copiar link de acompanhamento"** (vira "Link copiado!") e "Excluir" (`ScheduleDetailPanel.tsx:121-132, 245-265, 355-450`; `os.ts:1649-1702`).
  Cobranças de contrato aparecem na Agenda como lembretes ("Concluir Cobrança", "Reabrir Cobrança", "Excluir cobrança?") e usam RPC `resolve_billing_reminder`/`unresolve_billing_reminder` (`Schedule.tsx:487-520, 575-595`).
- **Visibilidade**: o técnico só vê as OS dele ou da equipe dele; tarefas só as próprias, exceto com "Gerenciar Tarefas"/"Ver Toda a Agenda" (`Schedule.tsx:263-293`).

### 3.11 Tarefa, OS pausadas, busca e conflito (Agenda)
- **"Nova Tarefa"** (`components/schedule/TaskFormDialog.tsx`): "Título da Tarefa *" (placeholder "Ex: Comprar materiais, Reunião com cliente..."), "Cliente (opcional)", "Tipo de Tarefa" (os tipos **ativos** do T4), "Responsáveis" (mesmo seletor), "Mostrar na agenda" (+ dica "Desligado, a tarefa continua na oportunidade, mas não aparece no calendário."), "Data", "Horário", "Duração (min)", "Descrição", "Recorrência" (inclui duração "Até uma data"/"Contínua"), "Cancelar"/"Criar Tarefa"
  (`os.ts:1442-1493`). Grava em `service_orders` com `entry_type='tarefa'` e `task_title` (`hooks/useTaskSubmit.ts:79-104`). Não aparece na tela de Ordens de Serviço.
- **"OS Pausadas"** (`PausedOrdersDialog.tsx`; `schedule.ts:62-77`): "Todas as ordens de serviço pausadas, independente da data."; busca "Buscar por nº OS, cliente ou endereço…"; cartão com "Agendada para:", "Pausada há {tempo}", "Ver detalhes" e **"Retomar agora"** (toast "OS retomada"/"OS #N voltou para a agenda."). Vazio: "Nenhuma OS pausada no momento."
  OS retomada em data posterior aparece também nos dias entre a retomada e hoje, com selo "Retomada" ("OS retomada, agendada originalmente para outra data") (`Schedule.tsx:310-347`).
- **"Buscar OS / Tarefa"** (`OsSearchDialog.tsx`): "Número da OS, cliente, descrição, técnico...", contadores "{n} resultado(s)", "Comece a digitar para buscar.", "Carregar mais ({n} restantes)" (10 por página) (`os.ts:1525-1538`).
- **Aviso de conflito** (`ScheduleConflictDialog.tsx`, textos fixos no componente): título "Conflito de agenda", texto "Já existe outro atendimento nesse horário para um dos responsáveis.", lista de até 3 conflitos ("OS #N · nomes · hora"; **a lista vem vazia** no caminho do arraste, porque o app transforma o erro do banco em `ScheduleConflictError` sem itens, `lib/scheduleBooking.ts:42-57`);
  para quem tem `fn:override_schedule_conflict`: campo "Justificativa obrigatória" (placeholder "Explique por que os atendimentos podem ficar no mesmo horário.", mínimo 10 caracteres), nota "A autorização e a justificativa serão registradas para auditoria." e botões "Voltar" · "Autorizar conflito" (desligado até 10 caracteres);
  sem a permissão: "Escolha outro horário ou outro responsável. Você não possui permissão para autorizar sobreposição." e só "Voltar" (`:20-100`; `Schedule.tsx:678-733, 774-809`). O conflito é decidido **no banco** (gatilho do motor de reservas, erro `public_api_schedule_conflict`, `supabase/migrations/20261017122000_public_api_v1_booking_engine.sql:162`); o backend falso não tem gatilhos, então o aviso só aparece se o handler da RPC o provocar.

### 3.12 Equipes (aba "Equipes" em Funcionários — `components/teams/TeamsPanel.tsx`, `TeamFormDialog.tsx`)
- Aba lateral "Equipes" (entre "PJ/MEI" e "Controle de Ponto") (`Employees.tsx:373-388`; `employees.ts:311-318`). Busca "Buscar equipe...", botão **"Nova Equipe"**; cartões com ícone/foto/cor, nome, selo "Ativa"/"Inativa", "N membros" ("Sem membros", "1 membro") e avatares; "Editar"/"Excluir". Vazio: "Nenhuma equipe cadastrada" · "Cadastre sua primeira equipe para organizar os técnicos." (`TeamsPanel.tsx:22-162`; `os.ts:1158-1191`).
- **Excluir** usa o `confirm()` **nativo do navegador** ("Tem certeza que deseja excluir esta equipe?", `TeamsPanel.tsx:49`), não uma janela do sistema; a gravação não captura esse diálogo. Excluir limpa `team_id` das OS e contratos e remove os membros (`hooks/useTeams.ts:178-181`).
- **"Nova Equipe"**/"Editar Equipe": "Nome *" (placeholder "Nome da equipe"), "Descrição", **"Visual da Equipe"** (botão "Foto" para enviar imagem, "Remover", seletor de cor nativo, grade de **ícones**), **"Membros"** (caixas de seleção com todos os colaboradores ativos; vazio "Nenhum usuário disponível"), "Cancelar"/"Criar Equipe" (ou "Salvar") (`TeamFormDialog.tsx:143-251`; `os.ts:1621-1636`). Foto vai para o bucket `team-photos` (`:101-103`).
  Não existe "líder da equipe": é lista plana (confirma a trilha).
- Pendência da trilha respondida: **sem o módulo RH a aba não existe** (a rota `/funcionarios` exige `rh`, `App.tsx:869`); ver 0.3.6.

### 3.13 Mapa e Rastreamento (`pages/LiveMap.tsx`, `components/tracking/TrackingHistoryTab.tsx`)
- Título "Mapa e Rastreamento" · "Posição em tempo real e histórico de deslocamentos"; abas **"Mapa ao Vivo"** e **"Histórico"** (`LiveMap.tsx:443-490`; `os.ts:1095-1099`).
- **Mapa ao Vivo**: botão "Atualizar", etiqueta "N técnico(s) ativo(s)" (texto fixo no componente, `:467, 500`), legenda "Executando OS", "A Caminho", "Check-out", "Destino cliente", "Base da empresa" (`os.ts:1103-1107`). Marcador do técnico com popup ("OS vinculada", "Última atualização: há N min", "Chegada em ~N min"), trilha da rota e linha até o **destino do cliente**; marcador "Base" no endereço da empresa.
  Técnicos vêm de `technician_locations` dos **últimos 120 min** (`hooks/useLiveTechnicianLocations.ts:63-72`); tipos de evento `check_in`, `check_out`, `en_route`, `tracking` (`LiveMap.tsx:128, TrackingHistoryTab.tsx:132-138`). A rota e o ETA vêm do OSRM; endereços sem coordenada são geocodificados (Nominatim) e a coordenada é gravada no cliente (`:126-180`; `utils/geolocation`).
  A base da empresa é geocodificada a partir do endereço em Configurações (`:206-230`).
- **Histórico** (`TrackingHistoryTab.tsx`): filtros "Técnico" ("Todos os técnicos") e "Data"; vazio "Selecione um técnico" · "Escolha um técnico e uma data para ver o histórico de deslocamentos."; estatísticas "Check-ins", "Check-outs", "Distância", "Tempo em campo"; lista de eventos com "Ver no mapa" (`os.ts:1122-1148`).
- Mapa: Leaflet + camada de vetores MapLibre (`lib/mapTiles.ts:13-30`), com `VITE_MAP_TILES_URL`; **sem WebGL** cai num fundo neutro (`:61-87`). O robô já serve tiles falsos de Niterói em `/__tiles` (`rec/env.json`).

---

## 4. Backend por tela × o que o backend falso (`rec/fakebase`) cobre hoje

Legenda da coluna "Fakebase hoje": **OK** = coberto pelo REST genérico (tabela existe em `schema.json`; seeds/handlers não são necessários para o app não quebrar); **SEED** = a tabela existe mas está vazia e a tela precisa de dados; **HANDLER** = RPC/função
sem handler (o falso devolve "vazio pelo tipo", sem efeito colateral); **NÃO** = nada cobre. Hoje existem só 3 handlers de RPC (`get_customer_portal_settings`, `get_lead_capture_form`, `save_customer_portal_settings`), 2 de função
(`cep-lookup`, `lead-capture-submit`) e 8 de host externo (`brasilapi.com.br`, `maps.google.com`, `nominatim.openstreetmap.org`, `router.project-osrm.org`, `servicodados.ibge.gov.br`, `unpkg.com`, `viacep.com.br`, `www.google.com`); hooks de tabela só para
`customers`, `equipment` e `lead_capture_forms` (`rec/fakebase/handlers/`, `hooks/`).

### 4.1 Ordens de Serviço (lista, Kanban, formulário, detalhe)
| Chamada | Onde | Fakebase hoje |
|---|---|---|
| `service_orders.select(*, customer:customers(...), equipment:equipment(...), form_template:form_templates(id,name), service_type:service_types!service_orders_service_type_id_fkey(...), contract:contracts(id,name,is_pmoc))` ordenado por `created_at`, paginado de 1000 em 1000 | `hooks/useServiceOrders.ts:200-211` | **SEED** (tabela vazia; o embed com dica de FK é suportado: `core/select.mjs:110`, `core/schema.mjs:46`). Sem `service_types` (T4) o cartão mostra o tipo vazio. |
| `service_order_assignees.select(service_order_id,user_id).in(...)` em blocos de 200 | `:230-240` | **SEED** (vazia) |
| `profiles.select(user_id, full_name, avatar_url, email)` dos criadores | `:262-265` | OK (7 perfis; os `created_by` das OS semeadas têm de ser `@id:user.*`) |
| `os_statuses.select().eq(company_id).order(position)`; insert/update/delete | `hooks/useOsStatuses.ts:27-81` | **SEED**. Sem linhas a tela cai nos 7 status "de reserva" **todos azuis** (`ServiceOrders.tsx:302-304`). Precisa das 7 linhas (cores na seção 3.5). |
| `os_config.select().limit(1).single()`, `os_sla_config.select(*, service_type:service_types(id,name))`, `os_required_fields.select()` | `OsStatusManagerDialog.tsx:37-44, 66-73, 106-113` — rodam **ao abrir a página**, pois a janela fica montada | **SEED** parcial: tabelas existem e vazias; `.single()` sem linha dá erro silencioso (sem tela). Semear 1 linha em `os_config` (`number_prefix:'OS'`, `number_format:'{prefix}-{year}-{number}'`, ver `supabase/migrations/20260228205056_3e270a52-c16f-4568-8e49-0f481c0f1baa.sql:29`) evita o ruído. |
| `service_orders.insert(...)` (criação), `.update` (edição e troca de status), `.delete` (+ limpeza manual de `service_order_equipment`, `form_responses`, `os_photos`, `service_ratings`, `inventory_movements`, `pmoc_schedules`) | `:362-367, 547-553, 705-750` | OK para gravar, **mas** sem hook de default: `status` nasce `agendada` (1º valor do enum; banco real: `pendente`), `order_number` nasce `0` (banco real: sequência) e `entry_type`/`origin` nascem `null` (real: `'os'`/`'manual'`) — `core/defaults.mjs:11-22, 59-69`; migrations `20260131190034_...sql` e `20260308151207_...sql:47`. Efeito visível: toast "OS #0 criada", código `OS-2026-0`, OS nova na coluna "Agendada". |
| RPC `sync_service_order_service_types(p_service_order_id, p_service_type_ids)` | `hooks/useServiceOrderBudget.ts:36-46` | **HANDLER** (grava `service_order_service_types`) |
| RPC `sync_service_order_scope_with_services(_service_order_id, _items, _confirm_response_deletion)` | `useServiceOrders.ts:349, 396, 663`; `ServiceOrderFormDialog.tsx:782, 931` | **HANDLER** (grava `service_order_equipment` + `service_order_equipment_service_types`). Sem ele a OS nasce **sem checklists/equipamentos** e o app do técnico (T7) abre vazio. |
| RPC `sync_service_order_budget(p_service_order_id, p_items)` | `useServiceOrderBudget.ts:24-34` | **HANDLER** (grava `service_order_budget_items`; `total_value` da OS também deveria ser atualizado pelo banco real — dúvida 7.4) |
| RPC `preview_service_order_scope_removal(_service_order_id, _items)` | edição que remove checklists (`ServiceOrderFormDialog.tsx` perto de `:1003`; `os.ts:276`) | **HANDLER** só se algum capítulo editar escopo; vazio ⇒ sem aviso |
| RPC `reset_service_order(_service_order_id, _clear_responses)` | `useServiceOrders.ts:766-775` | **HANDLER**: sem ele o toast diz "OS resetada com sucesso!" mas **nada muda** na OS. Deve: `status='agendada'`, limpar `started_at/paused_at/resumed_at/completed_at/check_*`, e se `_clear_responses` apagar `form_responses`/`os_photos`/assinaturas/`technician_locations` da OS. |
| RPCs `schedule_create_service_order_with_override` / `..._plan_with_override` | `useServiceOrders.ts:334-343` (conflito com justificativa) | **HANDLER** só se gravar o conflito; senão ficar fora do roteiro |
| RPC `os_billing_state(...)` e leituras `financial_transactions`, `tenant_charges` para os selos "Faturada" | `hooks/useOsBillingState.ts:43`, `hooks/useOsBillingFlags.ts:68, 87` | **HANDLER**/vazio: sem receita lançada não aparece selo; ok |
| `service_ratings.insert({service_order_id})` ao concluir (+ `snapshot_data` na OS, leitura de `profiles`, `service_order_assignees`, `contracts`) | `useServiceOrders.ts:555-640` | OK, mas `service_ratings.token` nasce `null` (sem default de token) — sem consequência nesta aula |
| `nps_settings.select()` (padrão do toggle de NPS) | `hooks/useNpsSettings.ts:51` | tabela existe e **vazia** (`seeds/00-vazias.json`); o hook usa padrão (`generate_on_finish: true`) — OK |
| `company_settings` (flags `os_finish_revenue_prompt_enabled`, `os_stock_consumption_enabled`) | `hooks/useOsFinishRevenuePrompt.ts:60-70` | OK (ambas **true** no seed) |
| `financial_transactions` (receita lançada na pergunta ao concluir / "Faturar OS") | `OsFinishRevenueDialog`, `OsBillingDialog` | OK (genérico); T13 cobre o formulário de recebimento |
| Hosts externos: CEP (`cep-lookup`, `viacep.com.br`, `brasilapi.com.br`), cidades (`servicodados.ibge.gov.br`), endereço/geocode (`nominatim.openstreetmap.org`) | `CepLookup`, `AddressAutocomplete`, `StateCitySelector`, `utils/geolocation.ts:127-128` | OK (mesmos handlers do T3) |
| Storage | nenhum nesta tela | — |

### 4.2 Aba Chamados, Relatório, NPS
| Chamada | Onde | Fakebase hoje |
|---|---|---|
| Aba Chamados: usa a mesma lista de OS (`origin='portal'`, `lib/portalCalls.ts:11-15`) | `PortalCallsPanel.tsx` | **SEED** (precisa de ao menos 1 OS com `origin:'portal'` se o capítulo mostrar a coluna do portal; senão fica vazia) |
| Relatório: só a lista de OS em memória | `OsReportDashboard.tsx:51` | **SEED** (OS com `scheduled_date` e `total_value` no mês corrente — `@now-Nd` — e `completed_at`/`started_at` para "Tempo médio" e "Saúde do agendamento") |
| NPS: `service_ratings.select(*, service_order:service_orders(id, order_number, scheduled_date, technician_id, customer:customers(id,name)))` | `hooks/useServiceRatings.ts:131-141` | **SEED** (precisa de linhas com `rated_at` dentro do período, `nps_score`, `quality_rating`…, `comment`, `rated_by_name`) |
| RPC `get_nps_technician_ranking(p_start,p_end)` → `{user_id, full_name, avatar_url, os_concluidas, respostas, taxa_resposta, nps_medio, media_estrelas}[]` | `hooks/useNpsRanking.ts:46` | **HANDLER** (sem ele devolve `[]` ⇒ "Sem avaliações por técnico no período") |
| RPC `get_nps_open_detractors(p_start,p_end)` → `{os_id, order_number, nps_score, comment, customer_name, rated_by_name, rated_at, technician_id, technician_name…}[]` | `useNpsRanking.ts:58` | **HANDLER** (sem ele ⇒ "Nenhum detrator em aberto no período.") |
| RPC `get_nps_criteria_averages(p_start,p_end)` → `{label, media, respostas}[]` e tabela `nps_criteria` (padrão de fábrica: Qualidade, Pontualidade, Profissionalismo) | `hooks/useNpsCriteria.ts:52-118` | **SEED** + **HANDLER** (`nps_criteria` vazia no seed) |
| Edge function `resolve-google-maps-link` (botão "Gerar link de avaliação") | `hooks/useResolveGoogleMapsLink.ts:28` | **HANDLER** (função sem handler devolve `{}` ⇒ erro "Não consegui identificar a empresa nesse link…" ou "Não foi possível gerar o link…"). Só necessário se o roteiro gerar o link. |
| `nps_settings.upsert/update` ao salvar "Configurações de NPS" | `useNpsSettings.ts:74` | OK (genérico) |

### 4.3 Agenda
| Chamada | Onde | Fakebase hoje |
|---|---|---|
| Mesma lista `service_orders` (OS e tarefas) + equipes (`teams`, `team_members`) + perfis | `Schedule.tsx`, `hooks/useTeams.ts:49-86` | **SEED** (`teams`/`team_members` estão em `seeds/00-vazias.json`) |
| RPC `schedule_book_service_order(p_service_order_id, p_starts_at, p_ends_at, p_resource_type, p_resource_id, p_override_justification)` e `schedule_book_service_order_plan(..., p_schedule_plan, ...)` — usados ao **arrastar** uma OS com responsável | `lib/scheduleBooking.ts:76-114`; `Schedule.tsx:703-733` | **HANDLER**: sem ele o toast "OS reagendada com sucesso!" aparece e **a OS não se move**. Deve atualizar `scheduled_date`, `scheduled_time`, `duration_minutes`, `schedule_plan`. Para o conflito: devolver erro de conflito no formato esperado por `isScheduleConflictError` (`lib/scheduleBooking.ts:117+`) — dúvida 7.5. |
| Arrastar tarefa / OS sem responsável | `Schedule.tsx:681-696` | OK (`service_orders.update`) |
| `service_orders.insert` com `entry_type='tarefa'`, `task_title`, `show_in_schedule` + `service_order_assignees.insert` | `hooks/useTaskSubmit.ts:79-111` | OK (mesmo cuidado de defaults da 4.1) |
| `task_types.select` (tipos ativos no formulário de tarefa) | `hooks/useTaskTypes.ts:36` | **SEED** (vem do T4) |
| `user_preferences.select/upsert` (modo Dia/Semana/Mês × Calendário/Lista por aparelho) | `hooks/useUserPreferences.ts:46, 78, 129` | OK (1 linha no seed; `upsert` genérico) — confirmar rodando (7.6) |
| `contracts.select` para lembretes de cobrança e RPC `resolve_billing_reminder`/`unresolve_billing_reminder` | `hooks/useFinancialScheduleEvents.ts:29`; `Schedule.tsx:580-590` | `contracts` vazio ⇒ sem lembretes (ok) |
| `service_orders` das pausadas | `hooks/usePausedOrders.ts:27` | **SEED** (pelo menos 1 OS `pausada` com `paused_at`) |
| Feriados | `utils/holidays.ts` (cálculo local, sem rede) | OK — depende de `company_settings.city/state` (Niterói/RJ no seed) |
| Links "Abrir com Maps/Waze" | `utils/geolocation.ts:33-37` | abrem outra página (não aparece na gravação) |

### 4.4 Equipes
| Chamada | Onde | Fakebase hoje |
|---|---|---|
| `teams.select`, `team_members.select`, insert/update/delete (limpa `service_orders.team_id`, `contracts.team_id`, `service_order_assignees`) | `hooks/useTeams.ts:49-181` | **SEED**/OK (tabelas existem, vazias; CRUD genérico serve) |
| `profiles` ativos (`useActiveCompanyProfiles`) para "Membros" | `TeamsPanel.tsx:26` | OK (7 perfis, todos `is_active:true`) |
| Storage bucket `team-photos` (`upload` + `getPublicUrl`) | `TeamFormDialog.tsx:101-103` | OK (bucket conhecido do falso; imagem ausente vira placeholder) — o `upload` do robô precisa de arquivo de teste genérico |
| `confirm()` nativo ao excluir equipe | `TeamsPanel.tsx:49` | não aparece em vídeo (diálogo do navegador) |
| `useModuleAccess('rh')` | `App.tsx:869` | OK (módulo `rh` ligado) |

### 4.5 Mapa e Rastreamento
| Chamada | Onde | Fakebase hoje |
|---|---|---|
| `profiles.select(user_id, full_name)` + `technician_locations.select(*).gte(created_at, agora-2h).order(created_at desc).limit(1000)` | `hooks/useLiveTechnicianLocations.ts:63-72` | **SEED** (tabela existe, sem linhas; usar `@now-5m`, `@now-12m`…; colunas `user_id`, `service_order_id`, `event_type` ∈ `check_in|check_out|en_route|tracking`, `lat`, `lng`, `address`) |
| Canal em tempo real `live-tech-locations-<company>` | `:126-141` | **stub** (não entrega eventos): posição só da carga inicial/botão "Atualizar" |
| `service_orders.select(id, customer_id).in(...)`, `customers.select(id, lat, lng, address…)` e `customers.update({lat,lng})` | `LiveMap.tsx:133-170` | OK; garantir `lat`/`lng` nos clientes do seed para o destino (senão geocodifica via Nominatim e grava) |
| OSRM `router.project-osrm.org/route/v1/driving/...` (rota + ETA) e Nominatim (`geocodeAddress`) | `utils/geolocation.ts:127-156` | OK (handlers existem; conferir que devolvem rota sobre os tiles de Niterói) |
| Tiles do mapa | `lib/mapTiles.ts:30-87`, `rec/env.json` | OK (`/__tiles`, mapa falso de Niterói); **WebGL em Chromium headless** é a dúvida 7.2 |
| Histórico: `technician_locations.select(*)` por técnico e dia (+ `profiles`) | `TrackingHistoryTab.tsx:55, 68` | **SEED** (eventos do dia escolhido) |

### 4.6 Sementes que o T5 precisa (resumo)
`os_statuses` (7) · `os_config` (1) · `nps_settings`/`nps_criteria` (3 critérios) · `service_orders` (≈ 12 a 16, ver plano) com `order_number`, `public_short_code`, `created_by`, `customer_id`, `service_type_id`,
`scheduled_date/time`, `schedule_plan`, `status` · `service_order_assignees` · `service_order_service_types` · `service_order_equipment` (+ `_service_types`) · `service_ratings` (≥ 8, respondidas) · `technician_locations` (relativas ao agora)
· `teams`/`team_members` (a aula cria 1 ao vivo; 1 já pode existir) · estado do T4 (`service_types`, `service_type_categories`, `task_types`, `form_templates`, `form_questions`, `form_template_service_types`).
Nada disso existe em `rec/fakebase/seeds/` hoje (só `companies`, `company_settings`, `subscription_plans`, `company_modules`, `tenant_payment_accounts`, `profiles`, `user_roles`, `user_preferences`, cadastros do T3 e `receita`).
