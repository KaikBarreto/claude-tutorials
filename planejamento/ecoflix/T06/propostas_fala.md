# T06 · Propostas de fala e achados do app (robô e ensaio, 11/11/2026)

Do ensaio do robô (EcoSistema 1.59.154, Supabase falso na 54306, mundo base da junção de 11/11). A revisão geral aplica;
`roteiro.md` e `tts_textos.py` não foram mexidos.

## Propostas de fala

| Cap. | Linha | Texto atual | Texto novo | Motivo |
|---|---|---|---|---|
| cap07 | L3 | "A principal: compra, venda, despesa e receita em dinheiro mexem só no caixa selecionado." | "A principal: o que entra e sai em dinheiro, como compra, venda, depósito e retirada, mexe só no caixa selecionado." | A janela "Como funcionam os Multi-Caixas?", que está na câmera, diz "Transações de caixa (depósitos, retiradas, compras em dinheiro, vendas em dinheiro) afetam somente o caixa selecionado." |

## Coluna Tela (a fala não muda)
- **Horário dos caixas.** O app grava a abertura com o minuto do campo "Data e Hora de Abertura" no instante em que a janela abre
  (o campo já vem com a hora atual). Com `FAKE_NOW` 08:30:00 em todos os capítulos da manhã o #85 sairia "Aberto em: 10/11/2026 08:30"
  e o #86 também, antes das 08:31 da linha do tempo. O relógio anda pela manhã como a história: cap00 e cap01 08:30:00; cap02 08:30:55
  (o #85 abre às 08:31); caps 3 a 5 08:41:50 (o #86 abre às 08:42, o "08:4x" do roteiro); caps 6 a 9 e o 8b 08:45:00; cap10 17:40:00
  (fecha às 17:42); cap11 17:42:40 (reabre às 17:43); cap12 17:44:00. O relógio do topo da tela anda junto.
- **cap01 L5.** O Shift+C abre "Nova Compra" (selo "Selecione um caixa") por 1 a 3 s antes do aviso "Abra o caixa antes de realizar
  compras" e da volta ao /caixa. O robô aperta o atalho em "lançar", e o aviso sobe em "o sistema avisa".
- **cap06 L5.** Em "Movimentações Financeiras" o grupo "Financeiro" do menu vem fechado: o robô clica "Financeiro" e "Caixa" (o roteiro
  já diz "menu lateral Financeiro › Caixa").
- **cap08.** O trecho do Marcos (L4 e L5) é o `cap08b` (outro navegador, logado como Marcos Antunes, `voz_inicio` = início da L4); o
  `cap08` acaba no início da L4.
- **cap09 L12/L13.** A sangria não é confirmada: a janela fecha com Esc no fim de "...a conta do banco que recebe." ("Cancelar" fica
  abaixo da dobra, y 886, e rolar até ele não cabe no vão entre as linhas). Visualmente é o mesmo: a janela fecha.
- **cap12.** O roteiro pede montagem com trechos dos capítulos; o robô grava um passeio de reserva pelo estado final (#85 reaberto).

## Achados do app
- O "?" ao lado das abas dos caixas (abre "Como funcionam os Multi-Caixas?") não tem nome acessível (sem `aria-label` nem `title`;
  `CashRegisterTabs.tsx:198-206`).
- "Diminuirá em R$ 3006,50" no saque sai sem separador de milhar (`WithdrawalForm.tsx:798`; inventário, H2).
- A abertura fica com o minuto em que a janela "Abrir Caixa" abriu, não o do clique em "Abrir Caixa" (o campo "Data e Hora de
  Abertura" é preenchido ao abrir a janela e enviado como está): janela aberta às 08:30:50 e confirmada às 08:31:20 grava 08:30.
- Reabrir (`Caixa.tsx:830-875`) apaga as linhas de diferença e de ajuste do fechamento, mas mantém a linha "Fechamento de caixa"
  (`closing`) do caixa reaberto; o saldo do caixa e o do cofre a ignoram, então nada muda na tela (só registro).
