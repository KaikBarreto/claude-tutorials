#!/usr/bin/env python3
"""T21 · tira as respostas simuladas R1 a R9 do plano (planejamento/ecoflix/T21/plano.md, "Respostas simuladas") e grava
rec/mundo/lib/cato_respostas.json, que o Supabase falso usa (rec/mundo/lib/cato.mjs: edge cato-background, tabela cato_jobs e
edge cato-assist com mode "followups"). O plano é a fonte: mudou uma resposta lá, rode de novo e suba a instância
(`FAKE_PORT=54321 bash rec/run.sh fake`).

Por resposta, além do `response_payload` e das sugestões (`followups`, que NÃO vão no payload):
 - `espera`: segundos até o job virar `completed` (a tela consulta a cada 1 s; R1 mostra "Pensando…" e "Buscando seus dados…",
   como o roteiro do cap03 pede);
 - `hora`: o "Atualizado às" de cada resposta (HH:MM do dia do relógio falso). Fixo por resposta para a conversa contínua dos
   caps. 3 a 8 sair igual quando um capítulo restaura as respostas dos anteriores pelo sessionStorage (cada gravação recomeça o
   relógio em 08:30).
Uso: python3 -I rec/t21/t21_respostas.py [--plano <plano.md>]
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PLANO = '/home/claude/claude-tutorials/planejamento/ecoflix/T21/plano.md'
if '--plano' in sys.argv:
    PLANO = sys.argv[sys.argv.index('--plano') + 1]
SAIDA = os.path.normpath(os.path.join(HERE, '..', 'mundo', 'lib', 'cato_respostas.json'))

ESPERA = {'R1': 3.2}            # demais: 1,6 s (completa no 3º poll, ~2 s depois do Enviar)
HORA = {**{f'R{i}': '08:30' for i in range(1, 6)}, **{f'R{i}': '08:31' for i in range(6, 9)}}

txt = open(PLANO, encoding='utf8').read()
ini = txt.index('### Respostas simuladas')
fim = txt.index('## Riscos e decisões')
bloco = txt[ini:fim]
achados = re.findall(r'^(R\d) · "([^"]+)".*?```json\n(.*?)\n```', bloco, re.S | re.M)
if len(achados) != 9:
    raise SystemExit(f'esperava R1 a R9 no plano, achei {len(achados)}')
out = []
for chave, pergunta, js in achados:
    d = json.loads(js)
    follow = d.pop('followups', [])
    out.append({'chave': chave, 'pergunta': pergunta, 'espera': ESPERA.get(chave, 1.6), 'hora': HORA.get(chave),
                'sugestoes': follow, 'payload': d})
json.dump({'_doc': 'Gerado por rec/t21/t21_respostas.py a partir de planejamento/ecoflix/T21/plano.md (R1 a R9). Não editar à mão.',
           'respostas': out}, open(SAIDA, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print(f'{len(out)} respostas -> {SAIDA}')
for r in out:
    print(f"  {r['chave']} espera {r['espera']} s, hora {r['hora']}: {r['pergunta']}")
