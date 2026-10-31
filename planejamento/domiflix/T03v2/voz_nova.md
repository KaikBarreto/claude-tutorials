# Voz nova · T3 v2 (Dominex 1.38.9)

Orçamento do Kaik: ~1,9 mil créditos. Regras da trilha: fluxo único `Domiflix · Vozes de todas as aulas`, voz Fernanda
(`KHmfNHtEjHhLK9eER20w`), `eleven_v4`, `language_code` "pt", **uma versão por fala** (`generations_count: 1`), nunca gerar de novo para
"tentar outra". Crédito = caractere enviado, quebras de linha e separadores incluídos (conferido no T4: 8.327 créditos = 7.953 de `CAPS` + 257 de
`TITULOS` + 117 de separadores ` [pause] `, 13 x 9).

## Resposta curta

- **Não passa do orçamento: 1.824 créditos** (96% de 1,9 mil); sobram **76**. A folga paga um teste curto de pronúncia (18) ou uma frase trocada (até 76), não um capítulo.
- **Nenhum capítulo existente é regerado inteiro.** Voz nova em dois capítulos novos (cap06 Etiquetas, cap07 Campos personalizados), em 8 frases trocadas no lugar
  e em 4 frases inseridas ou anexadas; o resto reaproveita o áudio do T3 sem mexer. Regerar inteiros os 7 capítulos que mudam custaria 5.515 caracteres
  (cap01 704, cap04 395, cap05 1.182, cap09 596, cap10 925, cap11 1.017, cap13 696); do jeito proposto, as emendas custam 783.
- Mais folga, se o Kaik quiser: cortes de 63 a 86 créditos cada, sem perder nenhum recurso novo (seção "Cortes").

## Mapa dos capítulos (v2 ← T3) e o que acontece com o áudio

| v2 | Título da vinheta | T3 | O que fazer com a voz |
| --- | --- | --- | --- |
| cap00 | Abertura | cap00 | Reaproveita (áudio e legendas do T3). |
| cap01 | A tela de Clientes | cap01 | 2 trocas no lugar (selo PJ; "Configurações"). |
| cap02 | Cliente empresa pelo CNPJ | cap02 | Reaproveita (já é uma emenda do T3). |
| cap03 | Cliente pessoa física pelo CEP | cap03 | Reaproveita (já é uma emenda do T3). |
| cap04 | Origens | cap04 | 1 troca no lugar ("Configurações"). |
| cap05 | A ficha do cliente | cap05 | 1 troca no lugar (menu "Ações"). |
| cap06 | Etiquetas | novo | **Nó novo** (509 caracteres). |
| cap07 | Campos personalizados | novo | **Nó novo** (491 caracteres). |
| cap08 | Formulário de captação | cap06 | Reaproveita (já é uma emenda do T3). |
| cap09 | Fornecedores | cap07 | 1 frase nova no buraco que a emenda do T3 deixou em silêncio. |
| cap10 | Preparando os equipamentos | cap08 | 3 trocas no lugar + 1 frase anexada no fim. |
| cap11 | Cadastrando um equipamento | cap09 | 2 frases inseridas. |
| cap12 | quê-érre côde e etiqueta | cap10 | Reaproveita (já é uma emenda do T3). |
| cap13 | Recapitulando | cap11 | 1 frase inserida. |

Vinhetas: as 11 do T3 reaproveitam `titulos/capNN.wav` (renumeradas: 06→08, 07→09, 08→10, 09→11, 10→12, 11→13); só "Etiquetas." e "Campos personalizados." são novos.

## Os 5 nós a criar no fluxo único (1 versão por fala)

| Nó (rótulo) | Conteúdo | Caracteres |
| --- | --- | --- |
| `T03v2 cap06 Etiquetas` | `CAPS[6]` de `narracao/tts_textos.py`, com as quebras de linha | 509 |
| `T03v2 cap07 Campos personalizados` | `CAPS[7]` | 491 |
| `T03v2 emendas` | as 8 frases de troca no lugar, separadas por ` [pause] ` (7 separadores = 63) | 478 |
| `T03v2 inserções` | as 4 frases de inserção, separadas por ` [pause] ` (3 separadores = 27) | 305 |
| `T03v2 títulos` | `Etiquetas. [pause] Campos personalizados.` | 41 |
| **Total** | | **1.824** |

Por que dois nós de emenda e não um: o `emendar.py` alinha o MP3 com a lista de `trocas`; frases a mais no fim do MP3 seriam coladas à última frase da lista e o trecho dela viria
com o resto do áudio. Dois nós custam 9 créditos a menos (um separador a menos) e cada ferramenta recebe só as frases dela.

Texto exato do nó `T03v2 emendas` (a ordem é a das linhas da tabela "Trocas no lugar"):

```
E esse selo diz se é pessoa jurídica ou pessoa física. [pause] Configurações, Formulários de captação e Novo Cliente. [pause] Essa lista você monta do seu jeito, aqui em Configurações. [pause] Em cima ficam o nome, a razão social e o menu Ações, com Editar e Excluir. [pause] Lá em cima, em Etiquetas, escolho a Preferencial. [pause] Agora as categorias. [pause] Em Categorias, a gente separa os tipos de aparelho. [pause] Vou criar Multi Split, escolho uma cor e clico no mais.
```

Texto exato do nó `T03v2 inserções` (ordem da tabela "Inserções"):

```
Por último, as Etiquetas dos equipamentos: crio Em garantia, escolho uma cor e Salvar etiqueta. [pause] As etiquetas do cliente aparecem aqui, na hora de escolher. [pause] Logo abaixo, em Etiquetas, escolho Em garantia. [pause] Marcou os clientes com etiquetas coloridas e criou o campo Horário de acesso.
```

Opcional, dentro da folga: um **teste de pronúncia** antes de gerar o cap06, nó `T03v2 teste pê-móqui` com `Contrato pê-móqui.` (18 créditos; total 1.842). Se soar errado,
trocar para "pê, ême, ó, cê" no `tts_textos.py` e no `config_narracao.json` antes de gerar o nó (o PERFIL pede teste antes; ver "Pronúncia e testes").

Decisão de texto: o app não traz nenhuma etiqueta pronta (nem `supabase/migrations` nem `src` têm "Preferencial"), então a fala do cap06 diz "Eu já deixei a Preferencial" (a etiqueta entra
por seed no mundo da aula) e não "já tem", que o aluno não encontraria na conta dele.

## Trocas no lugar (8 frases, 415 caracteres)

Janelas tiradas do `capNN.json` gravado do T3 (frases do próprio `capNN.json`). O `emendar.py` começa a frase nova onde a antiga começava, deixa o resto da janela em silêncio e,
se a frase nova for mais longa que a janela, comprime o tempo com `atempo` no máximo 8%, para a fala terminar 0,2 s antes da próxima. Duração estimada por um ajuste linear nas
190 frases gravadas do T3 (0,06 s por caractere + 0,28 s por frase; erro médio de 0,3 s). "Disponível" = do início da janela até 0,2 s antes da próxima fala (ou da frase nova da troca
seguinte); "folga" = disponível menos estimada.

| # | Cap. v2 (T3) | De, até (s) | Frase antiga | Frase nova | Car. | Estimada | Disponível | Folga |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | cap01 (cap01) | 26,93 a 30,61 | E essa etiqueta diz se é pessoa jurídica ou pessoa física. | E esse selo diz se é pessoa jurídica ou pessoa física. | 54 | 3,56 s | 3,67 s | +0,11 s |
| 2 | cap01 (cap01) | 42,85 a 47,08 | Configurar origens, Formulários de captação e Novo Cliente. | Configurações, Formulários de captação e Novo Cliente. | 54 | 3,56 s | 4,06 s | +0,50 s |
| 3 | cap04 (cap04) | 1,32 a 5,56 | Essa lista você monta do seu jeito, aqui em Configurar origens. | Essa lista você monta do seu jeito, aqui em Configurações. | 58 | 3,80 s | 4,47 s | +0,67 s |
| 4 | cap05 (cap05) | 6,20 a 11,16 | Em cima ficam o nome, a razão social e os botões pra editar e excluir. | Em cima ficam o nome, a razão social e o menu Ações, com Editar e Excluir. | 74 | 4,77 s | 4,95 s | +0,18 s |
| 5 | cap09 (cap07) | 26,02 a 30,02 | (silêncio: a emenda do T3 já tirou "Aqui o sistema não busca o CNPJ, então você digita tudo.") | Lá em cima, em Etiquetas, escolho a Preferencial. | 49 | 3,26 s | 4,07 s | +0,81 s |
| 6 | cap10 (cap08) | 46,64 a 48,32 | Terminou, é só fechar. | Agora as categorias. | 20 | 1,50 s | 1,72 s | +0,22 s |
| 7 | cap10 (cap08) | 48,56 a 52,40 | Do lado tem a aba Categorias, que separa os tipos de aparelho. | Em Categorias, a gente separa os tipos de aparelho. | 51 | 3,38 s | 3,83 s | +0,45 s |
| 8 | cap10 (cap08) | 55,76 a 59,44 | Vou criar Multi Split, escolho uma cor, e criar. | Vou criar Multi Split, escolho uma cor e clico no mais. | 55 | 3,62 s | 3,59 s | -0,03 s (comprime ~1%) |

Notas das trocas:

- #1 e #4 têm as folgas mais justas (0,11 s e 0,18 s). A compressão de até 8% (cerca de 0,3 s numa frase de 3,5 s) absorve um erro de estimativa dessa ordem. Se o `emendar.py` imprimir `ATENÇÃO` ou
  `CORTADA`, a frase deve ser gerada de novo mais curta, não esticada. Alternativa pronta para a #4, 22 caracteres mais curta: "Em cima ficam o nome, a razão social e o menu Ações." (52; perde o "com Editar e Excluir",
  que a tela mostra ao abrir o menu).
- #6 e #7 ficam coladas (0,24 s entre as janelas): o `emendar.py` já trata o início da frase nova seguinte como "próxima fala" da #6 (por isso o disponível dela é 1,72 s e não 5,7 s).
- #5: a base é a emenda do T3 (`cap07_v2.wav`, no v2 `cap09_t3`), em que a janela 26,02 a 30,02 está em silêncio; a frase nova entra nela. O robô tem ~4 s para rolar até o topo da janela e marcar a etiqueta.
- #8: o botão "Criar" da categoria de equipamento não existe na 1.38.9; o bloco de adicionar tem o campo "Nome da categoria", o seletor de cor e um botão só com o ícone de mais
  (`src/components/customers/EquipmentCategoryManagerDialog.tsx:87-107`). A fala antiga ("e criar") apontava para um rótulo que sumiu. Sem esta troca a fala ainda se entende; a troca custa 55 + 9 = 64 créditos (corte 4).
- Efeito colateral aceito: a #1 troca "etiqueta" por "selo" no cap01 para o selo PJ/PF não se confundir com as Etiquetas coloridas que entram no cap06.

Caracteres antigos substituídos: 382 (as 7 frases com texto; a #5 cai num silêncio).

## Inserções (4 frases, 278 caracteres)

O `emendar.py` só troca no lugar (mantém a duração do capítulo); inserir muda a duração. Como esses capítulos são regravados em vídeo de qualquer jeito, a duração nova é aceitável:
o robô grava em cima do áudio já recomposto.

| # | Cap. v2 (T3) | Onde (s do `capNN.json` do T3) | Frase | Car. | Estimada | Duração do capítulo |
| --- | --- | --- | --- | --- | --- | --- |
| A | cap10 (cap08) | no fim, depois de 59,52 s, com 0,25 s de silêncio antes | Por último, as Etiquetas dos equipamentos: crio Em garantia, escolho uma cor e Salvar etiqueta. | 95 | 6,49 s | 59,52 para ~66,4 s |
| B | cap11 (cap09) | corte em 6,52 s (a linha "Colégio Monte Verde." termina em 6,36 s e a seguinte começa em 6,68 s) | As etiquetas do cliente aparecem aqui, na hora de escolher. | 59 | 3,86 s | 63,52 para ~71,0 s (B e C) |
| C | cap11 (cap09) | corte em 18,50 s (a linha termina em 18,36 s com "Split Hi-Wall." e a seguinte começa em 18,64 s) | Logo abaixo, em Etiquetas, escolho Em garantia. | 47 | 3,13 s | |
| D | cap13 (cap11) | corte em 11,98 s (a frase termina em 11,84 s com "...com WhatsApp." e a seguinte, "Criou um formulário...", começa em 12,12 s) | Marcou os clientes com etiquetas coloridas e criou o campo Horário de acesso. | 77 | 4,95 s | 39,20 para ~44,4 s |

Como inserir (validado num take real do T3, 63,52 s para 70,94 s com dois clipes de teste, só em cópia de trabalho): estender o `emendar.py` com um passo depois do laço das trocas, usando clipes
cortados do MP3 do nó `T03v2 inserções` do mesmo jeito que ele já faz (alinhamento por palavra, bordas pelo VAD, volume casado por LUFS):

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

No cap10 o ponto é o fim do áudio (`len(y) / SR`) com `folga=0.25`; no cap11, `[(6.52, clipe_B), (18.50, clipe_C)]` com `folga=0.12` (0,16 s do silêncio original + 0,12 s dá ~0,28 s de cada lado, perto dos
0,24 s naturais entre linhas); no cap13, `[(11.98, clipe_D)]`.

## `trocas.json` pronto (formato do `emendar.py`)

A chave `insercoes` é nova (o `emendar.py` atual a ignora); o campo `no_elevenlabs` entra depois da geração, com o id dos dois nós.

```json
{"motivo": "T3 v2 (Dominex 1.38.9): menu Ações, modal Configurações, etiquetas e campos personalizados (Kaik, 31/10).",
 "no_elevenlabs": {"emendas": "<id do nó T03v2 emendas>", "insercoes": "<id do nó T03v2 inserções>", "sessions": ["<sessão>"]},
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

Pasta de trabalho: `$TUT_HOME/t3v2/narracao/`. O T3 em `$TUT_HOME/t3/` é a versão entregue e fica intocado.

**0. Montar a pasta (uma vez)**

- Copiar do T3: `takes/`, `emendas/`, `recebido_1225/`, `recebido_1559/`, `titulos/`, `cap*.json` e `nos_elevenlabs.json` (217 MB no total do T3).
  Copiar de verdade, sem link físico: o `emendar.py` regrava arquivos.
- Ferramentas: usar as **novas** de `ferramentas/narracao/` (`config.py`, `proc.py`, `emendar.py`, `titulos.py`, `legendas.py`, `legendas_aula.py`).
  A cópia que está em `t3/narracao/` é a velha (o `emendar.py` dela não comprime o tempo e não há `config_narracao.json`). Entram também
  o `tts_textos.py` e o `config_narracao.json` desta pasta (`T03v2/narracao/`).
- Caminho do T3 dentro dos JSON: `sed -i 's#/t3/narracao#/t3v2/narracao#g' cap*.json titulos/titulos.json`.
- Renumerar T3 → v2 (6→8, 7→9, 8→10, 9→11, 10→12, 11→13) **e renomear as emendas herdadas do T3**. Motivo: o `emendar.py` grava `emendas/capNN_v2.wav`,
  e `cap10_v2.wav` já existe no T3 (é a emenda do cap. 10 do T3, base do cap12 da v2): sem renomear, a emenda nova do cap10 sobrescreveria a base do cap12.
  Rodar dentro de `t3v2/narracao/` (testado numa cópia só com os JSON, sem áudio):

```python
import json, os
MAPA = {11: 13, 10: 12, 9: 11, 8: 10, 7: 9, 6: 8}   # T3 -> v2, de cima para baixo (nunca sobrescreve)
for velho, novo in MAPA.items():
    d = json.load(open(f"cap{velho:02d}.json"))
    d["cap"] = novo
    if os.path.basename(os.path.dirname(d["arquivo"])) == "emendas":    # emenda herdada: nome novo, sem colidir
        t3 = f"cap{novo:02d}_t3"
        os.rename(f"emendas/{d['take']}.wav", f"emendas/{t3}.wav")
        os.rename(f"takes/{d['take']}", f"takes/{t3}")
        d["arquivo"] = d["arquivo"].replace(f"/{d['take']}.wav", f"/{t3}.wav")
        d["pasta"] = d["pasta"].replace(f"/{d['take']}", f"/{t3}")
        d["take"] = t3
    json.dump(d, open(f"cap{novo:02d}.json", "w"), ensure_ascii=False, indent=1)
    os.remove(f"cap{velho:02d}.json")
    os.rename(f"titulos/cap{velho:02d}.wav", f"titulos/cap{novo:02d}.wav")
tj = json.load(open("titulos/titulos.json"))
novo_tj = {}
for k, v in tj.items():
    n = MAPA.get(int(k), int(k))
    v["wav"] = v["wav"].replace(f"cap{int(k):02d}.wav", f"cap{n:02d}.wav")
    novo_tj[f"{n:02d}"] = v
json.dump(dict(sorted(novo_tj.items())), open("titulos/titulos.json", "w"), ensure_ascii=False, indent=1)
```

  Resultado: ficam `cap00` a `cap05` e `cap08` a `cap13`; `cap06.json` e `cap07.json` nascem no passo 2. Emendas herdadas: `cap02_v2`, `cap03_v2` (sem mudança),
  `cap08_t3`, `cap09_t3`, `cap10_t3`, `cap12_t3`.

**1. Gerar os 5 nós** no fluxo único (`generations_count: 1`, rótulos da tabela acima). O Kaik exporta o zip. Anotar `node` e `sessions` em
`nos_elevenlabs.json` (chaves novas `"6"`, `"7"`, `"emendas"`, `"insercoes"`, `"titulos"`).

**2. Capítulos novos:** `python3 -I proc.py 06=<mp3 do nó cap06> 07=<mp3 do nó cap07>` (cria `cap06.json` e `cap07.json`; conferir "pê-móqui" e "Sim ou Não" no log).

**3. Títulos novos:** o `titulos.py` alinha **todos** os `TITULOS` do `tts_textos.py` (13) com o MP3, e o nó só tem 2 títulos; além disso ele reescreve
`titulos/titulos.json` só com o que processa. Sem mexer na ferramenta: rodar numa pasta irmã (`t3v2/narracao_tit/`, porque o `proc.py` acha o `kit/` subindo duas pastas)
com cópias das ferramentas, do `config_narracao.json` e de um `tts_textos.py` cujo `TITULOS` seja só `{6: "Etiquetas.", 7: "Campos personalizados."}` (e o `CAPS` completo),
e copiar de lá `titulos/cap06.wav`, `titulos/cap07.wav` e as duas entradas para o `titulos.json` da pasta principal. O melhor é a ferramenta ganhar uma opção `--so 6,7`.

**4. Emendas no lugar (8 trocas):**
- Guardar o JSON de cada capítulo cujo take é o original, para poder refazer: `cp cap01.json cap01.v1.json` (idem 04, 05, 11, 13).
- Nos capítulos 9 e 10 o take atual já é uma emenda do T3: `cp cap09.json cap09.v1.json; cp cap10.json cap10.v1.json`. O `emendar.py` então lê a emenda
  herdada (`takes/cap09_t3`, `takes/cap10_t3`) como base e o `trocas.json` lista só as trocas novas (a troca herdada do cap10, "Repara que cada mudança já grava
  sozinha.", já está dentro desse áudio e não se paga de novo).
- Colocar o `trocas.json` acima em `t3v2/narracao/` e rodar `python3 -I emendar.py <mp3 do nó emendas>`. Saída: `emendas/cap{01,04,05,09,10}_v2.wav`. O resumo precisa mostrar folga >= 0,2 s em todas e nenhum
  `ATENÇÃO` ou `CORTADA`.

**5. Inserções (4 frases), ainda sem ferramenta:** o `emendar.py` não tem modo de inserir. Estender com um passo depois do laço das trocas, usando a função `inserir` acima, o
mesmo cálculo de `clips` (agora sobre o MP3 do nó `T03v2 inserções`, com as 4 frases) e a igualação de volume por LUFS que o script já faz. Cap10: partir da saída do passo 4
(`emendas/cap10_v2.wav`) e gravar `emendas/cap10_v3.wav`. Cap11 e cap13: partir do take original (`carregar_cap`) e gravar `emendas/cap11_v2.wav` e `emendas/cap13_v2.wav`.
Antes de usar, rodar a extensão no exemplo (`exemplos/dominex-t3`), como manda o `CLAUDE.md` do repositório.

**6. Refazer palavras e legendas:**
`python3 -I proc.py 01=emendas/cap01_v2.wav 04=emendas/cap04_v2.wav 05=emendas/cap05_v2.wav 09=emendas/cap09_v2.wav 10=emendas/cap10_v3.wav 11=emendas/cap11_v2.wav 13=emendas/cap13_v2.wav`.
Conferir no log as palavras vigiadas e, pelas `words` novas, que cada frase trocada termina >= 0,2 s antes da palavra seguinte.
O `asr_fix` do `config_narracao.json` (`cap11_v2`: "1800" para "18000") herda a correção do T3 para o take novo do cap11; confirmar que o id do take no log é `cap11_v2`.

**7. Legendas e edição** seguem o fluxo normal (`legendas.py`, `legendas_aula.py`, `edit/`); não fazem parte da voz.

## O que regravar em vídeo (zero crédito de voz)

- **Obrigatório (a tela mudou ou há fala nova):** cap01, cap04, cap05, cap06, cap07, cap09, cap10, cap11, cap13.
- **Recomendado (mesmo áudio, mas a 1.38.9 aparece de fundo ou na ficha):** cap02 e cap03 (a janela "Novo Cliente" ganhou "Etiquetas" e "Campos personalizados"), cap08
  (botões do topo atrás da janela), cap12 (ficha do equipamento com "Ações" e selo "Em garantia").
- **Pode ficar como está:** cap00 (conferir só o menu lateral).

## Duração (limite do pedido: +2 min)

| Parcela | Segundos |
| --- | --- |
| cap06 Etiquetas (35,6 s de fala estimada + 0,9 s de pausas entre linhas) | 36,5 |
| cap07 Campos personalizados (34,0 s + 0,9 s) | 34,9 |
| cap10: frase anexada | 6,9 |
| cap11: duas frases inseridas | 7,5 |
| cap13: uma frase inserida | 5,2 |
| Duas vinhetas de capítulo novas (>= 3,2 s cada, `perfis/domiflix/PERFIL.md:23-27`) | ~7 |
| Folga de robô nos capítulos novos e alterados (cliques que não cabem dentro da fala viram trecho acelerado) | ~8 |
| **Soma** | **~106 s = +1:46** |

T3: 12:13 (733 s). v2: ~14:00. Faixa provável +1:35 a +1:55; ultrapassa +2:00 se o robô dos capítulos 6 e 7 precisar de mais de ~12 s além da fala. Se isso acontecer, tirar primeiro
as frases dos cortes 2 e 3 abaixo (cada uma poupa ~4 a 5 s).

## Cortes (para ganhar folga de créditos ou de tempo)

Cada corte vale para o `tts_textos.py` e para a linha do `roteiro.md`; o valor inclui o separador ` [pause] ` (ou a quebra de linha, no corte 5).

| Corte | O que sai | Créditos | Segundos | Perde |
| --- | --- | --- | --- | --- |
| 1 | Troca #1 (selo PJ): o cap01 fica com "etiqueta" | 63 | 0 | O esclarecimento "selo" x "etiqueta colorida" |
| 2 | Inserção D (o recap fala das etiquetas e do campo) | 86 | 5,2 | O recap não cita as novidades |
| 3 | Inserção B (cap11, etiquetas do cliente na escolha) | 68 | 4,1 | A etiqueta aparece na tela sem fala |
| 4 | Troca #8 ("clico no mais" volta a "e criar") | 64 | 0 | A exatidão do rótulo do botão de mais |
| 5 | Linha dos fornecedores do cap07 ("Os fornecedores têm os campos deles...") | 63 | 4,6 | A menção aos campos de fornecedores |

Cortes 1 + 2 + 3 = 217 créditos (total 1.607, folga 293). Cortes 1 a 4 = 281 (total 1.543, folga 357). A recomendação é **não cortar nada** e usar a folga de 76 num teste de pronúncia (18) ou numa
regeração curta; a linha 3 do cap06, a única com "pê-móqui" (134 caracteres), só cabe numa regeração se sair o corte 1 ou o 2.

## Extras que NÃO estão nos 1.824 (se o Kaik quiser, com o custo)

| Extra | Onde | Caracteres + separador |
| --- | --- | --- |
| "O menu Ações guarda o Editar e o Excluir, e a etiqueta fica embaixo do nome." | cap12, depois da primeira linha (inserção) | 75 + 9 |
| "Se você ligar Mostrar nos portais, o cliente também vê essa etiqueta no portal dele." | cap06, depois de "Salvar etiqueta" (inserção) | 83 + 9 |
| "A coluna Portal libera cada campo pra aparecer no portal do cliente." | cap10, depois de "Marco como obrigatório" (inserção) | 66 + 9 |
| "E aqui também dá pra marcar etiquetas, que a gente vê já já." | cap02, depois de "Origem" (inserção; exige recompor o cap02) | 58 + 9 |
| "Na lista de equipamentos, o Filtros também separa por etiqueta." | cap10 ou cap11 (inserção) | 63 + 9 |

Somados: 390 créditos, o que levaria o total a 2.214 (acima do orçamento). Com os cortes 1 a 4 ficariam em 1.929, ainda acima de 1,9 mil; entram só alguns, a critério do Kaik.

## Pronúncia e testes

- **PMOC** → "pê-móqui", convenção planejada em T10, T11, T13, T14 e T19; o PERFIL (`perfis/domiflix/PERFIL.md:53`) pede teste antes e ainda não houve geração. Está na `trocas` do `config_narracao.json`.
  Aparece 2 vezes no cap06 ("tem contrato de pê-móqui", "escrevo Contrato pê-móqui"). Plano B: "pê, ême, ó, cê" (uma troca de linha no `tts_textos.py` e no config); regerar só a linha 3 do cap06 custa 134.
- **Sim/Não** → a fala diz "Sim ou Não"; o `config_narracao.json` devolve "Sim/Não" na legenda (`numeros`, três palavras faladas viram uma).
- Nomes novos sem pronúncia especial: Preferencial, Horário de acesso, Em garantia, Ações, Configurações.
- Ouvir de ouvido na primeira geração: "Configurações" (4 vezes nas emendas, no cap06 e no cap07), "Ações" (5), "pê-móqui" (2).

## Se o botão "Configurar Campos" for renomeado para "Configurações"

O botão da página Equipamentos ainda se chama "Configurar Campos" (`src/lib/i18n/messages/app/equipment.ts:21`) e abre a janela "Configurações de equipamentos"
(`src/components/customers/EquipmentSettingsDialog.tsx:29`), que abre em Categorias. Se o app renomear o botão (candidato a pedido ao time do app), a frase da linha 1 do cap10
(`15,88 a 18,68`, "Em Configurar Campos estão os que já vêm prontos:") vira **"Em Configurações estão os que já vêm prontos:"** (45 caracteres + 9 de separador = 54 créditos; cabe na folga).

## Falas mantidas que citam a interface (conferidas na 1.38.9)

| Cap. v2 | Fala mantida | Rótulo ou tela citado | Evidência |
| --- | --- | --- | --- |
| 01 | "A tela tem duas abas, Clientes e Fornecedores." | abas do topo | `src/components/customers/CustomersPageChrome.tsx:80-89` |
| 01 | "...três botões...: Configurações, Formulários de captação e Novo Cliente" | botões do topo, aba Clientes | `src/components/customers/CustomersPageChrome.tsx:60-73` |
| 02 | "Receber mensagens pelo WhatsApp... Com o número completo, libera essa opção" | interruptor do WhatsApp | `src/lib/i18n/messages/app/customers.ts:100`; `src/components/customers/CustomerFormDialog.tsx:564` (`disabled={!hasMobile}`) |
| 02 | "Agora é só clicar em Criar" | botão do formulário de cliente | `src/components/customers/CustomerFormDialog.tsx:381-385` (`customer ? t.save : t.create`) |
| 04 | "Já tem Indicação, Instagram, Google e WhatsApp." / "Adicionar" | lista e botão da seção Origens | `src/components/customers/CustomerOriginManagerDialog.tsx:20,145`; `src/lib/i18n/messages/app/equipment.ts:330-346` |
| 05 | "No cartão Informações..." | cartão da ficha | `src/pages/CustomerDetail.tsx:850-855` |
| 09 | "O botão pra cadastrar fica aqui em cima, do lado direito: Novo Fornecedor." | botão no topo da coluna da ficha | `src/components/customers/SuppliersTab.tsx:194-201` |
| 09 | "Na ficha ficam os dados e o Histórico de Gastos." | cartão da ficha do fornecedor | `src/lib/i18n/messages/app/customers.ts:560` |
| 10 | "Em Configurar Campos estão os que já vêm prontos" | botão da página de equipamentos | `src/lib/i18n/messages/app/equipment.ts:21`; `src/components/customers/EquipmentPageChrome.tsx:49-52` |
| 11 | "Novo Equipamento" / "Criar" | botão da página e botão do formulário | `src/lib/i18n/messages/app/equipment.ts:19-21,71`; `src/components/customers/EquipmentPageChrome.tsx:53-58` |
| 11 | "Logo abaixo [da Categoria], em Etiquetas" | ordem dos campos do formulário de equipamento | `src/components/customers/EquipmentFormDialog.tsx:381-411` (Categoria, depois Etiquetas, depois os campos configuráveis) |
| 12 | "Em Gerar Etiqueta você escolhe o que sai impresso" | botão da ficha do equipamento | `src/pages/EquipmentDetail.tsx:581`; `src/lib/i18n/messages/app/equipment.ts:153` |
| 12 | "o Baixar quê-érre salva a imagem" | botão do diálogo da etiqueta | `src/lib/i18n/messages/app/equipment.ts:325` ("Baixar QR (PNG)") |

Pontos de atenção que a fala mantida não cobre e a gravação precisa tratar: a janela do botão "Configurar Campos" abre em **Categorias** (o robô clica em "Campos personalizados" no menu da esquerda enquanto a
fala diz "Em Configurar Campos estão os que já vêm prontos"); e nenhum arquivo do menu lateral mudou entre a 1.38.6 e a 1.38.9, então "Eles ficam em Gestão, Equipamentos" continua valendo.
