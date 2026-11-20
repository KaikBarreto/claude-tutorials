# T14 · andamento da aplicação no 1.60.18 (20/11/2026)

**Feito**
- `roteiro.md` e `narracao/tts_textos.py` reescritos: 19 capítulos (00 a 18). Novos: 03 Cartão de crédito, 06 Corrigir e excluir lançamentos,
  17 Outros casos do extrato. Renumerados: antigos 3-14 viram 4, 5, 7-16; recap vira 18. Fala 2.211 → 3.209 palavras (~20,6 min).
  Trechos novos nos capítulos antigos: cap01 (Selecionar lançamentos, linha de pedido, Extrato com o relatório aberto, contas por usuário),
  cap05 (Entrada), cap11 (Ajuste e Saldo do cliente/fornecedor), cap12 (avisos de data e centavos). Dica do saque sem cofre reescrita
  (a frase "Abra o caixa antes de realizar saques" não existe). Aparecida Ramos no lugar de Cooperativa Recomeço (cap14). Dica do cartão
  não promete regra de DRE (depende do regime).
- `rec/t14/gerar.py` com o NOVO mapa (funções capNN guardam o número ANTIGO; `NOVO` leva ao arquivo de hoje) e `cap_cartao`, `cap_corrigir`, `cap_outros`.
  `rec/t14/fake_now.json` criado (10/11 08:30 em todos).
- Sementes (`rec/t14/t14_sementes.py`): `inicio` com os 2 Pix da T13 pela Secundária (83.380,00; sai com 75.380,00), nova `lote` (3 despesas de teste de 09/11).
- Handlers novos (rec/mundo/handlers/rpc): delete_bank_transactions_batch_atomic, compute_card_bill_month, upsert_credit_card_bill,
  create_idempotent_manual_bank_transaction, reconcile_match_group, reconcile_match_entry_split, reconcile_search_split_candidates, reconcile_create_balance_payment.
- `cenas/ilustracoes.json` atualizado (cap renumerados; novas ilu01_extrato_pdf e ilu17_outra_conta; clima e v3 pendente).

**Falta / comandos** (instância 54314: `FAKE_NOW=2026-11-10T08:30:00-03:00 FAKE_PORT=54314 bash rec/run.sh fake`; `TUT_SENHA` 8+ caracteres no ambiente)
- Ensaio rápido em lote: `bash rec/t14/t14_lote.sh 00 01 ... 17` (cada um por `t14_rapido.sh NN`, fila prio 14). Resultado em `rec/t14/.lote*.out`.
- Completos só nos que o `prever.py` apontar (ver relatório final).
- Derrubar a instância no fim: `FAKE_PORT=54314 bash rec/run.sh down`.
