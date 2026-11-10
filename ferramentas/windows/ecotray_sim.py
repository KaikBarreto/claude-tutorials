"""Roda as janelas de verdade do EcoTray (o código do app, só leitura) num display virtual e captura cada estado pedido.

- Painel: `dashboard.py` (show_dashboard), com um EcoTray falso no WebSocket de comandos (127.0.0.1:8054) que responde
  get_status, list_printers, set_default_printer, check_update e get_activity no formato do ecotray.py, e manda pela
  conexão ao vivo do painel os eventos que o plano pede (peso, atividade, impressão, trava da balança).
- Instalador: `installer_win/installer_gui.py` (InstallerWindow), sem baixar nada: os textos e as porcentagens de cada
  etapa são os do próprio `_run_install` (STEPS e detalhes), aplicados pelo `_set_status` dele; o fim é o `_finish` dele.
Saída: um PNG por captura (só a janela, no tamanho real) e `quadros.json` com a posição da janela na tela e os alvos
(texto, retângulo relativo à janela e tipo de cursor do widget) para a cena mirar o cursor.

Roda no Python com Tk preparado por `preparar.sh`, dentro do `capturar_ecotray.py` (rede própria + Xvfb).
uso: python ecotray_sim.py <pasta ecotray do app> <plano.json> <saida/>
Plano: {"tela": [1920, 1200], "usuario_windows": "Rafael", "sessoes": [ {"programa": "painel"|"instalador", ...} ]}
(formato completo em docs/10-cena-windows.md)."""
import asyncio
import json
import os
import sys
import threading
import time
import types
from pathlib import Path, PosixPath

APP, PLANO, SAIDA = (Path(a) for a in sys.argv[1:4])
PL = json.load(open(PLANO, encoding="utf8"))
SAIDA.mkdir(parents=True, exist_ok=True)
DISPLAY = os.environ.get("DISPLAY", ":0")
USUARIO = PL.get("usuario_windows", "Rafael")
QUADROS = {}  # nome -> {arquivo, janela: [x, y, w, h], alvos: {nome: {r: [x, y, w, h], cursor}}}
ERROS = []

# ───────────────────────────── EcoTray falso (porta de comandos) ─────────────────────────────


class EcoTrayFalso:
    """Responde como o ecotray.py (_handle_printer_command) às ações que o painel usa; o estado vem do plano."""

    def __init__(self, estado):
        self.e = {"versao": "", "trava": "unlocked", "balancas": [], "balanca_padrao": None, "pesos": {},
                  "impressoras": [], "impressora_padrao": None, "navegadores": 0, "atividade": []}
        self.e.update(estado or {})
        self.conexoes, self.ouvintes = set(), set()  # ouvinte = conexão que nunca mandou comando (a "ao vivo" do painel)
        self.loop = asyncio.new_event_loop()
        self.pronto = threading.Event()

    def status(self):
        e = self.e; trava = e["trava"]; livre = trava == "unlocked"
        nomes = list(e["impressoras"])
        p = {"type": "status", "version": e["versao"], "capabilities": ["print", "print_raw", "print_image"],
             "scales_unlocked": livre, "scales_lock_state": trava, "printers": nomes,
             "printers_meta": [{"name": n, "driver": None, "is_compatible": True} for n in nomes], "printers_stale": False,
             "default_printer": e["impressora_padrao"],
             # como o ws_server.py: conta TODAS as conexões abertas na 8054 (inclusive a que está pedindo o status)
             "client_count": len(self.conexoes) + int(e["navegadores"]),
             "activity_log": list(e["atividade"])}
        if livre:
            b = e["balancas"]
            p.update({"scales": [{"id": s["id"], "name": s.get("nome") or s["id"], "connected": bool(s.get("conectada"))} for s in b],
                      "scales_full": [{"id": s["id"], "name": s.get("nome") or s["id"], "port": s.get("porta", "COM3"),
                                       "baudrate": s.get("baud", 9600), "protocol": s.get("protocolo", "auto")} for s in b],
                      "default_scale_id": e["balanca_padrao"] or (b[0]["id"] if b else None),
                      "last_weight_by_scale": {k: v for k, v in e["pesos"].items() if v not in (None, "")},
                      "last_weight": e["pesos"].get(e["balanca_padrao"] or (b[0]["id"] if b else ""), "")})
        else:
            p.update({"scales": [], "scales_full": [], "default_scale_id": None, "last_weight_by_scale": {}, "last_weight": ""})
        return p

    async def _handler(self, ws):
        self.conexoes.add(ws); self.ouvintes.add(ws)
        try:
            async for raw in ws:
                self.ouvintes.discard(ws)
                try:
                    d = json.loads(raw)
                except ValueError:
                    await ws.send(json.dumps({"type": "error", "message": "JSON inválido"})); continue
                a = d.get("action")
                if a == "get_status":
                    await ws.send(json.dumps(self.status(), ensure_ascii=False))
                elif a == "list_printers":
                    n = list(self.e["impressoras"])
                    await ws.send(json.dumps({"type": "printers", "data": n, "printers_stale": False,
                                              "data_meta": [{"name": x, "driver": None, "is_compatible": True} for x in n]}))
                elif a == "set_default_printer":  # como o ecotray.py: grava, responde e anota "Impressora padrão: X"
                    p = d.get("printer") or self.e["impressora_padrao"]
                    self.e["impressora_padrao"] = p
                    await ws.send(json.dumps({"type": "printer_config", "success": True}))
                    curto = p.split("\\")[-1] if p and "\\" in p else (p or "")
                    a_ = {"ts": self.e.get("hora", "08:30:00"), "msg": f"Impressora padrão: {curto}", "kind": "info"}
                    self.e["atividade"].insert(0, a_); del self.e["atividade"][20:]
                    await self._enviar(json.dumps({"type": "activity", **a_}, ensure_ascii=False))
                elif a == "check_update":
                    await ws.send(json.dumps({"type": "update_check", "status": "checking"}))
                elif a == "get_activity":
                    await ws.send(json.dumps({"type": "activity_log", "data": list(self.e["atividade"])}, ensure_ascii=False))
                elif a == "restore_dashboard":
                    await self._enviar(json.dumps({"type": "restore_window"}))
                else:
                    await ws.send(json.dumps({"type": "error", "message": f"Ação desconhecida: {a}"}, ensure_ascii=False))
        except Exception:
            pass
        finally:
            self.conexoes.discard(ws); self.ouvintes.discard(ws)

    async def _enviar(self, msg):
        for ws in list(self.ouvintes):
            try:
                await ws.send(msg)
            except Exception:
                self.ouvintes.discard(ws)

    def enviar(self, payload):
        """broadcast para a conexão ao vivo do painel (como o broadcast_json do ws_server.py)"""
        asyncio.run_coroutine_threadsafe(self._enviar(json.dumps(payload, ensure_ascii=False)), self.loop).result(3)

    def iniciar(self, porta=8054):
        from websockets.asyncio.server import serve

        async def main():
            async with serve(self._handler, "127.0.0.1", porta, ping_interval=20, ping_timeout=10, max_size=8 * 1024 * 1024):
                self.pronto.set()
                await asyncio.Future()

        threading.Thread(target=lambda: self.loop.run_until_complete(main()), daemon=True).start()
        if not self.pronto.wait(10):
            raise RuntimeError("EcoTray falso não subiu na 8054")


# ───────────────────────────── utilidades Tk ─────────────────────────────

RAIZES = []
_tk_init = None


def preparar_tk():
    """guarda a janela raiz que o código do app cria e aplica as cores padrão do Tk no Windows (o que o app não define)"""
    global _tk_init
    import tkinter as tk
    _tk_init = tk.Tk.__init__

    def init(self, *a, **k):
        _tk_init(self, *a, **k)
        # padrões do Tk no Windows (tkWinDefault.h): moldura de foco do botão na cor SystemButtonFace, texto desabilitado
        # em SystemGrayText. No X11 seriam #d9d9d9 e #a3a3a3.
        self.option_add("*Button.highlightBackground", "#f0f0f0", "widgetDefault")
        self.option_add("*Button.disabledForeground", "#6d6d6d", "widgetDefault")
        self.option_add("*Label.disabledForeground", "#6d6d6d", "widgetDefault")
        RAIZES.append(self)
        self.after(700, iniciar_roteiro)

    tk.Tk.__init__ = init


def janela_rect(root):
    root.update_idletasks()
    return [root.winfo_rootx(), root.winfo_rooty(), root.winfo_width(), root.winfo_height()]


def alvos(root):
    """todo widget visível com texto (botões são Labels no painel) + abas dos Notebooks, relativos à janela"""
    import tkinter.ttk as ttk
    rx, ry = root.winfo_rootx(), root.winfo_rooty()
    out, vistos = {}, {}

    def cur(w):
        try:
            c = str(w.cget("cursor"))
        except Exception:
            c = ""
        return "pointer" if c in ("hand2", "hand1") else ("text" if c == "xterm" else "arrow")

    def add(nome, r, c):
        nome = " ".join(nome.split())
        if not nome:
            return
        k = vistos.get(nome, 0) + 1; vistos[nome] = k
        out[nome if k == 1 else f"{nome}#{k}"] = {"r": [int(v) for v in r], "cursor": c}

    def anda(w):
        for c in w.winfo_children():
            try:
                if not c.winfo_ismapped():
                    continue
            except Exception:
                continue
            r = [c.winfo_rootx() - rx, c.winfo_rooty() - ry, c.winfo_width(), c.winfo_height()]
            if isinstance(c, ttk.Notebook):
                abas(c, r)
            try:
                t = c.cget("text")
            except Exception:
                t = ""
            if isinstance(t, str) and t.strip():
                add(t, r, cur(c))
            anda(c)

    def abas(nb, r):
        n = nb.index("end"); xs = {}
        for yy in range(2, 40, 3):
            for x in range(0, r[2], 2):
                try:
                    i = nb.index(f"@{x},{yy}")
                except Exception:
                    continue
                if isinstance(i, int) and 0 <= i < n:
                    a = xs.setdefault(i, [x, yy, x, yy])
                    a[0], a[1], a[2], a[3] = min(a[0], x), min(a[1], yy), max(a[2], x), max(a[3], yy)
        for i, (x0, y0, x1, y1) in xs.items():
            add("aba:" + str(nb.tab(i, "text")).strip(), [r[0] + x0, r[1] + y0, x1 - x0 + 2, y1 - y0 + 3], "arrow")

    anda(root)
    return out


def capturar(root, nome):
    from PIL import ImageGrab
    root.update(); time.sleep(0.05); root.update()
    x, y, w, h = janela_rect(root)
    img = ImageGrab.grab(bbox=(x, y, x + w, y + h), xdisplay=DISPLAY)
    arq = f"{nome}.png"; img.save(SAIDA / arq, optimize=True)
    QUADROS[nome] = {"arquivo": arq, "janela": [x, y, w, h], "alvos": alvos(root)}
    print(f"  {nome}: janela {w}x{h} em ({x}, {y})", flush=True)


def ponteiro(root, alvo):
    """leva o ponteiro do X até o centro do alvo (dispara Enter/Leave de verdade) ou para fora da janela"""
    if alvo is None:
        root.event_generate("<Motion>", warp=True, x=-400, y=-400); return
    a = alvos(root).get(alvo)
    if not a:
        ERROS.append(f"alvo {alvo!r} não achado na janela"); return
    x, y, w, h = a["r"]
    root.event_generate("<Motion>", warp=True, x=x + w // 2, y=y + h // 2)


# ───────────────────────────── roteiro das sessões ─────────────────────────────

SESSAO = {}
_roteiro = None


def iniciar_roteiro():
    global _roteiro
    if _roteiro is None:
        _roteiro = SESSAO["gerador"](RAIZES[-1])
        passo()


def passo():
    root = RAIZES[-1]
    try:
        espera = next(_roteiro)
    except StopIteration:
        root.after(50, root.destroy); return
    except Exception as ex:  # noqa: BLE001
        ERROS.append(f"{SESSAO.get('nome')}: {type(ex).__name__}: {ex}")
        import traceback; traceback.print_exc()
        root.after(50, root.destroy); return
    root.after(int(max(0.0, espera) * 1000), passo)


def peso_bruto(v):
    return None if v is None else str(v)


def roteiro_painel(srv, s):
    nome_s = s["nome"]

    def gerador(root):
        yield 1.2  # o painel pede get_status 0,3 s depois de abrir; espera a primeira carga
        for p in s.get("passos", []):
            if "estado" in p:
                srv.e.update(p["estado"])
            if "pesos" in p:
                srv.e["pesos"].update({k: peso_bruto(v) for k, v in p["pesos"].items()})
            if "atividade" in p:  # nova linha no topo, como o _log_activity do ecotray.py
                a = dict(p["atividade"]); a.setdefault("kind", "info")
                srv.e["atividade"].insert(0, a); srv.e["atividade"][:] = srv.e["atividade"][:20]
                srv.enviar({"type": "activity", **a})
            if "peso" in p:  # {"balanca": id, "valor": "1250.5"}: porta 8054, como o _on_weight
                sid = p["peso"].get("balanca") or srv.e["balanca_padrao"] or srv.e["balancas"][0]["id"]
                v = peso_bruto(p["peso"]["valor"]); srv.e["pesos"][sid] = v
                srv.enviar({"type": "weight", "scale_id": sid, "data": v})
            if "trava" in p:  # scale_lock_status (o navegador destravou ou não)
                srv.e["trava"] = p["trava"]
                srv.enviar({"type": "scale_lock_status", "unlocked": p["trava"] == "unlocked", "state": p["trava"]})
            if "impresso" in p:  # print_notification -> toast "✓  Impresso em <impressora>"
                srv.enviar({"type": "print_notification", "success": True, "printer": p["impresso"]})
            if "enviar" in p:
                srv.enviar(p["enviar"])
            if p.get("atualizar"):  # clique no ↻ da seção Balanças (get_status de novo)
                ponteiro(root, None)
                yield 0.05
            if "aba" in p:
                import tkinter.ttk as ttk
                for w in _todos(root):
                    if isinstance(w, ttk.Notebook) and w.winfo_ismapped():
                        for i in range(w.index("end")):
                            if w.tab(i, "text").strip() == p["aba"]:
                                w.select(i)
                        break
            if "clique" in p:  # clique de verdade num alvo (ex.: ↻, uma impressora): ButtonPress/Release no widget
                _clicar(root, p["clique"])
            yield float(p.get("espera", 0.45))
            if "ponteiro" in p:
                ponteiro(root, p["ponteiro"])
                yield 0.25
            if "capturar" in p:
                capturar(root, p["capturar"])
            if p.get("soltar_ponteiro", "ponteiro" in p):
                ponteiro(root, None)
                yield 0.15
        yield 0.1
    SESSAO.update(gerador=gerador, nome=nome_s)


def _todos(w):
    yield w
    for c in w.winfo_children():
        yield from _todos(c)


def _clicar(root, alvo):
    a = alvos(root).get(alvo)
    if not a:
        ERROS.append(f"clique: alvo {alvo!r} não achado"); return
    x, y, w, h = a["r"]; cx, cy = x + w // 2, y + h // 2
    root.event_generate("<Motion>", warp=True, x=cx, y=cy); root.update()
    alvo_w = root.winfo_containing(root.winfo_rootx() + cx, root.winfo_rooty() + cy)
    if alvo_w is not None:
        alvo_w.event_generate("<ButtonPress-1>", x=1, y=1); alvo_w.event_generate("<ButtonRelease-1>", x=1, y=1)


class CaminhoWindows(PosixPath):
    """caminho do log: mostra o do Windows (%APPDATA%\\EcoTray\\ecotray.log) e lê o arquivo de exemplo daqui"""
    real = None
    mostrado = ""

    def __str__(self):
        return CaminhoWindows.mostrado

    def __fspath__(self):
        return str(CaminhoWindows.real)


def sessao_painel(s):
    sys.path.insert(0, str(APP))
    import dashboard  # o código do app, sem alteração
    srv = EcoTrayFalso(s.get("servidor"))
    srv.e.setdefault("versao", ""); srv.e["versao"] = srv.e["versao"] or s.get("abrir", {}).get("version", "")
    srv.iniciar(int(s.get("abrir", {}).get("ws_port", 8054)))
    log = SAIDA / f".{s['nome']}.ecotray.log"
    log.write_text("".join(l + "\n" for l in s.get("log", [])), encoding="utf8")
    CaminhoWindows.real = log
    CaminhoWindows.mostrado = f"C:\\Users\\{USUARIO}\\AppData\\Roaming\\EcoTray\\ecotray.log"
    dashboard._log_file_path = lambda: CaminhoWindows(str(log))
    roteiro_painel(srv, s)
    dados = {"status": "warn", "scale_info": "", "printer_info": "", "printers_list": [], "ws_port": 8054,
             "ws_scale_port": 8053, "version": ""}
    dados.update(s.get("abrir", {}))
    dashboard.show_dashboard(dados)


# ───────────────────────────── instalador ─────────────────────────────

def sessao_instalador(s):
    sys.modules.setdefault("winreg", types.ModuleType("winreg"))  # só existe no Windows; o roteiro não chega a usar
    fake = SAIDA / ".instalador"; (fake / "Local").mkdir(parents=True, exist_ok=True); (fake / "Roaming").mkdir(exist_ok=True)
    os.environ["LOCALAPPDATA"] = str(fake / "Local"); os.environ["APPDATA"] = str(fake / "Roaming")
    sys.path.insert(0, str(APP / "installer_win"))
    import installer_gui as ig  # o código do app, sem alteração
    ig.InstallerWindow._run_install = lambda self: None  # nada de baixar: o roteiro abaixo aplica as mesmas etapas
    total_mb = float(s.get("tamanho_mb", 41.6))

    def gerador(root):
        app = SESSAO["app"]
        yield 0.6
        for p in s.get("passos", []):
            if p.get("instalar"):  # clique em "Instalar": o _start_install de verdade (botão vira "Instalando...")
                app._start_install()
            if "etapa" in p:  # [indice de STEPS, detalhe, pct] como no _run_install
                i, det, pct = p["etapa"]
                app._set_status(ig.STEPS[i], det, pct=pct)
            if "baixando" in p:  # pct do download (20 a 75), detalhe "x.x MB / y.y MB" como no _download_file
                pct = float(p["baixando"]); frac = (pct - 20) / 55.0
                app._set_status(ig.STEPS[1], f"{frac * total_mb:.1f} MB / {total_mb:.1f} MB", pct=pct)
            if p.get("concluir"):  # fim do _run_install: 100% e _finish (o Popen do exe instalado falha aqui e é ignorado)
                app._set_status(ig.STEPS[4], "EcoTray instalado com sucesso!", pct=100)
                app._finish()
            yield float(p.get("espera", 0.35))
            if "ponteiro" in p:
                ponteiro(root, p["ponteiro"]); yield 0.25
            if "capturar" in p:
                capturar(root, p["capturar"])
            if "ponteiro" in p:
                ponteiro(root, None); yield 0.15
        yield 0.1

    SESSAO.update(gerador=gerador, nome=s["nome"])
    app = ig.InstallerWindow()
    SESSAO["app"] = app
    app.run()


# ───────────────────────────── bandeja (ícone e menu do tray_app.py) ─────────────────────────────

def sessao_bandeja(s):
    """O menu da bandeja é nativo do Windows (pystray): não dá para fotografar aqui. Então o tray_app.py de verdade monta
    o menu com um pystray de mentira que só anota os itens (texto, padrão, ativo, separador), e o ícone sai do próprio
    _get_image() (icon.png 64x64 + a bolinha de status do _compose_icon). A cena desenha o menu no estilo do Windows 11
    com esses itens."""
    fake = types.ModuleType("pystray")

    class MenuItem:
        def __init__(self, text, action=None, checked=None, radio=False, default=False, visible=True, enabled=True):
            self.text, self.default, self.visible, self.enabled = text, default, visible, enabled

    class Menu:
        SEPARATOR = MenuItem("-")

        def __init__(self, *items):
            self.items = items

    fake.MenuItem, fake.Menu, fake.Icon = MenuItem, Menu, object
    sys.modules["pystray"] = fake
    sys.path.insert(0, str(APP))
    import tray_app  # o código do app, sem alteração
    t = tray_app.TrayApp(on_reconnect=lambda: None, on_open_settings=lambda: None, on_exit=lambda: None,
                         on_update=lambda: None, icon_path=str(APP / "assets" / "icon.png"))
    for p in s.get("passos", []):
        if "status" in p:  # como o ecotray.py chama: "connected:COM3@9600", "error:no_scale_found", ...
            t.set_scale_status(p["status"])
        if "impressora" in p:
            t.set_printer_info(p["impressora"] or None)
        if "capturar" in p:
            nome = p["capturar"]
            itens = [{"sep": True} if it is Menu.SEPARATOR else {"texto": it.text, "padrao": bool(it.default), "ativo": bool(it.enabled)}
                     for it in t._build_menu().items if getattr(it, "visible", True)]
            t._get_image().save(SAIDA / f"{nome}.png")
            QUADROS[nome] = {"arquivo": f"{nome}.png", "tipo": "bandeja", "status": t._status, "dica": "EcoTray", "menu": itens}
            print(f"  {nome}: ícone {t._status}, menu com {len(itens)} itens", flush=True)


# ───────────────────────────── principal ─────────────────────────────

def main():
    sessoes = PL["sessoes"]
    so = os.environ.get("SIM_SESSAO")  # cada sessão roda num processo próprio (o capturar_ecotray.py chama uma por vez)
    for s in sessoes:
        if so and s["nome"] != so:
            continue
        print(f"sessão {s['nome']} ({s['programa']})", flush=True)
        if s["programa"] in ("painel", "instalador"):
            preparar_tk()
        if s["programa"] == "painel":
            sessao_painel(s)
        elif s["programa"] == "instalador":
            sessao_instalador(s)
        elif s["programa"] == "bandeja":
            sessao_bandeja(s)
        else:
            ERROS.append(f"programa desconhecido: {s['programa']}")
    out = SAIDA / (f".quadros.{so}.json" if so else "quadros.json")
    json.dump({"quadros": QUADROS, "erros": ERROS}, open(out, "w", encoding="utf8"), ensure_ascii=False, indent=1)
    if ERROS:
        print("ERROS:", *ERROS, sep="\n  ", flush=True)
        sys.exit(2)


if __name__ == "__main__":
    main()
