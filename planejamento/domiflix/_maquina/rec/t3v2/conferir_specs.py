#!/usr/bin/env python3
"""T3 v2 · confere se todo rótulo citado em t3v2/edit/caps/specs.json existe no roteiro do robô do capítulo (rec/t3v2/capNN.json).
Com --gravacao confere também no <nome>.actions.json gravado (o que o montar_cap.py realmente usa).
uso: python3 -I rec/t3v2/conferir_specs.py [NN ...] [--gravacao]"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TUT = os.path.normpath(os.path.join(HERE, '..', '..'))
SPECS = os.path.join(TUT, 't3v2', 'edit', 'caps', 'specs.json')


def rotulos(nn, gravacao):
    if gravacao:
        p = os.path.join(HERE, f't3v2-cap{nn}.actions.json')
        if not os.path.exists(p):
            return None
        return {a.get('label') for a in json.load(open(p, encoding='utf8'))['actions'] if a.get('ok', True) and a.get('label')}
    p = os.path.join(HERE, f'cap{nn}.json')
    if not os.path.exists(p):
        return None
    return {s.get('label') for s in json.load(open(p, encoding='utf8'))['steps'] if s.get('label')}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    grav = '--gravacao' in sys.argv
    specs = json.load(open(SPECS, encoding='utf8'))
    quais = [f'{int(a):02d}' for a in args] or sorted(specs)
    faltas = 0
    for nn in quais:
        sp = specs.get(nn)
        if sp is None:
            print(f'cap{nn}: sem spec')
            continue
        labs = rotulos(nn, grav)
        if labs is None:
            print(f'cap{nn}: ainda sem {"gravação" if grav else "roteiro do robô"} (pulado)')
            continue
        usados = []
        for z in sp.get('zooms', []):
            usados += [z['de']] + ([z['ate']] if 'ate' in z else []) + ([z['fim']] if isinstance(z.get('fim'), str) and not z['fim'].startswith('+') else [])
        usados += [s['passo'] for s in sp.get('spots', [])]
        ruins = [u for u in usados if u not in labs]
        faltas += len(ruins)
        print(f'cap{nn}: {len(usados)} rótulos citados, {len(ruins)} faltando' + (' -> ' + '; '.join(repr(r) for r in ruins) if ruins else ''))
    sys.exit(1 if faltas else 0)


main()
