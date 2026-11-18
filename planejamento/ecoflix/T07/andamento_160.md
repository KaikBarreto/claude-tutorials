# T07 · andamento da aplicação do 1.60.10 (atualizado a cada etapa)

Numeração nova (20 capítulos, 00 a 19): novos **09** Dois pedidos ao mesmo tempo, **10** Rascunho, **12** Abater o vale;
antigos 09→11, 10→13, 11→14, 12→15, 13→16, 14→17, 15→18, 16→19. Sementes: apos-cap09→apos-cap11, apos-cap12→apos-cap15.

## Feito
- [x] `roteiro.md` e `narracao/tts_textos.py` (2.517 → ~3.550 palavras), `plano.md`, `inventario.md` (seção "1.60.10"), `cenas/ilustracoes.json`
  (renumerado + `ilu05_botao_cores` e `ilu10_rascunho`, "v3": "pendente").
- [x] `rec/t07/gerar.py` dos 20 capítulos (gera sem erro); `t07/inicio` sem o preço da bateria (vem do mundo base) e com o Depósito
  ligado à Tabela Depósitos; sementes renomeadas (apos-cap11, apos-cap15: ainda as de 11/11, regravar no ensaio).
- [x] Exploração da tela nova: `rec/t07/_ex/e160.json` → `o160.log` (seletores da barra, rascunhos, troca de fornecedor, excesso).

## Falta
- [ ] Ensaio rápido dos 20 capítulos, um por chamada: `TUT_SENHA=<8+> bash rec/t07/t07_ens.sh NN` (gera, ensaia pela fila, resume e
  grava a semente nos caps 03, 11, 15, 17 e 18). Olhar `rec/t07/_ens/t07-capNN.contact.jpg` e apagar MP4 e JPG depois.
- [ ] Completo (sem `--rapido`) onde a regra pede: 05, 09, 10, 11, 18 (lista aberta, aviso que some, tela que muda sozinha).
- [ ] Derrubar a instância no fim.

## Estado por capítulo (ensaio rápido no 1.60.10)
(preencher: NN ok | NN falha: motivo)

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
