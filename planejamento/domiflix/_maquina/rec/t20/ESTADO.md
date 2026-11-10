# T20 · estado (porta 54335) · fase 1, app 1.38.21

Regras: `export TUT_HOME=/home/claude/domiflix FAKE_URL=http://127.0.0.1:54335`; backend e robô com `FAKE_NOW=2026-11-10T10:00:00-03:00`
(`FAKE_PORT=54335 FAKE_NOW=... rec/run.sh fake`); navegador só sob `flock $TUT_HOME/.heavy.lock nice -n 10`, uma trava por capítulo
(`rec/t20/rodar.sh NN [--rapido] [--seed]`, lote `rec/t20/lote.sh 0 1 2 ...` NA ORDEM). Sem pkill; sem commit. Disco: parar abaixo de 3 GB.

## Mundo
- `semear.py` -> `seeds-extra/t20/inicio.json` (61 lançamentos de ago a out na Conta Principal + `_patch` do saldo inicial) e `cadeia.json`.
  Cadeia = a do T19 (`t3/apos-cap10 ... t13/apos-cap14, t19/inicio`) + SEMENTE FINAL DO T19 (`T19_FINAL`, hoje provisório `t19/apos-cap12`) + `t20/inicio`.
  Quando o T19 avisar a semente final: `T19_FINAL=t19/apos-capNN python3 -I rec/t20/semear.py`, depois `node rec/t20/snap.mjs base`.
- `_prov-t19.json` (seeds-extra/t20): só para EXPLORAR o app antes da semente do T19 (assinatura da Academia + cobrança do Restaurante). Fora da cadeia.
- Só o cap. 3 muda o banco (estrutura do DRE): `apos-cap03` -> caps 4..12. No fim, copiar `apos-cap03` para `apos-cap12` (o T14 parte dele).
## Handlers novos (rec/fakebase/handlers/rpc/)
- `cash_flow_opening_balances.mjs` (DFC previsto, "Saldo atual"); `get_company_dre_configuration.mjs` (modo legacy, sem visões).
## Robô
- `gerar.py` = `_head.py` + `_caps.py` (`cat _head.py _caps.py > gerar.py`). `confere*` lê a tela e compara com a fala; `OBS` vigia aviso de erro, tela escura e faixa da Domiflix.
- Descobertas: abas e regimes são role `tab`; DRE sem cartões/gráfico no alto; comparação não mostra coluna de variação; comparação fica na tela e bagunça a projeção
  (o cap. 6 usa "Remover comparações"); calendário abre sempre em nov/dez (mês de hoje); Dívida vazia no DFC.

## Fase 2 (05/11 20:4x em diante, Opus, app 1.38.24)
- Gravações finais: caps 00, 02, 07 a 12 de 19:01 a 20:08 (Sonnet); caps 01, 03, 04, 05 e 06 regravados 21:00 a 21:10 (`gravar_lote.sh 1 3 4 5 6`).
  Todos com 0 falho, `__avisos` vazio e `lateBy` <= 0,71 s. Cópia das gravações antigas dos 5 em `scratchpad/grav_antigas` (sessão Opus).
- Robô (em `_caps.py`): cap01 troca de mês do calendário por eval (`NAV_MES`); cap03 roda da janela antes do alvo, nomes por `colar`, respiro de
  2,6 s na voz (`t20/narracao/pausas.py 03 49.2:2.6`, original em `t20/narracao/emendas/cap03.orig.json`); cap04 e cap06 âncoras com `nth` corrigido
  (o W() casa por prefixo: "Competência," e "caixa," pegavam a 1ª frase; "Período" pegava "períodos."); cap06 "Aplicar comparação"/"Remover
  comparações" por `clicar_fixo` (rodapé fixo da janela); cap05 o clique em Despesas administrativas 3 s antes da L4 (sob a ilustração).
- Edição: `t20/edit/caps/specs.json` (cartões "Antes: Integração com Asaas, Assinaturas e Cobranças" e "Próximo: Notas Fiscais (NFS-e e NF-e)");
  ilustrações por código em `t20/edit/ilustracoes/` (cap05 três datas do cartão, cap11 roteiro de fechamento, cap12 resumo das três datas) ->
  `t20/edit/out/ilu_*.mp4|png`; `auditar_camera.py` 0 problema; render: `bash t20/edit/render_todos.sh 00 01 ...` (uma trava por capítulo).
- Finish: stems e `music.wav` em `/dev/shm/T20_stems` e `/dev/shm/T20_musica.wav` (links em `t20/edit/out/T20/proj/build`); apagar os dois em
  `/dev/shm` depois do finish. Parar antes do `entregar.py`.
- 05/11 22:2x FEITO até as legendas: `t20/edit/out/T20/aula_final.mp4` 584,6 s, -15,8 LUFS, pico real -3,6 dBTP depois do AAC (mix -3,5);
  153 legendas em `out/T20/legendas/aula_final.{srt,vtt}`; 12 vinhetas, 0 cortes; folhas de 3 s conferidas. O `mix.wav` ficou na RAM
  (`proj/build/mix.wav` -> `/dev/shm/T20_mix.wav`; some num reinício, o `remendar_aula.py` refaz). Fake 54335 desligado (religar com o
  `FAKE_NOW` acima se precisar regravar). Falta: `entregar.py`, hardlinks em `entrega_final/` e a limpeza pós-entrega.
