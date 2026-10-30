# Inventário funcional · T2 — Usuários, cargos e permissões (Dominex)

> Base para o roteiro do tutorial "T2 · Usuários, cargos e permissões" da Domiflix.
> Levantado em 30/10/2026 contra o código publicado `APP_VERSION = "1.38.6"` (`src/config/version.ts:1`), cópia em
> `/home/claude/domiflix/src-1.38.6`. **Análise estática, somente leitura**: nada foi executado. O que só se confirma com o
> app rodando está marcado "(a confirmar)" e repetido na seção 7.
> Formato e convenções iguais ao inventário do T3 (`_referencia/T03_inventario_exemplo.md`).

## Como ler

- Caminhos relativos a `src/`, exceto os que começam com `supabase/`. Formato `arquivo:linha`.
- Texto entre aspas "assim" é o rótulo exato da tela (pt-br). Fonte principal: `lib/i18n/messages/app/settings.ts:986-1135`
  (bloco `users`). Alguns textos são fixos no componente e estão citados onde aparecem.
- `screen:...` = permissão de tela; `fn:...` = permissão de ação ("função"). "Cargo" = registro de `permission_presets`
  (o código chama de *preset*). "Desktop" = janela de 1024 px ou mais (abaixo disso o app usa o layout de celular).
- Comportamentos de componentes compartilhados (lista com ficha ao lado, janelas `ResponsiveModal`, toasts) estão no
  inventário do T3, seções 7.1, 7.2 e 7.6; aqui só o que muda.

---

## 0. Resumo para quem escreve o roteiro

### 0.1 Capítulos da trilha (v1.22.5) contra o código de hoje

| # | Item da trilha | Situação | O que ajustar |
|---|---|---|---|
| 1 | Onde fica: Configurações → **Usuários e Permissões** | **Bate** | Botão "Configurações" no rodapé do menu lateral (`components/layout/SidebarMenuContent.tsx:708-718`), aba "Usuários e Permissões" (`pages/Settings.tsx:105-111`, rótulo em `settings.ts:31`). URL `/configuracoes?tab=usuarios`; `/usuarios` redireciona para lá (`App.tsx:865`). A aba só aparece com `screen:users` (`Settings.tsx:140-141`). |
| 2 | Criar usuário: dados, foto, **papel**, senha e vínculo com o funcionário do RH | **Parcial** | Não existe escolha de "papel" (Administrador/Gestor). O formulário tem só o interruptor **"Tipo de Usuário"**: "Interno" ↔ "Técnico" (`components/users/UserFormDialog.tsx:316-336`). O acesso real vem das permissões (coluna da direita da mesma janela). Vínculo: campo "Vincular a Funcionário" (`:258-313`), que lista a tabela de funcionários (vazia sem cadastro no RH). |
| 3 | O **editor de permissões** novo: busca, tela por tela, ações dentro de cada tela | **Bate** | `components/users/PermissionsEditor.tsx`. 25 telas em 7 categorias, 30 ações, cada ação dentro da sua tela (seção 3.5). Busca ignora acento e espaço (`components/users/permissionSearch.ts:1-13`). |
| 4 | Chip **Acesso Total** e por que não quebra com tela nova | **Bate** | Grava o curinga `*` (`UserFormDialog.tsx:152-158`), que libera inclusive telas futuras (`contexts/AuthContext.tsx:383-395`). Dica do chip: "Libera todas as telas e ações, inclusive as que forem criadas no futuro" (`settings.ts:1095`). Desde a 1.37.38 dá para alternar Acesso Total ↔ Personalizado sem perder a seleção manual (`PermissionsEditor.tsx:115-134`; Changelog 1.37.38). |
| 5 | **Aba Cargos**: criar, duplicar, aplicar num usuário, efeito de desmarcar | **Mudou** | No computador **não há aba Cargos**: é o botão **"Configurações"** do topo, que abre a janela **"Configurações de Cargos"** (`pages/Users.tsx:544-547`, `components/users/PermissionPresetDialog.tsx:84-91`). **"Duplicar" só existe no celular** (aba "Cargos", `components/users/PresetListMobile.tsx:67-69`). Aplicar = chip com o nome do cargo em "Perfis rápidos" no formulário do usuário. Desmarcar qualquer permissão apaga o chip e desfaz o vínculo com o cargo (seção 3.6). |
| 6 | Caso real: técnico só do link de campo, ação-filha sem a tela-mãe | **Bate** | A ação fica ligável com a tela desligada e aparece "A tela está desligada, mas estas ações continuam valendo por conta própria." (`PermissionsEditor.tsx:41-43,249-251`; `settings.ts:1100`). Ação do caso: **"Editar OS em campo"** (`fn:editar_os_campo`, `hooks/usePermissions.ts:132`), usada no link da OS (`pages/TechnicianOS.tsx:804`). |
| 7 | Ativar × desativar × excluir, e a vaga do plano | **Bate, com ajuste** | Botões "Desativar", "Reativar" e "Excluir" no painel do usuário (`components/users/UsersMasterDetail.tsx:133-146`). Desativar libera a vaga e derruba a sessão (`supabase/functions/manage-user/index.ts:133-168`). "Reativar" fica desligado sem vaga livre (`UsersMasterDetail.tsx:140`). Excluir pede confirmação "Excluir usuário permanentemente?". |
| 8 | Limite de usuários e como contratar mais | **Bate** | Faixa "Limite de usuários atingido ({count}/{max})" com "Contratar mais usuários" (`Users.tsx:557-566`), janela "Limite de usuários atingido" que leva a `/assinatura?addUsers=1` (`components/UserLimitModal.tsx:27-63`). |

Avisos da trilha: ⚠️ "não dá para desativar/excluir/trocar o papel do próprio usuário" → **parcial**: Desativar,
Reativar e Excluir somem para você (`UsersMasterDetail.tsx:136-144`), mas "Editar" continua e o interruptor
Interno/Técnico aparece; rebaixar o **último** administrador é bloqueado com "Ação bloqueada" (`Users.tsx:146-152,312-324`).
⚠️ "Reativar bloqueia sem vaga" → **bate**. ⚠️ "Excluir lançamento financeiro é separado e não vem ligado" → **bate**
(`fn:delete_finance`, `usePermissions.ts:111`; usuário novo começa com nenhuma permissão, `UserFormDialog.tsx:67-78`).

### 0.2 O que mudou desde a 1.22.5 (Changelog do app, `pages/Changelog.tsx`)

| Versão | Mudança | Efeito no T2 |
|---|---|---|
| 1.24.12 | Nova permissão **"Exportar Dados da Empresa"** (`Changelog.tsx:4265`) | Ação dentro de "Configurações" (`usePermissions.ts:123`). |
| 1.24.23 | Nova permissão **"Lançar Receita ao Finalizar OS"** (`Changelog.tsx:3943`) | Ação dentro de "Ordens de Serviço" (`usePermissions.ts:118`). |
| 1.24.32 / 1.24.37 | CRM: cada vendedor vê só as oportunidades dele; funil com "Quem pode ver" (`Changelog.tsx:3740,3600`) | "Gerenciar CRM" passa a significar "ver o funil inteiro" (T10). |
| 1.24.40 | Nova permissão **"Gerenciar Tarefas"** (`Changelog.tsx:3544`) | Ação dentro de "Agenda" (`usePermissions.ts:138`). |
| 1.29.0 | Planos com 5, 10 e 15 usuários; usuário extra R$ 20 (`Changelog.tsx:2213`) | Número do contador e do limite (seção 3.8). |
| 1.31.0 | Plano EXCEÇÃO até 3 usuários, sem Orçamentos e Financeiro (`Changelog.tsx:2157`) | Essas telas somem do menu mesmo marcadas (`lib/subscriptionCatalog.ts:11-23`). |
| 1.36.2 | Tela renomeada **"Clientes e Fornecedores"** também nas permissões (`Changelog.tsx:1603`) | Rótulo de `screen:customers` (`usePermissions.ts:63`). |
| 1.36.15 | Grupo de menu **"CRM e Projetos"**, permissões separadas (`Changelog.tsx:1412`) | Nova tela **"Projetos"** (`screen:projects`, `usePermissions.ts:65`). |
| 1.37.8 | Contas bancárias com acesso separado (`Changelog.tsx:1011`) | Ações "Usar Contas Bancárias" e "Gerenciar Contas Bancárias" (`usePermissions.ts:113-114`). |
| 1.37.38 | Alternar Acesso Total ↔ Personalizado sem perder a seleção (`Changelog.tsx:461`) | Chip "Personalizado" devolve a última seleção manual. |
| 1.37.53 | Configurações e Usuários com abas mais claras, **lista com detalhes** e formulário maior (`Changelog.tsx:201`) | Tela atual em mestre-detalhe (seção 3.2) e formulário de 2 colunas (seção 3.4). |
| 2026-10 | Add-on **PDV e Loja** | 6 telas novas na categoria "PDV e Loja" do editor (`usePermissions.ts:46,77-86`). |

### 0.3 O que mais pode surpreender (detalhes na seção 5)

1. A linha da **própria administradora** mostra "0 permissões", "Personalizado" e "Nenhuma permissão foi concedida."
   (ela tem acesso total pelo papel). O mesmo vale para técnicos antigos sem permissões gravadas.
2. Criar, editar ou excluir usuário **recarrega a página inteira** (`Users.tsx:132,212,274`).
3. Salvar uma edição dispara até três avisos seguidos ("Role atualizada com sucesso!", "Permissões atualizadas!",
   "Usuário atualizado!").
4. O botão dos cargos se chama **"Configurações"** e abre "Configurações de Cargos".
5. Excluir cargo no computador é **imediato, sem confirmação** (lixeira).
6. Editar um cargo **não muda** quem já usa o cargo.
7. Técnico criado **sem nenhuma permissão marcada** fica sem registro de permissões e passa a ver **todas** as telas
   (modo legado).
8. Não existe escolher "Administrador" ou "Gestor" na tela; só "Interno" ou "Técnico".

---

## 1. Rotas e navegação

| Tela | Caminho no menu (computador) | Rota |
|---|---|---|
| Configurações | Botão **"Configurações"** (ícone de engrenagem) no rodapé do menu lateral, ao lado de "Sair" (`SidebarMenuContent.tsx:708-728`; rótulos em `lib/i18n/messages/app/shell.ts:87-88`). No layout de barra superior: `components/layout/TopNavbar.tsx:468`. Celular: Menu → `components/layout/MoreMenuDrawer.tsx:563`. | `/configuracoes` (exige `screen:settings`, `App.tsx:866`) |
| Usuários e Permissões | Aba "Usuários e Permissões" da página Configurações (barra de abas horizontal no topo, `components/SettingsSidebarLayout.tsx:58-63,117-121`) | `/configuracoes?tab=usuarios` (`Settings.tsx:56,123-126`) |
| Endereço antigo | — | `/usuarios` → redireciona (`App.tsx:865`) |
| Assinatura (contratar mais usuários) | Janela de limite → "Contratar mais usuários" | `/assinatura?addUsers=1` (`UserLimitModal.tsx:55-58`) |

- Página: título "Configurações", subtítulo "Gerencie as configurações do sistema" (`settings.ts:26-27`) e, no canto, o
  selo do salvamento automático das configurações ("Salvando…", "Alterações não salvas", "Salvo", `settings.ts:40-44`;
  `Settings.tsx:1902-1928,1932-1937`). O selo continua aparecendo na aba de usuários, mas se refere às outras abas.
- Abas na ordem: "Empresa", "Regional", "Usuários e Permissões", "Usabilidade", "Atalhos", "Aparência", "Integrações"
  (`settings.ts:28-36`).
- O componente da aba é a página antiga `pages/Users.tsx`, carregada sob demanda (`Settings.tsx:54,1885-1890`).
- Para quem não tem `screen:settings` o botão "Configurações" continua visível no rodapé do menu (não há checagem em
  `SidebarMenuContent.tsx:708-718`), mas a rota redireciona para a tela inicial da pessoa (`App.tsx:360-382`) (a confirmar).

---

## 2. Permissões e módulos

### 2.1 Quem enxerga e quem mexe nesta tela

| Item | Regra | Fonte |
|---|---|---|
| Aba "Usuários e Permissões" | `screen:users` ("Usuários") | `Settings.tsx:141` |
| Botões "Criar Usuário", "Editar", "Desativar", "Reativar", "Excluir" e o painel de ações | `canManageRoles` = papel `admin` ou `gestor`, ou `fn:manage_users`, ou curinga `*`, ou **27 ou mais permissões marcadas**, ou empresa sem nenhum admin | `hooks/useUsers.ts:123-125` |
| Botão "Configurações" (cargos) | Aparece para todos que entram na aba; gravar exige `can_manage_users` no banco | `Users.tsx:544-547`; política em `supabase/migrations/20260308205452_dfbeb640-8f8f-4e3d-a654-e529ef722372.sql:71-81` |
| Servidor (criar/gerenciar) | Função `can_manage_users`: admin/gestor, acesso total, `*` ou `fn:manage_users` | `supabase/migrations/20260610180000_wildcard_star_permission_server_side.sql:28-48`; `supabase/functions/create-user/index.ts:144-151` |

### 2.2 Como o app decide o que cada pessoa vê (`contexts/AuthContext.tsx:186-221,373-395`)

1. Papel **`admin`** (ou `super_admin`): passa em toda tela e ação, com ou sem permissões gravadas.
2. Existe linha em `user_permissions` para a pessoa (**modo estrito**): vale **só** o que a lista tem, ou tudo com `*`.
   Linha com `is_active = false` = sem acesso nenhum.
3. **Sem** linha em `user_permissions` (**modo legado**): qualquer papel (`tecnico`, `gestor`...) libera **tudo**.
4. Depois disso, a tela ainda passa pelo **módulo contratado** (`hooks/useCompanyModules.ts:224-232`) e pelo
   **plano** (`lib/subscriptionCatalog.ts:11-23`: o plano Exceção bloqueia Orçamentos e Financeiro).
5. Menu lateral: cada item exige `hasScreenAccess` + `hasScreen` + módulo (`SidebarMenuContent.tsx:312-321`).
   Rota: `PermissionRoute` redireciona para a primeira tela permitida na ordem Agenda → Ordens de Serviço → Clientes →
   Equipamentos → Dashboard → PDV, senão `/perfil` (`App.tsx:251-311,360-382`).
6. "Gestor" não é acesso total no menu: com permissões gravadas, segue a lista; algumas ações liberam pelo papel
   (`isAdminOrGestor`, ex.: editar OS, `pages/ServiceOrders.tsx:183`).

### 2.3 Catálogo completo (`hooks/usePermissions.ts:36-139`) — 25 telas, 30 ações

Ordem e nomes exatamente como no editor. Entre parênteses, o contador "n/m" que aparece na linha da tela.

| Categoria | Tela (chave) — descrição curta | Ações dentro da tela (chave) |
|---|---|---|
| **Geral** | "Dashboard" (`screen:dashboard`) — Painel inicial com os indicadores e atalhos do dia a dia. (0) | — |
| | "Agenda" (`screen:schedule`) — Calendário de tarefas e visitas agendadas (sem esta tela o usuário não enxerga nem a própria agenda). (4) | "Sobrescrever Conflito de Agenda" (`fn:override_schedule_conflict`), "Ver Contas na Agenda" (`fn:view_financial_schedule`), "Ver Toda a Agenda" (`fn:view_all_schedule`), "Gerenciar Tarefas" (`fn:manage_tasks`) |
| **Serviços** | "Ordens de Serviço" (`screen:service_orders`) (6) | "Criar OS", "Editar OS", "Excluir OS", "Lançar Receita ao Finalizar OS" (`fn:os_finish_revenue`), "Resetar OS" (`fn:reopen_os`), "Editar OS em campo" (`fn:editar_os_campo`) |
| | "Serviços" (`screen:services`) (0) · "Checklists" (`screen:questionnaires`) (0) | — |
| | "Contratos" (`screen:contracts`) — Contratos recorrentes, PMOC e as visitas programadas de cada um. (1) | "Gerenciar Contratos" (`fn:manage_contracts`) |
| | "Equipamentos" (`screen:equipment`) (1) | "Gerenciar Equipamentos" (`fn:manage_equipment`) |
| **Comercial** | "Clientes e Fornecedores" (`screen:customers`) (4) | "Criar Cliente", "Editar Cliente", "Excluir Cliente", "Ver Financeiro do Cliente" |
| | "CRM/Kanban" (`screen:crm`) — Funis Kanban com leads, oportunidades e follow-ups (também exige o módulo contratado). (1) | "Gerenciar CRM" (`fn:manage_crm`) |
| | "Projetos" (`screen:projects`) (0) · "Orçamentos" (`screen:quotes`) (0) | — |
| **Operacional** | "Estoque" (`screen:inventory`) (1) | "Gerenciar Estoque" (`fn:manage_inventory`) |
| | "Área do Técnico™" (`screen:technician_tools`) (0) · "Mapa e Rastreamento" (`screen:tracking`) (0) | — |
| **PDV e Loja** | "Caixa e Venda (PDV)" (`screen:pdv`) (1) | "Editar Vendas do PDV" (`fn:edit_pdv_sales`) |
| | "Pedidos do Balcão (PDV)", "Expedição (PDV)", "Histórico de Caixa (PDV)", "Relatórios da Loja (PDV)", "Configurações do PDV" (0 cada) | — |
| **Financeiro** | "Financeiro" (`screen:finance`) (5) | "Gerenciar Financeiro", "Excluir Lançamento Financeiro" (`fn:delete_finance`), "Ver Totais Financeiros", "Usar Contas Bancárias", "Gerenciar Contas Bancárias" |
| | "Notas Fiscais" (`screen:fiscal_notes`) (0) | — |
| **Administração** | "Funcionários" (`screen:employees`) (2) | "Gerenciar Funcionários", "Gerenciar Ponto" |
| | "Usuários" (`screen:users`) (1) | "Gerenciar Usuários" (`fn:manage_users`) |
| | "Configurações" (`screen:settings`) (3) | "Gerenciar Configurações", "Gerenciar Chaves da API", "Exportar Dados da Empresa" (`fn:export_company_data`) |

Descrições completas de cada linha: `usePermissions.ts:56-91` (telas) e `:101-138` (ações). Total: 55 chaves.
"Acesso Total" grava `["*"]`.

### 2.4 Módulos 🔒 que mudam o que a pessoa vê (o editor mostra tudo, sem filtrar por módulo)

| Módulo (`company_modules`) | Nome na oferta (`components/ModuleGateModal.tsx:108-147`) | Telas afetadas |
|---|---|---|
| `crm` | "CRM/Kanban" | "CRM/Kanban" e "Projetos" (`useCompanyModules.ts:70-76`; menu `SidebarMenuContent.tsx:163-168`) |
| `contracts` | "Gestão de Contratos e PMOC" | "Contratos" (`useCompanyModules.ts:57-59`; menu `:116`) |
| `rh` | "Funcionários / RH" | "Funcionários" (`useCompanyModules.ts:67-68`; menu `:117`) |
| `nfe` | "Emissão de Notas Fiscais" | "Notas Fiscais" (menu `:186`) |
| `cobrancas` | "Cobranças online" | item "Cobranças" do Financeiro (menu `:180`) |
| `pdv` | "PDV e Loja" | as 6 telas PDV (`useCompanyModules.ts:77-89`) |
| Plano `excecao` | — | "Orçamentos" e "Financeiro" bloqueados (`subscriptionCatalog.ts:11-23`) |

- Marcar a tela no editor **não** libera um módulo que a empresa não tem: o item continua fora do menu. Abrir a rota
  de um módulo não contratado mostra a oferta do módulo (`App.tsx:499-519`).
- Empresa em teste (`subscription_status = 'testing'`) libera todos os módulos (`useCompanyModules.ts:203-222`).
- "Área do Técnico™" depende também do segmento da empresa ter ferramentas (refrigeração tem) (`SidebarMenuContent.tsx:107,318`).

### 2.5 O que cada perfil enxerga no menu (derivado de `SidebarMenuContent.tsx:95-186` e 2.2)

| Perfil | Menu lateral | Abre em |
|---|---|---|
| Administrador (papel `admin`) | Tudo o que o plano e os módulos liberam | Agenda (`App.tsx:288-299`) |
| Técnico **sem** permissões gravadas | Igual ao administrador (modo legado) | Agenda |
| Técnico com o cargo proposto "Técnico de Campo" (Agenda + Área do Técnico™ + "Editar OS em campo") | "Agenda" e "Área do Técnico™" | Agenda |
| Interno com o cargo proposto "Escritório" (seção 6 do plano) | Dashboard, Agenda, Operacional (Ordens de Serviço), Orçamentos, Gestão (Clientes e Fornecedores, Equipamentos), Financeiro | Agenda |
| Interno **sem** nenhuma permissão e sem papel | Nada; as rotas protegidas ficam no carregamento (seção 5, item 4) | `/perfil` (a confirmar) |

Os botões fixos do rodapé (Domiflix, suporte, conta, "Configurações", "Sair") aparecem para todos.

---

## 3. Por tela, janela e aba

### 3.1 Cabeçalho da aba (`pages/Users.tsx:530-568`)

- Título **"Usuários e Permissões"** com ícone de escudo; subtítulo **"{count}/{max} usuários • {active} ativos"**
  (`settings.ts:987-988`). `count` = usuários ativos da empresa (`useCompanyModules.ts:184-200`), `max` = usuários do
  plano + extras (`:236-243`), `active` = linhas da lista com `is_active` diferente de `false` (`Users.tsx:310`).
- Botões: **"Configurações"** (ícone de ajuste, abre "Configurações de Cargos") e **"Criar Usuário"** (só com
  `canManageRoles`, `Users.tsx:543-554`).
- Com o limite atingido (e permissão de gerenciar): faixa amarela **"Limite de usuários atingido ({count}/{max})"** /
  "Para cadastrar novos usuários, adicione usuários extras ao seu plano." com o botão **"Contratar mais usuários"**
  (`Users.tsx:557-566`; `settings.ts:1000-1002`).
- "Criar Usuário" com o limite atingido abre a janela de limite em vez do formulário (`Users.tsx:57-64`).

### 3.2 Lista com o painel do usuário (`components/users/UsersMasterDetail.tsx`)

Lista à esquerda (componente `ListDetailLayout`, mesmo do T3, seção 7.2), painel à direita.

- Título **"Usuários"**, legenda "{n} usuários cadastrados" ("1 usuário cadastrado"), busca **"Buscar por nome,
  e-mail, telefone ou perfil"**, ordem Nome A-Z/Z-A, 10 por página, vazio "Nenhum usuário encontrado"
  (`UsersMasterDetail.tsx:191-206`). A busca casa nome, cargo exibido, e-mail, telefone e o nome do papel (`:59`).
- Cada linha: foto ou iniciais, nome, embaixo o **nome do cargo**, ou "Acesso total", ou "{n} permissões"; à direita
  a etiqueta **"Ativo"** (verde) ou **"Inativo"** (cinza) (`:50-72`).
- Painel sem seleção: **"Selecione um usuário"** / "Escolha alguém na lista para consultar dados e permissões." com o
  botão **"Criar usuário"** (`:186-188`).
- Painel do usuário (`:101-184`):
  - Cabeçalho: foto (clicar amplia), nome, **"Você"** na própria linha, etiqueta Ativo/Inativo, e-mail (ou "E-mail não
    informado").
  - Ações (só com `canManageRoles`): **"Editar"**; **"Desativar"** (ativo e não é você); **"Reativar"** (inativo e não
    é você; desligado sem vaga livre); **"Excluir"** (não é você).
  - "Perfil de acesso": nome do cargo, ou "Acesso total", ou "Personalizado"; embaixo a descrição do cargo ou "{n}
    permissões configuradas.".
  - "Dados do usuário": "Administrador", "Técnico"... (`hooks/useUsers.ts:16-23`) ou **"Usuário interno"**; telefone ou
    "Telefone não informado".
  - **"Permissões concedidas"**: com acesso total, "Este usuário pode acessar todas as telas e ações disponíveis nos
    módulos contratados."; sem nada, "Nenhuma permissão foi concedida."; senão duas colunas **"Telas (n)"** e
    **"Ações (n)"** com ícone, rótulo e descrição.
- Carregando: esqueletos. Erro: "Não foi possível carregar os usuários" / "Verifique sua conexão e tente novamente."
  com "Tentar novamente" (`:81-90`).

### 3.3 Celular (abaixo de 1024 px) (`Users.tsx:387-525`)

Cabeçalho móvel com o mesmo título e subtítulo; abas **"Usuários"** e **"Cargos"**; botão flutuante **"Usuário"** ou
**"Cargo"**. Na aba Cargos: busca "Buscar cargos...", cartões com menu **"Editar"**, **"Duplicar"** e **"Excluir"**
(`PresetListMobile.tsx:56-78`); vazio "Nenhum cargo cadastrado" / "Toque em "Novo Cargo" para criar um perfil de
acesso". Excluir pede **"Excluir cargo?"** / "O cargo {name} será removido. Usuários que estavam vinculados a ele mantêm
as permissões individuais. Esta ação não pode ser desfeita." (`Users.tsx:490-508`). "Duplicar" cria "{nome} (cópia)" e
mostra "Cargo duplicado!" (`Users.tsx:340-351`).

### 3.4 Janela "Criar Usuário" / "Editar Usuário" (`components/users/UserFormDialog.tsx`)

Título "Criar Usuário" ou "Editar Usuário"; legenda "Preencha os dados do novo usuário" ou "Atualize os dados e
permissões do usuário" (`settings.ts:1046-1049`). Janela larga (até 1000 px) com duas colunas a partir de 1024 px:
dados à esquerda, **"Permissões"** à direita (`UserFormDialog.tsx:172-188`).

| Rótulo | Tipo | Obrigatório | Regras |
|---|---|---|---|
| **"Foto do Usuário"** | Círculo com câmera + botões **"Selecionar foto"** / **"Substituir"** e **"Remover"**; legenda "Foto opcional do usuário" | Não | HEIC vira JPEG e a imagem é reduzida (`utils/imageConvert.ts`, igual ao T3). Sobe só ao salvar (`Users.tsx:74-85`). |
| **"Nome Completo \*"** | Texto, placeholder "Nome do usuário" | Sim | Só exige não vazio (botão desligado) (`:181`). |
| **"Senha \*"** (só ao criar) | Senha com olho, placeholder "Crie uma senha segura" | Sim | Indicador "Senha fraca/média/boa/forte. Deve conter:" com 5 requisitos (8 caracteres, número, minúscula, maiúscula, especial) (`components/PasswordStrengthIndicator.tsx:15-29,61-73`). **Só informa**: o botão libera com qualquer senha. |
| **"Email \*"** (criar) / **"Email"** (editar) | E-mail, placeholder "email@exemplo.com" | Sim ao criar | Ao editar: "Alterar o email mudará o login de acesso do usuário" (`:248-252`). |
| **"Telefone"** | Texto, placeholder "(00) 00000-0000", máscara `phoneMask` | Não | — |
| **"Vincular a Funcionário"** | Lista: "Nenhum" + "Nome (Cargo)" de cada funcionário; placeholder "Nenhum funcionário vinculado"; legenda "Vincula este usuário a um funcionário cadastrado" | Não | Ao criar, se o e-mail do funcionário for diferente: quadro "Os emails são diferentes. Qual deve prevalecer?" com "Usuário:" e "Funcionário:" e "O email escolhido será aplicado em ambos os cadastros" (`:278-312`). |
| **"Tipo de Usuário"** | Interruptor entre **"Interno"** e **"Técnico"** | — | Técnico: "Aparece na listagem de técnicos da OS e pode ser adicionado a equipes". Interno: "Usuário interno do sistema, não aparece como técnico nas OS" (`:316-336`; `settings.ts:1074-1078`). Grava o papel `tecnico` ou nenhum. A lista de técnicos da OS e do contrato lê o papel `tecnico` (`hooks/useProfiles.ts:22-39`). |
| **"Permissões"** | "Escolha um perfil rápido ou ligue tela por tela. As ações de cada tela ficam dentro dela." + editor (3.5) | — | Começa sem nada marcado ao criar. |

- Rodapé: **"Cancelar"** e **"Criar Usuário"** (desligado sem nome, e-mail ou senha) ou **"Atualizar"**.
- Ao salvar, o cargo gravado é o **derivado** da seleção (chip aceso), não o último clicado (`:149-166`).

### 3.5 Editor de permissões (`components/users/PermissionsEditor.tsx`)

1. **"Perfis rápidos"** (só no formulário de usuário ou quando há cargos): chips **"Acesso Total"** (dica no passar do
   mouse: "Libera todas as telas e ações, inclusive as que forem criadas no futuro"), um chip por cargo (dica = descrição)
   e **"Personalizado"**. O chip aceso tem um ✓ (`:261-322`).
   - Clicar num cargo **substitui** a seleção (não soma) (`:131-132`).
   - "Personalizado" volta para a última seleção feita à mão (`:115-121,134`).
   - O chip aceso é calculado: bate exatamente com um cargo → chip do cargo; tudo marcado → "Acesso Total"; senão
     "Personalizado" (`:96-113`).
2. Busca **"Buscar tela ou ação..."** fixa no topo, com "Limpar busca"; casa rótulo ou descrição, sem acento e sem
   espaço ("ordemservico" acha "Ordem de Serviço"); as telas que sobram abrem sozinhas (`:137-146`). Sem resultado:
   `Nenhuma tela ou ação encontrada para "{query}".`
3. Lista por categoria (ícone + nome em maiúsculas): Geral, Serviços, Comercial, Operacional, PDV e Loja, Financeiro,
   Administração (`hooks/usePermissions.ts:36-49`).
4. Linha da tela: **interruptor** (liga a tela) + ícone + nome + descrição + contador **"n/m"** + seta. O interruptor
   **não** abre a linha e clicar na linha **não** liga a tela (`PermissionsEditor.tsx:39-40,177-243`). Tela sem ações não
   tem contador nem seta.
5. Linha aberta: **"Ações desta tela"** com um interruptor por ação (rótulo + descrição). Com a tela desligada aparece
   em itálico "A tela está desligada, mas estas ações continuam valendo por conta própria." (`:245-254`).
6. Não existe "marcar todos" (`:45`). A lista rola junto com a janela.

### 3.6 Cargos — janela "Configurações de Cargos" (`components/users/PermissionPresetDialog.tsx`)

- Título "Configurações de Cargos" / "Crie e edite perfis de acesso com permissões pré-definidas" (`settings.ts:1109-1110`).
- Lista: botão **"Novo Cargo"**; cada cargo com nome, descrição, etiqueta "{n} permissões" (conta telas + ações), lápis
  (editar) e **lixeira (exclui na hora, sem confirmação)** (`:93-118`). Vazio: "Nenhum cargo cadastrado".
- Formulário: **"← Voltar"**, **"Nome \*"** (placeholder "Ex: Técnico de Campo"), **"Descrição"** (placeholder
  "Descrição opcional"), o editor **sem** chips e sem "Acesso Total" (`:121-143`). Rodapé "Cancelar" e **"Criar Cargo"**
  (novo) ou **"Salvar"** (edição); desligado sem nome (`:74-82`).
- Avisos: "Cargo criado com sucesso!", "Cargo atualizado com sucesso!", "Cargo excluído com sucesso!"; erros "Erro ao
  criar cargo", "Erro ao atualizar cargo", "Erro ao excluir cargo" (`hooks/usePermissions.ts:223-262`).
- **Aplicar num usuário**: no formulário do usuário, chip com o nome do cargo. O usuário guarda **uma cópia** das
  permissões e o vínculo (`preset_id`). Desmarcar qualquer permissão apaga o chip; ao salvar o vínculo vira nulo e a lista
  passa a mostrar "{n} permissões" (`UserFormDialog.tsx:120-127,156-160`). Religar tudo igual reacende o chip.
- **Editar um cargo não atualiza os usuários que já o usam**: só a tabela de cargos muda (`usePermissions.ts:237-250`).
  A lista continua mostrando o nome do cargo para quem tem o vínculo, mesmo com permissões diferentes (`UsersMasterDetail.tsx:52,58`).
- Excluir cargo: os usuários ficam com as próprias permissões; o vínculo cai (`ON DELETE SET NULL`,
  `supabase/migrations/20260303155827_30007bb2-9fac-452d-b37c-857cac6cd260.sql:32`).

### 3.7 Desativar, reativar e excluir

| Ação | Confirmação | O que acontece | Avisos |
|---|---|---|---|
| **"Desativar"** | Nenhuma | `manage-user` marca `profiles.is_active = false` e apaga as sessões abertas (a pessoa cai na hora, `manage-user/index.ts:133-168`). Libera a vaga. | "Usuário desativado" / "O slot foi liberado. Você pode reativá-lo depois." (`settings.ts:1029-1030`). Erro: "Erro ao desativar". |
| **"Reativar"** | Nenhuma | Só com vaga livre: botão desligado sem vaga (`UsersMasterDetail.tsx:140`); o servidor confere de novo: "Limite de usuários atingido; faça upgrade ou desative outro." (`manage-user/index.ts:170-226`). | "Usuário reativado!" / "Erro ao reativar". |
| **"Excluir"** | **"Excluir usuário permanentemente?"** / "Esta ação é irreversível. O usuário {name} será removido permanentemente do sistema, incluindo login, permissões e vínculos." Botões "Cancelar" e **"Excluir Permanentemente"** ("Excluindo...") (`Users.tsx:587-600`) | Apaga permissões, papéis, perfil, sessões e o login; desfaz o vínculo com funcionário (`manage-user/index.ts:246-282`). Página recarrega. | "Usuário excluído permanentemente!" / "Erro ao excluir". |
| Último administrador ativo | — | Rebaixar, desativar ou excluir é bloqueado no navegador | "Ação bloqueada" / "A empresa precisa de pelo menos um administrador ativo." (`Users.tsx:312-324`) |
| Você mesmo | — | Desativar/Reativar/Excluir não aparecem (`UsersMasterDetail.tsx:136-144`); o servidor recusa: "Você não pode desativar a si mesmo." / "Você não pode excluir a si mesmo." | — |

Conta desativada tentando entrar: aviso "Conta desativada" / "Sua conta foi desativada. Fale com o administrador da
empresa." e volta ao login (`App.tsx:315-344`).

### 3.8 Limite de usuários (`components/UserLimitModal.tsx`)

- Vagas = usuários do plano + `extra_users` (no plano "personalizado", `companies.max_users`) (`useCompanyModules.ts:236-243`).
  Só usuários ativos ocupam vaga (`:184-200`).
- Planos atuais: 5, 10 e 15 usuários (`supabase/migrations/20261013120000_trial_7d_reprice_plans_and_base_features.sql:4,47-51`).
- Janela **"Limite de usuários atingido"**: "{count} / {max}" "usuários no seu plano", "Seu plano atual permite até {max}
  usuário(s). Para cadastrar mais, consulte as condições para adicionar usuários extras ao seu plano." Botões
  **"Voltar"** e **"Contratar mais usuários"** (vai para `/assinatura?addUsers=1`, tela do T0).

### 3.9 O que acontece ao salvar

**Criar** (`Users.tsx:87-144`): chama a função `create-user` com e-mail, senha, nome, telefone, permissões, cargo e
papel → se houver foto, sobe e grava no perfil → se houver funcionário, grava o vínculo (e a foto) → toast **"Usuário
criado com sucesso!"** → **recarrega a página**. E-mail repetido: "Erro ao criar usuário" / "Este e-mail já está
cadastrado no sistema.". O servidor cria o login já confirmado (sem e-mail de convite) e só grava `user_permissions` se
houver ao menos uma permissão marcada (`supabase/functions/create-user/index.ts:61-79,171-176`).

**Editar** (`Users.tsx:146-217`): grava nome/telefone/foto no perfil → troca o papel (Técnico liga, Interno remove; aviso
"Role atualizada com sucesso!") → grava as permissões (aviso "Permissões atualizadas!") → refaz o vínculo com funcionário
→ troca o e-mail se mudou → **"Usuário atualizado!"** → **recarrega a página**. Erro: toast "Erro" com o motivo.

---

## 4. Backend por tela (o que o backend falso precisa responder)

Regras gerais do supabase-js, das releituras e do formato de erro: inventário do T3, seção 12.0.

### 4.1 Ao abrir `/configuracoes?tab=usuarios`

| Chamada | Detalhe | Fonte |
|---|---|---|
| Página Configurações | `GET company_settings` (`company_id=eq.`, `.maybeSingle()`), `GET user_preferences` (próprio usuário), `GET customer_origins` | `Settings.tsx:118-155`; `hooks/useUserPreferences.ts:46` |
| `GET profiles?select=company_id&user_id=eq.<eu>` | `.single()` | `hooks/useUsers.ts:45-49` |
| `GET profiles?select=*&company_id=eq.<empresa>&order=full_name.asc` | A lista | `useUsers.ts:52-57` |
| `GET user_roles?select=*` | Todos os papéis visíveis (o app junta pelo `user_id`) | `useUsers.ts:60-62` |
| `GET user_roles?select=role&user_id=eq.<eu>` | `.maybeSingle()` — **mais de uma linha dá erro** | `useUsers.ts:83-88` |
| `GET user_roles?select=id&role=eq.admin&limit=1` | "Existe admin?" | `useUsers.ts:97-101` |
| `GET user_permissions?select=permissions&user_id=eq.<eu>` | `.maybeSingle()` | `useUsers.ts:113-118` |
| `GET user_permissions?select=*` | Permissões de todos | `hooks/usePermissions.ts:274-276` |
| `GET permission_presets?select=*&order=name.asc` | Cargos | `usePermissions.ts:209-212` |
| `GET company_modules`, `GET companies`, `GET subscription_plans`, `HEAD profiles` com `count=exact` e `is_active=eq.true` | Módulos, plano e vagas | `useCompanyModules.ts:117-200` |
| `GET employees?select=*&order=name.asc` | Lista "Vincular a Funcionário" | `hooks/useEmployees.ts:64-66` |

### 4.2 Ações

| Ação | Chamadas, na ordem |
|---|---|
| "Criar Usuário" | `POST /functions/v1/create-user` `{ email, password, full_name, phone, permissions, preset_id, role }` (`role` = `"tecnico"` ou `null`; `permissions` = lista ou `["*"]`). **Resposta esperada `{ "user": { "id", "email" } }`**; erro `{ "error": "..." }` com 400/403/500 (`create-user/index.ts:144-299`). Foto: `POST /storage/v1/object/customer-photos/user-<id>-<Date.now()>.<ext>` (upsert) + `PATCH profiles?user_id=eq.<id>` `{ avatar_url }`. Funcionário: `GET profiles?select=avatar_url` + `PATCH employees?id=eq.<id>` `{ user_id, email?, photo_url? }`. Depois `location.reload()`. |
| Abrir "Editar" | `POST /functions/v1/manage-user` `{ action: "get_email", user_id }` → `{ "email": "..." }` (falha vira o e-mail do funcionário) (`Users.tsx:282-307`). |
| "Atualizar" | Foto (como acima) → `PATCH profiles?user_id=eq.<id>` `{ full_name, phone, avatar_url? }` → Técnico: `GET user_roles?select=id&user_id=eq.<id>` (`.maybeSingle()`) + `PATCH user_roles?user_id=eq.<id>` `{ role }` ou `POST user_roles`; Técnico→Interno: `DELETE user_roles?user_id=eq.<id>&role=eq.tecnico` → `POST user_permissions?on_conflict=user_id` (upsert, `Prefer: resolution=merge-duplicates`) `{ user_id, permissions, preset_id, is_active: true }` → `PATCH employees?user_id=eq.<id>` `{ user_id: null }` (+ `PATCH employees?id=eq.<novo>`) → se o e-mail mudou, `manage-user` `{ action: "update_email", user_id, email }` → reload. |
| "Desativar" / "Reativar" | `manage-user` `{ action: "deactivate_user" \| "reactivate_user", user_id }` → `{ "success": true }`; o app relê `users` e a contagem. |
| "Excluir Permanentemente" | `manage-user` `{ action: "delete_user", user_id }` → `{ "success": true }` → reload. |
| Cargos | Criar `POST permission_presets` `{ name, description, permissions }` (sem `company_id`, sem pedir retorno); editar `PATCH permission_presets?id=eq.<id>`; excluir `DELETE permission_presets?id=eq.<id>`; duplicar (celular) = criar `"<nome> (cópia)"`. |

### 4.3 Tabelas e colunas (`integrations/supabase/types.ts`, via `rec/fakebase/schema.json`)

| Tabela | Colunas usadas |
|---|---|
| `profiles` | `user_id`, `company_id`, `full_name`, `email`, `phone`, `avatar_url`, `is_active` |
| `user_roles` | `user_id`, `role` (`admin`, `gestor`, `tecnico`, `comercial`, `financeiro`, `super_admin`) |
| `user_permissions` | `user_id` (único), `permissions` (lista de chaves ou `["*"]`), `preset_id`, `is_active` |
| `permission_presets` | `id`, `name`, `description`, `permissions` — **sem `company_id`** |
| `employees` | `id`, `name`, `position`, `email`, `user_id`, `photo_url` |
| `active_sessions` | apagada ao desativar/excluir |

### 4.4 Comparação com o backend falso (`/home/claude/domiflix/rec/fakebase`)

| Item | Situação hoje | Falta |
|---|---|---|
| Login por e-mail de qualquer perfil (qualquer senha) | **Coberto** (`http/auth.mjs:9-23`); o roteiro do robô aceita `"user": "<e-mail>"` (`rec/recorder/runner.mjs:683`) | — |
| `profiles` (7: Camila admin + 6 técnicos), `user_roles`, `companies`, `company_modules` (13), `subscription_plans` | **Coberto** (`seeds/gen-01-tenant.json`) | Planos do seed (start 3, avancado 8, master 20 usuários) não batem com os de hoje (5/10/15): o contador mostra "7/20". |
| `user_permissions` | Está em `_vazias` (`seeds/00-vazias.json`): ninguém tem registro → todos em modo legado | Seeds de permissões do estado final do T2 (seção 6 do plano). |
| `permission_presets` | Sem seed (cai em `TABELA_SEM_SEED`) | Seed vazio no início; linhas criadas no vídeo. |
| `employees` | Sem seed | Só se o vídeo mostrar "Vincular a Funcionário" com opções. |
| Função `create-user` | **Sem handler**: devolve `200 {}` (`http/functions.mjs:31-35`) → o app mostra "Usuário criado com sucesso!", recarrega e **ninguém aparece** | Handler que insere `profiles` (com `company_id`, `email`, `is_active: true`), `user_roles` (se `role`), `user_permissions` (se houver permissões) e devolve `{ user: { id, email } }`; e-mail repetido → 400 `{ error: "Este e-mail já está cadastrado no sistema." }`. |
| Função `manage-user` | **Sem handler** (`200 {}`): editar abre sem e-mail; desativar/reativar/excluir "funcionam" sem mudar nada | Handler com `get_email`, `update_email`, `deactivate_user`, `reactivate_user` (conferindo vagas), `delete_user`, recusando o próprio usuário. |
| Upsert `user_permissions?on_conflict=user_id` | **Coberto** (`core/mutate.mjs:44-58`) | — |
| Storage `customer-photos` | **Coberto** (bucket conhecido, `http/storage.mjs:15-18`) | — |
| `location.reload()` no meio da gravação | Os dados ficam (a memória do fakebase não zera) | O robô precisa esperar a página voltar (`waitFor idle`); a tela de carregamento aparece ~1-3 s (cortar na edição). |

---

## 5. Pegadinhas para roteiro e gravação

Marcadas **[handoff]** as que valem pedido de correção ao time do app.

1. **[handoff]** A administradora aparece com "0 permissões" na lista, "Personalizado", "0 permissões configuradas." e
   "Nenhuma permissão foi concedida." no painel, porque o dono da empresa não tem linha em `user_permissions`
   (`UsersMasterDetail.tsx:53-58,92-99,154-169`; o cadastro da empresa só grava o papel `admin`,
   `supabase/functions/self-register/index.ts:910-911`). No vídeo: semear `user_permissions` da Camila com `["*"]`
   (vira "Acesso total") ou não mostrar o painel dela.
2. **[handoff, segurança]** Usuário com papel e **sem** registro de permissões vê tudo (modo legado,
   `AuthContext.tsx:386-394`). Criar um **Técnico sem marcar nenhuma permissão** cai nesse caso, porque o servidor só grava
   permissões quando a lista não está vazia (`create-user/index.ts:61-62`). Os 6 técnicos do seed estão assim e aparecem com
   "0 permissões".
3. **[handoff]** Criar um **Interno sem permissões** deixa a pessoa sem papel e sem permissões: as rotas protegidas
   ficam no carregamento infinito (`App.tsx:378`) (deduzido do código; a confirmar rodando).
4. Criar, editar e excluir **recarregam a página inteira** (`Users.tsx:132,212,274`). Na gravação aparece a tela de
   carregamento e a lista volta sem o usuário selecionado.
5. **[handoff]** Salvar uma edição solta até três avisos: "Role atualizada com sucesso!" (`useUsers.ts:157`), "Permissões
   atualizadas!" (`usePermissions.ts:307`) e "Usuário atualizado!" (`Users.tsx:211`). "Role" está em inglês.
6. **[handoff]** O botão dos cargos tem o rótulo genérico **"Configurações"** (`settings.ts:998`), dentro de uma página
   que também se chama Configurações.
7. **[handoff]** A lixeira de cargo no computador exclui **sem confirmação** (`PermissionPresetDialog.tsx:112`); no
   celular há confirmação.
8. "Duplicar" cargo só existe no celular (`PresetListMobile.tsx:67-69`). No celular, "Editar" um cargo abre a lista da
   janela, não o cargo escolhido (`Users.tsx:334-338`).
9. **[handoff]** Editar um cargo não muda as permissões de quem já o usa, e a lista continua mostrando o nome do cargo
   (seção 3.6). Para o roteiro: falar em "aplicar o cargo" e, se mudar o cargo, "aplicar de novo em cada pessoa".
10. **[handoff]** A permissão de tela **"Checklists"** (`screen:questionnaires`) não é usada em lugar nenhum do app (só
    no catálogo, `usePermissions.ts:60`): os checklists ficam em Serviços (`screen:services`).
11. "Pedidos do Balcão (PDV)" e "Expedição (PDV)" estão no editor, mas a tela ainda não existe (`usePermissions.ts:78-83`).
    As telas PDV aparecem no editor mesmo sem o add-on.
12. O indicador de força da senha **não impede** senha fraca (`UserFormDialog.tsx:181`). O login real pode recusar senha
    curta (regra do Supabase Auth; a confirmar). No vídeo, usar uma senha "forte" (todos os itens verdes).
13. **[handoff]** Subtítulo "{count}/{max} usuários • {active} ativos": os dois números contam só ativos, então ficam
    sempre iguais (`useCompanyModules.ts:184-200`, `Users.tsx:310`).
14. "Reativar" fica desligado sem explicação no computador (o texto "Sem slot livre — faça upgrade ou desative outro" de
    `settings.ts` não é usado ali, `UsersMasterDetail.tsx:140`). "Desativar" não pede confirmação.
15. Texto do "Técnico" diz "pode ser adicionado a equipes", mas desde a 1.37.55 qualquer colaborador ativo entra em
    equipe (`Changelog.tsx:167`). Copy desatualizada **[handoff]**.
16. **[handoff, segurança]** `permission_presets` **não tem `company_id`** e as políticas liberam leitura para qualquer
    usuário autenticado e escrita para quem gerencia usuários em qualquer empresa (`types.ts` via `schema.json`;
    migrações `20260308205452_...sql:71-81` e `20260418163700_...sql:98-99`). Pelo código, cargos de uma empresa
    apareceriam (e poderiam ser apagados) em outra (a confirmar no banco real).
17. **[handoff, segurança/receita]** `create-user` não confere o limite de usuários; só o navegador bloqueia
    (`Users.tsx:57-64`). `reactivate_user` confere.
18. `canManageRoles` libera quem tem **27 ou mais** permissões marcadas (`useUsers.ts:124`), regra que ninguém vê na
    tela **[handoff]**.
19. O selo "Salvo" das Configurações continua no canto durante a aba de usuários (`Settings.tsx:1932-1937`); não tem
    relação com usuários.
20. Para quem não tem `screen:settings`, o botão "Configurações" do menu existe mas não leva à tela (seção 1) (a confirmar).

---

## 6. 🚫 Não prometer / telas mortas

- 🚫 Escolher papel "Administrador" ou "Gestor" na tela: só existe "Interno" ou "Técnico" (`UserFormDialog.tsx:316-336`;
  nenhum outro uso de `updateUserRole`, `Users.tsx:172`).
- 🚫 Cargo que atualiza sozinho as pessoas que o usam (seção 3.6).
- 🚫 "Duplicar cargo" no computador; 🚫 aba "Cargos" no computador.
- 🚫 Administrador redefinir a senha de outro usuário: a janela de edição não tem senha. Caminho positivo: a própria
  pessoa troca em "Meu Perfil" → "Alterar Senha" (`settings.ts`, bloco `profile`) ou pelo "esqueci a senha" do login.
- 🚫 Convite por e-mail: o login nasce confirmado com a senha definida pelo admin (`create-user/index.ts:171-176`).
- 🚫 Importar usuários em massa; 🚫 login social (trilha, "Coisas que parecem existir").
- 🚫 Permissão por depósito nesta tela: o acesso a estoque por local vive no Estoque (T8).
- Tela morta: `/usuarios` (redireciona, `App.tsx:865`). `components/users/UserListMobile.tsx` não é usado por nenhuma tela.

---

## 7. Dúvidas em aberto (só rodando o app)

1. Interno sem permissões: carregamento infinito ou cai em `/perfil`? (seção 5, item 3).
2. Botão "Configurações" do menu para quem não tem `screen:settings`: some, redireciona ou pisca a tela?
3. Senha fraca aceita pelo Auth real? Mínimo de caracteres do projeto Supabase.
4. Desativar derruba a sessão do outro usuário em tempo real (`useForcedLogout` + realtime de `active_sessions`)? No
   fakebase há realtime (`rec/fakebase/http/realtime.mjs`), mas não foi verificado para essa tabela.
5. `permission_presets` realmente global no banco de produção (item 16)? Afeta o que o cliente vê na lista de cargos.
6. Ordem dos três avisos ao editar e qual fica visível antes do reload.
7. O e-mail do perfil (`profiles.email`) é preenchido para usuários criados pela tela? (o painel mostra "E-mail não
   informado" se vier vazio; o `create-user` não envia `email` ao perfil, `create-user/index.ts:31-37`).
