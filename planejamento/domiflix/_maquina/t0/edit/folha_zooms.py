"""Folhas de conferência de TODOS os zooms (Kaik 30/10: "conferir os zooms"; zoom fora do alvo nunca deve acontecer).
Para cada capítulo renderizado (sidecar out/capNN/capNN.edit.json): um quadro com o zoom já assentado (s + 1,6 s) e um
quadro ~1 s depois de cada troca de alvo da câmera, com o tempo e o zoom no canto. Tira os quadros do MP4 do capítulo.
uso: python3 -I folha_zooms.py out/folhas_zoom [cap00 cap01 ...]   -> out/folhas_zoom/zooms_01.jpg, zooms_02.jpg ...
"""
import glob, json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(sys.argv[1]); os.makedirs(OUT, exist_ok=True)
caps = sys.argv[2:] or sorted(os.path.basename(os.path.dirname(p)) for p in glob.glob(os.path.join(HERE, "out", "cap*", "cap*.edit.json")))
FT = os.path.join(os.path.dirname(os.path.dirname(HERE)), "kit", "fonts", "Montserrat-700.ttf")
font = ImageFont.truetype(FT, 18) if os.path.exists(FT) else None
TW, TH, COLS, ROWS = 480, 270, 4, 4

marks = []
for c in caps:
    side = json.load(open(os.path.join(HERE, "out", c, c + ".edit.json"))); t0 = side.get("start", 0.0); dur = side["dur"]
    for r in side["regions"]:
        if r["z"] <= 1.05: continue
        ts = [(r["s"] + 1.6, f"z{r['z']:.2f} {r['src']}")]
        tr_ = r.get("track") or []; vw = 3097.0 / r["z"]  # vw0 do palco 2560x1600 com margem 44
        for k in range(1, len(tr_)):  # só trocas de verdade (campo largo repete a mesma âncora a cada tecla)
            if abs(tr_[k][1] - tr_[k - 1][1]) + abs(tr_[k][2] - tr_[k - 1][2]) > 0.05 * vw: ts.append((tr_[k][0] + 1.0, "troca de alvo"))
        for t, lab in ts:
            if t < r["e"] and 0 <= t - t0 < dur: marks.append((c, t - t0, lab))
print(len(marks), "quadros")
tmp = os.path.join(OUT, "_q"); os.makedirs(tmp, exist_ok=True); tiles = []
for i, (c, t, lab) in enumerate(marks):
    f = os.path.join(tmp, f"{i:04d}.jpg")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", os.path.join(HERE, "out", c, c + ".mp4"), "-frames:v", "1",
                    "-vf", f"scale={TW}:{TH}", f], check=True)
    im = Image.open(f).convert("RGB"); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, TW, 24], fill=(0, 0, 0)); d.text((6, 3), f"{c} {t:5.1f}s {lab}", fill=(255, 220, 0), font=font)
    tiles.append(im)
n = 0
for j in range(0, len(tiles), COLS * ROWS):
    sheet = Image.new("RGB", (COLS * TW, ROWS * TH), "white")
    for k, im in enumerate(tiles[j:j + COLS * ROWS]): sheet.paste(im, ((k % COLS) * TW, (k // COLS) * TH))
    n += 1; sheet.save(os.path.join(OUT, f"zooms_{n:02d}.jpg"), quality=85)
print(n, "folhas em", OUT)
