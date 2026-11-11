#!/usr/bin/env python3
"""T13 · sementes extras em rec/mundo/seeds-extra/t13/ e o PDF fictício do cap11.

  python3 -I rec/t13/t13_sementes.py inicio
      escreve t13/inicio.json (à mão, abaixo): o que a aula precisa e o mundo base não traz.
  python3 -I rec/t13/t13_sementes.py pdf
      escreve rec/t13/assets/comprovante-pix-energia-outubro.pdf (uma página, texto fictício, sem marca de banco).
  python3 -I rec/t13/t13_sementes.py api NN [--porta 54313]      (NN = 7 a 11)
      o mesmo apos-capNN sem navegador: as chamadas do app pela API do falso (logado como o Rafael) e a captura abaixo.
  python3 -I rec/t13/t13_sementes.py captura NN [--porta 54313]
      logo DEPOIS de um ensaio (ou gravação) do capítulo NN com 0 passo falho, lê a instância do Supabase falso (o estado que o robô
      deixou) e escreve t13/apos-capNN.json: as linhas criadas na aula (created_at >= FAKE_NOW) e, como _patch, as linhas do mundo que
      a aula alterou (updated_at >= FAKE_NOW). Cumulativo: o capítulo seguinte parte de ["t13/inicio", "t13/apos-capNN"].
Molde: rec/t04/t04_sementes.py. Nada de credencial: a chave anônima do mundo.json (pública, do build falso) e nenhum dado real.
"""
import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
TUT_HOME = os.path.normpath(os.path.join(HERE, '..', '..'))
MUNDO = os.path.join(TUT_HOME, 'rec', 'mundo')
SAIDA = os.path.join(MUNDO, 'seeds-extra', 't13')
FAKE_NOW_Z = '2026-11-10T11:30:00'   # 08:30 em Brasília
EMP = '@id:company.reciclavale'
PDF = os.path.join(HERE, 'assets', 'comprovante-pix-energia-outubro.pdf')


def inicio():
    return {
        '_doc': ('T13 · estado de partida (caps 0 a 4) por cima do mundo base B: o fornecedor "Hidráulica Moretti Ltda" (plano da T13, '
                 'manutenção da prensa; CNPJ 41.739.625/0001-57 com dígito válido), que a aula escolhe no cap04. Gerado por rec/t13/t13_sementes.py.'),
        'suppliers': [{
            'id': '@id:fornecedor.moretti', 'company_id': EMP, 'code': '6', 'name': 'Hidráulica Moretti Ltda', 'nome_fantasia': None,
            'razao_social': 'Hidráulica Moretti Ltda', 'cpf_cnpj': '41.739.625/0001-57', 'phone': '(12) 90000-3131', 'phone_unavailable': False,
            'email': 'contato@hidraulicamoretti.example', 'contact_name': None, 'address': None, 'logradouro': None, 'numero': None,
            'bairro': None, 'cep': None, 'cidade': 'Taubaté', 'uf': 'SP', 'codigo_ibge': '3554102', 'pix_key': None, 'is_mei': False,
            'indicador_ie': 9, 'inscricao_estadual': None, 'linked_customer_id': None, 'is_industry': False, 'default_price_table_id': None,
            'created_by': '@id:user.rafael', 'created_at': '2026-11-06T17:20:00.000Z', 'updated_at': '2026-11-06T17:20:00.000Z',
        }],
    }


def pdf():
    """PDF mínimo de uma página (Helvetica), escrito à mão: só texto fictício."""
    linhas = ['Comprovante de transferencia Pix (documento ficticio, tutorial EcoFlix)', '',
              'Pagador: Recicla Vale Metais Ltda - Conta Principal', 'Referente: Energia eletrica de outubro',
              'Valor: R$ 1.874,30', 'Data: 10/11/2026']
    corpo = 'BT /F1 13 Tf 56 760 Td 18 TL ' + ' '.join(f'({t}) Tj T*' for t in linhas) + ' ET'
    objs = ['<< /Type /Catalog /Pages 2 0 R >>', '<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
            '<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>',
            '<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>', f'<< /Length {len(corpo)} >>\nstream\n{corpo}\nendstream']
    out, offs = b'%PDF-1.4\n', []
    for i, o in enumerate(objs, 1):
        offs.append(len(out))
        out += f'{i} 0 obj\n{o}\nendobj\n'.encode('latin-1')
    xref = len(out)
    out += f'xref\n0 {len(objs) + 1}\n0000000000 65535 f \n'.encode() + b''.join(f'{o:010d} 00000 n \n'.encode() for o in offs)
    out += f'trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n'.encode()
    os.makedirs(os.path.dirname(PDF), exist_ok=True)
    open(PDF, 'wb').write(out)
    print(f'{os.path.relpath(PDF, TUT_HOME)}: {len(out)} bytes')


def _get(porta, caminho):
    chave = json.load(open(os.path.join(MUNDO, 'mundo.json'), encoding='utf8'))['env']['anonKey']
    req = urllib.request.Request(f'http://127.0.0.1:{porta}/rest/v1/{caminho}', headers={'apikey': chave, 'Authorization': f'Bearer {chave}'})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode('utf8'))


def _post(porta, caminho, corpo):
    req = urllib.request.Request(f'http://127.0.0.1:{porta}{caminho}', data=json.dumps(corpo).encode(), method='POST',
                                 headers={'content-type': 'application/json'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


IGNORA = {'active_sessions', 'usage_events'}   # sessão e telemetria do próprio login do robô: não são estado da aula


def captura(nn, porta):
    schema = json.load(open(os.path.join(MUNDO, 'schema.json'), encoding='utf8'))['tables']
    novas, patch = {}, {}
    for tab, info in sorted(schema.items()):
        cols = info.get('columns') or info
        if not isinstance(cols, dict) or 'id' not in cols or tab in IGNORA:
            continue
        if 'created_at' in cols:
            try:
                rows = _get(porta, f'{tab}?select=*&created_at=gte.{FAKE_NOW_Z}')
            except Exception:
                rows = []
            if rows:
                novas[tab] = rows
        if 'updated_at' in cols and 'created_at' in cols:
            try:
                rows = _get(porta, f'{tab}?select=*&updated_at=gte.{FAKE_NOW_Z}&created_at=lt.{FAKE_NOW_Z}')
            except Exception:
                rows = []
            if rows:
                patch[tab] = [{'match': {'id': r['id']}, 'set': {k: v for k, v in r.items() if k not in ('id', 'created_at')}} for r in rows]
    # o instante antes do 1º capítulo da cadeia (mundo base + t13/inicio): linha "nova" que já existe ali é do mundo (created_at na
    # hora da carga, ex. subscription_plans) e sai; o _patch fica só com os campos que a aula mudou
    _post(porta, '/__dev/reset', {})
    _post(porta, '/__dev/seed', {'files': ['t13/inicio']})
    for tab in list(novas):
        ids = ','.join(r['id'] for r in novas[tab])
        ja = {r['id'] for r in _get(porta, f'{tab}?select=id&id=in.({ids})')}
        novas[tab] = [r for r in novas[tab] if r['id'] not in ja]
        if not novas[tab]:
            del novas[tab]
    if patch:
        for tab, itens in list(patch.items()):
            novos = []
            for it in itens:
                antes = _get(porta, f"{tab}?select=*&id=eq.{it['match']['id']}")
                antes = antes[0] if antes else {}
                mud = {k: v for k, v in it['set'].items() if antes.get(k) != v}
                if mud:
                    novos.append({'match': it['match'], 'set': mud})
            if novos:
                patch[tab] = novos
            else:
                del patch[tab]
    d = {'_doc': f'T13 · estado depois do cap{nn:02d} (cumulativo sobre t13/inicio), capturado do Supabase falso logo depois do ensaio '
                 f'do capítulo (o que o app gravou). Gerado por rec/t13/t13_sementes.py captura {nn}.'}
    d.update(novas)
    if patch:
        d['_patch'] = patch
    return saldos_bancos(d, porta)


def saldos_bancos(d, porta):
    """o saldo gravado em bank_accounts (que o falso recalcula ao lançar, mas a carga de sementes não): saldo do mundo base + os lançamentos
    da semente, como _patch. A instância fica no estado "antes" (mundo base + t13/inicio)."""
    _post(porta, '/__dev/reset', {})
    _post(porta, '/__dev/seed', {'files': ['t13/inicio']})
    base = {r['id']: r['balance'] for r in _get(porta, 'bank_accounts?select=id,balance')}
    soma = {}
    for t in d.get('bank_transactions', []):
        soma[t['bank_account_id']] = soma.get(t['bank_account_id'], 0) + float(t['amount'])
    pt = [{'match': {'id': k}, 'set': {'balance': round(float(base[k]) + v, 2)}} for k, v in soma.items() if k in base and abs(v) > 0.001]
    d.setdefault('_patch', {}).pop('bank_accounts', None)
    if pt:
        d['_patch']['bank_accounts'] = pt
    elif not d['_patch']:
        del d['_patch']
    return d


def stable_id(chave):
    """o mesmo UUID do `@id:<chave>` das sementes (rec/fakebase/core/util.mjs, stableId)"""
    import hashlib
    h = bytearray(hashlib.sha1(('domiflix-fake:' + chave).encode()).digest())
    h[6] = (h[6] & 0x0F) | 0x50
    h[8] = (h[8] & 0x3F) | 0x80
    x = h[:16].hex()
    return f'{x[:8]}-{x[8:12]}-{x[12:16]}-{x[16:20]}-{x[20:32]}'


def _req(porta, metodo, caminho, corpo=None, token=None, extra=None):
    chave = json.load(open(os.path.join(MUNDO, 'mundo.json'), encoding='utf8'))['env']['anonKey']
    h = {'apikey': chave, 'Authorization': f'Bearer {token or chave}', 'content-type': 'application/json', **(extra or {})}
    data = json.dumps(corpo).encode() if corpo is not None else None
    req = urllib.request.Request(f'http://127.0.0.1:{porta}{caminho}', data=data, method=metodo, headers=h)
    with urllib.request.urlopen(req, timeout=30) as r:
        t = r.read().decode('utf8')
        return json.loads(t) if t else None


def api(nn, porta):
    """apos-capNN SEM navegador: parte de t13/inicio + apos-cap(NN-1) e faz, pela API do Supabase falso e logado como o Rafael, as
    MESMAS chamadas que o app faz no capítulo (hooks/useBills.ts, useTransactionAttachments.ts); depois captura como o `captura`.
    Serve para os capítulos da cadeia não esperarem um pelo outro na fila da trava; a gravação de cada capítulo confere a tela."""
    import secrets
    _post(porta, '/__dev/reset', {})
    _post(porta, '/__dev/seed', {'files': ['t13/inicio', f't13/apos-cap{nn - 1:02d}']})
    tok = _req(porta, 'POST', '/auth/v1/token?grant_type=password',
               {'email': 'rafael@reciclavalemetais.example', 'password': secrets.token_hex(8)})['access_token']   # o falso aceita qualquer senha
    rpc = lambda nome, args: _req(porta, 'POST', f'/rest/v1/rpc/{nome}', args, tok)
    get = lambda q: _req(porta, 'GET', f'/rest/v1/{q}', None, tok)
    patch = lambda q, corpo: _req(porta, 'PATCH', f'/rest/v1/{q}', corpo, tok, {'Prefer': 'return=representation'})
    post = lambda q, corpo: _req(porta, 'POST', f'/rest/v1/{q}', corpo, tok, {'Prefer': 'return=representation'})
    principal, aluguel = stable_id('banco.principal'), stable_id('categoria.aluguel')
    pagar = lambda bill, valor, resto=None: rpc('pay_financial_bill', {
        'p_bill_id': bill, 'p_amount': valor, 'p_payment_method': 'transfer', 'p_bank_account_id': principal, 'p_cash_register_id': None,
        'p_paid_date': '2026-11-10', 'p_fee_amount': 0, 'p_remainder_due_date': resto, 'p_notes': None, 'p_interest_amount': 0,
        'p_interest_category_id': None, 'p_tenders': None})
    if nn == 7:      # Repetir: aluguel da empilhadeira, mensal, 12/11/2026 até 12/04/2027 (sem previsto, sem parceiro)
        rpc('create_recurring_bill_template', {
            'p_client_request_id': stable_id('t13.cap07.aluguel-empilhadeira'), 'p_direction': 'payable', 'p_description': 'Aluguel da empilhadeira',
            'p_category_id': aluguel, 'p_amount': 2300, 'p_partner_type': None, 'p_partner_id': None, 'p_notes': None, 'p_frequency': 'monthly',
            'p_interval': 1, 'p_start_date': '2026-11-12', 'p_end_date': '2027-04-12', 'p_expected_payment_method': None,
            'p_expected_bank_account_id': None})
    elif nn == 8:    # Esta e as futuras a partir da de 12/12: molde + futuras não pagas (mesmos dados) e o deslocamento de +3 dias
        t = get('recurring_bill_templates?select=id&description=eq.Aluguel%20da%20empilhadeira')[0]['id']
        dados = {'description': 'Aluguel da empilhadeira', 'amount': 2300, 'category_id': aluguel, 'notes': None, 'direction': 'payable',
                 'partner_type': None, 'partner_id': None}
        patch(f'recurring_bill_templates?id=eq.{t}', dados)
        patch(f'financial_bills?recurring_template_id=eq.{t}&due_date=gte.2026-12-12&status=neq.paid', dados)
        rpc('shift_recurring_bills_due_date', {'p_template_id': t, 'p_from_due_date': '2026-12-12', 'p_new_due_date': '2026-12-15'})
    elif nn == 9:    # baixa da energia inteira e da prensa em parte (o resto para 30/11), Pix da Conta Principal
        pagar(stable_id('titulo.energia_out'), 1874.3)
        prensa = get('financial_bills?select=id&description=eq.Manuten%C3%A7%C3%A3o%20da%20prensa%20enfardadeira')[0]['id']
        pagar(prensa, 1740, '2026-11-30')
    elif nn == 10:   # recebimento de 2.000,00 do saldo da Aços Quiririm, Pix na Conta Principal
        rpc('pay_partner_balance', {'p_entity_type': 'customer', 'p_entity_id': stable_id('cliente.quiririm'), 'p_amount': 2000,
                                    'p_payment_method': 'transfer', 'p_bank_account_id': principal, 'p_cash_register_id': None,
                                    'p_paid_date': '2026-11-10', 'p_category_id': None})
    elif nn == 11:   # comprovante na energia (a linha de transaction_attachments; o arquivo do storage do falso é de memória) e o Salvar
        energia, emp = stable_id('titulo.energia_out'), stable_id('company.reciclavale')
        nome = os.path.basename(PDF)
        post('transaction_attachments', {'company_id': emp, 'ref_type': 'financial_bill', 'ref_id': energia, 'file_name': nome,
                                          'storage_path': f'{emp}/financial_bill/{energia}/{stable_id("t13.cap11.pdf")}-{nome}',
                                          'mime_type': 'application/pdf', 'size_bytes': os.path.getsize(PDF), 'created_by': stable_id('user.rafael')})
        patch(f'financial_bills?id=eq.{energia}', {'description': 'Energia elétrica de outubro'})
    else:
        raise SystemExit(f'api: capítulo {nn} sem operações (só 7 a 11)')
    return captura(nn, porta)


if __name__ == '__main__':
    os.makedirs(SAIDA, exist_ok=True)
    if sys.argv[1:2] == ['pdf']:
        pdf()
        sys.exit(0)
    if sys.argv[1:2] == ['saldos']:   # acerta o saldo gravado das contas nas apos-capNN já capturadas: saldos NN [NN ...]
        for a_ in sys.argv[2:]:
            if a_.startswith('--'):
                break
            cam = os.path.join(SAIDA, f'apos-cap{int(a_):02d}.json')
            d = saldos_bancos(json.load(open(cam, encoding='utf8')), 54313)
            json.dump(d, open(cam, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
            print(f'apos-cap{int(a_):02d}: {d.get("_patch", {}).get("bank_accounts")}')
        sys.exit(0)
    if sys.argv[1:2] == ['inicio']:
        nome, d = 'inicio', inicio()
    elif sys.argv[1:2] == ['api']:
        nn = int(sys.argv[2])
        porta = int(sys.argv[sys.argv.index('--porta') + 1]) if '--porta' in sys.argv else 54313
        nome, d = f'apos-cap{nn:02d}', api(nn, porta)
    elif sys.argv[1:2] == ['captura']:
        nn = int(sys.argv[2])
        porta = int(sys.argv[sys.argv.index('--porta') + 1]) if '--porta' in sys.argv else 54313
        nome, d = f'apos-cap{nn:02d}', captura(nn, porta)
    else:
        sys.exit(__doc__)
    caminho = os.path.join(SAIDA, f'{nome}.json')
    json.dump(d, open(caminho, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    resumo = {k: len(v) for k, v in d.items() if isinstance(v, list)}
    if '_patch' in d:
        resumo['_patch'] = {k: len(v) for k, v in d['_patch'].items()}
    print(f't13/{nome}: {resumo}')
