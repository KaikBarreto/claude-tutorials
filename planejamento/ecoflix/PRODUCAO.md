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
| T20 | afdb1a0ff5d8d10fb | rápido cap03-cap10 e cap00/cap01 com MP4; completo dos caps 4-8 | `bash rec/t20/t20_fila.sh --rapido 3 4 5 6 7 8 9 10 0 1` |
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
