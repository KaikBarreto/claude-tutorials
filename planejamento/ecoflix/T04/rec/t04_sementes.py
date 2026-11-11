#!/usr/bin/env python3
"""T04 · sementes extras em rec/mundo/seeds-extra/t04/.

  python3 -I rec/t04/t04_sementes.py inicio
      escreve t04/inicio.json (à mão, abaixo): o que a aula precisa e o mundo base não traz.
  python3 -I rec/t04/t04_sementes.py captura NN [--porta 54304]
      logo DEPOIS de um ensaio (ou gravação) do capítulo NN com 0 passo falho, lê a instância do Supabase falso (o estado que o robô
      deixou) e escreve t04/apos-capNN.json: as linhas criadas na aula (created_at >= FAKE_NOW) e, como _patch, as linhas do mundo que
      a aula alterou (updated_at >= FAKE_NOW). Cumulativo: o capítulo seguinte parte de ["t04/inicio", "t04/apos-capNN"].
Nada de credencial: a chave anônima do mundo.json (pública, do build falso) e nenhum dado real.
"""
import hashlib
import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
TUT_HOME = os.path.normpath(os.path.join(HERE, '..', '..'))
MUNDO = os.path.join(TUT_HOME, 'rec', 'mundo')
SAIDA = os.path.join(MUNDO, 'seeds-extra', 't04')
FAKE_NOW_Z = '2026-11-10T11:30:00'   # 08:30 em Brasília
EMP = '@id:company.reciclavale'


def token(nome):
    """link do portal fictício e estável (32 hex), como o token que o app gera ao criar o cadastro com o módulo de portal"""
    return hashlib.sha1(('t04-portal:' + nome).encode()).hexdigest()[:32]


FORNECEDORES = ['Valdir Pereira', 'Aparecida Ramos', 'Depósito Irmãos Siqueira', 'Auto Peças Vale Forte', 'Cooperativa Recomeço']
CLIENTES = ['Aços Quiririm Ltda', 'Fundição Bandeira do Vale', 'Serra Fina Alumínio Reciclagem', 'Depósito Irmãos Siqueira']


def inicio():
    d = {
        '_doc': ('T04 · estado de partida (caps 0 a 2) por cima do mundo base B: (1) "Cida Ramos", cadastro repetido da Aparecida Ramos '
                 '(mesmo telefone, sem documento nem endereço): as duas ganham o selo "Mesmo telefone" (cap01) e ela fica "Incompleto" '
                 '(cap04); (2) link do portal (portal_token) em todos os parceiros (a ficha da Cooperativa mostra "Acesso ao portal", '
                 'cap07); (3) Depósito Irmãos Siqueira na tabela padrão (a T4 liga a "Tabela Depósitos" na tela, cap06; a junção, seção 4, '
                 'já deixa B assim: o _patch só garante). Gerado por rec/t04/t04_sementes.py.'),
        'suppliers': [{
            'id': '@id:supplier.cida-ramos', 'company_id': EMP, 'code': '6', 'name': 'Cida Ramos', 'nome_fantasia': None,
            'razao_social': None, 'cpf_cnpj': None, 'phone': '(12) 90000-1201', 'phone_unavailable': False, 'email': None,
            'contact_name': None, 'pix_key': None, 'address': None, 'logradouro': None, 'numero': None, 'bairro': None,
            'complemento': None, 'cep': None, 'cidade': None, 'uf': None, 'codigo_ibge': None, 'indicador_ie': 9,
            'inscricao_estadual': None, 'regime_tributario': None, 'is_mei': False, 'default_price_table_id': None,
            'linked_customer_id': None, 'label_id': None, 'custom_fields': {}, 'portal_config': {}, 'portal_receipt_format': 'auto',
            'portal_token': token('Cida Ramos'), 'show_address_in_docs': True, 'show_bank_in_docs': True,
            'show_cpf_cnpj_in_docs': True, 'show_phone_in_docs': True, 'show_pix_in_docs': True,
            'created_by': '@id:user.rafael', 'created_at': '2026-09-18T12:40:00.000Z', 'updated_at': '2026-09-18T12:40:00.000Z',
        }],
        '_patch': {
            'suppliers': [{'match': {'name': n}, 'set': {'portal_token': token('f:' + n)}} for n in FORNECEDORES]
            + [{'match': {'name': 'Depósito Irmãos Siqueira'}, 'set': {'default_price_table_id': None}}],
            'customers': [{'match': {'name': n}, 'set': {'portal_token': token('c:' + n)}} for n in CLIENTES]
            + [{'match': {'name': 'Depósito Irmãos Siqueira'}, 'set': {'default_price_table_id': None}}],
        },
    }
    return d


def _get(porta, caminho):
    chave = json.load(open(os.path.join(MUNDO, 'mundo.json'), encoding='utf8'))['env']['anonKey']
    req = urllib.request.Request(f'http://127.0.0.1:{porta}/rest/v1/{caminho}', headers={'apikey': chave, 'Authorization': f'Bearer {chave}'})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode('utf8'))


def captura(nn, porta):
    schema = json.load(open(os.path.join(MUNDO, 'schema.json'), encoding='utf8'))['tables']
    novas, patch = {}, {}
    for tab, info in sorted(schema.items()):
        cols = info.get('columns') or info
        if not isinstance(cols, dict) or 'id' not in cols:
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
    d = {'_doc': f'T04 · estado depois do cap{nn:02d} (cumulativo sobre t04/inicio), capturado do Supabase falso logo depois do ensaio '
                 f'do capítulo (o que o app gravou). Gerado por rec/t04/t04_sementes.py captura {nn}.'}
    d.update(novas)
    if patch:
        d['_patch'] = patch
    return d


if __name__ == '__main__':
    os.makedirs(SAIDA, exist_ok=True)
    if sys.argv[1:2] == ['inicio']:
        nome, d = 'inicio', inicio()
    elif sys.argv[1:2] == ['captura']:
        nn = int(sys.argv[2])
        porta = int(sys.argv[sys.argv.index('--porta') + 1]) if '--porta' in sys.argv else 54304
        nome, d = f'apos-cap{nn:02d}', captura(nn, porta)
    else:
        sys.exit(__doc__)
    caminho = os.path.join(SAIDA, f'{nome}.json')
    json.dump(d, open(caminho, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    resumo = {k: len(v) for k, v in d.items() if isinstance(v, list)}
    if '_patch' in d:
        resumo['_patch'] = {k: len(v) for k, v in d['_patch'].items()}
    print(f't04/{nome}: {resumo}')
