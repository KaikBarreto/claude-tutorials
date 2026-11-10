#!/usr/bin/env python3
"""Gera as sementes do T0 v2 em rec/fakebase/seeds-extra/t0v2/. Mundo fictício: Glacial Cold Brasil, Camila Duarte."""
import json, os
OUT = os.path.join(os.path.dirname(__file__), '..', 'fakebase', 'seeds-extra', 't0v2')
os.makedirs(OUT, exist_ok=True)
def w(n, d): json.dump(d, open(os.path.join(OUT, n + '.json'), 'w'), ensure_ascii=False, indent=1)

PATH = 'c0000000-0000-4000-8000-000000000001'
core = [  # (n, título, descrição, capa, ordem, telas, arquivo|None, min)
 (0,'Boas-vindas à Dominex','Conheça os combinados da parceria, como funciona a DomiFlix e por onde começar.','t0-dashboard-completo',0,[],'t0-boas-vindas-dominex',4),
 (1,'Configurações e identidade da empresa','Configure os dados, a identidade visual e as preferências iniciais da empresa.','t1-configuracoes',10,['screen:settings'],'t1-configuracoes-identidade',13),
 (2,'Usuários, cargos e permissões','Cadastre a equipe e defina com clareza o que cada pessoa pode acessar.','t1-perfil',20,['screen:users'],None,25),
 (3,'Clientes, fornecedores e equipamentos','Monte a base de clientes, fornecedores e equipamentos usada pela operação.','t3-clientes',30,['screen:customers','screen:equipment'],'t3-clientes-fornecedores-equipamentos',13),
 (4,'Serviços, tarefas e checklists','Cadastre os serviços, tipos de tarefa e checklists usados no atendimento.','t4-servicos',40,['screen:services','screen:questionnaires'],'t4-servicos-tarefas-checklists',11),
 (5,'Ordens de Serviço, agenda, equipes e mapa ao vivo','Abra, distribua, agende e acompanhe Ordens de Serviço e equipes em campo.','t5-ordens-servico',50,['screen:service_orders','screen:schedule','screen:tracking'],'t5-os-agenda-equipes-mapa',14),
]
plan = [  # (código módulo, título, descrição, arquivo)
 ('contracts','Gestão de Contratos e PMOC','Crie contratos, acompanhe o PMOC e gere os documentos do contrato.','plano-contratos-pmoc'),
 ('rh','Funcionários e RH','Cadastre a equipe, acompanhe documentos e organize a rotina de RH.','plano-funcionarios-rh'),
 ('crm','CRM e Kanban','Acompanhe oportunidades e propostas em um quadro Kanban.','plano-crm-kanban'),
 ('nfe','Emissão de Notas Fiscais','Emita notas fiscais de serviço direto da Ordem de Serviço.','plano-notas-fiscais'),
 ('cobrancas','Cobranças online','Cobre seus clientes por Pix, boleto ou cartão e acompanhe os recebimentos.','plano-cobrancas'),
]
mods = [('basic','Módulo Básico',197,'module',1),('contracts','Gestão de Contratos e PMOC',100,'module',2),('rh','Funcionários / RH',60,'addon',3),
 ('crm','CRM / Kanban',90,'addon',4),('nfe','Emissão de Notas Fiscais',120,'addon',5),('customer_portal','Portal do Cliente',0,'addon',8),
 ('pricing_advanced','Precificação Avançada',0,'addon',9),('video_questions','Perguntas em Vídeo',0,'addon',10),('whatsapp','Avisos de WhatsApp',80,'addon',12),
 ('cobrancas','Cobranças online',150,'addon',13),('pdv','PDV e Loja',200,'addon',14)]
VTT = "WEBVTT\n\n00:00.000 --> 00:04.000\nNeste vídeo você aprende o tema da aula,\n\n00:04.000 --> 00:08.000\npasso a passo, com o sistema na tela.\n\n00:08.000 --> 00:12.000\nDepois, é só seguir para a próxima aula.\n"
titles, eps, tmod, subs, res = [], [], [], [], []
for n, t, d, cap, order, keys, f, mn in core:
    tid = f'd0000000-0000-4000-8000-00000000000{n}'
    titles.append(dict(id=tid, type='series', title=t, description=d, banner_url=f'/guia-tecnico/img/{cap}.jpg', thumbnail_url=f'/guia-tecnico/img/{cap}.jpg', tags=['tutorial'], is_featured=n==0, order_index=order, track_group='core', track_order=order, learning_path_id=PATH, is_active=True, required_screen_keys=keys))
    eid = f'e0000000-0000-4000-8000-00000000000{n}'
    eps.append(dict(id=eid, title_id=tid, season_id=None, episode_number=None, title=t, description=d if n else 'Entenda os combinados da parceria e como usar as trilhas da DomiFlix.', video_id=(f'tutorials/{f}.mp4' if f else None), video_type='storage', mobile_video_id=(f'tutorials/mobile/{f}.mp4' if f else None), mobile_video_type=('storage' if f else None), duration_minutes=mn, order_index=0, is_active=True, recorded_at='@now-10d'))
    if f:
        subs.append(dict(episode_id=eid, language_code='pt-BR', label='Português', format='vtt', content=VTT, is_default=True, order_index=0))
        res.append(dict(episode_id=eid, title='Guia Técnico: ' + t.split(',')[0], description='O assunto da aula, por escrito.', resource_type='link', url='https://www.dominex.app/guia-tecnico', order_index=0))
        if n in (1, 3): res.append(dict(episode_id=eid, title='Roteiro da aula', description='Resumo dos passos.', resource_type='link', url='https://www.dominex.app/guia-tecnico', order_index=1))
for i, (code, t, d, f) in enumerate(plan):
    tid = f'd1000000-0000-4000-8000-00000000000{i}'
    order = 100 + i * 10
    titles.append(dict(id=tid, type='series', title=t, description=d, banner_url='/guia-tecnico/img/t5-ordens-servico.jpg', thumbnail_url='/guia-tecnico/img/t5-ordens-servico.jpg', tags=['tutorial'], is_featured=False, order_index=order, track_group='plan', track_order=order, learning_path_id=PATH, is_active=True, required_screen_keys=[]))
    tmod.append(dict(title_id=tid, module_code=code))
    eid = f'e1000000-0000-4000-8000-00000000000{i}'
    eps.append(dict(id=eid, title_id=tid, season_id=None, episode_number=None, title=t, description=d, video_id=f'tutorials/{f}.mp4', video_type='storage', mobile_video_id=f'tutorials/mobile/{f}.mp4', mobile_video_type='storage', duration_minutes=12, order_index=0, is_active=True, recorded_at='@now-10d'))
    subs.append(dict(episode_id=eid, language_code='pt-BR', label='Português', format='vtt', content=VTT, is_default=True, order_index=0))
    res.append(dict(episode_id=eid, title='Guia Técnico: ' + t, description='O assunto da aula, por escrito.', resource_type='link', url='https://www.dominex.app/guia-tecnico', order_index=0))

CAT = {
 'domiflix_learning_paths': [dict(id=PATH, slug='tutoriais-do-sistema', title='Tutoriais do sistema', description='Aprenda a Dominex na ordem certa, da base às funções do seu plano.', cover_url='/images/blog/covers/gestao-produtividade-equipes-de-campo.jpg', is_onboarding=True, is_active=True, intro_gate_enabled_at='@now-30d', order_index=0)],
 'domiflix_titles': titles, 'domiflix_title_modules': tmod, 'domiflix_episodes': eps,
 'domiflix_episode_subtitles': subs, 'domiflix_episode_resources': res,
 # SEMENTE BASE (vale para TODA aula): sem trilha semeada a 1.38.19 abre a introdução escura bloqueando o app; com a introdução
 # confirmada por todos os usuários das sementes base, as outras aulas abrem normal. O T0 v2 usa o estado de primeiro acesso (Diego).
 'domiflix_intro_acknowledgements': [dict(user_id='@id:user.' + u, company_id='@id:company.glacial', learning_path_id=PATH, episode_id='e0000000-0000-4000-8000-000000000000', completed_at='@now-300d', understood_at='@now-300d') for u in ('camila','rafael','bruno','julia','lucas','marina','paulo')],
}
BASE = os.path.join(OUT, '..', '..', 'seeds', 'gen-03-domiflix.json')
json.dump(CAT, open(BASE, 'w'), ensure_ascii=False, indent=1)
w('catalogo', {
 'subscription_modules': [dict(code=c, name=n, description=n, price=p, type=ty, sort_order=s, is_active=True) for c, n, p, ty, s in mods],
 '_patch': {
  'subscription_plans': [dict(match=dict(code='avancado'), set=dict(included_modules=['basic','customer_portal','pricing_advanced','video_questions','contracts','rh'], price=547, max_users=10))],
  'company_modules': [dict(match=dict(module_code=c), set=dict(company_id='00000000-0000-4000-8000-0000000000ff')) for c in ('crm','nfe','cobrancas','whatsapp','pdv','finance_advanced','white_label')],
 }})
# progresso da Camila: 3 aulas da Formação básica; parada há 4 dias (lembrete "soft")
cam = '@id:user.camila'
prog = [dict(user_id=cam, company_id='@id:company.glacial', episode_id=f'e0000000-0000-4000-8000-00000000000{n}', title_id=f'd0000000-0000-4000-8000-00000000000{n}', completed=True, watched_at='@now-4d', progress_seconds=600, duration_seconds=600, last_progress_at='@now-4d') for n in (0,1,3)]
w('progresso-camila', {'domiflix_user_progress': prog,
 'domiflix_user_onboarding': [dict(user_id=cam, company_id='@id:company.glacial', window_started_at='@now-12d', last_progress_at='@now-4d')]})
comp_base = dict(learning_onboarding_started_at='@now-12d', subscription_plan='avancado', subscription_value=547, max_users=10)
w('conta-teste', {'_patch': {'companies': [dict(match=dict(name='Glacial Cold Brasil'), set=dict(comp_base, subscription_status='testing', subscription_expires_at='@now+3d', billing_cycle='monthly'))]}})
w('conta-contratada', {'_patch': {'companies': [dict(match=dict(name='Glacial Cold Brasil'), set=dict(comp_base, subscription_status='active'))]}})
w('lembrete-dispensado', {'_patch': {'domiflix_user_onboarding': [dict(match=dict(user_id='@id:user.camila'), set=dict(dismissed_until='@today'))]}})
pg = [dict(company_id='@id:company.glacial', amount=547, status='CONFIRMED', billing_type=bt, billing_cycle='monthly', payment_method=bt.lower(), type=ty, created_at=f'@now-{d}d', paid_at=f'@now-{d}d', due_date=f'@today-{d}d', updated_at=f'@now-{d}d') for d, bt, ty in ((84, 'CREDIT_CARD', 'primeira_venda'), (54, 'CREDIT_CARD', 'renovacao'), (24, 'CREDIT_CARD', 'renovacao'))]
w('pagamentos', {'subscription_payments': pg})
w('conta-anual', {'_patch': {'companies': [dict(match=dict(name='Glacial Cold Brasil'), set=dict(billing_cycle='yearly'))]}})
w('usuario-novo', {'profiles': [dict(id='@id:profile.diego', user_id='@id:user.diego', company_id='@id:company.glacial', full_name='Diego Martins', email='diego.martins@glacialcold.example', phone='(21) 3000-1008', is_active=True, navigation_style='sidebar', terms_accepted_at='@now', created_at='@now')],
 'user_roles': [dict(id='@id:role.diego', user_id='@id:user.diego', role='gestor')]})
print('ok', os.listdir(OUT))
