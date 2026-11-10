#!/usr/bin/env python3
"""T19 · prepara o ensaio RÁPIDO de um capítulo: copia rec/t19/capNN.json para rec/t19/_ens/capNN.json sem os `at` (o robô não espera a
fala: os passos correm um atrás do outro) e com cauda curta. Serve para achar seletor errado, passo que falha e estado que não fecha.
NÃO serve para medir `lateBy` nem o ritmo (isso é o ensaio completo, sem --rapido).
Uso: python3 -I rec/t19/ensaio.py NN"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
n = int(sys.argv[1])
d = json.load(open(os.path.join(HERE, f'cap{n:02d}.json'), encoding='utf8'))
passos = []
for st in d['steps']:
    st = dict(st)
    st.pop('at', None)
    if st.get('do') == 'mark':
        continue
    passos.append(st)
d['steps'] = passos
d['tail'] = 0.4
os.makedirs(os.path.join(HERE, '_ens'), exist_ok=True)
saida = os.path.join(HERE, '_ens', f'cap{n:02d}.json')
json.dump(d, open(saida, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print(f'ensaio rápido: {len(passos)} passos -> {os.path.relpath(saida, HERE)}')
