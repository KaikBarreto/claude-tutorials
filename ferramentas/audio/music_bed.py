"""Trilha de fundo para aulas (lo-fi leve, Ré maior, ~82 BPM) com instrumentos SoundFont.
Gera blocos de 8 compassos (A, B, A sem bateria, B com melodia) e os encadeia até a duração pedida,
com um acorde final ("button") no ponto `end_at`.
uso: python3 audio/music_bed.py <dur_s> <saida.wav> [--end-at S] [--seed N] [--bpm 82]"""
import argparse, os, sys
import numpy as np, soundfile as sf
from scipy.signal import fftconvolve

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from kit import filt, limit, make_ir, reverb, SR  # noqa
from sfsynth import Part

ap = argparse.ArgumentParser()
ap.add_argument("dur", type=float); ap.add_argument("out")
ap.add_argument("--end-at", type=float, default=None); ap.add_argument("--seed", type=int, default=3)
ap.add_argument("--bpm", type=float, default=82)
a = ap.parse_args()
BEAT = 60 / a.bpm; BAR = 4 * BEAT; SW = 0.58  # swing das colcheias
rng = np.random.default_rng(a.seed)
hum = lambda s=0.008: rng.normal(0, s)
sw8 = lambda i: (i // 2) * BEAT + (SW * BEAT if i % 2 else 0.0)  # i-ésima colcheia com swing

# acordes: (baixo, voicing sem fundamental p/ o piano elétrico, pad)
CH = {
    "Dmaj9": (38, [54, 57, 61, 64], [50, 57, 61, 64]),
    "Bm9": (35, [50, 54, 57, 61], [47, 54, 57, 62]),
    "Gmaj9": (31, [54, 57, 59, 62], [43, 50, 54, 57]),
    "A13s": (33, [55, 59, 62, 66], [45, 52, 55, 59]),
    "Em9": (40, [50, 54, 55, 59], [40, 47, 50, 54]),
    "F#m7": (42, [52, 57, 61, 64], [42, 49, 52, 57]),
}
PROG = {"A": ["Dmaj9", "Bm9", "Gmaj9", "A13s"] * 2, "B": ["Em9", "F#m7", "Gmaj9", "A13s"] * 2}
MOTIF = [(0.0, 0.5, 78), (0.5, 0.5, 76), (1.0, 1.5, 73), (3.0, 1.0, 71)]  # vibrafone, bem esparso


def block(kind, drums=True, melody=False, intro=False):
    L = 8 * BAR; tail = 3.0
    ep, bass, pad, kit, vib = Part(4, gain_db=-3), Part(33, gain_db=-2), Part(89, gain_db=-8), Part(0, drums=True, gain_db=-5), Part(11, gain_db=-9)
    for b, name in enumerate(PROG[kind]):
        t0 = b * BAR; root, ev, pv = CH[name]
        pad.chord(t0, BAR + 0.05, pv, vel=48)
        if intro and b < 2:
            ep.chord(t0 + hum(), BAR * 0.95, ev, vel=52, strum=0.03); continue
        # piano elétrico: 1, "e" do 2, às vezes 4
        ep.chord(t0 + hum(), 1.4 * BEAT, ev, vel=int(60 + rng.integers(-6, 7)), strum=0.012)
        ep.chord(t0 + sw8(3) + hum(), 0.9 * BEAT, ev[1:] if b % 2 else ev, vel=int(48 + rng.integers(-6, 7)), strum=0.01)
        if b % 4 == 3: ep.chord(t0 + 3 * BEAT + hum(), 0.6 * BEAT, ev, vel=44)
        # baixo
        bass.note(t0 + hum(0.004), 1.5 * BEAT, root, 84)
        bass.note(t0 + 2 * BEAT + hum(0.004), 0.9 * BEAT, root + 7 if root + 7 < 48 else root - 5, 70)
        nxt = CH[PROG[kind][(b + 1) % 8]][0]
        if b % 2 == 1: bass.note(t0 + sw8(7), 0.4 * BEAT, nxt + (1 if nxt < root else -1), 62)
        if drums:
            for i in range(8):  # hats com swing
                kit.note(t0 + sw8(i) + hum(0.004), 0.1, 42, int((50 if i % 2 == 0 else 34) + rng.integers(-5, 6)))
            kit.note(t0 + hum(0.003), 0.2, 36, 92)
            kit.note(t0 + sw8(5) + hum(0.003), 0.2, 36, 64 if b % 2 else 0)
            for bb in (1, 3): kit.note(t0 + bb * BEAT + 0.012 + hum(0.004), 0.2, 37, 70)  # aro (rim) no 2 e 4
            if b % 4 == 3: kit.note(t0 + sw8(7), 0.3, 46, 34)
        if melody and b % 2 == 0:
            for (bt, d, m) in MOTIF if b % 4 == 0 else MOTIF[:2] + [(1.0, 2.0, 74)]:
                vib.note(t0 + bt * BEAT + hum(), d * BEAT, m, 54)
    T = L + tail
    stems = [ep.render(T) * 0.9, bass.render(T) * 0.8, pad.render(T) * 0.5, vib.render(T) * 0.55]
    if drums: stems.append(kit.render(T) * 0.55)
    y = sum(stems)
    return y, L


plan_blocks = [("A", dict(intro=True, drums=False)), ("A", {}), ("B", dict(melody=True)), ("A", dict(drums=False)),
               ("B", {}), ("A", dict(melody=True)), ("B", dict(drums=False, melody=True)), ("A", {})]
cache = {}
end_at = a.end_at if a.end_at is not None else max(0.0, a.dur - 3 * BAR)
total = int(round((a.dur + 4.0) * SR)); out = np.zeros((total, 2))
t = 0.0; k = 0
while t < end_at - 0.01:
    kind, kw = plan_blocks[k if k < len(plan_blocks) else 1 + (k - 1) % (len(plan_blocks) - 1)]
    key = (kind, tuple(sorted(kw.items())))
    if key not in cache: cache[key] = block(kind, **kw)
    y, L = cache[key]
    i0 = int(round(t * SR)); i1 = min(total, i0 + len(y)); out[i0:i1] += y[: i1 - i0]
    t += L; k += 1
# corta no fim do conteúdo (fade de 1,2 s) e toca o acorde final
ie = int(round(end_at * SR)); f = int(1.2 * SR)
out[max(0, ie - f):ie] *= np.linspace(1, 0, min(f, ie))[:, None] ** 1.5; out[ie:] = 0
fin_ep, fin_pad, fin_bass, fin_vib = Part(4, gain_db=-3), Part(89, gain_db=-8), Part(33, gain_db=-2), Part(11, gain_db=-9)
fin_ep.chord(0.0, 2.6, [54, 57, 61, 64, 69], vel=58, strum=0.04); fin_pad.chord(0.0, 2.8, [50, 57, 61, 64], vel=52)
fin_bass.note(0.0, 2.6, 38, 80); [fin_vib.note(0.25 + 0.18 * j, 1.5, m, 50) for j, m in enumerate((78, 81, 85))]
F = fin_ep.render(6) * 0.9 + fin_pad.render(6) * 0.5 + fin_bass.render(6) * 0.8 + fin_vib.render(6) * 0.5
i1 = min(total, ie + len(F)); out[ie:i1] += F[: i1 - ie]
# cor lo-fi: passa-baixa suave + saturação leve + chiado de vinil discreto + reverb curto
out = filt(out, "lp", 7200, 2); out *= 1.6; np.tanh(out, out=out); out /= 1.6  # no lugar (memória)
# (memória: aulas longas, 10+ min, estouravam ~4 GB; chiado, estalos e reverb agora por blocos de 30 s)
CH = 30 * SR
idx = rng.integers(0, total, int(a.dur * 1.6)); lado = rng.integers(0, 2, len(idx)); amp = rng.uniform(0.002, 0.008, len(idx))
for i0 in range(0, total, CH):
    n_ = min(CH, total - i0)
    out[i0:i0 + n_] += filt(rng.standard_normal((n_, 2)), "bp", (1500, 7000)) * 10 ** (-58 / 20)
    sel = (idx >= i0) & (idx < i0 + n_)
    if sel.any():
        ck = np.zeros((n_, 2)); ck[idx[sel] - i0, lado[sel]] = amp[sel]; out[i0:i0 + n_] += filt(ck, "hp", 1200)
ir = make_ir(1.6, 0.012, 21, 0.6); rv = np.zeros_like(out)
for i0 in range(0, total, CH):
    seg = out[i0:i0 + CH]
    for c in (0, 1):
        r = fftconvolve(seg[:, c], ir[:, c]); j1 = min(total, i0 + len(r)); rv[i0:j1, c] += r[: j1 - i0]
rv *= 0.18; out += rv; del rv
out = out[: int(round(a.dur * SR))]
import pyloudnorm as pyln
lufs = pyln.Meter(SR).integrated_loudness(out); out = out * 10 ** ((-20.0 - lufs) / 20); out = limit(out, -2.0)
sf.write(a.out, out.astype(np.float32), SR, subtype="FLOAT")
print(f"trilha {a.dur:.1f}s ({len(cache)} blocos únicos, bloco={8*BAR:.1f}s) -> {a.out}  {pyln.Meter(SR).integrated_loudness(out):.1f} LUFS")
