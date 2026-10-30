"""Áudio final da aula: voz editada pela EDL (tratada) + trilha com ducking + som da vinheta e da cartela + SFX discretos.
uso: python3 kit/mix.py <projeto>   (rode depois do plan.py; usa build/intro_audio.wav e build/outro_audio.wav se existirem)
saída: build/mix.wav (48 kHz estéreo) + build/stems/
Memória: uma aula de 12 min tem 35 milhões de amostras (288 MB por canal em float64). Tudo é feito no lugar e cada
sinal é liberado assim que deixa de ser usado; gravação e medições em blocos de 10 s (limite da máquina ~4 GB)."""
import json, os, subprocess, sys
import numpy as np, soundfile as sf
from scipy.signal import stft, istft, lfilter

KIT = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(KIT)
sys.path.insert(0, os.path.join(ROOT, "audio")); sys.path.insert(0, KIT)
from kit import filt, compress, peaking, limit, true_peak, pan_st, whoosh, pop, tick, glass, Bus, SR  # noqa
import pyloudnorm as pyln

proj = os.path.abspath(sys.argv[1]); P = lambda *a: os.path.join(proj, *a)
cfg = json.load(open(P("render.json"))) if os.path.exists(P("render.json")) else {}
edl = json.load(open(P("edl.json"))); SEGS = edl["segments"]; CDUR = edl["out_dur"]
dur_of = lambda f: sf.info(f).duration if f.endswith(".wav") else float(subprocess.run(
    ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout or 0)
T_IN = dur_of(P("build", "intro_v.mp4")) if os.path.exists(P("build", "intro_v.mp4")) else 0.0
T_OUT = dur_of(P("build", "outro_v.mp4")) if os.path.exists(P("build", "outro_v.mp4")) else 0.0
XF_OUT = 0.5 if T_OUT else 0.0
OUT_START = T_IN + CDUR - XF_OUT; TOTAL = OUT_START + T_OUT if T_OUT else T_IN + CDUR
N = int(round(TOTAL * SR)); meter = pyln.Meter(SR); BLK = 10 * SR
os.makedirs(P("build", "stems"), exist_ok=True)


def write_st(path, a):
    """grava estéreo float32 em blocos (mono vira os dois canais iguais), sem cópia do sinal inteiro."""
    with sf.SoundFile(path, "w", SR, 2, subtype="FLOAT") as f:
        for j in range(0, len(a), BLK):
            b = a[j:j + BLK]; f.write((b if b.ndim == 2 else np.stack([b, b], 1)).astype(np.float32))


# ------------------------------------------------------------------ voz
x, sr = sf.read(P("audio48k.wav"), dtype="float64"); assert sr == SR
x = filt(x, "hp", 80, 2)
noise_db = edl.get("noise_floor_db", -80)
if cfg.get("denoise", "auto") is True or (cfg.get("denoise", "auto") == "auto" and noise_db > -62):
    # redução de ruído espectral suave (perfil = trechos abaixo do limiar de fala)
    f, t, Z = stft(x, SR, nperseg=2048, noverlap=1536)
    mag = np.abs(Z); fr_db = 20 * np.log10(np.sqrt((mag ** 2).mean(0)) + 1e-12)
    quiet = fr_db < np.percentile(fr_db, 15) + 3
    prof = np.median(mag[:, quiet], axis=1, keepdims=True) if quiet.sum() > 10 else np.percentile(mag, 10, axis=1, keepdims=True)
    g = np.clip(1 - 1.6 * prof / (mag + 1e-12), 10 ** (-13 / 20), 1); del mag
    g = lfilter([0.35], [1, -0.65], g, axis=1)  # suaviza no tempo (menos "água")
    Z *= g; del g
    _, x = istft(Z, SR, nperseg=2048, noverlap=1536); del Z
    print(f"redução de ruído aplicada (piso {noise_db:.1f} dB)")
x = peaking(peaking(x, 220, -2.0, 0.9), 3500, 2.0, 0.8)
# de-esser: x - ss * (1 - clip(1 - (env - 0.02) * 10, 0.6, 1)), no lugar
ss = filt(x, "bp", (5200, 9500)); env = lfilter([0.01], [1, -0.99], np.abs(ss))
env -= 0.02; env *= -10.0; env += 1.0; np.clip(env, 0.6, 1, out=env); np.subtract(1.0, env, out=env)
ss *= env; del env; x -= ss; del ss
x = compress(x, -26, 2.8, 0.005, 0.14, 0.0)

voice = np.zeros(N); XF = int(0.012 * SR); win = np.sin(np.linspace(0, np.pi / 2, XF)) ** 2
for s in SEGS:
    if s["speed"] != 1: continue
    a, b = int(round(s["src_s"] * SR)), int(round(s["src_e"] * SR)); o = int(round((T_IN + s["out_s"]) * SR))
    a0 = max(0, a - XF // 2); o0 = o - (a - a0); chunk = x[a0:b + XF // 2].copy()
    chunk[:XF] *= win[: len(chunk[:XF])]; chunk[-XF:] *= win[::-1][-len(chunk[-XF:]):]
    o1 = min(N, o0 + len(chunk)); voice[o0:o1] += chunk[: o1 - o0]
del x
speech_mask = np.zeros(N, bool)
for s in SEGS:
    if s["kind"] == "fala": speech_mask[int((T_IN + s["out_s"]) * SR):int((T_IN + s["out_e"]) * SR)] = True
lv = meter.integrated_loudness(voice[speech_mask]) if speech_mask.sum() > SR else meter.integrated_loudness(voice)
voice *= 10 ** ((-15.5 - lv) / 20)
voice = limit(voice, -2.0, inplace=True)

# ------------------------------------------------------------------ trilha
mus_path = P("build", "music.wav")
if not os.path.exists(mus_path) or cfg.get("remake_music"):
    subprocess.run([sys.executable, os.path.join(ROOT, "audio", "music_bed.py"), f"{TOTAL - T_IN + 0.5:.2f}", mus_path,
                    "--end-at", f"{OUT_START - T_IN:.2f}", "--seed", str(cfg.get("music_seed", 3))], check=True)
m, _ = sf.read(mus_path, dtype="float64")
M = np.zeros((N, 2)); i0 = int(round((T_IN - 0.25) * SR)); n_ = min(N - i0, len(m)); M[i0:i0 + n_] = m[:n_]; del m
fi = int(1.2 * SR); M[i0:i0 + fi] *= np.linspace(0, 1, fi)[:, None] ** 2
# ducking: envelope da voz (ataque 40 ms, soltura 600 ms) relativo ao percentil 60 da fala
va = np.abs(voice); aa, ar = np.exp(-1 / (0.04 * SR)), np.exp(-1 / (0.6 * SR))
duck = lfilter([1 - aa], [1, -aa], va); np.maximum(duck, lfilter([1 - ar], [1, -ar], va), out=duck)
ref = np.percentile(va[speech_mask], 60) if speech_mask.any() else 0.05; del va
duck /= ref; np.clip(duck, 0, 1, out=duck)
fast = np.zeros(N)
for s in SEGS:
    if s["speed"] > 1: fast[int((T_IN + s["out_s"]) * SR):int((T_IN + s["out_e"]) * SR)] = 1
fast = lfilter([1 - np.exp(-1 / (0.3 * SR))], [1, -np.exp(-1 / (0.3 * SR))], fast)
base_db, duck_db = cfg.get("music_db", -7.0), cfg.get("music_duck_db", -8.0)
gdb = duck; gdb *= duck_db; gdb += base_db; fast *= 2.0; gdb += fast; del fast, duck  # base + duck_db*duck + 2*fast
gdb /= 20.0; np.power(10.0, gdb, out=gdb); M *= gdb[:, None]; del gdb

# ------------------------------------------------------------------ vinheta, cartela e SFX
FX = Bus(TOTAL, 0.5)
if os.path.exists(P("build", "intro_audio.wav")):
    ia, _ = sf.read(P("build", "intro_audio.wav"), dtype="float64"); FX.add(ia if ia.ndim == 2 else pan_st(ia), 0.0)
if T_OUT and os.path.exists(P("build", "outro_audio.wav")):
    oa, _ = sf.read(P("build", "outro_audio.wav"), dtype="float64"); FX.add(oa if oa.ndim == 2 else pan_st(oa), OUT_START)
G = lambda db: 10 ** (db / 20)
prev_fast = False
for s in SEGS:
    t = T_IN + s["out_s"]
    if s["speed"] > 1 and not prev_fast: FX.add(whoosh(0.22, 900, 4200, 1.0, 0.2, seed=int(t)), t - 0.06, G(-30))
    prev_fast = s["speed"] > 1
for ch in edl.get("chapters", []):
    t = T_IN + ch["t_out"]; FX.add(whoosh(0.4, 500, 2600, 1.0, -0.3, seed=7), t - 0.12, G(-27)); FX.add(pop(79, 1.0), t + 0.22, G(-31))
for sp in edl.get("spots", []):
    FX.add(pan_st(glass(86, 0.5, 1.0, index=0.5, decay=8)), T_IN + sp["s_out"], G(-33))
for co in edl.get("callouts", []):
    FX.add(pop(81, 1.0), T_IN + co["s_out"], G(-31))
for z in edl.get("zooms", []):
    FX.add(whoosh(0.5, 400, 1800, 1.0, 0.0, seed=11), T_IN + z["s_out"] - 0.35, G(-34))
S_ = FX.x[:N]

# ------------------------------------------------------------------ stems, medições e mix (tudo no lugar)
voice *= np.cos(np.pi / 4)  # = pan_st(voice) / 1.4142: a mesma voz nos dois canais
write_st(P("build", "stems", "voz.wav"), voice); write_st(P("build", "stems", "musica.wav"), M); write_st(P("build", "stems", "sfx.wav"), S_)
acc, cnt = 0.0, 0
for j in range(0, N, BLK):
    mk = speech_mask[j:j + BLK]
    if mk.any(): b = M[j:j + BLK][mk]; acc += float((b ** 2).sum()); cnt += b.size
mu_under = 20 * np.log10(np.sqrt(acc / cnt) + 1e-12) if cnt else 0
v_lufs = meter.integrated_loudness(voice) + 10 * np.log10(2)  # dois canais iguais = +3 dB
M += S_; del S_, FX
M[:, 0] += voice; M[:, 1] += voice; del voice
mix = limit(M, -1.0, inplace=True); del M
write_st(P("build", "mix.wav"), mix)
print(f"mix {TOTAL:.1f}s | {meter.integrated_loudness(mix):.1f} LUFS | TP {20*np.log10(true_peak(mix)):.1f} dBTP | "
      f"voz {v_lufs:.1f} LUFS | música sob a voz {mu_under:.1f} dBFS RMS")
