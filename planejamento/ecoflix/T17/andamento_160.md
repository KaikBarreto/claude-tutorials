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
