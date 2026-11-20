#!/usr/bin/env python3
"""T03 · gera _ex/margem.json (exploração da tela Editar Preços e da Margem automática no 1.60.18). Não faz parte da gravação."""
import json, os, sys
sys.argv = [sys.argv[0]]
import importlib.util
spec = importlib.util.spec_from_file_location('gerar', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gerar.py'))
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
import os as _o
st = g.setup_login('rafael@reciclavalemetais.example') + g.ESTOQUE + g.RECOLHE
for x in st:
    if x.get('text') == '$TUT_SENHA': x['text'] = _o.environ['TUT_SENHA']
def shot(n): return {'do': 'shot', 'name': n}
def txt(sel, n): return {'do': 'text', 'selector': sel, 'name': n}
st = [({'do':'wait','ms':1500} if x.get('idle') else ({'do':'wait','ms':int(x['seconds']*1000)} if x.get('do')=='pause' else x)) for x in st]
ROW=lambda n,k: {'selector': f"[role=dialog] tbody tr:has-text('{n}') input", 'nth': k}
ROWS=lambda a,b: "[...document.querySelectorAll('[role=dialog] tbody tr')].slice(%d,%d).map(r=>r.innerText.replace(/\\s+/g,' ').slice(0,40)+' | '+[...r.querySelectorAll('input')].map(i=>i.value).join(',')).join(' ; ')" % (a,b)
import sys as _s
SEEDS = ['t03/inicio', 't03/apos-cap06', 't03/margem-material']
steps = st + [
  {'do': 'keys', 'target': g.BUSCA, 'text': 'radiador', 'clear': True}, {'do': 'wait', 'ms': 800},
  {'do': 'hover', 'target': g.ACOES('Radiador de cobre')}, {'do': 'wait', 'ms': 500}, {'do': 'click', 'target': g.ITEM('Editar')}, {'do': 'wait', 'ms': 1200},
  {'do': 'eval', 'js': "[...document.querySelectorAll('[role=dialog] button')].map(b=>(b.innerText||b.getAttribute('aria-label')||b.title||'').trim()).filter(Boolean).join(' | ')"},
  {'do': 'eval', 'js': "(()=>{const e=document.querySelector('#sale_price');e.scrollIntoView({block:'center'});return [...document.querySelectorAll('[role=dialog] input')].map(i=>i.id+'='+i.value).join(' ; ')})()"},
  {'do': 'wait', 'ms': 500}, shot('d01-editar'),
  {'do': 'click', 'target': {'selector': 'button[aria-label="Calcular a venda pela margem"]'}}, {'do': 'wait', 'ms': 500}, shot('d02-calc'),
  txt('[data-radix-popper-content-wrapper]', 'd02-popover'),
  {'do': 'eval', 'js': "[...document.querySelectorAll('[data-radix-popper-content-wrapper] input, [data-radix-popper-content-wrapper] button')].map(b=>b.tagName+':'+(b.value||b.innerText||b.title||'').trim().slice(0,60)).join(' | ')"},
  {'do': 'keys', 'target': {'selector': '[data-radix-popper-content-wrapper] input'}, 'text': '20', 'clear': True}, {'do': 'wait', 'ms': 400},
  txt('[data-radix-popper-content-wrapper]', 'd03-popover'),
  {'do': 'click', 'target': {'selector': '[data-radix-popper-content-wrapper] button[title^="Margem em porcentagem"]'}}, {'do': 'wait', 'ms': 400},
  txt('[data-radix-popper-content-wrapper]', 'd04-popover'),
  {'do': 'click', 'target': {'role': 'button', 'name': 'Aplicar', 'exact': True, 'within': '[data-radix-popper-content-wrapper]'}}, {'do': 'wait', 'ms': 500},
  {'do': 'eval', 'js': "[...document.querySelectorAll('[role=dialog] input')].map(i=>i.id+'='+i.value).join(' ; ')"},
  shot('d05-aplicado'),
  {'do': 'keys', 'target': {'selector': '#purchase_price'}, 'text': '22', 'clear': True}, {'do': 'wait', 'ms': 400},
  {'do': 'eval', 'js': "[...document.querySelectorAll('[role=dialog] input')].map(i=>i.id+'='+i.value).join(' ; ')+' || '+[...document.querySelectorAll('[role=dialog] p')].map(p=>p.innerText).filter(t=>/Margem/.test(t)).join(' / ')"},
  shot('d06-compra22'),
  {'do': 'eval', 'js': "[...document.querySelectorAll('[role=dialog] button')].map(b=>(b.innerText||'').trim()).filter(Boolean).join(' | ')"},
  ]
json.dump({'seedExtra': SEEDS, 'start': '/login', 'anonymous': True, 'storage': g.storage_de('user.rafael'), 'steps': steps},
          open('/dev/shm/t03_ex.json', 'w'), ensure_ascii=False, indent=1)
print(len(steps))
