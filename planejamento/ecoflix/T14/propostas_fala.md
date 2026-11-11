# T14 · Propostas de fala (ensaio do robô, 11/11/2026)

O que a fala precisa mudar para bater com a tela do app 1.59.154 e com o mundo da junção (`MUNDO_LINHA_DO_TEMPO.md`, seções 8, 14 e 15),
ou para caber no gesto. Linha = linha da tabela Tela × Fala do capítulo no `roteiro.md` (1 = a primeira com fala). Nada foi aplicado no
`roteiro.md` nem no `tts_textos.py`. As âncoras do robô (`rec/t14/gerar.py`) usam palavras que continuam nos textos novos.

## Fala

| Cap. | Linha | Texto atual | Texto novo | Motivo |
|---|---|---|---|---|
| 12 | 1 | "... Um foi pra Cooperativa Recomeço; o outro, pra Auto Peças Vale Forte." | "... Um foi pra Aparecida Ramos; o outro, pra Auto Peças Vale Forte." | Junção (seção 15): o Pix de R$ 380,00 de 06/11 09:40 é a compra de PET da Aparecida. Na tela: "PIX ENVIADO APARECIDA RAMOS" e "Compra #1747 • Aparecida Ramos". |
| 12 | 3 | "... e o nome no extrato diz qual é: a da Cooperativa Recomeço." | "... e o nome no extrato diz qual é: a da Aparecida Ramos." | Idem. |
| 12 | 4 | "Marco a compra da cooperativa, e Casar com o selecionado." | "Marco a compra da Aparecida, e Casar com o selecionado." | Idem. |
| 7 | 5 | "Então é em Mais ações, Casar com transferência. Aparece a transferência certa, ..." | "Pra transferência, o caminho é Mais ações, Casar com transferência. Aparece a transferência certa, ..." | A linha dos R$ 8.000,00 chega COM a sugestão verde "Transferência: Conta Secundária → Conta Principal" e o botão "Confirmar" (a perna de entrada é um `deposit` sem pedido, que a sugestão aceita). O "Então" soa como se não houvesse outro caminho; o robô vai por "Mais ações", como a fala. |
| 14 | 2 | "A Diferença é a distância entre os dois. Agora ela está em zero, em verde, ..." | "A Diferença é a distância entre os dois. Ela está em zero, em verde, ..." | No app o Saldo conciliado soma todas as linhas não ignoradas, inclusive as pendentes: a diferença já está em R$ 0,00 logo depois da importação (cap06). O que libera o fechamento é não sobrar linha pendente. |
| 14 | 4 | "Uma dica: se a diferença não zerar, falta lançamento, sobra lançamento ou alguma linha foi ignorada sem motivo. Cada linha se resolve de verdade, ..." | "Uma dica: o fechamento só libera com todas as linhas resolvidas e a diferença em zero. Se ela não zerar, alguma linha foi ignorada sem motivo. Cada linha se resolve de verdade, ..." | Pela fórmula do app (`get_bank_reconciliation_state`), só linha ignorada (ou um saldo final do arquivo diferente) tira a diferença do zero; lançamento faltando ou sobrando aparece como linha pendente, não como diferença. |

Ilustrações (coluna Tela do roteiro):
- **cap00**: o painel do sistema mostra R$ 46.382,57, número que não aparece em nenhuma tela da aula (é o saldo de 31/10, a abertura que o
  app calcula e não mostra). Na hora da importação a tela mostra "Conta Principal · R$ 45.236,97" (seletor "Conta para conciliar") e o
  banco R$ 44.933,47: a diferença de R$ 303,50 é a água (238,40) + a tarifa (64,90) + os centavos da Serra Fina (0,20), tudo o que a aula
  resolve. Proposta: "R$ 45.236,97" no lugar de "R$ 46.382,57".
- **cap12**: "R$ 380,00 · APARECIDA RAMOS" e "200 kg de plástico PET · Aparecida Ramos" no lugar da cooperativa.
- **cap06** (Tela, rodapé depois da importação): "Saldo do banco" R$ 44.933,47, "Saldo conciliado" R$ 44.933,47, "Diferença" R$ 0,00 e
  "Ainda há 17 linhas pendentes" (não R$ 46.382,57 / R$ -1.449,10). A fala ("os três números do fechamento") vale.

## Achados do app

1. **Rodapé da conciliação** (`ReconciliationBalanceFooter.tsx:14-22`, `get_bank_reconciliation_state`): "Saldo conciliado" = abertura +
   Σ das linhas não ignoradas, inclusive as pendentes; como a abertura é o saldo final do arquivo − Σ das linhas, a "Diferença" fica em
   R$ 0,00 desde a importação e só sai do zero com linha ignorada. O plano esperava R$ 46.382,57 e R$ -1.449,10 depois da importação.
2. **Transferência sugerida**: a linha XFER de R$ 8.000,00 ganha sugestão automática da perna de entrada da transferência (o pool aceita
   `deposit` sem pedido na janela de 3 dias); o roteiro previa "Sem casamento automático".
3. "Cancelar conciliação" abre uma janela comum (`role=dialog`), com a lista na ordem: "17 linha(s) do extrato serão canceladas", vínculos,
   contas reabertas, lançamentos criados, ignoradas (o roteiro bate).
