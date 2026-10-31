"""Teste sintético (sem ASR, leve) da opção `empurra` do emendar.py: áudio de tons no lugar da fala, `recortar` trocado por uma frase
sintética mais longa que a janela. Confere: (A) sem `empurra` a frase é CORTADA e a duração fica; (B) com `empurra` a duração cresce, nada é
cortado, a fala seguinte anda junto e a folga final fica >= 0,2 s; (C) duas trocas no mesmo capítulo: a 2ª acompanha o deslocamento da 1ª;
(D) inserção com `em` numérico depois da troca empurrada cai no instante deslocado; (E) `em: "fim"` depois de troca no fim com `empurra`.
uso: python3 -I testes/emendar_empurra.py [<emendar.py>]   (padrão: ferramentas/narracao/emendar.py desta skill)"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

import numpy as np
import soundfile as sf

SR = 48000
SRC = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ferramentas", "narracao", "emendar.py")
falhas = []


def confere(ok, msg):
    print(("OK    " if ok else "FALHA ") + msg)
    if not ok:
        falhas.append(msg)


def tom(f, dur, amp=0.3):
    t = np.arange(int(round(dur * SR))) / SR
    y = amp * np.sin(2 * np.pi * f * t)
    n = int(0.01 * SR)
    y[:n] *= np.linspace(0, 1, n)
    y[-n:] *= np.linspace(1, 0, n)
    return y.astype(np.float32)


def rms(y, a, b):
    seg = y[int(a * SR):int(b * SR)]
    return float(np.sqrt(np.mean(seg ** 2))) if len(seg) else 0.0


def freq(y, a, b):
    seg = y[int(a * SR):int(b * SR)]
    sp = np.abs(np.fft.rfft(seg * np.hanning(len(seg))))
    return float(np.argmax(sp) * SR / len(seg))


def monta(d):
    """capítulo sintético de 16 s: trechos de tom (a 'fala') com silêncio entre eles."""
    os.makedirs(os.path.join(d, "takes", "cap09"), exist_ok=True)
    os.makedirs(os.path.join(d, "emendas"), exist_ok=True)
    y = np.zeros(16 * SR, dtype=np.float32)
    segs = [(2.0, 4.0, 300), (4.2, 6.0, 500), (8.0, 9.5, 700), (9.7, 11.5, 900), (13.0, 15.5, 1100)]
    words = []
    for a, b, f in segs:
        ia = int(round(a * SR)); x = tom(f, b - a); y[ia:ia + len(x)] += x
        words.append({"w": f"p{f}", "s": a, "e": b})
    sf.write(os.path.join(d, "takes", "cap09", "audio48k.wav"), y, SR, subtype="PCM_24")
    vad = [[a, b] for a, b, _ in segs]
    json.dump({"cap": 9, "take": "cap09", "arquivo": os.path.join(d, "takes", "cap09", "audio48k.wav"), "pasta": os.path.join(d, "takes", "cap09"),
               "dur": 16.0, "words": words, "vad": vad, "linhas": []}, open(os.path.join(d, "cap09.json"), "w"))
    return y


def roda(d, cfg, insercoes=False):
    json.dump(cfg, open(os.path.join(d, "trocas.json"), "w"))
    drv = os.path.join(d, "drv.py")
    open(drv, "w").write(
        "import sys, numpy as np\nsys.path.insert(0, %r)\nimport emendar\nSR = 48000\n"
        "def tom(f, dur, amp=0.3):\n    t = np.arange(int(dur*SR))/SR\n    y = (amp*np.sin(2*np.pi*f*t)).astype(np.float32)\n    n=int(0.01*SR)\n    y[:n]*=np.linspace(0,1,n); y[-n:]*=np.linspace(1,0,n)\n    return y\n"
        "def rec(src, frases, rotulo='frase'):\n    return {f: (tom(1500, 3.0), 2.95) if len(f) > 10 else (tom(1700, 1.0), 0.95) for f in frases}\n"
        "emendar.recortar = rec\nsys.argv = ['emendar.py', 'x.mp3'] + (['--insercoes', 'y.mp3'] if %r else [])\nemendar.main()\n" % (d, insercoes))
    r = subprocess.run(["python3", "-I", drv], cwd=d, capture_output=True, text=True)
    print(r.stdout[-1800:])
    if r.returncode:
        print(r.stderr[-1500:])
    return r.returncode, r.stdout


tmp = tempfile.mkdtemp(prefix="teste_empurra_")
try:
    # --------- A) sem `empurra`: CORTADA, duração igual
    d = os.path.join(tmp, "A"); os.makedirs(d); shutil.copy(SRC, os.path.join(d, "emendar.py")); open(os.path.join(d, "proc.py"), "w").write("")
    base = monta(d)
    print("== A) sem empurra ==")
    rc, out = roda(d, {"trocas": [{"cap": 9, "velho": "v", "novo": "frase nova bem comprida", "de": 2.0, "ate": 4.0}]})
    y, _ = sf.read(os.path.join(d, "emendas", "cap09_v2.wav"), dtype="float32")
    confere(rc == 0 and "CORTADA" in out, "A: sem `empurra` o script avisa CORTADA")
    confere(abs(len(y) - len(base)) <= 2, "A: a duração do capítulo não mudou")

    # --------- B) com `empurra`
    d = os.path.join(tmp, "B"); os.makedirs(d); shutil.copy(SRC, os.path.join(d, "emendar.py")); open(os.path.join(d, "proc.py"), "w").write("")
    base = monta(d)
    print("== B) com empurra ==")
    rc, out = roda(d, {"trocas": [{"cap": 9, "velho": "v", "novo": "frase nova bem comprida", "de": 2.0, "ate": 4.0, "empurra": True}]})
    y, _ = sf.read(os.path.join(d, "emendas", "cap09_v2.wav"), dtype="float32")
    cresceu = (len(y) - len(base)) / SR
    confere(rc == 0 and "CORTADA" not in out and "EMPURRADA" in out, "B: avisa EMPURRADA e não CORTADA")
    confere(0.6 < cresceu < 0.9, f"B: a duração cresceu {cresceu:.3f} s (esperado ~0,7 s)")
    # a 'fala' seguinte (500 Hz, 4,2 a 6,0 s) agora começa em 4,2 + cresceu
    s2 = 4.2 + cresceu
    confere(abs(freq(y, s2 + 0.1, s2 + 1.0) - 500) < 15 and rms(y, s2 + 0.1, s2 + 1.0) > 0.1, "B: a fala seguinte (500 Hz) anda junto")
    confere(rms(y, s2 - 0.14, s2 - 0.03) < 0.01, "B: silêncio entre a frase nova e a fala seguinte (folga ~0,2 s; o trecho tem 0,05 s de rabo depois da última palavra)")
    confere(rms(y, s2 - 0.45, s2 - 0.25) > 0.1 and abs(freq(y, s2 - 0.45, s2 - 0.25) - 1500) < 25, "B: o fim da frase nova (1500 Hz) está inteiro, sem corte")
    # tudo depois da janela é o original deslocado
    a0 = int(5.0 * SR)
    confere(np.allclose(y[a0 + int(round(cresceu * SR)):a0 + int(round(cresceu * SR)) + SR], base[a0:a0 + SR], atol=1e-4), "B: depois da janela o áudio é o original deslocado")
    confere(np.allclose(y[:int(1.9 * SR)], base[:int(1.9 * SR)], atol=1e-4), "B: antes da janela o áudio é o original")

    # --------- C) duas trocas: a 2ª acompanha o deslocamento da 1ª
    d = os.path.join(tmp, "C"); os.makedirs(d); shutil.copy(SRC, os.path.join(d, "emendar.py")); open(os.path.join(d, "proc.py"), "w").write("")
    base = monta(d)
    print("== C) duas trocas (a 1ª com empurra) ==")
    rc, out = roda(d, {"trocas": [
        {"cap": 9, "velho": "v", "novo": "frase nova bem comprida", "de": 2.0, "ate": 4.0, "empurra": True},
        {"cap": 9, "velho": "v2", "novo": "curta", "de": 8.0, "ate": 9.5}]})
    y, _ = sf.read(os.path.join(d, "emendas", "cap09_v2.wav"), dtype="float32")
    cresceu = (len(y) - len(base)) / SR
    confere(rc == 0 and "CORTADA" not in out, "C: sem CORTADA")
    # a 2ª troca troca o tom 700 Hz (8,0 a 9,5) pela 'frase nova' de 1700 Hz, que agora começa em 8,0 + cresceu
    conta = out.count("folga final")
    confere(conta == 2, f"C: as duas trocas foram processadas ({conta})")
    s3 = 8.0 + cresceu
    confere(abs(freq(y, s3 + 0.1, s3 + 0.6) - 1700) < 25, "C: a 2ª troca caiu no lugar deslocado (1700 Hz em 8,0 + deslocamento)")
    confere(rms(y, 8.2, 8.6) < 0.01 or abs(freq(y, 8.2, 8.6) - 700) > 50 or cresceu < 0.05, "C: nada do 700 Hz antigo no lugar não deslocado")
    s4 = 9.7 + cresceu
    confere(abs(freq(y, s4 + 0.1, s4 + 1.0) - 900) < 20, "C: a fala depois da 2ª troca (900 Hz) continua no lugar deslocado")

    # --------- D) inserção com `em` numérico depois da troca empurrada
    d = os.path.join(tmp, "D"); os.makedirs(d); shutil.copy(SRC, os.path.join(d, "emendar.py")); open(os.path.join(d, "proc.py"), "w").write("")
    base = monta(d)
    print("== D) troca empurrada + inserção em 12.0 s (silêncio entre 11,5 e 13,0) ==")
    rc, out = roda(d, {"trocas": [{"cap": 9, "velho": "v", "novo": "frase nova bem comprida", "de": 2.0, "ate": 4.0, "empurra": True}],
                       "insercoes": [{"cap": 9, "em": 12.0, "folga": 0.1, "novo": "inserida"}]}, insercoes=True)
    v2, _ = sf.read(os.path.join(d, "emendas", "cap09_v2.wav"), dtype="float32")
    v3, _ = sf.read(os.path.join(d, "emendas", "cap09_v3.wav"), dtype="float32")
    cresceu = (len(v2) - len(base)) / SR
    confere(rc == 0 and "ATENÇÃO" not in out, "D: sem ATENÇÃO (o corte caiu em silêncio)")
    t_ins = 12.0 + cresceu
    confere(abs(freq(v3, t_ins + 0.15, t_ins + 0.9) - 1700) < 25, f"D: a inserção (1700 Hz) começa em {t_ins:.2f} s (12,0 + deslocamento da troca)")
    confere(abs((len(v3) - len(v2)) / SR - (1.0 + 0.2)) < 0.15, f"D: o _v3 ficou {(len(v3) - len(v2)) / SR:.2f} s maior que o _v2 (frase de 1 s + 2 x 0,1)")

    # --------- E) troca no fim do capítulo com `empurra` + inserção `fim`
    d = os.path.join(tmp, "E"); os.makedirs(d); shutil.copy(SRC, os.path.join(d, "emendar.py")); open(os.path.join(d, "proc.py"), "w").write("")
    base = monta(d)
    print("== E) troca no fim (14,0 a 15,5 s, frase de 3 s) com empurra + inserção no fim ==")
    rc, out = roda(d, {"trocas": [{"cap": 9, "velho": "v", "novo": "frase nova bem comprida", "de": 14.0, "ate": 15.5, "empurra": True}],
                       "insercoes": [{"cap": 9, "em": "fim", "folga": 0.25, "novo": "inserida"}]}, insercoes=True)
    v2, _ = sf.read(os.path.join(d, "emendas", "cap09_v2.wav"), dtype="float32")
    v3, _ = sf.read(os.path.join(d, "emendas", "cap09_v3.wav"), dtype="float32")
    confere(rc == 0 and "CORTADA" not in out, "E: sem CORTADA")
    confere(len(v2) > len(base) + int(0.1 * SR) or "folga final" in out, f"E: o _v2 ({len(v2) / SR:.2f} s) vs. original ({len(base) / SR:.2f} s)")
    fim_v2 = len(v2) / SR
    confere(abs(freq(v3, fim_v2 + 0.3, fim_v2 + 1.0) - 1700) < 25, "E: a inserção entra depois do fim (já empurrado) da troca")
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print("\nresultado:", "TUDO OK" if not falhas else f"{len(falhas)} FALHA(S)")
sys.exit(1 if falhas else 0)
