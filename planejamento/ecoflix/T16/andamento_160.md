# T16 · andamento da passada do app 1.60.10 (18/11)

## Feito
- `roteiro.md` e `narracao/tts_textos.py`: 25 capítulos (eram 19), 5.241 palavras (eram 2.867). Novos: 11 Impostos e as outras abas,
  13 Outras operações, 14 O que trava a emissão, 15 A SEFAZ recusou a nota, 17 Nota de devolução, 18 Nota complementar. Renumerados:
  11→12, 12→16, 13→19, 14→20, 15→21, 16→22, 17→23, 18→24. As edições estão em scripts (scratch do agente); a fonte é o `roteiro.md`.
- `plano.md` (tabela de capítulos e "Mundo novo do 1.60.10"), `inventario.md` (seção 15), `cenas/ilustracoes.json` (8 novas e 2
  alteradas com `"v3": "pendente"`; as outras só mudaram de `cap`/linha), `narracao/config_narracao.json` (números novos, IPI).
- Robô: `$TUT_HOME/rec/t16/gerar.py` (25 capítulos), `t16_lote160.sh` (lote de ensaios pela fila, captura a semente), sementes
  `seeds-extra/t16/` (`inicio` com a Metalúrgica Pinhal e o certificado `missing`; `rejeitada-1252`; `apos-capNN` da cadeia nova),
  `t16_sementes_160.py`. Handlers: `rpc/nfe_emissao_sem_rede.mjs` (novo) e `functions/plugnotas-upload-certificate.mjs` (grava
  `fiscal_certificate_status`).

## Ensaio (instância 54316, FAKE_NOW 2026-11-10T08:30:00-03:00)
```bash
cd /home/claude/ecoflix
FAKE_NOW=2026-11-10T08:30:00-03:00 FAKE_PORT=54316 bash rec/run.sh fake
bash rec/t16/t16_lote160.sh 0 1 2 ... 24            # rápido, em ordem (a cadeia de sementes depende da ordem)
bash rec/t16/t16_lote160.sh --completo 9 11 ...     # completo
cat rec/t16/_ens/_lote.txt                          # uma linha por capítulo: rc e passos falhos; resumo em t16-capNN.resumo.txt
```
Estado dos ensaios: ver o fim deste arquivo.
