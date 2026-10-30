# Inventário funcional · T20 — Relatório Financeiro e DRE (Dominex)

> Base para o roteiro do tutorial "T20 · Relatório Financeiro e DRE". Levantado em 30/10/2026 contra o código publicado
> `APP_VERSION = "1.38.6"` (`src/config/version.ts:1`), cópia em `/home/claude/domiflix/src-1.38.6`.
> **Análise estática, somente leitura.** "(a confirmar)" = só rodando. Formato do inventário do T3/T12.
> O lado "lançar" (contas, lançamentos, cartão, categorias) está no inventário do T13; aqui só a leitura dos números.

## Como ler

- Caminhos relativos a `src/`, exceto `supabase/...` e `rec/...`. Formato `arquivo:linha`.
- Rótulos entre aspas = texto exato (pt-br). **fin** = `lib/i18n/messages/app/finance.ts` (bloco pt-br `:7-2035`; DRE em
  `:94-183`). Vários textos dos relatórios estão escritos direto nos componentes (citados com a linha).
- "Regime de Caixa" = mês em que o dinheiro entrou/saiu; "Regime de Competência" = mês em que o fato aconteceu
  (fin `:146-158`; `components/financial/TransactionFormDialog.tsx`, dicas de "Data do lançamento" e "Data do pagamento",
  fin `:845,906`).

---

## 0. Resumo para o roteiro

### 0.1 Capítulos da trilha (v1.22.5) contra o código de hoje

| # | Item da trilha | Situação | O que ajustar |
|---|---|---|---|
| 1 | Relatórios → Visão Geral: filtros, indicadores, origem | **Mudou** | Financeiro → **"Relatórios"** abre na aba **"Visão Geral"** ("Visão geral dos relatórios"), com **regime próprio** ("Regime de Caixa", padrão) e cards **"Margem"**, **"Faturamento"**, **"Resultado"** (`components/financial/FinanceReportsOverview.tsx:64,183-238`). |
| 2 | DRE: receita, custos, despesas e resultado | **Maior** | Aba **"DRE - Resultado"**: tabela com códigos (1.01…), grupos configuráveis, "% da receita", comparação de períodos, filtro por centro de custo, "Patrimônio Operacional Atual" e **"Visão do DRE"** (visões próprias, 1.38.4) (`components/financial/FinanceDRE.tsx:1753-1916`; Changelog `:84,682,706,728`). |
| 3 | Caixa × Competência | **Mudou o padrão** | O DRE **abre em "Regime de Competência"** (`FinanceDRE.tsx:182`; Changelog 1.37.24 `:728`). O Guia Técnico (1.37.36) ainda diz Caixa. A Visão Geral e a Análise abrem em Caixa (`FinanceReportsOverview.tsx:64`; `FinanceAnalysis.tsx:71`). |
| 4 | Compra no cartão: compra × pagamento × fatura | **Bate** | Competência = mês da compra; Caixa = mês do pagamento da fatura, só com a fatura quitada inteira (fin `:150-153,1302-1303`). Nunca pelo mês da fatura. |
| 5 | Assinaturas previstas e projeções | **Bate (com o add-on)** | Interruptor **"Incluir projeções"** só em Competência e com Cobranças (`FinanceDRE.tsx:1861-1915`; `FinanceRelatorio.tsx:190`). |
| 6 | DFC: entradas, saídas e variação | **Maior** | Aba **"DFC - Fluxo de Caixa"** com **"Previsto"** (abre nele: próximos 15/30 dias, dia a dia) e **"Realizado"** (atividades operacionais, investimento, financiamento) (`components/financial/FinanceDFC.tsx:116,413-516`; `components/financial/CashFlowForecast.tsx:195-258`). |
| 7 | Pacote para a contabilidade | **Bate, tela nova** | Aba **"Contabilidade"**: **"Pacote para Contabilidade"** "Excel multiabas" → **"Exportar pacote"** (`components/financial/FinanceAccountingPackage.tsx:361-450`). |
| 8 | Exportar CSV e PDF do relatório | **Mudou** | DRE: **"Exportar"** → "Excel"/"PDF" (PDF **baixa direto**, não abre aba, `utils/drePdfGenerator.ts:297-300`). DFC realizado: "Excel", "PDF", "CSV". O "Exportar CSV" da Visão Geral do Financeiro não existe mais (T13). |
| 9 | Checklist mensal de fechamento | **Sem tela** | Conceito: fala + ilustração (plano, cap. 11). |

Novos desde a 1.22.5 sem capítulo na trilha: aba **"Análise"** (comparar períodos e ranking de clientes por margem,
1.36.20, `pages/Changelog.tsx:1266-1286`), **"Grupos do DRE"** em Configurações Financeiras (1.37.24, `:733`) e "Configurar DRE"
com **"Outras visões do DRE"** (1.38.4, `:84`).

Avisos da trilha:

- ⚠️ "Caixa = o que já entrou ou saiu; Competência = mês do fato" → **bate** (dicas e rodapé, fin `:150-157`).
- ⚠️ "Cartão: compra em Competência, pagamento em Caixa, nunca a fatura" → **bate** (fin `:151-153`; T13 3.7).
- ⚠️ "Transferência e pagamento de fatura fora do faturamento e da DRE" → **bate** (`pages/Finance.tsx:212-217`; categorias sem
  grupo DRE em `supabase/migrations/20261020223000_profit_distribution_and_investment_outside_dre.sql:33-34`).
- ⚠️ "Antes de exportar, confira período, regime e filtros" → **bate**: o PDF carimba o regime (Guia T13, cap. 14; `utils/drePdfGenerator.ts`).

### 0.2 O que mudou desde a 1.22.5 (`pages/Changelog.tsx`)

| Versão | Mudança | Linhas |
|---|---|---|
| 1.24.49 | DRE mostra todas as linhas, mesmo zeradas | `:3335` |
| 1.24.61 | DRE não conta subcategoria duas vezes | `:3080` |
| 1.26.0 | Previsão de assinaturas no DRE; centro de custo detalhado | `:2739-2744` |
| 1.27.0 / 1.28.2 | DFC; visão geral própria dos relatórios | `:2631,2712` |
| 1.36.19 / 1.36.20 | DFC previsto dia a dia; % sobre o faturamento; aba Análise; Margem corrigida | `:1266-1323` |
| 1.37.24 / 1.37.25 | DRE abre por competência, códigos, comparação; grupos configuráveis; DFC gerencial | `:706-733` |
| 1.37.27 / 1.37.46 | Grupos recolhíveis; comparativo com atalhos; Excel na ordem da tela | `:299-304,682` |
| 1.38.4 | Visões personalizadas do DRE | `:84` |

### 0.3 O que mais pode surpreender (detalhes na seção 5)

1. **[handoff]** O grupo padrão de despesa operacional se chama **"Despesas com pessoal"** e recebe toda categoria OPEX:
   aluguel e combustível aparecem como "4.01 Despesas com pessoal" no DRE padrão
   (`supabase/migrations/20261021110000_renomeia_grupo_receita_dre.sql:44-49`; `FinanceDRE.tsx:873-879`).
2. Três regimes padrão diferentes: Visão Geral e Análise em Caixa, DRE em Competência. A fala precisa dizer qual está aberto.
3. A "data de início do DRE" que o Guia diz estar "nas configurações da empresa" **não tem campo na tela**: só é lida
   (`company_settings.dre_start_date`, `FinanceDRE.tsx:173-177`; coluna criada em
   `supabase/migrations/20260707120000_dre_start_date_and_reset_company.sql:22-32`).
4. Todos os exports são downloads (DRE PDF/Excel, DFC, pacote): não aparecem no vídeo (TRILHA 6). Mostrar o botão e a
   confirmação.
5. Para os gráficos terem forma, o mundo precisa de meses anteriores com movimento (plano, decisão 1).

---

## 1. Rotas e navegação

| Tela | Como chegar | Rota / componente |
|---|---|---|
| Relatórios | Menu "Financeiro" → **"Relatórios"** | `/financeiro/relatorios` (`lib/i18n/appRouteSlugs.ts:159`) → `pages/Finance.tsx` → `components/financial/FinanceRelatorio.tsx:89-98` |
| Abas | **"Visão Geral"** (padrão), **"DRE - Resultado"**, **"DFC - Fluxo de Caixa"**, **"Contabilidade"**, **"Análise"** | `?tab=visao-geral|dre|dfc|contabilidade|analise` (`FinanceRelatorio.tsx:90-97`; fin `:81-91`) |
| DRE (URL antiga) | `/financeiro/dre` | redireciona para `?tab=dre` (`App.tsx:850`) |
| Grupos do DRE | "Configurações Financeiras" → aba **"Grupos do DRE"** | `?tab=grupos-dre` (`FinanceRelatorio.tsx:105-111`; rótulo fixo em pt-br `:109`) |
| Configurar DRE | Botão **"Configurar DRE"** no cabeçalho escuro da tabela do DRE | `components/financial/DreGroupsManagerDialog.tsx` (`FinanceDRE.tsx:1798-1809,2271-2277`) |

- Período: filtro do topo ("Este mês" por padrão; `pages/Finance.tsx:106`); some na aba "Análise", que tem períodos próprios
  (`pages/Finance.tsx:302-305`).
- Subtítulo do cabeçalho em Relatórios: "Visão geral, DRE e DFC" (fin `:15`).

---

## 2. Permissões e módulos

| Item | Regra | Fonte |
|---|---|---|
| Relatórios | `screen:finance`; Financeiro completo no Essencial; plano Exceção sem o grupo | `hooks/usePermissions.ts:87`; `components/ModuleGateModal.tsx:129-132` |
| Ver totais | `fn:view_finance_totals` | `hooks/usePermissions.ts:112` |
| "Configurar DRE" e aba "Grupos do DRE" | Admin/gestor ou `fn:manage_settings` (`useCanManageFinanceSettings`) | `FinanceDRE.tsx:1798`; `hooks/useCanManageFinanceSettings.ts:15-18` |
| Visões do DRE (criar/publicar) | Servidor confere empresa e permissão (`_assert_dre_company_access`, `_assert_dre_manage_permission`) | `supabase/migrations/20261030120000_dre_layouts_versionados.sql:508-626` |
| 🔒 "Incluir projeções" | Só com o add-on `cobrancas` e em Competência | `FinanceRelatorio.tsx:190`; `FinanceDRE.tsx:1861` |

---

## 3. Por tela

### 3.1 Visão Geral dos relatórios (`FinanceReportsOverview.tsx:183-310`)

- Título **"Visão geral dos relatórios"** / "Usa os regimes e o corte histórico do DRE, sem incluir projeções de assinaturas.".
- Abas de regime **"Regime de Caixa"** (padrão, `:64`) / **"Regime de Competência"** (`:192-214`).
- Cards **"Margem"**, **"Faturamento"**, **"Resultado"** (`:217-238`).
- **"Receita × despesa"** (áreas mês a mês; vazio "Registre receitas ou despesas para acompanhar a evolução do período.") (`:240-273`).
- Interruptor **"Somar subcategorias na categoria principal"** (só se houver subcategoria) (`:275-287`).
- **"Receitas por categoria"** e **"Despesas por categoria"** (`:289-292`); **"Receita e despesa por centro de custo"** (vazio "Os
  centros de custo usados nos lançamentos aparecerão aqui.") (`:294-310`).

### 3.2 DRE - Resultado (`FinanceDRE.tsx`; fin `:94-183`)

- Topo: cards **"Margem"**, **"Receita Líq."**, **"Resultado Líq."** e gráfico **"Evolução Receita × Despesas"** (fin `:95-105`).
- Filtro **"Filtros"** → "Centro de custo" (só quando há centros) (`:1758-1772`).
- Cabeçalho escuro **"Demonstrativo de Resultado (DRE)"** (`:1776-1916`): seletor **"Visão do DRE"** ("DRE padrão" + visões
  publicadas; só aparece com alguma visão, `:1782-1797`), **"Configurar DRE"** (`:1798-1809`), botões **"Regime de Caixa"** /
  **"Regime de Competência"** com dicas (`:1810-1860`; fin `:150-153`), **"Incluir projeções"** (`:1861-1876`) e **"Exportar"** →
  "Excel" / "PDF" ("Exportando...") (`:1877-1898`).
- Linhas (fin `:111-127`): "(+) Receita Bruta", "(-) Impostos e Deduções", "(=) Receita Líquida", "(-) Custo dos Serviços
  Prestados (CSP)", "(=) Lucro Bruto" + "Margem", "(-) Despesas Operacionais (OPEX)", "(=) Resultado Líquido",
  "(-) Despesas Não Operacionais" (dica "Juros, multas, perdas eventuais…"), "(=) Resultado Final"; selos "Superávit",
  "Déficit", "Equilibrado"; coluna "% da receita". Grupo vazio: "Nenhum lançamento nesta seção no período selecionado.".
- Cada grande grupo mostra subgrupos com código (ex. "4.01") e as categorias; abre por subcategoria e por centro de custo
  ("Por centro de custo", "Sem centro de custo"; "Lançado direto em {categoria}") (fin `:176-182`; `FinanceDRE.tsx:849-889`).
- **"Comparar períodos"** (`components/financial/DreHierarchyTable.tsx:215`) → janela **"Comparar períodos"**: "Período principal",
  "Comparar com" ("Período anterior" — "Mesmo número de dias, imediatamente antes"; "Mesmo período no ano passado";
  "Outro período"), "Períodos adicionados", "Cancelar" / **"Aplicar comparação"** (`DreComparisonDialog.tsx:146-154,229-432`).
- Card **"Patrimônio Operacional Atual"** / "Foto atual da operação; não acompanha o período selecionado no DRE e não
  substitui um balanço contábil." ("Saldo em caixa (dinheiro)", "Saldo bancário", "Contas a receber", "Estoque (projeção de
  venda)", "Contas a pagar", "Inclui R$ … em faturas de cartão") (fin `:162-175`; `FinanceDRE.tsx:1402-1416,1968`).
- Rodapé (`:2278-2287`): "\* Regime de Caixa: cada lançamento entra no mês em que o dinheiro entrou ou saiu da conta. Só aparece
  o que já foi pago ou recebido." ou "\* Regime de Competência: cada lançamento entra no mês em que aconteceu, pago ou não."
  + "\* O DRE é classificado automaticamente com base no campo "Grupo DRE" de cada categoria financeira…" (fin `:143-157`);
  com projeções: "Inclui R$ … de assinaturas identificadas como previstas; nenhuma transação foi criada."; com data de corte:
  "DRE contabilizado a partir de dd/mm/aaaa.".
- Projeções (`:1901-1915`): "n ciclo(s) previsto(s) · R$ …", "Nenhum ciclo futuro de assinatura neste período.", "Selecione um
  período com data final para calcular assinaturas futuras.".
- Fora do DRE: transferências, pagamento de fatura, "Ajuste de saldo", categorias em "Excluídos do DRE" (aporte, distribuição,
  aplicação/resgate, ativos, empréstimos) (`supabase/migrations/20261020223000_...:28-42`; T13 3.6).

### 3.3 Configurar DRE e Grupos do DRE (`DreGroupsManagerDialog.tsx`)

- Janela **"Configurar DRE"**: "Organize os grupos e mova categorias arrastando. Use o seletor como alternativa acessível.";
  bloco **"Outras visões do DRE"** / "Crie formas diferentes de apresentar os mesmos lançamentos e categorias." ("Precisa de
  outra forma de ver o DRE?", "Ver exemplo em PDF"; `components/financial-report/DreLayoutProfilesPanel.tsx`).
- **"Estrutura da DRE"**, **"Novo subgrupo"**, "Prévia da estrutura", "Nome", "Inativo"; naturezas: "Receita" ("Soma na receita
  bruta antes das deduções."), "Dedução da receita", "Custo", "Despesa operacional", "Não operacional", "Fora da DRE" ("Não
  entra nos cálculos nem nos totais da DRE.") (`:86-112,346-404`).
- Proteções: "Grupo essencial: não pode ser desativado nem excluído.", "Desative o grupo antes de excluí-lo.", "Reordene grupos
  apenas dentro da mesma natureza da DRE.", "Excluir grupo da DRE?" (`:290,430,535,582`).
- Grupos que toda empresa já tem: "Receitas de serviços", "Impostos sobre vendas", "Custos diretos", **"Despesas com
  pessoal"**, "Resultado financeiro", "Excluídos do DRE" (`supabase/migrations/20261021110000_...:35-50`).

### 3.4 DFC - Fluxo de Caixa

- Botões **"Previsto"** (padrão) / **"Realizado"** (`FinanceDFC.tsx:116,413-430`).
- **Previsto** (`CashFlowForecast.tsx:195-258`): cards **"Saldo atual"**, **"A receber · 15 dias"**, **"A pagar · 15 dias"**,
  **"Dívidas a receber"**, **"Dívidas a pagar"**; alerta "A conta X fica negativa em dd/mm." / "O saldo somado pode parecer
  saudável, mas o dinheiro não está na conta que vai ser debitada."; aviso de "Sem conta definida"; **"Próximos"** "15 dias" /
  "30 dias"; matriz dia a dia ("Saldo inicial", "Recebimentos", "Total de saídas" recolhível, "Saldo final", coluna "Dívida",
  saldo por "Conta"); clicar num valor abre a lista "Movimentações" e "Total do dia" (`:93-160,247-551`). Erro: "Não foi possível
  carregar o fluxo de caixa previsto" (`:181-183`).
- **Realizado** (`FinanceDFC.tsx:441-606`): cards **"Saldo inicial"**, **"Variação líquida"**, **"Saldo final"**; "Filtros" →
  "Centros de custo" ("Filtro aplicado ao realizado e às exportações."); atividades (operacionais, investimento, financiamento,
  pelo "Grupo DFC" da categoria); **"Exportar"** → "Excel", "PDF", "CSV" (`:504-516`); vazio "Nenhuma movimentação realizada no período".

### 3.5 Contabilidade (`FinanceAccountingPackage.tsx:361-450`)

- Faixa escura **"Pacote para Contabilidade"** + selo **"Excel multiabas"** / "Reúna em um único arquivo os dados financeiros
  necessários para conferência e fechamento com seu contador." / "Período selecionado: …".
- Botão **"Exportar pacote"** ("Carregando dados...", "Gerando pacote...") → toast **"Pacote para Contabilidade exportado!"** ou
  "Não foi possível gerar o pacote" (`:348-352`).
- Quatro cartões do que vai no arquivo: **"Lançamentos completos"**, **"DRE e DFC reconciliados"** ("DRE em Caixa e Competência,
  além do DFC realizado por atividade."), **"Saldos e obrigações"**, **"Plano gerencial"** (`:361-365`).
- Erro: "Não foi possível preparar o pacote para Contabilidade" / "A exportação foi bloqueada para impedir a geração de um
  arquivo parcial ou inconsistente.".

### 3.6 Análise (`FinanceAnalysis.tsx`)

- Título **"Análise"**; regime ("Regime de Caixa" padrão, `:71`) com as frases "Caixa considera somente valores realizados pela
  data da baixa." / "Competência considera a data em que a receita ou despesa aconteceu, mesmo sem baixa." (`:422-423`).
- Agrupamento **"Mês a mês"**, **"Trimestre"**, "Ano"; quantos períodos comparar (`:52-58,214-224`); gráfico "Receitas",
  "Despesas", "Resultado"; tabela "Período", "Receitas", "Despesas", "Resultado", "Variação" (`:249-263`).
- Ranking de clientes: **"Maior faturamento"** / **"Melhor margem"**, **"Top 5"**, "Top 10", "Top 25"; colunas "Cliente",
  "Faturamento", "Custo direto", "Sobra", "Margem"; vazio "Vincule o cliente nas receitas para ver o ranking e a margem de cada
  um." (`:314-348`).

### 3.7 Onde cada lançamento do mundo aparece (base para a fala dos caps. 3 e 4)

Regras do motor (`lib/dre-regime.ts:26-31,79-81`; `FinanceDRE.tsx:340-361`): em **Caixa** a data é `paid_date` (só o que foi
pago/recebido); em **Competência** é `transaction_date` ("Data do lançamento"), pago ou não. Saem do DRE nos dois regimes:
par de transferência/pagamento de fatura (`transfer_pair_id`, `:344`), categoria "Ajuste de saldo" (`:350`) e grupo "Excluídos
do DRE" (`:347`). Em Competência também saem as filhas "Recebimento parcial" (a mãe já conta inteira) e o vale de salário
(`:355,361`).

| Lançamento (T13/T19) | Regime de Competência | Regime de Caixa |
|---|---|---|
| Receita "Instalação de split…" recebida no dia | Mês do lançamento | Mesmo mês (data do recebimento) |
| Despesa "Gás R-410A…" (lançada a pagar, paga depois) | Mês do lançamento, mesmo antes de pagar | Só no mês em que foi paga |
| Compra no cartão em 3x | Cada parcela no mês da sua data, mês a mês a partir da compra (`hooks/useFinancial.ts:126-151`) | Só quando a fatura daquela parcela é quitada inteira, com a data do pagamento (`supabase/migrations/20260904130000_dre_pagar_fatura_quita_compras.sql`; fin `:1302-1303`) |
| Pagamento da fatura e transferência | Fora | Fora |
| Aluguel recorrente (12x a pagar) | Cada mês pela data de cada parcela | Só as pagas |
| Cobrança Asaas paga (T19) | Data de criação da cobrança ("a receita entra em {data}, o dia de hoje", `lib/i18n/messages/app/charges.ts:174`) | Data do pagamento informada pelo Asaas |
| Taxa da Asaas / tarifa de maquininha | Categoria "Tarifas e Taxas", grupo de impostos → linha "(-) Impostos e Deduções" (`supabase/migrations/20261020223000_...:29`; "deduzida da receita líquida no DRE", fin `:1472`) | Idem, na data da baixa |
| Ajuste de saldo | Fora | Fora |

---

## 4. Backend por tela

### 4.1 Chamadas

| Onde | Chamada | Fonte |
|---|---|---|
| Todas as abas | `financial_transactions` com filhas (tarifa, recebimento parcial) — o DRE/DFC usam `transactionsWithChildren` | `pages/Finance.tsx:122-130,367-386` |
| Categorias e grupos | `financial_categories`, `dre_groups` | `hooks/useFinancialCategories.ts:80`; `hooks/useDreGroups.ts` |
| Visões do DRE | RPC `get_company_dre_configuration {p_company_id}` + `create_dre_layout_draft`, `publish_dre_layout`… e tabelas `dre_layout_*` | `hooks/useDreLayoutProfiles.ts:124-253`; `supabase/migrations/20261030120000_...:12-207,1405-1412` |
| Patrimônio | `useOperationalPatrimony` (contas, contas a receber/pagar, estoque) | `FinanceDRE.tsx:164` |
| Projeções de assinaturas | `tenant_subscriptions`, `tenant_charges` | `hooks/useDreSubscriptionProjections.ts` |
| Data de corte | `company_settings.dre_start_date` (só leitura) | `FinanceDRE.tsx:173-177` |
| DFC previsto | RPC `cash_flow_opening_balances {p_today}` → `[{account_id, balance}]` + `financial_transactions` | `hooks/useCashFlowForecast.ts`; `supabase/migrations/20261018230000_fluxo_de_caixa_previsto_base.sql:253-270` |
| Exports | Gerados no navegador (PDF `jsPDF` → `save()`, Excel) | `utils/drePdfGenerator.ts:297-300`; `FinanceDFC.tsx:369`; `FinanceAccountingPackage.tsx` |

### 4.2 Comparação com o backend falso (`/home/claude/domiflix/rec/fakebase`)

| Item | Hoje | Falta |
|---|---|---|
| `financial_transactions`, `financial_categories`, `dre_groups` | No schema, sem seed | Histórico fictício de meses anteriores (plano, decisão 1) + categorias/grupos do T13 |
| RPC `cash_flow_opening_balances` | **Sem handler** (devolve `[]`): "Saldo atual" sairia zerado ou a projeção some (a confirmar) | Handler: saldo por conta caixa/banco = inicial + entradas pagas − saídas pagas até `p_today` |
| RPC `get_company_dre_configuration` e tabelas `dre_layout_*` | **Fora do schema** (`rec/fakebase/schema.json` não tem as tabelas da 1.38.4) → RPC devolve nulo; o seletor "Visão do DRE" não aparece | Nada, se o vídeo não mostrar visões próprias; senão regenerar o schema e fazer handlers |
| `company_settings.dre_start_date` | Nulo no seed | Manter nulo (sem rodapé de corte) |
| Projeções | Dependem de `tenant_subscriptions` do T19 | Só com a assinatura do T19 no estado inicial |
| Downloads | `acceptDownloads: false` no gravador (`rec/recorder/browser.mjs:131`, conforme o T12) | Só mostrar botão e toast |

---

## 5. Pegadinhas para roteiro e gravação

**[handoff]** = vale pedir correção ao time do app.

1. **[handoff]** Subgrupo padrão "Despesas com pessoal" recebe toda despesa operacional (aluguel, combustível, ferramentas),
   inclusive no DRE padrão (`FinanceDRE.tsx:873-879`). Sem ajuste, o vídeo mostraria "Aluguel" dentro de "Despesas com pessoal".
2. **[handoff]** Regimes padrão diferentes entre abas (Caixa na Visão Geral e na Análise, Competência no DRE), e o Guia Técnico
   ainda diz que o DRE abre em Caixa. Na gravação, clicar explicitamente no regime a cada aba.
3. **[handoff]** O Guia Técnico promete a "data de início do DRE nas configurações da empresa"; não há campo na tela
   (`FinanceDRE.tsx:173-177`). Não citar.
4. O PDF do DRE agora **baixa** (`utils/drePdfGenerator.ts:300`), não abre aba com "Imprimir / Salvar PDF" (Guia desatualizado).
5. "Incluir projeções" só aparece em Competência e com o add-on; troca de regime faz o interruptor sumir (`FinanceDRE.tsx:1861`).
6. A aba "Análise" ignora o filtro de período do topo (o filtro some) (`pages/Finance.tsx:302-305`).
7. "Grupos do DRE" (Configurações Financeiras) e "Configurar DRE" (no DRE) abrem a mesma configuração por dois caminhos.
8. O rótulo da aba "Grupos do DRE" está fixo em português (`FinanceRelatorio.tsx:109`) — só importa em outros idiomas.
9. Compra no cartão em Regime de Caixa só aparece depois da fatura quitada **inteira** (fin `:1302-1303`); fatura parcial deixa
   a compra fora. No mundo do T13 a fatura foi paga inteira.
10. Ranking da Análise depende de "Cliente vinculado" nas receitas e "custo direto" lançado com cliente; lançamentos sem cliente
    viram "despesas sem cliente" fora do ranking.
11. DFC previsto conta tudo como pago no vencimento e põe o vencido na coluna "Dívida" sem descontar do saldo (Guia T13 cap. 18;
    `CashFlowForecast.tsx:199-200,269`). Fala precisa explicar a "Dívida".
12. "% da receita" com receita zero no período mostra "Base zero" na comparação (fin `:141`).
13. **[handoff]** Textos discordam sobre a taxa do gateway: o lançamento parcelado no cartão diz "A taxa entra como despesa
    financeira, ela não diminui a receita." (fin `:892`), mas a categoria "Tarifas e Taxas" é do grupo de impostos e cai em
    "(-) Impostos e Deduções", que reduz a Receita Líquida (`supabase/migrations/20261020223000_...:29`; fin `:1472`). A fala do
    T20 segue a tabela (dedução); o texto do formulário precisa de ajuste.

---

## 6. 🚫 Não prometer

- 🚫 Data de início do DRE configurável pela empresa (sem campo na tela).
- 🚫 Balanço patrimonial contábil, depreciação, livro de imobilizado (o "Patrimônio Operacional Atual" diz que não substitui).
- 🚫 PDF do DRE abrindo em nova aba com botão de imprimir (hoje baixa o arquivo).
- 🚫 Projeção de assinaturas sem o add-on Cobranças ou em Regime de Caixa.
- 🚫 Ganho/perda automático na venda de ativo; separar sozinho principal e juros de empréstimo.
- 🚫 Exportar CSV na Visão Geral do Financeiro.

---

## 7. Dúvidas em aberto (só rodando)

1. Sem handler de `cash_flow_opening_balances`, o DFC previsto mostra "Saldo atual" zero ou o erro "Não foi possível carregar o
   fluxo de caixa previsto"?
2. O gráfico "Evolução Receita × Despesas" usa os últimos 6 meses do período ou do ano? (precisa de quantos meses de histórico)
3. Renomear "Despesas com pessoal" para outro nome muda o rótulo no DRE padrão na hora (o mapa de nomes antigos só troca os
   nomes canônicos antigos, `FinanceDRE.tsx:873-879`)?
4. A janela "Configurar DRE" sem as tabelas `dre_layout_*` no fakebase abre normal ou mostra erro no bloco "Outras visões"?
5. "Exportar pacote" dispara o toast de sucesso mesmo com o download bloqueado no gravador?

## 8. Termos e pronúncias

| Termo | Na tela | Leitura sugerida |
|---|---|---|
| DRE | "DRE - Resultado" | dê érri ê (já em uso) |
| DFC | "DFC - Fluxo de Caixa" | dê-éfe-cê |
| CSP | "(-) Custo dos Serviços Prestados (CSP)" | cê-ésse-pê |
| OPEX | "(-) Despesas Operacionais (OPEX)" | ópex |
| EBITDA | (Guia antigo; a tela diz "Resultado Líq.") | não usar |
| Receita Líq. / Resultado Líq. | cards | receita líquida / resultado líquido |
| (+) (−) (=) | linhas do DRE | não ler os sinais |
| Excel / PDF / CSV | "Exportar" | éxcel / pê-dê-éfe / cê-ésse-vê |
