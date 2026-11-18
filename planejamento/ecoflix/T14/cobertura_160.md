# Cobertura 1.60.10 · T14 Bancos, cofre e conciliação bancária

Auditoria de 18/11/2026, só leitura de código. Base: `/dev/shm/ecoflix-src` (1.60.10) contra o roteiro (1.59.154).
Caminhos relativos a `src/`, linhas do 1.60.10. `BTC` = `components/bank/BankTransactionsContent.tsx`, `BDD` =
`components/bank/BulkDeleteBankMovementsDialog.tsx`, `BCD` = `components/financial/BulkEditFinancialCategoryDialog.tsx`,
`FDF` = `components/financial/FinancialDescriptionField.tsx`, `EAP` = `components/reconciliation/EntryActionPanel.tsx`,
`BAS` = `components/BankAccountSelect.tsx`. A varredura do robô (`rec/varredura/t14.txt`) ainda não existe.

**Mudaram** entre `f37573ea0` e `5290be4cd` (das telas desta aula): `BTC` (+287), `BDD` e `BCD` (novos), `BAS`,
`hooks/useBankAccounts.ts`, `pages/BankTransactions.tsx` (só a chave da consulta), `BankInstitutionCombobox.tsx` (ícone
de reserva), `ReconciliationTransferMatchDialog.tsx` e `ReconciliationGroupMatchDialog.tsx` (só cor do item marcado).
**Sem mudança nenhuma**: `NewBankTransactionModal.tsx`, `BankAccountsManagement.tsx`, `BankAccountDeleteDialog.tsx`,
`components/dinheiro/*` (cofre, ajuste, resumo), `components/cash-movement/*` (saque, sangria), os cartões de crédito
(`CreditCard*.tsx`, `PayCreditCardBillModal.tsx`), o menu e, na conciliação, `ReconciliationTab`, `ReconciliationTable`,
`EntryActionPanel`, `ImportOfxDialog`, `ReconciliationBulkBar`, `ReconciliationBalanceFooter`,
`CancelReconciliationDialog`, `ReconciliationHelpModal`, `useBankReconciliation.ts`, `utils/ofx/*`. Ou seja: **os
capítulos 05 a 14 batem com a tela**; o que muda de verdade é o histórico da conta (caps. 01, 02 e 04).

Sobre as três novidades do pedido:
- **Exclusão em massa (1.60.1)**: está nesta tela e não tem cobertura. Veio junto, na mesma barra, o **"Alterar
  categoria"** em lote, que as notas de versão não citam. Proposta P2.
- **Preenchimento inteligente com conta e forma (1.60.5, 1.60.7 e 1.60.8)**: **não existe na "Nova Movimentação
  Financeira"** desta tela (`NewBankTransactionModal.tsx` não mudou e não usa o `FDF`). Ele vive na "Nova Despesa" e na
  "Nova Receita" do Caixa (`WithdrawalModal.tsx`, `DepositModal.tsx`: aula **T6**) e na "Nova conta" de Contas a
  Pagar e Receber (`BillFormModal.tsx`: aula **T13**). Na tela da T14 ele só aparece num lugar: o botão "Nova despesa"
  do cartão de crédito, que abre a mesma `WithdrawalModal` (`CreditCardContent.tsx:62-73,220`). Ver L3 e P4.
- **Contas bancárias por usuário (1.59.165)**: o efeito aqui é a lista lateral e os seletores mostrarem só as contas
  liberadas. Ver L4 e P1.

## 1. Mudou no app (por capítulo)

**cap01, cap02 e cap04 (todo capítulo que mostra o "Histórico de Movimentações" de uma conta bancária)**
1. O cabeçalho do histórico ganhou o botão **"Selecionar lançamentos"** (ícone de lista marcada), à esquerda do
   período "Este mês" e da busca (`BTC:1382-1399`). Só aparece quando o período tem pelo menos um lançamento que se
   pode excluir, e nunca no cofre (`BTC:650-653`; regra em `components/bank/acoesDaLinhaDeExtrato.ts`,
   `podeExcluirLinha`). Clicado, vira **"Cancelar seleção"**. A fala atual não fica errada, mas a câmera e as medidas
   do cabeçalho mudam (o período e a busca andam para a direita). No cap01 a fala do histórico deve citar o botão (P1).
2. Com a seleção ligada, a primeira coluna da tabela alarga e ganha caixas de marcar, e somem o menu de três
   pontinhos e o ícone "Transferir para outra conta" de cada linha (`BTC:1706-1715,1840-1853,1940,1958`). Não afeta
   o roteiro atual (ele não liga a seleção), só o capítulo novo.

**cap07 · Casar com o sistema**
3. Na janela "Casar com transferência", a candidata marcada deixou de ser azul claro: agora é **azul cheio com o
   texto branco** (`ReconciliationTransferMatchDialog.tsx:205-231`). A fala e o zoom valem; o quadro gravado muda.

**cap13 · Desfazer e cancelar**
4. A dica final ("lançamento conciliado não sai pelo Excluir das movimentações") continua certa e ganhou um irmão: no
   lote, o aviso é **"Um dos lançamentos está conciliado. Desfaça a conciliação antes de excluir o lote."**
   (`BDD:39-41`). Entra na fala do capítulo novo (P2), não aqui.

Nada mais mudou nas telas que o roteiro mostra. As contas do mundo não têm instituição, então a troca do ícone de
reserva do logo (`BankInstitutionCombobox.tsx:184-199`) não aparece.

## 2. Falta cobrir

Veredito: **sim** = vale capítulo ou trecho (ver a proposta); **citar** = uma frase; **não** = fica de fora, com o motivo.

### Novidades do 1.60

| # | O que é (rótulos do código) | Quando o cliente usa | Vale? |
|---|---|---|---|
| L1 | **Exclusão em massa** (1.60.1). "Selecionar lançamentos" → barra "{n} lançamentos selecionados" / "Selecione até 100 itens. Lançamentos protegidos não exibem caixa de seleção.", caixa "Selecionar lançamentos elegíveis desta página", "Limpar", "Alterar categoria", **"Excluir selecionados"** (`BTC:1428-1481`). Janela "Excluir {n} lançamentos?": "A seleção da conta {conta} será excluída em uma única operação. Se qualquer item não puder ser excluído, nenhum lançamento será alterado.", "Entradas selecionadas", "Saídas selecionadas", o aviso "Transferências, câmbios e baixas podem possuir lançamentos relacionados. Nesses casos, o sistema desfaz o grupo completo seguindo as mesmas regras da exclusão individual.", "Essa ação não pode ser desfeita.", "Cancelar" / "Excluir selecionados" (`BDD:118-170`). Aviso "{n} lançamentos excluídos." (`BDD:92-96`). RPC `delete_bank_transactions_batch_atomic(p_tx_ids)`. Limite: "Selecione no máximo 100 lançamentos por vez." (`BTC:710`). A seleção zera ao trocar de conta, de período ou de busca (`BTC:687-692`). Só marca lançamento avulso (sem pedido) de entrada, saída ou transferência; Pix de compra e venda não ganha caixa. | Lançou em dobro, lançou testes, importou errado: apaga tudo de uma vez em vez de linha por linha. | **sim** (P2) |
| L2 | **Alterar categoria em lote** (mesma barra). Janela "Alterar categoria de {n} lançamentos" / "Escolha a categoria que será aplicada ao lote inteiro.", "Despesas selecionadas" (ou "Receitas selecionadas"), "{n} no banco · Valores e saldos não mudam.", "Nova categoria (despesa)", "Escolha a nova categoria", opção "Sem categoria", "Aplicar categoria" (`BCD:155-250`). Aviso "Categoria de {n} lançamentos atualizada." Travas escritas na barra: "Transferências e ajustes não recebem categoria." e "Selecione apenas entradas ou apenas saídas para alterar a categoria." (`BTC:680-686`). RPC `update_financial_transaction_categories_batch`. | Arrumar a DRE: vários lançamentos caíram em "Outras Despesas" e precisam ir para a categoria certa. | **sim** (P2) |
| L3 | **Preenchimento inteligente** (`FDF`): digitando 3 letras na descrição aparece "Padrão encontrado: {descrição}", a linha com parceiro · categoria · centro de custo · conta (ou "Dinheiro (Caixa)") · "Pix / Transferência", "Boleto" ou "Cheque", "Usado {n} vezes · última vez em {mês de ano}" e o botão **"Preencher"**; setas, Enter ou Tab escolhem; depois "Campos preenchidos. Desfazer preenchimento" (`FDF:133-156`). Conta e forma só entram se ninguém escolheu antes (`FDF:79-98`). | Despesa que se repete todo mês (energia, internet). | **Aula T6** (Nova Despesa e Nova Receita do Caixa) e **T13** (Nova conta). Aqui: só dentro do capítulo do cartão (P4), se ele for aprovado; senão, **não**. A "Nova Movimentação Financeira" do cap04 não tem o recurso: não prometer na fala. |
| L4 | **Contas por usuário, o efeito** (1.59.165): com a restrição "Usar somente as contas bancárias liberadas", a pessoa só vê na lista lateral e nos seletores as contas marcadas; cofre e cartões não mudam (`config/routes.ts:361-366`); sem nenhuma conta liberada, o seletor mostra "Nenhuma conta bancária foi liberada para o seu usuário. Peça ao administrador para revisar seu acesso." (`BAS:221-239`); gravar em conta não liberada devolve "Esta conta bancária não está liberada para o seu usuário." (migração `20261112224000`). Usuário restrito também não consegue criar conta nova. | Operador que só pode pagar por uma conta. | **citar** (P1, uma frase). O cadastro é da **T2**. O Rafael é MASTER: nada muda na tela gravada. |
| L5 | Duas ações novas de permissão da tela: "Registrar Movimentação Bancária" e "Registrar Transferências Financeiras" (`config/routes.ts:269-270`). | Montar o acesso de um operador. | **não** aqui: **T2** (já no `T02/cobertura_160.md`, item 10). |
| L6 | Cato faz tarefas do financeiro pela conversa (1.60.0). | | **não** aqui: **T21**. |

### Tela das contas (existe desde antes e o roteiro não mostra)

| # | O que é | Quando o cliente usa | Vale? |
|---|---|---|---|
| L7 | **Menu de três pontinhos da linha** ("Ações do lançamento"): **"Editar"** → janela "Editar lançamento" com "Valor (R$)" e "Conta", aviso "Lançamento atualizado."; **"Excluir"** → "Excluir lançamento?", "{descrição} será removido e o saldo da conta {conta} será ajustado em R$ …", "Essa ação não pode ser desfeita.", aviso "Lançamento excluído." (`BTC:763-806`; `EditBankMovementDialog.tsx:78-108`; `DeleteBankMovementDialog.tsx:200-255`). Linha protegida abre "Este lançamento não pode ser excluído por aqui" com o botão "Entendi". | Digitou o valor errado, lançou na conta errada, lançou o que não devia. | **sim** (P2). Hoje o roteiro só fala do Excluir, sem mostrar. |
| L8 | **Ícone "Transferir para outra conta"** no fim da linha → janela "Transferir Movimentação" ("Transferir esta saída de R$ … para outra conta bancária"), "Conta destino", "Transferir", aviso "Movimentação transferida com sucesso" (`BTC:1940-1950`; `BankTransactionTransferModal.tsx:140-160`). | O lançamento está certo, mas caiu na conta errada. | **citar** (P2, uma frase; faz o mesmo que trocar a "Conta" no Editar). |
| L9 | Linha de pedido abre para baixo (itens, formas de pagamento, observação) (`BTC:1830-1838`). | Conferir de qual pedido veio o Pix. | **citar** (P1). |
| L10 | **"Extrato"** → janela "Exportar Extrato Bancário": "Formato" ("PDF", "Excel"), "Período" ("Hoje", "Esta semana", "Este mês", "Mês passado", "Últimos 3 meses", "Últimos 6 meses", "Este ano", "Personalizado" com "De" e "Até"); no Resumo, a lista "Contas" com "Todas" e "Nenhuma" (`BankReportExportModal.tsx:186-290`). No cofre: "Exportar Extrato — Dinheiro (Cofre)". | Mandar o movimento da conta para o contador; guardar o fechamento. | **sim** (P1, trecho). O botão já aparece no cap01 sem ser aberto. |
| L11 | Filtro de período do histórico, ordenar pelas colunas, paginação e o olho que esconde os valores. | Olhar outro mês; esconder o saldo com gente por perto. | **citar** (P1). |
| L12 | "Nova Movimentação Financeira": o tipo **"Entrada"**, "Data/hora do lançamento" e "Vincular a fornecedor/cliente (opcional)" (`NewBankTransactionModal.tsx`, linhas do inventário). O roteiro só faz Saída e Transferência. | Rendimento, devolução, dinheiro que entrou sem pedido; lançar com a data de ontem. | **citar** (P3, uma linha). |
| L13 | **Cartão de crédito**: "Novo Cartão" → "Novo Cartão de Crédito" ("Cadastre o cartão para lançar despesas e acompanhar as faturas"), "Nome do cartão *", "Dia do fechamento *", "Dia do vencimento *", a frase "A fatura que fecha no dia {n} vence no dia {m} do mês seguinte. Compras feitas no dia do fechamento já entram na próxima fatura.", "Limite do cartão", "Criar Cartão" (`CreditCardFormDialog.tsx:159-250`); o cartão na lista com "Fatura em aberto", "Limite total:", "Disponível:", "fecha dia {n} · vence dia {m}", "Nova despesa" e "Extrato" (`CreditCardContent.tsx:100-195`); painel "Faturas" com os selos "Aberta", "Parcialmente paga" e "Paga", **"Pagar Fatura"** (janela "Pagar Fatura", "Data do pagamento *", "Origem do pagamento", "Observação (opcional)", "Este pagamento quita a fatura." ou "Restante após este pagamento: R$ …"; avisos "Fatura paga" / "Pagamento parcial registrado") e "Estornar" ("Estornar pagamento da fatura?") (`CreditCardBillsPanel.tsx:392-603`; `PayCreditCardBillModal.tsx:144-225`); menu do cartão com "Editar" e "Excluir" ("Remover cartão"). | Empresa que paga combustível, peça e assinatura no cartão e quer a despesa no mês certo e a fatura controlada. | **sim, capítulo** (P4), **depende de decisão**: nenhuma aula da trilha cobre cartão e o `PRODUCAO.md` registra "o mundo não tem cartão". O roteiro mostra o botão "Novo Cartão" no cap01 e não diz para que serve. |
| L14 | "Migrar e Excluir" executado; "Tornar principal" clicado. | | **não**: já falados; clicar muda o mundo das aulas seguintes (decisão 1 do `plano.md`). |
| L15 | Cofre: "Nova movimentação", "Novo depósito" e "Extrato" do cartão do cofre; a **Sangria** feita de ponta a ponta. | | **não** aqui: **T6** (cap09, saque e sangria). O cap04 já aponta a Sangria. |
| L16 | Contas em outra moeda e câmbio ("Excluir o câmbio (as 2 pernas)"); contas compartilhadas entre matriz e filial. | | **não**: o mundo é só em real; matriz e filial são da **T22**. |
| L17 | "Como funciona?" do Resumo. | | **não**: texto de ajuda, sem ação. |

### Conciliação (existe desde antes e o roteiro não mostra)

| # | O que é | Quando o cliente usa | Vale? |
|---|---|---|---|
| L18 | "Mais ações" › **"Saldo do cliente/fornecedor"** → painel "Baixar na conta-corrente": "Use quando esta linha é o acerto de um pedido finalizado no saldo. Não precisa bater o valor: um pedido de R$ 30.000,00 pode ser acertado em vários pagamentos — cada linha abate o que ela vale.", "Cliente ou fornecedor *", o saldo do parceiro, "Descrição" (vem "Valor Pago a {nome}" ou "Valor Recebido de {nome}"), "Dar baixa de R$ …" (`EAP:2011-2140`). | Pix de acerto de fiado: o pedido foi fechado no saldo e o pagamento veio depois, em partes. É o caso mais comum de ferro-velho. | **sim** (P6) |
| L19 | "Mais ações" › **"Casar com vários lançamentos"** ("Um Pix que pagou dois pedidos, por exemplo"): marca dois ou mais lançamentos até a soma fechar; botão "Casar com {n} lançamentos" (`EAP:1440-1700,3183-3200`). | Um Pix só pagando duas vendas. | **sim** (P6) |
| L20 | Barra de seleção: **"Casar {n} linhas com um lançamento"** → janela "Casar {n} linhas com um lançamento" ("… Escolha o lançamento no sistema que corresponde a essas linhas juntas (ex.: o saque total do dia)."), botão "Casar {n} linhas" (`ReconciliationBulkBar.tsx:91-104`; `ReconciliationGroupMatchDialog.tsx:141-262`). Na mesma barra: "Casar com transferência" em lote, "Desfazer ({n})" e a caixa "Marcar todas pendentes" (`ReconciliationTable.tsx:444`). | O banco quebrou em duas linhas o que no sistema é um lançamento só. | **sim** (P6); o resto da barra, **citar**. |
| L21 | Bloco **"Achamos este lançamento em outra conta"** ("O valor e a data batem com esta linha, mas ele está guardado em outro lugar, por isso não aparece aqui pra casar.") com o botão "Mover para {conta} e casar" e a confirmação "Mover o lançamento para {conta}?" (`EAP:2813-3010`; `ConfirmMoveAndMatchDialog.tsx:84-175`). | O Pix foi lançado na conta errada (ou como Dinheiro) e o extrato mostra onde ele caiu de verdade. | **sim** (P6) |
| L22 | Blocos automáticos de **outra data** ("Encontramos 1 lançamento de R$ … nesta conta, mas em outra data. Confira antes de criar uma nova baixa." + "Casar com este lançamento") e de **valor quase igual** ("Atenção: nenhum lançamento de R$ … bate exatamente com esta linha, mas há 1 lançamento com valor quase igual. Confira antes de casar — a diferença vai pro resumo de ajustes.") (`EAP:2612-2800`). | Pagamento que caiu dias depois; centavos de diferença no mesmo dia. | **citar** (P5, uma dica no cap10: explica por que ali foi preciso buscar). |
| L23 | "Mais ações" › **"Ajuste"** ("Abre o lançamento com a opção de não contar na DRE") → "Registrar ajuste de saída" (ou "de entrada"), botão "Registrar ajuste R$ …" (`EAP:2215-2218,2403`). | Linha que só acerta saldo: estorno, saldo herdado. | **citar** (P5, uma linha no cap09; a chave já aparece desligada). |
| L24 | "Mais ações" › "Funcionário" → "Vale / pagamento de funcionário": funcionário, "Vale" ou "Pagamento", "Registrar vale de R$ …" (`EAP:1836-1995`). | Vale pago por Pix. | **não** repetir: já citado no cap09; a demonstração depende do cadastro de funcionários (**T19**, módulo). |
| L25 | "Criar receita" (linha de entrada), o "+" de "Nova categoria" e o "Centro de custo" do painel de criar. | Rendimento da conta, entrada sem lançamento. | **citar** (P6, uma linha). |
| L26 | "Importar outro"; reimportar o mesmo arquivo ("Este extrato já tinha sido importado antes"; "Veja o que entrou e o que já constava no extrato desta conta."); "Essa transação já foi conciliada" ao criar em dobro. | | **não**: o cap06 já fala da reimportação; mostrar exigiria encenar erro. |
| L27 | Erros do arquivo ("Arquivo muito grande. O limite é 5 MB.", "Este arquivo tem mais de uma conta. Exporte o extrato de uma conta por vez."). | | **não**: nenhum erro encenado (regra da trilha). Cabe numa dica só se sobrar tempo. |

Contagem: **27 lacunas** (6 de novidade, 11 da tela das contas, 10 da conciliação); 9 valem capítulo ou trecho, 8 valem uma
frase, 10 ficam de fora (5 delas por serem de outra aula).

## 3. Proposta

Quatro blocos sem decisão (P1, P2, P3, P5) e dois que dependem do Kaik (P4 e P6). Tom do roteiro: Rafael, "a gente",
"Uma dica:", sem erro encenado.

### P1 · cap01, trechos (o histórico, o Extrato e as contas por usuário)

| Onde | Tela | Fala |
| --- | --- | --- |
| Troca a linha do histórico | Desce até "Histórico de Movimentações"; a câmera passa pelo botão "Selecionar lançamentos", pelo período "Este mês" e pela busca "Buscar por descrição ou valor...". | Embaixo, o histórico do mês. Dá pra trocar o período, buscar por descrição ou valor e, no Selecionar lançamentos, mexer em vários de uma vez. A gente usa ele daqui a pouco. |
| Linha nova, logo depois | Clique numa linha de Pix de compra: ela abre para baixo com os itens do pedido e a forma de pagamento; clique de novo e fecha. A câmera passa pelo olho do cartão azul. | Linha que veio de pedido abre e mostra os itens. E o olho, aqui em cima, esconde os valores quando tem gente por perto. |
| Linha nova | Clique em "Extrato": janela "Exportar Extrato Bancário", com "Formato" ("PDF" e "Excel") e "Período" em "Este mês"; abre a lista do período ("Mês passado", "Personalizado"); fecha a janela (Esc) sem gerar. [ZOOM: "Formato" e "Período"] | O Extrato gera o movimento da conta em PDF ou em Excel, no período que você escolher. É o arquivo pra mandar pro contador ou guardar no fechamento. |
| Linha nova, antes das abas | A câmera volta à lista lateral das contas. | Um detalhe: em Usuários e Permissões, o administrador pode liberar só algumas contas pra uma pessoa. Quem tem essa restrição só enxerga aqui as contas liberadas. O cofre e os cartões não mudam. |

Mundo: nada novo (a janela do Extrato fecha sem gerar arquivo; a linha de pedido já existe na `inicio`). [BACKEND:
conferir o handler de `purchases` com `purchase_items(materials)` que o detalhe da linha consulta, `BTC:842-850`.]

### P2 · capítulo novo "Corrigir e excluir lançamentos" (vinheta: MOVIMENTAÇÕES), depois do cap04

Semente própria `lote` = `apos-cap04` + três despesas avulsas de teste na Conta Principal, de 10/11: "Internet do
pátio (teste)" R$ 149,90, "Seguro da picape (teste)" R$ 312,40 e "Rastreador (teste)" R$ 89,90 (categoria "Outras
Despesas"; soma R$ 552,20). Com elas a Conta Principal abre o capítulo em R$ 44.684,77 e termina em R$ 45.236,97, o
saldo do `apos-cap04`. **O estado não segue adiante** (o cap05 continua abrindo em `apos-cap04`, como já faz o cap13).

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `lote`), "Conta Principal". A câmera desce ao histórico: três linhas de hoje com "(teste)" na descrição. | Ontem, treinando a equipe, o Rafael lançou três despesas de teste na Conta Principal. Elas não existem de verdade, e o saldo ficou menor do que devia. |
| Na linha "Rastreador (teste)", clique nos três pontinhos ("Ações do lançamento"): o menu com "Editar" e "Excluir". | Todo lançamento feito à mão tem esses três pontinhos, com Editar e Excluir. |
| Clique em "Editar": janela "Editar lançamento", com "Valor (R$)" e "Conta"; a câmera passa pelos dois campos; clique em "Cancelar". [ZOOM: "Valor (R$)" e "Conta"] | O Editar corrige o valor ou a conta. Digitou cento e cinquenta no lugar de quinze, ou lançou na conta errada? É aqui. |
| A câmera passa pelo ícone de setas no fim da linha ("Transferir para outra conta"), sem clicar. | Esse ícone do lado faz só a troca de conta, num clique. |
| Nos três pontinhos, clique em "Excluir": janela "Excluir lançamento?", "Rastreador (teste) será removido e o saldo da conta Conta Principal será ajustado em R$ 89,90." e "Essa ação não pode ser desfeita."; clique em "Cancelar". [ZOOM: o texto da janela] | O Excluir apaga o lançamento e devolve o valor pro saldo. Dá pra fazer um por um. Mas são três, então vamos de uma vez. |
| Na busca "Buscar por descrição ou valor..." digita "teste": ficam as três linhas. | Primeiro eu filtro: busco por teste, e ficam só as três. |
| Clique em "Selecionar lançamentos": o botão vira "Cancelar seleção"; aparece a barra "0 lançamentos selecionados" / "Selecione até 100 itens. Lançamentos protegidos não exibem caixa de seleção."; cada linha ganha uma caixa de marcar. [ZOOM: a barra] | Agora, Selecionar lançamentos. Cada linha ganha uma caixinha, e aparece essa barra. Dá pra marcar até cem de uma vez, sempre da mesma conta. |
| Marca a caixa do cabeçalho ("Selecionar lançamentos elegíveis desta página"): a barra mostra "3 lançamentos selecionados" e os botões "Limpar", "Alterar categoria" e "Excluir selecionados". | Marco todas pela caixinha de cima. Três lançamentos selecionados. |
| Clique em "Alterar categoria": janela "Alterar categoria de 3 lançamentos" ("Escolha a categoria que será aplicada ao lote inteiro."), "Despesas selecionadas", "3 no banco · Valores e saldos não mudam." e "Nova categoria (despesa)"; clique em "Cancelar". [ZOOM: "Despesas selecionadas" e "Nova categoria (despesa)"] | Antes de excluir, repara nesse outro botão. O Alterar categoria troca a categoria de todos os marcados de uma vez. É o jeito rápido de arrumar despesa que caiu na categoria errada. Só não mistura entrada com saída no mesmo lote. |
| Clique em "Excluir selecionados": janela "Excluir 3 lançamentos?", "A seleção da conta Conta Principal será excluída em uma única operação. Se qualquer item não puder ser excluído, nenhum lançamento será alterado.", "Entradas selecionadas" R$ 0,00 e "Saídas selecionadas" R$ 552,20. [ZOOM: "Saídas selecionadas" R$ 552,20] | Agora sim, Excluir selecionados. O sistema mostra o total do que vai sair: quinhentos e cinquenta e dois reais e vinte. Confiro antes de confirmar. |
| A câmera desce ao aviso âmbar ("Transferências, câmbios e baixas podem possuir lançamentos relacionados…") e a "Essa ação não pode ser desfeita."; clique em "Excluir selecionados": aviso "3 lançamentos excluídos."; a barra some; o cartão azul sobe para R$ 45.236,97. [ZOOM: o saldo do cartão] [BACKEND: `delete_bank_transactions_batch_atomic` apaga as três e recalcula o saldo] | Excluir. Os três saem juntos, e o saldo da conta volta pro lugar. |
| Limpa a busca: o histórico volta inteiro; clique em "Selecionar lançamentos" de novo: os Pix de compra e de venda ficam sem caixa; clique em "Cancelar seleção". [ZOOM: uma linha de pedido sem caixa ao lado de uma com caixa] | Uma dica: Pix de compra e de venda não tem caixinha, porque pedido se corrige no próprio pedido. E o lote é tudo ou nada: se um dos marcados estiver conciliado ou protegido, o sistema avisa e não apaga nenhum. |

Mundo e backend: a semente `lote`; handler de `delete_bank_transactions_batch_atomic(p_tx_ids uuid[])` (apaga as linhas
e ajusta `bank_accounts.balance`); as consultas que a janela "Excluir lançamento?" faz ao abrir (`bank_transactions`
por `id`, `bill_payments` por `bank_transaction_id`, `DeleteBankMovementDialog.tsx:77-130`) devolvendo vazio; nenhuma
gravação no Editar nem no Alterar categoria (os dois são cancelados). Se o Kaik preferir **aplicar** a categoria de
verdade, trocar o exemplo: dois lançamentos reais em "Outras Despesas" indo para "Tarifas", com o handler de
`update_financial_transaction_categories_batch` (e conferir o reflexo na DRE da T15).

### P3 · cap04, uma linha (a Entrada)

| Onde | Tela | Fala |
| --- | --- | --- |
| Depois do "Salvar" do combustível | Clique em "Nova Movimentação"; a câmera passa por "Entrada" (verde), "Data/hora do lançamento" e "Vincular a fornecedor/cliente (opcional)"; segue para "Transferência". | A Entrada funciona do mesmo jeito, pra dinheiro que chegou sem pedido, como um rendimento. Dá pra acertar a data e a hora do lançamento e, se quiser, vincular a um cliente ou fornecedor. |

### P4 · capítulo novo "O cartão de crédito da empresa" (vinheta: BANCOS), depois do cap02 · depende de decisão

Único lugar desta aula em que o preenchimento inteligente (1.60.8) aparece. Semente `apos-cap02`; o cartão criado
**não segue adiante** (variante própria `cartao`), para não mudar a T15 nem a lista lateral dos capítulos seguintes.

| Tela | Fala |
| --- | --- |
| Capítulo novo. Clique em "Novo Cartão": janela "Novo Cartão de Crédito" ("Cadastre o cartão para lançar despesas e acompanhar as faturas"). | Além das contas, dá pra cadastrar o cartão de crédito da empresa. É no Novo Cartão. |
| "Nome do cartão *" "Cartão Empresa"; "Dia do fechamento *" 25; "Dia do vencimento *" 5; aparece "A fatura que fecha no dia 25 vence no dia 5 do mês seguinte. Compras feitas no dia do fechamento já entram na próxima fatura." [ZOOM: os dois dias e a frase] | O nome, o dia em que a fatura fecha e o dia em que ela vence: fecha no dia vinte e cinco e vence no dia cinco. O sistema já explica em qual fatura cada compra cai. |
| "Limite do cartão" 10.000,00; clique em "Criar Cartão": aviso "Cartão criado"; o cartão entra na lista lateral. [BACKEND: insert em `bank_accounts` com `kind` card, `closing_day`, `due_day`, `credit_limit`] | O limite é opcional: com ele, o sistema mostra quanto ainda dá pra gastar. Criar Cartão. |
| Clique em "Cartão Empresa": o cartão com "Fatura em aberto" R$ 0,00, "Limite total:" e "Disponível:" R$ 10.000,00, "fecha dia 25 · vence dia 5" e os botões "Nova despesa" e "Extrato". | Ele fica separado das contas, com a fatura em aberto e o limite disponível. |
| Clique em "Nova despesa": janela "Nova Despesa"; em "Descrição" digita "Con": aparece "Padrão encontrado: Conserto do pneu da empilhadeira", a linha "Manutenção de máquinas · Pátio · Conta Principal · Pix / Transferência", "Usado 1 vez · última vez em novembro de 2026" e o botão "Preencher". [ZOOM: o padrão e o "Preencher"] [BACKEND: `get_financial_description_suggestions` (`p_context` movement, `p_direction` payable) devolve o conserto do pneu da T13 (`T13/roteiro.md`, cap05: R$ 180,00, "Manutenção de máquinas", "Pátio")] | Compra no cartão é Nova despesa. E repara: comecei a digitar e o sistema lembrou de um lançamento parecido, com a categoria e o centro de custo. |
| Clique em "Preencher": a categoria e o centro de custo entram; "Pagou com" continua em "Cartão Empresa"; embaixo, "Campos preenchidos. Desfazer preenchimento". [ZOOM: "Pagou com" e a frase] | Preencher. Ele completa o que estava vazio e respeita o que eu já escolhi: o pagamento continua no cartão. Quando o campo está livre, ele sugere também a conta e a forma de pagamento mais usadas. |
| "Valor" 180,00; clique em "Confirmar Despesa"; o painel "Faturas" mostra a fatura do mês com o selo "Aberta" e R$ 180,00; "Disponível:" R$ 9.820,00. [BACKEND: a compra em `bank_transactions` do cartão e a fatura do mês] | Cento e oitenta reais, Confirmar Despesa. A compra não sai de conta nenhuma agora: ela entra na fatura. |
| Na fatura, clique em "Pagar Fatura": janela "Pagar Fatura", com o valor, "Data do pagamento *", "Origem do pagamento" em "Conta Principal" e "Este pagamento quita a fatura."; clique em "Cancelar". [ZOOM: "Origem do pagamento" e a frase] | Na hora de pagar, é Pagar Fatura: você escolhe de qual conta sai o dinheiro. Pode pagar tudo ou uma parte, e se errar, o pagamento tem o Estornar. Aqui eu só mostrei. |
| A câmera fica na fatura "Aberta". | Uma dica: a despesa do cartão conta no mês da compra, não no mês em que você paga a fatura. O pagamento só tira o dinheiro da conta. |

A última fala afirma uma regra de DRE: **conferir no código da T15 antes de gravar** (não li o relatório). Mundo:
handler do cartão (`bank_accounts.kind = 'card'`), das faturas e de `get_financial_description_suggestions`; a
"Nova Despesa" com o cartão na origem só funciona com internet (`CreditCardContent.tsx:168-183`).

### P5 · cap09 e cap10, duas linhas (Ajuste e os avisos automáticos)

| Onde | Tela | Fala |
| --- | --- | --- |
| cap09, depois da dica do Funcionário | No menu "Mais ações", o cursor para em "Ajuste" ("Abre o lançamento com a opção de não contar na DRE") e em "Saldo do cliente/fornecedor", sem clicar; fecha o menu (Esc). | O Ajuste abre o mesmo lançamento com a opção de não contar na DRE, pra linha que só acerta saldo. E o Saldo do cliente ou fornecedor é pro acerto de fiado. |
| cap10, última linha | A câmera fica no selo "Casada". | Uma dica: quando muda só a data, ou só uns centavos no mesmo dia, o sistema já mostra o lançamento num aviso, com o botão de casar. A busca fica pra quando mudam a data e o valor juntos, como aqui. |

### P6 · capítulo novo "Outros casos do extrato" (vinheta: CONCILIAÇÃO), depois do cap14 · depende de decisão

Um segundo extrato, pequeno, da **Conta Secundária** (`Extrato_Secundaria_20261101_20261110.ofx`, quatro linhas), para
não mexer nas 17 linhas nem nos números do extrato principal. Não é finalizado e **não segue para a T15**.

| Tela | Fala |
| --- | --- |
| Capítulo novo. Aba "Conciliação"; em "Conta para conciliar" escolhe "Conta Secundária"; "Importar novo extrato", entrega o arquivo, "Importar", "Concluir" (trecho acelerado): quatro linhas pendentes. | Na Conta Secundária, o extrato é pequeno, mas tem quatro casos que aparecem bastante. |
| Linha 1 (Pix enviado a um fornecedor com saldo a receber da empresa): "Mais ações" › "Saldo do cliente/fornecedor": painel "Baixar na conta-corrente"; em "Cliente ou fornecedor *" escolhe o fornecedor; aparece o saldo dele; a "Descrição" vem "Valor Pago a {nome}". [ZOOM: o saldo do parceiro e o botão "Dar baixa de R$ …"] | O primeiro é acerto de fiado: a empresa comprou no saldo e pagou uma parte depois, por Pix. É em Mais ações, Saldo do cliente ou fornecedor. Escolho o fornecedor, e o sistema mostra quanto a empresa deve a ele. |
| Clique em "Dar baixa de R$ …": selo da linha resolvida. [BACKEND: a RPC do pagamento de saldo pela conciliação] | Dar baixa. Não precisa bater com o pedido: cada Pix abate o valor dele, até zerar a dívida. |
| Linha 2 (Pix recebido que pagou duas vendas): "Mais ações" › "Casar com vários lançamentos" ("Um Pix que pagou dois pedidos, por exemplo"); marca as duas vendas; o botão vira "Casar com 2 lançamentos"; clique. [ZOOM: as duas vendas marcadas e a soma] | O segundo: um Pix só pagou duas vendas. Em Casar com vários lançamentos, marco as duas. Quando a soma fecha com a linha, o botão libera. |
| Linhas 3 e 4 (o banco dividiu em duas um pagamento que no sistema é um lançamento só): marca as duas caixas; na barra, "Soma:" e "Casar 2 linhas com um lançamento"; clique: janela "Casar 2 linhas com um lançamento"; escolhe o lançamento; "Casar 2 linhas". [ZOOM: "Soma:" e o botão] | O terceiro é o contrário: o banco mostra duas linhas, e no sistema é um lançamento só. Marco as duas, confiro a soma, e Casar duas linhas com um lançamento. |
| (ilustração ou câmera parada na tabela) | E quando o Pix foi lançado na conta errada, o sistema avisa na própria linha: achamos este lançamento em outra conta. Um botão move o lançamento pra conta certa e já casa. |
| A câmera passa por "Criar receita" numa linha de entrada, sem clicar; clique em "Voltar". | Entrada que não existe no sistema, como um rendimento, é Criar receita, igual à tarifa que a gente criou. O resto segue como no extrato anterior. |

Mundo: o segundo OFX (tem de passar no `parseOfx` real); um fornecedor com saldo a pagar e um Pix parcial dele na
Conta Secundária; duas vendas por Pix na Conta Secundária pagas num Pix só; um lançamento único que o banco partiu em
dois; handlers de `reconcile_search_candidates` para o modo de vários, da RPC de casar em grupo e da de baixa no saldo
(nomes em `hooks/useBankReconciliation.ts`, não mudaram). O bloco "em outra conta" fica só falado: mostrá-lo de verdade
pede um quinto caso e o handler de `reconcile_find_in_other_accounts`. **Os nomes e os valores saem da junção**
(`MUNDO_LINHA_DO_TEMPO.md`); não inventei número aqui para não bater com a T4, a T7 e a T13.

### Recapitulando (cap15)

| Tela | Fala |
| --- | --- |
| Montagem nova: a barra "3 lançamentos selecionados" e a janela "Excluir 3 lançamentos?" (P2). | Corrigiu e excluiu lançamentos, um por um e vários de uma vez. |
| Só com P4 e P6: o cartão "Cartão Empresa" e a janela "Casar 2 linhas com um lançamento". | Cadastrou o cartão de crédito e resolveu o acerto de fiado e os casos de vários lançamentos. |

Ordem proposta: 00 · 01 (com P1) · 02 · **03 Cartão de crédito (novo, se aprovado)** · 04 Cofre · 05 Movimentação (com
P3) · **06 Corrigir e excluir lançamentos (novo)** · 07 a 16 = a conciliação de hoje (com P5) · **17 Outros casos do
extrato (novo, se aprovado)** · 18 Recapitulando.

## 4. Estimativa

A 2,6 palavras por segundo, só fala (sem vinheta nem espera):

| Bloco | Fala a mais |
| --- | --- |
| P1 cap01 (histórico, Extrato, contas por usuário; uma linha é troca) | +42 s |
| P2 Corrigir e excluir lançamentos (novo) | +101 s |
| P3 cap04 (Entrada) | +13 s |
| P5 cap09 e cap10 (Ajuste e avisos) | +28 s |
| Recap (uma linha) | +5 s |
| **Sem decisão** | **+189 s, 1 capítulo novo** |
| P4 Cartão de crédito (novo, decisão) | +87 s |
| P6 Outros casos do extrato (novo, decisão) | +72 s |
| Recap (segunda linha) | +6 s |
| **Com tudo** | **+354 s (5,9 min), 3 capítulos novos** |

Vídeo: de ~16,5 min para ~20 min sem as decisões e ~24 min com tudo (mais 1 a 3 vinhetas e os trechos acelerados).

## Depende de decisão

1. **Cartão de crédito (P4)**: entra na T14? Nenhuma aula cobre e o mundo não tem cartão. É também o único jeito de
   mostrar o preenchimento inteligente dentro desta aula; sem o capítulo, a novidade fica só na T6 e na T13.
2. **Outros casos do extrato (P6)**: aceitar um segundo OFX, da Conta Secundária, com dados novos da junção.
3. **Alterar categoria em lote (P2)**: só mostrar e cancelar (proposto) ou aplicar de verdade (mexe na DRE da T15).
4. A regra "despesa do cartão conta no mês da compra" precisa ser conferida no relatório da T15 antes de ir para a voz.
