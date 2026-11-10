#!/usr/bin/env python3
"""Maior trecho de cada capítulo SEM zoom (z >= 1,2), destaque ou ilustração (regra de 04/11, T12: nada parado por mais de ~20 s).
Lê as regiões de câmera do render (<output.dir>/<nome>.edit.json) e o caps/capNN.chapter.json. Rode depois do render dos capítulos.
uso: python3 -I lacunas.py [NN ...] [--limite 20]   (sem NN: todos os caps/capNN.chapter.json com render)"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
argv = sys.argv[1:]
LIMITE = float(argv[argv.index("--limite") + 1]) if "--limite" in argv else 20.0
args = [a for i, a in enumerate(argv) if a != "--limite" and (i == 0 or argv[i - 1] != "--limite")]
todos = sorted(m.group(1) for p in glob.glob(os.path.join(HERE, "caps", "cap*.chapter.json"))
               if (m := re.fullmatch(r"cap(\d\d[a-z]?)\.chapter\.json", os.path.basename(p))))
caps = [f"{int(m[1]):02d}{m[2]}" for a in args if (m := re.fullmatch(r"(\d+)([a-z]?)", a))] or todos
acima = 0
for nn in caps:
    cj = os.path.join(HERE, "caps", f"cap{nn}.chapter.json")
    ch = json.load(open(cj))
    outd = os.path.normpath(os.path.join(os.path.dirname(cj), ch.get("output", {}).get("dir", os.path.join(HERE, "out", f"cap{nn}"))))
    p = os.path.join(outd, f"{ch.get('name', f'cap{nn}')}.edit.json")
    if not os.path.exists(p):
        print(f"cap{nn}: sem render")
        continue
    e = json.load(open(p))
    iv = [(r["s"], r["e"]) for r in e.get("regions", []) if r.get("z", 1) >= 1.2]
    iv += [(s["at"], s["at"] + s.get("dur", 2)) for s in ch.get("spots", [])]
    iv += [(s["at"], s["at"] + s.get("dur", 2)) for s in ch.get("illustrations", [])]
    iv.sort()
    t, pior, onde = 0.0, 0.0, 0.0
    for a, b in iv:
        if a - t > pior:
            pior, onde = a - t, t
        t = max(t, b)
    if e["dur"] - t > pior:
        pior, onde = e["dur"] - t, t
    acima += pior > LIMITE
    print(f"cap{nn}: maior trecho sem zoom/destaque/ilustração {pior:.1f} s (a partir de {onde:.1f} s) de {e['dur']:.1f} s"
          + (f"   <-- ACIMA DE {LIMITE:g} s" if pior > LIMITE else ""))
sys.exit(1 if acima else 0)
