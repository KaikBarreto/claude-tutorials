# T12 · estado da gravação (agente G, porta 54327) · iniciado 31/10 20:40

Regras: `export TUT_HOME=/home/claude/domiflix`; navegador/gravação/render/fumaça só sob `flock $TUT_HOME/.heavy.lock nice -n 10`, UMA trava por capítulo;
sem pkill/killall; `rm` só com "${VAR:?}"; sem commit/push; escrever só em `t12/`, `rec/t12/`, `rec/fakebase/seeds-extra/t12/` e handlers/hooks novos.
FAKE_NOW = 2026-11-10T10:00:00-03:00 (backend 54327 E robô). Porta própria: 54327 (`FAKE_PORT=54327 FAKE_NOW=... rec/run.sh fake`; robô com FAKE_URL=http://127.0.0.1:54327).
Aceite: 0 falho, lateBy < 0,8 s, "1.38.9" no rodapé; auditar_camera 0; folha_zooms; entregar.py ok; .mp4/.srt/.vtt em entrega_final por `ln -f`;
limpeza guardando video_sem_audio.mp4 e proj/ (remendar_aula.py). Disco: parar abaixo de 3 GB e avisar.

## Feito
- 31/10 20:40 leitura de brief/roteiro/plano/inventário/PRODUCAO/lições; porta 54327 livre; app 8080 na 1.38.9 (dist index-CwmJPxKb.js).
- Titulos prontos (Tech Lead 20:3x): t12/narracao/titulos/cap01..11.wav + titulos.json. Palavras fracas = ASR (nada a refazer). Título do cap05 "ouvido" como "recode" (ASR do QR Code).
- Diff 1.38.6 -> 1.38.9 nos arquivos do inventário: só etiquetas (CustomerDetail, CustomerPortal, PmocPublicPortal, EquipmentDetail, CustomerFormDialog aba Contato)
  + migrations 20261031194500 (equipment_field_config.is_visible_in_portal) e 20261031195000 (get_portal_data devolve labels e filtra campos por is_visible_in_portal).
  i18n (customers/pmoc/os/dashboard) IGUAL. ContractDetail, PmocContractDocsTab, PortalCallsPanel, ServiceOrders, PortalCallsAlert, Dashboard: IGUAIS.

- 31/10 21:05 APP_ORIGIN pronta (rec/recorder/{env,app-origin,browser,runner}.mjs + cópia ferramentas/rec/recorder), testada (rec/t12/_teste_origem.log), documentada em docs/04-gravacao.md; main avisado.
- 31/10 21:05 backend: lib/portal.mjs + handlers get_portal_data, create_customer_portal_ticket, functions/pmoc-portal-share (testados por curl); fake 54327 reiniciado (pid em rec/.runtime/fake54327.pid).
- 31/10 21:05 sementes: rec/t12/semear.py -> seeds-extra/t12/{inicio,apos-cap03,apos-cap07,apos-cap08,apos-cap11}.json + rec/t12/cadeia.json
  (cadeia: t3/apos-cap10, t1/apos-cap13, t4/inicio, t4/apos-cap14, t5/inicio, t5/apos-cap05, t12/inicio; apos-capNN cumulativos sobre inicio).
  Sem parcelas do contrato (financial_transactions): a base não tem contas/categorias; fica para o T11/T13.

## Falta (ordem)
1. explorar (rec/t12/explorar.mjs): páginas de contrato, portais, Dashboard; seletores; paginação das OS do hotel (OS #10 "A caminho" cai na página 2).
2. gerar.py (rec/t12) -> cap00..11.json; gravar um capítulo por vez (APP_ORIGIN=https://www.dominex.app).
3. Edição, ilustrações (cap05 QR do T3; cap10 dois cartões), render, finish, legendas, entregar, ln -f, limpeza, lições, handoffs.

## 04/11 (retomada, app 1.38.19, porta 54327) · FASE 1 CONCLUÍDA
- Backend: schema 1.38.19 já na base; `rec/run.sh fake` com FAKE_NOW 2026-11-10T10:00 (a 54327 sobe de novo após reinício do contêiner).
  Correção no fake (`core/query.mjs`, resolveRelated): embed `alias:coluna_fk(...)` do PostgREST (contrato -> responsible_technicians) devolvia []
  e a aba Documentos acusava "Dados faltando" do RT. Vale para T11 também.
- Sementes: `semear.py` agora põe a trilha Domiflix com is_onboarding false (_patch no id da base) e lista as tabelas vazias de propósito
  (`/__dev/unknowns` fica vazio). Cadeia inalterada.
- Robô: `rec/t12/gerar.py` -> cap00..11.json (at pelas palavras, mark Ln, observador de avisos de erro/tela escura no setup e eval final);
  `rodar.sh NN --rapido`, `ensaios.sh`, `resumo.py`. Ensaio rápido: 12/12 sem passo falho, unknowns vazio, rodapé v1.38.19.
- Pendências para a fase 2: medir lateBy no ensaio completo (cap02 página 2 da lista; cap05 recarga do portal; cap09 rolagens);
  1º clique em "Ações" da ficha não abre o menu (2º clique condicional no roteiro); ilustrações cap05 (QR do T3) e cap10 (dois cartões).
