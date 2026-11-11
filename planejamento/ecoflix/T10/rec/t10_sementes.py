#!/usr/bin/env python3
"""T10 · sementes extras (rec/mundo/seeds-extra/t10/) e as 2 fotos fictícias da compra de 09/11 (rec/mundo/storage/order-attachments/t10/).

Lê o mundo base (rec/mundo/seeds/02-cadastros.json e 03-historico.json): rode de novo SEMPRE que o mundo base mudar (o número do pedido
de 09/11 e os saldos de hoje vêm dele). Uso:  python3 -I rec/t10/t10_sementes.py
  t10/inicio      : as 2 fotos (order_attachments) da compra de 09/11 do Depósito Irmãos Siqueira (860 kg de ferro pesado). Caps. 0 a 12.
  t10/apos-cap03  : a transferência do cap03 (320 kg do Ferro misto para o Ferro pesado, Rafael, 10/11 08:35), gravada como o handler
                    transfer_material_stock grava (duas linhas TRANSFERENCIA, created_at = transaction_at). Caps. 4 a 12.
As fotos são DESENHO gerado por código (caçamba com sucata de ferro; sem placa, rosto, marca nem texto): nada de foto real.
"""
import json
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
TUT = os.path.normpath(os.path.join(HERE, '..', '..'))
MUNDO = os.path.join(TUT, 'rec', 'mundo')
SAIDA = os.path.join(MUNDO, 'seeds-extra', 't10')
FOTOS = os.path.join(MUNDO, 'storage', 'order-attachments', 't10')
EMPRESA = '@id:company.reciclavale'
TRANSF = 320
HORA_TRANSF = '2026-11-10T11:35:20.000Z'   # 08:35:20 em Taubaté (o robô transfere ~08:35)


def base():
    cad = json.load(open(os.path.join(MUNDO, 'seeds', '02-cadastros.json'), encoding='utf8'))
    hist = json.load(open(os.path.join(MUNDO, 'seeds', '03-historico.json'), encoding='utf8'))
    return cad, hist


def compra_0911(cad, hist):
    """a compra de 09/11 do Depósito Irmãos Siqueira com 860 kg de ferro pesado (o número do pedido muda quando o mundo base muda)"""
    sup = next(s['id'] for s in cad['suppliers'] if 'Siqueira' in s.get('name', ''))
    itens = {}
    for it in hist['purchase_items']:
        itens.setdefault(it.get('purchase_id') or it.get('order_id'), []).append(it)
    achadas = [p for p in hist['purchases'] if str(p.get('transaction_at', '')).startswith('2026-11-09') and p.get('supplier_id') == sup
               and any(i.get('material_id') == '@id:material.ferro_pesado' and abs(float(i.get('quantity') or 0) - 860) < 0.01 for i in itens.get(p['id'], []))]
    if len(achadas) != 1:
        raise SystemExit(f'compra de 09/11 (Siqueira, 860 kg de ferro pesado): achei {len(achadas)} no mundo base')
    return achadas[0]


def desenha_fotos():
    """duas fotos desenhadas: a caçamba com a sucata de ferro (de lado e mais de perto); determinístico"""
    from PIL import Image, ImageDraw, ImageFilter
    os.makedirs(FOTOS, exist_ok=True)
    saidas = []
    for k, (semente, zoom) in enumerate(((11, 1.0), (23, 1.35)), start=1):
        rnd = random.Random(semente)
        W, H = 1280, 960
        im = Image.new('RGB', (W, H))
        d = ImageDraw.Draw(im)
        for y in range(H):   # céu nublado e o pátio de terra batida
            if y < 430:
                t = y / 430
                d.line([(0, y), (W, y)], fill=(int(196 + 20 * t), int(206 + 14 * t), int(214 + 8 * t)))
            else:
                t = (y - 430) / (H - 430)
                d.line([(0, y), (W, y)], fill=(int(158 - 30 * t), int(146 - 28 * t), int(128 - 26 * t)))
        d.rectangle([0, 300, W, 430], fill=(150, 152, 150))          # muro do pátio
        for x in range(0, W, 160):
            d.line([(x, 300), (x, 430)], fill=(132, 134, 132), width=3)
        for _ in range(900):                                           # cascalho
            x, y = rnd.randint(0, W), rnd.randint(440, H)
            c = rnd.randint(90, 150)
            d.ellipse([x, y, x + 3, y + 2], fill=(c, c - 8, c - 18))
        cx, base_y = W // 2 + rnd.randint(-40, 40), int(800 + 60 * (zoom - 1))
        larg, alt = int(820 * zoom), int(300 * zoom)
        topo = base_y - alt
        d.ellipse([cx - larg // 2 - 20, base_y - 18, cx + larg // 2 + 20, base_y + 30], fill=(92, 84, 70))   # sombra
        sucata = []                                                    # a pilha acima da borda
        for _ in range(int(150 * zoom)):
            x = cx + rnd.randint(-larg // 2 + 40, larg // 2 - 40)
            y = topo + rnd.randint(-int(150 * zoom), 30)
            tom = rnd.choice([(96, 92, 88), (120, 84, 58), (140, 98, 62), (78, 74, 72), (110, 106, 100), (150, 110, 70)])
            forma = rnd.random()
            if forma < 0.45:   # vergalhão / barra
                comp = rnd.randint(60, 220)
                ang = rnd.uniform(-0.9, 0.9)
                import math
                x2, y2 = x + comp * math.cos(ang), y + comp * math.sin(ang)
                sucata.append(('linha', [(x, y), (x2, y2)], tom, rnd.randint(5, 14)))
            elif forma < 0.8:   # chapa
                w, h = rnd.randint(40, 130), rnd.randint(20, 70)
                pts = [(x, y), (x + w, y + rnd.randint(-15, 15)), (x + w + rnd.randint(-10, 10), y + h), (x + rnd.randint(-10, 10), y + h + rnd.randint(-10, 10))]
                sucata.append(('poli', pts, tom, 0))
            else:               # perfil / viga em L
                w, h = rnd.randint(80, 200), rnd.randint(14, 26)
                sucata.append(('poli', [(x, y), (x + w, y - rnd.randint(0, 30)), (x + w, y - rnd.randint(0, 30) + h), (x, y + h)], tom, 0))
        for tipo, pts, tom, larg_l in sucata:
            if tipo == 'linha':
                d.line(pts, fill=tom, width=larg_l)
            else:
                d.polygon(pts, fill=tom, outline=tuple(max(0, v - 30) for v in tom))
        # a caçamba (trapézio com nervuras), na frente da pilha
        amarelo, escuro = (214, 150, 32), (170, 112, 22)
        d.polygon([(cx - larg // 2, topo), (cx + larg // 2, topo), (cx + larg // 2 - int(90 * zoom), base_y), (cx - larg // 2 + int(90 * zoom), base_y)], fill=amarelo)
        for i in range(1, 8):
            x = cx - larg // 2 + i * larg // 8
            d.line([(x, topo + 6), (x - (x - cx) * 0.2, base_y - 4)], fill=escuro, width=int(9 * zoom))
        d.rectangle([cx - larg // 2 - 6, topo - 10, cx + larg // 2 + 6, topo + 8], fill=escuro)
        for _ in range(60):   # ferrugem e marcas de uso
            x = cx + rnd.randint(-larg // 2 + 60, larg // 2 - 60)
            y = rnd.randint(topo + 20, base_y - 20)
            r = rnd.randint(4, 18)
            d.ellipse([x, y, x + r, y + r // 2], fill=(150, 88, 40))
        im = im.filter(ImageFilter.GaussianBlur(0.8))
        caminho = os.path.join(FOTOS, f'compra-0911-{k}.jpg')
        im.save(caminho, 'JPEG', quality=84)
        saidas.append((f't10/compra-0911-{k}.jpg', os.path.getsize(caminho)))
    return saidas


def main():
    cad, hist = base()
    p = compra_0911(cad, hist)
    fotos = desenha_fotos()
    os.makedirs(SAIDA, exist_ok=True)
    t0 = p.get('created_at') or p['transaction_at']
    inicio = {
        '_doc': f"T10 · as 2 fotos da compra de 09/11 ({p.get('order_ref') or p['id']}, Depósito Irmãos Siqueira, 860 kg de ferro pesado). "
                "Gerado por rec/t10/t10_sementes.py (desenhos: rec/mundo/storage/order-attachments/t10/).",
        'order_attachments': [
            {'id': f'@id:t10.foto{k}', 'company_id': EMPRESA, 'order_id': p['id'], 'order_kind': 'purchase', 'storage_path': caminho,
             'file_name': os.path.basename(caminho), 'file_size': tam, 'mime': 'image/jpeg', 'created_by': p.get('created_by'), 'created_at': t0}
            for k, (caminho, tam) in enumerate(fotos, start=1)],
    }
    mats = {m['id']: m for m in cad['materials']}
    o, dst = mats['@id:material.ferro_misto'], mats['@id:material.ferro_pesado']
    oa, da = float(o['current_stock']), float(dst['current_stock'])
    od, dd = round(oa - TRANSF, 3), round(da + TRANSF, 3)
    base_mov = {'company_id': EMPRESA, 'type': 'TRANSFERENCIA', 'created_by': '@id:user.rafael', 'transaction_at': HORA_TRANSF,
                'transaction_date': '2026-11-10', 'created_at': HORA_TRANSF}
    apos3 = {
        '_doc': f'T10 · depois do cap03: {TRANSF} kg do Ferro misto ({oa:g} -> {od:g}) para o Ferro pesado ({da:g} -> {dd:g}), Rafael, 10/11 08:35. '
                'Gerado por rec/t10/t10_sementes.py (como o handler transfer_material_stock grava).',
        '_patch': {'materials': [{'match': {'id': o['id']}, 'set': {'current_stock': od}},
                                 {'match': {'id': dst['id']}, 'set': {'current_stock': dd}}]},
        'stock_movements': [
            {**base_mov, 'id': '@id:t10.transf.sai', 'material_id': o['id'], 'quantity': -TRANSF, 'stock_before': oa, 'stock_after': od,
             'description': f"Transferência para {dst['name']}"},
            {**base_mov, 'id': '@id:t10.transf.entra', 'material_id': dst['id'], 'quantity': TRANSF, 'stock_before': da, 'stock_after': dd,
             'description': f"Transferência de {o['name']}", 'related_movement_id': '@id:t10.transf.sai'},
        ],
    }
    for nome, dado in (('inicio', inicio), ('apos-cap03', apos3)):
        with open(os.path.join(SAIDA, f'{nome}.json'), 'w', encoding='utf8') as f:
            json.dump(dado, f, ensure_ascii=False, indent=1)
    print(f"compra de 09/11: {p['id']} ({p.get('order_ref')}); fotos {[c for c, _ in fotos]}")
    print(f'transferência: ferro misto {oa:g} -> {od:g}; ferro pesado {da:g} -> {dd:g}')


if __name__ == '__main__':
    main()
