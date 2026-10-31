"""Auditoria do recorte da tela do celular (Kaik 31/10: "a imagem do celular cruza o celular e fica com as bordas retas aparecendo").
A tela gravada tem de ficar presa ao retângulo ARREDONDADO do aparelho em TODO quadro: entrada e saída do zoom, deslizes, desfoque de
movimento. O erro que esta auditoria pega: o canto arredondado ainda invade o quadro quando a BORDA da tela já saiu dele (o palco só
recortava o canto com a borda dentro do quadro) e a tela aparecia com canto reto por cima da moldura.
Como funciona (sem decodificar o vídeo): compõe o palco duas vezes com a tela toda MAGENTA e toda PRETA; a diferença entre as duas é
exatamente a cobertura da tela no quadro final (inclusive a média dos sub-quadros do desfoque) e é comparada com a máscara analítica
(retângulo arredondado de cada sub-janela). Confere os quadros de risco (canto invadindo) e alguns espalhados pelo capítulo.
uso: python3 -I auditar_recorte.py caps/cap01.chapter.json [...] [--n 40]     (sob a trava: reexecuta sozinho)
saída: por capítulo, quadros de risco, quadros conferidos e o pior erro de cobertura (0 a 1); código 1 se algum passar de 0,5.
Também é módulo: `erro_cobertura(stage, g, SW, SH, views)` serve ao testes/recorte_celular.sh (sem gravação nenhuma)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.dont_write_bytecode = True
import numpy as np
from camera import W, H, FPS

YY, XX = np.mgrid[0:H, 0:W].astype(np.float32); XX += 0.5; YY += 0.5
LIMITE = 0.5   # erro de cobertura (0 a 1) acima do qual o quadro conta como problema


def janela(g, SW, SH, view):
    """retângulo da tela no quadro final (X0, Y0, X1, Y1) e o raio do canto, para uma janela (cx, cy, vw) da câmera"""
    cx, cy, vw = view; k = W / vw; vx, vy = cx - vw / 2, cy - vw * H / W / 2
    return -vx * k, -vy * k, (SW - vx) * k, (SH - vy) * k, g.radius * k / g.k0


def mascara(g, SW, SH, view):
    """cobertura analítica (0 a 1) do retângulo arredondado da tela nesta janela (distância com sinal, borda suavizada em 1 px)"""
    X0, Y0, X1, Y1, r = janela(g, SW, SH, view)
    hx, hy = (X1 - X0) / 2, (Y1 - Y0) / 2
    qx, qy = np.abs(XX - (X0 + X1) / 2) - (hx - r), np.abs(YY - (Y0 + Y1) / 2) - (hy - r)
    d = np.sqrt(np.maximum(qx, 0) ** 2 + np.maximum(qy, 0) ** 2) + np.minimum(np.maximum(qx, qy), 0) - r
    return np.clip(0.5 - d, 0, 1)


def erro_cobertura(stage, g, SW, SH, views):
    """compõe o palco com a tela magenta e com a tela preta e devolve (pior erro de cobertura, nº de pixels com erro > LIMITE).
    As 2 linhas de cima e de baixo do quadro ficam de fora (a borda do próprio quadro)."""
    mag = np.zeros((SH, SW, 3), np.uint8); mag[..., 0] = 255; mag[..., 2] = 255; preto = np.zeros((SH, SW, 3), np.uint8)
    a, _ = stage.render(mag, views); b, _ = stage.render(preto, views)
    cob = (a[..., 0].astype(np.float32) - b[..., 0].astype(np.float32)) / 255.0
    err = np.abs(cob - np.mean([mascara(g, SW, SH, v) for v in views], 0)); err[:2, :] = 0; err[-2:, :] = 0
    return float(err.max()), int((err > LIMITE).sum())


def em_risco(g, SW, SH, view):
    """True se o canto arredondado invade o quadro enquanto a BORDA da tela (cima ou baixo) já saiu dele: o caso que vazava"""
    X0, Y0, X1, Y1, r = janela(g, SW, SH, view)
    return (-r - 2 < Y0 <= 0 or H <= Y1 < H + r + 2) and X0 > 0 and X1 < W


def main(args):
    from common import ensure_heavy
    ensure_heavy()
    from chapter import Chapter
    N = int(args[args.index("--n") + 1]) if "--n" in args else 40
    caps = [a for i, a in enumerate(args) if a.endswith(".json") and (i == 0 or args[i - 1] != "--n")]
    ruim = 0
    for cj in caps:
        C = Chapter(cj); g, cam, stage, SW, SH = C.geom, C.cam, C.stage, C.SW, C.SH
        if not (C.ch.get("stage") or {}).get("phone"):
            print(f"{C.name}: não é capítulo de celular, nada a conferir"); continue
        risco = [q for q in range(int(C.dur * FPS)) if em_risco(g, SW, SH, cam.view(q / FPS))]
        esc = lambda lst, n: [lst[int(i * (len(lst) - 1) / max(1, n - 1))] for i in range(min(n, len(lst)))] if lst else []
        todos = esc(list(range(int(C.dur * FPS))), max(6, N // 4))
        quadros = sorted(set(esc(risco, N - len(todos)) + todos))
        pior = []
        for q in quadros:
            t = q / FPS; n = cam.n_samples(t, C.shut); ts = [t] if n == 1 else [t + (j / (n - 1) - 0.5) * C.shut for j in range(n)]
            e, npx = erro_cobertura(stage, g, SW, SH, [cam.view(tt) for tt in ts])
            pior.append((e, t, npx))
        pior.sort(reverse=True); nruim = sum(1 for p in pior if p[0] > LIMITE); ruim += nruim
        print(f"{C.name}: {len(risco)} quadros de risco (canto invadindo com a borda fora), {len(quadros)} conferidos, "
              f"pior erro de cobertura {pior[0][0]:.2f} (t={pior[0][1]:.2f} s), {nruim} acima de {LIMITE}")
        for p in pior[:3] if nruim else []:
            print(f"   t={p[1]:.2f} s: erro {p[0]:.2f}, {p[2]} px de tela fora do retângulo arredondado")
    print("RECORTE OK" if not ruim else f"RECORTE COM PROBLEMA em {ruim} quadro(s)")
    return 1 if ruim else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
