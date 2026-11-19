#!/bin/bash
# T08 · renderiza as ilustrações v3 (2560x1600) nas janelas do ilustracoes.json com os tempos da voz real.
# Saída: edit/out/ilus/<id>.mp4 e edit/out/ilus/janelas.json (at, dur por id) para o specs.json.
set -u
SK=/home/claude/claude-tutorials; A=$SK/planejamento/ecoflix/T08; N=/home/claude/ecoflix/t08/narracao; O=/home/claude/ecoflix/t08/edit/out/ilus
python3 -I - "$A" "$N" "$O" <<'P' > "$O/lista.txt"
import json,sys,unicodedata,re
A,N,O=sys.argv[1:]
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
    d=json.load(open(f"{N}/cap{i['cap']:02d}.json"))
    de=max(0,round(pal(d,i['de'],'s')-0.3,2)); ate=round(pal(d,i['ate'],'e')+i.get('cauda',.6),2)
    J[i['id']]={'cap':i['cap'],'at':de,'dur':round(ate-de,2)}
    print(i['id'],i['cap'],de,ate)
json.dump(J,open(O+'/janelas.json','w'),indent=1)
P
while read ID CAP DE ATE; do
  [ -s "$O/$ID.mp4" ] && continue
  flock /home/claude/ecoflix/.stills.lock nice -n 19 node $SK/ferramentas/edit/cenas/render_cenas.cjs $CAP $N/cap$(printf %02d $CAP).json "$O/$ID.tmp.mp4" --html $A/cenas_v3/cena.html --de $DE --ate $ATE --dsf 1.35 > "$O/$ID.log" 2>&1 \
    && mv "$O/$ID.tmp.mp4" "$O/$ID.mp4"; echo "$ID rc=$? $(date +%H:%M)"
done < "$O/lista.txt"
