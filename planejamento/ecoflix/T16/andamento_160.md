# T16 · andamento (app 1.60.22, tela 1600x900; passadas de 18/11, 19/11 e 20/11)

## Feito
- 18/11 (1.60.10): 25 capítulos (eram 19), sementes `seeds-extra/t16/`, `t16_lote160.sh`, handlers `rpc/nfe_emissao_sem_rede.mjs` e
  `functions/plugnotas-upload-certificate.mjs` (ver `cobertura_160.md` e `inventario.md` seção 15).
- 20/11 (1.60.18 e 1.60.22; handoff fiscal de 19/11; `inventario.md` seção 16): 14 linhas de fala trocadas e 1 tirada no `roteiro.md`
  e no `narracao/tts_textos.py` (5.261 → 5.264 palavras; os dois conferidos linha a linha):
  cap01 L2 "Relatório/Estoque Fiscal" (uma tela só); cap04 L2 a lupa do CNPJ (sem clicar) e L4 o endereço próprio do CNPJ padrão;
  cap06 L6 dica do número já usado (rejeição 539 → Rejeitada, 1.60.21); cap09 L3 sem anunciar Homologação ("Toda nota nova abre em
  Produção"); cap11 sem a linha da Pré-visualização (no 1.60.22 a aba só tem a DANFE real, que o backend falso não gera: proposta em
  `propostas_fala.md`); cap15 L9 "Reemitir NF-e"; cap16 L3 "Cancelamento enviado"; cap16 L9 sem o PDF da CC-e (não existe no motor
  próprio) e sem "vale sempre a última" (não está no código); cap17 L6 sem citar o DANFE (lê o aviso da tela); cap20 L3 Comprovante
  (Notinha) com o PDF, L4 DANFE só "pronto pra imprimir" (saíram "visual mais limpo" e "1º de dezembro"), L9 sem a aba Homologação;
  cap22 L3 sem o DANFE recebido (o falso não gera); cap24 L3 sem "a pré-visualização".
- Robô (`$TUT_HOME/rec/t16/gerar.py`, `VERSAO = '1.60.22'`): cap01 um item só no submenu; cap04 a lupa e as duas opções do Endereço
  Fiscal; cap06 a última nota na dica; cap11 sem a Pré-visualização (L11 = Emitir Nota); cap15 `emite_e_espera(..., botao='Reemitir
  NF-e')`; cap16 sem o "PDF"; cap17 zoom no aviso da coluna Item; cap20 `POPS` no setup, clique em "Comprovante (Notinha)" e `PDF_JS`
  depois dele e do "Download DANFE", sem a aba Homologação. `t16_pdf.py` (novo) grava os PDFs em `rec/t16/arquivos/` (o lote roda
  ele depois do cap20). `t16_lote160.sh`: `--completo` no meio da lista e trava de versão do build (`T16_VERSAO`).
- Handler novo (só da T16): `rec/mundo/handlers/rpc/get_invoice_for_print.mjs` (migration 20260925042000).
- `cenas/ilustracoes.json`: 3 entradas `"tipo": "comprovante"`, `"cena": "pdf"` (ilu20b Notinha, ilu20c DANFE, ilu24b DANFE no resumo).

## Ensaio (instância 54316, FAKE_NOW 2026-11-10T08:30:00-03:00)
```bash
cd /home/claude/ecoflix
FAKE_NOW=2026-11-10T08:30:00-03:00 FAKE_PORT=54316 bash rec/run.sh fake
bash rec/t16/t16_lote160.sh --junto 0 1 2 ... 24 --completo 15 16 20   # rápido em ordem (a cadeia de sementes depende da ordem), depois completos
cat rec/t16/_ens/_lote.txt rec/t16/_lote.txt                    # uma linha por capítulo; resumo em t16-capNN.resumo.txt
FAKE_PORT=54316 bash rec/run.sh down
```

## Estado dos ensaios
- Lote 1 (20/11, 1.60.22, uma senha da fila por capítulo): morreu nas 2 h com só cap00 e cap01 feitos (rápido, 0 falho); cada
  capítulo esperava ~50 min na fila.
- Lote 2 (`--junto`, uma senha só): **25 de 25 no rápido com 0 passo falho**, conferências tela × fala sem DIFERENTE, sementes
  `apos-cap03` a `apos-cap23` recapturadas no 1.60.22 (a cadeia 1252 → 1253 → 1254 fechou). Completos 15, 16 e 20: 0 falho; maxLate
  1,76 s (cap15, "#1252 Autorizada": espera da consulta de status de 5 s), 1,03 s (cap16, reabrir a Carta de Correção), 1,67 s
  (cap20, L9). Avisos na tela só os pedidos pelo roteiro (cap12 "Nenhum caixa...", cap14 NCM), mais o cap15 (NCM inválido no meio da
  digitação: agora o NCM é colado de uma vez). O PDF do Comprovante (Notinha) não veio ("SEM JANELA": a aba abre depois da RPC; o
  `PDF_JS` agora espera até 20 s). O DANFE veio: `rec/t16/arquivos/cap20-danfe-1250.pdf` (o fictício do backend falso).
- Lote 3 (`--junto`): rápido 15 e 20 com 0 falho (cap15 sem aviso; os dois PDFs do cap20 em `rec/t16/arquivos/`: o Comprovante
  (Notinha) real da 1250 e o DANFE fictício). Completos 05 09 11 12 13 14 15 17 18 20 22 24 (e 16 do lote 2): **0 passo falho em
  todos**, conferências sem DIFERENTE. Atraso acima de ~1 s, com a voz ESTIMADA e a máquina dividida: cap11 4,2 s ("Soma das
  parcelas", depois do calendário dos vencimentos), cap12 5,7 s (o caixa do Marcos, depois da troca de data), cap13 5,4 s (Incluir o
  papelão, trecho acelerado), cap14 3,3 s (os itens), cap20 1,9 s (L9), caps 15, 17 e 18 ~1,6 s (a autorização chega na consulta de
  status de 5 s), cap22 1,3 s, caps 05 e 24 1,2 s; 09 e 16 ~1,0 s.
- Só no rápido: 00 01 02 03 04 06 07 08 10 19 21 23.

## Falta
- Voz de verdade: depois do ElevenLabs, `python3 -I rec/t16/gerar.py` e completos dos capítulos acima de 1 s (11, 12, 13, 14 primeiro).
- Mundo base (pedido): `plugnotas-emit` falso atender `action: "preview_danfe_fiscal"` (a Pré-visualização do 1.60.21+ só tem a DANFE
  real; proposta de fala em `propostas_fala.md`) e um DANFE realista no `plugnotas-download` (o de hoje é um PDF de 5 linhas, no
  modelo de antes de 01/12). A IE da Fundição no mundo (6846208254) tem 10 dígitos e aparece no comprovante; SP usa 12.
- Ilustrações: as 3 entradas `comprovante` estão com `"v3": "pendente"` (a cena é do coordenador).
- Instância 54316 derrubada no fim de 20/11.
