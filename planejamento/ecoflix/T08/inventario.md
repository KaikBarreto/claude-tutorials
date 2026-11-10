# Inventário · T8 Ticket de Pesagem

Levantado em 10/11/2026 contra o código gravado (`APP_VERSION = "1.59.154"`), cópia em
`/home/claude/ecoflix/app-src-1.59.154/`. Caminhos relativos a `src/`. Rótulo entre aspas = texto exato.

## 1. Lista (`/ticket-pesagem`, `pages/WeighingTicket.tsx`)
- Menu lateral "Materiais" › **"Ticket de Pesagem"** (`config/routes.ts:446-455`); rota com a permissão
  `screen_weighing_ticket` (`App.tsx:423-427`). Tela livre para todo plano (o módulo `ticket_pesagem` está desativado no
  catálogo: a aula não fala em plano).
- Cabeçalho "Ticket de Pesagem" ("Gerencie tickets de pesagem rodoviária") `:3421-3440`; abas **"Tickets padrão"** e
  **"Pesagens avulsas"** `:3527-3530`; título "Últimos Tickets" / "Pesagens Avulsas"; busca "Buscar por nº ou
  cliente/fornecedor..."; botões Kanban / Lista (padrão Kanban, `:636-639`); **"Filtros"** ("Tipo": "Compra", "Venda";
  "Status": "Aguardando valorização", "Valorizado", "Cancelado"; "Usuário"; "Limpar filtros") `:259-268,3573-3630`;
  "Exportar" (PDF, Excel); **"Rascunhos abertos"** com contador `:3669-3683` (vazio: "Nenhum rascunho aberto por aqui.",
  `:2779`); **"Novo Ticket de Pesagem"** (abre a criação com uma aba nova e os rascunhos do usuário, `:2761-2774`).
- Kanban (`components/weighing/WeighingTicketKanbanBoard.tsx`): colunas **"Aguardando valorização"** (cabeçalho âmbar)
  e **"Valorizados"** (verde), com contador `:30-44,324-343`; vazias: "Nenhum ticket aguardando valorização." /
  "Nenhum ticket valorizado ainda.". Arrastar de "Valorizados" para trás: "Este ticket já virou pedido e não pode voltar."
- Cartão (`components/weighing/WeighingTicketCard.tsx:165-368`): "Ticket #58", selo **"COMPRA"** (azul) / "VENDA" (verde)
  / "PESAGEM AVULSA" (laranja); "Selecionar"; **"Ações"** › **"Valorizar"**, "Ver pedido" (valorizado), **"Ver
  comprovante"**, "Editar", "Excluir"; "Fornecedor: Depósito Irmãos Siqueira"; "Sem valores" (ou o total em R$);
  "Valorizado pelo pedido #…"; material, peso líquido em kg, data "10/11/26 08:52".
- Lista: selo de status "Aguardando valorização" (âmbar), "Valorizado" (verde), "Cancelado" (vermelho), "Pesagem avulsa"
  (laranja) (`components/weighing/WeighingTicketTable.tsx:103-131`).
- Salvo: toast **"Ticket de pesagem salvo"** `:2035` e janela **"Ticket #58 salvo"** ("O que deseja fazer com este ticket
  de pesagem?"): **"Imprimir comprovante"**, **"Valorizar"**, "Fechar" `:3909-3995`; com a impressão automática:
  "Comprovante enviado para a impressora automaticamente." e "Imprimir novamente". Pesagem avulsa: selo "PESAGEM
  AVULSA" e "Somente comprovante de peso. Esta pesagem não possui valor comercial e não pode ser valorizada."
- Comprovante: **"Gerar comprovante do ticket"** ("Escolha o formato do comprovante deste ticket de pesagem.") com
  **"A4"** ("Folha") e **"Térmico"** ("80mm") `:3898-3904`, `components/ReceiptFormatDialog.tsx:52-62`; os dois abrem
  PDF numa aba (`:3127-3142`). Térmico do ticket pendente: faixa "TICKET DE PESAGEM" / **"NÃO VALORIZADO"** +
  "Documento sem valor financeiro definitivo"; valorizado: "VALORIZADO" + "Pedido gerado: #…"; avulsa: "PESAGEM AVULSA"
  / "SEM VALOR COMERCIAL" (`utils/thermalReceiptGenerator.ts:1074-1084,1134-1136`); "Motorista: … Placa: …"
  (`:1616-1640`); no modo "Completo", "1ª pesagem", "2ª pesagem", "Bruto", "Tara", "Impureza … (3%)"
  (`utils/receiptWeightDisplay.ts:103-118`). Mescladas: uma linha só, somada.
- Impressão sozinha ao salvar: chave "Imprimir comprovante do Ticket de Pesagem" ("Envia o comprovante térmico direto
  pra impressora ao salvar um ticket"), em Configurações › Integrações, só com a impressão direta ligada
  (`components/settings/SettingsIntegrationsContent.tsx:549-584`; `WeighingTicket.tsx:2091-2116`).

## 2. Criação com abas (`components/weighing/WeighingTicketCreator.tsx`, `WeighingTicketForm.tsx`)
- Cabeçalho "Novo Ticket de Pesagem" ("Preencha o ticket. Use as abas para atender vários veículos.").
- Barra de topo (`WeighingTicketForm.tsx:2335-2419`): "Voltar"; **"Modalidade"** ("Ticket padrão" | "Pesagem avulsa");
  **"Tipo"** ("Compra" | "Venda"); **"Valores"** ("Sem valores" | "Com valores"; a escolha fica memorizada).
- **"Fornecedor"** (na compra; "Cliente" na venda): "Selecionar fornecedor" + "+" `:2424-2457`; janela "Selecionar
  Fornecedor" ("Buscar por nome, apelido, CPF/CNPJ ou telefone...", 1ª opção "Não informado") `:2522-2548`.
  Fornecedor é opcional, salvo se a empresa exigir (`:1527-1537`).
- Abas = `components/OrderSwitcher.tsx` (barra escura à direita): colunas **"Número"**, **"Peso"** (sem valores) ou
  "Valor", **"CLIENTE/FORNECEDOR"** `:346-370`; número previsto "#58", "#59" (próximo número + posição, `:170-175`;
  `get_next_ticket_number`); "Sem cliente/fornecedor"; embaixo, "Seu rascunho"; "(2)" com mais de uma aba; botão
  **"+ Novo ticket"** `:462-489`; lista "Tickets abertos"; o "x" pede "Descartar este ticket?" ("Manter ticket" /
  "Descartar ticket").
- Card **"Pesagem"** (`components/OrderFormInputs.tsx:638-870`): "Material" ("Escreva o nome ou código do material");
  "Quantidade (Kg)" com o botão **"Pesagem avançada"** embaixo; "Tara/Imp."; dentro do card **"Motorista"** ("Digite ou
  busque o motorista") e **"Placa do Veículo"** ("Digite ou busque a placa"), com sugestões do cadastro e
  "Gerenciar motoristas" / "Gerenciar placas" (`WeighingTicketForm.tsx:1640-1675`,
  `components/weighing/DriverVehicleAutocomplete.tsx:55-56,151-158`); "Peso Líquido do Item"; **"Incluir Item"**. Com a
  balança ligada, escolher o material já puxa o peso da balança (`InputPesoBalanca.tsx:133-141`).
- **"Pesagem avançada"** ("Registre pesagem dupla, tara, impureza e dados do transporte";
  `components/AdvancedWeighingDialog.tsx:382-729`): **"1ª Pesagem"**, **"2ª Pesagem"**, **"Peso Bruto (Kg)"** (=
  |1ª − 2ª| com "|9.460 − 6.380|" embaixo; números em `formatNumberBR`, sem casas fixas; só a 1ª: "= 1ª pesagem") `:244-257,407-480`; dica "Preencha 1ª e 2ª
  pesagem para o bruto, informe só a 1ª (conta como bruto) ou digite o bruto direto."; **"Tara (Kg)"**; **"Impureza"**
  com "kg" | "%" ("= 61,6 Kg (sobre bruto − tara)") `:491-549`; **"Líquido (Kg)"** = Bruto − Tara − Impureza `:274,555`;
  "Valor/Kg", "Valor estimado", "Desconto (R$)", "Valor final" (aparecem mesmo sem valores; ficam vazios);
  **"Como exibir no comprovante"**: "Resumido", "Detalhado", **"Completo"** ("1ª e 2ª pesagem, bruto, tara, impureza e
  líquido."); "Motorista", "Placa do veículo"; "Cancelar", **"Confirmar"**. Só com a 1ª, o item entra com ela como bruto
  (a 1ª não fica guardada à parte: na saída, ela é digitada de novo na "1ª Pesagem").
- "Itens do Ticket (1)" (`WeighingTicketForm.tsx:1911-2325`): "Adicione materiais à pesagem para vê-los aqui.";
  colunas "Código", "Material", "Peso", "Tara/Imp.", "Ações"; seta que abre o detalhe da pesagem; menu "Ações do item":
  "Editar", **"Adicionar tara / pesagem avançada"**, "Mesclar pesagens", "Excluir"; "Mesclar {n} pesagens deste material",
  **"Desmesclar pesagens"** ("Desmesclar e restaurar {n} pesagens originais"). Toast "Pesagem do item atualizada" `:1006`.
- "Observações"; "Opções avançadas" (anexar foto); **"Salvar Ticket de Pesagem"** `:1811-1880`; sem item: "Adicione pelo
  menos um material".
- Rascunho: cada aba grava sozinha em `weighing_tickets` (`status` draft, 600 ms depois de cada mudança) `:1423-1488`; o
  número só nasce no salvar (RPC `finalize_weighing_ticket_v3`, `WeighingTicket.tsx:1961`). Falha: "Não foi possível
  salvar este ticket".

## 3. Valorizar (`WeighingTicket.tsx:2189-2499`)
- Pega o tipo do próprio ticket (compra), relê o ticket e cria um rascunho de pedido (`order_drafts`) com os itens; sem
  valores, o preço vem na ordem da compra: personalizado do fornecedor > tabela dele > tabela > material
  (`resolveValorizationPrices`). Abre `/compra` com o rascunho. De novo no mesmo ticket: "Estes tickets já tinham um
  pedido em aberto — retomando." ("Atualizado com os itens atuais do ticket (1 item, R$ …).").
- Avulsa: "Pesagem avulsa não pode ser valorizada" ("Ela é somente um comprovante de peso, sem vínculo comercial.").
- Finalizar a compra (labels no `T07/inventario.md` §6: "Finalizar", "Finalizar Pedido", "Pix/Transferência", "CONFIRMAR
  PAGAMENTO", "Compra registrada!") marca o ticket como valorizado e volta sozinho: toast "Pedido finalizado — voltando
  ao Ticket de Pesagem" (`pages/Purchase.tsx:3215-3230`).

## 4. Backend
`weighing_tickets` (rascunho: update/insert; lista, kanban, `items` jsonb), RPC `get_next_ticket_number`, RPC
`finalize_weighing_ticket_v3`, `order_drafts` (insert/update na valorização), `drivers` e `vehicles` (sugestões),
`suppliers`/`customers`, preços (`entity_custom_prices`, tabelas), `profiles` (preferências), `purchases` e o RPC de
compra do T7 (`create_purchase_atomic`).
