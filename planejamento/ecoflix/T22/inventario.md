# Inventário · T22 Gerencial: matriz e filiais (EcoSistema 1.59.154)

Código lido: `/home/claude/ecoflix/app-src-1.59.154/` (só leitura). Caminhos relativos a `src/`, exceto `supabase/...`.
Rótulos entre aspas = texto exato do código (pt-BR). Gravação em 1280×800 (`xl` vale; `2xl` não).

## 0. Módulo, menu e quem é quem
- Menu lateral: grupo **"Gerencial (Filiais)"** com "Dashboard" (`/gerencial`), "Financeiro" (`/gerencial/financeiro`), "Estoque"
  (`/gerencial/estoque`), "Assinaturas" (`/gerencial/assinaturas`), "Configurações" (`/gerencial/configuracoes`)
  (`config/routes.ts:479-490`; `App.tsx:582-606`). 🔒 módulo `modulo_gerencial` (`hooks/useCompanyModules.tsx:32-36`), contratado na
  matriz; a filial só precisa da assinatura própria (o vínculo fica em Configurações › Empresa).
- Grupo (`hooks/useCompanyGroup.ts`): `company_groups` (dono = matriz, `invite_code`, `invite_code_expires_at`,
  `require_transfer_approval`) e `company_group_members` (filiais, `status` active/removed). Matriz = `isOwner`.
- Sem grupo, todas as telas do Gerencial mostram "Módulo Gerencial" · "Crie um grupo gerencial para conectar suas unidades e ter
  uma visão consolidada de financeiro, DRE e estoque." · botão "Configurar Grupo" (`components/gerencial/GerencialEmptyState.tsx`).

## 1. Configurações do grupo (`pages/GerencialConfiguracoes.tsx`)
- Sem grupo (`:170-213`): "Configurações do Grupo" · "Crie um grupo para gerenciar múltiplas unidades"; cartão "Criar Grupo
  Gerencial" · "Crie um grupo e compartilhe o código de convite com as filiais"; "Nome do Grupo" ("Ex: Grupo Reciclagem Silva");
  **"Criar Grupo"** → aviso "Grupo gerencial criado com sucesso!" (`useCompanyGroup.ts:89-118`: RPC `generate_group_invite_code` +
  `INSERT company_groups`). Sem nome: "Digite o nome do grupo".
- Com grupo (`:484-533`): "Gerencie as unidades e padronizações do grupo {nome}"; botão "Como funciona" (janela "Como funciona o
  Gerencial de Filiais", `components/gerencial/GerencialHowItWorksModal.tsx`: "O código expira em 30 dias. Regenere quando
  necessário."; "Relação Matriz × Filial"); abas "Unidades", "Catálogo de Materiais", "Tabelas de Preço", "Clientes e
  Fornecedores", "Categorias Financeiras", "Transferências" (`:43-48`).
- Aba Unidades: passo a passo "Configure o grupo" · "n de 5 etapas concluídas" ("Vincular filiais", "Catálogo de Materiais",
  "Tabelas de Preço", "Clientes e Fornecedores", "Enviar ativos para filiais"; some com tudo feito, `GerencialSetupChecklist.tsx:89-160`);
  cartão **"Código de Convite"** · "Compartilhe este código com as filiais que deseja vincular", código em destaque, copiar ("Código
  copiado!"), gerar outro ("Gerar novo código (válido por 30 dias)"), "Válido até dd/mm/aaaa" (`:228-253`); **"Unidades Ativas (n)"**:
  a matriz com o selo "MATRIZ" e "Desde"; sem filial: "Nenhuma filial vinculada ainda. Compartilhe o código de convite acima.";
  cada filial com **"Enviar Ativos"** e lixeira → "Remover unidade?" · "{nome} será removida do grupo e você perderá acesso aos dados
  dela." · "Cancelar" / "Remover" (`:255-333`; remover = `status` removed, `useCompanyGroup.ts:137-150`); "Histórico de Envios" ·
  "Últimos 20 envios de ativos para filiais" ("→ {filial}", "n materiais · n categorias · …", `:335-392`).
- Aba Transferências (`:401-476`): **"Exigir aprovação em transferências"** · "Quando ativo, o destino precisa confirmar antes da
  transferência ser executada"; "Usar estoque de outras unidades na venda"; a lista de transferências (seção 6).

## 2. Lado da filial (`components/settings/SettingsCompanyContent.tsx:296-370`)
- Rodapé do menu: "Configurações" (`components/layout/SidebarMenuContent.tsx:806-820`) → aba "Empresa" (`pages/Settings.tsx:37,73`);
  abaixo dos dados da empresa, cartão **"Filial"** · "Se esta empresa é uma filial, vincule-a à empresa-mãe usando o código de
  convite"; chave **"É Filial"** · "Ative para vincular esta empresa a um grupo gerencial"; "Código de Convite" · "Solicite o código
  ao administrador da empresa-mãe", campo "GRP-XXXXXX" (maiúsculas), **"Vincular"** → "Empresa vinculada ao grupo com sucesso!" (RPC
  `join_group_by_invite_code`, `useCompanyGroup.ts:121-134`). Vinculada: "Vinculada ao grupo" · {nome do grupo} · selo "Ativa".

## 3. Dashboard Gerencial (`pages/GerencialDashboard.tsx`)
- "Dashboard Gerencial", selo "MATRIZ" + nome da matriz, "{grupo} • n unidades" (`:274-292`); período ("Este mês" padrão; "Mês
  passado" etc., `i18n/locales/pt-BR/common.json:2-10`); seletor "Todas as Unidades" (`components/gerencial/BranchUnitSelector.tsx`).
- Cartões (`:234-267`): "Receita Total" (vendas + outras entradas), "Despesa Total" (compras + saídas), **"Lucro Líquido" = vendas −
  compras** (sem as despesas: não fecha com receita − despesa), "Estoque Total"; setinha com a variação sobre o período anterior.
- "Receita vs Despesa por Unidade" e **"Ranking por Lucro"** (barras; nome cortado em 15 letras, "★" na matriz, `:223-232,358-395`);
  **"Resumo por Unidade"**: "Unidade", "Receita", "Despesa", "Lucro" (receita − despesa), "Margem" (`:398-448`).
- RPCs: `get_group_financial_summary` (por empresa: `total_sales`, `total_purchases`, `total_cash_income/expense`,
  `total_bank_income/expense`), `get_group_stock_summary`, `get_group_expense_categories` (`hooks/useGroupFinancials.ts:123-185`).

## 4. Financeiro Gerencial (`pages/GerencialFinanceiro.tsx`)
- "Financeiro Gerencial" · "Relatório financeiro consolidado de todas as unidades"; período; "Todas as Unidades"; abas "Dashboard",
  "DRE", "Histórico" (`:159-161,1286-1330`). Na DRE: **"Consolidado"** | **"Comparativo"** (`:1166-1181`).
- Consolidado (`:718-1056`): "DRE — Todas as Unidades"; **"Regime de Caixa"** | **"Regime de Competência"** (padrão: competência,
  `:187`; dicas: "Considera todo o dinheiro que entrou e saiu no período. ..." / "Considera só o custo do material que você realmente
  vendeu no período. ..."); "Exportar"; "(+) Receita Operacional" · "Vendas de Material"; caixa: "(-) Custo Operacional" · "Compras de
  Material" e "(=) Resultado de Caixa"; competência: "(-) Custo Operacional (CMV)" · "CMV (Custo da Mercadoria Vendida)" e "(=) Lucro
  Bruto"; "Margem Bruta: x%"; aviso (só em competência e com estoque sem custo) **"Há material em estoque sem custo de compra
  cadastrado — o CMV pode estar subestimado."** (`:850-857`); "(-) Despesas Operacionais (OPEX)" · "Total Despesas"; "(+) Outras
  Receitas" (só se houver); **"(=) Resultado do Período"** · "Superávit"/"Déficit"; "Patrimônio Operacional Atual".
- Comparativo (`:1058-1135`): "DRE Comparativo por Unidade", "Linha" + uma coluna por unidade (nome cortado em 12 letras, selo
  "MATRIZ"), linhas "Vendas", "(-) Compras (CMV)", "Receita Líquida", "(-) Despesas Operacionais (OPEX)", "Resultado". **"Compras
  (CMV)" mostra as compras do período nos dois regimes** (`:1102`).
- RPCs: `get_group_financial_dre_summary` (`_regime`), `get_group_patrimony_summary`, `get_dre_expenses_by_group`,
  `get_group_order_history_lines`, `get_group_financial_categories`.

## 5. Estoque Gerencial (`pages/GerencialEstoque.tsx`)
- "Estoque Gerencial" · "Visão consolidada do estoque de todas as unidades do grupo"; abas "Visão Geral", "Posição de Estoque",
  "Histórico de Materiais", "Relatório de Estoque", "Transferências" (contador de pendentes) (`:20-60,84-136`).
- Visão Geral (`components/gerencial/GerencialEstoqueVisaoGeral.tsx`): "Valor Total em Estoque", "Unidades", "Materiais Distintos"
  (`:575-600`); cartão por unidade com "Valor total em estoque" e "n materiais" (`:116-131`); **"Tabela Unificada de Materiais"**:
  "Material", uma coluna por unidade, "Total", "Ações" (⋯ "Corrigir saldo", "Transferir entre unidades", "Transferir entre
  materiais", `:618-728`). RPC `get_group_inventory_report_data`. "Corrigir saldo" ajusta o estoque de uma unidade
  (`GroupAdjustStockDialog.tsx:242-243`, RPC `adjust_material_stock_atomic`).
- Posição de Estoque: "Código", "Material", "Unidade", "Saldo", "Custo médio", "Valor em estoque", "Projeção venda"
  (`GerencialEstoquePosicao.tsx:307-313`). Histórico de Materiais: "Usuário", "Data/Hora", "Tipo" ("Compra", "Venda",
  "Transferência"…), "Filial", "Nº Pedido", "Material", "Estoque Inicial", "Movimento" (`GerencialEstoqueHistorico.tsx:60-83,568-576`).
  Relatório de Estoque: "Qtd. Comprada", "Valor Comprado", "Preço Médio Compra", "Qtd. Vendida", "Valor Vendido", "Lucro", "Margem"
  (`GerencialEstoqueRelatorio.tsx:800-809`; `i18n/locales/pt-BR/materials.json:225-236`).

## 6. Padronizar e transferir
- Catálogo de Materiais (`components/gerencial/GerencialMaterialCatalog.tsx`): "Catálogo de Materiais do Grupo" · "Cadastre os materiais
  que serão compartilhados com todas as filiais. ..."; **"Importar do Estoque da Matriz"** → "n material(is) importado(s) do estoque"
  (RPC `import_owner_materials_to_group`); cada material com a unidade, "NCM …" e "n vínculo(s)" ou "Sem vínculos".
- Tabelas de Preço do Grupo (`GerencialPriceTables.tsx:110-140,222-262`): ao abrir a aba, importa sozinha as tabelas da matriz (RPC
  `import_owner_price_table_to_group`). Clientes e Fornecedores da Matriz (`GerencialClientsSuppliers.tsx:101-150`): "Marque os
  clientes e fornecedores que ficarão disponíveis para as filiais importarem. A marcação é imediata." → "Disponibilizado para
  filiais" (RPC `toggle_group_shared_entity`). Categorias Financeiras da Matriz (`GerencialCategories.tsx:87-150`): ao abrir, compartilha
  as categorias da matriz (RPC `import_company_categories_to_group`).
- **"Enviar Ativos para {filial}"** (`PushAssetsModal.tsx:88-245`): "Selecione quais categorias enviar. Itens já existentes na filial
  serão ignorados."; "Categorias" · "Desmarcar todos"; "Materiais", "Categorias Financeiras", "Tabelas de Preço", "Clientes",
  "Fornecedores" com "n disponível(is)"; "Sobrescrever preços existentes"; "Cancelar" / **"Confirmar Envio"** → "n novo(s)" por linha,
  "n ativo(s) enviado(s) para {filial}", "Fechar" (RPC `push_group_assets_to_company`, grava `group_push_audit`).
- Transferências (`GerencialTransfers.tsx:155-341`): "Transferências Inter-Unidades" · "Transfira estoque entre unidades do grupo. Os
  materiais precisam estar vinculados ao catálogo."; "Nova"; "Executar todas (n)"; cada linha "origem → destino", selo "Pendente" /
  "Concluída" / "Cancelada", "material — qtd un", data, observação; pendente: "Cancelar" / "Executar" → com aprovação: "Confirmar
  execução?" · "Este grupo exige aprovação antes de executar transferências. Confirme que o destino está ciente e de acordo com esta
  movimentação de estoque." · **"Confirmar e Executar"** → "Transferência executada com sucesso" (`hooks/useGroupTransfers.ts:140-147`).
- Formulário (`GerencialTransferForm.tsx:380-725`): "Nova transferência em lote", "Passo 1 de 2", "Origem" ("Unidade de origem..."),
  "Destino" ("Unidade de destino..."), "Materiais" ("Buscar material...", "sem vínculo"), "Quantidade", "Observações (opcional)" ("Ex:
  Transferência para suprir demanda..."), "Resumo"; com aprovação, a matriz vê "Este grupo exige aprovação: o estoque não se move
  agora. ..." e o botão **"Solicitar 1 transferência"** (sem aprovação: "Transferir"; na filial: "Enviar") → "Solicitação criada —
  aguardando aprovação" · "O estoque só se move quando você executar na lista abaixo". RPCs `create_group_transfer_and_execute`
  (matriz), `create_group_transfer_as_member` (filial), `execute_group_stock_transfer`.

## 7. Assinaturas e fatura única
- "Assinaturas do grupo" · "Acompanhe as assinaturas de todas as unidades e pague tudo de uma vez numa única fatura na matriz"
  (`pages/GerencialAssinaturas.tsx:44-58`); "Total do grupo · soma de 2 unidades", valor "/mês", **"Pagar tudo de uma vez"**
  (`components/gerencial/GerencialAssinaturas.tsx:426-445`); "Unidades": nome, "Matriz" / "Filial", "Ativa", "Personalizado · Mensal ·
  vence em dd/mm/aaaa", valor, "Gerenciar" (`:447-540`). RPC `get_group_subscription_summary`.
- Checkout do grupo (`pages/Checkout.tsx:144-148,1229-1470`; `components/checkout/CheckoutLayout.tsx`): "Pagamento do grupo",
  "Pagamento do grupo · 2 unidades", "Unidades cobradas juntas", **"Ao pagar, as cobranças individuais das unidades são canceladas e
  substituídas por esta fatura única na matriz."** (`:664-694`); "Forma de pagamento": "Cartão de Crédito", "PIX", "Boleto"; "Gerando
  QR Code PIX..."; "Pagamento Confirmado!" · "As cobranças das unidades agora são feitas nesta fatura única na matriz." · "Voltando
  para as assinaturas do grupo..." (`:860-1100`).
- Edge `create-group-payment` (`supabase/functions/create-group-payment/index.ts:1-40,740-806`): cria a cobrança do total na matriz
  (Asaas, `externalReference` `group:{id}`) e depois cancela as assinaturas individuais de todas as unidades; ciclos diferentes =
  recusa (`GROUP_MIXED_CYCLE`).
