#!/usr/bin/env python3
"""T7 · garante que a foto do checklist (cap05) exista no armazenamento falso antes de gravar um capítulo que parte de um estado com ela
(cap06 em diante). O bucket `os-photos` do falso vive na memória do processo: se o falso reiniciou desde a gravação do cap05, o app
mostraria o marcador cinza no lugar da foto. Uso: python3 -I rec/t7/fotos.py NN   (sem efeito antes do cap06 ou sem apos-cap05)."""
import json, os, re, sys, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
FAKE = os.environ.get('FAKE_URL', 'http://127.0.0.1:54321')
n = int(sys.argv[1]) if len(sys.argv) > 1 else 99
seed = os.path.join(HERE, '..', 'fakebase', 'seeds-extra', 't7', 'apos-cap05.json')
foto = os.path.join(HERE, 'assets', 'foto-equipamento.jpg')
if n < 6 or not os.path.exists(seed):
    sys.exit(0)
KEY = json.load(open(os.path.join(HERE, '..', 'env.json')))['anonKey']
urls = set(re.findall(r'/storage/v1/object/(?:public/)?(os-photos/[^"\s]+)', open(seed, encoding='utf8').read()))
if not urls:
    print('fotos: apos-cap05 sem foto de checklist')
    sys.exit(0)
dados = open(foto, 'rb').read()
for u in sorted(urls):
    alvo = f'{FAKE}/storage/v1/object/public/{u}'
    try:
        r = urllib.request.urlopen(urllib.request.Request(alvo, headers={'apikey': KEY}), timeout=8)
        if r.headers.get('content-type', '').startswith('image/jpeg'):
            print(f'fotos: {u} já está no armazenamento')
            continue
    except urllib.error.URLError:
        pass
    req = urllib.request.Request(f'{FAKE}/storage/v1/object/{u}', data=dados, method='POST',
                                 headers={'apikey': KEY, 'authorization': 'Bearer ' + KEY, 'content-type': 'image/jpeg'})
    urllib.request.urlopen(req, timeout=15).read()
    print(f'fotos: {u} enviada de novo ({len(dados)} bytes)')
