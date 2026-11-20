# T02 · andamento da aplicação no 1.60.18 (20/11)

**Feito:** `roteiro.md` e `narracao/tts_textos.py` (14 capítulos, 1.483 → 2.313 palavras; troca de pronúncia nova "SPED" em
`config_narracao.json`); `plano.md`, `inventario.md` (seção 8) e `cenas/ilustracoes.json` (renumerado, `v3: pendente`, entradas novas
cap 6, 7 e 12 com `tipo comprovante` no 12); `preparar_aula.sh T02` rodado; robô `rec/t02/gerar.py` (14 capítulos);
sementes `rec/mundo/seeds-extra/t02/` (`t02_sementes.py`); handlers novos `create-company-user` (editado, só T02),
`rpc/set_user_scale_weight_policy.mjs` e `rpc/save_user_permissions_and_bank_accounts.mjs`.
**Mapa de capítulos:** 0 a 5 como antes (1, 2, 3, 4, 5 editados); 6 Restrições e 7 Mapa (novos); 8 a 11 = antigos 6 a 9; 12 Relatório
(novo); 13 = antigo 10 (recap).
**Falhas da varredura (caps 3, 4, 5):** `Operador Padrão` ganhou o selo "Recomendado" (nome acessível "Operador Padrão Recomendado": alvo sem
`exact`, `CHIP_OP`); sem perfil a lista fica apagada (cap 4 clica em "Personalizado" antes); o "Personalizado" virou botão âmbar
(`button.bg-amber-500`, não mais `span`).

## Comandos
```bash
cd /home/claude/ecoflix
FAKE_NOW=2026-11-10T08:30:00-03:00 FAKE_PORT=54302 bash rec/run.sh fake          # a instância (se caiu)
export TUT_USER=rafael@reciclavalemetais.example TUT_SENHA=<8+ caracteres>
python3 -I rec/t02/gerar.py                                                       # reescreve rec/t02/cap00..13.json
bash rec/t02/t02_lote.sh 03 04 05      # ensaio rápido em lote pela fila (--prio 02); resultado em /dev/shm/t02rec/lote.txt
bash rec/t02/t02_rodar.sh 05           # completo de um capítulo (sem --ens)
FAKE_PORT=54302 bash rec/run.sh down   # no fim
```
## Falta / pendências
Ver o fim deste arquivo (preenchido ao fim do ensaio).
