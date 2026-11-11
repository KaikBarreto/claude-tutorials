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
