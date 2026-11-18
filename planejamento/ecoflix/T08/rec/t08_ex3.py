#!/usr/bin/env python3
"""T08 · exploração e9 (18/11): sem internet com queda de VERDADE (passo `rede`). B = backend inalcançável (navegador online);
A = navegador offline (setOffline). Uso: python3 -I rec/t08/t08_ex3.py  ->  rec/t08/_ex/e9.json"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
DLG = '[role=dialog]'
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
PDFTXT = ("(async()=>{const w=(window.__pops||[]).slice(-1)[0];if(!w)return 'SEM JANELA';for(let i=0;i<40;i++){let f=null;"
       "try{f=w.document&&w.document.querySelector('#pdf-frame')}catch(e){return 'ERRO '+e}"
       "if(f&&f.src){const b=await (await fetch(f.src.split('#')[0])).blob();const u=new Uint8Array(await b.arrayBuffer());let s='';"
       "for(let k=0;k<u.length;k+=8192)s+=String.fromCharCode.apply(null,u.subarray(k,k+8192));return 'PDF:'+btoa(s)}"
       "await new Promise(r=>setTimeout(r,250))}return 'SEM PDF '+(w.document?w.document.title:'')})()")
TOAST = txt('[data-sonner-toaster]', 500)
FILA = ("(async()=>{const r=await new Promise((ok,er)=>{const q=indexedDB.open('ecosistema-offline');q.onsuccess=()=>ok(q.result);q.onerror=()=>er(q.error)});"
        "if(!r.objectStoreNames.contains('weighing_ticket_queue'))return 'SEM STORE';const t=r.transaction('weighing_ticket_queue').objectStore('weighing_ticket_queue').getAll();"
        "const v=await new Promise(ok=>{t.onsuccess=()=>ok(t.result)});return 'FILA '+JSON.stringify(v.map(x=>[x.status,x.temp_order_number,x.error||''])) })()")
ESTADO = ("(async()=>{const o=await (await fetch('http://127.0.0.1:54308/__dev/state?table=weighing_tickets')).json();const l=Array.isArray(o)?o:(o.rows||o.data||[]);"
          "return 'TICKETS '+JSON.stringify(l.map(t=>[t.ticket_number,t.status,t.customer_supplier_name,t.ticket_ref]))})()")
LISTA = [{'do': 'goto', 'url': '/ticket-pesagem'}, {'do': 'waitFor', 'text': 'Gerencie tickets de pesagem rodoviária', 'timeout': 30}, W(1500)]
NOVO = [CK(B('Novo Ticket de Pesagem')), W(2500)]
ITEM = [opt({'do': 'keys', 'target': {'placeholder': 'Escreva o nome ou código do material'}, 'text': 'latinha'}), W(700), CK({'role': 'option', 'name': 'Alumínio latinha'}), W(900),
        CK(B('Pesagem avançada')), W(1000), opt({'do': 'keys', 'target': C('1ª Pesagem'), 'text': '7210'}), CK(B('Confirmar')), W(1200)]
SEEDS = ['base/balanca-ativada', 'base/caixa-aberto', 't08/inicio', 't08/apos-cap08']
e9 = {'seedExtra': SEEDS, 'start': '/dashboard', 'stopOnFail': False, 'steps': [
    W(2500), ev(POPS), *LISTA, S('01-lista-online'), txt('main', 1500), *NOVO, txt('main', 500),
    # ---- B: backend inalcançável, navegador online; o ping de 1 min detecta (relógio adiantado)
    {'do': 'rede', 'offline': True}, {'do': 'clock', 'forward': '01:01'}, W(1500), txt('body', 300), {'do': 'clock', 'forward': '01:01'}, W(2500),
    S('02-B-offline-form'), txt('body', 1500),
    *ITEM, S('03-B-item'), txt('main', 900),
    CK(B('Opções avançadas')), W(700), S('04-B-opcoes'), txt('[data-radix-popper-content-wrapper]', 600), {'do': 'press', 'key': 'Escape'}, W(400),
    CK(B('Salvar Ticket de Pesagem')), W(2500), S('05-B-salvo'), txt(DLG, 900), TOAST, ev(FILA),
    W(3500), S('05b-B-salvo-6s'), txt(DLG, 900),
    CK({'role': 'button', 'name': 'Imprimir comprovante'}), W(1500), S('06-B-imprimir'), txt(DLG, 900), txt('body', 600),
    CK({'role': 'button', 'name': 'Térmico', 'within': DLG}), W(2500), S('07-B-termico'), ev(PDFTXT, 400000), txt('body', 400),
    opt({'do': 'press', 'key': 'Escape'}), W(500),
    CK(B('Voltar')), W(2000), S('08-B-lista-offline'), txt('body', 2500),
    CK(ACOES(57)), W(600), S('09-B-acoes57'), txt('[role=menu]', 400),
    CK({'role': 'menuitem', 'name': 'Valorizar'}), W(900), S('10-B-valorizar'), TOAST, W(4500),
    CK(ACOES(57)), W(600), CK({'role': 'menuitem', 'name': 'Editar'}), W(900), S('11-B-editar'), TOAST, txt('body', 600), W(4500),
    # ---- a conexão volta (o evento online só faz o app medir)
    {'do': 'rede', 'offline': False, 'avisar': True}, W(1000), S('12-B-volta-1s'), txt('body', 300),
    W(1500), S('13-B-volta-2s5'), txt('body', 300), W(1500), S('14-B-volta-4s'), txt('body', 300), W(1500), S('15-B-volta-5s5'), txt('body', 300),
    W(2000), S('16-B-volta-7s5'), txt('body', 300), W(3000), S('17-B-volta-10s5'), txt('body', 2500), ev(FILA), ev(ESTADO),
    W(6000), S('18-B-volta-16s'), txt('main', 2500), ev(FILA), ev(ESTADO),
    # ---- A: navegador offline (cabo/wi-fi desligado)
    *NOVO, {'do': 'rede', 'offline': True, 'modo': 'navegador'}, W(3000), S('20-A-offline-form'), txt('body', 700),
    *ITEM, S('21-A-item'),
    CK(B('Salvar Ticket de Pesagem')), W(3000), S('22-A-salvar-3s'), txt(DLG, 500), TOAST, ev(FILA),
    W(12000), S('23-A-salvar-15s'), txt(DLG, 500), TOAST, ev(FILA),
    ev("(()=>{const b=[...document.querySelectorAll('button')].find(x=>/Salvar Ticket/.test(x.textContent));return b?[b.disabled,b.innerHTML.slice(0,200)]:'SEM'})()"),
    {'do': 'rede', 'offline': False, 'modo': 'navegador'}, W(1500), S('24-A-volta-1s5'), txt(DLG, 500), TOAST, ev(FILA),
    W(4000), S('25-A-volta-5s5'), txt(DLG, 500), TOAST, ev(FILA), W(8000), S('26-A-volta-13s'), txt('body', 1200), ev(FILA), ev(ESTADO),
]}
json.dump(e9, open(os.path.join(HERE, '_ex', 'e9.json'), 'w', encoding='utf8'), ensure_ascii=False)
print('e9', len(e9['steps']))
