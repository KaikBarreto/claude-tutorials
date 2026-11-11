#!/usr/bin/env python3
"""T16 · a aula inteira numa exploração só (uma trava): converte os roteiros do robô rec/t16/capNN.json (os mesmos alvos e dados)
em passos do explorar.mjs, em ordem, com uma foto e um "DUMP" do banco no fim de cada capítulo (t16_sementes.js_dump).
Serve para (1) conferir de uma vez os seletores de todos os capítulos e (2) tirar a cadeia de sementes apos-capNN sem esperar
15 ensaios em fila (`t16_sementes.py dump rec/t16/_ex/<nome>.out capNN NN`).

  python3 -I rec/t16/t16_cadeia.py <nome> DE ATE        -> rec/t16/_ex/<nome>.json (capítulos DE..ATE; parte da semente de DE)
  bash rec/t16/t16_ex.sh <nome>                         (sob a trava)

Diferenças do robô (só no explorador): digitação sem clique vira insertText no campo em foco (o React recebe o input), a senha do
certificado é um texto fictício, passos condicionais (when/unless) e marcas saem, `marcar` vira `count`."""
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('sem', os.path.join(HERE, 't16_sementes.py'))
sem = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sem)

ROTA = {}   # rota de partida de cada capítulo (o goto do setup)


def insere(txt):
    return {'do': 'eval', 'js': ("(()=>{const e=document.activeElement;if(!e||!/^(INPUT|TEXTAREA)$/.test(e.tagName))return 'SEM ALVO (nada em foco)';"
                                 f"document.execCommand('insertText',false,{json.dumps(txt, ensure_ascii=False)});return e.value}})()")}


BT = ("(()=>[...document.querySelectorAll('SEL')].filter(e=>e.offsetParent).map(e=>{const r=e.getBoundingClientRect();return e.tagName.toLowerCase()"
      "+'|'+(e.getAttribute('role')||'')+'|'+(e.id||'')+'|'+(e.getAttribute('aria-label')||'')+'|'+((e.innerText||e.getAttribute('placeholder')||e.value||'')"
      ".trim().replace(/\\s+/g,' ').slice(0,40))+'|'+Math.round(r.x)+','+Math.round(r.y)+','+Math.round(r.width)+'x'+Math.round(r.height)}).join(' ;; '))()")
bt = lambda sel, mx=4000: {'do': 'eval', 'js': BT.replace('SEL', sel), 'max': mx}
INFO = [  # o que a 1ª exploração (e1) não chegou a ver: o menu lateral, a tela de NF-e e a Configuração Fiscal
    {'do': 'click', 'target': {'selector': "button:has(span:text-is('Fiscal & Ambiental'))"}, 'after': 600},
    {'do': 'shot', 'name': 'i01-menu'}, bt('a[href*=fiscal], nav a, nav button', 3000),
    {'do': 'goto', 'url': '/fiscal-ambiental/nfe/entrada'}, {'do': 'wait', 'ms': 1500}, {'do': 'shot', 'name': 'i02-entrada'},
    bt('main button, main a, main [role=tab]', 5000), {'do': 'text', 'selector': 'main', 'name': 'entrada', 'max': 1200},
    {'do': 'goto', 'url': '/fiscal-ambiental/configuracao/certificado'}, {'do': 'wait', 'ms': 1500}, {'do': 'shot', 'name': 'i03-cert'},
    bt('main button, main a, main input, main label', 5000),
]


def converte(n):
    d = json.load(open(os.path.join(HERE, f'cap{n:02d}.json'), encoding='utf8'))
    out = [{'do': 'eval', 'js': f"'===== cap{n:02d} ====='"}]
    goto = [s for s in d['setup'] if s.get('do') == 'goto']
    out.append({'do': 'goto', 'url': goto[-1]['url'] if goto else '/dashboard'})
    depois = d['setup'][max([i for i, s in enumerate(d['setup']) if s.get('do') == 'goto'] or [len(d['setup'])]):]
    for s in depois:   # só as esperas depois do goto (as do login olham o Dashboard)
        if s.get('do') == 'waitFor' and (s.get('text') or s.get('selector')):
            out.append({'do': 'waitFor', **{k: s[k] for k in ('text', 'selector', 'timeout') if k in s}})
    out.append({'do': 'wait', 'ms': 800})
    for s in d['steps']:
        do = s.get('do')
        if do == 'mark' or s.get('when') or s.get('unless'):
            continue
        tag = s.get('label') or ''
        if do == 'click':
            out.append({'do': 'click', 'target': s['target'], 'after': 400, '_l': tag})
        elif do == 'hover':
            out.append({'do': 'hover', 'target': s['target'], 'after': 150, '_l': tag})
        elif do == 'type':
            txt = s.get('text', '')
            if txt == '' and s.get('noClick'):
                out.append({'do': 'count', 'target': s['target'], '_l': tag})
                continue
            if txt.startswith('$'):
                txt = 'senha-ficticia'
            if not s.get('noClick'):
                out.append({'do': 'click', 'target': s['target'], 'after': 200})
            if s.get('clear'):
                out.append({'do': 'press', 'key': ['Control+A', 'Backspace']})
            out.append({**insere(txt), '_l': tag})
        elif do == 'press':
            out.append({'do': 'press', 'key': s['key']})
        elif do == 'eval':
            out.append({'do': 'eval', 'js': s['js'], '_l': tag, 'max': 400})
        elif do == 'waitFor':
            w = {k: s[k] for k in ('text', 'selector', 'target', 'timeout') if k in s}
            if w and not s.get('idle'):
                out.append({'do': 'waitFor', **w})
        elif do == 'upload':
            out.append({'do': 'upload', 'target': s['target'], 'file': '../' + s['file'], '_l': tag})
        elif do in ('wait', 'pause'):
            out.append({'do': 'wait', 'ms': int(1000 * s.get('seconds', 0.5))})
        elif do == 'scroll':
            continue
    out.append({'do': 'wait', 'ms': 1200})
    out.append({'do': 'shot', 'name': f'fim-cap{n:02d}'})
    out.append({'do': 'eval', 'js': sem.js_dump(f'cap{n:02d}'), 'max': 3000000})
    return out


if __name__ == '__main__':
    nome, de, ate = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    passos = []
    for n in range(de, ate + 1):
        passos += converte(n)
    d0 = json.load(open(os.path.join(HERE, f'cap{de:02d}.json'), encoding='utf8'))
    if '--info' in sys.argv:
        passos = INFO + passos
    js = {'seedExtra': d0['seedExtra'], 'storage': d0['storage'], 'start': '/dashboard', 'steps': passos, 'stopOnFail': False}
    os.makedirs(os.path.join(HERE, '_ex'), exist_ok=True)
    json.dump(js, open(os.path.join(HERE, '_ex', f'{nome}.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print(f'_ex/{nome}.json: {len(passos)} passos, caps {de}..{ate}, semente {d0["seedExtra"]}')
