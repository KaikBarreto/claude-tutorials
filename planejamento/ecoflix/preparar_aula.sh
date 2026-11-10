#!/usr/bin/env bash
# Prepara a área de uma aula da EcoFlix para o robô e o ensaio, sem o instalar.sh inteiro (o disco tem pouco espaço: a
# pasta edit/ de cada aula, ~70 MB, só entra na edição).
#   bash planejamento/ecoflix/preparar_aula.sh T03 [T04 ...]        (TUT_HOME padrão: /home/claude/ecoflix)
# Cria $TUT_HOME/rec/tNN com o kit do robô (ensaio.py, prever.py, resumo.py, explorar.mjs) e $TUT_HOME/tNN/narracao com o
# tts_textos.py e o config_narracao.json da aula (atalhos para os arquivos do git: o que a junção e a revisão mudam vale na
# hora) e um capNN.json ESTIMADO por capítulo (tempos_estimados.py). Rode de novo depois de mudar a fala: os estimados são
# refeitos; o capNN.json da voz de verdade (sem "estimado") nunca é tocado.
set -euo pipefail
SKILL="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TUT_HOME="${TUT_HOME:-/home/claude/ecoflix}"
for A in "$@"; do
  N="${A#[Tt]}"; id="t$N"; P="$SKILL/planejamento/ecoflix/T$N"
  [ -f "$P/narracao/tts_textos.py" ] || { echo "sem $P/narracao/tts_textos.py"; exit 1; }
  mkdir -p "$TUT_HOME/rec/$id" "$TUT_HOME/$id/narracao"
  cp --update=none "$SKILL/ferramentas/rec/molde/"*.py "$SKILL/ferramentas/rec/molde/"*.mjs "$TUT_HOME/rec/$id/"
  for f in tts_textos.py config_narracao.json; do ln -sfn "$P/narracao/$f" "$TUT_HOME/$id/narracao/$f"; done
  n=0
  for c in $(python3 -c "import runpy,sys; print(' '.join(str(k) for k in sorted(runpy.run_path(sys.argv[1])['CAPS'])))" "$P/narracao/tts_textos.py"); do
    out="$TUT_HOME/$id/narracao/cap$(printf %02d "$c").json"
    if [ -f "$out" ] && ! python3 -c "import json,sys; sys.exit(0 if json.load(open(sys.argv[1])).get('estimado') else 1)" "$out"; then
      continue   # já é o da voz de verdade
    fi
    python3 "$SKILL/ferramentas/edit/cenas/tempos_estimados.py" "$out" --tts "$P/narracao/tts_textos.py" --cap "$c" >/dev/null
    n=$((n + 1))
  done
  echo "$id: $TUT_HOME/rec/$id e $TUT_HOME/$id/narracao prontos ($n capítulos estimados)"
done
