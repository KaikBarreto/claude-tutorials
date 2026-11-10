# Inventário · T4 Clientes, fornecedores e a ficha do parceiro (EcoSistema 1.59.154)

Levantado em 10/11/2026 no código gravado (`/home/claude/ecoflix/app-src-1.59.154/`, só leitura). Caminhos relativos a
`src/`, exceto `supabase/...`. Rótulos entre aspas = texto exato da tela. Gravação em 1280×800: a altura ≤ 820 px liga o
modo compacto da tela (`[@media(min-width:768px)_and_(max-height:820px)]`): some o subtítulo da página e, na lista, os
selos ficam só com o ícone (o texto vai para o leitor de tela; o tooltip continua).

## 0. O que a fonte diz × o que o código faz (vale o código)
| Fonte | Código 1.59.154 | Como a aula trata |
|---|---|---|
| "A ficha do parceiro e suas 5 abas" (Histórico de Pedidos, Conta-Corrente, Lucro Estimado, Despesas & Receitas, Notas Fiscais) | Clicar no parceiro na lista abre a ficha **ao lado da lista**, com 7 abas: "Visão geral", "Pedidos", "Conta-corrente", "Lucro estimado", "Financeiro", "Notas fiscais", "Preços" (`components/clients-suppliers/ClientsListView.tsx:220-230`). As 5 abas da fonte são as da página `/cliente/:slug` (`pages/PartnerDetail.tsx:277-294`), que só abre pelo olho do "Relatório de Saldos", pelo ranking da "Visão geral" ou por link antigo; o botão "Ficha" do cartão não aparece mais (`renderEntityCard` não é chamado, `pages/ClientsSuppliers.tsx:1056`) | capítulos 7 a 11 na ficha ao lado da lista, com os rótulos dela; a página cheia aparece só no fim do cap. 12 (olho do relatório) |
| Selo "Duplicado" casa pelo telefone | "Duplicado" (vermelho) = mesmo CPF/CNPJ; mesmo telefone sozinho = selo leve "Mesmo telefone" (tooltip "Mesmo telefone em outro cadastro"), "Isso é só um aviso, não trava nada." (`components/clients-suppliers/PartnerDuplicateBadge.tsx:39-99`); a busca acha os dois pelo número (`utils/partnerSearch.ts:28-43`) | dica no cap. 1 com o "Mesmo telefone" e a busca pelo número |
| 🚫 "Nomenclatura do sistema não muda nunca" | Existe "Inverter os termos Cliente e Fornecedor" em Configurações › Usabilidade (`components/settings/SettingsUsabilityContent.tsx:446`) | a fala só define cliente e fornecedor, sem dizer que nunca muda; a opção fica fora (não está na fonte) |
| "Só o Nome já gera histórico, saldo e portal" | bate; o portal é do módulo `portal_cliente` (aba "Portal" mostra a contratação sem ele, `components/EntityFormDialog.tsx:1918-1919`) | dica do cap. 4 fala de histórico e saldo; o portal entra no cap. 7 como "depende do plano" |

## 1. Rota e menu
- Menu lateral "Clientes e Fornecedores" (ícone de aperto de mão), item solto, sem grupo (`config/routes.ts:476`).
  Rota `/clientes-fornecedores` (`App.tsx:436-440`), permissão `screen_clientes_fornecedores`.
- Ficha cheia: `/cliente/:slug`, `/fornecedor/:slug` (`App.tsx:443-448`); `/balance/:type/:id` → `/saldo/...` →
  `/cliente/<nome>-<código>?tab=conta-corrente` (`App.tsx:686`, `:95-134`, `:458-460`).
- Recolher o menu: botão de ícone sem rótulo no topo, à esquerda (`components/layout/AppLayout.tsx:104-111`).

## 2. Tela Clientes e Fornecedores (`pages/ClientsSuppliers.tsx`)
- Título "Clientes e Fornecedores" (subtítulo "Gerencie seus clientes, fornecedores e tabelas de preços" some em
  1280×800), botões "Ver tutorial" e "Como funciona?" (`:1305-1323`).
- Abas "Clientes", "Fornecedores", "Visão geral" (`:193-197`). À direita: "Configurações" (etiquetas e campos, fora da
  aula), "Importar da Matriz" (só com grupo de empresas: não aparece), "<n> incompletos" / "Mostrar todos" (só ≥ 1280 px
  e com pendente na aba), "Relatório", "Novo Cliente" / "Novo Fornecedor" (`:1339-1399`).
- Lista + ficha (`components/clients-suppliers/ClientsListView.tsx`): à esquerda "Clientes"/"Fornecedores" com a
  contagem (`:596-599`); busca "Buscar cliente..." / "Buscar fornecedor..." (nome, apelido, código, CPF/CNPJ ou telefone)
  com "Filtros" ("Situação do saldo": "Todos", "Com saldo", "Saldo zerado"; "Etiquetas") e "Ordenar" ("Código", "Nome",
  "Saldo", "CPF/CNPJ", "Telefone") (`:601-669`, `:116-122`). Cada linha: "código · nome", CPF/CNPJ (ou telefone, ou "Sem
  documento ou telefone"), selos e o saldo em etiqueta colorida; menu "..." com "Editar", "Excluir", "Portal do
  Fornecedor", "Nova Movimentação" (`:673-726`, `:124-166`). Sem seleção: "Selecione um fornecedor" / "Escolha um cadastro
  na lista para consultar informações, movimentações, documentos e preços." (`:759-771`).
- Selos da linha: "Cliente+Fornecedor" (roxo, texto visível), aptidão fiscal (ícone verde, tooltip "Pronto para emitir
  NF-e"; ou triângulo âmbar "Incompleto", tooltip "Faltam dados para emitir NF-e para este cadastro:" + a lista,
  "Abra o cadastro do parceiro e preencha esses campos.", "...o selo é só um aviso e não trava venda, compra nem nada.")
  (`components/clients-suppliers/PartnerFiscalBadge.tsx:44-92`), duplicidade (acima). Campos que a régua exige: CPF/CNPJ,
  Logradouro, Número, Bairro, Cidade, UF, CEP, Código IBGE; telefone só se preenchido (`lib/nfe/partnerFiscalReadiness.ts:68-77`).
- Cor do saldo (`utils/balanceFormatting.ts`): cliente positivo verde, negativo vermelho; fornecedor positivo vermelho,
  negativo verde; zero cinza escuro. Texto curto embaixo: "a receber", "a pagar", "quitado" (`i18n/.../clients.json:2-6`);
  tooltip "<nome> te deve" / "Você deve a <nome>" / "Saldo zerado". Parceiro duplo: o saldo é um só (linha `party`, na
  convenção do cliente); na aba Fornecedores o sinal aparece invertido e a cor é a mesma (`ClientsSuppliers.tsx:263-289`).
- Backend: `customers`, `suppliers`, `balances`, `entity_custom_prices` (contagem), `entity_labels`,
  `entity_custom_field_definitions`, `price_tables` (selects).

## 3. Visão geral da tela (`components/clients-suppliers/EntitiesSummaryTab.tsx:566-797`)
Filtro de período, "Relatório de Saldos", "Ranking do período" ("Clientes por venda", "Fornecedores por compra",
"Exportar"), "Concentração de vendas" / "Concentração de compras", "Saldos de clientes" e "Saldos de fornecedores"
("<n> a receber", "<n> a pagar"), "<clientes|fornecedores> sem venda/compra no período". RPC `get_financial_dre_summary`
e as de ranking/inativos (só leitura; a aula só passa por ela).

## 4. Janela Novo/Editar (`components/EntityFormDialog.tsx`)
- Título "Novo Fornecedor" / "Editar Fornecedor" (`:1191`); abas "Dados de Contato", "Dados Fiscais", "Portal" (`:1212-1225`);
  rodapé "Cancelar", "Salvar" ("Salvando...") e, em parceiro duplo, "Desvincular" (`:1163-1185`).
- **Dados de Contato** (`:1227-1360`): "Identificação e contato": "Nome *" (placeholder "Nome fantasia"), "Pessoa de Contato
  ou Apelido", "Telefone" ("(00) 00000-0000"), caixa "Não possui telefone", "Mostrar o telefone no comprovante", "E-mail";
  "Recebimento": "Chave PIX", "Mostrar a chave PIX no comprovante"; "Tabela de Preços Padrão" (só com tabela de preço e a
  preferência de várias tabelas ligada; seletor com "Principal" ★ e "Buscar tabela...", `components/PriceTableSelector.tsx:36-80`),
  "Etiqueta"; "Dados bancários".
- **Dados Fiscais** (`:1442-1915`): "Informações Tributárias": "Tipo de Pessoa" ("Pessoa Física" | "Pessoa Jurídica"),
  "CPF" ou "CNPJ" (com a lupa só em PJ), "Nome Fantasia", "Mostrar CPF/CNPJ no comprovante", "Razão Social", "Inscrição
  Estadual" (" *" quando contribuinte), "Indicador IE *" ("Contribuinte ICMS", "Isento de Inscrição", "Não Contribuinte";
  "Contribuinte ICMS exige Inscrição Estadual; Isento/Não Contribuinte não."), "Regime tributário do fornecedor" ("Não
  informado", "Simples Nacional", "MEI", "Lucro Presumido", "Lucro Real"; depois da busca: "Preenchido pela consulta do
  CNPJ: a Receita informa que esta empresa é optante pelo Simples Nacional."; "É o regime de quem vende para você, não o
  da sua empresa..."). Só cliente: "É Indústria", "É uma Reciclagem". "Endereço Fiscal" ("Dados obrigatórios para emissão
  de notas fiscais"): "CEP" (busca sozinha com 8 dígitos), "Estado", "Cidade", "Logradouro", "Número", "Bairro",
  "Complemento", "Mostrar endereço no comprovante".
- **Campo vermelho** (`:758-764`, `:1790-1891`): só depois de uma busca de CNPJ, campo de endereço que a Receita não
  trouxe ganha embaixo, em vermelho, "Não veio da Receita — obrigatório para emitir NF-e" ("Obrigatório para emitir NF-e"
  no CEP); some quando o campo é preenchido.
- **Busca pelo CNPJ** (`components/CnpjLookupInput.tsx:85-157`): lupa à direita do CNPJ, title "Buscar dados da empresa pelo
  CNPJ" (aria "Buscar dados pelo CNPJ"), só com CNPJ válido; toast "Dados preenchidos — confira antes de salvar". Preenche
  razão social, nome fantasia e endereço; nome, telefone e e-mail só se estiverem vazios; o regime só quando a Receita
  afirma o Simples ou o MEI (`:714-752`). Edge `cnpj-lookup` (`utils/cnpjLookup.ts`, `supabase/functions/cnpj-lookup/index.ts:124-188`):
  `{success, data:{razao_social, nome_fantasia, logradouro, numero, complemento, bairro, cidade, uf, cep, phone, email,
  opcao_pelo_simples, opcao_pelo_mei}}`. Cidade casa com a lista da edge `ibge-cities` (`components/CitySelector.tsx`).
- Abaixo das abas (menos em Portal): caixa "Também é cliente" / "Também é fornecedor" ("Cria ou vincula também o cadastro
  de cliente.") (`:2253-2271`); "Saldo inicial" ("Comece com saldo zero ou registre um saldo de abertura.", "+ Adicionar saldo
  inicial", "Tipo de saldo", "Valor"); em edição, "Saldo" + "Alterar saldo" (`:2274-2398`). Parceiro duplo em edição: aviso
  azul "Mudanças em nome, CPF/CNPJ, contato, endereço e tabela de preços padrão refletem automaticamente no cadastro de
  cliente vinculado." (`:1198-1209`).
- Ao salvar: toasts "Fornecedor cadastrado com sucesso!", "Fornecedor atualizado!", "Cadastro criado também como cliente."
  (`ClientsSuppliers.tsx:466-547`, `:753-781`); CPF/CNPJ inválido barra ("CPF/CNPJ inválido"). Backend: `INSERT/UPDATE
  suppliers|customers`, RPC `set_partner_labels`, select com `ilike` do telefone/CPF ao sair do campo
  (`hooks/usePartnerDuplicateCheck.ts:68-76`), select do outro lado pelo CPF/CNPJ + RPC `link_customer_supplier`
  (`utils/dualEntityLink.ts:127-161`); com módulo de portal, `portal_token` gerado na criação.

## 5. A ficha ao lado da lista (`ClientsListView.tsx:185-468`)
- Cabeçalho: "código · nome", "Fornecedor", "Cliente+Fornecedor" (se duplo), saldo em etiqueta + "a pagar"/"a receber",
  "<n> preços personalizados"; botões "Editar", "Nova Movimentação" (some na aba Conta-corrente), "..." (`:242-312`).
- Abas (`:220-230`): "Visão geral" ("Cadastro": CPF/CNPJ, "Razão social", "Nome fantasia", "Inscrição estadual",
  "Contato"; "Contato e endereço"; "Acesso ao portal" com o link e "Copiar"), "Pedidos", "Conta-corrente", "Lucro estimado"
  (fornecedor ou cliente duplo), "Financeiro", "Notas fiscais", "Preços" ("Preços Personalizados", "Salvar preços").
  Em "Pedidos" e "Financeiro" aparece o filtro "Período" na faixa das abas (padrão: todos os tempos) (`:337-353`).
- **Pedidos** (`pages/CustomerSupplierHistory.tsx`): cartões "Total Comprado", "Total de Pedidos", "Ticket Médio"
  (`:1068-1138`); gráfico "Top 5 Materiais Mais Comprados" por **peso** (quantidade), legenda "<material>: <n>%"
  (`:475-494`, `:1141-1189`); "Histórico de Pedidos" ("Nº Pedido", "Tipo", "Valor", "Pagamento", "Data", "Ações"), "Exportar".
  Backend: `purchases`/`sales` com itens, `balances`, `balance_movements`.
- **Conta-corrente** (`pages/BalanceDetail.tsx`, modo embutido): "Saldo Atual", "Editar saldo", valor colorido e "<nome>
  te deve" / "Você deve a <nome>" / "Saldo zerado"; selo "Cliente+Fornecedor" no duplo; botões "Tabela de preços",
  "Crédito/débito", "Movimentação" (`:1316-1446`). "Histórico de Movimentações" com filtro "Data" e "Exportar" ("Abrir
  Relatório (PDF)", abre aba nova; "Baixar Excel (.xlsx)") (`:1450-1520`). Tabela: "Data", "Descrição" (+ tipo "Pedido" /
  "Pagamento" / "Ajuste" e a forma "Dinheiro" / "Pix/Transferência" / "Saldo"), "Valor", "Saldo Final", "Ações" (`:1686-1757`).
- **Nova Movimentação de Saldo** (`components/BalancePaymentModal.tsx:534-713`): "Registre um pagamento ou cobrança para
  <nome>", "Saldo Atual" (verde se > 0, vermelho se < 0, sem olhar o tipo), "Tipo de Operação" (fornecedor: "Pagar" =
  "Você pagou ao fornecedor - Reduz o saldo dele com você", já marcado; "Receber"), "Valor *", "Forma de Pagamento"
  ("Dinheiro", apagado sem caixa aberto, tooltip "Nenhum caixa aberto — abra um caixa para movimentar em dinheiro";
  "Pix/Transferência" + "Conta bancária"), "Observação", "Data e hora do lançamento", "Cancelar", "Confirmar"; toast
  "Movimentação registrada com sucesso!". Descrição gravada: "Valor Pago a <nome> · <observação>". Backend: RPC
  `create_manual_bank_transaction`, RPC `update_balance`, `INSERT balance_movements` (`:262-400`, `utils/bankAccountUtils.ts:230-245`).
- **Lucro estimado** (`pages/SupplierProfitEstimate.tsx`): período padrão "Este mês" (`:98`), "Exportar PDF"; aviso fixo
  "Estimativa — sucata é fungível; a margem é calculada sobre o preço médio de venda do material no período, não é lucro
  realizado." (`:279-285`); cartões "Custo total comprado", "Margem estimada total", "Margem média %"; "Margem estimada
  por material": "Código", "Material", "Qtd Comprada", "Preço Médio Compra", "Qtd Vendida", "Preço Médio Venda", "Margem
  R$/kg", "Margem Total", "%", linha "Total"; "* preço de venda do cadastro (sem venda no período)" (`:445-569`). RPC
  `get_supplier_profit_estimate(p_company_id, p_supplier_id, p_start_date, p_end_date)` (`:135`). Opções do período:
  "Todos os tempos", "Hoje", "Últimos 7 dias", "Este mês", "Mês passado", "Últimos 30 dias", "Este ano", "Personalizado".
- **Financeiro** (`components/partner/PartnerFinancialsTab.tsx`): "Receitas vinculadas", "Despesas vinculadas", "Saldo";
  "Despesas & Receitas" ("Tipo" "Receita"/"Despesa", "Descrição", "Categoria", "Data", "Valor"); vazio: "Nenhuma despesa ou
  receita vinculada a este parceiro ainda." Backend: `cash_transactions` e `financial_bills` com `partner_type`/`partner_id`
  (`:84-153`).
- **Notas fiscais** (`components/partner/PartnerInvoicesTab.tsx`): "Notas Fiscais"; vazio "Nenhuma nota fiscal para este
  parceiro."; tabela "Nº Nota", "Tipo" ("Entrada"/"Saída"), "Status", "Data", "Valor", "Ações". Backend: `invoices` por
  `customer_id`/`supplier_id`.

## 6. Relatório de Saldos (`components/BalancesReportModal.tsx:236-458`)
Botão "Relatório" da tela. Janela "Relatório de Saldos" ("Visualize todos os saldos a receber e a pagar"), "Exportar
Relatório" ("Exportar em PDF", "Exportar em Excel"), "A Receber" e "A Pagar" com "Total: R$ ..."; colunas "Nome", "Tipo"
("Cliente" azul, "Fornecedor" laranja, "Cliente+Fornecedor" roxo), "Saldo" (com sinal e cor), "Última Mov.", "Ações"
(olho → ficha cheia na conta-corrente); "Fechar". A Receber = cliente > 0, fornecedor < 0, duplo > 0; A Pagar = o contrário
(`:109-119`). Backend: `balances` com `balance_movements(created_at)` embutido, `.neq('balance', 0)`, ordem por saldo
decrescente (`hooks/useBalance.tsx:100-125`); "Última Mov." = o primeiro movimento que vier (`:143-148`).

## 7. Ficha cheia (só no fim do cap. 12, `pages/PartnerDetail.tsx`)
"Clientes e Fornecedores › <nome>", "Saldo: <valor> (<nome> te deve)", "Editar", "Copiar link do portal", "Nova
movimentação", "Excluir"; abas "Histórico de Pedidos", "Conta-Corrente do Cliente", "Despesas & Receitas", "Notas Fiscais",
"Coletas" (módulo) (`:277-294`, `:471-525`).

## 8. Detalhes para o handoff (a fala não depende deles)
- A janela de movimentação pinta o "Saldo Atual" de verde quando é positivo, também no fornecedor (onde positivo é
  "a pagar", vermelho na lista) (`BalancePaymentModal.tsx:545`). Sem zoom nele.
- "Como funciona?" pinta "Saldo positivo no Fornecedor" de verde (`ClientsSuppliersHelpModal.tsx:46`); a lista usa vermelho.
- Ajuda gerada (`components/help-center/helpCenterData.generated.ts:451`) ainda fala do cartão e do botão "Ficha".
