"""Emenda as frases novas (um MP3 com as frases de trocas.json separadas por [pause]) no áudio de cada capítulo,
no lugar da frase antiga, SEM mudar a duração do capítulo (a gravação de tela segue sincronizada):
frase nova começa onde a antiga começava; o resto da janela antiga vira silêncio. Troca sem frase nova = só silêncio.
Saída: emendas/capNN_v2.wav (48 kHz mono) para cada capítulo afetado; depois rode
  python3 -I proc.py NN=emendas/capNN_v2.wav ...   (refaz palavras/legendas desses capítulos)
uso: python3 -I emendar.py <frases_novas.mp3>"""
import json
import os
import subprocess
import sys

import numpy as np
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import proc  # noqa: E402

SR = 48000
T = json.load(open(os.path.join(HERE, "trocas.json")))["trocas"]
src = sys.argv[1]

# 1) transcreve o MP3 das frases novas e acha cada frase (alinhamento palavra a palavra com o texto pedido)
tid, d, words = proc.transcrever(src)
novas = [t["novo"] for t in T if t["novo"]]
texto = "\n".join(novas)
toks = proc.tokens(texto)
ws = proc.alinhar(toks, words, json.load(open(os.path.join(d, "vad.json"))))
x, sr = sf.read(os.path.join(d, "audio48k.wav"), dtype="float32")
assert sr == SR
vad = json.load(open(os.path.join(d, "vad.json")))


def borda(t, lado):
    """encosta o corte no silêncio mais próximo (VAD) para não cortar sílaba"""
    for v0, v1 in vad:
        if v0 - 0.02 <= t <= v1 + 0.02:
            return v0 - 0.04 if lado == "ini" else v1 + 0.06
    return t


clips = {}
for li, frase in enumerate(novas):
    fw = [w for w in ws if w["linha"] == li]
    a, b = borda(fw[0]["s"], "ini"), borda(fw[-1]["e"], "fim")
    clips[frase] = x[max(0, int(a * SR)):int(b * SR)].copy()
    ok = min(w["ok"] for w in fw)
    print(f"frase {li + 1}: {a:6.2f}-{b:6.2f} ({b - a:.2f}s) menor semelhança {ok:.2f}: {frase}")


def lufs(y):
    import pyloudnorm as pyln
    return pyln.Meter(SR).integrated_loudness(y.astype(np.float64)) if len(y) > SR * 0.4 else -70


def fade(y, ms=8):
    n = int(SR * ms / 1000)
    y[:n] *= np.linspace(0, 1, n)
    y[-n:] *= np.linspace(1, 0, n)
    return y


os.makedirs(os.path.join(HERE, "emendas"), exist_ok=True)
for cap in sorted({t["cap"] for t in T}):
    c = json.load(open(os.path.join(HERE, f"cap{cap:02d}.json")))
    y, sr2 = sf.read(os.path.join(c["pasta"], "audio48k.wav"), dtype="float32")
    assert sr2 == SR
    alvo = lufs(y)
    for t in [t for t in T if t["cap"] == cap]:
        # janela da frase antiga pelas palavras alinhadas (recuando/avançando para o silêncio vizinho)
        a, b = int(t["de"] * SR) - int(0.03 * SR), int(t["ate"] * SR) + int(0.05 * SR)
        y[a:b] = 0.0
        if t["novo"]:
            cl = clips[t["novo"]].copy()
            g = 10 ** ((alvo - lufs(cl)) / 20) if lufs(cl) > -60 else 1.0
            cl = fade(cl * min(g, 2.0))
            n = min(len(cl), len(y) - a)
            if len(cl) > b - a:
                print(f"  ATENÇÃO cap{cap:02d}: frase nova {len(cl) / SR:.2f}s > janela {(b - a) / SR:.2f}s (invade {(len(cl) - (b - a)) / SR:.2f}s)")
            y[a:a + n] += cl[:n]
        print(f"cap{cap:02d}: {t['de']:.2f}-{t['ate']:.2f} -> {t['novo'] or '(silêncio)'}")
    out = os.path.join(HERE, "emendas", f"cap{cap:02d}_v2.wav")
    sf.write(out, y, SR, subtype="PCM_24")
    print("  ->", out, f"{len(y) / SR:.2f}s, LUFS {lufs(y):.2f} (antes {alvo:.2f})")
