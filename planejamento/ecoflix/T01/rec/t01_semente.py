#!/usr/bin/env python3
"""T1 · grava rec/mundo/seeds-extra/t01/apos-capNN.json a partir do estado da instância do Supabase falso logo depois do ensaio do
capítulo NN (o que o robô digitou na tela), como diferença contra o estado de partida do capítulo (as sementes do roteiro).
Rodar DENTRO da mesma trava da gravação, logo depois dela (a instância é só desta aula; o próximo ensaio a reinicia):
    FAKE_URL=http://127.0.0.1:54301 python3 -I rec/t01/t01_semente.py 05
1) lê o estado final (companies, profiles, company_fiscal_config, payment_conditions); 2) reinicia a instância e aplica as sementes
do capítulo (o `seedExtra` de rec/t01/capNN.json); 3) grava a diferença. O logo e o ícone que o app enviou viram os arquivos do mundo
(rec/mundo/storage/avatars/recicla-vale-*.png, token @storage:), porque o upload do ensaio vive só na memória da instância."""
import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.normpath(os.path.join(HERE, '..', 'mundo', 'seeds-extra', 't01'))
URL = os.environ.get('FAKE_URL', 'http://127.0.0.1:54301').rstrip('/')
IGNORA = {'updated_at', 'created_at', 'last_activity', 'last_login_at', 'last_seen_at'}
ARQ = {'logo_url': '@storage:avatars/recicla-vale-logo.png', 'icon_url': '@storage:avatars/recicla-vale-icone.png'}
EMPRESA, RAFAEL = '@id:company.reciclavale', '@id:user.rafael'


def pega(tabela):
    with urllib.request.urlopen(f'{URL}/__dev/state?table={tabela}', timeout=20) as r:
        return json.load(r)


def posta(rota, corpo=None):
    req = urllib.request.Request(f'{URL}{rota}', data=json.dumps(corpo or {}).encode(), method='POST', headers={'content-type': 'application/json'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def main():
    n = int(sys.argv[1])
    roteiro = json.load(open(os.path.join(HERE, f'cap{n:02d}.json'), encoding='utf8'))
    tabelas = ['companies', 'profiles', 'company_fiscal_config', 'payment_conditions']
    fim = {t: pega(t) for t in tabelas}
    posta('/__dev/reset')
    if roteiro.get('seedExtra'):
        posta('/__dev/seed', {'files': roteiro['seedExtra']})
    ini = {t: pega(t) for t in tabelas}
    empresa_id = fim['companies'][0]['id']
    rafael_id = next(p['id'] for p in fim['profiles'] if p.get('email') == 'rafael@reciclavalemetais.example')
    patch, novas = {}, {}

    def dif(a, b):
        return {k: v for k, v in b.items() if k not in IGNORA and a.get(k) != v}

    c0 = next(c for c in ini['companies'] if c['id'] == empresa_id)
    c1 = next(c for c in fim['companies'] if c['id'] == empresa_id)
    d = dif(c0, c1)
    for k in ARQ:
        if k in d and d[k]:
            d[k] = ARQ[k]
    if d:
        patch['companies'] = [{'match': {'id': EMPRESA}, 'set': d}]
    p0 = next(p for p in ini['profiles'] if p['id'] == rafael_id)
    p1 = next(p for p in fim['profiles'] if p['id'] == rafael_id)
    d = dif(p0, p1)
    if d:
        patch['profiles'] = [{'match': {'id': RAFAEL}, 'set': d}]
    for t in ('company_fiscal_config', 'payment_conditions'):
        ids0 = {r['id'] for r in ini[t]}
        for r in fim[t]:
            if r['id'] not in ids0:
                linha = {k: v for k, v in r.items() if k not in IGNORA}
                linha['company_id'] = EMPRESA
                novas.setdefault(t, []).append(linha)
            else:
                r0 = next(x for x in ini[t] if x['id'] == r['id'])
                dd = dif(r0, r)
                if dd:
                    patch.setdefault(t, []).append({'match': {'id': r['id']}, 'set': dd})
    out = {'_doc': f'T1 (Sua conta e sua empresa), estado depois do cap{n:02d} (gerado por rec/t01/t01_semente.py a partir do ensaio: o que o robô '
                   f'digitou na tela), por cima de {", ".join(roteiro.get("seedExtra") or [])}.'}
    out.update(novas)
    if patch:
        out['_patch'] = patch
    os.makedirs(SAIDA, exist_ok=True)
    caminho = os.path.join(SAIDA, f'apos-cap{n:02d}.json')
    json.dump(out, open(caminho, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print(f'{os.path.relpath(caminho, os.path.join(HERE, "..", ".."))}: ' + json.dumps({k: (v if k == '_patch' else len(v)) for k, v in out.items() if k != '_doc'}, ensure_ascii=False)[:900])


if __name__ == '__main__':
    main()
