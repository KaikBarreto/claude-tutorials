# Andamento · T10 · aplicação no 1.60.18 (20/11/2026)

## Feito
- `roteiro.md`, `narracao/tts_textos.py` (15 capítulos, 2.470 palavras), `plano.md`, `inventario.md` e `cenas/ilustracoes.json` atualizados.
  Novos: cap07 "Achar uma movimentação", cap11 "Clientes, usuários e grupos". Renumeração: 7,8,9 -> 8,9,10; 10 -> 12; 11 -> 13; 12 -> 14.
- `preparar_aula.sh T10` rodado (cap00 a cap14 estimados). `cenas/tempos/` recebeu cópia dos estimados novos.
- Robô: `$TUT_HOME/rec/t10/gerar.py` reescrito (15 capítulos); lote de ensaio rápido em `rec/t10/t10_lote.sh`.

- Ensaio rápido dos 15 capítulos: 3 lotes feitos, todos 0 falhos e 0 DIFERENTE (cap05, cap06, cap11 da varredura corrigidos; view nova `rec/mundo/handlers/views/orders_with_payments.mjs`).
- PDFs na tela: `rec/t10/t10_pdfs.py --ens` tira Kardex (cap07), Posição e Relatório (cap13) para `rec/t10/pdfs/`; entradas `pdf07_kardex`, `pdf13_posicao`, `pdf13_relatorio` em `cenas/ilustracoes.json` (`tipo comprovante`, `cena pdf`, `v3 pendente`).

## Falta
- Cap11: o passo novo "confere a ordem do Resultado" (primeiro clique no cabeçalho ordena do maior para o menor, como a fala diz) entrou depois do lote 1 e não foi ensaiado: rodar `bash rec/t10/t10_lote.sh 11` e ler o `_ens/lote_11.txt`.
- Voz real: `bash planejamento/ecoflix/preparar_aula.sh T10` com a fala gerada; depois regravar completo (os tempos de hoje são estimados).
- Valores calculados citados só depois de vistos no ensaio (feito); rever se a voz mudar a fala.

## Comandos
- Instância: `cd /home/claude/ecoflix && FAKE_PORT=54310 bash rec/run.sh up` (derrubada ao fim: `... down`).
- Lote: `bash rec/t10/t10_lote.sh NN ...` (fila `--prio 10`, `FAKE_NOW=2026-11-10T08:30:00-03:00`).
