import json,sys
c=json.load(open('/home/claude/domiflix/rec/t15/cadeia.json'))
LISTA = """(()=>{const ds=[...document.querySelectorAll('[role=dialog]')];const d=ds.length?ds[ds.length-1]:document.body;const out=[];d.querySelectorAll('button,input,textarea,select,[role=tab],[role=switch],[role=combobox],[role=radio],[role=checkbox],label').forEach(e=>{const r=e.getBoundingClientRect();if(r.width<2||r.height<2)return;out.push([e.tagName.toLowerCase(),e.getAttribute('role')||'',(e.getAttribute('aria-label')||e.innerText||e.placeholder||e.name||'').trim().replace(/\\s+/g,' ').slice(0,60),e.type||'',e.value&&e.type!=='checkbox'?String(e.value).slice(0,30):'',Math.round(r.x),Math.round(r.y)].join(' | '))});return out.join('\\n')})()"""
S=[]
def a(**k): S.append(k)
def shot(n): a(do="shot",name=n)
def lst(n): a(do="eval",js=LISTA,max=7000); 
def txt(n,sel="[role=dialog]"): a(do="text",selector=sel,name=n,max=3000)
def click(**t): a(do="click",target=t)
def ty(ph,text,k=0): a(do="type",target={"selector":f"[role=dialog] input[placeholder='{ph}']","nth":k},text=text)
a(do="goto",url="/funcionarios"); a(do="waitFor",text="Lista de Funcionários",timeout=25); a(do="wait",ms=700)
a(do="eval",js="localStorage.clear();1")
click(role="button",name="Novo Funcionário",exact=True); a(do="wait",ms=900); shot("c1-dados"); lst("dados"); txt("dados")
ty("Nome do funcionário","Tatiane Ribeiro"); ty("000.000.000-00","41837290687"); ty("(00) 00000-0000","2130001008"); ty("email@exemplo.com","tatiane.ribeiro@glacialcold.example"); ty("Ex: Técnico","Assistente administrativa"); ty("Endereço completo","Rua Gavião Peixoto, 120, apto 302, Icaraí, Niterói - RJ")
shot("c2-dados-preenchidos"); lst("dados2")
# data de admissão: abre o seletor
click(role="button",name="Data de Admissão")  # palpite
a(do="wait",ms=700); shot("c3-calendario"); a(do="eval",js="document.querySelector('[data-radix-popper-content-wrapper]')?document.querySelector('[data-radix-popper-content-wrapper]').innerText.slice(0,400):'sem popper'")
a(do="eval",js="[...document.querySelectorAll('[data-radix-popper-content-wrapper] button')].map(b=>(b.getAttribute('aria-label')||b.innerText||'').trim().slice(0,25)).slice(0,45).join(' | ')",max=2000)
json.dump({"seedExtra":c['inicio']+['t15/salarios','t15/folhas'],"start":"/dashboard","storage":{"dominex:portal-tickets-seen:d40f5787-1779-501f-900c-ddb2b90a36e5":"2031-01-01T00:00:00.000Z"},"stopOnFail":False,"steps":S},open('/home/claude/domiflix/rec/t15/_ex/e2.json','w'),indent=1,ensure_ascii=False)
