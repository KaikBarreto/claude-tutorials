# Plano · T13 Contas a Pagar e Receber

- **Título:** Contas a Pagar e Receber (o da fonte).
- **Objetivo:** tirar as contas da Recicla Vale Metais da gaveta: lançar com data, categoria e dono; parcelar; repetir;
  dar baixa total e parcial; entender o fiado na mesma lista; anexar o comprovante; filtrar.
- **Antes:** T10 "Estoque: saldo, histórico e posição". **Próximo:** T14 "Bancos, cofre e conciliação bancária"
  (fonte: "fazer o extrato do banco bater com o sistema").
- **Vinhetas (áreas):** CONTAS · LANÇAMENTO · RECORRÊNCIA · BAIXA · FIADO · COMPROVANTE · FILTROS · RESUMO.
- **Alvo da fonte:** ~16 min. Estimativa: ~2.100 palavras de fala (~13,5 min) + 13 vinhetas, ilustrações e as esperas dos
  formulários (acelerados sem fala) ≈ 15 a 16 min.
- Base: `T13/inventario.md` (código 1.59.154). Sem 🔒 (Fase 1) e sem 🚫 na fonte desta aula.
- **FAKE_NOW:** `2026-11-10T08:30:00-03:00` (terça) em todos os capítulos. Desktop, Rafael Nogueira (MASTER) logado.

## Capítulos (os da fonte, na ordem)

| # | Vinheta (área / título) | O que a tela mostra | ⚠️ e ilustração | Estado de partida |
|---|---|---|---|---|
| 0 | (abertura) | Dashboard → menu "Financeiro" → "Contas a Pagar/Receber". Cartão "Antes". | [ILUSTRAÇÃO: as contas espalhadas viram uma lista com data] | `inicio` |
| 1 | CONTAS / A tela e as abas | Abas "Todas", "A Pagar", "A Receber"; colunas; status "Vencida", "Pendente", "Paga"; botão "Nova conta". | | `inicio` |
| 2 | CONTAS / Os quatro cartões | "Total a Pagar", "Total a Receber", "Vencidas", "Vence em 7 dias"; a água vencida e a energia de hoje. | [ILUSTRAÇÃO: linha do tempo vencidas × próximos 7 dias]; cartões = empresa inteira (dito aqui, dica no 12) | `inicio` |
| 3 | CONTAS / Lista e calendário | "Calendário": novembro; dia 5 com triângulo; clique no dia 10 ("Contas de 10/11/2026"); volta a "Lista". | ⚠️ calendário sem saldo (aviso na tela) | `inicio` |
| 4 | LANÇAMENTO / Lançar uma conta | "Nova conta": manutenção da prensa (Hidráulica Moretti), R$ 3.480,00, vence 19/11, "Manutenção de máquinas", "Pátio", previsto "Conta Principal". | | `inicio` |
| 5 | LANÇAMENTO / A conta que já nasce paga | "Já paguei essa conta": conserto do pneu da empilhadeira, R$ 180,00, pago ontem por Pix. | | `apos-cap04` |
| 6 | LANÇAMENTO / Parcelar uma conta | Pneus do caminhão truck, Auto Peças Vale Forte, R$ 7.080,00 em 3x de R$ 2.360,00 ("Configurar faturamento"). | [ILUSTRAÇÃO: uma compra vira três contas; parcelar × repetir] | `apos-cap05` |
| 7 | RECORRÊNCIA / A conta que se repete | "Repete?": aluguel da empilhadeira, R$ 2.300,00, mensal, dia 12, até 12/04/2027. | [ILUSTRAÇÃO: o molde e a janela de três meses] | `apos-cap06` |
| 8 | RECORRÊNCIA / Só esta ou esta e as futuras | Editar a de dezembro: "Esta e as futuras", vencimento 12/12 → 15/12 (dezembro e janeiro mudam); diálogo de excluir mostrado e cancelado. | [ILUSTRAÇÃO: só esta × esta e as futuras] | `apos-cap07` |
| 9 | BAIXA / Dar baixa | Energia R$ 1.874,30 inteira por Pix; manutenção da prensa: R$ 1.740,00 agora e o resto para 30/11 ("Parcial"). | ⚠️ baixa mexe em dinheiro (dica) + [ILUSTRAÇÃO: o caminho do dinheiro]; ⚠️ sem permissão bancária (dica) | `apos-cap08` |
| 10 | FIADO / O fiado na mesma lista | Aba "A Receber", busca "Quiririm": linha "Saldo" R$ 3.150,00 → "Receber" R$ 2.000,00 por Pix, sobra R$ 1.150,00; busca "Fundição": só as três parcelas. | ⚠️ fiado some quando vira parcela (dica) + [ILUSTRAÇÃO: fiado parcelado]; ⚠️ título de pedido (dica) | `apos-cap09` |
| 11 | COMPROVANTE / Anexar o comprovante | Energia paga → "Editar" → "Mais detalhes" → "Anexar" o PDF do Pix → "Salvar"; reabre e o PDF está lá. | dica: comprovante na hora da baixa vai também para o lançamento do banco ou do caixa | `apos-cap10` |
| 12 | FILTROS / Filtrar a lista | "Filtros": "Status" "Pendente" + "Cliente/Fornecedor" "Auto Peças Vale Forte" → as três parcelas dos pneus; passa por "Categoria", "Centro de custo", "Vencimento (período)"; "Limpar filtros". | ⚠️ cartões não mudam (dica); ⚠️ saldo sai com filtro (dica) | `apos-cap11` |
| 13 | RESUMO / Recapitulando | Montagem dos capítulos; cartão "Próximo". | | (montagem) |

Transições faladas: 0→1 "Vamos à tela"; 1→2 "Antes da lista, os cartões lá de cima"; 2→3 "E dá pra ver as mesmas contas
num calendário"; 3→4 "Agora, lançar uma conta nova"; 4→5 "E quando a conta chega já paga?"; 5→6 "Agora uma compra
dividida em vezes"; 6→7 "E a conta que volta todo mês?"; 7→8 "E se uma delas mudar?"; 8→9 "Chegou a hora de pagar";
9→10 "Agora, o fiado"; 10→11 "E o comprovante daquele Pix da energia?"; 11→12 "Com a lista cheia, os filtros"; 12→13
"Recapitulando".

## Falas dos cuidados ⚠️ (fonte → aula)
| ⚠️ da fonte | Onde | Fala (resumo) |
|---|---|---|
| Dar baixa mexe em dinheiro de verdade; herda a categoria; tudo ou nada | cap09 | "Uma dica: dar baixa mexe em dinheiro de verdade..." + ilustração |
| Cartões = empresa inteira | cap02 (informação) e cap12 ("Uma dica:") | "os quatro cartões não mudam com o filtro" |
| Por que o fiado às vezes some da lista | cap10 | "Uma dica: se o saldo de um cliente sumir da lista, olha se a venda foi parcelada" + ilustração |
| Fiado sai com filtro de status, período, categoria, centro de custo, banco previsto | cap12 | "Uma dica: ... é só limpar os filtros" |
| Calendário só com contas que vencem | cap03 | "Uma dica: o saldo não tem vencimento, então não entra no calendário" (aviso na tela) |
| Título de pedido não muda valor nem parceiro aqui | cap10 | "Uma dica: essas parcelas vieram do pedido de venda..." |
| Sem permissão bancária: só dinheiro, aviso amarelo | cap09 | "Uma dica: quem não tem permissão de banco..." |
| Em Despesas, o segundo valor da linha de cartão é subtotal | fora | O mundo não tem cartão e a aula não abre a aba Despesas (Relatório Financeiro). Fica para o T14/T15 (relatório). |
Nenhuma mensagem de erro encenada: todas as baixas dão certo; os avisos são falados como informação.

## Mundo: o que esta aula precisa
Além do `MUNDO_FICTICIO.md` (proposta; nomes de parceiro novos a conferir na semente):
- **Contas bancárias:** "Conta Principal" e "Conta Secundária", **sem código de banco** (o app mostra o ícone genérico, sem
  logo de terceiros); o cofre (Conta Dinheiro, R$ 18.500,00) fica fora da lista do Pix.
- **Centros de custo ativos:** "Pátio", "Escritório", "Frota" (com centro ativo o campo aparece no bloco "O que é").
- **Categorias de despesa:** "Energia elétrica", "Água e esgoto", "Aluguel", "Manutenção de máquinas", "Manutenção de
  veículos", mais as de sistema "Tarifas" e "Juros e Multas". **Receita:** "Venda de sucata" (a das vendas).
- **Fornecedor novo:** Hidráulica Moretti Ltda, PJ, CNPJ 41.739.625/0001-57, Taubaté, SP, contato@hidraulicamoretti.example,
  (12) 9 0000-3131 (manutenção da prensa enfardadeira).
- **Contas no início (financial_bills):**
  | Descrição | Tipo | Valor | Vencimento | Situação | Categoria · centro · previsto | Parceiro |
  |---|---|---|---|---|---|---|
  | Água e esgoto de outubro | a pagar | R$ 238,40 | 05/11/2026 | pendente (aparece "Vencida") | Água e esgoto · Escritório · nenhum | nenhum |
  | Aluguel do galpão de novembro | a pagar | R$ 6.800,00 | 05/11/2026 | paga em 05/11 por Pix (Conta Principal) | Aluguel · Pátio · Conta Principal | nenhum |
  | Energia elétrica de outubro | a pagar | R$ 1.874,30 | 10/11/2026 | pendente | Energia elétrica · Pátio · Pix Conta Principal | nenhum |
  | 3 parcelas do pedido de venda à Fundição | a receber | R$ 4.790,00 cada | 17/11/2026, 17/12/2026, 18/01/2027 | pendentes, com `order_id` | Venda de sucata | Fundição Bandeira do Vale |
- **Pedido da Fundição:** venda de 300 kg de cobre mel a R$ 47,90 = R$ 14.370,00 em 03/11/2026, a prazo em 3x; saldo da
  Fundição em `balances` (customer) +14.370,00 (todo itemizado nas parcelas: a linha de saldo não aparece).
- **Fiado da Aços Quiririm:** venda de 3.000 kg de ferro misto a R$ 1,05 = R$ 3.150,00 em 06/11/2026, a prazo sem parcelas;
  `balances` (customer) +3.150,00 e nenhum título.
- Outras contas e saldos do mundo (histórico pago de agosto a outubro, os saldos do T4) podem aparecer: a fala não depende
  deles; o robô usa a busca para isolar as linhas.
- **Esta aula cria:** a manutenção da prensa (Hidráulica Moretti, R$ 3.480,00, 19/11 → depois parcial, R$ 1.740,00 pagos
  e o resto para 30/11); o conserto do pneu da empilhadeira (R$ 180,00, pago em 09/11 por Pix); os pneus do caminhão
  truck (Auto Peças Vale Forte, 3x R$ 2.360,00: 23/11/2026, 23/12/2026, 23/01/2027); a recorrência "Aluguel da
  empilhadeira" (R$ 2.300,00, mensal, 12/11/2026 até 12/04/2027; dezembro e janeiro passam para 15/12 e 15/01); a baixa da
  energia (Pix, 10/11, com o PDF "comprovante-pix-energia-outubro.pdf" anexado, fictício); a baixa de R$ 2.000,00 no
  saldo da Aços Quiririm (sobra R$ 1.150,00). Atualizar o `MUNDO_FICTICIO.md` (o T14 concilia esses Pix com o extrato).

## Gravação
- **Rotas:** `/dashboard` (só no cap00), `/contas-pagar-receber`. Desktop, sem celular, sem página pública, um usuário só.
- **RPCs e tabelas a simular no backend falso:** `generate_due_recurring_bills` (no-op que devolve ok),
  `get_financial_bill_origin_dates`, `get_usable_bank_accounts`, `create_installment_bills`,
  `create_recurring_bill_template` (molde + contas da janela de 3 meses: 12/11, 12/12, 12/01),
  `shift_recurring_bills_due_date`, `pay_financial_bill` (grava `bill_payments`, lança em `bank_transactions` com a categoria
  da conta, atualiza `paid_amount`, `status`, `paid_at` e, no parcial, `due_date`), `pay_partner_balance` (baixa do saldo +
  lançamento no banco); `financial_bills` (select, insert, update, select com filtros do aviso de duplicidade), `balances`,
  `suppliers.linked_customer_id`, `recurring_bill_templates` (update), `financial_categories`, `cost_centers`,
  `bank_accounts`, `payment_conditions`, `transaction_attachments` e o bucket `financial-attachments` (upload e
  `createSignedUrls`).
- **Arquivo do comprovante:** `comprovante-pix-energia-outubro.pdf`, PDF fictício de uma página (o robô o entrega ao
  `input[type=file]` do "Anexar"); a câmera não abre o PDF (ele abriria em outra aba).
- **Ilustrações** (cenas HTML no estilo da marca, `docs/09-aula-ilustrada.md`): cap00 contas espalhadas → lista; cap02 linha do
  tempo; cap06 uma compra → três contas (parcelar × repetir); cap07 o molde e a janela de três meses; cap08 só esta × esta e
  as futuras; cap09 o caminho do dinheiro na baixa; cap10 o fiado parcelado.
- Datas pelo calendário do campo (desktop: botão + calendário). Formulários sem fala podem ser acelerados na edição.
- A tela não tem cartão de crédito no mundo: a seção "Faturas de Cartão" não aparece.
