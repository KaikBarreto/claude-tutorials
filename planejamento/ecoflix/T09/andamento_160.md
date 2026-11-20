# T09 · andamento da aplicação 1.60.18 (20/11/2026)

## Diagnóstico da varredura (resolvido)
O menu NÃO mudou. A varredura de 19/11 rodou a instância 54309 com o relógio padrão do mundo (10/11) porque a T09 não tinha
`rec/t09/fake_now.json`; no dia 10/11 o app abre a janela "Tarefas para hoje" (Radix) e esconde o resto da tela do leitor de
acessibilidade: por isso "Pedidos", "Financeiro", "Saldo" e "Mês passado" não eram achados e os caps 04 a 10 caíram no setup.
Correção: `rec/t09/fake_now.json` (11/11/2026 08:30 em todos os capítulos) e instância 54309 com `FAKE_NOW=2026-11-11T08:30:00-03:00`.

## Feito
- Fala e roteiro: `narracao/tts_textos.py`, `roteiro.md`, `plano.md`, `inventario.md` (bloco "Atualização 1.60.18"). 12 capítulos (o cap07
  "Exportar a lista" é novo; antigos 7 a 10 viraram 8 a 11). Fala 1.702 → 2.252 palavras. Sem travessão na fala.
- Robô: `rec/t09/gerar.py` (caps 2 a 11 refeitos), `t09_sementes.py` (#85 957,10; #86 15.000,00; gás, aluguel e sangria da T6; compra 1663
  sem fornecedor na `inicio`; bateria na Vale Forte desde `apos-cap04`; IP/navegador na auditoria), `t09_lote1.sh` e `t09_lote_run.sh`.
- Handlers compartilhados tocados (aditivo, só T09 usa): `mundo/lib/eco.mjs` (create_*_atomic aceita `p_force_cash_register` em caixa fechado),
  `mundo/lib/pedido_estorno.mjs` (revert mantém o caixa original fechado quando o pedido não tem dinheiro; auditoria com IP/navegador).
- `cenas/ilustracoes.json`: ilu04_soma reindexada; novas ilu04_caixa_fechado e as cenas de PDF/relatório (cap04, 06, 07, 09), todas `v3: pendente`.

## Falta / comandos exatos
- Ver o resultado do lote 1: `tail -80 /home/claude/ecoflix/rec/t09/_ens_lote2.out` e `/home/claude/ecoflix/rec/t09/_ens/.resumo-NN.txt`.
- Um capítulo: `cd /home/claude/ecoflix; TUT_USER=rafael@reciclavalemetais.example TUT_SENHA=<8+ caracteres> bash rec/t09/t09_lote1.sh NN`
  (só rápido, pela fila `--prio 09`); com o completo pela regra: `bash rec/t09/t09_ciclo3.sh NN`.
- Instância: `FAKE_NOW=2026-11-11T08:30:00-03:00 FAKE_PORT=54309 bash rec/run.sh fake` (derrubar: `FAKE_PORT=54309 bash rec/run.sh down`).
- Depois do ensaio: conferir os textos exatos dos PDFs/relatórios em `rec/t09/pdfs/` e ajustar `mostra` das cenas de PDF.
