# Inventário funcional · T8 — Estoque, compras e inventário (Dominex)

> Base para o roteiro do tutorial "T8 · Estoque, compras e inventário" da Domiflix. Levantado em 30/10/2026 contra o
> código publicado `APP_VERSION = "1.38.6"` (`src/config/version.ts:1`), cópia em `/home/claude/domiflix/src-1.38.6`.
> **Análise estática, somente leitura**: nada foi executado no app. O que só se confirma rodando está marcado
> "(a confirmar)" e repetido na seção 7. Fontes escritas secundárias: a trilha validada na 1.22.5
> (`_referencia/trilha-de-tutoriais_v1.22.5.md`, T8) e o Guia Técnico do app (`docs/guia-tecnico/secoes/T8.html`, que
> descreve a 1.38.x mas tem uma divergência com o código: seção 0.4). **Onde as fontes e o código divergem, vale o código.**

## Como ler

- Caminhos relativos a `src/`, exceto os que começam com `supabase/`, `docs/` ou `rec/`. Formato `arquivo:linha`.
- Texto entre aspas "assim" é o rótulo exato da tela (pt-br). Fonte principal dos rótulos:
  `lib/i18n/messages/app/inventory.ts` (bloco pt-br, linhas 8-1033). Blocos principais: cabeçalho e abas 8-22, filtros e
  tabela 28-60, Kardex 113, compras 187, compra direta 246, ordem de compra 277, exportar 339, transferir 349,
  configurações 371, locais 400, cadastro do material 413, configurador do local 491, movimento rápido 544,
  fornecedor 567-612, requisição 613, detalhe da requisição 663, cotação 744, inventário 772, posição 896, relatório
  941, NF-e 973.
- "Desktop" = janela de 1024 px ou mais (a tabela larga só aparece a partir de `xl`, 1280 px). "Tenant" = empresa
  cliente (aqui, Glacial Cold Brasil).
- "Local" = local de estoque (tabela `stocks`; a tela também diz "depósito", "almoxarifado" e "van"). "Saldo" = quantidade
  de um material num local (`inventory_stock_levels`). "Kardex" = histórico de movimentações (`inventory_movements`).
- Componentes compartilhados (janelas, abas, toasts) estão no inventário do T3. Fora deste tutorial, mas citados onde
  tocam: Fornecedores na tela Clientes (T3), consumo de estoque dentro da OS (T5/T7), estoque exclusivo do cliente na
  ficha do cliente (T3), PDV e Loja (módulo à parte), Financeiro (T13), NF-e/NFS-e emitidas (T14), orçamento convertido
  em OS (T9).

---

## 0. Resumo para o roteiro

### 0.1 Capítulos da trilha × código de hoje

Trilha: 11 capítulos, ~43 min (`_referencia/trilha-de-tutoriais_v1.22.5.md:329-358`). Veredito: ✅ confere · ⚠️ muda a fala · 🚫 não existe como prometido.

| Cap. | Título na trilha | Hoje (1.38.6) | | Onde |
|---|---|---|---|---|
| 1 | Tela Estoque: as 6 abas | 6 abas com os mesmos nomes (3 encurtam no celular); a aba "Estoque Atual" tem **3** cartões, não 4 (D3) | ✅ | 3.1, 3.2 |
| 2 | Cadastrar material: categoria/grupo, unidade, mínimo e custo | **Não há "Categoria"**, só **Grupo**; mínimo é **por local**; há custo **e** preço de venda, foto, código de barras, "Vendável na loja" (PDV) | ⚠️ | 3.3 |
| 3 | Depósitos/locais: criar, definir o que existe, transferir | "Configurações" (grupos e locais), engrenagem do local (itens/grupos), "Transferir entre locais de estoque" | ✅ | 3.4 a 3.6 |
| 4 | Restrição de acesso por depósito | Aba "Acesso" do local (Aberto/Restrito + pessoas), regra no banco; "Restrito" sem ninguém continua aberto (P3) | ✅ | 2, 3.6 |
| 5 | Kardex | Título "Kardex geral"; colunas diferentes do Guia (D2); local e transferência "Galpão → Van 01" | ✅ | 3.8 |
| 6 | Compras: requisição ou compra direta, fornecedor, financeiro | Requisição + "Registrar compra direta" (só quem administra estoque e financeiro) + janela "Fornecedores" | ✅ | 3.9 |
| 7 | Cotação com vários fornecedores e escolha da vencedora | **Redesenhada (1.28.10)**: cotações por fornecedor, **fornecedor escolhido por material**, **uma O.C. por fornecedor**, "Registrar recebimento" dá a entrada | ⚠️ | 3.9, P6 |
| 8 | Importar XML da NF-e e a compra montada sozinha | Só **dá entrada** (no local principal), cria o fornecedor novo; **não monta compra** nem lança despesa | 🚫 | 3.10, P1 |
| 9 | Inventários: contagem passo a passo e ajuste no fechamento | Assistente de 3 passos, contagem salva ao sair do campo, ajuste "Inventário #N" | ✅ | 3.11 |
| 10 | Posição: saldo numa data passada | Soma o Kardex até a data; valores pelo custo de hoje | ✅ | 3.12 |
| 11 | Relatório: histórico, média paga, projeção, exportação | Igual, mais o painel **"Evolução do preço de compra"** (1.38.0); vendas e lucro seguem desligados (PDV) | ✅ | 3.13 |
| ⚠️ | "Concluir a OS não dá baixa no estoque" | Confere: só com "Consumo de estoque na OS" ligado e materiais anotados | ✅ | 3.14 |

### 0.2 O que mudou desde a 1.22.5 (Changelog, `pages/Changelog.tsx`)

- **1.23.0/1.23.1**: consumo de estoque na OS, "Consumo" no Kardex, excluir material em uso é recusado, Kardex mostra o local, tela melhor no celular (linhas 4540-4602).
- **1.24.36**: Fornecedores ganham aba própria em Clientes (3616). **1.24.42/43**: campos aceitam vírgula; quantidade fracionada (3519, 3502).
- **1.28.10**: **ordem de compra** (fornecedor por material, recebimento parcial, entrada no local da requisição) (2490). **1.28.11**: fornecedor do material vem do cadastro (2478). **1.28.22**: conserta entrada pela nota e ajuste manual (2266).
- **1.30.1**: estoque exclusivo do cliente (2168). **1.36.12**: **compra direta** e **Relatório** com média paga (1467, 1472). **1.36.16**: calendário padrão (1395).
- **1.37.0**: locais "da loja × operacionais" e PDV (1136). **1.37.55**: fotos na lista (171). **1.38.0/1.38.1**: evolução do preço de compra, com fotos (132, 120).
- **Sem mudança desde a 1.22.5** nas abas Kardex (além do local), Inventários e Posição (além do visual, 1.28.2 e 1.36.16).

### 0.3 O que pode surpreender

1. **Estoque Atual vazio na gravação** se a função `get_accessible_inventory_ids` não existir no fakebase (seção 4.3, item 1): é o bloqueio nº 1.
2. A nota fiscal **não vira compra** e entra no local principal; a trilha e o título do capítulo do Guia prometem mais do que o app faz (P1).
3. **Aceitar a cotação não mexe no estoque**; a entrada é o recebimento da O.C. **enviada**, no local escolhido na requisição (3.9).
4. A **média paga** do Relatório só conta compras recebidas por O.C. e compras diretas; entradas rápidas, NF-e e ajustes ficam de fora (3.13).
5. No inventário o **ajuste usa o saldo de agora**, a contagem **grava ao sair do campo** e **cancelar não pede confirmação** (3.11, P8, P10).
6. **Posição e "Valor investido" usam o custo de hoje** do cadastro; nenhuma entrada o atualiza (P11).
7. **O mínimo é por local** e o cartão "Estoque baixo" só olha o local ativo (3.2); sem mínimo não há alerta.
8. As 6 abas **não têm endereço próprio** e as abas de cada tela voltam ao começo ao trocar (3.1).

### 0.4 Divergências do Guia Técnico (`docs/guia-tecnico/secoes/T8.html`)

| # | O Guia diz | O código faz | Vale |
|---|---|---|---|
| D1 | "Categoria" é lista fixa (Peças, Filtros, Gases…) no cadastro (`T8.html:57,70,524-525`) | Não há campo "Categoria"; só **Grupo**. A lista existe nos textos mas nenhuma tela a usa (`inventory.ts:481-489`) | código |
| D2 | Kardex com título "Histórico de Movimentações" e colunas Usuário, Data e Hora, Tipo, Origem, Material, Local, Estoque inicial, Movimento, Estoque final (`T8.html:159-162,187`) | Título "Kardex geral"; colunas **Data e Hora, Tipo, Material e origem, Local, Estoque inicial, Alteração, Estoque final**; autor dentro de "Material e origem" (3.8) | código |
| D3 | "Os quatro indicadores" da aba Estoque Atual, com "Projeção venda (R$)" (`T8.html:34-39`) | **Três** cartões; "Projeção venda" saiu da tela principal na 1.17.25 e hoje só existe na Posição e no Relatório (3.2) | código |
| D4 | Capítulo 8 chama-se "...a compra montada sozinha" (`T8.html:305`); o texto do capítulo descreve só a entrada | Confere com o texto; o título é que promete demais (P1) | código |

O resto do Guia (cotação, O.C., compra direta, inventário, posição, relatório) **confere** com o código.

---

## 1. Rotas e navegação

| Endereço (pt-br) | O que abre | Código |
|---|---|---|
| `/estoque` | Tela "Estoque" (subtítulo "Controle de peças e materiais"), sempre na aba "Estoque Atual". Tradução do endereço: en `/inventory`, es `/inventario`, fr `/stock` | `App.tsx:806`, `lib/i18n/appRouteSlugs.ts:57,138`, `lib/i18n/messages/app/inventory.ts:8-11` |
| (sem endereço próprio) | As 6 abas **não têm URL**: a aba ativa é estado local da página. Só entra em outra aba por clique | `pages/Inventory.tsx:150,1067-1082` |
| `state.inventoryTab` / `state.openNewPurchase` | Um atalho interno (estado de navegação) poderia abrir a aba e já a janela "Nova Requisição de Compra", mas **nenhum outro arquivo envia esse estado hoje**: o botão de compra do PDV vai para `/pdv/compra` (tela do PDV) | `pages/Inventory.tsx:105-107,150-157,1072`, `pages/PdvCaixa.tsx:859`, `lib/i18n/appRouteSlugs.ts:148` |

- **Como se chega:** Menu lateral, grupo "Gestão" > "Estoque" (`components/layout/SidebarMenuContent.tsx:109-118`; o "Operacional" do menu tem só Ordens de Serviço e Mapa), menu
  superior (`components/layout/TopNavbar.tsx:108`), menu "Mais" do celular (`components/layout/MoreMenuDrawer.tsx:104`),
  atalho de teclado **Shift+I** (`hooks/useKeyboardShortcuts.ts:24`). Título da aba do navegador "Estoque"
  (`hooks/usePageTitle.ts:18`); mensagem de carregamento "Calculando estoque..." (`hooks/useRouteLoadingMessage.ts:35`).
- **Seis abas na horizontal, em todas as larguras** (`pages/Inventory.tsx:591-598`): "Estoque Atual", "Histórico de
  Materiais (Kardex)", "Compras de Material", "Inventários", "Posição de Estoque", "Relatório"
  (`lib/i18n/messages/app/inventory.ts:12-22`). No **celular** três nomes encurtam: "Histórico", "Compras", "Posição"
  (`inventory.ts:15,17,20`).
- **Dentro da aba "Estoque Atual"** há uma segunda camada: uma aba por **local** quando a empresa tem mais de um (sublinhadas
  no desktop, pílulas no celular); **não existe aba "Todos"** (seção 3.2; `pages/Inventory.tsx:296-387,692-744`).
- **Telas vizinhas** (não são desta aula, mas aparecem no caminho): **Fornecedores** têm também aba própria na tela
  Clientes (`pages/Customers.tsx:238-251,379`, entrada 1.24.36 do Changelog, `pages/Changelog.tsx:3611`); o **estoque
  exclusivo do cliente** vive na ficha do cliente (`components/customers/CustomerStockTab.tsx`); o **consumo na OS** é
  feito na tela de execução da OS (seção 3.14).
- **Janelas e diálogos da tela** (todos abrem por cima, sem trocar de endereço): cadastro do material, movimento rápido
  (entrada/saída), transferir entre locais, configurações do estoque (grupos e locais), configurador do local (itens e
  acesso), importar XML, exportar (escolha dos materiais), fornecedores e cadastro de fornecedor, requisição de compra,
  cotação, receber O.C., compra direta, novo inventário (assistente), detalhe do inventário
  (`pages/Inventory.tsx:1094-1176`, `components/inventory/*`).

---

## 2. Permissões e módulos

| Quem / o quê | Regra | Código |
|---|---|---|
| Ver o item de menu e abrir `/estoque` | Permissão de tela `screen:inventory` ("Estoque": "Materiais, saldos e movimentações de estoque.", grupo de permissões "Operacional"; no menu lateral fica em "Gestão") | `hooks/usePermissions.ts:67`, `App.tsx:806`, `SidebarMenuContent.tsx:118` |
| Módulo pago | **Nenhum.** `screen:inventory` pertence ao módulo `basic` (todo plano). A rota não usa `ModuleRoute` | `hooks/useCompanyModules.ts:54`, `App.tsx:806` |
| Ação "Gerenciar Estoque" | Chave `fn:manage_inventory` ("Gerenciar materiais e movimentações de estoque", relacionada à tela Estoque). **Na tela de Estoque da empresa nenhum botão checa essa chave**: quem abre a tela cadastra, movimenta, transfere e importa. Ela só vale para (a) a compra direta (junto com `fn:manage_finance`) e (b) o estoque exclusivo do cliente | `hooks/usePermissions.ts:109`, `hooks/useCanRegisterDirectMaterialPurchase.ts:8-15`, `components/customers/CustomerStockTab.tsx:264` |
| **Registrar compra direta** | Só admin/gestor **ou** quem tem as duas chaves `fn:manage_inventory` e `fn:manage_finance` (o botão some para os demais; a RPC repete a regra: erro "Sem permissão para gerenciar estoque e financeiro") | `hooks/useCanRegisterDirectMaterialPurchase.ts:8-15`, `supabase/migrations/20261018005000_compra_direta_estoque_financeiro.sql:190-208` |
| Restrição por local ("Restrito") | Tabela `stock_access`: **zero linhas = local aberto a todos; uma ou mais linhas = só os listados**. `admin`, `gestor` e `super_admin` **sempre** têm acesso. A regra é aplicada **no banco** (RLS em `stocks`, `inventory_stock_levels`, `inventory_movements` e nas RPCs de movimentação/transferência), não só na tela | `supabase/migrations/20260814225028_stock_access_acl.sql:41-65,116-157,181-197,275,366-369` |
| O que a pessoa sem acesso a um local vê | Não vê a aba do local, o saldo, os movimentos daquele local no Kardex, nem a Posição dele; as RPCs recusam movimentar. Para ela o local "não existe" | `hooks/useStocks.ts`, `hooks/useStockAccess.ts`, `pages/Inventory.tsx:296-387`, `supabase/migrations/20260814225028_stock_access_acl.sql:275,366-369` |
| Quem edita o acesso de um local | Quem abre o configurador do local (aba "Acesso"); a RPC `set_stock_access` confere admin/gestor no servidor | `components/inventory/StockConfiguratorDialog.tsx`, `supabase/migrations/20260814225028_stock_access_acl.sql:693-786` |
| Consumo de estoque na OS | Opção da **empresa** (`company_settings.os_stock_consumption_enabled`, vem **desligada**): "Configurações → Usabilidade → Ordens de Serviço → Consumo de estoque na OS". Sem ela, concluir a OS não baixa estoque | `pages/Settings.tsx:663-679,1691`, `hooks/useOsMaterials.ts:169-176`, `lib/i18n/messages/app/settings.ts:229-231` |
| Quem vê o relatório e a posição | Quem abre a tela. A Posição e o Kardex respeitam o acesso por local; o Relatório também filtra os locais acessíveis (`stockIds` do usuário) | `components/inventory/StockPositionTab.tsx`, `hooks/useMaterialPurchaseReport.ts`, `supabase/migrations/20261018005000_compra_direta_estoque_financeiro.sql:669-907` |
| Quem pode fechar inventário / receber O.C. | Qualquer um com acesso à tela e ao local (não há chave própria); as RPCs conferem apenas empresa e acesso ao local | `supabase/migrations/20260930110000_compras_ordem_de_compra.sql`, `supabase/migrations/20260721170000_inventario_e_posicao_de_estoque.sql:206-319` |
| Isolamento entre empresas | Todas as tabelas de estoque têm `company_id` e políticas por empresa; o bucket das fotos é privado, com política por empresa | `supabase/migrations/20260418163700_*.sql:136-140`, `supabase/migrations/20261018162000_pdv_onda1_bucket_fotos_de_produto.sql` |

> **Para o roteiro:** o tutorial pode dizer, sem risco, que "quem tem a tela Estoque liberada usa o dia a dia do estoque; a
> compra direta é de quem administra estoque e financeiro; cada local pode ter acesso restrito". Não dizer que
> "Gerenciar Estoque" é uma trava dos botões da tela (não é; seção 5, P2).

---

## 3. Por tela, janela e aba (rótulos exatos)

### 3.1 Cabeçalho da tela e as 6 abas

- Título **"Estoque"**, subtítulo **"Controle de peças e materiais"** (`pages/Inventory.tsx:659-666`,
  `lib/i18n/messages/app/inventory.ts:8-11`). À direita, sempre visíveis: botão **"Importar XML (NF-e)"** (ícone de envio;
  o texto some abaixo de 1024 px) e botão **"Configurações"** (engrenagem) (`pages/Inventory.tsx:604-625`,
  `inventory.ts:42,44,46-49`).
- Barra de abas sublinhada logo abaixo (`pages/Inventory.tsx:667-682`): **"Estoque Atual"** · **"Histórico de Materiais
  (Kardex)"** · **"Compras de Material"** · **"Inventários"** · **"Posição de Estoque"** · **"Relatório"**
  (`inventory.ts:12-22`). No celular: "Histórico", "Compras" e "Posição".
- A aba aberta ao entrar é sempre **"Estoque Atual"** (`pages/Inventory.tsx:150`). Cada aba só existe enquanto está ativa
  (`pages/Inventory.tsx:686,1068-1082`): Histórico, Compras, Inventários, Posição e Relatório **voltam ao padrão** ao sair e
  voltar (menos as preferências guardadas no navegador do Relatório, seção 3.13); a busca e os filtros do "Estoque Atual"
  moram na própria página e **permanecem** (`pages/Inventory.tsx:135-138`).

### 3.2 Aba "Estoque Atual"

**Cartões de resumo** (`pages/Inventory.tsx:504-526,689`, `inventory.ts:23-28`): **três** cartões, "Total de itens",
"Valor investido (R$)" e "Estoque baixo". Todos refletem **só o local ativo** e só os materiais presentes nele
(`pages/Inventory.tsx:470-488`). "Valor investido" = saldo × preço de custo; no celular o valor vem compacto ("R$ 12 mil",
`pages/Inventory.tsx:495-501`). O cartão **"Projeção venda (R$)"** que o Guia Técnico cita **não existe mais** (texto sobrou
em `inventory.ts:26`, sem uso; removido na 1.17.25, `pages/Changelog.tsx:5852`).

**Abas de local** (só quando a empresa tem **mais de um** local: `pages/Inventory.tsx:692`): uma aba sublinhada por local,
com **estrela** no principal e uma **engrenagem** (rótulo de acessibilidade "Configurar itens deste local") que abre o
configurador do local (seção 3.6) (`pages/Inventory.tsx:296-387`, `inventory.ts:491-493`). **Não existe aba "Todos"**: o
local ativo é o último escolhido ou, na entrada, o principal (`pages/Inventory.tsx:165,171-179`). Com o módulo **PDV e Loja**
ligado (o mundo fictício liga todos os módulos), as abas ficam sob subtítulos: **"Loja"** para locais do tipo PDV e **"Operacional"** para
os demais; se todos os locais são operacionais (o padrão), aparece **só** o subtítulo "Operacional" acima das abas
(`pages/Inventory.tsx:121-131,692-742`, `inventory.ts:409-412`). Com **um só local**, as abas de local nem aparecem.

**Busca e filtros** (desktop: `pages/Inventory.tsx:746-790`; celular: barra de lista + "Filtros"):
- Campo de busca com placeholder **"Buscar por nome, código ou categoria..."** (celular: "Buscar material...")
  (`inventory.ts:29-32`). **A busca é universal**: com texto digitado, a tela ignora a presença no local e o filtro de
  estoque baixo (`pages/Inventory.tsx:198-220`); some a restrição "só materiais presentes neste local".
- Botão **"Filtros"** com: caixa **"Estoque abaixo do mínimo"**; lista **"Grupo"** (vazio: "Todos os grupos") quando há grupos;
  lista **"Categoria"** ("Todas as categorias") **só se algum material antigo tiver categoria** (`pages/Inventory.tsx:541-584`,
  `inventory.ts:33-38,409-412`). Há contador de filtros ativos e "limpar".
- Botão **"Exportar"** (menu "PDF" / "Excel", seção 3.7) e botão azul **"Cadastrar Material"**; no celular, ícone de exportar
  e botão flutuante **"Material"** (`pages/Inventory.tsx:440-468,782-790,1086-1092`, `inventory.ts:39-45`).

**Lista**:
- Desktop (cartão **"Itens do Estoque"**, com o sufixo **"no local de estoque {local}"** quando há local ativo):
  colunas **Nome** (miniatura da foto + nome + triângulo vermelho de estoque baixo), **SKU**, **Categoria** (mostra o **grupo**
  em selo com bolinha de cor; sem grupo, a categoria antiga), **Quantidade** (vermelho se abaixo do mínimo, seguida da
  unidade), **Qtd. mínima**, **Custo Unit.**, **Ações**. Ordenável por nome, SKU, categoria, quantidade e custo; 10 por
  página (`pages/Inventory.tsx:933-1062`, `inventory.ts:50-58`). Linha abaixo do mínimo fica com fundo avermelhado e dica
  **"Estoque abaixo do mínimo: {qty} de {min}"** (`inventory.ts:74`, `pages/Inventory.tsx:628-651`).
- Celular: lista de cartões (miniatura, nome, SKU, triângulo; subtítulo "grupo · quantidade unidade · mín N"; selo
  **"Baixo"**) e menu com **"Visualizar"** (`pages/Inventory.tsx:795-925`, `inventory.ts:61-73`).
- Menu de ações da linha (desktop): **"Editar"**, **"Registrar entrada"**, **"Registrar saída"**, **"Transferir"** (só com
  mais de um local) e **"Excluir"** (`pages/Inventory.tsx:1031-1043`).
- Vazio: **"Estoque vazio"** + "Clique em "Cadastrar Material" para adicionar peças ao estoque"; busca sem resultado:
  **"Nenhum item encontrado"** + "Tente uma busca ou filtro diferente" (`inventory.ts:75-81`).
- **Excluir** abre **"Excluir material"** ("Tem certeza que deseja excluir o material "{nome}"? Esta ação não pode ser
  desfeita.", botões "Cancelar"/"Excluir") (`pages/Inventory.tsx:1157-1175`, `inventory.ts:82-87`). Regras: se o material
  está lançado em OS, o app **bloqueia** com a mensagem "Este material está lançado em N ordens de serviço e não pode ser
  excluído…" (`hooks/useInventory.ts:21-31,384-395`); senão apaga **todas as movimentações dele** e desvincula de
  serviços e orçamentos (`hooks/useInventory.ts:396-416`), com o aviso "Item removido com sucesso!" (`hooks/useInventory.ts:436`).
  Para o vídeo: **não excluir material com histórico** (apaga o Kardex dele; seção 5, P4).

### 3.3 Janela "Novo Item de Estoque" / "Editar Item"

Abre por "Cadastrar Material", pelo botão flutuante "Material" ou por "Editar" (`components/inventory/InventoryFormDialog.tsx:418-432`,
`inventory.ts:413-416`). Campos, na ordem da tela (`components/inventory/InventoryFormDialog.tsx:433-655`, `inventory.ts:417-471`):

| Campo (rótulo) | Regra e comportamento |
|---|---|
| **Nome do Item \*** | Placeholder "Nome do item". Único obrigatório do HTML, **mas o botão Salvar não valida o nome**: vazio dá erro de banco no toast (seção 5, P5) |
| **Código/SKU** | Já vem preenchido com o **próximo código sequencial** `EST-001`, `EST-002`… (olha os 200 últimos `EST-` do catálogo da empresa); botão **"Auto"** (varinha) gera de novo, desligado ao editar; dica "Código sequencial sugerido automaticamente (você pode personalizar)."; placeholder "Ex: FLT-001". Vazio vira nulo (índice único por empresa) (`InventoryFormDialog.tsx:136-153,184-205,438-447`) |
| **Foto do item** | "Adicionar foto" / "Trocar foto" / "Remover foto"; dica "JPEG, PNG, WebP, AVIF ou HEIC. Até 5 MB."; comprime antes de enviar; vai para o bucket privado `inventory-photos`, pasta `<empresa>/<item>/` (`InventoryFormDialog.tsx:36-47,350-394,449-503`) |
| **Código de barras** | "Digite ou leia com a pistola"; o leitor USB preenche sozinho com a janela aberta; dica "A geração automática de código interno chega em breve." (`InventoryFormDialog.tsx:504-534`) |
| **Vendável na loja** (chave Sim/Não) | **Só com o módulo PDV e Loja**: "Aparece no caixa do PDV para venda ao cliente final." (`InventoryFormDialog.tsx:536-553`) |
| **Grupo** | Lista com busca e bolinha de cor; botão **"+"** ("Novo grupo") abre janela rápida com **"Nome do grupo"** (ex.: "Filtros") e **"Cor"**; sem grupos: "Nenhum grupo. Crie em Configurações." (`InventoryFormDialog.tsx:555-586,762-767`) |
| **Fornecedor** | **Lista ligada ao cadastro de fornecedores** (não é texto livre), "Escolher fornecedor...", com **"+"** ("Cadastrar fornecedor"); material antigo com texto digitado mostra "Antes estava escrito "{nome}". Escolha no cadastro para vincular." (`InventoryFormDialog.tsx:588-612`, entrada 1.28.11, `pages/Changelog.tsx:2473`) |
| **Descrição** | "Descrição detalhada do item..." |
| **Quantidade** | Saldo inicial (novo) ou saldo do **local ativo** (edição). Criar com quantidade > 0 registra uma **entrada** "Cadastro inicial"; mudar na edição registra um **ajuste** "Ajuste manual" com a diferença (`hooks/useInventory.ts:286-322,331-377`) |
| **Unidade** | Lista: Unidade (un), Quilograma (kg), Litro (l), Metro (m), Caixa (cx), Peça (pc) (`lib/inventoryUnits.ts:2-9`) |
| **Preço de Custo (R$)** e **Preço de Venda (R$)** | Duas casas, vírgula aceita ("17,99"), sem "0" travado; dica "Valor por unidade." (`InventoryFormDialog.tsx:60-61,634-655`) |
| **Locais deste material** | Um quadro por local: caixa de presença + nome (e "Principal") + campo **"Mín."** (quantidade mínima **por local**, desligado se o material não está no local). "Marcar todos"/"Desmarcar todos" só com mais de um local. Texto: "Marque os locais onde este material está presente. Defina a quantidade mínima para cada local." (`InventoryFormDialog.tsx:656-745`) |

- **Não existe campo "Categoria"** no cadastro: o texto "Categoria" sobrou como coluna da tabela e filtro para dados antigos
  (`pages/Inventory.tsx:975,1014-1016`); a lista fixa "Peças, Filtros, Gases…" do Guia Técnico está em `inventory.ts:481-489` mas
  **nenhuma tela a usa** (seção 0.4, D1).
- Ao salvar: cria/atualiza o material, grava o mínimo de cada local, grava a presença (`set_inventory_presence`); se desmarcar um
  local que ainda tem saldo, a RPC recusa (`presence_has_balance`) e a tela avisa **"Não é possível remover {nomes}"** +
  "Ainda há saldo nesse local. Transfira ou dê baixa antes. Transferir saldo." e abre a transferência já com a origem certa
  (`InventoryFormDialog.tsx:242-331`, `inventory.ts:476-480`). O botão **"Salvar"** só habilita depois que os locais carregaram
  (`InventoryFormDialog.tsx:426`). Toasts: "Item cadastrado com sucesso!" / "Item atualizado com sucesso!"
  (`hooks/useInventory.ts:322,377`).

### 3.4 Entrada e saída rápidas, e "Transferir entre locais de estoque"

**Registrar entrada / Registrar saída** (menu de ações da linha; `components/inventory/InlineMovementDialog.tsx`, `inventory.ts:544-566`):
- Título "Registrar entrada" ou "Registrar saída"; cabeçalho com o material, o SKU, o **local ativo** (selo com o nome e
  "Principal") e "Saldo atual: N un". **Não há seletor de local**: a movimentação vale para o local da aba ativa
  (`InlineMovementDialog.tsx:49-52,114-146`).
- Campos: **"Quantidade"** (placeholder "Qtd.") e **"Observação"** (placeholder "Motivo da entrada..." / "Motivo da saída..."); linha
  **"Saldo após: N"** que ganha o aviso vermelho **"Saldo ficaria negativo"** (`InlineMovementDialog.tsx:148-180`).
- Botão "Confirmar" (desligado com quantidade zero). Validações: "Informe uma quantidade maior que zero.", "Saldo
  insuficiente. Disponível: N." (saída acima do saldo é **bloqueada**). Sucesso: **"Entrada registrada"** / **"Saída registrada"**
  (`InlineMovementDialog.tsx:58-88`). RPC `register_inventory_movement` (seção 4).

**Transferir entre locais de estoque** (`components/inventory/StockTransferDialog.tsx`, `inventory.ts:349-370`): só no menu
quando há mais de um local. Subtítulo com o nome e SKU do material; **"Local de origem"** (já vem o ativo) e **"Local de
destino"** ("Selecionar local...", com selo "Principal"), mostrando **"Disponível: N"**; **"Quantidade"**; **"Observações"** ("Motivo da
transferência..."); botão **"Transferir"**. Erros no toast "Confira os dados": "Selecione o local de origem.", "Selecione o local
de destino.", "Origem e destino não podem ser o mesmo local de estoque.", "Informe uma quantidade maior que zero.", "Saldo
insuficiente no local de origem." (`StockTransferDialog.tsx:67-100`). Sucesso: "Transferência realizada com sucesso!"
(`hooks/useStocks.ts:171`). O envio leva um identificador único (`clientRequestId`), então repetir o clique não duplica.

### 3.5 Janela "Configurações do Estoque" (botão "Configurações")

Duas abas (`components/inventory/InventorySettingsDialog.tsx:35-85`, `inventory.ts:371-399`): **"Grupos de material"** e
**"Locais de estoque"**.
- **Grupos de material**: lista com bolinha de cor, nome, **arrastar para reordenar** (`InventorySettingsDialog.tsx:96-146`),
  lápis para editar nome e cor (seletor de cor) e lixeira. Criar: campo **"Novo grupo"** ("Nome do grupo...") + seletor de cor +
  botão "+". Vazio: "Nenhum grupo cadastrado." Excluir: **"Excluir grupo?"** — "O grupo será removido. Materiais vinculados
  ficarão sem grupo." (`InventorySettingsDialog.tsx:147-215`).
- **Locais de estoque**: lista com ícone de depósito, nome, selo **"Principal"** e menu com **"Definir como principal"**
  (só nos outros), **"Renomear"** e **"Excluir"** (nunca no principal). Criar: campo **"Novo local de estoque"** ("Nome do local...") +
  botão "+" (também Enter). Excluir: **"Excluir local de estoque?"** — "O local "{nome}" será removido. Esta ação não pode ser
  desfeita." (`InventorySettingsDialog.tsx:326-475`). Toasts: "Depósito criado com sucesso!", "Depósito renomeado!", "Depósito
  excluído!", "Depósito principal atualizado!" (`hooks/useStocks.ts:69,83,98,140`). Travas do banco: **o local principal e o
  último local não podem ser excluídos** ("O depósito principal não pode ser excluído. Defina outro como principal primeiro.",
  `hooks/useStocks.ts:101-111`, `supabase/migrations/20260721160000_multi_estoque_e_grupos_material.sql:150-188`).
- Toda empresa nasce com **"Estoque Principal"** (criado na empresa pelo banco: `supabase/migrations/20260721210000_ensure_default_stock.sql:1-40`).
  O primeiro local criado à mão não vira principal, o principal já existe.

### 3.6 Janela "Configurar {local}" (engrenagem do local)

Título **"Configurar {nome do local}"**; abas **"Itens"** e **"Acesso"** e, só com o módulo PDV e Loja, **"Tipo"**
(`components/inventory/StockConfiguratorDialog.tsx:275-322`, `inventory.ts:491-543`).
- **Itens** (`StockConfiguratorDialog.tsx:324-453`): quadro **"Adicionar por grupo"** (seletor "Selecionar grupo..." +
  botão **"Adicionar grupo"**, que marca todos os materiais do grupo e **grava na hora**, sem esperar o "Salvar": `StockConfiguratorDialog.tsx:204-222`), busca **"Buscar material..."**, **"Marcar todos"** /
  **"Desmarcar todos"** e a lista com caixa por material. Vazio: "Nenhum material cadastrado." / "Nenhum material encontrado.".
  Salvar: **"Itens do local atualizados"**. Desmarcar um material com saldo no local é recusado com **"Não é possível remover
  {nomes}"** + "Ainda há saldo neste local. Transfira ou dê baixa antes." + ação **"Transferir saldo"**
  (`StockConfiguratorDialog.tsx:242-262`).
- **Acesso** (`StockConfiguratorDialog.tsx:455-525`): chave **"Restringir acesso a este local"** (Aberto/Restrito) com a explicação
  **"Todos os usuários da empresa veem este local."** ou **"Apenas os usuários marcados veem e movimentam este local."**; no
  modo restrito aparece a lista de usuários: admin, gestor e super admin vêm marcados e travados, com o texto **"Sempre tem
  acesso"** (`StockConfiguratorDialog.tsx:30,131-138,494-503`); os demais têm uma chave cada. Botão **"Salvar acesso"** →
  **"Acesso do local atualizado"**. Detalhe: marcar "Restrito" **sem marcar ninguém** grava lista vazia e o local continua
  **aberto** (a RPC só guarda quem foi marcado; "restrito" é derivado de haver linhas: `supabase/migrations/20260814225028_stock_access_acl.sql:693-786`).
- **Tipo** (só PDV): "Este local é da loja ou operacional?" **Loja** / **Operacional**; "Locais da loja alimentam a venda no PDV.
  Locais operacionais ficam fora do balcão." → "Tipo do local atualizado" (`StockConfiguratorDialog.tsx:527-545`).

### 3.7 Exportar o estoque (PDF / Excel)

Botão **"Exportar"** → menu **"PDF"** / **"Excel"** → janela **"Selecionar materiais"** com **"Selecionar todos"**, **"Limpar todos"**,
lista com caixa (nome, SKU, selo com a quantidade do local ativo e a unidade), rodapé "N de M selecionados" e botão
**"Exportar PDF"** ou **"Exportar Excel"** (`components/inventory/InventoryExportDialog.tsx:30-173`, `inventory.ts:339-348`). O
arquivo é gerado **no navegador** e baixado (PDF "Relatório de Estoque", com "VALOR TOTAL EM ESTOQUE (CUSTO)"; Excel aba "Estoque")
(`pages/Inventory.tsx:389-436`, `inventory.ts:88-112`). **O gravador não captura download** (TRILHA, item 6): mostrar a janela de
seleção e parar antes de confirmar, ou aceitar o toast de erro/ausência de arquivo.

### 3.8 Aba "Histórico de Materiais (Kardex)"

Tela em **duas colunas** (lista de materiais à esquerda, movimentos à direita; no celular, lista e detalhe se alternam com o botão
"Materiais" de voltar) (`components/inventory/InventoryKardexTab.tsx:386-406`, `inventory.ts:113-186`).
- **Coluna "Materiais"** ("N materiais no estoque"): item fixo no topo **"Geral (Todos)"** ("N movimentações no período"), busca
  **"Buscar material..."**, ordenação ("Nome (A-Z)", "Nome (Z-A)", "Mais movimentados", "Movimentação mais recente") e botão
  **"Filtros"**; cada material mostra SKU ("Sem código" se não tiver) e uma bolinha com a **contagem de movimentos no período**
  (`InventoryKardexTab.tsx:305-358`).
- **Filtros**: **"Período"** (padrão **este mês**, `useDateRangeFilter('this_month')`), **"Tipo de movimento"** ("Todos os tipos") e
  **"Local"** ("Todos os locais"); só aparecem opções de tipo e de local que existem nos dados (`InventoryKardexTab.tsx:186-290`).
  **Atenção ao roteiro:** com o padrão "este mês", movimentos de meses anteriores não aparecem; a semente precisa de
  movimentos dentro do mês da data do navegador ou o roteiro troca o período.
- **Coluna da direita**: título **"Kardex geral"** ("Movimentações de todos os materiais no período selecionado") ou o nome do
  material ("Histórico deste material"), selo "N movimentações" (`InventoryKardexTab.tsx:416-433`). Vazio: **"Sem movimentações"**
  ("As entradas, saídas e ajustes de estoque aparecem aqui conforme acontecem.") ou, com filtro, **"Nenhuma movimentação
  encontrada"** ("Tente outro período ou filtro.") (`inventory.ts:180-185`).
- **Tabela (a partir de 1280 px; abaixo disso, cartões)**: **"Data e Hora"**, **"Tipo"** (selo colorido), **"Material e origem"** (com o
  material selecionado vira **"Origem"**; o nome e a foto de quem lançou ficam **dentro desta coluna**, não há coluna "Usuário"),
  **"Local"**, **"Estoque inicial"**, **"Alteração"** (verde com "+", vermelho com "−") e **"Estoque final"**; 25 por página
  (`InventoryKardexTab.tsx:231,504-583`, `inventory.ts:153-163`).
- **Tipos** (`inventory.ts:172-179`): Entrada, Saída, Ajuste, Transferência, Consumo, Estorno. **Origem** mostra: "OS #123" quando veio de
  OS (`formatOSNumber`), "Fornecedor: {nome}" quando veio de compra/recebimento, senão a **observação** digitada
  ("Cadastro inicial", "Ajuste manual", o motivo da entrada) ou "—" (`InventoryKardexTab.tsx:93-105`). Sem autor: "Sistema". Material
  apagado depois: "Material removido" (`inventory.ts:170-171`).
- **Local**: o nome do local; em **transferência** mostra o par "Galpão → Van 01" montado com a perna negativa (origem) e a positiva
  (destino) (`InventoryKardexTab.tsx:108-129`, `inventory.ts:168`). Se a contraparte não for visível ao usuário (acesso por local), mostra só o
  lado conhecido.
- Quem não tem acesso a um local **não vê os movimentos dele** (política de leitura por `can_access_stock`: seção 2).
- O título "Histórico de Movimentações" do arquivo de textos (`inventory.ts:114`) **não aparece** na tela hoje (seção 0.4, D2).

### 3.9 Aba "Compras de Material"

**Mudou muito desde a trilha (1.22.5).** O fluxo de hoje é: **requisição → cotações → fornecedor escolhido por material → ordens de compra
(uma por fornecedor) → marcar como enviada → registrar recebimento (entrada no estoque)**. "Aceitar" a cotação **não mexe no estoque**
e o antigo "Registrar entrada no estoque" da cotação foi **removido de propósito** (`hooks/useCompraCotacoes.ts:249-262`; entrada 1.28.10,
`pages/Changelog.tsx:2485`). Há ainda a **compra direta**, que lança estoque e Financeiro de uma vez.

**Lista de requisições** (`components/inventory/MaterialPurchasesTab.tsx:174-362`, `inventory.ts:187-245`):
- Título **"Requisições de Compra"**. Se há material abaixo do mínimo em algum local, faixa vermelha **"{count} material abaixo do mínimo"** / **"{count} materiais abaixo do mínimo"** (`inventory.ts:228-229`) com a
  ação **"Criar requisição"**, que apenas abre a janela de requisição **vazia** (não pré-preenche; conta materiais únicos, vinda da view `inventory_low_stock`) (`MaterialPurchasesTab.tsx:132,181-196`,
  `hooks/useLowStock.ts:29-47`).
- Barra: busca **"Buscar por código ou título..."** (aceita `#3`, `3`, título, status e observações) + filtro **"Status"** ("Todos os status":
  Aberta/Concluída/Cancelada); botões **"Fornecedores"**, **"Nova requisição de compra"** e, só para quem pode, **"Registrar compra direta"**
  (celular: ícones, "Nova Compra" e "Compra direta") (`MaterialPurchasesTab.tsx:199-278`, `inventory.ts:196-200`).
- Cartões em grade (1/2/3 colunas): `#número` + título + selo de status; data e "N cotação(ões)"; selo verde **"Aceita: {fornecedor}"** quando
  há cotação aceita; **"Menor cotação: R$ …"**; menu: "Editar", "Concluir requisição" (só aberta), "Reabrir requisição" (não aberta),
  "Cancelar requisição" (confirma: "Cancelar requisição?"), "Excluir" ("Excluir requisição?": "{título}" e suas cotações serão removidas…)
  (`MaterialPurchasesTab.tsx:149-175,296-362,371-420`, `inventory.ts:212-244`). Compra direta aparece com o selo **"Compra direta"**, o
  fornecedor e **"Total: R$ …"**, e **sem menu** (somente consulta).
- Vazio: **"Nenhuma requisição de compra"** ("Crie uma requisição de compra, liste os materiais e compare cotações de fornecedores.")
  (`inventory.ts:221-226`). Toasts de status: "Requisição concluída.", "Requisição reaberta.", "Requisição cancelada.",
  "Requisição excluída." (`hooks/useCompras.ts:265-272,319`).

**Janela "Nova Requisição de Compra" / "Editar Requisição de Compra"** (`components/inventory/CompraEditorDialog.tsx:268-466`,
`inventory.ts:613-662`): **"Título \*"** ("Ex.: Reposição de materiais, Junho"); **"Local de destino"** (já vem o principal: "Os
materiais recebidos entram neste local de estoque."); **"Materiais"** com chave **"Do estoque"** / **"Fora do estoque"** (busca do
catálogo "Adicionar material do estoque..."; ou "Adicionar material fora do estoque" com "Nome do material...", que ganha o selo
**"Fora do estoque"**), quantidade e unidade por linha (selo "Abaixo do mínimo" quando for o caso); botão **"Adicionar itens abaixo
do mínimo"** abre "Itens abaixo do mínimo" (escolha **"Selecionar local de estoque"**, lista com **"Deficit: N un"**, botão **"Adicionar à
requisição"**; as quantidades entram **em branco** para preencher) (`CompraEditorDialog.tsx:328-455,471-560`); **"Observações"**.
Validações (toast "Confira a requisição"): "Dê um título à requisição.", "Adicione ao menos um material.", "Dê um nome ao material fora
do estoque antes de salvar.", "Quantidade do material "X" deve ser maior que zero." (`CompraEditorDialog.tsx:238-258`). Editar uma
requisição que já tem cotação mostra o aviso amarelo **"Esta requisição já tem cotações. Mudar os materiais vai apagar os preços já informados."**
(`CompraEditorDialog.tsx:297-300`). Toasts: "Requisição criada!", "Requisição atualizada!" (`hooks/useCompras.ts:216,251`).

**Tela da requisição** (clicar no cartão; mesma aba, botão **"Voltar para requisições"**) (`components/inventory/CompraDetailView.tsx:226-540`,
`inventory.ts:663-743`):
1. Cabeçalho: `#número`, título, selo de status; menu **"Ações"** (Editar, Concluir/Reabrir, Cancelar, Excluir).
2. **"Materiais"**: cada linha com nome, "• qtd unidade" e (se foi precificado em alguma cotação não recusada) o seletor **"Fornecedor
   escolhido"** ("Escolher fornecedor...") com as opções "Fornecedor (R$ preço)" em ordem de preço; grava na hora, sem toast de sucesso
   (`CompraDetailView.tsx:254-309`, `hooks/useCompras.ts:284-306`).
3. **"Cotações"** com botão **"Nova cotação"** (janela com **"Fornecedor \*"** "Escolher fornecedor..." e botão "Novo"; um fornecedor só cota uma vez por requisição, "Todos os fornecedores já têm cotação."; tabela **Material · Qtd. · Valor unitário (R$) · Valor total (R$)** em que vale digitar o unitário **ou** o total, "Total geral", botões "Cancelar"/"Salvar cotação"; linha sem preço fica fora: `components/inventory/CotacaoDialog.tsx:110-160,208-337`, `inventory.ts:744-771`): vazio "Nenhuma cotação" ("Adicione cotações de fornecedores para comparar preços.").
   Cada cotação: fornecedor, selo (Pendente/Aceita/Recusada), selo **"Mais barata"** (troféu), "{n}/{total} materiais com preço", valor
   total e menu **"Editar preços"** ("Ver preços" se recusada), **"Aceitar"** (desligado se o total é zero), **"Desfazer aceite"**,
   **"Reabrir"** (recusada), **"Recusar"** ("Recusar cotação?": "Os preços ficam guardados, só não entram na comparação."), **"Excluir"**
   (`CompraDetailView.tsx:311-424`). Quando aceita, o cartão ganha borda verde e a nota **"Aceitar não mexe no estoque. Use "Registrar
   entrada" quando o material chegar."** (`CompraDetailView.tsx:416-421`, `inventory.ts:673`): **texto desatualizado**, porque o
   caminho de hoje é o "Registrar recebimento" da O.C. (seção 5, P6 [handoff]). Toasts: "Cotação criada!", "Preços salvos!",
   "Cotação aceita!", "Cotação recusada.", "Cotação reaberta.", "Cotação removida." (`hooks/useCompraCotacoes.ts:144,199,222-226,242`).
4. **"Ordens de compra"** com botão **"Gerar ordens de compra"** (ligado só quando algum material tem fornecedor escolhido): cria **uma O.C.
   por fornecedor escolhido**, status **Rascunho**; fornecedor que já tem O.C. em aberto na requisição é **pulado** com aviso; toasts "1 ordem de compra gerada." / "N ordens de compra
   geradas." / "Nenhum material com fornecedor escolhido. Escolha o fornecedor de cada material antes de gerar as ordens." /
   "N fornecedor já tinha ordem em aberto e foi pulado." (`hooks/useCompraOrdens.ts:164-342`, `inventory.ts:286-292`). Vazio: "Nenhuma
   ordem de compra gerada. Escolha o fornecedor de cada material e gere as ordens." Cada O.C.: `#número`, fornecedor, selo
   (**Rascunho, Enviada, Recebida parcial, Recebida, Cancelada**), "Itens: N", total e menu: **"Marcar como enviada"** (rascunho), **"Baixar PDF"**,
   **"Registrar recebimento"** (**só com a O.C. "Enviada" ou "Recebida parcial"**), **"Voltar para rascunho"** (cancelada), **"Cancelar
   ordem"** ("Cancelar esta ordem de compra?"), **"Excluir ordem"** (`CompraDetailView.tsx:428-540`, `inventory.ts:301-322`).
   "Baixar PDF" gera o arquivo no navegador (`generateOrdemCompraPdf`, `CompraDetailView.tsx:137-148`): download, que o gravador não captura.
5. **"Registrar recebimento"** (`components/inventory/OrdemCompraReceiveDialog.tsx:42-176`): subtítulo "Informe só o que chegou agora. Você pode
   receber em partes, o saldo continua pendente."; por item mostra **Qtd. pedida**, **Qtd. recebida**, **Qtd. pendente** e o campo
   "Quantidade" (passar do pendente fica vermelho: "A quantidade recebida de "X" passa do que foi pedido…" e trava o botão); botões
   **"Receber tudo"**, **"Cancelar"**, **"Confirmar recebimento"**; toast "Recebimento registrado. 1 item atualizado." / "Recebimento registrado. N itens atualizados." (`inventory.ts:328-329`); ao marcar como enviada, "Ordem marcada como enviada." (`inventory.ts:310`)
   (`inventory.ts:323-331`). A RPC `receber_ordem_compra` dá a **entrada no local de destino da requisição**, soma o recebido, recalcula
   o status (parcial → "Recebida parcial"; tudo → "Recebida"), cria no cadastro o material "fora do estoque" e **não cria despesa no
   Financeiro** (`supabase/migrations/20260930110000_compras_ordem_de_compra.sql:540-716`).

**Registrar compra direta** (`components/inventory/DirectMaterialPurchaseDialog.tsx`, `inventory.ts:246-276`): janela **"Compra de material"**
("Registre a entrada no estoque e a despesa financeira em uma única operação."). Campos: **"Descrição"** ("Ex.: Reposição de cobre"; opcional),
**"Fornecedor \*"** (com busca), **"Local de estoque \*"** (vem o principal), **"Data da compra \*"** (não aceita data futura); bloco
**"Materiais"** ("O total financeiro é calculado a partir dos itens.", "Adicionar material"; por linha Material, Quantidade, Preço unitário,
Subtotal, remover; **"Total da compra"**); **"Categoria financeira \*"** (sugere uma despesa de CMV com "materia" no nome),
**"Conta financeira \*"** (só contas ativas que não são cartão), **"Situação do pagamento"** (**Pago** ou **Pendente**), em Pago:
**"Forma de pagamento \*"** (Dinheiro, Pix, Cartão de débito, Transferência, Boleto, Cheque) e **"Data do pagamento \*"**; em Pendente:
**"Vencimento \*"**; **"Observações"**. Botão **"Registrar compra"** (toast "Compra registrada" / "O estoque e o financeiro foram
atualizados."). Validações no toast "Revise os dados da compra" (`DirectMaterialPurchaseDialog.tsx:164-186`). Sem conta elegível: "Nenhuma conta
financeira elegível" ("Cadastre uma conta de caixa ou banco ativa para registrar a compra."). Envia `clientRequestId`: repetir não duplica.
A RPC `registrar_compra_material_direta` cria a compra (`flow_type = compra_direta`), as entradas e a despesa numa transação
(`supabase/migrations/20261018005000_compra_direta_estoque_financeiro.sql:137-540`). Na lista e no detalhe a compra direta mostra a
nota **"Compra integrada ao estoque e ao financeiro. Para preservar o histórico, seus registros não podem ser alterados separadamente."**
(`inventory.ts:271`).

**Fornecedores** (botão "Fornecedores" da aba Compras; janela `components/inventory/SuppliersDialog.tsx`, `inventory.ts:590-612`): lista com
busca **"Buscar fornecedor..."** (nome, CPF/CNPJ, contato), botão **"Novo"**, cada linha com nome e "CPF/CNPJ • contato • telefone" (ou "Sem
dados adicionais"), lápis e lixeira; vazio "Nenhum fornecedor" ("Cadastre fornecedores para usá-los nas cotações."). Excluir:
"Excluir fornecedor?" — "{nome}" será removido. Esta ação não pode ser desfeita. (`SuppliersDialog.tsx:22-141`). Cadastro (**"Novo Fornecedor"** /
**"Editar Fornecedor"**, `components/inventory/SupplierFormDialog.tsx:29-121`, `inventory.ts:567-589`): **"Nome \*"** (único obrigatório),
**"CPF/CNPJ"**, **"Contato"**, **"Telefone"**, **"E-mail"**, **"Endereço"**, **"Observações"**; botões "Cancelar"/"Salvar". É o **mesmo cadastro** da aba
Fornecedores da tela Clientes (T3), com histórico de gastos; ao excluir um fornecedor as **cotações dele são apagadas** e os lançamentos
financeiros só perdem o vínculo (entrada 1.24.36, `pages/Changelog.tsx:3611`).


### 3.10 Janela "Importar XML (NF-e)" (botão do cabeçalho)

Abre pelo botão **"Importar XML (NF-e)"** do cabeçalho da tela (`pages/Inventory.tsx:604-625,1119`, `inventory.ts:42`); janela
`components/inventory/NfeImportDialog.tsx` (586 linhas), título **"Importar XML (NF-e)"** (`inventory.ts:973-1033`). **Tudo acontece no
navegador** (não existe função de servidor para ler a nota, só leitura do arquivo e gravação de entradas), então o arquivo precisa estar
na máquina de quem grava.

1. **Etapa 1, escolher o arquivo** (`NfeImportDialog.tsx:330-356`): caixa tracejada com ícone de envio e o texto "Selecione o arquivo
   **.xml** da nota fiscal eletrônica para dar entrada no estoque." e o botão **"Escolher arquivo XML"** (`inventory.ts:975-979`). O campo
   de arquivo é escondido e só aceita `.xml` (`NfeImportDialog.tsx:352`). O rodapé com o botão de confirmar só existe depois que a
   nota foi lida (`NfeImportDialog.tsx:310-327`).
2. **Leitura da nota** (`NfeImportDialog.tsx:162-193`, `lib/nfeParser.ts:101-199`): detecta se o arquivo é ISO-8859-1 pela primeira linha
   do XML (para não estragar os acentos), e extrai **chave de acesso** (44 dígitos), **emitente** (CNPJ ou CPF e razão social), cada
   **produto** (nome, código do fornecedor, código de barras, unidade, quantidade, valor unitário, total) e o **total da nota**
   (`lib/nfeParser.ts:134-180`). Código de barras "SEM GTIN" é ignorado; unidade vem em minúsculas ("un" se faltar). Erros viram aviso
   vermelho no canto (sem abrir a revisão): "Arquivo vazio. Selecione o XML da NF-e.", "XML de NF-e inválido. Verifique o arquivo.",
   "Este XML é de NFS-e/CT-e, não de NF-e de produto.", "XML de NF-e inválido. Não encontramos os dados da nota.", "Nenhum produto
   encontrado na nota." (`lib/nfeParser.ts:103-131,175`).
3. **Nota já importada** (`NfeImportDialog.tsx:183-190,557-585`, `hooks/useNfeImport.ts:53-71`): se a chave já está no registro de
   notas importadas da empresa, abre uma caixa **"Nota já importada"**: "Esta nota já foi importada em {data e hora}. Importar de novo
   vai duplicar a entrada no estoque. Deseja continuar?" com **"Cancelar"** (volta ao começo) e **"Importar mesmo assim"** (segue para a
   revisão) (`inventory.ts:1024-1029`). Isso é aviso, não trava: a tabela `nfe_imports` **não é única de propósito**
   (`supabase/migrations/20260619194000_nfe_imports_log.sql:1-5`). Nota sem chave não tem essa checagem e a revisão mostra "Esta nota não
   tem chave de acesso. Não será possível avisar se ela for importada de novo." (`NfeImportDialog.tsx:394-399`, `inventory.ts:993`). Se a
   própria consulta falhar, o fluxo segue sem avisar (`hooks/useNfeImport.ts:62-66`).
4. **Etapa 2, revisão** (`NfeImportDialog.tsx:358-548`):
   - **Cartão do fornecedor** (rótulo **"Fornecedor"**): razão social (ou "Não identificado") e CNPJ com máscara; selo **"Vinculado"** quando o
     CNPJ é igual ao de um fornecedor cadastrado (só vale documento com 11 dígitos ou mais) ou selo **"Novo"** com a frase
     "Será criado o fornecedor "{nome}"." (`NfeImportDialog.tsx:110-124,360-391`, `inventory.ts:986-992`). **Por isso, para o fornecedor
     aparecer "Vinculado", o CNPJ do fornecedor fictício no cadastro tem de ser igual ao da nota** (seção 4, lacunas da semente).
   - **"Produtos da nota"** com o resumo "N novos • M no total" (ou "M no total") (`NfeImportDialog.tsx:402-418`, `inventory.ts:994-1000`).
   - **Cada produto vira um cartão**: caixinha de incluir (marcada), **nome editável**, linha discreta "cód … • EAN …" (quando houver), **"Qtd"**,
     **"Unidade"**, **"Custo un."** (todos editáveis; vírgula aceita) e o seletor **"Destino no estoque"**, que oferece **"Criar novo
     item"** e todos os materiais do cadastro no formato "Nome (SKU)" (`NfeImportDialog.tsx:420-515`, `inventory.ts:1001-1005`). O sistema
     **já sugere um material existente** quando o nome da nota contém o nome cadastrado ou o contrário (sem diferenciar acento, caixa ou
     espaço; ou todas as palavras presentes), pegando o **primeiro** que casa; se nada casa, vem "Criar novo item"
     (`NfeImportDialog.tsx:50-53,141`, `lib/utils.ts:48-67`). Avisos por linha: vermelho **"Quantidade precisa ser maior que zero."** e
     amarelo **"Unidade da nota: UN ≠ cadastro: CX"** quando a unidade difere da do material escolhido (`NfeImportDialog.tsx:519-547`,
     `inventory.ts:1006-1007`). Linha desmarcada fica apagada e travada.
   - **Rodapé**: "N itens • R$ …" (a soma de quantidade × custo das linhas marcadas, **não** o total impresso na nota) e o botão
     verde **"Confirmar entrada"** ("Importando..." enquanto grava) (`NfeImportDialog.tsx:234-237,310-327`, `inventory.ts:980-985`).
5. **Confirmar** (`NfeImportDialog.tsx:240-296`, `hooks/useNfeImport.ts:77-209`):
   - Quantidade zero ou negativa em linha marcada trava com o aviso "Quantidade inválida" ("Corrija a quantidade (maior que zero) de N
     item(ns) ou desmarque esse item antes de importar.") (`NfeImportDialog.tsx:246-260`, `inventory.ts:1009-1013`).
   - Se o fornecedor não está vinculado, **cria o fornecedor** (nome e CNPJ da nota) no cadastro de fornecedores
     (`hooks/useNfeImport.ts:87-109`). Para cada linha: se escolheu "Criar novo item", cria o material (nome, unidade e custo da nota,
     **sem código, sem grupo e sem mínimo**) e depois lança a **entrada** no Kardex com o fornecedor, o custo e a observação
     **"Importado da NF-e {chave}"** (ou "Importado de NF-e (XML)") (`hooks/useNfeImport.ts:111-175`). Se a entrada falha, o material
     recém-criado é apagado e a linha conta como falha. Por fim registra a nota como importada (`hooks/useNfeImport.ts:178-190`).
   - **A entrada vai sempre para o local principal** (o padrão): a tela não tem seletor de local e a chamada não informa o local, então a
     função do servidor usa o local marcado como padrão (`hooks/useNfeImport.ts:148-155`,
     `supabase/migrations/20261013150000_customer_paid_expenses_and_customer_stock.sql:702-715`). O material passa a "existir" nesse local
     (`supabase/migrations/20261013150000_customer_paid_expenses_and_customer_stock.sql:781-786`).
   - Aviso de sucesso: título **"NF-e importada"** (ou **"Importação concluída com avisos"** se alguma linha falhou) e texto
     "3 itens importados • 2 novos. Entrada registrada no estoque." (`NfeImportDialog.tsx:269-296`, `inventory.ts:1014-1022`). A janela fecha.
- **O que a importação NÃO faz** (a trilha da 1.22.5 prometia "a compra montada sozinha"; **não é verdade no código de hoje**, seção 0.1,
  e seção 6): **não cria requisição/compra**, **não cria despesa no Financeiro**, **não aparece no "Relatório"** (que só lê ordens de
  compra recebidas e compras diretas, seção 3.13), **não guarda o XML** (só a chave, fornecedor, total e quantidade de itens) e **não
  atualiza o "Custo Unit." do material já cadastrado** (o custo pago fica só no movimento do Kardex). A leitura das **parcelas** da nota
  (`duplicatas`, `lib/nfeParser.ts:40-47,182-196`) é usada apenas na tela de **notas fiscais recebidas** do módulo fiscal para lançar a
  despesa com vencimento real (`components/fiscal/inboundNotes/LancarNotaDespesaDialog.tsx:120-131`), assunto do T14, não deste.
- **No Kardex** a entrada aparece como tipo "Entrada", origem **"Fornecedor: {nome}"** (a observação com a chave fica no banco, mas a
  coluna prefere o fornecedor) e local = o principal (`components/inventory/InventoryKardexTab.tsx:93-105`).
- **Desde a 1.22.5** (Changelog): 1.24.42 corrigiu o campo de valor que "engolia" a vírgula também na importação de nota (digitar 17,99 virava 1799;
  `pages/Changelog.tsx:3519`); 1.28.22 consertou a entrada de produtos pela importação de nota, que falhava (`pages/Changelog.tsx:2266`); a função
  nasceu na 1.13.8 ("Importar estoque pela NF-e do fornecedor", `pages/Changelog.tsx:7701`).
- Material criado por esta janela guarda o fornecedor só como texto antigo: ao abrir "Editar Item", o campo **Fornecedor** vem vazio com a
  frase "Antes estava escrito "{nome}". Escolha no cadastro para vincular." (`components/inventory/InventoryFormDialog.tsx:604-612`,
  `inventory.ts:440`; seção 5, P7).

### 3.11 Aba "Inventários" (contagem física)

**Lista** (`components/inventory/InventoryCountsTab.tsx`, 385 linhas; textos `inventory.ts:772-895`). À direita do topo, o botão **"Novo
inventário"** (`InventoryCountsTab.tsx:198-211`, `inventory.ts:773`). No desktop a lista é um cartão chamado **"Inventários"** com a tabela
**Número · Status · Data · Observações · Ações** (`InventoryCountsTab.tsx:271-352`, `inventory.ts:774,801-807`): "#N" (numeração sequencial por
empresa, `supabase/migrations/20260721170000_inventario_e_posicao_de_estoque.sql:30-112`), selo **Aberto / Finalizado / Cancelado**
(`inventory.ts:796-800`), data e hora, observação cortada ("-" se não houver) e, em Ações, o menu de exportar (PDF ou Excel) mais o menu da
linha com **"Ver detalhe"** e, só enquanto **Aberto**, **"Cancelar inventário"** (`InventoryCountsTab.tsx:320-345`, `inventory.ts:808-811`).
Clicar na linha abre o detalhe. No celular vira lista com título "Inventário #N" (`InventoryCountsTab.tsx:213-265`). Vazio: **"Nenhum
inventário"** ("Crie um inventário para conferir e ajustar os saldos do estoque.") com o botão "Novo inventário"
(`InventoryCountsTab.tsx:222-229,286-292`, `inventory.ts:821-826`).

**Assistente "Novo inventário"** (`components/inventory/InventoryCountWizard.tsx`, 446 linhas; janela de **3 etapas**, cujo título muda a cada
etapa: **"Locais"** → **"Escopo"** → **"Confirmar"**, com bolinhas de progresso, `InventoryCountWizard.tsx:23,144-148,186-197`,
`inventory.ts:839-874`):
1. **Locais**: "Selecione os locais de estoque que serão contados." Uma linha com caixa por local, o padrão traz o selo **"Principal"**;
   "Avançar" só habilita com pelo menos um local marcado; sem nenhum local: "Nenhum local de estoque cadastrado."
   (`InventoryCountWizard.tsx:121,199-233`). A lista traz os locais que a pessoa pode ver (acesso por local, seção 2).
2. **Escopo**: "Escolha quais materiais entram na contagem." Três botões de escolha: **"Todos os materiais dos locais"** (já vem marcado),
   **"Por grupo de material"** (busca "Buscar grupo...", lista com bolinha de cor) e **"Itens específicos"** (busca "Buscar por nome ou
   código...", lista com nome e SKU); nos dois últimos há "Selecionar todos" / "Limpar seleção" e o contador "N de M selecionados"
   (`InventoryCountWizard.tsx:235-392`). Sem grupos: "Nenhum grupo cadastrado."
3. **Confirmar**: quadro **"Resumo do inventário"** com "Locais: …" e "Escopo: Todos os materiais dos locais / N grupos / N itens", e o campo
   **"Observações"** ("Contexto, turno, responsável...") (`InventoryCountWizard.tsx:394-431`). **"Criar inventário"** ("Criando...") fica
   desligado se o escopo escolhido estiver vazio (`InventoryCountWizard.tsx:122-127,168-175`). Toast **"Inventário criado"**
   (`inventory.ts:873`). "Voltar"/"Cancelar" descartam tudo (`InventoryCountWizard.tsx:43-57,150-155`).
4. **O que a criação grava** (`hooks/useInventoryCounts.ts:74-175`): o cabeçalho (número gerado pelo banco), os locais escolhidos e **uma
   linha por par material × local** com o **"Esperado" congelado nesse instante** (o saldo do local naquele momento) e o custo unitário do
   cadastro. Os pares vêm das **linhas de saldo** que já existem nos locais escolhidos (`hooks/useInventoryCounts.ts:114-131`); um material
   que nunca foi movimentado nem configurado num local **não entra** na contagem, e um marcado como ausente do local entra com esperado 0
   (seção 5, P9).

**Detalhe e contagem** (`components/inventory/InventoryCountDetailModal.tsx`, 503 linhas; título **"Inventário #N"**,
`InventoryCountDetailModal.tsx:259`, `inventory.ts:795`). De cima para baixo (`InventoryCountDetailModal.tsx:262-298`):
- as observações do inventário numa faixa cinza, se houver;
- quando já existe divergência, faixa amarela **"Divergências encontradas: N itens"** com **"Valor total das divergências: R$ …"**
  (`InventoryCountDetailModal.tsx:269-277`, `inventory.ts:781-784`);
- duas abas: **"Todos os itens"** e **"Divergências (N)"** (`InventoryCountDetailModal.tsx:279-298`, `inventory.ts:785-787`).
- **"Todos os itens"**: colunas **Material** (com SKU), **Local**, **Esperado** (com a unidade), **Contado** e **Diferença**
  (`InventoryCountDetailModal.tsx:310-381`, `inventory.ts:788-792`). Com o inventário **Aberto**, "Contado" é um campo ("Qtd.", até 3
  casas, vírgula aceita) e **o valor é salvo quando a pessoa sai do campo** (não há botão "Salvar"; a divergência se atualiza na hora)
  (`InventoryCountDetailModal.tsx:136-155,347-360`). Campo vazio = **"Não contado"**. Diferença: "—" (não contado), "0", verde "+N" ou
  vermelho "−N". Depois de Finalizado ou Cancelado a coluna vira só leitura (`InventoryCountDetailModal.tsx:82,361-367`).
- **"Divergências"**: Material, Local, Esperado, Contado, Diferença, **"Valor divergência"** e, no rodapé, o total; vazio: "Nenhuma divergência
  encontrada." (`InventoryCountDetailModal.tsx:398-455`, `inventory.ts:792,824`). Itens não contados **não** contam como divergência
  (`hooks/useInventoryCounts.ts:61-72`).
- **Rodapé** (`InventoryCountDetailModal.tsx:211-249`): à esquerda **"Exportar"** (PDF ou Excel, geração no navegador: baixa arquivo);
  à direita **"Fechar"** e, só no inventário **Aberto**, o botão verde **"Finalizar inventário"**.
- **Caixa "Finalizar inventário?"** (`InventoryCountDetailModal.tsx:460-500`, `inventory.ts:827-838`): com divergência, "N itens com divergência.
  O estoque será ajustado em R$ …. **Esta ação não pode ser desfeita.**"; sem divergência, "Nenhuma divergência encontrada. O estoque não será
  alterado."; campo **"Observações finais"** ("Registre o motivo ou contexto do inventário..."); botões **"Cancelar"** e **"Finalizar"**
  ("Finalizando..."). Ao concluir, a janela fecha e aparece o aviso **"Inventário finalizado"** + "N itens ajustados no estoque." (ou
  "Nenhuma divergência encontrada.") (`hooks/useInventoryCounts.ts:216-229`, `inventory.ts:812-820`).
- **O que a finalização faz** (`supabase/migrations/20260721170000_inventario_e_posicao_de_estoque.sql:206-319`): para cada item **contado**,
  calcula a diferença entre o contado e o **saldo de agora** (não o "Esperado" de quando o inventário foi criado) e grava um movimento do tipo
  **Ajuste** com a observação **"Inventário #N"**, que aparece no Kardex como origem; item não contado não é tocado; repetir a finalização não
  duplica; grava as observações finais no cabeçalho
  (`supabase/migrations/20260721170000_inventario_e_posicao_de_estoque.sql:257-300`).
- **"Cancelar inventário"** (menu da linha, só Aberto) **não pede confirmação** e muda o status para Cancelado; aviso "Inventário cancelado"
  (`InventoryCountsTab.tsx:246,336`, `hooks/useInventoryCounts.ts:240-266`, `inventory.ts:817`). Nada foi ajustado antes, então nada é desfeito.
- Não há como editar a lista de itens, reabrir ou apagar um inventário; o único caminho de volta de um ajuste é outro inventário ou um
  ajuste manual.
- **Permissões na finalização**: qualquer pessoa com a tela e o acesso ao local pode finalizar (seção 2); se a pessoa
  não tiver acesso a algum local do inventário, a finalização inteira falha com "Sem acesso a este local de estoque."
  (`supabase/migrations/20261013150000_customer_paid_expenses_and_customer_stock.sql:728-731`).

### 3.12 Aba "Posição de Estoque" (saldo numa data)

`components/inventory/StockPositionTab.tsx` (396 linhas), textos `inventory.ts:896-940`.
- **Barra de filtros**: abas de local ("Todos os locais" + um por local; só quando há mais de um) (`StockPositionTab.tsx:157-202`), busca
  **"Buscar material ou SKU..."** (também acha pelo nome do local), seletor de **data e hora** (já vem **agora**, hora do navegador, sem botão
  de limpar), botões **"Exportar"** (PDF / Excel) e **"Atualizar"**; trocar a data **recalcula sozinho** (a consulta é chaveada pela data) e "Atualizar" só recarrega (`StockPositionTab.tsx:72-89,204-268`, `hooks/useStockPosition.ts:31`, `inventory.ts:897-904`).
- **Dois cartões** quando há linhas: **"Valor em estoque (custo)"** e **"Projeção de venda"** (`StockPositionTab.tsx:270-290`, `inventory.ts:906-907`).
- **Tabela (desktop)**, cartão **"Posição de Estoque"**: **Local · SKU · Material · Un. · Saldo · Valor (custo) · Projeção venda**, mais a
  linha **"Total"** (`StockPositionTab.tsx:337-392`, `inventory.ts:909-916`). No celular, lista com "Local · saldo unidade" e o valor à direita
  (`StockPositionTab.tsx:293-335`). Vazio: **"Nenhuma posição"** ("Selecione uma data e atualize para ver o saldo do estoque.") ou, com filtro,
  "Nenhum item encontrado" (`StockPositionTab.tsx:299-305`, `inventory.ts:917-922`).
- **Como o número nasce** (`supabase/migrations/20261013150000_customer_paid_expenses_and_customer_stock.sql:163-205`): a função
  `get_stock_balance_at_date` **soma os movimentos do Kardex até a data e hora escolhidas**, por material e local, e mostra só o que tem saldo
  diferente de zero. **O valor usa o preço de custo (e o de venda) de hoje do cadastro**, não o de naquela data; materiais arquivados e o
  estoque exclusivo de clientes ficam de fora; respeita o acesso por local (`can_access_stock`). Hook `hooks/useStockPosition.ts:27-47`.
- **Para o roteiro**: o tutorial só consegue mostrar "o saldo mudou" se o Kardex tiver movimentos em **duas épocas** (por exemplo uma
  entrada de 40 dias atrás e outra recente) e se a data escolhida na gravação ficar entre elas. O seletor de data é o calendário padrão do
  sistema (entrada 1.36.16, `pages/Changelog.tsx:1395`).
- Histórico: aba de local e acesso por local entraram na 1.19.9, antes da 1.22.5 (`pages/Changelog.tsx:5343-5349`); o visual dos cartões
  mudou na 1.28.2 (`pages/Changelog.tsx:2646`).

### 3.13 Aba "Relatório" (compras por material)

`components/inventory/MaterialPurchaseReportTab.tsx` (437 linhas), textos `inventory.ts:941-972`; chegou na 1.36.12 como "Histórico e média paga por
material" (`pages/Changelog.tsx:1472`). **O título do cabeçalho diz "Relatório de estoque por material"** e o subtítulo "Compras, custo médio
pago, saldo e projeção comercial por material." (`MaterialPurchaseReportTab.tsx:316-320`, `inventory.ts:942`).
- **Topo**: seletor de período (**"Últimos 30 dias"**, **"Últimos 90 dias"**, **"Este ano"**, **"Todo o histórico"** [padrão],
  **"Personalizado"**; com data aparecem os campos "Data inicial" e "Data final"), botão **"Exportar"** (PDF / Excel) e botão redondo de
  **"Atualizar"** (`MaterialPurchaseReportTab.tsx:60,133,164-170,321-365`, `inventory.ts:945`).
- **Quatro cartões** (`MaterialPurchaseReportTab.tsx:367-372`, `inventory.ts:948`): **"Total comprado"** ("N compras no período"),
  **"Total vendido"** e **"Lucro bruto"** (ambos **desligados**, mostram "—", selo **PDV** e "Será calculado a partir das vendas do PDV."), e
  **"Projeção de lucro"** ("Com base no preço de venda cadastrado.", selo **"estimativa"**). Os dois ligados são clicáveis: "Total comprado"
  já vem **aberto** e mostra **"Ticket médio por compra"**, **"Materiais comprados"**, **"Maior quantidade comprada"**, **"Cobertura de
  preço"**, **"Quantidade por unidade"** e **"Distribuição de pagamentos"** ("Em aberto", "Não vinculado" ou a forma de pagamento; "Nenhum
  pagamento vinculado no período.") (`MaterialPurchaseReportTab.tsx:374-387`); "Projeção" abre a faixa amarela **"Projeção, não lucro
  realizado"** — "Venda projetada de R$ … e margem estimada de …%, usando os preços de venda cadastrados. Materiais sem preço de venda projetam
  margem zero." (`MaterialPurchaseReportTab.tsx:389-391`). Se algum item comprado não tinha preço, outra faixa avisa **"A cobertura de preço é N%.
  Itens sem preço não entram no custo médio."** (`MaterialPurchaseReportTab.tsx:393`).
- **Painel "Evolução do preço de compra"** (`components/inventory/MaterialPriceAnalysis.tsx`, entrada **1.38.0**, `pages/Changelog.tsx:132`; fotos na 1.38.1,
  `pages/Changelog.tsx:120`): subtítulo "Compare cada material com o próprio histórico de compras recebidas no Estoque e no PDV." Lista à esquerda
  **"Materiais — Selecione para analisar"** com **"Visão geral — Maiores altas e quedas"** no topo; à direita, **"Variações recentes de preço"**
  (selo "comparação equivalente"; cada material só se compara com a compra anterior **do mesmo item e da mesma unidade**) com **"Maiores altas"** e
  **"Maiores quedas"**; sem histórico: **"Histórico ainda insuficiente — São necessárias ao menos duas datas de compra do mesmo material para
  calcular altas e quedas."** Ao escolher um material: **"Último preço"**, **"Média do período"**, **"Menor preço"**, **"Maior preço"**,
  **"Variação"**, escala **"Por dia / Por semana / Por mês / Por trimestre"** (automática) e abas **"Preço médio"** e **"Volume comprado"**,
  nota "Média ponderada pela quantidade recebida; marcadores indicam períodos com compra.", botão "Voltar aos materiais" no celular
  (`MaterialPriceAnalysis.tsx:131-148,201-226,339-373,522,541`, `inventory.ts:949-969`).
- **Lista**: campo **"Buscar material, SKU ou grupo..."** com botão **"Filtros"** (Materiais, Fornecedores, Locais, Grupos, **"Responsáveis pela
  O.C."**, um quadro "Clientes — Disponível quando o PDV estiver ativo." e a caixa **"Ocultar materiais sem movimento no período"**, **ligada
  por padrão**) e o seletor **"Visualização": "Por material" | "Por grupo"** (`MaterialPurchaseReportTab.tsx:271-286,406-417`,
  `inventory.ts:946-948`). Tabela (largura mínima 1320 px): **Material** (ou Grupo) · **Última compra** · **Compras** · **Qtd. comprada** ·
  **Valor comprado** · **Média paga** · **Saldo atual** · **Qtd. vendida** · **Valor vendido** · **Lucro projetado**, rodapé **"Total das linhas
  visíveis"** e paginação (**10 / 25 / 50 por página**, "Exibindo 1–10 de N", Anterior/Próxima) (`MaterialPurchaseReportTab.tsx:428-434`,
  `inventory.ts:967-970`). Clicar na linha abre o **"Histórico de compras"** do material: data · fornecedor · "local · O.C. #N" ·
  responsável e situação do pagamento · "quantidade × preço" · total (`MaterialPurchaseReportTab.tsx:288-312`). Vazio: **"Nenhum resultado"** —
  "Não há compras no período. Desative “ocultar sem movimento” para ver todo o catálogo." (`inventory.ts:945`).
- **Preferências que o navegador lembra** (tentar com o navegador limpo para o vídeo): visualização, "ocultar sem movimento", itens por página e ordenação
  (chaves `inventory-purchase-report-view`, `-hide-zero`, `-page-size`, `-sort`) (`MaterialPurchaseReportTab.tsx:142-145`). O período **não** é lembrado
  e volta a "Todo o histórico".
- **Quais compras entram** (`supabase/migrations/20261018005000_compra_direta_estoque_financeiro.sql:669-907`): somente itens com quantidade
  **recebida** de ordens de compra **recebidas ou recebidas parcialmente** e as **compras diretas**, de requisições não canceladas, nos locais que a
  pessoa pode ver (`supabase/migrations/20261018005000_compra_direta_estoque_financeiro.sql:788-841`). **Entradas pela importação de NF-e, entradas rápidas, "Cadastro inicial" e ajustes de inventário não entram** (não
  têm ordem de compra). **"Média paga" = soma dos valores ÷ soma das quantidades que tinham preço**, no período (média ponderada histórica, não custo
  médio contábil do saldo atual); quantidade sem preço fica fora (`supabase/migrations/20261018005000_compra_direta_estoque_financeiro.sql:842-853`, `lib/material-purchase-report.ts:396-418`). "Saldo atual" é a soma dos
  saldos dos locais visíveis. "Projeção" = quantidade comprada × preço de venda cadastrado − valor comprado; sem preço de venda, a projeção é
  zero (`lib/material-purchase-report.ts:305-315`).
- **Pagamento no histórico**: compra direta mostra **Pago** (forma) ou **Em aberto**; **ordem de compra recebida só aparece como "Não vinculado"**,
  porque receber a O.C. não cria despesa (`supabase/migrations/20261018005000_compra_direta_estoque_financeiro.sql:809-814`, `MaterialPurchaseReportTab.tsx:227-232`, `inventory.ts:950`).
- Exportar baixa arquivo (seção 3.7 e seção 6). É no relatório que aparece a "média paga"; o ⚠️ da trilha sobre "estimativa
  histórica ponderada" bate com o código: a função é descrita como "média histórica ponderada paga" (`supabase/migrations/20261018005000_compra_direta_estoque_financeiro.sql:909-910`) e o arquivo exportado traz a
  nota "Valores de custo médio e projeção são estimativas; vendas reais dependem do PDV." (`inventory.ts:971`).

### 3.14 Consumo de estoque dentro da OS (fora desta tela, mas é o elo com a Área do Técnico)

Não é uma janela do Estoque. Vive na tela de execução da OS do técnico (T5/T7) e é **opcional da empresa**.
- **Liga** em Configurações → aba **Usabilidade** → seção **"Ordens de Serviço"** → chave **"Consumo de estoque na OS"** ("Permite que o técnico registre
  os materiais usados durante a ordem de serviço e dê baixa no estoque ao finalizar") (`pages/Settings.tsx:663-679,1684-1695`,
  `lib/i18n/messages/app/settings.ts:228-231`). Vem **desligada**; é decisão da empresa (vale para todos os aparelhos), guardada em
  `company_settings` (`hooks/useOsMaterials.ts:169-176`).
- **Com ela ligada**, o técnico ganha no menu de mais ações da OS o item **"Consumir do estoque"**, que abre a janela de mesmo nome:
  "Anote o que você usou. O estoque só baixa quando a OS for finalizada." Campos **"De onde saiu"** (local), **"Material"** (busca "Buscar por nome ou
  código…", grupos "Neste estoque" / "Outros materiais"), **"Quantidade"**, **"Observação (opcional)"**; botão **"Adicionar"**; lista **"Já registrado
  nesta OS"** com selos "Aguardando envio" / "Já baixado" (`pages/TechnicianOS.tsx:817,4495,4615,4920-4925`, `lib/i18n/messages/app/os.ts:1012-1075`).
  Mostra o saldo do local escolhido ("Tem 12 un neste estoque") e, se passar do saldo, avisa "Você está tirando mais do que tem neste estoque. Dá
  para continuar, o saldo vai ficar negativo."
- **Ao finalizar a OS** com materiais anotados abre o **"Resumo do consumo"** ("Confira o que saiu do estoque nesta OS. Dá para corrigir a quantidade
  antes de confirmar."), com **"Voltar"** e **"Confirmar e finalizar"** (`pages/TechnicianOS.tsx:1799-1812`, `OsConsumptionSummaryDialog.tsx`). A
  baixa vira movimentos do tipo **Consumo** no Kardex, com origem "OS #N". **Se a baixa falhar, a OS fecha mesmo assim** ("Não deu para baixar os
  materiais do estoque — A OS foi finalizada mesmo assim. O consumo continua anotado aqui e pode ser confirmado depois.") e **o estoque nunca impede
  fechar a OS** (1.23.0, `pages/Changelog.tsx:4577,4592`).
- **Sem a chave ligada**, concluir a OS **não baixa nada** (a trilha já avisa isso) e o item "Consumir do estoque" não existe.
- A gestão enxerga o que foi anotado na OS no bloco somente leitura **"Materiais utilizados"** ("Custo total", "Ainda não baixado do estoque") dentro
  da OS, da Agenda e do formulário da OS (`components/service-orders/OsMaterialsSection.tsx:22-85`, `ServiceOrderViewDialog.tsx:407`,
  `components/schedule/ScheduleDetailPanel.tsx:355`).
- Excluir um material que já foi usado numa OS é recusado, com a contagem de OS afetadas (1.23.0, `pages/Changelog.tsx:4602`; seção 5, P4).

---

## 4. Backend por tela e comparação com o fakebase

> "Fakebase" = servidor falso usado na gravação (`rec/fakebase`, esquema com 245 tabelas, 6 views e 375 funções em `rec/fakebase/schema.json`).
> Ele só responde chamadas **que já têm tabela/semente/handler**; função sem handler devolve **valor vazio do tipo certo** e anota
> `RPC_SEM_HANDLER` em `rec/fakebase/desconhecidos.log` (`rec/fakebase/core/log.mjs:23`). Ele aceita escrita genérica em qualquer tabela do
> esquema, mas **não roda gatilhos nem funções do banco**: tudo que o banco real faz sozinho (numerar, criar o local padrão, espelhar saldo) precisa de
> `hooks/<tabela>.mjs`, `handlers/rpc/<função>.mjs` ou `handlers/views/<view>.mjs` (`rec/fakebase/server.mjs:25-37`,
> exemplo de gatilho emulado em `rec/fakebase/hooks/equipment.mjs`).

### 4.1 O que cada tela lê e grava

| Tela / ação | Lê | Grava | Função (RPC) / serviço | Código |
|---|---|---|---|---|
| **Estoque Atual** (lista, abas de local, cartões) | `inventory`, `inventory_stock_levels`, `stocks`, `material_groups` | — | `get_accessible_inventory_ids` (**filtra a lista inteira**, seção 4.3) | `hooks/useInventory.ts:75-76,101-102`, `hooks/useStocks.ts:30-31`, `hooks/useMaterialGroups.ts:19-20`, `hooks/useAccessibleInventoryIds.ts:20`, `pages/Inventory.tsx:113,217` |
| Foto do material | arquivo no bucket privado `inventory-photos` (endereço assinado) | envio da foto | storage | `components/inventory/InventoryFormDialog.tsx:383-388`, `supabase/migrations/20261018162000_pdv_onda1_bucket_fotos_de_produto.sql` |
| **Novo/Editar material** | — | `inventory` (insere/atualiza), mínimo por local em `inventory_stock_levels`, grupo novo em `material_groups` | `register_inventory_movement` ("Cadastro inicial" / "Ajuste manual"), `set_inventory_presence` | `hooks/useInventory.ts:156-175,199,286-377` |
| **Entrada / saída rápida** | — | — | `register_inventory_movement` | `hooks/useInventory.ts:267` |
| **Transferir entre locais** | — | — | `transfer_stock_between` | `hooks/useStocks.ts:156` |
| **Configurações** (grupos e locais) | `material_groups`, `stocks` | cria, renomeia, ordena, apaga grupos e locais | `set_default_stock` (local principal) | `hooks/useMaterialGroups.ts:35-92`, `hooks/useStocks.ts:60-135` |
| **Configurar local** (itens, acesso, tipo) | acesso do local | grupo/itens no local, restrição, tipo (operacional/PDV) | `add_group_to_stock`, `set_stock_materials`, `get_stock_access`, `set_stock_access` | `hooks/useInventory.ts:222,242`, `hooks/useStockAccess.ts:39,52`, `hooks/useStocks.ts:121` |
| **Excluir material** | uso em OS e orçamentos (`service_materials`, `quote_items`) | apaga movimentos e o material | — | `hooks/useInventory.ts:397-414` |
| **Kardex** | `inventory_movements`, e em consultas separadas `inventory`, `profiles`, `suppliers`, `service_orders`, `stocks` | — | — | `hooks/useInventoryMovements.ts:58-160` |
| **Compras** (lista) | `compras`, `compra_materiais`, `compra_cotacoes`, `compra_cotacao_precos`, `compra_ordens`, `compra_ordem_itens`, `suppliers`; aviso de mínimo vem da view `inventory_low_stock` | — | — | `hooks/useCompras.ts:68-107`, `hooks/useLowStock.ts:37` |
| **Requisição / cotação / O.C.** | as mesmas | `compras` (número vem de gatilho), `compra_materiais`, `compra_cotacoes`, `compra_cotacao_precos`, `compra_ordens` (número, autor e envio vêm de gatilho), `compra_ordem_itens` | — | `hooks/useCompras.ts:206-348`, `hooks/useCompraCotacoes.ts:82-236`, `hooks/useCompraOrdens.ts:164-349`, `supabase/migrations/20260930110000_compras_ordem_de_compra.sql:313-357` |
| **Receber O.C.** | — | — | `receber_ordem_compra` | `hooks/useCompraOrdens.ts:384` |
| **Compra direta** | contas financeiras ativas, categorias | — | `registrar_compra_material_direta` (compra + ordem + entrada + despesa, numa transação) | `hooks/useDirectMaterialPurchase.ts:58`, `supabase/migrations/20261018005000_compra_direta_estoque_financeiro.sql:431-507` |
| **Fornecedores** | `suppliers` | `suppliers` | — | `hooks/useSuppliers.ts:33-88` |
| **Importar XML (NF-e)** | `nfe_imports` (aviso de duplicidade) | `suppliers`, `inventory`, `nfe_imports` | `register_inventory_movement` (sem local: vai ao padrão) | `hooks/useNfeImport.ts:55,92,131,148,180` |
| **Inventários** | `inventory_counts`, `inventory_count_items` (com `inventory`, `stocks`), view `inventory_count_divergences` | cabeçalho, locais, itens; contagem de cada item; status | `finalize_inventory_count` | `hooks/useInventoryCounts.ts:32-244`, `supabase/migrations/20260721170000_inventario_e_posicao_de_estoque.sql:118-146,206-319` |
| **Posição de Estoque** | — | — | `get_stock_balance_at_date` | `hooks/useStockPosition.ts:33` |
| **Relatório** | usuários (`profiles`), fornecedores, locais, grupos | — | `get_material_purchase_report` | `hooks/useMaterialPurchaseReport.ts:68` |
| **Consumo na OS** (fora da tela) | `service_order_materials`, `inventory`, `stocks` | idem | `commit_os_material_consumption` | `hooks/useOsMaterials.ts:207-233,298,456` |

**Serviços externos (hosts)**: nenhum. Estoque, compras, NF-e (a nota é lida no navegador) e inventário só falam com o banco e o armazenamento. Não há
função de borda nem canal em tempo real nesta área (`grep` em `components/inventory`, `pages/Inventory.tsx` e nos hooks acima: só `storage` em
`InventoryFormDialog.tsx:383-388`).

### 4.2 O que o fakebase tem hoje para o T8

- **Esquema**: todas as tabelas, as 2 views do estoque e as 14 funções do T8 existem em `rec/fakebase/schema.json`. **A gravação genérica (inserir/atualizar/apagar) funciona** nelas.
  As funções constam no esquema (conferido por nome, inclusive `transfer_stock_between`, `get_accessible_inventory_ids` e `commit_os_material_consumption`).
- **Sementes**: **nada de estoque**. As sementes de base (`gen-01-tenant`, `gen-02-cadastros`) só trazem `company_settings` e **4 fornecedores**
  (Polar Distribuidora de Peças, Gelo Norte Componentes, Cobre Sul Suprimentos, Distribuidora Aurora de Peças); as do T3 acrescentam Ventura Gás e Tubos
  (`rec/fakebase/seeds/gen-02-cadastros.json`, `rec/fakebase/seeds-extra/t3/apos-cap07.json`). Não há `stocks`, `inventory`, `inventory_stock_levels`,
  `inventory_movements`, `material_groups`, `compras*`, `inventory_counts*`, `nfe_imports`.
- **Handlers**: só existem 3 funções com handler (`get_customer_portal_settings`, `get_lead_capture_form`, `save_customer_portal_settings`)
  (`rec/fakebase/handlers/rpc`). **Nenhuma função do estoque tem handler.** Não existe a pasta `handlers/views`.
- **Gatilhos emulados** (`rec/fakebase/hooks`): só `customers`, `equipment` e `lead_capture_forms`.

### 4.3 Lacunas a fechar antes de gravar (lista para quem for montar o ambiente)

1. **CRÍTICA, `get_accessible_inventory_ids`**: sem handler ela devolve lista vazia e a tabela **"Estoque Atual" aparece sem nenhum material**, mesmo com sementes
   (`pages/Inventory.tsx:113,217`; os seletores de material das janelas também usam, `components/inventory/InventoryMaterialSelect.tsx:54-58`). O handler
   deve devolver os ids dos materiais da empresa (regra do banco: presentes em algum local acessível ou sem presença configurada,
   `supabase/migrations/20261013150000_customer_paid_expenses_and_customer_stock.sql:137-160`).
2. **Sementes** (mundo da Glacial Cold Brasil): `stocks` (o padrão **"Estoque Principal"**, com `is_default = true`, mais 1 ou 2 locais, por exemplo uma van),
   `material_groups`, ~10 a 14 `inventory` (nome, SKU `EST-00N`, unidade, custo e preço de venda), **`inventory_stock_levels` por material × local com mínimo e
   `is_present`**, e `inventory.quantity` igual à soma dos saldos (o banco mantém esse espelho por gatilho: `supabase/migrations/20260930100000_estoque_presenca_materializa_ausencia.sql:35`).
   `inventory_movements` coerentes com os saldos (`stock_before` + `quantity` = `stock_after`), **datas dentro do mês da data congelada** (o Kardex abre em "este mês") e
   **ao menos uma entrada bem mais antiga** (Posição de Estoque e evolução de preço). Para a evolução do preço: pelo menos 2 datas de compra do mesmo material.
   Para o Relatório: `compras` + `compra_ordens` + `compra_ordem_itens` recebidos (com `quantity_received`, `unit_price`).
   Para Compras: 1 requisição em rascunho/cotação, 1 O.C. enviada para a cena de recebimento; para Inventários: opcionalmente 1 inventário finalizado de exemplo.
3. **Handlers de função** (os que as telas chamam ao clicar): `register_inventory_movement`, `transfer_stock_between`, `set_inventory_presence`,
   `add_group_to_stock`, `set_stock_materials`, `set_default_stock`, `get_stock_access`, `set_stock_access`, `finalize_inventory_count`,
   `receber_ordem_compra`, `registrar_compra_material_direta` (só se a cena confirmar a compra direta), `get_stock_balance_at_date`,
   `get_material_purchase_report`. Todas **calculam coisas** (saldo antes/depois, soma de movimentos até a data, média ponderada); não basta devolver vazio.
4. **Views**: `inventory_low_stock` (aviso de mínimo em Compras e janela "abaixo do mínimo" da requisição) e `inventory_count_divergences` (aba "Divergências"),
   como `handlers/views/<nome>.mjs` (`rec/fakebase/server.mjs:34-36`).
5. **Gatilhos emulados** (`hooks/<tabela>.mjs`): `compras.numero`, `compra_ordens.numero` (com autor e data de envio), `inventory_counts.numero` e
   `inventory_count_items.diff` (coluna calculada: contado − esperado). O local **"Estoque Principal"**, que o banco cria sozinho
   (`supabase/migrations/20260721210000_ensure_default_stock.sql`), tem de vir na semente. Se a cena criar um local novo, basta a gravação genérica; as
   travas de não apagar o padrão nem o último local ficam no banco (`supabase/migrations/20260721160000_multi_estoque_e_grupos_material.sql:150-188`).
6. **Arquivo da nota**: um XML de NF-e **fictício** (CNPJ e razão social do fornecedor da semente, 3 a 5 produtos, uma chave de 44 dígitos que não esteja em
   `nfe_imports`) na pasta do roteiro; o passo `upload` do gravador clica no botão que abre o seletor de arquivos e entrega o arquivo
   (`rec/recorder/runner.mjs:535-555`). O botão é "Escolher arquivo XML" (seção 3.10).
7. **Armazenamento**: o fakebase só tem o bucket `company-logos` (`rec/fakebase/storage`). Foto de material pede o bucket `inventory-photos`; sem ele a lista
   mostra o ícone alternativo (1.37.55, `pages/Changelog.tsx:171`). **Combinar com o Kaik** se o vídeo mostra foto.
8. **Downloads não existem para o gravador** (`rec/recorder/runner.mjs`: não há passo de download): "Exportar" PDF/Excel (estoque, inventário, posição, relatório) e o
   PDF da ordem de compra **não podem aparecer como arquivo baixado**; a cena mostra o menu e o aviso, não o arquivo (pontos 5 a 8 do `TRILHA.md`).
9. **Largura**: a tabela do Kardex só aparece a partir de 1280 px (abaixo, cartões); o gravador usa janela de 1280×800 pixels de tela (CSS) em escala 2, quadros de 2560×1600 (`rec/recorder/browser.mjs:1,12`), então a tabela **aparece**. O **Relatório** tem tabela de largura mínima de 1320 px dentro de um cartão que rola (`components/inventory/MaterialPurchaseReportTab.tsx:428`): com o menu lateral aberto, as últimas colunas (a 6ª, "Média paga", já fica no limite) podem sair da vista; planejar rolagem horizontal ou menu recolhido (estado "recolhido" em `components/layout/SidebarMenuContent.tsx:253-258`; a confirmar rodando).

---

## 5. Pegadinhas

`[handoff]` = comportamento que parece defeito ou texto desatualizado do app, para o time de produto decidir; **não corrigi nada**.

| # | O que acontece | Efeito no tutorial | Código |
|---|---|---|---|
| P1 | **Importar XML (NF-e) entra sempre no local principal**, sem escolher o local; não cria compra, despesa nem lançamento no Relatório; não guarda o XML | Dizer "dá entrada no estoque principal"; para outro local, usar a transferência | `hooks/useNfeImport.ts:148-155`, seção 3.10 |
| P2 | **`fn:manage_inventory` ("Gerenciar Estoque") não trava nenhum botão da tela**; só vale para compra direta e estoque do cliente `[handoff]` | Nunca dizer que a tela pede essa permissão | `hooks/usePermissions.ts:109`, `components/customers/CustomerStockTab.tsx:264`, seção 2 |
| P3 | **"Restrito" sem marcar ninguém** grava lista vazia e o local **continua aberto a todos** (zero linhas = aberto) | Na cena, marcar pelo menos uma pessoa (Rafael Lima) antes de salvar | `components/inventory/StockConfiguratorDialog.tsx:455-525`, `supabase/migrations/20260814225028_stock_access_acl.sql:41-65` |
| P4 | **Excluir material apaga o Kardex dele** (todas as movimentações) e desvincula serviços e orçamentos; só recusa quando está lançado em OS | Não excluir material com histórico na gravação | `hooks/useInventory.ts:384-436` |
| P5 | **Salvar o material sem nome** não é barrado pela tela: o erro vem do banco, em texto técnico `[handoff]` | Preencher sempre o nome; não mostrar este erro | `components/inventory/InventoryFormDialog.tsx:242-331,426` |
| P6 | Nota da cotação aceita: **"Aceitar não mexe no estoque. Use "Registrar entrada" quando o material chegar."** está desatualizada: hoje o caminho é "Registrar recebimento" na O.C. enviada `[handoff]` | O vídeo não deve ler esta frase; falar do fluxo real | `components/inventory/CompraDetailView.tsx:416-421`, `inventory.ts:673` |
| P7 | Material criado pela NF-e guarda o fornecedor **só como texto antigo**: ao editar, o campo Fornecedor vem vazio com "Antes estava escrito…" | Se a cena abrir o material criado pela nota, mostrar a frase, ou escolher outro material | `components/inventory/InventoryFormDialog.tsx:604-612` |
| P8 | No inventário, **"Esperado" é congelado na criação** e a divergência mostrada usa ele, mas o **ajuste usa o saldo de agora** | Não mexer no estoque entre criar e finalizar; não prometer "trava o estoque durante a contagem" | `supabase/migrations/20260721170000_inventario_e_posicao_de_estoque.sql:262-282` |
| P9 | A contagem é montada a partir das **linhas de saldo** dos locais: entra material marcado como ausente do local (esperado 0) e **não entra** material que nunca teve movimento ou configuração ali `[handoff]` | Semear saldo (mesmo zerado) para todo par material × local que deve aparecer; conferir rodando | `hooks/useInventoryCounts.ts:114-131` |
| P10 | **"Cancelar inventário" não pede confirmação** `[handoff]` | Não clicar por engano; só cancelar de propósito (e talvez nem mostrar) | `components/inventory/InventoryCountsTab.tsx:246,336` |
| P11 | **Nenhuma entrada (NF-e, O.C., compra direta) atualiza o "Custo Unit." do cadastro**: "Valor investido" e a Posição usam o custo e o preço de venda **de hoje** do cadastro; o preço pago só fica no movimento e no Relatório | Cuidado ao dizer "o custo se atualiza sozinho" | `hooks/useStockPosition.ts:33`, `supabase/migrations/20261013150000_customer_paid_expenses_and_customer_stock.sql:163-205` |
| P12 | Receber uma O.C. **em rascunho** é aceito pelo servidor (só a O.C. cancelada é recusada); a tela só oferece "Registrar recebimento" para enviada ou recebida parcial `[handoff, segurança baixa]` | Mostrar somente o caminho da tela | `supabase/migrations/20260930110000_compras_ordem_de_compra.sql:598-599`, `components/inventory/CompraDetailView.tsx:459` |
| P13 | Código e textos sem uso: estado `inventoryTab`/`openNewPurchase`, lista fixa de categorias, cartão "Projeção venda" da tela principal, título "Histórico de Movimentações" `[handoff]` | Não descrever nada disso | `pages/Inventory.tsx:105-107,150-157`, `inventory.ts:26,114,481-489` |
| P14 | **Dependência do relógio**: a Posição abre em "agora" e o Kardex em "este mês"; o Relatório abre em "Todo o histórico" | Data do navegador congelada (item 5 do `TRILHA.md`) e movimentos semeados dentro do mês | `components/inventory/StockPositionTab.tsx:72`, `components/inventory/InventoryKardexTab.tsx:231` |
| P15 | **Evolução do preço** só mostra altas e quedas com **2 ou mais datas de compra** do mesmo material e unidade | Semear compras recebidas em datas diferentes | `inventory.ts:960` |
| P16 | **Quem vê as abas vê todas**; mas a compra direta some para quem não administra estoque e financeiro, e o Relatório e a Posição respeitam o acesso por local | A Camila (admin) vê tudo; ⚠️ falado como permissão, não bug | `hooks/useCanRegisterDirectMaterialPurchase.ts:8-15` |
| P17 | **Segurança, entre pessoas da mesma empresa** `[handoff, segurança baixa]`: a política da tabela `inventory` é "tudo para a empresa" e a chave `fn:manage_inventory` só é conferida para estoque de cliente; qualquer usuário da empresa grava materiais pela API. O saldo, em compensação, só muda pelas funções (guarda de 18/10) | Nenhum efeito no vídeo | `supabase/migrations/20260418163700_*.sql:136-140`, `supabase/migrations/20261018164000_estoque_saldo_so_muda_pelo_kardex.sql` |

**Achados de segurança novos**: nenhum que cruze empresas. P2, P12 e P17 são só entre pessoas da mesma empresa e de gravidade baixa. Os achados já conhecidos da
`TRILHA.md` (presets sem `company_id`, modo legado sem permissões, contadores de NFS-e) não tocam esta tela.

---

## 6. 🚫 Não prometer / telas mortas

- **"A NF-e monta a compra sozinha"** (trilha, cap. 8): falso hoje; só dá entrada, cria o fornecedor se for novo e anota a nota como importada (P1).
- **Importar materiais por planilha**: não existe (a única importação é o XML da NF-e). Exportar PDF/Excel existe, mas não pode aparecer como arquivo baixado no vídeo.
- **Vendas, lucro realizado e margem real no Relatório**: só quando houver venda real do PDV; "Total vendido" e "Lucro bruto" ficam desligados; "Projeção de lucro" é estimativa (`inventory.ts:948`).
- **"Aceitar a cotação dá entrada no estoque"**: não dá. Também não existe mais "cotação vencedora" única: o fornecedor é escolhido **por material** e se gera **uma O.C. por fornecedor** (1.28.10, `pages/Changelog.tsx:2490`).
- **"Receber a O.C. lança a despesa"**: não lança. Só a **compra direta** cria a despesa no Financeiro; O.C. recebida aparece no Relatório como "Não vinculado".
- **"Concluir a OS baixa o estoque"**: só se a empresa ligar "Consumo de estoque na OS" **e** o técnico tiver anotado materiais; se a baixa falhar, a OS fecha mesmo assim (seção 3.14).
- **"Categoria" no cadastro** e a lista "Peças, Filtros, Gases…" do Guia Técnico: não existem (seção 0.4, D1). O que existe é **Grupo**.
- **Cartão "Projeção venda" na tela principal**: removido na 1.17.25; a projeção só vive na Posição e no Relatório.
- **"A média paga é o custo médio do estoque"**: não é; é média ponderada **histórica** do que foi pago em compras recebidas no período.
- **Inventário finalizado desfaz**: não desfaz, não reabre, não edita; também **não bloqueia** o estoque durante a contagem (P8).
- **Foto do material**: só prometer se o ambiente tiver o armazenamento `inventory-photos` (seção 4.3, item 7).
- **Valores de planos da Dominex**: fora do vídeo (regra "sem preços"); valores do **mundo fictício** (peças, fornecedores) podem aparecer.

---

## 7. Dúvidas em aberto

1. **(a confirmar rodando)** A janela "Importar XML (NF-e)" abre como janela no desktop e como gaveta no celular (`components/ui/ResponsiveModal.tsx`); o XML fictício precisa passar no leitor
   (`infNFe`, `emit`, `det/prod`, chave de 44 dígitos). Testar o arquivo e o passo `upload` antes do roteiro final.
2. **Decisão do Kaik**: com o módulo PDV ligado (mundo fictício com todos os módulos), a barra de locais mostra o subtítulo "Operacional" mesmo sem nenhum local de loja
   (`pages/Inventory.tsx:121-131,692-742`). O roteiro pode ignorar o rótulo ou explicar "Loja × Operacional" em uma frase; o tutorial do PDV é outro assunto.
3. **(a confirmar)** Seletor de data da Posição: ao escolher um dia no calendário, a hora fica 00:00 ou a atual? Muda se movimentos "de hoje" entram na posição escolhida
   (`components/inventory/StockPositionTab.tsx:72-89`).
4. **(a confirmar)** Compra direta na gravação: exige conta financeira ativa que não seja cartão e categoria de despesa; **o fakebase não tem `financial_accounts` nem
   `financial_categories`** (só `tenant_payment_accounts`), então a cena depende da semente do T13 ou de uma semente própria.
5. **(a confirmar)** No detalhe do inventário a lista inteira aparece sem paginação (`components/inventory/InventoryCountDetailModal.tsx:310-381`): com muitos itens a janela rola; definir o escopo da cena (um grupo ou poucos itens).
6. **Decisão do Kaik**: duração. A trilha prevê ~43 min em 11 capítulos; o perfil Domiflix costuma ficar mais curto (ver `plano.md`).
7. **Decisão do Kaik**: mostrar foto de material (exige armazenamento no fakebase) e mostrar o aviso "Nota já importada" (é fluxo normal, mas pede importar a mesma nota duas vezes).
8. **(a confirmar)** Depois de montar as sementes, rodar uma navegação completa e ler `rec/fakebase/desconhecidos.log` para achar função, tabela ou view faltando que a leitura estática não mostrou.
