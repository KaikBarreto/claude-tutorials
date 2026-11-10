# 10 · Cena de Windows (programa do computador junto do app)

Para aulas em que um programa instalado no computador do cliente entra na história, ao lado do app no navegador. Piloto:
EcoFlix, o **EcoTray** (a ponte entre o navegador, a balança e a impressora térmica; T5, e trechos do T7 e do T8). Pedido do
Kaik (10/11): "pegar exatamente como o ecotray é num windows e simular uma tela de windows a pessoa usando, junto do
sistema, baseado no dashboard.py". Peças em `ferramentas/windows/`; exemplo inteiro em `exemplos/ecoflix-ecotray/`.

## O que é de verdade e o que é recriado
| Parte | De onde sai |
|---|---|
| Painel do EcoTray e instalador | **o próprio código do app** (`dashboard.py`, `installer_win/installer_gui.py`, somente leitura) rodando num display virtual do tamanho da tela simulada, com Tk 8.6 + Xft, a Montserrat e um EcoTray falso no WebSocket 8054; cada estado vira um PNG da janela (`capturar_ecotray.py`) |
| Menu e ícone da bandeja | o `tray_app.py` de verdade monta o menu (um pystray de mentira só anota os itens: texto, padrão, desligado, separador) e o ícone (`_get_image`: `icon.png` + bolinha do status); a cena desenha o menu no estilo nativo do Windows 11, porque o pystray usa o menu do sistema |
| Área de trabalho, barra de tarefas, relógio, navegador, balão de downloads, SmartScreen | recriação genérica em HTML (`cena_windows.html`): estilo Windows 11 claro, **sem logo nem ícone da Microsoft, de navegador ou de terceiros** (Iniciar = grade de pontos, Explorador = pasta, navegador = globo), fonte Noto Sans no lugar da Segoe UI |
| Página do navegador | a gravação do robô (aula) ou uma imagem do app (prévia sem gravação) |
| Cursor e cliques | o cursor da skill, desenhado na edição (`render_chapter.py`) a partir da telemetria que a cena exporta |

Como o painel é o código rodando, sai igual até nas manias dele: o cartão de status ("Conectado e operando",
"Parcialmente ativo") é o do momento em que a janela abriu e não muda depois; com um navegador conectado o cabeçalho
mostra "2 cliente(s)" (o EcoTray conta também a conexão que pede o status); cada vez que o painel abre com uma impressora
só, ela é marcada de novo e entra "Impressora padrão: X" na Atividade Recente; o aviso de impressão some em 3 s.
Diferenças assumidas: fonte Montserrat (a primeira da lista do código; num Windows sem a Montserrat instalada o painel cai
na Segoe UI); "Consolas" vira Inconsolata; ✓ ● ↻ ⏳ vêm da DejaVu; janela sem sombra nem cantos, como uma janela
`overrideredirect` do Tk no Windows. Textos do Windows (SmartScreen, aviso de download) são os que a pessoa lê e clica.

## Peças
| Arquivo | Faz |
|---|---|
| `preparar.sh` | prepara, sem instalar nada no sistema, o Python com Tk (pacotes do Ubuntu baixados e só extraídos), Pillow, websockets e as fontes, em `$CENA_WIN_CACHE` (padrão `/dev/shm/cena-windows`; o `capturar_ecotray.py` chama sozinho) |
| `capturar_ecotray.py` + `ecotray_sim.py` | plano de capturas → `<saída>/<nome>.png` + `quadros.json` (posição da janela na tela e os alvos de cada uma: texto, retângulo, cursor do widget). Cada sessão roda numa rede própria (`unshare -n`), então a 8054 do EcoTray falso não briga com a do robô. Sessão sem mudança não roda de novo |
| `cena_windows.html` + `cena_windows.cjs` | cena (JSON) → `<nome>.mp4` 2560x1600 a 30 q/s **sem cursor** + `<nome>.telemetry.json` + `<nome>.actions.json`, no formato do robô (`rec/README.md`) |
| `rec/recorder/browser.mjs`, `"device": "windows"` | grava o app em 1280x712, que enche a página do navegador maximizado da cena na escala 1,5 |

## 1. Capturas (`capturas.json`)
```jsonc
{"tela": [1920, 1200], "usuario_windows": "Rafael",            // tela simulada (100%) e o usuário do caminho do log
 "sessoes": [
  {"nome": "bandeja", "programa": "bandeja", "passos": [
     {"status": "connected:COM3@9600", "impressora": "POS-58", "capturar": "bandeja_ok"},      // ícone limpo + menu
     {"status": "error:no_scale_found", "capturar": "bandeja_sem_balanca"}]},                  // bolinha amarela
  {"nome": "painel", "programa": "painel",
   "abrir": {"status": "ok", "scale_info": "Balança: COM3@9600", "printer_info": "Impressora: POS-58",
             "printers_list": ["POS-58"], "version": "1.7.22"},      // o JSON que o tray_app.py passa ao abrir o painel
   "servidor": {"versao": "1.7.22", "trava": "unlocked",            // unlocked | locked | unknown (gate da balança)
     "balancas": [{"id": "b1", "nome": "Balança", "conectada": true, "porta": "COM3"}], "balanca_padrao": "b1",
     "pesos": {"b1": "0.000"}, "impressoras": ["POS-58"], "impressora_padrao": "POS-58", "navegadores": 1,
     "hora": "08:31:03", "atividade": [{"ts": "08:12:40", "msg": "[scale:Balança] conectada", "kind": "ok"}]},
   "log": ["2026-11-10 08:12:30 [INFO] Iniciando EcoTray v1.7.22..."],   // conteúdo da aba Logs
   "passos": [
     {"capturar": "painel_0"},
     {"peso": {"valor": "1250.5"}, "capturar": "painel_1250_5"},           // evento "weight" na 8054
     {"ponteiro": "–", "capturar": "painel_minimizar"},                     // hover de verdade (o "–" fica claro)
     {"atividade": {"ts": "08:32:15", "msg": "Impresso em POS-58", "kind": "ok"}, "impresso": "POS-58",
      "espera": 0.3, "capturar": "painel_impresso"},                        // toast "✓  Impresso em POS-58"
     {"trava": "unlocked"}, {"estado": {"navegadores": 1}}, {"aba": "Logs"}, {"clique": "↻"}, {"enviar": {...}}]},
  {"nome": "instalador", "programa": "instalador", "tamanho_mb": 19.4, "passos": [
     {"capturar": "inst_pronto"}, {"instalar": true, "etapa": [0, "Verificando servidor de downloads...", 5], "capturar": "inst_05"},
     {"baixando": 50, "capturar": "inst_50"},                               // "x.x MB / 19.4 MB", como o _download_file
     {"concluir": true, "espera": 0.5, "capturar": "inst_fim"}]}]}          // 100% + _finish ("✓  Instalado com sucesso!")
```
Cada passo aplica o que tiver, espera (`espera`, padrão 0,45 s) e captura. As etapas do instalador usam os `STEPS` e o
`_set_status` do próprio `installer_gui.py` (nada é baixado). O EcoTray falso segue o `ecotray.py` também onde o painel
depende dele: `set_default_printer` anota "Impressora padrão: X" com a `hora` do servidor; a janela "Configurar Balanças"
pede `list_ports` (`portas` do plano), `list_scale_protocols` (o catálogo de verdade) e `run_diagnostics` (`diagnostico`
do plano, resposta depois de `diagnostico_seg`, relatório pelo `format_diagnosis_report` de verdade); `set_scale` (Gravar)
vira a lista de balanças, cada uma "conectada" com a linha "[scale:<nome>] conectada".

**Janelas filhas** (Toplevel do Tk, como "Configurar Balanças" e "Nova balança") e a **lista aberta de um combobox**: o
passo diz em que janela age e captura com `"janela": "<título>"` (ou `"lista"`); um passo que abre a janela não captura
nela (o seguinte, sim). Ações: `"clique": "<texto>"`, `"digitar": {"campo": "Nome", "texto": "Balança do pátio",
"letras": 8}` (o campo é o da mesma linha do rótulo), `"abrir_lista": "Porta Serial"`, `"escolher": {"campo": "Porta
Serial", "valor": "COM3  ✓ balança"}` (dispara o `<<ComboboxSelected>>` do código). A cena desenha a moldura do Windows 11
em volta do Toplevel (barra de título clara com o ícone e o título, — ▢ ✕). Exemplo: sessão `painel_configurar` do
`exemplos/ecoflix-ecotray/capturas.json` (T5, cenas 5 e 6). Com a detecção "sucesso", o próprio diálogo troca o Protocolo
para o detectado (ex.: Toledo). Hover só de quem tem `<Enter>` no código: no Windows o `tk.Button` (botões do instalador)
não muda de cor com o mouse em cima, só pressionado; no X11 mudaria, por isso não há captura de hover dele.

Rode e confira as janelas antes de montar a cena:
```bash
python3 ferramentas/windows/capturar_ecotray.py capturas.json capturas/ --app $APP_SRC/ecotray   # sob a trava pesada
```

## 2. Cena (`capNN.json`)
```jsonc
{"nome": "t5-cap02", "duracao": 24.0, "capturas": "capturas",          // caminhos relativos a este JSON
 "relogio": {"hora": "08:33", "data": "10/11/2026"},                    // anda junto com o tempo da cena
 "cursor": {"inicio": [820, 700]}, "semente": 7,
 "bandeja": {"icone": "bandeja_ok", "fixado": true},                    // null = EcoTray fechado; fixado false = no "^"
 "icone_app": "app/icon.png",                                           // atalho "EcoTray" na área de trabalho
 "navegador": {"modo": "maximizado", "url": "ecosistematecnologia.com.br/configuracoes", "aba": "Configurações | EcoSistema",
   "favicon": "app/icon.png",
   "pagina": {"gravacao": {"video": "../rec/t5-cap02-app.mp4", "telemetria": "...telemetry.json", "acoes": "...actions.json",
              "de": 0.0, "inicio": 0.0, "ate": 9.0}}},                  // ou {"imagem", "recorte", "escala", "pos", "fundo"}
 "download": {"arquivo": "EcoTray - Instalador.exe", "tamanho": "19,4 MB"},
 "passos": [{"at": 2.0, "do": "clicar", "alvo": "bandeja:ecotray", "botao": "direito", "label": "bandeja", "mostra": "menu"}, ...]}
```
- `at` em segundos da cena; o cursor chega sozinho antes (curva leve, acelera e freia, 0,4 a 1 s conforme a distância) e
  o clique cai no `at`. `mover` chega no `at`; `duplo` = clique duplo. `label` vira passo do `actions.json` (zooms e
  destaques do `specs.json`); `mostra`/`esconde` abrem ou fecham algo logo depois do clique (o menu da bandeja abre com o
  canto inferior direito no ponto do clique, como o pystray).
- Estados: `{"do": "painel" | "instalador", "quadro": "<captura>" | null, "pos"?: [x, y]}` (troca a janela; `null` some),
  `{"do": "janela", "slot": "config" | "dialogo" | "lista", "quadro": ...}` (janelas filhas e a lista do combobox, empilhadas
  na ordem em que abrem), `{"do": "arrastar", "janela": "painel", "para": [x, y], "dur": 1.0}` (o cursor pega a janela pelo
  topo, arrasta junto e solta: a janela do EcoTray não tem barra de título, mas o cabeçalho arrasta),
  `{"do": "sequencia", "janela": "painel", "quadros": [[dt, "<captura>"], ...]}` (peso subindo, barra do instalador),
  `{"do": "bandeja", "icone": ..., "fixado": ...}`, `{"do": "download", "estado": "baixando" | "aviso" | "opcoes" | "concluido" | null}`,
  `{"do": "smartscreen", "estado": "aviso" | "detalhes" | null}`, `{"do": "atalho", "visivel": true}`,
  `{"do": "navegador", "url": ..., "aba": ..., "visivel": ...}`, `{"do": "mostrar" | "esconder", "o": "menu" | "ocultos" | "dica"}`,
  `{"do": "campo" | "campos", ...}` (só para página em imagem: texto por cima de um campo, como o peso da prévia).
- Alvos: `bandeja:ecotray`, `bandeja:^`, `relogio`, `menu:<item>` (ex.: `menu:Abrir EcoTray`), `<vaga>:<texto>` (os alvos
  do `quadros.json` da captura visível na vaga, com os espaços repetidos reduzidos a um: `painel:–`, `painel:✕`,
  `painel:Configurar Balanças`, `painel:aba:Logs`, `instalador:Instalar`, `instalador:Fechar`, `config:Adicionar`,
  `lista:item:COM3 ✓ balança`; numa janela filha, `<vaga>:fechar` é o ✕ da moldura), `smartscreen:Mais informações`,
  `smartscreen:Executar assim mesmo`, `smartscreen:Não executar`, `download:botao`, `download:opcoes` (a setinha do aviso),
  `download:Manter`, `download:Abrir arquivo`, `atalho:EcoTray`, `navegador:pagina`, `navegador:<x>,<y>` (px da página),
  `campo:<id>`, `tela:<x>,<y>` (px da tela). Alvo que não existe naquele instante para o render com a lista.
- Hover: elementos da cena (menu, botões, barra de tarefas) acendem sozinhos com o cursor em cima; no painel e no
  instalador o hover é uma captura (`"ponteiro"` no plano) trocada na hora em que o cursor chega.

Conferir antes do vídeo (obrigatório, como nas cenas ilustradas): `node cena_windows.cjs capNN.json stills --stills 1,2.5,6
--mira` (o `--mira` marca onde o cursor está) e olhar cada quadro: texto, alvo, janela certa na hora certa.

## 3. Como uma aula pede a cena e como a montagem encaixa
1. **Roteiro**: a coluna Tela marca `[CENA WINDOWS n: ...]` com o passo a passo e os textos exatos do código do programa
   (`_BRIEF_ROTEIRO.md`); a fala não lê os textos do Windows, só diz o que fazer ("Clico em Mais informações e depois em
   Executar assim mesmo").
2. **Capturas** da aula em `<tutorial>/edit/windows/capturas.json`, com o mundo dela (impressora, balança, horários do
   relógio do app): um passo por estado que a cena mostra.
3. **Gravação** do trecho de navegador com `"device": "windows"` no roteiro do robô (1280x712), quando a cena mostra o app.
4. **Cena** `<tutorial>/edit/windows/capNN.json`, com os `at` casados com a narração (tempo das palavras no `capNN.json`
   da voz) e `label` nos cliques que terão zoom; `node cena_windows.cjs capNN.json $TUT_HOME/rec/<tut>/<tut>-capNN.mp4`.
   Sai como se fosse a gravação do robô (vídeo, telemetria e ações).
5. **Montagem igual à de um capítulo gravado**: `specs.json` (zooms e destaques pelos `label`) → `montar_cap.py` →
   `auditar_camera.py` com 0 problema → `render_chapter.py`. A câmera mira os cliques da cena; o cursor é o da skill.
   Unidades: px do vídeo = px da tela × 4/3 (`dsf` 1,333 na telemetria). O cursor sai do tamanho certo para a tela simulada
   (um pouco menor que nas aulas com o app a 1280x800); `"cursor": {"dpr": 2.0}` no capítulo o deixa igual ao das outras.
   Zoom na bandeja (canto da tela) passa na checagem até ~1,8x.
Exemplo encadeado: `exemplos/ecoflix-ecotray/previa.sh` (capturas → cena → palco, cursor e câmera), ~15 s de vídeo.

## Lições (10/11)
- O Python do `uv` (python-build-standalone) traz Tk sem Xft: só fontes de bitmap, sem Montserrat. O `preparar.sh` usa o
  Tk do Ubuntu (extraído, com o `_tkinter` do `/usr/bin/python3.X`). E **não use `uv python install`**: ele cria
  `~/.local/bin/python3.X`, que passa na frente do Python do sistema para todo mundo (desfeito com `uv python uninstall`).
- O Xft dá a toda letra de uma fonte "mono" a largura do maior glifo (Inconsolata: 20 px por letra, "1 2 7 . 0"):
  o `fonts.conf` da cena marca a Inconsolata como proporcional. Emoji colorido derruba o Xft: rejeitado no `fonts.conf`.
- Fonte variável no Xft também sai com espaçamento errado: só fontes estáticas no Tk.
