# Propostas de fala · T15 · Relatório Financeiro e DRE

Do ensaio do robô (11/11, app 1.59.154, mundo da junção com a seção 16 aplicada). Não editei `roteiro.md` nem `tts_textos.py`: a
revisão geral aplica. Linhas numeradas como no `capNN.json` (L1 = primeira linha da tabela do capítulo, sem a vinheta).

## O que a fala precisa mudar

| Cap. | Linha | Texto atual | Texto novo | Motivo |
|---|---|---|---|---|
| 02 | L3 | "A terceira frente vai ser a produção, a prensa que enfarda latinha e papelão." | "Agora, uma frente nova: a produção, a prensa que enfarda latinha e papelão." | A lista já tem quatro centros (Coleta, Escritório, Frota e Pátio: o T13 criou Escritório e Frota e a junção manteve). "Terceira" só vale para a ilustração. A coluna Tela do cap02 também diz "a lista com Coleta e Pátio": são quatro. |
| 10 | L3 | "Dá pra filtrar também por cliente ou fornecedor, por centro de custo e pela fonte." | "Dá pra filtrar também por cliente ou fornecedor e por centro de custo." | O filtro "Fonte" só aparece quando a lista tem mais de uma fonte (`RevenueExpenseList.tsx:889`, `sources.length > 1`); as despesas de outubro são todas do banco, então o painel mostra só Categoria, Cliente/Fornecedor e Centro de custo. |
| 10 | L5 | "Clico na lixeira da segunda e em Excluir." | "Clico na lixeira da primeira, a que foi lançada depois, e em Excluir." | A lista mostra a mais nova em cima: a cópia das 16:40 é a 1ª linha e a das 09:12 (a que o mundo mantém, T21) a 2ª. O robô exclui a das 16:40. |

## Achados do app

1. **Comparar períodos perde a comparação na primeira vez** (cap09). "Aplicar comparação" chama `onPeriodChange` e o filtro vira
   "Personalizado" (01/10/26 → 31/10/26); a consulta do DRE tem o nome do filtro na chave (`pages/FinancialReport.tsx:189-190`), a aba
   troca o DRE pelo esqueleto de carregamento (`:643-660`) e o `FinancialDRE` remonta com `comparisonSelections` vazio
   (`components/financial-report/FinancialDRE.tsx:511`, `:1526-1529`): as colunas de setembro não aparecem. Aplicando de novo (o filtro
   já é Personalizado, a chave não muda) as colunas ficam. O robô aplica uma vez no `setup` (fora do vídeo) e o capítulo mostra o
   filtro em "Personalizado", não em "Mês passado".
2. **Evolução Mensal com formato diferente do resto** (cap09): margem com ponto ("4.6%", "26.1%", "-1.1%") e resultado com o sinal
   depois do símbolo ("R$ -34.300,00"); o DRE ao lado usa "2,4%" e "-R$ 31.500,00".
3. **Diálogo de excluir** (cap10): "Conta de energia será removido e o saldo da conta a conta bancária será ajustado em R$ 3.850,00."
   (`RevenueExpenseList.tsx:1199` passa `accountName="a conta bancária"`; já estava no plano como handoff).
4. **Rótulo "07 (-) Outras Receitas e Despesas"** com o aluguel de caçamba (receita) somando R$ 2.800,00 ao resultado: o "(-)" do
   rótulo não combina com a linha que soma.
5. **Relatório abrindo** (cap03): entre "Processando relatório..." e os números, o banner mostra por ~0,5 s "R$ 0,00 · Equilibrado" e
   "Nenhuma despesa no período" (o banner desenha antes das consultas). Na montagem, um corte curto em ~7,8 s do cap03 resolve.

## Para a edição e a gravação final
- Cap09: o `setup` aplica a comparação uma vez (defeito do achado 1); na tela o filtro aparece "Personalizado 01/10/26 → 31/10/26".
- Cap10: a ilustração usa R$ 4.250,00 (compra de cobre), que não existe no mundo; a tela não mostra esse valor (a ilustração cobre o
  Histórico filtrado pela energia), então não há conflito. Se quiser um número do mundo: a compra #1605 de 08/10 (34 kg de cobre mel,
  R$ 1.445,00, dinheiro, balcão).
- Cap11: "Exportar PDF" abre uma aba nova (o robô fica na do relatório) e o aviso "PDF gerado em nova aba" aparece.
