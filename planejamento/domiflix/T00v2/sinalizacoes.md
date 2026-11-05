# T0 v2 · Sinalizações (plano, cobrança e funcionamento)

O Kaik pediu: "Não altere informações sobre plano, cobrança ou funcionamento sem sinalizar." Aqui está tudo o que o T0 v2
passa a dizer de diferente do T0 atual, o que o código confirma e o que ainda precisa de confirmação.

- **Código conferido: Dominex 1.38.11 + DomiFlix até `487a0ca3` (31/10 19:29)**, extraído em `$TUT_HOME/src-1.38.11` (os
  caminhos abaixo são relativos a essa pasta). A DomiFlix nova está publicada: trilha guiada, introdução obrigatória,
  selos de plano, legendas, materiais, lembretes e a versão para celular (migrations `20261031234000_domiflix_trilha_guiada`,
  `20261031235900_domiflix_mobile_video` e `20261031235930_domiflix_publicacao_admin`).
- Primeira versão desta lista: 1.38.9 (sem a DomiFlix nova). Saíram as perguntas que o código respondeu: **C8** (o menu continua
  "Tutoriais | Domiflix") e **C17** (a tela de confirmação não lista os combinados: o vídeo é a fonte).
- **C** = confirmar com quem cuida da DomiFlix ou do comercial. **D** = decisão do Kaik. No `roteiro.md`, cada cena traz as
  marcas `[confirmar Cn]` que ainda valem para ela.
- Nenhuma frase do vídeo cita preço, duração do teste, horário do suporte ou prazo que o código não mostre.

## Mais importantes
1. **C5, o botão de contratar leva a uma página que não existe.** "Adicionar ao meu plano" e "Escolher meu plano" abrem
   `/billing`, que não é rota do app (a Assinatura é `/assinatura`): cai em "não encontrada". A frase do Kaik ("solicitar a
   contratação por ali mesmo") fica; a cena 10 para no clique. Pedir a correção ao time do app.
2. **D7, a introdução é exigida de todo usuário da empresa, inclusive técnicos.** Os capítulos 4 e 5 (assinatura e plano)
   falam com quem gerencia a assinatura.
3. **A legenda agora aparece dentro do vídeo.** O player da DomiFlix desenha a legenda a 15% do pé (computador) e a 18% (celular),
   e a primeira legenda enviada já vem ligada. As folhas marcam essa faixa; nada essencial fica nela. Há **uma legenda por aula**
   para as duas versões: a 16:9 e a 9:16 precisam ter a mesma linha do tempo.
4. **A 9:16 é a "Versão para celular" da mesma aula.** Em tela menor que 1024 px ela substitui a horizontal sozinha, inclusive
   na introdução obrigatória (onde o T0 passa).
5. **C11, o teste.** O sistema libera todos os módulos no teste, mas na DomiFlix os selos e o percentual seguem o plano da
   empresa também no teste.
6. **D8, frases do Kaik × rótulos da tela** (não mexi nas frases): a página se chama "Aprenda a usar a Dominex" (o nome
   "Tutoriais do sistema" quase não aparece) e os materiais ficam em "Materiais e extras".
7. **C13, a proposta comercial** ainda promete "Implantação guiada".

## 1. O que muda em relação ao T0 atual
A coluna "O que o código publicado (1.38.9) tem" foi conferida de novo na **1.38.11 + DomiFlix `487a0ca3`**. Em cada linha:
**Confirmado**, **Muda** (o código diz outra coisa: a fala foi ajustada ou a frase do Kaik ficou e está marcada) ou **Aberto**.

| # | O vídeo passa a dizer | O T0 atual dizia | O que o código publicado (1.38.9) tem | Cena |
|---|---|---|---|---|
| C1 | O T0 é o **1º passo obrigatório**: assistir até o fim e **confirmar os combinados** para continuar. | Nada (era o primeiro vídeo da trilha, sem trava). | **Confirmado.** Tela cheia "Introdução obrigatória" antes do sistema e antes da DomiFlix, para todo usuário da empresa que não é da equipe Dominex (`src/components/layout/AppLayout.tsx:126`; `src/components/domiflix/DomiflixLayout.tsx:195`). Selo "Primeiro passo", vídeo travado, caixa "Assisti ao vídeo até o final e entendi os combinados." liberada só quando o vídeo termina, botão "Confirmar e começar a primeira aula" (`src/components/domiflix/DomiflixIntroGate.tsx:88-99,160,180,218,236-238`). O servidor recusa sem o vídeo concluído: "Conclua o vídeo antes de confirmar" (`supabase/migrations/20261031234000_domiflix_trilha_guiada.sql:596`). O vídeo da introdução é a 1ª aula da Formação básica (`:521,554-563`). Vale também para técnicos (D7). | 03, 38 |
| C2 | Quem começou no **teste** e contratou: a confirmação **continua valendo** e o vídeo não é exigido de novo. | Nada. | **Confirmado.** A confirmação fica gravada por usuário e trilha, sem prazo (`..._trilha_guiada.sql:186-194,597-599`), e a tela diz "Exibido uma única vez" e "Se você estiver em teste e depois contratar, esta confirmação continuará válida." (`DomiflixIntroGate.tsx:200-203`). Quem foi cadastrado antes de a introdução ser ligada não passa por ela (`..._trilha_guiada.sql:557`). | 04 |
| C3 | Estrutura: trilha **Tutoriais do sistema** → **Formação Básica** → módulos do plano na **ordem recomendada** → outros módulos. Trilha → módulos → aulas, sem temporadas. | "Cada aula mostra uma área inteira, na prática, dividida em capítulos"; a ordem era configurações, equipe, cadastros, OS, técnico, orçamentos, contratos, financeiro. | **Confirmado, com dois avisos.** Trilha `tutoriais-do-sistema`, título "Tutoriais do sistema" (`..._trilha_guiada.sql:37-44`); grupos `core` (na tela, "Formação básica") e `plan` (`:74-78`; `src/components/domiflix/DomiflixModuleBadge.tsx:16`); ordem Formação básica → plano → outros (`..._trilha_guiada.sql:473-476`); temporadas ignoradas (`:114-129`). Avisos: (1) a página mostra o título **"Aprenda a usar a Dominex"**; "Tutoriais do sistema" só aparece em "Cursos disponíveis", quando houver mais de um curso, e na mensagem do suporte (`src/pages/Domiflix.tsx:134-136,381-425`; `DomiflixLessonDetails.tsx:48`); (2) a tela escreve "Formação básica" (b minúsculo; no selo, tudo em maiúsculas). **Aberto:** quais aulas formam a Formação básica (catálogo); o T0 tem de ser a 1ª delas. | 06, 07 |
| C4 | Módulos do plano com o selo **"Tem no seu plano"**; os outros com **"Não tem no seu plano"** e as aulas **liberadas** para assistir. | Nada. | **Confirmado.** Selo verde com check e texto brancos, "Tem no seu plano", e vermelho com X e texto brancos, "Não tem no seu plano", em maiúsculas (`DomiflixModuleBadge.tsx:20-28`). As aulas dos outros módulos abrem depois do aviso "Consultar fora da ordem?" e "Consultar esta aula" (`Domiflix.tsx:607-636`). No celular, a página inicial não mostra os selos (só "Na sequência do seu plano" e "Conheça este módulo", `Domiflix.tsx:326-336`); eles aparecem na aula e na gaveta "Ver trilha" (`DomiflixLessonDetails.tsx:68`; `DomiflixTrackPanel.tsx:56`; `src/pages/DomiflixWatch.tsx:541,647-652`). | 06, 08, 09 |
| C5 | **"Solicitar a contratação por ali mesmo"**, na aula do módulo não contratado. | Contratar era só em Gerenciar Meu Plano (cap05, mantido). | **Muda o rótulo, e há um erro.** Bloco "Conheça agora. Ative quando fizer sentido." e "Esta aula está liberada, mas a função ... ainda não faz parte do seu plano."; conta contratada: o preço ("A partir de R$ .../mês") e o botão **"Adicionar ao meu plano"**; no teste: "Escolha o módulo ao montar sua assinatura." e **"Escolher meu plano"** (`src/components/domiflix/DomiflixModuleOffer.tsx:24-35`). Aparece para qualquer usuário. **Erro:** o botão abre `/billing`, que não é rota do app (a Assinatura é `/assinatura`, `src/lib/i18n/appRouteSlugs.ts:189`) e cai em "não encontrada" (`DomiflixModuleOffer.tsx:31`; `src/App.tsx:963`). A frase do Kaik fica; a cena para no clique; o preço fica coberto. | 10 |
| C6 | **Cada aula ensina um tema em um único vídeo**, com **descrição, legendas e materiais de apoio**. | Aula = área inteira com capítulos; "volta direto no capítulo daquele assunto" (saiu do cap03). | **Confirmado na estrutura.** Uma aula = um vídeo (com versão vertical opcional), descrição, legendas VTT ou SRT (a primeira enviada já vem ligada) e materiais em arquivo ou link (`..._trilha_guiada.sql:140-172`; `20261031235900_domiflix_mobile_video.sql`; `src/components/admin/AdminDomiflixLessonExtras.tsx:31-42`; `DomiflixWatch.tsx:731-747,1446-1452`). **Rótulo:** na aula, a seção se chama **"Materiais e extras"** (`DomiflixLessonDetails.tsx:90`); "Materiais de apoio" só no painel admin (`AdminDomiflixLessonExtras.tsx:117`). A frase do Kaik fica (D8). **Aberto:** como as aulas atuais (10 a 14 min, com capítulos) viram aulas de um tema (catálogo). | 11 |
| C7 | **Progresso salvo**; a DomiFlix **sempre indica a próxima aula**. | Nada. | **Confirmado.** Progresso por usuário (`save_domiflix_progress`, `..._trilha_guiada.sql:313-364`), aula concluída acima de 90% do vídeo (`src/lib/domiflixProgress.ts:45,79`); "Próxima aula recomendada", "Continuar trilha" e, no fim da aula, "Vamos para a próxima" (`Domiflix.tsx:371-374,573-583`; `DomiflixWatch.tsx:601-628`); a próxima aula é calculada no servidor (`..._trilha_guiada.sql:511-517`). | 12 |
| C9 | **Percentual da trilha**: só Formação Básica e módulos do plano contam; aulas de outros módulos não atrapalham. | Nada. | **Confirmado.** "Trilha do seu plano" mostra o percentual da Formação básica + módulos do plano; os outros ficam fora (`..._trilha_guiada.sql:503-506,543-550`; `Domiflix.tsx:427-451`; `DomiflixTrackPanel.tsx:39-47`), e embaixo vem "Formação básica X%". O cálculo é feito a cada consulta: módulo contratado depois entra no percentual na hora. | 15, 16 |
| C10 | **Lembretes nos primeiros 30 dias**, até concluir a Formação Básica e os tutoriais dos módulos do plano. | Nada. | **Confirmado.** Faixa no topo do sistema ("Lembrete da trilha de tutoriais"), por usuário, do dia 0 ao 30 contados do mais recente entre o cadastro do usuário e o início do onboarding da empresa, até concluir a Formação básica e os módulos do plano; fica mais forte depois de 3 e de 7 dias parado; o X é "Lembrar novamente amanhã" (`..._trilha_guiada.sql:419-423,524-532,604-630`; `src/components/domiflix/DomiflixLearningReminder.tsx:36-45`; textos em `src/lib/tutorialReminderCopy.ts:37-49`). O teste padrão é de 7 dias (`20261013120000_trial_7d_reprice_plans_and_base_features.sql:17-18`). | 17 |
| C11 | Selos e percentual pelo **plano**. | "No período de teste, todos os módulos ficam liberados" (mantido no cap05). | **Respondido.** Na DomiFlix, "Tem no seu plano" segue o plano e os módulos da empresa também no teste (`..._trilha_guiada.sql:433-446`), enquanto o sistema libera tudo no teste (`src/hooks/useCompanyModules.ts:204-229`). No teste, os módulos fora do plano aparecem com "Não tem no seu plano" e o botão "Escolher meu plano". A fala do cap05 continua verdadeira para o sistema. | 08, 15, 29 |
| C12 | A DomiFlix **pode ganhar outras trilhas**, como **gestão** e **contabilidade**. | Nada. | **Estrutura confirmada.** O app já aceita outros cursos: aparecem em "Cursos disponíveis" quando houver mais de um, e "Os demais cursos ficam livres e não geram cobrança diária" (`Domiflix.tsx:381-425`; `src/components/admin/AdminDomiflixLearningPaths.tsx:69`). **Aberto:** os nomes (gestão, contabilidade) são roteiro de produto. | 18 |
| C13 | **"Você não precisa esperar uma reunião para começar."** Dúvida específica: suporte pela própria aula. | "O nosso suporte atende pelo WhatsApp... quando você já assistiu à aula daquele assunto, a conversa fica bem mais rápida." | **Sem mudança.** A proposta e o simulador continuam com "Implantação guiada e tutoriais completos" (`src/utils/proposalSimulatorPdf.ts:1181`; `src/pages/ProposalSimulator.tsx:119`) e o follow-up 4 com "a implantação a gente faz junto com você" (`src/utils/followupMessages.ts:14`). O lembrete da conta contratada diz "continue a implantação pela trilha" (`tutorialReminderCopy.ts:12`), que combina com o vídeo. O ajuste é no texto comercial (não bloqueia). | 20 |
| C14 | **"Tirar dúvidas com o suporte"** (na aula) já leva **empresa, usuário, módulo e aula**. | "Falar com o Suporte", no menu da conta (mantido no fim do cap03). | **Confirmado; fala ajustada.** O botão verde "Tirar dúvidas com o suporte" (com o ícone do WhatsApp), embaixo da descrição da aula, abre o WhatsApp da Dominex com a mensagem pronta: "Olá, equipe de suporte! Preciso tirar uma dúvida sobre a aula X — (aula), da DomiFlix.", "E-mail do usuário", "Empresa", "Trilha", "Módulo", "Aula" e "Minha dúvida:" (`DomiflixLessonDetails.tsx:43-54,79-87`). Quem envia é a pessoa: "ele já envia ..." virou "o WhatsApp abre com a sua empresa, o seu usuário, o módulo e a aula já na mensagem" (cena 22). | 21, 22 |
| C15 | Guia Técnico: "explica cada função por escrito, tela por tela" (sai **"na mesma ordem dos tutoriais"** e a busca sai da fala; continua na imagem). | "...tela por tela, na mesma ordem dos tutoriais. É só digitar na busca..." | **Sem mudança.** A página publicada (igual da 1.38.6 à 1.38.11) diz "na ordem da Trilha Domiflix" e segue as 7 fases da trilha antiga (`public/guia-tecnico/index.html`). Com a trilha nova, a ordem não bate: ajuste no texto do guia para o time (não bloqueia). | 23 |
| C16 | Fecho: **"seguir pra primeira aula"** (da Formação Básica). | "No próximo tutorial, a gente coloca a logo, os dados da empresa e as preferências do dia a dia" (o T1). | **Confirmado.** O botão "Confirmar e começar a primeira aula" leva à próxima aula da trilha (`DomiflixIntroGate.tsx:106-111,236-238`; `src/hooks/useDomiflix.ts:104-109`). **Aberto:** o nome dessa aula (catálogo). | 38 |

## 2. Mantido e conferido (sem mudança de informação)
Os capítulos de **assinatura** (cap04) e de **crescimento do plano** (cap05) ficam com a fala do T0 atual, letra por letra. Os
arquivos que sustentam essas falas estão **iguais da 1.38.6 para a 1.38.11** (comparação arquivo a arquivo):
`src/lib/i18n/messages/app/settings.ts`, `src/pages/Billing.tsx`, `src/components/checkout/CheckoutLayout.tsx`,
`src/hooks/useCompanyModules.ts`, `src/components/billing/ModulesManagementCard.tsx`,
`supabase/functions/_shared/subscription-proration.ts`, `supabase/functions/change-subscription-plan/index.ts`,
`src/lib/i18n/messages/app/shell.ts`, `src/components/layout/{SidebarMenuContent,TopNavbar,MoreMenuDrawer,HelpCenterDrawer}.tsx`
e `public/guia-tecnico/`. A coluna da direita vale para a 1.38.9 e para a 1.38.11 (mesmas linhas).

| Fala mantida | Onde está no código (1.38.9) |
|---|---|
| Menu da conta: Perfil, Assinatura, Tema, Tutoriais \| Domiflix, Central de Ajuda, Falar com o Suporte (era o C8: o rótulo não mudou) | `shell.ts:79-86`; celular: `MoreMenuDrawer.tsx:374-396` |
| Falar com o Suporte abre o WhatsApp (o mesmo número do botão da aula) | `MoreMenuDrawer.tsx:178,390-396`; `TopNavbar.tsx:156`; `DomiflixLessonDetails.tsx:54` |
| Tela Assinatura: status, plano, vencimento, valor; uso da conta; histórico de pagamentos | `settings.ts:1177,1198-1199,1232,1383` |
| Pagar Agora; Pix, boleto ou cartão; anual com 20% só no Pix e no boleto; cartão mensal que renova sozinho | `settings.ts:1211-1212,1218-1219,1253` |
| Gerenciar Meu Plano com Planos Prontos e Personalizado (módulos e usuários) | `settings.ts:1238`; `src/components/billing/ModulesManagementCard.tsx:690-696` |
| No teste, todos os módulos liberados no sistema; ao ativar, os do plano | `useCompanyModules.ts:204-229` (na DomiFlix, ver C11) |
| Aumento no meio do ciclo: paga hoje a diferença proporcional ao que falta; libera depois da confirmação; a renovação seguinte vem com o valor novo | `_shared/subscription-proration.ts` (`remainingRatio`); `change-subscription-plan/index.ts:18-24`; `settings.ts:1261` |
| Redução: tudo até o vencimento; valor menor no próximo ciclo ("Mudança de valor agendada") | `change-subscription-plan/index.ts:26-32`; `settings.ts:1216` |
| Guia Técnico em dominex.app/guia-tecnico, cada função por escrito, tela por tela | `public/guia-tecnico/index.html` (publicado v1.37.36; sem link dentro do app logado) |

## 3. Decisões para o Kaik
| # | Decisão | Proposta |
|---|---|---|
| D1 | **Logo DomiFlix todo branco** na vinheta de abertura e na cartela, no lugar do "▶ DOMIFLIX" em texto verde. Mexe na identidade congelada do perfil. | Sim no T0 v2. A DomiFlix nova já trocou para o logo todo branco (`src/components/domiflix/DomiflixLayout.tsx:4`; `DomiflixTrackPanel.tsx:7`, arquivo `src/assets/domiflix-logo-horizontal-branco.png`). O Kaik diz se vale também para as outras aulas. |
| D2 | **Assinatura e Gerenciar Meu Plano como tela real** (sem mudança na 1.38.11), com os valores em R$ cobertos, no lugar do cartão desenhado do T0 atual. Na aba Planos Prontos aparecem os nomes dos planos (no painel admin: Essencial, Pro e Business, `src/components/admin/AdminClientsByPlanChart.tsx:11`; conferir o nome que o cliente vê) com os preços cobertos. Vale também para o preço do módulo no bloco de contratar da cena 10. | Tela real com valores cobertos. Alternativa: manter a ilustração do T0, reestilizada. |
| D3 | **Estado fictício das telas da DomiFlix**: a Glacial Cold Brasil com o plano `avancado` (Contratos e PMOC e Funcionários / RH no plano; CRM/Kanban, Emissão de Notas Fiscais e Cobranças online fora). Nas outras aulas a Glacial tem todos os módulos. E a conta: **"Contratado"** (botão "Adicionar ao meu plano", preço coberto) ou **"Em teste"** (botão "Escolher meu plano", sem preço). | Contratado: o botão fica mais perto de "solicitar a contratação" e combina com os capítulos 4 e 5. A diferença com as outras aulas é o "antes de crescer". |
| D4 | **Treinamento ao vivo**: o objetivo do pedido cita "eventuais treinamentos ao vivo"; o roteiro não promete, porque não há como conferir as condições. | Se quiser, entra no cap03, depois do botão do suporte: "E se surgir uma necessidade real, a gente combina um treinamento ao vivo com você." (~5 s; o vídeo iria a ~4:33 na estimativa conservadora: sairia a frase do menu da cena 13). |
| D5 | **Reaproveitar o áudio** dos capítulos de assinatura e crescimento (texto idêntico) e de quatro títulos. | Sim: gera 2.433 caracteres em vez de 3.575, mesma voz e ritmo. |
| D6 | **Vertical no pipeline**: palco, vinhetas, cartela e montagem em 9:16. | Em andamento por outro agente, numa área própria. Do lado da DomiFlix, a 9:16 entra como "Versão para celular" da mesma aula, com a mesma legenda (ver "Mais importantes", 3 e 4). |
| D7 | **A introdução é obrigatória para todo usuário da empresa**, inclusive técnicos (não há exceção por papel no código). O T0 fala de assinatura e plano (cap04 e cap05), que o técnico não gerencia. | Manter o vídeo único (é o pedido). Se o Kaik quiser, uma frase curta antes do cap04, por exemplo "Se você cuida do plano da empresa, presta atenção nesta parte.", ou pedir ao time do app que a introdução valha só para quem gerencia a assinatura. |
| D8 | **Frases do Kaik × rótulos da tela** (as frases ficaram letra por letra): "a trilha Tutoriais do sistema" (a página mostra "Aprenda a usar a Dominex"), "materiais de apoio" (a aula mostra "Materiais e extras") e "Formação Básica" (a tela escreve "Formação básica"). | Manter as frases e destacar o rótulo real na imagem. Alternativa: o Kaik troca a frase ou o time do app troca o rótulo. |

## 4. Para o time do app (não bloqueia o vídeo)
- **Aba Documentos do contrato PMOC sempre acusa "Endereço do cliente" em branco (achado no T12, 04/11):** a tela do contrato
  busca `customers (id, name, document, phone)` (`src/hooks/useContractDetail.ts:42`), sem `address, city, state`, mas monta
  `customer_address` com eles (`src/pages/ContractDetail.tsx:1519`); `PmocContractDocsTab.tsx:478` então mostra "Dados faltando
  para gerar documentos PMOC: Endereço do cliente" para TODO contrato, e o PDF pode sair sem endereço. A `useContracts.ts:1909`
  já pede o endereço. Afeta o T12 (cap08, 8:30–8:57): corrigido o app, regravar o cap08.
- **"Ver trilha" no celular não aparece (achado na gravação, 04/11):** na aula, no celular, a gaveta abre (`role=dialog`,
  `data-state=open`), mas fica atrás da página: a página da aula é `fixed inset-0 z-[100]` (`src/pages/DomiflixWatch.tsx:575`)
  e a gaveta usa `z-50` (`src/components/ui/drawer.tsx:21,57`). O cliente no celular não vê a trilha, os selos nem o progresso
  dentro da aula. Afeta o 9:16 do T0 v2 (cenas 07 a 09 e 12, sem selos no celular): corrigido o app, regravar o cap01-p.
- **Material novo some da lista do Estoque por até 30 s (achado no T8, 04/11):** a lista filtra pelos ids da consulta
  `accessible-inventory-ids` (`src/hooks/useAccessibleInventoryIds.ts:17-25`, `staleTime: 30_000`), e nada invalida essa chave
  quando se cadastra um material (as invalidações de `useStocks.ts`/`useInventoryCounts.ts` não a incluem). Quem acabou de
  salvar não vê o material até a janela perder e ganhar o foco ou a tela remontar depois de 30 s. Basta invalidar
  `['accessible-inventory-ids']` ao criar material e ao mudar locais. No vídeo (T8, caps 02 e 11) a lista atualiza pelo
  foco da janela, um evento real do navegador, como vai ser depois da correção.
- **Orçamentos a 1280 px (achado no T9, 04/11):** com o menu lateral aberto, o botão "Configurar Proposta" cobre parte da aba
  "Precificação". No vídeo o menu fica recolhido.
- **Dois "sugerido" no resumo do orçamento (T9):** ao lado de "Preço sugerido R$ 1.085,00" aparece "Composição do preço sugerido
  R$ 585,00" (`crm.ts:558`, `bdiCompositionTitle`), que é só a parte do BDI automático. Um rótulo como "Parte calculada pelo
  BDI" evitaria a leitura de dois preços sugeridos diferentes.
- **"Observações internas" sai na proposta (T9, P9 do inventário):** o campo de observações do orçamento tem o placeholder
  "Observações internas" (`crm.ts:628`), mas o texto é impresso para o cliente.
- **Botão de contratar da DomiFlix** ("Adicionar ao meu plano" e "Escolher meu plano") abre `/billing`, rota que não existe:
  cai em "não encontrada". O certo é `/assinatura?addModule=<código>` (como o "Adicionar módulo" do sistema faz:
  `src/components/ModuleGateModal.tsx:58-68`). Arquivo: `src/components/domiflix/DomiflixModuleOffer.tsx:31`. Se a cena 10
  for mostrar o destino do clique, isto precisa estar corrigido antes da gravação. **Corrigido em `36c6303f` (1.38.21): o botão vai
  para `/assinatura`.**
- Proposta e follow-up comercial falam em "implantação guiada" e "a implantação a gente faz junto com você" (C13).
- O Guia Técnico diz "na ordem da Trilha Domiflix" e segue a trilha antiga de 7 fases (C15).
- A barra da DomiFlix ainda mostra "Módulos", "Lives" e "Minha Lista", do modelo antigo (`src/lib/i18n/messages/app/domiflix.ts`,
  igual à 1.38.9; `DomiflixLayout.tsx:258-267`): conferir se ainda fazem sentido com a trilha guiada.
- A introdução diz "Bem-vindo, (nome)" para todos (`DomiflixIntroGate.tsx:189`); "Boas-vindas, (nome)" serve para qualquer pessoa.
- "Tutoriais | Domiflix" no menu, "DomiFlix" no pedido e no logo: definir uma grafia.
- "Formação básica" na tela e "Formação Básica" no pedido: definir uma grafia (D8).
- **Contagem de visitas do contrato (T11, 05/11):** o horizonte conta as duas pontas. Trimestral com "Horizonte (meses)" 12
  dá "= 5 ocorrências" e "Contrato criado com 5 OSs"; o PMOC mensal nasce com 13 OSs (a última no mesmo dia, um ano depois),
  com 12 parcelas. Se a visita do aniversário não for de propósito, é um a mais por contrato (e pode duplicar com a renovação).
  As falas do T11 não citam a quantidade, então a correção só mudaria a imagem.
- **Faixa "Dados faltando: Endereço do cliente" (T12 cap08 e T11 cap12):** o mesmo defeito do `useContractDetail.ts:42`
  (seção acima); os dois capítulos são regravados depois da correção. **Continua na 1.38.24** (05/11): a linha 42 ainda pede
  `customers (id, name, document, phone)`; o conserto é acrescentar `address, city, state` nesse `select`.
- **DRE: "Pagamento de Fatura" e "Transferência entre contas" na lista de despesas (T20, 05/11, a confirmar):** na configuração
  do DRE, categoria sem grupo (`dre_group` nulo) cai em despesa operacional, e essas duas categorias do sistema aparecem na
  lista junto das despesas com pessoal. Se o relatório também as somar, pagamento de fatura e transferência entre contas
  viram despesa no resultado. A fala do T20 não cita a lista.
- **Asaas, "Categoria da receita" sem lista (T19, 05/11):** o filtro compara `type === 'income'`, mas o banco grava 'entrada'
  (`SettingsAsaasContent.tsx:94`); o campo fica como texto com "Nenhuma" e a categoria não aparece para escolher.
- **Asaas, cartão de taxas em "referência" depois de "Ativar recebimentos" (T19, 05/11):** a consulta fica guardada por 10 min;
  as taxas da conta só aparecem depois de recarregar a página.
- **Orçamento, BDI com ponto decimal (T9, 05/11):** textos montados pelo app saem com ponto: "R$ 0,00 ÷ 0.6000" na Composição do
  preço sugerido, "BDI atual 1.0000" e "R$ 32,00/h × 1.5h" (formatação sem pt-BR; o cliente vê assim também).
- **"Retomar OS" com pouco contraste (T7, 1.38.21):** no celular, o botão virou neutro (`bg-foreground`) e fica cinza-escuro sobre o
  rodapé quase preto; o texto se lê, mas o botão quase some (caps 07 e 08 do T7; quadros em `rec/t7/quadros_1.38.21/retomar_os/`).
- **Ponto, saldo negativo com a jornada aberta (T15, 05/11):** em Hoje, o olho do dia mostra "Saldo -7h52min" enquanto a jornada
  ainda está aberta (a pessoa acabou de entrar); dá a impressão de dívida de horas antes do fim do dia.
- **Ponto no celular, logo escuro sobre cabeçalho preto (T15, 05/11):** a tela de bater o ponto põe o logo da empresa sobre fundo
  preto; logo com texto escuro (o caso comum) fica quase ilegível. Um fundo claro atrás do logo resolveria.
- **RH, fluxograma e organograma (T22, 05/11):** o painel "Editar nó" do organograma fica em parte coberto pela barra de ferramentas;
  no fluxograma, as alças de ligação da Decisão e do Documento ficam sob a camada do texto (arrastar a seta pega só parte delas);
  os botões de zoom do quadro não respondem; Conferência, Sobre o processo e Exportar só têm ícone (o nome só no tooltip).
- **Notas fiscais (T14, 05/11, achados no código da 1.38.24, a confirmar na tela):**
  - depois de uma ação, a lista de notas não recarrega sozinha (no vídeo, um corte no cap09);
  - "Descartar nota?" aparece mesmo com o rascunho já salvo;
  - "Baixar PDF" abre uma aba em branco antes de baixar.
- **WhatsApp (T21, 05/11):** o Histórico de envios mostra a chave técnica do aviso ("OS · a_caminho") em vez do nome; a prévia
  dos avisos de cobrança traz uma empresa de exemplo fixa ("Clima Forte Serviços") em vez do nome da empresa logada.
- **Assinatura do cliente vira texto cru no celular (T7, confirmado na 1.38.24, 05/11):** depois de "Confirmar" na pergunta de
  assinatura do checklist, a pergunta mostra o valor gravado, uma linha enorme `data:image/png;base64,...`, em vez da imagem; a
  assinatura só volta a aparecer ao tocar no lápis. Em `DynamicFormQuestions.tsx` o modo resposta só trata foto; o último caso
  imprime `response_value` como texto (vídeo gravado sai como parágrafo vazio). No vídeo, o trecho sai na montagem.
