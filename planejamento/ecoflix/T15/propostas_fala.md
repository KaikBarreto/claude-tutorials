# Propostas de fala · T15 · Relatório Financeiro e DRE

Do ensaio do robô (11/11, app 1.59.154, mundo da junção com a seção 16 aplicada). Não editei `roteiro.md` nem `tts_textos.py`: a
revisão geral aplica. Linhas numeradas como no `capNN.json` (L1 = primeira linha da tabela do capítulo, sem a vinheta).

## O que a fala precisa mudar

| Cap. | Linha | Texto atual | Texto novo | Motivo |
|---|---|---|---|---|
| 02 | L3 | "A terceira frente vai ser a produção, a prensa que enfarda latinha e papelão." | "Agora, uma frente nova: a produção, a prensa que enfarda latinha e papelão." | A lista já tem quatro centros (Coleta, Escritório, Frota e Pátio: o T13 criou Escritório e Frota e a junção manteve). "Terceira" só vale para a ilustração. A coluna Tela do cap02 também diz "a lista com Coleta e Pátio": são quatro. |
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
