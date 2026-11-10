import sys; sys.path.insert(0,'/home/claude/domiflix/rec/t15/_ex')
from _lib import *
def keys(sel,text,nth=0): a(do="keys",target={"selector":sel,"nth":nth},text=text,delay=30)
def toast(): a(do="eval",js="[...document.querySelectorAll('[data-sonner-toast],[role=status],li[role=status],ol li')].map(t=>t.innerText.replace(/\\n/g,' / ')).slice(0,4).join(' || ')",max=600)
def esc(): a(do="press",key="Escape"); wait(300); a(do="press",key="Escape"); wait(300)
a(do="goto",url="/funcionarios"); a(do="waitFor",text="Lista de Funcionários",timeout=25); wait()
click(text="Rafael Lima",within="main"); wait(900)
# vale
click(role="button",name="Vale",exact=True); wait(900)
click(selector="[role=dialog] button[role=combobox]",nth=0); wait(400); click(role="option",name="Caixa (em dinheiro)"); wait(300)
keys("[role=dialog] input[placeholder='R$ 0,00']","30000"); keys("[role=dialog] textarea","Adiantamento"); wait(300); shot("h1-vale-pronto"); a(do="eval",js="[...document.querySelectorAll('[role=dialog] input,[role=dialog] textarea')].map(i=>i.value).join(' | ')")
click(role="button",name="Registrar Vale",exact=True); wait(1500); toast(); shot("h2-apos-vale"); txt("ficha","main",3000)
# bonus
click(role="button",name="Bônus",exact=True); wait(900); shot("h3-bonus"); txt("bonus",mx=900)
keys("[role=dialog] input[placeholder='R$ 0,00']","15000"); keys("[role=dialog] textarea","Bônus por produtividade"); wait(300)
click(role="button",name="Registrar Bônus",exact=True); wait(1500); toast()
# falta
click(role="button",name="Falta",exact=True); wait(1200); shot("h4-falta"); lst(); txt("falta",mx=1500)
a(do="eval",js="[...document.querySelectorAll('[role=dialog] input,[role=dialog] textarea')].map(i=>i.placeholder+'='+i.value).join(' | ')")
keys("[role=dialog] textarea","Falta em 06/11"); wait(300); shot("h5-falta-pronta")
click(role="button",name="Registrar Falta",exact=True); wait(1500); toast(); shot("h6-apos-falta"); txt("ficha","main",3000)
# pagamento
click(role="button",name="Pagamento",exact=True); wait(1500); shot("h7-pagamento"); lst(); txt("pagamento",mx=3500)
click(role="button",name="Confirmar Pagamento",exact=True); wait(1800); shot("h8-recibo"); txt("recibo",mx=1200)
click(role="button",name="Não",exact=True); wait(1500); toast(); shot("h9-apos-pag"); txt("ficha","main",3000)
# extrato
click(role="button",name="Extrato",exact=True); wait(1500); shot("h10-extrato"); txt("extrato",mx=4500)
esc()
a(do="eval",js="location.pathname")
out("e3b",c['inicio']+['t15/salarios','t15/folhas'])
