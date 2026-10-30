"""Transcrição com tempo por palavra (Parakeet-TDT v3 int8 via sherpa-onnx), em blocos cortados em pontos silenciosos.
uso: python3 kit/asr.py <projeto>   -> words.json [{w,s,e}] + transcript.txt (frases com [mm:ss.s])"""
import json, os, re, sys, time
import numpy as np, soundfile as sf

proj = os.path.abspath(sys.argv[1])
MODEL = os.environ.get("PARAKEET", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models",
                                                 "sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8")) + "/"
SR = 16000; MAXC = 24.0; PAD0, PAD1 = 0.2, 0.4
x, sr = sf.read(os.path.join(proj, "audio16k.wav"), dtype="float32"); assert sr == SR

import sherpa_onnx
VADM = os.path.join(os.path.dirname(MODEL.rstrip("/")), "silero_vad.onnx")

# 1) detector de voz (Silero): onde há fala, independente do ASR — o plano nunca corta esses trechos
vc = sherpa_onnx.VadModelConfig(); vc.silero_vad.model = VADM; vc.silero_vad.threshold = 0.45
vc.silero_vad.min_silence_duration = 0.25; vc.silero_vad.min_speech_duration = 0.12; vc.silero_vad.window_size = 512
vc.sample_rate = SR; vad = sherpa_onnx.VoiceActivityDetector(vc, buffer_size_in_seconds=120); vsegs = []
def drain():
    while not vad.empty():
        sg = vad.front; vsegs.append([round(sg.start / SR, 3), round((sg.start + len(sg.samples)) / SR, 3)]); vad.pop()
for i in range(0, len(x), 512):
    vad.accept_waveform(x[i:i + 512]); drain()
vad.flush(); drain()
json.dump(vsegs, open(os.path.join(proj, "vad.json"), "w"))
print(f"VAD: {len(vsegs)} trechos de fala, {sum(b - a for a, b in vsegs):.1f}s")

# 2) blocos de até MAXC s formados por trechos de fala inteiros (corta só nas pausas)
groups = []
for a, b in vsegs:
    if groups and b - groups[-1][0] <= MAXC: groups[-1][1] = b
    else: groups.append([a, b])
cuts = [(max(0, int((a - 0.3) * SR)), min(len(x), int((b + 0.3) * SR))) for a, b in groups]

rec = sherpa_onnx.OfflineRecognizer.from_transducer(
    encoder=MODEL + "encoder.int8.onnx", decoder=MODEL + "decoder.int8.onnx", joiner=MODEL + "joiner.int8.onnx",
    tokens=MODEL + "tokens.txt", num_threads=os.cpu_count() or 4, model_type="nemo_transducer")
words = []; t0 = time.time()


def run(c0, c1):
    y = np.concatenate([np.zeros(int(PAD0 * SR), np.float32), x[c0:c1], np.zeros(int(PAD1 * SR), np.float32)])
    s = rec.create_stream(); s.accept_waveform(SR, y); rec.decode_stream(s); r = s.result
    off = c0 / SR - PAD0; cw = []
    for tok, ts, du in zip(r.tokens, r.timestamps, r.durations):
        core = tok.strip()
        if not core: continue
        t_s, t_e = off + ts, off + ts + max(du, 0.04)
        if re.fullmatch(r"[.,;:?!…]+", core):
            if cw: cw[-1]["w"] += core
            continue
        glued = bool(cw) and core[0].isdigit() and cw[-1]["w"][-1:].isalpha()
        if tok.startswith(" ") or not cw or glued:
            cw.append({"w": core, "s": round(max(0.0, t_s), 3), "e": round(t_e, 3)})
        else:
            cw[-1]["w"] += core; cw[-1]["e"] = round(t_e, 3)
    return cw


for c0, c1 in cuts:
    words += run(c0, c1)
    print(f"\r{c1/SR:7.1f}/{len(x)/SR:.1f}s  {len(words)} palavras  {time.time()-t0:.0f}s", end="", flush=True)
print()
# 3) trecho de fala sem nenhuma palavra (o modelo pulou): transcreve sozinho
for a, b in vsegs:
    if b - a >= 0.4 and not any(a - 0.1 <= w["s"] <= b for w in words):
        extra = run(max(0, int((a - 0.25) * SR)), min(len(x), int((b + 0.25) * SR)))
        print(f"  refeito {a:.1f}-{b:.1f}s: {' '.join(w['w'] for w in extra) or '(sem palavras)'}")
        extra = [w for w in extra if a - 0.7 <= w["s"] <= b + 0.3]
        for w in extra: w["s"] = max(w["s"], round(a - 0.05, 3)); w["e"] = max(w["e"], w["s"] + 0.05)  # 1º token sai adiantado
        words += extra
words.sort(key=lambda w: w["s"])
json.dump(words, open(os.path.join(proj, "words.json"), "w"), ensure_ascii=False, indent=0)

# transcrição legível: quebra em pontuação final ou pausa > 0,8 s
fmt = lambda t: f"{int(t//60):02d}:{t%60:04.1f}"
lines, cur = [], []
for i, wd in enumerate(words):
    cur.append(wd)
    nxt = words[i + 1] if i + 1 < len(words) else None
    if nxt is None or wd["w"][-1:] in ".?!" or nxt["s"] - wd["e"] > 0.8:
        lines.append(f"[{fmt(cur[0]['s'])}–{fmt(cur[-1]['e'])}] " + " ".join(w["w"] for w in cur)); cur = []
open(os.path.join(proj, "transcript.txt"), "w").write("\n".join(lines) + "\n")
print(f"{len(words)} palavras, {len(lines)} frases -> transcript.txt ({time.time()-t0:.0f}s)")
