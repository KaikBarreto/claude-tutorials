# 06 · Legendas (.srt e .vtt)

Legenda em **arquivo**: o player liga e desliga; nada queimado no vídeo, para não cobrir a tela do app.

- Fonte: as palavras com tempo de `narracao/capNN.json` (na grafia da legenda) e os títulos falados das vinhetas de
  capítulo (`narracao/titulos/titulos.json`).
- Regras (`legendas.py`): até 42 caracteres por linha e 2 linhas; cada frase vira uma ou mais legendas, divididas em
  partes equilibradas (de preferência depois de vírgula); legenda muito curta gruda na vizinha se couber; mínimo 1 s na
  tela, máximo 6,5 s; 0,25 s a mais no fim quando há espaço; nunca sobrepõe a seguinte.
- Números como aparecem na tela: configure em `config_narracao.json` → `numeros`
  (ex.: "dezoito mil BTUs" → "18.000 BTUs").
- Relógio: os tempos são arredondados para milissegundos **antes** de separar h/m/s (sem isso, 88,9999 s virava
  "00:01:28,000", um segundo adiantado).
- Por capítulo (prévia): `python3 -I legendas.py <saida> 02`.
- Aula inteira: `python3 -I legendas_aula.py out/<AULA>/capitulos.json out/<AULA>/proj/build/intro_v.mp4 <saida>`.
  Usa o início de cada capítulo no vídeo final (vinheta da aula + vinhetas de capítulo − cortes).
- Entregar com o **mesmo nome do vídeo** (`<Nome>.mp4` + `<Nome>.srt` + `<Nome>.vtt`): os players carregam sozinhos.
- Conferência: cobertura da fala ≥ 99% e início das legendas após pausa com mediana ~0 s em relação à voz
  ([07-conferencia.md](07-conferencia.md)).
