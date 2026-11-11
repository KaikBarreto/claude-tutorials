# T07 · propostas de fala e achados do app (ensaio do robô, 11/11/2026)

Robô: `$TUT_HOME/rec/t07/gerar.py` (voz estimada). App 1.59.154, mundo base da junção (seção 16), `FAKE_NOW` 10/11 08:35.
Não editei `roteiro.md` nem `tts_textos.py`: a revisão geral aplica.

## Propostas de fala

| Cap. | Linha | Texto atual | Texto novo | Motivo |
|---|---|---|---|---|
| 04 | 4 | "O Zé é novo e está na tabela principal, então vale o preço de cada material." | "O Zé é novo e está na tabela principal, então vale o preço dessa tabela." | No mundo base a tabela "Principal" tem preço explícito dos 15 materiais (`price_table_items`, estado do T3): ao escolher o material a tela avisa "Preço da tabela aplicado para Cobre misto" (visto na folha de contato do cap05). O valor é o mesmo do cadastro (R$ 36,00). |
| 05 | 1 | "O preço veio do cadastro do material: trinta e seis reais o quilo." | "O preço veio da tabela principal: trinta e seis reais o quilo." | Mesmo motivo: o aviso "Preço da tabela aplicado para Cobre misto" aparece na tela junto da fala. |
| 10 | 5 | "Escolho as três formas." | "O dinheiro já vem marcado: escolho também o Pix e o saldo." | Ao abrir o "Finalizar Pedido", "Dinheiro" já vem marcado (forma padrão, `MultiPaymentDialog.tsx:217,433-437`); clicar nele de novo, com "Múltiplas formas de pagamento" ligada, DESMARCA. O robô só passa o mouse no Dinheiro e clica Pix e Saldo. Opcional: a fala atual também vale. |

## Achados do app e do mundo

- **Nome da balança**: o mundo usa a do T5, "Balança do pátio" (EcoTray falso e visor "BALANÇA DO PÁTIO"); o plano/roteiro do cap05
  (cena de Windows) fala em "● Balança". A cena de Windows deve mostrar "Balança do pátio" para bater com o visor gravado.
- **Casas do peso**: a semente `base/balanca-ativada` tem `balanca_decimais: 1`, e o campo mostra "12,4", "21,6", "152,0" (o roteiro diz
  "12,400"; o plano, "3 casas (T5)"). A fala não depende.
- **Caixa #85**: aberto às 08:31 com R$ 1.500,00 (linha do tempo); o `MUNDO_FICTICIO.md` ainda diz "caixa aberto com R$ 2.500" na T7.
  A fala não diz o valor. A semente `base/caixa-aberto` abre o #85 às 08:05: a T7 não a usa (`t07/inicio` abre às 08:31).
- **Botão do Cato** (canto inferior direito) cobre o fim do "Total da Compra" com a página no topo; o robô rola o formulário 140 px no
  início (o "Incluir Item" também fica fora da faixa de clique, y 761).
- **Esc** na janela "Selecionar Fornecedor", depois de passar o mouse no indicador âmbar, não fecha a janela (o balão consome o Esc).
- Pedidos: o próximo número no mundo novo é #1759 (histórico #1253 a #1758).
- **Itens do Pedido a 1280 px** (menu recolhido): as células editáveis cortam o número ("446,4" no Valor Total do cobre, "130,2" na
  latinha, "21" no peso), visto nas folhas de contato dos caps. 05 e 09. A fala não depende; zoom na linha mostra o corte.
- **Resumo do Pedido** flutua ao lado da janela "Finalizar Pedido" (fora dela), como o roteiro pede.
- **Plano/roteiro do cap05** ("tabela padrão sem item explícito, então sem aviso de preço"): no mundo base a Principal tem itens, e o
  aviso "Preço da tabela aplicado" aparece (ver propostas dos caps. 04 e 05).
