#!/usr/bin/env python3
"""T21 · monta o mundo SÓ da T21 em /dev/shm/t21_mundo (FAKE_MUNDO): é o rec/mundo (tudo por link simbólico) com, por cima, os handlers
de rec/t21/overlay/handlers (substituem os de mesmo nome do mundo base, sem editar o base) e o schema.json com as tabelas que o Cato
1.60 usa e o schema gerado não tem (cato_attachments, cato_memory_items, cato_memory_state). Rode `python3 -I rec/t21/t21_mundo.py`
antes de subir a instância (t21_corpo.sh faz isso sozinho)."""
import json, os, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
REC = os.path.normpath(os.path.join(HERE, '..'))
BASE = os.path.join(REC, 'mundo')
DEST = '/dev/shm/t21_mundo'
OVER = os.path.join(HERE, 'overlay')

def col(t, n=True, o=0):
    return {'t': t, 'n': n, 'o': o}

NOVAS = {
    'cato_attachments': {'columns': {
        'id': col('string', False, 1), 'company_id': col('string', False, 0), 'user_id': col('string', False, 0), 'session_id': col('string', True, 0),
        'storage_path': col('string', False, 0), 'file_name': col('string', False, 0), 'mime_type': col('string', False, 0),
        'size_bytes': col('number', False, 0), 'created_at': col('string', False, 1)}, 'relationships': []},
    'cato_memory_items': {'columns': {
        'id': col('string', False, 1), 'company_id': col('string', False, 0), 'user_id': col('string', True, 0), 'scope': col('string', False, 0),
        'kind': col('string', False, 0), 'content': col('string', False, 0), 'origin': col('string', False, 0),
        'created_at': col('string', False, 1), 'updated_at': col('string', False, 1), 'expires_at': col('string', False, 0)}, 'relationships': []},
    'cato_memory_state': {'columns': {
        'id': col('string', False, 1), 'company_id': col('string', False, 0), 'user_id': col('string', False, 0), 'decision': col('string', False, 0),
        'enabled': col('boolean', False, 1), 'shared_enabled': col('boolean', False, 1)}, 'relationships': []},
}

def main():
    if os.path.isdir(DEST):
        shutil.rmtree(DEST)
    os.makedirs(DEST)
    for nome in os.listdir(BASE):
        if nome in ('handlers', 'schema.json'):
            continue
        os.symlink(os.path.join(BASE, nome), os.path.join(DEST, nome))
    s = json.load(open(os.path.join(BASE, 'schema.json'), encoding='utf8'))
    tabs = s['tables'] if 'tables' in s else s
    for k, v in NOVAS.items():
        tabs[k] = v
    json.dump(s, open(os.path.join(DEST, 'schema.json'), 'w', encoding='utf8'))
    for sub in os.listdir(os.path.join(BASE, 'handlers')):
        d = os.path.join(DEST, 'handlers', sub)
        os.makedirs(d)
        origem = os.path.join(BASE, 'handlers', sub)
        sob = os.path.join(OVER, 'handlers', sub)
        trocados = set(os.listdir(sob)) if os.path.isdir(sob) else set()
        for f in os.listdir(origem):
            if f not in trocados:
                os.symlink(os.path.join(origem, f), os.path.join(d, f))
        for f in trocados:
            os.symlink(os.path.join(sob, f), os.path.join(d, f))
    print('mundo da T21 em', DEST)

main()
