#!/usr/bin/env python3
"""Confere uma aula remendada (remendar_aula.py) contra a versão entregue antes de trocar o arquivo da entrega.

uso: python3 -I conferir_remendo.py antigo.mp4 novo.mp4 --novos INICIO:FIM [--emendas t1,t2,...]
                                    [--srt antigo.srt novo.srt]
  INICIO  primeiro instante do vídeo NOVO que muda (fim do último capítulo antigo antes dos novos)
  FIM     primeiro instante do vídeo NOVO que volta a ser o antigo (começo do capítulo antigo depois dos novos)
  --emendas  instantes (vídeo novo) das emendas para olhar o áudio; padrão: INICIO e FIM

Confere: (1) quadros iguais ao antigo antes de INICIO e, depois de FIM, iguais ao antigo deslocado (o deslocamento em
quadros inteiros é achado sozinho); (2) áudio em volta de cada emenda sem buraco (< -60 dB) e sem salto de amostra fora
do normal do próprio vídeo antigo; (3) legendas: falas antes de INICIO idênticas, depois de FIM com o mesmo texto e o
tempo deslocado. Sai com código 1 se algo falhar. Leva ~1 min numa aula de 14 min (não precisa da trava pesada).
"""
import re
import subprocess
import sys

import numpy as np


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
    a = sys.argv[1:]
    if len(a) < 4 or "--novos" not in a:
        sys.exit(__doc__)
    old, new = a[0], a[1]
    ini, fim = [float(x) for x in a[a.index("--novos") + 1].split(":")]
    emendas = [float(x) for x in a[a.index("--emendas") + 1].split(",")] if "--emendas" in a else [ini, fim]
    falhas = []
    do, dn, fr = dur(old), dur(new), fps(new)
    # deslocamento em quadros inteiros: o melhor casamento em volta de (dn - do), 6 s depois de FIM
    base, t = round((dn - do) * fr), min(fim + 6, dn - 2)
    qn = quadro(new, t)
    desl = min(range(base - 3, base + 4), key=lambda k: np.abs(quadro(old, t - k / fr) - qn).mean()) / fr
    print(f"duração antiga {do:.2f} s, nova {dn:.2f} s; deslocamento depois dos novos {desl:+.3f} s ({round(desl * fr)} quadros)")
    for t in [x for x in (5, ini * 0.33, ini * 0.66, ini - 3) if 1 < x < ini]:
        d = np.abs(quadro(old, t) - quadro(new, t)).mean()
        print(f"  antes  {t:8.2f}: diferença {d:5.2f}")
        if d > 1.0:
            falhas.append(f"quadro {t:.2f} diferente do antigo")
    for t in [x for x in (fim + 6, fim + (dn - fim) * 0.4, fim + (dn - fim) * 0.8, dn - 8) if fim < x < dn - 1]:
        d = np.abs(quadro(old, t - desl) - quadro(new, t)).mean()
        print(f"  depois {t:8.2f} (antigo {t - desl:8.2f}): diferença {d:5.2f}")
        if d > 1.0:
            falhas.append(f"quadro {t:.2f} diferente do antigo deslocado")
    ref = max(float(np.abs(np.diff(audio(old, c - 3, c + 3))).max()) for c in (do * 0.25, do * 0.5, do * 0.75))
    print(f"  áudio: maior salto entre amostras no antigo (3 trechos de 6 s) = {ref:.3f}")
    for s in emendas:
        x = audio(new, s - 3, s + 3)
        n = len(x) // 960
        db = 20 * np.log10(np.sqrt((x[:n * 960].reshape(n, 960) ** 2).mean(1) + 1e-12))
        salto, mudo = float(np.abs(np.diff(x)).max()), int((db < -60).sum())
        print(f"  emenda {s:8.2f}: rms (20 ms) {db.min():6.1f} a {db.max():5.1f} dB, maior salto {salto:.3f}, janelas mudas {mudo}")
        if mudo:
            falhas.append(f"buraco no áudio em {s:.2f}")
        if salto > max(1.0, ref * 1.3):
            falhas.append(f"salto de amostra em {s:.2f} ({salto:.2f})")
    if "--srt" in a:
        so, sn = srt(a[a.index("--srt") + 1]), srt(a[a.index("--srt") + 2])
        A, An = [c for c in so if c[1] <= ini + 0.01], [c for c in sn if c[1] <= ini + 0.01]
        B, Bn = [c for c in so if c[0] >= fim - desl - 0.01], [c for c in sn if c[0] >= fim - 0.01]
        okA = len(A) == len(An) and all(x[2] == y[2] and abs(x[0] - y[0]) < 0.02 for x, y in zip(A, An))
        okB = len(B) == len(Bn) and all(x[2] == y[2] and abs(x[0] + desl - y[0]) < 0.06 for x, y in zip(B, Bn))
        print(f"  legendas: {len(so)} -> {len(sn)} falas; antes iguais {okA} ({len(A)}/{len(An)}); depois deslocadas {okB} "
              f"({len(B)}/{len(Bn)}); última fala termina {sn[-1][1]:.2f} s")
        if not (okA and okB):
            falhas.append("legenda fora dos capítulos novos mudou")
        if sn[-1][1] > dn:
            falhas.append("legenda passa do fim do vídeo")
    print("OK" if not falhas else "FALHOU: " + "; ".join(falhas))
    sys.exit(1 if falhas else 0)


if __name__ == "__main__":
    main()
