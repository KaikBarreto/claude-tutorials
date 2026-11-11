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

## Mundo (para a junção)
- **Cida Ramos** (fornecedora PF, mesmo telefone da Aparecida, sem documento nem endereço) não está no mundo base B: entra pela semente
  `seeds-extra/t04/inicio` (código 6). Sem ela não há selo "Mesmo telefone" no cap01.
- **Link do portal:** nenhum parceiro de B tem `portal_token`; a ficha mostraria "Portal ainda não configurado para este cadastro."
  no cap07. A `t04/inicio` grava um token fictício em todos (o app gera um ao criar com o módulo de portal).
