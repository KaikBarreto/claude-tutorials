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
- Lote 2 (`--junto`, uma senha só): 2 a 24 no rápido + completos 15, 16, 20. Resultado: (pendente)
