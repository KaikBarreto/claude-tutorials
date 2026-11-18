# T07 · andamento da aplicação do 1.60.10 (atualizado a cada etapa)

Numeração nova (20 capítulos, 00 a 19): novos **09** Dois pedidos ao mesmo tempo, **10** Rascunho, **12** Abater o vale;
antigos 09→11, 10→13, 11→14, 12→15, 13→16, 14→17, 15→18, 16→19. Sementes: apos-cap09→apos-cap11, apos-cap12→apos-cap15.

## Feito
- [x] `roteiro.md` e `narracao/tts_textos.py` (2.517 → ~3.550 palavras), `plano.md`, `inventario.md` (seção "1.60.10"), `cenas/ilustracoes.json`
  (renumerado + `ilu05_botao_cores` e `ilu10_rascunho`, "v3": "pendente").
- [x] `rec/t07/gerar.py` dos 20 capítulos (gera sem erro); `t07/inicio` sem o preço da bateria (vem do mundo base) e com o Depósito
  ligado à Tabela Depósitos; sementes renomeadas (apos-cap11, apos-cap15: ainda as de 11/11, regravar no ensaio).
- [x] Exploração da tela nova: `rec/t07/_ex/e160.json` → `o160.log` (seletores da barra, rascunhos, troca de fornecedor, excesso).

## Estado final (18/11, 3 lotes usados; instância 54307 derrubada)
- **Rápido aprovado (0 falho, folha olhada):** 00 01 02 03 04 05 06 07 09 10 11 12 13 14 15 16 17.
- **Completo com 0 falho:** 05 06 07 09 10 11 12 13 14 15 16 17. `lateBy` < 0,8 só no 14 (0,35); os outros saíram com 1,2 a 4 s
  (cap17: 13 s) com a máquina dividida (cliques de 2 a 5 s): reconferir na gravação final com a voz.
- **Não fechou (corrigido no `gerar.py` depois do 3º lote, sem rodar de novo):**
  - cap08: o `confere` do detalhe usava seletor inválido (agora lê o `main`); o resto do capítulo passou.
  - cap18: a queda e a volta da internet funcionam (compra salva local, pendência, sincronização); falhou só o `hover` no aviso
    "Operações sincronizadas com sucesso!", que some sozinho (agora `registra`, sem mouse). Sem 0 falho, a `apos-cap18` não foi gravada.
  - cap19: depende da semente `apos-cap18`.
- **Falta rodar** (sobe a instância, um por vez, nesta ordem; depois o completo de 08 e 18):
  `FAKE_NOW=2026-11-10T08:35:00-03:00 FAKE_PORT=54307 bash rec/run.sh fake`
  `TUT_SENHA=<8+> bash rec/t07/t07_lote160b.sh "08 18 19" "08 18"` ; `FAKE_PORT=54307 bash rec/run.sh down`
- Sementes: `apos-cap03`, `apos-cap11`, `apos-cap15`, `apos-cap17` regravadas no 1.60.10; falta `apos-cap18`.

## Comandos
```bash
cd /home/claude/ecoflix
bash /home/claude/claude-tutorials/planejamento/ecoflix/preparar_aula.sh T07
FAKE_NOW=2026-11-10T08:35:00-03:00 FAKE_PORT=54307 bash rec/run.sh fake
python3 -I rec/t07/gerar.py NN && python3 -I rec/t07/ensaio.py NN
FAKE_NOW=2026-11-10T08:35:00-03:00 FAKE_URL=http://127.0.0.1:54307 bash rec/fila.sh --prio 07 -- node rec/record.mjs rec/t07/_ens/capNN.json --rapido --preset ultrafast --crf 30
python3 -I rec/t07/resumo.py NN --ens ; python3 -I rec/t07/t07_semente.py NN   # semente só nos caps 03, 11, 15, 17, 18
FAKE_PORT=54307 bash rec/run.sh down
```
