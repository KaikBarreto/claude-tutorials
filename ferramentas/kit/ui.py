"""Identidade visual (marca) + elementos desenhados em Python (PIL/numpy) para a aula: palco, selo de velocidade, título
de tópico, dica, rótulo de destaque.

A marca vem de UM arquivo: $MARCA_JSON (arquivo ou pasta) ou <TUT_HOME>/marca/marca.json, onde TUT_HOME é a pasta que
contém kit/ audio/ web/... (a pasta acima deste arquivo). Sem marca.json vale o padrão neutro (formato em
modelos/MARCA.md). Todo o editor lê daqui: ACCENT (= GREEN, nome antigo), DARK, LIGHT, ACCENT_TEXT (acento legível
sobre o escuro), ON_ACCENT (texto sobre o acento), font(peso, tamanho) e tom(cor) (cor desenhada para o verde de
referência #00C597 -> a mesma cor no acento da marca; com o acento da Dominex devolve a própria cor).
CLI: python3 kit/ui.py                  mostra a marca em uso
     python3 kit/ui.py --web <pasta web>  publica o que a vinheta precisa em <web>/_marca/<hash>/ (kit/brand_clips.sh)"""
import colorsys
import hashlib
import json
import os
import re
import shutil
import sys
import time
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

KIT = os.path.dirname(os.path.abspath(__file__))
TUT_HOME = os.path.dirname(KIT)
FONTS = os.path.join(KIT, "fonts")
REF = (0, 197, 151)  # verde de referência: fundos e luzes derivados foram desenhados para ele
ESTILOS = ("logo", "dominex-capacete", "ecosistema-reciclagem")
NEUTRA = {"serie": "Tutoriais",
          "cores": {"acento": "#3B82F6", "escuro": "#1E1E1E", "claro": "#F3F4F6"},
          "fonte": {"familia": "Montserrat", "arquivos": {}},
          "logo": {"arquivo": "", "simbolo": "", "wordmark": "", "wordmark_altura": 0.5},
          "vinheta": {"estilo": "logo"},
          "cartela": {"frase": "Até a próxima aula!"}}


# ------------------------------------------------------------------ marca
def rgb(c):
    """'#00C597', '#0C9' ou [0, 197, 151] -> (0, 197, 151)"""
    if isinstance(c, (list, tuple)) and len(c) == 3:
        return tuple(int(round(float(v))) for v in c)
    s = str(c).strip().lstrip("#")
    if len(s) == 3:
        s = "".join(ch * 2 for ch in s)
    if not re.fullmatch(r"[0-9a-fA-F]{6}", s):
        raise ValueError(f"marca.json: cor inválida {c!r} (use '#RRGGBB')")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def hexa(c):
    return "#%02X%02X%02X" % tuple(int(round(min(255, max(0, v)))) for v in c)


def caminho_marca():
    """marca.json em uso: $MARCA_JSON (arquivo ou pasta) > <TUT_HOME>/marca/marca.json > None (padrão neutro)"""
    p = os.environ.get("MARCA_JSON", "").strip()
    if p:
        p = os.path.abspath(os.path.expanduser(p))
        p = os.path.join(p, "marca.json") if os.path.isdir(p) else p
        if not os.path.isfile(p):
            raise FileNotFoundError(f"MARCA_JSON aponta para um marca.json que não existe: {p}")
        return p
    p = os.path.join(TUT_HOME, "marca", "marca.json")
    return p if os.path.isfile(p) else None


def carregar_marca(path=None):
    """lê um marca.json (None = padrão neutro), completa com o padrão e resolve os caminhos (relativos ao próprio arquivo)"""
    m = json.loads(json.dumps(NEUTRA))
    base = os.path.dirname(os.path.abspath(path)) if path else TUT_HOME
    if path:
        with open(path, encoding="utf-8") as fh:
            user = json.load(fh)
        atalho = {"logo": "arquivo", "vinheta": "estilo", "cartela": "frase"}  # "logo": "assets/logo.png" etc.
        for k, v in user.items():
            if k.startswith("_") or v is None:
                continue  # "_leia" e afins
            if k in atalho and isinstance(v, str):
                v = {atalho[k]: v}
            if isinstance(v, dict) and isinstance(m.get(k), dict):
                m[k].update(v)
            else:
                m[k] = v
    m["serie"] = str(m.get("serie") or "").strip()
    m["_rgb"] = {k: rgb(m["cores"][k]) for k in ("acento", "escuro", "claro")}
    if m["vinheta"].get("estilo") not in ESTILOS:
        raise ValueError(f"marca.json: vinheta.estilo deve ser um de {ESTILOS}, veio {m['vinheta'].get('estilo')!r}")

    def arq(v, onde):
        if not v:
            return ""
        p = os.path.normpath(os.path.join(base, os.path.expanduser(str(v))))
        if not os.path.isfile(p):
            raise FileNotFoundError(f"marca.json ({onde}): arquivo não encontrado: {p}")
        return p
    for k in ("arquivo", "simbolo", "wordmark"):
        m["logo"][k] = arq(m["logo"].get(k), "logo." + k)
    if m["logo"].get("pecas") or m["vinheta"]["estilo"] == "ecosistema-reciclagem":  # símbolo em peças (kit/brand_extract.py --pecas)
        if not m["logo"].get("pecas"):
            raise ValueError('marca.json: o estilo "ecosistema-reciclagem" precisa de "logo": {"pecas": "assets/pecas.json"} '
                             "(gere com kit/brand_extract.py --pecas)")
        m["logo"]["pecas"] = arq(m["logo"]["pecas"], "logo.pecas")
    if m["vinheta"].get("som"):  # som próprio da vinheta (mídia fora do git: o instalar.sh copia); sem o arquivo, som sintetizado
        p = os.path.normpath(os.path.join(base, os.path.expanduser(str(m["vinheta"]["som"]))))
        m["vinheta"]["som"], m["vinheta"]["som_ausente"] = (p, "") if os.path.isfile(p) else ("", p)
    fa = m["fonte"].get("arquivos") or {}
    fa = {"400": fa} if isinstance(fa, str) else fa  # um arquivo só (ex.: fonte variável)
    m["fonte"]["arquivos"] = {int(w): arq(p, f"fonte.arquivos.{w}") for w, p in fa.items() if p}
    m["cartela"]["frase"] = str(m["cartela"].get("frase") or NEUTRA["cartela"]["frase"]).replace("\n", " ").strip()
    m["_arquivo"], m["_base"] = path, base
    return m


MARCA = carregar_marca(caminho_marca())
ACCENT, DARK, LIGHT = MARCA["_rgb"]["acento"], MARCA["_rgb"]["escuro"], MARCA["_rgb"]["claro"]
GREEN = ACCENT  # nome antigo (kit/render.py e afins)


def _lum(c):
    f = lambda v: v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4  # noqa: E731
    r, g, b = (f(x / 255.0) for x in c)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contraste(a, b):
    la, lb = sorted((_lum(a), _lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def legivel(cor, fundo, minimo=4.5):
    """clareia a cor (mistura com branco) até ter contraste >= minimo sobre o fundo"""
    c, k = tuple(cor), 0.0
    while contraste(c, fundo) < minimo and k < 1:
        k += 0.05
        c = tuple(int(round(v + (255 - v) * k)) for v in cor)
    return c


ACCENT_TEXT = legivel(ACCENT, DARK)  # texto/traço fino no acento sobre fundo escuro
ON_ACCENT = (255, 255, 255) if contraste((255, 255, 255), ACCENT) >= 3.0 else DARK  # texto sobre o acento


def tom(c, acento=None):
    """cor desenhada para o verde de referência (#00C597) -> a mesma cor no acento da marca: gira a matiz e escala a
    saturação pelas do acento (o brilho fica). Com o acento igual à referência devolve a própria cor."""
    a = tuple(ACCENT if acento is None else acento)
    if a == REF:
        return tuple(float(v) for v in c)
    h0, s0, _ = colorsys.rgb_to_hsv(*(v / 255.0 for v in REF))
    h1, s1, _ = colorsys.rgb_to_hsv(*(v / 255.0 for v in a))
    h, s, v = colorsys.rgb_to_hsv(*(x / 255.0 for x in c))
    out = colorsys.hsv_to_rgb((h + h1 - h0) % 1.0, min(1.0, s * s1 / s0), v)
    return tuple(round(x * 255, 3) for x in out)


# ------------------------------------------------------------------ fonte
FONT_FILES = MARCA["fonte"]["arquivos"] or {w: os.path.join(FONTS, f"Montserrat-{w}.ttf") for w in (500, 600, 700, 800)}
FONT_CUSTOM = bool(MARCA["fonte"]["arquivos"])


@lru_cache(None)
def font(w, size):
    """fonte da marca no peso mais próximo de w (fonte variável: ajusta o eixo de peso)"""
    k = min(FONT_FILES, key=lambda p: (abs(p - w), -p))
    f = ImageFont.truetype(FONT_FILES[k], size)
    if FONT_CUSTOM:
        try:
            eixos = f.get_variation_axes()
        except OSError:
            eixos = None  # fonte estática
        if eixos:
            nome = lambda a: (a.get("name") or b"").decode("latin-1") if isinstance(a.get("name"), bytes) else str(a.get("name") or "")  # noqa: E731
            f.set_variation_by_axes([max(a["minimum"], min(a["maximum"], w)) if nome(a).lower() in ("weight", "wght") else a["default"]
                                     for a in eixos])
    return f


# ------------------------------------------------------------------ desenho
def rrect(w, h, r, fill, ss=4):
    """retângulo arredondado antisserrilhado (RGBA)"""
    im = Image.new("L", (w * ss, h * ss), 0)
    ImageDraw.Draw(im).rounded_rectangle([0, 0, w * ss - 1, h * ss - 1], r * ss, fill=255)
    a = im.resize((w, h), Image.LANCZOS)
    out = Image.new("RGBA", (w, h), fill[:3] + (0,)); out.putalpha(a.point(lambda v: v * (fill[3] if len(fill) > 3 else 255) // 255))
    return out


def with_shadow(sprite, blur=18, opacity=0.35, dy=8, pad=None):
    pad = pad or blur * 2
    W, H = sprite.width + 2 * pad, sprite.height + 2 * pad
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    a = Image.new("L", (W, H), 0); a.paste(sprite.getchannel("A"), (pad, pad + dy))
    a = a.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * opacity))
    sh.putalpha(a)
    sh.alpha_composite(sprite, (pad, pad))
    return sh, pad


def ff_icon(h, color=ACCENT_TEXT):
    """ícone de avanço rápido (dois triângulos; acento legível, porque fica sobre o escuro)"""
    ss = 4; w = int(h * 1.25)
    im = Image.new("RGBA", (w * ss, h * ss), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for k in range(2):
        x0 = k * w * ss * 0.48
        d.polygon([(x0, 0), (x0 + w * ss * 0.52, h * ss / 2), (x0, h * ss)], fill=color + (255,))
    return im.resize((w, h), Image.LANCZOS)


@lru_cache(None)
def speed_badge(x):
    txt = (f"{x:g}x").replace(".", ",")
    f = font(700, 30); tw = f.getbbox(txt)[2]
    ic = ff_icon(20); w, h = 30 + ic.width + 12 + tw + 26, 56
    base = rrect(w, h, h // 2, DARK + (225,))
    border = rrect(w, h, h // 2, (255, 255, 255, 30)); inner = rrect(w - 2, h - 2, h // 2 - 1, DARK + (255,))
    b = Image.new("RGBA", (w, h)); b.alpha_composite(border); m = Image.new("RGBA", (w, h)); m.alpha_composite(inner, (1, 1))
    spr = Image.new("RGBA", (w, h)); spr.alpha_composite(base)
    spr.alpha_composite(ic, (26, (h - ic.height) // 2))
    ImageDraw.Draw(spr).text((26 + ic.width + 12, h // 2), txt, font=f, fill=(255, 255, 255, 255), anchor="lm")
    return with_shadow(spr, 14, 0.30, 6)


@lru_cache(None)
def lower_third(title, kicker=""):
    ft, fk = font(700, 42), font(700, 19)
    tw = ft.getbbox(title)[2]; kw = (fk.getbbox(kicker.upper())[2] + len(kicker) * 3) if kicker else 0
    w = max(tw, kw) + 2 * 34 + 10; h = 132 if kicker else 96
    spr = rrect(w, h, 20, DARK + (236,))
    bar = rrect(6, h - 44, 3, ACCENT + (255,)); spr.alpha_composite(bar, (24, 22))
    d = ImageDraw.Draw(spr)
    if kicker:
        x = 46
        for ch in kicker.upper():  # espaçamento entre letras
            d.text((x, 30), ch, font=fk, fill=ACCENT_TEXT + (255,), anchor="lt"); x += fk.getbbox(ch)[2] + 3
        d.text((46, 62), title, font=ft, fill=(255, 255, 255, 255), anchor="lt")
    else:
        d.text((46, h // 2), title, font=ft, fill=(255, 255, 255, 255), anchor="lm")
    return with_shadow(spr, 22, 0.35, 10)


@lru_cache(None)
def callout(text):
    f = font(600, 30); tw = f.getbbox(text)[2]; w, h = tw + 2 * 30, 64
    spr = rrect(w, h, 18, DARK + (236,)); d = ImageDraw.Draw(spr)
    d.ellipse([22, h // 2 - 5, 32, h // 2 + 5], fill=ACCENT_TEXT + (255,))
    d.text((44, h // 2), text, font=f, fill=(255, 255, 255, 255), anchor="lm")
    spr2 = Image.new("RGBA", (w + 14, h)); spr2.alpha_composite(spr)
    return with_shadow(spr2, 16, 0.3, 8)


@lru_cache(None)
def spot_label(text):
    f = font(700, 26); tw = f.getbbox(text)[2]; w, h = tw + 2 * 22, 50
    spr = rrect(w, h, h // 2, ACCENT + (255,))
    ImageDraw.Draw(spr).text((w // 2, h // 2), text, font=f, fill=ON_ACCENT + (255,), anchor="mm")
    return with_shadow(spr, 12, 0.3, 6)


def stage_background(W, H, seed=1):
    """palco claro: claro da marca com luz suave no acento e granulado leve"""
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    base = np.array(LIGHT, np.float32)
    g1 = np.exp(-(((x - W * 0.18) / (W * 0.45)) ** 2 + ((y - H * 0.05) / (H * 0.55)) ** 2))
    g2 = np.exp(-(((x - W * 0.92) / (W * 0.40)) ** 2 + ((y - H * 1.05) / (H * 0.50)) ** 2))
    tint = np.array(tom((214, 245, 236)), np.float32)
    img = base[None, None] * (1 - 0.55 * (g1 + g2)[..., None].clip(0, 1)) + tint * (0.55 * (g1 + g2)[..., None].clip(0, 1))
    vign = 1 - 0.05 * ((((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2) / 2)
    img *= vign[..., None]
    img += np.random.default_rng(seed).normal(0, 2.2, (H, W, 1)).astype(np.float32)
    return img.clip(0, 255).astype(np.uint8)


def rrect_alpha(W, H, x0, y0, x1, y1, r, feather=1.0):
    """alfa (H,W) float32 de um retângulo arredondado em coords de saída (subpixel), por distância assinada"""
    xs = np.arange(W, dtype=np.float32) + 0.5; ys = np.arange(H, dtype=np.float32) + 0.5
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; hx, hy = (x1 - x0) / 2 - r, (y1 - y0) / 2 - r
    dx = np.maximum(np.abs(xs - cx) - hx, 0)[None, :]; dy = np.maximum(np.abs(ys - cy) - hy, 0)[:, None]
    qx = (np.abs(xs - cx) - hx)[None, :]; qy = (np.abs(ys - cy) - hy)[:, None]
    sd = np.sqrt(dx ** 2 + dy ** 2) + np.minimum(np.maximum(qx, qy), 0) - r
    return np.clip(0.5 - sd / feather, 0, 1), sd


# ------------------------------------------------------------------ vinheta (web/intro.html)
def _tamanho_svg(p):
    """(w, h) de um SVG pelo width/height ou viewBox da raiz"""
    head = open(p, encoding="utf-8", errors="ignore").read(4096)
    tag = re.search(r"<svg\b[^>]*>", head, re.S)
    tag = tag.group(0) if tag else ""
    num = lambda k: re.search(rf'\b{k}\s*=\s*["\']\s*([\d.]+)\s*(px)?\s*["\']', tag)  # noqa: E731
    w, h = num("width"), num("height")
    if w and h:
        return float(w.group(1)), float(h.group(1))
    vb = re.search(r'viewBox\s*=\s*["\']\s*[-\d.]+[\s,]+[-\d.]+[\s,]+([\d.]+)[\s,]+([\d.]+)', tag)
    if vb:
        return float(vb.group(1)), float(vb.group(2))
    raise ValueError(f"SVG sem width/height nem viewBox: {p}")


def _copiar_imagem(src, dst_dir, nome):
    """PNG/WebP/JPG: recorta as bordas transparentes e grava PNG; SVG: copia. Devolve {src, w, h}"""
    if src.lower().endswith(".svg"):
        shutil.copyfile(src, os.path.join(dst_dir, nome + ".svg"))
        w, h = _tamanho_svg(src)
        return {"src": nome + ".svg", "w": w, "h": h}
    im = Image.open(src).convert("RGBA")
    bb = im.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
    if bb:
        pad = max(2, int(0.01 * max(im.size)))
        im = im.crop((max(0, bb[0] - pad), max(0, bb[1] - pad), min(im.width, bb[2] + pad), min(im.height, bb[3] + pad)))
    im.save(os.path.join(dst_dir, nome + ".png"))
    return {"src": nome + ".png", "w": im.width, "h": im.height}


def dados_web(m=None):
    """configuração da vinheta (o que web/intro.html lê) + arquivos a copiar {nome no pacote: caminho}"""
    m = m or MARCA
    a, d, l = m["_rgb"]["acento"], m["_rgb"]["escuro"], m["_rgb"]["claro"]
    at = legivel(a, d)
    c3 = lambda c: ",".join(str(int(round(v))) for v in c)  # noqa: E731
    t = lambda c: hexa(tom(c, a))  # noqa: E731
    cfg = {"serie": m["serie"], "estilo": m["vinheta"]["estilo"], "frase": m["cartela"]["frase"],
           "cores": {"acento": hexa(a), "acento_rgb": c3(a), "acento_texto": hexa(at), "acento_texto_rgb": c3(at),
                     "escuro": hexa(d), "claro": hexa(l), "claro_rgb": c3(l),
                     "fundo": [t((7, 9, 10)), t((16, 22, 21)), t((10, 13, 13)), t((5, 6, 6))]},
           "fonte": {"familia": m["fonte"].get("familia") or "Marca", "arquivos": {}},
           "logo": {"wordmark_altura": float(m["logo"].get("wordmark_altura") or 0.5)}}
    arqs = {}
    for w, p in sorted(m["fonte"]["arquivos"].items()):
        nome = f"fonte-{w}{os.path.splitext(p)[1].lower()}"
        cfg["fonte"]["arquivos"][str(w)] = nome; arqs[nome] = p
    for k in ("arquivo", "simbolo", "wordmark"):
        if m["logo"][k]:
            arqs["img:" + k] = m["logo"][k]
    if m["vinheta"]["estilo"] == "ecosistema-reciclagem":  # peças, símbolo, brilho e nome copiados sem recorte (o quadro é a geometria)
        geo = json.load(open(m["logo"]["pecas"], encoding="utf-8")); pasta = os.path.dirname(m["logo"]["pecas"])
        geo = {k: v for k, v in geo.items() if not k.startswith("_")}
        for parte in [geo["simbolo"], geo["brilho"], geo["wordmark"]] + geo["pecas"]:
            nome = "pecas-" + os.path.basename(parte["arquivo"])
            arqs[nome] = os.path.join(pasta, parte["arquivo"]); parte["arquivo"] = nome
        cfg["pecas"] = geo
    return cfg, arqs


def publicar_web(web_dir, m=None):
    """copia a configuração e os arquivos da vinheta para <web>/_marca/<hash>/ (o servidor da página serve só web/) e
    devolve o caminho do JSON relativo a web/. Pasta por conteúdo: dois renders ao mesmo tempo não se atrapalham."""
    cfg, arqs = dados_web(m)
    h = hashlib.sha1(b"marca-web-v1" + json.dumps(cfg, sort_keys=True, ensure_ascii=False).encode())
    for k, p in sorted(arqs.items()):
        h.update(k.encode()); h.update(open(p, "rb").read())
    raiz = os.path.join(web_dir, "_marca"); dest = os.path.join(raiz, h.hexdigest()[:12])
    if not os.path.isfile(os.path.join(dest, "marca.json")):
        tmp = f"{dest}.tmp{os.getpid()}"
        shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
        for k, p in arqs.items():
            if k.startswith("img:"):
                cfg["logo"][k[4:]] = _copiar_imagem(p, tmp, k[4:])
            else:
                shutil.copyfile(p, os.path.join(tmp, k))
        with open(os.path.join(tmp, "marca.json"), "w", encoding="utf-8") as fh:
            json.dump(cfg, fh, ensure_ascii=False, indent=1)
        try:
            os.rename(tmp, dest)
        except OSError:  # outro processo publicou o mesmo conteúdo antes
            shutil.rmtree(tmp, ignore_errors=True)
    for velho in os.listdir(raiz):  # limpa pacotes de marcas antigas (mais de 1 dia sem uso)
        p = os.path.join(raiz, velho)
        if p != dest and os.path.isdir(p) and time.time() - os.path.getmtime(p) > 86400:
            shutil.rmtree(p, ignore_errors=True)
    os.utime(dest)
    return f"_marca/{os.path.basename(dest)}/marca.json"


if __name__ == "__main__":
    if "--web" in sys.argv:
        print(publicar_web(os.path.abspath(sys.argv[sys.argv.index("--web") + 1])))
        print(MARCA["cartela"]["frase"])
    else:
        print("marca.json:", MARCA["_arquivo"] or "(nenhum: padrão neutro)")
        print("série:", MARCA["serie"] or "(sem rótulo)", "| vinheta:", MARCA["vinheta"]["estilo"], "| cartela:", MARCA["cartela"]["frase"])
        if MARCA["vinheta"].get("som") or MARCA["vinheta"].get("som_ausente"):
            print("som da vinheta:", MARCA["vinheta"].get("som") or f"FALTA {MARCA['vinheta']['som_ausente']} (vai o sintetizado)")
        print("cores: acento", hexa(ACCENT), "texto", hexa(ACCENT_TEXT), "sobre o acento", hexa(ON_ACCENT), "escuro", hexa(DARK), "claro", hexa(LIGHT))
        print("fonte:", MARCA["fonte"].get("familia"), {w: os.path.relpath(p, TUT_HOME) for w, p in FONT_FILES.items()})
        print("logo:", {k: v for k, v in MARCA["logo"].items() if v})
