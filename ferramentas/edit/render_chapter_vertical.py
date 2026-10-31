"""Capítulo do formato vertical 9:16 (1080x1920): o equivalente do render_chapter.py para capítulos cuja imagem JÁ É o quadro
final vertical (palco escuro + painel + cena), como o vídeo de render_cenas_vertical.cjs (aula ilustrada). Não recompõe nem
recodifica o vídeo (nada de zoom, câmera ou cursor): confere o formato, alinha a narração ao relógio do vídeo (WAV mono 48 kHz,
o mesmo alinhamento do 16:9) e grava o arquivo ao lado (<nome>.edit.json) que o finish.py --formato 9x16 lê.
uso: python3 <tutorial>/edit/render_chapter_vertical.py <capitulo.json> [--wav narracao.wav] [--stills t1,t2,...] [--no-audio]
  --stills  PNGs de instantes soltos em <out>/stills (para conferir; nada é gravado além deles)
JSON do capítulo (o mesmo do 16:9, de capitulos_ilustrados.py): {"name","video","narration"?,"audio_offset"?,"title"?,
  "trim":{"start","end"}?, "callouts"?, "spots"?, "output":{"dir"}}. O "video" tem de ser 1080x1920 a 30 q/s.
  audio_offset: s em que a narração começa no relógio do vídeo (< 0 corta o começo dela: vídeo gerado com --de).
Recorte (trim) diferente do vídeo inteiro não é aceito aqui: gere só o trecho com render_cenas_vertical.cjs --de/--ate.
Capítulo com gravação do celular (tela real recortada) depende do render_chapter.py com a câmera do celular: não é este."""
import json
import os
import sys
from math import gcd

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
from common import Reader, probe  # noqa: E402
import vertical as V  # noqa: E402

argv = sys.argv[1:]
opt = lambda k, d=None: argv[argv.index(k) + 1] if k in argv else d  # noqa: E731
if "--help" in argv or not argv:
    print(__doc__)
    sys.exit(0)
W, H, FPS, SR = V.W, V.H, V.FPS, 48000

cj = os.path.abspath(argv[0])
base = os.path.dirname(cj)
ch = json.load(open(cj, encoding="utf-8"))
rp = lambda p: p if (p is None or os.path.isabs(p)) else os.path.normpath(os.path.join(base, p))  # noqa: E731
NAME = ch.get("name") or os.path.splitext(os.path.basename(cj))[0].replace(".chapter", "")
OUTD = rp(ch.get("output", {}).get("dir", "out"))
VIDEO = rp(ch["video"])
os.makedirs(OUTD, exist_ok=True)

info = probe(VIDEO)
if (info["w"], info["h"]) != (W, H):
    sys.exit(f"{VIDEO}: {info['w']}x{info['h']}; o capítulo vertical é o quadro final {W}x{H} (render_cenas_vertical.cjs)")
if abs(info["fps"] - FPS) > 0.01:
    sys.exit(f"{VIDEO}: {info['fps']:.2f} q/s; o vertical é {FPS} q/s")
trim = ch.get("trim", {})
t0, t1 = float(trim.get("start", 0.0)), float(trim.get("end") or info["dur"])
if t0 > 0.001 or t1 < info["dur"] - 0.05:
    sys.exit(f"trim {t0}..{t1} s diferente do vídeo inteiro (0..{info['dur']:.2f} s): gere só o trecho com render_cenas_vertical.cjs --de/--ate")
N = int(round(info["dur"] * FPS))

if "--stills" in argv:
    import cv2
    sd = os.path.join(OUTD, "stills")
    os.makedirs(sd, exist_ok=True)
    for t in map(float, opt("--stills").split(",")):
        rd = Reader(VIDEO, W, H, max(0.0, t), FPS, explicit=False)
        img = np.array(rd.next())
        rd.close()
        cv2.imwrite(os.path.join(sd, f"{NAME}_{t:07.2f}.png"), cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
        print(f"t={t:.2f} -> {sd}")
    sys.exit(0)


def alinhar_audio(out_wav):
    """narração (qualquer taxa/canais) -> WAV mono 48 kHz float32 alinhado ao vídeo (mesma duração, silêncio onde falta):
    a mesma conta do Chapter.align_audio do 16:9"""
    import soundfile as sf
    from scipy.signal import resample_poly
    n_out = int(round(N / FPS * SR))
    nar = rp(ch.get("narration"))
    off = float(ch.get("audio_offset", 0.0))
    y = np.zeros(n_out, np.float32)
    if nar:
        x, sr = sf.read(nar, dtype="float32", always_2d=True)
        x = x.mean(1)
        if sr != SR:
            g = gcd(SR, sr)
            x = resample_poly(x, SR // g, sr // g).astype(np.float32)
        s0 = int(round((t0 - off) * SR))  # amostra da narração que cai no 1º quadro
        a, b = max(0, s0), min(len(x), s0 + n_out)
        if b > a:
            y[a - s0:b - s0] = x[a:b]
        f = int(0.004 * SR)
        y[:f] *= np.linspace(0, 1, f)
        y[-f:] *= np.linspace(1, 0, f)
    sf.write(out_wav, y, SR, subtype="FLOAT")
    return nar is not None


out_wav = opt("--wav", os.path.join(OUTD, NAME + ".wav"))
has_audio = False if "--no-audio" in argv else alinhar_audio(out_wav)
side = dict(name=NAME, video=VIDEO, wav=out_wav if has_audio and os.path.exists(out_wav) else None, title=ch.get("title"), dur=N / FPS, frames=N,
            start=t0, zoom_in=[], regions=[], callouts=[{**c, "at": c["at"] - t0} for c in ch.get("callouts", [])], spots=ch.get("spots", []),
            stats=dict(formato="9x16", sem_recodificar=True))
json.dump(side, open(os.path.join(OUTD, NAME + ".edit.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)  # o finish.py lê este arquivo
print(f"ok {NAME}: {N} quadros ({N / FPS:.2f} s), {W}x{H}, áudio {'alinhado em ' + out_wav if has_audio else 'sem narração'}")
