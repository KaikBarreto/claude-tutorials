"""Kit v3 · acha quadros "piscados" num MP4 de cena: elemento que some por um ou poucos quadros e volta (o Chromium
fotografou antes de terminar de pintar um bloco; visto em 19/11 na T08 com --dsf 2). Compara cada quadro com os
vizinhos: salto grande que desfaz logo depois é piscada. Sai com 1 se achar.
uso: python3 -I piscadas.py cena.mp4 [...]   (leve: ~10 s por 20 s de vídeo)"""
import subprocess, sys
import numpy as np
W, H = 320, 200
def quadros(f):
    p = subprocess.Popen(['ffmpeg', '-nostdin', '-v', 'error', '-i', f, '-vf', f'scale={W}:{H},format=gray', '-f', 'rawvideo', '-'], stdout=subprocess.PIPE)
    while True:
        b = p.stdout.read(W * H)
        if len(b) < W * H: break
        yield np.frombuffer(b, np.uint8).astype(np.int16)
ruim = 0
for f in sys.argv[1:]:
    Q = list(quadros(f)); ach = []
    for i in range(1, len(Q)):
        d = np.abs(Q[i] - Q[i - 1]); pico = (d > 12).mean()          # fração da tela que mudou forte de um quadro para o outro
        if pico < .004: continue
        for k in range(1, 13):                                        # desfaz em até 12 quadros?
            if i + k < len(Q) and (np.abs(Q[i + k] - Q[i - 1]) > 12).mean() < pico * .25: ach.append((i, k, pico)); break
    # junta vizinhos
    J = []
    for i, k, p in ach:
        if J and i - J[-1][0] < 15: continue
        J.append((i, k, p))
    print(f"{f}: {len(Q)} quadros, {len(J)} piscada(s)" + ''.join(f"\n   {i / 30:.2f} s (volta em {k} quadro(s), {p * 100:.1f}% da tela)" for i, k, p in J))
    ruim += len(J)
sys.exit(1 if ruim else 0)
