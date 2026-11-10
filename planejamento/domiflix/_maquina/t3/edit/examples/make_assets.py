"""Gera ativos de teste para o capitulo de exemplo: sequencia PNG com alfa (selo animado) e um clipe MP4 curto (sem alfa),
mais uma narracao de teste (flite) para conferir alinhamento e ducking. uso: python3 examples/make_assets.py"""
import os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(HERE, "assets"); os.makedirs(A, exist_ok=True)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "..", "kit")); import ui  # noqa
seq = os.path.join(A, "selo"); os.makedirs(seq, exist_ok=True)
f = ui.font(700, 34); ss = 3
for i in range(36):
    w, h = 520, 190; im = Image.new("RGBA", (w * ss, h * ss), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w * ss - 1, h * ss - 1], 28 * ss, fill=(30, 30, 30, 238))
    p = min(1, i / 10); k = 1 + 0.12 * np.sin(np.pi * p) * (1 - p) * 3; r = 52 * k * ss; cx, cy = 100 * ss, h * ss / 2
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(0, 197, 151, 255))
    d.line([(cx - 24 * ss, cy + 2 * ss), (cx - 6 * ss, cy + 20 * ss), (cx + 28 * ss, cy - 18 * ss)], fill=(30, 30, 30, 255), width=9 * ss, joint="curve")
    d.text((190 * ss, cy), "Cliente salvo", font=ui.font(700, 34 * ss), fill=(255, 255, 255, 255), anchor="lm")
    im.resize((w, h), Image.LANCZOS).save(os.path.join(seq, f"selo_{i:04d}.png"))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc2=size=640x360:rate=30:duration=2", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                os.path.join(A, "clipe.mp4")], check=True)
# narracao de teste (voz sintetica em ingles, so para medir alinhamento e ducking)
phr = [(1.0, "Welcome to the customers screen."), (6.2, "Search for the customer by name."), (11.5, "Open the customer record."),
       (19.8, "Here you see the address and the map."), (28.6, "Now create a new customer.")]
sr = 48000; y = np.zeros(int(35.6 * sr), np.float32)
for t, txt in phr:
    out = subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", f"flite=text='{txt}':voice=slt", "-ar", str(sr), "-ac", "1", "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(out, np.float32); i = int(t * sr); y[i:i + len(x)] += x[: len(y) - i]
import soundfile as sf; sf.write(os.path.join(A, "narracao_teste.wav"), y * 0.8, sr, subtype="PCM_16"); print("ativos ok")
