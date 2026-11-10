"""Capítulos ilustrados (sem gravação): gera, a partir da narração já processada (<tutorial>/narracao/capNN.json),
a telemetria mínima de cada capítulo (sem mouse), o JSON de capítulo do editor (câmera sem zoom automático, cursor
oculto) e o JSON da aula para o finish.py. O vídeo de cada capítulo é a animação de cenas.html (render_todos.sh).

uso: python3 capitulos_ilustrados.py "<Título da aula>" [--cauda 1.2] [--aula T0] [--formato 9x16]
     (rode de dentro de <tutorial>/edit/cenas; vinhetas de capítulo = TITULOS/KICKERS do narracao/tts_textos.py)
Saídas: $TUT_HOME/rec/<tut>/<tut>-capNN.telemetry.json, <tutorial>/edit/caps/capNN.chapter.json e <AULA>.aula.json.
--formato 9x16 (vertical, docs/09-aula-ilustrada.md): os vídeos são os de render_todos_vertical.sh (<tut>-capNN-9x16.mp4, o quadro
final 1080x1920); gera caps/capNN.9x16.chapter.json (saída em out/capNN_9x16) e caps/<AULA>.9x16.aula.json (out/<AULA>_9x16,
"formato": "9x16"); sem telemetria (não há mouse nem câmera). Os do 16:9 não são tocados."""
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EDIT = os.path.dirname(HERE); TUT = os.path.dirname(EDIT); DOMI = os.path.dirname(TUT); NOME = os.path.basename(TUT)
argv = sys.argv[1:]
if not argv or argv[0].startswith("-"):
    sys.exit(__doc__)
opt = lambda k, d=None: argv[argv.index(k) + 1] if k in argv else d  # noqa: E731
TITULO, CAUDA, AULA = argv[0], float(opt("--cauda", 1.2)), opt("--aula", NOME.upper())
VERT = opt("--formato", "16x9") == "9x16"  # vertical: arquivos com sufixo próprio, ao lado dos do 16:9
sys.path.insert(0, os.path.join(TUT, "narracao"))
try:
    import tts_textos as T  # noqa: E402
    TITULOS, KICKERS = getattr(T, "TITULOS", {}), getattr(T, "KICKERS", {})
except ImportError:
    TITULOS, KICKERS = {}, {}

os.makedirs(os.path.join(DOMI, "rec", NOME), exist_ok=True)
os.makedirs(os.path.join(EDIT, "caps"), exist_ok=True)
fundo = os.path.join(EDIT, "assets", "fundo_escuro_9x16.png" if VERT else "fundo_escuro.png")
nomes = []
for cj in sorted(glob.glob(os.path.join(TUT, "narracao", "cap[0-9][0-9].json"))):
    n = json.load(open(cj)); nn = os.path.basename(cj)[3:5]; k = int(nn); dur = round(n["dur"] + CAUDA, 3)
    base = os.path.join(DOMI, "rec", NOME, f"{NOME}-cap{nn}")
    if VERT:  # o vídeo já é o quadro final 1080x1920: sem telemetria, câmera, cursor nem zoom (render_chapter_vertical.py)
        ch = {"name": f"cap{nn}", "video": base + "-9x16.mp4", "narration": os.path.join(n["pasta"], "audio48k.wav"), "audio_offset": 0.0,
              "trim": {"start": 0.0, "end": dur}, "stage": {"bg": fundo, "shadow": 0.35}, "spots": [], "callouts": [],
              "output": {"dir": os.path.join(EDIT, "out", f"cap{nn}_9x16")}}
    else:
        json.dump({"video": {"width": 2560, "height": 1600, "fps": 30, "durationS": dur, "dsf": 2,
                             "viewportCss": {"width": 1280, "height": 800}},
                   "clock": "t = segundos desde o 1o quadro do video", "units": "pixels do video (2560x1600)",
                   "cursorKinds": "arrow", "counts": {"move": 1}, "origem": "capítulo ilustrado (cenas.html), sem mouse",
                   "samples": [{"t": 0, "x": 1280, "y": 800, "type": "move", "cursor": "arrow", "src": "inicio"}]},
                  open(base + ".telemetry.json", "w"), indent=1)
        ch = {"name": f"cap{nn}", "video": base + ".mp4", "telemetry": base + ".telemetry.json",
              "narration": os.path.join(n["pasta"], "audio48k.wav"), "audio_offset": 0.0, "trim": {"start": 0.0, "end": dur},
              "camera": {"auto": False, "depth": 1.8}, "cursor": {"show": False}, "stage": {"bg": fundo, "shadow": 0.35},
              "zooms": [], "spots": [], "callouts": [], "illustrations": [],
              "output": {"dir": os.path.join(EDIT, "out", f"cap{nn}"), "crf": 18, "preset": "veryfast"}}
    if k in TITULOS:
        ch["card"] = {"kicker": KICKERS.get(k, ""), "title": TITULOS[k].rstrip(".")}
    p = os.path.join(EDIT, "caps", f"cap{nn}.{'9x16.' if VERT else ''}chapter.json")
    json.dump(ch, open(p, "w"), ensure_ascii=False, indent=1); nomes.append(os.path.basename(p))
    print(f"cap{nn}: {dur:.2f} s{'  vinheta: ' + ch['card']['title'] if 'card' in ch else ''}")
modelo = os.path.join(EDIT, "caps", "aula.modelo.json")
aula = json.load(open(modelo)) if os.path.exists(modelo) else {}
aula = {k: v for k, v in aula.items() if not k.startswith("_")}
aula.update({"title": TITULO, "out": f"../out/{AULA}{'_9x16' if VERT else ''}", "chapters": nomes})
if VERT:
    aula["formato"] = "9x16"
aula.setdefault("outro_line", "Até a próxima aula!")
aula.setdefault("card_voices", "../../narracao/titulos/titulos.json")
p = os.path.join(EDIT, "caps", f"{AULA}.{'9x16.' if VERT else ''}aula.json")
json.dump(aula, open(p, "w"), ensure_ascii=False, indent=1)
print(f"{p}: {len(nomes)} capítulos")
