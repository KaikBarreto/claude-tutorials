"""Monta o JSON de capítulo do editor (render_chapter.py) a partir da gravação do robô e de uma especificação curta.
Os zooms e destaques apontam para os RÓTULOS dos passos do roteiro do robô (rec/<tutorial>/capNN.json); os retângulos e
instantes vêm do <nome>.actions.json da gravação. A narração é a do capítulo (<tutorial>/narracao/capNN.json -> audio48k.wav),
começando em t=0 do vídeo, como os roteiros foram cronometrados.

Computador ou celular, pelo tamanho do vídeo no actions.json (mais alto que largo = celular, T7/T15/T22): a gravação do celular
("device": "phone", quadro 780x1688) ganha o aparelho genérico no palco (`stage.phone`), o toque como anel (`cursor.touch`, sem seta),
câmera depth 2,3 e `min_w` em pixels do vídeo do celular (zoom = 3348 / (min_w * 1,24), entre 1,15x e 3,5x: min_w 1100 ~ 2,4x;
900 ~ 3x; 1400 ~ 1,9x). O computador segue o padrão do T3 (2560x1600, depth 1,8, `min_w` 1150).
Capítulo gravado em dois trechos com a MESMA voz (T15: `09` no computador e `09b` no celular, os dois com a voz de cap09.json):
`"voz_ate": s` corta o primeiro nesse instante da voz (sem cauda) e `"voz_de": s` faz o segundo começar a voz nesse instante
(`audio_offset` = -voz_de; os tempos de palavra dos avisos e ilustrações são descontados). O legendas_aula.py lê o `audio_offset`.

uso: python3 <tutorial>/edit/montar_cap.py NN [NN ...]   (NN = 00, 01, ... ou 09b) -> <tutorial>/edit/caps/capNN.chapter.json
     TUT_REC=<pasta> troca a pasta das gravações (ex.: rec/tN/_ens, para conferir os rótulos do specs contra um ensaio)
especificação: <tutorial>/edit/caps/specs.json
  {"NN": {"titulo": "...", "kicker": "...", "sem_titulo": false, "voz_de"?: s, "voz_ate"?: s, "cauda"?: 0.8, "camera"?: {...},
          "zooms":  [{"de": "<rótulo>", "ate": "<rótulo>"?, "fim": "<rótulo>" | segundos | "+1.5"?, "escala"?, "min_w"?, "atraso"?,
                      "rect"?, "destino"?},
                     {"rect": [x, y, w, h], "at": s, "end": s, "escala"?, "min_w"?}],   # sem passo: área que só a fala cita (T22)
          "spots":  [{"passo": "<rótulo>", "antes": 1.2, "dur": 1.8, "rotulo": "Novo Cliente"?} | {"rect": [x, y, w, h], "at": s, "dur", "rotulo"?}],
          "callouts": [{"palavra": [linha, "texto"] | "at": s, "dur": 3, "texto": "...", "pos": "bottom"}],
          "ilustracoes": [{"at"|"palavra", "dur", "src", "box"}], "repouso": [[de, até], ...]?,
          "cortes": [[de, até], ...]?, "acelera": [[de, até, fator], ...]?}}
  - rótulo repetido no capítulo: "rótulo#2" = a 2ª ocorrência com retângulo (o cursor que rola até o alvo repete o rótulo do passo, T2);
  - zoom com "rect" e passos: o retângulo é o do spec e os tempos seguem os passos (o do passo é só o texto passado pelo cursor, T22);
  - "destino": true num zoom de arrasto: o zoom cabe também o destino (toRect do passo `drag`), não só a alça (T7);
  - "camera": sobrepõe a câmera do capítulo (ex.: {"guard": 1.0}, T7 cap09);
  - "acelera" (T14): trecho sem fala com a tela mexendo (digitação) que o finish.py acelera (mistura de quadros + selo "4x"), em s do
    vídeo do capítulo, fator inteiro >= 2; não pode cruzar um corte."""
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
REC = os.environ.get("TUT_REC") or os.environ.get("T7_REC") or os.path.join(DOMI, "rec", TUT)   # TUT_REC=rec/tN/_ens: confere os rótulos do specs contra um ensaio
NARR = os.path.join(DOMI, TUT, "narracao")
CAPS = os.path.join(HERE, "caps")
SW, SH = 2560, 1600   # computador; montar() lê o tamanho de cada gravação no actions.json (celular: 780x1688)
CAMERA_COMPUTADOR = {"auto": True, "depth": 1.8}
FASE_CELULAR = {"margin": 56, "radius": 46, "shadow": 0.45, "phone": {"bezel": 14}}
CAMERA_CELULAR = {"auto": True, "depth": 2.3}


def passo(acts, rot, com_rect=False):
    """o passo com o rótulo `rot`: o primeiro (com `com_rect`, o primeiro que tem retângulo); "rótulo#k" = o k-ésimo com retângulo"""
    k = None
    if "#" in rot and rot.rsplit("#", 1)[1].isdigit():
        rot, k = rot.rsplit("#", 1)[0], int(rot.rsplit("#", 1)[1])
    m = [a for a in acts if a.get("label") == rot]
    if not m:
        raise SystemExit(f"passo com rótulo {rot!r} não encontrado")
    if k is None and not com_rect:
        return m[0]
    com = [x for x in m if x.get("rect")] or m
    k = k or 1
    if k > len(com):
        raise SystemExit(f"passo {rot!r}#{k}: só há {len(com)} com esse rótulo")
    return com[k - 1]


def uniao(rs):
    x0 = min(r["x"] for r in rs)
    y0 = min(r["y"] for r in rs)
    x1 = max(r["x"] + r["w"] for r in rs)
    y1 = max(r["y"] + r["h"] for r in rs)
    return x0, y0, x1, y1


def ajusta(x0, y0, x1, y1, min_w, celular=False):
    """garante largura mínima (evita zoom exagerado em alvo pequeno) mantendo o centro, dentro da tela"""
    w, h = x1 - x0, y1 - y0
    if w < min_w:
        cx = (x0 + x1) / 2
        x0, x1 = cx - min_w / 2, cx + min_w / 2
    min_h = min_w * (9 / 16 if celular else 1600 / 2560) * 0.55
    if h < min_h:
        cy = (y0 + y1) / 2
        y0, y1 = cy - min_h / 2, cy + min_h / 2
    if celular:   # mais largo que o celular: centra (T7)
        dx = max(0, -x0) - max(0, x1 - SW) if (x1 - x0) <= SW else SW / 2 - (x0 + x1) / 2
        dy = max(0, -y0) - max(0, y1 - SH) if (y1 - y0) <= SH else SH / 2 - (y0 + y1) / 2
    else:
        dx = max(0, -x0) - max(0, x1 - SW)
        dy = max(0, -y0) - max(0, y1 - SH)
    x0, x1, y0, y1 = x0 + dx, x1 + dx, y0 + dy, y1 + dy
    return [round(x0), round(y0), round(x1 - x0), round(y1 - y0)]


def tamanho_do_video(A):
    v = A["video"]
    return int(v.get("width", 2560)), int(v.get("height", 1600))


def t_palavra(narr, ref, voz_de=0.0):
    li, texto = ref
    alvo = texto.lower()
    for w in narr["words"]:
        if w["linha"] == li and w["w"].lower().strip(".,:;!?…") == alvo.strip(".,:;!?…"):
            return w["s"] - voz_de
    raise SystemExit(f"palavra {ref!r} não achada na narração")


def montar(nn):
    global SW, SH
    spec = json.load(open(os.path.join(CAPS, "specs.json")))[nn]
    base = os.path.join(REC, f"{TUT}-cap{nn}")
    A = json.load(open(base + ".actions.json"))
    acts = [a for a in A["actions"] if a.get("ok", True)]
    narr = json.load(open(os.path.join(NARR, f"cap{nn[:2]}.json")))   # 09b usa a voz do cap. 9
    dur_v = float(A["video"]["durationS"])
    SW, SH = tamanho_do_video(A)
    celular = SH > SW
    voz_de = float(spec.get("voz_de", 0.0))
    if spec.get("voz_ate") is not None:   # corta exatamente nesse instante da voz (o resto da fala vai no trecho seguinte)
        fim_trim = float(spec["voz_ate"]) - voz_de
    else:
        fim_trim = narr["dur"] - voz_de + spec.get("cauda", 0.8)
    ch = {"name": f"cap{nn}", "video": base + ".mp4", "telemetry": base + ".telemetry.json",
          "narration": os.path.join(narr["pasta"], "audio48k.wav"), "audio_offset": round(-voz_de, 3) or 0.0,
          "trim": {"start": 0.0, "end": round(min(dur_v, fim_trim), 3)},
          "camera": {**CAMERA_COMPUTADOR, **spec.get("camera", {})}, "cursor": {"size": spec.get("cursor", 2.8)},
          "stage": {"bg": fundo(), "shadow": 0.35},
          "zooms": [], "spots": [], "callouts": [], "illustrations": [],
          "output": {"dir": os.path.join(HERE, "out", f"cap{nn}"), "crf": 18, "preset": "veryfast"}}
    if celular:
        ch["camera"] = {**CAMERA_CELULAR, **spec.get("camera", {})}
        ch["cursor"] = {"show": False, "touch": True, "ring_alpha": 0.7, "size": spec.get("cursor", 2.8)}
        ch["stage"] = {"bg": fundo(), **FASE_CELULAR}
    if not spec.get("sem_titulo"):  # título vai na vinheta de capítulo (finish.py), não no cartão pequeno do editor
        ch["card"] = {"kicker": spec.get("kicker", ""), "title": spec["titulo"]}
    min_w0 = 1100 if celular else 1150
    for z in spec.get("zooms", []):
        if "de" not in z:   # área sem passo do robô (gráfico, aviso, texto): "rect" [x, y, w, h] em px do vídeo + "at"/"end" em s (T22)
            x, y, w, h = z["rect"]
            rect = ajusta(x, y, x + w, y + h, z.get("min_w", min_w0), celular)
            item = {"at": round(float(z["at"]), 3), "end": round(float(z["end"]), 3), "rect": rect}
            if "escala" in z:
                item["scale"] = z["escala"]
            ch["zooms"].append(item)
            continue
        a = passo(acts, z["de"])
        b = passo(acts, z.get("ate", z["de"]))
        i0, i1 = acts.index(a), acts.index(b)
        rs = [x["rect"] for x in acts[i0:i1 + 1] if x.get("rect")]
        if z.get("destino"):  # arrasto: o zoom também cabe o destino (toRect do passo `drag`), não só a alça (T7)
            rs += [x["toRect"] for x in acts[i0:i1 + 1] if x.get("toRect")]
        if "rect" in z:   # retângulo explícito (o do passo é só o texto passado pelo cursor); os tempos seguem os passos (T22)
            x, y, w, h = z["rect"]; rs = [{"x": x, "y": y, "w": w, "h": h}]
        if not rs:
            raise SystemExit(f"zoom {z['de']!r}: nenhum passo com retângulo entre {z['de']!r} e {z.get('ate', z['de'])!r}")
        rect = ajusta(*uniao(rs), z.get("min_w", min_w0), celular)
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
        ch["zooms"].append({"at": float(r[0]), "end": float(r[1]), "scale": 1.0, "target": [SW / 2, SH / 2]})
    for s in spec.get("spots", []):
        if "passo" not in s:   # destaque sem passo do robô ("rect" em px do vídeo, "at" em s do capítulo; T22)
            item = {"at": round(float(s["at"]), 3), "dur": s.get("dur", 1.8), "rect": [float(v) for v in s["rect"]]}
            if s.get("rotulo"):
                item["label"] = s["rotulo"]
            ch["spots"].append(item)
            continue
        a = passo(acts, s["passo"], com_rect=True)
        if not a.get("rect"):
            raise SystemExit(f"destaque {s['passo']!r}: o passo não tem retângulo (use \"rect\" e \"at\")")
        r = a["rect"]
        t = a.get("tAct", a["tStart"]) - s.get("antes", 1.2)
        item = {"at": round(t, 3), "dur": s.get("dur", 1.8), "rect": [r["x"], r["y"], r["w"], r["h"]]}
        if s.get("rotulo"):
            item["label"] = s["rotulo"]
        ch["spots"].append(item)
    for c in spec.get("callouts", []):
        t = c["at"] if "at" in c else t_palavra(narr, c["palavra"], voz_de)
        ch["callouts"].append({"at": round(t, 3), "dur": c.get("dur", 3.0), "text": c["texto"], "pos": c.get("pos", "bottom")})
    for il in spec.get("ilustracoes", []):
        t = il["at"] if "at" in il else t_palavra(narr, il["palavra"], voz_de)
        item = {k: v for k, v in il.items() if k not in ("palavra",)}
        item["at"] = round(t, 3)
        ch["illustrations"].append(item)
    if spec.get("cortes"):  # trechos parados e sem fala que o finish.py tira (ritmo)
        ch["cortes"] = spec["cortes"]
    if spec.get("acelera"):  # trechos sem fala com a tela mexendo, acelerados pelo finish.py (mistura de quadros + selo; T14)
        for a_, b_, k_ in spec["acelera"]:
            if not (b_ > a_ and int(k_) >= 2):
                raise SystemExit(f"acelera inválido: {[a_, b_, k_]} (use [de, até, fator inteiro >= 2])")
            if any(a_ < y and x < b_ for x, y in spec.get("cortes", [])):
                raise SystemExit(f"acelera {[a_, b_]} cruza um corte")
        ch["acelera"] = spec["acelera"]
    os.makedirs(CAPS, exist_ok=True)
    out = os.path.join(CAPS, f"cap{nn}.chapter.json")
    json.dump(ch, open(out, "w"), ensure_ascii=False, indent=1)
    late = max([a.get("lateBy", 0) or 0 for a in A["actions"]] + [0])
    print(f"cap{nn}: vídeo {dur_v:.2f} s ({SW}x{SH}{', celular' if celular else ''}), narração {narr['dur'] - voz_de:.2f} s, "
          f"corte em {ch['trim']['end']:.2f} s, {len(ch['zooms'])} zooms, {len(ch['spots'])} destaques, {len(ch['callouts'])} avisos, "
          f"{len(ch['illustrations'])} ilustrações, maior atraso {late:.2f} s -> {out}")


if __name__ == "__main__":
    for nn in sys.argv[1:]:
        montar(f"{int(nn[:-1]):02d}b" if nn.endswith("b") else f"{int(nn):02d}")
