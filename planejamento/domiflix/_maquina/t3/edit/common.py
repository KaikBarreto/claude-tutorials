"""Utilitarios comuns: trava de processo pesado (flock + nice), ffprobe e leitura sequencial de video por pipe."""
import json, os, subprocess, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DOMI = os.path.dirname(os.path.dirname(HERE))
KIT = os.path.join(DOMI, "kit")
LOCK = os.path.join(DOMI, ".heavy.lock")


def _ppid(pid):
    try: return int(open(f"/proc/{pid}/stat").read().rsplit(")", 1)[1].split()[1])
    except (OSError, ValueError, IndexError): return 0


def lock_held_by_ancestor():
    """True se um processo acima de nos ja segura o .heavy.lock (ex.: o chamador rodou `flock .heavy.lock nice -n 10 python3 ...`)"""
    try:
        ino = os.stat(LOCK).st_ino; anc = set(); pid = os.getpid()
        while pid > 1: anc.add(pid); pid = _ppid(pid)
        for line in open("/proc/locks"):
            f = line.split()
            if len(f) > 5 and f[1] == "FLOCK" and f[5].endswith(f":{ino}") and int(f[4]) in anc: return True
    except OSError: pass
    return False


def ensure_heavy():
    """Todo processo pesado roda sob `flock .heavy.lock nice -n 10` (a gravacao de tela tem prioridade na maquina).
    Se o chamador ja segura o lock, so garante o nice; senao reexecuta sozinho sob flock + nice (sem deadlock)."""
    if os.environ.get("DOMIFLIX_LOCKED") == "1" or lock_held_by_ancestor():
        os.environ["DOMIFLIX_LOCKED"] = "1"
        try: os.nice(max(0, 10 - os.nice(0)))
        except OSError: pass
        return
    open(LOCK, "a").close()
    if subprocess.run(["flock", "-n", LOCK, "true"]).returncode != 0:
        print("aguardando .heavy.lock (outro processo pesado em andamento)...", flush=True)
    os.execvp("flock", ["flock", LOCK, "nice", "-n", "10", "env", "DOMIFLIX_LOCKED=1", sys.executable, os.path.abspath(sys.argv[0])] + sys.argv[1:])


def probe(path):
    j = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", path], capture_output=True, text=True, check=True).stdout)
    vs = next(s for s in j["streams"] if s["codec_type"] == "video")
    num, den = map(int, vs.get("avg_frame_rate", "30/1").split("/")); fps = num / den if den else 30.0
    return dict(w=int(vs["width"]), h=int(vs["height"]), fps=fps, dur=float(j["format"]["duration"]), nb=int(vs.get("nb_frames", 0) or 0))


class Reader:
    """leitura sequencial (streaming) de quadros RGB de um video, a partir de `start` s; um quadro por vez na memoria"""

    def __init__(self, path, w, h, start=0.0, fps=30, explicit=True):
        """explicit=True: o video e da gravacao (bt709 faixa TV); False: segue as marcas do arquivo (vinheta/cartela do kit, sem marcas = padrao do kit)"""
        vf = f"fps={fps},scale=in_color_matrix=bt709:in_range=limited:out_range=full:flags=accurate_rnd+full_chroma_int+bicubic,format=rgb24" if explicit else f"fps={fps},format=rgb24"
        cmd = ["ffmpeg", "-v", "error"] + (["-ss", f"{start:.4f}"] if start > 0 else []) + ["-i", path, "-an", "-vf", vf, "-f", "rawvideo", "-"]
        self.w, self.h, self.n = w, h, w * h * 3; self.last = None
        self.p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=self.n * 2)

    def next(self):
        raw = self.p.stdout.read(self.n)
        if len(raw) < self.n: return self.last  # fim do video: segura o ultimo quadro
        self.last = np.frombuffer(raw, np.uint8).reshape(self.h, self.w, 3)
        return self.last

    def close(self):
        if self.p: self.p.kill(); self.p.wait(); self.p = None


def still(path, t, w, h):
    """um unico quadro RGB (para --stills e folhas de contato)"""
    vf = "scale=in_color_matrix=bt709:in_range=limited:out_range=full:flags=accurate_rnd+full_chroma_int+bicubic,format=rgb24"
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.4f}", "-i", path, "-frames:v", "1", "-an", "-vf", vf, "-f", "rawvideo", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(h, w, 3).copy()
