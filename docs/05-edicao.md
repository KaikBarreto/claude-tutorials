# 05 · Edição e montagem (`ferramentas/edit/`)

## Por capítulo: `render_chapter.py`
Entrada: JSON do capítulo (gerado pelo `montar_cap.py`) com o MP4 2560×1600 do robô, a telemetria, a narração e as
camadas. Saída: MP4 1920×1080 30 fps (bt709, faixa TV) + WAV da narração alinhado + `.edit.json` (sidecar).
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
- Zooms e destaques apontam para **rótulos de passos** do robô; o retângulo e o instante vêm do `actions.json`
  (largura mínima do zoom ~1150–1300 px de 2560 para não exagerar). `"atraso": 0.8` faz o zoom começar 0,8 s depois
  do passo (quando um clique logo antes ainda precisa aparecer inteiro).
- A conferência do `entregar.py` tira quadros de cada ilustração pelo `caps/<nome>.chapter.json` (começo, meio e fim).
- Avisos ancorados numa palavra da narração (`[linha, "palavra"]`). Aviso só para regra que vale guardar e não está na
  tela, sempre no positivo.
- `titulo`/`kicker` viram a vinheta de capítulo (não há mais cartão pequeno de título).
- Zoom manual não pode coincidir com ilustração que cobre a janela (a ilustração usa a janela em repouso).

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

## Celular (gravação com `"device": "phone"`)
No JSON do capítulo: `"stage": {"bg": ..., "shadow": 0.45, "margin": 56, "radius": 46, "phone": {"bezel": 14}}` (aparelho
genérico, sem marca, desenhado em volta da tela e acompanhando a câmera) e `"cursor": {"show": false, "touch": true,
"ring_alpha": 0.7}` (sem seta; cada toque vira um anel verde). A câmera funciona igual (zoom na tela do aparelho).
