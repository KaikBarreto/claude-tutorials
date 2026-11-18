# Andamento · T08 no app 1.60.10 (atualizado em 18/11)

## Feito
- `roteiro.md`, `narracao/tts_textos.py` (1.243 → 2.114 palavras), `plano.md`, `inventario.md`, `propostas_fala.md` (achados),
  `cenas/ilustracoes.json` (4 entradas novas com `v3: pendente`; duas renumeradas).
- 14 capítulos: novos 07 (com valores), 11 (avulsa com cobrança), 12 (sem internet); antigos 07, 08, 09, 10 → 08, 09, 10, 13.
- `$TUT_HOME/rec/t08/gerar.py` (todos os capítulos; cala o balão do Cato), `t08_grava.sh` (religa sempre), `t08_pdf.py` (caps 09 e
  11), `t08_lote160.sh` (lote com as sementes da cadeia), `t08_ex2.py` (explorações e5 a e8).
- Mundo: `seeds-extra/t08/inicio.json` (+ #56 da cooperativa, + rascunho apagado); handlers `rpc/finalize_weighing_ticket_v4.mjs` e
  `rpc/apply_standalone_weighing_charge_v1.mjs`; `schema.json` e `defaults.json` com as colunas `weighing_tickets.standalone_*`.
- Sementes da cadeia: `apos-cap02` a `apos-cap06` (as de antes); `apos-cap07`, `apos-cap08`, `apos-cap10`, `apos-cap11` saem do
  ensaio (o lote grava com `t08_semente.py`). As antigas `apos-cap07` e `apos-cap09` (numeração velha) foram apagadas.

## Ensaio
Resultado de cada lote em `$TUT_HOME/rec/t08/lote160.txt`; folhas de contato em `rec/t08/_folhas/`; resumos em `rec/t08/_ens/capNN.resumo`.
(ver o fim deste arquivo para o estado de cada capítulo)

## Comandos
```bash
cd /home/claude/ecoflix
bash /home/claude/claude-tutorials/planejamento/ecoflix/preparar_aula.sh T08   # tempos estimados
python3 -I rec/t08/gerar.py                                                    # cap00..cap13.json
bash rec/t08/t08_lote160.sh 07 08 09 10 11 12 13     # rápido de cada um, em ordem (a cadeia 07 → 08 → 10 → 11 grava as sementes)
bash rec/t08/t08_lote160.sh 08:--os-dois             # rápido + completa de um capítulo
FAKE_PORT=54308 bash rec/run.sh down                 # derrubar a instância no fim
```
Um capítulo da cadeia só roda depois do anterior ter gravado a semente (07 → 08 → 09 e 10 → 11 → 12 e 13).

## Estado em 18/11 19:55 (três lotes usados; instância 54308 derrubada)
| Cap. | Rápido (MP4 + folha olhada) | Completa |
|---|---|---|
| 00 a 06 | aprovado (0 falho, sem aviso de erro na tela) | não pedida (06: o respiro de ~3 s da L2/L3 continua valendo) |
| 07 | aprovado; semente `apos-cap07` gravada | **falta**: duas completas saíram com atraso (0,81 s no "Fechar"; depois 1,80 s na marca L6). O `gerar.py` já foi ajustado (Salvar na L6, "Fechar" na palavra "valor"); não foi rodado de novo |
| 08 | aprovado; semente `apos-cap08` gravada | aprovada (maxLate 0,72 s) |
| 09 | aprovado (liga, mostra e desliga as assinaturas; PDF novo em `rec/t08/arquivos/cap09-comprovante-termico.pdf`) | não rodada |
| 10 | **não fechou**: 4 `hover` do painel "Filtros" não acharam o alvo (opção "Cancelado" e os botões "Tipo", "Status", "Usuário" na 2ª abertura); o resto passou (finalizar, "Ver pedido", Exportar, #59). Seletores trocados no `gerar.py` (`FILTRO(...)`, `[role=dialog]`), sem novo ensaio |
| 11, 12, 13 | **não rodaram** (dependem das sementes `apos-cap10` e `apos-cap11`). Os fluxos do 11 e do 12 foram feitos passo a passo nas explorações `_ex/e7` e `_ex/e8` (telas e números conferidos), mas o roteiro do robô deles nunca rodou |

Para fechar (um lote só, nesta ordem):
```bash
cd /home/claude/ecoflix && bash rec/t08/t08_lote160.sh 10:--os-dois 11:--os-dois 12 13 07: 09:
grep -n '!!ERRO\|DIFERENTE:\|SEM ALVO' rec/t08/_ens/cap1[0-3].resumo rec/t08/cap*.resumo; tail -8 rec/t08/lote160.txt
FAKE_PORT=54308 bash rec/run.sh down
```
