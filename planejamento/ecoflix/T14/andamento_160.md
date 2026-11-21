# T14 · andamento (20/11)
Feito: roteiro, fala (19 caps), plano, inventário, ilustrações (json), robô 18 caps (cap18 é montagem), sementes (inicio, lote, cartão),
8 handlers novos, fake_now.json, ensaio rápido de todos os capítulos limpo (0 falhos, 0 DIFERENTE).
Falta: voz; ensaio completo (`bash rec/t14/t14_cap.sh NN`) dos capítulos com atraso previsto (ver propostas_fala.md); cenas v3.
Comandos: `FAKE_NOW=2026-11-10T08:30:00-03:00 FAKE_PORT=54314 bash rec/run.sh fake`; `bash rec/t14/t14_lote.sh 01+ 05+ ...`.

## 21/11 · ilustrações v3 prontas (para o fechamento)
- 6 cenas em `T14/cenas_v3/cena.html` (cap00, 04, 05, 07, 08, 12); 5 tiradas (a tela mostra). Auditoria 0, piscadas 0.
- cap01 L5 "O Extrato gera o movimento da conta em PDF ou em Excel, no período que você escolher.": a tela mostra o diálogo Exportar Extrato Bancário com Formato "PDF ou Excel" (a fala descreve a escolha, não abre o arquivo). No fechamento, conferir que o diálogo está na tela durante a frase.
