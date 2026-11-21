#!/bin/bash
# T09 · prévia das ilustrações v3 (voz real, 16:9, --larg 1422 --dsf 1.35): cada janela em trechos de até 13 s, UM TRECHO POR
# TAREFA da fila pesada (rec/fila.sh --prio 12). Antes de cada trecho confere o disco (para abaixo de 600 MB). Trechos em
# /dev/shm/v3_t09/r. No fim (todas as janelas prontas), junta na ordem da aula em previa_ilustracoes/T09_v3.mp4 e monta a
# folha T09_v3.jpg (12 quadros). Molde: T04/cenas_v3/render_previa.sh.
# uso: render_previa.sh [id ...]   REFAZ=1 refaz as que já existem
set -u
TUT=/home/claude/ecoflix; SK=/home/claude/claude-tutorials; A=$SK/planejamento/ecoflix/T09; N=$TUT/t09/narracao; R=/dev/shm/v3_t09/r; O=$R/ilus
PV=$TUT/previa_ilustracoes
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
# a prévia da aula: todas as janelas, na ordem da aula (capítulo, instante), e a folha de 12 quadros (o fim de cada janela;
# a mais longa ganha também o meio)
python3 -I - "$O" "$PV" <<'P'
import json,os,shutil,subprocess,sys
from PIL import Image
O,PV=sys.argv[1:3]; J=json.load(open(O+'/janelas.json')); ids=sorted(J,key=lambda i:(J[i]['cap'],J[i]['at']))
falta=[i for i in ids if not (os.path.exists(f'{O}/{i}.mp4') and os.path.getsize(f'{O}/{i}.mp4'))]
if falta: sys.exit(f'prévia: faltam {falta}')
open(O+'/aula.txt','w').write(''.join(f"file '{O}/{i}.mp4'\n" for i in ids))
# os trechos saem em crf 14 (130 MB a aula toda): junta em /dev/shm e reencoda pela fila até caber nos 25 MB da prévia
subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-f','concat','-safe','0','-i',O+'/aula.txt','-c','copy',O+'/aula.mp4'],check=True)
for crf in (24, 28):
    subprocess.run(['bash','/home/claude/ecoflix/rec/fila.sh','--prio','12','--','nice','-n','19','ffmpeg','-nostdin','-v','error','-y','-i',O+'/aula.mp4','-c:v','libx264','-preset','medium',
        '-crf',str(crf),'-maxrate','1.8M','-bufsize','3.6M','-pix_fmt','yuv420p','-movflags','+faststart','-an',O+'/aula25.mp4'],check=True)
    if os.path.getsize(O+'/aula25.mp4')<=25e6: break
shutil.move(O+'/aula25.mp4',PV+'/T09_v3.mp4'); os.remove(O+'/aula.mp4')
q=[(i,J[i]['dur']-.7) for i in ids]; lg=max(ids,key=lambda i:J[i]['dur']); q.insert(ids.index(lg),(lg,J[lg]['dur']*.5)); q=q[:12]
TW,TH,G=960,540,8; folha=Image.new('RGB',(3*TW+2*G,4*TH+3*G),'white')
for n,(i,t) in enumerate(q):
    f=f'{O}/q{n}.jpg'; subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-ss',f'{t:.2f}','-i',f'{O}/{i}.mp4','-frames:v','1','-q:v','3',f],check=True)
    folha.paste(Image.open(f).resize((TW,TH)),((n%3)*(TW+G),(n//3)*(TH+G))); os.remove(f)
folha.save(PV+'/T09_v3.jpg',quality=86)
d=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',PV+'/T09_v3.mp4'],capture_output=True,text=True).stdout)
print(f'prévia {PV}/T09_v3.mp4: {d:.1f} s, {os.path.getsize(PV+"/T09_v3.mp4")/1e6:.1f} MB · folha T09_v3.jpg')
P
echo FIM
