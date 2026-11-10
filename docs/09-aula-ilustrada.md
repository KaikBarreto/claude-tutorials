# 09 · Aula ilustrada (sem tela do app)

Para aulas de conceito, boas-vindas ou combinados com o cliente, em que **não se mostra a tela do sistema** (no piloto:
Dominex · T0 "Boas-vindas à Dominex", 3 min 25 s). Cada capítulo vira uma **animação desenhada em HTML**, presa às
palavras da narração, que entra no lugar da gravação de tela: o resto do pipeline é o mesmo (palco escuro, vinheta da
aula, vinhetas de capítulo faladas, trilha, SFX, legendas, cartela). Exemplo completo: `exemplos/dominex-t0/`.

## Roteiro
Tabela **Ilustração × Fala** (em vez de Tela × Fala): cada linha é um momento, a cena muda junto com a frase ao lado.
Mesmas regras de fala (só possibilidades, rótulos exatos). As cenas **não imitam telas**: mostram o caminho com
cartões, ícones e os **rótulos reais** do app ("Menu da sua conta" → "Assinatura"). Nada de valor em dinheiro que
mude com o tempo (preço de plano) na ilustração; na gravação da tela, os valores aparecem como estão, sem tarja
(Kaik 03/11). Busca ou resultado mostrado precisa ser real (rode a busca de verdade e copie).

## Narração
Igual à aula com tela (`docs/03-narracao.md`). Em `narracao/tts_textos.py`, além de `CAPS` (uma linha por linha da
tabela), declare `TITULOS = {1: "Título da vinheta.", ...}` (só os capítulos com vinheta) e `KICKERS = {1: "Área", ...}`;
o `titulos.py` usa esses títulos.

## Cenas (`edit/cenas/`)
1. Copie `cenas_modelo.html` para `cenas.html` e escreva um `CAPS[n] = () => { ...monta o DOM...; return t => {...} }`
   por capítulo. Página de 1280×800 CSS (sai 2560×1600, como a gravação do robô).
2. **Tudo é função do tempo**: nada de `transition`/`animation` CSS. Utilidades: `vis(el, t, entra, sai, {dy, dx, sc})`,
   `ripple`, `pulse` (usa a propriedade `scale`, não apaga o `transform` das entradas), `digita`, `mix` (cor).
3. Cada mudança presa a uma palavra: `W(linha, 'palavra', ocorrência, 's'|'e')` lê o `capNN.json`; `L(i)`/`LE(i)` =
   início/fim da linha. A palavra é a do texto do TTS já com as trocas (ex.: "ép" vira "app"); números falados por
   extenso viram palavras soltas ("vinte", "por", "cento"). Palavra não achada aparece como AVISO no render.
4. `el(html, pai)` anexa **todos** os elementos do HTML e devolve o primeiro. Ícones: `ic('nome', px, cor)` com nomes do
   lucide (o renderizador acha sozinho os nomes usados na página; `npm i` na pasta instala o `lucide-static`).
5. Elemento com escala própria (ex.: um cartão reduzido) precisa de um invólucro: a animação mexe no `transform` do
   elemento externo e apagaria a escala.
6. **Cartão nunca vazio**: a cena seguinte entra quando a anterior sai (ou a anterior fica até ela entrar), e um título
   sozinho fica grande no centro, subindo quando o resto entra. No T0 v2 (04/11) o cartão ficou 2 a 3,6 s vazio entre duas
   cenas e 6,6 s só com o título pequeno no topo, na abertura. Medir no vídeo final: miolo do cartão branco e liso ≥ 1 s
   fora do começo de cena é defeito.

## Conferir antes do render (obrigatório)
```bash
cd <tutorial>/edit/cenas
node render_cenas.cjs 2 ../../narracao/cap02.json stills --stills 3.4,11.3,20.6     # quadros JPEG
```
Pegue 2 instantes por linha (meio e fim), monte uma folha de contato e olhe tudo: texto cortado, sobreposição, elemento
que não entrou, composição vazia. No piloto, a revisão pegou 9 problemas antes do render.

## Render e montagem
```bash
bash render_todos.sh                                   # cenas → $TUT_HOME/rec/<tut>/<tut>-capNN.mp4 (0,18 s/quadro)
python3 capitulos_ilustrados.py "<Título da aula>"    # telemetria mínima + caps/capNN.chapter.json + caps/<AULA>.aula.json
python3 -I ../render_chapter.py ../caps/cap05.chapter.json --stills 1,8.5    # confira um capítulo no palco
```
Depois, igual à aula com tela: `render_chapter.py` de cada capítulo → `finish.py` → `legendas_aula.py` → `entregar.py`
(exemplo encadeado: `exemplos/dominex-t0/edicao/montar_t0.sh`). Os capítulos saem com câmera sem zoom automático e
cursor oculto. Capítulo seguido de outro **sem** vinheta: a cena some no fim (`ST.style.opacity`) depois da última
palavra e a seguinte começa do branco.

## Ilustração de conceito no meio do capítulo (kit EcoFlix)
Na EcoFlix a ilustração entra **no meio do capítulo gravado**, cobrindo a janela do app, sempre que a fala explica um
conceito (`[ILUSTRAÇÃO: ...]` no roteiro), e depois volta para a tela. Kit pronto: `perfis/ecoflix/cenas/cenas_ecoflix.html`
(o `instalar.sh` do perfil copia para `<tutorial>/edit/cenas/`; copie para `cenas.html`). Mesmas regras de cima.
- **Estilo**: fundo branco com luz verde suave; Montserrat; o acento `#50D088` só em preenchimento, barra e contorno;
  texto verde `#2E7D57` e âmbar `#8A5A00` (contraste ≥ 4,5 no branco), o âmbar para o segundo conceito da cena; cartões
  brancos de sombra suave, chips e etiquetas; ícones lucide simples; desenhos genéricos sem marca (caminhão, balança);
  números do jeito brasileiro (`kg()`, `brl()`).
- **Movimento**: entrada e saída suaves com `vis`; `conta` (o número conta até o valor), `traco` (a linha se desenha),
  `arco` (o objeto viaja), `contorno` (a cor de destaque entra), `posTitulo` (o título começa grande no centro e sobe
  quando o desenho entra). Tudo preso a palavras com `W(linha, 'palavra')`.
- **Exemplos**: `CAPS[1]` "Tara e peso líquido" (Peso bruto − Tara = Peso líquido) e `CAPS[2]` "Caixa × competência",
  com as falas e tempos estimados em `exemplo/`. Antes da voz, `python3 tempos_estimados.py capNN.json "fala 0" ...`
  faz um `capNN.json` estimado (790 caracteres/min); quando a voz chega, as cenas se ajustam às palavras.
- Um conceito por ilustração; várias do mesmo capítulo cabem no mesmo `CAPS[n]`, cada uma no seu trecho. Rótulos
  exatamente como no app. Renderize só o trecho e encaixe no capítulo:
```bash
node render_cenas.cjs 7 ../../narracao/cap07.json ../out/ilu07_tara.mp4 --html cenas.html --de 41.2 --ate 58.9
# specs.json do capítulo 07: o "at" é o mesmo instante do --de (0,3 s antes da primeira palavra do conceito)
#   "ilustracoes": [{"at": 41.2, "dur": 17.7, "src": ".../out/ilu07_tara.mp4", "box": [166, 44, 1587, 992],
#                    "scale_in": 0.0, "radius": 16, "shadow": false, "loop": false}],  "repouso": [[41.2, 58.9]]
```
  O editor faz a fusão de 0,35/0,30 s com a tela; o `repouso` segura a câmera parada embaixo, e nenhum zoom manual
  termina a menos de 1 s do `at` (`docs/05-edicao.md`).

## Vertical 9:16
Molde `cenas/cenas_modelo_vertical.html` (copie para `<tutorial>/edit/cenas/cenas_vertical.html`): 1080x1920, cenas desenhadas na
área segura (x 72-1008, y 180-1420; a faixa da legenda do player, y 1420-1600, fica livre), um assunto por vez preso à palavra,
texto >= 44 px, até 2 linhas, telas reais = captura do celular (390x844) recortada. Mesmas utilidades do 16:9 (`W(linha,'palavra')`).
- `node render_cenas_vertical.cjs <cap> <capNN.json> <saida.mp4> [--cauda 1.2] [--de S --ate S]` (vídeo = quadro final, com palco e painel);
  `--stills t1,t2 [--guias]` mostra a área segura (magenta) e a faixa (laranja); `--auditar` confere texto, caixas e faixa (exit 2 se houver erro).
- `bash render_todos_vertical.sh [NN ...]` (uma trava por capítulo); `python3 capitulos_ilustrados.py "<Título>" --formato 9x16`
  gera `capNN.9x16.chapter.json` e `<AULA>.9x16.aula.json` a partir da MESMA narração do 16:9, então os tempos saem iguais.
- Montagem: `finish.py caps/<AULA>.9x16.aula.json`; legenda única: `legendas_aula.py ... --linha 32`. Exemplo: `exemplos/dominex-t0/edicao/previa_vertical.sh` (prévia vertical de ~20 s do T0 v2: cena do cap04 de 20,45 a
  29,45 s com `--de/--ate`, auditoria e `finish.py` com `PREVIA.9x16.aula.json`, `"card_no_primeiro": true`).
