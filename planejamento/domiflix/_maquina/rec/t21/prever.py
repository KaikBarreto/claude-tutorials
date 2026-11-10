#!/usr/bin/env python3
"""T21 · prévia do ritmo (sem abrir o navegador; molde do rec/t15/prever.py): simula o robô passo a passo com a DURAÇÃO MEDIDA de cada
passo na última gravação (rec/t21/t21-capNN.actions.json) ou, com --ens, no último ensaio --rapido (rec/t21/_ens/), e o `at` do roteiro
atual (rec/t21/capNN.json). O passo medido é achado pelo `do` + `label`, na ordem (passo novo, sem medida: modelo de custo).
Imprime o atraso previsto (início do passo - `at`) e o das marcas Ln. Estimativa: no ensaio rápido os passos correm colados, então as
esperas (waitFor) tendem a sair maiores que na gravação. A verdade é o actions.json da gravação (resumo.py).
Uso: python3 -I rec/t21/prever.py 02 05 10 [--tudo] [--ens]"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def digitacao(st, cps_cap):
    """tempo só da digitação: ~1,45/cps + 0,03 s por letra (medido no T22: fase 1 a 9 letras/s, 5,5 s para 26 letras; T15 final a 30, 0,06 a 0,07 s)"""
    return len(st.get('text', '')) * (1.45 / (st.get('cps') or cps_cap) + 0.03)


def modelo(st, cps_cap=9):
    d = st['do']
    if d == 'mark':
        return 0.0
    if d == 'click':
        return 0.85
    if d == 'hover':
        return 0.6 + st.get('seconds', 0.9)
    if d == 'type':
        return (0.3 if st.get('noClick') else 0.9) + digitacao(st, cps_cap)
    if d == 'press':
        return 0.2
    if d in ('pause', 'wait'):
        return st.get('seconds', 1)
    if d == 'waitFor':
        return 0.3
    if d == 'scroll':
        return 1.1 if st.get('point') else 2.5
    if d == 'drag':
        return 2.8
    if d == 'eval':   # fase 2 (T21): a rolagem suave por eval (js_main_ate) só termina depois de `dur_ms`
        m = re.search(r'\(t-t0\)/(\d+)', st.get('js', ''))
        return int(m.group(1)) / 1000 + 0.05 if m else 0.05
    return 0.5


def main():
    tudo = '--tudo' in sys.argv
    for a in [x for x in sys.argv[1:] if not x.startswith('--')]:
        n = f'{int(a):02d}'
        rot = json.load(open(os.path.join(HERE, f'cap{n}.json'), encoding='utf8'))
        p_med = os.path.join(HERE, '_ens' if '--ens' in sys.argv else '', f't21-cap{n}.actions.json')
        med = json.load(open(p_med))['actions'] if os.path.exists(p_med) else []
        med = [m for m in med if m.get('do') != 'mark']
        j, achados, total = 0, 0, 0
        print(f"=== cap{n}: {len(rot['steps'])} passos; medidas de {os.path.relpath(p_med, HERE) if med else '(nenhuma: só o modelo)'}")
        t, pior = 0.0, (0.0, '')
        for st in rot['steps']:
            at = st.get('at')
            ini = max(t, at) if at is not None else t
            atraso = ini - at if at is not None else 0.0
            fonte = ''
            if st.get('do') == 'mark':
                dur = 0.0
            else:
                total += 1
                m = None
                for k in range(j, min(len(med), j + 8)):
                    if med[k].get('do') == st.get('do') and (med[k].get('label') or '') == (st.get('label') or ''):
                        m, j = med[k], k + 1
                        break
                if m is None or st.get('do') in ('pause', 'wait'):   # pausa: vale o `seconds` ATUAL do roteiro
                    dur, fonte = modelo(st, rot.get('cps') or 9), (' (modelo)' if m is None else '')
                    achados += m is not None
                elif st.get('do') == 'type':   # a velocidade pode ter mudado desde a medida: deslocamento medido + digitação pelo modelo
                    dur = ((m.get('tAct') or m['tStart']) - m['tStart']) + digitacao(st, rot.get('cps') or 9)
                    achados += 1
                elif st.get('do') == 'hover' and m.get('tAct') is not None:
                    dur = (m['tAct'] - m['tStart']) + st.get('seconds', 0.9)   # deslocamento medido + o `seconds` ATUAL do roteiro
                    achados += 1
                else:
                    dur = m['tEnd'] - m['tStart']
                    achados += 1
            rot_ = (st.get('label') or st.get('name') or '')[:52]
            if atraso > pior[0]:
                pior = (atraso, rot_)
            flag = '  <-- ATRASO' if atraso >= 0.8 else ('  ~' if atraso >= 0.3 else '')
            if tudo or flag or st.get('do') == 'mark':
                print(f"  {ini:6.2f}->{ini + dur:6.2f} at={at if at is not None else '-':>6} {st['do']:7} {rot_}{fonte}{flag}{f' {atraso:.2f}' if flag else ''}")
            t = ini + dur
        print(f"  fim previsto {t:.2f} s; maior atraso {pior[0]:.2f} s em \"{pior[1]}\"; {achados}/{total} passos com duração medida")


if __name__ == '__main__':
    main()
