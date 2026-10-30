"""Separa o MP3 com os nomes dos capítulos (um por vinheta, separados por [pause]) em um WAV por capítulo.
Saída: titulos/capNN.wav (48 kHz mono, com o mesmo volume da narração) + titulos/titulos.json {NN: {texto, wav, dur}}
uso: python3 -I titulos.py <titulos.mp3>"""
import json
import os
import sys

import numpy as np
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import proc  # noqa: E402

SR = 48000
try:  # títulos do tutorial (tts_textos.py → TITULOS); sem eles, os do exemplo T3
    from tts_textos import TITULOS  # noqa: E402
except ImportError:
    TITULOS = {1: "A tela de Clientes.", 2: "Cliente empresa pelo CNPJ.", 3: "Cliente pessoa física pelo CEP.", 4: "Origens.",
               5: "A ficha do cliente.", 6: "Formulário de captação.", 7: "Fornecedores.", 8: "Preparando os equipamentos.",
               9: "Cadastrando um equipamento.", 10: "quê-érre côde e etiqueta.", 11: "Recapitulando."}
ALVO_LUFS = -21.9  # média da narração dos capítulos

tid, d, words = proc.transcrever(sys.argv[1])
textos = [TITULOS[k] for k in sorted(TITULOS)]
toks = proc.tokens("\n".join(textos))
vad = json.load(open(os.path.join(d, "vad.json")))
ws = proc.alinhar(toks, words, vad)
x, sr = sf.read(os.path.join(d, "audio48k.wav"), dtype="float32")
assert sr == SR


def borda(t, lado):
    for v0, v1 in vad:
        if v0 - 0.02 <= t <= v1 + 0.02:
            return v0 - 0.04 if lado == "ini" else v1 + 0.08
    return t


def lufs(y):
    import pyloudnorm as pyln
    return pyln.Meter(SR).integrated_loudness(np.pad(y, (0, max(0, int(0.5 * SR) - len(y)))).astype(np.float64))


def legenda(t):
    """grafia da fala -> grafia da legenda (config_narracao.json → trocas)"""
    for f, l in sorted(proc.TROCAS, key=lambda p: -len(p[0])):
        t = t.replace(f, l)
    return t


out = os.path.join(HERE, "titulos")
os.makedirs(out, exist_ok=True)
info = {}
for li, k in enumerate(sorted(TITULOS)):
    fw = [w for w in ws if w["linha"] == li]
    a, b = borda(fw[0]["s"], "ini"), borda(fw[-1]["e"], "fim")
    cl = x[max(0, int(a * SR)):int(b * SR)].copy()
    g = 10 ** ((ALVO_LUFS - lufs(cl)) / 20)
    cl = cl * min(g, 2.5)
    n = int(0.006 * SR)
    cl[:n] *= np.linspace(0, 1, n)
    cl[-n:] *= np.linspace(1, 0, n)
    p = os.path.join(out, f"cap{k:02d}.wav")
    sf.write(p, cl, SR, subtype="FLOAT")
    info[f"{k:02d}"] = {"texto": legenda(TITULOS[k]), "wav": p, "dur": round(len(cl) / SR, 3),
                        "ok": min(w["ok"] for w in fw), "ouvido": " ".join(w["ouvido"] for w in fw)}
    print(f"cap{k:02d}: {len(cl) / SR:.2f}s  ouvido: {info[f'{k:02d}']['ouvido']!r}")
json.dump(info, open(os.path.join(out, "titulos.json"), "w"), ensure_ascii=False, indent=1)
