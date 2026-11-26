# T14 · andamento (20/11)
Feito: roteiro, fala (19 caps), plano, inventário, ilustrações (json), robô 18 caps (cap18 é montagem), sementes (inicio, lote, cartão),
8 handlers novos, fake_now.json, ensaio rápido de todos os capítulos limpo (0 falhos, 0 DIFERENTE).
Falta: voz; ensaio completo (`bash rec/t14/t14_cap.sh NN`) dos capítulos com atraso previsto (ver propostas_fala.md); cenas v3.
Comandos: `FAKE_NOW=2026-11-10T08:30:00-03:00 FAKE_PORT=54314 bash rec/run.sh fake`; `bash rec/t14/t14_lote.sh 01+ 05+ ...`.

## 21/11 · ilustrações v3 prontas (para o fechamento)
- 6 cenas em `T14/cenas_v3/cena.html` (cap00, 04, 05, 07, 08, 12); 5 tiradas (a tela mostra). Auditoria 0, piscadas 0.
- cap01 L5 "O Extrato gera o movimento da conta em PDF ou em Excel, no período que você escolher.": a tela mostra o diálogo Exportar Extrato Bancário com Formato "PDF ou Excel" (a fala descreve a escolha, não abre o arquivo). No fechamento, conferir que o diálogo está na tela durante a frase.

## 26/11 · T14 fechada (app 1.60.22)
- Entregas: `$TUT_HOME/t14/edit/out/T14/aula_final.mp4` (+ `.srt`, `.vtt`), 21:19,2 (1279,2 s), 1920x1080, -16,3 LUFS, pico -3,8 dBTP. Prévia 720p (28,6 MiB) em `entrega_previa/`.
- maxLate por cap (gravação final): 00 0,22 | 01 0,58 | 02 0,72 | 03 0,39 | 04 0,08 | 05 1,06 | 06 0,72 | 07 0,10 | 08 0,47 | 09 0,42 | 10 0,48 | 11 0,44 | 12 0,09 | 13 0,32 | 14 0,46 | 15 0,57 | 16 0,23 | 17 0,50 | 18 montagem.
- Regravação: rodada 2 em 01, 03, 05, 06, 07, 09, 11, 12, 17; rodada 3 em 05, 06, 17. Âncoras do robô ajustadas em `rec/t14/gerar.py`; respiros em `t14/narracao/capNN.json` (pausas.py) nos caps 01, 03, 05, 06, 09, 11, 12, 17 (cap17 8,2 s e cap09 3,0 s os maiores); acelera em 05, 06, 09, 11, 12, 17 (`edit/caps/extra.json`).
- Pendente: cap05 ficou em 1,06 s (passos "Centro de custo" ~26,8 s, "Frota" 0,90 s e marca L5 ~39,5 s): lentidão do app sem silêncio real na voz.
- cap01 L5: o diálogo "Exportar Extrato Bancário" (PDF/Excel) está na tela durante a frase (conferido no vídeo final). Papel real: nenhum (o PDF abre em outra aba que o gravador não captura); nada desenhado.
- cap18: montagem de trechos reais (`rec/t14/t14_montagem_cap18.py`). 6 ilustrações v3, 0 piscadas. Auditoria de câmera 0.
- Memória: o mix e o finish precisaram de limitador em blocos (`limit_blocos` em t14_mix.py e finish.py) e `T14_PULA_MIX=1` (só para refazer o finish sobre um mix pronto).
