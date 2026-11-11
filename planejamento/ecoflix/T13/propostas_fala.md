# T13 · Propostas de fala (ensaio do robô, 11/11/2026)

O que a fala precisa mudar para bater com a tela do app 1.59.154 ou caber no gesto. Não editei `roteiro.md` nem
`tts_textos.py`: a revisão geral aplica. O gerador do robô (`$TUT_HOME/rec/t13/gerar.py`) já aceita a fala de hoje e a
proposta (âncoras `A_ou`), então não precisa ser reescrito quando a troca entrar.

| Cap. | Linha | Texto atual | Texto novo | Motivo |
|---|---|---|---|---|
| 07 | 6 | "Criar conta. Repara: já entraram as contas de novembro, dezembro e janeiro." | "Criar conta. Repara: já entraram todas, de novembro até abril." | Com "Repetir até" preenchido a RPC cria TODAS as contas até a data de parar: 12/11, 12/12, 12/01, 12/02, 12/03 e 12/04 (`_generate_bills_for_template`, migração 20260626130000 "end_date definido → gera até end_date"; a janela de 3 meses só vale sem data). A tela mostra seis linhas. |
| 07 | 7 | "O sistema guarda um molde da conta e mantém sempre os próximos três meses na lista. Conforme o tempo passa, ele cria a seguinte sozinho, até a data de parar." | "O sistema guarda um molde da conta. Com data de parar, ele já cria todas até ela. Sem data, ele mantém sempre os próximos três meses na lista e cria a seguinte sozinho, conforme o tempo passa." | Mesmo motivo. A ilustração do cap07 ("o molde e a janela de três meses") muda junto: com "Repetir até", as seis contas de uma vez até a bandeirinha de abril; a moldura "próximos 3 meses" só no quadro "sem data". |
| 08 | 5 | "Salvar. Novembro ficou no dia doze, e dezembro e janeiro foram pro dia quinze." | "Salvar. Novembro ficou no dia doze, e de dezembro em diante foi tudo pro dia quinze." | "Esta e as futuras" desloca todas as não pagas a partir de dezembro (`shift_recurring_bills_due_date`): 15/12, 15/01, 15/02, 15/03 e 15/04. |
| 08 | (ilustração) | "Esta e as futuras" acende dezembro, janeiro e o molde | acende dezembro a abril e o molde | Mesmo motivo. |

## Achados do app (e do mundo)
- **Recorrência com "Repetir até"** (cap07/cap08): ver a tabela; o roteiro e o plano diziam "a janela de 3 meses (12/11,
  12/12, 12/01)". O backend falso (`rec/mundo/handlers/rpc/create_recurring_bill_template.mjs`) segue a regra real.
- **Mundo base, `paid_at` do "Aluguel do galpão de novembro"**: a coluna é `date` (migração 20260925200000) e o app corta
  "aaaa-mm-dd" (`BillsList.formatPaidAt`); com o carimbo inteiro, "Quitada em" sairia "05T12:00:00.000Z/11/2026". Já
  corrigido na semente nova da junção (`gerar/sementes.mjs:877`); a `t13/inicio` não precisa mais do `_patch`.
- **Backend falso, busca de parceiro** (`rec/fakebase/core/filters.mjs`): valor entre aspas dentro de `or=(...)`
  (`name.ilike."%Moretti%"`, como o `usePartnerSearch` do app manda) nunca casava, e "Selecione o fornecedor" mostrava
  "Nenhum encontrado." em qualquer aula. Corrigido (tira as aspas, como o PostgREST).
- **Mundo base, recorrência do galpão**: o `generate_due_recurring_bills` do mundo (handler compartilhado) só cria as contas
  vencidas até hoje; o real completa a janela de 3 meses das recorrências SEM data-fim (o molde do galpão, com o próximo em
  05/12, teria 05/12, 05/01 e 05/02 na lista). Não mexi no handler (mudaria a lista e os cartões das outras aulas); a fala da
  T13 não depende disso.
- **Horário das baixas**: `pay_financial_bill` e `pay_partner_balance` lançam o dinheiro às 12:00 (Brasília) do dia pago
  (`v_tx_at`), não na hora do clique. A energia, a prensa e a Aços Quiririm entram no banco em 10/11 12:00 e o pneu em
  09/11 12:00 (a linha do tempo da junção pedia 08:05–08:15 e 09/11 11:00; vale para o OFX da T14).
