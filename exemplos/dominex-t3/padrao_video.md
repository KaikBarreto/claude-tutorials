# Padrão visual dos tutoriais · Trilha Domiflix

Pedido do Kaik (29/10, 23:28): "a gravação tem que ser estilo Recordly (recordly.dev), que tem zoom dinâmico conforme
o clique etc, zoom blur e tudo mais". Parâmetros tirados do código aberto do Recordly (src/components/video-editor/types.ts,
timeline/zoomSuggestionUtils.ts, videoPlayback/zoomTransform.ts) e adaptados ao padrão Domiflix (vinheta, palco, cartela).

## Identidade Domiflix (fica igual às aulas atuais)
- 1920×1080, 30 fps, H.264. Vinheta de abertura (capacete + DOMINEX + "▶ DOMIFLIX" + título) e cartela final.
- Palco claro (gelo #F3F4F6 com luz verde suave + granulado), tela com cantos arredondados e sombra suave.
- Títulos de capítulo em cartão escuro #1E1E1E com acento verde #00C597, Montserrat. Sem contador de etapas.
- Trilha lo-fi baixinha com ducking sob a voz.

## Câmera estilo Recordly
- Gravação limpa da tela (2560×1600, sem cursor) + telemetria do mouse e teclado; cursor e câmera são aplicados na edição.
- **Zoom automático pelos cliques:** cliques a menos de 2,5 s viram um grupo; o zoom começa 0,5 s antes do 1º clique
  e termina 0,5 s depois do último; foco no clique mais "forte" (campo de texto > menu > clique simples).
- **Profundidade:** 1,8× (escala 1,25 / 1,5 / 1,8 / 2,2 / 3,5 disponíveis para zooms manuais).
- **Entrada** ~1,5 s com mola suave; **saída** ~1,0 s. Grupos separados por menos de 1,5 s: a câmera desliza
  de um foco ao outro em ~1,0 s, sem afastar.
- **Dentro do zoom** a câmera acompanha o cursor com mola (sem tremer), mantendo o alvo dentro do quadro.
- **Zoom blur:** desfoque radial proporcional à variação de escala por quadro; **desfoque direcional** quando a câmera
  só anda. Implementação: média de 6 a 8 sub-quadros do transform dentro do obturador (180°) só nos quadros em movimento.

## Cursor (desenhado na edição)
- Seta estilo macOS grande (≈3× o tamanho nativo), mão sobre botões e links, barra de texto sobre campos.
- Suavização do caminho (≈0,67), leve inclinação no movimento, desfoque de movimento (≈0,6).
- Clique: "quique" de escala de ~350 ms e um anel discreto na cor da marca. Some quando parado por muito tempo.

## Edição por cima
- Zooms e destaques manuais do roteiro têm prioridade sobre os automáticos (ex.: explicar um campo pequeno).
- Callouts só para regra de negócio que não está na tela.
