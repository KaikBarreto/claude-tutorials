# T14 · propostas de fala e achados do app (1.60.18, 20/11)

As propostas antigas já estão aplicadas em `narracao/tts_textos.py` (19 capítulos, 3.209 palavras, cerca de 20,6 min).

## Atrasos previstos (fala estimada; refazer com `preparar_aula.sh T14` depois da voz)
Gesto mais longo que a fala em: cap01 "olho" (1,9 s) e "Exportar o PDF" (1,7 s); cap05 L5 (2,1 s); cap06 "Rastreador" (2,2 s);
cap07 "O que é conciliar" (0,9 s); cap09 L4 (3,2 s); cap11 L6 (0,4 s); cap12 L2 (1,1 s); cap17 L2 (7,6 s, a conferência de duas
vendas espera a tela). Se a voz real não abrir folga, alongar essas linhas ou tirar o gesto opcional.

## Achados do app
- Rótulos 1.60.18: selo "Casada"; menu "Movimentações Financeiras"; "Abra o caixa antes de realizar saques" não existe.
- Sugestão de preenchimento: só aparece com 2 usos ou descrição idêntica usada nos últimos 90 dias; traz receita lançada direto no banco.
- Extrato do banco abre como relatório HTML em aba nova (o robô devolve o HTML para a tela).
- Saldo do cliente/fornecedor: o parceiro já vem do sentido do Pix (saída = fornecedor); o campo mostra "Selecionar".
- Painel "Casar com vários lançamentos": botão só habilita com 2 ou mais marcados.
- DRE no regime de caixa não conta compra no cartão até pagar a fatura (aviso na fala do cartão).
