import json
DUMP = ("(()=>{const ds=[...document.querySelectorAll('[role=dialog],[data-radix-popper-content-wrapper]')];const root=ds.length?ds[ds.length-1]:document.querySelector('main')||document;"
        "return [...root.querySelectorAll('button,input,textarea,select,[role=combobox],[role=switch],[role=checkbox],[role=tab],[role=option],[role=menuitem],[role=slider]')]"
        ".filter(e=>e.getClientRects().length).map(e=>{const r=e.getBoundingClientRect();return [e.tagName[0],e.type||'',e.getAttribute('role')||'',(e.innerText||'').replace(/\\s+/g,' ').slice(0,38),e.getAttribute('aria-label')||'',e.placeholder||'',(e.value||'').slice(0,14),Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height),e.disabled?'D':''].join('|')})})()")
def dump(name, mx=6000): return {"do":"eval","js":DUMP,"max":mx}
def dlg_text(name, mx=2500): return {"do":"text","selector":"[role=dialog]","name":name,"max":mx}
S=[]
def a(*x): S.extend(x)
CHAIN = ["t3/apos-cap10","t1/apos-cap13","t4/inicio","t4/apos-cap14","t5/inicio","t9/inicio","t9/_dev/apos-cap04"]
a({"do":"goto","url":"/orcamentos"},
  {"do":"waitFor","text":"Gerencie orçamentos, custos e precificação","timeout":20},
  {"do":"wait","ms":1200},
  {"do":"eval","js":"(()=>{try{sessionStorage.clear()}catch(e){}return 'ss limpo'})()"},
  {"do":"click","target":{"role":"button","name":"Novo Orçamento","exact":True},"after":1200},
  {"do":"shot","name":"20-wizard-etapa1"},
  dump("etapa1"),
  {"do":"html","selector":"[role=dialog] [role=switch], [role=dialog] [data-state]","max":900},
  # prospecto
  {"do":"click","target":{"text":"Novo prospecto","exact":True,"within":"[role=dialog]"},"optional":True,"after":600},
  {"do":"shot","name":"21-prospecto"},
  dump("prospecto"),
  {"do":"click","target":{"text":"Cliente cadastrado","exact":True,"within":"[role=dialog]"},"optional":True,"after":600},
  # cliente
  {"do":"click","target":{"role":"combobox","name":"Selecione o cliente"},"optional":True,"after":700},
  {"do":"shot","name":"22-cliente-lista"},
  dump("cliente-lista"),
  {"do":"keys","target":{"selector":"[cmdk-input]"},"text":"Pousada","delay":60,"optional":True},
  {"do":"shot","name":"23-cliente-busca"},
  dump("cliente-busca"),
  {"do":"click","target":{"role":"option","name":"Pousada Brisa do Mar"},"optional":True,"after":700},
  {"do":"shot","name":"24-cliente-escolhido"},
  {"do":"click","target":{"role":"button","name":"Próximo","exact":True},"after":1200},
  {"do":"shot","name":"25-etapa2"},
  dump("etapa2"),
  {"do":"text","selector":"[role=dialog]","name":"etapa2 texto","max":2500},
  # serviço
  {"do":"click","target":{"role":"combobox","name":"Selecionar tipo de serviço..."},"optional":True,"after":800},
  {"do":"shot","name":"26-servico-lista"},
  dump("servico-lista"),
  {"do":"click","target":{"role":"option","name":"Higienização de Split"},"optional":True,"after":700},
  {"do":"shot","name":"27-servico-escolhido"},
  dump("servico-escolhido"),
  {"do":"keys","target":{"selector":"[role=dialog] input.w-16"},"text":"3","clear":True,"delay":60,"optional":True},
  {"do":"click","target":{"role":"button","name":"Adicionar","exact":True,"within":"[role=dialog]"},"optional":True,"after":1500},
  {"do":"shot","name":"28-servico-adicionado"},
  dump("servico-adicionado"),
  {"do":"text","selector":"[role=dialog]","name":"depois de adicionar","max":3000},
  {"do":"click","target":{"text":"Higienização de Split","exact":False,"within":"[role=dialog] table"},"optional":True,"after":800},
  {"do":"shot","name":"29-servico-expandido"},
  {"do":"text","selector":"[role=dialog]","name":"expandido","max":3200},
  {"do":"click","target":{"role":"combobox","name":"Selecionar tipo de serviço..."},"optional":True,"after":800},
  {"do":"click","target":{"role":"option","name":"Carga de Gás"},"optional":True,"after":700},
  {"do":"click","target":{"role":"button","name":"Adicionar","exact":True,"within":"[role=dialog]"},"optional":True,"after":1500},
  {"do":"shot","name":"30-carga-gas"},
  {"do":"text","selector":"[role=dialog]","name":"depois da carga de gás","max":3500},
  dump("etapa2-fim"),
  # etapa 3
  {"do":"click","target":{"role":"button","name":"Próximo","exact":True},"after":1200},
  {"do":"shot","name":"31-etapa3"},
  dump("etapa3"),
  {"do":"click","target":{"role":"button","name":"Adicionar materiais"},"optional":True,"after":1000},
  {"do":"shot","name":"32-seletor-materiais"},
  dump("seletor"),
  {"do":"keys","target":{"placeholder":"Buscar por nome, código ou categoria..."},"text":"gás","delay":80,"optional":True},
  {"do":"shot","name":"33-seletor-gas"},
  dump("seletor-gas"),
  {"do":"eval","js":"[...document.querySelectorAll('[role=dialog]')].pop().innerText","max":1800},
  )
json.dump({"seedExtra":CHAIN,"start":"/dashboard","stopOnFail":False,"steps":S}, open('s2a.json','w'), ensure_ascii=False, indent=1)
print(len(S),'passos')

a(
  {"do":"click","target":{"selector":"[role=dialog] div[role=button]:has-text('R-410A') button","nth":1},"optional":True,"after":700},
  {"do":"eval","js":"[...document.querySelectorAll('[role=dialog]')].pop().innerText","max":1500},
  dump("seletor-qtd1"),
  {"do":"click","target":{"role":"button","name":"Adicionar ao orçamento"},"optional":True,"after":1200},
  {"do":"shot","name":"34-materiais-adicionado"},
  {"do":"keys","target":{"selector":"[role=dialog] input[placeholder*='km']"},"text":"18","delay":80,"optional":True},
  {"do":"shot","name":"35-deslocamento"},
  {"do":"text","selector":"[role=dialog]","name":"etapa3 final","max":2500},
  dump("etapa3-fim"),
  # etapa 4
  {"do":"click","target":{"role":"button","name":"Próximo","exact":True},"after":1200},
  {"do":"shot","name":"36-etapa4"},
  dump("etapa4"),
  {"do":"keys","target":{"selector":"[role=dialog] input[type=number]","nth":0},"text":"67,00","delay":80,"optional":True},
  {"do":"eval","js":"[...document.querySelectorAll('[role=dialog] input[type=number]')].map(i=>i.value)","max":300},
  {"do":"shot","name":"37-desconto"},
  {"do":"click","target":{"role":"combobox","name":"R$"},"optional":True,"after":600},
  dump("select-desconto"),
  {"do":"click","target":{"role":"option","name":"%"},"optional":True,"after":600},
  {"do":"shot","name":"38-desconto-pct"},
  {"do":"click","target":{"role":"combobox","name":"%"},"optional":True,"after":600},
  {"do":"click","target":{"role":"option","name":"R$"},"optional":True,"after":600},
  {"do":"shot","name":"39-desconto-reais"},
  {"do":"click","target":{"placeholder":"Observações internas"},"optional":True},
  {"do":"keys","target":{"placeholder":"Observações internas"},"text":"Atendimento de segunda a sexta, das 8h às 17h.","delay":20,"optional":True},
  {"do":"keys","target":{"placeholder":"Condições de pagamento, garantia, etc."},"text":"Serviço executado após a aprovação, com data combinada com o cliente.","delay":20,"optional":True},
  {"do":"shot","name":"40-textos"},
  {"do":"eval","js":"[...document.querySelectorAll('[role=dialog] textarea')].map(t=>t.value)","max":400},
  # etapa 5
  {"do":"click","target":{"role":"button","name":"Próximo","exact":True},"after":1200},
  {"do":"shot","name":"41-etapa5"},
  dump("etapa5"),
  {"do":"click","target":{"text":"dd/mm/aaaa","exact":True,"within":"[role=dialog]"},"optional":True,"after":800},
  {"do":"shot","name":"42-calendario"},
  dump("calendario"),
  {"do":"eval","js":"[...document.querySelectorAll('[role=gridcell]')].slice(14,24).map(e=>[e.tagName,e.getAttribute('name'),e.innerText,e.getAttribute('aria-selected'),e.disabled].join('|'))","max":600},
  {"do":"click","target":{"role":"gridcell","name":"18","exact":True},"optional":True,"after":800},
  {"do":"shot","name":"43-etapa5-validade"},
  {"do":"text","selector":"[role=dialog]","name":"etapa5 texto","max":3500},
  {"do":"eval","js":"(()=>{const d=document.querySelector('[role=dialog]');d.scrollTo&&d.scrollTo(0,99999);const sc=[...d.querySelectorAll('*')].filter(e=>e.scrollHeight>e.clientHeight+20&&getComputedStyle(e).overflowY!=='visible');return sc.map(e=>[e.tagName,e.className.slice(0,50),e.scrollHeight,e.clientHeight].join('|'))})()","max":900},
  )
json.dump({"seedExtra":CHAIN,"start":"/dashboard","stopOnFail":False,"steps":S}, open('s2.json','w'), ensure_ascii=False, indent=1)
print(len(S),'passos (completo)')

ROW = "main tbody tr:has-text('Pousada Brisa do Mar') button[aria-haspopup='menu']"
a(
  {"do":"click","target":{"role":"button","name":"Criar Orçamento","exact":True},"optional":True,"after":2500},
  {"do":"shot","name":"44-criado"},
  {"do":"eval","js":"(document.querySelector('[data-sonner-toaster]')||{}).innerText||'sem toast'","max":300},
  {"do":"text","selector":"main","name":"lista depois de criar","max":2200},
  {"do":"eval","js":"[...document.querySelectorAll(\"main tbody tr button[aria-haspopup='menu']\")].slice(0,3).map(b=>[b.getAttribute('aria-label'),b.title,Math.round(b.getBoundingClientRect().x),Math.round(b.getBoundingClientRect().y)].join('|'))","max":400},
  {"do":"click","target":{"selector":ROW},"optional":True,"after":800},
  {"do":"shot","name":"45-menu-linha"},
  dump("menu-linha"),
  {"do":"click","target":{"role":"menuitem","name":"Visualizar"},"optional":True,"after":1500},
  {"do":"shot","name":"46-visualizar"},
  {"do":"eval","js":"[...document.querySelectorAll('[role=dialog]')].pop().innerText","max":2600},
  dump("visualizar"),
  {"do":"press","key":"Escape","after":800},
  {"do":"click","target":{"selector":ROW},"optional":True,"after":800},
  {"do":"click","target":{"role":"menuitem","name":"Gerar link da proposta"},"optional":True,"after":1200},
  {"do":"shot","name":"47-link-gerado"},
  {"do":"eval","js":"(document.querySelector('[data-sonner-toaster]')||{}).innerText||'sem toast'","max":400},
  {"do":"text","selector":"main tbody","name":"tabela depois do link","max":1800},
  )
json.dump({"seedExtra":CHAIN,"start":"/dashboard","stopOnFail":False,"steps":S}, open('s2.json','w'), ensure_ascii=False, indent=1)
print(len(S),'passos (completo + criar)')
