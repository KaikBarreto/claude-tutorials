# T21 · andamento no app 1.60.22

Estado (21/11 22:10): **etapas 1, 2 e 3 FEITAS.** `rec/t21/gerar.py` (18 capítulos + cortes `02b` e `15b`, 1600x900), `t21_corpo.sh`, `t21_lote.sh`,
`cenas/ilustracoes.json` (20 entradas, `v3: pendente`). Rápido e completo (voz estimada) com 0 falho e 0 "SEM ALVO" em todos; instância 54321 derrubada.
Falta só refazer as âncoras com a voz real (atrasos abaixo) e gravar.

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

### Falas com número que não bate com o mundo (ARRUMADAS na etapa 3: ver "Etapa 3 · feito")
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

## Etapa 3 · feito (21/11)
**Comandos** (de `/home/claude/ecoflix`, com `TUT_USER=rafael@reciclavalemetais.example` no ambiente; a senha é gerada no corpo e nunca vai a arquivo):
`bash rec/t21/t21_lote.sh 00:c 01:c ... > /dev/shm/t21_lote.log 2>&1` (item `NN:r` rápido, `NN:c` completo com os `at`, `02b`/`15b` os cortes do Marcos).
Cada item roda por `bash rec/fila.sh --prio 21 -- bash rec/t21/t21_corpo.sh NN M`: reinicia a instância 54321 (o overlay guarda estado em memória), grava SEMPRE em
`/dev/shm/t21_ens`, move só mp4, actions.json, telemetry.json e contact.jpg para `rec/t21/_ens/`, para abaixo de 450 MB livres. Derrubar:
`FAKE_MUNDO=/dev/shm/t21_mundo FAKE_PORT=54321 bash rec/run.sh down`.

**Ensaio rápido:** 0 falho em 00 a 17, 02b e 15b. **Completo (voz estimada), última rodada (`maxLate` em s):** 00 0,08; 01 1,38; 02 0,05; 03 2,78; 04 2,42; 05 1,34; 06 1,43; 07 0,50;
08 1,54; 09 1,70; 10 1,75; 11 1,25; 12 2,41; 13 3,75; 14 1,16; 15 2,78; 16 2,13; 17 0,28; 0 falho em todos. Os atrasos restantes vêm da espera da resposta/cartão
(o estimado fica 1 a 4 s antes do real) e ficam para as âncoras da voz real.

**Trocas de fala (tts_textos.py, roteiro.md e config_narracao.json juntos; `numeros` já estava certo):**
- cap04 L6: "sessenta e sete mil e seiscentos" -> "sessenta e dois mil e quinhentos" (resultado R$ 62.454,55); cap05 L4: "cento e trinta e dois mil" -> "cento e vinte e cinco mil" (R$ 125.313,67).
- cap03 L7: "Só quem tem acesso total escreve ali." -> "Como você tem acesso total, é você quem liga ou desliga essas notas." (o Rafael vê o interruptor, não a frase do Marcos).
- cap07 L7: "o comprovante abre aqui" -> "o botão Abrir comprovante fica aqui" (o botão abre um PDF em aba nova; o robô só aponta).
- cap09 L1: acrescentada "O cartão mostra a parcela de quatro mil, setecentos e noventa reais, com a forma e a data." (tempo do cartão) e L2 "Confirmar baixa" -> "Confirmar registro" (rótulo real; o cartão é "Registrar recebimento").
- cap10 L1: acrescentada "O Cáto pergunta se é cliente ou fornecedor, e eu respondo: fornecedor."; cap11 L1: acrescentada "O cartão mostra o nome e o telefone, eu confiro e salvo, e o cadastro entra na hora."
- cap12 L1: acrescentada "A foto aparece embaixo do campo, pronta pra enviar. Eu mando só a foto, sem escrever nada."
- Só `roteiro.md` (coluna Tela): cap01 "edição do Marcos" -> detalhe do Marcos (Permissões concedidas); cap03 frase da aba Da empresa; cap07/08 o cartão vira "Compra #N de Aparecida Ramos lançada" /
  "Venda #N para Serra Fina ... lançada"; "Próximos passos" abre ao clicar; cap09 "Registrar recebimento"/"Confirmar registro"; cap13 o botão "Preparar NF-e" já envia o pedido (não passa pelo campo); cap14 a compra da Aparecida aparece em "Para acompanhar".
- Fala final: 18 capítulos, 14.449 caracteres (2.703 palavras); títulos à parte.

**Frases sem tela / só aproximadas:** cap13 L11 (recusa da SEFAZ, só a fala, por desenho); cap07 L7 (Abrir comprovante só apontado, o PDF não é aberto); cap15 L1 "Pagamentos registram a operação..." sai depois da fala (a resposta
longa termina de digitar ~10 s depois); cap02/cap15 cortes do Marcos (`02b`, `15b`) em vídeo à parte. Ilustrações (20) sem tela por definição.

**Achados do robô para o MELHORIAS:**
- Bug de foco do app: depois de abrir o painel do Cato, um clique no campo "Pergunte ao Cato" pode devolver o foco a um botão "..." da tabela atrás (trava de foco velha), e a digitação abre o menu da linha. Aconteceu após visitar outra rota no setup (`aquecer`). O robô passou a travar o foco no campo (`window.__guarda`).
- Cliques reais do robô em "Conversas" e "Memória" (rodapé do painel) às vezes não abrem a janela; um `click()` por script abre. Idem o botão redondo (FAB) no primeiro carregamento.
- Com mensagens restauradas de sessão (hora à frente do relógio falso), a pesquisa de fim de conversa só aparece depois de 6 min no relógio do navegador (a conta usa a hora da mensagem).
- "Próximos passos" (cartão do pedido) nasce fechado; "Preparar NF-e" só aparece depois de abrir.
- O rótulo do FAB muda para "Abrir 1 notificação do Cato" quando há dica; seletores por "Abrir o Cato" falham nesse estado.

## 21/11 22:23 · reensaio da coordenação (depois das 3 frases)
- cap07: 0 falho, maxLate 0,50, PDF do comprovante capturado (`t21-cap07.actions.json`). cap13 (sem a frase da recusa da SEFAZ): 0 falho, 3,76 (resposta do Cato). cap15: 0 falho, 0,94. Instância 54321 derrubada. **T21 pronta para a voz** (14.446 + títulos); atrasos da resposta do Cato ficam para as âncoras da voz real.

## 25/11 · rotinas (resumos agendados) fora da aula
Decisão do Kaik: os resumos agendados do Cato ainda não estão liberados para os clientes, então saem da fala.
- `tts_textos.py`, `roteiro.md`, `plano.md` (o `config_narracao.json` não tinha nada de rotinas): cap04 L4 "...os pedidos e o atendente." (sem "as rotinas"); cap14 perde as duas frases das rotinas (Ver sinais agora e o agendamento das 8h) e fica com Acompanhar pedidos e Respostas revisadas (agora L1 e L2). Título do cap14: "Pedidos e revisões." (kicker "Pedidos"; vinheta PEDIDOS). Fica a menção a "rotina" só no cartão "Próximo: Dashboard, Agenda e rotina" (nome do T25).
- `gerar.py`: cap14 sem os passos de Suas rotinas/Ver sinais agora/Programar/Salvar agendamento; cap04 sem o hover em "Suas rotinas"; `NOMES` atualizado. `cenas/ilustracoes.json` não tinha entrada de rotinas (nada a tirar). Cópia de trabalho em `/home/claude/ecoflix/rec/t21/gerar.py` igualada.
- `preparar_aula.sh T21`: 18 capítulos estimados refeitos. Ensaio pela fila (lote em `/dev/shm`): cap04 rápido 0 falho, completo 0 falho (maxLate 2,34 s, espera da resposta); cap14 rápido 0 falho, completo 0 falho (maxLate 0,04 s). Instância 54321 derrubada.
- **Fala final: 14.181 caracteres (2.654 palavras), +383 de títulos.** Reabrir "Suas rotinas" na aula só quando os clientes tiverem o recurso.
- Obs.: o app (8080) estava parado; subi só ele (`rec/run.sh app`) e deixei no ar para a gravação da T04.

## 28/11 · ilustrações v3
Voz real 1.60.22 (`$TUT_HOME/t21/narracao`), 16:9, kit v3. **7 ilustrações** (de 21 entradas): `cenas_v3/cena.html` (6 cenas, escuro, menos a 1ª em claro) e `cenas_v3/comprovante.html` (papel real). `ilustracoes.json` com `v3` nas 7; as outras 14 saíram. Prévia: `/home/claude/ecoflix/previa_ilustracoes/T21_v3.mp4` (84,2 s, 10,5 MB) + `T21_v3.jpg`. Render: `cenas_v3/render_previa.sh`.
- **Feitas:** cap01 `ilu01_onde_fica` (claro: monitor e celular, botão à direita/esquerda, barra de baixo); cap02 `ilu02_caminho` (dados -> Cato -> serviços de IA, "não usa seus dados pra treinar"); cap06 `ilu06_saldo_movimentado` (janela de "A Fundição vem na frente" até "diferentes": valor movimentado x saldo em aberto); cap07 `ilu07_regra_cartao` ("sim" não confirma, o botão Lançar compra sim); cap07 `ilu07_comprovante_compra` (**papel real**, PDF do ensaio `_ens/t21-cap07.actions.json` ação 31, pedido #1759, rasterizado em `t21/edit/out/comprovantes/cap07-1.png`, marca-texto no pedido e no fornecedor); cap10 `ilu10_acerto_pagamento`; cap15 `ilu15_fica_nas_telas` (as quatro coisas que ficam nas telas).
- **Saíram (tela já mostra ou ideia repetida):** `ilu00_dois_balões` (a conversa real aparece); `ilu05_caixa_hoje` (a resposta e o pedido do mês aparecem na tela); `ilu06_regra_cartoes` (a tela mostra gráfico e tabela); `ilu07_dez_minutos` (aviso curto, sem o que mostrar); `ilu08_sem_estoque`; `ilu09_registra_banco` (a mesma ideia do `ilu10`, e o cap15 repete); `ilu11_cria_altera` e `ilu13_fora_do_cato` (juntas em `ilu15_fica_nas_telas`); `ilu12_arquivo_ordem` e `ilu12_formatos` (a tela mostra a foto e a resposta); `ilu13_danfe_previa` (o PDF da prévia é um stub de 1,3 KB do mundo falso, sem papel real de verdade: fica tirada, como as de MTR/CDF da T18); `ilu13_tres_tempos` (a tela mostra rascunho, envio e autorizada); `ilu15_mesma_chave` (o corte do Marcos mostra); `ilu15_limites_uso`.
- **Auditoria:** `auditar.cjs --aula ... --larg 1422` aprovado, 0 problemas nas 7 janelas. **Piscadas:** 6 janelas com 0; `ilu06_saldo_movimentado` com 5 (1 a 4 quadros, 0,5 a 0,9% da tela, sombra de vidro dos cartões/chips a ~38,5, 44,0, 45,0, 46,5 e 47,0 s do cap06); tirei os pulsos dos cartões e o resultado foi idêntico: causa não achada, fica para o fechamento (conferir no olho se incomoda ou re-renderizar).
- Limpeza: temporários em `/dev/shm/v3_t21/` apagados.
