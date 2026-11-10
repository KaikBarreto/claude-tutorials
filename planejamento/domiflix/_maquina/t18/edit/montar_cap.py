"""Monta o JSON de capítulo do editor (render_chapter.py) a partir da gravação do robô e de uma especificação curta.
Os zooms e destaques apontam para os RÓTULOS dos passos do roteiro do robô (rec/<tutorial>/capNN.json); os retângulos e
instantes vêm do <nome>.actions.json da gravação. A narração é a do capítulo (<tutorial>/narracao/capNN.json -> audio48k.wav),
começando em t=0 do vídeo, como os roteiros foram cronometrados.

uso: python3 <tutorial>/edit/montar_cap.py NN [NN ...]   -> <tutorial>/edit/caps/capNN.chapter.json
especificação: <tutorial>/edit/caps/specs.json
  {"NN": {"titulo": "...", "kicker": "...", "sem_titulo": false,
          "zooms":  [{"de": "<rótulo>", "ate": "<rótulo>"?, "fim": "<rótulo>" | segundos | "+1.5"?, "escala"?, "min_w"?, "atraso"?}],
          "spots":  [{"passo": "<rótulo>", "antes": 1.2, "dur": 1.8, "rotulo": "Novo Cliente"?}],
          "callouts": [{"palavra": [linha, "texto"] | "at": s, "dur": 3, "texto": "...", "pos": "bottom"}],
          "ilustracoes": [{"at"|"palavra", "dur", "src", "box"}]}}"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DOMI = os.path.dirname(os.path.dirname(HERE))
def fundo():
    """palco escuro na cor da marca: gera assets/fundo_escuro.png (fundo_escuro.py) se ainda não existir"""
    p = os.path.join(HERE, "assets", "fundo_escuro.png")
    if not os.path.exists(p):
        import subprocess
        subprocess.run([sys.executable, os.path.join(HERE, "fundo_escuro.py"), p], check=True)
    return p


TUT = os.path.basename(os.path.dirname(HERE))  # id do tutorial = nome da pasta (ex.: t3); gravações em rec/<id>/<id>-capNN.*
REC = os.path.join(DOMI, "rec", TUT)
NARR = os.path.join(DOMI, TUT, "narracao")
CAPS = os.path.join(HERE, "caps")
SW, SH = 2560, 1600


def passo(acts, rot):
    m = [a for a in acts if a.get("label") == rot]
    if not m:
        raise SystemExit(f"passo com rótulo {rot!r} não encontrado")
    return m[0]


def uniao(rs):
    x0 = min(r["x"] for r in rs)
    y0 = min(r["y"] for r in rs)
    x1 = max(r["x"] + r["w"] for r in rs)
    y1 = max(r["y"] + r["h"] for r in rs)
    return x0, y0, x1, y1


def ajusta(x0, y0, x1, y1, min_w):
    """garante largura mínima (evita zoom exagerado em alvo pequeno) mantendo o centro, dentro da tela"""
    w, h = x1 - x0, y1 - y0
    if w < min_w:
        cx = (x0 + x1) / 2
        x0, x1 = cx - min_w / 2, cx + min_w / 2
    min_h = min_w * 1600 / 2560 * 0.55
    if h < min_h:
        cy = (y0 + y1) / 2
        y0, y1 = cy - min_h / 2, cy + min_h / 2
    dx = max(0, -x0) - max(0, x1 - SW)
    dy = max(0, -y0) - max(0, y1 - SH)
    x0, x1, y0, y1 = x0 + dx, x1 + dx, y0 + dy, y1 + dy
    return [round(x0), round(y0), round(x1 - x0), round(y1 - y0)]


def t_palavra(narr, ref):
    li, texto = ref
    alvo = texto.lower()
    for w in narr["words"]:
        if w["linha"] == li and w["w"].lower().strip(".,:;!?…") == alvo.strip(".,:;!?…"):
            return w["s"]
    raise SystemExit(f"palavra {ref!r} não achada na narração")


def montar(nn):
    spec = json.load(open(os.path.join(CAPS, "specs.json")))[nn]
    base = os.path.join(REC, f"{TUT}-cap{nn}")
    A = json.load(open(base + ".actions.json"))
    acts = [a for a in A["actions"] if a.get("ok", True)]
    narr = json.load(open(os.path.join(NARR, f"cap{nn}.json")))
    dur_v = float(A["video"]["durationS"])
    ch = {"name": f"cap{nn}", "video": base + ".mp4", "telemetry": base + ".telemetry.json",
          "narration": os.path.join(narr["pasta"], "audio48k.wav"), "audio_offset": 0.0,
          "trim": {"start": 0.0, "end": round(min(dur_v, narr["dur"] + spec.get("cauda", 0.8)), 3)},
          "camera": {"auto": True, "depth": 1.8}, "cursor": {"size": spec.get("cursor", 2.8)},
          "stage": {"bg": fundo(), "shadow": 0.35},
          "zooms": [], "spots": [], "callouts": [], "illustrations": [],
          "output": {"dir": os.path.join(HERE, "out", f"cap{nn}"), "crf": 18, "preset": "veryfast"}}
    if not spec.get("sem_titulo"):  # título vai na vinheta de capítulo (finish.py), não no cartão pequeno do editor
        ch["card"] = {"kicker": spec.get("kicker", ""), "title": spec["titulo"]}
    for z in spec.get("zooms", []):
        a = passo(acts, z["de"])
        b = passo(acts, z.get("ate", z["de"]))
        i0, i1 = acts.index(a), acts.index(b)
        rs = [x["rect"] for x in acts[i0:i1 + 1] if x.get("rect")]
        rect = ajusta(*uniao(rs), z.get("min_w", 1150))
        fim = z.get("fim")
        if fim is None:
            e = b["tEnd"] + 0.4
        elif isinstance(fim, str) and fim.startswith("+"):
            e = b["tEnd"] + float(fim[1:])
        elif isinstance(fim, str):
            e = passo(acts, fim)["tStart"]
        else:
            e = float(fim)
        item = {"at": round(a["tStart"] - 0.2 + float(z.get("atraso", 0)), 3), "end": round(e, 3), "rect": rect}  # atraso: começa depois (clique logo antes)
        if "escala" in z:
            item["scale"] = z["escala"]
        ch["zooms"].append(item)
    for r in spec.get("repouso", []):  # [[de, até], ...] em s: câmera parada (zoom 1) sob uma ilustração que cobre a janela; o zoom automático dos cliques não puxa a tela
        ch["zooms"].append({"at": float(r[0]), "end": float(r[1]), "scale": 1.0, "target": [1280, 800]})
    for s in spec.get("spots", []):
        a = passo(acts, s["passo"])
        r = a["rect"]
        t = a.get("tAct", a["tStart"]) - s.get("antes", 1.2)
        item = {"at": round(t, 3), "dur": s.get("dur", 1.8), "rect": [r["x"], r["y"], r["w"], r["h"]]}
        if s.get("rotulo"):
            item["label"] = s["rotulo"]
        ch["spots"].append(item)
    for c in spec.get("callouts", []):
        t = c["at"] if "at" in c else t_palavra(narr, c["palavra"])
        ch["callouts"].append({"at": round(t, 3), "dur": c.get("dur", 3.0), "text": c["texto"], "pos": c.get("pos", "bottom")})
    for il in spec.get("ilustracoes", []):
        t = il["at"] if "at" in il else t_palavra(narr, il["palavra"])
        item = {k: v for k, v in il.items() if k not in ("palavra",)}
        item["at"] = round(t, 3)
        ch["illustrations"].append(item)
    if spec.get("cortes"):  # trechos parados e sem fala que o finish.py tira (ritmo)
        ch["cortes"] = spec["cortes"]
    os.makedirs(CAPS, exist_ok=True)
    out = os.path.join(CAPS, f"cap{nn}.chapter.json")
    json.dump(ch, open(out, "w"), ensure_ascii=False, indent=1)
    late = max([a.get("lateBy", 0) or 0 for a in A["actions"]] + [0])
    print(f"cap{nn}: vídeo {dur_v:.2f} s, narração {narr['dur']:.2f} s, corte em {ch['trim']['end']:.2f} s, "
          f"{len(ch['zooms'])} zooms, {len(ch['spots'])} destaques, {len(ch['callouts'])} avisos, maior atraso {late:.2f} s -> {out}")


if __name__ == "__main__":
    for nn in sys.argv[1:]:
        montar(f"{int(nn):02d}")
