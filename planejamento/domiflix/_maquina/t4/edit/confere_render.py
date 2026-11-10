"""Conferência dos capítulos já renderizados (T4): duas coisas que a auditoria da câmera não pega.
  1. zoom manual engolido: cada zoom de caps/capNN.chapter.json tem de virar uma região manual no sidecar
     out/capNN/capNN.edit.json. Zoom que começa antes de 0 s (passo no início do capítulo, `at` = tStart - 0,2)
     é descartado em silêncio pela câmera (índice negativo no corte do vetor): o capítulo sai sem o zoom.
     Conserto na especificação: `"atraso": 0.35` no zoom.
  2. aviso (callout) por cima do aviso do app (toast verde, canto inferior direito): lista, para cada aviso da edição,
     os instantes em que o toast aparece junto (4 amostras por segundo). Conserto: `at` depois do toast ou `pos: "top"`.
uso: python3 -I confere_render.py [cap00 cap01 ...]   (sem argumentos: todos os capítulos com sidecar)
Precisa dos MP4 dos capítulos (out/capNN/capNN.mp4), então rode antes da limpeza."""
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
caps = sys.argv[1:] or sorted(os.path.basename(p)[:5] for p in glob.glob(os.path.join(HERE, "out", "cap*", "cap*.edit.json")))


def toast_verde(png):
    im = np.array(Image.open(png).convert("RGB")).astype(int)
    sub = im[im.shape[0] // 2:, im.shape[1] // 4:]  # metade de baixo, três quartos da direita
    m = (sub[:, :, 0] < 22) & (sub[:, :, 1] > 135) & (sub[:, :, 1] < 165) & (sub[:, :, 2] > 90) & (sub[:, :, 2] < 122)
    return int(m.sum()) >= 40  # o verde do toast é (4, 150, 105); a 480 px de largura o bloco tem ~130 a 500 px


suspeitos = 0
for c in caps:
    ch = json.load(open(os.path.join(HERE, "caps", f"{c}.chapter.json"), encoding="utf-8"))
    side = json.load(open(os.path.join(HERE, "out", c, f"{c}.edit.json")))
    t0 = side.get("start", 0.0)
    man = [r for r in side["regions"] if r["src"] == "manual"]
    sem = [z["at"] for z in ch.get("zooms", []) if not any(abs(r["s"] - z["at"]) < 1.0 or r["s"] <= z["at"] <= r["e"] for r in man)]
    neg = [r["s"] for r in side["regions"] if r["s"] < 0]
    print(f"{c}: zooms manuais {len(ch.get('zooms', []))}, regiões manuais {len(man)}, sem região {sem}, início < 0 {neg}")
    suspeitos += len(sem) + len(neg)
    mp4 = os.path.join(HERE, "out", c, f"{c}.mp4")
    for k, co in enumerate(ch.get("callouts", [])):
        a, d = max(0.0, co["at"] - t0), co["dur"]
        with tempfile.TemporaryDirectory() as td:
            subprocess.run(["nice", "-n", "10", "ffmpeg", "-y", "-v", "error", "-ss", f"{a:.3f}", "-t", f"{d:.3f}", "-i", mp4,
                            "-vf", f"fps={FPS},scale=480:-2", os.path.join(td, "f%04d.png")], check=True)
            hits = [round(a + i / FPS, 2) for i, f in enumerate(sorted(glob.glob(td + "/f*.png"))) if toast_verde(f)]
        pos = co.get("pos", "bottom")
        junto = bool(hits) and pos != "top"
        suspeitos += int(junto)
        print(f"  aviso {k} [{a:.1f}-{a + d:.1f}] pos {pos} '{co['text'][:44]}': "
              + (f"TOAST junto de {hits[0]} a {hits[-1]} s" if junto else ("toast junto, mas o aviso está no alto" if hits else "ok")))
print("TOTAL de suspeitos:", suspeitos)
