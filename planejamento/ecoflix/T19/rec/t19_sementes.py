#!/usr/bin/env python3
"""T19 · escreve a semente de partida da aula (rec/mundo/seeds-extra/t19/inicio.json) e as selfies das batidas de hoje
(rec/mundo/storage/time-photos/...), a partir do plano (planejamento/ecoflix/T19/plano.md, "Mundo: o que esta aula precisa").

O que entra por cima do mundo base (B, 10/11/2026 08:30):
 - departamentos Escritório e Pátio; os 7 funcionários do plano (o Gabriel nasce no cap02, na tela);
 - movimentos: pagamento de 09/11 08:00 + "Reset para salário base" (Rafael, Juliana, Marcos, Cláudio, Diego); o do Rogério em
   30/10 17:00; o Edson com o ciclo de outubro (pagamento 07/10, ajuste de salário 13/10 no formato da tela de então, vales 15/10 e
   28/10, bônus 22/10);
 - ponto: time_settings (07:00-16:00, 60 min, tolerância 10, seg a sex, selfie e localização), o slug do tablet, batidas de 01/09 a
   09/11 do Marcos, Edson, Cláudio e Diego (menos Cláudio 05/11 e Diego 06/11) e as entradas de hoje (06:47, 06:52, 06:58, 07:03);
 - o caixa do Rafael aberto às 08:30 com R$ 1.500,00 (junção: B não tem caixa em 10/11); o cadastro fiscal em Lucro Real; a
   categoria "Folha salarial" de B com o nome que o app procura ("Folha Salarial", utils/payrollCategory.ts).
Determinístico: rodar de novo refaz os mesmos arquivos. Os slugs seguem o formato da 1.59.154 ({empresa}-{primeiro nome}-{12}),
com o código derivado do nome (o handler rpc/generate_ponto_slug.mjs usa a mesma conta: t19_slug abaixo).
Uso: python3 -I rec/t19/t19_sementes.py"""
import datetime as dt
import hashlib
import json
import os
import random

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
MUNDO = os.path.join(os.path.dirname(HERE), 'mundo')
SAIDA = os.path.join(MUNDO, 'seeds-extra', 't19', 'inicio.json')
FOTOS = os.path.join(MUNDO, 'storage', 'time-photos')
ALFA = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789'
EMPRESA = 'recicla-vale-metais'
ENDERECO = 'Rua das Oficinas, 1250 - Parque Industrial - Taubaté'
PATIO = (-23.0105, -45.5412)
UA = 'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36'
DEVICE = {'userAgent': UA, 'platform': 'Linux armv81', 'label': 'Mobile - Chrome'}


def stable_id(chave):
    """o mesmo UUID do fakebase (core/util.mjs stableId)"""
    h = bytearray(hashlib.sha1(('domiflix-fake:' + chave).encode()).digest())
    h[6] = (h[6] & 0x0f) | 0x50
    h[8] = (h[8] & 0x3f) | 0x80
    x = h[:16].hex()
    return f'{x[:8]}-{x[8:12]}-{x[12:16]}-{x[16:20]}-{x[20:32]}'


def codigo(chave):
    return ''.join(ALFA[b % len(ALFA)] for b in hashlib.sha1(chave.encode()).digest()[:12])


def t19_slug(nome):
    """slug pessoal do ponto no formato do generate_ponto_slug da 1.59.154: {empresa}-{primeiro nome}-{CÓDIGO12}"""
    import unicodedata
    primeiro = unicodedata.normalize('NFD', nome.split()[0]).encode('ascii', 'ignore').decode().lower()
    return f'{EMPRESA}-{primeiro}-{codigo("t19-ponto:" + nome)}'


KIOSK = f'{EMPRESA}-{codigo("t19-kiosk:Recicla Vale Metais")}'
CID = stable_id('company.reciclavale')
RAFAEL_USER = '@id:user.rafael'


def cpf_ok(c):
    d = [int(x) for x in c]
    for n in (9, 10):
        s = sum(d[i] * (n + 1 - i) for i in range(n))
        if (s * 10 % 11) % 10 != d[n]:
            return False
    return True


# chave, nome, cargo, depto, admissão, salário, regime, CPF, telefone, e-mail, Pix, ponto
FUNC = [
    ('rafael', 'Rafael Nogueira', 'Sócio-administrador', 'escritorio', '2015-03-02', 6000, 'informal', '27491350879', '4101',
     'rafael@reciclavalemetais.example', 'rafael@reciclavalemetais.example', False),
    ('juliana', 'Juliana Prado', 'Assistente administrativa', 'escritorio', '2023-06-05', 2800, 'clt', '36291847078', '4102',
     'juliana.prado@reciclavalemetais.example', 'juliana.prado@reciclavalemetais.example', False),
    ('marcos', 'Marcos Antunes', 'Balanceiro', 'patio', '2021-08-16', 2400, 'clt', '30567214826', '4103',
     'marcos.antunes@reciclavalemetais.example', '(12) 90000-4103', True),
    ('edson', 'Edson Moura', 'Motorista', 'patio', '2019-04-04', 2900, 'informal', '25184739637', '4104', None, '251.847.396-37', True),
    ('claudio', 'Cláudio Ferraz', 'Ajudante de pátio', 'patio', '2022-01-11', 2100, 'clt', '33409512764', '4105', None, '(12) 90000-4105', True),
    ('diego', 'Diego Morais', 'Ajudante de pátio', 'patio', '2025-07-07', 1980, 'informal', '44710368236', '4106', None, '(12) 90000-4106', True),
    ('rogerio', 'Rogério Batista', 'Ajudante de pátio', 'patio', '2025-02-03', 1980, 'informal', '39266051462', '4108', None, '(12) 90000-4108', False),
]
PONTO = ['marcos', 'edson', 'claudio', 'diego']
HOJE_ENTRADA = {'edson': '06:47', 'marcos': '06:52', 'claudio': '06:58', 'diego': '07:03'}
SEM_BATIDA = {('claudio', '2026-11-05'), ('diego', '2026-11-06')}
FERIADOS = {'2026-09-07', '2026-10-12', '2026-11-02'}


def iso(dia, hhmm, seg=0, ms=0):
    h, m = map(int, hhmm.split(':'))
    t = dt.datetime.fromisoformat(dia) + dt.timedelta(hours=h + 3, minutes=m, seconds=seg, milliseconds=ms)   # BRT -> UTC
    return t.strftime('%Y-%m-%dT%H:%M:%S.') + f'{t.microsecond // 1000:03d}Z'


def dias_uteis(ini, fim):
    d = dt.date.fromisoformat(ini)
    while d <= dt.date.fromisoformat(fim):
        if d.weekday() < 5 and d.isoformat() not in FERIADOS:
            yield d.isoformat()
        d += dt.timedelta(days=1)


def foto_avatar(caminho, semente):
    """selfie ilustrada genérica (sem rosto real): fundo do pátio, busto com colete e capacete, rosto de desenho"""
    rnd = random.Random(semente)
    S, K = 480, 3
    W = S * K
    im = Image.new('RGB', (W, W), (0, 0, 0))
    dr = ImageDraw.Draw(im)
    topo, base = (198, 214, 222), (148, 168, 178)
    for y in range(W):
        t = y / W
        dr.line([(0, y), (W, y)], fill=tuple(round(topo[i] + (base[i] - topo[i]) * t) for i in range(3)))
    dr.rectangle([0, int(W * .70), W, W], fill=(120, 128, 134))
    pele = rnd.choice([(224, 182, 150), (198, 150, 112), (164, 114, 82), (236, 196, 166)])
    roupa = rnd.choice([(242, 120, 32), (40, 92, 160), (60, 120, 80), (90, 90, 96)])
    cx = W // 2
    dr.ellipse([cx - int(W * .36), int(W * .66), cx + int(W * .36), int(W * 1.25)], fill=roupa)
    dr.rectangle([cx - int(W * .06), int(W * .58), cx + int(W * .06), int(W * .70)], fill=pele)
    dr.ellipse([cx - int(W * .17), int(W * .26), cx + int(W * .17), int(W * .66)], fill=pele)
    capacete = rnd.choice([(250, 204, 21), (250, 250, 250), (34, 139, 84)])
    dr.chord([cx - int(W * .19), int(W * .18), cx + int(W * .19), int(W * .50)], 180, 360, fill=capacete)
    dr.rectangle([cx - int(W * .22), int(W * .33), cx + int(W * .22), int(W * .355)], fill=capacete)
    olho = (40, 40, 48)
    for dx in (-1, 1):
        dr.ellipse([cx + dx * int(W * .07) - 14, int(W * .44) - 14, cx + dx * int(W * .07) + 14, int(W * .44) + 14], fill=olho)
    dr.arc([cx - int(W * .07), int(W * .48), cx + int(W * .07), int(W * .57)], 20, 160, fill=(150, 70, 60), width=10)
    if roupa == (242, 120, 32):
        dr.rectangle([cx - int(W * .30), int(W * .86), cx + int(W * .30), int(W * .89)], fill=(230, 230, 220))
    im = im.resize((S, S), Image.LANCZOS)
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    im.save(caminho, 'JPEG', quality=84)


def main():
    assert all(cpf_ok(f[7]) for f in FUNC), [f[1] for f in FUNC if not cpf_ok(f[7])]
    assert cpf_ok('41827395664')   # o do Gabriel (cap02)
    out = {'_doc': 'T19 · estado de partida (plano.md, "Mundo: o que esta aula precisa"), por cima do mundo base. Gerado por rec/t19/t19_sementes.py.'}
    out['employee_departments'] = [
        {'id': '@id:t19.depto.escritorio', 'company_id': '@id:company.reciclavale', 'name': 'Escritório', 'color': '#2563EB', 'icon': 'briefcase',
         'created_at': '2026-08-03T12:00:00.000Z', 'updated_at': '2026-08-03T12:00:00.000Z'},
        {'id': '@id:t19.depto.patio', 'company_id': '@id:company.reciclavale', 'name': 'Pátio', 'color': '#16A34A', 'icon': 'wrench',
         'created_at': '2026-08-03T12:01:00.000Z', 'updated_at': '2026-08-03T12:01:00.000Z'},
    ]
    emps = []
    for i, (k, nome, cargo, dep, adm, sal, reg, cpf, tel, email, pix, ponto) in enumerate(FUNC):
        criado = f'2026-08-03T12:{10 + i:02d}:00.000Z'
        emps.append({
            'id': f'@id:t19.func.{k}', 'company_id': '@id:company.reciclavale', 'name': nome, 'cpf': cpf, 'phone': f'(12) 90000-{tel}',
            'email': email, 'position': cargo, 'department_id': f'@id:t19.depto.{dep}', 'hire_date': adm, 'salary': sal,
            'employment_regime': reg, 'dependents_count': 0, 'vt_enabled': False, 'vt_monthly_value': None, 'pix_key': pix,
            'ponto_enabled': ponto, 'ponto_slug': t19_slug(nome) if ponto else None, 'is_active': True, 'archived_at': None,
            'photo_url': None, 'monthly_cost': None, 'monthly_cost_breakdown': None, 'address': None, 'payroll_schedule_id': None,
            'salary_period': None, 'created_by': RAFAEL_USER, 'created_at': criado, 'updated_at': criado})
    out['employees'] = emps

    movs = []

    def mov(k, chave, tipo, valor, saldo, quando, desc, metodo=None, det=None):
        movs.append({'id': f'@id:t19.mov.{k}.{chave}', 'company_id': '@id:company.reciclavale', 'employee_id': f'@id:t19.func.{k}',
                     'type': tipo, 'amount': valor, 'balance_after': saldo, 'description': desc, 'payment_method': metodo,
                     'payment_details': det, 'payroll_installment_id': None, 'created_by': RAFAEL_USER, 'created_at': quando, 'updated_at': quando})

    def pagamento(k, chave, dia, hhmm, salario, bonus=0, vales=0):
        pago = salario + bonus - vales
        det = {'cash': 0, 'pix': pago, 'salary': salario, 'bonus': bonus, 'faltas': 0, 'valesTotal': vales, 'valesDiscounted': vales,
               'valesRestantes': 0, 'holerite': None, 'valorCalculado': pago, 'valorPago': pago, 'diferenca': 0, 'motivoDiferenca': None}
        mov(k, chave, 'pagamento', -pago, 0, iso(dia, hhmm), 'Pagamento', 'pix', det)
        mov(k, chave + '.reset', 'ajuste', salario, salario, iso(dia, hhmm, ms=1), 'Reset para salário base')

    for k, nome, *_r in FUNC:
        sal = next(f[5] for f in FUNC if f[0] == k)
        if k in ('rafael', 'juliana', 'marcos', 'claudio', 'diego'):
            pagamento(k, 'pg0911', '2026-11-09', '08:00', sal)
    pagamento('rogerio', 'pg3010', '2026-10-30', '17:00', 1980)
    # Edson: pago em 07/10 (salário de então, 2.800,00); o ajuste de 13/10 saiu no formato do app de outubro (toLocaleString, antes da RPC de 28/10)
    pagamento('edson', 'pg0710', '2026-10-07', '08:00', 2800)
    mov('edson', 'aj1310', 'ajuste', 100, 2900, iso('2026-10-13', '10:00'), 'Ajuste de salário: R$ 2.800,00 → R$ 2.900,00')
    mov('edson', 'vl1510', 'vale', 200, 2700, iso('2026-10-15', '09:20'), 'Adiantamento', 'dinheiro', {'cash': 200, 'pix': 0})
    mov('edson', 'bn2210', 'bonus', 250, 2950, iso('2026-10-22', '17:10'), 'Viagens extras para São José dos Campos')
    mov('edson', 'vl2810', 'vale', 300, 2650, iso('2026-10-28', '08:40'), 'Adiantamento', 'dinheiro', {'cash': 300, 'pix': 0})
    out['employee_movements'] = movs

    out['time_settings'] = [{'id': '@id:t19.time_settings', 'company_id': '@id:company.reciclavale', 'default_in': '07:00:00', 'default_out': '16:00:00',
                             'default_break_min': 60, 'late_tolerance_min': 10, 'overnight_until': '05:00:00', 'work_weekdays': [1, 2, 3, 4, 5],
                             'require_selfie': True, 'require_geolocation': True, 'kiosk_require_face': False,
                             'created_at': '2026-09-01T10:00:00.000Z', 'updated_at': '2026-09-01T10:00:00.000Z'}]

    # batidas e folhas: 01/09 a 09/11 completas, hoje só a entrada
    recs, sheets = [], []
    for k in PONTO:
        eid = stable_id(f't19.func.{k}')
        arquivo = f'{CID}/{eid}/arquivo.jpg'
        foto_avatar(os.path.join(FOTOS, arquivo), 'arquivo-' + k)
        rnd = random.Random('batidas-' + k)
        for dia in dias_uteis('2026-09-01', '2026-11-09'):
            if (k, dia) in SEM_BATIDA:
                continue
            ent = f'06:{rnd.randint(50, 58):02d}'
            ini_int = f'11:{rnd.randint(0, 4):02d}'
            fim_int = f'12:{rnd.randint(int(ini_int[3:]), 6):02d}'
            sai = f'16:{rnd.randint(0, 7):02d}'
            batidas = [('clock_in', ent), ('break_start', ini_int), ('break_end', fim_int), ('clock_out', sai)]
            segs = {}
            for tipo, hh in batidas:
                s = rnd.randint(0, 59)
                segs[tipo] = (hh, s)
                recs.append(rec(k, eid, dia, tipo, hh, s, arquivo, rnd))
            mins = lambda t: int(segs[t][0][:2]) * 60 + int(segs[t][0][3:]) + segs[t][1] / 60
            pausa = int(mins('break_end') - mins('break_start'))
            trab = int(mins('clock_out') - mins('clock_in')) - pausa
            sheets.append(sheet(k, dia, iso(dia, ent, segs['clock_in'][1]), iso(dia, sai, segs['clock_out'][1]), trab, pausa, trab - 480, 'complete'))
        # hoje: só a entrada (dia em aberto: fora do saldo)
        hoje = '2026-11-10'
        hh = HOJE_ENTRADA[k]
        caminho = f'{CID}/{eid}/{hoje}-clock_in-{int(dt.datetime.fromisoformat(iso(hoje, hh, 21)[:19]).replace(tzinfo=dt.timezone.utc).timestamp() * 1000)}.jpg'
        foto_avatar(os.path.join(FOTOS, caminho), 'hoje-' + k)
        recs.append(rec(k, eid, hoje, 'clock_in', hh, 21, caminho, rnd))
        sheets.append(sheet(k, hoje, iso(hoje, hh, 21), None, 0, 0, None, 'open'))
    out['time_records'] = recs
    out['time_sheets'] = sheets

    out['cash_register'] = [{'id': '@id:t19.caixa.85', 'company_id': '@id:company.reciclavale', 'register_number': 85, 'status': 'open',
                             'opened_at': '2026-11-10T11:30:00.000Z', 'opened_by': RAFAEL_USER, 'initial_opening_balance': 1500,
                             'opening_balance': 1500, 'closing_balance': None, 'closed_at': None, 'currency': 'BRL',
                             'created_at': '2026-11-10T11:30:00.000Z'}]
    out['cash_transactions'] = [{'id': '@id:t19.ct.abertura', 'company_id': '@id:company.reciclavale', 'cash_register_id': '@id:t19.caixa.85',
                                 'type': 'opening', 'amount': 1500, 'description': 'Abertura do Caixa #85', 'transaction_at': '2026-11-10T11:30:00.000Z',
                                 'transaction_date': '2026-11-10', 'created_at': '2026-11-10T11:30:00.000Z', 'created_by': RAFAEL_USER,
                                 'excluded_from_dre': False}]
    out['company_fiscal_config'] = [{'id': '@id:t19.fiscal', 'company_id': '@id:company.reciclavale', 'cnpj': '47318506000107',
                                     'razao_social': 'Recicla Vale Metais Ltda', 'nome_fantasia': 'Recicla Vale Metais', 'uf': 'SP',
                                     'cidade': 'Taubaté', 'is_simples_nacional': False, 'is_default': True, 'ativo': True,
                                     'created_at': '2026-08-01T12:00:00.000Z', 'updated_at': '2026-08-01T12:00:00.000Z'}]
    out['_patch'] = {
        'companies': [{'match': {'id': '@id:company.reciclavale'}, 'set': {'ponto_kiosk_slug': KIOSK}}],
        'financial_categories': [{'match': {'company_id': '@id:company.reciclavale', 'name': 'Folha salarial'}, 'set': {'name': 'Folha Salarial'}}],
    }
    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    json.dump(out, open(SAIDA, 'w', encoding='utf8'), ensure_ascii=False, indent=0)
    print(f'{os.path.relpath(SAIDA, HERE)}: {len(emps)} funcionários, {len(movs)} movimentos, {len(recs)} batidas, {len(sheets)} folhas; '
          f'tablet {KIOSK}; slugs ' + ', '.join(f'{k} {t19_slug(n)}' for k, n, *_x in FUNC if k in PONTO) + f'; Gabriel {t19_slug("Gabriel Rocha")}')


def rec(k, eid, dia, tipo, hh, seg, foto, rnd):
    return {'id': f'@id:t19.tr.{k}.{dia}.{tipo}', 'company_id': '@id:company.reciclavale', 'employee_id': f'@id:t19.func.{k}', 'date': dia,
            'type': tipo, 'recorded_at': iso(dia, hh, seg), 'original_recorded_at': None, 'source': 'link_publico', 'address': ENDERECO,
            'latitude': round(PATIO[0] + rnd.uniform(-0.0002, 0.0002), 6), 'longitude': round(PATIO[1] + rnd.uniform(-0.0002, 0.0002), 6),
            'photo_path': foto, 'device_info': DEVICE, 'is_valid': True, 'notes': None, 'created_by': None, 'edited_at': None,
            'edited_by': None, 'invalidated_at': None, 'invalidated_by': None, 'face_match': False, 'face_score': None,
            'face_model_version': None, 'created_at': iso(dia, hh, seg)}


def sheet(k, dia, ent, sai, trab, pausa, saldo, status):
    return {'id': f'@id:t19.ts.{k}.{dia}', 'company_id': '@id:company.reciclavale', 'employee_id': f'@id:t19.func.{k}', 'date': dia,
            'first_clock_in': ent, 'last_clock_out': sai, 'total_worked_min': trab, 'total_break_min': pausa, 'expected_min': 480,
            'balance_min': saldo, 'status': status, 'justification': None, 'justified_by': None, 'created_at': ent, 'updated_at': sai or ent}


if __name__ == '__main__':
    main()
