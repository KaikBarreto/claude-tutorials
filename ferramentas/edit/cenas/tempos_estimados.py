"""Tempos estimados de uma fala (sem a voz) no formato do capNN.json do proc.py, para montar e conferir cenas ilustradas
antes de gerar a voz (a EcoFlix grava a voz por último). Ritmo padrão: 790 caracteres por minuto (o da trilha EcoFlix),
respiro de 0,35 s entre linhas e de 0,15 s depois de vírgula. Quando a voz chega, o proc.py grava o capNN.json de
verdade e as cenas, presas a palavras com W(linha, 'palavra'), se ajustam sozinhas.
uso: python3 tempos_estimados.py <saida capNN.json> "linha 0 da fala" "linha 1" ...  [--cap N] [--cpm 790] [--inicio 0.4]
     python3 tempos_estimados.py <saida capNN.json> --arquivo falas.txt                 (uma linha da fala por linha)"""
import json
import re
import sys


def estimar(linhas, cpm=790.0, inicio=0.4, respiro=0.35, virgula=0.15):
    cps = cpm / 60.0
    t, words, out = inicio, [], []
    for i, texto in enumerate(linhas):
        s0 = t
        for w in texto.split():
            d = (len(w) + 1) / cps
            words.append({"w": w, "fala": w, "linha": i, "s": round(t, 3), "e": round(t + d, 3)})
            t += d + (virgula if re.search(r"[,;:]$", w) else 0.0)
        out.append({"i": i, "texto": texto, "s": round(s0, 3), "e": round(t, 3)})
        t += respiro
    return {"dur": round(t + 0.4, 3), "words": words, "linhas": out}


def main(argv):
    opt = lambda k, d: argv[argv.index(k) + 1] if k in argv else d  # noqa: E731
    pos, pula = [], {"--cap", "--cpm", "--inicio", "--arquivo"}
    i = 0
    while i < len(argv):
        if argv[i] in pula:
            i += 2
            continue
        pos.append(argv[i]); i += 1
    if not pos:
        sys.exit(__doc__)
    saida, linhas = pos[0], pos[1:]
    if "--arquivo" in argv:
        linhas = [l.strip() for l in open(opt("--arquivo", ""), encoding="utf-8") if l.strip()]
    if not linhas:
        sys.exit("sem falas: passe as linhas como argumentos ou --arquivo")
    d = estimar(linhas, float(opt("--cpm", 790)), float(opt("--inicio", 0.4)))
    d = {"cap": int(opt("--cap", 0)), "estimado": True, **d}
    json.dump(d, open(saida, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{saida}: {len(linhas)} linhas, {len(d['words'])} palavras, {d['dur']:.1f} s (estimado)")


if __name__ == "__main__":
    main(sys.argv[1:])
