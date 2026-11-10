#!/usr/bin/env python3
"""Roteiros do robô dos capítulos 2 a 6 do T0 v2 (cap0N-d.json computador, cap0N-p.json celular), cronometrados pela voz real.
Sem tarja. Só as janelas de tela real têm ação; as ilustrações cobrem o resto. Grava com: gravar_cap.sh cap02-d ..."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'gerar_cap01.py')).read()
exec(src.split("N = json.load")[0])            # helpers do gerar.py (H, C, SC, EV, P, W, IDLE, G, AUL...) e imports
REFETCH = ("const root=document.getElementById('root');const key=Object.keys(root).find(k=>k.startsWith('__reactContainer$'));const st=[root[key]];let n=0;"
 "while(st.length&&n++<20000){const f=st.pop();if(!f)continue;const p=f.memoizedProps;if(p&&p.client&&typeof p.client.refetchQueries==='function'){p.client.invalidateQueries();p.client.refetchQueries({type:'active'});break;}if(f.sibling)st.push(f.sibling);if(f.child)st.push(f.child);}")
SEED = lambda nome: EV(f"fetch('http://127.0.0.1:54321/__dev/seed',{{method:'POST',headers:{{'content-type':'application/json'}},body:JSON.stringify({{files:['t0v2/{nome}']}})}}).then(()=>{{{REFETCH}}})", f'estado {nome}')
def at(s, step, label=None):
    step = dict(step); step['at'] = round(s, 2)
    if label: step['label'] = label
    return step
PUSH = lambda rota, lab=None: EV(f"window.history.pushState({{}}, '', '{rota}'); window.dispatchEvent(new PopStateEvent('popstate')); 'ok'", lab)
def gera(nn, nome, estado, d, p, setup_d, setup_p=None, user=None, extra=(), prewarm=('/dashboard', '/domiflix'), pace=0.5):
    N = json.load(open(f'/home/claude/domiflix/t0v2/narracao/cap{nn:02d}.json'))
    marks = [{'do': 'mark', 'name': f'L{l["i"] + 1}', 'at': round(l['s'], 2)} for l in N['linhas']]
    fim = at(N['dur'], P(0.5))
    base = {'title': f'T0 v2 · cap{nn:02d} · {nome}', 'seed': f't0v2-cap{nn:02d}', 'pace': pace, 'tail': 1.2, 'cps': 9,
            'seedExtra': SEEDS + [ESTADO[estado]] + (['t0v2/pagamentos'] if estado == 'contratada' else []) + list(extra) + ['t0v2/lembrete-dispensado'],
            'prewarm': list(prewarm)}
    if user: base['user'] = user
    for dev, st, su in (('d', d, setup_d), ('p', p, setup_p or setup_d)):
        s = dict(base, name=f't0v2-cap{nn:02d}' + ('-p' if dev == 'p' else ''), setup=su, steps=sorted(marks + st + [fim], key=lambda x: x['at']))
        if dev == 'p': s['device'] = 'phone'; s['start'] = {'x': 195, 'y': 600}
        json.dump(s, open(os.path.join(HERE, f'cap{nn:02d}-{dev}.json'), 'w'), ensure_ascii=False, indent=1)
TRILHA = [G('/dashboard'), IDLE, G('/domiflix?trilha=tutoriais-do-sistema'), W('Trilha do seu plano'), IDLE, P(0.6)]
# cap02: só a primeira linha é tela real (R02)
gera(2, 'O seu progresso', 'teste',
  d=[at(0.3, H('Trilha do seu plano', 1.2, 'Trilha do seu plano')), at(2.7, H('Formação básica 60%', 0.9, 'Formação básica %'))],
  p=[at(0.3, H('Trilha do seu plano', 1.2, 'Trilha do seu plano'))], setup_d=TRILHA)
# cap03: aula (suporte) -> [ilustração da mensagem] -> Guia Técnico -> menu da conta
AULA = lambda: [G('/dashboard'), IDLE, G(AUL(CONTR)), W('Tirar dúvidas com o suporte'), IDLE, EV(WA), P(0.6)]
VOLTA_D = [at(30.31, EV("location.href='/dashboard'; 'ok'")), at(30.6, W('Camila', 20)), at(32.9, EV(WA)), at(34.4, C('Camila Duarte', 'cartão da conta')),
           at(37.5, H('Falar com o Suporte', 0.6, 'Falar com o Suporte')), at(39.2, C('Falar com o Suporte', 'clica Falar com o Suporte'))]
VOLTA_P = [at(30.31, EV("location.href='/dashboard'; 'ok'")), at(30.6, IDLE), at(30.8, EV(WA)), at(34.4, C('Menu', 'abre o Menu', noScroll=True)),
           at(36.4, SC('Falar com o Suporte')), at(37.5, H('Falar com o Suporte', 0.6, 'Falar com o Suporte')), at(39.2, C('Falar com o Suporte', 'clica Falar com o Suporte', noScroll=True))]
GUIA = [at(19.6, EV("location.href='/guia-tecnico/'; 'ok'")), at(20.4, W('Guia Técnico', 20)), at(23.8, H({'placeholder': 'Buscar no guia…'}, 1.0, 'busca do guia'))]
SUP = [at(10.2, SC('Tirar dúvidas com o suporte')), at(11.7, H('Tirar dúvidas com o suporte', 0.6, 'botão Tirar dúvidas com o suporte')),
       at(12.9, C('Tirar dúvidas com o suporte', 'clica Tirar dúvidas com o suporte'))]
gera(3, 'Quando bater uma dúvida', 'contratada', d=SUP + GUIA + VOLTA_D, p=SUP + GUIA + VOLTA_P, setup_d=AULA(), prewarm=('/dashboard', '/domiflix', AUL(CONTR)), pace=0.4)
# cap04: Assinatura
ASS_SETUP = [G('/dashboard'), W('Camila', 30), IDLE, P(0.6)]
ass_steps = lambda dev: [
  at(1.1, C('Camila Duarte', 'cartão da conta') if dev == 'd' else C('Menu', 'abre o Menu', noScroll=True)),
  at(2.2, C({'text': 'Assinatura', 'exact': True}, 'abre Assinatura', noScroll=True) if dev == 'p' else C({'text': 'Assinatura', 'exact': True}, 'abre Assinatura')),
  at(3.3, PUSH('/assinatura')), at(3.8, W('Histórico de pagamentos', 20)),
  at(5.6, H('Ativa', 0.7, 'status')), at(6.5, H('Plano Avançado', 0.7, 'plano')), at(7.2, H('Vencimento', 0.7, 'vencimento')), at(8.3, H('Valor mensal', 0.7, 'valor')),
  at(9.5, SC('Uso da conta'), 'uso da conta'), at(10.6, SC('Histórico de pagamentos'), 'histórico'),
  at(11.9, SEED('conta-anual'), 'plano anual (bastidor)'), at(12.4, SC('Pagar Agora')),
  at(13.9, H('Pagar Agora', 1.0, 'botão Pagar Agora')), at(15.9, H('PIX', 0.5, 'Pix')), at(16.6, H('Boleto', 0.5, 'Boleto')), at(17.2, H('Cartão', 0.5, 'Cartão')),
  at(18.6, H('20% de desconto no plano anual', 1.2, '20% de desconto'))]
gera(4, 'A sua assinatura', 'contratada', d=ass_steps('d'), p=ass_steps('p'), setup_d=ASS_SETUP, prewarm=('/dashboard', '/assinatura'))
# cap05: Gerenciar Meu Plano (R18)
ASS2 = [G('/dashboard'), IDLE, G('/assinatura'), W('Histórico de pagamentos'), IDLE, P(0.6)]
DLG = '[role=dialog]'
ger = lambda by, pt=None: [at(8.6, SC('Gerenciar Meu Plano')), at(11.8, C('Gerenciar Meu Plano', 'abre Gerenciar Meu Plano')), at(12.9, W('Personalizado', 15)),
  at(14.5, H({'role': 'tab', 'name': 'Planos Prontos'}, 0.8, 'aba Planos Prontos')), at(15.8, C({'role': 'tab', 'name': 'Personalizado'}, 'aba Personalizado')),
  at(16.6, C({'text': 'Cobranças online', 'within': DLG}, 'marca Cobranças online', noScroll=True)), at(17.3, C({'text': 'CRM / Kanban', 'within': DLG}, 'marca CRM / Kanban', noScroll=True)),
  at(18.0, dict({'do': 'scroll', 'by': by, 'duration': 0.6}, **({'point': pt} if pt else {}))),
  at(18.7, C({'selector': DLG + ' button:has(svg.lucide-plus)', 'nth': 'last'}, 'sobe usuários', noScroll=True)), at(19.3, C({'selector': DLG + ' button:has(svg.lucide-plus)', 'nth': 'last'}, 'sobe usuários 2', noScroll=True))]
gera(5, 'Quando a empresa cresce', 'contratada', d=ger(500), p=ger(380, {'x': 195, 'y': 520}), setup_d=ASS2, prewarm=('/dashboard', '/assinatura'), pace=0.4)
# cap06: confirmação (R12), usuário novo
GATE = [G('/dashboard'), W('Primeiro passo'), IDLE]
f6 = lambda dev: ([]) + [at(0.9, W('Confirmar e começar a primeira aula', 40)),
  at(14.2, SC('Assisti ao vídeo até o final e entendi os combinados.')),
  at(14.9, C({'role': 'checkbox'}, 'marca a caixa')), at(16.9, C('Confirmar e começar a primeira aula', 'botão Confirmar e começar a primeira aula'))]
gera(6, 'Os combinados', 'teste', d=f6('d'), p=f6('p'), setup_d=GATE, user=DIEGO, prewarm=('/dashboard',))
print('ok')
