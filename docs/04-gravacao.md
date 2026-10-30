# 04 · Gravação com o robô (dados fictícios)

O robô (`ferramentas/rec/`, Playwright + Chromium sem janela) abre o app, clica e digita como uma pessoa, grava a tela
em **2560×1600 sem cursor** e registra a telemetria do mouse e do teclado no mesmo relógio dos quadros. O cursor, o
zoom e o resto vêm depois, na edição. Detalhes de todos os passos e saídas: [`ferramentas/rec/README.md`](../ferramentas/rec/README.md).

## Dois modos

| Modo | Quando usar | Como |
|---|---|---|
| **url** | O app de qualquer pessoa, rodando localmente (`npm run dev`/build) ou num staging, com uma conta de demonstração e dados fictícios | `APP_URL=https://staging.seuapp.com REC_MODE=url`; login nos passos de `setup` (não filmados) com `"$TUT_USER"`/`"$TUT_SENHA"` vindos do ambiente |
| **fakebase** | App com backend Supabase em que você quer controle total dos dados (estado inicial de cada capítulo, respostas de APIs externas) | Um Supabase falso local (`rec/fakebase`) com sementes; o app roda a partir de uma cópia do código (`rec/setup-app.sh`); usado no exemplo Dominex |

No modo **url** a rede não é isolada (o app fala com o próprio backend), nada é zerado entre gravações e cada
gravação começa com o navegador vazio (o login roda sempre, no `setup`). Prepare o estado de partida de cada capítulo
na conta de demonstração (ou crie no `setup`). Use **somente conta de demonstração com dados fictícios**, nunca conta
real nem dado de cliente; credenciais só por variável de ambiente (`read -rs TUT_SENHA && export TUT_SENHA`).
Modo escolhido por: `"mode"` no roteiro › `REC_MODE` › `rec/env.json`. Variável faltando: o robô para antes de abrir o
navegador. Detalhes (rotas em subcaminho, `"spa": true`, aviso de cookies via `"storage"`):
[`ferramentas/rec/README.md`](../ferramentas/rec/README.md) → "Modo URL".

## Mundo fictício
- Empresa de exemplo e pessoas inventadas, plausíveis para o público do app (no T3: Glacial Cold Brasil, usuária
  Camila Duarte, 12 clientes, fornecedores, marcas fictícias).
- Documentos (CPF/CNPJ etc.) sempre com dígito verificador válido; e-mails em `.example`; telefones de faixa fictícia.
- Estado inicial de cada capítulo = o que os capítulos anteriores criaram (no fakebase: `seeds-extra/<id>/apos-capNN.json`;
  no modo url: prepare na conta de demonstração ou recrie no `setup`).

## Roteiro do robô — `rec/<tutorial>/capNN.json`
```json
{"name": "t1-cap02", "mode": "url",
 "prewarm": ["/login"],
 "setup": [
  {"do": "goto", "url": "/login"},
  {"do": "type", "target": {"label": "E-mail"}, "text": "$TUT_USER"},
  {"do": "type", "target": {"label": "Senha"}, "text": "$TUT_SENHA"},
  {"do": "click", "target": {"role": "button", "name": "Entrar"}},
  {"do": "waitFor", "text": "Clientes"}, {"do": "goto", "url": "/clientes"}, {"do": "waitFor", "idle": true}],
 "steps": [
  {"do": "mark", "name": "L1", "at": 0},
  {"do": "click", "target": {"role": "button", "name": "Novo Cliente"}, "at": 4.2, "label": "Novo Cliente"},
  {"do": "type", "target": {"placeholder": "000.000.000-00"}, "text": "91847200000130", "cps": 5.5, "at": 18.4, "label": "digita o CNPJ"},
  {"do": "click", "target": {"role": "switch", "name": "Receber mensagens pelo WhatsApp"},
   "when": {"role": "switch", "name": "Receber mensagens pelo WhatsApp", "checked": false}, "label": "liga só se estiver desligado"}
 ]}
```
- `mark L1..Ln` no início de cada linha da narração; `at` = segundos desde o 1º quadro, tirados de
  `narracao/capNN.json` (a narração começa em t = 0 da gravação). O robô espera até o `at`; se atrasar, registra
  `lateBy`.
- **`label` em todo passo que a edição vai usar**: zooms, destaques e avisos apontam para o rótulo.
- `when`/`unless`: passo condicional (o roteiro vale em versões diferentes do app).
- Alvos por papel e nome acessível (`role`/`name`), `label`, `placeholder` ou `text`, como no Playwright.
- Digitação ASCII sai como tecla; acentos entram por `insertText`. Teclas de `"$NOME"` e de campo de senha saem como
  "•" na telemetria; o valor nunca vai para log, `actions.json` ou `telemetry.json`. Texto literal `$NOME`: `"$$NOME"`.
- Clique pelo teclado (Enter num botão) fica marcado `kb: true` na telemetria: não move o cursor desenhado, só orienta
  a câmera.

## Rodar
```bash
cd $TUT_HOME
# modo url
export APP_URL=https://staging.seuapp.com REC_MODE=url TUT_USER=demo@seuapp.example TUT_SENHA=...   # conta de demonstração
flock .heavy.lock node rec/record.mjs rec/t1/cap02.json --check   # confere o roteiro (passos, alvos, at) e sai
flock .heavy.lock node rec/record.mjs rec/t1/cap02.json            # grava
# modo fakebase (exemplo Dominex)
DOMINEX_SRC=<código do app> rec/setup-app.sh && rec/run.sh build && rec/run.sh up
```
- **Uma gravação por vez e nunca junto com render**: numa máquina de 2 núcleos, com render rodando o `lateBy` subiu de
  0,3 s para 1,3 a 5,8 s. Gravação, render e montagem usam a mesma trava (`$TUT_HOME/.heavy.lock`).
- Aceite de cada capítulo: 0 passo falho, `lateBy` < 0,8 s, `pageIssues` vazio; conferir a folha de contato
  (`<nome>.contact.jpg`: empresa fictícia, versão certa do app, nenhum dado real). Gravação aceita **vale como final**.
- Saídas em `rec/<tutorial>/`: `<nome>.mp4`, `<nome>.actions.json`, `<nome>.telemetry.json`, `<nome>.contact.jpg`.
