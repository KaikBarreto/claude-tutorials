# T11 · Produção: propostas de fala e achados do app

Ensaio do robô (`rec/t11/gerar.py`) contra o app 1.59.154 no mundo Recicla Vale Metais. **20/11 (1.60.18):** a proposta do cap06 (check logo depois de mostrar a coluna Concluída) e a dica do cap13/14 (Kardex)
foram aplicadas no `roteiro.md` e no `tts_textos.py`; os achados abaixo estão reavaliados na seção "Achados no 1.60.18".

## Propostas de fala

| Capítulo | Linha | Texto atual | Texto novo | Motivo |
|---|---|---|---|---|
| cap06 | 5 → passa a ser a 2 | "Na Recicla Vale, a coluna de conclusão é a Concluída. Repara no sinal de check do lado do nome." (hoje vem depois de "Salvar. Pronto, a coluna mudou de nome.") | Mesmo texto, logo depois da linha 1 ("Ele já vem com três: A fazer, Em produção e Concluída.") e antes de "As colunas são suas. Clicando no nome, você muda o nome e a cor..." | Depois de salvar qualquer coluna o app tira o check da coluna de conclusão até recarregar a página (achado 4). Com a fala atual, a tela não mostra o check que a fala pede. Na ordem nova o check aparece, e a chave "Coluna de conclusão" (linha 3) passa a explicar o que acabou de ser mostrado. O robô já segue a ordem das falas: com a ordem nova ele mostra o check antes da edição, sem mudar mais nada. |

## Notas para a edição

- cap00, linha 4 ("Se você ainda não viu o tutorial..."): o robô recolhe o menu lateral no começo da linha (o botão do topo).
  Sugestão de aviso na edição: "Dica: recolher o menu lateral dá mais espaço para o quadro". Sem o menu recolhido, a 1280 px
  o quadro e a ficha técnica ficam cortados (achados 1 e 2).
- cap02: o botão "+" (Criar novo produto) só aparece com o foco do teclado (Tab), porque o cartão "Produto final" fica
  cortado a 1280 px (achado 1).

## Achados do app

1. **Ficha técnica a 1280 px:** o cartão "Produto final" e o "+" (Criar novo produto) ficam cortados à direita
   (`RecipeList` com `md:grid-cols-[minmax(20rem,24rem)_minmax(0,1fr)]` e `RecipeFormDialog` com
   `lg:grid-cols-[1fr_auto_280px]`). Com o menu lateral aberto fica pior.
2. **Kanban a 1280 px:** o botão "Coluna" fica fora da faixa visível; é preciso rolar o quadro na horizontal.
3. **Ficha nova:** depois de salvar uma ficha técnica NOVA, o painel volta para "Selecione uma ficha técnica" em vez de
   mostrar a ficha salva (o efeito do `RecipeList` limpa a seleção antes de a lista recarregar).
4. **Check da coluna de conclusão some depois de salvar uma coluna** (até recarregar a página): `ProductionKanbanBoard`,
   `ProductionOrderDialog` e `FinalizeProductionDialog` usam a mesma chave de consulta
   `["production_kanban_columns", companyId]`, e o `select` da janela de ordem não traz `is_done`; o recarregamento da
   invalidação usa a consulta do último componente desenhado. O banco continua certo. Pelo código, até recarregar, arrastar
   um cartão para a coluna de conclusão só move o cartão, sem abrir "Finalizar".
5. **Motivo da perda cru no detalhe da ordem concluída:** aparece "reaproveitavel" em vez de "Material reaproveitável"
   (`ProductionOrderDetail.tsx`, perto da linha 590).
6. **Nome do menu:** o app diz "Histórico (Kardex)" (a fala nova já diz "o histórico do material, o Kardex").
7. **"Consumo por Kg"** mostra "1,6 Kg", e o roteiro escreve "1,60 Kg".
8. **"Nova ordem de produção":** ao abrir a janela, o campo de material ganha o foco e abre a lista sozinho.
9. **Kardex da produção:** o estorno da exclusão é tipo "Produção" com a observação "Estorno de produção (exclusão da OP)";
   a coluna do nº do pedido mostra "#-" nas linhas de produção (o Kardex tira o número da observação, e as observações da
   produção não têm "#").
10. **Unidade do custo:** o cartão da ordem mostra "R$ 28,80/peça" para o cobre mel, que é em Kg (a unidade da ficha vem
    "peça" por padrão). Também do inventário: a "Observação" do lançamento não fica salva.

## Mundo (para o coordenador)

- O mundo base novo tem 42 kg de cobre mel, e a fala do cap13 tira 50 kg ao excluir a #2. Para o estoque não ficar negativo,
  a semente da T11 deixa a #2 (a ordem duplicada) **por cima** do mundo base no cobre mel: na aula, o cobre mel é o do mundo
  base + 50 kg até o cap13, e a exclusão devolve exatamente o do mundo base. O fio de cobre é o do mundo base. Os saldos são
  lidos da semente base (`rec/t11/t11_sementes.py`), sem número fixo.

## Achados no 1.60.18 (para o MELHORIAS)

- **Corrigido**: "Observação" do lançamento agora grava (`p_note`); a palavra "peça" sumiu do aviso de finalizar ("custo/Kg") e do cartão
  ("R$ x/Kg") em produto por quilo.
- **Novo**: o cabeçalho do gráfico do relatório diz "Total: N peças" fixo, mesmo em produtos por quilo (`ProductionReport.tsx`, perto da linha 1300).
- **Ainda "peça" em produto por quilo**: "Custo estimado por peça" na janela da ordem e na Conversão; "Custo/peça" no relatório; "Peças por jogo" /
  "Peças por unidade de venda" (Configurações, ordem e Conversão, rótulos diferentes para a mesma coisa).
- **Aviso de exclusão de ordem concluída**: o texto de estorno aparece só na Lista; o Kanban mostra o texto genérico (a conferir no ensaio).
- **Texto da equipe**: "Na finalização você informa quanto cada um produziu" ainda aparece na ordem, mas o lançamento por funcionário é por dia.
- **Bugs antigos (1 a 5 acima)**: o check da coluna e o retorno a "Selecione uma ficha técnica" dependem de conferência no ensaio de 20/11
  (ver `andamento_160.md`); o motivo cru "reaproveitavel" idem.
