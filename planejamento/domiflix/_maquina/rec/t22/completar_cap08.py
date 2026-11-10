#!/usr/bin/env python3
"""T22 · completa o apos-cap08 do ensaio: as 8 ligações do desenho (com "Sim" e "Não" nas saídas da decisão) no `processes.data` do fluxograma.
Motivo: o arrasto de ligação do robô pega só 5 a 6 das 8 ligações (as alças da Decisão e do Documento ficam sob a camada do texto da forma). Plano B do roteiro
(cap08): os capítulos 9 a 11 partem do desenho já ligado, por semente, com a mesma fala. Rodar depois do ensaio do cap08:  python3 -I rec/t22/completar_cap08.py"""
import json, os, uuid
P = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'fakebase', 'seeds-extra', 't22', 'apos-cap08.json'))
d = json.load(open(P, encoding='utf8'))
p = d['processes'][0]
nid = {n['data'].get('label'): n['id'] for n in p['data']['nodes'] if n.get('type') != 'lane'}
L = [('Chamado aberto no portal', 'right', 'Triagem do chamado', 'left', None), ('Triagem do chamado', 'right', 'Precisa de visita?', 'left', None),
     ('Precisa de visita?', 'right', 'Agendar visita e técnico', 'left', 'Sim'), ('Agendar visita e técnico', 'right', 'Executar a visita', 'left', None),
     ('Executar a visita', 'bottom', 'Relatório de Serviço', 'top', None), ('Relatório de Serviço', 'left', 'Chamado encerrado', 'top', None),
     ('Precisa de visita?', 'bottom', 'Orientar o cliente por telefone', 'top', 'Não'), ('Orientar o cliente por telefone', 'right', 'Chamado encerrado', 'left', None)]
edges = []
for a, ha, b, hb, rot in L:
    e = {'id': str(uuid.uuid5(uuid.NAMESPACE_URL, f't22:{a}:{b}')), 'source': nid[a], 'target': nid[b], 'sourceHandle': f'{ha}-source', 'targetHandle': f'{hb}-target', 'data': {'kind': 'sequence'}}
    if rot:
        e['label'] = rot
    edges.append(e)
p['data']['edges'] = edges
json.dump(d, open(P, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print('apos-cap08 completado:', len(edges), 'ligações')
