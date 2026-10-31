# Inventário delta · T3 v2 (Dominex 1.38.9)

Levantamento de 31/10/2026 para a nova versão do T3 ("Clientes, Fornecedores e Equipamentos"). Base do T3 gravado: 1.37.56 (`exemplos/dominex-t3/inventario.md:4`).
Código lido: 1.38.9 (`src/config/version.ts:1`), com a 1.38.6 como comparação. Tudo só leitura.

**Como ler as citações** (formato `arquivo:linha`; um `:N` solto vale para o último arquivo citado antes dele):

- `src/...` e `supabase/...`: fonte da 1.38.9 (`$TUT_HOME/src-1.38.9`).
- `v1.38.6/src/...`: a mesma árvore na 1.38.6 (`$TUT_HOME/src-1.38.6`), quando o texto compara antes e depois.
- `rec/t3/`: robôs gravados do T3 (`$TUT_HOME/rec/t3`), um arquivo por capítulo. `rec/fakebase/...`: o Supabase falso (`$TUT_HOME/rec/fakebase`).
- `exemplos/...`, `docs/...`, `ferramentas/...`, `perfis/...`, `planejamento/...`: este repositório.
- `CLAUDE.md:N` é o `CLAUDE.md` da fonte 1.38.9. O app de gravação (`$TUT_HOME/app`) está na 1.38.6 (`version.ts:1` dele).

## 1. Resumo

### 1.1 O que muda em cada capítulo (v2 ← T3)

| v2 (T3) | O que muda na tela | O que o backend falso precisa | O que quebra nos robôs |
| --- | --- | --- | --- |
| 00 (00) | Nada. | Nada. | Nada. |
| 01 (01) | O botão "Configurar origens" virou "Configurações" (`src/components/customers/CustomersPageChrome.tsx:60-63`). O botão "Filtros" aparece ao lado da busca da lista para todo mundo, antes só com o módulo PDV (`src/pages/Customers.tsx:465`; `v1.38.6/src/pages/Customers.tsx:444`). Linhas ganham selo de etiqueta quando houver. | Esquema novo (ver seção 8). | `rec/t3/cap01.json:43` (passa o mouse no botão antigo). |
| 02, 03 (02, 03) | A janela "Novo Cliente" ganhou "Etiquetas" e, havendo campos, "Campos personalizados", no fim da aba Contato, antes de "Observações" (`src/components/customers/CustomerFormDialog.tsx:621-626`). "Criar" fica desabilitado enquanto as etiquetas carregam (`:381`). | RPC `set_customer_labels`, chamada em **todo** salvamento (`:347`). | Nada quebra; regravar para a janela nova aparecer. |
| 04 (04) | O botão abre o modal único "Configurações de clientes e fornecedores", na seção "Origens" (`src/components/customers/CustomerSettingsDialog.tsx:73-90`). | Nada além do esquema. | `rec/t3/cap04.json:18-19` (clique e espera em "Origens de Clientes"). |
| 05 (05) | "Editar" e "Excluir" saíram do cabeçalho e foram para o menu "Ações" (`src/pages/CustomerDetail.tsx:761-797`), desde a 1.38.6. | Nada. | `rec/t3/cap05.json:24-25` (passa o mouse nos botões visíveis). |
| 06 (novo) | Seção "Etiquetas" das Configurações; "Etiquetas" no formulário; selos na ficha e na lista; "Filtros" por etiqueta. | Tabelas `party_labels` e de vínculos, RPC `set_customer_labels`, etiqueta "Preferencial" por seed. | Robô novo. |
| 07 (novo) | Seção "Campos personalizados" (clientes e fornecedores); campo no formulário; linha no cartão "Informações". | Tabela `party_field_config`, coluna `customers.custom_fields`. | Robô novo. |
| 08 (06) | Sem mudança de fluxo (os botões do topo aparecem atrás). | Nada. | Nada. |
| 09 (07) | "Etiquetas" é o 2º campo do formulário de fornecedor, logo abaixo de "Nome" (`src/components/inventory/SupplierFormDialog.tsx:132-135`); selo na lista. Ficha do fornecedor **mantém** "Editar" e "Excluir" visíveis (`src/components/customers/SuppliersTab.tsx:227-243`). | RPC `set_supplier_labels`, em todo salvamento (`src/components/inventory/SupplierFormDialog.tsx:103`). | Acrescentar o passo de etiqueta. |
| 10 (08) | "Configurar Campos" abre agora "Configurações de equipamentos", com Categorias, Etiquetas e Campos personalizados (`src/components/customers/EquipmentSettingsDialog.tsx:16-20`); a aba "Categorias" da página sumiu; a coluna "Portal" é nova. | `equipment_field_config.is_visible_in_portal`, `party_labels` com escopo `equipment`. | `rec/t3/cap08.json:31-33,68,73-77` (os passos de campos continuam valendo, ver seção 9). |
| 11 (09) | O formulário ganhou "Etiquetas" logo abaixo de "Categoria" (`src/components/customers/EquipmentFormDialog.tsx:381-418`); o seletor de cliente mostra as etiquetas do cliente (`src/components/customers/CustomerSelectField.tsx:98-99`). | RPC `set_equipment_labels`, em todo salvamento (`src/components/customers/EquipmentFormDialog.tsx:248`). | `rec/t3/cap09.json:12-15` (abas da página que não existem mais). |
| 12 (10) | Ficha do equipamento com "Ações" e etiquetas sob o nome (`src/pages/EquipmentDetail.tsx:487-506`); "Gerar Etiqueta" segue separado (`:581`). | Nada além do esquema. | Nada quebra; regravar é recomendado. |
| 13 (11) | Recapitulando cita etiquetas e o campo novo. | Nada. | `rec/t3/cap11.json:23,41,43-47`. |

### 1.2 Respostas diretas ao pedido do Kaik

- **Ações:** a ficha do **cliente** (1.38.6, `5f0b64ea`) e a do **equipamento** (1.38.6) têm um menu "Ações" com Editar e Excluir (cliente também: Copiar link do portal, Abrir portal, Criar oportunidade no CRM, conforme o caso). A ficha do **fornecedor não mudou**: continua com "Editar" e "Excluir" visíveis.
- **Configurações:** um modal único por área. Clientes e fornecedores: "Configurações de clientes e fornecedores" com **Origens**, **Etiquetas** e **Campos personalizados**. Equipamentos: "Configurações de equipamentos" com **Categorias**, **Etiquetas** e **Campos personalizados**.
- **Onde foi parar a configuração de campos do equipamento:** o botão da página continua "Configurar Campos", mas agora abre "Configurações de equipamentos"; a antiga janela de campos virou a seção "Campos personalizados" desse modal e as categorias (antes uma aba da página) viraram a seção "Categorias" (seção 4.1).
- **Etiquetas:** várias por cadastro, com cor, "Mostrar nos portais" e "Etiqueta ativa"; aparecem nas listas, fichas, formulários, filtros e seletores de outros módulos (seções 3.4 e 5).
- **Campos personalizados:** cinco tipos (Texto, Número, Data, Lista de opções, Sim/Não), obrigatório, visível e, só para clientes, "Mostrar no Portal do Cliente" (seção 3.5).
- **Voz:** 1.824 créditos (`voz_nova.md`).

## 2. Linha do tempo (1.37.56 até 1.38.9)

| Versão | Commit | Quando | O que mudou para o usuário |
| --- | --- | --- | --- |
| 1.37.56 | (base do T3 gravado) | 29 e 30/10 | Fichas com "Editar" e "Excluir" visíveis; "Configurar origens"; aba "Categorias" na página de equipamentos. |
| 1.38.5 | `8de8b559` | 30/10 12:32 | Autorização do WhatsApp preservada ao digitar o celular; CPF, CNPJ, telefone e CEP formatados; mensagens de equipamento no idioma; busca tolerante a acento (`src/pages/Changelog.tsx:107-128`). |
| 1.38.6 | `5f0b64ea` | 30/10 19:10 | "Editar e excluir reunidos em Ações" nas fichas de cliente e equipamento (`src/pages/Changelog.tsx:96-106`). |
| 1.38.7 | `9ea75597` | 30/10 22:54 | Painel admin (sem efeito no T3) (`src/pages/Changelog.tsx:84-95`). |
| 1.38.8 | `0b35ea72` | 31/10 12:40 | Etiquetas e campos personalizados de clientes e fornecedores; modal "Configurações" (`src/pages/Changelog.tsx:67-82`). |
| (sem versão) | `2295ff0f` | 31/10 12:44 | Correção: permitir excluir etiquetas. |
| 1.38.9 | `7690807a` | 31/10 13:27 | Várias etiquetas por cadastro, equipamentos, filtros, seletores, configurações reunidas, portais (`src/pages/Changelog.tsx:45-64`). |

Nota de versão do pop-up: "Clientes, fornecedores e equipamentos agora podem receber várias etiquetas, com filtros, identificação nos seletores e configurações reunidas." (`src/config/version.ts:3-4`).

Dois deltas para o T3: **A** (1.37.56 até 1.38.6) e **B** (1.38.6 até 1.38.9). O T3 foi gravado antes do A; a árvore comparada aqui é a 1.38.6, a mesma do app de gravação e do esquema do backend falso (seção 8).

## 3. Clientes e fornecedores

### 3.1 Botões da página (`src/components/customers/CustomersPageChrome.tsx`)

- Aba **Clientes:** "Configurações" (ícone de ajustes, contorno) `:60-63`; "Formulários de captação" `:64-67`; "Novo Cliente" (primário; só com permissão de criar) `:68-73`.
- Aba **Fornecedores:** só "Configurações" `:60-63`. O "Novo Fornecedor" fica no topo da coluna de detalhe, alinhado à direita (`src/components/customers/SuppliersTab.tsx:194-201`).
- "Configurações" não tem guarda de permissão (qualquer usuário vê o botão; ver achado 2). No celular as ações vivem na barra da lista (`src/components/customers/CustomersPageChrome.tsx:46-47`).
- 1.38.6: o botão se chamava "Configurar origens" (`v1.38.6/src/components/customers/CustomersPageChrome.tsx:60-62`) e abria a janela "Origens de Clientes" (`:99`).

### 3.2 Modal "Configurações de clientes e fornecedores" (`src/components/customers/CustomerSettingsDialog.tsx`)

- Título "Configurações de clientes e fornecedores", janela larga (`sm:max-w-4xl`) `:77`. Menu à esquerda (no celular vira uma barra horizontal) e conteúdo à direita `:78-90`.
- Menu `:80-84` (rótulo / legenda): **Origens** / "Canais de aquisição" (abre nesta, `:74`); **Etiquetas** / "Cores e classificações"; **Campos personalizados** / "Informações adicionais".
- Seção **Origens** (`src/components/customers/CustomerSettingsDialog.tsx:87`): título "Origens", texto "Gerencie os canais usados para identificar a origem dos clientes." e o conteúdo da antiga janela (`src/components/customers/CustomerOriginManagerDialog.tsx:20`): lista de origens com menu Editar/Excluir por linha, campo "Nova origem...", seletor de ícone, seletor de cor e botão "Adicionar" (`:140-146`; textos em `src/lib/i18n/messages/app/equipment.ts:330-346`); aviso "Origem criada!" (`src/hooks/useCustomerOrigins.ts:79`). A janela antiga continua existindo para o cartão "Origens" das Configurações da empresa (`src/pages/Settings.tsx:46,1953`), então o **T1 não muda**.
- Seção **Etiquetas** (`src/components/customers/CustomerSettingsDialog.tsx:88`): `PartyLabelsManager` com escopo `party` (3.3).
- Seção **Campos personalizados** (`src/components/customers/CustomerSettingsDialog.tsx:89`): alternância "Clientes" | "Fornecedores" e o gerenciador de campos (3.5).

### 3.3 Etiquetas (`src/components/customers/PartyLabelsManager.tsx`)

- Cabeçalho `:42`: título "Etiquetas", texto "Classifique clientes e fornecedores com cores fáceis de reconhecer." (para equipamentos, "equipamentos" no lugar, `:39`) e botão "Nova etiqueta".
- Formulário (aparece em "Nova etiqueta" ou "Editar") `:43-49`:
  - "Nome da etiqueta", marcador "Ex.: BLOQUEADO" `:44`.
  - "Cor saturada": seletor de cor e uma prévia do selo, que mostra o nome digitado ou "ETIQUETA" `:45,38`. Cor inicial vermelha `#DC2626` `:17,21`.
  - Interruptor "Mostrar nos portais" com o texto "Libera esta classificação para o cliente." `:46` (padrão desligado).
  - Ao editar: interruptor "Etiqueta ativa" `:47` (inativa some dos seletores e filtros) e botão "Excluir" (confirmação do navegador "Excluir a etiqueta “X”? Ela será removida dos cadastros vinculados.", `:34`).
  - Botões "Cancelar" e "Salvar etiqueta" `:48`.
- Lista abaixo `:50`: selo colorido, olho cortado se inativa, botão "Editar" e lixeira ("Excluir etiqueta"); vazio: "Nenhuma etiqueta cadastrada."
- Seletor de cor (`src/components/ui/ColorPicker.tsx`): botão com a cor atual `:146-158`; painel com campo hexadecimal (`#000000`) `:213`, "Conta-gotas" `:222` e 19 cores prontas `:8-14`, cada uma com `title` igual ao hexadecimal (`:248`), por exemplo `#F97316` (laranja), `#3B82F6` (azul), `#22C55E` (verde).
- Aviso "Etiqueta criada!" (`src/hooks/usePartyLabels.ts:77`). Depois de "Salvar etiqueta" o formulário **continua aberto** em modo de edição, com a etiqueta selecionada (`src/components/customers/PartyLabelsManager.tsx:28-31`): o robô precisa clicar em "Cancelar".
- Escopos `party`, `equipment` e `all` (`src/hooks/usePartyLabels.ts:8`): clientes e fornecedores **compartilham** a mesma lista (`party`); equipamentos têm outra (`equipment`), na mesma tela (`src/components/customers/EquipmentSettingsDialog.tsx:59`); `all` existe no banco mas a tela não cria.
- Regras do banco: cor no formato `#RRGGBB` (`supabase/migrations/20261031120000_party_labels_and_custom_fields.sql:22`); nome de 1 a 60 caracteres (`:21`); nome único por empresa e escopo, sem diferenciar maiúsculas (`supabase/migrations/20261031193000_party_multi_labels.sql:15-17`).
- Quem pode: ver, qualquer usuário da empresa; criar, editar e excluir, só quem tem `can_manage_system` (`supabase/migrations/20261031120000_party_labels_and_custom_fields.sql:227-250`).

### 3.4 Onde as etiquetas de clientes e fornecedores aparecem

| Lugar | Como aparece | Citação |
| --- | --- | --- |
| Formulário "Novo/Editar Cliente" | Campo "Etiquetas" (marcador "Sem etiquetas"); ao abrir: "Selecione uma ou mais etiquetas", cada opção com a cor e um visto, e "Limpar etiquetas". Só entram etiquetas ativas (ou já marcadas). | `src/components/customers/CustomerFormDialog.tsx:149,621-624`; `src/components/customers/PartyLabelMultiSelect.tsx:27-46` |
| Formulário de fornecedor | "Etiquetas" é o 2º campo, abaixo de "Nome". | `src/components/inventory/SupplierFormDialog.tsx:132-135` |
| Lista de clientes (computador) | Primeira etiqueta e "+N" com o nome completo no tooltip, ao lado do selo PJ/PF. | `src/pages/Customers.tsx:456-461`; `src/components/customers/PartyLabelBadge.tsx:48-94` |
| Cartões (modo grade) | Todos os selos no computador; no celular, só o primeiro e "+N". | `src/pages/Customers.tsx:197` |
| Lista de clientes (celular) | Bandeirola colorida pequena (modo compacto); o nome da etiqueta aparece ao tocar ou passar o mouse. | `src/pages/Customers.tsx:667`; `src/components/customers/PartyLabelBadge.tsx:16-33` |
| Filtros da lista de clientes | Botão "Filtros" com o grupo "Etiquetas" (várias marcáveis; mostra quem tem **qualquer** uma). "Atende como" só com PDV. Painel lateral direito com "Limpar tudo" (só com filtro ativo); o botão do rodapé diz "Aplicar (N)" com filtro marcado e "Fechar" sem nenhum. | `src/pages/Customers.tsx:308,364-373`; `src/components/ui/FilterButton.tsx:27,117,154-156`; `src/lib/i18n/messages/app/common.ts:29,105` |
| Ficha do cliente | Selos cheios sob o nome, antes do selo PJ/PF; linha "Etiquetas" no cartão "Informações"; o seletor de "trocar de cliente" mostra o resumo. | `src/pages/CustomerDetail.tsx:321,736,749-752,850-851` |
| Lista de fornecedores | Resumo na linha; filtro "Etiquetas" embutido na lista. | `src/components/customers/SuppliersTab.tsx:81-88,181,185` |
| Ficha do fornecedor | Selos cheios. | `src/components/customers/SupplierDetailDialog.tsx:74` |

O vínculo guarda a ordem: a primeira etiqueta marcada vira a etiqueta principal e espelha na coluna antiga `label_id` (`src/components/customers/CustomerFormDialog.tsx:317`).

### 3.5 Campos personalizados de clientes e fornecedores (`src/components/customers/CustomerSettingsDialog.tsx`)

- Cabeçalho `:54`: "Campos de clientes" ou "Campos de fornecedores", texto "Crie informações adicionais para cadastro, ficha e portal." e botão "Novo campo".
- Formulário `:55-67`:
  - "Nome do campo" `:57`.
  - "Tipo" `:58`: Texto, Número, Data, Lista de opções, Sim/Não (`:16-19`).
  - Se Lista de opções: "Opções, separadas por vírgula", marcador "Ativo, Inativo, Em análise" `:59`.
  - Interruptores "Visível" (padrão ligado) `:61`, "Obrigatório" `:62` e, **só para clientes**, "Mostrar no Portal do Cliente" (padrão desligado) `:63`. Para fornecedores o portal é sempre falso: o banco proíbe (`supabase/migrations/20261031120000_party_labels_and_custom_fields.sql:58-59`) e a tela força (`src/components/customers/CustomerSettingsDialog.tsx:40`).
  - Botões "Excluir" (só ao editar, **sem confirmação**), "Cancelar" e "Salvar campo" `:65`.
- Lista `:68`: nome do campo, olho (visível) ou olho cortado, botão "Editar"; vazio "Nenhum campo personalizado."
- Avisos "Campo criado!" e "Campo removido!" (`src/hooks/usePartyFieldConfig.ts:63,96`). A chave interna é `custom_<milissegundos>` e a posição é a quantidade atual (`src/components/customers/CustomerSettingsDialog.tsx:47`). Como nas etiquetas, o formulário continua aberto depois de salvar (`:47-49`).
- Onde o campo aparece:
  - Formulário de cliente, bloco "Campos personalizados" ao fim da aba Contato, antes de "Observações": rótulo com " *" se obrigatório; entrada de texto ou número, "Selecione..." para lista, caixa "Sim" para Sim/Não, seletor de data (`src/components/customers/PartyFieldsForm.tsx:21-48`; `src/components/customers/CustomerFormDialog.tsx:625`). O bloco some se não houver campo visível (`src/components/customers/PartyFieldsForm.tsx:14-16`).
  - Obrigatórios só são checados no navegador: aviso "Campos obrigatórios / Preencha os campos personalizados obrigatórios." (`src/components/customers/CustomerFormDialog.tsx:270-276`).
  - Ficha do cliente: linhas no cartão "Informações", só campos visíveis e preenchidos (`src/pages/CustomerDetail.tsx:852-855`); valores formatados por `formatPartyFieldValue` (`src/hooks/usePartyFieldConfig.ts:111`).
  - Formulário do fornecedor (`src/components/inventory/SupplierFormDialog.tsx:160`) e ficha do fornecedor (`src/components/customers/SupplierDetailDialog.tsx:106-109`).
  - Portal do Cliente: só os marcados "Mostrar no Portal do Cliente" (`supabase/migrations/20261031120000_party_labels_and_custom_fields.sql:340-364`; tela `src/pages/CustomerPortal.tsx:1417-1419`).

### 3.6 Fichas e o menu "Ações"

- **Cliente** (`src/pages/CustomerDetail.tsx:761-797`): menu "Ações" ao lado do nome, com borda e texto (`triggerClassName`). Itens: Copiar link do portal e Abrir portal (escondidos se não houver portal), Criar oportunidade no CRM (só com CRM), **Editar**, **Excluir**. O comentário `:759-760` explica a decisão (espaço para o nome).
- **Equipamento** (`src/pages/EquipmentDetail.tsx:498-506`; na 1.38.6, `v1.38.6/src/pages/EquipmentDetail.tsx:492-500`): "Ações" com **Editar** e **Excluir**. Etiquetas sob o nome (`src/pages/EquipmentDetail.tsx:487`).
- **Fornecedor** (`src/components/customers/SuppliersTab.tsx:227-243`): `Editar` e `Excluir` continuam em botões visíveis, e o comentário da linha 227 ("Mesma régua da ficha de cliente") ficou desatualizado.

## 4. Equipamentos

### 4.1 Onde foi parar a configuração de campos (as ~190 linhas de `Equipment.tsx`)

- 1.38.6: `v1.38.6/src/pages/Equipment.tsx` tinha 196 linhas: duas abas na página (Equipamentos e Categorias, `:22,29-30`) e o painel de categorias escrito dentro dela (`:37-131`). O botão "Configurar Campos" ficava no cabeçalho e abria a janela de campos (`v1.38.6/src/components/customers/EquipmentPageChrome.tsx:57-59,96`).
- 1.38.9: `src/pages/Equipment.tsx` tem 11 linhas, só o cabeçalho e o painel, **sem abas**. O botão "Configurar Campos" (`src/components/customers/EquipmentPageChrome.tsx:49-52`) abre `EquipmentSettingsDialog` (`:77`), e as duas coisas viraram seções dele (`src/components/customers/EquipmentSettingsDialog.tsx:58-60`): Categorias (`EquipmentCategoryManagerDialog` embutido), Etiquetas (`PartyLabelsManager` com escopo `equipment`) e Campos personalizados (`EquipmentFieldConfigDialog` embutido).
- O subtítulo da página continua "Gerencie equipamentos e categorias" (`src/lib/i18n/messages/app/equipment.ts:11`) e o botão não foi renomeado (`:21`).

### 4.2 Modal "Configurações de equipamentos" (`src/components/customers/EquipmentSettingsDialog.tsx`)

- Título "Configurações de equipamentos", janela `sm:max-w-5xl` `:29-30`. Menu `:16-20` (rótulo / legenda): **Categorias** / "Tipos de equipamento" (abre nesta, `:23`), **Etiquetas** / "Cores e classificações", **Campos personalizados** / "Informações adicionais".
- **Categorias** (`src/components/customers/EquipmentCategoryManagerDialog.tsx:87-107`): lista das categorias e, antes dela, o bloco de adicionar (`:119`) com o campo "Nome da categoria", um seletor de cor nativo ("Cor da categoria") e um botão só com o ícone de mais; textos em `src/lib/i18n/messages/app/equipment.ts:118-119`. **Não há mais o botão "Nova Categoria" nem "Criar".** Enter no campo também cria (`src/components/customers/EquipmentCategoryManagerDialog.tsx:94`). O aviso é "Categoria criada com sucesso!" (`src/hooks/useEquipmentCategories.ts:41`).
- **Etiquetas:** o mesmo gerenciador de 3.3, com o texto "Classifique equipamentos com cores fáceis de reconhecer." Etiquetas de equipamento não se misturam com as de clientes.
- **Campos personalizados** (`src/components/customers/EquipmentFieldConfigDialog.tsx`): a janela de campos de antes, com uma coluna nova **"Portal"** (`:706`) com um interruptor por campo (`:310-317`, "Mostrar campo no portal"), também no menu de cada campo "Mostrar no portal" / "Ocultar do portal" (`:615-619`) e na edição (`:796-802`). Cada mudança grava sozinha (selo "Salvo", `:255,660`). Campo novo nasce **privado** (`is_visible_in_portal: false`, `:482`); os que já existiam foram liberados pela migração para manter o comportamento antigo (`supabase/migrations/20261031194500_equipment_fields_portal_visibility.sql:9-11`). Na ordem das colunas, "Portal" fica entre "Visível" e "Obrigatório" (`src/components/customers/EquipmentFieldConfigDialog.tsx:705-707`).

### 4.3 Etiquetas e filtros de equipamentos

- Formulário de equipamento: "Etiquetas" em largura total, logo abaixo de "Categoria", marcador "Selecione uma ou mais etiquetas" (`src/components/customers/EquipmentFormDialog.tsx:381-418`); as etiquetas são gravadas depois do equipamento (`:245-249`).
- Lista de equipamentos: resumo de etiquetas na linha (`src/components/customers/EquipmentPanel.tsx:405`) e, no "Filtros", um grupo novo **"Etiquetas"** com "Todas as etiquetas" (`:323-333`), ao lado de Categoria e Cliente (o grupo Cliente mostra as etiquetas do cliente e busca por elas, `:311-322`). Filtro por qualquer etiqueta marcada (`:191`).
- Ficha do equipamento: selos sob o nome (`src/pages/EquipmentDetail.tsx:487`) e no seletor de "trocar de equipamento" (`:474`).

## 5. Etiquetas em outros módulos (seletores)

Os seletores de cliente, fornecedor e equipamento mostram o resumo da etiqueta ao lado do nome na lista e uma bandeirola compacta depois de escolhido (`suffix` e `selectedSuffix`, `src/components/ui/SearchableSelect.tsx:26,28,219,261`), e a busca também acha pelo nome da etiqueta (`src/components/customers/CustomerSelectField.tsx:93-96`). Só aparece quando o cadastro tem etiqueta; sem etiquetas semeadas, as telas ficam iguais.

| Módulo | Citação |
| --- | --- |
| Seletor de cliente (todo o app) | `src/components/customers/CustomerSelectField.tsx:98-99` |
| Seletor de fornecedor (financeiro) | `src/components/financial/SupplierSelectField.tsx:58-59` |
| Agenda (cabeçalho e página) | `src/components/schedule/ScheduleHeader.tsx:182-183`; `src/pages/Schedule.tsx:958-959` |
| Ordem de serviço (equipamentos) | `src/components/service-orders/ServiceOrderFormDialog.tsx:1571` |
| Orçamento (distribuição de serviços) | `src/components/quotes/QuoteServiceDistributionDialog.tsx:146` |
| Compras e estoque | `src/components/inventory/CompraDetailView.tsx:162-163`; `src/components/inventory/DirectMaterialPurchaseDialog.tsx:110-111`; `src/components/inventory/MaterialPurchaseReportTab.tsx:277` |
| PDV (compra) | `src/pages/PdvPurchase.tsx:120-121` |
| Contratos | `src/components/contracts/ContractFormDialog.tsx:4755`; `src/components/contracts/ContractEquipmentTab.tsx:298,415`; `src/components/contracts/ContractEnvironmentsTab.tsx:1439` |
| PMOC | `src/components/pmoc/PmocExecutionHistoryView.tsx:163-164` |
| Detalhe do equipamento (diálogo) | `src/components/customers/EquipmentDetailDialog.tsx:375` |

## 6. Portais

- **Portal do Cliente:** etiquetas do cliente só se a etiqueta tem "Mostrar nos portais" e está ativa (`supabase/migrations/20261031195000_customer_portal_equipment_labels.sql:41-52`; tela `src/pages/CustomerPortal.tsx:1459`); campos do cliente só os marcados "Mostrar no Portal do Cliente" (`supabase/migrations/20261031120000_party_labels_and_custom_fields.sql:340-364`; tela `src/pages/CustomerPortal.tsx:1417-1419`); equipamentos: etiquetas liberadas e apenas os campos com a coluna "Portal" ligada (`supabase/migrations/20261031195000_customer_portal_equipment_labels.sql:54-90`; telas `src/pages/CustomerPortal.tsx:1074,1312,1599-1601`).
- **Portal PMOC (compartilhado):** a função de borda filtra campos de equipamento por `is_visible_in_portal` e etiquetas por `show_in_portal` e `is_active` (`supabase/functions/pmoc-portal-share/index.ts:1301,1315-1322,1356`); telas em `src/pages/public/PmocPublicPortal.tsx:1393,1512` e tipo em `src/types/pmocPortal.ts:274`.
- No modo parcial (link sem senha) o catálogo de campos e as etiquetas **não** vão (`supabase/migrations/20261031120000_party_labels_and_custom_fields.sql:330-335`; `supabase/migrations/20261031195000_customer_portal_equipment_labels.sql:34-36`).

## 7. Banco de dados (resumo)

| Objeto | O que é | Citação |
| --- | --- | --- |
| `party_labels` | Catálogo de etiquetas: nome, cor (padrão `#64748B`), `is_active`, `scope` (`party`, `equipment`, `all`; padrão `party`), `show_in_portal` (padrão falso). | `supabase/migrations/20261031120000_party_labels_and_custom_fields.sql:18-29`; `supabase/migrations/20261031193000_party_multi_labels.sql:6-13` |
| `party_field_config` | Definição de campos de clientes e fornecedores: `entity_type`, `field_key`, `label`, `field_type`, `options` (jsonb), `is_required`, `is_visible`, `is_visible_in_portal`, `position`. Portal só para cliente. | `supabase/migrations/20261031120000_party_labels_and_custom_fields.sql:43-59` |
| `customers.custom_fields`, `suppliers.custom_fields` | jsonb objeto, padrão `{}`. | `supabase/migrations/20261031120000_party_labels_and_custom_fields.sql:129,133,157-166` |
| `customers.label_id`, `suppliers.label_id` | Etiqueta principal (espelho da primeira), FK com `ON DELETE SET NULL`. | `supabase/migrations/20261031120000_party_labels_and_custom_fields.sql:142,150` |
| `customer_label_assignments`, `supplier_label_assignments`, `equipment_label_assignments` | Vínculos com posição; `ON DELETE CASCADE`; migrados do `label_id` antigo. | `supabase/migrations/20261031193000_party_multi_labels.sql:45-78,120-126` |
| `set_customer_labels`, `set_supplier_labels`, `set_equipment_labels` | RPC `SECURITY DEFINER`: conferem empresa e escopo, apagam o que saiu, regravam a posição e (cliente e fornecedor) atualizam `label_id`. | `supabase/migrations/20261031193000_party_multi_labels.sql:154-256` |
| `equipment_field_config.is_visible_in_portal` | Padrão falso; migração copiou `is_visible` nos campos existentes. | `supabase/migrations/20261031194500_equipment_fields_portal_visibility.sql:9-11` |
| Portal do cliente (função em camadas) | Só campos e etiquetas liberados. | `supabase/migrations/20261031120000_party_labels_and_custom_fields.sql:301-367`; `supabase/migrations/20261031195000_customer_portal_equipment_labels.sql` |

Tipos do app: `src/integrations/supabase/types.ts` (as tabelas e colunas acima aparecem a partir de `customers.custom_fields` `:3939`, `customers.label_id` `:3951`, `party_labels` `:8649`).

## 8. O que o backend falso precisa (`rec/fakebase`)

Verificado por script em `rec/fakebase/schema.json`: **nenhuma** das tabelas, colunas e RPCs abaixo existe. O esquema foi gerado de `app/src/integrations/supabase/types.ts` (chave `_geradoDe`), e o app de gravação (`$TUT_HOME/app`) está na 1.38.6 (`version.ts:1` dele).

1. **Atualizar o app de gravação e regenerar o esquema.** Copiar a 1.38.9 para `$TUT_HOME/app` e rodar `node rec/fakebase/tools/gen-schema.mjs`, que lê `app/src/integrations/supabase/types.ts` e regrava `rec/fakebase/schema.json` (uso em `rec/fakebase/tools/gen-schema.mjs:10-11`). O `app/` e o `schema.json` são **compartilhados por todas as aulas**: fazer com nenhuma gravação rodando, depois rodar `node rec/fakebase/tools/selftest.mjs` (`rec/fakebase/tools/selftest.mjs:1-4`) e conferir um capítulo de outro tema (as colunas novas passam a vir em todo `select=*`). Entram: tabelas `party_labels`, `party_field_config`, `customer_label_assignments`, `supplier_label_assignments`, `equipment_label_assignments`; colunas `customers.custom_fields`, `customers.label_id`, `suppliers.custom_fields`, `suppliers.label_id`, `equipment_field_config.is_visible_in_portal`; RPCs `set_customer_labels`, `set_supplier_labels`, `set_equipment_labels`.
2. **Padrões** em `TABLE_DEFAULTS` (`rec/fakebase/core/defaults.mjs:12-22`): `party_labels` com `scope: 'party'`, `show_in_portal: false`, `color: '#64748B'`, `is_active: true`; `party_field_config` com `field_type: 'text'`, `is_visible: true`, `is_required: false`, `is_visible_in_portal: false`, `position: 0`; `customers` e `suppliers` com `custom_fields: {}`; `equipment_field_config` com `is_visible_in_portal: false`. **Atenção:** a expressão `ALWAYS_TRUE` (`:24`) faz todo booleano `show_*` nascer verdadeiro, o que erra `party_labels.show_in_portal` (no banco é falso).
3. **Três RPC** em `rec/fakebase/handlers/rpc/` (modelo: `rec/fakebase/handlers/rpc/save_customer_portal_settings.mjs`; carregadas em `rec/fakebase/server.mjs:32-35`). Cada uma: confere que o cadastro existe, apaga os vínculos que saíram, grava os da lista com `position` igual ao índice (e `company_id`, que as leituras filtram: `src/hooks/usePartyLabels.ts:50-51`) e, em cliente e fornecedor, atualiza `label_id` com a primeira. Sem handler, o fake responde vazio e **não salva nada** (`rec/fakebase/http/rest.mjs:169-177`), então o cap06 não funciona. Elas são chamadas em todo salvamento de cliente (`src/components/customers/CustomerFormDialog.tsx:347`), fornecedor (`src/components/inventory/SupplierFormDialog.tsx:103`) e equipamento (`src/components/customers/EquipmentFormDialog.tsx:248`).
4. **Gancho novo** `rec/fakebase/hooks/party_labels.mjs` (arquivo a criar; o nome é o da tabela, como em `rec/fakebase/hooks/customers.mjs:1-9`) com `afterDelete(row, hc)`, que o executor já chama (`rec/fakebase/core/mutate.mjs:115-118`): apagar os vínculos da etiqueta e zerar `label_id` onde ela era a principal (o banco faz por cascata e `SET NULL`; o fake não tem cascata). Nenhum gancho atual usa `afterDelete`: testar com um "Excluir" de etiqueta.
5. **Sementes** `rec/fakebase/seeds-extra/t3v2/apos-capNN.json` (cadeia acumulada, um arquivo por capítulo; cada robô usa `"seedExtra": ["t3v2/apos-cap<anterior>"]`, como `rec/t3/cap03.json:9`). Gerar com `rec/fakebase/tools/snapshot-delta.mjs` (`base` antes do cap02; `diff <base> t3v2/apos-capNN` depois de cada capítulo: `rec/fakebase/tools/snapshot-delta.mjs:3-11`). **Atenção:** o `diff` só grava as tabelas de `T3_TABLES` (`rec/fakebase/tools/snapshot-delta.mjs:21-24`) e apenas avisa das demais (`:93`); passar `--tabelas` com as do T3 mais `party_labels,party_field_config,customer_label_assignments,supplier_label_assignments,equipment_label_assignments` (`:13`). O que cada semente carrega de novo: "Preferencial" (laranja `#F97316`, escopo `party`, sem vínculo) já no `apos-cap05` (inserir antes de capturar, é a etiqueta que o cap06 diz que já existe); "Contrato PMOC" (azul `#3B82F6`) e os vínculos do Colégio Monte Verde (cap06); o campo "Horário de acesso" e o valor no colégio (cap07); o vínculo "Preferencial" do fornecedor (cap09); a etiqueta de equipamento "Em garantia" (verde `#22C55E`, escopo `equipment`) (cap10); o vínculo no Hi-Wall (cap11). O T3 usou `apos-cap02` a `apos-cap10` (a lista está em `rec/fakebase/seeds-extra/t3/`); o T3 v2 vai de `apos-cap02` a `apos-cap12` e o cap13 (recapitulação) usa o último.
6. O que acontece sem isso: leitura de tabela fora do esquema devolve lista vazia e escrita cria uma tabela dinâmica em memória, sem padrões (`rec/fakebase/http/rest.mjs:84-90,104-107`); como a tela lê com `.in('scope', [...])` (`src/hooks/usePartyLabels.ts:45`), a etiqueta criada nunca volta para a lista. As RPC sem handler respondem vazio e não gravam. Tudo isso só aparece em `rec/fakebase/desconhecidos.log` (`rec/fakebase/core/log.mjs:1`): conferir o log depois de cada gravação.

## 9. Robôs que quebram e robôs novos

Robôs do T3 em `rec/t3/` (numeração do T3). Os trechos citados abaixo foram conferidos linha a linha.

| Robô do T3 (cap v2) | Linhas | O que mudou na tela | Como ficar |
| --- | --- | --- | --- |
| `cap01.json` (01) | `:43` | O botão agora se chama "Configurações". | Passar o mouse em "Configurações" (`within: 'main'`). |
| `cap04.json` (04) | `:18-19`, `:32-34` | Clique em "Configurar origens" e espera de "Origens de Clientes" não existem mais. O menu Editar/Excluir da linha continua dentro do modal. | Clicar em "Configurações" e esperar "Configurações de clientes e fornecedores"; "Origens" já vem aberta. |
| `cap05.json` (05) | `:24-25` | "Editar" e "Excluir" não estão mais visíveis. | Passar o mouse e clicar em "Ações" (com `unless` para não repetir) e mostrar o menu aberto, ou apenas mostrar o menu. |
| `cap08.json` (10) | `:31-33`, `:60`, `:68`, `:73` | Espera de "Configurar Campos do Equipamento"; a aba "Categorias" e o botão "Nova Categoria" não existem. | Clicar em "Configurar Campos", esperar "Configurações de equipamentos", clicar "Campos personalizados" no menu; categoria pelo campo "Nome da categoria" e o botão de mais. |
| `cap09.json` (11) | `:12-15` | Troca de abas "Categorias" e "Equipamentos" na preparação (sem abas). | Remover a preparação; esperar "Multi Split" direto. |
| `cap11.json` (13) | `:23`, `:41`, `:43-47` | O robô do recap abre os mesmos botões antigos. | Reescrever com os nomes novos. |
| `cap02.json`, `cap03.json` | (já protegem o interruptor do WhatsApp com `when checked:false`) | Janela com "Etiquetas". | Regravar sem mudar passos. |

Robôs novos: **cap06** (Configurações, Etiquetas, Nova etiqueta, preset de cor por `title`, "Salvar etiqueta", "Cancelar"; ficha, Ações, Editar, aba Contato, seção de Etiquetas, popover de várias, "Salvar"; "Filtros" com "Aplicar (N)"/"Fechar") e **cap07** (Configurações, Campos personalizados, "Novo campo", "Salvar campo", "Cancelar"; alternância "Fornecedores"; ficha, Ações, Editar, campo, "Salvar"; cartão "Informações"). O detalhe passo a passo está no `roteiro.md`.

## 10. Impacto em outras aulas

- **T1:** sem mudança (o cartão "Origens" das Configurações da empresa ainda abre a janela antiga: `src/pages/Settings.tsx:46,1953`).
- **T4:** parte do estado final do T3; não mexe em clientes (sem impacto).
- **T5 (agenda):** seletores só mostram etiqueta se houver; sem etiquetas semeadas, igual à gravação na 1.38.6 (`src/components/schedule/ScheduleHeader.tsx:182-183`). Conferir o filtro da agenda na entrega.
- **T8, T9 (compras e estoque):** mesma regra nos seletores de fornecedor (`src/components/inventory/CompraDetailView.tsx:162-163`).
- **T10, T11 (PMOC e contratos):** equipamento com etiqueta aparece nas telas de contrato e histórico (`src/components/contracts/ContractFormDialog.tsx:4755`; `src/components/pmoc/PmocExecutionHistoryView.tsx:163-164`). O T11 usa o Colégio Monte Verde e a categoria "Contratos PMOC", coerentes com a etiqueta "Contrato PMOC" (`planejamento/domiflix/T11/roteiro.md`).
- **T12 (portal do cliente):** campo de equipamento novo nasce privado, então o campo "Tensão" **só aparece no portal se a coluna "Portal" for ligada** (`src/components/customers/EquipmentFieldConfigDialog.tsx:482`). O T12 mostra "campos personalizados visíveis" em Equipamentos (`planejamento/domiflix/T12/inventario.md:165-168`; `planejamento/domiflix/T12/roteiro.md:84-90`): incluir o passo de ligar "Portal" no cap10 deste T3 v2 (sem voz nova, só no vídeo) ou no preparo do T12.

## 11. Achados de segurança e qualidade

| # | Gravidade | Achado | Evidência | Sugestão |
| --- | --- | --- | --- | --- |
| 1 | Média | As três RPC de vínculo são `SECURITY DEFINER` e conferem só empresa e escopo; a tabela de vínculos tem política `FOR ALL` para qualquer usuário da empresa (sem `can_manage_system`) e o espelho `UPDATE customers SET label_id` ignora a RLS de `customers`, que exige assinatura ativa. Um usuário sem permissão de edição, ou com assinatura bloqueada, ainda reetiqueta clientes. | `supabase/migrations/20261031193000_party_multi_labels.sql:128-145,154-187,185`; `supabase/migrations/20261004213000_tenant_subscription_entitlement_rls.sql:94-109` | Exigir a mesma regra de edição do cadastro (ou `tenant_subscription_allows_access`) nas RPC e nas políticas. |
| 2 | Baixa | O botão "Configurações" (clientes) e "Configurar Campos" (equipamentos) aparecem para todos, mas só `can_manage_system` grava etiquetas e campos: os demais veem a janela e recebem erro ao salvar. | `src/components/customers/CustomersPageChrome.tsx:60-63`; `src/components/customers/EquipmentPageChrome.tsx:49-52`; `supabase/migrations/20261031120000_party_labels_and_custom_fields.sql:235-250` | Esconder ou desabilitar o botão sem a permissão (hoje só "Novo Cliente" e "Novo Equipamento" têm guarda). |
| 3 | Baixa | Campo personalizado **obrigatório** só é validado no navegador; o banco só garante que `custom_fields` é um objeto. | `src/components/customers/CustomerFormDialog.tsx:270-276`; `supabase/migrations/20261031120000_party_labels_and_custom_fields.sql:157-166` | Aceitável para campo informativo; documentar. |
| 4 | Baixa | A cobertura de teste do SQL não inclui `show_in_portal` das etiquetas nem a coluna de portal do equipamento. | `supabase/tests/party_labels_custom_fields.sql:124-169,186-191` | Acrescentar casos: etiqueta sem `show_in_portal` não sai; campo de equipamento privado não sai. |
| 5 | Baixa | Campos de equipamento existentes viraram "visíveis no portal" por cópia de `is_visible`; os novos nascem privados. Comportamento coerente, mas muda o resultado de quem criar um campo igual ao que já havia. | `supabase/migrations/20261031194500_equipment_fields_portal_visibility.sql:9-11` | Avisar nas notas ou na tela ("Portal" desligado por padrão). |
| 6 | Baixa | O apagar de campo personalizado não pede confirmação e deixa os valores soltos no `custom_fields` (somem da tela e do portal, mas ficam no banco). Apagar etiqueta usa `window.confirm` do navegador. | `src/components/customers/CustomerSettingsDialog.tsx:65`; `src/components/customers/PartyLabelsManager.tsx:34` | Diálogo do app e limpeza dos valores. |
| 7 | Info | Textos novos escritos direto em português, fora do i18n, contra a regra da casa ("chave de i18n nova nasce nos 4 idiomas"). | `app/CLAUDE.md:110`; `src/components/customers/PartyLabelsManager.tsx:42-48` | Mover para `src/lib/i18n/messages/app/`. |
| 8 | Info | Os formulários de etiqueta e de campo ficam abertos em modo de edição depois de salvar; para fechar é preciso "Cancelar". | `src/components/customers/PartyLabelsManager.tsx:28-31`; `src/components/customers/CustomerSettingsDialog.tsx:47-49` | Fechar o formulário ao salvar (ou documentar). |
| 9 | Info | Nome "Etiquetas" repetido: etiqueta colorida do cadastro e "Gerar Etiqueta" (impressão de QR); na T3 antiga o selo PJ/PF também era chamado de "etiqueta" (resolvido na fala com "selo"). | `src/pages/EquipmentDetail.tsx:581`; `src/components/customers/PartyLabelsManager.tsx:42` | Manter "selo" na aula; considerar "Imprimir QR" no app. |
| 10 | Info | Nomes e textos do app ficaram para trás: botão "Configurar Campos" abre "Configurações de equipamentos"; subtítulo da página ainda "Gerencie equipamentos e categorias"; comentário da ficha de fornecedor cita uma "régua" que mudou. | `src/lib/i18n/messages/app/equipment.ts:10,21`; `src/components/customers/SuppliersTab.tsx:227-229` | Renomear o botão para "Configurações" (a aula então troca uma frase, ver `voz_nova.md`). |
| 11 | Info | Ficha do fornecedor ficou de fora do padrão "Ações". | `src/components/customers/SuppliersTab.tsx:227-243` | Decidir se segue o padrão; a aula só descreve o que existe. |
| 12 | Info | Com busca ou filtro de etiqueta sem resultado, a lista de fornecedores mostra o vazio "nenhum cadastrado" em vez do vazio de busca. | `src/components/customers/SuppliersTab.tsx:214-219` | Usar `t.emptySearch` quando houver filtro. |
| 13 | Fora do escopo | Uma migração da 1.38.7 grava o e-mail de uma pessoa fixo no SQL. | `supabase/migrations/20261030224600_grant_maicon_company_edit_permission.sql:5-9` | Revisar por quem cuida do banco (não afeta a aula). |

## 12. A testar na gravação

1. Cor: clicar no preset pelo `title` do botão (o hexadecimal); conferir a caixa (maiúsculas) de `#F97316`, `#3B82F6`, `#22C55E` na janela de cores.
2. Popover de várias etiquetas: as opções são botões comuns (sem `role="option"`); clicar pelo nome e fechar com Escape ou clique fora. Conferir que "Contrato PMOC" marcada primeiro vira a principal.
3. "Filtros" abre um painel à direita; usar `clicar_fixo` para marcar a etiqueta e fechar em "Aplicar (N)" ou "Fechar".
4. Depois de "Salvar etiqueta" e "Salvar campo" clicar em "Cancelar" para fechar o formulário (ele não fecha sozinho).
5. A janela de "Configurar Campos" abre em **Categorias**; clicar em "Campos personalizados" ao dizer "Em Configurar Campos estão os que já vêm prontos".
6. Campo "Horário de acesso": o valor entra pelo "Editar" da ficha, no bloco "Campos personalizados" ao fim da aba Contato; confirmar a linha no cartão "Informações".
7. Desconexão de nomes: a fala diz "Sim ou Não"; o rótulo na tela é "Sim/Não".
8. Confirmar com o app em execução que **nenhuma** etiqueta aparece no seletor de cliente do cap11 antes do cap06 existir no estado inicial (a cadeia de sementes começa sem vínculos).
