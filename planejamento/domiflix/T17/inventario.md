# Inventário funcional · T17 — Dashboard, relatórios e exportações (Dominex)

> Base para o roteiro do tutorial "T17 · Dashboard, relatórios e exportações", o último da trilha. Levantado em 31/10/2026 contra
> o código publicado `APP_VERSION = "1.38.6"` (`src/config/version.ts:1`), cópia em `/home/claude/domiflix/src-1.38.6`.
> **Análise estática, somente leitura.** "(a confirmar)" = só rodando. Formato do inventário do T3/T14.
> Os relatórios de cada área já têm inventário próprio: OS e NPS (`T05/inventario.md` 3.8 e 3.9), Estoque (`T08/inventario.md`
> 3.7, 3.11 a 3.13), Financeiro e DRE (`T13`, `T20`), Ponto (`T15/inventario.md` 3.9), "Exportar meus dados"
> (`T01/inventario.md` 3.11). Aqui fica o Dashboard em detalhe e o **mapa** de onde está cada relatório e cada exportação.

## Como ler

- Caminhos relativos a `src/`, exceto `supabase/...`, `docs/...` e `rec/...`. Formato `arquivo:linha`.
- Rótulos entre aspas = texto exato (pt-br). **dash** = `lib/i18n/messages/app/dashboard.ts` (bloco pt-br `:9-105`);
  **comum** = `lib/i18n/messages/app/common.ts`.
- Tudo no Dashboard é calculado **no navegador** a partir de seis leituras (`hooks/useDashboardStats.ts:9-91`): não há RPC de
  indicador. Os números saem, então, das sementes do mundo fictício, aula a aula.
- O robô grava com o navegador no fuso **America/Sao_Paulo** e o relógio congelado em `FAKE_NOW`
  (`rec/recorder/browser.mjs:22,178,189`). Isso importa para a pegadinha P2.

---

## 0. Resumo para o roteiro

### 0.1 Capítulos da trilha (v1.22.5, `_referencia/trilha-de-tutoriais_v1.22.5.md:719-743`) contra o código de hoje

| # | Item da trilha | Situação | O que ajustar |
|---|---|---|---|
| 1 | KPIs: OS abertas, pendentes, técnicos em campo, taxa de conclusão, faturamento, clientes ativos | **Mudou** | São **três cartões**: **"OS Abertas"** ("{n} pendentes"), **"Taxa de Conclusão"** ("{n} concluídas este mês"), **"Faturamento"** ("no período selecionado"), com seta de variação no primeiro e no terceiro (`components/dashboard/DashboardKPIs.tsx:49-81`; dash `:17-24`). "Técnicos em campo" virou rodapé de "Desempenho da Equipe"; "Clientes Ativos" e "Em Campo Agora" saíram na 1.5.9 (`pages/Changelog.tsx:11436`). |
| 2 | Mapa ao vivo, fluxo de caixa e evolução de OS | **Bate** | **"Equipe em Campo"** ("Ao vivo"), **"Fluxo de Caixa"** ("Entradas", "Saídas", "Saldo:"), **"Evolução de OS"** ("Diário", "Semanal", "Mensal"; "Total" e "Concluídas") (dash `:25-42,83-89`; `pages/Dashboard.tsx:376-391`). |
| 3 | Top Técnicos, status, OS por tipo e OS críticas | **Bate, com nomes novos** | **"Desempenho da Equipe"**, **"OS por Status"**, **"OS por Tipo de Serviço"**, **"Requer Atenção"** (dash `:43-82`); e o bloco **"Chamados abertos"** do portal (dash `:90-98`). |
| 4 | Filtros de período e a origem de cada indicador | **Bate** | Filtro no topo: "Todos os tempos", "Hoje", "Últimos 7 dias", **"Este mês"** (padrão), "Mês passado", "Últimos 30 dias", "Este ano", "Personalizado" (`components/ui/DateRangeFilter.tsx:130-141`; comum `:46-59`). Cada cartão e cada linha de status abre a tela de origem (seções 3.2 e 3.4). "Todos os tempos" mostra o mês atual (P1). |
| 5 | Relatórios de **OS e NPS** | **Bate** | Ordens de Serviço › abas **"Relatório"** e **"NPS e Satisfação"** (`T05/inventario.md:232-240`; rótulos em `lib/i18n/messages/app/os.ts:697-718,763-788`). Nenhuma das duas tem botão de exportar. |
| 6 | Onde fica cada família de relatório; quando voltar ao T20 | **Bate** | Mapa na seção 3.7. O Financeiro tem tela própria **"Relatórios"** (`components/layout/SidebarMenuContent.tsx:181`). |
| 7 | Estoque: posição, inventário e contagem | **Bate** | Estoque › "Inventários", "Posição de Estoque", "Relatório" (`T08/inventario.md:485-590`). |
| 8 | Pessoas e comercial: ponto e **atividade** | **Parcial** | Ponto: Funcionários › "Controle de Ponto" › "Histórico" (CSV) e "Relatório" (`T15/inventario.md` 3.9). **Atividade comercial** é do painel da Dominex, não do cliente (P21). |
| 9 | Exportações em **PDF, Excel e CSV** e **Exportar meus dados** | **Bate** | Contas a Pagar/Receber e Movimentações: "Exportar" → "Excel", "PDF", "CSV" (`components/financial/FinanceContas.tsx:1113-1124`; `components/financial/TransactionListPanel.tsx:919-930`); DRE, DFC, Estoque, Ponto (seção 3.8); "Exportar meus dados" em Configurações › Empresa (`pages/Settings.tsx:1624-1630`). |

Abertura, recapitulação e próximo da trilha (`trilha...v1.22.5.md:737-739`) continuam válidos: "Neste último tutorial você vai
aprender a ler o dashboard, encontrar cada relatório e levar os dados para PDF, Excel ou CSV."; "Fim da trilha. Volte em qualquer
tutorial pelo capítulo que precisar."

Avisos da trilha (`:741-743`):

- ⚠️ "Faturamento e fluxo de caixa excluem movimento interno" → **bate**: corte por `transfer_pair_id` (transferência entre contas e
  pagamento de fatura) (`pages/Dashboard.tsx:106-116,165-168`; a coluna vem de `hooks/useDashboardStats.ts:47-58`).
- ⚠️ "O mapa só plota técnico que já mandou o primeiro ponto de GPS" → **bate** (`pages/Dashboard.tsx:296-332`: "sem GPS ao vivo
  ainda → não plota").
- ⚠️ "Antes de exportar, aplique os filtros de período" → **bate**: o export de Contas e de Movimentações usa a lista filtrada da
  tela (`FinanceContas.tsx:956-957`; `TransactionListPanel.tsx:733,741`); o DRE carimba o regime (`T20/inventario.md:45`).

### 0.2 O que mudou desde a 1.22.5 (`pages/Changelog.tsx`)

| Versão | Mudança | Linhas |
|---|---|---|
| 1.22.3 | Transferência entre contas não conta mais como faturamento | `:4683-4684` |
| 1.24.9 | Botão "Exportar meus dados" na aba Empresa | `:4311` |
| 1.28.0 | Relatório de OS mais completo (evolução, conclusão, faturamento, tipos, dias, saúde dos agendamentos) | `:2685-2686` |
| 1.28.2 | Nova visão geral dos relatórios financeiros | `:2631` |
| 1.35.8 | Chamados do portal em área própria; o aviso do painel leva ao chamado | `:1649` |
| 1.36.20 | Aba "Análise" nos relatórios do financeiro | `:1266-1277` |
| 1.37.40 | "Financeiro virou um dashboard de verdade" (Visão Geral do Financeiro) | `:421` |

Antes da 1.22.5 e ainda valendo: 1.5.9 tirou "Clientes Ativos" e "Em Campo Agora" (`:11436`); 1.17.8 criou "Chamados abertos no
painel inicial" (`:6116`).

### 0.3 O que mais pode surpreender (detalhes na seção 5)

1. "Todos os tempos" no Dashboard mostra só o mês atual (P1).
2. **Fuso:** data sem hora vira o dia anterior no Brasil. OS aberta de hoje aparece em "Requer Atenção" como "Atrasada 0 dias";
   "Evolução de OS" e "Fluxo de Caixa" deslocam um dia (P2). O robô grava no fuso de São Paulo, então aparece no vídeo.
3. "Evolução de OS" ordena os rótulos em ordem alfabética: período que cruza meses sai fora de ordem (P3).
4. OS sem data agendada não entram em "OS Abertas" nem nos gráficos: o chamado pendente da Mariana Lopes fica de fora (P4).
5. "Faturamento" soma toda entrada paga, inclusive aporte e empréstimo, pela data do lançamento (P8).
6. Quem tem só a tela Dashboard vê faturamento e caixa: "Ver Totais Financeiros" não é conferida (P20, segurança).
7. Toda exportação baixa arquivo ou abre nova aba: no vídeo, os menus e o aviso de conclusão (P18).

### 0.4 Guia Técnico T17 (`docs/guia-tecnico/secoes/T17.html`) contra o código

O Guia T17 se chama "Dashboard, rotina e truques" (KPIs, mapa, blocos, chamados, atalhos, rotinas diária/semanal/mensal,
Novidades e ajuda). Ele descreve bem o Dashboard de hoje; as diferenças:

| O Guia diz | O código faz |
|---|---|
| Cap. 3: "O botão do rodapé é Ver todas as OS críticas." | No computador o botão é "Ver todas as OS" e só aparece com mais de 5 atrasadas (`components/dashboard/DashboardCriticalOS.tsx:118-124`); "Ver todas as OS críticas" é o do celular (`:76-79`). |
| FAQ: a taxa "compara as concluídas com o total que teve desfecho no período" | Conta concluídas ÷ (abertas + concluídas), canceladas fora (`pages/Dashboard.tsx:91-95`). |
| Suporte: "Meu Dashboard está vazio → Troque o filtro pra Todos os tempos" | "Todos os tempos" volta ao mês atual (P1): o conselho não muda nada. |
| Cap. 2: "O botão Abrir Mapa ao Vivo leva pra tela completa" | O botão só existe no estado vazio; com técnico em campo aparece a fileira de fotos (`components/dashboard/DashboardLiveMap.tsx:216-252`). |
| Cap. 8: "Vá em Financeiro › Visão Geral e abra a aba de DRE" | O DRE fica em Financeiro › "Relatórios" › "DRE - Resultado" (`SidebarMenuContent.tsx:181`; `/financeiro/dre` redireciona para `?tab=dre`, `App.tsx:850`). |
| Cap. 9: "No rodapé de qualquer tela aparece Dominex v1.22.5" | Aparece a versão em uso (1.38.6, `src/config/version.ts:1`). |
| Cap. 5: atalhos "Shift + D" etc. | Bate: "Shift + D" leva ao Dashboard (`hooks/useKeyboardShortcuts.ts:17`). Os atalhos são do T1. |

Handoff para quem mantém o Guia (não muda o vídeo).

### 0.5 O que a empresa ganha ao nascer (cadastro) e toca o Dashboard

Conferido nas duas portas de cadastro (`supabase/functions/self-register/index.ts`, `supabase/functions/create-company/index.ts`),
no RPC `seed_company_catalog` e nos gatilhos `AFTER INSERT ON companies`:

- **Dashboard sem configuração:** os blocos são fixos (`pages/Dashboard.tsx:372-408`); não há tabela de widgets nem de layout do
  painel nas migrations. Nada a semear.
- **Tipos de serviço:** "Manutenção Preventiva", "Visita Técnica" e "Higienização"
  (`supabase/migrations/20260718120000_seed_company_catalog_i18n.sql:33-95`, chamado em `self-register/index.ts:1042` e
  `create-company/index.ts:547`). São os nomes de "OS por Tipo de Serviço", com os que o T4 criou.
- **Status:** o Dashboard usa os seis status fixos (`pages/Dashboard.tsx:84`; dash `:56-66`), não os `os_statuses` da empresa
  (semeados no mesmo RPC, `:97`).
- **Categorias financeiras:** 14 padrão (`self-register/index.ts:999-1012`; `create-company/index.ts:504-517`) e 14 de sistema pelo
  gatilho `seed_system_financial_categories`
  (`supabase/migrations/20261020223000_profit_distribution_and_investment_outside_dre.sql:18-47`; gatilho em
  `20260904100000_cartao_fatura_higiene_schema.sql:92-96`), entre elas as entradas "Aporte de sócios", "Resgate de aplicação",
  "Venda de ativos" e "Empréstimos recebidos" (P8).
- **Contas:** "Caixa" e "Conta Principal" (`self-register/index.ts:1033-1038`; `create-company/index.ts:538-542`).
- **Endereço da empresa** (`company_settings`, linha criada pelo gatilho
  `20260612150000_company_settings_backfill_e_trigger.sql:100-102`): centraliza o mapa quando não há ninguém em campo
  (`DashboardLiveMap.tsx:51-69`).

---

## 1. Rotas e navegação

| Tela | Caminho | URL | Componente |
|---|---|---|---|
| Dashboard | menu "Dashboard" (primeiro item, `components/layout/SidebarMenuContent.tsx:97`); também no Menu Superior e na gaveta "Mais" do celular (`components/layout/TopNavbar.tsx:87`; `components/layout/MoreMenuDrawer.tsx:83`); atalho "Shift + D" | `/dashboard` (`App.tsx:789`) | `pages/Dashboard.tsx` |
| Destinos dos cartões | "OS Abertas" e "Taxa de Conclusão" → `/ordens-servico`; "Faturamento" → `/financeiro`, que redireciona a `/financeiro/relatorio` (Visão Geral) | `DashboardKPIs.tsx:58,68,79`; `App.tsx:840-842` | — |
| Destinos dos blocos | "OS por Status" → Ordens de Serviço já no status (`DashboardStatusSummary.tsx:51`); "Chamados abertos" → `/ordens-servico?aba=chamados` (`lib/portalCalls.ts:23-27`); "Abrir Mapa ao Vivo" → `/mapa-ao-vivo` (`DashboardLiveMap.tsx:232`) | — | — |
| Relatório e NPS de OS | Operacional › "Ordens de Serviço" › abas "Relatório", "NPS e Satisfação" | `/ordens-servico` (sem `?aba=`, `T05/inventario.md:82`) | `components/service-orders/OsReportDashboard.tsx`, `NpsDashboard.tsx` |
| Visão Geral do Financeiro | Financeiro › "Visão Geral" | `/financeiro/relatorio` (`SidebarMenuContent.tsx:177`) | `pages/Finance` (`App.tsx:843`) |
| Relatórios financeiros | Financeiro › **"Relatórios"** | `/financeiro/relatorios?tab=visao-geral|dre|dfc|contabilidade|analise` (`App.tsx:847`; `T20/inventario.md:80`) | `components/financial/*` |
| Movimentações | Financeiro › "Movimentações Financeiras" | `/financeiro/movimentacoes` (`SidebarMenuContent.tsx:178`) | `TransactionListPanel.tsx` |
| Contas a Pagar/Receber | Financeiro › "Contas a Pagar/Receber" | `/financeiro/contas` (`SidebarMenuContent.tsx:179`) | `FinanceContas.tsx` |
| Estoque | Gestão › "Estoque" › abas "Inventários", "Posição de Estoque", "Relatório" | `/estoque` | `pages/Inventory.tsx` (`T08/inventario.md:145-148`) |
| Ponto | Gestão › "Funcionários" › "Controle de Ponto" › "Histórico" / "Relatório" | `/funcionarios` | `components/time-tracking/*` (`T15/inventario.md` 3.9) |
| Loja (PDV, se contratado) | PDV › "Relatórios da Loja" | `/pdv/relatorios` (`App.tsx:836`; `SidebarMenuContent.tsx:153`) | `pages/PdvReports.tsx` |
| Exportar meus dados | Configurações › "Empresa", no fim da página, antes da "Zona de Perigo" | `/configuracoes` (seção `empresa`, `pages/Settings.tsx:760,1624-1640`) | `components/settings/DataExportCard.tsx`, `DataExportDialog.tsx` |

## 2. Permissões e módulos

| O quê | Regra | Onde |
|---|---|---|
| Dashboard | permissão "Dashboard" (`screen:dashboard`, "Painel inicial com os indicadores e atalhos do dia a dia."); módulo básico, sempre ligado | `hooks/usePermissions.ts:56`; `hooks/useCompanyModules.ts:47`; `App.tsx:789` |
| Valores financeiros no Dashboard | **nenhuma checagem** além da tela (P20) | `DashboardKPIs.tsx:70-79`; `components/dashboard/DashboardCashFlow.tsx` |
| "Ver Totais Financeiros" (`fn:view_finance_totals`, "Visualizar saldos, totais e projeções") | só nas regras das contas bancárias; nenhuma tela confere | `usePermissions.ts:112`; `supabase/migrations/20261019170000_split_bank_account_permissions.sql:122-168` |
| Relatórios financeiros, Contas, Movimentações | tela "Financeiro" (`screen:finance`) | `App.tsx:843-848` |
| Exportar meus dados | admin **ou** "Exportar Dados da Empresa" (`fn:export_company_data`, "Baixar em planilha todos os dados da empresa, incluindo financeiro e salários dos funcionários") com registro em `user_permissions` | `pages/Settings.tsx:121-127`; `usePermissions.ts:123` |
| Ponto | aba "Controle de Ponto" (admin/gestor, "Gerenciar Ponto" ou "Gerenciar Funcionários") + módulo `rh` | `T15/inventario.md` 2 |
| Relatórios da Loja | módulo `pdv` + `screen:pdv_reports` | `App.tsx:836` |

O Dashboard não tem módulo pago (o Guia diz o mesmo: "Módulo: nenhum. O Dashboard é base."). Sem a tela Dashboard, o item some
do menu e o usuário entra na primeira tela liberada (Guia T17, "Quem enxerga").

---

## 3. Por tela

### 3.1 Cabeçalho e avisos (`pages/Dashboard.tsx:336-370`)

- **"Olá, {primeiro nome}! 👋"** e a frase pela **hora do aparelho**: "Bom dia. Aqui está o resumo da sua operação." (5h–12h),
  "Boa tarde. Veja como está o dia." (12h–18h), "Boa noite. Resumo do dia de hoje." (`:33-38,348-351`; dash `:10-16`).
- Filtro de período à direita (no celular, abaixo do título) (`:352-370`).
- Acima do cabeçalho: avisos publicados pela Dominex (`SystemNoticeBanners scope="dashboard"`, `:341`; tabelas `admin_notices` e
  `admin_notice_dismissals`, `hooks/useSystemNotices.ts:36,55,79`) e o aviso de chamados **"Você tem {n} chamado de cliente
  aguardando"** / **"Você tem {n} chamados de cliente aguardando"** com **"Ver chamados"** e **"Depois"** (`:343-347`; dash `:99-104`).
- O aviso de chamados aparece quando há chamado do portal criado depois da última marca "visto", guardada no navegador por
  usuário (`dominex:portal-tickets-seen:<id do usuário>`) (`components/dashboard/PortalCallsAlert.tsx:35-52,152-167`). "Depois"
  grava a marca; "Ver chamados" grava e abre `/ordens-servico?aba=chamados` (`:172-182`).

### 3.2 Cartões do topo (`DashboardKPIs.tsx:49-103`; cálculo `pages/Dashboard.tsx:89-138`)

| Cartão | Conta | Linha de apoio | Seta | Clique |
|---|---|---|---|---|
| "OS Abertas" | OS do período (por data agendada) em pendente, agendada, a caminho, em andamento | "{n} pendentes" | variação contra o período anterior de mesmo tamanho (P7) | Ordens de Serviço |
| "Taxa de Conclusão" | concluídas ÷ (abertas + concluídas), em % | "{n} concluídas este mês" (P5) | — | Ordens de Serviço |
| "Faturamento" | entradas **pagas** com data do lançamento no período, menos as de `transfer_pair_id`; o número sobe em animação | "no período selecionado" | variação | Financeiro (Visão Geral) |

- A seta só aparece com variação diferente de zero: "↗ {n}%" ou "↘ {n}%" (`components/dashboard/KPICard.tsx:78-81`). Sem
  movimento no período anterior, a variação fica 0 e a seta some (`pages/Dashboard.tsx:124-125`).
- No celular, os três viram carrossel que se arrasta para o lado (`DashboardKPIs.tsx:83-97`).

### 3.3 Coluna da esquerda (computador)

- **"Equipe em Campo"** — selo "Ao vivo". Entra o técnico com OS **a caminho ou em andamento agendada para hoje** e com posição
  GPS recebida (carga das posições das **últimas 2 horas** + canal ao vivo compartilhado com o Mapa ao Vivo)
  (`pages/Dashboard.tsx:296-332`; `hooks/useLiveTechnicianLocations.ts:62-72`). Com técnico: marcadores no mapa (janela com nome
  e cliente) e uma fileira de fotos com o primeiro nome (`DashboardLiveMap.tsx:79-82,241-252`). Sem ninguém: o mapa continua,
  centrado na cidade da empresa, com o cartão **"Nenhum técnico em campo agora"** e **"Abrir Mapa ao Vivo"** (`:51-69,216-240`).
- **"Fluxo de Caixa"**: linhas "Entradas" e "Saídas"; resumo "Entradas:", "Saídas:", "Saldo:" (`DashboardCashFlow.tsx:138-148`).
  Segue o período, mas **termina hoje** (o "Este ano" não desenha meses futuros zerados); até 31 dias agrupa por dia ("dd/MM"),
  acima por mês ("nov/26"); exclui transferências; vazio "Sem dados para exibir" (`pages/Dashboard.tsx:140-182`;
  `DashboardCashFlow.tsx:154`; dash `:25-33`).
- **"Evolução de OS"**: botões "Diário" / "Semanal" / "Mensal" (abre em **"Mensal"**, `DashboardOSEvolution.tsx:26,42`), áreas
  "Total" e "Concluídas" com pontos (`:63-93`); a semana aparece como "S{dd/MM}" do início da semana (`pages/Dashboard.tsx:203-207`);
  vazio "Sem dados no período" (dash `:34-42`). Ver P2 e P3.
- **"Desempenho da Equipe"**: técnicos com OS concluída no período, do que mais concluiu ao que menos, até 5, com medalhas 🥇🥈🥉
  nos três primeiros (`DashboardTopTechnicians.tsx:20,88-110`; `pages/Dashboard.tsx:238-276`). No computador cada linha mostra
  "{n} concluídas", a nota média (estrelas das avaliações) e "{tempo} médio" (check-in a check-out, descartando acima de 24 h;
  formato "45min" ou "1h23", `DashboardTopTechnicians.tsx:22-27`). Rodapé: "{n} técnico em campo" / "{n} técnicos em campo" (OS de
  hoje a caminho/em andamento, `pages/Dashboard.tsx:97-104`) e **"Ver relatório"** (P9) (`DashboardTopTechnicians.tsx:117-131`);
  vazio "Nenhum técnico com OS concluída no período" (`:137`; dash `:67-77`).

### 3.4 Coluna da direita (computador)

- **"OS por Status"**: "Pendente", "Agendada", "A Caminho", "Em Andamento", "Concluída", "Cancelada" com quantidade e porcentagem
  do período; "Cancelada" some quando é zero; clicar abre Ordens de Serviço já filtrada naquele status
  (`components/dashboard/DashboardStatusSummary.tsx:45-51`; dash `:56-66`).
- **"OS por Tipo de Serviço"**: rosca com o total no centro ("total") e a lista de tipos com porcentagem, do mais frequente ao
  menos; o nome é o do tipo de serviço ou, em OS antiga, o tipo da OS (`components/dashboard/DashboardOSByType.tsx:39-91`;
  `pages/Dashboard.tsx:278-294`); vazio "Sem OS no período" (dash `:78-82`).
- **"Requer Atenção"**: OS com data **anterior a hoje** e não concluída nem cancelada, **sem olhar o período**, da mais atrasada à
  menos, até 5 (`pages/Dashboard.tsx:210-236`). No computador: número, tipo, cliente, cidade, **"Atrasada {n} dia"** /
  **"Atrasada {n} dias"** e, sem técnico, **"Atribuir técnico"** (P9); **"Ver todas as OS"** só com mais de 5
  (`DashboardCriticalOS.tsx:28-29,85-124`). No celular: "Atrasada {n}d · sem técnico" e "Ver todas as OS críticas" (`:51-79`).
  Tudo em dia: **"Tudo em dia!"** — "Nenhuma OS requer atenção imediata" (`:133-134`; dash `:43-55`).
- **"Chamados abertos"**: OS com origem no portal e status diferente de concluída/cancelada (`lib/portalCalls.ts:3,14`;
  `hooks/useDashboardStats.ts:35-38`), também **sem olhar o período**: cliente, descrição ("Sem descrição"), status e "há {tempo}";
  até 5; clicar na linha abre o chamado; **"Ver todos os chamados"** abre a aba "Chamados" das OS; vazio "Nenhum chamado aberto" —
  "Chamados recebidos pelo portal aparecem aqui" (`components/dashboard/DashboardPortalCalls.tsx:60-97,130-228`; dash `:90-98`).

### 3.5 Filtro de período (`components/ui/DateRangeFilter.tsx`)

- Botão com o nome do período; lista "Todos os tempos", "Hoje", "Últimos 7 dias", "Este mês", "Mês passado", "Últimos 30 dias",
  "Este ano", "Personalizado" (`:130-141`; comum `:46-54`).
- "Personalizado" abre **"Selecionar datas"** → "Selecione o período", calendário com **"Início"** e **"Fim"** e **"Aplicar"**
  (`:159,200-310,335-342`; comum `:44,55-58`). No celular vira gaveta (`:200-205`).
- Os cortes de período seguem o **fuso da empresa** (`:48-61`). O Dashboard recarrega sozinho a cada 30 s
  (`hooks/useDashboardStats.ts:89`). As setas comparam com o período anterior de mesmo tamanho (`pages/Dashboard.tsx:66-69`).
- A escolha não fica salva: ao voltar ao Dashboard, abre em "Este mês" (`useDateRangeFilter('this_month')`, `pages/Dashboard.tsx:61`;
  o filtro não usa `localStorage`).

### 3.6 No celular (`pages/Dashboard.tsx:376-408`)

Uma coluna só, nesta ordem: "Equipe em Campo", "OS por Status", "OS por Tipo de Serviço", "Fluxo de Caixa", "Evolução de OS",
"Desempenho da Equipe", "Requer Atenção", "Chamados abertos" (classes `order-1` a `order-8`). A aula é gravada no computador (plano).

### 3.7 Mapa dos relatórios (onde fica cada família)

| Família | Onde | O que tem | Exporta | Fonte |
|---|---|---|---|---|
| Operação (OS) | Ordens de Serviço › "Relatório" | "Total de OS", "Taxa de conclusão", "Tempo médio", "Faturamento"; "Volume de OS ao Longo do Tempo", "Faturamento ao Longo do Tempo", "OS por Dia da Semana"; "Top 10 Clientes", "Top Técnicos (Concluídas)"; "Saúde do agendamento" | — | `T05/inventario.md:232-234`; `os.ts:763-788` |
| Satisfação | Ordens de Serviço › "NPS e Satisfação" | "NPS Score", "Média Geral", "Respostas", "Taxa de Resposta", "Distribuição NPS", "Ranking de Técnicos", "Detratores em Aberto", "Feed de Feedbacks" | — | `T05/inventario.md:236-240`; `os.ts:697-718` |
| Financeiro (painel) | Financeiro › "Visão Geral" | o painel do Financeiro (1.37.40) | — | `T13`, `T20` |
| Financeiro (relatórios) | Financeiro › "Relatórios": "Visão Geral", "DRE - Resultado", "DFC - Fluxo de Caixa", "Contabilidade", "Análise" | resultado, DRE, fluxo realizado, pacote contábil, comparação de períodos | DRE "Excel"/"PDF"; DFC "Excel"/"PDF"/"CSV"; "Exportar pacote" (Excel multiabas) | `T20/inventario.md:25-35,80,169-176` |
| Lançamentos | Financeiro › "Movimentações Financeiras" e "Contas a Pagar/Receber" | listas com filtros; "Lista"/"Calendário" em Contas | **"Exportar"** → "PDF", "Excel", "CSV" / "Excel", "PDF", "CSV" | `TransactionListPanel.tsx:919-930`; `FinanceContas.tsx:1113-1124` |
| Estoque | Estoque › lista, "Inventários", "Posição de Estoque", "Relatório" | posição por local numa data, contagens, compras e média paga | "Exportar" → "PDF"/"Excel" em todas | `T08/inventario.md:285-290,531,556,578` |
| Pessoas | Funcionários › "Controle de Ponto" › "Histórico" / "Relatório" | jornadas, saldo, calendário do mês | "CSV" no Histórico | `T15/inventario.md` 3.9; `components/time-tracking/TimeHistory.tsx:193-215` |
| Loja | PDV › "Relatórios da Loja" (módulo PDV) | vendas do balcão | (fora da trilha) | `App.tsx:836` |
| Tudo | Configurações › Empresa › "Exportar meus dados" | planilha com uma aba por grupo | Excel | `T01/inventario.md:350-361` |

### 3.8 Exportações em detalhe

- **Contas a Pagar/Receber**: "Exportar" ▾ → "Excel" (planilha), "PDF" (abre em **nova aba**, com o botão "Baixar PDF"), "CSV";
  título do arquivo "Contas a Pagar", "Contas a Receber" ou "Contas a Pagar e Receber" conforme a aba; linhas = a lista
  **filtrada** da tela (`FinanceContas.tsx:956-1011`; `utils/movimentacoesPdfGenerator.ts:20,133,337`; `utils/openPdfInTab.ts:8-10,106`).
  Erros: "Não foi possível gerar o PDF", "Não foi possível gerar o Excel", "Não foi possível gerar o CSV" (`FinanceContas.tsx:995,1003,1011`).
- **Movimentações Financeiras**: o mesmo trio, na ordem "PDF", "Excel", "CSV" (`TransactionListPanel.tsx:717-743,919-930`).
- **DRE / DFC / Contabilidade**: `T20/inventario.md:31-32` (PDF do DRE **baixa direto**, `utils/drePdfGenerator.ts:297-300`).
- **Estoque**: "Exportar" → "PDF"/"Excel" → "Selecionar materiais" ("Selecionar todos", "Limpar todos") → "Exportar PDF"/"Exportar
  Excel" (`T08/inventario.md:285-290`); contagem, posição e relatório com o próprio "Exportar" (`T08/inventario.md:531,556,578`).
- **Ponto**: botão "CSV" do Histórico (`TimeHistory.tsx:193-196,212-215`; `utils/exportTimesheets.ts`), colunas "Funcionário",
  "Data", "Dia da semana", "Entrada", "Saída", "Trabalhado", "Intervalo", "Saldo", "Status", "Jornadas"
  (`lib/i18n/messages/app/employees.ts:646-655`).
- **Exportar meus dados** (`lib/i18n/messages/app/settings.ts:414-469`): cartão "Exportar meus dados" ("Baixe uma planilha do Excel
  com os dados da sua empresa…") → **"Exportar dados"** → janela "Exportar meus dados" ("Escolha o que deseja incluir na planilha. O
  arquivo é gerado na hora e baixado automaticamente.") com os grupos "Clientes", "Equipamentos", "Ordens de Serviço",
  "Orçamentos", "Contratos", "Financeiro", "Estoque", "Movimentações de Estoque", "Vendas do PDV", "Fiado dos Clientes",
  "Funcionários", "CRM / Leads", "Ponto"; "Marcar tudo" / "Limpar seleção"; aviso "Movimentações de Estoque e Ponto vêm desmarcados
  por padrão…"; "Cancelar" / **"Exportar"** → "Exportando...", "Exportando {sheet}... {rows} registros" → **"Exportação concluída! O
  arquivo foi baixado."** (erro: "Não foi possível exportar os dados. Tente novamente."; sem grupo: "Selecione pelo menos um item
  para exportar."). Abas do arquivo: "Resumo" e uma por tabela ("Contatos dos Clientes", "Materiais das OS", "Contas Bancárias"…).

---

## 4. Backend por tela

### 4.1 Chamadas do Dashboard (`hooks/useDashboardStats.ts`)

| Leitura | Detalhe | Linhas |
|---|---|---|
| `service_orders` | todas, paginadas: `id, order_number, status, os_type, scheduled_date, technician_id, check_in_time, check_out_time, created_at, service_type_id, origin, description, customer(name, city, state, lat, lng)` | `:14-33` |
| `customers` | só a contagem (`count: exact, head: true`), não exibida (P24) | `:40-45` |
| `financial_transactions` | pagas (`is_paid=eq.true`), paginadas: `transaction_type, amount, transaction_date, is_paid, transfer_pair_id` | `:47-58` |
| `profiles` | `user_id, full_name, avatar_url` | `:60-63` |
| `service_ratings` | `service_order_id, quality_rating, nps_score` (paginada) | `:65-70` |
| `service_types` | `id, name, color` | `:72-75` |
| `technician_locations` + `profiles` | posições das últimas 2 h (`created_at=gte`, até 1000) e canal ao vivo | `hooks/useLiveTechnicianLocations.ts:62-72` |
| `admin_notices`, `admin_notice_dismissals` | avisos da Dominex no topo | `hooks/useSystemNotices.ts:36,55,79` |
| `company_settings` + Nominatim | endereço da empresa geocodificado para centrar o mapa | `DashboardLiveMap.tsx:51-69`; `utils/geolocation.ts:125-128` |
| Tiles do mapa e ícones | `VITE_MAP_TILES_URL` (padrão OpenFreeMap) e ícones do Leaflet em `unpkg.com` | `lib/mapTiles.ts:17-27`; `DashboardLiveMap.tsx:120-122` |

A paginação (`utils/supabasePagination.ts`) pede `offset`/`limit` de 1000 em 1000.

### 4.2 Relatórios e exportações

- Relatório e NPS de OS: leituras do T5 (`T05/inventario.md` 4); Financeiro: `T13`/`T20` (seção 4 de cada); Estoque: `T08`; Ponto:
  `T15`. Todos herdados.
- Exportações de lista (Contas, Movimentações, DRE, DFC, Estoque, Ponto): geradas **no navegador** a partir do que já está na
  tela; nenhuma chamada nova.
- Exportar meus dados: lê, paginado, `customers`, `customer_contacts`, `equipment`, `service_orders`, `service_materials`,
  `quotes`, `quote_items`, `contracts`, `contract_items`, `financial_transactions`, `financial_accounts`, `inventory` (com o RPC
  `get_accessible_inventory_ids`), `inventory_stock_levels`, `inventory_movements`, `pdv_orders`, `pdv_order_items`,
  `pdv_order_payments`, `customer_credit_ledger`, `employees`, `leads`, `time_records`, só dos grupos marcados
  (`hooks/useCompanyDataExport.ts:218-1336`). Não grava nada no banco.

### 4.3 Comparação com o backend falso (`/home/claude/domiflix/rec/fakebase`)

| Precisa | Situação | O que fazer |
|---|---|---|
| As seis leituras do Dashboard | em 31/10 o log tinha `service_orders`, `technician_locations`, `financial_transactions`, `service_ratings` e `service_types` como `TABELA_SEM_SEED` (`desconhecidos.log:4-8`), já com `offset=0&limit=1000` | herdar a semente do fim do T21, que terá tudo |
| Avisos da Dominex | sem semente = nenhum aviso (o desejado) | nada |
| Mapa | tiles falsos de Niterói (`rec/fakebase/http/tiles.mjs`), Nominatim e unpkg com handler (`handlers/ext/nominatim.openstreetmap.org.mjs`, `handlers/ext/unpkg.com.mjs`) | conferir WebGL no Chromium do robô (dúvida do T5, `T05/inventario.md:479`) |
| Técnico no mapa (se a decisão 2 do plano for mostrar) | `technician_locations` com `created_at` recente (janela de 2 h) e uma OS de hoje a caminho/em andamento | semente do T17; ver P2 antes |
| `get_accessible_inventory_ids` | handler pedido no T8 (`T08/plano.md:94`) | herdar; sem ele, Estoque vazio e a aba "Estoque" do arquivo sem linhas |
| Relatórios das áreas | cada aula anterior lista o seu | herdar |
| Exportações | geradas no navegador | nada no backend; a gravação precisa aceitar o download (Exportar meus dados) e a nova aba (PDF de Contas) |

---

## 5. Pegadinhas para roteiro e gravação

- **P1. [handoff] "Todos os tempos" mostra o mês atual.** O preset devolve início e fim vazios (`DateRangeFilter.tsx:63-64`) e o
  Dashboard troca vazio pelo mês corrente (`pages/Dashboard.tsx:63-64`). O conselho do Guia ("Meu Dashboard está vazio → Todos os
  tempos") não funciona. Na aula: "Este mês", "Mês passado" ou "Este ano".
- **P2. [handoff, bug] Fuso: data sem hora vira o dia anterior.** `scheduled_date` e `transaction_date` são `DATE`
  (`supabase/migrations/20260131190034_d842ab49-6aeb-4fcb-ab46-1b86a7a5ce92.sql:73-81,141-148`), e três blocos fazem
  `new Date('AAAA-MM-DD')`, que o navegador lê como meia-noite UTC, ou seja, 21h do dia anterior em São Paulo. O filtro de período
  não erra porque ancora no meio-dia (`pages/Dashboard.tsx:43-47`). Efeitos:
  1. **"Requer Atenção"** lista OS **de hoje** ainda aberta como **"Atrasada 0 dias"** (`:221-222,229`).
  2. **"Evolução de OS"** marca cada OS no dia anterior, e OS de segunda-feira cai na semana de antes (`:193,204-205`).
  3. **"Fluxo de Caixa"** desloca um dia e **descarta o primeiro dia do período**: a chave cai fora dos baldes e o valor some do
     gráfico e dos totais "Entradas:/Saídas:/Saldo:" (`:164-174`), enquanto o cartão "Faturamento" conta o dia (`:114-116`).
  O robô grava em America/Sao_Paulo (`rec/recorder/browser.mjs:22,178`), então aparece no vídeo. Correção de uma linha por bloco:
  ancorar no meio-dia, como `filterByRange` já faz. Até lá, na gravação: nenhuma OS de hoje aberta no momento do Dashboard, nenhum
  lançamento no primeiro dia do período e sem zoom nos rótulos dos eixos.
- **P3. [handoff, bug] "Evolução de OS" em ordem alfabética.** Os pontos são ordenados pelo texto do rótulo
  (`pages/Dashboard.tsx:200`): "Mensal" em "Este ano" sai "abr, ago, dez, fev…"; "Diário" em "Últimos 30 dias" põe "01/11" antes de
  "15/10"; "Semanal" põe "S26/10" depois de "S23/11". Só "Este mês" com "Diário" sai em ordem (salvo OS no dia 1, por causa da P2).
- **P4. OS sem data ficam de fora.** Cartões, "OS por Status", "OS por Tipo" e "Evolução de OS" filtram por `scheduled_date` no
  período (`pages/Dashboard.tsx:40-49,71-87`): o chamado do portal ainda sem data (o da Mariana Lopes, T5) e a OS #17 "Agendada" do
  T9 (se seguir sem data) não contam em "OS Abertas". O chamado aparece em "Chamados abertos".
- **P5. [handoff, texto] "{n} concluídas este mês" fixo.** O texto não acompanha o filtro (dash `:21`; `DashboardKPIs.tsx:64`):
  em "Mês passado" continua "este mês".
- **P6. [handoff, Guia] "Taxa de Conclusão"** = concluídas ÷ (abertas + concluídas), canceladas fora (`pages/Dashboard.tsx:91-95`).
  A fala diz "a parte do trabalho do período que já foi concluída".
- **P7. [handoff, cálculo] Seta de "OS Abertas" compara com o que ainda está aberto.** O período anterior conta as OS dele pelo
  status **de hoje** (`pages/Dashboard.tsx:122-124`): como quase tudo do mês passado já foi concluído, a seta tende a subir. A fala
  não interpreta a seta de OS; a do Faturamento é confiável.
- **P8. "Faturamento" = entrada paga, não só receita de serviço.** Soma toda `entrada` paga exceto transferência
  (`pages/Dashboard.tsx:112-116`): aporte de sócios, empréstimo recebido, resgate de aplicação e venda de ativos (categorias do
  sistema, seção 0.5) entram, embora fiquem fora do DRE. Usa a data do lançamento (`transaction_date`), não a do pagamento
  (`paid_date`). No mundo fictício só há receitas de serviço; a fala diz "o que entrou no período, já pago".
- **P9. [handoff] Atalhos genéricos.** "Ver relatório" (Desempenho da Equipe), "Atribuir técnico" e "Ver todas as OS" (Requer
  Atenção) abrem a lista de OS sem filtro, não o relatório nem a OS (`DashboardTopTechnicians.tsx:128`;
  `DashboardCriticalOS.tsx:111,120`). Clicar na linha da OS crítica também abre só a lista (`:54,88`).
- **P10. Rótulos mudam entre computador e celular** (seções 3.3 e 3.4): "{n} concluídas" × "{n} OS"; "Atrasada {n} dias" ×
  "Atrasada {n}d"; "Ver todas as OS" × "Ver todas as OS críticas". O roteiro usa os do computador.
- **P11. "Requer Atenção" e "Chamados abertos" ignoram o período** (de propósito, Guia T17 cap. 3: "atraso antigo não pode sumir
  da vista").
- **P12. "Abrir Mapa ao Vivo" só no estado vazio.** Com técnico em campo, o cartão mostra as fotos e não tem botão
  (`DashboardLiveMap.tsx:216-252`); o caminho é o menu "Mapa e Rastreamento" (T5).
- **P13. Mapa vazio é o normal fora do atendimento.** Só entra quem tem OS de hoje a caminho/em andamento **e** posição das
  últimas 2 h (`pages/Dashboard.tsx:308-321`; `useLiveTechnicianLocations.ts:66-72`).
- **P14. Saudação pela hora do aparelho** (`pages/Dashboard.tsx:33-38`): com FAKE_NOW às 16:30 sai "Boa tarde. Veja como está o
  dia."; depois das 18h, "Boa noite. Resumo do dia de hoje.".
- **P15. Aviso de chamados na frente.** Sem a marca `dominex:portal-tickets-seen:<id da Camila>` no `storage`, o aviso cobre a tela
  ao abrir (`PortalCallsAlert.tsx:35-52`; `T12/plano.md:92`).
- **P16. "Evolução de OS" abre em "Mensal"** (`DashboardOSEvolution.tsx:26`): em "Este mês" é um ponto só ("nov"). O roteiro
  clica em "Diário".
- **P17. "Cancelada" some quando é zero** em "OS por Status" (`DashboardStatusSummary.tsx:45`).
- **P18. Toda exportação sai do vídeo.** Excel e CSV baixam arquivo; PDF de Contas e de Movimentações abre nova aba; PDF do DRE
  baixa (`T20/inventario.md:251`). O gravador ainda não grava download nem nova aba (`TRILHA.md`, trabalho comum 6): abrir os menus;
  em "Exportar meus dados", a barra de progresso e o aviso de conclusão ficam na própria tela.
- **P19. "Exportar meus dados" exige permissão gravada** (admin vê; outro usuário só com "Exportar Dados da Empresa" **com
  registro**, `pages/Settings.tsx:121-127`). **[LGPD, informativo]** A aba "Funcionários" leva CPF, e-mail, telefone, endereço,
  salário e chave PIX (`hooks/useCompanyDataExport.ts:1273-1291`); a trava é só na tela, e os mesmos dados já são legíveis pelas
  regras da tabela (`T15/inventario.md` P19). Na aula, não marcar "Funcionários".
- **P20. [handoff, segurança] (média, dentro da empresa) "Ver Totais Financeiros" não protege nada na tela, e o lançamento aceita
  qualquer papel.** A permissão `fn:view_finance_totals` ("Visualizar saldos, totais e projeções", `hooks/usePermissions.ts:112`) não
  é conferida em nenhum componente (só nas regras de `financial_accounts`,
  `supabase/migrations/20261019170000_split_bank_account_permissions.sql:122-168`): quem tem só a tela Dashboard vê "Faturamento"
  e "Fluxo de Caixa" (`DashboardKPIs.tsx:70-79`). E `financial_transactions` libera **ler, criar e alterar** lançamentos para
  qualquer usuário logado da empresa com assinatura ativa
  (`supabase/migrations/20261004213000_tenant_subscription_entitlement_rls.sql:162-197`); só excluir exige `can_delete_finance`
  (`:199-210`). No modo legado (sem permissões gravadas) todo usuário tem a tela Dashboard (`TRILHA.md`, achado 2). Mesma família
  do achado 5 do `TRILHA.md`; aqui com valores de caixa e escrita.
- **P21. Atividade comercial não é do cliente.** O relatório de atividade (com exportação) é do painel da Dominex
  (`components/admin/salesperson/activity/CommercialActivityTab.tsx`; `utils/salespersonActivityExport.ts`), que a trilha deixa de
  fora ("Só do painel da Dominex", `trilha...v1.22.5.md:1369-1370`); o CRM do cliente não tem relatório (`T10/inventario.md:371,402`).
  O item "pessoas e comercial" fica só com o ponto.
- **P22. "Faturamento" do cartão vai para a Visão Geral do Financeiro** (`/financeiro` → `/financeiro/relatorio`), não para
  "Relatórios" (`App.tsx:840-842`).
- **P23. Números do Dashboard dependem de todas as sementes.** O cálculo é no navegador sobre tudo o que as aulas criaram (OS #1 a
  #34 e as do T21, Financeiro do T13 ao T15, avaliações do T7); conferir os valores no ensaio. A fala não lê números.
- **P24. [handoff, desempenho] Consultas sem uso e recarga pesada.** A contagem de clientes é buscada e não aparece
  (`useDashboardStats.ts:40-45,80`); todas as OS e lançamentos pagos da empresa são relidos a cada 30 s (`:14-33,47-58,89`). Sem
  efeito no vídeo.
- **P25. A lista de OS aberta pelo bloco não leva o período.** Clicar num status de "OS por Status" abre Ordens de Serviço com o
  filtro daquele status (`pages/ServiceOrders.tsx:104-112`), mas a tela de OS abre em "Todo o período" (`T05/inventario.md:24`):
  a lista pode ter mais OS que o número do bloco. A fala diz "a lista já abre nesse status", sem prometer os mesmos números.

## 6. 🚫 Não prometer

- Cartões "Clientes ativos" e "Técnicos em campo" no topo (removidos na 1.5.9).
- Relatório de atividade comercial, de motivos de perda ou de vendedores para o cliente (P21).
- Dashboard personalizável (escolher ou mover blocos) ou envio do Dashboard por e-mail: não há nada no código (seção 0.5).
- Exportar o próprio Dashboard (não há botão) e exportar o Relatório de OS ou o NPS (nenhum botão em `OsReportDashboard.tsx` nem em
  `NpsDashboard.tsx`).
- "Todos os tempos" no Dashboard (P1) e "Ver relatório"/"Atribuir técnico" levando direto ao relatório ou à OS (P9).
- Busca única que procura em tudo (o Guia T17, cap. 5, confirma que não existe).

## 7. Dúvidas em aberto (só rodando)

1. Os números de cada cartão com a semente do fim do T21 (FAKE_NOW 13/11, "Este mês"), e se a seta do Faturamento aparece.
2. Se a semente herdada tem OS com data passada ainda aberta (vai para "Requer Atenção") ou se aparece "Tudo em dia!".
3. Se o mapa vetorial renderiza no Chromium do robô (WebGL) ou cai no fundo neutro (`lib/mapTiles.ts:61-87`).
4. Como o gravador reage ao download de "Exportar meus dados" (o aviso de conclusão depende do arquivo gerar) e ao PDF em nova aba.
5. Como fica a área de um ponto só em "Mensal" (dois pontos sobrepostos?).

## 8. Termos e pronúncias

Dashboard ("déchibórd"), KPI (não aparece na tela; a fala diz "indicadores"), NPS ("ene-pê-ésse"), DRE ("dê-érre-é"), DFC
("dê-éfe-cê"), CSV ("cê-ésse-vê"), PDF ("pê-dê-éfe"), Excel ("écsel"), GPS ("gê-pê-ésse"), Shift + D ("xífti dê").
