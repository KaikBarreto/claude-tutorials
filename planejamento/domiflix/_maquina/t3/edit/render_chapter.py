"""Editor do T3 (Domiflix): monta UM capitulo a partir da gravacao (MP4 2560x1600 sem cursor) + telemetria + narracao.
uso: python3 t3/edit/render_chapter.py <capitulo.json> [--out video.mp4] [--wav narracao.wav] [--range a:b] [--stills t1,t2,...]
                                       [--crf 17] [--preset veryfast] [--no-audio]
  --range a:b   renderiza so o trecho (s do video) | --stills  PNGs de tempos soltos em <out>/stills (sem codificar)
Roda sempre sob `flock /home/claude/domiflix/.heavy.lock nice -n 10` (reexecuta sozinho). Memoria: streaming (1 quadro por vez).
JSON do capitulo (caminhos relativos ao proprio JSON; tempos em s do video):
  {"name","video","telemetry","narration"?,"audio_offset"?,"title","title_kicker"?,"title_at"?,"title_dur"?,"trim":{"start","end"}?,
   "camera":{auto,depth,lead,tail,group_gap,slide_gap,t_in,t_out,t_slide,follow,...}, "cursor":{show,size,smooth,blur,idle_hide,...},
   "stage":{"margin","radius"}, "zooms":[{at,dur|end,scale|rect|target,follow?}], "callouts":[{at,dur,text,pos?}],
   "spots":[{at,dur,rect,label?}], "illustrations":[{at,dur,src,box?,fps?,loop?}], "output":{"dir","crf","preset"}}
  audio_offset: s em que a narracao comeca no relogio do video (>0 atrasa a voz; <0 corta o comeco dela)."""
import json, os, resource, subprocess, sys, time
import numpy as np, cv2
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.dont_write_bytecode = True
from common import ensure_heavy, probe, Reader, still  # noqa: E402

argv = sys.argv[1:]
opt = lambda k, d=None: argv[argv.index(k) + 1] if k in argv else d
if "--help" in argv or not argv: print(__doc__); sys.exit(0)
ensure_heavy()
from chapter import Chapter  # noqa: E402
from camera import W, H, FPS  # noqa: E402

cv2.setNumThreads(2)
rng = tuple(map(float, opt("--range").split(":"))) if "--range" in argv else None
C = Chapter(argv[0], rng); ch = C.ch; NAME, OUTD, VIDEO, N, T0, T1 = C.name, C.outd, C.video, C.n, C.t0, C.t1; SW, SH = C.SW, C.SH
os.makedirs(OUTD, exist_ok=True)
if getattr(C.cam, "problemas", None):  # Kaik 30/10: zoom fora do alvo "nunca deve acontecer" -> nao renderiza
    print("CHECAGEM DA CAMERA:", *C.cam.problemas, sep="\n  ", flush=True)
    if "--stills" not in argv and "--aceitar-camera" not in argv:
        sys.exit("camera com alvo fora do quadro: corrija o zoom/roteiro antes de renderizar (ou --aceitar-camera, com motivo)")
out_mp4 = opt("--out", os.path.join(OUTD, NAME + ".mp4")); out_wav = opt("--wav", os.path.join(OUTD, NAME + ".wav"))

if "--stills" in argv:
    sd = os.path.join(OUTD, "stills"); os.makedirs(sd, exist_ok=True)
    for t in map(float, opt("--stills").split(",")):
        img, n = C.compose(t, still(VIDEO, t, SW, SH)); cv2.imwrite(os.path.join(sd, f"{NAME}_{t:07.2f}.png"), cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
        print(f"t={t:.2f} zoom={C.geom.vw0 / C.cam.view(t)[2]:.2f} sub-quadros={n}")
    sys.exit()

has_audio = False if "--no-audio" in argv else C.align_audio(out_wav)
crf, preset = opt("--crf", ch.get("output", {}).get("crf", 17)), opt("--preset", ch.get("output", {}).get("preset", "veryfast"))
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                        "-vf", "scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p", "-c:v", "libx264",
                        "-preset", str(preset), "-crf", str(crf), "-g", "60", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
                        "-color_range", "tv", "-movflags", "+faststart", out_mp4], stdin=subprocess.PIPE)
rd = Reader(VIDEO, SW, SH, T0, FPS); t_wall = time.time(); moving = 0
for f in range(N):
    t = T0 + f / FPS; fr = rd.next(); img, n = C.compose(t, fr); enc.stdin.write(img.tobytes()); moving += n > 1
    if f % 30 == 29 or f == N - 1:
        el = time.time() - t_wall; print(f"\r{f + 1}/{N} quadros  {(f + 1) / el:.1f} q/s  falta ~{(N - f - 1) / max((f + 1) / el, 1e-3) / 60:.1f} min", end="", flush=True)
enc.stdin.close(); enc.wait(); rd.close(); C.ov.close(); el = time.time() - t_wall
cam = C.cam; rss = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024)
side = dict(name=NAME, video=out_mp4, wav=out_wav if os.path.exists(out_wav) else None, title=ch.get("title"), dur=N / FPS, frames=N, start=T0,
            zoom_in=[round(s - T0, 3) for s in cam.zoom_in_times() if T0 <= s < T1],
            regions=[{k: ([[round(float(a), 3) for a in tr] for tr in v] if k == "track" else
                          round(float(v), 3) if not isinstance(v, str) else v) for k, v in r.items()} for r in cam.regions],
            callouts=[{**c, "at": c["at"] - T0} for c in ch.get("callouts", [])], spots=ch.get("spots", []),
            stats=dict(wall_s=round(el, 1), fps=round(N / el, 2), frames_with_blur=int(moving), peak_rss_mb=rss))
json.dump(side, open(os.path.splitext(out_mp4)[0] + ".edit.json", "w"), ensure_ascii=False, indent=1)  # ao lado do MP4 (o finish.py le este arquivo)
print(f"\nok {out_mp4}  ({N / FPS:.1f} s, {el:.0f} s de render = {N / el:.1f} q/s, {moving} quadros com desfoque, pico {rss} MB)")
