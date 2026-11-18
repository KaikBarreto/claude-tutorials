# Cobertura 1.60.10 · T15 · Relatório Financeiro e DRE

Auditoria só de leitura (18/11). Código: `/dev/shm/ecoflix-src` (1.60.10); diferença contra o roteiro:
`git diff f37573ea0 5290be4cd`. Caminhos relativos a `src/`. A varredura do robô (`rec/varredura/t15.txt`) ainda não
existia: nada aqui foi conferido na tela, só no código.

**Resumo**: das telas desta aula, o 1.60 só mexeu na aba **Histórico** (seleção em lote, filtro "Conta bancária", coluna
nova nos arquivos) e no visual da tabela diária da DFC. `pages/FinancialReport.tsx`, `FinancialDRE.tsx`,
`DreHierarchyTable.tsx`, `DreComparisonDialog.tsx`, `CostCenterAnalysis.tsx`, `OperationalInsights.tsx`,
`MonthlyEvolution.tsx`, `FinancialCategoriesManager.tsx`, `FinancialCategoryFormDialog.tsx`, `CostCentersManager.tsx`,
`DateRangeFilter.tsx` e o menu "Financeiro" estão **idênticos** ao 1.59.154: os capítulos 0 a 9 e 12 continuam batendo.
O grosso do trabalho é a parte (b): a aula deixa de fora uma aba inteira (DFC), a organização do DRE e várias ações.

## 1. Mudou no app

### cap10 · O Histórico
| # | O que mudou | Texto exato no 1.60.10 | Onde |
|---|---|---|---|
| M1 | Botão novo na barra, entre a busca e o "Exportar". Aparece quando a lista tem lançamento manual de caixa ou banco (na aba "Despesas" de outubro, sempre). | "Selecionar" (dica "Selecionar lançamentos"); ligado vira "Cancelar seleção" | `components/financial-report/RevenueExpenseList.tsx:876-892` |
| M2 | Com a seleção ligada, somem da linha o clipe, a seta do pedido, o lápis e a lixeira; a linha ganha caixa de marcar e o clique na linha marca em vez de abrir. Fora da seleção, lápis e lixeira continuam como no roteiro. | caixa "Selecionar lançamento <descrição>" | `RevenueExpenseList.tsx:1302-1318, 1378, 1397, 1416, 1430` |
| M3 | Barra de seleção, nova. | "N lançamentos selecionados" / "1 lançamento selecionado"; "Selecione até 100 lançamentos manuais de caixa ou banco."; "Limpar"; "Alterar categoria"; "Excluir selecionados" (só na aba Despesas) | `RevenueExpenseList.tsx:1131-1183` |
| M4 | Painel "Filtros" ganhou um campo, entre "Centro de custo" e "Fonte". Só aparece se alguma linha traz conta bancária (o servidor passou a devolver `bank_account_id` e `bank_account_name`). Escolher uma conta tira da lista caixa, compra e venda. | "Conta bancária", opção "Todas as contas" | `RevenueExpenseList.tsx:1080-1097`; `lib/historicoFilters.ts` (filtro e rótulo "Conta bancária: <nome>", `:240`); `hooks/useDreExpenseLines.ts:61-63`, `hooks/useDreRevenueLines.ts:74-75` |
| M5 | Trocar busca, qualquer filtro ou o período desliga a seleção e desmarca tudo. | (comportamento) | `RevenueExpenseList.tsx:727-742` |

A fala L3 do cap10 lista os filtros ("por cliente ou fornecedor, por centro de custo e pela fonte"; a `propostas_fala.md`
já tira "pela fonte"). Com M4, a lista correta na tela de outubro é Categoria, Cliente/Fornecedor, Centro de custo e
Conta bancária. Fala nova na proposta P7.

A janela de excluir **um** lançamento não mudou (continua "o saldo da conta a conta bancária será ajustado",
`RevenueExpenseList.tsx:1482`). Só a exclusão em lote passa o nome real da conta (`:1524`).

### cap11 · Exportar em Excel e PDF
| # | O que mudou | Texto exato | Onde |
|---|---|---|---|
| M6 | A janela "Exportar Histórico (PDF/Excel)" ganhou o mesmo campo, com a mesma condição do M4. | "Conta bancária", "Todas as contas" | `components/financial-report/ExportHistoricoDialog.tsx:534-554` |
| M7 | O PDF e o Excel do histórico têm uma coluna a mais, entre "Fonte" e "Tipo" ("—" em caixa, compra e venda). | cabeçalho "Data, Descrição, Categoria, Centro de custo, Fonte, Conta bancária, Tipo, Valor" | `utils/financialHistoricoPdfGenerator.ts:501-510`; `utils/financialHistoricoExcelGenerator.ts:83-92` |

O roteiro não cita as colunas do arquivo: nenhuma fala quebra. Se o PDF aparecer na tela (`[TESTAR]` do cap11), ele sai
com a coluna nova.

### Fora do que o roteiro mostra (só registro)
- DFC, visão "Realizado": a tabela "Realizado dia a dia" trocou o cabeçalho escuro por claro e passou a colorir os
  valores (verde entrada, vermelho saída, cinza zero) (`components/financial-report/DfcDailyTable.tsx:22-50`). Vale para
  o capítulo novo da DFC (P5).
- Trocar a categoria de um lançamento agora atualiza as telas por uma função única
  (`lib/queryInvalidations.ts`, usada em `EditCategoryDialog.tsx:89`); nada muda na tela.

## 2. Falta cobrir

Novo no 1.60 (N) ou já existia no 1.59.154 e o roteiro não mostra (E).

| # | Função | O que é e quando o cliente usa | Vale? |
|---|---|---|---|
| F1 (N) | **Alterar categoria em lote** no Histórico | "Selecionar", marca até 100 receitas ou até 100 despesas manuais de caixa ou banco, "Alterar categoria": janela "Alterar categoria de N lançamentos", "Escolha a categoria que será aplicada ao lote inteiro.", resumo "Despesas selecionadas · N no banco · N no caixa · Valores e saldos não mudam.", campo "Nova categoria (despesa)", botão "Aplicar categoria"; aviso "Categoria de N lançamentos atualizada." (`components/financial/BulkEditFinancialCategoryDialog.tsx:59-166`). Uso: o mês fechou com vários lançamentos na categoria errada ou sem categoria. | **Sim, capítulo novo (P8)** |
| F2 (N) | **Excluir selecionados** | Só despesas de banco, todas da mesma conta, com a permissão de contas bancárias. Avisos da barra: "Para excluir, selecione somente lançamentos bancários." e "Para excluir, selecione lançamentos da mesma conta bancária." (`RevenueExpenseList.tsx:715-723`). Janela "Excluir N lançamentos?", com "Se qualquer item não puder ser excluído, nenhum lançamento será alterado." (`components/bank/BulkDeleteBankMovementsDialog.tsx:118-168`). | **Só citar** em P8 (uma frase, com o botão na tela). A demonstração é da **T14** (Movimentações Bancárias, nota 1.60.1). O cap10 continua com a lixeira de uma linha: a história é uma conta em dobro. |
| F3 (N) | **Filtro "Conta bancária"** | M4 e M6. Uso: conferir o que saiu de uma conta só, ou mandar pro contador o histórico de uma conta. | **Sim, trecho** (P7) |
| F4 (E) | **Aba DFC**, visão **Previsto** | Abre nela. "Próximos" "15 dias" / "30 dias"; cartões "Saldo atual", "A receber · 15 dias", "A pagar · 15 dias", "Dívidas a receber", "Dívidas a pagar"; tabela por dia "Fluxo de caixa", "Dívida", com "Saldo inicial", "Recebimentos", "Total de saídas" (a seta abre as categorias) e "Saldo final"; clicar num valor abre "<linha> · <dia>" com os lançamentos e "Para editar ou dar baixa, abra o lançamento em Contas a Pagar/Receber."; "Saldo por conta"; gráfico "Evolução do saldo"; lista "O que já venceu e não foi baixado"; alerta "A conta <nome> fica negativa em <dia>." (`FinancialCashFlow.tsx:160-164, 200-275, 327, 461-505`). Uso: saber se o dinheiro dá para as contas das próximas semanas. | **Sim, capítulo novo (P5)**. É a quinta aba, e a decisão 1 do `plano.md` ficou aberta. |
| F5 (E) | **Aba DFC**, visão **Realizado** | "Realizado em <período>. Transferências entre contas próprias ficam fora."; "Filtros" por "Centros de custo"; "Exportar" em "Excel", "PDF" e "CSV"; cartões "Entradas", "Saídas", "Variação líquida"; tabela "Estrutura do DFC" (atividades, categorias e subcategorias, com "Entradas", "Saídas", "Líquido" e "Variação líquida de caixa"); "Realizado dia a dia"; aviso "R$ X ainda está sem categoria DFC." (`FinancialCashFlow.tsx:596-745`; `DfcHierarchyTable.tsx:81-84,163`). Segue o filtro de período. É onde aparece o "Grupo no Fluxo de Caixa (DFC)" que o cap01 escolhe para "Máquinas e veículos". | **Sim, capítulo novo (P6)** |
| F6 (E) | **Organizar categorias do DRE** (botão do cabeçalho do DRE e item "Grupos do DRE" → "Estrutura do DRE" → "Configurar grupos") | Janela "Organizar categorias do DRE", "Organize os grupos do modelo padrão e mova categorias arrastando.": "Natureza" + "Novo subgrupo" ("Ex.: Despesas com pessoal") + "Adicionar" (aviso "Grupo criado"); "Prévia da estrutura" com os grupos de cada natureza; arrastar categoria para outro grupo ("Categoria movida"), reordenar grupos, renomear e excluir grupo ("Mova as categorias deste grupo antes de excluí-lo.") (`DreConfigurationDialog.tsx:155-160, 225-330`; `pages/FinancialCategories.tsx:57-70`). Uso: separar a folha num subgrupo "Despesas com pessoal", como o contador pede. O roteiro mostra os dois botões e nunca abre. | **Sim, capítulo novo (P3)** |
| F7 (E) | **Outras visões** do DRE | Dentro da mesma janela: "Precisa enxergar este DRE de outra forma?", botão "Outras visões": "Outras visões do mesmo DRE", "DRE padrão do sistema · Recomendado para a maioria das empresas." ("Em uso"), "Criar outra visão" ("Exemplos: DRE gerencial, DRE contábil ou EBITDA."), "Criar rascunho", "Usar esta visão", "Ver exemplo em PDF" (`DreConfigurationDialog.tsx:339-347`; `DreLayoutProfilesPanel.tsx:95-230`). Montar uma visão tem macrogrupos, subtotais e publicação: é um editor inteiro. | **Só citar** (duas falas em P3, abrindo a tela sem criar). Montar uma visão completa daria uns 3 min; **decisão do Kaik**. |
| F8 (E) | **Categoria do DRE abre os centros de custo** | Em competência, a categoria com centro de custo tem seta e abre as linhas de cada centro, com "Sem centro de custo" por último (`DreHierarchyTable.tsx:301-355`). O cap06 abre o grupo e para na categoria; o cap07 só mostra a faixa de aviso do regime de caixa. | **Sim, trecho** (P4) |
| F9 (E) | **Recolher as seções** do DRE | Cada faixa (01, 02, 04, 06, 07) tem a seta "Recolher <seção>" / "Expandir <seção>" (`DreHierarchyTable.tsx:270`). Uso: ver só os totais. | **Só citar** (P4, uma frase) |
| F10 (E) | **Comparar períodos**: o resto da janela | "escolha até três referências"; "Mesmo período no ano passado"; "Outro período" ("Escolha datas personalizadas no calendário"); "Períodos adicionados"; "Variação no Excel: ..."; "Remover comparações" (`DreComparisonDialog.tsx:138-150, 223, 312, 355, 406-419`). O cap09 só usa "Período anterior". | **Sim, trecho** (P9) |
| F11 (E) | **Aba Centros de Custo**: detalhar um centro | Clicar numa coluna do gráfico abre "Categorias de <centro>" ("Selecione uma categoria para ver as movimentações que formam o valor.") com "Abrir histórico do centro"; no ranking, o botão "Movimentações" leva ao Histórico já filtrado pelo centro; "Distribuição das despesas"; nos cartões, "vs. período anterior" (`CostCenterAnalysis.tsx:228-239, 419-425, 520-551`; `pages/FinancialReport.tsx:626-629`). O cap03 passa pela aba sem clicar. | **Sim, trecho** (P2) |
| F12 (E) | **Histórico**: busca, detalhes e abas | "Buscar por descrição, categoria ou valor..." (`RevenueExpenseList.tsx:869`); clipe "Ver detalhes e anexos" (abre "Descrição", "Valor", "Tipo", "Data do lançamento", "Registrado em", "Categoria", "Centro de custo", "Forma de pagamento", "Conta bancária", "Operador", "Anexos"); seta "Ver detalhes do pedido" nas compras e vendas ("Itens", "Formas de pagamento") (`TransactionExpandedDetails.tsx:114-283`); aba "Compras"; "Exibir 10 por página". | **Sim, trecho** (P7) |
| F13 (E) | **Editar categoria** de um lançamento | Lápis: janela "Editar categoria", "Pesquisar categoria...", botão "Sem categoria" e os avisos "Sem categoria, o lançamento não entra nas receitas do relatório." / "Sem categoria, o lançamento aparece agrupado em "Sem categoria" no relatório." (`EditCategoryDialog.tsx:124-218`). O cap10 só aponta o lápis. | **Sim**, dentro de P8 (o lote resolve vários, o lápis resolve um) |
| F14 (E) | **Categorias**: editar, promover, excluir e ordenar | Três pontos: "Editar", "Tornar principal" (na subcategoria; "Subcategoria promovida a categoria principal"), "Excluir" ("Excluir categoria?", com três textos: com subcategorias "As subcategorias não serão apagadas: elas virarão categorias principais. Os lançamentos existentes continuam vinculados às suas categorias."; subcategoria "Os lançamentos desta subcategoria serão movidos para "<pai>" antes da exclusão."; sem filhas "Os lançamentos não serão apagados: eles ficarão sem categoria. Esta ação não pode ser desfeita."); "N categorias · arraste para reordenar" (`FinancialCategoriesManager.tsx:200-229, 333, 400-417`). | **Sim, trecho** (P1) |
| F15 (E) | **Centros de custo**: editar e excluir | Lápis "Editar centro de custo" e lixeira "Excluir centro de custo" ("Os lançamentos que usavam este centro de custo ficarão SEM centro de custo (não serão apagados)."). A fala do cap02 já explica o excluir, sem mostrar. | **Só citar**: pôr o mouse no lápis e na lixeira durante a fala que já existe. Sem fala nova. |
| F16 (E) | **Período**: "Personalizado" e "Todos os tempos" | O cap03 abre a lista e escolhe "Mês passado". "Personalizado" abre o calendário; em "Todos os tempos" o "Comparar períodos" fica desligado (`pages/FinancialReport.tsx:703`). | **Só citar** (P2, uma frase) |
| F17 (E) | **"Ver todos"** dos Top Fornecedores e Top Clientes | Abre a lista completa, paginada (`OperationalInsights.tsx:39, 364`). O cap05 passa sem clicar. | **Só citar**: clicar de verdade na fala que já existe ("E o Ver todos abre a lista completa."). Sem fala nova. |
| F18 (E) | Aviso **CMV subestimado** | Em competência: "Há material em estoque sem custo de compra cadastrado — o CMV pode estar subestimado." (`FinancialDRE.tsx:1488`). Uso: quem deu entrada de estoque sem preço de compra vê lucro maior do que o real. | **Sim, uma frase** no cap07 (P4), sem mostrar (o mundo não tem esse caso) |
| F19 (E) | **Fechamento completo (Excel)** e exportar do DRE, clicando | O cap11 aponta e não clica. O fechamento avisa "Fechamento gerado: N lançamentos, N contas em aberto e N pendências para revisar." (`RevenueExpenseList.tsx:809-813`). | **Só citar**: clicar de verdade e mostrar o aviso (as três RPCs do fechamento já estão no inventário, seção 4). Sem fala nova, se o backend falso responder. |
| F20 (E) | Banner **"Equilibrado"** | Terceiro estado do "Resultado do Período" (`ResultBanner.tsx`). | **Não**: caso raro, a fala já cobre superávit e déficit. |
| F21 (E) | **Duas moedas** no relatório | Blocos por moeda no DRE, no patrimônio e na DFC (`PatrimonyByCurrency.tsx`, `FxExchangePanel.tsx`, "Valores não são somados com outras moedas"). | **Não**: o mundo é só em real e nenhuma aula da trilha liga a segunda moeda. Se o Kaik quiser, é aula própria. |
| F22 (N) | **Preenchimento inteligente** (1.60.5 a 1.60.8) | Sugere categoria e centro de custo ao digitar a descrição do lançamento. Alimenta este relatório, mas a tela é a do lançamento. | **Outra aula**: T13 (contas) e T14 (lançamento bancário). Não repetir. |
| F23 (N) | **Contas bancárias por usuário** (1.59.165) | Quem tem a restrição só enxerga no Histórico as linhas das contas liberadas (as opções do filtro vêm das próprias linhas). | **Outra aula**: T2. |

## 3. Proposta

Nove acréscimos: quatro capítulos novos (P3, P5, P6, P8) e cinco trechos em capítulos que já existem. Ordem nova dos
capítulos: 00 · 01 · 02 · 03 · 04 · 05 · 06 · **Organizando o DRE** · 07 · 08 · 09 · **DFC previsto** · **DFC
realizado** · 10 · **Vários lançamentos de uma vez** · 11 · 12. A fala do cap03 que diz "Nesta aula, a gente passa pelo
Dashboard, pelo DRE, pelos Centros de Custo e pelo Histórico" passa a citar as cinco abas.

### P1 · cap01, depois de criar "Frete de entrega" (trecho)
| Tela | Fala |
| --- | --- |
| No cartão "Frete de entrega", clica nos três pontos: "Editar" e "Tornar principal"; fecha sem escolher. | Nos três pontos de cada categoria dá pra editar. E numa subcategoria aparece o Tornar principal, que tira ela de dentro da outra. |
| Nos três pontos de "Aluguel de caçamba", clica em "Excluir": a janela "Excluir categoria?", "Os lançamentos não serão apagados: eles ficarão sem categoria. Esta ação não pode ser desfeita."; clica em "Cancelar". [ZOOM: o texto da janela, a frase inteira] | Excluir uma categoria não apaga lançamento nenhum. Eles só ficam sem categoria. Se ela tiver subcategorias, elas viram principais. E as categorias do sistema, as do cadeado, não têm o Excluir. |
| A câmera mostra "N categorias · arraste para reordenar"; arrasta "Máquinas e veículos" uma posição e solta de volta. | E a ordem da lista é sua: é só arrastar. |

Mundo: nada novo (o robô cancela a exclusão e devolve a ordem).

### P2 · cap03, na aba "Centros de Custo" (trecho), e o período
| Tela | Fala |
| --- | --- |
| Na lista do filtro, antes de escolher "Mês passado", o mouse passa por "Personalizado" e "Todos os tempos". | Tem também o Personalizado, pra escolher as datas no calendário, e o Todos os tempos. |
| Na aba "Centros de Custo", a câmera para nos cartões, com "vs. período anterior". | Cada cartão compara com o período anterior. Aqui, outubro contra setembro. |
| Clique na coluna "Pátio" do gráfico "Receitas x despesas por centro" ("Clique em uma coluna para detalhar o centro."): abre "Categorias de Pátio", "Selecione uma categoria para ver as movimentações que formam o valor.". | Clicando numa coluna, o centro abre nas categorias dele. No pátio, a folha, o aluguel e a energia. |
| No "Ranking dos centros de custo", clique em "Movimentações" na linha "Pátio": a tela vai para a aba "Histórico", em "Despesas", com o filtro de centro de custo em "Pátio". Volta para "Centros de Custo". | E o botão Movimentações leva pro Histórico já filtrado, com cada lançamento que formou esse valor. |

Mundo: `costCenters` por categoria de outubro e de setembro já estão no plano; as linhas de `get_dre_expense_lines`
precisam trazer `cost_center_id` para o filtro mostrar as do Pátio.

### P3 · capítulo novo "Organizando o DRE" (vinheta: DRE), depois do cap06
| Tela | Fala |
| --- | --- |
| `setup`: "Mês passado", aba "DRE". Clique em "Organizar categorias": a janela "Organizar categorias do DRE", "Organize os grupos do modelo padrão e mova categorias arrastando.", com a "Prévia da estrutura". | O DRE que a gente acabou de ler tem uma estrutura, e ela é sua pra arrumar. No cabeçalho, Organizar categorias. |
| A câmera desce pela prévia: as faixas "01 Receita Bruta", "02 Impostos e Deduções", "04 Custos Operacionais", "06 Despesas Operacionais" e "07 Outras Receitas e Despesas", cada uma com os grupos e as categorias. | Aqui aparecem as mesmas faixas do DRE. Dentro de cada uma ficam os grupos, e dentro de cada grupo, as categorias. |
| Em "Natureza", escolhe "06 · Despesas Operacionais"; em "Novo subgrupo", digita "Despesas com pessoal"; clique em "Adicionar": aviso "Grupo criado"; o grupo aparece na faixa 06. | O contador pediu a folha separada das outras despesas. Então eu crio um subgrupo nas Despesas Operacionais: Despesas com pessoal. |
| Arrasta "Folha salarial" para dentro de "Despesas com pessoal": aviso "Categoria movida". [ZOOM: o grupo novo com a folha dentro, a frase inteira] | Agora é só arrastar a Folha salarial pra dentro dele. Nenhum lançamento muda, só o lugar onde a categoria aparece. |
| A câmera mostra o lápis e a lixeira do grupo, sem clicar. | Dá pra renomear um grupo e trocar a ordem arrastando. Pra excluir, antes é preciso tirar as categorias de dentro dele. |
| Clique em "Outras visões": "Outras visões do mesmo DRE", com "DRE padrão do sistema", "Recomendado para a maioria das empresas." e o selo "Em uso"; embaixo, "Criar outra visão", "Exemplos: DRE gerencial, DRE contábil ou EBITDA.". Não cria. | Embaixo ficam as Outras visões. Quem precisa de um DRE gerencial, contábil ou com EBITDA monta outra apresentação com os mesmos lançamentos. O DRE padrão é o recomendado pra maioria das empresas. |
| Clique em "Voltar à organização padrão" e em "Fechar": o DRE mostra "Despesas com pessoal" na faixa 06, com a "Folha salarial" dentro. | Fecho, e o DRE já mostra o grupo novo. Uma dica: esse mesmo painel abre em Categorias Financeiras, no item Grupos do DRE. |

Mundo: insert em `dre_groups` (natureza `despesas_operacionais`, "Despesas com pessoal") e update do `dre_group_id` da
"Folha salarial" em `financial_categories`; as tabelas `dre_layout_*` vazias (a tela de "Outras visões" precisa
responder sem erro, senão mostra "O recurso de outras visões ainda não está disponível neste ambiente."). Usuário com
`action_manage_financial_categories` (Rafael é MASTER). **Decisão**: o grupo novo fica no mundo dos capítulos seguintes
(os códigos das linhas do grupo 06 mudam na tela) ou os capítulos 7 em diante continuam abrindo da semente sem ele? Os
totais não mudam nos dois casos; a proposta é não levar adiante (menos regravação).

### P4 · cap06 e cap07 (trechos)
| Tela | Fala |
| --- | --- |
| cap06, depois de abrir o grupo: clique na seta da "Energia elétrica": abrem as linhas dos centros de custo ("Pátio" e, se houver, "Sem centro de custo"). [ZOOM: as linhas, a frase inteira] | E a categoria também abre. Dentro dela aparece quanto foi de cada centro de custo. O que ficou sem marcação vem numa linha separada, Sem centro de custo. |
| cap06: clique na seta da faixa "06 (-) Despesas Operacionais" ("Recolher"): a faixa fecha no total; clique de novo. | Pra ver só os totais, cada faixa recolhe na seta. |
| cap07, depois da troca para "Regime de Caixa": a câmera para na faixa cinza "O detalhamento por centro de custo fica disponível no regime de competência, cuja data contábil é compatível com os lançamentos categorizados.". | No regime de caixa, a divisão por centro de custo some. Ela só existe na competência, e a tela avisa. |
| cap07, no fim, com o DRE em competência (sem mostrar aviso). | Uma dica: se a competência avisar que tem material em estoque sem custo de compra, o custo do que foi vendido pode estar menor do que o real. Vale conferir o cadastro desses materiais. |

Mundo: `get_financial_dre_cost_center_breakdown` de outubro com a energia no Pátio (já previsto no plano).

### P5 · capítulo novo "Vai ter dinheiro? A DFC prevista" (vinheta: DFC), depois do cap09
| Tela | Fala |
| --- | --- |
| `setup`: "Mês passado". Clique na aba "DFC": os botões "Previsto" (marcado) e "Realizado", "Próximos" "15 dias" / "30 dias" e os cartões "Saldo atual", "A receber · 15 dias", "A pagar · 15 dias", "Dívidas a receber" e "Dívidas a pagar". | O DRE diz se a empresa ganhou. A DFC, o demonstrativo do fluxo de caixa, diz se vai ter dinheiro. Ela abre no Previsto, que olha pra frente. |
| [ILUSTRAÇÃO: Olhando pra frente: um calendário de 15 dias; em cada dia, moedas entrando (verde) e saindo (vermelho) de um cofrinho; a linha do saldo sobe e desce de um dia para o outro] | Ele parte do saldo de hoje, soma o que você tem a receber e tira o que tem a pagar, dia por dia, pelas datas de vencimento. |
| A ilustração sai; a câmera fica nos cartões. [ZOOM: "Dívidas a pagar" e "Dívidas a receber", a frase inteira] | Em cima, o saldo atual, o que entra e o que sai nos próximos quinze dias, e as dívidas: o que já venceu e ninguém deu baixa. |
| A câmera desce para a tabela: "Fluxo de caixa", "Dívida" e uma coluna por dia, com "Saldo inicial", "Recebimentos", "Total de saídas" e "Saldo final". | Na tabela, cada coluna é um dia. O saldo final de um dia é o saldo inicial do outro. |
| Clique na seta de "Total de saídas": abrem as categorias ("Aluguel", "Folha salarial" e as outras). | A seta do Total de saídas abre as categorias. |
| Clique no valor de "Total de saídas" no dia do aluguel: a janela "Saídas · <dia>", "N lançamentos", com "Para editar ou dar baixa, abra o lançamento em Contas a Pagar/Receber."; fecha. | E clicando num valor, aparecem as contas daquele dia. Pra pagar ou mudar a data, o lugar é Contas a Pagar e Receber. |
| A câmera desce para "Saldo por conta", para o gráfico "Evolução do saldo" e para "O que já venceu e não foi baixado" (a conta de água vencida, "N dias em atraso"). | Embaixo, o saldo de cada conta, o gráfico do saldo e a lista do que já venceu, como a conta de água. |
| Clique em "30 dias": a tabela e os cartões recalculam. | Trocando pra trinta dias, a previsão vai mais longe. |
| A câmera para em "Previsão otimista: considera que tudo será pago e recebido no vencimento. O que já venceu aparece como dívida e não é descontado novamente do saldo.". [ZOOM: a frase, a frase inteira] | Uma dica: essa previsão é otimista. Ela conta que todo mundo paga no dia. E se uma conta bancária for ficar negativa, a tela avisa em vermelho, com o nome da conta e o dia. |
| A câmera abre. | O Previsto não segue o filtro de período. Ele sempre começa hoje. |

Mundo: a DFC prevista lê tabelas, não RPC (`hooks/useCashFlowReport.ts:73-95`: `financial_bills`, `bank_accounts`,
`cash_register`, `companies`). Precisa das contas abertas de novembro do T13 (água vencida, aluguel, o fiado da Aços
Quiririm, as parcelas da Fundição) com vencimento e conta prevista, e dos saldos de 10/11. `[TESTAR]` se alguma conta
fica negativa nos 30 dias: se ficar, o alerta "A conta <nome> fica negativa em <dia>." aparece e a fala pode apontar
pra ele; se não, fica só falado.

### P6 · capítulo novo "Por onde o dinheiro passou: a DFC realizada" (vinheta: DFC)
| Tela | Fala |
| --- | --- |
| `setup`: "Mês passado", aba "DFC". Clique em "Realizado": "Realizado em Outubro de 2026. Transferências entre contas próprias ficam fora." e os cartões "Entradas", "Saídas" e "Variação líquida". | O Realizado olha pra trás: o dinheiro que entrou e saiu de verdade do caixa e do banco. E esse segue o período, aqui outubro. |
| [ZOOM: "Variação líquida", com o valor negativo, a frase inteira] | Em outubro saiu mais do que entrou. É a mesma história do regime de caixa: o ferro que ficou no pátio. |
| A câmera abre e desce para "Estrutura do DFC": as atividades operacionais, de investimento e de financiamento, com "Entradas", "Saídas" e "Líquido". | A tabela separa o dinheiro em três atividades: as operacionais, do dia a dia, as de investimento e as de financiamento. |
| Clique numa atividade e numa categoria: abrem as categorias e as subcategorias. | Lembra do grupo do fluxo de caixa que a gente escolheu na categoria das máquinas? É ele que decide em qual atividade cada lançamento entra. |
| A câmera desce até "Variação líquida de caixa" e "Realizado dia a dia" ("Data", "Entradas", "Saídas", "Variação", "Saldo realizado"). | No fim, a variação do caixa no período. E embaixo, o realizado dia a dia. |
| Clique em "Filtros": "Centros de custo", marca "Coleta": "Filtros (1)" e "Filtro aplicado ao realizado e às exportações."; desmarca. | Dá pra filtrar por centro de custo, e o filtro vale também pro arquivo exportado. |
| Clique em "Exportar": "Excel", "PDF" e "CSV"; fecha sem escolher. | E o Exportar gera a DFC em Excel, PDF ou CSV. |
| A câmera abre. | Transferência entre contas da própria empresa não aparece aqui: o dinheiro só mudou de lugar. E se algum valor estiver sem categoria de fluxo de caixa, a tela mostra um aviso amarelo pra você corrigir a categoria. |

Mundo: o realizado lê `bank_transactions` e `cash_transactions` do período (`hooks/useCashFlowReport.ts:267-275`), com
categoria (para o `cash_flow_group`) e centro de custo. Os lançamentos de outubro da semente já existem para o
Histórico; conferir se trazem `category_id` em todos, senão aparece o aviso "ainda está sem categoria DFC" (pode até
ser útil: mostrar em vez de só falar). A variação líquida de outubro tem de contar a mesma história do regime de caixa
do cap07 (negativa); o número não precisa ser o -R$ 31.500,00 (a DFC conta dinheiro, o DRE em caixa conta pedidos).

### P7 · cap10 (trechos)
| Tela | Fala |
| --- | --- |
| Logo depois de abrir a aba "Despesas": digita "3850" em "Buscar por descrição, categoria ou valor...": ficam as duas contas de energia; apaga a busca. | A busca acha pela descrição, pela categoria ou pelo valor. Digitando três mil oitocentos e cinquenta, já aparecem as duas contas. |
| (substitui a fala L3) Clique em "Filtros": o painel com "Categoria", "Cliente/Fornecedor", "Centro de custo" e "Conta bancária" ("Todas as contas", "Conta Principal", "Conta Secundária"); em "Categoria", marca "Energia elétrica"; "Aplicar". | Lembra da energia de outubro? Em Filtros, escolho a categoria Energia elétrica. Dá pra filtrar também por cliente ou fornecedor, por centro de custo e por conta bancária. |
| Na linha das 09:12, clique no clipe ("Ver detalhes e anexos"): abre o detalhe, com "Descrição", "Valor", "Data do lançamento", "Registrado em", "Categoria", "Centro de custo", "Forma de pagamento", "Conta bancária", "Operador" e "Anexos". [ZOOM: o detalhe, a frase inteira] | Antes de excluir, eu abro o lançamento no clipe. Aparece tudo o que foi preenchido: a conta, a forma de pagamento, quem lançou, a hora e os anexos. Os dois são iguais, então um deles é a cópia. |
| Depois da ilustração do fim do capítulo: clique na aba "Compras"; clique na seta ("Ver detalhes do pedido") da compra do ferro pesado do Depósito Irmãos Siqueira: "Itens" e "Formas de pagamento". | Na aba Compras, e nas vendas dentro das Receitas, a seta abre o pedido, com os itens e as formas de pagamento. |

Mundo: `get_dre_expense_lines` e `get_dre_revenue_lines` do backend falso passam a devolver `bank_account_id` e
`bank_account_name` (sem isso o campo "Conta bancária" não aparece e a tela fica igual à do 1.59). As duas contas de
energia na "Conta Principal". O detalhe do lançamento e do pedido leem o lançamento e o pedido pelo id
(`TransactionExpandedDetails.tsx`): o robô confere quais consultas faltam no backend falso.

### P8 · capítulo novo "Vários lançamentos de uma vez" (vinheta: HISTÓRICO), depois do cap10
| Tela | Fala |
| --- | --- |
| `apos-cap10`; `setup`: "Mês passado", aba "Histórico", em "Despesas". Na linha "Diesel S10 Posto Bandeirante", clique no lápis: a janela "Editar categoria", com a lista e "Sem categoria"; escolhe "Combustível"; aviso "Categoria atualizada". | No Histórico também dá pra arrumar a categoria sem sair do relatório. Num lançamento só, é o lápis: escolho a categoria certa e pronto. |
| A câmera mostra três lançamentos "Pedágio" com o selo "Manutenção de veículos". | Mas olha os pedágios de outubro: três lançamentos, todos em Manutenção de veículos. O certo era Combustível. |
| Clique em "Selecionar": aparecem as caixas de marcar e a barra "0 lançamentos selecionados", "Selecione até 100 lançamentos manuais de caixa ou banco."; marca os três pedágios: "3 lançamentos selecionados". | Clico em Selecionar e marco os três. Dá pra marcar até cem de uma vez, do caixa e do banco. |
| Clique em "Alterar categoria": a janela "Alterar categoria de 3 lançamentos", "Despesas selecionadas", "3 no banco · Valores e saldos não mudam."; em "Nova categoria (despesa)", escolhe "Combustível". [ZOOM: o resumo e o campo, a frase inteira] | Em Alterar categoria, escolho a categoria nova. A janela avisa: os valores e os saldos não mudam, só a classificação. |
| Clique em "Aplicar categoria": aviso "Categoria de 3 lançamentos atualizada."; a seleção fecha e os três aparecem com o selo novo. | Aplico, e os três mudam juntos. O DRE e o Dashboard já recalculam com a categoria certa. |
| Clique em "Selecionar" de novo, marca duas linhas de banco: o botão vermelho "Excluir selecionados" fica ativo; clique em "Cancelar seleção". | Do lado fica o Excluir selecionados, pra apagar vários lançamentos de banco da mesma conta. Se um deles não puder ser excluído, nenhum é. |
| A câmera abre. | Uma dica: compra e venda não entram na seleção. A categoria delas vem do pedido. |

Mundo: três despesas de banco de outubro com a categoria errada (nomes e valores a definir no `MUNDO_FICTICIO.md`; os
"Pedágio" e "Diesel S10 Posto Bandeirante" acima são exemplo; as categorias "Manutenção de veículos" e "Combustível" são as do plano, e a soma das despesas operacionais de outubro, R$ 40.705,90,
não muda porque as duas categorias estão no mesmo grupo). Handler novo: RPC
`update_financial_transaction_categories_batch` (`p_cash_ids`, `p_bank_ids`, `p_category_id`). A lista "Despesas por
Categoria" do cap04 muda de valores se a troca for levada ao mundo: melhor gravar o cap04 já com os pedágios na
categoria errada e não citar essas duas categorias lá, ou não levar a troca adiante. **Decisão** junto com a de P3.

### P9 · cap09 (trecho), na janela "Comparar períodos"
| Tela | Fala |
| --- | --- |
| Antes de "Aplicar comparação": o mouse passa por "Mesmo período no ano passado" e "Outro período" ("Escolha datas personalizadas no calendário"). | Dá pra comparar também com o mesmo período do ano passado ou com outras datas, até três comparações lado a lado. |
| Depois da fala do nome da categoria: clique em "Comparar períodos" e em "Remover comparações": a tabela volta a uma coluna. | Pra voltar ao DRE de um mês só, Remover comparações. E o Excel do DRE sai com as mesmas colunas, mais a variação entre elas. |

Mundo: nada novo. Continua valendo o achado 1 da `propostas_fala.md` (a primeira comparação se perde).

### Sem fala nova (só a coluna Tela)
- cap02: o mouse passa no lápis "Editar centro de custo" e na lixeira "Excluir centro de custo" na fala do "Ativo" (F15).
- cap05: clicar de verdade em "Ver todos" do "Top Clientes" e fechar (F17).
- cap11: clicar em "Fechamento completo (Excel)" e mostrar o aviso "Fechamento gerado: ..." (F19); abrir a janela de
  exportar com o campo "Conta bancária" na tela (M6).
- cap12 (recap): uma linha a mais, "Organizou o DRE, olhou a DFC prevista e a realizada, e trocou a categoria de vários
  lançamentos de uma vez." (entra na conta abaixo).

## 4. Estimativa

A 2,6 palavras por segundo:

| Proposta | Palavras | Segundos |
|---|---|---|
| P1 (cap01) | 64 | 25 |
| P2 (cap03) | 60 | 23 |
| P3 (capítulo novo, DRE) | 158 | 61 |
| P4 (cap06 e cap07) | 92 | 35 |
| P5 (capítulo novo, DFC prevista) | 211 | 81 |
| P6 (capítulo novo, DFC realizada) | 170 | 65 |
| P7 (cap10; a fala trocada conta só a diferença) | 82 | 32 |
| P8 (capítulo novo, lote) | 137 | 53 |
| P9 (cap09) | 46 | 18 |
| Recap | 20 | 8 |
| **Total** | **~1.040** | **~400 s (6 min 40 s) de fala** |

Com quatro vinhetas novas e as ações sem fala, o vídeo vai de ~16 min 45 s para ~24 min 30 s, em 17 capítulos (13 hoje).
Uma ilustração nova (P5).

## Depende de decisão
1. **DFC** (P5 e P6): entra com dois capítulos (~2 min 30 s)? É a decisão 1 do `plano.md`, ainda aberta.
2. **Outras visões do DRE**: só citar (proposto) ou montar uma visão EBITDA de ponta a ponta (~3 min a mais)?
3. **Mundo**: o subgrupo "Despesas com pessoal" (P3) e a troca de categoria em lote (P8) ficam no mundo das aulas
   seguintes (T21, T25, T22) ou valem só dentro do capítulo?
4. **Dados de P8**: quais três despesas de outubro nascem com a categoria errada (mexe na semente e no
   `MUNDO_FICTICIO.md`).
5. **Excluir em lote**: fica na T14, citado aqui (proposto), ou o cap10 troca a lixeira pela seleção?
6. Duas moedas (F21) fica fora da trilha?
