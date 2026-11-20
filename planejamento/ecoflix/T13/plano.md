# Plano · T13 Contas a Pagar e Receber

- **Título:** Contas a Pagar e Receber (o da fonte).
- **Objetivo:** tirar as contas da Recicla Vale Metais da gaveta: lançar com data, categoria e dono; parcelar; repetir;
  dar baixa total e parcial; entender o fiado na mesma lista; anexar o comprovante; filtrar.
- **Antes:** T10 "Estoque: saldo, histórico e posição". **Próximo:** T14 "Bancos, cofre e conciliação bancária"
  (fonte: "fazer o extrato do banco bater com o sistema").
- **Vinhetas (áreas):** CONTAS · LANÇAMENTO · RECORRÊNCIA · BAIXA · FIADO · COMPROVANTE · FILTROS · RESUMO.
- **Alvo da fonte:** ~16 min. Estimativa 1.60.18: 3.076 palavras de fala (~19,7 min de voz, 1.951 antes) + vinhetas, cartela e as esperas dos
  formulários (acelerados sem fala) ≈ 22 min (a aula cresceu com os 6 capítulos novos; o alvo de 16 min foi estourado de propósito).
- Base: `T13/inventario.md` (código 1.60.18). Sem 🔒 (Fase 1) e sem 🚫 na fonte desta aula.
- **FAKE_NOW:** `2026-11-10T08:30:00-03:00` (terça) em todos os capítulos. Desktop, Rafael Nogueira (MASTER) logado.

## Capítulos (1.60.18: 20, na ordem; 6, 10, 12, 13, 14 e 18 são novos)

| # | Vinheta (área / título) | O que a tela mostra | ⚠️ e ilustração | Estado de partida |
|---|---|---|---|---|
| 0 | (abertura) | Dashboard → menu "Financeiro" → "Contas a Pagar/Receber". Cartão "Antes". | [ILUSTRAÇÃO: as contas espalhadas viram uma lista com data] | `inicio` |
| 1 | CONTAS / A tela e as abas | Abas; colunas; status; **novo:** dica do status ("Vencida há 5 dia(s)") e "Detalhes da conta" ao clicar na linha. | | `inicio` |
| 2 | CONTAS / Os quatro cartões | Cartões; **novo:** na aba A Pagar o 2º cartão vira "Total pago" e na A Receber "Total recebido"; cartões acompanham a lista. | [ILUSTRAÇÃO: vencidas × 7 dias] | `inicio` |
| 3 | CONTAS / Lista e calendário | Calendário de novembro, dia 5 com triângulo, dia 10; volta a "Lista". | ⚠️ calendário sem saldo | `inicio` |
| 4 | LANÇAMENTO / Lançar uma conta | Nova ordem: Descrição, Vencimento, Valor; manutenção da prensa R$ 3.480,00; **novo:** "Forma de pagamento" ao lado do previsto; dica do botão de mais e do aviso de conta igual. | | `inicio` |
| 5 | LANÇAMENTO / A conta que já nasce paga | "Já paguei essa conta": conserto do pneu R$ 180,00 (mesma ordem de campos). | | `apos-cap04` |
| **6** | LANÇAMENTO / O sistema preenche pra você | **Novo.** Descrição "Internet do escritório" → "Padrão encontrado" (Vale Fibra Telecom Ltda, Telefone e internet, Conta Principal, Boleto, "Usado 3 vezes") → "Preencher" → Valor 289,90, vencimento dia 15 → hover "Desfazer preenchimento". Lateral: não segue a cadeia. | só preenche campo vazio; vale na receita e no caixa/banco | `apos-cap05` + `internet` |
| 7 | LANÇAMENTO / Parcelar uma conta | Pneus do caminhão truck 3x R$ 2.360,00 (Descrição, Vencimento, Valor). | [ILUSTRAÇÃO: uma compra, três contas] | `apos-cap05` |
| 8 | RECORRÊNCIA / A conta que se repete | Aluguel da empilhadeira, R$ 2.300,00, mensal, até 12/04/2027. | [ILUSTRAÇÃO: o molde] | `apos-cap07` |
| 9 | RECORRÊNCIA / Só esta ou esta e as próximas | Editar a de dezembro: "Esta e as próximas", 12/12 → 15/12; excluir mostrado e cancelado. | [ILUSTRAÇÃO: só esta × esta e as próximas] | `apos-cap08` |
| **10** | LANÇAMENTO / E as parcelas? | **Novo.** Editar a parcela 2 dos pneus: "Só esta conta", "Esta e as próximas", "Todas as parcelas pendentes"; vencimento 28/12 (28/01 acompanha); excluir mostrado e cancelado. Lateral. | valor e campos vão para todas as escolhidas | `apos-cap09` |
| 11 | BAIXA / Dar baixa | Energia inteira por Pix; prensa parcial R$ 1.740,00 (resto 30/11); **novo:** a água vencida com "Juros / multa" 4,77, "Tarifa", "Múltiplas formas de pagamento" (cancela). | ⚠️ baixa mexe em dinheiro + [ILUSTRAÇÃO: o caminho do dinheiro]; sobra vira crédito do fornecedor | `apos-cap09` |
| **12** | BAIXA / O valor real do mês | **Novo.** "Marcar pago" no aluguel de novembro: "Valor desta ocorrência" 2.415,00; as próximas mantêm o previsto; Pix, Conta Secundária; dezembro segue R$ 2.300,00. | diferente de pagar em parte | `apos-cap11` |
| **13** | BAIXA / Pagar várias de uma vez | **Novo.** Marca as parcelas 1 e 2 dos pneus; barra "2 linhas selecionadas / Total: R$ 4.720,00"; "Quitar em lote"; Pix, Conta Secundária; um lançamento no banco. | mesma categoria; linha de saldo entra no lote + [ILUSTRAÇÃO: lote = um lançamento] | `apos-cap12` |
| **14** | BAIXA / Desfazer uma baixa | **Novo.** "Mais ações" → "Estornar pagamento" no conserto do pneu (R$ 180,00 voltam à Conta Principal); "Excluir e estornar"; cancela. Sem mudar o banco. | pagamento conciliado: desfazer a conciliação antes | `apos-cap13` |
| 15 | FIADO / O fiado na mesma lista | Aços Quiririm "Saldo" R$ 4.870,00 → Receber R$ 2.000,00; Fundição só nas parcelas. | ⚠️ fiado some quando vira parcela + [ILUSTRAÇÃO] | `apos-cap13` |
| 16 | COMPROVANTE / Anexar o comprovante | Energia paga → Editar → Mais detalhes → Anexar o PDF (**novo:** aviso "Anexo adicionado") → Salvar; reabre. | comprovante na baixa vai ao lançamento | `apos-cap15` |
| 17 | FILTROS / Filtrar a lista | Status Pendente, Cliente/Fornecedor; **novo:** os cartões mudam junto; atalhos de período e cartões "A receber no período" / "Recebido no período"; "Limpar filtros". | ⚠️ saldo sai com filtro | `apos-cap16` |
| **18** | FILTROS / Exportar a lista | **Novo.** "Exportar" → "PDF" → janela "Exportar contas" com os filtros da tela e "Opções do arquivo"; cancela. | | `apos-cap16` |
| 19 | RESUMO / Recapitulando | Montagem dos capítulos; cartão "Próximo". | | (montagem) |

Transições faladas: 0→1 "Vamos conhecer a tela"; 1→2 "Antes da lista, os cartões lá de cima"; 2→3 "E dá pra ver as mesmas
contas num calendário"; 3→4 "Agora, lançar uma conta nova"; 4→5 "E quando a conta chega já paga?"; 5→6 "Tem conta que
volta todo mês com os mesmos dados"; 6→7 "Agora uma compra dividida em vezes"; 7→8 (fim do 7, "o Repetir, que vem agora");
8→9 "E se uma delas mudar?"; 9→10 "As parcelas dos pneus funcionam parecido"; 10→11 "Chegou a hora de pagar"; 11→12 "Nem
toda conta que se repete vem sempre igual"; 12→13 "E quando um Pix só paga várias contas?"; 13→14 "Deu baixa na conta
errada?"; 14→15 "Agora, o fiado"; 15→16 "E o comprovante daquele Pix da energia?"; 16→17 "Com a lista cheia, os filtros";
17→18 "Precisa mandar essa lista pro contador ou imprimir?"; 18→19 "Recapitulando".

## Falas dos cuidados ⚠️ (fonte → aula)
| ⚠️ da fonte | Onde | Fala (resumo) |
|---|---|---|
| Dar baixa mexe em dinheiro de verdade; herda a categoria; tudo ou nada | cap11 | "Uma dica: dar baixa mexe em dinheiro de verdade..." + ilustração |
| Cartões = empresa inteira | cap02 ("Uma dica": acompanham a lista) | "os cartões acompanham o que está na lista" (1.60.18: mudam com busca e filtro) |
| Por que o fiado às vezes some da lista | cap15 | "Uma dica: se o saldo de um cliente sumir da lista, olha se a venda foi parcelada" + ilustração |
| Fiado sai com filtro de status, período, categoria, centro de custo, banco previsto | cap17 | "Uma dica: ... é só limpar os filtros" |
| Calendário só com contas que vencem | cap03 | "Uma dica: o saldo não tem vencimento, então não entra no calendário" (aviso na tela) |
| Título de pedido não muda valor nem parceiro aqui | cap15 | "Uma dica: essas parcelas vieram do pedido de venda..." |
| Sem permissão bancária: só dinheiro, aviso amarelo | cap11 | "Uma dica: quem não tem permissão de banco..." |
| Em Despesas, o segundo valor da linha de cartão é subtotal | fora | O mundo não tem cartão e a aula não abre a aba Despesas (Relatório Financeiro). Fica para o T14/T15 (relatório). |
Nenhuma mensagem de erro encenada: todas as baixas dão certo; os avisos são falados como informação.

## Mundo: o que esta aula precisa
Além do `MUNDO_FICTICIO.md` (proposta; nomes de parceiro novos a conferir na semente):
- **Contas bancárias:** "Conta Principal" e "Conta Secundária", **sem código de banco** (o app mostra o ícone genérico, sem
  logo de terceiros); o cofre (Conta Dinheiro, R$ 18.500,00) fica fora da lista do Pix.
- **Centros de custo ativos:** "Pátio", "Escritório", "Frota" (com centro ativo o campo aparece no bloco "O que é").
- **Categorias de despesa:** "Energia elétrica", "Água e esgoto", "Aluguel", "Manutenção de máquinas", "Manutenção de
  veículos", mais as de sistema "Tarifas" e "Juros e Multas". **Receita:** "Venda de sucata" (a das vendas).
- **Fornecedor novo:** Hidráulica Moretti Ltda (fala: Moréti), PJ, CNPJ 41.739.625/0001-57, Taubaté, SP, contato@hidraulicamoretti.example,
  (12) 9 0000-3131 (manutenção da prensa enfardadeira).
- **Semente `t13/internet` (só o cap06):** fornecedor Vale Fibra Telecom Ltda e 3 contas pagas "Internet do escritório" de R$ 289,90
  (17/08, 15/09, 15/10; boleto; Conta Principal; categoria "Telefone e internet") com seus `bill_payments`: dão "Usado 3 vezes" ao padrão.
  Fica fora da cadeia para as contas e a lista não vazarem para T14/T15.
- **Contas no início (financial_bills):**
  | Descrição | Tipo | Valor | Vencimento | Situação | Categoria · centro · previsto | Parceiro |
  |---|---|---|---|---|---|---|
  | Água e esgoto de outubro | a pagar | R$ 238,40 | 05/11/2026 | pendente (aparece "Vencida") | Água e esgoto · Escritório · nenhum | nenhum |
  | Aluguel do galpão de novembro | a pagar | R$ 6.800,00 | 05/11/2026 | paga em 05/11 por Pix (Conta Principal) | Aluguel · Pátio · Conta Principal | nenhum |
  | Energia elétrica de outubro | a pagar | R$ 1.874,30 | 10/11/2026 | pendente | Energia elétrica · Pátio · Pix Conta Principal | nenhum |
  | 3 parcelas do pedido de venda à Fundição | a receber | R$ 4.790,00 cada | 17/11/2026, 17/12/2026, 18/01/2027 | pendentes, com `order_id` | Venda de sucata | Fundição Bandeira do Vale |
- **Pedido da Fundição:** venda de 300 kg de cobre mel a R$ 47,90 = R$ 14.370,00 em 03/11/2026, a prazo em 3x; saldo da
  Fundição em `balances` (customer) +14.370,00 (todo itemizado nas parcelas: a linha de saldo não aparece).
- **Fiado da Aços Quiririm** (junção: é o saldo do T4, `MUNDO_LINHA_DO_TEMPO.md`): venda no saldo em 05/11/2026 de ferro
  pesado 2.608 kg, chaparia 1.000 kg e ferro misto 600 kg = R$ 4.870,00, a prazo sem parcelas; `balances` (customer)
  +4.870,00 e nenhum título.
- Outras contas e saldos do mundo (histórico pago de agosto a outubro, os saldos do T4) podem aparecer: a fala não depende
  deles; o robô usa a busca para isolar as linhas.
- **Esta aula cria:** a manutenção da prensa (Hidráulica Moretti, R$ 3.480,00, 19/11 → depois parcial, R$ 1.740,00 pagos
  e o resto para 30/11); o conserto do pneu da empilhadeira (R$ 180,00, pago em 09/11 por Pix); os pneus do caminhão
  truck (Auto Peças Vale Forte, 3x R$ 2.360,00: 23/11/2026, 23/12/2026, 23/01/2027); a recorrência "Aluguel da
  empilhadeira" (R$ 2.300,00, mensal, 12/11/2026 até 12/04/2027; dezembro e janeiro passam para 15/12 e 15/01); a baixa da
  energia (Pix, 10/11, com o PDF "comprovante-pix-energia-outubro.pdf" anexado, fictício); a baixa de R$ 2.000,00 no
  saldo da Aços Quiririm (sobra R$ 2.870,00). Atualizar o `MUNDO_FICTICIO.md` (o T14 concilia esses Pix com o extrato).

## Gravação
- **Rotas:** `/dashboard` (só no cap00), `/contas-pagar-receber`. Desktop, sem celular, sem página pública, um usuário só.
- **RPCs novas no backend falso (1.60.18, handlers só do T13):** `update_installment_bill_group`, `delete_installment_bill_group`, `pay_recurring_financial_bill` (valor da ocorrência), `pay_financial_bills_batch` (um lançamento por lote); `create_installment_bills` passou a gravar `installment_group_id`.
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
- **Ilustrações** (cenas a cargo do coordenador; aqui só `cenas/ilustracoes.json`, kit v3 pendente): cap00 contas → lista; cap02 vencidas × 7 dias;
  cap07 uma compra → três contas; cap08 o molde; cap09 só esta × esta e as próximas; cap11 o caminho do dinheiro; cap13 lote = um lançamento;
  cap15 o fiado parcelado; PDF do comprovante (cap16) e da lista exportada (cap18).
- Datas pelo calendário do campo (desktop: botão + calendário). Formulários sem fala podem ser acelerados na edição.
- A tela não tem cartão de crédito no mundo: a seção "Faturas de Cartão" não aparece.
