# Voz nova · T3 v2 (Dominex 1.38.9)

Orçamento do Kaik: ~1,9 mil créditos. Padrão da trilha: fluxo único `Domiflix · Vozes de todas as aulas`, voz Fernanda
(`KHmfNHtEjHhLK9eER20w`), `eleven_v4`, `language_code` "pt", **uma versão por fala** (`generations_count: 1`), sem repetir geração
para "tentar de novo". Crédito = caractere enviado (conferido no T4: 8.327 créditos = 7.953 de `CAPS` + 257 de `TITULOS` + 117 dos
separadores ` [pause] `).

## Resposta curta

- **Não passa do orçamento: 1.829 créditos** (96% de 1,9 mil), sobram **71**. A folga paga uma regeração curta, não duas.
- **Nenhum capítulo é regerado inteiro.** Só dois capítulos são novos (cap06 Etiquetas e cap07 Campos personalizados). O resto
  reaproveita o áudio do T3, com 8 frases trocadas no lugar e 4 frases inseridas ou anexadas. Regerar inteiros os 7 capítulos que
  mudam custaria 5.515 caracteres; assim custam 792 (mais os 1.037 dos dois novos).
- Se quiser mais folga: cortes na seção "Cortes" (de 63 a 281 créditos), sem perder nenhum recurso novo da 1.38.9.

## Mapa dos capítulos (v2 ← T3) e o que acontece com o áudio

| v2 | Título | T3 | O que fazer com a voz |
| --- | --- | --- | --- |
| cap00 | Abertura | cap00 | Reaproveita (áudio e legendas do T3). |
| cap01 | A tela de Clientes | cap01 | 2 trocas no lugar (selo PJ; "Configurações"). |
| cap02 | Cliente empresa pelo CNPJ | cap02 | Reaproveita (já é a emenda do T3). |
| cap03 | Cliente pessoa física pelo CEP | cap03 | Reaproveita (já é a emenda do T3). |
| cap04 | Origens | cap04 | 1 troca no lugar ("Configurações"). |
| cap05 | A ficha do cliente | cap05 | 1 troca no lugar (menu "Ações"). |
| cap06 | Etiquetas | novo | **Nó novo** (505 caracteres). |
| cap07 | Campos personalizados | novo | **Nó novo** (491 caracteres). |
| cap08 | Formulário de captação | cap06 | Reaproveita (já é a emenda do T3). |
| cap09 | Fornecedores | cap07 | 1 frase nova no buraco que a emenda do T3 deixou em silêncio. |
| cap10 | Preparando os equipamentos | cap08 | 3 trocas no lugar + 1 frase anexada no fim. |
| cap11 | Cadastrando um equipamento | cap09 | 2 frases inseridas. |
| cap12 | QR Code e etiqueta | cap10 | Reaproveita (já é a emenda do T3). |
| cap13 | Recapitulando | cap11 | 1 frase inserida. |

Títulos das vinhetas: os 11 do T3 reaproveitam `titulos/capNN.wav` (renumerados: 06→08, 07→09, 08→10, 09→11, 10→12, 11→13); só
"Etiquetas." e "Campos personalizados." são novos.

## Os 4 nós a criar no fluxo único (1 versão por fala)

| Nó (rótulo) | Conteúdo | Caracteres |
| --- | --- | --- |
| `T03v2 cap06 Etiquetas` | `CAPS[6]` de `narracao/tts_textos.py`, com as quebras de linha | 505 |
| `T03v2 cap07 Campos personalizados` | `CAPS[7]` | 491 |
| `T03v2 emendas` | as 12 frases abaixo, separadas por ` [pause] ` (11 separadores = 99) | 792 |
| `T03v2 títulos` | `Etiquetas. [pause] Campos personalizados.` | 41 |
| **Total** | | **1.829** |

Texto exato do nó `T03v2 emendas` (a ordem importa: 8 trocas no lugar, depois as 4 inserções, na ordem das tabelas abaixo):

```
E esse selo diz se é pessoa jurídica ou pessoa física. [pause] Configurações, Formulários de captação e Novo Cliente. [pause] Essa lista você monta do seu jeito, aqui em Configurações. [pause] Em cima ficam o nome, a razão social e o menu Ações, com Editar e Excluir. [pause] Lá em cima, em Etiquetas, escolho a Preferencial. [pause] Agora as categorias. [pause] Em Categorias, a gente separa os tipos de aparelho. [pause] Vou criar Multi Split, escolho uma cor e clico no mais. [pause] Por último, as Etiquetas dos equipamentos: crio Em garantia, escolho uma cor e Salvar etiqueta. [pause] As etiquetas do cliente aparecem aqui, na hora de escolher. [pause] Logo abaixo, em Etiquetas, escolho Em garantia. [pause] Marcou os clientes com etiquetas coloridas e criou o campo Horário de acesso.
```

## Trocas no lugar (8 frases, 415 caracteres)

Janelas tiradas do `capNN.json` gravado do T3 (frases do `capNN.json`; `emendar.py` começa a frase nova onde a antiga começava, deixa
o resto da janela em silêncio e, se a frase nova for mais longa, comprime com `atempo` no máximo 8% para terminar 0,2 s antes da
próxima fala). Duração estimada pela regressão das 177 frases gravadas do T3 (0,0606 s por caractere + 0,286 s por frase, erro médio
de 0,3 s). "Disponível" = do início da janela até 0,2 s antes da próxima fala.

| # | Cap. v2 (T3) | De, até (s) | Frase antiga | Frase nova | Car. | Estimada | Disponível | Folga |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | cap01 (cap01) | 26,93 a 30,61 | E essa etiqueta diz se é pessoa jurídica ou pessoa física. | E esse selo diz se é pessoa jurídica ou pessoa física. | 54 | 3,56 s | 3,67 s | +0,11 s |
| 2 | cap01 (cap01) | 42,85 a 47,08 | Configurar origens, Formulários de captação e Novo Cliente. | Configurações, Formulários de captação e Novo Cliente. | 54 | 3,56 s | 4,06 s | +0,50 s |
| 3 | cap04 (cap04) | 1,32 a 5,56 | Essa lista você monta do seu jeito, aqui em Configurar origens. | Essa lista você monta do seu jeito, aqui em Configurações. | 58 | 3,80 s | 4,47 s | +0,67 s |
| 4 | cap05 (cap05) | 6,20 a 11,16 | Em cima ficam o nome, a razão social e os botões pra editar e excluir. | Em cima ficam o nome, a razão social e o menu Ações, com Editar e Excluir. | 74 | 4,77 s | 4,95 s | +0,18 s |
| 5 | cap09 (cap07) | 26,02 a 30,02 | (silêncio: a frase "Aqui o sistema não busca o CNPJ, então você digita tudo." já saiu no T3) | Lá em cima, em Etiquetas, escolho a Preferencial. | 49 | 3,26 s | 4,07 s | +0,81 s |
| 6 | cap10 (cap08) | 46,64 a 48,32 | Terminou, é só fechar. | Agora as categorias. | 20 | 1,50 s | 1,72 s | +0,22 s |
| 7 | cap10 (cap08) | 48,56 a 52,40 | Do lado tem a aba Categorias, que separa os tipos de aparelho. | Em Categorias, a gente separa os tipos de aparelho. | 51 | 3,38 s | 3,83 s | +0,45 s |
| 8 | cap10 (cap08) | 55,76 a 59,44 | Vou criar Multi Split, escolho uma cor, e criar. | Vou criar Multi Split, escolho uma cor e clico no mais. | 55 | 3,62 s | 3,59 s | -0,03 s (comprime ~1%) |

Notas das trocas:

- #1 e #4 são as folgas mais justas (0,11 s e 0,18 s). Se o `emendar.py` avisar `ATENÇÃO` ou `CORTADA`, a frase deve ser gerada de novo
  mais curta, não esticada. Alternativa pronta para a #4, 8 caracteres a menos: "Em cima ficam o nome, a razão social e o menu Ações, com Editar e Excluir." → "Em cima ficam o nome, a razão social e o menu Ações." (51, perde o "com Editar e Excluir", que a tela mostra ao passar o mouse).
- #6 e #7 ficam coladas (0,24 s entre as janelas): o `emendar.py` já considera o início da frase nova seguinte como "próxima fala".
- #5: a base é o áudio já emendado do T3 (`emendas/cap07_v2.wav`), em que a janela 26,02 a 30,02 está em silêncio; a frase nova entra
  nele. O robô tem ~4 s para rolar até o topo e marcar a etiqueta (o buraco do T3 já era o tempo de digitar o endereço).
- #8: o botão "Criar" da categoria de equipamento não existe mais na 1.38.9; o bloco de adicionar tem campo de nome, cor e o botão "+"
  (`src/components/customers/EquipmentCategoryManagerDialog.tsx:87-107`). A fala "e criar" apontava para um rótulo que sumiu.
  Sem esta troca a fala continua entendível ("criar" como verbo); custa 55 + 9 de separador = 64 créditos (ver "Cortes").
- Efeito colateral aceito: a #1 troca "etiqueta" por "selo" no cap01 para não confundir o selo PJ/PF com as Etiquetas coloridas que
  entram no cap06.

## Inserções (4 frases, 278 caracteres)

O `emendar.py` só troca no lugar (mantém a duração do capítulo); inserir muda a duração. Como esses capítulos são regravados em vídeo de
qualquer jeito, a duração nova é aceitável: o robô grava em cima do áudio já recomposto.

| # | Cap. v2 (T3) | Onde (s do `capNN.json` do T3) | Frase | Car. | Estimada | Duração nova do capítulo |
| --- | --- | --- | --- | --- | --- | --- |
| A | cap10 (cap08) | no fim: depois de 59,52 s, com 0,25 s de silêncio antes | Por último, as Etiquetas dos equipamentos: crio Em garantia, escolho uma cor e Salvar etiqueta. | 95 | 6,49 s | 59,52 + 0,25 + 6,5 = ~66,3 s |
| B | cap11 (cap09) | corte em 6,52 s (a L1 "Colégio Monte Verde." termina em 6,36 e a L2 começa em 6,68) | As etiquetas do cliente aparecem aqui, na hora de escolher. | 59 | 3,86 s | |
| C | cap11 (cap09) | corte em 18,50 s (a L2 termina em 18,36 com "Split Hi-Wall." e a L3 "Marca, modelo..." começa em 18,64) | Logo abaixo, em Etiquetas, escolho Em garantia. | 47 | 3,13 s | 63,52 + 4,10 + 3,37 = ~71,0 s |
| D | cap13 (cap11) | corte em 11,98 s (a frase 3 termina em 11,84 com "...com WhatsApp." e a frase 4 "Criou um formulário..." começa em 12,12) | Marcou os clientes com etiquetas coloridas e criou o campo Horário de acesso. | 77 | 4,95 s | 39,20 + 5,19 = ~44,4 s |

Como inserir (validado em um take real do T3, 63,52 s → 70,94 s com dois clipes de teste): estender o `emendar.py` com um passo depois
do laço das trocas, usando os mesmos `clips` (alinhamento por palavra, bordas pelo VAD, volume casado por LUFS):

```python
def inserir(y, pontos, folga=0.12):
    """pontos: [(segundo_do_corte, clipe)] em ordem crescente, tempos do take original. Cola cada clipe no corte,
    com `folga` s de silêncio de cada lado; o resto do áudio é empurrado para a frente."""
    gap = np.zeros(int(folga * SR), dtype=y.dtype)
    partes, ult = [], 0
    for t, clip in pontos:
        i = int(round(t * SR))
        partes += [y[ult:i], gap, clip, gap]
        ult = i
    partes.append(y[ult:])
    return np.concatenate(partes)
```

No cap10 o ponto é o fim do áudio (`len(y) / SR`) com `folga=0.25`; no cap11, `[(6.52, clipe_B), (18.50, clipe_C)]` com `folga=0.12`
(0,16 s do silêncio original + 0,12 s dá ~0,28 s, perto dos 0,24 s naturais entre linhas); no cap13, `[(11.98, clipe_D)]`. Depois:
`python3 -I proc.py 10=emendas/cap10_v3.wav 11=emendas/cap11_v2.wav 13=emendas/cap13_v2.wav` refaz palavras, linhas e legendas.

## `trocas.json` pronto (formato do `emendar.py`)

A chave `insercoes` é nova (o `emendar.py` atual a ignora); `no_elevenlabs` entra depois da geração.

```json
{"motivo": "T3 v2 (Dominex 1.38.9): menu Ações, modal Configurações, etiquetas e campos personalizados (Kaik, 31/10).",
 "no_elevenlabs": {"node": "<id do nó T03v2 emendas>", "sessions": ["<sessão>"]},
 "trocas": [
  {"cap": 1, "velho": "E essa etiqueta diz se é pessoa jurídica ou pessoa física.", "novo": "E esse selo diz se é pessoa jurídica ou pessoa física.", "de": 26.93, "ate": 30.61},
  {"cap": 1, "velho": "Configurar origens, Formulários de captação e Novo Cliente.", "novo": "Configurações, Formulários de captação e Novo Cliente.", "de": 42.85, "ate": 47.08},
  {"cap": 4, "velho": "Essa lista você monta do seu jeito, aqui em Configurar origens.", "novo": "Essa lista você monta do seu jeito, aqui em Configurações.", "de": 1.32, "ate": 5.56},
  {"cap": 5, "velho": "Em cima ficam o nome, a razão social e os botões pra editar e excluir.", "novo": "Em cima ficam o nome, a razão social e o menu Ações, com Editar e Excluir.", "de": 6.20, "ate": 11.16},
  {"cap": 9, "velho": "", "novo": "Lá em cima, em Etiquetas, escolho a Preferencial.", "de": 26.02, "ate": 30.02},
  {"cap": 10, "velho": "Terminou, é só fechar.", "novo": "Agora as categorias.", "de": 46.64, "ate": 48.32},
  {"cap": 10, "velho": "Do lado tem a aba Categorias, que separa os tipos de aparelho.", "novo": "Em Categorias, a gente separa os tipos de aparelho.", "de": 48.56, "ate": 52.40},
  {"cap": 10, "velho": "Vou criar Multi Split, escolho uma cor, e criar.", "novo": "Vou criar Multi Split, escolho uma cor e clico no mais.", "de": 55.76, "ate": 59.44}
 ],
 "insercoes": [
  {"cap": 10, "em": "fim", "folga": 0.25, "novo": "Por último, as Etiquetas dos equipamentos: crio Em garantia, escolho uma cor e Salvar etiqueta."},
  {"cap": 11, "em": 6.52, "novo": "As etiquetas do cliente aparecem aqui, na hora de escolher."},
  {"cap": 11, "em": 18.50, "novo": "Logo abaixo, em Etiquetas, escolho Em garantia."},
  {"cap": 13, "em": 11.98, "novo": "Marcou os clientes com etiquetas coloridas e criou o campo Horário de acesso."}
 ]}
```

## Operação, na ordem

1. Copiar `t3/narracao/` para `t3v2/narracao/` renumerando: `cap06`→`cap08`, `cap07`→`cap09`, `cap08`→`cap10`, `cap09`→`cap11`, `cap10`→`cap12`,
   `cap11`→`cap13` (arquivos `capNN.json`, `titulos/capNN.wav`, e o campo `cap` dentro do JSON); ajustar `pasta` e `arquivo` se a pasta mudar de lugar.
   `config_narracao.json` e `tts_textos.py` desta pasta substituem os do T3.
2. Os capítulos 9 e 10 já são emendas do T3 (take dentro de `emendas/`): o `emendar.py` exige o `capNN.v1.json`. Criar `cap09.v1.json` e
   `cap10.v1.json` como cópias do JSON atual. Assim o "take original" do v2 é a emenda do T3, e o `trocas.json` do v2 lista só as trocas novas
   (a troca herdada do cap10, "Repara que cada mudança já grava sozinha.", já está dentro desse áudio e não se paga de novo).
3. Gerar os 4 nós no fluxo único, `generations_count: 1`; o Kaik exporta o zip; `proc.py` nos capítulos 6 e 7; `titulos.py` só com os dois
   títulos novos (`titulos/cap06.wav`, `titulos/cap07.wav`).
4. `emendar.py` com o MP3 do nó `T03v2 emendas`: gera `emendas/cap{01,04,05,09,10}_v2.wav`. Depois o passo de inserção (cap10 vira `cap10_v3.wav`; cap11 e cap13
   saem de `emendas/cap11_v2.wav` e `emendas/cap13_v2.wav`, a partir dos takes originais do T3).
5. `python3 -I proc.py 01=emendas/cap01_v2.wav 04=emendas/cap04_v2.wav 05=emendas/cap05_v2.wav 09=emendas/cap09_v2.wav 10=emendas/cap10_v3.wav 11=emendas/cap11_v2.wav 13=emendas/cap13_v2.wav`
   (guardar antes os `capNN.json` como `capNN.v1.json`). Conferir pelo ASR a folga de cada troca (`próxima palavra − fim da fala nova` ≥ 0,2 s).
6. O `asr_fix` do `config_narracao.json` herda a correção do T3 ("1800" → "18000") para o take `cap11_v2`; confirmar o id do take no log do `proc.py`.

## O que regravar em vídeo (zero crédito de voz)

- **Obrigatório (a tela mudou ou há fala nova):** cap01, cap04, cap05, cap06, cap07, cap09, cap10, cap11, cap13.
- **Recomendado (mesmo áudio, mas a 1.38.9 aparece de fundo ou na ficha):** cap02 e cap03 (a janela "Novo Cliente" ganhou "Etiquetas"), cap08
  (botões do topo atrás da janela), cap12 (ficha do equipamento com "Ações" e selo "Em garantia").
- **Pode ficar como está:** cap00 (só o menu; conferir se o menu lateral da 1.38.9 é o mesmo).

## Duração (limite do pedido: +2 min)

| Parcela | Segundos |
| --- | --- |
| cap06 Etiquetas (35 s de fala estimada + 0,9 s de pausas entre linhas) | 35,8 |
| cap07 Campos personalizados (34 s + 0,9 s) | 34,9 |
| cap10: frase anexada | 6,9 |
| cap11: duas frases inseridas | 7,5 |
| cap13: uma frase inserida | 5,2 |
| Duas vinhetas novas (~4 s cada; no T3 as 11 vinhetas, a abertura e a cartela somam ~51 s sobre 682 s de áudio) | ~8 |
| Folga de robô nos capítulos novos e alterados (cliques que não cabem dentro da fala viram trecho acelerado) | ~8 |
| **Soma** | **~106 s = +1:46** |

T3: 12:13 (733 s). v2: ~14:00. Faixa provável +1:35 a +1:55; ultrapassa +2:00 se o robô dos capítulos 6 e 7 precisar de mais de
~12 s além da fala. Se isso acontecer, tirar primeiro as frases dos cortes 2 e 3 abaixo (cada uma poupa ~4 a 5 s).

## Cortes (para ganhar folga de créditos ou de tempo)

Cada corte vale para o texto de `tts_textos.py` e para a linha da tabela do `roteiro.md`; o valor inclui o separador ` [pause] `.

| Corte | O que sai | Créditos | Segundos | Perde |
| --- | --- | --- | --- | --- |
| 1 | Troca #1 (selo PJ): o cap01 fica com "etiqueta" | 63 | 0 | O esclarecimento "selo" x "etiqueta colorida" |
| 2 | Inserção D (recap fala das etiquetas e do campo) | 86 | 5,2 | O recap não cita as novidades |
| 3 | Inserção B (cap11, etiquetas do cliente na escolha) | 68 | 4,1 | A etiqueta aparece na tela sem fala |
| 4 | Troca #8 ("clico no mais" volta a "e criar") | 64 | 0 | A exatidão do rótulo do botão "+" |
| 5 | Linha dos fornecedores do cap07 ("Os fornecedores têm os campos deles...") | 62 | 4,6 | A menção aos campos de fornecedores |

Cortes 1 + 2 + 3 = 217 créditos (núcleo 1.612, folga 288). Cortes 1 a 4 = 281 (núcleo 1.548, folga 352). A recomendação é **não cortar nada**
e deixar a folga de 71 para uma regeração curta; se o "pê-móqui" sair errado, a linha do cap06 que o contém (134 caracteres) cabe
só se sair o corte 1 ou o corte 2.

## Extras que NÃO estão nos 1.829 (se o Kaik quiser, com o custo)

| Extra | Onde | Caracteres + separador |
| --- | --- | --- |
| "O menu Ações guarda o Editar e o Excluir, e a etiqueta fica embaixo do nome." | cap12, depois da primeira linha (inserção) | 75 + 9 |
| "Se você ligar Mostrar nos portais, o cliente também vê essa etiqueta no portal dele." | cap06, depois de "Salvar etiqueta" (inserção) | 83 + 9 |
| "A coluna Portal libera cada campo pra aparecer no portal do cliente." | cap10, depois de "Marco como obrigatório" (inserção) | 66 + 9 |
| "E aqui também dá pra marcar etiquetas, que a gente vê já já." | cap02, depois de "Origem" (inserção; exige recompor o cap02) | 58 + 9 |
| "Na lista de equipamentos, o Filtros também separa por etiqueta." | cap10 ou cap11 (inserção) | 63 + 9 |

Somados: ~450 créditos, fora do orçamento. Entram só com os cortes 1 a 4 mais mais ~170 de folga do Kaik.

## Pronúncia e testes

- **PMOC** → "pê-móqui" (convenção da trilha, como em T11, T13 e T19); está na `trocas` do `config_narracao.json`. Aparece 2 vezes no cap06
  ("tem contrato de pê-móqui", "escrevo Contrato pê-móqui"). Plano B se sair "pêmóqui" estranho ou soletrado: "pê ême ó cê"
  (uma troca de linha no `tts_textos.py` e no config).
- **Sim/Não** → "Sim ou Não" na fala; o `config_narracao.json` devolve "Sim/Não" na legenda (`numeros`, três palavras faladas viram uma).
- Nomes novos sem pronúncia especial: Preferencial, Horário de acesso, Em garantia, Ações, Configurações.
- Ouvir de ouvido na primeira geração: "Configurações" (4 ocorrências nas emendas e no cap06), "Ações" (5), "pê-móqui" (2).

## Se o botão "Configurar Campos" for renomeado para "Configurações"

O botão da página Equipamentos ainda se chama "Configurar Campos" (`src/lib/i18n/messages/app/equipment.ts:21`) e abre a janela "Configurações
de equipamentos" (`src/components/customers/EquipmentSettingsDialog.tsx:29`). Se o app renomear o botão (candidato a handoff), a frase do cap10
`15,88 a 18,68` ("Em Configurar Campos estão os que já vêm prontos:", linha 1 do cap10) vira **"Em Configurações estão os que já vêm prontos:"**
(46 caracteres + 9 de separador = 55 créditos; cabe: 2,8 s de fala em 2,8 s de janela, comprime ~2%).

## Falas do T3 que saem do vídeo

Ficam de fora (276 caracteres de áudio antigo): as 8 frases da coluna "Frase antiga" acima, menos o buraco do cap09 (sem texto). Todo o resto
do áudio do T3 entra no v2 sem alteração.
