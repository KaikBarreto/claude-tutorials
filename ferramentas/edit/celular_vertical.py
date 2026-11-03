"""Capítulo vertical 9:16 a partir da gravação do CELULAR (viewport 390x844, "device": "phone"): sem moldura de aparelho.
A tela é recortada na área que a fala cita e ampliada 2,4x (390 px CSS -> 936 px) numa janela dentro do painel claro
(formato_9x16.json, "tela_real": x 72, y 240, 936x1160, acima da faixa da legenda do player). Reaproveita camera.py, cursor.py e
overlay.py SEM alterá-los: carrega cópias privadas deles com o quadro da janela (936x1160) no lugar do 16:9 (1920x1080), então a
câmera v2 (alvos do actions.json e da telemetria), o anel do toque e os destaques/avisos são os mesmos do 16:9.
Câmera do vertical: só desliza para o alvo (zoom 1 = largura inteira da tela = 2,4x); o que o 16:9 amplia, aqui já vem ampliado.
  - "zooms" do capítulo: mesmos tempos e alvos (rect/target); "scale9" (>= 1) opcional aprofunda um zoom só no vertical;
  - entre dois alvos a câmera FICA onde estava (não volta ao centro da tela); "camera_9x16": {...} ajusta a câmera só do vertical;
  - alvo da ação fora da janela = erro (como no 16:9; --aceitar-camera, com motivo, para renderizar mesmo assim)."""
import importlib.util
import os
import sys

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import camera as _camera16  # noqa: E402,F401  (os originais do 16:9 entram primeiro e ficam como estão)
import stage as _stage16  # noqa: E402,F401
from stage import ui  # noqa: E402
from tele import RATE, Tele  # noqa: E402
import vertical as V  # noqa: E402

TX, TY, TW, TH, TR = V.TELA_X, V.TELA_Y, V.TELA_W, V.TELA_H, V.TELA_R


def modulos_da_janela(w=TW, h=TH):
    """cópias privadas de camera, cursor e overlay com o quadro w x h (os módulos do 16:9 não são tocados)"""
    nomes = ("camera", "cursor", "overlay")
    salvos = {n: sys.modules.get(n) for n in nomes}
    mods = {}
    try:
        for n in nomes:
            sys.modules.pop(n, None)
        for n in nomes:
            spec = importlib.util.spec_from_file_location(n, os.path.join(HERE, n + ".py"))
            m = importlib.util.module_from_spec(spec)
            sys.modules[n] = m
            spec.loader.exec_module(m)
            if n == "camera":
                m.W, m.H = w, h  # antes de cursor/overlay fazerem `from camera import W, H`
            mods[n] = m
    finally:
        for n, m in salvos.items():
            if m is None:
                sys.modules.pop(n, None)
            else:
                sys.modules[n] = m
    return mods


def base_do_quadro(bg_png):
    """palco escuro vertical + painel claro 1008x1700 em (36,110) com a sombra do 16:9 (sigma 30, +14 px, 0,35)"""
    im = cv2.imread(bg_png, cv2.IMREAD_COLOR)
    assert im is not None and im.shape[:2] == (V.H, V.W), f"{bg_png}: esperado o palco vertical {V.W}x{V.H} (fundo_escuro_vertical.py)"
    bg = cv2.cvtColor(im, cv2.COLOR_BGR2RGB).astype(np.float32)
    sh, _ = ui.rrect_alpha(V.W, V.H, V.PX, V.PY + 14, V.PX + V.PW, V.PY + V.PH + 14, V.PR)
    sh = cv2.GaussianBlur(sh, (0, 0), 30)
    bg *= (1 - sh * V.PSOMBRA)[..., None]
    pw, ph = V.PW, V.PH  # painel: branco com os dois brilhos verdes discretos do painel das cenas (cenas_modelo_vertical.html)
    yy, xx = np.mgrid[0:ph, 0:pw].astype(np.float32)
    pan = np.full((ph, pw, 3), 255, np.float32)
    for cx, cy, rx, ry, a in ((0.92 * pw, -0.08 * ph, 900, 700, 0.075), (-0.12 * pw, 1.08 * ph, 800, 700, 0.05)):
        d = np.sqrt(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2)
        al = a * np.clip(1 - d / 0.62, 0, 1)
        pan = pan * (1 - al[..., None]) + np.array([0, 197, 151], np.float32) * al[..., None]
    m, _ = ui.rrect_alpha(pw, ph, 0, 0, pw, ph, V.PR)
    reg = bg[V.PY:V.PY + ph, V.PX:V.PX + pw]
    bg[V.PY:V.PY + ph, V.PX:V.PX + pw] = reg * (1 - m[..., None]) + pan * m[..., None]
    return np.ascontiguousarray(np.clip(bg, 0, 255).astype(np.uint8))


class CapituloCelular:
    """contexto de um capítulo com tela do celular: telemetria, câmera, anel do toque, destaques; compõe o quadro 1080x1920"""

    def __init__(self, ch, rp, video, SW, SH, dur, t0, t1):
        self.ch, self.SW, self.SH, self.dur, self.t0, self.t1 = ch, SW, SH, dur, t0, t1
        M = modulos_da_janela(); cam_m, cur_m, ov_m = M["camera"], M["cursor"], M["overlay"]
        self.FPS = V.FPS
        self.tele = Tele(rp(ch["telemetry"]), dur); self.T = np.arange(int((dur + 3) * RATE)) / RATE
        ccfg = {"show": False, "touch": True, "ring_alpha": 0.7, **ch.get("cursor", {})}  # só o anel do toque (como no T7)
        self.cur = self.tele.path(self.T, ccfg.get("smooth", 0.67))
        vp = self.tele.raw["video"].get("viewportCss", {}); ccfg.setdefault("dpr", SW / vp["width"] if vp.get("width") else 2.0)
        g = self.geom = cam_m.Geom(SW, SH, 0, 0)
        g.k0 = TW / SW; g.vw0 = float(SW)  # zoom 1 = a largura inteira da tela na janela (390 px CSS -> 936 px = 2,4x)
        zooms = []
        for z in ch.get("zooms", []):
            z = dict(z); z["scale"] = float(z.pop("scale9", 1.0)); zooms.append(z)  # o escala do 16:9 não vale aqui
        # o vertical só desliza (viagens de ~700 px entre o topo e o pé da tela): chega antes (lead) e com a mola mais rápida que a do 16:9
        cfg = {**ch.get("camera", {}), "depth": 1.0, "min_zoom": 1.0, "lead": 0.8, "t_out": 0.75, "t_slide": 0.75, "t_move": 0.6,
               **ch.get("camera_9x16", {})}
        self.cam = cam_m.Camera(self.tele, g, self.cur, self.T, dur, cfg, zooms)
        self._segurar(dur)
        self.problemas = list(getattr(self.cam, "problemas", [])) + self._fora_da_janela()
        self.cursor = cur_m.CursorLayer(self.tele, g, self.T, self.cur, ccfg)
        self.ov = ov_m.Overlays({**ch, "title": None, "illustrations": []}, os.path.dirname(rp(ch["video"])))
        self.shut = self.cam.cfg["shutter"] / self.FPS
        bg = rp(ch.get("stage", {}).get("bg")) or os.path.join(HERE, "assets", "fundo_escuro_9x16.png")
        self.base = base_do_quadro(bg)
        a, _ = ui.rrect_alpha(TW, TH, 0, 0, TW, TH, TR); self.mask = a[..., None]
        ring, _ = ui.rrect_alpha(TW + 8, TH + 8, 3, 3, TW + 5, TH + 5, TR + 2)
        inner, _ = ui.rrect_alpha(TW + 8, TH + 8, 5, 5, TW + 3, TH + 3, TR)
        self.fio = (ring - inner)[..., None] * 0.16  # fio discreto na borda da tela (não é moldura de aparelho)

    def _segurar(self, dur):
        """entre dois alvos (e depois do último) a câmera fica onde estava, em vez de voltar ao centro da tela"""
        regs = sorted(self.cam.regions, key=lambda r: r["s"]); out = []
        for i, r in enumerate(regs):
            out.append(r); nxt = regs[i + 1]["s"] if i + 1 < len(regs) else dur + 3
            if nxt - r["e"] > 0.05:
                ax, ay = r["track"][-1][1:] if r.get("track") else (r["ax"], r["ay"])
                out.append(dict(s=r["e"], e=nxt, z=r["z"], ax=ax, ay=ay, follow=0.0, src="hold"))
        self.cam.regions = out; self.cam._simulate()

    def _fora_da_janela(self):
        """alvo da ação (retângulo do toque/campo) que não cabe na janela de 936x1160 depois que a câmera assentou"""
        cam = self.cam; man = [r["s"] for r in getattr(cam, "_man", [])]; out = []
        for e in getattr(cam, "focus", []):
            if any(e["t"] - 0.2 <= m <= e["t"] + 1.0 for m in man):
                continue
            v6, d6, _ = cam._vis(e, e["t"] + 0.6)
            if v6 < 0.9 or d6 > 0.95:
                out.append(f"t={e['t']:.2f} {e['src']} visível {v6:.0%} descentrado {d6:.2f} (fora da janela do celular)")
        return out

    def _warp(self, fr, view):
        cx, cy, vw = view; k = TW / vw; vx, vy = cx - vw / 2, cy - vw * TH / TW / 2
        M = np.array([[k, 0, -vx * k], [0, k, -vy * k]], np.float32)
        return cv2.warpAffine(fr, M, (TW, TH), flags=cv2.INTER_CUBIC if k > 1.05 else cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)

    def compose(self, t, fr):
        cam = self.cam; n = cam.n_samples(t, self.shut)
        if n == 1:
            win = self._warp(fr, cam.view(t))
        else:
            ts = [t + (j / (n - 1) - 0.5) * self.shut for j in range(n)]; acc = np.zeros((TH, TW, 3), np.float32)
            for tt in ts:
                cv2.accumulate(self._warp(fr, cam.view(tt)), acc)
            win = cv2.convertScaleAbs(acc, alpha=1.0 / n)
        win = np.ascontiguousarray(win)
        self.cursor.draw(win, t, cam, self.shut); self.ov.over(win, t, (0, 0, TW, TH), cam.view(t))
        img = self.base.copy(); reg = img[TY:TY + TH, TX:TX + TW].astype(np.float32)
        reg = reg * (1 - self.mask) + win.astype(np.float32) * self.mask
        img[TY:TY + TH, TX:TX + TW] = np.clip(reg, 0, 255).astype(np.uint8)
        fy, fx = TY - 3, TX - 3; r2 = img[fy:fy + TH + 8, fx:fx + TW + 8].astype(np.float32)
        img[fy:fy + TH + 8, fx:fx + TW + 8] = (r2 * (1 - self.fio)).astype(np.uint8)
        return img, n

    def zoom_in(self):
        return [round(r["s"] - self.t0, 3) for r in self.cam.regions if r.get("src") != "hold" and self.t0 <= r["s"] < self.t1]

    def regioes(self):
        return [{k: ([[round(float(a), 3) for a in tr] for tr in v] if k == "track" else round(float(v), 3) if not isinstance(v, str) else v)
                 for k, v in r.items()} for r in self.cam.regions if r.get("src") != "hold"]
