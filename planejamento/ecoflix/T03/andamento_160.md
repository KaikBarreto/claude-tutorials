# T03 · andamento da aplicação ao 1.60.18 (20/11, fechamento)

**Feito**
- Fala `narracao/tts_textos.py`: 17 capítulos, 3.694 palavras (era 3.600). Prefixo (F10) no cap03 (2 linhas novas) e seleção em massa (F11) no fim do cap15 (2 linhas novas). Roteiro, plano e inventário atualizados.
- Robô `rec/t03/gerar.py` (cap03: digita P, "Fica assim: P70", apaga antes de Atualizar; cap15: limpa a busca, marca Ferro pesado e Ferro misto, barra, X). Todos os capNN.json gerados.
- Lote 1 (fila prio 03): rápido 03, 15, 06; completos 06, 09, 08, 11, 13, 03. Todos sem falha e sem DIFERENTE. Atrasos máximos: 06 1,17 s; 08 0,94; 11 1,25; 13 1,67; 09 0,24; 03 0,11.
- Lote 2: cap15 rápido e completo passam (0 DIFERENTE); completo com atraso de 5,29 s na L6 (hover da barra e clique no X esperaram ~7 s o seletor).

**Falta**
- Correção do cap15 feita DEPOIS do último ensaio (limite de 2 lotes): hover pelo texto "Transferir Estoque" e X por `div.fixed button:has(svg.lucide-x)`. Sem ensaio.
- Comando (de /home/claude/ecoflix; `source rec/t03/t03_env.sh`, senha em /dev/shm/t03_senha): `T03_LOTE_MIN=40 bash rec/t03/t03_lote2.sh misto r15 c15` e olhar `rec/t03/.cap15.resumo` (atrasos).
- Instância 54303 (FAKE_MUNDO=rec/t03/_mundo): religar com `FAKE_MUNDO=/home/claude/ecoflix/rec/t03/_mundo FAKE_PORT=54303 bash rec/run.sh fake`.

## 21/11 · fechamento (gravação final 1.60.22, montagem e prévia)
- Aula final: `$TUT_HOME/t03/edit/out/T03/aula_final.mp4` (23 min 24 s, 1080p, -16,4 LUFS, pico -3,8 dBTP) + legendas; prévia em `$TUT_HOME/entrega_previa/`.
- Gravação: `rec/t03/t03_final.sh` (fila prio 03). Regravados: cap05 (2 rodadas: a opção "Radiadores" do Grupo fica abaixo da faixa do robô, `noScroll`; cadeia do filtro enxuta), cap06 (respiro maior), cap15 (barra de seleção em y ~845: `noScroll`; desmarca pelas caixinhas, o X da barra fica fora da tela a 1600 px).
- Respiros (`pausas.py`): cap05 26.32:1.3 · cap06 26.80:0.9 e 35.20:2.5 (este acelerado 2x na edição) · cap08 39.64:0.5 · cap09 38.98:1.0. Âncoras ajustadas no `gerar.py`: cap03 (Prefixo em "P,"), 08, 11, 12, 13.
- cap01: o corte do Marcos (cap01b) entra pela `t03/edit/t03_juntar_cap01.py` (originais em `rec/t03/t03-cap01a.*`).
- Edição: `t03_specs.py` (+ `caps/extra.json`), `specs_ilus.py`, `fechar_t03.sh`, `montar_t03.sh`. Aula de 23 min estoura o limite de memória no `music_bed.py`, no `mix.py` e no fim do `finish.py`: use `MIX_PY=$TUT_HOME/t03/edit/t03_mix.py bash montar_t03.sh` (cópias locais de pouca memória, mesmo som).
