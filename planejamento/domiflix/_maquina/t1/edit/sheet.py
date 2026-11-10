"""Folha de quadros de um capitulo ja renderizado: zoom entrando, desfoque, cursor (mao/seta/barra), clique com quique e anel,
deslize entre focos, zoom manual, saida, callout, ilustracao. Os tempos saem da propria camera/telemetria do capitulo.
uso: python3 <tutorial>/edit/sheet.py <capitulo.json> [--mp4 video.mp4] [--out folha.jpg]   (gera tambem <out>_detalhe.jpg com recortes 1:1)"""
import io, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.dont_write_bytecode = True
from chapter import Chapter  # noqa: E402
from camera import W, H, FPS  # noqa: E402
import ui  # noqa: E402  (kit)

os.nice(10); argv = sys.argv[1:]; opt = lambda k, d=None: argv[argv.index(k) + 1] if k in argv else d
C = Chapter(argv[0]); mp4 = opt("--mp4", os.path.join(C.outd, C.name + ".mp4")); out = opt("--out", os.path.join(C.outd, C.name + ".folha.jpg"))
cam, tele, ch = C.cam, C.tele, C.ch; kname = {0: "seta", 1: "mão", 2: "barra de texto"}


def pick():
    sel = []; R = cam.regions; auto = [r for r in R if r["src"] == "auto"]; man = [r for r in R if r["src"] == "manual"]
    r0 = auto[0] if auto else R[0]; ts = np.arange(r0["s"], r0["s"] + 1.6, 1 / FPS); mo = [cam.motion(t, C.shut) for t in ts]; tb = float(ts[int(np.argmax(mo))])
    sel += [(max(0.0, r0["s"] - 0.4), "1  antes do zoom"), (r0["s"] + 0.2, "2  zoom entrando (mola, ~1,5 s)"),
            (tb, f"3  desfoque de zoom no pico ({max(mo):.0f} px nas bordas)")]
    c0 = next((c for c in tele.clicks if c.t >= r0["s"]), tele.clicks[0])
    sel += [(c0.td - 0.3, f"4  cursor a caminho: {kname[c0.kind]}"), (c0.td + 0.07, "5  clique: quique de escala + anel"), (c0.tu + 0.25, "6  anel #00C597 abrindo")]
    ct = next((c for c in tele.clicks if c.kind == 2), None)
    if ct: sel.append((ct.tu + 0.7, "7  barra de texto sobre o campo"))
    for i in range(1, len(R)):
        if abs(R[i]["s"] - R[i - 1]["e"]) < 1e-6 and R[i]["src"] == R[i - 1]["src"] == "auto": sel.append((R[i]["s"] + 0.4, "8  desliza de um foco ao outro (sem afastar)")); break
    if man: sel.append((man[0]["s"] + 1.7, "9  zoom manual (retângulo) por cima do automático"))
    sel.append((r0["e"] + 0.45, "10  saída do zoom (~1,0 s)"))
    if ch.get("callouts"): sel.append((ch["callouts"][0]["at"] + 0.7, "11  callout"))
    if ch.get("illustrations"): sel.append((ch["illustrations"][0]["at"] + 0.9, "12  ilustração encaixada (PNG com alfa)"))
    sel = sorted(sel[:12], key=lambda s: s[0])
    return [(t, f"{i + 1}  " + lab.split('  ', 1)[1], lab.split('  ', 1)[0]) for i, (t, lab) in enumerate(sel)]


def grab(t):
    p = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{max(0, t - C.t0):.3f}", "-i", mp4, "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"],
                       capture_output=True, check=True).stdout
    return Image.open(io.BytesIO(p)).convert("RGB")


sel = pick(); TW, TH, CAP, COLS = 640, 360, 38, 3; rows = (len(sel) + COLS - 1) // COLS
sheet = Image.new("RGB", (COLS * TW + (COLS + 1) * 8, rows * (TH + CAP) + (rows + 1) * 8), (24, 24, 26)); d = ImageDraw.Draw(sheet); f = ui.font(700, 21)
frames = {}
for k, (t, lab, _) in enumerate(sel):
    im = frames[t] = grab(t); x, y = 8 + (k % COLS) * (TW + 8), 8 + (k // COLS) * (TH + CAP + 8)
    sheet.paste(im.resize((TW, TH), Image.LANCZOS), (x, y + CAP)); d.text((x + 4, y + CAP // 2), f"{t:5.2f}s", font=f, fill=(0, 197, 151), anchor="lm")
    d.text((x + 90, y + CAP // 2), lab, font=f, fill=(235, 235, 235), anchor="lm")
sheet.save(out, quality=88); print(out, sheet.size)

# recortes 1:1: o pico do desfoque, a ponta do cursor no clique (quique) e o anel
cursor_at = lambda t: C.cur[int(np.clip(t * 240, 0, len(C.T) - 2))]
def crop_tip(t, wd=420, ht=300):
    cx, cy, vw = cam.view(t); k = W / vw; px, py = cursor_at(t); ox, oy = (px - (cx - vw / 2)) * k, (py - (cy - vw * H / W / 2)) * k
    x0, y0 = int(np.clip(ox - wd / 2, 0, W - wd)), int(np.clip(oy - ht / 2, 0, H - ht)); return frames.get(t, grab(t)).crop((x0, y0, x0 + wd, y0 + ht))
labs = {s[2]: s[0] for s in sel}; det = []
tb = labs.get("3"); t5 = labs.get("5"); t6 = labs.get("6")
if tb: im = frames[tb]; det.append((im.crop((W - 640, 120, W, 420)).resize((640, 300)), f"desfoque de zoom (recorte 1:1, {tb:.2f}s)"))
if t5: det.append((crop_tip(t5).resize((630, 450)), f"clique: seta/mão encolhe (quique) {t5:.2f}s"))
if t6: det.append((crop_tip(t6).resize((630, 450)), f"anel #00C597 {t6:.2f}s"))
if det:
    hh = max(i.height for i, _ in det) + CAP; sh = Image.new("RGB", (sum(i.width for i, _ in det) + 8 * (len(det) + 1), hh + 16), (24, 24, 26)); dd = ImageDraw.Draw(sh); x = 8
    for im, lab in det: sh.paste(im, (x, 8 + CAP)); dd.text((x + 4, 8 + CAP // 2), lab, font=f, fill=(235, 235, 235), anchor="lm"); x += im.width + 8
    p2 = os.path.splitext(out)[0] + "_detalhe.jpg"; sh.save(p2, quality=90); print(p2, sh.size)
