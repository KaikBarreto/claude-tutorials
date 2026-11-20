# T03 · andamento da aplicação ao 1.60.18

**Feito**
- Fala: `narracao/tts_textos.py` com 17 capítulos (3.600 palavras; era 1.959). Novos: 7, 8, 9, 10 (margem automática) e 12 (menu da tabela). Antigos 7 a 11 viraram 11, 13, 14, 15, 16.
- `roteiro.md`, `plano.md`, `inventario.md` (seções 6 e 14) e `cenas/ilustracoes.json` (v3 pendente; PDFs do cap. 14) atualizados.
- Robô: `rec/t03/gerar.py` (todos os `capNN.json` e o `cap01b` geram). Mundo privado `rec/t03/_mundo/` (schema regenerado). Handlers: `save_price_table_margins`, `duplicate_price_table`, `set_my_preferred_price_table`. Sementes: `rec/mundo/seeds-extra/t03/margem-material.json` e `margem-fora.json` (geradas por `rec/t03/t03_sementes_margem.py`).
- Ensaios: lote 1 rápido de todos os 17 + cap01b; correções; lotes 2 a 4. Aprovados no rápido: 00 a 05, 08, 10 a 16 (08 e 13 depois das correções). Completos aprovados: 07, 09 (antes do ajuste abaixo), 10, 12, 14 (atrasos até 0,8 s; PDFs gerados em `t03/pdf`).
- Correções aplicadas SEM novo ensaio: cap06 (hovers de Sair/Cancelar/rodapé com `noScroll`, que levavam 7 s cada) e cap09 (hover "Sem preço" ancorado em "Esses"; antes 5,6 s de atraso, prever agora 0,5 s).

**Falta**
- Rodar de novo o cap06 (rápido e completo) e o cap09 completo; completos de 08, 11 e 13 não foram feitos. O limite de 3 lotes foi gasto (lote 2 rodou com JSON velho).
- Pendente de decisão do Kaik: Prefixo (F10) e barra de seleção em massa (F11).
- A senha fica em `/dev/shm/t03_senha` (fora do repositório); `t03_env.sh` só lê dela.

**Comandos** (de `/home/claude/ecoflix`; `source rec/t03/t03_env.sh` antes)
- Lote: `bash rec/t03/t03_lote2.sh rapido 07 08 09 10 12` (cada capítulo entra por `rec/fila.sh --prio 03`).
- Leitura: `grep -h "FALHOU\\|SEM ALVO" rec/t03/_ens/.cap*.out`; `python3 -I rec/t03/resumo.py NN --ens`; `python3 -I rec/t03/prever.py NN --ens`.
