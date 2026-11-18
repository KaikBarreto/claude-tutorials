# T09 · Pedidos e histórico do caixa · cobertura no 1.60.10

Auditoria só de leitura (18/11/2026). Roteiro escrito no 1.59.154 (`f37573ea0`); app lido no 1.60.10 (`5290be4cd`, em
`/dev/shm/ecoflix-src/src`, caminhos abaixo relativos a essa pasta). Não existe `rec/varredura/t09.txt`: nada aqui foi
visto na tela, tudo vem do código. Caixa do Rafael = **#88** (`propostas_fala.md`), não #87.

**O que mudou de verdade.** Das telas da aula, só três arquivos têm mudança visível: `EditTransactionDialog.tsx` (texto
da janela "Editar Pedido"), `pages/Purchase.tsx` / `pages/Sale.tsx` em modo edição (caixa de destino da edição, 1.60.2;
faixa "Editando pedido"; janela "Trocar fornecedor?") e `CashRegisterPickerDialog.tsx` (opção "Manter no caixa
original"). **Não mudaram** (fora do diff): `pages/CashHistory.tsx`, `pages/HistoricoExclusoes.tsx` e
`components/historico-exclusoes/*`, `OrderDeletionPreviewDialog.tsx`, `ExportOrdersDialog.tsx`,
`OrdersPaymentSummaryCard.tsx`, `DateRangeFilter.tsx`, `PrintModal.tsx`, `RetroactiveDateTimePicker.tsx`,
`CashRegisterTabs.tsx`, `cashMaterialReportHtmlGenerator.ts`, `orders.json`, `caixa.json`. Em `pages/Orders.tsx` e
`pages/Caixa.tsx` a mudança é interna (restrição nova e consultas). Excluir pedido de caixa fechado continua igual
(estorno no caixa de hoje): a escolha de caixa do 1.60.2 vale **só para a edição**.

**Consequência para a história.** O pedido da aula (bateria de 21/10, R$ 744,00, só Pix, caixa #70 fechado do Marcos) é
exatamente o caso que o 1.60.2 resolve sem reabrir: o Rafael é administrador, então a edição abre com "Caixa #70 ·
Original" já escolhido. A dica do cap04 ("o caminho mais tranquilo é reabrir") e o motivo do cap09 ficaram
desatualizados. A nota da versão diz: "sem precisar reabrir e fechar o caixa só para salvar a edição"
(`config/version.ts:47`).

## 1. Mudou no app (por capítulo)

| # | Cap. | No roteiro | No 1.60.10 (texto exato) | Onde |
| --- | --- | --- | --- | --- |
| M1 | 04 (linha 1, zoom e fala) | "Se o pedido for de um caixa já fechado, o acerto do dinheiro é lançado no caixa de hoje e o pedido antigo fica marcado como estornado." | **"Se o caixa original estiver fechado, você poderá mantê-lo quando o pedido não movimentar dinheiro ou escolher um caixa aberto para receber o acerto."** Título, descrição e botões iguais ("Editar Pedido", "O pedido será carregado para edição. Após salvar, o pedido original será substituído.", "Cancelar", "Editar Pedido") | `components/EditTransactionDialog.tsx:218-224` |
| M2 | 04 (linha 2, a dica) e 09 (motivo) | "pra pedido de caixa fechado, o caminho mais tranquilo é reabrir o caixa daquele dia" | Na tela Compra/Venda em edição, com o caixa de origem fechado, aparece **"Caixa de destino da edição:"** + selo do caixa (clicável, aria "Trocar caixa"). Pedido **sem dinheiro** (só Pix e/ou saldo) e caixa do próprio operador, ou usuário que opera todos os caixas: selo **"Caixa #70 · Original"** já escolhido e a legenda **"Sem movimento em dinheiro: você pode manter o caixa original sem alterar o fechamento."** Pedido **com dinheiro**: **"O caixa original está fechado. Como houve movimento em dinheiro, escolha um caixa aberto."** (o selo vem com o caixa aberto do usuário, "Caixa #88 · Você"). Operador sem permissão sobre o caixa de outro: **"O caixa original pertence a outro operador. Escolha um caixa aberto autorizado."** | `pages/Purchase.tsx:2171-2179,2219-2240,4768-4788`; `pages/Sale.tsx:1984,1996,5102-5115`; `components/CurrentCashRegisterBadge.tsx:66-67,112-122` |
| M3 | 04 e 09 (clique no selo, novo) | (não existia) | Janela **"Em qual caixa registrar?"** · "Escolha o caixa onde a operação será registrada.": primeira linha **"Manter no caixa original #70"** · **"Sem movimento em dinheiro; o fechamento não será alterado."** (etiqueta "Atual" na escolhida), depois os caixas abertos: "Caixa #88 · Você" · "Aberto em 11/11/2026 07:10". Sem nenhum: "Nenhum caixa aberto" · "Abra um caixa antes de registrar a operação." | `components/CashRegisterPickerDialog.tsx:45-46,89-128,160-175`; `pages/Purchase.tsx:2234-2240` |
| M4 | 04 (linha 4) e 09 (linha 5) | Só o selo "Editando Compra #N" e "Cancelar Edição" | O selo e o botão continuam. Entra, acima do formulário, a faixa âmbar **"Editando pedido {número} · {fornecedor} · {tabela}"** (sem tabela: "Sem tabela"). A barra de pedidos (abas) some em edição: o achado "#1766 R$ 0,00 Sem fornecedor" do `propostas_fala.md` deixa de existir | `pages/Purchase.tsx:4815-4824,4893-4899`; ver T07 M10 |
| M5 | 09 (linha 5: trocar o fornecedor) | Escolher "Auto Peças Vale Forte" troca direto | Com item na lista, a troca abre **"Trocar fornecedor?"** · "O pedido já tem 1 item lançado. Escolha o que fazer com os preços atuais." · faixa "Depósito Irmãos Siqueira → Auto Peças Vale Forte" · **"Itens que mudam"** "1 de 1" (a Vale Forte tem preço especial de R$ 3,40 na bateria desde 09/11) · **"Total se atualizar"** (R$ 744,00 riscado e R$ 816,00) · botões **"Cancelar"**, **"Só nos próximos"**, **"Atualizar 1 item"**. Para manter R$ 744,00 o robô clica **"Só nos próximos"**. O `[TESTAR]` do roteiro ("o preço continua R$ 3,10") vira este passo | `components/orders/OrderPriceContextChangeDialog.tsx:48-87`; `pages/Purchase.tsx:2482-2502` |
| M6 | 04 (linha 10), 09 (linha 6) | Avisos "Revertendo pedido original...", "Pedido original revertido! Criando pedido editado..." | Iguais com a origem aberta **e** quando se mantém o caixa original fechado (o banco trata como origem aberta: apaga e recria no mesmo caixa, sem selo de estornado). Escolhendo um caixa aberto: "Pedido antigo estornado! Recriando no caixa de hoje..." e o pedido antigo fica com "Estornado em dd/MM". Mantendo o original e pondo dinheiro no pagamento: erro **"Para receber valor em dinheiro, escolha um caixa aberto antes de salvar a edição."** | `pages/Purchase.tsx:2674-2678,2760-2764,2925-2927,2945`; migração `20261116155500_edicao_pedido_escolhe_caixa_compensacao.sql:140-175` |
| M7 | 02 (linha 1) | "de todos os caixas e de todos os operadores" | Verdade para o Rafael. Usuário com a restrição nova **"Ver somente os pedidos que lançar"** vê só os próprios pedidos (lista, resumo e exportação). É da T2: aqui só uma frase (P9) | `config/routes.ts` (restrição `ORDERS_OWN_ONLY`); `pages/Orders.tsx:180-181,757,811,1638` |
| M8 | 06 (PDFs em aba nova) | Comprovante com duas assinaturas e "Operador(a):" | O comprovante segue a escolha nova de assinaturas da empresa (as duas, só a do parceiro ou só a do operador; configuração da T1) e, em pedido que veio de Ticket de Pesagem, mostra "Ticket: {nome}" e "Caixa: {nome}" no lugar de "Operador(a):". Fala igual; os PDFs de `rec/t09/pdfs/` precisam ser gerados de novo no 1.60.10 | `utils/orderReceiptHtmlGenerator.ts:512,1156`; `utils/orderReceiptA4Generator.ts` |
| M9 | 09 (menu da linha no Caixa) | Menu com "Emitir NF-e" | "Emitir NF-e" só aparece com a permissão de emitir NF-e (Rafael, administrador, continua vendo). Não é falado | `components/TransactionHistory.tsx:4367` |

Continua valendo o `propostas_fala.md` (cap04 L10: "Finalizar", não "Finalizar Compra"; ajustes da coluna Tela).

## 2. Falta cobrir

| # | O que é (rótulos do código) | Quando o cliente usa | Vale? |
| --- | --- | --- | --- |
| L1 | **Edição em caixa fechado com escolha do caixa** (M2, M3, M6) | Corrigir compra ou venda antiga sem reabrir o caixa | **Sim, é o centro da mudança** (P1 e P2). A T7 só cita |
| L2 | **Edição de venda**: mesmo fluxo na tela Venda ("Editando Venda #N", "Trocar cliente?") (`pages/Sale.tsx:5102-5131,5208`; `orders.json:81`) | Corrigir venda | **Só citar** (uma frase em P1) |
| L3 | **Exportar**: botão "Exportar" → "Exportar pedidos" → "PDF" / "Excel" → janela "Exportar PDF" · "Escolha quais pedidos serão incluídos no relatório": "Período", "Tipo de Pedido" ("Compras", "Vendas"), "Forma de Pagamento" ("Dinheiro", "PIX / Transferência", "Saldo"), "Detalhamento" · "Detalhar materiais de cada pedido" (só PDF); botão "Exportar PDF" ("Gerando..."); abre "Relatório de Pedidos" em aba nova; avisos "Relatório de pedidos gerado", "Excel gerado", "Nenhum pedido encontrado com os filtros escolhidos"; limite de 1.000 pedidos por relatório (`pages/Orders.tsx:2125-2150,1687,1802,1821-1829,1852`; `components/orders/ExportOrdersDialog.tsx:49-57,197,208-305`) | Mandar a lista do mês para o contador ou para o sócio | **Sim, capítulo novo curto** (P7). O roteiro marcou "fora da aula" e nenhuma outra aula mostra |
| L4 | **Ordenar** pelos cabeçalhos "Data", "N° Pedidos" e "Valor"; itens por página no rodapé (`pages/Orders.tsx:2442-2466`) | Achar o maior pedido do dia, o mais antigo | **Sim, trecho** (P3) |
| L5 | **Coluna Pagamento**: no pagamento misto, a dica mostra cada parte ("Dinheiro: …", "Pix/Transferência: …", "Saldo: …") e a conta; no Pix, o nome da conta (`pages/Orders.tsx:2560-2612`) | Saber em qual conta caiu o Pix | **Sim, trecho** (P3) |
| L6 | **Filtros que o roteiro não abre**: "Conta"; em "Forma de Pagamento", "Com Saldo", "Pagamento Misto", "Não informado"; "Marcar todos" / "Desmarcar todos" | Pedidos pagos por uma conta; pagos no saldo | **Só citar** (P4) |
| L7 | **Aviso de lista cortada**: "Mostrando os N pedidos mais recentes do período (a partir de dd/MM/yyyy). Busque por cliente/fornecedor ou reduza o período pra ver o resto." e, no resumo, "O período escolhido tem mais de 1000 pedidos e este resumo não inclui todos eles. Escolha um período menor para ver o total completo." (`pages/Orders.tsx:2166-2184`; `OrdersPaymentSummaryCard.tsx:419-425`) | "Este ano" em empresa com muito movimento | **Só citar** (P4): o mundo não tem mil pedidos |
| L8 | **Excluir pedido de caixa fechado, ao vivo**: na prévia, "↩ estorno hoje" no lugar de "(apaga)" e o aviso amarelo; ao confirmar, "Pedido estornado" · "O caixa antigo foi preservado e o estorno foi lançado no caixa de hoje." (`OrderDeletionPreviewDialog.tsx:95,115-119`; `pages/Orders.tsx:303-305`) | Apagar pedido antigo duplicado | **Sim, trecho** (P5): abrir a prévia e cancelar. O roteiro só mostra o estornado pronto |
| L9 | **Travas da exclusão**: "Abra o caixa de hoje" · "Para excluir um pedido de um caixa já fechado, o estorno é lançado no caixa de hoje. Abra o caixa primeiro."; "Este lançamento está conciliado. Desfaça a conciliação antes de excluir." (`pages/Orders.tsx:341-347`) | Excluir sem caixa aberto; pedido já conciliado (T14) | **Só citar** (P5) |
| L10 | **Histórico de Exclusões, o resto**: filtros "Período", "Todos os tipos", "Todos os usuários", "Buscar pelo nome do registro..."; clique na linha abre "Quem", "Onde" ("IP: …") e os dados do registro apagado ("Número", "Total", "Pagamento") (`AuditFiltersBar.tsx:86-164`; `AuditEventDetails.tsx:47-54,146-155`) | Apurar quem apagou o quê | **Sim, trecho** (P5) |
| L11 | **Resto do menu "⋮"**: "Ver fotos anexadas" (abre a linha; agora também mostra PDF anexado, `OrderAttachmentsGallery.tsx:37`), "Enviar pelo WhatsApp" (sem o módulo: janela "Enviar pelo WhatsApp" · "Para enviar o pedido pelo WhatsApp com o link do portal, você precisa do módulo Portal do Cliente."), "Imprimir direto" (EcoTray) (`pages/Orders.tsx:2670-2705,2913-2921`) | Mandar o pedido para o fornecedor; imprimir no balcão | **Só citar** (P6): fotos e WhatsApp são da T20, impressão direta da T5 |
| L12 | **Filtros do Histórico do Caixa** abertos: "Filtros do Histórico", "Aberto por" ("Todos os operadores"), "Período", "Limpar filtros", "Aplicar" (`pages/CashHistory.tsx:175-306`) | Ver só os caixas de um operador no mês | **Sim, trecho** (P8): o roteiro só aponta o botão |
| L13 | "Imprimir direto" nas ações do caixa fechado (EcoTray) | Reimprimir o fechamento na térmica | **Só citar** (P8) |
| L14 | Erros da edição sem caixa: "Escolha em qual caixa aberto lançar a edição.", "Não há caixa aberto disponível para lançar a edição.", "Carregando as opções de caixa. Tente novamente em instantes." (`pages/Purchase.tsx:4603-4612`) | Editar pedido com dinheiro sem nenhum caixa aberto | **Só citar** (frase em P1) |
| L15 | Celular (ordenação por lista, cartões), "Emitir NF-e" no menu do Caixa | | **Não**: aula é desktop; NF-e é da T16 |

## 3. Proposta

Tom da aula mantido. Linhas numeradas pela tabela do `roteiro.md`.

### P1 · cap04 "Editar um pedido": trocar as 3 primeiras linhas (a bateria se resolve aqui)

| Tela | Fala |
| --- | --- |
| No "⋮" da compra de 21/10, "Editar": janela "Editar Pedido". [ZOOM: "Se o caixa original estiver fechado, você poderá mantê-lo quando o pedido não movimentar dinheiro ou escolher um caixa aberto para receber o acerto."] | Achado o pedido, vem a correção. Em Editar, a janela avisa o que acontece quando o caixa do pedido já fechou: sem dinheiro no meio, dá pra manter o caixa original. Com dinheiro, você escolhe um caixa aberto pra receber o acerto. |
| Clique em "Editar Pedido": tela "Compra" com a faixa "Editando pedido … · Depósito Irmãos Siqueira · …" e o selo "Editando Compra #N". [ZOOM: "Caixa de destino da edição:" com o selo "Caixa #70 · Original" e a legenda "Sem movimento em dinheiro: você pode manter o caixa original sem alterar o fechamento."] | A bateria foi paga no Pix, e o caixa dela, o setenta, do Marcos, fechou em vinte e um de outubro. Como não teve dinheiro, o sistema já propõe manter o caixa original, sem mexer no fechamento daquele dia. |
| Clique no selo: janela "Em qual caixa registrar?" com "Manter no caixa original #70" ("Sem movimento em dinheiro; o fechamento não será alterado.", etiqueta "Atual") e "Caixa #88 · Você"; fecha sem trocar. | Clicando no selo, aparecem as opções: manter no caixa original ou lançar num caixa aberto, aqui o meu de hoje. Eu deixo no original. |
| Em "Fornecedor", clique em "Depósito Irmãos Siqueira": "Selecionar Fornecedor", digita "Vale Forte", escolhe "Auto Peças Vale Forte": janela "Trocar fornecedor?" ("O pedido já tem 1 item lançado. Escolha o que fazer com os preços atuais.", "Itens que mudam" "1 de 1", "Total se atualizar"). [ZOOM: os três botões] Clique em "Só nos próximos". [TESTAR: "1 de 1" e R$ 816,00; se a prévia der "0 de 1", a fala da segunda frase sai] | No fornecedor, eu troco pra Auto Peças Vale Forte. O sistema pergunta o que fazer com o preço, porque ela tem preço próprio na bateria. A compra já foi paga, então eu escolho Só nos próximos, e o valor continua setecentos e quarenta e quatro reais. |
| "Finalizar" → "Finalizar Pedido": "Pix/Transferência" na "Conta Principal" → "CONFIRMAR PAGAMENTO": avisos "Revertendo pedido original...", "Pedido original revertido! Criando pedido editado...", "Compra registrada!"; "Imprimir Comprovante" → "Visualizar PDF": o comprovante no nome da Auto Peças Vale Forte, com 21/10/2026. [BACKEND: `revert_consolidated_order_atomic` com `p_compensation_register_id` = #70 (fechado, sem dinheiro) → `reverted_mode` `hard_delete`, `origin_register_closed` false; `create_purchase_atomic` no #70 com a data original] [TESTAR: data 21/10 no comprovante] | Finalizar, Pix na conta principal, Confirmar pagamento. O comprovante já sai certo, no nome da Auto Peças, com a data de vinte e um de outubro. É esse que a gente manda pra ela. |
| Volta a "Pedidos" ("Mês passado", filtros do cap03): a linha de 21/10 com "Auto Peças Vale Forte", sem selo de estornado. Depois, no "⋮" da compra em dinheiro de 21/10 09:15 (R$ 187,50), "Editar" → "Editar Pedido": [ZOOM: "Caixa de destino da edição:" com "Caixa #88 · Você" e "O caixa original está fechado. Como houve movimento em dinheiro, escolha um caixa aberto."] | O pedido continua no caixa de vinte e um de outubro, e nada de estorno. Agora olha esta outra compra do mesmo dia, paga em dinheiro. Aqui o caixa original não é opção: o acerto precisa ir pra um caixa aberto, e o pedido antigo fica marcado como estornado. |
| Clique em "Cancelar Edição"; volta a "Pedidos"; período "Hoje"; "Limpar todos". | Uma dica: se a correção de um pedido em dinheiro precisa ficar no caixa daquele dia, reabra o caixa, corrija lá dentro e feche de novo. A gente faz isso no fim do tutorial. E tudo isso vale igual pra venda. [pause] Agora, o que é de hoje. Lembra da latinha da Aparecida? Ela trouxe quarenta e dois quilos, não vinte e quatro. |

As linhas 4 a 11 do cap04 (latinha, ilustração "não soma por cima", dica final) ficam como estão, com M4 na coluna Tela.
Saem ~95 palavras antigas, entram ~290: **+~195 palavras, ~75 s**.

### P2 · cap09 "Reabrir um caixa antigo": novo motivo (depende de decisão 1)

Com a bateria resolvida no cap04, a reabertura passa a corrigir a compra **em dinheiro** de 21/10 09:15, que na semente
da T9 fica em **"Não informado"** e é passada para "Aparecida Ramos" (valor e estoque não mudam; o #70 fecha de novo com
R$ 612,50). Mecânica do capítulo igual; mudam estas falas:

| Linha | Tela | Fala nova |
| --- | --- | --- |
| 1 | igual | Agora aquela compra em dinheiro de vinte e um de outubro. Ela saiu sem fornecedor, e eu quero corrigir sem tirar ela do caixa daquele dia. Então, nas ações do caixa, Reabrir caixa. |
| 4 | a compra "Não informado", R$ 187,50, no "Histórico de Transações" do #70 | Em cima aparece a aba do caixa do Marcos, de vinte e um de outubro, do lado do meu de hoje. Dentro dele está a compra em dinheiro, sem fornecedor. |
| 5 | "Editar" → "Editar Pedido": tela "Compra" **sem** "Caixa de destino da edição:"; "Fornecedor" → "Aparecida Ramos" → "Trocar fornecedor?" → "Só nos próximos". [ZOOM: "Fornecedor" e os dois itens, R$ 187,50] | Editar. Com o caixa aberto de novo, a edição é normal, sem escolher caixa de destino. No fornecedor, eu escolho a Aparecida, e nos preços, Só nos próximos. O valor fica igual: cento e oitenta e sete reais e cinquenta. |
| 6 | "Finalizar" → "Dinheiro" → "CONFIRMAR PAGAMENTO" → "Imprimir Comprovante" → "Não, obrigado" | Finalizar, em dinheiro, Confirmar pagamento. |

Linhas 2, 3 e 7 a 12 iguais (a de "seiscentos e doze e cinquenta" continua verdadeira). **+~15 palavras, ~6 s.**
Recap (cap10): linha 2 vira "Corrigiu o fornecedor da bateria direto na edição, mantendo o caixa original, e o peso da
latinha da Aparecida, sem duplicar estoque nem caixa."; linha 6 vira "E reabriu o caixa de vinte e um de outubro pra
corrigir uma compra em dinheiro lá dentro, e fechou de novo." (+~15 palavras, ~6 s). Ilustração do cap09 ("reabrir ×
corrigir por cima") ganha a terceira saída: "sem dinheiro: mantém o caixa original".

### P3 · cap02: ordenar e a coluna Pagamento (depois da linha 3)

| Tela | Fala |
| --- | --- |
| Clique no cabeçalho "Valor": a lista ordena do maior para o menor; clique de novo em "Data" para voltar. Câmera no rodapé (itens por página). | Clicando em Data, no número do pedido ou em Valor, a lista muda de ordem. E no rodapé você escolhe quantos pedidos aparecem por página. |
| O cursor para na coluna "Pagamento" de uma compra em Pix: a dica mostra "Conta Principal". | Na coluna Pagamento, passando o mouse num Pix, aparece em qual conta ele caiu. Num pagamento misto, aparece quanto foi em cada forma. |

~55 palavras, ~21 s. A dica é do próprio app (Radix), aparece na gravação.

### P4 · cap03: frases no fim (filtros restantes e lista cortada)

| Tela | Fala |
| --- | --- |
| Abre "Filtros" de novo; câmera em "Forma de Pagamento" (lista aberta: "Com Saldo", "Pagamento Misto", "Não informado", "Marcar todos") e em "Conta"; fecha. | Os outros filtros seguem a mesma ideia: pagos com saldo, pagamento misto, ou por uma conta bancária específica. |
| (câmera no período) | Uma dica: num período muito longo, com mais de mil pedidos, a tela mostra os mais recentes e avisa. Aí é só buscar pelo nome ou reduzir o período. |

~45 palavras, ~17 s.

### P5 · cap05: prévia em caixa fechado, travas e o detalhe do Histórico de Exclusões

| Tela | Fala |
| --- | --- |
| (depois da linha 5) No "⋮" de uma compra de outubro paga em dinheiro, "Excluir": na prévia, "Financeiro" com "↩ estorno hoje" e o aviso amarelo. [ZOOM: "↩ estorno hoje"] Clique em "Cancelar". | Dá pra ver isso antes de confirmar. Nesta compra antiga, a prévia mostra estorno hoje no lugar de apaga. Eu só quis mostrar, então cancelo. |
| (câmera na lista) | Uma dica: pra excluir pedido de caixa fechado, você precisa estar com um caixa aberto. E pedido já conciliado no banco só sai depois de desfazer a conciliação. |
| (na última linha, já no "Histórico de Exclusões") Câmera nos filtros "Período", "Todos os tipos", "Todos os usuários" e na busca "Buscar pelo nome do registro..."; clique na linha "Excluiu compra "Valdir Pereira"": abre "Quem", "Onde" e os dados ("Número", "Total", "Pagamento"). | Aqui dá pra filtrar por período, tipo e usuário. E clicando na linha, aparece quem excluiu, de onde, e os dados do pedido que saiu. |

~85 palavras, ~33 s.

### P6 · cap06: frase no fim (resto do menu)

| Tela | Fala |
| --- | --- |
| Abre o "⋮" da compra da Aparecida; câmera em "Ver fotos anexadas", "Enviar pelo WhatsApp" e "Imprimir direto"; fecha. | O menu ainda tem as fotos anexadas e o envio pelo WhatsApp, que fazem parte do Portal do Cliente, e o Imprimir direto, pra quem usa a impressora térmica com o EcoTray. |

~35 palavras, ~13 s. Só aparece "Imprimir direto" se o mundo tiver EcoTray com impressão direta; sem ele, a fala cita só os dois primeiros.

### P7 · capítulo novo "Exportar a lista" (vinheta: COMPROVANTES, depois do cap06)

| Tela | Fala |
| --- | --- |
| `/pedidos` com "Mês passado"; clique em "Exportar": "Exportar pedidos" com "PDF" e "Excel"; clique em "PDF". | Além do comprovante de um pedido, dá pra tirar a lista inteira. Em Exportar, você escolhe PDF ou Excel. |
| Janela "Exportar PDF" ("Escolha quais pedidos serão incluídos no relatório"): "Período" já em "Mês passado"; em "Tipo de Pedido", desmarca "Vendas"; "Forma de Pagamento" com "Dinheiro", "PIX / Transferência" e "Saldo" marcados. | A janela já vem com o período da tela. Eu deixo só as compras de outubro, em todas as formas de pagamento. |
| [ZOOM: "Detalhamento" · "Detalhar materiais de cada pedido"] marca a caixa. | No PDF, dá pra detalhar: embaixo de cada pedido saem os materiais, com peso, preço e total. |
| Clique em "Exportar PDF" ("Gerando..."): abre a aba nova "Relatório de Pedidos"; aviso "Relatório de pedidos gerado". [ZOOM: o cabeçalho com o período e duas linhas com os materiais] | Exportar, e o relatório abre numa aba nova, pronto pra imprimir ou mandar pro contador. No Excel, sai a planilha com uma linha por pedido. |

~90 palavras, ~35 s. O relatório entra na edição como ilustração (aba nova), igual aos PDFs do cap06.

### P8 · cap07 e cap08: filtros abertos e a impressão direta

| Tela | Fala |
| --- | --- |
| (cap07, última linha, no lugar de só apontar) Clique em "Filtros": "Filtros do Histórico"; em "Aberto por" escolhe "Marcos Antunes"; "Período" "Mês passado"; "Aplicar": só os caixas do Marcos de outubro; depois "Limpar filtros". | Em Filtros, eu escolho quem abriu o caixa e o período. Aplicar, e ficam só os caixas do Marcos em outubro. Limpar filtros volta tudo. |
| (cap08, última linha, acrescenta) câmera no item "Imprimir direto", se existir. | E com o EcoTray, o Imprimir direto manda o fechamento pra impressora térmica. |

Troca ~20 palavras por ~40: **+~20 palavras, ~8 s**.

### P9 · cap02, linha 1: acréscimo de uma frase

Fala: "Se um usuário só enxerga os próprios pedidos, é uma restrição ligada no cadastro dele, que a gente viu em Usuários
e permissões." ~22 palavras, ~8 s. (Só entra se a T2 ganhar o capítulo de restrições, `T02/cobertura_160.md` P4.)

### O que o mundo fictício e o backend falso precisam

- **P1**: `cash_register` #70 legível por id com `status` closed e `opened_by` = Marcos; multi-caixa ligado e Rafael
  administrador (libera "Manter no caixa original"). A janela "Editar Pedido" agora lê **três** tabelas pelo `order_id`:
  `cash_transactions` (`cash_register_id`, `amount`), `bank_transactions` e `balance_movements` (`cash_register_id`). Para a
  bateria: nenhuma linha de dinheiro com valor (ou uma de valor 0) e a linha de banco com `cash_register_id` = #70. Para a
  compra de 09:15: linha de dinheiro de R$ 187,50 no #70. `revert_consolidated_order_atomic` aceitando
  `p_compensation_register_id` = #70 e devolvendo `reverted_mode` `hard_delete` / `origin_register_closed` false;
  `create_purchase_atomic` gravando no #70 fechado com a data de 21/10.
- **P1 e P2 (janela "Trocar fornecedor?")**: preço especial da Vale Forte na bateria (R$ 3,40) visível na prévia; RPC
  `log_order_activity` respondendo vazio; itens gravados com `price_origin_type`, `price_table_id`, `price_table_name`;
  `profiles.preferred_price_table_id` nulo para o Rafael (mesmos itens da T07).
- **P2**: só na semente `inicio` da T9, a compra de 21/10 09:15 do #70 (18 kg de latinha + 138 kg de papelão, R$ 187,50,
  dinheiro) fica com fornecedor "Não informado"; o estado final devolve à Aparecida Ramos (as 14 compras dela na T4 não
  mudam). Atualizar `MUNDO_FICTICIO.md` (linha "Caixas") e `MUNDO_LINHA_DO_TEMPO.md` (seção 9 e a linha do Siqueira:
  a bateria deixa de ser corrigida por reabertura).
- **P5**: `preview_order_deletion` em modo compensado para uma compra em dinheiro de outubro (`register_status` closed e
  um texto em `warnings[0]`, que vem do banco: copiar do banco real, não inventar); `destructive_actions_audit` com
  `ip_address`, `user_agent` e o retrato do pedido (número, total, pagamento) na linha do Valdir.
- **P7**: nada novo de dado (as compras de outubro já existem); o relatório é montado no navegador. Robô: capturar a aba
  nova como nos PDFs.
- **P8**: nenhum dado novo. **M8**: gerar de novo os PDFs de `rec/t09/pdfs/`.
- Sementes: `apos-cap04` passa a incluir a bateria já no nome da Auto Peças Vale Forte.

### Handoffs para o time do app (a fala não depende)

- H4: a dica do selo "Estornado em dd/MM" ainda diz "correção lançada no caixa de hoje" (`pages/Orders.tsx:2248,2536`),
  mas no 1.60.2 o acerto da edição vai para o caixa aberto escolhido, que pode não ser o de hoje do usuário.
- H5: textos antigos na edição: "Pedido antigo estornado! Recriando no caixa de hoje..." (`Purchase.tsx:2762`) e "Para
  editar um pedido de um caixa já fechado, o estorno é lançado no caixa de hoje. Abra o caixa primeiro." (`:3665`).
- H1 a H3 do inventário: H3 resolvido pelo texto novo (M1); H1 ("Reabrir Último Caixa?" para caixa antigo) continua.

## 4. Estimativa

| Bloco | Palavras | Fala |
| --- | --- | --- |
| P1 cap04 (edição em caixa fechado, 1.60.2) | +~195 | ~75 s |
| P2 cap09 + recap | +~30 | ~12 s |
| P3 cap02 (ordenar, coluna Pagamento) | ~55 | ~21 s |
| P4 cap03 (filtros restantes, lista cortada) | ~45 | ~17 s |
| P5 cap05 (prévia em caixa fechado, travas, detalhe da auditoria) | ~85 | ~33 s |
| P6 cap06 (resto do menu) | ~35 | ~13 s |
| P7 capítulo novo "Exportar a lista" | ~90 | ~35 s |
| P8 caps. 07 e 08 | +~20 | ~8 s |
| P9 cap02 (restrição, se a T2 cobrir) | ~22 | ~8 s |
| **Total** | **~577** | **~222 s (3,7 min)** |

Capítulos novos: **1** (P7; mais uma vinheta). A fala vai de ~10,9 para ~14,6 min (cerca de 16,5 min de vídeo). Regravar
por causa do app: **cap04** e **cap09** (M1 a M6) e os PDFs do cap06 (M8); os demais só pelos trechos.

## Depende de decisão

1. **cap09 depois do 1.60.2**: (A, recomendado) a bateria se resolve no cap04 mantendo o caixa original, e a reabertura
   corrige uma compra em dinheiro (P2, pede a semente "Não informado"); (B, mais barato) o cap04 só mostra o "Caixa de
   destino da edição:" e cancela, e o cap09 segue reabrindo para a bateria, ensinando o caminho longo onde já existe o
   curto; (C) a reabertura vira só demonstração, sem correção dentro.
2. Exclusão em caixa fechado (P5): só abrir a prévia e cancelar (proposto) ou continuar só com o estornado pronto
   (decisão 1 do `plano.md`).
3. Capítulo "Exportar a lista" (P7): entra, ou fica como uma frase no cap02.
4. P9 depende de a T2 ganhar o capítulo de restrições.
5. "Imprimir direto" (P6, P8): só existe na tela se o mundo da T9 tiver EcoTray com impressão direta.
