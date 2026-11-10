# Plano · T10 · Estoque: saldo, histórico e posição

- **Título:** Estoque: saldo, histórico e posição (o da fonte). **Antes:** T9 "Pedidos e histórico do caixa".
  **Próximo:** T13 "Contas a Pagar e Receber".
- **Objetivo:** responder as três perguntas do contador da Recicla Vale Metais: quanto tem hoje (Estoque), de onde
  veio (Histórico/Kardex) e quanto tinha no dia 31 (Posição de Estoque); e ler o Relatório de Estoque do mês.
- **Áreas das vinhetas:** ESTOQUE · HISTÓRICO · RELATÓRIO · POSIÇÃO · RESUMO.
- **Alvo da fonte:** ~16 min. Desktop (janela 1280×800), logado como **Rafael Nogueira** (MASTER: vê valores e exporta).
  `FAKE_NOW=2026-11-10T08:30:00-03:00` (terça). Sem módulo 🔒 próprio; cita o Gerencial e a Produção como
  "depende do plano contratado".
- Base: `T10/inventario.md` (código 1.59.154).

## Capítulos (os da fonte, na ordem)

| # | Vinheta (área / título) | O que se mostra | Ilustração | Estado de partida |
|---|---|---|---|---|
| 0 | (sem vinheta) | Abertura: as três perguntas do contador; menu "Materiais"; cartão "Antes" | as três perguntas | `inicio` |
| 1 | ESTOQUE / As quatro portas do estoque | "Materiais" → "Estoque", "Histórico", "Relatório"; a "Posição de Estoque" na coluna "Tabelas de Preço" | as quatro portas | `inicio` |
| 2 | ESTOQUE / O saldo de cada material | cartões "Peso Total em Estoque", "Total Pago", "Projeção de Vendas"; linha do Cobre mel ("Estoque Atual", "Preço médio pago"); Ferro misto | o que mexe no saldo | `inicio` |
| 3 | ESTOQUE / Transferir entre materiais | "Transferir estoque" do Ferro misto para o Ferro pesado, 320 kg; a barra de seleção ("Transferir Estoque" = Transferência em Lote, Gerencial) só mostrada | a separação no pátio | `inicio` → `apos-cap03` |
| 4 | HISTÓRICO / O Kardex, linha a linha | "Histórico de Materiais", "Geral (Todos)" → "Ferro pesado"; a corrente Estoque Inicial → Movimentação → Estoque Final; ⚠️ "Este mês" → "Este ano" | Kardex = extrato; a corrente | `apos-cap03` |
| 5 | HISTÓRICO / Os tipos de movimentação | selos; "Tipo de movimentação" (os sete); "Edição Manual" de 31/10 aberta (observação); "Exclusão" de 22/10; ⚠️ filtro "Fornecedores" | os tipos no pátio | `apos-cap03` (setup: Ferro pesado, "Este ano") |
| 6 | HISTÓRICO / O pedido por trás da linha | a compra de 09/11 aberta: itens, "Fornecedor:", "Formas de Pagamento", "Total do Pedido:", "Fotos anexadas" | (só tela) | `apos-cap03` |
| 7 | RELATÓRIO / Comprado, vendido e lucro | "Relatório de Estoque", "Mês passado"; os quatro cartões; "Total Comprado" aberto; "Projeção de Lucro"; ⚠️ saldo ≠ comprado − vendido; ⚠️ só pedidos finalizados | a projeção; Estoque × Relatório lado a lado | `apos-cap03` |
| 8 | RELATÓRIO / Material por material | "Detalhamento por Material": Cobre mel de outubro (preço médio, Resultado, Margem, Lucro s/ Vendas); ⚠️ quantidade líquida; ⚠️ Bateria automotiva sem venda | resultado e margem; peso líquido | `apos-cap03` (setup: "Mês passado") |
| 9 | RELATÓRIO / O filtro de fornecedor | "Fornecedores" → "Depósito Irmãos Siqueira": só compras; desmarca | a pilha sem dono | `apos-cap03` (setup: "Mês passado") |
| 10 | POSIÇÃO / A foto do estoque numa data | "Posição de Estoque" de hoje; calendário → 31/10, 23:59; "Ver posição"; Ferro pesado 41.860 kg; "Valor", "Projeção venda", "Total geral" | a foto numa data | `apos-cap03` |
| 11 | POSIÇÃO / Exportar para o contador | "Exportar" → "PDF" ("Exportar estoque (PDF)") → aba do PDF; "Excel"; os "Exportar" do Histórico e do Relatório | (só tela) | `apos-cap03` (setup: 31/10 aplicado) |
| 12 | RESUMO / Recapitulando | montagem do que foi feito; cartão "Próximo: Contas a Pagar e Receber" | | |

Transições faladas: 1 "Vamos às quatro portas"; 2 "Esta é a tela do saldo"; 3 "Agora, a transferência"; 4 "Agora o
Histórico, de onde veio cada quilo"; 5 "Cada linha tem um tipo"; 6 "Toda linha de compra ou de venda abre o pedido";
7 "Agora o Relatório de Estoque"; 8 "Embaixo dos cartões"; 9 "Agora repara o que acontece quando eu filtro";
10 "E a terceira pergunta do contador"; 11 "Com a foto do dia 31 na tela, é só exportar".

**Cuidados (⚠️) na fala, com "Uma dica:"**: saldo do Estoque ≠ comprado − vendido do Relatório (cap. 7, com a
ilustração lado a lado); período em "Este mês" (cap. 4, trocando para "Este ano"; a opção da tela é "Todos os tempos");
quantidade comprada líquida (cap. 8, peso líquido); filtro de Fornecedores/Clientes no Kardex tira manual, transferência
e exclusão (cap. 5); compra sem venda não é erro (cap. 8, Bateria automotiva); só pedidos finalizados, pela data do
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
| Ferro pesado, novembro | (junção, `MUNDO_LINHA_DO_TEMPO.md`) 03/11 09:40 compra do Depósito Irmãos Siqueira +640 kg, Pix da Conta Secundária (→ 42.500); 04/11 venda à Aços Quiririm Ltda −38.992 kg, Pix (→ 3.508); 05/11 venda à Aços Quiririm no saldo −2.608 kg (T4) (→ 900); 06/11 compra do Depósito Irmãos Siqueira no saldo +1.200 kg (T4) (→ 2.100); 06/11 14:05 compra da Auto Peças Vale Forte +400 kg, Pix da Conta Principal (T14) (→ 2.500); 06/11 15:30 venda à Aços Quiririm Ltda −1.180 kg (→ 1.320); **09/11 15:20 compra do Depósito Irmãos Siqueira +860 kg a R$ 0,95 = R$ 817,00, paga em Pix (Conta Secundária: o extrato da Conta Principal da T14 não tem esse Pix), com 2 fotos** (→ **2.180 kg**) | caps. 4, 6 e 10 |
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
- **Setups fora do vídeo:** cap. 5 (Kardex do Ferro pesado em "Este ano"), caps. 8 e 9 (Relatório em "Mês passado"),
  cap. 11 (Posição em 31/10/2026 23:59 aplicada).
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
