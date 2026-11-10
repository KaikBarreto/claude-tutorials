"""Auditoria da câmera (Kaik 30/10 17:06-17:08: zoom foi para o canto; "os zooms num geral em algumas áreas estão um pouco perdidos").
Para cada evento com alvo conhecido (clique, tecla digitada num campo), confere se o retângulo do elemento estava
dentro do quadro naquele instante e quão centrado. Não renderiza nada: só simula a câmera.
uso: python3 -I auditar_camera.py caps/cap08.chapter.json [...]   (sem argumentos: todos os capítulos de caps/)
Saída: por capítulo, eventos conferidos, eventos com alvo fora do quadro (visível < 90%) e os piores instantes."""
import glob, json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chapter import Chapter
from camera import W, H

MOD = {"Shift", "Control", "Alt", "Meta", "Tab", "Shift+Tab", "Escape", "CapsLock"}


def eventos(tele):
    """(t, rect, tipo, texto do alvo) dos eventos com alvo: cliques e teclas que escrevem/confirmam num elemento"""
    ev = []
    for s in tele.raw["samples"]:
        r = s.get("rect")
        if not r or r.get("w", 0) <= 0 or r.get("h", 0) <= 0: continue
        if s["type"] == "click" or (s["type"] == "key" and s.get("key") not in MOD):
            ev.append((s["t"], r, s["type"], (s.get("target") or {}).get("text", "")[:30]))
    return ev


def visivel(view, r, vw0):
    cx, cy, vw = view; vh = vw * H / W
    x0, y0, x1, y1 = cx - vw / 2, cy - vh / 2, cx + vw / 2, cy + vh / 2
    ix = max(0.0, min(x1, r["x"] + r["w"]) - max(x0, r["x"])); iy = max(0.0, min(y1, r["y"] + r["h"]) - max(y0, r["y"]))
    frac = (ix * iy) / (r["w"] * r["h"])
    dx = (r["x"] + r["w"] / 2 - cx) / (vw / 2); dy = (r["y"] + r["h"] / 2 - cy) / (vh / 2)
    return frac, max(abs(dx), abs(dy)), vw0 / vw


def auditar(cj, quiet=False):
    ch = Chapter(cj); cam, tele = ch.cam, ch.tele; vw0 = ch.geom.vw0; ruins = []; n = 0
    for t, r, ty, tx in eventos(tele):
        if not (ch.t0 <= t <= ch.t1): continue
        n += 1; frac, desc, z = visivel(cam.view(t), r, vw0)
        if z > 1.05 and (frac < 0.9 or desc > 0.85):
            ruins.append((t, frac, desc, z, ty, tx))
    zero = sum(1 for s in tele.raw["samples"] if s.get("x") == 0 and s.get("y") == 0)
    regs = [r for r in cam.regions if r["z"] > 1]
    probs = getattr(cam, "problemas", [])
    if not quiet:
        print(f"{ch.name}: {n} eventos | {len(ruins)} com alvo fora/na borda do quadro | {len(regs)} zooms | amostras (0,0): {zero}"
              f" | checagem da câmera: {len(probs)} problema(s)")
        for p_ in probs[:8]: print("   CHECAGEM:", p_)
        for t, frac, desc, z, ty, tx in ruins[:12]:
            print(f"   t={t:6.2f} (saída {t - ch.t0:6.2f}) zoom {z:.2f} visível {frac:4.0%} descentrado {desc:.2f} {ty} '{tx}'")
        for r in regs:
            if r["ax"] < 60 or r["ay"] < 60: print(f"   ZOOM COM ÂNCORA NO CANTO: {r}")
    return ch.name, n, ruins + [("chk",) for _ in probs]


if __name__ == "__main__":
    files = sys.argv[1:] or sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "caps", "cap*.chapter.json")))
    tot = 0
    for f in files:
        _, n, ruins = auditar(f); tot += len(ruins)
    print(f"TOTAL de instantes com alvo fora do quadro: {tot}")
