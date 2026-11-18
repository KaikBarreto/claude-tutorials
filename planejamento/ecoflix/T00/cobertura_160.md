# Cobertura 1.60.10 · T0 Bem-vindo ao EcoSistema

Auditoria de 18/11/2026, só leitura de código. Base: `/dev/shm/ecoflix-src` (1.60.10) contra o roteiro (1.59.154), diff
`f37573ea0..5290be4cd`. Caminhos relativos a `src/`, linhas do 1.60.10. `RT` = `config/routes.ts`, `FAB` =
`components/cato/CatoFab.tsx`, `AL` = `components/layout/AppLayout.tsx`, `MBN` = `components/layout/MobileBottomNav.tsx`,
`MMC` = `components/billing/ModulesManagementCard.tsx`, `CSM` = `components/billing/CancelSubscriptionModal.tsx`,
`PHL` = `components/shared/PaymentHistoryList.tsx`, `EW` = `pages/EcoFlixWatch.tsx`.

**Resumo.** A aula quase não quebrou: a varredura do robô no app novo (`rec/varredura/t00.txt`) passou os 14 capítulos
com zero passo falho. O que muda é o **mapa**: o menu fiscal ganhou "Relatórios Fiscais", e o Cato (botão flutuante que
já estava em todas as telas gravadas, mas que o roteiro nunca cita) virou agente e passou a soltar um **balão de dica**
sozinho depois de 15 s. O resto é lacuna de cobertura antiga, principalmente na Assinatura (a T24 foi absorvida aqui e
os fluxos "Gerenciar plano" e "Cancelar assinatura" só são apontados, nunca abertos).

**Mudaram** entre as versões (das telas desta aula): `RT`, `FAB`, `AL`, `MBN`, `MMC` (12 linhas),
`components/settings/SettingsUsabilityContent.tsx` (fora do quadro da aula), `components/ecoflix/EcoFlixIntroGate.tsx`
(sem efeito visual: uma falha de carregamento deixou de travar o sistema, `:126-129`), `PHL` (o que entrou é a visão
administrativa; a do cliente segue em carrossel), `components/cato/CatoInviteModal.tsx`.
**Sem mudança nenhuma**: `pages/Billing.tsx`, `AccountUsageCard.tsx`, `CSM`, `UserLimitModal.tsx`, `pages/Checkout.tsx`,
`PixPaymentView.tsx`, `lib/billing/subscriptionChange.ts`, toda a EcoFlix (`pages/Tutoriais.tsx`, `EW`, `EcoFlixLayout`,
`EcoFlixTrackPanel`, `EcoFlixLessonDetails`, `EcoFlixModuleOffer`, `EcoFlixModuleBadge`), `SidebarMenuContent.tsx`,
`TopNavbar.tsx`, `MoreMenuDrawer.tsx`, `SettingsAppearanceContent.tsx`, `pages/Profile.tsx`, `SupportTriageDialog.tsx`,
`HelpCenterSheet.tsx` (só os artigos), o Dashboard e o catálogo de módulos (`lib/moduleUpsellCopy.ts`: os mesmos 8
módulos pagos mais o Kit Básico e o Gerencial). **Não há módulo novo no 1.60.10**: as novidades do mapa são o Cato
agente (1.60.0) e a tela "Relatórios Fiscais".

## 1. Mudou no app (por capítulo)

**Todos os capítulos gravados dentro do sistema (02, 04, 06 a 12)**
- **M1. Balão de dica do Cato (novo).** Com a tela parada 15 s, sobe um balão escuro ao lado do botão do Cato com uma
  frase sorteada e o link **"Abrir Cato"**; o xis tem o nome "Fechar dica do Cato"; some sozinho em 11 s
  (`FAB:24-27,244-278,295-305`). Fica em cima do canto inferior direito (no celular, à esquerda, acima da barra:
  `bottom-36 left-4`). Depois dele o botão ganha uma bolinha vermelha **"1"** e o nome "Abrir 1 notificação do Cato"
  (`FAB:332,384-388`). A varredura confirma: 7 chamadas a `track_cato_adoption_event` (`nudge_shown`, `n42_geral`), ou
  seja, o balão subiu em 7 capítulos, com a frase 42: "Qual número da operação você quer entender agora?" (`FAB:70`).
  Nas cenas longas da Assinatura ele cobre "Gerenciar plano" e o "Histórico de Pagamentos". Precisa calar na semente
  (ver Proposta, "Mundo") e aparecer só no trecho novo do Cato.
- **M2. Risco de barra vermelha no topo.** O aviso do certificado passou a consultar a RPC `fiscal_onboarding_status`
  (61 chamadas sem handler na varredura) e a tabela `dfe_certificate_notice_opt_outs` (desconhecida). Hoje a barra não
  aparece porque a RPC falha; se o handler novo devolver certificado não pronto, sobe em **todas as telas** a barra
  "Reenvie seu certificado A1 para continuar emitindo notas" com "Reenviar certificado agora" e "Não mostrar
  novamente" (`components/notifications/DfeCertificateNoticeBanner.tsx:124-153`, montada em `AL:429`; regra em
  `hooks/useCertificateInfo.tsx:262-269`). Vale para a trilha inteira, não só para a T0.

**cap06 · Um passeio pelo menu**
- **M3.** "Fiscal & Ambiental" agora tem **7 itens**: entrou **"Relatórios Fiscais"** no fim (`RT:511`, rota
  `/fiscal-ambiental/relatorios/nfe`) e "Estoque Fiscal" passou a abrir em `/fiscal-ambiental/estoque-fiscal/posicao`
  (`RT:510`). Ordem na tela: "Notas Fiscais (NF-e)", "SPED Fiscal" (selo "BETA", só com a função ligada), "Notas de
  Serviço (NFS-e)", "Transporte (MDF-e)", "Ambiental (MTR/CDF)", "Estoque Fiscal", "Relatórios Fiscais"
  (`RT:505-511`). O roteiro não abre o grupo, então a gravação não quebra, mas o mapa falado ("as notas fiscais e os
  documentos ambientais") fica curto. O inventário (seção 4) precisa da linha nova.

**cap07 · Os menus e a sua conta (celular)**
- **M4.** O leque do botão "Novo" mudou de desenho: duas fileiras ("Compra" e "Venda" embaixo, "Ticket de pesagem" e
  "Nota Fiscal" em cima; `MBN:63-68`); enquanto ele está aberto o botão do Cato some (`AL:295,540`, `FAB:352`);
  "Nota Fiscal" só aparece para quem pode emitir NF-e (`MBN:139-145`); e a barra de baixo sai da tela quando o teclado
  sobe (`MBN:198-204`). O roteiro não abre o leque; se a proposta P7 for aceita, as coordenadas são as novas.

**cap11 · Quando a empresa cresce**
- **M5.** "Gerenciar plano" agora sempre reabre a partir da assinatura vigente: descarta o que foi mexido e fechado
  sem aplicar, volta o nível de notas e o ciclo para os atuais e, no plano Personalizado, já abre no montador
  (`MMC:331-343`). O roteiro não abre a janela; importa para a proposta P9.

**cap12 · Formas de pagamento**
- **M6.** O histórico ganhou dois selos de cobrança: **"Substituído"** e **"Expirado"** (`PHL:290-293`). No mundo da
  aula todos os cartões são "Pago": sem efeito na gravação. Continua valendo o achado antigo de `propostas_fala.md`:
  pagamento de origem Asaas se chama "Cobrança • {empresa}", só o tipo `renovacao` vira "Renovação" (`PHL:249-254`).

**cap02 · a trilha (dado, não código)**
- **M7.** O cartão da T21 no catálogo da trilha (`rec/t00_catalogo.mjs:30`) diz "Cato, o assistente" / "O assistente
  do EcoSistema para tirar dúvidas e consultar números.". Se a T21 for reescrita como agente (ver
  `T21/cobertura_160.md`), título e descrição mudam aqui também.

**Fora do quadro, sem ação:** Usabilidade ganhou o campo "Quem assina" abaixo de "Assinaturas no comprovante"
(`SettingsUsabilityContent.tsx:897-925`, assunto da T1); o bloco "Nomenclatura de clientes e fornecedores" do cap08
está igual, agora em `:466-492`. O convite do Cato trocou "só consulta e não altera nada" por "Além de consultar, ele
prepara ações..." (`CatoInviteModal.tsx:123-127`); o Rafael já viu o convite, não aparece.

## 2. Falta cobrir

| # | O que é (código) | Quando o cliente usa | Vale? |
|---|---|---|---|
| F1 | **Cato**: botão redondo fixo no canto (computador: inferior direito; celular: inferior esquerdo, acima da barra), nome "Abrir o Cato" (`FAB:332,341-345`); abre o painel "Cato.ai — agente de IA da EcoSistema" com "Oi, Rafael 👋", "Pergunte o que quiser sobre seu negócio", "Sugestões para começar" e o campo "Pergunte ao Cato…" (`components/cato/CatoChatPanel.tsx:968,1189-1196,1645`). Só para empresa com o Cato ligado e usuário com "Usar o Cato (assistente de IA)" (`AL:283`, `RT:309`); sem isso, o canto mostra o atalho do suporte (`AL:531-545`) | Todo dia, em qualquer tela | **Sim, capítulo novo curto** (P3). Como perguntar, ações, anexos, NF-e e memória: **T21** |
| F2 | Submenu "Fiscal & Ambiental" com "Relatórios Fiscais" (M3) | Para achar as telas fiscais | **Sim, trecho** (P1). Conteúdo: T16, T17 (Relatórios Fiscais), T18 |
| F3 | Cabeçalho: botão "Buscar..." (Ctrl + K, "Buscar páginas, clientes, fornecedores, materiais, funcionários...", `components/CommandPalette.tsx:444,601-618`) e o sino "Notificações" (`components/notifications/NotificationsBell.tsx:218`) | Achar uma tela ou um cadastro sem passar pelo menu; ver avisos | **Só citar** (P2). A busca é da T25 |
| F4 | Menu da conta: "Trocar de conta" no cartão do fim (`SidebarMenuContent.tsx:759-763`), botão "Sair" (`:824`) e a terceira opção de "Tema", "Sistema" (`:698-728`) | Quem tem mais de uma empresa; fim do expediente | **Só citar** (P6) |
| F5 | "Falar com o Suporte" abre "Falar com o suporte": "Em qual tela/módulo? *", a descrição, "Você já assistiu aos nossos tutoriais sobre isso? *" (Sim / Não) e "Falar no WhatsApp", apagado até preencher (`SupportTriageDialog.tsx:297-365,405`) | Quando trava em alguma tela | **Sim, trecho** (P6): a fala atual diz só "chama o suporte" |
| F6 | "Central de Ajuda": gaveta com "Pesquisar artigos..." e, no fim, "Ainda tem dúvidas?" (`HelpCenterSheet.tsx:196-268`) | Dúvida rápida por escrito | **Sim, 1 gesto** (P6): hoje é só destaque no item |
| F7 | Celular, botão "Novo": "Compra", "Ticket de pesagem", "Nota Fiscal", "Venda" (`MBN:41-46`) | Começar um lançamento pelo celular | **Sim, trecho** (P7): a fala cita só compra e venda |
| F8 | EcoFlix, alto da tela: "Início", "Módulos", "Lives", "Minha Lista" e a busca "Buscar títulos..." (`EcoFlixLayout.tsx:283-292,339`); na trilha, "Buscar aula" (`Tutoriais.tsx:571`) | Achar uma aula pelo nome; guardar para depois | **Só citar** (P4) |
| F9 | Player da aula: "Legendas" (faixa, "Tamanho da legenda", "Estilo da legenda"), "Velocidade", "Episódios", "Próxima aula", "Abrir em tela cheia", "Voltar 10 segundos" / "Avançar 10 segundos" (`EW:810-903,2147-2323,2738`); no fim, o quadro "Aula concluída" · "Vamos para a próxima" · "Próxima aula agora" (`EW:665-694`); nos detalhes, "Materiais e extras" (`EcoFlixLessonDetails.tsx:91`) | Em toda aula | **Sim, trecho** (P5): é a aula que ensina a usar a trilha |
| F10 | Selo "Liberado no teste" para módulo fora do plano durante o teste (`EcoFlixModuleBadge.tsx:23-29`) | Cliente em teste olhando a trilha | **Só citar** (P4, 1 frase no cap03) |
| F11 | Assinatura no teste: a tela mostra só "Ative sua Assinatura" e "Escolher Plano e Ativar" (`Billing.tsx:365-418`, `i18n/locales/pt-BR/billing.json:105,110`) | Cliente em teste que abre Assinatura | **Sim, 1 linha** (P8): a maioria vê esta aula no teste e a tela dela é outra |
| F12 | Selos de status "Vence em breve" (7 dias ou menos) e "Vencida" / "Vencida há {n} dias" (`billing.json:118-124`) | Perto e depois do vencimento | **Sim, ilustração** (P8) |
| F13 | Nível de notas: "· Nível {n}" ao lado do módulo de notas em "Módulos ativos" (`MMC:507`) e o limite em "Notas fiscais este mês" (`AccountUsageCard.tsx:115`) | Quem emite muita nota | **Só citar** (P8) |
| F14 | "Adicione ao seu plano": aparece quando falta módulo, um cartão por módulo com chamada e botão próprio (CRM: "Ativar meu CRM"; padrão "Contratar") (`MMC:517-570`, `lib/moduleUpsellCopy.ts:48-53`) | Contratar um módulo direto da Assinatura | **Sim, trecho** (P10), com o estado S3 que já existe |
| F15 | **"Gerenciar plano" → "Montar plano"**: "Monte seu plano e veja como fica ao vivo"; "Escolha os módulos", "Nível de Notas Fiscais", "Usuários adicionais"; resumo "Seu plano" com "Mensal" / "Anual" e "Total mensal"; "Voltar aos planos", "Plano atual", cartão "Personalizado" ("Escolha módulo por módulo e monte o plano do seu jeito"); botão "Ver valor e aplicar" (anual: "Ver valor do anual") → "Confirmar mudança de plano" · "Confira o valor antes de confirmar" (`MMC:672-676,684,759-764,784,836-867,898,951-953,966,1020,1067,1132`; `SubscriptionChangeConfirmDialog.tsx:55,89`) | Ligar módulo, mudar nível de notas, somar usuário, passar para o anual | **Sim, capítulo novo** (P9): é a função central da tela e hoje é só um destaque |
| F16 | **"Cancelar assinatura"**: "Cancelar Assinatura" · "Nos ajude a entender o motivo" · "Motivo do cancelamento" (8 motivos) · "Falar com o Sucesso do Cliente" · "Continuar" → "Confirmar cancelamento" · "Ao confirmar:" (5 itens) · "Confirmar Cancelamento" (`CSM:29-36,348-356,411-484`) | Quando pensa em sair | **Sim, trecho** (P11), sem confirmar |
| F17 | Nota da assinatura: além de "Baixar PDF", "Baixar XML", "Solicitar Nota Fiscal" e "Nota disponível após o pagamento" (`PHL:459,494,504,547`) | Contador pede o XML; nota que ainda não saiu | **Só citar** (P12) |
| F18 | Sem permissão: "Pagar Agora" com cadeado ("Você não tem permissão para gerenciar assinatura") e "Peça ao administrador da empresa para alterar o plano." (`Billing.tsx:572-590`, `billing.json:111`, `MMC:586-588`) | Funcionário abrindo a tela | **Não**: a dica do cap09 já fala; mostrar exigiria outro usuário (T2) |
| F19 | Checkout de verdade depois de "Pagar Agora" (`/checkout?mode=renewal`) | Na hora de pagar | **Não** nesta rodada: a tela inteira é valor em reais; a ilustração do cap12 cobre. Depende de decisão (ver fim) |
| F20 | Submenus de "Coletas & Logística" (7 telas) e "Gerencial (Filiais)" (5 telas) (`RT:526-552`) | Quem tem os módulos | **Não**: T12 e T22 |

## 3. Proposta

Regra mantida: nenhum valor em reais na fala nem em zoom. As janelas de plano e de cancelamento mostram valores na tela;
a câmera passa sem parar neles.

**P1 · cap06, trocar a linha de "Fiscal & Ambiental"**

| Tela | Fala |
| --- | --- |
| Clique em "Fiscal & Ambiental" (o "Financeiro" fecha sozinho): abrem "Notas Fiscais (NF-e)", "Notas de Serviço (NFS-e)", "Transporte (MDF-e)", "Ambiental (MTR/CDF)", "Estoque Fiscal" e "Relatórios Fiscais"; o destaque desce pelos itens e para no último. [TESTAR: "SPED Fiscal" com o selo "BETA" só aparece com a função ligada; a fala não cita] | Em Fiscal & Ambiental ficam as notas fiscais de mercadoria e de serviço, o transporte, os documentos ambientais, o estoque fiscal e os relatórios fiscais. |

**P2 · cap06, linha nova depois do rodapé "Configurações"**

| Tela | Fala |
| --- | --- |
| Destaque no botão "Buscar..." e no sino "Notificações", no alto à direita (sem abrir). | No alto da tela ficam a busca, que acha uma tela, um cliente ou um material pelo nome, e o sino com os avisos. |

**P3 · capítulo novo "O Cato, o seu agente" (vinheta: O SISTEMA), entre o cap07 e o cap08**

| Tela | Fala |
| --- | --- |
| Capítulo novo (S2), no Dashboard. Destaque no botão redondo do canto inferior direito (nome "Abrir o Cato"). | E esse botão redondo, no canto da tela? É o Cato, o agente de inteligência artificial do EcoSistema. Ele acompanha você em todas as telas. |
| Clique no botão: o painel abre à direita com "Oi, Rafael 👋", "Pergunte o que quiser sobre seu negócio", as "Sugestões para começar" e o campo "Pergunte ao Cato…" (sem enviar nada). | Você pergunta do seu jeito, escrevendo ou falando, e ele responde com os números da sua empresa: o caixa, o estoque, as contas, as notas fiscais. |
| [ILUSTRAÇÃO, no tema escuro do Cato (`perfis/ecoflix/cenas/cato/`): um pedido falado "Lance uma compra de 100 kg de ferro" vira um cartão de resumo com o botão "Confirmar"; só depois do clique o cartão ganha o visto] | E ele não só responde. O Cato prepara uma compra, uma venda, um ticket de pesagem ou um reajuste de preço, e mostra um resumo pra você conferir. Nada é lançado sem a sua confirmação. |
| De volta à tela, painel fechado (xis "Fechar"); o balão de dica sobe ao lado do botão, com "Abrir Cato" (a única cena em que o balão fica ligado). | De vez em quando ele manda uma dica, num balão ao lado do botão. É só clicar pra abrir, ou fechar no xis. |
| Destaque no botão, com a bolinha "1". | Quem libera o Cato pra cada usuário é o administrador. E ele tem uma aula só dele, mais pra frente na trilha. |

No vertical: o botão fica embaixo à esquerda, acima da barra, e o painel ocupa a tela inteira.

**P4 · cap02 e cap03, uma linha em cada**

| Tela | Fala |
| --- | --- |
| cap02, depois de "Aqui estão todas as aulas": destaque nas abas "Início", "Módulos", "Lives" e "Minha Lista" e na busca. [TESTAR: abas visíveis na página da trilha no S2] | No alto, dá pra buscar uma aula pelo nome, e em Minha Lista ficam as aulas que você guardou pra ver depois. |
| cap03, depois da primeira linha: sem tela nova (mesmo quadro do selo). | No período de teste, o selo é outro: Liberado no teste. |

**P5 · cap04, três linhas antes do botão do suporte**

| Tela | Fala |
| --- | --- |
| Na aula "Sua conta e sua empresa", o mouse sobre o player: abre "Legendas" ("Tamanho da legenda"), depois "Velocidade"; destaque em "Voltar 10 segundos", "Avançar 10 segundos" e "Abrir em tela cheia". [TESTAR: os controles com o vídeo local fictício] | No player, dá pra ligar a legenda e escolher o tamanho dela, mudar a velocidade, voltar ou avançar dez segundos e abrir em tela cheia. |
| [BACKEND: vídeo fictício curto até o fim] O quadro "Aula concluída" · "Vamos para a próxima" com o botão "Próxima aula agora" (sem clicar). | Quando a aula termina, o sistema marca como concluída e já oferece a próxima. |
| A câmera desce até "Materiais e extras". | Embaixo, em Materiais e extras, ficam os arquivos da aula, quando tem. |

**P6 · cap07, trocar as linhas 2 e 3 e somar uma**

| Tela | Fala |
| --- | --- |
| Destaque em "Meu Perfil", "Assinatura" e "Tema" (abre "Claro", "Escuro", "Sistema"). | No seu perfil, você troca a foto, o nome e a senha. Em Assinatura, acompanha o seu plano. Em Tema, escolhe a tela clara, a escura ou a mesma do seu aparelho. |
| Destaque em "Tutoriais \| EcoFlix"; clique em "Central de Ajuda": a gaveta com "Pesquisar artigos..."; fecha. Clique em "Falar com o Suporte": "Falar com o suporte", com "Em qual tela/módulo? *", a descrição e "Você já assistiu aos nossos tutoriais sobre isso? *"; destaque em "Falar no WhatsApp" (apagado); fecha sem enviar. | Em Tutoriais EcoFlix, você volta pra trilha. Na Central de Ajuda, pesquisa a resposta por escrito. E em Falar com o Suporte, você diz em qual tela está e o que aconteceu, e a conversa já abre no WhatsApp com tudo isso. |
| Destaque no cartão do fim do menu da conta ("Trocar de conta") e no botão "Sair", ao lado de "Configurações". [TESTAR: o que o cartão mostra com uma conta só] | No fim do menu dá pra trocar de conta, pra quem tem mais de uma empresa. E o botão Sair fica ao lado das Configurações. |

**P7 · cap07, linha do celular**

| Tela | Fala |
| --- | --- |
| [CELULAR] Como hoje, mais um toque em "Novo": o leque com "Compra", "Ticket de pesagem", "Nota Fiscal" e "Venda" (o botão do Cato some enquanto o leque está aberto); toque fora fecha; depois "Menu". | No celular, o menu fica embaixo: Início, Caixa, o botão Novo, pra começar uma compra, uma venda, um ticket de pesagem ou uma nota fiscal, Estoque e o Menu, com todas as áreas e a sua conta. |

**P8 · cap09 e cap10, três linhas**

| Tela | Fala |
| --- | --- |
| cap09, depois da primeira linha. Corte para o estado S1 (teste): a tela "Assinatura" só com "Ative sua Assinatura" e "Escolher Plano e Ativar" (sem clicar). | Ainda está no período de teste? Aí esta tela mostra só o convite pra escolher o plano e ativar. |
| cap09, depois da linha do vencimento. [ILUSTRAÇÃO: os três selos lado a lado, "Ativa", "Vence em breve" e "Vencida", sobre uma régua do mês; cada um acende na sua palavra] | Faltando poucos dias, o selo muda pra Vence em breve. Passou do vencimento, vira Vencida. |
| cap10, depois da primeira linha: destaque em "· Nível 1" ao lado do módulo de notas, em "Módulos ativos". | No módulo de notas fiscais aparece também o nível, que é a quantidade de notas que dá pra emitir por mês. |

**P9 · capítulo novo "Montar o plano" (vinheta: ASSINATURA), no lugar da primeira linha do cap11; as ilustrações da régua, dos aparelhos e do "Sua equipe cresceu!" seguem depois**

| Tela | Fala |
| --- | --- |
| Capítulo novo (S2), em "Assinatura"; clique em "Gerenciar plano": abre "Montar plano" · "Monte seu plano e veja como fica ao vivo", já no montador. | E quando a empresa cresce, o plano cresce junto. Clicando em Gerenciar plano, abre o Montar plano. |
| A câmera percorre a esquerda: "Escolha os módulos", "Nível de Notas Fiscais" e "Usuários adicionais"; depois o resumo "Seu plano", à direita (sem zoom no "Total mensal"). | De um lado, você escolhe os módulos, o nível de notas fiscais e os usuários adicionais. Do outro, o resumo do seu plano vai se atualizando. |
| Destaque na chave "Mensal" / "Anual" (sem trocar); clique em "Voltar aos planos": a lista com o selo "Plano atual" e o cartão "Personalizado". | Dá também pra trocar entre mensal e anual, ou voltar e escolher um plano pronto. |
| Destaque no botão "Ver valor e aplicar" (sem clicar). | Nada muda enquanto você não clicar em Ver valor e aplicar. Aí o sistema mostra o valor exato pra você conferir antes de confirmar. |
| Esc fecha a janela; a tela "Assinatura" volta igual. | Uma dica: fechou a janela sem aplicar? A escolha é descartada, e da próxima vez ela abre de novo com o seu plano atual. |

**P10 · cap10, uma linha no fim (estado S3, sem o CRM)**

| Tela | Fala |
| --- | --- |
| Corte para o S3: abaixo de "Módulos ativos", a seção "Adicione ao seu plano" com o cartão "CRM/Kanban" e o botão "Ativar meu CRM" (sem clicar, sem zoom no valor). | Se faltar algum módulo, ele aparece logo abaixo, em Adicione ao seu plano, com o botão pra ativar. |

**P11 · cap12, trocar a última linha por duas**

| Tela | Fala |
| --- | --- |
| Clique em "Cancelar assinatura": "Cancelar Assinatura" · "Nos ajude a entender o motivo"; em "Motivo do cancelamento", escolhe "Pausa temporária"; "Continuar" → "Confirmar cancelamento", com a lista "Ao confirmar:". [TESTAR: se entra um passo de oferta entre os dois] | E, se um dia for cancelar, o sistema pede o motivo e mostra o que acontece: o acesso continua até o vencimento, as cobranças futuras são canceladas, e dá pra reativar quando quiser. |
| Volta um passo: destaque em "Falar com o Sucesso do Cliente"; fecha a janela sem confirmar. | Antes de confirmar, tem um botão pra falar com a nossa equipe. Muitas vezes dá pra resolver sem cancelar. |

**P12 · cap12, trocar a linha do histórico**

| Tela | Fala |
| --- | --- |
| Como hoje, com destaque em "Baixar PDF" e "Baixar XML" do primeiro cartão. | No Histórico de Pagamentos fica cada mensalidade paga, com a nota fiscal pra baixar, em PDF ou em XML. Se a nota ainda não saiu, o botão Solicitar Nota Fiscal pede na hora. |

**Recapitulação (cap13):** a segunda linha ganha "conheceu o Cato" e a terceira troca "como crescer" por "como montar o
plano"; a montagem ganha um quadro do painel do Cato e um do "Montar plano".

**Mundo: o que precisa para gravar**
1. **Calar o balão do Cato** em todos os capítulos menos o novo: gravar no armazenamento local, antes de abrir a
   página, `cato_adoption_nudge_<empresa>_<usuário>` = `{"count":16,"lastShownAt":<agora>}` (`FAB:249-258`). No capítulo
   do Cato, deixar sem a chave e esperar os 15 s. Handler `track_cato_adoption_event` devolvendo vazio.
2. **Painel do Cato aberto sem janela por cima**: memória pessoal já decidida para o Rafael (senão abre "Quer que o
   Cato lembre de você?", `FAB:185-190`); rotinas e respostas revisadas vazias. São os mesmos handlers do início da
   T21 (`T21/cobertura_160.md`). Nenhuma pergunta é enviada na T0.
3. **Certificado**: handler `fiscal_onboarding_status` devolvendo `requires_certificate` e `certificate_ready`
   verdadeiros; tabela `dfe_certificate_notice_opt_outs` vazia (M2).
4. **EcoFlix**: tabelas `ecoflix_episode_subtitles` (uma faixa "Português") e `ecoflix_episode_resources` (um arquivo
   fictício em "Materiais e extras") no esquema; `ecoflix_section_titles` com semente (as três aparecem como
   desconhecidas ou sem semente na varredura). Vídeo local curto para chegar em "Aula concluída".
5. **Assinatura**: nada novo para P9 (os planos, módulos e níveis do S2 já bastam, sem clicar em aplicar); P10 usa o
   S3; P8 usa o S1; P11 não grava nada (a janela fecha antes de "Confirmar Cancelamento"). Opcional para P12: um
   pagamento sem nota, para o botão "Solicitar Nota Fiscal" existir na tela.
6. `rec/t00_catalogo.mjs:30`: título e descrição da T21 iguais aos que a T21 adotar.

## 4. Estimativa

| Proposta | Fala a mais |
|---|---|
| P1 Fiscal & Ambiental aberto | 7 s |
| P2 busca e sino | 8 s |
| P3 capítulo "O Cato, o seu agente" | 50 s |
| P4 abas da EcoFlix e selo do teste | 13 s |
| P5 player, aula concluída, materiais | 20 s |
| P6 menu da conta, Central de Ajuda, suporte, trocar de conta | 17 s |
| P7 botão Novo no celular | 3 s |
| P8 teste, selos de status, nível de notas | 18 s |
| P9 capítulo "Montar o plano" | 37 s |
| P10 "Adicione ao seu plano" | 7 s |
| P11 cancelar | 14 s |
| P12 histórico: XML e solicitar nota | 7 s |
| Recapitulação | 6 s |
| **Total** | **~207 s (3 min 27 s)** |

**Capítulos novos: 2** (o do Cato e "Montar o plano") mais 2 vinhetas. A aula vai de ~11,5 para ~15,5 min.
Ilustrações novas: 2 (cartão de confirmação do Cato, três selos de status). Sem nenhum trecho novo, o mínimo para
bater com o 1.60.10 é P1 + P3 + o item 1 do Mundo (~57 s).

## Depende de decisão

1. **Tamanho do Cato na T0**: capítulo de 50 s (proposta) ou só uma frase no cap06 apontando o botão e mandando para a
   T21. E a ordem: depende de a T21 ser reescrita como agente antes da T0 (título do cartão na trilha, item M7).
2. **Balão de dica**: mostrar uma vez no capítulo do Cato (proposta) ou calar na aula inteira.
3. **Abrir "Gerenciar plano" e "Cancelar assinatura"**: as duas janelas mostram valores em reais (e o motivo "Preço
   muito alto" na lista). A fala não cita valor, mas a tela mostra. Alternativa: manter só o destaque, como hoje.
4. **Checkout real** (F19) fora: confirmar que a ilustração do cap12 basta.
5. **Duração**: ~15,5 min contra o alvo de 12 da fonte; se precisar cortar, saem primeiro P5, P4 e P12.
