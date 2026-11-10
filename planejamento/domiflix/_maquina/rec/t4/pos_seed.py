#!/usr/bin/env python3
"""Pós-processa os seeds do T4 depois que `rodar.sh 12 --seed` grava apos-cap12.json:
  1. acrescenta ao checklist "Higienização de split" as duas perguntas de bastidor do plano ("Observações", Texto, e
     "Assinatura do cliente", Assinatura), além das quatro criadas ao vivo (o capítulo 13 mostra "6 perguntas");
  2. deriva apos-cap13.json e apos-cap14.json de apos-cap12.json (os capítulos 13 e 14 não criam nada).
Idempotente: rodar de novo não duplica as perguntas. Uso: python3 rec/t4/pos_seed.py"""
import json
import os
import shutil
import uuid

HERE = os.path.dirname(os.path.abspath(__file__))
SEEDS = os.path.normpath(os.path.join(HERE, '..', 'fakebase', 'seeds-extra', 't4'))
ARQ = os.path.join(SEEDS, 'apos-cap12.json')

EXTRAS = [  # (texto, tipo, obrigatória)
    ('Observações', 'text', False),
    ('Assinatura do cliente', 'signature', True),
]


def main():
    d = json.load(open(ARQ, encoding='utf-8'))
    tpl = next(t for t in d['form_templates'] if t['name'] == 'Higienização de split')
    qs = d['form_questions']
    mine = [q for q in qs if q['template_id'] == tpl['id']]
    base = next(q for q in mine if q['question'] == 'Estado da serpentina')
    pos = max(q['position'] for q in mine) + 1
    feitas = {q['question'] for q in mine}
    for texto, tipo, obrig in EXTRAS:
        if texto in feitas:
            continue
        q = dict(base)
        q.update({
            'id': str(uuid.uuid5(uuid.NAMESPACE_DNS, f'domiflix-t4-{texto}')),
            'question': texto, 'question_type': tipo, 'is_required': obrig, 'description': None,
            'position': pos, 'answer_types': None, 'answer_mode': 'exclusive',
            'require_camera': False, 'require_camera_video': False, 'options': None,
        })
        qs.append(q)
        pos += 1
        print(f'+ pergunta de bastidor: {texto} ({tipo}) posição {q["position"]}')
    with open(ARQ, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    for n in (13, 14):
        shutil.copyfile(ARQ, os.path.join(SEEDS, f'apos-cap{n}.json'))
    n = sum(1 for q in qs if q['template_id'] == tpl['id'])
    print(f'apos-cap12/13/14.json: Higienização de split com {n} perguntas')


if __name__ == '__main__':
    main()
