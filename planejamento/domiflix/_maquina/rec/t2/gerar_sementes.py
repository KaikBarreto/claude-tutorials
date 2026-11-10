#!/usr/bin/env python3
"""T2 · gera as sementes de rec/fakebase/seeds-extra/t2/ (estado de partida e o estado depois de cada capítulo).

Mundo do T2: base própria `seeds-extra/t2/_base/` (FAKE_SEEDS_DIR) com SÓ a Camila Duarte; os extras somam por cima:
  inicio.json      Camila com acesso total (`user_permissions` = ["*"]): sem isso a linha dela diz "0 permissões" (handoff do app)
  apos-cap03.json  + cargo Técnico de Campo
  apos-cap04.json  + cargo Escritório
  apos-cap05.json  + Rafael Lima (Técnico, cargo Técnico de Campo)
  apos-cap06.json  + Tatiane Ribeiro (Interno, cargo Escritório)
  apos-cap07.json  = apos-cap06 (o cap07 só consulta e cancela); o Rafael já aceitou os termos de uso no primeiro login (cap08)
  apos-cap08.json  + Bruno Alves, Júlia Santos, Lucas Ferreira, Marina Costa e Paulo Souza (entram num corte, antes do cap09)
  apos-cap09.json  = apos-cap08 (o Paulo é desativado e reativado: termina ativo)
  apos-cap10.json  DELTA sobre a base PADRÃO (seeds/, que já tem os 7 perfis): os 2 cargos, as permissões dos 7 usuários e a Tatiane.
                   É o estado inicial do T5/T7 (lista de técnicos; o Rafael de acesso restrito). NÃO usar junto com a base do T2.
Cada apos-capNN do T2 é autossuficiente (tudo o que foi criado até ali, em cima de `inicio`): o robô lista ["t2/inicio", "t2/apos-capNN"].
Rodar: python3 -I rec/t2/gerar_sementes.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.normpath(os.path.join(HERE, '..', 'fakebase', 'seeds-extra', 't2'))
EMPRESA = '@id:company.glacial'

# Permissões na ordem em que o robô liga cada interruptor (a tela lista pela ordem do catálogo, não por esta)
TECNICO = ['screen:schedule', 'screen:technician_tools', 'fn:editar_os_campo']
ESCRITORIO = ['screen:quotes', 'screen:finance', 'fn:manage_finance', 'screen:dashboard', 'screen:schedule', 'fn:view_all_schedule',
              'screen:service_orders', 'fn:create_os', 'fn:edit_os', 'screen:customers', 'fn:create_customer', 'fn:edit_customer',
              'screen:equipment']
assert len(TECNICO) == 3 and len(ESCRITORIO) == 13 and len(set(ESCRITORIO)) == 13

PRESET_TECNICO = {'id': '@id:preset.tecnico', 'name': 'Técnico de Campo', 'description': 'Agenda, ferramentas e OS pelo link',
                  'permissions': TECNICO, 'created_at': '@now-10m', 'updated_at': '@now-10m'}
PRESET_ESCRITORIO = {'id': '@id:preset.escritorio', 'name': 'Escritório',
                     'description': 'Atendimento, OS, orçamentos e financeiro do dia a dia',
                     'permissions': ESCRITORIO, 'created_at': '@now-8m', 'updated_at': '@now-8m'}

# (chave, nome, e-mail, telefone) iguais aos de seeds/gen-01-tenant.json
TECNICOS = [
    ('rafael', 'Rafael Lima', 'rafael.lima@glacialcold.example', '(21) 3000-1002'),
    ('bruno', 'Bruno Alves', 'bruno.alves@glacialcold.example', '(21) 3000-1003'),
    ('julia', 'Júlia Santos', 'julia.santos@glacialcold.example', '(21) 3000-1004'),
    ('lucas', 'Lucas Ferreira', 'lucas.ferreira@glacialcold.example', '(21) 3000-1005'),
    ('marina', 'Marina Costa', 'marina.costa@glacialcold.example', '(21) 3000-1006'),
    ('paulo', 'Paulo Souza', 'paulo.souza@glacialcold.example', '(21) 3000-1007'),
]
TATIANE = ('tatiane', 'Tatiane Ribeiro', 'tatiane.ribeiro@glacialcold.example', '(21) 3000-1008')


def perfil(chave, nome, email, fone, criado):
    return {'id': f'@id:profile.{chave}', 'user_id': f'@id:user.{chave}', 'company_id': EMPRESA, 'full_name': nome, 'email': email,
            'phone': fone, 'is_active': True, 'navigation_style': 'sidebar', 'terms_accepted_at': criado, 'created_at': criado}


def permissao(chave, perms, preset):
    return {'id': f'@id:perm.{chave}', 'user_id': f'@id:user.{chave}', 'permissions': perms, 'preset_id': preset, 'is_active': True,
            'created_at': '@now-5m', 'updated_at': '@now-5m'}


def papel(chave):
    return {'id': f'@id:role.{chave}', 'user_id': f'@id:user.{chave}', 'role': 'tecnico'}


CAMILA = {'id': '@id:perm.camila', 'user_id': '@id:user.camila', 'permissions': ['*'], 'preset_id': None, 'is_active': True,
          'created_at': '@now-360d', 'updated_at': '@now-360d'}


# 1.38.19 (IMPACTO G1): sem a trilha `tutoriais-do-sistema` o gate escuro da Domiflix prende o app; com `is_onboarding: false` nem o gate nem a
# faixa de lembrete aparecem, para ninguém (Camila, Rafael, Tatiane), sem depender de reconhecimento por usuário.
TRILHA = {'id': '@id:t2.trilha.tutoriais', 'slug': 'tutoriais-do-sistema', 'title': 'Tutoriais do sistema', 'description': None, 'cover_url': None,
          'is_onboarding': False, 'is_active': True, 'intro_gate_enabled_at': '@now-30d', 'order_index': 0}


def estado(ate):
    """Linhas criadas até o capítulo `ate` (3..9), em cima da base do T2 + inicio."""
    t = {'permission_presets': [], 'profiles': [], 'user_roles': [], 'user_permissions': []}
    if ate >= 3:
        t['permission_presets'].append(PRESET_TECNICO)
    if ate >= 4:
        t['permission_presets'].append(PRESET_ESCRITORIO)
    if ate >= 5:
        k, n, e, f = TECNICOS[0]
        t['profiles'].append(perfil(k, n, e, f, '@now-30m'))
        t['user_roles'].append(papel(k))
        t['user_permissions'].append(permissao(k, TECNICO, '@id:preset.tecnico'))
    if ate >= 6:
        k, n, e, f = TATIANE
        t['profiles'].append(perfil(k, n, e, f, '@now-20m'))
        t['user_permissions'].append(permissao(k, ESCRITORIO, '@id:preset.escritorio'))
    if ate >= 8:
        for k, n, e, f in TECNICOS[1:]:
            t['profiles'].append(perfil(k, n, e, f, '@now-360d'))
            t['user_roles'].append(papel(k))
            t['user_permissions'].append(permissao(k, TECNICO, '@id:preset.tecnico'))
    return {k: v for k, v in t.items() if v}


def delta_base_padrao():
    """apos-cap10 para as aulas que usam a base PADRÃO (7 perfis e 7 papéis já existem; faltam cargos, permissões e a Tatiane)."""
    k, n, e, f = TATIANE
    perms = [dict(CAMILA)] + [permissao(c, TECNICO, '@id:preset.tecnico') for c, *_ in TECNICOS]
    return {'permission_presets': [PRESET_TECNICO, PRESET_ESCRITORIO],
            'profiles': [perfil(k, n, e, f, '@now-20m')],
            'user_permissions': perms + [permissao(k, ESCRITORIO, '@id:preset.escritorio')]}


def grava(nome, comentario, tabelas):
    d = {'_comentario': comentario, **tabelas}
    with open(os.path.join(DEST, nome + '.json'), 'w', encoding='utf-8') as fp:
        json.dump(d, fp, ensure_ascii=False, indent=1)
        fp.write('\n')
    print(nome, {k: len(v) for k, v in tabelas.items()})


def main():
    os.makedirs(DEST, exist_ok=True)
    grava('inicio', 'T2 · estado de partida (fim do T1) em cima da base própria _base/: a Camila tem Acesso Total (curinga *), como a conta '
                    'administradora de uma empresa real; sem a linha em user_permissions a lista de usuários diria "0 permissões" para ela. '
                    'Use junto com t1/apos-cap13 (identidade da empresa) e FAKE_SEEDS_DIR=seeds-extra/t2/_base.',
          {'user_permissions': [CAMILA], 'domiflix_learning_paths': [TRILHA]})
    textos = {
        3: 'cargo Técnico de Campo criado (3 permissões)',
        4: 'cargos Técnico de Campo (3 permissões) e Escritório (13 permissões)',
        5: 'Rafael Lima criado como Técnico, com o cargo Técnico de Campo',
        6: 'Tatiane Ribeiro criada como Interno, com o cargo Escritório',
        7: 'igual ao apos-cap06 (o cap07 só consulta e cancela); termos de uso aceitos por Rafael e Tatiane (primeiro login)',
        8: 'os cinco técnicos que entram num corte (Bruno, Júlia, Lucas, Marina e Paulo, ativos, cargo Técnico de Campo): a lista tem 8 pessoas',
        9: 'igual ao apos-cap08 (o Paulo é desativado e reativado: termina ativo)',
    }
    for n in range(3, 10):
        grava(f'apos-cap{n:02d}', f'T2 · estado DEPOIS do cap{n:02d}, autossuficiente (em cima de inicio): {textos[n]}.', estado(min(n, 8) if n != 9 else 8))
    grava('apos-cap10', 'T2 · estado FINAL da aula = DELTA sobre a base PADRÃO (seeds/): os 2 cargos (Técnico de Campo e Escritório), as permissões '
                        'de Camila (acesso total), Rafael, Bruno, Júlia, Lucas, Marina e Paulo (cargo Técnico de Campo) e a Tatiane Ribeiro '
                        '(Interno, cargo Escritório, tatiane.ribeiro@glacialcold.example, (21) 3000-1008). Oito usuários ativos. Estado inicial do T5 '
                        'e do T7. Não usar junto com a base própria do T2 (duplicaria os perfis).', delta_base_padrao())


if __name__ == '__main__':
    main()
