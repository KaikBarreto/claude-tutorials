# Kit 3D da EcoFlix (argila)

Ilustração de conceito em 3D de argila (three.js r170, local) com rótulos em HTML por cima, no estilo saturado da marca.
Piloto aprovado pelo Kaik em 11/11 (T07 cap06). Mesma API da cena 2D: `window.setup(dados)` e `window.R(t)`.

- `kit3d.js`: o kit (módulo ES). `three.module.min.js` + `three.LICENSE` (MIT): o three.js que ele importa.
- `vitrine.html`: todos os objetos com o nome da função embaixo (comando de render no topo do arquivo).

## Cena
Página com `<script type="module">` que importa o kit (de `planejamento/ecoflix/Tnn/cenas3d/`:
`'../../../../perfis/ecoflix/cenas3d/kit3d.js'`; copiando a cena para outro lugar, ajuste o caminho) e chama
`cena(d => { ...monta...; return t => {...} }, opções)`. Exemplos: `planejamento/ecoflix/T07/cenas3d/cena3d.html`
(tara, impureza, carroça na balança) e `T08/cenas3d/cena3d.html` (caminhão na balança, basculando, abas; um `CAPS` por
capítulo). Opções: `sombra` (meia largura coberta pela sombra; 6,5 para a mesa, 11 para caminhão), `mapa` (1024/2048),
`chao` (`false` com o `chaoPatio`), `aquece`, `semente`.

```bash
node ferramentas/edit/cenas/render_cenas.cjs 6 <capNN.json> saida.mp4 --html <cena3d.html> --de <at> --ate <at+dur>
# --dsf 1.35 = prévia 1728x1080 (~0,5 s/quadro); --dsf 1 = conferência; sem --dsf = 2560x1600 (~1 s/quadro)
```
O `render_cenas.cjs` sobe o Chromium com `--allow-file-access-from-files` (sem ela o import de módulo em `file://` cai
no CORS). Prévia longa: em trechos de até ~13 s, cada um na trava leve, e junte com o concat do ffmpeg (`-c copy`).
No `ilustracoes.json` da aula, `"3d": "cenas3d/cena3d.html"` marca a cena que vai em 3D; a 2D fica de reserva.

## O que tem
- **Fala**: `W(linha, 'palavra', n, 's'|'e')`, `L(i)`, `LE(i)`; tempo `eo`, `eio`, `pr`, `lerp`; sorteio `rng`, `ri`, `pega`.
- **Rótulos HTML**: `titulo` + `posTitulo`, `selo`, `chip`, `coluna` + `op` (a conta), `cartao`, `mostrador` (painel
  escuro, número verde; `troca` do rótulo 1 ao 2), `onda`; `vis`, `pulse`, `ripple`, `conta`, `kg`, `kgd`, `ic`.
  Presos ao mundo com `ancora(e, [x,y,z], ax, ay, dx, dy)`; `tela(p)` dá o px de um ponto; `mundo(obj, p)` o ponto no mundo.
- **3D**: `camera([[t, {x,y,z,d,az,el,oy}, 'eio'|'lin', arco], ...])` (movimento suave entre chaves), luz e sombra macia,
  `GL.style.opacity` (o mundo entra sem transparência nos objetos), `COR` e `ARGILA` (verde #50D088, escuro #121212, âmbar
  #F2B63D), `M`/`MU`, `argila` + `tinge` (argila crua → cor na palavra), `cresce`, `pulso`, `mancha` (sombra de contato),
  `anel` + `destaque`, `rbox`, `torno`, `domo` (pontos de monte), `peca`, `lote` + `transfere` (as peças voam de um lugar
  a outro, cada uma no seu tempo) + `ordemPor`.
- **Objetos** (unidade ≈ metro; frente do veículo para +x; roda gira em z): `saco`, `sacoAberto`, `tambor`, `cacamba`,
  `monte`, `palete`, `fardo`, `carroca`, `balancaPatio` (`topo` do poste, `altura(x)` das rampas), `caminhao` (verde ou
  `cor`; `eixos` 2|3; `bau` basculante|grade; `carga` latinha|bateria|vazio) + `anda` (rampa e rodas) + `bascula`, `roda`,
  `latinhas`, `baterias`, `prensa` + `aperta`, `fardoLatinhas`, `impressora` + `imprime`, `computador` (tela lisa) e
  `chaoPatio` (juntas e faixa âmbar).

## Regras
Nada de marca, tela do app ou dado inventado: rótulos do inventário da aula, números da fala. Ícone lucide com o nome
literal na página da cena (`ic('ticket', 28)`): o renderizador só procura no HTML. Tara é a embalagem: na dupla pesagem o
caminhão vazio não é tara. Quadros na trava leve com `nice -n 19`.
