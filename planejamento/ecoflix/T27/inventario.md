# Inventário · T27 White Label (EcoSistema 1.59.154)

Código: `/home/claude/ecoflix/app-src-1.59.154/` (`APP_VERSION = "1.59.154"`, `src/config/version.ts:16`). Leitura estática.
Caminhos relativos a `src/`, exceto `supabase/functions/...`. Rótulos entre aspas = texto exato da tela.
Não tem tela própria: é um painel dentro de Configurações → "Empresa".

## 1. Caminho e painel
| O quê | Onde | Rótulos |
|---|---|---|
| Rodapé do menu lateral, ao lado de "Sair" | `components/layout/SidebarMenuContent.tsx:807-820` | "Configurações" |
| `/configuracoes` abre na primeira aba permitida, "Empresa" (`action_config_empresa`) | `pages/Settings.tsx:48-56,72-73`; `lib/configTabsPermissions.ts:5-13` | "Configurações do Sistema" |
| Cartão da aba | `components/settings/SettingsCompanyContent.tsx:292-294` → `components/CompanySettings.tsx:803-816` | "Empresa", "Informações e configurações da sua empresa", seção "Identidade Visual" |
| Painel White Label, coluna da direita, **só com o módulo** `white_label` (`hasModule`, inclui plano e teste) | `components/CompanySettings.tsx:151,1093-1233` | gaveta recolhida "White Label", "Personalize o sistema com sua marca", selo "Ativo" quando ligado |

## 2. Logo e ícone (coluna da esquerda, `components/CompanySettings.tsx:820-1041`)
- "Logo da Empresa": vazio "Nenhum logo enviado", "PNG ou JPG, até 5MB"; com logo, a imagem e os botões "Substituir" e
  "Remover"; "Recomendado: formato horizontal, PNG ou JPG, máximo 5MB". Avisos: "Logo atualizado com sucesso!",
  "Logo removido com sucesso!", "Por favor, selecione uma imagem válida", "Imagem muito grande. Máximo 5MB" (`:713-800`).
- "Ícone da Empresa (1:1)", "Usado no menu lateral quando recolhido (White Label)"; vazio: quadrado tracejado com "1:1";
  com ícone: "Substituir", "Remover"; "Recomendado: formato quadrado (1:1), PNG transparente, 128×128px". Avisos: "Ícone
  atualizado com sucesso!", "Ícone removido com sucesso!", os mesmos dois de arquivo (`:987-1036,1736-1750`).
- Arquivo: `accept="image/*"`, recusa o que não é imagem e acima de 5 MB (`:717-725`, `:994-1001`).

## 3. Interruptor e personalizações (`components/CompanySettings.tsx:1120-1230`)
- Cartão do interruptor: "White Label Ativo" / "White Label Desativado"; "Seu logo está sendo exibido no lugar do logo
  EcoSistema" / "O logo da EcoSistema está sendo exibido". O interruptor fica **desabilitado sem logo** (`:1148`), com o
  aviso âmbar "Faça upload do logo ao lado para poder ativar o White Label" (`:1152-1157`). O toast "Você precisa fazer
  upload do logo primeiro para ativar o White Label" (`:663`) não aparece pela tela (o interruptor já está travado).
- Ligar/desligar (`:659-685`): avisos "White Label ativado! Seu logo agora será exibido em todo o sistema." / "White Label
  desativado."; invalida `["white-label"]` (`:360`): o menu troca na hora para quem ligou.
- Só com ele ligado aparece "Personalizações" (`:1159-1229`): "Nome Exibido no Sistema" (placeholder = nome da empresa);
  "Cor Primária" com o seletor de cor (mostra `#22c55e` vazio), o campo de texto (placeholder "#22c55e"), o quadrado
  "Preview" (só com cor) e "Reset" (só limpa o campo, `:1201`); botão "Salvar Personalizações" ("Salvando..."). Aviso
  "Configurações de White Label salvas!" (`:687-711`; grava `white_label_company_name` e `white_label_primary_color`,
  vazio = nulo).

## 4. Onde a marca aparece
| Lugar | Regra no código |
|---|---|
| Menu lateral aberto: logo da empresa | `components/layout/SidebarMenuContent.tsx:301-343`: com White Label **e** logo (`canUseCustomLogo`); senão o do EcoSistema |
| Menu recolhido: ícone 1:1 | mesmo arquivo `:304`: ícone só com White Label e logo; senão o ícone do EcoSistema. Botão de recolher (ícone de painel, sem texto) no cabeçalho, só em telas de 1280 px ou mais (`components/layout/AppLayout.tsx:102-111`); com o menu recolhido, passar o mouse em cima abre de novo (`components/layout/Sidebar.tsx:26-45`) |
| Cabeçalho | menu superior (`components/layout/TopNavbar.tsx:495-497`) e celular/tablet (`components/layout/AppLayout.tsx:160-163`) |
| Cor | `hooks/useWhiteLabelTheme.tsx:47-102`: troca `--primary`, `--ring`, `--accent`, `--sidebar-primary` e a barra do menu (`--wl-nav-neon`); no tema escuro, a mesma cor um pouco mais clara; sem cor, volta ao padrão |
| Comprovante térmico e A4 | rodapé do EcoSistema (logo + "ecosistematecnologia.com.br") some com `white_label_enabled` (`utils/thermalReceiptGenerator.ts:2428-2447`, `utils/orderReceiptA4Generator.ts:520-523`, `components/ThermalReceipt.tsx:365-380`); o logo da empresa no topo já aparecia sem White Label (`utils/thermalReceiptGenerator.ts:1189-1191`); com White Label, o QR das fotos leva o logo da empresa (`:2402`) |
| PDFs e relatórios | mesma regra do rodapé (`utils/cashClosingPdfGenerator.ts:476`, `utils/financialHistoricoPdfGenerator.ts:216,626`, `utils/materialsExport.ts:168,384`, `components/TransactionHistory.tsx:3254`, entre outros) |
| Portal do parceiro | `pages/EntityPortal.tsx:931-959,1962-1979`: topo na cor e rodapé do EcoSistema fora **só com White Label e Cor Primária** (dados da edge `entity-portal`, `supabase/functions/entity-portal/index.ts:154,766`) |
| Abrir o comprovante | "Pedidos" → no desktop (acima de 1024 px, `hooks/use-mobile.tsx:3`), menu "⋮" da linha (abre no passar do mouse) → "Ver comprovante" (`pages/Orders.tsx:2595-2634`); no celular, botão de olho com o mesmo título (`:2223-2227`); abre janela nova (`:1146-1157`); sem pop-up: "Popup bloqueado. Permita popups para gerar comprovantes." |

## 5. Todos os usuários
`hooks/useWhiteLabel.tsx:28-106`: cache por empresa e realtime em `companies` (UPDATE): quem estiver com o sistema aberto
recebe a troca sem sair. O hook lê o módulo **só** de `company_modules` (`removed_at` nulo, `:49-55`).

## 6. Backend chamado
| Ação | Chamada |
|---|---|
| Abrir o painel | `companies` (`select *`), módulos (`company_modules`, `subscription_plans`) |
| Logo / ícone | storage `avatars` (`remove` do antigo, `upload`, `getPublicUrl`); update `companies.logo_url` / `icon_url` |
| Interruptor | update `companies.white_label_enabled` |
| Personalizações | update `companies.white_label_company_name`, `white_label_primary_color` |
| Menu e cor (todos) | `companies` (`logo_url, icon_url, name, white_label_*`), `company_modules`; canal realtime `white-label:<empresa>:<uuid>` |
| Comprovante | pedido + itens + pagamentos (`pages/Orders.tsx:1159-1200`), `companies` fresca (`hooks/useReceiptPreloader.ts:36-45`); PDF gerado no navegador |

## 7. Achados (código × fonte e handoff)
1. 🚫 confirmado: "Nome Exibido no Sistema" é salvo e lido pelo hook, mas nenhum componente usa `customCompanyName`.
2. ⚠️ confirmados: remover o logo com o White Label ligado não desliga o interruptor (o menu volta ao EcoSistema porque
   pede logo; os documentos olham só `white_label_enabled`); ícone só no menu recolhido e com White Label; "Reset" só
   limpa o campo; 5 MB e só imagem.
3. **Portal**: o rodapé do EcoSistema e a cor do topo só mudam com a Cor Primária preenchida (`pages/EntityPortal.tsx:931`);
   sem cor, o portal fica com o rodapé do EcoSistema mesmo com o White Label ligado. A fonte não diz isso.
4. "Sem logo, o interruptor fica bloqueado": é aviso fixo (âmbar), não mensagem de erro; o toast de erro não tem como
   aparecer pela tela.
5. O botão de recolher o menu não tem texto nem `aria-label` (o robô acha pelo ícone).
6. Continuam do EcoSistema com o White Label ligado: o título da aba do navegador (" | EcoSistema",
   `hooks/usePageTitle.ts:55-56,113`) e o favicon (`index.html:93,154`). A abertura da fonte ("sem a marca EcoSistema
   aparecendo") promete demais; o roteiro diz o que muda.
7. O menu do app é escuro por padrão (`hooks/useNavThemePreference.tsx:29`): o logo da empresa precisa ler bem no fundo
   quase preto do menu e no papel do comprovante. Dentro do menu escuro, a cor entra só na barrinha do item ativo
   (`index.css:301-343,589-591`).
