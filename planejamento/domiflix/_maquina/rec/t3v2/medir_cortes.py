#!/usr/bin/env python3
"""Medidor de `cortes` do T3 v2: trechos em que (1) a tela não muda, (2) o cursor não anda e (3) a voz está calada.

uso: python3 -I medir_cortes.py NN [--min 0.6] [--margem 0.12] [--limiar 0.02]
Lê rec/t3v2/t3v2-capNN.{mp4,telemetry.json,actions.json} e t3v2/narracao/capNN.json; imprime as janelas candidatas
(em s do vídeo do capítulo) já com a margem tirada das duas pontas, e as pausas inseridas (`pausas`) com a parte cortável de cada uma.
Rodar sob `flock $TUT_HOME/.heavy.lock nice -n 10` (decodifica o vídeo inteiro em 160x100 cinza)."""
import json, os, subprocess, sys
import numpy as np

TUT = os.environ.get("TUT_HOME", "/home/claude/domiflix")
FPS = 30


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    nn = int(args[0])
    def opt(nome, padrao):
        return float(args[args.index(nome) + 1]) if nome in args else padrao
    minimo, margem, limiar = opt("--min", 0.6), opt("--margem", 0.12), opt("--limiar", 0.02)
    mp4 = f"{TUT}/rec/t3v2/t3v2-cap{nn:02d}.mp4"
    tele = json.load(open(f"{TUT}/rec/t3v2/t3v2-cap{nn:02d}.telemetry.json"))
    nar = json.load(open(f"{TUT}/t3v2/narracao/cap{nn:02d}.json"))
    # 1) tela parada: diferença média absoluta entre quadros consecutivos (160x100, cinza)
    W, H = 160, 100
    cmd = ["ffmpeg", "-v", "error", "-i", mp4, "-vf", f"fps={FPS},scale={W}:{H}:flags=area,format=gray", "-f", "rawvideo", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    n = len(raw) // (W * H)
    fr = np.frombuffer(raw[: n * W * H], dtype=np.uint8).reshape(n, H, W)
    d = np.abs(np.diff(fr.astype(np.int16), axis=0)).mean(axis=(1, 2))   # d[i] = diferença do quadro i para o i+1
    parada_q = np.concatenate([[True], d < limiar])                       # quadro i igual ao anterior
    # 2) cursor parado: amostras do telemetry (x, y) — parado entre duas amostras se não andou mais de 1 px
    t_s = np.array([s["t"] for s in tele["samples"]])
    xy = np.array([[s["x"], s["y"]] for s in tele["samples"]])
    cursor_move = np.zeros(n, dtype=bool)
    for i in range(1, len(t_s)):
        if np.hypot(*(xy[i] - xy[i - 1])) > 1.0 or tele["samples"][i]["type"] in ("down", "up", "click", "key", "scroll"):
            a, b = int(np.floor(t_s[i - 1] * FPS)), int(np.ceil(t_s[i] * FPS)) + 1
            cursor_move[max(a, 0): min(b, n)] = True
    # 3) voz calada: complemento do vad (segmentos de fala) do capNN.json
    fala = np.zeros(n, dtype=bool)
    for s, e in nar["vad"]:
        fala[max(int(np.floor(s * FPS)) - 1, 0): min(int(np.ceil(e * FPS)) + 1, n)] = True
    # 4) passos do robô: um `click`/`type`/`scroll` em andamento (tStart..tEnd) não é parado mesmo se a tela ainda não mudou
    act = json.load(open(f"{TUT}/rec/t3v2/t3v2-cap{nn:02d}.actions.json"))["actions"]
    passo = np.zeros(n, dtype=bool)
    for a in act:
        if a.get("do") in ("mark", "waitFor", "wait"):
            continue
        s0, e0 = a.get("tStart"), a.get("tEnd")
        if s0 is None or e0 is None:
            continue
        passo[max(int(np.floor(s0 * FPS)), 0): min(int(np.ceil(e0 * FPS)) + 1, n)] = True
    livre = parada_q & ~cursor_move & ~fala

    def janelas(mask):
        out, i = [], 0
        while i < len(mask):
            if mask[i]:
                j = i
                while j + 1 < len(mask) and mask[j + 1]:
                    j += 1
                out.append((i / FPS, (j + 1) / FPS))
                i = j + 1
            else:
                i += 1
        return out

    print(f"cap{nn:02d}: {n} quadros ({n / FPS:.2f} s), limiar {limiar}, margem {margem}, mínimo {minimo}")
    print("janelas (tela parada + cursor parado + voz calada + nenhum passo em andamento):")
    cand = []
    for a, b in janelas(livre):
        a2, b2 = a + margem, b - margem
        if b2 - a2 >= minimo:
            cand.append((round(a2, 2), round(b2, 2)))
            print(f"   [{a2:6.2f}, {b2:6.2f}]  {b2 - a2:4.2f} s   (bruta {a:6.2f}..{b:6.2f})")
    if not cand:
        print("   nenhuma")
    print("pausas inseridas na narração (T original -> posição no capítulo atual) e parte cortável:")
    acum = 0.0
    for T, dur in nar.get("pausas", []):
        ini = T + acum
        acum += dur
        cort = [(a, b) for a, b in cand if a < ini + dur and b > ini]
        print(f"   pausa de {dur:.2f} s em {ini:6.2f}..{ini + dur:6.2f}: " + (", ".join(f"[{max(a, ini):.2f}, {min(b, ini + dur):.2f}]" for a, b in cort) if cort else "nada cortável"))
        a0, b0 = int(round(ini * FPS)), min(int(round((ini + dur) * FPS)), n)
        def faixa(m, nome):
            w = [(x / FPS + a0 / FPS, y / FPS + a0 / FPS) for x, y in janelas(m[a0:b0])]
            return f"      {nome}: " + (", ".join(f"{x:.2f}-{y:.2f}" for x, y in w) if w else "nunca")
        print(faixa(~parada_q, "tela mexe"))
        print(faixa(cursor_move, "cursor/teclas"))
        print(faixa(fala, "voz"))
        em = [f"{a['i']}:{a.get('do')}[{a.get('tStart', 0):.2f}-{a.get('tEnd', 0):.2f}]" + (f" {a['label'][:30]}" if a.get('label') else "") for a in act if a.get('tStart') is not None and a.get('tEnd') is not None and a['tStart'] < ini + dur and a['tEnd'] > ini and a.get('do') != 'mark']
        print("      passos: " + (" | ".join(em) if em else "nenhum"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
