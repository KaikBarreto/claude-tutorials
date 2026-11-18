# T07 · Comprar e vender sucata · cobertura no 1.60.10

Auditoria só de leitura (18/11/2026). Roteiro escrito no 1.59.154 (`f37573ea0`); app lido no 1.60.10 (`5290be4cd`, em
`/dev/shm/ecoflix-src/src`, caminhos abaixo relativos a essa pasta). Varredura do robô (`rec/varredura/t07.txt`) ainda
não existe: nada aqui foi visto na tela, tudo vem do código.

**O que mudou de verdade.** `pages/Purchase.tsx` (+740) e `pages/Sale.tsx` (+667) receberam as MESMAS quatro frentes, uma
espelhada na outra: (1) janela nova ao trocar fornecedor/cliente ou tabela com itens já lançados, (2) legenda de origem
do preço embaixo do Valor/Kg de cada linha, (3) tabela fixada por usuário na ordem da tabela inicial, (4) edição de
pedido de caixa fechado com escolha do caixa de destino (1.60.2). Só a Compra ganhou a conferência do fornecedor na hora
de finalizar. **Não mudaram** (fora do diff): `OrderFormInputs` (cartão Pesagem), `AdvancedWeighingDialog`,
`InputPesoBalanca`, `WeighingDetailRow`, `EditableOrderTotal`, `AdvancedOptionsPopover`, `PrintModal`,
`SaleStockTransferDialog`, `OfflinePendingSyncTabs`, `OrderSwitcher`, `DeletedDraftsDialog`, `CommandPalette`, atalhos.
Em `MultiPaymentDialog` e `Caixa.tsx` a mudança é interna (pesagem avulsa e consultas), sem rótulo novo para esta aula.

## 1. Mudou no app (por capítulo)

| # | Cap. | No roteiro | No 1.60.10 (texto exato) | Onde |
| --- | --- | --- | --- | --- |
| M1 | 02 (última linha) e 03 (1ª) | Busca "Moreira": só "Nenhum resultado encontrado."; o cadastro abre pelo "+" | Embaixo de "Nenhum resultado encontrado." aparece o botão **"Cadastrar «Moreira»"** (com o texto digitado). O "+" continua (aria "Cadastrar novo"). Na Compra e na Venda o texto digitado NÃO vai para o cadastro: "Nome *" abre vazio | `components/EntitySearchModal.tsx:273,332,343`; `pages/Purchase.tsx:4915` |
| M2 | 04 (linha 1) | "Ela vem do cadastro do fornecedor, e quando ele não tem uma, vem a principal, a da estrela." | Ordem nova da tabela do pedido novo: tabela do fornecedor/cliente → **tabela que o usuário fixou** → principal da empresa. Na lista "Tabela de Preços", a fixada ganha um alfinete (aria **"Minha tabela fixada"**). Fixar é na T3 ("Fixar para meus pedidos e tickets") | `lib/precos/priceTablePreference.ts:24-26`; `components/PriceTableSelector.tsx:72,103`; `pages/Purchase.tsx:1044-1063,1807-1812`; `pages/Sale.tsx:932,1567,1583` |
| M3 | 04 (linha 4) | "escolha sempre o fornecedor antes dos materiais, porque o preço entra na hora em que você escolhe o material" | Com item na lista, trocar o fornecedor (ou cadastrar um novo pelo "+") ou a tabela abre a janela **"Trocar fornecedor?"** / **"Trocar tabela de preços?"** (na venda, "Trocar cliente?"): "O pedido já tem N itens lançados. Escolha o que fazer com os preços atuais.", faixa "anterior → novo", **"Itens que mudam"** "X de N" ("Calculando…"), **"Total se atualizar"** (total antigo riscado e o novo), botões **"Cancelar"**, **"Só nos próximos"**, **"Atualizar X itens"** ("Atualizar 1 item"). Sem item na lista, troca direto como antes | `components/orders/OrderPriceContextChangeDialog.tsx:48-87`; `pages/Purchase.tsx:2465-2502,6134-6143,6461`; `pages/Sale.tsx:2215,2231,6775` |
| M4 | 05, 07, 08, 10, 13, 14 (todo zoom em linha de "Itens do Pedido") | Célula "Valor/Kg" só com o número | Embaixo do Valor/Kg de cada linha há uma legenda cinza pequena com a origem do preço: nome da tabela (ex.: "Principal"; sem nome, "Tabela de preços"), **"Preço personalizado"**, **"Preço do material"**, **"Preço informado"** (digitou outro valor ou editou o Valor/Kg na linha), "Preço importado" (XML/nota), **"Preços combinados"** (mescla de origens diferentes), "Preço gravado" (pedido antigo em edição) | `lib/orders/itemPriceOrigin.ts:20-30`; `pages/Purchase.tsx:5588,5593,3886-3888,3973`; `pages/Sale.tsx:5886,5891` |
| M5 | 10 (linha 2) | Aviso "Preço especial aplicado para Bateria automotiva" | O aviso continua igual, mas a legenda da linha diz **"Preço personalizado"** (dois nomes para a mesma coisa na mesma tela; handoff H4) | `lib/orders/itemPriceOrigin.ts:23` |
| M6 | 11 (linhas 2 e 3) | "Nº de parcelas" só com os atalhos 1·2·3·4·6·12; botão "Adicionar parcela" | Ao lado dos atalhos há um campo numérico (aria **"Quantidade de parcelas"**) e a dica **"Use um atalho ou digite de 1 a 120 parcelas. O total é redistribuído automaticamente."**; o botão virou **"Adicionar e redistribuir"**. Adicionar, remover ou mudar a quantidade REFAZ todas as linhas em valores iguais e datas mensais (a data mudada à mão se perde). A ordem do roteiro (clicar "2" e só depois mudar a data) continua certa | `components/InstallmentsConfigDialog.tsx:258-292,331,347` |
| M7 | 12 (linha 4), 13 | "Opções avançadas" lista "Gerar nota fiscal" | "Gerar nota fiscal" só aparece com o módulo de notas **e** a permissão de emitir NF-e (antes bastava o módulo). Rafael é MASTER: continua aparecendo se o mundo tiver o módulo. O menu também traz a seção de fotos com o botão "Anexar" (já existia; o roteiro não lista: ver L11) | `pages/Purchase.tsx:1845,5138`; `pages/Sale.tsx` (mesmo); `components/AdvancedOptionsPopover.tsx:139-196` |
| M8 | 09, 10, 11, 15 (clique em "Finalizar" da compra) | Finalizar abre direto o pagamento | Só na Compra, com fornecedor escolhido: antes de abrir "Finalizar Pedido" o app relê o fornecedor no servidor. Se não achar: **"O fornecedor deste ticket não está disponível"** · "Ele pode ter sido removido ou não estar acessível. Selecione o fornecedor novamente no pedido."; sem internet e fora da lista local: "Fornecedor do pedido não está disponível neste aparelho" · "Conecte-se ou selecione o fornecedor novamente antes de finalizar." Não muda a fala; muda o backend falso (ver "Mundo") | `pages/Purchase.tsx:4483-4520` |
| M9 | 15 | Queda de internet simulada | A faixa "Sem conexão…" não acredita mais só no navegador: o app faz um teste real (`/auth/v1/health`) e só entra em modo offline depois de 2 falhas seguidas; volta depois de 2 acertos. Os textos da faixa são os mesmos. O robô precisa derrubar esse endereço, não só o `navigator.onLine` | `hooks/useOnlineStatus.ts:6-37`; `components/OfflineBanner.tsx` |
| M10 | (tela de Compra/Venda em edição; a T9 mostra) | Selo "Editando Compra #N" + "Cancelar Edição" | Em edição entram: faixa âmbar **"Editando pedido {número} · {fornecedor} · {tabela}"**; a barra de pedidos (abas) e o aviso de outro operador somem; com o caixa de origem fechado aparece **"Caixa de destino da edição:"** com o selo do caixa (ver 3.9). Na T7 nada disso aparece (nenhum capítulo edita pedido finalizado) | `pages/Purchase.tsx:4768-4788,4893-4899,4994,5278`; `pages/Sale.tsx:5102,5208` |
| M11 | 02, 13 | Campo Fornecedor/Cliente sempre clicável | Usuário com a restrição de parceiros (permissão nova da T2) vê só os parceiros que ele cadastrou; enquanto a permissão não resolve, o campo e o "+" ficam apagados em "Não informado". Rafael (MASTER) não é afetado: só citar na T2 | `pages/Purchase.tsx:1389-1427,4948,4966,5236,5255`; `pages/Sale.tsx` (espelho) |

Venda (`pages/Sale.tsx`): as 667 linhas são o espelho de M2, M3, M4, M7, M10 e M11. Não há mudança própria da venda
(coluna "Lucro", "Lucro estimado", "Estoque insuficiente" e a transferência estão iguais). Do pedido original: **não
existe** aviso de "venda abaixo do custo" nem campo de frete em `Sale.tsx` no 1.60.10 (o lucro negativo só fica
vermelho); não prometer na fala.

## 2. Falta cobrir

| # | Função (texto do código) | Quando o cliente usa | Vale? |
| --- | --- | --- | --- |
| L1 | **Barra de pedidos (várias abas)**: colunas "Número", "Valor", "FORNECEDOR"; "+" (aria "Novo pedido de compra" / "Nova venda"); lista com contador; "Nenhum pedido aberto"; até 20 abas; rascunho salvo sozinho e separado por caixa (`components/OrderSwitcher.tsx:346-366,436,480-483`; `hooks/useOrderCache.ts:21`) | Dois fornecedores no pátio ao mesmo tempo; fila na balança | **Sim, capítulo** (3.1) |
| L2 | **Trocar fornecedor/tabela com itens** (M3) | Pesou antes de saber de quem era; fornecedor pede a outra tabela | **Sim**, dentro de 3.1 |
| L3 | **Descartar pedido**: "Descartar este pedido?" · "Ele tem N material(is) incluído(s). Você pode recuperá-lo depois em Rascunhos apagados." · "Manter pedido" / "Descartar" (`OrderSwitcher.tsx:633,660-712`) | Fornecedor desistiu | **Sim, capítulo** (3.2) |
| L4 | **"Rascunhos apagados"** (topo, com contador): "Recupere um rascunho que foi apagado por engano. Ele volta como uma aba ativa."; "Apagado … por …"; "Recuperar" → "Rascunho recuperado"; lixeira "Excluir definitivamente" → "Excluir de vez?" / "Sim, excluir" → "Rascunho excluído definitivamente"; "Limite de abas atingido. Finalize ou feche uma aba antes de recuperar este rascunho." (`components/DeletedDraftsDialog.tsx:171-213,267-268`; `Purchase.tsx:4868`) | Apagou sem querer | **Sim**, em 3.2 |
| L5 | **"Pedidos Não Finalizados"** no Caixa e a trava: "Não é possível fechar o caixa com pedidos não finalizados" (`components/UnfinishedOrdersTabs.tsx:184`; `pages/Caixa.tsx:2325,2700`) | Fim do dia com pedido esquecido | **Sim**, em 3.2 (a T6 não mostra) |
| L6 | **"Cancelar"** do rodapé: "Cancelar pedido?" · "Isso irá limpar todos os itens adicionados neste pedido. Esta ação não pode ser desfeita." · "Não" / "Sim, cancelar" → "Pedido cancelado e limpo com sucesso!" (`i18n/locales/pt-BR/orders.json` `cancelOrder`; `Purchase.tsx:4651`) | Limpar e recomeçar | **Só citar** em 3.2 |
| L7 | **Dois operadores no mesmo rascunho**: "… está atendendo este pedido.", "Assumir o pedido", "Assumir o pedido de {nome}?" · "{nome} passa a ver a tela como somente leitura e perde o que ainda não tinha sido salvo. Combine antes de assumir.", "Pedido assumido. Você já pode editar." (`components/orders/DraftBatonBanner.tsx:75-188`) | Balanceiro começa, caixa termina | **Só citar** (1 frase em 3.2): pede dois logins na gravação |
| L8 | **Arredondar**: caixa "Arredondar para baixo (−R$ X)" quando o total tem centavos; a escolha fica gravada por operador (`components/MultiPaymentDialog.tsx:1670-1702`) | Pagar sem moeda | **Sim, trecho** (3.3): já está na tela do cap09 (R$ 913,20) e ninguém explica |
| L9 | **Pagar a mais (só compra)**: "Excesso: R$ X" + link "Deixar no saldo de {fornecedor}" → "Sobra de R$ X vai pro saldo" · "{fornecedor} ficará te devendo R$ X" · "Desfazer" (`MultiPaymentDialog.tsx:708,740-744,1635-1665`; `Purchase.tsx:5813`) | Sem troco; adiantamento | **Sim, trecho** (3.3) |
| L10 | **Saldo que já existe**: "Saldo atual:" e "Saldo após o pedido:" com "(Ele te deverá)" / "(Quitado)"; "Vencimento atual do saldo: … Deixe em branco para manter; informe uma nova data para substituir."; "Acima do dinheiro em caixa, o Caixa ficará negativo." (`MultiPaymentDialog.tsx:782-785,894,1142,1155`) | Abater vale do fornecedor na compra; cliente com fiado antigo | **Sim, trecho opcional** (3.10): muda o saldo do Valdir no mundo |
| L11 | **Opções avançadas, o resto**: "Data e hora do pedido" (com permissão) e a pergunta "Em qual caixa lançar?" · "Esta compra está com a data de …. O lançamento pode ir pro caixa daquele dia ou ficar no caixa que você tem aberto agora."; fotos ("Anexar", parte do Portal do Cliente) (`AdvancedOptionsPopover.tsx:128-196`; `components/OrderCashRegisterChoiceDialog.tsx:96-153`; `Purchase.tsx:2946-2975`) | Lançar a compra de ontem; foto da carga | **Sim, trecho** (3.4) para data; fotos **só citar** (T20) |
| L12 | **"Observação"** (campo embaixo da lista) (`Purchase.tsx:5344`; `orders.json` `purchaseForm.notes`) | Recado no pedido | **Só citar** em 3.4 |
| L13 | **Pesagem avançada, opções não mostradas**: "Resumido" ("Só o peso líquido cobrado.") e "Detalhado" ("Bruto, tara, impureza e líquido."); "Preencha 1ª e 2ª pesagem para o bruto, informe só a 1ª (conta como bruto) ou digite o bruto direto."; "Tara (Kg)" com valor; erros "Informe o peso bruto (1ª e 2ª pesagem ou o bruto direto)" e "Peso líquido inválido. Tara e impureza não podem somar mais que o bruto" (`components/AdvancedWeighingDialog.tsx`, linhas do `inventario.md` item 4) | Tambor com tara conhecida; pesagem única | **Sim, trecho** (3.5) |
| L14 | **Botão da balança**: "Substituir X pelo peso da balança (Y kg)?" "Cancelar" / "Substituir"; âmbar (aguardando peso) e vermelho ("Balança desconectada. Clique para ir às configurações."); Enter no peso inclui o item (`components/InputPesoBalanca.tsx`, `inventario.md` item 2) | Repesar; balança caiu | **Sim, trecho** (3.6) |
| L15 | **Trava do peso manual**: "O peso bruto deve ser capturado pela balança", "Para trocar o peso, faça uma nova captura da balança" (`Purchase.tsx:3726,3787,3960`) | Empresa que proíbe digitar peso | **Não aqui**: é preferência; conferir se a T5 cobre (função da T5/T1) |
| L16 | **Editar direto na linha** (peso, tara, Valor/Kg, Valor Total) e o aviso "O Valor Total só reduz (vira desconto na linha). O máximo desta linha é R$ X. Para aumentar, altere o Valor/Kg."; menu "Ações do item": "Editar", "Excluir"; "Desmescle as pesagens antes de editar esta linha" (`Purchase.tsx:3973,4034,4082`; `Sale.tsx:4439`) | Corrigir sem refazer o item | **Sim, trecho** (3.7, na venda) ; "Editar" do menu é da T9 |
| L17 | **"Projeção de Lucro"** no rodapé da COMPRA, com o olho (`Purchase.tsx:5725`) | Dono confere a margem já na compra | **Só citar** (frase em 3.8) |
| L18 | **"+" do Material** → "Cadastrar Novo Material" · "Preencha os dados do material para cadastrá-lo rapidamente" (`components/QuickMaterialDialog.tsx:513`) | Material novo no meio do pedido | **Só citar** (frase em 3.8); cadastro é da T3 |
| L19 | **Comprovante**: "Não, obrigado"; "Impressora EcoTray não conectada — abrindo PDF na janela do navegador. Reabra o EcoTray pra imprimir direto na próxima." (`Purchase.tsx:3474`) | EcoTray fechado | **Só citar** (frase em 3.8) |
| L20 | **Venda**: "Atenção: estoque ficará negativo após esta venda:" (lista dos materiais), "N transferências somando X Kg agendadas para a finalização da venda" (várias origens, "Adicionar origem") (`Sale.tsx:2557,4150`) | Falta coberta por dois materiais | **Só citar** (frase em 3.8); o cap14 já mostra uma origem |
| L21 | **Calculadora de quantidade** ("Calcular quantidade", "Quantidade total") no campo do peso (`components/orders/MaterialQuantityCalculator.tsx:101-177`) | Material vendido por embalagem | **Não**: só aparece em material com embalagem; conferir na T3 |
| L22 | **"Importar XML"** (aria "Importar XML de NF-e"), selo "Origem: Ticket de Pesagem #N", selo de nota recebida, "Gerar nota fiscal", troca de caixa pelo selo ("Selecione um caixa") | | **Não repetir**: T16 (XML, nota recebida, gerar nota), T8 (ticket), T6 (multi-caixa) |
| L23 | **Edição em caixa fechado (1.60.2)** (M10) | Corrigir compra/venda antiga sem reabrir o caixa | **É da T9** (cap04 e cap09). Trecho pronto em 3.9 para a T9 adotar; na T7, uma frase no recap se a decisão for citar |
| L24 | Celular (cadastro rápido na busca, selo de conexão), multimoeda | | **Não**: a aula é de computador; multimoeda é outro módulo |

## 3. Proposta

Tom do roteiro atual. Os capítulos novos entram entre o cap08 e o cap09 (o pedido do Zé ainda aberto, R$ 913,20) e
terminam com o mundo igual ao da entrada: nenhuma compra a mais, nenhum rascunho sobrando.

### 3.1 Capítulo novo · "Dois pedidos ao mesmo tempo" (vinheta: PEDIDOS), depois do cap08

| Tela | Fala |
| --- | --- |
| Zoom na barra escura acima de "Itens do Pedido": "Número" "#1759", "Valor" "R$ 913,20", "FORNECEDOR" "José Carlos Moreira" e o "+" na ponta. [TESTAR: número previsto] | Antes de pagar o Zé, repara nesta barra escura. Ela é o pedido que está aberto agora: o número, o valor e o fornecedor. |
| Clique no "+" (dica "Novo pedido de compra"): a tela esvazia; a barra mostra "#1760", "R$ 0,00", "Sem fornecedor"; o contador "(2)" aparece. | Enquanto o Zé confere a carga dele, chegou uma caminhonete. Não precisa fechar nada: o mais abre outro pedido, e o do Zé fica guardado. |
| "Selecionar fornecedor" → "Não informado"; Material "Cobre misto"; a balança marca 10,0 kg; "Incluir Item": linha com 36,00 e a legenda "Principal" embaixo do preço; total R$ 360,00. [BACKEND: estável em 10,0 kg] [ZOOM: a legenda embaixo do Valor/Kg] | O motorista ainda não disse de quem é a carga, então começo com Não informado e já peso: dez quilos de cobre misto. Embaixo do preço, a tela mostra de onde ele veio: da tabela Principal. |
| Clique no campo "Fornecedor" → "Depósito Irmãos Siqueira": abre "Trocar fornecedor?" ("O pedido já tem 1 item lançado. Escolha o que fazer com os preços atuais."), com "Não informado → Depósito Irmãos Siqueira", "Itens que mudam" "1 de 1" e "Total se atualizar" R$ 360,00 riscado e R$ 374,40. [ZOOM: "Itens que mudam" e "Total se atualizar"] [TESTAR: 37,44 e 374,40] | A carga é do Depósito Irmãos Siqueira, que tem tabela própria. Como já tem item lançado, a tela pergunta o que fazer com o preço. Ela mostra quantos itens mudam e quanto fica o total. |
| A câmera passa pelos três botões: "Cancelar", "Só nos próximos", "Atualizar 1 item". | Só nos próximos troca o fornecedor e deixa o que já foi pesado no preço antigo. Atualizar refaz o preço dos itens pela tabela nova. |
| Clique em "Atualizar 1 item": a linha vai a 37,44, a legenda vira "Tabela Depósitos", o total R$ 374,40; "Tabela de Preços" mostra "Tabela Depósitos". [ZOOM: a linha e o total] | Atualizar. O cobre passou pra trinta e sete e quarenta e quatro, e a legenda agora diz Tabela Depósitos. A mesma pergunta aparece quando você troca só a tabela de preços. |
| Clique na barra escura: a lista abre com os dois pedidos; clique no do Zé: a tela volta com os três itens e R$ 913,20. | Pra voltar ao Zé, é só clicar na barra e escolher o pedido dele. Cada um guarda os seus itens, o seu fornecedor e a sua tabela. |

Fala: ~225 palavras, ~87 s.

### 3.2 Capítulo novo · "Rascunho: sair, descartar e recuperar" (vinheta: RASCUNHO), depois do 3.1

| Tela | Fala |
| --- | --- |
| [ILUSTRAÇÃO: o rascunho: a barra de pedidos com um tique de "salvo" que pisca a cada item incluído; ao lado, o computador desligando e ligando, e os dois pedidos continuam na barra.] | Esses pedidos abertos são rascunhos. O sistema salva sozinho a cada mudança. Se você sair da tela ou fechar o navegador, eles continuam lá. |
| Clique em "Voltar para o caixa": no Caixa, o bloco "Pedidos Não Finalizados" com "2"; em "Compras", os cartões do Zé e do Depósito. [ZOOM: o bloco] | No caixa, eles aparecem em Pedidos Não Finalizados. Uma dica: o caixa não fecha com pedido não finalizado. Antes de fechar, finalize ou descarte cada um. |
| "Nova Compra"; abre a lista da barra; no pedido do Depósito, mouse no "x" ("Descartar pedido") e clique: "Descartar este pedido?" ("Ele tem 1 material incluído. Você pode recuperá-lo depois em Rascunhos apagados."), "Manter pedido" / "Descartar". [ZOOM: a janela] | O motorista do Depósito desistiu de vender hoje. Na lista, o xis descarta o pedido. A janela avisa quantos materiais ele tem. |
| Clique em "Descartar": sobra só o pedido do Zé; no topo, "Rascunhos apagados" com "1". [ZOOM: "Rascunhos apagados"] | Descartar. E se foi engano? Lá em cima, em Rascunhos apagados, fica tudo o que foi descartado, com o dia, a hora e quem apagou. |
| Clique em "Rascunhos apagados": janela "Rascunhos apagados" ("Recupere um rascunho que foi apagado por engano. Ele volta como uma aba ativa."); cartão "Depósito Irmãos Siqueira", "Apagado … por Rafael Nogueira"; clique em "Recuperar": aviso "Rascunho recuperado"; a barra volta a "(2)". | Recuperar, e ele volta como um pedido aberto, do jeito que estava. |
| (Sem fala: descarta de novo; em "Rascunhos apagados", lixeira "Excluir definitivamente" → "Excluir de vez?" → "Sim, excluir": aviso "Rascunho excluído definitivamente". Pode acelerar.) | Como o motorista foi embora mesmo, eu descarto de novo e, desta vez, excluo de vez pela lixeira. |
| No pedido do Zé, mouse em "Cancelar" (rodapé), sem clicar. | Já o Cancelar aqui embaixo é diferente: ele limpa os itens do pedido aberto, e isso não tem volta. E se um colega abrir o mesmo pedido em outro computador, a tela avisa quem está atendendo e deixa assumir. |

Fala: ~205 palavras, ~79 s.

### 3.3 Trecho no cap09 (depois da linha "Em Dinheiro, a tela mostra quanto tem no caixa agora") · arredondar e sobra

| Tela | Fala |
| --- | --- |
| Zoom na caixa "Arredondar para baixo", desmarcada, embaixo do bloco "Total" (sem clicar: a escolha fica gravada para os próximos pedidos). | Como o total tem centavos, aparece o Arredondar para baixo. Marcando, os vinte centavos saem do pagamento. Uma dica: essa escolha fica guardada pro próximo pedido, então confira antes de confirmar. |
| No valor do Dinheiro, digita "920,00": aparece "Excesso: R$ 6,80" e o link "Deixar no saldo de José Carlos Moreira"; clique: "Sobra de R$ 6,80 vai pro saldo" e "José Carlos Moreira ficará te devendo R$ 6,80". [ZOOM: o bloco "Total"] | E se você só tem nota inteira e paga a mais? A tela mostra o excesso e oferece deixar a sobra no saldo do Zé. Aí ele fica devendo esses seis e oitenta, que você abate na próxima compra. |
| Clique em "Desfazer"; o valor volta a 913,20. [TESTAR: o campo aceita voltar ao total] | Aqui o Rafael tem troco, então eu desfaço e pago o valor certo. |

Fala: ~95 palavras, ~37 s. O cap09 segue igual depois ("CONFIRMAR PAGAMENTO").

### 3.4 Trecho no cap12 (depois do balão do "Comprovante sem valores", antes de fechar o menu) · data, observação e fotos

| Tela | Fala |
| --- | --- |
| No mesmo menu, zoom em "Data e hora do pedido" (sem mudar). | No mesmo menu fica a Data e hora do pedido, pra lançar hoje uma compra que aconteceu ontem. Quando a data é de outro dia, a tela pergunta em qual caixa lançar: o daquele dia ou o que está aberto agora. Só aparece pra quem tem essa permissão. |
| A câmera desce até a seção de fotos com o botão "Anexar" e, fechando o menu, até o campo "Observação" embaixo da lista. | Aqui também dá pra anexar fotos da carga, o que faz parte do Portal do Cliente e depende do plano contratado. E fora do menu, embaixo dos itens, o campo Observação guarda um recado no pedido. |

Fala: ~85 palavras, ~33 s.

### 3.5 Trecho no cap06 (depois da linha do "Como exibir no comprovante") · as outras opções da pesagem avançada

| Tela | Fala |
| --- | --- |
| Antes de clicar "Confirmar": mouse em "Resumido" ("Só o peso líquido cobrado.") e "Detalhado" ("Bruto, tara, impureza e líquido."), voltando a "Completo". | No Resumido, o comprovante mostra só o peso líquido. No Detalhado, o bruto, a tara, a impureza e o líquido, sem as duas pesagens. |
| Zoom na dica "Preencha 1ª e 2ª pesagem para o bruto, informe só a 1ª (conta como bruto) ou digite o bruto direto." e em "Tara (Kg)". | E nem sempre tem carroça. Se o material veio num tambor de peso conhecido, é uma pesagem só: o peso na primeira pesagem e o tambor no campo Tara. Uma dica: tara e impureza juntas nunca podem passar do bruto, senão a tela não deixa confirmar. |

Fala: ~75 palavras, ~29 s.

### 3.6 Trecho no cap05 (depois da linha do "botão azul dentro do campo") · repesar e balança fora

| Tela | Fala |
| --- | --- |
| Com 12,400 no campo e a balança em 12,6 kg, clique no botão azul: "Substituir 12,400 pelo peso da balança (12,6 kg)?" "Cancelar" / "Substituir"; clique em "Cancelar". [BACKEND: estável em 12,6 kg e de volta a 12,4] [TESTAR: texto com as casas do mundo] | Se já tem peso no campo e você clica no botão, a tela pergunta antes de trocar. Assim ninguém perde uma pesagem sem querer. |
| [ILUSTRAÇÃO: o botão da balança em três cores: azul "conectada", âmbar "aguardando peso", vermelho "desconectada".] | O botão também avisa pela cor: azul, tudo certo. Âmbar, esperando o peso parar. Vermelho, a balança caiu, e clicando nele você vai pra configuração. |

Fala: ~60 palavras, ~23 s.

### 3.7 Trecho no cap13 (depois da linha do lucro, antes do "Estoque Disponível") · mexer na linha, na venda

| Tela | Fala |
| --- | --- |
| Na linha do latão, clique no "Valor/Kg" e troca 31,90 por 32,00: a legenda embaixo vira "Preço informado"; "Lucro" e "Lucro estimado" sobem; volta a 31,90. [TESTAR: a legenda volta ao nome da tabela ou fica "Preço informado"] [ZOOM: a linha] | Na venda e na compra, dá pra corrigir direto na linha: o peso, a tara e o preço. Mudou o preço na mão, a legenda embaixo vira Preço informado, e o lucro já se refaz. |
| A câmera fica na célula "Valor Total". | Já o Valor Total da linha só aceita baixar: a diferença vira desconto. Pra aumentar, mude o preço do quilo. E a pergunta de trocar preços que a gente viu na compra vale aqui também, quando você troca o cliente ou a tabela. |

Fala: ~80 palavras, ~31 s. Se o [TESTAR] mostrar que a legenda não volta, o robô refaz a linha no `setup` do cap14.

### 3.8 Frases a trocar ou acrescentar em capítulos que já existem

| Cap. | Hoje | Proposta | Motivo |
| --- | --- | --- | --- |
| 02, última linha | "Na busca, ninguém. Então a gente cadastra ele agora." | "Na busca, ninguém. E repara: a própria busca já oferece cadastrar." (Tela: zoom em "Cadastrar «Moreira»") | M1 |
| 03, 1ª linha | "Sem sair da compra, é só clicar no mais." | "Sem sair da compra, é só clicar em Cadastrar, ou no mais lá de cima." (Tela: clique em "Cadastrar «Moreira»"; "Nome *" abre vazio e o robô digita) | M1 |
| 04, 1ª linha | "Ela vem do cadastro do fornecedor, e quando ele não tem uma, vem a principal, a da estrela." | "Ela vem do cadastro do fornecedor. Se ele não tem uma, vem a tabela que você fixou pro seu usuário, e se você não fixou nenhuma, a principal, a da estrela." | M2 |
| 04, 4ª linha | "E escolha sempre o fornecedor antes dos materiais, porque o preço entra na hora em que você escolhe o material." | "O preço entra na hora em que você escolhe o material. Se trocar o fornecedor depois, a tela pergunta o que fazer com os preços, e a gente vê isso daqui a pouco." | M3 |
| 05, linha do "Incluir Item" do cobre | "Incluir Item, e o cobre entra na lista." | "Incluir Item, e o cobre entra na lista, com a origem do preço escrita embaixo dele." | M4 (se 3.1 não entrar) |
| 08, linha do lápis | (fim) | + "E quem tem permissão de ver lucro acompanha aqui embaixo a Projeção de Lucro da compra." | L17 |
| 05, 1ª linha | (fim) | + "Se o material ainda não existe, o mais ao lado do campo cadastra na hora." | L18 |
| 11, linha das duas parcelas | "Duas parcelas de mil reais." | "Duas parcelas de mil reais. Se forem muitas, dá pra digitar a quantidade no campo do lado." + dica: "Uma dica: mude as datas por último. Trocar a quantidade refaz todas as parcelas." | M6 |
| 12, 1ª linha | (fim) | + "Se o EcoTray estiver fechado, o comprovante abre em PDF, e a tela avisa." | L19 |
| 14, linha da origem | (fim) | + "E dá pra somar mais de uma origem, até cobrir a falta." | L20 |
| 16 (recap) | | + uma linha: "Abriu dois pedidos ao mesmo tempo, trocou o fornecedor com item lançado, descartou e recuperou um rascunho." | 3.1 e 3.2 |

Soma das frases: ~125 palavras, ~48 s. Também valem as três propostas de `propostas_fala.md` (caps. 04, 05 e 10); a do
cap04 linha 4 fica substituída pela de cima.

### 3.9 Edição em caixa fechado (1.60.2) · trecho pronto para a T9 (cap04), não para a T7

O que o código faz hoje, na Compra e na Venda em edição, quando o caixa de origem está fechado:
- Aparece **"Caixa de destino da edição:"** + selo do caixa (clicável; a janela é a "Em qual caixa registrar?").
- Pedido **sem dinheiro** (só Pix e/ou saldo) e caixa do próprio operador (ou de quem opera todos): a lista ganha
  **"Manter no caixa original #N"** · "Sem movimento em dinheiro; o fechamento não será alterado."; o selo mostra
  **"Caixa #N · Original"**; legenda "Sem movimento em dinheiro: você pode manter o caixa original sem alterar o
  fechamento." Mantendo o original, se a edição puser dinheiro: "Para receber valor em dinheiro, escolha um caixa aberto
  antes de salvar a edição."
- Pedido **com dinheiro**: "O caixa original está fechado. Como houve movimento em dinheiro, escolha um caixa aberto."
  Caixa de outro operador: "O caixa original pertence a outro operador. Escolha um caixa aberto autorizado."
- Sem caixa para lançar: "Escolha em qual caixa aberto lançar a edição." ou "Não há caixa aberto disponível para lançar
  a edição."; carregando: "Carregando as opções de caixa. Tente novamente em instantes."
- `pages/Purchase.tsx:2209-2240,2676,4604-4612,4768-4788`; `pages/Sale.tsx:1996,2411,4941-4947,5102-5114`.

Isso contradiz a fala do cap04 da T9 ("o caminho mais tranquilo é reabrir o caixa daquele dia"): para pedido sem dinheiro,
editar direto já não mexe no fechamento. Trecho sugerido (para a auditoria da T9 adotar):

| Tela | Fala |
| --- | --- |
| "Editar" numa compra paga no Pix, de caixa fechado: tela "Compra" com "Editando pedido …" e "Caixa de destino da edição:" "Caixa #70 · Original". [ZOOM: o selo e a legenda] | Essa compra foi paga no Pix e é de um caixa já fechado. Como não teve dinheiro, a edição pode ficar no caixa original, sem mudar o fechamento daquele dia. |
| Clique no selo: a lista com "Manter no caixa original #70" e o caixa aberto de hoje. | Se preferir, dá pra lançar a correção num caixa aberto. E quando o pedido teve dinheiro, só essa segunda opção aparece: você escolhe o caixa aberto que recebe o acerto. |

Fala: ~70 palavras, ~27 s. Mundo: uma compra só no Pix num caixa fechado do Rafael.

### 3.10 Trecho opcional no cap09 ou cap10 · comprar abatendo o vale (depende de decisão)

Caso de uso real que hoje ninguém mostra: o fornecedor já deve (Valdir Pereira tem um vale de R$ 300,00) e a compra
abate. Tela: compra do Valdir (Ferro misto, 200 kg, R$ 150,00) → "Finalizar" → "Saldo do Fornecedor": no resumo, "Saldo
atual:" e "Saldo após o pedido:" com "(Ele te deverá)". Fala (~55 palavras, ~21 s): "O Valdir pegou um vale de trezentos
reais. Então esta compra de cento e cinquenta eu pago no saldo: não sai dinheiro, e a dívida dele cai pela metade. O
resumo mostra o saldo de antes e o de depois. Quando zerar, aparece Quitado."
Custo: muda o saldo do Valdir (T4, T13 e a compra duplicada dele na T9 usam esse número). Alternativa sem custo: abrir o
pagamento, mostrar e fechar sem confirmar, descartando o pedido.

### O que o mundo fictício e o backend falso precisam

- **Todas as compras (M8)**: `GET suppliers?select=id,name,pix_key&company_id=eq.…&id=eq.…` precisa devolver o fornecedor,
  inclusive o **Zé criado no cap03** (o `INSERT` tem de ficar guardado no backend falso), senão o "Finalizar" para no
  aviso "O fornecedor deste ticket não está disponível".
- RPC **`log_order_activity`** (nova; chamada ao trocar preços e ao abrir edição): responder vazio, sem erro.
- **`profiles.preferred_price_table_id`** = `null` para o Rafael (consulta nova a cada tela de pedido); RPC
  `set_my_preferred_price_table` só na T3.
- Linhas de item gravadas por `create_purchase_atomic` / `create_sale_*` agora levam `price_origin_type`,
  `price_table_id`, `price_table_name`: aceitar os campos.
- **cap15 (M9)**: derrubar `/auth/v1/health` (2 falhas seguidas para cair, 2 acertos para voltar; conta uns 3 s a mais
  na volta) e manter a Aparecida na lista local de fornecedores.
- **3.1 e 3.2**: tabela `order_drafts` com leitura, gravação e `deleted_at`/`deleted_by` (apagar, recuperar, excluir de
  vez); "Tabela Depósitos" (+4 %) ligada ao Depósito Irmãos Siqueira com item de Cobre misto a 37,44; balança estável em
  10,0 kg; `profiles` com o nome do Rafael para o "Apagado … por"; previsão de número (#1759 e #1760) por
  `preview_next_order_ref`. Sem canal de presença, a faixa do colega não aparece (é o esperado).
- **3.3**: nada novo (o cap09 já tem o Zé com saldo zero). **3.6**: balança em 12,6 kg e de volta a 12,4.
- **3.9 (T9)**: compra só no Pix em caixa fechado do Rafael, e `cash_transactions` sem linha de dinheiro para ela.

### Handoffs novos (para o time do app; a fala não depende)

- H4: a mesma linha recebe o aviso "Preço especial aplicado" e a legenda "Preço personalizado".
- H5: trocando o fornecedor a partir do campo vazio, a janela mostra "Fornecedor atual → …" (não há nome anterior).
- H6: na Compra e na Venda, "Cadastrar «texto»" não leva o texto para o "Nome *" (no Ticket de Pesagem leva).
- H7: as mensagens antigas "Para editar um pedido de um caixa já fechado, o estorno é lançado no caixa de hoje. Abra o
  caixa primeiro." (`Purchase.tsx:3665`, `Sale.tsx:3909`) e "Pedido antigo estornado! Recriando no caixa de hoje..."
  (`Purchase.tsx:2762`) ficaram com o texto de antes do 1.60.2.

## 4. Estimativa

| Bloco | Palavras | Fala |
| --- | --- | --- |
| 3.1 capítulo "Dois pedidos ao mesmo tempo" | ~225 | ~87 s |
| 3.2 capítulo "Rascunho: sair, descartar e recuperar" | ~205 | ~79 s |
| 3.3 a 3.7 (cinco trechos em caps. 05, 06, 09, 12 e 13) | ~395 | ~153 s |
| 3.8 frases | ~125 | ~48 s |
| **Total recomendado** | **~950** | **~367 s (6,1 min)** |
| Opcional 3.10 (vale do Valdir) | ~55 | ~21 s |
| 3.9 (vai para a T9, não soma aqui) | ~70 | ~27 s |

Capítulos novos: **2** (mais 2 vinhetas, 1 ilustração no 3.2 e 1 no 3.6). A aula vai de ~16,1 para ~22,2 min de fala
(cerca de 25 min de vídeo). Regravar por causa do app: caps. 02 e 03 (M1), 05, 07, 08, 10, 13 e 14 (legenda nova nas
linhas, M4), 11 (M6) e 15 (M9); os demais só se entrarem trechos.

## Depende de decisão

1. Edição em caixa fechado: fica só na T9 (recomendado, trecho 3.9) ou a T7 também cita no recap.
2. 3.10 (vale do Valdir): gravar confirmando (muda saldo usado na T4, T9 e T13), só mostrar e descartar, ou deixar fora.
3. Dois operadores no mesmo rascunho (L7): só a frase do 3.2 ou cena gravada com o login do Marcos.
4. Trava do peso manual (L15) e calculadora por embalagem (L21): confirmar que T5 e T3 cobrem; se não, voltam para cá.
5. Tamanho: com tudo, a T7 passa do alvo de 22 min; alternativa é partir em duas aulas (compra · venda e sem internet).
