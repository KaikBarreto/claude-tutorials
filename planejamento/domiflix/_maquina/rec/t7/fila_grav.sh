#!/usr/bin/env bash
# T7 · fila do agente A: roda os itens UM A UM; cada item pede a trava sozinho (um flock por capítulo, regra do coordenador),
# assim as outras trilhas entram entre dois itens.
# uso: rec/t7/fila_grav.sh "01" "render:01" "00" "02 --seed" "03 --seed" ...
#   "NN [opções]"  -> rodar.sh NN [opções]  (gera o roteiro, grava sob a trava, resume; opções: --rapido --seed --ensaio)
#   "render:NN"    -> edição + render do capítulo NN: specs.py, montar_cap.py, auditar_camera.py, render_chapter.py (pede a trava
#                     sozinho), confere_render.py e a prévia leve com narração (previa.sh, sob a trava). Só roda se a gravação
#                     de NN fechou com 0 passos falhos.
# Para na 1ª falha de capítulo com --seed (os seguintes partem do estado dele); sem --seed, segue e avisa.
# Não editar este arquivo enquanto a fila roda (o bash lê o script aos poucos): copiar para outro nome e lançar de novo.
set -uo pipefail
cd /home/claude/domiflix
export TUT_HOME=/home/claude/domiflix
EDIT=t7/edit
declare -A FALHOS_DE

render_cap() {
  local NN="$1" rc
  if [ "${FALHOS_DE[$NN]:-x}" != "0" ]; then echo "--- render:$NN pulado (gravação sem 0 falhos nesta fila)"; return 0; fi
  echo "--- [$(date +%H:%M:%S)] edição do cap$NN (specs, montar_cap, auditoria da câmera)"
  python3 -I rec/t7/specs.py > "$EDIT/out/specs.log" 2>&1 || { echo "!!! specs.py falhou"; tail -5 "$EDIT/out/specs.log"; return 1; }
  python3 -I "$EDIT/montar_cap.py" "$NN" > "$EDIT/out/montar_$NN.log" 2>&1 || { echo "!!! montar_cap falhou"; tail -8 "$EDIT/out/montar_$NN.log"; return 1; }
  tail -3 "$EDIT/out/montar_$NN.log"
  python3 -I "$EDIT/auditar_camera.py" "$EDIT/caps/cap$NN.chapter.json" > "$EDIT/out/audit_$NN.log" 2>&1
  tail -8 "$EDIT/out/audit_$NN.log"
  echo "--- [$(date +%H:%M:%S)] renderizando cap$NN (pede a trava sozinho)"
  python3 -I "$EDIT/render_chapter.py" "$EDIT/caps/cap$NN.chapter.json" > "$EDIT/out/render_$NN.log" 2>&1
  rc=$?
  tail -c 400 "$EDIT/out/render_$NN.log" | tr '\r' '\n' | tail -4
  [ "$rc" -eq 0 ] || { echo "!!! render do cap$NN falhou (rc=$rc), veja $EDIT/out/render_$NN.log"; return 1; }
  python3 -I "$EDIT/confere_render.py" "cap$NN"
  echo "--- [$(date +%H:%M:%S)] prévia leve do cap$NN (sob a trava)"
  local DUR; DUR=$(python3 -I -c "import json;print(int(json.load(open('$EDIT/out/cap$NN/cap$NN.edit.json'))['dur']))")
  local TS; TS=$(python3 -I -c "d=$DUR;print(' '.join(str(max(1,int(d*k/9))) for k in range(1,9)))")
  flock "$TUT_HOME/.heavy.lock" nice -n 10 bash "$EDIT/previa.sh" "cap$NN" "$TS" 2>&1 | tail -4
  echo "--- [$(date +%H:%M:%S)] cap$NN renderizado: $EDIT/out/cap$NN/"
}

for ARGS in "$@"; do
  case "$ARGS" in
    render:*) render_cap "$(printf '%02d' "$((10#${ARGS#render:}))")" || echo "!!! $ARGS terminou com erro"; continue ;;
  esac
  NN=$(printf '%02d' "$((10#${ARGS%% *}))")
  echo "=== [$(date +%H:%M:%S)] cap$NN: rodar.sh $ARGS"
  # shellcheck disable=SC2086
  bash rec/t7/rodar.sh $ARGS > "rec/t7/.fila-$NN.out" 2>&1
  RES=$(grep -m1 -E "^cap$NN: .* falhos" "rec/t7/.fila-$NN.out" || true)
  echo "$RES"
  grep -m1 "pageErrors" "rec/t7/.fila-$NN.out" || true
  grep -E "ATRASO|ERRO" "rec/t7/.fila-$NN.out" | head -12 || true
  FALHOS=$(echo "$RES" | grep -oP 'falhos \K[0-9]+' || true)
  FALHOS=${FALHOS:-99}
  FALHOS_DE[$NN]="$FALHOS"
  if [ "$FALHOS" != "0" ]; then
    echo "!!! cap$NN: $FALHOS passo(s) falho(s) ou sem resumo (veja rec/t7/.fila-$NN.out)"
    case "$ARGS" in *--seed*) echo "FILA PAROU em cap$NN (os seguintes dependem dele)"; exit 1 ;; esac
  fi
done
echo "FILA OK: $*"
