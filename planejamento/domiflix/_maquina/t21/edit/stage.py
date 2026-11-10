"""Palco claro + tela com cantos arredondados e sombra suave (mesma identidade do kit/render.py), com camera por janela
(cx, cy, vw). Desfoque de zoom/movimento = media de sub-quadros do transform, so nos quadros em movimento."""
import os, sys
import numpy as np, cv2

KIT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "kit")
sys.path.insert(0, KIT)
import ui  # noqa: E402  (palco, cantos, titulos: o mesmo do kit das aulas)
from camera import W, H

cv2.setNumThreads(2)


class Stage:
    def __init__(self, geom, shadow=0.20, bg=None, phone=None):
        self.g = geom; self.shadow = shadow; self._cache = {}
        # phone: {"bezel": 14, "color": [18,18,20], "rim": [62,62,66]} -> aparelho genérico (sem marca) em volta da tela
        self.phone = None if not phone else {"bezel": 14, "color": (18, 18, 20), "rim": (62, 62, 66), **(phone if isinstance(phone, dict) else {})}
        if bg:  # fundo em imagem (ex.: assets/fundo_escuro.png), no tamanho de saida
            im = cv2.imread(bg, cv2.IMREAD_COLOR); assert im is not None, bg
            self.bg = np.ascontiguousarray(cv2.cvtColor(cv2.resize(im, (W, H), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2RGB))
        else:
            self.bg = ui.stage_background(W, H)
        self.SW, self.SH = geom.SW, geom.SH

    # ------------------------------------------------------------ fundo com sombra
    def _bg(self, X0, Y0, X1, Y1, r):
        key = (round(X0, 1), round(Y0, 1), round(X1, 1), round(Y1, 1))
        if key in self._cache: return self._cache[key]
        tela = (X0, Y0, X1, Y1, r)
        if self.phone:  # a sombra e o corpo do aparelho ficam em volta da tela, na escala da câmera
            b = self.phone["bezel"] * r / max(1e-6, self.g.radius); X0, Y0, X1, Y1, r = X0 - b, Y0 - b, X1 + b, Y1 + b, r + b
        bx0, by0 = max(0, int(X0) - 110) // 4 * 4, max(0, int(Y0) - 90) // 4 * 4
        bx1, by1 = min(W, int(X1) + 114), min(H, int(Y1) + 134)
        bx1, by1 = min(W, -(-bx1 // 4) * 4), min(H, -(-by1 // 4) * 4)
        bg = self.bg.copy()
        if bx1 > bx0 and by1 > by0:
            lw, lh = (bx1 - bx0) // 4, (by1 - by0) // 4
            a, _ = ui.rrect_alpha(lw, lh, (X0 - bx0) / 4, (Y0 - by0 + 14) / 4, (X1 - bx0) / 4, (Y1 - by0 + 14) / 4, r / 4)
            a = cv2.GaussianBlur(a, (0, 0), 30 / 4); a = cv2.resize(a, (bx1 - bx0, by1 - by0), interpolation=cv2.INTER_LINEAR)
            m = np.clip(255 * (1 - a * self.shadow), 0, 255).astype(np.uint8)
            box = bg[by0:by1, bx0:bx1]; cv2.multiply(box, cv2.cvtColor(m, cv2.COLOR_GRAY2RGB), dst=box, scale=1 / 255)
        if self.phone: self._corpo(bg, X0, Y0, X1, Y1, r)
        if len(self._cache) > 3: self._cache.clear()
        self._cache[key] = bg
        return bg

    def _corpo(self, bg, X0, Y0, X1, Y1, r):
        """corpo do celular: retângulo arredondado escuro com um aro discreto (desenhado no fundo; a tela vai por cima)"""
        x0, y0, x1, y1 = max(0, int(np.floor(X0)) - 2), max(0, int(np.floor(Y0)) - 2), min(W, int(np.ceil(X1)) + 2), min(H, int(np.ceil(Y1)) + 2)
        if x1 <= x0 or y1 <= y0: return
        a, _ = ui.rrect_alpha(x1 - x0, y1 - y0, X0 - x0, Y0 - y0, X1 - x0, Y1 - y0, r)
        e = max(1.2, 2.2 * r / 60.0)  # largura do aro, na escala
        ai, _ = ui.rrect_alpha(x1 - x0, y1 - y0, X0 - x0 + e, Y0 - y0 + e, X1 - x0 - e, Y1 - y0 - e, max(1.0, r - e))
        box = bg[y0:y1, x0:x1].astype(np.float32)
        rim, cor = np.array(self.phone["rim"], np.float32), np.array(self.phone["color"], np.float32)
        box = box * (1 - a[..., None]) + rim * (a - ai)[..., None] + cor * ai[..., None]
        bg[y0:y1, x0:x1] = np.clip(box, 0, 255).astype(np.uint8)

    # ------------------------------------------------------------ um quadro, uma janela
    def _render(self, pre, view, lin=False):
        cx, cy, vw = view; g = self.g; k = W / vw; vx, vy = cx - vw / 2, cy - vw * H / W / 2
        rx, ry = pre.shape[1] / self.SW, pre.shape[0] / self.SH
        X0, Y0, X1, Y1 = -vx * k, -vy * k, (self.SW - vx) * k, (self.SH - vy) * k
        interp = cv2.INTER_CUBIC if (k / rx > 1.05 and not lin) else cv2.INTER_LINEAR
        if X0 <= 0.5 and Y0 <= 0.5 and X1 >= W - 0.5 and Y1 >= H - 0.5:
            M = np.array([[k / rx, 0, -vx * k], [0, k / ry, -vy * k]], np.float32)
            return cv2.warpAffine(pre, M, (W, H), flags=interp, borderMode=cv2.BORDER_REPLICATE), (0, 0, W, H)
        r = g.radius * k / g.k0
        rx0, ry0, rx1, ry1 = max(0, int(np.floor(X0))), max(0, int(np.floor(Y0))), min(W, int(np.ceil(X1))), min(H, int(np.ceil(Y1)))
        bgimg = self._bg(X0, Y0, X1, Y1, r); out = bgimg.copy()
        M = np.array([[k / rx, 0, -vx * k - rx0], [0, k / ry, -vy * k - ry0]], np.float32)
        out[ry0:ry1, rx0:rx1] = cv2.warpAffine(pre, M, (rx1 - rx0, ry1 - ry0), flags=interp, borderMode=cv2.BORDER_REPLICATE)
        c = int(np.ceil(r)) + 2
        # Celular: o canto arredondado (raio r) invade o quadro mesmo com a borda da tela já FORA dele (zoom entrando/saindo, deslizes,
        # desfoque de movimento): sem recortar o canto a tela aparecia com cantos retos por cima da moldura. `pad` estende a regra
        # "este lado da tela está dentro do quadro" pela largura do canto. Desktop: pad = 0 (idêntico ao T3 congelado).
        pad = c if self.phone else 0
        L, R, T, B = X0 > -pad, X1 < W + pad, Y0 > -pad, Y1 < H + pad; patches = []
        for (on, px, py, pw, ph) in (
                (L and T, rx0, ry0, c, c), (R and T, rx1 - c, ry0, c, c), (L and B, rx0, ry1 - c, c, c), (R and B, rx1 - c, ry1 - c, c, c),
                (T, rx0 + (c if L else 0), ry0, (rx1 - (c if R else 0)) - (rx0 + (c if L else 0)), 2),
                (B, rx0 + (c if L else 0), ry1 - 2, (rx1 - (c if R else 0)) - (rx0 + (c if L else 0)), 2),
                (L, rx0, ry0 + (c if T else 0), 2, (ry1 - (c if B else 0)) - (ry0 + (c if T else 0))),
                (R, rx1 - 2, ry0 + (c if T else 0), 2, (ry1 - (c if B else 0)) - (ry0 + (c if T else 0)))):
            if not on or pw <= 0 or ph <= 0: continue
            a, _ = ui.rrect_alpha(pw, ph, X0 - px, Y0 - py, X1 - px, Y1 - py, r); a = a[..., None]
            sl = out[py:py + ph, px:px + pw]
            sl[:] = (sl.astype(np.float32) * a + bgimg[py:py + ph, px:px + pw].astype(np.float32) * (1 - a)).astype(np.uint8)
        return out, (max(0, X0), max(0, Y0), min(W, X1), min(H, Y1))

    def _static(self, fr, view):
        """repouso exato do palco: reduz com INTER_AREA direto para o retangulo inteiro (texto nitido) e cola"""
        g = self.g; cx, cy, vw = view
        if abs(cx - self.SW / 2) > 0.05 or abs(cy - self.SH / 2) > 0.05 or abs(vw - g.vw0) > 0.05: return None
        if "static" not in self._cache:
            X0, Y0, X1, Y1 = g.x0, g.y0, g.x0 + g.w0, g.y0 + g.h0; r = g.radius
            bg = self._bg(X0, Y0, X1, Y1, r); c = int(np.ceil(r)) + 2
            a, _ = ui.rrect_alpha(g.w0, g.h0, 0, 0, g.w0, g.h0, r)
            self._cache["static"] = (bg, a[..., None], (X0, Y0, X1, Y1))
        bg, a, (X0, Y0, X1, Y1) = self._cache["static"]
        out = bg.copy(); x0, y0 = int(X0), int(Y0)
        c = cv2.resize(fr, (g.w0, g.h0), interpolation=cv2.INTER_AREA); r = int(np.ceil(g.radius)) + 2
        out[y0:y0 + g.h0, x0:x0 + g.w0] = c
        for ys, xs in ((slice(0, r), slice(0, r)), (slice(0, r), slice(g.w0 - r, g.w0)),
                       (slice(g.h0 - r, g.h0), slice(0, r)), (slice(g.h0 - r, g.h0), slice(g.w0 - r, g.w0))):
            oy, ox = slice(y0 + ys.start, y0 + ys.stop), slice(x0 + xs.start, x0 + xs.stop)
            out[oy, ox] = (c[ys, xs] * a[ys, xs] + bg[oy, ox] * (1 - a[ys, xs])).astype(np.uint8)
        return out, (X0, Y0, X1, Y1)

    def render(self, fr, views):
        """fr: quadro do video (H,W,3 uint8 RGB); views: lista de janelas (sub-quadros). Retorna (img, retangulo do conteudo)"""
        if len(views) == 1:
            s = self._static(fr, views[0])
            if s is not None: return s
        kmax = max(W / v[2] for v in views)
        if kmax < 0.75 and len(views) == 1:
            pre = cv2.resize(fr, (max(2, int(round(self.SW * kmax))), max(2, int(round(self.SH * kmax)))), interpolation=cv2.INTER_AREA)
        else:
            pre = fr
        if len(views) == 1:
            return self._render(pre, views[0])
        acc = np.zeros((H, W, 3), np.float32); crect = None
        for j, v in enumerate(views):
            img, cr = self._render(pre, v, True); cv2.accumulate(img, acc)
            if j == len(views) // 2: crect = cr
        return cv2.convertScaleAbs(acc, alpha=1.0 / len(views)), crect
