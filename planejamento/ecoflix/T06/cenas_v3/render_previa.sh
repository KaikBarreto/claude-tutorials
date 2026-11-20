#!/bin/bash
# T06 · prévia das ilustrações v3: cada janela em trechos de até 13 s, UM TRECHO POR TAREFA da fila pesada (recado do coordenador, 20/11)
# uso: render.sh [id ...]   (sem ids = todas as janelas); REFAZ=1 refaz os trechos que já existem
set -u
TUT=/home/claude/ecoflix; SK=/home/claude/claude-tutorials; A=$SK/planejamento/ecoflix/T06; N=$TUT/t06/narracao; O=/dev/shm/v3_t06/r
python3 -I - "$A" "$N" "$@" <<'P' > $O/lista.txt
import json,sys,unicodedata,re
A,N=sys.argv[1:3]; so=sys.argv[3:]
def norm(w): return re.sub(r'[^a-z0-9%./-]+','',unicodedata.normalize('NFD',w.lower()).encode('ascii','ignore').decode())
def pal(d,a,campo):
    l,p,n=(a+[1])[:3]; k=0
    for w in d['words']:
        if w['linha']==l and re.sub(r'[.,:]$','',norm(w['w']))==norm(p):
            k+=1
            if k==n: return w[campo]
    raise SystemExit(f'ancora {a}')
for i in json.load(open(A+'/cenas/ilustracoes.json')):
    if so and i['id'] not in so: continue
    d=json.load(open(f"{N}/cap{i['cap']:02d}.json"))
    de=max(0,round(pal(d,i['de'],'s')-0.3,2)); ate=round(pal(d,i['ate'],'e')+i.get('cauda',.6),2)
    n=int((ate-de)/13)+1; passo=(ate-de)/n
    for k in range(n): print(i['id'],i['cap'],k,round(de+k*passo,3),round(de+(k+1)*passo,3))
P
while read ID CAP K DE ATE; do
  F=$O/${ID}_$K.mp4; [ -s "$F" ] && [ -z "${REFAZ:-}" ] && continue
  bash $TUT/rec/fila.sh --prio 40 -- nice -n 19 node $SK/ferramentas/edit/cenas/render_cenas.cjs $CAP $N/cap$(printf %02d $CAP).json $O/${ID}_$K.tmp.mp4 --html $A/cenas_v3/cena.html \
    --de $DE --ate $ATE --cauda 0 --larg 1422 --dsf 1.35 > $O/${ID}_$K.log 2>&1 < /dev/null && mv $O/${ID}_$K.tmp.mp4 "$F"
  echo "$ID $K rc=$? $(date +%H:%M)"
done < $O/lista.txt
echo FIM
