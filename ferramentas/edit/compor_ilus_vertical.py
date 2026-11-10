#!/usr/bin/env python3
"""Ilustrações no capítulo VERTICAL da tela real do celular, depois do render (T0 v2): o render_chapter_vertical.py não desenha as
"illustrations" da gravação do celular (celular_vertical.py as desliga), então cada ilustração de quadro cheio (1080x1920, já com palco e
painel, ex.: cena do render_cenas_vertical.cjs) cobre o capítulo renderizado na janela [at, at + dur). O áudio fica intacto; o vídeo é
recodificado uma vez (CRF 17, bt709 faixa TV como o render).
uso: python3 -I compor_ilus_vertical.py caps/capNN.9x16.chapter.json [...]   (ou só NN: caps/capNN.9x16.chapter.json)
Rode logo depois do render do capítulo, sob a trava (reexecuta sozinho sob flock .heavy.lock + nice). O render sem ilustração fica ao lado
(.sem_ilus_<nome>.mp4, hardlink) e o sidecar (<nome>.edit.json) guarda "ilustracoes_compostas": rodar de novo parte do render limpo, e um
render novo (sidecar reescrito) volta a valer como base."""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import ensure_heavy  # noqa: E402

args = sys.argv[1:]
if not args or "--help" in args:
    sys.exit(__doc__)
ensure_heavy()
CHEIO = [0, 0, 1080, 1920]


def compor(cj):
    ch = json.load(open(cj))
    nome = ch.get("name") or os.path.basename(cj).split(".")[0]
    il = ch.get("illustrations", [])
    if not il:
        print(f"{nome}: sem ilustrações")
        return
    for i in il:
        if i.get("box", CHEIO) != CHEIO:
            sys.exit(f"{nome}: ilustração em {i['box']}: aqui só entra quadro cheio {CHEIO} (cena vertical com palco e painel)")
    outd = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(cj)), ch.get("output", {}).get("dir", "out")))
    sp = os.path.join(outd, nome + ".edit.json")
    if not os.path.exists(sp):
        sys.exit(f"{nome}: falta o render ({sp}); rode o render_chapter_vertical.py antes")
    side = json.load(open(sp))
    v = side.get("video") or os.path.join(outd, nome + ".mp4")
    base = os.path.join(os.path.dirname(v), f".sem_ilus_{os.path.basename(v)}")
    if not (side.get("ilustracoes_compostas") and os.path.exists(base)):  # render novo: ele é a base
        if os.path.exists(base):
            os.remove(base)
        os.link(v, base)
    t0 = float(ch.get("trim", {}).get("start", 0.0))  # tempos do capítulo -> relógio do vídeo renderizado
    rp = lambda p: p if os.path.isabs(p) else os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(cj)), p))  # noqa: E731
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", base]
    f, ult = "", "0:v"
    for k, i in enumerate(il, 1):
        a = round(float(i["at"]) - t0, 3)
        cmd += ["-itsoffset", str(a), "-i", rp(i["src"])]
        f += f"[{ult}][{k}:v]overlay=0:0:enable='between(t,{a},{a + float(i['dur'])})':eof_action=pass[v{k}];"
        ult = f"v{k}"
    tmp = os.path.join(os.path.dirname(v), f".novo_{os.path.basename(v)}")
    cmd += ["-filter_complex", f.rstrip(";"), "-map", f"[{ult}]", "-map", "0:a?", "-c:v", "libx264", "-preset", "veryfast", "-crf", "17",
            "-g", "60", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
            "-c:a", "copy", "-movflags", "+faststart", "-f", "mp4", tmp]
    subprocess.run(cmd, check=True)
    os.replace(tmp, v)
    side["ilustracoes_compostas"] = len(il)
    json.dump(side, open(sp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"ok {v}: {len(il)} ilustração(ões) de quadro cheio")


for a in args:
    m = re.fullmatch(r"(\d+)([a-z]?)", a)
    compor(os.path.join(HERE, "caps", f"cap{int(m[1]):02d}{m[2]}.9x16.chapter.json") if m else a)
