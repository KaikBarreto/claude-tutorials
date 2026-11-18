# T07 · andamento da aplicação do 1.60.10 (atualizado a cada etapa)

Numeração nova (20 capítulos, 00 a 19): novos **09** Dois pedidos ao mesmo tempo, **10** Rascunho, **12** Abater o vale;
antigos 09→11, 10→13, 11→14, 12→15, 13→16, 14→17, 15→18, 16→19. Sementes: apos-cap09→apos-cap11, apos-cap12→apos-cap15.

## Feito
- [x] `roteiro.md` e `narracao/tts_textos.py` (2.517 → 3.541 palavras). Scripts usados (não rodar de novo): scratch `t07_texto.py`, `t07_roteiro.py`.

## Falta (ver o fim do arquivo para o estado de cada capítulo)
- [ ] `preparar_aula.sh T07`, `gerar.py` (20 capítulos), sementes, ensaio, `plano.md`, `inventario.md`, `cenas/ilustracoes.json`.

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
