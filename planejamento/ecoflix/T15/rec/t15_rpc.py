#!/usr/bin/env python3
"""T15: consulta as RPCs do relatório na MINHA instância (54315), com o estado de partida de um capítulo. Só leitura do mundo.
Uso: python3 -I rec/t15/t15_rpc.py [--seed t15/apos-cap01 ...] [--sem-reset] rpc '{"p_x": 1}' [rpc2 '{...}']"""
import base64, hashlib, json, sys, urllib.request
URL = 'http://127.0.0.1:54315'
T14 = ['t14/inicio'] + [f't14/apos-cap{n:02d}' for n in (2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 14)]


def sid(k):
    h = bytearray(hashlib.sha1(('domiflix-fake:' + k).encode()).digest()); h[6] = (h[6] & 0x0F) | 0x50; h[8] = (h[8] & 0x3F) | 0x80
    x = h[:16].hex(); return f'{x[:8]}-{x[8:12]}-{x[12:16]}-{x[16:20]}-{x[20:32]}'


def b64(d):
    return base64.urlsafe_b64encode(json.dumps(d).encode()).decode().rstrip('=')


TOK = b64({'alg': 'none'}) + '.' + b64({'role': 'authenticated', 'sub': sid('user.rafael'), 'email': 'rafael@reciclavalemetais.example'}) + '.x'
ANON = json.load(open('/home/claude/ecoflix/rec/mundo/mundo.json'))['env']['anonKey']
CID = sid('company.reciclavale')


def post(path, body):
    r = urllib.request.Request(URL + path, data=json.dumps(body).encode(), method='POST',
                               headers={'content-type': 'application/json', 'apikey': ANON, 'Authorization': 'Bearer ' + TOK})
    return json.load(urllib.request.urlopen(r))


def main():
    a = sys.argv[1:]
    seeds = list(T14) + ['t15/inicio']
    while a and a[0].startswith('--'):
        if a[0] == '--seed':
            seeds.append(a[1]); a = a[2:]
        elif a[0] == '--sem-reset':
            seeds = None; a = a[1:]
        else:
            a = a[1:]
    if seeds is not None:
        post('/__dev/reset', {}); post('/__dev/seed', {'files': seeds})
    while a:
        nome, arg = a[0], json.loads(a[1]) if len(a) > 1 else {}
        arg.setdefault('p_company_id', CID)
        print(f'== {nome}'); print(json.dumps(post(f'/rest/v1/rpc/{nome}', arg), ensure_ascii=False)[:6000])
        a = a[2:]


if __name__ == '__main__':
    main()
