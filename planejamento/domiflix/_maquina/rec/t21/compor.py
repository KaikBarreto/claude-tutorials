#!/usr/bin/env python3
"""T21 · compõe as sementes do dia 13: apos-cap07 (= apos-cap05 + corte-dia13, entrada dos caps 8 a 10) e apos-cap10 (igual: nada muda nos caps 8 a 10; é a semente de saída
para o T17). Os caps 8 a 10 só leem; por isso não há diff (o backend roda em outro FAKE_NOW e o diff acusaria falsas mudanças).
Rodar depois de gravar o apos-cap05:  python3 -I rec/t21/compor.py"""
import json
import os

EXTRA = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'fakebase', 'seeds-extra', 't21'))
a = json.load(open(os.path.join(EXTRA, 'apos-cap05.json'), encoding='utf8'))
b = json.load(open(os.path.join(EXTRA, 'corte-dia13.json'), encoding='utf8'))
out = {'_comentario': 'T21 · apos-cap05 + corte do dia 13/11 (OS #34 concluída, OS #35 da academia a caminho, 4 avisos no histórico). Gerado por rec/t21/compor.py.'}
for src in (a, b):
    for k, v in src.items():
        if k.startswith('_comentario'):
            continue
        if k == '_patch':
            for t, itens in v.items():
                out.setdefault('_patch', {}).setdefault(t, []).extend(itens)
        elif isinstance(v, list):
            out.setdefault(k, []).extend(v)
for nome in ('apos-cap07', 'apos-cap10'):
    with open(os.path.join(EXTRA, nome + '.json'), 'w', encoding='utf8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
print('apos-cap07.json e apos-cap10.json compostos:', {k: len(v) for k, v in out.items() if isinstance(v, list)})
