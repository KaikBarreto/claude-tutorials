# 08 · Lições do piloto (o que custou tempo e como evitar)

Piloto: Dominex · T3 "Clientes, Fornecedores e Equipamentos" (out/2026). "Kaik" é o dono do produto que revisou.

| Problema | Como evitar |
|---|---|
| Render e gravação ao mesmo tempo (2 núcleos): `lateBy` foi a 5,8 s e capítulos tiveram de ser regravados. | Tudo pesado sob a mesma trava `flock .heavy.lock`; gravações primeiro, renders depois. |
| Reinício da máquina matou o agente no meio. | Salvar progresso em disco por capítulo (roteiro, gravação, sidecar) e um registro de pedidos/decisões; retomar pelo disco. |
| `pgrep -f "<texto>"` dentro de um laço achava o próprio laço e nunca terminava. | Padrão com colchete: `pgrep -f "[r]ender_chapter.py"`. |
| Clique sintético (checkbox marcado pelo robô) veio na telemetria sem x/y e derrubou o render. | `tele.py` usa o centro do alvo quando falta o ponto. |
| Download dos áudios do ElevenLabs bloqueado no ambiente. | Kaik exporta o fluxo inteiro em zip; os scripts reconhecem cada capítulo pelo conteúdo. |
| Status do ElevenLabs devolve todas as URLs assinadas (muito texto). | Consultar só as sessões que ainda estão na fila. |
| A exportação do fluxo trouxe outra versão de um capítulo já usado. | Guardar o áudio usado na sincronização e não trocar depois de gravar. |
| Frase trocada por outra mais curta deixa silêncio. | `emendar.py` mantém a duração; a montagem corta o que estiver parado e sem fala. |
| Fala que dependia de um comportamento que o time corrigiu no meio ("eu ligo" o WhatsApp). | Escrever a fala para valer nas duas versões e usar passo condicional (`when`) no robô. |
| Whoosh do kit enterrado sob a trilha na vinheta de capítulo. | SFX da vinheta somados por cima do mix com nível próprio (−15/−16 dB). |
| ASR "perde" palavras coladas ("WhatsApp ligado"). | Decodificar o trecho isolado + medir duração e picos de sílaba antes de regravar. |
| Papel de parede de referência era da Apple. | Fundo próprio gerado por código no verde da marca. |
| Título no cartão pequeno ficava em cima do menu do app. | Vinheta de capítulo cobrindo a tela, com voz e SFX. |
| Trilha de 12 min estourou a memória (~4 GB) e o processo foi morto. | `audio/music_bed.py` faz chiado, estalos e reverb em blocos de 30 s. |
| Zoom e cursor foram para o canto superior esquerdo no cap. 8 (opções "127, 220 e 380 V"): o robô apertou Enter em "Adicionar opção"; clique disparado pelo teclado chega com posição (0, 0) e a telemetria passou a copiar esse ponto. | Gravador marca `kb: true` e não mexe na posição do mouse; `tele.py` descarta (0, 0) e ponto fora do vídeo; clique pelo teclado não move cursor nem faz anel, só orienta a câmera. |
| "Os zooms num geral estão um pouco perdidos": a câmera seguia o mouse parado enquanto a digitação acontecia em outro campo (Celular, Endereço, Categoria cortados na borda). | Câmera v2 mira o alvo da ação e ignora mouse parado; `auditar_camera.py` mede, para cada clique/tecla, se o alvo estava no quadro; render bloqueado se falhar. |
| Na ilustração do QR, "Hi-Wall 18.000 BTUs" (21 px) passou 20 px da borda do cartão no celular; só apareceu na conferência final. | Medir o texto com `getlength` antes de desenhar e olhar 1 quadro 1:1 de cada cena da ilustração antes do render do capítulo (ver 05-edicao.md). |
| Legenda do título do cap. 2 saiu 1 s adiantada: 88,9999 s virava "00:01:28,000" (milissegundos arredondados depois de separar os segundos). | `ts()` arredonda para milissegundos antes de separar h/m/s (`legendas.py` e `entregar.py`). Conferir legendas com a voz: cobertura da fala ≥ 99% e início após pausa com mediana ~0 s. |
| Mixagem da aula inteira morta por memória: `true_peak` sobreamostrava 12 min de uma vez (~4,6 GB) e o limitador criava uma lista Python de 36 milhões de itens. | `audio/kit.py`: pico e soltura do limitador em blocos de 10 s (`limit(..., inplace=True)`); `kit/mix.py` libera cada sinal ao terminar e grava em blocos. Saída idêntica bit a bit à versão antiga. |
| Telemetria com clique sem x/y também quebrava o caminho do cursor (NaN na câmera). | `tele.py` ignora amostras sem ponto ao montar o caminho. |
| Dividi a aula em 3 partes e preparei versão 720p achando que o envio no chat só aceitava ~30 MB. Kaik pediu um vídeo só e sempre a versão completa. | O envio aceitou o arquivo completo de 187 MB. Mandar sempre o completo; partes/720p só a pedido. |
