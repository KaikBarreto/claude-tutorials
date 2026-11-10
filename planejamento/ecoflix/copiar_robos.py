#!/usr/bin/env python3
"""Cópia de segurança, no git, do que os agentes do robô fazem fora dele (o coordenador roda antes de cada commit):
  $TUT_HOME/rec/tNN  -> planejamento/ecoflix/TNN/rec/   (gerar*.py, ajudantes .py/.mjs da aula e os capNN.json gerados;
                                                         sem o kit do molde, gravações, telemetria, _ens/ e _ex/)
  $TUT_HOME/rec/mundo -> perfis/ecoflix/mundo/           (handlers, hooks, lib, sementes; só arquivo novo ou mais novo)
Nada é apagado no destino. uso: python3 -I planejamento/ecoflix/copiar_robos.py   (TUT_HOME padrão: /home/claude/ecoflix)"""
import os
import re
import shutil
import sys

SKILL = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
TUT_HOME = os.environ.get('TUT_HOME', '/home/claude/ecoflix')
MOLDE = set(os.listdir(os.path.join(SKILL, 'ferramentas', 'rec', 'molde')))
TEXTO = ('.py', '.mjs', '.json', '.md', '.sh')


def copia(src, dst):
    if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
        return 0
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)
    return 1


n = 0
rec = os.path.join(TUT_HOME, 'rec')
for aula in sorted(os.listdir(rec)):
    if not re.fullmatch(r't\d\d', aula):
        continue
    dst = os.path.join(SKILL, 'planejamento', 'ecoflix', 'T' + aula[1:], 'rec')
    for f in sorted(os.listdir(os.path.join(rec, aula))):
        p = os.path.join(rec, aula, f)
        if not os.path.isfile(p) or f in MOLDE or not f.endswith(TEXTO):
            continue
        if f.endswith(('.actions.json', '.telemetry.json')) or os.path.getsize(p) > 2_000_000:
            continue
        n += copia(p, os.path.join(dst, f))
mundo = os.path.join(rec, 'mundo')
for raiz, dirs, arqs in os.walk(mundo):
    dirs[:] = [d for d in dirs if d not in ('node_modules', '.runtime')]
    for f in arqs:
        p = os.path.join(raiz, f)
        if f.endswith(TEXTO) and os.path.getsize(p) <= 5_000_000:
            n += copia(p, os.path.join(SKILL, 'perfis', 'ecoflix', 'mundo', os.path.relpath(p, mundo)))
print(f'{n} arquivo(s) copiado(s) para o git', file=sys.stderr)
