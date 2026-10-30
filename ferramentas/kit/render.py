"""Renderiza a aula editada: vinheta + conteúdo (cortes, acelerações com mistura de quadros, palco, câmera/zoom,
destaques e sobreposições) + cartela final. Gera só o vídeo; o áudio entra no mux (kit/mix.py + kit/mux.sh).
uso: python3 kit/render.py <projeto> [--out out/video.mp4] [--stills t1,t2,...] [--range a:b]
  --stills / --range usam tempo de CONTEÚDO (s, sem a vinheta) e servem para revisar antes do render completo.
Configuração opcional em <projeto>/render.json: {"stage": true, "margin": 44, "radius": 16, "decode_w": 2560,
  "crf": 20, "preset": "fast", "min_zoom_frac": 0.38}"""
import json, os, subprocess, sys, time
import numpy as np, cv2
from PIL import Image

KIT = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, KIT)
import ui

argv = sys.argv[1:]; proj = os.path.abspath(argv[0]); P = lambda *a: os.path.join(proj, *a)
opt = lambda k, d=None: argv[argv.index(k) + 1] if k in argv else d
cfg = json.load(open(P("render.json"))) if os.path.exists(P("render.json")) else {}
meta = json.load(open(P("project.json"))); edl = json.load(open(P("edl.json")))
W, H, FPS = 1920, 1080, 30
STAGE = cfg.get("stage", True); MARGIN = cfg.get("margin", 44); RADIUS = cfg.get("radius", 16)
SW, SH = meta["w"], meta["h"]
DW = min(SW, cfg.get("decode_w", 2560)); DW -= DW % 2; DH = int(round(SH * DW / SW / 2)) * 2; SC = DW / SW
SEGS = edl["segments"]; CDUR = edl["out_dur"]
XF_IN, XF_OUT = 0.4, 0.5
cv2.setNumThreads(2)


# ------------------------------------------------------------------ leitura sequencial (com salto por -ss)
class Source:
    def __init__(self, path, w, h, fps=FPS, vf_extra=""):
        self.path, self.w, self.h, self.fps, self.vf = path, w, h, fps, vf_extra
        self.p = None; self.idx = -1; self.buf = {}; self.last = None; self.eof = False

    def _open(self, i):
        if self.p: self.p.kill(); self.p.wait()
        info = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0",
                               self.path], capture_output=True, text=True).stdout.strip().split(",") if not hasattr(self, "same") else None
        if info: self.same = (int(info[0]), int(info[1])) == (self.w, self.h)
        sc = "" if self.same else f",scale={self.w}:{self.h}:flags=area"
        cmd = ["ffmpeg", "-v", "error"] + (["-ss", f"{i / self.fps:.4f}"] if i > 0 else []) + ["-i", self.path, "-an", "-vf",
               f"fps={self.fps}{sc}{self.vf},format=rgb24", "-f", "rawvideo", "-"]
        self.p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=self.w * self.h * 3 * 2)
        self.idx = i - 1; self.buf = {}; self.eof = False

    def get(self, i):
        if i in self.buf: return self.buf[i]
        if self.p is None or i < self.idx - 20 or i - self.idx > 240 or (i <= self.idx and i not in self.buf): self._open(i)
        n = self.w * self.h * 3
        while self.idx < i and not self.eof:
            raw = self.p.stdout.read(n)
            if len(raw) < n: self.eof = True; break
            self.idx += 1; self.last = self.buf[self.idx] = np.frombuffer(raw, np.uint8).reshape(self.h, self.w, 3)
            if len(self.buf) > 28: del self.buf[min(self.buf)]
        return self.buf.get(i, self.last)


# ------------------------------------------------------------------ tempo de saída -> fonte
seg_out = np.array([s["out_s"] for s in SEGS])


def src_frames(tau):
    """índices de quadro da fonte (30 qps) para o instante de conteúdo tau; >1 índice = mistura (acelerado)"""
    k = max(0, int(np.searchsorted(seg_out, tau, "right")) - 1); s = SEGS[k]
    sp = s["speed"]; t = s["src_s"] + (tau - s["out_s"]) * sp
    t = min(t, s["src_e"] - 0.5 / FPS)
    if sp <= 1: return [int(round(t * FPS))], s
    m = int(min(round(sp), 6)); span = sp / FPS
    return sorted(set(int(round((t + (j + 0.5) / m * span - span / 2) * FPS)) for j in range(m))), s


# ------------------------------------------------------------------ câmera (janela em px da fonte, aspecto 16:9)
def view_fit(margin):
    s0 = min((W - 2 * margin) / SW, (H - 2 * margin) / SH); vw, vh = W / s0, H / s0
    return np.array([SW / 2 - vw / 2, SH / 2 - vh / 2, vw])


V0 = view_fit(MARGIN if STAGE else 0)


def view_zoom(rect, pad=0.10):
    x, y, w, h = rect; cx, cy = x + w / 2, y + h / 2
    w2, h2 = w * (1 + 2 * pad), h * (1 + 2 * pad)
    w2 = max(w2, h2 * W / H)
    w2 = min(max(w2, SW * cfg.get("min_zoom_frac", 0.38)), SW, SH * W / H); h2 = w2 * H / W
    return np.array([min(max(cx - w2 / 2, 0), SW - w2), min(max(cy - h2 / 2, 0), SH - h2), w2])


anchors = [(0.0, V0)]
for z in sorted(edl.get("zooms", []), key=lambda z: z["s_out"]):
    Z = view_zoom(z["rect"]); a, b = z["s_out"], z["e_out"]
    tin, tout = float(z.get("tin", 0.7)), float(z.get("tout", 0.8))
    if a - tin > anchors[-1][0]: anchors.append((a - tin * 0.5, anchors[-1][1]))
    anchors.append((a + tin * 0.5, Z)); anchors.append((max(a + tin * 0.5, b - tout * 0.4), Z)); anchors.append((b + tout * 0.6, V0))
anchors.sort(key=lambda p: p[0])
AT = np.array([a[0] for a in anchors])
ease = lambda p: 4 * p ** 3 if p < .5 else 1 - (-2 * p + 2) ** 3 / 2


def view_at(tau):
    i = int(np.searchsorted(AT, tau, "right")) - 1
    if i < 0: return anchors[0][1]
    if i >= len(anchors) - 1: return anchors[-1][1]
    (t0, v0), (t1, v1) = anchors[i], anchors[i + 1]
    if t1 - t0 < 1e-6: return v1
    p = ease((tau - t0) / (t1 - t0))
    c0 = v0[:2] + np.array([v0[2], v0[2] * H / W]) / 2; c1 = v1[:2] + np.array([v1[2], v1[2] * H / W]) / 2
    w = np.exp(np.log(v0[2]) + (np.log(v1[2]) - np.log(v0[2])) * p); c = c0 + (c1 - c0) * p
    return np.array([c[0] - w / 2, c[1] - w * H / W / 2, w])


# ------------------------------------------------------------------ palco
BG = ui.stage_background(W, H) if STAGE else np.zeros((H, W, 3), np.uint8)
_shadow_cache = {}


def shadow_for(rect_key, X0, Y0, X1, Y1, r):
    if rect_key in _shadow_cache: return _shadow_cache[rect_key]
    f = 4; a, _ = ui.rrect_alpha(W // f, H // f, X0 / f, Y0 / f + 14 / f, X1 / f, Y1 / f + 14 / f, r / f)
    a = cv2.GaussianBlur(a, (0, 0), 30 / f); a = cv2.resize(a, (W, H), interpolation=cv2.INTER_LINEAR) * 0.20
    bg = (BG.astype(np.float32) * (1 - a[..., None])).astype(np.uint8)
    if len(_shadow_cache) > 4: _shadow_cache.clear()
    _shadow_cache[rect_key] = bg; return bg


_fast = {}


def compose_stage(frame):
    """caminho rápido p/ a vista padrão do palco (sem zoom): redimensiona, cola e mistura só os 4 cantos"""
    if not _fast:
        k = W / V0[2]; X0, Y0 = -V0[0] * k, -V0[1] * k
        x0, y0, w, h = int(round(X0)), int(round(Y0)), int(round(SW * k)), int(round(SH * k))
        bg = shadow_for(("stage", x0, y0, w, h), x0, y0, x0 + w, y0 + h, RADIUS) if STAGE else BG.copy()
        r = int(np.ceil(RADIUS)) + 1
        a, _ = ui.rrect_alpha(2 * r + 4, 2 * r + 4, 0, 0, 2 * r + 4, 2 * r + 4, RADIUS)
        _fast.update(x0=x0, y0=y0, w=w, h=h, bg=bg, r=r, a_tl=a[:r, :r, None], a_tr=a[:r, -r:, None], a_bl=a[-r:, :r, None], a_br=a[-r:, -r:, None])
    g = _fast; x0, y0, w, h, r = g["x0"], g["y0"], g["w"], g["h"], g["r"]
    out = g["bg"].copy()
    f_ = w / frame.shape[1]
    c = cv2.resize(frame, (w, h), interpolation=cv2.INTER_AREA if f_ < 0.75 else cv2.INTER_LINEAR if f_ <= 1.0 else cv2.INTER_CUBIC)
    out[y0:y0 + h, x0:x0 + w] = c
    for (ys, xs, a) in ((slice(0, r), slice(0, r), g["a_tl"]), (slice(0, r), slice(w - r, w), g["a_tr"]),
                        (slice(h - r, h), slice(0, r), g["a_bl"]), (slice(h - r, h), slice(w - r, w), g["a_br"])):
        oy = slice(y0 + ys.start, y0 + ys.stop); ox = slice(x0 + xs.start, x0 + xs.stop)
        out[oy, ox] = (c[ys, xs] * a + g["bg"][oy, ox] * (1 - a)).astype(np.uint8)
    return out, (x0, y0, x0 + w, y0 + h)


def compose(frame, v):
    """frame em px de decodificação; v = (vx, vy, vw) em px da fonte. Retorna (img RGB uint8, retângulo do conteúdo)"""
    if np.allclose(v, V0, atol=1e-3): return compose_stage(frame)
    k = W / v[2]; kd = k / SC
    X0, Y0, X1, Y1 = -v[0] * k, -v[1] * k, (SW - v[0]) * k, (SH - v[1]) * k
    r = RADIUS * k / (W / V0[2])
    if kd < 0.75:  # reduz antes com INTER_AREA (texto nítido)
        fw, fh = max(2, int(round(DW * kd))), max(2, int(round(DH * kd)))
        frame = cv2.resize(frame, (fw, fh), interpolation=cv2.INTER_AREA); kx, ky = fw / SW, fh / SH
    else:
        kx, ky = SC, SC
    M = np.array([[k / kx, 0, -v[0] * k], [0, k / ky, -v[1] * k]], np.float32)
    covers = X0 <= 0.5 and Y0 <= 0.5 and X1 >= W - 0.5 and Y1 >= H - 0.5
    interp = cv2.INTER_CUBIC if k / kx > 1.05 else cv2.INTER_LINEAR
    if covers:
        return cv2.warpAffine(frame, M, (W, H), flags=interp, borderMode=cv2.BORDER_REPLICATE), (0, 0, W, H)
    content = cv2.warpAffine(frame, M, (W, H), flags=interp, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    key = (round(X0, 1), round(Y0, 1), round(X1, 1), round(Y1, 1))
    bg = shadow_for(key, X0, Y0, X1, Y1, r) if STAGE else BG
    a, _ = ui.rrect_alpha(W, H, X0, Y0, X1, Y1, r)
    out = (content.astype(np.float32) * a[..., None] + bg.astype(np.float32) * (1 - a[..., None]))
    return out.astype(np.uint8), (max(0, X0), max(0, Y0), min(W, X1), min(H, Y1))


# ------------------------------------------------------------------ sobreposições
GREEN = np.array(ui.GREEN, np.float32)
ACT = np.load(P("activity.npz")) if os.path.exists(P("activity.npz")) else None
_corner = {}


def badge_corner(seg):
    """canto do selo de velocidade: o primeiro (sup. dir., inf. dir., sup. esq., inf. esq.) longe de onde a tela muda"""
    key = (seg["src_s"], seg["src_e"])
    if key in _corner: return _corner[key]
    best = "tr"
    if ACT is not None:
        m = (ACT["t"] >= seg["src_s"]) & (ACT["t"] <= seg["src_e"]) & (ACT["px"] > 8)
        bx = ACT["box"][m]
        if len(bx):
            bw, bh = 0.16 * SW, 0.12 * SH  # área do selo em px da fonte (com folga)
            cand = {"tr": (SW - bw, 0, SW, bh), "br": (SW - bw, SH - bh, SW, SH), "tl": (0, 0, bw, bh), "bl": (0, SH - bh, bw, SH)}
            hits = {c: int(((bx[:, 0] < r[2]) & (bx[:, 2] > r[0]) & (bx[:, 1] < r[3]) & (bx[:, 3] > r[1])).sum()) for c, r in cand.items()}
            best = min(["tr", "br", "tl", "bl"], key=lambda c: (hits[c], ["tr", "br", "tl", "bl"].index(c)))
    _corner[key] = best; return best
eoc = lambda p: 1 - (1 - min(max(p, 0), 1)) ** 3


def paste(img, spr_pad, x, y, alpha=1.0):
    spr, pad = spr_pad; a = np.asarray(spr, np.float32); x, y = int(round(x - pad)), int(round(y - pad))
    h, w = a.shape[:2]; x0, y0, x1, y1 = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
    if x1 <= x0 or y1 <= y0 or alpha <= 0.003: return
    s = a[y0 - y:y1 - y, x0 - x:x1 - x]; al = s[..., 3:4] / 255 * alpha
    reg = img[y0:y1, x0:x1].astype(np.float32); img[y0:y1, x0:x1] = (reg * (1 - al) + s[..., :3] * al).astype(np.uint8)


def overlays(img, tau, seg, v, crect):
    X0, Y0, X1, Y1 = crect; k = W / v[2]
    # destaque: escurece o resto + contorno verde
    for sp in edl.get("spots", []):
        a, b = sp["s_out"], sp["e_out"]
        al = min(eoc((tau - a) / 0.3), eoc((b - tau) / 0.3))
        if al <= 0: continue
        x, y, w, h = sp["rect"]; pad = 10
        rx0, ry0 = (x - v[0]) * k - pad, (y - v[1]) * k - pad; rx1, ry1 = (x + w - v[0]) * k + pad, (y + h - v[1]) * k + pad
        bx0, by0 = max(0, int(rx0) - 8), max(0, int(ry0) - 8); bx1, by1 = min(W, int(rx1) + 9), min(H, int(ry1) + 9)
        orig = img[by0:by1, bx0:bx1].astype(np.float32)
        img[:] = cv2.convertScaleAbs(img, alpha=1 - 0.42 * al)
        if bx1 > bx0 and by1 > by0:
            inside, sd = ui.rrect_alpha(bx1 - bx0, by1 - by0, rx0 - bx0, ry0 - by0, rx1 - bx0, ry1 - by0, 14)
            f = orig * (1 - 0.42 * al * (1 - inside[..., None]))
            ring = np.clip(1.6 - np.abs(sd + 1.5) / 1.2, 0, 1)[..., None] * al
            img[by0:by1, bx0:bx1] = (f * (1 - ring) + GREEN * ring).astype(np.uint8)
        if sp.get("label"):
            lab = ui.spot_label(sp["label"]); lw, lh = lab[0].width - 2 * lab[1], lab[0].height - 2 * lab[1]
            ly = ry0 - lh - 14 if ry0 - lh - 14 > Y0 + 8 else ry1 + 14
            paste(img, lab, min(max((rx0 + rx1) / 2 - lw / 2, X0 + 12), X1 - lw - 12), ly + 8 * (1 - eoc((tau - a) / 0.3)), al)
    # selo de velocidade
    if seg["speed"] > 1:
        al = min(eoc((tau - seg["out_s"]) / 0.15), eoc((seg["out_e"] - tau) / 0.12))
        b = ui.speed_badge(seg["speed"]); bw, bh = b[0].width - 2 * b[1], b[0].height - 2 * b[1]
        c = badge_corner(seg)
        bx = X1 - 28 - bw if c[1] == "r" else X0 + 28
        by = Y0 + 26 - 6 * (1 - al) if c[0] == "t" else Y1 - 26 - bh + 6 * (1 - al)
        paste(img, b, bx, by, al)
    # título de tópico (canto inferior esquerdo)
    for ch in edl.get("chapters", []):
        a = ch["t_out"]; b = a + float(ch.get("dur", 3.4))
        if not (a - 0.05 <= tau <= b): continue
        pin, pout = eoc((tau - a) / 0.4), eoc((b - tau) / 0.35)
        lt = ui.lower_third(ch["title"], ch.get("kicker", "")); lh = lt[0].height - 2 * lt[1]
        paste(img, lt, X0 + 36 - 46 * (1 - pin) - 20 * (1 - pout), Y1 - 36 - lh, min(pin, pout))
    for co in edl.get("callouts", []):
        a, b = co["s_out"], co["e_out"]
        al = min(eoc((tau - a) / 0.3), eoc((b - tau) / 0.25))
        if al <= 0: continue
        c = ui.callout(co["text"]); cw, chh = c[0].width - 2 * c[1], c[0].height - 2 * c[1]
        cy = Y0 + 26 - 10 * (1 - al) if co.get("pos") == "top" else Y1 - 30 - chh + 10 * (1 - al)
        paste(img, c, (X0 + X1) / 2 - cw / 2, cy, al)


# ------------------------------------------------------------------ quadro de conteúdo
src = Source(meta["src"], DW, DH)


def content_frame(tau):
    idx, seg = src_frames(tau)
    fr = src.get(idx[0])
    for j, i in enumerate(idx[1:], 2):
        fr = cv2.addWeighted(fr, (j - 1) / j, src.get(i), 1 / j, 0)
    v = view_at(tau); img, crect = compose(fr, v)
    img = np.ascontiguousarray(img); overlays(img, tau, seg, v, crect)
    return img


def run_stills(ts):
    os.makedirs(P("stills"), exist_ok=True)
    for t in ts:
        Image.fromarray(content_frame(t)).save(P("stills", f"c{t:08.2f}.png"))
    print("stills ->", P("stills"))


if "--stills" in argv:
    run_stills([float(t) for t in opt("--stills").split(",")]); sys.exit()

intro_p, outro_p = P("build", "intro_v.mp4"), P("build", "outro_v.mp4")
dur_of = lambda f: float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                                        capture_output=True, text=True).stdout or 0)
T_IN = dur_of(intro_p) if os.path.exists(intro_p) and "--range" not in argv else 0.0
T_OUT = dur_of(outro_p) if os.path.exists(outro_p) and "--range" not in argv else 0.0
n_in = int(round(T_IN * FPS)); n_c = int(round(CDUR * FPS)); n_out = int(round(T_OUT * FPS)); n_xo = int(round(XF_OUT * FPS)) if n_out else 0
r0, r1 = 0, n_in + n_c + n_out - n_xo
if "--range" in argv:
    a, b = map(float, opt("--range").split(":")); r0, r1 = int(a * FPS), int(b * FPS)
if "--frames" in argv:
    r0, r1 = map(int, opt("--frames").split(":"))
NW = int(opt("--workers", "1"))
if NW > 1 and "--frames" not in argv and "--range" not in argv:
    # divide em NW partes (cortes em múltiplos de 60 quadros = início de GOP) e junta sem recodificar
    out_path = opt("--out", P("out", "video.mp4")); os.makedirs(os.path.dirname(out_path), exist_ok=True)
    tot = r1; b = [0] + [int(round(tot * k / NW / 60)) * 60 for k in range(1, NW)] + [tot]
    t0 = time.time(); procs = []
    for k in range(NW):
        procs.append(subprocess.Popen([sys.executable, os.path.abspath(__file__), proj, "--frames", f"{b[k]}:{b[k + 1]}",
                                       "--out", P("build", f"part{k}.mp4")], stdout=open(P("build", f"part{k}.log"), "w"), stderr=subprocess.STDOUT))
    while any(pp.poll() is None for pp in procs):
        time.sleep(5)
        prog = []
        for k in range(NW):
            try: prog.append(open(P("build", f"part{k}.log")).read().replace("\r", "\n").strip().split("\n")[-1][:40])
            except Exception: prog.append("")
        print("\r" + " | ".join(prog), end="", flush=True)
    if any(pp.returncode for pp in procs): sys.exit("\nfalhou uma parte — veja build/part*.log")
    open(P("build", "parts.txt"), "w").write("".join(f"file '{P('build', f'part{k}.mp4')}'\n" for k in range(NW)))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", P("build", "parts.txt"), "-c", "copy",
                    "-movflags", "+faststart", out_path], check=True)
    json.dump({"intro": T_IN, "content": CDUR, "outro": T_OUT, "xf_out": XF_OUT if n_out else 0,
               "outro_start": T_IN + CDUR - (XF_OUT if n_out else 0), "total": tot / FPS}, open(P("timeline.json"), "w"), indent=1)
    print(f"\nok {out_path}  ({tot / FPS:.1f} s, {(time.time() - t0) / 60:.1f} min, {NW} partes)"); sys.exit()
intro = Source(intro_p, W, H) if n_in else None
outro = Source(outro_p, W, H) if n_out else None
out_path = opt("--out", P("out", "video.mp4")); os.makedirs(os.path.dirname(out_path), exist_ok=True)
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                        "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p", "-c:v", "libx264",
                        "-preset", cfg.get("preset", "veryfast"), "-crf", str(cfg.get("crf", 20)), "-g", "60",
                        "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-movflags", "+faststart", out_path],
                       stdin=subprocess.PIPE)
last_intro = None; t0 = time.time()
if "--frames" not in argv:
    json.dump({"intro": T_IN, "content": CDUR, "outro": T_OUT, "xf_out": XF_OUT if n_out else 0,
               "outro_start": T_IN + CDUR - (XF_OUT if n_out else 0), "total": (r1 - r0) / FPS},
              open(P("timeline.json"), "w"), indent=1)
for f in range(r0, r1):
    if f < n_in:
        img = intro.get(f); last_intro = img
    else:
        c = f - n_in
        if c < n_c:
            tau = c / FPS; img = content_frame(tau)
            if last_intro is None and n_in and tau < XF_IN: last_intro = intro.get(n_in - 1)
            if last_intro is not None and tau < XF_IN:
                p = tau / XF_IN; img = (img.astype(np.float32) * p + last_intro.astype(np.float32) * (1 - p)).astype(np.uint8)
            if n_out and c >= n_c - n_xo:
                o = outro.get(c - (n_c - n_xo)); p = (c - (n_c - n_xo) + 1) / (n_xo + 1)
                img = (img.astype(np.float32) * (1 - p) + o.astype(np.float32) * p).astype(np.uint8)
        else:
            img = outro.get(c - n_c + n_xo)
    enc.stdin.write(np.ascontiguousarray(img).tobytes())
    if f % 150 == 0:
        el = time.time() - t0; done = f - r0 + 1
        print(f"\r{done}/{r1 - r0} quadros  {done / el:.1f} q/s  falta ~{(r1 - r0 - done) / max(done / el, 1e-3) / 60:.1f} min", end="", flush=True)
enc.stdin.close(); enc.wait()
print(f"\nok {out_path}  ({(r1 - r0) / FPS:.1f} s, {(time.time() - t0) / 60:.1f} min)")
