"""T21 · folha das vinhetas de capítulo da aula final: um quadro de cada vinheta (título já pousado, 1,8 s depois do início), em 4x3,
com o nome do item e o instante no vídeo final. Para conferir área e título de cada vinheta contra o roteiro.
uso: python3 -I ferramentas_t21/folha_vinhetas.py <out/T21>   -> <out/T21>/folha_vinhetas.jpg"""
import json
import os
import subprocess
import sys

OUT = os.path.abspath(sys.argv[1])
MP4 = os.path.join(OUT, "aula_final.mp4")
intro = os.path.join(OUT, "proj", "build", "intro_v.mp4")
T_IN = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", intro],
                            capture_output=True, text=True, check=True).stdout.strip())
caps = json.load(open(os.path.join(OUT, "capitulos.json")))["chapters"]
tmp = os.path.join(OUT, "_vinhetas")
os.makedirs(tmp, exist_ok=True)
fonte = "/home/claude/domiflix/kit/fonts/Montserrat-700.ttf"
quadros = []
for c in caps:
    if not c["name"].startswith("vinheta-"):
        continue
    t = T_IN + c["start"] + 1.8
    p = os.path.join(tmp, f"{c['name']}.jpg")
    rot = f"{c['name']}  {t:.1f} s"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", MP4, "-frames:v", "1", "-vf",
                    f"scale=640:360,drawtext=fontfile={fonte}:text='{rot}':x=8:y=8:fontsize=18:fontcolor=white:box=1:boxcolor=black@0.6",
                    "-q:v", "3", p], check=True)
    quadros.append(p)
lista = os.path.join(tmp, "lista.txt")
with open(lista, "w") as f:
    for p in quadros:
        f.write(f"file '{p}'\n")
saida = os.path.join(OUT, "folha_vinhetas.jpg")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lista, "-vf", "tile=4x3:padding=4:color=white",
                "-frames:v", "1", "-q:v", "3", saida], check=True)
for p in quadros + [lista]:
    os.remove(p)
os.rmdir(tmp)
print(saida, len(quadros), "vinhetas")
