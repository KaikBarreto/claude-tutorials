#!/usr/bin/env python3
"""T22 · semente apos-capNN a partir do que o APP gravou na minha instância (54322) no ensaio do capítulo NN.
Uso: python3 -I rec/t22/t22_estado.py NN      (logo depois da gravação do capítulo, antes de outro reset; o t22_ens.sh NN --estado chama)

1. lê o estado de agora (/__dev/state) das tabelas da aula;
2. zera a instância e aplica as sementes de partida do capítulo (as do gerar.py), lê a base;
3. grava rec/mundo/seeds-extra/t22/apos-capNN.json com as linhas novas (tabela -> [linhas]), as alteradas (_patch {match:{id}, set}) e as
   que sumiram (_remove {id}). Ids e instantes ficam literais (o capítulo seguinte parte exatamente deste estado).
Capítulos 2 e 3: as sementes apos-cap02/apos-cap03 são as do t22_sementes.py (ids fixos); aqui só confere se o app gravou o mesmo.
No fim a instância fica com a base aplicada (o próximo ensaio zera de novo)."""
import json
import os
import sys
import urllib.request

URL = 'http://127.0.0.1:54322'
HERE = os.path.dirname(os.path.abspath(__file__))
DIR = os.path.normpath(os.path.join(HERE, '..', 'mundo', 'seeds-extra', 't22'))
TABELAS = ['company_groups', 'company_group_members', 'group_materials', 'material_group_links', 'group_price_tables', 'group_price_table_items',
           'group_shared_entities', 'group_financial_categories', 'group_push_audit', 'group_stock_transfers', 'materials', 'stock_movements',
           'financial_categories', 'price_tables', 'price_table_items', 'customers', 'suppliers', 'companies', 'subscription_payments']
sys.path.insert(0, HERE)
import gerar  # noqa: E402  (SEMENTE: as sementes de partida de cada capítulo)


def get(caminho):
    return json.load(urllib.request.urlopen(URL + caminho, timeout=30))


def post(caminho, corpo=None):
    req = urllib.request.Request(URL + caminho, data=json.dumps(corpo or {}).encode(), method='POST', headers={'content-type': 'application/json'})
    return json.load(urllib.request.urlopen(req, timeout=60))


def dump():
    return {t: get(f'/__dev/state?table={t}') for t in TABELAS}


def main():
    n = int(sys.argv[1])
    pos = dump()
    post('/__dev/reset')
    r = post('/__dev/seed', {'files': gerar.SEMENTE[n]})
    if not r.get('ok'):
        sys.exit(f'semente de partida não aplicou: {r}')
    base = dump()
    novo, patch, remove = {}, {}, {}
    for t in TABELAS:
        b = {x['id']: x for x in base[t] if 'id' in x}
        p = {x['id']: x for x in pos[t] if 'id' in x}
        for i, row in p.items():
            if i not in b:
                novo.setdefault(t, []).append(row)
            else:
                mud = {k: v for k, v in row.items() if b[i].get(k) != v}
                mud.pop('updated_at', None) if set(mud) == {'updated_at'} else None
                if mud and set(mud) != {'updated_at'}:
                    patch.setdefault(t, []).append({'match': {'id': i}, 'set': mud})
        for i in b:
            if i not in p:
                remove.setdefault(t, []).append({'id': i})
    for t, linhas in novo.items():
        print(f'  novo {t}: {len(linhas)}')
    for t, linhas in patch.items():
        print(f'  alterado {t}: {len(linhas)} ' + '; '.join(','.join(sorted(x["set"])) for x in linhas[:4]))
    for t, linhas in remove.items():
        print(f'  removido {t}: {len(linhas)}')
    if n in (2, 3):
        fixo = json.load(open(os.path.join(DIR, f'apos-cap{n:02d}.json'), encoding='utf8'))
        t = 'company_groups' if n == 2 else 'company_group_members'
        app = (novo.get(t) or [None])[0]
        print(f'  cap{n:02d}: a semente fixa fica (ids estáveis). O app gravou em {t}: {json.dumps(app, ensure_ascii=False)}')
        print(f'  semente fixa: {json.dumps(fixo[t][0], ensure_ascii=False)}')
        return
    saida = dict(novo)
    if patch:
        saida['_patch'] = patch
    if remove:
        saida['_remove'] = remove
    caminho = os.path.join(DIR, f'apos-cap{n:02d}.json')
    json.dump(saida, open(caminho, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print('gravado', os.path.relpath(caminho, os.path.join(HERE, '..', '..')))


if __name__ == '__main__':
    main()
