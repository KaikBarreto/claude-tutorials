# T20 · andamento da aplicação do 1.60.18 (20/11)

**Feito:** roteiro e fala (16 caps, 2.701 palavras); `preparar_aula.sh T20`; `rec/t20/gerar.py` (caps 0 a 14 geram sem erro de âncora; 15 é
só montagem); sementes `rec/mundo/seeds-extra/t20/*` (`t20_sementes.py`, exige `PORTAL_SENHA` no ambiente); handlers `entity-portal`,
`entity-portal-report`, `portal-order-receipt`, `collection-request` (aceita a sessão do portal); libs `coletas.mjs` e `portal.mjs`;
`plano.md`, `inventario.md`, `cenas/ilustracoes.json`. Os 3 lotes de ensaio rápido foram usados.
**Ensaio rápido:** passam 0, 1, 2, 6, 7, 11, 12 (sem PDF capturado), 13, 14. Corrigidos DEPOIS do lote 3 e ainda NÃO ensaiados: 3, 4, 5 (esperar a
aba Portal em vez do título), 8 (espera antes da aba Conta-corrente; o portal pós-pagamento precisa ser conferido), 9 (seletores Total e
filtro Material), 10 (Atualizar dados antes da aba Preços: o handler devolve `price_list` com sessão válida, conferido por curl).
**Falta:** ensaiar 3, 4, 5, 8, 9, 10; "SEM PDF" no cap12 (e conferir 09/10) com o ensaio completo; ler a mensagem do `wa.me` no cap13 e
fechar o balão da ilustração; cap04 linha 9 simplificada (só hover na chave e em Remover login; a fala ainda diz "desligar a chave").
**Comandos** (em `$TUT_HOME`, com `PORTAL_SENHA` e `TUT_SENHA` no ambiente): `python3 -I rec/t20/t20_sementes.py` · `python3 -I rec/t20/gerar.py` ·
`bash rec/t20/t20_fila.sh --rapido NN` · `FAKE_PORT=54320 bash rec/run.sh down`
