# Cobertura 1.60.10 · T2 Usuários e permissões

Auditoria de 18/11/2026, só leitura de código. Base: `/dev/shm/ecoflix-src` (1.60.10) contra o roteiro (1.59.154).
Caminhos relativos a `src/`, linhas do 1.60.10. `UM` = `pages/UserManagement.tsx`, `PE` =
`components/settings/PermissionsEditor.tsx`, `UMD` = `components/settings/UsersMasterDetail.tsx`, `RT` = `config/routes.ts`.

**Mudaram** entre `f37573ea0` e `5290be4cd`: `UM` (+309 linhas), `PE`, `UMD`, `RT`, `hooks/usePermissions.tsx`,
`supabase/functions/create-company-user/index.ts`. **Sem mudança nenhuma**: `pages/Settings.tsx`,
`SettingsUsersContent.tsx`, `lib/configTabsPermissions.ts`, `UserLimitModal.tsx`, `UserExcessModal.tsx`,
`DeleteUserConfirmDialog.tsx`, `PasswordStrengthIndicator.tsx`, `EmployeeOrdersReportDialog.tsx`,
`hooks/useCompanyModules.tsx`, `manage-company-users`, o menu lateral. Ou seja: caps. 0, 6, 7, 8, 9 e 10 batem com a
tela (só ganham a coluna nova do detalhe, item 1); caps. 1 a 5 precisam de ajuste.

Sobre o pedido: a tela não tem "arquivar/reativar"; o que existe é **"Desativar" / "Ativar"** (cap06, sem mudança).

## 1. Mudou no app (por capítulo)

**Todos os capítulos que abrem o detalhe de um usuário (01, 05, 06, 07)**
1. O detalhe ganhou uma terceira coluna, **"Peso dos pedidos"**, ao lado de "Perfil de acesso" e "Última atividade"
   (a 1280 px ficam três colunas, `UMD:309`). Valores: "Padrão da empresa" + "Acompanha a regra definida em
   Integrações." ou "Balança obrigatória" / "Digitação manual liberada" + "Exceção configurada especificamente para
   este usuário." (`UMD:322-337`). A fala não precisa mudar; a câmera e as medidas do painel mudam.

**cap02 · Criar o usuário**
2. **A fala da foto ficou errada.** A edge agora devolve `userId` (`create-company-user/index.ts:384`), então a foto e a
   tela inicial escolhidas na criação passam a gravar (`UM:415-460`). "A foto, coloca depois de criar, no Editar. É lá
   que ela fica gravada." não vale mais (achado 1 do inventário resolvido). Na criação a foto aparece na hora na
   bolinha (prévia local); o rótulo segue "Foto opcional para o novo usuário" (`UM:1200`).
3. Ao abrir "Criar Novo Usuário", a coluna "Permissões" mostra um aviso âmbar: **"Escolha primeiro o perfil deste
   usuário"** / "O Operador Padrão cobre a rotina diária. Use Personalizado quando quiser montar o acesso tela por
   tela." (`PE:172-181`). Enquanto nenhum perfil é escolhido, a busca e a lista ficam apagadas e sem clique
   (`PE:183`), a seção "Restrições" não aparece (`PE:493`), e "Criar Usuário" devolve o aviso **"Escolha um perfil de
   acesso para o novo usuário"** (`UM:772-776`; no servidor, "Escolha um perfil de acesso antes de criar o usuário.",
   `create-company-user/index.ts:159-167`). A última linha do cap02 passa a câmera por essa coluna: o aviso vai aparecer.
4. Entre "Tela inicial" e os "Perfis rápidos" entrou o campo **"Peso dos pedidos"** (`UM:1312-1333`): opções "Herdar
   padrão da empresa", "Exigir peso da balança", "Permitir digitação manual"; ajuda "A exceção vale para compras e
   vendas deste usuário. Sem exceção, futuras mudanças no padrão da empresa são aplicadas automaticamente." Empurra os
   perfis e a lista para baixo (a janela já tinha duas rolagens). A coluna "Dados do usuário" agora fica fixa enquanto
   a direita rola (`UM:1140`).

**cap03 · Os três perfis rápidos**
5. O chip "Operador Padrão", quando não é o marcado, traz o selo **"Recomendado"** dentro do botão (`PE:149-151`). O
   nome acessível vira "Operador Padrão Recomendado": foi aí que a varredura quebrou (cap03, passo 5).
6. **"Personalizado" deixou de ser selo e virou o quarto botão**, sempre visível, cinza; marcado, fica âmbar com o
   visto (`PE:155-168`). A coluna Tela ("e o selo 'Personalizado'") e a fala "São três" precisam dizer: três perfis
   prontos e o Personalizado.
7. O perfil escolhido agora é gravado na criação (`UM:825-827`, `create-company-user/index.ts:365-370`): depois de
   criar com "Operador Padrão", o detalhe mostra "Operador Padrão" (achado 2 do inventário resolvido). A lista continua
   "32 permissões · Ativo" (só o "Acesso Total" vira "Acesso total", `UMD:253`). O cap03 pode abrir o detalhe do Marcos.

**cap04 · Telas e ações**
8. **A Juliana precisa de um clique novo**: sem escolher "Personalizado" a lista não aceita clique (item 3). Foi aí que
   a varredura quebrou (cap04, passo 18). Passo novo: clicar em "Personalizado" (fica âmbar, a lista acende, tudo desligado).
9. Aviso novo **"Confira esta combinação"** no alto da coluna (`UM:1276-1290`), com até quatro frases (`UM:319-341`):
   "Ticket de Pesagem está liberado, mas o usuário não poderá criar tickets de Compra nem de Venda."; "Registrar Compra
   está ligado, mas a tela Caixa está desligada."; "Registrar Venda está ligado, mas a tela Caixa está desligada."; "O
   Cato ficará indisponível: ele consulta dados gerais da empresa e poderia revelar registros de outros usuários." A
   dica do cap04 ("o Registrar Venda sozinho não leva ninguém até o caixa") hoje é dita sem tela: agora a tela avisa.
10. Quatro ações novas mudam contadores: "Movimentações Bancárias" passa a **5 ações** ("Registrar Movimentação
    Bancária", "Registrar Transferências Financeiras"), "Clientes e Fornecedores" a **4** ("Cadastrar Parceiros"),
    "Estoque" a **3** ("Cadastrar Materiais") (`RT:269-272`). Os contadores que o roteiro cita não mudam: "Contas a
    Pagar/Receber" 4 e "2/4", "Fiscal & Ambiental" com a busca "nota" 4, "Caixa" 10, "Ticket de Pesagem" 4, busca
    "lucro" 1. A Juliana segue com 15 permissões se o mundo não ligar as novas.

**cap05 · O balanceiro e o escritório**
11. O zoom "selo âmbar 'Personalizado' e nenhum perfil marcado" agora é o **botão "Personalizado" âmbar com o visto**
    (`PE:155-168`); o seletor `span.bg-amber-500` do robô não existe mais. A fala serve.
12. A janela "Editar Usuário" tem o campo "Peso dos pedidos" (item 4) e, no fim da coluna, depois do bloco do Cato, a
    seção **"Restrições"** (`PE:493-530`). No Editar o perfil já vem escolhido, então nada fica travado.

**Backend falso (todos os capítulos que listam, criam ou salvam)**
13. Listar: `profiles` agora embute `user_bank_account_access!user_bank_account_access_user_id_fkey(bank_account_id)`
    e a tela lê `user_scale_weight_policies` (`user_id`, `requires_scale`) e `bank_accounts` (`UM:162-177,192-211`); se
    qualquer uma falhar, a lista mostra "Não foi possível carregar os usuários.". Criar: o corpo leva `preset`
    (obrigatório: `full_access`, `standard_operator`, `view_only` ou `custom`) e `bank_account_ids`; a resposta
    precisa de `userId`; em seguida a tela grava `profiles.initial_screen_path` e chama a RPC
    `set_user_scale_weight_policy(p_user_id, p_requires_scale)` (`UM:398-427`). Salvar: a RPC virou
    **`save_user_permissions_and_bank_accounts`** (`p_user_id`, `p_permissions`, `p_preset`, `p_bank_account_ids`,
    `p_scale_weight_override`) (`UM:558-564`); `save_user_permissions` não é mais chamada.
    A falha da varredura no cap01 (texto do cabeçalho da aba não encontrado) não tem causa no código da aba, que não
    mudou: hipótese de mundo ou robô, a conferir na regravação.

## 2. Falta cobrir

| # | O que é (onde) | Quando o cliente usa | Vale? |
|---|---|---|---|
| L1 | **Restrições** (4 chaves, `RT:338-367`; seção `PE:493-530`): "Ver somente clientes e fornecedores que cadastrar", "Ver somente os pedidos que lançar", "Ver somente os tíquetes de pesagem que criar", "Usar somente as contas bancárias liberadas". "Ficam desligadas por padrão. Ative somente para uma exceção consciente." Ligar qualquer uma tira o Cato da pessoa (aviso do item 9) e tira o perfil pronto (vira "Personalizado"); não valem para quem é "Acesso Total" (`hooks/usePermissions.tsx:262-263`). Não entram na contagem "N permissões" nem aparecem no detalhe (`UM:220-222`, `UMD:353-362`). | Comprador de rua que só pode ver os próprios fornecedores e pedidos; balanceiro que só vê os próprios tickets | **Sim, capítulo novo** (P4) |
| L2 | **Contas bancárias por usuário** (1.59.165): com a quarta restrição ligada abre "Contas liberadas para este usuário" / "Marque as contas que poderão aparecer em pagamentos por Pix ou transferência." com um cartão por conta (`UM:1351-1442`). Sem conta marcada: "Selecione pelo menos uma conta bancária para este usuário" (`UM:782-786`). Sem conta cadastrada: "Nenhuma conta bancária ativa foi encontrada. Cadastre uma conta antes de salvar esta restrição." "Cofre e cartões não são afetados" (`RT:364-365`). | Operador que paga por Pix só pode usar a conta do dia a dia | **Sim, no mesmo capítulo** (P4) |
| L3 | **Peso dos pedidos por usuário** (item 4 e item 1). A regra da empresa é "Peso somente pela balança", em Integrações, "Padrão da empresa; exceções ficam em Usuários e Permissões" (`components/settings/SettingsIntegrationsContent.tsx:651,665`). | Empresa exige balança, mas o gerente pode digitar; ou só o balanceiro novo é obrigado | **Sim, trecho** no cap05 (P5). A regra da empresa é da **T5** (cap07 de lá; o subtítulo que a T5 cita mudou, avisar a auditoria da T5) |
| L4 | **Foto e tela inicial já na criação** (item 2) | Todo usuário novo | **Sim**, reescreve a dica do cap02 (P1) |
| L5 | **Aviso "Escolha primeiro o perfil..."**, selo "Recomendado", "Personalizado" como ponto de partida (itens 3, 5, 6) | Toda criação | **Sim**, ajustes nos caps 02 a 04 (P1, P2, P3) |
| L6 | **Aviso "Confira esta combinação"** (item 9) | Montagem na mão | **Sim, trecho** no cap04 (P3) |
| L7 | **Cada permissão do catálogo** (24 telas e 60 ações, `RT:111-146,216-311`). O roteiro fala de 10 telas e 13 ações. Faltam, por grupo: **Caixa** "Registrar Compra", "Registrar Despesa", "Registrar Receita", "Abrir Caixa", "Fechar Caixa", "Ver e Operar Todos os Caixas", "Realizar lançamentos e abrir/fechar caixas com data retroativa"; **Histórico do Caixa**; **Categorias Financeiras** + "Gerenciar Categorias Financeiras"; **Relatório Financeiro** "Exportar Relatórios"; **Contas** "Gerenciar Contas Recorrentes", "Excluir Conta"; **Pedidos** "Editar e Excluir Pedidos"; **Movimentações Bancárias** "Usar Contas Bancárias", "Registrar Movimentação Bancária", "Registrar Transferências Financeiras"; **Fiscal** "Emitir MDF-e (Transporte)", "Emitir Documentos Ambientais (MTR/CDF)", "Manifestar Notas Recebidas", "Exportar Pacote Contábil" e as cinco do SPED ("Consultar", "Configurar", "Classificar Entradas", "Gerar", "Registrar validação"); **Estoque** "Editar, Movimentar e Excluir Materiais", "Zerar Estoque", "Cadastrar Materiais"; **Histórico de Materiais**, **Relatório de Estoque**; **Ticket** "Ticket de Pesagem — Compra", "— Venda", "Ver Tickets Valorizados"; **Produção** (3 ações, "Ver Custos na Produção"); **Coletas & Logística**; **Clientes** "Cadastrar Parceiros", "Editar e Excluir Clientes/Fornecedores", "Lançar crédito/débito no saldo"; **Funcionários** (3 ações); **CRM/Kanban**; **Gerencial** (3 telas); **Agenda**; **Configurações** (as seis "Configurar ..." além de "Gerenciar Usuários"); **Assinatura** + "Gerenciar Assinatura". | Quem monta acesso na mão | **Sim, capítulo novo** de passeio por grupo (P6). O detalhe de cada uma é da aula da tela (T6 caixa, T8 ticket, T10 estoque, T13/T14 financeiro, T16 a T18 fiscal, T19, T11, T12, T26, T22) |
| L8 | As quatro ações novas (`RT:269-272`) só são conferidas nas operações feitas pelo Cato (`supabase/migrations/20261114160000_cato_operation_framework.sql:11-16`); nenhuma tela de `src/` as consulta. | Quem usa o Cato para lançar | **Só citar** no P6 (uma frase); o detalhe é da **T21** |
| L9 | **"Relatório por Usuário"** (botão do topo, `UM:1094-1097`; `components/EmployeeOrdersReportDialog.tsx:374-375`): "Exporte um relatório de compras e vendas por usuário"; "Período"; "Usuários incluídos (N de N)" com "Desmarcar todos" / "Marcar todos"; botões "Excel" e "Visualizar / PDF"; avisos "Relatório exportado com sucesso!" / "Relatório gerado com sucesso!". Já existia no 1.59.154 e o roteiro só passa a câmera no botão. | Dono quer saber quanto cada operador comprou e vendeu no mês | **Sim, capítulo curto** (P7) |
| L10 | **Busca da lista** "Buscar por nome ou e-mail", "N encontrado(s)", vazio "Nenhum usuário encontrado" / "Ajuste os termos da busca." (`UMD:182-218`); paginação de 10 por página (`UM:996-1000`) | Equipe grande | **Só citar** (uma frase no cap01, P8) |
| L11 | **"Limite de Usuários Excedido"** (`components/UserExcessModal.tsx:165-166`): abre sozinha quando há mais ativos que o plano permite (`UM:119,381-385`): "Seu plano permite N usuários ativos, mas você tem M. Selecione X usuário(s) para desativar." | Plano reduzido com a equipe maior que o novo limite | **Só citar** no cap08 (P8); mostrar exigiria um mundo com excesso |
| L12 | **Quem cuida da aba sem ser master** vê, no Editar de outra pessoa, só a foto, o nome e o e-mail fixos e a frase "Você pode ajustar as permissões deste usuário, mas somente o master ou o próprio usuário pode alterar nome, e-mail e senha." (`UM:1244-1261`) | Gerente com "Gerenciar Usuários" | **Não**: a fala do cap06 já diz a regra; mostrar pede login de outro usuário |
| L13 | **E-mail repetido** na criação: "Esse email já é usuário desta empresa." / "Esse email já está em uso em outra empresa. Cada email só pode pertencer a uma empresa por vez." (`create-company-user/index.ts:235,243`) | Recontratação, e-mail usado em outra empresa | **Só citar** no cap02 (P1) |
| L14 | **"Última atividade"** ("Online agora", "há ...", "Sem atividade registrada", `UMD:314-320`): aparece na tela e não é falada | Saber quem está usando | **Só citar** (P8) |
| L15 | Regra do "Tela inicial": "Só aparecem telas liberadas acima. Se a permissão mudar, o sistema escolhe outra tela válida." (`UM:1307-1309`) | Tela escolhida deixa de estar liberada | **Só citar** (P5) |
| L16 | Bloco do Cato "Quem pode conversar com o assistente" (`PE:400-470`) | | **Não aqui**: decisão do plano, fica na **T21**. O P4 só diz que restrição desliga o Cato |

## 3. Proposta

Tom do roteiro atual. Marcas iguais (`[BACKEND]`, `[ZOOM]`, `[ILUSTRAÇÃO]`). Numeração nova sugerida no fim.

### P1 · cap02, trocar as duas últimas linhas (foto e passagem)

| Tela | Fala |
| --- | --- |
| Em "Foto do Usuário", clica em "Selecionar foto" e escolhe `marcos-antunes.jpg`: a foto aparece na bolinha ao lado ("Foto opcional para o novo usuário"). [BACKEND: storage `avatars` e `profiles.avatar_url` depois do criar, com o `userId` da resposta] | A foto é opcional. Escolho a do Marcos agora mesmo, e ela já entra junto com o cadastro. Se preferir, dá pra colocar ou trocar depois, no Editar. |
| A câmera passa para a coluna "Permissões": o aviso âmbar "Escolha primeiro o perfil deste usuário", com a lista apagada embaixo. [ZOOM: o aviso, a frase inteira] | Uma dica: cada e-mail só pode estar em uma empresa. Se ele já estiver em uso, o sistema avisa na hora de criar. [pause] Agora, o que o Marcos vai poder fazer. Repara que a tela pede o perfil antes de liberar a lista. |

### P2 · cap03, trocar as linhas 1, 2 e 8 (perfis)

| Tela | Fala |
| --- | --- |
| (setup reabre a janela com nome, e-mail, senha e foto) A câmera foca "Perfis rápidos": "Acesso Total", "Operador Padrão" com o selo "Recomendado", "Somente Visualização" e "Personalizado"; embaixo, o aviso "Escolha primeiro o perfil deste usuário" e a lista apagada. | Do lado direito ficam as permissões. E a primeira escolha é o perfil. Sem ele, a lista fica apagada e o sistema não deixa criar. |
| [ILUSTRAÇÃO: os três chaveiros, e um quarto, vazio, com a etiqueta "Personalizado", que entra na palavra "Personalizado".] | São três perfis prontos, e o Personalizado. Pensa num chaveiro: cada perfil pronto já vem com um conjunto de chaves. O Personalizado vem vazio, pra você montar. |
| (linhas 3 a 6 iguais; ao clicar em "Operador Padrão" o selo "Recomendado" some e entra o visto) | (iguais; na linha do Operador Padrão, acrescentar no fim:) É o que o sistema recomenda pra maioria da equipe. |
| Clica em "Criar Usuário": "Usuário criado com sucesso!"; a lista mostra "Marcos Antunes" com a foto e "32 permissões · Ativo"; selo "2 / 3 usuários". Clica no Marcos: "Perfil de acesso" "Operador Padrão". [BACKEND: edge `create-company-user` com `preset` `standard_operator`, resposta com `userId`; RPC `set_user_scale_weight_policy`; vira `apos-cap03` com `permission_preset` gravado e `avatar_url`] | Criar Usuário. Pronto, o Marcos está na lista, ativo, com a foto e o perfil Operador Padrão. |

### P3 · cap04, linha nova depois da primeira e troca da linha da dica do Caixa

| Tela | Fala |
| --- | --- |
| (depois de preencher a Juliana) Clica em "Personalizado": o botão fica âmbar com o visto, o aviso some e a lista acende, com tudo desligado. | Agora a Juliana, do escritório. Ela não se encaixa em nenhum perfil pronto. Então eu clico em Personalizado, e a lista libera, com tudo desligado, pra montar na mão. (substitui a fala da primeira linha) |
| No bloco "Financeiro", abre "Clique para ver 10 ações" da tela "Caixa" (desligada) e liga "Registrar Venda": aparece no alto "Confira esta combinação" com "Registrar Venda está ligado, mas a tela Caixa está desligada."; desliga "Registrar Venda" e o aviso some. [ZOOM: o aviso "Confira esta combinação", a frase inteira] | Uma dica: primeiro a tela, depois as ações. Olha o que acontece se eu ligar o Registrar Venda com a tela Caixa desligada: o sistema avisa pra conferir a combinação, porque sem a tela a pessoa não chega no caixa. Desligo, e o aviso some. (substitui a linha "A câmera mostra a linha Caixa") |

### P4 · capítulo novo "Restrições e contas do banco" (vinheta: PERMISSÕES), depois do cap05

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap05`); clica em "Marcos Antunes" e em "Editar"; rola a coluna "Permissões" até o fim, passando pelo bloco escuro do Cato sem parar: a seção "Restrições" ("Ficam desligadas por padrão. Ative somente para uma exceção consciente."), quatro chaves desligadas. | Até aqui a gente liberou coisas. No fim da lista tem o contrário: as restrições. Elas ficam desligadas, e só entram quando existe uma exceção de verdade. |
| [ILUSTRAÇÃO: um pátio com três operadores e três pilhas de fichas; na palavra "próprios", duas pilhas ficam cinza e sobra a de um operador só.] | Pensa num comprador que roda a rua e não deve ver os fornecedores dos colegas. A restrição faz a pessoa enxergar só o que ela mesma lançou. |
| De volta à janela. [ZOOM: as três primeiras linhas: "Ver somente clientes e fornecedores que cadastrar", "Ver somente os pedidos que lançar", "Ver somente os tíquetes de pesagem que criar", a frase inteira] | São três desse tipo: só os clientes e fornecedores que ela cadastrar, só os pedidos que ela lançar e só os tickets de pesagem que ela criar. |
| Liga "Usar somente as contas bancárias liberadas": abre embaixo "Contas liberadas para este usuário" ("Marque as contas que poderão aparecer em pagamentos por Pix ou transferência."), com os cartões "Conta Principal", "Conta Secundária" e "Poupança antiga". | A quarta é a das contas do banco. Ligo, e aparece a lista de contas da empresa. |
| Marca "Conta Principal": o cartão pinta com a cor da conta. [ZOOM: os cartões, a frase inteira] | Marco só a Conta Principal. Com isso, no Pix e na transferência, o Marcos só vê e só usa essa conta. O cofre e os cartões continuam como estão. |
| A câmera sobe ao topo da coluna: "Confira esta combinação" não aparece (o Marcos não tem o Cato); nos "Perfis rápidos", "Personalizado" âmbar. | Três detalhes. Com a restrição ligada, é preciso marcar pelo menos uma conta, senão o sistema não salva. Qualquer restrição desliga o Cato da pessoa, pra ele não contar o que ela não pode ver. E restrição não combina com Acesso Total: o perfil passa a ser Personalizado. |
| Clica em "Cancelar" (nada muda). | Aqui eu só mostrei, então cancelo. O Marcos continua usando todas as contas. |

Decisão embutida: **mostrar e cancelar**, para o Marcos seguir com todas as contas nas aulas T6, T7, T13 e T14. Se o Kaik
preferir gravar a restrição de verdade, as cenas de Pix do Marcos nas outras aulas passam a mostrar só a Conta Principal.

### P5 · cap05, duas linhas novas depois da linha "Tela inicial"

| Tela | Fala |
| --- | --- |
| A câmera fica em "Tela inicial" e na ajuda "Só aparecem telas liberadas acima. Se a permissão mudar, o sistema escolhe outra tela válida.". | Só aparecem aqui as telas que ele tem. E se um dia a permissão mudar, o sistema escolhe outra tela sozinho. |
| Logo abaixo, abre "Peso dos pedidos": "Herdar padrão da empresa" (marcado), "Exigir peso da balança", "Permitir digitação manual"; fecha sem trocar. [ZOOM: as três opções, a frase inteira] | Embaixo fica o Peso dos pedidos. É uma exceção por pessoa: obrigar o peso a vir da balança, ou liberar a digitação, mesmo que a regra da empresa seja outra. O Marcos segue o padrão da empresa. A balança, a gente vê no tutorial do EcoTray. |

### P6 · capítulo novo "O mapa das permissões" (vinheta: PERMISSÕES), depois do P4

Passeio pela lista no "Editar" do Marcos, abrindo as ações de cada tela citada; sem ligar nada; termina em "Cancelar".

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap05`); Marcos → "Editar"; a câmera no bloco "Financeiro". [ILUSTRAÇÃO curta: um mapa com quatro bairros, "Financeiro", "Materiais", "Cadastros" e "Sistema", que acendem um a um.] | Antes de seguir, vale um passeio pela lista inteira, pra você saber o que existe em cada grupo. |
| Abre "Clique para ver 10 ações" do "Caixa": "Registrar Compra", "Registrar Venda", "Registrar Despesa", "Registrar Receita", "Abrir Caixa", "Fechar Caixa", "Ver Dinheiro Total em Caixa", "Ver Projeção de Lucro", "Ver e Operar Todos os Caixas", "Realizar lançamentos e abrir/fechar caixas com data retroativa". | No Caixa, cada operação tem a sua chave: compra, venda, despesa e receita, abrir e fechar o caixa. E duas pra dar com cuidado: operar o caixa dos outros e lançar com data retroativa. |
| Desce: "Histórico do Caixa", "Movimentações Bancárias" (5 ações abertas), "Relatório Financeiro" ("Exportar Relatórios"), "Contas a Pagar/Receber" (4), "Categorias Financeiras", "Pedidos" ("Editar e Excluir Pedidos"). | No banco, o Usar Contas Bancárias deixa pagar por Pix sem ver saldo. O Gerenciar mostra os saldos e as contas. O relatório financeiro tem a chave de exportar, as contas têm a das recorrentes e a de excluir, e os pedidos, a de editar e excluir. |
| "Fiscal & Ambiental": abre "Clique para ver 11 ações". [ZOOM: a lista das 11, a frase inteira] | No Fiscal, cada documento é uma chave separada: nota de produto, nota de serviço, manifesto de transporte, documentos ambientais, manifestar notas recebidas e o pacote do contador. E o SPED tem cinco: consultar, configurar, classificar, gerar e registrar a validação. |
| Bloco "Materiais": "Estoque" (3 ações), "Histórico de Materiais", "Relatório de Estoque", "Ticket de Pesagem" (4), "Produção" (3), "Coletas & Logística". | Nos Materiais: no Estoque, dá pra deixar a pessoa só cadastrar material, sem editar preço, e o Zerar Estoque é uma chave à parte. O Ticket separa compra de venda. E a Produção tem a chave de ver os custos. |
| Bloco "Cadastros": "Clientes e Fornecedores" (4 ações), "Funcionários (RH)" (3), "CRM/Kanban". | Nos Cadastros: cadastrar parceiro é uma coisa, editar e excluir é outra. Ver o saldo e lançar crédito ou débito no saldo também são chaves separadas. Em Funcionários, excluir e cuidar do ponto têm as suas. |
| Bloco "Sistema": "Gerencial - Dashboard", "Gerencial - Financeiro", "Gerencial - Estoque", "Agenda", "Configurações" (7 ações abertas), "Assinatura" ("Gerenciar Assinatura"). | E no Sistema ficam o Gerencial, a Agenda, a Assinatura e as Configurações, com uma chave pra cada aba, como a gente viu no começo. |
| A câmera volta ao topo; clica em "Cancelar". | Algumas dessas chaves também valem quando o pedido é feito pelo Cato, o assistente. E cada uma aparece de novo no tutorial da tela dela. Aqui eu cancelo, sem mudar nada. |

### P7 · capítulo novo "Relatório por Usuário" (vinheta: USUÁRIOS), antes do Recapitulando

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap05`), na aba; clica em "Relatório por Usuário": janela "Relatório por Usuário" ("Exporte um relatório de compras e vendas por usuário"). | Ainda nesta aba tem um botão que pouca gente nota: o Relatório por Usuário. Ele mostra quanto cada pessoa comprou e vendeu. |
| Abre "Período" e escolhe "Este mês". | Primeiro o período. Escolho este mês. |
| Em "Usuários incluídos (3 de 3)", desmarca "Juliana Prado" ("2 de 3"); passa por "Desmarcar todos". | Depois, quem entra. Vêm todos marcados. Tiro a Juliana, que não lança pedido. |
| A câmera passa por "Excel" e clica em "Visualizar / PDF": aviso "Relatório gerado com sucesso!" (o relatório abre em outra janela; a câmera fica na aba). | Dá pra baixar em Excel ou abrir pra imprimir e salvar em PDF. O relatório traz as compras e as vendas de cada um, com os pedidos detalhados. |

Se o mundo do fim da T1 não tiver pedidos, o capítulo fica só na janela (três primeiras linhas) e a última fala vira:
"Quando a equipe começar a lançar, é aqui que você acompanha cada um." (decisão abaixo).

### P8 · frases soltas

| Onde | Tela | Fala a acrescentar |
| --- | --- | --- |
| cap01, depois da linha do contador | A câmera passa pela busca "Buscar por nome ou e-mail". | Com a equipe grande, a busca acha a pessoa pelo nome ou pelo e-mail. |
| cap01, linha do detalhe do Rafael | A câmera passa por "Última atividade" "Online agora" e "Peso dos pedidos" "Padrão da empresa". | E aqui você vê quando a pessoa usou o sistema pela última vez. |
| cap08, depois da linha das cadeiras | (ilustração) Uma cadeira some e um crachá fica de pé. | E se o plano diminuir e sobrar gente, o sistema abre uma janela pedindo pra você escolher quem desativar. |
| cap10 (recap) | Montagens novas: a seção "Restrições" e a janela "Relatório por Usuário". | Conheceu as restrições, as contas liberadas por pessoa e o Relatório por Usuário. |

### Ordem sugerida

00 Abertura · 01 Onde fica · 02 Criar o usuário · 03 Os perfis rápidos · 04 Telas e ações · 05 O balanceiro e o
escritório · **06 Restrições e contas do banco (novo)** · **07 O mapa das permissões (novo)** · 08 Desativar ou
excluir · 09 Passar o controle · 10 O limite de usuários · 11 Esconder o valor · **12 Relatório por Usuário (novo)** ·
13 Recapitulando. O título do cap03 pode virar "Os perfis rápidos" (deixaram de ser só três opções na tela).

### O que o mundo fictício precisa

- **Sementes da T2 com contas bancárias**: `bank_accounts` com "Conta Principal" (padrão), "Conta Secundária" e
  "Poupança antiga", `kind` `bank`, `is_archived` falso, sem logo (`institution_code` nulo), com `color`.
- **Tabelas novas**: `user_bank_account_access` (vazia; precisa responder ao embutido pelo nome da chave
  `user_bank_account_access_user_id_fkey`) e `user_scale_weight_policies` (vazia).
- **Edge `create-company-user`**: aceitar `preset` e `bank_account_ids`, gravar `permission_preset`, responder
  `{success, userId, user:{...}}`.
- **RPCs**: `save_user_permissions_and_bank_accounts` (substitui `save_user_permissions` no cap05) e
  `set_user_scale_weight_policy` (chamada em toda criação).
- **Marcos**: `permission_preset` `standard_operator` e `avatar_url` já em `apos-cap03`; no cap05 a foto deixa de ser
  enviada (ou vira "trocar a foto"); P4 e P6 terminam em "Cancelar", estado igual.
- **P7**: pedidos de compra e venda de novembro com `user_id` do Rafael e do Marcos e os itens (a consulta está em
  `components/EmployeeOrdersReportDialog.tsx`); `window.open` do relatório precisa não roubar o foco da gravação.
- **Robô**: seletor do "Operador Padrão" sem `exact` (ou pelo texto inicial), clique em "Personalizado" antes da lista
  no cap04, zoom do cap05 no botão `Personalizado` âmbar, medidas novas da janela (campo "Peso dos pedidos") e do detalhe.

## 4. Estimativa

| Proposta | Fala a mais |
|---|---|
| P1 cap02 (troca) | +10 s |
| P2 cap03 (troca) | +14 s |
| P3 cap04 (troca) | +14 s |
| P4 Restrições e contas do banco (novo) | +78 s |
| P5 cap05 (2 linhas) | +26 s |
| P6 O mapa das permissões (novo) | +100 s |
| P7 Relatório por Usuário (novo) | +34 s |
| P8 frases soltas | +20 s |
| **Total** | **~296 s de fala (~5 min), 3 capítulos novos**; a aula vai de ~11 para ~16,5 min com vinhetas e esperas |

## 5. Depende de decisão do Kaik

1. **Foto na criação (P1)** ou manter no Editar só corrigindo a frase errada (custa menos regravação do cap05).
2. **Restrição de contas: mostrar e cancelar (proposto)** ou gravar de verdade no Marcos (muda o Pix dele nas T6, T7, T13, T14).
3. **O mapa das permissões (P6)**: capítulo de 100 s citando todos os grupos, ou versão curta (~40 s) só com Caixa e Fiscal.
4. **Relatório por Usuário (P7)** aqui na T2 (o botão é desta tela) ou na T9 "Pedidos"; e se o mundo da T2 terá pedidos.
5. **Juliana com as ações novas do banco** ("Registrar Movimentação Bancária", "Registrar Transferências Financeiras")?
   Hoje só contam para pedidos feitos pelo Cato; proposto não ligar (ela segue com 15 permissões).
6. **Peso dos pedidos**: só mostrar (proposto) ou deixar o Marcos em "Exigir peso da balança" (mexe com T5, T7 e T8).
