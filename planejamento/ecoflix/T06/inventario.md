# Inventário · T6 "Caixa: abrir, fechar e o cofre" (EcoSistema 1.59.154)

Código lido em `/home/claude/ecoflix/app-src-1.59.154/` (`src/config/version.ts:16`, `APP_VERSION = "1.59.154"`). Análise
estática, só leitura. Caminhos relativos a `src/`. Rótulos entre aspas = texto exato do código. Vários rótulos têm a classe
CSS `uppercase` e aparecem em maiúsculas na tela ("DINHEIRO EM CAIXA", "FECHAR CAIXA", "SAQUE / SANGRIA"); a fala usa a
grafia do código.

## Onde fica
- Menu lateral: "Financeiro" (submenu) → "Caixa" (`config/routes.ts:413-420`). Rota `/caixa` com a permissão de tela
  `screen_caixa` (`App.tsx:385-389`). Página `pages/Caixa.tsx` (3.837 linhas), cabeçalho "Caixa", subtítulo "Gestão
  financeira e movimentações" (`:2341-2344`).
- Multi-caixa é o padrão (`hooks/useMultiCashEnabled.tsx:32`, `companies.multi_cash_enabled ?? true`); liga e desliga em
  Configurações › "Usabilidade" › "Multi-Caixas" (`components/settings/SettingsUsabilityContent.tsx:472-505`). Cofre:
  mesma tela, "Rastreabilidade do dinheiro físico (Cofre)" (`:512-526`).

## 1. Caixa sem caixa aberto
| Quem vê | O que aparece | Onde |
|---|---|---|
| Administrador (Rafael) ou quem tem "Ver e Operar Todos os Caixas", com multi-caixa | Aba "Início" = `CashRegisterHomePanel`: título "Meu Caixa" (ou "Abrir Caixa para Outro Usuário" quando ele já tem caixa aberto), botão "Abrir Caixa"; cartão âmbar com "#N · R$ X", nome do operador, "dd/MM HH:mm → dd/MM HH:mm", link "reabrir outro caixa" e botão "Reabrir #N"; depois "Painel Gerencial", seletor "Hoje", "N caixas encontrados", "Nenhum caixa foi aberto neste dia.", "Resumo do Dia" | `Caixa.tsx:2406-2418`, `:745-780` (aba Início quando ele não tem caixa); `components/CashRegisterHomePanel.tsx:575-707` |
| Operador sem "Ver e Operar Todos os Caixas" (ou caixa único) | Cartão tracejado "Caixa Fechado", "Clique para abrir o caixa e começar a trabalhar", botão "Abrir Caixa"; cartão âmbar "Reabrir Último Caixa" com "#N · R$ X", horários e "Reabrir #N" | `Caixa.tsx:2419-2542` |

- Abas do topo (`components/CashRegisterTabs.tsx:76-118`): só aparecem com algum caixa aberto; "Início" e uma aba por caixa
  aberto, "#N | Caixa - <operador>" e "(você)" no do usuário logado. Botão "?" → "Como funcionam os Multi-Caixas?" com
  "Caixa Individual", "Visão Multi-Caixa", "Abrir caixa para outros usuários", "O que acontece ao operar em outro caixa?",
  "Histórico" e "Dica:" (`:175-262`).
- Compra sem caixa: `/compra` mostra o aviso "Abra o caixa antes de realizar compras" e volta para `/caixa`
  (`pages/Purchase.tsx:2099-2120`); venda: "Abra o caixa antes de realizar vendas" (`pages/Sale.tsx:1879`). Atalho
  padrão "Compra" = Shift+C, que navega direto para `/compra` (`hooks/useKeyboardShortcuts.tsx:24,207-210`; atalhos
  ligados por padrão, `:66,89`). Pelo Ctrl+K, sem caixa escolhido, abre "Em qual caixa registrar?" com "Nenhum caixa
  aberto" (`components/CommandPalette.tsx:471-479`, `components/CashRegisterPickerDialog.tsx:39,108-118`).
- Saldo de parceiro sem caixa aberto: só a forma "Dinheiro" fica bloqueada; Pix/Transferência continua
  (`components/BalancePaymentModal.tsx:148-158,598-612`).

## 2. Abrir caixa (diálogo)
`Caixa.tsx:3196-3375`; valores iniciais em `openDialogWithDefaults` (`:699-727`).
- Título "Abrir Caixa"; descrição "Informe o saldo inicial em dinheiro. Deixe em branco ou 0 se abrir sem dinheiro em
  espécie."
- "Abrir para o usuário" (só gestor com multi-caixa, `:3224-3249`): lista os usuários ativos sem caixa aberto, por nome;
  "(Você)" no logado. Pré-seleção: o próprio usuário; se ele já tem caixa, o primeiro livre em ordem alfabética
  (`:704-711`), que no mundo é "Juliana Prado".
- "Saldo de Abertura (R$)" (`:3284`): **começa sempre vazio** (`:712-717`, comentário do bug do valor pré-preenchido).
- Dicas embaixo do campo: "Disponível no cofre agora: R$ X." e, havendo caixa aberto, "(de R$ Y total ... R$ Z está
  dentro de caixas abertos)" (`:3302-3318`); "R$ X foi o valor restante em dinheiro do último caixa (#N)" (`:3345-3350`,
  último caixa fechado **do usuário logado**, `:605-633`, mesmo quando o diálogo é para outro usuário).
- Campo vazio ou zero: aviso âmbar "O caixa será aberto sem dinheiro em espécie (R$ 0,00). Use isso se a operação é só
  Pix/cartão." (`:3351-3358`; `parseBRNumber("") = 0`, `utils/masks.ts:236-241`).
- "Data e Hora de Abertura" (só com `action_custom_cash_datetime` ou admin, `:3361-3373`), já com a hora atual.
- Botões "Cancelar" e "Abrir Caixa" ("Abrindo...").
- Ao abrir (`:1564-1907`): confere caixa já aberto do operador ("<nome> já possui um caixa aberto", `:1611-1618`);
  confere o cofre (`:1686-1753`); grava o caixa; com saldo > 0 grava a linha "Abertura do Caixa #N" (`:1805-1820`; com
  zero, não grava); aviso "Caixa aberto com sucesso!" (`:1832`); a tela passa para a aba do caixa novo (`:1849-1851`).

## 3. Saldo insuficiente em dinheiro (cofre)
`Caixa.tsx:3741-3833`; disparado em `:1741-1751` quando o valor passa do disponível (não é a primeira abertura da empresa).
- Título "⚠️ Saldo insuficiente em dinheiro"; texto "O caixa só pode abrir com o dinheiro que já está registrado no cofre
  da empresa. Você tentou abrir com R$ X, mas há apenas R$ Y disponíveis (R$ Z já reservados em caixas abertos)."
- Para quem gerencia contas: "Se há dinheiro físico que ainda não foi registrado, ajuste o saldo do dinheiro abaixo (...)
  o caixa abre em seguida com o mesmo valor." Botões "Usar disponível (R$ Y)" (preenche o campo com o disponível) e
  "Ajustar saldo do dinheiro" (abre "Ajustar saldo da Conta DINHEIRO", motivo sugerido "Dinheiro físico não registrado
  (abertura de caixa)", e ao concluir abre o caixa sozinho; `components/dinheiro/AdjustBalanceDialog.tsx:301-392`).
- 🔎 A fonte e a central de ajuda falam em "Abrir com valor menor"; no código o botão é "Usar disponível (R$ Y)".

## 4. Caixa aberto
`Caixa.tsx:2544-3193`.
- Cartão "Dinheiro em Caixa" (`:2547-2759`): valor (vermelho se negativo), olho "Ocultar saldo"/"Mostrar saldo";
  sem a permissão "Ver Dinheiro Total em Caixa" (`config/routes.ts:272`) ou com o olho fechado: "R$ ••••••"
  (`hooks/useBalanceVisibility.ts:46`). "Aberto em: dd/MM/yyyy HH:mm". Linha "Dinheiro total da empresa: R$ X ›"
  (cofre; clicável, vai para `/movimentacoes-bancarias` na conta DINHEIRO, `:2635-2656,175-178`). Botão "Fechar Caixa":
  com pedido não finalizado neste caixa fica com cadeado e a dica "Finalize ou cancele antes de fechar o caixa:" mais a
  lista (`:2658-2716`); enquanto confere, "Verificando...".
- Cartão "Saldo Bancário" (só com "Ver Totais e Valores Financeiros" e "Gerenciar Contas Bancárias", `:2761-2911`): soma
  das contas bancárias, carrossel das contas quando há mais de uma, botões "Saque / Sangria", "Nova Movimentação
  Bancária" e "Saldo de Cliente/Fornecedor" (`components/PartnerBalanceQuickAction.tsx:240-247`).
- Botões "Nova Compra", "Nova Venda", "Nova Despesa", "Nova Receita" (`:2982-3033`); "Resumo do Caixa Atual" com "Total
  Comprado", "Total Vendido", "Projeção de Lucro" (`:3058-3182`).
- "Histórico de Transações", "Neste caixa que está em aberto", abas "Todas", "Dinheiro", "Pix/Transferência"; a linha de
  abertura tem o tipo "Abertura" (selo âmbar) e a descrição "Abertura do Caixa #N" (`components/TransactionHistory.tsx:1014,
  2056,3434-3525`).

## 5. O cofre (Movimentações Financeiras › DINHEIRO)
Com o cofre ligado a tela `/movimentacoes-bancarias` se chama "Movimentações Financeiras" (`components/layout/
SidebarMenuContent.tsx:188,288`). Cartão `components/dinheiro/CashAccountCard.tsx:120-175`: "O cofre da empresa", valor,
"Saldo Total em Dinheiro", barra com legenda "Disponível no cofre: R$ X (N%)" e "Caixa de <operador>: R$ Y (N%)"
(`components/dinheiro/CashProgressBar.tsx:86-95`; caixa com zero não entra na barra), botões "Nova movimentação",
"Novo depósito", "Extrato".
Regra (central de ajuda gerada do guia, `components/help-center/helpCenterData.generated.ts:635,1491`, e o diálogo de
abertura): cofre = todo o dinheiro em espécie da empresa; parte está reservada nos caixas abertos; o resto é o disponível.

## 6. Saque / Sangria
`components/cash-movement/CashMovementModal.tsx:47-98`: título "Saque / Sangria", botões "Saque" e "Sangria".
- Saque (`WithdrawalForm.tsx:604-851`): "Transferir dinheiro do banco para o cofre ou para um caixa aberto"; "Conta de
  origem"; "Destino do saque" ("Cofre (Conta DINHEIRO)" ou "Caixa de <operador>", com o saldo; padrão: o caixa do
  usuário logado, `:139-161`); "Valor do Saque"; "Data/hora do lançamento" (só com a permissão retroativa); "Descrição
  (Opcional)"; "Tem tarifa no saque?" ("Não"/"Sim"); "Valor da Tarifa"; "Efeitos desta transação:" com "Saldo da Conta
  Bancária / Diminuirá em R$ ..." e "Fundo de Caixa / Aumentará em R$ ..."; "Cancelar", "Confirmar Saque"; aviso "Saque
  realizado com sucesso!". Grava: saída do banco tipo transferência, a tarifa como **despesa** "Tarifa de Saque para o
  Caixa #N", a entrada no caixa tipo transferência "↓ SAQUE · <banco> → Caixa #N" (não é receita) e o espelho no cofre
  (`:340-440`). Destino = cofre com caixa aberto pede "Atenção: este saque vai para o Cofre" (`:857-887`).
- Sangria (`SangriaForm.tsx:406-591`): "Transferir dinheiro do cofre ou de um caixa aberto para uma conta bancária";
  "Origem da sangria"; "Conta de destino"; "Valor da Sangria"; "Descrição (Opcional)"; efeitos "Diminuirá em" /
  "Aumentará em"; "Confirmar Sangria"; "Sangria realizada com sucesso!".

## 7. Nova Movimentação Bancária
Botão "Nova Movimentação Bancária" → `components/NewBankTransactionModal.tsx:576-1041`, título "Nova Movimentação
Financeira" (`i18n/locales/pt-BR/bank.json`, `transactionModal.title`). "Tipo": "Entrada", "Saída", "Transferência" (com
mais de uma conta); "Conta bancária" (sem o cofre, `:720-727`); "Descrição"; "Valor *"; "Categoria *"; "Centro de custo";
vínculo com parceiro; "Não contar na DRE (saldo herdado / histórico)"; anexos; botões "Cancelar"/"Salvar"; aviso
"Movimentação registrada com sucesso!". Vai com o caixa da tela (`cashRegisterIdContext`, `:294,336`).

## 8. Fechar caixa
`handleCloseCash` (`Caixa.tsx:2312-2336`; com pedido não finalizado: "Não é possível fechar o caixa com pedidos não
finalizados") → diálogo `:3377-3605`.
- Título "Fechar Caixa #N"; descrição "Caixa de <operador> · Aberto em dd/MM/yyyy HH:mm".
- "Saldo de Abertura", "Restante em Caixa"; "Saídas": "Compras" e "Despesas"; "Entradas": "Vendas" e "Receitas"; cada
  um com "Dinheiro:", "PIX/Transf." e (compras/vendas) "Saldo:"; detalhamento por material (`CashClosingMaterialsAccordion`).
- "Valor de Fechamento": enquanto calcula, "Calculando saldo de fechamento..." e o botão travado; depois **vem preenchido
  com o valor esperado** (nunca negativo, `:1500-1562`); aceita negativo digitado (`allowNegative`, `:3536`; `:1923-1927`).
  "Digite o valor físico em dinheiro que está no caixa"; "Valor esperado pelo sistema: R$ X".
- Diferença: "Diferença detectada: ±R$ X" e a chave "Registrar diferença no DRE" ("O cofre é acertado pelo valor que você
  contou de qualquer jeito. Ligada, essa falta também conta como Prejuízo (despesa)..." ou "...sobra também conta como
  Ganho (receita)...") (`:3545-3584`).
- "Data/hora do fechamento" (permissão retroativa); "Cancelar", "Confirmar Fechamento".
- Ao confirmar (`:1909-2272`): grava o fechamento, a linha que devolve o dinheiro ao cofre (`:1941-1963`), o ajuste da
  diferença (`:1995-2029`); aviso "Caixa fechado com sucesso!"; janela "Imprimir Relatório" ("Deseja imprimir o relatório
  de fechamento de caixa?", "Não, obrigado", "Ver comprovante", "Imprimir" só com impressão direta,
  `components/CashClosingPrintModal.tsx:17-45`, `i18n/locales/pt-BR/orders.json:72-77`); a tela volta para "Início".

## 9. Reabrir
- Botão "Reabrir #N" do cartão âmbar → confirmação; link "reabrir outro caixa" (gestor, ou mais de um reabrível,
  `Caixa.tsx:941-942`) → `components/ReopenCashPickerDialog.tsx`: "Reabrir outro caixa", "Escolha qual caixa fechado
  deseja reabrir. Ele volta exatamente como estava antes do fechamento.", lista dos últimos 10 fechados (gestor vê os de
  todos, `Caixa.tsx:635-670`) com "#N", operador, horários e valor; "Cancelar" e "Reabrir #N".
- Confirmação `Caixa.tsx:3680-3739`: "Reabrir caixa #N?", "O caixa será reaberto exatamente como estava antes do
  fechamento. Todas as transações registradas continuarão associadas a este caixa.", "Cancelar", "Reabrir Caixa".
- Regra (`:807-895`): o operador dono não pode ter outro caixa aberto ("Este operador já possui um caixa aberto"); apaga
  a diferença gravada no fechamento; aviso "Caixa reaberto com sucesso!".

## Permissões citadas (`config/routes.ts`)
"Abrir Caixa" (`:270`), "Fechar Caixa" (`:271`), "Ver Dinheiro Total em Caixa" (`:272`), "Ver e Operar Todos os Caixas"
(`:274`), "Realizar lançamentos e abrir/fechar caixas com data retroativa" (`:275`), "Gerenciar Contas Bancárias" (`:279`).

## Backend usado
| Tela | Tabela / RPC |
|---|---|
| Caixa (leitura) | `cash_register` (abertos, último fechado, últimos 10 fechados), `profiles`, `companies` (`multi_cash_enabled`, `cash_account_enabled`, `cash_account_opt_out`), `bank_accounts`, `cash_transactions`, `purchases`, `sales`, `order_drafts` (pedidos não finalizados), RPC `get_dinheiro_balance` |
| Abrir | `cash_register` insert (`register_number` sequencial), `cash_transactions` insert (`opening`), RPC `get_dinheiro_balance`; `enable_cash_account` só se o cofre estiver desligado |
| Ajustar saldo (não gravado na aula) | `cash_transactions` (`adjustment`) |
| Saque | RPC `create_manual_bank_transaction` (perna do banco, tarifa e espelho do cofre), `cash_transactions` insert (`transfer`), RPC `adjust_cash_register_balance` |
| Nova Movimentação Bancária | RPC `create_manual_bank_transaction`, `financial_categories` |
| Fechar | `cash_register` update, `cash_transactions` insert (`closing`, `adjustment`), `profiles` |
| Reabrir | `cash_register` select/update, `cash_transactions` delete (diferenças do fechamento) |
| Cofre | RPC `get_dinheiro_balance` (`saldo_total`, `reservado_total`, `disponivel`, `caixas_abertos[]`) |

## Pegadinhas do código (handoff, a fala não depende)
- H1. A dica "R$ X foi o valor restante em dinheiro do último caixa (#N)" é do usuário logado, também quando o diálogo
  abre o caixa de outra pessoa (`Caixa.tsx:605-633,3345-3350`).
- H2. "Diminuirá em R$ 3006,50" no saque sai sem separador de milhar (`WithdrawalForm.tsx:798`).
- H3. Botão do aviso de saldo insuficiente é "Usar disponível", e a central de ajuda diz "Abrir com valor menor".
- H4. "Nova Receita" sugere "Ex: Suprimento de caixa" (`i18n/locales/pt-BR/caixa.json`, `depositModal.reasonPlaceholder`),
  e a aula ensina que dinheiro mudando de lugar (saque, sangria, suprimento) não é receita.
- H5. Nos modais lidos não achei movimento direto cofre → caixa aberto no meio do dia (o dinheiro entra no caixa na
  abertura ou por saque do banco); a fala não fala desse caminho. Conferir com o time.
