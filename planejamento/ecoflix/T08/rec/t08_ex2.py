#!/usr/bin/env python3
"""T08 · explorações do app 1.60.10 (18/11): e5 = seleção em conjunto, lista/exportar, lixeira, ticket com valores, pesagem avulsa
com cobrança e Configurações > Usabilidade; e6 = sem internet. Uso: python3 -I rec/t08/t08_ex2.py"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
def dump(esc='body', n=140):
    return ("(()=>{const out=[];const root=document.querySelectorAll(%s);const vis=e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height>0&&r.bottom>0&&r.top<800};"
            "for(const R of root)for(const e of R.querySelectorAll('button,a,input,textarea,[role=tab],[role=switch],[role=combobox],[role=radio],[role=option],[role=menuitem],[role=checkbox],h1,h2,h3,label,th')){if(!vis(e))continue;const r=e.getBoundingClientRect();"
            "const t=(e.innerText||e.value||'').trim().replace(/\\s+/g,' ').slice(0,48);const a=[e.tagName.toLowerCase()+(e.getAttribute('role')?'['+e.getAttribute('role')+']':''),t];"
            "for(const k of ['aria-label','placeholder','title','data-state','aria-checked','aria-pressed','type','id'])if(e.getAttribute(k))a.push(k.slice(0,4)+'='+e.getAttribute(k).slice(0,30));"
            "a.push(Math.round(r.x)+','+Math.round(r.y)+','+Math.round(r.width)+'x'+Math.round(r.height));out.push(a.join('|'))}return out.slice(0,%d)})()") % (json.dumps(esc), n)
DLG = '[role=dialog]'
POP = '[data-radix-popper-content-wrapper]'
def ev(js, mx=6000): return {'do': 'eval', 'js': js, 'max': mx}
def opt(d): d['optional'] = True; return d
def txt(sel, n=1500):
    return ev("(()=>{const e=[...document.querySelectorAll(%s)].pop();return e?e.innerText.replace(/\\s+/g,' ').slice(0,%d):'SEM'})()" % (json.dumps(sel), n), n + 40)
W = lambda ms: {'do': 'wait', 'ms': ms}
S = lambda n: {'do': 'shot', 'name': n}
CK = lambda t, **k: opt({'do': 'click', 'target': t, **k})
B = lambda n: {'role': 'button', 'name': n}
C = lambda rot: {'selector': f"[role=dialog] div:has(> label:has-text('{rot}')) input"}
CARTAO = lambda n: (f"main div.rounded-lg:has([aria-label='Selecionar ticket #{n}']):not(:has(div.rounded-lg [aria-label='Selecionar ticket #{n}']))")
ACOES = lambda n: {'role': 'button', 'name': 'Ações', 'within': CARTAO(n)}
POPS = "(()=>{const o=window.open;window.__pops=[];window.open=function(...a){const w=o.apply(this,a);window.__pops.push(w);return w};return 'ok'})()"
PDF = ("(async()=>{const w=(window.__pops||[]).slice(-1)[0];if(!w)return 'SEM JANELA';for(let i=0;i<40;i++){let f=null;"
       "try{f=w.document&&w.document.querySelector('#pdf-frame')}catch(e){return 'ERRO '+e}"
       "if(f&&f.src){const b=await (await fetch(f.src.split('#')[0])).blob();const u=new Uint8Array(await b.arrayBuffer());let s='';"
       "for(let k=0;k<u.length;k+=8192)s+=String.fromCharCode.apply(null,u.subarray(k,k+8192));return 'PDF:'+btoa(s)}"
       "await new Promise(r=>setTimeout(r,250))}return 'SEM PDF'})()")
ESTADO = lambda ts: ("(async()=>{const u='http://127.0.0.1:54340/__dev/state?table=';const o={};for(const t of %s)"
          "o[t]=await (await fetch(u+t)).json();return 'ESTADO '+JSON.stringify(o)})()") % json.dumps(ts)
SEEDS = ['base/balanca-ativada', 'base/caixa-aberto', 't08/inicio', 't08/apos-cap06']
LISTA = [{'do': 'goto', 'url': '/ticket-pesagem'}, {'do': 'waitFor', 'text': 'Gerencie tickets de pesagem rodoviária', 'timeout': 30}, W(1500)]
e5 = {'seedExtra': SEEDS, 'start': '/dashboard', 'stopOnFail': False, 'steps': [
    W(2500), ev(POPS), *LISTA, S('01-kanban'), txt('main', 1800), ev(dump('main'), 7000),
    CK({'selector': "[aria-label='Selecionar ticket #56']"}), CK({'selector': "[aria-label='Selecionar ticket #58']"}), W(600), S('02-selecao'), txt('body', 2200),
    ev("(()=>{const b=[...document.querySelectorAll('button')].find(x=>/Valorizar 2 tickets/.test(x.textContent));if(!b)return 'SEM BARRA';let e=b,o=[];for(let i=0;i<5&&e;i++){o.push(e.tagName+'.'+String(e.className).slice(0,80)+'|'+e.innerText.replace(/\\s+/g,' ').slice(0,80));e=e.parentElement}return o})()"),
    CK({'selector': "[aria-label='Selecionar ticket #57']"}), W(500), txt('body', 600),
    CK({'selector': "[aria-label='Selecionar ticket #57']"}), CK({'selector': "[aria-label='Selecionar ticket #56']"}), CK({'selector': "[aria-label='Selecionar ticket #58']"}), W(500),
    CK(ACOES(57)), W(500), ev(dump('[role=menu]'), 1500), {'do': 'press', 'key': 'Escape'},
    # lixeira
    ev("(()=>[...document.querySelectorAll('main button')].map(b=>(b.innerText||'').trim().slice(0,30)+'|'+(b.getAttribute('aria-label')||'')+'|'+(b.getAttribute('title')||'')).slice(0,40))()"),
    CK({'selector': "main button:has-text('Lixeira')"}), W(900), S('03-lixeira'), txt(DLG, 900), ev(dump(DLG), 2500), {'do': 'press', 'key': 'Escape'}, W(500),
    # lista
    CK({'role': 'radio', 'name': 'Lista'}), W(1200), S('04-lista'), txt('main', 1800), ev(dump('main'), 6000),
    CK(B('Filtros')), W(700), S('05-filtros'), txt(POP, 600), ev(dump(POP), 2500), {'do': 'press', 'key': 'Escape'}, W(400),
    CK(B('Exportar')), W(700), S('06-exportar'), ev(dump('[role=menu]'), 1500),
    CK({'role': 'menuitem', 'name': 'PDF'}), W(900), S('07-exportar-pdf'), txt(DLG, 900), ev(dump(DLG), 3000), {'do': 'press', 'key': 'Escape'}, W(500),
    CK({'role': 'radio', 'name': 'Kanban'}), W(800),
    # ticket com valores (aba do Jair)
    CK({'text': 'Rascunhos abertos'}), W(2500), S('10-jair'), txt('main', 1200),
    CK(B('Com valores')), W(1500), S('11-com-valores'), txt('main', 1800), ev(dump('main'), 7000),
    CK({'selector': "main button[aria-label='Ações do item']"}), W(600), ev(dump('[role=menu]'), 1500),
    CK({'role': 'menuitem', 'name': 'Adicionar tara / pesagem avançada'}), W(1200), S('12-avancada-valores'), txt(DLG, 1200),
    opt({'do': 'keys', 'target': C('1ª Pesagem'), 'text': '5640'}), opt({'do': 'keys', 'target': C('2ª Pesagem'), 'text': '4180'}), W(700), S('13-avancada-2a'), txt(DLG, 1200), ev(dump(DLG), 5000),
    CK(B('Confirmar')), W(1500), S('14-item-valores'), txt('main', 2000),
    {'do': 'wheel', 'x': 700, 'y': 500, 'dy': 500}, S('15-total'), ev(ESTADO(['weighing_tickets']), 6000),
    CK(B('Salvar Ticket de Pesagem')), W(2500), S('16-salvo-59'), txt(DLG, 600), txt('body', 500), ev(dump(DLG), 2000),
    CK({'role': 'button', 'name': 'Fechar', 'exact': True, 'within': DLG, 'nth': 0}), W(800),
    CK(B('Voltar')), W(2000), S('17-kanban-59'), txt('main', 2200),
    # pesagem avulsa
    CK({'role': 'tab', 'name': 'Pesagens avulsas'}), W(900), CK(B('Nova Pesagem Avulsa')), W(2500), S('20-avulsa'), txt('main', 1800), ev(dump('main'), 8000),
    CK({'text': 'Selecionar cliente'}), W(900), S('21-busca'), txt(DLG, 900), ev(dump(DLG), 4000),
    opt({'do': 'keys', 'target': {'selector': '[role=dialog] input'}, 'text': 'Areal Boa Vista'}), W(900), S('22-busca-vazia'), txt(DLG, 600), ev(dump(DLG), 2500),
    CK({'selector': "[role=dialog] button:has-text('Cadastrar «')"}), W(1500), S('23-cadastro-rapido'), txt(DLG, 1500), ev(dump(DLG), 6000),
    ev("(()=>[...document.querySelectorAll('[role=dialog]')].map(d=>d.querySelector('h2')?.innerText))()"),
    CK({'selector': "[role=dialog] button[type=submit]"}), W(2000), S('24-depois-cadastro'), txt('body', 500), txt('main', 900),
    opt({'do': 'keys', 'target': {'placeholder': 'Ex.: Areia, terra, entulho'}, 'text': 'Areia média'}), W(500),
    CK(B('Pesagem avançada')), W(1200), S('25-avancada-avulsa'), txt(DLG, 1200),
    opt({'do': 'keys', 'target': C('1ª Pesagem'), 'text': '23840'}), opt({'do': 'keys', 'target': C('2ª Pesagem'), 'text': '9120'}), W(700), txt(DLG, 900),
    CK(B('Confirmar')), W(1500), S('26-item-avulsa'), txt('main', 1800),
    {'do': 'wheel', 'x': 700, 'y': 500, 'dy': 300},
    opt({'do': 'keys', 'target': {'placeholder': 'Digite ou busque a placa'}, 'text': 'HBN3F27'}), W(900), S('27-placa'), ev(dump(POP), 2000), ev(dump('[role=listbox]'), 1500),
    {'do': 'press', 'key': 'Tab'}, W(500),
    opt({'do': 'keys', 'target': {'selector': '#standalone-vehicle-type'}, 'text': 'Caçamba'}),
    opt({'do': 'keys', 'target': {'selector': '#standalone-weighing-fee'}, 'text': '6000'}), W(600), S('28-valor'), txt('main', 2000),
    ev("(()=>[...document.querySelectorAll('main input')].map(e=>(e.id||e.placeholder||'?')+'='+e.value))()"),
    CK(B('Salvar Pesagem Avulsa')), W(2000), S('29-pagamento'), txt(DLG, 1500), ev(dump(DLG), 6000), txt('body', 300),
    CK({'text': 'Dinheiro', 'within': DLG}), W(900), S('30-dinheiro'), txt(DLG, 1500), ev(dump(DLG), 6000),
    CK({'text': 'Dinheiro', 'within': DLG}), W(500),
    CK({'text': 'Pix/Transferência', 'within': DLG}), W(900), S('31-pix'), txt(DLG, 1500), ev(dump(DLG), 6000),
    CK(B('CONFIRMAR PAGAMENTO')), W(3000), S('32-salvo-avulsa'), txt(DLG, 700), txt('body', 500), ev(dump(DLG), 2000),
    ev(ESTADO(['weighing_tickets', 'bank_transactions', 'financial_categories', 'customers']), 400), 
    ev("(async()=>{const u='http://127.0.0.1:54340/__dev/state?table=';const w=(await (await fetch(u+'weighing_tickets')).json()).filter(t=>t.ticket_kind==='standalone');const b=(await (await fetch(u+'bank_transactions')).json()).filter(t=>/pesagem/i.test(t.description||''));const c=(await (await fetch(u+'customers')).json()).filter(t=>/Areal/.test(t.name));return JSON.stringify({w,b,c})})()", 5000),
    CK({'role': 'button', 'name': 'Imprimir comprovante', 'within': DLG}), W(1000), S('33-formato'), txt(DLG, 500),
    CK({'text': 'Térmico', 'within': DLG}), W(4000), ev(PDF, 200000), S('34-depois-termico'), txt('body', 400),
    CK({'role': 'button', 'name': 'Fechar', 'exact': True, 'within': DLG, 'nth': 0}), W(800), {'do': 'press', 'key': 'Escape'},
    CK(B('Voltar')), W(2000), S('35-avulsas'), txt('main', 1800), ev(dump('main'), 5000),
    CK({'selector': "main button:has-text('Ações')"}), W(600), S('36-acoes-avulsa'), ev(dump('[role=menu]'), 1500),
    CK({'role': 'menuitem', 'name': 'Editar'}), W(2500), S('37-editar-avulsa'), txt('main', 2000),
    {'do': 'wheel', 'x': 700, 'y': 500, 'dy': 300}, S('38-editar-avulsa-baixo'),
    # configurações
    {'do': 'goto', 'url': '/configuracoes?tab=usability'}, W(3000), S('40-usabilidade'), txt('main', 6000),
    ev("(()=>{const e=[...document.querySelectorAll('main *')].find(x=>x.children.length===0&&x.textContent.trim()==='Assinaturas no comprovante');if(!e)return 'SEM';e.scrollIntoView({block:'center'});return 'ok'})()"),
    W(600), S('41-assinaturas'), ev(dump('main'), 7000),
    ev("(()=>{const e=[...document.querySelectorAll('main *')].find(x=>x.children.length===0&&x.textContent.trim()==='Assinaturas no comprovante');let c=e;for(let i=0;i<6&&c;i++){const s=c.querySelector('[role=switch]');if(s){s.click();return 'clicou '+i}c=c.parentElement}return 'SEM SWITCH'})()"),
    W(1500), S('42-assinaturas-ligada'), txt('body', 300), ev(dump('main'), 7000),
    CK({'selector': "main button[role=combobox]:near(:text('Quem assina'))"}), W(700), S('43-quem-assina'), ev(dump('[role=listbox]'), 1500), {'do': 'press', 'key': 'Escape'},
    ev("(()=>{const e=[...document.querySelectorAll('main *')].find(x=>x.children.length===0&&x.textContent.trim()==='Permitir forma de pagamento no ticket de pesagem');if(!e)return 'SEM';e.scrollIntoView({block:'center'});return 'ok'})()"),
    W(600), S('44-forma-pagamento'),
]}
os.makedirs(os.path.join(HERE, '_ex'), exist_ok=True)
json.dump(e5, open(os.path.join(HERE, '_ex', 'e5.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print('e5', len(e5['steps']))

# ---------------------------------------------------------------- e6: o que a e5 não fechou + sem internet
OFF = ("(()=>{const of=window.fetch;window.fetch=function(u,...a){const s=String((u&&u.url)||u);if(s.includes('/auth/v1/health'))return Promise.reject(new TypeError('Failed to fetch'));"
       "return of.call(this,u,...a)};Object.defineProperty(navigator,'onLine',{configurable:true,get:()=>false});window.dispatchEvent(new Event('offline'));return 'offline'})()")
SELEC = lambda n: {'text': 'Selecionar', 'exact': True, 'within': CARTAO(n)}
MAT = {'placeholder': 'Escreva o nome ou código do material'}
e6 = {'seedExtra': SEEDS, 'start': '/dashboard', 'stopOnFail': False, 'steps': [
    W(2500), *LISTA,
    CK(SELEC(56)), CK(SELEC(58)), W(700), S('01-dois'), txt('body', 2400),
    ev("(()=>{const b=[...document.querySelectorAll('button')].find(x=>/Valorizar 2 tickets/.test(x.textContent));if(!b)return 'SEM BARRA';let e=b,o=[];for(let i=0;i<5&&e;i++){o.push(e.tagName+'.'+String(e.className).slice(0,90)+'|'+e.innerText.replace(/\\s+/g,' ').slice(0,80));e=e.parentElement}return o})()"),
    ev(dump('body > div, main ~ div', 60), 5000),
    CK({'selector': "button[aria-label='Limpar seleção']"}), W(500), txt('body', 300),
    ev("(()=>[...document.querySelectorAll('button')].filter(b=>{const r=b.getBoundingClientRect();return r.top>700&&r.left>600&&r.left<1100}).map(b=>b.outerHTML.slice(0,200)))()"),
    CK(ACOES(57)), W(500), S('02-acoes57'), ev(dump('[role=menu]'), 1500), {'do': 'press', 'key': 'Escape'}, W(300),
    CK(B('Rascunhos apagados 1')), CK({'selector': "main button:has-text('Rascunhos apagados')"}), W(900), S('03-lixeira'), txt(DLG, 900), ev(dump(DLG), 2500), {'do': 'press', 'key': 'Escape'}, W(500),
    # cap02: janela do fornecedor (pino, Não informado) e Gerenciar motoristas
    CK(B('Novo Ticket de Pesagem')), W(2500), CK({'text': 'Selecionar fornecedor'}), W(900), S('04-fornecedor'), ev(dump(DLG), 5000),
    ev("(()=>[...document.querySelectorAll('[role=dialog] button')].slice(0,12).map(b=>b.outerHTML.replace(/<svg.*?<\\/svg>/g,'<svg/>').slice(0,260)))()", 4000),
    CK({'text': 'Cooperativa Recomeço', 'within': DLG}), W(800),
    opt({'do': 'keys', 'target': MAT, 'text': 'latinha'}), W(600), {'do': 'press', 'key': 'Enter'}, W(800),
    {'do': 'wheel', 'x': 700, 'y': 460, 'dy': 120},
    CK({'placeholder': 'Digite ou busque o motorista'}), W(900), S('05-motoristas'), ev(dump(POP), 2500), ev(dump('[role=listbox]'), 2500),
    ev("(()=>[...document.querySelectorAll('button,[role=option]')].filter(b=>/Gerenciar/.test(b.textContent)&&b.textContent.length<40).map(b=>b.outerHTML.slice(0,220)))()"),
    {'do': 'press', 'key': 'Escape'}, W(300),
    # sem internet nesta aba (o ticket offline é descartado)
    ev(OFF), W(12000), S('06-offline-form'), txt('main', 1500), txt('body', 500),
    CK(B('Pesagem avançada')), W(1000), opt({'do': 'keys', 'target': C('1ª Pesagem'), 'text': '7210'}), CK(B('Confirmar')), W(1200),
    CK(B('Salvar Ticket de Pesagem')), W(3000), S('07-offline-salvo'), txt(DLG, 900), txt('body', 500), ev(dump(DLG), 2500),
    CK({'role': 'button', 'name': 'Fechar', 'exact': True, 'within': DLG, 'nth': 0}), W(600),
    CK(B('Voltar')), W(2500), S('08-offline-lista'), txt('main', 1500), ev(dump('main'), 4000),
    CK(ACOES(58)), W(500), S('09-offline-acoes'), ev(dump('[role=menu]'), 1500), {'do': 'press', 'key': 'Escape'},
    # volta a internet: recarrega (o ticket offline sobe?) e segue para o ticket com valores
    {'do': 'goto', 'url': '/ticket-pesagem'}, W(6000), S('10-de-volta'), txt('main', 1500),
    ev("(async()=>{const u='http://127.0.0.1:54340/__dev/state?table=';const w=(await (await fetch(u+'weighing_tickets')).json());return JSON.stringify(w.map(t=>[t.ticket_number,t.status,t.customer_supplier_name,t.deleted_at,(t.items||[]).map(i=>i.quantity)]))})()", 3000),
    CK({'text': 'Rascunhos abertos'}), W(2500), S('11-rascunhos'), txt('main', 900),
    ev("(()=>[...document.querySelectorAll('main button[aria-expanded]')].map(b=>b.innerText.replace(/\\s+/g,' ')))()"),
]}
json.dump(e6, open(os.path.join(HERE, '_ex', 'e6.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
# ---------------------------------------------------------------- e7: ticket com valores (preço digitado) e pesagem avulsa até o PDF e o Editar
e7 = {'seedExtra': SEEDS, 'start': '/dashboard', 'stopOnFail': False, 'steps': [
    W(2500), *LISTA,
    CK({'text': 'Rascunhos abertos'}), W(2500), CK(B('Com valores')), W(1500),
    CK({'selector': "main button[aria-label='Ações do item']"}), W(600), CK({'role': 'menuitem', 'name': 'Adicionar tara / pesagem avançada'}), W(1200),
    opt({'do': 'keys', 'target': C('1ª Pesagem'), 'text': '5640'}), opt({'do': 'keys', 'target': C('2ª Pesagem'), 'text': '4180'}),
    opt({'do': 'keys', 'target': C('Valor/Kg'), 'text': '3,40'}), W(800), S('01-avancada-preco'), txt(DLG, 1200),
    CK(B('Confirmar')), W(1500), S('02-item-valores'), txt('main', 2000), txt('body', 300),
    {'do': 'wheel', 'x': 700, 'y': 500, 'dy': 400}, W(500), S('03-total'),
    ev("(()=>{const e=[...document.querySelectorAll('main *')].find(x=>x.children.length<3&&/^Total geral/.test(x.textContent.trim()));return e?e.outerHTML.slice(0,300):'SEM'})()"),
    CK(B('Salvar Ticket de Pesagem')), W(2500), S('04-salvo-59'), txt(DLG, 600),
    CK({'role': 'button', 'name': 'Fechar', 'exact': True, 'within': DLG, 'nth': 0}), W(800), CK(B('Voltar')), W(2000), S('05-kanban-59'), txt('main', 1200),
    ev("(async()=>{const u='http://127.0.0.1:54340/__dev/state?table=';const w=(await (await fetch(u+'weighing_tickets')).json()).filter(t=>t.ticket_number===59);return JSON.stringify(w)})()", 3000),
    CK({'role': 'tab', 'name': 'Pesagens avulsas'}), W(900), S('06-avulsas-vazia'), CK(B('Nova Pesagem Avulsa')), W(2500),
    CK({'text': 'Selecionar cliente'}), W(900), opt({'do': 'keys', 'target': {'selector': '[role=dialog] input'}, 'text': 'Areal Boa Vista'}), W(900),
    CK({'selector': "[role=dialog] button:has-text('Cadastrar «')"}), W(1500), CK({'selector': "[role=dialog] button[type=submit]"}), W(2500), S('07-cliente'), txt('body', 200),
    opt({'do': 'keys', 'target': {'placeholder': 'Ex.: Areia, terra, entulho'}, 'text': 'Areia média'}), W(500),
    CK(B('Pesagem avançada')), W(1200), opt({'do': 'keys', 'target': C('1ª Pesagem'), 'text': '23840'}), opt({'do': 'keys', 'target': C('2ª Pesagem'), 'text': '9120'}),
    CK({'text': 'Completo', 'within': DLG}), CK(B('Confirmar')), W(1500),
    {'do': 'wheel', 'x': 700, 'y': 500, 'dy': 300},
    opt({'do': 'keys', 'target': {'placeholder': 'Digite ou busque a placa'}, 'text': 'HBN3F27'}), W(900), {'do': 'press', 'key': 'Tab'}, W(400),
    opt({'do': 'keys', 'target': {'selector': '#standalone-vehicle-type'}, 'text': 'Caçamba'}),
    opt({'do': 'keys', 'target': {'selector': '#standalone-weighing-fee'}, 'text': '60'}), {'do': 'press', 'key': 'Tab'}, W(600), S('08-valor'),
    ev("(()=>[...document.querySelectorAll('main input')].map(e=>(e.id||e.placeholder||'?')+'='+e.value))()"),
    CK(B('Salvar Pesagem Avulsa')), W(2000), S('09-pagamento'), txt(DLG, 600),
    CK({'text': 'Dinheiro', 'within': DLG}), W(1200), S('10-dinheiro'), txt(DLG, 800), ev(dump(DLG), 4000),
    CK({'text': 'Pix/Transferência', 'within': DLG}), W(900), S('11-pix'), txt(DLG, 800),
    CK(B('CONFIRMAR PAGAMENTO')), W(3000), S('12-salvo-avulsa'), txt(DLG, 500), txt('body', 200),
    ev(POPS), CK({'role': 'button', 'name': 'Imprimir comprovante', 'within': DLG}), W(1000),
    CK({'text': 'Térmico', 'within': DLG}), W(4000), ev(PDF, 400000), S('13-depois-termico'), txt('body', 300), ev(dump(DLG), 1500),
    {'do': 'press', 'key': 'Escape'}, W(500), CK({'role': 'button', 'name': 'Fechar', 'exact': True, 'within': DLG, 'nth': 0}), W(500),
    CK(B('Voltar')), W(2000), S('14-avulsas'), txt('main', 900),
    CK({'selector': "main tbody tr td:last-child button"}), W(600), S('15-acoes-avulsa'), ev(dump('[role=menu]'), 1500),
    CK({'role': 'menuitem', 'name': 'Editar'}), W(2500), S('16-editar-avulsa'), txt('main', 1500),
    {'do': 'wheel', 'x': 700, 'y': 500, 'dy': 300}, W(500), S('17-editar-avulsa-baixo'),
    ev("(()=>{const e=[...document.querySelectorAll('main p')].find(x=>/Cobrança já lançada/.test(x.textContent));return e?e.innerText:'SEM AVISO'})()"),
    CK(B('Voltar')), W(1500),
    CK({'selector': "main tbody tr td:last-child button"}), W(600), CK({'role': 'menuitem', 'name': 'Excluir'}), W(900), S('18-excluir'), txt('[role=alertdialog]', 500),
    ev("(()=>[...document.querySelectorAll('[role=alertdialog] button')].map(b=>b.innerText))()"),
    ev("(async()=>{const u='http://127.0.0.1:54340/__dev/state?table=';const f=async(t)=>await (await fetch(u+t)).json();const w=(await f('weighing_tickets')).filter(t=>t.ticket_kind==='standalone');const b=(await f('bank_transactions')).filter(t=>/pesagem/i.test(t.description||''));const c=(await f('financial_categories')).filter(t=>/pesagem/i.test(t.name));return JSON.stringify({w,b,c})})()", 6000),
]}
json.dump(e7, open(os.path.join(HERE, '_ex', 'e7.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print('e6', len(e6['steps']), 'e7', len(e7['steps']))

# ---------------------------------------------------------------- e8: seleção em conjunto (por que o 2º clique falha), filtro Status, botões "+" e salvar sem internet
PT = lambda n: ("(()=>{const e=document.querySelector(\"[aria-label='Selecionar ticket #%d']\");if(!e)return 'SEM';const r=e.getBoundingClientRect();const t=document.elementFromPoint(r.x+8,r.y+8);"
                "return [Math.round(r.x),Math.round(r.y),e.disabled,t&&t.outerHTML.slice(0,160),getComputedStyle(e).pointerEvents]})()") % n
e8 = {'seedExtra': SEEDS, 'start': '/dashboard', 'stopOnFail': False, 'steps': [
    W(2500), *LISTA,
    CK({'selector': "[aria-label='Selecionar ticket #58']"}), W(600), ev(PT(56)), 
    {'do': 'click', 'target': {'selector': "[aria-label='Selecionar ticket #56']"}, 'force': True, 'optional': True}, W(700), S('01-dois'), txt('body', 2600),
    ev("(()=>{const b=[...document.querySelectorAll('button')].find(x=>/Valorizar \\d tickets|Valorizar ticket/.test(x.textContent));if(!b)return 'SEM BARRA';return b.parentElement.parentElement.outerHTML.replace(/<svg.*?<\\/svg>/g,'<svg/>').slice(0,1500)})()", 1600),
    {'do': 'hover', 'target': {'selector': "[aria-label='Selecionar ticket #57']"}, 'optional': True}, W(900), S('02-dica57'), txt('[role=tooltip]', 200),
    ev("(()=>{const b=[...document.querySelectorAll('button')].find(x=>/Valorizar \\d tickets|Valorizar ticket/.test(x.textContent));const x=b&&b.parentElement.parentElement.querySelectorAll('button');if(!x)return 'SEM';x[x.length-1].click();return 'limpou '+x.length})()"),
    W(600), txt('main', 300),
    CK(ACOES(57)), W(500), S('03-acoes57'), ev(dump('[role=menu]'), 1500), {'do': 'press', 'key': 'Escape'}, W(300),
    CK({'role': 'radio', 'name': 'Lista'}), W(900), CK(B('Filtros')), W(600), CK({'selector': POP + " button:has-text('Status')"}), W(700), S('04-status'),
    ev("(()=>[...document.querySelectorAll('[data-radix-popper-content-wrapper]')].map(p=>p.innerHTML.replace(/<svg.*?<\\/svg>/g,'').replace(/class=\"[^\"]*\"/g,'').slice(0,1500)))()", 4000),
    {'do': 'press', 'key': 'Escape'}, {'do': 'press', 'key': 'Escape'}, W(300),
    CK({'role': 'combobox', 'name': 'Este mês'}), W(600), S('05-periodo'), ev(dump('[role=listbox]'), 1500), {'do': 'press', 'key': 'Escape'},
    CK({'role': 'radio', 'name': 'Kanban'}), W(600),
    CK(B('Novo Ticket de Pesagem')), W(2500),
    ev("(()=>[...document.querySelectorAll('main button[aria-label]')].map(b=>b.getAttribute('aria-label')))()"),
    CK({'text': 'Selecionar fornecedor'}), W(900),
    {'do': 'hover', 'target': {'selector': "[role=dialog] button[data-state]:not([aria-label]) >> nth=4"}, 'optional': True}, W(900), S('06-pino'), txt('[role=tooltip]', 200),
    CK({'text': 'Cooperativa Recomeço', 'within': DLG}), W(800),
    opt({'do': 'keys', 'target': MAT, 'text': 'latinha'}), W(700), CK({'role': 'option', 'name': 'Alumínio latinha'}), W(900),
    CK({'selector': "main button[aria-label='Gerenciar motoristas']"}), W(900), S('07-gerenciar-motoristas'), txt(DLG, 600), ev(dump(DLG), 2500), {'do': 'press', 'key': 'Escape'}, W(400),
    ev(OFF), W(12000), S('08-offline-form'),
    CK(B('Pesagem avançada')), W(1000), opt({'do': 'keys', 'target': C('1ª Pesagem'), 'text': '7210'}), CK(B('Confirmar')), W(1200), txt('main', 700),
    CK(B('Salvar Ticket de Pesagem')), W(6000), S('09-offline-6s'), txt('body', 400), W(12000), S('10-offline-18s'), txt(DLG, 900), txt('body', 500), ev(dump(DLG), 2500),
    ev("(async()=>{const d=await indexedDB.databases();return JSON.stringify(d)})()"),
]}
json.dump(e8, open(os.path.join(HERE, '_ex', 'e8.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print('e8', len(e8['steps']))
