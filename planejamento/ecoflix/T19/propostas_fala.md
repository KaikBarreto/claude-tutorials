# Propostas de fala · T19 · Funcionários e ponto eletrônico

Do robô e do ensaio (11/11/2026, EcoSistema 1.59.154, voz ainda estimada). O que a fala precisa mudar para bater com a tela ou caber
no gesto. Nada aqui foi aplicado: `roteiro.md` e `tts_textos.py` ficam para a revisão geral. Linha = número da linha do capítulo
(1 = primeira linha da tabela Tela × Fala). Gerador: `$TUT_HOME/rec/t19/gerar.py` (lê a voz de `t19/narracao/capNN.json`).

| Cap. | Linha | Texto atual | Texto novo | Motivo |
|---|---|---|---|---|
| 09 | 3 | (não existe no `tts_textos.py`) | Depois vem a selfie. Ela sai sozinha quando o rosto fica no centro, ou é só tocar em Tirar foto agora. | O `roteiro.md` (10/11 03:34) tem a linha da selfie e o `tts_textos.py` (10/11 01:24) não: a voz estimada do cap09 tem 5 linhas e o roteiro 6. O gerador aceita as duas versões (com a linha, o toque em "Tirar foto agora" cai na palavra "Tirar"; sem ela, logo antes da confirmação). |
| 11 | 5 | No lápis dela, troco os horários de segunda a sexta e deixo uma hora de intervalo. Salvar jornada, e a folha dela passa a esperar esse horário. | (mesmo texto, com respiro de ~7 s antes de "Salvar jornada") | Os dez horários (entrada e saída de seg a sex) são escolhidos na roleta de horas do app (`TimeField`): ~6 s de tela, o trecho acelerado (selo 4x) que o roteiro já marca. A voz precisa do vão: `pausas.py 11 <T>:7.0` no fim de "intervalo." (o gerador avisa o T na voz nova). |

## Roteiro × tela (para a revisão; a fala não muda)

- **Menu lateral recolhido nos caps 1 a 13** (o plano pede aberto): a 1280 px com o menu aberto, a faixa de abas corta
  "Configurações de RH" e esconde "Dashboard" (cap01 fala das duas e clica no Dashboard), e a ficha à direita corta o nome
  ("Ed..."). O cap00 fica com o menu aberto (o item "Funcionários (RH)" é o assunto). Sugestão: um aviso na edição do cap01
  ("Dica: recolher o menu lateral dá mais espaço para a tela"), como no T8.
- **Links do ponto no formato da 1.59.154:** o plano usa `gabriel-rocha-4f7k` e `recicla-vale-metais-2h6p`; na 1.59.154 o link
  pessoal é `{empresa}-{primeiro nome}-{CÓDIGO12}` e o do tablet `{empresa}-{CÓDIGO12}` (migrations 20260926140000 e
  20260926131000). O mundo segue o app: Gabriel `recicla-vale-metais-gabriel-8G9H5WS6MRTY`, tablet
  `recicla-vale-metais-4WNB8KBQ4BQP` (o cartão "Tablet da empresa" do cap08 mostra o link). A fala não diz o link.
- **Cadastro fiscal:** a calculadora lê o regime da config fiscal do mundo base (`fiscal.matriz`, Lucro Real); a semente da aula só
  confirma `is_simples_nacional = false` (sem inserir outra config).
- **Categoria da folha:** o app procura "Folha Salarial" (`utils/payrollCategory.ts`); o mundo base tem "Folha salarial". A semente
  da aula renomeia a de B (sem isso o 1º vale cria uma categoria nova). Sugestão para B: o nome do app.

## Achados do app

1. "Saldo: R$ 1500.00" com ponto no "Registrar Vale" (handoff 4 do plano, `EmployeeMovementModal.tsx:413,428`): aparece no cap05.
2. Na 1.59.154 o ajuste de salário é gravado pela RPC `update_employee_with_salary_adjustment` com `numeric::text`:
   "Ajuste de salário: R$ 2800 → R$ 2900" (sem milhar nem centavos), diferente do formato da tela até 28/10
   ("R$ 2.800,00 → R$ 2.900,00", o da linha de 13/10 do Edson no cap07). Quem trocar o salário hoje vê o texto cru.
3. A 1280 px com o menu lateral aberto, as abas da página Funcionários (RH) não cabem (Dashboard fica fora) e a ficha corta o nome.
