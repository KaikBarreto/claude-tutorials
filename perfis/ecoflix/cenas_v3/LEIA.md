# EcoFlix · kit de ilustrações v3 (estilo aprovado pelo Kaik em 18/11: "Ficou ótimo a prévia da animação")

Um mundo 3D só, dois climas, câmera contínua. Sai a argila; ficam o verde #50D088, a Montserrat, os selos saturados com
ícone branco, nada de marca de terceiros nem de tela do app. Os kits antigos (`../cenas3d/`, `../cenas/`) não mudaram.

- `motor.js`: palco, os dois climas, câmera e estações, planos HTML no espaço, material 3D, componentes e curvas.
- `objetos/`: a biblioteca 3D, um arquivo por objeto (tabela abaixo). Cada arquivo abre com o `uso:` e o `userData`.
- `dados/`: os componentes de DADOS (HTML para `plano()`), um arquivo por componente (tabela abaixo).
- `fundo.js`: os fundos em profundidade dos dois climas (`ceuClaro`, `mundoEscuro` + `E.fundo`), já com o enfeite atrás.
- `auditar.cjs`: a **verificação automática de acabamento**. Toda cena tem de passar nela (seção "Acabamento").
- `vitrine.html` + `vitrine_paginas.js`: tudo com o nome embaixo, 7 páginas, nos dois climas
  (`vitrine.html?k=0&p=1`; imagens em `ecoflix/previa_ilustracoes/v3_vitrine_{claro,escuro}[_1..7].jpg`).
- `climas.html`: a mesma cena nos dois climas (cap 0 = claro, cap 1 = escuro).
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
- **Acabamento**: `plano()` aceita `deco`, `sobre`, `sangra` e `z` (ordem de desenho sem mudar a profundidade); `p.ret()`,
  `enquadraRet`, `uneRet`, `cabe`, `auditar`. Ver a seção "Acabamento": a cena só está pronta quando o `auditar.cjs` aprova.

## Acabamento (obrigatório: toda cena passa na verificação antes da prévia)
Pedido do Kaik na prévia da T08 (18/11): "a animação ficou boa, só cuidado com desalinhamentos". O kit resolve na raiz e
confere sozinho; a cena só precisa usar o que está aqui.
```bash
# a aula inteira, pelas janelas do ilustracoes.json (tempos em $TUT_HOME/tNN/narracao; ou --tempos <pasta>)
nice -n 19 node perfis/ecoflix/cenas_v3/auditar.cjs --aula planejamento/ecoflix/T08 [--id ilu01_quando_usar] [--quadros /dev/shm/v3_t08/aud]
# um capítulo ou um trecho           node .../auditar.cjs <cena.html> <cap> <capNN.json> [--de S --ate S] [--passo 0.5]
# página sem fala (a vitrine)        node .../auditar.cjs vitrine.html 1 - --t 9 --dados '{"pagina":7}'
```
Roda a cena de 0,5 em 0,5 s (sem captura: ~0,2 s por instante, sem trava) e sai com 1 se achar algo. `--quadros` grava o
quadro de cada problema com a marca vermelha. Na página: `window.auditar(t)` devolve a lista; `auditar(t, { marca: true })` desenha.
O que acusa (mínimos em `RESP`, no `motor.js`; medidas em px do desenho, a 1280x800):

| Tipo | Acusa | Como resolver |
|---|---|---|
| `texto` | texto maior que a caixa (cartão, chip, visor, papel) ou a menos de 10 px da borda dela | o `.cartao` já cresce sozinho (`cabe`); fileira de `htmlFluxoCartoes` = todos da largura do maior. Sobrou? `cw` maior ou texto menor |
| `borda` | caixa, seta ou fio PARADO (anda menos de 40 px/s de t - 0,3 a t + 0,3) cortado pela borda ou a menos de 40 px dela | a câmera para com o grupo inteiro no quadro: `enquadraRet`. O que não é do grupo sai de cena (`p.op`, opacidade da parte) antes de a câmera parar. Em trânsito pode cruzar a borda; o assunto da fala, nunca (isso é no olho) |
| `titulo` | conteúdo em cima do título ou a menos de 10 px dele (em qualquer instante) | baixar o desenho (`y` da pose, `topo` do `enquadraRet`), afastar o visor |
| `respiro` | seta a menos de 8 px do cartão ou com respiro diferente nas pontas; fio que nem encosta (0) nem afasta (8); caixas a menos de 8 px | seta de `htmlFluxoCartoes` já sai certa; fio de `htmlFluxo` começa e acaba NA borda da caixa ou a 10 px dela |
| `sobreposicao` | duas caixas uma em cima da outra | afastar; selo posto de propósito na quina: `plano(..., { sobre: true })` |
| `alinhamento` | caixas vizinhas quase alinhadas (topo, meio ou base fora por 1,5 a 6 px) | mesma coordenada, mesma altura de cartão; coisas na mesma conta ficam na MESMA profundidade (`z: n` do plano decide quem fica na frente sem criar paralaxe) |

- **Enfeite fica atrás e nunca cruza conteúdo.** Fundo macio (mancha, brilho, pontos, poeira) = `tras: true`. Traço decorativo
  (anel, linha) = `tras: true, deco: true`: vai para uma camada que o motor recorta atrás de toda caixa de vidro (o anel
  passa atrás do cartão, não por dentro dele). Use `fundo.js` (`ceuClaro()`, `mundoEscuro(EIXO, ZD, EE)` + `E.fundo(cx, cy)`)
  em vez de copiar o fundo de outra cena. Diagrama com fios finos (garfo, ligações): `E.fundo(cx, cy, { aneis: false })`, para
  o anel não se confundir com os fios.
- **Câmera por grupo**: `enquadraRet(lugar, ret, { margem, topo, max, az })` devolve a pose que põe o retângulo (metros;
  `p.ret()` de um plano, `uneRet(a, b)` de vários) inteiro na área útil: 64 px dos lados e de baixo, 150 px livres em cima
  para o título. Fechar em parte de uma fileira = sumir com o resto da fileira (`parte(e, i)`, `seta(e, i)` do
  `fluxoCartoes.js`) enquanto a câmera viaja; ele volta no plano geral.
- **Largura real**: componente que mede o texto pode sair mais largo que o pedido. Posicione pelo que saiu (`p.w`, `p.h`,
  `p.ret()`), não pela conta de cabeça (`4 * CW + 3 * VAO`).
- O que a verificação NÃO vê: objeto 3D (caminhão sob o título, objeto cortado), o assunto da fala cortado em trânsito,
  legibilidade e composição. Continue olhando os quadros (1280x800 e ampliados).

## Migrar uma cena antiga
- **3D (`Tnn/cenas3d/cena3d.html`, 35 cenas)**: as chaves de câmera e as âncoras `W()` servem como estão; `vis`, `foco`,
  `conta`, `pesa`, `posTitulo` têm os mesmos parâmetros. Mudam: (1) objeto do kit de argila → objeto v3 (copiar a
  geometria e trocar `M(cor)` por `mat(cor)`; todos os objetos do kit de argila já existem em `objetos/`: ver a
  tabela da biblioteca); (2) rótulo `el()` + `ancora()` → `plano()` no espaço; (3) decidir o
  clima de cada momento e onde fica a tela que leva aos dados.
- **2D (`Tnn/cenas/cenas.html`, 218 cenas)**: cada elemento com `left/top` vira um `plano` (o grupo todo num plano só já
  dá câmera e clima; separar em camadas dá paralaxe); `.card/.tag/.op/.most` → `htmlCartao/htmlChip/htmlOp/htmlVisor`.
  Cena de conta, fluxo ou documento = clima escuro; cena de pátio = claro, com objeto 3D quando o objeto é o assunto.
- Modelo: o piloto (`T08/cenas_v3/cena.html`), que passa no `auditar.cjs` sem nenhum problema.

## Biblioteca · objetos 3D (`objetos/`)
Mesma convenção em todos: `nome(pai, [x, y, z], o)` devolve o grupo; base em y 0; medidas REAIS em metros (pessoa 1,72;
truck 7,3; galpão 12 x 8). Material `mat()` do motor: o mesmo objeto serve nos dois climas, sem trocar nada. `userData.topo`
= ponto acima do objeto (prenda ali o chip). Objeto pequeno (registradora, impressora, computador, cédula, folha, placa,
pino) tem `o.s`/`o.w` para crescer até ler ao lado de gente e caminhão. Peças de material têm tamanho de ilustração (lata
de 26 cm), igual à carga do caminhão. Construção como ícone de estação: `g.scale.setScalar(.4)`.

| Arquivo · função | Parâmetros (`o`) | Animações e pontos |
|---|---|---|
| `caminhao.js` · `caminhao(pai, o)` | `tipo` 'truck' \| 'tres4' (3/4), `bau` 'basculante' \| 'grade' \| 'nenhum', `carga` nº de latinhas \| 0 \| 'bateria', `placa` 'ABC1D23', `cor`, `cubo` | `dirige(T, x, altura, { sobe, arfa })`, `bascula(T, ang)`; `userData.bau`, `dim`, `carga`, `locais` |
| `poliguindaste.js` · `poliguindaste(pai, o)` | os do caminhão | `posiciona(T, x, z, dir)`, `poseCacamba(T, k, s)` (0 no chão → 1 nos trilhos), `lxCarga(s)` |
| `cacambaEstacionaria.js` | `c` 3.4, `l` 1.7, `h` 1.1, `cor` | `boca`, `pinos`; carga com `pecas()` |
| `balanca.js` · `balanca` (rodoviária) | `c`, `l`, `h`, `rampa`, `poste`, `hp` | `userData.altura(x)`, `poste` (visor) |
| `balancaPlataforma.js` | `c` 1.2, `l` 1.0, `hp` | `sup` (tampo), `topo`/`tela` (visor), `saida` (cabo) |
| `carroca.js` · `carroca` | `carga` (tipo), `n`, `cor` | `puxa(c, x)`; `rodas`, `dentro` |
| `pessoa.js` · `pessoa` | `s`, `pele`, `cabelo`, `camisa`, `calca`, `coque`, `bone`, `colete` | `userData.anda(fase, braco)`; `mao[0..1]` |
| `motorista.js` · `motorista` | os da pessoa, `braco` | `estende(a)`; `mao` (segura a folha) |
| `monte.js` · `monte` | `tipo` latinha \| pet \| ferro \| papelao \| cobre \| aluminio \| plastico \| bateria \| misto, `n`, `r`, `rz`, `h`, `s` | `cai(m, t, a, { d, queda, alt })`; `pecas(pai, tipo, P, { s })`, `pontosMonte(n, r, rz, h, y0)` |
| `latinhas.js` · `domo`, `despeja` | alvo do despejo do caminhão | `despeja(im, locais, alvo, t, a, o)` |
| `baterias.js` · `baterias` | `nx`, `nz`, `camadas`, `P`, `s` | `lotes` (para `cai`) |
| `fardo.js` · `fardo` (`fardoLatinhas`, `fardoPapelao`) | `tipo` latinha \| pet \| papelao \| aluminio \| cobre \| plastico \| ferro, `w`, `h`, `d`, `cintas`, `mancha` | empilha em `[x, h, z]` |
| `saco.js` · `saco` (`sacoAberto`) | `aberto`, `carga` (tipo), `n`, `s`, `cor` | `boca`, `lotes` |
| `bigBag.js` · `bigBag` | `estado` 'cheio' \| 'aberto' \| 'vazio', `carga`, `w`, `h` | `h`, `lotes` |
| `tambor.js` · `tambor` | `cor`, `corE`, `aberto` | `boca` |
| `cacamba.js` · `cacamba` (de pátio) | `s`, `cor` | `boca`, `dentro` |
| `palete.js` · `palete` | `mancha` | `sup` |
| `prensa.js` · `prensa` | `cor` | `aperta(p, 0..1)`; `boca`, `saida` |
| `esteira.js` · `esteira` | `c` 9, `l` 1.2, `h` .9 | `corre(e, dist)`; `topo` |
| `ima.js` · `ima`, `trilho` | `R` | `campo(im, 0..1)`; `ponta`, `topo` |
| `baia.js` · `baia` | `c` 4, `l` 3, `h` 1.5, `cor` (borda) | `dentro`, `topo` |
| `cancela.js` · `cancela` | `l` 4.5 | `ergue(c, 0..1)` |
| `chaoPatio.js` · `chaoPatio` | `c`, `l`, `passo`, `faixa` [z...] | |
| `guiche.js` · `guiche` | `c`, `l`, `h`, `cor`, `laje` | `balcao`, `janela` |
| `registradora.js` · `registradora` | `s`, `valor`, `cupom` | `userData.abre(p)`, `visor(txt)`, `cupom.userData.sai(p)` |
| `impressora.js` · `impressora` | `s`, `cupom` { tipo, h } | `imprime(i, 0..1)`; `fenda`, `entrada` |
| `cupom.js` · `cupom` | `w`, `h`, `tipo` 'generico' \| 'teste' \| 'branco', `quando`, `dobra` | `userData.sai(p)` |
| `computador.js` · `computador` | `s`, `mesa` | `tela` { centro, w, h, incl }: a porta dos dados |
| `cabo.js` · `cabo(pai, pontos, o)` | `r`, `cor`, `conector` | `caboAte(c, p)`, `sinal(c, u)` |
| `fio.js` · `fio(pai, cor, r)` | | `f.liga(a, b, p)` |
| `folha.js` · `folha` | `w`, `h`, `cor`, `linhas` | mexer em position/rotation |
| `pasta.js` · `pasta` | `w`, `h`, `cor` | `dentro`, `boca` |
| `placa.js` · `placa(pai, pos, texto, o)` | `w` | `userData.troca(texto)` |
| `cedula.js` · `cedula`, `maco(pai, pos, n, o)` | `w`, `d`, `cor` | |
| `pinoLocal.js` · `pinoLocal` | `s`, `cor` | flutuar com position.y |
| `galpao.js`, `fundicao.js` | `c`, `l`, `h` (+ `porta`, `cor`, `telhado`) | `porta`, `placa`, `chamine` |
| `banco.js` · `banco` | `s` | `porta` |
| `portao.js` · `portao` | `vao`, `h`, `cerca`, `hc`, `placa` (texto) | `placa`, `vao` |
| `estrada.js`, `porticoEstado.js` | `c`, `l` / `l`, `h` | `topo` (chip da sigla) |

O que era do kit de argila e mudou de nome: `balancaPatio` → `balanca({ c, l })`; `latinhas(pai, P)` / `pets(pai, P)` →
`pecas(pai, 'latinha' | 'pet', P)`; `anda` → `dirige`; `M(cor)` → `mat(cor)`; `mostrador` → `htmlVisor` num `plano`.

## Biblioteca · componentes de dados (`dados/`)
Convenção: `htmlNome(o)` devolve o HTML para um `plano(..., { clima: 'escuro' })` e `nome(p.e, t, a, b, o)` anima (entra em
`a`, sai em `b`; `o.tempos` = instantes das partes, vindos de `W()`; sem ele, escalonado). Depois valem `foco` e `pulso`.
Leem as variáveis do clima: no escuro são vidro aceso; no claro, papel branco. Ícone = nome do lucide, literal na página.

| Arquivo | Monta | Anima |
|---|---|---|
| `documento.js` | `htmlDocumento({ icone, tipo, sigla, numero, campos [[k, v]], itens [[desc, qtd, valor]], total [k, v], status, statusCor, cor, w })` (nota, manifesto, MTR: layout do kit, sem marca) | `documento`: campos, itens, total, chave e o carimbo que bate |
| `extrato.js` | `htmlExtrato({ icone, titulo, sub, linhas [[icone, rot, sub, valor]], total [k, v], fmt, w })` (nº = R$ com sinal; texto = como está) | `extrato` (linhas em cascata, total que conta), `marca(e, i, t, a)` |
| `barras.js` | `htmlBarras({ titulo, sub, dados [[rot, v]], destaque, fmt, selo, w, h })` | `barras`: crescem do chão, valor conta |
| `grafLinha.js` | `htmlGrafLinha({ titulo, sub, pontos, rotulos, valor, selo, w, h })` | `grafLinha`: a linha se desenha, a área acende, o ponto final bate |
| `linhaTempo.js` | `htmlLinhaTempo({ etapas [[icone, rot, sub, cor]], w, vertical, passo })` (etapas da largura do nome mais comprido: não se encostam) | `linhaTempo(..., { tempos, pendente })`: o trilho acende até a etapa |
| `fluxoCartoes.js` | `htmlFluxoCartoes({ cartoes [[icone, rot, sub, 'res' \| 'a' \| 'n']], cw (largura MÍNIMA), vao, respiro, vertical })`: cartões todos da largura do texto mais comprido, seta com o mesmo respiro (12) nas duas pontas | `fluxoCartoes`: seta com ponto de luz e cartão; `parte(e, i)`, `seta(e, i)` |
| `balao.js` | `htmlBalao({ lado 'e' \| 'd', icone, nome, texto, w })` (Cato: ícone genérico, sem logo) | `balao(..., { pensa, d })`: pontinhos e texto palavra a palavra |
| `calendario.js` | `htmlCalendario({ mes, ano, inicio, dias, hoje, marcas [[dia, '' \| 'a']], faixa [de, ate], icone })` | `calendario`: dias em cascata, marcas batem |
| `cadeado.js` | `htmlCadeado({ px })`, `htmlPermissao({ icone, papel, sub, itens [[rot, ligado]] })` | `cadeado(..., { abre })`, `permissao(..., { liga [[i, t]] })` |
| `moeda.js` | `htmlMoeda({ px, txt })`, `htmlSaldo({ rot, sub, valor, moedas, res, cor 'v' })` | `moeda` (entra girando), `saldo(..., { de, tConta })`: pilha cai, número conta |

Os do motor continuam: `htmlCartao`, `htmlChip`, `htmlOp`, `htmlVisor` + `ligaVisor`, `htmlFluxo` + `fluxo`, `titulo`.

## Exemplo mínimo · duas estações (claro → escuro)
```js
import { W, kg, vis, cl, eis, CENA, piso, camera, posCam, olho, mergulho, lugarDeFrente, plano, clima, cena, GL, htmlVisor, ligaVisor } from '.../cenas_v3/motor.js';
import { balancaPlataforma } from '.../cenas_v3/objetos/balancaPlataforma.js';
import { saco } from '.../cenas_v3/objetos/saco.js';
import { htmlDocumento, documento } from '.../cenas_v3/dados/documento.js';
cena(() => {   // ícone usado: 'file-text'
  piso(); const b = balancaPlataforma(CENA, [0, 0, 0]); saco(b, [0, b.userData.sup, 0]);
  // estação 1 (claro): o saco na balança e o visor, que é a porta dos dados
  const P1 = { x: 0, y: .8, z: 0, d: 7, az: .3, el: .25 }, VP = b.userData.topo, EIXO = lugarDeFrente(VP, posCam(P1));
  const v = plano(htmlVisor(['Peso']), { em: EIXO, pos: [0, 0, 0], esc: .004 }); ligaVisor(v.e); v.e.vn.textContent = kg(42);
  // estação 2 (escuro): do outro lado do visor, no mesmo eixo, o documento
  const doc = plano(htmlDocumento({ icone: 'file-text', tipo: 'Ticket', sigla: 'TK', numero: 'Nº 0118', campos: [['Material', 'Cobre'], ['Peso', '42 kg']], status: 'Pesado' }),
    { em: EIXO, pos: [0, 0, -13], esc: .01, clima: 'escuro' });   // 11 m além de onde a câmera para (z = -2)
  const tM = W(1, 'ticket') - 1.2, tC = tM + 1.5, P2 = EIXO.pose({ x: 0, y: 0, z: -13, d: 11 });
  camera([[0, P1], [tM, { ...P1, d: 6.6 }, 'lin'], [tC, P2, mergulho(EIXO.local(posCam(P1))[2], -2), { reta: true, mira: x => eis(cl(x * 2)) }]]);
  return t => {
    const dentro = EIXO.local(olho())[2] < .6 ? 1 : 0;        // a tela cobriu o quadro: troca o clima escondido
    clima(dentro); GL.style.visibility = dentro ? 'hidden' : 'visible'; v.op = dentro ? 0 : 1; doc.op = dentro;
    vis(v.e, t, .3); documento(doc.e, t, tC - .4);
  };
});
```

## Tempo de render
Prévia `--dsf 1.35` (1728x1080), CPU, trava leve, `nice 19`, máquina carregada (carga ~10 em 2 núcleos): **0,8 s por
quadro no claro (3D + planos) e também 0,8 s no escuro (só planos)**. O piloto inteiro (531 quadros) sai em ~7 min.
Com a biblioteca (18/11): cena de teste com caminhão (250 latas, placa), balança, monte de PET caindo (150), baia com
monte de cobre, prensa, 2 fardos, 2 pessoas e 4 planos, `--dsf 1.35`, `nice 19`, trava leve, carga ~4: **0,63 s por quadro**
(0,09 s de cena + 0,55 s de captura). Cada monte são 2 a 6 chamadas de desenho (lotes); o custo é a captura, não o 3D.
No clima escuro, corpo de objeto usa `emi` baixo (.1 a .3) e só luz, tela e destaque passam de 1: é o que mantém o vidro.

## Render final e piscadas (19/11)
Renderize em `--dsf 1.35` (a caixa da ilustração no palco tem 1587x992; `--dsf 2` não ganha nitidez e, nas cenas escuras de
vidro, o Chromium fotografa antes de pintar um bloco: cartões somem por 1 a 3 quadros). Depois de todo render:
`python3 -I perfis/ecoflix/cenas_v3/piscadas.py <cena>.mp4` (sai com 1 se algum elemento some e volta).
