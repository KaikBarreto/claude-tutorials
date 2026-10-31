# T0 v2 · Telas reais necessárias

Regra do Kaik: "Usar telas reais da nova DomiFlix. Não inventar interfaces." No storyboard, cada tela abaixo é um
retângulo "TELA REAL Rnn"; ilustração só entra para conceito (ciclo do trabalho, passos, mapa da trilha, 30 dias,
proporcional, combinados).

**Conferido na 1.38.11 + DomiFlix `487a0ca3` (31/10 19:29)**, em `$TUT_HOME/src-1.38.11` (caminhos relativos a essa
pasta). Os rótulos abaixo estão como no código; nos selos, o texto aparece em maiúsculas na tela.

- **Duas capturas de cada tela:** computador **1280×800** (o robô grava a 2560×1600, como nas aulas com tela) para o 16:9;
  celular **390×844** (escala 3) para o 9:16, recortada na área que a fala cita e ampliada 2,4× (390 → 936 px). Nunca o
  print do computador reduzido dentro do celular.
- **Celular na DomiFlix** = tela menor que 1024 px (`src/hooks/use-mobile.tsx:3`): a aula com "Versão para celular" toca o
  vídeo vertical no lugar do horizontal (`src/pages/DomiflixWatch.tsx:480,543`; `src/components/domiflix/DomiflixIntroGate.tsx:42`).
  A página inicial muda abaixo de 640 px (`src/pages/Domiflix.tsx:140,351`) e **não mostra os selos** na lista; no celular
  os selos aparecem na aula e na gaveta **"Ver trilha"** (`DomiflixWatch.tsx:541,647-652`).
- **Legenda dentro do vídeo:** o player desenha a legenda a 15% do pé no computador e a 18% no celular (`DomiflixWatch.tsx:1446-1452`).
  Na captura, o que a fala cita fica acima dessa faixa.
- **Backend falso**, nunca o Supabase real; mesmo `FAKE_NOW` no backend e no navegador. **Valores em R$ cobertos** por tarja
  lisa (preço de plano e de módulo). Nenhuma "Temporada" ou "Episódio" na tela gravada.
- Nomes de aula: os reais do catálogo da DomiFlix. Onde abaixo aparece "(aula)", o nome vem do catálogo publicado.

## Resumo
| ID | Tela | Situação | Cenas |
|---|---|---|---|
| R01 | Introdução obrigatória ("Primeiro passo"): é onde o T0 passa | **DomiFlix nova (1.38.11)**; fica fora do vídeo (opcional) | 03 |
| R02 | "Trilha do seu plano": percentual, barra e "Formação básica X%" | **DomiFlix nova (1.38.11)** | 07, 15 |
| R03 | Página "Aprenda a usar a Dominex": Módulo 1 com o selo "Formação básica" | **DomiFlix nova (1.38.11)** | 07 |
| R04 | Módulos do plano, selo verde "Tem no seu plano" | **DomiFlix nova (1.38.11)** | 08 |
| R05 | Outros módulos, selo vermelho "Não tem no seu plano", aviso "Consultar fora da ordem?" | **DomiFlix nova (1.38.11)** | 09 |
| R06 | Bloco "Conheça agora. Ative quando fizer sentido." com "Adicionar ao meu plano" | **DomiFlix nova (1.38.11)**; o botão abre página inexistente (C5) | 10 |
| R07 | Página da aula: vídeo com legenda, descrição, "Materiais e extras", trilha ao lado | **DomiFlix nova (1.38.11)** | 11, 21 |
| R08 | "Sua trilha": aulas 1.1, 1.2... com check e a próxima | **DomiFlix nova (1.38.11)** | 12 |
| R09 | Botão verde "Tirar dúvidas com o suporte" | **DomiFlix nova (1.38.11)** | 21 |
| R10 | Mensagem pronta para o suporte (texto do app no WhatsApp) | **DomiFlix nova (1.38.11)**; texto real, celular genérico | 22 |
| R11 | Faixa "Lembrete da trilha de tutoriais" no topo do sistema | **DomiFlix nova (1.38.11)** | 17 |
| R12 | Confirmação no fim do T0 e a primeira aula em seguida | **DomiFlix nova (1.38.11)** | 38 |
| R13 | Menu da conta: "Tutoriais \| Domiflix" | sem mudança na 1.38.11 | 13 |
| R14 | Menu da conta: "Falar com o Suporte" | sem mudança na 1.38.11 | 24 |
| R15 | Guia Técnico (página pública) | publicado, sem mudança | 23 |
| R16 | Assinatura | sem mudança na 1.38.11 | 26 |
| R17 | Assinatura: Pagar Agora e formas de pagamento | sem mudança na 1.38.11 | 27 |
| R18 | Gerenciar Meu Plano | sem mudança na 1.38.11 | 30 |

**Todas existem agora.** R01 a R12 estão na DomiFlix nova (1.38.11); R13 a R18 não mudaram. Nenhuma é gravável no app de
gravação de hoje (8080, 1.38.9): ver "Plano de captura na 1.38.11".

## Estado fictício (vale para todas)
- **Empresa:** Glacial Cold Brasil (climatização, Niterói/RJ), contato@glacialcold.example. **Usuária:** Camila Duarte
  (admin), camila.duarte@glacialcold.example. O e-mail aparece na mensagem do suporte (R10).
- **Conta (decisão D3):** **"Contratado"** (`subscription_status` `active`, mensal, vencimento em `@now+23d`): botão "Adicionar
  ao meu plano" e o preço do módulo (coberto). Se o Kaik preferir "Em teste": botão "Escolher meu plano", sem preço, e o
  lembrete com o selo "Em teste".
- **Plano:** `avancado` = base (Módulo Básico, Portal do Cliente, Precificação Avançada, Perguntas em Vídeo) + Gestão de
  Contratos e PMOC + Funcionários / RH (`supabase/migrations/20260613180000_pricing_reformulation_contracts_module_grandfather.sql:138`
  + `20261013120000_trial_7d_reprice_plans_and_base_features.sql`). A DomiFlix calcula "Tem no seu plano" pelos módulos da
  empresa e do plano (`..._domiflix_trilha_guiada.sql:433-446`). **Fora do plano:** CRM/Kanban, Emissão de Notas Fiscais e
  Cobranças online. Nas outras aulas a Glacial tem todos os módulos.
- **Catálogo da trilha "Tutoriais do sistema"** (`tutoriais-do-sistema`, onboarding ligado): Formação básica (módulos `core`,
  e a **1ª aula é o T0**: é ela que a introdução obrigatória toca), depois os módulos `plan` de Contratos e PMOC e de
  Funcionários / RH, depois os de CRM/Kanban, Emissão de Notas Fiscais e Cobranças online. Toda aula ativa e com vídeo
  (sem vídeo, a aula some da trilha: `..._trilha_guiada.sql:471`). Nomes e aulas: os do catálogo real [confirmar C3].
- **Progresso da Camila:** introdução confirmada; 3 aulas da Formação básica concluídas; a 4ª é a próxima. O percentual é o
  que o servidor calcular (no storyboard, 38% é só ilustração).
- **Aulas usadas:** a 4ª aula da Formação básica (R07, R08), uma aula de Gestão de Contratos e PMOC (R09, R10) e uma de
  Emissão de Notas Fiscais (R05, R06). Cada uma com descrição, uma legenda VTT (a primeira enviada já vem ligada) e 1 ou 2
  materiais (ex.: o trecho do Guia Técnico do assunto, em link).
- **Dois usuários** no backend falso: a Camila (já confirmou) e um usuário novo da mesma empresa, sem confirmação, para a
  introdução obrigatória (R01, R12).
- **Lembrete (R11):** janela dentro dos 30 dias e progresso parado há 3 dias ou mais: título "Camila, vamos retomar de onde
  você parou?" (`src/lib/tutorialReminderCopy.ts:37-43`).

## Telas da DomiFlix nova (1.38.11)

### R01 · Introdução obrigatória · cena 03 (opcional)
- **Na tela:** tela cheia escura, logo da Dominex e o selo "Primeiro passo"; o vídeo (travado: não dá para avançar);
  "Antes de usar o sistema", "Bem-vindo, (nome)", "Este vídeo explica os combinados importantes da nossa parceria e mostra
  como aproveitar os tutoriais. Assista até o final para continuar.", o quadro "Exibido uma única vez" com "Se você estiver
  em teste e depois contratar, esta confirmação continuará válida." (`DomiflixIntroGate.tsx:143-240`).
- **Computador:** vídeo à esquerda, painel à direita. **Celular:** vídeo em cima (vertical, se houver a versão para celular),
  painel embaixo.
- É a tela onde o próprio T0 passa: fica fora do vídeo (a cena 03 é ilustração).

### R02 · "Trilha do seu plano" · cenas 07 e 15
- **Computador:** "Trilha do seu plano" com o percentual, a barra e "X de Y aulas concluídas · Formação básica Z%", e a busca
  "Buscar aula" (`Domiflix.tsx:427-461`). **Celular:** o cartão do topo com "Trilha do seu plano", "X de Y aulas", o
  percentual, "Formação básica: X de Y · Z%" e o botão "Continuar de onde parei" (`Domiflix.tsx:197-230`).

### R03 · Página "Aprenda a usar a Dominex" · cena 07
- **Na tela:** "Olá, Camila · continue sua trilha", "Aprenda a usar a Dominex", a descrição "Aprenda a Dominex na ordem certa,
  da base às funções do seu plano.", o botão "Continuar trilha"; o Módulo 1 com o selo "Formação básica", "3/N", as aulas com
  check e "Próxima aula recomendada" (`Domiflix.tsx:351-378,481-600`; descrição em `..._trilha_guiada.sql:38`).
- **Celular:** "Sequência recomendada", "Aulas da trilha", "Módulo 1" e a lista (sem selo) (`Domiflix.tsx:232-349`).

### R04 · Módulos do plano · cena 08
- **Computador:** a câmera desce até Contratos e PMOC e Funcionários / RH, com o selo verde "Tem no seu plano" e as aulas
  "Na sequência do seu plano". **Celular:** gaveta "Ver trilha" (dentro de uma aula), com os módulos e o selo
  (`DomiflixTrackPanel.tsx:49-83`).

### R05 · Outros módulos · cena 09
- **Computador:** por último, CRM/Kanban, Emissão de Notas Fiscais e Cobranças online, com o selo vermelho "Não tem no seu
  plano" e as aulas "Conheça este módulo"; ao abrir uma aula, o aviso "Consultar fora da ordem?" ("Você pode abrir “(aula)”
  agora para resolver uma dúvida pontual sem alterar a sequência recomendada.") e "Consultar esta aula" (`Domiflix.tsx:607-636`).
- **Celular:** gaveta "Ver trilha": o separador "Conheça outros módulos" / "Você pode assistir e contratar direto pela aula."
  e o módulo com o selo vermelho (`DomiflixTrackPanel.tsx:52`).

### R06 · Bloco de contratar · cena 10
- **Na tela** (embaixo da descrição da aula de Emissão de Notas Fiscais): "Conheça agora. Ative quando fizer sentido.",
  "Esta aula está liberada, mas a função Emissão de Notas Fiscais ainda não faz parte do seu plano. A partir de R$ .../mês, com
  o valor exato confirmado antes da contratação." (preço coberto) e o botão "Adicionar ao meu plano"
  (`src/components/domiflix/DomiflixModuleOffer.tsx:24-35`).
- **Para no clique:** o botão abre `/billing`, que não existe (C5). Se o time corrigir para `/assinatura?addModule=...`, o
  destino é o Gerenciar Meu Plano com o módulo marcado (a cena 30 já mostra essa tela).

### R07 · Página da aula · cenas 11 e 21
- **Computador:** "Sua trilha" à esquerda (340 px); à direita o vídeo e, embaixo, o selo do módulo, "(módulo) · Aula 1.4", o
  título, a descrição, o botão "Tirar dúvidas com o suporte" e "Materiais e extras" (`DomiflixWatch.tsx:515-645`;
  `DomiflixLessonDetails.tsx:66-110`). No player: "Aula 1.4 · 4 de N na sua trilha" e o menu "Legendas"
  (`DomiflixWatch.tsx:500-504,1924-1933`).
- **Celular:** barra "Voltar" e "Ver trilha", o vídeo (vertical, se a aula tiver versão para celular) e, embaixo, os mesmos
  blocos da aula. Um recorte por vez.

### R08 · "Sua trilha" · cena 12
- **Computador:** a coluna da esquerda: logo DomiFlix branco, "Voltar ao sistema", "Voltar para todos os módulos", "Sua trilha",
  "Trilha do seu plano" e o percentual, "Formação básica X%", e as aulas numeradas 1.1, 1.2... com check; a atual em vermelho
  (`DomiflixTrackPanel.tsx:33-88`). **Celular:** a mesma lista na gaveta "Ver trilha".

### R09 · Botão "Tirar dúvidas com o suporte" · cena 21
- Botão verde com o ícone do WhatsApp, embaixo da descrição da aula de Gestão de Contratos e PMOC (`DomiflixLessonDetails.tsx:79-87`).
  Corta no clique (não grava o WhatsApp).

### R10 · Mensagem pronta para o suporte · cena 22
- O clique abre o WhatsApp com este texto (`DomiflixLessonDetails.tsx:43-54`):
  "Olá, equipe de suporte! Preciso tirar uma dúvida sobre a aula 2.1 — (aula), da DomiFlix." / "E-mail do usuário:
  camila.duarte@glacialcold.example" / "Empresa: Glacial Cold Brasil" / "Trilha: Tutoriais do sistema" / "Módulo: Gestão de
  Contratos e PMOC" / "Aula: 2.1 — (aula)" / "Minha dúvida:".
- O WhatsApp não é gravado (marca de terceiro): o texto real entra num celular genérico, sem logo, como a busca real do Guia
  Técnico no T0 atual. O número da Dominex não aparece.

### R11 · Lembrete da trilha · cena 17
- Faixa vermelha no topo do sistema: título (ex.: "Camila, vamos retomar de onde você parou?"), o selo "Contratado" (ou "Em
  teste"), a frase de contexto, o botão "Continuar trilha" (no celular, "Continuar tutorial") e o X "Lembrar novamente amanhã"
  (`src/components/domiflix/DomiflixLearningReminder.tsx:36-45`).

### R12 · Confirmação no fim do T0 · cena 38
- A caixa "Assisti ao vídeo até o final e entendi os combinados." (liberada quando o vídeo termina) e o botão "Confirmar e
  começar a primeira aula" (`DomiflixIntroGate.tsx:208-239`); depois do clique, a próxima aula da Formação básica.
- Gravar com o usuário novo (sem confirmação). Como a tela só libera a caixa no fim do vídeo, o robô precisa de um vídeo
  curto de dublê ou de pular o fim pelo backend (marcar a aula concluída) antes de clicar.

## Telas que já existem (sem mudança na 1.38.11)

### R13 · Menu da conta: "Tutoriais | Domiflix" · cena 13
- **Computador:** cartão da foto no rodapé da barra lateral → menu (Perfil, Assinatura, Tema, Tutoriais | Domiflix, Central de
  Ajuda, Falar com o Suporte); destaque e clique em "Tutoriais | Domiflix" (`src/lib/i18n/messages/app/shell.ts:79-86`).
- **Celular:** Menu da barra de baixo → seção Conta (`src/components/layout/MoreMenuDrawer.tsx:374-396`).

### R14 · Menu da conta: "Falar com o Suporte" · cena 24
- O mesmo menu da R13, destaque e clique em "Falar com o Suporte". Não abrir o WhatsApp (corta no clique).

### R15 · Guia Técnico · cena 23
- **Computador:** `dominex.app/guia-tecnico` (a página publicada, ou `public/guia-tecnico/index.html` servida no nome do
  produto, sem rede): "Manual completo do produto", "Guia Técnico", "Buscar no guia…"; o endereço digitado na barra.
- **Celular:** a página no celular, recorte do topo; o endereço em texto grande embaixo do recorte.

### R16 · Assinatura · cena 26
- Menu da conta → "Assinatura"; destaques na ordem da fala: status, Plano, Vencimento, Valor mensal (coberto), Uso da conta,
  Histórico de pagamentos. **Celular:** um recorte por vez.

### R17 · Assinatura: pagamento · cena 27
- "Pagar Agora"; "20% de desconto no plano anual · válido para Pix ou Boleto"; Pix, Boleto e Cartão; "Sua assinatura é renovada
  automaticamente no cartão cadastrado." (`src/lib/i18n/messages/app/settings.ts:1211-1212,1218-1219`). Valores cobertos;
  não gerar cobrança.

### R18 · Gerenciar Meu Plano · cena 30
- Abas "Planos Prontos" e "Personalizado" (clique em Personalizado), módulos, usuários adicionais e o painel "Seu Plano"
  (`src/components/billing/ModulesManagementCard.tsx:690-696`). Valores cobertos; não confirmar mudança.

## Plano de captura na 1.38.11 (sem executar)
O app de gravação (`$TUT_HOME/app`, porta 8080, backend falso 54321) fica na 1.38.9: há três aulas gravando nele. Para o
T0 v2, uma segunda instância, sem tocar na primeira:

1. **App 1.38.11 em outra pasta e porta.** `$TUT_HOME/app-1.38.11` copiado de `$TUT_HOME/src-1.38.11` (o `setup-app.sh` hoje
   grava em `../app`: precisa de uma pasta de destino própria). `package.json` e `package-lock.json` são iguais aos da 1.38.9:
   o `node_modules` pode ser ligado por hard link (`cp -al`), sem os 765 MB de novo. Build de produção com o mesmo
   `VITE_SUPABASE_URL` gravado (o robô desvia para a outra instância do backend com `FAKE_URL`, `rec/recorder/net.mjs:47`) e
   `serve-dist.mjs` na porta 8081. Build sob a trava (~2 min, até 5 GB de memória: `rec/run.sh:133`).
2. **Backend falso com as tabelas novas, numa cópia própria.** O `fakebase` lê um `schema.json` só (`rec/fakebase/core/schema.mjs:7`),
   então a 1.38.11 precisa de uma cópia (ex.: `rec/fakebase-1.38.11`) na porta 54322 (`FAKE_PORT=54322`). O `types.ts` da
   1.38.11 **não tem** as tabelas e RPCs novas (o app chama com `as any`): `gen-schema.mjs` não basta. Acrescentar à mão,
   a partir das três migrations:
   - tabelas `domiflix_learning_paths`, `domiflix_title_modules`, `domiflix_user_track_modules`, `domiflix_episode_subtitles`,
     `domiflix_episode_resources`, `domiflix_user_onboarding`, `domiflix_intro_acknowledgements`;
   - colunas `companies.learning_onboarding_started_at`, `domiflix_titles.track_group/track_order/learning_path_id/is_active`,
     `domiflix_episodes.mobile_video_id/mobile_video_type/is_active`, `domiflix_user_progress.company_id/last_progress_at`;
   - RPCs com handler: `get_domiflix_learning_status` (a principal: trilha, grupos, plano, progresso, próxima aula, lembrete e
     introdução, `..._trilha_guiada.sql:366-569`), `save_domiflix_progress`, `acknowledge_domiflix_intro`,
     `dismiss_domiflix_learning_reminder`;
   - armazenamento `domiflix-learning-assets` (link assinado dos materiais em arquivo) e `subscription_modules` com nome, preço e
     ordem dos módulos.
3. **Sementes:** a trilha `tutoriais-do-sistema` com `intro_gate_enabled_at`; os módulos e aulas do catálogo real (nomes, ordem,
   grupo, módulo vinculado), cada aula com vídeo, descrição, legenda VTT e materiais; o plano `avancado` da Glacial; o progresso
   da Camila (3 aulas concluídas); a confirmação dela; um usuário novo sem confirmação; a linha de onboarding para o lembrete;
   o mesmo `FAKE_NOW` no backend e no navegador.
4. **Vídeo do player:** as aulas tocam do YouTube ou do Drive, e a gravação não tem rede. Precisa de um dublê local (o robô
   intercepta o embed e serve um vídeo curto do próprio T0) ou de uma exceção de rede só para o embed. Também resolve a R12,
   que só libera a confirmação quando o vídeo termina.
5. **Robô:** `APP_URL=http://127.0.0.1:8081 FAKE_URL=http://127.0.0.1:54322` (`rec/recorder/env.mjs:10-13`); viewport de
   celular 390×844 para as capturas 9:16 (tela menor que 1024 px: toca a versão vertical). Cada captura sob a trava.
6. **Disco:** ~9 GB livres agora; a cópia do app com `node_modules` ligado e o `dist` ficam em ~100 MB.
