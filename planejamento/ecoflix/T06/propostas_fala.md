# T06 · Propostas de fala e achados do app (ensaio do robô, 11/11/2026)

Do ensaio do robô (EcoSistema 1.59.154, Supabase falso na 54306, mundo base da junção). A revisão geral aplica; `roteiro.md` e
`tts_textos.py` não foram mexidos.

## Propostas de fala

| Cap. | Linha | Texto atual | Texto novo | Motivo |
|---|---|---|---|---|
| cap07 | L3 | "A principal: compra, venda, despesa e receita em dinheiro mexem só no caixa selecionado." | "A principal: o que entra e sai em dinheiro, como compra, venda, depósito e retirada, mexe só no caixa selecionado." | A janela "Como funcionam os Multi-Caixas?" diz "Transações de caixa (depósitos, retiradas, compras em dinheiro, vendas em dinheiro) afetam somente o caixa selecionado." A fala fica igual à tela que está na câmera. |

## Coluna Tela (não muda a fala)
- cap02 e seguintes: o horário de abertura gravado é o minuto do campo "Data e Hora de Abertura" no instante em que a janela abre
  (`opened_at` = o valor do campo). Com `FAKE_NOW` 08:30:00 o #85 sairia "Aberto em: 10/11/2026 08:30" (antes das 08:31 da linha do
  tempo); o robô grava o cap02 com `FAKE_NOW` 08:30:55, os caps 3 a 5 com 08:41:50 (o #86 abre às 08:42, "08:4x" do roteiro), os caps
  6 a 9 e o 8b com 08:45 e os caps 10 a 12 com 17:40. O relógio do topo da tela anda junto (08:30 → 08:45).
- cap06 L5: na volta do cofre o grupo "Financeiro" do menu vem fechado em "Movimentações Financeiras": o robô clica "Financeiro" e
  "Caixa" (o roteiro já diz "menu lateral Financeiro › Caixa").

## Achados do app
- O "?" ao lado das abas dos caixas (abre "Como funcionam os Multi-Caixas?") não tem nome acessível (sem `aria-label` nem `title`).
- "Diminuirá em R$ 3006,50" no saque sai sem separador de milhar (`WithdrawalForm.tsx:798`; já no inventário, H2).
