"""Ferramentas de olhar a fonte para planejar zoom/destaque.
  python3 kit/look.py <projeto> sheet [a b]      -> folha de contato das miniaturas (com tempo) entre a e b s
  python3 kit/look.py <projeto> frame t [t2 ...] -> quadro(s) da FONTE em resolução cheia com grade de coordenadas (px da fonte)
  python3 kit/look.py <projeto> where a b        -> caixa onde a tela mudou entre a e b s (sugestão de retângulo de zoom)
Saídas em <projeto>/look/"""
import glob, json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

proj = os.path.abspath(sys.argv[1]); cmd = sys.argv[2]; P = lambda *a: os.path.join(proj, *a)
os.makedirs(P("look"), exist_ok=True)
meta = json.load(open(P("project.json")))
FONT = ImageFont.truetype(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts", "Montserrat-700.ttf"), 22)
fmt = lambda t: f"{int(t // 60):02d}:{t % 60:04.1f}"

if cmd == "sheet":
    a = float(sys.argv[3]) if len(sys.argv) > 3 else 0; b = float(sys.argv[4]) if len(sys.argv) > 4 else 1e9
    fs = sorted(glob.glob(P("thumbs", "t*.jpg")))
    sel = [(i * 2.0, f) for i, f in enumerate(fs) if a <= i * 2.0 <= b]
    step = max(1, len(sel) // 40); sel = sel[::step]
    tw, th = Image.open(sel[0][1]).size; cols = 5; rows = (len(sel) + cols - 1) // cols
    sh = Image.new("RGB", (cols * tw, rows * (th + 28)), (20, 20, 20)); d = ImageDraw.Draw(sh)
    for k, (t, f) in enumerate(sel):
        x, y = (k % cols) * tw, (k // cols) * (th + 28); sh.paste(Image.open(f), (x, y + 28)); d.text((x + 6, y + 3), fmt(t), font=FONT, fill=(0, 197, 151))
    out = P("look", f"sheet_{int(a)}_{int(min(b, 99999))}.jpg"); sh.save(out, quality=85); print(out)

elif cmd == "frame":
    for t in map(float, sys.argv[3:]):
        out = P("look", f"frame_{t:08.2f}.png")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", meta["src"], "-frames:v", "1", out], check=True)
        im = Image.open(out).convert("RGB"); d = ImageDraw.Draw(im, "RGBA"); W, H = im.size
        step = 100 if W <= 2000 else 200
        for x in range(0, W, step):
            d.line([(x, 0), (x, H)], fill=(255, 0, 90, 70 if x % (step * 5) else 150), width=1); d.text((x + 3, 3), str(x), font=FONT, fill=(255, 0, 90, 230))
        for y in range(0, H, step):
            d.line([(0, y), (W, y)], fill=(255, 0, 90, 70 if y % (step * 5) else 150), width=1); d.text((3, y + 3), str(y), font=FONT, fill=(255, 0, 90, 230))
        im.save(out); print(out, im.size)

elif cmd == "where":
    a, b = float(sys.argv[3]), float(sys.argv[4]); A = np.load(P("activity.npz"))
    m = (A["t"] >= a) & (A["t"] <= b) & (A["px"] > 8); bx = A["box"][m]
    if not len(bx): print("sem mudança de tela nesse trecho"); sys.exit()
    # ignora mudanças de tela inteira (troca de página) p/ achar a região de trabalho
    small = bx[((bx[:, 2] - bx[:, 0]) * (bx[:, 3] - bx[:, 1])) < 0.35 * meta["w"] * meta["h"]]
    use = small if len(small) else bx
    x0, y0 = np.percentile(use[:, 0], 5), np.percentile(use[:, 1], 5); x1, y1 = np.percentile(use[:, 2], 95), np.percentile(use[:, 3], 95)
    print(json.dumps({"rect": [int(x0), int(y0), int(x1 - x0), int(y1 - y0)], "amostras": int(m.sum()), "trocas_de_tela": int(len(bx) - len(small))}))
