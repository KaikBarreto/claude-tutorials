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
O mundo da Recicla Vale Metais no Supabase falso ainda não existe (PRODUCAO.md, "Preparação").

## O que fica igual à Domiflix
Formato (1920×1080, 30 fps, H.264 CRF 20 + AAC, ~−16 LUFS, pico ≤ −1 dBTP); palco escuro com a luz na cor da marca;
janela do app com cantos de 16 px, sombra 0,35, margem 44 px; vinheta de capítulo (área em maiúsculas, título
Montserrat 800, barra na cor do acento, o narrador lê o título, whoosh/pop/whoosh); cursor desenhado; câmera v2
(`auditar_camera.py` com 0 problema); cartões "Antes: <aula>" e "Próximo: <aula>"; avisos "Dica: ..." no positivo;
legendas .srt/.vtt; trilha lo-fi com ducking; nada coberto com tarja (os dados são fictícios e aparecem como estão).
**Sem**: contador de etapas, travessão na copy (as aberturas da fonte têm travessão: tirar), logo de terceiros, preço
de plano na fala.

## Identidade (marca `perfis/ecoflix/marca`)
- Logo oficial (repositório do EcoSistema, `src/assets`): símbolo de reciclagem em **3 peças** com gradiente verde
  (#5CE593 → #408B68) + wordmark **EcoFlix®**: `ecoflix_logo_light.png` no fundo escuro, `ecoflix_logo_dark.png` no
  claro. EcoSistema: `ecosistema_logo_light.png` e `ecosistema_logo_dark.png`. Nunca redesenhar.
- **Vinheta de abertura** (~4,4 s, molde da Domiflix): as 3 peças do símbolo se encaixam girando (no lugar das 3 peças
  do capacete), passa um brilho, o símbolo vai para a esquerda e o "EcoFlix" sai de trás; embaixo, o título da aula;
  escurece. Som proposto: o som oficial da EcoFlix que já toca no app (`src/assets/ecoflix-intro.mp3`, 4,1 s; mídia
  não vai para o git, o instalador copia do repositório do app). Decide-se na prévia.
- **Cartela final** (3,9 s): a mesma montagem do logo + "Até a próxima aula!".
- Cores: acento **#50D088** (o verde do símbolo), escuro **#121212** (fundo do tema escuro do app), claro **#F3F4F6**.
  O verde da interface do app (#16A34A) não é acento do vídeo: fica escuro demais no palco.
- Fonte **Montserrat** (a do app, igual à Domiflix). Nunca a "Netflix Sans" das telas da EcoFlix (fonte da Netflix).
- O app grava no tema padrão dele (claro).
- Grafia: **EcoFlix**, **EcoSistema**, **EcoTray**, **Cato** (o assistente).

## Voz (`voz.json`)
- Masculina, ElevenLabs, modelo **eleven_v4**, pt; voice settings padrão da voz; duas versões por nó.
- Escolha pendente (08/11): amostras no fluxo "EcoFlix · teste de voz masculina" com base44, Cristian, Davi Leão e
  Amanndev, o mesmo texto.
- Regras de fluxo da Domiflix: um nó por capítulo, um nó com os títulos dos capítulos, correções num nó só, nunca gerar
  de novo para "tentar"; o Kaik exporta o zip e o `proc.py` acha cada capítulo pelo conteúdo.
- Antes da primeira aula: um nó só com todas as palavras da tabela abaixo, na voz escolhida, para conferir.

### Pronúncia (no texto do TTS; a legenda usa a grafia da tela; `narracao/config_narracao.json`)
A troca fala → legenda precisa do mesmo número de palavras: sigla soletrada vai com hífen ("ene-éfe-é" → "NF-e").
| Tela / legenda | Texto do TTS | Situação |
|---|---|---|
| EcoSistema | Ecossistema | sabido (sem o "ss" o TTS erra) |
| EcoFlix / EcoTray / Cato | Écoflix / Ecotrêi / Cáto | testar |
| NF-e / NFS-e | ene-éfe-é / ene-éfe-ésse-é | testar |
| DANFE / SEFAZ | dânfi / séfaz | testar |
| NCM / CFOP / ICMS | ene-cê-ême / cê-fópi / i-cê-ême-ésse | testar |
| CST / CSOSN | cê-ésse-tê / cê-ésse-ó-ésse-ene | testar |
| MTR / CDF | ême-tê-érre / cê-dê-éfe | testar |
| OFX / XML / PDF | ó-éfe-xis / xis-ême-éle / pê-dê-éfe | testar |
| Kardex / Kanban / CRM | cárdecs / canban / cê-érre-ême | testar |
| CAPEX / OPEX | cápecs / ópecs | testar |
| Ctrl+K / SmartScreen / USB | contról-cá / smárti-scrím / u-ésse-bê | testar |
| QR Code / White Label / Asaas / DRE | quê-érre côde / uáit lêibou / asas / dê-érri-ê | herdado da Domiflix |
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
- **Erro de propósito na tela**: a fonte pede "mostre o erro de propósito em todo ⚠️"; a Domiflix tinha "não encenar a
  falha" (Kaik, 30/10). **Decisão do Kaik pendente** (PRODUCAO.md); até lá, vale a regra da Domiflix.

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
- O que o robô não grava com verdade (instalador do EcoTray, avisos do navegador e do SmartScreen, papel saindo da
  impressora): gravação real curta feita pelo Kaik, ou só na fala. Nunca tela inventada. Comprovante: o PDF do app.

## Edição
Igual à Domiflix (specs.json do T3, zooms por `label`, `min_w` 1300, folha de zooms, folha de 3 s do vídeo inteiro).
Zoom nos campos críticos da fonte: CNPJ, peso, valor, alíquota, chave de acesso, número da nota.
Montagem com `perfis/ecoflix/aula.json` (trilha lo-fi própria: `music_seed` provisório 5, decide-se na prévia).

## Entrega
- `EcoFlix T<n> - <Título>.mp4` + `.srt` + `.vtt` + **`.txt` com os capítulos marcados por tempo** (a descrição da aula
  na EcoFlix pede); T0 também `EcoFlix T0 - <Título> (vertical).mp4`. Nome de arquivo sem ":" (vira " - ").
- MP4 em qualidade cheia no chat, um por envio acima de ~200 MiB; no fim, ZIP das legendas e capítulos com LEIA-ME.

## Processo com o Kaik
Roteiros por lote em doc vivo, aprovação antes da voz; registro em `planejamento/ecoflix/PRODUCAO.md`; prévia de um
capítulo do T3 cedo (congela a identidade); avisar o que está rodando e quanto falta.
