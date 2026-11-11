#!/usr/bin/env python3
"""T0 · ensaio rápido das duas versões: python3 -I rec/t00/t00_ensaio.py [NN ...] -> rec/t00/_ens/capNN.json e capNN.9x16.json"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
quais = [int(a) for a in sys.argv[1:]] or range(14)
os.makedirs(os.path.join(HERE, '_ens'), exist_ok=True)
for n in quais:
    for suf in ('', '.9x16'):
        d = json.load(open(os.path.join(HERE, f'cap{n:02d}{suf}.json'), encoding='utf8'))
        d['steps'] = [{k: v for k, v in s.items() if k != 'at'} for s in d['steps'] if s.get('do') != 'mark']
        d['tail'] = 0.4
        json.dump(d, open(os.path.join(HERE, '_ens', f'cap{n:02d}{suf}.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print('ok')
