"""Kit de síntese (numpy/scipy, 48 kHz, estéreo): trilha e SFX 100% originais para demo reels."""
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve, lfilter, resample_poly

SR = 48000
RNG = np.random.default_rng(7)
mtof = lambda m: 440.0 * 2 ** ((np.asarray(m, float) - 69) / 12)
tvec = lambda d: np.arange(int(round(d * SR))) / SR
noise = lambda n, rng=None: (rng or RNG).standard_normal(n)


def filt(x, kind, f, order=2):
    if kind == "bp":
        s = butter(order, [f[0] / (SR / 2), f[1] / (SR / 2)], "bandpass", output="sos")
    else:
        s = butter(order, f / (SR / 2), {"lp": "lowpass", "hp": "highpass"}[kind], output="sos")
    return sosfilt(s, x, axis=0)


def pan_st(x, p=0.0):
    return np.stack([x * np.cos((p + 1) * np.pi / 4) * 1.4142, x * np.sin((p + 1) * np.pi / 4) * 1.4142], 1)


def fade(y, a_ms=1.5, r_ms=8):
    a, r = max(1, int(a_ms * SR / 1000)), max(1, int(r_ms * SR / 1000))
    y = y.copy(); y[:a] *= np.linspace(0, 1, a) ** 2; y[-r:] *= np.linspace(1, 0, r) ** 2
    return y


class Bus:
    def __init__(self, dur, tail=4.0):
        self.x = np.zeros((int(round((dur + tail) * SR)), 2))

    def add(self, sig, t, gain=1.0, pan=0.0):
        if sig.ndim == 1: sig = pan_st(sig, pan)
        i0 = int(round(t * SR))
        if i0 < 0: sig, i0 = sig[-i0:], 0
        i1 = min(len(self.x), i0 + len(sig))
        if i1 > i0: self.x[i0:i1] += sig[: i1 - i0] * gain


def adsr(n, a, d, s, r, hold):
    t = np.arange(n) / SR
    e = np.where(t < a, t / max(a, 1e-6), 1 - (1 - s) * np.clip((t - a) / max(d, 1e-6), 0, 1))
    return e * (1 - np.clip((t - hold) / max(r, 1e-6), 0, 1)) ** 1.6


def saw(freq, n, ph0=0.0):  # dente de serra anti-aliasing (polyBLEP)
    f = np.full(n, float(freq)) if np.ndim(freq) == 0 else np.asarray(freq, float)
    dt = f / SR; ph = (ph0 + np.cumsum(dt)) % 1.0; y = 2 * ph - 1
    m1 = ph < dt; t1 = ph[m1] / dt[m1]; y[m1] -= t1 + t1 - t1 * t1 - 1
    m2 = ph > 1 - dt; t2 = (ph[m2] - 1) / dt[m2]; y[m2] -= t2 * t2 + t2 + t2 + 1
    return y


# ------------------------------------------------------------------ instrumentos
def pad(notes, dur, vel=0.1, cutoff=1600, attack=0.5, release=0.8, detune=9, voices=5, seed=0):
    rng = np.random.default_rng(seed); n = int(round((dur + release) * SR)); out = np.zeros((n, 2))
    for m in notes:
        f0 = float(mtof(m))
        for v in range(voices):
            c = (v - (voices - 1) / 2) / ((voices - 1) / 2) * detune + rng.uniform(-1.5, 1.5)
            vib = 1 + 0.0018 * np.sin(2 * np.pi * rng.uniform(4, 6) * np.arange(n) / SR + rng.uniform(0, 6.3))
            out += pan_st(saw(f0 * 2 ** (c / 1200) * vib, n, rng.uniform()), (v / (voices - 1) * 2 - 1) * 0.7) / voices
    out = filt(out / max(1, len(notes)) ** 0.7, "lp", cutoff, 4)
    return out * adsr(n, attack, 0.5, 0.85, release, dur)[:, None] * vel


def pluck(m, dur=0.22, vel=0.05, cutoff=3000):
    f = float(mtof(m)); n = int(round(dur * SR)); t = np.arange(n) / SR
    y = filt(0.6 * saw(f, n) + 0.2 * np.sign(np.sin(2 * np.pi * f * t)), "lp", cutoff)
    return y * np.exp(-t * 7) * (1 - np.exp(-t * 1500)) * vel


def epiano(m, dur=0.6, vel=0.06, bright=0.5):
    f = float(mtof(m)); n = int(round((dur + 1.2) * SR)); t = np.arange(n) / SR
    idx = (1.1 + 1.4 * vel * bright) * np.exp(-t * 2.8) + 0.12
    y = np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * f * t)) * np.exp(-t * (0.9 + f / 1400)) * (1 - np.exp(-t * 600))
    return y * (1 - np.clip((t - dur) / 0.35, 0, 1)) ** 2 * vel


def sub(m, dur, vel=0.2, attack=0.01, release=0.15):
    f = float(mtof(m)); n = int(round((dur + release) * SR)); t = np.arange(n) / SR
    return np.tanh(np.sin(2 * np.pi * f * t) * 1.75) / np.tanh(1.75) * adsr(n, attack, 0.1, 0.9, release, dur) * vel


def kick(vel=0.36, tone=50, decay=10):
    t = tvec(0.6); f = tone + 120 * np.exp(-t * 32) + 30 * np.exp(-t * 8)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * decay) + 0.25 * filt(noise(len(t)), "hp", 2500) * np.exp(-t * 350)
    return np.tanh(y * 1.4) * vel


def snap(vel=0.08):
    t = tvec(0.3); b = sum(np.exp(-np.clip(t - d, 0, None) * 180) * (t >= d) for d in (0, 0.011, 0.023))
    return filt(noise(len(t)), "bp", (900, 3200)) * (b * 0.6 + np.exp(-t * 14) * 0.5 * (t >= 0.023)) * vel


def shaker(vel=0.035):
    t = tvec(0.09); return filt(noise(len(t)), "bp", (5000, 11000)) * np.sin(np.pi * np.clip(t / 0.07, 0, 1)) ** 2 * vel


def hat(vel=0.022):
    t = tvec(0.08); return filt(noise(len(t)), "hp", 7500) * np.exp(-t * 70) * vel


def sweep(dur, f0, f1, q=1.2, shape="whoosh", seed=5, move=0.0):
    """ruído com uma banda que varre f0->f1 (base de whooshes/risers)."""
    rng = np.random.default_rng(seed); n = int(round(dur * SR)); t = np.arange(n) / SR; nz = noise(n, rng)
    cs = np.geomspace(150, 12000, 18)
    bands = np.array([filt(nz, "bp", (c / (1 + q / 2), min(c * (1 + q / 2), SR / 2 - 100))) for c in cs])
    fc = np.exp(np.log(f0) + (np.log(f1) - np.log(f0)) * t / dur)
    y = (bands * np.exp(-((np.log(cs)[:, None] - np.log(fc)[None]) ** 2) / (2 * 0.35 ** 2))).sum(0)
    e = {"rise": (t / dur) ** 2.2, "fall": (1 - t / dur) ** 2}.get(shape, np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 1.5)
    y = y * e / (np.abs(y).max() + 1e-9)
    if move:
        p = np.clip(-move + 2 * move * t / dur, -1, 1)
        return np.stack([y * np.cos((p + 1) * np.pi / 4) * 1.4142, y * np.sin((p + 1) * np.pi / 4) * 1.4142], 1)
    return pan_st(y)


def riser(dur=1.2, vel=0.1, f0=300, f1=8000, seed=9):
    y = sweep(dur, f0, f1, 1.2, "rise", seed); t = tvec(dur)
    y[:, 0] += 0.18 * np.sin(2 * np.pi * np.cumsum(180 * 2 ** (2.5 * (t / dur) ** 1.4)) / SR) * (t / dur) ** 2
    y[:, 1] = y[:, 0]
    return y * vel


# ------------------------------------------------------------------ SFX (estilo Apple/SaaS: ataques arredondados, caudas curtas)
def glass(m, dur=1.0, vel=0.3, ratio=2.0, index=0.9, decay=3.5):
    f = float(mtof(m)); t = tvec(dur)
    y = np.sin(2 * np.pi * f * t + index * np.exp(-t * 6) * np.sin(2 * np.pi * ratio * f * t)) + 0.18 * np.sin(2 * np.pi * 4.07 * f * t) * np.exp(-t * 14)
    return fade(y * np.exp(-t * decay) * (1 - np.exp(-t * 2200)) * vel, 2.5, 30)


def click(vel=0.5, seed=0):  # trackpad
    rng = np.random.default_rng(seed); t = tvec(0.07)
    y = filt(noise(len(t), rng), "bp", (1400, 5200)) * np.exp(-t * 1500) * 0.8 + 0.22 * np.sin(2 * np.pi * 2100 * t) * np.exp(-t * 260)
    y += 0.35 * np.sin(2 * np.pi * 170 * t) * np.exp(-t * 95) * (1 - np.exp(-t * 3000))
    return fade(filt(y, "lp", 9000) * vel, 0.6, 8)


def key(vel=0.4, seed=0):
    rng = np.random.default_rng(seed); b = rng.uniform(0.85, 1.15); t = tvec(0.045)
    y = filt(noise(len(t), rng), "bp", (2200 * b, 7000 * b)) * np.exp(-t * 1900) + 0.16 * np.sin(2 * np.pi * 1150 * b * t) * np.exp(-t * 420)
    return fade(filt(y + 0.18 * np.sin(2 * np.pi * 260 * t) * np.exp(-t * 160), "lp", 9500) * vel, 0.4, 6)


def tick(vel=0.12, f=3000):
    t = tvec(0.05)
    return fade((np.sin(2 * np.pi * f * t) * np.exp(-t * 240) + 0.4 * filt(noise(len(t)), "bp", (2500, 8000)) * np.exp(-t * 1500)) * vel, 0.5, 6)


def pop(m=76, vel=0.4):
    f = float(mtof(m)); t = tvec(0.16); ph = 2 * np.pi * np.cumsum(f * (0.72 + 0.28 * (1 - np.exp(-t * 110)))) / SR
    y = (np.sin(ph) + 0.12 * np.sin(2 * ph)) * np.exp(-t * 26) * (1 - np.exp(-t * 2000)) + 0.12 * filt(noise(len(t)), "bp", (900, 3000)) * np.exp(-t * 700)
    return fade(y * vel, 1, 20)


def whoosh(dur=0.36, f0=900, f1=3600, vel=0.4, move=0.3, seed=1):
    y = filt(filt(sweep(dur, f0, f1, 1.5, "whoosh", seed, move), "lp", 9000), "hp", 160)
    return y / (np.abs(y).max() + 1e-9) * vel


def whoosh_big(vel=0.8, seed=8):  # transição grande (virada / cartela)
    a = whoosh(0.7, 250, 3200, 1.0, 0.0, seed); b = bloom(0.6, 1.6)
    out = np.zeros((max(len(a), len(b)), 2)); out[:len(a)] += a; out[:len(b)] += b
    return out * vel


def bloom(vel=0.6, dur=2.0, f=(62, 44)):  # "whoom" grave de revelação
    t = tvec(dur); ff = f[1] + (f[0] - f[1]) * np.exp(-t * 3)
    y = np.sin(2 * np.pi * np.cumsum(ff) / SR) * 0.9 + filt(noise(len(t)), "lp", 700) * np.exp(-t * 5) * 0.25
    return pan_st(fade(y * (1 - np.exp(-t * 14)) * np.exp(-t * 1.9) * vel, 3, 60))


def success(vel=0.5):
    out = np.zeros((int(0.8 * SR), 2))
    for k, m in enumerate((78, 81)):
        g = glass(m, 0.6, 1.0, index=0.8, decay=6); i = int(k * 0.07 * SR); out[i:i + len(g)] += pan_st(g, 0.1 * (2 * k - 1))
    return out * vel


def thock(vel=0.5):  # cartão pousando
    t = tvec(0.22); f = 105 + 150 * np.exp(-t * 60)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 20) * (1 - np.exp(-t * 2500)) + 0.35 * filt(noise(len(t)), "bp", (1500, 5000)) * np.exp(-t * 1200)
    return pan_st(fade(y * vel, 0.8, 30))


def sting(vel=0.5):  # assinatura da cartela
    out = np.zeros((int(3.6 * SR), 2))
    for k, (m, p) in enumerate(((74, -0.2), (78, 0.2), (81, -0.05), (86, 0.1))):
        g = glass(m, 2.6, 0.7 - 0.1 * k, index=0.8, decay=1.3); i = int(k * 0.09 * SR); out[i:i + len(g)] += pan_st(g, p)
    b = bloom(1.0, 2.6, (58, 41)); out[:len(b)] += b * 0.6
    return out * vel


def gliss(vel=0.2, dur=0.6):  # traço/linha desenhando
    t = tvec(dur); f = 880 * 2 ** ((t / dur) ** 0.8); w = np.sin(np.pi * np.clip(t / dur, 0, 1))
    return pan_st(fade((np.sin(2 * np.pi * np.cumsum(f) / SR) * w ** 1.2 + 0.3 * np.sin(2 * np.pi * np.cumsum(1.5 * f) / SR) * w ** 2) * vel, 5, 40))


def buzz(vel=0.3, dur=0.36, seed=0):  # celular vibrando na mesa
    rng = np.random.default_rng(seed); t = tvec(dur); ph = 2 * np.pi * np.cumsum(165 + 6 * np.sin(2 * np.pi * 9 * t)) / SR
    y = filt(np.tanh(3 * np.sin(ph)) * 0.6 + 0.25 * np.sin(2 * ph), "lp", 2400) * 0.8
    y += filt(noise(len(t), rng), "bp", (1800, 4200)) * (0.5 + 0.5 * np.sign(np.sin(ph))) * 0.22
    y = filt(y * np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 0.35, "hp", 90)
    return pan_st(fade(y / (np.abs(y).max() + 1e-9) * vel, 4, 25))


def paper(vel=0.5, seed=3):  # papel batendo
    rng = np.random.default_rng(seed); t = tvec(0.28)
    y = filt(noise(len(t), rng), "bp", (500, 6000)) * np.exp(-t * 55) * 0.7 + np.sin(2 * np.pi * (95 + 60 * np.exp(-t * 40)) * t) * np.exp(-t * 28) * 0.8
    return pan_st(fade(y / (np.abs(y).max() + 1e-9) * vel, 1, 30), 0.2)


def scribble(vel=0.35, dur=0.7, seed=5):  # caneta riscando
    rng = np.random.default_rng(seed); t = tvec(dur); st = np.zeros_like(t); k = 0.0
    while k < dur:
        L = rng.uniform(0.05, 0.12); i0, i1 = int(k * SR), min(len(t), int((k + L) * SR))
        if i1 > i0: st[i0:i1] = np.sin(np.pi * np.linspace(0, 1, i1 - i0)) * rng.uniform(0.6, 1)
        k += L + rng.uniform(0, 0.03)
    y = (filt(noise(len(t), rng), "bp", (2200, 7000)) + 0.35 * filt(noise(len(t), rng), "bp", (700, 1800))) * st
    return pan_st(fade(y / (np.abs(y).max() + 1e-9) * vel, 3, 30), -0.2)


def ping(vel=0.5):  # localização no mapa
    g = glass(86, 1.2, 1.0, index=0.6, decay=3.5); t = tvec(0.9)
    s = np.sin(2 * np.pi * (1500 - 500 * t / 0.9) * t) * np.exp(-t * 7) * 0.25
    y = np.zeros(len(g)); y[:len(s)] += s; y += g
    return pan_st(y * vel, 0.1)


# ------------------------------------------------------------------ processamento
def make_ir(dur=2.4, pre=0.02, seed=31, damp=0.55):
    rng = np.random.default_rng(seed); n = int(dur * SR); t = np.arange(n) / SR; out = np.zeros((n + int(pre * SR), 2))
    for ch in range(2):
        nz = rng.standard_normal(n)
        out[int(pre * SR):, ch] = damp * filt(nz, "lp", 2600) * np.exp(-t * 6.9 / dur) + (1 - damp) * nz * np.exp(-t * 6.9 / (dur * 0.45))
    return out / np.sqrt((out ** 2).sum(0)).max()


def reverb(x, ir):
    return np.stack([fftconvolve(x[:, c], ir[:, c])[: len(x)] for c in (0, 1)], 1)


def compress(x, thr=-22, ratio=2.5, att=0.006, rel=0.12, makeup=0.0, knee=6.0):
    m = np.sqrt((x ** 2).mean(1)) if x.ndim == 2 else np.abs(x)
    aa, ar = np.exp(-1 / (att * SR)), np.exp(-1 / (rel * SR))
    lv = np.maximum(lfilter([1 - aa], [1, -aa], m), lfilter([1 - ar], [1, -ar], m))
    o = 20 * np.log10(lv + 1e-9) - thr
    gr = np.where(o <= -knee / 2, 0, np.where(o >= knee / 2, o * (1 - 1 / ratio), (1 - 1 / ratio) * (o + knee / 2) ** 2 / (2 * knee)))
    g = 10 ** ((-gr + makeup) / 20)
    return x * (g[:, None] if x.ndim == 2 else g)


def peaking(x, f0, gdb, q=1.0):
    A = 10 ** (gdb / 40); w = 2 * np.pi * f0 / SR; al = np.sin(w) / (2 * q)
    b = np.array([1 + al * A, -2 * np.cos(w), 1 - al * A]); a = np.array([1 + al / A, -2 * np.cos(w), 1 - al / A])
    return lfilter(b / a[0], a / a[0], x, axis=0)


def true_peak(x, CH=10 * SR, PAD=256):
    """pico real com 4x de sobreamostragem, em blocos de 10 s (a aula inteira de uma vez passava de 4 GB)."""
    st = x if x.ndim == 2 else x[:, None]
    n = len(st); best = 0.0
    for i0 in range(0, n, CH):
        i1 = min(n, i0 + CH); a0, b0 = max(0, i0 - PAD), min(n, i1 + PAD)
        up = np.abs(resample_poly(st[a0:b0], 4, 1, axis=0))[(i0 - a0) * 4:(i1 - a0) * 4]
        if up.size: best = max(best, float(up.max()))
    return best


def limit(x, ceiling_db=-1.0, look_ms=1.5, rel_ms=80, inplace=False):
    """limitador por pico (4x oversampling), mono ou estéreo."""
    from scipy.ndimage import minimum_filter1d, uniform_filter1d
    st = x if x.ndim == 2 else x[:, None]
    # pico com 4x de sobreamostragem, em blocos de 10 s (o sinal inteiro de uma aula de 12 min passava de 4 GB)
    n = len(st); pk = np.zeros(n); CH, PAD = 10 * SR, 256
    for i0 in range(0, n, CH):
        i1 = min(n, i0 + CH); a0, b0 = max(0, i0 - PAD), min(n, i1 + PAD)
        up = np.abs(resample_poly(st[a0:b0], 4, 1, axis=0)).max(1); up = up[: (len(up) // 4) * 4].reshape(-1, 4).max(1)
        up = np.concatenate([up, np.zeros(max(0, (b0 - a0) - len(up)))]); pk[i0:i1] = up[i0 - a0:i1 - a0]
    W = max(1, int(look_ms * SR / 1000))
    np.maximum(pk, 1e-12, out=pk); np.divide(10 ** (ceiling_db / 20), pk, out=pk); np.minimum(pk, 1.0, out=pk)
    g = minimum_filter1d(pk, 2 * W + 1); del pk; g = uniform_filter1d(g, W + 1)
    # soltura em blocos de 10 s (tolist() da aula inteira criava 36 milhões de floats Python, ~1,2 GB)
    r = np.exp(-1 / (rel_ms * SR / 1000)); out = g; cur = 1.0
    for j0 in range(0, len(g), CH):
        res = []
        for gi in g[j0:j0 + CH].tolist():
            cur = gi if gi < cur else gi + (cur - gi) * r; res.append(cur)
        out[j0:j0 + len(res)] = res
    if inplace:
        st *= out[:, None]
        return x
    return st * out[:, None] if x.ndim == 2 else x * out
