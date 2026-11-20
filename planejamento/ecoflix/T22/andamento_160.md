# T22 · andamento da aplicação no 1.60.18 (20/11)

**Feito:** `tts_textos.py` (19 caps, 2.838 palavras), `roteiro.md` (gerado do tts + docstrings do robô), `plano.md` e `inventario.md`
(nota de atualização), `preparar_aula.sh T22`, `rec/t22/gerar.py` (18 caps com robô, monta sem erro de âncora), sementes
`t22/codigo-vencido` e `t22/venda-outra-unidade`, 8 handlers novos, `t22_estado.py` (`NOME_SEMENTE`), `cenas/ilustracoes.json`
(6 novas, 4 renumeradas, todas `v3: pendente`).

**Falta:** ensaio (lote 1 ainda por rodar/ler), trocar sondas `__LER__` (cap 8 Comparativo CMV, cap 11 saldo) por valores vistos,
conferir Lucro Líquido 18.336,70 e seletor de unidades (72.000 / 71.000), exportações (DRE Exportar, Exportar Relatório) sem filmar,
fala sem "PDF". Docstring do gerar.py ainda diz 1280x800.

**Comandos:** subir fake: `cd /home/claude/ecoflix && FAKE_NOW=2026-11-10T08:30:00-03:00 FAKE_PORT=54322 bash rec/run.sh fake`.
Conferir `pgrep -f t22_` vazio; lote (segundo plano, 7200000): `cd /home/claude/ecoflix && bash rec/t22/t22_lote.sh`
(lista em `rec/t22/_lote/lista.txt`; repetir = apagar `<id>.fim`). NÃO rodar `--estado` no cap 12 (preservar `apos-cap09`);
o cap 14 com `--estado` cria `apos-cap10`.
