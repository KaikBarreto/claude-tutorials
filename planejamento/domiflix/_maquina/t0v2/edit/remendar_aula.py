"""Remenda uma aula JÁ ENTREGUE quando só alguns capítulos mudaram, sem renderizar os outros.
(Depois da entrega a limpeza apaga as gravações e os renders dos capítulos; este script refaz a aula só com o que a entrega
deixa em <out>: capitulos.json, video_sem_audio.mp4 e proj/{audio48k.wav, edl.json, render.json, build/{intro_v.mp4, outro_v.mp4}}.)

uso: python3 -I remendar_aula.py <aula.json> [--audio cap03,cap07] [--novos cap05,cap06,cap13] [--plano] [--crf 20] [--formato 16x9|9x16]
                                  [--frames cap05=1954,cap06=1846]   (só com --plano: quadros de capítulos novos ainda sem render)
  --audio  capítulos que só ganharam narração nova, com a MESMA duração (o "narration" do caps/capNN.chapter.json aponta
           para a emenda); o vídeo deles não muda
  --novos  capítulos regravados e já renderizados pelo render_chapter.py (out/capNN/capNN.mp4, .wav e .edit.json), com a
           duração que tiverem; o que vem depois deles na linha do tempo se desloca
  --plano  só imprime o plano (linha do tempo nova, o que é copiado e o que é recodificado); não escreve nada e não pede a trava
  --manter-stems  não apaga proj/build/stems e music.wav depois do mix (por padrão somem: ~1,1 GB numa aula de 12 min)

O que faz (na ordem do finish.py, mas só no que mudou):
  1. voz: refaz proj/audio48k.wav (fatias do áudio antigo dos capítulos que não mudaram + o áudio novo dos que mudaram),
     proj/edl.json (eventos dos capítulos antigos deslocados) e capitulos.json
  2. kit/mix.py (trilha + ducking + SFX) e os SFX das vinhetas de capítulo, como no finish.py
  3. vídeo: copia bit a bit (pacotes, com PyAV) tudo o que não mudou e recodifica (mesmos parâmetros do finish.py) só as
     vinhetas de capítulo que encostam num capítulo novo, os capítulos novos e, no máximo, ~2 s de cada lado (até o
     keyframe vizinho; o GOP do x264 é fechado, então o corte é limpo). Só-áudio: nenhum quadro muda
  4. mux AAC 192k; tudo é escrito em arquivo temporário e trocado no fim (aula_final.mp4 costuma ter hardlinks em entrega/ e
     entrega_final/: `ffmpeg -y` no mesmo nome truncaria a entrega antiga no meio do caminho)
  Se a execução cair no meio, o estado antigo fica em <out>/_base (hardlinks) e a próxima execução parte dele; no fim bem
  sucedido o _base some.
Pesado: reexecuta sozinho sob flock .heavy.lock + nice (como o finish.py). Depois: legendas_aula.py e entregar.py."""
import json
import os
import shutil
import subprocess
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
argv = sys.argv[1:]
opt = lambda k, d=None: argv[argv.index(k) + 1] if k in argv else d  # noqa: E731
if "--help" in argv or not argv:
    print(__doc__)
    sys.exit(0)
from common import ensure_heavy, probe, Reader, KIT, DOMI  # noqa: E402

PLANO = "--plano" in argv
if not PLANO:
    ensure_heavy()
import soundfile as sf  # noqa: E402
from scipy.signal import butter, sosfilt  # noqa: E402

W, H, FPS, SR = 1920, 1080, 30, 48000
XF_IN, XF_OUT = 0.4, 0.5  # os mesmos do kit/render.py, kit/mix.py e finish.py
run = lambda cmd, **kw: subprocess.run(cmd, check=True, **kw)  # noqa: E731
log = lambda *a: print(*a, flush=True)  # noqa: E731

# ------------------------------------------------------------------ entrada
LJ = os.path.abspath(argv[0])
BASE = os.path.dirname(LJ)
L = json.load(open(LJ))
rp = lambda p, b=BASE: p if os.path.isabs(p) else os.path.normpath(os.path.join(b, p))  # noqa: E731
OUT = rp(L.get("out", "out/aula"))
PROJ = os.path.join(OUT, "proj")
BUILD = os.path.join(PROJ, "build")
AUDIO = [x for x in (opt("--audio") or "").split(",") if x]
NOVOS = [x for x in (opt("--novos") or "").split(",") if x]
FRAMES_TESTE = {k: int(v) for k, v in (kv.split("=") for kv in (opt("--frames") or "").split(",") if kv)}
CRF = int(opt("--crf", L.get("crf", 20)))
SFX = L.get("sfx", True)
# 06/11 (T0 v2 9:16): formato vertical como no finish.py ("formato": "9x16" na aula ou --formato 9x16): quadro 1080x1920 e vinheta de
# capítulo do vertical (vinheta_cap_vertical.py); voz, mix, SFX e emenda de pacotes são os mesmos. Sem a opção, nada muda.
FORMATO = opt("--formato", L.get("formato", "16x9"))
if FORMATO not in ("16x9", "9x16"):
    sys.exit(f"formato {FORMATO!r}: use 16x9 (padrão) ou 9x16")
VERT = FORMATO == "9x16"
if VERT:
    import vertical as _V  # noqa: E402
    W, H = _V.W, _V.H

# estado antigo: <out>/_base guarda hardlinks dos 4 arquivos que este script reescreve
ARQS = {"capitulos.json": os.path.join(OUT, "capitulos.json"), "audio48k.wav": os.path.join(PROJ, "audio48k.wav"),
        "edl.json": os.path.join(PROJ, "edl.json"), "video_sem_audio.mp4": os.path.join(OUT, "video_sem_audio.mp4")}
BASEDIR = os.path.join(OUT, "_base")
if os.path.isdir(BASEDIR):
    log("usando o estado antigo guardado em _base (uma execução anterior não terminou)")
elif not PLANO:
    os.makedirs(BASEDIR)
    for _nome, _p in ARQS.items():
        os.link(_p, os.path.join(BASEDIR, _nome))
OLD = lambda nome: os.path.join(BASEDIR, nome) if os.path.isdir(BASEDIR) else ARQS[nome]  # noqa: E731

# capítulos do aula.json -> {nome: (caminho, json)}
CJ = {}
for _p in L["chapters"]:
    _p = rp(_p)
    _ch = json.load(open(_p))
    CJ[_ch.get("name") or os.path.splitext(os.path.basename(_p))[0].replace(".chapter", "")] = (_p, _ch)
for _n in AUDIO + NOVOS:
    if _n not in CJ:
        sys.exit(f"{_n}: não está nos capítulos do {os.path.basename(LJ)}")
if set(AUDIO) & set(NOVOS):
    sys.exit("um capítulo não pode ser --audio e --novos ao mesmo tempo (o --novos já traz a narração nova)")

intro_p, outro_p = os.path.join(BUILD, "intro_v.mp4"), os.path.join(BUILD, "outro_v.mp4")
n_in, n_out, n_xo = (int(round(probe(intro_p)["dur"] * FPS)), int(round(probe(outro_p)["dur"] * FPS)), int(round(XF_OUT * FPS)))

# ------------------------------------------------------------------ linha do tempo antiga e nova
items = []
for c in json.load(open(OLD("capitulos.json")))["chapters"]:
    nm = c["name"]
    it = dict(name=nm, card=nm.startswith("vinheta-"), voz=c.get("voz"), cortes=c.get("cortes") or [], o_frames=int(round(c["dur"] * FPS)),
              o_start_s=float(c["start"]), novo=nm in NOVOS, audio=nm in AUDIO, side=None)
    if it["cortes"] and it["audio"]:
        sys.exit(f"{nm}: capítulo com cortes não é suportado com --audio (use --novos com o render do capítulo, ou o finish.py)")
    it["frames"] = it["o_frames"]
    if it["novo"]:
        outd = os.path.normpath(os.path.join(os.path.dirname(CJ[nm][0]), CJ[nm][1].get("output", {}).get("dir", "out")))
        side = os.path.join(outd, nm + ".edit.json")
        if os.path.exists(side):
            it["side"] = json.load(open(side))
            it["frames"] = int(it["side"]["frames"])
            # 06/11: capítulo novo com "cortes" no JSON (os do capítulo valem, como no finish.py): os quadros desses trechos saem do vídeo,
            # a voz é cortada nos mesmos instantes e os eventos (zoom, aviso, destaque) andam para trás o tanto que foi cortado antes deles
            cut = CJ[nm][1].get("cortes") or []
            it["cortes"] = cut
            if cut:
                n0 = it["frames"]
                keep = [i for i in range(n0) if not any(a_ <= i / FPS < b_ for a_, b_ in cut)]
                it.update(keep=set(keep), frames_src=n0, frames=len(keep))
                log(f"  {nm}: cortes {cut} -> {n0} -> {len(keep)} quadros")
        elif PLANO and nm in FRAMES_TESTE:
            it["frames"] = FRAMES_TESTE[nm]
        else:
            sys.exit(f"{nm}: falta o render ({side}); rode o render_chapter.py antes (ou --frames {nm}=N com --plano)")
    items.append(it)
for _n in AUDIO + NOVOS:
    if not any(i["name"] == _n for i in items):
        sys.exit(f"{_n}: não está no capitulos.json antigo")
for _k, it in enumerate(items):
    if it["card"]:  # a vinheta funde a tela do capítulo de antes com a do de depois: muda se um deles mudou
        it["sujo"] = any(items[j]["novo"] for j in (_k - 1, _k + 1) if 0 <= j < len(items))
    else:
        it["sujo"] = it["novo"]
_o, _n = n_in, n_in  # quadro em que cada item começa no vídeo antigo e no novo
for it in items:
    it["o_pos"], it["n_pos"] = _o, _n
    _o += it["o_frames"]
    _n += it["frames"]
O_TOTAL = _o + n_out - n_xo
N_TOTAL = _n + n_out - n_xo
N_C = sum(i["frames"] for i in items)
starts, _t = [], 0.0
for it in items:
    starts.append(_t)
    _t += it["frames"] / FPS
CDUR = round(_t, 3)
log(f"{len(items)} itens | conteúdo {sum(i['o_frames'] for i in items) / FPS:.2f} s -> {N_C / FPS:.2f} s | vídeo {O_TOTAL} -> {N_TOTAL} quadros")
for it in items:
    if it["novo"] or it["audio"] or it["sujo"]:
        log(f"  {it['name']:<14} {'novo' if it['novo'] else 'só áudio novo' if it['audio'] else 'vinheta refeita'}: {it['o_frames']} -> {it['frames']} quadros "
            f"(começa em {starts[items.index(it)]:.2f} s)")
HAS_GEN = any(i["sujo"] for i in items)


# ------------------------------------------------------------------ voz
def narracao_alinhada(cj, ch, frames):
    """igual ao Chapter.align_audio do render_chapter.py (mono 48 kHz float32 alinhado ao vídeo do capítulo), sem abrir o vídeo"""
    from math import gcd
    from scipy.signal import resample_poly
    nar = rp(ch["narration"], os.path.dirname(cj))
    off = float(ch.get("audio_offset", 0.0))
    t0 = float(ch.get("trim", {}).get("start", 0.0))
    n_o = int(round(frames / FPS * SR))
    y = np.zeros(n_o, np.float32)
    x, sr = sf.read(nar, dtype="float32", always_2d=True)
    x = x.mean(1)
    if sr != SR:
        g = gcd(SR, sr)
        x = resample_poly(x, SR // g, sr // g).astype(np.float32)
    s0 = int(round((t0 - off) * SR))
    a, b = max(0, s0), min(len(x), s0 + n_o)
    if b > a:
        y[a - s0:b - s0] = x[a:b]
    f = int(0.004 * SR)
    y[:f] *= np.linspace(0, 1, f)
    y[-f:] *= np.linspace(1, 0, f)
    return y


def segmentos(db, floor, top):
    """fala/pausa pela energia de 10 ms (igual ao finish.py)"""
    thr = max(floor + 12, top - 32)
    loud = db > thr
    idx = np.flatnonzero(loud)
    for a, b in zip(idx[:-1], idx[1:]):  # fecha buracos < 0,12 s
        if 1 < b - a <= 13:
            loud[a:b] = True
    spans, i = [], 0
    while i < len(loud):
        if loud[i]:
            j = i
            while j < len(loud) and loud[j]:
                j += 1
            if j - i >= 6:
                spans.append([max(0.0, i * 0.01 - 0.10), min(CDUR, j * 0.01 + 0.15)])
            i = j
        else:
            i += 1
    speech = []
    for s, e in spans:
        if speech and s - speech[-1][1] < 0.55:
            speech[-1][1] = max(speech[-1][1], e)
        else:
            speech.append([s, e])
    segs, cur = [], 0.0
    q = lambda v: round(v * FPS) / FPS  # noqa: E731
    for s, e in speech + [[CDUR, CDUR]]:
        s, e = q(s), q(e)
        if s > cur:
            segs.append((cur, s, "pausa"))
        if e > s:
            segs.append((s, e, "fala"))
        cur = max(cur, e)
    return thr, speech, [dict(src_s=a, src_e=b, speed=1.0, kind=k, out_s=a, out_e=b) for a, b, k in segs if b > a]


def refazer_voz():
    log("voz: refazendo proj/audio48k.wav, edl.json e capitulos.json ...")
    old_wav = sf.SoundFile(OLD("audio48k.wav"))
    assert old_wav.samplerate == SR and old_wav.channels == 1
    o_off, energia = 0, []
    tmp = os.path.join(PROJ, "audio48k.wav.novo")
    with sf.SoundFile(tmp, "w", SR, 1, "FLOAT", format="WAV") as fo:  # a extensão .novo não diz o formato
        for it in items:
            n_old, n = it["o_frames"] * SR // FPS, it["frames"] * SR // FPS
            if it["novo"]:
                wav = (it["side"] or {}).get("wav")
                x = sf.read(wav, dtype="float32")[0] if wav else np.zeros(n, np.float32)
                x = x.mean(1) if x.ndim == 2 else x
                if it.get("keep") is not None and wav:  # cortes: as mesmas amostras que o finish.py tira
                    tt = np.arange(len(x)) / SR
                    m_ = np.ones(len(x), bool)
                    for a_, b_ in it["cortes"]:
                        m_ &= ~((tt >= a_) & (tt < b_))
                    x = x[m_]
            elif it["audio"]:
                x = narracao_alinhada(CJ[it["name"]][0], CJ[it["name"]][1], it["frames"])
            else:  # não mudou: fatia do áudio antigo, idêntica
                old_wav.seek(o_off)
                x = old_wav.read(n_old, dtype="float32")
            o_off += n_old
            x = np.pad(x, (0, max(0, n - len(x))))[:n]
            fo.write(x)
            y = sosfilt(butter(2, 90 / (SR / 2), "hp", output="sos"), x)
            hop = SR // 100
            m = len(y) // hop
            energia.append(10 * np.log10((y[:m * hop].reshape(m, hop).astype(np.float64) ** 2).mean(1) + 1e-12))
    old_wav.close()
    os.replace(tmp, os.path.join(PROJ, "audio48k.wav"))
    db = np.concatenate(energia)
    floor, top = np.percentile(db, 10), np.percentile(db, 97)
    if top < -70:
        sys.exit("sem narração em nenhum capítulo: nada para mixar")
    thr, speech, segs = segmentos(db, floor, top)
    edl_old = json.load(open(OLD("edl.json")))

    def eventos(chave):  # SFX por capítulo: os do edl antigo (deslocados) ou, nos capítulos novos, os do .edit.json
        out = []
        for it, st in zip(items, starts):
            if it["card"]:
                continue
            if it["novo"]:
                sd = it["side"] or {}
                cut = it["cortes"] if it.get("keep") is not None else []
                mp = lambda t, cut=cut: t - sum(min(max(t - a_, 0.0), b_ - a_) for a_, b_ in cut)  # noqa: E731  (a do finish.py)
                if chave == "zooms":
                    out += [dict(s_out=round(st + mp(float(z)), 3)) for z in sd.get("zoom_in", [])]
                else:
                    out += [dict(s_out=round(st + mp(float(k["at"])), 3)) for k in sd.get(chave, [])]
            else:
                a, b = it["o_start_s"] - 1e-6, it["o_start_s"] + it["o_frames"] / FPS - 1e-6
                out += [dict(e, s_out=round(e["s_out"] - it["o_start_s"] + st, 3)) for e in edl_old.get(chave, []) if a <= e["s_out"] < b]
        return out if SFX else []

    chapters = [dict(t_out=round(st + 0.30, 3), title=CJ[it["name"][len("vinheta-"):]][1]["card"]["title"])
                for it, st in zip(items, starts) if it["card"] and SFX]
    edl = dict(fps=FPS, src_dur=CDUR, out_dur=CDUR, segments=segs, noise_floor_db=round(float(floor), 1), speech_thr_db=round(float(thr), 1),
               chapters=chapters, zooms=eventos("zooms"), callouts=eventos("callouts"), spots=eventos("spots"))
    json.dump(edl, open(os.path.join(PROJ, "edl.json.novo"), "w"), ensure_ascii=False, indent=1)
    os.replace(os.path.join(PROJ, "edl.json.novo"), os.path.join(PROJ, "edl.json"))
    json.dump(L.get("mix", {}), open(os.path.join(PROJ, "render.json"), "w"))
    caps = dict(chapters=[dict(name=it["name"], start=s, dur=it["frames"] / FPS, cortes=it["cortes"], voz=it["voz"]) for s, it in zip(starts, items)])
    json.dump(caps, open(os.path.join(OUT, "capitulos.json.novo"), "w"), indent=1, ensure_ascii=False)
    os.replace(os.path.join(OUT, "capitulos.json.novo"), os.path.join(OUT, "capitulos.json"))
    log(f"voz: {len(speech)} blocos de fala | limiar {thr:.1f} dB, piso {floor:.1f} dB | eventos: {len(edl['zooms'])} zooms, "
        f"{len(edl['callouts'])} avisos, {len(edl['spots'])} destaques, {len(chapters)} vinhetas")


def refazer_mix():
    run([sys.executable, os.path.join(KIT, "mix.py"), PROJ])
    if "--manter-stems" not in argv:  # stems e trilha só servem ao mix: apagá-los poupa ~1,1 GB numa aula de 12 min
        assert os.path.basename(BUILD) == "build" and os.path.basename(PROJ) == "proj"
        shutil.rmtree(os.path.join(BUILD, "stems"), ignore_errors=True)
        if os.path.exists(os.path.join(BUILD, "music.wav")):
            os.remove(os.path.join(BUILD, "music.wav"))
    if any(i["card"] for i in items):  # SFX também na saída da vinheta (Kaik 15:43), como no finish.py
        sys.path.insert(0, os.path.join(DOMI, "audio"))
        from kit import whoosh, pop, limit  # noqa: E402
        mw, _ = sf.read(os.path.join(BUILD, "mix.wav"), dtype="float64")
        t_in = probe(intro_p)["dur"]

        def put(sig, t, db):
            sig = np.asarray(sig, np.float64) * 10 ** (db / 20)
            sig = sig if sig.ndim == 2 else np.stack([sig, sig], 1)
            i_ = int(t * SR)
            n_ = min(len(sig), len(mw) - i_)
            if n_ > 0 and i_ >= 0:
                mw[i_:i_ + n_] += sig[:n_]

        for st, it in zip(starts, items):
            if not it["card"]:
                continue
            t0 = t_in + st
            put(whoosh(0.42, 500, 2600, 1.0, -0.3, seed=7), t0 + 0.02, -15)
            put(pop(79, 1.0), t0 + 0.52, -22)
            put(whoosh(0.45, 2600, 600, 1.0, 0.3, seed=9), t0 + it["frames"] / FPS - 0.62, -16)
        sf.write(os.path.join(BUILD, "mix.wav"), limit(mw, -1.0).astype(np.float32), SR, subtype="FLOAT")
        log("SFX das vinhetas de capítulo: ok")


# ------------------------------------------------------------------ vídeo
def encoder(saida):
    """os mesmos parâmetros do finish.py (e a mesma escala de tempo, 15360), saindo num MP4 próprio: os pacotes dele, com pts/dts
    certos, entram no vídeo novo (o H.264 puro perde a ordem de exibição dos quadros B)"""
    return subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                             "-vf", "scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p", "-c:v", "libx264",
                             "-preset", "veryfast", "-crf", str(CRF), "-g", "60", "-colorspace", "bt709", "-color_primaries", "bt709",
                             "-color_trc", "bt709", "-color_range", "tv", "-video_track_timescale", "15360", saida], stdin=subprocess.PIPE)


def quadros_antigos(video, i0, n):
    """n quadros RGB do vídeo ANTIGO a partir do quadro i0 (seek até o keyframe anterior e descarte até o instante exato)"""
    rd = Reader(video, W, H, max(0.0, (i0 - 0.25) / FPS), FPS, explicit=False)
    try:
        for _ in range(n):
            yield np.array(rd.next())
    finally:
        rd.close()


class Gerador:
    """gera os quadros dos itens novos e das vinhetas refeitas, na ordem, como o laço de vídeo do finish.py"""

    def __init__(self, video_antigo):
        import cv2  # noqa: E402
        if VERT:
            import vinheta_cap_vertical as VC  # noqa: E402
        else:
            import vinheta_cap as VC  # noqa: E402
        self.cv2, self.VC, self.vo = cv2, VC, video_antigo
        self.last_img, self.last_k, self.bgi = None, -1, None

    def fundo(self):
        if self.bgi is None:
            bgp = next((ch.get("stage", {}).get("bg") for _, ch in CJ.values() if ch.get("stage", {}).get("bg")), None)
            self.bgi = self.cv2.cvtColor(self.cv2.imread(bgp), self.cv2.COLOR_BGR2RGB) if bgp else np.zeros((H, W, 3), np.uint8)
        return self.bgi

    def quadros(self, k):
        it = items[k]
        if it["card"]:
            ant, prox = items[k - 1], items[k + 1]
            prev = self.last_img if self.last_k == k - 1 else next(quadros_antigos(self.vo, ant["o_pos"] + ant["o_frames"] - 1, 1))
            if prox["novo"]:
                rn = Reader(prox["side"]["video"], W, H, explicit=False)
                first = np.array(rn.next())
                rn.close()
            else:
                first = next(quadros_antigos(self.vo, prox["o_pos"], 1))
            cd = CJ[it["name"][len("vinheta-"):]][1]["card"]
            card = self.VC.Card(cd.get("kicker", ""), cd["title"], self.fundo(), dur=it["frames"] / FPS)
            for fi in range(it["frames"]):
                yield np.ascontiguousarray(card.frame(fi / FPS, prev, first))
            return
        base_idx = sum(i["frames"] for i in items[:k])  # c_idx do finish.py: índice do quadro entre todos os itens
        rd = Reader(it["side"]["video"], W, H, explicit=False)
        last_intro = next(quadros_antigos(intro_p, n_in - 1, 1)) if k == 0 else None
        r_out = Reader(outro_p, W, H, explicit=False) if k == len(items) - 1 and n_out else None
        keep, src_i = it.get("keep"), -1  # cortes: pula os quadros cortados, como o laço do finish.py
        for f in range(it["frames"]):
            img = rd.next()
            src_i += 1
            while keep is not None and src_i not in keep:
                img = rd.next()
                src_i += 1
            self.last_img, self.last_k = np.array(img), k
            c_idx = base_idx + f
            if last_intro is not None and c_idx < int(round(XF_IN * FPS)):
                p = c_idx / (XF_IN * FPS)
                img = (img.astype(np.float32) * p + last_intro.astype(np.float32) * (1 - p)).astype(np.uint8)
            if r_out is not None and c_idx >= N_C - n_xo:
                o = r_out.next()
                p = (c_idx - (N_C - n_xo) + 1) / (n_xo + 1)
                img = (img.astype(np.float32) * (1 - p) + o.astype(np.float32) * p).astype(np.uint8)
            yield np.ascontiguousarray(img)
        rd.close()
        if r_out is not None:
            r_out.close()


def planejar(idr):
    """lista de operações na ordem do vídeo novo: {"t": "copia", "a", "b"} (quadros do vídeo antigo, de IDR a IDR) ou
    {"t": "gera", "src": [("antigo", i0, n) | ("itens", [k, ...])]} (recodifica). Os quadros antigos que sobram entre um item
    gerado e o IDR vizinho vão para a recodificação (a cópia só começa e termina num IDR)."""
    runs = [dict(kind="old", a=0, b=n_in)]  # vinheta da aula
    for k, it in enumerate(items):
        if it["sujo"]:
            if runs[-1]["kind"] == "gen":
                runs[-1]["ks"].append(k)
            else:
                runs.append(dict(kind="gen", ks=[k]))
        else:
            a, b = it["o_pos"], it["o_pos"] + it["o_frames"]
            if runs[-1]["kind"] == "old" and runs[-1]["b"] == a:
                runs[-1]["b"] = b
            else:
                runs.append(dict(kind="old", a=a, b=b))
    runs.append(dict(kind="old", a=O_TOTAL - (n_out - n_xo), b=O_TOTAL))  # o resto da cartela
    if runs[-2]["kind"] == "old" and runs[-2]["b"] == runs[-1]["a"]:
        runs[-2]["b"] = runs[-1]["b"]
        runs.pop()
    ops, fringe, juntar = [], None, False
    for n_r, r in enumerate(runs):
        if r["kind"] == "gen":
            if juntar and ops and ops[-1]["t"] == "gera":
                g = ops[-1]
            else:
                g = dict(t="gera", src=[])
                ops.append(g)
            juntar = False
            if fringe:
                g["src"].append(fringe)
                fringe = None
            g["src"].append(("itens", r["ks"]))
            continue
        a, b = r["a"], r["b"]
        esq = bool(ops) and ops[-1]["t"] == "gera"   # há recodificação logo antes
        dir_ = n_r + 1 < len(runs)                   # há recodificação logo depois
        s = min([i for i in idr if a <= i <= b] + [b]) if esq else a
        e = max([i for i in idr if a <= i <= b] or [a]) if dir_ else b
        if s < e:
            if esq and s > a:
                ops[-1]["src"].append(("antigo", a, s - a))
            ops.append(dict(t="copia", a=s, b=e))
            if dir_ and e < b:
                fringe = ("antigo", e, b - e)
        else:  # não sobra um GOP inteiro para copiar: o pedaço todo é recodificado, uma vez só
            g = ops[-1] if esq else dict(t="gera", src=[])
            if not esq:
                ops.append(g)
            g["src"].append(("antigo", a, b - a))
            juntar = True
    return ops


def descrever(ops):
    tot_c = tot_g = 0
    for o in ops:
        if o["t"] == "copia":
            tot_c += o["b"] - o["a"]
            log(f"  copia      quadros antigos {o['a']:>6}-{o['b']:<6} ({(o['b'] - o['a']) / FPS:7.1f} s)")
        else:
            nq = sum(f[2] if f[0] == "antigo" else sum(items[j]["frames"] for j in f[1]) for f in o["src"])
            tot_g += nq
            log(f"  recodifica {nq:>5} quadros ({nq / FPS:6.1f} s): " + " + ".join(
                f"antigo {f[1]}+{f[2]}" if f[0] == "antigo" else "/".join(items[j]["name"] for j in f[1]) for f in o["src"]))
    log(f"  total {tot_c + tot_g} quadros ({tot_c} copiados, {tot_g} recodificados); esperado {N_TOTAL}")
    return tot_c + tot_g


def refazer_video():
    import av  # PyAV: emenda os pacotes (com pts/dts) do vídeo antigo e dos trechos recodificados, sem recodificar o resto
    old_mp4 = OLD("video_sem_audio.mp4")
    tmpd = os.path.join(OUT, "_tmp_remendo")
    os.makedirs(tmpd, exist_ok=True)
    cm = av.open(old_mp4)
    vm = cm.streams.video[0]
    idr, n = [], 0
    for p in cm.demux(vm):
        if p.dts is None:
            continue
        if p.is_keyframe:
            idr.append(n)
        n += 1
    log(f"vídeo antigo: {n} quadros, {len(idr)} keyframes IDR (a linha do tempo antiga tem {O_TOTAL})")
    if n != O_TOTAL:
        sys.exit("o vídeo antigo não tem os quadros da linha do tempo antiga: não é o mesmo vídeo")
    ops = planejar(idr)
    if descrever(ops) != N_TOTAL:
        sys.exit("o plano não fecha com o número de quadros novo")
    if PLANO:
        cm.close()
        os.rmdir(tmpd)
        return None
    passo = int(round(1 / (FPS * float(vm.time_base))))  # ticks por quadro (512 com a escala 15360)
    tmp_mp4 = os.path.join(OUT, "video_sem_audio.mp4.novo")
    out = av.open(tmp_mp4, "w", format="mp4", options={"movflags": "+faststart"})
    sv = out.add_stream_from_template(vm)
    sv.time_base = vm.time_base
    cm2 = av.open(old_mp4)  # segundo acesso ao antigo: leitura sequencial só para as cópias
    vm2 = cm2.streams.video[0]
    it = (p for p in cm2.demux(vm2) if p.dts is not None)
    pos, D = 0, 0  # pos: próximo pacote antigo; D: quadros já escritos no novo
    g = Gerador(old_mp4)
    feitos, t0 = 0, time.time()

    def poe(p, off):
        p.pts += off
        p.dts += off
        p.stream = sv
        out.mux(p)

    for n_op, o in enumerate(ops):
        if o["t"] == "copia":
            while pos < o["a"]:
                next(it)
                pos += 1
            desloc = (D - o["a"]) * passo  # fixo para a operação toda (D cresce a cada quadro copiado)
            for _ in range(o["b"] - o["a"]):
                poe(next(it), desloc)
                pos += 1
                D += 1
            continue
        dst = os.path.join(tmpd, f"gera{n_op}.mp4")
        enc = encoder(dst)
        for f in o["src"]:
            src = quadros_antigos(old_mp4, f[1], f[2]) if f[0] == "antigo" else (q for j in f[1] for q in g.quadros(j))
            for img in src:
                enc.stdin.write(np.ascontiguousarray(img).tobytes())
                feitos += 1
                if feitos % 150 == 0:
                    print(f"\r{feitos} quadros recodificados  {feitos / (time.time() - t0):.1f} q/s", end="", flush=True)
        enc.stdin.close()
        enc.wait()
        cg = av.open(dst)
        vg = cg.streams.video[0]
        if bytes(vg.codec_context.extradata or b"") != bytes(vm.codec_context.extradata or b"") or vg.time_base != vm.time_base:
            sys.exit("o trecho recodificado não tem os mesmos parâmetros (SPS/PPS, escala de tempo) do vídeo antigo: não dá para emendar")
        n_g = 0
        for p in cg.demux(vg):
            if p.dts is None:
                continue
            poe(p, D * passo)
            n_g += 1
        cg.close()
        os.remove(dst)
        D += n_g
    print()
    out.close()
    cm.close()
    cm2.close()
    os.rmdir(tmpd)
    st = json.loads(subprocess.run(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries",
                                    "stream=nb_read_packets,r_frame_rate,duration", "-of", "json", tmp_mp4], capture_output=True, text=True,
                                   check=True).stdout)["streams"][0]
    log(f"vídeo novo: {st['nb_read_packets']} pacotes, {st['r_frame_rate']}, {float(st['duration']):.3f} s (esperado {N_TOTAL} quadros = {N_TOTAL / FPS:.3f} s)")
    if int(st["nb_read_packets"]) != N_TOTAL or D != N_TOTAL:
        sys.exit("o vídeo remendado não tem o número de quadros esperado: nada foi trocado")
    return tmp_mp4, None


def mux(video):
    tmp = os.path.join(OUT, "aula_final.mp4.novo")
    run(["ffmpeg", "-v", "error", "-y", "-i", video, "-i", os.path.join(BUILD, "mix.wav"), "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac",
         "-b:a", "192k", "-ar", "48000", "-ac", "2", "-shortest", "-movflags", "+faststart", "-f", "mp4", tmp])
    return tmp


if __name__ == "__main__":
    t_ini = time.time()
    if PLANO:
        if HAS_GEN:
            refazer_video()  # com --plano só lê o vídeo antigo (keyframes) e imprime o plano
        else:
            log("só áudio: nenhum quadro de vídeo muda; o vídeo antigo vale")
        sys.exit(0)
    refazer_voz()
    refazer_mix()
    tmpd = None
    if HAS_GEN:
        tmp_mp4, tmpd = refazer_video()
        os.replace(tmp_mp4, os.path.join(OUT, "video_sem_audio.mp4"))
    final_tmp = mux(os.path.join(OUT, "video_sem_audio.mp4"))
    os.replace(final_tmp, os.path.join(OUT, "aula_final.mp4"))
    if tmpd:
        for f_ in os.listdir(tmpd):
            os.remove(os.path.join(tmpd, f_))
        os.rmdir(tmpd)
    for f_ in os.listdir(BASEDIR):
        os.remove(os.path.join(BASEDIR, f_))
    os.rmdir(BASEDIR)
    pr = probe(os.path.join(OUT, "aula_final.mp4"))
    log(f"ok {os.path.join(OUT, 'aula_final.mp4')}  ({pr['dur']:.1f} s; {(time.time() - t_ini) / 60:.1f} min). Depois: legendas_aula.py e entregar.py")
