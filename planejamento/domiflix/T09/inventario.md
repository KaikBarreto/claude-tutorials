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
| Excluir | Janela "Excluir orçamento?" / "Esta ação não pode ser desfeita." / "Cancelar" · "Excluir"; toast (fixo) "Orçamento excluído!". Vale para qualquer status; a tela não confere se já há lançamento ou OS ligados (a confirmar o que o banco faz, seção 7) | `pages/Quotes.tsx:924-940`, `hooks/useQuotes.ts:304-316` |

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
  Guarda destinatário, BDI, desconto, termos etc., **não os itens** (`QuoteFormDialog.tsx:406-445,1646-1660`, `components/ui/DraftResumeDialog.tsx:21,31-44`). **Cuidado de gravação:** um ensaio interrompido deixa esse aviso na próxima tomada (limpar o armazenamento da sessão do navegador entre tomadas).
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
- Apaga **a receita, a tarifa e todas as parcelas do mesmo parcelamento, pagas ou não**, e devolve o orçamento a "Enviado" (`hooks/useRelatedTransactions.ts:9-70,127-190`) `[handoff]`.
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
