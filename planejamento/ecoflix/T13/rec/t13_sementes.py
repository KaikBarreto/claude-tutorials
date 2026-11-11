#!/usr/bin/env python3
"""T13 · sementes extras em rec/mundo/seeds-extra/t13/ e o PDF fictício do cap11.

  python3 -I rec/t13/t13_sementes.py inicio
      escreve t13/inicio.json (à mão, abaixo): o que a aula precisa e o mundo base não traz.
  python3 -I rec/t13/t13_sementes.py pdf
      escreve rec/t13/assets/comprovante-pix-energia-outubro.pdf (uma página, texto fictício, sem marca de banco).
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
        '_doc': ('T13 · estado de partida (caps 0 a 4) por cima do mundo base B: (1) o fornecedor "Hidráulica Moretti Ltda" (plano da T13, '
                 'manutenção da prensa; CNPJ 41.739.625/0001-57 com dígito válido), que a aula escolhe no cap04; (2) `paid_at` do "Aluguel do '
                 'galpão de novembro" como DATA (a coluna é `date`, migração 20260925200000; o app corta "aaaa-mm-dd" em BillsList.formatPaidAt e '
                 'a semente de B grava o carimbo inteiro, que sairia "05T12:00:00.000Z/11/2026" em "Quitada em"). Gerado por rec/t13/t13_sementes.py.'),
        'suppliers': [{
            'id': '@id:fornecedor.moretti', 'company_id': EMP, 'code': '6', 'name': 'Hidráulica Moretti Ltda', 'nome_fantasia': None,
            'razao_social': 'Hidráulica Moretti Ltda', 'cpf_cnpj': '41.739.625/0001-57', 'phone': '(12) 90000-3131', 'phone_unavailable': False,
            'email': 'contato@hidraulicamoretti.example', 'contact_name': None, 'address': None, 'logradouro': None, 'numero': None,
            'bairro': None, 'cep': None, 'cidade': 'Taubaté', 'uf': 'SP', 'codigo_ibge': '3554102', 'pix_key': None, 'is_mei': False,
            'indicador_ie': 9, 'inscricao_estadual': None, 'linked_customer_id': None, 'is_industry': False, 'default_price_table_id': None,
            'created_by': '@id:user.rafael', 'created_at': '2026-11-06T17:20:00.000Z', 'updated_at': '2026-11-06T17:20:00.000Z',
        }],
        '_patch': {
            'financial_bills': [{'match': {'id': '@id:titulo.aluguel_nov'}, 'set': {'paid_at': '2026-11-05'}}],
        },
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
    return d


if __name__ == '__main__':
    os.makedirs(SAIDA, exist_ok=True)
    if sys.argv[1:2] == ['pdf']:
        pdf()
        sys.exit(0)
    if sys.argv[1:2] == ['inicio']:
        nome, d = 'inicio', inicio()
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
