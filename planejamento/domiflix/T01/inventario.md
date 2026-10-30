# Inventário funcional · T1 — Configurações e identidade da empresa (Dominex)

> Base para o roteiro do tutorial "T1 · Configurações e identidade da empresa" da Domiflix (aula nova, decidida pelo
> Kaik em 30/10/2026 21:55). Levantado em 30/10/2026 contra o código publicado `APP_VERSION = "1.38.6"`
> (`src/config/version.ts:1`), cópia em `/home/claude/domiflix/src-1.38.6`. **Análise estática, somente leitura**: nada foi
> executado. O que só se confirma com o app rodando está marcado "(a confirmar)" e repetido na seção 7.
> Fonte escrita secundária: `docs/guia-tecnico/secoes/T1.html` (redigida para a 1.37.36). **Onde o guia e o código
> divergem, vale o código** (divergências na seção 0.4).

## Como ler

- Caminhos relativos a `src/`, exceto os que começam com `supabase/`, `docs/` ou `rec/`. Formato `arquivo:linha`.
- Texto entre aspas "assim" é o rótulo exato da tela (pt-br). Fonte principal: `lib/i18n/messages/app/settings.ts`
  (bloco pt-br, linhas 22-1793). Alguns textos são fixos no componente e estão citados onde aparecem.
- "Desktop" = janela de 1024 px ou mais. "Tenant" = a empresa cliente (aqui, Glacial Cold Brasil).
- Componentes compartilhados (janelas `ResponsiveModal`, toasts, lista com ficha) estão no inventário do T3.
- Fora deste tutorial (têm aula própria): aba "Usuários e Permissões" (T2), WhatsApp (T21), Cobranças/Asaas (T19),
  Assinatura e plano (T0), perfil pessoal (`/perfil`).

---

## 0. Resumo para quem escreve o roteiro

### 0.1 Itens da trilha (T0 antiga, capítulos 5 a 10) contra o código de hoje

| # | Item da trilha (v1.22.5) | Situação | O que ajustar |
|---|---|---|---|
| 5 | Aba **Empresa**: logo, dados cadastrais, contato e endereço | **Bate, reorganizada** | Um único cartão "Dados da Empresa" com 5 seções em blocos (Identidade Visual, Dados Cadastrais, Contato, Endereço, White Label), mais cartões soltos abaixo: "Documentos Legais", "Exportar meus dados" e "Zona de Perigo" (`pages/Settings.tsx:760-1640`). Layout em colunas desde a 1.36.7 (`Changelog.tsx:1537`). |
| 6 | O switch "mostrar em documentos" e **o que sai no PDF e no relatório** | **Não bate como a trilha diz** | O interruptor se chama "Exibir em documentos" e existe em 5 lugares (`Settings.tsx:849,859,903,913,933`). No código ele só vale para PDFs/recibos de **Estoque, Financeiro e RH** e para a página pública de pagamento; **não é lido** pelo relatório da OS, pela proposta/orçamento, pelo contrato nem pelo PMOC (seção 3.3 e pegadinha P2). O guia (`T1.html`) diz o contrário. |
| 7 | 🔒 **White Label**: logo completo + ícone, cor, QR Code e cabeçalho do relatório | **Bate, com um bloco novo** | Entrou o bloco **"Imagem ao compartilhar a OS"** dentro do White Label (1.36.4 e 1.36.7, `Changelog.tsx:1578,1532`) e o selo de módulo: sem o módulo a seção vira um cartão clicável "Módulo não disponível no seu plano atual" + "Contratar" (`Settings.tsx:1006-1028`). |
| 8 | Abas **Regional** e **Usabilidade** | **Mudou muito** | Regional ganhou país + idioma da empresa × idioma pessoal + moeda + fuso (1.30.0, `Changelog.tsx:2190-2200`) e o cartão do teste DISC (`SettingsRegionalContent.tsx:474-505`). Usabilidade tem 4 grupos de interruptores **mais 3 cartões**: "Orçamento, OS e financeiro", "Movimentações financeiras" e "Origens" (`Settings.tsx:1646-1877`). |
| 9 | **Origens**, **Atalhos** e **Aparência** | **Parcial** | **Origens não é aba**: é um cartão dentro de Usabilidade com o botão "Gerenciar origens" (`Settings.tsx:1822-1876`). Atalhos e Aparência são abas próprias (`Settings.tsx:1879-1884`). |
| 10 | **Integrações**, documentos legais e **Zona de Perigo** | **Mudou** | Integrações tem **3 subabas**: "WhatsApp", "Cobranças (Asaas)" e "API Pública" (`components/settings/SettingsWhatsappContent.tsx:153-157`). Apareceu o cartão **"Exportar meus dados"** (1.24.9, `Changelog.tsx:4310`). Zona de Perigo e Exportar só aparecem para quem tem permissão (seção 2). |
| ⚠️ | Salvamento automático, sem botão Salvar, selo no topo | **Bate** | Selo "Salvando…", "Alterações não salvas", "Salvo" no canto do cabeçalho (`Settings.tsx:1902-1938`). Regional tem auto-save próprio (`SettingsRegionalContent.tsx:49`). |
| ⚠️ | Segmento somente leitura | **Bate** | Caixa cinza com ícone + texto "Define quais ferramentas e recursos do seu segmento aparecem no sistema. Para alterar, fale com a Dominex." (`Settings.tsx:866-884`). |
| 🚫 | Link de avaliação do Google não está em Configurações | **Bate** | Nenhuma ocorrência de "google/avalia" em `Settings.tsx` (busca feita). |

**Buraco entre T0 e T1.** Os capítulos 1 a 4 da T0 antiga (o que a Dominex resolve, **tour pelo menu** e os 3 públicos,
**sidebar × barra superior × menu do celular** e vocabulário, **"o menu muda conforme módulo e cargo"**, marcado como
"dúvida nº 1") não estão no plano do T0 novo (ilustrado, `T00/plano.md`). Ver "Riscos e decisões" do `plano.md`.

### 0.2 O que mudou desde a 1.22.5 (Changelog do app, `pages/Changelog.tsx`)

| Versão | Mudança | Efeito no T1 |
|---|---|---|
| 1.23.1 | Zona de Perigo com cabeçalho vermelho (`Changelog.tsx:4565`) | Cartão vermelho sólido (`components/settings/DangerZoneCard.tsx:35-48`). |
| 1.24.9 | Botão **Exportar meus dados** (planilha Excel) (`Changelog.tsx:4310`) | Cartão e janela de exportação (seção 3.11). |
| 1.24.12 | Permissão **"Exportar Dados da Empresa"** (`Changelog.tsx:4265`) | Quem não é admin pode ver o cartão (`Settings.tsx:126-127`). |
| 1.24.35 | Todo o sistema usa o fuso da empresa, aba Regional (`Changelog.tsx:3643`) | Fuso deixa de ser fixo em Brasília. |
| 1.28.0 | Navegação consistente (`Changelog.tsx:2700`) | Estilo de menu em Aparência. |
| 1.30.0 | País sugere idioma, moeda e fuso; valores na moeda da empresa; idioma pessoal (`Changelog.tsx:2190-2200`) | Regional em 3 cartões (seção 3.6). |
| 1.31.2 | Bandeiras na lista de moedas (`Changelog.tsx:2132`) | Seletor de moeda com bandeira. |
| 1.32.1 | Atalho "Contratar módulo" do WhatsApp nas configurações (`Changelog.tsx:1984`) | Banner na subaba WhatsApp. |
| 1.36.0 | **API Pública** com chaves (`Changelog.tsx:1631`) | 3ª subaba de Integrações. |
| 1.36.4 / 1.36.7 | Imagem ao compartilhar a OS, ajustável no White Label (`Changelog.tsx:1578,1532`) | Bloco novo do White Label (seção 3.4). |
| 1.37.0 | **Zerar Sistema** voltou a concluir; 3 etapas ainda podem falhar (`Changelog.tsx:1156`); add-on PDV vira grupo do Zerar | Nunca executar na gravação (seção 6). |
| 1.37.42 | Abas com padrão único e **3 níveis** (aba, aba, botões) (`Changelog.tsx:367`) | Integrações > Cobranças usa "botões" no 3º nível (`SettingsWhatsappContent.tsx:177-198`). |
| 1.37.53 | Configurações e Usuários com abas mais claras (`Changelog.tsx:200`) | Abas sublinhadas no topo, em linha (`Settings.tsx:1942-1949`). |

### 0.3 O que mais pode surpreender (detalhes na seção 5)

1. **Não existe botão Salvar** e o selo "Salvo" já aparece ao abrir a tela, antes de qualquer edição (`Settings.tsx:1919`).
2. O logo da seção "Identidade Visual" **salva na hora** (sem passar pelo atraso do auto-save) e **não mostra aviso de
   sucesso** (`Settings.tsx:557`).
3. Ligar o White Label **muda a cor do sistema inteiro ao vivo**, antes mesmo de salvar (`Settings.tsx:282-284`), e o logo
   só aparece no menu lateral se o White Label estiver ligado (`hooks/useWhiteLabel.ts:260-261`).
4. "Exibir em documentos" **não vale** para o relatório da OS, propostas e contratos (P2).
5. Trocar idioma, tema ou estilo de menu **muda a tela inteira na hora** e fica gravado (P9).
6. "Exportar meus dados" baixa um arquivo .xlsx e "Baixar PDF" dos termos baixa um PDF: o gravador não grava download
   (`_referencia`, item 6 da `TRILHA.md`).
7. Origens é um cartão de **Usabilidade**; "Atalhos" é só consulta (não dá para reatribuir teclas).

### 0.4 Guia Técnico (`T1.html`, v1.37.36) × código 1.38.6

| Trecho do guia | Código de hoje |
|---|---|
| "as sete abas à esquerda" | Abas **no topo, sublinhadas** (`SettingsSidebarLayout.tsx:116-139`, `Settings.tsx:1942-1949`). |
| Integrações com WhatsApp e Cobranças | Há **3 subabas** (inclui "API Pública", `SettingsWhatsappContent.tsx:153-157`) e a subaba se chama "Cobranças (Asaas)" enquanto o cartão por dentro se chama "Recebimentos (Asaas)" (`settings.ts:1477,1535`). |
| "Exibir em documentos" vale para relatório da OS, orçamento, proposta e contrato | Só Estoque, Financeiro, RH e checkout público (seção 3.3). |
| Estilo de navegação | Gravado **no servidor** (`profiles.navigation_style`, `hooks/useNavigationPreference.ts:25-53`); cor do menu e tema ficam **neste aparelho** (`useNavThemePreference.ts:5`, `SettingsAppearanceContent.tsx:20-27`). |
| Usabilidade com interruptores | Também há 3 cartões extras (decisões da **empresa** e uma **pessoal**), seção 3.7. |

---

## 1. Rotas e navegação

| Tela | Caminho no menu (computador) | Rota |
|---|---|---|
| Configurações | Botão **"Configurações"** (engrenagem) no rodapé do menu lateral, ao lado de "Sair" (`components/layout/SidebarMenuContent.tsx:708-718`). Barra superior: `components/layout/TopNavbar.tsx:468`. Celular: Menu (`components/layout/MoreMenuDrawer.tsx:563`). Atalho **Shift + S** (`hooks/useKeyboardShortcuts.ts:27`). | `/configuracoes` (exige `screen:settings`, `App.tsx:866`) |
| Abas | Barra horizontal sublinhada no topo (celular: pílulas rolantes) (`components/SettingsSidebarLayout.tsx:99-139`) | `?tab=empresa` (padrão), `regional`, `usuarios`, `usabilidade`, `atalhos`, `aparencia`, `integracoes` (`Settings.tsx:56,134-138,148-151`) |
| Subabas de Integrações | Linha sublinhada abaixo das abas | `?tab=integracoes&integration=whatsapp` (padrão) / `asaas` / `api` (`SettingsWhatsappContent.tsx:136-151`) |
| 3º nível de Cobranças | Botões segmentados "Configurações" e "Simulador" (estado local, sem URL) (`SettingsWhatsappContent.tsx:177-198`) | — |
| Endereço antigo | — | `/usuarios` redireciona para `?tab=usuarios` (`App.tsx:865`) |

- Cabeçalho da página: título "Configurações", subtítulo "Gerencie as configurações do sistema" e, à direita, o selo de
  salvamento (`settings.ts:26-27`, `Settings.tsx:1932-1938`).
- Abas, na ordem e com rótulo exato: "Empresa", "Regional", "Usuários e Permissões", "Usabilidade", "Atalhos", "Aparência",
  "Integrações" (`settings.ts:28-36`, ícones em `Settings.tsx:105-113`). "Usuários e Permissões" só aparece com `screen:users`
  (`Settings.tsx:141`).
- Trocar de aba grava `?tab=` com `replace` (não empilha histórico) (`Settings.tsx:148-151`). Abrir `/configuracoes` sem
  parâmetro cai em "Empresa".
- O botão "Configurações" do rodapé aparece para todos, mesmo sem `screen:settings` (não há checagem em
  `SidebarMenuContent.tsx:708-718`); a rota é que barra (`PermissionRoute`, `App.tsx:866`) (a confirmar o destino do redirecionamento).

---

## 2. Permissões e módulos

| Item | Regra | Fonte |
|---|---|---|
| Entrar na tela | `screen:settings` ("Configurações": "Dados da empresa, aparência e preferências do sistema.") | `hooks/usePermissions.ts:91`; `App.tsx:866` |
| **Salvar** qualquer coisa de `company_settings` | No banco: `can_manage_system` = admin ou gestor, acesso total, curinga `*` ou `fn:manage_settings` ("Gerenciar Configurações"), **e** a linha ser da própria empresa | `supabase/migrations/20260610180000_wildcard_star_permission_server_side.sql:50-70`; políticas em `supabase/migrations/20260927170000_harden_core_rls_dossie_seguranca.sql:310-338` |
| Zona de Perigo / Zerar Sistema | `hasRole('admin')` ou `super_admin`; o servidor confere de novo na RPC | `Settings.tsx:120,1633-1640` |
| Cartão "Exportar meus dados" | Admin **ou** quem tem `fn:export_company_data` ("Exportar Dados da Empresa") **com registro** em `user_permissions` (sem registro o modo legado liberaria tudo) | `Settings.tsx:121-127,1626-1630`; `usePermissions.ts:123` |
| Aba "Usuários e Permissões" | `screen:users` (T2) | `Settings.tsx:141` |
| Campos de empresa da aba Regional (país, idioma da empresa, moeda, fuso, DISC) | Só `canResetSystem` (admin); os demais usuários veem desabilitado e o texto "(somente admin)" | `Settings.tsx:1643-1644`; `SettingsRegionalContent.tsx:314,338,375,417,468,497` |
| Idioma **pessoal** | Qualquer usuário | `SettingsRegionalContent.tsx:70-74` |
| Subaba WhatsApp | Editar exige admin/gestor ou `fn:manage_settings` e o módulo `whatsapp`; sem módulo, vira "Prévia do módulo de WhatsApp" | `SettingsWhatsappContent.tsx:208-209,234-235,270-300` |
| Subaba Cobranças (Asaas) | Módulo `cobrancas`; sem ele, "Recebimentos não contratado" | `components/settings/SettingsAsaasContent.tsx:346-358` |
| API Pública | `fn:manage_api_keys` ("Gerenciar Chaves da API") | `usePermissions.ts:121`; `components/settings/SettingsPublicApiContent.tsx` (não aberto no vídeo) |
| Seção White Label | Módulo `white_label` (`hasModule`) | `Settings.tsx:995,1031` |
| Segmento | Somente leitura; só a Dominex muda | `Settings.tsx:866-884` |

- **Pegadinha de permissão**: quem tem a tela mas não tem `can_manage_system` vê todos os campos editáveis; o save falha
  com o toast "Erro ao salvar — Sem permissão para alterar os dados da empresa." (`hooks/useCompanySettings.ts:166-173,224`).
  Só os interruptores que vão direto ao servidor ficam desabilitados com `!canSave` (`Settings.tsx:1692,1738,1761,1782`).
  Marcado como [handoff, UX] em P7.
- Módulos 🔒 que mudam o que aparece: `white_label` (seção White Label), `whatsapp`, `cobrancas`, `pdv` (grupo "PDV e Loja"
  no Zerar Sistema e abas de exportação), `rh` (aba "Funcionários" na exportação).
- O segmento (`company_settings.segment`) também decide se a **Área do Técnico™** existe no menu (T18); por isso é de leitura.

---

## 3. Por tela / janela / aba

### 3.1 Aba "Empresa" — estrutura (`pages/Settings.tsx:760-1640`)

Ordem vertical: cartão "Dados da Empresa" (descrição "Informações da empresa que aparecem em etiquetas e documentos",
`settings.ts:48-49`) contendo as 5 seções em blocos arredondados; depois "Documentos Legais"; depois "Exportar meus dados"
(se permitido); por último "Zona de Perigo" (se admin). Largura máxima 6xl (`Settings.tsx:762`).

### 3.2 Seção "Identidade Visual" (`Settings.tsx:771-832`)

- Título "Identidade Visual", descrição "Logo da empresa para documentos e sistema" (`settings.ts:53-54`).
- **Sem logo**: área clicável com ícone de envio, "Clique para enviar o logo" e dica "PNG, JPG até 5MB" (`settings.ts:59-60`;
  `Settings.tsx:817-830`). O `<input type="file" accept="image/*">` fica escondido dentro do rótulo.
- **Com logo**: miniatura 112 px + botões **"Substituir"** (ícone de setas) e **"Remover"** (vermelho, ícone de lixeira)
  (`Settings.tsx:783-814`). "Remover" abre a confirmação **"Remover logo?"** / "O logo atual será removido permanentemente."
  com "Cancelar" e "Remover" (`settings.ts:57-58`; `Settings.tsx:797-813`).
- Regras do envio (`Settings.tsx:532-563`): passa por `processImageFile` (conversão/compressão, a confirmar), limite
  **5 MB** (toast "Arquivo muito grande (máx 5MB)"), tem de ser imagem ("Apenas imagens são permitidas"), apaga o logo antigo
  do bucket, envia `logo_<timestamp>.<ext>` para `company-logos` e grava `logo_url` **na hora** (sem debounce). Erro:
  "Erro ao enviar logo". **Sem toast de sucesso.**
- Remover: apaga do bucket e grava `logo_url = null` (`Settings.tsx:565-573`).
- Onde o logo da empresa aparece: cabeçalhos de PDFs e recibos (`utils/companyDocumentHeader.ts`,
  `utils/receiptGenerator.ts`), relatório da OS (`components/technician/OSReport.tsx`), proposta
  (`components/quotes/templates/shared.ts`), PMOC (`components/pmoc/CertificadoArtConfigDialog.tsx`), Ponto
  (`components/ponto/PontoScreen.tsx`) e, **se o White Label estiver ligado**, no menu lateral (3.4).

### 3.3 Seções "Dados Cadastrais", "Contato" e "Endereço" (`Settings.tsx:833-991`)

**Dados Cadastrais** — "Razão social, documento e informações oficiais" (`settings.ts:100-101`).

| Campo | Detalhes | Fonte |
|---|---|---|
| "Nome da Empresa" | Placeholder "Nome da sua empresa". Texto livre. É o nome que a Zona de Perigo pede para confirmar. | `Settings.tsx:846-852` |
| "CNPJ/CPF" | Placeholder "00.000.000/0000-00"; máscara automática de CPF ou CNPJ (`cpfCnpjMask`); **sem validação de dígitos** | `Settings.tsx:856-862` |
| "Segmento de Atuação da Empresa" | Somente leitura: caixa cinza com ícone e cor do segmento ("Refrigeração e Climatização" para a Glacial) ou "Não definido"; texto de apoio sobre falar com a Dominex | `Settings.tsx:866-884`; `utils/companySegments.ts:44` |
| "Exibir em documentos" (interruptor pequeno ao lado de Nome e CNPJ/CPF) | Padrão ligado | `Settings.tsx:849,859` |

**Contato** — "Telefone e e-mail da empresa" (`settings.ts:115`): "Telefone" (máscara `phoneMask`, placeholder "(00) 0000-0000")
e "Email" (`type=email`, placeholder "contato@empresa.com"), cada um com seu "Exibir em documentos" (`Settings.tsx:900-916`).

**Endereço** — "Localização física da empresa" (`settings.ts:126`), com **um único** "Exibir em documentos" no título da seção
(vale para o endereço inteiro) (`Settings.tsx:932-936`):

| Campo | Detalhes | Fonte |
|---|---|---|
| "CEP" | Máscara `00000-000`; ao completar 8 dígitos chama a edge function `cep-lookup` sozinho; botão só com lupa (sem texto) | `components/CepLookup.tsx:41-77`; `Settings.tsx:939-949` |
| "Endereço" | Campo com sugestões (digita a rua e escolhe); placeholder "Rua, Avenida…"; ao escolher preenche número, bairro, cidade, UF e CEP; busca em `nominatim.openstreetmap.org` | `components/AddressAutocomplete.tsx:88-89`; `Settings.tsx:951-970` |
| "Número" / "Complemento" | Placeholders "Nº" e "Sala, Andar…" | `Settings.tsx:971-977` |
| "Bairro" | Placeholder "Bairro" | `Settings.tsx:979-981` |
| "UF / Cidade" | Dois seletores com busca; a lista de cidades vem do IBGE (`servicodados.ibge.gov.br`); trocar a UF limpa a cidade | `components/StateCitySelector.tsx:82-83,107-110`; `Settings.tsx:983-990` |

- CEP encontrado: toast "Endereço encontrado!"; não achou: "CEP não encontrado"; falha: "Erro ao buscar CEP" (**textos fixos em
  português**, `CepLookup.tsx:33-41`). O CEP preenche Endereço, Bairro, Cidade e UF, **não** o Número nem o Complemento
  (`Settings.tsx:942-948`).
- **Quem lê "Exibir em documentos"** (busca por `show_*_in_documents` em todo o código): ordem de compra
  (`utils/ordemCompraPdfGenerator.ts:113-161`), movimentações (`utils/movimentacoesPdfGenerator.ts:111-164`,
  `movimentacoesReportHtmlGenerator.ts:115-166`), inventário e contagem (`inventoryPdfGenerator.ts:107-157`,
  `inventoryCountPdfGenerator.ts:78-122`, `stockPositionPdfGenerator.ts`), compras de material
  (`materialPurchaseReportExport.ts:75-207`), recibos (`utils/receiptGenerator.ts:82-134`), extrato e recibo térmico de
  funcionário (`components/employees/EmployeeExtract.tsx:81-85`, `utils/employeeReceiptThermalGenerator.ts:174-182`,
  `pages/Employees.tsx:81-82`), cabeçalho comum (`utils/companyDocumentHeader.ts:45-70`, usado só em `PublicCheckout.tsx`
  e `LaudoTecnico.tsx`) e a edge `supabase/functions/get-tenant-payment-checkout/index.ts:107-168`.
  **Nenhuma ocorrência** em `components/technician/OSReport.tsx`, `components/technician/ReportHeader.tsx`,
  `components/quotes/`, `components/contracts/` e `components/pmoc/`.
- Os cinco interruptores nascem ligados (`Settings.tsx:198-202`); desligar não apaga o dado.

### 3.4 Seção "White Label" (`Settings.tsx:994-1584`)

- **Sem o módulo** (`hasModule('white_label')` falso): cartão cinza clicável com ícone de pincel, título "White Label",
  "Módulo não disponível no seu plano atual" e selo "Contratar"; ao clicar abre a janela "Módulo não disponível" com
  "White Label — Personalização completa da marca: logo, cores e ícone do sistema", "Adicionar módulo" e "Ver planos"
  (sem preço) (`Settings.tsx:1006-1028`; `components/ModuleGateModal.tsx:36-100,145-148`).
- **Com o módulo**: título "White Label", descrição "Personalize o sistema com a identidade visual da sua marca", e o
  interruptor **"Ativar White Label"** ("Substitui o logo e a cor padrão do sistema") (`Settings.tsx:1031-1040`).
- Desligado, o resto some (os valores continuam guardados). **Ligado**, aparecem, nesta ordem (`Settings.tsx:1042-1583`):
  1. **"Imagem ao compartilhar a OS"** (`settings.ts:65-95`). Descrição "Define a imagem que aparece no WhatsApp e em outros
     aplicativos ao compartilhar o link público da Ordem de Serviço." Mostra "Logo da empresa" ou "Imagem personalizada"
     como origem ativa e a dica "A imagem é preparada em 1200×630. Para melhor nitidez, use um logo com pelo menos 800 px de
     largura." Botões: **"Usar logo da empresa"** (gera e salva na hora), **"Ajustar arte"** (abre o editor) e **"Enviar imagem
     personalizada"** (PNG/JPG/WebP, até 10 MB). Editor: "Prévia nos dois formatos" ("Cartão grande" e "Miniatura compacta" com
     "Área segura"), interruptor "Otimizar para miniatura", "Fundo da arte" ("Automático" × "Cor manual"), "Tamanho do logo" e
     **"Salvar arte"**. Toasts: "Imagem social gerada com o logo da empresa.", "Imagem social personalizada salva.", erros "Não foi
     possível salvar a imagem social" / "Imagem muito grande (máx. 10 MB)". Sem logo: "Envie primeiro o logo da empresa ou
     escolha uma imagem personalizada." (`Settings.tsx:383-530,1044-1292`). Envia `os_social_<ts>.png|jpg` ao bucket
     `company-logos` e grava `os_social_image_url` + `os_social_image_mode` (`Settings.tsx:429-465`). A prévia usa canvas
     e baixa a imagem por `fetch` com CORS (`utils/osSocialImage.ts:50`).
  2. **"Logo completo"** + **"Ícone (1:1)"** lado a lado (`Settings.tsx:1294-1387`). Logo: estados "Logo personalizado
     configurado" / "Usando o logo da empresa por padrão" / "Será utilizado o logo da empresa"; botão "Enviar logo (opcional)"
     ou "Substituir"/"Remover". Ícone: "Ícone quadrado para o menu lateral recolhido. 128×128px." com "Enviar ícone".
     Mesmos limites (5 MB, imagem) (`Settings.tsx:575-648`); arquivos `wl_logo_*`/`wl_icon_*`.
  3. **"Cor primária"** — "Substitui a cor verde padrão do sistema". Seletor `ColorPicker`: botão com a cor, paleta de 19
     cores (a primeira é `#00C597`, o verde da Dominex), campo hexadecimal e faixa de matiz (`components/ui/ColorPicker.tsx:8-13,145-189`);
     ao lado, uma faixa com a cor escolhida. Padrão `#00C597` (`Settings.tsx:192`).
  4. **"QR Code"** — "Personalize o visual dos QR Codes gerados pelo sistema, com o logo da sua marca no centro":
     "Estilo dos pontos" (Quadrado/Arredondado/Pontos/Elegante), "Cantos" (Quadrado/Arredondado/Ponto), "Cor do QR Code" e
     prévia ao vivo ("Pré-visualização") com um QR de `https://dominex.app` (`Settings.tsx:1404-1462`; `settings.ts:158-176`).
  5. **"Cabeçalho do Relatório de Serviço"** — "Personalize o visual do cabeçalho que aparece no relatório da OS concluída":
     prévia ao vivo do `ReportHeader` com os dados digitados, "Cor de fundo do cabeçalho", "Cor do texto", "Cor da barra de
     status", "Tamanho do logo ({size}px)" (barra 40-300 px com logo completo, 40-140 com ícone), "Fundo atrás do logo"
     (interruptor + "Cor do fundo") e **"Tipo de logo no relatório"** com os botões "Logo Completo" / "Ícone"
     (`Settings.tsx:1465-1580`; `settings.ts:177-190`).
- **Efeito ao vivo**: `useEffect(() => applyWhiteLabelTheme(wlEnabled, wlColor))` roda a cada mudança do interruptor ou da
  cor (`Settings.tsx:282-284`). Muda `--primary`, `--primary-foreground` (escolhe branco ou escuro pelo contraste), `--ring`,
  as variáveis da barra lateral, o gradiente da marca e o neon do menu (`hooks/useWhiteLabel.ts:211-250`) e guarda tudo em
  `localStorage` (`__wl_*`, `useWhiteLabel.ts:189-208`).
- **Onde a marca aparece de verdade** (só com WL ligado): menu lateral — ícone quando recolhido, logo quando aberto
  (`SidebarMenuContent.tsx:376-401`; `useWhiteLabel.ts:260-261`); relatório da OS e página pública da OS
  (`OSReport.tsx:557`, `pages/TechnicianOS.tsx:1183`); proposta pública (`pages/ProposalPublic.tsx:39`); portal do cliente
  (`pages/CustomerPortal.tsx:683`); portal PMOC (`pages/public/PmocPublicPortal.tsx:546`); captação de leads
  (`pages/PublicLeadCapture.tsx:229,497`); avaliação DISC (`pages/DiscAssessmentPublic.tsx:258`); ponto
  (`pages/PontoKiosk.tsx:242`); recibos (`utils/receiptGenerator.ts:116`) e QR Codes (`hooks/useBrandedQrConfig.ts`). O rodapé
  "Desenvolvido por Dominex · dominex.app" some nos documentos (`utils/companyDocumentHeader.ts:11,105`).

### 3.5 Cartões "Documentos Legais", "Exportar meus dados" e "Zona de Perigo" (`Settings.tsx:1590-1640`)

- **"Documentos Legais"** — "Consulte e baixe os termos que regem o uso do Dominex"; botão **"Ver termos de uso"** abre a
  janela "Termos de Uso — Dominex" (modo leitura) com os botões **"Baixar PDF"** (gera e baixa) e **"Fechar"**
  (`components/TermsOfServiceModal.tsx:179-195`; `settings.ts:194-199,1421-1435`). Abaixo, em verde, "Aceito em {data}"
  quando o usuário aceitou os termos (`Settings.tsx:1609-1613`; vem de `profiles.terms_accepted_at`).
- **"Exportar meus dados"** — ver 3.11. **"Zona de Perigo"** — ver 3.12.

### 3.6 Aba "Regional" (`components/settings/SettingsRegionalContent.tsx`, 506 linhas)

Três cartões. **Auto-save próprio** com atraso de 700 ms e gravação ao sair da aba (`SettingsRegionalContent.tsx:49,148-174`); o selo "Salvando…/Alterações
não salvas/Salvo" desta aba tem texto próprio (`settings.ts:330-332`; `SettingsRegionalContent.tsx:231-253,317`).

| Cartão | Conteúdo | Fonte |
|---|---|---|
| **"Meu idioma"** | "O idioma que VOCÊ vê no sistema. Aplica na hora, só para você." Seletor "Idioma" (Português, English, Español, Français); dica "Preferência pessoal. Sobrepõe o idioma padrão da empresa só para você." Grava na hora (`setUserLanguage`) em `user_preferences` | `:259-301`; `settings.ts:299-304` |
| **"Padrões da empresa"** (admin; "(somente admin)" para os demais) | "Idioma padrão, moeda e fuso horário para toda a empresa". Campos: "País da empresa" (busca "Buscar país ou moeda"), "Idioma padrão da empresa", "Moeda" (com bandeira), "Fuso horário" (busca "Buscar fuso (ex: Sao Paulo)", grupo "Mais usados" + "Todos os fusos"). Trocar o país abre a pergunta "Usar os padrões de {país} para idioma, moeda e fuso?" com "Manter atuais" / "Usar padrões" (toast "Padrões de {país} aplicados"); trocar o idioma pergunta "Usar os padrões de {idioma} para moeda e fuso?". Aviso fixo (sempre visível): "A moeda é a de operação da empresa. Trocar não converte os valores já registrados, eles continuam com o número original." | `:305-472`; `settings.ts:305-333` |
| **"Perfil Comportamental"** | "Como o teste comportamental (DISC) se comporta para os funcionários." Chave "Funcionário vê o próprio resultado do teste comportamental" com botões **Sim / Não**; dica "Ligado: ao terminar, o funcionário vê o próprio perfil. Desligado: vê só uma tela de agradecimento, e o resultado fica só para o RH." (detalhe é do T22) | `:474-505`; `settings.ts:334-342` |

Colunas gravadas: `country_code`, `language`, `currency`, `timezone`, `disc_show_result_to_employee` (`SettingsRegionalContent.tsx:136-144`).

### 3.7 Aba "Usabilidade" (`Settings.tsx:1646-1877`)

Cabeçalho "Usabilidade" — "Preferências de comportamento do sistema" (`settings.ts:204-205`). **Quatro grupos de interruptores**
em um cartão (`Settings.tsx:718-757`); cada interruptor mostra o toast **"Preferência salva!"** (`Settings.tsx:660`):

| Grupo | Interruptor (título — descrição) | Onde guarda | Padrão |
|---|---|---|---|
| "Ordens de Serviço" — "Comportamentos relacionados às ordens de serviço" | "Salvamento Automático" — Salvar automaticamente rascunhos de ordens de serviço ao editar | localStorage `usability-settings` (**por aparelho**) | ligado |
| | "Exibir Valores" — Mostrar valores financeiros (mão de obra, peças) nas ordens de serviço | idem | ligado |
| | "Exigir Assinatura" — Tornar obrigatória a assinatura do cliente ao finalizar OS | idem | desligado |
| | "Salvar fotos no dispositivo" — botão para salvar a foto no aparelho (iPhone: "Salvar Imagem"; Android: baixa direto) | idem | ligado |
| | **"Consumo de estoque na OS"** — Permite que o técnico registre os materiais usados durante a ordem de serviço e dê baixa no estoque ao finalizar | **servidor** (`company_settings.os_stock_consumption_enabled`), com spinner enquanto carrega | desligado (`supabase/migrations/20260902160100_os_consumo_materiais_rascunho_e_commit.sql:520`; **ligado no seed do fakebase**) |
| "Interface" — "Preferências visuais de listagens e tabelas" | "Tabelas Compactas" — Reduzir espaçamento nas tabelas para exibir mais dados por página; "Fotos de Equipamentos" — Exibir miniaturas de fotos dos equipamentos nas listagens | localStorage | compactas desligado; fotos ligado |
| "Segurança" — "Confirmações e validações de segurança" | "Confirmar Exclusões" — Exibir diálogo de confirmação antes de excluir registros | localStorage | ligado |
| "Agenda" — "Configurações da agenda e calendário" | "Exibir Feriados" — Mostrar feriados nacionais e municipais na agenda | localStorage | ligado |

Três cartões depois (`Settings.tsx:1713-1876`):

1. **"Orçamento, OS e financeiro"** — "O que vira lançamento no financeiro automaticamente, ao aprovar um orçamento ou ao
   finalizar uma Ordem de Serviço" (`settings.ts:264-276`). (a) "Ao aprovar um orçamento": botão duplo **"Já recebi" /
   "Vou receber depois"** com a dica "Lança como receita recebida e entra no saldo da conta na hora." ou "Gera conta a receber
   pendente. O saldo só muda quando você der a baixa."; (b) "Aprovação pelo link da proposta já gera conta a receber"; (c)
   "Perguntar sobre receita ao finalizar OS" (só aparece para quem tem a permissão "Lançar Receita ao Finalizar OS"). Os três
   gravam no servidor (`quote_approval_revenue_mode`, `quote_public_approval_creates_receivable`,
   `os_finish_revenue_prompt_enabled`). Contexto: T9 e T13.
2. **"Movimentações financeiras"** — "Preferência pessoal, vale em qualquer aparelho que você usar": "Incluir compras no cartão"
   ("Por padrão a lista traz só movimento de conta e caixa. O que saiu do caixa foi o pagamento da fatura, não cada compra.")
   em `user_preferences` (`Settings.tsx:1795-1820`; `lib/i18n/messages/app/finance.ts:461-465`).
3. **"Origens"** — "Lista de origens usada no cadastro de clientes e nas oportunidades do CRM"; botão **"Gerenciar origens"**.
   Vazio: "Nenhuma origem cadastrada. Crie um conjunto inicial e edite à vontade depois." + **"Criar origens padrão"**
   (cria 10: Indicação, Site, Telefone, WhatsApp, Google, Instagram, Facebook, Parceiro, Feira/Evento, Outro,
   `hooks/useCustomerOrigins.ts:38-49`). Com origens: lista com ícone colorido, nome e "Inativa" quando desativada
   (`Settings.tsx:1822-1876`).
   - Janela **"Origens de Clientes"** (`components/customers/CustomerOriginManagerDialog.tsx`): lista com ações Editar/Excluir
     por linha (menu de ações), edição em linha (nome, ícone, cor, confirmar/cancelar) e linha tracejada para criar
     ("Nova origem...", seletor de ícone, seletor de cor, botão **"Adicionar"**). Toasts: "Origem criada!", "Origem atualizada!",
     "Origem removida!". **Excluir é imediato, sem confirmação** (`:113-114`); o seletor de ícone mostra os nomes em inglês
     (Globe, UserPlus, Megaphone...) (`originIcons.tsx:9-13`).

### 3.8 Aba "Atalhos" (`components/settings/SettingsShortcutsContent.tsx`, 132 linhas)

Título "Atalhos de Teclado", "Use atalhos para acessar funcionalidades rapidamente"; interruptor **"Atalhos de Teclado"** com o
texto "Atalhos estão ativados/desativados" (guarda `dominex-shortcuts-enabled` no navegador, `hooks/useKeyboardShortcuts.ts:32,37-48`).
Lista **somente leitura** (não se reatribui tecla) em dois grupos (`hooks/useKeyboardShortcuts.ts:17-29`):

- "Navegação": Shift+D Dashboard · Shift+O Ordens de Serviço · Shift+A Agenda · Shift+C Clientes e Fornecedores · Shift+E
  Equipamentos · Shift+R CRM/Kanban · Shift+F Financeiro · Shift+I Estoque · Shift+Q Orçamentos · Shift+T Contratos · Shift+S
  Configurações.
- "Geral": Shift+P Perfil.

Caixa "Dicas": "Use Shift + letra para navegação rápida" (no Mac mostra ⇧), "Atalhos não funcionam quando você está digitando em
campos de texto", "Você pode desativar os atalhos a qualquer momento pelo toggle acima" (`SettingsShortcutsContent.tsx:116-126`).

### 3.9 Aba "Aparência" (`components/settings/SettingsAppearanceContent.tsx`, 245 linhas)

Cartão "Aparência" — "Personalize a interface visual do sistema". Três blocos, nesta ordem:

1. **"Estilo de Navegação (Desktop)"** — "Escolha entre menu lateral ou menu superior. Esta opção só afeta a visualização em
   desktop." Opções com ícone: **"Menu Lateral"** ("Sidebar tradicional à esquerda") e **"Menu Superior"** ("Barra horizontal no
   topo") (`:41-92`). Muda o layout inteiro na hora e grava em `profiles.navigation_style` (`hooks/useNavigationPreference.ts:44-56`).
2. **"Menu (lateral e superior)"** — "Escolha a cor do menu de navegação, independente do tema do sistema.": **"Escuro
   (recomendado)"** ("Menu sempre escuro, com destaque na cor da marca") e **"Seguir o tema"** (`:94-153`); fica no navegador
   (`nav-theme-preference`, `hooks/useNavThemePreference.ts:5`).
3. **"Tema do Sistema"** — "Escolha entre tema claro ou escuro para a interface." Dois cartões de prévia: **"Tema Claro"** e
   **"Tema Escuro"** (`:154-243`); grava `theme` no navegador e troca a classe `dark` do `<html>` (`:20-27`).

### 3.10 Aba "Integrações" (só onde ficam; `SettingsWhatsappContent.tsx:136-198`)

Três subabas sublinhadas: **"WhatsApp"** (padrão), **"Cobranças (Asaas)"**, **"API Pública"** (rótulo fixo em português, `:156`).

- **WhatsApp**: sem o módulo, faixa de aviso com cadeado "Prévia do módulo de WhatsApp" — "Você pode conhecer toda a estrutura.
  Para salvar e ativar as automações, contrate o módulo de WhatsApp." e botão "Contratar módulo" (`:270-300`; copy em
  `:85-106`). Com o módulo e sem número conectado: faixa "Conecte o WhatsApp para liberar as configurações" e a seção
  "Conexão com o WhatsApp" (conexão por QR Code). Seções do módulo: Automações, Atendimento, Modelos, Campanhas, Histórico,
  Conexão (`:104`). Detalhe: **T21**.
- **Cobranças (Asaas)**: botões segmentados "Configurações" e "Simulador". Sem o módulo `cobrancas`: "Recebimentos não
  contratado" (`SettingsAsaasContent.tsx:346-358`). Com conta ativa (seed): cartão "Recebimentos (Asaas)" — "Cobre seus
  clientes por Pix, boleto e cartão usando sua própria conta Asaas.", selo verde "Ativo", texto "Recebimentos ativos. Já é
  possível cobrar seus clientes.", cartão de taxas, "Lançar cobranças no Financeiro automaticamente" (`:360-530`;
  `settings.ts:1534-1613`). Inativa: campo "Chave de API da Asaas" (tipo senha) + "Ativar recebimentos" (**não mostrar**). Detalhe: **T19**.
- **API Pública**: chaves de API (`SettingsPublicApiContent.tsx`, 475 linhas; função `api-key-manager`). **Não abrir** no vídeo.

### 3.11 Janela "Exportar meus dados" (`components/settings/DataExportCard.tsx`, `DataExportDialog.tsx`)

- Cartão (`settings.ts:416-417`): "Exportar meus dados" — "Baixe uma planilha do Excel com os dados da sua empresa: clientes,
  equipamentos, ordens de serviço, orçamentos, contratos, financeiro e mais. Serve de backup e para levar seus dados para onde
  quiser." Botão **"Exportar dados"**.
- Janela: "Exportar meus dados" — "Escolha o que deseja incluir na planilha. O arquivo é gerado na hora e baixado
  automaticamente." Botões "Marcar tudo" / "Limpar seleção" / "Cancelar" / "Exportar"; caixas por grupo: Clientes,
  Equipamentos, Ordens de Serviço, Orçamentos, Contratos, Financeiro, Estoque, Movimentações de Estoque, Vendas do PDV e
  Fiado dos Clientes (só com o módulo PDV), Funcionários, CRM / Leads, Ponto. **Movimentações de Estoque e Ponto vêm
  desmarcados** com o aviso "Movimentações de Estoque e Ponto vêm desmarcados por padrão porque costumam ter muitos registros.
  Marque-os se também precisar deles." (`hooks/useCompanyDataExport.ts:146-163`; `DataExportDialog.tsx:210`).
- Ao confirmar: barra de progresso "Exportando {aba}... {n} registros", toast "Exportação concluída! O arquivo foi baixado."
  (`settings.ts:426-427`), arquivo `backup*.xlsx` — **download** (o gravador não grava).

### 3.12 Janela "Zerar Sistema" (`components/settings/DangerZoneCard.tsx`, `ResetSystemDialog.tsx`, 620 linhas) — **só informação**

- Cartão vermelho: "Zona de Perigo" — "Ações irreversíveis. Revise cuidadosamente antes de confirmar."; linha "Zerar Sistema" —
  "Exclui dados operacionais selecionados. Dados da empresa e usuários são preservados. Toda operação fica registrada em log
  de auditoria."; botão vermelho **"Zerar Sistema"** (`DangerZoneCard.tsx:35-66`; `settings.ts:404-412`).
- Janela: "Zerar Sistema" — "Esta ação irá DELETAR PERMANENTEMENTE os dados operacionais da empresa"; "Escolha o que deseja
  remover:" com "Marcar tudo" e "{n}/{total} selecionados"; grupos **Operacional** (Ordens de Serviço, Equipamentos, Contratos
  e PMOC, Configurações personalizadas), **Comercial (CRM)** (Orçamentos e Propostas, Clientes e Leads), **Financeiro**
  (Movimentações, Categorias financeiras), **RH e Inventário** (Funcionários e equipe, Materiais, Estoque) e **PDV e Loja**
  (Vendas, caixa e fiado). "Serão mantidos: Dados básicos da empresa, Usuários cadastrados, Histórico de pagamentos." "Esta ação
  NÃO PODE ser desfeita!" "Para confirmar, digite o nome da empresa:" (campo "Nome da empresa"); "Cancelar" e **"Sim, Zerar
  Sistema"**, desabilitado sem seleção, sem o nome certo ("O nome digitado não confere com o nome da empresa."), enquanto carrega
  ou **offline** ("Esta ação precisa de conexão com a internet. Você está offline.") (`ResetSystemDialog.tsx:389,421,499-500,606-614`;
  `settings.ts:866-983`).
- Para o vídeo: abrir a janela, mostrar os grupos e **cancelar**. Nunca digitar o nome.

---

## 4. Backend por tela

| Tela / ação | Chamada | Observação para o backend falso |
|---|---|---|
| Abrir `/configuracoes` | `profiles?select=company_id` (maybeSingle) e `company_settings?select=*&company_id=eq.<id>` (maybeSingle) (`useCompanySettings.ts:135-148`) | Seed já tem `company_settings` da Glacial (`rec/fakebase/seeds/gen-01-tenant.json`). |
| **Cada autosave** | `PATCH company_settings?id=eq.<id>` com `.select()`; **precisa devolver a linha**, senão o app lança "Sem permissão para alterar os dados da empresa." (`useCompanySettings.ts:161-173`) | Confirmar que o PATCH genérico devolve a linha atualizada (a confirmar). Se a linha não existir, o app faz `POST` com `company_id` (`:186-193`). |
| Logo, logo WL, ícone, imagem da OS | `storage.from('company-logos')`: `remove`, `upload` (`logo_<ts>.<ext>`, `wl_logo_*`, `wl_icon_*`, `os_social_<ts>`), `getPublicUrl` (`Settings.tsx:547-563,429-445`) | `http/storage.mjs` guarda em memória e serve com CORS; arquivos de exemplo em `rec/fakebase/storage/company-logos/glacial/`. O envio é um passo `upload` do gravador (`rec/recorder/runner.mjs:492-510`). A imagem social usa `fetch` com CORS (`utils/osSocialImage.ts:50`). |
| CEP | edge function `cep-lookup` (`CepLookup.tsx:30`) | Handler já existe (`rec/fakebase/handlers/functions/cep-lookup.mjs`). |
| Endereço com sugestão | `GET https://nominatim.openstreetmap.org/search?...` (`AddressAutocomplete.tsx:88`) | Handler de host já existe (`handlers/ext/nominatim.openstreetmap.org.mjs`). |
| UF / Cidade | `GET https://servicodados.ibge.gov.br/api/v1/localidades/estados/<UF>/municipios` (`StateCitySelector.tsx:82`) | Handler já existe (`handlers/ext/servicodados.ibge.gov.br.mjs`). |
| White Label | só `company_settings` + `company_modules` (`module_code = 'white_label'`) | Módulo já está no seed. `white_label_primary_color` **não está** no seed (cai em `#00C597`). |
| Regional | `PATCH company_settings` (5 colunas); idioma pessoal em `user_preferences` (`useAppLocaleContext.setUserLanguage`) | `user_preferences` tem linha da Camila no seed. |
| Usabilidade (servidor) | `PATCH company_settings` (`os_stock_consumption_enabled`, `quote_approval_revenue_mode`, `quote_public_approval_creates_receivable`, `os_finish_revenue_prompt_enabled`); `user_preferences` (cartão) | Seed já tem `os_stock_consumption_enabled` e `os_finish_revenue_prompt_enabled` ligados. |
| Origens | `customer_origins` select/insert/update/delete (`useCustomerOrigins.ts:57-138`) | Seed `gen-02-cadastros.json` tem 4 origens (Indicação, Instagram, Google, WhatsApp). |
| Aparência | `profiles` select/update `navigation_style` (`useNavigationPreference.ts:22-56`) | Seed tem `navigation_style: sidebar`. |
| Termos | `profiles.terms_accepted_at`; "Baixar PDF" gera no navegador | Seed tem `terms_accepted_at` (**cuidado: o PDF baixa arquivo**). |
| Exportar dados | leituras em dezenas de tabelas (`hooks/useCompanyDataExport.ts`) | Muitas sem seed (ver `desconhecidos.log`); **evitar executar**, só abrir a janela. |
| Zerar Sistema | RPC de reset por etapas (`ResetSystemDialog.tsx`) | **Não executar**; basta abrir/cancelar. |
| Integrações | `company_whatsapp_settings`, `whatsapp_connections`, `tenant_payment_accounts` (seed tem a conta Asaas ativa), edge functions `whatsapp-*`, `tenant-asaas-provision`, `api-key-manager` | Para apenas mostrar onde ficam: `company_whatsapp_settings`/`whatsapp_connections` sem seed devolvem lista vazia; abrir "API Pública" chama `api-key-manager` (sem handler). |

Buckets: `company-logos` (público para leitura, escrita isolada por empresa desde as migrations `20261016130000_storage_isolamento_por_empresa_onda2_policies.sql:107-146`).

---

## 5. Pegadinhas para roteiro e gravação

- **P1 — "Salvo" já aparece ao abrir.** O selo verde "Salvo" depende de `settingsLoadedRef.current`, não de ter editado (`Settings.tsx:1919`). Na gravação o selo muda "Alterações não salvas" → "Salvando…" → "Salvo" em ~1 s depois de parar de digitar (`Settings.tsx:341-358`; atraso de 800 ms) e na hora ao sair do campo (`onBlur` do contêiner, `Settings.tsx:1942`).
- **P2 — [handoff] "Exibir em documentos" não vale para OS, proposta, contrato nem PMOC.** O rótulo promete "documentos" e a trilha e o guia citam relatório da OS, orçamento, proposta e contrato, mas a busca por `show_*_in_documents` só encontra Estoque, Financeiro, RH, `LaudoTecnico`, `PublicCheckout` e a edge de pagamento (3.3). Decidir: aplicar nos demais ou trocar o rótulo/descrição. Para o vídeo: falar só do que é certo ("recibos e relatórios de estoque, financeiro e RH") ou aguardar decisão.
- **P3 — [handoff] "Substituir" logo apaga o logo antigo antes de enviar o novo** (`Settings.tsx:547-554`): se o envio falhar, a empresa fica com `logo_url` apontando para arquivo apagado.
- **P4 — Logo da empresa salva na hora e sem toast de sucesso** (`Settings.tsx:557`); só o selo do topo e a troca da miniatura confirmam. As imagens do White Label (logo, ícone) também.
- **P5 — Cor ao vivo.** Ligar o White Label e escolher cor troca o sistema inteiro **antes** do auto-save (`Settings.tsx:282-284`); desligar volta ao verde na hora. O que ficou gravado é o estado do último auto-save. Se a gravação deixar o WL ligado, **os próximos tutoriais saem com a cor nova** (seção "Riscos" do plano).
- **P6 — Logo no menu só com WL ligado.** Com WL desligado o menu lateral mostra sempre o logo da Dominex; o logo de "Identidade Visual" não aparece no menu (`useWhiteLabel.ts:260-261`; `SidebarMenuContent.tsx:384-401`). Quem espera ver o próprio logo no menu sem pagar o módulo vai estranhar.
- **P7 — [handoff, UX] Tela editável sem poder salvar.** Usuário com `screen:settings` sem `can_manage_system` edita tudo e só descobre pelo toast de erro (`useCompanySettings.ts:166-173,224`); o cartão de Usabilidade desabilita os interruptores de servidor (`Settings.tsx:1692,1738`), mas o formulário da Empresa não.
- **P8 — [handoff] Textos fixos fora do i18n:** toasts do CEP (`CepLookup.tsx:33-41`), "Erro ao salvar" (`useCompanySettings.ts:224`), toasts das origens (`useCustomerOrigins.ts:79-138`) e o rótulo "API Pública" (`SettingsWhatsappContent.tsx:156`) ficam em português nos outros 3 idiomas.
- **P9 — Mudanças que re-desenham a tela.** Idioma pessoal (`SettingsRegionalContent.tsx:70-74`), estilo de menu (`SettingsAppearanceContent.tsx:52-53`), tema (`:20-27`) e cor do menu (`:111`) aplicam na hora e persistem (servidor ou navegador). Em vídeo, mostrar e **voltar ao padrão** no mesmo capítulo.
- **P10 — Atalhos são só leitura.** Não dá para trocar teclas; "Shift+letra" navega. Com campo de texto focado não dispara (`SettingsShortcutsContent.tsx:121-123`).
- **P11 — Origens: excluir é imediato, sem confirmação** (`CustomerOriginManagerDialog.tsx:113-114`), e a lista de ícones tem nomes em inglês (`originIcons.tsx:9-13`) [handoff, texto]. Para não mexer no que o T3 usa, criar uma origem temporária e excluí-la na gravação.
- **P12 — "Cobranças (Asaas)" × "Recebimentos (Asaas)".** Mesma tela com dois nomes (`settings.ts:1477,1535`). Usar "Cobranças" ao apontar a subaba e "Recebimentos" ao ler o cartão.
- **P13 — Seed difere do produto real:** `os_stock_consumption_enabled` e `os_finish_revenue_prompt_enabled` já ligados (no produto novo, "Consumo de estoque na OS" nasce desligado), plano com 20 usuários e `white_label_primary_color` ausente.
- **P14 — CEP não preenche Número e Complemento** (`Settings.tsx:942-948`); a fala deve dizer isso (a pessoa completa o número).
- **P15 — Segmento muda o menu.** Um segmento diferente (ex.: elétrica) esconderia a Área do Técnico™ (T18). Por isso é só leitura.
- **P16 — Dois salvamentos independentes.** A aba Regional salva sozinha em 700 ms (`SettingsRegionalContent.tsx:49`) e a Empresa em 800 ms; o selo do topo vem só do `updateSettings` da Empresa e do Regional (mesma mutação), então ambos acendem o mesmo selo.

---

## 6. 🚫 Não prometer / telas mortas / fora de escopo

- 🚫 **Não prometer** "Exibir em documentos" no relatório da OS, proposta, contrato ou PMOC (P2).
- 🚫 O segmento **não** se altera na tela; só a Dominex.
- 🚫 Não existe botão Salvar; não existe "desfazer"; não existe trocar teclas de atalho.
- 🚫 Moeda: trocar **não converte** valores já lançados (aviso fixo, `settings.ts:324`).
- 🚫 Não existe configuração do link de avaliação do Google aqui (vive na NPS da OS, T5).
- 🚫 White Label **não** muda o nome "Dominex" nas telas além do logo/cor/ícone; o rodapé "Desenvolvido por Dominex" some só em documentos.
- ⛔ **Zerar Sistema: só mostrar e cancelar.** O próprio Changelog admite 3 etapas que ainda podem falhar (`Changelog.tsx:1156`).
- ⛔ Não abrir a chave de API da Asaas nem "API Pública" (credenciais). Não conectar WhatsApp real (QR). Não baixar a planilha nem o PDF dos termos (o gravador não grava download).
- ⛔ Textos de plano e preço (Assinatura, "Contratar") ficam fora do vídeo (decisão do Kaik, 30/10 21:55); a janela do módulo não mostra preço, mas é opcional.
- Telas que **não** são do T1: Perfil (`/perfil`), Assinatura, Usuários (T2), Configurações de Contrato (T11), Configurações Financeiras (T13), Configurações do PDV, Configurações fiscais (T14).

---

## 7. Dúvidas em aberto (só rodando o app)

1. O PATCH genérico do backend falso devolve a linha (`.select()`)? Sem isso todo autosave mostra "Erro ao salvar".
2. `processImageFile` redimensiona/converte o logo (formato final)? (`Settings.tsx:535`)
3. O armazenamento falso responde com `Access-Control-Allow-Origin` nos GET de imagem? (a "Imagem ao compartilhar a OS" usa `fetch` com CORS.)
4. O logo e a cor de exemplo do mundo fictício (`rec/fakebase/storage/company-logos/glacial/`) são criação nossa ou o logo/cor reais do cliente Glacial? O código cita a Glacial real e uma cor laranja (`useWhiteLabel.ts:100-101`; `components/ponto/PontoScreen.tsx:172-185`).
5. O botão "Configurações" do rodapé para quem não tem `screen:settings` redireciona para onde? (`App.tsx:360-382`.)
6. O seletor "Meu idioma" recarrega a página ou só troca os textos? (`setUserLanguage`, `SettingsRegionalContent.tsx:70-74`.)
7. Na gravação, o `ColorPicker` abre bem em 1920×1080 (popover de 256 px, `ColorPicker.tsx:160`) e o campo hexadecimal aceita digitar e colar? (a confirmar.)
