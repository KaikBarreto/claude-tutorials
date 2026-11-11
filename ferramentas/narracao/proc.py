"""Narração do tutorial: recebe os MP3 baixados do ElevenLabs (ou de outro TTS) (um ou mais takes por capítulo, qualquer nome),
descobre o capítulo pelo conteúdo, transcreve (Silero VAD + Parakeet, kit/asr.py), alinha o texto enviado
palavra a palavra e grava, por capítulo:
  takes/<id>/  audio16k.wav, audio48k.wav, words.json, vad.json, transcript.txt
  capNN.json   {take, arquivo, dur, lufs, words:[{w, fala, s, e, ok}], linhas:[{i, texto, s, e}], frases:[...]}
`w` = grafia da legenda (ex.: QR Code); `fala` = como foi escrito pro TTS (ex.: quê-érre côde). Ver config_narracao.json.
Também imprime a conferência das palavras com pronúncia trocada e o que o ASR ouviu em volta.

uso: python3 proc.py <arquivo.mp3> [...]            (escolhe o melhor take por capítulo)
     python3 proc.py --take NN=<arquivo.mp3> [...]  (força o take de um capítulo)"""
import difflib
import json
import os
import re
import subprocess
import sys
import unicodedata

import numpy as np
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(os.path.dirname(os.path.dirname(HERE)), "kit")
sys.path.insert(0, HERE)
from tts_textos import CAPS  # noqa: E402

from config import CFG  # noqa: E402  (config_narracao.json do tutorial: idioma, trocas, unidades, correções)

# grafia da fala -> grafia da legenda (mesmo número de palavras), ex.: ("quê-érre côde", "QR Code")
TROCAS = CFG["trocas"]
ASR_FIX = CFG["asr_fix"]  # {id do take: {o que o ASR ouviu: o certo}}
VIGIAR = {"QR", "Code", "Hi-Wall", "BTUs", "Waze", "Dominex", "LGPD", "CNPJ", "CPF", "CEP", "Site", "checklists"}


def norm(t):
    t = unicodedata.normalize("NFD", t.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", "", t)


def tokens(texto):
    """[(legenda, fala, linha)] na ordem do texto enviado, sem as tags [pause]."""
    out = []
    mapa = dict(TROCAS)
    rx = re.compile(r"(?<!\w)(?:" + "|".join(re.escape(f) for f, _ in sorted(TROCAS, key=lambda p: -len(p[0]))) + r")(?!\w)")  # só palavra inteira ("asas" não pega em "casas")
    for li, linha in enumerate(texto.split("\n")):
        linha = re.sub(r"\[[a-z ]+\]", " ", linha)
        # uma passada só, da troca mais longa para a mais curta (senão "quê-érre" entra dentro de "quê-érre côde")
        linha = rx.sub(lambda m: "\u0000" + m.group(0).replace(" ", "\u0001") + "|" +
                       mapa[m.group(0)].replace(" ", "\u0001") + "\u0000", linha)
        for w in linha.split():
            if "\u0000" in w:
                m = re.match(r"^(.*?)\u0000(.*?)\|(.*?)\u0000(.*)$", w)
                pre, fala, leg, pos = m.groups()
                fs, ls = fala.split("\u0001"), leg.split("\u0001")
                for k, (f, l) in enumerate(zip(fs, ls)):
                    out.append(((pre if k == 0 else "") + l + (pos if k == len(fs) - 1 else ""),
                                (pre if k == 0 else "") + f + (pos if k == len(fs) - 1 else ""), li))
            else:
                out.append((w, w, li))
    return out


def ffmpeg_wav(src, dst, sr, ch):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-ac", str(ch), "-ar", str(sr), "-c:a", "pcm_s16le", dst],
                   check=True)


def lufs(path):
    import pyloudnorm as pyln
    x, sr = sf.read(path)
    return round(float(pyln.Meter(sr).integrated_loudness(x)), 2)


def transcrever(mp3):
    tid = re.sub(r"[^A-Za-z0-9_-]+", "_", os.path.splitext(os.path.basename(mp3))[0])[-60:]
    d = os.path.join(HERE, "takes", tid)
    os.makedirs(d, exist_ok=True)
    if not os.path.exists(os.path.join(d, "words.json")):
        ffmpeg_wav(mp3, os.path.join(d, "audio16k.wav"), 16000, 1)
        ffmpeg_wav(mp3, os.path.join(d, "audio48k.wav"), 48000, 1)
        subprocess.run([sys.executable, "-I", os.path.join(KIT, "asr.py"), d], check=True, stdout=subprocess.DEVNULL)
    words = json.load(open(os.path.join(d, "words.json")))
    if isinstance(words, dict):
        words = words.get("words", words)
    # correções do ASR conferidas à parte (trecho isolado decodificado de novo)
    for w in words:
        w["w"] = ASR_FIX.get(tid, {}).get(w["w"], w["w"])
    return tid, d, words


def capitulo(words):
    ouvido = [norm(w["w"]) for w in words]
    best = None
    for k, txt in CAPS.items():
        alvo = [norm(f) for _, f, _ in tokens(txt)]
        r = difflib.SequenceMatcher(None, alvo, ouvido, autojunk=False).ratio()
        if best is None or r > best[1]:
            best = (k, r)
    return best


def expandir(words):
    """O ASR escreve número em algarismo ("Opções:127,220", "380V."): volta para palavras, com o tempo do token
    repartido pelo tamanho de cada palavra, pra casar com o texto enviado (que está por extenso)."""
    from num2words import num2words
    out = []
    for w in words:
        if not re.search(r"\d", w["w"]):
            out.append(w)
            continue
        partes = []
        for m in re.finditer(r"\d[\d.]*|[^\d,]+", w["w"]):
            p = m.group(0)
            if p[0].isdigit():
                partes += num2words(int(p.replace(".", "")), lang=CFG["idioma"]).split()
            elif p.strip(" .,:;!?") in CFG["unidades"]:
                u = p.strip(" .,:;!?"); partes.append(CFG["unidades"][u] + p.strip(" " + u))
            elif p.strip():
                partes.append(p.strip())
        if not partes:
            out.append(w)
            continue
        tot = sum(len(p) + 1 for p in partes)
        t = w["s"]
        for p in partes:
            d = (w["e"] - w["s"]) * (len(p) + 1) / tot
            out.append({"w": p, "s": round(t, 3), "e": round(t + d, 3)})
            t += d
    return out


def alinhar(toks, words, vad=None):
    """DP (custo de edição com substituição por semelhança) entre o texto enviado e o ASR."""
    words = expandir(words)
    a = [norm(f) for _, f, _ in toks]
    b = [norm(w["w"]) for w in words]
    n, m = len(a), len(b)
    INF = 1e9
    D = np.full((n + 1, m + 1), INF)
    P = np.zeros((n + 1, m + 1), np.int8)
    D[0, :] = np.arange(m + 1) * 0.7
    D[:, 0] = np.arange(n + 1) * 1.0
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            s = difflib.SequenceMatcher(None, a[i - 1], b[j - 1]).ratio() if a[i - 1] != b[j - 1] else 1.0
            c = [D[i - 1, j - 1] + (1 - s) * 1.6, D[i - 1, j] + 1.0, D[i, j - 1] + 0.7]
            k = int(np.argmin(c))
            D[i, j], P[i, j] = c[k], k
    i, j, par, extras = n, m, {}, []
    while i > 0 and j > 0:
        k = P[i, j]
        if k == 0:
            par.setdefault(i - 1, []).append(j - 1)
            i, j = i - 1, j - 1
        elif k == 1:
            i -= 1
        else:
            extras.append((j - 1, i))  # palavra extra do ASR entre o token i-1 e o token i do texto
            j -= 1
    while j > 0:
        extras.append((j - 1, 0))
        j -= 1

    def sim_com(ti, js):
        return difflib.SequenceMatcher(None, a[ti], "".join(b[x] for x in sorted(js))).ratio()

    # cada palavra extra vai para o vizinho que fica mais parecido com ela (ex.: "que" "erre" -> QR)
    for jj, ii in sorted(extras):
        opts = [t for t in (ii - 1, ii) if 0 <= t < n]
        best = max(opts, key=lambda t: sim_com(t, par.get(t, []) + [jj]) - sim_com(t, par.get(t, [])) if par.get(t) else
                   sim_com(t, [jj]))
        par.setdefault(best, []).append(jj)
    out = []
    for i, (leg, fala, li) in enumerate(toks):
        js = sorted(par.get(i, []))
        if js:
            s, e = words[js[0]]["s"], words[js[-1]]["e"]
            sim = difflib.SequenceMatcher(None, a[i], "".join(b[j] for j in js)).ratio()
            out.append({"w": leg, "fala": fala, "linha": li, "s": s, "e": e, "ok": round(sim, 2),
                        "ouvido": " ".join(words[j]["w"] for j in js)})
        else:
            out.append({"w": leg, "fala": fala, "linha": li, "s": None, "e": None, "ok": 0.0, "ouvido": ""})
    # quem ficou sem tempo: o ASR costuma colar a palavra na vizinha ("empresa pronta" -> "empresa" longo,
    # "Monte Verde" -> "Monteverde"). Se há folga entre as vizinhas, a sequência ocupa a folga; senão, divide o
    # tempo da vizinha mais "esticada" (duração por letra) com ela, na proporção do tamanho das palavras.
    def L(t):
        return len(norm(t["fala"])) + 1

    i = 0
    while i < len(out):
        if out[i]["s"] is not None:
            i += 1
            continue
        j = i
        while j < len(out) and out[j]["s"] is None:
            j += 1
        run = out[i:j]
        prv = out[i - 1] if i > 0 else None
        nxt = out[j] if j < len(out) else None
        g0 = prv["e"] if prv else (nxt["s"] if nxt else 0.0)
        g1 = nxt["s"] if nxt else g0
        need = 0.06 * sum(L(t) for t in run)

        def voz(a0, a1):  # fração do intervalo com voz segundo o VAD
            if not vad or a1 <= a0:
                return 1.0
            return sum(max(0.0, min(a1, v1) - max(a0, v0)) for v0, v1 in vad) / (a1 - a0)

        def esticada(t):  # duração do token em relação ao esperado pelo tamanho
            return (t["e"] - t["s"]) / (0.07 * L(t) + 0.05)

        if (g1 - g0 >= need and voz(g0, g1) >= 0.5) or (prv is None and nxt is None):
            grupo, a0, a1 = run, g0, max(g1, g0)
        else:
            rp = esticada(prv) if prv else -1
            rn = esticada(nxt) if nxt else -1
            if rp >= rn:
                grupo, a0, a1 = [prv] + run, prv["s"], prv["e"] if voz(g0, g1) < 0.5 else max(g1, prv["e"])
            else:
                grupo, a0, a1 = run + [nxt], (nxt["s"] if voz(g0, g1) < 0.5 else g0), nxt["e"]
        tot = sum(L(t) for t in grupo)
        t = a0
        for w in grupo:
            d = (a1 - a0) * L(w) / tot
            w["s"], w["e"] = round(t, 3), round(t + d, 3)
            t += d
        i = j
    # sem sobreposição: cada palavra termina no máximo onde a seguinte começa
    for w, nx in zip(out, out[1:]):
        if nx["s"] < w["s"]:
            nx["s"] = w["s"]
        if w["e"] > nx["s"]:
            w["e"] = nx["s"]
    return out


def frases(ws):
    out, cur = [], []
    for w in ws:
        cur.append(w)
        if re.search(r"[.!?…:]$", w["w"]) or w is ws[-1]:
            out.append({"texto": " ".join(x["w"] for x in cur), "s": cur[0]["s"], "e": cur[-1]["e"]})
            cur = []
    return out


def main(args):
    forcados, soltos = {}, []
    for a in args:
        if a.startswith("--take"):
            continue
        if re.match(r"^\d{1,2}=", a):
            k, p = a.split("=", 1)
            forcados[int(k)] = p
        else:
            soltos.append(a)
    cand = {}
    for mp3 in soltos + list(forcados.values()):
        tid, d, words = transcrever(mp3)
        k, r = capitulo(words)
        if mp3 in forcados.values():
            k = next(kk for kk, p in forcados.items() if p == mp3)
        toks = tokens(CAPS[k])
        ws = alinhar(toks, words, json.load(open(os.path.join(d, "vad.json"))))
        dur = sf.info(os.path.join(d, "audio48k.wav")).duration
        faltas = [w for w in ws if w["ok"] < 0.5]
        info = {"cap": k, "take": tid, "arquivo": os.path.abspath(mp3), "pasta": d, "dur": round(dur, 3),
                "lufs": lufs(os.path.join(d, "audio48k.wav")), "semelhanca": round(r, 3),
                "palavras_fracas": len(faltas), "words": ws}
        cand.setdefault(k, []).append(info)
        print(f"{os.path.basename(mp3)} -> cap {k} (semelhança {r:.2f}), {dur:.2f} s, {info['lufs']} LUFS, "
              f"{len(faltas)} palavras fracas")
    for k in sorted(cand):
        esc = sorted(cand[k], key=lambda c: (c["palavras_fracas"], -c["semelhanca"]))[0]
        if k in forcados:
            esc = next(c for c in cand[k] if c["arquivo"] == os.path.abspath(forcados[k]))
        ws = esc["words"]
        linhas = []
        for li in sorted({w["linha"] for w in ws}):
            lw = [w for w in ws if w["linha"] == li]
            linhas.append({"i": li, "texto": " ".join(w["w"] for w in lw), "s": lw[0]["s"], "e": lw[-1]["e"]})
        out = dict(esc, linhas=linhas, frases=frases(ws), vad=json.load(open(os.path.join(esc["pasta"], "vad.json"))))
        json.dump(out, open(os.path.join(HERE, f"cap{k:02d}.json"), "w"), ensure_ascii=False, indent=1)
        print(f"\n== cap {k:02d}: take {esc['take']} ({len(cand[k])} candidato(s)), {esc['dur']:.2f} s")
        for w in ws:
            base = w["w"].strip(".,;:!?…\"“”")
            if base in VIGIAR or w["ok"] < 0.5:
                print(f"   {w['s']:7.2f}  {w['w']:<16} ouvido: {w['ouvido']!r} (ok {w['ok']})")


if __name__ == "__main__":
    main(sys.argv[1:])
