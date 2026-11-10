"""Cursor desenhado na edicao: seta estilo macOS grande, mao sobre botoes/links e barra de texto sobre campos
(campo `cursor` da telemetria). Caminho suavizado (fase zero), inclinacao leve, desfoque de movimento, "quique" de escala
de ~350 ms no clique + anel discreto #00C597, some quando parado por muito tempo.
Tudo vetorial (PIL supersample 4x), com ponta/centro no ponto exato (subpixel)."""
import numpy as np, cv2
from PIL import Image, ImageDraw
from tele import RATE
from camera import W, H

GREEN = np.array([0, 197, 151], np.float32)
DEFAULTS = dict(show=True, size=2.5, dpr=2.0, zoom_follow=0.5, smooth=0.67, tilt=7.0, blur=0.6, idle_hide=3.0,
                bounce=0.22, ring=True, ring_alpha=0.55, ring_dur=0.6, ss=4)


def rr(x0, y0, x1, y1, r, n=7):
    pts = []
    for cx, cy, a0 in ((x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)):
        for k in range(n + 1):
            a = np.radians(a0 + 90 * k / n); pts.append((cx + r * np.cos(a), cy + r * np.sin(a)))
    return pts


DARK, WHITE = (22, 22, 24), (255, 255, 255)
SHAPES = {  # unidades = px CSS de um cursor nativo; (poligonos, linhas internas, ponto quente, cor do corpo, cor do contorno)
    0: dict(polys=[[(0, 0), (0, 16.4), (3.7, 13.0), (6.3, 19.2), (8.8, 18.1), (6.3, 12.1), (11.6, 12.1)]], lines=[], hot=(0, 0),
            body=DARK, edge=WHITE, ew=1.0),
    1: dict(polys=[rr(4.4, 0.5, 8.8, 12.5, 2.2), rr(8.8, 5.6, 12.0, 13.0, 1.6), rr(12.0, 6.8, 15.0, 13.6, 1.5),
                   rr(15.0, 8.2, 17.6, 14.6, 1.3), rr(4.4, 8.6, 17.6, 20.2, 3.2), [(4.8, 15.4), (1.0, 10.9), (2.7, 8.8), (5.6, 11.8)]],
            lines=[((8.8, 6.4), (8.8, 12.0)), ((12.0, 7.6), (12.0, 12.6)), ((15.0, 9.0), (15.0, 13.2))], hot=(6.6, 0.8),
            body=WHITE, edge=DARK, ew=1.0),
    2: dict(polys=[rr(-0.7, -8.4, 0.7, 8.4, 0.3, 2), rr(-3.4, -8.4, 3.4, -7.0, 0.5, 2), rr(-3.4, 7.0, 3.4, 8.4, 0.5, 2)], lines=[],
            hot=(0, 0), body=DARK, edge=WHITE, ew=1.0),
}


def sprite(kind, u, phi, fx, fy, ss=4):
    """cursor rasterizado: devolve (C premultiplicado float32 HxWx3 em 0..255, A float32 0..1, x0, y0 relativos ao pixel inteiro do ponto)"""
    s = SHAPES[kind]; pad = int(np.ceil(26 * u)) + 4; S = 2 * pad
    hx, hy = pad + fx, pad + fy; c, sn = np.cos(np.radians(phi)), np.sin(np.radians(phi))
    tr = lambda p: ((hx + (c * (p[0] - s["hot"][0]) - sn * (p[1] - s["hot"][1])) * u) * ss,
                    (hy + (sn * (p[0] - s["hot"][0]) + c * (p[1] - s["hot"][1])) * u) * ss)
    sil = Image.new("L", (S * ss, S * ss), 0); body = Image.new("L", (S * ss, S * ss), 0); ds, db = ImageDraw.Draw(sil), ImageDraw.Draw(body)
    ew = max(1, int(round(2 * s["ew"] * u * ss)))
    for poly in s["polys"]:
        pts = [tr(p) for p in poly]; ds.polygon(pts, fill=255); ds.line(pts + [pts[0]], fill=255, width=ew, joint="curve"); db.polygon(pts, fill=255)
    for a, b in s["lines"]:
        db.line([tr(a), tr(b)], fill=0, width=max(1, int(round(0.55 * u * ss))))
    d = lambda im: cv2.resize(np.asarray(im, np.float32) / 255, (S, S), interpolation=cv2.INTER_AREA)
    sil, body = d(sil), d(body); body = np.minimum(body, sil)
    bc, ec = np.array(s["body"], np.float32), np.array(s["edge"], np.float32)
    C = body[..., None] * bc + (sil - body)[..., None] * ec
    sh = cv2.GaussianBlur(sil, (0, 0), max(0.6, 0.55 * u)); M = np.float32([[1, 0, 0.35 * u], [0, 1, 0.8 * u]])
    sh = cv2.warpAffine(sh, M, (S, S)) * 0.32
    A = sil + sh * (1 - sil)
    return C, A, -pad, -pad


class CursorLayer:
    def __init__(self, tele, geom, T, cur, cfg=None):
        self.c = c = {**DEFAULTS, **(cfg or {})}; self.t, self.g, self.T, self.cur = tele, geom, T, cur; n = len(T); dt = 1.0 / RATE
        self.vel = np.gradient(cur, dt, axis=0); speed = np.hypot(self.vel[:, 0], self.vel[:, 1])
        # atividade -> visibilidade
        act = speed > 12
        for k in tele.clicks: act[int(max(0, (k.td - 0.05) * RATE)):int((k.tu + 0.3) * RATE) + 1] = True
        for st in tele.scrolls: act[int(max(0, (st - 0.2) * RATE)):int((st + 0.2) * RATE) + 1] = True
        last = np.maximum.accumulate(np.where(act, T, 0.0)); target = (T - last) < c["idle_hide"]
        vis = np.zeros(n); v = 1.0
        for i in range(n):
            v = min(1.0, v + dt / 0.15) if target[i] else max(0.0, v - dt / 0.40); vis[i] = v
        self.vis = vis
        # quique de escala
        b = np.ones(n); A = c["bounce"]
        for k in tele.clicks:
            i0, i1, i2 = int(k.td * RATE), int(k.tu * RATE), min(n, int((k.tu + 0.5) * RATE))
            if i0 >= n: continue
            b[i0:i1] = np.minimum(b[i0:i1], 1 - A * np.clip((T[i0:i1] - k.td) / 0.05, 0, 1))
            tau = T[i1:i2] - k.tu; b[i1:i2] = np.minimum(b[i1:i2], 1 - A * np.exp(-tau / 0.07) * np.cos(2 * np.pi * tau / 0.30))
        self.bounce = b
        # tipo de cursor com troca suave
        kd = tele.kind_series(T).astype(int); chg = np.concatenate([[0], np.flatnonzero(np.diff(kd) != 0) + 1])
        ci = np.maximum.accumulate(np.where(np.isin(np.arange(n), chg), np.arange(n), 0)); self.kd, self.ci = kd, ci
        self.cache = {}

    def _kinds(self, i, t):
        kc = int(self.kd[i]); j = int(self.ci[i]); w = np.clip((t - j / RATE) / 0.09, 0, 1) if j > 0 else 1.0
        return [(kc, w)] if w >= 0.999 else [(int(self.kd[j - 1]), 1 - w), (kc, w)]

    def _sprite(self, kind, u, phi, fx, fy):
        key = (kind, round(u, 2), round(phi * 2) / 2, round(fx * 4), round(fy * 4))
        r = self.cache.get(key)
        if r is None:
            if len(self.cache) > 80: self.cache.clear()
            r = self.cache[key] = sprite(kind, u, phi, fx, fy, self.c["ss"])
        return r

    def samples(self, t, cam, shutter_cam):
        """n de sub-quadros do cursor: velocidade na tela (px) x obturador do cursor"""
        i = int(np.clip(t * RATE, 0, len(self.T) - 1)); k = W / cam.view(t)[2]
        sp = np.hypot(*self.vel[i]) * k * self.c["blur"] / 30.0
        return int(np.clip(np.ceil(max(sp, cam.motion(t, shutter_cam)) / 5.0), 1, 8)) if self.c["blur"] > 0 else 1

    def draw(self, img, t, cam, shutter_cam=0.5 / 30):
        c = self.c
        if not c["show"]: return
        f = np.clip(t * RATE, 0, len(self.T) - 1.001); i0 = int(f); a = f - i0
        if self.vis[i0] < 0.004 and self.vis[min(i0 + 1, len(self.vis) - 1)] < 0.004 and not self._ring_active(t): return
        n = self.samples(t, cam, shutter_cam); sh = c["blur"] / 30.0
        ts = [t] if n == 1 else [t + (j / (n - 1) - 0.5) * sh for j in range(n)]
        layers = []; x0, y0, x1, y1 = 1e9, 1e9, -1e9, -1e9
        for tt in ts:
            f = np.clip(tt * RATE, 0, len(self.T) - 1.001); i = int(f); a = f - i; lerp = lambda arr: arr[i] + (arr[i + 1] - arr[i]) * a
            cx, cy, vw = cam.view(tt); k = W / vw; vx, vy = cx - vw / 2, cy - vw * H / W / 2
            px, py = lerp(self.cur[:, 0]), lerp(self.cur[:, 1]); ox, oy = (px - vx) * k, (py - vy) * k
            kc = self.g.k0 * (k / self.g.k0) ** c["zoom_follow"]; u = c["size"] * c["dpr"] * kc
            phi = float(np.clip(lerp(self.vel[:, 0]) * k / 220.0, -1, 1) * c["tilt"]); vis = lerp(self.vis); bn = lerp(self.bounce)
            L = dict(ox=ox, oy=oy, u=u, phi=phi, vis=vis, bn=bn, kinds=self._kinds(i, tt), k=k, vx=vx, vy=vy, t=tt)
            layers.append(L); r = 28 * u * 1.1; x0, y0, x1, y1 = min(x0, ox - r), min(y0, oy - r), max(x1, ox + r), max(y1, oy + r)
        rings = self._rings(ts, cam, layers)
        for rg in rings: r = rg["R"] + 6; x0, y0, x1, y1 = min(x0, rg["x"] - r), min(y0, rg["y"] - r), max(x1, rg["x"] + r), max(y1, rg["y"] + r)
        X0, Y0, X1, Y1 = max(0, int(x0)), max(0, int(y0)), min(W, int(x1) + 1), min(H, int(y1) + 1)
        if X1 <= X0 or Y1 <= Y0: return
        accA = np.zeros((Y1 - Y0, X1 - X0), np.float32); accC = np.zeros((Y1 - Y0, X1 - X0, 3), np.float32); wgt = 1.0 / len(layers)
        for L in layers:
            if L["vis"] < 0.004: continue
            ix, iy = int(np.floor(L["ox"])), int(np.floor(L["oy"])); fx, fy = L["ox"] - ix, L["oy"] - iy
            for kind, w in L["kinds"]:
                C, A, dx, dy = self._sprite(kind, L["u"] * L["bn"], L["phi"], fx, fy); self._add(accA, accC, C, A, ix + dx - X0, iy + dy - Y0, w * L["vis"] * wgt)
        wr = 1.0 / len(ts)
        for rg in rings: self._add_ring(accA, accC, rg, X0, Y0, wr)
        reg = img[Y0:Y1, X0:X1]; reg[:] = np.clip(reg.astype(np.float32) * (1 - accA[..., None]) + accC, 0, 255).astype(np.uint8)

    @staticmethod
    def _add(accA, accC, C, A, x, y, w):
        h, ww = A.shape; X0, Y0, X1, Y1 = max(0, x), max(0, y), min(accA.shape[1], x + ww), min(accA.shape[0], y + h)
        if X1 <= X0 or Y1 <= Y0 or w <= 0: return
        a = A[Y0 - y:Y1 - y, X0 - x:X1 - x]; cc = C[Y0 - y:Y1 - y, X0 - x:X1 - x]
        accA[Y0:Y1, X0:X1] += a * w; accC[Y0:Y1, X0:X1] += cc * w

    # ------------------------------------------------------------ anel do clique
    def _ring_active(self, t):
        return self.c["ring"] and any(0 <= t - k.tu < self.c["ring_dur"] for k in self.t.clicks)

    def _rings(self, ts, cam, layers):
        out = []
        if not self.c["ring"]: return out
        for tt, L in zip(ts, layers):
            for k in self.t.clicks:
                p = (tt - k.tu) / self.c["ring_dur"]
                if 0 <= p < 1:
                    e = 1 - (1 - p) ** 3; R = (2.0 + 9.0 * e) * L["u"]
                    out.append(dict(x=(k.x - L["vx"]) * L["k"], y=(k.y - L["vy"]) * L["k"], R=R, a=self.c["ring_alpha"] * (1 - p) ** 1.4,
                                    wd=max(2.0, 0.75 * L["u"] * (1 - 0.5 * p))))
        return out

    @staticmethod
    def _add_ring(accA, accC, rg, X0, Y0, w):
        h, ww = accA.shape; m = np.zeros((h, ww), np.uint8); sft = 4
        cxy = (int(round((rg["x"] - X0) * (1 << sft))), int(round((rg["y"] - Y0) * (1 << sft))))
        cv2.circle(m, cxy, int(round(rg["R"] * (1 << sft))), 255, max(1, int(round(rg["wd"]))), cv2.LINE_AA, sft)
        fill = np.zeros((h, ww), np.uint8); cv2.circle(fill, cxy, int(round(rg["R"] * (1 << sft))), 255, -1, cv2.LINE_AA, sft)
        a = (m.astype(np.float32) / 255 * rg["a"] + fill.astype(np.float32) / 255 * rg["a"] * 0.16) * w
        a = np.minimum(a, 0.9); accC += a[..., None] * GREEN; accA += a
