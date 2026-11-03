"""Formato vertical 9:16 (1080x1920): a geometria única (formato_9x16.json) e as checagens de área segura.

Pedido do Kaik (T0 v2, 31/10): versão nativa para celular, recomposta cena a cena (não é recorte do 16:9).
  - painel claro de 1008x1700 em (36, 110) sobre o palco escuro (no 16:9: janela de 1587x992 em (166, 44));
  - margem lateral mínima de 72 px; nada importante nos 180 px de cima e de baixo; texto de 44 px ou mais;
  - no máximo 2 linhas por bloco; legendas (.srt/.vtt) com linhas de ~32 caracteres.

Uso como módulo: `import vertical as V` -> V.W, V.H, V.PAINEL, V.SEGURA, V.LEGENDA_FAIXA, V.TEXTO_MIN, V.LEGENDA_COL,
V.fora_da_area_segura(img), V.caixa_fora_da_segura(caixa).
Linha de comando: python3 vertical.py <quadro.png> [...]   (confere se há conteúdo fora da área segura em cada imagem)"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
GEO = json.load(open(os.path.join(HERE, "formato_9x16.json"), encoding="utf-8"))
W, H, FPS = GEO["quadro"]["largura"], GEO["quadro"]["altura"], GEO["quadro"]["fps"]
_p = GEO["painel"]
PX, PY, PW, PH, PR, PSOMBRA = _p["x"], _p["y"], _p["largura"], _p["altura"], _p["raio"], _p["sombra"]
PAINEL = (PX, PY, PW, PH)
SEGURA = (GEO["segura"]["x0"], GEO["segura"]["y0"], GEO["segura"]["x1"], GEO["segura"]["y1"])
LEGENDA_FAIXA = (GEO["legenda_faixa"]["y0"], GEO["legenda_faixa"]["y1"])  # onde o player do celular desenha a legenda
TELA_X, TELA_Y, TELA_W, TELA_H, TELA_R = (GEO["tela_real"][k] for k in ("x", "y", "largura", "altura", "raio"))  # janela da tela real (celular)
TEXTO_MIN, LINHAS_MAX, LEGENDA_COL = GEO["texto_min"], GEO["linhas_max"], GEO["legenda_coluna"]


def fora_da_area_segura(img, limiar=150, minimo=60):
    """Conta pixels de CONTEÚDO (claros e vivos sobre o escuro da vinheta/palco) fora da área segura de um quadro
    1080x1920 RGB (uint8). Serve para vinhetas, cartela e palco escuro: o fundo vai até ~60 de luminância e o texto, o
    capacete e o logo passam de 150. Devolve {faixa: pixels} só com as faixas que passaram de `minimo` pixels."""
    assert img.shape[:2] == (H, W), f"quadro {img.shape[1]}x{img.shape[0]}: esperado {W}x{H}"
    x0, y0, x1, y1 = SEGURA
    lum = img[..., :3].max(axis=2)
    vivo = lum >= limiar
    faixas = {"alto (y < %d)" % y0: vivo[:y0].sum(), "baixo (y >= %d)" % y1: vivo[y1:].sum(),
              "esquerda (x < %d)" % x0: vivo[y0:y1, :x0].sum(), "direita (x >= %d)" % x1: vivo[y0:y1, x1:].sum()}
    return {k: int(v) for k, v in faixas.items() if v > minimo}


def caixa_fora_da_segura(caixa, folga=0):
    """caixa = (x0, y0, x1, y1) em px do quadro 1080x1920 (um texto, um logo, um bloco). Devolve a lista dos lados que
    passam da área segura (vazia = dentro). `folga` tolera alguns px (animações em curso)."""
    x0, y0, x1, y1 = SEGURA
    lados = []
    if caixa[0] < x0 - folga: lados.append(f"esquerda ({caixa[0]:.0f} < {x0})")
    if caixa[1] < y0 - folga: lados.append(f"alto ({caixa[1]:.0f} < {y0})")
    if caixa[2] > x1 + folga: lados.append(f"direita ({caixa[2]:.0f} > {x1})")
    if caixa[3] > y1 + folga: lados.append(f"baixo ({caixa[3]:.0f} > {y1})")
    return lados


if __name__ == "__main__":
    import cv2
    ruim = 0
    for p in sys.argv[1:]:
        im = cv2.imread(p)
        if im is None:
            print(f"{p}: não abriu")
            ruim += 1
            continue
        r = fora_da_area_segura(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
        print(f"{os.path.basename(p)}: {'ok' if not r else 'CONTEÚDO FORA DA ÁREA SEGURA ' + str(r)}")
        ruim += bool(r)
    sys.exit(1 if ruim else 0)
