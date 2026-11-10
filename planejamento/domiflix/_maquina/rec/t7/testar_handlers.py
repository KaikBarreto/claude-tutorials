#!/usr/bin/env python3
"""T7 · teste de fumaça dos handlers novos (estoque, link público e avaliação) contra o Supabase falso do agente A.

Uso:  FAKE_URL=http://127.0.0.1:54321 python3 -I rec/t7/testar_handlers.py
Reinicia o estado (/__dev/reset), semeia a cadeia do T7 e percorre: seletor de material, baixa na finalização, payload do
link público, avaliação. Sai com código 1 se algo não bater.
"""
import json, os, sys, urllib.request, urllib.error

F = os.environ.get('FAKE_URL', 'http://127.0.0.1:54321')
HERE = os.path.dirname(os.path.abspath(__file__))
cad = json.load(open(os.path.join(HERE, 'cadeia.json'), encoding='utf8'))
OS = cad['os16']
KEY = json.load(open(os.path.join(HERE, '..', 'env.json')))['anonKey']
erros = []


def req(metodo, caminho, corpo=None, token=None, extra=None):
    h = {'apikey': KEY, 'content-type': 'application/json', 'Prefer': 'return=representation'}
    if token:
        h['authorization'] = 'Bearer ' + token
    h.update(extra or {})
    r = urllib.request.Request(F + caminho, method=metodo, headers=h, data=None if corpo is None else json.dumps(corpo).encode())
    try:
        with urllib.request.urlopen(r) as resp:
            t = resp.read().decode()
            return resp.status, (json.loads(t) if t else None)
    except urllib.error.HTTPError as e:
        t = e.read().decode()
        try:
            return e.code, json.loads(t)
        except Exception:
            return e.code, t


def confere(cond, msg):
    print(('  ok   ' if cond else '  ERRO ') + msg)
    if not cond:
        erros.append(msg)


req('POST', '/__dev/reset')
st, _ = req('POST', '/__dev/seed', {'files': cad['inicio']})
confere(st == 200, f'semente da cadeia ({len(cad["inicio"])} arquivos)')

st, auth = req('POST', '/auth/v1/token?grant_type=password', {'email': 'rafael.lima@glacialcold.example', 'password': 'x'})
tok = auth['access_token']
confere(st == 200 and tok, 'login do Rafael')

st, ids = req('POST', '/rest/v1/rpc/get_accessible_inventory_ids', {}, tok)
confere(st == 200 and len(ids) == 3, f'get_accessible_inventory_ids -> {len(ids) if isinstance(ids, list) else ids} materiais')

st, mats = req('GET', '/rest/v1/inventory?select=id,name,quantity,unit&order=name', None, tok)
nome = {m['name']: m for m in mats}
st, locs = req('GET', '/rest/v1/stocks?select=id,name,is_default', None, tok)
loc = locs[0]['id']
confere(len(locs) == 1 and locs[0]['is_default'], 'um local padrão: ' + locs[0]['name'])

# o app grava o rascunho (committed_quantity 0) antes da finalização
linhas = []
for nm, q, obs in [('Limpa-evaporador em spray', 2, 'Limpeza da serpentina da evaporadora'), ('Fita isolante', 1, None)]:
    st, r = req('POST', '/rest/v1/service_order_materials', {'company_id': mats[0].get('company_id') or None, 'service_order_id': OS,
                                                              'inventory_id': nome[nm]['id'], 'stock_id': loc, 'quantity': q, 'notes': obs}, tok)
    confere(st in (200, 201), f'rascunho {nm} x{q} ({st})')
    linhas.append(r[0] if isinstance(r, list) else r)

# o resumo troca a fita para 2 rolos
payload = [{'id': l['id'], 'inventory_id': l['inventory_id'], 'stock_id': loc, 'quantity': (2 if l['quantity'] == 1 else l['quantity']), 'notes': l.get('notes')} for l in linhas]
st, res = req('POST', '/rest/v1/rpc/commit_os_material_consumption', {'p_service_order_id': OS, 'p_lines': payload}, tok)
confere(st == 200 and len(res['committed']) == 2 and not res['warnings'], f'commit_os_material_consumption -> {st} {json.dumps(res)[:140]}')
st, mats = req('GET', '/rest/v1/inventory?select=name,quantity&order=name', None, tok)
saldos = {m['name']: m['quantity'] for m in mats}
confere(saldos['Limpa-evaporador em spray'] == 10 and saldos['Fita isolante'] == 28 and saldos['Gás refrigerante R-410A'] == 8.5, f'saldos {saldos}')
st, movs = req('GET', '/rest/v1/inventory_movements?select=movement_type,quantity,stock_before,stock_after,notes,created_by,service_order_id&order=created_at', None, tok)
print('   movimentos:', [(m['movement_type'], m['quantity'], m['stock_before'], m['stock_after'], m['notes']) for m in movs])
confere(len(movs) == 2 and all(m['movement_type'] == 'consumo' and m['quantity'] < 0 for m in movs), 'duas saídas de consumo')
# segunda chamada idêntica: nada novo (delta 0)
st, res2 = req('POST', '/rest/v1/rpc/commit_os_material_consumption', {'p_service_order_id': OS, 'p_lines': payload}, tok)
confere(st == 200 and res2['committed'] == [], 'repetir a baixa não mexe no saldo')

# link público
req('PATCH', f'/rest/v1/service_orders?id=eq.{OS}', {'status': 'concluida'}, tok)
st, pub = req('POST', '/rest/v1/rpc/get_public_os', {'p_os_id': OS})
chaves = sorted(pub.keys()) if isinstance(pub, dict) else pub
confere(st == 200 and isinstance(pub, dict) and pub['service_order']['status'] == 'concluida' and pub['customer']['name'] == 'Colégio Monte Verde',
        f'get_public_os -> {len(chaves)} chaves')
confere(len(pub.get('nps_criteria', [])) == 3 and pub['equipment_items'][0]['form_template']['name'] == 'Manutenção preventiva de split', 'critérios do NPS e equipamento com checklist')
st, pub2 = req('POST', '/rest/v1/rpc/get_public_os_by_code', {'p_code': cad['public_short_code']})
confere(st == 200 and pub2 and pub2['service_order']['id'] == OS, 'get_public_os_by_code')
st, pos = req('POST', '/rest/v1/rpc/get_public_os_technician_location', {'p_os_id': OS})
confere(st == 200 and pos is None, 'sem ponto de localização: null')

# avaliação
st, ratings = req('GET', f'/rest/v1/service_ratings?service_order_id=eq.{OS}&select=id,rated_at', None, tok)
if not ratings:
    req('POST', '/rest/v1/service_ratings', {'service_order_id': OS}, tok)
crit = pub['nps_criteria']
st, ok = req('POST', '/rest/v1/rpc/submit_public_os_rating', {'p_os_id': OS, 'p_nps': 10, 'p_comment': 'Atendimento pontual e muito organizado. Obrigada!',
                                                              'p_name': 'Helena Barros', 'p_criteria': [{'criterion_id': c['id'], 'value': 5} for c in crit]})
confere(st == 200 and ok == {'success': True}, f'submit_public_os_rating -> {st} {ok}')
st, nota = req('GET', f'/rest/v1/service_ratings?service_order_id=eq.{OS}&select=nps_score,rated_by_name,quality_rating,rated_at,service_rating_criteria(label_snapshot,value)', None, tok)
print('   avaliação:', json.dumps(nota, ensure_ascii=False)[:260])
confere(nota and nota[0]['nps_score'] == 10 and len(nota[0].get('service_rating_criteria') or []) == 3, 'nota 10 e três critérios com 5 estrelas')
st, dup = req('POST', '/rest/v1/rpc/submit_public_os_rating', {'p_os_id': OS, 'p_nps': 9, 'p_criteria': []})
confere(st >= 400, f'segunda avaliação recusada ({st})')

print('\n' + ('TUDO CERTO' if not erros else f'{len(erros)} PROBLEMA(S): {erros}'))
sys.exit(1 if erros else 0)
