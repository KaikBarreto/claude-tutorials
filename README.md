# tutorial-em-video · tutoriais em vídeo de apps web, feitos pelo Claude

> **In English (short):** an agent skill that produces narrated video tutorials of a web app. A robot records the app
> with fictitious data in sync with a synthetic voice-over; an editor adds a branded dark stage, a camera that zooms on
> the element being used, spoken chapter cards, music, SFX and .srt/.vtt captions. Built and tested with Claude Opus
> 5.5 on a 12-minute, 12-chapter lesson. Docs are in Brazilian Portuguese.

Esta skill faz uma aula em vídeo (1080p, de 5 a 20 minutos) de um app web, do roteiro à entrega:

- **Roteiro** Tela × Fala a partir do app real (nada inventado), com fala natural e só com possibilidades.
- **Narração** por voz sintética (padrão: ElevenLabs), conferida palavra a palavra por reconhecimento de fala.
- **Gravação por robô** (Playwright): clica e digita como uma pessoa, com dados fictícios, no ritmo da narração;
  grava a tela em 2560×1600 sem cursor e registra mouse e teclado.
- **Edição**: palco escuro com a marca, cursor desenhado, **câmera que mira o elemento da ação** (com checagem que
  impede zoom fora do alvo), destaques, dicas, ilustrações quando o conceito não aparece na tela.
- **Montagem**: vinheta de abertura com o logo, **vinheta falada antes de cada capítulo**, trilha com ducking, efeitos,
  cortes de pausas, cartela final.
- **Legendas** .srt e .vtt e **conferência** (folha de quadros, volume, todos os zooms) antes de entregar.
- **Aula ilustrada** (boas-vindas, conceitos, combinados): sem tela do app, cada capítulo é uma animação HTML presa às
  palavras da fala, com o mesmo palco, vinhetas, trilha e legendas (`docs/09-aula-ilustrada.md`).

Piloto: Dominex · aula T3 "Clientes, Fornecedores e Equipamentos" (12:13, 12 capítulos), inteira em
[`exemplos/dominex-t3/`](exemplos/dominex-t3/).

---

## Sumário
1. [Requisitos](#1-requisitos)
2. [Instalar a skill](#2-instalar-a-skill)
3. [Como pedir um tutorial](#3-como-pedir-um-tutorial)
4. [Perfis: séries com padrão fechado (Domiflix)](#4-perfis-séries-com-padrão-fechado)
5. [Configurar para o seu app](#5-configurar-para-o-seu-app)
6. [O fluxo completo, passo a passo](#6-o-fluxo-completo-passo-a-passo)
7. [Regras de qualidade](#7-regras-de-qualidade)
8. [Estrutura do repositório](#8-estrutura-do-repositório)
9. [Problemas conhecidos](#9-problemas-conhecidos)
10. [Privacidade, segurança e licenças](#10-privacidade-segurança-e-licenças)

---

## 1. Requisitos

| | |
|---|---|
| **Modelo** | **Claude Opus 5.5 ou superior.** É um trabalho longo (horas), com dezenas de etapas, conferência visual de quadros e decisões de edição; modelos menores perdem o fio. |
| **Onde roda** | Qualquer ambiente com execução de código: Claude Code (terminal, desktop, web), o app Claude com execução de código ligada, ou a sua máquina/servidor Linux ou macOS. |
| **Máquina** | 2 núcleos ou mais, ~4 GB de RAM livres, ~3 GB de disco por aula. Em 2 núcleos, uma aula de 12 min leva ~45 min de render. |
| **Programas** | Python 3.10+, Node 18+, Playwright com Chromium, ffmpeg. O `instalar.sh` instala o que falta (pip, npm). |
| **Rede** | github.com e raw.githubusercontent.com (modelos de fala), pypi.org, registry.npmjs.org; o seu app (modo URL). |
| **Voz** | Uma conta de TTS. Padrão: ElevenLabs (conector do Claude ou exportação manual). Qualquer TTS que gere um arquivo por capítulo serve. |
| **App** | Uma URL do app com **conta de demonstração e dados fictícios** (servidor local ou staging), ou o código do app com backend falso (Supabase). |

## 2. Instalar a skill

O nome da skill é **`tutorial-em-video`** (o campo `name` do `SKILL.md`).

**Claude Code** (pessoal, todos os projetos):
```bash
git clone https://github.com/KaikBarreto/claude-tutorials ~/.claude/skills/tutorial-em-video
```
Ou só num projeto: clone em `.claude/skills/tutorial-em-video/` dentro do repositório. Também funciona com um link
simbólico para outro lugar do disco.

**App Claude** (claude.ai, desktop): a execução de código precisa estar ligada. Gere o zip e envie em
**Customize > Skills**:
```bash
bash empacotar.sh        # -> dist/tutorial-em-video.zip (a pasta da skill na raiz do zip)
```

**Numa sessão sem a skill instalada**: dá para clonar o repositório e pedir "siga o SKILL.md de
claude-tutorials".

Depois, a área de trabalho de cada tutorial é criada pelo próprio Claude com o `instalar.sh` (seção 6).

## 3. Como pedir um tutorial

Exemplos de pedido:
- "Faz um tutorial em vídeo do meu app (https://staging.meuapp.com) mostrando como cadastrar um pedido e emitir a nota.
  A conta de demonstração está nas variáveis TUT_USER e TUT_SENHA."
- "Próximo tutorial da Domiflix: T4, Tipos de Serviço, Tipos de Tarefa e Checklists." (usa o perfil Domiflix)

O Claude pergunta só o que faltar (assunto, app, marca, voz) e trabalha em duas paradas com você:
1. **Roteiro** para aprovar antes de gerar a voz.
2. **Um capítulo de prévia** pronto para aprovar o visual antes de produzir o resto.
No fim entrega o vídeo completo + legendas.

## 4. Perfis: séries com padrão fechado

Um perfil (`perfis/<serie>/`) congela o padrão de uma série para que todas as aulas saiam iguais: marca, voz,
pronúncias, mundo fictício, montagem, nomes de arquivo e entrega. Com perfil, **nada é adaptado**: só o conteúdo muda.

| Perfil | Série | O que fixa |
|---|---|---|
| [`domiflix`](perfis/domiflix/PERFIL.md) | Trilha Domiflix do Dominex (20 tutoriais) | Padrão do T3: vinheta do capacete Dominex, verde #00C597 + Montserrat, voz Fernanda (ElevenLabs eleven_v4), pronúncias (QR Code, Hi-Wall, BTUs...), Glacial Cold Brasil no Supabase falso, câmera v2, vinhetas faladas, trilha `music_seed` 3, `Domiflix T<n> - <Título>.mp4` |

```bash
TUT_HOME=~/domiflix TUTORIAL=t4 PERFIL=domiflix bash instalar.sh
```
**Garantia de que nada muda**: `bash testes/identidade_domiflix.sh` renderiza com as ferramentas do repositório e
compara com os arquivos reais do T3 (palco, cartão de capítulo, vinheta de abertura, cartela e o som da vinheta).
Tem de dar "IDÊNTICO ao T3" antes de publicar qualquer mudança (use `MODELOS=<pasta models>` para não baixar o
SoundFont).

Para criar o perfil de uma série nova, copie a estrutura de `perfis/domiflix/` (marca, `voz.json`,
`narracao/config_narracao.json`, `aula.json`, `PERFIL.md`).

## 5. Configurar para o seu app

### 5.1 Marca — `marca/marca.json`
Cores, fonte, logo, nome da série e estilo da vinheta. Modelo comentado em [`modelos/MARCA.md`](modelos/MARCA.md)
e [`modelos/marca.json`](modelos/marca.json); exemplo completo em [`perfis/domiflix/marca/`](perfis/domiflix/marca/).
Sem logo vetorial, um PNG com fundo transparente em boa resolução serve. Se a pessoa não informar, o Claude extrai as
cores e a fonte do próprio app (tema/CSS) e confirma.

### 5.2 Voz — narração
Um arquivo por capítulo + um com os títulos dos capítulos. Configure idioma, pronúncias e números em
`narracao/config_narracao.json` ([guia](docs/03-narracao.md)). O reconhecimento de fala (Parakeet v3) cobre 25
idiomas europeus, entre eles português, inglês e espanhol.

### 5.3 App — modo de gravação
- **Modo URL** (o app de qualquer pessoa): `APP_URL=<url>`, `REC_MODE=url`, login nos passos de `setup` com
  `"$TUT_USER"`/`"$TUT_SENHA"` lidos do ambiente. A rede não é isolada; o estado de partida de cada capítulo é
  preparado na conta de demonstração.
- **Modo fakebase** (apps com Supabase, controle total dos dados): um Supabase falso local com sementes e o app
  rodando a partir de uma cópia do código. É o modo do exemplo Dominex.
Detalhes e exemplo de roteiro do robô: [`docs/04-gravacao.md`](docs/04-gravacao.md) e
[`ferramentas/rec/README.md`](ferramentas/rec/README.md).

## 6. O fluxo completo, passo a passo

| # | Etapa | Ferramenta | Saída | Guia |
|---|---|---|---|---|
| 1 | Área de trabalho | `instalar.sh` | `$TUT_HOME/{kit,audio,web,rec,marca,models}`, `$TUT_HOME/<id>/{edit,narracao}` | este README |
| 2 | Inventário do app | leitura do código / app rodando | `inventario.md`, handoff de correções | [02](docs/02-roteiro.md) |
| 3 | Roteiro Tela × Fala | `modelos/roteiro.md` | roteiro aprovado | [02](docs/02-roteiro.md) |
| 4 | Narração | TTS + `narracao/proc.py` | `narracao/capNN.json` (palavras com tempo) | [03](docs/03-narracao.md) |
| 5 | Gravação | `rec/record.mjs` | `rec/<id>/<id>-capNN.{mp4,actions.json,telemetry.json}` | [04](docs/04-gravacao.md) |
| 6 | Edição por capítulo | `edit/montar_cap.py`, `auditar_camera.py`, `render_chapter.py` | `edit/out/capNN/capNN.mp4` | [05](docs/05-edicao.md) |
| 7 | Títulos falados | `narracao/titulos.py` | `narracao/titulos/` | [03](docs/03-narracao.md) |
| 8 | Montagem | `edit/finish.py` | `edit/out/<AULA>/aula_final.mp4` | [05](docs/05-edicao.md) |
| 9 | Legendas | `narracao/legendas_aula.py` | `.srt` + `.vtt` | [06](docs/06-legendas.md) |
| 10 | Conferência e entrega | `folha_zooms.py`, `lacunas.py`, `confere_render.py`, `entregar.py`, `folhas3s.sh` (folha de 3 s do vídeo inteiro) | vídeo completo + legendas com o mesmo nome | [07](docs/07-conferencia.md) |

Comandos de cada etapa estão nos guias. Toda tarefa pesada (gravar, renderizar, montar) roda sozinha, sob
`flock $TUT_HOME/.heavy.lock`.

## 7. Regras de qualidade
O padrão completo está em [`docs/01-padrao.md`](docs/01-padrao.md). Em resumo:
- Nada inventado: telas, resultados e funções saem do app real. Dados sempre fictícios.
- Fala natural, de colega mostrando o sistema; **só possibilidades**; rótulos exatos; sem travessão.
- Vinheta falada em cada capítulo; **sem contador de etapas**.
- Câmera sempre no alvo da ação: `auditar_camera.py` com 0 problema e folha de zooms conferida.
- Palco e desenhos próprios; só o logo da marca; nada de terceiros.
- Legendas em arquivo; entrega do vídeo completo.

## 8. Estrutura do repositório
```
SKILL.md                 instruções da skill (o Claude lê primeiro)
README.md                este documento
instalar.sh              cria a área de trabalho de um tutorial (TUT_HOME, TUTORIAL, PERFIL, MARCA)
empacotar.sh             zip para enviar no app Claude
docs/                    guias: 01 padrão · 02 roteiro · 03 narração · 04 gravação · 05 edição · 06 legendas ·
                         07 conferência · 08 lições do piloto
modelos/                 pontos de partida neutros: marca, roteiro, textos do TTS, config da narração, specs, aula
perfis/domiflix/         padrão fechado da trilha Domiflix (Dominex): marca, voz, pronúncias, montagem, PERFIL.md
testes/                  identidade_domiflix.sh + referências tiradas do T3 real (quadros e hash do áudio)
ferramentas/
  rec/                   robô gravador (Playwright) + Supabase falso opcional
  narracao/              conferência e alinhamento da voz, emendas, títulos, legendas
  edit/                  editor: câmera, cursor, palco, camadas, vinhetas de capítulo, montagem, auditoria, entrega
  edit/cenas/            capítulos ilustrados: modelo de cenas HTML, renderizador quadro a quadro, gerador de capítulos
  kit/ audio/ web/       vinheta e cartela, trilha e SFX, ASR, fontes
exemplos/dominex-t3/     a aula piloto inteira: inventário, roteiro, textos do TTS, roteiros do robô, specs, ilustração
exemplos/dominex-t0/     aula ilustrada (boas-vindas): cenas HTML, textos do TTS, montagem encadeada
```

## 9. Problemas conhecidos
Ver [`docs/08-licoes.md`](docs/08-licoes.md) (tudo que custou tempo no piloto e como evitar). Os principais:
- **Processo morto por memória** numa aula longa: as ferramentas já trabalham em blocos; não rode duas etapas
  pesadas juntas.
- **Gravação atrasada** (`lateBy` alto): havia render rodando junto. Use sempre a trava.
- **Zoom no canto ou campo cortado na borda**: a câmera v2 resolve e `render_chapter.py` recusa o capítulo se
  acontecer; rode `auditar_camera.py`.
- **Download da voz bloqueado** no ambiente: peça o zip exportado do fluxo.
- **Palavra "sumida" na conferência da voz**: quase sempre é o reconhecimento colando duas palavras; ouça o trecho
  antes de pedir regravação.

## 10. Privacidade, segurança e licenças
- Grave **somente** com conta de demonstração e dados fictícios. Credenciais só por variável de ambiente; teclas em
  campo de senha saem mascaradas na telemetria e nada antes do 1º quadro é guardado.
- Não grave dados reais de clientes, tokens ou documentos sensíveis; confira a folha de contato de cada gravação.
- O repositório do app é lido, nunca alterado. Nada é publicado sem ok explícito.
- Componentes de terceiros baixados na instalação: Parakeet TDT 0.6B v3 (NVIDIA, CC-BY-4.0) via sherpa-onnx (Apache-2.0),
  Silero VAD (MIT), GeneralUser GS SoundFont (licença própria, uso livre), Playwright (Apache-2.0), fonte Montserrat
  (SIL OFL 1.1). As marcas e logos do exemplo Dominex pertencem aos seus donos.
