#!/usr/bin/env python3
"""T25 · sementes extras em rec/mundo/seeds-extra/t25/.

  python3 -I rec/t25/t25_sementes.py inicio
      escreve t25/inicio.json: a Agenda da aula (plano.md, "Mundo"): tira as duas tarefas que o mundo base traz e põe as do roteiro
      (10/11 14:00 "Cotação do cobre com a Fundição Bandeira do Vale"; 11/11 08:00 "Coleta na Auto Peças Vale Forte", categoria Coleta).
  python3 -I rec/t25/t25_sementes.py captura NN [--porta 54325]
      logo DEPOIS de um ensaio do capítulo NN com 0 passo falho, lê a instância do Supabase falso e escreve t25/apos-capNN.json: as
      tarefas criadas na aula (created_at >= FAKE_NOW) e, em _patch, as que mudaram (updated_at >= FAKE_NOW). Cumulativo sobre
      CADEIA + t25/inicio. Só schedule_tasks: é a única tabela que a aula grava.
"""
import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
TUT_HOME = os.path.normpath(os.path.join(HERE, '..', '..'))
MUNDO = os.path.join(TUT_HOME, 'rec', 'mundo')
SAIDA = os.path.join(MUNDO, 'seeds-extra', 't25')
FAKE_NOW_Z = '2026-11-10T11:30:00'   # 08:30 em Brasília
EMP = '@id:company.reciclavale'
RAFAEL = '@id:user.rafael'
T14 = ['t14/inicio'] + [f't14/apos-cap{n:02d}' for n in (2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 14)]
T15 = ['t15/inicio', 't15/apos-cap01', 't15/apos-cap02', 't15/apos-cap10']
T13 = ['t13/inicio', 't13/apos-cap11']
CADEIA = T13 + T14 + T15 + ['t21/inicio', 't21/apos-cap02']   # o fim da T21, de onde a T25 parte (MUNDO_LINHA_DO_TEMPO, seção 14)


def tarefa(k, titulo, data, hora, categoria='tarefa', **extra):
    return {'id': f'@id:tarefa.{k}', 'company_id': EMP, 'title': titulo, 'scheduled_date': data, 'scheduled_time': hora,
            'category': categoria, 'status': 'pendente', 'priority': 'media', 'created_by': RAFAEL, 'assigned_to': RAFAEL,
            'created_at': '2026-11-06T12:00:00.000Z', 'updated_at': '2026-11-06T12:00:00.000Z', 'notify_on_day': True,
            'notify_minutes_before': 0, 'notify_push': False, **extra}


def inicio():
    return {
        '_doc': ('T25 · estado de partida: a Agenda do plano.md por cima do fim da T21. Tira "Carregamento Aços Quiririm" e "Buscar material '
                 'na Cooperativa Recomeço" (do mundo base) e põe a cotação do cobre (10/11 14:00) e a coleta na Auto Peças Vale Forte '
                 '(11/11 08:00). Gerado por rec/t25/t25_sementes.py.'),
        '_remove': {'schedule_tasks': [{'id': '@id:tarefa.quiririm'}, {'id': '@id:tarefa.cooperativa'}]},
        'schedule_tasks': [
            tarefa('cotacao_cobre', 'Cotação do cobre com a Fundição Bandeira do Vale', '2026-11-10', '14:00'),
            tarefa('coleta_valeforte', 'Coleta na Auto Peças Vale Forte', '2026-11-11', '08:00', 'coleta',
                   supplier_id='@id:fornecedor.valeforte', supplier_name='Auto Peças Vale Forte',
                   description='Retirar a chaparia e as baterias do dia.'),
        ],
    }


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


def captura(nn, porta):
    novas = _get(porta, f'schedule_tasks?select=*&created_at=gte.{FAKE_NOW_Z}')
    mudou = _get(porta, f'schedule_tasks?select=*&updated_at=gte.{FAKE_NOW_Z}&created_at=lt.{FAKE_NOW_Z}')
    # o que as sementes apos-cap anteriores já trouxeram (carregadas na instância com created_at da própria gravação) não se repete
    antes = set()
    for f in os.listdir(SAIDA):
        if f.startswith('apos-cap') and int(f[8:10]) < nn:
            antes |= {r['id'] for r in json.load(open(os.path.join(SAIDA, f), encoding='utf8')).get('schedule_tasks', [])}
    novas = [r for r in novas if r['id'] not in antes]
    ids_novas = {r['id'] for r in novas}
    mudou = [r for r in mudou if r['id'] not in ids_novas and r['id'] not in antes]
    d = {'_doc': f'T25 · estado depois do cap{nn:02d} (cumulativo sobre t25/inicio), capturado do Supabase falso logo depois do ensaio do '
                 f'capítulo (o que o app gravou). Gerado por rec/t25/t25_sementes.py captura {nn}.'}
    if novas:
        d['schedule_tasks'] = novas
    if mudou:
        d['_patch'] = {'schedule_tasks': [{'match': {'id': r['id']}, 'set': {k: v for k, v in r.items() if k not in ('id', 'created_at')}} for r in mudou]}
    return d


def _req(porta, metodo, caminho, corpo=None, token=None, extra=None):
    chave = json.load(open(os.path.join(MUNDO, 'mundo.json'), encoding='utf8'))['env']['anonKey']
    h = {'apikey': chave, 'Authorization': f'Bearer {token or chave}', 'content-type': 'application/json', **(extra or {})}
    req = urllib.request.Request(f'http://127.0.0.1:{porta}{caminho}', data=json.dumps(corpo).encode() if corpo is not None else None,
                                 method=metodo, headers=h)
    with urllib.request.urlopen(req, timeout=30) as r:
        t = r.read().decode('utf8')
        return json.loads(t) if t else None


def api(nn, porta):
    """apos-capNN SEM navegador (a gravação de cada capítulo confere a tela): parte de CADEIA + t25/inicio (+ apos-cap05) e faz, pela
    API do Supabase falso e logado como o Rafael, as MESMAS chamadas que o app faz (hooks/useScheduleTasks.tsx): o insert da Nova Tarefa
    e, no cap. 5, o update de scheduled_date do arrasto. Depois captura como o `captura`."""
    import secrets
    cadeia = CADEIA + ['t25/inicio'] + (['t25/apos-cap05'] if nn == 10 else [])
    _post(porta, '/__dev/reset', {})
    _post(porta, '/__dev/seed', {'files': cadeia})
    tok = _req(porta, 'POST', '/auth/v1/token?grant_type=password',
               {'email': 'rafael@reciclavalemetais.example', 'password': secrets.token_hex(8)})['access_token']   # o falso aceita qualquer senha
    emp = _get(porta, 'companies?select=id')[0]['id']
    rafael = _req(porta, 'GET', '/rest/v1/profiles?select=id&email=eq.rafael@reciclavalemetais.example', None, tok)[0]['id']
    post = lambda corpo: _req(porta, 'POST', '/rest/v1/schedule_tasks?select=*', corpo, tok, {'Prefer': 'return=representation'})
    patch = lambda q, corpo: _req(porta, 'PATCH', f'/rest/v1/schedule_tasks?{q}', corpo, tok, {'Prefer': 'return=representation'})
    if nn == 5:      # Nova Tarefa (12/11 09:00, Lembrar no dia) e o arrasto para o dia 13
        t = post({'title': 'Revisão do caminhão truck', 'category': 'tarefa', 'scheduled_date': '2026-11-12', 'scheduled_time': '09:00',
                  'notify_on_day': True, 'notify_push': False, 'company_id': emp, 'created_by': rafael})
        t = t[0] if isinstance(t, list) else t
        patch(f"id=eq.{t['id']}", {'scheduled_date': '2026-11-13'})
    elif nn == 10:   # Nova Tarefa: Fechamento de novembro (01/12 08:00, Lembrar no dia)
        post({'title': 'Fechamento de novembro', 'description': 'Conciliar o banco, conferir o DRE, mandar o pacote ao contador e ver MTR e CDF pendentes',
              'category': 'tarefa', 'scheduled_date': '2026-12-01', 'scheduled_time': '08:00', 'notify_on_day': True, 'notify_push': False,
              'company_id': emp, 'created_by': rafael})
    else:
        raise SystemExit('api: só os capítulos 5 e 10 gravam')
    return captura(nn, porta)


def main():
    a = sys.argv[1:]
    if not a:
        raise SystemExit(__doc__)
    os.makedirs(SAIDA, exist_ok=True)
    if a[0] == 'inicio':
        d, nome = inicio(), 'inicio.json'
    elif a[0] == 'api':
        nn = int(a[1])
        porta = int(a[a.index('--porta') + 1]) if '--porta' in a else 54325
        d, nome = api(nn, porta), f'apos-cap{nn:02d}.json'
    elif a[0] == 'captura':
        nn = int(a[1])
        porta = int(a[a.index('--porta') + 1]) if '--porta' in a else 54325
        d, nome = captura(nn, porta), f'apos-cap{nn:02d}.json'
    else:
        raise SystemExit(__doc__)
    with open(os.path.join(SAIDA, nome), 'w', encoding='utf8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    print(f'rec/mundo/seeds-extra/t25/{nome}: ' + ', '.join(f'{k}={len(v)}' for k, v in d.items() if isinstance(v, (list, dict))))


if __name__ == '__main__':
    main()
