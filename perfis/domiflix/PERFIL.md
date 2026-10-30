# Perfil Domiflix · trilha de tutoriais do Dominex

**Este perfil é o padrão do T3 ("Clientes, Fornecedores e Equipamentos", 30/10/2026) congelado.** Vale para todos os
tutoriais da trilha Domiflix (são 20). Tudo aqui é obrigatório e fica igual de aula para aula: só muda o conteúdo.
Nada muda sem pedido do Kaik. Na dúvida, compare com o T3 completo em `exemplos/dominex-t3/`.

## Instalar
```bash
TUT_HOME=~/domiflix TUTORIAL=t4 PERFIL=domiflix bash <pasta-da-skill>/instalar.sh
```
Instala a marca Dominex (vinheta do capacete), a voz, as pronúncias, o padrão de montagem (`aula.json`) e o gravador
com o Supabase falso e o mundo fictício da Glacial Cold Brasil. Prova de que a identidade é a mesma do T3:
`bash testes/identidade_domiflix.sh` (palco, cartão de capítulo, abertura, cartela e som: tem de dar "IDÊNTICO ao T3").

## Identidade (marca `perfis/domiflix/marca`, estilo `dominex-capacete`)
- 1920×1080, 30 fps, H.264 (CRF 20) + AAC; ~−16 LUFS, pico ≤ −1 dBTP.
- **Vinheta de abertura** (4,4 s): as 3 peças do capacete se encaixam (som metálico + assinatura em Ré maior), brilho
  metálico, o capacete vai para a esquerda e o DOMINEX sai de trás; embaixo "▶ DOMIFLIX" + título da aula; escurece.
- **Cartela final** (3,9 s): mesma montagem do logo + "Até a próxima aula!".
- Cores: verde **#00C597** (acento), escuro **#1E1E1E**, gelo **#F3F4F6**. Fonte **Montserrat** (a do app).
- **Palco escuro** próprio (curvas iluminadas no verde + fio ciano, bloom, vinheta, granulado), janela do app com
  cantos de 16 px, sombra 0,35, margem 44 px. Nunca papel de parede de terceiros.
- **Vinheta de capítulo** (todo capítulo menos o primeiro): cobre a tela do computador; área em maiúsculas em cima
  (CLIENTES, FORNECEDORES, EQUIPAMENTOS, RESUMO...), título grande Montserrat 800 (112 px; 92 px se passar de 2
  linhas), barra verde vertical; a Fernanda lê o título em 0,70 s; dura ≥ 3,2 s (estica com o título longo);
  fusão de entrada 0,40 s e de saída 0,50 s; whoosh na entrada (−15 dB), pop quando o título pousa (−22 dB), whoosh
  descendente na saída (−16 dB).
- Cursor desenhado grande, mão em botão, barra em campo, quique e anel verde no clique.
- **Sem**: contador de etapas ("Passo 1/5"), cartão pequeno de título, travessão na copy, logo de terceiros nos
  desenhos, promessa de funcionar offline.

## Voz (`voz.json`)
- ElevenLabs, **Fernanda - Natural Conversations** (`KHmfNHtEjHhLK9eER20w`), modelo **eleven_v4**, pt. Não mexer
  nas voice settings. Duas versões por nó (o padrão). Ritmo pela pontuação; `[pause]` só onde precisa de respiro.
- Um fluxo por tutorial: um nó por capítulo, um nó com os títulos dos capítulos (separados por `[pause]`), correções
  num nó só. Nunca repetir geração para "tentar de novo". Consultar status só das sessões na fila.
- O Kaik exporta o fluxo inteiro em zip e anexa; o `proc.py` descobre cada capítulo pelo conteúdo. Se a exportação
  trouxer outra versão de um capítulo já sincronizado com a gravação, manter a sincronizada (e avisar).

### Pronúncia (no texto do TTS; a legenda usa a grafia normal; `narracao/config_narracao.json`)
| Tela / legenda | Texto do TTS |
|---|---|
| QR Code / QR | quê-érre côde / quê-érre |
| Hi-Wall | rai-uól |
| BTUs | bê-tê-ús |
| Waze | Uêiz |
| 18.000 BTUs | dezoito mil bê-tê-ús |
| 127 V, 220 V e 380 V | cento e vinte e sete, duzentos e vinte e trezentos e oitenta volts |
| Asaas | asas |
| DRE | dê érri ê |
| PMOC | soletrar foneticamente quando aparecer (testar antes) |
CNPJ, CPF, CEP, OS, LGPD: escrita normal. Números por extenso como se fala. Palavra nova difícil: testar num trecho
curto e anotar aqui.

## Fala (pedido do Kaik: "o mais natural possível, como num tutorial mesmo, sem parecer engessado")
- Colega mostrando o sistema ao vivo: "vou clicar aqui em Novo cliente", "repara que ele já trouxe o endereço",
  "pronto, salvou". "A gente" e "você". Nada de "neste capítulo abordaremos", "é possível realizar".
- Frases curtas; conectores de fala (então, agora, olha, repara, pronto, beleza, aqui em cima, lembra que), no máximo
  um "olha"/"repara" a cada 3 ou 4 frases. Exemplo concreto antes da regra. "Uma dica:" quando houver.
- **Só possibilidades** (Kaik, 30/10): nunca o que o sistema não faz nem dificuldades; diga o caminho positivo
  ("pra ver os detalhes, é só clicar"). Vale para avisos e cartões na tela.
- Rótulos ditos exatamente como na tela. Fala que depende de comportamento que pode mudar: escrever para valer nas
  duas versões.

## Estrutura de cada tutorial
1. Abertura (~30 s): "Neste tutorial a gente vai..." com o porquê.
2. Pré-requisito (~15 s): qual tutorial ver antes, numa frase (aviso na tela: "Antes: <tutorial>").
3. Capítulos: cada um abre com transição falada ("bom, agora que o cliente tá cadastrado..."), nunca "capítulo 3".
4. Recapitulando (~1 min): o que ficou pronto, em fala corrida.
5. Próximo (~15 s): o tutorial seguinte (aviso: "Próximo: <tutorial>").
Duração = tempo natural da fala (o T3 deu 12:13 com 12 blocos).

## Mundo fictício e gravação
- Modo **fakebase** com o código do Dominex na **versão publicada** (o repositório do app é somente leitura):
  `git -C <repo> archive <commit> | tar -x -C <pasta>` → `DOMINEX_SRC=<pasta> rec/setup-app.sh` →
  `rec/run.sh build` → `rec/run.sh up`. Nunca gravar contra o Supabase real.
- Empresa **Glacial Cold Brasil** (climatização), usuária **Camila Duarte** (admin, MASTER). Clientes, fornecedores e
  marcas fictícios das sementes (`rec/fakebase/seeds`); documentos com dígito verificador válido; e-mails `.example`.
  Estado inicial de cada capítulo: `rec/fakebase/seeds-extra/<id>/apos-capNN.json` (o que os anteriores criaram).
- Aceite por capítulo: 0 passo falho, `lateBy` < 0,8 s, versão certa no rodapé, nada real na folha de contato.
- Pegadinha do app vira handoff de correções para o time (exemplo: `exemplos/dominex-t3/handoff-correcoes-app.md`).

## Edição
- `specs.json` como no T3 (`exemplos/dominex-t3/edicao/specs.json`): `kicker` = área, `titulo` curto, zooms de
  passo a passo com `min_w` 1300, destaques com o rótulo exato da tela, avisos "Dica: ..." no positivo.
- Câmera v2: `auditar_camera.py` com 0 problema e `folha_zooms.py` conferida antes de montar.
- Ilustração só para conceito que a tela não mostra: fundo branco, Montserrat, verde, objetos genéricos sem marca,
  texto medido para caber (exemplo: `exemplos/dominex-t3/ilustracoes/ilustra_qr.py`).
- Montagem com `perfis/domiflix/aula.json`: trilha lo-fi `music_db` −7, `music_duck_db` −8, **`music_seed` 3** (a
  mesma identidade sonora em todas as aulas), SFX ligados, CRF 20.

## Entrega
- Nome: **`Domiflix T<n> - <Título>.mp4`** + `.srt` + `.vtt` com o mesmo nome; o vídeo completo 1080p direto no chat.
- Mandar um capítulo de prévia cedo; depois a aula completa.

## Processo com o Kaik
- Roteiro em doc vivo compartilhado, aprovação antes de gerar a voz.
- Registro de pedidos e decisões em disco, atualizado a cada mensagem (ele manda ajustes em sequência).
- Velocidade importa: avisar o que está rodando e quanto falta; nunca deixar duas tarefas pesadas juntas.
- Commit/push só com ok explícito.
