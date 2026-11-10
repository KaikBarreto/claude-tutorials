"""Telemetria do gravador (rec/README.md): caminho do mouse, cliques, teclas e tipo de cursor.
Tempos em s desde o 1o quadro do video; posicoes em px do video (2560x1600)."""
import json
import numpy as np
from scipy.ndimage import gaussian_filter1d

RATE = 240  # Hz da grade densa (camera e cursor)
KINDS = {"arrow": 0, "pointer": 1, "text": 2}
# teclas que não dizem onde a ação está (só navegam ou modificam)
MOD = {"Shift", "Control", "Alt", "Meta", "Tab", "Shift+Tab", "Escape", "CapsLock"}


def ponto_ok(s, vw, vh):
    """posição do mouse confiável: (0, 0) vem de clique disparado pelo teclado (Enter/Espaço num botão) e de teclas
    copiadas depois dele; ponto fora do vídeo também não serve (Kaik 30/10: zoom e cursor foram para o canto)"""
    x, y = s.get("x"), s.get("y")
    return x is not None and y is not None and not (x == 0 and y == 0) and 0 < x < vw and 0 < y < vh


def rect_ok(r, vw, vh):
    """retângulo do alvo utilizável: com área e pelo menos metade dentro do vídeo"""
    if not r or r.get("w", 0) <= 1 or r.get("h", 0) <= 1: return False
    ix = max(0.0, min(vw, r["x"] + r["w"]) - max(0.0, r["x"])); iy = max(0.0, min(vh, r["y"] + r["h"]) - max(0.0, r["y"]))
    return ix * iy >= 0.5 * r["w"] * r["h"]


class Click:
    __slots__ = ("td", "tu", "x", "y", "button", "rect", "target", "kind")

    def __init__(self, td, tu, x, y, button, rect, target, kind):
        self.td, self.tu, self.x, self.y, self.button, self.rect, self.target, self.kind = td, tu, x, y, button, rect, target, kind

    @property
    def t(self):
        return self.tu


class Tele:
    def __init__(self, path, dur=None):
        d = json.load(open(path)); self.raw = d
        self.vw, self.vh = d["video"]["width"], d["video"]["height"]
        S = d["samples"]; self.dur = dur or d["video"].get("durationS", 0)
        pts = sorted(((s["t"], s["x"], s["y"]) for s in S if ponto_ok(s, self.vw, self.vh)), key=lambda p: p[0])
        self.P = np.array(pts, np.float64)
        mv = [s for s in S if s["type"] == "move"]
        self.kt = np.array([s["t"] for s in mv]); self.kk = np.array([KINDS.get(s.get("cursor", "arrow"), 0) for s in mv])
        self.keys = np.array(sorted(s["t"] for s in S if s["type"] == "key"))
        self.scrolls = np.array(sorted(s["t"] for s in S if s["type"] == "scroll"))
        downs = [s for s in S if s["type"] == "down"]; ups = [s for s in S if s["type"] in ("up", "click")]
        cl = [s for s in S if s["type"] == "click"]; self.clicks = []; self.kbclicks = []
        for c in cl:
            dn = [s for s in downs if s["button"] == c["button"] and s["t"] <= c["t"] + 1e-6 and c["t"] - s["t"] < 1.0]
            td = dn[-1]["t"] if dn else c["t"] - 0.11
            x_, y_, r_ = c.get("x"), c.get("y"), c.get("rect")
            if c.get("kb") or (x_ == 0 and y_ == 0):  # clique pelo teclado: o mouse não foi lá (sem cursor, sem anel); a câmera usa o alvo
                if rect_ok(r_, self.vw, self.vh): self.kbclicks.append((c["t"], r_, c.get("target") or {}))
                continue
            if x_ is None or y_ is None:  # clique sintetico (ex.: checkbox marcado pelo robo) vem sem ponto: usa o centro do alvo
                if not r_: continue
                x_, y_ = r_["x"] + r_["w"] / 2, r_["y"] + r_["h"] / 2
            self.clicks.append(Click(td, c["t"], x_, y_, c.get("button", 0), r_, c.get("target") or {}, self.kind_at(c["t"])))
        self.clicks.sort(key=lambda c: c.tu)
        # foco da digitação: tecla que escreve/confirma num elemento (o retângulo é o do campo com o foco)
        self.keyfocus = sorted(((s["t"], s["rect"], s.get("target") or {}) for s in S if s["type"] == "key"
                                and s.get("key") not in MOD and rect_ok(s.get("rect"), self.vw, self.vh)), key=lambda e: e[0])

    def kind_at(self, t):
        i = int(np.searchsorted(self.kt, t, "right")) - 1
        return int(self.kk[i]) if i >= 0 else 0

    def kind_series(self, tt):
        i = np.clip(np.searchsorted(self.kt, tt, "right") - 1, 0, max(len(self.kk) - 1, 0))
        return self.kk[i] if len(self.kk) else np.zeros(len(tt), int)

    # ------------------------------------------------------------ caminho do mouse
    def path(self, T, smooth=0.67, hold_gap=0.2, glide=0.12):
        """posicao (n,2) na grade densa. Lacuna sem amostras = mouse parado (segura e desliza no fim).
        Suavizacao de fase zero (sem atraso) e o clique fica exatamente sob a ponta."""
        P = self.P
        if P.ndim != 2 or len(P) == 0:  # sem mouse (celular, capítulo ilustrado): cursor parado no centro, invisível
            return np.tile(np.array([[self.vw / 2.0, self.vh / 2.0]]), (len(T), 1))
        t, x, y = [P[0, 0]], [P[0, 1]], [P[0, 2]]
        for k in range(1, len(P)):
            ta, tb = P[k - 1, 0], P[k, 0]
            if tb - ta > hold_gap:
                g = min(glide, tb - ta); t.append(tb - g); x.append(P[k - 1, 1]); y.append(P[k - 1, 2])
            t.append(tb); x.append(P[k, 1]); y.append(P[k, 2])
        t = np.array(t); t = t + np.arange(len(t)) * 1e-9
        X = np.stack([np.interp(T, t, x), np.interp(T, t, y)], 1)
        sig = 0.10 * (smooth / 0.67) * RATE
        if sig > 0.3:
            X = gaussian_filter1d(X, sig, axis=0, mode="nearest")
        for c in self.clicks:  # cola a ponta no ponto do clique
            a, b = c.td - 0.04, c.tu + 0.04; ramp = 0.25
            w = np.clip(np.minimum((T - (a - ramp)) / ramp, ((b + ramp) - T) / ramp), 0, 1)
            if w.max() <= 0: continue
            k = int(np.clip(round(c.td * RATE), 0, len(T) - 1)); d = np.array([c.x, c.y]) - X[k]
            X = X + w[:, None] * d[None, :]
        return X
