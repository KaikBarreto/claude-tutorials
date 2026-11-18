# Briefing do refino de motion e estética das ilustrações · trilha EcoFlix (piloto)

Pedido do Kaik (18/11): "as ilustrações que estava construindo, agora com fable 5.2 tente fazer algo mais refinado,
animações de maior qualidade técnica de motion, princípios do design, estética". O estilo atual está aprovado
(argila fosca 3D, selos saturados com ícone branco, verde da marca #50D088, tema escuro do Cato); o pedido é subir o
nível de acabamento, não trocar de identidade. **Tarefa**: versão 2 do kit 3D e do kit 2D + um piloto antes/depois
para o Kaik aprovar. Sem aprovação no meio: termine e relate.

## Ler antes
- `perfis/ecoflix/cenas3d/LEIA.md`, `kit3d.js`, `objetos/` e `vitrine.html`; `perfis/ecoflix/cenas/cenas_ecoflix.html`
  (kit 2D); `docs/09-aula-ilustrada.md` (como a cena é renderizada: `window.setup(dados)` e `window.R(t)`, quadro a
  quadro, determinístico); `perfis/ecoflix/PERFIL.md` (identidade). Cena de referência do piloto:
  `planejamento/ecoflix/T08/cenas3d/cena3d.html` (dupla pesagem) e a 2D correspondente em `T08/cenas/cenas.html`.

## O que refinar (você decide o como; isto é a régua)
- **Motion**: nada linear nem "aparece do nada". Curvas com intenção (entrada com desaceleração longa, saída curta),
  antecipação e acomodação nos objetos pesados (caminhão freia e assenta, carga balança e para, mola amortecida de
  verdade), sobreposição e escalonamento entre elementos (stagger de 60-120 ms), ação secundária discreta (poeira,
  suspensão, ponteiro da balança que passa e volta), arcos em vez de retas, tempo de leitura respeitado (nada some antes
  de ser lido). Câmera como operador humano: dolly e órbita lentos com inércia, enquadramento que guia o olho, sem zoom
  brusco (regra antiga do Kaik), sem cortar o assunto. Rótulos e números entram depois do objeto que nomeiam, com
  contagem animada onde fizer sentido.
- **Estética e design**: hierarquia clara (um foco por momento; o resto recua em contraste/saturação), composição
  (terços, respiro, margens de título seguras), luz com direção e sombra suave de contato, profundidade (névoa/gradiente
  de chão, oclusão sob os objetos), materiais com variação sutil (não plástico chapado), paleta contida com o verde da
  marca como acento, tipografia Montserrat com ritmo e alinhamento consistentes, selos e chips com o mesmo raio, sombra
  e espaçamento em todas as cenas. Transição entre momentos da cena com continuidade (o olho nunca se perde).
- **Técnica**: tudo determinístico em função de `t` (o render é quadro a quadro: nada de `Date.now`, física com passo
  variável nem `requestAnimationFrame`). Custo de render por quadro parecido com o atual (o render roda em CPU, sem GPU:
  nada de pós-processamento caro; se usar algum efeito de tela, meça o tempo por quadro e diga). **Compatível com as 35
  cenas 3D e as 2D que já existem**: a API atual continua valendo, e o que for melhoria geral (curvas padrão, luz,
  sombra, chão, câmera, entrada de rótulo) deve valer para elas sem reescrever cena por cena. O que exigir mudança na
  cena, documente como "passo de migração" curto.

## Entregar
1. Kit v2 em arquivos NOVOS: `perfis/ecoflix/cenas3d/kit3d_v2.js` (e `objetos/` novos se precisar; não edite os que
   existem) e `perfis/ecoflix/cenas/cenas_ecoflix_v2.html`. O v1 fica intacto (as cenas atuais continuam renderizando).
2. Piloto: a cena da dupla pesagem da T08 no kit v2 em `planejamento/ecoflix/T08/cenas3d/cena3d_v2.html` (mesmas âncoras
   de fala, mesmos textos e números da atual) e UMA cena 2D de conceito abstrato à sua escolha (diga qual) no kit 2D v2,
   em arquivo `_v2` ao lado da original.
3. Vídeo antes/depois lado a lado (ou em sequência, com legenda "antes"/"depois") de cada piloto:
   `/home/claude/ecoflix/previa_ilustracoes/motion_v2_3d.mp4` e `motion_v2_2d.mp4` (até 20 MB cada) + uma folha `.jpg` com
   6 quadros de cada. Render: `ferramentas/edit/cenas/render_cenas.cjs` com `--dsf 1.35`, na trava leve
   (`flock /home/claude/ecoflix/.stills.lock nice -n 19`) e `RENDER_PAUSA=0` (a varredura dos robôs está rodando e não é
   sensível a tempo); trechos de até 13 s por chamada, juntados com o concat do ffmpeg. Confira os quadros você mesmo
   (texto cortado, objeto atravessando outro, título coberto, primeiro segundo da cena) antes de entregar.
4. `perfis/ecoflix/cenas3d/MOTION_V2.md`: os princípios aplicados (curto), o que mudou no kit, o tempo de render por
   quadro antes/depois e os passos de migração das cenas existentes.

## Limites
- Escreva só nos arquivos novos acima e em `/home/claude/ecoflix/previa_ilustracoes/`. Não edite kit v1, cenas
  existentes, `ferramentas/`, roteiros nem `PRODUCAO.md`. Temporários em `/dev/shm/motion_v2/` (apague no fim).
- Nada de marca, logo de terceiros ou tela do app nas ilustrações; nenhum número ou rótulo novo. Sem commit. Nada de
  `pkill`/`killall`, `git stash/reset/clean`; `rm` só com caminho absoluto literal.

## Relatório final (até 150 palavras)
O que mudou no motion e na estética, a cena 2D escolhida, tempo de render por quadro antes/depois, o que as cenas
existentes ganham sozinhas e o que precisa de migração.
