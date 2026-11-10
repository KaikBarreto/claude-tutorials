import json
d={"_comentario":"PROVISÓRIA (exploração): conta Asaas ativa e configurada; será substituída pelo apos-cap03 gerado pela gravação do cap. 3",
 "_patch":{"tenant_payment_accounts":[{"match":{"id":"@id:tpa.glacial"},"set":{"status":"active","auto_post_to_finance":True,"auto_post_fees":True,"default_fine_percent":2,"default_interest_percent":1,"default_due_days":0,"allow_pix":True,"allow_boleto":True,"allow_card":True,"default_finance_account_id":"6711124b-176a-5f89-b699-2d47d1753f78","default_income_category":"Vendas de Serviços","default_fee_category":"Tarifas e Taxas","card_recurring_enabled":True,"pix_auto_enabled":True,"card_fee_override":{"pixFreeCount":0}}}]}}
json.dump(d,open('/home/claude/domiflix/rec/fakebase/seeds-extra/t19/apos-cap03.json','w'),ensure_ascii=False,indent=1)
c=json.load(open('../cadeia.json'))
BTN=lambda n,**k:{'role':'button','name':n,'exact':True,**k}
TAB=lambda n:{'role':'tab','name':n,'exact':True}
DLG='[role=dialog]'
def S(**k): return k
steps=[
 {'do':'goto','url':'/dashboard'},{'do':'waitFor','text':'Olá, Camila!','timeout':25},{'do':'wait','ms':1000},
 {'do':'goto','url':'/financeiro/cobrancas'},{'do':'waitFor','text':'Nenhuma cobrança','timeout':20},{'do':'shot','name':'b01-vazia'},
 {'do':'text','selector':'main','name':'vazia','max':1500},
 {'do':'list','selector':'main button,main [role=tab]'},
 {'do':'click','target':BTN('Nova cobrança',nth=0)},{'do':'wait','ms':1000},{'do':'shot','name':'b02-dialogo'},
 {'do':'text','selector':DLG,'name':'dlg1','max':2500},
 {'do':'list','selector':DLG+' button,'+DLG+' [role=tab],'+DLG+' input,'+DLG+' textarea'},
 {'do':'click','target':{'selector':DLG+' button[role=combobox]','nth':0}},{'do':'wait','ms':500},{'do':'shot','name':'b03-cli'},
 {'do':'list','selector':'[role=option],[cmdk-item],input'},
 {'do':'type','target':{'placeholder':'Buscar por cliente, telefone ou documento…'},'text':'Sabor'},{'do':'wait','ms':600},{'do':'shot','name':'b04-busca'},
 {'do':'list','selector':'[role=option],[cmdk-item]'},
 {'do':'click','target':{'text':'Restaurante Sabor da Serra'}},{'do':'wait','ms':800},{'do':'shot','name':'b05-cli-ok'},
 {'do':'keys','target':{'selector':'#charge-amount'},'text':'45000'},
 {'do':'eval','js':"document.querySelector('#charge-amount').value"},
 {'do':'click','target':{'selector':'#charge-due'}},{'do':'wait','ms':600},{'do':'shot','name':'b06-calendario'},
 {'do':'click','target':{'selector':'[data-radix-popper-content-wrapper] button:text-is("13")'}},{'do':'wait','ms':500},
 {'do':'keys','target':{'selector':'#charge-desc'},'text':'Limpeza e higienização de 2 splits da cozinha'},{'do':'wait','ms':500},{'do':'shot','name':'b07-aba1'},
 {'do':'text','selector':DLG,'name':'dlg-aba1','max':2500},
 {'do':'click','target':BTN('Avançar')},{'do':'wait','ms':600},{'do':'shot','name':'b08-pagamento'},{'do':'text','selector':DLG,'name':'dlg-pag','max':1500},
 {'do':'click','target':{'selector':DLG+' button[role=combobox]','hasText':'Cliente escolhe'}},{'do':'wait','ms':500},{'do':'shot','name':'b09-formas'},
 {'do':'list','selector':'[role=option]'},{'do':'press','key':'Escape'},{'do':'wait','ms':400},
 {'do':'click','target':BTN('Avançar')},{'do':'wait','ms':600},{'do':'shot','name':'b10-encargos'},{'do':'text','selector':DLG,'name':'dlg-enc','max':1500},
 {'do':'eval','js':"[...document.querySelectorAll('[role=dialog] input')].map(i=>(i.placeholder||i.id||i.name)+'='+i.value).join(' | ')"},
 {'do':'click','target':BTN('Avançar')},{'do':'wait','ms':600},{'do':'shot','name':'b11-financeiro'},{'do':'text','selector':DLG,'name':'dlg-fin','max':1800},
 {'do':'click','target':{'text':'Cliente escolhe a forma'}},{'do':'wait','ms':800},{'do':'shot','name':'b12-resumo'},{'do':'text','selector':DLG,'name':'dlg-resumo','max':2500},
 {'do':'click','target':BTN('Gerar cobrança')},{'do':'wait','ms':2500},{'do':'shot','name':'b13-gerada'},{'do':'text','selector':DLG,'name':'dlg-gerada','max':1500},
 {'do':'click','target':{'role':'button','name':'Copiar link'}},{'do':'wait','ms':600},{'do':'shot','name':'b14-copiado'},
 {'do':'list','selector':DLG+' button,'+DLG+' a'},
 {'do':'click','target':BTN('Fechar')},{'do':'wait','ms':1000},{'do':'shot','name':'b15-lista'},
 {'do':'text','selector':'main','name':'lista','max':1500},
 {'do':'list','selector':'main button,main [role=tab]'},
 {'do':'click','target':{'selector':'main button[aria-label="Ações da cobrança"]','nth':0}},{'do':'wait','ms':600},{'do':'shot','name':'b16-menu'},
 {'do':'list','selector':'[role=menuitem]'},
 {'do':'click','target':{'role':'menuitem','name':'Editar'}},{'do':'wait','ms':800},{'do':'shot','name':'b17-editar'},{'do':'text','selector':DLG,'name':'dlg-edit','max':1500},
 {'do':'click','target':BTN('Cancelar')},{'do':'wait','ms':500},
 {'do':'goto','url':'/pagar/hn7xq3rm'},{'do':'wait','ms':2500},{'do':'shot','name':'b18-cliente'},{'do':'text','selector':'body','name':'cliente','max':2000},
 {'do':'click','target':{'text':'Pix','exact':True}},{'do':'wait','ms':800},{'do':'shot','name':'b19-pix'},{'do':'text','selector':'body','name':'pix','max':1500},
 {'do':'click','target':{'text':'Copiar código Pix'}},{'do':'wait','ms':500},{'do':'shot','name':'b20-pix-copiado'},
 {'do':'list','selector':'button'},
 {'do':'click','target':BTN('Voltar')},{'do':'wait','ms':500},{'do':'click','target':{'text':'Boleto','exact':True}},{'do':'wait','ms':800},{'do':'shot','name':'b21-boleto'},{'do':'text','selector':'body','name':'boleto','max':1200},
 {'do':'click','target':BTN('Voltar')},{'do':'wait','ms':500},{'do':'click','target':{'text':'Cartão','exact':True}},{'do':'wait','ms':800},{'do':'shot','name':'b22-cartao'},{'do':'text','selector':'body','name':'cartao','max':1200},
 {'do':'eval','js':"fetch('http://127.0.0.1:54333/functions/v1/asaas-simular-pagamento',{method:'POST',headers:{'content-type':'application/json'},body:'{}'}).then(r=>r.text())"},
 {'do':'goto','url':'/pagar/hn7xq3rm'},{'do':'wait','ms':2500},{'do':'shot','name':'b23-confirmado'},{'do':'text','selector':'body','name':'confirmado','max':1200},
 {'do':'goto','url':'/dashboard'},{'do':'waitFor','text':'Olá, Camila!','timeout':25},
 {'do':'goto','url':'/financeiro/cobrancas'},{'do':'wait','ms':2500},{'do':'shot','name':'b24-lista-paga'},{'do':'text','selector':'main','name':'lista-paga','max':1500},
 {'do':'click','target':{'selector':'main button[aria-label="Ações da cobrança"]','nth':0}},{'do':'wait','ms':600},{'do':'shot','name':'b25-menu-pago'},{'do':'list','selector':'[role=menuitem]'},{'do':'press','key':'Escape'},
 {'do':'goto','url':'/financeiro/contas'},{'do':'wait','ms':2500},
 {'do':'click','target':TAB('A Receber')},{'do':'wait','ms':1000},{'do':'shot','name':'b26-areceber'},
 {'do':'eval','js':"[...document.querySelectorAll('main tr, main [role=row]')].filter(r=>/Limpeza/.test(r.innerText)).map(r=>r.innerText.replace(/\\s+/g,' ')).join(' || ')"},
 {'do':'goto','url':'/financeiro/movimentacoes'},{'do':'wait','ms':2500},{'do':'shot','name':'b27-mov'},
 {'do':'eval','js':"[...document.querySelectorAll('main tr')].filter(r=>/Limpeza|Tarifa/.test(r.innerText)).map(r=>r.innerText.replace(/\\s+/g,' ')).join(' || ')"},
]
json.dump({'seedExtra':c['inicio']+['t19/apos-cap03'],'stopOnFail':False,'storage':{'dominex:portal-tickets-seen:d40f5787-1779-501f-900c-ddb2b90a36e5':'2031-01-01T00:00:00.000Z'},'steps':steps},open('eB.json','w'),ensure_ascii=False,indent=1)
print('ok')
