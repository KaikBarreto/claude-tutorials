"""Monta o contexto de um capitulo (JSON -> telemetria, camera, cursor, palco, camadas) e compoe quadros.
Usado por render_chapter.py e sheet.py. Caminhos do JSON sao relativos ao proprio JSON; tempos em s do video."""
import json, os
import numpy as np, cv2
from common import probe
from tele import Tele, RATE
from camera import Camera, Geom, W, H, FPS
from stage import Stage
from cursor import CursorLayer
from overlay import Overlays


class Chapter:
    def __init__(self, cj, rng=None):
        self.cj = os.path.abspath(cj); self.base = os.path.dirname(self.cj); ch = self.ch = json.load(open(self.cj))
        self.name = ch.get("name") or os.path.splitext(os.path.basename(self.cj))[0].replace(".chapter", "")
        self.outd = self.rp(ch.get("output", {}).get("dir", "out")); self.video, self.tele_path = self.rp(ch["video"]), self.rp(ch["telemetry"])
        info = self.info = probe(self.video); self.SW, self.SH, self.dur = info["w"], info["h"], info["dur"]
        trim = ch.get("trim", {}); self.t0 = float(trim.get("start", 0.0)); self.t1 = float(trim.get("end") or self.dur)
        if rng: self.t0, self.t1 = max(self.t0, rng[0]), min(self.t1, rng[1])
        self.n = int(round((self.t1 - self.t0) * FPS))
        self.tele = Tele(self.tele_path, self.dur); self.T = np.arange(int((self.dur + 3) * RATE)) / RATE
        ccfg = dict(ch.get("cursor", {})); self.cur = self.tele.path(self.T, ccfg.get("smooth", 0.67))
        sc = ch.get("stage", {}); self.geom = Geom(self.SW, self.SH, sc.get("margin", 44), sc.get("radius", 16))
        self.cam = Camera(self.tele, self.geom, self.cur, self.T, self.dur, ch.get("camera"), ch.get("zooms", []))
        vp = self.tele.raw["video"].get("viewportCss", {}); ccfg.setdefault("dpr", self.SW / vp["width"] if vp.get("width") else 2.0)
        self.cursor = CursorLayer(self.tele, self.geom, self.T, self.cur, ccfg); self.stage = Stage(self.geom, sc.get("shadow", 0.20), self.rp(sc["bg"]) if sc.get("bg") else None, sc.get("phone"))
        self.ov = Overlays(ch, self.base); self.shut = self.cam.cfg["shutter"] / FPS; self._prev = None; self.reused = 0

    def rp(self, p):
        return p if (p is None or os.path.isabs(p)) else os.path.normpath(os.path.join(self.base, p))

    def compose(self, t, fr):
        """quadro final 1920x1080 RGB para o instante t (s do video) e o quadro de origem fr; devolve (img, n de sub-quadros).
        Se o video e a janela da camera nao mudaram desde o quadro anterior, reaproveita o palco ja composto (so refaz cursor e camadas)."""
        cam = self.cam; n = cam.n_samples(t, self.shut); ts = [t] if n == 1 else [t + (j / (n - 1) - 0.5) * self.shut for j in range(n)]
        views = [cam.view(tt) for tt in ts]; p = self._prev
        if n == 1 and p is not None and max(abs(views[0][i] - p[0][i]) for i in range(3)) < 0.02 and cv2.norm(fr, p[1], cv2.NORM_INF) == 0:
            base, crect = p[2], p[3]; self.reused += 1  # mantem a vista com que o palco foi composto (sem deriva acumulada)
        else:
            base, crect = self.stage.render(fr, views); base = np.ascontiguousarray(base)
            self._prev = (views[0], fr, base, crect) if n == 1 else None
        if n > 1: self._prev = None
        img = base.copy()
        self.cursor.draw(img, t, cam, self.shut); self.ov.under(img, t); self.ov.over(img, t, crect, cam.view(t))
        return img, n

    def align_audio(self, out_wav):
        """narracao (qualquer taxa/canais) -> WAV mono 48 kHz float32 alinhado ao MP4 (mesma duracao, silencio onde falta)"""
        import soundfile as sf
        from math import gcd
        from scipy.signal import resample_poly
        SR = 48000; n_out = int(round(self.n / FPS * SR)); nar = self.rp(self.ch.get("narration")); off = float(self.ch.get("audio_offset", 0.0))
        y = np.zeros(n_out, np.float32)
        if nar:
            x, sr = sf.read(nar, dtype="float32", always_2d=True); x = x.mean(1)
            if sr != SR: g = gcd(SR, sr); x = resample_poly(x, SR // g, sr // g).astype(np.float32)
            s0 = int(round((self.t0 - off) * SR)); a, b = max(0, s0), min(len(x), s0 + n_out)  # amostra da narracao que cai no 1o quadro
            if b > a: y[a - s0:b - s0] = x[a:b]
            f = int(0.004 * SR); y[:f] *= np.linspace(0, 1, f); y[-f:] *= np.linspace(1, 0, f)
        sf.write(out_wav, y, SR, subtype="FLOAT")
        return nar is not None
