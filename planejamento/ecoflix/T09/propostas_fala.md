# Propostas de fala · T9 "Pedidos e histórico do caixa"

Do robô e do ensaio (app 1.59.154, mundo base de 11/11 13:35, `FAKE_NOW` 2026-11-11T08:30:00-03:00, instância 54309). A revisão
geral aplica; `roteiro.md` e `tts_textos.py` não foram mexidos.

## Fala

| Cap. | Linha | Texto atual | Texto novo | Motivo |
|---|---|---|---|---|
| cap04 | L10 | "Finalizar Compra, em dinheiro, Confirmar pagamento." | "Finalizar, em dinheiro, Confirmar pagamento." | Na edição o botão é "Finalizar" (`Purchase.tsx`, rodapé da tela Compra); "Finalizar Compra" não aparece na tela. |

## Coluna Tela (sem mudar a fala)

- **Caixa do Rafael: #88** (coordenador, 11/11), não #87: abas "#88 \| Caixa - Rafael Nogueira (você)" (cap09) e "Volta para Caixa #88" na
  prévia da exclusão (cap05). Não existe #87 no mundo da aula (lacuna que nenhuma tela mostra).
- cap02 L2: o cartão "Resumo do período filtrado" abre FECHADO (só os totais de Compras e Vendas); o robô clica nele para mostrar
  Dinheiro, Pix/Transferência (Conta Principal) e Saldo, que a fala cita.
- cap02 L4: a linha aberta mostra "MATERIAL", "PESO", "VALOR UNIT.", "TOTAL" e "Formas de Pagamento" (o roteiro dizia "V.Unit.").
- cap03 L3: o painel "Filtrar pedidos" cobre as colunas da direita da lista; o robô o fecha (Esc) para o zoom nas compras da Vale
  Forte e abre de novo no fim da L3. Cada lista de opções (Tipo, Material) abre por cima do campo de baixo: o robô fecha cada uma com Esc.
- cap05 L4-L5: a dica do selo "Estornado em 05/11" é o `title` do navegador ("Estornado — correção lançada no caixa de hoje"), que
  não aparece na gravação: o robô passa o mouse no selo e lê o texto; a edição mostra como aviso "Ao passar o mouse: ...".
- cap05: a lista de "Este mês" mostra 10 pedidos por página; o capítulo entra com 50 por página (preferência do próprio app,
  `orders_table_items_per_page`) para as compras de 03/11 estarem na mesma página.
- cap05 L7: o menu lateral fica recolhido na aula (a tabela de Pedidos só cabe inteira assim) e, recolhido, não mostra "Configurações":
  o robô abre o menu e clica em "Configurações" no rodapé.
- cap06, cap08, cap09: o vídeo grava uma aba só. Os PDFs (comprovantes, relatório de fechamento) e o "Relatório de Estoque do Caixa #70"
  (HTML) que o app abre em aba nova saem do próprio app para `rec/t09/pdfs/` e entram na edição como ilustração.
- cap07 L4: o robô abre o resumo do #85 (o caixa do Rafael de ontem, com compras e venda), não o #86: o #86 do Marcos não tem pedido
  e o resumo sairia todo em R$ 0,00.
- cap09 L5: [TESTAR] conferido: trocar o fornecedor para a Auto Peças Vale Forte mantém o item a R$ 3,10 (240 kg, R$ 744,00).

## Achados do app

- Pedidos, linha aberta: o peso sai com ponto decimal, "24.00 Kg" (em pt-BR seria "24,00 Kg").
- Menu lateral recolhido: o rodapé só tem o avatar e "Sair"; "Configurações" some (`SidebarMenuContent.tsx`, ramo `collapsed`).
- Selo "Estornado em dd/MM": a explicação está só no `title` (dica nativa), invisível no celular e em gravação.
- Histórico do Caixa > "Ver comprovante": o PDF do relatório de fechamento do #70 tem ~15 MB (os comprovantes de pedido têm ~30 KB).
- Tela Compra em edição: a barra de pedidos ao lado mostra outro número ("#1766 R$ 0,00 Sem fornecedor", o próximo pedido novo)
  enquanto o selo diz "Editando Compra #1763".
- (do inventário) "Reabrir Último Caixa?" também para caixa antigo; o texto do "Editar Pedido" fala do caixa fechado mesmo com a origem aberta.
