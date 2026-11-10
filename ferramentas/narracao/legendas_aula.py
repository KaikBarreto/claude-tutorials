"""Legendas da aula inteira (.srt e .vtt) no relógio do vídeo final:
vinheta da aula (T_IN) + capítulos e vinhetas de capítulo na ordem de out/T3/capitulos.json, descontando os cortes.
O título falado de cada vinheta de capítulo também vira legenda.
T15: capítulo gravado em dois trechos com a MESMA voz (cap09 no computador, cap09b no celular): o `audio_offset` do JSON do capítulo
(../edit/caps/<nome>.chapter.json; -voz_de) diz de que segundo da voz de origem (cap09.json) o trecho parte; a voz de origem vem dos
2 dígitos depois de "cap" no nome. Sem JSON de capítulo, offset 0 (igual à skill).
uso: python3 -I legendas_aula.py <capitulos.json> <intro_v.mp4> <saida_sem_extensao> [--linha N]
  --linha N: caracteres por linha (padrão 42, o do 16:9; vertical 9:16: --linha 32, docs/05-edicao.md). O relógio é o mesmo; só a quebra em legendas muda."""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import legendas as L  # noqa: E402

argv = sys.argv[1:]
if "--linha" in argv:  # linhas mais curtas para o player do celular (a quebra de bloco e de linha usa L.MAXL)
    i = argv.index("--linha")
    L.MAXL = int(argv[i + 1])
    del argv[i:i + 2]
capj, intro, out = argv[:3]
T_IN = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", intro],
                            capture_output=True, text=True).stdout.strip())
TIT = json.load(open(os.path.join(HERE, "titulos", "titulos.json")))
CAPS_EDIT = os.path.join(os.path.dirname(HERE), "edit", "caps")
VOZ_AT = 0.70

itens = []
for c in json.load(open(capj))["chapters"]:
    st = T_IN + c["start"]
    if c["name"].startswith("vinheta-"):
        nn = c["name"][-2:]
        if nn in TIT:
            itens.append([st + VOZ_AT, st + VOZ_AT + TIT[nn]["dur"], TIT[nn]["texto"]])
        continue
    nn = re.match(r"cap(\d\d)", c["name"]).group(1)
    cap = json.load(open(os.path.join(HERE, f"cap{nn}.json")))
    cj = os.path.join(CAPS_EDIT, c["name"] + ".chapter.json")
    voz_de = -float(json.load(open(cj)).get("audio_offset", 0.0)) if os.path.exists(cj) else 0.0
    cortes = c.get("cortes") or []

    def mp(t):
        return t - sum(min(max(t - a, 0.0), b - a) for a, b in cortes)

    ws = []
    for w in L.juntar_numeros(cap["words"]):
        s_, e_ = w["s"] - voz_de, w["e"] - voz_de          # relógio do trecho (cap09b: a voz do cap. 9 a partir do corte)
        if s_ < -0.05 or s_ >= c["dur"] + sum(b - a for a, b in cortes):
            continue
        ws.append(dict(w, s=mp(s_), e=mp(e_)))
    for b in L.blocos(ws):
        itens.append([st + b[0]["s"], st + b[-1]["e"], " ".join(w["w"] for w in b)])

itens.sort()
for i, it in enumerate(itens):
    nxt = itens[i + 1][0] if i + 1 < len(itens) else it[1] + 2
    if it[1] - it[0] < L.MIND:
        it[1] = min(it[0] + L.MIND, nxt - 0.067)
    it[1] = min(it[1] + 0.25, nxt - 0.067) if it[1] + 0.25 <= nxt else min(it[1], nxt - 0.067)
with open(out + ".srt", "w", encoding="utf-8") as f:
    for i, (a, b, t) in enumerate(itens, 1):
        f.write(f"{i}\n{L.ts(a, ',')} --> {L.ts(b, ',')}\n" + "\n".join(L.linhas(t)) + "\n\n")
with open(out + ".vtt", "w", encoding="utf-8") as f:
    f.write("WEBVTT\n\n")
    for a, b, t in itens:
        f.write(f"{L.ts(a, '.')} --> {L.ts(b, '.')}\n" + "\n".join(L.linhas(t)) + "\n\n")
print(f"{len(itens)} legendas, T_IN {T_IN:.2f}s -> {out}.srt / .vtt")
