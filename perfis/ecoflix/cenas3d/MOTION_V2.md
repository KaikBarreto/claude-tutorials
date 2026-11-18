# Motion e acabamento v2 · kit 3D e kit 2D da EcoFlix (piloto de 18/11)

Pedido do Kaik: ilustrações "mais refinadas, com mais qualidade técnica de motion, princípios do design, estética". A
identidade aprovada não muda (argila fosca, selos saturados com ícone branco, verde #50D088, Montserrat): sobe o
acabamento. **Piloto, esperando a aprovação do Kaik**: o v1 continua intacto e as cenas atuais continuam renderizando nele.

- `kit3d_v2.js` (este diretório) e `../cenas/cenas_ecoflix_v2.html`: os kits.
- Pilotos: `planejamento/ecoflix/T08/cenas3d/cena3d_v2.html` (CAPS[4], dupla pesagem) e
  `planejamento/ecoflix/T08/cenas/cenas_v2.html` (CAPS[7], "Só no Finalizar", o conceito abstrato escolhido).
- Antes/depois: `~/ecoflix/previa_ilustracoes/motion_v2_3d.mp4`, `motion_v2_2d.mp4` e as folhas `.jpg`.

## Princípios aplicados
1. **Curva com intenção.** Entrada arranca na hora e desacelera por muito tempo (`eo5`); saída curta e acelerando (`ei`);
   movimento com peso (`eio5`); `passa` (passa um pouco e volta) só em quem entra por escala. Nada linear: até a deriva
   `'lin'` da câmera começa e termina em curva.
2. **Peso.** Mola amortecida analítica (`mola`, resposta ao degrau) e `golpe` (resposta ao impulso). O caminhão arranca e
   freia com a suspensão respondendo à aceleração; a carroceria sobe quando a carga sai; a caçamba desce e bate; a peça
   cai acelerando e dá um quique curto; a leitura da balança passa do valor e volta.
3. **Uma coisa puxa a outra** (sobreposição e escalonamento): a chamada do título entra 90 ms antes do título; a caçamba
   começa a subir no fim da ré; o caminhão arranca com a caçamba ainda descendo; filas com 60 a 120 ms (`escalona`).
4. **Ação secundária discreta**: pó (`poeira` + `sopra`), suspensão, luz do mostrador âmbar enquanto a leitura mexe,
   ampulheta que balança no cartão que espera.
5. **Um foco por momento** (`foco`): o que não é o assunto recua em opacidade e saturação, sem sumir (o que foi dito
   continua legível). O rótulo entra depois do objeto que nomeia; número que é resultado conta até o valor.
6. **Câmera de operador**: chaves alisadas por uma janela em sino (inércia), respiração de milésimos de radiano, e o
   enquadramento acompanha o assunto (perto na pesagem, abre na descarga, fecha na conta). Sem corte e sem zoom brusco.
7. **Luz com direção e profundidade**: sol morno mais de lado (a sombra cai à vista), céu frio, contraluz que solta a
   silhueta, estúdio fraco em tudo (a face de baixo escurece), névoa clara, chão que se desfaz no fundo da página.
8. **Material com variação**: argila com manchas largas e miúdas na cor e na rugosidade, escuro de contato perto do chão
   e brilho rasante leve. Concreto pintado (manchas, grão, juntas com sombra e fio de luz, faixa gasta).
9. **Um sistema só de rótulo** (3D e 2D): raios `--r1/--r2/--r3/--rp`, sombras `--s1/--s2/--s3` (com a mesma direção da
   luz do 3D), fio de luz em selo e chip (`--lz`), ritmo de letra do título e dos números.

Tudo continua função pura de `t` (nada de relógio, estado entre quadros ou física com passo): `dirige` calcula a
suspensão por convolução da aceleração de `fx(t)`, e a câmera alisa amostrando as próprias chaves.

## O que mudou no kit 3D
| Área | v1 | v2 |
|---|---|---|
| Curvas | `eo`, `eio` | + `eo5`, `ei`, `eio5`, `passa`, `mola`, `golpe`, `escalona` (as antigas ficam) |
| `vis` | cúbica nos dois sentidos | opacidade chega antes da posição, cauda longa; saída curta; `sc < .9` passa e volta |
| `pulse`, `pulso`, `ripple`, `destaque`, `cresce` | seno simétrico / cúbica | golpe de mola, onda mais longa, anel e objeto que passam e assentam |
| `conta` | cúbica | cauda longa; **novo `pesa(mostrador, ...)`**: leitura que passa e volta, de 10 em 10 kg, luz âmbar → verde |
| `posTitulo`, `mostrador.troca` | sobem juntos / troca seca | chamada antes do título, letras fechando; rótulo 1 sobe e sai, 2 sobe e entra |
| Câmera | interpolação por trecho | média em sino de 9 amostras (`inercia`, padrão 0,34 s) + respiração (`respira`) |
| Luz | hemisfério 1,7 + sol 2,3 + preenchimento | sol morno de lado 2,7, hemisfério 0,82 frio/quente, contraluz, estúdio 0,34, névoa (`nevoa`) |
| Material `M`/`MU` | cor chapada | `barro`: variação de cor e rugosidade, escuro de contato, brilho rasante (sem textura) |
| `mancha` | degradê de 3 paradas | miolo mais denso, borda mais longa |
| `transfere` | voo suave (eio) | queda com gravidade e quique; `{ suave: true }` volta ao voo do v1 |
| `caminhao` | um grupo só | rodas na raiz, o resto em `userData.corpo`; moldura de janela, vinco e maçaneta da porta, saia, escapamento |
| `chaoPatio` | caixa + juntas em malha | placa com textura feita na hora, bordas que se desfazem (`borda`, `tom`) |
| Novos | | `suspende`, `dirige`, `poeira`, `sopra`, `foco`, `pesa` |

Opções novas de `cena(..., {inercia, respira, nevoa})`: `inercia: 0` e `respira: 0` devolvem a câmera do v1.
O sorteio da cena (`rng`) anda igual: montes e cargas caem nos mesmos lugares (o kit usa um sorteio próprio, `hsh`).

## O que mudou no kit 2D
`cenas_ecoflix_v2.html` = o v1 inteiro + dois blocos no fim (`<style id="v2">` e `<script id="v2">`, entre os comentários
`KIT 2D V2 · INÍCIO/FIM`). O estilo troca o acabamento (as mesmas fichas do 3D); o script redefine `vis`, `ripple`, `pulse`,
`conta`, `traco`, `arco` e `posTitulo` com os mesmos nomes e parâmetros. O que é novo fica em `V2.*` (`eo5`, `ei`, `eio5`,
`passa`, `mola`, `golpe`, `escalona`, `foco`, `curso`, `sobre`, `pesa`), porque há aulas com `foco()`, `segue()` e
`viaja()` próprios.

## Tempo de render por quadro (prévia `--dsf 1.35`, 1728x1080, CPU, trava leve, `nice 19`)
Medido no mesmo lote, um depois do outro, com a varredura dos robôs rodando (carga da máquina entre parênteses):

| Cena | v1 | v2 |
|---|---|---|
| 3D · T08 cap04 (291 quadros) | __A3__ | __D3__ |
| 2D · T08 cap07 (360 quadros) | __A2__ | __D2__ |

Nenhum efeito de tela (sem pós-processamento, sem passe extra). O custo novo é por pixel no material de argila (três
senos), a névoa, o estúdio como luz ambiente e o chão com textura (que tira ~30 malhas de junta da cena).

## Migração das cenas existentes
### 3D (12 arquivos `Tnn/cenas3d/cena3d.html`, 35 cenas) · ganham sozinhas
Um passo por arquivo, sem tocar em nenhum `CAPS`: trocar o caminho do import para `kit3d_v2.js`. Quando a cena usa
`objetos/*.js` (que importam `../kit3d.js`), em vez disso pôr um importmap no `<head>`, antes do módulo, que leva o kit
e os objetos juntos para o v2:
```html
<script type="importmap">{"imports":{"../../../../perfis/ecoflix/cenas3d/kit3d.js":"../../../../perfis/ecoflix/cenas3d/kit3d_v2.js"}}</script>
```
Conferido assim, sem editar a cena: T08 cap00 e cap06 (import trocado) e T04 cap00 (importmap, com `objetos/`).
Vêm de graça: curvas de entrada e saída, pulso, contagem, título escalonado, câmera com inércia, luz, sombra, névoa,
argila, sombra de contato, queda das peças, caminhão novo e chão do pátio.

Depois de trocar, **olhar os quadros de cada cena** (a folha de sempre), porque três coisas mudam de lugar:
- a sombra cai mais para a direita (o sol está mais de lado): conferir se não cobre rótulo preso ao chão;
- o `chaoPatio` agora se desfaz nas bordas: cena que mostrava a quina da placa de propósito passa `borda: [0, 0, 0, 0]`;
- câmera com duas chaves quase juntas (um "corte") vira um movimento de ~0,7 s: `inercia: 0` nessa cena.

### 3D · o que pede mudança na cena (opcional, cena por cena)
| Para ter | Trocar |
|---|---|
| Suspensão no veículo | `anda(T, x, h)` por `dirige(T, t, fx, h, {carga, golpes})`, com `fx = u => ...` (a posição como função do tempo) |
| Leitura de balança que assenta | `conta(most.mn, ...)` por `pesa(most, t, a, d, v0, v1)` |
| Pó | `const p = poeira(CENA)` na montagem e `sopra(p, t, a, [x, y, z], {...})` no quadro |
| Um foco por momento | `foco(e, t, a, b)` depois do `vis` do mesmo elemento |
| Peça levada (não jogada) | `transfere(..., { suave: true })` |

Modelo: o `CAPS[4]` do `T08/cenas3d/cena3d_v2.html`.

### 2D (26 arquivos `Tnn/cenas/cenas.html`) · ganham sozinhas
Colar os dois blocos `KIT 2D V2` do `cenas_ecoflix_v2.html` antes do `</body>` (o script tem de vir depois do script da
aula). Nenhum `CAPS` muda. Conferir a folha de cada aula: o `pulse` agora bate e assenta (pico ~25 % maior e mais cedo) e
a entrada tem cauda ~30 % mais longa (quem dependia do fim exato de um `vis` para emendar outro movimento pode pedir
ajuste de 0,1 s). Cena do Cato (T21, tema escuro): o bloco de estilo troca raio, sombra e ritmo de letra de `.card`,
`.tag`, `.ico`, `.op` e `.most` e redefine o fundo do `#st`; conferir a folha dela antes de adotar.

Redesenho com o que é novo (`V2.foco`, `V2.curso` + `V2.sobre` para algo viajar sobre um traço, `V2.golpe`): cena por
cena, como o `CAPS[7]` do `T08/cenas/cenas_v2.html`.
