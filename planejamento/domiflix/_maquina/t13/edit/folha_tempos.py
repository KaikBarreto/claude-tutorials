#!/usr/bin/env python3
"""Folha de quadros de um MP4 em instantes escolhidos, cada quadro com o tempo no canto (revisão de remendo e de emenda).

uso: python3 -I folha_tempos.py video.mp4 saida.jpg "título" [t0:t1:passo ...] [--emendas 102.13,340.4] [--antes 2]
                                [--depois 2] [--passo 0.5] [--cols 5] [--w 384]
  t0:t1:passo   gera os instantes t0, t0+passo, ... até t1 (inclusive), em segundos do vídeo final
  --emendas     atalho para a folha de emendas: de (t - antes) a (t + depois), de passo em passo, para cada t
Exemplo (T5, remendo de 04/11): folha_tempos.py aula_final.mp4 emendas.jpg "T5 · emendas" --emendas 102.13,340.4,343.6
"""
import io
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
# instalada em tN/edit/ a fonte fica no kit da pasta de trabalho; rodando da skill, no kit de TUT_HOME
FT = next((p for p in (os.path.join(os.path.dirname(os.path.dirname(HERE)), "kit", "fonts", "Montserrat-700.ttf"),
                       os.path.join(os.environ.get("TUT_HOME", "."), "kit", "fonts", "Montserrat-700.ttf"))
           if os.path.exists(p)), "")


def opt(a, nome, padrao, tipo=float):
    return tipo(a[a.index(nome) + 1]) if nome in a else padrao


def main():
    a = sys.argv[1:]
    if len(a) < 3 or a[0] in ("-h", "--help"):
        sys.exit(__doc__)
    mp4, out, titulo = a[0], a[1], a[2]
    cols, W = opt(a, "--cols", 5, int), opt(a, "--w", 384, int)
    antes, depois, passo = opt(a, "--antes", 2.0), opt(a, "--depois", 2.0), opt(a, "--passo", 0.5)
    grupos = [g.split(":") for g in a[3:] if g.count(":") == 2 and not g.startswith("--")]
    if "--emendas" in a:
        for t in a[a.index("--emendas") + 1].split(","):
            t = float(t)
            grupos.append([t - antes, t + depois, passo])
    ts = []
    for t0, t1, p in grupos:
        t, t1, p = float(t0), float(t1), float(p)
        while t <= t1 + 1e-6:
            ts.append(round(max(t, 0.0), 2))
            t += p
    if not ts:
        sys.exit("nenhum instante: passe grupos t0:t1:passo ou --emendas")
    H = W * 9 // 16
    font = ImageFont.truetype(FT, 15) if FT else ImageFont.load_default()
    tiles = []
    for t in ts:
        r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", mp4, "-frames:v", "1", "-vf", f"scale={W}:{H}",
                            "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True)
        im = Image.open(io.BytesIO(r.stdout)).convert("RGB") if r.stdout else Image.new("RGB", (W, H), (90, 0, 0))
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, 92, 22], fill=(0, 0, 0))
        d.text((5, 3), f"{int(t // 60)}:{t % 60:05.2f}", fill=(255, 255, 255), font=font)
        tiles.append(im)
    rows = (len(tiles) + cols - 1) // cols
    sh = Image.new("RGB", (cols * (W + 4) + 4, rows * (H + 4) + 34), (30, 30, 30))
    ImageDraw.Draw(sh).text((8, 8), titulo, fill=(255, 255, 255), font=font)
    for i, im in enumerate(tiles):
        sh.paste(im, (4 + (i % cols) * (W + 4), 34 + (i // cols) * (H + 4)))
    sh.save(out, quality=85)
    print(out, len(tiles), "quadros", sh.size)


if __name__ == "__main__":
    main()
