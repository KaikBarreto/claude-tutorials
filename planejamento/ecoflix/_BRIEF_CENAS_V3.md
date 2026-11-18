# Briefing das cenas no kit v3 · trilha EcoFlix (uma aula por agente)

O Kaik aprovou o estilo v3 (18/11: "Ficou ótimo a prévia da animação"): um mundo só com dois climas (claro com
gradientes = mundo físico; escuro de vidro = mundo dos dados), câmera contínua entre estações, 3D quando ajuda.
**Tarefa**: as ilustrações da sua aula no kit v3, poucas e boas. Sem aprovação no meio: termine e relate.

## Ler (só isto)
- `perfis/ecoflix/cenas_v3/LEIA.md` (API, objetos, componentes de dados, regra dos climas, exemplo) e a cena aprovada
  `planejamento/ecoflix/T08/cenas_v3/cena.html` (o padrão de qualidade e de câmera).
- Da aula: `Tnn/cenas/ilustracoes.json` (as entradas com `"v3": "pendente"` e as antigas), `narracao/tts_textos.py`, os
  tempos `cenas/tempos/capNN.json` (regerados por `preparar_aula.sh`) e, para números e nomes, `JUNCAO_160.md` (seção da
  aula) e `MUNDO_FICTICIO.md`.

## Regras
- **Enxugar**: ilustração só onde o conceito não se entende pela tela do app. Meta de até ~4 cenas por aula (aula
  grande, até 6); o resto das entradas antigas sai do `ilustracoes.json` (liste no relatório o que saiu e por quê).
  Conceitos vizinhos viram UMA cena com estações e câmera contínua, em vez de várias cenas soltas.
- Mesmos textos e números da fala e da tela (nada novo, nada de marca de terceiros, nada de tela do app). Tara: no
  Ticket e na compra é a embalagem; o caminhão vazio da dupla pesagem não é tara; no cadastro de veículo das Coletas o
  app chama o veículo vazio de "Tara (kg)".
- Clima pela regra do kit; troca de clima só na passagem de conceito e motivada pela câmera. Título desde o primeiro
  quadro, cada elemento entra na palavra que o nomeia (âncoras `W(linha, 'palavra')`), nada some antes de ser lido,
  sem zoom brusco, nada cortado na borda (margem ≥ 40 px em 1280x800), nada sobre o título.
- Objeto que faltar: arquivo novo em `perfis/ecoflix/cenas_v3/objetos/` (veja antes se outro agente já fez). Não edite
  `motor.js` nem objeto existente (peça no relatório).

## Entregar
- `planejamento/ecoflix/Tnn/cenas_v3/cena.html` (um `CAPS` por capítulo ilustrado) e o `ilustracoes.json` atualizado
  (`"v3": "cenas_v3/cena.html"` nas cenas feitas).
- Conferência em quadros (primeiro segundo, meio de cada transição de câmera, fim) e prévia da aula em
  `/home/claude/ecoflix/previa_ilustracoes/Tnn_v3.mp4` (`--dsf 1.35`, até 25 MB) + `Tnn_v3.jpg` (12 quadros). Render
  com `ferramentas/edit/cenas/render_cenas.cjs` na trava leve (`flock /home/claude/ecoflix/.stills.lock nice -n 19`), em
  trechos de até 13 s por chamada juntados com o concat do ffmpeg. **Um lote de render por vez em segundo plano; olhe
  tudo junto quando terminar** (cada acordada relê o seu contexto: acorde pouco).

## Limites
Escreva só em `Tnn/cenas_v3/`, no `ilustracoes.json` da aula, em `cenas_v3/objetos/` (arquivos novos) e na pasta de
prévias; temporários em `/dev/shm/v3_tNN/` (apague no fim). Não mexa em roteiro, fala, robô, `ferramentas/`, outras
aulas nem `PRODUCAO.md`. Sem commit. Nada de `pkill`/`killall`, `git stash/reset/clean`; `rm` só com caminho absoluto.

## Relatório final (até 120 palavras)
Cenas feitas (capítulo, id, clima), as que saíram, objetos novos, tempo de render e o caminho da prévia.
