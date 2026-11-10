#!/usr/bin/env python3
"""T15 · prepara o ensaio RÁPIDO de um capítulo: copia rec/t15/capNN.json para rec/t15/_ens/capNN.json sem os `at` (o robô não espera a
fala: os passos correm um atrás do outro) e com cauda curta. Serve para achar seletor errado, passo que falha e estado que não fecha.
NÃO serve para medir `lateBy` nem o ritmo (isso é o ensaio completo, sem --rapido).
Uso: python3 -I rec/t15/ensaio.py NN"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
n = sys.argv[1] if sys.argv[1].endswith('b') else f'{int(sys.argv[1]):02d}'   # '09b' = trecho do celular
d = json.load(open(os.path.join(HERE, f'cap{n}.json'), encoding='utf8'))
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
saida = os.path.join(HERE, '_ens', f'cap{n}.json')
json.dump(d, open(saida, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print(f'ensaio rápido: {len(passos)} passos -> {os.path.relpath(saida, HERE)}')
