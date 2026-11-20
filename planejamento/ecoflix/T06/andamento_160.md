# T06 · andamento da aplicação no app 1.60.18 (20/11/2026)

## Feito
- `roteiro.md` e `narracao/tts_textos.py` refeitos: 16 capítulos (0 a 15), 3.253 palavras (era 2.044). Novos: **6** Cofre zerado ou negativo
  (handoff 19/11), **11** Despesa e receita do dia, **12** Sangria no fim do dia; trecho **13a** (trava do Fechar Caixa). Renumerados: antigos 6-9 →
  7-10, 10 → 13, 11 → 14, 12 → 15. Trechos novos em 2 (data retroativa), 3 (editar saldo de abertura), 5 (link do tutorial), 8 (painel, resumo),
  9 (permissões), 10 (cofre e data retroativa no saque), 13 (cartões, projeção, diferença 950,00, 957,10), 14 (corrigir sem reabrir).
- `rec/t06/gerar.py` (todos os capítulos, mais 09b e 13a), `t06_sementes.py` (sementes novas: `cofre-negativo`, `apos-cap10`, `apos-cap11`, `apos-cap12`,
  `apos-cap13`, `apos-cap14`, `dia-10-rascunho`), `t06_cap.sh`, `t06_lote160.sh`. `plano.md`, `inventario.md`, `cenas/ilustracoes.json` atualizados.
- Sem handler novo (usa os do mundo base: `get_financial_description_suggestions`, `get_cash_register_other_order_ids`, `get_dinheiro_balance`).

## Falta / comandos
- Ensaio: ver o resultado do lote em `rec/t06/_ens/lote160.log` e `rec/t06/_ens/capNN.resumo.txt`.
- Rodar um capítulo: `cd /home/claude/ecoflix && TUT_USER=rafael@reciclavalemetais.example TUT_SENHA=<8+ caracteres> bash rec/t06/t06_cap.sh NN --so-rapido`
  (NN = 00..15, 09b, 13a). Regerar: `python3 -I rec/t06/gerar.py [NN]`; sementes: `python3 -I rec/t06/t06_sementes.py todas`.
- Depois da voz: `bash planejamento/ecoflix/preparar_aula.sh T06` não toca o capNN.json da voz; rodar o `gerar.py` de novo.
