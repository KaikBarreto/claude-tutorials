# Inventário · T15 · Relatório Financeiro e DRE (EcoSistema 1.59.154)

Código lido: `/home/claude/ecoflix/app-src-1.59.154/` (`APP_VERSION = "1.59.154"`, `src/config/version.ts:16`). Análise estática,
só leitura. Caminhos relativos a `src/`. Só o que a aula usa. O SQL das RPCs não está na cópia (sem `supabase/migrations`):
o que depende dele vem marcado "(regra no servidor)" e vira `[BACKEND: ...]` no roteiro.

## 0. Código × fonte (vale o código)
1. **Cinco abas**, não quatro: "Dashboard", "DRE", "DFC", "Centros de Custo", "Histórico" (`pages/FinancialReport.tsx:612-618`).
   A fonte não fala da DFC; a aula mostra as cinco na tela e não entra na DFC (dúvida para o Kaik).
2. Categorias: os títulos são "Categorias de receita" e "Categorias de despesa", o botão é "Nova", e a janela se chama
   "Nova categoria" (`components/financial/FinancialCategoriesManager.tsx:326-333`, `FinancialCategoryFormDialog.tsx:196`).
   A ajuda do app ("Categorias de Entrada", "Nova Categoria", etiqueta "Sistema") está desatualizada: categoria do sistema
   tem só um cadeado e não tem "Excluir" (`FinancialCategoriesManager.tsx:221-226,269`).
3. No DRE, o botão do cabeçalho é "Organizar categorias" (a ajuda diz "Configurar DRE") (`FinancialDRE.tsx:1421-1434`).
4. O menu chama o extrato do caixa de "Histórico do Caixa" (`config/routes.ts:419`), não "Histórico de Transações do Caixa".
5. O DRE abre em "Regime de Competência" (`FinancialReport.tsx:91`), e o regime vale também para o banner do Dashboard
   (mesmo estado).

## 1. Categorias Financeiras · `/categorias-financeiras`
Menu "Financeiro" → "Categorias Financeiras" (`config/routes.ts:415-424`). Tela `pages/FinancialCategories.tsx`.
- Cabeçalho: "Categorias Financeiras", "Gerencie as categorias de receitas e despesas"; ajuda: "Crie categorias para
  classificar suas receitas e despesas. Isso permite montar o Demonstrativo de Resultado (DRE) e analisar onde seu dinheiro
  está sendo aplicado." (`:45-50`; `i18n/locales/pt-BR/financial.json`).
- Menu lateral da tela: "Categorias", "Centros de custo", "Grupos do DRE" (`:21-25`).
- Lista (`components/financial/FinancialCategoriesManager.tsx`): "Categorias de receita" e "Categorias de despesa", cada uma
  com "Nova" e "N categorias · arraste para reordenar" (`:326-333`). Na janela de 1280 px as duas seções ficam uma embaixo da
  outra (lado a lado só a partir de 1500 px, `:384`). Despesas separadas por grupo do DRE quando há 2 ou mais grupos, com
  divisória em maiúsculas e a contagem (`:301-308,344-354`; rótulos em `lib/dreGroups.ts`). Cartão: cor e ícone, nome,
  cadeado se for do sistema, "1 subcategoria" (`:265-283`); três pontos "Ações de <nome>" → "Editar", "Adicionar
  subcategoria" (só na principal), "Tornar principal" (só na sub), "Excluir" (não aparece nas do sistema) (`:200-229`).
  Sub em grupo diferente do pai: selo com o grupo dela e a nota "Subcategorias podem pertencer a outro grupo DRE; o
  lançamento segue sempre o grupo da própria subcategoria." (`:273-277,290-294`). Depois de criar uma subcategoria, o cartão
  do pai abre sozinho (`:110`).
- Janela (`components/financial/FinancialCategoryFormDialog.tsx`): título "Nova categoria" / "Nova subcategoria" /
  "Editar categoria" (`:196`), "Defina como os lançamentos desta categoria aparecem no DRE e no fluxo de caixa." (`:197`);
  "Nome" ("Ex.: Fretes, salários, tributos") (`:214-219`); "Categoria principal" (só se houver principal do mesmo tipo;
  "Nenhuma — categoria principal"; na sub: "A subcategoria herda os dados do pai como ponto de partida, mas pode ter grupo
  DRE próprio.") (`:227-246`); "Tipo" ("Receita"/"Despesa", travado na sub) (`:249-262`); "Onde aparece no DRE" ("Escolha
  pelo efeito financeiro. A prévia abaixo mostra a posição no modelo padrão.") com os grupos e a descrição de cada um
  (`:264-290`); prévia "Prévia no DRE padrão" · "Sem alterar lançamentos", o grupo, o nome, "− valor"/"informativo" e "No
  padrão atual, <efeito>." (`:37-91`); "Grupo no Fluxo de Caixa (DFC)" com a descrição embaixo (`:298-312`); "Cor" (botões
  "Usar cor #XXXXXX") (`:314-328`); "Ícone" (`:330-333`); "Cancelar" / "Criar categoria" (`:200-210`). Erros: "Informe o
  nome da categoria." e "Já existe uma categoria deste tipo com esse nome." (`:165-180`). Toast "Categoria criada" (`:108`).
- Grupos do DRE (`lib/dreGroups.ts`): "Impostos e deduções" ("Reduz a receita no demonstrativo."), "Custos adicionais"
  ("Soma ao custo de compra do material ou ao CMV."), "Despesas operacionais (OPEX)" ("Entra depois do lucro bruto como
  despesa operacional."), "Receitas/despesas não operacionais", "Não compõe o DRE" ("Movimentação patrimonial: aparece no
  caixa, mas não no DRE."). Efeito na prévia (`FinancialCategoryFormDialog.tsx:29-35`): "reduz a receita", "reduz o lucro
  bruto", "reduz o resultado operacional", "reduz o resultado final", "não altera o resultado".
- Grupos da DFC (`lib/cashFlowGroups.ts`): "Atividades operacionais", "Atividades de investimento" ("Compra ou venda de
  máquinas, veículos e outros ativos."), "Atividades de financiamento" ("Empréstimos, amortizações, aportes e retiradas de
  sócios."), "Não compõe a DFC".
- Backend: `financial_categories` (select `id, name, type, color, icon, is_system, dre_group, cash_flow_group, parent_id,
  sort_order`, `hooks/useFinancialCategories.ts:52`; insert/update/delete, `FinancialCategoriesManager.tsx:87-134`). O DRE
  hierárquico lê `dre_group_id` e `dre_groups` (`hooks/useDreConfiguration.ts:55-70`): o vínculo `dre_group` → `dre_group_id`
  é feito no banco (regra no servidor).

## 2. Centros de custo · mesma rota, item "Centros de custo"
`components/financial/CostCentersManager.tsx`.
- "Centros de custo", "Agrupe receitas e despesas por setor para saber quanto cada área gasta. É opcional em cada
  lançamento." (`:144-151`); botão "Novo centro de custo" (`:154-163`); lista em ordem alfabética, ativos primeiro, inativo
  esmaecido com "Inativo" (`:62-65,190-239`); lápis "Editar centro de custo" e lixeira "Excluir centro de custo"
  (`:217-234`).
- Janela "Novo centro de custo", "Defina um nome e uma cor para identificar o setor nos lançamentos." (`:242-246`): "Nome *"
  ("Ex: Produção, Administrativo, Frota"), "Cor" (botões "Cor #XXXXXX"), "Ícone (opcional)", "Descrição" ("Descrição
  opcional"), interruptor "Ativo" ("Centros inativos deixam de aparecer nos formulários de lançamento, mas seguem nos
  lançamentos antigos.") (`:268-333`); "Cancelar" / "Salvar" ("Salvando...") (`:247-266`). Toast "Centro de custo criado"
  (`:121`). Excluir: "Excluir centro de custo <nome>?" e "Os lançamentos que usavam este centro de custo ficarão SEM centro de
  custo (não serão apagados)." (`:337-361`).
- O campo "Centro de custo" aparece na despesa do caixa (`components/WithdrawalModal.tsx:877`), na receita, no lançamento
  bancário e na conta a pagar/receber (`components/contas/BillFormModal.tsx`).
- Backend: `cost_centers` (select/insert/update/delete, `hooks/useCostCenters.ts:40-90`).

## 3. Relatório Financeiro · `/relatorio-financeiro`
Menu "Financeiro" → "Relatório Financeiro" (`config/routes.ts:422`). `pages/FinancialReport.tsx`.
- "Relatório Financeiro", "Visão completa das finanças do seu negócio" (`:851-855`); filtro de período (`:856-863`;
  `components/DateRangeFilter.tsx:426-449`): "Todos os tempos", "Hoje", "Últimos 7 dias", "Este mês", "Mês passado",
  "Últimos 30 dias", "Este ano", "Personalizado" (`i18n/locales/pt-BR/common.json:2-10`). Abre sempre em "Este mês"
  (`:88`); a aba aberta fica guardada no navegador (`localStorage` "financial-report-tab", `:97-108`).
- Abas sublinhadas: "Dashboard", "DRE", "DFC", "Centros de Custo", "Histórico" (`:612-618,886-894`).
- Sem a permissão "Ver Totais e Valores Financeiros" (`action_view_financial_values`, `config/routes.ts:237`): "Acesso
  Restrito", "Você não tem permissão para visualizar os totais, DRE e gráficos financeiros. Entre em contato com o
  administrador para solicitar acesso." (`:866-884`). A permissão se dá em "Usuários e Permissões".

### 3.1 Aba "Dashboard"
- Banner "Resultado do Período", valor, "Superávit" / "Déficit" / "Equilibrado"; verde, vermelho ou escuro
  (`components/financial-report/ResultBanner.tsx:58-88`). Mesmo número do fim do DRE (`FinancialReport.tsx:532-539,806`).
- "Despesas por Categoria" (só as despesas operacionais, `FinancialReport.tsx:813`), rosca, "Total: R$ ..." em vermelho,
  lista da maior para a menor; vazio "Nenhuma despesa no período" (`ExpenseBreakdown.tsx:128-151`). "Receitas por Categoria"
  (receitas lançadas com categoria, sem as vendas), "Total: R$ ..." em verde; vazio "Nenhuma receita categorizada no período"
  (`RevenueBreakdown.tsx:73-96`).
- `OperationalInsights.tsx`: cartões "Ticket Médio Compra" (vermelho) e "Ticket Médio Venda" (verde) (`:397-429`); "Top
  Fornecedores" e "Top Clientes" com o alternador "R$" / "Kg" e "Ver todos" (`:255-372,434-458`); "Materiais + Comprados" e
  "Materiais + Vendidos", cinco primeiros, com "N kg" embaixo do nome (`:177-250,460-480`); vazio "Sem compras no período" /
  "Sem vendas no período"; sem parceiro: "Não informado" (`:152-155`).

### 3.2 Aba "Centros de Custo"
`CostCenterAnalysis.tsx`: cartões "Receitas financeiras", "Despesas financeiras", "Resultado das movimentações",
"Cobertura por centro de custo" (`:349-381`); "Receitas x despesas por centro" ("Clique em uma coluna para detalhar o
centro.") (`:384-421`); "Distribuição das despesas" (`:423-467`); "Ranking dos centros de custo" (colunas "Centro de custo",
"Receitas", "Despesas", "Resultado", "Participação"; botão "Movimentações"; "Sem centro de custo" com "Não classificado")
(`:470-539`); aviso azul "Esta visão considera receitas, despesas e impostos que já possuem dimensão financeira. Vendas e
compras de pedidos ainda não possuem centro de custo e, por isso, não entram nestes totais." (`:587-594`). Entram as
despesas operacionais e os impostos (`FinancialReport.tsx:787-798`). Vazio: "Nenhuma movimentação por centro de custo no
período" (`:330-344`).

### 3.3 Aba "DRE"
`FinancialDRE.tsx` (modo hierárquico, `FinancialReport.tsx:664-708`).
- Cabeçalho escuro "Demonstrativo Financeiro (DRE)" (`:1316-1333`); botões "Regime de Caixa" e "Regime de Competência"
  (`:1358-1413`) com as dicas: Caixa "Considera todo o dinheiro que entrou e saiu no período. Mostra sua situação de caixa,
  mas o material que você comprou e ainda está no estoque conta como custo agora, mesmo sem ter sido vendido." e Competência
  "Considera só o custo do material que você realmente vendeu no período. O que está parado no estoque não abate o lucro até
  ser vendido. É o lucro contábil do negócio." (`:1381-1410`); "Organizar categorias" (`:1421-1434`); "Exportar" →
  "Planilha Excel" / "Documento PDF" ("Exportando..."; os dois baixam arquivo: `utils/dreExcelGenerator.ts:719`,
  `utils/drePdfGenerator.ts:300`) (`:1435-1463`).
- Faixas: em caixa, "O detalhamento por centro de custo fica disponível no regime de competência, cuja data contábil é
  compatível com os lançamentos categorizados." (`:1491-1495`); em competência com estoque sem custo, "Há material em estoque
  sem custo de compra cadastrado — o CMV pode estar subestimado." (`:1485-1490`).
- Tabela (`DreHierarchyTable.tsx`, `lib/dreHierarchy.ts:92-98,206-209,313-315`): cabeçalho "Estrutura do DRE", "Comparar
  períodos", coluna "<Mês de ano>" com "Valor · % receita" (`:199-227`); seções "01 (+) Receita Bruta", "02 (-) Impostos e
  Deduções", "04 (-) Custos Operacionais", "06 (-) Despesas Operacionais", "07 (-) Outras Receitas e Despesas" (abertas;
  clique fecha); grupos fechados (clique abre as categorias); linhas fixas "Vendas" (01) e "CMV / Compras de materiais" (04:
  CMV em competência, compras em caixa, `lib/dreSummary.ts:124-131`); resultados "03 = Receita Líquida", "05 = Lucro Bruto",
  "08 = Resultado do Período" (verde se positivo, vermelho se negativo, `:174-196`). Categoria em "Não compõe o DRE" não entra.
  As linhas da comparação casam pelo nome da categoria (`lib/dreHierarchy.ts:152-170`).
- Faixa "Patrimônio Operacional Atual" (fechada; clique abre), ícone "Exportar Patrimônio" (abre aba nova,
  `utils/financialDreHtmlGenerator.ts:872`) (`FinancialDRE.tsx:1818-1843`); linhas "Saldo em Caixa (Dinheiro)", "Saldo
  Bancário" (só quem gerencia contas bancárias), "Contas a Receber", "Estoque (Projeção de Venda)", "Contas a Pagar" (em
  vermelho, subtrai); total "= Patrimônio Operacional Atual" com "Positivo" / "Negativo" / "Equilibrado" (`:1845-1937`). Não
  depende do período (`FinancialReport.tsx:240-273`).
- "Comparar períodos" (`DreComparisonDialog.tsx`): "Comparar períodos", "Defina o período principal e escolha até três
  referências para comparar lado a lado." (`:221-224`); "Período principal" (`:233-239`); "Comparar com": "Período anterior"
  ("Mesmo número de dias, imediatamente antes"), "Mesmo período no ano passado", "Outro período" (`:135-150,268-313`);
  "Prévia das colunas" (`:383-384`); "Remover comparações", "Cancelar", "Aplicar comparação" (`:419-424`). Outubro inteiro →
  "Período anterior" = setembro inteiro (`lib/dreComparisonPeriod.ts:50-57`).
- "Evolução Mensal" (`MonthlyEvolution.tsx:552-558`): gráfico com "Vendas", "Compras", "Resultado", "Margem Bruta %"
  (`:403-433`); tabela "Mês", "Vendas", "Compras", "Margem", "Resultado" (`:445-478`); meses abreviados ("out/26"). Seis
  meses, sem depender do filtro (`FinancialReport.tsx:295-302`).

### 3.4 Aba "Histórico"
`RevenueExpenseList.tsx`.
- Abas "Receitas" (vendas + receitas lançadas), "Despesas", "Compras", com contador (`:317-342`); abre em "Receitas"
  (`:244`).
- Busca "Buscar por descrição, categoria ou valor..." (`:695-697`); "Exportar" → "Exportar histórico": "PDF", "Excel";
  "Fechamento contábil": "Fechamento completo (Excel)" (`:704-747`); "Filtros" (painel à direita): "Categoria",
  "Cliente/Fornecedor", "Centro de custo", "Fonte"; "Limpar filtros", "Aplicar" (`:750-918`).
- Barra "N lançamentos" e o total (vermelho com "-" nas despesas) (`:941-964`). Linha: descrição, "dd/MM/aaaa HH:mm", selo
  "Compra"/"Venda"/"Caixa"/"Banco" (`lib/historicoFilters.ts:172-177`), selo da categoria, valor; clipe "Ver detalhes e
  anexos" (caixa/banco), lápis "Editar categoria" (caixa/banco), lixeira "Excluir lançamento" (só despesa de banco e só para
  quem gerencia contas bancárias) (`:1017-1158`). Rodapé "Exibir 10 por página", "1 de N" (`:1225-1266`). Vazio: "Nenhum
  lançamento no período" / "Nenhum resultado encontrado com os filtros aplicados" (`:1009-1014`).
- Excluir (`components/bank/DeleteBankMovementDialog.tsx`): "Excluir lançamento?" (`:207`); "<descrição> será removido e o
  saldo da conta a conta bancária será ajustado em R$ X." (`:220-226`, com `accountName="a conta bancária"`,
  `RevenueExpenseList.tsx:1199`: frase truncada, handoff); "Essa ação não pode ser desfeita."; "Cancelar" / "Excluir"
  ("Excluindo..."); toast "Lançamento excluído."; conciliado: "Este lançamento está conciliado. Desfaça a conciliação antes de
  excluir." (`:178-190,246-253`). Depois, o DRE e o patrimônio recarregam (`FinancialReport.tsx:771-778`).
- O que a lista mostra: compras e vendas pelos pedidos; receitas e despesas pela mesma régua do DRE (`get_dre_revenue_lines`,
  `get_dre_expense_lines`), que deixa de fora o dinheiro que espelha compra ou venda já listada (regra no servidor,
  `hooks/useDreExpenseLines.ts:1-16`).
- Exportar (`ExportHistoricoDialog.tsx`): "Exportar Histórico (PDF)" / "(Excel)" (`:280-285`); "O arquivo sai com os filtros
  abaixo, que já vêm iguais aos da tela. Ajuste aqui se quiser exportar algo diferente." (`:330`); "Incluir no arquivo":
  "Receitas", "Despesas", "Compras" (`:337-358`); "Período" "01/10/2026 a 31/10/2026" e "Para mudar o período, ajuste o
  filtro do relatório." (`:131-138,369-375`); "Cancelar" / "Exportar PDF" ("Gerando…") (`:287-321`); toasts "PDF gerado em
  nova aba", "Excel baixado com sucesso" (`:253-260`). O PDF abre numa aba nova (`:219-221`). Fechamento completo: arquivo com
  "Leia-me", "Resumo", lançamentos do período, contas em aberto na data de corte, notas relacionadas, posição de estoque no fim
  do período e pendências (`utils/financialAccountingReportExcelGenerator.ts:998-1090`).

## 4. Chamadas ao backend das telas da aula
| Tela | Tabelas | RPCs |
|---|---|---|
| Categorias | `financial_categories` | — |
| Centros de custo | `cost_centers` | — |
| Relatório (topo) | `profiles`, `companies`, `company_modules`, `customers`, `suppliers` (Histórico) | `get_financial_dre_summary` (`p_company_id`, `p_start_date`, `p_end_date`, `p_regime`; devolve `totalSales`, `totalPurchases`, `cmv`, `costBasis`, `otherRevenues`, `operatingExpenses`, `taxExpenses`, `revenueCategories` (com `costCenters`), `topSuppliers`, `topClients`, `topPurchaseMaterials`, `topSaleMaterials`, `avgTicketPurchase`, `avgTicketSale`, `stockCostReliable`, `stockValue`), `get_dre_expenses_by_group` (`operatingExpenses`, `taxExpenses`, `costExpenses`, `nonOperatingExpenses`), `get_company_patrimony`, `get_monthly_financial_evolution` (`p_months` 6) |
| DRE | `dre_groups`, `financial_categories` (`dre_group_id`), `dre_layout_*` (vazias) | `get_financial_dre_cost_center_breakdown` (competência), `get_financial_dre_summary` do período comparado (`hooks/useDreComparison.ts:69`) |
| Centros de Custo (aba) | `cost_centers` | `get_financial_dre_summary` do período anterior (`FinancialReport.tsx:213-238`) |
| Histórico | `purchases`, `sales` (status `completed`, por `transaction_date`) | `get_dre_expense_lines`, `get_dre_revenue_lines`; excluir: leituras de `bank_transactions`, `bill_payments`, `bill_payment_groups`, `cash_transactions`, `balance_movements` do grupo + `delete_bank_transaction_atomic` |
| Fechamento completo (não clicado) | — | `get_financial_accounting_report`, `get_accounting_closing_open_bills`, `get_stock_balance_at_date` |
