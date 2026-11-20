# Plano · T10 · Estoque: saldo, histórico e posição

- **Título:** Estoque: saldo, histórico e posição (o da fonte). **Antes:** T9 "Pedidos e histórico do caixa".
  **Próximo:** T13 "Contas a Pagar e Receber".
- **Objetivo:** responder as três perguntas do contador da Recicla Vale Metais: quanto tem hoje (Estoque), de onde
  veio (Histórico/Kardex) e quanto tinha no dia 31 (Posição de Estoque); e ler o Relatório de Estoque do mês.
- **Áreas das vinhetas:** ESTOQUE · HISTÓRICO · RELATÓRIO · POSIÇÃO · RESUMO.
- **Alvo da fonte:** ~16 min. Desktop (tela 1600×900), logado como **Rafael Nogueira** (MASTER: vê valores e exporta).
  `FAKE_NOW=2026-11-10T08:30:00-03:00` (terça). Sem módulo 🔒 próprio; cita o Gerencial e a Produção como
  "depende do plano contratado".
- Base: `T10/inventario.md` (código 1.60.18; aplicação de 20/11/2026: 15 capítulos, dois novos).

## Capítulos (os da fonte, na ordem)

| # | Vinheta (área / título) | O que se mostra | Ilustração | Estado de partida |
|---|---|---|---|---|
| 0 | (sem vinheta) | Abertura: as três perguntas do contador; menu "Materiais"; cartão "Antes" | as três perguntas | `inicio` |
| 1 | ESTOQUE / As quatro portas do estoque | "Materiais" → "Estoque", "Histórico (Kardex)", "Relatório"; a "Posição de Estoque" na coluna "Tabelas de Preço"; o botão do cabeçalho (só falado) | as quatro portas; o botão sem coluna | `inicio` |
| 2 | ESTOQUE / O saldo de cada material | cartões; linha do Cobre mel ("Estoque Atual", "Preço médio pago"); o triângulo "Sem histórico de compra" (só falado); Ferro misto | o que mexe no saldo; o aviso amarelo | `inicio` |
| 3 | ESTOQUE / Transferir entre materiais | "Transferir estoque" do Ferro misto para o Ferro pesado, 320 kg; a barra de seleção só mostrada | a separação no pátio | `inicio` → `apos-cap03` |
| 4 | HISTÓRICO / O Kardex, linha a linha | "Histórico de Materiais", "Geral (Todos)" → "Ferro pesado"; Estoque Inicial → Movimentação → Estoque Final; colunas "Usuário" e "Pedido"; "Este mês" → "Este ano" | Kardex = extrato; a corrente | `apos-cap03` |
| 5 | HISTÓRICO / Os tipos de movimentação | selos; os sete tipos; "Edição Manual" de 31/10 aberta; dica do "Editar" (só falada); "Exclusão" de 22/10; filtro "Fornecedores" (só compras) | os tipos no pátio | `apos-cap03` (setup: Ferro pesado, "Este ano") |
| 6 | HISTÓRICO / O pedido por trás da linha | a compra de 09/11 aberta: itens, "Fornecedor:", "Formas de Pagamento", "Total do Pedido:", "Fotos anexadas" | (só tela) | `apos-cap03` |
| **7** | **HISTÓRICO / Achar uma movimentação (novo)** | busca e "Ordenar"; "Personalizado" 01 a 07/11; "Quantidade movimentada" Igual a 860; "Clientes" Aços Quiririm e a venda de 04/11 aberta; "Exportar" PDF e Excel do Kardex; "Como funciona?" | PDF do Kardex na aba (cena `pdf`) | `apos-cap03` (setup: Kardex Geral) |
| 8 | RELATÓRIO / Comprado, vendido e lucro (era 7) | "Mês passado"; os quatro cartões; "Total Comprado", "Total Vendido" e "Lucro" abertos; "Distribuição por forma de pagamento"; "Projeção de Lucro"; saldo ≠ comprado − vendido; só pedidos finalizados | a projeção; Estoque × Relatório | `apos-cap03` |
| 9 | RELATÓRIO / Material por material (era 8) | Cobre mel de outubro; peso líquido; Bateria automotiva sem venda e o balão do "Resultado" (R$ 0,00) | resultado e margem; peso líquido | `apos-cap03` (setup: "Mês passado") |
| 10 | RELATÓRIO / O filtro de fornecedor (era 9) | "Fornecedores" → "Depósito Irmãos Siqueira": só compras; desmarca | a pilha sem dono | `apos-cap03` (setup: "Mês passado") |
| **11** | **RELATÓRIO / Clientes, usuários e grupos (novo)** | "Clientes" (Fundição Bandeira do Vale), "Usuários" (Marcos Antunes), "Grupos" (Cobre), "Por grupo" e "Subtotal", "Ocultar itens zerados", ordenar por "Resultado" e a linha "TOTAL" | (só tela) | `apos-cap03` (setup: "Mês passado") |
| 12 | POSIÇÃO / A foto do estoque numa data (era 10) | "Posição de Estoque" de hoje; 31/10 23:59; "Ver posição"; Ferro pesado 41.860 kg; a "Hora" 12:00 (41.874 kg); "Valor", "Projeção venda"; "Por grupo"; "Total geral"; a nota do rodapé | a foto numa data | `apos-cap03` |
| 13 | POSIÇÃO / Exportar para o contador (era 11) | "Exportar" → "PDF": desmarca "Valor do estoque", "Grupos", "Marcar todos" → aba do PDF; "Excel"; "Exportar Relatório" de outubro (aba HTML); Estoque Fiscal só falado | PDFs na aba (cenas `pdf`) | `apos-cap03` (setup: 31/10 aplicado) |
| 14 | RESUMO / Recapitulando (era 12) | montagem do que foi feito (inclui os dois capítulos novos); cartão "Próximo: Contas a Pagar e Receber" | | |

Transições faladas: 1 "Vamos às quatro portas"; 2 "Esta é a tela do saldo"; 3 "Agora, a transferência"; 4 "Agora o
Histórico, de onde veio cada quilo"; 5 "Cada linha tem um tipo"; 6 "Toda linha de compra ou de venda abre o pedido";
7 "Agora, como achar uma movimentação"; 8 "Agora o Relatório de Estoque"; 9 "Embaixo dos cartões"; 10 "Agora repara o que acontece quando eu
filtro"; 11 "Os outros filtros funcionam do mesmo jeito"; 12 "E a terceira pergunta do contador"; 13 "Com a foto do dia 31 na tela, é só exportar".

**Cuidados (⚠️) na fala, com "Uma dica:"**: saldo do Estoque ≠ comprado − vendido do Relatório (cap. 7, com a
ilustração lado a lado); período em "Este mês" (cap. 4, trocando para "Este ano"; a opção da tela é "Todos os tempos");
quantidade comprada líquida (cap. 8, peso líquido); filtro de Fornecedores/Clientes no Kardex tira manual, transferência
e exclusão, e (1.60.18) o de fornecedor tira também as vendas (cap. 5); compra sem venda não é erro (cap. 8, Bateria automotiva); só pedidos finalizados, pela data do
pedido, excluído sai (cap. 7). Nenhuma mensagem de erro na tela.

## Mundo: o que esta aula precisa
Além do `MUNDO_FICTICIO.md`. **A fala cita estes números**: a semente consolidada tem de bater com eles (ou a fala troca
os números nas linhas marcadas no roteiro). `stock_movements` sempre com `stock_before`/`stock_after` encadeados e
`created_at` = `transaction_at` (a tela ordena por `created_at`).

| Item | Valores (fictícios) | Onde a fala usa |
|---|---|---|
| Várias tabelas de preço ligadas, com a "Tabela Depósitos" do T3 | a coluna "Tabelas de Preço" (com "Posição de Estoque") aparece | caps. 1 e 10 |
| Ferro misto, saldo em 10/11 08:30 | **6.420,000 kg** (6.100 depois da transferência) | caps. 2 e 3 |
| Ferro pesado, outubro | 22/10: compra do Valdir Pereira de **180 kg** (junção: a Auto Peças tem só as três compras da T9 em outubro) lançada duas vezes; a repetida excluída no mesmo dia (linha "Exclusão" −180 kg). 31/10 (sábado) 12:40: "Edição Manual" **−14 kg** por Rafael, observação **"Contagem do pátio no fechamento do mês"**, 41.874 → **41.860 kg** (última linha de outubro; junção: as 40 t paradas do T15 estão aqui) | caps. 5 e 10 |
| Ferro pesado, novembro | (junção, `MUNDO_LINHA_DO_TEMPO.md`) 03/11 09:20 compra do Depósito Irmãos Siqueira +640 kg, Pix da Conta Secundária (a das 09:40 é a de ferro misto da T14) (→ 42.500); 04/11 venda à Aços Quiririm Ltda −38.992 kg, Pix (→ 3.508); 05/11 venda à Aços Quiririm no saldo −2.608 kg (T4) (→ 900); 06/11 compra do Depósito Irmãos Siqueira no saldo +1.200 kg (T4) (→ 2.100); 06/11 14:05 compra da Auto Peças Vale Forte +400 kg, Pix da Conta Principal (T14) (→ 2.500); 06/11 15:30 venda à Aços Quiririm Ltda −1.180 kg (→ 1.320); **09/11 15:20 compra do Depósito Irmãos Siqueira +860 kg a R$ 0,95 = R$ 817,00, paga em Pix (Conta Secundária: o extrato da Conta Principal da T14 não tem esse Pix), com 2 fotos** (→ **2.180 kg**) | caps. 4, 6 e 10 |
| Fotos da compra de 09/11 | 2 imagens fictícias em `order_attachments` + bucket `order-attachments`: sucata de ferro numa caçamba, sem placa nem rosto (desenho ou imagem gerada, nada de foto real) | cap. 6 |
| Cobre mel | saldo em 10/11: **42,000 kg** (junção: o do T7); todas as compras a R$ 42,50 (o "Preço médio pago" dá **R$ 42,50**), vendas a R$ 47,90 | cap. 2 |
| Cobre mel, outubro | compras **980 kg = R$ 41.650,00**; vendas à Fundição Bandeira do Vale **1.000 kg = R$ 47.900,00** (Resultado R$ 6.250,00; Margem 13,05%; Lucro s/ Vendas R$ 5.400,00). Valor de compra sobre o peso líquido | cap. 8 |
| Bateria automotiva, outubro | compras **1.320 kg** (R$ 4.092,00), **nenhuma venda** | cap. 8 |
| Cobre misto, outubro | compras do Depósito Irmãos Siqueira e do Valdir Pereira; venda à Fundição (números não falados) | cap. 9 (ilustração) |
| Depósito Irmãos Siqueira, outubro | compras de ferro pesado e de cobre misto (aparecem com o filtro "Fornecedores") | cap. 9 |
| Criado ao vivo (cap. 3) | transferência Ferro misto → Ferro pesado, **320 kg**, por Rafael, ~08:35 de 10/11: duas linhas "TRANSFERENCIA" (6.420 → 6.100 e 2.180 → 2.500). Vira `apos-cap03`, entrada dos caps. 4 a 11 | caps. 3, 4, 10 |

Fica para as próximas: nada (a transferência só existe nesta aula). Se o Kaik quiser continuidade, o T13 pode partir
de `apos-cap03`.

## Gravação
- **Rotas:** `/dashboard`, `/materiais`, `/historico-materiais`, `/relatorio-estoque`, `/materiais/posicao-estoque`.
- **Backend falso (RPCs e tabelas):** `transfer_material_stock` (escreve; cap. 3), `get_inventory_report_data` (com os
  filtros de fornecedor/cliente/usuário e a quantidade líquida), `get_financial_dre_summary` (cartões sem filtro),
  `get_orders_payment_distribution`, `get_stock_balance_at_date` (saldo em `p_at`, com `avg_cost` e `sale_price`, só
  saldo ≠ 0); `stock_movements` (+ `materials`, `profiles`), `purchases`/`sales`/`purchase_items`/`sale_items`, view
  `orders_with_payments`, `bank_transactions` (o Pix da compra), `order_attachments` + URLs assinadas do bucket
  `order-attachments`, `material_groups`, `price_tables`/`price_table_items`, upsert em `stock_export_preferences`.
- **Arquivos:** o PDF abre numa aba nova (o robô segue a aba ~3 s e volta; se o gravador não seguir aba nova, a fala do
  PDF fica sobre a toast); o Excel só baixa (toast).
- **Setups fora do vídeo:** cap. 5 (Kardex do Ferro pesado em "Este ano"), cap. 7 (Kardex Geral), caps. 9, 10 e 11 (Relatório em "Mês passado"),
  cap. 13 (Posição em 31/10/2026 23:59 aplicada).
- Sem celular, sem página pública, sem outro usuário. Nada de erro encenado.
- **Ilustrações** (desenho no estilo da marca, `docs/09-aula-ilustrada.md`; nunca tela do app): caps. 0, 1, 2, 3, 4 (duas),
  5, 7 (duas), 8 (duas), 9 e 10. Descrição e frase de cada uma no roteiro.

## Riscos e decisões para o Kaik
1. **"Em massa" (cap. 3):** na 1.59.154 a transferência entre materiais é só a da linha. O "Transferir Estoque" da
   barra de seleção abre a "Transferência em Lote", que é entre matriz e filial (Gerencial, T22). Proposta: mostrar a
   barra sem clicar e dizer o que ela é. Alternativa: cortar a frase.
2. **Números do mundo:** a fala cita os valores da tabela acima; a consolidação das sementes precisa garanti-los.
3. **Fotos da compra:** imagem fictícia gerada (sem placa, rosto ou marca). Alternativa: compra sem foto e a fala troca
   "as fotos" por "e, quando tem, as fotos anexadas".
4. **"Todos os tempos"** é o rótulo da tela (a fonte diz "Todo o período"); a fala usa o da tela.

## 20/11/2026 · aplicação no 1.60.18 (o que mudou no plano)
- **Capítulos novos**: 7 "Achar uma movimentação" e 11 "Clientes, usuários e grupos". Renumeração: 7, 8, 9 viram 8, 9, 10; 10 vira 12; 11 vira 13;
  12 vira 14 (15 capítulos, 0 a 14). Fala de 1.776 para 2.470 palavras (~15,8 min de voz).
- **Mundo**: nada novo. O filtro "Usuários" usa o `created_by` que o mundo base já tem (outubro: Marcos lança quase tudo, Rafael alguns). Não há material sem
  compra (a frase do triângulo amarelo fica só falada) nem corte da empresa com uma tabela de preço só (o botão do cabeçalho fica só falado).
  A venda de 04/11 à Aços Quiririm (38.992 kg de Ferro pesado, Pix) já está no mundo base e abre no Kardex.
- **PDF e HTML na tela** (pedido do Kaik, 19/11): o robô devolve o PDF do Kardex (cap. 7), o PDF da Posição (cap. 13) e o HTML do Relatório de Estoque
  (cap. 13) no `actions.json`; as cenas `pdf` estão no `cenas/ilustracoes.json`.
- **Decisões que dependem do Kaik**: a dica do "Editar" (cap. 5) recomenda o "Movimentar estoque" (a observação ali é opcional, então a fala diz "tem o
  campo de observação"); o botão "Posição de Estoque" do cabeçalho e o triângulo amarelo ficam só falados, com ilustração (`ilu01_botao_posicao`,
  `ilu02_sem_historico`).
