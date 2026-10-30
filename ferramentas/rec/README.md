# Gravador Domiflix

Roda o **Dominex de verdade** com dados fictícios (um Supabase falso), controla a tela com um robô que clica e digita
como uma pessoa e grava **vídeo + telemetria** para a edição das aulas. No modo `fakebase` (o padrão) nada aqui fala com
o Supabase real nem com serviço externo. O modo `url` grava o app de qualquer pessoa pelo endereço dele: veja
[Modo URL (o app de qualquer pessoa)](#modo-url-o-app-de-qualquer-pessoa).

```
rec/
  fakebase/    Supabase falso em Node (127.0.0.1:54321): REST, auth, storage, functions, RPC, tiles de mapa
  recorder/    robô + captura de tela + montagem do MP4 (Playwright + Chromium)
  record.mjs   comando de gravação            run.sh   sobe/derruba/reconstrói tudo
  setup-app.sh recria a cópia do app (../app)  poc/     roteiros de exemplo e saídas da prova de conceito
../app         cópia do código do Dominex (a origem é somente leitura; aqui roda o build de produção)
```

## Subir

```bash
rec/setup-app.sh      # só na primeira vez (ou se ../app sumir): copia o código-fonte e roda npm ci
rec/run.sh build      # build de produção apontado para o Supabase falso (~2 min; refaça se o código do app mudar)
rec/run.sh up         # sobe o fakebase (:54321) e o app (:8080)
node rec/recorder/smoke.mjs   # confere /clientes, ficha (9 abas), /equipamentos, ficha do equipamento e criar um cliente
```

Outros: `rec/run.sh status | logs | down`; `rec/run.sh fake` reinicia só o Supabase falso (recarrega seeds e handlers);
`rec/run.sh up --dev` usa o vite dev (**lento demais para gravar**: centenas de módulos por rota). O `run.sh` só encerra
os PIDs que ele mesmo criou (`rec/.runtime/*.pid`).

## Gravar

```bash
node rec/record.mjs rec/poc/poc.json                    # saídas ao lado do roteiro (ou --out pasta)
node rec/record.mjs meu.json --check                    # só confere o roteiro (passos, alvos, `at`) e sai
# outras opções: --name, --keep-frames, --no-encode, --no-reset, --cursor-overlay (depuração), --preset, --crf
```

Antes de cada gravação o robô zera os dados do Supabase falso (`POST /__dev/reset`), abre o app já logado como
**Camila Duarte, admin da Ártica Climatização**, aquece as rotas e roda o `setup` (nada disso vai para o vídeo) e só
então começa a gravar (assim é o modo `fakebase`; no modo `url` não há reset, seed nem login falso). **Nunca rode duas
gravações ao mesmo tempo.**

| saída (`<nome>` = `name` do roteiro) | conteúdo |
|---|---|
| `<nome>.mp4` | 2560×1600, 30 fps constantes, H.264 CRF 16, yuv420p, bt709 faixa TV. **Sem cursor** |
| `<nome>.actions.json` | cada passo do roteiro com instantes reais, alvo e retângulo |
| `<nome>.telemetry.json` | mouse e teclado no mesmo relógio dos quadros |
| `<nome>.contact.jpg` | folha de contato: 12 quadros do MP4 (4×3) com o tempo de cada um |

**Relógio e unidades** (valem para os dois JSON): `t`, `tStart`, `tEnd`, `tAct`, `at`, `lateBy` em **segundos desde o
1º quadro do vídeo**; `x`, `y`, `rect {x,y,w,h}`, `point` em **pixels do vídeo** (2560×1600 = px CSS × 2). A gravação é em
tempo real (1 s gravado = 1 s de relógio). O Chrome só entrega quadro quando a tela muda; o montador segura o último
até o próximo e fecha em 30 fps exatos. Alinhamento medido (`node rec/recorder/clock-check.mjs`): o carimbo do quadro
fica ~40 ms depois do instante em que a página pintou; num clique simples o efeito aparece no vídeo ~0,11 s depois do
`click` da telemetria (0,3 a 0,4 s em navegação de rota ou animação). Ou seja, a telemetria nunca chega depois da imagem.

### `telemetry.json`

`{ video, clock, units, cursorKinds, counts, samples[] }`, cada amostra `{ t, x, y, type, ... }`:

| `type` | campos extras |
|---|---|
| `move` | `cursor`: `arrow` \| `pointer` \| `text` (cursor CSS do elemento sob o ponteiro; `cursorRaw` traz o original quando é outro, ex. `grab`) |
| `down`, `up`, `click`, `dblclick` | `button` (0 esquerdo, 2 direito), `rect` do elemento clicado, `target` (`tag`, `role`, `text`); `click` com `kb: true` e sem `x`/`y` = clique disparado pelo teclado (Enter/Espaço num botão): o mouse não foi lá |
| `scroll` | `deltaY` (e `deltaX`) da roda, em px CSS; a soma dos `deltaY` de uma rolagem é o `by` do passo (rodas sobre iframe vêm do robô, `src: "runner"`) |
| `key` | `key`, `code`, modificadores (`shift`/`ctrl`/`alt`/`meta`) e `rect` do campo focado. Em campo de senha (ou texto vindo de `"$NOME"`) a tecla sai `key: "•"`, sem `code` nem modificadores |

As amostras vêm do próprio navegador (eventos reais). O que a página não enxerga (mapa em iframe, `up` de arrastar, letras
acentuadas, que entram por `insertText`) o robô completa e marca com `"src": "runner"`. Os movimentos do mouse saem em
dezenas de passos por trajetória (curva leve, acelera e desacelera, 0,3 a 0,9 s conforme a distância; ~60 amostras/s em
movimento): a suavização final fica para a edição. **O vídeo não tem cursor**; para depurar a trajetória use
`--cursor-overlay` (ou `"cursorOverlay": true`), que desenha um cursor na página.

### `actions.json`

`{ script, name, video, clock, t0EpochMs, actions[], marks[], late, pageIssues, stats }`. Cada item de `actions`: `i`, `do`,
`label`, `at` (pedido), `lateBy` (se atrasou), `tStart`, `tEnd`, `tAct` (instante do clique/digitação), `target`, `rect`,
`point`, `ok`/`error`. `pageIssues` lista erro de console, exceção, requisição falha e HTTP ≥ 400 vistos na gravação
(vazio = limpo). `stats`: quadros capturados, taxa de captura (`motionFps` = enquanto a tela muda), tempos de captura e
de codificação. `goto` e `waitFor idle` trazem `settled: false` + `pending` (requisições ainda em voo) quando a rede não
assentou no tempo; o `goto` completo traz `loadMs`; `stats.staleRequestsDropped` (esperado 0) conta requisições que o
navegador perdeu e o robô descartou para não travar a espera.

## Escrever um roteiro

JSON (ou `.mjs` com `export default {...}`). Exemplos: `rec/poc/poc.json` (aula curta com `at`) e
`rec/poc/exemplo-passos.json` (um de cada tipo de passo).

```jsonc
{
  "name": "clientes-01",           // nome dos arquivos de saída
  "seed": "x", "pace": 1.1,        // semente do "fator humano"; pace > 1 = mais devagar
  "cps": 9, "tail": 1.5,           // teclas por segundo; segundos de cauda no fim do vídeo
  "start": { "x": 980, "y": 470 }, // onde o ponteiro começa (px CSS)
  "prewarm": ["/dashboard", "/clientes"],   // TODAS as rotas que o capítulo visita (fora do vídeo)
  "setup": [{ "do": "goto", "url": "/dashboard" }, { "do": "waitFor", "idle": true }],  // fora do vídeo
  "steps": [
    { "do": "click", "target": { "role": "button", "name": "Gestão" }, "at": 1.6, "label": "abre o menu" },
    { "do": "type",  "target": { "placeholder": "Buscar clientes..." }, "text": "Padaria" },
    { "do": "waitFor", "text": "Padaria Bom Grão" },
    { "do": "pause", "seconds": 1.4 }
  ]
}
```

Chaves opcionais do roteiro além das acima: `"mode"` (`"fakebase"` ou `"url"`; ver [Modo URL](#modo-url-o-app-de-qualquer-pessoa)),
`"locale"` (idioma do navegador, padrão `"pt-BR"`), `"timezone"` (fuso, nome IANA, padrão `"America/Sao_Paulo"`) e `"storage"`
(`localStorage` inicial `{ "chave": "valor" }`).

**Passos** (`do`): `goto {url, reload?}` (no `fakebase`, com o app já aberto troca de rota por dentro dele, sem recarregar;
`reload: true` recarrega o documento) · `click`/`dblclick`/`rightclick {target}` · `hover {target, seconds}` ·
`type {target, text, clear?, submit?, noClick?, cps?}` (`text` `"$NOME"` = variável de ambiente, para credenciais de conta de
demonstração) · `press {key | [keys], times?}` ·
`scroll {by, duration?, x?, y?}` ou `scroll {target}` (rola até revelar) · `select {target, option}` (nativo ou Radix) ·
`upload {target, file}` (clica no botão e entrega o arquivo sem abrir a janela do sistema; caminho relativo à pasta do
roteiro) · `drag {target, to}` (`to` = alvo ou `{x,y}`) · `eval {js}` (JavaScript na página, retorno vai para `value`) ·
`wait`/`pause {seconds}` · `waitFor {idle | text | selector | target | url | gone}` · `mark {name}`.
Em qualquer passo: `label`, `optional: true` (falha sem abortar), `timeout`.

**Alvo** (`target`): texto (`"Novo Cliente"`) ou `{ text | role + name | selector | placeholder | label | testId | title | alt,
hasText?, exact?, within?, nth? }`; só conta o que está visível. Dicas: as abas da ficha são `role: "tab"`; combobox/select do
Radix não têm nome acessível, use `{ "role": "combobox", "hasText": "Pessoa Jurídica" }`. Se o alvo não aparece, o erro diz
quantos elementos casam.

**`at`** (segundos desde o início da gravação): o robô espera até lá antes de começar o passo; se já estiver atrasado,
segue sem esperar e registra `lateBy` (resumo em `late`). Use nos pontos em que a narração precisa cair; entre eles o robô
corre no ritmo humano. Passo que falha para a gravação e salva `_debug/falha-NN-<passo>.png`.

**`prewarm`**: a 1ª rota carrega o app; as demais abrem por navegação interna (sem recarregar), então os módulos ficam na
memória e a troca de tela dentro do vídeo é instantânea, como no produto. Rota que o capítulo visita e não está no
`prewarm` aparece com tela de carregamento (3 s ou mais sob captura). `goto` com o app já aberto também é interno
(`"reload": true` recarrega de verdade). Digitação: ASCII sai como tecla de verdade; acentuadas (ã, é, ç) por `insertText`.
(Isso vale para o modo `fakebase`; no modo `url` cada rota do `prewarm` e cada `goto` carrega o documento.)

## Modo URL (o app de qualquer pessoa)

O modo `fakebase` (padrão) grava o Dominex com dados fictícios. O modo `url` grava **qualquer app web pelo endereço dele**: um
servidor de desenvolvimento local ou um ambiente de testes (staging) com uma **conta de demonstração**. Nada do fakebase
entra: **sem** reset nem seed, **sem** login falso (a sessão começa anônima), **sem** desvio de rede (o app fala com os
servidores dele de verdade) e **sem** as chaves de `localStorage` da Dominex. Seguem valendo `prewarm`, `setup`, `steps`,
`storage`, `locale` e `timezone`; não precisa de `rec/run.sh` nem do app em `../app`.

**Escolher o modo** (vale a primeira origem que existir): `"mode": "url"` no roteiro › variável de ambiente `REC_MODE=url` ›
`"mode"` em `rec/env.json` (padrão `"fakebase"`). **Apontar o app**: variável de ambiente `APP_URL`. Sem ela o robô usa o
`appUrl` do `env.json` (o Dominex local) e avisa no início; ele imprime só a origem do endereço, nunca usuário e senha que
estiverem nele.

```bash
read -rs TUT_SENHA && export TUT_SENHA     # digita a senha sem ela aparecer na tela nem no histórico do shell
export TUT_USER=demo@exemplo.com.br
APP_URL=http://127.0.0.1:3000 node rec/record.mjs meu-app/cap01.json --check   # confere o roteiro (só avisa se faltar variável)
APP_URL=http://127.0.0.1:3000 node rec/record.mjs meu-app/cap01.json --out meu-app/saida
```

Roteiro de exemplo (`meu-app/cap01.json`). O login fica no `setup`, que **não vai para o vídeo**: a gravação começa já dentro
do app, e usuário e senha nunca aparecem no roteiro, no log, no `actions.json` nem no `telemetry.json`.

```jsonc
{
  "name": "meu-app-01",
  "mode": "url",
  "locale": "pt-BR", "timezone": "America/Sao_Paulo",   // opcionais (estes são os padrões)
  "seed": "meu-app-01", "pace": 1.1, "cps": 9, "tail": 1.5,
  "start": { "x": 980, "y": 470 },
  "prewarm": ["/login"],                                 // rotas que o capítulo visita (fora do vídeo)
  "setup": [                                             // fora do vídeo: entra com a conta de demonstração
    { "do": "goto", "url": "/login" },
    { "do": "type", "target": { "label": "E-mail" }, "text": "$TUT_USER" },
    { "do": "type", "target": { "label": "Senha" },  "text": "$TUT_SENHA" },
    { "do": "click", "target": { "role": "button", "name": "Entrar" } },
    { "do": "waitFor", "url": "/painel" },
    { "do": "waitFor", "idle": true }
  ],
  "steps": [
    { "do": "click", "target": { "role": "link", "name": "Clientes" }, "at": 1.5, "label": "abre Clientes" },
    { "do": "waitFor", "text": "Lista de clientes" },
    { "do": "type", "target": { "placeholder": "Buscar..." }, "text": "Padaria", "label": "busca" }
  ]
}
```

**Regras (valem sempre)**

- **Só conta de demonstração, com dados fictícios.** Nunca uma conta real, nunca dado de cliente: tudo o que aparece na tela
  vai para o vídeo. Crie no app (ou no staging) uma conta só para tutoriais, com nomes, e-mails, telefones e documentos inventados.
- **Credenciais só por variável de ambiente.** No passo `type`, o texto inteiro `"$NOME"` digita `process.env.NOME`. Nunca
  escreva a senha (nem o usuário) no roteiro. Variável que não existe ou está vazia: o robô para **antes de abrir o navegador**
  dizendo qual falta e onde (o `--check` só avisa). Para digitar o texto literal `$NOME`, escreva `"$$NOME"`.
- **O valor nunca é impresso nem gravado.** O `actions.json` guarda o `"$NOME"` literal; se a página mostrar o valor no
  console ou numa URL, ele vira `$NOME` ali também (valores com menos de 4 caracteres ficam de fora dessa troca). No
  `telemetry.json`, as teclas de um `"$NOME"` e as digitadas num campo de senha da página (`input[type=password]`) saem como
  `"•"`, sem `code` nem modificadores (campo de senha dentro de iframe só é mascarado quando o texto vem de `"$NOME"`).
- **O que está na tela vai para o vídeo.** Por isso o login fica no `setup`. Se filmar o login, o usuário aparece; a senha só
  se o app tiver "mostrar senha" e você clicar.

**Diferenças do `fakebase`**

- `goto` e cada rota do `prewarm` **carregam o documento**. A troca de rota por dentro do app (sem recarregar) só funciona
  com o roteador da Dominex (React Router); num app qualquer a tela não mudaria. Num app React Router de uma página só,
  `"spa": true` no `goto` pede a troca interna (em outros roteadores, teste antes).
- As rotas (`"/login"`) são resolvidas a partir da origem do `APP_URL`: para um app em subcaminho, escreva o caminho
  completo (`"/meu-app/login"`). Um endereço completo (`"https://..."`) também serve em `goto`.
- Cada gravação começa com o navegador vazio (sem cookies nem `localStorage`): o login roda em toda gravação. Para esconder
  um aviso de cookies ou tour de boas-vindas, ponha a chave dele em `"storage"` (ex.: `{ "cookie-consent": "accepted" }`).
- `seedExtra`, `user` e `noReset` do roteiro são ignorados (o `--check` avisa). Mundo vazio ou dado de demonstração é
  responsabilidade da conta que você usa; o robô não reinicia nada no app.
- O `pageIssues` do `actions.json` mostra o que o **app de verdade** reclamou (erro de console, HTTP ≥ 400); aviso de
  terceiros (analytics, chat) passa a aparecer, porque a rede não é mais desviada.
- App com polling ou conexão aberta (SSE) nunca "assenta": `goto` (25 s) e `waitFor idle` (15 s ou o `timeout` do passo)
  esperam até o limite e saem com `settled: false`. Num passo filmado, prefira `waitFor { text | target }` a `waitFor { idle }`.

## Dados fictícios (seeds) e o Supabase falso

- Seeds em `rec/fakebase/seeds/*.json` (ordem alfabética; linhas da mesma tabela se acumulam): `{ "tabela": [ {...} ] }`, uma
  lista (o nome do arquivo é a tabela) ou `{ "_vazias": ["tabela"] }` para tabelas consultadas que ficam vazias de propósito.
  Tokens em strings: `@id:chave` (UUID estável), `@today+3d`, `@now-2h`... (`fakebase/core/util.mjs`). Os `gen-*.json` saem de
  `fakebase/tools/gen-seeds.mjs`; para um mundo novo crie um arquivo novo. `tools/cols.mjs <tabela>` mostra as colunas.
- `public_short_code` precisa ter 12 caracteres de `[a-hj-np-z2-9]`, senão a ficha diz "não encontrado" (o gerador já cuida).
- **CPF/CNPJ**: o app **valida os dígitos verificadores** no cliente (`src/lib/documentValidation.ts`,
  `src/utils/cnpjValidation.ts`) e nas edge functions. Os fictícios têm dígitos válidos (`fakebase/tools/docs.mjs`): CNPJ com
  base 9x.xxx.xxx (faixa ainda não emitida), CPF por algoritmo (pode coincidir com pessoa real por acaso; evite CPF de
  aparência real na tela). Telefones `(21) 3000-xxxx`, e-mails `@exemplo.com.br`.
- Handlers em `rec/fakebase/handlers/`: `rpc/<nome>.mjs`, `functions/<nome>.mjs` (edge functions: `cep-lookup` pronta),
  `ext/<host>.mjs` (APIs externas: ViaCEP, BrasilAPI, Nominatim, OSRM...), `views/<nome>.mjs`. Cada arquivo exporta uma função
  `(args, ctx)` com `ctx.db` para ler/escrever as tabelas; regras ao gravar em tabela ficam em `rec/fakebase/hooks/<tabela>.mjs`.
  Mudou handler, hook ou seed: `rec/run.sh fake`.
- **`rec/fakebase/desconhecidos.log`**: tabela, RPC, função ou host externo que o app pediu e ninguém atende (resposta vazia
  + uma linha no log). É a lista de trabalho para enriquecer o mundo; o `smoke.mjs` mostra os novos de cada tela. Hosts
  externos nunca saem da máquina (analytics, fontes e tiles são bloqueados ou atendidos pelo fakebase;
  `rec/.runtime/externos.log`).

## Limites conhecidos

- **Taxa de captura**: o screencast do Chrome em 2560×1600 entrega ~11 a 13 quadros/s enquanto a tela muda (~20 numa página
  trivial) nesta máquina (2 CPUs, JPEG de ~280 KB por quadro codificado em série); com outro job pesado na mesma máquina cai
  para 5 a 8. O MP4 sai em 30 fps repetindo o último quadro: rolagem e animações rápidas têm menos passos que 30 fps.
  Máquina mais forte, mais quadros. Codificação: ~1,1 a 1,7× a duração do vídeo (`stats.encodeS`).
- Janelas fora da página não aparecem: nova aba/popup (o robô segue na aba original), `confirm()` nativo, seletor de
  arquivo (por isso o `upload`). Mapas: o mapa é o sintético de Niterói (sem ruas reais).
- O mundo falso ainda não tem OS, financeiro, contratos nem cobranças: o dashboard mostra zeros e as abas Histórico,
  Contratos, Financeiro... da ficha ficam vazias. Para uma aula que precise disso, crie os seeds das tabelas do `desconhecidos.log`.
