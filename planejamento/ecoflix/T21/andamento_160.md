# T21 · andamento no app 1.60.22

Estado (21/11): **etapa 1 de 3 FEITA** (fala e documentos). Etapas 2 (overlay e sementes) e 3 (`gerar.py`, lotes, ensaio,
ilustrações) pendentes. Nada foi gravado nem ensaiado; nenhuma instância no ar.

## Etapa 1 · feito
- `narracao/tts_textos.py`: 18 capítulos (00 a 17), 2.630 palavras, 14.065 caracteres de fala (+392 de títulos); `numeros` do
  `config_narracao.json` refeito (18 entradas). `roteiro.md` (tabela tela · fala, com o que o Cato responde), `plano.md` (capítulos, tabela
  "O que o Cato responde" com arquivo:linha, mundo, handlers, R1 a R8), `inventario.md` (seção "Revisão 1.60.22").
- `bash planejamento/ecoflix/preparar_aula.sh T21` rodado: 18 `capNN.json` estimados em `/home/claude/ecoflix/t21/narracao`.
- Cópias do que foi substituído: `/tmp/claude-0/-home-claude/5ab7153e-b0bb-5f91-8e7e-f0df5c647505/scratchpad/t21_*_antigo.*` (somem no reboot).

## Etapa 2 · lista exata (overlay em `/home/claude/ecoflix/rec/t21/overlay`, mundo em `rec/t21/t21_mundo.py`)
1. `lib/cato_t21.mjs`: respostas R1 a R8 (as do `plano.md`; já existem em `rec/mundo/lib/cato_respostas.json`, R9 sai) e **A1a a A19** do
   `plano.md` → "O que o Cato responde" (texto pelo pedido exato do `roteiro.md`; as marcadas "(código)" são verbatim; `expira_em` = agora + 10 min).
   Respostas por usuário: A19 só para o Marcos (sem permissão de preço).
2. Edges: `cato-background` (jobId), `cato-assist` (`followups`), `plugnotas-emit` (rascunho → processando → autorizada ao "Consultar situação", ~4 s;
   nota nº 1249) com `preview_danfe` (PDF fictício).
3. RPCs: `cato_confirm_{purchase,sale,weighing_ticket,price,partner_balance,operation}_action` (gravam de verdade; compra e venda por `criarPedido`
   de `rec/mundo/lib/eco.mjs`; baixa, caixa, banco, transferência, cadastros e `invoices` em rascunho), `cato_order_journeys`, `cato_memory_manage`
   (`status`, `accept_personal_consent`, `list`, `save`, `set_enabled`), `cato_routines_manage` (`status`, `preview`, `save`),
   `cato_corrections_manage` (vazia), `get_my_cato_conversations(_messages)`, `submit_cato_resolution_feedback`, `set_cato_feedback`.
4. Sementes `rec/mundo/seeds-extra/t21/`: `inicio` (memória `pending`; sem a chave `cato_adoption_nudge_*`; Marcos sem editar material),
   `apos-cap02`, **novo `apos-cap06`** (conversa dos caps. 4 a 6 pronta; cap. 7 começa em "Nova"). Arquivos fictícios: `pesagem-cooperativa.jpg`
   (Cooperativa Recomeço, Plástico PET, bruto 1.480, tara 60) e `tabela-fundicao.png` (4 materiais do mundo).
5. Conferir no mundo: o que o `plano.md` → "A conferir no ensaio" lista (cofre no abrir caixa, A17a, saldo do Valdir, número do pedido).

## Etapa 3 · lista exata
1. `gerar.py` em 1600×900: 18 capítulos pelo `roteiro.md`; `VERSAO` de `app/dist/.versao-app`; `__mostrarCato:'1'` no cap01 (balão de dica); PDF da prévia do
   DANFE (padrão `POPS` + `PDF_JS` do `rec/t08/gerar.py`); corte do Marcos nos caps. 2 e 15; avançar o relógio 3 min no cap. 16.
2. `t21_corpo.sh` e `t21_lote.sh` (molde T25): `--out /dev/shm/t21_ens`, prio 21, `df` >= 450 MB, só pela fila `rec/fila.sh`.
3. Ensaio em lote (rápido, MP4 `--preset ultrafast --crf 30`, `resumo.py --ens`, `prever.py`); no máximo 3 lotes.
4. `cenas/ilustracoes.json`: entradas novas com `cap`, `id`, `de`, `ate`, `resumo`, `mostra`, `"clima"` e `"v3": "pendente"` (as ilustrações do `roteiro.md`
   por capítulo; a do cap. 13 do PDF com `"tipo": "comprovante"`, `"cena": "pdf"`).
5. Só depois do ensaio: conferir os valores calculados na fala (744, 5.200, 1.420, 300 → 200) com o que a tela mostrou.

## Parâmetros (da pesquisa anterior)

Porta 54321; FAKE_NOW `2026-11-10T08:30:00-03:00`; usuário `rafael@reciclavalemetais.example`; TUT_SENHA só no ambiente.
Subir: `cd /home/claude/ecoflix; python3 rec/t21/t21_mundo.py; FAKE_MUNDO=/dev/shm/t21_mundo FAKE_NOW=2026-11-10T08:30:00-03:00 FAKE_PORT=54321 bash rec/run.sh fake`
Derrubar: `FAKE_MUNDO=/dev/shm/t21_mundo FAKE_PORT=54321 bash rec/run.sh down`
Cadeia de sementes: t14/inicio + t14/apos-cap02,03,04,06,07,08,09,10,11,12,14 + t15/inicio, apos-cap01, apos-cap02, apos-cap10 + t21/inicio + t21/apos-cap02.

## Achados para o MELHORIAS
- "Ver itens e tributos" (CatoFiscalDetails) não é renderizado em lugar nenhum no 1.60.22 (componente órfão): não entra na fala.
- Prompts iniciais em /materiais: os dois últimos são sorteados (já conhecido).
- No mundo falso a NF-e só vira "emitida" com clique em "Consultar situação" ~4 s depois.
- Sem ficha técnica confirmada de "Fardo de alumínio" na cadeia: produção só via resposta de capacidade.
- A permissão de ver só os próprios pedidos/cadastros/tíquetes/contas deixa a pessoa sem o Cato (`config/routes.ts:343-364`); a descrição da permissão "Usar o Cato" avisa que ele responde sobre dados gerais mesmo de telas que a pessoa não abre (`:309`).
- Rótulo "Preparar NF-e" do botão de próximos passos manda o texto "Prepare a NF-e da venda #N. Use o pedido existente; não crie outro pedido." ao campo (`CatoOrderJourney.tsx:36`).
- Venda no saldo não tem forma fiscal mapeada: o Cato pergunta "Qual forma de pagamento deve constar na NF-e…" (`invoiceFiscalAdapter.ts:56-58`); vale conferir se isso é o desejado para o cliente que vende sempre no saldo.
