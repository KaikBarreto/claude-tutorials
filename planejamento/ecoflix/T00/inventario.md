# Inventário · T0 · Bem-vindo ao EcoSistema

Código lido: EcoSistema **1.60.10** (cópia em `/dev/shm/ecoflix-src`), atualizado em 18/11 a partir do inventário do 1.59.154 e da
`cobertura_160.md` (as linhas citadas abaixo das seções 1 a 9 são as do 1.59.154, salvo as da seção 10, que são do 1.60.10).
Caminhos relativos a `src/`. Rótulo entre aspas = texto exato da tela (pt-BR). Só o que a aula usa.
A cópia não traz `supabase/migrations`: o que as RPCs fazem por dentro vem da fonte (que conferiu os ⚠️) e do front.

## 1. Introdução obrigatória (o "portão" do primeiro acesso)
- **Onde:** sobreposição em tela cheia, montada no `AppLayout` e na rota da aula (`App.tsx:623-624`).
  Componente `components/ecoflix/EcoFlixIntroGate.tsx` (diálogo `:214-355`).
- **Rótulos:** cabeçalho com o logo do EcoSistema e o selo "Primeiro passo" (`:233`); "Antes de usar o sistema" (`:274`);
  "Bem-vindo, {primeiro nome}" (`:277`); "Este vídeo explica os combinados importantes da nossa parceria e mostra como
  aproveitar os tutoriais." + no teste "Você pode assistir agora ou pular por enquanto durante o teste." / contratada
  "Assista até o final para continuar." (`:280-285`).
  Quadro: no teste "Você pode pular durante o teste" + "Seu progresso fica salvo. Se contratar sem concluir, este vídeo
  volta como etapa obrigatória."; contratada "Falta concluir suas boas-vindas" + "Depois de concluir, esta etapa não será
  exibida novamente." (`:290-299`).
  Caixa "Assisti ao vídeo até o final e entendi os combinados." (desligada até o vídeo terminar, `:300-314`).
  Botão "Assista até o final para confirmar" → "Confirmar e começar a primeira aula" (`:316-336`).
  Só no teste e antes de terminar o vídeo: "Pular por agora" (`:337-350`).
  Erro (não usado): "Não foi possível salvar sua confirmação. Tente novamente." (`:157`).
- **Regras do código:** "Pular por agora" grava o ponto em `localStorage` (`ecoflix:intro-trial-skipped:<user>:<episode>`) e
  em `save_ecoflix_progress` (`:161-183`); confirmar chama `acknowledge_ecoflix_intro` e leva à próxima aula da trilha
  (`getEcoFlixContinueUrl`, `:146-159`). No celular, toca o vídeo vertical do episódio, se houver (`:62`, `mobile_video_id`).
- **Backend:** RPC `get_ecoflix_learning_status` (`hooks/useEcoFlix.ts:457-470`, campos `user`, `progress`, `introGate`,
  `track`: `:121-157`); RPC `acknowledge_ecoflix_intro` (`:481-490`); RPC `save_ecoflix_progress` (`:576`); tabelas
  `ecoflix_episode_subtitles`, `ecoflix_episode_resources` (`:499-500`), `ecoflix_episodes` (vídeo vertical, `:529`).

## 2. EcoFlix · a trilha (`/ecoflix`)
- **Onde:** menu da conta → "Tutoriais | EcoFlix" (`components/layout/SidebarMenuContent.tsx:732-739`). Página
  `pages/Tutoriais.tsx` (layout `components/ecoflix/EcoFlixLayout.tsx`, abas "Início", "Módulos", "Lives", "Minha Lista").
- **Rótulos (computador):** "Olá, {nome} · continue sua trilha" (`:469`); título "Aprenda a usar o EcoSistema" (trilha de
  boas-vindas, `:134-136`); botão "Começar trilha" / "Continuar trilha" (`:485-488`); "Trilha do seu plano" + % (`:544-548`);
  "{n} de {total} aulas concluídas · Formação básica {n}%" (`:563`); busca "Buscar aula"; por módulo: capa, selo, "{feitas}/{total}",
  "Módulo {n}", título; por aula: "Próxima aula recomendada", "Concluída", "Na sequência da formação básica", "Na sequência do
  seu plano", "Conheça este módulo", "Em andamento" (`:686-696`).
- **Selos** (`components/ecoflix/EcoFlixModuleBadge.tsx`): "Formação básica" (`:15-20`), "Tem no seu plano" / "Não tem no seu
  plano" (`:32-40`), no teste para módulo fora do plano "Liberado no teste" (`:23-29`).
- **Aula fora da ordem** (`:718-746`): diálogo "Consultar fora da ordem?" · "Sua próxima aula recomendada continuará marcada na
  trilha." · "Você pode abrir “{aula}” agora para resolver uma dúvida pontual sem alterar a sequência recomendada." · botões
  "Voltar à trilha" e "Consultar esta aula". Abre para toda aula ainda não feita depois da primeira pendente (`:101-106`).
- **Celular** (`:249-460`): mesmo cabeçalho; cartão "Trilha do seu plano", "{n} de {total} aulas", "Formação básica: {n} de
  {total} · {n}%" e o botão "Começar pelos tutoriais" / "Continuar de onde parei" (`:308-339`); lista "Sequência recomendada" ·
  "Aulas da trilha". **No celular a lista não mostra os selos** (o selo aparece na página da aula e em "Ver trilha").
- **Backend:** RPC `get_ecoflix_learning_status` (`p_path_slug` "tutoriais-do-sistema"); `ecoflix_titles`, `ecoflix_seasons`,
  `ecoflix_episodes`, `ecoflix_user_progress`, `ecoflix_watchlist` (`hooks/useEcoFlix.ts`).

## 3. EcoFlix · a página da aula (`/ecoflix/assistir/:titulo/:n`)
- **Onde:** `pages/EcoFlixWatch.tsx:577-723`. Computador: painel da trilha à esquerda (`:580-582`) + player + detalhes.
  Celular: barra "Voltar" e "Ver trilha" (`:602-605`), que abre a gaveta "Sua trilha de tutoriais" (`:718-723`).
- **Painel da trilha** (`components/ecoflix/EcoFlixTrackPanel.tsx`): "Voltar ao sistema" (`:38`), "Voltar para todos os módulos"
  (`:43`), "Sua trilha" (`:45`), "Trilha do seu plano" + % (`:47-48`), "Formação básica {n}%" (`:53`); antes do primeiro módulo
  fora do plano: "Conheça outros módulos" · "Você pode assistir e contratar direto pela aula." (`:58-63`); aulas numeradas
  "{módulo}.{aula}".
- **Detalhes** (`components/ecoflix/EcoFlixLessonDetails.tsx`): selo (`:69`), "{módulo} · Aula {n}" (`:70`), título, descrição;
  módulo fora do plano: cartão "Conheça agora. Ative quando fizer sentido." · "Esta aula está liberada, mas a função {módulo}
  ainda não faz parte do seu plano." + (contratada) "O valor de catálogo é R$ …/mês; a confirmação mostrará o valor exato antes
  de qualquer cobrança." + botão "Adicionar ao meu plano" (teste: "Escolher meu plano"; sem permissão: "Peça ao administrador
  da empresa") (`components/ecoflix/EcoFlixModuleOffer.tsx:96-118`); botão verde "Tirar dúvidas com o suporte" (`:79-88`), que
  abre o WhatsApp do suporte com a mensagem pronta (`:45-55`: "Olá, equipe de suporte! Preciso tirar uma dúvida sobre a aula
  {n} — {aula}, da EcoFlix." + "E-mail do usuário", "Empresa", "Trilha", "Módulo", "Aula", "Minha dúvida:"); "Materiais e
  extras" (`:91`).
- **Backend:** o mesmo da trilha + `ecoflix_episode_subtitles` / `ecoflix_episode_resources`; o player toca `youtube` ou `drive`
  (`EcoFlixWatch.tsx:1066-1067`, `<video>` do Drive `:1669-1697`).

## 4. Menu do computador (lateral) e menu da conta
- **Itens** (`config/routes.ts:412-489`, rótulos traduzidos por `i18n/locales/pt-BR/navigation.json`):
  "Dashboard"; "Financeiro" (Caixa, Histórico do Caixa, Movimentações Bancárias ou "Movimentações Financeiras" com a Conta
  Dinheiro ligada (`hooks/useFinancialMovementsLabel.ts`), Relatório Financeiro, Contas a Pagar/Receber, Categorias
  Financeiras); "Pedidos"; "Fiscal & Ambiental" (Notas Fiscais (NF-e), SPED Fiscal "BETA", Notas de Serviço (NFS-e),
  Transporte (MDF-e), Ambiental (MTR/CDF), **Relatório/Estoque Fiscal** (1.60.18: `routes.ts:510`, rota `/fiscal-ambiental/estoque-fiscal/posicao`; substitui "Estoque Fiscal" e "Relatórios Fiscais"; o SPED não aparece no mundo)); "Materiais" (Estoque, "Histórico (Kardex)", Relatório, Ticket de
  Pesagem, Produção); "Coletas & Logística" (Ordens de Coleta, Frota, Equipamentos, Rastreamento, Rotas, Relatório,
  Configurações); "Clientes e Fornecedores"; "Funcionários (RH)"; "CRM/Kanban"; "Agenda"; depois de um traço, "Gerencial
  (Filiais)" (só com o módulo `modulo_gerencial`, `SidebarMenuContent.tsx:260`). Um grupo aberto por vez (`:234-238`).
- **Rodapé do menu** (`SidebarMenuContent.tsx:615-850`): cartão do usuário (aria "Menu da conta", `:628`) com nome, selo
  "MASTER" (dono, `company_admin`) e empresa; botões "Configurações" (`:819`) e "Sair" (`:828`).
- **Menu da conta** (sobe acima do cartão): "Meu Perfil" (`t('navigation:profile')` = "Meu Perfil", `:683-688`),
  "Assinatura" (`:690-696`), "Tema" → "Claro", "Escuro", "Sistema" (`:698-728`), "Tutoriais | EcoFlix" (`:732-739`),
  "Central de Ajuda" (`:42-54`, abre a gaveta com "Pesquisar artigos...", `components/help-center/HelpCenterSheet.tsx:206`),
  "Falar com o Suporte" (`:743-749`, abre "Falar com o suporte", `components/support/SupportTriageDialog.tsx:405`) e o cartão
  da conta (troca de conta).
- **Meu Perfil** (`/perfil`, `pages/Profile.tsx:125-185`): "Meu Perfil", "Alterar Foto", "Nome Completo", "Segurança".

## 5. Menu superior e Aparência
- `components/layout/TopNavbar.tsx` (barra no topo, mesmo menu da conta em `:616-760`), ligado por `profiles.navigation_style`
  ('sidebar' | 'topbar', `hooks/useNavigationPreference.tsx`; `AppLayout.tsx:260,391,399`). Só no computador (≥ 1280 px).
- **Configurações → "Aparência"** (`pages/Settings.tsx:41`; `components/settings/SettingsAppearanceContent.tsx:17-77`):
  "Estilo de Navegação (Desktop)" · "Escolha entre menu lateral ou menu superior. Esta opção só afeta a visualização em
  desktop." · "Menu Lateral" ("Sidebar tradicional à esquerda") e "Menu Superior" ("Barra horizontal no topo").
  Toast: "Estilo de navegação alterado para Menu Superior" (`useNavigationPreference.tsx:50`).
- **Backend:** `UPDATE profiles SET navigation_style`.

## 6. Celular
- **Barra de baixo** (`components/layout/MobileBottomNav.tsx:23-27`): "Início", "Caixa", "Novo" (botão do meio: "Compra",
  "Ticket de pesagem", "Nota Fiscal", "Venda", `:40-43`), "Estoque", "Menu".
- **"Menu"** (`components/layout/MoreMenuDrawer.tsx`): cartão do usuário; as mesmas áreas do menu, em grupos que abrem;
  seção "Conta" (`:433`) com "Perfil", "Assinatura", "Tutoriais | EcoFlix", "Central de Ajuda", "Falar com o Suporte"
  (`:257-286`); rodapé com "Tema" (Claro/Escuro, `:483-512`), "Configurações" (`:542`) e "Sair" (`:553`).

## 7. Configurações → Usabilidade (os nomes cliente e fornecedor)
- `components/settings/SettingsUsabilityContent.tsx:427-462`: "Usabilidade" · "Nomenclatura de clientes e fornecedores" ·
  "Personalize somente os nomes exibidos, sem alterar cadastros ou regras do sistema" · interruptor "Inverter os termos Cliente
  e Fornecedor" · "Compra: Fornecedor → Cliente. Venda: Cliente → Fornecedor. Compras, vendas, vínculos, saldos e documentos
  fiscais continuam com a mesma lógica." · "A mudança vale para todos os usuários desta empresa e para novos comprovantes e
  relatórios." Na aula: **só olhar**, sem ligar.

## 8. Assinatura (`/assinatura`)
- **Onde:** menu da conta → "Assinatura". Página `pages/Billing.tsx` (permissão `screen_assinatura`, `App.tsx:428-432`).
- **Topo** (`:358-597`): "Assinatura" · "Gerencie seu plano, módulos e pagamentos"; nome da empresa + selo de status ("Ativa";
  "Vence em breve" com ≤ 7 dias; "Vencida"); "Plano {nome} • {n} módulos" (`:429`; plano `personalizado` = "Personalizado",
  `:64`); "{n} dias restantes" (`:433`, conta em dias inteiros até `subscription_expires_at`, `:282-292`); "Vencimento"
  dd/mm/aaaa (`:441-447`); "Valor mensal" (anual: "Valor a pagar") com o valor e "/mês" (`:468-481`); "Formas de pagamento"
  "PIX", "Boleto", "Cartão" (`:500-520`); botão "Pagar Agora" (`:523-538`, leva a `/checkout?mode=renewal`); sem permissão,
  o mesmo botão com cadeado, desligado, dica "Você não tem permissão para gerenciar assinatura" (`:572-590`).
  Teste (`subscription_status` testing): só o cartão "Ative sua Assinatura" + "Escolher Plano e Ativar" (`:365-418`).
- **"Uso da conta"** (`components/billing/AccountUsageCard.tsx:72-140`): "Acompanhe o consumo do seu plano"; "Usuários"
  {cadastrados} / {limite}; "{2} incluídos + {n} adicionais" (`:103-105`); com o módulo de notas: "Notas fiscais este mês"
  e o limite do nível (`:113-138`).
- **Faixas** (`Billing.tsx:600-676`): cartão recorrente: "Débito recorrente ativo no cartão de crédito" · "Sua assinatura será
  cobrada automaticamente todo mês. Para cancelar, use a opção "Cancelar Assinatura"." (só com `asaas_subscription_id` e um
  pagamento de cartão recebido); cadastro incompleto: "Dados pendentes para emissão de notas fiscais" (a aula não mostra).
- **"Plano & módulos"** (`components/billing/ModulesManagementCard.tsx:441-602`): "Plano {nome} • {n} módulos • Mensal" e o
  valor "/mês"; no mensal, "Economize R$ … por ano" · "Mude para o plano anual e pague 12 meses com 20% de desconto (Pix ou
  Boleto)." (`:474-487`); "Módulos ativos" (`:493`); "Adicione ao seu plano" (só se faltar módulo, `:520`); "Gerenciar plano"
  (`:581`, abre "Montar plano") e "Cancelar assinatura" (`:597`); sem permissão: "Peça ao administrador da empresa para alterar
  o plano." e sem o botão de cancelar (`:584-586`).
- **"Histórico de Pagamentos"** (`Billing.tsx:685-760`, `components/shared/PaymentHistoryList.tsx`): cartões em carrossel,
  "Renovação • {empresa}", forma ("PIX", "Boleto", "Cartão"), selo "Pago" (`:105-107`), nota da assinatura: "Baixar PDF" /
  "Baixar XML" / "Solicitar Nota Fiscal" / "Nota disponível após o pagamento"; com CNPJ ou endereço faltando, o toast
  "Complete seu cadastro para emitir a nota" (`:236`, a aula só fala).
- **Citados, não abertos:** cancelar (`components/billing/CancelSubscriptionModal.tsx:478-484`: "Sua assinatura será cancelada
  ao final do período atual", "Você continuará tendo acesso até o vencimento"); limite de usuários
  (`components/UserLimitModal.tsx:385,410`: "Sua equipe cresceu! 🎉", "Nova mensalidade (estimada):", "Seu plano será
  convertido para Personalizado"); mudança de plano (`lib/billing/subscriptionChange.ts:224-236`: "Pagamento proporcional",
  "O novo plano é liberado depois que o pagamento for confirmado"); Pix Automático (`components/billing/PixPaymentView.tsx:220-254`;
  **nasce ligado** no checkout, `pages/Checkout.tsx:183-190`).
- **Backend:** `profiles`, `companies` (`subscription_status`, `subscription_plan`, `subscription_value`, `billing_cycle`,
  `subscription_expires_at`, `max_users`, `extra_users`, `nfe_tier`, `asaas_subscription_id`, `cnpj`, `email`, `contact_name`,
  `phone`), `company_modules`, `subscription_modules`, `subscription_plans` (`hooks/useCompanyModules.tsx:120-205`),
  `subscription_payments` e `company_payments` (`Billing.tsx:146-162`), `nfe_module_tiers` + RPC
  `count_fiscal_documents_in_month` (`hooks/useNfeTier.tsx`).

## 9. Dashboard (`/dashboard`), só como ponto de partida do tour
- `pages/Dashboard.tsx`; título "Olá, {nome}!" (`i18n/locales/pt-BR/dashboard.json`). A aula não lê números dele (é o T25).

## Fonte × código (vale o código)
1. Menu: a fonte diz "Fiscal e Ambiental", "Coletas", "Funcionários", "Gerencial"; a tela diz "Fiscal & Ambiental", "Coletas &
   Logística", "Funcionários (RH)", "Gerencial (Filiais)" (e há "CRM/Kanban", que a fonte não lista no tour).
2. Menu do avatar: a fonte diz "Perfil" e "Ajuda"; no computador é "Meu Perfil" e "Central de Ajuda" (no celular, "Perfil").
3. Sem permissão: a fonte diz que "Pagar Agora" e "Cancelar assinatura" ficam com cadeado; no código, "Pagar Agora" fica com
   cadeado e **"Cancelar assinatura" some** ("Gerenciar plano" vira "Peça ao administrador da empresa para alterar o plano.").
4. Pix: a fonte diz que a cobrança automática só existe se o cliente **ligar** o Pix Automático; no checkout ele **nasce ligado**
   (decisão de 14/10/2026), e funciona se o banco aceitar.
5. Sem rota de Guia Técnico no app: a ajuda por escrito dentro do sistema é a "Central de Ajuda".

## 10. O que entrou com o 1.60.10 (conferido na tela em 18/11)
- **Cato** (`components/cato/CatoFab.tsx`): botão redondo fixo, nome "Abrir o Cato" (computador: canto inferior direito; celular: inferior
  esquerdo, acima da barra); com dica pendente, "Abrir 1 notificação do Cato". **Balão de dica** 15 s depois de a tela abrir (`:24-27,244-278`),
  some em 11 s, com a frase, o link "Abrir Cato" e o xis "Fechar dica do Cato"; calado por `localStorage`
  `cato_adoption_nudge_<empresa>_<usuário>` = `{"count":16,...}`. Sem o aceite da empresa, o clique abre **"Antes da primeira conversa com o
  Cato"** · "Leia rapidinho como ele trata os dados da sua empresa." (`CatoAiConsentDialog.tsx`), com os itens "O Cato lê os dados da sua
  conta pra te responder…", "Quer falar em vez de digitar? O microfone só liga quando você toca nele…", "O Cato pode errar…". Painel (só com
  aceite; é da T21): "Cato.ai — agente de IA da EcoSistema", "Pergunte ao Cato…", botão "Falar". RPC `track_cato_adoption_event`.
- **Cabeçalho**: botões "Buscar" (Ctrl + K) e "Notificações" (nomes acessíveis conferidos na tela).
- **Menu da conta**: "Tema" abre "Claro", "Escuro", "Sistema"; "Central de Ajuda" abre a gaveta com "Pesquisar artigos..."; "Falar com o
  Suporte" abre "Falar com o suporte" · "Nos conte o que está acontecendo pra resolvermos mais rápido." · "Ver vídeos" / "Ver artigos" ·
  "Em qual tela/módulo? *" · "O que aconteceu? Descreva com detalhes *" · "Você já assistiu aos nossos tutoriais sobre isso? *" (Sim / Não)
  · "Falar no WhatsApp"; o cartão do fim ("Trocar de conta") abre "Apenas essa conta está salva. Use "+ Adicionar conta" pra incluir outra.",
  "Adicionar conta" e "Sair de todas as contas"; "Sair" no rodapé, ao lado de "Configurações".
- **Celular, "Novo"** (`MobileBottomNav.tsx:41-68`): leque em duas fileiras, "Compra" e "Venda" embaixo, "Ticket de pesagem" e "Nota Fiscal" em cima.
- **EcoFlix**: abas "Início", "Módulos", "Lives", "Minha Lista"; "Buscar aula" na trilha. **Player** (`pages/EcoFlixWatch.tsx`): "Ativar ou
  escolher legenda" → "Legendas" · "Escolha a faixa e ajuste como o texto aparece." ("Sem legendas", a faixa, "Tamanho da legenda", "Estilo da
  legenda"); "Velocidade de reprodução: 1x"; "Voltar 10 segundos"; "Avançar 10 segundos"; "Reproduzir próxima aula"; "Abrir em tela cheia".
  No fim do vídeo: "Aula concluída" · "Vamos para a próxima" · "A próxima aula começa em {n} segundos." (avança sozinho em 4 s; o mouse por
  cima pausa) · "Ficar nesta aula" / "Próxima aula agora" (`:449-455,665-694`). "Materiais e extras" nos detalhes. Tabelas
  `ecoflix_episode_subtitles` e `ecoflix_episode_resources` (fora do `schema.json`: entram pela semente da T0).
- **Assinatura**: "· Nível {n}" ao lado do módulo de notas em "Módulos ativos" (`ModulesManagementCard.tsx:505-507`); "Adicione ao seu plano"
  com o cartão do módulo que falta e o botão próprio (CRM: "Ativar meu CRM"); no teste, só "Ative sua Assinatura" e "Escolher Plano e Ativar".
  **"Montar plano"** · "Monte seu plano e veja como fica ao vivo": "Voltar aos planos", "Escolha os módulos" (9 cartões com valor),
  "Nível de Notas Fiscais" (Nível 1, 2, 3), "Usuários adicionais" ("3 usuários", "2 base + 1 extra"), resumo "SEU PLANO", "Ciclo" Mensal /
  Anual, "Total mensal", "Ver valor e aplicar"; em "Voltar aos planos": "Plano Start", "Plano Avançado", "Plano Master" e "Personalizado"
  ("Escolha módulo por módulo e monte o plano do seu jeito"). Reabre sempre a partir da assinatura vigente (`:331-343`).
  **"Cancelar Assinatura"** · "Nos ajude a entender o motivo": "Motivo do cancelamento" (8 motivos); em "Preço muito alto", "Não estou
  usando o suficiente", "Faltam funcionalidades que preciso" e "Dificuldade em usar o sistema" aparece o cartão com "Falar com o Sucesso do
  Cliente" (nos outros quatro motivos, não); "Continuar" → "Confirmar cancelamento" · "Tem certeza que deseja cancelar?" · "Ao confirmar:"
  (5 itens) · "Que tal reduzir seu plano?" (oferta com valores) · "Voltar" / "Confirmar Cancelamento".
  Histórico: o cartão se chama "Cobrança • {empresa}"; "Nota nº", "Baixar PDF", "Baixar XML"; sem nota, "Solicitar Nota Fiscal".
