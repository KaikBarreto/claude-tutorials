# T21 · andamento no app 1.60.22

Estado (21/11): **etapas 1 e 2 de 3 FEITAS** (fala e documentos; overlay, sementes e arquivos testados por chamada direta). Etapa 3
(`gerar.py`, lotes, ensaio, ilustrações) pendente. Nada foi gravado nem ensaiado; nenhuma instância no ar.

## Etapa 1 · feito
- `narracao/tts_textos.py`: 18 capítulos (00 a 17), 2.630 palavras, 14.065 caracteres de fala (+392 de títulos); `numeros` do
  `config_narracao.json` refeito (18 entradas). `roteiro.md` (tabela tela · fala, com o que o Cato responde), `plano.md` (capítulos, tabela
  "O que o Cato responde" com arquivo:linha, mundo, handlers, R1 a R8), `inventario.md` (seção "Revisão 1.60.22").
- `bash planejamento/ecoflix/preparar_aula.sh T21` rodado: 18 `capNN.json` estimados em `/home/claude/ecoflix/t21/narracao`.
- Cópias do que foi substituído: `/tmp/claude-0/-home-claude/5ab7153e-b0bb-5f91-8e7e-f0df5c647505/scratchpad/t21_*_antigo.*` (somem no reboot).

## Etapa 2 · FEITA (overlay em `/home/claude/ecoflix/rec/t21/overlay`, mundo montado por `python3 -I rec/t21/t21_mundo.py`)
- `lib/`: `cato_t21.mjs` (A1a a A19 + R1 a R8 com `CORRECOES` dos números, ver abaixo), `cato_confirma.mjs`, `cato_pedido.mjs`.
- Edges (`handlers/functions`): `cato-background`, `cato-assist` (`followups` só R1 a R8), `plugnotas-emit` (`preview_danfe` por `previewInvoiceId`
  ou `previewActionId` devolve PDF de 1.302 bytes; o resto vai ao handler base, nota nº 1249, "emitida" ao `plugnotas-status` após ≥ 3,5 s).
- RPCs (`handlers/rpc`): `cato_confirm_{purchase,sale,weighing_ticket,price,partner_balance,operation}_action`, `cato_order_journeys`,
  `cato_memory_manage` (todas as ações), `cato_routines_manage` (`status`, `preview`, `save`, `pause`, `resume`, `delete`; estado em memória do
  processo), `cato_corrections_manage`, `get_my_cato_conversations(_messages)`, `submit_cato_resolution_feedback`, `set_cato_feedback`. Faltando: nada.
- Sementes (`rec/mundo/seeds-extra/t21/`): `inicio` (agora também com `codigo_ibge` 3132305 na Serra Fina e CSTs de saída na configuração fiscal,
  sem os quais o Cato recusa a NF-e), `apos-cap02` (+ 1 conversa antiga do Rafael, para "Conversas" mostrar 1), **novo `apos-cap03`** (memória aceita e ligada,
  nota "Prefiro os valores em tabela, do maior para o menor."), **novo `apos-cap06`** (conversa dos caps. 4 a 6 com R1 a R8 gravadas em `cato_events`;
  2 contas a pagar: internet vencida 8/11 e aluguel do pátio 15/11, para "Ver sinais agora" mostrar vencida e a vencer).
  Cadeia: `...t15/apos-cap10, t21/inicio, t21/apos-cap02` (caps. 3), `+ t21/apos-cap03` (caps. 4 a 6), `+ t21/apos-cap06` (caps. 7 a 14; 15 em diante seguem o estado que o cap. 14 deixa).
- Arquivos (`rec/t21/arquivos/`, o `upload` do gravador resolve a partir de `rec/t21/`): `pesagem-cooperativa.jpg` (900x1200; motorista Jair Lopes, placa GHT7B19, os mesmos do cartão),
  `tabela-fundicao.png` (Alumínio latinha 6,50; perfil 9,20; Cobre mel 43,00; Cobre misto 37,00).
- Testado (chamada direta, instância na 54321, `FAKE_NOW` 10/11 08:30): A1 compra #1759 total 744; A2 venda #1760 total 5.200 e conta "Fatura venda #1760" 5.200 (vence 10/12);
  A3 ticket #58, líquido 1.420; A4 cobre mel 42,50→43,00 e misto 36,00→36,50; A5 baixa 4.790; A6 abre caixa #85 com 1.500 (saldo inicial é o valor dito, sem cofre);
  A7 saída 85 (esperado 1.415); A8 transferência 2.000 (Secundária 75.380→73.380; Principal 48.979,67→50.979,67); A9 esperado 1.415, contado 1.415, **diferença 0,00**;
  A10 Valdir "te deve" 300→200; A11 Quiririm 2.870→1.870; A12, A13 (Chumbo, código 16); A15a/b (ticket da foto, anexo no cartão); A16a/b; A17a/b → rascunho →
  `plugnotas-emit` (nº 1249) → `plugnotas-status` emitida; prévia em PDF antes e depois do rascunho; A18; A19 (Marcos); `cato_order_journeys` (venda com NF emitida, compra paga por transferência);
  conversas, memória (Rafael `accepted`, Marcos `pending` sem gerenciar), rotinas (preview dos 3 focos, save diário 08:00).

### Falas com número que não bate com o mundo (a fala NÃO foi mudada; arrumar na etapa 3 ou no ensaio)
- cap04, R1, resultado do mês: a fala diz "uns sessenta e sete mil e seiscentos"; o mundo dá **R$ 62.454,55** ("uns sessenta e dois mil e quatrocentos"). Despesas: R$ 37.384,20.
  (O texto-base de R1 tinha 30.249,20 de despesas e 69.589,55 de resultado; o overlay corrige para 37.384,20 e 62.454,55.)
- cap05, R4, saldo das contas: a fala diz "uns cento e trinta e dois mil"; o total é **R$ 125.313,67** ("cento e vinte e cinco mil"). Conta Secundária 75.380,00; saídas do mês 60.689,10.
- cap11/cap14: os cartões reais têm rótulos diferentes dos do roteiro (ex.: baixa = "Registrar recebimento"; caixa = "Saída do caixa"; saldo = "Receber saldo do parceiro"); o `roteiro.md` descreve, o código manda.
- cap14, "Outros pedidos (a compra da Aparecida)": na lista a compra cai em "Para acompanhar", não em "Outros pedidos".
- cap03, aba "Da empresa": a frase "Apenas usuários com acesso total podem publicar…" não aparece para o Rafael (ele é acesso total e pode gerenciar); só a veria o Marcos.

## Etapa 3 · lista exata
1. `gerar.py` em 1600×900: 18 capítulos pelo `roteiro.md`; `VERSAO` de `app/dist/.versao-app`; `__mostrarCato:'1'` no cap01 (balão de dica); PDF da prévia do
   DANFE (padrão `POPS` + `PDF_JS` do `rec/t08/gerar.py`); corte do Marcos nos caps. 2 e 15; avançar o relógio 3 min no cap. 16.
2. `t21_corpo.sh` e `t21_lote.sh` (molde T25): `--out /dev/shm/t21_ens`, prio 21, `df` >= 450 MB, só pela fila `rec/fila.sh`.
3. Ensaio em lote (rápido, MP4 `--preset ultrafast --crf 30`, `resumo.py --ens`, `prever.py`); no máximo 3 lotes.
4. `cenas/ilustracoes.json`: entradas novas com `cap`, `id`, `de`, `ate`, `resumo`, `mostra`, `"clima"` e `"v3": "pendente"` (as ilustrações do `roteiro.md`
   por capítulo; a do cap. 13 do PDF com `"tipo": "comprovante"`, `"cena": "pdf"`).
5. Setup dos capítulos: cada capítulo parte da semente da cadeia acima; as conversas dos caps. 4 a 6 e 7 a 14 são sessões do painel guardadas em
   `sessionStorage` (`cato-conversation-v3:<empresa>:<usuário>`): o setup de cap. 15 em diante restaura a conversa do cap. 14 ou aceita o painel vazio.
   O `upload` usa `arquivos/pesagem-cooperativa.jpg` e `arquivos/tabela-fundicao.png` (caminho relativo a `rec/t21/`).
6. Só depois do ensaio: conferir os valores calculados na fala (744, 5.200, 1.420, 300 → 200) com o que a tela mostrou.

## Parâmetros (da pesquisa anterior)

Porta 54321; FAKE_NOW `2026-11-10T08:30:00-03:00`; usuário `rafael@reciclavalemetais.example`; TUT_SENHA só no ambiente.
Subir: `cd /home/claude/ecoflix; python3 rec/t21/t21_mundo.py; FAKE_MUNDO=/dev/shm/t21_mundo FAKE_NOW=2026-11-10T08:30:00-03:00 FAKE_PORT=54321 bash rec/run.sh fake`
Derrubar: `FAKE_MUNDO=/dev/shm/t21_mundo FAKE_PORT=54321 bash rec/run.sh down`
Cadeia de sementes: t14/inicio + t14/apos-cap02,03,04,06,07,08,09,10,11,12,14 + t15/inicio, apos-cap01, apos-cap02, apos-cap10 + t21/inicio + t21/apos-cap02 (+ t21/apos-cap03 nos caps. 4 a 6; + t21/apos-cap06 nos caps. 7 a 14).

## Achados para o MELHORIAS
- "Ver itens e tributos" (CatoFiscalDetails) não é renderizado em lugar nenhum no 1.60.22 (componente órfão): não entra na fala.
- Prompts iniciais em /materiais: os dois últimos são sorteados (já conhecido).
- No mundo falso a NF-e só vira "emitida" com clique em "Consultar situação" ~4 s depois.
- Sem ficha técnica confirmada de "Fardo de alumínio" na cadeia: produção só via resposta de capacidade.
- A permissão de ver só os próprios pedidos/cadastros/tíquetes/contas deixa a pessoa sem o Cato (`config/routes.ts:343-364`); a descrição da permissão "Usar o Cato" avisa que ele responde sobre dados gerais mesmo de telas que a pessoa não abre (`:309`).
- Rótulo "Preparar NF-e" do botão de próximos passos manda o texto "Prepare a NF-e da venda #N. Use o pedido existente; não crie outro pedido." ao campo (`CatoOrderJourney.tsx:36`).
- Venda no saldo não tem forma fiscal mapeada: o Cato pergunta "Qual forma de pagamento deve constar na NF-e…" (`invoiceFiscalAdapter.ts:56-58`); vale conferir se isso é o desejado para o cliente que vende sempre no saldo.
- Os textos de R1 e R4 em `rec/mundo/lib/cato_respostas.json` têm números que não fecham com o mundo (despesas 30.249,20 e resultado 69.589,55; total 132.448,67): vale corrigir na fonte em vez de só no overlay (`CORRECOES`).
- O Cato real devolve `facts` com valores formatados na confirmação de operação (ex.: "R$ 4.790,00"); o `receipt` do mundo falso mostra o número cru ("4790"). Conferir na tela no ensaio e, se feio, ajustar no overlay.
- A forma de pagamento "Duplicata a prazo" da NF-e mostra o vencimento em ISO (2026-12-10) no cartão; vale conferir como a tela formata.
- Conta a pagar vencida/a vencer não existia no mundo base para o 10/11 (só uma parcela da prensa em 30/11): o "Ver sinais agora" ficaria sem contas; `apos-cap06` cria duas.
