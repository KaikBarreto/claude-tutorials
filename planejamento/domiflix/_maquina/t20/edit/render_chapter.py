"""Editor de tutoriais: monta UM capitulo a partir da gravacao (MP4 2560x1600 sem cursor) + telemetria + narracao.
uso: python3 <tutorial>/edit/render_chapter.py <capitulo.json> [--out video.mp4] [--wav narracao.wav] [--range a:b] [--stills t1,t2,...] [--partes 2]
                                       [--crf 17] [--preset veryfast] [--no-audio]
  --range a:b   renderiza so o trecho (s do video) | --stills  PNGs de tempos soltos em <out>/stills (sem codificar)
  --partes N    processos ao mesmo tempo (padrao 2 ou $TUT_PARTES; 1 = um so; trecho < 10 s vai inteiro). Junta com concat -c copy.
Roda sempre sob `flock $TUT_HOME/.heavy.lock nice -n 10` (reexecuta sozinho). Memoria: streaming (1 quadro por vez).
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

QUADROS = "--quadros" in argv  # filho do modo em partes: so os quadros F0..F1-1 do capitulo (sem audio)
has_audio = False if ("--no-audio" in argv or QUADROS) else C.align_audio(out_wav)
crf, preset = opt("--crf", ch.get("output", {}).get("crf", 17)), opt("--preset", ch.get("output", {}).get("preset", "veryfast"))
F0, F1 = map(int, opt("--quadros").split(":")) if QUADROS else (0, N)
P = max(1, int(opt("--partes", os.environ.get("TUT_PARTES", "2"))))  # processos ao mesmo tempo (1 = como antes)


def cortes(P):
    """Onde dividir: 2P trechos, cada corte no quadro sem aviso, destaque, ilustracao nem titulo mais perto do ideal (essas
    camadas guardam estado do 1o quadro em que aparecem, ex.: a largura do aviso ao lado do celular). Sem quadro livre perto,
    o corte cai fora (menos trechos)."""
    jan = [(float(x["at"]), float(x["at"]) + float(x.get("dur", 3.0))) for k in ("callouts", "spots", "illustrations") for x in ch.get(k, [])]
    if ch.get("title"): a = float(ch.get("title_at", 0.5)); jan.append((a, a + float(ch.get("title_dur", 3.6))))
    livre = lambda f: all(not (a - 0.15 <= T0 + f / FPS <= b + 0.15) for a, b in jan)
    S, cs = 2 * P, [0]
    for i in range(1, S):
        ideal, meia = round(N * i / S), int(N / S / 2)
        f = next((g for d in range(meia) for g in (ideal - d, ideal + d) if cs[-1] + 60 <= g <= N - 60 and livre(g) and livre(g - 1)), None)
        if f is not None: cs.append(f)
    return cs + [N]


def em_partes(P, cuts):
    """Kaik 03/11 ("nao tem como renderizar em paralelo?"): o desenho do quadro usa 1 nucleo e deixava 43% da maquina parada.
    Renderiza os trechos de `cuts`, P de cada vez (este mesmo script com --quadros, ainda sob a mesma trava), e junta com
    concat -c copy. Cada quadro usa o mesmo t (T0 + f/FPS) e o mesmo quadro da gravacao do render inteiro."""
    import ctypes, shutil, signal, tempfile
    tmp = tempfile.mkdtemp(prefix=f".{NAME}.partes.", dir=os.path.dirname(os.path.abspath(out_mp4)))
    S = len(cuts) - 1; parte = lambda i: os.path.join(tmp, f"p{i:02d}.mp4")
    cmd = [sys.executable, "-I", os.path.abspath(__file__), argv[0], "--crf", str(crf), "--preset", str(preset), "--partes", "1"]
    cmd += (["--aceitar-camera"] if "--aceitar-camera" in argv else []) + (["--range", opt("--range")] if rng else [])
    morre_junto = lambda: ctypes.CDLL(None).prctl(1, signal.SIGKILL)  # PR_SET_PDEATHSIG: filho nao sobrevive ao pai
    signal.signal(signal.SIGTERM, lambda *a: sys.exit(143))
    fila, rodando, feitos, env = list(range(S)), [], 0, dict(os.environ, TUT_LOCKED="1")
    try:
        while fila or rodando:
            while fila and len(rodando) < P:
                i = fila.pop(0); log = open(parte(i) + ".log", "w")
                rodando.append((i, subprocess.Popen(cmd + ["--quadros", f"{cuts[i]}:{cuts[i + 1]}", "--out", parte(i)], env=env,
                                                    stdout=log, stderr=subprocess.STDOUT, preexec_fn=morre_junto), log))
            time.sleep(0.5)
            for item in [r for r in rodando if r[1].poll() is not None]:
                i, p, log = item; rodando.remove(item); log.close()
                if p.returncode: raise RuntimeError(f"trecho {i} ({cuts[i]}:{cuts[i + 1]}) falhou:\n" + open(parte(i) + ".log").read()[-1500:])
                feitos += cuts[i + 1] - cuts[i]; el = time.time() - t_wall
                print(f"\r{feitos}/{N} quadros  {feitos / el:.1f} q/s  falta ~{(N - feitos) / max(feitos / el, 1e-3) / 60:.1f} min", end="", flush=True)
        open(os.path.join(tmp, "lista.txt"), "w").write("".join(f"file '{parte(i)}'\n" for i in range(S)))
        junto = os.path.join(tmp, "junto.mp4")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(tmp, "lista.txt"), "-c", "copy",
                        "-movflags", "+faststart", junto], check=True)
        os.replace(junto, out_mp4)
        st = [json.load(open(os.path.splitext(parte(i))[0] + ".edit.json"))["stats"] for i in range(S)]
        return sum(s["frames_with_blur"] for s in st), max(s["peak_rss_mb"] for s in st)
    except BaseException:
        for _, p, _ in rodando: p.kill()
        raise
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


t_wall = time.time()
CUTS = cortes(P) if (P > 1 and not QUADROS and N >= 300) else [0, N]
if len(CUTS) > 2:
    moving, rss = em_partes(P, CUTS); C.ov.close()
else:
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-vf", "scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p", "-c:v", "libx264",
                            "-preset", str(preset), "-crf", str(crf), "-g", "60", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
                            "-color_range", "tv", "-movflags", "+faststart", out_mp4], stdin=subprocess.PIPE)
    rd = Reader(VIDEO, SW, SH, T0, FPS, skip=F0); moving = 0
    for f in range(F0, F1):
        t = T0 + f / FPS; fr = rd.next(); img, n = C.compose(t, fr); enc.stdin.write(img.tobytes()); moving += n > 1
        if (f - F0) % 30 == 29 or f == F1 - 1:
            k = f - F0 + 1; el = time.time() - t_wall
            print(f"\r{k}/{F1 - F0} quadros  {k / el:.1f} q/s  falta ~{(F1 - F0 - k) / max(k / el, 1e-3) / 60:.1f} min", end="", flush=True)
    enc.stdin.close(); enc.wait(); rd.close(); C.ov.close()
    rss = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024)
el = time.time() - t_wall; cam = C.cam; NQ = F1 - F0
side = dict(name=NAME, video=out_mp4, wav=out_wav if os.path.exists(out_wav) else None, title=ch.get("title"), dur=N / FPS, frames=N, start=T0,
            zoom_in=[round(s - T0, 3) for s in cam.zoom_in_times() if T0 <= s < T1],
            regions=[{k: ([[round(float(a), 3) for a in tr] for tr in v] if k == "track" else
                          round(float(v), 3) if not isinstance(v, str) else v) for k, v in r.items()} for r in cam.regions],
            callouts=[{**c, "at": c["at"] - T0} for c in ch.get("callouts", [])], spots=ch.get("spots", []),
            stats=dict(wall_s=round(el, 1), fps=round(NQ / el, 2), frames_with_blur=int(moving), peak_rss_mb=rss,
                       partes=len(CUTS) - 1, cortes=CUTS[1:-1]))
json.dump(side, open(os.path.splitext(out_mp4)[0] + ".edit.json", "w"), ensure_ascii=False, indent=1)  # ao lado do MP4 (o finish.py le este arquivo)
print(f"\nok {out_mp4}  ({NQ / FPS:.1f} s, {el:.0f} s de render = {NQ / el:.1f} q/s, {moving} quadros com desfoque, pico {rss} MB)")
