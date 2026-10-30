# Inventário funcional · T19 — Integração com Asaas, Assinaturas e Cobranças (Dominex)

> Base para o roteiro do tutorial "T19 · Integração com Asaas, Assinaturas e Cobranças". Levantado em 30/10/2026 contra o
> código publicado `APP_VERSION = "1.38.6"` (`src/config/version.ts:1`), cópia em `/home/claude/domiflix/src-1.38.6`.
> **Análise estática, somente leitura.** "(a confirmar)" = só rodando. Formato do inventário do T3/T12.
> Gravação só com o Asaas **simulado** no backend falso (TRILHA, decisão 3): nenhuma conta, chave ou token real.

## Como ler

- Caminhos relativos a `src/`, exceto `supabase/...` e `rec/...`. Formato `arquivo:linha`.
- Rótulos entre aspas = texto exato (pt-br). Fontes dos textos: **ch** = `lib/i18n/messages/app/charges.ts:10-700`
  (bloco pt-br: `central`, `cobrar`, `checkout`, `subscriptions`) e **st** = `lib/i18n/messages/app/settings.ts:1474-1672`
  (bloco `integrations`).
- "Cobrança" = cobrança online gerada no Asaas da empresa (`tenant_charges`), com link `/pagar/<código>`. "Assinatura" =
  cobrança recorrente do cliente da empresa (`tenant_subscriptions`). **Não confundir** com a assinatura que a empresa paga
  à Dominex (tela "Assinatura", `/assinatura`, `pages/Billing.tsx`), que é do T0.

---

## 0. Resumo para o roteiro

### 0.1 Capítulos da trilha (v1.22.5) contra o código de hoje

| # | Item da trilha | Situação | O que ajustar |
|---|---|---|---|
| 1 | Papel da Dominex e do Asaas | **Bate** | O dinheiro cai na conta Asaas da própria empresa; "A Dominex não retém nada por transação." (st `:1565`). Conceito sem tela: ilustração. |
| 2 | Configurações → Integrações → Asaas: conectar e validar a chave | **Mudou o caminho** | Configurações → aba **"Integrações"** → sub-aba **"Cobranças (Asaas)"** → botão **"Configurações"** (`components/settings/SettingsWhatsappContent.tsx:137-200`; st `:1475-1480`). Card **"Recebimentos (Asaas)"**: **"Chave de API da Asaas"** → **"Ativar recebimentos"** (`components/settings/SettingsAsaasContent.tsx:289-303,404-435`). |
| 3 | Taxas reais, métodos e condições | **Bate** | Card **"Taxas da Asaas"** com **"Atualizar taxas"** (`components/settings/AsaasFeesCard.tsx`; st `:1564-1597`); **"Preferências de cobrança"** → "Meios de pagamento habilitados" (st `:1634-1646`). |
| 4 | Conta de recebimento e lançamento automático | **Bate** | **"Lançar cobranças no Financeiro automaticamente"**, **"Lançar a taxa da Asaas como despesa"** e **"Lançamento no Financeiro"** ("Conta bancária de destino", "Categoria da receita", "Categoria da taxa (Asaas)") (st `:1612-1666`). Aviso "Falta escolher a conta que recebe o dinheiro" (st `:1600-1602`). |
| 5 | Simulador: Pix, boleto, cartão, prazo e líquido | **Mudou de lugar** | Botão **"Simulador"** ao lado de "Configurações", dentro de "Cobranças (Asaas)" (Changelog 1.32.1, `pages/Changelog.tsx:1974`; `components/settings/SettingsAsaasSimulator.tsx`; st `:1481-1527`). |
| 6 | Cobrança avulsa: cliente, vencimento, juros, multa, desconto | **Mudou** | Financeiro → **"Cobranças"** → **"Nova cobrança"**: janela em 4 abas **"Cobrança"**, **"Pagamento"**, **"Encargos"**, **"Financeiro"**, com **"Avançar"**, **"Gerar agora"** e **"Gerar cobrança"** (`components/financial/ChargeDialog.tsx:1094-1168`; ch `:146-381`). |
| 7 | Compartilhar o checkout e acompanhar status | **Bate** | Resultado **"Cobrança gerada"**: QR, **"Link de pagamento"** `https://dominex.app/pagar/<código>`, **"Copiar link"**, **"Enviar por WhatsApp"** (ch `:352-362`; `hooks/useTenantCharges.ts:294-296`). Status **"A receber"**, **"Pago"**, **"Vencido"**, **"Estornado"** (ch `:124-130`). |
| 8 | Repasse de taxa e conciliação do líquido | **Bate** | No cartão: **"Quem paga a taxa do cartão?"** "Empresa"/"Cliente" (ch `:226-233`); **"Resumo do recebimento"** com "Taxa da Asaas" e "Você recebe" (ch `:270-333`). A baixa pelo líquido vem do aviso do Asaas (webhook). |
| 9 | Criar assinatura: frequência, duração, formas | **Bate** | Aba **"Assinaturas"** → **"Nova assinatura"**: "Frequência" (Semanal a Anual), "Duração" "Contínua"/"Número de ciclos", "1º vencimento" (ch `:465-537`). |
| 10 | Acompanhar, editar e cancelar assinaturas | **Bate** | Ações "Cancelar", "Editar", "Excluir", "Arquivar"; MRR no topo (ch `:590-650`). |
| 11 | Cobrança de contrato e orçamento | **Maior** | **"Cobrar online"** em cada parcela do contrato e em lote (`lib/i18n/messages/app/pmoc.ts:259-309`); **"Cobrar o saldo"** em Contas a Receber (`lib/i18n/messages/app/finance.ts:270-310`); "Gerar cobranças no Asaas" ao parcelar receita (`finance.ts:853-873`); o mesmo `ChargeDialog` em Orçamentos e no "Faturar" da OS (`pages/Quotes.tsx:999-1001`; `components/service-orders/OsBillingDialog.tsx:188,319-321`). |

Avisos da trilha:

- ⚠️ "CPF ou CNPJ válido do cliente é obrigatório" → **bate**: aviso "<cliente> ainda não tem CPF ou CNPJ no cadastro. A
  Asaas exige esse dado para gerar a cobrança." + **"Completar cadastro"** (ch `:335-341`); o servidor também valida.
- ⚠️ "A confirmação visual do checkout não dá baixa sozinha; o status vem do webhook" → **bate**
  (`supabase/functions/tenant-asaas-webhook/index.ts:18-53`). O checkout do cartão diz "Estamos confirmando com o banco.
  Esta página atualiza sozinha em instantes." (ch `:431-436`).
- ⚠️ "Mostre as taxas retornadas pela conta" → **bate**: "Taxas da sua conta Asaas, atualizadas em…" vs "Taxas de
  referência, não conseguimos ler as da sua conta agora." (st `:1582-1585`).
- ⚠️ "Cancelar assinatura × revogar Pix Automático" → **bate**: selo "Autorização ativa no banco" + "Cancelar de novo"
  (ch `:694-697`). As opções "Cartão de crédito (recorrente)" e "Pix Automático" só aparecem com as chaves da conta ligadas
  (`components/financial/SubscriptionDialog.tsx:182-202`), que em produção nascem **ligadas**
  (`supabase/migrations/20260823170000_cobrancas_flags_default_on.sql`); no seed do fakebase estão **desligadas** (4.4).
- 🔒 **Mudou desde a 1.22.5:** Cobranças é **add-on pago à parte** ("Cobranças online", "Pix, boleto, cartão e assinaturas
  recorrentes via Asaas", `components/ModuleGateModal.tsx:133-136`; Changelog 1.35.6 `:1687`); nenhum plano pronto inclui
  (`supabase/migrations/20261016235900_restaurar_cobrancas_como_addon_pago.sql:1-9`, conforme o T12).

### 0.2 O que mudou desde a 1.22.5 (`pages/Changelog.tsx`)

| Versão | Mudança | Linhas |
|---|---|---|
| 1.24.18–1.24.20 | Decidir por cobrança se entra no Financeiro; editar/excluir cobrança não paga; excluir em lote | `:4023-4033,4092-4097` |
| 1.24.25 / 1.24.52 | Assinatura com prazo para acabar; multa em reais; resumo por cobrança | `:3229-3239,3893` |
| 1.24.44 / 1.24.60 | "Cobrar online" a parcela do contrato; cobrança de várias parcelas de uma vez | `:3097-3107,3465-3480` |
| 1.24.53 | Cancelar Pix Automático encerra a autorização; arquivar assinatura cancelada | `:3202-3212` |
| 1.26.0 | Assinatura no cartão com checkout seguro; previsão de assinaturas no DRE | `:2734-2739` |
| 1.32.1 | Simulador dentro de "Cobranças (Asaas)"; taxas do cartão por faixa de parcelas | `:1974-1979` |
| 1.34.2 | Ativação da integração com a Asaas corrigida | `:1769` |
| 1.35.6 | Cobranças volta a ser módulo contratado separadamente | `:1687` |
| 1.37.32 / 1.37.33 | Boleto excluído no Asaas encerra a conta a receber; "Cobrar o saldo" | `:570-592` |
| 1.37.39 / 1.37.41 | Cobranças de um parcelamento em lote; barra única de busca/filtros | `:399,448` |

### 0.3 O que mais pode surpreender (detalhes na seção 5)

1. **[handoff]** O botão **"Ir para Integrações"** da tela Cobranças (empresa com o módulo mas sem a conta ativa) leva a
   `/configuracoes/integracoes`, rota que não existe (`components/financial/FinanceRelatorio.tsx:141-155`; rotas em
   `App.tsx:866`, `lib/i18n/appRouteSlugs.ts:167`): cai na página "não encontrada". O caminho certo é
   `/configuracoes?tab=integracoes&integration=asaas` (`SettingsWhatsappContent.tsx:141-151`). A aula entra pelo menu.
2. No mundo do fakebase a conta Asaas **já está ativa** (`rec/fakebase/seeds/gen-01-tenant.json`, `tenant_payment_accounts`,
   `status: "active"`). Para mostrar a conexão, o T19 precisa começar sem essa linha (plano, decisão 1).
3. O link mostrado é sempre `https://dominex.app/pagar/<código>` (montado no navegador, `hooks/useTenantCharges.ts:294-296`):
   bom para o vídeo, mas abrir o checkout na gravação exige `goto` na URL local, deslogado (TRILHA 6/7, como no T12).
4. "Pago" depende do aviso do Asaas (webhook). Na gravação isso precisa ser simulado no fakebase (4.3).

---

## 1. Rotas e navegação

| Tela | Como chegar | Rota / componente |
|---|---|---|
| Conectar Asaas | Botão **"Configurações"** no rodapé do menu lateral, junto da conta do usuário (`components/layout/SidebarMenuContent.tsx:705-712`; também no menu do topo, `components/layout/TopNavbar.tsx:468`) → aba **"Integrações"** → **"Cobranças (Asaas)"** → **"Configurações"** | `/configuracoes?tab=integracoes&integration=asaas` (`pages/Settings.tsx:56,112,1892-1893`; `SettingsWhatsappContent.tsx:137-200`) → `components/settings/SettingsAsaasContent.tsx` |
| Simulador | Mesma área → botão **"Simulador"** | `components/settings/SettingsAsaasSimulator.tsx` |
| Cobranças e Assinaturas | Menu "Financeiro" → **"Cobranças"** (só com o add-on) | `/financeiro/cobrancas` (`lib/i18n/appRouteSlugs.ts:158`), abas `?tab=cobrancas` (padrão) e `?tab=assinaturas` (`components/financial/FinanceRelatorio.tsx:99-104`) → `FinanceCobrancas.tsx`, `FinanceAssinaturas.tsx` |
| Checkout público da cobrança | Link `/pagar/<código>` (cliente, sem login) | `App.tsx:763` → `pages/PublicCheckout.tsx` |
| Checkout público da assinatura | Link `/assinar/<código>` (cartão recorrente / Pix Automático) | `App.tsx:765` → `pages/PublicSubscriptionCheckout.tsx` |
| Cobrar parcela de contrato | Contratos → contrato → aba "Financeiro" → **"Cobrar online"** | `pages/ContractDetail.tsx:2574`; `pmoc.ts:259-309` |
| Cobrar o saldo | Financeiro → Contas a Pagar/Receber → "A Receber" → **"Cobrar o saldo"** | `components/financial/FinanceContas.tsx:1661`; `finance.ts:270-310` |
| Cobrar de orçamento / OS | Orçamentos (cobrança do orçamento) e "Faturar" da OS → "Gerar cobrança" | `pages/Quotes.tsx:999-1001`; `components/quotes/QuoteViewDialog.tsx:134`; `OsBillingDialog.tsx:188` |
| Ficha do cliente | Abas "Financeiro" e "Cobranças" (editar, excluir, cobrar) | Changelog 1.24.19/1.24.57 `:3141,4070` |

Sem o módulo, "Cobranças" some do menu e a rota volta para a Visão Geral (`components/layout/SidebarMenuContent.tsx:180`;
`pages/Finance.tsx:112-116`). Com o módulo e sem conta ativa, a tela mostra **"Ative os recebimentos primeiro"** / "Para
cobrar seus clientes online, ative a integração de recebimentos em Configurações, Integrações." + **"Ir para Integrações"**
(ch `:150-154`; `FinanceRelatorio.tsx:141-157`).

---

## 2. Permissões e módulos

| Item | Regra | Fonte |
|---|---|---|
| 🔒 Add-on `cobrancas` "Cobranças online" | Sem ele: item do menu some; em Integrações, card **"Recebimentos não contratado"** / "Este recurso não está incluído no seu plano atual. Fale com nosso time…" | `ModuleGateModal.tsx:133-136`; `SettingsAsaasContent.tsx:345-358`; st `:1530-1533` |
| Ativar/desativar recebimentos | Edge privilegiada: Bearer + módulo `cobrancas` + `can_manage_system`; `company_id` sempre do perfil | `supabase/functions/tenant-asaas-provision/index.ts:3-9` |
| Tela Cobranças | `screen:finance` (mesma do Financeiro) | `SidebarMenuContent.tsx:180` |
| Gerar cobrança em parcelas / no lançamento | `canManagePayments` + módulo + conta ativa | `components/financial/ContaFormDialog.tsx:175-182` |
| Editar/excluir cobrança | Só "A receber"/"Vencido"; estornar só paga, com id do Asaas e não "recebida em dinheiro" | `lib/tenantChargeRules.ts:26-40`; `lib/chargeRowActions.ts:53-71` |
| Cartão recorrente / Pix Automático na assinatura | Chaves `card_recurring_enabled` / `pix_auto_enabled` da conta | `SubscriptionDialog.tsx:182-202`; `hooks/useTenantPaymentAccount.ts:281-283` |

---

## 3. Por tela

### 3.1 Integrações → Cobranças (Asaas) → Configurações (`SettingsAsaasContent.tsx:370-1043`; st `:1528-1672`)

- Cabeçalho com o logo do Asaas, título **"Recebimentos (Asaas)"** / "Cobre seus clientes por Pix, boleto e cartão usando sua
  própria conta Asaas." e selo de status **"Ativo"**, **"Em verificação"**, **"Desativado"**, **"Recusado"** (`:361-366,376-383`).
- **Sem conta ativa** (`:404-462`): "Cole a chave de API da sua conta Asaas para ativar os recebimentos. Você gera essa chave
  no painel da Asaas, em Configurações, Integrações."; **"Chave de API da Asaas"** ("Cole aqui sua chave de API");
  **"Ativar recebimentos"** ("Ativando…"); guia recolhível **"Como consigo minha chave de API da Asaas?"** com 4 passos e a
  dica do sandbox (st `:1551-1559`). Sucesso: toast **"Recebimentos ativados!"** (`:293-295`; st `:1679`); erro: título do
  card + mensagem do servidor ou "Não foi possível ativar os recebimentos. Confira a chave e tente novamente." (st `:1675`).
- **Com conta ativa** (`:471-1015`):
  - Aviso **"Recebimentos ativos. Já é possível cobrar seus clientes."** (ou, em verificação, "Sua conta está em verificação
    na Asaas…") (st `:1562-1563`).
  - Pendência **"Falta escolher a conta que recebe o dinheiro"** / "Enquanto você não escolher, as cobranças pagas não entram
    sozinhas no seu Financeiro." + **"Escolher agora"**; sem conta bancária: "Você ainda não tem conta bancária cadastrada" +
    "Abrir o Financeiro" (st `:1600-1605`; `SettingsAsaasContent.tsx:233,487`).
  - **"Taxas da Asaas"** (`AsaasFeesCard`): "Pix", "Boleto", "Cartão de crédito" com faixas "À vista (1x)", "2 a 6x", "7 a
    12x", "13 a 21x", "Antecipação", "Prazo para o dinheiro cair"; procedência "Taxas da sua conta Asaas, atualizadas em…",
    "Taxas de referência, não conseguimos ler as da sua conta agora."; nota "As taxas são cobradas pela Asaas diretamente
    na sua conta. A Dominex não retém nada por transação."; **"Atualizar taxas"** → "Taxas atualizadas com a Asaas." (st `:1564-1597`).
  - Interruptores **"Lançar cobranças no Financeiro automaticamente"** ("Cada cobrança vira um "a receber" que baixa sozinho
    quando o cliente paga.") e **"Lançar a taxa da Asaas como despesa"** (toasts "Lançamento automático ativado." etc.) (st `:1612-1621`).
  - **"Multa e juros por atraso"**: "Multa por atraso (%)", "Juros ao mês (%)" ("O limite máximo da Asaas é 10% ao mês."),
    "Salvar" → "Multa e juros atualizados." (st `:1622-1630`).
  - **"Preferências de cobrança"**: "Vencimento padrão" (dias), "Descrição/instrução padrão", **"Meios de pagamento
    habilitados"** ("Pix", "Boleto", "Cartão de crédito"), "Máximo de parcelas (cartão)", "Salvar" → "Preferências de
    cobrança salvas." (st `:1634-1646`).
  - **"Desconto por antecipação"**: "Desconto (%)", "Até X dias antes" ("Deixe em branco para não aplicar desconto.") (st `:1648-1656`).
  - **"Lançamento no Financeiro"**: **"Conta bancária de destino"**, **"Categoria da receita"**, **"Categoria da taxa (Asaas)"**,
    "Salvar" → "Configuração de lançamento salva." (st `:1658-1666`).
  - **"Desativar recebimentos"** → "Desativar recebimentos?" / "Cobranças já geradas continuam válidas, mas você não poderá
    criar novas até reativar." → "Sim, desativar" (st `:1610,1668-1672`).

### 3.2 Simulador (`SettingsAsaasSimulator.tsx`; st `:1481-1527`)

- **"Simulador de venda"** / "Veja quanto sobra de uma venda depois da taxa da Asaas e quando o dinheiro cai na sua conta.".
- Campos "Valor da venda", "Forma de pagamento" ("Pix", "Boleto", "Cartão"), "Parcelas" ("nx"), "Quem paga a taxa" ("A empresa
  absorve"/"Repassar ao cliente"), "Antecipar o recebimento".
- Resultado: **"Resultado da simulação"** ("Valor bruto", "O cliente paga", "Taxa da Asaas", **"Valor líquido na sua conta"**,
  "Cada parcela para o cliente", "Custo da antecipação"), **"Com e sem antecipação"**, **"Quando o dinheiro cai na sua conta"**
  ("na hora", "em 1 dia útil (data)", "em n dias (data)"), "Estimativa. O valor final é calculado pela Asaas no momento da
  cobrança.". Vazio: "Digite o valor da venda para ver a simulação.". Sem conta: "Sua conta Asaas ainda não está conectada".

### 3.3 Financeiro → Cobranças, aba "Cobranças" (`FinanceCobrancas.tsx`; ch `:12-143`)

- Botão **"Nova cobrança"**; faixa de totais **"A receber"**, **"Recebido"**, **"Vencido"** (`:242-244`).
- Busca "Buscar por cliente, telefone ou documento…", filtros "Todos", "A receber", "Pago", "Vencido", "Estornado", "Período".
- Colunas "Cliente", "Valor", "Status", "Vencimento", "Forma" ("Pix", "Boleto", "Cartão", "Cliente escolhe"), "Ações".
- Ações por linha (`lib/chargeRowActions.ts:53-71`): **"Copiar link"** ("Link copiado!"), WhatsApp, abrir checkout; com status
  a receber/vencido também **"Editar"** ("Editar cobrança": "Valor", "Vencimento", "Descrição", "Salvar alterações") e
  **"Excluir"** ("Excluir cobrança?" / "Ao excluir, o link de pagamento desta cobrança deixa de funcionar para o cliente…");
  paga: **"Estornar"** ("Estornar cobrança?" / "Ao estornar, o valor será devolvido ao pagador…" → "Estorno solicitado com
  sucesso.") (ch `:44-87`).
- Seleção múltipla → **"Excluir selecionadas"** (ch `:104-122`). Vazio: **"Nenhuma cobrança"** / "Gere a primeira cobrança e
  envie o link de pagamento para o seu cliente." (ch `:139-142`).
- Status vindos do Asaas e como aparecem (`utils/tenantChargeStatus.ts`): RECEIVED/CONFIRMED/RECEIVED_IN_CASH → "Pago";
  PENDING/AWAITING_PAYMENT… → "A receber"; OVERDUE → "Vencido"; REFUNDED/CHARGEBACK… → "Estornado"; outros → "Outro".

### 3.4 Nova cobrança (`ChargeDialog.tsx`; ch `:146-381`)

- Título **"Nova cobrança"** / "Gere um link de pagamento para enviar ao seu cliente.". Abas (`:1149-1168`):
  - **"Cobrança"**: **"Cliente"** ("Selecione o cliente"; criar na hora "Novo cliente" com "Nome", "CPF / CNPJ"…, ch `:235-253`),
    "Ordem de serviço" ("Vincular a uma OS (opcional)"), **"Valor"**, **"Vencimento"** (dica: "Esta é a data em que o cliente deve
    pagar. Para o Regime de Competência, a receita entra em {data}, o dia de hoje…"), **"Descrição"** ("Ex.: Manutenção do
    ar-condicionado").
  - **"Pagamento"**: **"Forma de pagamento"** ("Pix", "Boleto", "Pix e boleto", "Cartão de crédito", "Cliente escolhe"); no
    cartão "Parcelas" ("1x (à vista)"…), "Juros de parcelamento (% ao mês)", **"Quem paga a taxa do cartão?"** "Empresa"/"Cliente".
  - **"Encargos"**: "Opções avançadas": "Multa (%)" ou "Multa (R$)", "Juros ao mês (%)", "Desconto (%)", "Desconto até X dias
    antes do vencimento".
  - **"Financeiro"** (some quando a cobrança é de parcela de contrato ou do saldo de uma conta): **"Lançar no financeiro"**
    "Sim"/"Não" ("Ao gerar, esta cobrança já entra como uma conta a receber no seu financeiro."), "Categoria", centro de custo.
- Sempre visível: **"Resumo do recebimento"** ("Valor da cobrança", "Cliente paga", "Taxa da Asaas", **"Você recebe"**, "O dinheiro
  cai na conta…", "Quanto o cliente paga" com cenários de atraso, "Estimativa…") (ch `:270-333`).
- Rodapé (`:1099-1134`): "Cancelar", **"Gerar agora"** (atalho em qualquer aba antes da última), **"Avançar"** e, na última,
  **"Gerar cobrança"** ("Gerando…"). Validações "Selecione um cliente.", "Informe um valor maior que zero.", "Informe o vencimento.".
- Cliente sem documento: aviso + **"Completar cadastro"** e botão de gerar desligado (`:1107,1116`; ch `:335-341`).
- Sucesso (`:688`; ch `:352-362`): toast **"Cobrança gerada"** / "Copie o link ou envie direto pelo WhatsApp."; quadro com QR
  ("Aponte a câmera para pagar"), **"Link de pagamento"**, **"Copiar link"**, **"Enviar por WhatsApp"** (mensagem pronta
  "Olá! Segue o link para pagamento de *R$ …*…", ch `:364`), **"Nova cobrança"**, "Fechar".
- Variante de contrato: "Esta cobrança é da parcela do contrato. Quando o cliente pagar, a parcela é baixada automaticamente
  no seu financeiro, sem lançamento novo." + "O valor é o da parcela e não pode ser alterado." (ch `:195-199`).

### 3.5 Checkout público `/pagar/<código>` (`pages/PublicCheckout.tsx`; ch `:384-462`)

- Layout em 2 colunas: resumo com a marca da empresa (nome, logo, cor; endereço/telefone/e-mail/CNPJ conforme as chaves
  "mostrar nos documentos", `supabase/functions/get-tenant-payment-checkout/index.ts:107-169`) e **"Pagamento"** / "Escolha a
  forma de pagamento para finalizar.".
- "Valor a pagar", "Vencimento", "Descrição"; formas **"Pix"** ("Aprovação na hora"), **"Boleto"** ("1 a 2 dias úteis"),
  **"Cartão"** ("Aprovação imediata") (ch `:440-453`; `:656`).
- Pix: "Pague com Pix", QR (`BrandedQRCode`, `:690`), **"Copiar código Pix"** → "Código copiado!" (`:678-709`). Boleto: "Abrir
  boleto" (nova aba) + "O boleto abre em uma nova aba…" (`:742`). Cartão: formulário próprio "Pagamento com cartão", "Pagar
  R$ …", "Cobrança única…", "Pagamento aprovado!" / "Estamos confirmando com o banco. Esta página atualiza sozinha em
  instantes." (ch `:421-438`; `:760`).
- Estados: "Carregando cobrança…", **"Cobrança não encontrada"** (`:448`), **"Pagamento confirmado"** / "Recebemos seu
  pagamento. Obrigado!" (`:558-572`), "Aguardando pagamento", "Cobrança vencida", "Cobrança cancelada", "Pagamento estornado",
  "Pagamento indisponível". A página consulta de novo sozinha (`pollMs`, `:149`): muda para "Pagamento confirmado" quando o
  status vira pago. Rodapé "Conexão segura" / "Pagamento processado com segurança por" (Asaas).

### 3.6 Aba "Assinaturas" (`FinanceAssinaturas.tsx`; ch `:465-697`)

- Topo **"Receita recorrente mensal (MRR)"** / "n assinaturas ativas" (ch `:590-593`; cálculo `:85`); **"Nova assinatura"**.
- Colunas "Cliente", "Valor", "Frequência", "Próx. vencimento", "Forma", "Status" ("Ativa", "Vencida", "Cancelada", "Pausada",
  "Pendente"), "Ações" ("Cancelar", "Editar", "Excluir", "Arquivar", "Desarquivar", "Cancelar de novo").
- Canceladas escondidas por padrão: "Mostrar canceladas (n)" / "Ocultar canceladas"; "Ver arquivadas" (ch `:681-693`;
  `FinanceAssinaturas.tsx:629-648`). Vazio **"Nenhuma assinatura"** / "Crie a primeira assinatura recorrente do seu cliente.".
- "Cancelar assinatura": "Ao cancelar, as próximas cobranças desta assinatura deixam de ser geradas na Asaas. O histórico…
  continua disponível no Financeiro. Esta ação não pode ser desfeita." → "Cancelar assinatura" / "Voltar" (ch `:618-623`).
  "Excluir assinatura sem pagamentos" só sem cobrança paga (RPC `get_tenant_subscription_delete_capabilities`). "Editar
  assinatura": "O cliente não pode ser trocado depois que a recorrência é criada." (ch `:631-637`).

### 3.7 Nova assinatura (`SubscriptionDialog.tsx`; ch `:465-589`)

- **"Nova assinatura"** / "Configure uma cobrança recorrente para o seu cliente.". Campos **"Cliente"**, **"Valor"**,
  **"Frequência"** ("Semanal", "Quinzenal", "Mensal", "Trimestral", "Semestral", "Anual"), **"Forma de pagamento"** ("Cliente
  escolhe", "Pix", "Boleto"; e, com as chaves ligadas, "Cartão de crédito (recorrente)" e "Pix Automático"), **"1º vencimento"**,
  **"Duração"** ("Contínua" — "A assinatura segue gerando cobranças até você cancelar." — ou "Número de ciclos" → "Quantas
  cobranças no total"), **"Descrição"** ("Ex.: Contrato de manutenção mensal"), "Categoria", "Opções avançadas" (multa, juros).
- **"Resumo por cobrança"** ("Valores de UMA cobrança (Mensal), não o total da assinatura."). **"Criar assinatura"** →
  toast **"Assinatura criada"** / "A assinatura recorrente foi configurada." (`hooks/useTenantSubscriptions.ts:362-366`).
- Cartão recorrente e Pix Automático geram **"Link de checkout criado"** com "Copiar link"/"Abrir checkout" (ch `:564-575`).

### 3.8 Cobrar parcela de contrato e saldo (`pmoc.ts:259-309`; `finance.ts:270-310`)

- Contrato → "Financeiro" → parcela → **"Cobrar online"** (ou **"Ver cobrança"** e selo "Cobrança gerada"); bloqueios "Parcela
  já recebida.", "Vincule um cliente ao contrato para cobrar online."… Em lote: marcar parcelas → "Cobrar online" → "Gerar n
  cobranças online?" / "Total de R$ … O cliente escolhe a forma de pagamento no próprio link." → "Gerar n cobranças".
- Conta a receber → **"Cobrar o saldo"**, **"Substituir a cobrança"**, **"Ver cobrança"**; selos "Cobrança em aberto",
  "Cobrança vencida", "Cobrança paga", "Cobrança encerrada"; após receber à mão: "E a cobrança online?" com "Cobrar só o que
  falta", "Encerrar a cobrança", "Deixar como está".

---

## 4. Backend por tela (o que o Asaas simulado precisa responder)

### 4.1 Chamadas

| Onde | Chamada | Fonte |
|---|---|---|
| Ler a conta | `GET tenant_payment_accounts?select=id,…,card_recurring_enabled,pix_auto_enabled…` | `hooks/useTenantPaymentAccount.ts:109-113` |
| Ativar / desativar | Edge `tenant-asaas-provision` `{action:'activate', api_key}` / `{action:'deactivate'}` → `{status}` ou `{error}` | `useTenantPaymentAccount.ts:121-147` |
| Interruptores e preferências | `PATCH tenant_payment_accounts` (`auto_post_to_finance`, `auto_post_fees`, multa/juros, meios, descontos, conta e categorias) | `useTenantPaymentAccount.ts:149-180` |
| Taxas (card, simulador, resumo) | Edge `tenant-asaas-card-fees` → `{card, pix, bankSlip, anticipation, settlementDays, source, extrasSource, feePayerDefault, syncedAt}` | `hooks/useTenantCardFees.ts:46-99` |
| Lista de cobranças | `GET tenant_charges?select=id,company_id,customer_id,value,description,billing_type,status,due_date,payment_date,public_short_code,invoice_url,pix_copy_paste,boleto_url,asaas_payment_id,created_at` | `hooks/useTenantCharges.ts:331-335` |
| Gerar cobrança | Edge `tenant-asaas-create-charge` `{customer_id, value, due_date, billing_type, description, fine_*, interest_percent, discount_*, installment_count, fee_payer, source_type, source_id, category, cost_center_id, post_to_finance}` → `{charge:{id, public_short_code, checkout_url, invoice_url, pix_copy_paste, boleto_url, value, due_date, status}, finance_warning?}`; órfã (HTTP 207) → `{invoice_url, asaas_payment_id, warning}` | `useTenantCharges.ts:85-98,440-490` |
| Editar / excluir / estornar | Edges `tenant-asaas-update-charge`, `tenant-asaas-delete-charge`, `tenant-asaas-refund-charge` | `useTenantCharges.ts:347,381,416` |
| Checkout público | Edge `get-tenant-payment-checkout` `{code}` → `{company:{name, logo_url, primary_color, address_line, phone, email, document}, charge:{value, due_date, description, status, billing_type, invoice_url, pix_copy_paste, boleto_url, public_short_code, allow_card}}` | `hooks/useTenantPaymentCheckout.ts:18-80`; `supabase/functions/get-tenant-payment-checkout/index.ts` |
| Pagar no cartão (checkout) | Edge `tenant-asaas-pay-charge-card` | `pages/PublicCheckout.tsx:22` |
| Assinaturas | `GET tenant_subscriptions`; edges `tenant-asaas-create-subscription` (→ `{subscription, checkout_url?, checkout_kind?}`) e `tenant-asaas-manage-subscription` (editar/cancelar/arquivar); RPC `get_tenant_subscription_delete_capabilities` | `hooks/useTenantSubscriptions.ts:255,283,340-366,566` |
| Checkout da assinatura | Edge `get-tenant-subscription-checkout` | `pages/PublicSubscriptionCheckout.tsx` |
| Aviso do Asaas (baixa) | Edge pública `tenant-asaas-webhook` (header `asaas-access-token`): PAYMENT_RECEIVED/CONFIRMED → `apply_tenant_charge_payment`; OVERDUE; REFUNDED; DELETED; SUBSCRIPTION_* | `supabase/functions/tenant-asaas-webhook/index.ts:1-53,1016-1217` |

### 4.2 Estados que a tela precisa mostrar (contrato para o simulado)

| Estado | Dado | Na tela |
|---|---|---|
| Sem conta | nenhuma linha em `tenant_payment_accounts` | Card com "Chave de API da Asaas" / Cobranças: "Ative os recebimentos primeiro" |
| Ativando ok | provision → `{status:'active'}` e a linha passa a existir | Selo "Ativo", "Recebimentos ativos…", "Falta escolher a conta que recebe o dinheiro" |
| Cobrança criada | `tenant_charges.status = 'PENDING'` + conta a receber em `financial_transactions` (se "Lançar no financeiro" = Sim) | "A receber"; checkout "Aguardando pagamento" |
| Pago | webhook simulado: `status='RECEIVED'`, `payment_date`; receita marcada paga (e despesa da taxa, se ligada) | "Pago", "Recebido" soma; checkout "Pagamento confirmado"; Contas a Receber "Pago" |
| Vencido | `status='OVERDUE'` | "Vencido"; checkout "Cobrança vencida" |
| Estornado | `status='REFUNDED'`, filhas de recebimento apagadas | "Estornado" |

### 4.3 Comparação com o backend falso (`/home/claude/domiflix/rec/fakebase`)

| Item | Hoje | Falta |
|---|---|---|
| `tenant_payment_accounts` | **1 linha ativa** no seed (`seeds/gen-01-tenant.json`): `status "active"`, `auto_post_to_finance true`, multa 2 %, juros 1 %, `default_due_days 3`, meios todos ligados, `default_fee_category "Taxas de cobrança"`, `card_recurring_enabled false`, `pix_auto_enabled false` | Estado inicial sem a linha (para o cap. de conexão); `default_fee_category` = "Tarifas e Taxas" (categoria que existe); chaves de cartão recorrente/Pix Automático **ligadas**, como em produção |
| Edges `tenant-asaas-*`, `get-tenant-payment-checkout` | **Sem handler**: devolvem `{}` com 200 (`rec/fakebase/http/functions.mjs:32-35`) → "Cobrança gerada" não aparece (falta `charge`) e o checkout fica sem dados | Handlers: provision, card-fees (tabela fictícia de referência), create-charge (insere `tenant_charges` + receita a receber; `public_short_code` curto; `pix_copy_paste` fictício), get-tenant-payment-checkout, update/delete/refund, create/manage-subscription |
| Baixa | Não existe webhook no fakebase | Rota de dev (ex.: `POST /__dev/asaas/pay`) ou semente entre capítulos que faça o que o webhook faz (4.2, "Pago") |
| RPC `get_tenant_subscription_delete_capabilities` | Sem handler (devolve `[]`) | Só se mostrar "Excluir" |
| Checkout deslogado | Gravador sempre logado | Mesmo passo do T12 (limpar sessão + `goto`), TRILHA 6 |
| Endereço do link | O app mostra `https://dominex.app/pagar/<código>`; a gravação abre `127.0.0.1:8080/pagar/<código>` e a barra de endereço não aparece no vídeo | Nada (só não mostrar a barra) |
| WhatsApp / boleto | "Enviar por WhatsApp" e "Abrir boleto" abrem nova aba | Só zoom |
| Cliente com documento | Seeds com CNPJ/CPF de dígito válido (Restaurante Sabor da Serra 91.234.505/0001-76, Academia Ponto Forte 91.234.504/0001-21…) | — |

---

## 5. Pegadinhas para roteiro e gravação

**[handoff]** = vale pedir correção ao time do app.

1. **[handoff]** "Ir para Integrações" leva a `/configuracoes/integracoes` → página não encontrada (`FinanceRelatorio.tsx:151`).
   Deveria ser `/configuracoes?tab=integracoes&integration=asaas`.
2. **[handoff]** "Recebimentos não contratado" (concordância) no card sem o módulo e no simulador (st `:1486,1531`).
3. Dois nomes para a mesma coisa: menu "Cobranças", sub-aba "Cobranças (Asaas)", card "Recebimentos (Asaas)", módulo
   "Cobranças online". A fala usa "cobranças" e "a integração com o Asaas".
4. A sub-aba aberta por padrão em "Integrações" é **WhatsApp** (`SettingsWhatsappContent.tsx:142-144`): clicar em "Cobranças
   (Asaas)" na gravação.
5. O seed do fakebase não bate com produção nas chaves de cartão recorrente e Pix Automático (produção: ligadas,
   `supabase/migrations/20260823170000_cobrancas_flags_default_on.sql`); os comentários "feature dormente" do i18n (ch `:538,576`)
   estão velhos (**[handoff]**, limpeza).
6. "Gerar agora" aparece em toda aba antes da última e pula as outras (`ChargeDialog.tsx:1094-1111`): na gravação, usar "Avançar".
7. O valor mínimo das cobranças em lote é R$ 5,00 por cobrança (`finance.ts:864-865`).
8. "Pago" só chega pelo aviso do Asaas; a tela do checkout mostra "Pagamento aprovado!" no cartão antes da baixa. Não dizer
   que o pagamento "já caiu" ao ver o checkout.
9. A assinatura cria a primeira cobrança pelo Asaas; com o simulado, a lista de cobranças só ganha a linha se o handler criar.
10. Cobrança "de parcela de contrato" não tem a aba "Financeiro" (a parcela já é o lançamento) (`ChargeDialog.tsx:1161-1164`).
11. Excluir cobrança apaga o link para o cliente; em conta a receber já baixada, aparece "Atenção ao lançamento no
    financeiro" (ch `:97-102`). Não encenar.
12. O logo do Asaas aparece no card de integração e no rodapé do checkout (marca de terceiro na tela do app; ver plano, decisão 5).

---

## 6. 🚫 Não prometer

- 🚫 Que a Dominex recebe ou repassa o dinheiro: o dinheiro vai direto para a conta Asaas da empresa.
- 🚫 Baixa instantânea só porque o cliente viu a tela de pagamento (a baixa vem do Asaas).
- 🚫 Cobrança online sem CPF/CNPJ do cliente. 🚫 Cobranças sem o add-on.
- 🚫 Editar valor de cobrança já paga ou estornada; trocar o cliente de uma assinatura.
- 🚫 Outro gateway além do Asaas.
- 🚫 Pix Automático e cartão recorrente para quem não tem as opções habilitadas na conta.

---

## 7. Dúvidas em aberto (só rodando)

1. Com a linha em `tenant_payment_accounts` ausente, a aba "Cobranças" mostra "Ative os recebimentos primeiro" e o card pede a
   chave (`status` nulo)? E com `status: 'disabled'`?
2. O QR do resultado da cobrança e do checkout é gerado a partir de `pix_copy_paste` ou do link? (imagem fictícia ou texto)
3. A lista de cobranças atualiza sozinha quando o status muda (sem tempo real), ou só ao recarregar?
4. Depois de ativar, a pendência "Falta escolher a conta que recebe o dinheiro" aparece na hora (depende de haver conta
   bancária elegível, `SettingsAsaasContent.tsx:233`)?
5. O handler simulado de create-charge deve inserir a conta a receber, como faz a edge real? (sim, para a Visão Geral e o T20)

## 8. Termos e pronúncias

| Termo | Na tela | Leitura sugerida |
|---|---|---|
| Asaas | "Recebimentos (Asaas)" | asas (já em uso) |
| Pix | "Pix" | pix |
| MRR | "Receita recorrente mensal (MRR)" | ême-érre-érre (ou só "receita recorrente") |
| API | "Chave de API da Asaas" | a-pê-í |
| 2 a 6x | "2 a 6x" | de duas a seis vezes |
| R$ 450,00 | valores | quatrocentos e cinquenta reais |
| dominex.app/pagar | link | não ler o endereço |
