#!/usr/bin/env python3
"""T12 · escreve rec/mundo/seeds-extra/t12/rastreamento.json: o motorista Tiago Freitas com login (drivers.user_id) e o trajeto fictício da
ordem 7 (Taubaté -> Rua das Paineiras), do "Saiu" às 06:40 ao último ping às 07:00:50 (o selo "Ao vivo" dura 2 min depois do último
ponto). Só o capítulo 13 usa. Uso: python3 -I rec/t12/t12_rastreamento.py"""
import json
import os
from datetime import datetime, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.normpath(os.path.join(HERE, '..', 'mundo', 'seeds-extra', 't12', 'rastreamento.json'))
CO, TIAGO, USER = '@id:company.reciclavale', '@id:motorista.picape', '@id:t12.user.tiago'
ORDEM7 = '@id:t12.ordem.7'


def z(hh, mm, ss=0):
    t = datetime(2026, 11, 10, hh, mm, ss) + timedelta(hours=3)
    return t.strftime('%Y-%m-%dT%H:%M:%S.000Z')


A = (-23.0105, -45.5412)     # pátio da Recicla Vale
B = (-23.0236, -45.5588)     # Rua das Paineiras (fictícia), Taubaté
pts = []
quando = [(6, 40, 5), (6, 41, 0), (6, 43, 0), (6, 45, 30), (6, 48, 0), (6, 50, 30), (6, 53, 0), (6, 55, 30), (6, 57, 40), (6, 59, 20), (7, 0, 50)]
tipos = ['saiu', 'a_caminho'] + ['ping'] * 9
for i, ((h, m, s), tp) in enumerate(zip(quando, tipos)):
    f = i / (len(quando) - 1)
    # sai pela latitude e vira na esquina (rota "em L" com leve curva)
    lat = A[0] + (B[0] - A[0]) * min(1, f * 1.5)
    lng = A[1] + (B[1] - A[1]) * max(0, (f - 0.35) * 1.55) if f > 0.35 else A[1] + (B[1] - A[1]) * 0.02 * i
    pts.append({'id': f'@id:t12.pos.{i:02d}', 'company_id': CO, 'order_id': ORDEM7, 'driver_id': TIAGO, 'user_id': USER, 'event_type': tp,
                'lat': round(lat, 6), 'lng': round(lng, 6), 'accuracy_m': 18 if i < 10 else 24, 'speed_kmh': 0 if i == 0 else 31 + (i * 3) % 14,
                'heading_deg': 225, 'address': None, 'recorded_at': z(h, m, s), 'created_at': z(h, m, s)})
out = {'_doc': 'T12 · rastreamento: o trajeto de Tiago Freitas na ordem 7 (gerado por rec/t12/t12_rastreamento.py).',
       'collection_driver_locations': pts,
       '_patch': {'drivers': [{'match': {'id': TIAGO}, 'set': {'user_id': USER}}]}}
os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
json.dump(out, open(SAIDA, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print('gravado', SAIDA, len(pts), 'pontos')
