#!/usr/bin/env python3
"""T05 · refaz os tempos (t0, duração e `at`) das cenas de Windows com a VOZ REAL.
Os JSON de cena (t05/windows/*.json) foram cronometrados com a voz estimada (t05/narracao/estimado/capNN.json). Como o texto é o mesmo, a palavra
k da voz estimada é a palavra k da voz real: cada instante da cena (t0 + at) vira "palavra mais próxima + folga" e a folga NÃO encolhe (o cursor
leva o mesmo tempo para chegar). Uso: python3 -I rec/t05/t05_cenas_retempo.py [--grava]   (sem --grava só imprime a tabela)"""
import json, os, re, sys, glob
TUT = '/home/claude/ecoflix'; W = f'{TUT}/t05/windows'; N = f'{TUT}/t05/narracao'
GRAVA = '--grava' in sys.argv
def pal(cap, estimado):
    d = json.load(open(f'{N}/{"estimado/" if estimado else ""}cap{cap:02d}.json'))
    return [(w['s'], w['e']) for w in d['words']]
def mapa(cap):
    a, b = pal(cap, True), pal(cap, False)
    assert len(a) == len(b), (cap, len(a), len(b))
    return a, b
def novo(cap, t):
    """instante `t` da voz estimada -> instante equivalente da voz real"""
    a, b = mapa(cap)
    k = min(range(len(a)), key=lambda i: abs(a[i][0] - t))
    return b[k][0] + (t - a[k][0]), k

# (t0, fim) de cada cena na linha do tempo da VOZ REAL (s do capítulo). Fronteiras coladas onde as cenas se seguem; ancoradas em começos de linha da fala.
FRONT = {
 'cap02_1_download': (6.18, 20.80), 'cap02_2_smartscreen': (20.80, 29.60), 'cap02_3_instalador': (29.60, 56.20),
 'cap04_4_impressao': (12.40, 33.23),
 'cap06_5_destrava': (22.79, 29.78), 'cap06_6_configurar': (29.78, 76.82),
 'cap09_7_sair': (0.0, 7.00), 'cap09_8_atalho': (33.11, 38.40),
 'cap10_9_atualizar': (7.16, 31.65), 'cap10_10_menu': (31.65, 42.72),
}
PAGINA = {2: 't05-cap02w', 4: 't05-cap04w', 6: 't05-cap06w', 9: 't05-cap09w', 10: 't05-cap10'}   # gravação que vira a página do navegador
BAK = f'{W}/estimado'; os.makedirs(BAK, exist_ok=True)
for f in sorted(glob.glob(f'{W}/cap*_*.json')):
    nome = os.path.basename(f)[:-5]
    if nome not in FRONT: continue
    if not os.path.exists(f'{BAK}/{nome}.json'):
        import shutil; shutil.copy2(f, f'{BAK}/{nome}.json')
    s = json.load(open(f'{BAK}/{nome}.json')); cap = int(nome[3:5])
    t0 = float(re.search(r't0 = ([0-9,]+) s', s['_leia']).group(1).replace(',', '.'))
    n0, n1 = FRONT[nome]; dur = round(n1 - n0, 2)
    print(f"== {nome} cap{cap:02d}: t0 {t0} -> {n0}; fim {n1}; duração {s['duracao']} -> {dur}")
    for p in s['passos']:
        if p['at'] < 0: continue
        nt, k = novo(cap, t0 + p['at'])
        a = max(0.0, round(nt - n0, 2))
        if a > dur - 0.05: print(f"   !! passo {p['do']} {p.get('alvo')} em {a} passa do fim {dur}")
        p['at'] = a
    # ordem de execução preservada (o `at` nunca anda para trás dentro da lista original)
    ult = -9
    for p in s['passos']:
        if p['at'] < 0: continue
        if p['at'] < ult: p['at'] = ult
        ult = p['at']
    s['duracao'] = dur
    s['_leia'] = re.sub(r't0 = [0-9,]+ s', f"t0 = {str(n0).replace('.', ',')} s", s['_leia'])
    s['_leia'] += f" [VOZ REAL 1.60.22: t0 {n0}, fim {n1}; página = gravação {PAGINA[cap]}]"
    nav = s['navegador']
    nav['pagina'] = {'gravacao': {'video': f'../../rec/t05/{PAGINA[cap]}.mp4', 'telemetria': f'../../rec/t05/{PAGINA[cap]}.telemetry.json',
                                  'acoes': f'../../rec/t05/{PAGINA[cap]}.actions.json', 'de': 0.0, 'inicio': n0, 'ate': round(n1 + 0.5, 2)}}
    if '--grava' in sys.argv:
        json.dump(s, open(f, 'w'), ensure_ascii=False, indent=1)
print('gravado' if '--grava' in sys.argv else 'simulação (use --grava)')
