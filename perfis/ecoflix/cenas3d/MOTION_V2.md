# Biblioteca de motion do kit v2 (EcoFlix) · para reaproveitar em outro estilo

**Situação (18/11).** O piloto de refino em argila foi encerrado antes da entrega: o Kaik escolheu outros estilos na
folha de estilos (vidro escuro e gradientes suaves), então a parte de ESTÉTICA do v2 (luz, argila, chão, fichas de
sombra dos rótulos) não vai ser usada como está. O que serve a qualquer estilo é a **biblioteca de motion** descrita
aqui: funções puras do tempo, sem dependência de cor, material ou tema. O kit v1 e as cenas atuais não foram tocados.
Não foi gerado vídeo antes/depois (nada em `~/ecoflix/previa_ilustracoes/`).

Arquivos (todos novos):
- `perfis/ecoflix/cenas3d/kit3d_v2.js`: kit 3D v2 (cópia do v1 com trocas; mesma API). Linhas citadas abaixo como `3D:n`.
- `perfis/ecoflix/cenas/cenas_ecoflix_v2.html`: kit 2D v1 inteiro + blocos `KIT 2D V2` (linhas 342 a 427). `2D:n`.
- Exemplos de uso: `planejamento/ecoflix/T08/cenas3d/cena3d_v2.html` (`CAPS[4]`, linha 93) e
  `planejamento/ecoflix/T08/cenas/cenas_v2.html` (`CAPS[7]`, ajudantes `anda/chega/recua/espera` nas linhas 465 a 470).

Regra de base: tudo é função só de `t` (o render é quadro a quadro, em qualquer ordem). Nada de relógio, estado entre
quadros, `requestAnimationFrame` ou física com passo. `pr(t, a, d)` = avanço de 0 a 1 a partir do instante `a`, por `d` s.

## 1. Curvas (`3D:20-33`; no 2D dentro de `V2`, `2D:373-381`)
| Função | O que faz | Quando usar |
|---|---|---|
| `eo5(x)` | quíntica de saída: arranca na hora, desacelera por muito tempo | entrada de rótulo, contagem, onda |
| `ei(x)` | cúbica de entrada: acelera | saída (curta, não pede atenção) |
| `eio5(x)` | quíntica nos dois lados | movimento com peso (título que sobe, conta que viaja) |
| `passa(x, k)` | passa do alvo e volta (k = quanto; 1,1 ≈ 4 %) | quem entra por escala (selo, operador, anel) |
| `eo`, `eio` | as cúbicas do v1, mantidas | as cenas chamam direto |
| `escalona(a, i, passo = .09)` | instante do item `i` de uma fila | stagger de 60 a 120 ms |

## 2. Molas (`3D:26` e `3D:31`; `2D:378` e `2D:380`)
- `mola(x, z = .5)`: resposta ao degrau de uma mola amortecida, analítica, 0 → 1 com x de 0 a 1. `z` = amortecimento
  (0,3 balança muito; 0,7 passa uma vez; ≥ 1 não passa). A frequência é escolhida para o resto ser < 0,1 % em x = 1.
- `golpe(x, n = 1.6, a = 4.2)`: resposta ao impulso (sai de 0, bate, oscila e volta a 0). `n` = idas e voltas, `a` =
  quanto morre. Pico ≈ 1: multiplicar pela amplitude. Serve para pulso, tremor de batente, cartão que balança.

## 3. Entrada, saída e ênfase de rótulo (HTML; independem do tema)
| Função | Onde | O que faz |
|---|---|---|
| `vis(e, t, a, b, {dy, dx, sc, din, dout})` | `3D:105`, `2D:397` | entra em `a`, sai em `b`. Opacidade em 62 % do tempo e posição com cauda de 130 % (`eo5`): já se lê enquanto assenta. Saída em 70 % do tempo, acelerando. `sc < .9` usa `passa` |
| `pulse(e, t, a, amp, dur)` | `3D:115`, `2D:408` | ênfase por `golpe` (bate e assenta). No 2D compõe com o `transform` do `vis`: chamar depois dele |
| `ripple(r, t, a)` | `3D:113`, `2D:405` | onda que abre com `eo5` e some com potência 1,6 |
| `foco(e, t, a, b, {min, fora, d})` | `3D:119`, `V2.foco` `2D:383` | um assunto por momento: fora de `[a, b]` o elemento recua (opacidade × `min`, saturação 35 %); `fora: true` inverte. Chamar depois do `vis` |
| `posTitulo(e, t, a, sobe, sai)` | `3D:134`, `2D:421` | título grande no centro que sobe com `eio5`; a chamada entra antes, com o espaçamento das letras fechando de .42 a .3 em, e o título 90 ms depois |
| `mostrador().troca(t, a)` | `3D:157` | rótulo 1 sobe e sai, rótulo 2 sobe e entra (80 ms de defasagem) |

## 4. Contagem
- `conta(e, t, a, d, v0, v1, fmt)` (`3D:125`, `2D:415`): número que conta com `eo5` (cauda 15 % mais longa que `d`).
- `pesa(mostrador, t, a, d, v0, v1, {z, passo, fmt})` (`3D:128`): leitura de balança. O valor segue `mola` (passa e
  volta, `z` .74 ≈ 4 %), anda de `passo` em `passo` (10) enquanto mexe e crava o valor exato no fim; acende a luz
  `.md` do mostrador em âmbar até 93 % e verde depois. No 2D, `V2.pesa(elementoDoNumero, ...)` (`2D:390`), sem a luz.

## 5. Traço e viagem sobre traço (2D)
- `traco(path, t, a, d)` (`2D:417`) e `arco(e, t, a, d, x0, y0, x1, y1, h, rot)` (`2D:418`): mistura de `eio` com `eo5`
  (arranca com peso, chega desacelerando).
- `V2.curso(path, q)` (`2D:386`): desenha o `<path>` até a fração `q` (o traço segue um objeto).
- `V2.sobre(e, path, q)` (`2D:388`): põe o elemento no ponto da fração `q` do `<path>`.
  Juntos fazem "a conta que viaja pelo caminho e acende o nó quando chega": ver `anda()` em `T08/cenas/cenas_v2.html:465`.

## 6. Câmera 3D (`3D:169`, `3D:196-218`)
- `camera([[t, {x, y, z, d, az, el, oy}, 'eio'|'lin', arco], ...])`: as chaves do v1, sem mudança.
- `poseBruta(t)` (`3D:197`): a interpolação do v1. `pose(t)` (`3D:210`): média de 9 amostras de `poseBruta` em
  `t ± inercia` com peso em sino (`1 + cos`): toda quina de velocidade vira curva (arranque e parada com peso; a deriva
  `'lin'` não começa de tranco). Depois soma a respiração do operador: `az` ± 0,0032 e 0,0015 rad, `el` ± 0,002 rad, em
  senos lentos de `t`.
- Opções de `cena(monta, {inercia: .34, respira: 1})`; `0` em cada uma devolve a câmera do v1. Duas chaves quase juntas
  (um corte) viram ~0,7 s de movimento: usar `inercia: 0` nessa cena.
- A técnica vale para qualquer câmera ou valor com chaves: alisar amostrando a própria função, em vez de filtrar no tempo.

## 7. Objetos com peso (3D)
| Função | Onde | O que faz |
|---|---|---|
| `cresce(o, t, a, d, giro)` | `3D:315` | objeto entra por escala com `passa` (3 %) e giro que desacelera com `eo5` |
| `pulso(o, t, a, amp, dur)` | `3D:319` | ênfase de objeto por `golpe` |
| `destaque(anel, onda, t, a)` | `3D:310` | anel que passa e assenta + onda longa |
| `transfere(im, B, t, a, d, {ordem, passo, arco, suave})` | `3D:526` | peças de um lote caem com gravidade (horizontal quase linear, vertical ao quadrado, arco que perde força) e um quique nos últimos 18 %; `passo` escalona; `suave: true` = voo do v1 |
| `suspende(v, arfa, afunda, rola)` | `3D:730` | mexe a carroceria (`userData.corpo`) sem tirar as rodas do chão |
| `dirige(v, t, fx, h, {k, hz, z, carga, golpes})` | `3D:736` | o veículo segue `x = fx(t)`; a suspensão é a convolução da aceleração de `fx` (diferença finita) com a resposta ao impulso de uma mola (54 amostras de 1/30 s). `golpes: [[t0, força]]` = trancos verticais; `carga(t)` de 0 a 1 afunda a mola |
| `poeira(pai, n, cor)` + `sopra(p, t, a, [x, y, z], {d, r, dir, alto, op})` | `3D:744`, `3D:750` | sopro de `n` sprites macios: abrem com `eo5`, sobem, somem com potência 1,4; atraso e direção de cada um vêm de `hsh` (sorteio fixo, `3D:34`) |

`dirige` precisa do veículo com as rodas na raiz e o resto em `userData.corpo` (como o `caminhao` do v2, `3D:664`).
O `hsh` existe para o kit não consumir o `rng()` da cena (montes e cargas caem nos mesmos lugares do v1).

## Levar para outro estilo
- **2D**: copiar o bloco `<script id="v2">` (`2D:368-426`) para depois do script da cena. Ele redefine `vis`, `ripple`,
  `pulse`, `conta`, `traco`, `arco` e `posTitulo` com os mesmos nomes e parâmetros e expõe o resto em `V2.*` (há aulas
  com `foco()`, `segue()` e `viaja()` próprios). Depende só de `pr`, `eo`, `eio`, `lerp`, `cl` e `kg` do kit base.
  O `<style id="v2">` (`2D:347-367`) é estética do estilo claro: **não levar**.
- **3D**: as seções 1 a 4, 6 e 7 não dependem de material. Num kit de outro estilo, copiar as linhas citadas; `vis`,
  `foco`, `pulse`, `conta`, `pesa` e `posTitulo` só mexem em `style` de elementos HTML.
- **Não levar** (estética da argila): `CSS` (`3D:57`), luz, névoa e `LUZ` (`3D:170-190`), `barro` (`3D:252`), a textura
  de `mancha`, o `chaoPatio` pintado (`3D:851`) e os detalhes novos do `caminhao`.

## O que ficou medido e o que ficou em aberto
- Render de prévia (`--dsf 1.35`, CPU, trava leve, máquina com carga ~11 pela varredura dos robôs):
  3D T08 cap04, 291 quadros: v1 776 s (2,7 s/quadro), v2 1.355 s (4,7 s/quadro). 2D T08 cap07, 360 quadros: v1 74 s
  (0,21 s/quadro), v2 85 s (0,24 s/quadro).
- **O 3D v2 ficou ~1,75x mais caro e a causa não foi isolada.** Numa medição alternada de 15 quadros, tirar o estúdio
  como luz ambiente (`?env=0`) ou o material `barro` (`?br=0`) mudou a mediana em menos de 7 % cada. Faltou medir a
  névoa (`?nv=0`), o contraluz (`?cl=0`), a anisotropia do chão (`?an=1`) e o chão transparente. Nada disso é motion:
  a biblioteca de motion roda em JavaScript por quadro e custa pouco (`dirige` faz ~160 chamadas de `fx`, `pose` 9
  interpolações), mas isso não foi medido em separado.
- Conferido só em quadros parados (folhas de contato): o `CAPS[4]` 3D e o `CAPS[7]` 2D redesenhados; T08 cap00 e cap06
  com o import trocado; T04 cap00 por importmap (kit e `objetos/` juntos no v2), que é o caminho de migração sem
  editar `CAPS`:
  `<script type="importmap">{"imports":{"../../../../perfis/ecoflix/cenas3d/kit3d.js":"../../../../perfis/ecoflix/cenas3d/kit3d_v2.js"}}</script>`
- Não conferido: o movimento em vídeo (só um render do `CAPS[4]` foi olhado por amostra de quadros, antes do último
  ajuste do pó), as outras cenas 3D e 2D no v2, e a cena do Cato com o bloco 2D.
