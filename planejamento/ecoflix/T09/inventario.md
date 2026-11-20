# Atualização 1.60.18 (20/11/2026): o que vale por cima do texto abaixo (código em `/dev/shm/ecoflix-src/src`)

O corpo deste inventário é do 1.59.154. Para a aula, mandam estes pontos (detalhe em `cobertura_160.md`):
- **Menu e telas**: "Pedidos" continua item de primeiro nível; "Financeiro" › "Histórico do Caixa" idem. Nada mudou no menu: o robô não achava
  "Pedidos" porque a varredura de 19/11 rodou com o relógio do mundo em 10/11 (padrão) e a janela "Tarefas para hoje" cobria a tela (o
  Radix esconde o resto do leitor de tela). Para a T9 o relógio é **11/11/2026 08:30** (`rec/t09/fake_now.json`).
- **Editar Pedido** (`components/EditTransactionDialog.tsx`): "Se o caixa original estiver fechado, você poderá mantê-lo quando o pedido
  não movimentar dinheiro ou escolher um caixa aberto para receber o acerto." Lê `cash_transactions`, `bank_transactions` e
  `balance_movements` pelo `order_id`.
- **Compra em edição** (`pages/Purchase.tsx`): faixa "Editando pedido {ref} · {fornecedor} · {tabela}"; com caixa de origem fechado,
  "Caixa de destino da edição:" + selo "Caixa #70 · Original" ("Sem sem movimento em dinheiro: você pode manter o caixa original sem alterar o
  fechamento."), ou, com dinheiro, "O caixa original está fechado. Como houve movimento em dinheiro, escolha um caixa aberto." Janela "Em qual
  caixa registrar?" (`components/CashRegisterPickerDialog.tsx`): "Manter no caixa original #70" · "Sem movimento em dinheiro; o fechamento não
  será alterado.".
- **Troca de fornecedor com itens** (`components/orders/OrderPriceContextChangeDialog.tsx`, 1.60.18): janela **"Atualizar os preços?"**
  ("Com {nome}, o preço de N item(ns) é diferente."), linhas "material R$ de → R$ para/kg", "Total dos itens", botões **"Manter preços"** e
  **"Atualizar N preço(s)"**; só abre se algum preço mudar. (No 1.60.10 era "Trocar fornecedor?" / "Só nos próximos".)
- **Caixa**: "Reabrir caixa #N?" (`pages/CashHistory.tsx`, chave `reopen.confirmTitleNumbered`); o texto "Reabrir Último Caixa?" só vale sem número.
- **Pedidos**: ordenar por "Data", "N° Pedidos" e "Valor"; dica da coluna Pagamento (conta do Pix; partes do pagamento misto);
  "Exportar" → "Exportar pedidos" → "PDF"/"Excel" → janela "Exportar PDF" ("Escolha quais pedidos serão incluídos no relatório": "Período", "Tipo de
  Pedido", "Forma de Pagamento", "Detalhamento" · "Detalhar materiais de cada pedido"), "Relatório de pedidos gerado"; prévia da exclusão em caixa
  fechado: "↩ estorno hoje"; selo "Estornado em dd/MM" e "Comprovante sem valores" iguais.
- **Histórico do Caixa**: "Filtros" abre "Filtros do Histórico" ("Aberto por", "Período", "Limpar filtros", "Aplicar"). **Histórico de Exclusões**:
  filtros "Período", "Todos os tipos", "Todos os usuários", busca "Buscar pelo nome do registro..."; a linha abre "Quem", "Onde" (navegador e IP).
- Caixa do Rafael na aula: **#88**.

# Inventário · T9 "Pedidos e histórico do caixa" (EcoSistema 1.59.154)

Código lido em `/home/claude/ecoflix/app-src-1.59.154/` (`src/config/version.ts:16`, `APP_VERSION = "1.59.154"`). Análise
estática, só leitura. Caminhos relativos a `src/`. Rótulos entre aspas = texto exato do código (vários vêm de
`i18n/locales/pt-BR/orders.json` e `caixa.json`). Rótulos com a classe `uppercase` aparecem em maiúsculas na tela.

## Onde fica
- Menu lateral: "Pedidos" (item de primeiro nível) → `/pedidos`, permissão `screen_pedidos` (`config/routes.ts:427`,
  `App.tsx:537-541`). "Financeiro" › "Histórico do Caixa" → `/historico-caixa`, permissão `screen_historico_caixa`
  (`config/routes.ts:420`, `App.tsx:547-551`).
- Histórico de Exclusões: "Configurações" (rodapé do menu, ao lado de "Sair", `components/layout/SidebarMenuContent.tsx:
  809-834`) › aba "Empresa" › cartão "Histórico de Exclusões" › "Ver histórico" (`components/settings/
  SettingsCompanyContent.tsx:600-625`) → `/historico-exclusoes` (`App.tsx:420`), só administrador.

## 1. Pedidos (`pages/Orders.tsx`, 2.892 linhas)
- Cabeçalho "Pedidos", "Histórico completo de compras e vendas"; o período fica no canto ("Este mês" é o padrão, `:144`):
  "Todos os tempos", "Hoje", "Últimos 7 dias", "Este mês", "Mês passado", "Últimos 30 dias", "Este ano", "Personalizado"
  (`components/DateRangeFilter.tsx:426-450`, `i18n/locales/pt-BR/common.json` `dateFilter`).
- "Todas as Ordens" e "N ordem(ns) • Exibindo a-b de N" (`:1975-1978`). Card "Resumo do período filtrado" com
  "Compras" e "Vendas" por forma ("Dinheiro", "Pix/Transferência", ...) (`components/orders/OrdersPaymentSummaryCard.tsx:
  380-450`). A lista traz pedidos de todos os caixas (consulta por empresa e período, `:540-660`).
- Botão "Filtros" → "Filtrar pedidos", "Combine os campos para chegar ao pedido certo."; busca "Pedido, cliente,
  operador, placa..." (casa nome do parceiro, número, operador, placa e observação, `:906-930`); "Tipo" ("Compras",
  "Vendas"); "Material"; "Forma de Pagamento" ("Com Dinheiro", "Com Pix/Transferência", "Com Saldo", "Pagamento Misto",
  "Não informado"); "Conta"; "Limpar" (`:1996-2079`, `:974-980`). Cada multiseleção tem "Marcar todos" / "Desmarcar
  todos" (`components/ui/filter-multi-select.tsx`). Filtros ativos viram etiquetas: "Filtrando por", "Busca: ...",
  "Tipo: Compras", "Material: ...", "Pagamento: ...", e "Limpar todos" (`:982-1012`, `:1865-1900`).
- "Exportar" → "Exportar pedidos" → "PDF" / "Excel" (`:2082-2111`; fora da aula).
- Colunas: "Usuário", "Data", "Tipo", "N° Pedidos", "Cliente/Fornecedor", "Pagamento", "Valor", "Ações" (`:2397-2428`).
  Selos na coluna Tipo: "Compra"/"Venda", "Comprovante sem valores" e "Estornado em dd/MM" com a dica
  "Estornado ... correção lançada no caixa de hoje" (`:2480-2500`). Pedido estornado **continua na lista** (decisão de
  26/09/2026, `:896-905`); só sai dos totais e da exportação (`:1613-1620`). 🔎 A central de ajuda diz que ele some da
  lista: vale o código.
- Linha expandida: "Material", "Peso", "V.Unit.", "Total" e "Formas de Pagamento" (`:2702-2760`).
- Menu "⋮" da linha (`:2629-2697`): "Ver comprovante", "Ver fotos anexadas", "Enviar pelo WhatsApp", "Imprimir direto"
  (só com impressão direta do EcoTray), "Cupom sem valor" (ou "Mostrar valores no comprovante"), e, com a permissão de
  editar e excluir pedidos e se não estiver estornado, "Editar" e "Excluir".
- "Ver comprovante" (`:1146-1157`): abre a nova aba no clique; se o navegador bloquear, aviso "Popup bloqueado. Permita
  popups para gerar comprovantes."; o PDF abre em nova aba.
- "Cupom sem valor" (`:1492-1514`): RPC `set_order_hide_financials`; avisos "Cupom sem valor ativado" / "Cupom sem valor
  desativado"; o comprovante sai sem valores (material e peso).
- "Editar" → `components/EditTransactionDialog.tsx:177-203`: "Editar Pedido", "O pedido será carregado para edição. Após
  salvar, o pedido original será substituído.", "Se o pedido for de um caixa já fechado, o acerto do dinheiro é lançado no
  caixa de hoje e o pedido antigo fica marcado como estornado.", "Cancelar", "Editar Pedido" → `/compra` (ou `/venda`) em
  modo edição com o caixa de origem.
- "Excluir" → `components/OrderDeletionPreviewDialog.tsx:64-139`: "Excluir compra #N" + "<parceiro> · R$ X", "Vou desfazer
  tudo que este pedido criou:", "Calculando o que será desfeito…", blocos "Estoque" ("− <material> <qtd> <un>") e
  "Financeiro" ("− Pagamento em dinheiro R$ X (apaga)", ou "↩ estorno hoje" quando o caixa de origem está fechado),
  aviso amarelo no modo compensado; "Cancelar", "Excluir pedido" ("Excluindo…"). Prévia pela RPC `preview_order_deletion`
  (`hooks/useOrderDeletionPreview.ts:10`). Exclusão (`:270-357`): RPC `delete_purchase_atomic` / `delete_sale_atomic`
  com `p_compensation_register_id` = caixa aberto de hoje do usuário. Caixa de origem aberto: "Pedido excluído" / "Pedido
  excluído e saldos revertidos."; fechado: "Pedido estornado" / "O caixa antigo foi preservado e o estorno foi lançado no
  caixa de hoje."; sem caixa de hoje: "Abra o caixa de hoje".

## 2. Edição na tela de Compra (`pages/Purchase.tsx`)
- Selo "Editando Compra #N" e botão "Cancelar Edição" (`:4341-4350`); a data original do pedido é mantida (`:663-676`).
- Campo "Fornecedor" com o nome atual → janela "Selecionar Fornecedor", busca "Buscar por nome, apelido, CPF/CNPJ ou
  telefone..." (`:4421,4757-4771`); trocar o fornecedor reaplica a tabela de preço padrão dele (`:1642-1687`).
- Item: menu "Ações do item" → "Editar" (volta o item para o formulário, aviso "Item carregado para edição"),
  "Adicionar tara / pesagem avançada", "Excluir" (`:5176-5194`, `:3704-3747`). Formulário: material, "Valor/Kg",
  "Quantidade (Kg)", "Tara/Imp.", "Peso Líquido do Item", "Valor Total do Item", "Incluir Item"
  (`components/OrderFormInputs.tsx:664-867`). "Finalizar Compra".
- "Finalizar Pedido" (`components/MultiPaymentDialog.tsx:1225`): "Dinheiro", "Pix/Transferência", "CONFIRMAR PAGAMENTO"
  (`:1088-1096`).
- Gravação da edição (`:2338-2412`, `:2567-2574`): RPC `revert_consolidated_order_atomic` desfaz o pedido inteiro
  (estoque, caixa, banco, saldo do parceiro, itens) com os avisos "Revertendo pedido original..." e "Pedido original
  revertido! Criando pedido editado..." (origem aberta; com origem fechada: "Pedido antigo estornado! Recriando no caixa
  de hoje..."); depois `create_purchase_atomic` grava a versão nova no caixa de origem (`:2659`); aviso "Compra
  registrada!" (`:2946-2949`). Janela "Imprimir Comprovante", "Deseja imprimir o comprovante de compra?", "Não, obrigado",
  "Visualizar PDF" (com EcoTray, seletor "Visualizar"/"Imprimir" e "Imprimir direto") (`components/PrintModal.tsx:42-117`).
- Lançamento com data de outro dia: o banco põe no caixa que cobre a data; quando ele difere do caixa aberto, a tela
  pergunta "Em qual caixa lançar?" ("Caixa N ... é o caixa que cobre a data do pedido" ou "Caixa M ... aberto agora")
  (`:2576-2624`, `components/OrderCashRegisterChoiceDialog.tsx:96-156`, `lib/orderCashRegisterPreview.ts`). Em edição a
  pergunta não aparece.

## 3. Histórico do Caixa (`pages/CashHistory.tsx`, 1.459 linhas)
- "Histórico do Caixa", "Todos os registros de fechamento do caixa"; "Caixas Fechados" com a dica "Sobre o Histórico do
  Caixa"; "N registro(s) • Exibindo a-b de N"; busca "Buscar por responsável, data ou código..." (casa nome, data
  dd/MM/yyyy e número); "Filtros" → "Filtros do Histórico": "Aberto por" ("Todos os operadores"), "Período", "Limpar
  filtros", "Aplicar" (`:970-1030`, `:175-306`). Período padrão "Todos os tempos" (`:332`).
- Colunas "Código", "Abertura", "Fechamento", "Aberto por", "Saldo Inicial", "Saldo Final", "Ações" (`:1033-1077`); ícone
  de corrente com a dica "Caixas fechados no mesmo dia" (`:1098-1118`).
- Clique na linha: resumo "Total Compras", "Total Vendas", "Receitas", "Despesas", "Lucro Projetado" ("Carregando
  resumo...") (`:61-161`).
- "Ações" (`:1147-1220`): "Ver comprovante" (relatório de fechamento em PDF, `:892-905`), "Imprimir direto" (EcoTray),
  "Relatório de estoque" (`:921-958`; página "Relatório de Estoque do Caixa #N" com "Código", "Material", "Qtd.
  Comprada", "Valor Comprado", "Preço Médio Compra", "Qtd. Vendida", "Valor Vendido", "Preço Médio Venda", "Projeção de
  Lucro", "Margem Projetada", `utils/cashMaterialReportHtmlGenerator.ts:298-444`) e "Reabrir caixa".
- "Reabrir caixa": apagado com a dica "Só é possível reabrir o caixa de <nome> quando ele não tiver outro caixa aberto.
  Ex.: feche o caixa atual de <nome> para reabrir este." quando o dono do caixa tem outro aberto (`:537-546`); senão,
  confirmação "Reabrir Último Caixa?" (título fixo, também para caixa antigo), "O caixa será reaberto exatamente como
  estava antes do fechamento. Todas as transações registradas continuarão associadas a este caixa.", "Fechado em:
  dd/MM/yyyy HH:mm", "Cancelar", "Reabrir Caixa" (`:1430-1455`). Reabre (`:452-527`): apaga as diferenças do fechamento,
  `status` open, `closed_at` e `closing_balance` nulos, `reopened_at`; aviso "Caixa reaberto com sucesso!"; vai para
  `/caixa`.

## 4. No Caixa, depois de reabrir (`pages/Caixa.tsx`)
- Abas "Início", "#N | Caixa - <operador>" (o gestor vê todas, `components/CashRegisterTabs.tsx:76-118`); a aba
  selecionada ao abrir é a do próprio usuário (`Caixa.tsx:773-779`).
- "Histórico de Transações", abas "Todas", "Dinheiro", "Pix/Transferência"; menu da linha de pedido: "Ver comprovante",
  "Ver fotos anexadas", "Enviar pelo WhatsApp", "Imprimir direto", "Emitir NF-e", "Editar", "Excluir"
  (`components/TransactionHistory.tsx:3434-3525,4318-4440`). A aba "Todas" é a consulta paginada que se refaz em segundo
  plano depois de mexer num pedido (`pages/Orders.tsx:312-317`).
- "Fechar Caixa" → "Fechar Caixa #N", "Caixa de <operador> · Aberto em ...", "Valor de Fechamento" já preenchido com o
  esperado, "Data/hora do fechamento" (com a permissão de data retroativa) com o botão da data (dd/MM/yyyy, calendário sem
  datas futuras) e o campo "Hora" (`Caixa.tsx:3377-3605`, `components/ui/RetroactiveDateTimePicker.tsx:200-291`),
  "Confirmar Fechamento"; aviso "Caixa fechado com sucesso!"; "Imprimir Relatório" → "Não, obrigado".

## 5. Histórico de Exclusões (`pages/HistoricoExclusoes.tsx`)
"Histórico de Exclusões"; filtros (período 30 dias, tipo, usuário, busca); cada linha "Excluiu compra "<rótulo>"" com data,
hora e e-mail (`components/historico-exclusoes/AuditEventRow.tsx:61-69`); vazio: "Nenhum registro encontrado no período
selecionado."; sem acesso: "Você não tem permissão para acessar esta tela. Apenas administradores da empresa podem ver o
histórico de exclusões." Tabela `destructive_actions_audit`.

## Backend usado
| Tela | Tabela / RPC |
|---|---|
| Pedidos | `orders_with_payments` (ou consultas de `purchases`/`sales` com itens e pagamentos), `profiles`, `materials`, `companies`, `bank_accounts`, `cash_register` (caixa aberto de hoje) |
| Comprovante | `purchase_items`/`sale_items`, formas de pagamento do pedido; PDF gerado no navegador (nova aba) |
| Cupom sem valor | RPC `set_order_hide_financials` |
| Excluir | RPCs `preview_order_deletion`, `delete_purchase_atomic`; `destructive_actions_audit` (a linha da auditoria) |
| Editar | `cash_transactions` (caixa de origem), `purchases` com itens; RPCs `revert_consolidated_order_atomic`, `create_purchase_atomic` |
| Histórico do Caixa | `cash_register` fechados e abertos, `profiles`, `cash_transactions`, `bank_transactions`, `purchases`, `sales` (resumo e relatórios) |
| Reabrir / fechar de novo | `cash_register` update; `cash_transactions` delete (diferenças) e insert (`closing`) |

## Pegadinhas do código (handoff, a fala não depende)
- H1. A confirmação de reabrir no Histórico do Caixa diz "Reabrir Último Caixa?" mesmo para um caixa antigo; a dica de
  "Caixas Fechados" diz "O último caixa fechado pode ser reaberto", mas qualquer um pode (`CashHistory.tsx:535`).
- H2. A central de ajuda diz que o pedido estornado não aparece na lista e que o selo é "Sem valor"; no código ele aparece
  com "Estornado em dd/MM" e o selo do cupom é "Comprovante sem valores".
- H3. O texto do diálogo "Editar Pedido" fala do caixa fechado mesmo quando o caixa de origem está aberto (texto fixo).
