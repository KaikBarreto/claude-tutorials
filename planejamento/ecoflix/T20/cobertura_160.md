# T20 · Portal do Cliente e Fornecedor · cobertura contra o 1.60.10

Auditoria de 18/11/2026, só leitura de código (`/dev/shm/ecoflix-src` e `git diff f37573ea0 5290be4cd`). Caminhos
relativos a `src/`, menos `supabase/...`. Rótulo entre aspas = texto exato do código. Sem varredura do robô para a T20
(`rec/varredura/` só tem t00 a t05). O pedido de coleta pelo portal fica **nesta** aula (a T12 só cita).

## 1. Mudou no app (1.59.154 → 1.60.10)

`git diff` sai **vazio** para `pages/EntityPortal.tsx`, `components/portal/`, `pages/OrderPhotosPublic.tsx`,
`utils/publicLinkSlug.ts`, `utils/portalBalancePerspective.ts`, `lib/whatsappOrder.ts`, `AdvancedOptionsPopover.tsx`,
`orders/OrderPhotoAttachSection.tsx`, as edges `entity-portal-report`, `collection-request`, `portal-login`,
`portal-set-credentials` e `_shared/portal-*`. Na aba "Portal" de `EntityFormDialog.tsx` nenhuma linha mudou (as 570
linhas do diff são da aba fiscal: consulta de IE e painel de pendências). **Nenhum rótulo, botão ou aviso do roteiro
mudou de texto.** O que mudou:

| # | Cap. | O que mudou | Arquivo:linha |
|---|---|---|---|
| M1 | cap09 | O comprovante tirado **do portal** passou a obedecer "quem assina" (duas linhas, só a do cliente/fornecedor ou só a do operador). Antes saíam sempre as duas. A edge agora devolve `company.receipt_signature_mode` (`both`, `counterparty`, `operator`). Só muda o quadro do A4 se o mundo tiver assinatura no comprovante ligada; a fala não muda. Nota 1.59.155: "Vale no comprovante, no ticket e no Portal do Cliente." | `supabase/functions/portal-order-receipt/index.ts:41-42,197,526`; `config/version.ts:108` |
| M2 | cap05, cap09, cap10 | "Fotos do pedido", o QR "Escaneie para ver fotos" e a página `/fotos/...` passaram a contar **só imagem** (`mime` vazio ou `image/%`). O pedido agora pode ter PDF anexado (a galeria do sistema mostra "Abrir PDF ..."), e o PDF não vai para o portal nem para a contagem do QR. Fala igual; o backend falso precisa aceitar o filtro `.or('mime.is.null,mime.like.image/%')` em `order_attachments` e as três fotos da semente têm de ter `mime` de imagem. | `supabase/functions/entity-portal/index.ts:430`; `order-photos-public/index.ts:120`; `portal-order-receipt/index.ts:451`; `utils/buildReceiptParams.ts:129`; `components/orders/OrderAttachmentsGallery.tsx` |

Em volta das telas (não muda fala, pode mudar quadro):

| Onde | O que mudou | Arquivo |
|---|---|---|
| cap03 (ilustração do parceiro duplo) e qualquer quadro com o Depósito Irmãos Siqueira no sistema | No parceiro que é cliente e fornecedor, o saldo da lista, da ficha e do "Editar" passou a usar a leitura de cliente nos dois cadastros (cor, sinal e "a receber"/"a pagar"). A Cooperativa não é dupla: o "R$ 1.350,00" vermelho do cap06 continua igual. | `utils/dualBalancePerspective.ts:6-10`; `clients-suppliers/ClientsListView.tsx:205-206,511,687`; `pages/PartnerDetail.tsx:173`; `hooks/usePartnerActions.tsx:320-328,497` |
| cap02 a cap04 ("Editar Fornecedor") | Acima das abas pode aparecer o painel âmbar "Falta isto para emitir NF-e" · "Dá para salvar o cadastro assim, mas a nota não sai até preencher.". Só aparece depois de uma consulta de CNPJ ou CEP **naquela abertura** da janela; o robô vai direto à aba "Portal", então não aparece. Não digitar em CEP nem CNPJ nesses capítulos. | `components/entity-form/PendenciasNfePanel.tsx:43-48`; `entity-form/pendenciasNfe.ts:65-66`; `EntityFormDialog.tsx:1557` |
| Telas logadas (cap00, 02, 03, 04, 06, 08) | Botão flutuante do Cato (se o mundo ligar) e o filho "Relatórios Fiscais" no menu "Fiscal & Ambiental" (só com o grupo aberto). | `components/layout/AppLayout.tsx:35,267`; `config/routes.ts:511` |

## 2. Falta cobrir (está no 1.60.10 e o roteiro não mostra)

### Aba "Portal" do cadastro · `components/EntityFormDialog.tsx`
| # | O que é | Quando o cliente usa | Vale? |
|---|---|---|---|
| L1 | **Aba Preços do fornecedor.** Sem senha: "Mostrar aba Preços" · "O fornecedor passa a ver quanto a empresa paga por cada material, já com o preço dele aplicado. Nasce desligado." Com senha: "Aba Preços" · "Quanto a empresa paga por cada material, já com o preço deste fornecedor. Nasce oculta." Só no cadastro de fornecedor (`:2689-2708`). No portal vira a aba "Preços" (L11). | Fornecedor que liga perguntando o preço do dia | **Sim, capítulo C.** O roteiro deixou de fora de propósito ("a fonte não cita"); com o pedido de cobrir cada função, entra |
| L2 | **Senha por parte, de verdade.** Com o login ligado e uma aba em "Livre", o link abre sem pedir nada, as abas travadas ganham um cadeado no ícone e o conteúdo vira o cartão "Acesso com senha" · "Para ver <aba>, entre com o usuário e senha. O resto do portal continua aberto." (`pages/EntityPortal.tsx:752-782,1089-1136`). Dicas das pílulas: "Não aparece no portal", "Aparece sem pedir senha", "Só depois do login" (`:194-196`); cada linha tem descrição ("Pedidos, pesos e comprovantes.", "Saldo, extrato e moeda.", "Notas emitidas e canceladas.", "Totais por material no período.", "Histórico de coletas e o pedido de nova coleta.", `:2606-2715`) | Deixar o histórico aberto e proteger o saldo | **Sim, capítulo A** (hoje é só ilustração no cap04) |
| L3 | **Trocar a senha e tirar o login.** Com usuário já salvo, o campo "Senha" mostra "deixe em branco p/ manter"; chave desligada muda o botão para "Remover login" → "Login removido" (`:2570,2579`, `:1370`). A tela "Acesso restrito" não tem "esqueci a senha" (`EntityPortal.tsx:611-666`) | Parceiro esqueceu a senha; trocou o contato | **Sim, trecho** no cap04 |
| L4 | Parceiro duplo: aviso "Este parceiro é cliente e fornecedor: o acesso vale pros dois links." (`:2545-2549`) | Senha no parceiro duplo | **Sim**, mostrado de verdade no capítulo A (hoje é falado no cap04) |
| L5 | Cadastro sem link: "Este cadastro ainda não tem link de portal." + "Gerar link" → "Link do portal gerado" (`:2493-2504,1327-1337`); na ficha: "Portal ainda não configurado para este cadastro." (`ClientsListView.tsx:411`). No cadastro novo: "Salve o cadastro para ativar o link." e "A senha do portal pode ser configurada depois de salvar o cadastro." (`:2487-2513`) | Cadastro antigo, de antes do módulo | **Só citar** (cap02) |
| L6 | Ícone "Abrir portal" (aba nova) (`:2473-2483`): o roteiro mostra e não usa | Conferir o que o parceiro vai ver | **Só citar** (cap02) e usar no trecho do cap03 |
| L7 | Formato "Térmico (80mm)" e "Automático (segue o formato da empresa)" (`:2751-2762`) | Parceiro que imprime em bobina | **Só citar** (cap03) |
| L8 | Efeito de cada chave: sem "Valores financeiros" somem "Total Comprado" e "Ticket Médio" e os pedidos saem "R$ 0,00" com cadeado; sem "Cards de resumo" somem os três cartões; sem "Fotos dos pedidos" somem as miniaturas; sem "Permitir solicitar coleta" o botão some e a lista fica (`EntityPortal.tsx:1146-1216`; `portal/PortalCollectionsTab.tsx:71,83`). Tudo desligado: "Nada para exibir" · "Este portal está sem seções ativas no momento. Fale com a empresa." (`EntityPortal.tsx:1064-1067`) | Esconder preço de um parceiro só | **Sim, trecho** "desliga e confere" no cap03 (hoje o mouse só passa) |
| L9 | O "Salvar" do rodapé também grava a exibição (nota em `version.ts:1040`) | Quem não clica em "Salvar exibição" | **Só citar** (cap03) |
| L10 | Página cheia do parceiro: botão "Copiar link do portal" (`pages/PartnerDetail.tsx:315-324,367-372`) | Quem abre o parceiro em página cheia | **Só citar** (cap02) |

### Portal do parceiro · `pages/EntityPortal.tsx`, `components/portal/`
| # | O que é | Quando | Vale? |
|---|---|---|---|
| L11 | **Aba "Preços"**: "Preços atualizados em <data>", "Valores sujeitos a alteração. Vale o preço do momento da pesagem.", blocos "Seus materiais" e "Outros materiais que compramos", "Baixar em PDF" ("Gerando tabela de preços"), "Buscar material" (só com mais de 20 itens), vazio "Nenhum preço disponível" (`portal/PortalPricesTab.tsx:54,229-289`). O preço já vem resolvido para aquele fornecedor (preço próprio, tabela ligada ou padrão), sem marca de preço especial (`supabase/migrations/20260909020000_portal_price_list_rpc.sql`) | Fornecedor consulta o preço | **Sim, capítulo C** |
| L12 | **Parceiro duplo no portal**: selo "Cliente + Fornecedor" (`:1014-1017`); quatro cartões "Total Comprado", "Total Vendido", "Total de Pedidos", "Ticket Médio" (`:1147-1216`); gráfico "Top 5 Materiais" (`:874-876`); filtro "Todos"/"Compras"/"Vendas" com a contagem (`:1280-1306`); vazios "Nenhuma compra no período"/"Nenhuma venda no período"; Relatório com "Qtd. Comprada" e "Qtd. Vendida" lado a lado (`PortalReportTab.tsx`) | Depósito que compra e vende | **Sim, capítulo B** (hoje só ilustração no cap03) |
| L13 | Link que abre **num pedido**: `?pedido=<id>` abre o Histórico, expande o pedido e contorna a linha por uns 6 s (`:234-246,512-544`). É o link do "Enviar pelo WhatsApp" (L20) e do QR "Ver no portal" do comprovante do sistema | Mandar um pedido específico | **Sim, capítulo D** |
| L14 | Cartão do parceiro: etiquetas e campos personalizados liberados ("Mostrar esta etiqueta nos portais", "Mostrar no portal" em Clientes e Fornecedores › Configurações) (`:1011-1013,1039-1048`; `clients-suppliers/ClientsSuppliersSettingsDialog.tsx:86,139`) | Mostrar ao parceiro a categoria dele | **Só citar** (cap01). Criar etiqueta e campo é da **T4** (N6 da auditoria dela) |
| L15 | Linha de pesagem embaixo do material ("Bruto ... · Tara ...", "Impureza ...") (`:101-117,1567-1575`) | Pedido com tara ou desconto | **Só citar** (cap05) |
| L16 | Saldo quando o **parceiro deve**: valor com traço em vermelho, selo "Você tem a pagar", frase "<parceiro> deve <valor> para <empresa>" (`utils/portalBalancePerspective.ts:37-63,111`) | Fornecedor com vale; cliente comprando a prazo | **Sim, trecho** no cap06 |
| L17 | Extrato: tipo "Ajuste" (crédito ou débito lançado à mão, com o motivo), "Ver todas as N movimentações" acima de 20 linhas, cadeado no movimento de pedido sem valor, vazio "Nenhuma movimentação encontrada" (`:921-928,1791-1798,1715`) | Ler o extrato | **Só citar** (cap06) |
| L18 | Notas: selo "Entrada" (nota de entrada da compra), status "Cancelada"; só nota `emitida` ou `cancelada` chega ao portal, até 200 (`:1876-1896`; `supabase/functions/entity-portal/index.ts:300,313`) | Fornecedor confere a nota de entrada; nota cancelada | **Sim, trecho** no cap07 (parte fiscal: hoje só mostra uma saída autorizada) |
| L19 | Relatório: filtro "Material" (vários), período "Personalizado" e os outros, vazio "Nenhum material no período selecionado" · "Ajuste o período ou o filtro de material." (`PortalReportTab.tsx:213-235,291-292`) | Quanto entreguei de papelão no trimestre | **Sim, trecho** no cap07 |
| L20 | Coletas: cartão "Concluída" clicável, "Ver relatório da coleta" → `/portal/<link>/coleta/<id>` com "Voltar ao portal"; cancelada mostra "Motivo: ..."; selo "A caminho" (`PortalCollectionsTab.tsx:108-166`; `App.tsx:362`; `pages/CollectionReportPublic.tsx:184`) | Parceiro acompanha a coleta | **Sim, trecho** no cap08 (a T12 mostra o relatório pelo lado da empresa) |
| L21 | Regras do pedido: "A data escolhida já passou. Escolha hoje ou uma data futura.", "A coleta precisa ser pedida com no mínimo Nh de antecedência.", "A empresa não aceita coleta no dia escolhido. Escolha outro dia." (`lib/coletas/collectionSettings.ts:93-113`); "Período" só com os períodos que a empresa usa (`PortalRequestCollectionDialog.tsx:107`); endereço editável; sem "Exigir aprovação da solicitação" o pedido "já entra agendada" (`coletas/CollectionSettingsTab.tsx:193-196`) | Parceiro pede fora da regra | **Só citar** (cap08, sem erro encenado). A configuração é da **T12** (cap11) |
| L22 | Comprovante: no celular o pedido aberto tem o botão "Comprovante"; janela bloqueada: "Seu navegador bloqueou a janela, abrindo o comprovante aqui mesmo" (`:272,1448-1461`); assinatura conforme M1 | Parceiro no celular, pelo WhatsApp | **Só citar** (cap09) |
| L23 | Telas de aviso: "Link inválido" · "Este link de portal não é válido ou expirou. Solicite um novo link ao seu parceiro comercial." (`:691-694`); "Nada para exibir" (L8) | Link colado pela metade | **Só citar** (cap01, junto do "Portal indisponível") |
| L24 | No celular as abas viram uma lista suspensa (`SettingsSidebarLayout`, comentário em `:1053-1056`) | Quase todo parceiro abre no celular | **Só citar** (cap01) |
| L25 | White Label (cor da empresa no cabeçalho, sem o rodapé do EcoSistema), várias moedas por cartão, nomes de cliente/fornecedor invertidos | Empresas com esses módulos | **Não**: fora do mundo da trilha (real, sem White Label) |

### No sistema, ligado ao portal
| # | O que é | Quando | Vale? |
|---|---|---|---|
| L26 | **"Enviar pelo WhatsApp"** no menu "⋮" do pedido (tela de pedidos e histórico da ficha): abre o WhatsApp no telefone do cadastro com "Olá, <parceiro>!" / "Aqui é da <empresa>." / "Segue o comprovante do Pedido <nº>, de <data>." / "Valor total, R$ ...." (ou "Cupom sem valor.") / "Acesse pelo link abaixo:" + link do portal já no pedido. Avisos: "<Fornecedor> sem telefone cadastrado", "Este cadastro ainda não tem link de portal" (`lib/whatsappOrder.ts:109-131,194,239-244`; `pages/Orders.tsx:2684-2697`; `components/TransactionHistory.tsx:4346-4356`) | Mandar o pedido ao parceiro na hora | **Sim, capítulo D.** A auditoria da T9 (L11) deixou para esta aula |
| L27 | **Anexar as fotos, de verdade**: "Opções avançadas" › "Fotos do pedido" › "Anexar" (várias de uma vez, só imagem), miniatura com "Remover foto", sem internet "Disponível com internet."; também no Ticket de Pesagem (`orders/OrderPhotoAttachSection.tsx:83,118-162`; `weighing/WeighingTicketForm.tsx:2061`). Depois: "⋮" › "Ver fotos anexadas" (`Orders.tsx:2677-2683`) | Foto da carga no pedido | **Sim, trecho** no cap10 (hoje é ilustração). T7 e T8 só citam e apontam para cá |
| L28 | Página de fotos: linhas "Pago", "Motorista", "Placa", "Observações"; "Link inválido ou expirado." (`pages/OrderPhotosPublic.tsx:168,469-511`) | Pedido com motorista | **Só citar** (cap10) |
| L29 | Sem o módulo: aba "Portal" mostra só a contratação; "Anexar" e "Enviar pelo WhatsApp" abrem a contratação ("Envio pelo WhatsApp precisa do módulo Portal do Cliente") | Empresa sem o módulo | **Não**: já coberto por "depende do plano contratado" (sem preço) |
| L30 | Quem assina o comprovante (Configurações → Usabilidade) | M1 | **Não aqui**: aula de Configurações; uma frase no cap09 |

## 3. Proposta

Quatro capítulos novos (A a D) e trechos nos existentes. Numeração sugerida para não renumerar sementes: cap04b (A),
cap04c (B), cap07b (C), cap09b (D). Os capítulos A e B usam o **Depósito Irmãos Siqueira** para não mexer na
Cooperativa (que segue toda "Com senha" do cap04 ao fim) nem na Fundição (sem senha).

### Trechos em capítulos existentes

| Cap. | Tela | Fala |
|---|---|---|
| cap01 | Depois das abas: o mouse no cartão do parceiro (se o mundo tiver etiqueta liberada, ela aparece ao lado do nome). | Se você usa etiquetas ou campos personalizados no cadastro, só aparece aqui o que você liberou pro portal, nas Configurações de Clientes e Fornecedores. |
| cap01 | [ILUSTRAÇÃO: o mesmo portal num celular genérico, com as abas numa lista em cima] | No celular, que é onde quase todo parceiro abre o link, as abas viram uma lista no alto da página. |
| cap01 (dica) | Plano geral, sem tela de erro. | E se aparecer Link inválido, o endereço chegou errado ou pela metade. É só copiar de novo na ficha e mandar outra vez. |
| cap02 | Na aba "Portal": o mouse no ícone "Abrir portal". | Este ícone abre o portal numa aba nova, pra você conferir do jeito que o parceiro vai ver. |
| cap02 | (falado sobre a aba "Portal"; cena opcional com um cadastro sem link: "Este cadastro ainda não tem link de portal." e "Gerar link") | Em cadastro antigo, pode aparecer o aviso de que ainda não tem link. Aí é só clicar em Gerar link. E na página do parceiro, o botão Copiar link do portal faz a mesma coisa. |
| cap03 | Depois do "A4": o mouse em "Térmico (80mm)" e "Automático (segue o formato da empresa)". | Se o parceiro imprime em bobina, é o Térmico. No Automático, vale o formato da sua empresa. |
| cap03 | Novo, antes da dica do parceiro duplo: "Editar Cliente" da Aços Quiririm Ltda › "Portal"; desliga "Valores financeiros (preços e totais)" e "Aba Saldo"; "Salvar exibição" ("Exibição do portal salva"); clique em "Abrir portal" (corte): só o cartão "Total de Pedidos", a lista com "R$ 0,00" e o cadeado, sem a aba "Saldo". | Vamos ver na prática. Na Aços Quiririm, eu desligo os Valores financeiros e a aba Saldo, e salvo. No portal dela, sobra o total de pedidos, os valores aparecem zerados com um cadeado, e a aba Saldo sumiu. |
| cap03 | O mouse em "Permitir solicitar coleta" e no "Salvar" do rodapé. | Com o Permitir solicitar coleta desligado, o parceiro acompanha as coletas, mas não pede uma nova. E o Salvar de baixo também grava essas escolhas. |
| cap04 (fim) | Reabre a aba "Portal" da Cooperativa: "Senha" com "deixe em branco p/ manter"; o mouse na chave "Pedir login no portal" (não desliga). | Se a cooperativa esquecer a senha, não tem recuperação pelo portal: você digita uma nova aqui e salva. Deixando em branco, a senha continua a mesma. E pra tirar o login, é desligar a chave e clicar em Remover login. |
| cap05 | Num pedido com tara (a latinha do ticket da T8, se a semente tiver tara): a linha "Bruto ... · Tara ..." embaixo do material. | Quando o pedido tem tara ou desconto, aparecem embaixo do material o peso bruto e a tara, igual ao comprovante. |
| cap06 | Depois da dica: portal do Valdir Pereira (sem senha) › "Saldo": "-R$ 300,00" em vermelho, selo "Você tem a pagar", "Valdir Pereira deve R$ 300,00 para Recicla Vale Metais". [ZOOM: valor, selo e frase] | E quando é o parceiro que deve? O Valdir pegou um vale de trezentos reais. No portal dele, o saldo aparece em vermelho, com Você tem a pagar, e a frase diz quem deve pra quem. |
| cap06 | No extrato do Valdir: a linha "Ajuste" (se a semente tiver) e o rodapé da lista. | No extrato, além de Pedido e Pagamento, aparece Ajuste, quando você lança um crédito ou um débito na conta do parceiro, com o motivo que você escreveu. E passando de vinte linhas, tem o Ver todas as movimentações. |
| cap07 | Portal da Cooperativa › "Notas Fiscais": uma linha "Entrada" (azul) "Autorizada"; no portal da Fundição, uma linha com "Cancelada". | No fornecedor, aparecem as notas de entrada que a Recicla Vale emitiu nas compras dele, com o selo Entrada. Só chegam aqui as notas autorizadas e as canceladas, que ficam marcadas. Nota rejeitada ou ainda em digitação não aparece. |
| cap07 | No Relatório: "Material" → marca "Papelão" (tabela com uma linha) → limpa; "Período" → "Personalizado", de 01/10/2026 a 31/10/2026. | Dá pra filtrar por material, e escolher um período do seu jeito, em Personalizado. |
| cap08 | Na janela "Solicitar coleta": o mouse em "Endereço da coleta" e em "Período". | Se a coleta for em outro lugar, ela troca o endereço ali mesmo. |
| cap08 | Em "Minhas coletas": clique no cartão "#5" "Concluída", em "Ver relatório da coleta": abre o relatório; "Voltar ao portal". Se a semente tiver uma cancelada: a linha "Motivo: ...". | Depois que a coleta é concluída, o cartão vira um atalho: Ver relatório da coleta, com o que foi recolhido e entregue. E se você recusar ou cancelar um pedido, ela vê o motivo aqui. |
| cap08 (depois da ilustração) | (sem tela de erro) | Se ela escolher um dia que a Recicla Vale não atende, ou pedir em cima da hora, o portal explica o motivo e pede outra data. E se você tirar a exigência de aprovação, o pedido já entra como Agendada. Essas regras ficam nas Configurações de Coletas. |
| cap09 | [ZOOM: rodapé do A4, só se o mundo tiver assinatura ligada] | Se a sua empresa imprime linha de assinatura no comprovante, ela sai aqui também, do jeito que você escolheu nas Configurações, em Usabilidade. No celular, se o navegador bloquear a janela, o comprovante abre por cima do portal, com um X pra voltar. |
| cap10 (troca a 1ª ilustração) | Sistema: "Nova Compra" da Cooperativa com um item (T7) › "Opções avançadas" › "Fotos do pedido" › "Anexar": três fotos; miniaturas com o X "Remover foto". [TESTAR: seletor de arquivo do robô] Depois, tela de pedidos › "⋮" › "Ver fotos anexadas". | Agora, as fotos. Elas entram na compra ou na venda, em Opções avançadas, no Anexar. Dá pra escolher várias de uma vez, e tirar uma foto errada no X antes de salvar. Precisa estar com internet, e vale também no Ticket de Pesagem. Depois, nos Pedidos, o Ver fotos anexadas mostra as fotos daquela linha. |
| cap10 | Em "Dados do Pedido": "Motorista", "Placa", "Observações" (se o pedido tiver). | Se o pedido tiver motorista, placa ou observação, aparecem aqui também. |
| cap11 | Montagem: cadeado nas abas, selo "Cliente + Fornecedor", aba "Preços", a mensagem do WhatsApp. | A gente também deixou o histórico livre e o resto com senha, viu o portal de quem é cliente e fornecedor, liberou a tabela de preços pra cooperativa e mandou um pedido pelo WhatsApp. |

### Capítulo A (novo, depois do cap04) · Senha só no que é sensível (vinheta: SENHA)

| Tela | Fala |
|---|---|
| Sistema: "Editar Fornecedor" do Depósito Irmãos Siqueira › "Portal"; liga "Pedir login no portal"; aparece "Este parceiro é cliente e fornecedor: o acesso vale pros dois links."; "Usuário" "deposito.siqueira", "Senha"; "Salvar acesso" ("Acesso salvo"). | Nem tudo precisa de senha. No Depósito Irmãos Siqueira, eu ligo o login e salvo o acesso. Repara no aviso: como ele é cliente e fornecedor, o acesso vale pros dois links. |
| Em "O que exibir no portal": "Aba Histórico" → "Livre"; as outras ficam "Com senha"; "Salvar exibição". | Agora, no Histórico, eu marco Livre. Saldo, Notas e Relatório continuam Com senha. Salvar exibição. |
| Navegador do parceiro, sem nada salvo: o link do Depósito abre direto no "Histórico"; nas abas "Saldo", "Notas Fiscais", "Relatório" e "Coletas", um cadeado pequeno no ícone. [ZOOM: as abas com cadeado] | Quando o Depósito abre o link, o Histórico aparece direto, sem pedir nada. E as outras abas ganham um cadeado. |
| Clique em "Saldo": cartão "Acesso com senha" · "Para ver Saldo, entre com o usuário e senha. O resto do portal continua aberto.", "Usuário", "Senha", "Entrar" (não entra). | Clicando em Saldo, o portal pede o usuário e a senha só pra essa parte. O resto continua aberto. |
| Volta ao "Histórico". | Uma dica: o que está com senha nem chega no navegador de quem abriu o link sem entrar. E o comprovante, o relatório e o pedido de coleta seguem a mesma trava. |

Mundo: `portal-set-credentials` para o par do Depósito; `entity-portal` do Depósito sem sessão devolvendo
`requires_login: true`, `locked_sections` (`historico: false`, resto `true`), só o bloco do Histórico, `has_coletas`
true; vira `apos-cap04b`.

### Capítulo B (novo, depois do A) · Cliente e fornecedor no mesmo portal (vinheta: PORTAL)

| Tela | Fala |
|---|---|
| Portal do Depósito (como ficou no A): cartão do parceiro com o selo "Cliente + Fornecedor". | Repara no selo: cliente e fornecedor. É um link só pros dois lados. |
| Os quatro cartões "Total Comprado", "Total Vendido", "Total de Pedidos", "Ticket Médio"; o gráfico "Top 5 Materiais". | Em cima, o que a Recicla Vale comprou dele e o que vendeu pra ele, cada um no seu cartão. |
| Em "Histórico de Pedidos": "Todos", "Compras", "Vendas" com a contagem; clique em "Vendas": só linhas "Venda", três cartões com "Total Vendido", gráfico "Top 5 Materiais Mais Vendidos"; volta a "Todos". | Na lista, ele filtra: Todos, Compras ou Vendas. Clicando em Vendas, os cartões e o gráfico acompanham. |
| O mouse na aba "Saldo" (com cadeado), sem clicar. | E o saldo é um só, já com as compras e as vendas na mesma conta. |

Mundo: `entity-portal` do Depósito com `is_dual: true`, `sides` com os dois lados e pelo menos duas compras e duas
vendas no feed (o bronze a R$ 30,50 da T3 serve de compra). Com este capítulo, a ilustração do parceiro duplo no cap03
pode encurtar para a regra "vale o que esconde mais".

### Capítulo C (novo, depois do cap07) · A tabela de preços do fornecedor (vinheta: PREÇOS)

| Tela | Fala |
|---|---|
| Sistema: "Editar Fornecedor" da Cooperativa › "Portal"; em "O que exibir no portal", a linha "Aba Preços" · "Quanto a empresa paga por cada material, já com o preço deste fornecedor. Nasce oculta.", em "Oculto". [ZOOM: a linha] | Seu fornecedor vive perguntando quanto está o material? Dá pra mostrar a tabela de preços no portal dele. É a única aba que nasce oculta, pra ninguém ver preço sem você decidir. |
| Clique em "Com senha"; "Salvar exibição" ("Exibição do portal salva"). | Na cooperativa, eu mudo de Oculto pra Com senha, e salvo. |
| Portal da Cooperativa (com sessão): a aba nova "Preços"; "Preços atualizados em 10/11/2026"; bloco "Seus materiais" (Papelão, Plástico PET, Alumínio latinha, Chaparia, Ferro misto) e "Outros materiais que compramos". | No portal, apareceu a aba Preços. Primeiro, os materiais que a cooperativa já entrega. Depois, os outros que a Recicla Vale compra. |
| [ZOOM: "Valores sujeitos a alteração. Vale o preço do momento da pesagem."] | E o aviso protege você: os valores podem mudar, e vale o preço do momento da pesagem. |
| [ZOOM: "Baixar em PDF"], sem clicar. | No Baixar em PDF, ela leva a tabela pronta. |
| De volta à lista de preços. | Uma dica: cada fornecedor vê o preço dele. Se a cooperativa tem preço combinado ou uma tabela própria, é esse que aparece, sem nenhuma marca de preço especial. E essa aba só existe no cadastro de fornecedor. |

Mundo: `UPDATE suppliers` com `precos: true`; `entity-portal` da Cooperativa devolvendo `price_list` (campos
`material_id`, `code`, `code_prefix`, `name`, `unit`, `price`, `is_own`, `own_qty`, `last_purchase_at`, na ordem
próprios primeiro) e `price_list_generated_at`; os preços saem da tabela de compra do T3. Vira `apos-cap07b`; os
capítulos seguintes passam a mostrar a aba "Preços" na barra da Cooperativa.

### Capítulo D (novo, depois do cap09) · Mandar o pedido pelo WhatsApp (vinheta: LINK)

| Tela | Fala |
|---|---|
| Sistema: tela de pedidos (a da T9); na compra de 06/11 da Cooperativa, o menu "⋮": "Ver comprovante", "Ver fotos anexadas", "Enviar pelo WhatsApp". | Em vez de esperar o parceiro abrir o portal, você pode mandar o pedido pra ele. Nos Pedidos, no menu da compra, tem o Enviar pelo WhatsApp. |
| Clique (a janela do WhatsApp não é filmada). [ILUSTRAÇÃO: um balão de mensagem genérico com o texto exato: "Olá, Cooperativa Recomeço!" · "Aqui é da Recicla Vale Metais." · "Segue o comprovante do Pedido <nº>, de 06/11/2026." · "Valor total, R$ 3.700,00." · "Acesse pelo link abaixo:" e o link] | O WhatsApp abre com a mensagem pronta, no telefone do cadastro: o número do pedido, a data, o valor e o link. |
| Navegador do parceiro (sessão da Cooperativa): o link com `?pedido=` abre o "Histórico" já no pedido de 06/11, aberto e contornado. [ZOOM: a linha contornada] | E esse link já abre o portal em cima daquele pedido, com os materiais e as fotos. |
| De volta ao menu "⋮". | Uma dica: precisa do telefone no cadastro do parceiro. E num pedido com Comprovante sem valores, a mensagem avisa que o cupom é sem valor, e não mostra o total. O mesmo botão aparece no histórico da ficha do parceiro. |

Mundo: telefone no cadastro da Cooperativa; o robô intercepta `window.open` para `wa.me` (não carregar site externo);
`entity-portal` já devolve o pedido de 06/11 (o `id` da semente vai no `?pedido=`).

### Outras necessidades do mundo
- Aços Quiririm: `entity-portal` com `portal_config` (`valores: false`, `saldo: false`) e pedidos com `hide_financial_details` (a edge zera os valores).
- Valdir Pereira: `entity-portal` com o saldo de R$ 300,00 a favor da empresa e, se possível, um movimento "Ajuste".
- Notas: uma `invoices` de entrada `emitida` da Cooperativa e uma `cancelada` da Fundição (conferir com a linha do tempo fiscal da T16).
- Coletas: `collection-report` aceitando token do portal + id da ordem #5; opcional uma cancelada com `cancel_reason`.
- cap10: três arquivos de imagem para o `setInputFiles` e o `storage` falso do balde `order-attachments`.
- cap09: `portal-order-receipt` com `receipt_signature_mode` (M1) e o filtro de imagem (M2).

## 4. Estimativa

| Bloco | Palavras | Segundos de fala |
|---|---|---|
| Trechos nos capítulos existentes (21) | ~650 | ~250 |
| Capítulo A · Senha só no que é sensível | ~120 | ~46 |
| Capítulo B · Cliente e fornecedor no mesmo portal | ~65 | ~25 |
| Capítulo C · A tabela de preços do fornecedor | ~130 | ~50 |
| Capítulo D · Mandar o pedido pelo WhatsApp | ~105 | ~40 |
| **Total** | **~1.070** | **~410 s** |

Capítulos novos: 4. A aula vai de ~12 min para ~20 min de vídeo. Sementes novas: `apos-cap04b`, `apos-cap07b`.

## Depende de decisão
1. **Aba Preços** entra (capítulo C)? O plano original deixou fora porque a fonte não citava.
2. Capítulos A e B no **Depósito Irmãos Siqueira** (proposto) ou na Cooperativa (muda o estado dos capítulos seguintes).
3. **Notas de entrada e cancelada** no cap07: o mundo precisa dessas duas notas; conferir com a T16 antes de semear.
4. **WhatsApp**: a janela externa não é filmada; a mensagem vira ilustração com o texto exato. Aceita?
5. cap10: gravar o **Anexar** de verdade (depende do seletor de arquivo do robô) ou manter a ilustração.
6. Relatório da coleta pelo portal aparece aqui (cap08) e no capítulo B da T12: manter os dois (lados diferentes) ou só um.
7. O mundo liga o Cato e a assinatura no comprovante? Os dois mudam quadros (M1 e botão flutuante).
