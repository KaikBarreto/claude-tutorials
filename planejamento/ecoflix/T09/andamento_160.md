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

## Ensaio (20/11, só rápido, pela fila --prio 09)
Lote 1 (00..11), lote 2 (02, 03, 04, 07, 10), lotes 3 a 6 (02, 07, 10, 06, 10 de novo): todos os 12 capítulos fecham no rápido, 0 falhos.
Correções: JS do filtro (aspas), ordem de Data (2 cliques com pausa), toast do relatório antes do HTML, menu do Caixa (botão "Abrir ações", passar o mouse),
PDF do Valdir (índice 2), cap04 L6 com uma busca só ("166"). Em cap10 a troca de fornecedor NÃO abre "Atualizar os preços?" (passo tirado).
Sobra: atrasos de prever (gestos além da janela da fala): cap04 L2 (~4 s) e L6 (~5 s), cap07 L4 (espera do PDF), cap08 L6 (Aplicar/Limpar).
Completos (BRIEF_ROBO item 3) NÃO rodados: `bash rec/t09/t09_ciclo3.sh NN`.
## Falta / comandos exatos
- Completos e ajuste de tempos dos caps com atraso: `cd /home/claude/ecoflix; TUT_USER=rafael@reciclavalemetais.example TUT_SENHA=<8+ caracteres> bash rec/t09/t09_ciclo3.sh NN`.
- Instância (derrubada ao fim): `FAKE_NOW=2026-11-11T08:30:00-03:00 FAKE_PORT=54309 bash rec/run.sh fake`.
- PDFs/HTML em `rec/t09/pdfs/` conferidos; `mostra` das cenas de PDF atualizado.
