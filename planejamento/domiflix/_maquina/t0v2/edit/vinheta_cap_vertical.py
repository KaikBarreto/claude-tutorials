"""Vinheta de capítulo do formato vertical 9:16 (1080x1920): a mesma animação, o mesmo tempo (DUR, VOZ_AT, dur_for), a mesma
fusão e o mesmo som da vinheta do 16:9 (vinheta_cap.py, congelada), recompostos para o celular (storyboard_9x16 do T0 v2):
cobre o painel (a "tela" do celular, 1008x1700 em (36, 110)) com a área em letras maiúsculas espaçadas (44 px) e o título
grande (Montserrat 800, 112 px em até 3 linhas; menor só se não couber) à direita de uma barra no acento, barra em x = 72,
bloco no meio da altura e acima da faixa da legenda do player. Margem lateral 72 px; nada nos 180 px de cima e de baixo.
Reaproveita de vinheta_cap.py (sem alterá-lo) as constantes e as funções de texto: o 16:9 não muda.
Uso como módulo (finish.py --formato 9x16): Card(kicker, title, bg, dur).frame(t, prev, nxt) -> RGB uint8 1080x1920.
Prévias: python3 vinheta_cap_vertical.py <saida.mp4> "<área>" "<título>" <quadro_antes.png> <quadro_depois.png>
         python3 vinheta_cap_vertical.py --stills <pasta> "<área>" "<título>" 0.8,1.6,2.6   (PNGs; fundo cinza antes/depois)
         (as duas aceitam --palco <png 1080x1920>; padrão assets/fundo_escuro_9x16.png)"""
import os
import sys

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
import vertical as V  # noqa: E402
import vinheta_cap as VC  # noqa: E402  (o 16:9: só se LÊ dele)

ui = VC.ui
W, H, FPS = V.W, V.H, V.FPS
DUR, VOZ_AT, dur_for = VC.DUR, VC.VOZ_AT, VC.dur_for  # a mesma duração e a mesma hora da voz do 16:9
ease, out_cubic, texto, quebra, cola = VC.ease, VC.out_cubic, VC.texto, VC.quebra, VC.cola
PX, PY, PW, PH = V.PAINEL
PR = V.PR
ACENTO = ui.ACCENT

BARRA_X, BARRA_L, FOLGA = 72, 10, 34          # barra à esquerda (x 72); texto 34 px depois dela
TX = BARRA_X + BARRA_L + FOLGA                # início do texto: 116
MAXW = V.SEGURA[2] - TX                       # largura do título: até a margem direita segura (1008)
KICK_PX, KICK_TRACK = 44, 9                   # área: maiúsculas espaçadas (texto mínimo do vertical: 44 px)
TITULO_PX = (112, 96, 80, 68, 56, 48, 44)     # o maior que cabe em até 3 linhas
MAX_LINHAS = 3
CENTRO_Y = 926                                # centro do bloco (um pouco acima do meio, como no storyboard)


def _largura(sprite):
    return sprite.shape[1] - 8                # o sprite de texto() tem 4 px de folga de cada lado


class Card:
    def __init__(self, kicker, title, bg, dur=DUR):
        assert bg.shape[:2] == (H, W), f"o palco do vertical deve ter {W}x{H} (assets/fundo_escuro_9x16.png), veio {bg.shape[1]}x{bg.shape[0]}"
        self.dur = dur
        bg = bg.astype(np.float32)
        # palco com a sombra do painel (a mesma conta do 16:9: deslocada 14 px, desfoque 30, 0,35)
        a, _ = ui.rrect_alpha(W, H, PX, PY + 14, PX + PW, PY + PH + 14, PR)
        a = cv2.GaussianBlur(a, (0, 0), 30)
        base = bg * (1 - V.PSOMBRA * a)[..., None]
        # "tela do celular": o próprio fundo, desfocado e escurecido, com luz suave no acento no canto de baixo à esquerda
        inner = cv2.GaussianBlur(bg, (0, 0), 28) * 0.42 + 6
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        g = np.exp(-(((xx - PX) / 640.0) ** 2 + ((yy - (PY + PH)) / 780.0) ** 2))
        inner += np.array(ACENTO, np.float32) * (0.16 * g)[..., None]
        inner += np.random.default_rng(3).normal(0, 2.2, (H, W, 1)).astype(np.float32)
        m, _ = ui.rrect_alpha(W, H, PX, PY, PX + PW, PY + PH, PR)
        self.base = np.clip(base * (1 - m[..., None]) + inner * m[..., None], 0, 255).astype(np.uint8)
        # textos: área (maiúsculas espaçadas, no acento legível) e título (até 3 linhas; reduz só se não couber)
        track = KICK_TRACK
        self.kick = texto(kicker.upper(), 700, KICK_PX, ui.ACCENT_TEXT + (255,), track=track) if kicker else None
        while self.kick is not None and _largura(self.kick) > MAXW and track > 2:
            track -= 2
            self.kick = texto(kicker.upper(), 700, KICK_PX, ui.ACCENT_TEXT + (255,), track=track)
        size, linhas = TITULO_PX[-1], [title]
        for s in TITULO_PX:
            ls = quebra(title, 800, s, MAXW)
            size, linhas = s, ls
            if len(ls) <= MAX_LINHAS and max(ui.font(800, s).getlength(l) for l in ls) <= MAXW:
                break
        self.tit = [texto(l, 800, size, ui.LIGHT + (255,)) for l in linhas]
        self.size = size
        lh = int(size * 1.12)
        kh = KICK_PX + 34 if self.kick is not None else 0
        bloco = kh + lh * len(self.tit)
        self.x = TX
        self.y0 = CENTRO_Y - bloco / 2
        self.kh, self.lh, self.bloco = kh, lh, bloco

    def caixas(self):
        """caixas (x0, y0, x1, y1) de cada linha de texto, em repouso, em px do quadro (para conferir a área segura)"""
        out = []
        if self.kick is not None:
            out.append((self.x, self.y0 + 4, self.x + _largura(self.kick), self.y0 + self.kick.shape[0] - 4))
        for i, sp in enumerate(self.tit):
            y = self.y0 + self.kh + i * self.lh - 10
            out.append((self.x, y + 4, self.x + _largura(sp), y + sp.shape[0] - 4))
        out.append((BARRA_X, self.y0 + 6, BARRA_X + BARRA_L, self.y0 + 6 + self.bloco))
        return out

    def conteudo(self, t):
        img = self.base.copy()
        # barra vertical no acento à esquerda do bloco (cresce de cima para baixo)
        bh = int(self.bloco * out_cubic((t - 0.16) / 0.40))
        if bh > 0:
            cv2.rectangle(img, (BARRA_X, int(self.y0) + 6), (BARRA_X + BARRA_L - 1, int(self.y0) + 6 + bh), ACENTO, -1)
        sai = ease((t - (self.dur - 0.52)) / 0.22)
        if self.kick is not None:
            k = out_cubic((t - 0.22) / 0.33)
            cola(img, self.kick, self.x - 4, self.y0 + 20 * (1 - k) - 14 * sai, k * (1 - sai))
        for i, sp in enumerate(self.tit):
            k = out_cubic((t - 0.30 - 0.06 * i) / 0.45)
            cola(img, sp, self.x - 6, self.y0 + self.kh + i * self.lh - 10 + 44 * (1 - k) - 16 * sai, k * (1 - sai))
        return img

    def frame(self, t, prev, nxt):
        c = self.conteudo(t).astype(np.float32)
        a_in = ease(t / 0.40)
        a_out = ease((t - (self.dur - 0.50)) / 0.50)
        out = prev.astype(np.float32) * (1 - a_in) + c * a_in
        out = out * (1 - a_out) + nxt.astype(np.float32) * a_out
        return np.clip(out, 0, 255).astype(np.uint8)


def _bg(p=None):
    p = p or os.path.join(HERE, "assets", "fundo_escuro_9x16.png")
    im = cv2.imread(p)
    if im is None:
        sys.exit(f"falta {p}: rode python3 fundo_escuro_vertical.py")
    return cv2.cvtColor(im, cv2.COLOR_BGR2RGB)


if __name__ == "__main__":
    a = sys.argv[1:]
    palco = None
    if "--palco" in a:  # --palco <png>: outro palco 1080x1920 (padrão: assets/fundo_escuro_9x16.png)
        i = a.index("--palco")
        palco = a[i + 1]
        del a[i:i + 2]
    if a and a[0] == "--stills":
        pasta, kicker, title, ts = a[1:5]
        os.makedirs(pasta, exist_ok=True)
        C = Card(kicker, title, _bg(palco), dur=dur_for(1.64))
        cinza = np.full((H, W, 3), 128, np.uint8)
        for t in map(float, ts.split(",")):
            cv2.imwrite(os.path.join(pasta, f"card_v_{t:05.2f}.png"), cv2.cvtColor(C.frame(t, cinza, cinza), cv2.COLOR_RGB2BGR))
        for cx in C.caixas():
            lados = V.caixa_fora_da_segura(cx)
            print("caixa", tuple(round(v) for v in cx), "ok" if not lados else "FORA DA ÁREA SEGURA: " + ", ".join(lados))
        sys.exit(0)
    out, kicker, title, f0, f1 = a[:5]
    prev = cv2.cvtColor(cv2.imread(f0), cv2.COLOR_BGR2RGB)
    nxt = cv2.cvtColor(cv2.imread(f1), cv2.COLOR_BGR2RGB)
    C = Card(kicker, title, _bg(palco))
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
