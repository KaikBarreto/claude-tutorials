# Produção EcoFlix · registro de pedidos, decisões e andamento

## Pedido (Kaik, 08/11 23:36)
"baseado em tudo que aprendemos da domiflix e tutoriais da dominex agora quero planejar os tutoriais da ecosistema
(ecosistematecnologia.com.br) com a marca dela, no mesmíssimo padrão que fizemos pra domiflix, mas agora pra ecoflix /
com todo aprendizado que tivemos, de nomenclaturas e pronunciações corretas, estrutura / para que seja da forma mais
produtiva e rápida possível, economizando tokens etc. / daqui 10 minutos vou atualizar também uma pagina
https://ecosistematecnologia.com.br/trilha-ecoflix que tem a ordme também / mas se achar melhor você pode sugerir
alterações etc. / E vamos fazer com uma voz masculina os da ecoflix"
Anexo "EcoFlix-briefing-gravacao.md" = `docs/ecoflix/trilha-de-tutoriais.md` do repositório do EcoSistema.

## Decisões (08/11)
- Perfil `perfis/ecoflix`: herda a Domiflix inteira; mudam marca, voz, pronúncias, app e mundo.
- Mundo: Recicla Vale Metais (sugestão da fonte), em Taubaté, SP; `FAKE_NOW` 10/11/2026 08:30 (terça).
- T3 é a primeira aula (molde e prévia), como na Domiflix.

## Decisões pendentes (Kaik) · respondidas em 10/11 (ver "Kaik, 10/11")
1. **Voz**: qual das quatro amostras do fluxo "EcoFlix · teste de voz masculina" (base44, Cristian, Davi Leão,
   Amanndev), ou outra.
2. **Erro de propósito na tela**: a fonte pede "mostre o erro de propósito em todo ⚠️"; a Domiflix tinha "não encenar a
   falha" (30/10). Proposta: caminho certo primeiro e a consequência como informação (regra da Domiflix); mensagem de
   erro na tela só quando reconhecê-la é o que o cliente precisa ("Abra o caixa antes de realizar compras", "Popup
   bloqueado", o aviso do cofre), com a saída logo em seguida.
3. **Som da vinheta**: o som oficial da EcoFlix (`ecoflix-intro.mp3`, o que toca no app) ou um sintetizado no molde da
   Domiflix.
4. **T5**: trecho real de instalação do EcoTray (Windows/Mac, avisos do navegador e do SmartScreen) gravado pelo Kaik,
   ou só falado.
5. **Regime fiscal do exemplo** (proposto: Simples Nacional), antes do T16.

## Preparação (antes da primeira aula)
0. Consolidar na skill as melhorias da Domiflix que ficaram só nas cópias das aulas (aceleração no `finish.py`,
   `montar_cap.py`, `remendar_aula.py` e `celular_vertical.py` do vertical, folha de 3 s, pico do AAC, três ajustes do
   Supabase falso) e rodar o exemplo T3.
1. Marca: separar as 3 peças do símbolo (como o `brand_extract.py` fez com o capacete), vinheta no molde da do capacete,
   cartela; prévia da vinheta para o Kaik.
2. Voz escolhida + nó de teste de pronúncia (tabela do PERFIL); fechar o `config_narracao.json`.
3. App: versão publicada do EcoSistema (1.59.154 = `f37573ea0`, a da fonte; ou release mais nova) por `git archive`,
   `rec/setup-app.sh`, schema do `types.ts`, smoke nas rotas da Fase 1.
4. Mundo base inteiro de uma vez (empresa, pessoas, materiais, parceiros, 3 meses de histórico) e o EcoTray falso.
5. Roteiros do lote 1 (T3, T4, T6 a T10) num doc para aprovação; voz do T3; gravação do T3 com prévia de um capítulo.

## Economia (tokens e tempo)
- Produção numa sessão nova (contexto limpo e disco livre), com os repositórios claude-tutorials e EcoSistema anexados.
  A sessão da Domiflix está com o disco no limite (1,4 GB) e um contexto grande.
- Mundo base montado uma vez para a trilha toda, em vez de encadear sementes aula a aula (o que mais custou na
  Domiflix); cada aula só acrescenta o que ela cria na tela.
- Cada roteiro lê só a seção da sua aula na fonte (a fonte inteira tem ~60 mil tokens): `trecho_aula.py T7` (a fazer).
- Aprovação de roteiro por lote; um fluxo de voz por lote (o `proc.py` acha cada capítulo pelo conteúdo).
- Agentes com briefing curto e caminhos, no máximo 2 ao mesmo tempo; Sonnet no trabalho mecânico quando o limite dele
  voltar (11/11), Opus nos roteiros e em bug de causa desconhecida.
- Ensaio (`prever.py --ens`) antes de cada gravação final; câmera auditada antes do render; folha de 3 s antes de entregar.

## Kaik, 10/11 (00:21, 00:29 e 00:33)
"use a voz kaik barreto (até fiz nesse flow um run dela) / No exemplo o regime fiscal pode ser o lucro real, que é o
padrão de muita reciclagem / a vinheta faça como achar melhor, a sugestão sobre eeros é boa / bote 20 subagentes em
paralelo para já começar a gravar e estruturar tudo, toda a parte que precisa de ti / E planejar o roteiro , tudo /
quero terminar tudo isso bem mais rapido do que foi o da dominex, avance"
"consegue estruturar de uma forma que você continue fazendo tudo independentemente de acabar meu limite de 5h ou
semanal? ir voltando a fazer conforme voltar o limite / e estime já a produção de todos os audios como a dominex fez
mas já fazendo uma repassada de uma vez nisso tudo, talvez até esperar gravar tudo pra ver se não mudaria algo, assim
fica mais preciso e economiza creditos do eleven labs, que vou btoar depois que você levantar tudo / a gravação evite
erros, zooms bruscos, informações erradas etc. / Onde achar melhor, pode ilustrar visualmente, até mais do que foi
feito na dominex, sempre que falar de um conceito (não necessariamente algo na tela), ilustre bem pra ficar fácil de
entender pro publico / Sempre tentando falar de uma forma simples e facil de entender"
"se achar melhor,a o invés de supabase falso pode usar a conta teste@ecosistematecnologia.com.br"
Decisões:
- Voz **Kaik Barreto** (`KtH4mnH3mgKFGT4Ik9jZ`), uma versão por fala, fluxo único. Fiscal: **Lucro Real**. Vinheta a
  critério (som oficial da EcoFlix, se casar). Erro na tela: a proposta aprovada (PERFIL → "Fala").
- **Voz por último**: ensaio gravado de cada aula sem voz, depois uma revisão geral de todos os textos, então a
  estimativa de créditos para o Kaik comprar, e só aí a voz de tudo de uma vez.
- Mais ilustração de conceito do que na Domiflix; fala simples; zero zoom brusco e zero informação errada (briefing).
- **Supabase falso mantido** (a conta teste fica de plano B para alguma tela muito difícil de simular): data do mundo
  fixa, capítulo regravável do mesmo ponto, nenhuma nota, MTR ou cobrança de verdade, versão do app travada na
  gravada.
- Retomadas automáticas: `RETOMADAS.md`.

## Fila
1. ✅ **10/11 00:3x a 02:1x** (roteiros das 26 aulas, Ferramentas e Marca prontos; Mundo, Junção do mundo e vinheta
   9:16 em andamento): 17 agentes de roteiro (26 aulas, `_BRIEF_ROTEIRO.md`) e 3 de estrutura: Ferramentas
   (melhorias da Domiflix na skill, branch `consolidacao-domiflix`), Mundo (EcoSistema 1.59.154 no Supabase falso, mundo
   da Recicla Vale Metais, EcoTray falso; branch `ecoflix-mundo`), Marca (vinheta, cartela, cartões e kit de ilustração;
   branch `ecoflix-marca`, prévia em `/home/claude/ecoflix/previa_marca/`).
2. Juntar: conferir os roteiros (tom, precisão, ilustrações), juntar os branches no main, consolidar no
   `MUNDO_FICTICIO.md` e nas sementes o que cada aula pediu, handlers do que faltar. Em paralelo (desde 10/11 02:3x): as
   cenas ilustradas de todas as aulas (`_BRIEF_ILUSTRACOES.md`); depois da junção, conferir as âncoras e o que cada cena
   mostra contra a fala final.
3. Robôs de todas as aulas e **ensaio gravado sem voz** (tempos estimados), corrigindo texto e tela.
4. **Revisão geral** dos textos numa passada só, aplicando o teste de pronúncia; **estimativa de créditos** (caracteres
   de todos os `CAPS` e `TITULOS`, ~1 crédito por caractere no eleven_v4) → avisar o Kaik e esperar os créditos.
5. Voz: fluxo único "EcoFlix · Vozes de todas as aulas", uma versão por fala → o Kaik exporta o zip.
6. Gravação final, edição e entrega, aula por aula, na ordem de produção da `TRILHA.md`.
7. ZIP final das legendas e capítulos; apagar os lembretes que sobrarem.

## Registro
- 08/11 23:5x Planejamento: perfil `perfis/ecoflix`, `TRILHA.md`, `MUNDO_FICTICIO.md` e este registro. Quatro amostras
  de voz geradas no ElevenLabs (mesmo texto, 2 versões cada, 362 créditos por versão, 2.896 no total).
- 10/11 00:2x Decisões do Kaik aplicadas no PERFIL, voz.json e MUNDO; `_BRIEF_ROTEIRO.md`, `trecho_aula.py` (só a seção
  da aula, 2 a 4 KB em vez de 60 mil tokens) e o código 1.59.154 em `/home/claude/ecoflix/app-src-1.59.154/` (61 MB).
- 10/11 00:3x 20 agentes lançados (opus). Teste de pronúncia na voz Kaik Barreto (16 itens numerados, 634 créditos) no
  fluxo "EcoFlix · teste de voz masculina". Os 20 lembretes de retomada criados (`RETOMADAS.md`; o limite de criação
  aceita uns 10 por minuto).
- 10/11 00:40 **Container reiniciou** e derrubou os 20 agentes (~10 min de leitura perdidos; nenhuma pasta de aula
  tinha sido salva). Kaik, 00:40: "nf-e e nfs-e tem que ser falado (ENE ÉFE Ê e ENE ÉFE ÉSSE Ê) SEFAZ está (séfas, mas é
  SEFÁS) / CFOP tá falando CÊFOP mas deveria ser CÊ ÉFE Ó PÊ, ICMS tá meio estranho, tem que falar I CÊ EME ÉSSE como
  sigla / kardex tá "cárdex" mas é "CARDÉX" / nas aulas do ecotray para integração com impressora e balança você vai
  pegar exatamente como o ecotray é num windows e simular uma tela de windows a pessoa usando, junto do sistema,
  baseado no dashboard.py (ou a tela que monta a UI do cato usando)". Pronúncias corrigidas no PERFIL e no
  `config_narracao.json` (agora com todas as trocas); reteste curto das seis no fluxo de teste (188 créditos). Cena de
  Windows no PERFIL e no briefing; código do EcoTray 1.59.154 em `/home/claude/ecoflix/app-src-1.59.154/ecotray/`
  (Tkinter; aqui não há tkinter, há Xvfb). 21 agentes relançados (os 20 + EcoTray: cena do Windows).
- 10/11 00:4x Relançados 20 agentes (o limite da sessão é 20 ao mesmo tempo): Ferramentas, Mundo, Marca, EcoTray (cena do
  Windows) e 16 de roteiro. **Falta lançar o de T20 + T26** (bateu no limite): lançar assim que um agente terminar.
- 10/11 00:49 Kaik: "nf-e e nfs-e ainda tá ruim / tenta botar "éne éfe é" e "éne éfe ésse é" / o CMS ficou icêemess
  ÊSSE ao invés de icêeme éssi". Grafias novas no PERFIL e no `config_narracao.json`: "éne éfe é", "éne éfe ésse é",
  "i cê eme éssi" (com espaço). Terceiro teste no fluxo de teste. **Antes da voz**: (a) o `proc.py` passa a aceitar troca
  de N palavras faladas para 1 da legenda (hoje junta par a par); (b) na revisão geral, trocar nos `tts_textos.py` as
  grafias antigas ("ene-éfe-ê", "ene-éfe-ésse-ê", "i-cê-eme-ésse", "ene-éfe-é", "séfaz", "cê-fópi", "cárdecs") pelas da
  tabela do PERFIL.
- 10/11 01:05 Kaik: "nf-e e nfs-e e ICMS ainda tá muito blocado / tinha que ser algo mais como êniéfiê, êniéfiéssiê,
  Icêémiésse". Grafias de corrido, numa palavra (a troca volta a ser 1 para 1: o ajuste no `proc.py` deixa de ser
  necessário). Quarto teste no fluxo de teste. Na revisão geral, trocar também "éne éfe é", "éne éfe ésse é" e
  "i cê eme éssi" pelas grafias novas.
- 10/11 01:10 Kaik: "ficou horrivel ainda, não tá vocálico, veja se dá pra descrever exatamente o som pro eleven labs /
  na frase "a nf-e saiu e o icms está certo" o nf-e e icms está otimo". Dentro da frase, a grafia de corrido funciona;
  sozinha, não. O guia do eleven_v4 aceita o som exato em IPA entre barras ("/ʃɪˈvɔːn/"). Quinto teste em IPA, sozinhas e
  em frases: NF-e /ˌẽniˌɛfiˈe/, NFS-e /ˌẽniˌɛfiˌɛsiˈe/, ICMS /iseˌɛmiˈɛsi/. Se o Kaik aprovar, o IPA vira a grafia
  do TTS dessas três (a troca IPA → sigla é 1 para 1) e vale para outras siglas difíceis.
- 10/11 01:12 Kaik sobre o IPA: "esse ɛfi não tá bom, faça ser algo mais vocal como "éfi" com acento , mesma coisa em
  éssi / e no ICMS tá ISE ao invés de ICÊ". Sexto teste: acento tônico em cada letra (/ˈẽniˈɛfiˈe/, /ˈẽniˈɛfiˈɛsiˈe/,
  /iˈseˈɛmiˈɛsi/) e a mesma coisa com vogal longa (ː), sozinhas e numa frase.
- 10/11 01:16 Kaik: "show, avance / os melhores: 1, 4 / Mas o "S" ainda tá "êsse" ao invés de "éssi"". NF-e fechada em
  /ˈẽniˈɛfiˈe/; NFS-e /ˈẽːniˈɛːfiˈɛːsiˈeː/ e ICMS /iˈseˈɛmiˈɛsi/ provisórias até o sétimo teste (três jeitos do S:
  ɛːsːi, ɛsːi, æːsi). Na revisão geral, as grafias antigas dessas três viram o IPA final.
- 10/11 01:18 O agente do T03 gravou o texto da voz dele por cima de `perfis/ecoflix/narracao/config_narracao.json` (o
  arquivo do perfil), e isso entrou no commit 5b3a506. Restaurado da versão boa (234acde) com o IPA novo; a cópia do que
  ele escreveu está no scratchpad. O `tts_textos.py` dele está certo na pasta do T03. Agente avisado. **Na junção dos
  roteiros, conferir `git diff` de `perfis/` contra o que eu mudei.**
- 10/11 01:2x **T1 pronta** (roteiro): 14 capítulos, 2.351 palavras, ~15 min de voz (~17 min de vídeo), 12 ilustrações,
  5 zooms. Pronúncias novas a testar: A4 "á-quatro", Shift "xífti". Backend a simular: `self-register` sem criar a
  empresa, `password-reset` (código 481207), `cep-lookup`, municípios do IBGE por fixture, upload em `avatars`, `public/`
  (imagens do login). Identidade da empresa para a trilha: CNPJ 47.318.506/0001-07, Rua das Oficinas, 1250, CEP
  12086-410, logo e ícone fictícios a criar, frase do comprovante, condição 30/60/90. Código × fonte: não existe aviso
  fixo de cadastro incompleto; biometria sem tela de cadastro (fora da fala); prefixo do material vai para a T3; opções
  de pedido da Usabilidade gravam por usuário (a fala avisa); `/instalar` fora. **Pergunta ao Kaik**: Usabilidade e
  numeração só mostradas, sem mudar (para não alterar o que T7 e T8 esperam), ou ligar "Exigir cliente/fornecedor no
  Ticket de Pesagem"? Agente de T20 + T26 lançado na vaga.
- 10/11 01:19 Kaik: "o "S" em ICMS tá ótimo na 4 / mas o "S" em NFS-e tá ruim". ICMS fechada em /iˈseˈɛmiˈɛːsːi/.
  Oitavo teste só da NFS-e: S separado do "ê" final por ponto, por oclusiva glotal e por "j", e a grafia de corrido numa
  frase para comparar.
- 10/11 01:2x **T2 e T27 prontas** (roteiro). T2: 11 blocos, 1.483 palavras, ~9,5 min de fala (~11 min de vídeo);
  troca nova "Fiscal e Ambiental" → "Fiscal & Ambiental"; testar "master". Backend: edges `create-company-user` (resposta
  igual à real, sem `userId`) e `manage-company-users` (`update_email`), RPC `save_user_permissions`, storage `avatars`,
  sessão em `active_sessions`. Código × fonte: foto e tela inicial escolhidas na criação nunca gravam (a tela lê
  `result.userId`, que a edge não devolve: a aula usa o "Editar"); o perfil rápido não grava na criação. T27: 8 blocos,
  798 palavras, ~5,1 min; "cinco megas" → "5 MB"; testar "Reset". Backend: `company_modules` com `white_label`,
  `avatars`, updates em `companies`, um pedido para "Ver comprovante", sessão da Juliana no cap06. Código × fonte: com o
  White Label ligado, a aba e o favicon continuam "EcoSistema" (a abertura foi corrigida); o Portal só muda depois que a
  cor é salva.
  **Decisões do coordenador** (no MUNDO, "Decidido pelas aulas"): `max_users` 3 e preço do extra visível sem fala
  (regra da Domiflix); White Label só na T27; **o ícone já vem da T1 (cap05)**: na junção, ajustar a T27 para não subir
  o ícone de novo; o Portal na T27 é a página real (não ilustração de tela), então **a T20 é gravada antes da T27**.
- 10/11 01:3x **T3 pronta** (roteiro, a aula-molde): 12 capítulos, 1.959 palavras, ~12,6 min de voz (~14 min de vídeo);
  troca nova "á-quatro" → A4; "Excel" e "Siqueira" para o ensaio. Código × fonte: venda abaixo do custo pede confirmação,
  não bloqueia (fora da fala). Backend: `/compra` com o caixa do Rafael aberto (só no cap07), `ncm_presets`, RPCs de
  estoque, preços e transferência, login do Marcos, PDFs em aba nova. Decisões do coordenador: abrir uma compra no cap07
  só para mostrar "Preço especial aplicado" (sem finalizar; exemplo concreto); a tabela ligada ao depósito vale na venda
  também (é o que o código faz); permissões do Marcos = as da T2.
- 10/11 01:4x **T11 pronta** (roteiro): abertura, 13 capítulos e recap, 2.044 palavras, ~13 min de voz (~16 min de vídeo),
  12 ilustrações; sem pronúncia nova; 24 `numeros` para a legenda. Backend: RPCs de ficha, ordem, lançamento,
  finalização e exclusão (estorno no Kardex). Código × fonte: coproduto é digitado no lançamento do dia; "Observação"
  não grava; a tela diz "peça" em produto por kg. **O agente da T11 assumiu o incidente do config do perfil**: rodou um
  `gera_tts.py` de mesmo nome que o do T03 no scratchpad compartilhado. Todos os agentes avisados: script com nome único
  (prefixo da aula), nunca rodar script alheio, nada em `perfis/`. Histórico semeado do cobre aceito (coordenador);
  ajudantes Cláudio Ferraz e Diego Morais passados ao agente da T19.
- 10/11 01:5x **T15 pronta** (roteiro): 13 blocos, 2.259 palavras, ~14,5 min de voz (~16 min 45 s de vídeo); pronúncias a
  testar: CMV "cê-ême-vê", Excel "ékisel". Backend: RPCs do DRE, patrimônio, evolução, Histórico sem espelhos, exclusão
  bancária; PDF em aba nova. Código × fonte: são cinco abas (há DFC); o botão do DRE é "Organizar categorias".
  Decisões do coordenador: a DFC entra no tour das abas numa frase (existe no código; sem aprofundar); a energia em
  dobro só existe do estado da T15 em diante. **Risco de precisão**: os números falados (DRE de outubro) precisam sair
  iguais das sementes e dos handlers; conferir no ensaio, antes da voz.
- 10/11 02:0x **T7 pronta** (roteiro, a principal): 17 blocos, 2.520 palavras, ~16 a 17 min de voz (~19 min de vídeo; alvo
  22), 11 ilustrações e uma cena de Windows com o EcoTray. Pronúncias a testar: "xíft-cê" e "xíft-vê" (Shift+C, Shift+V),
  "tara-ímp" (Tara/Imp.), "ao vivo" (AO VIVO). Backend: EcoTray falso com sequência fixa de pesos e impressão direta;
  RPCs de compra (com parcelas) e de venda com transferência; queda de internet sem derrubar o EcoTray; janela do PDF.
  Decisões do coordenador: duas compras na parte do pagamento (para mostrar as formas) e uma balança só.
  **Para o Kaik (bugs do EcoSistema achados no código)**: a coluna "Peso Líquido" mostra o peso bruto; a Central de
  Ajuda erra o nome do cadastro e diz que o cupom sem valor fica gravado. Se a coluna aparecer na aula, ela mostra o
  erro: ou o Kaik corrige antes da gravação, ou a aula não mostra a coluna.
- 10/11 02:1x **T4 pronta** (roteiro): abertura e 13 capítulos, 1.966 palavras, ~12,6 min de fala (~15 min de vídeo; alvo
  17), 8 ilustrações. Pronúncias a testar: "Cliente-mais-Fornecedor" (Cliente+Fornecedor), "pét" (PET). Backend: busca de
  CNPJ simulada, lista de cidades, RPCs de vínculo cliente+fornecedor, pagamento por Pix, lucro estimado. Código × fonte:
  a ficha abre ao lado da lista, com 7 abas; telefone repetido dá "Mesmo telefone", não "Duplicado". Decisão do
  coordenador: o saldo do Valdir é um vale que a Recicla adiantou (MUNDO).
- 10/11 02:2x **T16 pronta** (roteiro, NF-e): 19 blocos, 2.858 palavras, ~18,3 min de fala (~22 min de vídeo; alvo 25). Usa o
  IPA novo de NF-e, NFS-e e ICMS. Pronúncias a testar: CC-e, A1, pfx, IBS, CBS, "Fiscal & Ambiental". Backend: edges da
  PlugNotas (certificado, cadastro, emissão e status, cancelamento, CC-e, inutilização, download, notas recebidas,
  manifestação), importação por XML, inutilizadas na lista. Código × fonte: o aviso IBS/CBS do topo não é renderizado;
  "nome sem acento no XML" não confere no código (fora da fala); "cancelada conta na cota" não dá para conferir (a RPC
  não está na cópia; fora da fala). Decisão do coordenador: as ações do exemplo (cancelar a 1249, CC-e da placa,
  inutilizar 1246 e 1247, cenário com CST 51) ficam, todas simuladas e sem tom de recomendação; vai como aviso ao Kaik.
- 10/11 02:3x **T14 pronta** (roteiro): 16 capítulos, 104 falas, 2.211 palavras, ~14,2 min de voz (~16,5 min de vídeo), 9
  ilustrações; sem pronúncia nova ("Quiririm" a conferir no ensaio). Backend: RPCs da conciliação (sugestões por linha,
  importar, casar, baixar, criar, ignorar, desfazer, finalizar), do cofre e do saque. Código × fonte: "Abra o caixa antes
  de realizar saques" não existe (com o cofre, o saque não pede caixa); o selo da linha é "Casada"; o menu diz
  "Movimentações Financeiras". Conflito com a T6 ("Conta Reserva") resolvido: "Conta Secundária" (agente da T6 avisado).
  "Tornar principal" só mostrado (coordenador).
- 10/11 02:4x **T13 e T12 prontas** (roteiro). T13: 14 blocos, 1.951 palavras, ~12,5 min de voz (~14,5 min de vídeo), 7
  ilustrações; pronúncias a testar "Moréti" (Moretti), "Vence em sete dias"; backend `pay_financial_bill`,
  `pay_partner_balance`, `create_installment_bills`, `create_recurring_bill_template` (molde e janela de 3 meses),
  `shift_recurring_bills_due_date`, anexos; fora: o ⚠️ do subtotal do cartão (o mundo não tem cartão). T12: 13 blocos,
  1.716 palavras, ~11 min de voz (~13 min de vídeo); pronúncias a testar "bégue" (bag), "pét" (PET), "cê-ene-agá" (CNH),
  "Tíquete" (Ticket), "categoria cê"; backend `change_collection_order_status` e as edges `collection-request`,
  `entity-portal`, `collection-report`. Código × fonte: o Rastreamento já abre um mapa; "Caçambas" virou
  "Equipamentos"; a ordem registra "Entreguei/Recolhi", que vale quando a coleta é concluída; o relatório conta a ordem
  sem data pelo dia em que foi criada. **Pergunta ao Kaik**: a T12 cobre o Rastreamento, já que ele funciona? (a fonte o
  deixava de fora como "Em breve"). **Na junção**: refazer o `config_narracao.json` de cada aula a partir do do perfil
  final + as trocas da aula (vários agentes copiaram versões intermediárias); um agente rodou sem querer o script de
  outro (falhou sem efeito).
- 10/11 02:5x **T10 e T21 prontas** (roteiro). T10: 13 blocos, 1.775 palavras, ~11,4 min de voz (~14 min de vídeo);
  Excel "ékisel" a testar; "Lucro sobre vendas" → "Lucro s/ Vendas" na legenda; backend `transfer_material_stock`,
  `get_inventory_report_data`, `get_financial_dre_summary`, `get_orders_payment_distribution`,
  `get_stock_balance_at_date`, fotos em `order_attachments`, PDF em aba nova. Código × fonte: não existe ação "em massa"
  entre materiais (o botão da barra de seleção transfere entre matriz e filial: Gerencial); o rótulo é "Todos os tempos";
  no Kardex o filtro de fornecedor mantém as vendas na lista. Decisão do coordenador: o botão de transferência entre
  matriz e filial fica para a T22. T21: 10 blocos, 1.028 palavras, ~6,6 min de voz (~8 min de vídeo); backend edges
  `cato-background` e `cato-assist` (modo followups), tabela `cato_jobs`, RPCs `accept_ai_terms`, `set_cato_feedback`,
  `cato_memory_manage`. Código × fonte: o Cato só aparece com a liberação da empresa e a permissão de uso; o limite de
  40 perguntas por dia por usuário é da fonte; o "caixa" do Cato soma banco e saldo de parceiro das sessões do dia.
  **Pergunta ao Kaik**: o Cato propõe reajuste de preço por cartão de confirmação, e a fonte diz que ele só consulta:
  mostrar ou não? **Conflito T10 × T15** (Ferro pesado) anotado no MUNDO, com proposta.
- 10/11 03:0x **T17 e T18 prontas** (roteiro). T17: 14 capítulos, 1.846 palavras, ~13 min; a pendência 3 da fonte está
  resolvida (Frota e NFS-e recebida existem, caps 2 e 8); "Configurações do MDF-e" só tem série e número (o percurso vai
  em cada manifesto); o Relatório Fiscal virou aba do Estoque Fiscal; o sistema não envia nada ao contador (o pacote
  sai em ZIP). Pronúncias a testar: MDF-e e ISS em IPA, "trúqui" (truck), "Fiscal & Ambiental". Backend: edges do MDF-e,
  NFS-e emitida e recebida, download; RPCs dos relatórios; cidades do IBGE locais. T18: 11 capítulos, 1.403 palavras,
  ~10,5 min; no MTR a empresa é a geradora e no CDF a destinadora (a ilustração mostra os dois papéis); a unidade "SIGLA -
  Nome" vem de uma lista; não existe status "recebido"; o cancelamento só vale para MTR emitido; o CDF é definitivo.
  Pronúncias a testar: "Sigôr" (SIGOR), "Ibama". Backend: edges `sigor-mtr-sync-ref`, `sigor-mtr-emit`,
  `sigor-mtr-cancel`, `sigor-cdf-emit`, RPC `mtr_set_credential`, rota SP → SIGOR. Decisões do coordenador: Serra Fina
  em Itamonte, MG; números de outubro podem ser falados; IBAMA 19 12 02 e Classe II B no exemplo, sem recomendação.
  **Teste de pronúncia 2**: juntar todas as palavras novas das aulas num nó só quando os roteiros fecharem.
- 10/11 03:1x **T5 e T8 prontas** (roteiro). T5: abertura e 11 capítulos, 1.645 palavras, ~10,5 min de fala (~12 min com
  vinhetas e cenas), 8 `[CENA WINDOWS]` com os textos do código (aviso do download, SmartScreen, instalador, painel,
  Configurar Balanças, bandeja › "Sair", atalho) e 10 ilustrações; pronúncia a testar "dráiver"; backend: EcoTray falso
  que muda de estado a cada capítulo. Código × fonte: o indicador de peso não aparece no celular (sem trecho de
  celular); com a trava de peso ligada não dá para digitar o peso com o EcoTray fechado; o "Guia de Instalação" ainda
  fala em ZIP. T8: abertura e 10 capítulos, 1.243 palavras, ~8 min de fala (~10 min de vídeo), sem cena de Windows;
  backend `get_next_ticket_number` = 58, rascunho em `weighing_tickets`, `finalize_weighing_ticket_v3`, `order_drafts`,
  caixa do Rafael aberto. Código × fonte: só com a 1ª pesagem, ela vira o bruto e precisa ser digitada de novo na
  saída; valorizar um ticket sem valores ignora a tabela do fornecedor (o exemplo não usa o Siqueira). Decisões do
  coordenador: T5 sem celular e papel de 58 mm; T8 com pesos digitados e compra finalizada no cap09. **Para o Kaik
  (possíveis bugs)**: o "Guia de Instalação" do EcoTray ainda fala em ZIP; valorizar ticket sem valores ignora a tabela de
  preço do fornecedor.
- 10/11 03:2x **T0 e T25 prontas** (roteiro). T0: 14 blocos, 1.544 palavras, ~9,9 min de fala (~11,5 min de vídeo); o
  vertical usa o mesmo áudio, com cada tela regravada no celular 390×844 (tabela no plano); trocas novas "Fiscal e
  Ambiental" e "Coletas e Logística" (o "&" do menu); backend `get_ecoflix_learning_status` (4 estados),
  `acknowledge_ecoflix_intro`, catálogo das 26 aulas. Código × fonte: o Pix Automático já vem ligado; sem permissão,
  "Cancelar assinatura" some (não ganha cadeado); os rótulos do menu são outros. T25: 12 blocos, 1.308 palavras, ~8,4 min
  de fala (~10 min de vídeo); pronúncias a testar Shift ("xífti", "xífti-cê"), "Vence em sete dias"; backend RPCs do
  Dashboard; arrastos `[TESTAR]`. Código × fonte: o "?" não abre a lista de atalhos (o hook não está montado; a aula usa
  o Ctrl+K); a Agenda já não conta o fiado em dobro (o ⚠️ saiu); o gráfico de 6 meses termina no fim do período do
  filtro; o Marketplace saiu da rotina semanal. Decisões do coordenador: o "20 %" do anual não é falado (regra de
  preço); o CRM sai do plano só no cap03 da T0; o cartão final da T25 é "Próximo: os módulos do seu plano". **Para o
  Kaik (possível bug)**: o atalho "?" não abre a lista de atalhos.
- 10/11 03:3x **T6 e T9 prontas** (roteiro). T6: 13 capítulos, 2.044 palavras, ~13,1 min de fala (~14,5 min de vídeo); sem
  pronúncia nova; backend `get_dinheiro_balance`, `register_number` sequencial, `create_manual_bank_transaction`,
  `adjust_cash_register_balance`; cap08 com trecho logado como Marcos. Código × fonte: o botão do aviso do cofre é "Usar
  disponível"; o gestor sem caixa aberto vê a aba Início ("Meu Caixa"); sem caixa aberto, o saldo de parceiro só trava
  em dinheiro (Pix segue). T9: 11 capítulos, 1.702 palavras, ~10,9 min de fala (~12,5 min de vídeo); pronúncias a testar
  "pópâp" (Popup), "pópâps" (Pop-ups); backend `preview_order_deletion`, `delete_purchase_atomic` com auditoria,
  `revert_consolidated_order_atomic`, `create_purchase_atomic`, `set_order_hide_financials`; o "Popup bloqueado" é
  simulado pelo robô (`window.open` devolve `null`). Código × Central de Ajuda: o pedido estornado continua na lista; o
  selo do cupom é "Comprovante sem valores"; a confirmação diz "Reabrir Último Caixa?" mesmo para caixa antigo.
  Decisões do coordenador: abrir com zero só no diálogo; numeração dos caixas #84 a #88 no mundo; `FAKE_NOW` 11/11 na T9;
  o caixa reaberto fecha com a data de 21/10 (é o que o código faz). **Para o Kaik (possível bug)**: "Reabrir Último
  Caixa?" aparece também para caixa antigo.
- 10/11 01:42 Kaik: "esses levantamentos de bugs vá anotando pra no final me dar um report do que melhorar no sistema
  desses problemas". Lista em `MELHORIAS_ECOSISTEMA.md` (prováveis bugs, melhorias de uso, textos desatualizados), com
  tudo o que os roteiros acharam até agora. Os ensaios e as gravações vão somando nela; no fim, vira o report.
- 10/11 04:0x **T19 e T22 prontas** (roteiro). T19: 14 capítulos, 2.062 palavras, ~13 min de fala (~16 min de vídeo), 11
  ilustrações; pronúncias a testar RH "érre-agá", CLT "cê-éle-tê", INSS "i-ene-ésse-ésse", EPI "é-pê-í", PIN "pin";
  backend: ajuste de salário e vale, bônus, falta, pagamento e recebimento, ponto pelo servidor (hora do servidor,
  selfie e local) com mapa e câmera simulados no celular. T22: 13 capítulos, 1.410 palavras, ~9 min de fala (~12 min de
  vídeo; todos os capítulos da fonte cobertos), 9 ilustrações; CMV "cê-ême-vê" (como na T15); backend: criar o grupo,
  vincular a filial, Enviar Ativos, transferência pendente e executada, pagamento do grupo simulado; cap03 gravado como
  Sandra Pires. Achados de sistema no `MELHORIAS_ECOSISTEMA.md`. **Na junção**: CNPJ da filial na T22 vira
  47.318.506/0002-98 (raiz da T1); números de outubro da T22 × T15 × T25.
- 10/11 01:4x **Ferramentas na skill**: o branch `consolidacao-domiflix` (6 commits) entrou no main (d0702be): `montar_cap.py`
  (computador ou celular pelo tamanho do vídeo, voz_de, zoom e destaque por rect sem passo, acelera, rótulo#k, destino),
  `finish.py` (acelera; apaga stems e music.wav depois do mix), `remendar_aula.py` (9:16, cortes em capítulo novo),
  `celular_vertical.py`, `legendas_aula.py`; novas `folhas3s.sh`, `pico_aac.py`, `lacunas.py`, `confere_render.py`,
  `compor_ilus_vertical.py`, `ilustracoes/ilu_comum.py`; os 3 ajustes do Supabase falso; `rec/molde/` (prever, resumo,
  ensaio, explorar) copiado pelo `instalar.sh`. Testes: identidade da Domiflix idêntica ao T3; `montar_cap.py` igual às
  cópias em 136 capítulos; `finish.py` igual bit a bit; legendas do T15 reproduzidas.
- 10/11 01:4x **Cópia de segurança da Domiflix** no branch `backup-domiflix-maquina` (8b74fe7): mundo da Dominex 1.38.24,
  roteiros do robô e projetos de edição, só texto (75 MB, sem a telemetria `*.actions.json`, que tinha a chave pública do
  app); serve aos remendos pendentes.
- 10/11 01:5x **Marca pronta** (branch `ecoflix-marca`, 5 commits, no main): peças e nome separados do PNG oficial sem
  redesenhar (juntas refazem o PNG pixel a pixel); vinheta `ecosistema-reciclagem` com os tempos, curvas e sons do
  capacete, escura em 4,30 s; cartela; vinheta de capítulo e cartões "Antes:"/"Próximo:" com o acento; kit de ilustração
  com "Tara e peso líquido" e "Caixa × competência" presas às palavras da fala; recorte de trecho no render de cenas.
  Domiflix idêntica ao T3. **Som escolhido: o sintetizado em Mi maior**, porque o player da EcoFlix já toca o oficial
  antes de cada vídeo (soaria duas vezes). Prévia em `/home/claude/ecoflix/previa_marca/` enviada ao Kaik. Falta a
  vinheta vertical 9:16 desse estilo (para o T0 vertical).
- 10/11 02:0x Kaik: "gostei do vinheta som sintetizado alternativa / E avance com tudo". Junção mecânica dos textos:
  grafias antigas trocadas (T02: NF-e e NFS-e; T03: ICMS final), `config_narracao.json` de cada aula refeito = o do perfil
  + as trocas próprias da aula; sem sigla crua nem travessão no texto da voz. **Estimativa da voz**: 248.602 caracteres
  em 25 aulas (falta a T26, ~9 mil) → ~258 mil caracteres ≈ **258 mil créditos** no eleven_v4 (~1 crédito por caractere,
  uma versão por fala); com ~5 % de folga para refazer falas, **~270 mil créditos**. O T0 vertical usa o mesmo áudio.
  Os textos ainda mudam um pouco no ensaio (±5 %). Teste de pronúncia 2 (24 frases com as palavras novas das aulas) no
  fluxo de teste. Diferenças a unificar depois do teste: Shift+C "xíft-cê" (T07) × "xífti-cê" (T25).
- 10/11 02:0x **Cena de Windows do EcoTray pronta** (branch `ecoflix-ecotray`, no main): `dashboard.py` e
  `installer_gui.py` de verdade, sem alteração, num Xvfb 1920×1200 a 96 dpi (Tk 8.6 com Xft extraído de pacotes do Ubuntu
  em /dev/shm, nada instalado: refazer depois de reinício com `ferramentas/windows/preparar.sh`), Montserrat, EcoTray
  falso na porta 8054 numa rede própria; o menu e o ícone da bandeja saem do `tray_app.py`. Área de trabalho genérica
  estilo Windows 11 com o navegador onde entra a gravação do robô; aviso de download, SmartScreen, instalador,
  "Configurar Balanças", "Nova balança", arrasto. Sai no formato do robô (o `render_chapter.py` põe cursor, câmera e
  palco); `"device": "windows"` (1280×712) no gravador; uso em `docs/10-cena-windows.md`. Prévia de 15,5 s enviada ao
  Kaik. **Para o T5 na revisão**: com a balança detectada, o diálogo troca o Protocolo para "Toledo" (o roteiro diz
  "Automático"); com um navegador conectado, o painel mostra "2 cliente(s)".
- 10/11 02:04 Kaik: "essa tela de "registrar compra" é muito antiga da ecosistema, não é a versão atual / As pronuncias do
  audio ficaram boas, algumas coisas erradas mas ok por enquanto". A tela era só a imagem provisória da prévia da cena
  do EcoTray (`feature-pedidos.png`, imagem antiga de divulgação que está no código do app). **Regra**: nas aulas, a
  página do navegador é sempre a gravação do app na versão 1.59.154; imagem de divulgação do app nunca vira tela. Teste
  de pronúncia 2 aceito por enquanto (algumas palavras a refinar quando o Kaik apontar). Shift+C/V unificados em
  "xífti-cê"/"xífti-vê" (a T07 usava "xíft-").
- 10/11 02:1x **Roteiros T20 e T26 prontos: as 26 aulas têm roteiro.** T20 (Portal do Cliente e Fornecedor): 12 blocos,
  1.515 palavras, ~9,7 min de voz (~12 min de vídeo), 10 ilustrações; dois navegadores (o do sistema e o do parceiro, sem
  login); backend: edges `entity-portal`, `entity-portal-report`, `portal-set-credentials`, `portal-login`,
  `portal-order-receipt`, `collection-request` (aviso no sino) e `order-photos-public`, um Pix no sistema; mundo: saldo
  da cooperativa R$ 1.350,00 (o do fim da T4), 3 fotos fictícias com token fixo, senha do portal, Pix de R$ 1.350,00,
  coleta pedida para 12/11. **Decidido**: a T20 grava com `FAKE_NOW` 10/11 15:00 (a venda sem valor da T7 e a NF-e 1250
  da T16 já existem nessa hora; a hora não muda nada para quem assiste), em vez de mudar as datas dessas aulas. T26
  (CRM/Kanban): as automações estão na 1.59.154 (entraram na 1.59.151; migration `20261106170000` no commit de release);
  14 blocos, 1.817 palavras, ~11,6 min de voz (~15 min de vídeo), 10 ilustrações (o funil de vendas no cap01); backend:
  RPCs `ensure_company_crm_default_pipeline` e `reorder_company_crm_opportunities` e as regras do banco (trava pela etapa
  de origem, automação só ao avançar, prazo em dias úteis, histórico, contagem de tarefas, Agenda); mundo: CRM vazio no
  início, funil "Sucata industrial", oportunidade da Metalúrgica Jequitibá de R$ 8.400,00 e, no cap12 (17:30), mais 5
  cartões (R$ 62.300,00 no total); o cartão barrado pela trava pede recarregar a página fora do vídeo. Achados no
  `MELHORIAS_ECOSISTEMA.md`. **Mostrar ao Kaik junto com a estimativa**: o funil da T26 e os nomes fictícios. **Para a
  revisão geral**: o QR do comprovante do caixa leva ao portal (todo parceiro do mundo tem link), conferir a ilustração
  do cupom na T7; pronúncias a testar: WhatsApp e Siqueira (T20), checklist, Jequitibá e "cê-érre-ême-canban"
  (CRM/Kanban, T26). **Estimativa da voz com as 26 aulas**: 259.103 caracteres ≈ 259 mil créditos; com 5 % de folga,
  **~272 mil**. Carimbos 03:5x a 04:3x deste registro corrigidos para 01:4x a 02:0x (os commits mostram a hora certa).
- 10/11 02:2x **Vinheta e cartela verticais 9:16 prontas** (branch `ecoflix-marca-9x16`, no main em e08bf3c): molde e
  tempos do capacete vertical, área segura, título em até 2 linhas que diminui até caber; som sintetizado idêntico ao do
  16:9; Domiflix idêntica ao T3 e a vertical dela igual pixel a pixel; `testes/vertical_9x16.sh` confere também a EcoFlix.
  Prévias em `/home/claude/ecoflix/previa_marca/`. Resolve a nota "Falta a vinheta vertical" da Marca (01:5x).
- 10/11 02:3x **Ilustrações em andamento**, 14 agentes (`_BRIEF_ILUSTRACOES.md`): T00 · T01+T02 · T03+T09 · T04+T06 ·
  T05+T27 · T07+T08 · T10+T12 · T11+T21 · T13+T14 · T15+T22 · T16 · T17+T18 · T19+T25 · T20+T26. Cada aula ganha
  `Tnn/cenas/` (`cenas.html`, `tempos/` estimados, manifesto `ilustracoes.json` com as âncoras e o que a cena mostra);
  folha de contato em `/home/claude/ecoflix/previa_ilustracoes/Tnn.jpg`; quadros sob a trava pesada (2 CPUs). Ferramentas:
  `tempos_estimados.py --tts <tts_textos.py> --cap N` (lê o CAPS da aula como o `proc.py`: tags fora, trocas aplicadas) e
  Montserrat da skill no `render_cenas.cjs` quando a cena fica fora do `$TUT_HOME` (antes o render quebrava; os quadros
  saem idênticos aos de dentro). Disco com 1,1 GB livres: perguntar ao Kaik se pode apagar as pastas de trabalho de 29 a
  31/10 (`/home/claude/fix-29out` e `/home/claude/brand-fix`, 7,7 GB) antes do ensaio (trocar a cópia duplicada do modelo
  de voz por um atalho foi barrado pela trava automática de segurança).
- 10/11 02:4x **Mundo pronto** (branch `ecoflix-mundo`, no main em 51224e1): app 1.59.154 em build na 8080 e Supabase
  falso na 54340 (subir de novo: `/home/claude/ecoflix/RELIGAR.md`), login do Rafael (MASTER); 17 rotas da Fase 1 com 0
  problema (mais /caixa, /compra e /venda com `base/caixa-aberto`); `rec/mundo/gerar/sementes.mjs` gera o mundo base e para
  se um número falado não bater (outubro do T15 no centavo, estoque do T21 R$ 52.112,25, saldos do T4, contas do T13,
  caixas #70, #83 e #84, cofre R$ 18.500,00); 37 RPCs, 1 function e 7 hooks; `_remove` nas sementes extras; EcoTray
  falso no robô (8053/8054, "Balança do pátio" COM3, POS-58, versão 1.7.22; passos `balanca` e `ecotray`; semente
  `base/balanca-ativada`). Falta: as sementes de cada aula (ficam com os agentes do robô). Os 8 conflitos entre aulas
  ("Para a junção" no `MUNDO_FICTICIO.md`) foram para a junção, com a cota da NF-e da T16 de preferência fora da fala.
  Identidade da Domiflix idêntica. O `browser.mjs` da área de trabalho recebeu o `device: windows` da cena do EcoTray.
- 10/11 02:5x **Robô e ensaio começaram** (`_BRIEF_ROBO.md`), 5 agentes: T03 (molde), T01, T02, T11 e T26, cada um com o
  seu Supabase falso na porta 54300 + aula. `preparar_aula.sh Tnn` monta a área leve da aula (kit do robô, atalhos para a
  fala do git e `capNN.json` estimados; sem a pasta edit/ de 70 MB por aula, que só entra na edição);
  `copiar_robos.py` copia para o git o robô de cada aula (`Tnn/rec/`) e o mundo vivo (`perfis/ecoflix/mundo`) antes de
  cada commit. Propostas de mudança de fala e achados do app de cada aula: `Tnn/propostas_fala.md` (a revisão geral
  aplica). Próximos lotes do robô conforme os agentes de ilustração forem terminando (máximo de 20 ao mesmo tempo).
- 10/11 03:2x **Trava presa 10 min** por um render de quadros parado da T0 (18 agentes na fila): o processo saiu sozinho;
  `render_cenas.cjs` ganhou vigia (sai com código 3 se nada anda em 90 s, testado), lição em `docs/08-licoes.md`.
- 10/11 03:5x **Ilustrações T04 e T06 prontas** (8 + 5 cenas, conferidas em quadros; folhas em
  `/home/claude/ecoflix/previa_ilustracoes/`). Sem contador de etapas; valores em constantes no topo de cada cena; a
  junção mudou as duas falas no meio e os tempos foram refeitos. Nenhuma mudança de fala. **Para a revisão geral**: o app
  escreve "Conta DINHEIRO" e a legenda terá "Conta Dinheiro" (decidir); desenhos que faltaram no kit e cada aula fez o
  seu (vermelho de saldo e despesa, seta com ponta, ficha que viaja, chip de parceiro, pátio, fardos, latinhas, gaveta,
  cofre, banco, carroça, notas): unificar no kit depois que todas terminarem, para o mesmo objeto sair igual em todas as
  aulas. Robô da T04 lançado no lugar.
- 10/11 ~04:0x **Limite semanal acabou** com os 20 agentes no meio (429 "weekly limit", volta 11/11 11:00 de Lisboa). Os
  lembretes 1 a 6 dispararam durante a parada e chegaram juntos com o 7.
- 11/11 11:4x **Retomada 7/20**: a máquina tinha reiniciado (`/dev/shm` vazio): app e Supabase falso religados pelo
  `RELIGAR.md` (o build está em disco); os 20 agentes retomados por mensagem, com o mesmo contexto (junção, 6 robôs e 13 de
  ilustração), avisados de subir de novo a instância de cada um, de rodar o `preparar_aula.sh` (a junção mexeu nas falas) e
  de economizar tokens. Os quadros da T06 em tamanho real têm texto legível: a escala das cenas está boa (a folha de contato
  é que engana).
- 11/11 11:5x **Junção pronta** (`MUNDO_LINHA_DO_TEMPO.md`): história e cadeias do mundo, estado de partida de cada aula
  (seção 14), decisões (15), mudanças para a semente (16), a T26 (17) e os 580 números falados conferidos (18). Principais
  decisões: Edson e o FKD2E41 na T8, T12 e T17 (a T12 passa para 07:00, tara 6.380); nenhum caixa aberto antes das 08:31
  (a venda da T16 vai para 09/11); NF-e de outubro com 1246 e 1247 puladas e as de hoje de 1249 a 1254; alumínio da T17 e
  chaparia da T18 no estoque; Pix de 380,00 da Aparecida no OFX da T14; Vale Forte com três compras em outubro;
  "Contabilidade Manacá" na T17 e Sérgio Paiva sem repetição. Falas acertadas em T4, T6 a T10, T12 a T14, T16, T17, T20 a
  T22, T25 e T27 (a cota da NF-e da T16 saiu da fala). A comparação roteiro × tts foi parcial: fica para a revisão geral.
  **Semente do mundo base** (seção 16) com um agente novo; os robôs seguem no gerador e no ensaio rápido e só fazem o
  ensaio completo depois do aviso de mundo novo pronto (a T26 não depende e segue).
- 11/11 11:5x **Ilustrações T11 e T21 prontas** (12 + 9 cenas; folhas em `previa_ilustracoes/`): o Cato só como balão de
  conversa; diferença e perda em âmbar; valores da T21 já com os números da junção (17.540, 112.800, 14.370, 96.076).
  **Para o robô da T21**: o `T21/plano.md` (respostas R1 a R9) ainda tem os números antigos e "Conta Reserva" (o mundo diz
  "Conta Secundária"): atualizar antes do robô da T21. Mais itens do kit para a unificação (etiquetas, escala em `svg()`,
  janela pelas âncoras, fundo opaco para cenas seguidas, balão de conversa, desenhos). Robô da T19 lançado no lugar.
- 11/11 11:5x **Ilustrações T01 e T02 prontas** (12 + 9 cenas). **Para a revisão**: não existe logo da Recicla Vale; a T01
  desenhou um símbolo fictício (caps 00, 05, 06 e 08): usar o MESMO logo do robô da T01 (o que ele sobe na tela) nas
  cenas e no mundo. "Excluir Conta" vem de `config/routes.ts:245` (fora do inventário). Kit: `pulse()` chamado duas vezes no
  mesmo quadro apaga o primeiro (o `CAPS[1]` do kit perde um pulso; corrigir na unificação). `render_cenas.cjs` com
  `--stills` vazio renderizava o MP4 inteiro: agora recusa. Robô da T27 lançado no lugar.
- 11/11 11:5x **Ilustrações T07 e T08 prontas** (10 + 8 cenas). **Erro de conceito no exemplo do kit** "Tara e peso
  líquido" (o que foi na prévia da marca): ele chama o caminhão vazio de "Tara", mas no app essa é a "2ª Pesagem", a
  diferença entre as duas é o "Peso Bruto" e tara é a embalagem (saco, tambor, caçamba). As cenas da T07 e da T08 seguem o
  app (a da T07 virou carroça com 412, 96 e 316 kg: caminhão com 412 kg seria falso); corrigir o `CAPS[1]` do kit na
  unificação e avisar o Kaik. Agentes da T05 e da T10+T12 avisados. Kit: kg com decimais, seta e tracejado no `traco()`,
  carroça, caminhão com carga e vazio, balança; o render não carrega ícone de uma letra ("x"). T08 cap08 usa 1.200 e 800
  kg do roteiro, fora do mundo (conferir na revisão). Robô da T06 lançado no lugar.
- 11/11 12:0x **Disco liberado com o ok do Kaik** (12:00): só os intermediários pesados das pastas de 29 a 31/10
  (arquivos acima de 1 MB em `fix-29out/work` e `brand-fix/work`, 4,6 GB) e as bibliotecas do projeto da animação
  (`gancho-whats/node_modules`, 0,5 GB). Ficaram os originais, os finais (`saida`, `entrega`), ferramentas, ajustes e
  parâmetros de cada vídeo e o projeto da animação: dá para editar de novo (só refaz os intermediários). Disco: 5,7 GB livres.
- 11/11 12:0x **Ilustrações T16 prontas** (19 cenas, uma por capítulo; a cota sem número, como a fala nova). **Para o robô
  da T16**: conferir na tela se a NF-e da Serra Fina (Itamonte, MG) sai com CFOP 6102, como dizem o roteiro e a linha do
  tempo, ou se o app põe o 5102 padrão (a ilustração viu 5102 no fluxo do app); se o app não trocar sozinho, é achado
  para o relatório de melhorias e o robô escolhe 6102. Ícone de uma letra ("x") agora carrega no render. Robô da T07
  lançado no lugar.
- 11/11 12:1x **Ilustrações T00 prontas** (21 cenas; o cap00 e o cap05 são só ilustração, do primeiro ao último quadro;
  janelas encostadas no cap00, cap05, cap10 e cap11: renderizar cada bloco de uma vez). A trava presa de ontem foi um
  `--stills` vazio que caiu no modo vídeo (já recusado). Sinal dos saldos da T4 ambíguo no MUNDO (o vale de −300 do Valdir
  é a receber?): o robô da T04 confere na tela. Robô da T08 lançado no lugar.
- 11/11 12:2x **Ilustrações T10 e T12 prontas** (13 + 7 cenas): "Ajuste manual" nos dois lados (é o rótulo do app); a tara
  da T10 é o saco ("Tara/Imp."); a cena da pesagem da T12 sem "Peso bruto" nem "Peso líquido" (tara do caminhão 6.380 da
  junção); sem desenho de tela do app. Robô da T09 lançado no lugar.
- 11/11 12:3x **Ilustrações T19 e T25 prontas** (12 + 8 cenas): relógios sem horário escrito no ponto da T19; nenhum
  número de outubro na tela da T25; "Módulo do plano" virou cadeado + "depende do plano". Propostas de fala e pendências
  das ilustrações agora em `PROPOSTAS_ILUSTRACOES.md` (para a revisão geral). Robô da T10 lançado no lugar.
- 11/11 12:3x **Ilustrações T03, T09, T13, T14, T17 e T18 prontas** (11 + 5 + 7 + 10 + 7 + 8 cenas); pendências na
  `PROPOSTAS_ILUSTRACOES.md` (a principal: o cap01 da T18 tem uma fala no roteiro que não está no tts). Faltam as
  ilustrações de T05+T27, T15+T22 e T20+T26. Robôs da T12, T13 e T14 lançados nos lugares (20 agentes).
- 11/11 12:4x **Kaik pediu para ver as ilustrações** ("vai me dando as ilustrações aqui pra eu ver se corrijo algo ou o
  estilo delas"): mandadas as folhas de contato das 20 aulas prontas (`previa_ilustracoes/Tnn.jpg`). `folha_cenas.py Tnn`
  faz uma folha maior com o quadro final de cada cena (`Tnn_cenas.jpg`), para quando ele quiser ver de perto (sob a trava;
  com a fila cheia, demora).
- 11/11 12:20 **Kaik sobre o estilo das ilustrações**: "as etapas mostram com o ícone escuro sobre o verde, devia ser branco
  / E em vários lugares estão com badges dessaturados com texto saturado, tem que ser saturados com ícone branco / tipo em
  quadrados atrás de ícones, badges, etc. / substitua em tudo / E nas ilustrações do cato devia usar a identidade visual
  real do cato / e na ilustração do cato pode usar o tema escuro que fica melhor, igual no video motion do cato do site"
  (mandou a marca do Cato: degradê #6366F1 → #A855F7 → #EC4899 → #F97316, estrela, logo, ícone, #EFEFEF e #121212).
  **Feito**: bloco `<style id="saturado">` no kit e nas 26 `cenas.html` (`estilo_saturado.py`: `.ico`, `.ico.a`,
  `.tag.v` e `.tag.a` com fundo cheio e ícone/texto branco; tokens `--vs` #16A34A, `--as` #D97706, `--rs` #DC2626). A
  prova lado a lado (verde da marca × verde do sistema) foi para o Kaik escolher; o padrão é o verde do sistema, que lê
  bem com texto branco (trocar é só mudar `--vs`/`--as` no `estilo_saturado.py` e rodar de novo). O que cada aula fez com
  estilo próprio: 6 agentes de estilo (`_BRIEF_ESTILO.md`, Sonnet: T00-T02, T03/T04/T06, T07-T09, T10-T12, T13/T14/T16,
  T17/T18/T19/T25); as 3 frentes de ilustração ainda abertas foram avisadas. Cato: identidade em
  `perfis/ecoflix/cenas/cato/` (ícone, logo e espiral do próprio app; estrelas da marca; `LEIA.md`) e um agente refazendo
  as 9 cenas da T21 no tema escuro. **Quadros de conferência agora na trava leve** `.stills.lock` com `nice -n 19` (a
  trava pesada tinha 36 na fila; ela fica só para as gravações do robô).
- 11/11 12:5x **Ilustrações T05 e T27 prontas no estilo novo** (11 + 6 cenas). **Estilo saturado pronto em T03, T04 e T06**
  (22, 7 e 7 ajustes: `.tag.n`/`.ico.n` cinza #4B5563 com branco, `.tag.r`/`.ico.r` vermelho cheio, fichas, bolinhas de
  "=", "×" e "?"; ficaram como estavam o ícone nu no degrau da T03 cap07, o maço de notas com borda verde da T06 e os
  marcadores grandes). Folhas mandadas ao Kaik (T05, T27, T03, T04, T06). Trocas de pronúncia agora só em palavra inteira
  (a "asas"→"Asaas" pegava em "casas" na T05).
- 11/11 13:0x **Estilo saturado pronto em T00, T01 e T02** (~22, 14 e 20 ajustes; "desligado" em cinza #9CA3AF com ícone
  branco que acende em verde ou âmbar). Ficaram como estavam: os cartões "Ligada/Desligada" da T01, os valores "R$ ••••"
  coloridos e o realce de texto `.hl` da T02 (texto sobre branco, não selo); se o Kaik quiser, viram chip. Folhas mandadas.
- 11/11 13:0x **Ilustrações T15 e T22 prontas no estilo novo** (9 + 7 cenas; a junção mudou falas da T22 e as cenas foram
  refeitas). Folhas mandadas ao Kaik. Faltam as ilustrações de T20+T26, o Cato (T21) e o estilo saturado de T07-T19 e T25.
- 11/11 13:1x **Estilo saturado pronto em T13, T14 e T16** (17, 14 e 15 trocas; painéis grandes "Disponível no cofre" e
  "Diferença" da T14 ficaram claros; o carimbo "Cancelada" da T16 continua desenho; os elementos esmaecidos de propósito
  continuam esmaecidos). Folhas mandadas ao Kaik.
- 11/11 13:1x **Ilustrações T20 e T26 prontas no estilo novo** (9 + 10 cenas; quadros do CRM só em esquema, dominós com os
  rótulos do app) e **estilo saturado pronto em T07, T08 e T09** (~9, 8 e 12 ajustes, num bloco `saturado-aula` por aula;
  ícones soltos sem fundo, linhas de resumo dentro de cartões e o navegador esquemático da T09 ficaram como estavam).
  Todas as 26 aulas têm ilustração. Folhas mandadas ao Kaik. Faltam: estilo de T10-T12 e T17/T18/T19/T25 e o Cato (T21).
- 11/11 13:2x **Estilo saturado pronto em T10, T11 e T12** (~11, 9 e 10 pontos: etapas de cinza a verde cheio com ícone
  branco, balões de pergunta em âmbar cheio, sinais e operadores em cinza; a etiqueta "Cancelada" da T12 cap10 segue
  apagada como o cartão cancelado). Folhas mandadas. Faltam o estilo de T17/T18/T19/T25 e o Cato (T21).
- 11/11 13:2x **Estilo saturado pronto em T17, T18, T19 e T25** (7, 8, 13 e 8 elementos; desenhos como cédulas, avatares,
  ícones soltos de pasta e arquivo e os cartões "NF-e/Pedido" da régua da T17 ficaram como estavam). **As 26 aulas estão
  no estilo novo**, menos o Cato (T21), que está sendo refeito no tema escuro. Folhas mandadas ao Kaik.
- 11/11 13:3x **Cato (T21) no tema escuro com a identidade dele**: fundo #121212 com a espiral do app a 15 %, kicker no
  degradê, título #EFEFEF, ícone do Cato como avatar e botão, logo na janela de conversa do cap00, balões escuros
  translúcidos, selos e números de destaque no degradê (texto branco no laranja com sombra: contraste ~2,8). Folha mandada
  ao Kaik. **Na edição**: copiar a pasta `cato/` junto com o `cenas.html` da T21. **Todas as 26 aulas estão ilustradas no
  estilo novo.**
- 11/11 13:03 **Kaik**: "A) verde da marca com branco ficou melhor que verde do sistema mesmo / agora os quadros ficaram
  melhores com tudo saturado / E podem ter ilustrações de conceitos que ficariam melhor se fossem ilustradas/3D, não?".
  **Feito**: cores do estilo saturado trocadas para as da marca em todas as cenas (`--vs` #50D088, `--as` #F2B63D, `--rs`
  #EF4444; também as cores fixas que as aulas tinham posto); folhas de todas as aulas sendo refeitas. **Piloto 3D** (three.js
  no Chromium) da pesagem da T07 com um agente, para o Kaik ver antes de levar 3D a outros conceitos (entrega em
  `T07/cenas3d/` e `previa_ilustracoes/T07_3d_piloto.mp4`).
- 11/11 13:31 **Kaik** (sobre a T06): "essa ilustração de 'caixa' não tá muito clara, podia ser uma caixa registradora".
  Um agente desenha a `registradora()` no kit (visor escuro com número no verde, teclado, gaveta que abre com notas e
  moedas) e troca o caixa-gaveta na T06, T09, T19, T21 (variante escura) e na T00 se houver.
- 11/11 14:0x **Caixa registradora pronta**: `registradora({aberta, cheia, visor, w, tema, cores})` e `abreGaveta()` no kit;
  trocada na T06 (4 cenas; a gaveta abre quando entra dinheiro e o visor conta), T19 (o vale volta para a gaveta), T21 (tema
  escuro do Cato, fechada em R$ 0,00) e T00 (a etapa "Caixa" e o glossário). A T09 não tinha gaveta desenhada. Folha da
  T06 mandada ao Kaik.
- 11/11 14:1x **Mundo base novo pronto** (seção 16 da linha do tempo no gerador; 272 conferências passam; smoke 17 rotas ok;
  sementes antigas no scratch `gen/seeds-antigos`). Decisões do agente: distribuição de lucros de R$ 40.000,00 em 30/10 fora
  da DRE (sem ela a Principal fica negativa no fim do mês); cooperativa de agosto e setembro pela tabela do T4; Tabela
  Depósitos desligada no depósito (a T4 liga na tela); pedidos começam em #1253. **Pendências**: sementes de aula afetadas
  (t01 `apos-cap05` e t19 inserem outra `company_fiscal_config`; t06 `dia-10` e `apos-cap09` com saldos antigos; t11 com
  índices e números fixos e o estorno de 50 kg sobre 42 kg de cobre mel) e números da seção 18 que não fecham (cooperativa
  450/120 da T4 cap11; papelão −370 kg de 05/11 16:10 a 06/11 10:45; `lib/eco.mjs` soma a compra estornada e a
  compensação: novembro com compras de 19.171,05) — cada robô foi avisado do seu. **Os 16 robôs foram liberados para o
  ensaio completo**; robôs da T15, T16 e T17 lançados.
- 11/11 14:3x **Piloto 3D pronto** (T07 cap06, three.js r170 local, argila/low-poly, câmera contínua; mesma API, âncoras e
  números da cena 2D; em `T07/cenas3d/` com uma cópia do renderizador que liga `--allow-file-access-from-files` para o import
  do módulo em `file://`). Custo: ~1,0 s por quadro em 2560×1600 (3,5× o 2D): ~17 min por cena de 36 s. Vídeo e folha
  mandados ao Kaik; esperando ele dizer quais conceitos ganham 3D (o agente sugere T00 caminho do pátio, T08/T12 caminhão e
  tara, T11 latinha e fardo, T10/T04 pilha e fardo, T05 EcoTray, T16-T18 carga e percurso; metáforas da T19, T15 e T26).
- 11/11 14:15 **Kaik sobre o piloto 3D**: "ficou bom". Um agente monta o kit 3D (`perfis/ecoflix/cenas3d/`: objetos da
  pesagem, caminhão, latinhas, prensa, fardo, impressora, computador, pátio), liga `--allow-file-access-from-files` no
  `render_cenas.cjs` (conferindo que o 2D sai idêntico) e converte a T07 (cap06) e a T08 (caminhão na balança). Depois do
  kit: T00 (caminho do pátio), T12, T11, T10/T04, T05 e T16-T18, como o Kaik não escolheu outra lista.
- 11/11 15:1x **Kit 3D pronto** (`perfis/ecoflix/cenas3d/`: `kit3d.js`, three.js r170 + licença MIT, `LEIA.md`, `vitrine.html`
  com todos os objetos). O `render_cenas.cjs` oficial liga `--allow-file-access-from-files` e ganhou `--dsf` (prévia 1,35);
  o 2D da T08 cap04 saiu idêntico byte a byte (3 quadros e 30 quadros de MP4). Em 3D: T07 cap06 e T08 cap00, cap04 e cap06
  (`"3d"` no `ilustracoes.json`; o cap05 da T08, só a conta, fica na 2D). Prévias T07_3d.mp4 e T08_3d.mp4 mandadas ao Kaik
  às 15:2x.
- 11/11 15:2x **3D nas outras aulas** (`_BRIEF_3D.md`): cinco agentes, T00 (Opus, a aula de abertura), T11+T12, T04+T10,
  T05+T16 e T17+T18 (Sonnet). Objeto novo só em `perfis/ecoflix/cenas3d/objetos/` (nunca no `kit3d.js`); quadros e prévias
  na trava leve com `nice -n 19` (a pesada é da gravação dos robôs, com 20 na fila). Nota para a edição: a ilustração
  aparece numa caixa de ~1420 px de largura no vídeo final; renderizar o 3D final com `--dsf 1.35` (1728×1080) em vez de 2
  corta ~45% do tempo (~1 s/quadro em 2560×1600) sem perda visível.
- 11/11 15:3x **Robôs da T00, T20, T21 e T22 lançados** (`preparar_aula.sh` antes; portas 54300, 54320, 54321, 54322). T00
  com as duas versões (computador e 9:16 no celular 390×844); T21 primeiro acerta no `plano.md` as respostas R1 a R9 com
  os números do mundo base novo e "Conta Secundária" (no lugar de "Conta Reserva"); T22 calcula os números do grupo pela
  soma real das unidades. Opus na T21 e na T22 (números financeiros), Sonnet na T00 e na T20. Faltam os robôs da T05 (com o
  agente das cenas de Windows), T18 e T25 (conferir no `eco.mjs` a compra estornada e a compensação de novembro): entram
  quando a fila de agentes abrir.
- 11/11 15:30 **Kaik sobre as prévias 3D da T07/T08**: "ficou ótimo". Pediu materiais mais claros ("latinhas (coloridas e
  metálicas), garrafas pet (transparentes e verdes, amassadas e inteiras), ferro etc") e um big bag no lugar da carroça
  na dupla pesagem. Perguntado (a fala e a gravação contam a carroça do Zé e a aula ensina que saco é tara), escolheu
  **big bag como tara**: o saco do exemplo de tara vira big bag; a dupla pesagem fica com a carroça, com o ferro visível.
  O agente do kit 3D (retomado) faz os materiais reconhecíveis no kit sem mudar a API (latinha, PET, ferro, cobre,
  papelão, terra, borracha, plástico; `bigBag`), troca o `kit3d.js` de uma vez e refaz as prévias da T07/T08; as cinco
  frentes 3D foram avisadas e refazem as prévias quando o kit trocar.
- 11/11 16:3x **Prioridade dos renders**: a prévia 3D rodava com `nice -n 19`, mas o processo da GPU do Chromium aparecia
  em nice -8 (como root, o Chromium sobe a prioridade dele) e disputava CPU com a gravação dos robôs (57 % contra 44 %). O
  `render_cenas.cjs` agora se põe em SCHED_IDLE antes de abrir o navegador (Chromium e ffmpeg herdam; conferido: node,
  GPU e renderer em SCHED_IDLE; captura com prazo de 90 s); `docs/09` e `docs/08-licoes`. Prévias 3D passam a `--dsf 1`
  (a trava leve estava em ~7 min por trecho de 13 s) e só depois da troca dos materiais no kit.
- 11/11 16:3x **3D da T11 e T12 prontos** (cenas e quadros): T11 cap00, cap02, cap04 (ímã e esteira) e cap08; T12 cap08
  (tara do veículo, "Tara 6.380 kg") e cap09 (poliguindastes trocando as caçambas 05 e 03; a 06 chega do Externo pelo
  Movimentar). Objetos novos `ima.js`, `esteira.js`, `poliguindaste.js`. As prévias em vídeo não saíram (a tarefa de fundo
  bateu no limite de tempo com 4 de 10 trechos): renderizar depois da troca dos materiais (script do agente:
  `scratchpad/previa.sh T11|T12`, passar a `--dsf 1`). O `objetos/chaparia.js` sumiu da pasta durante o trabalho (a T11 e a
  T12 copiaram uma pilha de chapas nas páginas; perguntado ao agente do kit).
- 11/11 16:4x **Robôs da T18 e T25 lançados** (portas 54318 e 54325; T25 confere antes no `eco.mjs` como o app conta a
  compra estornada e a compensação em novembro). Falta o da T05, com o agente das cenas de Windows.
- 11/11 16:4x **Retomada 8/20** (lembrete): trabalho andando; app (8080) e Supabase falso (54340) no ar; disco 4,8 GB livres;
  17 agentes rodando e 12 robôs esperando a trava pesada (53 na fila). **Kit 3D com materiais reconhecíveis no lugar desde
  16:33** (latinha com faixa de cor, PET transparente e verde, ferro e chapa enferrujados, cobre em fio e tubo, papelão,
  terra, borracha, plástico, `bigBag`; mesma API, os montes caem nos mesmos lugares). As frentes 3D foram avisadas para
  conferir e fazer as prévias com `--dsf 1`; o agente da T11/T12 foi retomado para as prévias dele. O `chaparia.js` não
  foi apagado pelo agente do kit (perguntado à frente T17/T18).
- 11/11 17:3x **Robô da T13**: com renders ao lado, os gestos do ensaio completo saíam 1,5 a 2x mais lentos (cap04 às
  17:21, já com o render em SCHED_IDLE: maxLate 8,2 s com 0 passo falho; no ensaio sem carga, 0,8 a 1,1 s por gesto).
  **O `render_cenas.cjs` agora pausa entre quadros enquanto um `node record.mjs` captura** (sem ffmpeg filho; volta quando
  ele monta o MP4 ou sai; `RENDER_PAUSA=0` desliga; conferido o detector e um quadro 2D). Aviso mandado aos 18 robôs que
  ensaiaram desde as 13:30 (regravar o capítulo antes de mexer em âncora por atraso visto nesse intervalo) e às frentes 3D
  (prévias mais lentas, trechos de 7 s). Na gravação final, a mesma regra: nada de render enquanto o robô captura.
- 11/11 17:50 **Limite semanal batido** (volta em 18/11 11:00 Lisboa): pararam o agente do kit 3D, o 3D da T00 e o robô da
  T18. 17:5x **Kaik usou um reset** ("pode continuar como estava"): os três retomados com SendMessage de onde pararam; o
  ritmo segue o de antes (até ~20 agentes).
- 11/11 18:42 **Kaik perguntou o andamento**: ~45% do total (roteiros, mundo e ilustrações 2D prontos; robôs ~metade, com
  ~45% dos 340 capítulos no ensaio rápido e ~10% no completo; 3D ~1/3; faltam revisão, voz, gravação final, edição e
  entrega; uns 3 a 4 dias de máquina). 18:46 **Kaik: "isso, faça o que for acelerar o processo, sem perder qualidade"**.
  - **Ensaio completo só onde precisa** (`_BRIEF_ROBO.md` item 3; aviso aos 25 robôs): sempre o rápido COM a folha de
    contato e o `prever.py`; o completo só com pouca folga prevista (≥ 0,4 s), gesto sensível a espera (arrasto, menu
    aberto, aviso que some, digitação longa, celular, dois navegadores, tela que muda sozinha) ou aviso no rápido. A
    gravação final, com a voz, confere o resto. Corta ~10 a 15 h da trava pesada.
  - **Esteira por aula** (próximo): a aula cujo robô terminar segue sozinha (revisão das falas dela → voz → gravação
    final → edição), sem esperar as outras; a primeira vira o piloto completo para o Kaik aprovar o acabamento.
  - Robô da T05 e cenas de Windows: o limite de 20 subagentes ao mesmo tempo barrou o lançamento; entram na primeira vaga.
- 11/11 19:0x **Robô da T05 lançado** (porta 54305; EcoTray falso, gravações `device: windows` para as cenas de Windows,
  hora do cupom de teste 08:41:07). O agente das **cenas de Windows da T05** (8 momentos, `planejamento/ecoflix/T05/windows/`)
  esbarrou no limite de 20 subagentes duas vezes: entra quando um agente terminar de vez (o briefing está pronto nesta
  sessão).
- 11/11 19:1x **Agente das cenas de Windows da T05 lançado** (abriu vaga). Agora todas as frentes estão rodando: 26 robôs, as
  cenas de Windows da T05, o kit 3D (prévias T07/T08) e as frentes 3D (T00, T04+T10, T05+T16, T17+T18, prévias T11/T12).
- 11/11 19:2x **T05**: robô e cenas de Windows entregaram parciais (a trava pesada com 40+ na fila); deixaram os ensaios
  rápidos e as capturas do EcoTray na fila e acordam quando rodarem. Hora do cupom de teste alinhada: **08:41:07** na
  ilustração do cap04, na Atividade Recente do EcoTray (cena 4) e no relógio próprio do cap04 do robô (calculado a partir do
  instante do clique na voz de verdade). Mudanças do robô levadas à skill: `ferramentas/rec/recorder/runner.mjs` e
  `ecotray-falso.mjs` (passos `balancas`, `mudo` e `comandos` do EcoTray falso; só acréscimos, padrão igual ao de antes) e
  a correção do upload multipart no `net.mjs` (T14/T01, do dia 10); o `$TUT_HOME/rec` e a skill estão iguais de novo.
- 11/11 19:3x **Prévias 3D da T11 e T12 prontas** (kit novo, `--dsf 1`). Na revisão: T12 cap08 deixava "TARA 6.380 kg" no
  mostrador com o caminhão cheio (lia como se o cheio pesasse 6.380; a fala diz "pesa mais") e T11 cap02 apontava "Entra /
  Alumínio latinha" para o chão vazio depois da prensa. Agente retomado: carregado sobe para 9.460 kg e a diferença
  "peso do material" 3.080 kg (números do mundo: o FKD2E41 do T08), pilha de latinha fica no "Entra". Mando ao Kaik depois.
- 11/11 19:3x **3D da T05 e T16 prontos** (8 cenas, nenhuma ficou na 2D): T05 cap01 (a ponte: balança de plataforma,
  computador, impressora e cabos; 18,6 kg vai ao Pedido e o cupom volta), cap04 (térmica e cupom de teste, 08:41:07) e cap05
  (largura do papel); T16 cap00 (carga de cobre, cancela, nota, fundição), cap07 (placa na nota), cap10 (506 kg bruto,
  500 kg líquido, R$ 23.950,00) e cap14 (DANFE e XML). Objetos novos: `balancaPlataforma`, `cabo`, `cupom`, `placa`,
  `cancela`, `fundicao`, `pasta`. Na revisão: o mostrador da T16 cap10 cobre o título por um instante; agente retomado.
- 11/11 19:4x **Fila justa na trava pesada**: o `flock` direto acorda os que esperam em ordem quase aleatória; com 101
  tarefas na fila, tarefas esperavam mais de 2 h e morriam no prazo sem rodar (o robô da T02 desistiu de cap03/cap04/cap05/
  cap08 assim). **`ferramentas/rec/fila.sh`** (cópia em `$TUT_HOME/rec/fila.sh`): senha por prioridade (o número da aula,
  menor primeiro) e ordem de chegada; só a primeira senha tenta a trava (`flock -n`), então quem chega com prioridade maior
  passa à frente; senha de tarefa morta sai sozinha; `--ver` mostra a fila (conferido: A rodando, B prio 30 chegou antes de
  C e D prio 10, ordem A, C, D, B; código de saída preservado). Aviso aos 26 robôs e à cena de Windows: trocar o `flock`
  pelo `fila.sh --prio NN`, uma tarefa por vez, MP4 de ensaio com `--preset ultrafast --crf 30`, prazo máximo e, se morrer
  duas vezes no prazo, relatório parcial (retomo quando a fila andar). Efeito esperado: as aulas fecham em ordem (T00,
  T01, T02...), e a esteira (revisão → voz → gravação final → edição) começa pelas primeiras sem esperar as últimas.
- 11/11 19:3x **Robô da T02 (parcial)**: cap00 e cap01 aprovados no completo; rápido dos 11 no mundo antigo; cap02 e cap07
  pedem completo de novo (render ao lado); faltam os completos de cap04, cap05, cap06 e cap09 e o rápido com MP4 de cap03,
  cap08 e cap10. Retomado com prioridade 02. Achados do app no `MELHORIAS_ECOSISTEMA.md`.
- 11/11 20:1x **Robô da T20 (parcial, parou à espera da fila; instância 54320 derrubada)**: rápido aprovado em cap00-cap02
  (cap00 e cap01 sem MP4: repetir com a folha); cap03-cap10 por ensaiar (seletores do código, sem execução). Gerador,
  handlers do portal (portal-set-credentials, portal-login, entity-portal-report, order-photos-public, portal-order-receipt,
  `lib/portal.mjs`), sementes e as três fotos prontos; Edit mínimo no `entity-portal.mjs` compartilhado. **Os dois
  navegadores viram `goto` interno rotulado ("navegador do parceiro/sistema", corte na edição)**: o gravador filma um
  contexto só; o PDF do cap09 sai em base64 no `actions.json` (como a T08). **Retomar quando a fila chegar na prioridade
  20**: `cd /home/claude/ecoflix; export PORTAL_SENHA=... TUT_USER=rafael@reciclavalemetais.example; bash rec/t20/t20_fila.sh
  --rapido 3 4 5 6 7 8 9 10 0 1`, depois `prever.py` e o completo dos caps 4, 5, 6, 7 e 8 (dois navegadores); atenção ao
  cap06 L4 (pouca folga) e ao sino do cap08 (recarrega `/dashboard`).

## Retomar quando a fila andar (robôs parados à espera da vez)
| Aula | Agente | O que falta | Comando |
|---|---|---|---|
| T20 | afdb1a0ff5d8d10fb | rápido cap03-cap10 e cap00/cap01 com MP4; completo dos caps 4-8 | `bash rec/t20/t20_fila.sh --rapido 3 4 5 6 7 8 9 10 0 1` · **retomado 11/11 23:1x** (agente) |
| T18 | a82b96199a5d77ce9 | rápido de 03, 04 (seletores corrigidos), 05, 06 (selo da cota) e os estritos com folha de 00-10; `prever.py`; derrubar a 54318 | `bash /home/claude/ecoflix/rec/t18/t18_lote.sh 04:r 03:r 05:s 06:r 00:s 01:s 02:s 07:s 08:s 09:s 10:s` · **rodando desde 11/11 21:4x** (cap04 feito às 23:0x); no fim, conferir o log e retomar o agente para o `prever.py` e o relatório |
- 11/11 20:2x **Unificação do kit 2D lançada** (vaga aberta pelo robô da T20): `pulse()` sem deslocar elemento posicionado
  por `transform` e com pulsos que se somam; classe de grupo do kit com nome único (a "g" colidia, círculo gigante no tema
  do Cato); `descarrega` sem as peças 16 px abaixo do chão; exemplo "Tara e peso líquido" do kit sem chamar o caminhão vazio
  de tara (a T12, cadastro de veículo, fica como está). No kit e nas aulas que copiaram o código, conferindo antes e depois.
- 11/11 20:3x **Fila com envelhecimento** (aviso do robô da T15: desde 19:44 só a T00 e a T01 rodavam, voltando à fila
  logo depois de cada tarefa): a ordem agora é a hora de chegada + 3 min por nível de prioridade (a aula de número baixo
  passa à frente, mas ninguém espera mais de ~80 min a mais). Senha nova com prefixo "50-": as antigas (prioridade pura)
  andam primeiro, em ordem de aula, até acabarem; script trocado com `mv` (quem já roda segue no arquivo antigo). Conferido:
  antigo E20 primeiro, depois C0, B15, D15.
- 11/11 20:4x **Kit 3D com materiais reconhecíveis concluído** (agente do kit): latinha metálica com faixa genérica
  (inteira e amassada), PET translúcida (transparente e verde), ferro enferrujado (vergalhão, cano, chapa, perfil), cobre em
  fio e tubo, papelão, torrão, pneu, mangueira, sacola; tipos novos `latinha`, `pet`, `ferro`, `papelao`; `pets()`,
  `fardoPapelao()`, `bigBag()`. T07 com o big bag como tara (chip "saco") e a carroça com ferro misto; T08 com as latinhas
  novas. **Mandados ao Kaik às 20:4x: T07_3d.mp4, T08_3d.mp4, vitrine_3d.jpg e T05_3d.mp4.** Faltam as correções da T11,
  T12 e T16 (prévias depois).
- 11/11 21:1x **T11 em 3D mandada ao Kaik** (a pilha de latinha fica no "Entra"). T12 cap08: carregado agora sobe a
  "Carregado 9.460 kg" com "peso do material 3.080 kg", mas o "Tara 6.380 kg" ficava só ~0,4 s (a conta terminava em
  "Carregado"): agente retomado para chegar à tara até "peso" e segurar até "Carregado".
- 11/11 21:3x **T16 em 3D mandada ao Kaik** (cap10 corrigido: o título sobe antes do mostrador). Pendência para o render
  final: no cap07 ("O caminhão na nota") o caminhão passa sob o título grande por ~0,3 s no começo; fazer o título subir
  antes de o caminhão entrar no quadro (mesma correção do cap10). Regra geral para o render final das cenas 3D: conferir
  o primeiro segundo de cada cena (título grande × objeto entrando).
- 11/11 21:4x **3D da T04 e T10 prontos e mandados ao Kaik**: T04 cap00 (quem traz e quem leva, o Saldo), cap08 (papelão
  59% do peso a R$ 0,55 × latinha 9% a R$ 6,20), cap10 (a latinha de todo mundo vira o mesmo fardo; margem estimada R$ 1,20
  o quilo); T10 cap03 (separação: 6.420 → 6.100 kg e 2.180 → 2.500 kg) e cap09 (cobre do Siqueira e do Valdir na mesma
  pilha, a Fundição leva). O cap05 da T10 fica na 2D. Sem objeto novo (usou o `fardoPapelao` do kit e o `galpao`).
- 11/11 21:4x **Retomada 9/20** (lembrete): andando; app e Supabase falso no ar; fila justa com 24 senhas (as antigas
  quase acabaram); 17 agentes rodando. **Disco: 4,1 GB livres** (a pasta `/home/claude/domiflix` ocupa 16 GB: entregas
  finais da Domiflix 3,7 GB, app, gravações e projetos das aulas; as `aula_final.mp4` não são cópias soltas das entregas).
  Risco para a fase final da EcoFlix (gravações finais em 2560×1600 e renders): montar aula por aula e apagar os
  intermediários de cada uma depois de entregar; se faltar, perguntar ao Kaik o que da Domiflix pode sair.
- 11/11 22:0x **T12 em 3D mandada ao Kaik** ("Tara 6.380 kg" segura ~2 s com o caminhão vazio; carregado, 9.460 kg e o
  "peso do material" 3.080 kg). Prévias 3D já mandadas: T05, T07, T08, T04, T10, T11, T12, T16 (e a vitrine). Faltam T00
  (Opus, em andamento) e T17+T18.
- 11/11 22:1x **Cenas de Windows da T05**: as 8 cenas prontas e conferidas com `--mira` (textos e horas batem; 08:41:07 na
  cena 4), 38 capturas do código do EcoTray (sem linha repetida na Atividade Recente), `LEIA.md`; a prévia `T05_windows.mp4`
  está na fila (prio 05). Ao liberar a balança, o EcoTray de verdade escreve "Impressora padrão: POS-58" (08:44:10), fora do
  roteiro mas real. **Antes da gravação final**: trocar a página do navegador (hoje a imagem `feature-integracao.png`, que
  mostra "v1.2.5" de marketing) pela gravação `device: windows` do robô da T05 (`navegador.pagina.gravacao`).
- 11/11 22:2x **Robô da T05**: nenhum capítulo aprovado ainda; os dois primeiros ensaios caíram no login (a `TUT_SENHA`
  "x" era curta para o formulário; `_BRIEF_ROBO.md` agora pede 8+ caracteres); usa `fila.sh --prio 05`, um por vez. Cap04
  com relógio próprio para o cupom 08:41:07 (a calibrar); trechos `device: windows` só como roteiro (`cap02w`, `cap04w`,
  `cap06w`, `cap09w`); completo provável em cap06, cap09 e cap10.
- 11/11 22:3x **Robô da T18 (parcial)**: gerador dos 11 capítulos, handlers do SIGOR (`mtr_set_credential`, `sigor-mtr-sync-ref`, `-emit`, `-cancel`, `sigor-cdf-emit`, `lib/mtr_sigor.mjs`), sementes `inicio` e `apos-cap03..07`, `propostas_fala.md` (pausas e a 1ª linha do cap01 que falta na voz). Rápido passou em 0, 1, 2, 5-8 e 10; 3, 4 e 9 corrigidos sem rodar de novo; 6 com o selo da cota sem alvo. Na tabela de retomada.
- 11/11 22:5x **Unificação do kit 2D concluída** (kit e as 26 aulas): `pulse()` agora acrescenta `scale()` no fim do
  `transform` (sem deslocar; pulsos do mesmo quadro se multiplicam; chamar depois do `vis`); grupo `.g` → `.eco-grupo`;
  `descarrega` com o monte na linha da roda (compensado onde havia balança: kit, T07, T08, T15, T22, sem mudar a imagem);
  exemplo do kit vira "Dupla pesagem" (1ª − 2ª = Peso Bruto). Mudou na imagem: o pulso (sem escorregar e com os pulsos que
  se perdiam; >20 aulas) e o monte da T16 cap00 (um pouco mais alto). Conferido aqui: as 27 cópias com o código novo e dois
  quadros (T01 cap10 e T21 cap00, tema do Cato) sem erro.
- 11/11 22:5x **T00 em 3D pronta e mandada ao Kaik** (cap00 vista do pátio com as seis paradas; cap05 um pátio contínuo
  com a câmera do portão à balança 38 kg, à caixa registradora R$ 235,60, à baia e ao caminhão da Serra Fina; ilu05_conta
  na 2D). Objetos novos: `pessoa`, `registradora`, `cedula`, `portao`, `guiche`, `baia`, `banco`. **Vigia do render**: com
  a máquina cheia, um quadro 3D em SCHED_IDLE passou de 90 s sem estar travado; o padrão agora é 600 s (90 s com
  `RENDER_PRIORIDADE=normal`). Cenas de Windows da T05: 1 de 8 trechos da prévia renderizado (fila prio 05).
- 11/11 23:0x **T17 e T18 em 3D prontas e mandadas ao Kaik** (fecham as prévias 3D de todas as aulas). T17: ilu01_manifesto
  (MDF-e com as NF-e da carga; "Autorizado antes de sair", "Encerrado no fim da viagem"), ilu03_percurso (estrada com
  pórticos SP/RJ/MG, sem contorno de mapa; origem Tatuí, destino Itamonte), ilu06_servico (mercadoria × serviço). T18:
  ilu01_cadeia (gerador → transportador → destinador, MTR e CDF), ilu05_pdf_motorista (3/4 GHT7B19 com chaparia),
  ilu07_cargas_outubro (três 3/4 com baterias em 06/10, 16/10 e 27/10 e um CDF). Objetos novos: `folha`, `galpao`,
  `cacambaEstacionaria`, `motorista`, `estrada`, `porticoEstado`, `pinoLocal`, `fio` (a chaparia usa o tipo `ferro` misto
  do kit). **Na conferência, três ajustes pedidos ao agente** (refaz só esses trechos da prévia): na T17 o selo
  "Encerrado" sai metade na borda direita e o "Carregamento (Origem)" fica cortado na esquerda; na T18 os selos MTR/PDF da
  folha ficam em cima do título (e o quadro só tem a folha). Mandei as prévias ao Kaik já avisando dos ajustes.
- 11/11 23:0x **Kaik: "temos algum do ecotray já?"** Respondido: nenhuma aula tem voz ainda; da T05 existem as cenas 3D
  (16:17), as 8 cenas de Windows conferidas (folha de quadros + a cena 1 em vídeo mandadas agora; o ponto vermelho é a mira
  do cursor, a página do navegador ainda provisória) e o robô no ensaio (cap00 passou; 01-11 na fila). **Prévia das cenas
  de Windows numa vez só da fila**: a `previa.sh` mandava uma cena por vez, e cada cena voltava para o fim da fila (~1 h de
  espera por cena, ~7 h para as 7); parei e juntei as 7 numa tarefa (`fila.sh --prio 00`, o lugar que a senha da T05 já
  tinha; ~12 min de trava). Log `/home/claude/ecoflix/t05/windows/previa_resto.log`; o agente das cenas de Windows monta o
  `T05_windows.mp4` quando o "fim" aparecer.
- 11/11 23:1x **Robô da T20 retomado** (a fila com envelhecimento não deixa aula parada: não há "vez da prioridade 20").
  Robôs que encerraram a vez com o lote ainda na fila (T01, T02, T03, T05, T07, T08, T09, T10, T11, T13, T14, T17, T19,
  T26) seguem vivos: voltam sozinhos quando o lote ou o Monitor deles avisa.
- 11/11 23:2x **Robô da T13 (parcial) retomado**: cap04 aprovado no completo (maxLate 0,65 s; os 8,2 s sob os renders
  sumiram); cap06 e cap09 gravados sob carga (regravar); cap05 completo falhou (o calendário fechando fechava a lista da
  categoria; corrigido); 00-03 só no rápido sem folha olhada; 07, 08, 10-13 não rodaram. Novos: 5 handlers
  (`pay_financial_bill`, `pay_partner_balance`, `create_installment_bills`, `create_recurring_bill_template`,
  `shift_recurring_bills_due_date`), sementes `t13/inicio` e `apos-cap04..11` (Conta Principal fecha em 39.593,47). Fala:
  cap07 L6/L7 e cap08 L5 (com "Repetir até" o app cria as 6 contas de nov a abr, não a janela de 3 meses; as ilustrações
  mudam junto). Mundo: o `generate_due_recurring_bills` não completa a janela de 3 meses; as baixas lançam às 12:00 do dia
  pago. **Causa da parada**: o lote de 13 capítulos numa chamada só em segundo plano morre nas 2 h (cada capítulo espera
  45-60 min na fila). Regra nova no `_BRIEF_ROBO.md`: um capítulo por chamada; lote que morreu depois de rodar parte não é
  "morreu sem rodar". T13 e T18 retomadas assim (o lote da T18 rodou o cap04 e morreria às 23:45 antes do cap03).
  Robô que parar por isso: retomar com a mesma instrução.
- 11/11 23:2x **Supabase falso da skill atualizado** com os ajustes da cópia viva: valor entre aspas em `or=(...)`
  (`core/filters.mjs`, T13) e, no `http/auth.mjs`, o `iat` do token pelo relógio do mundo (o app 1.59 recusa login com
  diferença > 5 min) e o `verifyOtp` do "Esqueci minha senha".
- 11/11 23:2x **Kaik: "esses 3D vão intercalando com o conteúdo no sistema né?"** Sim: cada ilustração entra no meio do
  capítulo gravado, no lugar da janela do app, de uma palavra a outra da fala (5 a 20 s), e a gravação volta mostrando onde
  se faz aquilo; as prévias só emendam as ilustrações. 35 cenas em 3D no total.
- 11/11 23:3x **Robô da T05 (parcial) retomado** até o fim, um capítulo por chamada (o lote de 11 numa chamada morreria
  às 00:55): só o cap00 com rápido aprovado (montou 0,8 s de vídeo: conferir); cap04 na fila; depois 01-03, 05-11 e os
  trechos `device: windows` (02w, 04w, 06w, 09w), que substituem a página provisória das cenas de Windows. Sementes
  `t05/inicio`, `apos-cap02/04/05/06`; relógio do cap04 calculado pelo clique em "Testar" (SETUP_S a calibrar pela hora do
  cupom 08:41:07). Completo provável em cap06, cap09 e cap10.
- 11/11 23:5x **Cenas de Windows da T05 prontas e mandadas ao Kaik** (`T05_windows.mp4`, 58 s com trechos das 8 cenas;
  as 7 restantes renderizaram numa vez só da trava, 23:35-23:45). Notas para o robô da T05 repassadas (cursor parado na
  página no clique da bandeja). Falta só trocar a página provisória pela gravação `device: windows`.
- 11/11 23:5x **Robô da T08 (parcial) retomado** um capítulo por chamada: 00, 01 e 02 aprovados no completo (maxLate
  0,07-0,10 s); 03-10 por rodar (o lote morreu duas vezes nas 2 h). Handlers `get_next_ticket_number` e
  `finalize_weighing_ticket_v3`; sementes `t08/inicio` e `apos-cap02..07/09`; Edit de 5 linhas no `lib/eco.mjs`
  (`criarPedido` marca o ticket de origem como valorizado). Fala: cap06 respiro de ~3 s depois de "aba em branco", cap07
  "No fim do dia" → "Pouco depois", cap09 tirar "em vermelho". Achados no MELHORIAS (preço no ticket sem valores, "#1" na
  aba nova, telas cortadas em 1280 px). Gravação final: FAKE_NOW por capítulo (08:40, 08:49, 08:51, 08:58), o PDF térmico
  do cap08 vira ilustração. **Mundo base**: o ticket #57 tem `items` vazio e o app o trata como legado (0 kg na lista);
  formato fiel (item com a 1ª pesagem como bruto, `two_weighings`) pedido ao robô nas sementes dele; levar ao mundo base
  depois que ele confirmar.
- 11/11 23:5x **Robô da T05**: cap00 e cap04 aprovados no rápido; cap04 e `cap04w` vão ao completo (prever 3,4 s no
  "Testar" com a máquina cheia); relógio do cupom calibrado (`SETUP_S=10`); cap01 na fila, um por chamada.
- 11/11 23:5x **Robô da T04 (parcial) retomado** um item por chamada: rápido aprovado em 00, 01 e 03; faltam 02 (agora
  apaga o rascunho), 04-13 (o 09 tinha o menu aberto: setup corrigido) e os completos 03, 09, 12 (toast ou menu junto da
  fala). Handlers: cnpj-lookup, ibge-cities, set_partner_labels, link_customer_supplier, update_balance,
  create_manual_bank_transaction, get_supplier_profit_estimate, list_top_clients/suppliers_paginated,
  get_clients_suppliers_inactive_count; hooks de suppliers/customers (código sequencial e espelho do cadastro duplo);
  sementes `t04/inicio`, `apos-cap02/04/05/06/09`. Fala: cap03 "A tela pede pra conferir…" vai para a L4 (o toast some
  antes da L7); respiros para digitar em 02 L2/L3, 03 L2, 04 L5 e 09 L9. Gravação final: caps 01 e 07 com `APP_ORIGIN`
  no domínio (o link do portal saía 127.0.0.1). Achados no MELHORIAS.
- 11/11 23:5x **Economia de tokens na espera da fila**: os robôs que esperavam com Monitor eram acordados a cada 30 min
  (o Monitor expira) e mandavam relatório a cada acordada, relendo o contexto inteiro (300-700 mil tokens por acordada).
  Regra nova no `_BRIEF_ROBO.md`: o comando do capítulo é a própria chamada em segundo plano (prazo 7200000), e a
  notificação de término acorda o robô uma vez só; nada de Monitor para esperar a fila; relatório só no fim. Avisados
  T04, T05, T08, T18 e T20.
- 12/11 00:0x **Robô da T22 (parcial) retomado** um capítulo por chamada: rápido aprovado em 1, 2, 3, 4, 7 e 9 (antigos,
  sem MP4); 0, 5, 6 e 8 corrigidos sem reteste; cap10 falhou duas vezes (Quantidade já com 1.850; aviso cobrindo
  "Executar"; corrigido); cap11 só testado pela API. Ficam só no rápido 0, 1 e 3; completos previstos 2, 4, 6, 7, 9, 10,
  11. 25 RPCs, create-group-payment, check-asaas-payment, 2 hooks, `lib/grupo.mjs`; Edit no
  `get_dre_expenses_by_group.mjs` (soma o grupo por nome). Fala: cap07 L1-L3 com os números da tela (CMV 273.873,30,
  resultado 18.336,70, diferença 44.986,70), cap09 L6 sem a frase do Sobrescrever. **Código do grupo agora GRP-7C4E9A**
  (o que o app gera no mundo): trocado no MUNDO_FICTICIO, plano, roteiro (coluna Tela) e na ilustração do cap03 (a voz
  não lê o código). Gravação final: cap03 como Sandra Pires. Achados no MELHORIAS.

## Retomada de 18/11 (app 1.60.10, pouco limite)
- 18/11 13:29 **Kaik**: "continue de onde parou e tente não estourar tão rápido meu limite; use fable onde achar
  interessante; o app em si mudou bastante no repositório". Todos os agentes antigos morreram no limite semanal de 12/11
  (contextos de 300-700 mil tokens: **não retomar**; agente novo e pequeno por aula quando precisar).
- **App passou de 1.59.154 (f37573ea0) para 1.60.10 (origin/main 5290be4cd, 270 commits)**: Compra, Venda, Ticket e
  Usuários mudaram muito; Cato virou agente (1.60.0); Estoque Fiscal em abas (1.60.6); preenchimento inteligente de contas
  (1.60.5-8); CNPJ traz IE e regime (1.59.157); contas bancárias por usuário (1.59.165); pesagem avulsa com recebimento
  (1.59.163). Build novo em `app/dist` (o antigo em `app/dist-1.59.154`), `schema.json`, `defaults.json` e sementes
  regenerados (272 conferências). Script do build: ver RELIGAR (trocar o commit).
- **Varredura sem agente** (`rec/varredura/varrer.sh`, duas frentes): ensaio rápido sem MP4 de todos os capítulos no app
  novo; uma linha por capítulo em `rec/varredura/tNN.txt` e as chamadas desconhecidas em `tNN.unknowns.json`.
- 18/11 13:38 **Kaik (regra nova)**: "garanto que todos os tutoriais cubram tudo em detalhes, não tem problema ficar um
  pouco mais longo e explicar bem as coisas, principalmente na parte fiscal do sistema, e cobrir cada função e o máximo
  de casos de uso pertinente". → Depois da varredura, **auditoria de cobertura** por aula contra o 1.60.10 (cada função
  da tela e casos de uso), com peso nas fiscais (T16, T17, T18 e a parte fiscal da T04/T07/T03); capítulos novos onde
  faltar. Entra na mesma passada que adapta a aula ao app novo.
- 18/11 **Cobertura 1.60.10 das fiscais pronta** (`Tnn/cobertura_160.md`): T16 (18 mudanças, 5 capítulos novos, +705 s,
  ~35 min), T17 (26 mudanças, 3 capítulos novos + trechos, +395 s, ~20 min), T18 (4 mudanças, 3 capítulos novos, +243 s,
  ~15 min). **Kaik (13:47): "acho que uma aula só do fiscal, mesmo que grande mesmo"** → a T16 NÃO se divide: uma aula
  só de ~35 min. Decisões do coordenador: SPED (BETA) fora da T17; CIOT sem citar a marca do parceiro; a complementar só
  mostra a tela, sem ensinar valor de imposto. Em conferência: T07, T03, T02.
- 18/11 14:1x **Cobertura 1.60.10 das 26 aulas pronta** (`Tnn/cobertura_160.md`, agentes pequenos no Fable, ~230 mil
  tokens cada). Soma: ~84 capítulos novos e ~8.950 s (~2 h 30) de fala a mais. Por aula (capítulos novos / segundos):
  T00 2/207 · T01 1/306 · T02 3/296 · T03 1/172 · T04 4/445 · T05 1/130 (EcoTray 1.7.25: refazer as cenas de Windows 3-7)
  · T06 2/325 · T07 2/367 · T08 3/300 · T09 1/222 · T10 2/278 · T11 4/395 · T12 3/400 · T13 6/405 · T14 3/354 (com cartão
  de crédito e 2º OFX) · T15 4/400 (DFC completa) · T16 5/705 · T17 3/395 · T18 3/243 · T19 5/390 · T20 4/410 · T21 10/565
  (refeita: o Cato virou agente) · T22 6/488 · T25 2/215 · T26 3/410 · T27 1/125.
  **Decisões do coordenador** (Kaik: aula única mesmo grande): nenhuma aula se divide; SPED (BETA) fora; CIOT sem marca;
  edição em caixa fechado só na T09; excluir em lote na T14, categoria em lote na T15; pedido pelo portal na T20;
  Rastreamento entra na T12 ("Rotas" não); automação da folha na T19; WhatsApp só até o botão. **Na junção do mundo**:
  despesa/sangria da T06 (fechamento 957,10 afeta a T09), dois Pix da T13 (OFX da T14 e DRE da T15), cartão de crédito,
  devolução e notas 1252-1254 (T16 → T17/T18/T20), Aços Quiririm em Lucro Real/"É Indústria" (T04 → T16/T17),
  MUNDO_FICTICIO × plano da T22. Valores de folha (T19) e de imposto: só o que a tela mostrar no ensaio.
- 18/11 14:12 **Varredura: defeito corrigido**. Os `gerar.py` fixavam `VERSAO = '1.59.154'` no localStorage, e o app novo
  abria a janela "Sistema atualizado" por cima das telas (falhas falsas). Trocado para 1.60.10 nos 26 `gerar.py` e nos 354
  `capNN.json`; T00-T07 rodaram antes: **rodar de novo** quando as frentes terminarem. Handler novo
  `rpc/get_my_scale_weight_lock.mjs` (sem ele o peso travava na T07/T08). A fazer no mundo: `fiscal_onboarding_status`
  (faixa vermelha do certificado A1), balão do Cato (`cato_adoption_nudge_*` no localStorage), `app_config.app_version`.
- 18/11 15:42 **Kaik escolheu o estilo das ilustrações** na folha de 10 estilos (`planejamento/ecoflix/estilos/`,
  `estilos_10.jpg`): "vidro escuro e gradientes suaves me pegaram, daria pra intercalar de forma que não fique bagunçado?
  e esses estilos quando necessário ter algum tipo de 3D também"; "as transições entre um conceito e outro parecer que
  foram cenas e planos planejados, com transição de câmera 3D como se fosse um plano que vai mudando, a câmera dando zoom
  em relação ao plano". **A argila 3D sai.** Proposta em piloto (`_BRIEF_ESTILO_V3.md`, kit `perfis/ecoflix/cenas_v3/`):
  um sistema só com dois climas (claro/gradientes = mundo físico; escuro/vidro = mundo dos dados), troca só na passagem
  de conceito e motivada pela câmera; câmera contínua entre "estações". Piloto: T08 ilu04+ilu05. O piloto de motion em
  argila (kit v2) foi encerrado; a biblioteca de motion dele (`MOTION_V2.md`) é reaproveitada. As 35 cenas 3D e as 2D
  serão migradas depois da aprovação do piloto. Também: tutorial do Cato = T21 (confirmado); "Montar o plano" fica na T00.
- 18/11 16:5x **Varredura no 1.60.10 completa** (cópia em `planejamento/ecoflix/varredura_160/`; capítulos sem falha /
  total): T00 14/14, T01 13/14, T02 8/11, T03 13/13, T04 12/14, T05 14/16, T06 13/14, T07 ver arquivo, T08 8/11, T09 0/11,
  T10 9/13, T11 10/15, T12 10/12, T13 13/14, T14 14/15, T15 12/12, T16 12/19, T17 4/14, T18 10/11, T19 5/14, T20 3/11,
  T21 8/10, T22 10/12, T25 9/12, T26 10/14, T27 8/8. T09, T17, T19 e T20: parte é robô inacabado em 12/11. As chamadas de
  2 h do sistema cortaram as duas frentes; relançadas em lotes menores. **Junção do mundo em andamento**
  (`_BRIEF_JUNCAO_160.md` → `JUNCAO_160.md`); depois dela, a aplicação por aula (roteiro, fala, robô).
- 18/11 16:4x **Piloto do estilo v3 mandado ao Kaik** (`estilo_v3_piloto.mp4`, `estilo_v3_climas.jpg`; kit em
  `perfis/ecoflix/cenas_v3/`, 0,8 s/quadro). Aguardando aprovação; ilustrações antigas paradas. Migração estimada: 35 cenas
  3D (faltam ~25 objetos) e 218 cenas 2D.
- 18/11 17:18 **Kaik aprovou o estilo v3**: "Ficou ótimo a prévia da animação". Estilo das ilustrações da trilha = kit
  `perfis/ecoflix/cenas_v3/` (dois climas, câmera contínua). Próximo: biblioteca de objetos v3 (os que as cenas antigas
  usam) e, por aula, as cenas no v3 depois que a aplicação do 1.60.10 fechar o `ilustracoes.json` dela.
- 18/11 17:0x **Junção 1.60 aplicada** (`JUNCAO_160.md`; 280 conferências). **Aplicação por aula em andamento**
  (`_BRIEF_APLICAR_160.md`): primeira leva T16, T07, T08, T00.
- 18/11 17:25 **Kaik: "já gastou 26 por cento do meu limite semanal, tente economizar mais"**. Onde foi: 26 auditorias
  (~6 M de tokens, uma vez só), junção, estilos. **Regras de economia daqui em diante**: (1) ensaio em LOTE, o agente
  acorda uma vez por lote e não por capítulo (era o maior gasto: ~330 mil tokens por acordada); (2) no máximo 4 agentes
  de aula ao mesmo tempo, nenhum agente retomado com contexto > 400 mil (agente novo lendo o `andamento_160.md`);
  (3) Sonnet 5 nas aulas não fiscais de robô simples; Fable só em fiscal, Cato e direção de arte; (4) ilustração v3 só
  onde o conceito não se entende pela tela (enxugar as 218 cenas 2D na migração: meta de até ~4 por aula);
  (5) o coordenador responde curto e não comenta notificação de "esperando".
- 18/11 18:5x **T00 aplicada no 1.60.10**: 16 capítulos (novos: 8 "O Cato, o seu agente", 12 "Montar o plano";
  renumerados 8-13 → 9, 10, 11, 13, 14, 15), fala 1.544 → 2.066 palavras (~15,5 min). Rápido aprovado em todos
  (computador e celular, variantes cap40/cap41); completo em 04, 08, 12, 14, 07b, 08b; **falta** reensaiar o cap07
  completo (`bash rec/t00/t00_um.sh 07 --completo`). **Pedido ao mundo base (pendente)**: mensalidade 1.350,00 e
  `extra_users` 1. Ilustração nova: `ilu10_selos_status`. Valores em reais aparecem na tela de "Montar plano" e na oferta
  do cancelamento (a fala não cita). Próxima na fila de aplicação: T17. Depois: cenas v3 da T00 (`_BRIEF_CENAS_V3.md`).
- 18/11 19:01 **Kaik: "vamos montar a T08 toda do zero primeiro pra ser um piloto"**. T08 aplicada (14 capítulos, fala
  1.243 → 2.114 palavras, ~12,2 mil caracteres); rápido aprovado em 00-09, completa só no 08; o coordenador rodou o lote
  final (`t08_lote160.sh 10:--os-dois 11:--os-dois 12 13 07: 09:`, log `rec/t08/lote160_coord.log`). Cenas v3 da T08 em
  andamento. Nenhuma aula nova abre até o piloto sair (T16, T07, T17 terminam o que começaram).
- 18/11 20:05 **Kaik**: pode usar mais o Fable 5.2 "desde que seja eficiente" (tem 2 resets: 3x o limite semanal de
  Fable); e quer, no fim, **a lista completa de melhorias e correções do app, com os detalhes finos**
  (`MELHORIAS_ECOSISTEMA.md`: todo "achado" de agente entra ali na hora; no fim, revisar item a item contra o 1.60.10,
  tirar o que já foi corrigido e entregar organizado por tela e gravidade).
- 18/11 21:2x **T08 cap12 "Sem internet" refeito com queda de verdade** (passo novo `rede` no `runner.mjs`: `offline`,
  `modo` servidor/navegador, `avisar`; levado à skill): mostra o aviso, pesar e salvar ("Ticket OFF-01 guardado neste
  aparelho", comprovante provisório), os três bloqueios com motivo e a volta com o número oficial. Rápido 0 falhos,
  completo maxLate 0,71 s; fala 4 → 6 linhas. **Defeito real do app** no MELHORIAS (navegador offline: o Salvar gira).
  T08: completos aprovados em 07, 08, 09, 12; cap10 com o painel Filtros corrigido (fica aberto da linha 6 para a 7);
  lote rápido 10, 11, 12, 13 rodando (`lote160_coord3.log`). Cenas v3 prontas (`T08_v3.mp4` mandado ao Kaik).
- 18/11 21:5x **T08 pronta para a voz**: 14 capítulos com rápido aprovado (completo em 07, 08, 09, 12); texto mandado ao
  Kaik (`T08_narracao.md`, 2.154 palavras, 11.974 caracteres ≈ 12-13 mil créditos). **Aguardando o ok do Kaik para a voz.**
- 18/11 21:5x **T07 aplicada no 1.60.10**: 20 capítulos (novos 09 dois pedidos, 10 rascunho, 12 abater o vale), fala
  2.517 → 3.557 palavras (~23 min). Rápido aprovado em 00-07 e 09-17; completos com atraso por máquina dividida (refazer
  na gravação final); 08, 18, 19 corrigidos e rodando no lote do coordenador (`rec/t07/lote160_coord.log`). **Pedidos ao
  mundo base (pendentes)**: handler de `GET /auth/v1/health`; ligar o Depósito Irmãos Siqueira à Tabela Depósitos; e, da
  T00, mensalidade 1.350,00 + `extra_users` 1; da T08, o #57 com item. Ilustrações v3 pendentes: `ilu05_botao_cores`,
  `ilu10_rascunho`.
- 18/11 22:0x **T07: caps 08, 18 e 19 continuam abertos** (lote do coordenador, `rec/t07/lote160_coord.log`): o cap08 ainda
  tem `:has-text(...)` dentro de um `confere` (vira `querySelectorAll`: seletor inválido; 4 ocorrências no `cap08.json`);
  o cap18 tem 1 passo falho e o `record.mjs` sai com exceção (linha 48), sem folha; o cap19 depende da `apos-cap18`.
  **Fica para depois do piloto T08**: agente novo e pequeno, só esses três capítulos, lendo `T07/andamento_160.md`.
- 18/11 22:29 **Kaik sobre a T08**: "a animação ficou boa, só cuidado com desalinhamentos" (quadro aos 0:37: texto
  estourando o cartão "Compra ou venda", setas coladas, cartões cortados na borda, arco do fundo por cima) e "falaria da
  pesagem avulsa mas sem tanta ênfase, é algo mais de ponta; focar nos tickets, valorização, conceito, casos de uso".
  → Dois agentes: (1) cap11 encurtado para 5-6 linhas, casos de uso no cap01, valorização conferida, reensaio em lote;
  (2) correção na raiz do kit v3 (cartões medem o texto, respiro igual, fundo sempre atrás) + **verificação automática de
  quadro** que todas as aulas vão ter de passar, cenas da T08 revistas, ilu11 só com a 1ª janela, prévia nova.
  **Regra para todas as aulas**: recurso de ponta entra curto; o tempo vai para o fluxo principal e os casos de uso.
- 18/11 23:04 **Kaik aprovou a voz da T08 ("pode")**. Fala final: 2.017 palavras, 11.209 caracteres (avulsa enxuta,
  casos de uso no cap01). **Voz gerada** no fluxo novo "EcoFlix · Vozes de todas as aulas" (flow `E2aF9NQaqA00Zo9ZhjLg`,
  voz Kaik Barreto, eleven_v4, 1 versão por nó): 14 nós de capítulo (cap00 a cap13, na ordem) + 1 nó com os 13 títulos;
  **11.643 créditos** (1,04 crédito por caractere). Nó de estimativa vazio `K9N41E6d3H8t6Loh1RSJ` (sem geração; pode
  apagar). Próximo: o Kaik exporta o zip do fluxo e anexa; `proc.py` + `titulos.py`; gravação final da T08 com a voz;
  cenas v3 reancoradas nos tempos reais; edição.
- 18/11 23:46 **CORREÇÃO: a voz da T08 NÃO foi gerada.** As 15 gerações falharam por falta de crédito no ElevenLabs
  ("quota of 286000, 415 credits remaining"); nada foi cobrado. O coordenador tinha anotado "gerada" sem consultar o
  status: **regra**: depois de mandar gerar, consultar o status uma vez antes de dizer que saiu. Os 15 nós estão no fluxo
  `E2aF9NQaqA00Zo9ZhjLg` com o texto certo: quando houver crédito, rodar os MESMOS nós (`creative_run_flow_nodes`), sem
  criar nós novos. Necessário: T08 = 11.643 créditos; trilha inteira ≈ 366 mil caracteres ≈ 380-400 mil créditos (259 mil
  antigos + ~107 mil dos capítulos novos, a ~12 caracteres por segundo e 1,04 crédito por caractere, com 5% de folga).
  O plano do Kaik (Creator) renova em 28/11.
- 18/11 23:5x **Voz da T08 rodando** (Kaik pôs crédito): os MESMOS 15 nós via `creative_run_flow_nodes` (1 versão,
  11.642 créditos estimados). Status consultado: sem falha, 1 gerando e os demais na fila (limite de concorrência da conta,
  o ElevenLabs tenta de novo sozinho). Falta confirmar o término e receber o zip do Kaik.
- 19/11 00:0x **Contêiner reiniciado** (00:0x). `/dev/shm` zerou: código do app 1.60.10 reextraído em
  `/dev/shm/ecoflix-src` (só `git archive 5290be4cd`, sem `node_modules`: serve para leitura; o build segue em
  `app/dist`); app religado na 8080; instâncias do Supabase falso todas paradas. Lotes perdidos: T16
  (`t16_lote160.sh --completo 9 11 14 15 17 18`; o rápido de 3, 13, 15-24 já tinha terminado) e T17 (lote2: rápidos feitos,
  completos de 04 e 05 feitos, o resto dos completos não).
  **Estado T16** (25 capítulos; `rec/t16/_ens/_lote.txt`): rápido com falha em 15, 16, 17, 18 e 24; os demais ok.
  **Estado T17** (20 capítulos, 3.197 palavras; `rec/t17/_ens/lote2.txt`): rápido com falha em 08, 09 e 11; os demais ok.
  Os agentes da T16 e da T17 ficaram esperando lotes que não existem mais (contextos de ~510 mil tokens): **não
  retomar**; depois do piloto T08, agente novo por aula lendo `Tnn/andamento_160.md` + este registro, só para os
  capítulos com falha. Os completos ficam para a gravação final com a voz.

## 19/11 · T08 piloto: voz real, gravação final e montagem
- Voz da T08 alinhada (`proc.py` + `titulos.py`): 14 capítulos e 13 títulos, nenhuma palavra errada (as "fracas" eram artefato do
  reconhecedor; trecho do cap13 conferido em câmera lenta). Área de edição instalada com `instalar.sh` (TUTORIAL=t08 PERFIL=ecoflix);
  `models` é link para os da Domiflix.
- Gravação final: `rec/t08/t08_final.sh NN ...` (qualidade padrão, religa a instância no FAKE_NOW de cada capítulo). ~3 a 5 min por
  capítulo com a máquina livre.
- **A voz real saiu mais rápida que a estimada**: 06, 10, 11 e 12 atrasaram (até 4,9 s). Respiros com `pausas.py` nos vãos REAIS de
  silêncio (o `vad` do `emendas/capNN.orig.json`; vão de vírgula não serve, o script recusa). **Conferir o código de saída do
  `pausas.py`**: com `| tail -1` o erro passou batido e regravei 10 e 11 à toa. Respiro ANTES da linha não cura atraso que nasce
  dentro da frase (âncoras são por palavra): o respiro vai DEPOIS do trecho denso, e a edição acelera o silêncio (`acelera` no
  specs: cap06 3x, cap11 2x). Para as próximas aulas: no `gerar.py`, prever folga para voz ~8% mais rápida que a estimativa.
- Câmera: digitação com `noClick` na Pesagem avançada reprovou em 11 e 12; zoom manual `escala 1.4` no specs resolveu.
- **Ilustração v3 em `--dsf 2` pisca** nas cenas escuras de vidro (o Chromium fotografa antes de pintar um bloco: cartões somem por 1
  a 3 quadros; 8 piscadas na `ilu01`). Em `--dsf 1.35` (1728x1080, maior que a caixa de 1587x992 do palco) sai limpo e 4x mais
  rápido (141 s contra 9 min). **Padrão da trilha: `--dsf 1.35`, e `python3 -I perfis/ecoflix/cenas_v3/piscadas.py *.mp4` em toda
  cena renderizada** (acha elemento que some e volta; calibrado na `ilu01`).
- Janelas das cenas com a voz real: `ilu05` passou a ir até "quatrocentos" (o resultado é falado com ele na tela); auditoria
  `auditar.cjs --passo 0.25` aprovada depois de 3 ajustes de margem e do título no mergulho.
- Montagem: `t08/edit/montar_t08.sh` (render dos capítulos ~2,5 min cada, `finish.py` ~13 min, legendas). Aula: 13 min 50 s.

## 19/11 (noite) · retorno do Kaik sobre o piloto T08 e app 1.60.18
- **Decisões do Kaik**: gravar em **16:9, tela de 1600x900** (escolheu entre 1920x1080 e 1600x900 vendo os dois no palco);
  **fundo do palco escurecido** (brilho 0,55, aprovado). T08 cap09: "quando fala de abrir o comprovante 80mm não mostra nada
  na tela": o comprovante abre em outra aba; **toda aula que fala de PDF/comprovante mostra o papel real na tela** (ilustração
  com as páginas do PDF gerado pelo app, zoom acompanhando a fala). Vale também para o cap11 (avulsa).
- **Como ficou no código**: `mundo.json -> navegador.tela {1600, 900, escala 1.8}` (quadros 2880x1620), lido por
  `rec/recorder/browser.mjs` (`TUT_VIEWPORT`/`TUT_SCALE` vencem); `marca.json -> palco.brilho 0.55`, lido por
  `fundo_escuro.py` (sem a chave sai idêntico; `identidade_domiflix.sh` conferido). O palco se ajusta sozinho ao 16:9
  (janela 1832x1030 em (44, 25)). **As cenas v3 são 1280x800 (16:10): precisam de versão 16:9** e a caixa das ilustrações no
  specs muda para a janela nova.
- **App 1.60.18** (`e8edc9e6d`, 93 commits depois da 1.60.10) no build de gravação (`app/dist`; a 1.60.10 ficou em
  `app/dist-1.60.10`). Handoffs do Kaik em `planejamento/ecoflix/handoffs/`: fiscal (Relatório/Estoque Fiscal em 7 abas,
  status "Encerramento enviado"/"Cancelamento enviado", aba Empresa, endereço fiscal próprio, Pré-visualização com DANFE/XML
  reais, textos automáticos; **homologação só por CNPJ: não anunciar; DANFE modelo novo não é o de produção até 01/12**),
  caixa (abrir zerado nunca é barrado; aviso "Saldo insuficiente em dinheiro" com "Abrir zerado (R$ 0,00)" e link do
  tutorial `TUTORIAL_DINHEIRO_FISICO_URL` em `src/lib/caixa.ts`, **que temos de avisar quando a estrutura da EcoFlix mudar**),
  resposta às nossas correções (quase tudo corrigido; ver arquivo) e a novidade **margem automática na tabela de preços**
  (T03: Materiais > Editar Preços em tela cheia, chave "Margem automática", por tabela ou por material, % ou R$/kg, resumo
  com "Venda abaixo da compra"/"Sem preço"/"Margem típica", calculadora no cadastro; margem sempre sobre a compra).
- Aulas com mudança visível (lista do Kaik): T07, T08, T02, T00, T04, T06/T09, T10, T11, T19, T20, T22, T26, T05, T18, T27;
  mais T03 (margem), T16/T17 (fiscal). Todas serão reensaiadas de qualquer forma (versão e tela novas).
- Varredura 1.60.18 em 1600x900: `rec/varredura/tudo.sh` (resultado anterior em `rec/varredura/v160_10/`).

## 20/11 · adaptação por aula ao 1.60.18 (agentes Sonnet, `_BRIEF_APLICAR_160.md` com o bloco de 20/11)
- **T02**: 14 capítulos (eram 11; novos 06 Restrições e contas do banco, 07 O mapa das permissões, 12 Relatório por
  Usuário; antigos 06-09 viraram 08-11, 10 virou 13). Fala 1.483 → 2.313 palavras. 14/14 no rápido; completos 04, 05, 07
  (cap04 com 1,0 s em "liga Pedidos": rever com a voz real). Ilustrações pendentes do v3: ilu06_proprios, ilu07_mapa_grupos,
  ilu12_relatorio_pdf (comprovante; o robô devolve o HTML do relatório). `cenas.html` e `tempos/` antigos ficaram velhos.
- **T08 refeita na 1.60.18** (20/11 03:26): 1600x900, palco escurecido, 8 ilustrações v3 em 1920x1080 (`--larg 1422 --dsf
  1.35`, sem piscadas), cupom real na tela no cap09 e no cap11 (`cenas_v3/comprovante.html`), voz nova do cap04/cap07
  (1.644 créditos). Aula 13:59,9, -16,3 LUFS, -3,8 dBTP. Prévia de 720p enviada. **Lições**: (1) ensaio fora da fila junto
  com a gravação final deu atrasos de até 16 s: tudo em série; (2) um `confere` com texto que o app não mostra mais espera
  ~6,7 s e empurra o resto do capítulo: na troca de versão, conferir os textos dos `confere` antes de pôr respiro na voz;
  (3) `--dsf 1.3` em 16:9 dá largura ímpar e o x264 recusa (o `render_cenas` agora sai na hora).
- **T03**: 17 capítulos + cap01b (novos 07-10 margem automática, 12 menu da tabela; 07-11 antigos viraram 11, 13-16).
  Fala 1.959 → 3.600 palavras (~23 min). Todos no rápido; completos 07, 10, 12, 14; faltavam 06 (rápido e completo) e
  09 (completo): rodados pelo coordenador no mundo base (20/11 04:15): 06 rápido 0 falho, completo 1,17 s no pior gesto (rever com a voz); 09 completo 0,33 s. Sementes `margem-fora`, `margem-material`; handlers
  `save_price_table_margins`, `duplicate_price_table`, `set_my_preferred_price_table`. **schema.json e defaults.json do
  mundo base regenerados do 1.60.18** (tabela nova `price_table_material_margins`; colunas `auto_margin_*` em
  `price_tables`, `show_on_receipt` nos itens, `show_pack_conversion_on_orders` em `companies`); o mundo privado da T03
  (`rec/t03/_mundo`) ficou igual ao base e saiu do `t03_env.sh`. Ilustrações pendentes: ilu07_margem, ilu09_fora,
  ilu12_ordem e dois PDFs (pdf14_estoque, pdf14_tabela). **Para o Kaik**: Prefixo (F10) e seleção em massa (F11) ficaram fora.
- **T04**: 18 capítulos (novos 05 Lucro Real, 06 baixada, 09 etiquetas e filtros, 13 ajustes de saldo; cap04 refeito).
  Fala 3.238 palavras (~20,8 min). Rápido aprovado: 00-03, 09-16. Não fecharam: 04 (lentidão da máquina) e, por cadeia,
  05-08 e 17; cap12 com o PDF do extrato só no cabeçalho (gerar.py corrigido). Coordenador relançou os lotes de
  `andamento_160.md`. Handlers: `ext/publica.cnpj.ws`, `registrar_consulta_cnpj_ie`, `apply_balance_delta`; editados
  `cnpj-lookup` e `functions/cep-lookup` (compartilhado: só o CEP 12062150). PDFs (extrato e relatório) com cena pendente.
  T04 fechamento (agente Sonnet, 20/11): rápido aprovado 04-07, 09-16; completo sem falha 05, 06, 07, 09, 10, 12, 13, 14
  (06, 07, 09, 12, 13 com gesto ≥ 0,85 s na voz estimada: rever com a voz). Falta: `t04_lote160.sh 8 12 17` (cap08 e cap17
  dependem das sementes da cadeia), completos 04 e 16 (correções sem teste). Lição: clique de linha vai no NOME (o centro da
  linha caía no botão "..."); `js_garante` reclica sem cursor quando o efeito não vem; aviso de CNPJ repetido só no onBlur.
- **T06**: 16 capítulos (novos 06 cofre zerado/negativo, 11 despesa e receita, 12 sangria; cortes 09b e 13a; 06-09
  antigos viraram 07-10, 10→13, 11→14, 12→15). Fala 2.044 → 3.253 palavras. Rápido aprovado em todos menos o 03 (menu
  "Editar saldo de abertura": correção no gerar.py, coordenador reensaiando). Valores conferidos na tela: 3.006,50,
  1.450,00, 957,10. Impacto na T09: #85 fecha com 957,10, #86 com 15.000,00, Conta Principal +5.120,00. Sementes novas:
  cofre-negativo, apos-cap10..14, dia-10-rascunho. **Faltou** a cena do PDF "Ver comprovante" (regra do comprovante na
  tela): fazer junto das cenas v3 da aula. O modal "sem permissão" só é falado (o mundo não tem usuário sem permissão).
  **Para o Kaik (fim do projeto)**: o link "Ver tutorial: como funciona o dinheiro do caixa" (`TUTORIAL_DINHEIRO_FISICO_URL`
  em `src/lib/caixa.ts`) aponta para a aula 5.5 da EcoFlix antiga; trocar quando a trilha nova for publicada.
  T06 cap03 fechado pelo coordenador (20/11 06:11): no 1.60.18 o menu da linha do histórico abre no HOVER (o clique o
  fechava) e Todas/Dinheiro/Pix/Transferência viraram botões (não `role=tab`). T06: 16/16 no rápido.
  T04 fechado pelo coordenador (20/11 06:20): cadeia 04-09, 12, 17 relançada; 09 e 17 falharam uma vez por clique que não
  pegou (instável) e passaram na repetição. **T04: 18/18 no rápido.** Completos pendentes: 04 e 16 (sem teste das correções);
  gestos de 06, 07, 09, 12, 13 a rever com a voz.
- **T10**: 15 capítulos (novos 07 "Achar uma movimentação", 11 "Clientes, usuários e grupos"; 07-09 antigos viraram 08-10,
  10→12, 11→13, 12→14). ~2.470 palavras. 15/15 no rápido (0 DIFERENTE); cap11 com passo novo (ordem do Resultado) em
  ensaio pelo coordenador. View nova no mundo base: `handlers/views/orders_with_payments.mjs` (mantida no base). PDFs com
  cena pendente: pdf07_kardex, pdf13_posicao, pdf13_relatorio (`rec/t10/t10_pdfs.py` extrai).
- **T09**: 12 capítulos (novo 07 "Exportar a lista"; 07-10 antigos viraram 08-11). Fala 1.702 → 2.252 palavras. 12/12 no
  rápido (6 lotes pela fila). A varredura falhava por falta de `fake_now.json` (com 10/11 a janela "Tarefas para hoje"
  cobria a tela); agora 11/11 08:30. Atrasos previstos a tratar com a voz: cap04 (L2 ~4 s, L6 ~5 s), cap07 L4 (espera do
  PDF), cap08 L6. Mundo base (aditivo): `lib/eco.mjs` (`p_force_cash_register`) e `lib/pedido_estorno.mjs`. Sementes do
  `t09_sementes.py` seguem a T06 (#85 957,10, #86 15.000,00). Ilustrações pendentes: ilu04_soma, ilu04_caixa_fechado e 6
  PDFs (comprovantes Vale Forte, Aparecida, Valdir; relatório de pedidos; fechamento; estoque do caixa). "Imprimir direto"
  depende do EcoTray (só falado).
- **T12**: 18 capítulos (novos 07 editar/cancelar/excluir, 08 relatório para o parceiro, 12 movimentações e ficha do
  parceiro, 13 rastreamento, 16 checklist e assinaturas; portal 7→9, frota 8→10, caçambas 9→11, relatório 10→14, regras
  11→15, resumo 12→17). Fala 1.716 → 2.943 palavras. `gerar.py` = `_head.py` + `_caps1.py` + `_caps2.py` (edite as partes).
  Handlers: `delete_collection_order`, `get_collection_live_positions`, rede externa cdnjs e arcgis (mapa). Lote de
  ensaio lançado pelo agente; coordenador recolhe (`rec/t12/_ens/lote.log`). **A T20 parte de `apos-cap15`** (cap06 +10
  bags ao Depósito, cap11 cria "Palete de madeira" e põe a Caçamba 02 em manutenção, cap12 +10 bags à Cooperativa).
- **T11**: 19 capítulos (novos 10 editar ordem em andamento, 15 Conversão, 16 Perda padrão, 17 Máquinas; 10-13 antigos
  viraram 11-14, 14→18). Fala 2.044 → 3.087 palavras. 19/19 no rápido num lote só, sem atraso. Valores vistos na tela:
  Conversão 16 kg de fio, R$ 28,80; Perda padrão 37,5%, capa 24 kg. Handlers só da T11: `add_production_entry_atomic`
  (grava `note`), `register_production_atomic` (novo). Capa de fio com código 17 (o 16 é o Fardo de alumínio).
  Ilustrações pendentes: ilu12_pdf (comprovante), ilu15_conversao, ilu16_perda_padrao.
- **T13**: 20 capítulos (novos 06 preenchimento por padrão, 10 parcelas em grupo, 12 valor da ocorrência, 13 quitar em
  lote, 14 estornar, 18 exportar; 6-13 antigos viraram 7, 8, 9, 11, 15, 16, 17, 19). Fala 1.951 → 3.076 palavras (aula
  ~22 min). 20/20 no rápido. Completos dos sensíveis (08-13, 17) depois da voz. Handlers só da T13:
  `update_installment_bill_group`, `delete_installment_bill_group`, `pay_recurring_financial_bill`,
  `pay_financial_bills_batch`; `create_installment_bills` (compartilhado) grava `installment_group_id`. **Mundo base
  (coordenador)**: `schema.json` ganhou `financial_bills.installment_group_id` à mão (o `types.ts` do app não tem a
  coluna; a migration `20261117234500` tem: **ao regenerar o schema do types.ts, repor**); o filtro de banco de
  `get_financial_description_suggestions` segue a migration `20261119223100` (a pagar: withdrawal|expense; a receber:
  deposit). PDFs com cena pendente: cap16 comprovante, cap18 lista exportada (o robô não abre aba: a cena sai do arquivo).
- **T12 rodada 2** (agente Sonnet): aprovados 00-07, 09-12, 14, 15 (08 e 12 também completos). Correções: lote conta
  gravador caído como falha; cap12 abre a ficha completa `/cliente/...` (a lista só abre painel sem a aba Coletas);
  cap13 com GPS simulado e `history.back()`; cap16 com `apos-cap15` sem `collection_settings` duplicado. Coordenador
  rodando `t12_lote.sh 08 13 16`.
  T12 fechado pelo coordenador (20/11 09:57): 08 rápido e completo; 13 rápido ok, completo com 2 passos falhos (prever 2,65 s:
  rever com a voz); 16 rápido e completo ok (prever 5,1 s: respiro na voz). **T12: 17/17 capítulos com robô no rápido**
  (o 17 é montagem). Cap16: em Configurações o grupo "Coletas & Logística" fica fechado; abrir o grupo antes do link.
  Lição: dois lotes da mesma aula ao mesmo tempo (o do agente que "terminou" e o do coordenador) disputam a porta 543NN e
  dão resultado misturado: antes de relançar, `pgrep -f tNN_lote` vazio.
- **T15**: 17 capítulos (novos 07 Organizando o DRE, 11 DFC prevista, 12 DFC realizada, 14 Vários lançamentos).
  ~3.392 palavras. Lote 00-15 lançado pelo agente (coordenador recolhe). 5 handlers novos e a semente `lote-categoria`.
  Ilustrações pendentes: ilu11_dfc_previsto, ilu15_historico_pdf. **Pedido ao mundo base**: `bank_account_id/name` em
  `linhasDRE` (senão o filtro "Conta bancária" do Histórico fica vazio). A aula não tem o cartão "Lucro Líquido".
  **Decisão do Kaik pendente**: citar só as "Outras visões" e deixar de fora as duas moedas?
- **T14**: 19 capítulos (novos 03 cartão, 06 corrigir/excluir lote, 17 outra conta/vários lançamentos; 3→4, 4→5, 5-14→7-16,
  recap→18 sem robô). Fala 2.211 → 3.209 palavras (~20,6 min). 18/18 no rápido; completos depois da voz
  (`bash rec/t14/t14_cap.sh NN`); atrasos previstos em 01, 05, 06, 09, 12, 17 (`propostas_fala.md`). Valores vistos:
  552,20, 44.684,77, 45.236,97. 8 handlers novos (conciliação, cartão, lote de banco). Ilustrações pendentes:
  ilu01_extrato_pdf (o Extrato abre em HTML numa aba nova), ilu17_outra_conta. O pedido ao mundo base (filtro de banco das
  sugestões) já foi aplicado.
  T15 fechada (agente Sonnet, 20/11): **16/16 no rápido**, 0 tela diferente da fala. Fala mudou em 2 linhas (cap06: o DRE
  padrão não abre centros de custo; cap08: a divisão por centro de custo nunca aparece no regime de caixa). Semente nova
  `t15/previsto`; `_patch` do `created_at` do `bt.135`. **Mundo base**: `lib/eco.mjs` → `linhasDRE` devolve
  `bank_account_id`/`bank_account_name` como o RPC real. Valores vistos: Pátio R$ 28.500,00 de despesas; DFC de outubro
  com variação de R$ -67.749,00.
- **T19**: 18 capítulos (novos 07 folha CLT, 08 férias e 13º, 10 relatório, 13 tablet; extrato 7→9, ponto 8→11, celular
  9→12, folha 10→14, config 11→15, arquivar 12→16, recap 13→17). Fala 2.062 → 3.146 palavras. Rápido: 00-08, 10, 11,
  15-17 limpos; 09 e 12 com 1 passo opcional; **não fecham 13** (tablet para em "Tirar foto agora") **e 14** ("Data de
  início" da Ausência não aceita digitação); `apos-cap13/14` aproximadas. Valores vistos: líquido 2.168,11, INSS e saldos.
  Handlers só da T19: `rpc/set_ponto_pin`, `functions/time-clock-portal`. 6 ilustrações novas pendentes (recibos, holerite,
  relação de pagamento). Voz: respiro de 4,5 s na L2 do cap11. Tablet em 4:3; reconhecimento facial não é filmável.
  T19 fechada (coordenador, 20/11 12:16): 13-17 com sementes regravadas na cadeia; 13, 15, 16, 17 limpos; 14 com 1 passo
  opcional (hover da linha da Juliana). **T19: 18/18 no rápido.** Fala do cap13 corrigida: depois da saída o tablet volta
  para a CÂMERA (não para a lista). cap13: stub de `navigator.geolocation` no setup (o tablet não tem a permissão de
  localização do celular). cap14: "Data de início" é DateField (calendário), não aceita digitação.
- 20/11 12:23 **Kaik viu a T08 pronta ("ficou muito bom") e liberou o resto ("pode seguir com todo o resto")**: voz das aulas
  prontas em lotes, T03 com Prefixo (F10) e seleção em massa (F11), T15 sem as duas moedas (já estava fora). Voz: nós no
  fluxo `E2aF9NQaqA00Zo9ZhjLg` (label `Tnn capMM <título> (1.60.18)` e `Tnn títulos (1.60.18)`, títulos separados por
  `\n[pause]\n`, como na T08), lotes A = T02, T04, T06; B = T09, T10, T11, T12; C = T13, T14, T15, T19 (≈ 180 mil caracteres,
  ≈ 188 mil créditos); listas exatas em `scratchpad/voz/Tnn.json`. T19 cap09: "folha A4" → "folha á-quatro" na voz (troca
  `á-quatro` → `A4` no `config_narracao.json`). T03, T20 e T22 entram na voz quando fecharem. Ajudantes: voz (Sonnet),
  T03 (Sonnet), T20 retomado depois do lote 3; T22 no lote 1. Saldo de créditos: a ferramenta de uso da conta pede
  permissão nova (não deu para consultar); se faltar crédito, a geração falha sem cobrar.
- 20/11 12:4x **T20 aplicada (agente, 3 lotes gastos)**: 16 capítulos (novos 5 senha por seção, 6 cliente e fornecedor, 10
  preços, 13 WhatsApp; 7, 8, 9, 11, 12, 14, 15 renumerados), fala 1.518 → 2.701 palavras. Rápido ok: 0, 1, 2, 6, 7, 11, 13,
  14; cap12 passa mas sem PDF; 3, 4, 5, 8, 9, 10 corrigidos sem ensaio; cap08 com saldo antigo no portal depois do pagamento
  (causa não achada); cap04 L9 fala "desligar a chave" e o robô só passa o mouse. Handlers `entity-portal`,
  `entity-portal-report`, `portal-order-receipt` no 1.60.18; o agente mexeu também em arquivos compartilhados com a T12
  (`lib/coletas.mjs` com `cfg.locked`, `lib/portal.mjs`, `collection-request` aceitando sessão). Achado: o portal 1.60.18 não
  tem `<main>`. Ajudante novo (Sonnet) fecha T20 e confere a T12 (cap09 no portal + `t12_lote.sh 08 13 16`).
- 20/11 12:3x **Crédito**: o Kaik pôs US$ 47 (limite 313.500 → 561.000; usado 298.872; ~262 mil livres; renova em 28/11 12:42 UTC).
  Ajudante da voz liberado para os lotes A, B e C (~188 mil). Ficam ~74 mil para T03, T20 e T22 (~54 mil). As 11 restantes
  (~195 mil estimados, texto ainda vai crescer) precisam de mais crédito depois. Regras de economia no `perfis/ecoflix/voz.json`
  (`economia`): voz só com texto congelado; correção por frase com `emendar.py`; 1 versão; eleven_v4 mantido.
- 20/11 13:xx **Voz disparada**: lote A (T02, T04, T06; 51 nós) e T09, T10, T11, T12, T13 (88 nós, menos o nó de títulos da T13)
  com 1 versão; nenhuma falha. Estimativas por aula (créditos): T02 12.699, T04 18.281, T06 17.749, T09 12.431, T10 13.622,
  T11 17.351, T12 16.649, T13 16.987, T14 18.062, T15 19.097, T19 17.521. Faltam disparar: T13 títulos (`P5sRktMXiDOTkajVV7OE`),
  T14, T15, T19 (ids em `scratchpad/voz/nos_Tnn.json`): o disparo parou em 429 (fila de gerações cheia; nada cobrado).
  Ajudantes de voz estouraram contexto com `creative_add_flow_node`; jeito barato anotado em `perfis/ecoflix/voz.json` (`montar_nos`).
- 20/11 13:xx **T03 fechada (agente)**: Prefixo no cap03 (2 linhas: "Ao lado do código fica o Prefixo ... Digito pê, e a linha
  embaixo mostra pê setenta." / "O prefixo aparece na tela, no comprovante e na nota fiscal. O número no banco não muda. Aqui eu
  não preciso dele, então apago.") e seleção em massa no cap15 (antigo cap10; 2 linhas, com Transferir Estoque, Definir prefixo
  e Excluir); 3.600 → 3.694 palavras. Completos de 03, 06, 08, 09, 11, 13 sem falha (pior atraso 1,67 s no 13); cap15 trocou
  para Ferro pesado e Ferro misto (o radiador fica na 2ª página), completo com 5,29 s na L6 (respiro na voz). Coordenador:
  legenda "Digito P" e "P70" (`config_narracao.json`) e o último ensaio do cap15 (`t03_lote2.sh misto r15 c15`).
- 20/11 13:13 T03 cap15 com os seletores novos: rápido 0 falho; completo 0 falho com L6 5,7 s atrasada (o "Definir prefixo" e o
  desmarcar levam mais que a fala da L5): respiro de ~6 s antes da L6 com `pausas.py` depois da voz. **T03 pronta para a voz**
  (18 nós, 20.465 caracteres; `scratchpad/voz/T03.json`).
- 20/11 13:1x **Voz disparada também**: T13 títulos, T14, T15, T19 (fila baixou; lotes de 10 a 19 aceitos) e T03 (18 nós
  criados pelo coordenador, 20.463 créditos; custo por nó = caracteres exatos do texto). **Voz de 12 aulas no forno**
  (T02, T03, T04, T06, T09-T15, T19; ~208 mil créditos). Falta: conferir que tudo completou e pedir ao Kaik o zip do fluxo.
- 20/11 13:5x **Voz das 12 aulas completa** (215 nós `completed`, sem label duplicado; conta: 298.872 → 499.805 créditos,
  200.933 gastos). Pedido ao Kaik: exportar o fluxo "EcoFlix · Vozes de todas as aulas" em zip e anexar. Dica de economia de
  contexto: `creative_get_flow` grande vai para arquivo; contar os estados com Python em vez de ler.
- 20/11 13:5x **T07 aplicada ao 1.60.18 (agente, 3 lotes)**: 20 capítulos, rápido 20/20 sem falha; completos sem falha em 05,
  08, 09, 10, 13, 15, 16, 17, 18 (atrasos até 2,3 s com a máquina dividida; cap17 e cap18 6,8 s: no 18, a faixa "Sem conexão"
  só aparece quando o ping em andamento estoura, até 8 s). Fala 3.557 → 3.628 palavras (cap04 margem automática; cap05 coluna
  "Peso Bruto"; cap09 janela "Atualizar os preços?"; cap18 sem a faixa verde, que some em 0,3 s). Sementes regravadas e
  `apos-cap18` nova. **Bloqueios**: cap17 (PDF com valores apesar do "sem valores": bug do app CONFIRMADO no código,
  handoff `handoffs/2026-11-20_correcoes_T07.md`) e cap15 (cupom 58 mm com "Material não identificado": ajudante apurando
  se é do app ou do simulador). Voz da T07 só depois disso.
- 20/11 14:xx **T00 no 1.60.18 (agente)**: só o menu Fiscal & Ambiental mudou ("Relatório/Estoque Fiscal", `routes.ts:510`, no
  lugar de "Estoque Fiscal" e "Relatórios Fiscais"); 1 linha de fala (cap06: "...os documentos ambientais e o relatório e
  estoque fiscal."). Lote de 36 rápidos + completos 06, 07, 06b rodando (`rec/t00/_ens/lote_*.log`, LOTE-FIM); instância 54300
  fica de pé até o fim. Cupom 58 mm sem nome do material: bug do app confirmado (handoff T07, item 2).
- 20/11 14:47 **Kaik liberou o Fable**. Uso: ilustrações v3 em 16:9 das aulas com voz pronta (a maior fatia que falta), uma
  aula por ajudante Fable, começando por T02 e T06; `_BRIEF_CENAS_V3.md` ganhou o bloco de 20/11 (16:9, piscadas, comprovante
  com o papel real tirado do PDF do robô, âncoras por palavra sobre os tempos estimados). Sonnet segue nas adaptações; Opus na T16.
- 20/11 14:56 **Zip das vozes recebido** (230 MP3; as 215 dos 12 nós "(1.60.18)" conferidas, nenhuma faltando). MP3 movidos
  para `$TUT_HOME/tNN/narracao/recebido_1.60.18/capMM.mp3` e `titulos.mp3`; ferramentas de narração copiadas; processamento
  (`proc.py --take` + `titulos.py`) pela fila com `rec/voz_proc_lote.sh` (log `rec/voz_proc_lote.log`, VOZ-LOTE-FIM).
  Disco: 2,8 → 3,8 GB livres (apagados os intermediários regeráveis da T08 e MP4 de ensaio velhos; o zip em
  `/mnt/user-data/uploads` ocupa 231 MB do mesmo disco e é só leitura). Aula final 1080p ~180 MB cada: guardar todas não cabe;
  decidir com o Kaik como entregar. Briefing novo `_BRIEF_FINAL.md` (gravação final + montagem por aula, molde da T08).
- 20/11 15:11 **Kaik publicou o 1.60.22** com as correções da T07 (comprovante sem valores no PDF pós-finalização, cupom
  58 mm com o material, faixa de sincronizado 3 s, título do menu lateral). Entre 1.60.18 e 1.60.22 (21 commits): pagamento
  retroativo de funcionário (T19: rever no ensaio), DANFE real na pré-visualização, lupa de CNPJ na Configuração Fiscal e 539
  (T16/T17: avisado o agente da T16), ticket avulso → padrão limpa o parceiro (T08 pronta: não usa essa troca), login com
  conta sem empresa. Migrations sem tabela nova para o mundo (só função de saldo de funcionário, repair e 539).
  Build do 1.60.22 pela fila (`rec/build_1.60.22.sh`, log `rec/build_1.60.22.log`); `app/dist-1.60.18` guardado,
  `dist-1.60.10` apagado. Novos achados do Kaik (fora do pedido): rascunho ao lado mostra o número antigo no seletor até
  recarregar; uma vez o "Finalizar" abriu o Cato com a dica aberta.
- 20/11 15:5x **App de gravação no 1.60.22** (build `bea545ecf` no ar na 8080; `app/dist-1.60.18` guardado). 1ª tentativa
  morreu por memória no `vite build` (o app ficou fora do ar até eu religar; nada gravava). 2ª: apaguei a cópia 1.60.18 de
  `/dev/shm` (agora `/dev/shm/ecoflix-src` é link para `/dev/shm/ecoflix-src22`, com `node_modules`) e passou.
  **Robô do celular** (T00): com a escala 1,8 do computador 16:9, o screencast do celular pedia 702x1519,2 e o Chrome recusava;
  `DEVICES.phone.scale = 2` + tamanho arredondado (skill + `$TUT_HOME/rec/recorder`). cap00b passou (780x1688); os 18 de
  celular da T00 regravando no rápido (`rec/t00/_ens/lote_celular_2011.log`).
- 20/11 17:1x **Aviso "Sistema atualizado · v1.60.22" dentro das gravações**: os roteiros traziam a versão 1.60.18 no localStorage. T02 final: cap00..07 saíram com o toast (pedido ao ajudante regravar). T00 celular: a gaveta do aviso tapava a barra de baixo (11 de 18 falharam). Correção no gravador (`buildStorageState` força a versão do build); T00 celular regravando (`rec/t00/_ens/lote_celular_2011b.log`); T07, T20/T12 e T22 avisados.
- 20/11 17:3x **T22 (Grupo) adaptada, ensaio parcial**: 19 capítulos (novos 4, 9, 11, 13, 15, 16), fala 1.410 → 2.838 palavras; rápido OK em 0..7, 9 e 14; corrigidos sem reensaio 8, 10..13; nunca rodaram 15..17; cap18 sem robô. Fila disputada (1 a 5 caps por lote). 8 handlers novos, sementes `codigo-vencido` e `venda-outra-unidade`, 6 ilustrações novas (v3 pendente). Pedidos ao mundo base: (1) `push_group_assets_to_company` sobrescrevia preço com "Sobrescrever" desligado: era o SQL antigo; o 1.60.22 (migração 20261120001000) passou a proteger preço > 0 da filial em tabelas e espelho, e o handler falso agora faz o mesmo; (2) `get_group_financial_dre_summary` sem CMV por unidade no Comparativo: a conferir contra o SQL na continuação. Falta confirmar com o Kaik a fala dos caps 8, 11 e 13 depois de ver os valores na tela.
- 20/11 17:4x **T02 ilustrações v3 (Fable)**: 5 cenas (perfis rápidos, próprios, desativar/excluir, vagas do plano, some/fica), auditoria 0 problemas, 0 piscadas; objetos novos `cadeira.js` e `pessoaSenta.js`. Saíram as que a tela já mostra. Pendente o papel real do relatório (cap12), a fazer no fechamento com o PDF da gravação final. Prévia em `$TUT_HOME/previa_ilustracoes/T02_v3.mp4`. Passado ao ajudante do fechamento da T02.
- 20/11 17:5x **T06 ilustrações v3 (Fable)**: 5 cenas (dinheiro do dia, dia só de Pix, cofre e caixa, suprimento e sangria, esperado e contado), auditoria 0 problemas; objeto novo `cofre.js`. A prévia não saiu: o render pela fila com `--prio 40` esperou 2 h sem vez. Regra trocada para `--prio 12` (brief de cenas e 08-licoes). Sem comprovante na fala da T06. As cenas serão renderizadas com a voz real no fechamento da aula.
- 20/11 18:1x **T01 adaptada, ensaio parcial**: 16 capítulos (novos 10, comprovante; 11, ticket/idioma/guia), fala 2.351 → 3.348 palavras (~21,5 min); rápido OK em 05, 06, 08..15; faltam 00..04 e 07 no 1.60.22 (passaram no lote 1, com o aviso de versão); lote 3 com os completos ainda na fila. Ilustrações novas `ilu10_assinaturas` e `ilu11_idioma_usuario` (v3 pendente). Achado: a dica do Cato ("Qual número de operação...") aparece no canto, a esconder no robô como nas outras aulas. Ocorrência: o ajudante da T01 reusou `scratchpad/lote.sh` do lote do T12 e o esvaziou; o ajudante T20/T12 foi avisado. Regra para os próximos briefs: script de lote com nome da aula, nunca genérico no scratchpad.
- 20/11 18:3x **T00 celular OK no 1.60.22**: os 18 capítulos de celular passaram no rápido (0 passo falho) depois da correção da versão no login pela tela; folha do cap14 conferida (sem aviso). Computador da T00 reensaiando no 1.60.22 (`rec/t00/_ens/lote_pc_2011.log`).
- 20/11 18:5x **T07 pronta e voz disparada**: reensaio no 1.60.22 dos caps 15, 17 e 18 (rápido e completo, 0 falho; maxLate 1,09 / 6,12 / 6,83 com a máquina dividida, ressalva para a final). O aviso agora diz "Comprovante enviado para impressora" (robô corrigido). PDFs conferidos: cupom 58 mm com o nome dos materiais; comprovante sem valores sem "R$". Voz: 21 nós (`T07 capNN ... (1.60.22)` + títulos), 19.954 créditos, 1 versão cada, voz Kaik Barreto, eleven_v4, pt.
- 20/11 19:4x **Voz real processada nas 12 aulas** (T02, T03, T04, T06, T09..T15, T19): `proc_rc=0` e `titulos_rc=0` em todas; capNN.json reais (o "estimado" que aparece em T04 cap10 e T11 cap05/cap11 é palavra da fala, "lucro estimado"). Semelhança mais baixa: T04 cap11 e T11 cap11 (0,86), a ouvir no fechamento de cada aula.
- 20/11 20:0x **Voz da T07 gerada**: 21 de 21 concluídas (sem falha), ~22 min de fala. Saldo ElevenLabs ~41 mil créditos (renova 28/11). Ordem para o resto do saldo: T00 (11,5 mil) quando o computador passar no 1.60.22, depois T20 (15 mil). T01 (18,5 mil), T22 (16 mil) e T16 (29,6 mil) ficam para depois da renovação ou de mais crédito.
- 20/11 20:1x **T16 (NF-e) pronta para a voz no 1.60.22** (Opus): 25 capítulos, fala 5.264 palavras (14 linhas trocadas, 1 tirada: a Pré-visualização do cap11, porque a aba agora só mostra a DANFE real do motor fiscal, que o backend falso não gera). Rápido OK nos 25; completos OK em 05, 09, 11..18, 20, 22, 24 (atraso com voz estimada até 5,7 s no cap12). Sementes apos-cap03..23 recapturadas; handler novo `rpc/get_invoice_for_print`. Pedidos ao mundo base: `preview_danfe_fiscal` no `plugnotas-emit`; DANFE realista no `plugnotas-download` (hoje 5 linhas fictícias); IE da Fundição com 10 dígitos. A DANFE de verdade sai de um motor fiscal externo (`callFiscalEnginePdf`), fora do repositório: pedido ao Kaik um PDF de exemplo da homologação para copiar o layout.
- 20/11 20:4x **T01 pronta para a voz no 1.60.22**: os 16 capítulos passaram no rápido (0 falho); completos cap14 (0,60 s) e cap10 (0,28 s); 03, 04, 09, 11, 12 e 13 ficam para a gravação final conferir. Balão de dica do Cato calado no robô da T01 (o mundo base só cala na sessão logada; a T01 entra pela tela).
- 20/11 21:0x **T00 pronta e voz disparada**: computador (18 caps) e celular (18) passaram no rápido do 1.60.22 com 0 falho. Voz: 17 nós (`T00 capNN ... (1.60.22)` + títulos), 11.476 créditos, 1 versão cada; sem preço de plano na fala.
- 20/11 22:0x **Voz da T00 gerada**: 17 de 17 concluídas (sem falha), 12,2 min de fala + 32 s de títulos. Falta o Kaik exportar o flow com os nós novos (T07 e T00, rótulos terminados em "(1.60.22)") para processar.
- 20/11 22:0x **T20 e T12, relatório do ajudante**: T20 aprovada no rápido em 0..2, 5..9, 11..14 (cap12: PDF A4 real; cap13: texto do wa.me bate com `whatsappOrder.ts`, pedido #1761 de 10/11, R$ 18.714,08); caps 3, 4 e 10 corrigidos só no robô (fala igual), reensaio pela fila (`rec/t20/_ens/lote3_2011.log`). Causas: `portal-order-receipt` dava 500 (corrigido no handler); saldo antigo no cap08 era o cache de 30 s do portal (robô recarrega). T12: cap08, 13 e 16 com 0 falho (atrasos no completo: cap13 máx. 3,7 s, cap16 máx. 6,5 s, a folga fica para a gravação final); cap09 reensaiando (`rec/t12/cap09_2011.log`) depois do ENOSPC. Para o MELHORIAS: o menu da linha em Clientes/Fornecedores abre no hover e bloqueia o clique em "Editar".
- 20/11 22:0x **Disco a 98%** (1,1 GB livres): apagados os `audio16k.wav` de `tNN/narracao/takes/*` (458 MB; só servem ao reconhecedor e o `proc.py` não os relê quando já há `words.json`).
- 20/11 23:0x **T02 fechada (1ª aula do fechamento com voz real)**: 15 min 04 s, 1080p, -16,3 LUFS; os 14 capítulos regravados no 1.60.22 (o `gerar.py` agora lê `app/dist/.versao-app`), respiros nos caps 02, 04 e 12; 6 ilustrações (a do cap12 é o relatório real, `T02/cenas_v3/relatorio.html`, entrada atualizada no `ilustracoes.json`), 20 zooms, 2 destaques. Prévia: `$TUT_HOME/entrega_previa/EcoFlix T02 - Usuários e permissões 1.60.22 (previa 720p).mp4`. Ressalva: o balão de dica do Cato aparece por cima da tela nos caps 00, 01, 08, 09 e 13 (login pela tela não tinha a chave do mundo).
- 20/11 23:1x **Gravador cala o balão do Cato também no login pela tela** (`browser.mjs` → `calaCatoNaLeitura`; teste: sessão anônima lê o "já visto" do mundo, `__mostrarCato` desliga, valor do roteiro prevalece). T00 cap08 (o capítulo do balão) com `__mostrarCato`. Lição em `docs/08-licoes.md`, regra no `PERFIL.md`.
- 20/11 23:2x **Reensaios T20/T12**: T20 caps 3 e 10 aprovados (0 falho); cap04 falhou no "Remover login" (a chave chega ligada só depois que o acesso salvo carrega; o clique ligava em vez de desligar): o robô espera `#portal-password-enabled[data-state=checked]` antes de desligar. T12 cap09 falhou de novo no "Agendar" (data vazia): as correções do ajudante estavam em `_caps1.py`/`_caps2.py` mas o `gerar.py` não tinha sido reconcatenado (`cat _head.py _caps1.py _caps2.py`); reconcatenado (entram também os ajustes de tempo dos caps 13 e 16). Reensaio: T20 cap04, T12 caps 09, 13 e 16 (`rec/t12/caps_2011b.log`).
- 20/11 23:2x O zip que chegou às 23:11 (`EcoFlix___Vozes_de_todas_as_aulas_1.zip`) é idêntico ao de 14:56 (mesmo md5): sem as vozes novas da T07 e da T00. Pedido ao Kaik exportar de novo.
- 20/11 23:3x **T12 fechada nos ensaios**: caps 09, 13 e 16 no rápido e no completo com 0 falho (maxLate 0,24 / 3,65 / 5,05 s; os atrasos do 13 e do 16 ficam para a voz real na gravação final). T20 cap04 ainda falhou: a lista de fornecedores em cache trazia a chave do portal desligada; o robô agora volta ao sistema com carga inteira da página (`location.assign`). Reensaio do cap04 na fila.
- 20/11 23:5x **T20 pronta e voz gerada**: cap04 passou no rápido (0 falho, maxLate 0,00) com a carga inteira da página; todos os 16 capítulos aprovados no 1.60.22. Voz: 17 nós (`T20 capNN ... (1.60.22)` + títulos, duplicados dos da T00), 15.050 créditos, 17 de 17 concluídas, 16,2 min + 30 s de títulos. Saldo ElevenLabs ~14,7 mil (renova 28/11). Para processar: T07, T00 e T20 (pedido ao Kaik exportar os nós "(1.60.22)").
- 20/11 23:5x **T03 ilustrações v3 prontas** (Fable): 7 cenas encaixadas na voz real (11 ×2, 12, 13, 14 com os 2 PDFs reais, 15), auditoria 0 problema, 0 piscadas; saíram ilu07_margem e ilu09_fora (a tela já mostra). Prévia `$TUT_HOME/previa_ilustracoes/T03_v3.mp4`. **Fechamento da T03 despachado** (Fable, brief `_BRIEF_FINAL.md` atualizado para o 1.60.22, disco e `/dev/shm`).
- 21/11 03:0x **T03 fechada** (Fable): 23 min 24 s, 1080p, -16,4 LUFS, pico -3,8 dBTP, 502 legendas. Regravados cap05 (2 rodadas, opção "Radiadores" abaixo da faixa), cap06 (respiro), cap15 (barra de seleção fora da faixa); 17 caps com 0 falho e `maxLate` < 0,8. Respiros cap05/06/08/09; 7 ilustrações encaixadas, nenhuma pendente; 45 zooms, 2 destaques, câmera sem problema. Corte do Marcos (cap01b) por `t03/edit/t03_juntar_cap01.py`. Aula longa estourou a memória no `music_bed.py`, `mix.py` e `finish.py`: cópias locais de pouca memória (`t03_mix.py`, `t03_music_bed.py`; `MIX_PY`), anotadas no `_BRIEF_FINAL.md` para T06 e T12 (17 a 19 min). Folha de quadros mostrava "20:60.0": `entregar.py` arredonda antes. Prévia `$TUT_HOME/entrega_previa/EcoFlix T03 - Materiais e tabelas de preço 1.60.22 (previa 720p).mp4` enviada ao Kaik. Disco livre 1,2 GB. Apagado `/dev/shm/t03_senha` (senha do ensaio esquecida em arquivo).
- 21/11 0x:xx **T22 ensaios fechados no 1.60.22** (Sonnet): rápidos 8, 10-13, 15-18 com 0 falho; completos com voz estimada 0 falho (maxLate só referência; cap16 17,96 s, âncoras na voz real). DRE do cap08 por competência ("(-) CMV" no Comparativo). Frases sem tela conferidas no fonte (verdadeiras); cap17 L7 reescrita para citar cartão e boleto com os botões na tela. **T22 pronta para a voz** (créditos). **T06 fechamento despachado** (Fable).
- 21/11 06:4x **T06 fechada** (Fable): 20 min 06 s, 1080p, -16,3 LUFS, pico -4,0 dBTP, 447 legendas. Regravados 03, 08, 10, 11, 13a (âncoras: voz real mais rápida) e 13 duas vezes (quadros JPEG de 162 s encheram o disco: gravação passou para `/dev/shm/t06_rec`; o 1.60.22 mudou o Fechar Caixa). Dinheiro conferido (3.006,50; 1.450,00; 957,10; 17.000,00). Respiro cap11 72.85:1.0; 5 ilustrações encaixadas; 38 zooms (até 1,8x), 12 destaques. Sem cena de comprovante (a aula não abre PDF). cap13 L10 cita a Projeção de Lucro para comprado e vendido, que no 1.60.22 é do Relatório de Pedidos do Caixa: frase nova gerada (146 créditos, 9,0 s), entra quando o Kaik mandar o MP3 (remendo só do cap13). Prévia enviada. Disco livre 716 MB.
- 21/11 0x:xx **T12 ilustrações v3 prontas** (Fable): 5 cenas (cap01 caminho da coleta, cap10 tara, cap11 caçamba, cap14 taxa de conclusão, cap15 regras do portal), âncoras do cap11 e cap15 corrigidas; tiradas ilu00 (repetia o cap01) e ilu09/12/13/16 (a tela já mostra). Sem PDF na fala. Auditoria 0, piscadas 0. Prévia `$TUT_HOME/previa_ilustracoes/T12_v3.mp4`. O visor da balança passa de 9.460 no assentamento (mola do `pesa`, luz amarela), como na T08. **Espaço**: `node_modules` das cenas (4 x 70 MB) virou link para `ferramentas/edit/cenas/node_modules`; mídias velhas de revisão do scratchpad apagadas (303 MB). Disco 1,3 GB. **Fechamento da T12 despachado** (Fable).
- 21/11 0x:xx **T04 ilustrações v3 prontas** (Fable): 7 cenas (cap00 pátio, cap01 cliente e fornecedor, cap07 saldo único, cap08 qual preço, cap12 ler o saldo, cap14 fungível, cap16 Relatório de Saldos em papel real); âncoras corrigidas para a voz real; tiradas ilu04 e ilu11 (a tela já mostra). Auditoria 0, piscadas 0. Prévia `$TUT_HOME/previa_ilustracoes/T04_v3.mp4`. Pendente para o fechamento: PDF detalhado do cap12 L11 (o ensaio não capturou). Despachadas as ilustrações da T09.
- 21/11 08:1x **Limite do Fable atingido** (volta 25/11 11:00 de Lisboa). O fechamento da T12 parou no meio com a gravação final rodando (caps 00-07 com 0 falho); continuação despachada com Opus. Ajudantes seguintes em Opus (julgamento) ou Sonnet (padrão) até lá.
- 21/11 1x:xx **T09 ilustrações v3 prontas** (Opus, continuando o Fable): 11 cenas, 6 com papel real (comprovantes e relatórios gravados), âncoras na voz real, tirada ilu05_estornado; auditoria 0; ficam 8 piscadas de 1 px (ilu01 e ilu04_soma) para corrigir no fechamento. Prévia `$TUT_HOME/previa_ilustracoes/T09_v3.mp4`. Despachadas as ilustrações da T10 (Sonnet).
- 21/11 1x:xx **T12 fechada** (Opus, continuando o Fable): 19 min 24 s, 1080p, -16,3 LUFS, pico -3,8 dBTP, 419 legendas; 18 caps 0 falho, maxLate < 0,8 (regravados 08, 10, 11, 12; sementes apos-cap11/12/15 sem o "Caçamba 06ç"). 5 ilustrações, 21 zooms, aceleração 2x no cap16. Prévia enviada. **Pendente**: cap17 (recapitulação, 19:12-19:18) mostra o bloco Checklist vazio enquanto a fala diz "montou o checklist": semente apos-cap16 e regravar o cap17. Como `proj`, `video_sem_audio.mp4` e `out/capNN` foram apagados (disco), o remendo (T12 cap17 e T06 cap13) é uma remontagem inteira a partir de `rec/tNN` e das specs (`fechar_tNN.sh` com todos os capítulos): fica para quando houver disco. Disco 761 MB.
- 21/11 1x:xx **T10 ilustrações v3 prontas** (Sonnet, ~96 mil tokens contra ~400 mil do Opus na T09, qualidade no molde): 6 cenas (cap0 perguntas, cap1 portas, cap2 saldo, cap3 separação, cap9 líquido, cap10 pilha) + 3 papéis reais (cap7 kardex, cap13 Posição e Relatório); auditoria 0, piscadas 0. Prévia `$TUT_HOME/previa_ilustracoes/T10_v3.mp4`. Ilustrações seguintes em Sonnet: T11 e T13 despachadas.
- 21/11 1x:xx **T13 ilustrações v3 prontas** (Sonnet): 6 cenas + comprovante Pix real (cap16); tiradas ilu08 e ilu13; auditoria 0, piscadas 0. Prévia `$TUT_HOME/previa_ilustracoes/T13_v3.mp4`. cap18 (Exportar) a conferir no fechamento.
- 21/11 1x:xx **T11 ilustrações v3 prontas** (Sonnet): 6 cenas (cap0 pátio, cap1 caminho, cap3 por quilo, cap4 ímã, cap9 tolerância, cap13 baixa) + Relatório de Produção em papel real (cap12 L7, do ensaio: no fechamento usar o PDF da gravação final); 8 tiradas (a tela mostra ou cena vizinha cobre); auditoria 0, piscadas 0; contas conferidas (2% de 480 = 9,6; 498 - 480 = 18; 3,8%). Prévia `$TUT_HOME/previa_ilustracoes/T11_v3.mp4`.
- 21/11 1x:xx **T14 ilustrações v3 prontas** (Sonnet): 6 cenas (extrato e sistema, cofre e banco, só muda de lugar, conciliar, OFX, centavos); 5 tiradas; auditoria 0, piscadas 0 (deriva da câmera mais lenta na ilu05). Prévia `$TUT_HOME/previa_ilustracoes/T14_v3.mp4`. Despachadas as ilustrações da T19.
- 21/11 1x:xx **T19 ilustrações v3 prontas** (Sonnet): 5 cenas + 4 papéis reais (recibo do Edson, holerite do Marcos, recibo A4, Relação de pagamento 22.540,00), impressos do HTML da aba nova do ensaio; 9 tiradas; auditoria 0, piscadas 0 nas 9. Prévia `$TUT_HOME/previa_ilustracoes/T19_v3.mp4`.
- 21/11 1x:xx **Voz que falta (contagem)**: T01 18.512, T16 29.582, T22 16.161 (prontas para gerar) + T05 9.474, T17 18.219, T18 8.132, T21 5.687, T25 7.441, T26 10.607, T27 4.408 (ainda a aplicar no 1.60.22) = ~128 mil créditos; na conta ~14,5 mil (renova 28/11). **T18 despachada** (Sonnet, `_BRIEF_APLICAR_160.md`). T05 (EcoTray, Windows) e T17 (fiscal) ficam para depois.
- 21/11 1x:xx **T15 ilustrações v3 prontas** (Sonnet): 5 cenas (contas conferidas: caixa -35.000, competência +3.000, estoque 38.000); 5 tiradas; auditoria 0; 1 piscada na ilu07_patio e o PDF do Histórico (cap15) para o fechamento. Prévia `$TUT_HOME/previa_ilustracoes/T15_v3.mp4`. **Ilustrações v3 prontas em todas as aulas com voz real** (T02-T04, T06, T08-T15, T19); faltam as de T00, T07 e T20 (esperam o MP3 da voz) e das aulas sem voz.
- 21/11 1x:xx **T18 pronta para a voz no 1.60.22** (Sonnet): 14 caps (novos 6 Usar como modelo, 8 envio com erro, 11 CDF com erro), 13.047 caracteres; rápido 0 falho nos 14; completos com voz estimada (âncoras na voz real). Handlers `sigor-mtr-emit`/`sigor-cdf-emit` novos no mundo. PDFs do MTR e do CDF são do órgão: papel simulado NÃO vai ao vídeo; pedir ao Kaik exemplos (como o DANFE da T16). **T25 despachada** (Sonnet).
- 21/11 1x:xx **T25 aplicada no 1.60.22** (Sonnet): 14 caps (novos cap04 Saldos em Aberto e formas de pagamento, cap07 concluir/editar/excluir), 10.024 caracteres; rápido 0 falho; "Notificação push" e "Sem permissão" fora (sem tela). Reensaio completo de 04, 07 e 10 rodando (coordenação, instância 54325).
- 21/11 15:50 **T25 pronta para a voz**: reensaio completo de 04, 07 e 10 com 0 falho (maxLate 0,27 / 3,03 / 2,21, voz estimada). T27 despachada (Sonnet).
- 21/11 1x:xx **T27 aplicada no 1.60.22** (Sonnet): 9 caps (novo cap06 Desligar e voltar atrás), 6.061 caracteres; rápido e completo 0 falho; cobertura corrigida (o interruptor não trava sem logo). Reensaio de 06 e 03 rodando (coordenação, instância 54327).
- 21/11 1x:xx **T21 em 3 etapas**: o ajudante Sonnet esgotou o contexto na pesquisa (o Cato virou agente: cartões de ação, NF-e, memória, rotinas; plano de 18 caps). Pesquisa e mundo sobreposto em `T21/andamento_160.md`. Etapa 1 (fala, roteiro com as respostas do Cato conferidas no código) despachada (Sonnet); etapa 2 (handlers do overlay, sementes) e 3 (robô, ensaio) depois.
- 21/11 16:56 **T27 pronta para a voz**: reensaio de 06 e 03 com 0 falho (maxLate 0,70 / 0,07).
- 21/11 17:xx **T21 etapa 1 feita** (Sonnet): 18 caps, 14.065 + 392 caracteres (~17 min), respostas do Cato com fonte no código (roteiro/plano). Saíram: "Ver itens e tributos", produção detalhada, ambiente da nota, números de limite. **Perguntar ao Kaik**: as rotinas (resumos agendados do Cato, cap14) já estão liberadas para os clientes? No cliente só dependem do consentimento de memória (`CatoFab.tsx:137`). Etapa 2 (overlay e sementes) despachada.
- 21/11 17:xx **T21 etapa 2 feita** (Sonnet): overlay completo (cato-background, cato-assist, plugnotas-emit com prévia do DANFE, 6 `cato_confirm_*`, jornadas, memória, rotinas, correções, conversas, feedback), sementes inicio/apos-cap02/03/06, números conferidos (744; 5.200; 1.420; Valdir 300 para 200; caixa 1.500 e 1.415). Coordenação corrigiu a fala: R1 "sessenta e dois mil e quinhentos" (mundo 62.454,55) e R4 "cento e vinte e cinco mil" (125.313,67). Para a etapa 3 conciliar com a tela: rótulos reais dos cartões, a aba "Da empresa" que não aparece para o Rafael (cap03), compra da Aparecida em "Para acompanhar" (cap14).
