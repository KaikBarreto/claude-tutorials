# T0 v2 · Sinalizações (plano, cobrança e funcionamento)

O Kaik pediu: "Não altere informações sobre plano, cobrança ou funcionamento sem sinalizar." Aqui está tudo o que o T0 v2
passa a dizer de diferente do T0 atual, o que dá para conferir no código publicado e o que precisa de confirmação.

- Código conferido: Dominex **1.38.9** (`$TUT_HOME/src-1.38.9`, `main` de 31/10). A **DomiFlix nova não está publicada**:
  o `main` ainda tem a DomiFlix "estilo Netflix", com seções, títulos, **temporadas** e episódios. Nada do que é novo na
  DomiFlix (Formação Básica, selos de plano, "Tirar dúvidas com o suporte", confirmação dos combinados) pode ser conferido.
- **C** = confirmar antes de gravar (com quem fez a DomiFlix nova). **D** = decisão do Kaik. No `roteiro.md`, cada cena
  traz as marcas `[confirmar Cn]` que valem para ela.
- Nenhuma frase do vídeo cita preço, duração do teste, horário do suporte ou prazo que o código não mostre.

## Mais importantes
1. **C5, o botão de contratar** ("solicitar a contratação por ali mesmo"): o que ele faz e quem vê. Se for contratação
   direta, cai no proporcional (cap05) e precisa de quem gerencia a assinatura.
2. **C11, o período de teste**: no teste, o sistema libera todos os módulos. O que a DomiFlix mostra (selos e percentual)
   para quem ainda está no teste? É o caso de quem assiste ao T0 pela primeira vez.
3. **C1 e C2, a confirmação**: por usuário ou por empresa, e se usuários convidados depois (técnicos) também passam pelo T0.
   Se o técnico também assiste, os capítulos de assinatura (cap04 e cap05) falam de algo que ele não acessa.
4. **C6, "um tema em um único vídeo, com legendas e materiais de apoio"**: as aulas já produzidas (T1, T3, T4, T5) têm de
   10 a 14 min, com vários capítulos, e o player atual não tem legenda nem material de apoio.
5. **C13, reunião de implantação**: a proposta comercial promete "Implantação guiada".

## 1. O que muda em relação ao T0 atual
| # | O vídeo passa a dizer | O T0 atual dizia | O que o código publicado (1.38.9) tem | Cena |
|---|---|---|---|---|
| C1 | O T0 é o **1º passo obrigatório**: assistir até o fim e **confirmar os combinados** para continuar. | Nada (era o primeiro vídeo da trilha, sem trava). | Nenhuma trava: a DomiFlix abre direto (`src/pages/Domiflix.tsx`), sem confirmação. | 03, 38 |
| C2 | Quem começou no **teste** e contratou: a confirmação **continua valendo** e o vídeo não é exigido de novo. | Nada. | Não existe. | 04 |
| C3 | Estrutura: trilha **Tutoriais do sistema** → **Formação Básica** → módulos do plano na **ordem recomendada** → outros módulos. Trilha → módulos → aulas, sem temporadas. | "Cada aula mostra uma área inteira, na prática, dividida em capítulos"; a ordem era configurações, equipe, cadastros, OS, técnico, orçamentos, contratos, financeiro. | Seções, títulos (séries), **temporadas** e episódios (`src/hooks/useDomiflix.ts:9-75`; `src/lib/i18n/messages/app/domiflix.ts:98-101`: "Episódios", "Temporada {{number}}"); a seção "Tutoriais" é um carrossel (`src/hooks/useDomiflixSections.ts`). Não há "Tutoriais do sistema" nem "Formação Básica". | 06 a 09 |
| C4 | Módulos do plano com o selo **"Tem no seu plano"**; os outros com **"Não tem no seu plano"** e as aulas **liberadas** para assistir. | Nada. | A DomiFlix não tem selo de plano. No sistema, módulo fora do plano abre o aviso de módulo (`src/components/ModuleGateModal.tsx`). | 06, 08, 09 |
| C5 | **"Solicitar a contratação por ali mesmo"**, na aula do módulo não contratado. | Contratar era só em Gerenciar Meu Plano (cap05, mantido). | No sistema, "Adicionar módulo" leva a `/assinatura?addModule=<código>` e abre Gerenciar Meu Plano na aba Personalizado com o módulo marcado (`src/components/ModuleGateModal.tsx:56-68`; `src/pages/Billing.tsx:50-53`); a tela Assinatura tem "Contratar" em Módulos Disponíveis (`settings.ts:1204`). Se o CTA da DomiFlix for igual, a contratação no meio do ciclo cai no proporcional do cap05. | 10 |
| C6 | **Cada aula ensina um tema em um único vídeo**, com **descrição, legendas e materiais de apoio**. | Aula = área inteira com capítulos; "volta direto no capítulo daquele assunto" (saiu do cap03). | Episódio com descrição (`src/hooks/useDomiflix.ts:35-49`). O player não tem legenda (nenhum `<track>` em `src/pages/DomiflixWatch.tsx`) nem material de apoio (nenhuma tabela ou campo para isso nas `domiflix_*`). As aulas produzidas são de área inteira: T1 11:58, T3 12:13, T5 13:49. | 11 |
| C7 | **Progresso salvo**; a DomiFlix **sempre indica a próxima aula**. | Nada. | Progresso por usuário e episódio, concluído acima de 90% do vídeo (`src/hooks/useDomiflix.ts:304-372`, regra na linha 347); "Continuar Assistindo"; o próximo é o 1º episódio do título seguinte da mesma seção (`useNextTitleFirstEpisode`, `useDomiflix.ts:139`). | 12 |
| C8 | Menu da conta → **Tutoriais DomiFlix** (fala mantida do T0). | Igual. | "Tutoriais \| Domiflix" (`src/lib/i18n/messages/app/shell.ts:84`). Confirmar se a versão nova muda o rótulo (DomiFlix) ou o caminho, e se o primeiro acesso já abre o T0. | 13 |
| C9 | **Percentual da trilha**: só Formação Básica e módulos do plano contam; aulas de outros módulos não atrapalham. | Nada. | Só "{{pct}}% concluído" por seção (`domiflix.ts:56`), sem regra de plano. Confirmar: por usuário; o que conta como concluída; o que acontece quando o plano muda (módulo novo entra no percentual? módulo retirado sai?). | 15, 16 |
| C10 | **Lembretes nos primeiros 30 dias**, até concluir a Formação Básica e os tutoriais dos módulos do plano. | Nada. | Não existe. Confirmar: 30 dias contados de quê (cadastro da empresa, 1º acesso do usuário?); canal e formato (aviso no sistema, e-mail, WhatsApp?); para quem. O teste padrão é de **7 dias** (`supabase/migrations/20261013120000_trial_7d_reprice_plans_and_base_features.sql:17-18`): os 30 dias passam do teste. | 17 |
| C11 | Selos e percentual pelo **plano**. | "No período de teste, todos os módulos ficam liberados" (mantido no cap05). | No teste, `hasModule` libera todos (`src/hooks/useCompanyModules.ts:204-229`). Confirmar o que a DomiFlix mostra no teste: todos "Tem no seu plano"? só os do plano escolhido? O que entra no percentual? | 08, 15, 29 |
| C12 | A DomiFlix **pode ganhar outras trilhas**, como **gestão** e **contabilidade**. | Nada. | Roteiro de produto (pedido do Kaik). Confirmar os nomes. | 18 |
| C13 | **"Você não precisa esperar uma reunião para começar."** Dúvida específica: suporte pela própria aula. | "O nosso suporte atende pelo WhatsApp... quando você já assistiu à aula daquele assunto, a conversa fica bem mais rápida." | Alinhar com o comercial: a proposta e o simulador prometem **"Implantação guiada e tutoriais completos"** (`src/utils/proposalSimulatorPdf.ts:1181`; `src/pages/ProposalSimulator.tsx:119`) e o follow-up 4 diz **"a implantação a gente faz junto com você"** (`src/utils/followupMessages.ts:14`). O vídeo segue o pedido; o ajuste é no texto comercial (não bloqueia). | 20 |
| C14 | **"Tirar dúvidas com o suporte"** (na aula) já envia **empresa, usuário, módulo e aula**. | "Falar com o Suporte", no menu da conta (mantido no fim do cap03). | "Falar com o Suporte" abre `wa.me/<número da Dominex>` **sem mensagem** (`src/components/layout/MoreMenuDrawer.tsx:178,390-396`; `TopNavbar.tsx:156`). Confirmar: rótulo exato; canal (WhatsApp com mensagem pronta? chamado no sistema?); o texto que vai junto (o vídeo mostra esse texto real). Horário de atendimento fica fora do vídeo. | 21, 22 |
| C15 | Guia Técnico: "explica cada função por escrito, tela por tela" (sai **"na mesma ordem dos tutoriais"** e a busca sai da fala; continua na imagem). | "...tela por tela, na mesma ordem dos tutoriais. É só digitar na busca..." | A página publicada (igual na 1.38.6 e na 1.38.9) diz "na ordem da Trilha Domiflix" e segue as 7 fases da trilha antiga (`public/guia-tecnico/index.html`). Com a trilha nova, a ordem pode não bater: sugestão de ajuste no texto do guia para o time (não bloqueia). | 23 |
| C16 | Fecho: **"seguir pra primeira aula"** (da Formação Básica). | "No próximo tutorial, a gente coloca a logo, os dados da empresa e as preferências do dia a dia" (o T1). | Confirmar qual é a primeira aula da Formação Básica e o que acontece depois de confirmar (abre a aula? volta para a trilha?). A fala não cita o nome para valer nos dois casos. | 38 |
| C17 | **Os combinados**: (1) Formação Básica e módulos do plano, na ordem; (2) dúvida depois da aula, suporte pela própria aula; (3) plano e pagamentos na tela Assinatura. | Um "combinado mais importante": "assiste aos tutoriais, na ordem". | Não existe. O texto da tela de confirmação precisa bater com esses três itens (ou o vídeo muda para bater com ela). | 35 a 38 |

## 2. Mantido e conferido (sem mudança de informação)
Os capítulos de **assinatura** (cap04) e de **crescimento do plano** (cap05) ficam com a fala do T0 atual, letra por
letra. Os arquivos que sustentam essas falas estão **iguais da 1.38.6 para a 1.38.9** (comparação arquivo a arquivo):
`src/lib/i18n/messages/app/settings.ts`, `src/pages/Billing.tsx`, `src/components/checkout/CheckoutLayout.tsx`,
`src/hooks/useCompanyModules.ts`, `supabase/functions/_shared/subscription-proration.ts`,
`supabase/functions/change-subscription-plan/index.ts`, `src/lib/i18n/messages/app/shell.ts`,
`src/components/layout/{SidebarMenuContent,TopNavbar,MoreMenuDrawer,HelpCenterDrawer}.tsx` e `public/guia-tecnico/`.

| Fala mantida | Onde está no código (1.38.9) |
|---|---|
| Menu da conta: Perfil, Assinatura, Tema, Tutoriais \| Domiflix, Central de Ajuda, Falar com o Suporte | `shell.ts:79-86`; celular: `MoreMenuDrawer.tsx:374-396` |
| Falar com o Suporte abre o WhatsApp | `MoreMenuDrawer.tsx:178,390-396`; `TopNavbar.tsx:156` |
| Tela Assinatura: status, plano, vencimento, valor; uso da conta; histórico de pagamentos | `settings.ts:1177,1198-1199,1232,1383` |
| Pagar Agora; Pix, boleto ou cartão; anual com 20% só no Pix e no boleto; cartão mensal que renova sozinho | `settings.ts:1211-1212,1218-1219,1253` |
| Gerenciar Meu Plano com Planos Prontos e Personalizado (módulos e usuários) | `settings.ts:1238`; `src/components/billing/ModulesManagementCard.tsx:690-696` |
| No teste, todos os módulos liberados; ao ativar, os do plano | `useCompanyModules.ts:204-229` |
| Aumento no meio do ciclo: paga hoje a diferença proporcional ao que falta; libera depois da confirmação; a renovação seguinte vem com o valor novo | `_shared/subscription-proration.ts` (`remainingRatio`); `change-subscription-plan/index.ts:18-24`; `settings.ts:1261` |
| Redução: tudo até o vencimento; valor menor no próximo ciclo ("Mudança de valor agendada") | `change-subscription-plan/index.ts:26-32`; `settings.ts:1216` |
| Guia Técnico em dominex.app/guia-tecnico, cada função por escrito, tela por tela | `public/guia-tecnico/index.html` (publicado v1.37.36; sem link dentro do app logado) |

## 3. Decisões para o Kaik
| # | Decisão | Proposta |
|---|---|---|
| D1 | **Logo DomiFlix todo branco** na vinheta de abertura e na cartela, no lugar do "▶ DOMIFLIX" em texto verde. Mexe na identidade congelada do perfil. | Sim no T0 v2 (pedido explícito); o Kaik diz se vale também para as outras aulas. Arquivo pronto no app: `src/assets/domiflix-logo-horizontal-branco.png` (o logo atual do app tem o capacete vermelho: `domiflix-logo-horizontal.png`). |
| D2 | **Assinatura e Gerenciar Meu Plano como tela real** (1.38.9), com os valores em R$ cobertos, no lugar do cartão desenhado do T0 atual (regra "não inventar interfaces"). Na aba Planos Prontos aparecem os nomes dos planos (no painel admin: Essencial, Pro e Business, `src/components/admin/AdminClientsByPlanChart.tsx:11`; conferir o nome que o cliente vê) com os preços cobertos. | Tela real com valores cobertos. Alternativa: manter a ilustração do T0, reestilizada. |
| D3 | **Estado fictício das telas da DomiFlix**: a Glacial Cold Brasil com parte dos módulos (Contratos e PMOC e Funcionários / RH contratados; CRM/Kanban, Emissão de Notas Fiscais e Cobranças online não). Nas outras aulas a Glacial tem todos os módulos ligados. | Aceitar: é o "antes de crescer", e combina com o capítulo do plano. Alternativa: outra empresa fictícia só no T0. |
| D4 | **Treinamento ao vivo**: o objetivo do pedido cita "eventuais treinamentos ao vivo"; o roteiro não promete, porque não há como conferir as condições. | Se quiser, entra no cap03, depois do botão do suporte: "E se surgir uma necessidade real, a gente combina um treinamento ao vivo com você." (~5 s; o vídeo iria a ~4:33 na estimativa conservadora: sairia a frase do menu da cena 13). |
| D5 | **Reaproveitar o áudio** dos capítulos de assinatura e crescimento (texto idêntico) e de quatro títulos. | Sim: gera 2.445 caracteres em vez de 3.587, mesma voz e ritmo. |
| D6 | **Vertical no pipeline**: palco, vinhetas e cartela em 9:16 não existem; a montagem só faz 16:9. | Fazer as versões verticais e mandar uma prévia curta (vinheta + 1 capítulo) antes do vídeo inteiro. |

## 4. Para o time do app (não bloqueia o vídeo)
- Proposta e follow-up comercial falam em "implantação guiada" e "a implantação a gente faz junto com você" (C13).
- O Guia Técnico diz "na ordem da Trilha Domiflix" e segue a trilha antiga de 7 fases (C15).
- A DomiFlix nova deve sair sem "Temporada" e "Episódio" na interface (pedido: trilha → módulos → aulas).
- "Tutoriais | Domiflix" no menu e "DomiFlix" no pedido: definir uma grafia (C8).
