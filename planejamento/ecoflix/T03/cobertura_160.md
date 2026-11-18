# Cobertura 1.60.10 · T3 Materiais e tabelas de preço

Auditoria de 18/11/2026, só leitura de código. Base: `/dev/shm/ecoflix-src` (`APP_VERSION = "1.60.10"`,
`src/config/version.ts:16`) contra o roteiro (1.59.154). Caminhos relativos a `src/`; linhas do 1.60.10.

> **Aviso de escopo (ler primeiro).** O pedido chegou como "T03 = Venda de material (`pages/Sale.tsx`)". Na trilha, a
> **T3 é "Materiais e tabelas de preço"** (`TRILHA.md`, `T03/plano.md`, `T03/roteiro.md`); a tela de Venda é da
> **T7 "Comprar e vender sucata"**, e a edição de pedido antigo é da **T9**. Esta auditoria cobre a T3 de verdade
> (tela Estoque, tabelas de preço e o trecho de compra do cap07). O que do pedido é da tela de Venda está mapeado na
> seção 5, sem roteiro: a auditoria de `Sale.tsx` precisa ser feita com Tnn = T07 (e T09). `T07/cobertura_160.md` ainda
> não existe.

Arquivos da aula **sem nenhuma mudança** entre `f37573ea0` e `5290be4cd`: `i18n/locales/pt-BR/materials.json`,
`PriceTableSettingsModal.tsx`, `PriceTablesHelpModal.tsx`, `StockMovementDialog.tsx`, `TransferMaterialDialog.tsx`,
`notas-fiscais/NcmSelectorModal.tsx`, `components/materiais/*` (grupos, importar planilha, zerar, seletor de exportação),
`components/estoque/*`, `utils/materialsExport.ts`, `utils/priceTableGenerator.ts`, `OrderFormInputs.tsx`,
`constants/materialUnits.ts`, `hooks/useUndoToast.ts`. Ou seja: caps. 2, 3, 4, 5, 8, 9 e 10 batem com o 1.60.10 como estão.

## 1. Mudou no app (por capítulo)

**cap01 · A tela Estoque**
1. Menu "..." de cada tabela na coluna "Tabelas de Preço" ganhou itens. Antes: "Configurações" e "Excluir". Agora, na
   ordem: "Configurações", **"Duplicar tabela"**, separador, **"Fixar para meus pedidos e tickets"** (vira **"Remover minha
   tabela fixada"** quando é a fixada), **"Definir como principal da empresa"** (só fora da principal e só para admin ou
   quem tem `action_edit_delete_materials`), separador, "Excluir" (`components/PriceTableSidebar.tsx:280-320`, permissão
   `:62`). O roteiro não abre esse menu, então nenhuma fala fica errada; a tela que a câmera mostra é a mesma.
2. A tabela fixada pelo usuário ganha um alfinete ao lado do nome, com rótulo de acessibilidade "Fixada para meus pedidos
   e tickets" (`PriceTableSidebar.tsx:256-261`). Só aparece se alguém fixar; no mundo base ninguém fixa.

**cap02 a cap05 · Novo/Editar Material**
3. "Quantidade em Estoque" trocou o formato do campo (`decimals={3}` virou `maxDecimals={3}`, `pages/Materiais.tsx:2085-2091`;
   nota 1.59.159 "Estoque mantém os milhares ao editar materiais"). O rótulo e o placeholder "0,000" são os mesmos; muda
   só a máscara do número ao reabrir o "Editar" (deixa de forçar três casas). O roteiro não cita o valor formatado desse
   campo: **nada a mudar na fala**; conferir na regravação se o "Resumo" continua "120 Kg".

**cap06 · Editar preços em massa**
4. Só mudança interna no texto da variação personalizada das tabelas vinculadas (`components/BulkPriceEditModal.tsx:148-155`;
   nota 1.59.160). Rótulos, grade e avisos iguais. **Nada a mudar.**

**cap07 · Várias tabelas de preço**
5. **A tabela inicial do pedido tem um degrau novo.** Antes: tabela do parceiro, senão a principal. Agora: tabela do
   parceiro → **tabela fixada pelo usuário** → principal da empresa (`lib/precos/priceTablePreference.ts:12-28`; usado em
   `pages/Purchase.tsx:1057`, `:1807`, `:1823`, `pages/Sale.tsx:932`, `:1567`, `:1583`, `pages/WeighingTicket.tsx:2453`).
   A fala do roteiro ("Escolho o depósito, e a tabela dele já vem selecionada") **continua certa**, porque o parceiro vem
   primeiro. A escada de três degraus do preço (personalizado → tabela do pedido → preço do material) não mudou
   (`components/OrderFormInputs.tsx:449-451`, avisos "Preço especial aplicado para …" e "Preço da tabela aplicado para …").
6. No seletor "Tabela de Preços" da compra, a tabela fixada mostra o alfinete "Minha tabela fixada"
   (`components/PriceTableSelector.tsx:72,103`, `components/PriceTableSelect.tsx:69`). Não aparece no mundo base.
7. Trocar o fornecedor ou a tabela **com itens já lançados** agora abre a janela "Trocar tabela de preços?" / "Trocar
   fornecedor?" ("O pedido já tem N itens lançados. Escolha o que fazer com os preços atuais."; "Itens que mudam", "Total se
   atualizar"; botões "Cancelar", "Só nos próximos", "Atualizar N itens";
   `components/orders/OrderPriceContextChangeDialog.tsx:48-88`; `pages/Purchase.tsx:2466-2500`, `:6462`). O cap07 troca de
   material **sem incluir item**, então a janela não abre na gravação. É assunto da T7; aqui cabe uma frase (ver 3.4).
8. Ficha do fornecedor: "Tabela de Preços Padrão" continua igual, só mudou de linha (`components/EntityFormDialog.tsx:1691`).
   A lista de parceiros ganhou o vazio "Nenhum fornecedor encontrado" / "Tente outro termo ou limpe a busca."
   (`components/clients-suppliers/ClientsListView.tsx:675-685`); a busca "Depósito" do roteiro acha o parceiro, não aparece.

**Fora da tela, mas toca a aula:** permissão nova "Cadastrar Materiais" ("Criar materiais sem editar preços ou estoque de
materiais existentes", `config/routes.ts:272`). No 1.60.10 ela só existe na lista de permissões; a tela Estoque continua
liberando "+ Novo Material" por `action_edit_delete_materials` (`pages/Materiais.tsx:219`, `:2789`). Assunto da T2; não citar aqui.

Total: **8 mudanças**, nenhuma quebra fala ou rótulo do roteiro atual. As que pedem conteúdo novo são a 1, a 2 e a 5.

## 2. Falta cobrir

| # | O que é (rótulo exato) | Quando o cliente usa | Vale? |
|---|---|---|---|
| F1 | **"Duplicar tabela"** (menu "..." da tabela). Cria "<nome> (cópia)", **independente**, com os preços que valiam na hora; fica selecionada. Aviso `Tabela "<nome>" duplicada com sucesso!` (`hooks/usePriceTables.tsx:173-194`; RPC `duplicate_price_table`) | Montar uma tabela nova a partir de outra (promoção, cliente grande) sem digitar tudo | **Sim**, trecho novo |
| F2 | **"Fixar para meus pedidos e tickets"** / "Remover minha tabela fixada". É por usuário. Avisos "Tabela fixada para seus novos pedidos e tickets" e "Tabela pessoal removida; você voltará a usar a principal da empresa" (`usePriceTables.tsx:224-245`) | Operador que sempre trabalha numa tabela (ex.: quem compra na rua) | **Sim**, trecho novo; muda a explicação de "qual tabela o pedido abre" |
| F3 | **"Definir como principal da empresa"** → "Definir “<nome>” como principal?" · "Os preços desta tabela virarão a base da empresa. A principal atual será preservada como independente e todas as tabelas vinculadas serão recalculadas automaticamente." · "Cancelar" / "Definir como principal"; aviso "Tabela principal atualizada" (`PriceTableSidebar.tsx:379-405`, `usePriceTables.tsx:196-222`) | Trocar a base de preços da empresa | **Sim, só mostrar e cancelar** (mexe em todos os preços do mundo) |
| F4 | **"Configurações"** da tabela → "Editar Tabela de Preços" (mesmos campos do "Nova Tabela"; "Tabela de preço atualizada!"; `PriceTableSettingsModal.tsx:255`) | Mudar o nome ou a variação (de +4% para +5%) | **Sim**, uma frase com a janela aberta |
| F5 | **"Excluir"** tabela → "Excluir Tabela de Preços" · "Tem certeza que deseja excluir a tabela "<nome>"? Esta ação não pode ser desfeita e todos os preços desta tabela serão perdidos." → "Tabela de preço excluída!"; a principal não tem "Excluir" (`PriceTableSidebar.tsx:408-427`) | Limpar tabela que não usa mais | **Sim**, apagando a cópia do F1 |
| F6 | **Cadeado por material na tabela vinculada** ("Editar Tabela" com a vinculada escolhida): coluna "Variação"; cadeado fechado "Variação padrão - clique para personalizar", aberto "Variação personalizada - clique para usar padrão"; setas "Aumenta o preço — clique para diminuir"; "%"/"R$" (`BulkPriceEditModal.tsx:1318-1402`) | Um material da tabela vinculada foge da regra (ex.: fio encapado +2% e não +4%) | **Sim**, trecho curto |
| F7 | **Venda abaixo da compra**: "Preço de venda abaixo do custo" · "O preço de venda (…) está abaixo do preço de compra (…). Isso registra prejuízo nesse material. Deseja continuar?" · "Salvar mesmo assim" (`materials.json:120-122`; no lote, `BulkPriceEditModal.tsx:1833-1868`). Não bloqueia. O plano deixou de fora (decisão 1) | Erro de digitação no reajuste | **Sim**, dica curta no cap06 |
| F8 | **Variação em valor** (R$) e **"Diminui"** no "Nova Tabela", e tabela **independente** (sem marcar "Vincular à tabela principal") | Tabela "dez centavos a menos", ou tabela toda digitada | **Só citar** no cap07 |
| F9 | **"Como funciona"** (?) da coluna: "Tabela Principal (Padrão)", "Tabelas Independentes", vinculadas, "Sobrescritas Individuais", hierarquia (`PriceTablesHelpModal.tsx:35-166`) | Dúvida na hora | **Só citar** (mostrar o botão) |
| F10 | **"Prefixo"** do código ("Ex: P"; "Fica assim: P70"; "O prefixo aparece na tela, no comprovante e na nota fiscal. O número no banco não muda.") e a ação em massa **"Definir prefixo"** ("Definir prefixo dos selecionados"; `components/materiais/BulkMaterialPrefixDialog.tsx:89-102`) | Quem separa famílias por letra | **Depende de decisão** (o plano tirou porque a fonte tira). Com "cobrir tudo", proponho trecho curto no cap03 |
| F11 | **Seleção em massa**: marcar as caixinhas abre a barra com "Transferir Estoque", "Definir prefixo", ("Definir resíduo do MTR", só com sistema ambiental na UF) e excluir → "Excluir N material(is)?" · "Atenção: Alguns materiais possuem estoque. Eles serão excluídos mesmo assim." (`pages/Materiais.tsx:3653-3686`; `materials.json:103-105`) | Arrumar vários materiais de uma vez | **Sim**, trecho curto no cap10 (só mostrar a barra) |
| F12 | **Ordenar a lista** clicando no título da coluna (código, nome, estoque, valor pago, preço médio, compra, venda; `pages/Materiais.tsx:3091-3159`) | Achar o material com mais estoque ou o mais caro | **Só citar** no cap01, com um clique em "Estoque Atual" |
| F13 | Preferência **"Múltiplas Tabelas de Preço"** em Configurações › Usabilidade ("Permite criar e gerenciar múltiplas tabelas de preço vinculadas"; `components/settings/SettingsUsabilityContent.tsx:759-773`). Desligada, a coluna some | Cliente que não vê a coluna | **Só citar** no cap07 (uma frase, sem ir à tela) |
| F14 | Formato **"Térmico"** da tabela em PDF e **"Estoque (Excel)"** | Imprimir a tabela na impressora do balcão | Já citados no cap09. **Não** gravar a mais |
| F15 | "Trocar tabela de preços?" com itens lançados (mudança 7) | No meio do pedido | **Só citar**; a demonstração é da **T7** |
| F16 | Aba "Preços" da ficha do parceiro (preço personalizado, "Vinculada à tabela principal") | Preço especial por parceiro | **T4**. Não repetir |
| F17 | "Posição de Estoque" e histórico do material | Saldo em data passada | **T10**. Não repetir |
| F18 | Aba "Produção" do material; "Resíduo do MTR"; "Tipo do item no SPED Fiscal" | Módulos | **T11**, **T18**, **T17**. Não repetir |
| F19 | Cato atualiza preços por conversa ou por print de tabela (nota 1.60.0) | Reajuste por foto | **T21**. Uma frase no recap, opcional |
| F20 | Preço do material em outra moeda (`purchase_price_currency`, `pages/Materiais.tsx:153-158`) | Empresas fora do Brasil | **Não**: o mundo é só real |

Total: **20 lacunas** (7 "sim", 5 "só citar", 1 depende de decisão, 7 "não" ou de outra aula).

## 3. Proposta

### 3.1 Capítulo novo · cap08 "Duplicar, fixar e trocar a principal" (vinheta: PREÇOS), depois do cap07 atual

Os caps. 8 a 11 atuais viram 9 a 12. Semente de entrada: `apos-cap07`. O capítulo termina com o mundo igual ao da entrada.

| Tela | Fala |
| --- | --- |
| Em "Materiais" › "Estoque", coluna "Tabelas de Preço"; clique no "..." da "Tabela Depósitos": "Configurações", "Duplicar tabela", "Fixar para meus pedidos e tickets", "Definir como principal da empresa" e "Excluir". | Cada tabela tem um menu nos três pontinhos. É por ele que você ajusta, copia, fixa ou apaga uma tabela. |
| Clique em "Configurações": abre "Editar Tabela de Preços", com o nome e a variação de 4%; clique em "Cancelar". | Em Configurações, dá pra trocar o nome e a variação. Se os depósitos passarem a ganhar cinco por cento, é aqui que muda. |
| "..." → "Duplicar tabela": aviso `Tabela "Tabela Depósitos" duplicada com sucesso!`; na coluna entra "Tabela Depósitos (cópia)", selecionada, sem a corrente. [ZOOM: a tabela nova na coluna] | O Duplicar cria uma cópia com os preços de hoje. Repara que a cópia não tem a corrente: ela nasce independente, e não acompanha mais a principal. Serve de ponto de partida pra uma tabela nova. |
| "..." da cópia → "Excluir": "Excluir Tabela de Preços", com "Esta ação não pode ser desfeita e todos os preços desta tabela serão perdidos."; clique em "Excluir": aviso "Tabela de preço excluída!". | Como era só um exemplo, eu excluo a cópia. Uma dica: excluir tabela não tem volta, e a principal nunca pode ser excluída. |
| "..." da "Tabela Depósitos" → "Fixar para meus pedidos e tickets": aviso "Tabela fixada para seus novos pedidos e tickets"; o alfinete aparece ao lado do nome. [ZOOM: o alfinete] | Agora, o Fixar. Ele vale só pro seu usuário: os seus pedidos e tickets novos passam a abrir nessa tabela, e os dos colegas continuam como estavam. |
| [ILUSTRAÇÃO: qual tabela o pedido abre: três degraus que acendem um por vez, "1. Tabela do cliente ou fornecedor", "2. A tabela que você fixou", "3. Principal da empresa".] | A ordem é esta: se o cliente ou fornecedor tem tabela no cadastro, vale a dele. Senão, a que você fixou. E se não fixou nenhuma, a principal. |
| "..." → "Remover minha tabela fixada": aviso "Tabela pessoal removida; você voltará a usar a principal da empresa". | O Rafael trabalha na principal, então eu removo. |
| "..." → "Definir como principal da empresa": abre "Definir “Tabela Depósitos” como principal?". [ZOOM: o texto da janela] Clique em "Cancelar". | Por último, Definir como principal da empresa. Os preços dessa tabela viram a base de tudo, a principal antiga fica guardada como independente e as vinculadas são recalculadas. É uma troca grande, pra quando a empresa muda a política de preço. Aqui eu só mostro e cancelo. |

Fala: ~215 palavras, ~83 s.

### 3.2 Trecho no cap06 (depois de "Salvar") · venda abaixo da compra

| Tela | Fala |
| --- | --- |
| Reabre "Editar Tabela", busca "bronze"; em "Venda (R$)" digita um valor menor que a compra; "Salvar": abre "Preço de venda abaixo do custo", com "Salvar mesmo assim". Clique em "Cancelar" e fecha sem salvar. | Uma dica: se o preço de venda ficar menor que o de compra, o sistema avisa antes de salvar, porque isso é prejuízo naquele material. Normalmente é erro de digitação; se for de propósito, é só confirmar em Salvar mesmo assim. |

Fala: ~42 palavras, ~16 s. Reverte a decisão 1 do `plano.md` (que tirou o assunto por a fonte falar em bloqueio; o código pede confirmação).

### 3.3 Trecho no cap07 (depois de criar a "Tabela Depósitos", antes de ir ao fornecedor) · o cadeado

| Tela | Fala |
| --- | --- |
| Com a "Tabela Depósitos" selecionada, "Editar Tabela": a grade mostra a coluna "Variação" e um cadeado fechado em cada linha. [ZOOM: a linha "Fio de cobre encapado"] Clique no cadeado (abre), troca a variação para 2; a compra recalcula. Clique em "Cancelar". | E se um material fugir da regra? No Editar Tabela, cada linha da vinculada tem um cadeado. Fechado, o material segue os quatro por cento. Abrindo, você põe uma variação só dele, em porcentagem ou em reais, e os outros continuam na regra. |
| A câmera volta à janela "Nova Tabela de Preços" (corte curto do trecho anterior, parado em "Tipo de variação" e "Direção da variação"). | Na criação também dá pra variar em reais em vez de porcentagem, pra baixo em vez de pra cima, ou não vincular: aí é uma tabela independente, com os preços digitados um a um. |

Fala: ~80 palavras, ~31 s.

### 3.4 Frases a acrescentar em capítulos que já existem

| Onde | Tela | Fala |
| --- | --- | --- |
| cap01, na linha da "Lista de Materiais" | Clique no título "Estoque Atual": a lista ordena do maior para o menor; clique de novo em "Código". | Clicando no título de uma coluna, a lista ordena por ela. |
| cap01, na coluna "Tabelas de Preço" | Cursor no "?" "Como funciona", sem abrir. | (acrescentar à fala existente) O botão de interrogação explica os tipos de tabela. |
| cap07, abertura | (mesma tela) | (acrescentar) Se essa coluna não aparece pra você, ligue Múltiplas Tabelas de Preço em Configurações, Usabilidade. |
| cap07, fim (depois do bronze) | (mesma tela da compra) | E se você trocar a tabela com itens já lançados, o sistema pergunta se atualiza os preços desses itens ou se vale só pros próximos. Isso a gente vê no tutorial de compra e venda. |
| cap10 (Excluir) | Marca as caixinhas de dois materiais: sobe a barra com "Transferir Estoque", "Definir prefixo" e excluir; desmarca. | Marcando as caixinhas, aparece uma barra pra agir em vários materiais de uma vez: transferir, definir prefixo ou excluir. |
| Recapitulando | Montagem do cap08 novo. | (acrescentar) E viu o menu da tabela: duplicar, fixar pro seu usuário e trocar a principal. |

Fala: ~110 palavras, ~42 s.

### 3.5 Trecho opcional no cap03 · Prefixo (depende de decisão)

| Tela | Fala |
| --- | --- |
| No "Editar Material", ao lado de "Código": em "Prefixo" digita "P"; a linha passa a "Fica assim: P70". [ZOOM: "Fica assim:"] Apaga o "P" antes de "Atualizar". | Do lado do código tem o Prefixo. É uma letra que vai na frente do número, na tela, no comprovante e na nota. Tem pátio que usa pra separar famílias, como P de plástico. Aqui a Recicla Vale não usa, então eu deixo vazio. |

Fala: ~47 palavras, ~18 s.

### O que o mundo fictício precisa para gravar

- Handlers RPC novos no backend falso: `duplicate_price_table` (devolve o id; cria "Tabela Depósitos (cópia)" com
  `is_linked` falso e os itens com o preço efetivo), `set_my_preferred_price_table` (devolve o id ou `null`) e a coluna
  `profiles.preferred_price_table_id` na leitura do perfil (`null` em todos os usuários do mundo base).
  `promote_price_table_to_default` **não** precisa: a aula cancela.
- `DELETE price_tables` da cópia e `UPDATE price_tables` já devem existir (o "Excluir" e o "Configurações" são do 1.59.154);
  conferir no `rec/t03_estado.py`.
- Trecho 3.3: `price_table_items` da "Tabela Depósitos" com `is_override` falso; nada é salvo.
- Trecho 3.2: nenhum dado novo (cancela antes de gravar).
- Semente nova `apos-cap08` igual à `apos-cap07` (o capítulo desfaz tudo). Nenhum nome ou número novo no `MUNDO_FICTICIO.md`.
- Ilustração nova: "qual tabela o pedido abre" (três degraus), irmã da escada do cap07; cuidar para as duas não se
  confundirem (uma é da tabela, a outra é do preço).

## 4. Estimativa

| Item | Fala a mais |
| --- | --- |
| 3.1 cap08 novo (menu da tabela) | ~83 s |
| 3.2 venda abaixo da compra | ~16 s |
| 3.3 cadeado e tipos de tabela | ~31 s |
| 3.4 frases soltas | ~42 s |
| 3.5 Prefixo (se aprovado) | ~18 s |
| **Total** | **~172 s sem o Prefixo, ~190 s com** |

**1 capítulo novo** (12 vinhetas no lugar de 11). A aula vai de ~14 min para ~17 min de vídeo. Regravar: cap01, cap03 (se
Prefixo), cap06, cap07, cap08 novo, cap10 e o recap; caps. 2, 4, 5, 8 e 9 atuais ficam como estão.

**Depende de decisão do Kaik:** (a) incluir o Prefixo (o plano tirou de propósito); (b) reverter a decisão 1 do plano e
falar da venda abaixo da compra; (c) "Definir como principal da empresa" só mostrado e cancelado, como proposto, ou
executado num mundo descartável.

## 5. O que o pedido listou e é da tela de Venda (não é desta aula)

Nada disto está roteirizado aqui. `pages/Sale.tsx` mudou 667 linhas entre as versões e pede auditoria própria com Tnn = T07.

| Item pedido | Onde mora | O que já dá para adiantar |
| --- | --- | --- |
| Tabela de preço na venda | T7 (regra explicada na T3) | Mesma ordem nova da mudança 5 (`pages/Sale.tsx:932`, `:1567`, `:1583`) e a janela "Trocar tabela de preços?" (`pages/Sale.tsx:6775`) |
| Venda abaixo do custo | T3 no cadastro (F7); na venda, T7 | Em `pages/Sale.tsx` do 1.60.10 não há aviso com o texto "abaixo do custo": conferir na auditoria da T7 antes de prometer |
| Pesagem, descontos, formas de recebimento, fiado e saldo do cliente, frete, comprovante | T7 (saldo também T4 e T13; balança T5) | Não lido aqui |
| Edição em caixa fechado (1.60.2) | T9 (e T7) | Textos novos em `pages/Sale.tsx:4947` ("Escolha em qual caixa aberto lançar a edição."), `:5112` ("Sem movimento em dinheiro: você pode manter o caixa original sem alterar o fechamento.") e `:5114` ("O caixa original está fechado. Como houve movimento em dinheiro, escolha um caixa aberto.") |
| NF-e a partir do pedido | T16, com ponte na T7 | Não lido aqui |
