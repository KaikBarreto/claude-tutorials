# Propostas de fala · T21 · Cato, o assistente

Do robô da T21 (11/11). A fala (`narracao/tts_textos.py`) e o roteiro não foram editados: a revisão geral aplica.

## Números das respostas R1 a R9 (plano.md atualizado)
O T21 parte do fim da T15 (cadeia T13 → T14 → T15 da junção; as mesmas sementes do `rec/t15/gerar.py`). Conferido no Supabase
falso, com os filtros das ferramentas do Cato (`supabase/functions/_shared/cato/tools.ts` da 1.59.154). Mudaram só R1 e R4:

| Resposta | Antes | Agora | De onde |
|---|---|---|---|
| R1 Despesas | R$ 32.234,10 | R$ 30.249,20 | `get_financial_dre_summary` 01 a 10/11, regime de caixa (o mesmo da tela "Este mês" do Relatório Financeiro): folha 19.800,00, aluguel 6.800,00, energia 1.874,30, combustível 1.530,00, manutenção 180,00, tarifas 64,90 |
| R1 Resultado | R$ 67.604,65 | R$ 69.589,55 | vendas 118.620,20 − compras 18.781,45 − despesas 30.249,20 |
| R4 Entradas de novembro | R$ 101.620,20 | R$ 114.620,20 | `get_bank_summary`: lançamentos das contas bancárias não arquivadas de 01 a 10/11 com `type` ≠ `transfer` |
| R4 Saídas de novembro | R$ 43.554,10 | R$ 53.554,10 | idem; a frase "sem contar as transferências entre elas" saiu (ver Achados, 1) |

Sem mudança (conferidos): R1 vendas 118.620,20, compras 18.781,45, Fundição 57.460,00; R2 17.540,00 (Fundição 14.370,00, Aços
Quiririm 2.870,00, Valdir 300,00, 82 %); R3 e R8 26.733 kg, R$ 96.076,00, projeção R$ 116.689,40 (= "Total geral" da Posição de
Estoque); R4 saldos 44.933,67 + 82.515,00 + 5.000,00 = 132.448,67; R5 nenhum caixa aberto, #83 R$ 640,00 e #84 R$ 1.250,00; R6, R7
(42 %). "Conta Reserva" já não estava no plano ("Conta Secundária").

## Fala
| Cap. | Linha | Texto atual | Texto novo | Motivo |
|---|---|---|---|---|
| 03 | L4 | "...e o resultado do mês está em uns sessenta e sete mil e seiscentos." | "...e o resultado do mês está em uns sessenta e nove mil e seiscentos." | R1 agora dá R$ 69.589,55 |

## Roteiro e plano (fora das respostas)
- `roteiro.md` cap03: `[ZOOM: "Vendas" R$ 118.620,20 e o resultado R$ 67.604,65]` → resultado **R$ 69.589,55**.
- `plano.md`, "Mundo: o que esta aula precisa": a linha de novembro (despesas 32.234,10, resultado 67.604,65) e a de bancos
  (entradas 101.620,20, saídas 43.554,10) seguem com os valores antigos; `MUNDO_LINHA_DO_TEMPO.md` seção 8 ("Cato") e seção 18
  (T21 cap03, "67.600") também.

## Achados do app
1. **Cato, resumo bancário conta transferência como entrada e saída.** `get_bank_summary` (migration
   `20261011202500_moeda_no_razao_patrimonio_estoque_e_nas_rpc_de_grupo.sql`) só separa as transferências internas quando
   `type = 'transfer'`, mas a tela grava a transferência entre contas como `withdrawal` + `deposit` (`NewBankTransactionModal.tsx:320-350`,
   com `group_id` e `excluded_from_dre`) e o saque para o cofre como `withdrawal` (`WithdrawalForm.tsx:219-250`). Na T21: a
   transferência de R$ 8.000,00 da T14 entra nos dois lados, o saldo inicial da Conta Cooperativa (+5.000,00) vira entrada e o saque
   de R$ 2.000,00 vira saída. A resposta simulada segue o que o app faz hoje; se o app passar a separar por `group_id`, R4 volta a
   R$ 101.620,20 e R$ 43.554,10.
2. (Supabase falso, não o app) O DRE do falso (`rec/mundo/lib/eco.mjs`, `lancamentosResultado`) não conta lançamento de banco com
   `partner_id` ou `group_id`: as baixas da prensa (R$ 1.740,00, Hidráulica Moretti) e da água (R$ 238,40) e a tarifa do saque
   (R$ 6,50) ficam fora das despesas de novembro. R1 segue o falso (o mesmo número da tela "Este mês" da T15); se o falso mudar,
   R1 e a fala do cap03 mudam junto.
