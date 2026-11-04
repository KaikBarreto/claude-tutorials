# 05 · Edição e montagem (`ferramentas/edit/`)

## Por capítulo: `render_chapter.py`
Entrada: JSON do capítulo (gerado pelo `montar_cap.py`) com o MP4 2560×1600 do robô, a telemetria, a narração e as
camadas. Saída: MP4 1920×1080 30 fps (bt709, faixa TV) + WAV da narração alinhado + `.edit.json` (sidecar).
- **Em partes** (padrão desde 03/11; `--partes 1` ou `TUT_PARTES=1` volta ao processo único): o desenho do quadro usa um
  núcleo só e deixava 43% da máquina de 2 núcleos parada. O capítulo vira 4 trechos, renderizados 2 de cada vez sob a mesma
  trava, e o `concat -c copy` junta tudo: ~1,4× mais rápido (20 s de vídeo: 136 → 97 s), 598 de 600 quadros idênticos ao
  render inteiro (os outros 2 a 81,5 dB). Cada trecho decodifica a gravação desde o início do capítulo e descarta os quadros
  anteriores, para usar os mesmos quadros da gravação. Os cortes só caem em quadros sem aviso, destaque, ilustração ou
  título, porque essas camadas guardam estado do 1º quadro em que aparecem. Trecho < 10 s vai inteiro.
- **Câmera v2** (estilo Recordly/Screen Studio; refeita em 30/10 depois do "zoom no canto" e dos "zooms perdidos"):
  - Mira o **alvo da ação**, não o mouse: clique do mouse (ponto/campo), clique pelo teclado (Enter/Espaço num botão,
    telemetria `kb`) e cada tecla digitada (retângulo do campo com o foco). Eventos a menos de 2,5 s viram um grupo.
  - Zoom do grupo = 1,8× ou menos, para caber o maior alvo com 10% de folga (abaixo de 1,2× não dá zoom).
    Começa 0,5 s antes do 1º evento, termina 0,5 s depois do último; entrada ~1,5 s, saída ~1,0 s.
  - Dentro do grupo a âncora só muda quando o próximo alvo sairia dos 80% centrais da vista; sai 0,5 s antes do evento
    (até ~1 s se o deslocamento for grande), fica pelo menos 0,6 s em cada lugar e desliza em ~0,8 s.
  - **Mouse parado não puxa a câmera** (seguir 0,35 e caixa segura só com o mouse em movimento ou clicando).
  - Clique isolado em Fechar/Cancelar não dá zoom (a tela muda em seguida e o zoom ficaria olhando o vazio).
  - Zoom manual (retângulo do roteiro) tem prioridade; desfoque de movimento só nos quadros em movimento.
  - **Checagem obrigatória**: 0,6 s depois de cada evento o alvo tem de estar ≥ 90% no quadro e longe da borda, e
    nenhuma âncora perto do canto (0, 0). Se falhar, `render_chapter.py` **não renderiza**. Auditoria de todos os
    capítulos sem renderizar: `python3 -I auditar_camera.py` (no T3 caiu de 114 instantes ruins para 0).
  - Conferência visual: `python3 -I folha_zooms.py out/folhas_zoom` = um quadro de cada zoom assentado e de cada
    troca de alvo, em folhas 4×4 com capítulo, tempo e zoom.
- **Cursor** desenhado (seta grande, mão em botão, barra em campo), quique e anel na cor de acento da marca no clique.
- **Palco**: `stage.bg` = `assets/fundo_escuro.png` (gerado por `fundo_escuro.py` na cor de acento da marca), sombra
  0,35, margem 44 px, cantos 16 px.
- **Destaques** (spots: escurece o resto + contorno na cor de acento + rótulo), **avisos** (callouts: cartão escuro embaixo) e
  **ilustrações** (sequência PNG com alfa ou MP4 num retângulo).
Velocidade: ~9–15 quadros/s na máquina de 2 núcleos (um capítulo de 110 s leva ~5 min).

## Marca: `$TUT_HOME/marca/marca.json`
Cores (acento, escuro, claro), fonte, logo (arquivo, símbolo, wordmark), nome da série, estilo da vinheta (`logo` ou
`dominex-capacete`) e frase da cartela. Lida por `kit/ui.py` e usada por tudo que desenha: palco (`fundo_escuro.py`),
cursor, destaques, avisos, vinhetas de capítulo, abertura e cartela. Guia: [`modelos/MARCA.md`](../modelos/MARCA.md).
Trocou a marca? Apague `edit/assets/fundo_escuro.png` (o `montar_cap.py` gera de novo na cor nova).

## Especificação curta por capítulo: `caps/specs.json` + `montar_cap.py`
```json
"02": {"titulo": "Cliente empresa pelo CNPJ", "kicker": "Clientes",
       "spots": [{"passo": "Novo Cliente", "antes": 1.4, "dur": 1.8, "rotulo": "Novo Cliente"}],
       "zooms": [{"de": "Razão Social", "ate": "E-mail fiscal", "fim": "bloco Endereço fiscal"}],
       "callouts": [{"palavra": [6, "Uma"], "dur": 4.5, "texto": "Dica: ..."}],
       "ilustracoes": [{"at": 40.62, "dur": 8.1, "src": ".../ilu_qr", "box": [166, 44, 1587, 992], "scale_in": 0.0}],
       "cortes": [[109.2, 110.7]]}
```
- `callouts.palavra` = `[linha, "palavra"]` com a linha contada **a partir de 0** (`words[].linha` da narração; a
  linha 1 do roteiro é 0) e a palavra exata, sem pontuação. Com a numeração do roteiro o aviso cai na linha seguinte
  ou o `montar_cap.py` aborta (T5 e de novo no T8; lição em `08-licoes.md`).
- Zooms e destaques apontam para **rótulos de passos** do robô; o retângulo e o instante vêm do `actions.json`
  (largura mínima do zoom ~1150–1300 px de 2560 para não exagerar). `"atraso": 0.8` faz o zoom começar 0,8 s depois
  do passo (quando um clique logo antes ainda precisa aparecer inteiro).
- `"escala": 1.4` fixa o aumento do zoom (sem ele, sai do tamanho do retângulo) e `"min_w"` muda a largura mínima.
  Digitação com `noClick` (cursor parado longe do campo): `escala` ≈ 1,4, para campo e cursor caberem juntos. Alvo
  colado na borda direita (≤ ~90 px): `min_w` pequeno e `escala` ≥ 2,6. Passo logo depois de abrir um modal pode ter
  `rect` velho: para o zoom, use o rótulo de um passo posterior. Conferir tudo com `auditar_camera.py` (T4, ver `08-licoes.md`).
- A conferência do `entregar.py` tira quadros de cada ilustração pelo `caps/<nome>.chapter.json` (começo, meio e fim).
- `"repouso": [[de, até], ...]` (segundos do capítulo) segura a câmera parada, sem zoom, sob uma ilustração que cobre
  a janela, para os cliques do robô não puxarem a tela por baixo dela (T5, cap16).
- Avisos ancorados numa palavra da narração (`[linha, "palavra"]`, a primeira ocorrência na linha: use uma palavra que
  só aparece onde o aviso deve entrar). Aviso só para regra que vale guardar e não está na tela, sempre no positivo.
- `titulo`/`kicker` viram a vinheta de capítulo (não há mais cartão pequeno de título).
- Zoom manual não pode coincidir com ilustração que cobre a janela (a ilustração usa a janela em repouso); a saída do
  zoom leva ~1 s, então termine-o pelo menos 1 s antes do `at` da ilustração.

## Ilustração na tela (ex.: `ilustra_qr.py`)
Sequência PNG 1587×992 com alfa (cantos de 16 px) desenhada por código (PIL, 2× para anti-serrilhado), fundo
branco, fonte e cor de acento da marca, objetos genéricos sem marca de terceiros. Tempos casados com as palavras da fala. No JSON:
`box` = janela em repouso `[166, 44, 1587, 992]`, `scale_in: 0`, `shadow: false`; o editor faz fade de 0,35/0,30 s.
Todo texto dentro de cartão/aparelho é medido antes de desenhar (`font.getlength(texto)`): termina pelo menos
12 px antes da borda; se não couber, diminua a fonte ou o ícone ao lado. Confira 1 quadro 1:1 de cada cena da
ilustração antes de renderizar o capítulo (no T3 o nome do aparelho passou 20 px da borda e custou um re-render).

## Montagem final: `finish.py caps/<AULA>.aula.json` (modelo em `modelos/aula.json`)
- Vinheta da aula e cartela (`kit/brand_clips.sh`, a partir de `marca/marca.json`): logo da marca + "▶ SÉRIE" +
  título da aula; cartela com o logo e a frase final (`outro_line`, padrão "Até a próxima aula!"). No perfil Domiflix:
  o capacete em 3 peças que se encaixam.
- **Vinheta de capítulo** (`vinheta_cap.py`) antes de cada capítulo com `card` (menos o primeiro): fusão de entrada
  0,4 s, área + título sobem com a barra na cor de acento, voz do título em 0,70 s (`card_voices` = `titulos.json`), saída por
  fusão no 1º quadro do capítulo seguinte; ≥ 3,2 s. SFX por cima do mix: whoosh na entrada (−15 dB), pop quando o
  título pousa (−22 dB), whoosh descendente na saída (−16 dB).
- **Cortes**: `cortes` do capítulo tiram vídeo e voz juntos (só em trecho parado e sem fala; medir antes com a
  diferença entre quadros) e deslocam os SFX e as legendas.
- Trilha lo-fi (`kit/mix.py`): começa no fim da vinheta, ~−27 LUFS sem fala, cai sob a voz (ducking), termina num
  acorde na cartela. Mix final ~−16 LUFS, teto −1 dBTP.
- Saídas: `aula_final.mp4`, `capitulos.json` (início de cada item no conteúdo, cortes, título falado).
Tempo: ~40 quadros/s na junção (aula de 12 min ≈ 10 min) + vinheta e mix.

### Vertical 9:16 (versão para celular)
A 9:16 é a "Versão para celular" da MESMA aula: a DomiFlix troca sozinha o vídeo em tela menor que 1024 px (inclusive na
introdução obrigatória). Por isso o vertical tem de ter **a mesma linha do tempo** do 16:9 (mesmas vinhetas, cortes, tempos e
áudio) e **uma única legenda por aula** (SRT/VTT iguais nas duas versões). É opção nova; o 16:9 não muda (`identidade_domiflix.sh`).
- Peças: `fundo_escuro_vertical.py` (palco = o do 16:9 girado 90°), `web/intro_vertical.html` + `kit/brand_clips_vertical.sh`
  (vinheta e cartela, logo DomiFlix todo branco, mesmo som e mesma duração), `vinheta_cap_vertical.py` (vinheta de capítulo),
  `render_chapter_vertical.py` (cena ilustrada 1080x1920 pronta, sem recodificar; ou tela real do celular, abaixo), `finish.py --formato 9x16` (ou `"formato": "9x16"` na aula; mesma mixagem), `entregar.py --unico` (720x1280).
- **Tela real do celular** (gravação 390x844, `"telemetry"` no JSON): `render_chapter_vertical.py` recorta a área que a fala cita e amplia
  2,4x (390 -> 936 px) na janela `tela_real` do painel (x 72, y 240, 936x1160, acima da faixa da legenda), sem moldura de aparelho;
  câmera v2 (alvos do actions/telemetria; só desliza, e fica no alvo entre uma ação e outra), anel do toque, destaques e avisos como
  no 16:9. Usa `camera.py`/`cursor.py`/`overlay.py` por cópia privada (`celular_vertical.py`): os do 16:9 não mudam. Mesmo JSON do
  capítulo de celular do 16:9, mais `"camera_9x16"` e `"scale9"` (opcionais). Alvo fora da janela = erro (`--aceitar-camera`).
- Geometria única em `formato_9x16.json`: painel 1008x1700 em (36,110); conteúdo em x 72-1008, **y 180-1420**; texto >= 44 px;
  até 2 linhas. **Faixa da legenda do player: y 1420-1600** (18% do pé no celular; 15% no computador, y 800-930 do 16:9): nada essencial.
- Vinheta e cartela verticais não levam o logo da DomiFlix (pedido do Kaik): capacete + DOMINEX + título; `SERIE_LOGO=assets/<png>` o devolve.
  No 16:9, `"sem_domiflix": true` na aula (ou `brand_clips.sh --sem-domiflix`) tira o "▶ DOMIFLIX"; o padrão continua com ele.
- Legenda única com linhas curtas, que servem às duas proporções: `legendas_aula.py ... --linha 32`; gere uma vez e use o mesmo
  arquivo nas duas entregas. Nomes: `<Aula>.mp4` e `<Aula> (vertical).mp4`, cada um com `.srt` e `.vtt`.
- Teste: `flock $TUT_HOME/.heavy.lock nice -n 10 bash testes/vertical_9x16.sh`. Ver também `docs/09-aula-ilustrada.md` (cenas).

## Corrigir uma aula já entregue sem refazer tudo: `remendar_aula.py caps/<AULA>.aula.json`
Depois da entrega a limpeza apaga as gravações e os renders dos capítulos; ficam só `out/<AULA>/capitulos.json`,
`video_sem_audio.mp4` e `proj/{audio48k.wav, edl.json, render.json, build/intro_v.mp4, build/outro_v.mp4}`. Rodar o
`finish.py` de novo exigiria regravar e renderizar TODOS os capítulos; o `remendar_aula.py` refaz a aula só com o que mudou
(a mesma linha do tempo, os mesmos parâmetros do `finish.py`).
Com o disco apertado, o `video_sem_audio.mp4` pode sair, porque o vídeo do `aula_final.mp4` é cópia dele. Antes de apagar,
confira o MD5 dos pacotes (`ffmpeg -i X -map 0:v -c copy -f md5 -` nos dois). Antes de remendar, recrie com
`ffmpeg -i aula_final.mp4 -map 0:v -c copy video_sem_audio.mp4`. Exceção: quando o `-shortest` cortou o último quadro do
final (T2, T4 e T12, um quadro a menos), o MD5 difere; nesse caso, mantenha o `video_sem_audio.mp4`. Feito em 04/11 em T0,
T1, T3 v2, T5, T7 e T18: ~1 GB liberado. O `proj/build/mix.wav` também pode sair depois da entrega: o remendo refaz o mix
do zero (`refazer_mix()`, a partir de `audio48k.wav` e `edl.json`). Ajuste feito à mão no mix se perde no remendo (T8: -3 dB
em 834,93–835,06 s contra o pico do AAC): confira o pico real que o `entregar.py` mostra. Uso:
- `--audio cap03,cap07`: só narração nova **de mesma duração** (emenda do `emendar.py`; o `narration` do
  `caps/capNN.chapter.json` aponta para `takes/capNN_v2/audio48k.wav`). Nenhum quadro muda: refaz `audio48k.wav`, `edl.json`,
  o mix (`kit/mix.py` + SFX das vinhetas) e o MP4 final com o vídeo antigo.
- `--novos cap05,cap06,cap13`: capítulos regravados e já renderizados (`render_chapter.py`; `out/capNN/capNN.mp4/.wav/.edit.json`),
  com a duração que tiverem; o que vem depois se desloca. O vídeo antigo é copiado pacote a pacote (PyAV, com pts/dts; GOP
  fechado, então o corte é limpo) e só se recodifica: os capítulos novos, as vinhetas de capítulo vizinhas (elas fundem a tela do
  capítulo de antes com a do de depois) e, no máximo, ~2 s de cada lado até o IDR vizinho. Os quadros copiados saem idênticos.
- `--plano` mostra a linha do tempo nova e o que é copiado/recodificado, sem escrever nada e sem pedir a trava
  (`--frames cap05=1954` simula capítulo ainda sem render).
- `--manter-stems`: por padrão, depois do mix, `proj/build/stems` e `music.wav` somem (~1,1 GB numa aula de 12 min; a trilha sai
  igual de novo, `--seed 3`). O `mix.wav` fica: apague-o depois de entregar.
- **Depois**: `legendas_aula.py` e `entregar.py` como sempre (cada um sob a trava, ou a cadeia toda numa posse só:
  `flock .heavy.lock nice -n 10 env TUT_LOCKED=1 bash cadeia.sh`, com render do capítulo que falta, remendo, legendas e entrega).
- **Medido** (31/10, 2 núcleos): T1 com 3 capítulos novos e 2 só de áudio = 8,4 min (5.541 de 21.755 quadros recodificados, ~23 q/s;
  o mix leva ~1 min); T4 só áudio = 4,1 min.
- **Conferir uma aula remendada**: `ffmpeg -xerror -i aula.mp4 -f null -` (decodifica tudo sem erro); a diferença entre quadros
  consecutivos em cada emenda (T1: 0,4 e 0,6, no nível dos vizinhos; um salto de 85 no quadro 20.309 já existia no vídeo antigo, é
  um corte de cena do próprio capítulo); e a diferença de áudio antigo × novo por janela de 5 s (só as janelas trocadas passam de
  −10 dB; o resto fica no piso do AAC, −30 a −38 dB).
  Automático (04/11, T5/T4/T1, ~1 min cada): `conferir_remendo.py antigo.mp4 novo.mp4 --novos INICIO:FIM --emendas t1,t2
  --srt antigo.srt novo.srt` confere quadros iguais antes dos capítulos novos e iguais com deslocamento (em quadros inteiros,
  achado sozinho) depois deles, áudio sem buraco nas emendas (silêncio que o antigo já tinha no mesmo ponto, como a pausa
  de 0,1 s antes da cartela, não conta) e legendas iguais fora dos novos; sai com 1 se algo falhar.
  Dois ou mais trechos novos separados (ex.: caps 07-08 e 14): `--novos A:B,C:D`, cada trecho antigo entre eles ganha o
  próprio deslocamento (testado com par sintético: +1 s e −1 s achados, e FALHOU quando faltou um trecho).
  A olho: `folha_tempos.py aula_final.mp4 emendas.jpg "Tnn · emendas" --emendas t1,t2` (de 0,5 em 0,5 s, 2 s antes e
  depois de cada emenda) e a folha de 3 s só dos capítulos novos.
- **Antes de escolher o que regravar**: o rótulo que mudou entre versões do app aparece também na tela de capítulos que
  não falam dele. No T4 (1.38.19) o botão "Novo Tipo" virou "Novo Serviço": regravados só os 2 capítulos com fala, os
  vizinhos 02, 04, 05 e 06 seguiram com "+ Novo Tipo" no topo, e a revisão mandou regravar mais 4 (só tela, mesma voz).
  A segunda revisão achou mais 3: cap07 e cap08 começam na página (o `setup` do robô abre `/servicos`) e trocam de aba
  em 1 s; o cap14 (recapitulação) volta a ela por 10 s. Liste todos de uma vez pelo robô: os `rec/tN/capNN.json` cujo
  `setup` ou passo abre a página, mais os cliques de aba, não só os capítulos vizinhos.
- **Hardlinks**: `aula_final.mp4` tem links em `entrega/` e `entrega_final/`; o script escreve em arquivo temporário e troca no
  fim (`ffmpeg -y` no mesmo nome truncaria a entrega antiga). Já `legendas_aula.py` + `entregar.py` reescrevem `.srt`/`.vtt` no mesmo
  arquivo: a legenda nova já vale em `entrega_final/` antes do MP4. Troque o MP4 logo depois (`ln -f entrega/<nome>.mp4 entrega_final/`).
- Se cair no meio, o estado antigo fica em `out/<AULA>/_base` e a execução seguinte parte dele. Capítulo com `cortes` não é
  suportado (use o `finish.py`). H.264 bruto (`-f h264`) perde a ordem dos quadros B: por isso o remendo trabalha com pacotes de MP4.
- **Mexeu na emenda de pacotes? Teste antes numa amostra** (copia `[0, IDR)` + recodifica um trecho + copia o resto, tirado do vídeo
  antigo): conferir pts/dts estritamente crescentes (passo 512), md5 dos quadros copiados idêntico ao antigo e PSNR dos recodificados
  ≥ 44 dB. Esse teste pegou um deslocamento que crescia a cada quadro copiado (`(D − a) * passo` dentro do laço), que teria
  estragado a primeira aula de verdade.

## Celular (gravação com `"device": "phone"`)
No JSON do capítulo: `"stage": {"bg": ..., "shadow": 0.45, "margin": 56, "radius": 46, "phone": {"bezel": 14}}` (aparelho
genérico, sem marca, desenhado em volta da tela e acompanhando a câmera) e `"cursor": {"show": false, "touch": true,
"ring_alpha": 0.7}` (sem seta; cada toque vira um anel verde). A câmera funciona igual (zoom na tela do aparelho).

- **A tela fica presa ao retângulo ARREDONDADO do aparelho em todo quadro, com a moldura por cima** (entrada e saída do zoom,
  deslizes, desfoque de movimento). O `Stage._render` recorta cada canto da tela com a máscara arredondada, e antes só o fazia
  quando o lado correspondente da tela estava DENTRO do quadro. No celular a tela é mais alta que o quadro: na entrada/saída do
  zoom a borda de cima ou de baixo sai do quadro enquanto o canto (raio ~100 px a 2,2x) ainda invade, e nada o recortava: a tela
  vazava com canto reto por cima da moldura (Kaik, T7 cap. 1: "a imagem do celular cruza o celular e fica com as bordas retas
  aparecendo"; 362 quadros de risco num capítulo de 70 s, 139 seguidos numa só passagem). Agora a regra é "dentro do quadro OU a menos
  de um canto (`pad = ceil(r) + 2`) dele", só quando `stage.phone` existe; no computador `pad = 0` e o quadro é idêntico ao do T3.
- **Conferir** (sob a trava, nenhum precisa de gravação nova): `python3 -I auditar_recorte.py caps/capNN.chapter.json` compõe o palco
  com a tela toda magenta e toda preta, tira a cobertura da tela de cada quadro (média dos sub-quadros do desfoque inclusive) e
  compara com o retângulo arredondado calculado; sai com código 1 se algum pixel erra mais de 0,5 (olhar a folha de quadros não
  basta: em vários trechos o canto reto dura só 2 a 13 quadros, uns 0,07 a 0,4 s). `python3 -I folha_transicoes.py caps/capNN.chapter.json` tira do MP4 renderizado só os
  quadros de transição (os de risco e um no meio de cada entrada, saída e deslize) numa folha `.folha_transicoes.jpg`.
  `bash testes/recorte_celular.sh` (~1 min, sem gravação) confere o palco: o código novo passa, o ANTIGO (`pad = 0`) é acusado e o
  16:9 sai idêntico bit a bit. Rode junto de `bash testes/identidade_domiflix.sh` depois de mexer em `stage.py`.
