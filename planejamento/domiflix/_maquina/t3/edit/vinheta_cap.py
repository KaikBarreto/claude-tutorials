"""Vinheta de capítulo do T3 (pedido do Kaik, 30/10 15:12): cobre a tela do computador (a janela do app no palco) com
o título grande em Montserrat, a área em cima (sem número de etapa), entra e sai com fusão. ≥3,2 s, mesma animação
em todos os capítulos; a voz lê o título em VOZ_AT; whoosh + pop na entrada (kit/mix.py) e whoosh na saída (finish.py).
Uso como módulo (finish.py): Card(kicker, title, bg).frame(t, prev, nxt) -> RGB uint8.
Prévia: python3 vinheta_cap.py <saida.mp4> "<área>" "<título>" <quadro_antes.png> <quadro_depois.png>"""
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "kit"))
import ui  # noqa: E402

W, H, FPS = 1920, 1080, 30
DUR = 3.2          # duração mínima (Kaik 15:43: "levemente mais durável")
VOZ_AT = 0.70      # a voz lê o título depois do pop


def dur_for(voz_s):
    """duração da vinheta para caber o título falado + respiro + saída"""
    return round(max(DUR, VOZ_AT + voz_s + 0.35 + 0.50), 2)
WX, WY, WW, WH, WR = 166, 44, 1587, 992, 16  # janela do app em repouso (Geom com margem 44)
VERDE = (0, 197, 151)


def ease(t):
    t = float(np.clip(t, 0, 1))
    return t * t * (3 - 2 * t)


def out_cubic(t):
    t = float(np.clip(t, 0, 1))
    return 1 - (1 - t) ** 3


def texto(txt, w, size, cor, track=0):
    f = ui.font(w, size)
    if track:
        larg = sum(f.getlength(ch) for ch in txt) + track * (len(txt) - 1)
    else:
        larg = f.getlength(txt)
    asc, desc = f.getmetrics()
    im = Image.new("RGBA", (int(larg) + 8, asc + desc + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if track:
        x = 4
        for ch in txt:
            d.text((x, 4), ch, font=f, fill=cor)
            x += f.getlength(ch) + track
    else:
        d.text((4, 4), txt, font=f, fill=cor)
    return np.array(im)


def quebra(txt, w, size, maxw):
    f = ui.font(w, size)
    linhas, cur = [], ""
    for p in txt.split():
        t = (cur + " " + p).strip()
        if f.getlength(t) <= maxw or not cur:
            cur = t
        else:
            linhas.append(cur)
            cur = p
    linhas.append(cur)
    return linhas


def cola(img, spr, x, y, alpha=1.0):
    h, w = spr.shape[:2]
    x, y = int(round(x)), int(round(y))
    x0, y0, x1, y1 = max(0, x), max(0, y), min(img.shape[1], x + w), min(img.shape[0], y + h)
    if x1 <= x0 or y1 <= y0 or alpha <= 0:
        return
    s = spr[y0 - y:y1 - y, x0 - x:x1 - x].astype(np.float32)
    a = s[..., 3:4] / 255.0 * alpha
    reg = img[y0:y1, x0:x1].astype(np.float32)
    img[y0:y1, x0:x1] = (reg * (1 - a) + s[..., :3] * a).astype(np.uint8)


class Card:
    def __init__(self, kicker, title, bg, dur=DUR):
        self.dur = dur
        bg = bg.astype(np.float32)
        # palco com a sombra da janela
        a, _ = ui.rrect_alpha(W, H, WX, WY + 14, WX + WW, WY + WH + 14, WR)
        a = cv2.GaussianBlur(a, (0, 0), 30)
        base = bg * (1 - 0.35 * a)[..., None]
        # "tela do computador": o próprio fundo, desfocado e escurecido, com luz verde suave no canto
        inner = cv2.GaussianBlur(bg, (0, 0), 28) * 0.42 + 6
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        g = np.exp(-(((xx - WX) / 700.0) ** 2 + ((yy - (WY + WH)) / 520.0) ** 2))
        inner += np.array(VERDE, np.float32) * (0.16 * g)[..., None]
        inner += np.random.default_rng(3).normal(0, 2.2, (H, W, 1)).astype(np.float32)
        m, _ = ui.rrect_alpha(W, H, WX, WY, WX + WW, WY + WH, WR)
        self.base = np.clip(base * (1 - m[..., None]) + inner * m[..., None], 0, 255).astype(np.uint8)
        # textos
        self.kick = texto(kicker.upper(), 700, 34, VERDE + (255,), track=7) if kicker else None
        size = 112
        linhas = quebra(title, 800, size, WW - 330)
        if len(linhas) > 2:
            size = 92
            linhas = quebra(title, 800, size, WW - 330)
        self.tit = [texto(l, 800, size, (243, 244, 246, 255)) for l in linhas]
        lh = int(size * 1.12)
        kh = 34 + 26 if self.kick is not None else 0
        bloco = kh + lh * len(self.tit)
        self.x = WX + 150
        self.y0 = WY + WH / 2 - bloco / 2 - 6
        self.kh, self.lh, self.bloco = kh, lh, bloco

    def conteudo(self, t):
        img = self.base.copy()
        # barra verde vertical à esquerda do bloco (cresce de cima para baixo)
        bh = int(self.bloco * out_cubic((t - 0.16) / 0.40))
        if bh > 0:
            cv2.rectangle(img, (self.x - 40, int(self.y0) + 6), (self.x - 33, int(self.y0) + 6 + bh), VERDE, -1)
        sai = ease((t - (self.dur - 0.52)) / 0.22)
        if self.kick is not None:
            k = out_cubic((t - 0.22) / 0.33)
            cola(img, self.kick, self.x - 4, self.y0 + 16 * (1 - k) - 10 * sai, k * (1 - sai))
        for i, sp in enumerate(self.tit):
            k = out_cubic((t - 0.30 - 0.06 * i) / 0.45)
            cola(img, sp, self.x - 6, self.y0 + self.kh + i * self.lh - 10 + 34 * (1 - k) - 12 * sai, k * (1 - sai))
        return img

    def frame(self, t, prev, nxt):
        c = self.conteudo(t).astype(np.float32)
        a_in = ease(t / 0.40)
        a_out = ease((t - (self.dur - 0.50)) / 0.50)
        out = prev.astype(np.float32) * (1 - a_in) + c * a_in
        out = out * (1 - a_out) + nxt.astype(np.float32) * a_out
        return np.clip(out, 0, 255).astype(np.uint8)


if __name__ == "__main__":
    out, kicker, title, f0, f1 = sys.argv[1:6]
    bg = cv2.cvtColor(cv2.imread(os.path.join(HERE, "assets", "fundo_escuro.png")), cv2.COLOR_BGR2RGB)
    prev = cv2.cvtColor(cv2.imread(f0), cv2.COLOR_BGR2RGB)
    nxt = cv2.cvtColor(cv2.imread(f1), cv2.COLOR_BGR2RGB)
    C = Card(kicker, title, bg)
    n = int(round(DUR * FPS))
    pre, pos = int(0.8 * FPS), int(1.0 * FPS)
    enc = cv2.VideoWriter(out + ".tmp.mp4", cv2.VideoWriter_fourcc(*"mp4v"), FPS, (W, H))
    for _ in range(pre):
        enc.write(cv2.cvtColor(prev, cv2.COLOR_RGB2BGR))
    for i in range(n):
        enc.write(cv2.cvtColor(C.frame(i / FPS, prev, nxt), cv2.COLOR_RGB2BGR))
    for _ in range(pos):
        enc.write(cv2.cvtColor(nxt, cv2.COLOR_RGB2BGR))
    enc.release()
    print("ok", out + ".tmp.mp4", (pre + n + pos) / FPS, "s")
