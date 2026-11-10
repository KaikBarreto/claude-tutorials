#!/usr/bin/env python3
"""T22 · gera o mundo de partida das Ferramentas de RH (rec/fakebase/seeds-extra/t22/inicio.json) e rec/t22/cadeia.json.

Estado de partida = fim do T15 (cadeia do T15 + a semente final dele, `T15_FINAL`) + `t22/inicio`: duas avaliações DISC respondidas do Bruno Alves
(15/05/2026 e 05/11/2026) para o "Comparar" e a "Evolução do perfil", e o padrão da empresa "Funcionário vê o resultado ao final" ligado
(`company_settings.disc_show_result_to_employee`, padrão `true` no banco). Nenhum organograma nem fluxograma (nascem ao vivo).
Enquanto o T15 não termina, a cadeia provisória é a do T20 + `t22/_prov-t15` (só a Tatiane Ribeiro, "Assistente administrativa"): serve para EXPLORAR, não para gravar.
Rodar de qualquer pasta:  python3 -I rec/t22/semear.py                      (cadeia provisória)
                          T15_FINAL=t15/apos-capNN python3 -I rec/t22/semear.py   (cadeia real: lê rec/t15/cadeia.json)
"""
import hashlib
import json
import os
import re
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
EXTRA = os.path.normpath(os.path.join(HERE, '..', 'fakebase', 'seeds-extra'))
FAKE_NOW = '2026-11-12T10:00:00-03:00'
EMP = '9c307966-79f1-567c-ac4d-d5fd3c1a2f40'
CAMILA = 'd40f5787-1779-501f-900c-ddb2b90a36e5'
T15_FINAL = os.environ.get('T15_FINAL')


def short_code(seed, n=12):
    """igual a shortCode() do fakebase (core/util.mjs): sha1 do texto, alfabeto base32 sem ambíguos"""
    a = 'abcdefghjkmnpqrstuvwxyz23456789'
    d = hashlib.sha1(str(seed).encode()).digest()
    return ''.join(a[d[i] % len(a)] for i in range(n))


def avaliacao(n, quando_criada, quando_respondida, scores, primary, secondary, code):
    """uma avaliação DISC respondida do Bruno; o código segue a regra do gatilho do fakebase (hooks/disc_assessments.mjs): nome + ordem do link"""
    return {
        'id': f'@id:t22.disc.bruno.{n}', 'company_id': EMP, 'employee_id': '@id:t9.func.bruno', 'status': 'completed',
        'public_short_code': short_code(f'disc_assessments:Bruno Alves:{n - 1}'), 'show_result_to_employee': True,
        'answers': None, 'scores': scores, 'primary_type': primary, 'secondary_type': secondary, 'profile_code': code, 'locale': 'pt-br',
        'completed_at': quando_respondida, 'created_by': CAMILA, 'created_at': quando_criada,
    }


def montar():
    ini = {'_comentario': 'T22 · duas avaliações DISC respondidas do Bruno Alves (15/05 e 05/11/2026) + padrão da empresa "Funcionário vê o resultado". Gerado por rec/t22/semear.py: não edite à mão.'}
    # maio: Conformidade 71 e Dominância 68 (perfil CD); novembro: Conformidade 72 e Influência 60 (perfil CI): a Dominância cai e a Influência sobe
    ini['permission_presets'] = []   # a tela de Funcionários lê a tabela (GET sem filtro); vazia basta e evita o aviso TABELA_SEM_SEED em /__dev/unknowns
    ini['disc_assessments'] = [
        avaliacao(1, '2026-05-15T13:50:00.000Z', '2026-05-15T14:20:00.000Z', {'D': 68, 'I': 35, 'S': 42, 'C': 71}, 'C', 'D', 'CD'),
        avaliacao(2, '2026-11-05T13:10:00.000Z', '2026-11-05T13:40:00.000Z', {'D': 45, 'I': 60, 'S': 52, 'C': 72}, 'C', 'I', 'CI'),
    ]
    ini['_patch'] = {'company_settings': [{'match': {'company_id': EMP}, 'set': {'disc_show_result_to_employee': True}}]}
    return ini


def cadeia_base():
    c15 = os.path.join(HERE, '..', 't15', 'cadeia.json')
    if T15_FINAL:
        with open(c15, encoding='utf8') as f:
            base = list(json.load(f)['inicio'])
        return base + [T15_FINAL], 'real'
    with open(os.path.join(HERE, '..', 't20', 'cadeia.json'), encoding='utf8') as f:
        base = list(json.load(f)['inicio'])
    extra = [f't15/{n}' for n in ('inicio', 'salarios', 'folhas') if os.path.exists(os.path.join(EXTRA, 't15', n + '.json'))]
    if os.path.exists(os.path.join(EXTRA, 't20', 'apos-cap03.json')):
        base = base + ['t20/apos-cap03']
    return base + extra + ['t22/_prov-t15'], 'PROVISÓRIA (T20 + sementes do T15 que existem + Tatiane)'


def verificar(ini, cadeia):
    ids = set()
    faltam = []
    for rel in cadeia:
        arq = os.path.join(EXTRA, rel + '.json')
        if not os.path.exists(arq):
            faltam.append(rel)
            continue
        with open(arq, encoding='utf8') as f:
            ids |= set(re.findall(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', f.read()))
            f.seek(0)
            ids |= set(re.findall(r'@id:[A-Za-z0-9_.\-]+', f.read()))
    ref = set(re.findall(r'@id:[A-Za-z0-9_.\-]+', json.dumps(ini)))
    ref = {r for r in ref if not r.startswith('@id:t22.')}
    print('ids @id: usados e não definidos na cadeia:', sorted(ref - ids) or 'nenhum')
    if faltam:
        print('SEMENTES DA CADEIA QUE AINDA NÃO EXISTEM:', faltam)


def main():
    ini = montar()
    base, modo = cadeia_base()
    os.makedirs(os.path.join(EXTRA, 't22'), exist_ok=True)
    with open(os.path.join(EXTRA, 't22', 'inicio.json'), 'w', encoding='utf8') as f:
        json.dump(ini, f, ensure_ascii=False, indent=1)
    cad = {'fake_now': FAKE_NOW, 'inicio': base + ['t22/inicio'], 't15_final': T15_FINAL or 'PROVISORIO', 'modo': modo,
           'nota': 'mundo do T22 = fim do T15 (cadeia do T15 + semente final) + t22/inicio; apos-capNN do T22 são cumulativos sobre t22/inicio (caps 1, 2, 6 a 10 mudam o banco)'}
    with open(os.path.join(HERE, 'cadeia.json'), 'w', encoding='utf8') as f:
        json.dump(cad, f, ensure_ascii=False, indent=1)
    print(f't22/inicio.json e rec/t22/cadeia.json gerados (cadeia {modo}, T15_FINAL = {T15_FINAL}).')
    print('  códigos das avaliações do Bruno:', [a['public_short_code'] for a in ini['disc_assessments']], '· Rafael (1º link):', short_code('disc_assessments:Rafael Lima:0'))
    verificar(ini, base)


if __name__ == '__main__':
    main()
