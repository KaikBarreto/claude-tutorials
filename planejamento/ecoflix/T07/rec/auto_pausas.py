#!/usr/bin/env python3
"""T07 · escolhe parada mais curta do cursor (DWELL do gerar.py) e respiros (pausas.py) para os capítulos com gesto atrasado na gravação final.
Simula o capítulo com as durações MEDIDAS na gravação final (lidas pelo prever.py com o capNN.json de base, em /dev/shm/t07_base) e os `at` do
gerar.py atual (que lê a narração com as pausas). Cada passo parte em max(fim do anterior, at). Acha o 1º passo atrasado (>= LIM) e tenta, nesta ordem:
um respiro no último vão REAL de silêncio (vad) DENTRO da sequência atrasada (depois do último passo que partiu na hora e antes da palavra do
atrasado); sem vão, parada mais curta do cursor (fator 0.6, depois 0.4). Uso: python3 -I rec/t07/auto_pausas.py NN [NN ...]; deixa a narração e o
capNN.json no estado final e imprime DWELL e respiros para anotar. Variável LIM (padrão 0.6)."""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NARR = os.path.normpath(os.path.join(HERE, '..', '..', 't07', 'narracao'))
BASE = os.environ.get('BASE', '/dev/shm/t07_base2')
LIM = float(os.environ.get('LIM', '0.6'))
PY = [sys.executable, '-I']


def roda(*a, env=None):
    e = dict(os.environ)
    e.update(env or {})
    return subprocess.run(PY + list(a), capture_output=True, text=True, env=e)


def duracoes_base(nn):
    """[(do, label, duração medida, seconds)] na ordem do capNN.json de base"""
    base = json.load(open(f'{BASE}/cap{nn}.json'))['steps']
    cur = os.path.join(HERE, f'cap{nn}.json')
    guarda = open(cur, encoding='utf8').read()
    open(cur, 'w', encoding='utf8').write(open(f'{BASE}/cap{nn}.json', encoding='utf8').read())
    try:
        r = roda(os.path.join(HERE, 'prever.py'), nn, '--tudo')
    finally:
        open(cur, 'w', encoding='utf8').write(guarda)
    linhas = []
    for ln in r.stdout.splitlines():
        m = re.match(r'\s*([\d.]+)->\s*([\d.]+) at=\s*([\d.-]+)\s+(\S+)\s+(.*?)(?:\s+<-- ATRASO [\d.]+|\s+~ [\d.]+)?\s*$', ln)
        if m:
            linhas.append(float(m.group(2)) - float(m.group(1)))
    assert len(linhas) == len(base), (nn, len(linhas), len(base))
    return [(st['do'], st.get('label'), d, st.get('seconds') if st['do'] == 'hover' else None) for st, d in zip(base, linhas)]


def simula(nn, dur_base, reg=()):
    """[(início, at, atraso, do, rótulo)] com o capNN.json atual"""
    cur = json.load(open(os.path.join(HERE, f'cap{nn}.json')))['steps']
    usados = {}
    t = 0.0
    out = []
    for st in cur:
        chave = (st['do'], st.get('label'))
        k = usados.get(chave, 0)
        usados[chave] = k + 1
        cands = [b for b in dur_base if (b[0], b[1]) == chave]
        if k < len(cands):
            _, _, d, sec0 = cands[k]
        else:
            d, sec0 = 0.8, None
        if st.get('label') in reg and st['do'] == 'type':
            d = 0.35
        elif st['do'] == 'hover' and sec0 is not None:
            d = max(0.2, d - (sec0 - st.get('seconds', sec0)))
        at = st.get('at')
        ini = max(t, at) if at is not None else t
        out.append((ini, at, (ini - at) if at is not None else 0.0, st['do'], st.get('label') or st.get('name') or ''))
        t = ini + d
    return out


def capa(x):
    """quanto o passo pode partir antes da palavra: parada/zoom do cursor 1.3 s; clique e digitação 0.9 s; o resto não"""
    if x[3] == 'hover' or (x[3] == 'type' and 'zoom' in x[4]):
        return 1.3
    if x[3] in ('click', 'type'):
        return 0.9
    return 0


def cfg(nn, dw, ant, reg, pts):
    print('CFG', nn, json.dumps({'dw': dw, 'ant': ant, 'reg': reg, 'pausas': sorted(pts.items())}, ensure_ascii=False))


def main(nn):
    orig_p = os.path.join(NARR, 'emendas', f'cap{nn}.orig.json')
    cur_p = os.path.join(NARR, f'cap{nn}.json')
    if os.path.exists(orig_p):
        roda(os.path.join(NARR, 'pausas.py'), nn, '--desfazer')
    d = json.load(open(orig_p if os.path.exists(orig_p) else cur_p, encoding='utf8'))
    vad = d['vad']
    words = d['words']
    gaps = [(vad[i][1], vad[i + 1][0]) for i in range(len(vad) - 1) if vad[i + 1][0] - vad[i][1] >= 0.1]
    dur_base = duracoes_base(nn)

    def fim_frase(t):
        ant = [w for w in words if w['e'] <= t + 0.02]
        return bool(ant) and bool(re.search(r'[.?!:;]$', ant[-1]['w']))

    import ast
    tab = {}
    for ln in open(os.path.join(HERE, 'gerar.py'), encoding='utf8'):
        for nome in ('DWELL', 'ANTECIPA', 'REGISTRA'):
            if ln.startswith(nome + ' = '):
                tab[nome] = ast.literal_eval(ln.split(' = ', 1)[1])
    pf = json.load(open(os.path.join(HERE, 'pausas_final.json')))
    pts = {float(t): float(x) for t, x in pf.get(str(int(nn)), [])}
    banidos = set()
    ultimo = {}
    ant = dict(tab['ANTECIPA'].get(str(int(nn)), {}))
    reg = list(tab['REGISTRA'].get(str(int(nn)), []))
    dw = tab['DWELL'].get(int(nn), 1.0)
    for volta in range(40):
        sp = sorted(pts.items())
        if sp:
            r = roda(os.path.join(NARR, 'pausas.py'), nn, *[f'{t}:{x}' for t, x in sp])
            if r.returncode:
                print(nn, 'pausas.py falhou:', (r.stdout + r.stderr)[-300:])
                return 1
        elif os.path.exists(orig_p):
            roda(os.path.join(NARR, 'pausas.py'), nn, '--desfazer')
        roda(os.path.join(HERE, 'gerar.py'), nn, env={'T07_DW': str(dw), 'T07_ANT': json.dumps(ant), 'T07_REG': json.dumps(reg)})
        lista = simula(nn, dur_base, reg)
        ruins = [i for i, x in enumerate(lista) if x[2] >= LIM and x[3] != 'mark']
        if not ruins:
            cfg(nn, dw, ant, reg, pts)
            print(f'cap{nn}: OK  DWELL {dw}  ANTECIPA {json.dumps(ant, ensure_ascii=False)}  REGISTRA {json.dumps(reg, ensure_ascii=False)}  respiros {sp}  (+{sum(pts.values()):.1f} s)')
            return 0
        j = ruins[0]
        ini_j, A, L, tipo, lab = lista[j]
        folga = {'click': 0.7, 'hover': 0.55, 'type': 0.95, 'typen': 0.05, 'press': 0.05, 'scroll': 0.15}.get(tipo, 0.0)
        k = max([i for i in range(j) if lista[i][1] is not None and lista[i][2] < 0.2] or [-1])
        lb_atual = lista[k][0] if k >= 0 else 0.0

        def p2o(x):
            acc = 0.0
            for t, x2 in sp:
                if t + acc < x - 1e-6:
                    acc += x2
            return x - acc
        Ao, lb = p2o(A) + ant.get(lab, 0), p2o(lb_atual)   # Ao sem a antecipação do próprio passo: a palavra dele é que o respiro precisa preceder
        cand = [round((a + b) / 2, 2) for a, b in gaps if lb - 0.05 <= (a + b) / 2 <= Ao + max(0.02, folga - 0.1)]
        cand = [t for t in cand if t not in banidos and not any(w['s'] - 0.01 < t < w['e'] + 0.01 for w in words)]
        if cand:
            pref = [t for t in cand if fim_frase(t)]
            t = pref[-1] if pref else cand[-1]
            if t in pts and abs(ultimo.get('L', 0) - L) < 0.05:
                banidos.add(t)   # o respiro não adiantou (o robô é o gargalo): não insiste
            else:
                pts[t] = round(pts.get(t, 0) + L + 0.2, 1)
            ultimo['L'] = L
        elif any(ant.get(lista[i][4], 0) < capa(lista[i]) - 0.05 for i in range(max(0, k - 2), j) if capa(lista[i]) > 0):
            for i in range(max(0, k - 2), j):
                if capa(lista[i]) > 0:
                    ant[lista[i][4]] = round(min(capa(lista[i]), ant.get(lista[i][4], 0) + L + 0.1), 2)
        elif any(lista[i][3] == 'hover' for i in range(max(0, k - 2), j + 1)):
            for i in range(max(0, k - 2), j + 1):
                if lista[i][3] == 'hover':
                    reg.append(lista[i][4])
        elif dw > 0.45:
            dw = 0.6 if dw >= 1.0 else 0.4
        else:
            cfg(nn, dw, ant, reg, pts)
            print(f'cap{nn}: SEM SOLUÇÃO para "{lab}" (atraso {L:.2f}, {lb:.1f}-{Ao:.1f}); DWELL {dw}, respiros {sp}, ANTECIPA {ant}')
            return 3
    print(f'cap{nn}: não convergiu', pts, dw)
    return 2


if __name__ == '__main__':
    rc = 0
    for n in sys.argv[1:]:
        rc |= main(f'{int(n):02d}')
    sys.exit(rc)
