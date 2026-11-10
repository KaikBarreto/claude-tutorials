"""Depois de gravar o cap. 5 do T1: leva o logo que o robô enviou em "Substituir" (o JPEG que o app gerou a partir do PNG com o
texto branco) para as sementes que vêm depois (apos-cap05 .. apos-cap12), no campo white_label_logo_url, como data URI.
O robô guarda o arquivo no passo `eval` "guarda o logo enviado..." (campo `value` do t1-cap05.actions.json). Sem esse passo
(gravação antiga), emula o processImageFile do app com o PIL (máx. 1920 px, fundo preto no lugar do transparente, JPEG q 82).
uso: python3 -I rec/t1/atualizar_semente_logo.py"""
import base64
import glob
import io
import json
import os
import re

AQUI = os.path.dirname(os.path.abspath(__file__))
SEEDS = os.path.join(os.path.dirname(AQUI), "fakebase", "seeds-extra", "t1")
acts = json.load(open(os.path.join(AQUI, "t1-cap05.actions.json")))["actions"]
uri = next((a.get("value") for a in acts if a.get("do") == "eval" and "guarda o logo enviado" in (a.get("label") or "") and a.get("ok")), None)
if uri and uri.startswith("data:image/"):
    origem = "robô (bytes que o app enviou)"
else:
    from PIL import Image
    im = Image.open(os.path.join(AQUI, "assets", "glacial_horizontal_texto_branco.png")).convert("RGBA")
    if max(im.size) > 1920:
        k = 1920 / max(im.size)
        im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    fundo = Image.new("RGB", im.size, (0, 0, 0))
    fundo.paste(im, mask=im.split()[3])
    buf = io.BytesIO()
    fundo.save(buf, "JPEG", quality=82)
    uri = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    origem = "emulação com o PIL (o actions.json não trouxe o arquivo)"
# Redução para as sementes: o JPEG que o app gera tem até 1920 px de largura; com ele a geração da imagem social e as prévias do
# QR/relatório levam ~4 s na máquina de gravação (0,9 s com o logo antigo de 900 px) e os gestos do robô saem 3 a 5 s atrasados.
# A mesma imagem em 900 px de largura (como era o logo da empresa) mantém o tempo e não muda nada na tela (o menu mostra ~160 px).
from PIL import Image  # noqa: E402
LARG = 900
raw = Image.open(io.BytesIO(base64.b64decode(uri.split(",", 1)[1]))).convert("RGB")
if raw.width > LARG:
    raw = raw.resize((LARG, round(raw.height * LARG / raw.width)), Image.LANCZOS)
    buf = io.BytesIO()
    raw.save(buf, "JPEG", quality=85)
    uri = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
print(f"logo do White Label: {len(uri)} caracteres ({raw.width}x{raw.height}), de: {origem}")
NOVO = "logo completo = versão da marca com o texto branco enviada em Substituir (31/10, pedido do Kaik: o menu é escuro)"
for n in range(5, 13):
    p = os.path.join(SEEDS, f"apos-cap{n:02d}.json")
    d = json.load(open(p))
    d["_patch"]["company_settings"][0]["set"]["white_label_logo_url"] = uri
    d["_comentario"] = re.sub(r"logo completo = logo da empresa", NOVO, d["_comentario"])
    if "texto branco" not in d["_comentario"]:
        d["_comentario"] += " | White Label: " + NOVO + "."
    open(p, "w").write(json.dumps(d, ensure_ascii=False, indent=1))
    print("  atualizado", os.path.basename(p))
