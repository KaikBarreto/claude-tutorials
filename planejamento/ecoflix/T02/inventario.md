# Inventário · T2 Usuários e permissões (EcoSistema 1.59.154)

Código: `/home/claude/ecoflix/app-src-1.59.154/` (`APP_VERSION = "1.59.154"`, `src/config/version.ts:16`). Leitura estática.
Caminhos relativos a `src/`, exceto `supabase/functions/...`. Rótulos entre aspas = texto exato da tela.

## 1. Caminho até a aba
| O quê | Onde | Rótulos |
|---|---|---|
| Botão no rodapé do menu lateral, ao lado de "Sair" | `components/layout/SidebarMenuContent.tsx:807-820` | "Configurações" |
| Página `/configuracoes` (gate da rota: `screen_configuracoes`) | `pages/Settings.tsx:36-46,94-130` | título "Configurações do Sistema", "Personalize as preferências e comportamento do sistema" (`i18n/locales/pt-BR/settings.json:2-3`); abas "Empresa", "Usuários e Permissões", "Usabilidade", "Condições de Pagamento", "Aparência", "Integrações", "Atalhos" |
| `/configuracoes?tab=users`; `/gerenciar-usuarios` redireciona | `pages/Settings.tsx:38,74-75`; `App.tsx:472` | |
| Cada aba tem a sua permissão (a de usuários: `action_manage_users`) | `lib/configTabsPermissions.ts:5-13,24-26` | sem nenhuma aba: "Você não tem permissão para nenhuma seção de Configurações." (`pages/Settings.tsx:113-118`) |
| Cabeçalho da aba | `components/settings/SettingsUsersContent.tsx:9-14` | "Usuários e Permissões", "Gerencie usuários da empresa, papéis e permissões de acesso" |

## 2. Tela da equipe (`pages/UserManagement.tsx`, `embedded`)
- Topo `:933-955`: "Empresa: <nome>", selo "{ativos} / {limite} usuários", "Relatório por Usuário", "Criar Usuário".
- Lista `components/settings/UsersMasterDetail.tsx:182-259`: "Usuários", "N encontrado(s)", busca "Buscar por nome ou e-mail";
  linha com coroa (master), e-mail e "Acesso total · Ativo" ou "N permissões · Ativo"/"· Inativo" (`:246-253`).
- Menu "..." da linha (`aria-label "Ações de <nome>"`, abre no passar do mouse, `:95-128`): "Editar", "Tornar master",
  "Desativar"/"Ativar", "Excluir". Regras `pages/UserManagement.tsx:899-911`: Desativar/Ativar em todo usuário que não é
  master; Excluir só para o master, nunca em si mesmo nem no master; Tornar master só o master atual, em usuário ativo.
- Detalhe `UsersMasterDetail.tsx:270-362`: "Master", "Ativo"/"Inativo", "Editar"; "Perfil de acesso" (nome do perfil ou
  "Personalizado", "N permissões configuradas individualmente."); "Última atividade" ("Online agora", "há ...", "Sem
  atividade registrada"); "A conta pode acessar o sistema." / "A conta está impedida de entrar."; "Permissões
  concedidas": "Este usuário tem acesso a todas as telas e ações disponíveis nos módulos contratados pela empresa." ou
  "Telas (n)" e "Ações (n)". Vazio: "Selecione um usuário", "Escolha alguém na lista para consultar dados, atividade e
  permissões."

## 3. Janela de criar e editar (`pages/UserManagement.tsx:960-1163`)
- Título "Criar Novo Usuário" / "Editar Usuário"; "Preencha os dados do novo usuário" / "Atualize os dados e permissões
  deste usuário"; rodapé "Cancelar" e "Criar Usuário" ("Criando...") / "Atualizar" ("Salvando...").
- Coluna esquerda: "Dados do usuário", "Identificação, acesso e foto usada no sistema."; "Foto do Usuário" + "Selecionar
  foto" ("Foto opcional para o novo usuário"; no editar, "Clique para adicionar ou alterar a foto", sobe na hora);
  "Nome Completo"; "Email"; "Senha" / "Nova Senha (opcional)" (editar: "Deixe em branco para manter").
  Força da senha (`components/PasswordStrengthIndicator.tsx:15-30`): "Senha fraca/média/boa/forte. Deve conter:",
  "Pelo menos 8 caracteres", "Pelo menos 1 número", "... letra minúscula", "... letra maiúscula", "... caractere especial".
- Coluna direita: "Permissões", "Escolha um perfil rápido ou ligue telas e ações individualmente. Cada tela é um grupo —
  expanda para ver as ações dela." (travessão é da tela; a fala não lê); "Tela inicial" ("Automática (última tela
  acessada)" + só as telas ligadas; "Só aparecem telas liberadas acima. Se a permissão mudar, o sistema escolhe outra
  tela válida.").
- Editor `components/settings/PermissionsEditor.tsx`: "Perfis rápidos" com "Acesso Total", "Operador Padrão",
  "Somente Visualização" e o selo âmbar "Personalizado" quando a seleção não bate com nenhum (`:115-145`); busca "Buscar
  tela ou ação..." (`:151-155`); blocos "Geral", "Financeiro", "Materiais", "Cadastros", "Sistema"
  (`config/routes.ts:404-409`); por tela: interruptor (`aria-label "Acesso à tela X"`), "Clique para ver N ações",
  selo "x/N" (`:226-276`); dentro: "Ações desta tela" (`:317-319`); com a tela desligada: "A tela está desligada, mas
  estas ações continuam valendo por conta própria." (`:320-325`); bloco escuro do Cato no fim, "Quem pode conversar com
  o assistente" + "Atenção: ..." (`:363-441`).
- Catálogo `config/routes.ts:102-297`. Usados na aula: telas "Dashboard", "Caixa", "Movimentações Bancárias",
  "Relatório Financeiro", "Contas a Pagar/Receber", "Pedidos", "Fiscal & Ambiental", "Clientes e Fornecedores",
  "Ticket de Pesagem", "Funcionários (RH)"; ações "Ver Totais e Valores Financeiros" (Geral: "Visualizar saldo
  bancário, totais e projeções de lucro"), "Registrar Venda", "Ver Dinheiro Total em Caixa", "Ver Projeção de Lucro"
  ("Ver a projeção de lucro na finalização de compras e vendas, no resumo do caixa, no relatório de materiais e na ficha
  do parceiro"), "Criar Ticket de Pesagem com Valores", "Gerenciar Contas Bancárias", "Conciliar Extrato Bancário",
  "Criar Conta a Pagar/Receber", "Dar Baixa em Conta", "Emitir NF-e (Produto)", "Emitir NFS-e (Serviço)", "Ver saldos
  de cliente/fornecedor", "Gerenciar Usuários".
- Perfis `config/routes.ts:306-401`: "Acesso Total" ("Acesso completo a todas as telas e funções"), "Operador Padrão"
  (12 telas + 20 ações, "Acesso às operações do dia-a-dia sem funções administrativas"; inclui valores e projeção de
  lucro, não inclui "Criar Ticket de Pesagem com Valores" nem "Movimentações Bancárias"), "Somente Visualização" (14
  telas + 2 ações de ticket e "Ver Custos na Produção"; "Apenas visualização, sem permissão para editar ou excluir").
- Avisos: "Usuário criado com sucesso!" (`:372`), "Usuário atualizado com sucesso!" (`:450`), "Permissões atualizadas! O
  usuário precisa fazer login novamente para ver as mudanças." (`:480`), "Foto atualizada com sucesso!" (`:636`),
  "Usuário desativado!" / "Usuário ativado!" (`:513`), "Controle transferido para <nome>" (`:571`).

## 4. Excluir, master e limite
- Excluir (`components/DeleteUserConfirmDialog.tsx:61-113`): "Excluir usuário", "Esta ação é irreversível", "Você está
  prestes a excluir permanentemente o usuário <nome>.", "Para confirmar, digite o email do usuário:", "Email de
  confirmação", "Cancelar", "Excluir Usuário" (só liga com o e-mail digitado igual).
- Tornar master (`pages/UserManagement.tsx:1244-1271`): "Passar o controle da empresa?", "Você vai tornar <nome> o novo
  master da empresa. <nome> passará a ter controle total e você deixará de ser o master (mantém suas permissões atuais,
  mas não poderá mais transferir o controle nem ficará protegido contra exclusão). Esta ação é imediata.", "Cancelar",
  "Sim, passar o bastão".
- Limite (`hooks/useCompanyModules.tsx:229-233,308-311,347`): conta só usuários **ativos**; plano `personalizado` usa
  `max_users` como total. Sem vaga, "Criar Usuário" abre `components/UserLimitModal.tsx:407-418`: "Sua equipe cresceu!
  🎉", "Seu plano inclui até N usuários. Adicione quem falta por R$25/usuário ao mês ...", "Usuários cadastrados",
  "Adicionar usuários extras" (− e +), "R$25,00 por usuário adicional/mês", "Novo limite de usuários:", "Valor acrescido
  (estimado):", "Nova mensalidade (estimada):", "Valor estimado — o valor exato é calculado no servidor ao confirmar.",
  "Seu plano será convertido para Personalizado", "Cancelar", "Continuar".

## 5. Valores escondidos (para a fala do cap09)
- `hooks/usePermissions.tsx:302-314`: "Ver Totais e Valores Financeiros" libera os totais; o lucro pede também "Ver
  Projeção de Lucro" (`pages/Purchase.tsx:511-516`, `pages/Sale.tsx:458-462`: só o lucro depende delas, o preço fica).
- Caixa sem valores mostra "R$ ••••••" (`pages/Caixa.tsx:496,3401-3484`).
- Ticket de Pesagem: valor aparece com "Criar Ticket de Pesagem com Valores" **ou** "Ver Totais e Valores Financeiros"
  (`lib/weighingTicketPermissions.ts:52-60`).
- Módulo vale mais que a permissão, até no acesso total (`hooks/usePermissions.tsx:210-277`; "Funcionários (RH)" pede o
  módulo `funcionarios`, `hooks/useCompanyModules.tsx:29`); telas de módulo não contratado nem entram no editor
  (`pages/UserManagement.tsx:103-116`). "Registrar Venda" sozinha: `/venda` exige a tela "Caixa" (`App.tsx:478-482`).

## 6. Backend chamado
| Ação | Chamada |
|---|---|
| Listar | `profiles` (+ `user_permissions`), `user_roles`, `active_sessions` (a cada 30 s), contagem de `profiles` ativos, `companies` (`max_users`, `subscription_plan`, `subscription_value`) |
| Criar | edge `create-company-user` (`supabase/functions/create-company-user/index.ts`): auth + `profiles.company_id` + `user_roles` operator + `user_permissions`; resposta `{success, user:{id,email,full_name}}` (`:327-336`); erros "Esse email já é usuário desta empresa." e "Esse email já está em uso em outra empresa. ..." |
| Editar | `profiles` (`full_name`, `initial_screen_path`); edge `manage-company-users` `update_email` (vai sempre, o e-mail vem preenchido) e `update_password` (só com senha nova, mínimo 6); RPC `save_user_permissions(p_user_id, p_permissions, p_preset)` |
| Foto (editar) | storage `avatars` (upload + `getPublicUrl`) e `profiles.avatar_url` (`:604-644`) |
| Desativar / Ativar | `profiles.is_active` (`:503-521`) |
| Excluir | edge `manage-company-users` `delete_user` (recusa o master e a si mesmo) |
| Tornar master | RPC `transfer_company_master(_new_master_user_id)` |
| Limite: "Continuar" | edge `change-subscription` (cotação); a aula não clica |

## 7. Achados (código × fonte e handoff)
1. **Foto e tela inicial da criação nunca gravam**: a tela lê `result.userId` (`pages/UserManagement.tsx:328,337`), mas a
   edge devolve `user.id`. A fonte diz "nem sempre sobe"; no código não sobe nunca. A aula coloca a foto e a tela
   inicial no "Editar" (é onde gravam).
2. **Perfil rápido não fica gravado na criação**: a edge só insere as linhas de permissão, sem `permission_preset`;
   logo depois de criar com "Operador Padrão", o detalhe diz "Personalizado" (o editar recalcula e mostra "Operador
   Padrão"). Na criação com "Acesso Total" a lista diz "N permissões", não "Acesso total".
3. **Tela desligada**: a fonte diz que a ação com a tela desligada "não adianta nada"; o editor diz "continuam valendo
   por conta própria". Vale o código: algumas valem sozinhas ("Usar Contas Bancárias" no "Operador Padrão", sem a tela
   "Movimentações Bancárias"); "Registrar Venda" sem a tela "Caixa" não leva a lugar nenhum (`App.tsx:478-482`). A fala
   usa só o exemplo do Caixa.
4. Excluir: a edge aceita quem tem "Gerenciar Usuários", a tela mostra o botão só ao master. A fala segue a tela.
5. A janela do limite mostra o preço do usuário extra e a mensalidade estimada (dado real de preço na tela).
