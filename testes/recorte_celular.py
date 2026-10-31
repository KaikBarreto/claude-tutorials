"""Teste do recorte da tela no palco (Stage._render), sem gravação nenhuma (use o recorte_celular.sh, que monta a pasta certa).
Kaik (31/10, T7): "nos zooms a imagem do celular cruza o celular e fica com as bordas retas aparecendo". Três conferências:
  1. CELULAR, código novo: em janelas em que o canto arredondado invade o quadro com a BORDA da tela já fora dele (entrada e saída do
     zoom, deslizes, desfoque de movimento), a cobertura da tela é o retângulo arredondado (erro < 0,5 em todos os pixels);
  2. CELULAR, código ANTIGO (a linha `pad = ...` trocada por `pad = 0`): o teste TEM de acusar canto reto nele. Um teste que não
     pode falhar não prova nada;
  3. COMPUTADOR 16:9, código novo x antigo: quadros do palco IDÊNTICOS bit a bit (o conserto vale só para o celular).
uso: python3 -I recorte_celular.py <pasta edit>        (o .sh cria a pasta com o kit ao lado, como em testes/identidade_domiflix.sh)"""
import os, sys, types
sys.dont_write_bytecode = True
EDIT = os.path.abspath(sys.argv[1]); sys.path.insert(0, EDIT)
import numpy as np
from camera import Geom, W, H
from auditar_recorte import erro_cobertura, em_risco, LIMITE


def carrega(nome, troca=None):
    """classe Stage do stage.py desta pasta; `troca` = (trecho, novo) devolve a versão antiga, sem o conserto"""
    f = os.path.join(EDIT, "stage.py"); src = open(f).read()
    if troca:
        assert troca[0] in src, f"trecho do recorte não encontrado em stage.py ({troca[0]!r}): atualize este teste"
        src = src.replace(*troca)
    mod = types.ModuleType(nome); mod.__file__ = f; exec(compile(src, f, "exec"), mod.__dict__)
    return mod.Stage


Novo = carrega("stage_novo"); Antigo = carrega("stage_antigo", ("pad = c if self.phone else 0", "pad = 0"))
ruim = 0

# ---------------------------------------------------------------- 1 e 2: celular (390x844 a 2x -> 780x1688)
SW, SH = 780, 1688
g = Geom(SW, SH, 56, 46)
fase = {"bezel": 14}
novo, antigo = Novo(g, 0.45, None, fase), Antigo(g, 0.45, None, fase)
casos = []   # (descrição, janelas): cada caso é UM quadro final (várias janelas = desfoque de movimento)
for z in (1.6, 2.16, 3.2):
    k = z * g.k0; vw = W / k; r = g.radius * k / g.k0
    for f in (0.15, 0.5, 0.85):   # borda de cima/baixo a f do raio FORA do quadro: o canto arredondado ainda invade
        for lado in ("cima", "baixo"):
            cy = (H / 2 + f * r) / k if lado == "cima" else SH - (H / 2 + f * r) / k   # centro da câmera (px do vídeo)
            casos.append((f"zoom {z} borda de {lado} {f:.2f} r fora", [(SW / 2, cy, vw)]))
            if f == 0.5: casos.append((f"zoom {z} borda de {lado} {f:.2f} r fora, câmera 40 px à esquerda", [(SW / 2 - 40, cy, vw)]))
    for dy0 in (0.0, 0.4 * r / k):   # desfoque de movimento: 5 sub-janelas deslizando 60 px de vídeo pela borda
        casos.append((f"zoom {z} deslize com desfoque (+{dy0:.0f} px)", [(SW / 2, (H / 2 + 0.6 * r) / k + dy0 + j * 15, vw) for j in range(5)]))
casos = [(d, v) for d, v in casos if any(em_risco(g, SW, SH, vv) for vv in v)]   # só o risco que o teste existe para pegar
assert len(casos) >= 20, f"poucos casos de risco ({len(casos)}): a geometria do teste mudou?"
pn, pa, falhas_ant = 0.0, 0.0, 0
for d, v in casos:
    en, _ = erro_cobertura(novo, g, SW, SH, v); ea, npx = erro_cobertura(antigo, g, SW, SH, v)
    pn, pa = max(pn, en), max(pa, ea); falhas_ant += ea > LIMITE
    if en > LIMITE: print(f"   FALHOU (novo): {d}: erro {en:.2f}"); ruim += 1
print(f"1. celular, código novo: {len(casos)} quadros de risco, pior erro de cobertura {pn:.3f} (limite {LIMITE})  {'ok' if pn <= LIMITE else 'FALHOU'}")
if falhas_ant == 0:
    print("2. celular, código antigo: o teste NÃO acusou canto reto nele: não serve para nada. FALHOU"); ruim += 1
else:
    print(f"2. celular, código antigo (pad = 0): {falhas_ant} de {len(casos)} quadros com canto reto, pior erro {pa:.2f}  ok (o teste acusa o erro)")

# ---------------------------------------------------------------- 3: computador 16:9, novo x antigo bit a bit
SWd, SHd = 2560, 1600
gd = Geom(SWd, SHd, 44, 16)
rng = np.random.default_rng(7)
quadro = rng.integers(0, 256, (SHd, SWd, 3), dtype=np.uint8)
quadro[::40] = 255; quadro[:, ::40] = 0   # linhas finas: qualquer deslocamento de 1 px aparece
nd, ad = Novo(gd, 0.20, None, None), Antigo(gd, 0.20, None, None)
iguais = total = 0
for z in (1.0, 1.3, 1.8, 2.4, 3.0):
    k = z * gd.k0; vw = W / k
    for cx, cy in ((SWd / 2, SHd / 2), (vw / 2, vw * H / W / 2), (SWd - vw / 2, SHd - vw * H / W / 2), (SWd / 2, vw * H / W / 2 - 25), (vw / 2 - 25, SHd / 2)):
        for views in ([(cx, cy, vw)], [(cx, cy + j * 12, vw * (1 + 0.01 * j)) for j in range(4)]):
            a, ra = nd.render(quadro, views); b, rb = ad.render(quadro, views)
            total += 1; iguais += bool(np.array_equal(a, b)) and tuple(ra) == tuple(rb)
print(f"3. computador 16:9: {iguais} de {total} quadros idênticos bit a bit ao código antigo  {'ok' if iguais == total else 'FALHOU'}")
ruim += iguais != total
print("RECORTE DO CELULAR OK" if not ruim else f"RECORTE DO CELULAR COM PROBLEMA ({ruim})")
sys.exit(1 if ruim else 0)
