#!/usr/bin/env python3
"""T15 · prévia do ritmo (sem abrir o navegador): simula o robô passo a passo com a DURAÇÃO MEDIDA de cada passo no último ensaio
--rapido (rec/t15/_ens/t15-capNN.actions.json, mesma ordem dos passos sem as marcas) e o `at` do roteiro atual (rec/t15/capNN.json).
Imprime o atraso previsto (início do passo - `at`) e o das marcas Ln. Estimativa: no ensaio rápido os passos correm colados, então as
esperas (waitFor) tendem a sair maiores que na gravação. A verdade é o actions.json da gravação (resumo.py).
Uso: python3 -I rec/t15/prever.py 02 05 10 [--tudo] [--ens]   (padrão: durações da última GRAVAÇÃO; --ens: do ensaio rápido)"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def modelo(st, pace=0.5):
    d = st['do']
    if d == 'mark':
        return 0.0
    if d == 'click':
        return 0.8
    if d == 'hover':
        return 0.5 + st.get('seconds', 0.9)
    if d == 'type':
        return (0.3 if st.get('noClick') else 0.9) + len(st.get('text', '')) / (st.get('cps') or 9)
    if d == 'press':
        return 0.2
    if d in ('pause', 'wait'):
        return st.get('seconds', 1)
    if d == 'waitFor':
        return 0.3
    if d == 'scroll':
        return 1.1 if st.get('point') else 2.5
    if d == 'eval':
        return 0.05
    return 0.5


tudo = '--tudo' in sys.argv
for a in [x for x in sys.argv[1:] if not x.startswith('--')]:
    n = a if a.endswith('b') else f'{int(a):02d}'
    rot = json.load(open(os.path.join(HERE, f'cap{n}.json'), encoding='utf8'))
    p_ens = os.path.join(HERE, "_ens" if "--ens" in sys.argv else "", f"t15-cap{n}.actions.json")
    med = json.load(open(p_ens))['actions'] if os.path.exists(p_ens) else []
    passos = [s for s in rot['steps'] if s.get('do') != 'mark']
    med = [m for m in med if m.get('do') != 'mark']   # a gravação guarda as marcas; o ensaio rápido não
    usa = len(med) == len(passos) and all((m.get('label') or '') == (s.get('label') or '') for m, s in zip(med, passos))
    print(f"=== cap{n}: {len(rot['steps'])} passos; durações {'MEDIDAS no ensaio' if usa else 'do MODELO (ensaio ausente ou diferente)'}")
    t, k, pior = 0.0, 0, (0.0, '')
    for st in rot['steps']:
        at = st.get('at')
        ini = max(t, at) if at is not None else t
        atraso = ini - at if at is not None else 0.0
        if st.get('do') == 'mark':
            dur = 0.0
        else:
            m = med[k] if usa else None
            if m is None:
                dur = modelo(st)
            elif st.get('do') == 'hover' and m.get('tAct') is not None:
                dur = (m['tAct'] - m['tStart']) + st.get('seconds', 0.9)   # deslocamento medido + o `seconds` ATUAL do roteiro
            else:
                dur = m['tEnd'] - m['tStart']
            k += 1
        rot_ = (st.get('label') or st.get('name') or '')[:52]
        if atraso > pior[0]:
            pior = (atraso, rot_)
        flag = '  <-- ATRASO' if atraso >= 0.8 else ('  ~' if atraso >= 0.3 else '')
        if tudo or flag or st.get('do') == 'mark':
            print(f"  {ini:6.2f}->{ini + dur:6.2f} at={at if at is not None else '-':>6} {st['do']:7} {rot_}{flag}{f' {atraso:.2f}' if flag else ''}")
        t = ini + dur
    print(f"  fim previsto {t:.2f} s (narração até a marca FIM); maior atraso {pior[0]:.2f} s em \"{pior[1]}\"")
