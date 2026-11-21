#!/bin/bash
# T04 · prévia das ilustrações v3 (voz real, 16:9, --larg 1422 --dsf 1.35): cada janela em trechos de até 13 s, UM TRECHO POR
# TAREFA da fila pesada (rec/fila.sh --prio 12). Antes de cada trecho confere o disco (para abaixo de 600 MB). Trechos em /dev/shm/v3_t04/r.
# uso: render_t04.sh [id ...]   REFAZ=1 refaz as que já existem
set -u
TUT=/home/claude/ecoflix; SK=/home/claude/claude-tutorials; A=$SK/planejamento/ecoflix/T04; N=$TUT/t04/narracao; R=/dev/shm/v3_t04/r; O=$R/ilus
mkdir -p "$O"
python3 -I - "$A" "$N" "$O" "$TUT" "$@" <<'P' > "$R/lista.txt"
import json,sys,unicodedata,re,os
A,N,O,TUT=sys.argv[1:5]; so=sys.argv[5:]
def norm(w): return re.sub(r'[^a-z0-9%./-]+','',unicodedata.normalize('NFD',w.lower()).encode('ascii','ignore').decode())
def pal(d,a,campo):
    l,p,n=(a+[1])[:3]; k=0
    for w in d['words']:
        if w['linha']==l and re.sub(r'[.,:]$','',norm(w['w']))==norm(p):
            k+=1
            if k==n: return w[campo]
    raise SystemExit(f'ancora {a}')
J={}
for i in json.load(open(A+'/cenas/ilustracoes.json')):
    v3=i.get('v3','')
    if not v3.endswith('.html'): continue
    d=json.load(open(f"{N}/cap{i['cap']:02d}.json")); assert not d.get('estimado'), 'voz estimada'
    de=max(0,round(pal(d,i['de'],'s')-0.3,2)); ate=round(pal(d,i['ate'],'e')+i.get('cauda',.6),2)
    J[i['id']]={'cap':i['cap'],'at':de,'dur':round(ate-de,2)}
    if so and i['id'] not in so: continue
    n=int((ate-de)/13)+1; q=round((ate-de)*30/n)/30
    for k in range(n): print(i['id'],i['cap'],k,n,round(de+k*q,4),ate if k==n-1 else round(de+(k+1)*q,4),os.path.join(A,v3),os.path.join(TUT,i['anexo']) if i.get('anexo') else '-')
json.dump(J,open(O+'/janelas.json','w'),indent=1)
P
while read ID CAP K NT DE ATE HTML ANEXO; do
  [ -s "$O/$ID.mp4" ] && [ -z "${REFAZ:-}" ] && continue
  [ -s "$R/${ID}_$K.mp4" ] && [ -z "${REFAZ:-}" ] || {
    L=$(df --output=avail -m / | tail -1); echo "disco $L MB"; [ "$L" -lt 600 ] && { echo "PAROU: disco abaixo de 600 MB"; exit 9; }
    EXTRA=(); [ "$ANEXO" != "-" ] && EXTRA=(--anexo "$ANEXO")
    bash $TUT/rec/fila.sh --prio 12 -- nice -n 19 node $SK/ferramentas/edit/cenas/render_cenas.cjs $CAP $N/cap$(printf %02d $CAP).json "$R/${ID}_$K.mp4" --html "$HTML" "${EXTRA[@]}" \
      --de $DE --ate $ATE --cauda 0 --larg 1422 --dsf 1.35 > "$R/${ID}_$K.log" 2>&1 < /dev/null
    rc=$?; echo "$ID trecho $K/$NT rc=$rc $(date +%H:%M)"; [ $rc -ne 0 ] && continue; }
  if [ $((K + 1)) -eq "$NT" ]; then
    ok=1; : > "$R/$ID.txt"; for k in $(seq 0 $((NT - 1))); do [ -s "$R/${ID}_$k.mp4" ] || ok=0; echo "file '$R/${ID}_$k.mp4'" >> "$R/$ID.txt"; done
    if [ $ok -eq 1 ]; then
      if [ "$NT" -eq 1 ]; then mv "$R/${ID}_0.mp4" "$O/$ID.mp4"; else ffmpeg -nostdin -v error -y -f concat -safe 0 -i "$R/$ID.txt" -c copy "$R/$ID.j.mp4" && mv "$R/$ID.j.mp4" "$O/$ID.mp4"; fi
      for k in $(seq 0 $((NT - 1))); do rm -f "$R/${ID}_$k.mp4"; done; rm -f "$R/$ID.txt"
      echo "$ID pronto $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$O/$ID.mp4") s · $(python3 -I $SK/perfis/ecoflix/cenas_v3/piscadas.py "$O/$ID.mp4" 2>&1 | tail -1)"
    else echo "$ID: falta trecho"; fi
  fi
done < "$R/lista.txt"
echo FIM
