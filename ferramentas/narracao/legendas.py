"""Legendas (.srt e .vtt) do tutorial a partir dos tempos por palavra da narração (capNN.json).
Regras: até 42 caracteres por linha e 2 linhas; quebra preferida em fim de frase, depois em vírgula/dois-pontos;
mínimo de 1 s na tela (estende sem invadir a próxima), máximo 6,5 s; números na forma de leitura da tela.

uso: python3 legendas.py <saida_sem_extensao> NN[@offset] [NN[@offset] ...]
  ex.: python3 legendas.py ../edit/out/cap02/cap02 02            (prévia de um capítulo, offset 0)
       python3 legendas.py ../edit/out/aula/T3 00@4.0 01@33.9 ...  (aula inteira: início de cada capítulo no vídeo final)"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MAXL, MAXLINES, MIND, MAXD = 42, 2, 1.0, 6.5

# sequência falada (grafia da legenda, minúsculas, sem pontuação) -> como escrever na legenda (config_narracao.json)
sys.path.insert(0, HERE)
from config import CFG  # noqa: E402
NUMEROS = CFG["numeros"]


def chave(w):
    return re.sub(r"[^\wÀ-ú-]+", "", w.lower())


def juntar_numeros(ws):
    out, i = [], 0
    while i < len(ws):
        feito = False
        for seq, txt in NUMEROS:
            n = len(seq.split())
            if " ".join(chave(w["w"]) for w in ws[i:i + n]) == seq:
                pont = re.search(r"[.,:;!?…]+$", ws[i + n - 1]["w"])
                out.append({"w": txt + (pont.group(0) if pont else ""), "s": ws[i]["s"], "e": ws[i + n - 1]["e"]})
                i += n
                feito = True
                break
        if not feito:
            out.append(dict(ws[i]))
            i += 1
    return out


def linhas(texto):
    """quebra um bloco em até 2 linhas equilibradas"""
    if len(texto) <= MAXL:
        return [texto]
    pal = texto.split()
    best = None
    for k in range(1, len(pal)):
        a, b = " ".join(pal[:k]), " ".join(pal[k:])
        if len(a) > MAXL or len(b) > MAXL:
            continue
        custo = abs(len(a) - len(b)) - (12 if re.search(r"[,:;]$", a) else 0)
        if best is None or custo < best[0]:
            best = (custo, [a, b])
    return best[1] if best else [texto]


def blocos(ws):
    """agrupa palavras em legendas de até 2 linhas, cortando de preferência em fim de frase ou vírgula"""
    def txt(lst):
        return " ".join(w["w"] for w in lst)

    def cabe(lst):
        t = txt(lst)
        return len(t) <= MAXL * MAXLINES - 4 and len(linhas(t)) <= MAXLINES and max(len(l) for l in linhas(t)) <= MAXL and (lst[-1]["e"] - lst[0]["s"]) <= MAXD

    def partir(s):
        """frase que não cabe numa legenda: divide em partes equilibradas, de preferência depois de vírgula"""
        if len(s) < 2 or cabe(s):
            return [s]
        tot = len(txt(s))
        best = None
        for k in range(1, len(s)):
            custo = abs(len(txt(s[:k])) - tot / 2) - (14 if re.search(r"[,:;]$", s[k - 1]["w"]) else 0)
            if best is None or custo < best[0]:
                best = (custo, k)
        return partir(s[:best[1]]) + partir(s[best[1]:])

    frases, cur = [], []
    for w in ws:
        cur.append(w)
        if re.search(r"[.!?…]$", w["w"]):
            frases.append(cur)
            cur = []
    if cur:
        frases.append(cur)
    out = [p for f in frases for p in partir(f)]
    # bloco muito curto ("220.", "Salvar.") gruda no vizinho se couber
    res = []
    for b in out:
        t = " ".join(w["w"] for w in b)
        if res and len(t) < 14 and cabe(res[-1] + b):
            res[-1] = res[-1] + b
        else:
            res.append(b)
    return res


def ts(t, sep):
    # arredonda para milissegundos ANTES de separar h/m/s (88,9999 s saía "00:01:28,000", um segundo adiantado)
    ms = int(round(max(0.0, t) * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d}{sep}{ms % 1000:03d}"


def main(out, caps):
    itens = []
    for c in caps:
        nn, _, off = c.partition("@")
        off = float(off or 0)
        cap = json.load(open(os.path.join(HERE, f"cap{int(nn):02d}.json")))
        ws = juntar_numeros(cap["words"])
        for b in blocos(ws):
            itens.append([b[0]["s"] + off, b[-1]["e"] + off, " ".join(w["w"] for w in b)])
    itens.sort()
    for i, it in enumerate(itens):
        nxt = itens[i + 1][0] if i + 1 < len(itens) else it[1] + 2
        if it[1] - it[0] < MIND:
            it[1] = min(it[0] + MIND, nxt - 0.067)
        it[1] = min(it[1] + 0.25, nxt - 0.067) if it[1] + 0.25 <= nxt else min(it[1], nxt - 0.067)
    with open(out + ".srt", "w", encoding="utf-8") as f:
        for i, (a, b, t) in enumerate(itens, 1):
            f.write(f"{i}\n{ts(a, ',')} --> {ts(b, ',')}\n" + "\n".join(linhas(t)) + "\n\n")
    with open(out + ".vtt", "w", encoding="utf-8") as f:
        f.write("WEBVTT\n\n")
        for i, (a, b, t) in enumerate(itens, 1):
            f.write(f"{ts(a, '.')} --> {ts(b, '.')}\n" + "\n".join(linhas(t)) + "\n\n")
    print(f"{len(itens)} legendas -> {out}.srt / .vtt")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
