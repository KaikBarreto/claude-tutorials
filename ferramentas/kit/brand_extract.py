"""Prepara os arquivos de logo de uma marca para a vinheta (web/intro.html) e grava em <pasta da marca>/assets.
As cores vêm do marca.json dessa pasta (senão, da marca em uso: kit/ui.py).

uso: python3 kit/brand_extract.py <logo horizontal .png/.webp> <pasta da marca> [--nome-claro]
  Recorta as bordas transparentes e separa símbolo e nome pelo primeiro vão vertical largo (símbolo à esquerda):
  assets/logo.png, simbolo.png e wordmark.png (--nome-claro: o nome em cor única no "claro" da marca, para fundo
  escuro). Sem vão (só símbolo ou só nome) grava só o logo.png. Depois aponte o marca.json:
  "logo": {"arquivo": "assets/logo.png", "simbolo": "assets/simbolo.png", "wordmark": "assets/wordmark.png"}
Dominex (exemplo do estilo "dominex-capacete"), a partir dos arquivos enviados (webp com alfa):
  python3 kit/brand_extract.py --dominex <pasta com 1.webp 3.webp 5.webp> <pasta da marca>
  -> assets/helmet_{green,light,dark}.png, piece_*.png, pieces.json, wordmark_*.png, logo_h_*.png, helmet_3d.jpg"""
import json, os, sys
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ui  # noqa: E402

args = [a for a in sys.argv[1:] if not a.startswith("--")]
if len(args) != 2:
    sys.exit(__doc__)
SRC, MARCA_DIR = args
OUT = os.path.join(MARCA_DIR, "assets")
os.makedirs(OUT, exist_ok=True)
_cores = dict(ui.MARCA["cores"])  # só as cores do marca.json da pasta (os logos dele ainda vão ser gerados aqui)
if os.path.isfile(os.path.join(MARCA_DIR, "marca.json")):
    _cores.update(json.load(open(os.path.join(MARCA_DIR, "marca.json"), encoding="utf-8")).get("cores", {}))
GREEN, LIGHT, DARK = (ui.rgb(_cores[k]) for k in ("acento", "claro", "escuro"))


def recolor(a, rgb):
    out = np.zeros(a.shape[:2] + (4,), np.uint8); out[..., :3] = rgb; out[..., 3] = a
    return Image.fromarray(out, "RGBA")


def trim(a, pad=4):
    ys, xs = np.nonzero(a > 0)
    y0, y1, x0, x1 = max(0, ys.min() - pad), min(a.shape[0], ys.max() + pad + 1), max(0, xs.min() - pad), min(a.shape[1], xs.max() + pad + 1)
    return a[y0:y1, x0:x1], (x0, y0, x1, y1)


if "--dominex" not in sys.argv:  # ------------------------------------------------ qualquer marca
    im = np.array(Image.open(SRC).convert("RGBA"))
    _, (x0, y0, x1, y1) = trim(im[..., 3], 2); im = im[y0:y1, x0:x1]
    Image.fromarray(im, "RGBA").save(os.path.join(OUT, "logo.png"))
    a = im[..., 3]; cols = np.nonzero((a > 40).any(0))[0]; gaps = np.nonzero(np.diff(cols) > max(6, 0.12 * a.shape[0]))[0]
    if not len(gaps):
        print("logo.png", a.shape[::-1], "(sem vão entre símbolo e nome: use só \"arquivo\")"); sys.exit(0)
    split = int((cols[gaps[0]] + cols[gaps[0] + 1]) / 2)
    for nome, part in (("simbolo", im[:, :split]), ("wordmark", im[:, split:])):
        _, (x0, y0, x1, y1) = trim(part[..., 3], 2); part = part[y0:y1, x0:x1]
        img = recolor(part[..., 3], LIGHT) if nome == "wordmark" and "--nome-claro" in sys.argv else Image.fromarray(part, "RGBA")
        img.save(os.path.join(OUT, nome + ".png")); print(nome + ".png", img.size)
    print("logo.png", a.shape[::-1], "| símbolo e nome separados na coluna", split)
    sys.exit(0)

# --------------------------------------------------------------------------------- Dominex: capacete em 3 peças
# capacete (verde, 5.webp)
helm = np.array(Image.open(os.path.join(SRC, "5.webp")).convert("RGBA"))[..., 3]
helm, box = trim(helm, 0)
H, W = helm.shape
recolor(helm, GREEN).save(os.path.join(OUT, "helmet_green.png"))
recolor(helm, LIGHT).save(os.path.join(OUT, "helmet_light.png"))
recolor(helm, DARK).save(os.path.join(OUT, "helmet_dark.png"))
from scipy import ndimage  # noqa: E402
lab, n = ndimage.label(helm > 40)
sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
pieces = []
for i in np.argsort(-sizes):
    if sizes[i] < 500: continue
    m = lab == (i + 1)
    # inclui a borda antialiasada vizinha
    m = ndimage.binary_dilation(m, iterations=2) & (helm > 0)
    a = np.where(m, helm, 0).astype(np.uint8)
    ys, xs = np.nonzero(a)
    k = len(pieces)
    recolor(a, GREEN).save(os.path.join(OUT, f"piece_{k}.png"))
    pieces.append({"i": k, "area": int(sizes[i]), "bbox": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
                   "cx": float(xs.mean()), "cy": float(ys.mean())})
json.dump({"W": W, "H": H, "pieces": pieces}, open(os.path.join(OUT, "pieces.json"), "w"), indent=1)
print("helmet", W, H, "pieces", len(pieces)); [print(" ", p) for p in pieces]

# logotipo horizontal (3.webp): capacete + DOMINEX
logo = np.array(Image.open(os.path.join(SRC, "3.webp")).convert("RGBA"))
a = logo[..., 3]
cols = np.nonzero((a > 40).any(0))[0]
gaps = np.nonzero(np.diff(cols) > 30)[0]
split = int((cols[gaps[0]] + cols[gaps[0] + 1]) / 2)
word, wbox = trim(a[:, split:], 2)
recolor(word, LIGHT).save(os.path.join(OUT, "wordmark_light.png"))
recolor(word, DARK).save(os.path.join(OUT, "wordmark_dark.png"))
la, lbox = trim(a, 2)
rgb = np.zeros(la.shape + (3,), np.uint8); rgb[:] = DARK; rgb[:, : split - lbox[0]] = GREEN
Image.fromarray(np.dstack([rgb, la]), "RGBA").save(os.path.join(OUT, "logo_h_dark.png"))
rgb[:] = LIGHT; rgb[:, : split - lbox[0]] = GREEN
Image.fromarray(np.dstack([rgb, la]), "RGBA").save(os.path.join(OUT, "logo_h_light.png"))
print("wordmark", word.shape[::-1], "split at", split, "logo", la.shape[::-1])
# capacete 3D (1.webp) para capas
if os.path.isfile(os.path.join(SRC, "1.webp")):
    Image.open(os.path.join(SRC, "1.webp")).convert("RGB").save(os.path.join(OUT, "helmet_3d.jpg"), quality=92)
# as peças em meia resolução da vinheta (piece_*_h.png, helmet_green_h.png, helmet_glow.png) ficam em web/assets
