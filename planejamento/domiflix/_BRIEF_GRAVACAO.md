# Briefing da gravação, edição e entrega · trilha Domiflix (uma aula, do roteiro ao vídeo final)

Molde: **T3** (`exemplos/dominex-t3/`: `robo/capNN.json`, `edicao/specs.json`, `edicao/T3.aula.json`) e `docs/04` a
`07`. Perfil `perfis/domiflix/PERFIL.md` (vale inteiro). Área de trabalho: `TUT_HOME=/home/claude/domiflix`,
aula em `$TUT_HOME/tnn/` (já instalada), robô em `$TUT_HOME/rec/`.

## Entradas
`planejamento/domiflix/Tnn/{roteiro,plano,inventario}.md` (coluna Tela = o que o robô faz; `[BACKEND: ...]`,
`[TESTAR ...]`, `[ILUSTRAÇÃO: ...]`), `Tnn/narracao/tts_textos.py` e, depois da voz, `$TUT_HOME/tnn/narracao/capNN.json`
(tempos de cada palavra e de cada linha). Sem `capNN.json` ainda: prepare tudo e deixe os `at` para depois.
`PRODUCAO.md` → "Alinhamentos entre aulas" vale por cima do roteiro (datas, sementes e handlers combinados entre aulas).

## Ambiente (não atrapalhar o outro agente)
- Uma instância do Supabase falso por agente, na porta da aula: `FAKE_PORT=543xx rec/run.sh fake`, e
  `export FAKE_URL=http://127.0.0.1:543xx` em TODO comando do robô (`docs/04-gravacao.md`, fim). A 54321 (padrão)
  fica desligada: robô sem `FAKE_URL` falha na hora em vez de gravar no mundo de outra aula. O app (porta 8080) é um
  só: `rec/run.sh app` sobe só ele (não faz nada se já estiver de pé). Depois de reinício do container, cada agente
  religa a própria porta e refaz a etapa que escrevia direto no arquivo final (gravação, finish).
- Data do mundo: `FAKE_NOW=2026-11-03T09:00:00-03:00` (terça) no backend E no robô, salvo se o `plano.md` pedir outra.
- Gravação e render só sob `flock $TUT_HOME/.heavy.lock` (um de cada vez na máquina), com `nice`.
  **Uma trava por capítulo** (cada gravação, ensaio ou render pega e solta a trava): nunca um lote inteiro sob um flock
  só. Em 31/10 um lote de 1 h do T3 v2 parou a fila de 4 agentes (T7, voz nova, storyboard do T0).
- Esperar uma etapa: rode o próprio comando em segundo plano e aguarde o aviso de término, sem laço de consulta. Nunca
  `pgrep -f` com o padrão dentro do próprio laço: ele acha o próprio laço e não termina (T3 v2 parado 16 min, 03/11).
- **Link ou QR escrito na tela** (portal, proposta, ponto, cobrança): grave com `APP_ORIGIN=https://www.dominex.app` para o
  link sair com o domínio real, e não `http://127.0.0.1:8080` ([docs/04-gravacao.md](../../docs/04-gravacao.md), "Endereço do
  produto na tela"). Desligada por padrão.
- Nunca `pkill`/`killall`; `rm` só com `"${VAR:?}"`; nada fora de `tnn/`, `rec/tnn/`, `rec/fakebase/seeds-extra/tnn/` e
  handlers novos em `rec/fakebase/handlers/` (um arquivo por função; não reescreva handler de outra aula: estenda).
- Código do app: só leitura (`$TUT_HOME/app` é a cópia de gravação, 1.38.19; `src-1.38.19` para ler).

## Etapas
1. **Mundo e backend falso**: estado de partida em `rec/fakebase/seeds-extra/tnn/` (herda o fim da aula anterior na
   ordem de exibição; `MUNDO_FICTICIO.md`), handlers/RPCs/edge functions da lista do `plano.md` → "Gravação".
   Teste com `node rec/recorder/smoke.mjs <rotas>` (0 problema) e `/__dev/unknowns`.
2. **Robô** (`rec/tnn/capMM.json`, formato do T3): `mark Ln` no início de cada linha (`linhas[i].s` do `capMM.json`),
   passos com `at` tirado da palavra que os anuncia, `label` em tudo que a edição usa, `seedExtra` encadeado
   (`tnn/apos-capMM`). Celular: `"device": "phone"` + passos `geo`/`clock`. Página pública: `"anonymous": true`;
   outra aba: `"sameTab": true`; outro usuário: `"user"`. Página fora do app (ex.: Guia Técnico): a volta recarrega o app;
   pausa na voz no fim da linha, `mark` só com o app carregado e `cortes` no recarregamento.
3. **Gravação** (`node rec/record.mjs rec/tnn/capMM.json --out rec/tnn --name tnn-capMM`): aceite = 0 passo falho,
   `lateBy` < 0,8 s, folha de contato sem dado real e sem aviso de erro do app ("Não foi possível", "erro", "Tente
   novamente", "indisponível", R$ 0,00 onde devia haver preço), rodapé com a versão do app. Um capítulo por vez.
4. **Edição**: `tnn/edit/caps/specs.json` (título e área da vinheta = `TITULOS`/`KICKERS`, escritos como na tela: aplique
   as `trocas` do `config_narracao.json`, ex.: "O teste disque." → "O teste DISC"; zooms e destaques por
   `label`; avisos por palavra; ilustrações) → `python3 -I montar_cap.py MM` → **`python3 -I auditar_camera.py` com
   0 problema** → `render_chapter.py` (fila) → conferir com `folha_zooms.py`. Celular: no capítulo, `stage.phone` e
   `cursor.touch` (`docs/05-edicao.md`, fim). `[ILUSTRAÇÃO]`: desenho por código (exemplo
   `exemplos/dominex-t3/ilustracoes/ilustra_qr.py`) ou cenas HTML (`docs/09-aula-ilustrada.md`).
5. **Montagem e entrega**: `titulos.py` → `finish.py caps/Tnn.aula.json` → `legendas_aula.py` → `entregar.py out/Tnn
   "Domiflix Tnn - <Título>"`; ponha `.mp4/.srt/.vtt` em `$TUT_HOME/entrega_final/` com `ln -f` (hardlink: o mesmo
   arquivo, sem gastar disco; nunca `cp`). Logo depois do `finish.py`, apague `proj/build/{stems,music.wav}` (~1 GB; só
   servem ao mix e o finish os refaz; o `mix.wav` fica). Depois da entrega, apague gravações e renders de capítulo,
   guardando a gravação do cap00, `video_sem_audio.mp4` e `proj/` (o `remendar_aula.py` usa). Disco: `df -h /home/claude`
   antes de gravar e antes do finish; abaixo de 3 GB, pare e avise.

## Regras do vídeo (as do T3)
Só o app real (nada inventado); dados fictícios (sem dado real, token ou senha na tela: senha só por `$TUT_SENHA`);
nada coberto com tarja (Kaik 03/11: dados de demonstração, preços de plano inclusive, aparecem como estão; só a fala e as
ilustrações não citam preço de plano); zoom sempre no alvo da ação (a montagem recusa capítulo com alvo fora do quadro);
vinheta falada por capítulo; sem contador de etapas; legendas em arquivo; vídeo completo 1080p; nenhum trecho parado
mais de ~20 s sem zoom ou destaque (o cap00 também tem zoom: no T18 a abertura ficou 32 s parada no Dashboard).
Antes de mandar ao main: folha de 3 s do vídeo INTEIRO, não só a de destaques.

## Relatório (≤ 200 palavras)
Duração final, specs e loudness (saída do `entregar.py`), problemas de câmera (deve ser 0), o que ficou diferente do
roteiro e por quê, handlers/sementes criados, pendências.
