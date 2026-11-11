#!/usr/bin/env python3
"""T08 · gera as explorações (rec/t08/_ex/eN.json) com o despejo de elementos visíveis (DUMP). Uso: python3 -I rec/t08/t08_ex.py"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
def dump(esc='body', n=140):
    return ("(()=>{const out=[];const root=document.querySelectorAll(%s);const vis=e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height>0&&r.bottom>0&&r.top<800};"
            "for(const R of root)for(const e of R.querySelectorAll('button,a,input,textarea,[role=tab],[role=switch],[role=combobox],[role=radio],[role=option],[role=menuitem],[role=checkbox],h1,h2,h3,label,th')){if(!vis(e))continue;const r=e.getBoundingClientRect();"
            "const t=(e.innerText||e.value||'').trim().replace(/\\s+/g,' ').slice(0,48);const a=[e.tagName.toLowerCase()+(e.getAttribute('role')?'['+e.getAttribute('role')+']':''),t];"
            "for(const k of ['aria-label','placeholder','title','data-state','aria-checked','aria-pressed','type'])if(e.getAttribute(k))a.push(k.slice(0,4)+'='+e.getAttribute(k).slice(0,30));"
            "a.push(Math.round(r.x)+','+Math.round(r.y)+','+Math.round(r.width)+'x'+Math.round(r.height));out.push(a.join('|'))}return out.slice(0,%d)})()") % (json.dumps(esc), n)
DLG = '[role=dialog]'
def ev(js, mx=9000): return {'do': 'eval', 'js': js, 'max': mx}
def opt(d): d['optional'] = True; return d
SEEDS = ['base/balanca-ativada', 'base/caixa-aberto']
e1 = {'seedExtra': SEEDS, 'start': '/dashboard', 'stopOnFail': False, 'steps': [
    {'do': 'wait', 'ms': 3000},
    {'do': 'goto', 'url': '/ticket-pesagem'}, {'do': 'waitFor', 'text': 'Gerencie tickets de pesagem rodoviária', 'timeout': 30}, {'do': 'wait', 'ms': 1500},
    {'do': 'shot', 'name': '01-lista'}, ev(dump()),
    opt({'do': 'click', 'target': {'text': 'Pesagens avulsas'}}), {'do': 'wait', 'ms': 800}, {'do': 'shot', 'name': '02-avulsas'}, ev(dump('main'), 4000),
    opt({'do': 'click', 'target': {'text': 'Tickets padrão'}}),
    {'do': 'click', 'target': {'role': 'button', 'name': 'Novo Ticket de Pesagem'}}, {'do': 'wait', 'ms': 2000}, {'do': 'shot', 'name': '03-novo'}, ev(dump()),
    opt({'do': 'click', 'target': {'text': 'Selecionar fornecedor'}}), {'do': 'wait', 'ms': 800}, {'do': 'shot', 'name': '04-forn'}, ev(dump(DLG), 5000),
    opt({'do': 'type', 'target': {'placeholder': 'Buscar por nome, apelido, CPF/CNPJ ou telefone...'}, 'text': 'Recomeço'}), {'do': 'wait', 'ms': 800}, ev(dump(DLG), 3000),
    opt({'do': 'click', 'target': {'text': 'Cooperativa Recomeço', 'within': DLG}}), {'do': 'wait', 'ms': 800},
    opt({'do': 'type', 'target': {'placeholder': 'Escreva o nome ou código do material'}, 'text': 'latinha'}), {'do': 'wait', 'ms': 1200}, {'do': 'shot', 'name': '05-mat'}, ev(dump(), 7000),
    opt({'do': 'click', 'target': {'role': 'option', 'name': 'Alumínio latinha'}}), {'do': 'wait', 'ms': 1200},
    opt({'do': 'type', 'target': {'placeholder': 'Digite ou busque o motorista'}, 'text': 'Edson'}), {'do': 'wait', 'ms': 1000}, {'do': 'shot', 'name': '06-mot'}, ev(dump(), 7000),
    opt({'do': 'click', 'target': {'text': 'Edson Moura'}}), {'do': 'wait', 'ms': 800},
    opt({'do': 'click', 'target': {'placeholder': 'Digite ou busque a placa'}}), {'do': 'wait', 'ms': 1000}, {'do': 'shot', 'name': '07-placa'}, ev(dump(), 7000),
    opt({'do': 'click', 'target': {'text': 'FKD2E41'}}), {'do': 'wait', 'ms': 1000}, {'do': 'shot', 'name': '08-preenchido'}, ev(dump()),
    opt({'do': 'click', 'target': {'role': 'button', 'name': 'Pesagem avançada'}}), {'do': 'wait', 'ms': 1200}, {'do': 'shot', 'name': '09-avancada'}, ev(dump(DLG)),
    opt({'do': 'type', 'target': {'label': '1ª Pesagem'}, 'text': '9460'}), {'do': 'wait', 'ms': 800}, {'do': 'shot', 'name': '10-1a'},
    opt({'do': 'click', 'target': {'text': 'Completo', 'within': DLG}}), {'do': 'wait', 'ms': 500}, {'do': 'shot', 'name': '11-completo'}, ev(dump(DLG)),
    opt({'do': 'click', 'target': {'role': 'button', 'name': 'Confirmar'}}), {'do': 'wait', 'ms': 1500}, {'do': 'shot', 'name': '12-confirmado'}, ev(dump()),
]}
json.dump(e1, open(os.path.join(HERE, '_ex', 'e1.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print('ok')

# ---------------------------------------------------------------- e2: o fluxo inteiro, com os seletores corrigidos
def txt(sel, n=1500):
    return ev("(()=>{const e=[...document.querySelectorAll(%s)].pop();return e?e.innerText.replace(/\\s+/g,' ').slice(0,%d):'SEM'})()" % (json.dumps(sel), n), n + 40)
ANC = ("(()=>{let e=document.querySelector(\"[aria-label='Selecionar ticket #57']\");const o=[];for(let i=0;i<9&&e;i++){o.push(e.tagName+'.'+(e.className||'').toString().slice(0,90));e=e.parentElement}return o})()")
POPS = "(()=>{const o=window.open;window.__pops=[];window.open=function(...a){const w=o.apply(this,a);window.__pops.push(w);return w};return 'ok'})()"
PDF = ("(async()=>{const w=(window.__pops||[]).slice(-1)[0];if(!w)return 'sem janela';for(let i=0;i<40;i++){let f=null;try{f=w.document&&w.document.querySelector('#pdf-frame')}catch(e){return 'erro '+e}"
       "if(f&&f.src){const b=await (await fetch(f.src.split('#')[0])).blob();return 'PDF '+b.size+' '+b.type+' titulo='+w.document.title}await new Promise(r=>setTimeout(r,250))}"
       "return 'sem pdf: '+(w.document&&w.document.title)+' '+(w.document&&w.document.body&&w.document.body.innerText.slice(0,200))})()")
C = lambda rot: {'selector': f"[role=dialog] div:has(> label:has-text('{rot}')) input"}
IMP = {'selector': "[role=dialog] div:has(> div > label:has-text('Impureza')) input"}
ACOES58 = {'role': 'button', 'name': 'Ações', 'within': "main div.rounded-lg:has([aria-label='Selecionar ticket #58']):not(:has(div.rounded-lg [aria-label='Selecionar ticket #58']))"}
SW = {'selector': "button[aria-expanded]:has-text('#58')"}
def forn(nome, busca):
    return [opt({'do': 'click', 'target': {'text': 'Selecionar fornecedor'}}), {'do': 'wait', 'ms': 700},
            opt({'do': 'keys', 'target': {'placeholder': 'Buscar por nome, apelido, CPF/CNPJ ou telefone...'}, 'text': busca}), {'do': 'wait', 'ms': 600},
            opt({'do': 'click', 'target': {'text': nome, 'within': DLG}}), {'do': 'wait', 'ms': 700}]
e2 = {'seedExtra': SEEDS, 'start': '/dashboard', 'stopOnFail': False, 'steps': [
    {'do': 'wait', 'ms': 2500}, ev(POPS),
    {'do': 'goto', 'url': '/ticket-pesagem'}, {'do': 'waitFor', 'text': 'Gerencie tickets de pesagem rodoviária', 'timeout': 30}, {'do': 'wait', 'ms': 1200},
    ev(ANC, 1500),
    {'do': 'click', 'target': {'role': 'button', 'name': 'Novo Ticket de Pesagem'}}, {'do': 'wait', 'ms': 1500},
    *forn('Cooperativa Recomeço', 'Recomeço'),
    opt({'do': 'keys', 'target': {'placeholder': 'Escreva o nome ou código do material'}, 'text': 'latinha'}), {'do': 'wait', 'ms': 700}, ev(dump('[role=listbox]'), 800),
    opt({'do': 'click', 'target': {'role': 'option', 'name': 'Alumínio latinha'}}), {'do': 'wait', 'ms': 900},
    opt({'do': 'keys', 'target': {'placeholder': 'Digite ou busque o motorista'}, 'text': 'Edson'}), {'do': 'wait', 'ms': 700},
    opt({'do': 'click', 'target': {'text': 'Edson Moura'}}), {'do': 'wait', 'ms': 600},
    {'do': 'wheel', 'x': 700, 'y': 500, 'dy': 300},
    opt({'do': 'keys', 'target': {'placeholder': 'Digite ou busque a placa'}, 'text': 'FKD'}), {'do': 'wait', 'ms': 800}, {'do': 'shot', 'name': '01-placa'}, ev(dump(), 9000),
    opt({'do': 'click', 'target': {'text': 'FKD2E41'}}), {'do': 'wait', 'ms': 900}, {'do': 'shot', 'name': '02-cabecalho'}, txt('main', 900),
    opt({'do': 'click', 'target': {'role': 'button', 'name': 'Pesagem avançada'}}), {'do': 'wait', 'ms': 1000},
    opt({'do': 'keys', 'target': C('1ª Pesagem'), 'text': '9460'}), {'do': 'wait', 'ms': 600}, {'do': 'shot', 'name': '03-1a'}, txt(DLG, 700),
    opt({'do': 'click', 'target': {'text': 'Completo', 'within': DLG}}), opt({'do': 'click', 'target': {'role': 'button', 'name': 'Confirmar'}}), {'do': 'wait', 'ms': 1500},
    {'do': 'shot', 'name': '04-item'}, txt('main', 1500),
    opt({'do': 'click', 'target': SW}), {'do': 'wait', 'ms': 800}, {'do': 'shot', 'name': '05-abas'}, ev(dump('[data-radix-popper-content-wrapper]'), 2500), {'do': 'press', 'key': 'Escape'},
    opt({'do': 'click', 'target': {'role': 'button', 'name': 'Voltar'}}), {'do': 'wait', 'ms': 1500}, txt('main', 400),
    opt({'do': 'click', 'target': {'text': 'Rascunhos abertos'}}), {'do': 'wait', 'ms': 2000}, {'do': 'shot', 'name': '06-reaberto'}, txt('main', 1200),
    opt({'do': 'click', 'target': {'selector': "button[aria-label='Ações do item']"}}), {'do': 'wait', 'ms': 600}, ev(dump('[role=menu]'), 1200),
    opt({'do': 'click', 'target': {'role': 'menuitem', 'name': 'Adicionar tara / pesagem avançada'}}), {'do': 'wait', 'ms': 1000}, {'do': 'shot', 'name': '07-edita'}, txt(DLG, 700),
    opt({'do': 'keys', 'target': C('1ª Pesagem'), 'text': '9460'}), opt({'do': 'keys', 'target': C('2ª Pesagem'), 'text': '6380'}), {'do': 'wait', 'ms': 600},
    {'do': 'shot', 'name': '08-bruto'}, txt(DLG, 700),
    opt({'do': 'click', 'target': {'role': 'button', 'name': 'Confirmar'}}), {'do': 'wait', 'ms': 1200}, txt('body', 300),
    opt({'do': 'click', 'target': {'selector': "button[aria-label='Ver detalhes da pesagem']"}}), {'do': 'wait', 'ms': 800}, {'do': 'shot', 'name': '09-detalhe'}, txt('main', 1500),
    opt({'do': 'click', 'target': {'selector': "button[aria-label='Ações do item']"}}), {'do': 'wait', 'ms': 600},
    opt({'do': 'click', 'target': {'role': 'menuitem', 'name': 'Adicionar tara / pesagem avançada'}}), {'do': 'wait', 'ms': 1000}, txt(DLG, 500),
    opt({'do': 'click', 'target': {'role': 'radio', 'name': '%'}}), {'do': 'wait', 'ms': 400},
    opt({'do': 'keys', 'target': IMP, 'text': '2'}), {'do': 'wait', 'ms': 600}, {'do': 'shot', 'name': '10-impureza'}, txt(DLG, 900), ev(dump(DLG), 5000),
    opt({'do': 'click', 'target': {'role': 'button', 'name': 'Confirmar'}}), {'do': 'wait', 'ms': 1200}, txt('main', 1200),
    opt({'do': 'click', 'target': {'selector': "button[aria-label='Novo ticket de pesagem']"}}), {'do': 'wait', 'ms': 1200}, {'do': 'shot', 'name': '11-aba2'},
    *forn('Auto Peças Vale Forte', 'Vale Forte'),
    opt({'do': 'keys', 'target': {'placeholder': 'Escreva o nome ou código do material'}, 'text': 'bateria'}), {'do': 'wait', 'ms': 500}, {'do': 'press', 'key': 'Enter'}, {'do': 'wait', 'ms': 800},
    opt({'do': 'keys', 'target': {'placeholder': 'Digite ou busque o motorista'}, 'text': 'Jair'}), {'do': 'wait', 'ms': 500}, {'do': 'press', 'key': 'Enter'}, {'do': 'wait', 'ms': 600},
    opt({'do': 'keys', 'target': {'placeholder': 'Digite ou busque a placa'}, 'text': 'GHT'}), {'do': 'wait', 'ms': 500}, {'do': 'press', 'key': 'Enter'}, {'do': 'wait', 'ms': 800},
    {'do': 'shot', 'name': '12-aba2-preenchida'}, txt('main', 900),
    opt({'do': 'click', 'target': {'role': 'button', 'name': 'Pesagem avançada'}}), {'do': 'wait', 'ms': 900},
    opt({'do': 'keys', 'target': C('1ª Pesagem'), 'text': '5640'}), {'do': 'press', 'key': 'Enter'}, {'do': 'wait', 'ms': 1000}, txt('body', 300),
    opt({'do': 'click', 'target': {'role': 'button', 'name': 'Confirmar'}}), {'do': 'wait', 'ms': 1200},
    opt({'do': 'click', 'target': {'selector': "button[aria-expanded]:has-text('#59')"}}), {'do': 'wait', 'ms': 800}, {'do': 'shot', 'name': '13-lista-abas'},
    ev(dump('[data-radix-popper-content-wrapper]'), 3000),
    opt({'do': 'click', 'target': {'selector': "[data-radix-popper-content-wrapper] button:has-text('#58')"}}), {'do': 'wait', 'ms': 1200},
    opt({'do': 'click', 'target': {'role': 'button', 'name': 'Salvar Ticket de Pesagem'}}), {'do': 'wait', 'ms': 2500}, {'do': 'shot', 'name': '14-salvo'}, ev(dump(DLG), 2000), txt('body', 400),
    {'do': 'press', 'key': 'Escape'}, {'do': 'wait', 'ms': 800}, txt('main', 600),
    opt({'do': 'click', 'target': {'selector': "button[aria-expanded]:has-text('#59')"}}), {'do': 'wait', 'ms': 700}, ev(dump('[data-radix-popper-content-wrapper]'), 2000), {'do': 'press', 'key': 'Escape'},
    opt({'do': 'click', 'target': {'role': 'button', 'name': 'Voltar'}}), {'do': 'wait', 'ms': 1800}, {'do': 'shot', 'name': '15-kanban'}, txt('main', 1500),
    opt({'do': 'click', 'target': ACOES58}), {'do': 'wait', 'ms': 600}, ev(dump('[role=menu]'), 1200),
    opt({'do': 'click', 'target': {'role': 'menuitem', 'name': 'Valorizar'}}), {'do': 'wait', 'ms': 3500}, {'do': 'shot', 'name': '16-compra'}, txt('main', 2500), ev(dump('main'), 9000), txt('body', 300),
    {'do': 'goto', 'url': '/ticket-pesagem'}, {'do': 'wait', 'ms': 2500},
    opt({'do': 'click', 'target': ACOES58}), {'do': 'wait', 'ms': 600}, opt({'do': 'click', 'target': {'role': 'menuitem', 'name': 'Ver comprovante'}}), {'do': 'wait', 'ms': 800},
    {'do': 'shot', 'name': '17-formato'}, ev(dump(DLG), 1500),
    opt({'do': 'click', 'target': {'text': 'Térmico', 'within': DLG}}), {'do': 'wait', 'ms': 4000}, ev(PDF, 400), {'do': 'shot', 'name': '18-depois-termico'}, txt('body', 300),
    opt({'do': 'click', 'target': ACOES58}), {'do': 'wait', 'ms': 600}, opt({'do': 'click', 'target': {'role': 'menuitem', 'name': 'Valorizar'}}), {'do': 'wait', 'ms': 1500},
    txt('body', 600), {'do': 'wait', 'ms': 2000},
    opt({'do': 'click', 'target': {'role': 'button', 'name': 'Finalizar'}}), {'do': 'wait', 'ms': 1500}, {'do': 'shot', 'name': '19-finalizar'}, ev(dump(DLG), 6000),
    opt({'do': 'click', 'target': {'text': 'Pix/Transferência', 'within': DLG}}), {'do': 'wait', 'ms': 900}, {'do': 'shot', 'name': '20-pix'}, ev(dump(DLG), 6000),
    opt({'do': 'click', 'target': {'role': 'button', 'name': 'CONFIRMAR PAGAMENTO'}}), {'do': 'wait', 'ms': 2500}, {'do': 'shot', 'name': '21-depois'}, txt('body', 800),
    {'do': 'wait', 'ms': 2500}, {'do': 'shot', 'name': '22-volta'}, txt('main', 1500),
    opt({'do': 'click', 'target': {'role': 'radio', 'name': 'Lista'}}), {'do': 'wait', 'ms': 1000}, {'do': 'shot', 'name': '23-lista'}, txt('main', 1500),
    opt({'do': 'click', 'target': {'role': 'button', 'name': 'Filtros'}}), {'do': 'wait', 'ms': 800}, {'do': 'shot', 'name': '24-filtros'}, ev(dump('[data-radix-popper-content-wrapper]'), 3000),
    {'do': 'press', 'key': 'Escape'},
    {'do': 'goto', 'url': '/configuracoes?tab=integrations'}, {'do': 'wait', 'ms': 3000},
    ev("(()=>{const e=[...document.querySelectorAll('main *')].find(x=>x.children.length===0&&x.textContent.trim()==='Imprimir comprovante do Ticket de Pesagem');if(!e)return 'SEM';e.scrollIntoView({block:'center'});const r=e.getBoundingClientRect();let c=e;for(let i=0;i<5&&c;i++)c=c.parentElement;return [Math.round(r.x),Math.round(r.y),c&&c.innerText.slice(0,300)]})()", 600),
    {'do': 'wait', 'ms': 600}, {'do': 'shot', 'name': '25-integracoes'}, ev(dump('main'), 4000),
]}
json.dump(e2, open(os.path.join(HERE, '_ex', 'e2.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print('e2 ok')
