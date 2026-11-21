# T21 · andamento no app 1.60.22 (INCOMPLETO)

Estado: a aula NÃO está pronta para a voz. Fala, roteiro, plano, inventário e `gerar.py` continuam os do 1.59/1.60.18
(9 capítulos, 1280x800). Nada foi gravado nem ensaiado nesta rodada. Instância 54321 derrubada.

## Feito
- Pesquisa no código 1.60.22 (`/dev/shm/ecoflix-src22/src`): rótulos dos cartões de ação, NF-e, memória, rotinas, histórico, pesquisa.
- `rec/t21/t21_mundo.py`: monta o mundo sobreposto `/dev/shm/t21_mundo` (rec/mundo por symlink; `handlers` e `schema.json`
  próprios, com as tabelas novas cato_attachments, cato_memory_items, cato_memory_state). Pastas vazias
  `rec/t21/overlay/handlers/{rpc,functions,views}` e `overlay/lib`.
- `/dev/shm/t21q.py` (consulta de estado; some no reboot).

## Falta (nesta ordem)
1. Fala nova (18 capítulos, ver cobertura_160.md seção 3) em `narracao/tts_textos.py` + `numeros` em `config_narracao.json`;
   regerar `roteiro.md`, `plano.md`, `inventario.md`; `bash planejamento/ecoflix/preparar_aula.sh T21`.
2. Overlay (hoje vazio): `lib/cato_t21.mjs` (respostas A-series), `cato-background`, `cato-assist`, `cato_jobs`,
   `cato_memory_manage` (personalDecision), `cato_routines_manage` (preview), `plugnotas-emit` com `preview_danfe`;
   RPCs novas `cato_confirm_{purchase,sale,weighing_ticket,price,partner_balance,operation}_action`,
   `cato_order_journeys`, `get_my_cato_conversations(_messages)`, `submit_cato_resolution_feedback`
   (confirmações chamam `criarPedido` de `rec/mundo/lib/eco.mjs`; propostas gravam `cato_pending_actions`).
3. Sementes `rec/mundo/seeds-extra/t21/{inicio,apos-capNN}` e arquivos fictícios (foto de pesagem, tabela).
4. `gerar.py` em 1600x900, `VERSAO` de `app/dist/.versao-app`, `__mostrarCato:'1'` no cap01; `t21_corpo.sh`/`t21_lote.sh`
   (molde T25, `--out /dev/shm/t21_ens`, prio 21, df >= 450 MB).
5. Ensaio em lote pela fila; `cenas/ilustracoes.json` (clima, v3 pendente).

## Parâmetros
Porta 54321; FAKE_NOW `2026-11-10T08:30:00-03:00`; usuário `rafael@reciclavalemetais.example`; TUT_SENHA só no ambiente.
Subir: `cd /home/claude/ecoflix; python3 rec/t21/t21_mundo.py; FAKE_MUNDO=/dev/shm/t21_mundo FAKE_NOW=2026-11-10T08:30:00-03:00 FAKE_PORT=54321 bash rec/run.sh fake`
Derrubar: `FAKE_MUNDO=/dev/shm/t21_mundo FAKE_PORT=54321 bash rec/run.sh down`
Cadeia de sementes: t14/inicio + t14/apos-cap02,03,04,06,07,08,09,10,11,12,14 + t15/inicio, apos-cap01, apos-cap02, apos-cap10 + t21/inicio + t21/apos-cap02.

## Achados para o MELHORIAS
- "Ver itens e tributos" (CatoFiscalDetails) não é renderizado em lugar nenhum no 1.60.22 (componente órfão): não entra na fala.
- Prompts iniciais em /materiais: os dois últimos são sorteados (já conhecido).
- No mundo falso a NF-e só vira "emitida" com clique em "Consultar situação" ~4 s depois.
- Sem ficha técnica confirmada de "Fardo de alumínio" na cadeia: produção só via resposta de capacidade.
