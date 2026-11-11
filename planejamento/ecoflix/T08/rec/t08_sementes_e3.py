#!/usr/bin/env python3
"""T08 · compõe as sementes apos-cap02..07 (e ajusta os horários da apos-cap09) a partir da exploração e3 (rec/t08/_ex/e3.out), que faz o
fluxo dos caps 02 a 09 de uma vez e despeja `weighing_tickets` e `order_drafts` depois de cada etapa. Assim cada capítulo parte da
própria semente e os capítulos podem entrar na fila da trava ao mesmo tempo (a cadeia não espera a gravação do anterior).
Horários: a exploração roda às 08:40 (FAKE_NOW); cada instante novo de uma etapa vai para o horário da história dela (linha do tempo,
"O dia 10/11": o Edson pesa cheio às 08:41, vazio às 08:50, o #58 nasce às 08:52, a valorização às 08:58 e a compra perto das 09:00),
mantendo a ordem e a distância entre os instantes da etapa.
Uso: python3 -I rec/t08/t08_sementes_e3.py   (depois de rodar a e3 e o `t08_semente.py apos-cap09`)"""
import json
import os
import re
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.normpath(os.path.join(HERE, '..', 'mundo', 'seeds-extra', 't08'))
ISO = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:?\d{2})$')
INICIO_E3 = datetime(2026, 11, 10, 11, 40, tzinfo=timezone.utc)          # FAKE_NOW 08:40 da exploração
BRT = lambda h, m, s=0: datetime(2026, 11, 10, h + 3, m, s, tzinfo=timezone.utc)
HORA = {'02': BRT(8, 40, 40), '03': BRT(8, 41, 40), '04': BRT(8, 50, 20), '05': BRT(8, 51, 0), '06': BRT(8, 51, 40), '07': BRT(8, 58, 30),
        '09': BRT(8, 59, 30)}
DOC = {'02': 'rascunho #58 com a Cooperativa Recomeço, o Edson Moura e o FKD2E41 (sem item: o material escolhido não fica no rascunho)',
       '03': '+ o item Alumínio latinha com a 1ª pesagem de 9.460 kg (conta como bruto), modo Completo',
       '04': '+ 1ª 9.460 e 2ª 6.380: bruto 3.080',
       '05': '+ impureza 2 % = 61,6 kg: líquido 3.018,4 kg',
       '06': '#58 salvo às 08:52 (pendente) + rascunho #59 do Jair Lopes (Auto Peças Vale Forte, bateria, 1ª 5.640, GHT7B19)',
       '07': '+ a compra em rascunho do #58 (order_drafts, R$ 6,20/kg, R$ 18.714,08), aberta pelo Valorizar'}


def para_dt(s):
    return datetime.fromisoformat(s.replace('Z', '+00:00'))


def fmt(dt, modelo):
    s = dt.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
    return s + ('Z' if modelo.endswith('Z') else '+00:00')


def instantes(v, out):
    if isinstance(v, str) and ISO.match(v):
        out.add(v)
    elif isinstance(v, dict):
        for x in v.values():
            instantes(x, out)
    elif isinstance(v, list):
        for x in v:
            instantes(x, out)
    return out


def troca(v, mapa):
    if isinstance(v, str) and v in mapa:
        return mapa[v]
    if isinstance(v, dict):
        return {k: troca(x, mapa) for k, x in v.items()}
    if isinstance(v, list):
        return [troca(x, mapa) for x in v]
    return v


def main():
    etapas, atual = [], None
    for linha in open(os.path.join(HERE, '_ex', 'e3.out'), encoding='utf8'):
        m = re.match(r'^\d+ eval: (.*)$', linha.rstrip('\n'))
        if not m:
            continue
        v = json.loads(m.group(1))
        if isinstance(v, str) and v.startswith('ETAPA '):
            atual = v[6:]
        elif isinstance(v, str) and v.startswith('ESTADO ') and atual:
            etapas.append((atual, json.loads(v[7:])))
    if [e for e, _ in etapas] != ['02', '03', '04', '05', '06', '07']:
        raise SystemExit(f'etapas da e3: {[e for e, _ in etapas]}')
    mapa, vistos = {}, set()
    for nome, est in etapas:
        linhas = {t: [r for r in est[t] if r.get('ticket_number') != 57] for t in ('weighing_tickets', 'order_drafts')}
        novos = sorted({s for t in linhas.values() for r in t for s in instantes(r, set()) if s not in vistos and para_dt(s) >= INICIO_E3},
                       key=para_dt)
        if novos:
            t0 = para_dt(novos[0])
            for s in novos:
                mapa[s] = fmt(HORA[nome] + (para_dt(s) - t0), s)
        vistos |= set(novos)
        sem = {'_doc': f'T8 · estado depois do cap{nome} (cumulativo desde t08/inicio): {DOC[nome]}. Composto por rec/t08/t08_sementes_e3.py '
                       f'da exploração e3 (o mesmo fluxo do robô), com os horários da história.'}
        sem.update({t: troca(r, mapa) for t, r in linhas.items() if r})
        json.dump(sem, open(os.path.join(SAIDA, f'apos-cap{nome}.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
        print(f'apos-cap{nome}: ' + ', '.join(f'{t} {len(r)}' for t, r in linhas.items()) + f'; {len(novos)} instantes novos')
    # apos-cap09 (t08_semente.py, diff completo contra a base): mesmos horários das etapas e a compra perto das 09:00
    p9 = os.path.join(SAIDA, 'apos-cap09.json')
    s9 = json.load(open(p9, encoding='utf8'))
    if 'horários da história' in s9.get('_doc', ''):
        print('apos-cap09 já ajustada (rode o t08_semente.py apos-cap09 de novo para refazer)'); return
    resto = sorted({s for s in instantes(s9, set()) if s not in mapa and para_dt(s) >= INICIO_E3}, key=para_dt)
    if resto:
        t0 = para_dt(resto[0])
        for s in resto:
            mapa[s] = fmt(HORA['09'] + (para_dt(s) - t0), s)
    s9 = troca(s9, mapa)
    s9['_doc'] = ('T8 · estado depois do cap09 (cumulativo desde t08/inicio): o #58 valorizado pela compra de R$ 18.714,08 (Pix, Conta '
                  'Principal, ~09:00), o estoque e o banco que ela mexe, e o rascunho #59 do Jair. Diff do t08_semente.py com os horários da história.')
    json.dump(s9, open(p9, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print(f'apos-cap09: {len(resto)} instantes da compra ajustados')


if __name__ == '__main__':
    main()
