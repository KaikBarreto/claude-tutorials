# T13 · Cobertura contra o EcoSistema 1.60.10

Auditoria de 18/11/2026, só leitura de código (`/dev/shm/ecoflix-src`, diff `f37573ea0..5290be4cd`). Caminhos relativos a
`src/`. Nada foi rodado no navegador: o que depende de tela está marcado `[TESTAR]`. O comportamento das RPCs vem das
migrações `20261117180000`, `20261117234500` e `20261117235000`. Não existe varredura do robô para a T13 ainda
(`rec/varredura/` só tem t00 a t04). As trocas do `propostas_fala.md` (cap07 e cap08, recorrência com "Repetir até")
continuam valendo e não se repetem aqui.

## 1. Mudou no app (por capítulo)

| # | Cap. | O que o roteiro mostra | Como está no 1.60.10 | Onde |
|---|---|---|---|---|
| 1 | 02, 12 (e 13) | "Os cartões mostram sempre a empresa inteira, com ou sem filtro"; no cap12, "os cartões continuam iguais" | **Falso agora.** Os cartões somam exatamente as linhas da lista: mudam com a aba, a busca e todos os filtros. Com filtro de status ligado, o saldo (fiado) sai da lista e também do total | `hooks/useBills.ts:548-564` (`summarizeListRows(rows, ...)`), `lib/contasBillsCurrency.ts:190-214` |
| 2 | 01, 02, 09, 10, 12 | Quatro cartões fixos: "Total a Pagar", "Total a Receber", "Vencidas", "Vence em 7 dias" | Só na aba "Todas". Na aba "A Pagar": "Total a Pagar", **"Total pago"**, "Vencidas", "Vence em 7 dias". Na "A Receber": "Total a Receber", **"Total recebido"**, "Vencidas", "Vence em 7 dias". Com "Vencimento (período)" preenchido os dois primeiros viram "A pagar no período" / "A receber no período" e "Pago no período" / "Recebido no período" | `components/contas/BillsSummaryCards.tsx:109-141`, `pages/ContasPagarReceber.tsx:1111-1112` |
| 3 | 04, 05, 06, 07 | Ordem dos campos: "Tipo", "Valor", "Descrição", "Vencimento", "Categoria" | Ordem nova: "Tipo", **"Descrição"**, **"Vencimento"**, **"Valor"**, "Categoria". O cursor já nasce na "Descrição" ao abrir "Nova conta" | `components/contas/BillFormModal.tsx:907-963` (`autoFocus={!isEdit}` em `:913`) |
| 4 | 04, 05, 06, 07 | "Descrição" é um campo de texto comum | Ao criar, a "Descrição" busca padrões depois de 3 letras e pode abrir, embaixo do campo, o bloco "Padrão encontrado: ..." com o botão "Preencher" (empurra os campos de baixo). `[TESTAR]` em cada descrição do roteiro; risco maior no cap07: "Aluguel da empilhadeira" começa igual a "Aluguel do galpão", e se o mundo tiver duas contas do galpão com a mesma descrição o padrão aparece enquanto o robô digita | `components/financial/FinancialDescriptionField.tsx:132-152`, `hooks/useFinancialDescriptionSuggestions.ts:37-55` |
| 5 | 04, 05 | "Pagamento previsto" ocupa a linha inteira | Ao escolher uma conta bancária, o campo encolhe e aparece ao lado **"Forma de pagamento"**, com "Pix / Transferência" (padrão), "Boleto" e "Cheque". Em "Dinheiro (Caixa)" ou "Não definido" ele não aparece | `BillFormModal.tsx:1179-1195`, `components/financial/PaymentMethodRefine.tsx:24-28,55` |
| 6 | 08 (e 13) | Botão "Esta e as futuras" na janela "Editar conta recorrente" / "Excluir conta recorrente" | O botão agora é **"Esta e as próximas"**. Título e pergunta da janela não mudaram. O aviso embaixo do vencimento continua "Esta data e as futuras serão deslocadas pelo mesmo período." e o toast de exclusão continua "Esta e as futuras excluídas" | `components/contas/BillsList.tsx:706`; `BillFormModal.tsx:946`; `pages/ContasPagarReceber.tsx:983` |
| 7 | 06 (depois dele) | Parcela criada pelo "Parcelar" edita e exclui direto, como conta avulsa | "Editar" ou "Excluir" numa parcela abre **"Editar parcelas"** / **"Excluir parcelas"**: ""<descrição>" faz parte de um parcelamento. O que deseja editar?", com "Só esta conta", "Esta e as próximas", "Todas as parcelas pendentes" e "Cancelar". Na edição, a descrição abre sem o " (parcela 2/3)". Só vale para parcelamento feito na tela (as parcelas da Fundição, que vêm de pedido, seguem como antes) | `BillsList.tsx:558,572,668-723`; `BillFormModal.tsx:307-311` |
| 8 | todos | Clicar numa linha da lista não faz nada | Clicar em qualquer ponto da linha de uma conta (fora dos botões e da caixinha) abre **"Detalhes da conta"**, "Informações completas do lançamento". Robô: nenhum clique pode cair no corpo da linha | `BillsList.tsx:732-761,1113-1127` |
| 9 | 11 | "Anexar" mostra a miniatura e o "Salvar" grava | Na edição o arquivo sobe na hora e aparece o aviso **"Anexo adicionado"** antes do "Salvar"; o botão "Anexar" fica girando enquanto carrega `[TESTAR]` | `components/financial/TransactionAttachmentsField.tsx:250-289,345` |

Sem mudança de rótulo: abas, busca, "Lista"/"Calendário", painel "Filtros" (ganhou atalhos, ver lacuna 6), "Pagar conta"
para conta não recorrente, "Receber de <parceiro>" (fiado), calendário.

### Trocas de fala obrigatórias (texto novo)
- **cap02, última linha.** De: "Uma dica: repara que eu troquei de aba e os números não mudaram. Os cartões mostram sempre a
  empresa inteira, com ou sem filtro." Para: "Uma dica: os cartões acompanham o que está na lista. Na aba A Pagar, eles
  mostram o Total a Pagar e o Total pago. Na A Receber, o Total a Receber e o Total recebido. E com busca ou filtro
  ligado, somam só o que apareceu." Tela: clique em "A Pagar" (o segundo cartão vira "Total pago"), "A Receber" ("Total
  recebido"), volta para "Todas".
- **cap04.** Reordenar as linhas para Descrição, Vencimento, Valor. Depois do "Pagamento previsto", acrescentar: "Do lado
  aparece a Forma de pagamento: Pix ou transferência, boleto ou cheque. Deixo no Pix." (manter Pix: com "Boleto" ou
  "Cheque" no previsto a janela de baixa abre em "Dinheiro", `PayBillModal.tsx:146-150`, e o cap09 depende do Pix sugerido).
- **cap05, cap06, cap07.** Só a ordem da coluna Tela (Descrição, Vencimento, Valor). No cap06 a frase "No Valor vai o total
  da compra" passa para depois da descrição e do vencimento.
- **cap08.** Trocar "esta e as futuras" por "esta e as próximas" nas quatro falas que citam o botão (linhas 2, 3, 4 e 6) e
  no letreiro da ilustração. No cap13: "mudou o vencimento desta e das próximas".
- **cap12, linha dos cartões.** De: "E os cartões lá em cima continuam iguais, como a gente viu." Para: "E os cartões lá em
  cima mudaram junto: agora somam só as pendentes."

## 2. Falta cobrir

| # | Função (rótulo exato) | Quando o cliente usa | Vale? | Onde |
|---|---|---|---|---|
| 1 | **Preenchimento inteligente** na "Descrição": "Padrão encontrado: <descrição>", linha com parceiro · categoria · centro de custo · conta · forma, "Usado N vezes · última vez em <mês> de <ano>", botão "Preencher", "Campos preenchidos. Desfazer preenchimento"; setas, Enter ou Tab, Esc fecha (1.60.5, 1.60.7, 1.60.8) | Conta que volta com a mesma descrição (internet, contador, frete) | **Sim, capítulo** | `FinancialDescriptionField.tsx:76-104,116-126,138-155` |
| 2 | **Baixa de recorrente pelo valor real**: "Valor desta ocorrência", "Atualizar o valor previsto das próximas contas", resumo "Previsto: R$ X · Valor desta ocorrência: R$ Y." (1.60.5) | Conta recorrente que veio com valor diferente no mês, ou reajuste | **Sim, capítulo** | `PayBillModal.tsx:73-79,773-785,936-941`; RPC `pay_recurring_financial_bill` |
| 3 | **Editar e excluir parcelas em grupo** ("Esta e as próximas", "Todas as parcelas pendentes"; toasts "N parcelas pendentes atualizadas", "N parcelas pendentes excluídas", "N parcelas foram mantidas porque já têm pagamento registrado.") | Fornecedor muda o vencimento das parcelas; compra cancelada | **Sim, capítulo curto** | `BillsList.tsx:668-723`; `pages/ContasPagarReceber.tsx:935-958,1013-1021` |
| 4 | **"Detalhes da conta"** (clique na linha): "Tipo", "Valor", "Vencimento", "Categoria", "Cliente/fornecedor", "Parcela", "Observação" | Conferir uma conta sem abrir a edição | Sim, trecho no cap01 | `BillsList.tsx:732-761` |
| 5 | Dica do status (mouse em cima): "Vencida há N dia(s)"; na paga ou parcial, "Valor pago", "Juros", "Tarifa", "Total pago", "Falta" | Ver rápido quanto já foi pago | Sim, uma frase no cap01 | `components/contas/BillStatusTooltip.tsx:98-170` |
| 6 | Atalhos do "Vencimento (período)": "Este mês", "Próximos 7 dias", "Até o fim do mês" | Ver o que vence no mês sem digitar datas | Sim, trecho no cap12 (junto com os cartões "no período") | `pages/ContasPagarReceber.tsx:1375-1379,724-744` |
| 7 | "Forma de pagamento" prevista: "Boleto" e "Cheque"; a etiqueta da lista passa a "Boleto · <conta>" | Marcar que a conta é paga por boleto | Sim, frase no cap04 (ver trocas) | `PaymentMethodRefine.tsx`; `BillsList.tsx:256-272` |
| 8 | "Juros / multa (opcional)" + "Categoria do juros" (vem "Juros e Multas"); "A conta continua valendo R$ X. Este valor entra como despesa separada." Só em conta a pagar | Conta paga com atraso | **Sim, trecho no cap09** (a água vencida) | `PayBillModal.tsx:993-1035` |
| 9 | "Tarifa (opcional)" | Banco cobrou tarifa no boleto ou na transferência | Sim, uma frase no mesmo trecho | `PayBillModal.tsx:1039-1050` |
| 10 | "Múltiplas formas de pagamento" (recebimento: "Múltiplas formas de recebimento"), "Valor em <forma>", e a forma "Saldo da ficha" (só com parceiro) | Parte em dinheiro e parte em Pix; abater do crédito do parceiro | Sim, uma frase no mesmo trecho | `PayBillModal.tsx:788-803,445` |
| 11 | "Sobra R$ X → vira crédito de <parceiro>" | Pagou a mais | Só citar (no mesmo trecho) | `PayBillModal.tsx:946-951` |
| 12 | "Mais ações" → **"Estornar pagamento"**: "Saiu de"/"Entrou em", "Voltam R$ X para <origem>"; travas: caixa fechado, pagamento conciliado, baixa de lote, baixa pelo saldo | Deu baixa na conta errada | **Sim, capítulo curto** (o inventário cita o menu, o roteiro não mostra) | `BillsList.tsx:592-617`; `components/contas/UndoBillPaymentModal.tsx:53-69,313-345,398` |
| 13 | Excluir conta com baixa: "Excluir conta?", "Excluir devolve R$ X para <origem>", botão "Excluir e estornar" | Conta lançada e paga por engano | Sim, no capítulo do estorno | `components/contas/DeleteBillDialog.tsx:271-298,341,353` |
| 14 | **Pagamento em lote**: caixinha da linha ("Selecionar para pagar em lote"), barra "N linhas selecionadas", "Total: R$ X", "N de saldo", "Limpar", "Quitar em lote" / "Receber em lote"; janela "Pagar N linhas em 1 lançamento", "Total R$ X — vira um único lançamento, que casa 1-pra-1 na conciliação bancária.", "Descrição do lançamento", aviso de "categorias diferentes" | Um Pix pagou várias contas | **Sim, capítulo** | `components/contas/BillsBulkPayBar.tsx:70-128`; `PayBillsBatchModal.tsx:520-552,656-672,762` |
| 15 | **"Exportar"** → "Exportar contas" → "PDF" / "Excel": janela "Exportar contas (PDF)", "Escolha o que entra no arquivo. Os filtros já vêm com o que você está usando na tela.", "Opções do arquivo", "Fiado / saldo de cliente e fornecedor", "Agrupar por" ("Nenhum", "Status", "Categoria", "Mês") | Mandar a lista ao contador, imprimir | Sim, capítulo curto (o roteiro tinha deixado fora) | `pages/ContasPagarReceber.tsx:1169-1203`; `components/contas/BillsExportDialog.tsx:116-119,517-518,752-812` |
| 16 | "Pendurar no saldo do fornecedor (pagar depois)" (só conta a pagar, com fornecedor, sem vencimento) | Compra fiada sem data | Só citar no cap10 (uma frase); gravar exigiria apagar o vencimento | `BillFormModal.tsx:460-470,516` |
| 17 | Aviso "Conta igual já cadastrada" / "Salvar mesmo assim" | Lançou a mesma conta duas vezes | Só citar (uma frase no cap04) | `BillFormModal.tsx` (bloco do aviso de duplicidade) |
| 18 | "+" ao lado de "Categoria" e do parceiro (cria sem sair da janela) | Categoria ou fornecedor ainda não cadastrado | Só citar no cap04 | `BillFormModal.tsx` (bloco "O que é") |
| 19 | "Faturas de Cartão" (seção recolhida) e a nota do cartão no "Total a Pagar" | Empresa com cartão de crédito cadastrado | Não: o mundo não tem cartão e a seção não aparece. Uma frase só se a T14 cadastrar cartão | `pages/ContasPagarReceber.tsx:1424-1489` |
| 20 | Status "Projetada" ("Valor estimado pelo RH; pode mudar até o fechamento.") | Folha em aberto | Não aqui: é da T19 (Funcionários) | `BillStatusTooltip.tsx:102-104` |
| 21 | O mesmo preenchimento inteligente nos lançamentos de entrada e saída (`DepositModal`, `WithdrawalModal`) | Lançamento avulso no caixa ou no banco | Não aqui: T6 (Caixa) e T14 (Bancos). Na T13, só a frase "vale também nos lançamentos" | `components/DepositModal.tsx`, `components/WithdrawalModal.tsx` |

## 3. Proposta

Ordem nova sugerida: 00, 01, 02, 03, 04, 05, **05b**, 06, 07, 08, **08b**, 09 (com o trecho novo), **09b**, **09c**,
**09d**, 10, 11, 12 (com o trecho novo), **12b**, 13 (recapitulação refeita).

### Trechos em capítulos que já existem

**cap01, depois da linha do aluguel (2 linhas novas)**

| Tela | Fala |
| --- | --- |
| O mouse para em cima do status "Vencida" da água: a dica mostra "Vencimento 05/11/2026" e "Vencida há 5 dia(s)". | Parando o mouse em cima do status, o sistema conta mais: há quantos dias venceu, ou quanto já foi pago. |
| Clique no meio da linha "Energia elétrica de outubro": janela "Detalhes da conta" ("Informações completas do lançamento"), com "Tipo", "Valor", "Vencimento", "Categoria", "Cliente/fornecedor", "Parcela" e "Observação"; fecha (Esc). | E clicando na linha, abrem os Detalhes da conta: tipo, valor, vencimento, categoria, de quem é, a parcela e a observação. |

**cap09, depois do pagamento parcial da prensa (trecho "conta atrasada")**

| Tela | Fala |
| --- | --- |
| Na linha "Água e esgoto de outubro" ("Vencida", R$ 238,40), clique em "Marcar pago": "Pagar conta", "Água e esgoto de outubro · Restante R$ 238,40". | E a conta que atrasou? A água venceu dia cinco e veio com multa. Clico em Marcar pago. |
| Em "Juros / multa (opcional)" digita 4,77: aparece "A conta continua valendo R$ 238,40. Este valor entra como despesa separada." e "Categoria do juros" com "Juros e Multas". [ZOOM: o campo e o aviso] | O valor da conta continua o mesmo. A multa vai no campo Juros / multa: quatro reais e setenta e sete. Ela entra como uma despesa separada, na categoria Juros e Multas. |
| A câmera desce para "Tarifa (opcional)". | Tem também o campo Tarifa, pra quando o banco cobra pelo boleto ou pela transferência. |
| Liga "Múltiplas formas de pagamento": os cartões "Dinheiro" e "Pix/Transferência" passam a aceitar os dois, com "Valor em Dinheiro" e "Valor em Pix/Transferência"; desliga. | E se você paga uma parte em dinheiro e outra por Pix, liga o Múltiplas formas de pagamento e coloca o valor de cada uma. |
| A câmera fica no resumo "Total informado". | Uma dica: se pagar a mais numa conta com fornecedor, a sobra vira crédito dele, e a tela avisa antes de confirmar. |
| Clique em "Cancelar". | Aqui eu só cancelo. |

**cap12, depois do filtro de status (trecho "período")**

| Tela | Fala |
| --- | --- |
| "Filtros" → em "Vencimento (período)", clique em "Este mês": "De" 01/11/2026 e "Até" 30/11/2026; a câmera passa por "Próximos 7 dias" e "Até o fim do mês"; "Aplicar". | No período de vencimento, tem três atalhos: Este mês, Próximos 7 dias e Até o fim do mês. |
| A câmera sobe aos cartões: "A receber no período" e "Recebido no período". [ZOOM: os dois primeiros cartões] | Com um período ligado, os cartões mudam de nome: A receber no período e Recebido no período. |

### cap05b · O sistema preenche pra você (vinheta: LANÇAMENTO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t13/apos-cap05`), aba "Todas"; clique em "Nova conta": o cursor já está em "Descrição". | Tem conta que volta todo mês com os mesmos dados. A internet do escritório, por exemplo. Pra essas, o sistema ajuda a preencher. |
| Digita "Internet do escritório" (inteiro: o padrão não troca o texto da descrição); embaixo do campo abre "Padrão encontrado: Internet do escritório". [BACKEND: rpc `get_financial_description_suggestions` (`p_context` bill, `p_direction` payable)] | Começo pela Descrição: Internet do escritório. Repara que, depois de três letras, aparece um Padrão encontrado. |
| [ZOOM: o bloco, com "Vale Fibra Telecom Ltda · Internet e telefone · Escritório · Conta Principal · Boleto" e "Usado 2 vezes · última vez em outubro de 2026"] | Ele mostra o que a empresa usou das outras vezes: o fornecedor, a categoria, o centro de custo, a conta do banco e a forma de pagamento. E quantas vezes esse padrão já foi usado. |
| Clique em "Preencher": "Categoria", o fornecedor, "Centro de custo", "Pagamento previsto" ("Conta Principal") e "Forma de pagamento" ("Boleto") preenchidos; o cursor vai para "Valor"; embaixo da descrição, "Campos preenchidos. Desfazer preenchimento". | Clico em Preencher. Pronto: categoria, fornecedor, centro de custo e pagamento previsto, tudo de uma vez. E o cursor já pula pro Valor. |
| Em "Valor" digita 189,90; em "Vencimento" escolhe 20 (20/11/2026). [ZOOM: "Valor" com 189,90] | Digito cento e oitenta e nove e noventa, e ajusto o Vencimento pro dia vinte. |
| A câmera vai a "Campos preenchidos. Desfazer preenchimento" (sem clicar). | Uma dica: o padrão só preenche campo vazio. O que você já escolheu, ele não troca. E se não era isso, tem o Desfazer preenchimento, logo embaixo. |
| A câmera fica na janela. | Dá pra fazer tudo pelo teclado: as setas escolhem o padrão, e o Enter ou o Tab preenchem. |
| Clique em "Criar conta": aviso "Conta criada"; a linha "Internet do escritório", 20/11/2026, R$ 189,90, "Pendente", etiqueta "Boleto · Conta Principal". [BACKEND: insert em `financial_bills` com `expected_payment_method` boleto] | Criar conta. E de onde vêm os padrões? Das contas e dos lançamentos do último ano com a mesma descrição. Vale também nas entradas e saídas do caixa e do banco. |

Mundo: duas contas a pagar **pagas**, com a descrição idêntica "Internet do escritório" (vencimentos 10/09/2026 e
10/10/2026, `created_at` em setembro e outubro, R$ 189,90), categoria de despesa "Internet e telefone" (nova), centro
"Escritório", fornecedor "Vale Fibra Telecom Ltda" (novo, fictício, conferir na semente), `expected_payment_method`
boleto e `expected_bank_account_id` da Conta Principal, sem `order_id` nem `source_type`. Regra real para o handler: só
sugere com 3 letras ou mais, descrição começando igual, vencimento entre hoje menos 365 dias e hoje, e padrão usado 2
vezes ou mais (ou 1 vez nos últimos 90 dias se a descrição for digitada inteira); devolve no máximo 3, com
`description`, `category_id`, `category_label`, `partner_id`, `partner_type`, `partner_name`, `cost_center_id`,
`cost_center_name`, `payment_source` (id da conta ou `__cash__`), `payment_method`, `bank_account_name`, `usage_count`,
`last_used`. Para as outras descrições do roteiro o handler devolve `[]` (conferir o galpão, mudança 4).

### cap08b · E as parcelas? (vinheta: LANÇAMENTO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t13/apos-cap08`); na busca digita "pneus": as três parcelas da Auto Peças Vale Forte. | As parcelas dos pneus funcionam parecido. A Auto Peças pediu pra passar o vencimento pro dia vinte e oito, a partir da segunda. |
| Na parcela de 23/12/2026, clique no lápis "Editar": janela "Editar parcelas", ""Pneus do caminhão truck (parcela 2/3)" faz parte de um parcelamento. O que deseja editar?", com "Só esta conta", "Esta e as próximas", "Todas as parcelas pendentes" e "Cancelar". | Clico em editar na parcela dois. Aqui são três opções: Só esta conta, Esta e as próximas, ou Todas as parcelas pendentes. |
| Clique em "Esta e as próximas": "Editar conta" (descrição "Pneus do caminhão truck"); em "Vencimento" troca para 28 (28/12/2026); aparece "Esta data e as futuras serão deslocadas pelo mesmo período.". | Escolho Esta e as próximas e troco o vencimento pra vinte e oito de dezembro. |
| Clique em "Salvar": aviso "2 parcelas pendentes atualizadas"; a lista: 23/11/2026, 28/12/2026 e 28/01/2027. [BACKEND: rpc `update_installment_bill_group` (`p_scope` future)] [TESTAR: se sai também "Conta atualizada"] | Salvar. A segunda e a terceira andaram juntas, e a primeira ficou como estava. |
| A câmera fica nas três linhas. | Uma dica: nessa edição em grupo, o valor e os outros campos da tela vão pra todas as parcelas escolhidas. Se as parcelas têm valores diferentes, mude uma de cada vez, com Só esta conta. |
| Na parcela de 28/01/2027, clique na lixeira: "Excluir parcelas", com as três opções ("Esta e as próximas" e "Todas as parcelas pendentes" em vermelho) e "Parcelas pagas ou com baixa permanecem no histórico e não serão excluídas."; clique em "Cancelar". | Excluir faz a mesma pergunta. E parcela que já foi paga não é apagada: fica no histórico. |

Mundo: o handler `create_installment_bills` do cap06 precisa gravar `installment_group_id` (o mesmo nas três),
`installment_number` e `installment_total`, senão a janela "Editar parcelas" não abre. Handlers novos:
`update_installment_bill_group` (desloca as pendentes do escopo pelo mesmo número de dias; devolve `updated`) e
`delete_installment_bill_group` (não usado se o robô cancela).

### cap09b · O valor real do mês (vinheta: BAIXA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t13/apos-cap09`); na busca digita "aluguel da": a conta de 12/11/2026, R$ 2.300,00, "Pendente". | Nem toda conta que se repete vem sempre igual. Este mês, o aluguel da empilhadeira veio com horas a mais: dois mil quatrocentos e quinze reais, em vez de dois mil e trezentos. |
| Clique em "Marcar pago": "Pagar conta"; no alto, "Valor desta ocorrência" com 2.300,00 e o texto "Altere o valor da conta antes de informar quanto será pago agora. Por padrão, as próximas contas mantêm o valor previsto.". | Clico em Marcar pago na de novembro. Como ela é de uma recorrência, aparece um campo lá em cima: Valor desta ocorrência. |
| Apaga e digita 2.415,00; o valor da forma de pagamento acompanha (2.415,00). [ZOOM: "Valor desta ocorrência" com 2.415,00] | Troco pra dois mil quatrocentos e quinze. O valor do pagamento acompanha sozinho. |
| [ZOOM: o resumo "Previsto: R$ 2.300,00 · Valor desta ocorrência: R$ 2.415,00. As próximas contas mantêm o valor previsto." e "Quita a conta"] | Embaixo, o resumo mostra o previsto e o valor deste mês. E avisa: as próximas contas mantêm o valor previsto. |
| A câmera vai ao interruptor "Atualizar o valor previsto das próximas contas" (desligado). | Se fosse um reajuste do contrato, era só ligar o Atualizar o valor previsto das próximas contas. Aí as próximas, que ainda estão abertas no valor antigo, passam pro valor novo. |
| Clica no cartão "Pix/Transferência", escolhe "Conta Principal" em "Conta bancária"; "Data do pagamento" 10/11/2026; "Confirmar pagamento": aviso "Pagamento registrado". [BACKEND: rpc `pay_recurring_financial_bill` (`p_occurrence_amount` 2415, `p_update_future_amounts` false)] | Aqui foi só este mês, então deixo desligado. Escolho o Pix, a Conta Principal, e confirmo. |
| A lista: 12/11/2026 "Paga", R$ 2.415,00; 15/12/2026 "Pendente", R$ 2.300,00. [ZOOM: os dois valores] | Pronto. Novembro ficou paga por dois mil quatrocentos e quinze, e dezembro continua com dois mil e trezentos. |
| A câmera fica na lista. | Uma dica: isso é diferente de pagar em parte. Aqui você corrige quanto a conta vale. O pagamento parcial é quando você paga menos do que ela vale. |

Mundo: a conta de 12/11 precisa de `recurring_template_id`, `status` pending e `paid_amount` 0 (sai do cap07). Handler
novo `pay_recurring_financial_bill`: troca o `amount` da conta, e com o interruptor ligado troca também o do molde e o
das próximas pendentes que ainda estão no valor do molde; depois faz a baixa normal. A recorrência não tem "Pagamento
previsto", então a janela abre em "Dinheiro" (por isso o robô troca para Pix). **Cria um Pix de R$ 2.415,00 em 10/11 na
Conta Principal**: o OFX da T14 e a DRE da T15 precisam contar com ele.

### cap09c · Pagar várias de uma vez (vinheta: BAIXA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t13/apos-cap09b`), aba "A Pagar"; na busca digita "pneus": as três parcelas. | E quando um Pix só paga várias contas? A Recicla Vale vai adiantar duas parcelas dos pneus de uma vez. |
| Marca a caixinha das parcelas 1 e 2: no rodapé, a barra "2 linhas selecionadas", "Total: R$ 4.720,00", "Limpar" e "Quitar em lote". [ZOOM: a barra] | Marco a caixinha das duas. Embaixo aparece uma barra com duas linhas selecionadas e o total: quatro mil setecentos e vinte reais. |
| Clique em "Quitar em lote": janela "Pagar 2 linhas em 1 lançamento", "Total R$ 4.720,00 — vira um único lançamento, que casa 1-pra-1 na conciliação bancária.". | Clico em Quitar em lote. As duas viram um lançamento só, do jeito que vai aparecer no extrato do banco. |
| Em "Forma de pagamento" escolhe Pix e a "Conta Principal"; a câmera passa por "Descrição do lançamento" ("Pagamento agrupado: Auto Peças Vale Forte (2 linhas)") e "Data do pagamento" 10/11/2026; "Confirmar pagamento". [BACKEND: rpc do lote (`pay_financial_bills_batch`): duas `bill_payments` com o mesmo `group_id` e uma saída em `bank_transactions`] [TESTAR: texto do aviso de sucesso] | Escolho o Pix, a Conta Principal, confiro a descrição do lançamento e a data, e confirmo. |
| A lista: parcelas 1 e 2 "Paga", a 3 "Pendente". | Pronto: as duas parcelas estão pagas, com um único lançamento no banco. |
| A câmera fica na lista. | Uma dica: junte contas da mesma categoria. Com categorias diferentes, o pagamento entra no relatório sem categoria, e a tela avisa antes. |
| (sem ação) | E dá pra marcar linha de saldo também: o fiado entra no lote, e você ainda escolhe quanto abater de cada um. |

Mundo: handler do lote. **Cria um Pix de R$ 4.720,00 em 10/11** (T14 e T15). A seleção trava numa direção só (a
primeira linha marcada decide): o robô marca só contas a pagar.

### cap09d · Desfazer uma baixa (vinheta: BAIXA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t13/apos-cap09c`); na busca digita "pneu da": a linha "Conserto do pneu da empilhadeira", "Paga"; clique em "Mais ações" (três pontinhos) → "Estornar pagamento". | Deu baixa na conta errada? Dá pra desfazer. Na conta paga, clico em Mais ações e em Estornar pagamento. |
| Janela "Estornar pagamento": "Saiu de" Conta Principal e "Voltam R$ 180,00 para Conta Principal". [ZOOM: a frase "Voltam R$ 180,00 para ..."] [TESTAR: texto exato do nome da origem] | A tela mostra de onde o dinheiro saiu e avisa que ele volta pra lá: os cento e oitenta reais voltam pra Conta Principal, e a conta fica pendente de novo. |
| "Cancelar"; clique na lixeira da mesma linha: "Excluir conta?", "Excluir devolve R$ 180,00 para ..." e o botão "Excluir e estornar"; "Cancelar". | Excluir uma conta paga faz o mesmo caminho: o botão vira Excluir e estornar, e o dinheiro volta antes de a conta sumir. |
| A câmera fica na linha. | Uma dica: se o pagamento já foi conciliado com o extrato do banco, desfaça a conciliação primeiro. Aqui eu só cancelo. |

Mundo: `bill_payments` do conserto do pneu legível (select com `bank_account` e `cash_register`), já criado no cap05.
Nenhum dado muda (o robô cancela).

### cap12b · Exportar a lista (vinheta: FILTROS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t13/apos-cap11`); clique em "Exportar": menu "Exportar contas", com "PDF" e "Excel"; clique em "PDF". | Precisa mandar essa lista pro contador ou imprimir? O botão Exportar gera um PDF ou uma planilha do Excel. |
| Janela "Exportar contas (PDF)", "Escolha o que entra no arquivo. Os filtros já vêm com o que você está usando na tela."; a câmera desce pelo bloco "Filtros". | A janela já vem com os filtros que você está usando na tela, e dá pra mudar ali mesmo. |
| Bloco "Opções do arquivo": "Fiado / saldo de cliente e fornecedor" e "Agrupar por" ("Nenhum", "Status", "Categoria", "Mês"). [ZOOM: o bloco] | Em Opções do arquivo, você escolhe se o saldo dos clientes e fornecedores entra, e como agrupar: por status, por categoria ou por mês. |
| Fecha a janela (Esc). | Aqui eu só fecho. |

Mundo: nada novo (o PDF não é gerado; a permissão de exportar o MASTER já tem).

### cap13 · Recapitulando
Acrescentar três falas: "Deixou o sistema preencher a internet do escritório pelo padrão." / "Pagou o aluguel da
empilhadeira pelo valor real do mês e duas parcelas dos pneus num lançamento só." / "E viu como estornar uma baixa e
exportar a lista." Trocar "desta e das futuras" por "desta e das próximas" e incluir as parcelas ("e fez o mesmo nas
parcelas dos pneus").

## 4. Estimativa

| Bloco | Palavras | Segundos de fala |
|---|---|---|
| cap05b Preenchimento inteligente | ~195 | ~75 |
| cap08b Parcelas em grupo | ~125 | ~48 |
| cap09b Valor real do mês | ~185 | ~71 |
| cap09c Pagamento em lote | ~135 | ~52 |
| cap09d Estorno | ~92 | ~35 |
| cap12b Exportar | ~65 | ~25 |
| Trechos (cap01, cap02, cap04, cap09, cap12) e cap13 | ~260 | ~100 |
| **Total** | **~1.055** | **~405 s (6,8 min)** |

Seis capítulos novos e três trechos. A aula sai de ~14,5 min para ~22 min de vídeo (com as vinhetas novas).

## Depende de decisão
1. **Tamanho**: 22 min numa aula só, ou dividir em duas (lançar · dar baixa e conferir).
2. **Dinheiro novo no mundo**: cap09b (Pix de R$ 2.415,00) e cap09c (Pix de R$ 4.720,00) mexem no extrato da T14 e na DRE
   da T15. Alternativa sem impacto: o robô mostra a janela e cancela (perde o "pronto, ficou paga").
3. **Trecho da água com multa**: proposto cancelando. Se for para confirmar, a água sai de "Vencida" e os cartões e o
   cap12 mudam; em dinheiro exige caixa aberto.
4. **Dados novos**: fornecedor "Vale Fibra Telecom Ltda", categoria "Internet e telefone" e as duas contas pagas de
   setembro e outubro (entram no histórico e na DRE desses meses).
5. **Para o `MELHORIAS_ECOSISTEMA.md`** (achados do app, não da aula): o botão diz "Esta e as próximas" mas o aviso e o
   toast ainda dizem "futuras"; conta com previsto "Boleto" ou "Cheque" abre a baixa em "Dinheiro" em vez da conta
   prevista (`PayBillModal.tsx:146-150`); "Esta e as próximas" numa parcela iguala o valor de todas as do escopo ao da
   parcela editada (`update_installment_bill_group`).
