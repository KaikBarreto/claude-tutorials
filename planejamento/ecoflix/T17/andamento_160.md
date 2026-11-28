# Andamento · T17 no app 1.60.10 (para retomar)

Atualizado em 18/11. Instância 54317, prioridade 17. Leia `_BRIEF_APLICAR_160.md` e só depois isto.

## Feito
- `roteiro.md`, `narracao/tts_textos.py` e `config_narracao.json`: 20 capítulos (0 a 19), 3.197 palavras (eram 1.846). Novos: 6, 13,
  15. O antigo 8 virou 9 e 10; o antigo 10 virou 12, 14 e 16. `plano.md`, `inventario.md` (seção 11), `propostas_fala.md` e
  `cenas/ilustracoes.json` (3 novas, 3 alteradas, todas `"v3": "pendente"`) atualizados.
- Mundo: `rec/t17/t17_sementes.py` (inicio + laterais `mdfe2-rejeitado` e `nfse-recebidas`), `rec/t17/t17_semente_api.py` (cadeia
  `apos-cap02`, `04`, `05`, `08`, `09`, `10`, `13` sem navegador). Handlers novos: `functions/mdfe-contingency.mjs`,
  `rpc/get_invoice_dashboard_secure.mjs`, `rpc/get_nfse_dashboard.mjs`, `rpc/get_next_nfse_number.mjs`,
  `rpc/record_fiscal_inventory_entries.mjs`; `lib/estoque_fiscal.mjs` (devoluções e NF-e recebidas com lançamento fiscal).
- `rec/t17/gerar.py` reescrito do cap04 ao cap19 (o original do 1.59 está em `/dev/shm/t17_gerar_159.py`, some no reinício).
- `rec/t17/t17_lote.sh`: lote de ensaios em sequência pela fila; uma linha por capítulo em `rec/t17/_ens/<lote>.txt`, resumo e
  previsão em `rec/t17/_ens/capNN.resumo.txt` e `capNN.prever.txt`.

## Comandos
```bash
cd /home/claude/ecoflix
python3 -I rec/t17/t17_sementes.py                                  # inicio + laterais
TUT_SENHA=<8+ caracteres> python3 -I rec/t17/t17_semente_api.py      # cadeia de sementes sem navegador (não usa a fila)
python3 -I rec/t17/gerar.py                                         # capNN.json + fake_now.json
bash rec/t17/t17_lote.sh loteN 04 08 13                             # rápido dos capítulos dados (segundo plano, prazo 7200000)
bash rec/t17/t17_lote.sh loteN 04:c                                 # completo (sem --rapido)
FAKE_PORT=54317 bash rec/run.sh down                                # no fim
```

## Falta
(ver o fim deste arquivo: resultado dos lotes)

## 28/11 · 1.60.39

Etapa 1 (preparação, sem build, sem ensaio, sem voz). A T17 estava no 1.60.10 (roteiro) e no 1.60.18 (robô, com 5 capítulos falhando
na varredura de 20/11); foi levada direto ao 1.60.39 (`origin/main` de 26/11, `bab2eb1e8`). Repositório do app só lido por `git show`.
Backups do antes: `/tmp/claude-0/-home-claude/5ab7153e-b0bb-5f91-8e7e-f0df5c647505/scratchpad/T17_*` (somem no reinício).

**O que mudou no app para a T17:**
- Menu e telas (desde o 1.60.15): um item só, **"Relatório/Estoque Fiscal"** (`config/routes.ts`), com sete abas (`NotasFiscais.tsx`,
  `ESTOQUE_FISCAL_SUBTABS`): "Saldo atual", "Posição em uma data", "Movimentações", "Relatório de estoque", "Fiscal × operacional", "NF-e"
  (`/estoque-fiscal/relatorio-nfe`) e "NFS-e". O "Fiscal × operacional" (`EstoqueFiscalTab.tsx`) separa entradas e saídas (notas −
  pedidos): cartões "Entradas com diferença", "Saídas com diferença", "Materiais conferindo", "Alertas"; colunas "Compras (pedidos)",
  "Notas de entrada", "Diferença", "Vendas (pedidos)", "Notas de saída", "Diferença"; "sem nota" / "nota a mais"; quadro "Como ler a
  diferença (notas − pedidos)". Saíram "Materiais com divergência", "Mov. Fiscal", "Delta" e "Como ler o Delta".
- Novo MDF-e (`mdfe/NovoMdfeModal.tsx`, +801 linhas; `shared/fiscal/mdfeTransportOperation.ts`): na etapa "Veículo e motorista",
  "NATUREZA DA VIAGEM" ("Carga própria" padrão, "Transporte para terceiros", "CT-e globalizado"), "CATEGORIA DO TRANSPORTADOR" ("Próprio"
  padrão, ETC, TAC, CTC, com o proprietário do veículo), "COMPOSIÇÃO" e a seção sempre aberta "CIOT e contratação do frete": selo "Sem
  CIOT"/"CIOT obrigatório", "Esta viagem possui frete contratado?" (Não/Sim), "RNTRC do emitente / transportador"; com Sim: "CIOT *",
  "CPF/CNPJ do gerador do CIOT *", "Contratante — CPF/CNPJ *" e "Contratante — Nome *" (o contratante era opcional); com Não: "CIOT não se
  aplica a esta viagem". Seguro e pagamento do frete só em "Transporte para terceiros"/"CT-e globalizado". Revisão e contingência iguais.
- `MdfeTab.tsx`: "Histórico" no menu "Ações" (diálogo único `FiscalDocumentHistoryDialog`, RPC `list_fiscal_document_history`).
- NFS-e: bloco "IBS e CBS da NFS-e" ("Ativar IBS/CBS", desligado) no passo Serviço e na Configuração Fiscal › Impostos › NFS-e;
  "Baixar PDF" gera link novo no clique. Notas Recebidas: "Importar XML" e a escolha NF-e/NFS-e em cima da aba NF-e; a NFS-e importada
  entra em `inbound_nfse` com a configuração padrão (gatilho `stamp_inbound_nfse_fiscal_config`) e aparece na aba NFS-e (com o recurso
  ativo), com "Lançar despesa / conta".
- NF-e recebida → compra (1.60.39): a conferência mostra "Produtos", "Encargos/descontos", "Total da nota" e "Registrar também no estoque
  fiscal (não altera o saldo físico)"; "Conferir na tela de compra" abre a Compra com os itens; a compra carimba a nota ("Lançada como
  compra") e o menu passa a "Lançar compra de novo…" com o aviso "Lançar esta compra de novo?".
- `SettingsSidebarLayout.tsx`: a barra de abas virou `div role=navigation` com `aria-label="Navegação da seção"` (não `<nav>`).

**Avaliação pedida (Importar XML e NF-e que vira compra):** entra **um capítulo novo, o 11 "Da nota recebida à compra"** (vinheta
COMPRA), logo depois de "Da nota recebida à despesa": a nota 3871 da Cooperativa, importada pelo "Importar XML" na T16 cap23, vira
compra (totais, estoque fiscal, tela de Compra, Pix, selo). É o par natural de "serviço vira despesa" e o único horário da trilha com
o caixa #85 aberto (14:40, como na T06). O "Importar XML" de NFS-e só é citado (cap09 L5 e cap11 L2), sem importar outra nota: a lista
de NFS-e é a mesma do cap10. Fica de fora: o "Importar nota" pela chave (já citado na T16) e encargos na nota (ver achado 2 da T16).

**Aula: 21 capítulos (0 a 20), 3.197 → 3.526 palavras.** Novo: 11. Renumerados: 11→12 ... 19→20 (`roteiro.md`, `tts_textos.py`,
`cenas/ilustracoes.json`, `gerar.py`, sementes). Alterados: 00 (menu), 04 (L7 a L13 e o menu Ações), 06 (Tela), 08 (Tela), 09 (Tela da
faixa e L5), 12 (navegação, L1 e L8), 13 (L1), 17 (refeito para a tela nova), 20 (L2 e Tela). Nenhum capítulo tirado.
`roteiro.md` × `tts_textos.py`: 0 diferença linha a linha.

**Frases trocadas** (★ = muda informação de funcionamento; nenhuma fala de plano ou cobrança mudou):
| Cap/linha | Antes | Depois |
|---|---|---|
| ★ 00 L3 | ...em Transporte, em Notas de Serviço, no Estoque Fiscal e nos Relatórios Fiscais. | ...em Transporte, em Notas de Serviço e no Relatório e Estoque Fiscal. |
| ★ 04 L7 (nova) | (era "Continuar. No veículo, o caminhão truck...") | Continuar. Primeiro, a natureza da viagem: carga própria, porque a mercadoria é da Recicla Vale. E na categoria do transportador fica Próprio, porque o caminhão também é dela. |
| 04 L8 | (a antiga L7 sem "Continuar.") | No veículo, o caminhão truck, e no motorista, o Edson. Como a Frota está completa, não falta nenhum dado. |
| 04 L10 | Aqui embaixo fica o frete de terceiros. O CIOT é um código... | Embaixo fica o CIOT e a contratação do frete. O CIOT é um código... |
| ★ 04 L11 | Nesse caso, vão aqui o registro do transportador na ANTT, o código do CIOT, com doze dígitos, e o CPF ou CNPJ de quem gerou o código. Os dois últimos andam juntos: um não entra sem o outro. + E, se quiser, quem contratou o frete. | Nesse caso, a resposta aqui é Sim. Aí a tela pede o código do CIOT, com doze dígitos, o CPF ou CNPJ de quem gerou o código, quem contratou o frete e o registro do transportador na ANTT. |
| 04 L13 | ...sem cobrar frete. Então fica em branco. | ...sem cobrar frete. Então fica no Não, e a tela confirma: o CIOT não se aplica a esta viagem. |
| ★ 09 L5 | ...Se uma nota não aparecer, peça o PDF ao prestador e lance a despesa na mão. | ...Se uma nota não aparecer, peça o XML ao prestador: ela entra pelo Importar XML, que a gente vê daqui a pouco. |
| ★ 11 (novo, 9 linhas) | (não havia) | ver `roteiro.md`; as que afirmam funcionamento: L2 "Por ele entra também a nota de serviço de uma cidade que ainda não está no sistema nacional. Com o recurso ativo, ela vai pra aba de serviço e vira despesa como as outras."; L4 os totais; L6 "registrar também no estoque fiscal... o estoque do pátio fica por conta da compra"; L9 "o sistema avisa antes, pra mesma nota não entrar duas vezes no estoque". |
| ★ 12 L1 | ...Em Relatórios Fiscais, a primeira aba é a das notas de mercadoria. ... | ...No menu, em Relatório e Estoque Fiscal, fica a aba NF-e, das notas de mercadoria. ... |
| 12 L8 | A segunda aba é o mesmo relatório pras notas de serviço... | A aba do lado, NFS-e, é o mesmo relatório pras notas de serviço... |
| ★ 13 L1 | ...Ele abre no Saldo atual, com o saldo fiscal de cada material. | ...Ele fica na mesma tela, na primeira aba, Saldo atual, com o saldo fiscal de cada material. |
| ★ 17 (era 16) | Delta único: "Na última aba, o fiscal e o operacional ficam lado a lado..."; "quantos materiais deram diferença e quantos têm alerta"; "Repara no metal amarelo: mil e cem quilos de diferença."; "Seiscentos são de uma venda..."; "Os outros quinhentos vêm do caso mais comum..."; "Este quadro, Como ler o Delta..." | Por direção: "Agora, a aba que compara o fiscal com o operacional: as notas e os pedidos ficam lado a lado..."; "o sistema separa as entradas e as saídas: quantos materiais deram diferença nas compras, quantos nas vendas, quantos conferem e os alertas."; "Nas entradas, quinhentos quilos comprados e nenhuma nota: a tela marca sem nota."; "Nas saídas, seiscentos quilos de nota a mais. Foi uma venda pra Fundição..."; "Este quadro, Como ler a diferença..." (500, 1.100 e +600 do mundo base: **conferir na tela no ensaio antes da voz**) |
| 20 L2 | ...ativou as notas de serviço recebidas e lançou uma delas como despesa. | ...ativou as notas de serviço recebidas, lançou uma delas como despesa e levou a nota da cooperativa até a compra. |

**Robô (`$TUT_HOME/rec/t17/gerar.py`, cópia em `T17/rec/`):** funções e `Cap()` renumerados; `FAKE_NOW` até 20; `NAV =
"[aria-label='Navegação da seção']"`; cap00 um item no menu; cap04 natureza/categoria, "frete contratado?" Sim e volta a Não; cap09 espera a
faixa real; cap11 novo; cap12 entra pelo menu "Relatório/Estoque Fiscal" e clica na aba "NF-e"; cap13 clica na aba "Saldo atual";
cap17 refeito. `SEMENTE`/`LATERAL` novos (11 = `apos-cap10` + `compra-coop`). `t17_lote.sh` (00 a 20, semente do 14) e
`t17_semente_api.py` (`apos-cap14`). `capNN.json` e `fake_now.json` regerados com a voz estimada.
**Sementes:** `t17_sementes.py` rodado (a `inicio` ganhou a NF-e 3871 da Cooperativa, `origem` "manual", sem número; lateral nova
`compra-coop` com o caixa #85 aberto às 08:31, R$ 1.500,00); `apos-cap13.json` renomeado para `apos-cap14.json` (nas duas cópias).
**Mundo:** além dos handlers da T16 (`inbound-xml-import`, `list_fiscal_document_history`, `set_inbound_fiscal_entries`, `get_invoices_paged`,
`lib/eco.mjs`), `functions/plugnotas-nfse-dfe-sync.mjs` ganhou o ramo "sefin" da função real (responde "A consulta direta ao Ambiente
Nacional é automática. As novas NFS-e aparecerão após a próxima rodada do motor fiscal." sem trazer notas; antes trazia as duas na hora,
o que derrubava o cap09). Só a T17 usa essa edge. `config_narracao.json`: 4 números novos da legenda.

**Etapa 2 (depois que a T21 fechar: o build troca o `app/dist` e derruba a 8080).** Disco `/` ~2,1 GB (o dist tem 94 MB; o `dist.novo`
temporário mais 94 MB); `/dev/shm` ~6,3 GB livres.
```bash
cd /home/claude/ecoflix
cp -a app/dist /dev/shm/app-dist-1.60.22                       # o 1.60.22 para remendos das aulas já entregues
rm -rf /dev/shm/ecoflix-src39 && mkdir -p /dev/shm/ecoflix-src39
git -C /home/claude/ecosistema2-f3f6b533 archive bab2eb1e8 | tar -x -C /dev/shm/ecoflix-src39
(cd /dev/shm/ecoflix-src39 && npm_config_cache=/dev/shm/npm-cache-ecoflix nice -n 10 npm ci --no-audit --no-fund --ignore-scripts > /dev/shm/npm-ci-39.log 2>&1)
rm -rf /dev/shm/npm-cache-ecoflix
APP_SRC=/dev/shm/ecoflix-src39 APP_WORK=/dev/shm/ecoflix-src39 bash rec/setup-app.sh > rec/setup-app-39.log 2>&1
flock /home/claude/ecoflix/.heavy.lock env APP_WORK=/dev/shm/ecoflix-src39 BUILD_MEM_MB=4096 nice -n 10 bash rec/run.sh build
rm -rf /dev/shm/ecoflix-src39/dist && bash rec/run.sh app && cat app/dist/.versao-app   # 1.60.39
```
(se o `vite build` morrer por memória, como no 1.60.22, repetir só a linha do `flock`). Opcional, só se o ensaio pedir: schema do
1.60.39 (`node rec/fakebase/tools/gen-schema.mjs /dev/shm/ecoflix-src39/src/integrations/supabase/types.ts --out rec/mundo/schema.json`,
e copiar para `perfis/ecoflix/mundo/`): vale para todas as aulas.
- **Ensaio** (lote em segundo plano, pela fila): T16 instância 54316 (`FAKE_NOW=2026-11-10T08:30:00-03:00`): `bash rec/t16/t16_lote160.sh
  --junto 0 1 2 ... 24 --completo 04 15 20 23` (recaptura `apos-cap03` a `apos-cap23`). T17 instância 54317 (FAKE_NOW por capítulo, do
  `fake_now.json`): `bash rec/t17/t17_lote.sh lote39` (rápido 00 a 20, regrava a cadeia) e depois `bash rec/t17/t17_lote.sh lote39c 04:c
  11:c 17:c`. Conferir na tela: cap17 (500, 1.100 e +600), cap11 (total R$ 7.550,00, Pix, selo, sem "Atualizar os preços?"), cap09 (a
  faixa), cap04 (a pergunta do frete).
- **Voz** (ElevenLabs, ~1,01 crédito por caractere, conferido na T05 e na T25): T16 29.675 caracteres → **~30,0 mil créditos**; T17
  19.931 → **~20,1 mil**; total ~50 mil (o saldo renovou hoje: 676,5 mil). Só depois do ok do Kaik nas frases ★ das duas aulas.
- **Ilustrações v3:** T16 com a DANFE do Kaik (ilu20c e ilu24b) e as que já estavam pendentes; T17 sem cena nova (o cap11 é tela);
  ilu10_fiscal_operacional com o "nota a mais" e a nova janela (cap17 L5 "Foi" a L6 "diferente").
- **Fechamento:** gravação final com a voz real (`gerar.py` de novo com os `capNN.json` da voz), montagem, legendas, varreduras (tela
  parada e balão), entrega.

**Riscos:** (1) T17 sem ensaio desde o 1.60.18 e com 9 capítulos mexidos: contar com um 2º lote. (2) Números do cap17 vêm do mundo base
(conferir antes da voz). (3) DANFE de homologação ("SEM VALOR FISCAL", destinatário trocado pela homologação, modelo de 01/12). (4) O
seletor `nav[aria-label='Navegação da seção']` também está na T18, T19 e T25: quebra se forem regravadas no 1.60.39. (5) Remendos das
aulas já entregues precisam do dist 1.60.22 guardado. (6) A compra do cap11 não segue para os capítulos seguintes (eles partem da
`apos-cap10`/`apos-cap14`): o cap13 não mostra a latinha e o PET no estoque fiscal; nada na fala depende disso.
