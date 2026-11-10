#!/usr/bin/env bash
# T7 · edição + render + prévia leve de UM capítulo já gravado (não grava): specs, montar_cap, auditoria da câmera, render e prévia
# na MESMA posse da trava (uma espera só), conferências leves depois.
# uso: rec/t7/render_um.sh NN
set -uo pipefail
cd /home/claude/domiflix
export TUT_HOME=/home/claude/domiflix
NN=$(printf '%02d' "$((10#${1:?capítulo}))"); EDIT=t7/edit
echo "--- [$(date +%H:%M:%S)] edição do cap$NN (specs, montar_cap, auditoria da câmera)"
python3 -I rec/t7/specs.py > "$EDIT/out/specs.log" 2>&1 || { echo "!!! specs.py falhou"; tail -5 "$EDIT/out/specs.log"; exit 1; }
python3 -I "$EDIT/montar_cap.py" "$NN" > "$EDIT/out/montar_$NN.log" 2>&1 || { echo "!!! montar_cap falhou"; tail -8 "$EDIT/out/montar_$NN.log"; exit 1; }
tail -2 "$EDIT/out/montar_$NN.log"
python3 -I "$EDIT/auditar_camera.py" "$EDIT/caps/cap$NN.chapter.json" > "$EDIT/out/audit_$NN.log" 2>&1
tail -4 "$EDIT/out/audit_$NN.log"
DUR=$(python3 -I -c "import json;print(int(json.load(open('$EDIT/caps/cap$NN.chapter.json')).get('trim',{}).get('end') or 0))")
[ "$DUR" -gt 0 ] || DUR=$(python3 -I -c "import json;print(int(json.load(open('rec/t7/t7-cap$NN.actions.json'))['video']['durationS']))")
TS=$(python3 -I -c "d=$DUR;print(' '.join(str(max(1,int(d*k/9))) for k in range(1,9)))")
echo "--- [$(date +%H:%M:%S)] renderizando cap$NN + prévia (uma posse da trava)"
flock "$TUT_HOME/.heavy.lock" nice -n 10 env TUT_LOCKED=1 bash -c "python3 -I $EDIT/render_chapter.py $EDIT/caps/cap$NN.chapter.json > $EDIT/out/render_$NN.log 2>&1 && bash $EDIT/previa.sh cap$NN '$TS' > $EDIT/out/previa_$NN.log 2>&1; r=\$?; python3 -I $EDIT/auditar_recorte.py $EDIT/caps/cap$NN.chapter.json --n 40 > $EDIT/out/recorte_$NN.log 2>&1; exit \$r"
RC=$?
tail -2 "$EDIT/out/recorte_$NN.log"
tail -c 400 "$EDIT/out/render_$NN.log" | tr '\r' '\n' | tail -3
[ "$RC" -eq 0 ] || { echo "!!! render/prévia do cap$NN falhou (rc=$RC), veja $EDIT/out/render_$NN.log e previa_$NN.log"; exit 1; }
python3 -I "$EDIT/confere_render.py" "cap$NN"
tail -3 "$EDIT/out/previa_$NN.log"
echo "--- [$(date +%H:%M:%S)] cap$NN renderizado: $EDIT/out/cap$NN/"
