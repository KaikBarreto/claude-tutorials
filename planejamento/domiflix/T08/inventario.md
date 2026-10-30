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

@@SECAO0@@

---

## 1. Rotas e navegação

| Endereço (pt-br) | O que abre | Código |
|---|---|---|
| `/estoque` | Tela "Estoque" (subtítulo "Controle de peças e materiais"), sempre na aba "Estoque Atual". Tradução do endereço: en `/inventory`, es `/inventario`, fr `/stock` | `App.tsx:806`, `lib/i18n/appRouteSlugs.ts:57,138`, `lib/i18n/messages/app/inventory.ts:8-11` |
| (sem endereço próprio) | As 6 abas **não têm URL**: a aba ativa é estado local da página. Só entra em outra aba por clique | `pages/Inventory.tsx:150,1067-1082` |
| `state.inventoryTab` / `state.openNewPurchase` | Um atalho interno (estado de navegação) poderia abrir a aba e já a janela "Nova Requisição de Compra", mas **nenhum outro arquivo envia esse estado hoje**: o botão de compra do PDV vai para `/pdv/compra` (tela do PDV) | `pages/Inventory.tsx:105-107,150-157,1072`, `pages/PdvCaixa.tsx:859`, `lib/i18n/appRouteSlugs.ts:148` |

- **Como se chega:** Menu lateral "Estoque" (grupo Operacional, `components/layout/SidebarMenuContent.tsx:118`), menu
  superior (`components/layout/TopNavbar.tsx:108`), menu "Mais" do celular (`components/layout/MoreMenuDrawer.tsx:104`),
  atalho de teclado **Shift+I** (`hooks/useKeyboardShortcuts.ts:24`). Título da aba do navegador "Estoque"
  (`hooks/usePageTitle.ts:18`); mensagem de carregamento "Calculando estoque..." (`hooks/useRouteLoadingMessage.ts:35`).
- **Seis abas na horizontal, em todas as larguras** (`pages/Inventory.tsx:591-598`): "Estoque Atual", "Histórico de
  Materiais (Kardex)", "Compras de Material", "Inventários", "Posição de Estoque", "Relatório"
  (`lib/i18n/messages/app/inventory.ts:12-22`). No **celular** três nomes encurtam: "Histórico", "Compras", "Posição"
  (`inventory.ts:14,16,19`).
- **Dentro da aba "Estoque Atual"** há uma segunda camada: uma aba por **local** quando a empresa tem mais de um (sublinhadas
  no desktop, pílulas no celular), mais uma aba "Todos"? Não: só os locais que a pessoa pode ver (seção 3.2;
  `pages/Inventory.tsx:296-387,692-744`).
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
| Ver o item de menu e abrir `/estoque` | Permissão de tela `screen:inventory` ("Estoque": "Materiais, saldos e movimentações de estoque.", grupo Operacional) | `hooks/usePermissions.ts:67`, `App.tsx:806`, `SidebarMenuContent.tsx:118` |
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
