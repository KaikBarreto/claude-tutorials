# Inventário · T1 · Sua conta e sua empresa (EcoSistema 1.59.154)

Levantado em 10/11/2026 contra `/home/claude/ecoflix/app-src-1.59.154/` (`src/config/version.ts:16`, `APP_VERSION = "1.59.154"`).
Análise estática, só leitura. Caminhos relativos a `src/`, exceto `supabase/...`. Rótulo entre aspas = texto exato do código
(pt-BR). Onde o código e a fonte (`trecho_aula.py T1`) discordam, vale o código: ver "Divergências" no fim.

## 1. Cadastro · `/cadastro` (página pública)
`pages/Registration.tsx` (rota `App.tsx:356`). Logo do EcoSistema no topo, título "Cadastro" (`:1206`), subtítulo
"Teste grátis por ${trialDays} dias · Sem compromisso · Acesso total" (`:1213`; `trialDays` = `?dias=` do link, senão 7, `:351`).
- Etapas (`:399-405`): visitante orgânico (sem `?origem`, `?vendedor`, `?afiliado`, `?ref`) vê só **"Dados"** e **"Acesso"**;
  "Origem" aparece em link de afiliado sem origem travada; "Plano" e "Pagamento" só na venda direta (`?tipo=venda`).
- Barra "Preenchimento obrigatório" com a porcentagem dos 6 campos obrigatórios (`:1255-1277`).
- **Dados** (`:1282-1404`): "Nome da Empresa*" (placeholder "Ex: Minha Empresa Ltda"), "Seu Nome Completo*" ("Ex: João Silva"),
  "Email*" ("email@exemplo.com"), "Telefone*" ("(21) 98765-4321", máscara ao digitar), link "Recebeu um código de indicação?"
  (abre "Código de indicação", "Ex: ECO-ABC123"). **Não há campo de CNPJ nem de endereço na tela** (o estado existe, sem campo).
- Botão "Continuar" (→ "Verificando..." enquanto checa o e-mail na edge `self-register` com `check_email_only`, `:1113-1132`).
  Erros: "Por favor, preencha todos os campos obrigatórios", "Email inválido", "Este email já está em uso. Faça login ou use outro email.".
- **Acesso** (`:1842-1931`): caixa "Email de acesso: <e-mail>", "Senha*" (placeholder "Mínimo 8 caracteres", indicador de força
  `PasswordStrengthIndicator`), "Confirmar Senha*" ("Digite a senha novamente"); cartão **"Teste Grátis · Acesso Total"** com
  "**${trialDays} dias grátis** com acesso a todos os módulos" e "**5 usuários** inclusos durante o teste" (`:1886-1903`).
  Botões "Voltar" e **"Criar Conta"** (→ "Cadastrando..."). Aviso "Ao criar sua conta, você concorda com os Termos de Uso e a
  Política de Privacidade." (`:2143-2164`; "Termos de Uso" abre `TermsOfServiceModal` só leitura). Rodapé "Já tem uma conta? Fazer Login".
- Validação da senha: mínimo 8 no campo (`:1856-1859`; o toast de reserva diz 6, `:1161`), "As senhas não coincidem" (`:1157`).
- Sucesso (teste): toast "Cadastro realizado com sucesso! Redirecionando...", login automático (`signInWithPassword`) e `/inicio`
  (`:828-843`). Erros: "Esse e-mail já possui uma conta no sistema. ..." (`:888`).
- Backend: edge **`self-register`** (`:725-768`; manda `company_name`, `company_email`, `company_phone`, `contact_name`,
  `password`, `link_type: 'teste'`, `trial_days`, `terms_version`...); `supabase.auth.signInWithPassword`.
- Na página também há o botão flutuante do WhatsApp (`WhatsAppFloatingButton`, `:2212`) e o seletor de tema (`AuthThemeToggle`).

## 2. Login · `/login` (página pública; `/auth` redireciona)
`pages/Auth.tsx` (rota `App.tsx:352`), textos em `i18n/locales/pt-BR/auth.json`. Título "Acesse sua conta", "Entre para continuar
no EcoSistema." (`:999-1003`). À direita, `LoginShowcase`.
- "E-mail *" (placeholder "seu@email.com"), "Senha *" ("••••••••", olho "Mostrar senha"), caixa **"Lembrar de mim"**, link
  **"Esqueci minha senha"**, botão **"Entrar"** ("Entrando..."), "Ou", botão **"Entrar com Google"**, "Ainda não tem conta?
  Cadastre-se" (`:1125-1272`).
- "Entrar com Biometria" só aparece com `biometricState.available && enrolled` (`:1274-1297`); `enrolled` exige linha em
  `biometric_credentials` do usuário **já logado** (`hooks/useBiometricAuth.tsx:18-49`) e **nenhuma tela chama `enrollBiometric`**
  na 1.59.154: na prática o botão não aparece. Fora da fala.
- Google (`:436-451`): só entra em conta que já existe; e-mail Google sem conta volta para o login com "Este e-mail Google ainda
  não possui uma conta no EcoSistema. Faça seu cadastro primeiro.".
- Erros: "Email ou senha incorretos. Verifique suas credenciais e tente novamente.", "Múltiplas tentativas falhadas. ...".
- Outro acesso ativo na última hora → `SessionConfirmDialog` (`:666-674`, `:1317-1326`). Sem toast de sucesso; vai para `/inicio`
  (`:756-831`).
- Backend: `supabase.auth.signInWithPassword`, `active_sessions` (select), `profiles.must_change_password`, `user_roles`; edge
  `password-reset` (`check_first_access`) quando a senha falha.

## 3. Esqueci minha senha (dentro do `/login`)
`components/ForgotPasswordFlow.tsx`. Títulos com `uppercase` na tela.
- Passo e-mail (`:145-185`): "Voltar ao login", "Recuperar Senha", "Informe o email da sua conta e enviaremos um código de
  verificação.", campo "E-mail", botão **"Enviar Código"** ("Enviando..."). Toast: "Se o email existir no sistema, um código será
  enviado. Verifique sua caixa de entrada." Backend: edge **`password-reset`** `{action: 'send', email}`.
- Passo código (`:188-246`): "Verificar Código", "Digite o código de 6 dígitos enviado para <e-mail>", 6 casas (`InputOTP`),
  caixa laranja "Não recebeu? Confira também a pasta de Spam / Lixo Eletrônico do seu email" (o texto segue com travessão:
  não ler), botão **"Verificar"**, "Reenviar código em {n}s" (60 s) → "Reenviar código". Toasts: "Código verificado com
  sucesso!" / "Código inválido ou expirado. Tente novamente.". Backend: `supabase.auth.verifyOtp({type: 'recovery'})`.
- Passo nova senha (`:249-336`): "Nova Senha", "Defina sua nova senha. Use no mínimo 6 caracteres.", "Nova Senha",
  "Confirmar Nova Senha", botão **"Alterar Senha e Entrar"** ("Alterando..."). Toast "Senha alterada com sucesso! Você já está
  logado.". Backend: `supabase.auth.updateUser({password})`, `profiles.update({must_change_password: false})`.

## 4. Menu: card com o nome, Configurações, trocador de contas
`components/layout/SidebarMenuContent.tsx` (menu lateral, o padrão).
- Rodapé do menu (`:618-830`): card "Menu da conta" com avatar, nome (2 primeiras palavras), selo **"MASTER"** (coroa,
  `company_admin`) e o nome da empresa; embaixo, os botões **"Configurações"** (→ `/configuracoes`) e **"Sair"**.
- Clique no card abre o menu (acima): "Perfil" (→ `/perfil`), "Assinatura", "Tema" ("Claro", "Escuro", "Sistema"),
  "Tutoriais | EcoFlix", Central de Ajuda, "Falar com o Suporte" e, no fim, o card do trocador ("Trocar de conta": avatar, nome,
  "MASTER", e-mail, empresa).
- Trocador (`components/account-switcher/AccountSwitcherDropdown.tsx`): o card cresce e mostra a conta ativa (botão "Sair desta
  conta"), as outras contas salvas ou "Apenas essa conta está salva. Use "+ Adicionar conta" pra incluir outra." (`:360`),
  **"Adicionar conta"** (até 5: `lib/savedSessions.ts:41`; depois "Limite de 5 contas atingido", tooltip com travessão) e
  "Sair de todas as contas" (confirmação "Sair de todas as contas?"). "Adicionar conta" salva a sessão atual, sai só deste
  navegador e abre o login (`hooks/useSavedSessions.tsx:243-259`); trocar usa o `refresh_token` salvo, sem senha (`:92-188`).

## 5. Configurações · `/configuracoes`
`pages/Settings.tsx` (rota `App.tsx:567`, permissão `screen_configuracoes`). Trilha "Configurações", título "Configurações do
Sistema", "Personalize as preferências e comportamento do sistema" (`i18n/.../settings.json`). Abas na ordem
(`lib/configTabsPermissions.ts:5-13`): **"Empresa"**, "Usuários e Permissões", **"Usabilidade"**, **"Condições de Pagamento"**,
**"Aparência"**, "Integrações", **"Atalhos"** (layout `components/SettingsSidebarLayout.tsx`, `desktopVariant="underline"`).

## 6. Aba Empresa
`components/settings/SettingsCompanyContent.tsx` → `components/CompanySettings.tsx` (cartão "Empresa", "Informações e
configurações da sua empresa", `:808-809`). **Salva sozinho** 800 ms depois de cada mudança (`:609-631`, update em `companies`);
o botão **"Salvar alterações"** grava na hora com o toast "Configurações salvas" (`:593-607`, `:1643-1668`). Indicador "Salvando...".
- **"Identidade Visual"** (`:816-1235`): "Logo da Empresa" (vazio: "Nenhum logo enviado", "PNG ou JPG, até 5MB"; com logo:
  "Substituir", "Remover"; "Recomendado: formato horizontal, PNG ou JPG, máximo 5MB"; toasts "Logo atualizado com sucesso!",
  "Imagem muito grande. Máximo 5MB"); "Ícone da Empresa (1:1)" ("Usado no menu lateral quando recolhido (White Label)",
  "Recomendado: formato quadrado (1:1), PNG transparente, 128×128px", toast "Ícone atualizado com sucesso!"); **"Nome da
  Empresa"** e **"CNPJ/CPF"** (placeholder "00.000.000/0000-00", máscara `cpfCnpjMask`), cada um com a chave **"Exibir nos
  documentos"**. Storage `avatars` (upload) + update `companies.logo_url` / `icon_url`.
- White Label (`:1093-1233`, só com o módulo `white_label`): cartão recolhido "White Label", "Personalize o sistema com sua
  marca". **Só menção** (aula T27).
- **"Informações de Contato"** (`:1240-1265`): "Telefone" ("(00) 00000-0000") e "E-mail" ("contato@empresa.com"), cada um com
  "Exibir nos documentos".
- **"Endereço"** (`:1270-1434`): "Endereço da empresa", botão "2º endereço", chave "Exibir nos documentos" (do endereço todo);
  campos (`components/AddressFields.tsx`) "CEP" ("00000-000"), "Estado", "Cidade", "Logradouro", "Número", "Bairro",
  "Complemento" ("Sala, Galpão, etc. (opcional)"); nota "É este endereço que sai na nota fiscal. A Configuração Fiscal usa
  exatamente o que estiver aqui."; **"Prévia no comprovante"** com as caixas "Logradouro", "Número", "Complemento", "Bairro",
  "Cidade/UF", "CEP" (caixa de campo vazio fica apagada); "Fuso horário" (preenchido pelo estado).
  CEP de 8 dígitos → edge **`cep-lookup`** (`components/CepLookup.tsx:49`) → toast "Endereço encontrado!" e foco no "Número";
  a lista de cidades vem do IBGE por `fetch` direto (`components/StateCitySelector.tsx:71`,
  `servicodados.ibge.gov.br/.../municipios`). Cidade sem código IBGE: aviso "Escolha a cidade na lista. ..." e o save
  manual avisa "Escolha a cidade na lista para gravar o código do IBGE ..." (os dois com travessão). O save também grava
  `company_fiscal_config` (endereço), chama a edge `geocode-company` e, se houver `asaas_customer_id`, a `sync-asaas-customer`.
- "Ticket de Pesagem" (`:1438-1464`): "Compartilhar rascunhos de tickets entre operadores" (fica para o T8).
- **"Numeração de pedidos"** (`:1469-1596`): "Reinício da numeração" ("Nenhum (segue direto)", "Mensal (zera todo mês)",
  "Anual (zera todo ano)"); "Formato do número" com os modelos "Padrão", "Barras", "Pontos", "Ano/Nº", "Zeros", cada um com o
  exemplo do pedido 30 na data de hoje (`lib/orderNumber.ts:11-27`: em 10/11/2026 saem "#30", "30/11/26", "30.11.26", "26/30",
  "0030"); campo do formato; "Exemplo: <número>"; "Variáveis disponíveis:"; chave **"Numeração separada para compras e
  vendas"** ("Cada tipo passa a ter sua própria contagem."), que ao ligar pede "Ativar numeração separada?" ("Compras e vendas
  passarão a contar separadamente. Os números vão refletir só o volume de cada tipo, então podem parecer menores que o número
  atual. Os pedidos que você já fez não mudam. Deseja ativar?", "Cancelar" / "Ativar", `:1672-1695`).
- **"Comprovantes e Documentos"** (`:1598-1641`): "Frase Personalizada" com a chave "No comprovante", caixa de texto
  ("Ex: Obrigado pela preferência! Volte sempre.", até 2000), contador "<n>/2000 caracteres", **"Alinhar à esquerda"**
  ("Por padrão a frase sai centralizada. Ative para alinhar à esquerda (bom para textos longos).").
- Abaixo do cartão (`SettingsCompanyContent.tsx`): "Filial" ("É Filial", T22), "Moedas" (só com multimoeda ligada no banco:
  não aparece), **"Segurança"** / "Alterar Senha" (`:543-568`), **"Termos de Uso"** / "Ver Contrato" / "Aceito em <data>"
  (`:571-598`), "Histórico de Exclusões" / "Ver histórico" (`:601-625`), **"Zona de Perigo"** / "Zerar Sistema" (`:628-659`).

## 7. Aba Usabilidade
`components/settings/SettingsUsabilityContent.tsx` ("Usabilidade", "Configure preferências gerais de usabilidade do sistema", `:428`).
Cada chave salva na hora (sem botão).
- **"Nomenclatura de clientes e fornecedores"** (`:432-464`): "Inverter os termos Cliente e Fornecedor" ("Compra: Fornecedor →
  Cliente. Venda: Cliente → Fornecedor. Compras, vendas, vínculos, saldos e documentos fiscais continuam com a mesma lógica.",
  "A mudança vale para todos os usuários desta empresa e para novos comprovantes e relatórios."); ao mexer, abre "Inverter
  Cliente e Fornecedor?" ("Apenas os nomes visíveis mudam. Nenhum cadastro, pedido, saldo ou vínculo será alterado. ...",
  "Cancelar" / "Confirmar alteração", `:1381-1423`). Grava pelo `useEntityTerminology`.
- **"Caixa"** (`:469-594`): **"Multi-Caixas"** ("Cada operador abre e gerencia seu próprio caixa. Se desativado, toda a empresa
  compartilha um único caixa."; toast "Multi-caixas ativado" ou "Multi-caixas desativado", update `companies.multi_cash_enabled`);
  "Rastreabilidade do dinheiro físico (Cofre)" (o cofre do T6; não mexer); **"Formato do Comprovante"** ("Layout do
  comprovante para cada tipo de dispositivo (preferência por usuário)") com "Computador" e "Celular/Tablet", cada um
  "Térmico (58/80mm)" ou "A4 (PDF em folha)"; toast "Formato no computador: A4 (PDF em folha)" (`:155-181`, `profiles.receipt_format_*`).
- **"Pedidos e Pagamentos"** (`:599-1116`): **"Forma de Pagamento Padrão"** ("Forma de pagamento pré-selecionada ao finalizar
  pedidos": "Dinheiro", "Pix/Transferência", "Perguntar sempre"; tooltip "Define qual opção vem marcada ao finalizar: "Dinheiro"
  abre direto no caixa, "Pix" no banco, "Perguntar" exibe o modal."); "Permitir Edição de Itens"; **"Arredondar Pagamentos"**
  ("Arredonda o valor para baixo, ignorando centavos (ex: R$100,50 → R$100,00). Configure separadamente para vendas e compras.",
  chaves "Na Venda" e "Na Compra"; tooltip "Ex: Uma compra de R$347,85 será paga como R$347,00. Os R$0,85 ficam como saldo a
  pagar para o fornecedor."); "Múltiplas Tabelas de Preço"; **"Impureza/Tara Desconta no Valor"** ("Impureza desconta tanto no
  estoque quanto no valor do pedido"; tooltip "Ex: Compra de 100kg com 5kg de impureza. Ativo: paga 95kg. Desativado: paga
  100kg, mas estoque recebe 95kg."); **"Lucro no Comprovante"** ("Exibe o lucro estimado no PDF do comprovante de venda";
  tooltip "... Visível apenas para usuários com a permissão Ver Projeção de Lucro."); "Mostrar só peso líquido"; "Assinaturas
  no comprovante"; "Marca de ticket não valorizado"; "QR de fotos no comprovante" (só com `portal_cliente`); "Estilo do
  comprovante térmico" ("Compacto", "Nome em destaque"); **"Exigir cliente/fornecedor no Ticket de Pesagem"** ("Quando ligado, o
  funcionário não consegue salvar um ticket sem escolher o cliente ou fornecedor."; toast "Ticket de Pesagem passa a exigir
  cliente/fornecedor"; tooltip "... Vale para todos os usuários da empresa."); "Permitir forma de pagamento no ticket de pesagem".
- **Onde grava:** forma de pagamento, edição de itens, arredondar, múltiplas tabelas, impureza/tara no valor e lucro no
  comprovante vão para o **perfil de quem está logado** (`hooks/usePaymentPreferences.tsx:118-161`, `profiles`, save silencioso;
  as telas de pedido leem do usuário logado, `components/OrderFormInputs.tsx:363-371`). Multi-Caixas, peso líquido, assinaturas,
  estilo térmico e exigir parceiro no ticket vão para `companies`. Formato do comprovante: `profiles` (a tela diz).
- "Regionalização" ("Idioma do Sistema", "Moeda do Sistema"), "Agenda" ("Exibir Feriados"), "Guia de configuração"
  ("Reativar guia de configuração"): fora da aula.
- O prefixo do código do material **não está nesta aba** na 1.59.154: fica no cadastro de cada material (T3).

## 8. Aba Condições de Pagamento
`pages/config/CondicoesPagamentoTab.tsx` (dados: `hooks/usePaymentConditions.ts`, tabela `payment_conditions`).
- Título "Condições de Pagamento", "Defina parcelamentos padrão (à vista, 30/60/90…) para agilizar vendas e compras a prazo.",
  botão **"Nova condição"** (`:183-194`). Lista vazia: "Nenhuma condição cadastrada ainda." e "Criar primeira condição" (`:201-211`).
- Janela **"Nova condição de pagamento"** ("Defina o nome e as parcelas. A soma dos percentuais precisa ser 100%.", `:315-336`):
  **"Nome *"** ("Ex: 30/60/90 dias"), caixas **"Definir como condição padrão"** e **"À vista (parcela única, 0 dias, 100%)"**
  (**nasce marcada**, `:84-91`; com ela marcada as linhas e o "Adicionar parcela" ficam travados), "Parcelas", **"Adicionar
  parcela"**, colunas "Dias após emissão" e "% do total" (aceita vírgula), lixeira "Remover parcela", **"Soma dos
  percentuais"** (verde quando dá 100%, vermelha senão), botões "Cancelar" e **"Criar condição"** ("Salvar" ao editar).
- Validações (`:131-158`): "Informe o nome da condição", "Parcela N: dias deve ser um número inteiro maior ou igual a zero",
  "Parcela N: informe um percentual maior que zero", "A soma dos percentuais deve ser 100%. Atual: X%".
- Lista (`:213-309`): nome, selo **"Padrão"** (estrela), "Inativa", resumo "30 / 60 / 90 dias · 3 parcelas", botão "Padrão"
  (estrela, só nas outras ativas), chave ativa/inativa, "Editar", "Excluir" ("Excluir condição?"). Toasts "Condição criada",
  "Condição definida como padrão".
- Onde aparece depois: painel "Configurar faturamento" → "Condição de pagamento" (`components/InstallmentsConfigDialog.tsx:259-283`):
  "Manual (definir parcelas)" e as condições ativas, a padrão no topo da lista com " (padrão)" no nome (ordem do hook,
  `usePaymentConditions.ts:58-61`). **Não vem escolhida sozinha** (abre em "manual", `:134`).

## 9. Abas Aparência e Atalhos
`components/settings/SettingsAppearanceContent.tsx` ("Aparência", "Personalize a interface visual do sistema"):
- **"Estilo de Navegação (Desktop)"**: "Menu Lateral" ("Sidebar tradicional à esquerda", padrão) / **"Menu Superior"** ("Barra
  horizontal no topo"); grava em `profiles.navigation_style` (`hooks/useNavigationPreference.tsx`).
- **"Menu (lateral e superior)"**: "Escuro (recomendado)" (padrão, "Menu escuro mesmo no tema claro") / "Seguir o tema";
  `localStorage`.
- **"Tema do Sistema"**: miniaturas "Tema Claro" / "Tema Escuro" (`next-themes`). O mesmo "Tema" está no menu do card.
`components/settings/SettingsShortcutsContent.tsx` ("Atalhos de Teclado", "Use atalhos para acessar funcionalidades rapidamente"):
- Chave "Atalhos de Teclado" ("Atalhos estão ativados"); "Navegação" ("Clique na tecla para personalizar"): Dashboard,
  Compra, Venda, Caixa, Pedidos, Ver Estoque, Configurações, Funcionários (RH), Fiscal & Ambiental, Agenda, cada um
  "Shift" + letra (D, C, V, X, P, E, S, F, N, A; `hooks/useKeyboardShortcuts.ts:23-35`); "Geral": "Busca Global" "Ctrl+K";
  "Dicas" ("Atalhos não funcionam quando você está digitando em campos de texto"). Trocar a letra: toast 'Tecla alterada para "X"'.
- **Ctrl+K** abre a paleta (`components/CommandPalette.tsx:615-760`): "Buscar páginas, clientes, fornecedores, materiais,
  funcionários...", grupos "Ações Rápidas", "Resultados da Busca", "Navegação"; busca em `customers`, `suppliers`,
  `balances`, `materials` (`ilike name`), `employees` (`:286-420`).

## 10. Empresa, parte de baixo: senha, termos e Zona de Perigo
- "Segurança" ("Gerencie suas configurações de segurança e acesso") → "Alterar Senha" ("Atualize sua senha de acesso ao
  sistema") → botão "Alterar Senha" → janela `components/ChangePasswordDialog.tsx` "Alterar Senha" ("Digite sua nova senha
  abaixo. Certifique-se de usar uma senha forte."), "Nova Senha", "Confirmar Nova Senha", "Cancelar" / "Alterar Senha"
  (mínimo 6; toast "Senha alterada com sucesso!"; `supabase.auth.updateUser`). O mesmo botão está em `/perfil`.
- "Termos de Uso" ("Consulte o contrato de termos de uso do sistema") → **"Ver Contrato"**, embaixo "Aceito em DD/MM/AAAA às
  HH:MM:SS" (`profiles.terms_accepted_at`, `hooks/useTermsOfService.tsx`; formato `utils/brtDate.ts:145-162`). Janela
  `components/TermsOfServiceModal.tsx` "Termos de Uso e Responsabilidade" / "CONTRATO DE TERMOS DE USO E RESPONSABILIDADE",
  "Versão ... · Atualizado pela última vez em ...", "Aceito em ...", botões "Baixar PDF" e "Fechar" (modo leitura, `:221-242`).
- **"Zona de Perigo"** ("Ações irreversíveis. Revise cuidadosamente antes de confirmar.") → "Zerar Sistema" ("Exclui dados
  operacionais selecionados. Dados da empresa e usuários são preservados. Toda operação fica registrada em log de
  auditoria.") → **"Tem certeza?"** ("Você está prestes a acessar a função de zerar o sistema. Esta ação pode excluir
  permanentemente dados operacionais da sua empresa.", "Deseja continuar para selecionar o que será excluído?", "Cancelar" /
  "Sim, continuar") → `components/ResetSystemDialog.tsx` **"Zerar Sistema - Ação Irreversível"** (não fecha clicando fora):
  "Selecionar tudo" e as 10 caixas (todas **marcadas** ao abrir, `:93-95`): "Clientes e Fornecedores", "Saldos de Clientes e
  Fornecedores", "Cadastro de Materiais", "Estoque de Materiais", "Movimentações Financeiras", "Categorias Financeiras", "Contas
  a Pagar e Receber", "Funcionários e Movimentações", "Pedidos (Vendas e Compras)", "Notas Fiscais e Config. Fiscal"; "O sistema
  voltará ao estado inicial, como se a empresa tivesse acabado de ser criada."; "Serão mantidos: Dados básicos da empresa,
  Usuários cadastrados, Histórico de pagamentos."; "Esta ação NÃO PODE ser desfeita!"; "PARA CONFIRMAR, DIGITE O NOME DA
  EMPRESA:" + o nome + campo "Nome da empresa"; "Cancelar" / "Sim, Zerar Sistema" (travado até o nome bater). Backend
  (não chamar): RPCs `reset_company_audit_start` e `reset_company_step`.

## 11. Perfil · `/perfil` e Instalar · `/instalar`
- `pages/Profile.tsx`: "Meu Perfil", "Informações do Perfil", "Alterar Foto", "Nome Completo", "E-mail" (travado), "Salvar",
  "Segurança" ("Altere sua senha de acesso quando necessário") + "Alterar Senha". Só citado na aula (menu do card).
- `pages/Install.tsx` ("Instalar App", textos `i18n/.../install.json`): nenhum link no menu leva a ela e nenhum capítulo da
  fonte usa; a tela promete "Funciona Offline". **Fora da aula.**

## 12. Chamadas ao backend usadas na aula
| Tela | Chamada |
|---|---|
| Cadastro | edge `self-register` (`check_email_only` e cadastro), `auth.signInWithPassword` |
| Login | `auth.signInWithPassword`, `active_sessions`, `profiles`, `user_roles`; edge `password-reset` (`check_first_access`, só se a senha falhar) |
| Esqueci a senha | edge `password-reset` (`send`), `auth.verifyOtp` (`recovery`), `auth.updateUser`, `profiles.update` |
| Trocador | `localStorage` (sessões salvas) e `auth.refreshSession` (só ao trocar) |
| Empresa | `companies` (select/update), storage `avatars` (upload, `getPublicUrl`), edge `cep-lookup`, `fetch` IBGE (municípios), `company_fiscal_config` (select/insert/update), edge `geocode-company`, edge `sync-asaas-customer` (só com `asaas_customer_id`) |
| Usabilidade | `profiles` (preferências), `companies` (multi-caixa etc.), `useEntityTerminology` |
| Condições de Pagamento | `payment_conditions` (select/insert/update) |
| Aparência / Atalhos | `profiles.navigation_style`, `localStorage`; paleta: `customers`, `suppliers`, `balances`, `materials`, `employees` |
| Termos / senha | `profiles.terms_accepted_at`; `auth.updateUser` |

## 13. Divergências (fonte × código 1.59.154; vale o código)
1. **Aviso fixo de cadastro incompleto**: a fonte diz que "um aviso fica fixo no topo do sistema" enquanto falta o CNPJ. Na
   1.59.154 não há esse aviso: a chave `address-incomplete-check` só é invalidada (`CompanySettings.tsx:361`,
   `hooks/useFiscalConfig.tsx:189`), nenhum componente a lê. O que existe é a cobrança da nota da assinatura pedindo CNPJ,
   endereço e e-mail (`supabase/functions/request-subscription-nfse/index.ts:60-73`). A fala não cita aviso.
2. **Biometria**: sem tela para cadastrar (`enrollBiometric` sem uso) e o botão só aparece com o usuário já logado. Fora da fala.
3. **"Exibir no comprovante"**: o rótulo das chaves é **"Exibir nos documentos"**; a do endereço é uma só, e campo a campo
   são as caixas da "Prévia no comprovante".
4. **Prefixo do material** (⚠️ da fonte): não fica na Usabilidade; fica no cadastro de cada material (`pages/Materiais.tsx`,
   `components/materiais/BulkMaterialPrefixDialog.tsx`). Vai para o T3.
5. **Condição padrão**: aparece no topo da lista com "(padrão)", mas não vem escolhida sozinha no faturamento.
6. **Opções de pedido da Usabilidade** (forma de pagamento padrão, edição de itens, arredondar, múltiplas tabelas,
   impureza/tara no valor, lucro no comprovante): gravam no **perfil de quem está logado**, e a tela não diz. A fala avisa.
7. Login: o rótulo é "Lembrar de mim" e "E-mail" (a Central de Ajuda diz "Lembrar-me" e "Email").
8. Cadastro: a senha pede no mínimo 8 no campo; trocar a senha (logado ou pelo código) pede no mínimo 6.
9. Rotas da fonte: `/instalar` não tem capítulo (fora); o "card com o seu nome → Configurações" é, no menu lateral, o botão
   "Configurações" logo abaixo do card (no Menu Superior, fica dentro do menu da conta, `components/layout/TopNavbar.tsx:729`).
