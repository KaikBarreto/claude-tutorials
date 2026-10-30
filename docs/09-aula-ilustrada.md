# 09 · Aula ilustrada (sem tela do app)

Para aulas de conceito, boas-vindas ou combinados com o cliente, em que **não se mostra a tela do sistema** (no piloto:
Dominex · T0 "Boas-vindas à Dominex", 3 min 25 s). Cada capítulo vira uma **animação desenhada em HTML**, presa às
palavras da narração, que entra no lugar da gravação de tela: o resto do pipeline é o mesmo (palco escuro, vinheta da
aula, vinhetas de capítulo faladas, trilha, SFX, legendas, cartela). Exemplo completo: `exemplos/dominex-t0/`.

## Roteiro
Tabela **Ilustração × Fala** (em vez de Tela × Fala): cada linha é um momento, a cena muda junto com a frase ao lado.
Mesmas regras de fala (só possibilidades, rótulos exatos). As cenas **não imitam telas**: mostram o caminho com
cartões, ícones e os **rótulos reais** do app ("Menu da sua conta" → "Assinatura"). Nada de valor em dinheiro que
mude com o tempo (preço de plano). Busca ou resultado mostrado precisa ser real (rode a busca de verdade e copie).

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
