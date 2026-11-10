# T22 · estado (porta 54337) · fase 2 (G) na 1.38.24 · EM ANDAMENTO (05/11 23:5x)

**Feito:** emendas da voz (9 trocas) na velocidade natural; robô ajustado às falas novas e ao ritmo; respiros na voz dos caps 02, 06, 07, 08 e 09;
ensaios `--rapido` (01, 03, 04, 05, 06, 07, 08, 09, 10, 11: 0 falho). **Em curso:** gravação final (G) de 00 a 11 (`lote.sh --gravar`).
**Não montar nem renderizar** antes do "T22: render" do coordenador.

Regras: `export TUT_HOME=/home/claude/domiflix FAKE_URL=http://127.0.0.1:54337`; backend e robô com `FAKE_NOW=2026-11-12T10:00:00-03:00`
(`FAKE_NOW=2026-11-12T10:00:00-03:00 FAKE_PORT=54337 rec/run.sh fake`). Navegador só sob `flock $TUT_HOME/.heavy.lock nice -n 10`, uma trava por
capítulo. Sem pkill; sem commit. **Sem `--seed`** (as `seeds-extra/t22/apos-capNN.json` de 05/11 valem; o `rodar.sh` recusa `--seed`).
- `rec/t22/lote.sh [--gravar] NN ...` (sem `--gravar`: ensaio `--rapido`); resumo em `rec/t22/_debug/{ens,rec}-NN.log`.
- `rodar.sh` para se o disco tiver < 1,5 GiB ou se o 8080 não responder 200 (confere antes e de novo dentro da trava).
- `prever.py NN [--ens]`: simula o ritmo com as durações medidas na última gravação (ou no ensaio rápido) e o `at` atual, sem navegador.
- `gerar.py` = `_head.py` + `_caps.py` + `_fim.py` (`bash rec/t22/montar.sh`). Versões da fase 1: `*.fase1` e `_fase1/` (roteiros e ensaios).

## 06/11 00:4x · reinício do container (00:39) · nota do coordenador
- O reinício parou a regravação do cap07 (00:32) e apagou o `/dev/shm`. Gravações boas em `rec/t22/`: 00, 01, 02, 03, 04, 05, 06, 08, 09, 10
  (0 falho; maior atraso 0,68 no cap06). O `t22-cap07.mp4` das 00:28 era a tomada g2 (5 atrasos, 1,32 s) e o `t22-cap11.mp4` das 00:30
  FALHOU no passo 1: abriu em Funcionários (o onBack do editor do organograma chegou depois do clique na aba "Perfil Comportamental").
- Conserto no setup do cap11 (`_caps.py`): espera de 3,5 s depois do Voltar (era 1,5) e um segundo clique na aba depois de 2 s.
- Fakebase 54337 religado com o FAKE_NOW certo; o coordenador regrava 07 e 11 (`lote.sh --gravar 07 11`, 00:4x). Depois: "T22: render".
- 06/11 01:0x **Gravação final completa (00 a 11)**: 07 regravado às 00:45 (0 falho, maior atraso 0,25 s); 11 às 01:0x (0 falho, 0,23 s).
  Conserto do cap11 (`_caps.py`): o Voltar do editor deixa a rota `/funcionarios/organograma` e a troca de aba a partir dela navega para
  `/funcionarios` (a página remonta na lista): o setup passa pela aba Funcionários antes do Perfil Comportamental. No setup `when`/`unless`
  NÃO valem (o `runSetup` executa todos os passos). "Excluir nó" na barra do quadro com `noScroll` (sem ele, 5,6 s e a L4 4,8 s atrasada).

## Voz (emendas 1.38.21, `recebido/1454_lote9/zip/T22_emendas.mp3`, 100,28 s)
- `t22/narracao/tts_textos.py` = o do planejamento (falas novas; o antigo em `tts_textos.py.antes_emendas`); `config_narracao.json` igual;
  `emendar.py`, `titulos.py`, `pausas.py` = os da skill (antigos em `*.antes_skill`); `proc.py` já era igual.
- `trocas.json` (9 trocas, `empurra` em todas) + `EMENDA_COMPRIME_MAX=0`. Originais em `capNN.v1.json` (01, 04, 07, 08, 09, 10); saída
  `emendas/capNN_v2.wav` e `proc.py` neles (logs `emendar_1_38_21.log`, `proc_emendas_1_38_21.log`). 0 palavra fraca nova.
- Durações com as emendas: cap01 38,45 s (+1,41), cap04 37,01 s (+5,17), cap07 34,58 s (+2,90), cap08 57,19 s (+8,15), cap09 33,56 s (+1,08;
  a L2 nova é mais curta e deixa 2,0 s antes da L3), cap10 46,13 s (+4,69).
- Respiros (`pausas.py`; o original de cada um em `t22/narracao/emendas/capNN.orig.json`; tempos no relógio de antes do respiro):
  cap02 `25.0:29.0` (as 28 perguntas, ~33 s, entre a L3 e a L4) -> 60,44 s; cap06 `15.35:2.4 36.7:19.5` (campos da Camila; os cinco técnicos)
  -> 70,06 s; cap07 `12.0:2.2` (anotação + arrasto da caixa) -> 36,77 s; cap08 `17.4:4.4 47.508:20.8` (zoom e Início no lugar; as 7 formas)
  -> 82,39 s; cap09 `11.1:16.0` (raias + 5 arrastos + Organizar) -> 49,56 s.

## Mudanças no robô na fase 2 (`_head.py`, `_caps.py`)
- **Rolagem consertada** (caps 03, 04, 05): `js_main_ate`/`rola_topo` rolavam o 1º `<main>` (o SidebarInset, que não rola); na fase 1 a página nunca
  descia (o eval devolvia o alvo ainda fora da tela, 1674 px). Agora rolam o contêiner que rola (o `<main>` interno); os alvos chegam a y 200/220.
- Falas novas: cap01 a grade entra no "Troco pra grade" (L1 fica na lista); cap04 L2 desce primeiro aos gráficos cruzados, L4 com Voltar no "Volto"
  e aba no "Perfil" (o "Com" casava "Comportamental"), Comparar no "ganha", opção do Bruno na virada para a L5; cap07 L3 o cursor passa pela
  lateral (Árvore, Destacar, Buscar) antes da Tela cheia; cap08 L3 o cursor passa pelas oito formas da lista e pousa em Tarefa e Decisão com
  `nth=1`; cap09 L2 sem duração ("Como fazer" por colar), L3 Organizar e depois Formatar; cap10 escudo e prancheta, Área/Frequência por colar e o
  Dono DIGITADO no "escrevo a Tatiane".
- Ritmo: `digitar_num(..., cps=)` e `clicar_colar()` novos; nomes longos por colar (nome do fluxograma, nomes das 7 formas do trecho rápido,
  Objetivo/Disparo); cap06 a 18-20 letras/s, Rafael no "Coloco"; cap07 texto da caixa a 24/s, arrasto no "Equipe", Exportar em tela cheia;
  cap11 recap enxuto (Interações + "Ver comparação" + Histórico do Bruno pela lista da esquerda + organograma em Tela cheia; `noScroll` na barra
  do quadro, que fazia cada clique tentar rolar ~6 s).
- **cap08, plano B:** o robô faz só a PRIMEIRA ligação (Chamado aberto -> Triagem; `LIGACOES[:1]`), com a repetição só se a
  ligação não pegou (`unless` na 1ª ligação). As que saem da Decisão falham (alça sob o texto) e o arrasto que erra a alça MOVE a forma;
  o rótulo ia para a última ligação, que podia ser a errada (ensaio: "Sim" na Triagem -> Decisão).

## Para a montagem (só com "T22: render")
- Respiro + corte nos trechos longos (o `finish.py` tira vídeo e áudio juntos; cortes em s do vídeo do capítulo):
  - cap02: silêncio de 24,9 a 54,2 s (as 28 perguntas, rápido 4x no roteiro); manter o início (Pergunta 1 e 2) e o fim (última pergunta e Enviar).
  - cap06: silêncio de 38,9 a 58,6 s (Rafael e os cinco técnicos); o de 15,2 a 17,9 s é curto (campos da Camila) e pode ficar.
  - cap08: silêncio de 17,2 a 22,0 s (zoom e Início no lugar, curto) e de 51,9 a 72,7 s (as formas do trecho rápido; L5 começa em 72,71).
  - cap09: silêncio de 10,9 a 27,2 s (raias + arrastos para as faixas + Organizar).
- **cap08, ligações pelo plano B:** a L5 ("As setas ligam... até a outra") cobre a ligação do robô; no "E na decisão, cada saída ganha um
  rótulo, sim ou não" cortar para o desenho já ligado (8 ligações, "Sim" e "Não"): é o primeiro quadro do cap09 (semente `apos-cap08`, antes do
  "Adicionar raia", ~1,7 s parado).

## 06/11 02:5x-03:4x · MONTAGEM ("T22: render") · PRONTA até as legendas; falta só o entregar.py (coordenador)
- cap03 regravado às 02:37 (0 falho, maior atraso 0,35 s): o tooltip do gráfico DISC (nome de pessoa real) não aparece mais (quadros 7-30 s conferidos).
- Edição em `t22/edit/`: `montar_cap.py` = o do T15 (computador + celular; o cap02 é 780x1688) + `rect`/`at`/`end` explícitos em zooms e destaques
  (antigo em `montar_cap.py.antes_celular`); `stage.py`/`overlay.py` = os da skill (antigos em `*.antes_skill`). `caps/specs.json` (modelo em
  `specs.modelo.json`), `caps/T22.aula.json`. `auditar_camera.py`: 0 instantes ruins nos 12 capítulos (repousos nos cliques colados no topo/borda).
- Cortes: cap02 [25,95-40,95] e [44,0-53,3] (perguntas 10 a 27 e a espera do Enviar); cap06 [41,0-57,4] (Júlia a Paulo; Bruno fica); cap08
  [56,2-72,2] (Relatório, Orientar e Fim do trecho rápido); cap09 [13,3-22,3] e [24,7-26,9] (3 arrastos e a espera; o 1º Organizar fica).
- Ilustrações = quadros reais da gravação (`t22/edit/assets/ilu_*.png`, janela em repouso [166,44,1587,992]): cap06 8,4-9,45 s = editor só com a
  Direção (o painel da "Nova caixa" piscava ~0,4 s ao criar o quadro); cap08 78,3 s até o fim = 1º quadro do
  cap09 (desenho ligado, "Sim"/"Não"; plano B, com destaque "Sim ou não"); cap11 19,2-21,75 s = organograma sem a "Nova caixa" (o editor cria uma ao abrir e o robô a exclui)
  e 25,3-26,8 s = lista de Fluxograma (a troca de aba a partir de /funcionarios/organograma cai em Funcionários por ~1,2 s).
- Avisos: cap00 "Módulo Funcionários / RH" e "Antes: Funcionários: Financeiro do Funcionário e Ponto Eletrônico"; cap05 e cap10 dicas; cap11
  "Próximo: Integração com WhatsApp".
- Render: `bash t22/edit/render_todos.sh NN ...` (uma trava por capítulo; MP4 em `t22/edit/out/capNN/`, WAV do capítulo em `/dev/shm/t22_caps/`
  para o disco ficar >= 1,5 GiB no finish). Sem o WAV (reinício apaga o /dev/shm), refazer só o áudio, sem renderizar:
  `cd t22/edit && python3 -I -c "import sys; sys.path.insert(0,'.'); from chapter import Chapter; [Chapter(f'caps/cap{n}.chapter.json').align_audio(f'/dev/shm/t22_caps/cap{n}.wav') for n in sys.argv[1:]]" 00 01 ...`
- Finish + legendas: `bash rec/t22/finish_t22.sh` (molde do T7: stems, music.wav e mix.wav em `/dev/shm/t22_finish`; não apaga `video_sem_audio.mp4`).
- **Resultado (06/11 03:41):** `t22/edit/out/T22/aula_final.mp4` 556,3 s (9:16), 1920x1080 30 fps, -15,9 LUFS (LRA 3,6), pico verdadeiro -3,6 dBFS;
  `pico_aac.py --so-medir`: nenhum pico acima de -1 dBTP depois do AAC. `video_sem_audio.mp4` mantido. Legendas: 142 (`out/T22/legendas/aula_final.srt/.vtt`).
  Folhas de 3 s da aula inteira: `t22/edit/out/T22/folhas3s/folha_01..07.jpg` (conferidas: 11 vinhetas, avisos Antes/Próximo, cortes, ilustrações).
  Cortes tiram 67,9 s. Renders dos capítulos em `t22/edit/out/capNN/` (190 MB; apagar só depois da revisão). `/dev/shm` do T22 apagado à mão
  (mix.wav e WAVs dos capítulos; o `proj/build/mix.wav` ficou como link quebrado). Disco depois do finish: 1,2 GiB livres.
- **Divergências do roteiro / app:** cap08 só a 1ª ligação filmada (plano B); cap09 L3 diz "da esquerda pra direita", mas o Organizar empilha as
  etapas em coluna (dagre por raia só com as ligações internas; semente `apos-cap08`); cap07 Tela cheia só com o cursor (API de tela cheia não
  grava); bugs do app escondidos com quadros reais: "Nova caixa" criada a cada abertura do editor do organograma (cap06 e cap11) e troca de aba
  a partir de `/funcionarios/organograma` que cai em Funcionários (cap11); semente `apos-cap08` com "Relatório de Serviço" sob "Chamado encerrado".
