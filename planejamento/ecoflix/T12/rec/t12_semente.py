#!/usr/bin/env python3
"""T12 · grava rec/mundo/seeds-extra/t12/<nome>.json com o que a aula deixou na instância 54312, logo depois do ensaio (ou gravação)
de um capítulo e ANTES de outra gravação resetar a instância. Compara o estado atual com o do ponto de partida da aula (reset + as
sementes BASE do gerar.py): linhas novas, linhas alteradas (_patch por id) e linhas que sumiram (_remove por id). A semente sai
CUMULATIVA (tudo desde a base), como a cadeia do gerar.py espera. Tabelas efêmeras (presença/edição em andamento) ficam de fora.
Uso: python3 -I rec/t12/t12_semente.py apos-cap03 [--ver]   (--ver: só mostra o que mudou, sem gravar)"""
import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
FAKE = 'http://127.0.0.1:54312'
SAIDA = os.path.normpath(os.path.join(HERE, '..', 'mundo', 'seeds-extra', 't12'))
BASE = ['t12/inicio']
FORA = ('presence', 'editing', 'heartbeat', 'audit', 'request_log', 'session')


def get(u):
    return json.load(urllib.request.urlopen(FAKE + u, timeout=60))


def post(u, corpo=None):
    r = urllib.request.Request(FAKE + u, data=json.dumps(corpo or {}).encode(), headers={'content-type': 'application/json'}, method='POST')
    return json.load(urllib.request.urlopen(r, timeout=120))


def estado():
    cont = get('/__dev/state')
    return {t: {r.get('id', json.dumps(r, sort_keys=True)): r for r in get(f'/__dev/state?table={t}')} for t, n in cont.items()
            if n and not any(f in t for f in FORA)}


def main():
    nome = sys.argv[1]
    so_ver = '--ver' in sys.argv
    atual = estado()
    post('/__dev/reset')
    r = post('/__dev/seed', {'files': BASE})
    if not r.get('ok'):
        raise SystemExit(f'semente base: {r}')
    base = estado()
    out = {'_doc': f'T12 · estado depois do capítulo ({nome}), cumulativo desde a base da aula (t12/inicio). Gerado por rec/t12/t12_semente.py a partir da instância do ensaio.'}
    patch, remove = {}, {}
    for t in sorted(set(atual) | set(base)):
        a, b = atual.get(t, {}), base.get(t, {})
        novos = [a[k] for k in a if k not in b]
        mud = []
        for k in a:
            if k in b and a[k] != b[k]:
                st = {c: v for c, v in a[k].items() if b[k].get(c) != v}
                mud.append({'match': {'id': k}, 'set': st})
        sai = [{'id': k} for k in b if k not in a]
        if novos:
            out[t] = novos
        if mud:
            patch[t] = mud
        if sai:
            remove[t] = sai
        if novos or mud or sai:
            print(f'  {t}: +{len(novos)} novas, {len(mud)} alteradas, -{len(sai)} removidas'
                  + (('  ' + '; '.join(sorted({c for m in mud for c in m["set"]}))[:200]) if mud else ''))
    if patch:
        out['_patch'] = patch
    if remove:
        out['_remove'] = remove
    if so_ver:
        return
    os.makedirs(SAIDA, exist_ok=True)
    caminho = os.path.join(SAIDA, f'{nome}.json')
    json.dump(out, open(caminho, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print(f'gravado {os.path.relpath(caminho, os.path.join(HERE, "..", ".."))}')


if __name__ == '__main__':
    main()
