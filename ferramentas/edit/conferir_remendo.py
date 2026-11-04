#!/usr/bin/env python3
"""Confere uma aula remendada (remendar_aula.py) contra a versão entregue antes de trocar o arquivo da entrega.

uso: python3 -I conferir_remendo.py antigo.mp4 novo.mp4 --novos INICIO:FIM[,INICIO:FIM...] [--emendas t1,t2,...]
                                    [--srt antigo.srt novo.srt]
  INICIO  primeiro instante do vídeo NOVO que muda (fim do último capítulo antigo antes dos novos)
  FIM     primeiro instante do vídeo NOVO que volta a ser o antigo (começo do capítulo antigo depois dos novos)
          Mais de um trecho novo (ex.: T4, caps 07-08 e 14): um INICIO:FIM por trecho, separados por vírgula, em ordem.
  --emendas  instantes (vídeo novo) das emendas para olhar o áudio; padrão: todos os INICIO e FIM

Confere: (1) quadros iguais ao antigo antes do primeiro INICIO e, em cada trecho antigo depois de um FIM, iguais ao antigo
deslocado (deslocamento em quadros inteiros, achado sozinho trecho a trecho); (2) áudio em volta de cada emenda sem buraco
(< -60 dB) que o antigo não tenha no mesmo ponto e sem salto de amostra fora do normal do próprio vídeo antigo; (3) legendas: falas antes do primeiro INICIO
idênticas e, em cada trecho antigo, com o mesmo texto e o tempo deslocado. Sai com código 1 se algo falhar. Leva ~1 min numa
aula de 14 min (não precisa da trava pesada).
"""
import re
import subprocess
import sys

import numpy as np

FR = 30.0  # quadros por segundo do vídeo novo (lido em main)


def dur(f):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))


def fps(f):
    n, d = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                    "stream=r_frame_rate", "-of", "csv=p=0", f]).decode().strip().split("/")
    return float(n) / float(d)


def quadro(f, t):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-ss", f"{max(t, 0):.4f}", "-i", f, "-frames:v", "1",
                                   "-vf", "scale=480:270", "-f", "rawvideo", "-pix_fmt", "gray", "-"])
    return np.frombuffer(raw, np.uint8).astype(np.float32)


def janela(f, n0, n, w=160, h=90):
    """n quadros seguidos a partir do quadro n0, em cinza w x h, num processo só."""
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-ss", f"{max(n0 - 0.25, 0) / FR:.5f}", "-i", f, "-frames:v",
                                   str(n), "-vf", f"scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "gray", "-"])
    return np.frombuffer(raw, np.uint8).astype(np.float32).reshape(-1, w * h)


def achar_desl(old, new, b, e, busca=10.0):
    """Deslocamento do trecho antigo [b, e) do vídeo novo, até ±busca s: assinatura de 8 quadros, 0,5 s entre eles."""
    span = 7 * 15
    m = round((b + max(0.5, min(6.0, (e - b) / 2 - span / FR / 2))) * FR)
    S = round(busca * FR)
    sig = janela(new, m, span + 1)[::15]
    lo = max(m - S, 0)
    ow = janela(old, lo, m + S + span + 1 - lo)
    best = (float("inf"), 0)
    for s in range(-S, S + 1):
        idx = m - s - lo + np.arange(0, span + 1, 15)
        if idx[0] >= 0 and idx[-1] < len(ow) and len(sig) == len(idx):
            best = min(best, (float(np.abs(ow[idx] - sig).mean()), s))
    return best[1] / FR, best[0]


def audio(f, a, b):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-ss", f"{max(a, 0):.3f}", "-t", f"{b - a:.3f}", "-i", f,
                                   "-ac", "1", "-ar", "48000", "-f", "f32le", "-"])
    return np.frombuffer(raw, np.float32)


def srt(f):
    falas = []
    for blk in open(f, encoding="utf-8").read().strip().split("\n\n"):
        L = blk.strip().split("\n")
        m = re.match(r"(\d+):(\d+):(\d+),(\d+) --> (\d+):(\d+):(\d+),(\d+)", L[1]) if len(L) >= 3 else None
        if m:
            g = [int(v) for v in m.groups()]
            falas.append((g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000, g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000,
                          " ".join(L[2:])))
    return falas


def main():
    global FR
    a = sys.argv[1:]
    if len(a) < 4 or "--novos" not in a:
        sys.exit(__doc__)
    old, new = a[0], a[1]
    trechos = [tuple(float(x) for x in r.split(":")) for r in a[a.index("--novos") + 1].split(",")]
    emendas = ([float(x) for x in a[a.index("--emendas") + 1].split(",")] if "--emendas" in a
               else [t for r in trechos for t in r])
    falhas = []
    do, dn, FR = dur(old), dur(new), fps(new)
    ini = trechos[0][0]
    print(f"duração antiga {do:.2f} s, nova {dn:.2f} s")
    # trechos antigos depois de cada FIM ([b, e) no vídeo novo) e o deslocamento de cada um
    segs = []
    for k, (_, b) in enumerate(trechos):
        ultimo = k + 1 == len(trechos)
        e = dn if ultimo else trechos[k + 1][0]
        if ultimo:  # o fim dos dois vídeos é o mesmo: o deslocamento é a diferença de duração, em quadros inteiros
            base, t = round((dn - do) * FR), min(b + 6, dn - 2)
            qn = quadro(new, t)
            desl = min(range(base - 3, base + 4), key=lambda s: np.abs(quadro(old, t - s / FR) - qn).mean()) / FR
        else:
            desl, dmin = achar_desl(old, new, b, e)
            if dmin > 1.0:
                falhas.append(f"trecho antigo {b:.2f}-{e:.2f} não achado no vídeo antigo (diferença {dmin:.2f})")
        segs.append((b, e, desl, ultimo))
        print(f"  trecho antigo {b:8.2f} a {e:8.2f}: deslocamento {desl:+.3f} s ({round(desl * FR)} quadros)")
    for t in sorted(x for x in (5, ini * 0.33, ini * 0.66, ini - 3) if 1 < x < ini):
        d = np.abs(quadro(old, t) - quadro(new, t)).mean()
        print(f"  antes  {t:8.2f}: diferença {d:5.2f}")
        if d > 1.0:
            falhas.append(f"quadro {t:.2f} diferente do antigo")
    for b, e, desl, ultimo in segs:
        for t in sorted(x for x in (b + 6, b + (e - b) * 0.4, b + (e - b) * 0.8, e - (8 if ultimo else 3)) if b < x < e - 1):
            d = np.abs(quadro(old, t - desl) - quadro(new, t)).mean()
            print(f"  depois {t:8.2f} (antigo {t - desl:8.2f}): diferença {d:5.2f}")
            if d > 1.0:
                falhas.append(f"quadro {t:.2f} diferente do antigo deslocado")
    ref = max(float(np.abs(np.diff(audio(old, c - 3, c + 3))).max()) for c in (do * 0.25, do * 0.5, do * 0.75))
    print(f"  áudio: maior salto entre amostras no antigo (3 trechos de 6 s) = {ref:.3f}")

    def rms(x):
        n = len(x) // 960
        return 20 * np.log10(np.sqrt((x[:n * 960].reshape(n, 960) ** 2).mean(1) + 1e-12))

    todos = [(0.0, ini, 0.0)] + [(b, e, d) for b, e, d, _ in segs]
    for s in emendas:
        x = audio(new, s - 3, s + 3)
        db = rms(x)
        # silêncio que já existe no antigo, no mesmo ponto do trecho antigo vizinho (ex.: a pausa antes da cartela), não conta
        d = min(todos, key=lambda g: 0 if g[0] <= s <= g[1] else min(abs(s - g[0]), abs(s - g[1])))[2]
        dbo = rms(audio(old, s - d - 3, s - d + 3))
        k = min(len(db), len(dbo))
        salto, mudo = float(np.abs(np.diff(x)).max()), int(((db[:k] < -60) & (dbo[:k] >= -60)).sum())
        ja = int((db < -60).sum()) - mudo
        print(f"  emenda {s:8.2f}: rms (20 ms) {db.min():6.1f} a {db.max():5.1f} dB, maior salto {salto:.3f}, janelas mudas {mudo}"
              + (f" (+{ja} que o antigo já tinha)" if ja else ""))
        if mudo:
            falhas.append(f"buraco no áudio em {s:.2f}")
        if salto > max(1.0, ref * 1.3):
            falhas.append(f"salto de amostra em {s:.2f} ({salto:.2f})")
    if "--srt" in a:
        so, sn = srt(a[a.index("--srt") + 1]), srt(a[a.index("--srt") + 2])
        A, An = [c for c in so if c[1] <= ini + 0.01], [c for c in sn if c[1] <= ini + 0.01]
        ok = len(A) == len(An) and all(x[2] == y[2] and abs(x[0] - y[0]) < 0.02 for x, y in zip(A, An))
        msg = f"  legendas: {len(so)} -> {len(sn)} falas; antes iguais {ok} ({len(A)}/{len(An)})"
        for b, e, desl, ultimo in segs:
            B = [c for c in so if c[0] >= b - desl - 0.01 and (ultimo or c[1] <= e - desl + 0.01)]
            Bn = [c for c in sn if c[0] >= b - 0.01 and (ultimo or c[1] <= e + 0.01)]
            okB = len(B) == len(Bn) and all(x[2] == y[2] and abs(x[0] + desl - y[0]) < 0.06 for x, y in zip(B, Bn))
            msg += f"; deslocadas a partir de {b:.2f} {okB} ({len(B)}/{len(Bn)})"
            ok = ok and okB
        print(msg + f"; última fala termina {sn[-1][1]:.2f} s")
        if not ok:
            falhas.append("legenda fora dos capítulos novos mudou")
        if sn[-1][1] > dn:
            falhas.append("legenda passa do fim do vídeo")
    print("OK" if not falhas else "FALHOU: " + "; ".join(falhas))
    sys.exit(1 if falhas else 0)


if __name__ == "__main__":
    main()
