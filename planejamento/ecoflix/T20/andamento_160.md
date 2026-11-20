# T20 · andamento da aplicação do 1.60.18 (20/11, fechamento)

**Feito:** roteiro e fala (16 caps), sementes, handlers, `gerar.py`, `ilustracoes.json` (cap13: texto real do wa.me, pedido #1761 de 10/11, R$ 18.714,08).
**Ensaio rápido aprovado:** 0, 1, 2, 5, 6, 7, 8 (saldo novo no portal), 9 (relatório sai como HTML, não PDF), 11, 12 (PDF A4 capturado: #1749, Papelão..Ferro misto, Saldo R$ 3.700,00, "Escaneie para ver fotos"), 13 (wa.me lido), 14.
**Causas achadas:** (1) `portal-order-receipt` dava 500 ("semValor antes de inicializar"): corrigido, era o "SEM PDF" do cap12. (2) Saldo "antigo" do cap08 = cache de 30 s do React Query do portal no ensaio rápido (a volta ao portal acontece em <30 s): o robô agora recarrega a página ao voltar. (3) Cap04 linha 9: o robô agora liga a chave a desligada de verdade (o botão vira "Remover login", sem clicar); a fala não mudou. (4) Cap10: o desktop navega a janela ao blob (headless baixa o PDF): gancho `BLOB_HOOK` + `PDF_BLOB_JS`. (5) Cliques em "Editar" do cadastro passaram a ser por eval (menu da linha, aberto por hover, intercepta o ponteiro e o clique esperava 60 s).
**NÃO fechou (limite de 2 lotes):** caps 3, 4 e 10 corrigidos DEPOIS do lote 2 e não reensaiados.
**Comando** (em `$TUT_HOME`, `TUT_SENHA` e `PORTAL_SENHA` no ambiente, 8+ caracteres; regravar antes `python3 -I rec/t20/t20_sementes.py`): `bash rec/t20/t20_fila.sh --rapido 3 4 10`
**Disco:** `/` a 98% (ENOSPC derrubou o gravador do T12 cap09 às 21:51).
**Instância 54320 derrubada:** `FAKE_PORT=54320 bash rec/run.sh down`.
