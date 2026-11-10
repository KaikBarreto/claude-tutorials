# T19 · estado da gravação (porta 54333) · fase 1 em 05/11, app 1.38.19

Regras: `export TUT_HOME=/home/claude/domiflix FAKE_URL=http://127.0.0.1:54333` em TODO comando; `FAKE_NOW=2026-11-10T10:00:00-03:00` no backend
(`FAKE_NOW=... FAKE_PORT=54333 rec/run.sh fake`) e no robô; navegador só sob `flock $TUT_HOME/.heavy.lock nice -n 10`, uma trava por capítulo
(`rec/t19/rodar.sh NN [--ensaio] [--rapido] [--seed]`, lote `rec/t19/lote.sh 0 1 2 ...` NA ORDEM); sem pkill; `rm` só com caminho literal; escrever só em
`t19/edit/`, `rec/t19/`, `rec/fakebase/seeds-extra/t19/` e handlers novos; sem commit. Disco: parar abaixo de 3 GB. PARAR depois da fase 1 (não gravar).

## Retomar depois de reinício do container
1. `FAKE_NOW=2026-11-10T10:00:00-03:00 FAKE_PORT=54333 rec/run.sh fake` (e `rec/run.sh app` se o 8080 caiu).
2. `python3 -I rec/t19/semear.py` só se `inicio.json` mudou; depois `node rec/t19/snap.mjs base` (precisa rodar de novo sempre que `inicio` mudar).
3. Ver a tabela "Progresso" abaixo e seguir do primeiro capítulo sem OK.

## Mundo
- `semear.py` -> `seeds-extra/t19/inicio.json` + `cadeia.json`. Cadeia: a do T13 (`...t13/inicio`) + `t13/apos-cap14` + `t19/inicio`.
- `t19/inicio`: G1 (`_patch` da trilha com `is_onboarding: false`); a linha de `tenant_payment_accounts` da base (ativa) vira `status: null` (sem selo, com o campo da chave);
  `tenant_charges` e `tenant_subscriptions` vazias de propósito.
- Sementes da cadeia (`rodar.sh NN --rapido --seed` grava `apos-capNN`, cumulativas sobre `t19/inicio`): `apos-cap02` (conta ativa), `apos-cap03` (conta de destino e categorias),
  `apos-cap06` (cobrança a receber), `apos-cap08` (cobrança paga), `apos-cap10` (assinatura), `apos-cap12` (cobrança da parcela).
  Obs.: `apos-cap03.json` provisório (escrito à mão para explorar) até a gravação real do cap. 3 sobrescrevê-lo.

## Handlers novos (rec/fakebase/handlers/)
- functions/`tenant-asaas-provision`, `tenant-asaas-create-charge`, `get-tenant-payment-checkout`, `tenant-asaas-create-subscription`, `tenant-asaas-manage-subscription`,
  `asaas-simular-pagamento` (bastidor: o que o aviso do Asaas faz; o robô chama por `eval fetch` no cap. 8); rpc/`get_tenant_subscription_delete_capabilities`.
- Estendido (compatível): `functions/tenant-asaas-card-fees` lê `card_fee_override.pixFreeCount` (padrão 100, como no T1); a ativação do T19 grava 0.

## Progresso
- 05/11 01:3x: backend (handlers), sementes, `semear.py`, `gerar.py` (montado por `montar_gerar.sh` a partir de `_head.py`, `_alvos.py`, `_caps1.py`, `_caps2.py`, `_final.txt`)
  e `cap00..13.json` gerados; `--check` ok nos 14. Explorações A (caps 2-5), B (cap 6, 7, 9) e C (assinaturas, contrato) rodaram; D (checkout público) na fila da trava.
- Falta: `node rec/t19/snap.mjs base` (inicio mudou), depois `rec/t19/lote.sh 0 1 2 ... 13` (ensaio --rapido + semente apos-capNN, NA ORDEM) e conferir `_debug/ens-NN.log`.
- Achado: o código do link tem de ter 12 caracteres (`extractShortCode`, base32 sem i/o/0/1); o da 1ª cobrança é `hn7xq3rmk4vp`.

- 05/11 02:5x: ENSAIO RÁPIDO dos 14 capítulos: 0 passo falho, conferências tela x fala sem DIFERENTE, `window.__avisos` vazio (cap. 8 sem observador: a página pública recarrega),
  `/__dev/unknowns` vazio. Sementes reais `apos-cap02/03/06/08/10/12` gravadas (os `apos-cap00/01/04/05/07/09/11/13` sobram do `--seed`, inofensivos).
- Pendente (não feito de propósito, só ensaio rápido): ensaio completo com `at` (lateBy), vídeo/folha de contato, `cortes`. Ver o relatório ao main.
