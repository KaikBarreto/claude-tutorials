"""Passo final da aula: vinheta (com o titulo) + capitulos + cartela, e a trilha lo-fi com ducking sob a voz (kit/mix.py).
uso: python3 <tutorial>/edit/finish.py <aula.json> [--render] [--skip-brand] [--crf 20] [--formato 16x9|9x16]
  aula.json: {"title": "titulo da vinheta", "outro_line": "Ate a proxima aula!", "out": "out/aula",
              "chapters": ["cap1.chapter.json", ...],            # na ordem; cada um ja renderizado (ou use --render)
              "mix": {"music_db": -7, "music_duck_db": -8, "music_seed": 3}, "sfx": true,
              "formato": "16x9", "card_no_primeiro": false}      # formato: 9x16 = vertical 1080x1920 (docs/05-edicao.md, "Vertical 9:16")
Reaproveita do kit sem alterar: kit/brand_clips.sh (vinheta/cartela) e kit/mix.py (voz, trilha, ducking, SFX discretos).
Com --formato 9x16 (ou "formato" no JSON) so troca as pecas de imagem: kit/brand_clips_vertical.sh, vinheta_cap_vertical.py e
render_chapter_vertical.py; a voz, a trilha, o SFX e o mix.py sao os mesmos (mesmo som do 16:9). Sem a opcao, nada muda.
Monta um "projeto do kit" em <out>/proj (audio48k.wav = narracoes em sequencia, edl.json, render.json) e o mix.py roda em cima dele.
Saidas: <out>/aula_final.mp4 (H.264 yuv420p bt709 TV + AAC 192k) e <out>/proj/build/mix.wav. Sempre sob flock .heavy.lock + nice."""
import json, os, socket, subprocess, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.dont_write_bytecode = True
from common import ensure_heavy, probe, Reader, KIT, DOMI  # noqa: E402

argv = sys.argv[1:]; opt = lambda k, d=None: argv[argv.index(k) + 1] if k in argv else d
if "--help" in argv or not argv: print(__doc__); sys.exit(0)
ensure_heavy()
import soundfile as sf  # noqa: E402
from scipy.signal import butter, sosfilt  # noqa: E402
W, H, FPS, SR = 1920, 1080, 30, 48000
XF_IN, XF_OUT = 0.4, 0.5  # os mesmos do kit/render.py e kit/mix.py

LJ = os.path.abspath(argv[0]); BASE = os.path.dirname(LJ); L = json.load(open(LJ)); rp = lambda p: p if os.path.isabs(p) else os.path.normpath(os.path.join(BASE, p))
FORMATO = opt("--formato", L.get("formato", "16x9"))  # 9x16 = vertical (1080x1920): vinhetas, cartela e capitulos dos modulos *_vertical
if FORMATO not in ("16x9", "9x16"): sys.exit(f"formato {FORMATO!r}: use 16x9 (padrao) ou 9x16")
VERT = FORMATO == "9x16"
if VERT: import vertical as V; W, H = V.W, V.H  # noqa: E402,E702
OUT = rp(L.get("out", "out/aula")); PROJ = os.path.join(OUT, "proj"); BUILD = os.path.join(PROJ, "build"); os.makedirs(BUILD, exist_ok=True)
run = lambda cmd, **kw: subprocess.run(cmd, check=True, **kw)

# ---------------------------------------------------------------- capitulos (sidecar .edit.json do render_chapter)
chs = []
for cj in L["chapters"]:
    cj = rp(cj); ch = json.load(open(cj)); outd = os.path.normpath(os.path.join(os.path.dirname(cj), ch.get("output", {}).get("dir", "out")))
    name = ch.get("name") or os.path.splitext(os.path.basename(cj))[0].replace(".chapter", ""); side = os.path.join(outd, name + ".edit.json")
    if "--render" in argv or not os.path.exists(side):
        print(f"renderizando {name}...", flush=True); run([sys.executable, os.path.join(HERE, "render_chapter_vertical.py" if VERT else "render_chapter.py"), cj])
    s = json.load(open(side)); s["ch"] = ch; chs.append(s)
print(f"{len(chs)} capitulos, {sum(c['frames'] for c in chs) / FPS:.1f} s de conteudo")

# ---------------------------------------------------------------- cortes: trechos com a tela parada e sem fala (ex.: a pausa que sobrou
# de uma frase trocada por outra mais curta). "cortes": [[t0, t1], ...] no JSON do capitulo, em s do video do capitulo.
for c in chs:
    cut = c["ch"].get("cortes") or []
    if not cut: continue
    n0 = c["frames"]; keep = [i for i in range(n0) if not any(a_ <= i / FPS < b_ for a_, b_ in cut)]
    mp = lambda t, cut=cut: t - sum(min(max(t - a_, 0.0), b_ - a_) for a_, b_ in cut)
    c.update(keep=set(keep), frames_src=n0, frames=len(keep), cortes=cut)
    c["zoom_in"] = [mp(float(z)) for z in c.get("zoom_in", [])]
    c["callouts"] = [dict(k, at=mp(float(k["at"]))) for k in c.get("callouts", [])]
    c["spots"] = [dict(k, at=mp(float(k["at"]))) for k in c.get("spots", [])]
    print(f"{c['name']}: cortes {cut} -> {(n0 - len(keep)) / FPS:.2f} s a menos", flush=True)

# ---------------------------------------------------------------- vinhetas de capitulo (vinheta_cap.py): antes de cada capitulo com "card"
# (exceto o primeiro, que ja vem depois da vinheta da aula). Entram como itens da linha do tempo: video gerado aqui,
# voz em silencio, e o whoosh + pop do kit/mix.py pelo "title"/"title_at" (chapters[].t_out do edl).
if L.get("cards", True):
    if VERT: import vinheta_cap_vertical as VC  # noqa: E402,E701
    else: import vinheta_cap as VC  # noqa: E402,E701
    VOZES = json.load(open(rp(L["card_voices"]))) if L.get("card_voices") else {}  # {NN: {wav, dur}} (narracao/titulos.py)
    seq = []
    for i, c in enumerate(chs):
        cd = c["ch"].get("card")
        if cd and (i > 0 or L.get("card_no_primeiro")):  # card_no_primeiro: vinheta tambem no 1o capitulo (previas de um capitulo so)
            voz = VOZES.get(c["name"][-2:])
            dur = VC.dur_for(voz["dur"]) if voz else VC.DUR
            seq.append(dict(name="vinheta-" + c["name"], card=cd, frames=int(round(dur * FPS)), wav=None, video=None, voz=voz,
                            title=cd["title"], ch={"title_at": 0.30}, zoom_in=[], callouts=[], spots=[]))
        seq.append(c)
    chs = seq
    print(f"{sum(1 for c in chs if c.get('card'))} vinhetas de capitulo ({VC.DUR:.1f} s cada)")

# ---------------------------------------------------------------- voz: narracoes em sequencia + segmentos fala/pausa (como o plan.py)
starts, t = [], 0.0
for c in chs: starts.append(t); t += c["frames"] / FPS
CDUR = round(t, 3); energy = []
with sf.SoundFile(os.path.join(PROJ, "audio48k.wav"), "w", SR, 1, "FLOAT") as fo:
    for c in chs:
        n = c["frames"] * SR // FPS
        x = sf.read(c["wav"], dtype="float32")[0] if c.get("wav") else np.zeros(n, np.float32)
        if c.get("cortes") and c.get("wav"):
            tt = np.arange(len(x)) / SR; m_ = np.ones(len(x), bool)
            for a_, b_ in c["cortes"]: m_ &= ~((tt >= a_) & (tt < b_))
            x = x.mean(1) if x.ndim == 2 else x; x = x[m_]
        if c.get("voz"):
            v_, _ = sf.read(c["voz"]["wav"], dtype="float32"); v_ = v_.mean(1) if v_.ndim == 2 else v_
            a_ = int(VC.VOZ_AT * SR); x[a_:a_ + len(v_)] = v_[:max(0, n - a_)]
        x = x.mean(1) if x.ndim == 2 else x; x = np.pad(x, (0, max(0, n - len(x))))[:n]; fo.write(x)
        y = sosfilt(butter(2, 90 / (SR / 2), "hp", output="sos"), x); hop = SR // 100; m = len(y) // hop
        energy.append(10 * np.log10((y[:m * hop].reshape(m, hop).astype(np.float64) ** 2).mean(1) + 1e-12))
db = np.concatenate(energy); floor, top = np.percentile(db, 10), np.percentile(db, 97); thr = max(floor + 12, top - 32)
if top < -70: sys.exit("sem narracao em nenhum capitulo: nada para mixar (a trilha segue a voz)")
loud = db > thr; idx = np.flatnonzero(loud)
for a, b in zip(idx[:-1], idx[1:]):  # fecha buracos < 0,12 s
    if 1 < b - a <= 13: loud[a:b] = True
spans = []; i = 0
while i < len(loud):
    if loud[i]:
        j = i
        while j < len(loud) and loud[j]: j += 1
        if j - i >= 6: spans.append([max(0.0, i * 0.01 - 0.10), min(CDUR, j * 0.01 + 0.15)])
        i = j
    else: i += 1
speech = []
for s, e in spans:
    if speech and s - speech[-1][1] < 0.55: speech[-1][1] = max(speech[-1][1], e)
    else: speech.append([s, e])
segs = []; cur = 0.0; q = lambda v: round(v * FPS) / FPS
for s, e in speech + [[CDUR, CDUR]]:
    s, e = q(s), q(e)
    if s > cur: segs.append((cur, s, "pausa"))
    if e > s: segs.append((s, e, "fala"))
    cur = max(cur, e)
S = [dict(src_s=a, src_e=b, speed=1.0, kind=k, out_s=a, out_e=b) for a, b, k in segs if b > a]
sfx = L.get("sfx", True)
edl = dict(fps=FPS, src_dur=CDUR, out_dur=CDUR, segments=S, noise_floor_db=round(float(floor), 1), speech_thr_db=round(float(thr), 1),
           chapters=[dict(t_out=round(st + float(c["ch"].get("title_at", 0.5)), 3), title=c["title"]) for st, c in zip(starts, chs) if sfx and c.get("title")],
           zooms=[dict(s_out=round(st + z, 3)) for st, c in zip(starts, chs) for z in (c["zoom_in"] if sfx else [])],
           callouts=[dict(s_out=round(st + float(k["at"]), 3)) for st, c in zip(starts, chs) for k in (c["callouts"] if sfx else [])],
           spots=[dict(s_out=round(st + float(k["at"]), 3)) for st, c in zip(starts, chs) for k in (c["spots"] if sfx else [])])
json.dump(edl, open(os.path.join(PROJ, "edl.json"), "w"), ensure_ascii=False, indent=1)
json.dump(L.get("mix", {}), open(os.path.join(PROJ, "render.json"), "w"))
json.dump(dict(chapters=[dict(name=c["name"], start=s, dur=c["frames"] / FPS, cortes=c.get("cortes", []), voz=(c.get("voz") or {}).get("texto"))
                         for s, c in zip(starts, chs)]), open(os.path.join(OUT, "capitulos.json"), "w"), indent=1, ensure_ascii=False)
print(f"voz: {len(speech)} blocos de fala | limiar {thr:.1f} dB, piso {floor:.1f} dB", flush=True)

# ---------------------------------------------------------------- vinheta e cartela (kit/brand_clips.sh, com o servidor da pagina sob nosso controle)
if "--skip-brand" not in argv or not os.path.exists(os.path.join(BUILD, "intro_v.mp4")):
    sk = socket.socket(); sk.bind(("127.0.0.1", 0)); port = sk.getsockname()[1]; sk.close()
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1"], cwd=os.path.join(DOMI, "web"),
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1.2)
    try:
        run(["bash", os.path.join(KIT, "brand_clips_vertical.sh" if VERT else "brand_clips.sh"), PROJ, L.get("title", "Aula"), L.get("outro_line", "")], env={**os.environ, "PORT": str(port)})
    finally:
        srv.terminate(); srv.wait()

# ---------------------------------------------------------------- trilha + ducking + SFX (kit/mix.py)
run([sys.executable, os.path.join(KIT, "mix.py"), PROJ])
if any(c.get("card") for c in chs):  # Kaik 15:43: SFX tambem na saida da vinheta
    sys.path.insert(0, os.path.join(DOMI, "audio")); from kit import whoosh, pop, limit  # noqa: E402
    mw, _ = sf.read(os.path.join(BUILD, "mix.wav"), dtype="float64")
    t_in = probe(os.path.join(BUILD, "intro_v.mp4"))["dur"] if os.path.exists(os.path.join(BUILD, "intro_v.mp4")) else 0.0

    def put(sig, t, db):
        sig = np.asarray(sig, np.float64) * 10 ** (db / 20); sig = sig if sig.ndim == 2 else np.stack([sig, sig], 1)
        i_ = int(t * SR); n_ = min(len(sig), len(mw) - i_)
        if n_ > 0 and i_ >= 0: mw[i_:i_ + n_] += sig[:n_]

    for st, c in zip(starts, chs):  # vinheta de capitulo: whoosh na entrada, pop quando o titulo pousa, whoosh na saida
        if not c.get("card"): continue
        t0 = t_in + st
        put(whoosh(0.42, 500, 2600, 1.0, -0.3, seed=7), t0 + 0.02, -15)
        put(pop(79, 1.0), t0 + 0.52, -22)
        put(whoosh(0.45, 2600, 600, 1.0, 0.3, seed=9), t0 + c["frames"] / FPS - 0.62, -16)
    sf.write(os.path.join(BUILD, "mix.wav"), limit(mw, -1.0).astype(np.float32), SR, subtype="FLOAT")
    print("SFX das vinhetas de capitulo: ok", flush=True)

# ---------------------------------------------------------------- video: vinheta + capitulos + cartela (mesmos fundidos do kit/render.py)
intro_p, outro_p = os.path.join(BUILD, "intro_v.mp4"), os.path.join(BUILD, "outro_v.mp4")
n_in, n_out = int(round(probe(intro_p)["dur"] * FPS)), int(round(probe(outro_p)["dur"] * FPS)); n_c = sum(c["frames"] for c in chs); n_xo = int(round(XF_OUT * FPS))
total = n_in + n_c + n_out - n_xo; crf = opt("--crf", L.get("crf", 20)); vid = os.path.join(OUT, "video_sem_audio.mp4")
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                        "-vf", "scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p", "-c:v", "libx264", "-preset", "veryfast",
                        "-crf", str(crf), "-g", "60", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
                        "-movflags", "+faststart", vid], stdin=subprocess.PIPE)
r_in, r_out = Reader(intro_p, W, H, explicit=False), Reader(outro_p, W, H, explicit=False); last_intro = None; t0 = time.time(); f = 0
for _ in range(n_in):
    last_intro = np.array(r_in.next()); enc.stdin.write(last_intro.tobytes()); f += 1
c_idx = 0; last_img = last_intro; BGI = None
for k, c in enumerate(chs):
    if c.get("card"):
        import cv2  # noqa: E402
        if BGI is None:
            bgp = next((x["ch"].get("stage", {}).get("bg") for x in chs if x["ch"].get("stage", {}).get("bg")), None)
            BGI = cv2.cvtColor(cv2.imread(bgp), cv2.COLOR_BGR2RGB) if bgp else np.zeros((H, W, 3), np.uint8)
        rn = Reader(chs[k + 1]["video"], W, H, explicit=False); first = np.array(rn.next()); rn.close()
        card = VC.Card(c["card"].get("kicker", ""), c["card"]["title"], BGI, dur=c["frames"] / FPS); prev = last_img if last_img is not None else first
        for fi in range(c["frames"]):
            img = card.frame(fi / FPS, prev, first)
            enc.stdin.write(np.ascontiguousarray(img).tobytes()); c_idx += 1; f += 1
        continue
    rd = Reader(c["video"], W, H, explicit=False)  # o MP4 do capitulo ja carrega bt709/TV
    keep = c.get("keep"); src_i = -1
    for _ in range(c["frames"]):
        img = rd.next(); src_i += 1
        while keep is not None and src_i not in keep: img = rd.next(); src_i += 1
        last_img = np.array(img)
        if last_intro is not None and c_idx < int(round(XF_IN * FPS)):
            p = c_idx / (XF_IN * FPS); img = (img.astype(np.float32) * p + last_intro.astype(np.float32) * (1 - p)).astype(np.uint8)
        if n_out and c_idx >= n_c - n_xo:
            o = r_out.next(); p = (c_idx - (n_c - n_xo) + 1) / (n_xo + 1); img = (img.astype(np.float32) * (1 - p) + o.astype(np.float32) * p).astype(np.uint8)
        enc.stdin.write(np.ascontiguousarray(img).tobytes()); c_idx += 1; f += 1
        if f % 150 == 0: print(f"\r{f}/{total} quadros  {f / (time.time() - t0):.1f} q/s", end="", flush=True)
    rd.close()
for _ in range(n_out - n_xo):
    enc.stdin.write(np.ascontiguousarray(r_out.next()).tobytes()); f += 1
enc.stdin.close(); enc.wait(); r_in.close(); r_out.close()
final = os.path.join(OUT, "aula_final.mp4")
run(["ffmpeg", "-v", "error", "-y", "-i", vid, "-i", os.path.join(BUILD, "mix.wav"), "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
     "-ar", "48000", "-ac", "2", "-shortest", "-movflags", "+faststart", final])
pr = probe(final); print(f"\nok {final}  ({pr['dur']:.1f} s; esperado {total / FPS:.1f} s; {f} quadros; {(time.time() - t0) / 60:.1f} min)")
