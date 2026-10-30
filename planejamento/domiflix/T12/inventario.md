# Inventário funcional · T12 — Portal do Cliente, Portal do Contrato e QR Codes (Dominex)

> Base para o roteiro do tutorial "T12 · Portal do Cliente, Portal do Contrato e QR Codes". Levantado em 30/10/2026 contra
> o código publicado `APP_VERSION = "1.38.6"` (`src/config/version.ts:1`), cópia em `/home/claude/domiflix/src-1.38.6`.
> **Análise estática, somente leitura.** "(a confirmar)" = só rodando. Formato do inventário do T3.
> O lado de dentro que o T3 já detalhou (aba "Portal" do cadastro do cliente, QR e etiqueta do equipamento, o portal aberto
> no aparelho) está no inventário do T3, seções 3.4.3, 6.8 e 6.9; aqui só o que o T12 acrescenta ou corrige.

## Como ler

- Caminhos relativos a `src/`, exceto `supabase/...` e `rec/...`. Formato `arquivo:linha`.
- Rótulos entre aspas = texto exato (pt-br). Fontes principais: `lib/i18n/messages/app/customers.ts:378-513` (bloco
  `portal`), `lib/i18n/messages/app/pmoc.ts:130-162` (card do contrato), `:398-406` (regenerar), `:551-692` (página pública
  do contrato), `:700-706` (documentos no portal), `lib/i18n/messages/app/os.ts:15-41,83` (Chamados).
- "Portal do Cliente" = `/portal/<token>` (tabela `customer_portals`, um por cliente). "Portal do Contrato" =
  `/contrato/unidade/<nome-do-contrato>-<código>` (ou o token antigo de 32 caracteres), colunas `public_short_code` e
  `public_pmoc_token` de `contracts`. No PMOC a página se apresenta como "Plano de Manutenção".

---

## 0. Resumo para o roteiro

### 0.1 Capítulos da trilha (v1.22.5) contra o código de hoje

| # | Item da trilha | Situação | O que ajustar |
|---|---|---|---|
| 1 | Portal do Cliente já nasce criado; falta torná-lo público | **Mudou** | Nasce criado **e ativo** para todo cliente (o fakebase imita em `rec/fakebase/hooks/customers.mjs`). Não existe interruptor "público" do cliente: a aba "Portal" tem **"Portal ativo"** e, opcional, **"Exigir senha para entrar"** (T3 3.4.3). Salvar a aba sempre grava `is_public = true` (`supabase/migrations/20261021140000_customer_portal_public_sections.sql:777-783`). |
| 2 | Copiar o link, ligar "Portal público" e testar | **Mudou** | Na ficha do cliente: **"Ações"** → **"Copiar link do portal"** ("Link do portal copiado!") ou **"Abrir portal"** (nova aba) (`pages/CustomerDetail.tsx:752-767`; `customers.ts:160-164`). O interruptor **"Portal Público"** existe, mas no **Portal do Contrato** (`pages/ContractDetail.tsx:388-420`). |
| 3 | O que o cliente enxerga: OS, equipamentos, contratos e cobranças | **Maior** | Menu: **"Ordens de Serviço"**, **"Equipamentos"**, **"Contratos"** (só se houver), **"Cobranças"** (só se houver), **"Notas fiscais"**, **"Documentos"**, cada um ligado ou não em "O que o cliente pode ver" (`pages/CustomerPortal.tsx:1364-1388`). Notas e Documentos vêm desligados. |
| 4 | Chamado pelo portal e onde cai (aba Chamados) | **Maior** | **"Abrir Chamado"** no rodapé do portal vira OS **"Pendente"** com origem portal. Aparece no aviso do Dashboard, em **Ordens de Serviço → "Chamados"**, na coluna **"Chamados do Portal"** do quadro e nas abas "Chamados" do cliente, do equipamento e do contrato (Changelog 1.35.8, 1.37.28, 1.37.30). |
| 5 | QR do equipamento abre o portal filtrado no aparelho | **Bate** | QR = `/portal/<token do cliente>?eq=<id do equipamento>` (`pages/EquipmentDetail.tsx:212-231`); o portal abre em "Equipamentos" já no aparelho (`CustomerPortal.tsx:589,637-638`). O T3 prometeu mostrar isso "em detalhe" no T12 (roteiro do T3, cap. 10). |
| 6 | Portal do Contrato/PMOC: gerar, copiar e testar link e QR da unidade | **Bate, sem "gerar"** | O link nasce sozinho para **todo** contrato, comum ou PMOC (`supabase/migrations/20260611110747_contract_portal_token_generalize.sql:24,37-81`). Card **"Portal do Contrato"** na "Visão Geral" do contrato. **"Imprimir QR Code"** só no PMOC (`ContractDetail.tsx:1804-1820`). |
| 7 | Diferença entre os dois portais | **Conceitual** | Seção 3.12. |

Avisos da trilha:

- ⚠️ "Link certo sem estar público = acesso negado" → vale para o **Portal do Contrato** ("Portal Público" desligado → "Portal
  privado" + "Fazer login"). No Portal do Cliente o equivalente é **"Portal ativo"** desligado → "Acesso Indisponível" /
  "Portal não encontrado." (seção 3.3).
- ⚠️ "Aba Chamados só com o módulo Portal" → **bate** (`CustomerDetail.tsx:630-632`), mas o módulo **Portal do Cliente é gratuito
  e incluído nos planos prontos** desde a 1.28.19 (`supabase/migrations/20261005210000_align_commercial_catalog_pricing_and_customer_portal.sql:35-66`;
  `pages/Changelog.tsx:2302-2315`), exceto o plano **Exceção** (`Changelog.tsx:2151-2156`).
- ⚠️ "Cobranças desde o Essencial" → **mudou**: Cobranças voltou a ser add-on pago (R$ 150/mês, nenhum plano pronto inclui)
  (`supabase/migrations/20261016235900_restaurar_cobrancas_como_addon_pago.sql:1-9`).
- ⚠️ "Link do contrato dentro do portal abre outra página" → **bate**: a linha do contrato é um link para nova aba
  (`CustomerPortal.tsx:1321-1357`).
- 🚫 "Não existe login com senha pro cliente" → **desatualizado**: há **senha opcional por cliente**, que vale nos dois portais
  (`Changelog.tsx:1234-1256,599-611`). 🚫 "Não existe chat" → **continua** (seção 6).

### 0.2 O que mudou desde a 1.22.5 (`pages/Changelog.tsx`)

| Versão | Mudança | Linhas |
|---|---|---|
| 1.28.19 | Portal do Cliente gratuito e obrigatório nos planos | `:2302-2315` |
| 1.31.0 | Plano Exceção sem Portal do Cliente | `:2151-2156` |
| 1.35.8 | Chamados do portal com área própria nas OS, no cliente, no equipamento e no contrato; aviso no painel | `:1643-1649` |
| 1.36.21 | Aba Portal no cadastro do cliente; senha por cliente; escolha do que o portal mostra | `:1234-1256` |
| 1.37.0 | Abrir chamado pelo portal voltou a funcionar (erro em português) | `:1111-1165` |
| 1.37.22 | Notas fiscais e Documentos no portal | `:757-768` |
| 1.37.28 / 1.37.30 | Coluna "Chamados do Portal" no quadro, só quando há pedido sem data | `:645-657,621-627` |
| 1.37.31 | Senha por seção nos dois portais | `:599-611` |
| 1.37.35 | Card do Portal do Contrato reorganizado | `:501-517` |
| 1.37.40 | QR do equipamento sem troca visual | `:416-437` |
| 1.37.47 | Cadastro do cliente conclui a configuração do portal | `:277-283` |

### 0.3 O que mais pode surpreender (detalhes na seção 5)

1. As OS geradas por contrato nascem com status `agendada` e o Portal do Cliente não tem rótulo para ele: o selo aparece como
   "agendada", em minúsculas, na lista de OS e no histórico do equipamento (pegadinha 1, handoff).
2. "Próxima manutenção" nos dois portais vem de um campo antigo: no PMOC mostra a **segunda** visita; no contrato comum,
   "A definir" (pegadinha 2, handoff).
3. Aberto **logado** na empresa, o portal mostra tudo, sem senha e com "Preencher OS". A visão do cliente se grava deslogado.
4. "Regenerar token" troca só o código do QR impresso; o link amigável e o QR da tela continuam valendo; e em contrato comum
   o botão aparece, mas o servidor recusa (pegadinha 3, handoff).

---

## 1. Rotas e navegação

| Tela | Como chegar | Rota / componente |
|---|---|---|
| Configurar o Portal do Cliente | Clientes → ficha → "Ações" → "Editar" → aba **"Portal"** | `components/customers/CustomerPortalSettingsTab.tsx` (T3 3.4.3) |
| Copiar/abrir o link do cliente | Ficha do cliente → **"Ações"** → "Copiar link do portal" / "Abrir portal" | `CustomerDetail.tsx:752-767` |
| Portal do Cliente (público) | Link ou QR | `/portal/:token` (`App.tsx:769`) → `pages/CustomerPortal.tsx`; `?eq=<id>` abre o equipamento |
| Configurar o Portal do Contrato | Gestão → Contratos → contrato → **"Visão Geral"** → card "Portal do Contrato" | `ContractDetail.tsx:1711-1840` |
| Liberar documentos do PMOC | Contrato PMOC → aba **"Documentos"** → card "Documentos no portal do cliente" | `components/pmoc/PmocContractDocsTab.tsx:585-627` |
| Portal do Contrato (público) | Link ou QR da unidade | `/contrato/unidade/:token`, alias `/pmoc/unidade/:token` (`App.tsx:771-773`) → `pages/public/PmocPublicPortal.tsx` |
| Chamados recebidos | Ordens de Serviço → aba **"Chamados"**; aviso do Dashboard → "Ver chamados" | `/ordens-servico?aba=chamados` (`ServiceOrders.tsx:115-117`; `lib/portalCalls.ts:23-27`) |
| Acompanhar OS / relatório (do portal) | Botões dos cartões de OS | `/os-tecnico/<id>?modo=cliente` em nova aba (`App.tsx:742`; `CustomerPortal.tsx:965-1015`) |
| Pagar cobrança (do portal) | "Pagar" na seção Cobranças | `/pagar/<código>` em nova aba (`App.tsx:763`; `components/portal/PortalChargesSection.tsx:118,159`) |

As duas páginas públicas ficam fora do login. A do cliente chama o servidor com o cliente `supabase` normal, que leva a sessão
se houver (`CustomerPortal.tsx:35,302-306`); a do contrato manda `Authorization` quando há sessão
(`utils/pmocPortalApi.ts:125-142`). Por isso quem está logado na empresa vê a versão "membro" (seção 5, pegadinha 4).

---

## 2. Permissões e módulos

| Item | Regra | Fonte |
|---|---|---|
| Módulo `customer_portal` | Grátis nos planos prontos; sem ele ou sem assinatura vigente, o portal mostra "Portal ainda não disponível" e não aceita chamado (nem pelo Portal do Contrato) | `20261021140000_...:126-157,560-582`; `20261021160000_contract_portal_sections_password.sql:343-361`; `CustomerPortal.tsx:316,424` |
| Aba "Chamados" e itens "Copiar link do portal"/"Abrir portal" da ficha | Só com o módulo `customer_portal` | `CustomerDetail.tsx:162,630-632,761,767` |
| Módulo `contracts` ("Gestão de Contratos e PMOC") | Inclui "Portal do Contrato e Portal do PMOC públicos" | `components/ModuleGateModal.tsx:113-116` |
| Módulo `cobrancas` (add-on) | Cobranças online que aparecem nos portais | migração `20261016235900_...:1-9` |
| Editar a aba Portal | Quem edita o cliente (T3 2.1) | T3 |
| Documentos avulsos do cliente | Admin/gestor ou `fn:edit_customer` | `CustomerDetail.tsx:161` |
| "Regenerar token" (botão) | Papéis admin, gestor ou super_admin | `ContractDetail.tsx:363-364` |
| `regenerate_pmoc_token` (servidor) | Só contrato **PMOC** e quem `can_manage_contracts` | `supabase/migrations/20260613120000_can_manage_contracts_pmoc.sql` (função `regenerate_pmoc_token`) |
| "Imprimir QR Code" | Só contrato PMOC (botão e função) | `ContractDetail.tsx:1804-1820`; `supabase/functions/generate-pmoc-qr-pdf/index.ts:133-135` |
| Visitante logado na empresa dona | `viewer_can_fill = true`: vê tudo, ignora senha, ganha "Preencher OS" | `20261021140000_...:159-211`; `CustomerPortal.tsx:342,976-985` |

---

## 3. Por tela

### 3.1 Aba "Portal" do cadastro do cliente (resumo; detalhe no T3 3.4.3)

- Cartões **"Portal do cliente"** ("Portal ativo", "Link do portal" com "Copiar link"/"Abrir portal"), **"Proteção por senha"**
  ("Exigir senha para entrar", "Senha", "Confirmar senha"; mínimo 8 caracteres) e **"O que o cliente pode ver"** (sete
  interruptores: Ordens de serviço, Equipamentos, Contratos, Cobranças, Notas fiscais, Documentos, Abrir chamados).
- Padrões no servidor: tudo ligado, menos Notas fiscais e Documentos
  (`supabase/migrations/20261020120000_customer_portal_documents_and_invoices.sql:270-284`; `hooks/useCustomerPortalSettings.ts:34-42`).
- Com senha ligada cada linha vira **"Oculto"** / **"Sem senha"** / **"Com senha"** (`hooks/useCustomerPortalSettings.ts:21-30`).
- A janela fecha sem salvar em **"Cancelar"** (`components/customers/CustomerFormDialog.tsx:336-341`; `customers.ts:75`).

### 3.2 Ficha do cliente: link, chamados e documentos

- **"Ações"** (`CustomerDetail.tsx:752-780`): **"Copiar link do portal"** → toast **"Link do portal copiado!"**; **"Abrir portal"**
  → nova aba; ambos só aparecem com o módulo e um portal ativo. O link vem de `customer_portals` com `is_active = true`
  (`CustomerDetail.tsx:644-661`).
- Abas (`CustomerDetail.tsx:622-642`): "Geral", "Equipamentos", "Histórico", "Tarefas", "Estoque", **"Chamados"** (com o módulo),
  "Contratos", **"Documentos"**, "Financeiro", "Cobranças".
- "Chamados": OS com `origin = 'portal'` do cliente, dos dois portais (`:609`); título "Chamados do Portal"; vazio "Nenhum
  chamado" / "Nenhum chamado aberto pelo portal do cliente" (`customers.ts:281-284`; `CustomerDetail.tsx:1394-1399`).
- "Documentos" (`components/customers/CustomerDocumentsTab.tsx`): subabas "Notas fiscais" e "Documentos", botões "Adicionar nota
  externa" / "Adicionar documento"; avisos "Documento adicionado", "Arquivo liberado no portal" / "Arquivo ocultado do portal".
  É o que alimenta as seções Notas fiscais e Documentos do portal (tabela `customer_documents`).

### 3.3 Portal do Cliente — estados de entrada (`CustomerPortal.tsx:280-495`)

| Situação (resposta de `get_portal_data`) | O que a pessoa vê |
|---|---|
| Token não existe, **portal inativo** ou cliente excluído (resposta nula) | **"Acesso Indisponível"** / "Portal não encontrado." (falha de rede: "Não foi possível carregar o portal. Tente novamente.") (`:481-495`) |
| Empresa sem assinatura vigente ou sem o módulo | **"Portal ainda não disponível"** / "Este portal ainda não está disponível. Em caso de dúvida, fale com a empresa responsável." (`:424`; `components/portal/PortalUnavailable.tsx`) |
| `is_public = false` e visitante de fora | **"Portal privado"** / "Este portal é restrito e exige que você entre com a conta da empresa." + **"Fazer login"** (`/login?redirect=`) (`:447-475`). Só em portal antigo: salvar a aba Portal liga `is_public`. |
| Senha ligada e nenhuma seção "Sem senha" | Tela cheia **"Portal protegido"** / "Digite a senha fornecida pela empresa para acessar seus dados." → "Senha" → **"Entrar no portal"** (`:427-445`; `components/portal/PortalUnlockCard.tsx:84-118`) |
| Senha ligada com parte livre | Portal abre; seções protegidas com cadeado e **"Conteúdo protegido"** / "Esta parte do portal pede a senha fornecida pela empresa." |
| Nenhuma seção liberada | "A empresa ainda não liberou conteúdos para este portal." (`:1450`) |

Erros da senha: "Senha inválida. Confira e tente novamente."; "Muitas tentativas incorretas. Aguarde 15 minutos e tente
novamente."; "Não foi possível entrar. Tente novamente." (`customers.ts:503-505`). Regras no servidor:
`20261021140000_...:105-215` (função `get_portal_data_before_customer_documents`, envolvida por `get_portal_data` em `:334`).

### 3.4 Portal do Cliente — por dentro (`CustomerPortal.tsx:1364-1617`)

- **Cabeçalho** (`components/portal/PublicPortalShell.tsx`): logo da empresa (com White Label, logo e cor dela), título = **nome
  da empresa**, subtítulo **"Olá, {cliente}"** (`:1401-1406`). À direita: ícone de WhatsApp (abre wa.me em nova aba) e o botão
  **"Falar com a empresa"** com "Ligar", "WhatsApp", "E-mail" (`components/portal/PortalContactButton.tsx:38-125`). Com sessão de
  senha aparece o botão de sair (`:1415-1426`).
- **Menu**: no computador, coluna lateral; no celular, pílulas no topo (`:1364`).
- **"Ordens de Serviço"** (`:880-1030`): busca "Buscar ordens de servico..." (sem acento); cartões com número, selo de status
  ("Pendente", "Em andamento", "A caminho", "Concluída", "Cancelada", `:595-601`), "Agendada: dd/mm/aaaa" ou "Criada: …",
  e botões: **"Acompanhar"** (a caminho/em andamento), **"Avaliar atendimento"** (concluída; depois "Obrigado pela avaliacao!"),
  **"Ver relatório"**; os links abrem `/os-tecnico/<id>?modo=cliente` em nova aba (`:960-1015`). Vazio "Nenhuma ordem de
  serviço encontrada". Ordem: mais nova primeiro (`20261021140000_...:276-297`). Tarefas internas nunca aparecem (`:355-361`).
- **"Equipamentos"**: busca "Buscar equipamentos...", lista com foto e local; detalhe com "Visão geral" (Marca, Modelo,
  Capacidade, campos personalizados visíveis), "Histórico" ("Histórico de OS deste equipamento", "Ver relatório"), "Anexos"
  ("Nenhum anexo disponível" ou "Anexos não disponíveis"), "Voltar para lista" (`customers.ts:404-423`; T3 6.9).
- **"Contratos"** (só com contrato ativo ou pausado, `20261021140000_...:298-309`): linha com o nome, selo **"PMOC"** e
  "Próxima manutenção: dd/mm/aaaa" ou "A definir"; a linha inteira é um link para o Portal do Contrato em **nova aba** (o texto
  "Abrir portal do contrato" é só rótulo de acessibilidade) (`:1321-1357`).
- **"Cobranças"** (só com cobrança online, `tenant_charges`): "Vencimento", status "Pago"/"Pendente"/"Vencido"/"Estornado",
  **"Pagar"** → `/pagar/<código>` em nova aba (`PortalChargesSection.tsx:118-160`).
- **"Notas fiscais"** e **"Documentos"**: NFS-e autorizadas, notas externas, documentos avulsos e anexos de contrato liberados;
  selos "Emitida pelo Dominex", "Anexo de contrato", "Enviada manualmente"; vazios "Nenhuma nota fiscal disponível" /
  "Nenhum documento disponível" (`components/portal/PortalDocumentsSection.tsx:100-140`;
  `20261020120000_...:1-10`). Download pela função `customer-portal-document-download` (`:73`).
- **Rodapé fixo "Abrir Chamado"** quando "Abrir chamados" está ligado (`:1432-1436`).
- Atualiza sozinho quando uma OS do cliente muda (canal em tempo real em `service_orders`, `:400-412`).

### 3.5 Chamado pelo Portal do Cliente (`CustomerPortal.tsx:794-826,1540-1585`)

- Janela **"Abrir Chamado"**: **"Descreva o problema \*"** (placeholder "Descreva o problema que você está enfrentando..."),
  **"Equipamento (opcional)"** ("Selecione...", busca "Buscar equipamento...", opção "Nenhum"), botão **"Enviar Chamado"**
  (`customers.ts:425-436`).
- O botão só envia com 10 caracteres ou mais (`:795`); o servidor aceita até 2.000.
- Sucesso: toast **"Chamado aberto com sucesso!"**, a janela fecha e o portal recarrega com a OS nova no topo. Erros traduzidos:
  "Erro ao abrir chamado" + "Descreva o problema com pelo menos 10 caracteres." ou "Este portal não está aceitando chamados
  agora. Fale com a empresa responsável pela manutenção." (`:812-822`).
- O que nasce (`20261021140000_...:599-607`): OS **`pendente`**, `origin = 'portal'`, `os_type = 'manutencao_corretiva'`, sem data,
  com o equipamento escolhido (o servidor confere se o aparelho é do cliente, `:589-597`). Com senha ligada, só abre com sessão,
  salvo se "Abrir chamados" estiver "Sem senha" (`:548-560`).

### 3.6 Onde o chamado aparece para a empresa

- **Aviso no Dashboard** (`components/dashboard/PortalCallsAlert.tsx:150-200`; `pages/Dashboard.tsx:343`): janela **"Você tem 1
  chamado de cliente aguardando"** (plural "…chamados de cliente aguardando") com **"Ver chamados"** e **"Depois"**
  (`lib/i18n/messages/app/dashboard.ts:99-104`). Aparece uma vez ao abrir o painel, para chamados abertos ainda não vistos; a
  marca de "visto" fica no navegador (`dominex:portal-tickets-seen:<usuário>`, `PortalCallsAlert.tsx:35-56`). Card "Chamados
  abertos" / "Ver todos os chamados" no painel (`dashboard.ts:90-98`; `Dashboard.tsx:405`).
- **Ordens de Serviço → aba "Chamados"** (`components/service-orders/PortalCallsPanel.tsx`): busca "Buscar por chamado, cliente,
  equipamento ou contrato..."; filtros **"Chamados abertos"** / "Todos os chamados" e **"Todos os portais"** / "Portal do
  Cliente" / "Portal do Contrato"; colunas **"OS"**, **"Cliente"** (com o equipamento embaixo), **"Descrição"**, **"Origem"**,
  **"Aberto em"**, **"Status"**, **"Ações"** (olho "Abrir chamado"); vazio "Nenhum chamado recebido" / "Os chamados abertos
  pelos portais aparecerão aqui." (`os.ts:21-41`). "Aberto" = não concluído nem cancelado (`lib/portalCalls.ts:3-15`); origem
  "Portal do Contrato" quando a OS tem contrato (`:17-21`).
- Clicar na linha abre a OS (janela de visualização) com **"Editar"**, que leva ao formulário para marcar data e técnico (T5)
  (`ServiceOrders.tsx:612-630`; `components/service-orders/ServiceOrderViewDialog.tsx:700-701`; `os.ts:388`).
- **Quadro (Kanban)**: primeira coluna **"Chamados do Portal"** só enquanto houver chamado sem data; ao marcar a data, a OS sai
  dela sozinha (`ServiceOrders.tsx:398-416`; `os.ts:83`).
- Abas "Chamados" do **cliente** (`CustomerDetail.tsx:609`), do **equipamento** (só chamados com aquele aparelho,
  `EquipmentDetail.tsx:208-209`) e do **contrato** (`ContractDetail.tsx:570,1636,1648`).

### 3.7 Portal do Contrato — o card na Visão Geral (`ContractDetail.tsx:1711-1840`; `pmoc.ts:130-162`)

- Só aparece quando há link (`publicToken`, `:1713`); sem código ainda: "Link público em geração. Aguarde alguns instantes."
- **"Portal do Contrato"** / "Página pública deste contrato para o cliente final. Aparece no QR Code colado no quadro físico."
- Interruptor **"Portal Público"**: ligado, "Qualquer pessoa com o link vê o portal (somente leitura)."; desligado, "O link exige
  login da sua empresa para abrir." Avisos **"Portal público ativado"** / **"Portal agora exige login"**. Ausente ou nulo conta
  como ligado (`:388-420`).
- **"Quem vê o quê no portal"** / "Escolha o que abre direto e o que pede senha. Assim o mesmo link serve para a portaria e para o
  síndico." Oito seções, cada uma em **"Oculto"**, **"Sem senha"** ou **"Com senha"**: "Visão geral", "Equipamentos",
  "Cronograma", "Ocorrências", "Documentos", "Histórico", "Histórico PMOC", "Cobranças". Grava sozinho a cada clique, sem
  aviso de sucesso (`:440-466`). "A senha é a mesma do Portal do Cliente deste cliente."; sem senha cadastrada, "Com senha" fica
  indisponível com o texto "Este cliente ainda não tem senha no Portal do Cliente..." e o atalho **"Abrir cadastro do cliente"**
  (`:434-438,1748-1761`; `components/contracts/ContractPortalSectionsCard.tsx`). "Ocorrências" também controla o botão de
  chamado da página (oculto = sem botão).
- Link amigável clicável (nova aba) `…/contrato/unidade/<nome>-<código>` (`:369-374,1763-1773`); QR na tela
  (`BrandedQRCode`, `:1783`); **"Copiar link"** → **"Link copiado"** / "Cole onde quiser compartilhar." (`:468-480`).
- **"Imprimir QR Code"** (só PMOC): baixa `pmoc-qr-<nome do contrato>.pdf` gerado pela função `generate-pmoc-qr-pdf`, sem aviso
  de sucesso; erro "Erro ao gerar QR Code" (`:482-525`).
- **"Regenerar token"** (admin/gestor): diálogo **"Regenerar token do Portal Público?"** / "Isso invalida QR Codes já impressos
  deste contrato. Clientes que escanearem o QR antigo verão página de erro." / "Você precisará imprimir e colar um QR Code novo
  no quadro físico da unidade." / "Tem certeza?" → "Cancelar" / "Regenerar token" (`pmoc.ts:398-406`); sucesso "Token
  regenerado" / "O QR Code antigo foi invalidado. Reimprima e cole no quadro." (`hooks/usePmocPortal.ts:95-123`).

### 3.8 Documentos do contrato no portal

- PMOC, aba "Documentos", card **"Documentos no portal do cliente"** com selo **"Oculto"** / **"Liberado"** e o texto "Quando
  liberado, o cliente vê os documentos (Dossiê, Termo, Certificado, Cronograma) no portal público da unidade." Botão **"Liberar
  documentos no portal do cliente"** (vira "Ocultar documentos do portal") (`PmocContractDocsTab.tsx:585-627`; `pmoc.ts:700-706`).
- Aviso **"Documentos liberados no portal"** / "Documentos ocultados do portal" (`hooks/useContracts.ts:3642-3665`); grava
  `contracts.portal_documents_released`.
- Contrato comum: anexos com o interruptor **"Liberar documentos no portal"** / "Quando ativado, os anexos ficam visíveis para o
  cliente no portal público deste contrato." (`components/contracts/ContractAttachmentsSection.tsx:238-256`; `pmoc.ts:447-448`).

### 3.9 Portal do Contrato — página pública (`pages/public/PmocPublicPortal.tsx`; `pmoc.ts:551-692`)

- **Cabeçalho**: título = nome da empresa; subtítulo **"Plano de Manutenção"** (PMOC) ou **"Portal do Contrato"** (`:647,670-675`);
  selo de saúde **"Em dia"** / **"Manutenção pendente"** / **"ATENÇÃO"** com "n pendência(s)" (`:651-658`); "Falar com a empresa".
  Endereço da unidade sob o menu (`:697-705`). O título da aba do navegador é "Plano de Manutenção Preventiva (PMOC)" (`:265-266`).
- **Abas** (`:160-185`): **"Visão Geral"**; **"Equipamentos"** (se houver); **"Cronograma"**; **"Ocorrências"**; **"Documentos"**
  (PMOC ou contrato com anexos liberados); **"Histórico"**; **"Histórico PMOC"** (PMOC com execução registrada); **"Cobranças"**
  (se houver). As marcadas "Oculto" somem; "Com senha" ganham cadeado (`:456-473`).
- **Visão Geral** (`:910-935`): cartões "Plano" (ou "Contrato"), "Frequência", "Próxima manutenção" (ou "Próximo atendimento"),
  "Início do contrato", "Conformidade" ("Conforme Lei Federal 13.589/2018"), "Status"; bloco **"Responsável Técnico"** com
  "Registro:", "CFT/CREA", "Modalidade".
- **Cronograma**: calendário; "Toque em uma manutenção do calendário para ver detalhes."; vazio "Ainda não há manutenções
  registradas para esta unidade." **Ocorrências**: visitas e chamados do contrato com status ("Agendada", "Pendente",
  "A caminho"...); "Acompanhar ao vivo" quando há técnico a caminho (`:1097`); vazio "Ainda não há ocorrências registradas para
  este contrato." (`:1019`). **Documentos**: "Baixar PDF", "Válido até", selos "Vigente"/"Vence em breve"/"Vencido",
  "Assinatura pendente"; vazio "Os documentos desta unidade serão disponibilizados em breve." **Histórico**: vazio "Nenhuma
  manutenção concluída ainda." **Histórico PMOC**: "Prova de cumprimento da Planilha, tarefa por tarefa, em cada visita."
- **Rodapé**: "Próxima ocorrência: dd/mm/aaaa" (`:660-666`), botão **"Abrir chamado nesta unidade"** (`:688`), "Portal atualizado em"
  (`:1912`). Janela do chamado: "Descreva o problema \*" → "Enviar Chamado" (10 a 2.000 caracteres) → "Chamado aberto com
  sucesso!"; nasce OS pendente com o contrato e **sem equipamento** (`20261021160000_...:385-399`).
- **Estados**: "Portal privado" + **"Fazer login"** (`:2019`); **"Portal não encontrado"** / "Este link de QR Code não está mais
  ativo ou pode ter sido renovado. Procure a empresa responsável pela manutenção para obter o link atualizado." + "Ir para o
  Dominex" (`:2051`); "Não foi possível carregar" / "Tentar novamente"; "A empresa ainda não liberou conteúdos neste portal."
  (`:710`); senha: o mesmo `PortalUnlockCard` com `contract_portal_login` (`:391,718,838`).

### 3.10 QR Codes

| QR | Onde se pega | Para onde leva | Fonte |
|---|---|---|---|
| Equipamento | Ficha do equipamento: QR, "Baixar QR (PNG)", "Abrir link", "Copiar link", "Gerar Etiqueta" (T3 6.8) | `/portal/<token do cliente>?eq=<equipamento>` (sem portal ativo, vira o texto `EQ-<identificador>`) | `EquipmentDetail.tsx:212-231` |
| Unidade (na tela) | Card "Portal do Contrato" | Link amigável `/contrato/unidade/<nome>-<código>` | `ContractDetail.tsx:369-374,1783` |
| Unidade (impresso) | "Imprimir QR Code" (PDF) | Link com o token de 32 caracteres `/contrato/unidade/<token>` | `generate-pmoc-qr-pdf/index.ts:30,176` |
| Portal do Cliente | Não há QR próprio na ficha do cliente; vai o link | — | `CustomerDetail.tsx:752-767` |

O PDF do "Imprimir QR Code" (página única, `generate-pmoc-qr-pdf/index.ts:196-360`): nome da empresa, título "PMOC — Plano de
Manutenção, Operação e Controle", nome do cliente, endereço, o QR, "Escaneie para acompanhar o PMOC desta unidade", o endereço
do link, a linha "Responsável Técnico: <nome> • <CFT/CREA> • <modalidade>" e o selo "Conforme Lei Federal 13.589/2018".
Aparência do QR da tela: `components/BrandedQRCode.tsx` (com White Label usa logo, estilo e cor da empresa).

### 3.11 Avaliação de OS pelo portal

"Avaliar atendimento" (OS concluída) carrega `get_public_os` e abre a mesma pesquisa do link público (`OSRatingSurvey`, textos em
`os.ts` bloco `nps`); envio por `submit_public_os_rating` (`CustomerPortal.tsx:829-870,1587-1603`;
`hooks/useServiceRatings.ts:86-91`). Assunto do NPS (T5/T7): no T12 só citar.

### 3.12 Qual portal mandar (base para a fala)

| | Portal do Cliente | Portal do Contrato |
|---|---|---|
| Escopo | Toda a relação com o cliente | Uma unidade / um contrato |
| Conteúdo | OS, equipamentos, contratos, cobranças, notas, documentos | Visão geral, equipamentos, cronograma, ocorrências, documentos e histórico do PMOC, cobranças |
| Público típico | Dono ou gestor do cliente | Portaria, síndico, fiscalização (QR no quadro) |
| Acesso | "Portal ativo" + senha opcional, seção por seção | "Portal Público" + "Quem vê o quê", com a mesma senha |
| Chamado | "Abrir Chamado" (escolhe o equipamento) | "Abrir chamado nesta unidade" (vai para o contrato) |
| Ligação entre eles | Seção "Contratos" leva ao Portal do Contrato | — |

---

## 4. Backend por tela

### 4.1 Chamadas

| Onde | Chamada | Fonte |
|---|---|---|
| Ficha do cliente | `GET customer_portals?select=token&customer_id=eq.<id>&is_active=eq.true` | `CustomerDetail.tsx:644-661` |
| Ficha do equipamento | idem pelo cliente do equipamento | `EquipmentDetail.tsx:212-226` |
| Aba Portal | RPCs `get_customer_portal_settings` / `save_customer_portal_settings` | T3 |
| Portal do Cliente | `POST /rest/v1/rpc/get_portal_data` `{ p_token, p_session_token }` | `CustomerPortal.tsx:302-306` |
| Senha | RPC `customer_portal_login` / `contract_portal_login` `{ p_token, p_password }` → `{ ok, session_token }` ou `{ ok: false, error }` | `PortalUnlockCard.tsx:92-100` |
| Chamado (cliente) | RPC `create_customer_portal_ticket` `{ p_token, p_session_token, p_description, p_equipment_id }` | `utils/customerPortalApi.ts:40-54` |
| Avaliar | RPCs `get_public_os` `{ p_os_id }` e `submit_public_os_rating` | `CustomerPortal.tsx:835`; `useServiceRatings.ts:91` |
| Documentos do portal | Função `customer-portal-document-download` `{ portalToken, sessionToken, documentId }` | `PortalDocumentsSection.tsx:73-77` |
| Tempo real | Canal `portal-os`, `postgres_changes` em `service_orders` filtrado por cliente | `CustomerPortal.tsx:400-412` |
| Card do contrato | `GET contracts?select=public_pmoc_token,public_short_code,name`; `PATCH contracts` (`portal_is_public`, `portal_sections`); RPC `regenerate_pmoc_token`; `GET /functions/v1/generate-pmoc-qr-pdf?contract_id=` (PDF) | `hooks/usePmocPortal.ts:25-49,95-105`; `ContractDetail.tsx:399-403,453-458,492-498` |
| Senha do dono (card) | RPC `get_customer_portal_settings` do cliente do contrato | `ContractDetail.tsx:437-438` |
| Liberar documentos | `PATCH contracts` `portal_documents_released` | `hooks/useContracts.ts:3642-3650` |
| Portal do Contrato | `GET /functions/v1/pmoc-portal-share?token=<token ou nome-código>` com `apikey`, `Authorization` (se logado) e `X-Portal-Session` (se houver senha); 400/404 = não encontrado; 200 com `{ error: 'module_unavailable' }`, `{ access: 'denied' }`, `{ access: 'password_required' }` ou o payload | `utils/pmocPortalApi.ts:117-206` |
| Chamado (contrato) | RPC `create_contract_portal_ticket` `{ p_token, p_description, p_session_token }` | `utils/pmocPortalApi.ts:233-248` |
| Dashboard e Chamados | `service_orders` já carregadas (filtro `origin = 'portal'`) | `hooks/useDashboardStats.ts:35-38`; `PortalCallsPanel.tsx:50-65` |

### 4.2 O que o `get_portal_data` precisa devolver (para um handler do fakebase)

- Nulo se o token não existe, o portal está inativo ou o cliente foi excluído (`20261021140000_...:105-125`).
- `{ access: 'module_unavailable', company_name }` sem assinatura vigente ou sem o módulo (`:126-157`); `{ access: 'denied' }`
  se `is_public` falso e visitante de fora (`:166-168`); `{ access: 'password_required' }` com senha e nada livre (`:196-207`).
- Senão `{ access: 'granted', viewer_can_fill, partial, locked_sections, permissions, customer {id,name}, company_settings {name,
  logo_url, phone, email, address, city, state, white_label_*, language, currency, timezone}, equipment_field_config,
  equipment[{..., category {name,color}, custom_fields, attachments_public, attachments}], service_orders[{id, order_number,
  status, description, scheduled_date, created_at, os_type, equipment_id, entry_type, service_type_name, technician_name
  (primeiro nome), team_name}] (sem `tarefa`, mais nova primeiro), contracts[{id, name, is_pmoc, status,
  next_maintenance_date, public_short_code, public_pmoc_token}] (ativo/pausado), charges[...] }` (`:209-325`), mais `invoices` e
  `documents` do invólucro (`:334-495`).
- Permissões com padrão: tudo `true`, menos `invoices` e `documents` (`20261020120000_...:270-284`); os seeds trazem `{}`.

### 4.3 O que o `pmoc-portal-share` precisa devolver

Payload `types/pmocPortal.ts:323-438` (versão 1.4.0): `generated_at`, `payload_version`, `access`, `viewer_can_fill`, `is_pmoc`,
`unit` (nome, endereço), `contract` (nome, `start_date`, `frequency_label`, `next_maintenance_date`, `compliance_text`,
`status_label`, `health_status`, `overdue_count`; `supabase/functions/pmoc-portal-share/index.ts:1422-1459`),
`responsible_technician`, `tenant` (nome, telefone, e-mail, logo, cores), `schedule`, `history`, `occurrences`,
`documents_released`, `documents`, `execution_history`, `attachments_released`, `attachments`, `equipment`,
`equipment_field_config`, `charges`, `partial`, `locked_sections`, `hidden_sections`. A função aceita o token de 32 caracteres
ou o nome com o código curto no fim (`index.ts:42-46,244-256`).

### 4.4 Comparação com o backend falso (`/home/claude/domiflix/rec/fakebase`)

| Item | Hoje | Falta |
|---|---|---|
| `customer_portals` (1 por cliente, ativo, público, sem senha) e RPCs de configuração | **Coberto** (`hooks/customers.mjs`; `handlers/rpc/get_customer_portal_settings.mjs`, `save_customer_portal_settings.mjs`; 12 portais no seed e 4 do T3) | Senha de verdade (o handler só marca "configurada") |
| RPC `get_portal_data` | **Sem handler**: devolve nulo (`core/schema.mjs:80-95`) → a página mostra "Acesso Indisponível" | Handler com 4.2, lendo do store |
| RPC `create_customer_portal_ticket` | **Sem handler**: devolve nulo com 200, o app mostra "Chamado aberto com sucesso!" **sem criar a OS** | Handler: insert em `service_orders` (pendente, `origin: 'portal'`, sem data, `order_number` do T11) |
| RPCs `customer_portal_login`, `contract_portal_login`, `get_public_os`, `submit_public_os_rating`, `create_contract_portal_ticket`, `regenerate_pmoc_token` | **Sem handler** | Conforme o roteiro (login só se mostrar senha) |
| Função `pmoc-portal-share` | **Sem handler**: devolve `{}` (a confirmar como a página reage) | Handler com 4.3 (o modo "demo" do app, `utils/pmocPortalApi.ts:30-35,254-330`, tem dados de outro mundo e não serve) |
| Funções `generate-pmoc-qr-pdf`, `customer-portal-document-download` | **Sem handler** | Só se o vídeo clicar (download não aparece no vídeo) |
| `contracts.portal_is_public` | Padrão genérico do fakebase = **false** (`core/defaults.mjs:24,64-66`; coluna com DEFAULT em `schema.json`) → card mostraria "O link exige login..." | `TABLE_DEFAULTS.contracts = { portal_is_public: true, portal_sections: {} }` |
| `contracts.public_short_code` | **Coberto** (gerado, `core/defaults.mjs:59-62`) | — |
| `contracts.public_pmoc_token` | Nulo | Hook de 32 hex (já pedido no T11) |
| `contracts.portal_documents_released` | Padrão false (correto) | — |
| Tempo real `service_orders` | `rec/fakebase/http/realtime.mjs` existe | Conferir se o portal recarrega (a confirmar) |
| Visão do cliente deslogada | O gravador sempre abre logado: `openSession` aceita `anonymous`, mas o runner não repassa (`rec/recorder/runner.mjs:683`; `rec/recorder/browser.mjs:112-133`) | Passo `eval` que limpa o `localStorage` + `goto` com `reload: true`, ou opção `anonymous` no runner |
| Nova aba ("Abrir portal", "Abrir link", contrato no portal, PDFs, "Ver relatório") | Não aparece no vídeo (`rec/README.md:147-154`) | `goto` direto na URL pública |
| Downloads ("Imprimir QR Code", "Baixar PDF") | Contexto com `acceptDownloads: false` (`rec/recorder/browser.mjs:131`) | Só mostrar o botão |
| Celular lendo o QR | Viewport fixo 1280×800 (`rec/recorder/browser.mjs:10`) | Ilustração do T3 (`exemplos/dominex-t3/ilustracoes/ilustra_qr.py`) |
| Endereço visível nos links | O app roda em `http://127.0.0.1:8080` (`rec/env.json`): o link do portal e o do contrato mostram esse endereço | Decisão (plano, decisão 4) |

---

## 5. Pegadinhas para roteiro e gravação

**[handoff]** = vale pedir correção ao time do app.

1. **[handoff]** O Portal do Cliente não tem rótulo para `agendada` nem `pausada` (`CustomerPortal.tsx:595-601`) e mostra o valor
   cru (`:914,1145`). Toda OS de contrato nasce `agendada` (`hooks/useContracts.ts:1201`): as 12 visitas do hotel e as 4 do
   colégio aparecem com "agendada" em minúsculas, na lista e no histórico do equipamento. O Portal do Contrato tem "Agendada".
2. **[handoff]** "Próxima manutenção" (Portal do Cliente e Portal do Contrato) e "Próxima ocorrência" (rodapé) usam
   `next_pmoc_generation_date`, que no PMOC é a **segunda** data da série e no contrato comum fica vazio ("A definir")
   (`hooks/useContracts.ts:1990-2037,2212-2216`; `20261021140000_...:301`; `pmoc-portal-share/index.ts:1435-1436`). Com início em
   01/11/2026, o hotel veria "01/12/2026" antes da primeira visita.
3. **[handoff]** "Regenerar token" troca só `public_pmoc_token` (`20260613120000_...`, `UPDATE ... SET public_pmoc_token`); o link
   amigável e o QR da tela usam o código curto e **continuam valendo**, ao contrário do texto do diálogo. O QR impresso usa o
   token (`generate-pmoc-qr-pdf/index.ts:176`) e esse sim é invalidado. Em contrato **comum** o botão aparece, mas o servidor
   recusa (`not_a_pmoc_contract`) e sai o aviso "Não foi possível regenerar".
4. Logado na empresa, os dois portais abrem como "membro" (tudo visível, sem senha, "Preencher OS" nos cartões)
   (`CustomerPortal.tsx:342,976-985`; `PmocPublicPortal.tsx:1114`). Gravar a visão do cliente deslogado.
5. **[handoff]** Textos sem acento visíveis: "Buscar ordens de servico..." (`customers.ts:484`, usado em `CustomerPortal.tsx:885`) e
   "Obrigado pela avaliacao!" (`customers.ts:461`, usado em `:1003`). Outras chaves sem acento do bloco (`rateSend`,
   `rateComment`...) não são usadas (limpeza).
6. O interruptor "Portal Público" é só do contrato. No cliente, desligar "Portal ativo" faz o link responder "Acesso
   Indisponível" / "Portal não encontrado." e some o QR do equipamento (T3 6.8).
7. **[handoff]** "Regenerar token" e "token" são termos técnicos para quem entende "link"/"QR".
8. A linha do contrato no Portal do Cliente não tem botão visível: a linha inteira é o link (nova aba) (`CustomerPortal.tsx:1333-1357`).
9. "Imprimir QR Code" **baixa** o PDF, sem abrir impressão nem aviso de sucesso (`ContractDetail.tsx:505-514`).
10. O chamado aberto pelo Portal do Contrato não tem equipamento: não aparece na aba "Chamados" do equipamento
    (`EquipmentDetail.tsx:208-209`; `20261021160000_...:391-397`).
11. O chamado sem data some da coluna "Chamados do Portal" assim que recebe data (`ServiceOrders.tsx:398-405`); continua na aba
    "Chamados" até ser concluído ou cancelado (`lib/portalCalls.ts:3-15`).
12. O aviso "Você tem 1 chamado de cliente aguardando" abre **uma vez** por carregamento do painel para chamados não vistos; a marca
    fica no `localStorage` do navegador (`PortalCallsAlert.tsx:35-56,152-167`). Em gravação (navegador novo a cada capítulo) ele
    reaparece em toda aula seguinte que abrir o Dashboard enquanto o chamado estiver aberto.
13. "Cobranças" do portal são as cobranças online (`tenant_charges`), não as parcelas do contrato do T11
    (`20261021140000_...:310-325`); sem cobrança online a seção nem aparece.
14. Senha errada repetida bloqueia por 15 minutos ("Muitas tentativas incorretas..."). Trocar a senha encerra as sessões
    abertas (`20261021140000_...:769-775`).
15. A chave `statusBarPmoc` ("Plano de Manutenção, Operação e Controle, Lei 13.589/2018") existe em `pmoc.ts:553` mas não é usada
    na página; a lei aparece no cartão "Conformidade" e no PDF do QR.
16. "Quem vê o quê" grava a cada clique sem aviso; a mudança vale na hora para quem abrir o link.

---

## 6. 🚫 Não prometer

- 🚫 Chat ou resposta ao chamado pelo portal: o chamado vira OS e a conversa segue por telefone/WhatsApp ("Falar com a empresa").
- 🚫 Cliente criar conta própria (e-mail e senha): a senha é **uma por cliente**, definida pela empresa, e serve aos dois portais.
- 🚫 QR próprio do Portal do Cliente na ficha do cliente (só link). 🚫 Pagar as parcelas do contrato pelo portal sem o add-on
  Cobranças (T19).
- 🚫 Portal do Cliente no plano Exceção (`Changelog.tsx:2151-2156`).
- 🚫 "Imprimir QR Code" em contrato comum (só PMOC).
- Tela "demo" do Portal do Contrato (`utils/pmocPortalApi.ts:30-35`): é de desenvolvimento, não recurso para o cliente.

---

## 7. Dúvidas em aberto (só rodando)

1. O portal recarrega sozinho quando o chamado é aberto em outra janela (tempo real no fakebase)?
2. Com senha e algumas seções "Sem senha", como fica o menu com cadeados (vale mostrar)?
3. "Acompanhar ao vivo" no Portal do Contrato depende de OS a caminho e localização (T5/T7): há OS assim no mundo do T12?
4. A Visão Geral do Portal do Contrato mostra a assinatura/carimbo do RT ou só o texto?
5. O selo de saúde fica "Em dia" com as 12 visitas futuras (visão `contract_health_status`, T11)?
6. Se o T5/T7 deixar uma OS concluída do hotel, o cartão mostra "Ver relatório" e "Avaliar atendimento" (confirmar a lista final
   de OS do mundo).

## 8. Termos e pronúncias

| Termo | Na tela | Leitura sugerida |
|---|---|---|
| QR Code | "Imprimir QR Code" | quê-érre côde (já no `config_narracao.json`) |
| PMOC | selo "PMOC" | pê-móqui (testar; T11) |
| Lei 13.589/2018 | "Conforme Lei Federal 13.589/2018" | lei treze mil quinhentos e oitenta e nove, de dois mil e dezoito |
| OS | "OS" | ó-ésse (plural ó-ésses) |
| PDF | "Baixar PDF" | pê-dê-éfe |
| CFT/CREA | "CFT/CREA" | cê-éfe-tê, créa |
| WhatsApp | "WhatsApp" | uatsápi (testar) |
| Link | "Copiar link" | línqui (a fala evita "token" e "URL") |
