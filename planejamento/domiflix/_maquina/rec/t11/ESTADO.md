# T11 · estado da gravação (porta 54329) · fase 1 em 04/11, app 1.38.19

Regras: `export TUT_HOME=/home/claude/domiflix FAKE_URL=http://127.0.0.1:54329` em TODO comando; backend com `FAKE_NOW=2026-11-10T10:00:00-03:00 FAKE_PORT=54329 rec/run.sh fake`
(o robô herda o mesmo `FAKE_NOW`); navegador só sob `flock $TUT_HOME/.heavy.lock nice -n 10`, uma trava por capítulo (`rec/t11/rodar2.sh NN [--ensaio] [--rapido] [--seed]`);
sem pkill; `rm` só com caminho absoluto; escrever só em `t11/edit/`, `rec/t11/`, `rec/fakebase/seeds-extra/t11/` e handlers novos; sem commit. Disco: parar abaixo de 3 GB
(ensaio rápido, sem vídeo: 1 GB).

## Peças
- `semear.py` -> `seeds-extra/t11/inicio.json` + `cadeia.json` (base do T5 como o T12 + G1 (`_patch` da trilha `is_onboarding: false`) + OS #16 concluída e OS #17 + padrões
  financeiros copiados do `t9/inicio` + catálogo da norma PMOC reconstruído das migrações (`catalogo.py`, 151 atividades) + tabelas vazias de propósito).
- `gerar.py` -> `cap00..cap14.json` (marcas `Ln`, `at` pelas palavras, `OBS` de avisos de erro/tela escura/faixa Domiflix, `confere ...` tela x fala).
- `colher.py NN` guarda o rascunho do assistente (`sessionStorage['form-draft:contract-form']`) que o capítulo 4 a 8 deixou; `setup_retomar` do gerar.py o devolve no capítulo seguinte.
- `rodar2.sh` (um capítulo), `lote2.sh "NN --rapido [--seed]" ...` (cadeia, colhe o rascunho depois dos capítulos 4 a 8), `resumo.py NN [--ens]`, `snap.mjs base|diff NN`, `explorar.mjs`.
- Handlers/hook novos (fakebase): `hooks/contracts.mjs`, `handlers/rpc/{ensure_pmoc_norm_templates,replace_contract_plan_activities}.mjs`,
  `handlers/functions/generate-pmoc-{trt,certificado,cronograma,dossie,planilha}-pdf.mjs` (+ `lib/pmocDocs.mjs`), `handlers/views/contract_health_status.mjs`.
