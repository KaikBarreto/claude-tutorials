# Inventário · T14 "Bancos, cofre e conciliação bancária" (EcoSistema 1.59.154)

Código lido (só leitura): `/home/claude/ecoflix/app-src-1.59.154/`. Caminhos relativos a `src/`. Formato `arquivo:linha`.
Rótulos entre aspas = texto exato da tela (pt-BR). Só o que a aula usa.

## 0. Conferência código × fonte (vale o código)

| # | Fonte diz | Código 1.59.154 | Onde |
|---|---|---|---|
| 1 | Financeiro → "Movimentações Bancárias" | Com o cofre ligado (o mundo), menu, título e aba viram **"Movimentações Financeiras"**; a rota não muda | `hooks/useFinancialMovementsLabel.ts:19-22`, `components/layout/SidebarMenuContent.tsx:289`, `pages/BankTransactions.tsx:610-628` |
| 2 | ⚠️ Saque e Nova Movimentação exigem caixa aberto ("Abra o caixa antes de realizar saques") | A frase não existe. O Saque só precisa de um destino: o cofre **ou** um caixa aberto; sem nenhum, toast "Nenhum caixa aberto para receber o saque. Abra um caixa primeiro.". Nova Movimentação não pede caixa | `components/bank/BankTransactionsContent.tsx:247-252,1204-1215`; `i18n/locales/pt-BR/bank.json` (`page.openCashFirstWithdrawal`) |
| 3 | Linha casada ganha a etiqueta "Conciliada" | Casar com lançamento existente = **"Casada"**; "Conciliada" é só o caso genérico | `components/reconciliation/EntryActionPanel.tsx:426-474` |
| 4 | ⚠️ OFX do Safra manda débito positivo: conferir o sinal | O parser já corrige DEBIT/CREDIT com sinal trocado; nos tipos ambíguos (XFER, ATM, PAYMENT, FEE...) respeita o arquivo | `utils/ofx/parseOfx.ts:262-306` |
| 5 | ⚠️ Arquivar não tem volta | Confere: não há "desarquivar" na tela (nenhum update `is_archived: false` fora de Materiais). O diálogo diz "Você poderá consultar os dados futuramente." | `components/bank/BankAccountDeleteDialog.tsx:54-56`; `hooks/useBankAccounts.ts:349-358` |
| 6 | (não cita) | Nova Conta ganhou o campo "Data desse saldo" quando há valor | `components/bank/BankAccountsManagement.tsx:191-208` |
| 7 | Buscar lançamento quando "o sistema não sugeriu" | Há blocos automáticos de "outra data" (valor exato fora de 3 dias) e de "valor quase igual" (mesmo dia, até R$ 2,00). A busca manual é o caminho quando a data **e** o valor diferem | `EntryActionPanel.tsx:2612-2796`; `hooks/useBankReconciliation.ts:72-89,165-171` |
| 8 | (não cita) | Logo do banco vem do serviço de favicon do Google e a lista de bancos da BrasilAPI: no mundo, contas **sem instituição** (sem logo de terceiros) | `hooks/useBrazilBanks.ts:109-120` |
| 9 | Categoria de sistema "Tarifas" | Confere com a central de ajuda ("Outras Receitas, Outras Despesas e Tarifas"); o nome vem do banco | `components/help-center/helpCenterData.generated.ts` (seção de categorias) |

## 1. Menu e página · `/movimentacoes-bancarias`
- Rota `App.tsx:542-546` (permissão `screen_movimentacoes_bancarias`); menu "Financeiro" `config/routes.ts:415-424`.
- Página `pages/BankTransactions.tsx`: breadcrumb "Banco" › "Movimentações Financeiras" (`:607-612`); título
  "Movimentações Financeiras", subtítulo "Controle de pagamentos via Pix/Transferência" (`:614-620`; `bank.json`
  `page.subtitle`); abas "Movimentações Financeiras" | "Conciliação" (`:624-647`, só com `canReconcileBank`).
- Lista lateral (`:239-430`): "Resumo"; "DINHEIRO (COFRE)" primeiro, depois a principal, depois em ordem alfabética
  (`:104-113`); saldo embaixo do nome; botões pontilhados "Nova Conta" e "Novo Cartão" (`:573-602`). Abre já na conta
  principal (`:178-186`).
- Menu de três pontinhos da conta bancária: "Tornar principal" (só se não é a principal) → toast "Conta padrão alterada";
  "Editar"; "Excluir" (não aparece na principal) (`:337-378`, `:193-200`). Do cofre: só "Ajustar saldo" (`:304-336`).
- Backend: `bank_accounts` select (`:96-100`); `useCashAccountEnabled`; `useCofreBalances` → RPC `get_dinheiro_balance`.

## 2. Cadastrar, editar e arquivar conta
- `components/bank/BankAccountsManagement.tsx`: "Nova Conta Bancária" / "Adicione uma nova conta para controlar suas
  movimentações" (editando: "Editar Conta Bancária" / "Altere os dados da conta bancária") (`:145-150`). Campos: "Nome
  da conta *" (placeholder "Ex: Bradesco PJ") (`:153-161`); "Instituição" ("Selecione a instituição...") (`BankInstitutionCombobox.tsx:84-92`);
  "Valor em conta (R$)" (`:168-186`), na edição a dica "Alterar este valor gerará um ajuste automático no saldo (sem
  impacto no DRE)." (`:181-185`); "Data desse saldo" + "Dia em que esse saldo aparecia no extrato do banco. Se você já tem
  movimentações depois dessa data, lance-as normalmente que elas entram por cima." (`:191-208`); "Cor identificadora"
  (`accountColors.tsx:38`); "Pré-visualização" (`:298-314`). Botões "Criar Conta" / "Salvar Alterações" e "Cancelar"
  (`:129-142`). Toasts "Conta criada com sucesso", "Conta atualizada" (`:108,119`).
- `hooks/useBankAccounts.ts`: criar = insert `bank_accounts` (`is_default` false) + com valor ≠ 0 insert `bank_transactions`
  "Ajuste de saldo - Saldo inicial" (`excluded_from_dre` true, `transaction_at` = data do saldo) + RPC `update_bank_balance`
  (`:228-293`); editar com diferença = insert "Ajuste de saldo - Correção manual" + `update_bank_balance` + update
  (`:295-347`); "Tornar principal" = RPC `set_default_bank_account` (`:456-468`); arquivar = update `is_archived` true
  (`:349-358`); migrar = move `bank_transactions`, recalcula e apaga a conta (`:360-428`).
- `components/bank/BankAccountDeleteDialog.tsx`: "Remover conta bancária" / "Como deseja proceder com a conta
  **{nome}**?"; opções "Arquivar" ("Oculta a conta mantendo todo o histórico") e "Migrar e Excluir" ("Transfere
  transações para outra conta e exclui permanentemente"); modo arquivar: "Arquivar conta" + "A conta será ocultada das
  listagens mas todo o histórico de transações será preservado. Você poderá consultar os dados futuramente." + botão
  "Arquivar"; "Cancelar" (`:45-151`). Toast "Conta arquivada com sucesso" (`pages/BankTransactions.tsx:202-210`).
- Histórico: ajuste aparece com a etiqueta preta "Ajuste" (descrição começando por "Ajuste de saldo")
  (`BankTransactionsContent.tsx:594-601,1658-1661`).

## 3. Cofre (DINHEIRO (COFRE))
- `components/dinheiro/CashAccountCard.tsx:121-170`: "O cofre da empresa", saldo, "Saldo Total em Dinheiro", barra
  ("Disponível no cofre", "Caixa de {operador}", `:103-109`), botões "Nova movimentação", "Novo depósito", "Extrato".
- `components/dinheiro/AdjustBalanceDialog.tsx`: "Ajustar saldo da Conta DINHEIRO"; "Saldo atual"; "Novo saldo";
  "Diferença" (verde/vermelha); "Motivo *" (placeholder "Ex: conferência de inventário"); "Cancelar", "Confirmar ajuste"
  (`:297-411`). Toasts "Motivo obrigatório", "Nenhuma diferença", "Saldo ajustado" + "+R$ … registrado no histórico"
  (`:218-295`). Backend: insert `cash_transactions` (`type` adjustment, `excluded_from_dre` true, descrição "Ajuste de
  saldo — {motivo}") (`:250-269`); saldo pela RPC `get_dinheiro_balance`.

## 4. Conta bancária: cartão, Nova Movimentação, Transferência, Saque
- Cartão (`BankTransactionsContent.tsx:1158-1251`): nome, saldo, olho; botões "Saque", "Sangria" (cofre ligado e conta não
  é o cofre), "Nova Movimentação", "Extrato". "Histórico de Movimentações", período "Este mês" (`:193`), busca "Buscar por
  descrição ou valor..." (`:1254-1288`). Backend: `bank_transactions`/`get_financial_movements`.
- `components/NewBankTransactionModal.tsx`: "Nova Movimentação Financeira" (`:579`); "Tipo": "Entrada", "Saída",
  "Transferência" (este só com 2+ contas e fora do cofre) (`:583-628`); "Conta bancária" (`BankAccountSelect`, sem o
  cofre) (`:720-727`); "Descrição" ("Ex: Recebimento de pagamento") (`:730-741`); "Valor *"; "Data/hora do lançamento"
  (`:873-879`); "Categoria *"; "Centro de custo" (`:960`); "Vincular a fornecedor/cliente (opcional)"
  (`financial/PartnerLinkField.tsx:70`); "Não contar na DRE (saldo herdado / histórico)" (`:998`); botões "Cancelar",
  "Salvar"/"Transferir" (`:560-572`). Transferência: "Conta de origem" (vem a conta aberta), "Conta de destino",
  "Descrição (opcional)", "Prévia da transferência:" (`:631-760`, `:1028`). Toasts "Movimentação registrada com
  sucesso!", "Transferência realizada com sucesso!" (`:411`). Validações `:499-552` ("Selecione a conta de origem e
  destino", "A conta de origem e destino devem ser diferentes"). Backend: `insertBankTransaction` (duas pernas com o mesmo
  `group_id`, `excluded_from_dre` true na transferência) (`:316-374`).
- Saque: `components/cash-movement/CashMovementModal.tsx:46-98` ("Saque / Sangria", botões "Saque" e "Sangria");
  `WithdrawalForm.tsx:604-852`: "Transferir dinheiro do banco para o cofre ou para um caixa aberto"; "Conta de origem";
  "Destino do saque" ("Cofre (Conta DINHEIRO)" com o saldo, ou "Caixa de {operador}"); "Valor do Saque"; "Descrição
  (Opcional)"; "Tem tarifa no saque?" ("Não"/"Sim"); "Valor da Tarifa"; "Efeitos desta transação:" com "Saldo da Conta
  Bancária · Diminuirá em R$ …" e "Cofre (Conta DINHEIRO) · Aumentará em R$ …"; "Cancelar", "Confirmar Saque". Destino
  padrão: o cofre, salvo caixa aberto do usuário ou único (`:131-160`); com caixa aberto e destino cofre, confirma
  "Atenção: este saque vai para o Cofre" (`:855-887`). Toast "Saque realizado com sucesso!" (`:443`). Backend (destino
  cofre, `:200-281`): insert duplo em `bank_transactions` ("↑ SAQUE · {conta} → Cofre (DINHEIRO)" e "↓ SAQUE · {conta} →
  Cofre", `excluded_from_dre` true, mesmo `group_id`), RPC `update_bank_account_balance` ×2, tarifa "Tarifa de Saque para
  o Cofre" (type expense) por `insertBankTransaction`.

## 5. Resumo
`components/dinheiro/FinancialSummaryWithCash.tsx:356-480`: "Resumo financeiro", "Dinheiro e contas bancárias",
"{n} fontes", o total, "Dinheiro", "Contas bancárias" ("{n} contas cadastradas"), "Distribuição do saldo";
`components/bank/BankTransactionsSummary.tsx:285-324` "Como funciona?" (recolhível).

## 6. Conciliação
- Aba: `components/reconciliation/ReconciliationTab.tsx`: "Conta para conciliar" (`BankAccountSelect` com
  `autoSelectDefault`: já vem a principal) (`:155-160`; `BankAccountSelect.tsx:98,164-166`); "Como funciona?" (`:166-173`);
  com extrato aberto, "Voltar" (finalizado: "Fechar") e "Importar outro" (`:175-199`); sem extrato: "Nenhum extrato em
  conciliação" + "Suba o arquivo .ofx do banco para casar cada linha com uma movimentação, dar baixa em contas ou criar
  lançamentos." + "Importar novo extrato" (`:216-264`); "Continuar conciliação" ("Faltam {n} de {m} linhas", "Continuar")
  (`:328-384`); "Conciliações anteriores ({n})" com o selo "Conciliado" (`:266-295,388-416`). Backend: RPC
  `get_statement_imports` (`hooks/useBankReconciliation.ts:476-500`).
- "Como funciona?": `ReconciliationHelpModal.tsx`: "Como funciona a conciliação bancária" (`:321,339`), "O que é conciliar?"
  e "Conciliar é conferir, uma a uma, as linhas do extrato do banco contra os lançamentos do seu sistema, até bater tudo
  …" (`:46-58`); passos 1 a 3 (`:61-300`).
- Importar: `ImportOfxDialog.tsx`: "Importar extrato OFX" / "Suba o arquivo .ofx do banco para conciliar as
  movimentações." (`:264-273`); área "Arraste o arquivo .ofx aqui ou clique para selecionar" + "Extrato do banco no formato
  OFX — até 5 MB" (`:405-408`); "Como pegar o arquivo do seu banco?" (`:434-500`); arquivo + "Trocar" (`:501-519`);
  "Prévia do extrato": "Banco", "Conta do arquivo", "Período", "Transações", "Saldo final do extrato … em {data}"
  (`:529-576`); aviso de conta só com dígitos no nome da conta (`:89-101,579-590`); "Cancelar", "Importar"; depois
  "Extrato importado" / "{n} de {m} linhas importadas" / "Tudo certo — nenhuma linha estava repetida." / "Concluir"
  (`:233-330`). Erros: `:144-189`. Backend: parse no navegador (`utils/ofx/parseOfx.ts`), RPC `create_bank_statement_import`
  (`p_bank_account_id, p_file_name, p_file_hash, p_bank_id, p_acct_id, p_period_start, p_period_end, p_ledger_balance,
  p_ledger_balance_date, p_entries[]`) → `{import_id, inserted_count, total_entries, skipped_count, skipped_dup_count,
  skipped_samples, opening_balance}`; toast "Extrato importado — {n} transações" (`useBankReconciliation.ts:596-696`).
- Tabela: `ReconciliationTable.tsx`: "Cancelar conciliação" (`:352-362`); faixa "Conciliação finalizada — somente
  leitura" (`:373-380`); cabeçalho "Linha do extrato" | "Conciliação" + caixa "Marcar todas pendentes" (`:434-451`); linha:
  data, etiqueta do TRNTYPE, memo (ou nome), valor "+"/"−" verde/vermelho (`:567-623`). Etiquetas: XFER "Transferência",
  FEE/SRVCHG "Tarifa", PAYMENT "Pagamento", ATM "Caixa eletrônico", DEP "Depósito"; DEBIT e CREDIT sem etiqueta
  (`lib/reconciliation/trnTypeLabel.ts:17-34`). Estado: RPC `get_bank_reconciliation_state` + `reconcile_find_distant_exact_candidates`
  (`useBankReconciliation.ts:528-560`).
- Painel da linha pendente (`EntryActionPanel.tsx`): sugestão "Casa com um lançamento no sistema" + o lançamento (pedido
  "Compra #{n} • {parceiro}" ou a descrição, data, valor) + botão "Casar com {pedido}" ou "Confirmar" (`:2512-2577`; rótulo
  `:306-318`); ambíguo "Atenção: há {n} lançamentos de R$ … que podem casar com esta linha. Escolha qual deles é o certo
  para evitar duplicidade." + "Escolher lançamento" (`:2580-2607`); outra data (`:2612-2695`); valor quase igual
  (`:2704-2796`); primário "Baixar conta" (há conta compatível) ou "Criar receita"/"Criar despesa", e "Mais ações"
  (`:3028-3095`); itens de "Mais ações": "Baixar conta" (sem conta: "Nenhuma conta em aberto bate com esta linha"), "Criar
  receita"/"Criar despesa", "Ajuste" ("Abre o lançamento com a opção de não contar na DRE"), "Funcionário" (só saída),
  "Saldo do cliente/fornecedor", "Casar com transferência" ("Dinheiro que veio de outra conta sua"), "Buscar
  lançamento", "Casar com vários lançamentos", "Ignorar" (`:3096-3217`); rodapé "Sem casamento automático. Veja os outros
  destinos (…) em “Mais ações”." (`:3224-3245`).
- Sub-modos: "Escolha o lançamento que casa com esta linha" + "Casar com o selecionado" (`:1093-1202`); "Buscar lançamento
  para casar", busca "Nome do cliente/fornecedor, nº do pedido...", "Mostra lançamentos de R$ … (ou com até R$ 2,00 de
  diferença) — casa mesmo com data diferente da linha do extrato.", selo "dif. −R$ …", "Casar com selecionado"
  (`:1205-1383`, `:346-349`); "Casar com valor diferente?" / "O lançamento é R$ … e a linha é R$ …. Casar assim? A diferença
  de R$ … vai pro resumo de ajustes." / "Casar assim" (`ConfirmDiffMatchDialog.tsx:48,61-85`); "Baixar conta a pagar"
  (ou "a receber"), "Selecione a conta" (descrição, parceiro · restante), "Dar baixa de R$ …" (`:1734-1829`; contas em aberto
  do mesmo lado e mesmo restante, `:872-880`); "Vale / pagamento de funcionário" + aviso "Para salário mensal com
  holerite, lance em Funcionários e depois use Buscar lançamento aqui. Este atalho é para adiantamento/vale ou pagamento
  simples pago por PIX — ele já registra tudo, então não lance de novo em Funcionários." (`:1832-1858`); "Criar
  lançamento de saída" (ou "de entrada"), aviso azul "Veio de outra conta sua? Volte e use Casar com transferência. Criar
  aqui registraria o valor de novo e aumentaria o saldo em dobro.", chave "Não é receita nem despesa (só ajusta o saldo)",
  "Categoria *" ("Selecione a categoria"), "+" ("Nova categoria"), "Centro de custo", "Descrição" (vem o memo), "Criar
  R$ …", "Escolha a categoria acima para liberar o lançamento." (`:2179-2412`, descrição inicial `:599-601`).
- Linha resolvida (`:895-992`): selo "Casada", "Criada", "Baixada", "Funcionário", "Ignorada"; botão "Desfazer"; pede
  "Desfazer conciliação?" só para Criada, Baixada, Funcionário, Saldo e grupo ("Isso vai estornar o lançamento e recalcular
  o saldo. Continuar?"; "Isso vai estornar a baixa da conta e recalcular o saldo. Continuar?"), botões "Cancelar" e
  "Desfazer".
- Seleção em lote (`ReconciliationBulkBar.tsx:45-125`): "{n} selecionada(s)", "Soma: ±R$ …", "Casar com transferência",
  "Casar {n} linhas com um lançamento", "Ignorar ({n})", "Desfazer ({n})", "Limpar seleção"; confirmação "Ignorar {n}
  linhas?" / "Elas saem do cálculo do saldo e podem ser desfeitas depois." / "Cancelar" / "Ignorar".
- "Casar com transferência" (`ReconciliationTransferMatchDialog.tsx`): título "Casar com transferência" (`:100`),
  "Escolha a transferência entre suas contas que corresponde às linhas do extrato." (`:133`), "Valor da linha", candidato
  "{origem} → {destino}", data, descrição ("Transferência entre contas"), valor (`:215-240`); "Isso só cria o vínculo da
  conciliação. Nenhum lançamento é criado e o saldo não muda." (`:151`); "Casar transferência" (`:123`). Toast "Linha casada
  com a transferência".
- "Cancelar conciliação" (`CancelReconciliationDialog.tsx`): "Cancelar esta conciliação?" + descrição + a lista do que
  volta (`:120-160`); "Digite CANCELAR para confirmar" (`:162-168`); "Manter conciliação" / "Cancelar e reverter tudo"
  (`:92,107`). RPC `cancel_bank_reconciliation`.
- Rodapé (`ReconciliationBalanceFooter.tsx`): "Saldo do banco" (= saldo final do OFX), "Saldo conciliado" (= saldo inicial
  + linhas resolvidas, sem as ignoradas), "Diferença" (verde em zero), "Diferenças casadas" (âmbar, popover "Diferenças de
  valor casadas" / "Linhas casadas com um lançamento de valor um pouco diferente. Não altera o saldo conciliado.")
  (`:14-33,62-101,282-330`); "Finalizar conciliação" só com diferença zero e nenhuma pendente; "Ainda há {n} linhas
  pendentes" / "A diferença precisa estar zerada" (`:115-128`); selo "Conciliação finalizada" (`:356`).
- RPCs das ações (`useBankReconciliation.ts`): `reconcile_match_existing` (toast "Linha casada"), `reconcile_search_candidates`,
  `reconcile_search_transfer_candidates` + `reconcile_match_existing` com `p_allow_any_date` (`:974-1030`),
  `reconcile_find_in_other_accounts`, `reconcile_create_transaction` ("Lançamento criado"), `reconcile_settle_bill` ("Conta
  baixada"), `reconcile_ignore_entries_batch` ("{n} linha(s) ignorada(s)"), `reconcile_unmatch_entry` ("Conciliação desfeita"),
  `cancel_bank_reconciliation`, `finalize_bank_reconciliation` ("Conciliação finalizada").

## 7. Excluir lançamento conciliado (só falado)
`components/bank/DeleteBankMovementDialog.tsx:169-196`: RPC `delete_bank_transaction_atomic`; recusa do banco →
toast "Este lançamento está conciliado. Desfaça a conciliação antes de excluir.".

## 8. O arquivo OFX (o que o parser aceita)
`utils/ofx/parseOfx.ts`: SGML 1.x ou XML 2.x; charset do cabeçalho (`CHARSET:1252`); `DTPOSTED` com ou sem hora e fuso
(`[-3:BRT]`), sem hora ancora meio-dia; tag-folha sem fechamento; um `<STMTRS>` só (dois: "Este arquivo tem mais de uma
conta. Exporte o extrato de uma conta por vez."); linhas com memo começando por "SALDO" são descartadas; `BANKID`,
`ACCTID`, `DTSTART`/`DTEND`, `LEDGERBAL` (`BALAMT`, `DTASOF`); sinal corrigido só para DEBIT/CREDIT (`:262-306`).
Modelo de estrutura: `utils/ofx/fixtures/itau_sgml.ofx`.
