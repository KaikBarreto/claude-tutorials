# EcoFlix · kit de ilustrações v3 (piloto de 18/11, esperando a aprovação do Kaik)

Um mundo 3D só, dois climas, câmera contínua. Sai a argila; ficam o verde #50D088, a Montserrat, os selos saturados com
ícone branco, nada de marca de terceiros nem de tela do app. Os kits antigos (`../cenas3d/`, `../cenas/`) não mudaram.

- `motor.js`: palco, os dois climas, câmera e estações, planos HTML no espaço, material 3D, componentes e curvas.
- `objetos/`: `caminhao.js` (truck basculante + carga de latinha), `balanca.js` (rodoviária com poste), `latinhas.js`
  (monte e despejo com gravidade).
- `climas.html`: a mesma cena nos dois climas (cap 0 = claro, cap 1 = escuro); serve de vitrine dos componentes.
- Piloto: `planejamento/ecoflix/T08/cenas_v3/cena.html` (ilu04 emendada na ilu05) + `tempos_piloto.json`.

## A regra dos climas
| | Claro (gradientes suaves) | Escuro (vidro) |
|---|---|---|
| É | o mundo físico: pátio, caminhão, balança, material, gente, papel | o mundo dos dados: conta, saldo, documento fiscal, fluxo do sistema, Cato |
| Fundo | gelo com manchas de cor e disco claro, em profundidade | #161618 com brilho verde, pontos e anéis, em profundidade |
| 3D | degradê macio, sombra de mancha, brilho de borda | corpo escuro, fio de luz na borda, emissivo |
| Cartão | branco com sombra larga esverdeada | vidro (degradê translúcido + fio de luz), número aceso |

1. **Nunca os dois no mesmo plano.** Um quadro é claro ou é escuro.
2. **A única superfície escura do mundo claro é a tela de um aparelho** (visor da balança, monitor, celular): é a porta
   dos dados. A troca de clima acontece atravessando uma tela dessas (ou saindo por ela), nunca por corte nem por fusão.
3. **A troca é escondida pela câmera**: `clima(1)` entra no quadro em que a tela cobre o quadro inteiro.
4. O que é igual nos dois: formas, raios, tipografia, verde, selos, curvas, câmera. Só a luz muda.

## Como montar uma cena
```js
import { W, plano, htmlCartao, vis, camera, clima, cena, CENA, piso } from '.../cenas_v3/motor.js';
cena(() => {
  piso();                                            // objetos 3D em CENA (objetos/*.js)
  const c = plano(htmlCartao('scale', 'Bruto', 'a latinha', '3.080 kg'), { pos: [x, y, z], rot: [rx, ry, 0], esc: .0085, clima: 'claro' });
  camera([[0, P0], [2, P1], [4, P2, 'lin']]);        // as estações: uma pose por plano da peça
  return t => { vis(c.e, t, W(0, 'bruto') - .15); }; // função pura de t
});
```
- **Plano** = HTML preso no espaço (posição em metros, giro, `esc` = metros por px), visto pela mesma câmera do 3D.
  `p.e` recebe `vis`, `foco`, `pulso`; `p.pos`/`p.rot`/`p.op` mexem por quadro; `tras: true` fica atrás do 3D (fundo).
  Planos ficam sempre na frente do 3D: ponha-os onde o objeto não deveria cobri-los.
- **Componentes** (o clima vem da classe do plano): `titulo` + `posTitulo` (fica no quadro, fora do espaço: nada passa por
  cima), `htmlCartao` (selo + rótulo + legenda + número; `res` = resultado), `htmlChip`, `selo`, `htmlOp`, `htmlVisor` +
  `ligaVisor` (`troca`, `pesa`), `conta`, `htmlFluxo` + `fluxo` (traço que se desenha, com ponto de luz), `ondaEm`.
- **3D**: `mat(cor, { emi, emiC, bri, alt })` (um material, dois climas), `caixa`, `perfil`, `cil`, `malha`, `grupo`,
  `mancha` (sombra no claro, reflexo no escuro), `piso`, `anel` + `destaque`. Sem luz, sem mapa de sombra, sem pós.
- **Câmera**: chave `[t, { x, y, z, d, az, el, oy, rol, fov }, curva, opções]`, os mesmos nomes do kit 3D antigo. Curva
  padrão `eis` (arranca e para sem tranco); `'lin'` para a deriva lenta de um plano parado. Inércia e respiração de
  operador por cima. `{ reta: true }` leva em linha reta (travessia); `mira` faz o olhar chegar antes do corpo;
  `mergulho(z0, zf)` faz o plano crescer em razão constante (sem zoom brusco). `lugarDeFrente(alvo, olho)` cria o
  referencial do outro lado; `enquadra(plano)` devolve a pose que o põe de frente.
- Regras de direção: um movimento por conceito e com motivo (seguir o assunto, abrir para o contexto, fechar no
  resultado, atravessar a tela); nada cortado pela borda num plano parado; ícone do lucide com o nome literal na página.

## Migrar uma cena antiga
- **3D (`Tnn/cenas3d/cena3d.html`, 35 cenas)**: as chaves de câmera e as âncoras `W()` servem como estão; `vis`, `foco`,
  `conta`, `pesa`, `posTitulo` têm os mesmos parâmetros. Mudam: (1) objeto do kit de argila → objeto v3 (copiar a
  geometria e trocar `M(cor)` por `mat(cor)`; caminhão, balança e latinhas já existem; faltam ~25 de `cenas3d/objetos/` e
  os do kit: monte, fardo, prensa, tambor, pessoa); (2) rótulo `el()` + `ancora()` → `plano()` no espaço; (3) decidir o
  clima de cada momento e onde fica a tela que leva aos dados.
- **2D (`Tnn/cenas/cenas.html`, 218 cenas)**: cada elemento com `left/top` vira um `plano` (o grupo todo num plano só já
  dá câmera e clima; separar em camadas dá paralaxe); `.card/.tag/.op/.most` → `htmlCartao/htmlChip/htmlOp/htmlVisor`.
  Cena de conta, fluxo ou documento = clima escuro; cena de pátio = claro, com objeto 3D quando o objeto é o assunto.
- Modelo: o piloto (`T08/cenas_v3/cena.html`).

## Tempo de render
Prévia `--dsf 1.35` (1728x1080), CPU, trava leve, `nice 19`, máquina carregada (carga ~10 em 2 núcleos): **0,8 s por
quadro no claro (3D + planos) e também 0,8 s no escuro (só planos)**. O piloto inteiro (531 quadros) sai em ~7 min.
