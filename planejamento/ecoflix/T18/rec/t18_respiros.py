#!/usr/bin/env python3
"""T18 · acha e aplica os respiros (pausas.py) de UM capítulo a partir do atraso medido na última gravação (prever.py com a duração
real de cada passo): enquanto o primeiro passo atrasado (>= LIM s) existir, abre um respiro (atraso + 0,25 s) no último vão de voz
(>= 0,15 s) antes do `at` desse passo, regrava a narração (pausas.py, sempre a partir do original), refaz o roteiro do robô (gerar.py) e mede de novo.
Uso: python3 -I rec/t18/t18_respiros.py NN [LIM=0.7] [--zerar]     Estado: rec/t18/_resp/capNN.json (lista [T, dur] no tempo ORIGINAL).
Não grava nada; depois é só regravar o capítulo (t18_final.sh NN). Saída 0 = nenhum passo atrasado >= LIM."""
import json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); TUT = os.path.dirname(os.path.dirname(H))
NN = f'{int(sys.argv[1]):02d}'
LIM = float(next((a for a in sys.argv[2:] if not a.startswith('--')), 0.7))
NAR = os.path.join(TUT, 't18', 'narracao'); EM = os.path.join(NAR, 'emendas', f'cap{NN}.orig.json')
EST = os.path.join(H, '_resp'); os.makedirs(EST, exist_ok=True); ARQ = os.path.join(EST, f'cap{NN}.json')
pts = [] if '--zerar' in sys.argv or not os.path.exists(ARQ) else [tuple(x) for x in json.load(open(ARQ))]
if not os.path.exists(EM):
    import shutil; os.makedirs(os.path.dirname(EM), exist_ok=True); shutil.copy2(os.path.join(NAR, f'cap{NN}.json'), EM)
orig = json.load(open(EM, encoding='utf-8')); vad = orig['vad']
W = orig['words']
fronteiras = []   # (instante, pref): fronteira entre palavras; pref 2 = fim de frase, 1 = vírgula, 0 = resto
for i in range(len(W) - 1):
    x = W[i]['w'].rstrip()[-1:]
    fronteiras.append((round((W[i]['e'] + max(W[i + 1]['s'], W[i]['e'])) / 2, 3), 2 if x in '.?!:' else 1 if x == ',' else 0))
bad = set()


def run(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def aplicar():
    a = [f'{t}:{d}' for t, d in sorted(pts)]
    r = run([sys.executable, '-I', 'pausas.py', NN, *a] if a else [sys.executable, '-I', 'pausas.py', NN, '--desfazer'], NAR)
    if r.returncode: return (r.stdout + r.stderr)[-300:]
    run([sys.executable, '-I', os.path.join(H, 'gerar.py'), NN], TUT)
    json.dump(sorted(pts), open(ARQ, 'w'))
    return None


def dividir_vad(T):   # o respiro cria silêncio de verdade em T: o trecho de voz do `vad` que passa por T é partido ali (só metadado do original)
    global orig
    novo = []
    for a, b in orig['vad']:
        if a < T < b: novo += [[a, T], [T, b]]
        else: novo.append([a, b])
    if novo != orig['vad']:
        orig['vad'] = novo; json.dump(orig, open(EM, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def para_original(t):   # tempo com as pausas -> tempo original
    o = t
    for a, b in sorted(pts):
        if o >= a + b - 1e-9: o -= b
        elif o > a: o = a
    return o


ign, ult = set(), None
for it in range(40):
    err = aplicar()
    if err:
        if not ult: sys.exit('pausas.py falhou: ' + err)
        T0, d0 = ult[2], ult[3]; k = [i for i, (t, d) in enumerate(pts) if abs(t - T0) < 0.01][0]
        pts[k] = (T0, round(pts[k][1] - d0, 2))
        if pts[k][1] <= 0.01: pts.pop(k)
        bad.add(T0); print(f'  T={T0} não serve ({err.strip()[:60]}); outro vão'); ult = None
        err = aplicar()
        if err: sys.exit('pausas.py falhou: ' + err)
    out = run([sys.executable, '-I', os.path.join(H, 'prever.py'), NN], TUT).stdout
    pior = None; ats = []
    for ln in subprocess.run([sys.executable, '-I', os.path.join(H, 'prever.py'), NN, '--tudo'], cwd=TUT, capture_output=True, text=True).stdout.splitlines():
        m = re.match(r'\s*([\d.]+)->\s*([\d.]+) at=\s*([\d.]+) (\w+)\s+(.*?)(?:\s+<-- ATRASO ([\d.]+))?(?:\s+~ [\d.]+)?$', ln)
        if not m: continue
        at_, lab = float(m.group(3)), m.group(5)
        if m.group(6) and float(m.group(6)) >= LIM and lab not in ign: pior = (at_, float(m.group(6)), lab, max([a for a in ats if a < at_ - 0.05] or [0.0])); break
        if at_ > 0: ats.append(at_)
    if not pior:
        print(f'cap{NN}: ignorados (âncora constante): {sorted(ign)}'); print(f'cap{NN}: OK em {it} rodada(s); respiros {sorted(pts)} = {sum(d for _, d in pts):.2f} s'); print(out.splitlines()[-1]); sys.exit(0)
    at, atraso, rot, prev = pior
    if ult and ult[0] == rot and (abs(ult[1] - at) < 0.05 or atraso > ult[4] - 0.3 * ult[3]):   # o respiro não moveu o `at` (âncora constante no gerar.py): desfaz e ignora este passo
        T0, d0 = ult[2], ult[3]; k = [i for i, (t, d) in enumerate(pts) if abs(t - T0) < 0.01][0]
        pts[k] = (T0, round(pts[k][1] - d0, 2))
        if pts[k][1] <= 0.01: pts.pop(k)
        ign.add(rot); print(f'  "{rot}" at={at}: respiro não reduziu o atraso (âncora constante ou encadeada ao passo anterior), desfeito (ajustar no gerar.py)'); ult = None; continue
    o, po = para_original(at), para_original(prev)
    cand = [f for f in fronteiras if po + 0.9 < f[0] <= o + 0.85 and round(f[0], 2) not in bad]
    if not cand: cand = [f for f in fronteiras if po + 0.1 < f[0] <= o + 0.85 and f[1] >= 1 and round(f[0], 2) not in bad]
    if not cand and at > 0.5:
        ign.add(rot); print(f'  "{rot}" at={at} atraso {atraso}: sem fronteira de palavra entre o passo anterior ({prev}) e ele; ajustar no gerar.py'); continue
    if cand:
        mx = max(f[1] for f in cand); T = round([f[0] for f in cand if f[1] == mx][-1], 3)
    else: T = 0.0
    dividir_vad(T)
    ja = [i for i, (t, d) in enumerate(pts) if abs(t - T) < 0.01]
    d = round(atraso + 0.25, 2)
    if ja: pts[ja[0]] = (T, round(pts[ja[0]][1] + d, 2))
    else: pts.append((T, d))
    ult = (rot, at, T, d, atraso)
    if sum(d for _, d in pts) > 40 or d > 10: sys.exit(f'respiros demais ({sum(d for _, d in pts):.1f} s): conferir {pts}')
    print(f'  rodada {it}: "{rot}" at={at} atraso {atraso} -> respiro {d} s em T={T}')
print('não convergiu'); sys.exit(1)
