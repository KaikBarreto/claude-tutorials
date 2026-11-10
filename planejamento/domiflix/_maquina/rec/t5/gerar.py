#!/usr/bin/env python3
"""T5 · gera rec/t5/cap00..cap17.json (roteiros do robô) a partir da voz pronta (t5/narracao/capNN.json).

Os `at` saem da palavra que anuncia cada passo (A(linha, palavra, folga)): o clique "pousa" ~1 s depois do início do
passo, então `at` = início da palavra - folga. Rodar de qualquer pasta: `python3 rec/t5/gerar.py [NN ...]`.
Depois de gerar, confira com `node rec/record.mjs rec/t5/capNN.json --check`.
A cadeia de sementes vem de rec/t5/cadeia.json (gerado por rec/t5/semear.py): [t3, t1, t4, t5/inicio] + o último apos-capNN.
"""
import json, os, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
NARR = os.path.normpath(os.path.join(HERE, '..', '..', 't5', 'narracao'))

BASE = json.load(open(os.path.join(HERE, 'cadeia.json'), encoding='utf8'))['inicio'] + ['t5/g1-trilha', 't5/g2-vazias']  # 1.38.19: trilha sem onboarding + tabelas vazias
# estado de partida de cada capítulo (último apos-capNN que existe; só os capítulos que mudam o banco geram um)
SEMENTE = {0: None, 1: None, 2: None, 3: None, 4: None, 5: None, 6: 'apos-cap05', 7: 'apos-cap06', 8: 'apos-cap07', 9: 'apos-cap07',
           10: 'apos-cap09', 11: 'apos-cap09', 12: 'apos-cap09', 13: 'apos-cap09', 14: 'apos-cap13', 15: 'apos-cap14',
           16: 'apos-cap15', 17: 'apos-cap15'}
# sementes extras só deste capítulo (não encadeiam)
EXTRA = {0: ['t5/cap00-painel'], 12: ['t5/tarefas-agenda'], 13: ['t5/tarefas-agenda']}

NOMES = ['Abertura', 'A tela de Ordens de Serviço', 'Abrindo uma nova OS', 'Orçamento e rascunho', 'Equipamentos e checklists',
         'Agendamento e detalhes', 'Recorrência', 'Acompanhando no Kanban', 'Status, filtros e busca', 'Concluir e faturar',
         'Chamados e relatório', 'Satisfação do cliente', 'As visões da Agenda', 'Criar e reagendar', 'Pausadas, busca e resumo',
         'Montando uma equipe', 'Onde está cada técnico', 'Recapitulando']


def norm(s):
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode().lower()
    return ''.join(ch for ch in s if ch.isalnum() or ch in '?')


class Cap:
    def __init__(s, n, pace=1.0, cps=9, start=(700, 420), prewarm=None, setup=None, user=None):
        s.n = n
        d = json.load(open(f'{NARR}/cap{n:02d}.json'))
        s.words, s.linhas, s.dur = d['words'], d['linhas'], d['dur']
        s.steps = []
        s.pace, s.cps, s.start = pace, cps, start
        s.prewarm = prewarm or ['/dashboard']
        s.setup = setup or []
        s.anchors = []
        s.pending = []
        s.user = user

    # ---- tempo
    def L(s, i):
        return round(s.linhas[i - 1]['s'], 2)

    def W(s, i, palavra, nth=0):
        q = norm(palavra)
        hits = [w for w in s.words if w['linha'] == i - 1 and norm(w['w']).startswith(q)]
        if len(hits) <= nth:
            raise SystemExit(f'cap{s.n:02d}: palavra "{palavra}" (#{nth}) não achada na linha {i}')
        return hits[nth]['s']

    def A(s, i, palavra, folga=1.0, nth=0):
        t = round(max(0.0, s.W(i, palavra, nth) - folga), 2)
        s.anchors.append((i, palavra, t))
        return t

    # ---- passos
    def flush(s, ate):
        keep = []
        for mt, mi in s.pending:
            if round(mt, 2) <= ate + 1e-9:
                s.steps.append({'do': 'mark', 'name': f'L{mi}', 'at': round(mt, 2)})
            else:
                keep.append((mt, mi))
        s.pending = keep

    def add(s, d):
        # as marcas Ln entram na ordem do tempo: antes do primeiro passo cujo `at` já é >= ao início da linha
        if d.get('at') is not None:
            for mt, mi in s.pending:  # passo que começaria até 0,25 s antes da linha começa junto com ela (a marca vem antes)
                if d['at'] < mt <= d['at'] + 0.25:
                    d['at'] = round(mt, 2)
            s.flush(d['at'])
        s.steps.append(d)
        return d

    def mark(s, i):
        t = s.L(i)
        if t <= 0:
            s.steps.append({'do': 'mark', 'name': f'L{i}', 'at': 0})
        else:
            s.pending.append((t, i))

    def _p(s, d, at, label, kw):
        if at is not None: d['at'] = at
        if label: d['label'] = label
        d.update(kw)
        return s.add(d)

    def click(s, target, at=None, label=None, **kw):
        return s._p({'do': 'click', 'target': target}, at, label, kw)

    def dblclick(s, target, at=None, label=None, **kw):
        return s._p({'do': 'dblclick', 'target': target}, at, label, kw)

    def hover(s, target, seconds=0.9, at=None, label=None, **kw):
        return s._p({'do': 'hover', 'target': target, 'seconds': seconds}, at, label, kw)

    def type(s, target, text, at=None, label=None, cps=None, **kw):
        d = {'do': 'type', 'target': target, 'text': text}
        if cps: d['cps'] = cps
        return s._p(d, at, label, kw)

    def select(s, target, option, at=None, label=None, **kw):
        return s._p({'do': 'select', 'target': target, 'option': option}, at, label, kw)

    def press(s, key, at=None, label=None, **kw):
        return s._p({'do': 'press', 'key': key}, at, label, kw)

    def scroll(s, target=None, at=None, label=None, **kw):
        d = {'do': 'scroll'}
        if target is not None: d['target'] = target
        return s._p(d, at, label, kw)

    def pause(s, seconds):
        return s.add({'do': 'pause', 'seconds': seconds})

    def waitfor(s, **kw):
        return s.add({'do': 'waitFor', **kw})

    def drag(s, target, to, at=None, label=None, **kw):
        return s._p({'do': 'drag', 'target': target, 'to': to}, at, label, kw)

    def ev(s, js, at=None, label=None, **kw):
        return s._p({'do': 'eval', 'js': js}, at, label, kw)

    def clicar_fixo(s, sel, ponto, at, label, ultimo=False, texto=None):
        """Botão fixo do app fora da faixa y 96..730 (ex.: o Fechar do cabeçalho de uma janela): o `click` do robô tentaria rolar
        em vão e atrasaria 2 a 6 s (lição do T1). Leva o cursor com `scroll by 0 point`, registra o rect com `type noClick` e
        clica por `eval`. `at` = instante do clique; o cursor parte 0,9 s antes. `ultimo`: o último botão que casa (janela aninhada).
        `texto`: só os elementos de `sel` cujo texto casa (sem diferenciar maiúsculas), ex.: o botão "Fechar" sem aria-label."""
        s._p({'do': 'scroll', 'point': {'x': ponto[0], 'y': ponto[1]}, 'by': 0, 'duration': 0.3, 'after': 0}, round(max(0.0, at - 0.9), 2), label + ' (cursor)', {})
        alvo = {'selector': sel, **({'hasText': texto} if texto else {}), **({'nth': 'last'} if ultimo else {})}
        s.add({'do': 'type', 'target': alvo, 'text': '', 'noClick': True, 'label': label})
        filtro = f'.filter(b=>/{texto}/i.test(b.textContent))' if texto else ''
        js = f'[...document.querySelectorAll({json.dumps(sel)})]{filtro}.{"pop()" if ultimo else "shift()"}.click()'
        return s._p({'do': 'eval', 'js': js}, round(at, 2), label + ' (clique)', {})

    def clicar_fixo_alvo(s, alvo, ponto, js, at, label):
        """Como `clicar_fixo`, para um alvo que `selector`+`hasText` não separa (ex.: o dia 3 de um calendário: o texto "3" também casa
        com 13, 23, 30...). `alvo` é o alvo do robô (só registra o retângulo do passo), `js` faz o clique por eval. `at` = instante do
        clique; o cursor parte 0,9 s antes. Lição do T5, cap. 6: o clique do robô no dia levava 2,4 s (a janela do calendário ainda assenta)."""
        s._p({'do': 'scroll', 'point': {'x': ponto[0], 'y': ponto[1]}, 'by': 0, 'duration': 0.3, 'after': 0}, round(max(0.0, at - 0.9), 2), label + ' (cursor)', {})
        s.add({'do': 'type', 'target': alvo, 'text': '', 'noClick': True, 'label': label})
        return s._p({'do': 'eval', 'js': js}, round(at, 2), label + ' (clique)', {})

    def fim(s):
        s.flush(1e9)
        if any(x.get('js') == OBS for x in s.setup):
            s.steps.append({'do': 'eval', 'js': 'JSON.stringify(window.__avisos || "sem observador")', 'label': 'avisos de erro na tela'})
        s.steps.append({'do': 'mark', 'name': 'FIM', 'at': round(s.dur, 2)})

    def out(s):
        sem = SEMENTE[s.n]
        d = {
            'name': f't5-cap{s.n:02d}',
            'title': f'T5 · Cap. {s.n} · {NOMES[s.n]} (narração {str(round(s.dur, 1)).replace(".", ",")} s; marcas L1..L{len(s.linhas)} = início de cada linha do roteiro)',
            'seed': f't5-cap{s.n:02d}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
            'start': {'x': s.start[0], 'y': s.start[1]},
            'seedExtra': BASE + ([f't5/{sem}'] if sem else []) + EXTRA.get(s.n, []),
            'prewarm': s.prewarm, 'setup': s.setup, 'steps': s.steps,
        }
        if s.user: d['user'] = s.user
        d['storage'] = dict(STORAGE)
        return d


# ---------------------------------------------------------------- alvos
# localStorage de partida de todo capítulo: o aviso "Você tem 1 chamado de cliente aguardando" (Dashboard) já foi visto
STORAGE = {'dominex:portal-tickets-seen:d40f5787-1779-501f-900c-ddb2b90a36e5': '2031-01-01T00:00:00.000Z'}
BTN = lambda n, **kw: {'role': 'button', 'name': n, 'exact': True, **kw}
LINK = lambda n: {'role': 'link', 'name': n, 'exact': True}
TAB = lambda n, **kw: {'role': 'tab', 'name': n, **kw}
TXT = lambda t, **kw: {'text': t, 'exact': True, **kw}
SEL = lambda s, **kw: {'selector': s, **kw}
DLG = '[role=dialog]'
POP = '[data-radix-popper-content-wrapper]'
OPERACIONAL = BTN('Operacional')
GESTAO = BTN('Gestão')

SETUP_APP = lambda rota, esperar: [
    {'do': 'goto', 'url': rota}, {'do': 'waitFor', 'text': esperar, 'timeout': 20}, {'do': 'waitFor', 'idle': True}]
SETUP_DASH = SETUP_APP('/dashboard', 'Olá, Camila!')
PREWARM_OS = ['/dashboard', '/ordens-servico', '/agenda', '/funcionarios', '/mapa-ao-vivo']


# ================================================================ capítulos
def cap00():
    c = Cap(0, pace=0.6, start=(700, 420), prewarm=PREWARM_OS + ['/dashboard'], setup=SETUP_DASH)
    c.mark(1)
    c.hover(TXT('Olá, Camila!', exact=False), 1.2, at=1.0, label='tela inicial do Dominex, logada')
    c.hover(OPERACIONAL, 1.0, at=c.A(1, 'mapa', 1.4), label='o cursor desliza pelo menu até o grupo Operacional')
    c.mark(2)
    c.click(OPERACIONAL, at=c.L(2), label='abre o grupo Operacional')
    c.hover(LINK('Ordens de Serviço'), 0.9, at=c.A(2, 'abre', 0.4), label='menu: Ordens de Serviço')
    c.hover(LINK('Agenda'), 0.8, at=c.A(2, 'marca', 0.5), label='menu: Agenda')
    c.hover(LINK('Mapa e Rastreamento'), 1.4, at=c.A(2, 'acompanha', 0.5), label='menu: Mapa e Rastreamento')
    c.mark(3)
    c.hover(LINK('Ordens de Serviço'), 3.0, at=c.A(3, 'Vamos', 0.9), label='vamos começar pela tela de Ordens de Serviço')
    c.fim()
    return c

# ---------------------------------------------------------------- trechos comuns (não filmados, no `setup`)
OS_OK = 'Gerencie suas ordens de serviço'
SETUP_OS = SETUP_APP('/ordens-servico', OS_OK)
PROXIMO = {'role': 'button', 'name': 'Próximo', 'exact': True}
CLOCK_0900 = [{'do': 'clock', 'set': '2026-11-03T09:00:00-03:00'}]  # o navegador corre; a Nova OS nasce com 09:00 se abrir logo


def wiz_equip_marcado():
    return [{'do': 'click', 'target': {'role': 'checkbox', 'within': DLG}},
            {'do': 'waitFor', 'text': 'Serviços neste equipamento', 'timeout': 8},
            {'do': 'pause', 'seconds': 0.6}]


def fim_setup():
    return [{'do': 'waitFor', 'idle': True}, {'do': 'pause', 'seconds': 0.4}]


# ================================================================ capítulos de Ordens de Serviço
def cap01():
    c = Cap(1, pace=0.5, cps=9, start=(700, 420), prewarm=['/ordens-servico'], setup=SETUP_OS)
    MAIN_TOP = {'x': 760, 'y': 120}  # cabeçalho da página: a roda do mouse rola o conteúdo (main)
    c.mark(1)
    c.hover(LINK('Ordens de Serviço'), 1.2, at=c.A(1, 'Operacional,', 0.5), label='menu: Operacional, Ordens de Serviço')
    c.hover(TAB('Ordens de Serviço'), 0.4, at=c.A(1, 'Ordens', 0.7, nth=2), label='aba Ordens de Serviço')
    c.hover(TAB('Chamados'), 0.4, at=c.A(1, 'Chamados,', 0.7), label='aba Chamados')
    c.hover(TAB('Relatório'), 0.4, at=c.A(1, 'Relatório', 0.7), label='aba Relatório')
    c.hover(TAB('NPS e Satisfação'), 0.8, at=c.A(1, 'NPS', 0.7), label='aba NPS e Satisfação')
    c.mark(2)
    kpi = lambda t: TXT(t, exact=False, within='main')
    c.hover(kpi('OS Abertas'), 0.5, at=c.A(2, 'Abertas,', 0.9), label='cartão OS Abertas')
    c.hover(kpi('Concluídas'), 0.5, at=c.A(2, 'Concluídas,', 0.9), label='cartão Concluídas')
    c.hover(kpi('Atrasadas'), 0.5, at=c.A(2, 'Atrasadas', 0.9), label='cartão Atrasadas')
    c.hover(kpi('Próximos 7 dias'), 0.6, at=c.A(2, 'Próximos', 0.9), label='cartão Próximos 7 dias')
    c.hover({'role': 'button', 'name': 'Todos os tempos'}, 1.6, at=c.A(2, 'período', 0.7), label='filtro de período')
    c.mark(3)
    c.scroll(None, at=c.A(3, 'Kanban,', 0.5), label='desce até o Kanban', by=330, point=MAIN_TOP)
    KAN = {'x': 640, 'y': 520}
    c.scroll(None, at=c.A(3, 'Caminho,', 0.9), label='colunas A Caminho e Em Andamento', by=420, axis='x', point=KAN)
    c.scroll(None, at=c.A(3, 'Concluída,', 0.9), label='colunas Concluída e Pausada', by=420, axis='x', point=KAN)
    c.scroll(None, at=c.A(3, 'Cancelada.', 0.9), label='coluna Cancelada', by=600, axis='x', point=KAN)
    c.scroll(None, at=c.A(3, 'Cada', 0.4), label='volta ao início do Kanban', by=-1600, axis='x', point=KAN)
    c.hover(TXT('MP-2026-13', within='main'), 1.0, at=c.A(3, 'prefixo', 0.7), label='código do cartão: prefixo, ano e número')
    c.hover(TXT('MP-2026-12', within='main'), 3.0, at=c.A(3, 'como', 0.9), label='código do cartão: MP-2026-12')
    c.mark(4)
    c.click(SEL('main button:has(svg.lucide-layout-list)'), at=c.A(4, 'trocar', 0.9), label='alterna para Lista')
    th = lambda t: SEL('main th', hasText=t)
    for palavra, nome, rot in (('OS,', 'OS', 'OS'), ('criador,', 'Criador', 'Criador'), ('cliente,', 'Cliente', 'Cliente'), ('tipo,', 'Tipo', 'Tipo'),
                               ('data,', 'Data', 'Data'), ('status', 'Status', 'Status'), ('ações.', 'Ações', 'Ações')):
        c.hover(th(nome), 0.2, at=c.A(4, palavra, 0.55), label=f'coluna {rot}')
    c.click(SEL('main button:has(svg.lucide-layout-grid)'), at=c.A(4, 'neste', 1.1), label='volta ao Kanban')
    c.fim()
    return c


# Observador de avisos de erro na tela (aceite da fase 1): guarda em window.__avisos todo texto que apareça com "Não foi possível", "erro",
# "Tente novamente" ou "indisponível"; o passo final de cada capítulo devolve a lista (o resumo imprime) e ela tem de sair vazia.
OBS = ("(()=>{window.__avisos=[];const re=/N[ãa]o foi poss[ií]vel|erro|Tente novamente|indispon[ií]vel/i;const chk=(t)=>{t=(t||'').trim();"
       "const m=t&&t.match(new RegExp('[^]{0,40}('+re.source+')[^]{0,40}','i'));"
       "if(m&&window.__avisos.length<10)window.__avisos.push(m[0].replace(/[\\n\\r\\t ]+/g,' '))};new MutationObserver(ms=>{for(const m of ms){"
       "m.addedNodes.forEach(n=>chk(n.textContent));if(m.type==='characterData')chk(m.target.textContent)}}).observe(document.body,"
       "{childList:true,subtree:true,characterData:true});chk(document.body.innerText);"
       # tela escura de introdução e faixa de lembrete da trilha Domiflix (G1)
       "setInterval(()=>{const f=document.querySelector('section[aria-label^=\"Lembrete da trilha\"]');"
       "const e=[...document.querySelectorAll('div.fixed')].some(x=>getComputedStyle(x).backgroundColor==='rgb(17, 17, 17)');"
       "if((f||e)&&window.__avisos.length<10&&!window.__avisos.includes('TRILHA DOMIFLIX'))window.__avisos.push('TRILHA DOMIFLIX')},300);return 1})()")

# ---------------------------------------------------------------- 1.38.19: assistente da Nova OS refeito (4 etapas novas)
# Etapas: 1 Atendimento e orçamento · 2 Escopo técnico · 3 Equipe e agenda · 4 Revisão. A troca de etapa usa framer-motion (WAAPI) e,
# no navegador de gravação, a animação começa no futuro (relógio simulado) e a etapa fica presa na anterior: um observador no `setup`
# religa toda animação atrasada ao relógio do documento (mesma causa da lição do T5, cap. 10; aqui vale para toda troca de etapa).
FIXI = ('(()=>{if(!window.__fixAnim){window.__fixAnim=setInterval(()=>document.getAnimations().filter(a=>a.currentTime<0)'
        '.forEach(a=>{a.startTime=document.timeline.currentTime}),40)}return 1})()')
SETUP_OS2 = SETUP_OS + [{'do': 'eval', 'js': FIXI}, {'do': 'eval', 'js': OBS}]
ROLA_TOPO = '(()=>{const c=document.querySelector("[role=dialog] .overflow-y-auto");if(c)c.scrollTo({top:0,behavior:"auto"});return 1})()'
ROLA_FIM = '(()=>{const c=document.querySelector("[role=dialog] .overflow-y-auto");if(c)c.scrollTo({top:c.scrollHeight,behavior:"auto"});return 1})()'
FECHAR_PT = (1167, 77)  # botão "Fechar" do cabeçalho da janela (aria-label=Fechar), fora da faixa y 96..730 do robô
SW_CLIENTE = {'role': 'switch', 'name': 'Cliente cadastrado'}
RESUMO = '[aria-label="Resumo da ordem de serviço"]'


def wiz_etapa1(clock=False):
    """abre a Nova OS e preenche a etapa 1: Colégio Monte Verde + Manutenção Preventiva (a linha do orçamento já nasce com Qtd 1 e R$ 180,00)"""
    return (CLOCK_0900 if clock else []) + [
        {'do': 'click', 'target': BTN('Nova OS')},
        {'do': 'waitFor', 'text': 'Nova Ordem de Serviço', 'timeout': 10},
        {'do': 'click', 'target': {'role': 'combobox', 'hasText': 'Selecione o cliente'}},
        {'do': 'type', 'target': {'placeholder': 'Buscar cliente...'}, 'text': 'Colégio'},
        {'do': 'click', 'target': {'role': 'option', 'name': 'Colégio Monte Verde'}},
        {'do': 'click', 'target': SEL(f'{DLG} button[role=combobox]', hasText='Adicionar serviços')},
        {'do': 'click', 'target': TXT('Manutenção Preventiva', within=POP)},
        {'do': 'press', 'key': 'Escape'},
        {'do': 'waitFor', 'text': 'Gerenciar serviços', 'timeout': 8},
        {'do': 'waitFor', 'selector': f'{DLG} input[aria-label="Quantidade de Manutenção Preventiva"]', 'timeout': 8},
        {'do': 'pause', 'seconds': 0.6}]


def wiz_equip():
    """Próximo (etapa 2, Escopo técnico), ainda sem marcar o aparelho"""
    return [
        {'do': 'click', 'target': PROXIMO},
        {'do': 'waitFor', 'text': 'Selecione o equipamento.', 'timeout': 10},
        {'do': 'pause', 'seconds': 0.6}]


def cap02():
    c = Cap(2, pace=0.5, cps=14, start=(900, 480), prewarm=['/ordens-servico'], setup=SETUP_OS2)
    c.mark(1)
    c.click(BTN('Nova OS'), at=c.A(1, 'OS.', 1.0), label='Nova OS')
    c.waitfor(text='Nova Ordem de Serviço', timeout=10)
    c.hover(TXT('Revisão', within=DLG), 0.4, at=c.A(1, 'quatro', 0.7), label='as quatro etapas')
    c.hover(TXT('Atendimento e orçamento', within=DLG, nth=0), 0.9, at=c.A(1, 'Atendimento', 0.7), label='etapa Atendimento e orçamento')
    c.mark(2)
    c.hover(SW_CLIENTE, 0.3, at=c.A(2, 'cadastrado', 0.6), label='Cliente cadastrado')
    c.click(SW_CLIENTE, at=c.A(2, 'avulso.', 1.0), label='Cliente avulso')
    c.hover(SEL(f'{DLG} p', hasText='O cliente será criado automaticamente'), 1.3, at=c.A(2, 'dados', 0.8), label='aviso: o cliente é criado com estes dados')
    c.click(SW_CLIENTE, at=c.A(2, 'cadastro', 1.0), label='volta para Cliente cadastrado')
    c.mark(3)
    c.click({'role': 'combobox', 'hasText': 'Selecione o cliente'}, at=c.A(3, 'Aqui', 0.8), label='campo Cliente')
    c.type({'placeholder': 'Buscar cliente...'}, 'Colégio', at=c.A(3, 'Colégio', 0.35), cps=12, noClick=True, label='busca Colégio')
    c.click({'role': 'option', 'name': 'Colégio Monte Verde'}, at=c.A(3, 'Monte', -0.1), label='Colégio Monte Verde')
    c.mark(4)
    c.click(SEL(f'{DLG} button[role=combobox]', hasText='Adicionar serviços'), at=c.A(4, 'Tipos', 0.9), label='campo Tipos de Serviço')
    c.click(TXT('Manutenção Preventiva', within=POP), at=c.A(4, 'Manutenção', 0.9), label='Manutenção Preventiva')
    # a lista (com caixas de marcar e cores) fica aberta enquanto a fala diz "mais de um serviço"
    c.hover(TXT('Visita Técnica', within=POP), 1.6, at=c.A(4, 'mais', 0.7), label='a lista deixa marcar mais de um serviço')
    c.press('Escape', at=c.A(4, 'principal,', 0.6), label='fecha a lista de serviços')
    c.hover(TXT('Manutenção Preventiva', within=RESUMO), 1.8, at=c.A(4, 'cor', 0.5), label='o serviço principal no resumo da OS')
    c.mark(5)
    SW = {'role': 'switch', 'name': 'Endereço de serviço (diferente do cliente)'}
    c.ev(js_centrar(f'{DLG} button[role=switch][aria-label="Endereço de serviço (diferente do cliente)"]'), at=c.L(5) + 0.2, label='desce até o Endereço de serviço')
    c.click(SW, at=c.A(5, 'ligar', 1.0), label='liga o Endereço de serviço')
    c.hover(SEL(f'{DLG} p', hasText='O atendimento será feito neste endereço'), 1.6, at=c.A(5, 'vale', 0.7), label='campos do endereço de serviço')
    c.click(SW, at=c.A(5, 'desligo', 1.0), label='desliga o Endereço de serviço')
    c.fim()
    return c


def cap03():
    c = Cap(3, pace=0.5, cps=14, start=(900, 480), prewarm=['/ordens-servico'], setup=SETUP_OS2 + wiz_etapa1() + fim_setup())
    c.mark(1)
    c.ev(js_centrar(f'{DLG} #os-service-budget'), at=0.0, label='desce até o orçamento')
    c.hover(TXT('Serviços e Mão de Obra', exact=False, within=DLG), 0.3, at=c.A(1, 'serviços,', 0.7), label='serviços')
    c.hover(TXT('Materiais', within=DLG, nth=0), 0.5, at=c.A(1, 'materiais.', 0.7), label='materiais')
    c.mark(2)
    c.hover(SEL(f'{DLG} table tbody tr:first-child'), 0.4, at=c.A(2, 'Manutenção', 0.7), label='a linha do serviço já criada')
    c.hover(SEL(f'{DLG} input[aria-label="Quantidade de Manutenção Preventiva"]'), 0.4, at=c.A(2, 'quantidade', 0.7), label='Qtd: 1')
    c.hover(SEL(f'{DLG} input[aria-label="Valor unitário de Manutenção Preventiva"]'), 1.0, at=c.A(2, 'cento', 0.7), label='Valor Unit.: 180')
    c.hover(TXT('Total para faturamento', within=DLG), 1.4, at=c.A(2, 'Total', 0.8), label='Total para faturamento')
    c.mark(3)
    c.clicar_fixo(f'{DLG} button[aria-label=Fechar]', FECHAR_PT, at=c.A(3, 'janela,', 0.2), label='fecha a janela')
    c.click(BTN('Nova OS'), at=c.A(3, 'Nova', 0.9), label='Nova OS de novo')
    c.waitfor(text='Rascunho encontrado', timeout=10)
    c.click(BTN('Retomar rascunho'), at=c.A(3, 'Retomar', 0.9), label='Retomar rascunho')
    c.mark(4)
    c.hover({'role': 'combobox', 'hasText': 'Colégio Monte Verde'}, 0.8, at=c.A(4, 'Pronto,', 0.15), label='cliente e serviço de volta')
    c.click(PROXIMO, at=c.A(4, 'Vamos', 0.9), label='Próximo (Escopo técnico)')
    c.waitfor(text='Selecione o equipamento.', timeout=10)
    c.fim()
    return c


def cap04():
    # só a tela mudou (nome da etapa 2: Escopo técnico; o cartão do aparelho já abre ao marcar); a fala é a mesma
    c = Cap(4, pace=0.5, cps=14, start=(900, 480), prewarm=['/ordens-servico'],
            setup=SETUP_OS2 + wiz_etapa1() + wiz_equip() + fim_setup())
    c.mark(1)
    c.click({'role': 'checkbox', 'within': DLG}, at=c.A(1, 'marco', 0.9), label='marca o Hi-Wall 18.000 BTUs')
    c.waitfor(text='Serviços neste equipamento', timeout=8)
    c.hover(SEL(f'{DLG} p', hasText='Hi-Wall 18.000 BTUs - Sala dos professores'), 1.0, at=c.A(1, 'Como', 0.7), label='o aparelho marcado')
    c.hover(TXT('Manutenção Preventiva', within=f'{DLG} form'), 1.2, at=c.A(1, 'vinculada', 0.7), label='serviço vinculado a equipamento')
    c.mark(2)
    c.hover(SEL(f'{DLG} button[aria-expanded]', hasText='checklist(s)'), 0.2, at=c.A(2, 'Abrindo', 0.7), label='setinha do aparelho')
    c.hover(TXT('Serviços neste equipamento', within=DLG), 1.0, at=c.A(2, 'serviços', 0.7), label='serviços neste equipamento')
    c.hover(TXT('Checklists aplicados', within=DLG), 0.8, at=c.A(2, 'checklists', 0.7), label='checklists aplicados')
    c.hover(SEL(f'{DLG} p', hasText='Manutenção preventiva de split'), 1.2, at=c.A(2, 'Olha:', 0.7), label='o checklist entrou sozinho')
    c.click(SEL(f'{DLG} button[title="Pré-visualizar checklist"]'), at=c.A(2, 'treze', 1.0), label='pré-visualiza o checklist')
    c.waitfor(text='Como este checklist aparece para o técnico na Ordem de Serviço', timeout=10)
    c.clicar_fixo(f'{DLG} button[aria-label=Fechar]', (961, 69), at=c.A(2, 'anterior.', -0.1), label='fecha a prévia', ultimo=True)
    c.mark(3)
    c.hover(SEL(f'{DLG} button[title="Pré-visualizar checklist"]'), 0.8, at=c.A(3, 'pré-visualizar', 0.7), label='ícone de pré-visualizar')
    c.hover(TXT('Serviços neste equipamento', within=DLG), 1.0, at=c.A(3, 'copiar', 0.7), label='serviços e checklists do aparelho')
    c.scroll(TXT('Checklists avulsos', within=DLG), at=c.A(3, 'Tem', 0.7), label='desce até os checklists avulsos')
    c.hover(TXT('Checklists a nível de OS, sem equipamento vinculado.', within=DLG), 1.8, at=c.A(3, 'avulsos,', 0.8), label='Checklists avulsos')
    c.fim()
    return c


def cap05():
    c = Cap(5, pace=0.45, cps=26, start=(900, 480), prewarm=['/ordens-servico'],
            setup=SETUP_OS2 + wiz_etapa1() + wiz_equip() + wiz_equip_marcado() + fim_setup())
    c.mark(1)
    c.click(PROXIMO, at=0.0, label='Próximo (Equipe e agenda)')
    c.waitfor(text='Defina responsáveis, organize as jornadas', timeout=10)
    c.hover(SEL(f'{DLG} h2', hasText='Equipe e agenda'), 0.6, at=c.A(1, 'escolhe', 0.7), label='etapa Equipe e agenda')
    c.mark(2)
    RESP = SEL(f'{DLG} button[role=combobox]', hasText='Selecione...')
    c.click(RESP, at=c.A(2, 'Responsáveis,', 0.9), label='campo Responsáveis')
    c.click(TXT('Rafael Lima', within=POP), at=c.A(2, 'Rafael', 0.9), label='Rafael Lima')
    c.hover(TXT('Técnicos', exact=False, within=POP), 1.0, at=c.A(2, 'Técnicos', 0.7), label='técnicos e equipes no mesmo seletor')
    c.press('Escape', at=c.A(2, 'daqui', 0.2), label='fecha o seletor')
    c.mark(3)
    c.hover(TXT('Período do atendimento', within=DLG), 0.5, at=c.A(3, 'Período', 0.7), label='Período do atendimento')
    c.click(SEL(f'{DLG} button:has(svg.lucide-calendar)', nth=0), at=c.A(3, 'data', 0.9), label='Data inicial')
    c.click({'role': 'gridcell', 'name': '10', 'exact': True}, label='terça, dia 10')
    c.click({'role': 'button', 'name': 'Quando começa'}, label='Quando começa')
    c.click({'role': 'option', 'name': '09', 'exact': True, 'within': '[role=listbox][aria-label=Horas]'}, label='hora 09')
    c.click({'role': 'option', 'name': '00', 'exact': True, 'within': '[role=listbox][aria-label=Minutos]'}, label='minuto 00')
    c.click({'role': 'button', 'name': 'Concluir'}, label='Concluir (início)')
    c.click({'role': 'button', 'name': 'Quando termina'}, label='Quando termina')
    c.click({'role': 'option', 'name': '11', 'exact': True, 'within': '[role=listbox][aria-label=Horas]'}, label='hora 11')
    c.click({'role': 'option', 'name': '00', 'exact': True, 'within': '[role=listbox][aria-label=Minutos]'}, label='minuto 00')
    c.click({'role': 'button', 'name': 'Concluir'}, label='Concluir (fim)')
    c.mark(4)
    DESC = {'placeholder': 'Descreva o serviço a ser realizado'}
    # a Descrição fica abaixo da faixa do robô (y 729): o clique rolaria ~1,6 s dentro do passo e atrasava L4 em 1,1 s (ensaio completo)
    c.ev(js_centrar(f'{DLG} textarea[placeholder="Descreva o serviço a ser realizado"]'), at=c.L(4) - 2.2, label='leva a Descrição à vista')
    c.click(DESC, at=c.A(4, 'descrição,', 0.8), label='campo Descrição do Serviço')
    c.type(DESC, 'Manutenção preventiva', at=c.A(4, 'vai', 0.7), cps=14, noClick=True, label='Descrição do Serviço')
    c.mark(5)
    NPS = {'role': 'switch', 'name': 'Gerar Pesquisa de Satisfação ao finalizar?'}
    c.ev(js_centrar(f'{DLG} button[role=switch][aria-label="Gerar Pesquisa de Satisfação ao finalizar?"]'), at=c.L(5), label='desce até a pesquisa de satisfação')
    c.hover(TXT('Gerar Pesquisa de Satisfação', exact=False, within=DLG), 0.6, at=c.A(5, 'Gerar', 0.2), label='Gerar Pesquisa de Satisfação')
    c.click({**NPS, 'checked': False}, at=c.A(5, 'Sim:', 1.0), label='deixa a pesquisa em Sim', when={**NPS, 'checked': False})
    c.hover(NPS, 1.2, at=c.A(5, 'assim', 0.7), label='pesquisa ligada')
    c.mark(6)
    c.ev(ROLA_TOPO, at=c.L(6) - 0.1, label='volta ao topo da etapa')
    c.hover(SEL(f'{DLG} button[role=combobox]', hasText='Rafael Lima'), 2.0, at=c.A(6, 'técnico', 0.7), label='volta ao seletor Responsáveis')
    c.mark(7)
    c.click(PROXIMO, at=c.L(7) + 0.1, label='Próximo (Revisão)')
    # na tela do computador a Revisão abre com "Pronto para criar" + o resumo por etapa (o rótulo "Confira antes de salvar" só existe no
    # resumo do celular): o destaque cai no cabeçalho real da tela, na palavra "Confira" da fala (avisado ao main)
    c.waitfor(text='Pronto para criar', timeout=10)
    c.ev(ROLA_TOPO, label='topo da Revisão')
    c.hover(TXT('Pronto para criar', within=DLG), 1.4, at=c.A(7, 'Confira', 0.7), label='Revisão: Pronto para criar')
    c.click(BTN('Criar OS'), at=c.A(7, 'Criar', 0.25), label='Criar OS')
    c.waitfor(text='OS #16', timeout=12)
    c.scroll(None, at=c.A(7, 'aparece', 1.2), label='desce até o Kanban', by=330, point={'x': 760, 'y': 120})
    c.hover(TXT('MP-2026-16', within='main'), 2.4, at=c.A(7, 'Pendente,', 0.9), label='cartão MP-2026-16 na coluna Pendente')
    c.fim()
    return c


# ================================================================ capítulos 6 a 9 (Ordens de Serviço: recorrência, Kanban, status, conclusão)
MAIN_TOP = {'x': 760, 'y': 120}  # cabeçalho da página: a roda do mouse rola o conteúdo (main)
KAN = {'x': 640, 'y': 520}       # sobre o Kanban: a roda rola as colunas na horizontal
RESP_VAZIO = SEL(f'{DLG} button[role=combobox]', hasText='Selecione...')
SW_REC = SEL(f'{DLG} div:has(> label > svg.lucide-repeat) > button[role=switch]')


def js_clicar(sel, texto=None):
    """clique instantâneo (sem cursor) para os passos "acelerados": o app troca de etapa na hora, como num time-lapse"""
    filtro = f'.filter(b=>/{texto}/i.test(b.textContent))' if texto else ''
    return f'[...document.querySelectorAll({json.dumps(sel)})]{filtro}[0].click()'


def js_centrar(sel):
    """rola de forma suave (scrollTo smooth, sem passo do robô) o container com rolagem que contém `sel`, até o centro dele:
    o clique seguinte já encontra o alvo à vista e não gasta ~1 s de rolagem dentro do passo (lição do T5, cap. 6)"""
    return ('(()=>{const el=document.querySelector(%s);if(!el)return false;for(let n=el.parentElement;n&&n!==document.documentElement;n=n.parentElement){'
            'const s=getComputedStyle(n);if(/(auto|scroll)/.test(s.overflowY)&&n.scrollHeight>n.clientHeight+4){const r=el.getBoundingClientRect(),b=n.getBoundingClientRect();'
            'n.scrollTo({top:n.scrollTop+(r.top+r.height/2)-(b.top+b.height/2),behavior:"smooth"});return true}}return false})()') % json.dumps(sel)


def cap06():
    abrir = CLOCK_0900 + [{'do': 'click', 'target': BTN('Nova OS')}, {'do': 'waitFor', 'text': 'Nova Ordem de Serviço', 'timeout': 10}, {'do': 'pause', 'seconds': 0.5}]
    c = Cap(6, pace=0.3, cps=14, start=(900, 480), prewarm=['/ordens-servico'], setup=SETUP_OS2 + abrir)
    PROX = js_clicar(f'{DLG} button', '^Próximo')
    c.mark(1)
    c.click({'role': 'combobox', 'hasText': 'Selecione o cliente'}, at=0.0, label='campo Cliente')
    c.click({'role': 'option', 'name': 'Academia Ponto Forte'}, at=c.A(1, 'Academia', 1.0), label='Academia Ponto Forte')
    c.click(SEL(f'{DLG} button[role=combobox]', hasText='Adicionar serviços'), at=c.A(1, 'higienização', 1.0), label='campo Tipos de Serviço')
    c.click(TXT('Higienização de Split', within=POP), at=c.A(1, 'dos', 0.8), label='Higienização de Split')
    c.press('Escape', label='fecha a lista de serviços')
    c.ev(PROX, at=c.A(1, 'splits', 0.2), label='Próximo (acelerado, Escopo técnico)')
    c.waitfor(text='Selecione um ou mais equipamentos para esta OS.', timeout=10)
    c.ev(js_clicar(f'{DLG} button', 'Selecionar todos'), label='marca os dois splits (acelerado)')
    c.waitfor(text='Desmarcar todos', timeout=8)
    c.ev(PROX, label='Próximo (acelerado, Equipe e agenda)')
    c.waitfor(text='Defina responsáveis, organize as jornadas', timeout=10)
    c.click(RESP_VAZIO, label='campo Responsáveis')
    # o Lucas vai por eval (time-lapse): o clique do robô na opção levava 2 s e atrasava a Recorrência. Lição do T5, cap. 6
    c.waitfor(text='Lucas Ferreira', timeout=6)
    c.ev(js_opcao_pop('Lucas Ferreira'), label='Lucas Ferreira (acelerado)')
    c.pause(0.2)
    c.press('Escape', label='fecha o seletor')
    SW_STR = f'{DLG} div:has(> label > svg.lucide-repeat) > button[role=switch]'
    # A janela rola com a roda do mouse (o tempo é do robô): o scrollTo suave do navegador anda com os quadros da página e, com a máquina
    # ocupada, ainda estava no começo quando o robô chegava ao interruptor. No fim da rolagem o interruptor fica em css (239, 589).
    # Ligado o interruptor, o painel (Frequência, A cada, Até) cresce para baixo e o clique em Frequência teria de rolar a janela por conta
    # própria (~2,4 s dentro do passo): a segunda rolagem leva o painel inteiro à vista antes. Lição do T5, cap. 6.
    ROLA_FORM = {'do': 'scroll', 'point': {'x': 640, 'y': 420}, 'by': 900, 'duration': 0.5, 'after': 0}
    c._p(dict(ROLA_FORM), None, 'leva a Recorrência à vista (rolagem)', {})
    t_sw = c.A(1, 'Recorrência.', 0.4)
    c.clicar_fixo(SW_STR, (239, 589), at=t_sw, label='liga a Recorrência')
    c._p(dict(ROLA_FORM), round(t_sw + 0.6, 2), 'mostra o painel da Recorrência (rolagem)', {})
    c.mark(2)
    # A narração ganhou duas pausas (t5/narracao/pausas.py: 1,2 s antes de "Em Frequência" e 1,5 s antes de "A prévia"): os seletores
    # do formulário levam 1 a 2 s por clique e o calendário passa 3 meses; a escolha do dia cai dentro da segunda pausa. Lição do T5, cap. 6.
    c.click(SEL(f'{DLG} button[role=combobox]', hasText='Semanal'), at=c.A(2, 'Frequência,', 1.2), label='campo Frequência')
    c.click({'role': 'option', 'name': 'Mensal'}, at=c.A(2, 'Mensal,', 1.0), label='Mensal')
    c.click(SEL(f'{DLG} button', hasText='dd/mm/aaaa'), at=c.A(2, 'Até', 1.0), label='campo Até')
    c.waitfor(selector='button[name=next-month]', timeout=8)
    for i in range(3):
        c.ev('document.querySelector("button[name=next-month]").click()', label=f'mês seguinte ({i + 1})')
        c.pause(0.25)
    DIA_3 = js_clicar_expr("[...document.querySelectorAll('[role=gridcell]')].find(x=>x.textContent.trim()==='3'&&!x.disabled)")
    c.clicar_fixo_alvo({'role': 'gridcell', 'name': '3', 'exact': True}, (928, 267), DIA_3, at=c.A(2, 'prévia', 0.7), label='dia 3 de fevereiro')
    c.hover(SEL(f'{DLG} p', hasText='Serão criadas'), 2.4, at=c.A(2, 'diz', 0.7), label='prévia: serão criadas 4 OS')
    c.mark(3)
    # 1.38.19: a recorrência ligada na etapa Equipe e agenda ainda passa pela etapa Revisão antes do botão final (a fala não a cita)
    c.ev(PROX, at=c.L(3) - 0.6, label='Próximo (acelerado, Revisão)')
    c.waitfor(text='Pronto para criar', timeout=10)
    c.click(BTN('Criar OS Recorrentes'), at=c.A(3, 'Criar', 0.2), label='Criar OS Recorrentes')
    c.waitfor(text='com recorrência!', timeout=15)
    c.scroll(None, at=c.A(3, 'série', 0.4), label='desce até o Kanban', by=330, point=MAIN_TOP)
    c.mark(4)
    serie = lambda cod: TXT(cod, within='main')
    c.hover(serie('HIG-2026-17'), 0.4, at=c.A(4, 'mudar', 0.5), label='cartão da série: novembro')
    c.hover(serie('HIG-2026-18'), 0.4, at=c.A(4, 'ordem', 0.5), label='cartão da série: dezembro')
    c.hover(serie('HIG-2027-19'), 0.4, at=c.A(4, 'sistema', 0.5), label='cartão da série: janeiro')
    c.hover(serie('HIG-2027-20'), 2.0, at=c.A(4, 'vale', 0.5), label='cartão da série: fevereiro')
    c.fim()
    return c


def cap07():
    c = Cap(7, pace=0.45, cps=14, start=(900, 480), prewarm=['/ordens-servico'], setup=SETUP_OS)
    c.mark(1)
    # o arrasto leva ~2,2 s só para o cursor chegar ao cartão e ~1,6 s até soltar: começa cedo para que o cartão seja pego perto de "arrastar"
    c.scroll(None, at=0.3, label='desce até o Kanban', by=330, point=MAIN_TOP)
    c.scroll(None, at=1.4, label='mostra Pendente, A Caminho e Em Andamento', by=560, axis='x', point=KAN)
    c.drag(TXT('MC-2026-11', within='main'), SEL('main h3', hasText='Em Andamento'), at=2.6, label='arrasta MC-2026-11 de Pendente para Em Andamento')
    c.hover(TXT('MC-2026-11', within='main'), 0.8, at=c.A(1, 'hora.', 0.9), label='o cartão já está em Em Andamento')
    c.mark(2)
    c.hover({'role': 'button', 'name': 'Criar OS em "Pendente"'}, 1.8, at=c.A(2, 'cada', 0.8), label='o "+" da coluna Pendente')
    c.mark(3)
    c.click(TXT('HIG-2026-9', within='main'), at=c.A(3, 'Clicando', 0.1), label='abre o detalhe da OS #9')
    c.waitfor(text='Check-in / Check-out', timeout=10)
    c.hover(SEL(f'{DLG} h3', hasText='Cliente'), 0.3, at=c.A(3, 'cliente,', 1.0), label='cartão Cliente')
    c.hover(SEL(f'{DLG} h3', hasText='Equipamento'), 0.3, at=c.A(3, 'equipamento,', 0.5), label='cartão Equipamento')
    c.hover(SEL(f'{DLG} h3', hasText='Check-in / Check-out'), 1.2, at=c.A(3, 'registros', 0.2), label='cartão Check-in / Check-out')
    c.scroll(SEL(f'{DLG} button', hasText='Preencher OS'), at=c.A(3, 'Embaixo', 0.8), label='desce até as ações')
    c.click(SEL(f'{DLG} button', hasText='Link OS'), at=c.A(3, 'copia', 1.0), label='Link OS')
    c.hover(SEL(f'{DLG} button', hasText='Preencher OS'), 2.4, at=c.A(3, 'Preencher', 0.8), label='Preencher OS')
    c.mark(4)
    c.click(SEL(f'{DLG} button', hasText='Resetar OS'), at=c.A(4, 'Resetar', 0.9), label='Resetar OS')
    c.waitfor(text='Manter o preenchimento', timeout=10)
    c.hover(TXT('Manter o preenchimento'), 0.4, at=c.A(4, 'mantém', 0.8), label='Manter o preenchimento')
    c.hover(TXT('Apagar o preenchimento'), 0.4, at=c.A(4, 'apaga', 0.8), label='Apagar o preenchimento')
    c.click(BTN('Cancelar'), at=c.A(4, 'preenchido.', 0.2), label='Cancelar')
    c.fim()
    return c


def cap08():
    c = Cap(8, pace=0.3, cps=14, start=(900, 480), prewarm=['/ordens-servico'], setup=SETUP_OS)
    CFG = {'role': 'button', 'name': 'Configurações', 'exact': True, 'within': 'main'}
    LINHA = lambda nome: f'{DLG} div[draggable=true]:has-text("{nome}")'
    c.mark(1)
    c.click(CFG, at=c.A(1, 'Configurações', 1.0), label='Configurações')
    c.waitfor(text='Configurações de OS', timeout=10)
    TRIG = SEL(LINHA('Pausada') + ' button[aria-label="Ações"]')
    c.hover(TRIG, 0.4, at=c.A(1, 'status.', 0.6), label='menu da linha Pausada')  # o menu das linhas abre por hover
    c.click(TRIG, unless={'role': 'menuitem', 'name': 'Editar'}, label='abre o menu se ainda não abriu')
    c.click({'role': 'menuitem', 'name': 'Editar'}, at=c.A(1, 'mudar', -0.1), label='Editar')
    c.hover(SEL(f'{DLG} input[type=color]'), 0.3, at=c.A(1, 'cor', -0.2), label='nome e cor')
    c.click(BTN('Cancelar'), at=c.A(1, 'arrastar', 0.0), label='Cancelar')
    c.clicar_fixo(f'{DLG} button', (913, 76), at=c.A(1, 'colunas.', 0.0), label='fecha as configurações', texto='fechar')
    c.mark(2)
    FILTROS = {'role': 'button', 'name': 'Filtros'}
    # A narração ganhou uma pausa de 1,5 s antes de "Em Filtros" (t5/narracao/pausas.py): fechar as configurações, abrir a janela de
    # filtros (1,1 a 2,7 s) e marcar o status levam mais que os 3 s da fala. Lição do T5, cap. 8.
    c.click(FILTROS, at=c.A(2, 'Filtros,', 1.8), label='Filtros')
    c.click(TXT('Em Andamento', within=DLG), at=c.A(2, 'escolhe', 0.2), label='marca Em Andamento')
    # o "Aplicar" fica colado no rodapé da janela (y ~768, fora da faixa 96..730 do robô): clique fixo, sem rolagem em vão (lição do T1)
    c.clicar_fixo(f'{DLG} button', (1056, 768), at=c.A(2, 'ver.', -0.3), label='Aplicar', texto='Aplicar')
    c.mark(3)
    BUSCA = {'placeholder': 'Buscar por OS, cliente, telefone, endereço ou serviço...'}
    c.click(BUSCA, at=c.A(3, 'telefone,', 1.0), label='campo de busca')
    c.type(BUSCA, 'Monte', at=c.A(3, 'digita,', 0.2), cps=14, noClick=True, label='busca Monte')  # 5 letras bastam: 'Monte Verde' (1,6 s) atrasava o aviso "filtros pausados" em 0,8 s
    c.hover(TXT('Mostrando resultados de todas as OS (filtros pausados)'), 1.2, at=c.A(3, 'olha', 0.4), label='filtros pausados')
    c.press('Control+A', at=c.A(3, 'período', 0.0), label='seleciona a busca')
    c.press('Backspace', label='limpa a busca')
    c.fim()
    return c


def cap09():
    c = Cap(9, pace=0.3, cps=14, start=(900, 480), prewarm=['/ordens-servico'], setup=SETUP_OS)
    c.mark(1)
    c.scroll(None, at=c.A(1, 'ciclo', 0.9), label='desce até o Kanban', by=330, point=MAIN_TOP)
    c.scroll(None, at=c.A(1, 'concluir', 0.9), label='mostra Em Andamento e Concluída', by=800, axis='x', point=KAN)
    c.drag(TXT('MC-2026-11', within='main'), SEL('main h3', hasText='Concluída'), at=c.A(1, 'arrastando', 0.8), label='arrasta MC-2026-11 de Em Andamento para Concluída')
    c.waitfor(text='Receita da Ordem de Serviço', timeout=10)
    c.hover(TXT('Houve alguma receita nesta Ordem de Serviço?', within=DLG), 1.0, at=c.A(1, 'houve', 0.8), label='a pergunta sobre a receita')
    c.hover(TXT('Receita da Ordem de Serviço', within=DLG), 1.6, at=c.A(1, 'Perguntar', 0.8), label='o título da janela')
    c.hover(TXT('Se entrou (ou vai entrar)', exact=False, within=DLG), 1.2, at=c.A(1, 'entrou', 0.8), label='lance agora e o valor fica vinculado')
    c.hover(TXT('Valor da OS', within=DLG), 1.0, at=c.A(1, 'valor', 0.9), label='Valor da OS sugerido')
    c.click(BTN('Não'), at=c.A(1, 'respondo', 0.9), label='Não')
    # a Lista tem a OS concluída lá embaixo (linha 9 de 10, y > 730): rola de forma suave ANTES de apontar o menu, para o robô não gastar 2 s rolando em vão
    c.click(SEL('main button:has(svg.lucide-layout-list)'), at=c.A(2, 'Dá', 0.9), label='alterna para Lista')
    c.mark(2)
    c.ev('document.querySelector("main").scrollTo({top: 99999, behavior: "smooth"})', at=c.A(2, 'Dá', -0.2), label='rola a lista até o fim (suave)')
    c.pause(0.7)
    TRIG9 = SEL('main tbody tr:has-text("MC-2026-11") td:last-child button')
    c.hover(TRIG9, 0.4, label='menu Ações da OS concluída')  # abre por hover
    c.click(TRIG9, unless={'role': 'menuitem', 'name': 'Faturar OS'}, label='abre o menu se ainda não abriu')
    c.hover({'role': 'menuitem', 'name': 'Faturar OS'}, 4.0, label='Faturar OS')
    c.fim()
    return c


def js_kpis():
    """Cartões de KPI (framer-motion) montados depois da carga demoram a aparecer no navegador de gravação: o relógio simulado do
    Playwright adianta o performance.now e a animação (WAAPI) começa no futuro (currentTime < 0). Religa as animações atrasadas ao
    relógio do documento: o fade nativo (0,5 s, escalonado) corre na hora. Lição do T5, cap. 10."""
    return 'document.getAnimations().filter(a=>a.currentTime<0).forEach(a=>{a.startTime=document.timeline.currentTime})'


def cap10():
    c = Cap(10, pace=0.45, cps=14, start=(900, 480), prewarm=['/ordens-servico'], setup=SETUP_OS)
    c.mark(1)
    c.hover(TAB('Chamados'), 0.4, at=c.A(1, 'Chamados', 1.1), label='aba Chamados (cursor)')
    c.hover(TAB('Relatório'), 0.4, at=c.A(1, 'Relatório.', 0.7), label='aba Relatório (cursor)')
    c.click(TAB('Chamados'), at=c.A(1, 'Na', 0.5), label='aba Chamados')
    c.waitfor(text='Chamado pelo portal', timeout=10)
    c.hover(TXT('Portal do Cliente', within='main'), 0.8, at=c.A(1, 'portais.', 0.9), label='origem: Portal do Cliente')
    c.click(SEL('main button[role=combobox]', hasText='Chamados'), at=c.A(1, 'filtra', 0.9), label='filtro Chamados abertos')
    c.press('Escape', at=c.A(1, 'abertos', 0.1), label='fecha o filtro')
    c.hover({'role': 'button', 'name': 'Abrir chamado'}, 1.4, at=c.A(1, 'abre', 0.6, nth=1), label='Abrir chamado')
    c.mark(2)
    c.click(TAB('Ordens de Serviço'), at=round(c.L(2) - 0.2, 2), label='volta à aba Ordens de Serviço')
    c.ev(js_kpis(), label='cartões de KPI (animação)')
    c.hover(SEL('main h3', hasText='Chamados do Portal'), 1.6, at=c.A(2, 'azul', 0.3), label='coluna Chamados do Portal')
    c.hover(TXT('MC-2026-15', within='main'), 1.6, at=c.A(2, 'Aí', 0.8), label='o chamado vira uma OS normal')
    c.mark(3)
    c.click(TAB('Relatório'), at=round(c.L(3) - 0.2, 2), label='aba Relatório')
    c.ev(js_kpis(), label='cartões de KPI (animação)')
    c.waitfor(text='Taxa de conclusão', timeout=12)
    c.hover(TXT('Total de OS', within='main'), 0.6, at=c.A(3, 'total', 1.5), label='KPI Total de OS')  # o 1º movimento depois da troca de aba custa ~1,4 s (gráficos montando): sai cedo e não atrasa os KPIs seguintes
    c.hover(TXT('Taxa de conclusão', within='main'), 0.6, at=c.A(3, 'taxa', 0.8), label='KPI Taxa de conclusão')
    c.hover(TXT('Tempo médio', within='main'), 0.6, at=c.A(3, 'tempo', 0.8), label='KPI Tempo médio')
    c.hover(TXT('Faturamento', within='main'), 0.8, at=c.A(3, 'faturamento,', 0.8), label='KPI Faturamento')
    c.scroll(None, at=c.A(3, 'gráficos', 0.9), label='desce até os gráficos', by=520, point=MAIN_TOP)
    c.hover(TXT('OS por Status', within='main'), 0.3, at=c.A(3, 'status,', 0.8), label='gráfico por status')
    c.hover(TXT('OS por Tipo de Serviço', within='main'), 0.3, at=c.A(3, 'tipo', 0.8), label='gráfico por tipo de serviço')
    c.scroll(None, at=c.A(3, 'dia', 1.2), label='desce até o dia da semana', by=520, point=MAIN_TOP)
    c.hover(TXT('OS por Dia da Semana', within='main'), 0.6, at=c.A(3, 'semana.', 0.5), label='gráfico por dia da semana')
    c.hover(TXT('Saúde do agendamento', within='main'), 1.2, at=c.A(3, 'Saúde', 0.8), label='quadro Saúde do agendamento')
    c.hover(TXT('Concluídas no', exact=False, within='main'), 2.0, at=c.A(3, 'concluídas', 0.8), label='Concluídas no prazo')
    c.fim()
    return c


def cap11():
    c = Cap(11, pace=0.45, cps=14, start=(900, 480), prewarm=['/ordens-servico'], setup=SETUP_OS)
    c.mark(1)
    c.click(TAB('NPS e Satisfação'), at=c.A(1, 'NPS', 1.0), label='aba NPS e Satisfação')
    c.waitfor(text='Média por Categoria', timeout=12)
    c.hover(TXT('NPS Score', within='main', nth=0), 0.3, at=c.A(1, 'Score,', 0.9), label='KPI NPS Score')
    c.hover(TXT('Média Geral', within='main'), 0.3, at=c.A(1, 'média', 0.9), label='KPI Média Geral')
    c.hover(TXT('Respostas', within='main'), 0.3, at=c.A(1, 'respostas', 0.9, nth=1), label='KPI Respostas')
    c.hover(TXT('Taxa de Resposta', within='main'), 0.5, at=c.A(1, 'taxa', 0.9), label='KPI Taxa de Resposta')
    c.hover(TXT('Distribuição NPS', within='main'), 0.5, at=c.A(1, 'distribuição', 0.9), label='gráfico Distribuição NPS')
    c.hover(TXT('Promotores', exact=False, within='main'), 0.3, at=c.A(1, 'promotores,', 0.9), label='Promotores')
    c.hover(TXT('Neutros', exact=False, within='main'), 0.3, at=c.A(1, 'neutros', 0.9), label='Neutros')
    c.hover(TXT('Detratores', exact=False, within='main'), 1.0, at=c.A(1, 'detratores.', 0.9), label='Detratores')
    c.mark(2)
    c.scroll(None, at=round(c.L(2) - 0.2, 2), label='desce até o ranking', by=600, point=MAIN_TOP)   # 1º gesto da linha em L(2) - 0,2: a marca L2 sobe junto com a fala
    c.hover(TXT('Ranking de Técnicos', within='main'), 0.5, at=c.A(2, 'ranking', 0.0), label='Ranking de Técnicos')
    c.hover(TXT('Detratores em Aberto', exact=False, within='main'), 0.5, at=c.A(2, 'detratores', 0.9), label='Detratores em Aberto')
    c.hover(TXT('Atenção', within='main'), 0.5, at=c.A(2, 'atenção,', 0.9), label='selo Atenção')
    c.scroll(None, at=c.A(2, 'feed', 0.9), label='desce até o feed', by=700, point=MAIN_TOP)
    c.hover(TXT('Feed de Feedbacks', within='main'), 0.6, at=c.A(2, 'comentários', 0.9), label='Feed de Feedbacks')
    c.mark(3)
    c.scroll(None, at=c.A(3, 'Em', 1.2), label='volta ao topo', by=-1400, point=MAIN_TOP)
    c.click({'role': 'button', 'name': 'Configurações', 'exact': True, 'within': 'main'}, at=round(c.L(3) - 0.2, 2), label='Configurações de NPS')
    c.waitfor(text='Configurações de NPS', timeout=10)
    c.hover(TXT('Pergunta da escala', exact=False, within=DLG), 0.4, at=c.A(3, 'pergunta', 0.9), label='Pergunta da escala')
    c.hover(TXT('Critérios de avaliação', within=DLG), 0.4, at=c.A(3, 'critérios', 0.9), label='Critérios de avaliação')
    c.hover(SEL(f'{DLG} input', nth=0), 0.2, at=c.A(3, 'Qualidade,', 0.9), label='critério Qualidade')
    c.hover(SEL(f'{DLG} input', nth=1), 0.2, at=c.A(3, 'Pontualidade', 0.9), label='critério Pontualidade')
    c.scroll(None, label='desce um pouco na janela', by=160, point={'x': 640, 'y': 420})
    c.hover(SEL(f'{DLG} input', nth=2), 0.3, at=c.A(3, 'Profissionalismo.', 0.9), label='critério Profissionalismo')
    c.scroll(None, at=c.A(3, 'tem', 0.9), label='desce até a Avaliação no Google', by=800, point={'x': 640, 'y': 420})
    c.hover(TXT('Avaliação no Google', within=DLG), 0.4, at=c.A(3, 'Google,', 0.9), label='Avaliação no Google')
    c.hover(SEL(f'{DLG} input[placeholder*="g.page"]'), 2.0, at=c.A(3, 'link', 0.9), label='link da avaliação do Google')
    c.click(BTN('Cancelar'), at=c.A(3, 'cliente.', 0.4), label='Cancelar')
    c.fim()
    return c


# ================================================================ capítulos 12 a 14 (Agenda)
SETUP_AGENDA = SETUP_APP('/agenda', 'Visualize e gerencie os agendamentos')
CELULA = lambda n: f'main .grid-cols-7.flex-1 > div:nth-child({n})'   # célula do mês (n = dia do mês de novembro de 2026, que começa no domingo)


def cap12():
    c = Cap(12, pace=0.3, cps=14, start=(900, 480), prewarm=['/ordens-servico', '/agenda'], setup=SETUP_OS)
    c.mark(1)
    c.click(LINK('Agenda'), at=0.1, label='menu: Agenda')
    c.waitfor(text='Visualize e gerencie os agendamentos', timeout=12)
    c.hover(LINK('Dashboard'), 0.4, at=c.A(1, 'Dashboard.', 0.7), label='menu: Dashboard, logo acima')
    # cada hover custa de 0,9 a 1,5 s (o da aba Mês até o dia 5 leva ~1,5 s): o cursor sai ANTES da palavra para chegar nela
    c.hover(TAB('Mês'), 0.3, at=c.A(1, 'computador', 0.6), label='visão Mês')
    c.hover(TXT('#12', within='main'), 0.5, at=c.A(1, 'ordens', 1.6), label='uma OS no dia 5')
    c.hover(TXT('Entregar material no Hotel Mirante do Mar', exact=False, within='main'), 0.5, at=c.A(1, 'tarefas', 0.5), label='uma tarefa no dia 4')
    c.hover(TXT('Finados', exact=False, within='main'), 0.8, at=c.A(1, 'feriados', 0.8), label='feriado: Finados')
    c.mark(2)
    c.click(TAB('Semana'), at=c.A(2, 'Semana', 0.8), label='visão Semana')
    c.click(TAB('Dia'), at=c.A(2, 'Dia,', 0.8), label='visão Dia')
    c.click(BTN('Hoje'), at=c.A(2, 'Hoje', 0.1), label='Hoje')
    c.click(TAB('Mês'), label='volta ao Mês')
    c.mark(3)
    c.click(TAB('Lista'), at=c.A(3, 'Lista,', 0.8), label='visão Lista')
    c.hover(TXT('atrasado', exact=False, within='main'), 0.3, at=c.A(3, 'atrasado.', 0.8), label='seção Atrasado')
    c.click(TAB('Calendário'), label='volta ao Calendário')
    c.mark(4)
    # A narração ganhou duas pausas (t5/narracao/pausas.py: 4 s antes de "Os filtros" e 1,2 s antes de "E a legenda"): a janela de
    # filtros leva ~2 s para abrir e desenhar as listas, e o primeiro gesto dentro dela espera esse tempo. O clique em Filtros sai logo
    # depois da volta ao Calendário, dentro da primeira pausa; a janela fecha dentro da segunda. Lição do T5, cap. 12.
    c.click(BTN('Filtros'), label='Filtros')
    # cada hover na janela de filtros custa ~1 s (o cursor atravessa a janela): só o Técnico e o Tipo ganham gesto; Cliente e Status
    # passam na rolagem
    c.hover(TXT('Técnico', exact=False, within=DLG), 0.1, at=c.A(4, 'técnico,', 2.3), label='filtro Técnico')
    # o cursor fica na faixa de margem da janela (x=842): a roda rola a janela inteira e não a lista de clientes
    c.scroll(None, at=c.A(4, 'status', 1.4), label='desce até Status e Tipo', by=613, point={'x': 842, 'y': 450})
    c.hover(TXT('Tipo', exact=False, within=DLG), 0.1, at=c.A(4, 'tipo.', 1.4), label='filtro Tipo')
    # a agenda rola por trás da janela (escurecida): ao fechar, a legenda já está à vista
    c.ev('document.querySelector("main").scrollTo({top: 140})', label='rola a agenda por trás da janela')
    c.clicar_fixo(f'{DLG} button', (1056, 768), at=c.A(4, 'legenda', 1.2), label='fecha os filtros', texto='fechar', ultimo=True)
    c.clicar_fixo('main button', (868, 712), at=c.A(4, 'legenda', -0.4), label='legenda: ver todos os tipos', texto='Ver todos')
    c.fim()
    return c


def cap13():
    c = Cap(13, pace=0.3, cps=14, start=(900, 480), prewarm=['/agenda'], setup=SETUP_AGENDA)
    TAREFA = SEL(f'{DLG} button', hasText='Tarefa')
    c.mark(1)
    c.click(BTN('Nova Tarefa/OS'), at=c.A(1, 'Nova', 0.9), label='Nova Tarefa/OS')
    c.waitfor(text='O que deseja criar?', timeout=10)
    c.hover(SEL(f'{DLG} button', hasText='Ordem de Serviço'), 0.5, at=c.A(1, 'ordem', 0.7), label='opção Ordem de Serviço')
    c.hover(TAREFA, 0.4, at=c.A(1, 'tarefa.', 0.7, 1), label='opção Tarefa')
    c.press('Escape', at=c.A(1, 'Também', 0.5), label='fecha a janela')
    c.dblclick(SEL(CELULA(9) + ' span', nth=0), at=c.A(1, 'cliques', 1.2), label='dois cliques no dia 9')
    c.waitfor(text='O que deseja criar?', timeout=10)
    # a escolha da Tarefa e a abertura do formulário cabem no fim da linha 1: o título (32 letras, ~3,3 s mesmo a 30 cps, porque cada tecla
    # espera a página) já começa a ser digitado quando a fala diz "Vou criar uma tarefa" e termina junto com "da equipe"
    c.click(TAREFA, label='escolhe Tarefa')
    c.waitfor(text='Título da Tarefa', timeout=10)
    c.mark(2)
    c.type(SEL(f'{DLG} input', nth=0), 'Reunião de alinhamento da equipe', at=round(c.L(2) + 0.05, 2), cps=30, noClick=True, label='título da tarefa')
    # daqui até "Criar Tarefa" os passos correm um atrás do outro (cada clique ~0,85 s); o `at` só segura o passo que adiantaria demais
    c.click(SEL(f'{DLG} button[role=combobox]', hasText='Nenhum', nth=1), at=c.A(2, 'tipo', 0.9), label='campo Tipo de Tarefa')
    c.click({'role': 'option', 'name': 'Reunião'}, label='tipo Reunião')
    c.click(SEL(f'{DLG} button[role=combobox]', hasText='Selecione...'), at=c.A(2, 'escolho', 1.5), label='campo Responsáveis')
    c.click(TXT('Bruno Alves', within=POP), label='Bruno Alves')
    c.click(TXT('Lucas Ferreira', within=POP), label='Lucas Ferreira')
    c.press('Escape', label='fecha o seletor')
    c.hover(SEL(f'{DLG} button', hasText='09/11/2026'), 0.2, at=c.A(2, 'data,', 0.3), label='Data')
    c.hover(SEL(f'{DLG} input[type=time]'), 0.2, at=c.A(2, 'horário', 0.0), label='Horário')
    c.hover(SEL(f'{DLG} input', nth=2), 0.2, at=c.A(2, 'duração.', 0.2), label='Duração')
    c.click(BTN('Criar Tarefa'), at=c.A(2, 'Criar', 0.6, 1), label='Criar Tarefa')
    c.hover(TXT('Reunião de alinhamento da equipe', exact=False, within='main'), 1.4, at=c.A(2, 'compromisso', 0.5), label='a tarefa no dia 9')
    c.hover(TXT('#13', within='main'), 0.8, at=c.A(2, 'apenas', 0.7), label='uma OS no mesmo dia')
    c.mark(3)
    c.hover(TXT('#16', within='main'), 1.0, at=c.A(3, 'arrastar', 1.0), label='a OS #16 na terça')
    c.hover(SEL(CELULA(11)), 0.5, at=c.A(3, 'dia.', 0.8), label='o novo dia: quarta, 11')
    c.drag(TXT('#16', within='main'), SEL(CELULA(11)), at=c.A(3, 'conferir', 1.0), label='arrasta a OS #16 da terça para a quarta')
    c.waitfor(text='OS reagendada com sucesso!', timeout=10)
    c.hover(TXT('#16', within='main'), 1.9, at=c.A(3, 'dezesseis', 0.9), label='a OS #16 agora na quarta')
    c.fim()
    return c



# ---------------------------------------------------------------- capítulo 14 (Agenda: pausadas, busca e resumo)
PAINEL = {'x': 1090, 'y': 520}   # painel "Resumo da OS" da Agenda: a roda do mouse rola o conteúdo dele (rolagem interna)


def cap14():
    c = Cap(14, pace=0.3, cps=14, start=(900, 480), prewarm=['/agenda'], setup=SETUP_AGENDA)
    BUSCAR = {'role': 'button', 'name': 'Buscar OS ou tarefa'}
    CAMPO = {'placeholder': 'Número da OS, cliente, descrição, técnico...'}
    c.mark(1)
    c.click(BTN('OS Pausadas'), at=c.A(1, 'Pausadas', 1.4), label='OS Pausadas')
    c.waitfor(text='Retomar agora', timeout=10)
    c.hover(TXT('Restaurante Sabor da Serra', within=DLG), 0.8, at=c.A(1, 'lista', 0.7), label='a OS pausada na lista')
    c.hover(TXT('Pausada há cerca de', exact=False, within=DLG), 1.5, at=c.A(1, 'tempo', 0.8), label='o tempo que está parada')
    c.click(BTN('Retomar agora'), at=c.A(1, 'Retomar', 0.8), label='Retomar agora')
    c.hover(TXT('#8', within='main'), 0.6, at=c.A(1, 'volta', 0.5), label='a OS #8 de volta à agenda')
    c.mark(2)
    c.click(BUSCAR, at=c.A(2, 'achar', 0.4), label='Pesquisar')
    c.type(CAMPO, 'Monte', at=c.A(2, 'pesquisar', 0.3), cps=14, noClick=True, label='busca Monte')  # 5 letras bastam e não atrasam o primeiro resultado (como no cap. 8)
    c.hover(TXT('#16', exact=False, within=DLG), 0.4, at=c.A(2, 'número,', 0.3), label='resultado: o número da OS')
    c.hover(TXT('Colégio Monte Verde', within=DLG), 0.4, at=c.A(2, 'cliente,', 0.4), label='resultado: o cliente')
    c.hover(TXT('Manutenção preventiva', within=DLG), 0.4, at=c.A(2, 'descrição', 0.4), label='resultado: a descrição')
    c.hover(TXT('Rafael Lima', within=DLG), 0.4, at=c.A(2, 'técnico.', 0.6), label='resultado: o técnico')
    c.press('Escape', label='fecha a busca')
    c.mark(3)
    c.click(TXT('#8', within='main'), at=round(c.L(3) - 0.2, 2), label='abre o resumo da OS #8')
    c.waitfor(text='Resumo da OS', timeout=8)
    c.scroll(None, at=c.A(3, 'abre', 0.1), label='rola o resumo até os responsáveis', by=150, point=PAINEL)
    c.hover(TXT('Responsáveis', within='main'), 0.6, at=c.A(3, 'responsáveis,', 0.5), label='Responsáveis')
    c.hover(TXT('Descrição', within='main'), 0.6, at=c.A(3, 'descrição', 0.5), label='Descrição')
    c.scroll(None, at=c.A(3, 'linha', 0.7), label='rola o resumo até a linha do tempo', by=170, point=PAINEL)
    c.hover(TXT('Linha do tempo', within='main'), 0.3, at=c.A(3, 'tempo.', 0.9), label='Linha do tempo')
    c.click(SEL('main button', hasText='Ações'), at=c.A(3, 'Ações', 0.6), label='menu Ações')
    c.hover({'role': 'menuitem', 'name': 'Editar'}, 0.2, at=c.A(3, 'editar,', 1.0), label='Ações: Editar')
    c.hover({'role': 'menuitem', 'name': 'Pausar OS'}, 0.2, at=c.A(3, 'pausar,', 0.5), label='Ações: Pausar OS')
    c.hover({'role': 'menuitem', 'name': 'Faturar OS'}, 0.2, at=c.A(3, 'faturar', 0.5), label='Ações: Faturar OS')
    c.hover({'role': 'menuitem', 'name': 'Copiar link de acompanhamento'}, 1.6, at=c.A(3, 'copiar', 0.5), label='Ações: Copiar link de acompanhamento')
    c.press('Escape', at=c.A(3, 'botão', 0.5), label='fecha o menu Ações')
    c.hover(SEL('main button', hasText='Preencher OS'), 4.5, at=c.A(3, 'Preencher', 0.5), label='botão Preencher OS')
    c.fim()
    return c


# ---------------------------------------------------------------- capítulos 16 e 17 (Mapa ao Vivo e recapitulação)
# marcadores do Leaflet pela cor (Base teal, Bruno "A Caminho" índigo, Júlia "Executando OS" verde, Lucas "Check-out" vermelho 16 px, destino vermelho 20 px)
MARC_BRUNO = SEL('.leaflet-marker-icon:has(div[style*="#6366f1"])')
MARC_JULIA = SEL('.leaflet-marker-icon:has(div[style*="#22c55e"])')
MARC_LUCAS = SEL('.leaflet-marker-icon:has(div[style*="width:16px"][style*="#ef4444"])')
MARC_DESTINO = SEL('.leaflet-marker-icon:has(div[style*="width:20px"])')
POPUP = '.leaflet-popup-content'
SETUP_MAPA = SETUP_APP('/mapa-ao-vivo', 'Posição em tempo real e histórico de deslocamentos')


def cap16():
    c = Cap(16, pace=0.3, cps=14, start=(900, 480), prewarm=['/agenda', '/mapa-ao-vivo'], setup=SETUP_AGENDA)
    c.mark(1)
    c.hover(LINK('Agenda'), 0.5, at=0.4, label='a Agenda, onde o tutorial anterior parou')
    # A ilustração cobre o palco de 2,4 s a 15,6 s: o app já vai ao mapa por baixo dela e o primeiro hover num marcador também acontece
    # ali. O mapa (MapLibre em WebGL por software, 2x) trava a página por 3 a 11 s no primeiro gesto depois de carregar: o aquecimento
    # sai logo que o marcador existe (sem `at`) e a narração ganhou uma pausa de 3 s entre o fim da ilustração e "No menu Operacional"
    # (t5/narracao/pausas.py) para o que sobrar do trava terminar antes dos hovers da linha 2. Lição do T5, cap. 16.
    c.click(OPERACIONAL, at=2.6, label='vai ao grupo Operacional (sob a ilustração)')
    c.click(LINK('Mapa e Rastreamento'), at=3.6, label='vai ao Mapa e Rastreamento (sob a ilustração)')
    c.waitfor(selector='.leaflet-marker-icon', timeout=20)
    c.hover(MARC_BRUNO, 0.5, label='aquece o mapa (sob a ilustração)')
    c.mark(2)
    c.hover(OPERACIONAL, 0.3, at=c.A(2, 'Operacional,', 0.8), label='menu: Operacional')
    c.hover(LINK('Mapa e Rastreamento'), 0.4, at=c.A(2, 'Mapa', 0.7), label='menu: Mapa e Rastreamento')
    c.hover(MARC_BRUNO, 0.5, at=c.A(2, 'marcador', 0.5), label='marcador do Bruno')
    c.hover(MARC_JULIA, 0.5, at=c.A(2, 'técnico', 0.5), label='marcador da Júlia')
    c.hover(MARC_LUCAS, 0.5, at=c.A(2, 'horas,', 0.9), label='marcador do Lucas')
    c.hover(TXT('A Caminho', within='main'), 0.6, at=c.A(2, 'caminho,', 0.5), label='legenda: A Caminho')
    c.hover(TXT('Executando OS', within='main'), 0.6, at=c.A(2, 'executando', 0.5), label='legenda: Executando OS')
    c.hover(TXT('Check-out', within='main'), 1.0, at=c.A(2, 'saída.', 0.9), label='legenda: Check-out')
    c.mark(3)
    c.click(MARC_BRUNO, at=round(c.L(3) - 0.2, 2), label='clica no marcador do Bruno')
    c.waitfor(text='OS vinculada', timeout=8)
    c.hover(TXT('OS vinculada', within=POPUP), 0.6, at=c.A(3, 'OS', 0.5), label='popup: OS vinculada')
    c.hover(TXT('Última atualização', exact=False, within=POPUP), 0.6, at=c.A(3, 'última', 0.5), label='popup: última atualização')
    c.hover(TXT('Chegada em', exact=False, within=POPUP), 0.8, at=c.A(3, 'quanto', 0.6), label='popup: chegada em ~5 min')
    c.hover(MARC_DESTINO, 1.5, at=c.A(3, 'linha', 0.5), label='a linha até o destino do cliente')
    c.mark(4)
    c.click(BTN('Atualizar'), at=round(c.L(4) - 0.2, 2), label='Atualizar')
    c.mark(5)
    c.click(TAB('Histórico'), at=c.A(5, 'Histórico', 1.2), label='aba Histórico')
    c.click({'role': 'combobox', 'hasText': 'Todos os técnicos'}, at=c.A(5, 'escolhe', 0.8), label='campo Técnico')
    c.click({'role': 'option', 'name': 'Júlia Santos'}, label='Júlia Santos')
    c.hover(TXT('Check-in', exact=False, within='main', nth=1), 0.3, at=c.A(5, 'deslocamentos,', 0.6), label='os deslocamentos do dia')
    c.hover(TXT('Distância total', within='main'), 0.6, at=c.A(5, 'distância', 0.6), label='Distância total')
    c.hover(TXT('Tempo em campo', within='main'), 1.2, at=c.A(5, 'tempo', 0.6), label='Tempo em campo')
    c.fim()
    return c


def cap17():
    # A narração ganhou três pausas (t5/narracao/pausas.py: 1,5 s depois de "todo mês.", 3 s antes de "Depois montou" e 4 s antes de
    # "No próximo tutorial"): o Kanban, a aba NPS e o mapa levam ~2 a 6 s para desenhar. Lição do T5, cap. 17.
    # O recap tem 9 gestos de menu e página em ~9 s de fala: o grupo Gestão, o link de Funcionários, o grupo Operacional vão por eval
    # (time-lapse, sem cursor; o grupo que contém a página aberta já vem aberto e um clique a mais o fecharia). O cursor fica nos
    # cartões, nos botões da fala e nos cliques de Agenda, aba Equipes e Mapa. Lição do T5, cap. 17.
    c = Cap(17, pace=0.3, cps=14, start=(900, 480), prewarm=['/ordens-servico', '/agenda', '/funcionarios', '/mapa-ao-vivo'], setup=SETUP_OS)
    LINK_FUNC = js_clicar_expr("[...document.querySelectorAll('a')].find(x=>x.textContent.trim()==='Funcionários (RH)')")
    c.mark(1)
    c.click(BTN('Nova OS'), at=c.A(1, 'abriu', 0.5), label='Nova OS')
    c.waitfor(text='Nova Ordem de Serviço', timeout=10)
    c.hover(TXT('Cliente e Serviço', within=DLG), 0.4, at=c.A(1, 'cliente,', 0.5), label='etapa Cliente e Serviço')
    c.hover(TXT('Orçamento', within=DLG), 0.4, at=c.A(1, 'orçamento,', 0.5), label='etapa Orçamento')
    c.hover(TXT('Equipamentos e Checklists', within=DLG), 1.0, at=c.A(1, 'equipamento', 0.5), label='etapa Equipamentos e Checklists')
    c.click(SEL(f'{DLG} button', hasText='fechar'), at=c.A(1, 'criou', 1.2), label='fecha a Nova OS')
    c.scroll(None, at=c.A(1, 'série', 0.5), label='desce até o Kanban', by=330, point=MAIN_TOP)
    # um só cartão da série (cada hover custa ~1 s e a fala cita um mês só): o 4º da coluna fica cortado e faria o robô rolar a coluna ~2 s
    c.hover(TXT('HIG-2026-17', within='main'), 0.4, at=c.A(1, 'repete', 0.4), label='cartão da série: novembro')
    c.ev('document.querySelector("main").scrollTo({top: 0})', at=c.A(1, 'Acompanhou', 0.3), label='volta ao topo (time-lapse)')
    c.hover(BTN('Configurações', within='main'), 0.2, at=c.A(1, 'status,', 2.2), label='Configurações (status)')   # o hover logo depois do salto ao topo leva ~2,1 s
    c.hover(BTN('Filtros'), 0.2, at=c.A(1, 'filtros', 0.6), label='Filtros e busca (o funil fica dentro do campo)')
    c.click(TAB('NPS e Satisfação'), at=c.A(1, 'viu', 0.8), label='aba NPS e Satisfação')
    c.ev(js_kpis(), label='cartões de KPI (animação)')
    c.waitfor(text='Média por Categoria', timeout=12)
    c.mark(2)
    c.click(LINK('Agenda'), at=round(c.L(2) - 0.2, 2), label='menu: Agenda')
    c.waitfor(text='Visualize e gerencie os agendamentos', timeout=15)
    c.hover(TXT('#16', within='main'), 0.5, at=c.A(2, 'reagendamento,', 0.6), label='a OS reagendada na quarta')
    c.ev(js_abrir_grupo('Gestão', 'Funcionários (RH)'), at=c.A(2, 'criou', 0.5), label='abre o grupo Gestão (time-lapse)')
    c.waitfor(target=LINK('Funcionários (RH)'), timeout=10)
    c.ev(LINK_FUNC, label='menu: Funcionários (RH) (time-lapse)')
    c.click(TAB('Equipes'), label='aba Equipes')
    c.hover(TXT('Equipe Alfa', within='main'), 0.8, at=c.A(2, 'mais', 0.1), label='a Equipe Alfa')
    c.ev(js_abrir_grupo('Operacional', 'Mapa e Rastreamento'), at=c.A(2, 'acompanhou', 0.4), label='abre o grupo Operacional (time-lapse)')
    c.waitfor(target=LINK('Mapa e Rastreamento'), timeout=10)
    c.click(LINK('Mapa e Rastreamento'), label='menu: Mapa e Rastreamento')
    c.waitfor(selector='.leaflet-marker-icon', timeout=20)
    # o primeiro gesto no mapa (MapLibre em WebGL por software) trava a página por 3 s ou mais: o aquecimento cai na folga antes da fala
    c.hover(MARC_BRUNO, 0.3, label='aquece o mapa')
    c.mark(3)
    c.hover(MARC_BRUNO, 0.8, at=c.A(3, 'olhos', 0.6), label='o técnico no mapa')
    c.click(MARC_BRUNO, at=c.A(3, 'celular:', 0.3), label='abre o técnico no mapa')
    c.hover(TXT('OS vinculada', within=POPUP), 2.5, at=c.A(3, 'relatório', 0.5), label='a OS do técnico')
    c.fim()
    return c


# ---------------------------------------------------------------- capítulo 15 (Equipes)
LISTA_MEMBROS = f'{DLG} div[class*="max-h-[200px]"]'   # caixa "Membros" do formulário da equipe (rolagem própria, 200 px)


def js_rolar_fim(sel):
    """rola de forma suave (scrollTo smooth) até o fim o container com rolagem que contém `sel`: o que fica no fim (a lista de
    Membros) aparece inteiro e dentro da faixa do robô, e o clique seguinte não rola em vão. Lição do T5, cap. 15."""
    return ('(()=>{const el=document.querySelector(%s);if(!el)return false;for(let n=el.parentElement;n&&n!==document.documentElement;n=n.parentElement){'
            'const s=getComputedStyle(n);if(/(auto|scroll)/.test(s.overflowY)&&n.scrollHeight>n.clientHeight+4){n.scrollTo({top:n.scrollHeight,behavior:"smooth"});return true}}return false})()') % json.dumps(sel)


def js_clicar_expr(expr):
    """clique instantâneo no elemento que a expressão JS `expr` devolve ('SEM ALVO' no log do robô se ele não existe)"""
    return f"(()=>{{const e={expr};if(!e)return 'SEM ALVO';e.click();return 1}})()"


def js_opcao_pop(nome):
    """clique instantâneo na opção `nome` de uma lista aberta num popover (cmdk/Radix): o item é o elemento folha com esse texto"""
    return js_clicar_expr(f"[...document.querySelectorAll('[data-radix-popper-content-wrapper] *')].find(x=>x.children.length===0&&x.textContent.trim()==={json.dumps(nome)})")


def js_abrir_grupo(grupo, filho):
    """abre o grupo do menu lateral só se ainda estiver fechado: o grupo que contém a página aberta já vem aberto e um clique a mais
    o fecharia (o link some do DOM e o robô esperaria 30 s por ele). Lição do T5, cap. 17."""
    return ("(()=>{if([...document.querySelectorAll('a')].some(a=>a.textContent.trim()===%s))return 'já aberto';"
            "const b=[...document.querySelectorAll('button')].find(x=>x.textContent.trim()===%s);if(!b)return 'SEM ALVO';b.click();return 1})()"
            % (json.dumps(filho), json.dumps(grupo)))


def cap15():
    c = Cap(15, pace=0.25, cps=14, start=(900, 480), prewarm=['/agenda', '/funcionarios', '/ordens-servico'], setup=SETUP_AGENDA)
    NOME = {'placeholder': 'Nome da equipe'}
    PROX = js_clicar(f'{DLG} button', '^Próximo')
    campo = lambda rot: js_clicar_expr(f"[...document.querySelectorAll('[role=dialog] button')].find(x=>(x.getAttribute('aria-label')||x.textContent).includes('{rot}'))")
    opcao = lambda lista, n: js_clicar_expr(f"[...document.querySelectorAll('[role=listbox][aria-label={lista}] [role=option]')].find(x=>x.textContent.trim()==='{n}')")
    CONCLUIR = js_clicar_expr("[...document.querySelectorAll('button')].find(x=>x.textContent.trim()==='Concluir')")
    PERIODO = f'{DLG} section:has(svg.lucide-calendar)'      # "Período do atendimento" (a "Revisão do escopo" não tem calendário)
    # O campo Cliente é um Select do Radix: o `.click()` por eval NÃO abre (ele abre com pointerdown de mouse de verdade, e um PointerEvent
    # sintético também não bastou); com o foco no campo, a tecla Enter abre a lista. A opção, depois de aberta, aceita `.click()`.
    # Lição do T5, cap. 15.
    foco_cliente = ("(()=>{const el=[...document.querySelectorAll('[role=combobox]')].find(x=>x.textContent.includes('Selecione o cliente'));"
                    "if(!el)return 'SEM ALVO';el.focus();return document.activeElement===el})()")
    opcao_cliente = js_clicar_expr("[...document.querySelectorAll('[role=option]')].find(x=>x.textContent.trim().startsWith('Pousada Sol Nascente'))")
    abrir_servicos = js_clicar_expr("[...document.querySelectorAll('[role=dialog] button[role=combobox]')].find(x=>x.textContent.includes('Adicionar serviços'))")
    # ---- L1: onde ficam as equipes
    c.mark(1)
    c.click(GESTAO, at=c.A(1, 'Gestão,', 0.8), label='abre o grupo Gestão')
    c.click(LINK('Funcionários (RH)'), at=c.A(1, 'Funcionários,', 0.8), label='menu: Funcionários (RH)')
    c.click(TAB('Equipes'), at=c.A(1, 'Equipes,', 0.9), label='aba Equipes')
    c.waitfor(text='Nenhuma equipe cadastrada', timeout=10)
    c.hover(TXT('Funcionários (RH)', within='main'), 0.5, at=c.A(1, 'RH.', 0.8), label='o módulo de RH')
    # ---- L2: criar a Equipe Alfa
    c.mark(2)
    c.click(BTN('Nova Equipe'), at=round(c.L(2) - 0.5, 2), label='Nova Equipe')
    c.waitfor(text='Visual da Equipe', timeout=10)
    c.click(NOME, at=c.A(2, 'dou', 0.5), label='campo Nome')
    c.type(NOME, 'Equipe Alfa', at=c.A(2, 'nome:', 0.1), cps=14, noClick=True, label='nome Equipe Alfa')
    c.ev(js_rolar_fim(LISTA_MEMBROS), label='leva a lista de membros à vista (rolagem suave)')
    c.hover(SEL(f'{DLG} input[type=color]'), 0.5, at=c.A(2, 'cor', 0.7), label='cor da equipe')
    c.click(SEL(f'{DLG} button:has(svg.lucide-hard-hat)'), at=c.A(2, 'ícone,', 0.3), label='ícone')
    c.click(TXT('Bruno Alves', within=DLG), at=c.A(2, 'Bruno', 0.6), label='Bruno Alves')
    c.click(TXT('Lucas Ferreira', within=DLG), at=c.A(2, 'Lucas', 0.5), label='Lucas Ferreira')
    c.click(BTN('Criar Equipe'), at=c.A(2, 'Criar', 0.2), label='Criar Equipe')
    # ---- L3: a OS da Pousada Sol Nascente, com a equipe
    # A fala descreve 8 escolhas em ~7 s; o robô gasta ~1 s por clique com cursor. O caminho do menu, as opções das listas, os "Próximo",
    # a data e as horas vão por eval (time-lapse, sem cursor); o cursor fica nos itens que a fala cita (Nova OS, os campos de Serviço
    # e Cliente, o equipamento, Responsáveis/Equipes e o resultado em "Quando começa"). Lição do T5, cap. 15.
    GRUPO_OPERACIONAL = ("(()=>{if([...document.querySelectorAll('a')].some(a=>a.textContent.trim()==='Ordens de Serviço'))return 'já aberto';"
                         "const b=[...document.querySelectorAll('button')].find(x=>x.textContent.trim()==='Operacional');if(!b)return 'SEM ALVO';b.click();return 1})()")
    LINK_OS = js_clicar_expr("[...document.querySelectorAll('a')].find(x=>x.textContent.trim()==='Ordens de Serviço')")
    LINK_AGENDA = js_clicar_expr("[...document.querySelectorAll('a')].find(x=>x.textContent.trim()==='Agenda')")
    OPCAO_POP = lambda n: js_clicar_expr(f"[...document.querySelectorAll('[data-radix-popper-content-wrapper] *')].find(x=>x.children.length===0&&x.textContent.trim()==='{n}')")
    BOTAO_DATA = js_clicar_expr(f"document.querySelector('{PERIODO}')?.querySelector('button:has(svg.lucide-calendar)')")
    DIA_11 = js_clicar_expr("[...document.querySelectorAll('[role=gridcell]')].find(x=>x.textContent.trim()==='11'&&!x.disabled)")
    c.mark(3)
    # sem esperar a janela da equipe fechar: a equipe é gravada em segundo plano e a janela some com a troca de página. A narração
    # ganhou pausas (t5/narracao/pausas.py: 1,5 s antes de "Agora", 4 s antes de "Na quarta" e 3,8 s antes de "Na agenda") para o
    # ritmo real do app: as páginas e os seletores levam ~1 s cada, e "Criar OS" só termina ~4,7 s depois do clique. Lição do T5, cap. 15.
    c.ev(GRUPO_OPERACIONAL, label='abre o grupo Operacional (acelerado)')
    c.waitfor(selector='a:has-text("Ordens de Serviço")', timeout=8)  # por CSS: com a janela aberta o menu fica aria-hidden e o papel `link` não casa
    c.ev(LINK_OS, label='menu: Ordens de Serviço (acelerado)')
    c.waitfor(text='Gerencie suas ordens de serviço', timeout=15)
    # a janela da Nova OS abre durante a pausa que precede "Agora, numa nova ordem". O clique com cursor levava ~3 s (a página das OS
    # ainda desenha o Kanban) e empurrava a fala em 1 s; por eval a janela abre na hora. Lição do T5, cap. 15.
    c.ev(js_clicar_expr("[...document.querySelectorAll('button')].find(x=>x.textContent.trim()==='Nova OS')"), label='Nova OS (acelerado)')
    c.waitfor(text='Nova Ordem de Serviço', timeout=10)
    c.ev(abrir_servicos, at=c.A(3, 'Carga', 1.4), label='abre a lista de serviços (acelerado)')
    c.waitfor(text='Carga de Gás', timeout=6)
    c.ev(OPCAO_POP('Carga de Gás'), label='Carga de Gás (acelerado)')
    c.press('Escape', label='fecha a lista de serviços')
    c.ev(foco_cliente, at=c.A(3, 'Pousada', 0.9), label='foca o campo Cliente (acelerado)')
    c.press('Enter', label='abre a lista de clientes')
    c.waitfor(selector='[role=option]:has-text("Pousada Sol Nascente")', timeout=6)
    c.ev(opcao_cliente, label='Pousada Sol Nascente (acelerado)')
    c.ev(PROX, label='Próximo (acelerado)')
    c.waitfor(text='Serviços, mão de obra e materiais', timeout=10)
    c.ev(PROX, label='Próximo (acelerado, Equipamentos)')
    c.waitfor(text='Selecione o equipamento.', timeout=10)
    c.click({'role': 'checkbox', 'within': DLG}, at=c.A(3, 'Cassete', 0.3), label='marca o Cassete 36.000 BTUs')
    c.waitfor(target={'role': 'checkbox', 'within': DLG, 'checked': True}, timeout=8)
    c.ev(PROX, label='Próximo (acelerado, Agendamento e Detalhes)')
    c.waitfor(text='Revisão do escopo da OS', timeout=10)
    c.click(RESP_VAZIO, at=c.A(3, 'Responsáveis', 0.6), label='campo Responsáveis')
    c.hover(TXT('Equipes', exact=False, within=POP), 0.4, at=c.A(3, 'seção', 0.5), label='a seção Equipes')
    c.click(TXT('Equipe Alfa', within=POP), at=c.A(3, 'Equipe', 0.6, 1), label='Equipe Alfa')
    c.hover(TXT('Lucas Ferreira', within=POP), 0.5, at=c.A(3, 'dois', 0.5), label='os dois membros marcados')
    c.press('Escape', label='fecha o seletor')
    # data e horas em "time-lapse" (por eval) dentro da pausa da narração: o fim primeiro (16:00) e o início depois (14:00), para a
    # mensagem de término inválido nunca aparecer
    # roda do mouse com a quantidade fixa: o "revelar alvo" do robô gastava ~2 s; com 1 aparelho na revisão do escopo, o botão
    # "Quando começa" está em css y 661 (cortado pela borda da janela) e 280 px de rolagem o levam ao meio da janela
    c._p({'do': 'scroll', 'point': {'x': 640, 'y': 420}, 'by': 280, 'duration': 0.4, 'after': 0}, None, 'leva o Período do atendimento à vista (rolagem)', {})
    c.ev(BOTAO_DATA, label='Data inicial (acelerado)')
    c.waitfor(selector='[role=gridcell]', timeout=8)
    c.ev(DIA_11, label='quarta, dia 11 (acelerado)')
    # sem a espera pelo fechamento o próximo seletor abria por cima do anterior e a hora 14 caía no campo errado (a máquina sem
    # concorrência é rápida: o `waitFor` da lista achava a lista antiga ainda saindo). Lição do T5, cap. 15.
    c.waitfor(gone=SEL('[role=gridcell]'), timeout=6)
    c.ev(campo('Quando termina'), label='Quando termina (acelerado)')
    c.waitfor(selector='[role=listbox][aria-label=Horas]', timeout=8)
    c.ev(opcao('Horas', '16'), label='hora 16')
    c.ev(opcao('Minutos', '00'), label='minuto 00')
    c.ev(CONCLUIR, label='Concluir (fim)')
    c.waitfor(gone=SEL('[role=listbox][aria-label=Horas]'), timeout=6)
    c.ev(campo('Quando começa'), label='Quando começa (acelerado)')
    c.waitfor(selector='[role=listbox][aria-label=Horas]', timeout=8)
    c.ev(opcao('Horas', '14'), label='hora 14')
    c.ev(opcao('Minutos', '00'), label='minuto 00')
    c.ev(CONCLUIR, label='Concluir (início)')
    c.waitfor(gone=SEL('[role=listbox][aria-label=Horas]'), timeout=6)
    c.hover(SEL(f'{DLG} button[aria-label^="Quando começa"]'), 0.4, at=c.A(3, 'quarta,', 0.5), label='Quando começa: 14:00')
    c.click(BTN('Criar OS'), at=c.A(3, 'tarde.', 0.5), label='Criar OS')
    # ---- L4: a OS na Agenda, com a equipe. A página muda logo depois do clique (a OS é gravada em segundo plano) e o robô espera o
    # aviso "OS criada - Agendada para 11/11/2026 às 14:00": o trecho parado dessa espera é cortado na edição (specs.py, "cortes").
    c.mark(4)
    c.ev(LINK_AGENDA, label='menu: Agenda (acelerado)')
    c.waitfor(text='Visualize e gerencie os agendamentos', timeout=15)
    c.waitfor(text='Agendada para 11/11/2026', timeout=40)
    c.click(TXT('Pousada Sol Nascente', exact=False, within='main .grid-cols-7.flex-1'), at=c.A(4, 'ordem', 0.6), label='abre o resumo da OS na quarta')
    c.waitfor(text='Resumo da OS', timeout=8)
    c.hover(TXT('Equipe Alfa', within='main'), 1.4, label='Equipe Alfa no resumo')
    c.fim()
    return c


CAPS = {0: cap00, 1: cap01, 2: cap02, 3: cap03, 4: cap04, 5: cap05, 6: cap06, 7: cap07, 8: cap08, 9: cap09, 10: cap10, 11: cap11, 12: cap12, 13: cap13, 14: cap14, 15: cap15, 16: cap16, 17: cap17}

if __name__ == '__main__':
    quais = [int(a) for a in sys.argv[1:]] or sorted(CAPS)
    for n in quais:
        c = CAPS[n]()
        if os.environ.get('ANCHORS'):
            for i, w, t in c.anchors:
                print(f'   anchor L{i} "{w}" -> {t}')
        d = c.out()
        # o `at` precisa ser crescente
        last = -1
        for st in d['steps']:
            if 'at' in st:
                if st['at'] < last:
                    print(f'  aviso cap{n:02d}: at {st["at"]} < {last} em "{st.get("label") or st.get("name")}"')
                last = max(last, st['at'])
        path = os.path.join(HERE, f'cap{n:02d}.json')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
        print(f'cap{n:02d}: {len(d["steps"])} passos, narração {c.dur:.1f} s -> {os.path.relpath(path, HERE)}')
