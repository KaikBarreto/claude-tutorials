#!/bin/bash
# T02 · renderiza as ilustrações v3 nas janelas do ilustracoes.json com os tempos da voz real, em 16:9 (--larg 1422, --dsf 1.35:
# 1920x1080, maior que a caixa de 1763x992 do palco; com 1,3 a largura sai ímpar e o x264 recusa). Cada ilustração usa a página dela ("v3") e, se tiver, a pasta "anexo"
# (relativa ao TUT_HOME: o PNG do comprovante real). Saída: edit/out/ilus/<id>.mp4 e edit/out/ilus/janelas.json (at, dur por id).
# Depois de cada render: piscadas.py (elemento que some e volta). REFAZ=1 refaz as que já existem.
set -u
TUT=/home/claude/ecoflix; SK=/home/claude/claude-tutorials; A=$SK/planejamento/ecoflix/T02; N=$TUT/t02/narracao; O=$TUT/t02/edit/out/ilus
mkdir -p "$O"
python3 -I - "$A" "$N" "$O" "$TUT" <<'P' > "$O/lista.txt"
import json,sys,unicodedata,re,os
A,N,O,TUT=sys.argv[1:]
def norm(w): return re.sub(r'[^a-z0-9%./-]+','',unicodedata.normalize('NFD',w.lower()).encode('ascii','ignore').decode())
def pal(d,a,campo):
    l,p,n=(a+[1])[:3]; k=0
    for w in d['words']:
        if w['linha']==l and re.sub(r'[.,:]$','',norm(w['w']))==norm(p):
            k+=1
            if k==n: return w[campo]
    raise SystemExit(f'ancora {a}')
J={}
LOC=json.load(open(os.path.join(TUT,'t02/edit/ilus_local.json')))   # ajustes locais por id (o ilustracoes.json da aula não é editado aqui)
for i in json.load(open(A+'/cenas/ilustracoes.json')):
    i.update(LOC.get(i['id'],{}))
    html=os.path.join(A,i.get('v3','cenas_v3/cena.html'))
    if not os.path.isfile(html): print('PENDENTE',i['id'],i.get('v3'),file=sys.stderr); continue   # cena ainda não feita ("v3": "pendente")
    d=json.load(open(f"{N}/cap{i['cap']:02d}.json"))
    de=max(0,round(pal(d,i['de'],'s')-0.3,2)); ate=round(pal(d,i['ate'],'e')+i.get('cauda',.6),2)
    J[i['id']]={'cap':i['cap'],'at':de,'dur':round(ate-de,2)}
    print(i['id'],i['cap'],de,ate,os.path.join(A,i.get('v3','cenas_v3/cena.html')),os.path.join(TUT,i['anexo']) if i.get('anexo') else '-')
json.dump(J,open(O+'/janelas.json','w'),indent=1)
P
while read ID CAP DE ATE HTML ANEXO; do
  [ -s "$O/$ID.mp4" ] && [ -z "${REFAZ:-}" ] && continue
  [[ " ${PULA:-} " == *" $ID "* ]] && continue   # PULA="id ..." deixa estas para depois (ex.: voz do capítulo ainda por chegar)
  EXTRA=(); [ "$ANEXO" != "-" ] && EXTRA=(--anexo "$ANEXO")
  flock $TUT/.stills.lock nice -n 19 node $SK/ferramentas/edit/cenas/render_cenas.cjs $CAP $N/cap$(printf %02d $CAP).json "$O/$ID.tmp.mp4" --html "$HTML" "${EXTRA[@]}" \
    --de $DE --ate $ATE --larg 1422 --dsf 1.35 > "$O/$ID.log" 2>&1 && mv "$O/$ID.tmp.mp4" "$O/$ID.mp4"
  echo "$ID rc=$? $(date +%H:%M) $(python3 -I $SK/perfis/ecoflix/cenas_v3/piscadas.py "$O/$ID.mp4" 2>&1 | head -1 | sed 's/.*: //')"
done < "$O/lista.txt"
