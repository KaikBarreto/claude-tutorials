# Andamento T15 · aplicação do 1.60.18

**Feito:** roteiro (17 capítulos) e `narracao/tts_textos.py` (3.392 palavras, sem travessão); `config_narracao.json` (trocas
DFC, EBITDA, CSV); `rec/t15/gerar.py` (16 capítulos do robô, todos geram sem aviso); sementes (`lote-categoria`) e 5 handlers
novos; `fake_now.json`; `cenas/ilustracoes.json` (11 entradas, 2 novas); `cenas/tempos`; `plano.md`, `inventario.md`.
**Falta:** resultado do ensaio em lote (rodando); conferir valores falados da DFC e do Pátio na tela; afinar o seletor da coluna
do gráfico (cap03, placeholder `.recharts-bar-rectangle >> nth=0`); salvar o PDF do cap15 e refinar `mostra` de `ilu15_historico_pdf`.

**Comandos**
- Lote: `cd /home/claude/ecoflix && export TUT_SENHA=... && nohup bash rec/t15/t15_lote.sh 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 > rec/t15/_ens/lote_geral.log 2>&1 &`
- Resultado: `ls rec/t15/_ens | grep lote_`; `tail rec/t15/_ens/lote_NN.txt prever_NN.txt`; fim: `lote_FIM.txt`.
- Derrubar a instância: `FAKE_PORT=54315 bash rec/run.sh down`.
- Regerar robô: `cd` scratchpad `t15x` e `python3 patch_gerar.py`; texto: `python3 edit_texto.py`.
**Pedido ao mundo base:** `bank_account_id/name` em `linhasDRE`.

**Estado ao parar:** o lote (capítulos 00 a 15, fila prio 15) foi lançado às 09:54 de 20/11 e estava no capítulo 00, atrás de
outras aulas na fila. A instância 54315 ficou LIGADA de propósito (o lote depende dela). Quando `lote_FIM.txt` existir:
analisar, corrigir e, só se preciso, um segundo lote; depois derrubar com `FAKE_PORT=54315 bash rec/run.sh down`.
