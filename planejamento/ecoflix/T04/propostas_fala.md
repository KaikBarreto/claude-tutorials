# T04 · Propostas para a fala e achados do app (do robô e do ensaio)

Rascunho do agente do robô (11/11/2026). Não edita `roteiro.md` nem `tts_textos.py`: a revisão geral aplica.
Linhas numeradas como no `capNN.json` (L1 = 1ª linha da tabela do capítulo).

## Propostas de fala
| Cap. | Linha | Texto atual | Texto novo | Motivo |
|---|---|---|---|---|
| (preencher no ensaio) | | | | |

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
