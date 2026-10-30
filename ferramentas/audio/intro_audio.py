"""Som da vinheta e da cartela (web/intro.html). Lê build/intro_meta.json (tempos exportados pela página) ->
build/intro_audio.wav (48 kHz estéreo).
- estilo "dominex-capacete" (cue "clank"): whooshes das peças, encaixe metálico + assinatura (Ré maior), brilho,
  título, saída. Igual ao T3.
- estilo "logo" (cue "land"): whoosh na entrada do logo e assinatura discreta no pouso (sino de vidro + grave suave +
  pad e piano elétrico em Ré maior), brilho, nome, título, saída. Não depende de peças."""
import json, os, sys
import numpy as np, soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from kit import *  # noqa
from sfsynth import Part

meta = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "build/intro_meta.json"))
out_path = sys.argv[2] if len(sys.argv) > 2 else "build/intro_audio.wav"
DUR = meta["duration"]; cue = {}
for c in meta["cues"]: cue.setdefault(c["id"], []).append(c)


def clank(vel=0.5, seed=3):
    """encaixe metálico discreto: transiente + parciais inarmônicas curtas + corpo grave"""
    rng = np.random.default_rng(seed); t = tvec(1.4); f0 = 330.0
    y = np.zeros(len(t))
    for r, a in ((1.0, 1.0), (1.593, .7), (2.136, .55), (2.296, .5), (2.653, .4), (3.156, .32), (3.501, .25), (4.152, .18)):
        y += a * np.sin(2 * np.pi * f0 * r * t + rng.uniform(0, 6.28)) * np.exp(-t * (7 + 4.5 * r))
    y = y / np.abs(y).max() * 0.55
    y += filt(noise(len(t), rng), "bp", (2200, 9000)) * np.exp(-t * 260) * 0.9
    body = np.sin(2 * np.pi * np.cumsum(95 + 140 * np.exp(-t * 55)) / SR) * np.exp(-t * 16) * 0.9
    return pan_st(fade((y + body) * vel, 0.3, 40))


def shimmer(vel=0.18):
    out = np.zeros((int(1.6 * SR), 2))
    for k, m in enumerate((86, 88, 90, 93, 95, 98)):
        g = glass(m, 1.1, 1.0 - 0.08 * k, ratio=3.0, index=0.5, decay=4.5); i = int(k * 0.045 * SR)
        out[i:i + len(g)] += pan_st(g, -0.5 + 0.2 * k)
    return out * vel


fx, verb_send, mus = Bus(DUR, 2.0), Bus(DUR, 2.0), Bus(DUR, 2.0)
if "clank" in cue:  # ------------------------------------------------ "dominex-capacete" (não mexer: padrão do T3)
    T_CLANK = cue["clank"][0]["t"]
    # 1) respiro inicial subindo até o encaixe
    r = riser(T_CLANK - 0.05, 0.08, 250, 5200, 11); fx.add(r, 0.05); verb_send.add(r, 0.05, 0.6)
    for k, c in enumerate(cue.get("whoosh", [])):
        y = whoosh(0.42, 700 + 250 * k, 3400, 0.30, move=0.35 * (c.get("pan", 0) or (k - 1)), seed=20 + k)
        fx.add(y, c["t"] - 0.12); verb_send.add(y, c["t"] - 0.12, 0.3)
    # 2) encaixe + assinatura
    fx.add(clank(0.55), T_CLANK); verb_send.add(clank(0.55), T_CLANK, 0.35)
    fx.add(bloom(0.55, 2.4, (60, 42)), T_CLANK)
    st = sting(0.42); fx.add(st, T_CLANK + 0.01); verb_send.add(st, T_CLANK + 0.01, 0.5)
    pad_p = Part(89, gain_db=-4)   # Pad 2 (warm)
    pad_p.chord(T_CLANK, DUR - T_CLANK - 0.2, [50, 57, 62, 64, 66, 69], vel=62)
    ep = Part(4, gain_db=-6)       # Electric Piano 1
    ep.chord(T_CLANK + 0.02, 2.6, [62, 66, 69, 73, 76], vel=58, strum=0.035)
    P = pad_p.render(DUR + 2.0); E_ = ep.render(DUR + 2.0)
    att = np.clip((np.arange(len(P)) / SR - T_CLANK) / 0.25, 0, 1)[:, None]
    mus.x[:len(P)] += P * att * 0.9 + E_ * 0.8
else:  # ------------------------------------------------------------ "logo": whoosh + assinatura discreta
    T_LAND = cue["land"][0]["t"] if "land" in cue else min(1.0, DUR / 3)
    # 1) respiro baixo subindo até o pouso + um whoosh só (o logo entra inteiro)
    r = riser(max(0.3, T_LAND - 0.05), 0.06, 250, 4200, 11); fx.add(r, 0.05); verb_send.add(r, 0.05, 0.6)
    for c in cue.get("whoosh", []):
        y = whoosh(0.55, 600, 3000, 0.30, move=0.25, seed=21)
        fx.add(y, c["t"] - 0.10); verb_send.add(y, c["t"] - 0.10, 0.35)
    # 2) pouso: grave suave + sino de vidro, sem metal
    fx.add(bloom(0.45, 2.4, (58, 41)), T_LAND)
    st = sting(0.34); fx.add(st, T_LAND + 0.01); verb_send.add(st, T_LAND + 0.01, 0.6)
    fx.add(tick(0.04, 2600), T_LAND)
    pad_p = Part(89, gain_db=-4)   # Pad 2 (warm)
    pad_p.chord(T_LAND, DUR - T_LAND - 0.2, [50, 57, 62, 66, 69], vel=56)
    ep = Part(4, gain_db=-7)       # Electric Piano 1
    ep.chord(T_LAND + 0.04, 2.4, [62, 69, 74, 78], vel=50, strum=0.05)
    P = pad_p.render(DUR + 2.0); E_ = ep.render(DUR + 2.0)
    att = np.clip((np.arange(len(P)) / SR - T_LAND) / 0.30, 0, 1)[:, None]
    mus.x[:len(P)] += P * att * 0.85 + E_ * 0.7
# 3) brilho, movimento, título, saída
for c in cue.get("shine", []): y = shimmer(0.22); fx.add(y, c["t"]); verb_send.add(y, c["t"], 0.8)
for c in cue.get("swoosh", []): y = whoosh(0.55, 500, 3000, 0.28, move=-0.4, seed=33); fx.add(y, c["t"] - 0.1); verb_send.add(y, c["t"] - 0.1, 0.4)
for c in cue.get("pop", []): fx.add(pop(81, 0.22), c["t"]); fx.add(tick(0.05, 3200), c["t"] + 0.02)
for c in cue.get("out", []): y = whoosh(0.6, 2600, 600, 0.22, move=0.0, seed=41); fx.add(y, c["t"]); verb_send.add(y, c["t"], 0.6)

n = int(round(DUR * SR))
mix = fx.x + reverb(verb_send.x, make_ir(2.2, 0.015, 7, 0.55)) * 0.35 + mus.x * 0.55
mix = mix[:n]
fo = int(0.45 * SR); mix[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.6
mix = mix / (np.abs(mix).max() + 1e-9) * 10 ** (-4.0 / 20)
import pyloudnorm as pyln
lufs = pyln.Meter(SR).integrated_loudness(mix)
mix = mix * 10 ** ((-19.0 - lufs) / 20)          # um pouco abaixo da voz (-16 LUFS)
mix = limit(mix, -1.5)
sf.write(out_path, mix.astype(np.float32), SR, subtype="FLOAT")
print(f"vinheta {DUR:.2f}s  {pyln.Meter(SR).integrated_loudness(mix):.1f} LUFS  pico {20*np.log10(np.abs(mix).max()):.1f} dBFS")
