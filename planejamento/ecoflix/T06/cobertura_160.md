# T06 · Caixa: abrir, fechar e o cofre · cobertura no 1.60.10

Auditoria só de leitura (18/11/2026). Roteiro escrito no 1.59.154 (`f37573ea0`); app lido no 1.60.10 (`5290be4cd`, em
`/dev/shm/ecoflix-src/src`, caminhos abaixo relativos a essa pasta). A varredura do robô (`rec/varredura/t06.txt`) ainda
não existe: nada aqui foi visto na tela, tudo vem do código.

**O que mudou de verdade: quase nada na tela.** Das telas desta aula, só 7 arquivos têm diff, e nenhum rótulo que o
roteiro mostra mudou. `pages/Caixa.tsx` (+24/−18) trocou uma consulta por uma RPC nova (M1). **Sem diff nenhum**:
`CashRegisterHomePanel`, `CashRegisterTabs`, `cash-movement/*` (Saque e Sangria), `dinheiro/*` (cofre, barra, ajuste),
`NewBankTransactionModal`, `ReopenCashPickerDialog`, `CashClosingPrintModal`, `CashClosingMaterialsAccordion`,
`EditTransactionAmountDialog`, `i18n/locales/pt-BR/caixa.json`, `bank.json`, `useKeyboardShortcuts`, `CommandPalette`.
Os números de linha do `inventario.md` em `Caixa.tsx` andaram **+6 a partir da linha 966** (ex.: aviso do cofre
`:1747-1757`, "Caixa aberto com sucesso!" `:1838`, diálogo de fechar `:3383-3611`); antes disso estão iguais.
O trabalho desta aula é a parte (b): a tela do Caixa tem funções que nenhuma aula da trilha mostra (seção 2).

## 1. Mudou no app (por capítulo)

| # | Cap. | No roteiro / plano | No 1.60.10 (texto exato) | Onde |
| --- | --- | --- | --- | --- |
| M1 | 06 a 11 (todo capítulo com caixa aberto) | Backend falso sem essa RPC (`plano.md`, "Backend falso") | A tela chama a RPC nova **`get_cash_register_other_order_ids`** (`p_company_id`, `p_cash_register_id`, `p_created_since`; devolve linhas `{order_id}`, paginada de 1.000 em 1.000). As consultas de "Total Comprado", "Total Vendido" e de "Compras"/"Vendas" por forma de pagamento (cartões do "Fechar Caixa #85") **só ligam depois que ela responde** (`enabled: ... && otherCaixasOrderIds !== undefined`). Sem o handler, o cap10 fica sem "COMPRAS R$ 492,90". Handler: devolver `[]` com um caixa só e os pedidos do outro caixa com dois abertos | `pages/Caixa.tsx:969-989,1043,1219,1285,1372` |
| M2 | plano, "Backend falso" item 5 | "canal de tempo real `multi-cash-<empresa>` tolerado" | O canal agora se chama **`company-updates:<empresa>:<uuid aleatório>`** (um hook só para todas as telas). O backend falso precisa tolerar esse nome | `hooks/useMultiCashEnabled.tsx:42-44`; `hooks/useCompanyUpdateSubscription.ts:21` |
| M3 | 08 (trecho do Marcos) e 01 (inventário, "Em qual caixa registrar?") | A janela listava todos os caixas abertos | "Em qual caixa registrar?" passou a usar a mesma lista do resto do app: quem não tem "Ver e Operar Todos os Caixas" (com multi-caixa) **só vê o próprio caixa** como destino. Reforça a fala do cap08 ("o Marcos vê só o caixa dele"); o roteiro não mostra a janela, então nada a regravar | `components/CashRegisterPickerDialog.tsx:50`; `hooks/useOpenCashRegisters.ts:79-83` |
| M4 | 11 (linha 1) | "Fechei e lembrei de uma compra que ficou sem lançar. O caminho é reabrir o caixa." | Continua certo para **lançar** o que faltou. Mas para **corrigir** um pedido de caixa fechado a 1.60.2 tirou a necessidade de reabrir: a janela de edição avisa **"Se o caixa original estiver fechado, você poderá mantê-lo quando o pedido não movimentar dinheiro ou escolher um caixa aberto para receber o acerto."** e a tela do pedido mostra **"Caixa de destino da edição:"** com a opção **"Manter no caixa original #N"** ("Sem movimento em dinheiro; o fechamento não será alterado."). A aula não pode deixar a ideia de que toda correção pede reabertura: ver P8 (a demonstração é da T9) | `components/EditTransactionDialog.tsx:224`; `pages/Purchase.tsx:2237,4772` |
| M5 | 09 (linha da dica "nunca lance um saque como Nova Receita") | As janelas "Nova Despesa" e "Nova Receita" eram só citadas | As duas ganharam o **preenchimento inteligente** na "Descrição" (lista "Padrões de preenchimento": **"Padrão encontrado: {descrição}"**, a linha com parceiro · categoria · centro de custo · "Dinheiro (Caixa)" ou a conta · forma, **"Usado N vezes · última vez em {mês de ano}"**, botão **"Preencher"**, depois **"Campos preenchidos. Desfazer preenchimento"**); a "Data/hora do lançamento" subiu para logo depois da descrição; a despesa ganhou **"Observação (opcional)"** ("Ex.: referência, competência, documento ou detalhe interno"). A fala do cap09 não muda; as janelas entram em P1 | `components/financial/FinancialDescriptionField.tsx:131-153`; `components/WithdrawalModal.tsx:971-1001,1221-1232`; `components/DepositModal.tsx:859-891` |
| M6 | 03 e 10 (câmera no "Histórico de Transações") | Menu da linha de pedido com "Emitir NF-e" sempre | "Emitir NF-e" só aparece para quem tem a permissão de emitir NF-e. O Rafael (MASTER) continua vendo; o roteiro não abre esse menu. Avisos de vale mudaram para "Vales/Adiantamentos ..." (T19) | `components/TransactionHistory.tsx:4359-4366` |

Conferido e **igual**: aviso "Abra o caixa antes de realizar compras" e a volta ao `/caixa` (agora em
`pages/Purchase.tsx:2343`); janela "Abrir Caixa" inteira; "⚠️ Saldo insuficiente em dinheiro" e os dois botões; cartões
"Dinheiro em Caixa" e "Saldo Bancário"; abas e o "?"; "Saque / Sangria" (inclusive o "Diminuirá em R$ 3006,50" sem
milhar, H2); "Nova Movimentação Financeira"; "Fechar Caixa #N"; "Imprimir Relatório"; reabertura.

## 2. Falta cobrir

| # | Função (texto do código) | Quando o cliente usa | Vale? |
| --- | --- | --- | --- |
| L1 | **"Nova Despesa"** (botão do caixa, permissão "Registrar Despesa"): janela "Nova Despesa" · "Informe o valor e motivo da despesa", blocos "O que é" ("Descrição" com o preenchimento inteligente, "Data/hora do lançamento", "Valor *", "Categoria *" com busca e "Criar categoria", "Cliente / Fornecedor", "Centro de custo"), "Dinheiro" ("Pagou com": grupos "Dinheiro" › "Dinheiro (Caixa)", "Contas", "Cartões"), "Mais detalhes" ("Observação (opcional)", anexos, "Não contar na DRE (saldo herdado / histórico)"), "Parcelar ou repetir"; "Confirmar Despesa" → "Retirada realizada com sucesso!" (`WithdrawalModal.tsx:957-1420`; `caixa.json` `withdrawalModal.*`, `messages.withdrawalSuccess`) | Gás, almoço, frete, conserto: toda saída do dia que não é compra de sucata | **Sim, capítulo** (P1). Nenhuma aula da trilha abre essa janela (a T13 mostra só "Parcelar ou repetir" na conta a pagar; a T7 só cita o botão) |
| L2 | **"Nova Receita"** (permissão "Registrar Receita"): "Nova Receita" · "Informe o valor e motivo da receita", mesmos blocos, "Recebeu em", "Confirmar Receita" → "Depósito realizado com sucesso!" (`DepositModal.tsx`; `caixa.json` `depositModal.*`) | Entrada que não é venda de sucata (aluguel de caçamba, serviço) | **Sim**, no mesmo capítulo (P1). A dica "saque não é receita" ganha a tela |
| L3 | **Despesa no cartão de crédito**: "Compra no cartão **não sai do caixa nem da conta bancária** — ela entra na fatura ... e some do fechamento de caixa."; "Parcelar no cartão"; sem internet: "Sem conexão: cartão de crédito fica indisponível ..." (`WithdrawalModal.tsx:1158-1200,1296-1330`) | Quem paga despesa no cartão da empresa | **Só citar** em P1 se o mundo tiver cartão; cartão e fatura são da T14/T13. Sem cartão no mundo, o grupo "Cartões" nem aparece: não falar |
| L4 | **"Editar saldo de abertura"** (três pontinhos da linha "Abertura" do histórico, com "Editar e Excluir Pedidos"): "Editar Saldo de Abertura" · "Ajuste o valor com que o caixa foi aberto. O Dinheiro em Caixa atual será ajustado proporcionalmente." · "Saldo de Abertura Atual" · "Novo Saldo de Abertura" · "**Atenção:** alterar o saldo de abertura ajusta o Dinheiro em Caixa atual no mesmo valor da diferença. Esta alteração fica registrada na auditoria do caixa." · "Confirmar Alteração" → "Saldo de abertura atualizado com sucesso!" (`TransactionHistory.tsx:4383-4396,4421`; `EditTransactionAmountDialog.tsx:1033,1181-1207,1418-1424`) | Digitou errado na abertura (o erro que o cap02 ensina a evitar) | **Sim, trecho** no cap03 (P2). É a saída do erro mais comum e ninguém mostra |
| L5 | **Data retroativa** na abertura e no fechamento: "Data e Hora de Abertura" · "Altere para abrir o caixa com data/hora retroativa"; "Data/hora do fechamento" · "Altere para fechar o caixa com data/hora retroativa" (permissão "Realizar lançamentos e abrir/fechar caixas com data retroativa") (`Caixa.tsx:3369-3377,3601-3608`) | Esqueceu de abrir ou de fechar no sistema no dia certo | **Sim, trecho** (P3): o campo já está na câmera do cap02 e ninguém explica |
| L6 | **Sangria confirmada**: "Origem da sangria" ("Cofre (Conta DINHEIRO)" ou "Caixa de {operador}", cada um com o saldo), "Conta de destino", "Valor da Sangria", "Data/hora do lançamento", "Descrição (Opcional)" ("Ex: Depósito do cofre na conta corrente"), "Efeitos desta transação:" ("Caixa selecionado" / "Diminuirá em R$ X"; "Conta Bancária de destino" / "Aumentará em R$ X"), "Confirmar Sangria" → "Sangria realizada com sucesso!" (`cash-movement/SangriaForm.tsx:420-590,327`) | Tirar dinheiro da gaveta no meio ou no fim do dia e depositar | **Sim, trecho** (P4). O título do capítulo é "Saque e sangria" e a sangria só aparece de relance, sem preencher; a T14 também não confirma nenhuma |
| L7 | **Saque que vai para o cofre com caixa aberto**: "Atenção: este saque vai para o Cofre" · "Existem 2 caixas abertos (...). Este saque de R$ X entra no Cofre (Conta DINHEIRO), **não no caixa** — o dinheiro não vai aparecer no caixa do operador. Confirma?" · "Voltar e escolher o caixa" / "Mandar pro Cofre mesmo assim" (`cash-movement/WithdrawalForm.tsx:857-887`) | Errou o destino do saque | **Só citar** (uma frase em P4) |
| L8 | **"Data/hora do lançamento"** no saque e na sangria (com a permissão retroativa) (`WithdrawalForm.tsx`, `SangriaForm.tsx:520-524`) | Sangria de ontem que ficou sem lançar | **Só citar** (frase em P4) |
| L9 | **Trava do "Fechar Caixa" na tela**: painel "Pedidos Não Finalizados" (contador laranja, colunas "Compras"/"Vendas", cada pedido com parceiro, itens, kg, valor e quem criou; clicar abre o pedido); cadeado no botão com a dica "Finalize ou cancele antes de fechar o caixa:" + lista; clique no botão travado: "Não é possível fechar o caixa com pedidos não finalizados" com a lista (`components/UnfinishedOrdersTabs.tsx:183-190`; `Caixa.tsx:2325,2692-2716`) | Fim do dia com pedido esquecido | **Sim, trecho** (P5): hoje o cap10 fala do cadeado sem mostrar. O painel e o descartar pedido são da T7 (auditoria da T07, L5 e 3.2): aqui só a trava |
| L10 | **Fechamento com diferença, na tela**: "Diferença detectada: −R$ X" (vermelho) ou "+R$ X" (verde), a borda âmbar do campo, a chave "Registrar diferença no DRE" com o texto que muda entre falta ("...conta como Prejuízo (despesa)...") e sobra ("...conta como Ganho (receita)..."); a escolha da chave fica gravada no navegador; o acerto do cofre sai como "Ajuste de saldo — Diferença de fechamento do ..." e, com a chave, vai para a categoria "Prejuízos" ou "Ganhos" (`Caixa.tsx:3546-3585,1997-2002`) | Todo fechamento que não bate | **Sim, trecho** (P6): é o caso de uso central do fechamento e hoje é só falado |
| L11 | **Cartões do fechamento não explicados**: "SAÍDAS" › "Despesas" e "ENTRADAS" › "Vendas" e "Receitas", cada um com "Dinheiro:", "PIX/Transf." e "Saldo:"; o detalhamento "Projeção de Lucro" por material (colunas "Material", "Comprado (kg)", "Valor Compra", "Vendido (kg)", "Valor Venda", "Total") (`Caixa.tsx:3405-3505`; `CashClosingMaterialsAccordion.tsx:218,263-286`) | Conferir o dia antes de confirmar | **Sim, trecho** (P6): a câmera já passa por eles |
| L12 | **"Ver comprovante"** e "Imprimir" (só com impressão direta) na janela "Imprimir Relatório" (`CashClosingPrintModal.tsx:17-45`) | Guardar o relatório do fechamento | **Só citar** (frase em P6). O relatório em si é da T9 (cap08) |
| L13 | **"Resumo do Caixa Atual"**: olho "Ocultar valores"/"Mostrar valores", "Total Comprado", "Total Vendido", "Projeção de Lucro" (com "Margem de Lucro" e "Markup" e as explicações), "Receitas", "Despesas" (`Caixa.tsx:3067-3182`) | Dono acompanha o dia sem abrir relatório | **Sim, trecho** (P7). Nenhuma aula mostra (busca na trilha: zero) |
| L14 | **Painel Gerencial, o resto**: seletor de data ("Hoje" ou "dd de MMMM, yyyy", botão "Hoje" para voltar), "Resumo do Dia" com o olho, "Transações do Dia (N)" com selo ("Compra", "Depósito", "Retirada") e o operador, gráficos "Visão Geral", "Compras por Forma", "Vendas por Forma", "Distribuição entre Caixas", "Receitas e Despesas por Caixa" (`CashRegisterHomePanel.tsx:654-679,707-1081`) | Dono com dois ou mais operadores; olhar o dia de ontem | **Sim, trecho** (P7) |
| L15 | **"Saldo de Cliente/Fornecedor"** (menu "Nova movimentação de saldo" › "Cliente" / "Fornecedor" → busca → "Nova Movimentação de Saldo") (`PartnerBalanceQuickAction.tsx:255-290`; `BalancePaymentModal.tsx:470-640`) | Receber fiado ou pagar vale sem sair do caixa | **Só citar** (frase em P7): a janela é da **T4** |
| L16 | **Histórico de Transações, o resto**: "Buscar transação...", "Filtros" ("Tipo", "Forma de pagamento", "Aplicar Filtros"), colunas ("Nº Pedido", "Tipo", "Cliente/Fornecedor", "Valor", "Pagamento", "Saldo Após" nas abas "Dinheiro" e "Pix/Transferência", "Data"), menu da linha ("Ver comprovante", "Ver fotos anexadas", "Enviar pelo WhatsApp", "Imprimir direto", "Emitir NF-e", "Editar", "Excluir") (`TransactionHistory.tsx:3444-3650,4125-4131,4330-4450`) | Achar e corrigir um lançamento do dia | **Só citar** (frase em P2): editar, excluir e reimprimir são da **T9**; NF-e da T16 |
| L17 | **Primeira abertura da vida da empresa**: o cofre nasce com o valor digitado ("Saldo inicial do dinheiro (primeira abertura de caixa)"), aviso "Cofre iniciado com R$ X", sem o bloqueio (`Caixa.tsx:1705-1745,1842-1847`) | Cliente novo no primeiro dia | **Só citar** (frase em P3): o mundo não é empresa nova; gravar pediria outra empresa |
| L18 | **Cofre desligado** ("Rastreabilidade do dinheiro físico (Cofre)" em Configurações › Usabilidade): sem ele o caixa abre com qualquer valor e somem "Disponível no cofre agora" e "Dinheiro total da empresa" | Empresa que não quer o controle | **Não aqui**: a chave é da **T1**; o cap07 já cita Usabilidade para o Multi-Caixas |
| L19 | **Erros de quem já tem caixa**: "{nome} já possui um caixa aberto" (abrir) e "Este operador já possui um caixa aberto" (reabrir) (`Caixa.tsx:1623,837`) | Tentar abrir ou reabrir em dobro | **Só citar**: o cap11 já diz "um caixa aberto por vez"; a lista "Abrir para o usuário" nem mostra quem já tem caixa |
| L20 | **Sem permissão**: cadeado "Você não tem permissão para abrir o caixa" / "... para fechar o caixa" (`Caixa.tsx:2431,2474,2758`) | Operador sem "Abrir Caixa" ou "Fechar Caixa" | **Só citar** (frase em P7). As permissões são da T2 |
| L21 | **Duas moedas**: caixa e cofre por moeda, "Abrir caixa em {símbolo}", "Escolha o cofre (moeda)" (`Caixa.tsx:2620-2630,2730-2745`) | Empresa de fronteira com o módulo | **Não**: o mundo é só em reais e a função fica escondida sem o módulo |
| L22 | **Celular**: botões redondos "Despesa"/"Receita", "Saque/Sangria" e "Movimentação" encurtados, "Travado por: ..." embaixo do botão (`Caixa.tsx:2700-2705,2893-2905,2962-2985`) | Dono no celular | **Não**: a aula é de desktop; nenhuma função é exclusiva do celular |
| L23 | **Ajuda da tela**: o "?" do título "Caixa" (sete itens: "Abrir/Fechar Caixa", "Compras e Vendas", ...) e o "?" do histórico ("Como funcionam as abas:") (`Caixa.tsx:2354-2360`; `TransactionHistory.tsx:3453-3456`) | Dúvida rápida | **Não**: repete a aula |

## 3. Proposta

Ordem nova: 00 · 01 · 02 (+P3) · 03 (+P2) · 04 · 05 · 06 · 07 (+P7) · 08 · 09 (+P4a) · **09b Despesa e receita (P1, novo)** ·
**09c Sangria no fim do dia (P4b, novo)** · 10 (+P5, P6) · 11 (+P8) · 12 (recap com duas linhas novas). Fala sempre do Rafael.

### P1 · cap09b · Despesa e receita do dia (vinheta: MOVIMENTAÇÕES) · capítulo novo

Semente `apos-cap09`, aba "#85 | Caixa - Rafael Nogueira (você)", 08:5x.

| Tela | Fala |
| --- | --- |
| Câmera nos botões "NOVA DESPESA" e "NOVA RECEITA". | Nem tudo que sai do caixa é compra de sucata. O gás da empilhadeira, o almoço da equipe, um conserto: isso é despesa, e aqui no caixa ela tem botão próprio. |
| Clique em "Nova Despesa": janela "Nova Despesa" ("Informe o valor e motivo da despesa"), com os blocos "O QUE É", "DINHEIRO", "MAIS DETALHES" e "PARCELAR OU REPETIR". | Nova Despesa. A janela pergunta o que é, de onde sai o dinheiro, e guarda os detalhes mais embaixo. |
| Em "Descrição" o robô digita "Gás da empilhadeira"; a partir da terceira letra abre a lista com "Padrão encontrado: Gás da empilhadeira", "Combustível · Pátio · Dinheiro (Caixa)" e "Usado 4 vezes · última vez em outubro de 2026". [ZOOM: a lista e o botão "Preencher"] | Começo pela descrição, e o sistema reconhece: essa despesa já foi lançada outras vezes. Ele mostra o padrão encontrado, com a categoria, o centro de custo e a forma de pagamento. |
| Clique em "Preencher": "Categoria" fica "Combustível", "Centro de custo" "Pátio", "Pagou com" "Dinheiro (Caixa)"; embaixo, "Campos preenchidos. Desfazer preenchimento". O robô digita "50,00" em "Valor". | Clico em Preencher e os campos vêm prontos. Se não era isso, tem o Desfazer preenchimento logo embaixo. Agora o valor: cinquenta reais. |
| O robô abre a lista "Pagou com": grupo "Dinheiro" com "Dinheiro (Caixa)" e grupo "Contas" com "Conta Principal" e "Conta Secundária"; fecha sem trocar. | Em Pagou com, você diz de onde saiu o dinheiro. Dinheiro, Caixa, sai da gaveta deste caixa. Se você escolher uma conta do banco, a gaveta não muda. |
| Clique em "Mais detalhes": "Observação (opcional)", os anexos e "Não contar na DRE (saldo herdado / histórico)". Câmera desce até "Parcelar ou repetir", sem abrir. | Em Mais detalhes dá pra escrever uma observação e anexar o comprovante. Parcelar e repetir a gente vê no tutorial Contas a Pagar e Receber. |
| Clique em "Confirmar Despesa": aviso "Retirada realizada com sucesso!"; "DINHEIRO EM CAIXA" cai de R$ 1.500,00 para R$ 1.450,00; no "Histórico de Transações", a linha "Despesa", "Gás da empilhadeira", R$ 50,00, "Dinheiro". [ZOOM: o valor do cartão] | Confirmar Despesa. Repara no Dinheiro em Caixa: caiu de mil e quinhentos pra mil quatrocentos e cinquenta. E a despesa já está no histórico. |
| Clique em "Nova Receita": janela "Nova Receita" ("Informe o valor e motivo da receita"); "Descrição": "Aluguel de caçamba" (o padrão aparece; "Preencher": "Categoria" "Aluguel de caçamba", "Recebeu em" "Conta Principal", forma "Pix / Transferência"); "Valor": "120,00". | A Nova Receita é o mesmo caminho, pro dinheiro que entra e não é venda de sucata. Aqui, o aluguel de uma caçamba: cento e vinte reais, recebidos por Pix na conta do banco. |
| Clique em "Confirmar Receita": aviso "Depósito realizado com sucesso!"; "DINHEIRO EM CAIXA" segue R$ 1.450,00 e o "SALDO BANCÁRIO" sobe R$ 120,00. | Confirmar Receita. Como caiu no banco, a gaveta não mudou. |
| Câmera nos dois cartões. | Uma dica: receita é dinheiro novo que a empresa ganhou. Troco que vem do banco pra gaveta não é receita, é saque, como a gente acabou de ver. |

Mundo: categorias "Combustível" (despesa, já existe pela T14) e "Aluguel de caçamba" (receita, já citada na T15); centro
de custo "Pátio"; nenhuma conta do tipo cartão (se a junção tiver cartão, o grupo "Cartões" aparece na lista "Pagou com":
a fala não cita). Handlers: RPC `get_financial_description_suggestions` (`p_context` "movement", `p_direction` "payable" e
"receivable", `p_prefix`, `p_limit` 3) devolvendo uma linha cada (`description`, `category_id`, `category_label`,
`cost_center_id`, `cost_center_name`, `payment_source` = o valor de "Dinheiro (Caixa)" ou o id da Conta Principal,
`payment_method` "cash" / "transfer", `bank_account_name`, `usage_count` 4, `last_used` em outubro); insert de despesa em
`cash_transactions` (dinheiro, com `cash_register_id` do #85) e a entrada bancária da receita; `financial_categories`,
`cost_centers`. A lista só abre com 3 letras ou números e 350 ms de pausa; o "Preencher" não mexe na descrição.

### P2 · cap03 · trecho novo depois da 1ª linha (a linha "Abertura do Caixa #85")

| Tela | Fala |
| --- | --- |
| No fim da linha "Abertura", clique nos três pontinhos ("Abrir ações da movimentação"): item "Editar saldo de abertura"; clique: janela "Editar Saldo de Abertura", com "Saldo de Abertura Atual" R$ 1.500,00 e "Novo Saldo de Abertura". | E se você digitou o valor errado na abertura? Não precisa fechar e abrir de novo. Nos três pontinhos dessa linha tem o Editar saldo de abertura. |
| [ZOOM: "Atenção: alterar o saldo de abertura ajusta o Dinheiro em Caixa atual no mesmo valor da diferença. Esta alteração fica registrada na auditoria do caixa."] Clique em "Cancelar". | Você informa o valor certo, o Dinheiro em Caixa se ajusta pela diferença, e a mudança fica registrada. Aqui está certo, então eu cancelo. |
| A câmera passa pela busca "Buscar transação...", por "Filtros" e pelas abas "Todas", "Dinheiro" e "Pix/Transferência". | Nesse histórico dá pra buscar, filtrar e corrigir cada lançamento do dia. Isso a gente vê no tutorial Pedidos e histórico do caixa. |

Mundo: nada novo (o Rafael já tem "Editar e Excluir Pedidos" por ser MASTER); nada é gravado.

### P3 · cap02 · duas linhas novas antes do clique final em "Abrir Caixa"

| Tela | Fala |
| --- | --- |
| Câmera em "DATA E HORA DE ABERTURA" e em "Altere para abrir o caixa com data/hora retroativa". | Embaixo fica a Data e Hora de Abertura, que já vem com a hora de agora. Ela só aparece pra quem tem a permissão de data retroativa, e serve pro dia em que o caixa ficou sem abrir no sistema. |
| (mesma câmera) | Uma dica: no primeiro caixa da vida da empresa não tem limite. O valor que você digitar é o que inaugura o cofre. |

E no cap10, depois da linha do valor negativo: Tela "Câmera em 'Data/hora do fechamento' e 'Altere para fechar o caixa com
data/hora retroativa'"; Fala "Com a mesma permissão, dá pra fechar com a data e a hora em que o caixa parou de verdade."

### P4 · Sangria de verdade

**P4a · cap09**: as duas linhas da sangria "sem preencher" saem; no lugar, depois de "Confirmar Saque":

| Tela | Fala |
| --- | --- |
| Clique de novo em "Saque / Sangria"; em "Destino do saque" o robô abre a lista e pousa em "Cofre (Conta DINHEIRO)", sem escolher. | Uma dica: se o destino for o cofre e tiver caixa aberto, o sistema pergunta antes de gravar, porque esse dinheiro não aparece na gaveta de ninguém. |
| Câmera em "Data/hora do lançamento"; clique em "Cancelar". | E esqueceu de lançar o saque de ontem? Quem tem a permissão de data retroativa escolhe o dia aqui. |

**P4b · cap09c · Sangria no fim do dia (vinheta: MOVIMENTAÇÕES) · capítulo novo**, semente `apos-cap09` + `dia-10`, 17:30.

| Tela | Fala |
| --- | --- |
| Aba "#86 \| Caixa - Marcos Antunes": "DINHEIRO EM CAIXA" com o valor do fim do dia. | Fim da tarde, e o caixa do Marcos ainda está com muito dinheiro vivo. Dinheiro parado na gaveta é risco. A saída é uma sangria. |
| Clique em "Saque / Sangria" e em "Sangria" ("Transferir dinheiro do cofre ou de um caixa aberto para uma conta bancária"). Em "Origem da sangria" o robô abre a lista ("Cofre (Conta DINHEIRO)", "Caixa de Rafael Nogueira", "Caixa de Marcos Antunes", cada um com o saldo) e escolhe "Caixa de Marcos Antunes". | Em Saque, Sangria, opção Sangria. A origem pode ser o cofre ou um caixa aberto, cada um com o saldo do lado. Escolho o caixa do Marcos. |
| "Conta de destino": "Conta Principal"; "Valor da Sangria": "5.000,00"; "Descrição (Opcional)": "Depósito do fim do dia". [ZOOM: "Valor da Sangria"] | O destino é a conta principal, e o valor, cinco mil reais, que o Marcos vai depositar no banco. |
| Câmera em "Efeitos desta transação:": "Caixa selecionado", "Diminuirá em R$ 5.000,00"; "Conta Bancária de destino", "Aumentará em R$ 5.000,00". | Embaixo, os efeitos: o caixa do Marcos diminui cinco mil, e a conta do banco aumenta cinco mil. |
| Clique em "Confirmar Sangria": aviso "Sangria realizada com sucesso!"; o "DINHEIRO EM CAIXA" do #86 cai R$ 5.000,00. | Confirmar Sangria. Não é despesa: o dinheiro só trocou a gaveta pelo banco. |

Mundo: o #86 chega às 17:30 com o saldo que a junção definir (R$ 20.000,00 se nada mais passar por ele; a fala não diz o
saldo). Handlers: os da sangria (`create_manual_bank_transaction` com a entrada no banco e o espelho do cofre,
`cash_transactions` `transfer` −5.000 no #86, `adjust_cash_register_balance`, `get_dinheiro_balance` com `caixas_abertos`).
Depois dela: cofre total R$ 16.500,00 e Conta Principal +5.000,00 em 10/11 17:3x (conferir T9 e `MUNDO_LINHA_DO_TEMPO.md`).

### P5 · cap10 · a trava na tela (troca as linhas 2 e 3)

Gravada num trecho próprio (`cap10a`, semente `apos-cap09` + `dia-10` + um rascunho de compra no #85: Valdir Pereira,
1 item, cobre, R$ 86,00, criado pelo Rafael), que não segue para a cadeia; o `cap10` continua da semente limpa.

| Tela | Fala |
| --- | --- |
| Aba #85; a câmera desce até "PEDIDOS NÃO FINALIZADOS" com o contador "1" e abre o painel: a compra do Valdir Pereira, "1 item", o peso, R$ 86,00 e "Rafael Nogueira". | Antes de fechar, olha o painel Pedidos Não Finalizados. Ficou uma compra do Valdir pela metade. |
| A câmera sobe ao botão "FECHAR CAIXA" com o cadeado; o mouse para em cima: dica "Finalize ou cancele antes de fechar o caixa:" e o pedido. [ZOOM: o botão e a dica] | Enquanto ela estiver aí, o Fechar Caixa fica com cadeado, e passando o mouse ele diz qual pedido está travando. |
| Clique no pedido do painel: abre a compra; volta. Corte para o `cap10` (botão sem cadeado). | Clicando no pedido, o sistema abre ele pra você finalizar ou descartar. Resolvido isso, o cadeado some. |

Mundo: semente `dia-10-rascunho` (uma linha em `order_drafts` do #85 com `items`, parceiro e criador); a tela `/compra`
precisa abrir o rascunho.

### P6 · cap10 · o fechamento por inteiro (trechos novos; a linha "Se não batesse..." sai)

| Tela | Fala |
| --- | --- |
| (depois do zoom em "RESTANTE EM CAIXA") Câmera em "SAÍDAS" › "DESPESAS" ("Dinheiro: R$ 50,00", "PIX/Transf.: R$ 39,90") e em "ENTRADAS" › "VENDAS" ("PIX/Transf.: R$ 2.000,00") e "RECEITAS" ("PIX/Transf.: R$ 120,00"). | Cada cartão separa o que foi em dinheiro do que foi por Pix ou transferência. Só a coluna do dinheiro mexe na gaveta: as compras e o gás da empilhadeira. |
| Clique em "Projeção de Lucro" (abre a tabela por material: "Material", "Comprado (kg)", "Valor Compra", "Vendido (kg)", "Valor Venda"). | Abrindo a Projeção de Lucro, você confere o dia material por material: quanto comprou e quanto vendeu de cada um. |
| (no lugar de "Se não batesse...") O robô digita "950,00" no "Valor de Fechamento": borda amarela, "Diferença detectada: -R$ 7,10" e a chave "Registrar diferença no DRE". [ZOOM: o aviso e a chave] | Olha o que acontece se eu contar novecentos e cinquenta: o sistema mostra a diferença, sete reais e dez centavos a menos. |
| (zoom continua em "...essa falta também conta como Prejuízo (despesa) no resultado da empresa.") | A chave Registrar diferença no DRE decide se essa falta entra no resultado como prejuízo. Se fosse sobra, entraria como ganho. O cofre fica sempre com o valor que você contou. |
| O robô corrige para "957,10": o aviso some. | Contei de novo, e tinha uma nota dobrada: novecentos e cinquenta e sete e dez. Bateu. |
| (na janela "Imprimir Relatório") Câmera em "Ver comprovante". | Em Ver comprovante, o relatório abre na tela pra salvar ou mandar pro dono. |

Com P1 gravado na cadeia o esperado do dia passa a **R$ 957,10** (1.500,00 − 492,90 − 50,00). Sem P1 na cadeia, os
números desta tabela voltam a 1.007,10 e a diferença de exemplo vira "1.000,00" (−R$ 7,10); as linhas das despesas e
receitas mostram só a tarifa de R$ 39,90.

### P7 · cap07 · o painel e o resumo (trechos novos no fim do capítulo)

| Tela | Fala |
| --- | --- |
| Aba "Início"; clique no seletor "Hoje": abre o calendário; o robô escolhe 09/11: "2 caixas encontrados" (#83 e #84) e o "RESUMO DO DIA" de ontem; clique em "Hoje" para voltar. | O painel não mostra só hoje. No calendário, eu escolho ontem e vejo os caixas e o resumo daquele dia. No botão Hoje, eu volto. |
| A câmera desce por "TRANSAÇÕES DO DIA", com o selo e o nome do operador em cada linha, e pelos gráficos "Visão Geral", "Compras por Forma", "Vendas por Forma" e "Distribuição entre Caixas". | Mais embaixo, as transações do dia com o nome de quem lançou, e os gráficos: quanto foi em dinheiro e quanto foi por Pix, e quanto cada caixa movimentou. |
| Clique na aba #85; a câmera desce até "RESUMO DO CAIXA ATUAL": "Total Comprado", "Total Vendido", "Projeção de Lucro", "Receitas" e "Despesas"; clique no olho ("Ocultar valores") e de novo. | Dentro de cada caixa tem o Resumo do Caixa Atual: o que comprou, o que vendeu, a projeção de lucro, as receitas e as despesas só deste caixa. O olhinho esconde os valores, se tiver gente por perto. |
| Câmera no botão "Saldo de Cliente/Fornecedor" do cartão "SALDO BANCÁRIO". | E esse botão lança um recebimento ou um pagamento no saldo de um cliente ou fornecedor, sem sair do caixa. A janela é a mesma do tutorial de clientes e fornecedores. |
| (cap08, depois de "Quem pode ver e operar o caixa dos outros?") Câmera nas abas. | Abrir e fechar caixa também são permissões. Quem não tem vê o botão com um cadeado. |

Mundo: "Resumo do Dia" de 09/11 precisa dos caixas #83 e #84 fechados naquele dia com as transações (compras da T16 no
#83); handlers do painel para data passada (`cash_register` por dia, `cash_transactions`, `purchases`, `sales`).
A "Projeção de Lucro" depende dos preços de venda do mundo: a fala não diz o número.

### P8 · cap11 · uma linha nova depois da primeira

| Tela | Fala |
| --- | --- |
| (cartão amarelo na tela) | Reabrir é pra lançar o que ficou de fora. Pra corrigir uma compra ou venda de um caixa já fechado, não precisa: a edição do pedido deixa manter o caixa original ou escolher um caixa aberto. Isso está no tutorial Pedidos e histórico do caixa. |

### Recap (cap12): duas linhas a mais
"Lançou uma despesa em dinheiro e uma receita no banco, com o preenchimento que o sistema sugere." (montagem: "Padrão
encontrado") e "Fez a sangria do caixa do Marcos e viu a diferença aparecer no fechamento." (montagem: "Efeitos desta
transação:" da sangria e "Diferença detectada").

### Falas atuais que mudam se P1 entrar na cadeia do dia
cap10: "saíram duas compras em dinheiro" → acrescentar "e o gás da empilhadeira"; "saíram quatrocentos e noventa e dois e
noventa em compras, em dinheiro" → "... em compras e cinquenta reais de despesa, em dinheiro"; "mil e sete reais e dez
centavos" e "Contei mil e sete e dez" → "novecentos e cinquenta e sete reais e dez centavos"; Tela: R$ 1.007,10 → R$ 957,10
nos caps 10, 11 e 12 (`rec/cap10.json` a `cap12.json`, `t06_sementes.py`, `cenas/ilustracoes.json` "esperado").

## 4. Estimativa

| Proposta | Fala a mais |
| --- | --- |
| P1 cap09b Despesa e receita (novo) | ~100 s |
| P2 editar saldo de abertura + histórico | ~32 s |
| P3 datas retroativas e primeira abertura | ~28 s |
| P4a dicas do saque (troca 2 linhas) | ~8 s líquidos |
| P4b cap09c Sangria no fim do dia (novo) | ~42 s |
| P5 trava na tela (troca 2 linhas) | ~8 s líquidos |
| P6 fechamento por inteiro | ~45 s líquidos |
| P7 painel, resumo e atalho de saldo | ~62 s |
| P8 + recap | ~22 s |
| **Total** | **~350 s (~5,8 min) de fala; 2 capítulos novos e 1 trecho gravado à parte (`cap10a`)** |

A aula vai de ~14,5 min para ~21 min de vídeo.

## Depende de decisão
1. **P1 dentro ou fora da cadeia do dia.** Dentro (recomendado: o fechamento passa a mostrar a despesa e a receita que o
   aluno viu nascer): o #85 fecha com R$ 957,10, e isso mexe na `MUNDO_LINHA_DO_TEMPO.md` (17:4x), no `MUNDO_FICTICIO.md`
   e na semente da T9 (`T09/rec/t09_sementes.py` cita 1.007,10). Fora: capítulo descartável, nada muda nas outras aulas,
   mas o fechamento do cap10 não mostra a despesa lançada minutos antes.
2. **P4b (sangria de R$ 5.000,00 do #86).** Muda o cofre e a Conta Principal no fim de 10/11; conferir com a T9 (11/11)
   ou gravar descartável.
3. **Tamanho.** São ~6 min a mais numa aula de 14,5 min. Se for demais, a T6 pode virar duas (abrir e cofre · movimentar
   e fechar), cortando no cap08.
4. **H4 continua** (handoff ao time do app): "Nova Receita" sugere "Ex: Suprimento de caixa" no campo da descrição
   (`caixa.json` `depositModal.reasonPlaceholder`), o contrário do que a aula ensina; o P1 põe esse texto na câmera.
