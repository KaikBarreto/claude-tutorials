import json
c=json.load(open('../cadeia.json'))
BTN=lambda n,**k:{'role':'button','name':n,'exact':True,**k}
TAB=lambda n:{'role':'tab','name':n,'exact':True}
DLG='[role=dialog]'
F="http://127.0.0.1:54333"
mk=("(async()=>{const cs=await (await fetch('%s/__dev/state?table=customers')).json();const id=cs.find(c=>c.name==='Restaurante Sabor da Serra').id;"
    "const r=await fetch('%s/functions/v1/tenant-asaas-create-charge',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({customer_id:id,value:450,due_date:'2026-11-13',billing_type:'UNDEFINED',description:'Limpeza e higienização de 2 splits da cozinha'})});return (await r.text()).slice(0,80)})()"%(F,F))
steps=[
 {'do':'goto','url':'/dashboard'},{'do':'waitFor','text':'Olá, Camila!','timeout':25},
 {'do':'eval','js':mk},
 {'do':'goto','url':'/financeiro/cobrancas'},{'do':'wait','ms':2000},
 {'do':'click','target':{'selector':'main button[aria-label="Ações da cobrança"]','nth':0}},{'do':'wait','ms':500},
 {'do':'eval','js':"[...document.querySelectorAll('[role=menuitem]')].map(x=>x.innerText)"},{'do':'press','key':'Escape'},
 {'do':'goto','url':'/pagar/hn7xq3rmk4vp'},{'do':'wait','ms':2500},{'do':'shot','name':'d01-cliente'},{'do':'text','selector':'body','name':'cliente','max':2000},
 {'do':'list','selector':'button'},
 {'do':'click','target':{'text':'Pix','exact':True}},{'do':'wait','ms':800},{'do':'shot','name':'d02-pix'},{'do':'text','selector':'body','name':'pix','max':1500},
 {'do':'list','selector':'button'},
 {'do':'click','target':BTN('Copiar código Pix')},{'do':'wait','ms':500},{'do':'shot','name':'d03-copiado'},
 {'do':'click','target':{'text':'Voltar'}},{'do':'wait','ms':500},{'do':'click','target':{'text':'Boleto','exact':True}},{'do':'wait','ms':800},{'do':'shot','name':'d04-boleto'},{'do':'text','selector':'body','name':'boleto','max':1200},
 {'do':'click','target':{'text':'Voltar'}},{'do':'wait','ms':500},{'do':'click','target':{'text':'Cartão','exact':True}},{'do':'wait','ms':800},{'do':'shot','name':'d05-cartao'},{'do':'text','selector':'body','name':'cartao','max':1200},
 {'do':'eval','js':"fetch('%s/functions/v1/asaas-simular-pagamento',{method:'POST',headers:{'content-type':'application/json'},body:'{}'}).then(r=>r.text())"%F},
 {'do':'goto','url':'/pagar/hn7xq3rmk4vp'},{'do':'wait','ms':2500},{'do':'shot','name':'d06-confirmado'},{'do':'text','selector':'body','name':'confirmado','max':1200},
 {'do':'goto','url':'/dashboard'},{'do':'waitFor','text':'Olá, Camila!','timeout':25},
 {'do':'goto','url':'/contratos'},{'do':'wait','ms':2500},{'do':'click','target':{'text':'PMOC - Hotel Mirante do Mar'}},{'do':'wait','ms':2000},
 {'do':'click','target':TAB('Financeiro')},{'do':'wait','ms':1500},
 {'do':'hover','target':{'selector':'main button[aria-label="Cobrar online"]','nth':0}},{'do':'wait','ms':900},{'do':'shot','name':'d07-hover'},
 {'do':'click','target':{'selector':'main button[aria-label="Cobrar online"]','nth':0}},{'do':'wait','ms':1200},{'do':'shot','name':'d08-parcela'},{'do':'text','selector':DLG,'name':'parcela','max':1800},
 {'do':'click','target':BTN('Gerar agora')},{'do':'wait','ms':2000},{'do':'shot','name':'d09-gerada'},{'do':'text','selector':DLG,'name':'parcela-gerada','max':800},
 {'do':'click','target':BTN('Fechar')},{'do':'wait','ms':1200},{'do':'shot','name':'d10-selo'},
 {'do':'eval','js':"[...document.querySelectorAll('main')].map(m=>m.innerText).join('').split('\\n').filter(l=>/jan\\/2027|Cobrança gerada|Ver cobrança/.test(l)).join(' | ')"},
 {'do':'eval','js':"[...document.querySelectorAll('main button')].filter(b=>/Ver cobrança|Cobrar online/.test((b.getAttribute('aria-label')||'')+b.innerText)).slice(0,3).map(b=>b.getAttribute('aria-label')+'|'+b.innerText)"},
 {'do':'goto','url':'/financeiro/contas'},{'do':'wait','ms':2500},{'do':'click','target':TAB('A Receber')},{'do':'wait','ms':1000},
 {'do':'eval','js':"[...document.querySelectorAll('main tr')].filter(r=>/Orçamento #2 \\(1\\/3\\)/.test(r.innerText)).map(r=>[...r.querySelectorAll('button')].map(b=>(b.getAttribute('aria-label')||b.innerText||'?')).join(','))"},
]
json.dump({'seedExtra':c['inicio']+['t19/apos-cap03'],'stopOnFail':False,'storage':{'dominex:portal-tickets-seen:d40f5787-1779-501f-900c-ddb2b90a36e5':'2031-01-01T00:00:00.000Z'},'steps':steps},open('eD.json','w'),ensure_ascii=False,indent=1)
