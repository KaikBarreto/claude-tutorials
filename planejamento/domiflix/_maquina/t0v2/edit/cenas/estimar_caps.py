#!/usr/bin/env python3
"""Tempos ESTIMADOS (2,6 palavras/s) dos capítulos do T0 v2, no formato do capNN.json, só para conferir as cenas antes da voz.
Quando a voz existir, use o capNN.json real (narracao/): as cenas leem as mesmas palavras. Uso: python3 estimar_caps.py"""
import json, os, re, importlib.util
H = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('tts', os.path.join(H, '..', '..', 'narracao', 'tts_textos.py'))
p = os.path.join('/home/claude/claude-tutorials/planejamento/domiflix/T00v2/narracao/tts_textos.py')
spec = importlib.util.spec_from_file_location('tts', p); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
for cap, txt in m.CAPS.items():
    t, words, linhas = 0.4, [], []
    for i, l in enumerate(x for x in txt.split('\n') if x.strip()):
        s0 = t
        for w in l.split():
            d = 0.38 + 0.012 * len(w) + (0.25 if w[-1] in ',:;' else 0) + (0.4 if w[-1] in '.?!' else 0)
            words.append({'w': w, 'linha': i, 's': round(t, 3), 'e': round(t + d * .8, 3)}); t += d
        linhas.append({'i': i, 'texto': l, 's': round(s0, 3), 'e': round(t, 3)}); t += 0.25
    json.dump({'cap': cap, 'dur': round(t, 3), 'words': words, 'linhas': linhas}, open(os.path.join(H, 'est', f'cap{cap:02d}.json'), 'w'), ensure_ascii=False)
    print(cap, round(t, 1), len(words))
