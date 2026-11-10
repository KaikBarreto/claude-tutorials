"""Camadas por cima do video: titulo de capitulo (cartao escuro #1E1E1E + acento verde, Montserrat, sem contador),
callouts, destaques (spots) e ilustracoes (clipe MP4 ou sequencia PNG com alfa) encaixadas num intervalo.
Todos os tempos do JSON sao em segundos do video (mesmo relogio da telemetria)."""
import glob, json, os, subprocess
import numpy as np, cv2
from stage import ui
from camera import W, H

eoc = lambda p: 1 - (1 - min(max(p, 0.0), 1.0)) ** 3
GREEN = np.array(ui.GREEN, np.float32)


def paste(img, spr_pad, x, y, alpha=1.0, fit_w=None):
    spr, pad = spr_pad; a = np.asarray(spr, np.float32)
    if fit_w and a.shape[1] - 2 * pad > fit_w:  # titulo maior que a tela: encolhe mantendo a proporcao
        f = fit_w / (a.shape[1] - 2 * pad); a = cv2.resize(a, None, fx=f, fy=f, interpolation=cv2.INTER_AREA); pad = int(pad * f)
    x, y = int(round(x - pad)), int(round(y - pad)); h, w = a.shape[:2]
    x0, y0, x1, y1 = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
    if x1 <= x0 or y1 <= y0 or alpha <= 0.003: return
    s = a[y0 - y:y1 - y, x0 - x:x1 - x]; al = s[..., 3:4] / 255 * alpha
    reg = img[y0:y1, x0:x1].astype(np.float32); img[y0:y1, x0:x1] = (reg * (1 - al) + s[..., :3] * al).astype(np.uint8)


def size_of(spr_pad):
    return spr_pad[0].width - 2 * spr_pad[1], spr_pad[0].height - 2 * spr_pad[1]


class Illus:
    """ilustracao: clipe de video (mp4/mov/webm; com alfa se o pix_fmt tiver) ou sequencia PNG (%04d, pasta ou arquivo unico)"""

    def __init__(self, d, base):
        self.d = d; self.at = float(d["at"]); self.dur = float(d.get("dur", 3.0)); self.src = d["src"]
        self.src = self.src if os.path.isabs(self.src) else os.path.join(base, self.src)
        self.box = d.get("box", [1080, 190, 740, 700]); self.fps = float(d.get("fps", 30)); self.loop = bool(d.get("loop", True))
        self.radius = float(d.get("radius", 18)); self.shadow = bool(d.get("shadow", True)); self.pop = float(d.get("scale_in", 0.06))
        self.mode = None; self.proc = None; self.idx = -1; self.cur = None; self.files = None; self.w = self.h = 0; self.alpha_ch = False; self.nf = 0

    def _open(self):
        s = self.src
        if os.path.isdir(s): self.files = sorted(glob.glob(os.path.join(s, "*.png")))
        elif "%" in s: self.files = sorted(glob.glob(os.path.join(os.path.dirname(s), "*" + os.path.splitext(s)[1])))
        elif s.lower().endswith(".png"): self.files = [s]
        if self.files:
            self.mode = "png"; im = cv2.imread(self.files[0], cv2.IMREAD_UNCHANGED); ih, iw = im.shape[:2]
        else:
            self.mode = "video"
            pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,pix_fmt",
                                            "-of", "json", s], capture_output=True, text=True).stdout)["streams"][0]
            iw, ih = pr["width"], pr["height"]; self.alpha_ch = pr.get("pix_fmt", "").startswith(("yuva", "rgba", "bgra", "argb", "abgr", "gbrap", "ya"))
        bx, by, bw, bh = self.box; f = min(bw / iw, bh / ih) * float(self.d.get("scale", 1.0))
        self.w, self.h = int(round(iw * f / 2)) * 2, int(round(ih * f / 2)) * 2
        self.x, self.y = int(bx + (bw - self.w) / 2), int(by + (bh - self.h) / 2)
        a, _ = ui.rrect_alpha(self.w, self.h, 0, 0, self.w, self.h, self.radius); self.mask = a
        if self.shadow:
            pad = 40; big = np.zeros((self.h + 2 * pad, self.w + 2 * pad), np.float32); big[pad:pad + self.h, pad:pad + self.w] = 1.0
            self.sh = cv2.GaussianBlur(big, (0, 0), 16) * 0.28; self.pad = pad

    def _start(self):
        if self.proc: self.proc.kill(); self.proc.wait()
        pf = "rgba" if self.alpha_ch else "rgb24"
        self.proc = subprocess.Popen(["ffmpeg", "-v", "error", "-i", self.src, "-an", "-vf", f"fps={self.fps},scale={self.w}:{self.h}:flags=area,format={pf}",
                                      "-f", "rawvideo", "-"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=self.w * self.h * 4 * 2)
        self.idx = -1

    def frame(self, tl):
        """quadro (h,w,3 uint8 RGB, alfa h,w float 0..1) para o tempo local tl"""
        want = int(max(0, tl) * self.fps)
        if self.mode == "png":
            i = want % len(self.files) if self.loop else min(want, len(self.files) - 1)
            if i != self.idx:
                im = cv2.imread(self.files[i], cv2.IMREAD_UNCHANGED)
                if im.ndim == 2: im = cv2.cvtColor(im, cv2.COLOR_GRAY2BGR)
                if im.shape[2] == 4:  # redimensiona premultiplicado (sem borda escura nas bordas do alfa)
                    f = im.astype(np.float32); f[..., :3] *= f[..., 3:4] / 255; f = cv2.resize(f, (self.w, self.h), interpolation=cv2.INTER_AREA)
                    a_ = f[..., 3:4]; f[..., :3] = f[..., :3] / np.maximum(a_ / 255, 1e-4); im = np.clip(f, 0, 255).astype(np.uint8)
                else: im = cv2.resize(im, (self.w, self.h), interpolation=cv2.INTER_AREA)
                al = im[..., 3:4].astype(np.float32) / 255 if im.shape[2] == 4 else np.ones((self.h, self.w, 1), np.float32)
                self.cur = (cv2.cvtColor(im[..., :3], cv2.COLOR_BGR2RGB), al[..., 0], im.shape[2] == 4); self.idx = i
            return self.cur
        nch = 4 if self.alpha_ch else 3; n = self.w * self.h * nch
        if self.nf: want = want % self.nf if self.loop else min(want, self.nf - 1)
        if self.proc is None or want < self.idx: self._start()
        while self.idx < want:
            raw = self.proc.stdout.read(n)
            if len(raw) < n:
                if self.idx >= 0: self.nf = self.idx + 1
                if self.loop and self.nf and self.cur is not None: self._start(); want = want % self.nf; continue
                break
            arr = np.frombuffer(raw, np.uint8).reshape(self.h, self.w, nch); self.idx += 1
            self.cur = (arr[..., :3].copy(), arr[..., 3].astype(np.float32) / 255 if nch == 4 else np.ones((self.h, self.w), np.float32), nch == 4)
        return self.cur

    def draw(self, img, t):
        a, b = self.at, self.at + self.dur
        if not (a - 0.01 <= t <= b + 0.01): return
        if self.mode is None: self._open()
        al = min(eoc((t - a) / 0.35), eoc((b - t) / 0.30))
        if al <= 0.003: return
        fr = self.frame(t - a)
        if fr is None: return
        rgb, alpha, has_alpha = fr; sc = 1 - self.pop * (1 - eoc((t - a) / 0.35)); w, h = self.w, self.h
        m = alpha if has_alpha else alpha * self.mask
        if abs(sc - 1) > 1e-3:
            nw, nh = int(round(w * sc)), int(round(h * sc)); rgb = cv2.resize(rgb, (nw, nh), interpolation=cv2.INTER_AREA)
            m = cv2.resize(m, (nw, nh), interpolation=cv2.INTER_AREA); w, h = nw, nh
        x, y = self.x + (self.w - w) // 2, self.y + (self.h - h) // 2
        if self.shadow and not has_alpha:
            pad = self.pad; sx0, sy0 = self.x - pad, self.y - pad + 10; sh = self.sh
            x0, y0, x1, y1 = max(0, sx0), max(0, sy0), min(W, sx0 + sh.shape[1]), min(H, sy0 + sh.shape[0])
            if x1 > x0 and y1 > y0:
                s = sh[y0 - sy0:y1 - sy0, x0 - sx0:x1 - sx0] * al; reg = img[y0:y1, x0:x1]; reg[:] = (reg * (1 - s[..., None])).astype(np.uint8)
        x0, y0, x1, y1 = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
        if x1 <= x0 or y1 <= y0: return
        mm = (m[y0 - y:y1 - y, x0 - x:x1 - x] * al)[..., None]; reg = img[y0:y1, x0:x1].astype(np.float32)
        img[y0:y1, x0:x1] = (reg * (1 - mm) + rgb[y0 - y:y1 - y, x0 - x:x1 - x].astype(np.float32) * mm).astype(np.uint8)

    def close(self):
        if self.proc: self.proc.kill(); self.proc.wait(); self.proc = None


class Overlays:
    def __init__(self, ch, base):
        self.title = ch.get("title"); self.kicker = ch.get("title_kicker", ""); self.t_at = float(ch.get("title_at", 0.5))
        self.t_dur = float(ch.get("title_dur", 3.6)); self.callouts = ch.get("callouts", []); self.spots = ch.get("spots", [])
        self.illus = [Illus(d, base) for d in ch.get("illustrations", [])]

    def under(self, img, t):
        for il in self.illus: il.draw(img, t)

    def over(self, img, t, crect, view):
        X0, Y0, X1, Y1 = crect; cx, cy, vw = view; k = W / vw; vx, vy = cx - vw / 2, cy - vw * H / W / 2
        for sp in self.spots:
            a, b = float(sp["at"]), float(sp["at"]) + float(sp.get("dur", 3.0)); al = min(eoc((t - a) / 0.3), eoc((b - t) / 0.3))
            if al <= 0: continue
            x, y, w, h = sp["rect"]; pad = 10
            rx0, ry0, rx1, ry1 = (x - vx) * k - pad, (y - vy) * k - pad, (x + w - vx) * k + pad, (y + h - vy) * k + pad
            bx0, by0, bx1, by1 = max(0, int(rx0) - 8), max(0, int(ry0) - 8), min(W, int(rx1) + 9), min(H, int(ry1) + 9)
            orig = img[by0:by1, bx0:bx1].astype(np.float32); img[:] = cv2.convertScaleAbs(img, alpha=1 - 0.42 * al)
            if bx1 > bx0 and by1 > by0:
                inside, sd = ui.rrect_alpha(bx1 - bx0, by1 - by0, rx0 - bx0, ry0 - by0, rx1 - bx0, ry1 - by0, 14)
                f = orig * (1 - 0.42 * al * (1 - inside[..., None])); ring = np.clip(1.6 - np.abs(sd + 1.5) / 1.2, 0, 1)[..., None] * al
                img[by0:by1, bx0:bx1] = (f * (1 - ring) + GREEN * ring).astype(np.uint8)
            if sp.get("label"):
                lab = ui.spot_label(sp["label"]); lw, lh = size_of(lab); ly = ry0 - lh - 14 if ry0 - lh - 14 > Y0 + 8 else ry1 + 14
                paste(img, lab, min(max((rx0 + rx1) / 2 - lw / 2, X0 + 12), X1 - lw - 12), ly + 8 * (1 - eoc((t - a) / 0.3)), al)
        for co in self.callouts:
            a, b = float(co["at"]), float(co["at"]) + float(co.get("dur", 3.0)); al = min(eoc((t - a) / 0.3), eoc((b - t) / 0.25))
            if al <= 0: continue
            c = ui.callout(co["text"]); cw, chh = size_of(c)
            cy_ = Y0 + 26 - 10 * (1 - al) if co.get("pos") == "top" else Y1 - 30 - chh + 10 * (1 - al)
            paste(img, c, (X0 + X1) / 2 - cw / 2, cy_, al, fit_w=X1 - X0 - 40)
        if self.title:
            a, b = self.t_at, self.t_at + self.t_dur
            if a - 0.05 <= t <= b:
                pin, pout = eoc((t - a) / 0.4), eoc((b - t) / 0.35); lt = ui.lower_third(self.title, self.kicker); lw, lh = size_of(lt)
                paste(img, lt, X0 + 36 - 46 * (1 - pin) - 20 * (1 - pout), Y1 - 36 - lh, min(pin, pout), fit_w=X1 - X0 - 72)

    def close(self):
        for il in self.illus: il.close()
