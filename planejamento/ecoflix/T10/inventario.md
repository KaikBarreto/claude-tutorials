# Inventário · T10 · Estoque: saldo, histórico e posição (EcoSistema 1.60.18, aplicado em 20/11/2026)

Código lido (só leitura): `/dev/shm/ecoflix-src` (`APP_VERSION = "1.60.18"`, `src/config/version.ts:16`; a primeira versão deste
inventário é de 1.59.154, e as linhas citadas abaixo podem ter andado). Veja "Mudou na 1.60.18" no fim. Caminhos relativos a `src/`. Textos pt-BR de `i18n/locales/pt-BR/materials.json` (chave `materials:`) e
`common.json` (`dateFilter`). Desktop, logado como Rafael Nogueira (MASTER: vê valores e exporta).

## Onde fica (menu)
`config/routes.ts:446-456`: menu **"Materiais"** com "Estoque" (`/materiais`), **"Histórico (Kardex)"** (`/historico-materiais`; `navigation.json` `stockHistory`),
"Relatório" (`/relatorio-estoque`), "Ticket de Pesagem" e "Produção". A **Posição de Estoque**
(`/materiais/posicao-estoque`) não está no menu: com várias tabelas de preço ligadas (o T3 cria a "Tabela Depósitos"),
fica na coluna "Tabelas de Preço" da tela de Estoque, embaixo de "Nova Tabela" (`components/PriceTableSidebar.tsx:272-285`);
com uma tabela só, vira o botão "Posição de Estoque" no cabeçalho (`pages/Materiais.tsx:217-218,2339-2350`).
Rotas: `App.tsx:390,410,415,483`.

## 1. Estoque · `/materiais` · `pages/Materiais.tsx`
- Cabeçalho: "Estoque", "Gerencie os materiais do estoque" (`:2333-2337`); trilha "Materiais" › "Estoque".
- Botões (`:2352-2420`): "Movimentar estoque", "Editar Tabela", "Grupos", "Exportar" ("Exportar Estoque":
  "Estoque (PDF)", "Estoque (Excel)"; "Tabela de Preços").
- Cartões (`:2581-2630`): "Peso Total em Estoque" (soma do saldo, "Kg"), "Total Pago" (soma do Valor Pago),
  "Projeção de Vendas" (saldo × preço de venda da tabela escolhida) (`:1851-1887`).
- "Lista de Materiais", "Exibindo preços da tabela: <nome>" (`:2763-2768`); filtro "Todos os Materiais" (`:2772-2790`).
- Colunas (`:3001-3078`): "Código", "Nome", "Estoque Atual" (número com 3 casas + unidade), "Valor Pago",
  "Preço médio pago" (selo "estimativa"), "Preço de Compra", "Preço de Venda", "Ações".
- Menu "..." da linha (`:3170-3215`): "Movimentar estoque", "Transferir estoque", "Editar", "Excluir".
- Barra de seleção (caixas marcadas, `:3534-3566`): "Transferir Estoque", "Definir prefixo", "Excluir".
- Backend: `materials`, `price_tables`/`price_table_items`, `purchase_items` (custo médio, `:456`), `material_groups`.

### 1.1 Transferir estoque (avulsa) · `components/TransferMaterialDialog.tsx`
- Título "Transferir Estoque"; descrição "Transferir quantidade de <material> (Código: <código>) para outro material";
  "Estoque Atual de <material>" (número grande, "Kg"); "Material de Destino *" (busca "Escreva o nome ou código do
  material"); "Quantidade a Transferir (Kg) *" ("0,000"); "Cancelar" / "Transferir" (`:155-196`).
- Toast: "Transferido 320,000 Kg de Ferro misto para Ferro pesado" (`:84-86`).
- RPC `transfer_material_stock(p_source_id, p_target_id, p_quantity, p_client_request_id)`: tira da origem, põe no
  destino e grava duas linhas "TRANSFERENCIA" em `stock_movements` (`:66-77`).

### 1.2 "Transferir Estoque" da barra de seleção · `components/BulkTransferDialog.tsx`
- Título "Transferência em Lote"; "Criar transferências para N material(is) selecionado(s)." (`:404-410`).
- **É entre unidades do grupo (matriz e filial), não entre materiais**: "Destino" / "Selecionar unidade de destino..."
  (`:459-466`). Sem grupo: "Sua empresa não faz parte de nenhum grupo gerencial. Configure primeiro em Configurações."
  (`:430-434`). RPCs `get_group_destinations_for_member`, `link_own_material_to_group_catalog`. É do Gerencial (T22).

### 1.3 Movimentar estoque (entrada/saída manual) · `components/StockMovementDialog.tsx`
- "Movimentar estoque", "Registre uma entrada ou saída manual de material com quantidade e observação."; "Entrada" /
  "Saída"; "Material *"; "Quantidade *"; "Estoque atual" → "Após a movimentação"; "Descrição / observação"
  ("Ex: ajuste de inventário, sobra de produção, quebra..."). RPC `adjust_material_stock_atomic` (tipo EDICAO_MANUAL,
  `:97-103`). A aula só cita (o T3 ensina).

## 2. Histórico de Materiais (Kardex) · `/historico-materiais` · `pages/MaterialHistory.tsx`
- Cabeçalho "Histórico de Materiais", "Rastreamento de todas as movimentações de estoque - KARDEX" (`:790-796`).
- Coluna esquerda "Materiais" (contador), busca "Buscar código ou material", "Ordenar"; primeiro item
  **"Geral (Todos)"** / "Todas as movimentações"; depois cada material com "Código <n>" (`:535-632`).
- Título da tabela: "KARDEX" + "Geral" ou "<código> - <nome>" (`:819`; tem travessão no meio, não ler). Botões
  "Filtros" (com contador), "Como funciona?", "Exportar" ("Exportar Kardex": "PDF", "Excel") (`:820-870`).
- **Período padrão "Este mês"** (`:203`; conta como filtro ativo só quando muda, `:384-390`).
- Painel "Filtros do Kardex", "Refine as movimentações por período, tipo, quantidade e parceiro." (`:884-888`):
  "Período" (opções "Todos os tempos", "Hoje", "Últimos 7 dias", "Este mês", "Mês passado", "Últimos 30 dias",
  "Este ano", "Personalizado"; `components/DateRangeFilter.tsx:426-449`), "Tipo de movimentação", "Fornecedores",
  "Clientes", "Quantidade movimentada" ("Considera o valor sem sinal: 40 encontra +40 e -40."); rodapé
  "Limpar filtros" (volta tudo, inclusive o período para "Este mês", `:370-380`) e "Aplicar filtros" (`:962-980`).
- Colunas (`:1210-1218`): "Usuário", "Data" (dica com "dd/MM/yyyy às HH:mm"), "Tipo", "Pedido #", "Material",
  "Estoque Inicial", "Movimentação" (+ verde / − vermelho), "Estoque Final". Ordem: mais recente em cima.
- Tipos (selos coloridos, `:173-191`): "Compra", "Venda", "Transferência", "Edição Manual", "Exclusão", "Produção",
  "Saldo inicial". "Exclusão" = pedido excluído ou estornado (o estoque volta), ou material arquivado com estoque
  ("Arquivamento do material <nome>", `pages/Materiais.tsx:1327-1345`).
- **Filtro de parte** (`utils/fetchStockMovements.ts:206-272`, regra do dono, 1.60.18): fornecedor ligado deixa só as COMPRAS dele
  (as vendas saem); cliente ligado deixa só as VENDAS dele (as compras saem); os dois: compras do fornecedor mais vendas do
  cliente. Edição manual, transferência, exclusão, produção e saldo inicial saem com qualquer um ligado.
- Linha aberta (clique, `:1341-1420`): compra/venda mostra "Material", "Peso", "Valor Unit.", "Total";
  "Fornecedor:"/"Cliente:"; "Formas de Pagamento" ("Dinheiro: ...", "Pix/Transferência: ...", "Saldo: ..."); observação e
  Pix; "Total do Pedido:"; **"Fotos anexadas"** (miniaturas que ampliam; sem foto: "Nenhuma foto anexada.").
  Movimento manual: "Entrada"/"Saída", "Observação" ("Sem observação"), "Estoque" antes → depois, usuário e hora.
- Ajuda "Como funciona o Kardex" (`:1500-1600`): "Move quantidade de um material para outro.", "Ajuste feito direto no
  estoque, sem compra ou venda.", "Estorno" + "um pedido foi excluído e o estoque voltou ao que era." (o texto da tela tem travessão entre os dois: não ler).
- Backend: `stock_movements` (+ `materials`, `profiles`), `suppliers`, `customers`, `purchases`/`sales` (filtro de parte);
  ao abrir: `purchase_items`/`sale_items`, view `orders_with_payments`, `cash_transactions`/`bank_transactions`/
  `balance_movements` (`utils/paymentMethodsHelper.ts`), `order_attachments` + bucket `order-attachments`.

## 3. Relatório de Estoque · `/relatorio-estoque` · `pages/InventoryReport.tsx`
- Cabeçalho "Relatório de Estoque", "Análise detalhada de compras, vendas e lucro por material"; período (padrão
  **"Este mês"**, `:73`); "Exportar Relatório" (PDF) (`:912-950`).
- Cartões que abrem ao clicar (`:953-1170`): "Total Comprado" ("Preço médio de compra", "Qtd. Comprada", "Materiais
  comprados", "Material que mais comprou"), "Total Vendido", "Lucro" ("Lucro s/ vendas total", "Resultado total",
  "Margem"...), "Projeção de Lucro" (selo "estimativa"; dica `materials:report.profitProjectionHint`).
- Filtros (`:1289-1400`): "Todos os Materiais", "Fornecedores", "Clientes", "Usuários", "Grupos", "Ocultar itens
  zerados"; "Detalhamento por Material" com "Por material"/"Por grupo".
- Colunas (`:1427-1462`): "Código", "Material", "Qtd. Comprada", "Valor Comprado", "Preço Médio Compra", "Qtd. Vendida",
  "Valor Vendido", "Preço Médio Venda", "Lucro s/ Vendas" (estimativa: (preço médio de venda − preço médio de compra) ×
  qtd. vendida, `components/reports/inventoryTooltips.tsx:9-18`), "Resultado" (valor vendido − valor comprado no
  período, mínimo R$ 0,00: `utils/profitDisplay.ts:14-16`), "Margem" (resultado ÷ valor vendido); linha "TOTAL".
- **Qtd. Comprada líquida**: a RPC devolve quantidade − (tara + impureza) (`:298-304`; na compra o campo é "Tara/Imp." e
  o resultado "Peso Líquido do Item", `components/OrderFormInputs.tsx:800,851`).
- **Com "Fornecedores" marcado** o relatório fica só de compras: some "Total Vendido", "Lucro", "Projeção de Lucro" e as
  colunas de venda, resultado e margem (`:231-238,953,1006,1432`). Motivo no código: a venda não tem fornecedor.
- Backend: RPCs `get_inventory_report_data(p_company_id, p_start_date, p_end_date, p_supplier_ids, p_customer_ids,
  p_creator_ids)`, `get_financial_dre_summary` (cartões sem filtro), `get_orders_payment_distribution`; tabelas
  `materials`, `companies`, `suppliers`, `customers`, `profiles`. "Só pedidos finalizados e não estornados, pela data do
  pedido": regra da RPC (o SQL não está nesta cópia; vale o que a fonte conferiu).

## 4. Posição de Estoque · `/materiais/posicao-estoque` · `pages/PosicaoEstoque.tsx`
- Cabeçalho "Posição de Estoque" (`:698-702`; a descrição tem travessão, não ler). Coluna "Tabelas de Preço" com
  "Posição de Estoque" destacada.
- Cartão "Escolha a data": "Data e hora (padrão: fim do dia)" (data + "Hora"), "Ver posição", "Exportar" ("Exportar
  posição": "PDF", "Excel"); "O padrão é o fim do dia (23:59). Você pode ajustar o horário." (`:704-760`).
- Data: abre em hoje 23:59 (`:168-180`); trocar o dia mantém a hora; dia futuro bloqueado
  (`components/ui/RetroactiveDateTimePicker.tsx:180-228`).
- "Posição de estoque em 31/10/2026 23:59"; "Por material"/"Por grupo"; colunas "Código", "Material", "Unidade", "Saldo",
  "Valor", "Projeção venda"; linha "Total geral"; nota "Valores negativos indicam movimentações lançadas fora da ordem
  cronológica. Valor = saldo × custo médio das compras até a data. Projeção = saldo × preço de venda atual. Itens sem
  compra registrada até a data aparecem sem valorização." (`:766-817`). Só materiais com saldo diferente de zero.
- Exportar → `components/estoque/StockExportDialog.tsx`: "Exportar estoque (PDF)" / "(Excel)", "Escolha os materiais e
  as colunas do arquivo. Sua última seleção fica salva para a próxima exportação."; "Colunas do arquivo" ("Código",
  "Material", "Unidade", "Saldo", "Valor do estoque", "Projeção de venda"), "Grupos", "Materiais" ("Marcar todos",
  "Desmarcar todos"); "N de M materiais", "Cancelar", "Exportar" (`:264-290`).
- Toasts: "Posição de estoque exportada em PDF" / "...em Excel" (`:382,390`). PDF: aba nova com o arquivo e os botões
  "Baixar Imagem" e "Baixar PDF" (`utils/openPdfInTab.ts:255-262`); Excel: baixa `posicao-estoque-...xlsx`.
- Backend: RPC `get_stock_balance_at_date(p_company_id, p_at)` (só saldo ≠ 0, com `avg_cost` e `sale_price`),
  `materials`, `production_recipes`, `material_groups`, upsert em `stock_export_preferences`.

## Fonte × código (para o relatório)
- Cap. 3 "avulsa e em massa": na 1.59.154 a transferência **entre materiais** é só a avulsa (menu da linha). A da
  barra de seleção é "Transferência em Lote" entre unidades do grupo (Gerencial, T22).
- ⚠️ do período: a opção é **"Todos os tempos"** (a fonte diz "Todo o período").
- ⚠️ do Kardex (corrigido na 1.60.18): com o filtro de fornecedor as vendas SAEM (antes continuavam). O que também some é o que
  não tem parte (manual, transferência, exclusão, produção, saldo inicial).

## Mudou na 1.60.18 (aplicado na aula em 20/11)
- **Kardex, coluna "Materiais"** (`pages/MaterialHistory.tsx:536-628`): busca "Buscar código ou material" (`aria-label` "Buscar material"),
  botão "Ordenar" (dica "Ordenar materiais": "Código", "Nome"), páginas de 25. Cap. 7.
- **Kardex, Filtros** (`:884-980`): "Período" com "Personalizado" (calendário de dois meses que aplica sozinho quando o início e o fim
  estão marcados), "Quantidade movimentada" (operador "Operador da quantidade": "Maior que", "Maior ou igual a", "Igual a", "Menor ou
  igual a", "Menor que"; campo "Ex.: 40"; "Considera o valor sem sinal: 40 encontra +40 e -40."). Cap. 7.
- **Kardex, exportar de verdade** (`components/estoque/KardexExportDialog.tsx`, `MaterialHistory.tsx:763,770`): "Exportar" →
  "PDF"/"Excel" abre "Exportar Kardex (PDF)"/"(Excel)", "Escolha o recorte do extrato. Mudar os filtros aqui não altera os filtros da
  tela."; botão "Exportar PDF"/"Exportar Excel"; avisos "Kardex exportado em PDF"/"em Excel". O PDF abre em aba nova (`openPdfInTab`
  com a janela pré-aberta). Recorte acima de 20.000 linhas: "Recorte grande demais para a tela" (`fetchStockMovements.ts:53`). Cap. 7.
- **"Como funciona?"** do Kardex (`:1480-1600`): resume colunas, tipos e filtros. Só citado.
- **Linha de venda aberta**: "Cliente:", itens, "Formas de Pagamento", "Total do Pedido:" (`:1341-1420`). Cap. 7.
- **Colunas "Usuário" e "Pedido"** da linha (`:1210-1218,1296-1310`): o primeiro nome de quem lançou e "#<número do pedido>". Cap. 4.
- **"Editar" do material grava "Edição Manual"** sem observação (`pages/Materiais.tsx:1122-1133`; a nota 1.59.159 manteve os milhares
  do "Quantidade em Estoque"). **"Movimentar estoque": a observação é OPCIONAL** (`StockMovementDialog.tsx:348-350`, "Descrição /
  observação (opcional)"): a fala diz "tem o campo de observação", não "pede o motivo". Cap. 5.
- **Relatório, cartões abertos**: "Total Vendido" ("Preço médio de venda", "Qtd. Vendida", "Materiais vendidos", "Material que mais
  vendeu"), "Lucro" ("Lucro s/ vendas total", "Resultado total", "Margem", "Margem média", "Material mais lucrativo") e, no fim,
  "Distribuição por forma de pagamento" ("Dinheiro", "Pix/Transferência", "Saldo", "Em aberto"; "Considera os pedidos do período; não
  segue o filtro de material.") (`InventoryReport.tsx:650-754`, `materials.json` `report.kpiPayment*`). Cap. 8.
- **Relatório, filtros** (desktop): chips "Fornecedores", "Clientes", "Usuários", "Grupos" (na gaveta do celular: "Usuário", "Grupo"),
  "Por material"/"Por grupo" (`aria-label` "Ver por material"/"Ver por grupo") com "Subtotal <grupo>", chip "Ocultar itens zerados"
  (`aria-pressed`, guarda a escolha no aparelho), ordenar pelo título de qualquer coluna, linha "TOTAL". Cap. 11.
- **Resultado nunca negativo** (`utils/profitDisplay.ts:13-21`, `components/reports/ProfitCellTooltipContent.tsx:22-43`): mostra R$ 0,00 e
  o balão traz a conta ("… vendidos", "− … comprados", "(prejuízo)", "Lucro exibido: R$ 0,00"). Cap. 9.
- **Relatório, exportar de verdade**: o botão "Exportar Relatório" abre uma aba com HTML (`utils/inventoryReportHtmlGenerator.ts`,
  `window.open` + `document.write`), com período e filtros da tela; com fornecedor marcado sai só compras. Cap. 13.
- **Posição de Estoque, hora e grupo**: campo "Hora" (`<input type=time>`, `aria-label` "Hora") muda o instante da foto; "Por
  grupo" com "Subtotal <grupo>"; rodapé com as quatro frases (`PosicaoEstoque.tsx:803-808`). Cap. 12.
- **Janela "Exportar estoque"**: cada coluna é um checkbox (nome = rótulo da coluna), "Grupos", "Materiais" com "Marcar todos" e
  "Desmarcar todos", "N de M materiais" (`StockExportDialog.tsx:288-430`). Cap. 13.
- **Coluna "Tabelas de Preço"** (`PriceTableSidebar.tsx`): menu "..." da tabela ganhou "Duplicar tabela", "Fixar para meus pedidos e
  tickets", "Definir como principal da empresa"; é assunto da T3. O botão "Posição de Estoque" do cabeçalho só existe sem várias
  tabelas (`Materiais.tsx:2360-2370`): citado em fala, não gravado.
- **"Sem histórico de compra"** (`materials.json` `avgCostPaidNoHistory`; `Materiais.tsx:3236-3252`): triângulo amarelo no "Preço médio
  pago" de material com saldo e sem compra. O mundo não tem esse material: só falado.
- Menu "Fiscal & Ambiental": "Estoque Fiscal" agora abre em `/fiscal-ambiental/estoque-fiscal/posicao` (T17); só citado no cap. 13.
