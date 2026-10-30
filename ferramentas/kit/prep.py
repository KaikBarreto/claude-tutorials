"""Prepara uma aula gravada (tela + narração).
uso: python3 kit/prep.py <video> <projeto>
Gera em <projeto>/: project.json (metadados), audio16k.wav (ASR), audio48k.wav (mix),
activity.npz (mudança de tela a 10 qps: px alterados + caixa da mudança em coords da fonte) e thumbs/ (1 quadro a cada 2 s)."""
import json, os, subprocess, sys
import numpy as np

src, proj = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
os.makedirs(os.path.join(proj, "thumbs"), exist_ok=True)
P = lambda *a: os.path.join(proj, *a)

info = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", src],
                                 capture_output=True, check=True).stdout)
vs = next(s for s in info["streams"] if s["codec_type"] == "video")
au = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
num, den = map(int, vs.get("avg_frame_rate", "30/1").split("/")); fps = num / den if den else 30.0
rot = 0
for sd in vs.get("side_data_list", []) or []:
    if "rotation" in sd: rot = int(sd["rotation"])
w, h = int(vs["width"]), int(vs["height"])
if abs(rot) in (90, 270): w, h = h, w
dur = float(info["format"]["duration"])
meta = {"src": src, "w": w, "h": h, "fps_src": round(fps, 3), "dur": dur, "codec": vs.get("codec_name"),
        "pix_fmt": vs.get("pix_fmt"), "color_transfer": vs.get("color_transfer"), "has_audio": au is not None,
        "audio_ch": au and au.get("channels"), "audio_sr": au and au.get("sample_rate"), "rotation": rot}
json.dump(meta, open(P("project.json"), "w"), indent=1)
print(json.dumps(meta, indent=1))

if au is not None:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", P("audio16k.wav")], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vn", "-ac", "1", "-ar", "48000", "-c:a", "pcm_f32le", P("audio48k.wav")], check=True)
    print("áudio ok")

# atividade de tela: 10 qps, 960 px de largura, cinza (sensível o bastante p/ ver digitação em fonte pequena)
AW = 960; AH = int(round(h * AW / w / 2) * 2); AF = 10
cmd = ["ffmpeg", "-v", "error", "-i", src, "-vf", f"fps={AF},scale={AW}:{AH}:flags=area,format=gray", "-f", "rawvideo", "-"]
pr = subprocess.Popen(cmd, stdout=subprocess.PIPE)
fsz = AW * AH; prev = None; rows = []; k = 0
sx, sy = w / AW, h / AH
while True:
    buf = pr.stdout.read(fsz)
    if len(buf) < fsz: break
    f = np.frombuffer(buf, np.uint8).reshape(AH, AW).astype(np.int16)
    if prev is None:
        rows.append((0, 0.0, -1, -1, -1, -1))
    else:
        d = np.abs(f - prev) > 10
        n = int(d.sum())
        if n:
            ys, xs = np.nonzero(d)
            rows.append((n, float(np.abs(f - prev).mean()), xs.min() * sx, ys.min() * sy, (xs.max() + 1) * sx, (ys.max() + 1) * sy))
        else:
            rows.append((0, float(np.abs(f - prev).mean()), -1, -1, -1, -1))
    prev = f; k += 1
pr.wait()
A = np.array(rows, np.float64)
np.savez_compressed(P("activity.npz"), t=np.arange(len(A)) / AF, px=A[:, 0], mean=A[:, 1], box=A[:, 2:6], scale=AW / w)
print(f"atividade: {len(A)} amostras ({len(A)/AF:.1f}s), {np.mean(A[:,0] > 8)*100:.0f}% com mudança")

# miniaturas a cada 2 s (480 px) para folhas de contato
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", "fps=1/2,scale=480:-2", "-q:v", "4", P("thumbs", "t%05d.jpg")], check=True)
print("miniaturas ok:", len(os.listdir(P("thumbs"))))
