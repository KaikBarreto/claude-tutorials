# Perfil EcoFlix · trilha de tutoriais do EcoSistema

**Rascunho de 08/11/2026.** O padrão é o da Domiflix (`perfis/domiflix/PERFIL.md`, o T3 congelado): tudo o que este
arquivo não muda vale igual. Mudam a marca (EcoSistema/EcoFlix), a voz (masculina), as pronúncias, o app e o mundo
fictício (Recicla Vale Metais). Vira padrão congelado quando o Kaik aprovar a prévia da primeira aula (T3); depois disso,
mudança visual ou sonora só com pedido dele.

Fonte do conteúdo: `docs/ecoflix/trilha-de-tutoriais.md` no repositório do EcoSistema (dela saem a página
`/trilha-ecoflix` e o briefing de gravação). Ordem, status e notas de produção: `planejamento/ecoflix/TRILHA.md`.
Decisões e pendências: `planejamento/ecoflix/PRODUCAO.md`.

## Instalar
```bash
TUT_HOME=~/ecoflix TUTORIAL=t3 PERFIL=ecoflix bash <pasta-da-skill>/instalar.sh
```
O instalador copia o mundo da Recicla Vale Metais (`perfis/ecoflix/mundo`) para `$TUT_HOME/rec/mundo`. Religar tudo
depois de um reinício: `$TUT_HOME/RELIGAR.md` (app 1.59.154 em `/dev/shm`, build em `$TUT_HOME/app`, porta 8080; Supabase
falso na 54340, `FAKE_NOW` do `mundo.json`).

## O que fica igual à Domiflix
Formato (1920×1080, 30 fps, H.264 CRF 20 + AAC, ~−16 LUFS, pico ≤ −1 dBTP); palco escuro com a luz na cor da marca;
janela do app com cantos de 16 px, sombra 0,35, margem 44 px; vinheta de capítulo (área em maiúsculas, título
Montserrat 800, barra na cor do acento, o narrador lê o título, whoosh/pop/whoosh); cursor desenhado; câmera v2
(`auditar_camera.py` com 0 problema); cartões "Antes: <aula>" e "Próximo: <aula>"; avisos "Dica: ..." no positivo;
legendas .srt/.vtt; trilha lo-fi com ducking; nada coberto com tarja (os dados são fictícios e aparecem como estão).
**Sem**: contador de etapas, travessão na copy (as aberturas da fonte têm travessão: tirar), logo de terceiros, preço
de plano na fala.

## Identidade (marca `perfis/ecoflix/marca`, estilo `ecosistema-reciclagem`)
- Logo oficial (repositório do EcoSistema, `src/assets`): símbolo de reciclagem em **3 peças** com gradiente verde
  (#5CE593 → #408B68) + wordmark **EcoFlix®**: `ecoflix_logo_light.png` no fundo escuro, `ecoflix_logo_dark.png` no
  claro. EcoSistema: `ecosistema_logo_light.png` e `ecosistema_logo_dark.png`. Nunca redesenhar: as 3 peças e o nome
  saíram do `ecoflix_logo_light.png` por `kit/brand_extract.py --pecas` (cores originais; empilhadas, refazem o PNG).
- **Vinheta de abertura** (4,42 s, os tempos e curvas do capacete; escura em 4,30 s): as 3 peças giram em volta do
  centro, no sentido das setas, e se encaixam (soco e brilho), passa o reflexo, o símbolo vai para a esquerda e o
  "EcoFlix" sai de trás; embaixo, o fio verde e o título da aula (sem "▶ ECOFLIX": o nome já está no logo); escurece.
- **Som** (decidido em 10/11; o Kaik deixou a critério): o oficial do app (`src/assets/ecoflix-intro.mp3`, "tã-dã" em
  Ré com cauda que morre sozinha), inteiro: o 1º golpe cai quando a última peça assenta (0,88 s) e o 2º no encaixe
  (1,02 s); por baixo, o respiro e os whooshes das peças; −19 LUFS com 0,3 dB de limitador. Casou em duração, final e
  volume. Mídia fora do git: `APP_SRC=<código do app> bash instalar.sh` copia; sem o arquivo, vai o sintetizado da
  Domiflix 2 semitons acima (Mi maior). **Escolha (10/11): o sintetizado em Mi maior** (`"som": ""` no marca.json),
  porque o player da EcoFlix já toca o som oficial antes de cada vídeo e ele soaria duas vezes seguidas. Para voltar ao
  oficial (ex.: vídeo usado fora do player), `"som": "assets/ecoflix-intro.mp3"`.
- **Cartela final** (3,85 s): a mesma montagem do logo + fio + "Até a próxima aula!"; o encaixe em 1,20 s e a cauda do
  som some com o preto.
- Vinheta de capítulo, cartões "Antes:"/"Próximo:", avisos, destaques, cursor e palco: o layout da Domiflix nas cores
  daqui (tudo lê o marca.json).
- Cores: acento **#50D088** (o verde do símbolo), escuro **#121212** (fundo do tema escuro do app), claro **#F3F4F6**.
  O verde da interface do app (#16A34A) não é acento do vídeo: fica escuro demais no palco.
- Fonte **Montserrat** (a do app, igual à Domiflix). Nunca a "Netflix Sans" das telas da EcoFlix (fonte da Netflix).
- O app grava no tema padrão dele (claro).
- Grafia: **EcoFlix**, **EcoSistema**, **EcoTray**, **Cato** (o assistente).

## Voz (`voz.json`)
- **Kaik Barreto** (clone da voz do Kaik, `voice_id` KtH4mnH3mgKFGT4Ik9jZ), escolhida por ele em 10/11; ElevenLabs,
  modelo **eleven_v4**, pt; voice settings padrão da voz.
- **Uma versão por fala** e **um fluxo só** para todas as aulas ("EcoFlix · Vozes de todas as aulas"), como o Kaik pediu
  na Domiflix (30/10): ele baixa tudo de uma vez; fala ruim se regera sozinha.
- Regras de fluxo da Domiflix: um nó por capítulo, um nó com os títulos dos capítulos, correções num nó só, nunca gerar
  de novo para "tentar"; o Kaik exporta o zip e o `proc.py` acha cada capítulo pelo conteúdo.
- Antes da primeira aula: um nó só com todas as palavras da tabela abaixo, na voz escolhida, para conferir.

### Pronúncia (no texto do TTS; a legenda usa a grafia da tela; `narracao/config_narracao.json`)
Som exato: o eleven_v4 aceita IPA entre barras no lugar da palavra ("/ˈẽniˈɛfiˈe/"); é o caminho quando a grafia
não basta (NF-e, NFS-e, ICMS: soletradas soavam "blocadas", de corrido só funcionavam dentro da frase). Acento tônico
em cada letra deixa a sigla "vocal" (Kaik, 10/11). Com hífen quando a voz já lê bem (CFOP, MTR). Troca fala → legenda
com o mesmo número de palavras dos dois lados (o IPA conta como uma).
| Tela / legenda | Texto do TTS | Situação |
|---|---|---|
| EcoSistema | Ecossistema | ok (sem o "ss" o TTS erra) |
| EcoFlix / EcoTray / Cato | Écoflix / Ecotrêi / Cáto | ok (Kaik ouviu, 10/11) |
| NF-e | /ˈẽniˈɛfiˈe/ (IPA) | Kaik, 10/11 01:16: o melhor do teste 6 (o guia do eleven_v4 aceita IPA entre barras) |
| NFS-e | /ˈẽːniˈɛːfiˈɛːsiˈeː/ (IPA, provisório) | Kaik, 10/11 01:19: o S ainda ruim nos três do teste 7; teste 8 |
| SEFAZ | sefás | Kaik, 10/11: é "SEFÁS" ("séfaz" saía "séfas") |
| CFOP | cê-éfe-ó-pê | Kaik, 10/11: soletrada ("cê-fópi" saía "cêfop") |
| ICMS | /iˈseˈɛmiˈɛːsːi/ (IPA) | Kaik, 10/11 01:19: a 4 do teste 7 ("o S tá ótimo") |
| Kardex | cardécs | Kaik, 10/11: é "CARDÉX" ("cárdecs" saía "cárdex") |
| DANFE / NCM | dânfi / ene-cê-ême | ok (10/11) |
| CST / CSOSN | cê-ésse-tê / cê-ésse-ó-ésse-ene | ok (10/11) |
| MTR / CDF | ême-tê-érre / cê-dê-éfe | ok (10/11) |
| OFX / XML / PDF | ó-éfe-xis / xis-ême-éle / pê-dê-éfe | ok (10/11) |
| Kanban / CRM | canban / cê-érre-ême | ok (10/11) |
| CAPEX / OPEX | cápecs / ópecs | ok (10/11) |
| Ctrl+K / SmartScreen / USB | contról-cá / smárti-scrím / u-ésse-bê | ok (10/11) |
| QR Code / White Label / Asaas / DRE | quê-érre côde / uáit lêibou / asas / dê-érri-ê | ok (Domiflix e 10/11) |
CNPJ, CPF, CEP, Pix: escrita normal. Números por extenso como se fala ("quarenta e dois reais e cinquenta", "mil e
duzentos quilos"); na legenda: kg, t, mm, %. Palavra nova difícil: testar num trecho curto e anotar aqui.

## Fala
Igual à Domiflix (colega mostrando ao vivo, "a gente" e "você", frases curtas, conectores com moderação, exemplo antes da
regra, rótulos exatamente como na tela, fala que vale nas duas versões quando o comportamento pode mudar). E, da fonte:
- Vocabulário do cliente: **cliente** é para quem a empresa vende; **fornecedor** é de quem ela compra. Pedido, caixa,
  cofre, saldo (fiado), tabela de preço, ticket de pesagem. Nada de "entidade", "registro", "módulo X do sistema".
- Dados do pátio ditos em voz alta (material, peso, valor), sempre do mundo da Recicla Vale Metais.
- ⚠️ entra falado, aberto com **"Uma dica:"**, na hora em que o cliente cairia nele.
- 🚫 entra como informação do que acontece ("sem a opção, concluir não mexe no estoque"), no tom positivo da Domiflix.
- 🔒 ao entrar numa parte de módulo, dizer que ela depende do plano contratado. Sem preço.
- **Erro na tela** (Kaik, 10/11): caminho certo primeiro e a consequência como informação; a mensagem de erro só
  aparece na tela quando reconhecê-la é o ponto ("Abra o caixa antes de realizar compras", "Popup bloqueado", o aviso
  do cofre), com a saída logo em seguida. A fonte pedia o erro em todo ⚠️; a Domiflix, nunca.
- **Fiscal**: regime do exemplo **Lucro Real** (Kaik, 10/11: o padrão de muita reciclagem); a fala mostra os campos e
  diz que quem define a tributação é o contador, sem ensinar regra tributária.

## Estrutura de cada aula (o "molde" da fonte é o da Domiflix)
1. Abertura (20 a 30 s): "Oi! Neste tutorial a gente vai..." com o problema real, citando a Recicla Vale Metais.
2. Pré-requisito (10 a 15 s), com o cartão "Antes: <aula>".
3. Onde fica: o caminho do menu clicado na tela; depois o tour (abas, cartões do topo, filtros, botão principal).
4. Capítulos = os da fonte, na ordem; cada um com vinheta de capítulo e a ação feita de verdade na tela.
5. Recapitulando (40 a 60 s): a lista do que foi executado, em fala corrida.
6. Próximo (10 s), pelo benefício, com o cartão "Próximo: <aula>"; fecha com "Até lá!".
A minutagem da fonte é alvo; a duração é a da fala (~790 caracteres de narração por minuto).

## App, mundo fictício e gravação
- Modo fakebase com o código do EcoSistema na **versão publicada** (`git archive <commit>`; o repositório do app é
  somente leitura) → `APP_SRC=<pasta> rec/setup-app.sh` → schema gerado do `src/integrations/supabase/types.ts`.
  Nunca gravar contra o Supabase real nem em conta de cliente.
- Mundo: **Recicla Vale Metais** (`planejamento/ecoflix/MUNDO_FICTICIO.md`), `FAKE_NOW=2026-11-10T08:30:00-03:00`.
- Integrações simuladas no backend falso, com a tela fiel ao código: EcoTray (peso e impressão), NF-e, NFS-e, MTR e CDF
  (sem SEFAZ, sem cota, sem queimar numeração), cobrança da assinatura, extrato OFX, respostas do Cato.
- Celular (`device: phone`): T0 vertical; trechos do T5 (indicador de peso) e do T19 (ponto).
- **Cena de Windows** (Kaik, 10/11): nas aulas do EcoTray, o que acontece no Windows (baixar, instalar, a janela do
  EcoTray, a bandeja, os avisos) é uma tela de Windows simulada com a pessoa usando, junto do sistema no navegador. A
  janela do EcoTray é a do código (`ecotray/dashboard.py`, `tray_app.py`, `installer_win/installer_gui.py`): textos,
  cores, fonte e medidas exatos. A área de trabalho é genérica no estilo Windows, sem logo nem ícones da Microsoft.
- Papel saindo da impressora: só na fala ou ilustração. Nunca tela inventada do app. Comprovante: o PDF do app.

## Edição
Igual à Domiflix (specs.json do T3, zooms por `label`, `min_w` 1300, folha de zooms, folha de 3 s do vídeo inteiro).
Zoom nos campos críticos da fonte: CNPJ, peso, valor, alíquota, chave de acesso, número da nota.
**Ilustração de conceito** (Kaik, 10/11: bem mais que na Domiflix): cada `[ILUSTRAÇÃO: ...]` do roteiro vira uma cena
do kit `cenas/cenas_ecoflix.html` (estilo, utilidades e os exemplos "Tara e peso líquido" e "Caixa × competência"),
presa às palavras da fala, renderizada só no trecho (`--de/--ate`) e encaixada sobre a janela do app
(`docs/09-aula-ilustrada.md`, "Ilustração de conceito no meio do capítulo"); antes da voz, com tempos estimados.
Montagem com `perfis/ecoflix/aula.json` (trilha lo-fi própria: `music_seed` provisório 5, decide-se na prévia).

## Entrega
- `EcoFlix T<n> - <Título>.mp4` + `.srt` + `.vtt` + **`.txt` com os capítulos marcados por tempo** (a descrição da aula
  na EcoFlix pede); T0 também `EcoFlix T0 - <Título> (vertical).mp4`. Nome de arquivo sem ":" (vira " - ").
- MP4 em qualidade cheia no chat, um por envio acima de ~200 MiB; no fim, ZIP das legendas e capítulos com LEIA-ME.

## Processo com o Kaik
Roteiros por lote em doc vivo, aprovação antes da voz; registro em `planejamento/ecoflix/PRODUCAO.md`; prévia de um
capítulo do T3 cedo (congela a identidade); avisar o que está rodando e quanto falta.
