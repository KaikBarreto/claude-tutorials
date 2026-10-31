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

### 0.1 Capítulos da trilha (1.22.5) × código de hoje (1.38.6)

| # | Capítulo da trilha | O que o código faz hoje | Veredito | Onde |
|---|---|---|---|---|
| 1 | Tela Orçamentos: indicadores | Cartões "Em Aberto", "Conversão", "Ticket Médio"; as 4 abas ficam **no topo**; "Conversão" não conta "Convertido" | Vale, com ajuste | 3.1, P11 |
| 2 | Etapa 1 Destinatário | "Cliente cadastrado" × "Novo prospecto"; o "+" cria o cliente na hora (T3) | Vale | 3.2 |
| 3 | Etapa 2 Serviços e preço padrão | "Serviços e mão de obra": bloco "Configurações BDI" e seletor de serviço; preço = custo ÷ BDI, senão preço padrão do tipo, senão 0 | Vale; a ordem do preço é nova | 3.2.1, P8 |
| 4 | Etapa 3 Materiais | Botão "Adicionar materiais" (seletor em lote); preço de venda, sem BDI; sem saldo na tela | Mudou | 3.2.3 |
| 5 | Etapa 4 Desconto e brindes | "Desconto e condições": R$ × %, "Incluir brindes"; **aqui** ficam "Observações" e "Condições / Termos" | Vale, com cuidado | 3.2, P9, P18 |
| 6 | Etapa 5 Revisão | "Validade e revisão": "Válido até", "Template da Proposta" (Clean), parcelas, 1º vencimento, "Resumo do Orçamento" | Mudou (observações e termos saíram daqui) | 3.2 |
| 7 | 🔒 Custos do Serviço | Aba "Custos dos Serviços", **sem bloqueio**; sub-abas "Mão de obra", "Recursos" (com os brindes), "Materiais" e "Resumo"; salva sozinha | Vale; o 🔒 caiu | 3.8, P7 |
| 8 | 🔒 Custos Globais | Aba cujo título na tela é "Centro de Custos", **sem bloqueio**; lista pesquisável e ficha (29/10) | Vale; o 🔒 caiu | 3.9, P7 |
| 9 | 🔒 Precificação (BDI) | Aba "Precificação", sem bloqueio; **empresa nova começa zerada** (BDI 1,0000) | Vale; o 🔒 caiu; padrões mudam | 3.10, P6 |
| 10 | Configurar Proposta | Assistente de 3 etapas; 4 modelos; escolher modelo ali é só prévia; logo com tamanho; 7 seções (só o Clean reordena) | Vale, com ajustes | 3.7, P17 |
| 11 | Link, WhatsApp, PDF | "Gerar link da proposta" (promove a Enviado); "WhatsApp" e "PDF" na janela Visualizar | Vale | 3.1, 3.3, P3 |
| 12 | Visão do cliente | `/proposta/<token>`; "Aprovar"/"Rejeitar" só em Enviado; "Baixar PDF"; "Pagar" | Vale (gravação por navegação interna) | 3.11, 4.3 |
| 13 | Contador de visualizações | "Não visualizada" / "Visualizada N× · última vez…"; mesma pessoa em 30 min não conta de novo; `?preview=1` não conta | Vale | 3.1, 3.11 |
| 14 | Aprovar … Converter em OS | "Aprovar Orçamento" com "Já recebi" × "Vou receber depois" e **sem custo**; **"Gerar OS"** com "Distribuir serviços" e **sem estoque** | **Mudou muito** | 3.4–3.6, P1, P2 |
| ⚠ | Link promove a Enviado | Continua verdade: só "Gerar link da proposta" | Vale | P3 |
| ⚠ | Aprovar lança receita + custo + MO e trava | **Desatualizado**: só receita, e existe "Desfazer lançamento" | Trocar | P2, 3.6 |
| ⚠ | Converter cria OS avulsa e baixa estoque | **Desatualizado**: "Gerar OS", sem baixa; antes de 08/10/2026 nem funcionava | Trocar | P1, 4.2 |
| ⚠ | 🔒 Precificação Avançada (e a margem na lista) | **Caiu**: todos os planos desde a 1.29.0; a margem não tem bloqueio | Trocar | P7, 2 |
| 🚫 | Sem contrato, assinatura nem lembrete | Continua verdade | Vale | 6 |

### 0.2 O que mudou desde a 1.22.5 (04/09/2026) até a 1.38.6 (30/10/2026), só o que toca este tutorial

| Versão · data | Mudança | Onde pesa | Changelog |
|---|---|---|---|
| 1.23.1 · 06/09 | "Novo Orçamento" e "Configurar Proposta" redesenhados (menos caixas dentro de caixas) | telas diferentes da trilha | `pages/Changelog.tsx:4556` |
| 1.24.4 · 08/09 | "Ver lançamento no financeiro"; orçamento não fica mais preso como recebido | menu da linha, 4.2 | `pages/Changelog.tsx:4390-4396` |
| 1.24.5 e 1.24.7 · 09/09 | Aprovar deixa de lançar custo de material e mão de obra | P2 | `pages/Changelog.tsx:4349,4378` |
| 1.24.11 · 11/09 | Aprovar: "Já recebi" × "Vou receber depois" | 3.4 | `pages/Changelog.tsx:4276` |
| 1.24.15 · 12/09 | Tarifa maior que a venda é bloqueada; orçamento com cobrança não aprova por cima | 3.4, P30 | `pages/Changelog.tsx:4209-4213` |
| 1.24.43 · 18/09 | "Adicionar materiais" (seletor em lote) | 3.2.3 | `pages/Changelog.tsx:3497` |
| 1.24.51 · 19/09 | Aprovação pelo link usa o nome atual da categoria de receita | 3.11 | `pages/Changelog.tsx:3271` |
| 1.28.22 · 08/10 | "Converter em OS" volta a funcionar (antes dava erro e nada era criado); orçamento não fica mais travado | 4.2 | `pages/Changelog.tsx:2261-2272` |
| 1.29.0 · 13/10 | Precificação Avançada (BDI) em todos os planos | P7 | `pages/Changelog.tsx:2217` |
| 1.31.6 a 1.31.9 · 14/10 | Propostas e PDF com layout correto; celular; "Sobre a empresa" em todos os modelos; tamanho do logo | 3.7, 3.11 | `pages/Changelog.tsx:2018-2064` |
| 1.36.22 e 1.36.24 · 19/10 | "Converter em OS" vira "Gerar OS"; distribuir os serviços por equipamento antes | 3.5, P1 | `pages/Changelog.tsx:1178,1227` |
| 1.37.10 · 19/10 | O valor cadastrado do serviço entra sozinho no orçamento | P8 | `pages/Changelog.tsx:971` |
| 27/10 (só migration) | A OS recebe o **total comercial** do orçamento | P5 | `supabase/migrations/20261027120000_orcamento_total_comercial_na_conversao_os.sql:8-30` |
| 1.37.55 · 29/10 | Abas internas horizontais; "Custos Globais" com busca e ficha | seção 1, 3.9 | `pages/Changelog.tsx:161,176` |

Não são desta aula: 1.28.19, 1.31.8 e 1.35.6 tratam do **simulador de proposta da Dominex** (planos e descontos de assinatura), fora do vídeo.

### 0.3 O que pode surpreender o roteirista

1. **O orçamento mostra dois valores** ("Total do orçamento" e "Sugestão pelo BDI"); só o primeiro vai ao cliente e à OS (P5).
2. **Nem aprovar nem "Gerar OS" mexem em custo ou estoque** (P1, P2); a trilha e o Guia dizem o contrário.
3. **Empresa nova começa com Precificação zerada**: sem salvar as taxas, BDI = 1,0000 e preço = custo (P6).
4. **Só "Gerar link da proposta" muda para Enviado**; WhatsApp e PDF não (P3). Sem isso o cliente abre a proposta **sem botões**.
5. **Aprovação do cliente no link não lança financeiro** por padrão e deixa o orçamento sem o item "Aprovar orçamento" (P4).
6. **As "Observações" saem impressas** para o cliente (P9).
7. **As quatro abas ficam no topo**, não na lateral (seção 1).
8. **"Expirado" é só visual** (P10).
9. **Segurança, para o Kaik decidir:** quem tem o link pode ler custo e margem pela API aberta (P27). Não é assunto do vídeo.

### 0.4 Divergências do Guia Técnico (`docs/guia-tecnico/secoes/T9.html`, escrito entre a 1.29.0 e a 1.36.22; vale o código)

- **D1.** "Barra lateral de abas" (`docs/guia-tecnico/secoes/T9.html:16,19`) × barra horizontal no topo (seção 1).
- **D2.** Padrão de fábrica 10/12/10/R$ 1,00/6%/10 (`docs/guia-tecnico/secoes/T9.html:104-107`) × empresa nova zerada (P6).
- **D3.** Materiais: "Selecionar do estoque…", "Ou digite o nome do material…" (`docs/guia-tecnico/secoes/T9.html:136`) × botão único "Adicionar materiais" com seletor em lote (3.2.3).
- **D4.** Aprovar: "Como o cliente pagou? Vamos lançar a receita e os custos…", "Valor recebido *", botão "Confirmar recebimento", **quatro lançamentos** (receita, "CMV - Materiais", "CMV - Mão de Obra Avulsa", tarifa) e selo "Recebido" (`docs/guia-tecnico/secoes/T9.html:347-366`) × dois modos, botões "Aprovar e lançar receita" / "Aprovar e gerar conta a receber", **só receita**, selo "No financeiro" (3.4, 3.1). O texto antigo sobrevive no i18n morto `approveDesc` (P26).
- **D5.** "Aprovar é via de mão única… não dá para desaprovar" (`docs/guia-tecnico/secoes/T9.html:368,389`) × existe "Desfazer lançamento" (3.6).
- **D6.** "Converter em OS", toast "Orçamento convertido!", descrição "Convertido do Orçamento #", **baixa de estoque na conversão** (`docs/guia-tecnico/secoes/T9.html:378-382,496`) × "Gerar OS", "OS gerada com sucesso!", "Gerada do Orçamento #N", sem baixa (3.5, P1).
- **D7.** "Expirado automático ao abrir a tela" e "o orçamento expira sozinho" (`docs/guia-tecnico/secoes/T9.html:53,493`) × só visual (P10).
- **D8.** PDF "proposta-<número>.pdf" (`docs/guia-tecnico/secoes/T9.html:300`) × "Proposta - <Cliente> DD MÊS AAAA.pdf" (3.3).
- **D9.** O aviso do sino "leva direto ao orçamento" (`docs/guia-tecnico/secoes/T9.html:316`) × cai na lista (P31).
- **D10.** O Guia acerta em: Observações impressas (P9), "Gerar link" promove a Enviado, WhatsApp não muda status (P3), modelo do Configurar Proposta só prévia (P17), aprovação do cliente sem financeiro (P4), BDI mínimo 0,01.

---

## 1. Rotas e navegação

| Endereço (pt-br) | O que abre | Código |
|---|---|---|
| `/orcamentos` | Tela "Orçamentos" (subtítulo "Gerencie orçamentos, custos e precificação"), com 4 abas em barra horizontal no topo. Tradução do endereço: en `/quotes`, es `/presupuestos`, fr `/devis` | `App.tsx:805`, `lib/i18n/appRouteSlugs.ts:56,137`, `lib/i18n/messages/app/crm.ts:405-408` |
| (sem endereço próprio) | As 4 abas ("Orçamentos", "Custos dos Serviços", "Custos Globais", "Precificação") **não têm URL**: a aba ativa é estado local; ao sair e voltar abre sempre em "Orçamentos" | `pages/Quotes.tsx:1030,1051-1054` |
| `/proposta/:token` | **Link público** que o cliente abre, sem login (página "Proposta Comercial"); `?preview=1` marca a abertura do próprio dono (não conta visualização) | `App.tsx:767`, `pages/ProposalPublic.tsx:396-402` |
| `/orcamento/:token` | Endereço antigo: só redireciona para `/proposta/:token` | `App.tsx:761`, `pages/QuotePublic.tsx:3-5` |
| `/proposta` (sem token) | **Não é desta aula**: é o "Simulador de Proposta" da própria Dominex (módulos e valores de plano, atrás de assinatura). Fora do vídeo (regra "sem preços de plano") | `App.tsx:766`, `hooks/usePageTitle.ts:39`, `pages/ProposalSimulator.tsx:36-60` |

- **Como se chega:** Menu lateral "Orçamentos" (item solto, entre "Área do Técnico™" e o grupo "Gestão", `components/layout/SidebarMenuContent.tsx:107-108`), menu
  superior (`components/layout/TopNavbar.tsx:98`), menu "Mais" do celular (`components/layout/MoreMenuDrawer.tsx:94`), atalho **Shift+Q**
  (`hooks/useKeyboardShortcuts.ts:25`). Título da aba do navegador "Orçamentos" (`hooks/usePageTitle.ts:17`); mensagem de
  carregamento "Buscando orçamentos..." (`hooks/useRouteLoadingMessage.ts:34`).
- **Quatro abas no topo** (barra horizontal sublinhada, com rolagem se faltar espaço; no celular, pílulas; o mesmo componente das Configurações, sem a variante lateral): "Orçamentos" (a lista), "Custos dos
  Serviços", "Custos Globais", "Precificação" (`pages/Quotes.tsx:72-78,1051-1055`, `components/SettingsSidebarLayout.tsx:74,99-139`, `lib/i18n/messages/app/crm.ts:409-412`). A barra horizontal vale desde a 1.37.55 (29/10/2026, "Abas internas mais consistentes", `pages/Changelog.tsx:176-178`). **As quatro aparecem para todo plano**: não há
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

> Rótulos do pt-br em `lib/i18n/messages/app/crm.ts` (bloco `quotes`, 403-649) salvo indicação. **Textos fixos em português dentro do código**
> (não passam pelo i18n) estão marcados "(fixo)": as mensagens dos hooks (`hooks/useQuotes.ts:244,279,297,311`) e o selo "Lançamento financeiro gerado".

### 3.1 Aba "Orçamentos" (a lista) — `pages/Quotes.tsx:156-1027`

| Elemento | Rótulo exato e comportamento | Código |
|---|---|---|
| Topo (desktop) | Dois botões à direita: "Configurar Proposta" (contorno) e "+ Novo Orçamento". No celular: botão flutuante "Orçamento"; "Configurar Proposta" fica dentro do filtro | `pages/Quotes.tsx:590-599,398-406,884-891` |
| Cartão "Em Aberto" | Soma do **valor** das propostas em "Enviado". **Clicar** filtra a lista por Enviado | `pages/Quotes.tsx:323-331`, `hooks/useQuotes.ts:401` |
| Cartão "Conversão" | Aprovados ÷ (Enviado + Aprovado + Rejeitado), em %, arredondado. **Clicar** filtra por Aprovado. "Convertido" (OS já gerada) **não entra na conta**: a % cai depois do "Gerar OS" `[handoff]` | `pages/Quotes.tsx:332-340`, `hooks/useQuotes.ts:402-404` |
| Cartão "Ticket Médio" | Média do valor dos orçamentos "Aprovado" (0 se não há) | `pages/Quotes.tsx:341-348`, `hooks/useQuotes.ts:405-407` |
| Busca | Placeholder "Buscar por cliente, número ou telefone...". Procura no nome do cliente, nome do prospecto, nº e telefone (telefone só com 6+ dígitos) | `pages/Quotes.tsx:414-418,286-303` |
| Filtro "Status" | Botão de filtro dentro da busca, com caixas "Rascunho · Enviado · Aprovado · Rejeitado · Expirado · Convertido"; vazio = "Todos" | `pages/Quotes.tsx:373-382,420-432` |
| Colunas | "Nº" (com `#`), "Cliente", "Data" (dd/MM/aa), "Custo" e "Margem" (só tela larga), "Valor", "Status", "Ações". Ordenáveis: Nº, Cliente, Data, Custo, Valor, Status | `pages/Quotes.tsx:726-736` |
| "Cliente" | Nome do cliente cadastrado, ou do prospecto com o sufixo "(prospecto)". Embaixo, o indicador de visualização: "Não visualizada" (olho apagado) ou olho + nº + "· visto há X"; dica ao pairar: "Visualizada N× · última vez dd/MM HH:mm (há X)" | `pages/Quotes.tsx:113-154,746-756` |
| "Custo" / "Valor" / "Margem" | Custo = `total_cost` ou "—". Valor = `total_value` (cai para `total_price` em registro antigo). Margem = (valor − custo) ÷ valor, em %: selo verde ≥ 20, amarelo de 0 a 19, vermelho se negativo, "—" sem custo | `pages/Quotes.tsx:739-742,760-772`, `lib/quote-commercial-total.ts:9-11` |
| "Status" | Selo colorido: Rascunho (cinza), Enviado (azul), Aprovado (verde), Rejeitado (vermelho), Expirado (âmbar), Convertido (índigo) | `pages/Quotes.tsx:89-96,773-782` |
| Selos na coluna "Ações" | "No financeiro" (verde; dica fixa "Lançamento financeiro gerado") quando já gerou lançamento; "Cobrança gerada" (âmbar; dica "Este orçamento já tem uma cobrança gerada. Aprovar agora criaria a receita duas vezes.") quando existe cobrança. O primeiro marca "gerou lançamento", **não** "dinheiro recebido" (a aprovação pode ter sido "Vou receber depois") | `pages/Quotes.tsx:785-801` |
| Vazio | "Nenhum orçamento cadastrado" / "Crie seu primeiro orçamento para começar" + botão "Novo Orçamento". Com busca/filtro: "Nenhum orçamento encontrado" / "Tente outro termo ou ajuste os filtros" | `pages/Quotes.tsx:623-649` |
| Excluir | Janela "Excluir orçamento?" / "Esta ação não pode ser desfeita." / "Cancelar" · "Excluir"; toast (fixo) "Orçamento excluído!". Vale para qualquer status; a tela não confere se já há lançamento ou OS ligados (pelas chaves do banco, os itens caem junto e o lançamento e a OS ficam: 4.1; a confirmar rodando, seção 7) | `pages/Quotes.tsx:924-940`, `hooks/useQuotes.ts:304-316` |

**Menu "⋮" da linha** (ordem real; item some quando a condição falha) — `pages/Quotes.tsx:802-863`:

| # | Item | Aparece quando | O que faz |
|---|---|---|---|
| 1 | "Visualizar" | sempre | Abre a janela "Proposta #N" (3.3) |
| 2 | "Abrir proposta em nova guia" | sempre | `window.open` de `…/proposta/<token>?preview=1` em **outra aba** (o recorder não segue nova aba: TRILHA 5-8) |
| 3 | "Gerar link da proposta" | sempre | Copia o link para a área de transferência, toast "Link gerado e copiado!" / "Já pode colar e enviar pro cliente." (se o navegador bloquear: toast "Link da proposta gerado" com o link no texto). **Se está em Rascunho, vira "Enviado"** (e aparece o toast fixo "Status atualizado!"). Nunca rebaixa Aprovado/Rejeitado/Convertido/Expirado | `pages/Quotes.tsx:190-214`, `utils/shareLinks.ts:62-67` |
| 4 | "Aprovar orçamento" | Rascunho **ou** Enviado, sem lançamento gerado e sem cobrança gerada | Abre "Aprovar Orçamento #N" (3.4) |
| 5 | "Rejeitar" | só Enviado | Muda para Rejeitado **na hora, sem confirmação e sem desfazer**; toast "Status atualizado!" `[handoff]` |
| 6 | "Gerar OS" | Aprovado, sem OS ligada, e quem tem `fn:create_os` (ou admin/gestor) | Abre a distribuição por equipamento (3.5) |
| 7 | "Ver lançamento no financeiro" | tem lançamento | Vai para `/financeiro/movimentacoes?txn=<id>` (T13) |
| 8 | "Desfazer lançamento" | tem lançamento **e** permissão de excluir lançamento | Janela de confirmação (3.6) |
| 9 | "Gerar cobrança" | módulo Cobranças + conta ativa + cliente cadastrado + sem lançamento | Janela de cobrança (T19) |
| 10 | "Editar" | **todos os status** (inclusive Aprovado/Convertido) | Abre o wizard preenchido (3.2). A edição não refaz lançamento nem OS já gerados `[handoff]` |
| 11 | "Excluir" | sempre | "Excluir orçamento?" |

- **Mobile** (fora do vídeo, que é 1280×800): mesma lista no menu de cada cartão, com rótulos curtos "Abrir proposta" e "Ver no financeiro" (`pages/Quotes.tsx:438-547`, `crm.ts:473-478`).
- **Dica de gravação:** a linha "Gerar link da proposta" é o jeito de **mostrar** o "Rascunho → Enviado" sem abrir nada fora do app; no gravador o toast pode cair no texto alternativo se a área de transferência falhar (inócuo).

### 3.2 Janela "Novo Orçamento" (wizard de 5 etapas) — `components/quotes/QuoteFormDialog.tsx` (rótulos `crm.ts:528-649`)

**Moldura:** janela larga (até 920 px, `QuoteFormDialog.tsx:1639`), **sem fechar ao clicar fora** (`lockBackdrop`, `:1641`). Título "Novo Orçamento" (novo) ou "Editar Orçamento #N" (editar)
(`:1629-1631`; o "Rascunho de Orçamento" só existiria entre o 1º "Salvar rascunho" e o fechamento da janela, que é imediato: na prática não aparece).
Barra de progresso + 5 bolinhas numeradas com o nome da etapa (nome some em tela estreita). Dá para clicar numa etapa **já visitada** ou na **próxima**
(só se o destinatário estiver escolhido); em edição todas já estão liberadas (`:1065-1107,994-998,501-520`). Rodapé: "Cancelar" (1ª etapa) ou "Voltar"; "Salvar rascunho" (qualquer etapa, desabilitado sem destinatário);
"Próximo" (desabilitado na etapa 1 sem destinatário); na última etapa "Criar Orçamento" (novo) ou "Salvar Alterações" (editar), que exige destinatário **e** ao menos 1 item (`:1585-1627,982-992`).

| Etapa | Rótulo da etapa / cabeçalho | Campos e comportamento exatos | Código |
|---|---|---|---|
| 1 | "Destinatário" | Alternador "Cliente cadastrado" × "Novo prospecto". Cadastrado: campo "Cliente *" (placeholder "Selecione o cliente", lista de busca). Prospecto: "Nome *" (placeholder "Nome do prospecto"), "Telefone" ("(00) 00000-0000"), "E-mail" ("email@exemplo.com"). Só o nome (ou o cliente) é obrigatório | `:1113-1152` |
| 2 | "Serviços e mão de obra" → seção "Serviços e Mão de Obra", **precedida do bloco "Configurações BDI"** | Bloco BDI: selo "BDI NN.N%" (cor muda: vermelho/âmbar/neutro), campos "Imposto %", "Adm. Indireta %", "Lucro %", "Custo / km", e em "Condições de Pagamento": "Desconto à vista %" e "Parcelas (cartão)". **Valores iniciais vêm da aba Precificação** (3.10); aqui são só deste orçamento (não gravam de volta na Precificação). Seletor "Selecionar tipo de serviço..." (busca "Buscar ou criar serviço...", grupos "Recentes" = 5 mais usados em orçamentos anteriores e "Todos os serviços"), botão "+" (aria "Novo tipo de serviço": cria o tipo na hora e já adiciona), "Qtd:", botão "Adicionar". Vazio: "Nenhum serviço adicionado"; catálogo vazio: "Nenhum tipo de serviço cadastrado ainda" | `:1003-1040,1154-1209,959-962` |
| 2 (tabela) | Colunas "Serviço", "Qtd", "Custo unit." (tela larga), "Preço unit.", "Total", lixeira; rodapé "Subtotal Serviços" | Clicar no nome **expande**: "Mão de obra" (`R$/h × Nh = R$`), "Materiais", "Custos extras", "Custo total unit.". Campo "Descrição (opcional)" sob o nome (já vem preenchido com a descrição do tipo de serviço). Selo âmbar **"Sem custos configurados"** quando o custo unitário é 0. "Qtd" aqui é inteira (mín. 1). **Preço unit. é editável**: editar (ou mudar a Qtd) fixa o preço e para o recálculo automático | `:165-310,201-267,764-792` |
| 3 | "Materiais e deslocamento" → "Materiais" | Botão único **"Adicionar materiais"** abre o seletor em lote (abaixo). Lista: "Material", "Qtd" (aceita decimal e botões −/+), "Preço unit." (editável), "Total", "+ detalhe" (campo de descrição por linha), "Subtotal Materiais". Vazio: "Nenhum material adicionado" | `:1211-1423` |
| 3 | "Deslocamento" | Um campo de km (placeholder "0 km"); ao lado "= R$ X" (km × "Custo / km") | `:1426-1438` |
| 4 | "Desconto e condições" → "Desconto" | Seletor "R$" × "%" + valor; mostra "− R$ X" em vermelho. "%" incide sobre **itens + deslocamento** | `:1445-1473`, `:81-102` |
| 4 | "Brindes" | Caixa "Incluir brindes neste orçamento" (vem marcada) | `:1477-1489` |
| 4 | "Observações" / "Condições / Termos" | Dois campos de texto. Placeholders "Observações internas" e "Condições de pagamento, garantia, etc." **Mas as Observações saem impressas na proposta** (seção 5, P9) | `:1493-1503`, `components/quotes/templates/CleanTemplate.tsx` |
| 5 | "Validade e revisão" | "Válido até" (data, pode limpar), "Template da Proposta" (lista com bolinha de cor; novo orçamento nasce no **"Clean"**), "Nº de parcelas" ("À vista", "2x" … "12x"), "1º vencimento" (dica "Em branco, vence na data da aprovação."). Abaixo, avisos de BDI e o cartão **"Resumo do Orçamento"** (3.2.2). Sem itens: "Adicione ao menos um serviço ou material para finalizar." | `:1506-1578,462-486` |

**3.2.1 Regras de preço (o que o roteiro pode explicar):**

1. **BDI** = (100 − (Imposto + Adm. Indireta + Lucro)) ÷ 100, nunca abaixo de 0,01 (`hooks/useBDICalculator.ts:46-48`). Ex.: 6 + 12 + 22 → 0,60 (aparece "BDI 60.0%").
2. **Preço sugerido do serviço**, por ordem (`QuoteFormDialog.tsx:678-692`): (a) se o serviço tem **custos cadastrados** (mão de obra, materiais, custos extras, recursos, brindes: abas "Custos dos Serviços"/"Custos Globais"),
   preço = custo unitário ÷ BDI; (b) senão, se o tipo de serviço tem **preço padrão**, usa o preço padrão (e o trava como se tivesse sido digitado); (c) senão, 0 para digitar.
3. **Recálculo automático:** mudar Imposto/Adm./Lucro **reprecifica** os serviços cujo preço ainda não foi digitado/travado (`:605-618`). Digitar o preço, ou mudar a quantidade, trava a linha.
4. **Material do estoque** entra pelo **preço de venda** cadastrado (se não houver, o de custo) e **sem BDI**; o custo da linha é o preço de custo do estoque. Material avulso ("Criar "{nome}" como material avulso") usa o preço digitado nos dois (`:116-153`).
5. **Deslocamento** = km × "Custo / km", somado **a custo** (sem BDI) ao total (`useBDICalculator.ts:51`, `:81-102`).
6. **"Total do orçamento"** (o valor que o cliente vê e que a lista mostra em "Valor") = Σ preços das linhas + deslocamento − desconto, mínimo 0 (`QuoteFormDialog.tsx:81-102`, `lib/quote-commercial-total.ts:9-11`).
   Já **"Sugestão pelo BDI"** = (Σ custos das linhas + deslocamento) ÷ BDI: é só referência interna, **não** é o valor final (`useBDICalculator.ts:53-59`).
7. Gravado no orçamento: as taxas do BDI, `total_cost`, `total_price` (sugestão), `total_value` (comercial), desconto, condições (`QuoteFormDialog.tsx:811-874`).

**3.2.2 Cartão "Resumo do Orçamento"** (fundo escuro; `components/quotes/BDISummaryCard.tsx:26-119`, rótulos `crm.ts:1115-1128`): "BDI Calculado" (NN.N%), "Lucro Médio", "Custo Total", "+ Deslocamento" (se houver),
"Sugestão pelo BDI", **"Total do orçamento"** (verde, em destaque), "Opções de Pagamento": "À vista (N% desc.)" e "Nx cartão" (sobre o total do orçamento), e a nota "Custos e margem são referências internas".
Avisos acima do cartão: vermelho "O BDI está muito baixo ou negativo. O preço final não cobre os custos. Revise as taxas." (BDI < 5% **ou** sugestão < custo) e âmbar "BDI abaixo de 20% — margem de lucro muito apertada." (`QuoteFormDialog.tsx:601-603,1043-1062`).

**3.2.3 Seletor "Adicionar materiais"** (`components/inventory/MaterialBatchPicker.tsx`): janela com busca "Buscar por nome, código ou categoria..." (foco automático), grupos "Mais usados" (5 mais usados em orçamentos) e "Todos";
cada linha mostra nome, "SKU …" (ou a categoria) e "R$ X / unidade", com −/campo/+ para a quantidade; **não mostra saldo de estoque, de propósito** ("orçar não consome estoque", comentário em `:204-211`).
Rodapé: "N materiais" / "1 material", "Total: R$ X", botão "Adicionar ao orçamento". Se o texto digitado não bate com nenhum nome aparece a linha pontilhada **Criar "…" como material avulso** com "Preço unitário" (`:222-330,378`, `crm.ts:589-603`).

**3.2.4 Rascunhos — dois mecanismos diferentes:**

- **"Salvar rascunho"** grava de verdade no banco (status "Rascunho", sem exigir itens) e **fecha a janela**; toast (fixo) "Orçamento criado com sucesso!" também para rascunho (`QuoteFormDialog.tsx:896-916`, `hooks/useQuotes.ts:244`).
  **"Criar Orçamento" não define status**: nasce com o padrão do banco, também "Rascunho" (`QuoteFormDialog.tsx:877-891`, `supabase/migrations/20260308135145_03d237fb-65e5-410b-8098-2b2a567d12b7.sql:7`). O orçamento só vira "Enviado" quando o link é gerado (3.1, item 3).
- **Rascunho leve do navegador:** ao fechar a janela no meio do preenchimento (sem salvar), na próxima abertura de "Novo Orçamento" aparece "Rascunho encontrado" / "Existe um preenchimento interrompido deste formulário. Deseja retomar de onde parou ou começar do zero?" / "Começar do zero" · "Retomar rascunho".
  Guarda destinatário, BDI, desconto, termos etc., **não os itens** (`QuoteFormDialog.tsx:406-445,1646-1660`, `components/ui/DraftResumeDialog.tsx:24,58-70`). **Cuidado de gravação:** um ensaio interrompido deixa esse aviso na próxima tomada (limpar o armazenamento da sessão do navegador entre tomadas).
- **Pegadinha:** "Salvar rascunho" num orçamento que está sendo **editado** envia status "Rascunho": um Enviado/Aprovado editado e salvo por esse botão **volta a Rascunho** (`QuoteFormDialog.tsx:899-904`) `[handoff]`.
- Fechar a janela com "Cancelar" ou X não pergunta nada.

### 3.3 Janela "Proposta #N" (Visualizar) — `components/quotes/QuoteViewDialog.tsx`

- Janela larga (até 56 rem) com o título "Proposta #N" (`crm.ts:519`, `QuoteViewDialog.tsx:131,159-170`). **Não tem botões "Aprovar", "Editar" ou "Gerar link"**: só leitura + até três botões.
- Primeira linha (olho): "Não visualizada pelo cliente ainda" ou "Visualizada N× · última vez dd/MM HH:mm (há X)" (`:76-93`, `crm.ts:520-522`).
- Botões à direita: **"Gerar cobrança"** (só com módulo Cobranças + conta ativa + cliente cadastrado), **"WhatsApp"**, **"PDF"** (`:95-112`, `crm.ts:523-524`).
  - "WhatsApp" abre `https://wa.me/?text=…` **em outra aba**, com o texto "Olá! Segue a proposta #N no valor de R$ X.\n\nAcesse: <endereço do app>/proposta/<token>" (`:66-74`, `crm.ts:527`). O endereço é o da página aberta (`window.location.origin`), sem o apelido do cliente no link.
    **Não muda o status para Enviado** (diferente do "Gerar link da proposta") `[handoff]`.
  - "PDF" gera e **baixa** um arquivo "Proposta - <Cliente> DD MÊS AAAA.pdf" (largura A4 de 794 px); com erro: toast "Não foi possível gerar o PDF. Tente novamente." (`:53-64`, `utils/proposalPdf.ts:4,68-87`, `crm.ts:525`).
    **O gravador não captura downloads nem nova aba (TRILHA 5-8)**: mostrar só o botão.
- Corpo: a própria proposta desenhada com o modelo escolhido no orçamento (`proposal_templates.slug`; sem modelo cai em "classico") e os dados da empresa, em largura fixa de PDF, com rolagem horizontal se a janela for estreita (`:51,114-127`).
  Detalhe do desenho e do que cada modelo mostra: 3.11.

### 3.4 Janela "Aprovar Orçamento #N" — `components/financial/ApproveQuoteModal.tsx` (rótulos `lib/i18n/messages/app/finance.ts:1405-1454`)

Abre pelo item "Aprovar orçamento" (a partir de Rascunho **ou** Enviado). Título "Aprovar Orçamento #N", subtítulo "Valor: R$ X" (= total do orçamento). **O modo que abre marcado vem da empresa**
(Configurações > Usabilidade > "Ao aprovar um orçamento", padrão do banco "Vou receber depois") e dá para trocar na hora (`pages/Quotes.tsx:908-922`, `ApproveQuoteModal.tsx:156-192`).
Dois botões em pílula: **"Já recebi"** e **"Vou receber depois"**, com a dica embaixo (`:284-308`).

| | Modo "Já recebi" | Modo "Vou receber depois" |
|---|---|---|
| Dica | "Lança como receita recebida e já entra no saldo da conta escolhida." | "Gera conta a receber pendente. O saldo da conta só muda quando você der a baixa." |
| Campos | "Forma de pagamento *" (Dinheiro · PIX · Cartão de Débito · Cartão de Crédito · Boleto · Transferência · Cheque; abre em PIX), "Data do recebimento *" (hoje), "Caixa / Conta bancária *" (busca "Buscar conta...", "+" cria conta se tem permissão; sem conta: "Cadastre um caixa ou conta primeiro."), "Tarifa de máquina/gateway" (placeholder "0,00"; dica "Será lançada como despesa em "Tarifas e Taxas" (deduzida da receita líquida no DRE)."), centro de custo (só se a empresa usa), "Observação" | "Parcelas" ("À vista", "2x" … "12x"; vem do orçamento), "Primeiro vencimento *" (hoje, ou o do orçamento; dica "As parcelas seguintes caem no mesmo dia dos próximos meses."), "Conta prevista do recebimento" ("Decidir na hora da baixa"; dica "É só uma previsão: enquanto a parcela estiver pendente, ela não mexe no saldo da conta."), centro de custo, "Observação"; lista **"Parcelas que serão criadas"** ("Parcela 1/3 · dd/mm/aaaa … Total") e a nota "A tarifa do recebimento você informa na hora de dar a baixa de cada parcela." |
| Botão de confirmar | "Aprovar e lançar receita" (precisa de conta e tarifa válida) | "Aprovar e gerar conta a receber" (precisa de 1º vencimento) |
| Toast | "Orçamento aprovado!" / "Receita lançada no financeiro." | "Orçamento aprovado!" / "Conta a receber criada. Dê a baixa quando o dinheiro entrar." ou "N parcelas criadas em Contas a Receber. Dê a baixa conforme o dinheiro entrar." |
| O que grava | **1 entrada paga** "Orçamento #N" (categoria de receita de serviço da empresa, conta, forma, data) + **1 saída** "Tarifa do recebimento — Orçamento #N" se houve tarifa; status vira "Aprovado" | **N entradas pendentes** "Orçamento #N" (ou "Orçamento #N (1/3)"…), com vencimentos mensais; status "Aprovado" |

- Código das duas colunas: `ApproveQuoteModal.tsx:311-405` (já recebi), `:408-499` (receber depois), `:255-269` (rodapé "Cancelar" + botão verde; "Aprovando..." enquanto grava). Formas de pagamento: `finance.ts:1486-1494`.
- Com tarifa: cartão "Valor bruto recebido / Tarifa / Líquido na conta". Tarifa absurda: aviso âmbar "A tarifa (R$ X) é alta perto do valor da venda (R$ Y). Confira antes de confirmar." ou bloqueio "A tarifa (R$ X) é maior que o valor da venda (R$ Y). Confira o valor digitado."
- **Em nenhum dos modos a aprovação gera custo** (material ou mão de obra): "o custo do orçamento é demonstrativo" (regra de produto, `hooks/useQuoteConversion.ts:205-220,323-348`). A trilha de 1.22.5 dizia "lança receita + custo + MO e trava": **desatualizada** (seção 0.2).
- Código da gravação: `hooks/useQuoteConversion.ts:221-370`, linhas montadas em `:43-160`. Depois de aprovado a linha ganha o selo "No financeiro" e passa a ter "Ver lançamento no financeiro" e "Desfazer lançamento" (3.1/3.6).
- Texto morto: o i18n ainda tem `approveDesc` "Como o cliente pagou? Vamos lançar a receita e os custos no financeiro." (`crm.ts:510-511`), **não usado** pela janela atual `[handoff]`.
- **Aprovação pelo cliente no link** é outro caminho (3.11): por padrão **não** cria lançamento (opção da empresa "Aprovação pelo link da proposta já gera conta a receber", desligada).

### 3.5 Janela "Distribuir serviços · Orçamento #N" e o botão "Gerar OS" — `components/quotes/QuoteServiceDistributionDialog.tsx`

**Todos os textos desta janela são fixos no código (sem i18n)** `[handoff]`. Abre pelo item "Gerar OS" (orçamento Aprovado, sem OS ligada, com `fn:create_os`).

- Título "Distribuir serviços · Orçamento #N"; texto "Defina em qual equipamento cada serviço será executado. Os checklists vinculados serão aplicados automaticamente." (`:82-83`).
- Para **cada serviço** do orçamento (por tipo de serviço, sem repetir): bolinha na cor do serviço + nome + selo "N equipamento(s)"; botão "Todos"/"Limpar" (só com 2+ equipamentos); um cartão por equipamento **do cliente** com caixa de seleção, nome e "marca · modelo · identificador" (ou "Sem detalhes") (`:104-151`).
- Trava: se o cliente tem equipamentos, **cada serviço precisa de ao menos 1 equipamento** (erro "Selecione ao menos um equipamento para este serviço.") e o botão "Gerar OS" fica desabilitado até completar (`:47-49,152-154`).
- Avisos: sem cliente cadastrado → "Este orçamento não tem cliente cadastrado. A OS será gerada sem equipamentos."; cliente sem equipamento → "O cliente não possui equipamentos cadastrados. Você poderá adicioná-los depois na OS."; sem tipos de serviço → "O orçamento não possui tipos de serviço vinculados. A OS será gerada com os itens e valores, sem distribuição." (`:88-102`).
- Rodapé: "Cancelar" e "Gerar OS" (vira "Gerando...") (`:63-76`). Sucesso: toast fixo "OS gerada com sucesso!" / "Serviços, equipamentos, checklists, materiais e valores foram copiados." (`hooks/useQuoteConversion.ts:177-203`). Erro: "Não foi possível gerar a OS" + a mensagem do servidor.
- **O que a função do servidor `generate_service_order_from_quote` faz** (`supabase/migrations/20261019041000_protecao_escopo_e_distribuicao_orcamento.sql:198-352`, valor trocado em `20261027120000_orcamento_total_comercial_na_conversao_os.sql:8-30`):
  exige quem tem `fn:create_os` e orçamento **Aprovado**; cria **1 OS** com status **"agendada"** (sem data nem técnico), valor = **total do orçamento** (`total_value`), descrição "Gerada do Orçamento #N", observações do orçamento;
  copia as linhas do orçamento para o orçamento da OS (`service_order_budget_items`); liga os tipos de serviço e a **distribuição por equipamento**; aplica o checklist ativo ligado a cada serviço daquele equipamento;
  marca o orçamento como **"Convertido"** e liga a OS (`converted_to_os_id`). **Idempotente** (repetir devolve a mesma OS). **Não mexe em estoque nem em financeiro.**
- **Depois de gerar**, a linha vira "Convertido": somem "Gerar OS" e "Aprovar"; a % do cartão "Conversão" **cai** (3.1). Não existe "desfazer Gerar OS".

### 3.6 Janela "Desfazer o lançamento?" — `pages/Quotes.tsx:942-997`

- Título "Desfazer o lançamento?"; texto "Os lançamentos financeiros criados na aprovação do orçamento Nº N serão excluídos, e o orçamento volta para "Enviado" para você aprovar de novo." (`crm.ts:481-482`).
- Carrega a prévia ("Conferindo os lançamentos...") e lista cada lançamento (descrição, categoria, `+/−` valor) sob "1 lançamento será excluído:" ou "N lançamentos serão excluídos:". Se o lançamento não existe mais: aviso âmbar "Não encontramos mais esse lançamento no financeiro. Ao confirmar, o orçamento volta para "Enviado" mesmo assim." (`crm.ts:483-486`).
- Botões "Cancelar" e "Excluir lançamentos" (vira "Excluindo...") (`pages/Quotes.tsx:988-995`). Sucesso: "Lançamento desfeito" / "O orçamento Nº N voltou para Enviado. Agora dá para aprovar de novo." (`crm.ts:490-491`). Erro: "Não foi possível desfazer o lançamento" + mensagem (`crm.ts:492`).
- Apaga **a receita, a tarifa e todas as parcelas do mesmo parcelamento, pagas ou não**, e devolve o orçamento a "Enviado" (`hooks/useRelatedTransactions.ts:9-70,127-188`) `[handoff]`.
  Se o orçamento já virou "Convertido" (OS gerada), o desfazer o devolve a "Enviado" **mantendo a OS ligada**; a linha fica sem "Gerar OS" (exige Aprovado) `[handoff]`.

### 3.7 Janela "Configurar Proposta" (3 etapas) — `components/quotes/ProposalConfigDialog.tsx` (rótulos `crm.ts:652-746`)

Abre pelo botão "Configurar Proposta" do topo da lista. Janela larga (`sm:max-w-4xl`), não fecha ao clicar fora, mesmo molde do wizard de orçamento (barra + bolinhas; as 3 etapas já liberadas desde a abertura) (`:132-135,239-263,781-792`).
Rodapé: "Cancelar" (1ª etapa) / "Voltar", "Próximo", e na última etapa "Salvar" ("Salvando…"). Na Revisão, no centro do rodapé, setas ◀ "Página X/Y" ▶ para folhear a prévia (`:724-779`).
**Salvar grava na empresa** (`company_settings.proposal_customization`), vale para **todas** as propostas, toast "Configuração da proposta salva", e **a janela continua aberta** (não fecha sozinha) `[handoff]` (`:270-275`).

| Etapa | Cabeçalho | Campos e comportamento | Código |
|---|---|---|---|
| 1 "Modelo" | "Modelo da proposta" — "Escolha o estilo visual da proposta enviada ao cliente." | Lista rolante com os 4 modelos **Clean** (padrão), **Vanguarda**, **Aurora**, **Prisma** (ícone + nome) e, ao lado, a **capa A4** do modelo marcado, com os dados da empresa (nome, logo) e um exemplo fixo ("Maria Silva", proposta #1042). **Escolher o modelo aqui só muda a prévia: não é gravado** (o modelo de cada proposta é escolhido na etapa 5 do orçamento) `[handoff]` | `:408-459,100-126,141,270-275` |
| 2 "Personalização" | "Personalização" | **"Logo da proposta"** ("Opcional. Se vazio, a proposta usa o logo da empresa."): "Enviar logo"/"Trocar logo" (escolhe imagem de até 5 MB: erros "Arquivo muito grande (máx 5MB)", "Apenas imagens são permitidas"), "Remover (usar logo da empresa)"; **o envio já grava na hora**, sem esperar o "Salvar" (toast "Logo da proposta atualizado" / "Logo da proposta removido" / "Erro ao enviar logo"), bucket `company-logos`. "Tamanho do logo" (controle deslizante de 50% a 200%, passo 10, "Ajusta o tamanho do logo na proposta, mantendo a proporção.") | `:469-530,277-335` |
| 2 | "Personalizar Cores" | "Cor Primária" (padrão `#2563eb`), "Cor de Destaque" (`#f97316`), "Fundo do Cabeçalho" (`#1e3a5f`) | `:533-558,161-169` |
| 2 | Três chaves Sim/Não | "Mostrar paginação?" ("Exibe "Página XX/YY" no canto inferior de cada página da proposta."), "Mostrar deslocamento" ("Exibe o valor de deslocamento no resumo de investimento da proposta."), "Mostrar brindes" ("Exibe a seção de brindes (cortesias) quando a proposta os inclui."). Os três abrem em **Sim** | `:563-614`, `crm.ts:695-700` |
| 2 | "Seções da proposta" — "Ligue, desligue e reordene as seções. O texto vira o padrão de todos os orçamentos, quando o orçamento não tiver o seu próprio." | 7 seções, nesta ordem: "Mensagem de abertura", "Formas de pagamento", "Informações adicionais", "Observações", "Sobre a empresa", "Garantia", "Mensagem de encerramento". Cada uma tem setas ▲▼ para mover e uma chave para ligar/desligar; ligada e com texto, mostra a caixa de texto com a dica "Ex: …" (a de "Formas de pagamento" não tem texto: é calculada). **Ligar/desligar e reordenar só vale no modelo Clean**; o texto de "Sobre a empresa" vale nos 4 modelos | `:617-689`, `components/quotes/templates/types.ts:3-102` |
| 3 "Revisão" | "Revisão" — "Veja como a proposta vai chegar ao cliente. Confirme em "Salvar"." | Prévia **A4 de várias folhas** do exemplo fixo com as cores, logo e seções escolhidas; folhear pelas setas do rodapé | `:693-717` |

- Os textos `sectionEnabled`, `sectionDisabled`, `sectionDragHandle` e `sectionPagamentoHint` existem no i18n mas **nenhuma tela os usa** (não aparecem) (`crm.ts:710-712,728`) `[handoff]`.
- A prévia **não é o orçamento real**: usa um orçamento de exemplo fixo (`ProposalConfigDialog.tsx:36-97`); o modo de ver o orçamento de verdade é "Visualizar" (3.3) ou a página pública (3.11).
- O modelo "Clean" é o padrão de novos orçamentos; só o Clean tem as seções reordenáveis; Aurora, Prisma e Vanguarda têm capa própria (`types.ts:3-12`, `ProposalConfigDialog.tsx:98-111`).
- O padrão de "Mostrar paginação?" aqui é **Sim**, mas o comentário do tipo diz "Default: desligado" (`templates/types.ts:57-58` × `ProposalConfigDialog.tsx:165,182`) `[handoff]`.

### 3.8 Aba "Custos dos Serviços" — `components/service-orders/ServiceCostsTab.tsx` (rótulos `crm.ts:749-792`, `os.ts:1292-1309`, `crm.ts:918-1115`)

**Sem trava de plano nem de permissão** (seção 2). Cabeçalho "Custos por Tipo de Serviço" / "Defina mão de obra e materiais para precificação automática." e o seletor **"Tipo de serviço"** ("Selecione o tipo de serviço", bolinha de cor). **O primeiro tipo da lista já abre selecionado** (`ServiceCostsTab.tsx:41-46,215-231`).
Sem tipo: "Selecione um tipo de serviço para configurar custos." Quatro sub-abas sublinhadas: **"Mão de obra"**, **"Recursos"**, **"Materiais"**, **"Resumo"** (`:238-272`). Os custos de um serviço alimentam o preço sugerido quando ele entra num orçamento (3.2.1).

| Sub-aba | O que a tela mostra (rótulos exatos) | Código |
|---|---|---|
| "Mão de obra" | Cartão **"Mão de obra"** com botão **"Calcular"**, campos "Custo / hora (R$)" e "Horas" (começa em 1) e a caixa "Custo HH" (= custo/hora × horas). Cartão **"Custos extras"** com botão "+ Adicionar" (abre "Adicionar Custo Extra": "Tipo" [Veículo, Ferramentas, EPI, Combustível, Equipamentos, Outro], "Descrição" "Descreva o custo", "Valor" "0,00", "Cancelar", "Adicionar"), linhas editáveis "Descrição" / "Valor (R$)" com "×", vazio "Nenhum custo extra." e a soma "Total extras". Cartão "Observações" ("Observações internas do custo") e botão "Salvar" com o aviso verde "Salvo automaticamente" | `:274-361`, `components/service-orders/ExtraCostModal.tsx:28`, `crm.ts:918-1115` |
| "Recursos" | "Recursos Vinculados" — "Selecione recursos globais para este serviço. Custo = custo/hora × Nh" (N = as horas da aba "Mão de obra"). Grupos "Veículos", "Ferramentas", "EPIs", "Outros": caixa de seleção por recurso, com "Sobrescrever:" (placeholder "Auto") para trocar o custo calculado por um valor fixo; grupo **"Brindes"** (selo "por execução"); rodapé "Total recursos vinculados" | `:363-369`, `components/service-orders/LinkedResourcesSection.tsx:108-113,193,228,293` |
| "Materiais" | "Materiais do serviço" — "Vincule materiais do estoque ou cadastre manualmente."; campos "Item do estoque (opcional)" ("Selecione do estoque"), "Nome manual" ("Ex: Tubo de cobre"), "Quantidade", "Custo unit. (R$)", botão "Adicionar"; tabela "Material · Qtd. · Custo unit. · Subtotal" e o "Total". Vazio: "Nenhum material vinculado." Item do estoque entra pelo **preço de custo** do estoque | `:371-373`, `ServiceMaterialsList.tsx:83-95,121-185`, `os.ts:1292-1309` |
| "Resumo" | "Resumo e preço sugerido (BDI)": caixas "Mão de obra", "Materiais", "Recursos", "Extras manuais"; simulação "Imposto (%)", "Adm. indireta (%)", "Lucro (%)" **partindo dos valores da Precificação**; dica "Simulação. Não altera suas configurações de precificação."; botão "Restaurar padrão" (aparece depois de mexer); cartão com "Custo total", **"Preço sugerido (BDI)"** e a linha "BDI: 0.6000 | Lucro padrão: 22.00%" | `:375-454`, `crm.ts:777-791` |

- **Salvamento:** a aba "Mão de obra" **salva sozinha 1 s depois de qualquer mudança** (mão de obra, horas, extras, observações) e mostra "Salvo automaticamente" por 2 s; o botão "Salvar" salva na hora. Vínculos da aba "Recursos" e "Materiais" gravam a cada clique/adição (`ServiceCostsTab.tsx:161-176,207-211`, `hooks/useServiceCosts.ts`).
- **"Calcular"** abre **"Calcular Custo de Mão de Obra"** (selo "Calculadora de equipe"): "Horas mensais base" (padrão 176 h = 22 d × 8 h), "Horas padrão neste serviço", lista "Funcionários (N)" com "Adicionar" (campo "Nome ou selecione..." + busca "Buscar funcionário..." que **lista os funcionários ativos com o custo mensal de cada um**),
  por pessoa "Custo mensal", "Horas neste serviço", opção "Valor fixo por serviço (não é mensalista)", e o botão "Calcular custo mensal detalhado" (abre "Calcular Custo Mensal": salário base, periculosidade/insalubridade, leis sociais, benefícios, custos anuais ÷ 12, regime tributário, INSS patronal, "Custo Total Mensal", "Hora Homem (HH)").
  Resumo: "Horas do serviço", "Custos fixos incluídos", "Custo HH total", "Custo/hora médio"; botões "Cancelar" e **"Aplicar R$ X/h"**, que preenche "Custo / hora" e "Horas" da aba (`LaborCalculatorModal.tsx:56-135,243-264,440-452`, `crm.ts:994-1074`).
  **Aplicar o custo mensal numa pessoa cadastrada grava o custo no cadastro do funcionário** (`employees.monthly_cost` e o detalhamento) (`LaborCalculatorModal.tsx:465-479`).
- O que o orçamento lê: `service_costs` (custo/hora × horas + extras), `service_materials.subtotal`, recursos vinculados (custo/hora do recurso × horas, ou o valor "Sobrescrever") e brindes (`QuoteFormDialog.tsx:635-672`).

### 3.9 Aba "Custos Globais" (título na tela: "Centro de Custos") — `components/service-orders/GlobalCostsTab.tsx` (rótulos `crm.ts:795-865`, `crm.ts:918-998`)

**Atenção ao nome:** a aba do topo chama "Custos Globais", mas o título dentro da página é **"Centro de Custos"** (`crm.ts:411,796`, `GlobalCostsTab.tsx:357`). Sem trava de plano.

| Elemento | Rótulo exato e comportamento | Código |
|---|---|---|
| Cabeçalho | "Centro de Custos" / "Cadastre veículos, ferramentas e recursos. O custo/hora é rateado automaticamente." + botão **"Novo Recurso"** (abre "Qual recurso deseja cadastrar?" / "Escolha a categoria para abrir o cadastro com os cálculos corretos." com Veículos · Ferramentas · Brindes · EPIs · Outros) | `:355-363,410-420`, `crm.ts:796-798,822-823` |
| Faixa de totais | "Custo/hora Veículos", "Custo/hora Ferramentas", "Custo/hora EPIs" (cada um "R$ X/h") e "Custo/Brinde" | `:365-375`, `crm.ts:830-833` |
| Lista | "Recursos de custo", busca "Buscar recurso...", filtros "Categoria" e "Status" ("Ativo"/"Inativo"), ordenação "Nome: A a Z", "Nome: Z a A", "Custo: maior primeiro", "Custo: menor primeiro"; cada linha mostra o nome, selo "Ativo"/"Inativo" e o custo "/mês" (brinde: "/un"). Vazio: "Nenhum recurso cadastrado." / "Nenhum recurso corresponde aos filtros." | `:130-175,392-398`, `crm.ts:799-808` |
| Detalhe (ao clicar) | "Selecione um recurso" (nada marcado) / "Voltar para a lista"; "Custo mensal" (brinde: "Custo por unidade"), "Horas mensais", "Custo por hora"; "Composição do custo" (cada componente, com "Valor anual" quando for anual), "Nenhum item compõe este custo."; "Observações" ("Nenhuma observação cadastrada."); botões "Editar" e "Excluir" | `:262-350`, `crm.ts:808-821` |
| Excluir | "Excluir recurso?" ("Esta ação removerá "{nome}" e todos os seus componentes de custo.") ou "Excluir brinde?"; "Cancelar" · "Excluir" | `:446-458`, `crm.ts:858-865` |

**Janela de cadastro** ("Novo Veículo" · "Nova Ferramenta" · "Novo Brinde"… / "Editar …"; `components/service-orders/CostResourceFormSheet.tsx`, rótulos `crm.ts:936-992`):
"Nome do veículo" (placeholder por categoria, ex. "Spin 2024"), "Foto (opcional)" + "Adicionar foto" (envio de imagem para o bucket `equipment-files`, `:239-250`), "Horas de uso mensal (para rateio)" (dica "Padrão: 176h (22 dias × 8h)"), chave "Recurso ativo".
**Só veículo** tem a "Calculadora de Depreciação" ("Fórmula: (Valor 0km − Valor após 2 anos) ÷ 24 meses", campos "Valor 0km" e "Valor após 2 anos", resultado "Depreciação mensal:", botão "Aplicar ao campo de depreciação") (`:337-395`).
"Componentes de Custo" já vêm com linhas por categoria: veículo "Depreciação mensal", "Manutenção + Combustível", "Seguro" (anual), "Documentação / IPVA" (anual); ferramenta "Depreciação mensal", "Manutenção mensal"; EPI "Custo mensal do kit"; outro "Custo mensal"; brinde "Cartão de visita" (com "Custo total", "Unidades no lote", "Quantidade por brinde") (`:62-90`).
Cada componente tem a chave "Valor anual (÷12)". Cartão "Resumo": "Total mensal:", "Horas mensais:", "Custo/hora:" (brinde: "Itens no brinde:", "Custo total por brinde:"). Botão "Salvar" ("Salvando...").
**Custo/hora do recurso = soma dos componentes mensais ÷ horas mensais** (view `cost_resources_with_rate`, seção 4).

### 3.10 Aba "Precificação" — `components/pricing/` (rótulos `crm.ts:868-914`)

Cabeçalho "Precificação" / "Taxas padrão aplicadas em todos os orçamentos via método BDI". Duas colunas: formulário à esquerda, simulador à direita (`PricingTab.tsx:6-26`).

| Bloco | Rótulos exatos | Código |
|---|---|---|
| Cartão azul | "Método BDI" — "O preço final é calculado dividindo o custo real pelo BDI, garantindo que impostos e overhead nunca sejam subprecificados." e a caixa "Preço = Custo Total ÷ BDI" | `PricingConfigForm.tsx:66-79` |
| "Taxas do BDI" | Número grande **"BDI atual"** = fator com 4 casas ("0.6000"); campos "Imposto (%)", "Adm. Indireta (%)", "Lucro Padrão (%)"; barra colorida de composição com legenda "Imposto 6%", "Adm. 12%", "Lucro 22%", "BDI 60.0%"; botão "Salvar" | `PricingConfigForm.tsx:82-146` |
| "Deslocamento e Pagamento" | "Custo por KM (R$)", "Desconto à vista (%)", "Parcelas (cartão)"; **outro** botão "Salvar" | `PricingConfigForm.tsx:155-190` |
| "Simulador de Preço" (selo "Tempo real") | "Teste qualquer custo para ver o preço final calculado pelo BDI."; campos "Custo do serviço" (abre em 1.000) e "Distância (KM)"; quatro cartões "Deslocamento" (`N km × R$ X/km`), "Custo Total" ("Serviço + deslocamento"), "BDI" (`60.00%`, "Coeficiente 0.6000"), "Lucro Esperado" (`22%`, "≈ R$ X"); destaque **"Preço Final (BDI)"** com selo "BDI 0.6000"; "À vista (N% desc.)", "Cartão (Nx sem juros)" e a linha "Preço = R$ X ÷ 0.6000 = R$ Y" | `BDIPreviewCard.tsx:23,61-188` |

- Toast ao salvar (fixo no código): "Configurações de precificação salvas!" (`hooks/usePricingSettings.ts:64`). Os **dois botões "Salvar" gravam as seis taxas de uma vez** (o de baixo não é "só deslocamento") (`PricingConfigForm.tsx:137-145,175-185`) `[handoff]`. Salvar usa os valores digitados nos campos.
- **O simulador usa os valores SALVOS** (não os digitados ainda): mexer nos campos sem salvar não o muda (`BDIPreviewCard.tsx:28-34`).
- Os mesmos seis números abastecem o bloco "Configurações BDI" de todo **novo** orçamento (3.2) e a simulação do "Resumo" de cada serviço (3.8). Alterar aqui **não reprecifica orçamentos já criados**.
- **Padrão de uma empresa nova é tudo 0** (e "Parcelas (cartão)" 0): ao abrir qualquer tela que lê as taxas, o app **cria a linha da empresa só com o padrão do banco, que é 0** (`hooks/usePricingSettings.ts:37-46`, `supabase/migrations/20260425000000_drift_missing_tables.sql:29-39`); os "10/12/10/1/6/10" do código só valem para linha inexistente e nunca aparecem (`PricingConfigForm.tsx:24-29`).
  Resultado: sem salvar, **BDI = 1,0000 e "Preço sugerido" = custo**. O Guia Técnico fala em "padrão 10/12/10" (seção 0.4) `[handoff]`.

### 3.11 Página pública da proposta (o que o cliente vê) — `pages/ProposalPublic.tsx`, `components/quotes/ProposalRenderer.tsx`, `templates/CleanTemplate.tsx` (rótulos `crm.ts:652-670`, `crm.ts:1133-1236`)

- **Endereço:** `https://dominex.app/proposta/<apelido-do-destinatário>-<token de 64 caracteres>` (o apelido é só enfeite; vale também só o token). **Abre sem login.** `?preview=1` = "olhada do dono": não conta como visualização (`utils/shareLinks.ts:62-67`, `pages/ProposalPublic.tsx:396-402`).
- **Carregamento:** círculo girando; token inválido: ícone de documento + "Proposta não encontrada." Os dados vêm da função `get_quote_public_payload` (orçamento, itens, cliente, empresa com logo/cores/idioma) (`:131-179,271-286`).
- **Visualização:** a cada abertura (menos `?preview=1`) o app chama `record_quote_view`; **o mesmo navegador não conta de novo em 30 minutos**; atualiza "visto há X" e o número na lista (`:181-195`, `supabase/migrations/20260624120000_quote_view_tracking.sql:58-133`).
- **O que aparece na página:** a proposta no modelo do orçamento (3.11.1); botão escuro flutuante **"Baixar PDF"** no canto inferior direito (dica "Baixa a proposta pronta em PDF.", falha: alerta do navegador "Não foi possível gerar o PDF. Tente novamente."); botão verde **"Pagar"** só se existir cobrança ligada ao orçamento (abre `/pagar/<código>` em outra aba);
  e, **só quando o orçamento está "Enviado"**, os botões **"Aprovar"** (verde) e **"Rejeitar"** (vermelho) (`:288-290,296-368`). Em "Rascunho" a página abre **sem esses botões**: é por isso que "Gerar link da proposta" precisa mudar o status para Enviado.
- **Respostas:** depois de clicar: "✅ Proposta aprovada! Obrigado." ou "❌ Proposta rejeitada."; ao reabrir um orçamento já respondido: "Esta proposta foi aprovada." / "Esta proposta foi rejeitada."; resposta de outro aparelho no meio: "Esta proposta já foi respondida."; sem internet: "Não foi possível registrar sua resposta. Verifique sua conexão e tente novamente." e os botões continuam ativos (`:216-256,369-390`, `crm.ts:658-669`).
  **Não há confirmação antes de aprovar/rejeitar** nem como o cliente desfazer `[handoff]`.
- **O que a resposta do cliente muda na empresa:** a função `respond_quote_public` só atua em orçamento "Enviado" (senão devolve "não pendente"); muda para "Aprovado"/"Rejeitado"; **só cria conta a receber se a opção "Aprovação pelo link da proposta já gera conta a receber" estiver ligada** (padrão desligada; usa as parcelas e o 1º vencimento da etapa 5 do orçamento)
  (`supabase/migrations/20260919230000_aprovacao_publica_usa_categoria_renomeada.sql:161-337`, `20260911200000_orcamento_recebivel_parcelado_e_aprovacao_publica.sql`).
  Com a opção desligada o orçamento fica "Aprovado" **sem** "No financeiro" e **sem** o item "Aprovar orçamento" no menu (que só existe para Rascunho/Enviado): para lançar a receita sobra o "Gerar cobrança" ou o lançamento manual `[handoff]`.
- **Aviso no app:** a função `notify-quote-response` grava uma notificação para os **admins ativos** da empresa (sino): título "Orçamento aprovado"/"Orçamento recusado" e texto "<cliente> aprovou/recusou o orçamento #N no valor de R$ X." (se o destinatário era cliente cadastrado, o texto diz "O cliente"). O link da notificação `/orcamentos?quote=<id>&r=<status>` **não é lido por nenhuma tela** (cai na lista, sem destaque) (`supabase/functions/notify-quote-response/index.ts:95-192`) `[handoff]`.

**3.11.1 Modelo "Clean" (padrão), de cima para baixo** (`CleanTemplate.tsx:236-430`; rótulos `crm.ts:1203-1235`):
cabeçalho com logo/nome/CNPJ/telefone/e-mail/endereço da empresa e, à direita, **"Orçamento"** + `#N` + selo "Proposta válida até dd/mm/aaaa" (se houver validade) → bloco **"Cliente"** (nome, documento, endereço, telefone, e-mail) → "Mensagem de abertura" (se ligada e com texto) →
tabelas **"Serviços"** e **"Produtos e materiais"** (colunas "Item", "Valor unitário", "Quantidade", "Subtotal"; vazio "Nenhum item adicionado.") → totais "Total dos serviços", "Total de materiais", "Subtotal", "Deslocamento (N km)", "Descontos" (− R$), **"Total"** →
**"Formas de pagamento"**: "À vista no PIX" com "N% de desconto" e o valor, e "Parcelado no cartão" com "Em até Nx de R$ …" e "Total parcelado" → seções de texto na ordem configurada: "Informações adicionais" (= **"Condições / Termos"** do orçamento), "Observações" (= **"Observações"** do orçamento), "Sobre a empresa", "Garantia", mensagem de encerramento (se ligadas e com texto; texto do orçamento vence o texto padrão da empresa) →
rodapé "Proposta preparada por <empresa>" + "Documento gerado em dd/mm/aaaa às hh:mm" (`templates/shared.ts:203-213`).
**O Clean não tem seção de brindes** (a caixa "Incluir brindes neste orçamento" não muda nada nele, embora o custo do brinde entre no preço do serviço); Vanguarda/Aurora/Prisma mostram "Brindes inclusos" / "Esta proposta acompanha brindes de cortesia, sem custo adicional." (`crm.ts:1184-1185`) `[handoff]`.
A hora "Documento gerado em…" vem do relógio do navegador: **travar o relógio na gravação** (TRILHA 5).

### 3.12 Opções da empresa que mudam o comportamento do orçamento — Configurações > Usabilidade > "Orçamento, OS e financeiro" (detalhe no inventário do T1)

| Opção | Rótulo exato | Efeito neste tutorial | Código |
|---|---|---|---|
| Alternador | **"Ao aprovar um orçamento"** — "Define o que já vem marcado no modal de aprovação. Dá pra trocar em cada orçamento." — "Já recebi" × "Vou receber depois" | Muda o que abre marcado em "Aprovar Orçamento #N" (3.4). Vem em **"Vou receber depois"** | `pages/Settings.tsx:1722-1750`, `settings.ts:264-271`, `supabase/migrations/20260911200000_orcamento_recebivel_parcelado_e_aprovacao_publica.sql:33-55` |
| Chave | **"Aprovação pelo link da proposta já gera conta a receber"** — "Desligado, aprovar pelo link só muda o status do orçamento, nada entra no financeiro. Ligado, a conta a receber é criada automaticamente." | Define se a resposta do cliente no link cria lançamento (3.11). Vem **desligada** | `pages/Settings.tsx:1751-1775`, `settings.ts:273-274` |

- Quem muda: quem pode salvar Configurações (`pages/Settings.tsx:1738,1761`). O cartão também tem "Perguntar sobre receita ao finalizar OS" (fora desta aula).
- Outras opções que o orçamento lê: dados da empresa (nome, logo, CNPJ, endereço, e-mail, telefone) e `proposal_customization` (3.7) em `company_settings`; moeda/idioma/fuso da empresa (`ProposalPublic.tsx:171-176`).

---

## 4. Backend por tela e comparação com o fakebase

> Banco = Supabase (Postgres). Quase toda tabela abaixo é "da empresa" (`company_id`) e protegida por RLS; em `quotes` a regra é `Users manage own company quotes`
> (todo usuário logado da empresa, **sem checagem de papel**) (`supabase/migrations/20260418163700_9165358e-c67c-420d-b74f-be9aeac54c1e.sql:207`).

### 4.1 O que cada tela lê e grava

| Tela / ação | Lê | Grava | Função do banco · borda · bucket · host externo | Código |
|---|---|---|---|---|
| Lista "Orçamentos" (3.1) | `quotes` com os embutidos `customers(nome, e-mail, telefone, celular, documento, endereço…)`, `quote_items(*)`, `proposal_templates(slug, name)`, do mais novo ao mais antigo; `tenant_charges` (selo "Cobrança gerada"); `company_settings` (modo de aprovação) | Nada ao abrir. O "Expirado" é **só visual**: o código manda `update status='expirado'` sem aguardar a resposta e o cliente do Supabase só envia o pedido quando é aguardado, então o banco segue "Enviado" (a confirmar) | — | `hooks/useQuotes.ts:203-209,389-399`, `hooks/useQuoteChargedIds.ts:49`, `pages/Quotes.tsx:174` |
| Mudar status · Excluir (3.1) | — | `quotes` (update do status; delete). Os `quote_items` caem junto (`ON DELETE CASCADE`). Lançamento financeiro e OS ligados **não** são apagados; a OS só perde a origem (`service_orders.quote_id` é `ON DELETE SET NULL`) | — | `hooks/useQuotes.ts:283-316`, `supabase/migrations/20260308135145_03d237fb-65e5-410b-8098-2b2a567d12b7.sql:26`, `supabase/migrations/20261008130000_par_orcamento_os_converter_em_os.sql:73-79` |
| Gerar link · Copiar · WhatsApp (3.1/3.3) | — (o token já vem na lista) | "Gerar link" em Rascunho: `quotes.status` → `enviado` (3.1). "Copiar link" e "WhatsApp" não gravam nada | Host `wa.me` (abre outra aba); área de transferência do navegador | `utils/shareLinks.ts:62-67,89-90`, `components/quotes/QuoteViewDialog.tsx:73` |
| Wizard "Novo Orçamento" (3.2) | `customers`, `service_types`, `inventory` (só itens da empresa, `customer_id is null`) e `inventory_stock_levels`, `pricing_settings`, `proposal_templates`; ao marcar um serviço: `service_costs`, `service_materials`, `service_cost_resources`, `service_gifts` e a view `cost_resources_with_rate` | `quotes` (insert/update) e `quote_items`. **Editar apaga todas as linhas e insere de novo (ids novos)**. `status` ("rascunho"), `token` (64 caracteres hex) e `quote_number` (sequência) vêm dos **padrões do banco**, não do app. Rascunho em andamento: `sessionStorage` do navegador | — | `components/quotes/QuoteFormDialog.tsx:331-336,638-656,811-816,881,898`, `hooks/useQuotes.ts:225-282`, `hooks/useInventory.ts:73-80,99-104`, `supabase/migrations/20260308135145_03d237fb-65e5-410b-8098-2b2a567d12b7.sql:5,7,17` |
| "Visualizar" (3.3) | `company_settings` (logo, cores, `proposal_customization`) | Nada | PDF gerado **no navegador** (`utils/proposalPdf.ts`, baixa um arquivo) | `components/quotes/QuoteViewDialog.tsx:38,124`, `utils/proposalPdf.ts` |
| "Aprovar Orçamento" (3.4) | `financial_accounts`, `cost_centers`, `financial_categories` (nome atual da categoria de receita; se não achar, usa o nome de semente "Vendas de Serviços"), `company_settings` | `financial_transactions` (insert: "Já recebi" = 1 receita + tarifa opcional; "Vou receber depois" = 1 a N parcelas) e `quotes` (`status='aprovado'`, `financial_generated_at`, `financial_transaction_id`, `receivable_installments`, `receivable_first_due_date`). **Nenhum lançamento de custo** | — | `components/financial/ApproveQuoteModal.tsx:125,133`, `hooks/useFinancialCategories.ts:79-112`, `lib/finance-system-categories.ts:143-145`, `hooks/useQuoteConversion.ts:255-290,302-370` |
| "Desfazer lançamento" (3.6) | `financial_transactions` (prévia: a receita, a tarifa e as parcelas do mesmo grupo) | `financial_transactions` (delete) e `quotes` (zera `financial_generated_at`/`financial_transaction_id`, status → `enviado`). Rede de segurança **no banco**: gatilho `trg_reset_quote_financial_link_on_delete` (4.2) | — | `hooks/useRelatedTransactions.ts:9-70,127-188`, `pages/Quotes.tsx:942-997` |
| "Gerar OS" (3.5) | No app: `equipment` do cliente, `service_types`. No banco (função): `quotes`, `quote_items`, `customers`, `equipment`, `service_types`, `inventory`, `form_template_service_types`, `form_templates` | Função `generate_service_order_from_quote(p_quote_id, p_equipment_services)` grava `service_orders` (status `agendada`), `service_order_budget_items`, `service_order_service_types`, `service_order_equipment_service_types`, `service_order_equipment` e `quotes` (`status='convertido'`, `converted_to_os_id`). **Não toca em estoque nem em financeiro** | RPC só para `authenticated` (sem `anon`) | `hooks/useQuoteConversion.ts:177-203`, `components/quotes/QuoteServiceDistributionDialog.tsx:28-29`, `supabase/migrations/20261019041000_protecao_escopo_e_distribuicao_orcamento.sql:198-355`, `supabase/migrations/20261027120000_orcamento_total_comercial_na_conversao_os.sql:8-30` |
| "Configurar Proposta" (3.7) | `company_settings.proposal_customization` (JSON) | `company_settings` (update do JSON); o logo grava na hora | Bucket **`company-logos`** (envia, remove, URL pública) | `components/quotes/ProposalConfigDialog.tsx:160,270-275,299-333` |
| Aba "Custos dos Serviços" (3.8) | `service_types`, `service_costs`, `service_materials`, `service_cost_resources`, `service_gifts`, view `cost_resources_with_rate`, `inventory`, `employees`, `pricing_settings` | `service_costs` (mão de obra: valor/hora e horas), `service_materials` (o app calcula o `subtotal`), `service_cost_resources` (recurso + valor próprio), `service_gifts`, e `employees.monthly_cost` (calculadora de mão de obra) | — | `hooks/useServiceCosts.ts:38-84`, `hooks/useServiceMaterials.ts:29-109`, `hooks/useServiceCostResources.ts:43-221`, `components/service-orders/LaborCalculatorModal.tsx:67,471` |
| Aba "Custos Globais" (3.9) | A view `cost_resources_with_rate` (lista e "Custo por hora") | `cost_resources` e `cost_resource_items` (criar, editar, apagar); foto do recurso | Bucket **`equipment-files`** (foto) | `hooks/useCostResources.ts:67,122-268`, `components/service-orders/CostResourceFormSheet.tsx:247-249` |
| Aba "Precificação" (3.10) | `pricing_settings` (cria a linha da empresa sozinho na 1ª abertura) | `pricing_settings` (upsert) | — | `hooks/usePricingSettings.ts:28-54` |
| Página pública (3.11) | Função `get_quote_public_payload(_token)`; tabela `proposal_templates` (pelo apelido do modelo) | Funções `record_quote_view(_token, _fingerprint, _user_agent)` (grava `quote_views` e `quotes.view_count/last_viewed_at`) e `respond_quote_public(_token, _status)` (grava `quotes.status` e, se a opção estiver ligada, a conta a receber) | Função de borda **`notify-quote-response`** (grava `user_notifications` para os admins); `/pagar/<código>` abre outra aba; PDF no navegador | `pages/ProposalPublic.tsx:133,184,196,216,236`, `supabase/migrations/20260624120000_quote_view_tracking.sql:58-133`, `supabase/functions/notify-quote-response/index.ts:95-192` |

### 4.2 Regras que o **banco** aplica sozinho (o roteiro não pode prometer diferente)

- **Padrões:** `quotes.status` = "rascunho"; `quotes.token` = 64 caracteres hexadecimais aleatórios; `quotes.quote_number` = sequência (o `#N` que o cliente vê) (`supabase/migrations/20260308135145_03d237fb-65e5-410b-8098-2b2a567d12b7.sql:5,7,17`).
- **Apagar o lançamento pelo Financeiro (T13) destrava o orçamento:** gatilho `trg_reset_quote_financial_link_on_delete` (antes de apagar): zera `financial_generated_at` e `financial_transaction_id` e, se estava "Aprovado" e sem OS, volta a "Enviado". Só a **1ª parcela** é a apontada pelo orçamento; apagar outra parcela não destrava (`supabase/migrations/20261008120000_destrava_orcamento_quando_lancamento_e_apagado.sql:44-92`).
- **Apagar a OS gerada devolve o orçamento a "Aprovado":** gatilho `trg_reset_quote_conversion_on_os_delete` (antes de apagar a OS): solta `converted_to_os_id` e troca "Convertido" por "Aprovado" (`supabase/migrations/20261008140000_destrava_orcamento_quando_os_convertida_e_apagada.sql:66-96`).
- **Uma OS por orçamento e um orçamento por OS:** índices únicos `uq_service_orders_quote_id` e `uq_quotes_converted_to_os_id`; gatilho que impede ligar orçamento e OS de empresas diferentes (`supabase/migrations/20261018231000_orcamento_da_os_e_gerar_os.sql:60-65,86,107-108`).
- **Estimativa não é consumo:** o cabeçalho da migration que criou o orçamento dentro da OS diz que a estimativa comercial "não é consumo de estoque"; a baixa física fica para os materiais da OS durante a execução (`supabase/migrations/20261018231000_orcamento_da_os_e_gerar_os.sql:1-5`).
- **"Converter em OS" nunca funcionou antes de 08/10/2026:** as colunas `service_orders.quote_id` e `quotes.converted_to_os_id` não existiam no banco (PGRST204); nenhum orçamento "Convertido" existia (`supabase/migrations/20261008130000_par_orcamento_os_converter_em_os.sql:1-35`). Por isso a trilha de 1.22.5 não é base confiável para o capítulo 14.
- **Brinde tem `subtotal` gerado pelo banco** (`unit_cost * quantity`); o de **material** é calculado pelo app (`supabase/migrations/20260309023425_76066298-98c3-4891-96c5-1fb6a94dda1b.sql:42`, `hooks/useServiceMaterials.ts:45-51,74-85`).
- **A view `cost_resources_with_rate`** devolve, por recurso, "custo mensal total" = soma dos itens e "custo por hora" = custo mensal ÷ horas mensais (0 se as horas forem 0) (`supabase/migrations/20260316040419_65562494-bab7-40ac-906f-eacfad3165bc.sql:5-25`). Ela chegou a vazar entre empresas por falta de `security_invoker`; **já corrigido** em 18/10/2026 (`supabase/migrations/20261018190000_fecha_vazamento_view_custo_e_superficie_anon.sql:161-185`), não é achado novo.

### 4.3 Comparação com o backend falso (`/home/claude/domiflix/rec/fakebase`)

O T9 é o tutorial que **mais depende de dado que o fakebase ainda não tem**. Estado de hoje:

| Item | Hoje no fakebase | O que o T9 precisa | Evidência |
|---|---|---|---|
| Sementes do ecossistema de orçamento | **Nenhuma** linha de `quotes`, `quote_items`, `pricing_settings`, `service_types`, `service_costs`, `service_materials`, `service_gifts`, `service_cost_resources`, `cost_resources`, `cost_resource_items`, `proposal_templates`, `quote_views`, `inventory`, `employees`, `financial_accounts`, `financial_categories`, `cost_centers`, `tenant_charges`, `service_orders`, `form_templates` | Criar sementes (inclusive 4 linhas de `proposal_templates`: `clean`, `vanguarda`, `aurora`, `prisma`; a migration do repositório só cria `classico`/`moderno`/`minimalista` e depois `aurora`/`prisma`, ver seção 7) | `rec/fakebase/seeds/gen-01-tenant.json`, `rec/fakebase/seeds/gen-02-cadastros.json`, `rec/fakebase/seeds/00-vazias.json`, `supabase/migrations/20260308142051_f923d891-447c-4b19-a26c-0c70b909a9c3.sql:18-21`, `supabase/migrations/20260624130000_proposal_templates_catalog_swap.sql:13-17` |
| Padrões de linha nova | `TABLE_DEFAULTS` só tem `equipment` e `customers`. Em `quotes`, `status` e `token` (texto com padrão no banco) nascem **`null`** e `quote_number` nasce **0** (o fakebase só chuta valor para booleano, número, lista e enumeração); as linhas novas nasceriam sem status, sem link e com o número 0 | Acrescentar `TABLE_DEFAULTS.quotes` = `status: 'rascunho'`, `token` aleatório de 64 caracteres, `quote_number` pela sequência (`nextSeq`, disponível no contexto: `rec/fakebase/core/mutate.mjs:36`) | `rec/fakebase/core/defaults.mjs:12-22,40-72`, `rec/fakebase/core/defaults.mjs:26-34`, `rec/fakebase/schema.json` (`quotes.status/token/quote_number`) |
| Colunas "geradas" | O fakebase não calcula coluna gerada: o `subtotal` de `service_gifts` ficaria `null` (custo do brinde = 0) | Gancho (`rec/fakebase/hooks/`) que preenche `subtotal = unit_cost × quantity` em `service_gifts`; nas sementes, `subtotal` já calculado | `rec/fakebase/hooks/` (só `customers`, `equipment`, `lead_capture_forms`), `hooks/useServiceCostResources.ts:127` |
| View `cost_resources_with_rate` | Existe no `schema.json`, mas **não há provedor** (`handlers/views/` vazio): a aba "Custos Globais" e o "Custo por hora" nasceriam vazios | `handlers/views/cost_resources_with_rate.mjs` que some `cost_resource_items` e divida pelas horas mensais | `rec/fakebase/server.mjs:35-37`, `rec/fakebase/core/query.mjs:10-16`, `rec/fakebase/schema.json` (views) |
| Função `generate_service_order_from_quote` | **Sem manipulador**: o pedido vira `RPC_SEM_HANDLER` e devolve `{}`; o app mostra o toast de sucesso "OS gerada com sucesso!" **sem criar OS nem mudar o orçamento** | Manipulador que crie a OS (status `agendada`), as linhas de orçamento da OS e marque o orçamento "Convertido" | `rec/fakebase/http/rest.mjs:172-176`, `rec/fakebase/core/schema.mjs:80-94`, `hooks/useQuoteConversion.ts:186` |
| Funções públicas da proposta | `get_quote_public_payload` e `respond_quote_public` (retorno `json`) devolvem `null`: a página mostra "Proposta não encontrada." e, ao responder, cai em "Esta proposta já foi respondida."; `record_quote_view` devolve 0 | Manipuladores dos três; a gravação precisa **navegar** (`goto`) para `/proposta/<token>?preview=1` na mesma aba (sem nova aba, sem sessão anônima) | `rec/fakebase/http/rest.mjs:172-176`, `pages/ProposalPublic.tsx:133-179,216-256` |
| Função de borda `notify-quote-response` | Sem manipulador (só existem `cep-lookup`, `lead-capture-submit`, `tenant-asaas-card-fees`); a chamada é "melhor esforço" e não quebra a resposta | Opcional: manipulador que grave `user_notifications` | `rec/fakebase/handlers/functions/`, `pages/ProposalPublic.tsx:229-243` |
| Opções da empresa | A semente de `company_settings` não traz `quote_approval_revenue_mode` nem `quote_public_approval_creates_receivable`: valor `null` cai em "a receber"/desligado (o esperado) | Só confirmar; se o roteiro mostrar "Já recebi" como padrão, trocar na semente | `rec/fakebase/seeds/gen-01-tenant.json`, `pages/Quotes.tsx:174` |
| Estoque que o orçamento usa (T8) | `useInventory` lê `inventory` e `inventory_stock_levels`; sem semente, o passo "Materiais" fica vazio | Semear os 9 materiais do T8 **com preço de venda** (sem ele o orçamento usa o preço de custo) | `hooks/useInventory.ts:73-80,99-104`, `T08/plano.md:70-84` |
| Funcionários e contas | `employees`, `financial_accounts`, `financial_categories` sem semente: a calculadora de mão de obra e o modal "Aprovar Orçamento" abrem vazios | Semear técnicos com `monthly_cost` fictício, 1 conta (ex.: "Conta principal") e as categorias de sistema | `components/service-orders/LaborCalculatorModal.tsx:67-71`, `components/financial/ApproveQuoteModal.tsx:125,133` |
| Downloads, nova aba, anônimo | Fora do alcance do gravador (TRILHA 5-8): "Baixar PDF", "WhatsApp", "Abrir proposta" (aba nova), "Pagar" e a foto do recurso (envio de arquivo funciona, mas é arriscado) | Mostrar a proposta **dentro** do "Visualizar" e por `goto`; não gravar download | `pages/Quotes.tsx:452,805`, `pages/ProposalPublic.tsx:296-368` |

- O recorte `quotes → customers`, `quotes → proposal_templates` e `quote_items → quotes` existe no `schema.json` (relacionamentos), então os **embutidos da lista** devem resolver; testar `quotes?select=*,customers(...),quote_items(*),proposal_templates(...)` depois de semear (`rec/fakebase/schema.json`, `quotes`/`quote_items` → `relationships`).
- `desconhecidos.log` hoje só tem 13 linhas, nenhuma do T9: o que o app pede na abertura de Orçamentos ainda **não foi exercitado** contra o fakebase (`rec/fakebase/desconhecidos.log`).

---

## 5. Pegadinhas

> `[handoff]` = decisão de produto ou de tela para quem cuida do app (o tutorial não conserta nem esconde). `[handoff, segurança]` = risco de dados, só relatado, **não corrigido**.
> "Roteiro" = muda o que o narrador pode dizer. "Gravação" = muda como gravar.

**Roteiro: o que mudou ou engana**

- **P1. "Gerar OS" não baixa estoque nem lança nada no financeiro.** Cria a OS ("agendada"), copia as linhas do orçamento e a distribuição por equipamento e marca o orçamento "Convertido" (`supabase/migrations/20261019041000_protecao_escopo_e_distribuicao_orcamento.sql:300-349`).
  O banco diz que a estimativa da OS "não é consumo de estoque": a baixa fica nos materiais da própria OS, na execução (`supabase/migrations/20261018231000_orcamento_da_os_e_gerar_os.sql:1-5`). A trilha (1.22.5: "converter... baixa o estoque") e o Guia Técnico estão **desatualizados**; o roteiro só pode dizer que o consumo de material acontece na OS (T5).
- **P2. Aprovar lança só a receita; o custo do orçamento é "demonstrativo".** Dois modos: "Já recebi" (entrada paga + tarifa opcional) e "Vou receber depois" (1 a 12 parcelas pendentes); o que abre marcado vem da empresa, padrão "Vou receber depois" (3.4, 3.12; `hooks/useQuoteConversion.ts:205-220,323-348`). Trilha e Guia ainda dizem "receita + custo + mão de obra".
- **P3. Só "Gerar link da proposta" promove Rascunho a Enviado.** "WhatsApp" e "PDF" do Visualizar não mudam o status `[handoff]`; "Criar Orçamento" também deixa em Rascunho. A página pública só mostra "Aprovar"/"Rejeitar" com o orçamento em Enviado: proposta mandada por WhatsApp sem ter gerado o link chega **sem botões** (`pages/Quotes.tsx:190-214`, `components/quotes/QuoteViewDialog.tsx:66-74`, `pages/ProposalPublic.tsx:288-290`).
- **P4. Aprovação feita pelo cliente no link não lança nada (padrão) e depois o orçamento fica sem saída pelo menu.** A opção "Aprovação pelo link da proposta já gera conta a receber" vem desligada; com ela desligada o orçamento fica "Aprovado" sem "No financeiro" e o item "Aprovar orçamento" só existe para Rascunho/Enviado: sobram "Gerar cobrança" ou o lançamento manual `[handoff]` (`pages/Settings.tsx:1751-1775`, `pages/Quotes.tsx:462-473`, `supabase/migrations/20260919230000_aprovacao_publica_usa_categoria_renomeada.sql:161-337`).
- **P5. Dois valores no orçamento: "Total do orçamento" × "Sugestão pelo BDI".** O cliente vê, a lista mostra e a OS recebe o **Total do orçamento** (preços das linhas + deslocamento − desconto). A "Sugestão pelo BDI" é referência interna. Até a migration de 27/10/2026 a OS recebia a sugestão; hoje recebe o total comercial (`lib/quote-commercial-total.ts:9-11`, `components/quotes/QuoteFormDialog.tsx:81-102`, `supabase/migrations/20261027120000_orcamento_total_comercial_na_conversao_os.sql:8-30`).
- **P6. Empresa nova nasce com a Precificação zerada** `[handoff]`. A aba cria a linha da empresa com Imposto, Adm., Lucro, Custo por km, Desconto à vista e Parcelas todos em 0: **BDI 1,0000** e "Preço sugerido" = custo. Os "padrões 10/12/10/1/6/10" da tela e do Guia só valem depois que alguém salva
  (`supabase/migrations/20260425000000_drift_missing_tables.sql:29-39`, `hooks/usePricingSettings.ts:37-46`, `components/pricing/PricingConfigForm.tsx:24-29`). O roteiro precisa **preencher e salvar** a Precificação antes de orçar.
- **P7. Custos Globais e Precificação deixaram de ser "módulo pago".** A trilha marcava 🔒; desde a 1.29.0 (13/10/2026) valem para todo plano e nenhuma tela consulta o módulo (seção 2; `pages/Changelog.tsx:2217`). Não dizer "do plano avançado".
- **P8. Preço sugerido do serviço, em ordem:** (a) custos cadastrados ÷ BDI; (b) preço padrão do tipo de serviço (T4); (c) 0. Serviço sem custo mostra o selo âmbar "Sem custos configurados" e pode ainda ter preço pelo padrão do tipo (`components/quotes/QuoteFormDialog.tsx:678-692`). Para o BDI aparecer funcionando, o serviço da cena precisa ter custos cadastrados.
- **P9. As "Observações" saem impressas na proposta** `[handoff]`. O campo tem o exemplo "Observações internas", mas o modelo Clean imprime a seção "Observações" para o cliente (`components/quotes/templates/CleanTemplate.tsx:236-430`, ordem das seções em `components/quotes/templates/types.ts:3-102`).
  No vídeo, não escrever nada interno ali; usar "Condições / Termos" para o texto do cliente.
- **P10. "Expirado" é só visual; a validade não bloqueia nada** (a confirmar rodando). A lista troca o selo para "Expirado" no navegador, mas o pedido que gravaria isso não é aguardado (nunca sai) e nenhuma rotina do servidor expira orçamento; a função pública de resposta só exige status "Enviado" e não olha a data (`hooks/useQuotes.ts:389-399`, `supabase/migrations/20260919230000_aprovacao_publica_usa_categoria_renomeada.sql:161-337`).
  O Guia Técnico afirma que o orçamento "expira sozinho ao abrir a tela". O roteiro pode falar "a validade aparece na proposta", sem prometer bloqueio.
- **P11. A % do cartão "Conversão" cai depois do "Gerar OS"** `[handoff]` (o "Convertido" sai da conta: 3.1; `hooks/useQuotes.ts:402-404`). Não mostrar o cartão logo depois de gerar uma OS, ou falar "Conversão = aprovados entre os já respondidos".
- **P12. "Salvar rascunho" num orçamento já enviado/aprovado o rebaixa a Rascunho** `[handoff]` (3.2.4; `components/quotes/QuoteFormDialog.tsx:896-916`). Na edição usar "Salvar Alterações".
- **P13. "Editar" vale para qualquer status** `[handoff]` e a edição **apaga e recria todas as linhas** (ids novos): não refaz lançamento nem OS, e as linhas do orçamento da OS perdem o vínculo com a linha de origem (`source_quote_item_id` é `ON DELETE SET NULL`) (`hooks/useQuotes.ts:260-282`, `supabase/migrations/20261018231000_orcamento_da_os_e_gerar_os.sql:6-26`). Não mostrar edição de orçamento aprovado ou convertido.
- **P14. "Rejeitar" não pede confirmação nem tem desfazer** `[handoff]` (3.1, item 5; `pages/Quotes.tsx:802-863`); o cliente também não confirma no link (3.11). No vídeo, mostrar o menu sem clicar em "Rejeitar".
- **P15. "Desfazer lançamento" apaga também parcelas já pagas e funciona depois do "Gerar OS"** `[handoff]` (3.6; `hooks/useRelatedTransactions.ts:127-188`). Apagar o lançamento direto no Financeiro também destrava o orçamento, pelo banco (4.2). No vídeo, desfazer só **antes** de gerar a OS e sem parcela paga.
- **P16. "Gerar OS" exige distribuir** cada serviço em ao menos 1 equipamento do cliente (se ele tiver equipamentos); cliente sem equipamento ou prospecto gera OS sem equipamentos. **Não existe "desfazer Gerar OS"** (apagar a OS devolve o orçamento a "Aprovado", 4.2). Textos fixos no código (3.5; `components/quotes/QuoteServiceDistributionDialog.tsx:47-49,88-102,152-154`). A cena precisa de cliente **com equipamentos**.
- **P17. "Configurar Proposta":** o modelo escolhido na etapa 1 é só prévia (não grava), o "Salvar" não fecha a janela e ligar/desligar/reordenar seções só vale no Clean `[handoff]` (3.7; `components/quotes/ProposalConfigDialog.tsx:270-275,408-459`). O modelo que vale é o da etapa 5 de cada orçamento.
- **P18. O Clean (padrão) não mostra brindes** `[handoff]`, mesmo com "Incluir brindes neste orçamento" marcada e o custo do brinde dentro do preço do serviço (3.11.1; `components/quotes/templates/CleanTemplate.tsx:236-430`, `lib/i18n/messages/app/crm.ts:1184-1185`). Não prometer "brinde na proposta" com o Clean.
- **P19. Dois botões "Salvar" na Precificação** gravam as seis taxas de uma vez `[handoff]` (3.10; `components/pricing/PricingConfigForm.tsx:137-145,175-185`). Clicar em qualquer um.

**Gravação**

- **P20. O rascunho do navegador reaparece na tomada seguinte** ("Rascunho encontrado"): fechar o assistente no meio deixa o aviso; limpar o armazenamento da sessão entre tomadas (3.2.4; `components/ui/DraftResumeDialog.tsx:24,58-70`, `components/quotes/QuoteFormDialog.tsx:406-445,1646-1660`).
- **P21. Área de transferência:** se o gravador bloquear a cópia, "Gerar link da proposta" mostra o toast "Link da proposta gerado" com o link no texto (inócuo; `pages/Quotes.tsx:190-214`).
- **P22. Relógio:** "Proposta válida até", "Documento gerado em", "visto há X", a data de recebimento e o 1º vencimento padrão usam o relógio do navegador: travar (TRILHA 5).
- **P23. Download, nova aba, sessão anônima:** "PDF", "WhatsApp", "Abrir proposta em nova guia" e "Pagar" ficam fora do gravador (TRILHA 5-8). A proposta se mostra no "Visualizar" e, para a visão do cliente, por navegação na mesma aba (4.3; `pages/Quotes.tsx:452,805`, `pages/ProposalPublic.tsx:296-368`).
- **P24. "Visualizada N×" só aparece se o orçamento da semente tiver `view_count` e `last_viewed_at`**; abrir com `?preview=1` não conta (3.11; `pages/ProposalPublic.tsx:181-195`).

**Produto e segurança (só relato)**

- **P25. Textos fixos fora do i18n** `[handoff]` (baixa): janela de distribuição, aviso "Rascunho encontrado", toasts dos hooks ("Orçamento criado com sucesso!", "Orçamento atualizado!", "Status atualizado!", "Orçamento excluído!") e o selo "Lançamento financeiro gerado" ficam em português se o idioma mudar (`hooks/useQuotes.ts:244,279,297,311`). Não aparece no vídeo em pt-br.
- **P26. Textos e funções sem uso** `[handoff]` (baixa): `approveDesc`, `reviewSummaryTitle`, `cleanVisitDate`, `sectionEnabled/sectionDisabled/sectionDragHandle/sectionPagamentoHint` existem no i18n sem tela que os use (`lib/i18n/messages/app/crm.ts:511,636,1206,710-712,728`), e a função `duplicateQuote` do hook não tem botão (`hooks/useQuotes.ts:318,429`): **não existe "Duplicar orçamento" na tela**.
- **P27. [handoff, segurança] (média, a confirmar rodando) Quem tem o link da proposta consegue ler custo, margem e BDI pela API aberta.** A função pública da proposta foi corrigida em 22/07/2026 para **não** devolver custo, margem nem BDI (lista de campos permitidos, `supabase/migrations/20260722140100_get_quote_public_payload_allowlist.sql:1-14`).
  Mas as tabelas `quotes` e `quote_items` mantêm leitura para `anon` condicionada **só** ao cabeçalho `x-share-token` igual ao token do orçamento e **sem restrição de colunas** (`supabase/migrations/20260418165718_0810b15b-ad57-4b5a-8b2a-8120eb22db34.sql:28-31`; itens: `supabase/migrations/20261019050000_pdv_cofre_no_zerar_sistema_e_aperto_de_policy_anon.sql:806-823`). A própria equipe classificou as duas como "gateadas por token, ficam" (`supabase/migrations/20261018211000_revoga_anon_acidental_no_schema_public.sql:19-20,91-97`)
  e **mediu** que a chave pública mais o cabeçalho devolve as linhas do orçamento (`supabase/migrations/20261019050000_pdv_cofre_no_zerar_sistema_e_aperto_de_policy_anon.sql:51-61`). Provável efeito: o destinatário, com a chave pública do app (visível no navegador) e o token do próprio link, lê `total_cost`, `bdi`, `profit_rate`, `tax_rate`, `km_cost`, `created_by`, `assigned_to` e, nas linhas, `unit_total_cost`, `unit_labor_cost`, `unit_materials_cost`, `unit_hourly_rate`, `price_override`.
  **Não é vazamento entre empresas** (o token é do próprio orçamento): é segredo comercial de quem orça. Confirmar com uma chamada de teste e, se confirmar, restringir colunas ou ler só pela função. Nada foi alterado.
- **P28. [handoff, segurança] (baixa, dentro da mesma empresa) Acesso só por empresa, sem papel.** `quotes` e `employees` liberam leitura e escrita a **qualquer usuário logado da empresa**; quem restringe por papel é a tela (`supabase/migrations/20260418163700_9165358e-c67c-420d-b74f-be9aeac54c1e.sql:116,207`).
  A calculadora de mão de obra (Custos dos Serviços) lista os funcionários ativos **com o custo mensal ou salário de cada um** e grava `employees.monthly_cost` e o detalhamento sem checar papel (`components/service-orders/LaborCalculatorModal.tsx:67-71,98-116,465-479`); as colunas "Custo" e "Margem" da lista também aparecem para qualquer um com a tela de Orçamentos. Usar **só valores fictícios** na gravação e confirmar se existe outra camada de restrição em `employees`.
- **P29. [handoff, segurança] (baixa) A função pública devolve a alíquota de imposto** (`tax_rate`) que nenhum modelo de proposta usa (`supabase/migrations/20261013023000_quote_public_payload_country_regional.sql:52`). Tirar da lista de campos permitidos.
- **P30. [handoff] (baixa) "Aprovar orçamento" e "Gerar cobrança" não se excluem no banco:** as duas travas (esconder "Aprovar orçamento" quando já há cobrança, esconder "Gerar cobrança" quando já há lançamento) existem só na tela (`pages/Quotes.tsx:462-473,520,811-815,848`, `hooks/useQuoteChargedIds.ts:1-70`; histórico em `pages/Changelog.tsx:4213`).
  Não achei trava no banco: dois navegadores abertos, ou um lançamento manual no Financeiro, ainda podem duplicar a receita.
- **P31. [handoff] O link da notificação** `/orcamentos?quote=<id>&r=<status>` não é lido por nenhuma tela (cai na lista, sem destaque) (`supabase/functions/notify-quote-response/index.ts:98`). O Guia Técnico diz que "leva direto ao orçamento".

---

## 6. 🚫 Não prometer / telas mortas

- **Orçamento virar contrato**, **assinatura eletrônica** da proposta, **lembrete ou cobrança automática** de proposta/validade: não existem no código do orçamento (a busca por assinatura e lembrete em `components/quotes/`, `pages/Quotes.tsx`, `pages/ProposalPublic.tsx`, `hooks/useQuotes.ts` e `hooks/useQuoteConversion.ts` não acha nada; "contrato" só aparece num comentário, `hooks/useQuoteConversion.ts:73`). A aprovação do cliente é **um clique**, sem validade de assinatura formal.
- **Expiração automática** ou bloqueio por validade (P10): o selo "Expirado" é só da tela.
- **Duplicar orçamento**: não há botão (P26).
- **Desfazer "Gerar OS"** e **desfazer "Rejeitar"** (P14, P16); apagar a OS pelo módulo de OS devolve o orçamento a "Aprovado" (4.2), mas isso é outra aula.
- **Baixa de estoque, ou qualquer lançamento financeiro, pelo "Gerar OS"** (P1); **custo no financeiro** pela aprovação (P2).
- **WhatsApp automático**: o botão abre `wa.me` com texto pronto; o envio é manual e não muda o status (P3). O menu da linha e o Visualizar não têm envio por e-mail (3.1, 3.3).
- **Gravar o modelo escolhido em "Configurar Proposta"** (P17), **brindes na proposta Clean** (P18), **reordenar seções fora do Clean** (3.7), **abrir o orçamento pelo aviso do sino** (P31).
- **Aprovar parte do orçamento** ou o cliente editar a proposta: a resposta do cliente é do orçamento inteiro (função pública com um único status, `supabase/migrations/20260919230000_aprovacao_publica_usa_categoria_renomeada.sql:161-337`).
- **"Precificação Avançada" como plano pago** e o **simulador `/proposta`** (sem token) da própria Dominex, que mostra módulos e **valores de plano**: fora do vídeo (decisão de 30/10, seção 1).
- **Foto do recurso, "Baixar PDF", "Pagar", nova aba:** o gravador não faz upload nem download nem segue outra aba; mostrar o botão, não o resultado (P23).
- **Telas e textos mortos que não aparecem:** `approveDesc`, `reviewSummaryTitle`, `cleanVisitDate`, os quatro textos de seção do Configurar Proposta (P26) e as funções `fetchQuoteByToken`/`respondByToken` do hook, sem uso (`hooks/useQuotes.ts:369,380`).

---

## 7. Dúvidas em aberto

1. **Padrão de `pricing_settings` em produção.** Empresa nova nasce zerada mesmo? (arquivo de migration diz 0; a tela e o Guia dizem 10/12/10/1/6/10). Conferir numa empresa criada hoje (P6).
2. **A leitura anônima de `quotes`/`quote_items` com `x-share-token` devolve as colunas internas?** Testar com uma chamada de verdade (P27).
3. **O "Expirado" grava no banco?** Esperado que não (P10); conferir abrindo a lista com um orçamento vencido e olhando o status na tabela.
4. **Linhas `clean` e `vanguarda` em `proposal_templates`.** As migrations do repositório só criam `classico`/`moderno`/`minimalista` e `aurora`/`prisma`; `vanguarda` e `clean` devem ter nascido fora delas (`supabase/migrations/20260624130000_proposal_templates_catalog_swap.sql:2-8,19-21`). Conferir em produção quais slugs existem e como o app acha o "Clean" padrão.
5. **Padrão de "Mostrar paginação?"**: a tela abre em Sim, o comentário do tipo diz "desligado" (3.7). Qual é o intencional?
6. **Como a OS gerada aparece na tela de OS (T5):** o banco grava o status `agendada`, sem data nem técnico (3.5); confirmar o rótulo exato na lista de OS.
7. **Excluir orçamento com lançamento ou OS ligados:** pelas chaves do banco o lançamento e a OS ficam (4.1); confirmar rodando e ver como a OS mostra a origem perdida.
8. **A visão do cliente por `goto`:** a página `/proposta/<token>?preview=1` abre na mesma aba com o usuário logado e as funções públicas aceitam essa sessão? (4.3). Alternativa: gravar só o "Visualizar".
9. **Ordem dos capítulos:** "motor primeiro" (Precificação → Custos Globais → Custos dos Serviços → orçamento) ou a ordem da trilha (orçamento primeiro)? Decisão do Kaik (plano).
10. **Preços de venda dos materiais do T8:** o orçamento usa o preço de venda; a semente do T8 tem só compra/cotação. Definir os preços de venda junto com o T8.
11. **Funcionários da calculadora de mão de obra:** quais nomes e custos mensais fictícios (P28).
12. **Nome da categoria de receita:** sem categorias semeadas o app cai em "Vendas de Serviços" (`lib/finance-system-categories.ts:143-145`); combinar com o T13.
13. **"Gerar cobrança" no menu da linha:** com módulo Cobranças e conta Asaas ativa na semente atual o item aparece; mostrar ou só passar? (T19).
14. **Cliente da cena com equipamentos:** conferir quantos equipamentos a Pousada Brisa do Mar tem na semente (4.3, P16).
