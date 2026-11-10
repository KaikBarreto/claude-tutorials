---
name: tutorial-em-video
description: Produz tutoriais em vídeo de um app web com roteiro, narração por voz sintética, gravação automática com dados fictícios, câmera que segue a ação, vinhetas e legendas.
compatibility: Claude Opus 5.5 ou superior. Execução de código com Python 3.10+, Node 18+, Playwright/Chromium e ffmpeg; ~4 GB de RAM.
---

# Tutorial em vídeo de um app web

Produz uma aula em vídeo (1080p, ~5 a 20 min) de um app web: o app é gravado por um robô que clica e digita como uma
pessoa, com dados fictícios, no ritmo de uma narração gerada por TTS; a edição põe o app num palco escuro com a marca,
faz zoom no que está sendo feito, abre cada capítulo com uma vinheta falada, soma trilha e efeitos e gera legendas
.srt/.vtt. Referência completa: `README.md` e `docs/` nesta pasta. Exemplo inteiro: `exemplos/dominex-t3/`.

## Perfis (séries com padrão fechado)
Se o tutorial é de uma série que já tem perfil em `perfis/`, **o perfil vale inteiro e não se adapta nada**:
- **Domiflix (Dominex)** → `PERFIL=domiflix` e siga `perfis/domiflix/PERFIL.md` à risca. É o padrão do T3
  (`exemplos/dominex-t3/`) congelado: marca e vinheta do capacete, voz Fernanda, pronúncias, mundo fictício Glacial
  Cold Brasil no Supabase falso, câmera, vinhetas faladas, trilha (seed 3), nomes de arquivo e entrega. Só o conteúdo
  muda de uma aula para outra.
- **EcoFlix (EcoSistema)** → `PERFIL=ecoflix` e `perfis/ecoflix/PERFIL.md`: o padrão da Domiflix com a marca da
  EcoSistema, voz masculina e o mundo da Recicla Vale Metais. Em montagem desde 08/11/2026: o que o perfil ainda não
  fixou segue a Domiflix.
Sem perfil (o app de outra pessoa): use os modelos neutros e configure marca, voz e app (abaixo). Para uma série nova
que vai ter várias aulas, crie `perfis/<serie>/` copiando a estrutura do perfil Domiflix.

Responda na língua da pessoa, curto. Mostre resultado cedo (o roteiro, depois um capítulo pronto) e peça retorno
antes de produzir tudo. Trabalho longo: mantenha uma lista de tarefas e um registro de pedidos e decisões em disco
(sobrevive a reinício).

## 0. O que pedir (só o que faltar)
- **Assunto** da aula (telas e fluxos) e público.
- **App**: URL de demonstração (servidor local ou staging) e uma **conta de demonstração** com dados fictícios,
  passada por variável de ambiente (`TUT_USER`, `TUT_SENHA`), nunca escrita em arquivo. Alternativa: o código do app
  com backend falso (modo fakebase, ver `docs/04-gravacao.md`).
- **Marca**: nome da série, logo (PNG/SVG com fundo transparente), cores (acento, escuro, claro) e fonte. Sem isso,
  extraia do app (CSS/tema) e confirme. Vira `marca/marca.json` (modelo em `modelos/marca.json`, guia em
  `modelos/MARCA.md`).
- **Voz**: TTS e voz (padrão: conector ElevenLabs, uma voz natural de conversa) e idioma.

## 1. Preparar a área de trabalho
```bash
TUT_HOME=~/tutoriais TUTORIAL=t1 MARCA=/caminho/da/marca bash <pasta-da-skill>/instalar.sh    # app de outra pessoa
TUT_HOME=~/domiflix  TUTORIAL=t4 PERFIL=domiflix bash <pasta-da-skill>/instalar.sh            # série Domiflix
```
Cria `$TUT_HOME/{kit,audio,web,rec,marca,models}` e `$TUT_HOME/t1/{edit,narracao}`, instala as dependências e baixa
os modelos (ASR Parakeet v3, VAD Silero, SoundFont). Rede: github.com, raw.githubusercontent.com, pypi, npm. Se algo
for bloqueado, diga qual domínio liberar.

## 2. Inventário e roteiro (`docs/02-roteiro.md`)
1. Inventário lendo o código e/ou percorrendo o app: rótulos exatos, regras, avisos, pegadinhas. Pegadinha vira
   lista de correções para o time do app; o roteiro nunca depende de bug.
2. Roteiro Tela × Fala por capítulo (`modelos/roteiro.md`): abertura, capítulos, recapitulação + próximo. Fala
   natural, **só possibilidades**, rótulos como na tela, trocas de pronúncia anotadas. **Aprovação antes da voz.**

## 3. Narração (`docs/03-narracao.md`)
Um arquivo por capítulo + um com os títulos dos capítulos (para as vinhetas). Texto exato em
`narracao/tts_textos.py`; idioma, trocas de pronúncia e números em `narracao/config_narracao.json`.
`python3 -I proc.py recebido/*.mp3` identifica cada capítulo, alinha palavra a palavra e grava `capNN.json`.
Nunca repita uma geração paga para "tentar de novo".

## 4. Mundo fictício e gravação (`docs/04-gravacao.md`)
Dados de exemplo plausíveis (empresa, pessoas, documentos válidos, e-mails `.example`). Um roteiro de robô por capítulo
(`rec/<tutorial>/capNN.json`): `mark` em cada linha da narração, `at` com os tempos do `capNN.json`, `label` em todo
passo que a edição vai usar, login no `setup` (não filmado) com `"$TUT_USER"`/`"$TUT_SENHA"`. Grave um capítulo por
vez, sob a trava `.heavy.lock`, nunca junto com render. Aceite: 0 passo falho, `lateBy` < 0,8 s, folha de contato
sem dado real.

## 5. Edição por capítulo (`docs/05-edicao.md`)
`edit/caps/specs.json` (título e área da vinheta, zooms e destaques por `label`, avisos por palavra, ilustração,
cortes) → `python3 -I montar_cap.py NN` → **`python3 -I auditar_camera.py` com 0 problema** → `render_chapter.py`
(fila: `out/fila.sh`). A câmera mira o alvo da ação e o render recusa capítulo com alvo fora do quadro.
Confira `python3 -I folha_zooms.py out/folhas_zoom` e mande **um capítulo de prévia** antes de seguir.
Ilustração (fundo branco com desenho por cima, depois volta ao app) só para conceito que a tela não mostra; texto
medido antes de desenhar; exemplo em `exemplos/dominex-t3/ilustracoes/`.
**Aula ilustrada inteira** (boas-vindas, conceitos, combinados; sem tela do app): cada capítulo é uma animação HTML
presa às palavras da fala (`edit/cenas/`), conferida em quadros antes do render; ver `docs/09-aula-ilustrada.md` e
`exemplos/dominex-t0/`.

## 6. Montagem, legendas, conferência e entrega (`docs/05`, `06`, `07`)
`python3 -I titulos.py` (títulos falados) → `python3 -I finish.py caps/<AULA>.aula.json` (vinheta da aula, vinhetas
de capítulo com voz e SFX, cortes, trilha com ducking, cartela) → `python3 -I legendas_aula.py ...` →
`python3 -I entregar.py out/<AULA> "<Série> - <Título>"` (specs, volume, folha de quadros) → **folha de 3 s do vídeo
inteiro** (`bash folhas3s.sh out/<AULA>/aula_final.mp4 out/<AULA>/folhas3s`), olhada do começo ao fim. Entregue **o vídeo
completo** 1080p + `.srt` + `.vtt` com o mesmo nome.

## Sempre
- Tudo que aparece sai do app real: nada de tela, resultado ou função inventada.
- Dados fictícios; nenhuma credencial, token ou dado pessoal na tela, em log ou em arquivo do repositório.
- Uma vinheta falada por capítulo, sem contador de etapas ("Passo 1/5").
- Palco escuro próprio; só o logo da marca; nenhum logo ou papel de parede de terceiros.
- Fala só com possibilidades; sem travessão na copy; rótulos exatos.
- Uma tarefa pesada por vez (gravar, renderizar, montar) sob `flock $TUT_HOME/.heavy.lock`.
- Não mexer no repositório do app (somente leitura). Não publicar nada sem ok explícito.

## Problemas conhecidos (detalhes em `docs/08-licoes.md`)
Processo morto por memória numa aula longa → as ferramentas já trabalham em blocos; não junte etapas pesadas.
Zoom no canto ou alvo cortado → `auditar_camera.py`. Legenda adiantada 1 s → `ts()` corrigido. `pgrep -f` dentro de
laço acha o próprio laço → use `"[r]ender_chapter.py"`. Download do TTS bloqueado → peça o zip exportado.
