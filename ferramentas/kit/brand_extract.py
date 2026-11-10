"""Prepara os arquivos de logo de uma marca para a vinheta (web/intro.html) e grava em <pasta da marca>/assets.
As cores vêm do marca.json dessa pasta (senão, da marca em uso: kit/ui.py).

uso: python3 kit/brand_extract.py <logo horizontal .png/.webp> <pasta da marca> [--nome-claro]
  Recorta as bordas transparentes e separa símbolo e nome pelo primeiro vão vertical largo (símbolo à esquerda):
  assets/logo.png, simbolo.png e wordmark.png (--nome-claro: o nome em cor única no "claro" da marca, para fundo
  escuro). Sem vão (só símbolo ou só nome) grava só o logo.png. Depois aponte o marca.json:
  "logo": {"arquivo": "assets/logo.png", "simbolo": "assets/simbolo.png", "wordmark": "assets/wordmark.png"}
Símbolo feito de peças separadas (estilo "ecosistema-reciclagem": as peças se encaixam girando), cores originais:
  python3 kit/brand_extract.py --pecas <logo horizontal .png> <pasta da marca>
  Nada é redesenhado nem recolorido: cada pixel do PNG vai para uma peça (a borda suave fica com a peça mais perto).
  -> assets/simbolo.png, peca_<k>.png (no quadro do símbolo, na ordem do encaixe: horário a partir do alto),
     simbolo_brilho.png (halo no acento), wordmark.png e pecas.json (centro de giro, peças e o lugar do símbolo e do
     nome no logo). marca.json: "logo": {"pecas": "assets/pecas.json", "simbolo": ..., "wordmark": ...}
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


if "--pecas" in sys.argv:  # ------------------------------------------------ símbolo em peças separadas + nome
    from scipy import ndimage  # noqa: E402
    im = np.array(Image.open(SRC).convert("RGBA")); a = im[..., 3]
    # o miolo (alfa > 40) define as formas; a borda suave (alfa > 0) vai para a forma mais perto (até 3 px); o pó
    # quase transparente solto pelo PNG (alfa 1 ou 2, longe de tudo) fica de fora
    lab, n = ndimage.label(a > 40)
    dist, (iy, ix) = ndimage.distance_transform_edt(lab == 0, return_indices=True)
    perto = np.where((a > 0) & (dist <= 3), lab[iy, ix], 0)
    _, (X0, Y0, X1, Y1) = trim(np.where(perto > 0, a, 0), 2)  # o logo inteiro, recortado
    im, perto = im[Y0:Y1, X0:X1], perto[Y0:Y1, X0:X1]; a = im[..., 3]
    cols = np.nonzero((perto > 0).any(0))[0]; gaps = np.nonzero(np.diff(cols) > max(6, 0.12 * a.shape[0]))[0]
    if not len(gaps):
        sys.exit("--pecas: não achei o vão entre o símbolo (à esquerda) e o nome")
    split = int((cols[gaps[0]] + cols[gaps[0] + 1]) / 2)
    ids = [k for k in np.unique(perto[:, :split]) if k]
    areas = {k: int(((perto == k) & (a > 40)).sum()) for k in ids}
    ids = [k for k in ids if areas[k] >= 0.05 * max(areas.values())]  # peças de verdade (sem cisco)
    if len(ids) < 2:
        sys.exit(f"--pecas: o símbolo tem {len(ids)} forma(s) separada(s); para um símbolo inteiro use o modo sem --pecas")
    so = np.where(np.isin(perto, ids), a, 0); so[:, split:] = 0
    _, (sx0, sy0, sx1, sy1) = trim(so, 2)
    nome = np.where((perto > 0) & ~np.isin(perto, ids), a, 0); nome[:, :split] = 0
    _, (wx0, wy0, wx1, wy1) = trim(nome, 2)
    def canvas(m, box):  # RGBA do PNG só onde a máscara vale (fora dela, transparente e sem cor)
        r = np.where(m[..., None], im, 0).astype(np.uint8)
        return r[box[1]:box[3], box[0]:box[2]]
    sbox, wbox = (sx0, sy0, sx1, sy1), (wx0, wy0, wx1, wy1)
    SW, SH = sx1 - sx0, sy1 - sy0
    # peças: centro de giro = média dos centros das peças; ordem do encaixe = sentido horário a partir do alto
    info = []
    for k in ids:
        ys, xs = np.nonzero((perto == k) & (a > 40))
        info.append({"k": k, "area": areas[k], "cx": float(xs.mean() - sx0), "cy": float(ys.mean() - sy0)})
    CX, CY = float(np.mean([p["cx"] for p in info])), float(np.mean([p["cy"] for p in info]))
    ang = lambda p: (np.degrees(np.arctan2(p["cy"] - CY, p["cx"] - CX)) + 90) % 360  # noqa: E731  (0 = alto, horário)
    info.sort(key=ang)
    pecas = []
    for i, p in enumerate(info):
        m = perto == p["k"]; img = canvas(m, sbox)
        ys, xs = np.nonzero(img[..., 3])
        Image.fromarray(img, "RGBA").save(os.path.join(OUT, f"peca_{i}.png"))
        pecas.append({"arquivo": f"peca_{i}.png", "area": p["area"], "bbox": [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1],
                      "cx": round(p["cx"], 2), "cy": round(p["cy"], 2), "angulo": round(float(ang(p)), 1)})
    Image.fromarray(canvas(np.isin(perto, ids), sbox), "RGBA").save(os.path.join(OUT, "simbolo.png"))
    Image.fromarray(canvas((perto > 0) & ~np.isin(perto, ids), wbox), "RGBA").save(os.path.join(OUT, "wordmark.png"))
    # halo no acento (brilho do encaixe): o contorno do símbolo desfocado, com folga em volta
    from PIL import ImageFilter  # noqa: E402
    sig = 0.045 * SH; pad = int(np.ceil(4 * sig))
    alfa = Image.new("L", (SW + 2 * pad, SH + 2 * pad), 0)
    alfa.paste(Image.fromarray(np.where(np.isin(perto, ids), a, 0)[sy0:sy1, sx0:sx1].astype(np.uint8)), (pad, pad))
    alfa = np.asarray(alfa.filter(ImageFilter.GaussianBlur(sig)), np.float32)
    recolor(np.clip(alfa / max(1.0, alfa.max()) * 255, 0, 255).astype(np.uint8), GREEN).save(os.path.join(OUT, "simbolo_brilho.png"))
    geo = {"_leia": "gerado por kit/brand_extract.py --pecas (não editar à mão)", "fonte": os.path.basename(SRC),
           "logo": {"W": int(a.shape[1]), "H": int(a.shape[0]), "simbolo": [int(v) for v in sbox], "wordmark": [int(v) for v in wbox]},
           "simbolo": {"arquivo": "simbolo.png", "W": int(SW), "H": int(SH), "centro": [round(CX, 2), round(CY, 2)]},
           "pecas": pecas, "brilho": {"arquivo": "simbolo_brilho.png", "pad": pad},
           "wordmark": {"arquivo": "wordmark.png", "W": int(wx1 - wx0), "H": int(wy1 - wy0)}}
    json.dump(geo, open(os.path.join(OUT, "pecas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # prova: as peças empilhadas no lugar refazem o símbolo do PNG pixel a pixel (o pó de alfa 1-2 fica de fora)
    soma = np.zeros((SH, SW, 4), np.float32)
    for p in pecas:
        soma += np.asarray(Image.open(os.path.join(OUT, p["arquivo"])), np.float32)
    orig = im[sy0:sy1, sx0:sx1].astype(np.float32); orig[..., 3] = np.where(np.isin(perto, ids), a, 0)[sy0:sy1, sx0:sx1]
    dif = np.abs(soma[..., 3] - orig[..., 3]).max(), np.abs((soma[..., :3] - orig[..., :3]) * (orig[..., 3:] > 0)).max()
    print(f"símbolo {SW}x{SH}, centro de giro ({CX:.1f}, {CY:.1f}); {len(pecas)} peças (horário a partir do alto):")
    [print("  ", p) for p in pecas]
    print(f"nome {wx1 - wx0}x{wy1 - wy0}; logo {a.shape[1]}x{a.shape[0]}; brilho com folga {pad} px")
    print(f"peças somadas = símbolo do PNG: dif. máx. alfa {dif[0]:.0f}, cor {dif[1]:.0f}")
    sys.exit(0)

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
