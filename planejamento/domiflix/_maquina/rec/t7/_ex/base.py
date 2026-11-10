#!/usr/bin/env python3
"""Explorador T7: monta um cenário (prefixo comum + passos próprios) e roda o explorar.mjs. Uso: python3 base.py nome 'json-dos-passos'"""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
cad = json.load(open(os.path.join(HERE, '..', 'cadeia.json'), encoding='utf8'))
STUB = open(os.path.join(HERE, '..', 'geo_stub.js'), encoding='utf8').read()

def rolar(alvo_js, y=540, nome=None):
    """passo eval que leva o centro do elemento (alvo_js: expressão que devolve o elemento) para y (px CSS), instantâneo"""
    js = "(()=>{const el=(" + alvo_js + ");if(!el)return 'sem alvo';const r=el.getBoundingClientRect();window.scrollTo({top:Math.round(window.scrollY+r.top+r.height/2-" + str(y) + "),behavior:'instant'});const q=el.getBoundingClientRect();return [Math.round(q.top),Math.round(q.height)]})()"
    return {"do": "eval", "js": js}

def pre(ate='checkin'):
    p = [{"do": "wait", "ms": 2500}, {"do": "eval", "js": STUB},
         {"do": "eval", "js": "window.__setGeo(-22.9003,-43.1180)"},
         {"do": "click", "target": {"text": "Colégio Monte Verde", "within": "main"}}, {"do": "wait", "ms": 1200},
         {"do": "click", "target": {"role": "button", "name": "Preencher OS"}}, {"do": "wait", "ms": 3000}]
    if ate == 'os': return p
    p += [{"do": "click", "target": {"role": "button", "name": "A Caminho"}}, {"do": "wait", "ms": 3000},
          {"do": "eval", "js": "window.__setGeo(-22.89758,-43.09913)"}, {"do": "wait", "ms": 1000},
          {"do": "clock", "set": "2026-11-11T09:05:00-03:00"}]
    if ate == 'caminho': return p
    p += [{"do": "click", "target": {"role": "button", "name": "Fazer Check-in"}}, {"do": "wait", "ms": 3500}]
    return p

def run(nome, passos, ate='checkin', env=None, extra=None):
    sc = {"seedExtra": (extra or {}).get('seed', cad['inicio']), "user": "rafael.lima@glacialcold.example", "device": "phone", "start": "/agenda",
          "steps": pre(ate) + passos}
    f = os.path.join(HERE, nome + '.json')
    json.dump(sc, open(f, 'w'), ensure_ascii=False, indent=1)
    e = dict(os.environ, TUT_HOME='/home/claude/domiflix', FAKE_URL='http://127.0.0.1:54321', FAKE_NOW='2026-11-11T08:50:00-03:00')
    e.update(env or {})
    r = subprocess.run(['nice', '-n', '19', 'timeout', '290', 'node', 'rec/t7/explorar.mjs', f, '--out', 'rec/t7/_ex/out'], cwd=ROOT, env=e, capture_output=True, text=True)
    out = r.stdout + r.stderr
    npre = len(pre(ate))
    # esconde as linhas "ok" do prefixo e dos passos simples
    linhas = [l for l in out.splitlines() if not (': ok' in l and len(l) < 140)]
    print('\n'.join(linhas))

if __name__ == '__main__':
    run(sys.argv[1], json.loads(sys.argv[2]), ate=(sys.argv[3] if len(sys.argv) > 3 else 'checkin'))
