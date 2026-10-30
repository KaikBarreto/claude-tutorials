# Inventário funcional · T10 — CRM: funil, leads e captação (Dominex)

> Base para o roteiro do tutorial "T10 · CRM: funil, leads e captação" (Kanban, comercial, acompanhamento de processos e
> projetos). Levantado em 30/10/2026 contra o código publicado `APP_VERSION = "1.38.6"` (`src/config/version.ts:1`),
> cópia em `/home/claude/domiflix/src-1.38.6`. **Análise estática, somente leitura.** "(a confirmar)" = só rodando.
> Formato do inventário do T3 (`_referencia/T03_inventario_exemplo.md`).

## Como ler

- Caminhos relativos a `src/`, exceto `supabase/...`. Formato `arquivo:linha`.
- Rótulos entre aspas = texto exato (pt-br). Fonte principal: `lib/i18n/messages/app/crm.ts:11-402` e
  `lib/i18n/messages/app/projects.ts:7-146`. Textos fixos no componente estão citados onde aparecem.
- "Oportunidade", "lead" e "card" são a mesma linha da tabela `leads`. "Funil" = `crm_pipelines`; "estágio"/"etapa" =
  `crm_stages` (a tela usa as duas palavras).
- Componentes compartilhados (janelas, toasts, seletor de cliente com "+") seguem o inventário do T3, seções 6.4 e 7.

---

## 0. Resumo para o roteiro

### 0.1 Capítulos da trilha (v1.22.5) contra o código de hoje

| # | Item da trilha | Situação | O que ajustar |
|---|---|---|---|
| 1 | Tela CRM: kanban × lista; empty-state "criar estágios padrão" | **Parcial** | No computador **só existe o Kanban** (a alternância Lista/Kanban fica no filtro do celular, `pages/CRM.tsx:785-812,1663-1667`). Empty-state: **"Configure seu funil"** com **"Começar com estágios padrão"** e "Personalizar estágios" (`CRM.tsx:950-976`; `crm.ts:80-84`). A tela tem duas abas: **"Funil"** e **"Tarefas"** (`CRM.tsx:1256-1266`). |
| 2 | Montar o funil: criar, renomear, reordenar, colorir estágios | **Mudou de lugar** | Tudo em **"Configurações do CRM/Kanban"** (botão no topo) → seção **"Funis"** → expandir o funil → etapas (`components/crm/CrmSettingsDialog.tsx:20-25`; `components/crm/PipelineManagerDialog.tsx:340-366`). Reordenar também **arrastando o cabeçalho da coluna** no quadro (`CRM.tsx:539-582,1037-1052`). Agora há **vários funis** por empresa, cada um com cor e etapas próprias. |
| 3 | Marcar estágio como "ganho" e "perdido" | **Bate, com ajuste** | Interruptores **"Ganho"** e **"Perdido"** só aparecem ao **editar** a etapa (lápis), não ao criar (`components/crm/StageManagerDialog.tsx:174-268,343-366`). Os 5 estágios padrão já vêm com "Fechado (Ganho)" e "Fechado (Perdido)" marcados (`hooks/useCrmStages.ts:62-68`). |
| 4 | Criar oportunidade: título, cliente (ou criar na hora), vendedor, origem, valor, probabilidade, previsão | **Bate** | Janela "Nova Oportunidade" (`components/crm/LeadFormDialog.tsx`). "Vendedor Responsável" agora aceita **vários** (o primeiro é o "Principal") (`:282-327`). Cliente com "Cadastrar "{name}"" na hora. |
| 5 | Arrastar entre estágios e o **motivo da perda** obrigatório | **Bate** | Soltar em etapa "Perdido" abre "Motivo da Perda" (`components/crm/LossReasonDialog.tsx`); soltar em etapa "Ganho" oferece lançar a receita ("Oportunidade ganha") (`CRM.tsx:593-648`). Toda troca de etapa vai para o histórico. |
| 6 | Detalhe do lead: ligar, WhatsApp, e-mail e **interação** com próxima ação | **Bate, maior** | Janela com abas **"Detalhes"**, **"Tarefas (n)"**, **"Histórico (n)"** (`components/crm/LeadDetailModal.tsx:456-463`). Contato com telefone, botão "WhatsApp" e e-mail (`:668-718`). "Nova Interação" na aba Histórico (`:888-965`). Novos: etiquetas, checklists, comentários, "Criar OS", "Criar Tarefa", "Assumir oportunidade". |
| 7 | Filtros: origem, vendedor, faixa de valor, busca | **Bate** | Botão de filtro dentro da busca: "Origem", "Vendedor" (com "Sem responsável"), "Valor Mínimo", "Valor Máximo" (`CRM.tsx:1772-1822`). Busca também por telefone e documento do cliente. |
| 8 | **Webhooks de captação**: criar, vincular a uma origem, copiar a URL e testar | **Bate, sem "testar"** | Seção **"Webhooks"** das configurações (`components/crm/WebhookManagerDialog.tsx`). Agora escolhe também **funil e etapa de destino**. Não existe botão de teste: o teste é um POST externo (seção 3.4.5). |
| 9 | Rotina diária em 5 minutos | **Conceitual** | Sem tela própria. Apoios reais: aba "Tarefas" (vencidas primeiro, `CRM.tsx:331-348`), filtro "Sem responsável", busca. |

Avisos da trilha: ⚠️ 🔒 "sem o módulo CRM a tela nem aparece" → **bate** (`components/layout/SidebarMenuContent.tsx:163-168`;
rota abre a oferta do módulo, `App.tsx:499-519`). ⚠️ "Filtro Origem usa lista fixa" → **bate** (`hooks/useLeads.ts:96-107`),
enquanto o campo do formulário usa o catálogo de origens do T3. ⚠️ "Excluir lead usa a confirmação do navegador" → **bate**
(`LeadDetailModal.tsx:349-353`). ⚠️ "Motivo da perda é texto nas observações" → **bate** (`CRM.tsx:650-667`).
🚫 "formulário público do T3 não cria lead" → **continua valendo**: o envio grava em `customers`
(`supabase/migrations/20261015233000_lead_capture_insert_dinamico_respeita_default.sql:15,317`).

### 0.2 O que mudou desde a 1.22.5 (Changelog, `pages/Changelog.tsx`)

| Versão | Mudança |
|---|---|
| 1.24.22-1.24.30 | "Criar oportunidade no CRM" a partir do cliente abre o formulário completo; botões "Criar OS" e "Criar Tarefa" no card; oferta de lançar receita ao ganhar (`Changelog.tsx:3970,3779-3784,3774`). |
| 1.24.24 / 1.24.28 | Reordenar colunas arrastando o nome; ícone por coluna; origem com cor e ícone no card (`:3926,3833-3838`). |
| 1.24.32 | **Vários responsáveis** por oportunidade; **cada vendedor vê as dele** (quem tem "Gerenciar CRM" vê tudo); fila "Sem responsável" (`:3735-3745`). |
| 1.24.34 | **Vários funis** na mesma empresa; mover oportunidade de funil; funil com conteúdo não pode ser excluído (`:3686-3696`). |
| 1.24.37 | **"Quem pode ver"** por funil, com aviso antes de restringir (`:3600-3605`). |
| 1.24.38-1.24.40 | **Tarefas** dentro da oportunidade e aba **Tarefas** na tela; permissão "Gerenciar Tarefas" (`:3573-3578,3544`). |
| 1.24.46-1.24.50 | Busca esconde etapas vazias; observações com salvamento automático; mudança de etapa no histórico (`:3432,3284-3289`). |
| 1.28.0-1.28.9 | Funis coloridos, configurações reunidas numa janela, **etiquetas**, **checklists**, **comentários**, tarefas em Lista/Kanban/Agenda (`:2681,2576-2581,2513`). |
| 1.36.6 / 1.36.14-1.36.15 | Funil **sem valores** ("Acompanha valores financeiros"); tela **Projetos** com frentes de trabalho; grupo de menu **"CRM e Projetos"** (`:1550-1555,1424-1429,1412`). |
| 1.37.56 | Cards do CRM na API pública (`:145`). Fora do escopo do vídeo. |

### 0.3 O que mais pode surpreender (detalhes na seção 5)

1. Empresa nova **não tem funil**: o primeiro clique em "Começar com estágios padrão" cria o funil **"Funil de Vendas"**
   e as 5 etapas (gatilho no banco).
2. Não há lista no computador; não há botão de testar webhook; a URL do webhook mostra o endereço do servidor.
3. Avisos falam "Lead ... com sucesso!" enquanto os botões falam "oportunidade".
4. Excluir oportunidade e mover de funil usam `confirm()`/`alert()` do navegador (o gravador não mostra).
5. Etapa nova não tem "Ganho/Perdido" no formulário de criação: é preciso salvar e editar.
6. "Projetos" exige "Gerenciar Configurações" para criar/editar, não "Gerenciar CRM".

---

## 1. Rotas e navegação

| Tela | Menu (computador) | Rota |
|---|---|---|
| CRM/Kanban | Grupo **"CRM e Projetos"** → **"CRM/Kanban"** (`SidebarMenuContent.tsx:162-168`) | `/crm` (`lib/i18n/appRouteSlugs.ts:134`) |
| Projetos | Grupo "CRM e Projetos" → **"Projetos"** | `/projetos`; detalhe `/projetos/:id` (`appRouteSlugs.ts:135-136`) |
| Criar oportunidade a partir do cliente | Ficha do cliente → "Ações" → **"Criar oportunidade no CRM"** (`lib/i18n/messages/app/customers.ts:50`; `pages/CustomerDetail.tsx:1974`) | abre a mesma janela com o cliente travado |
| Webhook (entrada externa) | — | `POST https://<projeto>.supabase.co/functions/v1/crm-lead-webhook?token=<token>` (`WebhookManagerDialog.tsx:103-105,229`) |

Guardas: `/crm` exige `screen:crm` + módulo `crm`; `/projetos` exige `screen:projects` + módulo `crm` (`App.tsx:807-809`).
Celular: Menu → "CRM e Projetos" (`components/layout/MoreMenuDrawer.tsx:135`).

---

## 2. Permissões e módulos

| Chave | Rótulo | Efeito nesta área | Fonte |
|---|---|---|---|
| `screen:crm` | "CRM/Kanban" | Entrar na tela | `hooks/usePermissions.ts:64` |
| `screen:projects` | "Projetos" | Entrar em Projetos | `usePermissions.ts:65` |
| `fn:manage_crm` | "Gerenciar CRM" | **Ver todas as oportunidades** do funil (sem ela: só as em que é responsável, co-responsável ou criador) e enxergar funis restritos | `pages/CRM.tsx:139-149`; `crm.ts:327-330` |
| `fn:create_os` (ou admin/gestor) | "Criar OS" | Botões "Criar OS" e "Criar Tarefa" no card e "Nova tarefa" | `LeadDetailModal.tsx:118-119,586-612` |
| `fn:manage_finance` (com permissões gravadas) ou admin/gestor | "Gerenciar Financeiro" | Oferta "Oportunidade ganha" ao soltar em etapa de ganho | `hooks/useCanLaunchLeadRevenue.ts` |
| `fn:manage_settings` ou admin/gestor | "Gerenciar Configurações" | Criar/editar/excluir **projeto** e frentes | `pages/Projects.tsx:131`; `pages/ProjectDetail.tsx:118` |
| `fn:manage_tasks` / `fn:view_all_schedule` | "Gerenciar Tarefas" / "Ver Toda a Agenda" | Quem vê as tarefas dos outros na aba Tarefas | `CRM.tsx:309-319`; `lib/taskVisibility.ts` |

Módulo 🔒 **`crm`** ("CRM/Kanban" — "Funis Kanban, oportunidades, interações e webhooks de captação",
`components/ModuleGateModal.tsx:121-123`): some do menu sem ele; **Projetos usa o mesmo módulo**
(`hooks/useCompanyModules.ts:70-76`). Planos que o incluem: Pro e Business (seed do fakebase: `avancado` e `master`).
Empresa em teste libera tudo.

---

## 3. Por tela, janela e aba

### 3.1 Cabeçalho, indicadores e abas (`pages/CRM.tsx:1667-1840`)

- Título **"CRM/Kanban"**, subtítulo **"Gerencie oportunidades e processos"**, botão **"Configurações do CRM/Kanban"**
  (`crm.ts:13-14,59`; `CRM.tsx:1669-1681`).
- Abas da tela: **"Funil"** e **"Tarefas"** (não ficam lembradas: sempre abre em Funil, `CRM.tsx:252-256`).
- 4 indicadores (só do funil aberto e já com os filtros): **"Total no funil"** (quantidade); **"Valor Total"** (soma) ou
  **"Em andamento"** (quantidade) em funil sem valores; o **nome da 1ª etapa de ganho** com o valor dela; o **nome da 1ª
  etapa neutra** com o valor dela (`CRM.tsx:839-844,1688-1751`).
- Busca **"Buscar por título, cliente, telefone ou documento..."** (título, nome, telefone, celular, e-mail e documento
  do cliente, sem acento) com o botão de filtro embutido; botão **"Nova oportunidade"** (`CRM.tsx:1772-1828`).
- Filtros (contador no botão; "limpar"): **"Origem"** ("Todas" + lista fixa de 10: Indicação, Site, Telefone, WhatsApp,
  Google, Instagram, Facebook, Parceiro, Feira/Evento, Outro), **"Vendedor"** ("Todos", **"Sem responsável"** e cada
  usuário), **"Valor Mínimo"** ("R$ 0") e **"Valor Máximo"** ("R$ 999.999"). Filtros ativos viram etiquetas "Origem: ...",
  "Vendedor: ...", "Min: ...", "Max: ..." com "x" (`CRM.tsx:1832-1866`; `crm.ts:27-49`). Com filtro, aparece "{filtrado} de
  {total}" acima do quadro (`CRM.tsx:932-936`).

### 3.2 O quadro (Kanban) (`CRM.tsx:903-1112`)

- Linha do funil: ícone + **nome do funil aberto** sublinhado na cor dele; à direita, os **outros funis** como abas
  (cada uma com engrenagem "Configurar funil") e o botão **"+"** ("Novo funil") (`components/crm/PipelineTabsBar.tsx:79-84,208-222`).
  O funil escolhido fica lembrado por usuário no navegador (`CRM.tsx:151-189`).
- Coluna (260-300 px): cabeçalho na cor da etapa, ícone, nome, **contador** e o **valor somado** (inclusive "R$ 0,00"; em
  funil sem valores não mostra valor) (`CRM.tsx:1053-1077`). Arrastar o cabeçalho reordena as colunas (dica "Arraste para
  reordenar os estágios"; desligado durante a busca).
- Coluna vazia: **"Sem oportunidades"**. Funil sem nenhuma oportunidade: linha "Toque em "Nova Oportunidade" para começar a
  gerenciar este funil" acima das colunas (`CRM.tsx:995-1006`; texto em `crm.ts:87`).
- Com busca, etapas sem resultado somem e aparece "{n} etapas sem resultado estão ocultas." + **"Mostrar todas"**
  (`CRM.tsx:478-497,1006-1022`).
- Card (`components/crm/LeadCard.tsx`): etiquetas coloridas, **título**, cliente, fotos dos responsáveis (ou etiqueta
  amarela **"Sem responsável"**), **valor**, barra **"Probabilidade"** com % (verde ≥70, amarelo ≥40, vermelho abaixo,
  `:41-45,129-140`), origem com cor/ícone e previsão. Funil sem valores esconde valor/probabilidade.
- Clicar no card abre o detalhe (3.7). Arrastar o card para outra coluna troca a etapa (3.8).

### 3.3 Funil vazio e estágios padrão

- Empresa **sem funil** ou funil **sem etapas**: cartão **"Configure seu funil"** / "Crie os estágios do pipeline pra
  começar a organizar suas oportunidades. Use o conjunto padrão ou monte do seu jeito." com **"Começar com estágios
  padrão"** ("Criando estágios...") e **"Personalizar estágios"** (`CRM.tsx:950-976`).
- "Começar com estágios padrão" grava 5 etapas: **Lead** (cinza), **Proposta** (azul), **Negociação** (amarelo),
  **Fechado (Ganho)** (verde, ganho), **Fechado (Perdido)** (vermelho, perda) (`hooks/useCrmStages.ts:62-68,145-171`). Aviso
  **"Estágios padrão criados!"**. Sem funil, o banco cria antes o **"Funil de Vendas"** padrão
  (`supabase/migrations/20260918100000_crm_multi_pipeline.sql:183-185,322-352`).

### 3.4 Janela "Configurações do CRM/Kanban" (`components/crm/CrmSettingsDialog.tsx`)

Janela larga com 4 seções: **"Funis"**, **"Checklists"**, **"Etiquetas"**, **"Webhooks"** (`:20-25`). Abre pelo botão do
topo, pela engrenagem de cada aba de funil ou pelo "+".

#### 3.4.1 Funis (`components/crm/PipelineManagerDialog.tsx`)

- Título **"Gerenciar Funis"** / "Crie funis separados para vendas, pós-venda, licitação e outros fluxos comerciais. Para
  organizar uma obra com várias frentes ao mesmo tempo, use Projetos." (`crm.ts:289-291`).
- **"Novo funil"** → "Novo Funil": nome ("Nome do funil"), cor e **"Criar"**; legenda "O funil novo nasce vazio: depois de
  criar, use a engrenagem da aba dele para cadastrar as etapas." Aviso "Funil criado com sucesso!".
- Linha de cada funil: setas de ordem, cor, nome, "{n} etapas · {n} oportunidades", "Sem etapas", **"Padrão"**; menu
  **"Editar"** (nome, cor, **"Acompanha valores financeiros"** Sim/Não com a dica "Desligue para funis de projeto ou
  processo: os indicadores passam a contar cards em vez de somar dinheiro."), **"Tornar padrão"**, **"Quem pode ver"**,
  **"Excluir"** ("Remover funil?"; funil com etapas ou oportunidades não pode ser removido) (`:190-340,416-436`; `crm.ts:292-314`).
- Expandir o funil mostra as **etapas** dele (3.4.2).

#### 3.4.2 Etapas (`components/crm/StageManagerDialog.tsx`)

- **"Novo estágio"** → "Novo Estágio": nome ("Nome do estágio"), **ícone** (lista de nomes em inglês, ex. "Users",
  "Globe"), **cor** e **"Adicionar estágio"**. Aviso "Estágio criado com sucesso!" (`:343-366`; `useCrmStages.ts:102-138`).
- Linha: setas de ordem, nome, troféu (ganho) ou X (perdido); menu **"Editar"** / **"Excluir"**. Editar mostra nome, ícone,
  cor e os interruptores **"Ganho"** e **"Perdido"** (ligar um desliga o outro) (`:174-268`). Aviso "Estágio atualizado!".
- Excluir: **"Remover estágio?"** / "Esta ação não pode ser desfeita. Leads neste estágio ficarão sem estágio atribuído."
  (`:438-452`). Lead sem etapa aparece na **1ª coluna** (`CRM.tsx:457-465`).

#### 3.4.3 Quem pode ver (`components/crm/PipelineAccessDialog.tsx`; `crm.ts:316-347`)

"Acesso ao funil": vazio = **"Aberto para toda a empresa"**; com pessoas marcadas = **"Restrito"** (só elas e quem tem
"Gerenciar CRM"). Antes de restringir: "Restringir o acesso a este funil?" com a conta de quem deixa de ver; botão
"Restringir mesmo assim". Aviso "Acesso ao funil atualizado!".

#### 3.4.4 Checklists e Etiquetas (`components/crm/CrmChecklistTemplatesManager.tsx`, `CrmLabelsManager.tsx`)

- **"Modelos de checklist"** / "Padronize etapas que podem ser aplicadas a qualquer oportunidade." Vazio "Nenhum modelo
  cadastrado" / "Crie um checklist reutilizável para seu processo comercial." Campos "Nome do checklist" e "Novo item do
  checklist". Aviso "Modelo de checklist criado".
- **"Etiquetas"** / "Crie marcadores coloridos para identificar oportunidades rapidamente." Campo "Ex.: Urgente, Renovação,
  Cliente VIP" + cor. Vazio "Nenhuma etiqueta cadastrada". Aviso "Etiqueta criada" (`hooks/useCrmCardTools.ts:112`).

#### 3.4.5 Webhooks (`components/crm/WebhookManagerDialog.tsx`)

- **"Webhooks de Leads Externos"** / "Crie endereços seguros para receber novas oportunidades de outros sistemas." (`:132`).
- **"Criar novo webhook"**: **"Nome"** ("Ex: Meta Ads - Campanha Março"), **"Origem padrão"** ("Sem origem fixa" ou uma
  origem **do catálogo de origens do T3**), **"Funil de destino"** ("Selecione o funil") e **"Etapa de destino"** ("Escolha o
  funil primeiro" / "Selecione a etapa"), botão **"Criar webhook"** (`:133-215`). Aviso "Webhook criado com sucesso!".
- **"Webhooks configurados"**: nome, **"Ativo"/"Inativo"**, "Origem: ...", interruptor "Ativo", lixeira (sem confirmação),
  funil e etapa de destino editáveis, **campo com a URL completa (com o token)** e botão de copiar → "URL copiada!"
  (`:218-327`).
- Bloco **"Como usar o webhook"**: POST com JSON; obrigatórios `name` e `phone` (texto da tela); opcionais `email`,
  `source`, `title`, `notes`, `value`; exemplo `{ "name": "João Silva", "phone": "11999999999", "email": "joao@email.com" }`
  e a dica do cabeçalho `x-idempotency-key` (`:330-400`).
- O que o servidor faz (`supabase/functions/crm-lead-webhook/index.ts:97-371`): aceita **só POST**; token na URL, no
  cabeçalho `x-webhook-token` ou no corpo; exige **pelo menos um** de nome, telefone ou e-mail ("Informe ao menos um destes
  campos: name, phone ou email"); título = `title` ou **"Lead via {nome do webhook}"**; origem = a do webhook, senão `source`,
  senão "Webhook Externo"; etapa = a configurada; **cria a oportunidade sem cliente e sem responsável**, com nome, telefone e
  e-mail nas **observações** ("Nome: ...", "Telefone: ...", "Email: ...", "Origem: {webhook}"). Resposta
  `{ success: true, lead }`; token errado/inativo 401 "Webhook inválido ou inativo".

### 3.5 Janela "Nova Oportunidade" / "Editar Oportunidade" (`components/crm/LeadFormDialog.tsx`)

Em funil sem valores o título vira "Novo card"/"Editar card" e alguns campos somem (`:134-160,238-242`).

| Rótulo | Tipo | Obrigatório | Regras |
|---|---|---|---|
| **"Título da Oportunidade \*"** | Texto, "Ex: Instalação de 3 splits" | Sim (`required` do navegador) | — |
| **"Cliente"** | Seletor com busca "Buscar cliente...", "Nenhum cliente", "+" e "Cadastrar "{nome}"" | Não | Vindo da ficha do cliente: travado, com "Cliente definido pela ficha de onde você abriu esta oportunidade." (`:260-280`) |
| **"Vendedor Responsável"** (ou "Responsável") | Seleção múltipla de usuários ("Vendedores") | Não | "O primeiro selecionado vira o responsável principal, que é quem entra nos filtros e relatórios." Etiqueta "Principal" no primeiro (`:282-327`). Lista = todos os usuários da empresa (`useUsers`). |
| **"Origem"** | Seletor do **catálogo de origens** ("De onde veio?", "Buscar origem...", "Não informado") + criar na hora | Não | Some em funil sem valores (`:332-352`). |
| **"Estágio"** | Lista agrupada por funil ("Selecione o estágio", "Não atribuído") | Não | Já vem a 1ª etapa do funil aberto. Escolher etapa de outro funil move a oportunidade (`:356-423`). |
| **"Valor Estimado (R$)"** | Número | Não | Padrão 0. Colar "4.550" vira 4550,00 (`:430-458`). |
| **"Probabilidade (%)"** | Número 0 a 100 | Não | Padrão 50 (`:460-495`). |
| **"Previsão Fechamento"** (ou "Prazo") | Data | Não | — |
| **"Observações"** | Texto longo, "Detalhes da oportunidade..." | Não | — |

Rodapé "Cancelar" / **"Salvar"** ("Salvando..."). Avisos: **"Lead criado com sucesso!"**, **"Lead atualizado com sucesso!"**,
erros "Erro ao criar lead"/"Erro ao atualizar lead" (`hooks/useLeads.ts:235-238,344-347`).

### 3.6 Mudança de etapa (arrastar, menu do celular ou seletor do detalhe) (`CRM.tsx:593-680`)

- Etapa comum: grava e mostra "Lead atualizado com sucesso!"; registra no Histórico **"Mudança de estágio"** — `De "{a}" para
  "{b}"` (`useLeads.ts:256-343`; `crm.ts:175-181`).
- Etapa **"Perdido"**: abre **"Motivo da Perda"** / "Registre o motivo da perda do negócio "{título}"", **"Motivo \*"**
  ("Selecione o motivo": Preço alto, Concorrente escolhido, Sem orçamento, Não respondeu, Projeto cancelado, Fora do escopo,
  Outro), **"Detalhes (opcional)"**, botões "Cancelar" e **"Confirmar Perda"** (desligado sem motivo). Grava "Motivo da perda:
  {motivo}" no fim das Observações (`components/crm/LossReasonDialog.tsx:27-100`; `crm.ts:246-265`). Cancelar = card não muda.
- Etapa **"Ganho"**: grava e, se a pessoa pode lançar no Financeiro e a oportunidade ainda não gerou receita, abre
  **"Oportunidade ganha"** / "Quer lançar a receita desta venda?" com "Oportunidade", "Cliente", **"Valor a lançar"** e os
  botões **"Agora não"** e **"Sim, lançar receita"** (abre a conta a receber, assunto do T13)
  (`lib/i18n/messages/app/finance.ts:1530-1545`; `hooks/useLeadWonRevenuePrompt.ts:39-94`).

### 3.7 Detalhe da oportunidade (`components/crm/LeadDetailModal.tsx`)

- Cabeçalho: título, cliente, **"Editar"** e lixeira (**`confirm()` do navegador**: "Tem certeza que deseja excluir este
  lead?"; aviso "Lead removido com sucesso!") (`:429-447,349-353`).
- Abas **"Detalhes"**, **"Tarefas ({n})"**, **"Histórico ({n})"** (`:456-463`).
- **Detalhes**: "Funil:" (só com mais de um funil; "Mudar o funil move esta oportunidade para a primeira etapa do funil
  escolhido." + `confirm()`), "Estágio:", "Responsáveis:" com "Principal" ou **"Sem responsável"** + **"Assumir
  oportunidade"** ("Você vira responsável e ela sai da fila compartilhada."; aviso "Oportunidade assumida!"), botões
  **"Criar OS"** e **"Criar Tarefa"**, quadros "Valor Estimado", "Probabilidade", "Previsão Fechamento", "Origem",
  **"Contato do Cliente"** (telefone clicável `tel:`, botão verde **"WhatsApp"**, e-mail `mailto:`), **"Observações"** com
  salvamento automático ("Salvando..." → "Salvo"), "Criado em:", "Atualizado:", **"Etiquetas da oportunidade"**,
  **"Checklists da oportunidade"** ("Checklist em branco" ou modelo; "Adicionar item") e, ao lado, **"Comentários e
  atividades"** ("Escreva um comentário..." + "Comentar") (`:470-775`).
- **Tarefas**: "Nova tarefa" (mesma janela de tarefa da Agenda, T5); vazio "Nenhuma tarefa nesta oportunidade"; marcar
  "Concluir"/"Reabrir"; excluir com `confirm()` (`:780-880`).
- **Histórico**: **"Nova Interação"** → "Registrar Interação": **"Tipo de Interação \*"** (Ligação, E-mail, WhatsApp,
  Reunião, Visita, Proposta Enviada, Outro), **"Próxima Ação"** ("Ex: Enviar proposta"), **"Descrição \*"** ("Descreva o que
  foi conversado..."), **"Data da Próxima Ação"**, botão **"Registrar"**. Aviso "Interação registrada!". Vazio "Nenhuma
  interação registrada" / "Clique em "Nova Interação" para registrar o primeiro contato". Linhas com "Próxima ação:"
  (`:888-1020`; `useLeads.ts:466-505`). A próxima ação **não vira tarefa** nem aparece na Agenda.

### 3.8 Aba "Tarefas" da tela (`CRM.tsx:1256-1440`)

Tarefas ligadas a oportunidades de **todos os funis comerciais**: busca "Buscar tarefa ou oportunidade...", filtro
"Responsável", visões **"Lista"**, **"Kanban"**, **"Agenda"** (lembrada no navegador), vencidas primeiro, ações de concluir,
editar e excluir na linha. Vazio: "Nenhuma tarefa vinculada a oportunidades" / "Crie tarefas dentro de uma oportunidade
para acompanhá-las aqui." (`crm.ts:374-394`).

### 3.9 Projetos (acompanhamento de obras e processos)

- **Lista** (`pages/Projects.tsx`): título "Projetos" / "Acompanhe obras e projetos com suas frentes de trabalho";
  indicadores "Projetos", "Em andamento", "Atrasados", "Concluídos"; busca "Buscar por nome, código ou cliente..."; filtro
  "Status"; tabela "Código" (`#{n}`), "Projeto", "Cliente", "Prazo", "Progresso", "Status", "Ações"; botão **"Novo projeto"**.
  Vazio: "Nenhum projeto ainda" / "...Cada frente é um quadro Kanban, igual ao do CRM." + "Criar projeto"
  (`projects.ts:8-58`; `Projects.tsx:203-206,373-379`).
- **Formulário** "Novo projeto": "Nome do projeto" ("Ex: Instalação de 80 splits, Indústria X"; obrigatório: "Informe o nome
  do projeto"), "Cliente" ("Projeto interno (sem cliente)"), "Responsável", "Status" (Planejada, Em andamento, Pausada,
  Concluída, Cancelada), "Início previsto", "Prazo final", "Descrição", "Cor". Avisos "Projeto criado com sucesso!" etc.
  O código `#n` é gerado pelo banco (`hooks/useProjects.ts:98-105`).
- **Detalhe** `/projetos/:id`: subtítulo `#{código}`; abas **"Visão geral"** (cliente, responsável, prazo, "Progresso da obra",
  "Frentes de trabalho"), **"Frentes"** (um quadro Kanban por frente, "Novo card", "Nova frente", "Gerenciar etapas") e
  **"Tarefas"** (Kanban/Agenda) (`projects.ts:85-145`; `ProjectDetail.tsx:648`).
- **Frente** = funil com `project_id` e **sem valores**; nasce com as etapas **"A fazer"**, **"Em execução"**, **"Concluído"**
  (ganho) (`hooks/useProjectPipelines.ts:18-27,95-131`). Aviso "Frente de trabalho criada!".
- **Progresso** = cards em etapa de ganho ÷ cards não perdidos, pela RPC `project_progress_summary`
  (`hooks/useProjectProgress.ts:1-49`). Sem etapa de ganho: "Configure uma etapa de ganho em alguma frente para ver o progresso".

### 3.10 Celular

Cabeçalho "CRM/Kanban" / "Funil Kanban"; lista por padrão (Kanban pelo filtro "Visualização"); botão "Lead"; chips de etapa
filtram a lista; menu da linha "Mover para {etapa}", "Editar" (`CRM.tsx:1560-1660`; `crm.ts:15-17,52-54`).

---

## 4. Backend por tela

### 4.1 Ao abrir `/crm`

| Chamada | Detalhe | Fonte |
|---|---|---|
| `GET leads` | `select=*,customers(id,name,phone,celular,email,document),crm_stages(id,name,color),lead_assignees(user_id,is_primary)`, `order=updated_at.desc`; depois `GET profiles?select=user_id,full_name,avatar_url&user_id=in.(...)` | `hooks/useLeads.ts:113-147` |
| `GET crm_stages?select=*&order=position.asc` | Todas as etapas (o app separa por funil) | `useCrmStages.ts:89-99` |
| `GET crm_pipelines?select=*&project_id=is.null&order=position.asc` | Funis comerciais | `hooks/useCrmPipelines.ts:104-115` |
| `GET crm_labels?select=id,name,color&order=name.asc` | Etiquetas dos cards | `useCrmCardTools.ts:82-96` |
| Usuários (`profiles`, `user_roles`, `user_permissions`) | Filtro "Vendedor" | `hooks/useUsers.ts` (ver T2) |
| `GET service_orders` (consulta completa) | Aba Tarefas (`entry_type = 'tarefa'` com `lead_id`) | `CRM.tsx:261,301-307` |
| `GET teams`, `GET team_members`, `GET profiles` | Visibilidade de tarefas | `CRM.tsx:136-138,262-263` |

### 4.2 Ações

| Ação | Chamadas |
|---|---|
| "Começar com estágios padrão" | `GET profiles` (empresa) + `POST crm_stages` com **lista de 5 linhas** `{ name, color, is_won, is_lost, position, company_id, pipeline_id? }` pedindo retorno; **sem `pipeline_id` o banco cria/acha o "Funil de Vendas"** (gatilho `trg_crm_stages_resolve_pipeline`) |
| Funil: criar / editar / padrão / ordem / excluir | `POST crm_pipelines` `{ name, color, position, company_id, is_default: false }`; `PATCH crm_pipelines?id=eq.`; padrão = 2 PATCH (tira o antigo, põe o novo); excluir `DELETE crm_pipelines?id=eq.` (`useCrmPipelines.ts:127-284`) |
| Etapa: criar / editar / excluir / reordenar | `POST crm_stages` `{ ..., position, company_id }`; `PATCH crm_stages?id=eq.`; `DELETE`; reordenar = N `PATCH { position }` (`useCrmStages.ts:102-246`) |
| "Quem pode ver" | `GET crm_pipeline_access?select=*`; salvar = `DELETE` + `POST` das linhas do funil (`hooks/useCrmPipelineAccess.ts:44-90`) |
| Etiquetas / modelos de checklist | `crm_labels` e `crm_checklist_templates` (insert/update/delete); no card: `GET leads?select=crm_label_ids,crm_checklists&id=eq.` e `PATCH leads` com `crm_label_ids`/`crm_checklists` (`useCrmCardTools.ts:82-240`) |
| Webhook | `GET profiles?select=company_id` (`.single()`), `GET crm_webhooks?select=*&order=created_at.desc`, `POST crm_webhooks` `{ company_id, name, origin, pipeline_id, stage_id, created_by }` (o **token vem do banco**), `PATCH` (ativo/funil/etapa), `DELETE` (`hooks/useCrmWebhooks.ts:30-120`). Lista de origens: `GET customer_origins`. |
| "Salvar" (nova) | `GET /auth/v1/user`; `POST leads` com `{ title, customer_id, value, probability, source, stage_id, expected_close_date, notes, created_by }` pedindo o objeto; depois `DELETE lead_assignees?lead_id=eq.` + `POST lead_assignees` `[{ lead_id, user_id, is_primary }]` (`useLeads.ts:183-239`) |
| Trocar etapa | `PATCH leads?id=eq.` `{ stage_id }` (perda: + `notes`); `GET crm_stages?select=id,name,pipeline_id&id=in.(...)`; (troca de funil: `GET crm_pipelines?select=id,name&id=in.(...)`); `POST lead_interactions` `{ lead_id, interaction_type: 'stage_change', description, created_by }` (`useLeads.ts:241-349`) |
| Ganho | `GET leads?select=won_transaction_id&id=eq.` antes de oferecer (`hooks/useLeadWonRevenue.ts:38-49`) |
| Observações (auto) | `PATCH leads` `{ notes }` sem aviso de sucesso (`useLeads.ts:357-374`) |
| "Assumir oportunidade" | `PATCH leads` `{ assigned_to: <eu> }` (o banco espelha em `lead_assignees`) (`useLeads.ts:383-405`) |
| Excluir | `DELETE leads?id=eq.` (`useLeads.ts:407-425`) |
| Histórico / "Registrar" / "Comentar" | `GET lead_interactions?select=*&lead_id=eq.&order=created_at.desc`; `POST lead_interactions` `{ lead_id, interaction_type, description, next_action, next_action_date }` (comentário = `'comentario'`) (`useLeads.ts:466-505`; `LeadDetailModal.tsx:341-347`) |
| "Criar OS" / "Criar Tarefa" | Formulários de OS/tarefa (T5): `POST service_orders` etc. |
| Projetos | `GET projects?select=*&order=created_at.desc`; `POST projects` (`company_id`, `created_by`; código pelo banco); `POST /rest/v1/rpc/project_progress_summary` (sem argumentos) → `[{ project_id, done_count, active_count, lost_count, has_won_stage }]`; frente = `POST crm_pipelines` `{ ..., project_id, tracks_value: false }` + `POST crm_stages` (3 linhas) (`useProjects.ts:77-170`; `useProjectPipelines.ts:68-190`) |

### 4.3 Gatilhos do banco que mudam a tela (o backend falso precisa imitar)

1. `crm_stages` sem `pipeline_id` → acha/cria o funil padrão **"Funil de Vendas"** (`is_default`, posição 0)
   (`20260918100000_crm_multi_pipeline.sql:155-190,322-352`).
2. `leads`: `pipeline_id` sempre = funil da etapa (`:379-420`), senão o card some do funil aberto.
3. `lead_assignees` ↔ `leads.assigned_to`: o principal espelha nos dois sentidos (migração `20260917150000_...`; citada em
   `useLeads.ts:171-182,377-382`).
4. `crm_webhooks.token` = 64 caracteres hexadecimais por padrão.
5. `projects.code` = contador por empresa (`trg_set_project_code`, `useProjects.ts:98-105`).

### 4.4 Comparação com o backend falso (`/home/claude/domiflix/rec/fakebase`)

| Item | Hoje | Falta |
|---|---|---|
| `leads`, `crm_stages`, `crm_pipelines` | Sem seed (aparecem no `desconhecidos.log` como `TABELA_SEM_SEED`) | Começar vazio é o que o capítulo 1 precisa. Estados intermediários em `seeds-extra/t10/`. |
| Gatilhos 4.3 | **Nenhum** (`rec/fakebase/hooks/` só tem customers, equipment, lead_capture_forms) | Hooks `crm_stages.mjs` (funil padrão), `leads.mjs` (pipeline pela etapa; espelho do responsável), `lead_assignees.mjs`, `crm_webhooks.mjs` (token), `projects.mjs` (código). Sem o 1, "Começar com estágios padrão" grava etapas **sem funil** e o quadro continua vazio. |
| Embeds `customers(...)`, `crm_stages(...)`, `lead_assignees(...)` | Resolvidos pelo schema (`core/schema.mjs:42-76`) | Conferir no smoke (a confirmar). |
| `customer_origins` (catálogo do T3: Indicação, Instagram, Google, WhatsApp, Site) e clientes do T3 | **Coberto** (`seeds/gen-02-cadastros.json`, `seeds-extra/t3/apos-cap10.json`) | — |
| Função `crm-lead-webhook` | **Sem handler** | Handler com o contrato da seção 3.4.5, se o vídeo mostrar um lead chegando. Disparo: passo `eval` do robô com `fetch` para `http://127.0.0.1:54321/functions/v1/crm-lead-webhook?token=...` (local, não é desviado pelo `rec/recorder/net.mjs`). |
| RPC `project_progress_summary` | **Sem handler** (devolve `[]`): a lista mostra "Configure uma etapa de ganho..." | Handler que conta os cards por frente. |
| `lead_interactions`, `crm_labels`, `crm_checklist_templates`, `crm_pipeline_access`, `crm_webhooks`, `projects`, `lead_assignees` | Tabelas conhecidas, sem seed | Vazias no começo. |
| `service_orders`, `teams` | Vazias | Aba Tarefas vazia (ok). |
| `confirm()`/`alert()` nativos | O gravador não mostra janelas do navegador (`rec/README.md`, "Limites") | Evitar excluir oportunidade e trocar de funil pelo seletor na gravação. |
| Arrastar card (HTML5 drag-and-drop) | Passo `drag {target, to}` do robô | Confirmar que o `drop` nativo dispara (a confirmar). |
| URL do webhook | O build usa `VITE_SUPABASE_PROJECT_ID` = `domiflix-fake` (`rec/env.json`) | A tela vai mostrar `https://domiflix-fake.supabase.co/functions/v1/crm-lead-webhook?token=...` (decisão no plano). |

---

## 5. Pegadinhas para roteiro e gravação

**[handoff]** = vale pedir correção ao time do app.

1. No computador não existe a visão em lista do funil; ela só existe no celular (`CRM.tsx:236-237,785-812`).
2. **[handoff]** Avisos dizem "Lead criado/atualizado/removido com sucesso!" (`useLeads.ts:235,344,421`) e os botões dizem
   "Nova oportunidade"; o texto do funil vazio diz "Toque em "Nova Oportunidade"" mesmo no computador (`crm.ts:87`).
3. **[handoff]** Excluir oportunidade, trocar de funil pelo seletor e excluir tarefa usam `confirm()`/`alert()` do navegador
   (`LeadDetailModal.tsx:304-312,349-353,383`), diferente do resto do sistema; o gravador não captura essas janelas.
4. Etapa nova não oferece "Ganho"/"Perdido" ao criar; só no "Editar" (`StageManagerDialog.tsx:343-366` × `:205-250`).
5. **[handoff]** O seletor de ícone da etapa lista nomes em inglês ("Users", "Globe"...) sem desenho no formulário de criação
   (`StageManagerDialog.tsx:360`).
6. A dica "Arraste para reordenar os funis/estágios" aparece na janela, mas lá a ordem é por setas; arrastar funciona no
   cabeçalho das colunas do quadro (`PipelineManagerDialog.tsx:261-262`; `CRM.tsx:1037-1052`).
7. Filtro "Origem" = lista fixa de 10 (`useLeads.ts:96-107`); o campo Origem da oportunidade = catálogo do T3. Uma origem
   criada pela empresa que não esteja na lista fixa não aparece no filtro. Com o catálogo do T3 (Indicação, Instagram,
   Google, WhatsApp, Site) todas existem no filtro.
8. "Motivo da perda" vira texto nas Observações (`CRM.tsx:650-667`); não há relatório de motivos.
9. **[handoff]** A fila "Sem responsável" é descrita no Changelog 1.24.32 como visível para todos (`Changelog.tsx:3745`), mas a
   tela esconde de quem não tem "Gerenciar CRM" toda oportunidade em que a pessoa não é responsável nem criadora,
   inclusive as sem responsável (`CRM.tsx:141-149`). Para a administradora nada muda (a confirmar com vendedor).
10. Lead que chega por webhook não tem cliente: nome, telefone e e-mail ficam só nas Observações
    (`crm-lead-webhook/index.ts:315-323`); o "Contato do Cliente" do detalhe não aparece.
11. A tela de webhooks diz que `name` **e** `phone` são obrigatórios; o servidor aceita qualquer um de nome, telefone ou
    e-mail (`WebhookManagerDialog.tsx:353-362` × `index.ts:168-170`) **[handoff de copy]**.
12. Não existe botão "testar webhook"; a URL exibida traz o **token** (segredo) e o endereço do projeto
    (`WebhookManagerDialog.tsx:229,321-326`). No vídeo, o token é fictício, mas o domínio aparece.
13. Excluir webhook (lixeira) não pede confirmação (`WebhookManagerDialog.tsx:256-262`).
14. A "Próxima Ação" da interação é só texto e data no histórico: não gera tarefa nem lembrete (`useLeads.ts:480-505`).
15. Probabilidade e valor somem em funil sem valores; "Origem" também (`LeadFormDialog.tsx:332-352`).
16. **[handoff]** Projetos: criar/editar exige "Gerenciar Configurações" (`Projects.tsx:131`), não "Gerenciar CRM".
17. O indicador "Valor Total" e os cards somam **o funil aberto com os filtros**, não a empresa toda (`CRM.tsx:494-497`).
18. Os 4 indicadores mostram o nome da **primeira** etapa de ganho e da **primeira** neutra (normalmente "Lead"), não a
    soma do pipeline em andamento (`CRM.tsx:839-844`).
19. Oferta "Oportunidade ganha" só para admin/gestor ou quem tem "Gerenciar Financeiro" **gravado** (`useCanLaunchLeadRevenue.ts`).
20. Excluir etapa com oportunidades: elas ficam sem etapa e passam a aparecer na 1ª coluna (`CRM.tsx:457-465`).

---

## 6. 🚫 Não prometer / telas mortas

- 🚫 O formulário de captação do T3 criar oportunidade no CRM: ele cria **cliente** (seção 0.1).
- 🚫 Importar leads em massa; 🚫 distribuição automática por vendedor (nada no código).
- 🚫 Oportunidade virar contrato ou orçamento automaticamente: o caminho do card é "Criar OS"/"Criar Tarefa". Contrato é
  montado do zero (T11).
- 🚫 Testar webhook dentro do sistema; 🚫 integração pronta com Meta Ads/Google Ads (o webhook recebe qualquer POST; o
  exemplo "Meta Ads" é só nome).
- 🚫 Lembrete automático da "Próxima Ação".
- 🚫 Relatório de motivos de perda.
- 🚫 Visão em lista do funil no computador.
- 🚫 A avaliação DISC tem relação com CRM (é do RH, T22).
- Não há telas mortas próprias do CRM; os rótulos "Gerenciar estágios", "Gerenciar funis" e "Configurar webhooks" existem no
  i18n (`crm.ts:57-59`) mas não são usados por nenhuma tela.

---

## 7. Dúvidas em aberto

1. O robô consegue arrastar card e cabeçalho de coluna (drag-and-drop nativo) e o app recebe o `drop`?
2. Vendedor sem "Gerenciar CRM" enxerga as oportunidades "Sem responsável"? (item 9).
3. Toasts empilhados ao soltar em "Ganho": "Lead atualizado com sucesso!" + janela "Oportunidade ganha" (ordem visual).
4. Projetos sem nenhuma frente: o que aparece na coluna "Progresso" (texto de etapa de ganho?).
5. O seletor de "Estágio" do formulário mostra os funis de projeto? (`LeadFormDialog.tsx:356-423` filtra por `projectId`; a
   confirmar com frente criada).
6. Qual URL o Kaik quer exibida no webhook (domínio `domiflix-fake.supabase.co` do build falso).
