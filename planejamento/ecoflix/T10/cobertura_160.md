# Cobertura 1.60.10 · T10 Estoque: saldo, histórico e posição

Auditoria de 18/11/2026, só leitura de código. Base: `/dev/shm/ecoflix-src` (`APP_VERSION = "1.60.10"`,
`src/config/version.ts:16`) contra o roteiro (1.59.154). Caminhos relativos a `src/`; linhas do 1.60.10. Não há varredura
do robô para a T10 (`rec/varredura/` só vai até `t04.txt`): nada aqui foi visto na tela.

Arquivos da aula **sem nenhuma mudança** entre `f37573ea0` e `5290be4cd`: `pages/MaterialHistory.tsx`,
`pages/InventoryReport.tsx`, `pages/PosicaoEstoque.tsx`, `components/TransferMaterialDialog.tsx`,
`components/BulkTransferDialog.tsx`, `components/StockMovementDialog.tsx`, `components/estoque/*` (janelas de exportar),
`components/reports/*`, `utils/fetchStockMovements.ts`, `components/DateRangeFilter.tsx`,
`components/ui/RetroactiveDateTimePicker.tsx`, `utils/openPdfInTab.ts`, `i18n/locales/pt-BR/materials.json` e
`navigation.json`. Ou seja: **os caps. 3 a 12 batem com o 1.60.10 como estão**. Mudaram só `pages/Materiais.tsx`,
`components/PriceTableSidebar.tsx` e `config/routes.ts`.

## 1. Mudou no app (por capítulo)

**cap01, cap02, cap03 e cap10 · a coluna "Tabelas de Preço" (aparece no Estoque e na Posição de Estoque)**
1. O menu "..." de cada tabela ganhou itens: "Configurações", **"Duplicar tabela"**, **"Fixar para meus pedidos e
   tickets"** (vira **"Remover minha tabela fixada"**), **"Definir como principal da empresa"** (só fora da principal e só
   para admin ou quem tem `action_edit_delete_materials`) e "Excluir" (`components/PriceTableSidebar.tsx:280-320`). O
   roteiro não abre esse menu; a coluna e o item "Posição de Estoque" embaixo de "Nova Tabela" continuam iguais. **Nada a
   mudar na fala.** É assunto da T3 (ver `T03/cobertura_160.md`, 3.1).
2. Tabela fixada pelo usuário ganha um alfinete ao lado do nome ("Fixada para meus pedidos e tickets",
   `PriceTableSidebar.tsx:256-261`). No mundo base ninguém fixa; se a T3 passar a fixar e não desfizer, o alfinete
   aparece nos caps. 1 e 10. **Conferir a semente `inicio`.**
3. No seletor compacto de tabela (o que substitui a coluna quando ela não cabe), entraram um botão "Duplicar tabela" e um
   "..." ("Ações da tabela de preços") com os mesmos itens (`pages/Materiais.tsx:2672-2735`). Na janela 1280×800 a aula usa
   a coluna lateral; **não aparece na gravação**.

**cap02 e cap05 · saldo e "Edição Manual"**
4. **1.59.159, "Estoque mantém os milhares ao editar materiais."** No "Editar Material", o campo "Quantidade em Estoque"
   passou de `decimals={3}` para `maxDecimals={3}` (`pages/Materiais.tsx:2083-2091`). Antes, abrir e salvar um material com
   mais de 1.000 kg podia reduzir o saldo sem o cliente perceber; agora o número volta inteiro. O roteiro da T10 não abre o
   "Editar", então **nenhuma fala muda**. Mas o efeito do defeito antigo é uma linha de "Edição Manual" no Kardex (o
   "Editar" grava o ajuste pela mesma RPC, `adjust_material_stock_atomic` com `EDICAO_MANUAL`, `pages/Materiais.tsx:1128-1133`),
   e é a T10 que ensina a ler essa linha: ver lacuna L3 e trecho 3.3.
5. A lista de materiais deixou de travar no cache local quando o aparelho se diz sem rede (`pages/Materiais.tsx:373-404`).
   Não muda rótulo nem fluxo; **nada a mudar**.

**cap00 e cap01 · menu**
6. No menu "Fiscal & Ambiental", "Estoque Fiscal" agora abre em `/fiscal-ambiental/estoque-fiscal/posicao` (antes
   `/relatorio`) e entrou o item **"Relatórios Fiscais"** (`config/routes.ts:510-511`). O grupo "Materiais" não mudou. A T10
   não abre esse menu; só importa para a frase que cita o Estoque Fiscal (trecho 3.6). **O conteúdo é da T17.**

Total: **6 mudanças**, nenhuma quebra rótulo ou fala do roteiro atual.

**Pendências herdadas do ensaio de 11/11 (não são do 1.60.10, mas continuam valendo; `propostas_fala.md`):** o item do menu
é **"Histórico (Kardex)"** (`navigation.json:13`), o roteiro diz "Histórico"; os números saem sem casas fixas ("6.420 Kg",
"+320 Kg", "Transferido 320 Kg de Ferro misto para Ferro pesado"), o roteiro marca "6.420,000"; a explicação do "Preço
médio pago" abre no **valor** da linha, não no cabeçalho; no Kardex cada filtro vale na hora e "Aplicar filtros" só fecha
a folha; o PDF abre em outra aba que a gravação não segue.

## 2. Falta cobrir

| # | O que é (rótulo exato) | Quando o cliente usa | Vale? |
|---|---|---|---|
| **Estoque** | | | |
| L1 | Botão **"Posição de Estoque"** no cabeçalho da tela, quando a empresa tem uma tabela de preço só (`pages/Materiais.tsx:2360-2370`) | A maioria dos clientes novos não tem a coluna "Tabelas de Preço" e não acha a quarta porta | **Sim**, uma frase no cap01 |
| L2 | Aviso no "Preço médio pago": triângulo amarelo e "⚠ Sem histórico de compra: usando o preço cadastrado, pode não refletir o custo real." (`materials.json` `avgCostPaidNoHistory`; `pages/Materiais.tsx:3236-3252`) | Material que entrou por saldo inicial ou ajuste, sem compra | **Sim**, frase no cap02 (se a semente tiver um material assim; senão só fala) |
| L3 | Alterar a "Quantidade em Estoque" pelo "Editar" também gera "Edição Manual" no Kardex, sem observação (`pages/Materiais.tsx:1122-1133`); nota 1.59.159 | Cliente que achou um ajuste que "ninguém fez" | **Sim**, frase no cap05 |
| L4 | Ordenar a lista pelo título da coluna; seleção em massa ("Definir prefixo", "Definir resíduo do MTR", excluir); "Movimentar estoque"; "Zerar Estoque"; "Importar planilha"; "Grupos"; exportar a lista | Cadastro e arrumação | **Não**: T3 (caps. 1, 2, 5, 8, 9, 10 e propostas F11 e F12 da auditoria da T3) |
| L5 | Valores com cadeado "Sem permissão" e botão "Exportar" que some sem a ação `action_export_reports` (`pages/Materiais.tsx:221`, `MaterialHistory.tsx:202,845`, `PosicaoEstoque.tsx:115,727`) | Operador que não vê valor ou não acha o Exportar | **Só citar** no cap11 (o como é da T2) |
| L6 | Erros da transferência: "Selecione o material de destino", "Informe a quantidade a transferir", "Material de destino não pode ser o mesmo que o de origem" (`TransferMaterialDialog.tsx:114-124`) | Engano ao preencher | **Não**: a trilha não encena erro |
| **Histórico (Kardex)** | | | |
| L7 | Coluna "Materiais": busca **"Buscar código ou material"**, botão **"Ordenar"** ("Ordenar materiais": "Código", "Nome") e páginas de 25 (`MaterialHistory.tsx:545-575,519-521,620-628`) | Empresa com dezenas de materiais | **Sim**, no capítulo novo 3.1 |
| L8 | Filtro **"Quantidade movimentada"**: "Maior que", "Maior ou igual a", "Igual a", "Menor ou igual a", "Menor que" + valor ("Ex.: 40"); "Considera o valor sem sinal: 40 encontra +40 e -40." (`MaterialHistory.tsx:932-961`; `components/estoque/KardexExportDialog.tsx:29-35`) | "Cadê aquela carga de oitocentos e sessenta quilos?" | **Sim**, 3.1 |
| L9 | Período **"Personalizado"** (datas de início e fim) e as outras opções ("Hoje", "Últimos 7 dias", "Mês passado", "Últimos 30 dias") (`common.json:3-10`) | Conferir uma semana ou um intervalo que o contador pediu | **Sim**, 3.1 |
| L10 | Filtro **"Clientes"** aplicado de fato, e **linha de venda aberta** ("Cliente:", itens, "Formas de Pagamento", "Total do Pedido:") (`MaterialHistory.tsx:1341-1420`) | Para onde foi o material | **Sim**, 3.1 (o roteiro só abre compra) |
| L11 | Colunas **"Usuário"** e **"Pedido #"** (o número do pedido ligado; `MaterialHistory.tsx:1307-1310`) | Quem lançou e qual pedido procurar na tela de Pedidos | **Sim**, frase no cap04 |
| L12 | **"Como funciona?"** → "Como funciona o Kardex" (`MaterialHistory.tsx:1480-1600`) | Dúvida na hora | **Só citar** (cursor no botão, 3.1) |
| L13 | **Exportar Kardex de verdade**: janela "Exportar Kardex (PDF)" / "(Excel)", "Escolha o recorte do extrato. Mudar os filtros aqui não altera os filtros da tela."; campos "Período", "Materiais", "Tipos de movimentação", "Quantidade movimentada", "Fornecedores", "Clientes"; botão "Exportar PDF"; avisos "Kardex exportado em PDF" / "Kardex exportado em Excel" (`KardexExportDialog.tsx:176-290`; `MaterialHistory.tsx:763,770`) | Mandar o extrato de um material pro contador ou pro sócio | **Sim**, 3.1 (o cap11 só mostra o menu por 2 s) |
| L14 | Aviso **"Recorte grande demais para a tela"** ("Este período tem N lançamentos, mais do que a tela consegue mostrar de uma vez. Escolha um período menor nos filtros, ou use o botão Exportar para baixar o extrato completo em Excel."; acima de 20.000, `fetchStockMovements.ts:53`; `MaterialHistory.tsx:993-999`) | Pátio grande em "Todos os tempos" | **Só citar** (uma frase; não dá para encenar no mundo) |
| L15 | Linha com "Material excluído" no lugar do nome; vazio "Nenhuma movimentação encontrada com estes filtros." | Material apagado; filtro apertado demais | **Não**: o cap05 já explica a Exclusão; vazio não se encena |
| **Relatório de Estoque** | | | |
| L16 | Cartões **"Total Vendido"** e **"Lucro"** abertos: "Preço médio de venda", "Qtd. Vendida", "Materiais vendidos", "Material que mais vendeu"; "Lucro s/ vendas total", "Resultado total", "Margem", "Margem média", "Material mais lucrativo" (`InventoryReport.tsx:1035-1045,1103-1116`) | Fechamento do mês em um minuto | **Sim**, trecho no cap07 (hoje só abre "Total Comprado") |
| L17 | **"Distribuição por forma de pagamento"** nos cartões de compra e venda: "Dinheiro", "Pix/Transferência", "Saldo", "Em aberto"; nota "Considera os pedidos do período; não segue o filtro de material." (`materials.json` `report.kpiPayment*`; `components/reports/KpiDetail.tsx:100-106`) | Quanto do mês saiu em dinheiro e quanto ficou fiado | **Sim**, mesma tomada do L16 |
| L18 | Filtro **"Clientes"**: mexe só nas colunas de venda (`InventoryReport.tsx:1219-1228`) | Quanto vendi pra Fundição, de cada material | **Sim**, capítulo novo 3.2 |
| L19 | Filtro **"Usuários"**: quem registrou a compra ou a venda (`InventoryReport.tsx:1229-1238,1376-1383`) | Conferir o que cada operador comprou | **Sim**, 3.2 |
| L20 | Filtros **"Todos os Materiais"** e **"Grupos"** (com "Geral / Sem grupo", `InventoryReport.tsx:67,1300-1400`) e a visão **"Por material" / "Por grupo"** com a linha **"Subtotal <grupo>"** (`:1262-1287,1497-1530`) | Quanto entrou de cobre no mês, sem somar na mão | **Sim**, 3.2 |
| L21 | Chave **"Ocultar itens zerados"** (fica guardada no aparelho; `InventoryReport.tsx:90-93,1403`) | Lista limpa só com o que girou | **Sim**, frase no 3.2 |
| L22 | **Ordenar** pelo título de qualquer coluna (`InventoryReport.tsx:1427-1461`) e a linha **"TOTAL"** (`:1568`) | Achar o material que mais deu resultado | **Sim**, frase no 3.2 |
| L23 | **"Resultado" nunca fica negativo**: se comprou mais do que vendeu, mostra R$ 0,00, e o mouse na célula abre "… vendidos", "− … comprados", "= … (prejuízo)", "Lucro exibido: R$ 0,00" (`utils/profitDisplay.ts:13-21`; `components/reports/ProfitCellTooltipContent.tsx:22-43`); explicação do cabeçalho: "Valor Vendido − Valor Comprado no período (não casa quantidades; pode misturar estoque de períodos diferentes)." | Cliente estranha o zero num material que só comprou | **Sim**, dica no cap08, na linha da bateria automotiva |
| L24 | **"Exportar Relatório" de verdade** (PDF respeita período e filtros; com fornecedor marcado sai só compras; `InventoryReport.tsx:402-492`); avisos "Nenhum dado para exportar" | Relatório do mês pro contador | **Sim**, um clique no cap11 |
| L25 | Aviso de custo: "Este material tem estoque sem custo registrado (ajuste manual/transferência) — o custo pode estar subestimado." no "Lucro s/ Vendas" (`components/reports/inventoryTooltips.tsx:60-72`) | Material que cresceu por transferência (o ferro pesado do cap03) | **Só citar**, junto do L2 |
| **Posição de Estoque** | | | |
| L26 | **Ajustar a hora** ("Hora"; "O padrão é o fim do dia (23:59). Você pode ajustar o horário."; `PosicaoEstoque.tsx:713-760`) | Saldo antes da contagem, na virada de turno | **Sim**, trecho no cap10 (hoje a hora só é lida) |
| L27 | Visão **"Por material" / "Por grupo"** com "Subtotal <grupo>" (`PosicaoEstoque.tsx:771-796,588-600`) | Inventário por família de material | **Sim**, frase no cap10 |
| L28 | Rodapé: **"Valores negativos indicam movimentações lançadas fora da ordem cronológica."** e **"Itens sem compra registrada até a data aparecem sem valorização."** (`PosicaoEstoque.tsx:803-808`) | Saldo negativo numa data antiga; material sem "Valor" | **Sim**, dica no cap10 (o roteiro lê só as duas frases do meio) |
| L29 | Só aparece material com saldo diferente de zero; vazio "Nenhum material em estoque nessa data"; dia futuro bloqueado | Material que "sumiu" da foto | **Só citar** (meia frase no cap10) |
| L30 | Na janela de exportar: **desmarcar coluna** (ex.: "Valor do estoque"), escolher por **"Grupos"**, "Marcar todos" / "Desmarcar todos", contador "N de M materiais" (`components/estoque/StockExportDialog.tsx:288-430`) | Mandar a posição sem mostrar quanto pagou | **Sim**, ação no cap11 (hoje a câmera só passa) |
| L31 | Coluna de caixas/jogos na Posição (ficha de produção; `PosicaoEstoque.tsx:229-266,809-815`) | Quem usa Produção | **Não**: T11 |
| L32 | **Estoque Fiscal** (saldo pelas notas e comparação com o estoque operacional; notas 1.60.6) | Quem emite nota | **T17. Só citar** (3.6) |
| L33 | "Transferência em Lote" entre unidades | Matriz e filial | **T22**: o cap03 já cita |
| L34 | Cato responde saldo de estoque | Pergunta rápida | **T21**. Não repetir |

Total: **34 lacunas**: 22 "sim", 6 "só citar", 6 "não" ou de outra aula.

## 3. Proposta

Dois capítulos novos e trechos nos que já existem. Os caps. 7 a 12 atuais viram 8 a 13 depois do 3.1, e o 10 a 13 viram
11 a 14 depois do 3.2 (numeração final: 15 capítulos, 0 a 14).

### 3.1 Capítulo novo · "Achar uma movimentação" (vinheta: HISTÓRICO), depois do cap06 atual

Semente `apos-cap03`. O capítulo não grava nada.

| Tela | Fala |
| --- | --- |
| "Materiais" → "Histórico (Kardex)"; na coluna "Materiais", digita "cobre" em "Buscar código ou material": ficam os três cobres; limpa. Clique em "Ordenar": "Ordenar materiais", com "Código" e "Nome"; escolhe "Nome". | Agora, como achar uma movimentação no meio de centenas. Na coluna dos materiais, a busca aceita o código ou o nome, e o Ordenar muda a lista de código pra nome. |
| Clique em "Ferro pesado"; "Filtros" → "Período" → "Personalizado": escolhe de 01/11/2026 a 07/11/2026; a tabela fica com a primeira semana de novembro. | No período, além das opções prontas, tem o Personalizado. O contador pediu a primeira semana de novembro? É só marcar o dia um e o dia sete. |
| No mesmo painel, volta o período para "Este mês"; em "Quantidade movimentada" escolhe "Igual a" e digita 860. [ZOOM: "Quantidade movimentada" e "Considera o valor sem sinal: 40 encontra +40 e -40."] Fica só a "Compra" de 09/11 (+860 Kg). | E quando você lembra do peso, mas não do dia? O filtro de quantidade movimentada resolve. Igual a oitocentos e sessenta, e sobra a compra de ontem. Ele ignora o sinal: acha a entrada e a saída com esse peso. |
| Limpa a quantidade; em "Clientes" marca "Aços Quiririm Ltda"; "Aplicar filtros": ficam as vendas de novembro. Clique na venda de 04/11 (−38.992 Kg): abre os itens, "Cliente:", "Formas de Pagamento" e "Total do Pedido:". [BACKEND: `sale_items` e `orders_with_payments` da venda de 04/11, Pix] | O filtro de clientes mostra pra onde o material foi. Abrindo a venda do dia quatro, aparece o cliente, a Aços Quiririm, os itens, o pagamento e o total, do mesmo jeito que na compra. |
| "Filtros" → "Limpar filtros". Clique em "Exportar" → "PDF": janela "Exportar Kardex (PDF)", já com "Este mês" e "Ferro pesado". [ZOOM: "Escolha o recorte do extrato. Mudar os filtros aqui não altera os filtros da tela."] | Pra mandar esse extrato pra alguém, é o Exportar. A janela já vem com o que está na tela: o período e o ferro pesado. Dá pra mudar aqui sem mexer nos filtros da tela. |
| Clique em "Exportar PDF": aviso "Kardex exportado em PDF" (a aba do PDF entra como ilustração na edição, igual ao cap. de exportar). | Exportar, e o extrato do ferro pesado sai em PDF. Em Excel, é o mesmo caminho. |
| Cursor no botão "Como funciona?", sem abrir. | Uma dica: se o período for grande demais, a tela avisa e pede um recorte menor. Nesse caso, o Excel baixa o extrato inteiro. E o Como funciona resume as colunas e os tipos. |

Fala: ~225 palavras, ~87 s.

### 3.2 Capítulo novo · "Clientes, usuários e grupos" (vinheta: RELATÓRIO), depois do cap09 atual ("O filtro de fornecedor")

Semente `apos-cap03`; `setup` deixa o período em "Mês passado". Não grava nada.

| Tela | Fala |
| --- | --- |
| Em "Detalhamento por Material", clique em "Clientes" e marca "Fundição Bandeira do Vale": as colunas de venda passam a mostrar só o que foi pra Fundição; as de compra não mudam. Desmarca. [BACKEND: `get_inventory_report_data` com `p_customer_ids`] | Os outros filtros funcionam do mesmo jeito. O de clientes mexe só nas vendas: marcando a Fundição Bandeira do Vale, eu vejo quanto ela levou de cada material em outubro. |
| "Usuários" → marca "Marcos Antunes": ficam as compras e as vendas que ele lançou. Desmarca. [BACKEND: `p_creator_ids`; pedidos de outubro com `created_by` do Marcos] | O de usuários mostra o que cada pessoa lançou. Aqui, só as compras e as vendas que o Marcos registrou. |
| "Grupos" → marca "Cobre": ficam os três cobres e os cartões recalculam. | E o de grupos junta os materiais da mesma família. Só o grupo Cobre, e os cartões de cima já somam só o cobre. |
| Desmarca o grupo; clique em "Por grupo": a tabela ganha uma faixa por grupo e a linha "Subtotal Ferrosos", "Subtotal Cobre"… [ZOOM: "Subtotal Cobre"] | Quer ver todos, mas separados? Em Por grupo, cada família ganha a sua faixa e o seu subtotal. |
| Volta para "Por material"; liga "Ocultar itens zerados": somem as linhas sem compra nem venda no mês. | O Ocultar itens zerados tira da lista o que não girou no mês. O sistema lembra dessa escolha. |
| Clique no título "Resultado": a lista ordena do maior para o menor; a câmera desce até a linha "TOTAL". | Clicando no título de uma coluna, a lista ordena por ela. Em Resultado, o material que mais rendeu vai pro topo. E a última linha soma tudo. |

Fala: ~150 palavras, ~58 s.

### 3.3 Trechos em capítulos que já existem

| Onde | Tela | Fala |
| --- | --- | --- |
| cap01, depois de "A quarta fica dentro do Estoque…" | [ILUSTRAÇÃO ou corte: o cabeçalho da tela "Estoque" com o botão "Posição de Estoque" (empresa com uma tabela só)] | Se a sua empresa usa uma tabela de preço só, essa coluna não aparece. Aí a Posição de Estoque é um botão no alto da tela. |
| cap01, primeira linha | (mesma tela) | (trocar) "…aparecem as três primeiras: Estoque, Histórico, que é o Kardex, e Relatório." (proposta já registrada em `propostas_fala.md`) |
| cap02, depois do selo "estimativa" | Mouse no valor do "Preço médio pago" de um material com triângulo amarelo: "⚠ Sem histórico de compra: usando o preço cadastrado, pode não refletir o custo real." | Uma dica: quando o material tem saldo e nenhuma compra lançada, aparece um triângulo amarelo. O sistema usa o preço do cadastro, e o valor pode não ser o que você pagou. |
| cap04, na linha da transferência | [ZOOM: colunas "Usuário" e "Pedido #" da linha "Compra" de 09/11] | Cada linha mostra também quem lançou e, quando veio de um pedido, o número dele. |
| cap05, depois de abrir a "Edição Manual" de 31/10 | (mesma tela) | Uma dica: mudar a quantidade pelo Editar do material também vira uma Edição Manual, só que sem observação. Por isso, pra ajustar o saldo, prefira o Movimentar estoque, que pede o motivo. |
| cap07, depois de abrir "Total Comprado" | Clique em "Total Vendido" e em "Lucro": abrem os detalhes; a câmera para em "Distribuição por forma de pagamento" ("Dinheiro", "Pix/Transferência", "Saldo", "Em aberto"). [BACKEND: `get_orders_payment_distribution` de outubro] | O Total Vendido e o Lucro abrem do mesmo jeito: o material que mais vendeu, o mais lucrativo, a margem. E embaixo, como o mês foi pago: dinheiro, Pix, saldo e o que ficou em aberto. |
| cap08, na linha "Bateria automotiva" | Mouse na célula "Resultado" (R$ 0,00): abre "… vendidos", "− R$ 4.092,00 comprados", "(prejuízo)" e "Lucro exibido: R$ 0,00". [TESTAR: o texto abre na célula] | Repara que o Resultado dela é zero, e não negativo. O Resultado nunca fica abaixo de zero. Passando o mouse, a conta aparece inteira. |
| cap10, depois de "Ver posição" | Em "Hora", troca 23:59 por 12:00; "Ver posição": o Ferro pesado mostra 41.874 Kg; volta para 23:59 e "Ver posição". [ZOOM: "Hora" e o "Saldo"] | E dá pra mudar a hora. Ao meio-dia do dia trinta e um, o ferro pesado tinha quarenta e um mil oitocentos e setenta e quatro quilos. Era o saldo antes da contagem, que tirou catorze. |
| cap10, na tabela | Clique em "Por grupo": faixas por grupo e "Subtotal Ferrosos"; volta para "Por material". | Em Por grupo, a foto vem separada por família, com o subtotal de cada uma. |
| cap10, no rodapé | [ZOOM: a nota inteira do rodapé] | Uma dica: se aparecer saldo negativo numa data antiga, é lançamento feito fora de ordem, com data anterior. Material sem compra até aquela data aparece sem valor. E material zerado não entra na foto. |
| cap11, na janela "Exportar estoque (PDF)" | Em "Colunas do arquivo", desmarca "Valor do estoque"; a câmera passa por "Grupos" e "Marcar todos" / "Desmarcar todos". (Marca de novo antes de exportar, para o PDF do recap.) | (trocar a fala atual) Aqui você escolhe as colunas e os materiais do arquivo. Não quer mostrar quanto pagou? É só tirar a coluna Valor do estoque. A tela guarda essa escolha pra próxima vez. |
| cap11, no fim | No "Relatório de Estoque" de outubro, clique em "Exportar Relatório": a aba do PDF (ilustração na edição). | (trocar a última fala) O Relatório exporta em PDF pelo Exportar Relatório, com o período e os filtros da tela. E o Histórico, a gente já exportou. Se o Exportar não aparece pra um usuário, é permissão dele. |
| cap11 ou recap (3.6) | (mesma tela) | Quem emite nota tem ainda o Estoque Fiscal, que compara esse estoque com o das notas. Ele fica no tutorial de transporte, serviço e contador. |
| Recapitulando | Montagens dos dois capítulos novos. | (acrescentar) Achou uma movimentação pelo peso e exportou o Kardex. E filtrou o Relatório por cliente, usuário e grupo. |

Fala a mais: ~345 palavras, ~133 s.

### O que o mundo fictício precisa para gravar

- **3.1**: `sale_items`, `orders_with_payments` e o Pix da venda de 04/11 à Aços Quiririm Ltda (38.992 kg de ferro pesado);
  o filtro de período "Personalizado" e o de quantidade (`eq 860`) já saem do `stock_movements` da semente; nenhum handler
  novo (o PDF e o Excel do Kardex são feitos no navegador).
- **3.2**: `get_inventory_report_data` respondendo a `p_customer_ids` (Fundição Bandeira do Vale) e a `p_creator_ids`
  (Marcos Antunes): os pedidos de outubro precisam de `created_by` repartido entre Rafael, Juliana e Marcos, coerente com
  a T7 e a T9. `materials.group_id` dos grupos da T3 (Ferrosos, Cobre, Alumínio, Metais, Outros). Nenhum número novo falado.
- **cap02 (L2)**: um material com saldo e sem `purchase_items`. Se a semente não tiver, **não criar**: o estoque soma
  R$ 52.112,25 na T21; nesse caso a fala fica sobre a tela atual, sem o triângulo.
- **cap07**: `get_orders_payment_distribution` de outubro com as quatro linhas (dinheiro, Pix, saldo, em aberto).
- **cap08**: Bateria automotiva com R$ 4.092,00 comprados e zero vendido (já está no `plano.md`).
- **cap10**: `get_stock_balance_at_date` em 31/10 12:00 devolvendo 41.874 kg de ferro pesado (a "Edição Manual" é das
  12:40, já no plano). Materiais com `group_id` para o "Por grupo".
- **cap01**: o botão do cabeçalho só existe com `multiplePriceTablesEnabled` desligado; gravar um corte de 3 s numa
  semente à parte, ou usar ilustração.
- Nada de dado real; nenhum nome novo no `MUNDO_FICTICIO.md`.

## 4. Estimativa

| Item | Fala a mais |
| --- | --- |
| 3.1 capítulo novo "Achar uma movimentação" | ~87 s |
| 3.2 capítulo novo "Clientes, usuários e grupos" | ~58 s |
| 3.3 trechos (caps. 1, 2, 4, 5, 7, 8, 10, 11 e recap) | ~133 s |
| **Total** | **~278 s (4 min 40 s)** |

**2 capítulos novos** (14 vinhetas no lugar de 12). A aula vai de ~14 min para ~19 min de vídeo. Regravar: caps. 1, 2, 4,
5, 7, 8, 10, 11 e o recap; caps. 0, 3, 6 e 9 ficam como estão.

**Depende de decisão do Kaik:**
1. Dois capítulos novos, como proposto, ou espalhar o 3.1 nos caps. 4 a 6 e o 3.2 no cap09 (menos vinhetas, capítulos
   mais longos).
2. Aplicar junto as pendências herdadas do ensaio ("Histórico (Kardex)" e os números sem ",000" nas marcas de zoom).
3. Filtro "Usuários": exige decidir quem lançou cada pedido de outubro no mundo (mexe nas sementes da T7 e da T9).
4. A dica do "Editar" (L3) recomenda o "Movimentar estoque": confirmar que é essa a orientação que ele quer dar ao cliente.
5. O botão "Posição de Estoque" do cabeçalho: corte gravado numa semente sem várias tabelas, ou só ilustração.
