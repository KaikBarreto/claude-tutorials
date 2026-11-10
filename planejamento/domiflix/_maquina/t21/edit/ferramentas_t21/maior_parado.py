"""T21 · maior trecho sem zoom, destaque, aviso ou ilustração em cada capítulo (regra: nenhum trecho parado mais de ~20 s).
Usa a mesma câmera do render (chapter.Chapter -> cam.regions) e as camadas do caps/capNN.chapter.json; os cortes do capítulo contam.
uso: python3 -I ferramentas_t21/maior_parado.py   (da pasta t21/edit)"""
import glob, json, os, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
from chapter import Chapter  # noqa: E402

for p in sorted(glob.glob(os.path.join(HERE, "caps", "cap*.chapter.json"))):
    ch = json.load(open(p))
    C = Chapter(p, None)
    t0, t1 = ch["trim"]["start"], ch["trim"]["end"]
    iv = [(r["s"], r["e"]) for r in C.cam.regions if r["z"] > 1.05]
    iv += [(s["at"], s["at"] + s.get("dur", 1.8)) for s in ch.get("spots", [])]
    iv += [(c["at"], c["at"] + c.get("dur", 3.0)) for c in ch.get("callouts", [])]
    iv += [(i["at"], i["at"] + i.get("dur", 3.0)) for i in ch.get("illustrations", [])]
    iv += [tuple(c) for c in ch.get("cortes", [])]   # trecho cortado não aparece
    iv = sorted(iv)
    t, pior = t0, (0.0, t0)
    for a, b in iv:
        if a > t and a - t > pior[0]:
            pior = (a - t, t)
        t = max(t, b)
    if t1 - t > pior[0]:
        pior = (t1 - t, t)
    print(f"{ch['name']}: maior trecho parado {pior[0]:5.1f} s (a partir de {pior[1]:.1f} s); {len(iv)} camadas/zooms; duração {t1 - t0:.1f} s")
