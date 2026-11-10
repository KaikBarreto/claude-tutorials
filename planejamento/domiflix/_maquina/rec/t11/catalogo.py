#!/usr/bin/env python3
"""T11 · reconstrói o catálogo global da norma PMOC (`pmoc_activity_catalog`) a partir das migrações do app 1.38.19:
  20260617200000 (INSERT das atividades) + 20260628150000 (renomeios, linhas novas, essential_tier e activity_group)
  + 20260619140000 (guidance). Devolve a lista de linhas para a semente. Só leitura das migrações."""
import os, re

HOME = os.environ.get('TUT_HOME') or os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
MIG = os.path.join(HOME, 'src-1.38.19', 'supabase', 'migrations')
STR = r"'(?:[^']|'')*'"


RENOMEADOS = {('condicionadores', 'circuito_refrigerante', 'Verificar vazamento de gás'): 'Inspecionar indícios de vazamento de refrigerante',
              ('condicionadores', 'bandejas', 'Lavar e remover o biofilme'): 'Lavar a bandeja e remover o biofilme'}


def sql_str(s):
    return s[1:-1].replace("''", "'")


def ler(nome):
    return open(os.path.join(MIG, nome), encoding='utf8').read()


def monta():
    linhas = []
    fase2 = ler('20260617200000_pmoc_activity_catalog_fase2.sql')
    pat = re.compile(r"^\s*\(\s*(" + STR + r")\s*,\s*(NULL|" + STR + r")\s*,\s*(" + STR + r")\s*,\s*(" + STR + r")\s*,\s*(true|false)\s*,\s*(NULL|" + STR +
                     r")\s*,\s*(\d+)\s*\)\s*[,;]?\s*$", re.M)
    for m in pat.finditer(fase2):
        sec, comp, desc, freq, med, unit, ordem = m.groups()
        linhas.append({'section': sql_str(sec), 'component': None if comp == 'NULL' else sql_str(comp), 'description': sql_str(desc),
                       'default_freq_code': sql_str(freq), 'is_measurement': med == 'true', 'unit': None if unit == 'NULL' else sql_str(unit),
                       'sort_order': int(ordem), 'guidance': None, 'essential_tier': None, 'activity_group': None,
                       'expected_min': None, 'expected_max': None, 'is_active': True})
    assert len(linhas) > 140, len(linhas)

    ess = ler('20260628150000_pmoc_catalog_essencial_e_grupos.sql')
    # renomeios
    for l in linhas:
        if l['section'] == 'condicionadores' and l['component'] == 'circuito_refrigerante' and l['description'] == 'Verificar vazamento de gás':
            l['description'] = 'Inspecionar indícios de vazamento de refrigerante'
        if l['section'] == 'condicionadores' and l['component'] == 'bandejas' and l['description'] == 'Lavar e remover o biofilme':
            l['description'] = 'Lavar a bandeja e remover o biofilme'
    # linhas novas
    linhas.append({'section': 'condicionadores', 'component': 'evaporadores', 'description': 'Desobstruir o dreno', 'default_freq_code': 'M',
                   'is_measurement': False, 'unit': None, 'sort_order': 125, 'guidance': None, 'essential_tier': 'base', 'activity_group': 'limpeza',
                   'expected_min': None, 'expected_max': None, 'is_active': True})
    linhas.append({'section': 'testes', 'component': None, 'description': 'Teste operacional', 'default_freq_code': 'M', 'is_measurement': False,
                   'unit': None, 'sort_order': 5, 'guidance': None, 'essential_tier': 'base', 'activity_group': 'teste',
                   'expected_min': None, 'expected_max': None, 'is_active': True})

    def acha(sec, comp, desc):
        return [l for l in linhas if l['section'] == sec and l['component'] == comp and (desc is None or l['description'] == desc)]

    # UPDATE ... SET essential_tier='x', activity_group='y' WHERE section='s' AND [component='c' AND] description='d'
    up = re.compile(r"UPDATE public\.pmoc_activity_catalog SET (essential_tier='(\w+)')?(?:,\s*)?(activity_group='(\w+)')?\s*WHERE section\s*=\s*'(\w+)'"
                    r"(?:\s+AND component\s*=\s*'(\w+)')?\s+AND description\s*=\s*(" + STR + r")\s*;")
    n_up = 0
    for m in up.finditer(ess):
        _, tier, _, grp, sec, comp, desc = m.groups()
        alvo = acha(sec, comp, sql_str(desc)) if comp else [l for l in linhas if l['section'] == sec and l['description'] == sql_str(desc)]
        assert alvo, (sec, comp, desc)
        for l in alvo:
            if tier:
                l['essential_tier'] = tier
            if grp:
                l['activity_group'] = grp
            n_up += 1
    for l in linhas:  # passo 5
        if l['section'] == 'medicoes' and not l['activity_group']:
            l['activity_group'] = 'medicao'
        if l['section'] == 'testes' and not l['activity_group']:
            l['activity_group'] = 'teste'
    for l in linhas:
        if l['section'] == 'condicionadores' and not l['activity_group']:
            d = l['description']
            l['activity_group'] = 'limpeza' if d.startswith(('Limpar', 'Lavar', 'Aplicar', 'Desobstruir', 'Desencrustar', 'Fazer a limpeza')) else 'inspecao'
    n = {t: sum(1 for l in linhas if l['essential_tier'] == t) for t in ('base', 'central', 'infra')}
    assert n == {'base': 17, 'central': 4, 'infra': 8}, n

    # guidance
    gu = ler('20260619140000_pmoc_activity_guidance_seed_backfill.sql')
    g = re.compile(r"UPDATE public\.pmoc_activity_catalog SET guidance = (" + STR + r") WHERE section = '(\w+)' AND component IS NOT DISTINCT FROM (NULL|'\w+') AND description = (" + STR + r");")
    ng = 0
    for m in g.finditer(gu):
        txt, sec, comp, desc = m.groups()
        comp = None if comp == 'NULL' else comp.strip("'")
        d = sql_str(desc)
        d = RENOMEADOS.get((sec, comp, d), d)  # a guidance foi gravada antes do renomeio
        for l in acha(sec, comp, None):
            if l['description'] == d:
                l['guidance'] = sql_str(txt)
                ng += 1
    for i, l in enumerate(sorted(linhas, key=lambda x: (x['section'], x['sort_order']))):
        l['id'] = f'@id:pmoc.catalogo.{i:03d}'
    return linhas, n_up, ng


if __name__ == '__main__':
    ls, nu, ng = monta()
    print(len(ls), 'atividades;', nu, 'updates de nível/grupo;', ng, 'guidances;', sum(1 for l in ls if not l['guidance']), 'sem guidance')
