# T06 · andamento da aplicação no app 1.60.18 (20/11/2026)

## Feito
- `roteiro.md` e `narracao/tts_textos.py` refeitos: 16 capítulos (0 a 15), 3.253 palavras (era 2.044). Novos: **6** Cofre zerado ou negativo
  (handoff 19/11), **11** Despesa e receita do dia, **12** Sangria no fim do dia; trecho **13a** (trava do Fechar Caixa). Renumerados: antigos 6-9 →
  7-10, 10 → 13, 11 → 14, 12 → 15. Trechos novos em 2 (data retroativa), 3 (editar saldo de abertura), 5 (link do tutorial), 8 (painel, resumo),
  9 (permissões), 10 (cofre e data retroativa no saque), 13 (cartões, projeção, diferença 950,00, 957,10), 14 (corrigir sem reabrir).
- `rec/t06/gerar.py` (todos os capítulos, mais 09b e 13a), `t06_sementes.py` (sementes novas: `cofre-negativo`, `apos-cap10`, `apos-cap11`, `apos-cap12`,
  `apos-cap13`, `apos-cap14`, `dia-10-rascunho`), `t06_cap.sh`, `t06_lote160.sh`. `plano.md`, `inventario.md`, `cenas/ilustracoes.json` atualizados.
- Sem handler novo (usa os do mundo base: `get_financial_description_suggestions`, `get_cash_register_other_order_ids`, `get_dinheiro_balance`).

## Ensaio rápido (3 lotes feitos, 20/11)
- Fecharam sem falha: 00, 01, 02, 04 a 07, 08, 09, 09b, 10, 11, 12, 13, 13a, 14, 15 (lote 3: 08, 10, 11, 12, 13a).
- **Não reverificado**: cap03 (menu "Editar saldo de abertura" falhou no lote 3; conserto já no gerar.py, espera por laço de 10 s no `[role=menuitem]`).
  Comando: `cd /home/claude/ecoflix && TUT_USER=rafael@reciclavalemetais.example TUT_SENHA=<8+> bash rec/t06/t06_lote160.sh 03`
- Correções do lote 3: cap10 (esperar `#fee` antes do foco), cap11 (contas "Aluguel de caçamba" movidas para a semente `apos-cap10`), cap12 (ids `#sangria-amount`/`#sangria-description`), `ensaio/resumo/prever.py` com sufixo `a`.
- Só rápido (sem ensaio completo com voz): todos. Folhas de contato em `rec/t06/_ens/*.contact.jpg` (nenhuma vista; apagar à mão depois).
- Sem a voz: números de dinheiro confirmados pelos `confere` do rápido (3.006,50; 1.450,00; 957,10 etc.); repetir no ensaio completo.

## Comandos
- Rodar um capítulo: `cd /home/claude/ecoflix && TUT_USER=rafael@reciclavalemetais.example TUT_SENHA=<8+ caracteres> bash rec/t06/t06_cap.sh NN --so-rapido`
  (NN = 00..15, 09b, 13a). Regerar: `python3 -I rec/t06/gerar.py [NN]`; sementes: `python3 -I rec/t06/t06_sementes.py todas`.
- Depois da voz: `bash planejamento/ecoflix/preparar_aula.sh T06` não toca o capNN.json da voz; rodar o `gerar.py` de novo.
- Pendências para o Kaik: cena de PDF "Ver comprovante" (não incluída); texto do modal para quem não tem permissão só é falado (sem usuário sem permissão no mundo).
