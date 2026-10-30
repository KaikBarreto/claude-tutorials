"""Plano de edição (EDL) da aula.
- Fala fica em 1x. Pausas curtas (< MIN_GAP) ficam como estão.
- Pausa longa com tela parada: corta, deixando um respiro.
- Pausa longa com tela mexendo (digitando, preenchendo, navegando): acelera (1.5x–8x, com selo na tela).
- edits.json (opcional, tempos da FONTE em s): cut [[s,e]], keep [[s,e]], speed [[s,e,x]], head, tail,
  zooms [{s,e,rect:[x,y,w,h]}], spots [{s,e,rect,label?}], chapters [{t,title,kicker?}], callouts [{s,e,text}].
uso: python3 kit/plan.py <projeto>  -> edl.json, legendas.srt"""
import json, os, sys
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt


def fill_gaps(on, n):
    """preenche buracos (False) menores que n amostras entre dois True (fechamento sem efeito de borda)"""
    on = np.asarray(on, bool).copy(); idx = np.flatnonzero(on)
    if len(idx) < 2: return on
    for a, b in zip(idx[:-1], idx[1:]):
        if 1 < b - a <= n: on[a:b] = True
    return on

proj = os.path.abspath(sys.argv[1]); P = lambda *a: os.path.join(proj, *a)
E = lambda k, d: float(os.environ.get(k, d))
PAD_PRE, PAD_POST = E("PAD_PRE", 0.10), E("PAD_POST", 0.15)
MIN_GAP = E("MIN_GAP", 0.55)       # pausa menor que isso fica intacta
KEEP_AFTER, KEEP_BEFORE = E("KEEP_AFTER", 0.12), E("KEEP_BEFORE", 0.14)  # respiro deixado ao cortar uma pausa
ACT_PX = E("ACT_PX", 8)            # px alterados (análise a 960 px) p/ contar como tela ativa
MIN_FAST = E("MIN_FAST", 1.4)      # trecho ativo menor que isso fica em 1x
MAX_SPEED = E("MAX_SPEED", 8)
NICE = np.array([1.5, 2, 3, 4, 6, 8, 10, 12, 16])
FPS = 30.0
q = lambda t: round(t * FPS) / FPS  # quantiza no quadro de 30 qps

meta = json.load(open(P("project.json"))); DUR = meta["dur"]
words = json.load(open(P("words.json")))
ed = json.load(open(P("edits.json"))) if os.path.exists(P("edits.json")) else {}
act = np.load(P("activity.npz")); at, apx = act["t"], act["px"]

# ---------------------------------------------------------------- fala: palavras do ASR refinadas pela energia
x, sr = sf.read(P("audio48k.wav"), dtype="float32")
x = sosfilt(butter(2, 90 / (sr / 2), "hp", output="sos"), x)
hop = int(0.01 * sr); n = len(x) // hop
db = 10 * np.log10((x[: n * hop].reshape(n, hop).astype(np.float64) ** 2).mean(1) + 1e-12)
floor, top = np.percentile(db, 10), np.percentile(db, 97)
thr = max(floor + 12, top - 32)
loud = db > thr
loud = fill_gaps(loud, 13)  # junta buracos < 0,12 s
regs = []; i = 0
while i < n:
    if loud[i]:
        j = i
        while j < n and loud[j]: j += 1
        if j - i >= 6: regs.append((i * 0.01, j * 0.01))
        i = j
    else: i += 1

VAD = json.load(open(P("vad.json"))) if os.path.exists(P("vad.json")) else []
in_vad = lambda w: any(w["e"] >= a - 0.3 and w["s"] <= b + 0.3 for a, b in VAD)  # palavra encosta num trecho de voz
spans = []
for w in (w for w in words if not in_vad(w)):
    s, e = w["s"] - PAD_PRE, w["e"] + PAD_POST
    for r0, r1 in regs:  # estende até o fim real da energia (o ASR encurta finais de palavra)
        if r0 <= w["e"] <= r1 + 0.05 and r1 - w["e"] < 0.45: e = max(e, r1 + 0.08)
        if r0 - 0.05 <= w["s"] <= r1 and w["s"] - r0 < 0.3: s = min(s, r0 - 0.05)
    spans.append([max(0.0, s), min(DUR, e)])
# trechos do detector de voz são fala (inclusive frases que o ASR deixou passar)
spans += [[max(0.0, a - PAD_PRE), min(DUR, b + PAD_POST)] for a, b in VAD]
spans.sort()
speech = []
for s, e in spans:
    if speech and s - speech[-1][1] < MIN_GAP: speech[-1][1] = max(speech[-1][1], e)
    else: speech.append([s, e])

# ---------------------------------------------------------------- cortes manuais, cabeça e cauda
head = float(ed.get("head", 0.0)); tail = float(ed.get("tail", min(DUR, (speech[-1][1] + 0.5) if speech else DUR)))
removed = [[0.0, head], [tail, DUR]] + [list(c) for c in ed.get("cut", [])]
keep_force = [list(k) for k in ed.get("keep", [])]
speed_force = [list(k) for k in ed.get("speed", [])]
inside = lambda t, L: any(a <= t < b for a, b, *_ in L)


def nice_speed(L):
    target = min(4.5, max(1.0, 0.8 + 0.16 * L))
    sp = L / target
    if sp < 1.4: return 1.0
    sp = NICE[np.argmin(np.abs(np.log(NICE) - np.log(sp)))]
    return float(min(sp, MAX_SPEED))


segs = []  # [src_s, src_e, speed, kind]
def add(s, e, sp, kind):
    s, e = q(s), q(e)
    if e - s < 1 / FPS: return
    segs.append([s, e, sp, kind])


def gap(g0, g1, lead, trail):
    """g0..g1 sem fala; lead/trail = há fala antes/depois"""
    L = g1 - g0
    if L < MIN_GAP and lead and trail: add(g0, g1, 1.0, "pausa"); return
    for a, b, sp in speed_force:
        if a <= g0 and g1 <= b: add(g0, g1, sp, "rapido"); return
    if any(a <= g0 and g1 <= b for a, b in keep_force): add(g0, g1, 1.0, "pausa"); return
    ka = KEEP_AFTER if lead else 0.0; kb = KEEP_BEFORE if trail else 0.0
    if ka: add(g0, g0 + ka, 1.0, "pausa")
    a0, a1 = g0 + ka, g1 - kb
    if a1 - a0 > 0.05:
        m = (at >= a0) & (at < a1); ts = at[m]; on = apx[m] > ACT_PX
        if len(on): on = fill_gaps(on, 16)  # junta rajadas de digitação (buracos < 1,5 s)
        i = 0; runs = []
        while i < len(on):
            j = i
            while j < len(on) and on[j] == on[i]: j += 1
            runs.append([bool(on[i]), ts[i], ts[j - 1] + 0.1 if j < len(on) else a1]); i = j
        if runs: runs[0][1] = a0
        for r in runs:
            ra, rb = r[1], min(r[2], a1)
            if rb - ra <= 0.02: continue
            if r[0] and rb - ra >= MIN_FAST:
                sp = nice_speed(rb - ra)
                add(ra, rb, sp, "rapido" if sp > 1 else "acao")
            elif r[0]:
                add(ra, rb, 1.0, "acao")
            elif lead and trail:
                # tela parada: corta (deixa 2 quadros p/ não "piscar" entre dois trechos acelerados)
                add(ra, ra + min(rb - ra, 2 / FPS), 1.0, "corte")
    if kb: add(g1 - kb, g1, 1.0, "pausa")


bounds = [[s, e] for s, e in speech]
t = 0.0
for k, (s, e) in enumerate(bounds):
    if s > t: gap(t, s, k > 0, True)
    add(s, e, 1.0, "fala"); t = e
if t < DUR: gap(t, DUR, True, False)

# remove o que foi cortado à mão / cabeça / cauda (recorta segmentos)
def subtract(segs, cuts):
    out = []
    for s, e, sp, kind in segs:
        parts = [[s, e]]
        for c0, c1 in cuts:
            nxt = []
            for a, b in parts:
                if c1 <= a or c0 >= b: nxt.append([a, b]); continue
                if a < c0: nxt.append([a, c0])
                if c1 < b: nxt.append([c1, b])
            parts = nxt
        out += [[q(a), q(b), sp, kind] for a, b in parts if q(b) - q(a) >= 1 / FPS]
    return out
segs = subtract(sorted(segs), removed)

# junta vizinhos contíguos com a mesma velocidade
merged = []
for s in segs:
    if merged and abs(merged[-1][1] - s[0]) < 1e-6 and merged[-1][2] == s[2]:
        merged[-1][1] = s[1]; merged[-1][3] = merged[-1][3] if merged[-1][3] == "fala" else s[3]
    else: merged.append(list(s))
segs = merged

# linha do tempo de saída
out_t = 0.0; S = []
for s, e, sp, kind in segs:
    d = (e - s) / sp; S.append({"src_s": round(s, 4), "src_e": round(e, 4), "speed": sp, "kind": kind,
                               "out_s": round(out_t, 4), "out_e": round(out_t + d, 4)}); out_t += d
OUT = out_t


def map_t(ts):
    for sg in S:
        if ts < sg["src_s"]: return sg["out_s"]
        if ts <= sg["src_e"]: return sg["out_s"] + (ts - sg["src_s"]) / sg["speed"]
    return OUT


mk = lambda L, ks: [dict(d, **{k + "_out": round(map_t(d[k]), 3) for k in ks}) for d in L]
edl = {"fps": FPS, "src_dur": DUR, "out_dur": round(OUT, 3), "segments": S,
       "zooms": mk(ed.get("zooms", []), ["s", "e"]), "spots": mk(ed.get("spots", []), ["s", "e"]),
       "chapters": mk(ed.get("chapters", []), ["t"]), "callouts": mk(ed.get("callouts", []), ["s", "e"]),
       "speech_thr_db": round(thr, 1), "noise_floor_db": round(floor, 1)}
json.dump(edl, open(P("edl.json"), "w"), ensure_ascii=False, indent=1)

# legendas (.srt) na linha do tempo editada (sem a vinheta; o render soma o deslocamento)
caps, cur = [], []
for i, w in enumerate(words):
    if inside(w["s"], removed): continue
    cur.append(w); txt = " ".join(c["w"] for c in cur)
    nxt = words[i + 1] if i + 1 < len(words) else None
    if nxt is None or len(txt) > 70 or w["w"][-1:] in ".?!" or (nxt["s"] - w["e"] > 0.6) or (w["e"] - cur[0]["s"] > 5.5):
        caps.append((map_t(cur[0]["s"]), map_t(w["e"]) + 0.15, txt)); cur = []
json.dump([{"s": round(a, 3), "e": round(b, 3), "text": c} for a, b, c in caps], open(P("captions.json"), "w"), ensure_ascii=False, indent=0)

# resumo
tot = lambda kind: sum((g["src_e"] - g["src_s"]) for g in S if g["kind"] == kind)
fast = [g for g in S if g["speed"] > 1]
print(f"fonte {DUR/60:.1f} min -> editado {OUT/60:.1f} min ({(1-OUT/DUR)*100:.0f}% menor)")
print(f"limiar de fala {thr:.1f} dB (ruído {floor:.1f} dB) | {len(speech)} blocos de fala | {len(S)} segmentos")
print(f"acelerados: {len(fast)} trechos, {sum(g['src_e']-g['src_s'] for g in fast):.0f}s de fonte -> {sum(g['out_e']-g['out_s'] for g in fast):.0f}s"
      f" | velocidades: {sorted(set(g['speed'] for g in fast))}")
print(f"cortado: {DUR - sum(g['src_e']-g['src_s'] for g in S):.0f}s de fonte")
