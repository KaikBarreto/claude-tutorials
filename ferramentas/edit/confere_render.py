"""Conferência dos capítulos já renderizados: o que a auditoria da câmera não pega (T4 no computador, T7 no celular).
  1. zoom manual engolido: cada zoom de caps/capNN.chapter.json tem de virar uma região manual no sidecar (<output.dir>/<nome>.edit.json).
     Zoom que começava antes de 0 s (passo no início do capítulo) era descartado em silêncio (corrigido no camera.py em 31/10, `s = max(0, s)`);
     a conferência segue valendo para qualquer zoom que a câmera deixe de fora.
  2. avisos (callouts):
     - celular (stage.phone): o aviso em coluna (overlay.py: callout_coluna) fica no espaço livre do palco; com o aparelho ampliado demais
       (zoom > 2,6x) esse espaço some e o aviso passaria por cima da tela. Lista os avisos que caem em zoom assim (só lê os JSON).
     - computador, com --toast R,G,B: o aviso da edição por cima do aviso do app (toast no canto inferior direito). Tira 4 quadros por
       segundo do MP4 renderizado na janela de cada aviso e procura a cor do toast (no app Dominex: --toast 4,150,105, o verde do
       "salvo com sucesso"). Conserto: `at` depois do toast ou "pos": "top". Precisa dos MP4 (rode antes da limpeza).
uso: python3 -I confere_render.py [cap00 cap01 ...] [--toast R,G,B]   (sem capítulos: todos com sidecar). Sai com 1 se houver suspeito."""
import glob
import json
import os
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
FPS = 4
ZOOM_MAX_AVISO = 2.6
argv = sys.argv[1:]
TOAST = tuple(int(v) for v in argv[argv.index("--toast") + 1].split(",")) if "--toast" in argv else None
args = [a for i, a in enumerate(argv) if a != "--toast" and (i == 0 or argv[i - 1] != "--toast")]


def sidecar(c):
    cj = os.path.join(HERE, "caps", f"{c}.chapter.json")
    ch = json.load(open(cj, encoding="utf-8"))
    outd = os.path.normpath(os.path.join(os.path.dirname(cj), ch.get("output", {}).get("dir", os.path.join(HERE, "out", c))))
    return ch, outd, os.path.join(outd, f"{ch.get('name', c)}.edit.json")


def toast(png, cor, tol=16):
    """a cor do toast em >= 40 px da metade de baixo e dos três quartos da direita (a 480 px de largura o toast tem ~130 a 500 px)"""
    im = np.array(Image.open(png).convert("RGB")).astype(int)
    sub = im[im.shape[0] // 2:, im.shape[1] // 4:]
    m = np.all(np.abs(sub - np.array(cor)) <= tol, axis=2)
    return int(m.sum()) >= 40


caps = args or sorted(os.path.basename(p)[:-len(".chapter.json")] for p in glob.glob(os.path.join(HERE, "caps", "cap*.chapter.json"))
                      if ".9x16." not in p and os.path.exists(sidecar(os.path.basename(p)[:-len(".chapter.json")])[2]))
suspeitos = 0
for c in caps:
    ch, outd, sp = sidecar(c)
    side = json.load(open(sp))
    t0 = side.get("start", 0.0)
    celular = bool(ch.get("stage", {}).get("phone"))
    man = [r for r in side["regions"] if r["src"] == "manual"]
    zooms = [z for z in ch.get("zooms", []) if z.get("scale", 2) != 1.0]  # repouso (scale 1) não vira região manual de zoom
    sem = [z["at"] for z in zooms if not any(abs(r["s"] - z["at"]) < 1.0 or r["s"] <= z["at"] <= r["e"] for r in man)]
    neg = [r["s"] for r in side["regions"] if r["s"] < 0]
    print(f"{c}{' (celular)' if celular else ''}: zooms manuais {len(zooms)}, regiões manuais {len(man)}, sem região {sem}, início < 0 {neg}")
    suspeitos += len(sem) + len(neg)
    mp4 = side.get("video") or os.path.join(outd, f"{ch.get('name', c)}.mp4")
    for k, co in enumerate(ch.get("callouts", [])):
        a, d = co["at"], co.get("dur", 3.0)
        txt = co["text"][:44]
        if celular:
            zs = [r["z"] for r in side["regions"] if r["s"] + t0 < a + d and r["e"] + t0 > a]
            zmax = max(zs) if zs else 1.0
            junto = zmax > ZOOM_MAX_AVISO
            suspeitos += int(junto)
            print(f"  aviso {k} [{a - t0:.1f}-{a - t0 + d:.1f}] '{txt}': zoom máx. {zmax:.2f}x " + ("-> SEM ESPAÇO AO LADO" if junto else "ok"))
        elif TOAST:
            a = max(0.0, a - t0)
            with tempfile.TemporaryDirectory() as td:
                subprocess.run(["nice", "-n", "10", "ffmpeg", "-y", "-v", "error", "-ss", f"{a:.3f}", "-t", f"{d:.3f}", "-i", mp4,
                                "-vf", f"fps={FPS},scale=480:-2", os.path.join(td, "f%04d.png")], check=True)
                hits = [round(a + i / FPS, 2) for i, f in enumerate(sorted(glob.glob(td + "/f*.png"))) if toast(f, TOAST)]
            pos = co.get("pos", "bottom")
            junto = bool(hits) and pos != "top"
            suspeitos += int(junto)
            print(f"  aviso {k} [{a:.1f}-{a + d:.1f}] pos {pos} '{txt}': "
                  + (f"TOAST junto de {hits[0]} a {hits[-1]} s" if junto else ("toast junto, mas o aviso está no alto" if hits else "ok")))
if not TOAST and any(not bool(sidecar(c)[0].get("stage", {}).get("phone")) and sidecar(c)[0].get("callouts") for c in caps):
    print("(avisos do computador sem conferir o toast do app: use --toast R,G,B com a cor do aviso do app)")
print("TOTAL de suspeitos:", suspeitos)
sys.exit(1 if suspeitos else 0)
