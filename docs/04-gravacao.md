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

## Mundo de uma série no perfil (`perfis/<série>/mundo`)
O mundo da Dominex mora dentro de `rec/fakebase` (é o padrão). Outra série leva o mundo dela no perfil, e o instalador o
copia para `$TUT_HOME/rec/mundo`; com essa pasta (ou `FAKE_MUNDO=<pasta>`) o `rec/run.sh`, o Supabase falso e o robô
usam só ela. Exemplo inteiro: `perfis/ecoflix/mundo` (EcoSistema, Recicla Vale Metais).
- `mundo.json`: identidade (`config`: empresa e usuário logado), endereços (`env`: porta e chave gravadas no build,
  `fakeNow` e `fakeClock: "anda"`), `navegador` (localStorage da sessão, local do celular) e `smoke` (rota do 1º acesso,
  textos de erro, rótulos em que R$ 0,00 é o valor certo).
- `schema.json` (`node rec/fakebase/tools/gen-schema.mjs <app>/src/integrations/supabase/types.ts --out <mundo>/schema.json`)
  e `defaults.json` (DEFAULT de cada coluna lido das migrations: `node <mundo>/gerar/defaults-do-sql.mjs <app>/supabase/migrations`).
- `seeds/` (gerado por `gerar/sementes.mjs`, nunca à mão), `seeds-extra/` (estado de partida por aula), `handlers/{rpc,
  functions,ext,views}` (um arquivo por função; recebem `RpcError`/`FunctionError` no ctx), `hooks/` (os triggers do banco)
  e `lib/` (contas compartilhadas).
- `app/ajustes.json`: o que o `rec/setup-app.sh` troca na cópia do app para o build falar com o Supabase falso (regex que
  tem de casar 1 vez; o EcoSistema fixa o endereço de produção no `vite.config.ts`).
- Relógio: com `fakeClock: "anda"` o backend parte de `FAKE_NOW` e corre, recomeçando a cada reset (o robô reseta no
  início de cada gravação), igual ao relógio do navegador; registro novo sai com a hora certa.
- Mudou handler ou `lib/`: `rec/run.sh fake` (o `/__dev/reset` só recarrega sementes).

App fora do disco (pouco espaço em `/home`): `git archive` em `/dev/shm`, `APP_SRC=APP_WORK=/dev/shm/<app> rec/setup-app.sh`
(trabalha na própria cópia, recusa pasta com `.git`), `npm ci` lá, e `APP_WORK=/dev/shm/<app> rec/run.sh build`: o build roda
em `/dev/shm` e só o `dist` vai para `$TUT_HOME/app` (menos as pastas de `foraDoBuild`, ex. vídeos do site).

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
- Opções do capítulo (raiz do JSON): `"user"` (entra como outro usuário do mundo fictício, ex.: a visão do técnico),
  `"anonymous": true` (sem sessão: página pública, tela de login), `"sameTab": true` (link `target=_blank` e
  `window.open` abrem na mesma aba, porque o vídeo grava uma aba só; PDF vira ilustração na edição),
  `"seedExtra"` (estado de partida do mundo, por cima das sementes), `"device": "phone"` (celular: 390×844 a 2×, toque,
  cara de Android, permissão de localização; o vídeo sai 780×1688).
- Passos de celular: `{"do": "geo", "lat": -22.89, "lng": -43.12}` (posição do aparelho) e
  `{"do": "clock", "forward": "01:25:00"}` (avança o relógio do navegador; precisa de `FAKE_NOW`).
- Data do mundo: o mesmo `FAKE_NOW` para o backend falso (`rec/run.sh up`) e para o robô (o navegador instala o relógio
  nessa data e o tempo corre normalmente). Datas diferentes nos dois = telas com datas incoerentes.

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

## Custo real dos gestos e como encaixar na fala
O `at` marca o INÍCIO do passo e a fala não espera por ele: um gesto que custa mais que o intervalo entre as palavras chega
atrasado, e o atraso se soma ao do passo seguinte. Medido no T3 v2 (app 1.38.9, sem outro agente na máquina):

| Gesto | pace 0,5 | pace 0,9 |
|---|---|---|
| `click` | 0,5 a 0,9 s | 0,8 a 1,3 s |
| 1º clique numa janela ou folha recém-aberta | 0,9 a 1,6 s | até 2,1 s |
| `hover` curto (`seconds` 0,15 a 0,3) | 0,55 a 0,75 s | 1,0 a 1,6 s |
| `type`, por caractere | 0,09 s a `cps` 40; 0,17 s a `cps` 14 | igual (quem manda é o `cps`) |
| `scroll` com `point` + `by` (`duration` 0,5, `after` 100) | ~1,1 s | |
| `scroll` com `target`, ou clique num alvo fora da parte visível de uma lista (o robô rola o alvo até o centro) | 2,5 a 2,6 s | |
| `eval` | < 0,1 s | |

- **Pace 0,5 e `seconds` curtos** nos capítulos de formulário e de janelas de Configurações. O `pace` só encurta o movimento e a
  pausa do clique (~0,2 s por clique); o resto é custo do navegador. Capítulo adotado de outro tutorial (`adotar` no `gerar.py`)
  sai ~25% mais lento que o original: baixe `pace` e `seconds` herdados com `modif`.
- **Âncora do `at`** = palavra − (custo do gesto − `seconds`), para o cursor CHEGAR na palavra. O 1º clique de uma janela ou folha
  entra com folga ≥ 1,5 s; uma cadeia de hovers só cabe se `custo + seconds` ≤ intervalo entre as palavras.
- **Digitar sem esperar**: `click` no campo e depois `type` com `noClick: true`, `cps` 40, `at` = palavra − 0,05. Texto longo ou
  sem graça visual: `colar()` do `gerar.py` do T3 v2 (`document.execCommand('insertText')`, ~0,05 s; o valor fica no `actions.json`).
- **Alvo fixo no topo ou na base da tela** (cabeçalho, barra de baixo do celular): o robô só aceita alvo entre y 96 e a altura
  − 70 e tenta rolar a página 6 vezes (~6 s de atraso). Use `"noScroll": true` no passo: clique de verdade, com anel e
  telemetria, sem rolar (T0 v2, celular, "Ver trilha" e "Menu").
- **Foco por `eval`, não por Tab**: depois de escolher um item de um Select (Radix) o foco volta ao seletor com atraso, e há tab stops
  escondidos entre os campos. Focar pelo seletor (`input[placeholder="Marca"].focus()`) e, para "Adicionar opção", clicar o botão
  pelo texto e focar a linha nova (`ADD_OPCAO`).
- **Fechar janela**: Esc (duas vezes se houver seletor de cor ou popover aberto) e, como plano B, um `eval` que clica o botão
  Fechar (`FECHAR_EVAL`). Um `click` condicional no botão Fechar pode travar 30 s se a janela sumir durante o passo.
- **Espera do app maior que a pausa da fala** (3 a 6 s depois de um Salvar): `pausas.py NN T:DUR ...` (script do T5, copiado para
  `<tutorial>/narracao/`; ainda não está em `ferramentas/narracao/`) insere silêncio na voz num vão entre frases, e a montagem corta o
  trecho parado com `cortes` ([05-edicao.md](05-edicao.md)).

## Duas pessoas (ou agentes) gravando em paralelo
Cada um com o seu Supabase falso (o estado é reiniciado a cada gravação): o primeiro usa o padrão (`rec/run.sh up`);
o segundo sobe outra instância, `FAKE_PORT=54322 rec/run.sh fake`, e roda o robô com
`FAKE_URL=http://127.0.0.1:54322`. O app continua um só: o robô desvia, dentro do navegador, as chamadas do endereço
gravado no build para a instância indicada. `FAKE_PORT=54322 rec/run.sh down` derruba só essa instância. A gravação
em si continua uma de cada vez (trava `.heavy.lock`).
- **Porta só sua** (ex.: 54377, não "a próxima livre"): `rec/run.sh fake` de quem usa a mesma porta derruba e recria a
  instância do outro (o `.pid` leva a porta no nome). Em 31/10 duas pessoas escolheram 54323; a instância recriada subiu
  sem `FAKE_NOW` e a gravação do T1 cap. 13 falhou no meio (o menu não trocou de logo).
- **`FAKE_NOW` igual no fakebase e no robô**: suba com `FAKE_NOW=... FAKE_PORT=<porta> rec/run.sh fake`, grave com
  `FAKE_NOW=... FAKE_URL=http://127.0.0.1:<porta>` e, antes de cada gravação, confira que a instância ainda é a sua:
  `tr '\0' '\n' < /proc/$(cat rec/.runtime/fake<porta>.pid)/environ | grep FAKE_`.
- **Sequência de gravações: uma trava por capítulo** (`flock .heavy.lock` em cada gravação, ensaio ou render), para os
  jobs curtos dos outros entrarem entre os seus. Em 31/10 um lote de 1 h sob um flock só (T3 v2) parou a fila de quatro
  agentes. Cada capítulo parte da própria semente (`apos-capNN`) e cada agente tem o seu Supabase falso, então quem entra
  entre dois capítulos não mexe em nada seu. Comando em segundo plano com `timeout` é MORTO (com os filhos, o `flock` e a
  gravação em andamento) quando o prazo acaba: prazo por capítulo e com folga (~3× a duração dele), nunca um prazo curto
  para o lote todo.

## Kit do robô por aula (`rec/<id>/`, molde em `ferramentas/rec/molde/`)
O `instalar.sh` copia para `rec/<id>/` as ferramentas que a trilha Domiflix afinou de aula em aula (T15 → T22/T21 → T14); o id da
aula é o nome da pasta. Ordem de uso de cada capítulo, cada passo pesado sob a trava:
1. `python3 -I rec/<id>/ensaio.py NN` → `rec/<id>/_ens/capNN.json` sem os `at` e com cauda curta; grave com `--rapido`. Acha seletor
   errado, passo que falha e estado que não fecha; NÃO mede atraso.
2. `python3 -I rec/<id>/resumo.py NN --ens` (ou sem `--ens`, na gravação): falhas, atrasos, ruído esperado contado à parte
   (WebSocket do realtime, 406 de `.single()` sem linha) e, por passo, a palavra falada no instante do gesto (coluna `voz:`) e o
   valor devolvido pelos `eval` (`=> ...`; `confere*` acusa TELA DIFERENTE DA FALA).
3. `python3 -I rec/<id>/prever.py NN [...] --ens`: simula o roteiro atual com as durações medidas no ensaio (passo novo: modelo de
   custo; rolagem suave por `eval` conta o `dur_ms`). Atraso previsto ≥ 0,8 s pede robô mais enxuto ou respiro, e outro ensaio.
4. `node rec/<id>/explorar.mjs rec/<id>/_ex/algo.json`: abre o app no Supabase falso e executa passos soltos (fotos, textos, HTML,
   `upload`), para achar seletores antes de escrever o roteiro. Divide o backend falso com a gravação (e o reseta): sob a trava.
O gerador do roteiro (`gerar.py`, com os ajudantes de âncora, rolagem e observador de avisos) é de cada aula: veja as lições em
`08-licoes.md` antes de escrever o seu.

## Endereço do produto na tela (`APP_ORIGIN`)
Quando o assunto da aula é um LINK que aparece escrito na tela (T12: "Link do portal", link da unidade do contrato), o
`http://127.0.0.1:8080/...` parece ambiente de teste. `APP_ORIGIN=https://www.dominex.app` (opção do gravador, **desligada por
padrão**, só no modo fakebase) abre o app nessa origem: o navegador acredita estar em `https://www.dominex.app`, mas o
`page.route` serve cada requisição daquela origem do app local (8080), com fallback de SPA para o `index.html` (rota sem
extensão que dá 404), do mesmo jeito que o gravador já desvia o Supabase para a instância falsa. O endereço não é gravado
(gravamos só a página), então não há certificado nem servidor https: a requisição roteada nunca vai para a rede.
- **Como usar**: `APP_ORIGIN=https://www.dominex.app FAKE_URL=http://127.0.0.1:<porta> node rec/record.mjs rec/tNN/capNN.json`
  (também em `explorar` e `smoke`; vale para qualquer script que use `openSession`). Sem a variável o comportamento é o de sempre
  (`rec/recorder/{env,app-origin,browser,runner}.mjs`). Só aceita `http(s)://host` sem caminho; recusa `localhost`/`127.0.0.1`.
- **Nada sai para fora**: com a origem ligada o Chromium sobe com `--host-resolver-rules=MAP * ~NOTFOUND , EXCLUDE 127.0.0.1 ,
  EXCLUDE localhost` e `--no-proxy-server`, além da rede isolada de sempre (analytics, mapas e demais externos já são abortados
  ou respondidos pelo `net.mjs`); `serviceWorkers: 'block'`. Conferido em 31/10 (`rec/t12/app_origin_teste.mjs`): `/`, `/clientes`
  e `/equipamentos` abrem idênticos à linha de base, com 495 requisições servidas do app local, 0 erros no console, 0 respostas
  >= 400, e o único externo (gtag do `index.html`) desviado.
- **O app não muda pelo hostname** (conferido no código: nenhuma lógica de `location.hostname`/`origin` separa site e app; só
  `src/lib/indexNow.ts` cita o domínio, para avisar buscadores, e não roda nos fluxos gravados). Quem usar a opção deve repetir
  o teste (`APP_ORIGIN=... node rec/t12/app_origin_teste.mjs / /clientes --anon`) se o app mudar.
- **O que muda na tela**: tudo o que o app monta com `window.location.origin` (Link do portal, "Copiar link", link da unidade, QR
  Code) passa a mostrar `https://www.dominex.app/...`. O token do link continua fictício (não existe no servidor de verdade).
  A opção vive em `rec/recorder` do ambiente de gravação e na cópia da skill (`ferramentas/rec/recorder/{env,app-origin,browser,
  runner}.mjs`, idênticas, sincronizadas em 31/10).

## Interface do navegador na tela (instalar o app, barra de endereço)
O robô grava só a página. Quando a aula precisa da interface do próprio navegador (ícone de instalar na barra de
endereço, a janela "Instale o app", o app abrindo em janela própria), grave a tela inteira, de verdade (T1 cap14, 04/11):
- `Xvfb :99 -screen 0 1920x1080x24` e `ffmpeg -f x11grab -draw_mouse 1 -framerate 30`; Chromium do Playwright com
  `headless: false`, `DISPLAY=:99`, `--lang=pt-BR`, perfil limpo e `ignoreDefaultArgs: ['--enable-automation']` (sem a
  faixa "controlado por software de teste"). O Playwright segue valendo para o backend falso (route) na página.
- Endereço real do produto com conexão segura: `--host-resolver-rules="MAP dominex.app 127.0.0.1:<porta>"`, um proxy
  HTTPS local para o 8080 e um certificado de uma CA local posta no NSS do perfil (`certutil`). Não aparece "Não seguro"
  (o Chromium mostra o ícone de ajustes de conexão). Contexto seguro, manifest e service worker deixam o app instalável.
- Cliques na interface do navegador são eventos X reais (XTest via `python-xlib`; o `xdotool` não está no apt).
- O Playwright não enxerga a janela do app instalado: detecte a abertura pelo título da janela no X.
- `clock.install` do Playwright travou a tela nesse modo: para a data do mundo, desloque só o `Date`.
- Rótulos reais (Chromium pt-BR): dica do ícone "Instalar Dominex", janela "Instale o app" com "Cancelar" e "Instalar",
  título da janela do app "Dominex - Dashboard | Dominex". Entre "Instalar" e a janela do app há ~4 s parados e um quadro
  branco: corte ou acelere na montagem.
- Celular (Android/iOS) não roda nesta máquina (sem KVM): ilustre o aparelho com as telas reais da Dominex dentro.

## Dado de bastidor no meio da gravação
Quando a fala só cita itens "cadastrados do mesmo jeito" (T4: cinco tipos de serviço), o robô os insere por REST no
backend falso (`eval` com `fetch` em `/rest/v1/<tabela>`, `Prefer: return=representation`) enquanto a câmera olha outra
coisa, e manda o app refazer a consulta **sem eventos de rede**: o par offline/online mostra o aviso "Conexão restaurada".
Acha-se o `QueryClient` pela fibra do React (`#root` → chave `__reactContainer$` → `memoizedProps.client`) e chama-se
`refetchQueries({ type: 'active' })` (exemplo: `REFETCH_JS` em `rec/t4/gerar.py`). O estado final do capítulo, com os
itens de bastidor, vai para a semente `apos-capNN`, e o capítulo seguinte já parte dele.
