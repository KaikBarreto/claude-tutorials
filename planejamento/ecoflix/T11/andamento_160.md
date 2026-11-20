# T11 · andamento 1.60.18 (20/11)

## Feito
- `narracao/tts_textos.py` (19 capítulos, 3.087 palavras; antes 2.044), `config_narracao.json` (numeros novos), `roteiro.md`,
  `plano.md`, `inventario.md` (bloco 1.60.18 no topo), `cenas/ilustracoes.json` (cap renumerados; novas: ilu12_pdf comprovante,
  ilu15_conversao, ilu16_perda_padrao, todas `v3: pendente`), `propostas_fala.md`.
- Renumeração: 10 (editar ordem), 15 (Conversão), 16 (Perda padrão), 17 (Máquinas) são novos; antigos 10-13 viram 11-14; 14 vira 18.
- Tempos: `bash planejamento/ecoflix/preparar_aula.sh T11` (estimados, caps 00-18).
- Robô `rec/t11/gerar.py` (caps 0-18, sem avisos), sementes (`t11_sementes.py`, Capa de fio código 17), handlers T11
  (`add_production_entry_atomic.mjs` com `note`, `register_production_atomic.mjs` novo).
- Lote de ensaio lançado: `bash rec/t11/t11_lote160.sh` (resumo em `rec/t11/_ens/.lote160.txt`; logs `/dev/shm/t11/lote-NN.log`).

## Falta
- Ler o lote, corrigir o que falhou, 2º lote só dos que falharam: `bash rec/t11/t11_lote160.sh 03 06 ...`.
- Confirmar na tela e ajustar a fala: Conversão (16 kg de fio, R$ 28,80), perda padrão (37,5%, 24 kg), estoque do fio.
- `cenas/tempos/` e `cenas.html` ainda na numeração antiga. Derrubar a instância: `cd /home/claude/ecoflix && FAKE_PORT=54311 bash rec/run.sh down`.
