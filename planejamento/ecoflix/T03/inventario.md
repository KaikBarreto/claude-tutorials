# Inventário · T3 Materiais e tabelas de preço (EcoSistema 1.59.154)

Levantado em 10/11/2026 contra `/home/claude/ecoflix/app-src-1.59.154/` (`src/config/version.ts:16`, `APP_VERSION = "1.59.154"`).
Leitura estática, só o que a aula usa. Caminhos relativos a `src/`. **mat** = `i18n/locales/pt-BR/materials.json`.
O guia embutido no app (`components/help-center/helpCenterData.generated.ts`, seções `t3-c01` a `t3-c11`) serviu de mapa;
onde ele e o código discordam, vale o código (marcado **≠ guia**).

## 1. Menu e rota
- Menu lateral "Materiais" › "Estoque" → `/materiais` (`config/routes.ts:446-456`; permissão `screen_estoque`, `App.tsx:390-394`).
- Página `pages/Materiais.tsx`. Migalha "Materiais" › "Estoque"; título "Estoque", subtítulo "Gerencie os materiais do
  estoque"; botão "Ver tutorial" (EcoFlix, `components/TutorialButton.tsx:38`) (`:2314-2338`).
- Backend da tela: `materials` (`is_archived = false`, `:364-390`), códigos ativos (`:419-448`), `purchase_items` +
  `purchases` concluídas (preço médio pago, `:451-496`), `price_tables`, `price_table_items` (`hooks/usePriceTables.tsx`),
  `material_groups` (`hooks/useMaterialGroups.ts`), preferências de pagamento (`multiple_price_tables_enabled`,
  `hooks/usePaymentPreferences.ts:75,93`; **padrão ligado**).

## 2. Tela Estoque (`pages/Materiais.tsx`)
- **Coluna "Tabelas de Preço"** (computador, preferência ligada; `components/PriceTableSidebar.tsx:159-288`): "Como funciona"
  (?); um botão por tabela (estrela = principal; corrente + selo "+4%" = vinculada); "Nova Tabela" (tracejado); "Posição de
  Estoque". Menu "..." da tabela: "Configurações" e, fora da principal, "Excluir" ("Não é possível excluir a tabela padrão").
- **Barra** (`:2355-2440`): "Movimentar estoque" (cheio; `action_edit_delete_materials` ou admin), "Editar Tabela",
  "Grupos" | "Exportar" ▾ (`action_export_reports`), "Zerar Estoque" (vermelho; `action_zero_stock`).
- **Cartões** (`:2581-2631`): "Peso Total em Estoque" (soma, rótulo "Kg"), "Total Pago", "Projeção de Vendas". **Seguem o
  filtro de materiais e grupos** (`:1851-1885`). Sem `action_view_financial_values` ("Ver Totais e Valores Financeiros",
  `config/routes.ts:237`): cadeado + "Sem permissão" (`:224-236`).
- **"Lista de Materiais"** (`:2758-3256`): "Exibindo preços da tabela: <nome>"; filtro "Todos os Materiais" ▾ (seções
  "Grupos", com a contagem, e "Materiais"; marcar um grupo marca todos os materiais dele; com tudo marcado, clicar num grupo
  o tira; `:683-744`, `:2773-2873`); "Importar planilha"; "+ Novo Material"; busca "Buscar material por código ou nome...";
  10 por página. Colunas: caixinha, "Código", "Nome" (bolinha + nome do grupo embaixo), "Estoque Atual" (+ unidade),
  "Valor Pago", "Preço médio pago" (selo "estimativa"; triângulo âmbar + "⚠ Sem histórico de compra: usando o preço
  cadastrado, pode não refletir o custo real."), "Preço de Compra", "Preço de Venda", "Ações" (...): "Movimentar estoque",
  "Transferir estoque", "Editar", "Excluir" (`:3180-3224`). Sem permissão de valores: cadeado + "***" (`:231-234`).
- **Preço por tabela** (`:500-568`; `lib/precos/linkedTablePrice.ts:126-163`): "Preço de Compra" segue a tabela escolhida
  na coluna (vinculada = principal × variação); **"Preço de Venda" é sempre o do material** (`:513-514`).

## 3. Novo Material / Editar Material (`pages/Materiais.tsx:1887-2309`; diálogo `:2444-2515`)
- Título "Novo Material" / "Editar Material"; "Cancelar" e "Criar" / "Atualizar". Com o módulo de Produção: abas "Dados" e
  "Produção" (🔒 producao, `:2473-2508`). Painel "Resumo" (nome ou "Novo material", código · unidade, "Compra", "Venda",
  "Estoque", "Grupo", "NCM"; `:2250-2285`).
- "Identificação" ("Como o material aparece nas operações e documentos."): **"Código"** (placeholder "Será gerado: 16";
  **só dígitos; zeros da frente somem enquanto se digita**, `:1906-1916`), "Prefixo" ("Ex: P"), "Unidade" (padrão "Kg";
  lista "Mais utilizados"/"Menos utilizados", `constants/materialUnits.ts:7-28`), "Fica assim: 16" + "O prefixo aparece na
  tela, no comprovante e na nota fiscal. O número no banco não muda." (`:1945-1957`), **"Nome \*"**,
  **"Identificação/Produto Fiscal"** ("Ex: SUCATA DE ALUMÍNIO"; legenda "Só preencha se o nome na nota fiscal for diferente
  do nome do material."; ajuda (?) "Como funciona:" · "Para que serve: o nome que sai na nota fiscal, quando ele for
  diferente do nome que você usa no dia a dia." · "Exemplo: no sistema o material é "Latinha", mas na nota precisa sair
  "SUCATA DE ALUMÍNIO"." · "Se deixar vazio: a nota sai com o nome normal do material, como já funciona hoje.").
- "Valores e estoque" ("Preços usados na tabela selecionada e saldo inicial."): "P. Compra", "P. Venda" (R$, até 3 casas),
  "Quantidade em Estoque" ("0,000").
- "Fiscal e organização" ("Classificações usadas em estoque, nota e MTR."): **"NCM (Nota Fiscal)"** (máscara "0000.00.00";
  botão (?) "Selecionar NCM padrão"; legenda "Código NCM usado na emissão de notas fiscais"), **"Grupo"** ("— Sem grupo —" +
  botão "+" "Criar grupo"). "Resíduo do MTR" só se a UF da empresa tem sistema ambiental ativo (`hooks/useMtrSistemaLeve.tsx`);
  "Tipo do item no SPED Fiscal" só com `get_sped_rollout_context` ligado. A aula não fala dos dois.
- **Salvar** (`:832-1202`): código vazio = maior código **ativo** + 1 (`:886-893`, consulta `:419-448`); "Código deve ser um
  número maior que zero"; "Este código já está sendo usado por outro material"; "NCM incompleto. Informe os 8 dígitos no
  formato 0000.00.00."; venda menor que compra **pede confirmação** ("Preço de venda abaixo do custo" / "Salvar mesmo
  assim", `:853-872`, `:2520-2552`; **≠ guia e fonte**, que falam em bloqueio). Toasts "Material criado!" / "Material
  atualizado!". Criar: `INSERT materials` (com `current_stock`). Editar com a principal: `UPDATE materials` + upsert em
  `price_table_items` da principal; saldo alterado: `rpc adjust_material_stock_atomic` (`p_reason` "EDICAO_MANUAL").

## 4. Seletor de NCM (`components/notas-fiscais/NcmSelectorModal.tsx`; textos `invoices.json` › `ncmSelector`)
- "Selecionar NCM para Materiais Recicláveis"; busca "Buscar por código NCM ou descrição..."; cartões por categoria (selo +
  "1 NCM"/"N NCMs"): código, descrição, nota em itálico (`tax_notes`), botão "Selecionar"; vazio: "Nenhum NCM encontrado".
- Backend: `ncm_presets` (tabela global: `ncm`, `description`, `material_category`, `tax_notes`). Escolher grava só os 8 dígitos.

## 5. Grupos (`components/materiais/MaterialGroupsDialog.tsx`, `QuickMaterialGroupDialog.tsx`, `MaterialGroupForm.tsx`)
- "Grupos de materiais" ("Organize seus materiais em grupos por cor e ícone."): linhas com círculo colorido + ícone, nome,
  "Editar grupo" (lápis), "Excluir grupo". Bloco "Novo grupo": "Nome \*" ("Ex: Metais, Plásticos, Papéis"), "Cor" (`<input
  type="color">` nativo), "Ícone" (círculo; abre grade de 50 ícones, ex.: `car`, `wrench`, `truck`, `flame`), "Adicionar" →
  "Grupo criado" (vazio: "Informe o nome do grupo"). Excluir: "Os materiais deste grupo ficarão sem grupo. Nenhum dado de
  estoque é apagado."
- O "+" do campo Grupo abre "Novo grupo de material" (mesmos campos, "Salvar") e já seleciona o grupo no material.
- Backend: `material_groups` (insert/update/delete).

## 6. Editar Preços em Massa (`components/BulkPriceEditModal.tsx`, botão "Editar Tabela")
- "Editar Preços em Massa" ("Altere os preços de compra e venda de todos os materiais"). Esquerda: "Tabelas disponíveis"
  ("Buscar tabela...", selo "Padrão"). Direita: "Editando tabela de preços" + nome + "Padrão"; aviso "Alterações na tabela
  principal serão refletidas em todas as tabelas vinculadas."; busca "Buscar por código ou nome..."; resumo "N material(is)
  com alterações pendentes"; grade "Cód.", "Material", "Compra (R$)", "Venda (R$)" (célula alterada destacada; vinculada
  mostra "Variação" e cadeados). "Cancelar" / "Salvar" (`:1135-1480`, `:1888-1905`).
- Salvar na principal: `UPDATE materials` dos alterados + `rpc save_price_table_items` (`:130`, `:702-790`) → "Preços
  atualizados! As tabelas vinculadas serão recalculadas automaticamente."; nada mudado: "Nenhuma alteração para salvar";
  venda < compra: confirmação "Preço de venda abaixo do custo" (lote).

## 7. Nova Tabela de Preços (`components/PriceTableSettingsModal.tsx`; `hooks/usePriceTables.tsx:53-87`)
- "Nova Tabela de Preços": "Nome da Tabela" ("Ex: Atacado, Varejo, Premium..."), caixa "Vincular à tabela principal" →
  "Tipo de variação" ("Porcentagem" | "Valor"), "Valor da variação" (%), "Direção da variação" ("Aumenta" | "Diminui"),
  "Exemplo de cálculo:" "Preço base: R$ 10,00" / "Preço nesta tabela: R$ 10,40 (+4%)". "Cancelar" / "Criar Tabela".
- `INSERT price_tables` (`is_linked`, `linked_to_table_id` = principal, `variation_*`) → "Tabela de preço criada com
  sucesso!"; a tabela nova fica selecionada.

## 8. Vínculo da tabela ao parceiro (`pages/ClientsSuppliers.tsx`, `components/EntityFormDialog.tsx`)
- Menu "Clientes e Fornecedores" → abas "Clientes" | "Fornecedores" | "Visão geral" (`:193-197`); busca "Buscar
  fornecedor..."; clicar no parceiro abre a ficha ("Visão geral", "Pedidos", ..., "Preços"; selo "1 preço personalizado")
  com "Editar" (`clients-suppliers/ClientsListView.tsx:220-305`).
- "Editar Fornecedor", aba "Dados de Contato": aviso do parceiro duplo "Mudanças em nome, CPF/CNPJ, contato, endereço e
  tabela de preços padrão refletem automaticamente no cadastro de cliente vinculado." (`clients.json` › `dual.syncWarning`);
  campo **"Tabela de Preços Padrão"** (`EntityFormDialog.tsx:1335-1347`); "Salvar" → "Fornecedor atualizado!".
  Backend: `UPDATE suppliers.default_price_table_id` (e do lado cliente, pelo vínculo duplo).

## 9. Prioridade do preço no pedido (`components/OrderFormInputs.tsx:382-455`, `pages/Purchase.tsx`)
- Ordem no código: 1) preço personalizado do parceiro (`entity_custom_prices`) → toast "Preço especial aplicado para
  <material>"; 2) tabela escolhida no pedido (personalizada por material, vinculada calculada ou item da tabela) → "Preço da
  tabela aplicado para <material>"; 3) preço do material. Bate com a fonte.
- Compra: "Financeiro" › "Caixa" › "Nova Compra" (`pages/Caixa.tsx:2985-2997`) → `/compra`; **sem caixa aberto:** "Abra o
  caixa antes de realizar compras" e volta ao caixa (`pages/Purchase.tsx:2099-2121`). Fornecedor: "Selecionar Fornecedor"
  ("Buscar por nome, apelido, CPF/CNPJ ou telefone..."); escolher o fornecedor troca "Tabela de Preços" para a padrão dele
  (`:1682-1683`, `:4506-4511`); material: "Escreva o nome ou código do material"; preço em "Valor/kg". Escolher o material
  já preenche o preço e mostra o toast (sem precisar incluir o item). A tela grava rascunho em `order_drafts`
  (`hooks/useOrderCache.ts:1379`).

## 10. Movimentar, transferir, zerar
- **Movimentar estoque** (`components/StockMovementDialog.tsx`): "Registre uma entrada ou saída manual de material com
  quantidade e observação."; "Entrada" (verde) | "Saída" (vermelho); "Material \*" ("Escreva o nome ou código do material");
  "Quantidade \*"; "Estoque de <material>": "Estoque atual" → "−2 Kg" → "Após a movimentação" (vermelho se negativo);
  "Descrição / observação" ("Ex: ajuste de inventário, sobra de produção, quebra..."); "Cancelar" / "Registrar saída".
  `rpc adjust_material_stock_atomic` (`p_reason` "SAIDA", `p_description`) → "Saída de 2 Kg de Radiador de cobre".
- **Transferir Estoque** (`components/TransferMaterialDialog.tsx`): "Transferir quantidade de Radiador de cobre (Código: 70)
  para outro material"; "Estoque Atual de Radiador de cobre" (118 Kg); "Material de Destino \*"; "Quantidade a Transferir
  (Kg) \*"; "Cancelar" / "Transferir". `rpc transfer_material_stock` → "Transferido 8 Kg de Radiador de cobre para Ferro misto".
- **Zerar Estoque** (`components/materiais/ClearStockSelectionDialog.tsx`): "Zerar Todo o Estoque" ("Selecione os materiais
  que deseja zerar, individualmente ou por grupo. Por padrão, todos estão marcados."), "Atenção: Ação irreversível",
  "Marcar todos"/"Desmarcar todos", "N de M selecionados", "Grupos", "Materiais", "Já zerado", "Para confirmar, digite
  Zerar todo o meu estoque:" ("Digite para confirmar"), "Cancelar" / "Zerar selecionados (N)". Sem desfazer. A aula só mostra.

## 11. Exportar (`pages/Materiais.tsx:1640-1850`)
- "Exportar" ▾: "Exportar Estoque" › "Estoque (PDF)", "Estoque (Excel)" | "Tabela de Preços" › "Tabela de Preços (PDF)".
- Estoque: "Exportar estoque (PDF)" ("Escolha os materiais e as colunas do arquivo. Sua última seleção fica salva para a
  próxima exportação."), "Colunas do arquivo", "Grupos", "Materiais", "Cancelar" / "Exportar"
  (`components/estoque/StockExportDialog.tsx:288-399`). PDF "Lista de Materiais" (jsPDF, aba nova, `utils/materialsExport.ts`)
  → "Lista exportada como PDF!"; Excel baixa direto → "Lista exportada como Excel!".
- Tabela de preços: "Exportar tabela de preços em PDF" (busca, "Ordenar por": "Código (crescente)", ...; "Exportar PDF";
  `components/materiais/SeletorMateriaisExportDialog.tsx:192-312`) → "Formato da tabela de preços" ("Escolha o formato da
  tabela de preços que deseja gerar.": "A4" Folha | "Térmico") → PDF com os dados da empresa, título "TABELA: <NOME DA
  TABELA>" (ou "TABELA DE PREÇOS" na "Principal"), "Cód. | Material | Preço/KG" (preço de **compra** da tabela escolhida na
  coluna; `utils/priceTableGenerator.ts:607-723`) → `Tabela "<nome>" exportada!`. Pop-up bloqueado: "Pop-up bloqueado.
  Permita pop-ups para este site."

## 12. Excluir (`pages/Materiais.tsx:1312-1393`, `:3293-3329`; `hooks/useUndoToast.ts`)
- "Confirmar Exclusão": "Tem certeza que deseja excluir o material **Radiador de cobre** (Código: 70)?" + "Atenção: Este
  material possui 110 Kg em estoque." · "Cancelar" / "Sim, Excluir".
- **Arquiva**: com saldo, `INSERT stock_movements` tipo `EXCLUSAO` ("Arquivamento do material <nome>"); `UPDATE materials`
  `is_archived` true, `archived_at`, `current_stock` 0. Some da lista; compras, vendas e movimentos ficam. Toast
  `"Radiador de cobre" excluído` + **"Desfazer"** (5 s) → desarquiva, devolve o saldo, apaga o `EXCLUSAO` →
  `"Radiador de cobre" restaurado!`. O código do arquivado volta a ficar livre (`:418-448`).

## 13. Importar planilha (`components/materiais/ImportMaterialsSpreadsheetDialog.tsx`)
- "Importar materiais por planilha" ("Baixe o modelo, preencha uma linha por material e envie o arquivo para conferir antes
  de cadastrar."): "1. Baixe o modelo" + "Baixar modelo"; "2. Envie a planilha preenchida" + "Arraste a planilha aqui ou
  clique para selecionar" / "O sistema confere tudo antes de cadastrar." / "Aceita somente o modelo .xlsx, com até 5 MB."
  A aula só abre e fecha (nenhum arquivo). Tudo ou nada e reenvio sem duplicar: confirmados no guia (`t3-c03`); o código
  da gravação fica no backend (não lido aqui).
