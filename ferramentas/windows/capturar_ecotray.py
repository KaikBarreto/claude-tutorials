"""Captura as janelas de verdade do EcoTray (painel e instalador) nos estados que a cena pede.

Cada sessão do plano roda o código do app (somente leitura) num display virtual do tamanho da tela simulada, numa rede
própria (unshare -n: o EcoTray falso ocupa a 8054 sem brigar com o EcoTray falso do robô) e grava em <saida>/ um PNG por
captura + quadros.json (posição da janela na tela e alvos para o cursor). Sessão que não mudou (mesmo plano e mesmo
código do app) não roda de novo.

uso: python3 capturar_ecotray.py <plano.json> <saida/> [--app <pasta ecotray do app>] [--refazer]
     a pasta do app vem de --app, ou de $ECOTRAY_SRC, ou de $APP_SRC/ecotray
Precisa de: Xvfb, unshare (util-linux) e o Python com Tk de preparar.sh (chamado sozinho se faltar).
Formato do plano e exemplos: docs/10-cena-windows.md e exemplos/ecoflix-ecotray/."""
import fcntl
import hashlib
import json
import os
import socket
import struct
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.environ.get("CENA_WIN_CACHE", "/dev/shm/cena-windows")


def opt(argv, k, d=None):
    return argv[argv.index(k) + 1] if k in argv else d


def lo_up():
    """sobe a interface de loopback da rede nova (sem o comando ip)"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ifr = struct.pack("16sh", b"lo", 0)
    flags = struct.unpack("16sh", fcntl.ioctl(s, 0x8913, ifr))[1]
    fcntl.ioctl(s, 0x8914, struct.pack("16sh", b"lo", flags | 1))


def env_tk():
    envf = os.path.join(CACHE, "env.sh")
    if not os.path.exists(envf):
        subprocess.run(["bash", os.path.join(HERE, "preparar.sh")], check=True, env=dict(os.environ, CENA_WIN_CACHE=CACHE))
    env = dict(os.environ)
    for linha in open(envf):
        if linha.startswith("export "):
            k, v = linha[7:].strip().split("=", 1); v = v.strip('"')
            v = v.replace("${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}", (":" + env["LD_LIBRARY_PATH"]) if env.get("LD_LIBRARY_PATH") else "")
            env[k] = v
    return env


def dentro(plano, saida, app, sessao, tela):
    """já na rede própria: loopback, Xvfb do tamanho da tela simulada a 96 dpi (Windows a 100%) e a sessão"""
    try:
        lo_up()
    except OSError as e:
        print(f"aviso: loopback da rede nova não subiu ({e})", flush=True)
    r, w = os.pipe()
    xv = subprocess.Popen(["Xvfb", "-displayfd", str(w), "-screen", "0", f"{tela[0]}x{tela[1]}x24", "-dpi", "96",
                           "-nolisten", "tcp", "-noreset"], pass_fds=(w,), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.close(w)
    num = b""
    while not num.endswith(b"\n"):
        ch = os.read(r, 1)
        if not ch:
            break
        num += ch
    os.close(r)
    if not num.strip():
        xv.terminate(); sys.exit("Xvfb não subiu")
    env = env_tk(); env.update(DISPLAY=f":{num.decode().strip()}", SIM_SESSAO=sessao, PYTHONDONTWRITEBYTECODE="1")
    try:
        rc = subprocess.run([env["CENA_WIN_TKPY"], os.path.join(HERE, "ecotray_sim.py"), app, plano, saida], env=env, timeout=600).returncode
    finally:
        xv.terminate()
        try:
            xv.wait(5)
        except subprocess.TimeoutExpired:
            xv.kill()
    sys.exit(rc)


def hash_app(app):
    h = hashlib.sha256()
    for rel in ("dashboard.py", "installer_win/installer_gui.py", "version.py", "assets/icon.png", "assets/ecotray-logo-light.png"):
        p = os.path.join(app, rel)
        if os.path.exists(p):
            h.update(rel.encode()); h.update(open(p, "rb").read())
    for rel in ("ecotray_sim.py",):
        h.update(open(os.path.join(HERE, rel), "rb").read())
    return h.hexdigest()[:16]


def main():
    argv = sys.argv[1:]
    if "--dentro" in argv:
        i = argv.index("--dentro"); plano, saida, app, sessao, tw, th = argv[i + 1:i + 7]
        return dentro(plano, saida, app, sessao, (int(tw), int(th)))
    if len(argv) < 2 or argv[0].startswith("-"):
        sys.exit(__doc__)
    plano, saida = os.path.abspath(argv[0]), os.path.abspath(argv[1])
    app = opt(argv, "--app") or os.environ.get("ECOTRAY_SRC") or (os.path.join(os.environ["APP_SRC"], "ecotray") if os.environ.get("APP_SRC") else None)
    if not app or not os.path.exists(os.path.join(app, "dashboard.py")):
        sys.exit("pasta do EcoTray do app não achada (--app, ECOTRAY_SRC ou APP_SRC)")
    app = os.path.abspath(app)
    PL = json.load(open(plano, encoding="utf8")); tela = PL.get("tela", [1920, 1200])
    os.makedirs(saida, exist_ok=True)
    qj = os.path.join(saida, "quadros.json")
    antigo = json.load(open(qj, encoding="utf8")) if os.path.exists(qj) else {}
    ha = hash_app(app); feitos = dict(antigo.get("sessoes", {})); quadros = dict(antigo.get("quadros", {})); erros = []
    env_tk()  # prepara o Python com Tk antes (fora da rede própria, que não tem internet)
    usa_unshare = os.geteuid() == 0 and subprocess.run(["unshare", "-n", "true"], capture_output=True).returncode == 0
    for s in PL["sessoes"]:
        hs = hashlib.sha256((ha + json.dumps(s, sort_keys=True, ensure_ascii=False) + json.dumps(tela) +
                             PL.get("usuario_windows", "")).encode()).hexdigest()[:16]
        nomes = [p["capturar"] for p in s.get("passos", []) if "capturar" in p]
        if "--refazer" not in argv and feitos.get(s["nome"]) == hs and all(os.path.exists(os.path.join(saida, f"{n}.png")) for n in nomes):
            print(f"sessão {s['nome']}: sem mudança ({len(nomes)} capturas)"); continue
        cmd = [sys.executable, os.path.abspath(__file__), "--dentro", plano, saida, app, s["nome"], str(tela[0]), str(tela[1])]
        if usa_unshare:
            cmd = ["unshare", "-n"] + cmd
        else:
            print("aviso: sem unshare -n (precisa de root); a porta 8054 tem de estar livre", flush=True)
        t0 = time.time(); rc = subprocess.run(cmd).returncode
        parcial = os.path.join(saida, f".quadros.{s['nome']}.json")
        if os.path.exists(parcial):
            d = json.load(open(parcial, encoding="utf8")); os.remove(parcial)
            quadros.update(d["quadros"]); erros += d["erros"]
        if rc == 0:
            feitos[s["nome"]] = hs
        else:
            erros.append(f"sessão {s['nome']} terminou com código {rc}")
        print(f"sessão {s['nome']}: {len(nomes)} capturas em {time.time() - t0:.1f} s", flush=True)
    json.dump({"tela": tela, "app": ha, "sessoes": feitos, "quadros": quadros}, open(qj, "w", encoding="utf8"), ensure_ascii=False, indent=1)
    if erros:
        sys.exit("ERROS:\n  " + "\n  ".join(erros))
    print(f"ok: {len(quadros)} quadros em {saida}")


if __name__ == "__main__":
    main()
