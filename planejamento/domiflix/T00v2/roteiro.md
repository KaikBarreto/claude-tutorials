# T0 v2 · Boas-vindas à Dominex (onboarding novo)

**Roteiro revisado para aprovação.** Pedido do Kaik de 31/10 17:13 (`pedido_kaik_31-10.txt`): o vídeo vira o 1º passo
obrigatório do onboarding e mostra a DomiFlix nova. Nesta etapa só roteiro, storyboard e lista de telas: **nada de voz
nem vídeo antes do ok**. Base: o T0 atual (3:25, aprovado em 30/10; `../T00/plano.md` e a área `$TUT_HOME/t0`).

**Conferido na DomiFlix publicada (1.38.11 + `487a0ca3`, 31/10 19:29).** O que o código novo mudou neste roteiro: a frase do
botão do suporte (cena 22: ele abre o WhatsApp com a mensagem pronta, não envia sozinho); os rótulos reais nas telas
(cenas 07 a 12, 15, 17, 21, 22 e 38: "Aprenda a usar a Dominex", "Trilha do seu plano", "Formação básica", "Materiais e
extras", "Adicionar ao meu plano", "Confirmar e começar a primeira aula"); no celular, os selos vêm da gaveta "Ver trilha";
e a faixa onde o player desenha a legenda (ver "Composição"). As frases do Kaik ficaram letra por letra; onde a tela usa
outro rótulo, está marcado (decisão D8 em `sinalizacoes.md`).

Nesta pasta:
- `roteiro.md` (este): cenas numeradas com tempo, fala (texto final da legenda) e composição 16:9 e 9:16.
- `storyboard_16x9.png` e `storyboard_9x16.png`: um quadro por cena. Fonte em `storyboard/` (`cenas.py` calcula os tempos e
  escreve as tabelas de duração e de cenas deste roteiro; `render.cjs` desenha as folhas).
- `narracao/tts_textos.py` e `narracao/config_narracao.json`: o texto da voz (grafia de pronúncia) e as trocas da legenda.
- `telas_necessarias.md`: as telas reais (R01 a R18), com estado, dados fictícios e cena.
- `sinalizacoes.md`: o que mudou de plano, cobrança e funcionamento, o que o código confirmou e o que segue aberto (C1 a C16)
  e as decisões (D1 a D8).

## Ficha
- **Título:** Boas-vindas à Dominex (o mesmo). **Vinhetas:** COMEÇANDO (2) · AJUDA · ASSINATURA (2) · RECAPITULANDO.
- **Formatos:** 16:9 1920×1080 no estilo atual (palco escuro, painel claro) e 9:16 1080×1920 nativo, recomposto cena a
  cena. Mesma fala, trilha e duração nos dois; só a imagem muda. H.264 + AAC; SRT e VTT de cada versão.
- **Voz:** Fernanda (eleven_v4), como no T0. `voz: nova` = gerar; `voz: T0` = áudio do T0 atual reaproveitado (texto
  idêntico letra por letra; `python3 narracao/tts_textos.py diff` confere).
- **Caracteres:** roteiro inteiro **3.575** (3.452 de fala + 123 dos títulos). A gerar: **2.433** (capítulos 0, 1, 2, 3
  e 6 + os títulos 2 e 6), reaproveitando os capítulos 4 e 5 e quatro títulos do T0 atual (decisão D5).
- **Duração estimada: 4:27** (fala nova a 2,6 palavras/s); no ritmo que a Fernanda teve no T0 atual, ~4:11. Conta abaixo.
- **Marcas:** `[confirmar Cn]` = ponto que o código publicado (1.38.11) não fecha sozinho: catálogo, comercial ou frase
  ajustada que o Kaik precisa ver (`sinalizacoes.md`);
  `TELA REAL Rnn` = tela real a capturar (`telas_necessarias.md`). Nenhuma interface desenhada: onde vai tela real, o
  storyboard tem um retângulo "TELA REAL" com o que precisa aparecer. Ilustração só para conceito.
- **Fala:** as frases que o Kaik deu entre aspas (itens 1, 3 e 7) estão letra por letra. O resto segue o perfil: fala
  natural, só possibilidades, rótulos exatos, sem preço de plano, nenhum travessão.

## O pedido, item por item
| Pedido do Kaik | Onde | Como |
|---|---|---|
| 1. Primeiro passo obrigatório, "assista até o final e confirme..." | Cena 03 | Frase do Kaik, letra por letra |
| 2. Começou no teste e contratou: a confirmação vale, o vídeo não volta | Cena 04 | Frase nova |
| 3. Explicação nova da DomiFlix (trilha, Formação Básica, módulos, "Não tem no seu plano", aula de um tema, progresso, próxima aula) | Cenas 06 a 12 | Texto do Kaik, letra por letra (só "DomiFlix" na grafia da voz) |
| 4. Três grupos com os selos e o CTA | Cena 06 (mapa da trilha), 07 a 10 (telas reais), 16 | Formação Básica → módulos do plano → outros módulos |
| 5. Só Formação Básica e módulos contratados no percentual | Cenas 15 e 16 | Frases novas |
| 6. Lembretes nos primeiros 30 dias | Cena 17 | Frase nova |
| 7. "Você não precisa esperar uma reunião..." | Cena 20 (e o combinado da cena 36) | Frase do Kaik, letra por letra |
| 8. "Tirar dúvidas com o suporte" envia empresa, usuário, módulo e aula | Cenas 21 e 22 | Tela real; a fala segue o código: o WhatsApp abre com a mensagem pronta |
| 9. Outras trilhas no futuro (gestão, contabilidade), foco na Tutoriais do sistema | Cena 18 | Frase nova |
| Manter suporte, assinatura e crescimento | cap03, cap04, cap05 | cap04 e cap05 sem mudar uma palavra; cap03 só no necessário |
| Telas reais, selos saturados, sem temporadas, ordem dos grupos | todas as cenas de tela | R01 a R18 |
| 9:16 nativo com as regras de composição | coluna 9:16 de cada cena | ver "Composição" |
| Logo DomiFlix todo branco no escuro | vinheta e cartela | decisão D1 |
| 4:00 a 4:30 | | 4:27 estimado (4:11 no ritmo real) |

## Mapa dos capítulos (v2 ← T0 atual)
| v2 | Vinheta (título) | Área | T0 atual | Fala | Título falado |
|---|---|---|---|---|---|
| cap00 | sem vinheta (Boas-vindas) | | cap00 | nova (a 1ª linha é a do T0) | |
| cap01 | Como funcionam os tutoriais | COMEÇANDO | cap01 | nova | T0 |
| cap02 | O seu progresso | COMEÇANDO | novo | nova | novo |
| cap03 | Quando bater uma dúvida | AJUDA | cap02 | nova | T0 |
| cap04 | A sua assinatura | ASSINATURA | cap03 | **T0, idêntica** | T0 |
| cap05 | Quando a empresa cresce | ASSINATURA | cap04 | **T0, idêntica** | T0 |
| cap06 | Os combinados | RECAPITULANDO | cap05 (fecho), trocado | nova | novo |

## Duração
Vinheta da aula, vinhetas de capítulo, cauda de 1,2 s por capítulo e cartela com as durações do T0 atual
(`out/T0/capitulos.json`); títulos novos curtos ficam no mínimo de 3,2 s.

<!-- DURACAO -->
| Bloco | Palavras | Fala | Vinheta + cauda | Total | Começa em | Voz |
|---|---|---|---|---|---|---|
| Vinheta da aula | | | 4,4 s | 4,4 s | 0:00,0 | identidade |
| cap00 · Boas-vindas | 72 | 27,7 s | 1,2 s | 28,9 s | 0:04,4 | nova (2,6 palavras/s) |
| cap01 · Como funcionam os tutoriais | 121 | 46,5 s | 4,9 s | 51,5 s | 0:33,3 | nova (2,6 palavras/s) |
| cap02 · O seu progresso | 79 | 30,4 s | 4,4 s | 34,8 s | 1:24,8 | nova (2,6 palavras/s) |
| cap03 · Quando bater uma dúvida | 98 | 37,7 s | 4,5 s | 42,2 s | 1:59,5 | nova (2,6 palavras/s) |
| cap04 · A sua assinatura | 75 | 25,6 s | 4,4 s | 30,0 s | 2:41,7 | áudio do T0 atual (tempo real) |
| cap05 · Quando a empresa cresce | 122 | 42,9 s | 4,4 s | 47,3 s | 3:11,7 | áudio do T0 atual (tempo real) |
| cap06 · Os combinados | 53 | 20,4 s | 4,4 s | 24,8 s | 3:59,0 | nova (2,6 palavras/s) |
| Cartela | | | 3,4 s | 3,4 s | 4:23,8 | identidade |
| **Total** | **620** | | | **4:27,2** | | |

Estimativa principal **4:27,2** (fala nova a 2,6 palavras/s + áudio real dos capítulos 4 e 5). Na velocidade que a Fernanda teve no T0 atual (2,89 palavras/s, pausas incluídas): **4:10,9**. Se tudo fosse lido a 2,6: 4:34,5. Faixa pedida: 4:00 a 4:30.
<!-- /DURACAO -->

Para caber folga (por exemplo, a frase opcional do treinamento ao vivo, D4, ~5 s), o candidato a sair é a frase do menu
da conta (cena 13, ~6 s): a DomiFlix nova já indica a próxima aula e o menu aparece de novo na cena 24.

## Composição
### 16:9 (estilo atual)
- Palco escuro e painel claro de 1587×992 com cantos de 16 px, como o T0 atual; vinhetas, cartela, trilha (seed 3), SFX e
  legendas do perfil.
- **Tela real:** a gravação ocupa o painel inteiro, como nas aulas com tela, com a câmera v2 (zoom no que a fala cita) e
  destaques com o rótulo exato. Dados do mundo fictício (Glacial Cold Brasil, Camila Duarte); valores em R$ cobertos.
- **Faixa da legenda:** o player da DomiFlix desenha a legenda dentro do vídeo, a 15% do pé no computador
  (`src/pages/DomiflixWatch.tsx:1446-1452`), e a primeira legenda enviada já vem ligada. No quadro 1920×1080, a faixa vai de
  **y 800 a 930**: nada essencial ali (marcada em laranja nas folhas).
- **Ilustração**, só para conceito, com o ajuste de estilo pedido: menos cartões e cantos arredondados, nada de fundo
  acinzentado nem barras-fantasma; texto grande, ícone, linha e cor saturada. Selos sempre saturados, ícone e texto brancos.

### 9:16 (nativo, recomposto cena a cena)
- Palco escuro e painel claro de 1008×1700 (x 36, y 110). Conteúdo só na área segura: **x 72 a 1008 e y 180 a 1740** (guias
  magenta nas folhas).
- **Faixa da legenda:** no celular o player desenha a legenda a 18% do pé do vídeo vertical: **y 1420 a 1600** do quadro.
  Nada essencial ali (marcada em laranja). Na prática, o conteúdo vai de y 180 a ~1400.
- **É a "Versão para celular" da aula:** em tela menor que 1024 px a DomiFlix troca sozinha o vídeo horizontal pelo
  vertical, inclusive na introdução obrigatória (`DomiflixWatch.tsx:480`; `DomiflixIntroGate.tsx:42`).
- **Um assunto por vez:** o que no 16:9 aparece junto entra em sequência, preso à palavra da fala.
- Texto mínimo **44 px** (≈ 16 px num celular de 390 px de largura); títulos de 88 a 112 px; **no máximo 2 linhas** por bloco.
- **Tela real = captura do celular** (viewport 390×844), recortada na área que a fala cita e ampliada 2,4× (390 → 936 px).
  Nunca o print do computador reduzido. A lista de aulas é a da interface mobile real da DomiFlix: na página inicial do
  celular não há selos; os selos e a trilha com as aulas vêm da gaveta "Ver trilha", dentro da aula.
- Grupos e comparações sempre na vertical: Formação Básica em cima, módulos do plano no meio, outros módulos embaixo.

## Cenas
Cada quadro do storyboard mostra o fim da cena. Tempo = estimativa (ver "Duração"); depois da voz, as cenas se prendem às
palavras do `capNN.json`, como no T0 atual.

<!-- CENAS -->
### Abertura

**Cena 01 · 0:00,0 a 0:04,4** · Vinheta da aula · VINHETA
> (sem fala) Boas-vindas à Dominex

- **16:9:** Vinheta do perfil: o capacete se monta, DOMINEX e o título "Boas-vindas à Dominex". Proposta: o "▶ DOMIFLIX" verde vira o logo DomiFlix todo branco, capacete e texto (D1), o mesmo que a DomiFlix nova passou a usar.
- **9:16:** Vinheta nativa na vertical: capacete (y 520 a 830), DOMINEX (y 880), logo DomiFlix branco (420 px, y 1060) e o título em 2 linhas de 88 px (y 1210 a 1400); tudo entre y 180 e 1740.

### cap00 · Boas-vindas (sem vinheta; voz nova)

**Mudança em relação ao T0 atual:** Ficam as duas primeiras frases (boas-vindas e o ciclo do trabalho). Sai "Neste vídeo rápido, eu te mostro como a gente vai caminhar junto." Entram o 1º passo obrigatório do onboarding (texto do Kaik, item 1) e a confirmação que vale do teste para a assinatura (item 2). Visual: o ciclo do trabalho reestilizado (sem cartões) e duas ilustrações novas.

**Cena 02 · 0:04,4 a 0:15,2** · O ciclo do trabalho · ILUSTRAÇÃO · voz: nova
> Oi! Boas-vindas à Dominex. A partir de agora, a sua empresa tem um lugar só pra organizar o trabalho, do chamado do cliente até o dinheiro na conta.

- **16:9:** Painel claro. "Boas-vindas à Dominex" no alto (Dominex em verde). Embaixo, o arco verde se fecha em volta do capacete e as 4 estações entram entre "chamado" e "dinheiro": Chamado do cliente, Ordem de serviço, Técnico em campo, Dinheiro na conta. Só ícone e texto, sem cartão.
- **9:16:** Título em 2 linhas no topo (96 px). As 4 estações numa coluna (círculo de 140 px com o ícone, texto 58 px em até 2 linhas), ligadas pela linha verde que desce, volta pela direita e entra de novo no topo (o ciclo); acendem uma por vez. O capacete embaixo.

**Cena 03 · 0:15,2 a 0:24,4** · O primeiro passo · ILUSTRAÇÃO · voz: nova
> Este vídeo é o primeiro passo para começar a usar a Dominex. Assista até o final e confirme que entendeu os combinados para continuar.

- **16:9:** Selo "Primeiro passo" (o mesmo rótulo da tela do app). Três passos numa linha, número grande e texto, sem cartões: 1 Assistir até o final (a barrinha do vídeo enche em "final"), 2 Confirmar os combinados (acende em "confirme"), 3 Começar a primeira aula (acende em "continuar"; é o botão real "Confirmar e começar a primeira aula"). A tela real da introdução (R01) é onde este vídeo passa: fica fora, para não mostrar a tela dentro dela mesma.
- **9:16:** Selo no alto e os 3 passos empilhados (círculo de 180 px, texto 62 px em até 2 linhas), um acende por vez; a barrinha do vídeo no passo 1. Tudo acima da faixa da legenda.

**Cena 04 · 0:24,4 a 0:33,3** · Do teste para a assinatura · ILUSTRAÇÃO · voz: nova
> Começou pelo período de teste? Quando você contratar, essa confirmação continua valendo e o vídeo não é exigido de novo.

- **16:9:** Linha do tempo: Período de teste → Assinatura ativa. O selo verde "Combinados confirmados" nasce no teste e segue pela assinatura (faixa contínua); no fim, "Vídeo já assistido" com check. Nada riscado. A tela real diz o mesmo: "Exibido uma única vez" e "Se você estiver em teste e depois contratar, esta confirmação continuará válida."
- **9:16:** A mesma linha do tempo na vertical (teste em cima, assinatura embaixo), o selo descendo junto; texto 44 a 64 px.

### cap01 · Como funcionam os tutoriais (vinheta: COMEÇANDO; voz nova)

**Mudança em relação ao T0 atual:** A fala vira a explicação nova do Kaik (item 3), letra por letra: trilha Tutoriais do sistema, Formação Básica, módulos do plano na ordem recomendada, aulas dos módulos não contratados com "Não tem no seu plano" e a contratação por ali, uma aula por tema com descrição, legendas e materiais de apoio, progresso salvo e próxima aula. Saem "cada aula mostra uma área inteira, dividida em capítulos", a ordem antiga (configurações, equipe, cadastros, OS...) e o "combinado mais importante" (vira o 1º combinado do fecho). Fica a frase do menu da conta. Visual: telas reais da DomiFlix nova no lugar do cartão de aula com capítulos e da trilha de 7 fases; os três grupos (item 4) num mapa da trilha.

**Cena 05 · 0:33,3 a 0:37,0** · Vinheta do capítulo · VINHETA · título: T0
> COMEÇANDO · Como funcionam os tutoriais.

- **16:9:** Vinheta de capítulo do perfil (título com a voz do T0 atual).
- **9:16:** Vinheta vertical: barra verde à esquerda (x 72), área em 40 px espaçada e título em até 3 linhas de 112 px, no meio da altura.

**Cena 06 · 0:37,0 a 0:41,6** · O mapa da trilha · ILUSTRAÇÃO · voz: nova
> Na DomiFlix, o seu primeiro caminho é a trilha Tutoriais do sistema.
>
> [confirmar C3]

- **16:9:** "Tutoriais do sistema" grande à esquerda (rótulo TRILHA). Dela sai a linha da trilha com os 3 grupos em ordem (verde nos dois primeiros, vermelha no terceiro) e as aulas como pontos: Formação Básica · Módulos do seu plano (selo verde, check e texto brancos, "TEM NO SEU PLANO") · Outros módulos (selo vermelho, X e texto brancos, "NÃO TEM NO SEU PLANO"). Selos iguais aos do app. Trilha → módulos → aulas, sem temporadas. Na tela do app, o título da página é "Aprenda a usar a Dominex" (C3).
- **9:16:** "Tutoriais do sistema" em 2 linhas no topo; a trilha desce na vertical com os 3 grupos empilhados (nomes 62 px, selos 42 px), acima da faixa da legenda.

**Cena 07 · 0:41,6 a 0:46,3** · Formação Básica · TELA REAL R03 · voz: nova
> Ela começa pela Formação Básica, com aquilo que todo cliente precisa aprender.
>
> [confirmar C3]

- **16:9:** A página da DomiFlix ("Aprenda a usar a Dominex", "Olá, Camila · continue sua trilha") e zoom no Módulo 1, com o selo "FORMAÇÃO BÁSICA"; destaque no selo em "Formação Básica".
- **9:16:** A página inicial no celular (nessa lista não há selos): "Aprenda a usar a Dominex", o cartão "Trilha do seu plano" e o Módulo 1; recorte ampliado (390 → 936 px) na lista do módulo.
- **Tela real R03** (Trilha: módulo da Formação básica): "Aprenda a usar a Dominex" e "Olá, Camila · continue sua trilha"; Módulo 1 com o selo "FORMAÇÃO BÁSICA"; aulas com check e "Próxima aula recomendada".

**Cena 08 · 0:46,3 a 0:51,6** · Módulos do seu plano · TELA REAL R04 · voz: nova
> Depois vêm os módulos que fazem parte do seu plano, sempre na ordem recomendada.

- **16:9:** A câmera desce para os módulos do plano: selo verde "TEM NO SEU PLANO" em "plano"; as aulas com "Na sequência do seu plano" em "ordem".
- **9:16:** A página inicial do celular não mostra selos: o recorte vem da gaveta "Ver trilha" (a mesma lista da lateral), com os módulos do plano um embaixo do outro e o selo verde em zoom.
- **Tela real R04** (Trilha: módulos do plano, selo verde): Gestão de Contratos e PMOC e Funcionários / RH; selo verde, check e texto brancos: "TEM NO SEU PLANO"; "Na sequência do seu plano".

**Cena 09 · 0:51,6 a 0:59,7** · Outros módulos · TELA REAL R05 · voz: nova
> Você também pode assistir às aulas dos módulos que ainda não contratou. Eles aparecem identificados como “Não tem no seu plano”,

- **16:9:** A câmera desce até os outros módulos, por último: selo vermelho "NÃO TEM NO SEU PLANO" em "identificados"; as aulas com "Conheça este módulo"; em "assistir", o aviso real "Consultar fora da ordem?" e o clique em "Consultar esta aula".
- **9:16:** Gaveta "Ver trilha" no celular: o separador "Conheça outros módulos" ("Você pode assistir e contratar direto pela aula.") e o módulo com o selo vermelho em zoom.
- **Tela real R05** (Trilha: outros módulos, selo vermelho): CRM/Kanban, Emissão de Notas Fiscais, Cobranças online; selo vermelho, X e texto brancos: "NÃO TEM NO SEU PLANO"; "Conheça este módulo" e o aviso "Consultar fora da ordem?".

**Cena 10 · 0:59,7 a 1:06,3** · Contratar por ali mesmo · TELA REAL R06 · voz: nova
> para você conhecer a função na prática e, se fizer sentido, solicitar a contratação por ali mesmo.
>
> [confirmar C5]

- **16:9:** Na aula do módulo não contratado, o bloco "Conheça agora. Ative quando fizer sentido." e o botão "Adicionar ao meu plano" (conta contratada); zoom e clique em "solicitar". O valor "A partir de R$ .../mês" fica coberto. A cena para no clique: hoje o botão abre um endereço que não existe (C5).
- **9:16:** Recorte do bloco embaixo do vídeo, no celular, com o botão grande; toque em "solicitar".
- **Tela real R06** (CTA de contratação de módulo não contratado): "Conheça agora. Ative quando fizer sentido."; "Esta aula está liberada, mas a função ... ainda não faz parte do seu plano."; botão "Adicionar ao meu plano" (em teste: "Escolher meu plano").

**Cena 11 · 1:06,3 a 1:12,4** · Uma aula, um tema · TELA REAL R07 · voz: nova
> Cada aula ensina um tema em um único vídeo, com descrição, legendas e materiais de apoio.
>
> [confirmar C6]

- **16:9:** Página da aula: a trilha à esquerda, o vídeo, "(módulo) · Aula 1.4", o título e a descrição. Destaques em sequência: a descrição ("descrição"), o menu "Legendas" do player ("legendas") e "Materiais e extras" ("materiais").
- **9:16:** No celular (com a versão vertical da aula, se houver), um recorte por vez: o vídeo com a legenda → a descrição → "Materiais e extras".
- **Tela real R07** (Página da aula): vídeo com a legenda ligada (menu "Legendas"); "(módulo) · Aula 1.4", título e descrição; "Materiais e extras" com 1 ou 2 itens.

**Cena 12 · 1:12,4 a 1:17,8** · Progresso e próxima aula · TELA REAL R08 · voz: nova
> Seu progresso fica salvo, e a DomiFlix sempre indica qual é a próxima aula.

- **16:9:** Zoom na trilha à esquerda ("Sua trilha"): "Trilha do seu plano" com o percentual, as aulas 1.1, 1.2... com check em "salvo" e a próxima em destaque em "próxima".
- **9:16:** No celular, o botão "Ver trilha" abre a gaveta com a mesma lista; recorte com os checks e a próxima aula.
- **Tela real R08** (Sua trilha: aulas com progresso e próxima aula): "Sua trilha", "Trilha do seu plano" e o percentual; aulas numeradas (1.1, 1.2...) com check; a aula atual e a próxima.

**Cena 13 · 1:17,8 a 1:24,8** · Onde encontrar · TELA REAL R13 · voz: nova
> Pra encontrar, é só abrir o menu da sua conta e clicar em Tutoriais DomiFlix.

- **16:9:** Sistema com o menu da conta aberto (cartão da foto no rodapé da barra lateral); "Tutoriais | Domiflix" destacado e clicado em "Tutoriais". Rótulo igual na 1.38.11.
- **9:16:** Celular: Menu → seção Conta, recorte dos atalhos; "Tutoriais | Domiflix" em destaque.
- **Tela real R13** (Menu da conta: Tutoriais | Domiflix): menu da conta: Perfil, Assinatura, Tema, Tutoriais | Domiflix, Central de Ajuda, Falar com o Suporte.

### cap02 · O seu progresso (vinheta: COMEÇANDO; voz nova)

**Mudança em relação ao T0 atual:** Capítulo novo: o percentual da trilha (item 5), os lembretes dos primeiros 30 dias (item 6) e as outras trilhas no futuro (item 9).

**Cena 14 · 1:24,8 a 1:28,0** · Vinheta do capítulo · VINHETA · título: voz nova
> COMEÇANDO · O seu progresso.

- **16:9:** Vinheta de capítulo do perfil (título com voz nova).
- **9:16:** Vinheta vertical, como a do capítulo 1.

**Cena 15 · 1:28,0 a 1:34,5** · A barra de progresso · TELA REAL R02 · voz: nova
> Na barra de progresso da trilha, só contam a Formação Básica e os módulos do seu plano.

- **16:9:** Zoom no bloco "Trilha do seu plano" com o percentual e a barra; embaixo, "X de Y aulas concluídas · Formação básica Z%". Destaque em "Trilha do seu plano".
- **9:16:** O cartão do topo da página no celular ("Trilha do seu plano", "X de Y aulas", o percentual e "Formação básica: ..."), ampliado.
- **Tela real R02** (Trilha do seu plano: barra de progresso): "Trilha do seu plano" e o percentual; barra de progresso; "Formação básica" com o percentual dela.

**Cena 16 · 1:34,5 a 1:39,9** · Explorar à vontade · ILUSTRAÇÃO · voz: nova
> As aulas dos outros módulos você explora à vontade, sem atrapalhar o seu progresso.

- **16:9:** O mapa da trilha de novo: uma chave verde abraça Formação Básica e Módulos do seu plano ("Contam no progresso"); Outros módulos fica fora ("Explorar à vontade"). Uma aula do grupo vermelho ganha check e o percentual não se mexe.
- **9:16:** Grupos empilhados; uma chave verde à direita junta os dois primeiros ("Contam no progresso"); o terceiro embaixo com "explorar à vontade"; o percentual no topo (120 px), parado.

**Cena 17 · 1:39,9 a 1:49,5** · Lembretes de 30 dias · ILUSTRAÇÃO · voz: nova
> Nos primeiros 30 dias, a Dominex vai te lembrar de continuar, até você concluir a Formação Básica e os tutoriais dos módulos do seu plano.

- **16:9:** Faixa de 30 dias com sininhos em alguns dias; a barra de progresso enche até 100% e a faixa termina em "Concluído". No fim, a faixa real do lembrete no topo do sistema (R11): "Camila, vamos retomar de onde você parou?", o selo "Contratado" e "Continuar trilha".
- **9:16:** Calendário de 30 dias (6 × 5) com sininhos e, embaixo, o progresso chegando a 100%; no fim, a faixa do lembrete no topo da tela do celular ("Continuar tutorial").

**Cena 18 · 1:49,5 a 1:59,5** · Outras trilhas no futuro · ILUSTRAÇÃO · voz: nova
> No futuro, a DomiFlix pode ganhar outras trilhas, como gestão e contabilidade. Mas o primeiro foco é sempre a trilha Tutoriais do sistema.
>
> [confirmar C12]

- **16:9:** Tutoriais do sistema grande à esquerda (cheia, verde, "Primeiro foco"); à direita, Gestão e Contabilidade só em contorno tracejado ("No futuro"). Em "primeiro foco", as duas recuam. No app, quando houver mais de um, eles aparecem em "Cursos disponíveis".
- **9:16:** Empilhadas: Tutoriais do sistema grande no alto; Gestão e Contabilidade tracejadas embaixo.

### cap03 · Quando bater uma dúvida (vinheta: AJUDA; voz nova)

**Mudança em relação ao T0 atual:** Entram o reforço do Kaik (item 7, letra por letra) e o botão Tirar dúvidas com o suporte com o contexto (item 8). O Guia Técnico fica, mais curto e sem "na mesma ordem dos tutoriais" (a trilha mudou; ver sinalizações). O WhatsApp pelo menu da conta fica (com "também"). Saem "Volta direto no capítulo daquele assunto" (a aula nova não tem capítulos) e a dica "quando você já assistiu à aula..." (o reforço novo diz o mesmo). Conferência na 1.38.11: a frase do botão foi ajustada ao código (ele abre o WhatsApp com a mensagem pronta; antes dizia "ele já envia").

**Cena 19 · 1:59,5 a 2:02,8** · Vinheta do capítulo · VINHETA · título: T0
> AJUDA · Quando bater uma dúvida.

- **16:9:** Vinheta de capítulo do perfil (título com a voz do T0 atual).
- **9:16:** Vinheta vertical.

**Cena 20 · 2:02,8 a 2:14,0** · Primeiro os tutoriais · ILUSTRAÇÃO · voz: nova
> Você não precisa esperar uma reunião para começar. Primeiro siga os tutoriais. Se depois da aula ainda restar uma dúvida específica, fale com o suporte diretamente pela própria aula.
>
> [confirmar C13]

- **16:9:** A ordem certa, sem cartões: "Comece agora" com o play (em "começar"), 1 Siga os tutoriais (em "Primeiro"), 2 Restou uma dúvida específica? (em "dúvida"), 3 Suporte pela própria aula (em "suporte"), ligados pela linha verde. Nada de reunião riscada.
- **9:16:** Os passos empilhados, um por vez (círculo de 180 px, texto 62 px).

**Cena 21 · 2:14,0 a 2:17,5** · Tirar dúvidas com o suporte · TELA REAL R09 · voz: nova
> É só clicar em Tirar dúvidas com o suporte:

- **16:9:** Na página da aula, o botão verde "Tirar dúvidas com o suporte" (com o ícone do WhatsApp, como no app); zoom e clique em "clicar".
- **9:16:** Recorte do botão embaixo do vídeo, no celular, grande; toque.
- **Tela real R09** (Botão Tirar dúvidas com o suporte): botão verde "Tirar dúvidas com o suporte", embaixo da descrição da aula.

**Cena 22 · 2:17,5 a 2:24,4** · O contexto vai junto · TELA REAL R10 · voz: nova
> o WhatsApp abre com a sua empresa, o seu usuário, o módulo e a aula já na mensagem.
>
> [confirmar C14]

- **16:9:** O que abre: a conversa do WhatsApp com a mensagem pronta. Sem gravar o WhatsApp (marca de terceiro): celular genérico, sem logo, com o texto real do app; cada item destaca com a fala: Empresa, E-mail do usuário, Módulo e Aula (a mensagem também traz "Trilha: Tutoriais do sistema").
- **9:16:** Os itens da mensagem em linhas grandes (56 px), um destaque por vez, acima da faixa da legenda.
- **Tela real R10** (Mensagem pronta para o suporte no WhatsApp): "Olá, equipe de suporte! Preciso tirar uma dúvida sobre a aula 2.1 — (aula), da DomiFlix."; E-mail do usuário: camila.duarte@glacialcold.example; Empresa: Glacial Cold Brasil · Trilha: Tutoriais do sistema; Módulo: Gestão de Contratos e PMOC · Aula: 2.1 — (aula); Minha dúvida:.

**Cena 23 · 2:24,4 a 2:33,2** · Guia Técnico · TELA REAL R15 · voz: nova
> Se você preferir ler, o Guia Técnico explica cada função por escrito, tela por tela, no endereço dominex.app/guia-tecnico.
>
> [confirmar C15]

- **16:9:** A página do Guia Técnico (já existe): "Manual completo do produto", "Guia Técnico", "Buscar no guia…"; o endereço dominex.app/guia-tecnico digitado na barra em "endereço".
- **9:16:** O Guia no celular (recorte do topo) e o endereço em texto grande (64 px) embaixo do recorte.
- **Tela real R15** (Guia Técnico (página pública)): topo do guia e a busca; endereço dominex.app/guia-tecnico.

**Cena 24 · 2:33,2 a 2:41,7** · WhatsApp pelo menu · TELA REAL R14 · voz: nova
> Fora da aula, o suporte também atende pelo WhatsApp, em Falar com o Suporte, no menu da sua conta.

- **16:9:** Menu da conta aberto; "Falar com o Suporte" destacado e clicado em "Falar".
- **9:16:** Celular: Menu → Conta; "Falar com o Suporte" em destaque.
- **Tela real R14** (Menu da conta: Falar com o Suporte): menu da conta com "Falar com o Suporte".

### cap04 · A sua assinatura (vinheta: ASSINATURA; fala e áudio do T0 atual, sem voz nova)

**Mudança em relação ao T0 atual:** Fala idêntica ao T0 atual (reaproveita o áudio). Código da assinatura igual da 1.38.6 para a 1.38.11. Visual: tela real da Assinatura (já existe) com os valores cobertos, no lugar do cartão desenhado (decisão D2).

**Cena 25 · 2:41,7 a 2:44,9** · Vinheta do capítulo · VINHETA · título: T0
> ASSINATURA · A sua assinatura.

- **16:9:** Vinheta de capítulo do perfil (título com a voz do T0 atual).
- **9:16:** Vinheta vertical.

**Cena 26 · 2:45,0 a 2:57,4** · A tela Assinatura · TELA REAL R16 · voz: T0
> Tudo sobre o seu plano fica na tela Assinatura, também no menu da sua conta. Ali você vê o status, o plano, o vencimento e o valor, acompanha o uso da conta e o histórico de pagamentos.

- **16:9:** Menu da conta → "Assinatura" (em "Assinatura"); a tela com destaques na ordem da fala: status, plano, vencimento, valor (coberto), uso da conta, histórico de pagamentos. Valores em R$ cobertos por tarja lisa (D2).
- **9:16:** A Assinatura no celular, um recorte por vez: status, plano e vencimento → uso da conta → histórico.
- **Tela real R16** (Assinatura): status Ativa, Plano, Vencimento, Valor mensal (coberto); Uso da conta; Histórico de pagamentos.

**Cena 27 · 2:57,4 a 3:11,7** · Pagar Agora · TELA REAL R17 · voz: T0
> Pra pagar, é só clicar em Pagar Agora: dá pra usar Pix, boleto ou cartão. No plano anual, o Pix e o boleto têm 20% de desconto; no cartão, a cobrança é mensal e renova sozinha.

- **16:9:** Card Pagamento: clique em "Pagar Agora"; destaque em "20% de desconto no plano anual · válido para Pix ou Boleto"; as formas Pix, Boleto e Cartão; no "cartão", o aviso de renovação automática. Valores cobertos.
- **9:16:** Recortes em sequência: botão Pagar Agora → Pix, Boleto, Cartão empilhados → o selo do anual.
- **Tela real R17** (Assinatura: pagamento): Pagar Agora; 20% de desconto no plano anual · válido para Pix ou Boleto; Pix, Boleto, Cartão.

### cap05 · Quando a empresa cresce (vinheta: ASSINATURA; fala e áudio do T0 atual, sem voz nova)

**Mudança em relação ao T0 atual:** Fala idêntica ao T0 atual (reaproveita o áudio). Visual: Gerenciar Meu Plano real (valores cobertos); as ilustrações do teste e do proporcional ficam, reestilizadas (sem cartões e sem cinza).

**Cena 28 · 3:11,7 a 3:14,9** · Vinheta do capítulo · VINHETA · título: T0
> ASSINATURA · Quando a empresa cresce.

- **16:9:** Vinheta de capítulo do perfil (título com a voz do T0 atual).
- **9:16:** Vinheta vertical.

**Cena 29 · 3:14,9 a 3:23,4** · Teste e plano · ILUSTRAÇÃO · voz: T0
> No período de teste, todos os módulos ficam liberados pra você conhecer; ao ativar a assinatura, ficam os do plano que você escolheu.

- **16:9:** Os módulos (nomes do catálogo) em grade de ícone e texto, todos acesos sob "Período de teste"; em "ativar a assinatura", ficam acesos só os do plano e os outros viram contorno com "+".
- **9:16:** Os módulos numa coluna (texto 46 px, quadrado de 92 px), com a mesma virada.

**Cena 30 · 3:23,4 a 3:35,5** · Gerenciar Meu Plano · TELA REAL R18 · voz: T0
> E quando a sua empresa crescer, o plano cresce junto. Em Gerenciar Meu Plano, você escolhe um dos Planos Prontos ou monta o seu no Personalizado, com os módulos e os usuários que precisar.

- **16:9:** "Gerenciar Meu Plano": abas "Planos Prontos" e "Personalizado" (clique em "Personalizado"), módulos, usuários adicionais e o painel "Seu Plano". Valores cobertos (D2).
- **9:16:** Recortes do celular: as abas → a lista de módulos → usuários adicionais.
- **Tela real R18** (Gerenciar Meu Plano): abas Planos Prontos e Personalizado; módulos e usuários adicionais; painel Seu Plano (valores cobertos).

**Cena 31 · 3:35,5 a 3:44,4** · O proporcional · ILUSTRAÇÃO · voz: T0
> E funciona assim: se você aumenta o plano no meio do caminho, paga hoje só a diferença, proporcional aos dias que faltam até o vencimento.

- **16:9:** O ciclo numa linha: Início do ciclo · Hoje · Vencimento; o trecho "Já pago" em contorno escuro e o que falta em verde, "Cobrança proporcional hoje".
- **9:16:** O ciclo na vertical (início em cima, vencimento embaixo), o trecho que falta em verde.

**Cena 32 · 3:44,4 a 3:51,4** · Liberado e renovação · ILUSTRAÇÃO · voz: T0
> Os recursos novos entram assim que o pagamento é confirmado, e a renovação seguinte já vem com o valor do plano novo.

- **16:9:** "Pagamento confirmado" → "Liberado"; embaixo, "Próxima renovação: valor do plano novo".
- **9:16:** Empilhado: confirmado → liberado → próxima renovação.

**Cena 33 · 3:51,4 a 3:59,0** · Reduzir o plano · ILUSTRAÇÃO · voz: T0
> E se você reduzir, continua com tudo até o vencimento, e o valor menor começa no próximo ciclo.

- **16:9:** "Reduzir o plano": "Ciclo atual: tudo liberado até o vencimento" e "Próximo ciclo: valor menor", com o rótulo real "Mudança de valor agendada".
- **9:16:** Empilhado: ciclo atual em cima, próximo ciclo embaixo.

### cap06 · Os combinados (vinheta: RECAPITULANDO; voz nova)

**Mudança em relação ao T0 atual:** No lugar do fecho antigo ("no próximo tutorial, a gente coloca a logo...", que apontava para o T1): recapitulação dos combinados, o convite para confirmar e a primeira aula da Formação Básica.

**Cena 34 · 3:59,0 a 4:02,2** · Vinheta do capítulo · VINHETA · título: voz nova
> RECAPITULANDO · Os combinados.

- **16:9:** Vinheta de capítulo do perfil (título com voz nova).
- **9:16:** Vinheta vertical.

**Cena 35 · 4:02,2 a 4:08,0** · Combinado 1 · ILUSTRAÇÃO · voz: nova
> Então, recapitulando: primeiro a Formação Básica e os módulos do seu plano, na ordem indicada.

- **16:9:** Lista "Os combinados" em texto grande, sem cartões; o item 1 entra com check: "Formação Básica e módulos do plano", e embaixo, menor, "na ordem indicada".
- **9:16:** A lista item por item: título 60 px (até 2 linhas) e a linha de baixo em 46 px; check de 110 px.

**Cena 36 · 4:08,0 a 4:13,0** · Combinado 2 · ILUSTRAÇÃO · voz: nova
> Restou uma dúvida depois da aula? Fale com o suporte pela própria aula.

- **16:9:** Item 2: "Dúvida depois da aula?" e, embaixo, "suporte pela própria aula".
- **9:16:** Item 2 entra embaixo do 1.

**Cena 37 · 4:13,0 a 4:16,4** · Combinado 3 · ILUSTRAÇÃO · voz: nova
> E o seu plano você acompanha na tela Assinatura.

- **16:9:** Item 3: "Plano e pagamentos" e, embaixo, "tela Assinatura".
- **9:16:** Item 3 entra embaixo do 2.

**Cena 38 · 4:16,4 a 4:23,8** · Confirmar e seguir · TELA REAL R12 · voz: nova
> Agora é só confirmar que entendeu os combinados e seguir pra primeira aula. Te vejo lá!
>
> [confirmar C16]

- **16:9:** A confirmação real no fim do vídeo: a caixa "Assisti ao vídeo até o final e entendi os combinados." e o botão "Confirmar e começar a primeira aula" (em "confirmar"); depois, a próxima aula da Formação básica.
- **9:16:** No celular, abaixo do vídeo vertical: a caixa e o botão em recorte ampliado; depois, a próxima aula.
- **Tela real R12** (Confirmação no fim do T0): caixa "Assisti ao vídeo até o final e entendi os combinados."; botão "Confirmar e começar a primeira aula"; "Exibido uma única vez".

### Cartela

**Cena 39 · 4:23,8 a 4:27,2** · Cartela · VINHETA
> (sem fala) Até a próxima aula!

- **16:9:** Cartela do perfil: "Até a próxima aula!" (proposta D1: logo DomiFlix branco).
- **9:16:** Cartela vertical: capacete e DOMINEX no meio da altura, logo DomiFlix branco e a frase em 72 px.

<!-- /CENAS -->

## Produção (depois do ok)
1. **Voz** (só depois do ok e com crédito): um nó por capítulo novo (`T00v2 cap00` a `cap03` e `cap06`) e um nó
   `T00v2 títulos` ("O seu progresso. [pause] Os combinados."); `proc.py` e `titulos.py`. Os capítulos 4 e 5 e os títulos
   1, 3, 4 e 5 vêm do T0 atual (`capNN.json`, wav e `titulos/`), renumerados.
2. **Telas:** todas existem na 1.38.11 (R01 a R12 na DomiFlix nova; R13 a R18 sem mudança), mas nenhuma é gravável no app de
   gravação de hoje (8080, na 1.38.9). Precisa de uma segunda instância 1.38.11 com backend falso próprio: plano em
   `telas_necessarias.md`, "Plano de captura na 1.38.11". Cada tela em duas capturas: computador (1280×800, para o 16:9) e
   celular (390×844, para o 9:16). O botão de contratar abre uma página que não existe (C5): a cena 10 para no clique.
3. **Ilustrações:** refazer `edit/cenas/cenas.html` no estilo novo, com uma versão 16:9 (1280×800) e uma 9:16 (1080×1920)
   de cada cena, presas às palavras, e nada essencial nas faixas da legenda.
4. **9:16 no pipeline:** palco, vinhetas, cartela e montagem verticais estão com outro agente, numa área própria. Do lado da
   DomiFlix, a 9:16 é a "Versão para celular" da mesma aula (campo do painel admin: "Use o mesmo conteúdo em vídeo vertical
   9:16. No celular ele substitui automaticamente a versão horizontal.", `src/pages/admin/AdminDomiflix.tsx:709`).
5. **Legendas:** a DomiFlix guarda as legendas **por aula**, não por vídeo (`domiflix_episode_subtitles`), e a primeira enviada
   já vem ligada. As duas versões usam o mesmo arquivo: a 16:9 e a 9:16 precisam ter **exatamente a mesma linha do tempo**
   (mesmo áudio, mesmos cortes). Linhas de até ~40 caracteres cabem no player vertical (fonte de 14 px num vídeo de ~370 px
   de largura). O SRT e o VTT "de cada versão" pedidos pelo Kaik saem iguais.
6. **Catálogo:** o T0 v2 tem de ser a **1ª aula da Formação básica** da trilha "Tutoriais do sistema", ativa e com vídeo: é
   ela que a introdução obrigatória toca (`supabase/migrations/20261031234000_domiflix_trilha_guiada.sql:521,554-563`).
7. **Entrega:** `Domiflix T0 - Boas-vindas à Dominex.mp4` (16:9) e `Domiflix T0 - Boas-vindas à Dominex (vertical).mp4`
   (9:16), cada um com `.srt` e `.vtt` do mesmo nome; na DomiFlix, o vertical entra como "Versão para celular" da mesma aula.
