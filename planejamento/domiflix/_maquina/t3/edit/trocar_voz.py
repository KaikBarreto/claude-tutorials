"""Troca só a narração de capítulos já renderizados (sem refazer o vídeo): aponta o JSON do capítulo para o áudio
emendado (t3/narracao/emendas/capNN_v2.wav) e regrava out/capNN/capNN.wav alinhado ao MP4 (o finish.py usa esse WAV).
uso: python3 -I t3/edit/trocar_voz.py NN [NN ...]"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
from chapter import Chapter  # noqa: E402

EMENDAS = os.path.join(os.path.dirname(HERE), "narracao", "emendas")
for nn in sys.argv[1:]:
    nn = f"{int(nn):02d}"
    cj = os.path.join(HERE, "caps", f"cap{nn}.chapter.json")
    ch = json.load(open(cj))
    nova = os.path.join(EMENDAS, f"cap{nn}_v2.wav")
    assert os.path.exists(nova), nova
    ch["narration"] = nova
    json.dump(ch, open(cj, "w"), ensure_ascii=False, indent=1)
    C = Chapter(cj)
    wav = os.path.join(C.outd, f"cap{nn}.wav")
    C.align_audio(wav)
    print(f"cap{nn}: narração emendada -> {wav}")
