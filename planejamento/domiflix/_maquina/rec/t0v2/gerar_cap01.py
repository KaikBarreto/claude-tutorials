#!/usr/bin/env python3
"""Roteiro do robô do capítulo 1 (Como funcionam os tutoriais) do T0 v2, cronometrado pela voz real (narracao/cap01.json).
Gera cap01-d.json (computador) e cap01-p.json (celular). Grava com: gravar_cap.sh cap01-d  (nome de saída t0v2-cap01)."""
import json, os, re
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gerar.py')).read().split("tela('R01'")[0])  # helpers: COBRIR, H, C, SC, EV, P, W, IDLE, G, AUL...
N = json.load(open('/home/claude/domiflix/t0v2/narracao/cap01.json'))
def t(linha, palavra, n=1):
    k = 0
    for w in N['words']:
        if w['linha'] == linha and re.sub(r'[.,“”]', '', w['w']).lower() == palavra.lower():
            k += 1
            if k == n: return w['s']
    raise SystemExit(f'palavra {linha}/{palavra}')
SEED = lambda nome: EV(f"fetch('http://127.0.0.1:54321/__dev/seed',{{method:'POST',headers:{{'content-type':'application/json'}},body:JSON.stringify({{files:['t0v2/{nome}']}})}}).then(()=>{{{REFETCH}}})", f'estado {nome}')
REFETCH = ("const root=document.getElementById('root');const key=Object.keys(root).find(k=>k.startsWith('__reactContainer$'));const st=[root[key]];let n=0;"
 "while(st.length&&n++<20000){const f=st.pop();if(!f)continue;const p=f.memoizedProps;if(p&&p.client&&typeof p.client.refetchQueries==='function'){p.client.invalidateQueries();p.client.refetchQueries({type:'active'});break;}if(f.sibling)st.push(f.sibling);if(f.child)st.push(f.child);}")
def at(s, step, label=None):
    step = dict(step); step['at'] = round(s, 2)
    if label: step['label'] = label
    return step
marks = [{'do': 'mark', 'name': f'L{l["i"] + 1}', 'at': round(l['s'], 2)} for l in N['linhas']]
CRM_AULA = AUL(CRM); SERV_AULA = AUL(SERV)
d = [
 at(5.1, H('Formação básica', 0.8, 'selo Formação básica')),
 at(9.2, SC({'text': 'Gestão de Contratos e PMOC', 'within': 'main'}), 'desce até os módulos do plano'),
 at(11.9, H('Tem no seu plano', 0.8, 'selo Tem no seu plano')),
 at(13.0, H('Na sequência do seu plano', 0.7, 'Na sequência do seu plano')),
 at(14.0, SEED('conta-contratada'), 'conta contratada (bastidor)'),
 at(14.5, SC({'text': 'CRM e Kanban', 'within': 'main'}), 'desce até os outros módulos'),
 at(19.9, H('Não tem no seu plano', 0.8, 'selo Não tem no seu plano')),
 at(21.2, C({'text': 'CRM e Kanban', 'within': 'main', 'nth': 1}, 'abre a aula do módulo')),
 at(22.9, W('Consultar fora da ordem?', 8)),
 at(23.3, H('Consultar esta aula', 0.6, 'Consultar esta aula')),
 at(23.9, SEED('conta-teste'), 'volta ao teste (bastidor)'),
 at(24.2, C('Consultar esta aula', 'clica Consultar esta aula')),
 at(25.2, H('Escolher meu plano', 1.0, 'botão Escolher meu plano')),
 at(29.6, {'do': 'scroll', 'by': 300, 'duration': 0.6}),
 at(32.2, H('Materiais e extras', 0.6, 'Materiais e extras')),
 at(34.4, H('Sua trilha', 0.8, 'Sua trilha')),
 at(36.9, H({'role': 'button', 'name': 'Aula 5.1: Ordens de Serviço, agenda, equipes e mapa ao vivo'}, 0.8, 'próxima aula')),
 at(38.6, EV("window.history.pushState({}, '', '/dashboard'); window.dispatchEvent(new PopStateEvent('popstate')); 'ok'", 'volta ao sistema')),
 at(40.4, C('Camila Duarte', 'cartão da conta')),
 at(42.0, H('Tutoriais | Domiflix', 1.0, 'Tutoriais | Domiflix')),
 at(44.0, P(0.5)),
]
pre = ['/dashboard', '/domiflix', CRM_AULA, SERV_AULA]
base = {'title': 'T0 v2 · cap01 · Como funcionam os tutoriais', 'seed': 't0v2-cap01', 'pace': 0.5, 'tail': 1.2, 'cps': 9,
        'seedExtra': SEEDS + ['t0v2/conta-teste', 't0v2/lembrete-dispensado'], 'prewarm': pre}
setup_d = [G('/dashboard'), IDLE, G('/domiflix?trilha=tutoriais-do-sistema'), W('Aprenda a usar a Dominex'), IDLE, EV(COBRIR), P(0.6)]
json.dump(dict(base, name='t0v2-cap01', setup=setup_d, steps=sorted(marks + d, key=lambda s: s['at'])), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cap01-d.json'), 'w'), ensure_ascii=False, indent=1)
# celular (opção b, 03/11): a gaveta "Ver trilha" abre atrás do player no app (z-index); nenhum toque nela. Página inicial no celular (lista de módulos na ordem
# Formação básica -> "Na sequência do seu plano" -> "Conheça este módulo") -> aula CRM e Kanban -> volta à trilha (progresso e próxima aula) -> menu
CLICK_JS = lambda t, exato=False: "[...document.querySelectorAll('button,a,[role=button]')].find(e=>e.innerText.trim()%s).click();'ok'" % (f"==='{t}'" if exato else f".startsWith('{t}')")
p = [
 at(5.3, H('Formação básica: 3 de 5', 0.9, 'Formação básica')),
 at(8.8, SC('Na sequência do seu plano')),
 at(11.9, H('Na sequência do seu plano', 0.8, 'Na sequência do seu plano')),
 at(14.4, SC('Conheça este módulo')),
 at(17.3, H('Conheça este módulo', 0.9, 'Conheça este módulo')),
 at(21.0, C({'text': 'Conheça este módulo', 'nth': 0}, 'abre a aula do módulo')),
 at(22.7, W('Consultar fora da ordem?', 8)),
 at(24.0, EV(CLICK_JS('Consultar esta aula'), 'clica Consultar esta aula')),
 at(25.3, H('Não tem no seu plano', 0.8, 'selo Não tem no seu plano')),
 at(26.0, SEED('conta-teste'), 'volta ao teste (bastidor)'),
 at(26.7, H('Escolher meu plano', 0.9, 'botão Escolher meu plano')),
 at(29.6, {'do': 'scroll', 'by': 380, 'duration': 0.8}),
 at(32.2, H('Materiais e extras', 0.7, 'Materiais e extras')),
 at(33.9, EV("window.history.pushState({}, '', '/domiflix?trilha=tutoriais-do-sistema'); window.dispatchEvent(new PopStateEvent('popstate')); 'ok'", 'volta à trilha')),
 at(34.3, W('Trilha do seu plano', 10)),
 at(34.6, EV("window.scrollTo(0, 0); 'ok'")),
 at(34.9, H('Trilha do seu plano', 0.9, 'Trilha do seu plano 43%')),
 at(36.3, {'do': 'scroll', 'by': 760, 'duration': 0.5, 'point': {'x': 195, 'y': 520}, 'after': 100}),
 at(37.6, H('Próxima recomendada', 0.9, 'Próxima recomendada')),
 at(38.9, EV("window.history.pushState({}, '', '/dashboard'); window.dispatchEvent(new PopStateEvent('popstate')); 'ok'", 'volta ao sistema')),
 at(39.4, W('Menu', 10)),
 at(40.0, C('Menu', 'abre o Menu', noScroll=True)),
 at(42.0, SC('Tutoriais | Domiflix')),
 at(43.0, H('Tutoriais | Domiflix', 0.8, 'Tutoriais | Domiflix')),
 at(44.4, P(0.5)),
]
base_p = dict(base, seedExtra=[x for x in base['seedExtra'] if x != 't0v2/conta-teste'] + ['t0v2/conta-contratada'][:0] + ['t0v2/conta-contratada', 't0v2/pagamentos'][:1])
json.dump(dict(base_p, name='t0v2-cap01-p', device='phone', start={'x': 195, 'y': 600}, setup=setup_d, steps=sorted(marks + p, key=lambda s: s['at'])), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cap01-p.json'), 'w'), ensure_ascii=False, indent=1)
print('ok')
