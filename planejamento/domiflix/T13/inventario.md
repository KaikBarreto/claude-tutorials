# Inventário funcional · T13 — Financeiro (Dominex)

> Base para o roteiro do tutorial "T13 · Financeiro". Levantado em 30/10/2026 contra o código publicado
> `APP_VERSION = "1.38.6"` (`src/config/version.ts:1`), cópia em `/home/claude/domiflix/src-1.38.6`.
> **Análise estática, somente leitura.** "(a confirmar)" = só rodando. Formato do inventário do T3/T12.
> O Guia Técnico (`docs/guia-tecnico/secoes/T13.html`, escrito para a 1.37.36) ajudou a achar as telas; onde ele
> diverge do código, vale o código (seção 0.3). DRE, DFC, Contabilidade e Análise ficam no T20; Cobranças e
> Assinaturas (Asaas) no T19.

## Como ler

- Caminhos relativos a `src/`, exceto `supabase/...` e `rec/...`. Formato `arquivo:linha`.
- Rótulos entre aspas = texto exato (pt-br). Fonte principal dos textos: `lib/i18n/messages/app/finance.ts:7-2035`
  (bloco pt-br). Abreviação: **fin** = `lib/i18n/messages/app/finance.ts`.
- "Conta" tem dois sentidos no app: **conta bancária/caixa/cartão** (tabela `financial_accounts`, tela Movimentações)
  e **conta a pagar/receber** (linha de `financial_transactions` não paga, tela Contas a Pagar/Receber). A fala precisa
  separar os dois (pegadinha 1).

---

## 0. Resumo para o roteiro

### 0.1 Capítulos da trilha (v1.22.5) contra o código de hoje

| # | Item da trilha | Situação | O que ajustar |
|---|---|---|---|
| 1 | Os endereços do menu Financeiro | **Mudou** | Grupo **"Financeiro"** com 5 itens: "Visão Geral", "Movimentações Financeiras", "Contas a Pagar/Receber", "Cobranças" (🔒 add-on) e "Relatórios" (`components/layout/SidebarMenuContent.tsx:170-183`). Categorias e centros de custo saíram do menu: botão **"Configurações Financeiras"** no topo da tela (`pages/Finance.tsx:325-334`). Notas Fiscais saiu do Financeiro e virou item próprio (`SidebarMenuContent.tsx:184-186`; Changelog 1.36.2, `pages/Changelog.tsx:1607`). |
| 2 | Movimentações: criar a primeira conta/caixa | **Mudou de lugar** | Coluna **"Contas e cartões"** de "Movimentações Financeiras" → botões **"Nova conta"** / **"Novo cartão"** no rodapé da coluna (`components/financial/FinanceMovimentacoes.tsx:630-761`). Formulário com **"Faz parte do caixa da empresa"** (novo, 1.36.19). Nenhuma conta nasce com a empresa (seção 3.2). |
| 3 | Lançar receita e despesa, pagar, editar, excluir | **Mudou** | Um botão só: **"Nova movimentação"** → "Receita" / "Despesa" / "Transferência" (`components/financial/NewMovementDialog.tsx`; fin `:68-78`). O formulário "Nova Transação" ganhou seções ("O que é", "Dinheiro", "Mais detalhes", "Parcelas"), cliente, fornecedor, OS e centro de custo (fin `:753-951`). "Marcar como pago" saiu de Movimentações: vive só em Contas a Pagar/Receber (`FinanceMovimentacoes.tsx:102-107`). |
| 4 | Extrato com "saldo após" e ajuste manual | **Bate** | Coluna **"Saldo Após"** no extrato de uma conta; na visão "Geral (Todos)" vira **"Saldo Total Após"** (fin `:535-539`). **"Ajustar saldo"** no menu ⋮ da conta (fin `:478-484`, `:1228-1246`). |
| 5 | Transferência entre contas | **Bate** | Pelo botão **"Transferir entre contas"** da Visão Geral ou "Transferir" no menu ⋮ da conta; precisa de 2 contas (fin `:77`). Par de lançamentos `transfer_pair_id`, fora do resultado (`pages/Finance.tsx:209-234`). |
| 6 | Cadastrar cartão: fechamento, vencimento e limite | **Bate** | "Novo cartão": "Dia de fechamento *", "Dia de vencimento *", "Limite de crédito (R$)" e a frase automática da regra (fin `:984-1024`). |
| 7 | Compra parcelada no cartão e a fatura de cada parcela | **Bate** | Bloco **"Despesa no Cartão de Crédito"** com a prévia "1/3 → fatura de …" (fin `:816-827`). |
| 8 | Pagar a fatura: integral × parcial e o limite | **Bate, com trava de data** | "Pagar Fatura" só a partir do dia do fechamento (fin `:1286-1287`). Integral quita as compras e devolve o limite; parcial não quita nenhuma (fin `:1300-1303`, `:1317-1320`). |
| 9 | Visão Geral: cards, fluxo de caixa e pizza | **Maior** | Virou um painel em blocos (1.37.40/1.37.41): "Saldo do Período", "A Receber", "A Pagar", "Saldo por Conta", "Fluxo realizado e resultado", "Projeção do caixa", "Agenda de vencimentos", "Concentração das despesas", "Evolução do resultado", "Últimas Movimentações" (`components/financial/FinanceOverview.tsx:462-907`). **Sem** "Exportar CSV", "Nova Receita" e "Nova Despesa" (o Guia ainda cita). |
| 10 | Categorias: criar, colorir, ordenar, grupo de DRE | **Maior** | Em "Configurações Financeiras" → abas **"Categorias"**, **"Centro de Custo"** e **"Grupos do DRE"** (`components/financial/FinanceRelatorio.tsx:105-111`). Agora há **subcategoria** (2 níveis), "Grupo DFC" e o campo **"Onde aparece no DRE"** ligado a grupos configuráveis (`components/financial/CategoryFormDialog.tsx:430-452`). A 🚫 "lista plana" da trilha caiu. |
| 11 | Contas a Pagar/Receber: recorrência, baixa, recebimento parcial | **Bate, tela nova** | Abas **"Todas"** (abre nela), "A Pagar", "A Receber" (`components/financial/FinanceContas.tsx:159,1040-1043`); "Lista"/"Calendário"; "Exportar"; **"Nova Conta"** com "Recorrência" 2 a 60 vezes (`components/financial/ContaFormDialog.tsx:157-159`); "Marcar pago"/"Marcar recebido" e recebimento parcial (fin `:1456-1509`). Novo: quitação/recebimento **em lote** (fin `:355-436`). |

Avisos da trilha:

- ⚠️ "Fatura integral quita, parcial não quita nenhuma — mostre o aviso" → **bate** (`hooks/useCreditCardBills.ts`, RPC
  `pay_credit_card_bill`; textos fin `:1300-1303`). Pela regra de 30/10 o parcial vira fala, sem encenar.
- ⚠️ "Transferência e pagamento de fatura não entram no faturamento nem na DRE" → **bate** (`pages/Finance.tsx:212-217`).
- ⚠️ "Recorrência já cria todas as parcelas de uma vez" → **bate**: grava 2 a 60 linhas na hora
  (`ContaFormDialog.tsx:157-159,228-242`).
- ⚠️ "Financeiro completo desde o Essencial; Exceção sem o grupo" → **bate** (comentário `SidebarMenuContent.tsx:174-176`;
  `components/ModuleGateModal.tsx:129-132`; Changelog 1.34.0 `:1781` e 1.35.6 `:1687`).
- ⚠️ "Excluir lançamento exige permissão específica" → **bate**: `fn:delete_finance` (`hooks/usePermissions.ts:111`).
- 🚫 "Não existe subcategoria" → **desatualizado** (subcategorias desde 1.24.61, `pages/Changelog.tsx:3070-3085`).
- 🚫 "Não existe tela de BDI aqui" → **continua** (BDI é do T9).

### 0.2 O que mudou desde a 1.22.5 (`pages/Changelog.tsx`)

| Versão | Mudança | Linhas |
|---|---|---|
| 1.24.61 | Subcategorias financeiras (2 níveis) | `:3070-3085` |
| 1.25.10 | Notas recebidas viram conta a pagar; pagar várias contas num lançamento só | `:2800-2815` |
| 1.27.0 | DFC; Financeiro reorganizado (Visão Geral, Movimentações, Contas, Cobranças, Relatórios) | `:2712-2722` |
| 1.28.0 | Um botão só de "nova movimentação" (receita, despesa, transferência) | `:2690` |
| 1.35.6 | Cobranças volta a ser módulo pago à parte; o resto do Financeiro segue no Essencial | `:1687` |
| 1.36.17 | Conciliação por arquivo .ofx (conta e fatura do cartão); importação por planilha | `:1362-1377` |
| 1.36.19 | Previsão de caixa por dia; conta "fora do caixa" (poupança); categorias de aporte/ativo/empréstimo | `:1303-1323` |
| 1.37.8 | Usar contas sem ver saldo (permissões separadas) | `:1010` |
| 1.37.33 | "Cobrar o saldo" direto da conta a receber (T19) | `:570-575` |
| 1.37.39 | Gerar todas as cobranças de um parcelamento (T19) | `:448` |
| 1.37.40 / 1.37.41 | Visão Geral em painel; abas horizontais; aviso quando os dados não carregam | `:394-421` |

### 0.3 O que mais pode surpreender (detalhes na seção 5)

1. **[corrigido em 31/10, conferido pelo Tech Lead]** O cadastro da empresa **cria** as contas **"Caixa"** (tipo caixa) e
   **"Conta Principal"** (banco), com saldo inicial 0, e 14 categorias padrão por `upsert` sobre as 14 "do sistema" do
   gatilho: "Serviços Prestados", "Vendas de Peças/Materiais", "Contratos PMOC" (entrada), "Impostos e Taxas" (`is_system`),
   "Custo de Materiais", "Fornecedores e Insumos", "Alimentação", "Luz/Energia", "Aluguel", "Combustível/Transporte",
   "Salários e Encargos", "Marketing e Publicidade", "Ferramentas e Equipamentos", "Outros"
   (`supabase/functions/self-register/index.ts:997-1037`; `supabase/functions/create-company/index.ts:503-541`); mais os
   6 grupos do DRE (`supabase/migrations/20261020223000_profit_distribution_and_investment_outside_dre.sql:28-42`;
   `supabase/migrations/20261021110000_renomeia_grupo_receita_dre.sql:35-50`). O nome é único por empresa
   (`supabase/migrations/20260919190000_dedup_categorias_financeiras_e_trava.sql`): criar "Aluguel" de novo dá erro. O plano
   do T11 está certo ("Caixa", "Conta Principal" e "Contratos PMOC" são padrões do cadastro). A versão anterior deste item
   dizia o contrário e estava errada.
2. Guia Técnico desatualizado em pontos visíveis: "Exportar CSV" e "Nova Receita/Nova Despesa" na Visão Geral não existem
   mais; o interruptor "Incluir compras no cartão" mudou para Configurações → Usabilidade → "Movimentações financeiras"
   (`FinanceMovimentacoes.tsx:936-940`; `lib/i18n/messages/app/settings.ts:281-284`).
3. "Pagar Fatura" fica travado até o dia do fechamento, pelo relógio do navegador (TRILHA, trabalho comum 5).
4. O grupo de despesa operacional padrão do DRE se chama **"Despesas com pessoal"** e recebe toda categoria OPEX
   (aluguel, combustível…) (`components/financial/FinanceDRE.tsx:873-879`; pegadinha 6, handoff). Pesa no T20, mas
   aparece já no campo "Onde aparece no DRE" ao criar categoria.

---

## 1. Rotas e navegação

| Tela | Como chegar | Rota / componente |
|---|---|---|
| Visão Geral | Menu "Financeiro" → **"Visão Geral"** | `/financeiro/relatorio` (`lib/i18n/appRouteSlugs.ts:155`) → `pages/Finance.tsx` → `components/financial/FinanceOverview.tsx` |
| Movimentações Financeiras | Menu → **"Movimentações Financeiras"** | `/financeiro/movimentacoes` (`appRouteSlugs.ts:156`) → `FinanceMovimentacoes.tsx` |
| Contas a Pagar/Receber | Menu → **"Contas a Pagar/Receber"** | `/financeiro/contas` (`appRouteSlugs.ts:157`) → `FinanceContas.tsx` |
| Cobranças (T19) | Menu → "Cobranças" (só com o add-on) | `/financeiro/cobrancas` (`appRouteSlugs.ts:158`) |
| Relatórios (T20) | Menu → "Relatórios" | `/financeiro/relatorios` (`appRouteSlugs.ts:159`) |
| Configurações Financeiras | Botão **"Configurações Financeiras"** no topo de qualquer tela do Financeiro | `/financeiro/configuracoes-financeiras` (`appRouteSlugs.ts:160`; `pages/Finance.tsx:325-334`); abas `?tab=categorias` (padrão), `centro-de-custo`, `grupos-dre` |
| Preferência "Incluir compras no cartão" | Configurações → "Usabilidade" → card "Movimentações financeiras" | `lib/i18n/messages/app/settings.ts:281-284` |

- Todas as telas usam o mesmo cabeçalho **"Financeiro"** com subtítulo por tela ("Gerencie suas finanças", "Movimentações
  por conta", "Contas a pagar e a receber"…) (fin `:8-19`; `pages/Finance.tsx:289-301`).
- Filtro de período no topo (`components/ui/DateRangeFilter.tsx:130-139`): "Todos os tempos", "Hoje", "Últimos 7 dias",
  **"Este mês"** (padrão, `pages/Finance.tsx:106`), "Mês passado", "Últimos 30 dias", "Este ano", "Personalizado"
  (`lib/i18n/messages/app/common.ts:46-55`). Some em Cobranças e Configurações (`pages/Finance.tsx:305`).
- URLs antigas redirecionam: `/financeiro` → relatório; `/financeiro/caixas-bancos` → movimentações;
  `/financeiro/categorias`, `/financeiro/configuracoes`, `/financeiro/centro-de-custo` → configurações (`App.tsx:840-854`).
- Deep-links: `?account=<id>` abre a conta na coluna; `?txn=<id>` abre o mês do lançamento e destaca a linha
  (`pages/Finance.tsx:76-97,157-170`).
- Erro de carga: tela **"Não foi possível carregar os dados financeiros"** + "Tentar novamente" (`pages/Finance.tsx:340-366`).

---

## 2. Permissões e módulos

| Item | Regra | Fonte |
|---|---|---|
| Tela Financeiro | `screen:finance` "Financeiro" ("Visão geral, movimentações e contas a pagar e receber.") | `hooks/usePermissions.ts:87`; `App.tsx:843-848` |
| Plano Exceção | Sem o grupo Financeiro (barrado por `screen:finance`) | `SidebarMenuContent.tsx:174-176` |
| Criar/editar lançamento | `fn:manage_finance` "Gerenciar Financeiro" | `hooks/usePermissions.ts:110` |
| Excluir lançamento | `fn:delete_finance` "Excluir Lançamento Financeiro" (admin/gestor sempre) | `hooks/usePermissions.ts:111` |
| Ver saldos e totais | `fn:view_finance_totals` "Ver Totais Financeiros" | `hooks/usePermissions.ts:112` |
| Usar contas sem ver saldo | `fn:use_bank_accounts` "Usar Contas Bancárias" | `hooks/usePermissions.ts:113` |
| Cadastrar/editar/ajustar/excluir conta | `fn:manage_bank_accounts` "Gerenciar Contas Bancárias"; sem ela, a coluna mostra só nomes e some "Nova conta"/"Novo cartão" e o menu ⋮ | `hooks/usePermissions.ts:114`; `FinanceMovimentacoes.tsx:290-291,749-758` |
| "Configurações Financeiras" (categorias, centros, grupos do DRE) | Admin/gestor ou `fn:manage_settings` | `hooks/useCanManageFinanceSettings.ts:15-18`; `pages/Finance.tsx:117-119,325` |
| Receita ao concluir OS | `fn:os_finish_revenue` (T5/T7) | `hooks/usePermissions.ts:118` |
| Contas na Agenda | `fn:view_financial_schedule` | `hooks/usePermissions.ts:126` |
| 🔒 Cobranças | Add-on `cobrancas`; sem ele o item some e a rota volta para a Visão Geral | `SidebarMenuContent.tsx:180`; `pages/Finance.tsx:112-116` |
| Financeiro completo | `finance_advanced` "Contas a Pagar e Receber, DRE, DFC e relatórios, inclusos no Módulo Básico" | `components/ModuleGateModal.tsx:129-132` |

Camila é admin: vê tudo (mundo da trilha).

---

## 3. Por tela

### 3.1 Visão Geral (`FinanceOverview.tsx:462-907`; textos fin `:22-66`)

- **Cartão escuro "Saldo do Período"** com "(Receitas − Despesas)" e o ícone de ajuda: "O saldo do período é o total de
  receitas já recebidas menos o total de despesas já pagas dentro do período filtrado. Não considera valores a
  receber/a pagar nem o saldo existente nas contas." (fin `:26-29`). Dentro: "Receitas" e "Despesas" (clicam para
  Movimentações) e os botões **"Nova movimentação"** e **"Transferir entre contas"** (desligado com menos de 2 contas,
  dica "Cadastre ao menos duas contas para transferir.") (`:516-536`; fin `:41-42,77`).
- **"A Receber"** e **"A Pagar"** (clicam para Contas a Pagar/Receber) (`:540-564`).
- **"Saldo por Conta"**: "Disponível R$ …" (· "Faturas R$ …"), selo "Projeção ±R$ …", abas "Contas bancárias", "Caixas",
  "Cartões" com contador; cartão aparece com o rótulo "fatura" (`:150-170,566-603`). Vazio: "Cadastre uma conta para
  acompanhar seus saldos aqui." (`:579-582`).
- Gráficos: **"Fluxo realizado e resultado"** ("Compara entradas, saídas e o resultado líquido por mês/semana."),
  **"Projeção do caixa"** ("Saldo disponível após aplicar os vencimentos pendentes do período.", selo "Final", "Menor saldo
  projetado"), **"Agenda de vencimentos"** (faixas "Vencido", "Até 7 d"…, selo "Cobertura n×"), **"Concentração das
  despesas"** (pizza, selo "Top 3 · n%"), **"Evolução do resultado"**, **"Últimas Movimentações"** com "Ver todas" e selos
  "Pago"/"Pendente" (`:606-907`). Vazios: "Sem dados no período", "Sem vencimentos pendentes", "Sem valores em aberto".
- Transferências e pagamento de fatura ficam fora de Receitas/Despesas (`pages/Finance.tsx:209-234`).

### 3.2 Movimentações Financeiras — coluna "Contas e cartões" (`FinanceMovimentacoes.tsx:630-761`)

- Título **"Movimentações Financeiras"** (`:775`; fin `:449`). Coluna "Contas e cartões" / "Selecione para abrir o extrato e
  as ações.", busca "Buscar conta ou cartão", filtro "Tipo" ("Contas bancárias e caixa"/"Cartões"), ordenar "Nome (A–Z)",
  "Maior valor", "Menor valor" (`:633-673`).
- Itens fixos: **"Geral (Todos)"** com o saldo total e **"Conciliação"** (`:677-689`; fin `:1584`). Depois os grupos
  **"Contas"** (sublinha "Saldo R$ …") e **"Cartões"** (sublinha "Fatura em aberto R$ …") (`:693-730`).
- Rodapé: "Mostrando n de m itens", botões **"Nova conta"** e **"Novo cartão"** (`:733-758`). No celular, "Adicionar" →
  "Nova Conta"/"Novo Cartão" (`:530-547`).
- Menu ⋮ de cada conta (`:290-361`; fin `:478-484`): conta/caixa → **"Transferir"**, **"Editar"**, **"Ajustar saldo"**,
  **"Excluir"**; cartão → "Editar", **"Recalcular faturas"**, "Excluir". Excluir: "Excluir conta"/"Excluir cartão" +
  "Tem certeza? Transações vinculadas perderão a referência à conta." (fin `:485-492`).
- "Geral (Todos)": card **"Resumo financeiro"** / "Saldo consolidado das contas", "Saldos positivos", "Faturas em aberto",
  "Distribuição do saldo" (rosca, "Somente valores positivos") e aviso de conta negativa (`:798-935`); abaixo a lista de
  movimentações (3.4).
- Conta selecionada: cartão colorido com logo do banco, nome e saldo (`:462-524`) + extrato. Cartão selecionado: painel
  de faturas (3.7). Sem seleção: "Selecione uma conta ou cartão" (`:1001-1005`).

### 3.3 Nova conta / Novo cartão (`components/financial/AccountFormDialog.tsx`; fin `:984-1024`)

- Títulos "Nova Conta" / "Novo Cartão" / "Editar Conta" / "Editar Cartão".
- **"Nome da Conta \*"** (placeholder "Ex: Nubank Crédito"); **"Tipo"**: "Caixa", "Conta Bancária", "Cartão de Crédito";
  **"Instituição"** (banco e cartão; combobox "Selecione a instituição", grupos "Mais populares"/"Todos os bancos",
  fin `:973-981`).
- Caixa e banco: **"Saldo Inicial (R$)"**; **"Faz parte do caixa da empresa"** (ligado) com a explicação "Ligado, o
  dinheiro desta conta entra no fluxo de caixa dos próximos dias. Desligue em conta de poupança ou investimento…" e, se
  desligado, "Esta conta fica FORA do fluxo de caixa…" (fin `:1008-1011`). Editando conta com movimento: "Editar o saldo
  inicial recalcula o saldo atual da conta." (`:1012`).
- Cartão: **"Dia de fechamento \*"**, **"Dia de vencimento \*"** (listas "Dia 1"…"Dia 31"), frase "A fatura que fecha no dia X
  vence no dia Y do mesmo mês."/"do mês seguinte." e "Compras feitas no dia do fechamento já entram na próxima fatura.";
  **"Limite de crédito (R$)"** "opcional" (fin `:998-1007`).
- **"Cor"** (paleta + "Cor personalizada"), **"Pré-visualização"** (cartão: "Fecha dia X · Vence dia Y", "(mês seguinte)"),
  "Cancelar" / **"Criar Conta"** / **"Criar Cartão"** / "Salvar" (fin `:1013-1023`).
- Nenhuma conta é criada automaticamente com a empresa (não há `INSERT` de `financial_accounts` em migração de cadastro;
  só nas rotinas de "zerar sistema", ex. `supabase/migrations/20260524004553_zerar_sistema.sql`).

### 3.4 Lista de movimentações / extrato (`components/financial/TransactionListPanel.tsx`; fin `:509-623`)

- Barra: busca "Buscar...", filtros "Tipo" ("Entrada"/"Saída"), "Categoria", "Caixa / Conta bancária", botões
  **"Importar planilha"** (`FinanceMovimentacoes.tsx:552-563`), **"Exportar"** → "PDF", "Excel", "CSV"
  (`TransactionListPanel.tsx:915-933`) e **"Nova movimentação"** (`:816,934`).
- Colunas "Data", "Usuário", "Tipo", "Descrição", "Categoria", "Conta", "Valor", **"Saldo Após"** (extrato de uma conta) ou
  **"Saldo Total Após"** (Geral), "Ações" ("Editar", "Excluir"); divisor por dia "Saldo do dia" (fin `:527-560`).
- Só aparece o que já foi pago (`pages/Finance.tsx:190-193`). Compras no cartão ficam fora da visão Geral por padrão
  (preferência em Usabilidade; selecionar o cartão no filtro "Conta" mostra as compras dele) (`FinanceMovimentacoes.tsx:153-177`).
- Lotes ("Pagamento em lote, n contas", "Desfazer lote") e exclusão em massa ("Excluir n transações") (fin `:571-607`).
  Toasts "Lançamento excluído!", "Erro ao gerar PDF"/"Erro ao gerar Excel" (fin `:617-621`).
- Vazio: "Nenhuma movimentação" / "As entradas e saídas aparecem aqui assim que você registrar a primeira." (fin `:561-567`).

### 3.5 Nova movimentação → Nova Transação (`NewMovementDialog.tsx`; `TransactionFormDialog.tsx`; fin `:68-78,753-951`)

- Escolha: **"Nova movimentação"** / "Escolha como o dinheiro se movimenta." → **"Receita"** ("Dinheiro que entra na
  empresa."), **"Despesa"** ("Dinheiro que sai da empresa."), **"Transferência"** ("Movimento entre contas da empresa.").
- Janela **"Nova Transação"** / "Registre uma receita ou despesa", seções:
  - **"O que é"** (`TransactionFormDialog.tsx:1625-1750`): "Tipo de Movimentação" ("Receita"/"Despesa"), "Categoria"
    (busca "Buscar categoria...", criar na hora 'Criar "…"'), "Subcategoria" ("Usar a categoria principal"), "Centro de
    custo", **"Descrição"** ("Descreva a movimentação").
  - **"Dinheiro"** (`:1756-2007`): **"Valor (R$)"**, **"Conta Bancária / Caixa \*"**, "Forma de pagamento" ("Dinheiro",
    "PIX", "Cartão de Crédito", "Cartão de Débito", "Transferência", "Boleto", "Cheque"), **"Data do lançamento"** (dica:
    "Quando isso aconteceu… É essa data que conta no relatório em Regime de Competência."), interruptor **"Já foi
    recebido"/"Já foi pago"** ("Será registrado como recebido" / "Irá para contas a receber" / "Irá para contas a pagar"),
    "Data do recebimento"/"Data do pagamento" (não aceita data futura) ou **"Vencimento"** quando desligado
    (`:1983-1986`; fin `:898-907`).
  - **"Mais detalhes"** (recolhida, `:2011-2044`): "Cliente vinculado" / "Fornecedor vinculado", "Ordem de serviço",
    **"Comprovantes / Notas Fiscais"** ("Anexar comprovantes"; JPG, PNG e PDF), "Observações".
  - **"Parcelas"** (recolhida, `:2049-2185`): "À vista" ou n parcelas mensais ("Serão geradas n parcelas de R$ … com
    vencimentos mensais a partir da data informada."); com Cobranças ativo, **"Gerar cobranças no Asaas"** (T19, fin `:853-873`).
- Despesa em conta do tipo cartão: bloco **"Despesa no Cartão de Crédito"**: "n parcelas distribuídas nas faturas do cartão
  X:", linhas "1/3 → fatura de <mês> — R$ …", "Mês da fatura", lembrete "Compra no cartão não sai do caixa nem da conta
  bancária — ela entra na fatura e some do fechamento de caixa." (fin `:816-827`). Cartão não oferece "Já foi pago".
- Sem conta cadastrada: "Nenhuma conta cadastrada" / "É necessário cadastrar pelo menos uma conta ou caixa…" /
  **"Cadastrar agora"** (fin `:802-804`).
- Validações: "Descrição é obrigatória", "Valor deve ser positivo", "Data é obrigatória", "Selecione uma conta ou caixa",
  "Esta data não pode ser no futuro…" (fin `:914-924`). "Cancelar" / **"Salvar"**.
- Editar parcela muda só ela ("A alteração vale só para esta parcela…"); trocar forma de pagamento ou parcelar abre
  **"Refazer este lançamento?"** → "Refazer lançamento" (fin `:925-938`).

### 3.6 Transferência e Ajustar saldo

- **"Transferência entre Contas"** (`components/financial/TransferFormDialog.tsx`; fin `:954-970`): "Origem", "Destino"
  (só caixa/banco ativos, `pages/Finance.tsx:145-148`), "Valor (R$)", "Data", "Descrição (opcional)" ("Ex: Transferência para
  pagar fornecedor"), "Cancelar" / **"Transferir"**. Cria 2 lançamentos pagos com o mesmo `transfer_pair_id`
  (`hooks/useFinancialAccounts.ts:243-280`).
- **"Ajustar saldo"** (`components/financial/AdjustBalanceDialog.tsx:25-31`; fin `:1228-1246`): "Saldo atual", **"Saldo em
  conta (R$)"** ("Informe quanto a conta realmente tem. O sistema lança a diferença automaticamente."), frase "Será lançado
  um ajuste de R$ X (entrada|saída).", **"Confirmar ajuste"** → "Saldo ajustado!" / "Novo saldo da conta: R$ …"; mesmo valor:
  "O saldo já está nesse valor" / "Nenhum ajuste foi necessário.". Categoria "Ajuste de saldo", fora do DRE
  (`lib/finance-constants.ts:8`; `lib/finance-analysis.ts:155`).

### 3.7 Cartão: faturas e pagamento (`CreditCardBillPanel.tsx`, `CreditCardInvoiceRow.tsx`; fin `:1249-1322`)

- Cabeçalho do cartão: "Fatura em aberto", "Limite total", "Disponível"/"Disp.", linha "fecha dia X · vence dia Y"
  (fin `:466-475`).
- Filtro "Status da fatura": "Todas", "Aberta", "Fechada", "Parcial", "Paga". Linha: "Vence em dd/mm/aaaa · fecha em
  dd/mm/aaaa · n lançamentos" + selo. Vazio: "Nenhuma fatura registrada" / "As faturas aparecem automaticamente quando você
  lança despesas neste cartão.".
- **"Pagar Fatura"**: antes do fechamento fica com cadeado e a dica "Esta fatura ainda está aberta, ela fecha em {data}. A
  partir dessa data o pagamento é liberado." (fin `:1286-1287`). Janela "Pagar Fatura": "Total da fatura", "Já pago",
  "Restante a pagar", **"Pagar com \*"** (conta/caixa; "Cadastre um caixa ou conta primeiro."), **"Data do pagamento \*"**,
  **"Valor a pagar"**, avisos **"Fatura será completamente quitada"** ou "Pagamento parcial, ficará R$ X em aberto" + "As
  compras desta fatura só entram no seu resultado, no Regime de Caixa, quando a fatura for quitada por inteiro…",
  "Observações", **"Confirmar Pagamento"**. Toasts **"Fatura quitada!"** / "Pagamento registrado e limite do cartão
  liberado." ou "Pagamento parcial registrado!" / "Ainda faltam R$ X para quitar esta fatura." (fin `:1293-1321`).
- "Recalcular faturas": "Tem certeza? Isso vai recalcular a fatura de todas as despesas deste cartão. As suas despesas e
  valores não serão alterados, só a fatura em que cada uma aparece." → "Recalcular" (fin `:493-502`).
- As faturas também aparecem em Contas a Pagar/Receber, seção **"Faturas de Cartão"** (`FinanceContas.tsx:1207-1242`).

### 3.8 Contas a Pagar/Receber (`FinanceContas.tsx`; fin `:186-443`)

- Abas **"Todas"** (padrão), **"A Pagar"**, **"A Receber"** (`:159,1040-1043`). Busca "Buscar por nome, descrição, categoria
  ou valor..." com filtro ("Pendentes", "Vencidas", "Pagas", "Todas"; categoria; centro de custo) e ordenação; alternador
  **"Lista"/"Calendário"**; **"Exportar"** → "Excel", "PDF", "CSV"; **"Nova Conta"** (`:1097-1135`).
- Cards: em "Todas", "A pagar" e "A receber"; nas outras, **"Total Pendente"** e **"Total Pago"/"Total Recebido"**
  (`:1048-1056`). Faixa de horizonte: **"Vencidas"**, **"Próximos 7 dias"**, **"De 8 a 30 dias"** (`:1171-1187`).
- Linhas: "Descrição", "Categoria", "Vencimento" ("Sem vencimento"), "Valor" (em recebidas: "Bruto", "Taxa", "Líquido"),
  "Status" ("Pago", "Vencida", "Parcial", "Pendente"), "Ações": **"Marcar pago"** / **"Marcar recebido"**, **"Ver
  histórico"**, "Editar", "Excluir"; com Cobranças, **"Cobrar o saldo"**/"Ver cobrança" e selos "Cobrança em aberto"… (T19)
  (fin `:232-310`). Excluir: "Excluir conta" / "Tem certeza que deseja excluir esta conta? Esta ação não pode ser
  desfeita." (fin `:326-331`).
- Vazios: "Nenhuma conta a pagar" / "Cadastre uma conta a pagar para acompanhar os vencimentos." (e "a receber") e, na
  busca, "Ver 1 resultado em <aba>" (fin `:311-325`).
- **Quitar/Receber em lote**: marcar várias → "Quitar em lote"/"Receber em lote" → "Quitar n contas" (RPC
  `pay_transactions_batch`); motivos de bloqueio por linha (cartão, transferência, folha, parcial, cobrança enviada…) (fin `:355-436`).

### 3.9 Nova Conta (a pagar/receber) (`ContaFormDialog.tsx`; fin `:1168-1225`)

- **"Nova Conta"** / "Crie uma conta a {pagar|receber}, com opção de recorrência.". Seções "O que é", "Dinheiro", "Mais
  detalhes", **"Parcelar ou repetir"**.
- "Tipo" ("A Pagar"/"A Receber"), **"Descrição \*"** ("Ex: Aluguel do escritório"), **"Valor (R$) \*"**, "Vencimento",
  "Categoria", **"Conta Bancária / Caixa"** (obrigatória para salvar, `:224-226`), "Funcionário vinculado", "Contrato
  vinculado", "Cliente vinculado", **"Recorrência"** ("Única", "Semanal", "Mensal", "Anual") e **"Parcelas"** (2 a 60,
  `:157-159`), "Observações". "Cancelar" / **"Criar Conta"** ("Criando...").
- Gera todas as ocorrências na hora, datas por `addWeeks/addMonths/addYears` (`:228-242`).
- Com Cobranças ativo e A Receber parcelado: opção de gerar as cobranças no Asaas (`:175-182`; T19).

### 3.10 Dar baixa (`FinanceContas.tsx`; fin `:332-354,1456-1509`; `components/financial/ReceivePaymentModal.tsx`)

- A pagar → **"Confirmar pagamento"**: **"Pago com \*"** ("Selecione caixa ou conta"), "Forma de pagamento", **"Data do
  pagamento \*"** (não aceita futuro), "Observações". Conta de cartão não entra aqui: é pela fatura.
- A receber → **"Como foi recebido?"**: **"Valor recebido \*"** ("Restante a receber: R$ X. Informe um valor menor para
  registrar um recebimento parcial."), **"Novo vencimento do saldo restante \*"** (só no parcial), **"Forma de pagamento \*"**,
  **"Data do recebimento \*"**, **"Caixa / Conta bancária \*"**, "Tarifa de máquina/gateway (R$)" ("Será lançado como despesa
  em "Tarifas e Taxas"…"), resumo "Valor bruto recebido", "Tarifa", "Líquido na conta", "Valor da conta", "Já recebido",
  "Recebendo agora", "Restante após este recebimento", "Observação", **"Confirmar recebimento"**. Conta parcelada: "Conta
  parcelada — recebimento parcial não está disponível.". Validações "Informe um valor maior que zero." / "Valor não pode
  ser maior que o restante (R$ X)." (fin `:1456-1509`).
- O parcial cria a linha filha "Recebimento parcial — …" e o banco recalcula `amount_received` da conta-mãe por gatilho
  (`hooks/useFinancial.ts:193-227,886-935`; `supabase/migrations/20260523234208_pagamento_parcial_recebivel.sql:28-112`).
- **"Ver histórico"** → "Histórico de recebimentos", "Estornar recebimento?" (fin `:1365-1379`).

### 3.11 Configurações Financeiras: Categorias e Centro de Custo (`FinanceRelatorio.tsx:105-111`)

- Abas **"Categorias"**, **"Centro de Custo"**, **"Grupos do DRE"** (esta no T20).
- **Categorias** (`components/financial/FinanceCategorias.tsx`; fin `:626-686`): seções "Categorias de Receita" e
  "Categorias de Despesa" (dica "arraste para reordenar"), botão **"Nova categoria"**; selo **"Sistema"** (tooltip "Categoria
  do sistema" ou "Categoria do sistema, você pode renomear"; "Categoria usada pelos lançamentos automáticos. Você pode mudar
  o nome, a cor e o ícone, o tipo e o grupo do DRE ficam travados."); ações "Mover para cima", "Mover para baixo",
  "Editar", "Excluir", **"Adicionar subcategoria"**, "Tornar categoria principal". Excluir: "Tem certeza? Transações com esta
  categoria não serão afetadas." (variações para subcategoria e principal com filhas, fin `:681-685`).
- **Nova Categoria** (`CategoryFormDialog.tsx`; fin `:1027-1070`): **"Nome \*"** ("Ex: Serviços"), **"Tipo \*"** ("Receita",
  "Despesa", "Ambos"), **"Categoria mãe/principal"** ("Nenhuma, esta é uma categoria principal"; "A hierarquia tem no máximo
  dois níveis."), **"Onde aparece no DRE"** (grupos da empresa, `:430-452`; sem grupos, o antigo "Grupo DRE" com
  "Impostos e Deduções", "CSP (Custo do Serviço Prestado)", "Despesas Operacionais (OPEX)", "Não compõe o DRE…", `:453-476`),
  quadro **"Prévia no DRE"** (`:43`), **"Grupo DFC"** ("Atividades operacionais/de investimento/de financiamento"), "Cor",
  "Ícone", "Cancelar" / **"Criar"**. Validações "Nome é obrigatório", "Tipo é obrigatório", "Cor é obrigatória".
- Categorias que toda empresa já tem (gatilho `trg_seed_system_financial_categories`,
  `supabase/migrations/20261020223000_...:28-42`): "Tarifas e Taxas", "CSP - Materiais", "CSP - Mão de Obra Avulsa",
  "Vendas de Serviços", "Pagamento de Fatura", "Transferência entre contas", "Aporte de sócios", "Distribuição de lucros",
  "Aplicação financeira", "Resgate de aplicação", "Aquisição de ativos", "Venda de ativos", "Empréstimos recebidos",
  "Amortização de empréstimos". "Ajuste de saldo" e "Folha de Pagamento" nascem no uso.
- Grupos do DRE que toda empresa tem (`supabase/migrations/20261021110000_renomeia_grupo_receita_dre.sql:35-50`):
  "Receitas de serviços", "Impostos sobre vendas", "Custos diretos", **"Despesas com pessoal"**, "Resultado financeiro",
  "Excluídos do DRE".
- **Centro de Custo** (`components/financial/FinanceCostCenters.tsx`; fin `:1073-1165`): "Organize despesas e receitas por obra,
  projeto ou setor", "Buscar centro de custo...", **"Novo"** → "Novo Centro de Custo": "Nome \*" ("Ex: Obra Shopping Vale"),
  "Cor", "Ícone", "Descrição", "Ativo"; vazio "Nenhum centro de custo cadastrado".

### 3.12 Fora do roteiro principal (existem e são novos)

- **Conciliação** (item da coluna de Movimentações; `components/reconciliation/ReconciliationTab.tsx`; fin `:1583-1925`):
  "Conta para conciliar", "Importar extrato" (.ofx), "Continuar conciliação", "Conciliações anteriores", destinos por linha.
- **Importar planilha** (fin `:1927+`): "Baixar molde", "Enviar planilha preenchida", conferência "pronta(s)/para
  conferir/duplicada(s)", "Desfazer essa importação".
- Ambos dependem de enviar arquivo (o gravador não escolhe arquivos hoje) e de muitas RPCs (seção 4). Proposta no plano:
  citar com zoom, sem demonstrar.

---

## 4. Backend por tela

### 4.1 Chamadas

| Onde | Chamada | Fonte |
|---|---|---|
| Lançamentos (todas as telas) | `GET financial_transactions` (paginado), `POST/PATCH/DELETE`; anexos `financial_transaction_attachments` + bucket de comprovantes | `hooks/useFinancial.ts:337-944`; `hooks/useTransactionEditSubmit.ts:97` |
| Contas (gerente) | `GET financial_accounts` (`order=sort_order,name`), insert/update/delete; saldos somando `financial_transactions` pagas | `hooks/useFinancialAccounts.ts:95-169` |
| Contas (só usar) | RPC `list_usable_financial_accounts` (sem saldo) | `hooks/useFinancialAccounts.ts:105` |
| Transferência | 2 `POST financial_transactions` com `transfer_pair_id` | `hooks/useFinancialAccounts.ts:243-280` |
| Ajustar saldo | `POST financial_transactions` categoria "Ajuste de saldo" | `components/financial/AdjustBalanceDialog.tsx:25-40` |
| Faturas do cartão | `credit_card_bills` (select/insert/update) | `hooks/useCreditCardBills.ts:190`; `hooks/useFinancial.ts` |
| Pagar fatura | RPC `pay_credit_card_bill` `{p_bill_id, p_payment_account_id, p_amount, p_payment_date, p_notes}` → json | `hooks/useCreditCardBills.ts`; `rec/fakebase/schema.json` (args) |
| Estornar pagamento de fatura | RPC `revert_credit_card_bill_payment` `{p_transaction_id}` | `hooks/useFinancial.ts:696,790` |
| Recalcular faturas | `credit_card_bills` + `financial_transactions` | `hooks/useRecalculateBills.ts` |
| Baixa / recebimento parcial | `PATCH financial_transactions`; filha "Recebimento parcial"; tarifa em "Tarifas e Taxas"; gatilho recalcula `amount_received` | `hooks/useFinancial.ts:886-935`; `supabase/migrations/20260523234208_...:28-112` |
| Lote | RPCs `pay_transactions_batch`, `undo_payment_group` | `hooks/useFinancial.ts:1060,1097` |
| Categorias | `financial_categories` (+ contagem em `financial_transactions`; padrão da conta Asaas em `tenant_payment_accounts`) | `hooks/useFinancialCategories.ts:80` |
| Grupos do DRE | `dre_groups` | `hooks/useDreGroups.ts` |
| Centros de custo | `cost_centers` | `hooks/useCostCenters.ts:76` |
| Bancos (lista e logo) | `GET https://brasilapi.com.br/api/banks/v1`; logo `https://www.google.com/s2/favicons?domain=…` | `hooks/useBrazilBanks.ts:41-50,80` |
| Preferência de compras no cartão | `user_preferences` | `FinanceMovimentacoes.tsx:167` |
| Conciliação | 24 RPCs (`create_bank_statement_import`, `reconcile_*`, `finalize_bank_reconciliation`…) | `hooks/useBankReconciliation.ts` |
| Importar planilha | RPCs `preview_financial_import`, `apply_financial_import`, `revert_financial_import`; `financial_imports` | `hooks/useFinancialImport.ts` |

### 4.2 Gatilhos do banco que mudam a tela (o fakebase não tem gatilho)

| Gatilho | Efeito | Fonte |
|---|---|---|
| `trg_seed_system_financial_categories` / `trg_00_seed_system_dre_groups` | 14 categorias e 6 grupos do DRE ao criar empresa | `supabase/migrations/20261020223000_...:28-42`; `20261021090000_dre_groups_configuraveis.sql:109-116` |
| `trg_recalc_amount_received` | Soma das filhas → `amount_received` da conta-mãe ("Parcial", "Recebido R$ X de R$ Y") | `supabase/migrations/20260523234208_...:73-112` |
| `tg_set_transaction_date_financial_transactions`, `guard_reconciled_transaction_delete`, `trg_nfse_auto_enqueue_on_payment` | Data padrão, trava de exclusão conciliada, fila de nota automática | `supabase/migrations/*.sql` (`CREATE TRIGGER`) |

### 4.3 Comparação com o backend falso (`/home/claude/domiflix/rec/fakebase`)

| Item | Hoje | Falta |
|---|---|---|
| Tabelas do Financeiro (`financial_*`, `credit_card_bills`, `cost_centers`, `dre_groups`) | **No schema**, sem seed: o T3 registrou `TABELA_SEM_SEED financial_accounts/financial_categories/cost_centers/financial_transactions` (`rec/fakebase/desconhecidos.log`) | Seeds: 14 categorias do sistema + 6 grupos do DRE (imitam os gatilhos) + o que o T11 deixar ("Conta Principal", "Contratos PMOC", 12 parcelas do PMOC) |
| RPC `pay_credit_card_bill` | **Sem handler** (devolve nulo) | Handler: 2 pernas com `transfer_pair_id` (saída na conta, entrada no cartão), atualiza `credit_card_bills` (pago/parcial) e, se integral, `is_paid=true` + data nas compras da fatura |
| Recebimento parcial | Insert genérico funciona | Hook em `financial_transactions` que recalcula `amount_received` da mãe (só se o vídeo mostrar parcial) |
| RPCs `pay_transactions_batch`, `undo_payment_group`, `revert_credit_card_bill_payment` | Sem handler | Só se o vídeo mostrar lote/estorno |
| `list_usable_financial_accounts` | Sem handler | Não precisa (Camila é admin) |
| Bancos | `handlers/ext/brasilapi.com.br.mjs:85-96` devolve 8 bancos **com nomes reais** (Banco do Brasil, Bradesco, Itaú…) e um fictício "COOPERATIVA DE CRÉDITO EXEMPLO" | Usar o fictício ou deixar "Instituição" vazia (plano, decisão 3); conferir o que `www.google.com.mjs` devolve para o favicon (a confirmar) |
| Conciliação / planilha | Sem handlers; upload de arquivo não suportado pelo gravador | Fora do vídeo (proposta) |
| Datas | Fakebase congela com `FAKE_NOW` (`rec/fakebase/core/util.mjs:20-27`); o navegador usa o relógio real | Congelar o navegador (TRILHA, trabalho comum 5): "Este mês", vencidas e a trava de "Pagar Fatura" dependem disso |

---

## 5. Pegadinhas para roteiro e gravação

**[handoff]** = vale pedir correção ao time do app.

1. **[handoff]** "Conta" com dois sentidos lado a lado: "Nova conta" (bancária, Movimentações, `FinanceMovimentacoes.tsx:751-753`)
   e "Nova Conta" (a pagar/receber, `FinanceContas.tsx:1131`; fin `:190`), inclusive com caixa diferente. A fala diz sempre
   "conta bancária" ou "conta a pagar".
2. Dois "Visão Geral" no Financeiro: o item do menu (`/financeiro/relatorio`) e a 1ª aba de "Relatórios" (T20), além de
   "Geral (Todos)" em Movimentações. Câmera no menu ao trocar.
3. O Guia Técnico (1.37.36) promete "Exportar CSV", "Nova Receita" e "Nova Despesa" na Visão Geral e o interruptor
   "Incluir compras no cartão" na lista; nada disso está mais lá (`FinanceOverview.tsx:516-536`;
   `FinanceMovimentacoes.tsx:936-940`). Exportar fica em Movimentações e Contas a Pagar/Receber.
4. "Pagar Fatura" só libera no dia do fechamento ou depois, pelo relógio do navegador (fin `:1286-1287`). O mundo precisa de
   uma fatura já fechada no dia da gravação (plano, Gravação 4).
5. Contas a Pagar/Receber abre na aba **"Todas"** (`FinanceContas.tsx:159`), não em "A Pagar" (o Guia diz o contrário).
6. **[handoff]** O grupo padrão de despesa operacional do DRE chama **"Despesas com pessoal"** e recebe toda categoria OPEX
   (aluguel, combustível) (`supabase/migrations/20261021110000_...:44-49`; `FinanceDRE.tsx:873-879`). No formulário de categoria
   aparece em "Onde aparece no DRE". Para o T13, criar a categoria de exemplo num grupo de custo ("Custos diretos").
7. "Configurações Financeiras" não está no menu: só o botão escuro no topo (`pages/Finance.tsx:325-334`).
8. Selecionar banco mostra logo de banco real (favicon do Google, `hooks/useBrazilBanks.ts:41-50`) e a lista do fakebase
   tem nomes reais. Proposta: "Instituição" vazia ou "Cooperativa de Crédito Exemplo".
9. Recebimento parcial depende de gatilho do banco (4.2); no fakebase, sem hook, a conta não vira "Parcial".
10. Cartão não aparece como opção em "Pago com"/"Caixa / Conta bancária" nem em "Origem/Destino" da transferência
    (`pages/Finance.tsx:145-148`; Changelog 1.24.17 e 1.24.31 `:4119,3761`). Comportamento certo; só não procurar.
11. Excluir conta bancária não apaga lançamentos: eles ficam sem conta (fin `:488-489`). Não encenar.
12. "Nova movimentação" mora em dois lugares: no cartão escuro da Visão Geral e no topo da lista de Movimentações; no
    desktop, "Nova conta"/"Novo cartão" ficam só no rodapé da coluna (`FinanceMovimentacoes.tsx:527-529`).
13. Lançar despesa com "Já foi pago" desligado e sem "Vencimento" vale: vira conta "Sem vencimento" (fin `:242,907`).
14. O "Saldo Após" considera todo o histórico da conta, não só o período filtrado (`FinanceMovimentacoes.tsx:428-437`).
15. **[handoff]** A Visão Geral não tem mais atalho de exportar; quem procurar "Exportar" na primeira tela não acha
    (comportamento, não bug: registrar para o Guia Técnico).

---

## 6. 🚫 Não prometer

- 🚫 Recorrência que "dispara sozinha" todo mês: a conta recorrente grava as 2 a 60 parcelas na hora; parar = excluir as futuras.
- 🚫 Pagar fatura com outro cartão; dar baixa em compra de cartão uma a uma (só pela fatura).
- 🚫 Pagamento parcial de fatura quitando compras.
- 🚫 Tela de BDI no Financeiro (é do T9). 🚫 Subcategoria de subcategoria (máximo 2 níveis).
- 🚫 Exportar CSV na Visão Geral (sumiu).
- 🚫 Conciliação automática com o banco (a conciliação é por arquivo .ofx enviado pela pessoa).
- 🚫 Data de início da DRE editável pela empresa (só aparece se configurada; não há campo na tela, ver T20).

---

## 7. Dúvidas em aberto (só rodando)

1. A fatura vira "Fechada" sozinha pela data do navegador ou depende de algum campo gravado? (`CreditCardInvoiceRow.tsx`)
2. Com o fakebase, "Saldo Após" e "Saldo do dia" batem com os saldos do card (dependem de todas as transações carregadas)?
3. O que o handler `www.google.com.mjs` do fakebase devolve para o favicon do banco (imagem genérica ou erro)?
4. A Visão Geral com só as 12 parcelas do PMOC (a receber) e nenhum realizado mostra os gráficos vazios ou "Sem dados"?
5. Criar categoria pelo "Criar "…"" dentro do lançamento pergunta o grupo do DRE ou usa um padrão?
6. A ordem do T11 já terá lançado alguma receita (OS faturada no T5/T7, orçamento aprovado no T9)? Muda a Visão Geral inicial.

## 8. Termos e pronúncias

| Termo | Na tela | Leitura sugerida |
|---|---|---|
| PIX / Pix | "PIX" | pix |
| CSP | "CSP - Materiais" | cê-ésse-pê (ou "custo do serviço") |
| OPEX | "Despesas Operacionais (OPEX)" | ópex |
| DRE / DFC | "Onde aparece no DRE", "Grupo DFC" | dê érri ê (já em uso) / dê-éfe-cê |
| R$ 1.850,00 | valores | mil oitocentos e cinquenta reais |
| .ofx | "Importar extrato .OFX" | ó-éfe-xis (só se citar) |
