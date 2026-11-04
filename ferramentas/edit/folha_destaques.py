"""Folha de TODOS os destaques e zooms do 9:16 (celular) com o rótulo ao lado e conferência por OCR do texto do alvo.
uso: python3 -I folha_destaques.py <saida.jpg>   (lê t0v2/edit/caps/cap0N.9x16.chapter.json e as gravações do celular; imprime os destaques com OCR OK/NAO CONFERE;
destaque = retângulo vermelho, zoom = janela azul; tesseract 'eng' tira o acento, então "dúvidas"/"Cobranças" podem sair como falha de OCR: olhe o quadro).
Ajuste E (pasta edit da aula) e ZL (rótulos dos zooms, na ordem do capítulo) para outra aula."""
import json, subprocess, os, sys, unicodedata, re
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0,'/home/claude/domiflix/t0v2/edit')
E='/home/claude/domiflix/t0v2/edit'
def norm(s): return re.sub(r'[^a-z0-9 ]','',unicodedata.normalize('NFD',s.lower()).encode('ascii','ignore').decode())
def frame(video,t,path):
    subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',str(max(t,0)),'-i',video,'-frames:v','1',path],check=True); return Image.open(path).convert('RGB')
def ocr(img):
    img.save('/tmp/claude-0/fd/o.png'); return subprocess.run(['tesseract','/tmp/claude-0/fd/o.png','-','--psm','6','-l','eng'],capture_output=True,text=True).stdout
ZL={1:['Formação básica','Na sequência do seu plano','Conheça este módulo','selo Não tem no seu plano','botão Escolher meu plano','Materiais e extras','Trilha do seu plano 43%','Próxima recomendada','abre o Menu','Tutoriais | Domiflix'],
 2:['Trilha do seu plano'],3:['botão Tirar dúvidas ... / clica','busca do guia','Falar com o Suporte / clica'],4:['status ... valor','Pagar Agora ... 20% de desconto'],
 5:['abre Gerenciar Meu Plano','Cobranças online ... CRM / Kanban','sobe usuários ... 2'],6:['marca a caixa ... botão Confirmar']}
cells=[]; rel=[]
for n in range(1,7):
    c=json.load(open(f'{E}/caps/cap{n:02d}.9x16.chapter.json')); v=c['video']
    for s in c['spots']:
        t=s['at']+0.9; im=frame(v,t,'/tmp/claude-0/fd/f.png'); x,y,w,h=s['rect']
        crop=im.crop((max(0,int(x-6)),max(0,int(y-6)),min(im.width,int(x+w+6)),min(im.height,int(y+h+6))))
        txt=norm(ocr(crop.resize((crop.width*3,crop.height*3))))
        ok=all(tok in txt for tok in norm(s['label']).split()[:2]) 
        d=ImageDraw.Draw(im); d.rectangle((x,y,x+w,y+h),outline=(255,0,0),width=6)
        reg=im.crop((0,max(0,int(y-200)),780,min(im.height,int(y+h+200))))
        cells.append((f'cap{n:02d} t={t:.1f}s DESTAQUE "{s["label"]}"  OCR: {"OK" if ok else "NAO CONFERE"}',reg)); rel.append((n,'destaque',s['label'],round(t,1),ok,txt[:50]))
    for i,z in enumerate(c['zooms']):
        t=z['at']+0.8; im=frame(v,t,'/tmp/claude-0/fd/f.png'); x,y,w,h=z['rect']
        d=ImageDraw.Draw(im); d.rectangle((x+4,y+4,x+w-4,y+h-4),outline=(0,160,255),width=8)
        lab=ZL[n][i] if i<len(ZL[n]) else '?'
        cells.append((f'cap{n:02d} t={t:.1f}s ZOOM "{lab}" (janela azul = o que o zoom mostra)',im)); rel.append((n,'zoom',lab,round(t,1),None,''))
W=300; font=ImageFont.load_default()
rows=[]; per=6
for k in range(0,len(cells),per):
    row=cells[k:k+per]; imgs=[]
    for cap,im in row:
        r=im.resize((W,int(im.height*W/im.width))); canvas=Image.new('RGB',(W,r.height+36),(20,20,20)); canvas.paste(r,(0,36)); ImageDraw.Draw(canvas).text((3,3),cap[:55]+'\n'+cap[55:110],fill=(255,255,255),font=font); imgs.append(canvas)
    hh=max(i.height for i in imgs); R=Image.new('RGB',(W*per,hh),(0,0,0))
    for j,i in enumerate(imgs): R.paste(i,(j*W,0))
    rows.append(R)
H=sum(r.height for r in rows); S=Image.new('RGB',(W*per,H)); yy=0
for r in rows: S.paste(r,(0,yy)); yy+=r.height
out=sys.argv[1]; S.save(out,quality=88); json.dump(rel,open(out+'.json','w'),ensure_ascii=False)
for r in rel:
    if r[1]=='destaque': print(r)
print(S.size)
