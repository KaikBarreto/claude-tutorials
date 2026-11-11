#!/usr/bin/env python3
"""T22 · teste de API (sem navegador) da transferência do cap10 na MINHA instância (54322), para achar erro de handler antes do ensaio.
Só roda se nenhuma gravação T22 estiver em curso e o meu ticket não estiver na frente da fila (rec/fila.sh). Zera e semeia como o cap10
(inicio, apos-cap02, apos-cap03, apos-cap09), entra como o Rafael (senha qualquer, gerada aqui e não gravada), liga a aprovação, cria a
transferência (pendente), executa e confere os saldos. A instância fica suja: a próxima gravação zera de novo."""
import json
import os
import secrets
import subprocess
import sys
import urllib.request

URL = 'http://127.0.0.1:54322'
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gerar  # noqa: E402

fila = subprocess.run(['bash', os.path.join(HERE, '..', 'fila.sh'), '--ver'], capture_output=True, text=True).stdout.splitlines()
senhas = [x for x in fila if x[:3].strip('-').isdigit() and x[2] == '-']
if senhas and senhas[0].startswith('22-'):
    sys.exit('meu ticket está na frente da fila: não testo agora')
if subprocess.run(['pgrep', '-f', '^(timeout [0-9]+ )?node rec/record.mjs rec/t22/'], capture_output=True).returncode == 0:
    sys.exit('gravação T22 em curso: não testo agora')


def req(metodo, caminho, corpo=None, token=None, extra=None):
    h = {'content-type': 'application/json', 'apikey': 'x'}
    if token:
        h['authorization'] = 'Bearer ' + token
    h.update(extra or {})
    r = urllib.request.Request(URL + caminho, data=json.dumps(corpo).encode() if corpo is not None else None, method=metodo, headers=h)
    try:
        with urllib.request.urlopen(r, timeout=30) as f:
            t = f.read().decode()
            return f.status, (json.loads(t) if t.strip() else None)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:300]


print(req('POST', '/__dev/reset', {})[0], req('POST', '/__dev/seed', {'files': gerar.SEMENTE[10]})[1])
st, ses = req('POST', '/auth/v1/token?grant_type=password', {'email': 'rafael@reciclavalemetais.example', 'password': secrets.token_urlsafe(9)})
tk = ses['access_token']
g = gerar.GRUPO
print('aprovação:', req('PATCH', f'/rest/v1/company_groups?id=eq.{g}', {'require_transfer_approval': True}, tk, {'Prefer': 'return=representation'})[0])
st, links = req('POST', '/rest/v1/rpc/get_group_linked_material_stock', {'_group_id': g}, tk)
lat = [x for x in links if x['material_name'] == 'Alumínio latinha']
print('linked latinha:', [(x['company_name'], x['current_stock']) for x in lat])
filial = [x for x in lat if x['company_name'] == 'Filial Pindamonhangaba'][0]
matriz = [x for x in lat if x['company_name'] == 'Recicla Vale Metais'][0]
st, dest = req('POST', '/rest/v1/rpc/get_group_destinations_for_member', {'_group_id': g, '_from_company_id': filial['company_id']}, tk)
print('destinos:', st, str(dest)[:160])
st, r = req('POST', '/rest/v1/rpc/create_group_transfer_and_execute', {
    '_group_id': g, '_from_company_id': filial['company_id'], '_to_company_id': matriz['company_id'], '_group_material_id': filial['group_material_id'],
    '_from_material_id': filial['material_id'], '_to_material_id': matriz['material_id'], '_quantity': 1200, '_unit': 'kg',
    '_notes': 'Lote para a Serra Fina Alumínio Reciclagem', '_client_request_id': 'teste-api-t22'}, tk)
print('cria:', st, r)
st, r2 = req('POST', '/rest/v1/rpc/execute_group_stock_transfer', {'_transfer_id': r['transfer_id']}, tk)
print('executa:', st, r2)
st, links = req('POST', '/rest/v1/rpc/get_group_linked_material_stock', {'_group_id': g}, tk)
print('depois:', [(x['company_name'], x['current_stock']) for x in links if x['material_name'] == 'Alumínio latinha'])
st, tr = req('GET', f'/rest/v1/group_stock_transfers?group_id=eq.{g}&select=*', None, tk)
print('transferências:', st, [(t['status'], t['quantity'], t.get('executed_at')) for t in tr] if isinstance(tr, list) else tr)
