# T4 · Serviços, tarefas e checklists · inventário do app 1.38.6

Levantamento feito em 30/10/2026 sobre `/home/claude/domiflix/src-1.38.6` (somente leitura; só análise estática, o app e o
backend falso não foram executados). Convenções:

- Caminhos `arquivo:linha` são relativos a `src/` da 1.38.6 (ex.: `pages/Services.tsx:52`). `rec/...` = `/home/claude/domiflix/rec/`.
- `os.ts` = `lib/i18n/messages/app/os.ts` (textos pt-br; o bloco pt-br vai até a linha ~1700, as outras línguas vêm depois).
- Rótulos entre aspas estão EXATOS como aparecem na tela. Onde o texto é fixo no componente (fora do i18n), a linha do componente
  é a fonte.
- Os arquivos de T4 do `app/` que o robô usa (1.38.5) são byte a byte iguais aos da 1.38.6 (`cmp` em `Services.tsx`, os 3
  painéis, `ChecklistDetail.tsx`, `ChecklistCatalogModal.tsx`, `useFormTemplates.ts`, `TaxCodeCombobox.tsx`). Nada deste
  inventário muda entre 1.38.5 e 1.38.6.
- Fonte secundária conferida e marcada: `docs/guia-tecnico/secoes/T4.html` (manual do app). Está desatualizado em pontos
  importantes (tabela com colunas, vídeo só com módulo, limite de vídeo); o código manda. Divergências na seção 5.

---

## 0. Resumo para o roteiro

### 0.1 Capítulos da trilha (1.22.5) × código de hoje

| # | Capítulo da trilha 1.22.5 | Situação na 1.38.6 | Evidência |
|---|---|---|---|
| 1 | Onde fica: menu Serviços (`/servicos`) e as 3 abas | Bate, mas o menu é **Gestão › Serviços** e as abas se chamam "Tipos de Serviços", "Tipos de Tarefas", "Checklists" (plural em "Serviços"). Título "Serviços", subtítulo "Configure os tipos de serviços, tarefas e checklists". | `components/layout/SidebarMenuContent.tsx:110-113`; `os.ts:1600-1606`; `pages/Services.tsx:18-22` |
| 2 | Tipos de Serviço: nome, cor, categoria, prefixo | **Layout mudou**: não é mais tabela. No computador (≥ 1024 px) é lista à esquerda + "Ficha do tipo de serviço" à direita (mestre-detalhe) com o formulário já aberto; "Novo Tipo" abre modal. Categorias têm botão e janela próprios. | `ServiceTypesPanel.tsx:581-624, 393-423, 428-438`; `ui/ListDetailLayout.tsx:313-316` |
| 3 | Switch "exige equipamento" | **Renomeado**: o rótulo é "Vinculado a equipamento" (vem ligado). O efeito é o mesmo: some o bloco de equipamentos na criação da OS. | `os.ts:573`; `ServiceTypesPanel.tsx:775-783`; `ServiceOrderFormDialog.tsx:289-292` |
| 4 | Campos fiscais | Bate. Aba "Fiscal" **só aparece com o módulo `nfe`** (Glacial tem). Busca de cTribNac/NBS chama a edge `nfse-tax-codes`. cTribMun só aceita 3 dígitos. | `ServiceTypesPanel.tsx:113-114, 801-896`; `fiscal/TaxCodeCombobox.tsx:74-90` |
| 5 | Preço padrão e orçamento | Bate: "Preço padrão (opcional)" na aba Dados; o orçamento usa como sugestão **só quando não há custo calculado**. | `ServiceTypesPanel.tsx:762-772`; `quotes/QuoteFormDialog.tsx:679-696` |
| 6 | Tipos de Tarefa | Bate. Também mestre-detalhe. Os tipos alimentam o "Nova Tarefa" da Agenda (só os ativos). | `TaskTypesPanel.tsx:279-290`; `schedule/TaskFormDialog.tsx:295-300` |
| 7 | Checklists: do zero × catálogo | Bate. Hoje: lista + prévia ("Prévia na ordem de serviço") com botões "Ver", "Adicionar pergunta", "Editar checklist"; "Catálogo de Checklists" e "Novo checklist" sobem para a linha das abas. | `ChecklistsPanel.tsx:252-285, 389-403`; `ChecklistOsPreview.tsx:96-125` |
| 8 | Editor: sim/não, conformidade, texto, número, **medição PMOC**, seleção, foto, assinatura | **Não bate**: o editor oferece 8 tipos: "Verdadeiro/Falso" (não é mais "Sim/Não"), "Conformidade", "Texto", "Número", "Foto", "Vídeo", "Seleção", "Assinatura". **"Medição PMOC" não é escolhível**; só chega via Catálogo PMOC/contrato. | `hooks/useFormTemplates.ts:36-45` |
| 9 | Combinar tipos + exigir câmera | Bate: marcar 2+ tipos abre "Modo de resposta múltipla" (Exclusivo/Cumulativo); "Exigir foto da câmera" e "Permitir múltiplas fotos" aparecem com o tipo Foto. | `pages/ChecklistDetail.tsx:872-1022` |
| 10 | 🔒 Pergunta de vídeo (módulo, com limite) | **Não bate**: o tipo "Vídeo" aparece para todos, sem trava de módulo e **sem limite aplicado/mostrado** (as frases de limite existem no `os.ts` mas nenhum componente as usa). Há o switch "Exigir gravação na hora". | `useFormTemplates.ts:42`; `os.ts:515-516` (sem uso); `ChecklistDetail.tsx:1011-1022` |
| 11 | Vincular a tipos de serviço e desativar | Bate: "Serviços habilitados" (vazio = todos) e "Desativar checklist?" (nunca apaga). Cadastro de serviço: "Excluir" **apaga de verdade**, "Ativo" desligado é o caminho seguro. | `ChecklistDetail.tsx:566-574, 1046-1075`; `useFormTemplates.ts:126-143`; `useServiceTypes.ts:167-182` |

### 0.2 O que o roteiro precisa saber antes de escrever
1. **Dá para falar de lista + ficha, não de tabela.** Nenhuma coluna ("Cor, Nome, Prefixo OS, Equipamento, Status, Valor") aparece
   mais; as strings continuam no `os.ts:546-557` mas nenhum painel as usa (grep em `ServiceTypesPanel.tsx`/`TaskTypesPanel.tsx`).
2. **"Novo Tipo" com um tipo já selecionado, no computador, provavelmente reabre a ficha do tipo selecionado** em vez de um
   formulário limpo (pegadinha P1, **handoff recomendado**). Só o PRIMEIRO tipo de serviço nasce limpo; na gravação isto limita o
   que dá para criar ao vivo (ver `plano.md`).
3. **Os textos do modal "Nova Pergunta" são fixos no componente** e diferem do `os.ts` ("Orientação para o técnico (opcional)",
   não "Descrição interna (opcional)"). Usar a seção 3.8.
4. **Catálogo de Checklists é local** (`data/checklistCatalog.ts`): 4 modelos de refrigeração (Instalação de Split 13 perguntas,
   Higienização de Split 11, Manutenção Preventiva de Split 13, Carga de Gás 13) para empresas com segmento `refrigeracao`
   (a Glacial tem). Não depende de backend. A parte "Catálogo PMOC" depende da tabela `pmoc_activity_catalog` (vazia no
   backend falso).
5. **Glacial Cold Brasil tem os módulos `nfe`, `contracts` e `video_questions`** (`rec/fakebase/seeds/gen-01-tenant.json`,
   `company_modules`), então na gravação aparecem: aba "Fiscal", o campo "Frequência" em cada pergunta e o badge de frequência
   nas linhas. Isso precisa de decisão de roteiro (falar ou ignorar).

### 0.3 Pode surpreender (positivo e negativo)
- A lista lembra a última busca/ordenação por tela (sessionStorage `service-types-list`, `service-task-types-list`,
  `service-checklists-list-detail`); em gravação com navegador limpo não há resíduo. (`ui/ListDetailLayout.tsx:136-160`)
- Criar um checklist abre direto o editor ("Voltar à prévia" no canto) e criar pelo catálogo também. (`ChecklistsPanel.tsx:156-170`)
- O modal de pergunta tem **prévia ao vivo** "Prévia na OS" ("Atualiza enquanto você configura"). (`ChecklistDetail.tsx:50-176`)
- "Ver" abre a prévia COMPLETA com o mesmo componente que o técnico usa e permite responder sem salvar. (`ChecklistPreviewDialog.tsx`)

---

## 1. Rotas e navegação

| Item | Valor | Evidência |
|---|---|---|
| Menu (barra lateral) | Gestão › **Serviços** (ícone chave inglesa) | `layout/SidebarMenuContent.tsx:110-113`; também `layout/TopNavbar.tsx:103` e `layout/MoreMenuDrawer.tsx:99` |
| URL | `/servicos` (outros idiomas: `/services`, `/servicios`) | `App.tsx:791`; `lib/i18n/appRouteSlugs.ts:50,128` |
| Aba na URL | `?tab=types` (padrão) · `?tab=task-types` · `?tab=checklists`; `?tab=questionnaires` vira `checklists`; valor desconhecido volta a `types` | `pages/Services.tsx:25-30, 42-50` |
| Detalhe de checklist (tela própria) | `/checklists/:id` (mesma tela do editor, sem prévia) — usado fora do painel (link antigo, retorno) | `App.tsx:793`; `appRouteSlugs.ts:129`; `ChecklistDetail.tsx:245-248` (`leaveEditor` volta a `/servicos?tab=checklists`) |
| Redirects antigos | `/checklists` → `/servicos` (aba padrão, **não** `?tab=checklists`); `/questionarios` → `/checklists`; `/questionarios/:id` → `/checklists/:id` | `App.tsx:792, 795-796, 974-977` |
| Mesma lista em outra porta | Configurações fiscais › Serviços reaproveita o mesmo painel já na aba Fiscal (`<ServiceTypesPanel embedded defaultFormTab="fiscal" />`); criação rápida de tipo dentro de OS/orçamento usa `QuickServiceTypeDialog` | `fiscal/ServicosSection.tsx:26`; `pages/FiscalSettings.tsx:605`; `service-orders/QuickServiceTypeDialog.tsx` |
| Cabeçalho da página | `PageHeader` "Serviços" + subtítulo; abas sublinhadas (ícones Settings/CheckSquare/FileText); no computador as ações do painel ativo sobem para a MESMA linha das abas (`ScreenActionsSlot`) | `Services.tsx:54-71`; `ui/ScreenActions.tsx:16-36` |
| Corte computador/celular | `useIsMobile` = largura < **1024 px** (não 768) | `hooks/use-mobile.tsx:3-4` |

Componentes principais: `pages/Services.tsx` → `ServiceTypesPanel.tsx` (920 linhas) · `TaskTypesPanel.tsx` (327) · `ChecklistsPanel.tsx`
(525) → `ChecklistDetail.tsx` (1129, embutido ou rota) · `ChecklistCatalogModal.tsx` (759) · `ChecklistOsPreview.tsx` ·
`ChecklistPreviewDialog.tsx` · `ServiceTypeCategoriesDialog.tsx` · `ServicesMultiSelect.tsx`.

---

## 2. Permissões e módulos

| Chave / módulo | Rótulo | Efeito em T4 | Evidência |
|---|---|---|---|
| `screen:services` | **Serviços** — "Catálogo de serviços prestados e seus valores." | Guarda `/servicos` **e** `/checklists/:id`. Módulo base (`basic`): todos os planos. | `hooks/usePermissions.ts:59`; `App.tsx:791,793`; `hooks/useCompanyModules.ts:52` |
| `screen:questionnaires` | **Checklists** — "Modelos de checklist usados dentro das ordens de serviço." | **Sem efeito**: existe no editor de permissões, mas nenhuma rota ou tela a consulta (grep no `src/` só acha a declaração). Quem tem `screen:services` vê a aba Checklists. | `usePermissions.ts:60` (P6) |
| `fn:*` para tipos/checklists | — | Não há função específica de gerenciar tipos de serviço/checklists: quem entra na tela edita tudo. | grep em `usePermissions.ts` |
| Módulo `nfe` | Nota Fiscal | Sem ele, o formulário do tipo de serviço só tem "Dados" (as pílulas "Dados/Fiscal" somem). | `ServiceTypesPanel.tsx:113-114, 149, 276-282, 667-683` |
| Módulo `contracts` | Contratos e PMOC (pago) | Com ele aparece "Frequência" na pergunta e o badge de frequência em cada linha ("Toda visita", Mensal...). | `ChecklistDetail.tsx:213-215, 734-740, 1025-1037` |
| Módulo `video_questions` | Perguntas em Vídeo (add-on, R$ 50) | **Não gateia nada na 1.38.6**: nenhum componente consulta. Limite por plano (`subscription_plans.max_video_questions`: start 0, avancado 1, master 3) só existe no catálogo/banco. | `hooks/useCompanyModules.ts:23`; `supabase/migrations/20260715120000_video_question_type_and_module.sql:68-81`; grep sem uso em `src/` |
| Segmento da empresa | `company_settings.segment` | `refrigeracao` libera os 4 modelos curados + o "Catálogo PMOC" no catálogo; outros segmentos veem só "Visita Técnica". | `data/checklistCatalog.ts:157-171`; `ChecklistCatalogModal.tsx:136-144` |
| Papel | `admin` (Camila) | Tudo liberado. Técnicos (`tecnico`) não precisam desta tela. | `rec/fakebase/seeds/gen-01-tenant.json` (`user_roles`) |

Na Glacial (plano `master`, `company_modules` com 13 módulos): `basic, rh, crm, contracts, nfe, pricing_advanced, customer_portal,
white_label, video_questions, whatsapp, cobrancas, finance_advanced, pdv` — todos os gates de T4 ficam abertos.

---

## 3. Por tela / janela / aba

### 3.1 Página "Serviços" (`pages/Services.tsx`)
- Título "Serviços"; subtítulo "Configure os tipos de serviços, tarefas e checklists" (`os.ts:1601-1602`).
- Abas (sublinhadas): "Tipos de Serviços" (`types`), "Tipos de Tarefas" (`task-types`), "Checklists" (`checklists`) (`os.ts:1603-1605`).
  A aba escolhida vai para a URL com `replace` (não empilha histórico) (`Services.tsx:31-38`).
- No celular as abas viram pílulas rolantes e não há `ScreenActionsSlot` (`Services.tsx:70`); o botão de criar vira FAB.

### 3.2 Aba "Tipos de Serviços" — `ServiceTypesPanel.tsx`
**Barra de ações (computador)**, na linha das abas, à direita (`:428-438`): botão contorno **"Categorias"** (ícone etiquetas) e botão
primário **"Novo Tipo"** (ícone +). No celular: FAB "Tipo" (`os.ts:563`; `ServiceTypesPanel.tsx:628-635`) e barra de busca + filtro.

**Estado vazio** (`:505-511`): ícone chave inglesa, "Nenhum tipo de serviço", "Cadastre seus tipos de serviço para organizar as OS"
(celular: "Toque em Novo Tipo para cadastrar") (`os.ts:543-545`).

**Lista (esquerda, `ListDetailLayout`, `:581-624`)**
- Título "Tipos de Serviço"; descrição "N tipo cadastrado" / "N tipos cadastrados" (`:584-585`); botão "Recolher lista"/"Expandir lista"
  (`common.ts:82-84`); busca "Buscar por nome ou descrição..." (`os.ts:559`) — o termo também casa com nome da categoria e prefixo
  (`:232-246`); ordenar "Ordenar" → "Nome (A-Z)" (padrão) / "Nome (Z-A)" (`common.ts:89-91`); paginação 25/página (`ListDetailLayout.tsx:118`).
- Linha: quadradinho colorido com ícone de chave inglesa; título = nome; subtítulo = "Categoria • Prefixo" ou, sem eles, a descrição;
  selo "Inativo" quando desligado (`:232-246`).
- Botão **"Filtros"** só aparece se existir ao menos uma categoria (`:586-612`): popover com grupo "Categoria", "Todas as categorias" (vazio),
  "Sem categoria" (só se houver tipo sem categoria) e "Limpar filtros" (`:220-229`; `os.ts:615-618`).
- **Seleção automática**: no computador o primeiro item da lista é selecionado sozinho (`:248-253`); o clique em outro item chama
  `handleEdit` (`:617-621`).

**Ficha à direita (`:393-423` + editor inline `:266-391`)**: sobretítulo "Ficha do tipo de serviço", nome grande, botão **"Excluir"**
(contorno vermelho); formulário inline (abas "Dados"/"Fiscal" se `nfe`) e rodapé com **"Salvar"** (desabilitado sem nome ou com cTribMun
inválido). Salvar atualiza o tipo (`:183-207`; toast "Tipo de serviço atualizado!").

**Modal "Novo Tipo de Serviço"** (`:642-897`; largura `sm:max-w-[860px]`; sempre este título, o `modalTitleEdit` não é usado)
- Abas (pílulas sublinhadas, só com `nfe`): **"Dados"** e **"Fiscal"** (`os.ts:578-579`).
- Aba Dados, na ordem da tela (`:684-792`):
  1. **"Nome *"** — placeholder "Ex: Manutenção Preventiva". Obrigatório (botão "Criar" desabilitado sem nome).
  2. **"Cor"** — `<input type="color">` nativo + campo de texto com o hex (padrão `#22c55e`, `:70`). Os dois estão ligados ao mesmo estado.
  3. **"Categoria"** — select; opções "Sem categoria" + categorias cadastradas (`:713-737`).
  4. **"Descrição"** — placeholder "Descrição do tipo de serviço".
  5. **"Prefixo de Numeração OS"** — placeholder "Ex: MP, MC, INS"; embaixo, prévia fixa `→ MP-2026-0001` (usa "OS" sem prefixo) (`:751-760`).
  6. **"Preço padrão (opcional)"** — `type=number` (`step 0.01`, `min 0`), placeholder "Ex: 350,00"; ajuda "Valor sugerido ao adicionar este serviço
     em um orçamento. Pode ser editado pelo vendedor." (`:762-772`). Vazio vira `null` (`:199`).
  7. Switch **"Vinculado a equipamento"** (padrão LIGADO, `:73`) e switch **"Ativo"** (padrão LIGADO) (`:775-791`).
- Aba **Fiscal** (`:801-896`, só `nfe`): bloco "Fiscal (NFS-e)" + "Classificação tributária usada ao emitir nota fiscal de serviço. Todos os
  campos são opcionais." Campos:
  - "Código de serviço (cTribNac)" — combobox "Selecione o código..." → popover com busca "Buscar por código ou descrição..."; lista "07.10.02"
    (máscara de 6 dígitos) + descrição + "(item LC116)"; escolher preenche o campo "Item da LC 116" (`TaxCodeCombobox.tsx:225-343`; `ServiceTypesPanel.tsx:812-827`).
    Ajuda: "Código nacional do serviço. O item da LC 116 é preenchido automaticamente."
  - "Código de tributação municipal (cTribMun)" — placeholder "Ex.: 001"; só dígitos, máx. 3; ajuda "Complemento de 3 dígitos definido pela prefeitura, que se junta
    ao código nacional (ex.: 14.01.01 + 001). Sem ele a prefeitura pode recusar a nota."; erro vermelho "O código de tributação municipal deve ter 3 dígitos."
    (`:835-856`; também repetido no rodapé se o usuário está na aba Dados, `:654-656`).
  - "Item da LC 116" — placeholder "14.01" (texto livre).
  - "Código NBS" — mesmo combobox, busca no servidor só com ≥ 2 caracteres ("Digite ao menos 2 caracteres pra buscar."); ajuda "Nomenclatura Brasileira de Serviços...".
  - "Alíquota de ISS (%)" — placeholder "5".
- Rodapé: **"Cancelar"** e **"Criar"** (`:651-663`). Ao criar, o modal fecha (`:204-206`) e aparece o toast "Tipo de serviço criado!".
- Valores vazios viram `null`; `category_id` vazio vira `null` (`:186-200`).

**Excluir** (`:900-917`): confirmação "Excluir Tipo de Serviço" — "Tem certeza que deseja excluir este tipo de serviço? Esta ação não pode ser desfeita." — "Cancelar"/"Excluir";
toast "Tipo de serviço removido!" (`useServiceTypes.ts:167-182`). É `DELETE` real (não há exclusão lógica).

**Celular (<1024 px)**: lista de cartões com menu de ação (Editar/Excluir), preço formatado quando existe (`:520-575`), filtro por categoria em gaveta, FAB "Tipo";
tocar num item abre a ficha com "Voltar aos tipos de serviço" (`:395-400`).

### 3.3 Janela "Categorias de Serviço" — `ServiceTypeCategoriesDialog.tsx`
- Abre pelo botão "Categorias"; modal de 480 px (`:81-86`). Título "Categorias de Serviço".
- Lista arrastável (alça) com nome + cor; edição inline (clicar em "Editar" no menu da linha; Enter salva, Esc cancela, `:222-223`); menu de linha "Editar"/"Excluir" (`os.ts:609-610`).
  Vazio: "Nenhuma categoria cadastrada." (`:90`).
- Rodapé de criação: rótulo "Nova categoria", campo placeholder "Nome da categoria...", seletor de cor (`ui/ColorPicker.tsx`, 19 cores prontas + conta-gotas, padrão `#6B7280`)
  e botão "+" (Enter também cria) (`:123-142`). Toasts "Categoria criada!", "Categoria atualizada!", "Categoria excluída!" (`useServiceTypeCategories.ts:49,73,91`).
- Excluir: "Excluir categoria?" — "A categoria será removida. Tipos de serviço vinculados ficarão sem categoria." — "Cancelar"/"Excluir" (`os.ts:611-614`).
- Nome repetido: erro "Já existe uma categoria com esse nome." (vem da restrição do banco; o backend falso não tem restrição única).
- Reordenar: arrastar (HTML5) → N `UPDATE ... sort_order` sequenciais (`useServiceTypeCategories.ts:110-122`).

### 3.4 Aba "Tipos de Tarefas" — `TaskTypesPanel.tsx`
- Ações (computador): só **"Novo Tipo"** na linha das abas (`:225-231`). Vazio: "Nenhum tipo de tarefa" / "Cadastre tipos de tarefas para organizar sua agenda" (`os.ts:629-631`).
- Lista: título "Tipos de Tarefas", "N tipo cadastrado/tipos cadastrados" (`:283`), busca "Buscar tipo de tarefa" (`:245,284`), `storageKey service-task-types-list`; linha com ícone CheckSquare;
  subtítulo = descrição ou "Ativo"/"Inativo"; seleciona o primeiro automaticamente (`:139-143`).
- Ficha: "Ficha do tipo de tarefa" + "Excluir" + "Salvar". Campos (nesta ordem, `:49-95`): "Nome *" (placeholder "Ex: Reunião, Entrega, Compra"), "Cor" (hex + seletor nativo, padrão `#8b5cf6`),
  "Descrição" (textarea, placeholder "Descrição do tipo de tarefa"), switch "Ativo" (padrão ligado).
- Modal "Novo Tipo de Tarefa" com "Cancelar"/"Criar" (`:297-309`); **usa estado separado do detalhe** (`createForm` × `detailForm`), por isso NÃO tem o problema do tipo de serviço (P1).
- Toasts: "Tipo de tarefa criado!", "Tipo de tarefa atualizado!", "Tipo de tarefa removido!" (`useTaskTypes.ts:57,77,94`). Excluir: "Excluir Tipo de Tarefa" — "Tem certeza que deseja excluir este tipo de tarefa? Esta ação não pode ser desfeita." (`os.ts:653-654`).
- Onde aparece depois: campo "Tipo de Tarefa" do formulário Nova Tarefa da Agenda, só ativos (`schedule/TaskFormDialog.tsx:295-300`).

### 3.5 Aba "Checklists" — `ChecklistsPanel.tsx`
- Cabeçalho da aba (some quando o editor está aberto, `:249`): "Checklists" / "Modelos de checklist reutilizáveis em OS e PMOC" (`os.ts:429-430`).
- Ações (computador, linha das abas): **"Catálogo de Checklists"** (contorno, ícone livro) e **"Novo checklist"** (primário) (`:271-284`). Celular: botão "Catálogo" e FAB "Checklist".
- Vazio: "Nenhum checklist criado" — "Crie seu primeiro checklist para padronizar as inspeções em campo." (`:296-300`; `os.ts:436-438`).
- Lista (`ListDetailLayout`, `:389-403`): título "Lista de checklists", descrição "Selecione para visualizar ou editar", busca "Buscar checklist...", ordenar Nome (A-Z)/(Z-A),
  **10 por página**, `storageKey service-checklists-list-detail`. Linha: círculo com ícone de documento; título = nome; subtítulo = "N perguntas · Todos os serviços" ou "N serviços"
  (`:85-117`); selo numérico com a contagem. Só mostra checklists com `is_active` (`:68`). Primeiro item selecionado sozinho no computador (`:132-138`).
- Ficha (direita) sem seleção: "Selecione um checklist para visualizar como ele ficará na OS." (`:218`).
- Ficha em modo prévia (`ChecklistOsPreview.tsx:96-170`): sobretítulo "Prévia na ordem de serviço", nome, botões **"Ver"** (olho), **"Adicionar pergunta"** (primário), **"Editar checklist"** (lápis);
  resumo "N perguntas" + "Aplicação: todos os tipos de serviço" (ou nomes dos serviços ligados); lista das perguntas com asterisco vermelho nas obrigatórias; vazio "Este checklist ainda não tem perguntas" /
  "Adicione a primeira pergunta para montar a prévia da OS." (`:146-147`).
- **Modal "Novo Checklist"** (`:416-480`): campo "Nome do checklist" (placeholder "Ex: Checklist de manutenção preventiva"; Enter cria), rótulo "Serviços habilitados", switch **"Todos os serviços"** (padrão ligado);
  desligando, aparece grade de caixas com os tipos de serviço ATIVOS (bolinha de cor + nome + categoria embaixo). Rodapé "Cancelar"/"Criar" ("Criar" desabilitado sem nome).
  Fluxo (`handleCreate` `:156-170`): cria o modelo → se "Todos" desligado grava os vínculos → fecha → seleciona o novo → **abre o editor** (`openEditor`). Toast "Template criado com sucesso!" (`useFormTemplates.ts:98`, vocabulário antigo, P3).
- Catálogo (`:483-492`): botão "Catálogo de Checklists" abre o `ChecklistCatalogModal` em `mode="create"`; ao terminar chama `onCreated(id)` → seleciona e abre o editor.
- Mobile: menu da linha "Visualizar / Editar" e "Excluir" (que, na verdade, abre "Desativar checklist?") (`:340-356`, P3). Erro de carga: "Não foi possível carregar os checklists" / "Verifique sua conexão e tente novamente." / "Tentar novamente" (`:234-247`).
- Desativar: "Desativar checklist?" — "O checklist "{nome}" deixará de aparecer na listagem e não poderá mais ser vinculado em novas OSs, mas continuará preservado nas OSs já existentes." — "Cancelar"/"Desativar" (`:502-520`; `os.ts:461-463`); toast "Checklist desativado!".

### 3.6 Janela "Catálogo de Checklists" — `technician/ChecklistCatalogModal.tsx` (`os.ts:1354-1400`)
- Modal largo (`sm:max-w-5xl`, `:553-555`). Título "Catálogo de Checklists"; subtítulo (modo criar) "Escolha modelos ou atividades; depois você dá um nome e o checklist é criado já preenchido." (modo importar do editor: "As perguntas escolhidas entram no checklist atual.").
- Aviso âmbar de uma linha: **"Estes são apenas modelos sugeridos."** "Cada empresa deve adequá-los aos seus próprios processos. As perguntas ficam totalmente editáveis depois." (`:572-579`)
- Duas colunas (`:396-440, 580-760`): ESQUERDA busca "Buscar modelo ou pergunta..." + grupos; DIREITA mostra as perguntas do item aberto. Grupo "Modelos de checklist" (refrigeração: **Instalação de Split**, **Higienização de Split**, **Manutenção Preventiva de Split**, **Carga de Gás**);
  grupos "Expansão Direta" e "Sistemas Centrais" do Catálogo PMOC só se `pmoc_activity_catalog` devolver linhas. Vazio: "Nenhum modelo encontrado."; sem direita aberta: "Escolha um modelo ou uma seção da lista para ver as perguntas." (`:660`).
- Cada pergunta do modelo mostra número, texto, selo do tipo (com unidade, ex. "Número (psi)") e selo vermelho de obrigatória.
- Botão no topo da direita: modelo → **"Selecionar"** (modo criar) / **"Importar"** (modo importar); seção PMOC → "Selecionar tudo"/"Importar tudo"; no rodapé, com itens PMOC marcados: "Selecionar N"/"Importar N" (`:547-566, 698`).
- Modo criar: escolher um modelo abre o passo **"Nome do novo checklist"** ("N perguntas selecionadas para o novo checklist.", campo "Nome do checklist", placeholder "Ex: Checklist PMOC mensal", botões "Voltar" e **"Criar checklist"**), cria o modelo e insere as perguntas em lote (`:327-360, 494-545`).
  Toast da inserção em lote: "13 perguntas importadas!" (`useFormTemplates.ts:181`).
- Modo importar (dentro do editor): pula perguntas que já existem pelo TEXTO ("já no checklist"); toasts "Nada a importar" / "Essas perguntas já estão no checklist." e "Importação concluída" / "N pergunta(s) já existiam e foram ignoradas." (`:262-302`).
- Dados vêm de `data/checklistCatalog.ts` (modelos no bundle, unidade/faixa viram `unit`, `expected_min`, `expected_max` na pergunta, `:344-345`).

### 3.7 Editor de checklist — `pages/ChecklistDetail.tsx` (embutido no painel; rota `/checklists/:id`)
- Cabeçalho (`:496-566`): seta **"Voltar à prévia"** (embutido) ou ícone seta (rota); nome grande (clique renomeia no lugar; Enter/blur salva, Esc cancela, `:507-533`) + lápis ao passar o mouse;
  subtítulo "N perguntas"; botões **"Catálogo"** (contorno) e **"Nova Pergunta"** (primário) no computador; switch **"Ativo"** (`:553-558`, grava `is_active` na hora, toast "Template atualizado!"); **lixeira** (ícone, sem texto/tooltip) que abre "Desativar checklist?" (`:559-561`).
- Linha "Serviços habilitados" + `ServicesMultiSelect` à direita (`:566-574`): botão com o resumo ("Todos os serviços" | nome | "N serviços"); popover/gaveta com busca "Buscar serviço...", caixa "Todos os serviços" e um item por tipo ATIVO (bolinha de cor).
  Regra: vazio = todos; desmarcar "Todos" seleciona o PRIMEIRO serviço; salva na hora, toast "Serviços vinculados ao checklist!" (`ui/ServicesMultiSelect.tsx:53-79`; `useFormTemplates.ts:238-262`).
- Seção "Perguntas". Com ≥ 1 pergunta, barra com busca "Pesquisar pergunta, descrição ou tipo...", filtro "Todos os tipos" (+ cada tipo) e ordenação "Ordem do checklist" / "Pergunta A-Z" / (Z-A) / "Tipo de pergunta" (`:589-627`). Lista paginada de 20 em 20 ("1–20 de N", "Anterior", "Próxima") (`:471, 780-796`).
- Vazio: "Nenhuma pergunta criada" — "Clique em "Nova Pergunta" para começar" (`:630-636`).
- Linha de pergunta (`:650-775`): alça de arrastar (computador, `lg:`) com número; setas ▲▼ só abaixo de 1024 px; texto; ponto vermelho "Obrigatória"; descrição com cadeado; "N opções: a, b" nas de Seleção; selos de tipo (ícone + rótulo), selo "Exclusivo"/"Cumulativo" se 2+ tipos,
  selo "Câmera" quando exige câmera, badge de frequência (só `contracts`); ações lápis ("Editar: <pergunta>") e lixeira ("Excluir: <pergunta>").
- **Reordenar só vale** com busca vazia, filtro "Todos os tipos" e ordem "Ordem do checklist" crescente (`canReorder`, `:489`). Arrastar usa HTML5 drag/drop nativo (`:658-662`) → N `UPDATE form_questions SET position` (`useFormTemplates.ts:226-235`).
- Remover pergunta: "Remover pergunta?" — "Esta ação não pode ser desfeita." — "Cancelar"/"Remover" (`:1061-1072`); toast "Pergunta removida!".
- Padrão de nova pergunta: tipo "Verdadeiro/Falso", "Campo obrigatório" LIGADO, modo "Exclusivo" (`:233-236`).

### 3.8 Modal "Nova Pergunta" / "Editar Pergunta" — `ChecklistDetail.tsx:808-1042`
Largura `sm:max-w-[1120px]`; subtítulo "Configure a pergunta e confira, em tempo real, como o técnico verá na ordem de serviço." Duas colunas: formulário (3 blocos numerados) e **prévia à direita**.
- Bloco **1 · "Escreva a pergunta"** ("Seja direto e use a orientação para explicar como executar."):
  - "Pergunta" — placeholder "Ex.: Verificar a pressão do equipamento" (obrigatória; botão desabilitado sem texto).
  - "Orientação para o técnico (opcional)" — textarea, placeholder "Ex.: Com o equipamento ligado, aguarde 5 minutos antes de medir."; nota "Visível para o técnico durante o preenchimento; não aparece no relatório do cliente." (`:845-870`).
- Bloco **2 · "Escolha como responder"** ("Você pode combinar mais de uma forma de resposta."): oito blocos clicáveis (`role=checkbox`): **Verdadeiro/Falso, Conformidade, Texto, Número, Foto, Vídeo, Seleção, Assinatura** (`useFormTemplates.ts:36-45`). Sempre sobra ao menos um (não deixa desmarcar o último, `:318-319`).
  - 2 ou mais marcados → painel **"Modo de resposta múltipla"** com botões **"Exclusivo"** ("O técnico escolhe um único tipo para responder; os outros somem automaticamente.") e **"Cumulativo"** ("O técnico responde todos os tipos juntos nesta pergunta (ex.: marca a opção E anexa a foto).") (`:903-930`).
  - "Seleção" marcado → "Opções de resposta": campo "Adicionar opção..." + botão "+" (Enter adiciona); cada opção vira linha editável com X (`:933-960`).
- Bloco **3 · "Defina as regras"** ("Ajustes de obrigatoriedade, captura e frequência."):
  - Switch **"Campo obrigatório"** (padrão ligado) — "A OS só poderá avançar depois que o técnico responder."
  - Com "Foto": **"Exigir foto da câmera"** ("Bloqueia upload da galeria, exige foto tirada na hora") e **"Permitir múltiplas fotos"** (padrão ligado; "Se desativado, o técnico envia apenas uma foto").
  - Com "Vídeo": **"Exigir gravação na hora"** ("Bloqueia escolha da galeria, o técnico precisa gravar o vídeo no momento").
  - **"Frequência"** ("Em quais visitas esta pergunta deve aparecer.") só com `contracts`: select `FrequencyEditor` com "Toda visita", "Mensal", "Bimestral", "Trimestral", "Semestral", "Anual", "Personalizado…" (`os.ts:518-535`).
- **Prévia à direita** `QuestionOsPreview` (`:50-176`): cabeçalho "Prévia na OS" / "Atualiza enquanto você configura" + selo "Técnico"; cartão "Checklist" com o nome; a pergunta numerada com asterisco se obrigatória; abaixo o controle de cada tipo
  (Verdadeiro/Falso = chave "Sem resposta"; Conformidade = "Conforme", "Não conforme", "N/A"; Texto = "Digite a resposta..."; Número = "Digite o valor medido"; Foto = "Tirar ou anexar foto" (com câmera: "Tirar foto agora");
  Vídeo = "Gravar ou anexar vídeo" ("Gravar vídeo agora"); Seleção = opções ou "Opção 1/Opção 2"; Assinatura = "Área para assinatura"). Com 2+ tipos: "O técnico escolhe uma das formas de resposta abaixo." ou "O técnico preencherá todas as formas de resposta abaixo." Rodapé: "Prévia ilustrativa; nenhuma resposta será salva aqui."
- Rodapé do modal: texto "* Campo obrigatório para salvar", "Cancelar" e **"Nova Pergunta"** (criar) ou **"Salvar Alterações"** (editar) (`:812-830`). Criar fecha o modal; toast "Pergunta adicionada!". Editar não mostra toast de sucesso (`useFormTemplates.ts:188-206`).
- Gravação do tipo: o primeiro marcado é `question_type`; com 2+ vai também em `answer_types` (array) e `answer_mode`; sem Seleção as opções não vão; `position` = quantidade atual de perguntas (`:332-415`).

### 3.9 Prévia "Ver" — `ChecklistPreviewDialog.tsx`
Modal `sm:max-w-3xl` com o nome do checklist e "Como este checklist aparece para o técnico na Ordem de Serviço"; faixa azul "Esta é uma prévia: você pode responder para ver como fica, mas **nada é salvo** e nenhuma Ordem de Serviço é criada."; corpo = `VisitChecklistPanel` (o mesmo do técnico em campo) com equipamento-fantasma `__previa__`; rodapé "Fechar".
Respostas só no estado local (descartadas ao fechar). Sem perguntas: "Nenhuma pergunta neste checklist." (`:36-136`).

---

## 4. Backend por tela (o que o backend falso precisa responder)

Cabeçalhos comuns a toda a aplicação (já cobertos desde o T3): `GET /auth/v1/user`, `GET profiles?select=company_id&user_id=eq.<uid>` (`hooks/useUserCompany.ts:38-51`), `company_modules` e `companies` (`hooks/useCompanyModules.ts:72-110`).

| Tela / ação | Chamada | Evidência | Fakebase hoje |
|---|---|---|---|
| Tipos de Serviços · listar | `GET service_types?select=*&company_id=eq.<id>&order=name` | `hooks/useServiceTypes.ts:54-63` | OK (REST genérico; tabela existe no schema; **sem seed** → lista vazia) |
| · criar | `POST service_types` (sem `company_id`; o servidor completa) com `Prefer: return=representation` + objeto único | `useServiceTypes.ts:70-76` | OK: `applyDefaults` põe `company_id`, `id`, datas (`core/defaults.mjs:40-50`) |
| · editar / excluir | `PATCH service_types?id=eq.<id>` · `DELETE service_types?id=eq.<id>` | `useServiceTypes.ts:89-96, 167-175` | OK (sem emular FKs: apagar tipo usado não dá erro nem limpa `form_template_service_types`) |
| Categorias | `GET service_type_categories?select=*&order=sort_order&order=name`; `POST` (nome, cor, `sort_order`=máx+1, `company_id`); `PATCH`/`DELETE ?id=eq.`; reordenar = N `PATCH sort_order` | `hooks/useServiceTypeCategories.ts:19-22, 35-42, 66-68, 83-85, 117-119` | OK (tabela no schema, sem seed). Sem restrição única de nome, sem `SET NULL` ao apagar categoria |
| Fiscal · cTribNac | `POST /functions/v1/nfse-tax-codes {type:'servico', q:''}` ao abrir o combobox (1x; cache); retry 700 ms/1,8 s se falhar | `fiscal/TaxCodeCombobox.tsx:70, 74-90, 96-106, 130-143` | **LACUNA**: função sem handler devolve `{}` e registra; o combobox mostra "Nenhum código encontrado." (items vazio). Precisa handler `functions/nfse-tax-codes.mjs` |
| Fiscal · NBS | `POST nfse-tax-codes {type:'nbs', q}` (≥ 2 caracteres, debounce 300 ms) | `TaxCodeCombobox.tsx:148-175` | **LACUNA** (mesma função) |
| Tipos de Tarefas | `GET task_types?select=*&company_id=eq.<id>&order=name`; `POST`/`PATCH ?id=eq.`/`DELETE ?id=eq.` | `hooks/useTaskTypes.ts:30-39, 48-50, 67-70, 87-89` | OK (já apareceu no `desconhecidos.log` como `TABELA_SEM_SEED`) |
| Checklists · listar | `GET form_templates?select=*,questions:form_questions(*),service_type_links:form_template_service_types(service_type_id)&order=created_at.desc` (sem filtro de empresa: depende de RLS) | `hooks/useFormTemplates.ts:58-67` | OK (embeds por Relationships em `core/query.mjs`); sem seed |
| · criar modelo | `GET auth/v1/user` + `GET profiles` + `POST form_templates` (`name`, `created_by`, `company_id`) → objeto | `useFormTemplates.ts:84-92` | OK; `is_active` nasce `true` pelo palpite do nome (`ALWAYS_TRUE`, `defaults.mjs:24,66`) |
| · renomear / ativo / desativar | `PATCH form_templates?id=eq.` (`name`/`is_active`) | `useFormTemplates.ts:106-112, 126-133` | OK |
| · perguntas | `POST form_questions` (1) ou array (lote do catálogo); `PATCH ?id=eq.`; `DELETE ?id=eq.`; reordenar = N `PATCH position` | `useFormTemplates.ts:148-153, 169-174, 189-195, 209-213, 226-233` | OK (28 colunas no schema: `answer_types`, `answer_mode`, `require_camera_video`, `freq_*`, `unit`, `expected_*`...) |
| · vincular serviços | `DELETE form_template_service_types?template_id=eq.<id>` e depois `POST` (N linhas, sem `company_id`) | `useFormTemplates.ts:240-252` | OK (tabela de 4 colunas) |
| Catálogo | `GET company_settings` (segmento) · `GET pmoc_activity_catalog?select=...` (≈ 149 linhas globais) | `ChecklistCatalogModal.tsx:136-144`; `hooks/usePmocActivityCatalog.ts` | Segmento OK (`seeds/gen-01-tenant.json`: `refrigeracao`). **`pmoc_activity_catalog` sem seed** (`desconhecidos.log` 14:03:37): só some a seção PMOC; os 4 modelos curados funcionam (local) |
| Prévia "Ver" | nenhuma (estado local); se o técnico-fantasma for usado com foto/vídeo, o campo pode tentar subir arquivo ao storage | `ChecklistPreviewDialog.tsx:36-136` | OK se não anexar arquivo na gravação |
| Realtime / storage / hosts externos | nenhum em T4 | — | — |

Resumo de lacunas do backend falso para T4: (1) handler `nfse-tax-codes` (cTribNac e, se o capítulo mostrar, NBS); (2) seeds por capítulo em `seeds-extra/t4/` (nenhuma tabela de T4 tem
seed, nem em `seeds/`); (3) opcional `pmoc_activity_catalog`. Não há RPC, edge function nem host externo além de `nfse-tax-codes`. A origem real do catálogo fiscal
é a migration `supabase/migrations/20260903182000_nfse_catalogos_tributacao_e_nbs.sql` (cTribNac `140101`/item `14.01` na linha 312; `140601`/item `14.06` na 317) e
`20260907120000_nfse_catalogo_nbs_completo.sql` (NBS); a edge real exige módulo `nfe` ativo e papel que gerencia o sistema (`_shared/nfse-handlers/tax-codes.ts:3-4`).

Colunas gravadas (para os seeds): `service_types` → `name, color, description, is_active, requires_equipment, number_prefix, category_id, codigo_servico, codigo_tributacao_municipal, codigo_nbs, iss_aliquota, item_lc116, default_price` (`ServiceTypesPanel.tsx:186-200`);
`service_type_categories` → `name, color, sort_order, company_id`; `task_types` → `name, color, description, is_active` (+ `icon` na tabela); `form_templates` → `name, description, is_active, created_by, company_id` (+ `is_pmoc_default, pmoc_family, pmoc_tier, service_type_id` não usados em T4);
`form_questions` → `template_id, question, question_type, is_required, description, options, position, require_camera, require_camera_video, allow_multiple_photos, answer_types, answer_mode, unit, expected_min, expected_max, freq_*` ; `form_template_service_types` → `template_id, service_type_id`.

---

## 5. Pegadinhas (para roteiro e gravação)

**P1 · HANDOFF (alta) · "Novo Tipo" no computador, com tipo selecionado, reabre a ficha do tipo selecionado (provável; confirmar rodando).**
`handleNew` zera `editingId` e abre o modal (`ServiceTypesPanel.tsx:151-156`); logo em seguida o efeito `if (selectedType && editingId !== selectedType.id) handleEdit(selectedType)` (`:255-257`)
detecta "o formulário não está no tipo selecionado" e recarrega o formulário e o `editingId` com o tipo selecionado — que no computador existe sempre (seleção automática do primeiro, `:248-253`).
Resultado esperado: modal "Novo Tipo de Serviço" aberto com os dados do tipo selecionado; digitar um nome novo e clicar "Criar" **atualiza o tipo selecionado** (cai no ramo `editingId`, `:201-203`) e o modal não fecha (só o ramo de criar chama `setFormOpen(false)`, `:204-206`).
O criar só funciona limpo com a lista vazia (primeiro tipo). `TaskTypesPanel` não tem o problema (estados `createForm`/`detailForm` separados, `:109-110`). Sem testes automatizados cobrindo o painel (nenhum `*.test.*` para ele). Pedir correção ao time do app antes de gravar vários tipos.

**P2 · "Vinculado a equipamento" × "exige equipamento".** A fala deve usar o rótulo novo. O efeito é só na criação da OS: com o tipo desligado, some o bloco de seleção de equipamentos da etapa "Equipamentos e Checklists" (`ServiceOrderFormDialog.tsx:289-292`); sem tipo escolhido assume "exige" (`:290`). Mudar depois não altera OS já criadas.

**P3 · HANDOFF (baixa) · vocabulário e ações confusas.** "Template criado com sucesso!"/"Template atualizado!" (`useFormTemplates.ts:98,119`) quando a tela diz "checklist"; no menu do celular o item **"Excluir"** de um checklist abre "Desativar checklist?" (`ChecklistsPanel.tsx:340-356`); a **lixeira** do editor não tem texto nem tooltip (`ChecklistDetail.tsx:559-561`) — o robô precisa de seletor por ícone; o switch "Ativo" desativa sem confirmação, enquanto a lixeira pede confirmação.

**P4 · HANDOFF (baixa) · prévia do prefixo ≠ código real.** A tela mostra `→ MP-2026-0001` (ano 2026 fixo e 4 dígitos, `ServiceTypesPanel.tsx:322, 758`), mas a lista de OS monta `prefixo-ano-número` com o número SEM zeros à esquerda e o ano da data agendada: `MP-2026-123` (`pages/ServiceOrders.tsx:187-191`; `lib/osNumber.ts:56-58`). Na fala, dizer "o prefixo aparece no começo do número da OS" sem prometer os zeros.

**P5 · Cor é seletor nativo.** O quadradinho `<input type="color">` abre o seletor do sistema operacional, que não aparece na gravação (ver docs de gravação: janelas fora da página). O campo de texto ao lado recebe o hex (`#3B82F6`) e atualiza o mesmo estado (`ServiceTypesPanel.tsx:695-706`). Em Categorias o seletor é do app (`ColorPicker`, 19 cores) e funciona na tela.

**P6 · Permissão "Checklists" (`screen:questionnaires`) não faz nada** (`usePermissions.ts:60`; ver seção 2). Possível handoff (baixa) para o time remover ou aplicar.

**P7 · Excluir × desativar são coisas diferentes.** Tipo de serviço e tipo de tarefa: "Excluir" apaga a linha (`useServiceTypes.ts:170-173`); o seguro é o switch "Ativo" (some das listas de escolha). Checklist: não existe exclusão, só "Desativar" (`useFormTemplates.ts:126-143`); não há tela para reativar além do switch "Ativo" dentro do editor, mas o checklist inativo some da lista, então na prática não volta pela tela.

**P8 · Lista de checklists só mostra ativos** (`ChecklistsPanel.tsx:68`): ao desligar "Ativo" dentro do editor, o item some da lista e a ficha volta a "Selecione um checklist..." (efeito `:132-138`).

**P9 · "Serviços habilitados": desmarcar "Todos" seleciona o primeiro serviço** (`ServicesMultiSelect.tsx:53-61`) e desmarcar o último volta a "todos" (`:63-79`). Na fala, dizer "marque só os serviços onde esse checklist deve aparecer" e fazer a ação marcando no modal "Novo Checklist" (desligando "Todos os serviços" ali a grade começa vazia).

**P10 · Frequência de pergunta e "Fiscal" aparecem por módulo.** Na Glacial os dois estão ligados; se o roteiro não quiser abrir esse assunto agora, não clicar nessas áreas (e não deixar a câmera focada nelas). `ChecklistDetail.tsx:215, 1025-1037`.

**P11 · Catálogo "modo criar": a escolha é do modelo inteiro.** No botão da aba, "Selecionar" num modelo já pede o nome e cria (não há marcação por pergunta em modelo curado; só nas atividades PMOC) (`ChecklistCatalogModal.tsx:327-360, 698`). Para marcar/desmarcar perguntas é preciso importar dentro do editor depois e apagar o que sobrar.

**P12 · Nenhum toast ao editar pergunta** e o toast de criar pergunta é "Pergunta adicionada!"; ao importar 13 perguntas: "13 perguntas importadas!" (`useFormTemplates.ts:160,181`). Combinar a fala com o que aparece.

**P13 · Ordem alfabética mexe nas seleções.** O primeiro item da lista (pela ordem "Nome (A-Z)") é o que vem selecionado; ao criar o 2º tipo/checklist, a ficha pode abrir em OUTRO item (o primeiro alfabético), não no recém-criado (checklists selecionam o novo, tipos de serviço NÃO: ficam no primeiro) (`ServiceTypesPanel.tsx:248-253`; `ChecklistsPanel.tsx:156-170`).

**Divergências do guia técnico do app (`docs/guia-tecnico/secoes/T4.html`) × código 1.38.6** (usar o código):
(a) guia: "no computador é uma tabela com Cor, Nome, Categoria, Descrição, Prefixo OS, Valor e Ações" e menu de três pontos — hoje é lista + ficha; (b) guia: "as abas aparecem como coluna de navegação à esquerda" — hoje são abas sublinhadas no topo;
(c) guia: "o bloco Vídeo só aparece com o módulo de vídeo" e "Limite de perguntas de vídeo" ao salvar — o código 1.38.6 não tem essa trava nem a mensagem; (d) guia: "Frequência... só com módulo de Contratos" — confere.

---

## 6. 🚫 Não prometer · telas mortas e desligadas que tocam T4

- 🚫 Custo, mão de obra, materiais e BDI do serviço NÃO ficam em Serviços (vivem no Orçamento). Aqui só o "Preço padrão (opcional)", valor único por tipo, usado como sugestão no orçamento quando não há custo calculado (`QuoteFormDialog.tsx:679-696`).
- 🚫 Não existe importação/exportação em massa de tipos, tarefas ou checklists. 🚫 Não existe versionamento de checklist: editar uma pergunta vale para as próximas OS; respostas já gravadas ficam.
- 🚫 Não existem seções/grupos de perguntas dentro do checklist (só a ordem).
- 🚫 "Medição PMOC" não é um tipo escolhível no editor (só o Catálogo PMOC e o contrato criam). Para medir à mão: tipo "Número" e a unidade no texto da pergunta.
- 🚫 "Vídeo": não prometer limite por plano nem "módulo" na tela do editor — a 1.38.6 não aplica nenhum dos dois. Prometer só: o técnico grava/anexa um clipe e há o switch "Exigir gravação na hora".
- 🚫 Não prometer reativar checklist desativado por uma tela dedicada.
- 🚫 `/checklists` e `/questionarios` são endereços antigos que redirecionam para `/servicos` (aba padrão "Tipos de Serviços"); gravar sempre por Gestão › Serviços.
- Código morto/sem uso na 1.38.6: strings de coluna (`colColor`...`colActions`, `badgeYes`, `badgeNo`) e `modalTitleEdit` em `os.ts:539-600`; `videoLimitSingular/Plural` em `os.ts:515-516`; permissão `screen:questionnaires`.
- `QuickServiceTypeDialog` (cadastro rápido: nome, cor, "Vinculado a equipamento"; fiscal opcional) existe em OS/orçamento, fora de T4: não mostrar aqui.

---

## 7. Dúvidas em aberto (só dá para fechar rodando o app)

1. **P1** — confirmar que "Novo Tipo" com tipo selecionado abre com os dados do selecionado e que "Criar" atualiza em vez de criar. (Teste: criar o 1º tipo; clicar "Novo Tipo" de novo.)
2. O que acontece ao "Excluir" um tipo de serviço já usado em OS/orçamento no banco real (erro de FK com toast "Erro ao excluir tipo de serviço"?). No backend falso nada falha.
3. Se `nfse-tax-codes` na produção devolve a lista completa para empresa com `nfe` mas sem certificado/configuração fiscal (afeta o que o aluno vê na própria conta).
4. Se o botão **"Catálogo de Checklists"** do cabeçalho (modo importar) dentro do editor aparece junto com "Catálogo" duplicado no celular (`ChecklistDetail.tsx:580-585`) — irrelevante para o desktop da gravação.
5. Como a câmera/zoom enxerga o quadradinho de cor: o `<input type="color">` pode virar um quadrado sem borda no headless (visual fora do padrão do app).
6. Se o arrastar-e-soltar HTML5 de perguntas/categorias funciona com o passo `drag` do robô no Chromium headless (sem isso, o reordenar fica só na fala ou usa a janela abaixo de 1024 px, o que muda o layout).
7. Se o formato do número no tooltip/lista de OS usa o ano da data agendada (T5) — ver P4.
8. Nome fictício "Glacial Cold Brasil": o comentário de uma migration do app cita uma "Glacial Cold" real (nota fiscal autorizada, `supabase/migrations/20260903182000_nfse_catalogos_tributacao_e_nbs.sql:17-18`). Já foi aprovado no T3; só registrar para o Kaik confirmar que o nome não coincide com cliente real exposto.
