# T25 · propostas de fala e achados do app (robô)

Gerado pelo robô da aula (`$TUT_HOME/rec/t25/gerar.py`). Voz ainda ESTIMADA. Não altera `roteiro.md` nem `tts_textos.py`: a revisão
geral aplica tudo de uma vez. Esta lista é parcial até o ensaio completo fechar; a seção final registra o que fechou.

## Propostas de fala

| Cap./linha | Texto atual | Texto novo | Motivo |
|---|---|---|---|
| (a preencher pelos ensaios) | | | |

## Achados do app

- **Compra estornada no Dashboard.** `get_dashboard_operacao` (migração 20260909163000) só filtra `status = 'completed'`: pedido
  estornado conta nos cartões do painel de operação, ao contrário de `get_monthly_purchases_sales`, `get_financial_dre_summary`
  (caixa) e `get_top_materials`, que o excluem. É assim no app real; o falso passou a imitar.
- **Compra de balcão no ranking de fornecedores.** `get_top_partners` rotula a compra sem cadastro como "Sem cadastro" (nos
  clientes também), não "Sem fornecedor"/"Sem cliente". O falso foi corrigido para o rótulo do app.
- **Título da tarefa do cap. 5.** O `plano.md` diz "Revisão do caminhão FKD2E41"; o `roteiro.md` e a fala dizem "Revisão do
  caminhão truck". O robô digita "Revisão do caminhão truck" (segue a fala).
