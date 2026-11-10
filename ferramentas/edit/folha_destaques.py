#!/usr/bin/env python3
"""Folha de TODOS os destaques e zooms do 9:16 da tela real do celular, com o rótulo ao lado e conferência por OCR do texto do alvo (T0 v2).
uso: python3 -I folha_destaques.py [saida.jpg] [NN ...]   (padrão: out/folha_destaques_9x16.jpg e todos os caps/capNN.9x16.chapter.json)
Lê os caps/capNN.9x16.chapter.json e as gravações do celular ("video" do JSON); para cada destaque (spot) tira o quadro em at + 0,9 s,
recorta o alvo, passa o OCR (tesseract) e diz se as duas primeiras palavras do rótulo aparecem (OK / NAO CONFERE). Destaque = retângulo
vermelho; zoom = janela azul (o que o zoom mostra), com o número do zoom no capítulo e os tempos. O tesseract 'eng' tira o acento e
troca letras ("formagao", "ddvidas"): cada palavra vale com parecença >= 0,8; NAO CONFERE pede olhar o quadro. Sem tesseract a folha sai
igual, sem a coluna do OCR.
Saídas: a folha e <saida>.json com [capítulo, tipo, rótulo, t, ok, texto lido] (os destaques também vão para a tela)."""
import difflib
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
saida = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'out', 'folha_destaques_9x16.jpg')
todos = sorted(m.group(1) for p in glob.glob(os.path.join(HERE, 'caps', 'cap*.9x16.chapter.json'))
               if (m := re.fullmatch(r'cap(\d\d[a-z]?)\.9x16\.chapter\.json', os.path.basename(p))))
caps = [f'{int(m[1]):02d}{m[2]}' for a in sys.argv[2:] if (m := re.fullmatch(r'(\d+)([a-z]?)', a))] or todos
OCR = shutil.which('tesseract')
TMP = tempfile.mkdtemp(prefix='folha_destaques_')


def norm(s):
    return re.sub(r'[^a-z0-9 ]', '', unicodedata.normalize('NFD', s.lower()).encode('ascii', 'ignore').decode())


def frame(video, t):
    p = os.path.join(TMP, 'f.png')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(max(t, 0)), '-i', video, '-frames:v', '1', p], check=True)
    return Image.open(p).convert('RGB')


def ocr(img):
    p = os.path.join(TMP, 'o.png')
    img.save(p)
    return subprocess.run([OCR, p, '-', '--psm', '6', '-l', 'eng'], capture_output=True, text=True).stdout


def quebra(texto, fonte, larg):
    """linhas do rótulo que cabem em `larg` px na fonte (palavra a palavra)"""
    linhas, cur = [], ''
    for w in texto.split():
        prova = (cur + ' ' + w).strip()
        if cur and fonte.getlength(prova) > larg:
            linhas.append(cur)
            cur = w
        else:
            cur = prova
    return linhas + [cur]


cells, rel = [], []
try:
    for nn in caps:
        c = json.load(open(os.path.join(HERE, 'caps', f'cap{nn}.9x16.chapter.json')))
        v = c['video']
        if not os.path.isabs(v):
            v = os.path.normpath(os.path.join(HERE, 'caps', v))
        for s in c.get('spots', []):
            t = s['at'] + 0.9
            im = frame(v, t)
            x, y, w, h = s['rect']
            rot = s.get('label') or ''
            ok, txt = None, ''
            if OCR and rot:
                crop = im.crop((max(0, int(x - 6)), max(0, int(y - 6)), min(im.width, int(x + w + 6)), min(im.height, int(y + h + 6))))
                txt = norm(ocr(crop.resize((crop.width * 3, crop.height * 3))))
                lidas = txt.split()  # tolera 1 letra trocada pelo OCR (ç -> g, ú -> d): parecença >= 0,8 por palavra
                ok = all(tok in txt or any(difflib.SequenceMatcher(None, tok, w).ratio() >= 0.8 for w in lidas) for tok in norm(rot).split()[:2])
            ImageDraw.Draw(im).rectangle((x, y, x + w, y + h), outline=(255, 0, 0), width=6)
            reg = im.crop((0, max(0, int(y - 200)), im.width, min(im.height, int(y + h + 200))))
            nota = '' if ok is None else f'  OCR: {"OK" if ok else "NAO CONFERE"}'
            cells.append((f'cap{nn} t={t:.1f}s DESTAQUE "{rot}"{nota}', reg))
            rel.append((nn, 'destaque', rot, round(t, 1), ok, txt[:50]))
        for i, z in enumerate(c.get('zooms', []), 1):
            if 'rect' not in z:
                continue  # repouso (câmera parada) e alvos sem retângulo
            t = z['at'] + 0.8
            im = frame(v, t)
            x, y, w, h = z['rect']
            ImageDraw.Draw(im).rectangle((x + 4, y + 4, x + w - 4, y + h - 4), outline=(0, 160, 255), width=8)
            lab = z.get('label') or f'zoom {i} ({z["at"]:.1f}-{z.get("end", z["at"]):.1f} s)'
            cells.append((f'cap{nn} t={t:.1f}s ZOOM {lab} (janela azul = o que o zoom mostra)', im))
            rel.append((nn, 'zoom', lab, round(t, 1), None, ''))
finally:
    shutil.rmtree(TMP, ignore_errors=True)
if not cells:
    raise SystemExit('nenhum destaque nem zoom nos caps/capNN.9x16.chapter.json')
W = 300
FONTE = os.path.join(os.environ.get('TUT_HOME') or os.path.dirname(os.path.dirname(HERE)), 'kit', 'fonts', 'Montserrat-600.ttf')
font = ImageFont.truetype(FONTE, 12) if os.path.exists(FONTE) else ImageFont.load_default()  # com acento (a padrão do PIL não tem)
rows, per = [], 6
for k in range(0, len(cells), per):
    imgs = []
    for cap, im in cells[k:k + per]:
        r = im.resize((W, int(im.height * W / im.width)))
        canvas = Image.new('RGB', (W, r.height + 36), (20, 20, 20))
        canvas.paste(r, (0, 36))
        ImageDraw.Draw(canvas).text((3, 3), '\n'.join(quebra(cap, font, W - 6)[:2]), fill=(255, 255, 255), font=font)
        imgs.append(canvas)
    hh = max(i.height for i in imgs)
    linha = Image.new('RGB', (W * per, hh), (0, 0, 0))
    for j, i in enumerate(imgs):
        linha.paste(i, (j * W, 0))
    rows.append(linha)
S = Image.new('RGB', (W * per, sum(r.height for r in rows)))
yy = 0
for r in rows:
    S.paste(r, (0, yy))
    yy += r.height
os.makedirs(os.path.dirname(os.path.abspath(saida)), exist_ok=True)
S.save(saida, quality=88)
json.dump(rel, open(saida + '.json', 'w'), ensure_ascii=False)
for r in rel:
    if r[1] == 'destaque':
        print(r)
print(saida, S.size, f'{len(cells)} quadros' + ('' if OCR else ' (sem tesseract: sem OCR)'))
