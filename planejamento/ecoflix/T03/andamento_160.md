# T03 · andamento da aplicação ao 1.60.18

**Feito**
- Fala: `narracao/tts_textos.py` com 17 capítulos (3.600 palavras; era 1.959). Novos: 7, 8, 9, 10 (margem automática) e 12 (menu da tabela). Antigos 7 a 11 viraram 11, 13, 14, 15, 16.
- `roteiro.md`, `plano.md`, `inventario.md` (seções 6 e 14) e `cenas/ilustracoes.json` (v3 pendente; PDFs do cap. 14) atualizados.
- Robô: `rec/t03/gerar.py` (todos os `capNN.json` e o `cap01b` geram). Mundo privado `rec/t03/_mundo/` (schema regenerado). Handlers: `save_price_table_margins`, `duplicate_price_table`, `set_my_preferred_price_table`. Sementes: `rec/mundo/seeds-extra/t03/margem-material.json` e `margem-fora.json` (geradas por `rec/t03/t03_sementes_margem.py`).
- Lote 1 rápido lançado (log `/dev/shm/t03_lote1.log`).

**Falta**
- Ler o lote 1, corrigir, lote 2 só com falhas; completos dos capítulos de risco (7 a 10, 12, 14).
- Pendente de decisão do Kaik: Prefixo (F10) e barra de seleção em massa (F11).
- Ao fim: `FAKE_PORT=54303 bash rec/run.sh down`.

**Comandos** (de `/home/claude/ecoflix`; `source rec/t03/t03_env.sh` antes)
- Lote: `bash rec/t03/t03_lote2.sh rapido 07 08 09 10 12` (cada capítulo entra por `rec/fila.sh --prio 03`).
- Leitura: `grep -h "FALHOU\\|SEM ALVO" rec/t03/_ens/.cap*.out`; `python3 -I rec/t03/resumo.py NN --ens`; `python3 -I rec/t03/prever.py NN --ens`.
