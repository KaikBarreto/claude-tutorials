# Marca: `marca/marca.json`

Um arquivo define a identidade do tutorial inteiro (vinheta, cartela, vinhetas de capítulo, palco, cursor, cartões).
Fica em `<TUT_HOME>/marca/marca.json` (o `instalar.sh` copia a pasta de `MARCA=<pasta>`); `MARCA_JSON=<arquivo ou
pasta>` troca só naquela execução. Sem o arquivo vale o padrão neutro, que é o `modelos/marca.json`. Caminhos são
relativos à pasta do marca.json; chaves que começam com `_` são comentário.

| Chave | O que é | Padrão |
|---|---|---|
| `serie` | nome da série no rótulo "▶ SÉRIE" da vinheta e da cartela (vazio: sem rótulo) | `Tutoriais` |
| `cores.acento` | cor da marca: luz da vinheta e do palco, área e barra da vinheta de capítulo, anel do clique, destaques | `#3B82F6` |
| `cores.escuro` | cartões (dicas, títulos, selo de velocidade) | `#1E1E1E` |
| `cores.claro` | títulos sobre o escuro e o palco claro | `#F3F4F6` |
| `fonte.arquivos` | `{"500": "fontes/X-Medium.ttf", "700": "fontes/X-Bold.ttf", "800": "..."}` (TTF/OTF). Peso que faltar usa o mais próximo; um arquivo só serve todos (fonte variável) | `{}` = Montserrat do kit |
| `fonte.familia` | nome da fonte (informativo) | `Montserrat` |
| `logo.arquivo` | logo principal, PNG com fundo transparente (≥ 1600 px de largura) ou SVG, na versão para fundo escuro | sem logo: selo neutro |
| `logo.simbolo` e `logo.wordmark` | opcionais; com os dois, o símbolo entra primeiro e o nome sai de trás dele | |
| `logo.wordmark_altura` | altura do nome em relação à do símbolo nessa composição | `0.5` |
| `logo.pecas` | `pecas.json` do símbolo em peças (gerado por `kit/brand_extract.py --pecas`), para o estilo `ecosistema-reciclagem` | |
| `vinheta.estilo` | `logo` (qualquer marca), `dominex-capacete` (só a Dominex: peças do capacete em `web/assets`) ou `ecosistema-reciclagem` (símbolo em peças que se encaixam girando; EcoFlix) | `logo` |
| `vinheta.som` | som próprio da vinheta (mp3/wav, **fora do git**); no `ecosistema-reciclagem` o 2º golpe dele cai no encaixe. Sem o arquivo, vale o sintetizado | sintetizado |
| `vinheta.som_origem` e `som_tom` | de onde o `instalar.sh` copia o som (caminho dentro de `APP_SRC`); transposição do sintetizado quando o som falta (semitons) | `2` |
| `cartela.frase` | frase da cartela final; o `outro_line` do aula.json, se houver, vale mais | `Até a próxima aula!` |

- O resto sai do acento: texto no acento sobre o escuro é clareado até ficar legível, texto sobre o acento fica branco
  ou escuro pelo contraste, e o fundo escuro do palco gira as luzes para a matiz do acento. Depois de trocar a marca,
  gere o fundo de novo: `python3 <tutorial>/edit/fundo_escuro.py`.
- Conferir a marca em uso: `python3 kit/ui.py`. Logo num arquivo só (símbolo à esquerda + nome):
  `python3 kit/brand_extract.py logo.png <pasta da marca>` grava `assets/simbolo.png` e `assets/wordmark.png`.
- Símbolo feito de peças separadas (ex.: o de reciclagem): `python3 kit/brand_extract.py --pecas logo.png <pasta da marca>`
  separa as peças e o nome **sem redesenhar** (cada pixel do PNG vai para uma peça; empilhadas, refazem o símbolo pixel a
  pixel) e grava `assets/pecas.json` (centro de giro, ordem do encaixe e o lugar de cada parte no logo).
- Estilo `ecosistema-reciclagem`: os tempos, curvas e sons do `dominex-capacete` (vinheta 4,42 s com saída escura em
  4,30 s; cartela 3,85 s). As peças giram em volta do centro do símbolo, no sentido das setas, até o lugar exato do logo
  oficial; soco e brilho no encaixe; o nome sai de trás do símbolo; título embaixo, sem o rótulo "▶ SÉRIE" (o nome já é a
  série). Com `vinheta.som`, o som da marca toca inteiro: os dois primeiros golpes, achados no próprio arquivo, caem quando
  a última peça assenta e no encaixe; por baixo, o respiro e os whooshes das peças. O som não vai para o git: o
  `instalar.sh` copia de `APP_SRC/<som_origem>`. No vertical 9:16 (`web/intro_vertical.html`), o molde do capacete
  vertical: o símbolo sobe e o nome sai de trás dele para baixo, centrado pelas letras (®/™ do fim fica pendurado).
- O estilo `logo` só tem 16:9; o vertical existe para `dominex-capacete` e `ecosistema-reciclagem`.
- Só o logo da própria marca; nada de logo ou fonte de terceiros sem licença.
- Exemplos completos: `perfis/domiflix/marca/` (estilo `dominex-capacete`, saída idêntica ao T3) e
  `perfis/ecoflix/marca/` (`ecosistema-reciclagem`, som sintetizado em Mi maior; o oficial da EcoFlix é opcional).
