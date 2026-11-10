# Inventário · T11 Produção (EcoSistema 1.59.154)

Código: `/home/claude/ecoflix/app-src-1.59.154/` (só leitura). Caminhos relativos a `src/`. Só o que a aula usa.
A cópia não tem `supabase/migrations`: o comportamento das RPCs vem do cliente e da Central de Ajuda do próprio app
(`components/help-center/helpCenterData.generated.ts`, entradas `t11-c01` a `t11-c14`); onde a Ajuda e o código
discordam, vale o código (lista no fim).

## 0. Onde fica e quem pode
- Menu lateral **"Materiais"** › **"Produção"** (`config/routes.ts:448,455`), rota `/producao`, permissão de tela
  `screen_producao` (`App.tsx:395-398`). Caminho no topo **"Estoque" › "Produção"**, título **"Produção"**, descrição
  "Fichas técnicas, ordens de produção e custo por peça" (`pages/Producao.tsx:54-63`).
- Abas na coluna da esquerda (`pages/Producao.tsx:16-23`): **"Ordens de Produção"**, "Conversão", **"Fichas Técnicas"**,
  "Máquinas", **"Relatório"**, **"Configurações"**. A aula usa as quatro em negrito ("Conversão" e "Máquinas" ficam
  fora da fonte).
- Ações (Configurações › Usuários e Permissões, `config/routes.ts:218-219`): **"Gerenciar Fichas Técnicas"** (fichas e
  Configurações: `RecipeList.tsx:45`, `RecipeFormDialog.tsx:113`, `ProductionSettings.tsx:95`) e **"Registrar Produção"**
  (criar, lançar, finalizar, excluir: `ProductionOrderDialog.tsx:110`, `ProductionKanbanBoard.tsx:626`,
  `ProductionOrderDetail.tsx:127`, `FinalizeProductionDialog.tsx:47`).
- 🔒 Sem o módulo: cartão **"Ainda não está no seu plano"**, nome "Produção", "Saiba o custo real de cada peça que você
  produz", "Adicione à sua assinatura por apenas R$ X/mês", "Sem cobrança agora — entra só na sua próxima fatura." e o
  botão **"Ativar produção"** (`components/ModuleUpsellScreen.tsx:113-160`, `lib/moduleUpsellCopy.ts:36-41,75`). Mostra
  preço: **não vai para a tela** (só falado, sem valor).

## 1. Aba "Fichas Técnicas" (`components/producao/RecipeList.tsx`)
- Coluna da lista: "Fichas técnicas" + contador, botão **"Nova"** (`:164-170`), busca "Buscar ficha ou produto..."
  (`:178`); cada linha = nome + unidade (`:254-255`). Painel vazio: "Selecione uma ficha técnica", botão "Nova ficha"
  (`:309-311`). A ficha abre **no painel da direita** (formulário em linha, `:288-303`), não em janela.
- Backend: `production_recipes` (select `is_active = true`, `:60-67`).

### Formulário da ficha (`components/producao/RecipeFormDialog.tsx`)
- Título **"Nova ficha técnica"** / "Editar ficha técnica"; "Monte a receita: matérias-primas entram, o produto final
  sai." (`:916-917`).
- **"Nome da ficha"**, placeholder "Opcional — usa o nome do produto" (`:925-930`).
- **"Matérias-primas (entram) \*"** (`:941`); cartão tracejado **"Adicionar matéria-prima"** (`:950`); em cada cartão,
  combobox "Escolher material" (`:639`), campo "Qtd" (3 casas) e a unidade do material ao lado (`:645-655`); "Perda
  padrão" recolhido (`:679`, fora da fonte: não abrir).
- Cartão **"Produto final"** (`:966`): "Selecione o produto acabado abaixo" (`:984`), combobox "Selecione o produto"
  (`:996`), botão "+" com título "Criar novo produto" (`:1005`, abre "Cadastrar Novo Material"); depois de escolher:
  nome + "unidade de produção: {unidade}" (`:975-980`); total ao vivo **"Consumo por {unidade}"** (`:1021-1025`).
- **"Unidade de produção"** (select de unidades, `:1033`; lista em `constants/materialUnits.ts:7-28`, "Kg — Quilograma").
- **"Peças por unidade de venda (ex.: jogo = 4)"**, placeholder "Opcional" (`:1043-1050`).
- **"Coprodutos (saem junto) · opcional"** (`:1060`); texto "Coproduto que vem da perda de uma matéria-prima já sai
  calculado no lançamento do dia (e dá pra ajustar na mão). Coproduto avulso: a quantidade você digita no lançamento do
  dia." (`:1063-1067`); vazio: "Use quando a produção gera mais de um material (ex.: sobra reaproveitável)." (`:1071`);
  cartão **"Adicionar coproduto"** (`:1089`); cartão do coproduto: **"Quantidade digitada no lançamento do dia"** (`:661`).
- Botão **"Salvar ficha"** (`:537`) → toast **"Ficha técnica salva"** (`:336`). Travas (`:378-451`): "Selecione o produto
  (material de saída)", "Adicione ao menos 1 insumo com material e quantidade maior que zero", "Há insumos com o mesmo
  material repetido", "Há coprodutos com o mesmo material repetido", "Um coproduto não pode ser o mesmo material do
  produto principal". "Excluir ficha" só na edição (`:505-514`).
- Backend: `companies.production_default_unit` (`:151-155`), `materials` não arquivados (`:170-174`),
  `production_recipe_inputs` / `production_recipe_outputs` (edição, `:205-212`), RPC **`upsert_production_recipe_atomic`**
  (`p_company_id, p_recipe_id, p_header{output_material_id, name, production_unit, pieces_per_commercial_unit},
  p_inputs[{material_id, qty_per_output}], p_outputs[{material_id}]`, devolve o id; `:322-328`). Coproduto grava
  `qty_per_output` 0.

## 2. Aba "Ordens de Produção" (`components/producao/ProductionOrderList.tsx`)
- Título "Ordens de produção", alternância **"Kanban"** / "Lista" (`:284-299`; abre em Kanban), botão **"Nova produção"**
  (`:305`).
- Backend: `production_orders` (todas, por número), `production_order_workers`, `employees` (`:163-197`); RPC
  `delete_production_order_atomic` (`:264`).

### Quadro (`components/producao/ProductionKanbanBoard.tsx`)
- Colunas criadas sozinhas na primeira visita: **"A fazer"** (#EF4444), **"Em produção"** (#F59E0B), **"Concluída"**
  (#10B981, conclusão) (`:118-122,746-776`). Cabeçalho: nome (clique abre a edição), ícone de check com título
  **"Coluna de conclusão"**, contador, menu de três pontos ("Editar", "Excluir coluna") (`:429-488`). Coluna vazia:
  "Arraste ordens pra cá" (`:501`). Botão tracejado **"Coluna"** no fim (`:1091-1102`) cria "Nova coluna" → toast
  "Coluna criada" (`:973-991`).
- **"Editar coluna"** (`:557-607`): "Nome", "Cor", chave **"Coluna de conclusão"** ("As ordens finalizadas vão
  automaticamente para esta coluna. Só uma coluna pode ser a de conclusão."), "Cancelar" / **"Salvar"** → toast
  **"Coluna atualizada"** (`:942`).
- Cartão (`:217-344`): "#N" + selo ("Rascunho", "Em andamento", "Concluída", "Cancelada", `:111-116`); produto;
  rascunho: "planejado: 500 Kg"; senão "480 Kg produzido"; concluída: "R$ 3.087,60 · R$ 6,43/peça" (rótulo "/peça"
  mesmo em kg, `:279`); quem criou + data; "Equipe:" / "Produziu:" (`:302`); botão **"Finalizar"** nas vivas (`:342`);
  no passar do mouse, lápis "Editar ordem" e lixeira **"Excluir ordem"** (`:188,202`).
- Arrastar (`:840-883`): entre colunas grava `kanban_column_id`; ordem viva solta na coluna de conclusão **abre
  "Finalizar"** em vez de mover; "Ordem já finalizada não sai da coluna de conclusão" (`:859`).
- Excluir ordem (`:1172-1196`): **"Excluir ordem de produção?"**; concluída: "Atenção: esta produção já foi finalizada.
  Ao excluir, o estoque será estornado — a matéria-prima volta e o produto sai. Esta ação não pode ser desfeita.";
  botão **"Excluir ordem"** → toast **"Ordem excluída"** (`:969`).
- Backend: `production_kanban_columns` (select, insert, update, delete), RPC `set_production_done_column(p_column_id,
  p_company_id)` ao ligar a conclusão (`:907-930`), `production_orders` (select; update `kanban_column_id`),
  `profiles`, `production_order_workers`, `employees` (`:652-740`), RPC **`delete_production_order_atomic(p_order_id)`**
  (`:955`).

### "Nova ordem de produção" (`components/producao/ProductionOrderDialog.tsx`)
- Título e frase: "Nova ordem de produção", "Planeje a produção a partir de uma ficha técnica. Depois você vai lançando a
  produção dia a dia." (`:736,741`).
- **"Ficha técnica \*"** (placeholder "Escreva o nome ou código do produto", `:747-756`; sem ficha: "Nenhuma ficha técnica
  ativa. Crie uma ficha antes de produzir.", `:766`); **"Quantidade planejada \*"** com "Peças" / "jogos" (o segundo
  desligado sem pack, `:775-820`); **"Data da produção"** (hoje, `:121,830`); **"Responsável"** (usuários da empresa;
  nasce com quem está logado, `:317,841-874`); "Máquina" só se houver máquina (`:882`, o mundo não tem); **"Equipe (quem
  vai produzir)"** ("Selecione a equipe", busca "Buscar funcionário...", `EmployeeMultiSelect.tsx:40,131`; ajuda "Quem
  vai produzir esta ordem. Na finalização você informa quanto cada um produziu. Usado no relatório por funcionário.",
  `:902-914`); **"Coluna"** (nasce na primeira, `:326,932`).
- **"Consumo teórico estimado"**: "Material", "Qtd teórica", "Custo est."; **"Custo estimado total"**, **"Custo estimado por
  peça"** (`:957-1006`).
- **"Criar ordem"** (`:722`) → toast **"Ordem criada"** (`:659`); travas "Selecione uma ficha técnica", "Informe a
  quantidade planejada (maior que zero)", "Selecione ao menos um funcionário" (só com a configuração) (`:680-692`).
- Backend: `companies.production_require_employee`, `production_kanban_columns`, `production_machines`,
  `production_recipes`, `profiles`, `materials`, `production_recipe_inputs/outputs`; RPCs
  **`get_material_cost_with_basis(p_material_id, p_company_id)`** → `{cost, basis_used, is_fallback}` (`:511`) e
  **`get_next_production_order_number(p_company_id)`** (`:630`); `INSERT production_orders` (`status` draft,
  `:637-653`); equipe em `production_order_workers` sem `entry_id` (`orderTeam.ts:55-102`).

### Detalhe da ordem (`components/producao/ProductionOrderDetail.tsx`, clique no cartão)
- Título "Produção #N" + produto (`:328-334`); "Data", "Responsável", "Máquina" (`:410-419`); **"Meta (referência)"**,
  **"Produzido até agora"** (ou "Produzido"), barra "480 de 500 Kg" e % (`:428-453`); **"Lançamentos"** (vazio: "Nenhum
  dia lançado ainda. Comece lançando a produção do dia.", `:467-476`); linha do dia: "10/11", "480 Kg", fotos, "Cláudio
  Ferraz e Diego Morais", menu "Editar este dia" / "Excluir este dia" (`:480-535`); botões **"Lançar produção do dia"**
  e "Finalizar ordem" (`:546,558`).
- Backend: `production_orders`, `production_order_consumption`, `production_order_outputs`, `production_order_entries`,
  `production_order_workers`, `employees` (`:146-211`); RPC `delete_production_entry_atomic` (`:349`).

### "Lançar produção do dia" (`components/producao/DailyEntryDialog.tsx`)
- Título "Lançar produção do dia", "Fardo de alumínio · lançamento de 10/11/2026" (`:856-861`).
- **"Dia da produção \*"** (hoje, `:874`); **"Produzido (por funcionário) \*"** (a equipe da ordem, um campo por pessoa,
  `:887,939-968`; sem equipe: "Esta ordem não tem equipe. Edite a ordem e adicione os funcionários que vão produzir.",
  `:934`); **"Total do dia"** (`:970`). O seletor "Peças" / "jogos" só aparece com pack (`:205`; não aparece no fardo).
- **"Subprodutos (se sobrar algo aproveitável)"**, botão **"+ Adicionar"**, vazio "Nenhum subproduto neste dia."; linha:
  "Material" ("Selecione o subproduto", qualquer material menos o produto) e "Qtd (Kg)" (`:989-1056`). O coproduto avulso
  da ficha **não** vem preenchido: o operador adiciona.
- **"Matéria-prima usada"** (`:1085`): por insumo, **"Sugerido pela ficha: 480 Kg"** (`:1119-1126`), campo **"Real (Kg)"**
  já com o sugerido (`:1130-1141`, `:605-624`), diferença ao lado em vermelho com "+" ou verde com "−" (`:1094-1149`).
- Tolerância (`lib/producao.ts:590-603`): pede motivo quando |real − teórico| > teórico × tolerância%. Acima:
  **"Motivo da perda \*"** (placeholder "Motivo") com "Perda de corte", "Sucata", "Retrabalho", "Peça rejeitada",
  "Defeito de fabricação", **"Material reaproveitável"**, "Outros" (`lib/producao.ts:163-171`) e, sem escolha, **"Informe o
  motivo da diferença"** em vermelho (`:1151-1178`); dentro: "Dentro da tolerância de 2% — não precisa de motivo."
  (`:1179-1183`). Sem motivo, **"Salvar lançamento" fica desligado** (`:729,833`).
- "Observação (opcional)" (`:1205-1218`): **não é gravada** (não vai na RPC, `:731-768`). A aula não usa.
- **"Salvar lançamento"** (`:839`) → toast **"Lançamento salvo — estoque ajustado"** (baixa a cada lançamento) ou
  "Lançamento salvo" (`:770-776`). Fechar com dados: "Descartar este lançamento?" (`:1228`).
- Backend: `production_orders`, `production_recipe_inputs/outputs`, `production_order_workers`, `employees`,
  `materials` (`:168-326`); RPC **`add_production_entry_atomic(p_order_id, p_entry_date, p_consumption[{material_id,
  theoretical_qty, actual_qty, loss_reason}], p_outputs[{material_id, is_primary, qty}], p_workers[{employee_id,
  produced_qty}], p_client_request_id)`** (`:758-765`).

### "Finalizar #N" (`components/producao/FinalizeProductionDialog.tsx`)
- Título "Finalizar #3", produto (`:373-374`); **"Meta (referência)"**, **"Produzido de verdade"** com "96% da meta"
  (`:394-416`); **"Resumo do lote"**: "Produto principal", "Subprodutos", "Matéria-prima usada", **"Perdas"** (excedente do
  real sobre o teórico) (`:173-190,422-431`); **"Custo total do lote"**, **"Custo por peça"** (`:441-449`); **"Produção por
  funcionário"** (`:466`); "Voltar" / **"Finalizar ordem"** (`:320,329`) → toast **"Ordem finalizada — custo/peça R$ 6,43"**
  (`:273`); o cartão vai para a coluna de conclusão (`:238-251`).
- Backend: `production_orders`, `production_order_consumption` (`line_cost`), `production_order_outputs`,
  `production_order_workers`, `production_order_entries`, `employees`; RPC **`finalize_production_order_atomic(p_order_id,
  p_client_request_id)`** (`:226`); `production_kanban_columns` (`is_done`) + update `production_orders.kanban_column_id`.

## 3. Aba "Relatório" (`components/producao/ProductionReport.tsx`)
- "Relatório de produção" (`:1139`); filtros **"PERÍODO"** (Este mês), **"PRODUTO"** ("Todos os produtos"),
  **"FUNCIONÁRIO"**, "MÁQUINA" (`:1145-1218`).
- Indicadores (`:501-541`): **"Ordens concluídas"** ("no período"), **"Custo de matéria-prima"** ("soma do período"),
  **"Perda média"** ("real × teórico"), **"Rendimento médio"** ("produzido / real"; "não aplicável" quando algum produto
  não é kg → kg, `:128-153,478-499`).
- Gráfico "Peças produzidas · {produto}" (`:708-712`; diz "peças" mesmo em kg); abas **"Por produto"**, **"Por
  funcionário"**, "Lançamentos" (`:1396-1398`).
- "Por produto": "Ranking de produtos" ("Quantidade" / "Custo (R$)"), botão "Exportar" ("PDF", "Excel (.xlsx)") e a
  tabela "Produto", "Produzido", "Teórico (kg)", "Real (kg)", **"% Perda"**, **"% Rendim."**, "Custo MP", **"Custo/peça"**
  (`:786-1022`). Só ordens **concluídas** (`:282`).
- "Por funcionário" (`ProductionByEmployeeReport.tsx`): **"Ranking de funcionários"** (pizza, `:663`), **"Produção do dia"**
  (data, hoje), "Meta: 250/dia por funcionário." e a tabela "Funcionário", "Cargo", "Peças", "Ordens" com os selos
  **"bateu"** e **"faltam 30"** (`:744-835`).
- Backend: `production_orders` (`status` completed, período), `production_order_consumption`, `production_machines`
  (`:276-340`); `productionEmployeeData.ts`: `production_order_entries`, `production_orders`, `production_order_workers`,
  `employees` (`:124-208`).

## 4. Aba "Configurações" (`components/producao/ProductionSettings.tsx`)
- Cada item grava na hora em `companies` (update, `:200-219`) com toast próprio. Os da fonte: **"Custo de produção em
  cadeia (multinível)"** (texto com "(ex.: plástico moído virando pellet)", `:379-385`); **"Quando dar baixa no
  estoque"** ("A cada lançamento" (padrão) / "Só ao finalizar"; "Agora: baixa a cada lançamento do dia.", `:600-611`);
  **"Bloquear finalização quando faltar matéria-prima em estoque"** ("Ligado: não deixa finalizar uma produção sem estoque
  suficiente de insumo. Desligado: finaliza mesmo assim e o estoque do insumo fica negativo, apenas avisando.",
  `:632-639`) → toast **"Passou a bloquear finalização sem estoque"** (`:270`); **"Tolerância de perda (%)"** ("Só pede o
  motivo da perda quando a diferença entre real e teórico passar deste percentual. 0 = sempre pedir.", `:660-664`; toast
  "Tolerância de perda salva"); **"Meta de produção por dia"** ("Alvo de peças por dia por funcionário; destaca no
  relatório quem bateu (0/vazio = sem meta).", `:690-694`; toast "Meta de produção salva").
- Fora da fonte (só passam na tela): "Descontar o valor das sobras do custo de produção", "Qual preço de compra vira o
  custo do produto", "Exigir funcionário na ordem", "Como você chama o agrupamento de peças", "Lançar produção em jogos",
  "Padrões de ficha e ordem".
- Padrões do código (`hooks/useProductionConfig.ts:31-46`): tolerância 0, meta vazia, baixa a cada lançamento, bloqueio
  desligado, multinível desligado.

## 5. Histórico de Materiais (Kardex) (`pages/MaterialHistory.tsx`)
- Menu **"Materiais"** › **"Histórico"** (`config/routes.ts:452`), título "Histórico de Materiais"; lista de materiais à
  esquerda com busca "Buscar código ou material" (`:547`); cabeçalho "KARDEX — {código} - {material}" (`:819`); período
  "Este mês". Tipo da movimentação de produção: selo **"Produção"** (`PRODUCAO`, `:185-186`; i18n
  `materials.json:212`).
- Backend: `stock_movements` (`utils/fetchStockMovements.ts:108`). O tipo da linha de estorno da produção depende da RPC
  (sem migrations aqui): ver `[BACKEND]` no roteiro.

## Ajuda do app × código (vale o código)
1. Tolerância: a Ajuda (`t11-c09`) diz que o motivo é pedido sempre que real ≠ teórico; o código respeita a tolerância
   (`DailyEntryDialog.tsx:702-721`, `lib/producao.ts:590-603`). A fonte (⚠️) bate com o código.
2. Coproduto: a Ajuda (`t11-c04`) diz "Quantidade informada na finalização"; o código diz "Quantidade digitada no
   lançamento do dia" (`RecipeFormDialog.tsx:661`) e a finalização só lê.
3. Abas: a Ajuda fala em quatro; o código tem seis ("Conversão" e "Máquinas" a mais).
4. Coluna nova: a Ajuda fala em "Nova coluna"; o botão é "Coluna" e cria uma coluna chamada "Nova coluna".
5. Falta motivo: a Ajuda cita o toast "Informe o motivo da diferença de consumo nas linhas afetadas"; na tela o botão
   "Salvar lançamento" fica desligado antes disso (`:729,833`), então o que aparece é a frase da linha.

## Para o time do app (a fala não depende disso)
- "Observação" do lançamento do dia não é gravada (`DailyEntryDialog.tsx:143,731-768`).
- Custo por unidade sai como "/peça" e "Custo por peça" mesmo em produto por kg (`ProductionKanbanBoard.tsx:279`,
  `FinalizeProductionDialog.tsx:447`, `ProductionReport.tsx:1009`); gráfico e "Produção do dia" dizem "peças".
- "Quantidade planejada" mostra o seletor "Peças" em produto por kg (`ProductionOrderDialog.tsx:776-812`).
- Texto da equipe na ordem diz "Na finalização você informa quanto cada um produziu"; quem informa é o lançamento do dia
  (`ProductionOrderDialog.tsx:911-913`).
