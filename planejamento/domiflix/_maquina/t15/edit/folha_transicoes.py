"""Folha de quadros SÓ das transições de zoom de um capítulo de celular (entrada, saída e deslizes), tirados do MP4 já renderizado.
Serve para conferir a olho o que a auditoria numérica (auditar_recorte.py) confere em contas: a tela presa ao retângulo arredondado
do aparelho, com a moldura por cima, sem canto reto. Escolhe os instantes em que o canto arredondado invade o quadro com a borda da
tela já fora dele (os de maior risco) e mais um quadro no meio de cada entrada, saída e deslize da câmera.
uso: python3 -I folha_transicoes.py caps/cap01.chapter.json [--n 24] [--cols 8] [--saida arquivo.jpg]
Sem trava: só extrai alguns quadros (ffmpeg -ss, nice 10) e monta a folha com PIL."""
import os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.dont_write_bytecode = True
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from chapter import Chapter
from camera import W, H, FPS

av = sys.argv[1:]
opt = lambda k, d=None: av[av.index(k) + 1] if k in av else d
cj = next(a for a in av if a.endswith(".json"))
N, COLS = int(opt("--n", 24)), int(opt("--cols", 8))
C = Chapter(cj); g, cam = C.geom, C.cam
mp4 = os.path.join(C.outd, C.name + ".mp4")
saida = opt("--saida", os.path.join(C.outd, C.name + ".folha_transicoes.jpg"))
risco = []
for q in range(int(C.dur * FPS)):
    t = q / FPS; cx, cy, vw = cam.view(t); k = W / vw; vx, vy = cx - vw / 2, cy - vw * H / W / 2
    Y0, Y1, r = -vy * k, (C.SH - vy) * k, g.radius * k / g.k0
    if -r - 2 < Y0 <= 0 or H <= Y1 < H + r + 2: risco.append(t)
# um quadro no meio de cada troca da câmera (entrada, deslize e saída): ~0,6 s depois do começo da região e ~0,4 s depois do fim
trocas = sorted({round(r["s"] + 0.6, 2) for r in cam.regions} | {round(r["e"] + 0.4, 2) for r in cam.regions})
pick = lambda lst, n: [lst[int(i * (len(lst) - 1) / max(1, n - 1))] for i in range(min(n, len(lst)))] if lst else []
ts = sorted(set(round(t, 2) for t in pick(risco, max(0, N - len(trocas))) + [t for t in trocas if t < C.dur]))[:max(N, len(trocas))]
cw, ch_ = 330, 360   # faixa central do quadro (onde fica o aparelho, mesmo ampliado) reduzida
tmp = tempfile.mkdtemp(prefix="trans-", dir=os.path.dirname(mp4))
fonte = ImageFont.load_default()
folha = Image.new("RGB", (COLS * (cw + 4) + 4, ((len(ts) + COLS - 1) // COLS) * (ch_ + 18) + 4), (24, 24, 27)); d = ImageDraw.Draw(folha)
for i, t in enumerate(ts):
    p = os.path.join(tmp, f"q{i:03d}.png")
    subprocess.run(["nice", "-n", "10", "ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", mp4, "-frames:v", "1", p], check=False)
    x, y = 4 + (i % COLS) * (cw + 4), 4 + (i // COLS) * (ch_ + 18)
    if os.path.exists(p):
        im = Image.open(p).convert("RGB").crop((440, 0, 1480, 1080)).resize((cw, ch_)); folha.paste(im, (x, y + 14)); os.remove(p)
    cx, cy, vw = cam.view(t); d.text((x + 2, y + 1), f"{t:.2f}s zoom {C.geom.vw0 / vw:.2f}", fill=(240, 240, 240), font=fonte)
os.rmdir(tmp)
folha.save(saida, quality=90); print(saida, folha.size, f"{len(ts)} quadros ({len(risco)} de risco no capítulo)")
