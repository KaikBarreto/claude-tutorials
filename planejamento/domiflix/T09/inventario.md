# Inventário funcional · T9 — Orçamentos, Precificação e Proposta (Dominex)

> Base para o roteiro do tutorial "T9 · Orçamentos, Precificação e Proposta" da Domiflix. Levantado em 30/10/2026 contra o
> código publicado `APP_VERSION = "1.38.6"` (`src/config/version.ts:1`), cópia em `/home/claude/domiflix/src-1.38.6`.
> **Análise estática, somente leitura**: nada foi executado no app. O que só se confirma rodando está marcado
> "(a confirmar)" e repetido na seção 7. Fontes escritas secundárias: a trilha validada na 1.22.5
> (`_referencia/trilha-de-tutoriais_v1.22.5.md`, T9, linhas 362-396) e o Guia Técnico do app
> (`docs/guia-tecnico/secoes/T9.html`, que diz descrever a 1.38.x mas **diverge do código em pontos importantes**: seção 0.4).
> **Onde as fontes e o código divergem, vale o código.**

## Como ler

- Caminhos relativos a `src/`, exceto os que começam com `supabase/`, `docs/` ou `rec/`. Formato `arquivo:linha`.
- Texto entre aspas "assim" é o rótulo exato da tela (pt-br). Fonte principal dos rótulos: `lib/i18n/messages/app/crm.ts`,
  bloco pt-br (linhas 11-1238): orçamentos 403-649, proposta (página pública e "Configurar Proposta") 652-746, custos dos
  serviços 749-792, custos globais 795-865, precificação 868-914, janelas de custo 918-1115, resumo do BDI 1116-1132, PDF 1133-1238.
- "Wizard" = a janela "Novo Orçamento" (5 etapas). "Prospecto" = destinatário que ainda não é cliente cadastrado. "BDI" = fator
  que divide o custo para chegar ao preço (seção 3.6). "Tenant" = empresa cliente (aqui, Glacial Cold Brasil).
- Componentes compartilhados (janelas, abas, toasts) estão no inventário do T3. Fora deste tutorial, mas citados onde tocam:
  Estoque (T8), tipos de serviço (T4), OS (T5), Financeiro (T13), cobrança (T19), CRM (T10), Configurações (T1).

---

## 0. Resumo para o roteiro

(preenchido no fim)

---

## 1. Rotas e navegação

| Endereço (pt-br) | O que abre | Código |
|---|---|---|
| `/orcamentos` | Tela "Orçamentos" (subtítulo "Gerencie orçamentos, custos e precificação"), com 4 abas laterais. Tradução do endereço: en `/quotes`, es `/presupuestos`, fr `/devis` | `App.tsx:805`, `lib/i18n/appRouteSlugs.ts:56,137`, `lib/i18n/messages/app/crm.ts:405-408` |
| (sem endereço próprio) | As 4 abas ("Orçamentos", "Custos dos Serviços", "Custos Globais", "Precificação") **não têm URL**: a aba ativa é estado local; ao sair e voltar abre sempre em "Orçamentos" | `pages/Quotes.tsx:1030,1051-1054` |
| `/proposta/:token` | **Link público** que o cliente abre, sem login (página "Proposta Comercial"); `?preview=1` marca a abertura do próprio dono (não conta visualização) | `App.tsx:767`, `pages/ProposalPublic.tsx:396-402` |
| `/orcamento/:token` | Endereço antigo: só redireciona para `/proposta/:token` | `App.tsx:761`, `pages/QuotePublic.tsx:3-5` |
| `/proposta` (sem token) | **Não é desta aula**: é o "Simulador de Proposta" da própria Dominex (módulos e valores de plano, atrás de assinatura). Fora do vídeo (regra "sem preços de plano") | `App.tsx:766`, `hooks/usePageTitle.ts:39`, `pages/ProposalSimulator.tsx:36-60` |

- **Como se chega:** Menu lateral "Orçamentos" (item solto, entre "Área do Técnico™" e o grupo "Gestão", `components/layout/SidebarMenuContent.tsx:107-108`), menu
  superior (`components/layout/TopNavbar.tsx:98`), menu "Mais" do celular (`components/layout/MoreMenuDrawer.tsx:94`), atalho **Shift+Q**
  (`hooks/useKeyboardShortcuts.ts:25`). Título da aba do navegador "Orçamentos" (`hooks/usePageTitle.ts:17`); mensagem de
  carregamento "Buscando orçamentos..." (`hooks/useRouteLoadingMessage.ts:34`).
- **Quatro abas na lateral** (`components/SettingsSidebarLayout`, o mesmo layout de Configurações): "Orçamentos" (a lista), "Custos dos
  Serviços", "Custos Globais", "Precificação" (`pages/Quotes.tsx:59-64`, `lib/i18n/messages/app/crm.ts:409-412`). **As quatro aparecem para todo plano**: não há
  checagem de módulo na tela (seção 2).
- **Janelas e diálogos da tela** (todos abrem por cima, sem trocar de endereço): "Novo Orçamento" (wizard), "Proposta #N" (visualizar), "Configurar Proposta" (wizard de 3 etapas),
  "Aprovar Orçamento #N", distribuição dos serviços por equipamento (antes de "Gerar OS"), "Desfazer o lançamento?", "Excluir orçamento?", cobrança
  (`pages/Quotes.tsx:894-1024`).
- **Telas vizinhas** (não são desta aula, mas aparecem no caminho): cliente cadastrado no "+" do wizard (T3), tipo de serviço criado no "+" (T4),
  movimentações do Financeiro ao "Ver lançamento no financeiro" (T13, `pages/Quotes.tsx:233-236`), nova OS gerada (T5), ajuste do modo de aprovação em Configurações (T1).

---

## 2. Permissões e módulos

| Quem / o quê | Regra | Código |
|---|---|---|
| Ver o item de menu e abrir `/orcamentos` | Permissão de tela `screen:quotes` ("Orçamentos": "Orçamentos e propostas enviadas aos clientes.", grupo Comercial) | `hooks/usePermissions.ts:66`, `App.tsx:805`, `components/layout/SidebarMenuContent.tsx:108` |
| Módulo pago | **Nenhum.** `screen:quotes` pertence ao módulo `basic` (todo plano). A rota não usa `ModuleRoute` | `hooks/useCompanyModules.ts:50`, `App.tsx:805` |
| "🔒 Precificação Avançada" (trilha) | **Não bloqueia mais nada.** O código do módulo `pricing_advanced` existe só como tipo e no simulador de planos; **nenhuma tela o consulta**. Desde a 1.29.0 (13/10/2026) "Precificação Avançada, incluindo o cálculo de BDI, ... faz parte de todos os planos"; no banco o preço do módulo é 0 e a descrição diz "inclusos na base" | `hooks/useCompanyModules.ts:19`, `pages/Changelog.tsx:2217`, `supabase/migrations/20261013120000_trial_7d_reprice_plans_and_base_features.sql:23,30` |
| Ver as abas de custos e precificação | Quem abre a tela de Orçamentos vê as 4 abas (não há permissão própria nem módulo) | `pages/Quotes.tsx:1046-1055` |
| Criar/editar/excluir orçamento, aprovar por dentro, rejeitar, gerar link | Sem chave própria: qualquer pessoa com a tela. (A segurança de dados é a RLS da tabela `quotes`, seção 5) | `pages/Quotes.tsx:439-547,802-863` |
| **"Gerar OS"** | Só aparece para admin/gestor **ou** quem tem `fn:create_os` ("Criar OS") | `pages/Quotes.tsx:165,484,827`, `hooks/usePermissions.ts:102` |
| **"Desfazer lançamento"** | Só admin/gestor **ou** quem tem registro de permissões **com** `fn:delete_finance` ("Excluir Lançamento Financeiro"); espelha a RLS de exclusão do Financeiro | `pages/Quotes.tsx:171,505,842`, `hooks/usePermissions.ts:111` |
| **"Gerar cobrança"** | Só com o módulo **Cobranças** ligado **e** conta de recebimento ativa **e** orçamento de cliente cadastrado (não de prospecto) **e** sem lançamento financeiro já gerado | `pages/Quotes.tsx:161-163,520,848` |
| "Aprovar orçamento" | Escondido se o orçamento já gerou lançamento, se já tem cobrança gerada (evita duas receitas) ou se não está em Rascunho/Enviado | `pages/Quotes.tsx:462-473,811-815`, `hooks/useQuoteChargedIds.ts:1-70` |
| Link público `/proposta/:token` | **Sem login.** Quem tem o endereço vê a proposta e responde; o acesso é pelo token do orçamento (RPCs `SECURITY DEFINER`, seção 4) | `pages/ProposalPublic.tsx:126-236`, `supabase/migrations/20261013023000_quote_public_payload_country_regional.sql:7-159` |
| Opções da empresa que mudam a aprovação | Em Configurações > Usabilidade > "Orçamento, OS e financeiro": "Ao aprovar um orçamento" ("Já recebi" × "Vou receber depois") e "Aprovação pelo link da proposta já gera conta a receber" (vem **desligada**). Quem edita: quem tem permissão de salvar Configurações. Detalhe no inventário do T1 | `pages/Settings.tsx:1722-1775`, `lib/i18n/messages/app/settings.ts:264-276`, `supabase/migrations/20260911200000_orcamento_recebivel_parcelado_e_aprovacao_publica.sql:33-55` |

> **Para o roteiro:** o tutorial pode dizer, sem risco, que "quem tem a tela Orçamentos liberada monta orçamentos e propostas; gerar a OS e desfazer o lançamento dependem de
> permissão própria". **Não** dizer que Custos Globais e Precificação "são do plano avançado" (a trilha de 1.22.5 dizia; hoje valem para todo plano).

---

## 3. Por tela, janela e aba (rótulos exatos)

(preenchido por partes)

---

## 4. Backend por tela e comparação com o fakebase

(preenchido por partes)

---

## 5. Pegadinhas

(preenchido por partes)

---

## 6. 🚫 Não prometer / telas mortas

(preenchido por partes)

---

## 7. Dúvidas em aberto

(preenchido por partes)
