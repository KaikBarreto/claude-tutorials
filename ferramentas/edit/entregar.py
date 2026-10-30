"""Confere e prepara a entrega da aula final.
uso: python3 -I entregar.py <out_da_aula> "<Nome do arquivo>" [--partes cap04,cap08] [--max-mib 29]
- specs (ffprobe), loudness integrado e pico real do áudio final;
- folha de quadros (vinheta, início, cada vinheta de capítulo, ilustração, cartela) em <out>/conferencia.jpg;
- cópia com nome amigável + legendas (.srt/.vtt) com o mesmo nome;
- partes cortadas nas vinhetas de capítulo indicadas, cada uma até --max-mib (limite do envio no chat),
  com as legendas de cada parte no relógio dela.
Pesado (reencode das partes): rode sob flock .heavy.lock. --so-legendas refaz só as legendas (aula e partes), sem reencode; --refazer 3 reencoda só a parte 3."""
import json, os, re, subprocess, sys

argv = sys.argv[1:]; opt = lambda k, d=None: argv[argv.index(k) + 1] if k in argv else d
OUT = os.path.abspath(argv[0]); NOME = argv[1]
FINAL = os.path.join(OUT, "aula_final.mp4"); CAPJ = os.path.join(OUT, "capitulos.json")
INTRO = os.path.join(OUT, "proj", "build", "intro_v.mp4"); LEG = os.path.join(OUT, "legendas", "aula_final")
MAXB = float(opt("--max-mib", 29)) * 1024 * 1024
ENT = os.path.join(OUT, "entrega"); os.makedirs(ENT, exist_ok=True); SO_LEG = "--so-legendas" in argv
REF = {int(x) for x in (opt("--refazer") or "").split(",") if x}  # só reencoda estas partes (ex.: 3)


def sh(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)


def dur(f):
    return float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).stdout)


# ------------------------------------------------------------------ specs e loudness
pr = json.loads(sh(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", FINAL]).stdout)
v = next(s for s in pr["streams"] if s["codec_type"] == "video"); a = next(s for s in pr["streams"] if s["codec_type"] == "audio")
D = float(pr["format"]["duration"]); T_IN = dur(INTRO)
print(f"final: {D:.2f} s ({int(D // 60)}:{D % 60:04.1f}) | {v['width']}x{v['height']} {v['r_frame_rate']} {v['codec_name']} {v['pix_fmt']} "
      f"{v.get('color_primaries', '?')}/{v.get('color_transfer', '?')}/{v.get('color_space', '?')} {v.get('color_range', '?')} | "
      f"{a['codec_name']} {a['sample_rate']} Hz {a['channels']} ch | {int(pr['format']['size']) / 2**20:.1f} MiB "
      f"({int(pr['format']['bit_rate']) / 1e6:.2f} Mb/s)")
ld = "" if SO_LEG else subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", FINAL, "-map", "0:a", "-af", "ebur128=peak=true", "-f", "null", "-"],
                    capture_output=True, text=True).stderr
I = re.findall(r"I:\s+(-?[\d.]+) LUFS", ld); TP = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", ld)
print(f"áudio: {I[-1] if I else '?'} LUFS integrado | pico real {TP[-1] if TP else '?'} dBTP")

# ------------------------------------------------------------------ folha de quadros
caps = json.load(open(CAPJ))["chapters"]
marks = [(1.6, "vinheta"), (T_IN + 3.0, "início")]
for c in caps:
    if c["name"].startswith("vinheta-"): marks.append((T_IN + c["start"] + 1.8, c["name"].replace("vinheta-", "vinheta ")))
    if c["name"] == "cap10":  # ilustração do QR (40,62 s do capítulo, menos o corte anterior a ela)
        cut = sum(e - s for s, e in (c.get("cortes") or []) if e <= 40.62)
        marks += [(T_IN + c["start"] + 40.62 - cut + 2.5, "ilustração 1"), (T_IN + c["start"] + 40.62 - cut + 6.5, "ilustração 2")]
marks.append((D - 1.6, "cartela"))
tmp = os.path.join(ENT, "_q"); os.makedirs(tmp, exist_ok=True)
for i, (t, _) in enumerate([] if SO_LEG else marks):
    sh(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", FINAL, "-frames:v", "1", "-vf", "scale=480:-2", os.path.join(tmp, f"{i:02d}.jpg")])
from PIL import Image, ImageDraw  # noqa: E402
ims = [] if SO_LEG else [Image.open(os.path.join(tmp, f"{i:02d}.jpg")) for i in range(len(marks))]
cols = 4; w, h = ims[0].size if ims else (480, 270); rows = (len(ims) + cols - 1) // cols
sheet = Image.new("RGB", (cols * w, rows * (h + 22)), "white"); d = ImageDraw.Draw(sheet)
from PIL import ImageFont  # noqa: E402
FT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "kit", "fonts", "Montserrat-600.ttf")
font = ImageFont.truetype(FT, 13) if os.path.exists(FT) else None  # a fonte padrão do PIL não tem acentos
for i, (im, (t, lab)) in enumerate(zip(ims, marks)):
    x, y = (i % cols) * w, (i // cols) * (h + 22); sheet.paste(im, (x, y + 22)); d.text((x + 6, y + 4), f"{int(t // 60)}:{t % 60:04.1f}  {lab}", fill="black", font=font)
SO_LEG or sheet.save(os.path.join(OUT, "conferencia.jpg"), quality=88); SO_LEG or print("folha:", os.path.join(OUT, "conferencia.jpg"))

# ------------------------------------------------------------------ cópia com nome + legendas
full = os.path.join(ENT, NOME + ".mp4")
if not os.path.exists(full) or os.path.getmtime(full) < os.path.getmtime(FINAL):
    sh(["cp", FINAL, full])
for ext in ("srt", "vtt"):
    sh(["cp", f"{LEG}.{ext}", os.path.join(ENT, f"{NOME}.{ext}")])


# ------------------------------------------------------------------ partes (cada uma cabe no envio)
def ts(t, sep):
    ms = int(round(max(0.0, t) * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d}{sep}{ms % 1000:03d}"


def parse_srt(p):
    out = []
    for b in open(p, encoding="utf-8").read().strip().split("\n\n"):
        ln = b.split("\n"); m = re.match(r"(\S+) --> (\S+)", ln[1])
        tt = [sum(float(x) * k for x, k in zip(s.replace(",", ".").split(":"), (3600, 60, 1))) for s in m.groups()]
        out.append((tt[0], tt[1], "\n".join(ln[2:])))
    return out


partes = opt("--partes")
if partes:
    nomes = partes.split(","); cuts = [0.0]
    for n in nomes:
        c = next(c for c in caps if c["name"] == "vinheta-" + n); cuts.append(T_IN + c["start"])
    cuts.append(D); subs = parse_srt(LEG + ".srt")
    for k in range(len(cuts) - 1):
        s0, s1 = cuts[k], cuts[k + 1]; base = os.path.join(ENT, f"{NOME} - parte {k + 1} de {len(cuts) - 1}")
        pula = SO_LEG or (REF and k + 1 not in REF)
        # CRF 23 com teto de taxa (VBV): uma passada só e o tamanho não passa do limite; cenas simples ficam abaixo do teto
        for frac in () if pula else (0.95, 0.86, 0.78):
            vmax = int((MAXB * 8 * frac - 128e3 * (s1 - s0)) / (s1 - s0)); tmpf = base + ".tmp.mp4"
            sh(["nice", "-n", "10", "ffmpeg", "-y", "-v", "error", "-ss", f"{s0:.3f}", "-i", FINAL, "-t", f"{s1 - s0:.3f}",
                "-c:v", "libx264", "-preset", "medium", "-crf", "23", "-maxrate", str(vmax), "-bufsize", str(2 * vmax),
                "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv",
                "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", tmpf])
            sz = os.path.getsize(tmpf)
            if sz <= MAXB:
                os.replace(tmpf, base + ".mp4")
                print(f"parte {k + 1}: {s0:.1f}-{s1:.1f} s, crf 23 teto {vmax / 1e3:.0f} kb/s, {sz / 2**20:.1f} MiB", flush=True); break
            print(f"parte {k + 1}: teto {vmax / 1e3:.0f} kb/s deu {sz / 2**20:.1f} MiB, tentando mais leve", flush=True)
        else:
            if not pula: raise SystemExit(f"parte {k + 1} não coube em {MAXB / 2**20:.0f} MiB")
        sel = [(max(a_, s0) - s0, min(b_, s1) - s0, tx) for a_, b_, tx in subs if b_ > s0 + 0.05 and a_ < s1 - 0.05]
        with open(base + ".srt", "w", encoding="utf-8") as f:
            for i, (a_, b_, tx) in enumerate(sel, 1): f.write(f"{i}\n{ts(a_, ',')} --> {ts(b_, ',')}\n{tx}\n\n")
        with open(base + ".vtt", "w", encoding="utf-8") as f:
            f.write("WEBVTT\n\n")
            for a_, b_, tx in sel: f.write(f"{ts(a_, '.')} --> {ts(b_, '.')}\n{tx}\n\n")
if "--unico" in argv and not SO_LEG:
    # a aula inteira num arquivo só que cabe no envio do chat (Kaik 30/10 17:03: "junte tudo num vídeo só"):
    # 720p, duas passadas no tamanho exato, AAC 80k, legendas embutidas (faixa mov_text, desligada por padrão)
    alvo = os.path.join(ENT, f"{NOME} (720p).mp4"); A_KB = 80; pl = os.path.join(ENT, "_2pass")
    for frac in (0.965, 0.93, 0.89):
        vbr = int((MAXB * 8 * frac - A_KB * 1e3 * D) / D); tmpf = alvo + ".tmp.mp4"
        comum = ["-vf", "scale=1280:720:flags=lanczos", "-c:v", "libx264", "-preset", "medium", "-b:v", str(vbr), "-g", "300",
                 "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                 "-color_range", "tv", "-passlogfile", pl]
        sh(["nice", "-n", "10", "ffmpeg", "-y", "-v", "error", "-i", FINAL, *comum, "-pass", "1", "-an", "-f", "null", "/dev/null"])
        sh(["nice", "-n", "10", "ffmpeg", "-y", "-v", "error", "-i", FINAL, "-i", LEG + ".srt", "-map", "0:v", "-map", "0:a", "-map", "1:s",
            *comum, "-pass", "2", "-c:a", "aac", "-b:a", f"{A_KB}k", "-c:s", "mov_text", "-metadata:s:s:0", "language=por",
            "-metadata:s:s:0", "title=Português", "-disposition:s:0", "0", "-movflags", "+faststart", tmpf])
        sz = os.path.getsize(tmpf)
        if sz <= MAXB:
            os.replace(tmpf, alvo); print(f"único 720p: vídeo {vbr / 1e3:.0f} kb/s + áudio {A_KB} kb/s, {sz / 2**20:.1f} MiB -> {alvo}", flush=True); break
        print(f"único 720p: {vbr / 1e3:.0f} kb/s deu {sz / 2**20:.1f} MiB, tentando menor", flush=True)
    else:
        raise SystemExit(f"o vídeo único não coube em {MAXB / 2**20:.0f} MiB")
    for ext in ("srt", "vtt"):
        sh(["cp", f"{LEG}.{ext}", os.path.join(ENT, f"{NOME} (720p).{ext}")])
    for f_ in os.listdir(ENT):
        if f_.startswith("_2pass"): os.remove(os.path.join(ENT, f_))
print("entrega:", ENT)
