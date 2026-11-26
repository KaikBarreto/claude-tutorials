#!/usr/bin/env python3
"""T13 · antecipa os `at` do robô (rodar DEPOIS do gerar.py): com as durações MEDIDAS na gravação final (rec/t13/_med/), agenda de trás
para frente: cada passo começa, no máximo, quando o seguinte precisa dele (at_i' = min(at_i, at_{i+1}' - dur_i)), mas nunca mais que LIM s antes do
`at` original. Assim uma sequência densa começa a tempo em vez de chegar atrasada. O que sobrar (limite) aparece no 'previsto' e pede respiro.
Uso: python3 -I rec/t13/t13_retime.py NN [--lim 0.8] [--alvo 0.3]   (alvo: folga de segurança em s)"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import t13_plano_pausas as PL   # noqa  (importa simula; main() só roda via __main__)


PIN = {('18', 'PDF (abre a janela)')}


def main():
    nn = f'{int(sys.argv[1]):02d}'
    lim = float(sys.argv[sys.argv.index('--lim') + 1]) if '--lim' in sys.argv else float(os.environ.get('T13_LIM', 0.8))
    folga = float(sys.argv[sys.argv.index('--alvo') + 1]) if '--alvo' in sys.argv else 0.3
    p = os.path.join(HERE, f'cap{nn}.json')
    rot = json.load(open(p, encoding='utf8'))
    sim, fim = PL.simula(nn)
    steps = rot['steps']
    novo = [None] * len(steps)
    prox = None   # início máximo permitido do passo seguinte (com `at`) menos as durações dos sem `at` no caminho
    for i in range(len(steps) - 1, -1, -1):
        st, ini, at, atr, dur = sim[i]
        if at is None:
            if prox is not None:
                prox -= dur
            continue
        novo_at = at if prox is None else min(at, prox - dur - folga)
        novo_at = max(novo_at, at - lim)
        if (nn, st.get('label')) in PIN: novo_at = at   # o menu Exportar tem de ficar aberto até "Excel." (cap18)
        novo[i] = round(novo_at, 2)
        prox = novo_at
    # os passos com `at` na ordem do roteiro precisam ficar em ordem não decrescente
    ult = 0.0
    for i, st in enumerate(steps):
        if novo[i] is None: continue
        novo[i] = max(novo[i], ult) if novo[i] < ult else novo[i]
        ult = novo[i]
        st['at'] = novo[i]
    json.dump(rot, open(p, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    sim2, fim2 = PL.simula(nn)
    pior = max(sim2, key=lambda s: s[3])
    movidos = sum(1 for i, st in enumerate(steps) if novo[i] is not None and abs(novo[i] - sim[i][2]) > 0.01)
    maxant = max([sim[i][2] - novo[i] for i in range(len(steps)) if novo[i] is not None] or [0])
    print(f'cap{nn}: {movidos} passos antecipados (até {maxant:.2f} s); atraso previsto {pior[3]:.2f} s em {(pior[0].get("label") or pior[0].get("name"))!r}')


if __name__ == '__main__':
    main()
