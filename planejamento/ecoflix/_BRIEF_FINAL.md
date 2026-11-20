# Briefing do fechamento · gravação final e montagem de uma aula EcoFlix (uma aula por agente)

Repositório da skill: `/home/claude/claude-tutorials` (caminhos relativos a ele); área de trabalho `$TUT_HOME` =
`/home/claude/ecoflix`. App **1.60.22** em `$TUT_HOME/app/dist` (servido na 8080: `bash rec/run.sh app` se cair), tela 1600x900.
A aula já tem: fala aprovada, robô ensaiado (no 1.60.18 ou no 1.60.22), **voz real processada** (`$TUT_HOME/tNN/narracao/capNN.json`, sem
"estimado", e `titulos/titulos.json`) e as ilustrações v3 feitas ou em andamento (`Tnn/cenas_v3/`, `Tnn/cenas/ilustracoes.json`).
**Tarefa**: gravação final com a voz, montagem e prévia da aula, no padrão da T08 (aprovada pelo Kaik: "ficou muito bom").
Sem aprovação no meio: termine e relate. Fechada antes no mesmo molde: a **T02** (`$TUT_HOME/t02/edit/`, `rec/t02/t02_final.sh`;
`ilus_local.json` para ajuste de ilustração sem editar o `ilustracoes.json`).

## Modelo a copiar: a T08
- Gravação final: `$TUT_HOME/rec/t08/t08_final.sh` (um capítulo por vez pela fila, instância religada no `FAKE_NOW` do
  capítulo, qualidade padrão do `record.mjs`, até 2 tentativas, aceita `maxLate < 0.8` e 0 falho).
- Edição: `$TUT_HOME/t08/edit/` → `caps/specs.json`, `render_ilus_v3.sh`, `specs_ilus.py`, `montar_cap.py`,
  `auditar_camera.py`, `montar_t08.sh`, `fechar_t08.sh`, `entregar.py`. Copie e troque `t08`/`T08` pelos da sua aula.
- Leia antes: `SKILL.md` (seções 5 e 6), `docs/05-edicao.md`, `docs/07-conferencia.md`, `docs/08-licoes.md` (só o que for de
  edição e gravação final), `perfis/ecoflix/PERFIL.md` → "Gravação" e "Edição", e em `planejamento/ecoflix/PRODUCAO.md` as
  seções "19/11 · T08 piloto" e "19/11 (noite)". Da aula: `Tnn/andamento_160.md` (comandos, porta, sementes, `FAKE_NOW`).

## Fazer, nesta ordem
1. **Voz**: confira `tNN/narracao/proc_1.60.18.log` e `titulos_1.60.18.log` (palavra trocada de verdade? "fraca" costuma ser
   artefato do reconhecedor: ouça o trecho antes de concluir). Palavra errada de verdade: pare e relate (não gere voz).
2. **Robô com a voz real**: `python3 -I rec/tNN/gerar.py` lê os tempos reais; confira com `prever.py` os capítulos com gesto
   atrasado. Atraso que nasce dentro da frase: respiro DEPOIS do trecho denso com `pausas.py NN T:DUR` (T na linha do tempo
   ORIGINAL, num vão REAL de silêncio do `emendas/capNN.orig.json`; confira o código de saída, nunca `| tail`), e o
   `acelera` no specs encurta o silêncio na edição. Na T08 a voz real saiu ~8% mais rápida que a estimada.
3. **Gravação final**: script `rec/tNN/tNN_final.sh` no molde do da T08, tudo pela fila (`rec/fila.sh --prio NN`), um
   capítulo por vez, em segundo plano (prazo 7200000); olhe só no fim. Antes, `pgrep -af tNN_` vazio. Capítulo com
   `maxLate >= 0,8` ou passo falho: corrija e regrave só ele (no máximo 2 rodadas de regravação).
4. **PDF e comprovante na tela**: toda fala sobre PDF/comprovante mostra o papel real (cena `comprovante` do
   `ilustracoes.json`, molde `T08/cenas_v3/comprovante.html`; o PDF sai do `actions.json` da gravação final).
5. **Edição**: instale a área de edição sem ocupar disco à toa (`TUT_HOME=$TUT_HOME TUTORIAL=tNN PERFIL=ecoflix bash
   instalar.sh`; `models` já é link). `specs.json` com título e kicker de cada capítulo (do `tts_textos.py` → `TITULOS` e
   `KICKERS`), zooms e destaques só onde a fala aponta algo pequeno, `acelera` nos silêncios longos; ilustrações renderizadas
   com a voz real (`render_ilus_v3.sh`, `--larg 1422 --dsf 1.35`, `piscadas.py` em cada uma) e encaixadas por `specs_ilus.py`;
   `montar_cap.py`, `auditar_camera.py` (zoom brusco, recorte, alvo fora do quadro), render dos capítulos, `finish.py`,
   legendas (`legendas_aula.py`).
6. **Conferência** (`docs/07-conferencia.md`): folha de quadros da aula inteira, cada ilustração e cada zoom olhados;
   texto na tela sem travessão e sem dado real; título de capítulo certo; nada cortado; áudio sem estouro.
7. **Entrega**: `entregar.py` → aula final 1080p em `tNN/edit/out/Tnn/aula_final.mp4` + legendas, e uma prévia 720p de até
   28 MB em `$TUT_HOME/entrega_previa/EcoFlix Tnn - <título> 1.60.22 (previa 720p).mp4`.
8. **Disco** (sobra pouco: ~1,8 GB para tudo; na T02 chegou a zero no `finish.py`): `proj` e `video_sem_audio.mp4` em
   `/dev/shm/tNN_*` (link simbólico em `out/Tnn/`), `df -h /` antes de cada passo pesado e pare se ficar abaixo de 600 MB; no fim, apague `out/Tnn/proj`, `out/Tnn/video_sem_audio.mp4` e as pastas
   `out/capNN` (regeráveis), sempre com caminho absoluto literal. Fica: `aula_final.mp4`, legendas, `capitulos.json`, a prévia,
   as gravações finais em `rec/tNN/` e as ilustrações em `out/ilus/`.

## Limites
- Tudo na tela sai do app real 1.60.22 (o gravador já cala o aviso "Sistema atualizado" e o balão de dica do Cato
  em qualquer login: não precisa mexer no `VERSAO` do `gerar.py`); dados do mundo fictício; nenhuma credencial em arquivo (`TUT_SENHA` 8+ caracteres
  só no ambiente). Nunca gere nem peça voz nova (frase errada: relate com a frase exata; o coordenador corrige por frase).
- Não mexa em `perfis/`, `ferramentas/`, outras aulas, mundo base, `PRODUCAO.md`. Sem commit. Nada de `pkill`/`killall`,
  `git stash/reset/clean/checkout`; `rm` só com caminho absoluto literal. Derrube a sua instância no fim.
- Scripts e logs com o nome da aula (`rec/tNN/...`, `/dev/shm/tNN_...`), nunca `lote.sh` genérico no scratchpad: outro agente
  pode usar o mesmo caminho (20/11 a T01 apagou o lote da T12 assim).
- Economize contexto: acorde pouco (lotes em segundo plano, olhe tudo junto), não despeje log inteiro.

## Relatório final (até 200 palavras)
Duração da aula; capítulos regravados e por quê; respiros e acelerações; ilustrações encaixadas (e as pendentes); zooms e
destaques; achados do app para o MELHORIAS; caminho da prévia e da aula final; espaço livre no disco no fim.
