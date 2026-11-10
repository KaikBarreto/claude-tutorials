"""Pico real acima de -1 dBTP DEPOIS do AAC (lição do T8: o mix.wav estava em -4,7 dBFS e o AAC 192k estourou a -0,6 dBTP num "s" forte).
Acha os trechos no áudio do MP4 (sobreamostragem 4x, segundo a segundo, com folga entre blocos), baixa 3 dB só neles no mix.wav (janela
de +-65 ms com rampas de 20 ms) e grava um mix novo. Com --mux, refaz o MP4 com o vídeo COPIADO e o mix novo (AAC 192k, os mesmos
parâmetros do finish.py), confere que os pacotes de vídeo são idênticos e mede de novo.
uso: python3 -I pico_aac.py <aula_final.mp4> <mix.wav> <mix_novo.wav> [--so-medir] [--mux <aula_nova.mp4>] [--db 3]
  O mix.wav é o da aula (<out>/proj/build/mix.wav); sem ele (apagado depois da entrega), refaça-o antes com o remendar_aula.py.
  Depois do --mux: troque o arquivo à mão (ln -f ...: o aula_final.mp4 costuma ter hardlinks em entrega/), rode o entregar.py de novo
  e confira o pico real que ele mostra. Ajuste no mix.wav se perde num remendo (o remendar_aula.py refaz o mix do zero)."""
import hashlib
import json
import os
import subprocess
import sys

import numpy as np
import soundfile as sf
from scipy.signal import resample_poly

argv = sys.argv[1:]
if len(argv) < 3 or "--help" in argv:
    sys.exit(__doc__)
mp4, mixwav, novo = argv[:3]
opt = lambda k, d=None: argv[argv.index(k) + 1] if k in argv else d  # noqa: E731
LIM = 10 ** (-1.0 / 20)
ALVO = 10 ** (-float(opt("--db", 3)) / 20)
CTX = 256  # amostras de folga de cada lado do bloco (o filtro do resample_poly não "vê" além da borda)


def picos(path_mp4):
    """[(t, dBTP)] do maior pico de cada segundo que passa de -1 dBTP (áudio decodificado do MP4, em streaming)"""
    info = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=sample_rate,channels",
                                      "-of", "json", path_mp4], capture_output=True, text=True, check=True).stdout)["streams"][0]
    sr, ch = int(info["sample_rate"]), int(info["channels"])
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", path_mp4, "-map", "0:a:0", "-f", "f32le", "-acodec", "pcm_f32le", "-"],
                         stdout=subprocess.PIPE)
    ler = lambda: np.frombuffer(p.stdout.read(sr * ch * 4) or b"", np.float32).reshape(-1, ch)  # noqa: E731
    hits, i0, ant, cur = [], 0, np.zeros((0, ch), np.float32), ler()
    while len(cur):
        prox = ler()
        x = np.concatenate([ant[-CTX:], cur, prox[:CTX]])
        a = np.abs(resample_poly(x, 4, 1, axis=0)).max(axis=1)
        n0 = min(CTX, len(ant)) * 4
        meio = a[n0:n0 + len(cur) * 4]
        pk = float(meio.max())
        if pk > LIM:
            hits.append((round(float(i0 + meio.argmax() / 4) / sr, 3), round(float(20 * np.log10(pk)), 2)))
        i0 += len(cur)
        ant, cur = cur, prox
    if p.wait() != 0:
        sys.exit(f"ffmpeg não decodificou o áudio de {path_mp4}")
    return hits


def md5_video(path):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-map", "0:v:0", "-c", "copy", "-f", "md5", "-"], capture_output=True, text=True)
    return r.stdout.strip()


hits = picos(mp4)
print("picos acima de -1 dBTP no MP4:", hits or "nenhum")
if "--so-medir" in argv or not hits:
    sys.exit(0)

# ganho: 1 fora dos trechos; ALVO em +-65 ms em volta de cada pico, com rampas de 20 ms (mix.wav lido e escrito em blocos)
with sf.SoundFile(mixwav) as fi:
    srm, nch, total = fi.samplerate, fi.channels, fi.frames
    meia, rampa = int(0.065 * srm), int(0.020 * srm)
    janelas = []
    for t, _ in hits:
        c = int(t * srm)
        janelas.append((max(0, c - meia), min(total, c + meia)))
    tmp = novo + ".tmp.wav"
    with sf.SoundFile(tmp, "w", srm, nch, "FLOAT", format="WAV") as fo:
        pos, bloco = 0, srm * 10
        while pos < total:
            x = fi.read(min(bloco, total - pos), dtype="float32", always_2d=True)
            g = np.ones(len(x), np.float32)
            for a, b in janelas:
                if b <= pos or a >= pos + len(x):
                    continue
                env = np.full(b - a, ALVO, np.float32)
                r = min(rampa, (b - a) // 2)
                env[:r] = np.linspace(1.0, ALVO, r)
                env[-r:] = np.linspace(ALVO, 1.0, r)
                s0, s1 = max(a, pos), min(b, pos + len(x))
                g[s0 - pos:s1 - pos] = np.minimum(g[s0 - pos:s1 - pos], env[s0 - a:s1 - a])
            fo.write(x * g[:, None])
            pos += len(x)
os.replace(tmp, novo)
print(f"mix novo: {novo} ({len(hits)} trecho(s) a -{opt('--db', 3)} dB)")

saida = opt("--mux")
if saida:
    tmp = saida + ".tmp.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp4, "-i", novo, "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac",
                    "-b:a", "192k", "-ar", "48000", "-ac", "2", "-shortest", "-movflags", "+faststart", "-f", "mp4", tmp], check=True)
    a, b = md5_video(mp4), md5_video(tmp)
    if a != b:
        os.remove(tmp)
        sys.exit(f"os pacotes de vídeo mudaram ({a} -> {b}): nada foi gravado")
    os.replace(tmp, saida)
    depois = picos(saida)
    print(f"{saida}: vídeo idêntico (md5 {hashlib.md5(a.encode()).hexdigest()[:8]}); picos acima de -1 dBTP agora: {depois or 'nenhum'}")
