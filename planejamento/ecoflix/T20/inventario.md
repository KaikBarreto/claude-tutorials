# Inventário · T20 · Portal do Cliente e Fornecedor

Código 1.59.154 (`/home/claude/ecoflix/app-src-1.59.154/`, `src/config/version.ts:16`), leitura estática. Caminhos relativos a
`src/`, menos `supabase/...`. Rótulo entre aspas = texto exato da tela. Só o que a aula usa.

## 1. Clientes e Fornecedores › ficha ao lado (`/clientes-fornecedores`)
- Lista, abas "Clientes"/"Fornecedores" e ficha ao lado: como no `T04/inventario.md` (seções 1 e 5).
- `components/clients-suppliers/ClientsListView.tsx`
  - Aba "Visão geral" da ficha, bloco **"Acesso ao portal"**: o link num campo só de leitura (`aria-label` "Link do portal") e o
    botão **"Copiar"** (`:398-410`); toast **"Link do portal copiado"** · "O endereço está pronto para compartilhar." (`:232-240`).
    Sem token: "Portal ainda não configurado para este cadastro."
  - Menu "..." da ficha: "Editar", "Excluir", **"Portal do Cliente"** / **"Portal do Fornecedor"** (copia o mesmo link) e "Nova
    Movimentação" (`:124-162`); a cópia é `hooks/usePartnerActions.tsx:561-573` (toast "Link do portal copiado").
  - Botões "Editar" e "Nova Movimentação" no cabeçalho da ficha (`:296-310`).
- Formato do link (`utils/publicLinkSlug.ts`, `buildEntityPortalPath`): `/portal/<empresa>-<primeiro nome do parceiro>-<código de
  22 letras>` → `/portal/recicla-vale-metais-cooperativa-…` e `/portal/recicla-vale-metais-fundicao-…`. O código é o
  `portal_token` (um por cadastro, gerado na criação quando a empresa tem o módulo, `components/EntityFormDialog.tsx:603-610`).
- Página cheia `/cliente/...` (`pages/PartnerDetail.tsx:313-324`) tem o botão "Copiar link do portal": **a aula não usa** (a ficha
  da lista é o caminho da T4).

## 2. Editar › aba "Portal" (`components/EntityFormDialog.tsx`)
- Janela "Editar Fornecedor"; abas "Dados de Contato", "Dados Fiscais", **"Portal"** (`:1211-1225`). Sem o módulo `portal_cliente`,
  a aba mostra só a contratação (`:1918-1919`, `settings/PortalModuleUpsellCard.tsx`): não aparece na aula.
- **"Portal do Fornecedor"** · "Página só de leitura com o histórico, saldo e notas deste fornecedor." (`:1925-1931`);
  **"Link do portal"** + ícone "Copiar link" (toast "Link copiado", `:969-979`) + ícone "Abrir portal" (aba nova) (`:1934-1956`).
- **"Exigir senha"** · "Quando ligado, o portal pede usuário e senha antes de mostrar os dados." (`:1988-1997`); chave **"Pedir login
  no portal"** (`:2002`); ligada: **"Usuário"** (placeholder "ex: joao.silva") e **"Senha"** ("Defina uma senha") (`:2021-2045`);
  botão **"Salvar acesso"** (ligada) / "Remover login" (desligada) (`:2047-2050`); toasts **"Acesso salvo"** / "Login removido",
  "Informe o usuário do portal", "Erro ao salvar o acesso do portal" (`:1001-1031`). Parceiro duplo: "Este parceiro é cliente e
  fornecedor: o acesso vale pros dois links." (`:2015-2019`). Edge `portal-set-credentials` (grava `portal_password_enabled`,
  `portal_username`, hash).
- **"O que exibir no portal"** (`:2056-2206`). Sem senha: "Tudo vem ligado. Desligue o que não quiser mostrar neste portal." e
  chaves: **"Aba Histórico"** → "Cards de resumo (totais, ticket médio)", "Gráfico de materiais", **"Valores financeiros (preços e
  totais)"**, "Fotos dos pedidos"; **"Aba Saldo"**; **"Aba Notas Fiscais"**; **"Aba Relatório"** → "Mostrar valores (R$ e preço
  médio)"; "Mostrar aba Preços" (só fornecedor, nasce desligada; **fora da fala**, a fonte não cita); **"Mostrar aba Coletas"** →
  **"Permitir solicitar coleta"** (só com o módulo `coletas`). Com senha: "Escolha seção por seção: Oculto, Livre (abre sem senha)
  ou Com senha. Toda seção nasce Com senha." e cada aba vira as pílulas **"Oculto"** / **"Livre"** / **"Com senha"** (`:157-207`).
- **"Formato do comprovante no portal"** · "Como o comprovante do pedido é gerado quando o cliente clica no portal.": "Automático
  (segue o formato da empresa)", **"A4"**, "Térmico (80mm)" (`:2209-2235`).
- Botão **"Salvar exibição"** (`:2237-2242`) → update de `portal_config` e `portal_receipt_format` no cadastro e **espelho no
  cadastro vinculado do parceiro duplo** (`:1038-1104`); toast **"Exibição do portal salva"**. O "Salvar" do rodapé também grava a
  exibição (`:898-950`).
- Edge `entity-portal` mescla os dois lados do duplo: `false` em qualquer lado esconde nos dois links ("o mais restritivo vence",
  `supabase/functions/_shared/portal-party.ts:128-171`); senha em qualquer lado protege os dois links (`:286-288`).

## 3. Portal do parceiro, página pública `/portal/:token` (`pages/EntityPortal.tsx`; rota `App.tsx:357`, sem login)
- Edge **`entity-portal`** (`?token=&session=`); a página refaz a busca a cada 30 s, ao voltar o foco e no botão (`:453-481`).
- Sem o módulo: **"Portal indisponível"** · "Este portal não está disponível no momento. Fale com a empresa." (`:588-606`;
  `_shared/portal-module-gate.ts`). Link errado: "Link inválido" (`:682-700`). (Nenhum dos dois é gravado.)
- Com senha e sem sessão: **"Acesso restrito"** · "Entre com o usuário e senha para ver seus dados.", "Usuário" ("Seu usuário"),
  "Senha" ("Sua senha"), **"Entrar"** (`:611-666`); erro "Usuário ou senha inválidos" (`:431`). Edge `portal-login` → sessão de
  30 dias no `localStorage` (`portal_session_<token>`; `_shared/portal-session.ts:32`). Seção travada com outra livre: "Acesso
  com senha" · "Para ver <aba>, entre com o usuário e senha. O resto do portal continua aberto." (`:1089-1136`).
- Cabeçalho verde (sem White Label): logo, nome da empresa, **"Portal do Cliente"** (nome fixo do produto, também no fornecedor),
  CNPJ, telefone, e-mail, endereço (`:957-998`). Cartão do parceiro: nome, "Fornecedor"/"Cliente" ou "Cliente + Fornecedor",
  ícone **"Atualizar dados"**, ícone **"Sair"** (só com sessão) (`:1002-1051`).
- Abas (barra lateral no computador): **"Histórico"**, **"Saldo"**, **"Notas Fiscais"**, **"Relatório"**, **"Coletas"** (módulo
  `coletas` + chave), "Preços" (só se ligada; fora da aula) (`:1071-1082`). Rodapé: "Atualizado em <data> às <hora> · <empresa>",
  logo e "ecosistematecnologia.com.br" (`:1958-1981`).
- **Histórico** (`:1142-1625`): cartões **"Total Comprado"** (ou "Total Vendido"), **"Total de Pedidos"**, **"Ticket Médio"**
  (os de dinheiro só com "Valores financeiros"); gráfico **"Top 5 Materiais Mais Comprados"** / "Mais Vendidos" por quilo, legenda
  "<material>: <n>%" (`:874-876`, `:1221-1269`); **"Histórico de Pedidos"**: "Nº Pedido", "Tipo" ("Compra"/"Venda"), "Valor",
  "Pagamento", "Data", "Ações" (impressora **"Gerar comprovante"**); clique na linha abre "Material", "Peso", "Valor Unit.",
  "Total", "Total do Pedido:" e **"Fotos do pedido"** (miniaturas; clique abre em tela cheia) (`:1471-1619`).
  Pedido com "Comprovante sem valores" (ou "Valores financeiros" desligado): a edge zera os valores e a tela põe **"R$ 0,00"** com
  um cadeado ("Valores deste comprovante estão ocultos", `:151-160`; edge `:548-586`).
- **Saldo** (`:1630-1805`): **"Saldo Atual"** no olhar do parceiro (`utils/portalBalancePerspective.ts`): verde **"Você tem a
  receber"**, vermelho "Você tem a pagar", cinza **"Em dia"**; frase "<empresa> deve <valor> para <parceiro>" / "<parceiro> deve…"
  / **"Não há valores em aberto entre <parceiro> e <empresa>"**; **"Histórico de Movimentações"**, selo **"Últimos 90 dias"**:
  "Data", "Tipo" ("Pedido"/"Pagamento"/"Ajuste"), "Descrição", "Forma Pgto.", "Saída", "Entrada", "Saldo". Mesma linha de
  `balances` da ficha (edge `:210-282`).
- **Notas Fiscais** (`:1810-1907`): "Notas Fiscais" · "Todas as NF-e relacionadas a você (entrada e saída) em ordem do mais
  recente."; "Tipo" ("Saída"/"Entrada"), "Nº", "Série", "Data", "Valor", "Status" ("Autorizada"/"Cancelada"); vazio: "Nenhuma nota
  fiscal encontrada.". **Sem botão de download** (nem XML nem DANFE). Só `invoices` emitidas ou canceladas (edge `:284-330`).
- **Relatório** (`components/portal/PortalReportTab.tsx`): **"Período"** (padrão "Últimos 30 dias"; opções "Todos os tempos",
  "Hoje", "Últimos 7 dias", "Este mês", **"Mês passado"**, "Últimos 30 dias", "Este ano", "Personalizado") (`:63`, `:211-224`),
  "Material" (`:228`), **"Baixar PDF"** (abre o relatório numa janela com "Salvar PDF") (`:247`), **"Relatório por Material"**:
  "Código", "Material", "Qtd. Comprada", "Valor Compra", "Preço Médio Compra" (venda: "Qtd. Vendida"...), linha "Total"
  (`:254-420`). Edge `entity-portal-report` (compras `completed` do período; "Mostrar valores" desligado zera os R$).
- **Coletas** (`components/portal/PortalCollectionsTab.tsx`): "Coletas" · "Acompanhe suas coletas e solicite uma nova." (`:79`),
  **"Solicitar coleta"** (`:85`, com "Permitir solicitar coleta"), **"Minhas coletas"** (`:93`), vazio "Nenhuma coleta ainda.
  Clique em “Solicitar coleta” para pedir a primeira."; cartão "#<n>", selo **"Solicitada"**/"Agendada"/"A caminho"/"Concluída"/
  "Cancelada", material, data · período, **"Solicitada em <data>"**, observações.
- Janela **"Solicitar coleta"** (`components/portal/PortalRequestCollectionDialog.tsx:178-279`): "Peça a coleta do seu material. A
  empresa confirma o dia e o horário."; "Tipo" "Coletar material"; **"Material *"** ("ex: Sucata de ferro"); **"Quantidade
  estimada"** ("ex: 500 kg"); **"Data preferida"** (não aceita dia passado); **"Período"** ("Manhã", "Tarde", "Dia todo");
  **"Endereço da coleta"** (vem do cadastro, editável); **"Observações"**; "Cancelar", **"Solicitar coleta"**. Toasts: **"Solicitação
  enviada (#<n>)"**, "Informe o material a coletar". Edge **`collection-request`**: grava `collection_orders` com `origem` "portal",
  `status` "solicitada" (padrão "exige aprovação", `lib/coletas/collectionSettings.ts:29-41`) ou "agendada", motorista e veículo
  vazios; avisa os usuários da empresa em `user_notifications`: **"Nova solicitação de coleta"** · "<parceiro> solicitou uma coleta
  (#<n>)." (`supabase/functions/collection-request/index.ts:205-295`).
- Comprovante pelo portal (`:259-414`): a impressora abre "Gerando comprovante" numa janela e depois o PDF (A4 ou térmico, pelo
  "Formato do comprovante no portal"); janela bloqueada: toast "Seu navegador bloqueou a janela, abrindo o comprovante aqui mesmo"
  e o comprovante por cima do portal. Edge **`portal-order-receipt`**: com foto no pedido, o comprovante leva o QR **"Escaneie para
  ver fotos"** para o link `/fotos/...` (`supabase/functions/portal-order-receipt/index.ts:429-474`).

## 4. Fotos do pedido, página pública `/fotos/:token` (`pages/OrderPhotosPublic.tsx`; rota `App.tsx:371`)
- Edge **`order-photos-public`** (token de `order_photo_shares`; não pede a senha do portal; respeita o "sem valor").
- Cabeçalho verde: logo, nome da empresa, **"Fotos do pedido #<n>"** (`:214`); **"Fotos"** (carrossel; clique abre em tela cheia;
  sem foto: "Nenhuma foto neste pedido.") (`:223-237`); **"Dados do Pedido"**: "Fornecedor"/"Cliente", "Data", "Itens" (material,
  quilos × preço, total), "Total", "Pago", "Forma de pagamento", "Motorista", "Placa", "Observações" (`:239-247`, `:400-515`).
- Link `/fotos/<empresa>-compra-<nº>-<código>` (`utils/publicLinkSlug.ts`, `buildOrderPhotosPath`). No comprovante feito **no
  sistema**, o QR leva ao portal ("Ver no portal") quando o parceiro tem link de portal, e às fotos só quando não tem
  (`utils/buildReceiptParams.ts:113-151`).
- As fotos entram no pedido em "Opções avançadas" › "Fotos do pedido" › "Anexar" (módulo Portal do Cliente;
  `components/AdvancedOptionsPopover.tsx:189-197`, `components/orders/OrderPhotoAttachSection.tsx`).

## 5. No sistema, durante a aula
- Pagamento (cap06): ficha › "Conta-corrente" › "Movimentação" › "Nova Movimentação de Saldo" ("Pagar", "Valor *", "Forma de
  Pagamento" "Pix/Transferência", "Conta bancária", "Observação", "Confirmar"; toast "Movimentação registrada com sucesso!"), como
  no `T04/inventario.md` (seção 5). RPCs `create_manual_bank_transaction`, `update_balance`; `INSERT balance_movements`.
- Sino (cap08): `components/notifications/NotificationsBell.tsx:218` ("Notificações"; com aviso: "1 notificações não lidas");
  `user_notifications` lida ao montar (`hooks/useUserNotifications.ts:36-39`), novidades por realtime.

## 6. Código × fonte (para o relatório)
1. **Relatório ignora o "sem valor" do pedido**: a edge `entity-portal-report` soma o `total_price` de todo pedido do período; só a
   chave "Mostrar valores (R$ e preço médio)" esconde os R$ ali. A fonte diz que o pedido sem valor "sai sem os números também no
   portal" (vale para Histórico, comprovante e fotos). A fala só afirma o que vale.
2. **Saldo do portal × tela de Saldo**: é a mesma linha de `balances`, mas a edge desconta do saldo os movimentos de pedido sem
   valor dos últimos 90 dias (`entity-portal/index.ts:576-586`). Com pedido "sem valor" lançado no saldo, os dois números diferem.
   Na aula não há esse caso (a venda sem valor é no Pix).
3. **Aba "Preços"** do fornecedor existe (nasce desligada) e a fonte não cita: fora da fala.
4. **QR do comprovante do sistema** vai para o portal quando o parceiro tem link (todos têm no mundo); o link de fotos aparece no
   comprovante tirado **do portal**.
5. O cabeçalho do portal diz "Portal do Cliente" também para fornecedor (nome do produto).
