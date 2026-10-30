"""Instrumentos de verdade via SoundFont (GeneralUser GS + tinysoundfont), 48 kHz estéreo float.
Uso: p = Part(4); p.note(t, dur, 62, 70); y = p.render(total)  -> np.ndarray (n, 2)"""
import os
import numpy as np
import tinysoundfont

SR = 48000
SF2 = os.environ.get("SF2", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models", "GeneralUser-GS.sf2"))
_SF_BYTES = None


class Part:
    def __init__(self, preset, bank=0, drums=False, gain_db=0.0):
        self.preset, self.bank, self.drums, self.gain = preset, bank, drums, gain_db
        self.ev = []  # (amostra, ordem, tipo, a, b)

    def note(self, t, dur, key, vel=80):
        i0 = int(round(t * SR)); i1 = max(i0 + 1, int(round((t + dur) * SR)))
        self.ev.append((i0, 1, "on", int(key), int(np.clip(vel, 1, 127))))
        self.ev.append((i1, 0, "off", int(key), 0))

    def chord(self, t, dur, keys, vel=70, strum=0.0):
        for k, key in enumerate(keys):
            self.note(t + k * strum, dur - k * strum, key, vel)

    def cc(self, t, ctrl, val):
        self.ev.append((int(round(t * SR)), 0, "cc", int(ctrl), int(val)))

    def render(self, total):
        global _SF_BYTES
        if _SF_BYTES is None:
            _SF_BYTES = open(SF2, "rb").read()
        syn = tinysoundfont.Synth(gain=self.gain, samplerate=SR)
        sfid = syn.sfload(_SF_BYTES)
        ch = 9 if self.drums else 0
        syn.program_select(ch, sfid, 128 if self.drums else self.bank, self.preset, is_drums=self.drums)
        n = int(round(total * SR)); out = np.zeros((n, 2), np.float32); pos = 0
        for i, _, kind, a, b in sorted(self.ev):
            i = min(i, n)
            if i > pos:
                out[pos:i] = np.frombuffer(syn.generate(i - pos), np.float32).reshape(-1, 2); pos = i
            if kind == "on": syn.noteon(ch, a, b)
            elif kind == "off": syn.noteoff(ch, a)
            else: syn.control_change(ch, a, b)
        if pos < n:
            out[pos:] = np.frombuffer(syn.generate(n - pos), np.float32).reshape(-1, 2)
        return out.astype(np.float64)
