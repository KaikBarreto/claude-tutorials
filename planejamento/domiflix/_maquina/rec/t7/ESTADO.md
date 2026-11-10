# T7 · estado da gravação (agente A, porta 54321) · atualizado em 31/10 21:00

## 06/11 00:4x · reinício do container (00:39) · nota do coordenador
- Capítulos 00 a 14 renderizados (câmera 0 problema, recorte ok). O finish das 00:3x parou no meio do vídeo (o `video_sem_audio.mp4` de
  164 MB ficou incompleto e o `mix.wav` estava em `/dev/shm`, apagado). O coordenador roda de novo o `rec/t7/finish_t7.sh` (piso de 1,5 GiB;
  ele apaga o vídeo incompleto), depois das regravações 07 e 11 do T22. Revisão e entrega: coordenador.

## 05/11 21:56 · regravação na 1.38.24: fase 2 (G) feita; montar e renderizar só com "T7: render"
- App 8080 na 1.38.24; falso 54334 (`FAKE_NOW=2026-11-11T08:50:00-03:00 FAKE_PORT=54334 rec/run.sh fake`); robô com
  `FAKE_URL=http://127.0.0.1:54334`.
- Voz (lote 9): `t7/narracao/cap14.json` (131,20 s), `titulos/cap14.wav` (2,64 s); emendas sem compressão (`EMENDA_COMPRIME_MAX=0`,
  `empurra`): cap03 L3 "área de Checklists" (`emendas/cap03_v2.wav`, 33,92 s, folga 0,28 s) e cap13 L4 inserida
  (`emendas/cap13_v2.wav`, 54,62 s, +9,42 s). Cópias: `cap03.v1.json`, `cap13.v1.json`, `trocas.json.cap05_3110`, `*.antes_1.38.21`.
  `tts_textos.py`/`config_narracao.json` = os do planejamento; `titulos.py`, `emendar.py` e `pausas.py` = os da skill.
- `gerar.py` (antes: `gerar.py.antes_1.38.24`): cap13 com 5 linhas; cap14 refeito sobre a voz real (hold 3,7 s no arrasto, gaveta
  rolada por eval até o Local e até Início/Fim); cap02 L6 rola a página por eval (sem isso o mapa dava zoom e atrasava 6,2 s).
- Gravações em `rec/t7/t7-capNN.*` (00 a 14), resumos em `.g-1.38.24/NN.out` (fila: `fila_g.sh`): 0 falho em todos; maxLate 00 0,04 ·
  01 0,06 · 02 0,11 · 03 0,00 · 04 0,16 · 05 0,78 · 06 0,34 · 07 0,04 · 08 0,46 · 09 0,72 · 10 0,21 · 11 0,00 · 12 0,60 · 13 0,00 · 14 0,15.
  Sementes `apos-capNN` não regravadas (as de 03/11 valem).
- Para a montagem: cap14 entra entre o cap12 e o cap13; a L4 nova do recap pede trecho da gaveta Editar OS (cap14: arrasto ~72-77 s,
  aviso "OS atualizada" ~92-97 s); cap09 mostra o P23 do app (texto cru "data:image/png;base64..." de ~28,8 a 34,7 s): cortar ou cobrir.

App **1.38.9 no ar** (8080); meu falso (54321) com o schema da 1.38.9; `snap.mjs base` refeito (`.base-t7.json`).
Regra do coordenador (sem exceção): navegador/gravação/render/teste pesado só sob `flock /home/claude/domiflix/.heavy.lock nice -n 10 ...`
e **um flock por capítulo**. Disco: ~8,6 GB livres (parar abaixo de 3 GB e avisar). Gravações brutas pequenas (1 a 4 MB cada).

## Recorte do celular (correção pedida pelo Kaik, FEITA)
Causa: `Stage._render` só recortava o canto arredondado da tela quando a BORDA do lado estava dentro do quadro; no zoom a borda de
cima/baixo sai e o canto (~100 px) ainda invade (362 quadros de risco no cap. 1). Conserto: `pad` em `ferramentas/edit/stage.py` + cópia
`t7/edit/stage.py` (só com `stage.phone`; 16:9 idêntico). Provas: `testes/recorte_celular.sh` (novo 0,004; antigo 18 de 30 quadros com canto
reto, erro 1,00; 16:9 50/50 idêntico bit a bit), `testes/identidade_domiflix.sh` = IDÊNTICO ao T3 (log `scratchpad/logs/identidade_base.log`),
`auditar_recorte.py` (cap. 1, código antigo acusa 9 quadros; os 3 do código novo eram o repouso exato, meio pixel de arredondamento do
`_static`, já tratado: reconferência em `rec/t7/.testes-recorte2.out`). Folha só das transições:
`t7/edit/out/cap01/cap01.folha_transicoes.jpg`. Prévia nova do cap. 1 enviada ao `main` (20:52): `t7/edit/out/cap01/cap01_previa.mp4`.
Anotado em `docs/05-edicao.md` (Celular) e `docs/08-licoes.md`. `render_um.sh NN` agora roda `auditar_recorte.py` na mesma posse (log
`t7/edit/out/recorte_NN.log`).

## Gravação (cadeia `fila_grav2.sh`, saída `rec/t7/.fila-main2.out`, por capítulo `.fila-NN.out`)
Itens: `"02 --seed" ... "10 --seed" "11" "12" "13"` (um flock por capítulo; `--seed` grava `apos-capNN`; para no 1º `--seed` com falha).
- cap. 0: final (20:12, 0 falhos, maxLate 0,12). cap. 1: final (20:17, 0 falhos, maxLate 0,24, 70,5 s), renderizado com o recorte novo.
- cap. 2: gravado 20:51, 0 falhos, **maxLate 2,36 = regravar**. Causa: o mapa da rota (MapLibre desenhado por software) deixa a página
  ocupada ~7 s depois do A Caminho; o hover do mapa (`at` 11,8 s) esperou ~3 s. Conserto no gerar.py (já feito, prever.py sem atrasos): sem
  hover/zoom do mapa em "mapa"; passo `eval js_quieto()` espera a página sossegar; selo A Caminho em "Caminho,"; hover do caminho 1,4 -> 0,8;
  Waze 0,4 -> 0,2 e Google Maps em "Google" − 0,2; zoom do mapa passa para "a posição do técnico" (specs.py). Regravar SEM `--seed`
  (o estado final é o mesmo; `apos-cap02` já existe): `bash rec/t7/fila_grav2.sh "02"`, depois do 1º lote ou quando houver vaga de espera.
- Demais capítulos: aguardando a cadeia. Para cada um ver `.fila-NN.out` (falhos, maxLate) e conferir `406 GET form_responses` como único erro
  esperado.

## Ferramentas prontas
- `rec/t7/gerar.py [NN...]` -> `capNN.json` (âncoras na fala); `prever.py NN` (estimativa de atraso sem navegador); `rodar.sh NN [--rapido] [--seed]`;
  `fila_grav.sh`/`fila_grav2.sh`; `render_um.sh NN` (specs, montar_cap, auditar_camera, render + prévia + auditar_recorte numa posse, confere_render);
  `testes_recorte.sh [capNN]` (testes de recorte numa posse).
- `resumo.py NN [--ens]`; `ensaio.py`; `snap.mjs base|diff N`; `fotos.py`; `semear_pesquisa.py`; `folha.py NN t1,t2,...`; `specs.py`.
- Edição (`t7/edit/`): `montar_cap.py NN`, `overlay.py` (aviso em coluna ao lado do celular), `ilustra_pdf.py`, `montagem_cap13.py` (SÓ depois das
  gravações e ANTES da limpeza; sob a trava), `confere_render.py`, `auditar_recorte.py`, `folha_transicoes.py`, `caps/T7.aula.json`.
  Na skill (`ferramentas/edit/`): `stage.py` (conserto), `auditar_recorte.py`, `folha_transicoes.py`; `testes/recorte_celular.sh/.py`.

## Lições já aplicadas (gerar.py)
- `hover`/`click` em elemento FIXO fora da faixa do runner (centro y > 774 ou < 96) rola em vão ~7 s: usar `apontar` ou `toque`.
- Passo ~ 0,45 s + `seconds`; hovers de 0,2 a 0,4 s nas cadeias. Mapa da rota: não consultar a página enquanto ele desenha (`js_quieto`).
- cap. 12: sem hovers nos campos nome/comentário; arrasto da nota 1,5 s antes de "Preencho"; "Enviar avaliação" por `toque`; marca L4 antecipada.

## Falta (ordem)
1. Cadeia 03..13 (+ regravar cap. 2 e quaisquer capítulos com `lateBy` >= 0,8).
2. Render por capítulo: `bash rec/t7/render_um.sh NN` (cap. 0 já aceito: pode ir à fila), `folha_zooms.py`, `confere_render.py`, `/__dev/unknowns`.
3. cap. 13: `montagem_cap13.py` (sob a trava) com as gravações brutas ainda no disco -> render do cap. 13 -> só então limpeza.
4. `titulos.py`/`finish.py` (/dev/shm se o disco apertar), `legendas_aula.py`, `entregar.py out/T7 "Domiflix T7 - O técnico em campo"`, `ln -f` de
   `.mp4/.srt/.vtt` em `entrega_final/`, limpeza de gravações/renders/`proj/build/{stems,music.wav}`.
5. Lições do T7 em `/home/claude/claude-tutorials/docs/08-licoes.md` (rascunho `rec/t7/LICOES.md`; só o recorte já foi), `rec/t7/HANDOFFS.md`
   ("Achados da gravação"), avisar o T8 (Fita isolante 28 / consumo 2 rolos).
6. Relatório final (<= 200 palavras) só por SubagentHandback.

## Regras que continuam valendo
`export TUT_HOME=/home/claude/domiflix`; sem `pkill`/`killall`; `rm` só com `"${VAR:?}"`; sem commit/push; dados fictícios; escrever só em `t7/`,
`rec/t7/`, `rec/fakebase/seeds-extra/t7/` e handlers novos (e `ferramentas/edit/` + docs nesta correção); o app em 8080 nunca é reiniciado;
background com `timeout` até 7200000; matar só PID exato próprio.
