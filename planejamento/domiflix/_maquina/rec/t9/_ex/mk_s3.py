import json
exec(open('mk_s2.py',encoding='utf8').read().split('S=[]')[0])   # DUMP, dump, dlg_text
def run(nome, steps, chain):
    json.dump({"seedExtra":chain,"start":"/dashboard","stopOnFail":False,"steps":steps}, open(nome,'w'), ensure_ascii=False, indent=1)
    print(nome, len(steps), 'passos')
C9 = ["t3/apos-cap10","t1/apos-cap13","t4/inicio","t4/apos-cap14","t5/inicio","t9/inicio","t9/_dev/apos-cap04","t9/_dev/apos-cap09"]
TOAST = {"do":"eval","js":"(document.querySelector('[data-sonner-toaster]')||{}).innerText||'sem toast'","max":400}
ROW = lambda nome: f"main tbody tr:has-text('{nome}') button[aria-haspopup='menu']"
LISTA = [{"do":"goto","url":"/orcamentos"},{"do":"waitFor","text":"Gerencie orçamentos, custos e precificação","timeout":20},{"do":"wait","ms":1200}]

# ---------------- S3a: Configurar Proposta + Visualizar + Gerar link
S=[]
S += LISTA
S += [
  {"do":"eval","js":"(()=>{try{sessionStorage.clear()}catch(e){}return 'ss limpo'})()"},
  {"do":"click","target":{"role":"button","name":"Configurar Proposta","exact":True},"after":1500},
  {"do":"shot","name":"50-config-modelo"},
  dump("config-modelo"),
  {"do":"text","selector":"[role=dialog]","name":"config etapa 1","max":1500},
  {"do":"hover","target":{"text":"Vanguarda","within":"[role=dialog]"},"optional":True,"after":500},
  {"do":"click","target":{"text":"Vanguarda","within":"[role=dialog]"},"optional":True,"after":900},
  {"do":"shot","name":"51-config-vanguarda"},
  {"do":"click","target":{"text":"Clean","within":"[role=dialog]"},"optional":True,"after":900},
  {"do":"shot","name":"52-config-clean"},
  {"do":"click","target":{"role":"button","name":"Próximo","exact":True},"after":1200},
  {"do":"shot","name":"53-config-personalizacao"},
  dump("config-personalizacao"),
  {"do":"text","selector":"[role=dialog]","name":"config etapa 2","max":3500},
  {"do":"eval","js":"(()=>{const s=document.querySelector('[role=dialog] [role=slider]');if(!s)return 'sem slider';const r=s.getBoundingClientRect();const t=s.parentElement.parentElement.getBoundingClientRect();return {thumb:[r.x,r.y,r.width,r.height].map(Math.round),track:[t.x,t.y,t.width,t.height].map(Math.round),val:s.getAttribute('aria-valuenow')}})()","max":300},
  {"do":"click","target":{"role":"slider","name":"Tamanho do logo"},"optional":True,"after":300},
  {"do":"press","key":"ArrowRight","times":2,"after":500},
  {"do":"eval","js":"document.querySelector('[role=dialog] [role=slider]').getAttribute('aria-valuenow')","max":50},
  {"do":"click","target":{"role":"switch","name":"Garantia"},"optional":True,"after":700},
  {"do":"shot","name":"54-config-garantia-ligada"},
  {"do":"keys","target":{"selector":"[role=dialog] textarea[placeholder*='Ex']","nth":3},"text":"Garantia de 90 dias sobre o serviço.","delay":15,"optional":True},
  {"do":"eval","js":"[...document.querySelectorAll('[role=dialog] textarea')].map(t=>[t.placeholder.slice(0,30),t.value.slice(0,40)].join('='))","max":900},
  {"do":"click","target":{"selector":"[role=dialog] div.rounded-lg:has-text('Garantia') button[aria-label='Mover para cima']"},"optional":True,"after":900},
  {"do":"eval","js":"[...document.querySelectorAll('[role=dialog] span.flex-1')].map(e=>e.innerText)","max":500},
  {"do":"shot","name":"55-config-garantia-subiu"},
  {"do":"click","target":{"role":"button","name":"Próximo","exact":True},"after":1500},
  {"do":"shot","name":"56-config-revisao"},
  dump("config-revisao"),
  {"do":"text","selector":"[role=dialog]","name":"config etapa 3","max":900},
  {"do":"click","target":{"role":"button","name":"Próxima página"},"optional":True,"after":800},
  {"do":"click","target":{"selector":"[role=dialog] button[aria-label*='róxim']"},"optional":True,"after":800},
  {"do":"shot","name":"57-config-pagina2"},
  {"do":"click","target":{"role":"button","name":"Salvar","exact":True,"within":"[role=dialog]"},"optional":True,"after":1200},
  TOAST,
  {"do":"shot","name":"58-config-salvo"},
  {"do":"eval","js":"[...document.querySelectorAll('[role=dialog] button')].filter(b=>b.getClientRects().length).slice(0,4).map(b=>[b.innerText.slice(0,20),b.getAttribute('aria-label'),Math.round(b.getBoundingClientRect().x),Math.round(b.getBoundingClientRect().y)].join('|'))","max":400},
  {"do":"press","key":"Escape","after":900},
  {"do":"eval","js":"document.querySelectorAll('[role=dialog]').length","max":20},
  # Visualizar
  {"do":"click","target":{"selector":ROW('Pousada Brisa do Mar')},"after":800},
  {"do":"click","target":{"role":"menuitem","name":"Visualizar"},"optional":True,"after":2200},
  {"do":"shot","name":"59-visualizar"},
  {"do":"eval","js":"[...document.querySelectorAll('[role=dialog]')].pop().innerText.slice(0,1500)","max":1800},
  dump("visualizar"),
  {"do":"press","key":"Escape","after":900},
  # Gerar link
  {"do":"click","target":{"selector":ROW('Pousada Brisa do Mar')},"after":800},
  {"do":"click","target":{"role":"menuitem","name":"Gerar link da proposta"},"optional":True,"after":1500},
  TOAST,
  {"do":"shot","name":"60-link-gerado"},
  {"do":"text","selector":"main tbody","name":"tabela depois do link","max":1800},
  {"do":"click","target":{"selector":ROW('Pousada Brisa do Mar')},"after":800},
  dump("menu-depois-link"),
  {"do":"press","key":"Escape","after":500},
]
run('s3a.json', S, C9)


TK9 = json.load(open('../cadeia.json'))['token9']
# ---------------- S3b: link -> página pública -> aprovar -> lista; indicador de visualização
S=[]
S += LISTA
S += [
  {"do":"click","target":{"selector":ROW('Pousada Brisa do Mar')},"after":800},
  {"do":"click","target":{"role":"menuitem","name":"Gerar link da proposta"},"optional":True,"after":1500},
  TOAST,
  {"do":"goto","url":f"/proposta/{TK9}?preview=1"},
  {"do":"wait","ms":2500},
  {"do":"shot","name":"70-publica-topo"},
  {"do":"text","selector":"body","name":"pública topo","max":3800},
  dump("publica-botoes"),
  {"do":"eval","js":"({h:document.documentElement.scrollHeight,vh:innerHeight,sc:[...document.querySelectorAll('*')].filter(e=>e.scrollHeight>e.clientHeight+40&&['auto','scroll'].includes(getComputedStyle(e).overflowY)).map(e=>[e.tagName,e.className.slice(0,40),e.scrollHeight,e.clientHeight].join('|')).slice(0,6)})","max":600},
  {"do":"wheel","x":640,"y":420,"dy":600,"after":900},
  {"do":"shot","name":"71-publica-meio1"},
  {"do":"wheel","x":640,"y":420,"dy":700,"after":900},
  {"do":"shot","name":"72-publica-meio2"},
  {"do":"wheel","x":640,"y":420,"dy":700,"after":900},
  {"do":"shot","name":"73-publica-meio3"},
  {"do":"wheel","x":640,"y":420,"dy":1500,"after":900},
  {"do":"shot","name":"74-publica-fim"},
  dump("publica-fim"),
  {"do":"eval","js":"[...document.querySelectorAll('button')].filter(b=>b.getClientRects().length).map(b=>[b.innerText.trim().slice(0,24),Math.round(b.getBoundingClientRect().x),Math.round(b.getBoundingClientRect().y),Math.round(b.getBoundingClientRect().width),Math.round(b.getBoundingClientRect().height)].join('|'))","max":600},
  {"do":"click","target":{"role":"button","name":"Aprovar","exact":True},"optional":True,"after":1500},
  {"do":"shot","name":"75-publica-aprovada"},
  {"do":"text","selector":"body","name":"pública depois de aprovar","max":600},
  {"do":"goto","url":"/orcamentos"},
  {"do":"waitFor","text":"Gerencie orçamentos, custos e precificação","timeout":20},
  {"do":"wait","ms":1500},
  {"do":"shot","name":"76-lista-aprovado"},
  {"do":"text","selector":"main tbody","name":"lista depois de aprovar","max":3200},
  # indicador de visualização
  {"do":"html","selector":"main tbody tr:has-text('Hotel Mirante do Mar') td:nth-child(2)","max":1600},
  {"do":"hover","target":{"selector":"main tbody tr:has-text('Hotel Mirante do Mar') td:nth-child(2) [title], main tbody tr:has-text('Hotel Mirante do Mar') td:nth-child(2) svg"},"optional":True,"after":1000},
  {"do":"shot","name":"77-hover-visualizacoes"},
  {"do":"eval","js":"[...document.querySelectorAll('[role=tooltip]')].map(e=>e.innerText)","max":300},
  {"do":"html","selector":"main tbody tr:has-text('Casa de Repouso') td:nth-child(2)","max":1200},
  {"do":"click","target":{"selector":ROW('Hotel Mirante do Mar')},"after":800},
  {"do":"shot","name":"78-menu-hotel"},
  dump("menu-hotel"),
  {"do":"press","key":"Escape","after":500},
]
run('s3b.json', S, C9)

# ---------------- S3c: aprovar por dentro (#2) e Gerar OS (#9)
S=[]
S += LISTA
S += [
  {"do":"click","target":{"selector":ROW('Hotel Mirante do Mar')},"after":800},
  {"do":"click","target":{"role":"menuitem","name":"Aprovar orçamento"},"optional":True,"after":1500},
  {"do":"shot","name":"80-aprovar-hotel"},
  dump("aprovar-modal"),
  {"do":"eval","js":"[...document.querySelectorAll('[role=dialog]')].pop().innerText.slice(0,2200)","max":2300},
  {"do":"click","target":{"role":"button","name":"Já recebi"},"optional":True,"after":900},
  {"do":"shot","name":"81-ja-recebi"},
  {"do":"eval","js":"[...document.querySelectorAll('[role=dialog]')].pop().innerText.slice(0,2200)","max":2300},
  dump("ja-recebi"),
  {"do":"click","target":{"role":"button","name":"Vou receber depois"},"optional":True,"after":900},
  {"do":"shot","name":"82-vou-receber"},
  dump("vou-receber"),
  {"do":"eval","js":"[...document.querySelectorAll('[role=dialog] button')].filter(b=>/\\d{2}\\/\\d{2}\\/\\d{4}|dd\\/mm/.test(b.innerText)).map(b=>[b.innerText,Math.round(b.getBoundingClientRect().y)].join('|'))","max":300},
]
run('s3c.json', S, C9)

S += [
  {"do":"click","target":{"selector":"[role=dialog] button:has-text('03/11/2026')"},"optional":True,"after":900},
  {"do":"shot","name":"83-calendario-venc"},
  {"do":"click","target":{"role":"gridcell","name":"20","exact":True},"optional":True,"after":900},
  {"do":"shot","name":"84-venc-20"},
  {"do":"eval","js":"[...document.querySelectorAll('[role=dialog]')].pop().innerText.slice(0,2400)","max":2500},
  {"do":"click","target":{"role":"button","name":"Aprovar e gerar conta a receber"},"optional":True,"after":1800},
  TOAST,
  {"do":"shot","name":"85-hotel-aprovado"},
  {"do":"text","selector":"main tbody","name":"lista depois do hotel","max":3200},
  {"do":"click","target":{"selector":ROW('Hotel Mirante do Mar')},"after":800},
  dump("menu-hotel-aprovado"),
  {"do":"press","key":"Escape","after":500},
  # Pousada (#9): aprovar por dentro só para poder gerar a OS
  {"do":"click","target":{"selector":ROW('Pousada Brisa do Mar')},"after":800},
  {"do":"click","target":{"role":"menuitem","name":"Aprovar orçamento"},"optional":True,"after":1500},
  {"do":"click","target":{"role":"button","name":"Aprovar e gerar conta a receber"},"optional":True,"after":1800},
  TOAST,
  {"do":"click","target":{"selector":ROW('Pousada Brisa do Mar')},"after":800},
  dump("menu-pousada-aprovada"),
  {"do":"click","target":{"role":"menuitem","name":"Gerar OS"},"optional":True,"after":1500},
  {"do":"shot","name":"86-distribuir"},
  dump("distribuir"),
  {"do":"eval","js":"[...document.querySelectorAll('[role=dialog]')].pop().innerText.slice(0,2400)","max":2500},
  {"do":"click","target":{"role":"button","name":"Todos"},"optional":True,"after":800},
  {"do":"shot","name":"87-distribuir-todos"},
  dump("distribuir-todos"),
  ]
run('s3c.json', S, C9)

# ---------------- S3d: distribuição completa + OS gerada + lista de OS (parte da S3c, em continuação não é possível: nova sessão refaz o caminho)

# ---------------- S4: cap03 (Custos Globais: criar a Van 01 com digitação real)
BASE = ["t3/apos-cap10","t1/apos-cap13","t4/inicio","t4/apos-cap14","t5/inicio","t9/inicio"]
TAB = lambda n: {"do":"click","target":{"role":"tab","name":n},"after":1200}
S=[]
S += LISTA
S += [
  TAB("Custos Globais"),
  {"do":"click","target":{"role":"button","name":"Novo Recurso"},"after":1000},
  {"do":"click","target":{"role":"button","name":"Veículos","exact":True},"after":1200},
  {"do":"shot","name":"90-veiculo-vazio"},
  {"do":"keys","target":{"placeholder":"Ex: Spin 2024"},"text":"Van 01","delay":60},
  {"do":"keys","target":{"selector":"[role=dialog] input[type=text]","nth":1},"text":"176","clear":True,"delay":60},
  {"do":"keys","target":{"selector":"[role=dialog] input[placeholder='Valor mensal']","nth":0},"text":"1400","delay":60},
  {"do":"keys","target":{"selector":"[role=dialog] input[placeholder='Valor mensal']","nth":1},"text":"1620","delay":60},
  {"do":"keys","target":{"selector":"[role=dialog] input[placeholder='Valor anual']","nth":0},"text":"3600","clear":True,"delay":60},
  {"do":"keys","target":{"selector":"[role=dialog] input[placeholder='Valor anual']","nth":1},"text":"2400","clear":True,"delay":60},
  {"do":"eval","js":"[...document.querySelectorAll('[role=dialog] input')].filter(i=>i.type!=='file').map(i=>[i.placeholder.slice(0,22),i.value].join('='))","max":700},
  {"do":"eval","js":"[...document.querySelectorAll('[role=dialog] button#annual-0,[role=dialog] button#annual-1,[role=dialog] button#annual-2,[role=dialog] button#annual-3')].map(b=>[b.id,b.getAttribute('aria-checked'),b.getAttribute('data-state'),b.getAttribute('role'),b.getAttribute('aria-label'),b.title].join('|'))","max":600},
  {"do":"eval","js":"(()=>{const d=document.querySelector('[role=dialog]');const sc=[...d.querySelectorAll('*')].filter(e=>e.scrollHeight>e.clientHeight+20&&['auto','scroll'].includes(getComputedStyle(e).overflowY));return sc.map(e=>[e.tagName,e.className.slice(0,60),e.scrollHeight,e.clientHeight].join('|'))})()","max":500},
  {"do":"text","selector":"[role=dialog]","name":"veiculo preenchido","max":2200},
  {"do":"shot","name":"91-veiculo-preenchido"},
  {"do":"click","target":{"role":"button","name":"Salvar","exact":True,"within":"[role=dialog]"},"after":1800},
  {"do":"shot","name":"92-van-salva"},
  TOAST,
  {"do":"text","selector":"main","name":"custos globais com a van","max":1800},
  {"do":"click","target":{"text":"Van 01","exact":True,"within":"main"},"after":1200},
  {"do":"shot","name":"93-van-detalhe"},
  {"do":"text","selector":"main","name":"detalhe da van","max":2200},
]
run('s4.json', S, BASE)

# ---------------- S5: cap04 (Custos dos Serviços), a partir do estado depois do cap03
S=[]
S += LISTA
S += [
  TAB("Custos dos Serviços"),
  {"do":"shot","name":"100-custos-servicos"},
  {"do":"text","selector":"main","name":"custos dos serviços (inicial)","max":2200},
  dump("custos-servicos"),
  {"do":"click","target":{"role":"combobox","within":"main"},"optional":True,"after":900},
  {"do":"shot","name":"101-tipos-lista"},
  dump("tipos-lista"),
  {"do":"click","target":{"role":"option","name":"Higienização de Split"},"optional":True,"after":900},
  {"do":"shot","name":"102-higienizacao"},
  dump("mao-de-obra"),
  {"do":"keys","target":{"selector":"main input[type=number]","nth":0},"text":"32","clear":True,"delay":60,"optional":True},
  {"do":"keys","target":{"selector":"main input[type=number]","nth":1},"text":"1,5","clear":True,"delay":60,"optional":True},
  {"do":"eval","js":"[...document.querySelectorAll('main input')].filter(i=>i.getClientRects().length).map(i=>[i.type,i.placeholder.slice(0,20),i.value].join('|'))","max":500},
  {"do":"wait","ms":1500},
  {"do":"shot","name":"103-mao-de-obra-preenchida"},
  {"do":"text","selector":"main","name":"mão de obra preenchida","max":2600},
  {"do":"click","target":{"role":"button","name":"Calcular"},"optional":True,"after":1500},
  {"do":"shot","name":"104-calculadora"},
  dump("calculadora"),
  {"do":"eval","js":"[...document.querySelectorAll('[role=dialog]')].pop().innerText.slice(0,2600)","max":2700},
  {"do":"click","target":{"role":"button","name":"Cancelar","within":"[role=dialog]"},"optional":True,"after":900},
  {"do":"click","target":{"role":"tab","name":"Recursos"},"optional":True,"after":1200},
  {"do":"shot","name":"105-recursos"},
  dump("recursos"),
  {"do":"eval","js":"document.querySelector('main').innerText.slice(0,1800)","max":1900},
  {"do":"click","target":{"text":"Van 01","exact":True,"within":"main"},"optional":True,"after":1000},
  {"do":"shot","name":"106-van-marcada"},
  {"do":"eval","js":"document.querySelector('main').innerText.slice(0,1800)","max":1900},
  {"do":"click","target":{"role":"tab","name":"Materiais"},"optional":True,"after":1200},
  {"do":"shot","name":"107-materiais"},
  dump("materiais"),
  {"do":"click","target":{"role":"combobox","name":"Selecione do estoque"},"optional":True,"after":900},
  {"do":"shot","name":"108-estoque-lista"},
  dump("estoque-lista"),
  {"do":"click","target":{"role":"option","name":"Limpa-evaporador em spray"},"optional":True,"after":900},
  {"do":"shot","name":"109-limpa-escolhido"},
  dump("limpa-escolhido"),
  ]
run('s5.json', S, BASE+["t9/_dev/apos-cap03"])

# ---------------- S1b: o filtro de Status (folha lateral) depois do clique em "Em Aberto"
S=[]
S += LISTA
S += [
  {"do":"click","target":{"selector":"main .grid > *","nth":0},"after":1000},
  {"do":"click","target":{"role":"button","name":"Filtros, 1 ativo"},"after":1200},
  {"do":"shot","name":"110-filtro-aberto"},
  dump("filtro-aberto"),
  {"do":"eval","js":"[...document.querySelectorAll('[role=dialog]')].pop().innerText.slice(0,800)","max":900},
  {"do":"click","target":{"role":"button","name":"Enviado","exact":True,"within":"[role=dialog]"},"after":1000},
  {"do":"shot","name":"111-filtro-desmarcado"},
  dump("filtro-desmarcado"),
  {"do":"press","key":"Escape","after":900},
  {"do":"shot","name":"112-filtro-fechado"},
  {"do":"text","selector":"main tbody","name":"lista inteira","max":300},
  # menu da linha (itens), com a lista cheia
  {"do":"click","target":{"selector":"main tbody tr:has-text('Hotel Mirante do Mar') button[aria-haspopup='menu']"},"after":800},
  {"do":"shot","name":"113-menu-hotel"},
  dump("menu-hotel-enviado"),
  {"do":"press","key":"Escape","after":600},
  {"do":"click","target":{"role":"button","name":"Novo Orçamento","exact":True},"after":1500},
  {"do":"shot","name":"114-wizard-aberto"},
  {"do":"eval","js":"[...document.querySelectorAll('[role=dialog]')].pop().innerText.slice(0,900)","max":1000},
  dump("wizard-etapa1"),
  ]
run('s1b.json', S, BASE)
