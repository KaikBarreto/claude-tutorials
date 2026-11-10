"""Tempos estimados de uma fala (sem a voz) no formato do capNN.json do proc.py, para montar e conferir cenas ilustradas
antes de gerar a voz (a EcoFlix grava a voz por último). Ritmo padrão: 790 caracteres por minuto (o da trilha EcoFlix),
respiro de 0,35 s entre linhas e de 0,15 s depois de vírgula. Quando a voz chega, o proc.py grava o capNN.json de
verdade e as cenas, presas a palavras com W(linha, 'palavra'), se ajustam sozinhas.
uso: python3 tempos_estimados.py <saida capNN.json> "linha 0 da fala" "linha 1" ...  [--cap N] [--cpm 790] [--inicio 0.4]
     python3 tempos_estimados.py <saida capNN.json> --arquivo falas.txt                 (uma linha da fala por linha)
     python3 tempos_estimados.py <saida capNN.json> --tts narracao/tts_textos.py --cap N [--config config_narracao.json]
         lê o CAPS[N] da aula como o proc.py: tags [pause] fora (contam 0,5 s; [short pause] 0,25 s), trocas do config
         aplicadas ("w" = grafia da legenda, a que o W(linha, 'palavra') procura; "fala" = a do TTS, que dá a duração).
         Sem --config, usa o config_narracao.json ao lado do tts_textos.py."""
import json
import os
import re
import runpy
import sys

PAUSAS = {"pause": 0.5, "short pause": 0.25, "long pause": 0.9}
TAG = r"\[[a-z ]+\]"


def linhas_tts(texto, trocas):
    """Cada linha do texto como ([(legenda, fala, pausa_antes)], pausa_no_fim), igual ao tokens() do proc.py."""
    mapa = dict(trocas)
    rx = re.compile("|".join(re.escape(f) for f, _ in sorted(trocas, key=lambda p: -len(p[0])))) if trocas else None
    linhas = []
    for linha in texto.split("\n"):
        toks, pend = [], 0.0
        for parte in re.split("(" + TAG + ")", linha):
            if re.fullmatch(TAG, parte):
                pend += PAUSAS.get(parte[1:-1], 0.0)
                continue
            if rx:  # uma passada só, da troca mais longa para a mais curta (como no proc.py)
                parte = rx.sub(lambda m: "\u0000" + m.group(0).replace(" ", "\u0001") + "|" +
                               mapa[m.group(0)].replace(" ", "\u0001") + "\u0000", parte)
            for w in parte.split():
                if "\u0000" in w:
                    pre, fala, leg, pos = re.match(r"^(.*?)\u0000(.*?)\|(.*?)\u0000(.*)$", w).groups()
                    fs, ls = fala.split("\u0001"), leg.split("\u0001")
                    for k, (f, l) in enumerate(zip(fs, ls)):
                        a, b = (pre if k == 0 else ""), (pos if k == len(fs) - 1 else "")
                        toks.append((a + l + b, a + f + b, pend))
                        pend = 0.0
                else:
                    toks.append((w, w, pend))
                    pend = 0.0
        linhas.append((toks, pend))
    return linhas


def estimar(linhas, cpm=790.0, inicio=0.4, respiro=0.35, virgula=0.15):
    """linhas: textos (uma fala por item) ou a saída de linhas_tts()."""
    cps = cpm / 60.0
    t, words, out = inicio, [], []
    for i, linha in enumerate(linhas):
        toks, cauda = ([(w, w, 0.0) for w in linha.split()], 0.0) if isinstance(linha, str) else linha
        s0 = None
        for leg, fala, pausa in toks:
            t += pausa
            s0 = t if s0 is None else s0
            d = (len(fala) + 1) / cps
            words.append({"w": leg, "fala": fala, "linha": i, "s": round(t, 3), "e": round(t + d, 3)})
            t += d + (virgula if re.search(r"[,;:]$", fala) else 0.0)
        texto = linha if isinstance(linha, str) else " ".join(l for l, _, _ in toks)
        out.append({"i": i, "texto": texto, "s": round(t if s0 is None else s0, 3), "e": round(t, 3)})
        t += cauda + respiro
    return {"dur": round(t + 0.4, 3), "words": words, "linhas": out}


def main(argv):
    opt = lambda k, d: argv[argv.index(k) + 1] if k in argv else d  # noqa: E731
    pos, pula = [], {"--cap", "--cpm", "--inicio", "--arquivo", "--tts", "--config"}
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
    if "--tts" in argv:
        tts = opt("--tts", "")
        if "--cap" not in argv:
            sys.exit("--tts pede --cap N (o capítulo do CAPS)")
        caps = runpy.run_path(tts, run_name="tempos")["CAPS"]
        cfg = json.load(open(opt("--config", os.path.join(os.path.dirname(os.path.abspath(tts)), "config_narracao.json")),
                             encoding="utf-8"))
        linhas = linhas_tts(caps[int(opt("--cap", 0))].strip("\n"), cfg.get("trocas", []))
    if not linhas:
        sys.exit("sem falas: passe as linhas como argumentos, --arquivo ou --tts")
    d = estimar(linhas, float(opt("--cpm", 790)), float(opt("--inicio", 0.4)))
    d = {"cap": int(opt("--cap", 0)), "estimado": True, **d}
    json.dump(d, open(saida, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{saida}: {len(linhas)} linhas, {len(d['words'])} palavras, {d['dur']:.1f} s (estimado)")


if __name__ == "__main__":
    main(sys.argv[1:])
