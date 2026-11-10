"""Camera estilo Recordly a partir da telemetria (padrao_video.md).
Zoom pelos cliques (grupos < 2,5 s; entra 0,5 s antes do 1o clique e sai 0,5 s depois do ultimo; 1,8x), mola critica
(entrada ~1,5 s, saida ~1,0 s, deslize ~1,0 s entre grupos separados por < 1,5 s), segue o cursor dentro do zoom e
mantem o alvo no quadro. Zooms manuais do JSON tem prioridade sobre os automaticos.
A camera e uma janela (cx, cy, vw) em px do video; vh = vw*H/W. zoom = vw0/vw (1 = palco inteiro).
v2 (Kaik 30/10 17:06/17:08, zoom no canto e "zooms um pouco perdidos"): a camera mira o ALVO da acao (campo digitado,
botao clicado, inclusive clique pelo teclado) e chega antes dele; mouse parado nao puxa a camera; zoom de cada grupo cabe
o maior alvo; e a checagem final (self.problemas) acusa qualquer alvo fora do quadro ou ancora no canto."""
import re
import numpy as np
from tele import RATE

FECHA = re.compile(r"^(fechar|cancelar|close|×|voltar)$", re.I)

W, H, FPS = 1920, 1080, 30
DEFAULTS = dict(auto=True, depth=1.8, lead=0.5, tail=0.5, group_gap=2.5, slide_gap=1.5, t_in=1.5, t_out=1.0, t_slide=1.0,
                follow=0.35, safe=0.62, guard=0.44, min_region=1.4, follow_tau=0.30, follow_t=2.2, keys_extend=True, key_gap=1.2,
                zeta=1.0, target_tau=0.10, shutter=0.5, blur_n=(6, 8),
                ant=0.5, t_move=0.8, dwell=0.6, pad=0.10, inner=0.80, min_zoom=1.2, act_speed=150.0, act_hold=0.4)


class Geom:
    """geometria do palco: o video em repouso fica inteiro, com margem, no quadro 1920x1080"""

    def __init__(self, SW, SH, margin=44, radius=16):
        self.SW, self.SH, self.margin, self.radius = SW, SH, margin, radius
        s0 = min((W - 2 * margin) / SW, (H - 2 * margin) / SH)
        self.w0, self.h0 = int(round(SW * s0)), int(round(SH * s0))
        self.x0, self.y0 = (W - self.w0) // 2, (H - self.h0) // 2
        self.k0 = self.w0 / SW; self.vw0 = W / self.k0


def clamp_axis(c, size, S, soft=30.0):
    """janela do centro da camera: pinado no meio com o palco inteiro, dentro do video com zoom. O limite e suavizado (softplus de ~30 px)
    para a camera nao ganhar um "tranco" de velocidade no instante em que a borda do video encosta na borda do quadro."""
    h = soft * np.logaddexp(0.0, (S - size) / 2 / soft)
    return S / 2 + np.clip(c - S / 2, -h, h)


def strength(c):
    """forca do clique: campo de texto (3) > menu/aba/link (2) > clique simples (1)"""
    tg, tag, role, ty = c.target, c.target.get("tag", ""), c.target.get("role", ""), c.target.get("type", "")
    if c.kind == 2 or tag in ("textarea", "select") or role in ("textbox", "combobox", "searchbox") or \
            (tag == "input" and ty not in ("button", "checkbox", "radio", "submit", "file")):
        return 3
    if role in ("menuitem", "menuitemcheckbox", "menuitemradio", "option", "tab", "treeitem") or tag == "a":
        return 2
    return 1


def anchor_of(c):
    if strength(c) == 3 and c.rect:
        r = c.rect; return 0.5 * c.x + 0.5 * (r["x"] + r["w"] / 2), r["y"] + r["h"] / 2
    return c.x, c.y


class Camera:
    def __init__(self, tele, geom, cur, T, dur, cfg=None, manual=()):
        self.cfg = c = {**DEFAULTS, **(cfg or {})}; self.g = g = geom; self.T, self.cur = T, cur; self.dur = dur
        self._tele_clicks = list(tele.clicks); self.focus = self._focus(tele)
        self.regions = self._auto(tele, dur) if c["auto"] else []
        self._man = self._manual(manual, cur); self.regions = self._merge(self.regions, self._man)
        self._simulate()

    # ------------------------------------------------------------ regioes
    def _focus(self, tele):
        """eventos com alvo, em ordem: clique do mouse (ponto/campo), clique pelo teclado e tecla digitada (retangulo do campo)"""
        ev = []
        for k in tele.clicks:
            ax, ay = anchor_of(k); ev.append(dict(t=k.td, x=ax, y=ay, rect=k.rect, src="clique", txt=(k.target or {}).get("text", "")))
        for t, r, tg in getattr(tele, "kbclicks", []):
            ev.append(dict(t=t, x=r["x"] + r["w"] / 2, y=r["y"] + r["h"] / 2, rect=r, src="enter", txt=(tg or {}).get("text", "")))
        for t, r, _ in getattr(tele, "keyfocus", []):
            ev.append(dict(t=t, x=r["x"] + r["w"] / 2, y=r["y"] + r["h"] / 2, rect=r, src="tecla"))
        return sorted(ev, key=lambda e: e["t"])

    def _anchor(self, e, vw, vh):
        """centro desejado para o alvo; campo mais largo/alto que 80% da vista mostra o comeco (onde o texto aparece)"""
        x, y, r = e["x"], e["y"], e["rect"]
        if r and r["w"] > 0.8 * vw: x = r["x"] + 0.4 * vw
        if r and r["h"] > 0.8 * vh: y = r["y"] + 0.4 * vh
        return float(x), float(y)

    def _inside(self, e, cx, cy, vw, vh, frac):
        g = self.g; cx = float(clamp_axis(np.array([cx]), vw, g.SW)[0]); cy = float(clamp_axis(np.array([cy]), vh, g.SH)[0])
        hw, hh = vw * frac / 2, vh * frac / 2; r = e["rect"]
        if r: return cx - hw <= r["x"] and r["x"] + r["w"] <= cx + hw and cy - hh <= r["y"] and r["y"] + r["h"] <= cy + hh
        return abs(e["x"] - cx) <= hw and abs(e["y"] - cy) <= hh

    def _auto(self, tele, dur):
        c = self.cfg; g = self.g; out = []; ev = self._focus(tele); self.focus = ev; groups = []
        for e in ev:
            if groups and e["t"] - groups[-1][-1]["t"] < c["group_gap"]: groups[-1].append(e)
            else: groups.append([e])
        for gp in groups:
            if len(gp) == 1 and gp[0]["src"] != "tecla" and FECHA.match((gp[0].get("txt") or "").strip()):
                continue  # clique isolado em Fechar/Cancelar: a tela muda em seguida, zoom ali ficaria olhando o vazio
            z = c["depth"]
            for e in gp:  # o zoom do grupo cabe o maior alvo com folga
                r = e["rect"]
                if r: z = min(z, g.vw0 / max(r["w"] * (1 + 2 * c["pad"]), r["h"] * (1 + 2 * c["pad"]) * W / H))
            if z < c["min_zoom"]: continue  # alvo grande demais: fica no palco inteiro
            vw = g.vw0 / z; vh = vw * H / W
            s = max(0.0, gp[0]["t"] - c["lead"]); e_ = max(gp[-1]["t"] + c["tail"], s + c["min_region"])
            ax, ay = self._anchor(gp[0], vw, vh); track = [(s, ax, ay)]; last = s
            for k in range(1, len(gp)):
                e = gp[k]
                if self._inside(e, ax, ay, vw, vh, c["inner"]): continue
                nx, ny = self._anchor(e, vw, vh)
                ant = c["ant"] + 0.35 * min(1.5, np.hypot(nx - ax, ny - ay) / vw)  # deslocamento grande: sai mais cedo
                t_sw = max(last + c["dwell"], gp[k - 1]["t"] + 0.1, e["t"] - ant)
                ax, ay = nx, ny; track.append((t_sw, ax, ay)); last = t_sw
            out.append(dict(s=s, e=e_, z=float(z), ax=track[0][1], ay=track[0][2], follow=c["follow"], src="auto", track=track))
        return out

    def _manual(self, zooms, cur):
        out = []; g = self.g
        for z in zooms:
            s = float(z["at"]); e = float(z["end"]) if "end" in z else s + float(z.get("dur", 3.0))
            sc, fol = z.get("scale"), z.get("follow")
            if "rect" in z:
                x, y, w, h = z["rect"]; ax, ay = x + w / 2, y + h / 2
                if sc is None:
                    pad = z.get("pad", 0.12); need = max(w * (1 + 2 * pad), h * (1 + 2 * pad) * W / H)
                    sc = float(np.clip(g.vw0 / need, 1.15, 3.5))
                fol = False if fol is None else fol
            elif "target" in z:
                ax, ay = z["target"]; fol = False if fol is None else fol
            else:
                k = int(np.clip(round(s * RATE), 0, len(cur) - 1)); ax, ay = cur[k]; fol = True if fol is None else fol
            out.append(dict(s=s, e=e, z=float(sc if sc is not None else self.cfg["depth"]), ax=float(ax), ay=float(ay),
                            follow=(self.cfg["follow"] if fol is True else float(fol or 0)), src="manual"))
        return out

    def _merge(self, auto, manual):
        """manual > auto: o automatico perde (ou encurta) o trecho coberto; depois liga grupos proximos (deslizar sem afastar)"""
        c = self.cfg; res = []
        for r in auto:
            r = dict(r); drop = False
            for m in manual:
                if r["e"] <= m["s"] - 0.3 or r["s"] >= m["e"] + 0.3: continue
                if r["s"] >= m["s"] - 0.3 and r["e"] <= m["e"] + 0.3: drop = True; break
                if r["s"] < m["s"] - 0.3 and r["e"] > m["e"] + 0.3: drop = True; break
                if r["s"] < m["s"]: r["e"] = m["s"] - 0.3
                else: r["s"] = m["e"] + 0.3
            if not drop and r["e"] - r["s"] >= 0.8: res.append(r)
        allr = sorted(res + [dict(m) for m in manual], key=lambda r: r["s"])
        for i in range(1, len(allr)):  # sobreposicao: o proximo comeca onde o anterior termina
            if allr[i]["s"] < allr[i - 1]["e"]: allr[i - 1]["e"] = allr[i]["s"]
            if allr[i]["s"] - allr[i - 1]["e"] < c["slide_gap"]: allr[i]["s"] = allr[i - 1]["e"]
        return [r for r in allr if r["e"] - r["s"] > 0.05]

    # ------------------------------------------------------------ simulacao da mola
    def _simulate(self):
        c, g, T, cur = self.cfg, self.g, self.T, self.cur; n = len(T); SW, SH = g.SW, g.SH
        zt = np.ones(n); ax = np.full(n, SW / 2); ay = np.full(n, SH / 2); fol = np.zeros(n); rid = np.zeros(n, int)
        for j, r in enumerate(self.regions, 1):
            i0, i1 = int(r["s"] * RATE), min(n, int(r["e"] * RATE))
            if i0 >= n: break
            zt[i0:i1] = r["z"]; ax[i0:i1] = r["ax"]; ay[i0:i1] = r["ay"]; fol[i0:i1] = r["follow"]; rid[i0:i1] = j
            for k, (ts, x_, y_) in enumerate(r.get("track") or []):  # ancora muda quando a acao muda de lugar
                a_ = max(i0, int(ts * RATE)) if k else i0
                b_ = min(i1, int(r["track"][k + 1][0] * RATE)) if k + 1 < len(r["track"]) else i1
                if b_ > a_: ax[a_:b_] = x_; ay[a_:b_] = y_
        zprev = np.concatenate([[1.0], zt[:-1]]); rprev = np.concatenate([[0], rid[:-1]])
        chg = (np.abs(zt - zprev) > 1e-9) | (np.abs(np.diff(ax, prepend=ax[0])) > 1e-9) | (np.abs(np.diff(ay, prepend=ay[0])) > 1e-9)
        w_of = lambda zp, zn, same: 4.74 / (c["t_out"] if zn == 1 else c["t_in"] if zp == 1 else c["t_move"] if same else c["t_slide"])
        wmark = np.zeros(n)
        for i in np.flatnonzero(chg): wmark[i] = w_of(zprev[i], zt[i], rid[i] == rprev[i] and rid[i] > 0)
        # atividade do mouse: so o mouse em movimento (ou clicando) puxa a camera; parado enquanto se digita, nao
        from scipy.ndimage import maximum_filter1d, gaussian_filter1d
        sp = np.hypot(*np.gradient(cur, 1.0 / RATE, axis=0).T); act = (sp > c["act_speed"]).astype(float)
        for k in getattr(self, "_tele_clicks", []): act[int(max(0, (k.td - 0.3) * RATE)):int((k.tu + 0.3) * RATE) + 1] = 1.0
        act = maximum_filter1d(act, int(2 * c["act_hold"] * RATE) + 1); act = np.clip(gaussian_filter1d(act, 0.12 * RATE), 0, 1)
        self.act = act; fol = fol * act
        cm = np.maximum.accumulate(np.where(wmark > 0, np.arange(n), 0))  # ultimo ponto de mudanca
        wv = np.where(wmark[cm] > 0, wmark[cm], 4.74 / c["t_slide"]); tsince = (np.arange(n) - cm) / RATE
        # centro desejado: ancora + parte do cursor, mantendo o cursor na caixa segura
        zdes = zt; vw_t = g.vw0 / zdes; vh_t = vw_t * H / W
        cl = self._lp(cur, c["follow_tau"])
        cdx = ax + fol * (cl[:, 0] - ax); cdy = ay + fol * (cl[:, 1] - ay)
        hw, hh = vw_t / 2 * c["safe"], vh_t / 2 * c["safe"]; on = fol > 0
        ex = (cl[:, 0] - cdx) - np.clip(cl[:, 0] - cdx, -hw, hw); ey = (cl[:, 1] - cdy) - np.clip(cl[:, 1] - cdy, -hh, hh)
        cdx = cdx + np.where(on, ex, 0) * act; cdy = cdy + np.where(on, ey, 0) * act
        cdx, cdy = clamp_axis(cdx, vw_t, SW), clamp_axis(cdy, vh_t, SH)
        sm = np.clip(tsince / 1.2, 0, 1); sm = sm * sm * (3 - 2 * sm); wc = wv + (c["follow_t"] - wv) * sm
        wc = np.where(fol > 0, wc, wv)
        lz = np.zeros(n); cx = np.zeros(n); cy = np.zeros(n); dt = 1.0 / RATE; zeta = c["zeta"]
        from scipy.signal import lfilter  # alvo suavizado (1a ordem): a aceleracao da mola nasce continua, sem "tranco" no inicio do movimento
        al = 1 - np.exp(-1 / (RATE * c["target_tau"])); sm1 = lambda x: lfilter([al], [1, -(1 - al)], x, zi=[x[0] * (1 - al)])[0]
        lzt = sm1(np.log(zt)).tolist(); wl, wcl, cxt, cyt = wv.tolist(), wc.tolist(), sm1(cdx).tolist(), sm1(cdy).tolist()
        z = vz = vx = vy = 0.0; x, y = SW / 2, SH / 2
        for k in range(n):
            w = wl[k]; vz += (w * w * (lzt[k] - z) - 2 * zeta * w * vz) * dt; z += vz * dt
            w = wcl[k]; vx += (w * w * (cxt[k] - x) - 2 * zeta * w * vx) * dt; x += vx * dt
            vy += (w * w * (cyt[k] - y) - 2 * zeta * w * vy) * dt; y += vy * dt
            lz[k], cx[k], cy[k] = z, x, y
        vw = g.vw0 * np.exp(-lz); vh = vw * H / W
        cx, cy = clamp_axis(cx, vw, SW), clamp_axis(cy, vh, SH)
        zoomed = (g.vw0 / vw) > 1.05  # garantia: o cursor nunca sai do quadro (margem minima)
        gx, gy = c["guard"] * vw, c["guard"] * vh
        cx = np.where(zoomed, cx + act * ((cur[:, 0] - cx) - np.clip(cur[:, 0] - cx, -gx, gx)), cx)
        cy = np.where(zoomed, cy + act * ((cur[:, 1] - cy) - np.clip(cur[:, 1] - cy, -gy, gy)), cy)
        self.cx, self.cy = clamp_axis(cx, vw, SW), clamp_axis(cy, vh, SH); self.vw = vw; self.zoom = g.vw0 / vw
        self._check()

    # ------------------------------------------------------------ checagem (nunca entregar alvo fora do quadro)
    def _vis(self, e, t):
        """(visivel, descentrado, zoom) do alvo do evento no instante t; alvo maior que a vista conta pelo ponto da acao"""
        cx, cy, vw = self.view(t); z = self.g.vw0 / vw; vh = vw * H / W; r = e["rect"]
        if not r or r["w"] > 0.8 * vw or r["h"] > 0.8 * vh: r = dict(x=e["x"] - 1, y=e["y"] - 1, w=2, h=2)
        ix = max(0.0, min(cx + vw / 2, r["x"] + r["w"]) - max(cx - vw / 2, r["x"]))
        iy = max(0.0, min(cy + vh / 2, r["y"] + r["h"]) - max(cy - vh / 2, r["y"]))
        desc = max(abs(r["x"] + r["w"] / 2 - cx) / (vw / 2), abs(r["y"] + r["h"] / 2 - cy) / (vh / 2))
        return ix * iy / (r["w"] * r["h"]), desc, z

    def _check(self, min_vis=0.9, max_desc=0.95):
        """alvo da acao inteiro no quadro: grosseiro 0,3 s depois (>= 50%) e assentado 0,6 s depois (>= 90%, longe da borda).
        Nao conta o evento logo antes de um zoom manual (o zoom do roteiro leva a camera para o resultado da acao)."""
        self.problemas = []
        for r in self.regions:
            for ts, x_, y_ in (r.get("track") or [(r["s"], r["ax"], r["ay"])]):
                if x_ < 40 or y_ < 40: self.problemas.append(f"t={ts:.2f} ancora no canto ({x_:.0f}, {y_:.0f})")
        man = [r["s"] for r in getattr(self, "_man", [])]  # inicio original do zoom do roteiro (antes de emendar)
        for e in getattr(self, "focus", []):
            if any(e["t"] - 0.2 <= m_ <= e["t"] + 1.0 for m_ in man): continue
            v3, _, z3 = self._vis(e, e["t"] + 0.3); v6, d6, z6 = self._vis(e, e["t"] + 0.6)
            if (z3 > 1.05 and v3 < 0.5) or (z6 > 1.05 and (v6 < min_vis or d6 > max_desc)):
                self.problemas.append(f"t={e['t']:.2f} {e['src']} visivel {v6:.0%} descentrado {d6:.2f} zoom {z6:.2f}")

    @staticmethod
    def _lp(x, tau):
        from scipy.ndimage import gaussian_filter1d
        return gaussian_filter1d(x, tau * RATE, axis=0, mode="nearest")

    # ------------------------------------------------------------ consulta
    def view(self, t):
        f = np.clip(t * RATE, 0, len(self.T) - 1.001); i = int(f); a = f - i
        lerp = lambda arr: arr[i] + (arr[i + 1] - arr[i]) * a
        return lerp(self.cx), lerp(self.cy), lerp(self.vw)

    def motion(self, t, shutter):
        """deslocamento (px de saida) do ponto mais afastado durante o obturador: decide se o quadro leva desfoque"""
        a, b = self.view(t - shutter / 2), self.view(t + shutter / 2); k = W / ((a[2] + b[2]) / 2)
        return max(abs(b[0] - a[0]) * k, abs(b[1] - a[1]) * k, abs(np.log(b[2] / a[2])) * W / 2 * 1.1)

    def n_samples(self, t, shutter):
        m = self.motion(t, shutter); lo, hi = self.cfg["blur_n"]
        return 1 if m < 1.2 else (4 if m < 4 else (lo if m < 10 else hi))  # 6 a 8 sub-quadros nos quadros em movimento; 4 no desfoque quase imperceptivel

    def zoom_in_times(self):
        return [r["s"] for r in self.regions if r["z"] > 1]
