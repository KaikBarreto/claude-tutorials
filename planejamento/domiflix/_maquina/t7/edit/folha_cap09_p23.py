#!/usr/bin/env python3
"""T7 · folha do cap09 renderizado de 28 a 36 s, a cada 0,25 s (conferência do P23: a linha "data:image..." da assinatura
não pode aparecer, salvo alguns quadros na transição). Quadros do out/cap09/cap09.mp4, em grade com o tempo de cada um.
uso: python3 -I t7/edit/folha_cap09_p23.py [de=28] [ate=36] [passo=0.25]  -> t7/edit/out/cap09/cap09.folha_p23_28-36.jpg"""
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
V = os.path.join(HERE, "out", "cap09", "cap09.mp4")
a = [float(x) for x in sys.argv[1:4]] + [28.0, 36.0, 0.25][len(sys.argv[1:4]):]
de, ate, passo = a
ts = [round(de + k * passo, 3) for k in range(int(round((ate - de) / passo)) + 1)]
W, COLS = 480, 6
tmp = tempfile.mkdtemp(prefix="folha09_")
ims = []
for t in ts:
    p = os.path.join(tmp, f"{t:07.3f}.png")
    subprocess.run(["nice", "-n", "10", "ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", V, "-frames:v", "1",
                    "-vf", f"scale={W}:-1", p], check=True)
    ims.append((t, Image.open(p).convert("RGB")))
h = ims[0][1].height
rows = (len(ims) + COLS - 1) // COLS
folha = Image.new("RGB", (COLS * (W + 8) + 8, rows * (h + 30) + 8), "white")
d = ImageDraw.Draw(folha)
for k, (t, im) in enumerate(ims):
    x, y = 8 + (k % COLS) * (W + 8), 8 + (k // COLS) * (h + 30)
    d.text((x + 4, y + 4), f"cap09 t = {t:.2f} s", fill="black")
    folha.paste(im, (x, y + 22))
out = os.path.join(HERE, "out", "cap09", f"cap09.folha_p23_{int(de)}-{int(ate)}.jpg")
folha.save(out, quality=88)
for f in os.listdir(tmp):
    os.remove(os.path.join(tmp, f))
os.rmdir(tmp)
print(f"{len(ims)} quadros -> {out}")
