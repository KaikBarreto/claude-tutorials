# T20 · andamento da aplicação do 1.60.18 (20/11)

**Feito:** roteiro e fala (16 caps, 2.701 palavras); `preparar_aula.sh T20`; `rec/t20/gerar.py` (caps 0 a 14 geram sem erro de âncora;
15 é só montagem); sementes `rec/mundo/seeds-extra/t20/*` (`t20_sementes.py`, exige `PORTAL_SENHA` no ambiente); handlers `entity-portal`,
`entity-portal-report`, `portal-order-receipt`, libs `coletas.mjs`/`portal.mjs`; `plano.md`, `inventario.md`, `cenas/ilustracoes.json`.
**Em curso:** lote 1 de ensaio rápido (log em `/home/claude/ecoflix/rec/t20/_ens/lote1.log`, resumos `_ens/resumoNN.txt`, `_ens/preverNN.txt`).
**Falta:** corrigir o que o lote 1 mostrar (seletores, fala × tela, valores calculados vistos na tela), texto exato do WhatsApp na
ilustração do cap13, ensaio completo (sem `--rapido`) dos caps que o `_BRIEF_ROBO.md` pede, derrubar a instância.
**Comandos** (no `$TUT_HOME`, com `PORTAL_SENHA` e `TUT_SENHA` no ambiente):
`python3 -I rec/t20/t20_sementes.py` · `python3 -I rec/t20/gerar.py` · `bash rec/t20/t20_fila.sh --rapido NN` · `FAKE_PORT=54320 bash rec/run.sh down`
