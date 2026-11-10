# Inventário · T25 · Dashboard, Agenda e rotina

Código lido: EcoSistema **1.59.154** (`src/config/version.ts:16`), cópia em `/home/claude/ecoflix/app-src-1.59.154/`.
Caminhos relativos a `src/`. Rótulo entre aspas = texto exato da tela (pt-BR). Só o que a aula usa.
A cópia não traz `supabase/migrations`: o que as RPCs devolvem vem do contrato do front (e do T15 para os números de outubro).

## 1. Dashboard (`/dashboard`, `pages/Dashboard.tsx`)
- **Onde:** primeiro item do menu lateral, "Dashboard" (`config/routes.ts:413`); no celular, "Início" na barra de baixo.
- **Cabeçalho** (`:2104-2142`): "Olá, {nome}!" · "Bem-vindo de volta ao seu painel de controle"; à direita o filtro de período
  (`components/DateRangeFilter.tsx:410-450`: "Todos os tempos", "Hoje", "Últimos 7 dias", **"Este mês"** (padrão, `:410`),
  "Mês passado", "Últimos 30 dias", "Este ano", "Personalizado") e o botão **"Configurações"** (só ícone no celular).
- **Ordem padrão** (`hooks/useDashboardLayout.ts:63-80`): "Lembretes da Agenda" (faixa, só com tarefa do dia), os três cartões,
  "Compras vs Vendas", "Evolução", os três comparativos, "Saldos em Aberto", "Métodos de Pagamento", "Volume Semanal",
  "Materiais Mais Comprados", "Principais Fornecedores", "Principais Clientes" e, no fim, "Demonstrativo Financeiro (DRE)".
- **Cartões** (`:1272-1395`): "Total Compras", "Total Vendas", "Margem (Vendas − Compras)" (verde se positiva, vermelho se
  negativa, cinza se zero, `:1340-1350`), cada um com "Ver detalhes" (`:1298,1332,1382`). Seguem o filtro (RPC
  `get_financial_dre_summary`, regime padrão "caixa", `:421,514-530`; margem = vendas − compras, `:526`).
- **"Ver detalhes"** (`components/dashboard/StatDetailModal.tsx`): título "Margem (Vendas − Compras)" (`:69`), "Detalhamento da
  métrica do período selecionado" (`:175`), "Total no período", **"Como é calculado"**: "Total de Vendas", "− Total de
  Compras", "= Margem" (`:204-224`), "Comparativo mensal" com "vs. mês anterior" (`:119,228-245`).
- **Gráficos de 6 meses**: "Compras vs Vendas (Últimos 6 Meses)" (barras "compras" e "vendas", `:1396-1445`) e **"Evolução da
  Margem"** (área "Margem", `:1446-1490`). RPC `get_monthly_purchases_sales` com `p_months` 6 e `p_reference_date` = fim do
  período do filtro (`:755-770`): **sempre seis meses**, terminando no fim do período escolhido.
- **Comparativos** (`:1522-1640`): "Comparativo Mensal - Total Compras", "… - Total Vendas", "… - Margem"; linhas "Mês Anterior"
  e "Mês Atual" e a variação em % com seta. Sempre o mês passado inteiro × o mês atual até hoje, sem olhar o filtro
  (`:945-975`, "mês anterior inteiro versus mês atual acumulado até hoje").
- **"Volume Semanal de Compras"** (`:1785-1835`): área "Peso (kg)", eixo com o domingo de cada semana ("dd/MM"), dica "Peso" em
  kg. **8 semanas fixas**, sem olhar o filtro (RPC `get_dashboard_operacao`, `:824-834`).
- **Rankings** (seguem o filtro; top 5; RPCs `get_top_materials` e `get_top_partners` `p_kind` compra/venda, `:636-665`):
  "Materiais Mais Comprados" (`:1836-1930`), "Principais Fornecedores" (`:1931-2010`), "Principais Clientes" (`:2011-2095`),
  cada um com o seletor "R$" / "Kg" (`:1847-1868`) e, nos parceiros, "Ver todos os fornecedores" / "Ver todos os clientes", que
  abre "Todos os fornecedores" / "Todos os clientes" (`components/dashboard/TopEntitiesDialog.tsx`, RPCs
  `list_top_suppliers_paginated` / `list_top_clients_paginated`, "Anterior", "Próximo").
- **Personalizar** (`components/dashboard/DashboardSettingsModal.tsx`): botão "Configurações" (`:28`) → "Configurações do
  Dashboard" (`:35`) · "Escolha quais seções exibir. Arraste os cards para reordená-los." (`:40`) · uma chave por seção com os
  nomes de `useDashboardLayout.ts:22-39` ("Lembretes da Agenda", "Card Total Compras", "Card Total Vendas", "Card Lucro",
  "Compras vs Vendas", "Evolução do Lucro", "Demonstrativo Financeiro (DRE)", "Comparativo Mensal - Compras", "Comparativo
  Mensal - Vendas", "Comparativo Mensal - Lucro", "Saldos em Aberto", "Métodos de Pagamento", "Volume Semanal", "Materiais
  Mais Comprados", "Principais Fornecedores", "Principais Clientes") · "Voltar ordem ao normal" (`:55`, volta ordem, chaves e
  tamanhos ao padrão, `useDashboardLayout.ts:219-226`). **Arrastar:** a alça (ícone de seis pontos) aparece no canto de cima
  à esquerda ao passar o mouse (`components/dashboard/SortableDashboardSection.tsx:31-38`); dnd-kit com `PointerSensor` e
  distância mínima de 8 px (`Dashboard.tsx:431-432`). Tudo fica no `localStorage` `dashboard-layout-v2-<usuário>`
  (`useDashboardLayout.ts:97-99`): por usuário, no navegador.
- **Faixa "Lembretes da Agenda"** (`components/dashboard/AgendaReminders.tsx`): "{n} lembrete(s) para hoje" + as três primeiras
  tarefas do dia com "Lembrar no dia" (`schedule_tasks`, pendentes, `:14-30,41`); clique leva à Agenda.
- **"Tarefas para hoje"** (`components/dashboard/DailyTasksReminderModal.tsx`, montado no `AppLayout.tsx:520`): abre uma vez
  por dia quando há tarefa pendente hoje (`localStorage` `daily-tasks-reminder-last-shown-<usuário>`, `:14,41-45`): "Tarefas para
  hoje", "Você tem {n} tarefa(s) pendente(s)", lista com horário, "Fechar" e "Ir para Agenda" (`:58-110`).

## 2. Agenda (`/agenda`, `pages/Agenda.tsx`)
- **Onde:** último item do menu lateral, "Agenda" (`config/routes.ts:491`); atalho Shift+A.
- **Tela:** "Agenda" · "Gerencie suas tarefas e compromissos"; abre em "Mês" no computador e em "Dia" no celular (`:74`).
  Cabeçalho do calendário (`components/agenda/AgendaCalendar.tsx:228-290`): setas, o mês ("nov 2026") com seletor, "Hoje",
  "Dia" · "Semana" · "Mês". À direita (≥ 1280 px, `Agenda.tsx:225-234`), o dia escolhido ("10 de novembro", "terça-feira"),
  o botão **"Nova Tarefa"** e as tarefas do dia ("Nenhuma tarefa neste dia") (`components/agenda/AgendaDaySidebar.tsx:36-80`).
  Rodapé "Legenda:" "Tarefa", "Coleta", "CRM", "Outro" (`components/agenda/TaskCard.tsx:229-247`).
- **"Nova Tarefa"** (`components/agenda/TaskFormDialog.tsx`): "Título", "Descrição", "Categoria" ("Tarefa" padrão, "Coleta",
  "CRM", "Outro", `:288-315`), "Cliente / Fornecedor" (só na categoria Coleta, `:318-400`), "Data", "Horário", "Lembrar no dia"
  (ligado por padrão, `:115,440-447`), "Notificação push"; "Cancelar", "Salvar". Toasts "Tarefa criada com sucesso" e
  "Tarefa atualizada" (`hooks/useScheduleTasks.tsx:465,488`). Backend: `schedule_tasks` (insert/update).
- **Arrastar para outro dia** (`AgendaCalendar.tsx:126-190`): arrasto nativo do navegador (`draggable`, `onDrop`) nas vistas
  "Semana" e "Mês"; grava `scheduled_date` (`Agenda.tsx:172-177`, toast "Tarefa atualizada"). Não arrastam: vista "Dia",
  avisos automáticos e tarefas do CRM (`:169`).
- **Feriados** (`Agenda.tsx:59-87`, `utils/holidays.ts:39-56,154`): nacionais calculados (novembro: "Finados" 02, "Proclamação
  da República" 15, "Consciência Negra" 20) e municipais de uma lista própria (Taubaté não está nela); cidade e UF de
  `company_fiscal_config`. Etiqueta com estrela no dia (`AgendaCalendar.tsx:192-215`). Liga e desliga em Configurações →
  "Usabilidade" → seção "Agenda" → **"Exibir Feriados"** ("Mostrar feriados nacionais e municipais (baseados na cidade da
  empresa) na agenda"; toasts "Feriados ativados na agenda" / "Feriados desativados na agenda";
  `components/settings/SettingsUsabilityContent.tsx:1227-1262`, guardado no `localStorage` `agenda-show-holidays`).
- **Avisos automáticos** (só leitura, não arrastam nem editam; `hooks/useScheduleTasks.tsx:70-80,353-440`):
  1. "Vencimento - Assinatura EcoSistema" ("Data de vencimento da assinatura"), laranja, na data de `companies.subscription_expires_at`
     (`:358-390`).
  2. Contas a pagar e a receber não pagas (`financial_bills`): "A Pagar: R$ …" (vermelho) e "A Receber: R$ …" (verde), com
     "{parceiro} — {descrição}", no vencimento (`:161-200,392-401,316-350`).
  3. Fiado (saldo) com vencimento (`balances.due_date`): **abatido** dos títulos do mesmo parceiro; só entra o que sobra, como
     "Saldo (fiado)" (`:403-428`). Venda ou compra a prazo com vencimento já gera o título (`components/MultiPaymentDialog.tsx:47-58`),
     então o fiado aparece **uma vez**, como a conta (ou as parcelas).
  Clique num aviso de conta ou fiado leva a "Contas a Pagar/Receber" (`TaskCard.tsx:39`).

## 3. Atalhos de teclado e Ctrl+K
- **Lista dos atalhos** (`hooks/useKeyboardShortcuts.tsx:21-36`): Shift+D "Dashboard", Shift+C "Compra", Shift+V "Venda",
  Shift+X "Caixa", Shift+P "Pedidos", Shift+E "Ver Estoque", Shift+S "Configurações", Shift+F "Funcionários (RH)", Shift+N
  "Fiscal & Ambiental", Shift+A "Agenda"; Ctrl+K "Busca Global". Não valem digitando num campo (`:170-177`). Ligados por
  padrão (`user_shortcuts.shortcuts_enabled`, `:50-92`).
- **"Atalhos de Teclado"** (`components/KeyboardShortcutsModal.tsx`): abre **só** por "Ver Atalhos de Teclado", na busca do Ctrl+K
  (digitando "atalho", "teclado" ou "shortcut", `CommandPalette.tsx:555,660-680`), pelo evento `open-keyboard-shortcuts`
  (`AppLayout.tsx:350-355,539`). O "?" do hook `useKeyboardShortcutsModal` (`:139-166`) **não está montado** em lugar nenhum.
  Conteúdo: "Atalhos Globais" (Ctrl+Z "Desfazer última ação", Ctrl+Shift+Z, Esc, Enter), "Geral", "Navegação" (rótulo,
  descrição e a tecla), quadro "Dica" (`:37-140`).
- **Configurações → "Atalhos"** (`components/settings/SettingsShortcutsContent.tsx:100-148`): "Atalhos de Teclado" (chave),
  "Navegação" · "Clique na tecla para personalizar", "Geral", dicas ("Atalhos não funcionam quando você está digitando em
  campos de texto"). A aula só cita.
- **Ctrl+K** (`components/CommandPalette.tsx`): abre de qualquer tela (`:441-452`); "Buscar páginas, clientes, fornecedores,
  materiais, funcionários..." (`:618`); grupos "Ações Rápidas" ("Nova Compra", "Nova Venda", "Abrir Caixa", `:127-129,684-700`),
  "Resultados da Busca" (a partir de 2 letras, até 5 por tipo, `:287-410,705`), "Navegação" (as telas, `:95-123,735`);
  painel ao lado: tipo ("Material"), nome, "Estoque", "P. Compra", "P. Venda" (`:210-232`), "Pressione Enter para abrir"
  (`:256`). No cabeçalho, o botão "Buscar..." com "Ctrl + K" (`:600-612`). Backend: `customers`, `suppliers`, `balances`,
  `materials`, `employees`.

## 4. Telas da rotina (só abertas e apontadas; cada uma tem a sua aula)
- "Histórico do Caixa" (`/historico-caixa`, `pages/CashHistory.tsx:960-1000`): "Todos os registros de fechamento do caixa",
  "Caixas Fechados", colunas "Código", "Abertura", "Fechamento", "Aberto por", "Saldo Inicial", "Saldo Final", "Ações" (T6, T9).
- "Contas a Pagar/Receber" (`/contas-pagar-receber`, ver `T13/inventario.md` §1-2): cartões "Total a Pagar", "Total a Receber",
  "Vencidas", "Vence em 7 dias"; abas "Todas", "A Pagar", "A Receber" (T13).
- "Estoque" (`/materiais`, menu "Materiais" → "Estoque", Shift+E, T10).
- Mensal, só na fala e na ilustração: conciliação (Financeiro → "Movimentações Financeiras", T14), DRE ("Relatório Financeiro",
  T15), pacote contábil e MTR/CDF ("Fiscal & Ambiental", módulo `notas_fiscais`, T17 e T18); coletas (módulo `coletas`, T12).

## Fonte × código (vale o código)
1. **Gráfico de 6 meses:** a fonte diz "independente do filtro"; no código são sempre seis meses, mas **terminando no fim do
   período do filtro** (`p_reference_date`, `Dashboard.tsx:764-768`). A fala diz só "sempre seis meses, mesmo com o filtro num mês
   só; o filtro manda nos cartões e nos rankings".
2. **Agenda contando saldo e título duas vezes:** a 1.59.154 já abate o fiado dos títulos do mesmo parceiro
   (`useScheduleTasks.tsx:403-428`, mesma regra de Contas a Pagar/Receber): o ⚠️ não vale mais. A fala diz o positivo (o fiado
   aparece uma vez, cada parcela no seu dia; clique leva às Contas).
3. **"Evolução do lucro":** a tela diz "Evolução da Margem" e "Margem (Vendas − Compras)"; só a janela "Configurações do
   Dashboard" ainda diz "Card Lucro", "Evolução do Lucro" e "Comparativo Mensal - Lucro" (handoff para o time).
4. **Rotina semanal "propostas do marketplace":** o Marketplace está fora da trilha (seção "fora" da fonte): sai da fala.
5. **Lista de atalhos pelo "?":** o código tem o atalho, mas o hook não está montado; a lista abre pelo Ctrl+K ("Ver Atalhos de
   Teclado"). A aula ensina esse caminho (handoff: montar o hook ou tirar o código morto).
6. **"Contas a Pagar/Receber" e "Agenda" não estão na "Navegação" do Ctrl+K** (`CommandPalette.tsx:93-123`): a aula chega às duas
   pelo menu e pelo Shift+A.
