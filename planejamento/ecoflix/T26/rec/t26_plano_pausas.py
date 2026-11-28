#!/usr/bin/env python3
"""T26 · propõe os respiros (pausas.py) de um capítulo a partir dos atrasos da gravação final (lateBy >= 0,3).
Regra (aprendida na 1a rodada, 28/11): o respiro tem de cair DEPOIS do passo lento e ANTES da palavra que ancora o primeiro passo atrasado:
  - primeiro atrasado = marca Lk  -> vão logo antes do começo da linha k da voz;
  - primeiro atrasado = outro passo -> vão logo antes da palavra do `at=c.A(linha, 'palavra', folga)` desse rótulo em gerar.py.
(Respiro antes do passo lento só atrasa o início do trecho denso e não resolve: cap06/cap07 da 1a rodada.) Duração = maior atraso da corrida + folga.
Tempos: as ações vêm da gravação (com as pausas que já existiam); tudo é convertido para o tempo ORIGINAL da voz. Só imprime.
uso: python3 -I rec/t26/t26_plano_pausas.py NN [folga]      SEM_PAUSAS=1 se a gravação analisada foi feita SEM respiros (capNN.json sem pausas)"""
import json, sys, os, re
H = os.path.dirname(os.path.abspath(__file__)); TUT = os.path.normpath(os.path.join(H, '..', '..'))
nn = f'{int(sys.argv[1]):02d}'; folga = float(sys.argv[2]) if len(sys.argv) > 2 else 0.3
A = json.load(open(f'{H}/t26-cap{nn}.actions.json'))['actions']
EM = f'{TUT}/t26/narracao/emendas/cap{nn}.orig.json'
orig = json.load(open(EM if os.path.exists(EM) else f'{TUT}/t26/narracao/cap{nn}.json'))
pausas = [] if os.environ.get('SEM_PAUSAS') else (json.load(open(f'{TUT}/t26/narracao/cap{nn}.json')).get('pausas') or [])
vad, W, L = orig['vad'], orig['words'], orig['linhas']
G = open(f'{H}/gerar.py', encoding='utf8').read()
def orig_t(t):
    cum = 0.0
    for a, b in sorted(pausas):
        pos = a + cum
        if t >= pos + b: cum += b
        elif t > pos: return a
        else: break
    return round(t - cum, 3)
def livres():
    r = []
    ini = None
    for k in range(0, int(orig['dur'] * 100) + 1):
        t = k / 100
        ocupado = any(w['s'] < t < w['e'] for w in W)   # pausas_fino.py aceita ponto no vão REAL entre palavras, mesmo dentro do trecho de voz
        if not ocupado and ini is None: ini = t
        if ocupado and ini is not None:
            if t - ini >= 0.06: r.append((ini, t))
            ini = None
    return r
LIV = livres()
def ponto_antes(alvo, minimo):
    """último ponto livre (vão real) antes de `alvo` e depois de `minimo`"""
    for a, b in reversed(LIV):
        if a < alvo - 0.03 and b > minimo + 0.03:
            return round(max(a + 0.03, min(b - 0.03, alvo - 0.04)), 2)
    return None
def ancora(label):
    m = re.search(r"at=c\.A\((\d+), '([^']+)'(?:, ([0-9.]+))?(?:, nth=(\d+))?\)[^\n]*?label='" + re.escape(label) + "'", G)
    return m
# v4 (28/11): o atraso é SOMA de saltos. Cada passo cujo atraso sobe >= 0,4 em relação ao passo anterior com `at` pede um respiro ANTES da palavra
# que o ancora (duração = salto + folga); o respiro adia só o que vem depois dele, então cada salto precisa do seu.
ancorados = [x for x in A if x.get('at') is not None and x.get('do') != 'waitFor']
prev, ult, saltos = 0.0, 0.0, []
for x in ancorados:
    lb = x.get('lateBy') or 0.0
    d = lb - prev
    prev = lb if lb >= 0.1 else 0.0
    if d < 0.4: continue
    nome = x.get('label') or x.get('name')
    if x.get('do') == 'mark' and re.fullmatch(r'L\d+', x.get('name', '')):
        k = int(x['name'][1:]); alvo = L[k - 1]['s'] if k - 1 < len(L) else orig_t(x['at']) + 0.9
    else:
        m = ancora(x.get('label') or '')
        alvo = orig_t(x['at']) + (float(m.group(3) or 0.8) if m else 0.5)
    t = ponto_antes(alvo, ult)
    if t is None: print(f'  salto de {d:.2f} em {nome} (alvo {alvo:.2f}): SEM VÃO; aparar o robô'); continue
    saltos.append((t, round(d + folga, 1), nome, d)); ult = t
novas = {}
for t, dur, nome, d in saltos:
    k = round(t, 1); novas[k] = (t, round(novas.get(k, (0, 0))[1] + dur, 1))
    print(f'  salto de {d:.2f} em {nome}: respiro em {t:.2f} por {dur}')
vel = {round(a, 1): (a, b) for a, b in pausas}
tot = dict(vel)
for k, (t, dur) in novas.items():
    tot[k] = (tot[k][0], round(tot[k][1] + dur, 1)) if k in tot else (t, dur)
print('ADICIONAIS: ' + ' '.join(f'{t:.2f}:{d}' for t, d in sorted(novas.values())))
print('pausas.py ' + nn + ' ' + ' '.join(f'{t:.2f}:{d}' for t, d in sorted(tot.values())) + '   (lista completa: as que já existem + as novas)')
