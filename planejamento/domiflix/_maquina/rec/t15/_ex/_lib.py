import json
c=json.load(open('/home/claude/domiflix/rec/t15/cadeia.json'))
LISTA = """(()=>{const ds=[...document.querySelectorAll('[role=dialog]')];const d=ds.length?ds[ds.length-1]:document.body;const out=[];d.querySelectorAll('button,input,textarea,select,[role=tab],[role=switch],[role=combobox],[role=radio],[role=checkbox],label').forEach(e=>{const r=e.getBoundingClientRect();if(r.width<2||r.height<2)return;out.push([e.tagName.toLowerCase(),e.getAttribute('role')||'',(e.getAttribute('aria-label')||e.innerText||e.placeholder||e.name||'').trim().replace(/\\s+/g,' ').slice(0,60),e.type||'',e.value&&e.type!=='checkbox'?String(e.value).slice(0,30):'',Math.round(r.x),Math.round(r.y)].join(' | '))});return out.join('\\n')})()"""

S=[]
def a(**k): S.append(k)
def shot(n): a(do="shot",name=n)
def lst(n=''): a(do="eval",js=LISTA,max=7000)
def txt(n,sel="[role=dialog]",mx=3000): a(do="text",selector=sel,name=n,max=mx)
def click(**t): a(do="click",target=t)
def ty(ph,text,k=0): a(do="type",target={"selector":f"[role=dialog] input[placeholder='{ph}']","nth":k},text=text)
def wait(ms=700): a(do="wait",ms=ms)
STORAGE={"dominex:portal-tickets-seen:d40f5787-1779-501f-900c-ddb2b90a36e5":"2031-01-01T00:00:00.000Z"}
def out(nome,seeds,device=None,start="/dashboard"):
    d={"seedExtra":seeds,"start":start,"storage":STORAGE,"stopOnFail":False,"steps":S}
    if device: d["device"]=device
    json.dump(d,open(f'/home/claude/domiflix/rec/t15/_ex/{nome}.json','w'),indent=1,ensure_ascii=False)
