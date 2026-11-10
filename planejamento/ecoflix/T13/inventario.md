# Inventário · T13 Contas a Pagar e Receber (EcoSistema 1.59.154)

Levantado em 10/11/2026 contra `/home/claude/ecoflix/app-src-1.59.154/` (análise estática, só leitura). Caminhos relativos
a `src/`. Rótulo entre aspas = texto exato da tela. Só o que a aula usa. Não há `supabase/migrations` na cópia: o que as
RPCs fazem por dentro vem dos comentários do front e da fonte (conferida pela equipe), e o backend falso precisa simular.

## 0. Rota, menu e permissão
- Rota `/contas-pagar-receber` (`App.tsx:562-566`), permissão `screen_contas_pagar_receber`.
- Menu lateral: "Financeiro" → "Contas a Pagar/Receber" (`config/routes.ts:413-425`, item `:423`). O grupo "Financeiro"
  tem ainda "Caixa", "Histórico do Caixa", "Movimentações Bancárias", "Relatório Financeiro", "Categorias Financeiras".
- Quem vê a tela opera: criar, dar baixa e recorrência pedem só a permissão da tela (`pages/ContasPagarReceber.tsx:170-177`).
  "Excluir" pede `action_delete_bill`; o interruptor "Repete?" pede `action_manage_recurring`
  (`components/contas/BillFormModal.tsx:196,1309`). Rafael Nogueira (MASTER, full_access) tem tudo.
- Não é módulo pago (Fase 1).

## 1. A tela (`pages/ContasPagarReceber.tsx`)
- Caminho no topo: "Financeiro" › "Contas a Pagar/Receber"; título "Contas a Pagar/Receber"; botão "Nova conta" (`:1019-1035`).
- Abas "Todas" (abre por padrão), "A Pagar" (vermelha), "A Receber" (`:149-153`, `:1060-1086`).
- Busca: "Buscar por valor, descrição ou parceiro..." (`:999-1014`).
- Visão: "Lista" e "Calendário" (`:1090-1111`); "Exportar" (PDF/Excel, fora da aula) (`:1113-1148`).
- "Filtros" (painel lateral, título "Filtros", `:1150-1334`): "Status" (opções "Projetada", "Pendente", "Vencida", "Parcial",
  "Paga", `:155-161`), "Categoria" (só as que aparecem nas contas), "Cliente/Fornecedor" (busca "Buscar parceiro...",
  grupos Clientes e Fornecedores, "Todos"), "Centro de custo", "Banco previsto" (só com permissão bancária),
  "Vencimento (período)" com "De" e "Até"; rodapé "Limpar filtros" (só ativo com filtro ligado) e "Aplicar".
  Com filtro ligado, o botão "Filtros" fica verde com o número de filtros (`:702-709`, `:1150-1167`).
- Avisos que trocam uma seção escondida por uma linha (`:1344-1359`): faturas de cartão escondidas pelo filtro e
  "1 conta sem vencimento não aparece com o filtro de período ligado." (`lib/contasBillsFilter.ts:705-709`).
- "Faturas de Cartão" (`:1367-1428`): só com cartão cadastrado. O mundo não tem cartão: a seção não aparece.
- Ao abrir a tela: `rpc generate_due_recurring_bills` (completa a janela das recorrências, `:425-438`).

## 2. Os quatro cartões (`components/contas/BillsSummaryCards.tsx:97-138,178-211`; conta em `lib/contasBillsCurrency.ts:139-177`)
- "Total a Pagar" (rosa), "Total a Receber" (verde), "Vencidas" (vermelho), "Vence em 7 dias" (laranja).
- Somam a empresa inteira, ignorando aba e filtros (`hooks/useBills.ts:537-557`). Conta parcial entra pelo que falta.
- "Total a Pagar" e "Total a Receber" somam contas abertas + saldo (fiado) já sem a parte que virou título.
- "Vencidas" e "Vence em 7 dias" somam só contas (os dois lados, pagar e receber); "Vence em 7 dias" = de hoje até
  hoje + 7, contando hoje, sem as vencidas.

## 3. A lista (`components/contas/BillsList.tsx`)
- Colunas (computador): "Descrição", "Categoria", "Emissão", "Vencimento", "Valor", "Status", "Quitada em" (na aba
  "A Pagar": "Paga em"; na "A Receber": "Recebida em", `:173-177`), "Ações" (`:942-985`). Paginação de 10.
- Status (`:141-149`): "Pendente" (cinza), "Vencida" (vermelho; o vencimento vira selo vermelho, `:278-291`), "Parcial"
  (âmbar; o valor mostra "pago R$ X de R$ Y", `:302-316`), "Paga" (verde), "Projetada" (azul, folha; fora da aula).
- Etiqueta do pagamento previsto ao lado da categoria: "Dinheiro" ou o nome da conta bancária (`:231-276`).
- Conta sem vencimento: "Sem vencimento" (`:279-281`).
- Ações da conta (`:1104-1141`): "Marcar pago" (a pagar) ou "Receber" (a receber), verde, some na "Paga"; lápis
  "Editar"; lixeira "Excluir"; com baixa feita, "Mais ações" → "Estornar pagamento" (`:589-617`).
- Linha de saldo (fiado) (`:990-1046`): nome do parceiro (clicável, abre o histórico dele) com "Cliente" ou "Fornecedor"
  embaixo; traço em Categoria, Emissão e Vencimento; o valor; chip roxo "Saldo" (`:214-221`); botão "Receber" ou "Pagar".
  O fiado vem antes das contas (`lib/contasBillsFilter.ts:652-653`).
- Excluir conta avulsa sem baixa: "Excluir conta?" / "A conta "<descrição>" será removida permanentemente. Esta ação não
  pode ser desfeita." / "Cancelar" e "Excluir" (`:634-661`).
- Conta de recorrência, ao clicar em "Editar" ou "Excluir" (`:546-582`, `:663-711`): "Editar conta recorrente" (ou "Excluir
  conta recorrente"), ""<descrição>" faz parte de uma recorrência. O que deseja editar?" (ou "excluir?"), botões
  "Só esta conta", "Esta e as futuras" e "Cancelar".
- Lista vazia: "Nenhuma conta por aqui" / "Crie uma nova conta a pagar ou a receber para começar."; com filtro:
  "Nenhuma conta encontrada" (`:723-739`).

## 4. Calendário (`components/contas/BillsCalendar.tsx`)
- Aviso no topo: "Saldos de clientes/fornecedores não têm vencimento — veja na visão de Lista." (`:126-131`).
- Mês com seletor, "Hoje", "Mês anterior", "Próximo mês" (`:135-177`); dias "Dom" a "Sáb" (`:43`).
- Cada dia: etiquetas com a descrição (vermelha a pagar, verde a receber), "+N" quando passa de 3, totais do dia embaixo,
  triângulo quando há vencida (`:198-284`).
- Clique no dia: "Contas de dd/mm/aaaa", "N contas"; cada conta com "A Pagar"/"A Receber", valor que falta,
  "Vencida" quando for o caso, "Marcar pago" (ou "Receber") e "Editar" (`:289-379`).

## 5. Nova conta / Editar conta (`components/contas/BillFormModal.tsx`)
- Título "Nova conta", "Cadastre uma conta a pagar ou a receber com vencimento." (edição: "Editar conta", "Altere os dados
  da conta.") (`:849-857`). Rodapé "Cancelar" e "Criar conta" (edição: "Salvar") (`:828-845`).
- Bloco "O que é" (`:864-1135`): "Tipo" ("A pagar (despesa)" / "A receber (receita)"; vem da aba; em "Todas", a pagar,
  `pages/ContasPagarReceber.tsx:1492`), "Valor", "Descrição" ("Ex: Aluguel do galpão"), "Vencimento" (vem com hoje;
  calendário), "Categoria" ("Selecione a categoria", busca "Pesquisar categoria...", "+" cria; só despesa na conta a
  pagar e receita na a receber, `:281-282`), "Cliente / Fornecedor" (tipo "Nenhum"/"Cliente"/"Fornecedor", pré-seleção
  pela direção, `:161-168`; depois "Selecione o fornecedor", busca "Pesquisar fornecedor...", "+" cria), "Centro de custo"
  (aqui só quando a empresa tem centro ativo, `:192-195,795-807,1134`; opção "— Nenhum —").
- Bloco "Dinheiro" (`:1141-1240`): "Pagamento previsto" (`components/financial/PaymentSourceSelect.tsx`: "Não definido",
  grupo "Dinheiro" com "Dinheiro (Caixa)", grupo "Contas" com as contas; conta sem código de banco = ícone genérico).
  Só ao criar: "Já paguei essa conta" (a receber: "Já recebi essa conta"), "Registra o pagamento agora — a conta já nasce
  quitada.", com "Data do pagamento"; avisos "Escolha de onde sai o dinheiro no campo acima." e "Abra um caixa para pagar
  em dinheiro." (`:1160-1216`). "Pendurar no saldo do fornecedor (pagar depois)" só sem vencimento (fora da aula).
- Bloco "Mais detalhes" (recolhido; abre sozinho se já tem conteúdo) (`:1243-1283`): "Centro de custo" (só sem centro
  ativo), "Observações" ("Observação opcional"), anexos (`components/financial/TransactionAttachmentsField.tsx`: "Anexos (foto
  ou PDF)", botão "Anexar", "Nenhum anexo.", miniatura com "PDF", "Ver anexo"/"Baixar anexo", "Remover anexo"; 5 MB e 5
  arquivos; na edição o arquivo sobe na hora, `:355-419`; ao criar, sobe depois de gravar a conta).
- Bloco "Parcelar ou repetir" (recolhido; só ao criar) (`:1287-1317`):
  - "Parcelar" (`components/contas/InstallmentToggleSection.tsx:72-101`): ligar abre "Configurar faturamento"
    (`components/InstallmentsConfigDialog.tsx:239-394`): "Parcelar R$ X do saldo", "Condição de pagamento" ("Manual
    (definir parcelas)" + as cadastradas), "Nº de parcelas" (1, 2, 3, 4, 6, 12: divide igual, 1ª no vencimento e as
    outras +1 mês), linhas data + "R$" valor, "Adicionar parcela", faixa "Soma das parcelas" (verde quando fecha),
    "Total do saldo: R$ X. A última parcela absorve os centavos para fechar a soma.", "Limpar faturamento" e "Aplicar
    faturamento". Resumo no bloco: "4x — 1º venc. 20/11/2026 — total R$ 4.720,00" e botão "Editar".
  - "Repete?" (`components/contas/RecurrenceFields.tsx:103-180`): "Gera contas automaticamente na frequência escolhida.";
    "Frequência" ("Semanal", "Mensal", "Anual"; padrão Mensal), "A cada" (padrão 1), "Repetir até (opcional)", "Deixe vazio
    para repetir sem data-fim.". Ligar um desliga o outro (`BillFormModal.tsx:425-434,1296-1300`). Com "Repete?" ligado o
    campo de anexos some (`:1272`).
- Edição "Esta e as futuras": embaixo do vencimento, "Esta data e as futuras serão deslocadas pelo mesmo período."
  (`:923-927`).
- Toasts: "Informe a descrição da conta", "Informe um valor válido", "Selecione uma categoria", "Informe a data de
  vencimento", "Configure as parcelas antes de salvar" (`:483-561`); "Conta criada", "Conta criada e paga" (`:717-723`),
  "4 parcelas criadas" (`:664`), "Conta recorrente criada" (`:686`), "Conta atualizada" (`:648`); "Anexos não são
  suportados em parcelamento..." e "...em conta recorrente..." (`:667,690`).
- Aviso de conta igual (só conta única com parceiro): "Conta igual já cadastrada" / "Salvar mesmo assim" (`:591-641,1358-1419`).
  Os dados da aula não repetem parceiro + vencimento + valor, então ele não abre.
- Edição de conta que veio de pedido: valor e parceiro travados, "Esta conta veio de um pedido; para mudar o valor, edite o
  pedido" (`hooks/useBills.ts:662-705`). Descrição, vencimento, categoria, centro de custo e observação livres.
- Parcelamento e recorrência não levam centro de custo (`hooks/useBills.ts:60-72,79-97`).

## 6. Dar baixa (`components/contas/PayBillModal.tsx`)
- Abre por "Marcar pago"/"Receber". Título "Pagar conta" (ou "Receber conta"), subtítulo "<descrição> · Restante R$ X"
  (`:709-713`). Rodapé "Cancelar" e "Confirmar pagamento" (ou "Confirmar recebimento").
- Ao abrir (`:136-162`): forma = Pix com a conta prevista se o previsto for conta bancária; senão "Dinheiro". Valor =
  restante. Data = hoje. Novo vencimento do restante = vencimento atual.
- "Múltiplas formas de pagamento" (interruptor, fora da aula), "Forma de pagamento", cartões "Dinheiro",
  "Pix/Transferência", "Saldo da ficha" (este só com parceiro) (`:338-351,420-424,788-808`); campo do valor; com Pix,
  "Conta bancária" (`:835-853`).
- Caixa fechado com "Dinheiro" marcado: aviso âmbar "O caixa está fechado. Abra o caixa para registrar a parte em
  dinheiro." (`:864-871`). Sem permissão bancária: aviso âmbar "Sua conta não tem permissão para movimentar contas
  bancárias. Este pagamento será registrado como Dinheiro (Caixa). ..." (`:776-786`).
- Resumo: "Total informado: R$ X" e "Quita a conta", "Falta R$ X para quitar" ou "Sobra R$ X → vira crédito de <parceiro>"
  (`:894-910`).
- "Data do pagamento"; no parcial, "Novo vencimento do restante" e "O saldo de R$ X continuará em aberto com este
  vencimento." (`:914-944`); "Juros / multa (opcional)" (só a pagar), "Tarifa (opcional)", "Observação (opcional)",
  "Comprovante (foto ou PDF)" (`:949-1028`). O comprovante da baixa fica na conta e também no lançamento do caixa ou do
  banco que a baixa criou (`:447-499,599-631`).
- Toasts: "Pagamento registrado" / "Recebimento registrado" (`:633`); "O caixa está fechado. Abra o caixa para registrar o
  pagamento." (`:651-653`); "Informe a nova data de vencimento do restante" (`:702`).
- Depois: status "Paga" ou "Parcial" ("pago R$ X de R$ Y") com o vencimento novo.

## 7. Baixa do fiado (`components/contas/PayFiadoModal.tsx`)
- Título "Receber de <parceiro>" (ou "Pagar a <parceiro>"), "Saldo em aberto R$ X" (`:325-330`).
- "Forma de recebimento": "Dinheiro (Caixa)" (padrão) ou "Pix / Transferência (Banco)"; com Pix, "Conta bancária"
  (`:364-402`). "Valor" vem com o saldo inteiro e aceita menos; "Saldo após esta baixa: R$ X" (`:405-419`).
  "Data do recebimento" (`:422-433`). Categoria (opcional) só no pagamento a fornecedor (`:436-522`).
  "Comprovante (foto ou PDF)" (`:529-535`). Sem tarifa, sem observação, sem novo vencimento.
- "Confirmar recebimento"; toast "Recebimento registrado" (`:278`); "O valor não pode exceder o saldo em aberto (R$ X)" (`:319`).

## 8. Regras do fiado na lista (`lib/contasBillsFilter.ts`)
- Venda ou compra a prazo com parcelas (títulos com `order_id`) e o saldo do parceiro guardam o mesmo dinheiro: a linha
  de saldo mostra só o que sobra depois de descontar os títulos abertos daquele parceiro; se tudo virou título, ela não
  aparece (`:369-453,636-650`).
- Com filtro de "Status", "Vencimento (período)", "Categoria", "Centro de custo" ou "Banco previsto" ligado, as linhas de
  saldo saem da lista; aba, parceiro e busca elas respondem (`:550-588`).
- Calendário: só contas, sem saldo (`pages/ContasPagarReceber.tsx:489-495`).

## 9. Backend que a tela chama (`hooks/useBills.ts` e vizinhos)
| Ação | Chamada |
|---|---|
| Listar contas | `financial_bills` select `*, category:financial_categories(...)` por empresa, paginado (`:336-343`); nomes em `customers` e `suppliers` (`:361-375`) |
| Saldos (fiado) | `balances` (`entity_type, entity_id, balance, currency`, `balance != 0`) (`:410-419`); `suppliers.linked_customer_id` (`:485-489`) |
| Janela das recorrências | `rpc generate_due_recurring_bills` (página `:431`) |
| Data de emissão | `rpc get_financial_bill_origin_dates` (`hooks/useBillOriginDates.ts:27`) |
| Opções | `financial_categories` (`hooks/useFinancialCategories.ts:91`), `cost_centers` (`hooks/useCostCenters.ts:40`), `bank_accounts` + `rpc get_usable_bank_accounts` (`hooks/useBankAccounts.ts:89,168`), `payment_conditions` (`hooks/usePaymentConditions.ts:56`), `customers`/`suppliers` (página `:458-473` e busca do formulário) |
| Criar conta | `financial_bills` insert (`:583-601`) |
| Já paguei | o insert acima + `rpc pay_financial_bill` (`BillFormModal.tsx:696-716`) |
| Parcelar | `rpc create_installment_bills` (`:614-628`) |
| Repetir | `rpc create_recurring_bill_template` (cria o molde e as contas da janela de 3 meses) (`:970-985`) |
| Editar só esta | `financial_bills` update (`:723-728`) |
| Editar esta e as futuras | `recurring_bill_templates` update, `financial_bills` update (futuras não pagas), `rpc shift_recurring_bills_due_date` se o vencimento mudou (`:1137-1163`) |
| Excluir | `rpc delete_financial_bill_cascade` (`:760-763`); esta e as futuras: `recurring_bill_templates` update `is_active=false` + delete das futuras sem baixa (`:1014-1052`) |
| Dar baixa | `cash_register` aberto (`PayBillModal.tsx:218-247`); `rpc pay_financial_bill` (`useBills.ts:789-806`, parâmetros `:202-217`) |
| Baixa do fiado | `rpc pay_partner_balance` (`:940-960`) |
| Anexos | bucket `financial-attachments` (upload e `createSignedUrls`) e tabela `transaction_attachments` (`hooks/useTransactionAttachments.ts:19,63,222-317`) |

Pela fonte (conferida pela equipe): a baixa em dinheiro lança um movimento no caixa aberto, a baixa por Pix lança na conta
bancária, o lançamento herda a categoria da conta (por isso aparece na DRE) e tudo acontece junto ou nada é gravado.
