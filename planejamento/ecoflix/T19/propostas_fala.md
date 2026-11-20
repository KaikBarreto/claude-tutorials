# Propostas de fala · T19 · Funcionários e ponto eletrônico

Atualizado em 20/11/2026 (EcoSistema 1.60.18, voz ainda estimada). As propostas de 11/11 foram aplicadas na revisão de 20/11 (linha da
selfie no cap. 12, que antes era o 9). Linha = número da linha do capítulo (1 = primeira linha da tabela Tela × Fala). Gerador:
`$TUT_HOME/rec/t19/gerar.py` (lê a voz de `t19/narracao/capNN.json`).

| Cap. | Linha | O que pedir à voz | Motivo |
|---|---|---|---|
| 11 | 2 | respiro de 4,5 s antes de "Se ele esquecer" (`pausas.py 11 <T>:4.5`; o gerador avisa o T com a voz de verdade) | o robô grava o PIN (Atualizar) e reabre o cadastro para mostrar "Trocar PIN" e "Remover PIN" |
| 6 | 7, 8 | conferir que "dois mil setecentos e cinquenta" e "dois mil e novecentos" batem com a tela (o ensaio confere) | valor na fala só depois de visto na tela |
| 7 | 5 | conferir "dois mil quinhentos e oitenta", INSS, zero de IRRF, VT e "dois mil cento e sessenta e oito reais e onze centavos" | idem; o INSS vem da tabela do app |
| 12 | 7, 8 | a hora do ponto avança (almoço 11:00, saída 16:00) no falso: a fala não diz horário | evitar número que só existe no falso |

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

1. "Saldo: R$ 1500.00" com ponto no "Registrar Vale" (handoff 4 do plano, `EmployeeMovementModal.tsx:413,428`): aparece no cap05 (corrigido no 1.60.18 com máscara de moeda).
2. Na 1.59.154 o ajuste de salário é gravado pela RPC `update_employee_with_salary_adjustment` com `numeric::text`:
   "Ajuste de salário: R$ 2800 → R$ 2900" (sem milhar nem centavos), diferente do formato da tela até 28/10
   ("R$ 2.800,00 → R$ 2.900,00", o da linha de 13/10 do Edson no cap07). Quem trocar o salário hoje vê o texto cru.
3. A 1280 px com o menu lateral aberto, as abas da página Funcionários (RH) não cabem (Dashboard fica fora) e a ficha corta o nome.
