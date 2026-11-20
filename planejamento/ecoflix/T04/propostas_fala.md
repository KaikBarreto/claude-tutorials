# T04 · Propostas para a fala e achados do app (do robô e do ensaio)

Rascunho do agente do robô (11/11/2026). Não edita `roteiro.md` nem `tts_textos.py`: a revisão geral aplica.
Linhas numeradas como no `capNN.json` (L1 = 1ª linha da tabela do capítulo).

## Propostas de fala
| Cap. | Linha | Texto atual | Texto novo | Motivo |
|---|---|---|---|---|
| 02 | L2 | "O único campo obrigatório é o Nome." | "O único campo obrigatório é o Nome. Eu escrevo Rogério Alves Costa." | 19 letras levam ~3 s com o robô (~0,16 s por letra nos ensaios de 11/11, máquina cheia) e a linha tem 2,7 s; hoje o nome é **colado** na palavra "Nome" |
| 02 | L3 | "...chama ele: Rogério Eletricista. O apelido..." | (igual) ou respiro de ~1,5 s depois de "Eletricista." (`pausas.py`) | apelido também colado: digitado, invadiria a linha 4 |
| 03 | L2 | "Em Dados Fiscais, Pessoa Jurídica, e eu digito o CNPJ." | "Em Dados Fiscais, Pessoa Jurídica, e eu preencho o CNPJ." ou respiro de ~2 s depois de "CNPJ." | os 14 dígitos digitados levam ~2,3 s depois de dois cliques de ~1,5 a 3 s (aba e Pessoa Jurídica): hoje o CNPJ é colado em "CNPJ." |
| 04 | L5 | "...é o contador. Eu preencho o que ele passou." | "...é o contador. Eu preencho o que ele passou: contribuinte de ICMS, com a inscrição estadual." | escolher o indicador e digitar 12 dígitos leva ~5 s; a frase dá 2,6 s depois de "Eu": hoje o indicador sai em "Quem define" e a inscrição é colada em "Eu" |
| 09 | L9 | "...Em Observação, eu anoto o motivo." | (igual) ou respiro de ~2 s depois de "motivo." | "Acerto parcial da entrega de 06/11" (34 letras) digitado levaria ~5 s: hoje é colado em "anoto" |
| 03 | L4 e L7 | L4 "Pronto. Vieram a razão social e o nome fantasia." / L7 "A tela pede pra conferir antes de salvar. E repara que um campo ficou vermelho." | L4 "Pronto. A tela pede pra conferir antes de salvar. Vieram a razão social e o nome fantasia." / L7 "E repara que um campo ficou vermelho." | o pedido é o toast "Dados preenchidos — confira antes de salvar", que sai com a lupa (~23 s) e some ~4 s depois; na L7 (~41 s) ele já sumiu |

As linhas 02 L2/L3, 03 L2, 04 L5 e 09 L9 vêm de medidas feitas entre 13:30 e 17:35, com renders 3D ao lado (gestos 1,5 a 2x mais
lentos, aviso do coordenador): com a máquina normal a digitação pode caber; o robô cola esses textos de qualquer jeito, e a proposta
fica para a revisão decidir com a voz real.

## Achados do app (1.60.18, ensaio de 20/11)
- **Corrigidos desde o 1.59.154 (tirar da lista do MELHORIAS):** CEP já vem com máscara (12062-150) depois da consulta e quando digitado;
  "Rascunho encontrado" não aparece mais depois de salvar; a lupa do CNPJ ganhou dica visível (a fala não a cita); as 7 abas da ficha
  cabem em 1600x900 (faixa 1040/1040 px, última aba termina em x=1370 de 1536), sem rolar.
- **Bug novo:** a mensagem de campo obrigatório de endereço diz "Informe o estado (UF) na aba Endereço", mas a aba chama-se Dados Fiscais
  (Endereço Fiscal) (conferir no código antes de citar).
- **Aviso do React no console** ("Select is changing from controlled to uncontrolled") quando a busca preenche UF e cidade: só console.
- **Link do portal com o endereço local** na ficha: para a gravação final, `APP_ORIGIN` do produto (docs/04).
- **"PDF" do extrato e do relatório de saldos** são HTML escrito numa aba nova (`document.write`), não o `#pdf-frame` do T08: o robô devolve
  o HTML (`html_js`, `rec/t04/t04_pdf.py` grava em `rec/t04/arquivos/`). O extrato detalhado só tem a tabela de materiais depois que o
  app termina de gerar (aguardar "Preço unit.").
- **Crédito/débito, lápis e lixeira do extrato** funcionam como na cobertura; o ajuste de R$ 50,00 e a exclusão devolvem o saldo a R$ 1.350,00.

## Sinal dos saldos (pedido do coordenador, 11/11)
Conferido no código (`utils/balanceFormatting.ts`, `BalancesReportModal.tsx:109-119`) e nas folhas de contato dos caps 01 e 09
(mundo B novo): cliente + verde "a receber" (Aços 4.870,00, Fundição 14.370,00); cliente − vermelho "a pagar" (Serra Fina
−1.500,00); fornecedor + vermelho "a pagar" (Cooperativa 2.550,00 → 1.350,00 depois do Pix); fornecedor − verde "a receber"
(Valdir −300,00, o vale que a Recicla adiantou); duplo na convenção do cliente (Depósito −840,00, vermelho nas duas abas). A fala dos
caps 05, 09 e 12 bate com a tela: nada a propor. O cap12 confere as seis cores no relatório (`confere as cores dos 6 saldos`).

## Mundo (para a junção)
- **Cida Ramos** (fornecedora PF, mesmo telefone da Aparecida, sem documento nem endereço) não está no mundo base B: entra pela semente
  `seeds-extra/t04/inicio` (código 6). Sem ela não há selo "Mesmo telefone" no cap01.
- **Link do portal:** nenhum parceiro de B tem `portal_token`; a ficha mostraria "Portal ainda não configurado para este cadastro."
  no cap07. A `t04/inicio` grava um token fictício em todos (o app gera um ao criar com o módulo de portal).
- **Financeiro da cooperativa (cap11):** a conta paga "Frete das entregas de outubro" (R$ 450,00, categoria Frete, venc. 31/10) e a
  entrada no caixa #64 "Venda de sacos de ráfia usados" (R$ 120,00, Outras Receitas, 15/10) estão na `t04/inicio` (B não as tem).
- **Gatilhos novos** (`rec/mundo/hooks/suppliers.mjs` e `customers.mjs`): código sequencial do parceiro criado na tela (Rogério 7,
  serralheria 8, a serralheria cliente 5) e o espelho do cadastro duplo (tabela de preços padrão, nome, documento, contato, endereço),
  como o banco faz. Valem para todas as aulas depois de `rec/run.sh fake`.
