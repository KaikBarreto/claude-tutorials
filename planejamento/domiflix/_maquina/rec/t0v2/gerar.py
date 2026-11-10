#!/usr/bin/env python3
"""Gera os roteiros do robô das telas R01..R18 do T0 v2 (computador 'd' e celular 'p'). Uso: python3 gerar.py"""
import json, os
D = os.path.dirname(os.path.abspath(__file__))
SEEDS = ['t0v2/catalogo', 't0v2/progresso-camila', 't0v2/usuario-novo']
ESTADO = {'teste': 't0v2/conta-teste', 'contratada': 't0v2/conta-contratada'}
DIEGO = 'diego.martins@glacialcold.example'
# Kaik (3/11): nenhuma tarja em nada; valores de demonstração aparecem como estão. O cobrir() foi retirado.
COBRIR = "'sem tarja'"
def P(s): return {'do': 'pause', 'seconds': s}
def W(t, to=30): return {'do': 'waitFor', 'text': t, 'timeout': to}
IDLE = {'do': 'waitFor', 'idle': True}
def G(u): return {'do': 'goto', 'url': u}
def H(t, s=0.8, label=None, **k): return dict({'do': 'hover', 'target': t, 'seconds': s, 'optional': True, 'timeout': 3, 'label': label or (t if isinstance(t, str) else t.get('text') or t.get('name'))}, **k)
def C(t, label=None, **k): return dict({'do': 'click', 'target': t, 'optional': True, 'timeout': 8, 'label': label or (t if isinstance(t, str) else t.get('text') or t.get('name'))}, **k)
def SC(t): return {'do': 'scroll', 'target': t, 'optional': True, 'timeout': 8}
def EV(js, label=None): return {'do': 'eval', 'js': js, **({'label': label} if label else {})}
AUL = lambda slug, n=1: f'/domiflix/assistir/{slug}/{n}?trilha=tutoriais-do-sistema'
SERV, CONTR, NF, CRM = 'servicos-tarefas-e-checklists', 'gestao-de-contratos-e-pmoc', 'emissao-de-notas-fiscais', 'crm-e-kanban'
WA = "(() => { window.__wa = null; window.open = (u) => { window.__wa = u; return null; }; return 'stub'; })()"
LERWA = "(() => { const a = [...document.querySelectorAll('a')].find(x => x.href.startsWith('https://wa.me')); if (!a) return 'sem link'; try { return decodeURIComponent(a.href.split('text=')[1] || ''); } catch (e) { return a.href; } })()"

def tela(rid, nome, d=None, p=None, estado='teste', user=None, anon=False, dispensa=False, anual=False):
    for dev, st in (('d', d), ('p', p)):
        if st is None: continue
        s = {'name': f'{rid}-{dev}', 'title': f'T0 v2 · {rid} · {nome} ({"computador 1280x800" if dev == "d" else "celular 390x844"})',
             'seed': f't0v2-{rid}', 'pace': 0.6, 'tail': 1.2, 'cps': 9,
             'seedExtra': SEEDS + [ESTADO[estado]] + (['t0v2/pagamentos'] if estado == 'contratada' else []) + (['t0v2/conta-anual'] if anual else []) + (['t0v2/lembrete-dispensado'] if dispensa else []),
             'prewarm': st.get('prewarm', ['/dashboard', '/domiflix']), 'setup': st['setup'], 'steps': [{'do': 'mark', 'name': 'L1', 'at': 0}] + st['steps']}
        if dev == 'p': s['device'] = 'phone'; s['start'] = {'x': 195, 'y': 600}
        if user: s['user'] = user
        if anon: s['anonymous'] = True
        if not anon: s['setup'] = s['setup'][:1] + [EV(COBRIR)] + s['setup'][1:] if False else s['setup']
        json.dump(s, open(os.path.join(D, f'{rid}-{dev}.json'), 'w'), ensure_ascii=False, indent=1)

def abre(url, esperar, extra=()):  # setup padrão: entra no sistema, abre a rota, cobre valores
    return [G('/dashboard'), IDLE, G(url), W(esperar), IDLE, EV(COBRIR), P(0.6)] + list(extra)

tela('R01', 'Introdução obrigatória', user=DIEGO,
  d={'prewarm': ['/dashboard'], 'setup': [G('/dashboard'), W('Primeiro passo'), IDLE], 'steps': [P(2.5), H('Antes de usar o sistema', 1.0), P(3), H('Bem-vindo, Diego', 1.0), P(4)]},
  p={'prewarm': ['/dashboard'], 'setup': [G('/dashboard'), W('Primeiro passo'), IDLE], 'steps': [P(2.5), {'do': 'scroll', 'by': 420, 'duration': 1.4}, P(3), {'do': 'scroll', 'by': 420, 'duration': 1.4}, P(3)]})
tela('R02', 'Trilha do seu plano (barra de progresso)',
  d={'setup': abre('/domiflix?trilha=tutoriais-do-sistema', 'Trilha do seu plano'), 'steps': [P(1.5), H('Trilha do seu plano', 1.2), P(2.5), H('Formação básica 60%', 0.8, 'Formação básica %', ), P(2.5)]},
  p={'setup': abre('/domiflix?trilha=tutoriais-do-sistema', 'Trilha do seu plano'), 'steps': [P(2.5), H('Trilha do seu plano', 0.8), P(3)]})
tela('R03', 'Página Aprenda a usar a Dominex: Formação básica',
  d={'setup': abre('/domiflix?trilha=tutoriais-do-sistema', 'Aprenda a usar a Dominex'), 'steps': [P(2.0), H('Formação básica', 0.9, 'selo Formação básica', **{}), P(2.0), {'do': 'scroll', 'by': 360, 'duration': 1.5}, H('Próxima aula recomendada', 0.8), P(2.5)]},
  p={'setup': abre('/domiflix?trilha=tutoriais-do-sistema', 'Aprenda a usar a Dominex'), 'steps': [P(2), {'do': 'scroll', 'by': 560, 'duration': 1.6}, P(2.5), {'do': 'scroll', 'by': 420, 'duration': 1.4}, P(2.5)]})
tela('R04', 'Módulos do plano: selo verde Tem no seu plano', estado='contratada',
  d={'setup': abre('/domiflix?trilha=tutoriais-do-sistema', 'Aprenda a usar a Dominex'), 'steps': [SC({'text': 'Gestão de Contratos e PMOC', 'within': 'main'}), P(1.2), H('Tem no seu plano', 1.2, 'selo Tem no seu plano'), P(2.5), H('Na sequência do seu plano', 0.8), P(2.5)]},
  p={'setup': abre(AUL(SERV), 'Ver trilha'), 'steps': [C('Ver trilha', 'abre a gaveta Ver trilha'), P(1.5), SC('Gestão de Contratos e PMOC'), P(1.5), H('Tem no seu plano', 1.0, 'selo Tem no seu plano'), P(2.5)]})
tela('R05', 'Outros módulos: selo vermelho Não tem no seu plano', estado='contratada',
  d={'setup': abre('/domiflix?trilha=tutoriais-do-sistema', 'Aprenda a usar a Dominex'), 'steps': [SC({'text': 'CRM e Kanban', 'within': 'main'}), P(1.2), H('Não tem no seu plano', 1.2, 'selo Não tem no seu plano'), P(2.0), H('Conheça este módulo', 0.8), P(1.5), C({'text': 'CRM e Kanban', 'within': 'main', 'nth': 1}, 'abre a aula do módulo'), W('Consultar fora da ordem?', 8), P(2.0), H('Consultar esta aula', 0.8), P(1.5)]},
  p={'setup': abre(AUL(SERV), 'Ver trilha'), 'steps': [C('Ver trilha', 'abre a gaveta Ver trilha'), P(1.5), SC('Conheça outros módulos'), P(1.5), H('Não tem no seu plano', 1.0, 'selo Não tem no seu plano'), P(2.5)]})
bloco = lambda: abre(AUL(NF), 'Conheça agora')
tela('R06', 'Bloco de contratar (Conheça agora)',
  d={'prewarm': ['/dashboard', '/domiflix'], 'setup': bloco(), 'steps': [SC('Conheça agora. Ative quando fizer sentido.'), P(1.5), H('Escolher meu plano', 1.2, 'botão Escolher meu plano'), P(3)]},
  p={'prewarm': ['/dashboard', '/domiflix'], 'setup': bloco(), 'steps': [SC('Conheça agora. Ative quando fizer sentido.'), P(1.5), H('Escolher meu plano', 1.2, 'botão Escolher meu plano'), P(3)]})
aula = lambda: abre(AUL(SERV), 'Materiais e extras')
tela('R07', 'Página da aula (vídeo, legenda, descrição, materiais)',
  d={'setup': aula(), 'steps': [P(3), H({'text': 'Português', 'nth': 0}, 1.0, 'menu Legendas'), P(1.5), SC('Materiais e extras'), H('Materiais e extras', 1.0), P(3)]},
  p={'setup': aula(), 'steps': [P(3.5), {'do': 'scroll', 'by': 420, 'duration': 1.4}, P(2.5), SC('Materiais e extras'), P(2.5)]})
tela('R08', 'Sua trilha (progresso e próxima aula)',
  d={'setup': aula(), 'steps': [P(1.5), H('Sua trilha', 1.0), P(2), H('Formação básica 60%', 0.8, 'Formação básica %'), P(2), H({'role': 'button', 'name': 'Aula 4.1: Serviços, tarefas e checklists'}, 1.0, 'aula atual'), P(2.5)]},
  p={'setup': aula(), 'steps': [P(1.2), C('Ver trilha', 'abre a gaveta Ver trilha'), P(3.5)]})
cont = lambda: abre(AUL(CONTR), 'Tirar dúvidas com o suporte')
tela('R09', 'Botão Tirar dúvidas com o suporte',
  d={'setup': cont(), 'steps': [P(1.5), SC('Tirar dúvidas com o suporte'), H('Tirar dúvidas com o suporte', 1.4, 'botão Tirar dúvidas com o suporte'), P(3)]},
  p={'setup': cont(), 'steps': [P(1.5), SC('Tirar dúvidas com o suporte'), H('Tirar dúvidas com o suporte', 1.4, 'botão Tirar dúvidas com o suporte'), P(3)]})
tela('R10', 'Mensagem pronta para o suporte (texto lido do app)',
  d={'setup': cont() + [EV(WA)], 'steps': [SC('Tirar dúvidas com o suporte'), H('Tirar dúvidas com o suporte', 1.2, 'o botão'), EV(LERWA, 'texto da mensagem'), P(2.5)]},
  p={'setup': cont() + [EV(WA)], 'steps': [SC('Tirar dúvidas com o suporte'), H('Tirar dúvidas com o suporte', 1.2, 'o botão'), EV(LERWA, 'texto da mensagem'), P(2.5)]})
tela('R11', 'Lembrete da trilha no topo do sistema',
  d={'prewarm': ['/dashboard'], 'setup': [G('/dashboard'), W('vamos retomar de onde você parou'), IDLE], 'steps': [P(2.5), H('Continuar trilha', 1.0), P(3.5)]},
  p={'prewarm': ['/dashboard'], 'setup': [G('/dashboard'), W('vamos retomar de onde você parou'), IDLE], 'steps': [P(2.5), H('Continuar tutorial', 1.0), P(3.5)]})
tela('R12', 'Confirmação no fim do T0', user=DIEGO,
  d={'prewarm': ['/dashboard'], 'setup': [G('/dashboard'), W('Primeiro passo'), IDLE], 'steps': [{'do': 'waitFor', 'text': 'Confirmar e começar a primeira aula', 'timeout': 40, 'label': 'vídeo terminou'}, P(1.2), C({'role': 'checkbox'}, 'marca a caixa'), P(1.2), C('Confirmar e começar a primeira aula', 'botão Confirmar e começar a primeira aula'), P(4)]},
  p={'prewarm': ['/dashboard'], 'setup': [G('/dashboard'), W('Primeiro passo'), IDLE], 'steps': [{'do': 'waitFor', 'text': 'Confirmar e começar a primeira aula', 'timeout': 40, 'label': 'vídeo terminou'}, SC('Assisti ao vídeo até o final e entendi os combinados.'), P(1.2), C({'role': 'checkbox'}, 'marca a caixa'), P(1.2), C('Confirmar e começar a primeira aula', 'botão Confirmar e começar a primeira aula'), P(4)]})
conta = lambda alvo: {'prewarm': ['/dashboard'], 'setup': [G('/dashboard'), W('Camila'), IDLE], 'steps': [P(1.5), C('Camila Duarte', 'cartão da conta'), P(1.2), H(alvo, 1.2, alvo), P(2.5)]}
conta_p = lambda alvo: {'prewarm': ['/dashboard'], 'setup': [G('/dashboard'), IDLE], 'steps': [P(1.5), C('Menu', 'abre o Menu'), P(1.5), SC(alvo), H(alvo, 1.2, alvo), P(2.5)]}
tela('R13', 'Menu da conta: Tutoriais | Domiflix', d=conta('Tutoriais | Domiflix'), p=conta_p('Tutoriais | Domiflix'), dispensa=True)
tela('R14', 'Menu da conta: Falar com o Suporte', d=conta('Falar com o Suporte'), p=conta_p('Falar com o Suporte'), dispensa=True)
guia = {'prewarm': ['/guia-tecnico/'], 'setup': [G('/guia-tecnico/'), W('Guia Técnico'), IDLE], 'steps': [P(2.5), H({'placeholder': 'Buscar no guia…'}, 1.0, 'busca do guia'), P(3)]}
tela('R15', 'Guia Técnico (página pública)', d=guia, p=guia, anon=True)
ass = lambda extra: abre('/assinatura', 'Histórico de pagamentos', extra)
tela('R16', 'Assinatura', estado='contratada', dispensa=True, d={'setup': ass([]), 'steps': [P(2), H('Plano', 0.8), P(1.5), H('Vencimento', 0.8), P(1.5), SC('Uso da conta'), P(1.5), SC('Histórico de pagamentos'), P(2.5)]},
  p={'setup': ass([]), 'steps': [P(2), {'do': 'scroll', 'by': 520, 'duration': 1.5}, P(2), {'do': 'scroll', 'by': 520, 'duration': 1.5}, P(2.5)]})
tela('R17', 'Assinatura: Pagar Agora e formas de pagamento', estado='contratada', dispensa=True, anual=True, d={'setup': ass([]), 'steps': [SC('Pagar Agora'), H('Pagar Agora', 1.2, 'botão Pagar Agora'), P(1.5), H('20% de desconto no plano anual', 1.0), P(2.5)]},
  p={'setup': ass([]), 'steps': [SC('Pagar Agora'), H('Pagar Agora', 1.2, 'botão Pagar Agora'), P(2.5)]})
tela('R18', 'Gerenciar Meu Plano', estado='contratada', dispensa=True, d={'setup': ass([]), 'steps': [SC('Gerenciar Meu Plano'), C('Gerenciar Meu Plano', 'abre Gerenciar Meu Plano'), W('Personalizado', 15), P(1.5), C({'role': 'tab', 'name': 'Personalizado'}, 'aba Personalizado'), P(2), {'do': 'scroll', 'by': 500, 'duration': 1.5}, P(2.5)]},
  p={'setup': ass([]), 'steps': [SC('Gerenciar Meu Plano'), C('Gerenciar Meu Plano', 'abre Gerenciar Meu Plano'), W('Personalizado', 15), P(1.5), C({'role': 'tab', 'name': 'Personalizado'}, 'aba Personalizado'), P(2), {'do': 'scroll', 'by': 520, 'duration': 1.5}, P(2.5)]})
print(sorted(f for f in os.listdir(D) if f.endswith('.json')))
