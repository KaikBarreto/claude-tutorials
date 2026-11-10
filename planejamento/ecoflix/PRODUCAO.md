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
1. **Agora (10/11 00:3x)**: 17 agentes de roteiro (26 aulas, `_BRIEF_ROTEIRO.md`) e 3 de estrutura: Ferramentas
   (melhorias da Domiflix na skill, branch `consolidacao-domiflix`), Mundo (EcoSistema 1.59.154 no Supabase falso, mundo
   da Recicla Vale Metais, EcoTray falso; branch `ecoflix-mundo`), Marca (vinheta, cartela, cartões e kit de ilustração;
   branch `ecoflix-marca`, prévia em `/home/claude/ecoflix/previa_marca/`).
2. Juntar: conferir os roteiros (tom, precisão, ilustrações), juntar os branches no main, consolidar no
   `MUNDO_FICTICIO.md` e nas sementes o que cada aula pediu, handlers do que faltar.
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
