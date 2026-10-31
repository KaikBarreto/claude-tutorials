# T0 v2 · Telas reais necessárias

Regra do Kaik: "Usar telas reais da nova DomiFlix. Não inventar interfaces." No storyboard, cada tela abaixo é um
retângulo "TELA REAL Rnn"; ilustração só entra para conceito (ciclo do trabalho, passos, mapa da trilha, 30 dias,
proporcional, combinados).

- **Duas capturas de cada tela:** computador **1280×800** (o robô grava a 2560×1600, como nas aulas com tela) para o 16:9;
  celular **390×844** (escala 3) para o 9:16, recortada na área que a fala cita e ampliada 2,4× (390 → 936 px). Nunca o
  print do computador reduzido dentro do celular; a lista de aulas é a da interface mobile da DomiFlix.
- **Backend falso** (`rec/fakebase`), nunca o Supabase real; mesmo `FAKE_NOW` no backend e no navegador.
- **Valores em R$ cobertos** por tarja lisa em qualquer tela de assinatura (sem preço de plano no vídeo).
- Nenhuma "Temporada" ou "Episódio" na interface gravada (trilha → módulos → aulas).
- Nomes de aula: os reais da DomiFlix nova. Onde abaixo aparece "(nome real)", o nome vem do catálogo publicado.

## Resumo
| ID | Tela | Situação | Cenas |
|---|---|---|---|
| R01 | Onboarding: o T0 como 1º passo obrigatório | **DomiFlix nova**, se tiver tela própria (opcional) | 03 |
| R02 | Trilha Tutoriais do sistema: topo e barra de progresso | **DomiFlix nova** | 07, 15 |
| R03 | Trilha: grupo Formação Básica | **DomiFlix nova** | 07 |
| R04 | Trilha: módulos do plano, selo verde "Tem no seu plano" | **DomiFlix nova** | 08 |
| R05 | Trilha: outros módulos, selo vermelho "Não tem no seu plano" | **DomiFlix nova** | 09 |
| R06 | CTA de contratação de módulo não contratado | **DomiFlix nova** | 10 |
| R07 | Página da aula (player com legenda, descrição, materiais, lista lateral) | **DomiFlix nova** | 11, 21 |
| R08 | Lista de aulas com progresso salvo e próxima aula | **DomiFlix nova** | 12 |
| R09 | Botão "Tirar dúvidas com o suporte" | **DomiFlix nova** | 21 |
| R10 | Contexto enviado ao suporte (empresa, usuário, módulo, aula) | **DomiFlix nova** | 22 |
| R11 | Lembrete dos primeiros 30 dias | **DomiFlix nova**, se for aviso no sistema (opcional) | 17 |
| R12 | Confirmação dos combinados e a 1ª aula em seguida | **DomiFlix nova** | 38 |
| R13 | Menu da conta: "Tutoriais \| Domiflix" | existe na 1.38.9; conferir na nova | 13 |
| R14 | Menu da conta: "Falar com o Suporte" | existe na 1.38.9 | 24 |
| R15 | Guia Técnico (página pública) | publicado | 23 |
| R16 | Assinatura | existe na 1.38.9 | 26 |
| R17 | Assinatura: Pagar Agora e formas de pagamento | existe na 1.38.9 | 27 |
| R18 | Gerenciar Meu Plano | existe na 1.38.9 | 30 |

**Faltam (não existem no `main`):** R01 a R12, todas da DomiFlix nova. **Dá para gravar já:** R13 a R18 (1.38.9).

## Estado fictício (vale para todas)
- **Empresa:** Glacial Cold Brasil (climatização, Niterói/RJ), contato@glacialcold.example. **Usuária:** Camila Duarte
  (admin; é quem gerencia a assinatura e vê o CTA de contratar, se ele for só de admin).
- **Assinatura:** ativa, mensal, vencimento em `@now+23d` (como nas outras aulas).
- **Plano (decisão D3):** Módulo Básico com a base (Portal do Cliente, Precificação Avançada, Perguntas em Vídeo) +
  **Gestão de Contratos e PMOC** + **Funcionários / RH**. É a composição do plano pronto `avancado`
  (`supabase/migrations/20260613180000_pricing_reformulation_contracts_module_grandfather.sql:138` +
  `20261013120000_trial_7d_reprice_plans_and_base_features.sql`). **Não contratados:** CRM/Kanban, Emissão de Notas
  Fiscais e Cobranças online (e os outros que a trilha listar). Nas demais aulas a Glacial tem todos os módulos.
- **Progresso da Camila:** T0 confirmado; 3 aulas da Formação Básica concluídas; a 4ª é a próxima. O percentual é o que
  a regra da DomiFlix nova calcular (no storyboard, 38% é só ilustração) [confirmar C9].
- **Aulas usadas:** a 4ª aula da Formação Básica (R07, R08) e uma aula de Gestão de Contratos e PMOC (R09, R10), com
  os nomes reais.
- **Backend falso, a conferir para R16 a R18:** os planos da semente `gen-01-tenant` estão com nome e preço antigos
  ("Start" etc.) e a Glacial está no `master`. Para estas telas: plano `avancado` com os módulos acima, catálogo de módulos
  (`subscription_modules`) e histórico com 2 ou 3 pagamentos confirmados. [BACKEND: planos, catálogo e histórico]
- **Backend falso para R01 a R12:** as tabelas e funções da DomiFlix nova (trilha, grupos, aulas, progresso, materiais,
  legendas, confirmação, contexto do suporte). [BACKEND: levantar quando a DomiFlix nova sair]

## Telas da DomiFlix nova (não publicada)

### R01 · Onboarding: o T0 como 1º passo obrigatório · cena 03 (opcional)
- **Estado:** 1º acesso da Camila, T0 ainda não confirmado.
- **Precisa aparecer:** o T0 como passo obrigatório e a confirmação liberada só no fim do vídeo, do jeito que a tela mostrar.
- **16:9:** tela inteira, zoom no passo e na confirmação. **9:16:** recorte do celular com o passo e a confirmação.
- Se não houver tela própria, a cena 03 fica só com a ilustração dos três passos. [confirmar C1]

### R02 · Trilha Tutoriais do sistema: topo e barra de progresso · cenas 07 e 15
- **Precisa aparecer:** o nome da trilha, a barra de progresso com o percentual e a aula recomendada (continuar).
- **16:9:** tela inteira; na cena 15, zoom na barra com o destaque "Formação Básica + módulos do seu plano".
- **9:16:** recorte só da barra e do percentual, ampliados. [confirmar C3, C9, C11]

### R03 · Trilha: grupo Formação Básica · cena 07
- **Precisa aparecer:** a Formação Básica **primeiro**, as aulas na ordem, 3 concluídas.
- **16:9:** a trilha inteira e zoom no grupo. **9:16:** a lista da Formação Básica na interface do celular. [confirmar C3]

### R04 · Trilha: módulos do plano · cena 08
- **Precisa aparecer:** Gestão de Contratos e PMOC e Funcionários / RH **depois** da Formação Básica, na ordem recomendada,
  cada um com o selo **verde saturado, check e texto brancos, "Tem no seu plano"**.
- **16:9:** a câmera desce até os módulos do plano; zoom no selo. **9:16:** os módulos empilhados; zoom no selo. [confirmar C4, C11]

### R05 · Trilha: outros módulos · cena 09
- **Precisa aparecer:** CRM/Kanban, Emissão de Notas Fiscais e Cobranças online **por último**, com o selo **vermelho
  saturado, X e texto brancos, "Não tem no seu plano"**, e as aulas com o play (liberadas para assistir).
- **16:9:** a câmera desce até os outros módulos; destaque no play e no selo. **9:16:** um módulo não contratado: selo em zoom e as aulas. [confirmar C4]

### R06 · CTA de contratação · cena 10
- **Estado:** módulo Emissão de Notas Fiscais (não contratado) aberto.
- **Precisa aparecer:** o CTA de contratação e o que acontece no clique. Se abrir Gerenciar Meu Plano com o módulo marcado
  (como o "Adicionar módulo" do sistema faz hoje), a cena para no clique: o cap05 explica o resto. Não confirmar contratação.
- **16:9:** zoom no CTA e clique. **9:16:** recorte só com o CTA, grande. [confirmar C5: rótulo, ação, quem vê]

### R07 · Página da aula · cenas 11 e 21
- **Estado:** a 4ª aula da Formação Básica, parada no meio.
- **Precisa aparecer:** player com a **legenda ligada**, título e **descrição**, **materiais de apoio** (pelo menos um item),
  **lista lateral de aulas** e o botão "Tirar dúvidas com o suporte".
- **16:9:** tela inteira; destaques em sequência: descrição → legendas → materiais.
- **9:16:** a aula no celular, um recorte por vez: player com legenda → descrição → materiais. [confirmar C6]

### R08 · Lista de aulas com progresso e próxima aula · cena 12
- **Precisa aparecer:** as 3 aulas concluídas com check e a próxima (aula recomendada) em destaque.
- **16:9:** zoom na lista lateral. **9:16:** a lista de aulas da interface mobile real (não a lateral reduzida). [confirmar C7]

### R09 · Botão "Tirar dúvidas com o suporte" · cena 21
- **Estado:** uma aula de Gestão de Contratos e PMOC aberta (nome real).
- **16:9:** zoom no botão e clique. **9:16:** recorte com o botão, grande. [confirmar C14: rótulo exato]

### R10 · Contexto enviado ao suporte · cena 22
- **Precisa aparecer:** **Empresa:** Glacial Cold Brasil · **Usuário:** Camila Duarte · **Módulo:** Gestão de Contratos e
  PMOC · **Aula:** (nome real), cada um destacado junto com a fala.
- Se o canal for o **WhatsApp**: não gravar o WhatsApp (marca de terceiro). Vai o celular genérico do T0 atual, sem logo,
  com o **texto real** da mensagem copiado do código (como a busca real do Guia Técnico no T0). Número da Dominex não
  aparece. Se for um chamado dentro do sistema: tela real.
- **9:16:** os quatro itens em linhas grandes, um destaque por vez. [confirmar C14: canal e texto]

### R11 · Lembrete dos primeiros 30 dias · cena 17 (opcional)
- Se o lembrete for um aviso no sistema: o aviso real entra no fim da cena, depois da ilustração dos 30 dias.
- Se for e-mail ou WhatsApp: a cena fica só com a ilustração. [confirmar C10]

### R12 · Confirmação dos combinados · cena 38
- **Estado:** fim do T0, antes de confirmar; depois do clique, a 1ª aula da Formação Básica (ou a trilha, se for para lá).
- **Precisa aparecer:** o texto dos combinados, o botão de confirmar e o que vem em seguida.
- **16:9:** tela inteira, clique em "confirmar", corte para a aula. **9:16:** recorte com a confirmação e o botão. [confirmar C1, C16, C17]

## Telas que já existem (1.38.9)

### R13 · Menu da conta: "Tutoriais | Domiflix" · cena 13
- **16:9:** cartão da foto no rodapé da barra lateral → menu aberto (Perfil, Assinatura, Tema, Tutoriais | Domiflix,
  Central de Ajuda, Falar com o Suporte); destaque e clique em "Tutoriais | Domiflix" (`shell.ts:79-86`;
  `SidebarMenuContent.tsx`).
- **9:16:** botão Menu da barra de baixo → seção Conta (`MoreMenuDrawer.tsx:374-396`); recorte dos atalhos com destaque.
- Conferir o rótulo e o caminho na versão nova. [confirmar C8]

### R14 · Menu da conta: "Falar com o Suporte" · cena 24
- O mesmo menu da R13, destaque e clique em "Falar com o Suporte". Não abrir o WhatsApp (corta no clique).

### R15 · Guia Técnico · cena 23
- **16:9:** navegador em `dominex.app/guia-tecnico` (a página publicada, ou `public/guia-tecnico/index.html` servida no nome
  do produto, sem rede): "Manual completo do produto", "Guia Técnico", "Buscar no guia…"; o endereço digitado na barra.
- **9:16:** a página no celular, recorte do topo; o endereço em texto grande embaixo do recorte.
- É o mesmo conteúdo do T0 atual, agora gravado em vez de desenhado. [confirmar C15]

### R16 · Assinatura · cena 26
- **16:9:** menu da conta → "Assinatura"; destaques na ordem da fala: status (Ativa), Plano, Vencimento, Valor mensal
  (coberto), Uso da conta, Histórico de pagamentos.
- **9:16:** a tela no celular, um recorte por vez: status, plano e vencimento → uso da conta → histórico.
- Valores em R$ cobertos (decisão D2). [BACKEND: plano, catálogo e histórico]

### R17 · Assinatura: pagamento · cena 27
- **Precisa aparecer:** "Pagar Agora"; "20% de desconto no plano anual · válido para Pix ou Boleto"; Pix, Boleto e Cartão;
  o aviso "Sua assinatura é renovada automaticamente no cartão cadastrado." (`settings.ts:1211-1212,1218-1219`).
- Valores cobertos; não gerar cobrança nem concluir pagamento.

### R18 · Gerenciar Meu Plano · cena 30
- **Precisa aparecer:** abas "Planos Prontos" e "Personalizado" (clique em Personalizado), a lista de módulos, os usuários
  adicionais e o painel "Seu Plano" (`ModulesManagementCard.tsx:690-696`).
- Valores cobertos; na aba Planos Prontos aparecem os nomes dos planos (decisão D2). Não confirmar mudança.
