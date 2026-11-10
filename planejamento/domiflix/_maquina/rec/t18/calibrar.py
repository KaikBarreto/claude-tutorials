#!/usr/bin/env python3
"""T18 · calibra o ritmo de um capítulo com a DURAÇÃO REAL de cada passo medida no ensaio rápido (rec/t18/_ens/t18-capNN.actions.json).

O ensaio rápido roda os mesmos passos sem esperar a fala; a duração de cada passo (tEnd - tStart) é a mesma que ele terá na gravação
de verdade. Aqui a gente simula a linha do tempo da gravação cheia: cada passo começa em max(fim do anterior, `at`) e dura o que durou no
ensaio. Mostra onde o robô chegaria atrasado (lateBy = início real - `at`), sem abrir o navegador.

uso: python3 -I rec/t18/calibrar.py NN [NN ...] [--tudo]     (--tudo: lista todos os passos, não só os atrasados)
Ressalvas: `waitFor` e esperas de carregamento valem o do ensaio; passos de hover que o gerador divide em dois (em volta de um `mark`)
só aparecem no roteiro cheio; nesse caso a estimativa usa a soma das partes.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
tudo = '--tudo' in sys.argv
for n in [a for a in sys.argv[1:] if not a.startswith('--')]:
    n = int(n)
    cheio = json.load(open(os.path.join(HERE, f'cap{n:02d}.json'), encoding='utf8'))
    ens = json.load(open(os.path.join(HERE, '_ens', f't18-cap{n:02d}.actions.json'), encoding='utf8'))
    acts = ens['actions']
    passos = [s for s in cheio['steps'] if s['do'] != 'mark']
    print(f'=== cap{n:02d}: {len(passos)} passos no roteiro cheio, {len(acts)} ações no ensaio rápido')
    if len(passos) != len(acts):
        print('   AVISO: a contagem não bate; o alinhamento por posição pode estar errado')
    t = 0.0
    k = 0
    maior = 0.0
    for s in cheio['steps']:
        at = s.get('at')
        if s['do'] == 'mark':
            ini = max(t, at) if at is not None else t
            atraso = ini - at if at is not None else 0.0
            if atraso > 0.3 or tudo:
                print(f'   {ini:7.2f}        mark    {s.get("name", "")}  atraso {atraso:4.2f}')
            maior = max(maior, atraso)
            continue
        a = acts[k] if k < len(acts) else None
        k += 1
        dur = (a['tEnd'] - a['tStart']) if a else 0.5
        # em modo cheio o robô só espera a fala quando há `at`; sem `at`, começa assim que o anterior termina
        ini = max(t, at) if at is not None else t
        # o gesto cai ~tAct - tStart depois do início do passo
        gesto = ((a.get('tAct') or a['tStart']) - a['tStart']) if a else 0.8
        atraso = ini - at if at is not None else 0.0
        t = ini + dur
        maior = max(maior, atraso)
        flag = '  <-- ATRASO' if atraso >= 0.8 else ('  ~atraso' if atraso >= 0.3 else '')
        if flag or tudo:
            print(f'   {ini:7.2f}->{t:7.2f} (gesto ~{ini + gesto:6.2f}) at={at if at is not None else "-":>6} {s["do"]:7} dur {dur:4.2f}  {(s.get("label") or "")[:56]}{flag}')
    print(f'   maior atraso estimado: {maior:.2f} s; fim estimado {t:.1f} s')
