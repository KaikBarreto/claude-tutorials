#!/usr/bin/env python3
"""T10 · "corte" entre os capítulos 3 e 4 (roteiro.md, "Criado ao vivo"): acrescenta ao `seeds-extra/t10/apos-cap03.json` (diff do ensaio do cap. 3:
funil, seis etapas e a oportunidade do colégio) as outras TRÊS oportunidades, que na aula já "estão cadastradas do mesmo jeito":
  - PMOC anual - Hotel Mirante do Mar · R$ 14.400,00 · 70% · Google · Tatiane Ribeiro · Negociação, com uma "Mudança de estágio" de Proposta para Negociação;
  - Split 12.000 BTUs no quarto - Marcos Antônio Braga · R$ 4.550,00 · 50% · Instagram · Camila · Proposta;
  - Higienização de 2 splits - Luana Martins · R$ 380,00 · 40% · Site · Camila · Proposta.
Os ids de etapas, funil, clientes e usuários vêm do apos-cap03.json e do fakebase vivo (FAKE_URL), nunca copiados à mão. Idempotente (não duplica).
Rodar logo depois de `rec/t10/snap.mjs diff 3`, na mesma trava (o ensaio do cap. 3 deixou o estado no fakebase): `python3 -I rec/t10/corte.py`.
"""
import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
FAKE = os.environ.get('FAKE_URL', 'http://127.0.0.1:54328')
ARQ = os.path.normpath(os.path.join(HERE, '..', 'fakebase', 'seeds-extra', 't10', 'apos-cap03.json'))
EMP = '9c307966-79f1-567c-ac4d-d5fd3c1a2f40'


def estado(tabela):
    with urllib.request.urlopen(f'{FAKE}/__dev/state?table={tabela}', timeout=20) as r:
        return json.load(r)


def main():
    d = json.load(open(ARQ, encoding='utf8'))
    etapas = {e['name']: e for e in d.get('crm_stages', [])}
    for n in ('Lead', 'Visita técnica', 'Proposta', 'Negociação', 'Fechado (Ganho)', 'Fechado (Perdido)'):
        if n not in etapas:
            sys.exit(f'apos-cap03.json sem a etapa "{n}": rode o ensaio do cap. 3 (--seed) antes')
    cli = {c['name']: c['id'] for c in estado('customers')}
    usr = {p['full_name']: p['user_id'] for p in estado('profiles')}
    novos = [
        ('PMOC anual - Hotel Mirante do Mar', 'Hotel Mirante do Mar', 14400, 70, 'Google', 'Negociação', 'Tatiane Ribeiro', '2026-12-18', '2026-10-29T14:10:00.000Z',
         'Contrato anual de manutenção dos aparelhos do hotel.'),
        ('Split 12.000 BTUs no quarto - Marcos Antônio Braga', 'Marcos Antônio Braga', 4550, 50, 'Instagram', 'Proposta', 'Camila Duarte', '2026-12-10',
         '2026-10-31T10:30:00.000Z', None),
        ('Higienização de 2 splits - Luana Martins', 'Luana Martins', 380, 40, 'Site', 'Proposta', 'Camila Duarte', '2026-11-20', '2026-10-30T09:15:00.000Z', None),
    ]
    ja = {l['title'] for l in d.get('leads', [])}
    pipeline = etapas['Lead']['pipeline_id']
    d.setdefault('leads', [])
    d.setdefault('lead_assignees', [])
    d.setdefault('lead_interactions', [])
    feitos = []
    for titulo, cliente, valor, prob, origem, etapa, resp, previsao, criado, notas in novos:
        if titulo in ja:
            continue
        lid = f'e10{len(d["leads"]):05d}-0000-4000-8000-{len(d["leads"]) + 1:012d}'
        d['leads'].append({
            'id': lid, 'company_id': EMP, 'title': titulo, 'customer_id': cli[cliente], 'value': valor, 'probability': prob, 'source': origem,
            'stage_id': etapas[etapa]['id'], 'pipeline_id': pipeline, 'status': 'lead', 'assigned_to': usr[resp], 'created_by': usr[resp],
            'expected_close_date': previsao, 'notes': notas, 'crm_label_ids': [], 'crm_checklists': [], 'created_at': criado, 'updated_at': criado,
        })
        d['lead_assignees'].append({'lead_id': lid, 'user_id': usr[resp], 'is_primary': True, 'created_at': criado})
        if titulo.startswith('PMOC anual'):
            snap = {'from_stage_id': etapas['Proposta']['id'], 'from_stage_name': 'Proposta', 'to_stage_id': etapas['Negociação']['id'], 'to_stage_name': 'Negociação'}
            d['lead_interactions'].append({'id': 'e10a0001-0000-4000-8000-000000000001', 'lead_id': lid, 'interaction_type': 'mudanca_estagio',
                                           'description': json.dumps(snap, ensure_ascii=False), 'created_by': usr[resp], 'created_at': '2026-11-02T16:40:00.000Z'})
        feitos.append(titulo)
    json.dump(d, open(ARQ, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print('corte: ' + (', '.join(feitos) if feitos else 'nada a acrescentar (já estava)'))


if __name__ == '__main__':
    main()
