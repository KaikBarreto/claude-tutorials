"""Insere silêncios na narração de UM capítulo quando o ritmo real da tela pede mais tempo do que a fala deixa (formulários lentos,
espera de gravação do app): a voz continua a mesma, só ganha respiros entre frases. A tela continua mexendo nesses respiros (ou o
trecho parado é cortado depois, com "cortes" no spec: o finish.py tira vídeo e áudio juntos).

uso: python3 -I pausas.py NN T:DUR [T:DUR ...]
  T   = instante, em s da narração ORIGINAL, no vão entre duas frases (nenhuma palavra pode atravessá-lo)
  DUR = duração do silêncio, em s
Lê emendas/capNN.orig.json (a cópia do capNN.json antes da primeira pausa; criada na 1ª execução) e regrava:
  takes/<take>_pausas/audio48k.wav (áudio com os silêncios) e capNN.json (palavras, linhas, frases, vad, dur e "pasta" apontando
  para o áudio novo). Rodar de novo com outros pontos recomeça sempre do original. `--desfazer` volta ao original."""
import json
import os
import shutil
import sys

import numpy as np
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
EM = os.path.join(HERE, "emendas")


def main(argv):
    if len(argv) < 2 or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    nn = f"{int(argv[0]):02d}"
    cur = os.path.join(HERE, f"cap{nn}.json")
    orig = os.path.join(EM, f"cap{nn}.orig.json")
    os.makedirs(EM, exist_ok=True)
    if not os.path.exists(orig):
        shutil.copy2(cur, orig)
    if argv[1] == "--desfazer":
        shutil.copy2(orig, cur)
        print(f"cap{nn}: narração original restaurada")
        return 0
    pts = sorted((float(a), float(b)) for a, b in (x.split(":") for x in argv[1:]))
    d = json.load(open(orig, encoding="utf-8"))

    def mp(x, fim=False):  # tempo original -> tempo com as pausas; o FIM de uma palavra/linha que termina exatamente no ponto fica antes da pausa
        return round(x + sum(b for a, b in pts if (x > a + 1e-9 if fim else x >= a - 1e-9)), 3)

    def vao(s, e):  # nenhuma palavra/intervalo pode atravessar um ponto de inserção
        return not any(s < a < e for a, _ in pts)

    for w in d["words"]:
        if not vao(w["s"], w["e"]):
            sys.exit(f"a palavra {w['w']!r} ({w['s']}-{w['e']}) atravessa um ponto de inserção")
        w["s"], w["e"] = mp(w["s"]), mp(w["e"], True)
    for k in ("linhas", "frases"):
        for x in d[k]:
            # uma linha/frase pode conter o ponto (é o caso das linhas): só o início e o fim movem, e o fim leva todas as pausas dentro dela
            x["s"], x["e"] = mp(x["s"]), mp(x["e"], True)
    for v in d.get("vad") or []:
        if not vao(v[0], v[1]):
            sys.exit(f"um trecho de voz ({v}) atravessa um ponto de inserção")
    d["vad"] = [[mp(a), mp(b, True)] for a, b in d.get("vad") or []]
    d["dur"] = round(d["dur"] + sum(b for _, b in pts), 3)
    d["pausas"] = [[a, b] for a, b in pts]

    od = json.load(open(orig, encoding="utf-8"))
    wav = os.path.join(od["pasta"], "audio48k.wav")
    x, sr = sf.read(wav, dtype="float32")
    x = x.mean(1) if x.ndim == 2 else x
    partes, ult = [], 0
    for a, b in pts:
        i = int(round(a * sr))
        partes += [x[ult:i], np.zeros(int(round(b * sr)), np.float32)]
        ult = i
    partes.append(x[ult:])
    y = np.concatenate(partes)
    nova = od["pasta"].rstrip("/") + "_pausas"
    os.makedirs(nova, exist_ok=True)
    sf.write(os.path.join(nova, "audio48k.wav"), y, sr, subtype="FLOAT")
    d["pasta"] = nova
    json.dump(d, open(cur, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"cap{nn}: {len(pts)} pausa(s) = {sum(b for _, b in pts):.2f} s; narração {od['dur']:.2f} s -> {d['dur']:.2f} s ({len(y) / sr:.2f} s de áudio)")
    for i, ln in enumerate(d["linhas"], 1):
        print(f"   L{i}: {ln['s']} - {ln['e']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
