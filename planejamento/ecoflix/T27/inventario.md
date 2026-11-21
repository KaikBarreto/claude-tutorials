# Inventário · T27 White Label (EcoSistema 1.60.22)

Código: `/dev/shm/ecoflix-src22/src` (`APP_VERSION = "1.60.22"`, `src/config/version.ts:16`). Leitura estática; atualizado em 21/11 (as telas do White Label são as mesmas do 1.59.154; os números de linha abaixo são do 1.59.154 e andaram pouco).
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
  EcoSistema" / "O logo da EcoSistema está sendo exibido". O interruptor fica **desabilitado só quando não há logo e o White Label está
  desligado** (`disabled={... (!logo_url && !white_label_enabled)}`, `:1145`; **corrige** a cobertura de 20/11, que dizia que ele trava também
  ligado), e o aviso âmbar "Faça upload do logo ao lado para poder ativar o White Label" (`:1150-1155`) aparece sempre que não há logo, ligado ou
  desligado. O toast "Você precisa fazer
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

## 8. 1.60.22: o que a aula passou a cobrir (cobertura de 20/11, conferida no código de 21/11)
| O quê | Onde | Rótulo / regra |
|---|---|---|
| Sem o módulo a gaveta não existe; no teste ele vem liberado | `CompanySettings.tsx:151,1093` (`hasModule`); `hooks/useCompanyModules.tsx:323-329` (`isTrial` libera tudo); `supabase/functions/self-register/index.ts:564` | cap01 L3 |
| Sem ícone, o menu recolhido usa o ícone do EcoSistema | `SidebarMenuContent.tsx:300-304` (`iconSrc = (canUseCustomLogo && companyIcon) ? companyIcon : logoIcon`) | cap02 L6 |
| Menu escuro por padrão; saída: Configurações → "Aparência" → "Menu (lateral e superior)" → "Seguir o tema" ("Claro no tema claro, escuro no escuro") | `hooks/useNavThemePreference.tsx:29`; `components/settings/SettingsAppearanceContent.tsx:82-134`; aba `#tab-btn-appearance` (`pages/Settings.tsx:41`) | cap03 L8 e L9 (só aponta; clicar muda a aparência da conta) |
| A cor só entra se o código começar com "#" (sem ele o tema não aplica nada, e o "Salvar Personalizações" avisa "salvas" do mesmo jeito) | `hooks/useWhiteLabelTheme.tsx:5-6,52-55`; `CompanySettings.tsx:687-711` não valida | cap04 L4. A cobertura dizia também "seis caracteres": o código só confere o "#", então a fala só diz o "#" |
| Desligar: "White Label desativado."; somem o selo e as "Personalizações"; menu, cor e rodapé dos documentos voltam; a cor fica guardada (o desligar só grava `white_label_enabled`) | `CompanySettings.tsx:659-685`; `useWhiteLabel.tsx:62-70` (`primaryColor` só com `effectiveWhiteLabel`) | cap06 L2 a L4 |
| Remover o logo: "Remover logo da empresa?" / "O logo personalizado será removido e o logo padrão (símbolo de reciclagem) será usado nos comprovantes." / "Cancelar" / "Remover"; "Logo removido com sucesso!"; área "Nenhum logo enviado" / "PNG ou JPG, até 5MB". Ligado e sem logo: o menu volta ao EcoSistema (`canUseCustomLogo` falso), o cartão segue "White Label Ativo" e o aviso âmbar aparece; os documentos seguem sem o rodapé (`white_label_enabled`) | `CompanySettings.tsx:775-795,873-890,1698-1718`; `useWhiteLabel.tsx:66`; `utils/priceTableGenerator.ts:344` | cap06 L5 a L7 |
| Outros documentos sem o rodapé: tabela de preços, ticket de pesagem, fechamento de caixa e relatórios | `priceTableGenerator.ts:344`, `weighingTicketGenerator.ts:478-482`, `cashClosingPdfGenerator.ts`, `cashClosingHtmlGenerator.ts` | cap05 L3 (ilustração) |
| O QR das fotos leva o logo da empresa no meio com o White Label e o logo (sem eles, o ícone do EcoSistema) | `utils/qrCode.ts:5-23,89-98`; opção do QR é do T1 | cap05 L5 (ilustração; o pedido do robô não tem foto) |
| Portal: topo na cor e rodapé do EcoSistema fora só com White Label **e** cor; o comprovante baixado pelo parceiro depende só do interruptor (`white_label_enabled` volta da edge) | `pages/EntityPortal.tsx:937-965,1983`; `supabase/functions/portal-order-receipt/index.ts:193,533` | cap05 L6 e L7 (ilustração; a página é do T20) |
| Cadastro do rosto no ponto: logo e cor da empresa com o White Label | `pages/FaceEnrollment.tsx:53-56` | cap05 L8 (ilustração; a tela é do T19) |
| Logo da nota fiscal é outro campo ("Logo para Nota Fiscal", "Aparecerá no DANFE (máx. 200KB).") na página "Configuração Fiscal" | `components/notas-fiscais/EmpresaSection.tsx:683-686`; `pages/ConfiguracaoFiscal.tsx:1355` | cap05 L8 (ilustração; a tela é do T16) |
| Comprovante de pedido que nasceu de ticket mostra "Ticket: <nome>" e "Caixa: <nome>" no lugar de "Operador"; assinatura segue `receipt_signature_mode` | `utils/orderReceiptA4Generator.ts:801-802`; `thermalReceiptGenerator.ts` (assinaturas) | cap05: usar pedido sem ticket |
| Canal realtime renomeado `company-updates:<empresa>:<uuid>` (a fala continua certa) | `hooks/useCompanyUpdateSubscription.ts:20-23` | cap07 |
