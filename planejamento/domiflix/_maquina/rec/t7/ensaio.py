#!/usr/bin/env python3
"""T7 · prepara o ensaio RÁPIDO de um capítulo: copia rec/t7/capNN.json para rec/t7/_ens/capNN.json sem os `at` (o robô não espera a
fala: os passos correm um atrás do outro) e com cauda curta. Serve para achar seletor errado, passo que falha, estado que não
fecha e para gerar o apos-capNN do encadeamento. NÃO serve para medir `lateBy` nem o ritmo (isso é o ensaio completo, sem --rapido).
Uso: python3 -I rec/t7/ensaio.py NN"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
n = int(sys.argv[1])
d = json.load(open(os.path.join(HERE, f'cap{n:02d}.json'), encoding='utf8'))
passos = []
for st in d['steps']:
    st = dict(st)
    st.pop('at', None)
    if st.get('do') == 'upload':
        st['file'] = '../' + st['file']   # o `upload` resolve o caminho pela pasta do roteiro (aqui, _ens/)
    if st.get('do') == 'mark':
        continue
    passos.append(st)
# 1.38.21: sonda final (sem gesto): gaveta de novidades da versão e avisos de erro do app visíveis no fim do capítulo
passos.append({'do': 'eval', 'js': "({novidades:/novidades|nova vers|Atualiza(ç|c)ão disponível/i.test(document.body.innerText),"
               "avisosErro:[...document.querySelectorAll('[role=status],[role=alert],li[data-state]')].map(e=>e.innerText.trim().slice(0,80)).filter(t=>/não foi possível|erro|tente novamente|indispon/i.test(t)),"
               "dialogos:[...document.querySelectorAll('[role=dialog]')].map(e=>e.innerText.trim().slice(0,40))})", 'label': 'sonda final'})
d['steps'] = passos
d['tail'] = 0.4
os.makedirs(os.path.join(HERE, '_ens'), exist_ok=True)
saida = os.path.join(HERE, '_ens', f'cap{n:02d}.json')
json.dump(d, open(saida, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print(f'ensaio rápido: {len(passos)} passos -> {os.path.relpath(saida, HERE)}')
