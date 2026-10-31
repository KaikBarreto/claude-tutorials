# Briefing da gravação, edição e entrega · trilha Domiflix (uma aula, do roteiro ao vídeo final)

Molde: **T3** (`exemplos/dominex-t3/`: `robo/capNN.json`, `edicao/specs.json`, `edicao/T3.aula.json`) e `docs/04` a
`07`. Perfil `perfis/domiflix/PERFIL.md` (vale inteiro). Área de trabalho: `TUT_HOME=/home/claude/domiflix`,
aula em `$TUT_HOME/tnn/` (já instalada), robô em `$TUT_HOME/rec/`.

## Entradas
`planejamento/domiflix/Tnn/{roteiro,plano,inventario}.md` (coluna Tela = o que o robô faz; `[BACKEND: ...]`,
`[TESTAR ...]`, `[ILUSTRAÇÃO: ...]`), `Tnn/narracao/tts_textos.py` e, depois da voz, `$TUT_HOME/tnn/narracao/capNN.json`
(tempos de cada palavra e de cada linha). Sem `capNN.json` ainda: prepare tudo e deixe os `at` para depois.

## Ambiente (não atrapalhar o outro agente)
- Uma instância do Supabase falso por agente: agente A porta 54321 (`rec/run.sh up`), agente B
  `FAKE_PORT=54322 rec/run.sh fake` + `FAKE_URL=http://127.0.0.1:54322` no robô (`docs/04-gravacao.md`, fim). O app
  (porta 8080) é um só: suba com `rec/run.sh up` só se `rec/run.sh status` disser que está parado.
- Data do mundo: `FAKE_NOW=2026-11-03T09:00:00-03:00` (terça) no backend E no robô, salvo se o `plano.md` pedir outra.
- Gravação e render só sob `flock $TUT_HOME/.heavy.lock` (um de cada vez na máquina), com `nice`.
- Nunca `pkill`/`killall`; `rm` só com `"${VAR:?}"`; nada fora de `tnn/`, `rec/tnn/`, `rec/fakebase/seeds-extra/tnn/` e
  handlers novos em `rec/fakebase/handlers/` (um arquivo por função; não reescreva handler de outra aula: estenda).
- Código do app: só leitura (`$TUT_HOME/app` é a cópia de gravação, 1.38.6; `src-1.38.6` para ler).

## Etapas
1. **Mundo e backend falso**: estado de partida em `rec/fakebase/seeds-extra/tnn/` (herda o fim da aula anterior na
   ordem de exibição; `MUNDO_FICTICIO.md`), handlers/RPCs/edge functions da lista do `plano.md` → "Gravação".
   Teste com `node rec/recorder/smoke.mjs <rotas>` (0 problema) e `/__dev/unknowns`.
2. **Robô** (`rec/tnn/capMM.json`, formato do T3): `mark Ln` no início de cada linha (`linhas[i].s` do `capMM.json`),
   passos com `at` tirado da palavra que os anuncia, `label` em tudo que a edição usa, `seedExtra` encadeado
   (`tnn/apos-capMM`). Celular: `"device": "phone"` + passos `geo`/`clock`. Página pública: `"anonymous": true`;
   outra aba: `"sameTab": true`; outro usuário: `"user"`.
3. **Gravação** (`node rec/record.mjs rec/tnn/capMM.json --out rec/tnn --name tnn-capMM`): aceite = 0 passo falho,
   `lateBy` < 0,8 s, folha de contato sem dado real, rodapé com a versão do app. Um capítulo por vez.
4. **Edição**: `tnn/edit/caps/specs.json` (título e área da vinheta = `TITULOS`/`KICKERS`; zooms e destaques por
   `label`; avisos por palavra; ilustrações) → `python3 -I montar_cap.py MM` → **`python3 -I auditar_camera.py` com
   0 problema** → `render_chapter.py` (fila) → conferir com `folha_zooms.py`. Celular: no capítulo, `stage.phone` e
   `cursor.touch` (`docs/05-edicao.md`, fim). `[ILUSTRAÇÃO]`: desenho por código (exemplo
   `exemplos/dominex-t3/ilustracoes/ilustra_qr.py`) ou cenas HTML (`docs/09-aula-ilustrada.md`).
5. **Montagem e entrega**: `titulos.py` → `finish.py caps/Tnn.aula.json` → `legendas_aula.py` → `entregar.py out/Tnn
   "Domiflix Tnn - <Título>"`; ponha `.mp4/.srt/.vtt` em `$TUT_HOME/entrega_final/` com `ln -f` (hardlink: o mesmo
   arquivo, sem gastar disco; nunca `cp`). Depois apague gravações, renders de capítulo e `proj/build/{stems,music.wav}`
   da aula (disco: ~7 GB livres no total, `df -h /home/claude` antes de gravar; abaixo de 3 GB, pare e avise).

## Regras do vídeo (as do T3)
Só o app real (nada inventado); dados fictícios (sem dado real, token ou senha na tela: senha só por `$TUT_SENHA`);
sem preço de plano da Dominex; zoom sempre no alvo da ação (a montagem recusa capítulo com alvo fora do quadro);
vinheta falada por capítulo; sem contador de etapas; legendas em arquivo; vídeo completo 1080p.

## Relatório (≤ 200 palavras)
Duração final, specs e loudness (saída do `entregar.py`), problemas de câmera (deve ser 0), o que ficou diferente do
roteiro e por quê, handlers/sementes criados, pendências.
