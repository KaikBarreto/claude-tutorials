import json
c=json.load(open('../cadeia.json'))
BTN=lambda n,**k:{'role':'button','name':n,'exact':True,**k}
TAB=lambda n:{'role':'tab','name':n,'exact':True}
DLG='[role=dialog]'
steps=[
 {'do':'goto','url':'/dashboard'},{'do':'waitFor','text':'Olá, Camila!','timeout':25},{'do':'wait','ms':1000},
 {'do':'goto','url':'/financeiro/cobrancas'},{'do':'waitFor','text':'Nenhuma cobrança','timeout':20},
 {'do':'click','target':TAB('Assinaturas')},{'do':'wait','ms':1000},{'do':'shot','name':'c01-vazia'},{'do':'text','selector':'main','name':'subs-vazia','max':1200},
 {'do':'list','selector':'main button,main [role=tab]'},
 {'do':'click','target':BTN('Nova assinatura',nth=0)},{'do':'wait','ms':1000},{'do':'shot','name':'c02-dialogo'},
 {'do':'text','selector':DLG,'name':'dlg','max':2500},
 {'do':'list','selector':DLG+' button,'+DLG+' input,'+DLG+' textarea'},
 {'do':'click','target':{'selector':DLG+' button[role=combobox]','nth':0}},{'do':'wait','ms':500},
 {'do':'type','target':{'placeholder':'Buscar por cliente, telefone ou documento…'},'text':'Academia'},{'do':'wait','ms':600},
 {'do':'click','target':{'text':'Academia Ponto Forte'}},{'do':'wait','ms':800},{'do':'shot','name':'c03-cli'},
 {'do':'eval','js':"[...document.querySelectorAll('[role=dialog] input')].map(i=>(i.placeholder||i.id||i.name)+'='+i.value).join(' | ')"},
 {'do':'click','target':{'selector':DLG+' input[placeholder="0,00"]'}},
 {'do':'keys','target':{'selector':DLG+' input[placeholder="0,00"]'},'text':'38000'},
 {'do':'click','target':{'selector':DLG+' button[role=combobox]','hasText':'Mensal'}},{'do':'wait','ms':500},{'do':'shot','name':'c04-freq'},{'do':'list','selector':'[role=option]'},{'do':'press','key':'Escape'},{'do':'wait','ms':400},
 {'do':'click','target':{'selector':DLG+' button[role=combobox]','hasText':'Cliente escolhe'}},{'do':'wait','ms':500},{'do':'shot','name':'c05-forma'},{'do':'list','selector':'[role=option]'},{'do':'press','key':'Escape'},{'do':'wait','ms':400},
 {'do':'shot','name':'c06-meio'},
 {'do':'click','target':{'selector':DLG+' button[aria-haspopup]','hasText':'/2026'}},{'do':'wait','ms':500},{'do':'shot','name':'c07-cal'},
 {'do':'click','target':{'role':'button','name':'Go to next month'}},{'do':'wait','ms':300},
 {'do':'click','target':{'selector':'[data-radix-popper-content-wrapper] button:text-is("10")'}},{'do':'wait','ms':500},
 {'do':'keys','target':{'placeholder':'Ex.: Contrato de manutenção mensal'},'text':'Manutenção mensal dos splits'},{'do':'wait','ms':400},
 {'do':'shot','name':'c08-preenchido'},{'do':'text','selector':DLG,'name':'dlg2','max':2500},
 {'do':'click','target':{'text':'Resumo por cobrança'}},{'do':'wait','ms':700},{'do':'shot','name':'c09-resumo'},{'do':'text','selector':DLG,'name':'dlg3','max':2500},
 {'do':'click','target':BTN('Criar assinatura')},{'do':'wait','ms':2500},{'do':'shot','name':'c10-criada'},{'do':'text','selector':'main','name':'subs','max':1800},
 {'do':'list','selector':'main button'},
 {'do':'click','target':{'selector':'main button[aria-label="Ações da assinatura"]','nth':0}},{'do':'wait','ms':600},{'do':'shot','name':'c11-menu'},{'do':'list','selector':'[role=menuitem]'},
 {'do':'click','target':{'role':'menuitem','name':'Editar'}},{'do':'wait','ms':800},{'do':'shot','name':'c12-editar'},{'do':'text','selector':DLG,'name':'dlg-edit','max':1800},
 {'do':'click','target':BTN('Cancelar')},{'do':'wait','ms':500},
 {'do':'click','target':{'selector':'main button[aria-label="Ações da assinatura"]','nth':0}},{'do':'wait','ms':600},
 {'do':'click','target':{'role':'menuitem','name':'Cancelar'}},{'do':'wait','ms':800},{'do':'shot','name':'c13-cancelar'},{'do':'text','selector':'[role=alertdialog],[role=dialog]','name':'dlg-cancel','max':1500},{'do':'list','selector':'[role=alertdialog] button,[role=dialog] button'},
 {'do':'click','target':BTN('Voltar')},{'do':'wait','ms':600},{'do':'shot','name':'c14-voltou'},
 {'do':'goto','url':'/contratos'},{'do':'wait','ms':2500},{'do':'shot','name':'c15-contratos'},
 {'do':'click','target':{'text':'PMOC - Hotel Mirante do Mar'}},{'do':'wait','ms':2500},{'do':'shot','name':'c16-contrato'},{'do':'list','selector':'[role=tab]'},
 {'do':'click','target':TAB('Financeiro')},{'do':'wait','ms':1500},{'do':'shot','name':'c17-fin'},{'do':'text','selector':'main','name':'contrato-fin','max':2500},
 {'do':'list','selector':'main button[aria-label],main button[title]','attr':'aria-label'},
 {'do':'eval','js':"[...document.querySelectorAll('main button')].filter(b=>b.querySelector('svg')&&!b.innerText.trim()).slice(0,6).map(b=>(b.getAttribute('aria-label')||b.title||'?')+'@'+Math.round(b.getBoundingClientRect().x)+','+Math.round(b.getBoundingClientRect().y))"},
]
json.dump({'seedExtra':c['inicio']+['t19/apos-cap03'],'stopOnFail':False,'storage':{'dominex:portal-tickets-seen:d40f5787-1779-501f-900c-ddb2b90a36e5':'2031-01-01T00:00:00.000Z'},'steps':steps},open('eC.json','w'),ensure_ascii=False,indent=1)
print('ok')
