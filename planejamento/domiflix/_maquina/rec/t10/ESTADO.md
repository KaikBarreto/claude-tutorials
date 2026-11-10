# T10 · estado da preparação (porta 54328, app 1.38.19)

Regras: `export TUT_HOME=/home/claude/domiflix FAKE_URL=http://127.0.0.1:54328` em TODO comando; backend com `FAKE_NOW=2026-11-03T09:00:00-03:00 FAKE_PORT=54328 rec/run.sh fake`;
navegador só sob `flock $TUT_HOME/.heavy.lock nice -n 10`, uma trava por capítulo (`rec/t10/rodar.sh NN [--rapido] [--seed]`, lote `rec/t10/lote.sh 0 1 2 ...` NA ORDEM).

## Quando a voz chegar
1. `t10/narracao/capNN.json` no lugar (o `gerar.py` usa o real; sem ele usa tempos PROVISÓRIOS estimados de `tts_textos.py`).
2. `python3 -I rec/t10/gerar.py` (ANCHORS=1 mostra as palavras-âncora) e `node rec/record.mjs rec/t10/capNN.json --check`.
3. Ensaio completo (sem --rapido) por capítulo para medir `lateBy`; depois gravar.

## Mundo
`semear.py` -> `seeds-extra/t10/inicio.json` + `cadeia.json` (t2/apos-cap10 para a Tatiane + cadeia do T9 + t9/apos-cap16 + CRM vazio + G1 `_patch` is_onboarding false).
Sementes entre capítulos: `rodar.sh NN --rapido --seed` grava `apos-capNN` (`snap.mjs`); o `apos-cap03` ganha hotel, Marcos e Luana por `corte.py` (automático no rodar.sh do cap. 3).
Backend novo (hooks `crm_pipelines`, `crm_stages`, `leads`, `lead_assignees`, `crm_webhooks`, `projects`; RPC `project_progress_summary`; function `crm-lead-webhook`) testado por REST.
