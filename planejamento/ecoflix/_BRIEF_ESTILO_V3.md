# Briefing do estilo v3 das ilustrações · trilha EcoFlix (piloto para o Kaik aprovar)

## O que o Kaik decidiu (18/11, vendo a folha `planejamento/ecoflix/estilos/`, imagem em
`/home/claude/ecoflix/previa_ilustracoes/estilos_10.jpg`)
- "**vidro escuro** [painel 9] e **gradientes suaves** [painel 10] me pegaram, daria pra intercalar de forma que não
  fique bagunçado? e esses estilos, quando necessário, se achar bom, ter algum tipo de **3D** também."
- "as transições entre um conceito e outro, se conseguir, **parecer que foram cenas e planos planejados, com transição
  de câmera 3D como se fosse um plano que vai mudando, a câmera dando zoom em relação ao plano** etc."
- Antes: "animações de maior qualidade técnica de motion, princípios do design, estética"; "evite zooms bruscos".
A argila 3D sai. A identidade continua: verde #50D088, Montserrat, selos saturados com ícone branco, nada de marca de
terceiros nem tela do app, mesmos textos e números das cenas atuais.

## A ideia a realizar (você é o diretor de arte e de motion; refine, não precisa seguir à risca)
- **Um sistema só, dois climas.** Vidro escuro e gradientes suaves são o MESMO mundo com luz diferente: mesmas formas,
  mesma tipografia, mesmos raios, mesmo verde, mesmo motion. Regra de uso que não vira bagunça (proposta): **clima claro
  (gradientes) = o mundo físico** (pátio, caminhão, balança, material, gente, papel); **clima escuro (vidro) = o mundo
  dos dados** (conta, saldo, documento fiscal, fluxo do sistema, Cato). Nunca os dois misturados no mesmo plano; a troca
  acontece só na passagem de um conceito para o outro e é motivada pela câmera (ex.: a câmera mergulha no visor da
  balança e o visor vira o painel escuro; ao sair, volta o dia). Se tiver regra melhor, proponha e aplique.
- **Planos planejados, câmera contínua.** A cena é um espaço 3D com "estações" (planos/cartões/objetos em profundidade).
  Passar de um conceito a outro é um movimento de câmera (dolly, travelling, órbita curta, push-in num plano que vira o
  quadro seguinte, pull-back que revela o contexto), com paralaxe entre camadas, foco que guia o olho e inércia de
  operador humano. Sem corte seco, sem zoom brusco, sem girar à toa: cada movimento tem motivo.
- **3D quando ajuda.** Objeto físico (caminhão, balança, fardo, prensa) pode ser 3D de verdade ou 2,5D em camadas, no
  acabamento dos dois climas (vidro/emissivo no escuro; gradiente, sombra macia e brilho suave no claro). Conceito
  abstrato fica em planos 2D dentro do mesmo espaço 3D (cartões de vidro, gráficos, contas).
- **Motion**: aproveite a biblioteca do piloto anterior (`perfis/ecoflix/cenas3d/MOTION_V2.md`, `kit3d_v2.js`,
  `perfis/ecoflix/cenas/cenas_ecoflix_v2.html`: curvas, molas, stagger, contagem, câmera com inércia), adaptando ao estilo.

## Técnica (não negociável)
- Render quadro a quadro, determinístico em `t`: a página expõe `window.setup(dados)` e `window.R(t)`
  (`docs/09-aula-ilustrada.md`; renderizador `ferramentas/edit/cenas/render_cenas.cjs`, 1280x800 lógicos, `--dsf`).
  CPU sem GPU (WebGL por software): `backdrop-filter` e blur grande são caros ou saem errados; prefira gradientes,
  camadas pré-borradas e emissivo falso. Meça o tempo por quadro e mantenha perto de 1-2 s em `--dsf 1.35`.
- three.js local: `perfis/ecoflix/cenas3d/three.module.min.js`. Fontes: `ferramentas/web/fonts`. Ícones: lucide (como o
  `render_cenas.cjs` injeta `window.ICONS`). Sem rede.
- Âncoras de fala como nas cenas atuais (`W(linha, 'palavra')`; veja `planejamento/ecoflix/T08/cenas3d/cena3d.html` e
  `T08/cenas/cenas.html`), tempos em `T08/cenas/tempos/capNN.json`, lista em `T08/cenas/ilustracoes.json`.

## Entregar
1. Kit novo `perfis/ecoflix/cenas_v3/` (motor, os dois climas, câmera/estações, componentes: título, selo, chip, cartão de
   vidro, visor, número com contagem, seta/fluxo; objetos físicos em `objetos/`) + `LEIA.md` curto (API, regra dos climas,
   como montar uma cena, como migrar uma cena antiga, tempo de render).
2. **Piloto**: a sequência da T08 que junta físico e dados, numa cena só com câmera contínua: `ilu04_entrada_saida`
   (pesou cheio 9.460 kg, descarregou, pesou vazio 6.380 kg, diferença 3.080 kg de latinha) emendada na
   `ilu05_conta_liquido` (Bruto 3.080 − Tara 0 − Impureza 61,6 = Líquido 3.018,4 kg). Mesmos textos, números e âncoras das
   cenas atuais (o caminhão vazio NÃO é "tara" aqui: veja `_BRIEF_3D.md` → Tara). Arquivo:
   `planejamento/ecoflix/T08/cenas_v3/cena.html`.
3. Vídeo do piloto com a duração real das falas: `/home/claude/ecoflix/previa_ilustracoes/estilo_v3_piloto.mp4`
   (`--dsf 1.35`, até 25 MB) e uma folha `estilo_v3_piloto.jpg` com 12 quadros. Render na trava leve
   (`flock /home/claude/ecoflix/.stills.lock nice -n 19`), com `RENDER_PAUSA=0`, em trechos de até 13 s juntados com o
   concat do ffmpeg. **Olhe os quadros** (inclusive o meio de cada transição de câmera e o primeiro segundo) e itere até
   estar com cara de peça planejada por um estúdio: composição, hierarquia, ritmo, nada cortado, nada sobre o título.
4. Uma folha `estilo_v3_climas.jpg` (2 quadros lado a lado) mostrando o mesmo componente/objeto nos dois climas, para o
   Kaik ver que é um sistema só.

## Limites
- Escreva só em `perfis/ecoflix/cenas_v3/`, `planejamento/ecoflix/T08/cenas_v3/` e
  `/home/claude/ecoflix/previa_ilustracoes/`. Não edite kits antigos, cenas existentes, `ferramentas/`, roteiros nem
  `PRODUCAO.md`. Temporários em `/dev/shm/estilo_v3/` (apague no fim; cuidado para não criar pasta fora dali).
- Sem commit. Nada de `pkill`/`killall`, `git stash/reset/clean`; `rm` só com caminho absoluto literal.

## Relatório final (até 150 palavras)
A regra dos climas que ficou, como são as transições de câmera, onde entrou 3D, tempo de render por quadro, esforço para
migrar as cenas que já existem (35 em 3D e as 2D das 26 aulas) e os caminhos dos arquivos.
