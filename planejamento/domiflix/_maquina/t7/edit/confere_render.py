"""Conferência dos capítulos já renderizados (T7, celular): duas coisas que a auditoria da câmera não pega.
  1. zoom manual engolido: cada zoom de caps/capNN.chapter.json tem de virar uma região manual no sidecar
     out/capNN/capNN.edit.json. Zoom que começa antes de 0 s (passo no início do capítulo, `at` = tStart - 0,2) é descartado em
     silêncio pela câmera. Conserto na especificação: `"atraso": 0.35` no zoom.
  2. aviso (callout) ao lado do celular: o aviso em coluna (overlay.py: callout_coluna) fica no espaço livre do palco; com o aparelho
     ampliado demais (zoom > 2,6x) esse espaço some e o aviso passaria por cima da tela. Lista os avisos que caem em zoom assim.
uso: python3 -I confere_render.py [cap00 cap01 ...]   (sem argumentos: todos os capítulos com sidecar)
Só lê os JSON (não precisa dos MP4)."""
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ZOOM_MAX_AVISO = 2.6
caps = sys.argv[1:] or sorted(os.path.basename(p)[:5] for p in glob.glob(os.path.join(HERE, "out", "cap*", "cap*.edit.json")))

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
    for k, co in enumerate(ch.get("callouts", [])):
        a, d = co["at"], co["dur"]
        zs = [r["z"] for r in side["regions"] if r["s"] + t0 < a + d and r["e"] + t0 > a]
        zmax = max(zs) if zs else 1.0
        junto = zmax > ZOOM_MAX_AVISO
        suspeitos += int(junto)
        print(f"  aviso {k} [{a - t0:.1f}-{a - t0 + d:.1f}] '{co['text'][:44]}': zoom máx. {zmax:.2f}x " + ("-> SEM ESPAÇO AO LADO" if junto else "ok"))
print("TOTAL de suspeitos:", suspeitos)
