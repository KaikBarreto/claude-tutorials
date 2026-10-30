# Inventário funcional · T12 — Portal do Cliente, Portal do Contrato e QR Codes (Dominex)

> Base para o roteiro do tutorial "T12 · Portal do Cliente, Portal do Contrato e QR Codes". Levantado em 30/10/2026 contra
> o código publicado `APP_VERSION = "1.38.6"` (`src/config/version.ts:1`), cópia em `/home/claude/domiflix/src-1.38.6`.
> **Análise estática, somente leitura.** "(a confirmar)" = só rodando. Formato do inventário do T3.
> O lado de dentro (aba "Portal" do cadastro do cliente, QR e etiqueta do equipamento) já está detalhado no inventário do
> T3, seções 3.4.3, 6.8 e 6.9; aqui entram as páginas públicas, os chamados e o Portal do Contrato.

## Como ler

- Caminhos relativos a `src/`, exceto `supabase/...`. Formato `arquivo:linha`.
- Rótulos entre aspas = texto exato (pt-br). Fontes: `lib/i18n/messages/app/customers.ts:378-526` (bloco `portal`) e
  `lib/i18n/messages/app/pmoc.ts:120-176,399-406,551-698` (Portal do Contrato).
- "Portal do Cliente" = `/portal/<token>` (tabela `customer_portals`). "Portal do Contrato" = `/contrato/unidade/<nome>-<código>`
  ou `/contrato/unidade/<token>` (colunas `public_pmoc_token`/`public_short_code` de `contracts`); no PMOC a página se
  apresenta como "Plano de Manutenção".

---

## 0. Resumo para o roteiro

### 0.1 Capítulos da trilha (v1.22.5) contra o código de hoje

| # | Item da trilha | Situação | O que ajustar |
|---|---|---|---|
| 1 | Portal do Cliente já nasce criado; falta torná-lo público | **Mudou** | Nasce criado **e ativo** para todo cliente (gatilho; `rec/fakebase/hooks/customers.mjs` imita). Não existe interruptor "público" para o cliente: a tela tem **"Portal ativo"** e, opcional, **"Exigir senha para entrar"** (aba "Portal" do cadastro, T3 3.4.3). O `is_public` do portal existe no banco mas não aparece na tela. |
| 2 | Copiar o link, ligar "Portal público" e testar | **Mudou** | Copiar: ficha do cliente → "Ações" → **"Copiar link do portal"** ("Link do portal copiado!") ou **"Abrir portal"** (nova aba) (`pages/CustomerDetail.tsx:758-767`). O interruptor **"Portal Público"** existe, mas no **Portal do Contrato** (`pages/ContractDetail.tsx:391-420,1729-1745`). |
| 3 | O que o cliente enxerga: OS, equipamentos, contratos e cobranças | **Maior** | Menu do portal: **"Ordens de Serviço"**, **"Equipamentos"**, **"Contratos"** (se houver), **"Cobranças"** (se houver), **"Notas fiscais"**, **"Documentos"** — cada um ligado ou não em "O que o cliente pode ver" (`pages/CustomerPortal.tsx:1365-1388`). |
| 4 | Chamado pelo portal e onde cai (aba Chamados) | **Maior** | Botão **"Abrir Chamado"** (rodapé do portal). Vira OS **"Pendente"** com origem portal. Aparece em **Ordens de Serviço → aba "Chamados"** e na coluna "Chamados do Portal" do quadro, e nas abas "Chamados" do cliente, do equipamento e do contrato (`pages/ServiceOrders.tsx:115,398-410`; Changelog 1.35.8). |
| 5 | QR do equipamento abre o portal filtrado no aparelho | **Bate** | QR = `/portal/<token>?eq=<id do equipamento>` (`pages/EquipmentDetail.tsx:218-231`); o portal abre em "Equipamentos" já com o aparelho (`CustomerPortal.tsx:589,637-638`). |
| 6 | Portal do Contrato/PMOC: gerar, copiar e testar link e QR da unidade | **Bate, sem "gerar"** | O link nasce sozinho para **todo** contrato (comum ou PMOC) (`supabase/migrations/20260611110747_contract_portal_token_generalize.sql:24,37-81`). Card **"Portal do Contrato"** na Visão Geral do contrato: "Portal Público", QR, "Copiar link", **"Imprimir QR Code"** (baixa PDF), "Regenerar token", **"Quem vê o quê no portal"**. |
| 7 | Diferença entre os dois portais | **Conceitual** | Seção 3.5. |

Avisos da trilha: ⚠️ "link certo sem estar público = acesso negado" → **vale para o Portal do Contrato** ("Portal Público" desligado
→ "Portal privado" + "Fazer login"); no Portal do Cliente o equivalente é "Portal ativo" desligado → "Acesso Indisponível" /
"Portal não encontrado." ⚠️ "aba Chamados do cliente só com o módulo Portal" → o módulo **Portal do Cliente é gratuito e
incluído em todos os planos prontos** desde a 1.28.19 (`supabase/migrations/20261005210000_align_commercial_catalog_pricing_and_customer_portal.sql:1-60`),
exceto o plano **Exceção** (Changelog 1.31.0). ⚠️ "Cobranças desde o Essencial" → **mudou**: **Cobranças** voltou a ser add-on
pago (R$ 150/mês, nenhum plano inclui) (`supabase/migrations/20261016235900_restaurar_cobrancas_como_addon_pago.sql:1-9`).
⚠️ "link do contrato dentro do portal abre outra página" → **bate**: "Abrir portal do contrato" abre em **nova aba**
(`CustomerPortal.tsx:1327-1345`). 🚫 "não existe login com senha pro cliente" → **desatualizado**: existe **senha opcional**
por cliente, usada pelos dois portais (Changelog 1.36.21, 1.37.31). 🚫 "não existe chat" → **continua**: o chamado é de mão única.

### 0.2 O que mudou desde a 1.22.5

| Versão | Mudança (`pages/Changelog.tsx`) |
|---|---|
| 1.28.19 | Portal do Cliente gratuito e incluído em todos os planos (`:2313`). |
| 1.35.8 / 1.37.28-1.37.30 | Chamados do portal com área própria nas OS, no cliente, no equipamento e no contrato; coluna "Chamados do Portal" no quadro (`:1649,656,627`). |
| 1.36.21 | Aba Portal no cadastro do cliente; **senha** por cliente; escolha do que o portal mostra (`:1240-1250`). |
| 1.37.22 | **Notas fiscais** e **Documentos** no portal (`:763-768`). |
| 1.37.31 / 1.37.35 | Senha **por seção** nos dois portais; card do Portal do Contrato reorganizado (`:605-610,517`). |

### 0.3 O que mais pode surpreender (seção 5)

1. Abrir o portal **logado** na empresa mostra o portal como "membro da empresa" (vê tudo, sem senha, e com "Preencher OS"). Para
   gravar a visão do cliente é preciso estar **deslogado**.
2. "Abrir portal" e "Abrir portal do contrato" abrem **nova aba** (o gravador não acompanha).
3. Sem nenhuma seção liberada, o portal mostra "A empresa ainda não liberou conteúdos para este portal."
4. A seção Cobranças do portal mostra cobranças online (Asaas), não as parcelas do contrato.

---

## 1. Rotas e navegação

| Tela | Como chegar | Rota |
|---|---|---|
| Configurar o Portal do Cliente | Clientes → ficha → "Editar" → aba **"Portal"** (T3 3.4.3) | — |
| Copiar/abrir o link do cliente | Ficha do cliente → **"Ações"** → "Copiar link do portal" / "Abrir portal" | — |
| Portal do Cliente (público) | Link ou QR | `/portal/:token` (`App.tsx:769`); `?eq=<id>` abre o equipamento |
| Configurar o Portal do Contrato | Contratos → detalhe → **"Visão Geral"** → card "Portal do Contrato" | — |
| Portal do Contrato (público) | Link ou QR da unidade | `/contrato/unidade/:token` (alias `/pmoc/unidade/:token`) (`App.tsx:771-773`) |
| Chamados recebidos | Ordens de Serviço → aba **"Chamados"** | `/ordens-servico?aba=chamados` (`ServiceOrders.tsx:115`) |

As duas páginas públicas ficam fora do login (sem `ProtectedRoute`). A do cliente chama o servidor com o cliente
`supabase` normal (vai **com a sessão**, se houver) (`CustomerPortal.tsx:35,302-306`); a do contrato manda o token de acesso
da sessão, se houver, para a função `pmoc-portal-share` (`utils/pmocPortalApi.ts:117-160`).

---

## 2. Permissões e módulos

| Item | Regra | Fonte |
|---|---|---|
| Módulo `customer_portal` ("Portal do Cliente") | Grátis e incluído em start/avancado/master; sem ele (ou sem assinatura ativa), o portal mostra "Portal ainda não disponível" | migração `20261005210000_...:1-60`; `20261021140000_customer_portal_public_sections.sql:126-157`; `components/portal/PortalUnavailable.tsx` |
| Módulo `contracts` | Portal do Contrato faz parte de "Gestão de Contratos e PMOC" | `components/ModuleGateModal.tsx:113-115` |
| Módulo `cobrancas` (add-on) + conta de recebimento | Cobranças online que aparecem no portal | migração `20261016235900_...:1-9` |
| Quem configura | Quem edita o cliente (`fn:edit_customer`) e quem tem a tela Contratos | T3 2.1; T11 2 |
| Visitante logado na empresa | `viewer_can_fill = true`: vê tudo, ignora senha e ganha "Preencher OS" | `20261021140000_...:159-211`; `CustomerPortal.tsx:338` |

---

## 3. Por tela

### 3.1 Portal do Cliente — estados de entrada (`pages/CustomerPortal.tsx:280-480`)

| Situação (servidor `get_portal_data`) | O que a pessoa vê |
|---|---|
| Token não existe ou **portal inativo** (resposta nula) | **"Acesso Indisponível"** / "Portal não encontrado." (erro de rede: "Não foi possível carregar o portal. Tente novamente.") |
| Empresa sem assinatura ativa ou sem o módulo | **"Portal ainda não disponível"** / "Este portal ainda não está disponível. Em caso de dúvida, fale com a empresa responsável." |
| `is_public = false` e visitante de fora | **"Portal privado"** / "Este portal é restrito e exige que você entre com a conta da empresa." + **"Fazer login"** |
| Senha ligada e nada liberado sem senha | Cartão **"Portal protegido"** / "Digite a senha fornecida pela empresa para acessar seus dados." → "Senha" → **"Entrar no portal"**; erros "Senha inválida. Confira e tente novamente." e "Muitas tentativas incorretas. Aguarde 15 minutos e tente novamente." (`components/portal/PortalUnlockCard.tsx:85-115`) |
| Senha ligada com parte liberada | Portal abre; seções protegidas mostram cadeado e **"Conteúdo protegido"** / "Esta parte do portal pede a senha fornecida pela empresa." |

Regras do servidor em `supabase/migrations/20261021140000_customer_portal_public_sections.sql:112-215`.

### 3.2 Portal do Cliente — por dentro (`CustomerPortal.tsx:1365-1617`)

- Cabeçalho (`components/portal/PublicPortalShell.tsx`): logo e cor da empresa (com White Label), título = **nome da empresa**,
  subtítulo **"Olá, {cliente}"**; botão **"Falar com a empresa"** ("Ligar", "WhatsApp", "E-mail") (`components/portal/PortalContactButton.tsx`).
  Computador: menu lateral; celular: pílulas no topo (`CustomerPortal.tsx:1365`).
- Seções (só as liberadas): **"Ordens de Serviço"** (busca "Buscar ordens de servico...", cartões com status Pendente/Em
  andamento/A caminho/Concluída/Cancelada, "Agendada:"/"Criada:", "Acompanhar", "Ver relatório", **"Avaliar atendimento"** nas
  concluídas; as ações abrem `/os-tecnico/<id>?modo=cliente` em nova aba) (`:960-1010`); **"Equipamentos"** (busca "Buscar
  equipamentos...", detalhe com "Visão geral", "Histórico", "Anexos", "Voltar para lista"); **"Contratos"** (só com contrato:
  nome, selo "PMOC", "Próxima manutenção", **"Abrir portal do contrato"** em nova aba); **"Cobranças"** (só com cobrança:
  "Vencimento", "Pagar"); **"Notas fiscais"**; **"Documentos"** (download por função `customer-portal-document-download`).
- Rodapé fixo **"Abrir Chamado"** (se liberado) (`:1432-1438`).
- Tarefas internas da equipe nunca aparecem (filtro no servidor e no navegador, `:351-358`).
- Atualiza sozinho quando uma OS do cliente muda (canal em tempo real, `:395-410`).

### 3.3 Chamado pelo Portal do Cliente

- Janela **"Abrir Chamado"**: **"Descreva o problema \*"** ("Descreva o problema que você está enfrentando..."), **"Equipamento
  (opcional)"** ("Selecione...", busca "Buscar equipamento...", "Nenhum"), botão **"Enviar Chamado"** (`customers.ts:428-437`).
- Mínimo **10 caracteres** ("Descreva o problema com pelo menos 10 caracteres."); servidor aceita até 2.000.
- Sucesso: **"Chamado aberto com sucesso!"**. Portal sem chamados liberados: "Este portal não está aceitando chamados agora. Fale
  com a empresa responsável pela manutenção." (`CustomerPortal.tsx:795-830`).
- O que nasce: **OS** com `status = 'pendente'`, `origin = 'portal'`, `os_type = 'manutencao_corretiva'`, sem data, com o
  equipamento escolhido (`20261021140000_...:560-603`).

### 3.4 Onde o chamado aparece para a empresa

- **Ordens de Serviço → aba "Chamados"**: busca "Buscar por chamado, cliente, equipamento ou contrato...", filtros "Chamados
  abertos"/"Todos os chamados" e "Todos os portais"/"Portal do Cliente"/"Portal do Contrato"; colunas "OS", "Cliente",
  "Descrição"...; vazio "Nenhum chamado recebido" / "Os chamados abertos pelos portais aparecerão aqui." (`lib/i18n/messages/app/os.ts:17,21-36`).
- Quadro de OS: coluna **"Chamados do Portal"** só quando há chamado **sem data**; ao marcar a data a OS segue o fluxo normal
  (`ServiceOrders.tsx:398-410`; Changelog 1.37.30).
- Abas **"Chamados"** na ficha do cliente (vazio "Nenhum chamado"; `CustomerDetail.tsx:1399`), do equipamento e do contrato
  (`ContractDetail.tsx:1636`).

### 3.5 Portal do Contrato — configuração (card na Visão Geral; `ContractDetail.tsx:1700-1840`; `pmoc.ts:136-169`)

- **"Portal do Contrato"** / "Página pública deste contrato para o cliente final. Aparece no QR Code colado no quadro físico."
- Interruptor **"Portal Público"**: ligado (padrão do banco) "Qualquer pessoa com o link vê o portal (somente leitura)."; desligado
  "O link exige login da sua empresa para abrir." Avisos "Portal público ativado" / "Portal agora exige login" (`ContractDetail.tsx:391-420`).
- **"Quem vê o quê no portal"** / "Escolha o que abre direto e o que pede senha. Assim o mesmo link serve para a portaria e para o
  síndico." Para cada seção ("Visão geral", "Equipamentos", "Cronograma", "Ocorrências", "Documentos", "Histórico" ou
  "Histórico PMOC", "Cobranças") três estados: **"Oculto"**, **"Sem senha"**, **"Com senha"**. "A senha é a mesma do Portal do
  Cliente deste cliente."; sem senha cadastrada, "Com senha" fica indisponível com o atalho "Abrir cadastro do cliente"
  (`components/contracts/ContractPortalSectionsCard.tsx`; `ContractDetail.tsx:438,446-470`).
- QR na tela (`BrandedQRCode`) + **"Copiar link"** ("Link copiado" / "Cole onde quiser compartilhar."), **"Imprimir QR Code"**
  (baixa `pmoc-qr-<contrato>.pdf` da função `generate-pmoc-qr-pdf`; erro "Erro ao gerar QR Code"), **"Regenerar token"**
  ("Regenerar token do Portal Público?" / "Isso invalida QR Codes já impressos deste contrato..." → "Regenerar token")
  (`ContractDetail.tsx:482-521`; `pmoc.ts:399-406`).
- Link amigável `…/contrato/unidade/<nome-do-contrato>-<código>` (cai no token antigo se não houver código) (`ContractDetail.tsx:365-376`;
  `utils/pmocPortalApi.ts:477-499`). Sem token ainda: "Link público em geração. Aguarde alguns instantes."
- Documentos do PMOC só aparecem no portal depois de **"Liberar documentos no portal do cliente"** (aba Documentos, T11 3.4);
  anexos de contrato comum: "Liberar documentos no portal".

### 3.6 Portal do Contrato — página pública (`pages/public/PmocPublicPortal.tsx`; `pmoc.ts:551-698`)

- Faixa no topo: **"Plano de Manutenção, Operação e Controle, Lei 13.589/2018"** (PMOC) ou **"Portal do Contrato"**; subtítulo
  "Plano de Manutenção" / "Portal do Contrato" (`:647`).
- Abas (as ocultas somem; `:139,167-183,456-473`): **"Visão Geral"**, **"Equipamentos"** (se houver), **"Cronograma"**,
  **"Ocorrências"**, **"Documentos"** (PMOC ou com anexos), **"Histórico"** / **"Histórico PMOC"**, **"Cobranças"** (se houver).
- Visão Geral: "Plano"/"Contrato", "Frequência", "Próxima manutenção"/"Próximo atendimento", "Início do contrato",
  "Conformidade" ("Em dia", "Manutenção pendente", "ATENÇÃO"), "Status"; bloco **"Responsável Técnico"** ("Registro:",
  "CFT/CREA", "Modalidade").
- Cronograma: "Toque em uma manutenção do calendário para ver detalhes."; vazio "Ainda não há manutenções registradas para esta
  unidade." Documentos: "Baixar PDF", "Válido até", selos "Vigente"/"Vence em breve"/"Vencido", "Assinatura pendente"; vazio
  "Os documentos desta unidade serão disponibilizados em breve."
- Rodapé: **"Abrir chamado nesta unidade"** → "Descreva o problema \*" → "Enviar Chamado" (mínimo 10 caracteres) → OS pendente
  com o contrato (`supabase/migrations/20261021160000_contract_portal_sections_password.sql:391-399`); "Acompanhar ao vivo"
  quando há técnico a caminho (`:1097`); "Portal atualizado em".
- Estados: "Portal privado" + **"Fazer login"** (`:2019`); **"Portal não encontrado"** / "Este link de QR Code não está mais ativo
  ou pode ter sido renovado..." + "Ir para o Dominex" (`:2051`); "Não foi possível carregar" + "Tentar novamente".

### 3.7 QR Codes

| QR | Onde se pega | Para onde leva | Fonte |
|---|---|---|---|
| Equipamento | Ficha do equipamento: QR, "Baixar QR (PNG)", "Gerar Etiqueta" (T3 6.8) | `/portal/<token do cliente>?eq=<equipamento>` (portal do cliente aberto no aparelho) | `EquipmentDetail.tsx:218-231` |
| Unidade do contrato | Card "Portal do Contrato": QR na tela e "Imprimir QR Code" (PDF) | `/contrato/unidade/<nome>-<código>` | `ContractDetail.tsx:365-376,482-521` |
| Portal do Cliente | Não há QR próprio na tela do cliente; o link vai por "Copiar link do portal" | — | `CustomerDetail.tsx:758-767` |

Aparência: `components/BrandedQRCode.tsx` (com White Label usa logo, estilo e cor da empresa; T0).

### 3.8 Qual portal mandar (base para a fala)

| | Portal do Cliente | Portal do Contrato |
|---|---|---|
| Escopo | Toda a relação com o cliente | Uma unidade/contrato |
| Conteúdo | OS, equipamentos, contratos, cobranças, notas, documentos | Visão geral, equipamentos, cronograma, ocorrências, documentos e histórico do PMOC, cobranças |
| Público típico | Dono/gestor do cliente | Portaria, síndico, fiscalização (QR no quadro) |
| Acesso | Ativo/inativo + senha opcional por seção | Público/privado + "Quem vê o quê" com a mesma senha |
| Chamado | "Abrir Chamado" (escolhe equipamento) | "Abrir chamado nesta unidade" (vai para o contrato) |

---

## 4. Backend por tela

### 4.1 Chamadas

| Onde | Chamada | Fonte |
|---|---|---|
| Portal do Cliente | `POST /rest/v1/rpc/get_portal_data` `{ p_token, p_session_token }` → `{ access, viewer_can_fill, partial, locked_sections, permissions, customer, company_settings, equipment, equipment_field_config, service_orders, contracts[{id,name,is_pmoc,status,next_maintenance_date,public_short_code,public_pmoc_token}], charges, invoices, documents }` ou `null` | `CustomerPortal.tsx:161-183,302-361` |
| Senha | `rpc customer_portal_login` / `contract_portal_login` `{ p_token, p_password }` → `{ ok, session_token }` ou `{ ok:false, error:'locked'|... }` | `PortalUnlockCard.tsx:85-115` |
| Chamado (cliente) | `rpc create_customer_portal_ticket` `{ p_token, p_session_token, p_description, p_equipment_id }` | `utils/customerPortalApi.ts:40-55` |
| Avaliar OS | `rpc get_public_os` `{ p_os_id }` (cliente anônimo) | `CustomerPortal.tsx:829-850` |
| Documentos | função `customer-portal-document-download` | `components/portal/PortalDocumentsSection.tsx:73` |
| Portal do Contrato | `GET /functions/v1/pmoc-portal-share?token=<token ou código>&session=...` (com `Authorization` se logado) → payload de `types/pmocPortal.ts:320-430` (`unit`, `contract`, `health`, `responsible_technician`, `tenant`, `schedule`, `history`, `occurrences`, `documents`, `equipment`, `charges`, `hidden_sections`, `locked_sections`...) ou `{ access: 'denied' | 'password_required' }`; 400/404 = não encontrado | `utils/pmocPortalApi.ts:117-232` |
| Chamado (contrato) | `rpc create_contract_portal_ticket` | `utils/pmocPortalApi.ts:233-252` |
| Dentro do app | `get_customer_portal_settings` (cadastro e card do contrato), `PATCH contracts` (`portal_is_public`, `portal_sections`), `rpc regenerate_pmoc_token`, `GET /functions/v1/generate-pmoc-qr-pdf?contract_id=` (blob PDF) | `ContractDetail.tsx:391-521`; `hooks/usePmocPortal.ts:96-120` |

### 4.2 Comparação com o backend falso (`/home/claude/domiflix/rec/fakebase`)

| Item | Hoje | Falta |
|---|---|---|
| `customer_portals` (1 por cliente, ativo, público) e RPCs `get_/save_customer_portal_settings` | **Coberto** (`hooks/customers.mjs`, `handlers/rpc/*_customer_portal_settings.mjs`) | Senha de verdade (`PORTALS_WITH_PASSWORD` só marca "configurada") |
| RPC `get_portal_data` | **Sem handler** → a página pública não monta | Handler com as regras de 3.1 e o payload de 4.1, lido do store (OS sem `tarefa`, equipamentos, contratos, documentos liberados) |
| RPCs `create_customer_portal_ticket`, `customer_portal_login`, `get_public_os` | **Sem handler** | Ticket = insert em `service_orders` (pendente, `origin: 'portal'`, sem data); login só se o vídeo mostrar senha |
| Função `pmoc-portal-share` | **Sem handler** | Handler que monta o payload do contrato (o app tem um modo "demo" com dados próprios — `utils/pmocPortalApi.ts:30-35,254-330` — com nomes de outro mundo, não serve) |
| RPC `create_contract_portal_ticket`, `regenerate_pmoc_token`; funções `generate-pmoc-qr-pdf`, `customer-portal-document-download` | **Sem handler** | Conforme o roteiro |
| `contracts.portal_is_public` | O padrão genérico do fakebase põe **false** (`core/defaults.mjs:24,64-70`): o card mostraria "O link exige login..." | `TABLE_DEFAULTS.contracts = { portal_is_public: true, portal_sections: {} }` + token (T11) |
| Página pública com o navegador **logado** como Camila | O gravador sempre abre logado (`rec/recorder/runner.mjs:683`; `openSession` tem `anonymous`, o runner não repassa) | Opção `"anonymous": true` no roteiro ou passo de setup que sai da conta antes do `goto` |
| Nova aba ("Abrir portal", "Abrir portal do contrato", PDFs) | Não aparece no vídeo (`rec/README.md`, "Limites") | Usar `goto` direto na URL pública |
| Celular (QR lido pelo telefone) | Viewport fixo 1280×800 (`rec/recorder/browser.mjs:10`) | Ilustração (como a do QR no T3) ou viewport de celular no gravador |
| Tempo real do portal (`postgres_changes` em `service_orders`) | `rec/fakebase/http/realtime.mjs` existe | Conferir se o portal recarrega ao criar o chamado (a confirmar) |

---

## 5. Pegadinhas para roteiro e gravação

**[handoff]** = vale pedir correção ao time do app.

1. Logado na empresa, o portal mostra tudo e o botão "Preencher OS" (`CustomerPortal.tsx:338`; servidor `viewer_can_fill`).
   Gravar a visão do cliente **deslogado**.
2. "Abrir portal", "Abrir portal do contrato", "Acompanhar"/"Ver relatório" das OS e os PDFs abrem **nova aba**.
3. Seções "Contratos" e "Cobranças" só aparecem se houver contrato/cobrança (`CustomerPortal.tsx:1373-1382`); "Cobranças" é de
   cobrança online (`tenant_charges`), não das parcelas do contrato (T11).
4. **[handoff]** Textos do portal sem acento: "Enviar avaliacao", "Comentario (opcional)", "Avaliacao ja enviada. Obrigado!",
   "o quanto voce ficou satisfeito", "Buscar ordens de servico..." (`customers.ts:470-481,495`).
5. O interruptor "Portal Público" existe só no contrato; no cliente, desligar "Portal ativo" faz o link responder "Portal não encontrado."
6. **[handoff]** O card do contrato chama de "Regenerar token" e "token" o que o usuário entende como link; texto técnico.
7. "Imprimir QR Code" **baixa** um PDF (não abre impressão) (`ContractDetail.tsx:505-512`); no vídeo não há o que mostrar além
   do botão.
8. O QR do equipamento só aponta para o portal se o cliente tiver portal ativo (T3 6.8).
9. Chamado sem data some da coluna "Chamados do Portal" assim que recebe data (`ServiceOrders.tsx:398-410`): é o fluxo esperado.
10. Senha errada repetida bloqueia por 15 minutos ("Muitas tentativas incorretas...").

---

## 6. 🚫 Não prometer

- 🚫 Chat ou resposta ao chamado pelo portal (o chamado vira OS; a conversa segue por telefone/WhatsApp).
- 🚫 Cliente criar conta, e-mail e senha próprios: a senha é **uma por cliente**, definida pela empresa.
- 🚫 QR próprio do Portal do Cliente na tela do cliente (só link). 🚫 Pagamento das parcelas do contrato pelo portal sem o add-on
  Cobranças (T19).
- 🚫 Portal do Cliente no plano Exceção (Changelog 1.31.0).
- Tela "demo" do Portal do Contrato (`utils/pmocPortalApi.ts:30-35`) não é recurso para o cliente.

---

## 7. Dúvidas em aberto

1. O portal recarrega sozinho quando o chamado é aberto (tempo real) no fakebase?
2. Com senha ligada e "Sem senha" em OS/Equipamentos, como fica o menu com cadeados (para decidir se vale mostrar)?
3. "Acompanhar ao vivo" no Portal do Contrato depende de OS "a caminho" e localização (T5/T7): mostrar ou não.
4. Qual imagem o "Imprimir QR Code" gera (para uma ilustração fiel)?
5. A aba "Chamados" do equipamento lista também chamados do Portal do Contrato que citam o equipamento? (a OS do contrato não tem
   equipamento, `20261021160000_...:391-399`).
