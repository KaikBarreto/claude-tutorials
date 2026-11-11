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

## Achados do app (1.59.154)
- **Lupa do CNPJ (cap03 L3):** a dica "Buscar dados da empresa pelo CNPJ" é o `title` nativo do botão
  (`components/CnpjLookupInput.tsx:146-150`): não aparece no vídeo. O robô passa o mouse e lê o texto (`eval` "texto da dica (title)
  da lupa"); a edição põe um aviso "Ao passar o mouse: Buscar dados da empresa pelo CNPJ" (docs/08, T9 cap13). A fala fica.

- **As 7 abas da ficha não cabem em 1280 px** (o [TESTAR] do cap07), mesmo com o menu recolhido: a faixa "Seções da ficha"
  (`ClientsListView.tsx:315`, `overflow-x-auto`) corta "Notas fiscais" e deixa "Preços" fora (x ≈ 1276 numa janela de 1280). O robô
  rola a faixa de lado (suave, ~0,5 s) antes de "Notas fiscais"/"Preços" nos caps 06, 07 e 11; a fala não muda.

- **CEP sem máscara depois da busca do CNPJ (cap03 L5):** o campo mostra "12062150", não "12062-150": `handleCnpjData` grava o CEP
  só com dígitos e o `CepLookup` só formata quando a pessoa digita (`EntityFormDialog.tsx:728-731`, `CepLookup.tsx:138-150`). A fala
  não diz o número; a tela fica como o app mostra.
- **Aviso do React no console** quando a busca preenche UF e cidade ("Select is changing from uncontrolled to controlled", Selects do
  Radix que nasceram sem valor): só console. Entrou no `ruidoConsole` do `mundo.json` para não contar como problema da gravação.

## Mundo (para a junção)
- **Cida Ramos** (fornecedora PF, mesmo telefone da Aparecida, sem documento nem endereço) não está no mundo base B: entra pela semente
  `seeds-extra/t04/inicio` (código 6). Sem ela não há selo "Mesmo telefone" no cap01.
- **Link do portal:** nenhum parceiro de B tem `portal_token`; a ficha mostraria "Portal ainda não configurado para este cadastro."
  no cap07. A `t04/inicio` grava um token fictício em todos (o app gera um ao criar com o módulo de portal).
