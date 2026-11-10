#!/usr/bin/env python3
"""T4 · gera rec/t4/cap00..cap14.json (roteiros do robô) a partir da voz pronta (t4/narracao/capNN.json).

Os `at` saem da palavra que anuncia cada passo (A(linha, palavra, folga)): o clique "pousa" ~1 s depois do início do
passo, então `at` = início da palavra - folga. Rodar de qualquer pasta: `python3 rec/t4/gerar.py [NN ...]`.
Depois de gerar, confira com `node rec/record.mjs rec/t4/capNN.json --check`.
"""
import json, os, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
NARR = os.path.normpath(os.path.join(HERE, '..', '..', 't4', 'narracao'))

BASE = ['t3/apos-cap10', 't1/apos-cap13', 't4/inicio', 't4/g1-trilha', 't4/g2-vazias']  # 1.38.19: trilha sem onboarding
# estado de partida de cada capítulo (último apos-capNN que existe)
SEMENTE = {0: None, 1: None, 2: None, 3: 'apos-cap02', 4: 'apos-cap03', 5: 'apos-cap03', 6: 'apos-cap05', 7: 'apos-cap06',
           8: 'apos-cap07', 9: 'apos-cap08', 10: 'apos-cap09', 11: 'apos-cap10', 12: 'apos-cap11', 13: 'apos-cap12', 14: 'apos-cap12'}

# Observador de avisos de erro / tela escura / faixa da trilha Domiflix na tela (aceite da fase 1; copiado do T12)
OBS = ("(()=>{window.__avisos=[];const re=/N[ãa]o foi poss[ií]vel|erro|Tente novamente|indispon[ií]vel/i;const chk=(t)=>{t=(t||'').trim();"
       "const m=t&&t.match(new RegExp('[^]{0,40}('+re.source+')[^]{0,40}','i'));"
       "if(m&&window.__avisos.length<10)window.__avisos.push(m[0].replace(/[\\n\\r\\t ]+/g,' '))};new MutationObserver(ms=>{for(const m of ms){"
       "m.addedNodes.forEach(n=>chk(n.textContent));if(m.type==='characterData')chk(m.target.textContent)}}).observe(document.body,"
       "{childList:true,subtree:true,characterData:true});chk(document.body.innerText);"
       # tela escura de introdução e faixa de lembrete da trilha Domiflix (G1)
       "setInterval(()=>{const f=document.querySelector('section[aria-label^=\"Lembrete da trilha\"]');"
       "const e=[...document.querySelectorAll('div.fixed')].some(x=>getComputedStyle(x).backgroundColor==='rgb(17, 17, 17)');"
       "if((f||e)&&window.__avisos.length<10&&!window.__avisos.includes('TRILHA DOMIFLIX'))window.__avisos.push('TRILHA DOMIFLIX')},300);return 1})()")

NOMES = ['Abertura', 'A tela de Serviços', 'Categorias', 'Novo tipo de serviço', 'Organizando a lista', 'Dados fiscais',
         'Editar, desativar e excluir', 'Tipos de tarefa', 'Catálogo de modelos', 'Checklist do zero', 'As perguntas',
         'Combinando respostas', 'Organizar e conferir', 'Vincular e desativar', 'Recapitulando']


def norm(s):
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode().lower()
    return ''.join(ch for ch in s if ch.isalnum() or ch in '?')


class Cap:
    def __init__(s, n, pace=1.0, cps=9, start=(700, 420), prewarm=None, setup=None):
        s.n = n
        d = json.load(open(f'{NARR}/cap{n:02d}.json'))
        s.words, s.linhas, s.dur = d['words'], d['linhas'], d['dur']
        s.steps = []
        s.pace, s.cps, s.start = pace, cps, start
        s.prewarm = prewarm or ['/servicos']
        s.setup = setup or []
        s.anchors = []
        s.pending = []

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

    def click(s, target, at=None, label=None, **kw):
        d = {'do': 'click', 'target': target}
        if at is not None: d['at'] = at
        if label: d['label'] = label
        d.update(kw)
        return s.add(d)

    def hover(s, target, seconds=0.9, at=None, label=None, **kw):
        d = {'do': 'hover', 'target': target, 'seconds': seconds}
        if at is not None: d['at'] = at
        if label: d['label'] = label
        d.update(kw)
        return s.add(d)

    def type(s, target, text, at=None, label=None, cps=None, **kw):
        d = {'do': 'type', 'target': target, 'text': text}
        if cps: d['cps'] = cps
        if at is not None: d['at'] = at
        if label: d['label'] = label
        d.update(kw)
        return s.add(d)

    def select(s, target, option, at=None, label=None, **kw):
        d = {'do': 'select', 'target': target, 'option': option}
        if at is not None: d['at'] = at
        if label: d['label'] = label
        d.update(kw)
        return s.add(d)

    def press(s, key, at=None, label=None, **kw):
        d = {'do': 'press', 'key': key}
        if at is not None: d['at'] = at
        if label: d['label'] = label
        d.update(kw)
        return s.add(d)

    def scroll(s, target, at=None, label=None, **kw):
        d = {'do': 'scroll', 'target': target}
        if at is not None: d['at'] = at
        if label: d['label'] = label
        d.update(kw)
        return s.add(d)

    def pause(s, seconds):
        return s.add({'do': 'pause', 'seconds': seconds})

    def waitfor(s, **kw):
        return s.add({'do': 'waitFor', **kw})

    def drag(s, target, to, at=None, label=None, **kw):
        d = {'do': 'drag', 'target': target, 'to': to}
        if at is not None: d['at'] = at
        if label: d['label'] = label
        d.update(kw)
        return s.add(d)

    def ev(s, js, at=None, label=None):
        d = {'do': 'eval', 'js': js}
        if at is not None: d['at'] = at
        if label: d['label'] = label
        return s.add(d)

    def fim(s):
        if any(x.get('js') == OBS for x in s.setup):
            s.flush(1e9)
            s.steps.append({'do': 'eval', 'js': 'JSON.stringify(window.__avisos || "sem observador")', 'label': 'avisos de erro na tela'})
        s.flush(1e9)
        s.steps.append({'do': 'mark', 'name': 'FIM', 'at': round(s.dur, 2)})

    def out(s):
        sem = SEMENTE[s.n]
        d = {
            'name': f't4-cap{s.n:02d}',
            'title': f'T4 · Cap. {s.n} · {NOMES[s.n]} (narração {str(round(s.dur, 1)).replace(".", ",")} s; marcas L1..L{len(s.linhas)} = início de cada linha do roteiro)',
            'seed': f't4-cap{s.n:02d}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
            'start': {'x': s.start[0], 'y': s.start[1]},
            'seedExtra': BASE + ([f't4/{sem}'] if sem else []),
            'prewarm': s.prewarm, 'setup': s.setup, 'steps': s.steps,
        }
        return d


# ---------------------------------------------------------------- alvos
GESTAO = {'role': 'button', 'name': 'Gestão', 'exact': True}
LINK = lambda n: {'role': 'link', 'name': n, 'exact': True}
TAB_SERV = {'role': 'tab', 'name': 'Tipos de Serviços'}
TAB_TASK = {'role': 'tab', 'name': 'Tipos de Tarefas'}
TAB_CHK = {'role': 'tab', 'name': 'Checklists', 'exact': True}
BTN = lambda n: {'role': 'button', 'name': n, 'exact': True}
TXT = lambda t, **kw: {'text': t, 'exact': True, **kw}
SEL = lambda s, **kw: {'selector': s, **kw}
DLG = '[role=dialog]'
POP = '[data-radix-popper-content-wrapper]'
# interruptor com rótulo ao lado (modal/ficha de serviço e tarefa; "Ativo" do editor)
SWROW = lambda t: SEL(f'div.flex.items-center.gap-2:has(> label:text-is("{t}"))')
# regra do modal de pergunta (interruptor + rótulo + descrição)
RULEROW = lambda t: SEL(f'{DLG} div.flex.items-start.gap-3:has(label:text-is("{t}"))')
RULESW = lambda t: SEL(f'{DLG} div.flex.items-start.gap-3:has(label:text-is("{t}")) button[role=switch]')
CK_TRASH = SEL('button:has(svg.lucide-trash2):not([aria-label])')
TIPO = lambda n: {'role': 'checkbox', 'name': n, 'exact': True, 'within': DLG}
FICHA_TXT = 'FICHA DO TIPO DE SERVIÇO'

SETUP_APP = lambda rota, esperar: [
    {'do': 'goto', 'url': rota}, {'do': 'waitFor', 'text': esperar, 'timeout': 20}, {'do': 'waitFor', 'idle': True}]
SERV_OK = 'Configure os tipos de serviços, tarefas e checklists'
SEIS = '6 tipos cadastrados'


def setup_serv(esperar=SERV_OK):
    return SETUP_APP('/servicos', esperar)


def setup_checklists(editor, nome=None):
    s = SETUP_APP('/servicos', SERV_OK)
    s += [{'do': 'click', 'target': TAB_CHK}, {'do': 'waitFor', 'text': 'Lista de checklists', 'timeout': 15},
          {'do': 'waitFor', 'text': 'Editar checklist', 'timeout': 15}]
    if nome:  # escolhe na lista o checklist em que a aula trabalha (o app abre o primeiro da ordem interna, que pode ser outro)
        s += [{'do': 'click', 'target': TXT(nome, within='main [role=list]')}, {'do': 'waitFor', 'idle': True}]
    if editor:
        s += [{'do': 'click', 'target': BTN('Editar checklist')}, {'do': 'waitFor', 'text': 'Voltar à prévia', 'timeout': 15},
              {'do': 'waitFor', 'idle': True}]
    return s


# ================================================================ capítulos
def cap00():
    c = Cap(0, pace=0.6, start=(700, 420), prewarm=['/dashboard'], setup=SETUP_APP('/dashboard', 'Olá, Camila!'))
    c.mark(1)
    c.hover(TXT('Olá, Camila!', exact=False), 1.2, at=1.0, label='tela inicial do Dominex, logada')
    c.hover(GESTAO, 1.0, at=c.A(1, 'checklists', 5.6), label='o cursor vai ao menu Gestão')
    c.mark(2)
    c.click(GESTAO, at=c.L(2), label='abre o menu Gestão')
    c.hover(LINK('Serviços'), 1.5, at=c.A(2, 'ordens', 0.3), label='menu Gestão: Serviços (ordens de serviço)')
    c.hover(LINK('Serviços'), 3.0, at=c.A(2, 'prefixo', 0.8), label='Serviços: tipo, prefixo e roteiro')
    c.mark(3)
    c.hover(LINK('Clientes e Fornecedores'), 1.0, at=c.A(3, 'Clientes', 0.9), label='menu Gestão: Clientes e Fornecedores (tutorial anterior)')
    c.hover(LINK('Equipamentos'), 1.0, at=c.A(3, 'Equipamentos', 0.8), label='menu Gestão: Equipamentos (tutorial anterior)')
    c.hover(LINK('Serviços'), 0.8, at=c.A(3, 'Serviços', 1.1, nth=0), label='Vamos abrir a tela de Serviços')
    c.fim()
    return c


def cap01():
    # pace 0,6: o deslocamento entre abas/botões custa ~0,5 s; cada "seconds" abaixo cabe na janela até o próximo `at`
    c = Cap(1, pace=0.6, start=(700, 420), prewarm=['/dashboard', '/servicos'], setup=SETUP_APP('/dashboard', 'Olá, Camila!') + [{'do': 'eval', 'js': OBS}])
    c.mark(1)
    c.click(GESTAO, at=c.A(1, 'Gestão', 1.0), label='abre o grupo Gestão do menu')
    c.click(LINK('Serviços'), at=c.A(1, 'Serviços', 0.6, nth=1), label='Serviços')
    c.waitfor(text=SERV_OK, timeout=15)
    c.mark(2)
    c.hover(TAB_SERV, 0.9, at=c.A(2, 'Tipos', 0.6, nth=0), label='aba Tipos de Serviços')
    c.hover(TAB_TASK, 0.9, at=c.A(2, 'Tarefas', 0.9, nth=0), label='aba Tipos de Tarefas')
    c.hover(TAB_CHK, 1.0, at=c.A(2, 'Checklists', 0.7), label='aba Checklists')
    c.hover(TAB_SERV, 2.0, at=c.A(2, 'serviço', 0.8, nth=1), label='o tipo de serviço diz o que a equipe vai fazer')
    c.hover(TAB_CHK, 1.6, at=c.A(2, 'checklist', 0.8, nth=1), label='o checklist é o roteiro da visita')
    c.hover(TAB_TASK, 2.4, at=c.A(2, 'tarefa', 0.8, nth=1), label='o tipo de tarefa organiza os compromissos internos')
    c.hover(TAB_SERV, 0.45, at=c.A(2, 'passa', 0.9), label='passa pelas três: Tipos de Serviços')
    c.hover(TAB_TASK, 0.45, label='passa pelas três: Tipos de Tarefas')
    c.hover(TAB_CHK, 0.45, label='passa pelas três: Checklists')
    c.mark(3)
    c.hover(TXT('Nenhum tipo de serviço'), 1.2, at=c.A(3, 'primeira', 0.2), label='primeira aba vazia')
    c.hover(BTN('Categorias'), 0.6, at=c.A(3, 'botões', 0.35), label='botão Categorias')
    c.hover(BTN('Novo Serviço'), 0.8, at=c.A(3, 'Novo', 0.7), label='botão Novo Serviço')
    c.hover(BTN('Categorias'), 0.9, at=c.A(3, 'categorias', 1.0, nth=1), label='vamos começar pelas categorias')
    c.fim()
    return c


def cap02():
    # Ritmo: um clique do robô custa no mínimo ~0,55 s (localizar, mover, assentar, apertar), então a janela da fala
    # "Instalação, Manutenção e Higienização" (~3 s) não comporta 3 ciclos completos (nome, cor, "+"). O 1º ciclo acompanha
    # a fala passo a passo (nome, cor azul, clique no "+"); o 2º e o 3º só com nome e Enter (cor padrão, cinza), com o
    # cursor ainda no campo: terminam junto das palavras. Desvio do roteiro (verde/ciano) declarado no relatório.
    c = Cap(2, pace=0.3, cps=40, start=(900, 480), setup=setup_serv('Nenhum tipo de serviço'))
    nome = {'placeholder': 'Nome da categoria...'}
    cor = SEL(f'{DLG} button:has(span.font-mono)')
    mais = SEL(f'{DLG} button:has(svg.lucide-plus)')
    sw = lambda h: SEL(f'{POP} button[title="{h}"]')
    linha = lambda n: f'{DLG} div[draggable=true]:has-text("{n}")'
    hand = lambda n: SEL(f'{DLG} div[draggable=true]:has-text("{n}") svg.lucide-grip-vertical')
    row = lambda n: SEL(linha(n))

    c.mark(1)
    c.click(BTN('Categorias'), at=c.A(1, 'categorias', 0.2), label='botão Categorias')
    c.waitfor(selector=f'{DLG}', timeout=8)
    c.hover(TXT('Nenhuma categoria cadastrada.'), 2.2, at=c.A(1, 'viram', 1.0), label='janela Categorias de Serviço, vazia')
    c.mark(2)
    # 1º ciclo, passo a passo com a fala
    c.type(nome, 'Instalação', at=c.L(2), label='nome da categoria Instalação')
    c.click(cor, label='seletor de cor (Instalação)')
    c.click(sw('#3B82F6'), label='cor #3B82F6 (Instalação)')
    c.click(mais, at=c.A(2, 'mais', 0.2), label='botão + (Instalação)')
    c.waitfor(selector=linha('Instalação'), timeout=8)
    # 2º e 3º: nome + Enter (o foco continua no campo depois do Enter)
    c.type(nome, 'Manutenção', label='nome da categoria Manutenção')
    c.press('Enter', delay=60, label='confirma Manutenção')
    c.waitfor(selector=linha('Manutenção'), timeout=8)
    c.type(nome, 'Higienização', noClick=True, label='nome da categoria Higienização')
    c.press('Enter', delay=60, label='confirma Higienização')
    c.waitfor(selector=linha('Higienização'), timeout=8)
    c.mark(3)
    c.hover(hand('Higienização'), 0.5, at=c.A(3, 'alça', 0.3), label='alça de arrastar')
    c.drag(hand('Higienização'), row('Manutenção'), at=c.A(3, 'arrastar', 0.45), label='arrasta Higienização uma posição para cima')
    c.drag(hand('Higienização'), row('Manutenção'), label='devolve Higienização ao fim')
    c.mark(4)
    c.hover(TXT('Instalação', within=DLG), 0.6, at=c.A(4, 'categorias', 0.6), label='as três categorias')
    c.click({'role': 'button', 'name': 'Fechar', 'within': DLG}, at=c.A(4, 'Agora', 0.6), label='fecha a janela de categorias')
    c.waitfor(gone={'selector': DLG}, timeout=8)
    c.fim()
    return c


def modal_novo_tipo_campos(c):
    nome = {'placeholder': 'Ex: Manutenção Preventiva'}
    return nome


def cap03():
    # pace 0,6 / digitação 18 cps: o nome, a categoria e a descrição acompanham a fala sem estourar a janela de cada linha
    c = Cap(3, pace=0.6, cps=18, start=(900, 480), setup=setup_serv('Nenhum tipo de serviço') + [{'do': 'eval', 'js': OBS}])
    nome = {'placeholder': 'Ex: Manutenção Preventiva'}
    cor = SEL('input[type=color] + input')
    cat = {'role': 'combobox', 'hasText': 'Sem categoria'}
    desc = {'placeholder': 'Descrição do tipo de serviço'}
    pref = {'placeholder': 'Ex: MP, MC, INS'}
    preco = {'placeholder': 'Ex: 350,00'}
    c.mark(1)
    c.hover(BTN('Novo Serviço'), 1.0, at=c.A(1, 'Glacial', 1.0), label='botão Novo Serviço')
    c.click(BTN('Novo Serviço'), at=c.A(1, 'Novo', 0.9), label='Novo Serviço')
    c.waitfor(target={'role': 'dialog'}, timeout=8)
    c.mark(2)
    c.type(nome, 'Manutenção Preventiva', at=c.L(2), cps=18, label='nome: Manutenção Preventiva')
    c.type(cor, '#22C55E', at=c.A(2, 'escolho', 0.0), cps=12, clear=True, label='cor do serviço')
    c.hover(SEL('input[type=color]'), 1.6, at=c.A(2, 'diferente', 0.8), label='uma cor diferente para cada serviço')
    # a lista de categorias abre ~1 s antes da fala (a escolha da opção cai em "categoria Manutenção") para a descrição caber em L3
    c.click(cat, at=c.L(3) - 1.0, label='abre a lista de categorias')
    c.mark(3)
    c.click({'role': 'option', 'name': 'Manutenção'}, label='categoria Manutenção')
    c.type(desc, 'Limpeza e conferência completa do aparelho', at=c.A(3, 'escrevo', 2.0), cps=40, label='descrição curta')
    c.mark(4)
    c.hover(TXT('Prefixo de Numeração OS'), 1.0, at=c.A(4, 'Numeração', 0.8), label='Prefixo de Numeração OS')
    c.type(pref, 'MP', at=c.A(4, 'MP', 1.0), cps=6, label='prefixo MP')
    c.hover(TXT('-2026-0001', exact=False), 3.2, at=c.A(4, 'Assim', 0.8), label='prévia do número da OS')
    c.mark(5)
    c.type(preco, '180', at=c.A(5, 'coloco', 0.9), cps=6, label='preço padrão 180')
    c.hover(TXT('Valor sugerido ao adicionar este serviço em um orçamento. Pode ser editado pelo vendedor.', exact=False), 3.4, at=c.A(5, 'valor', 0.8), label='o orçamento sugere esse valor')
    c.mark(6)
    c.hover(SWROW('Vinculado a equipamento'), 2.0, at=c.A(6, 'Vinculado', 1.6), label='interruptor Vinculado a equipamento')
    c.hover(SWROW('Ativo'), 2.4, at=c.A(6, 'Ativo', 1.1), label='interruptor Ativo')
    c.mark(7)
    c.click(BTN('Criar'), at=c.A(7, 'Criar', 0.9), label='Criar')
    c.waitfor(text='Tipo de serviço criado!', timeout=10, optional=True)
    c.mark(8)
    c.ev(BASTIDOR_JS, at=c.A(8, 'Os', -0.1), label='(bastidor) os outros cinco serviços já cadastrados')
    c.waitfor(text='6 tipos cadastrados', timeout=10)
    c.hover(TXT('Manutenção Corretiva'), 0.3, at=c.A(8, 'corretiva', 0.55), label='lista: Manutenção Corretiva')
    c.hover(TXT('Instalação de Split'), 0.3, at=c.A(8, 'instalação', 0.55), label='lista: Instalação de Split')
    c.hover(TXT('Higienização de Split'), 0.3, at=c.A(8, 'higienização', 0.55), label='lista: Higienização de Split')
    c.hover(TXT('Carga de Gás'), 0.3, at=c.A(8, 'carga', 0.55), label='lista: Carga de Gás')
    c.hover(TXT('Visita Técnica'), 0.9, at=c.A(8, 'visita', 0.55), label='lista: Visita Técnica')
    c.fim()
    return c


# refetch das listas sem eventos de rede (o par offline/online faz o app mostrar o aviso "Conexão restaurada"): acha o QueryClient
# na árvore do React e manda recarregar as consultas ativas
REFETCH_JS = ("const root=document.getElementById('root'); const key=Object.keys(root).find(k=>k.startsWith('__reactContainer$'));"
              "const stack=[root[key]]; let n=0; let ok=false;"
              "while(stack.length&&n++<20000){const f=stack.pop(); if(!f) continue; const p=f.memoizedProps;"
              "if(p&&p.client&&typeof p.client.refetchQueries==='function'){p.client.refetchQueries({type:'active'}); ok=true; break;}"
              "if(f.sibling) stack.push(f.sibling); if(f.child) stack.push(f.child);}")


# (bastidor) cadastrados "do mesmo jeito" fora da câmera: REST direto no backend falso + refetch da lista (REFETCH_JS)
_BAST = [
    ('Manutenção Corretiva', 'Diagnóstico e reparo de falhas no aparelho', '#F97316', 'Manutenção', 'MC', 220, True, None),
    ('Instalação de Split', 'Instalação completa de aparelho split', '#3B82F6', 'Instalação', 'INS', 650, True, ('140601', '14.06')),
    ('Higienização de Split', 'Limpeza interna e externa do aparelho', '#06B6D4', 'Higienização', 'HIG', 180, True, None),
    ('Carga de Gás', 'Recarga de gás refrigerante', '#A855F7', 'Manutenção', 'GAS', 350, True, None),
    ('Visita Técnica', 'Visita para avaliação e orçamento', '#6B7280', None, 'VT', 120, False, None),
]
BASTIDOR_JS = ('(async () => {'
               "const B='http://127.0.0.1:54321/rest/v1'; const H={'content-type':'application/json',Prefer:'return=representation'};"
               "const cats=await (await fetch(B+'/service_type_categories?select=id,name')).json();"
               "const c=Object.fromEntries(cats.map(x=>[x.name,x.id]));"
               'const rows=' + json.dumps([
                   {'name': n, 'description': d, 'color': col, 'category_id': ('@' + cat if cat else None), 'number_prefix': p,
                    'default_price': pr, 'requires_equipment': req, 'is_active': True,
                    **({'codigo_servico': fs[0], 'item_lc116': fs[1], 'codigo_tributacao_municipal': '001', 'iss_aliquota': 5} if fs else {})}
                   for n, d, col, cat, p, pr, req, fs in _BAST], ensure_ascii=False) + ';'
               "for(const r of rows){ if(typeof r.category_id==='string'&&r.category_id.startsWith('@')) r.category_id=c[r.category_id.slice(1)]; }"
               "const r=await fetch(B+'/service_types',{method:'POST',headers:H,body:JSON.stringify(rows)});"
               + REFETCH_JS +
               'return r.status;})()')


def cap04():
    c = Cap(4, pace=0.42, cps=10, start=(900, 480), setup=setup_serv(SEIS))
    busca = {'placeholder': 'Buscar por nome ou descrição...'}
    pop = lambda t: TXT(t, within=POP)
    ficha_sw = SWROW('Vinculado a equipamento')
    c.mark(1)
    c.hover(TXT(SEIS), 1.2, at=0.05, label='lista com os seis serviços')
    c.hover(TXT('Carga de Gás', within='main [role=list]'), 0.6, at=c.A(1, 'cor', 0.7), label='cada serviço com a sua cor')
    c.hover(TXT('Manutenção • GAS'), 1.0, label='categoria e prefixo na linha')
    c.mark(2)
    c.type(busca, 'higien', at=c.A(2, 'buscar', 1.3), cps=10, label="busca por 'higien'")
    c.press(['Control+a', 'Backspace'], at=c.A(2, 'descrição', 0.0), label='limpa a busca')
    c.click(BTN('Filtros'), at=c.A(3, 'Filtros', 0.6), label='botão Filtros')
    c.mark(3)
    c.click(pop('Manutenção'), at=c.A(3, 'categoria', 0.85), label='filtra a categoria Manutenção')
    c.click(BTN('Limpar filtros'), label='Limpar filtros')
    c.press('Escape', delay=60, label='fecha o filtro')
    c.click({'role': 'button', 'name': 'Ordenar', 'exact': False}, at=c.A(3, 'Ordenar', 0.1), label='botão Ordenar')
    c.hover(pop('Nome (A-Z)'), 0.4, at=c.A(3, 'ordem', 0.1), label='Nome (A-Z)')
    c.hover(pop('Nome (Z-A)'), 0.3, at=c.A(3, 'ou', 0.0), label='Nome (Z-A)')
    c.press('Escape', delay=60, label='fecha o Ordenar')
    c.mark(4)
    # a ficha rola sozinha até o interruptor quando o cursor vai até ele (o hover espera a rolagem terminar)
    c.click(TXT('Manutenção Preventiva', within='main [role=list]'), at=c.A(4, 'Manutenção', 0.7), label='abre Manutenção Preventiva')
    c.hover(ficha_sw, 4.5, label='Vinculado a equipamento ligado (Manutenção Preventiva)')
    c.click(TXT('Visita Técnica', within='main [role=list]'), at=c.A(4, 'Visita', 0.9), label='abre Visita Técnica')
    c.hover(ficha_sw, 5.0, at=c.A(4, 'desligada', 0.6), label='Vinculado a equipamento desligado (Visita Técnica)')
    c.mark(5)
    c.hover(ficha_sw, 6.0, at=c.A(5, 'hora', 0.3), label='(ilustração) ligado × desligado')
    c.fim()
    return c


def cap05():
    c = Cap(5, pace=0.5, cps=8, start=(900, 480), setup=setup_serv(SEIS))
    ctn = SEL('button[role=combobox]', hasText='Selecione o código...', nth=0)
    mun = {'placeholder': 'Ex.: 001'}
    iss = {'placeholder': '5'}
    item = SEL('div:has(> label:text-is("Item da LC 116"))')
    c.mark(1)
    c.click(TXT('Manutenção Preventiva', within='main [role=list]'), at=0.2, label='abre Manutenção Preventiva')
    c.hover({'role': 'tab', 'name': 'Fiscal'}, 0.8, at=c.A(1, 'aba', 0.9), label='pílula Fiscal')
    c.click({'role': 'tab', 'name': 'Fiscal'}, at=c.A(1, 'Fiscal', 1.0, nth=1), label='abre a aba Fiscal')
    c.waitfor(text='Fiscal (NFS-e)', timeout=8)
    c.hover(TXT('Fiscal (NFS-e)'), 1.8, at=c.A(1, 'módulo', 0.8), label='bloco Fiscal (NFS-e)')
    c.mark(2)
    c.click(ctn, at=c.L(2), label='Código de serviço (cTribNac)')
    c.type({'placeholder': 'Buscar por código ou descrição...'}, '14.01.01', at=c.A(2, 'catorze', 1.0), cps=3.4, label='busca 14.01.01')
    c.click(TXT('14.01.01', within=POP), at=c.A(2, 'escolho', 0.1), label='escolhe 14.01.01')
    c.hover(item, 1.8, label='Item da LC 116 preenchido sozinho')
    c.mark(3)
    c.hover(TXT('Código de tributação municipal (cTribMun)'), 1.5, at=c.A(3, 'código', 0.2), label='Código de tributação municipal')
    c.type(mun, '001', at=c.A(3, 'zero', 1.0), cps=3.2, label='cTribMun 001')
    c.hover(TXT('Complemento de 3 dígitos', exact=False), 2.6, at=c.A(3, 'ele', 0.9), label='a prefeitura usa para aceitar a nota')
    c.mark(4)
    c.hover(TXT('Alíquota de ISS (%)'), 1.6, at=c.L(4), label='Alíquota de ISS')
    c.type(iss, '5', at=c.A(4, 'cinco', 1.0), cps=4, label='ISS 5%')
    c.click(BTN('Salvar'), at=c.A(4, 'Salvo', 1.0), label='Salvar')
    c.waitfor(text='Tipo de serviço atualizado!', timeout=10, optional=True)
    c.hover(SEL('button[role=combobox]', hasText='14.01.01', nth=0), 2.0, at=c.A(4, 'código', 1.0, nth=0), label='código salvo na ficha')
    c.hover(mun, 1.6, at=c.A(4, 'nasce', 1.0), label='cTribMun salvo')
    c.fim()
    return c


def cap06():
    c = Cap(6, pace=0.5, cps=24, start=(900, 480), setup=setup_serv(SEIS))
    c.mark(1)
    c.click(TXT('Manutenção Preventiva', within='main [role=list]'), at=c.A(1, 'abrir', 1.5), label='abre Manutenção Preventiva')
    c.scroll(BTN('Salvar'), label='ficha: botão Salvar à vista')  # a ficha rola enquanto a fala explica; o clique em Salvar não precisa rolar
    # edita a descrição: o clique cai depois do texto (fim do campo) e acrescenta o que mudou
    c.type(SEL('textarea'), ' e teste', cps=20, label='edita a descrição')
    c.click(BTN('Salvar'), at=c.A(1, 'salvar', 0.6), label='Salvar')
    c.waitfor(text='Tipo de serviço atualizado!', timeout=10, optional=True)
    c.mark(2)
    c.hover(SWROW('Ativo'), 3.0, at=c.A(2, 'desligar', 1.1), label='interruptor Ativo')
    c.scroll(BTN('Excluir'), at=c.L(3) - 1.8, label='ficha: botão Excluir à vista')
    c.mark(3)
    c.click(BTN('Excluir'), at=c.A(3, 'Excluir', 0.4), label='Excluir')
    c.waitfor(text='Excluir Tipo de Serviço', timeout=8)
    c.hover(TXT('Tem certeza que deseja excluir este tipo de serviço? Esta ação não pode ser desfeita.', exact=False), 1.4, at=c.A(3, 'remove', 0.9), label='confirmação: não pode ser desfeita')
    c.click(BTN('Cancelar'), at=c.A(3, 'cancelo', 0.9), label='Cancelar')
    c.waitfor(gone={'role': 'alertdialog'}, timeout=8)
    c.fim()
    return c


def bastidor_tarefa(nome_t, cor_t, desc_t):
    """(bastidor) tipo de tarefa cadastrado "do mesmo jeito" fora da câmera: REST direto no backend falso + refetch da lista"""
    corpo = json.dumps({'company_id': '9c307966-79f1-567c-ac4d-d5fd3c1a2f40', 'name': nome_t, 'color': cor_t, 'description': desc_t, 'is_active': True}, ensure_ascii=False)
    return ('(async () => {'
            "const B='http://127.0.0.1:54321/rest/v1'; const H={'content-type':'application/json',Prefer:'return=representation'};"
            "const r=await fetch(B+'/task_types',{method:'POST',headers:H,body:JSON.stringify(" + corpo + ")});"
            + REFETCH_JS +
            'return r.status;})()')


def cap07():
    # 1º tipo (Reunião) ao vivo, passo a passo; "Entrega de material" e "Compra de peças" entram de bastidor no instante em que a
    # fala os cita (dois ciclos completos não cabem nos ~4 s de fala). Descrição só nos de bastidor (a fala não a cita ao criar).
    c = Cap(7, pace=0.45, cps=12, start=(900, 480), prewarm=['/servicos', '/servicos?tab=task-types'], setup=setup_serv(SEIS))
    nome = {'placeholder': 'Ex: Reunião, Entrega, Compra'}
    cor = SEL(f'{DLG} input[type=color] + input')
    c.mark(1)
    c.click(TAB_TASK, at=0.4, label='aba Tipos de Tarefas')
    c.waitfor(text='Treinamento da equipe', timeout=8)
    c.hover(TXT('Treinamento da equipe', within='main [role=list]'), 1.4, at=c.A(1, 'Tarefa', 0.8), label='tipo de tarefa já cadastrado')
    c.hover(TXT('Ficha do tipo de tarefa', exact=False), 1.6, at=c.A(1, 'compromisso', 0.8), label='ficha do tipo de tarefa')
    c.hover(SWROW('Ativo'), 2.0, at=c.A(1, 'só', 0.9), label='só os ativos entram na escolha')
    c.mark(2)
    c.click(BTN('Novo Tipo'), at=c.A(2, 'Novo', 0.7), label='Novo Tipo')
    c.waitfor(target={'role': 'dialog'}, timeout=8)
    c.type(nome, 'Reunião', noClick=True, at=c.A(2, 'Reunião', 0.3), cps=9, label='nome: Reunião')
    c.type(cor, '#8B5CF6', cps=20, clear=True, label='cor da Reunião')
    c.click(BTN('Criar'), at=c.A(2, 'Criar', 0.5), label='Criar')
    c.waitfor(text='Tipo de tarefa criado!', timeout=10, optional=True)
    c.mark(3)
    c.ev(bastidor_tarefa('Entrega de material', '#F97316', 'Entrega de material e ferramentas nos clientes'), at=c.A(3, 'Entrega', 0.0), label='(bastidor) Entrega de material')
    c.ev(bastidor_tarefa('Compra de peças', '#EAB308', 'Compra de peças e insumos no fornecedor'), at=c.A(3, 'Compra', 0.0), label='(bastidor) Compra de peças')
    c.waitfor(text='4 tipos cadastrados', timeout=10, optional=True)
    c.mark(4)
    c.click(TXT('Compra de peças', within='main [role=list]'), at=c.A(4, 'Cada', 0.7), label='abre Compra de peças')
    c.hover(SEL('input[type=color] + input'), 0.3, at=c.A(4, 'cor', 0.5), label='cor do tipo')
    c.hover(SEL('textarea'), 0.3, at=c.A(4, 'descrição', 0.5), label='descrição do tipo')
    c.hover(SWROW('Ativo'), 0.3, at=c.A(4, 'Ativo', 0.5), label='interruptor Ativo')
    c.hover(BTN('Salvar'), 0.5, at=c.A(4, 'igual', 0.5), label='Salvar e Excluir como nos serviços')
    c.fim()
    return c


def cap08():
    c = Cap(8, pace=0.6, cps=11, start=(900, 480), prewarm=['/servicos', '/servicos?tab=checklists'], setup=setup_serv(SEIS))
    cat = BTN('Catálogo de Checklists')
    item = lambda t: TXT(t, within=DLG)
    aviso = TXT('Estes são apenas modelos sugeridos.')
    c.mark(1)
    c.click(TAB_CHK, at=0.0, label='aba Checklists')
    c.waitfor(text='Nenhum checklist criado', timeout=10)
    c.hover(TXT('Nenhum checklist criado'), 1.5, at=c.A(1, 'roteiro', 1.0), label='aba Checklists vazia')
    c.hover(cat, 0.5, at=c.A(1, 'modelos', 1.0), label='botão Catálogo de Checklists')
    c.mark(2)
    c.click(cat, at=c.L(2), label='Catálogo de Checklists')
    c.waitfor(text='Estes são apenas modelos sugeridos.', timeout=10)
    c.hover(aviso, 0.5, at=c.A(2, 'sugeridos', 1.2), label='aviso: apenas modelos sugeridos')
    c.hover(item('Instalação de Split'), 0.3, at=c.A(2, 'instalação', 0.6), label='modelo Instalação de Split')
    c.hover(item('Higienização de Split'), 0.3, at=c.A(2, 'higienização', 0.6), label='modelo Higienização de Split')
    c.hover(item('Manutenção Preventiva de Split'), 0.3, at=c.A(2, 'manutenção', 0.6), label='modelo Manutenção Preventiva de Split')
    c.hover(item('Carga de Gás'), 0.3, at=c.A(2, 'carga', 0.6), label='modelo Carga de Gás')
    c.hover(aviso, 1.5, at=c.A(2, 'porque', 1.2), label='as perguntas ficam editáveis depois')
    c.mark(3)
    c.click(item('Manutenção Preventiva de Split'), at=c.L(3), label='abre o modelo Manutenção Preventiva')
    c.waitfor(text='Filtros limpos / em bom estado?', timeout=8)
    c.hover(item('Filtros limpos / em bom estado?'), 0.6, at=c.A(3, 'perguntas', 0.8), label='perguntas prontas')
    c.hover(TXT('Número (psi)', within=DLG, nth=0), 1.0, at=c.A(3, 'psi', 1.5), label='selo Número (psi)')
    c.hover(TXT('Obrigatória', within=DLG, nth=0), 0.8, at=c.A(3, 'obrigatórias', 0.8), label='selo Obrigatória')
    c.mark(4)
    c.click(BTN('Selecionar'), at=c.L(4), label='Selecionar')
    c.waitfor(text='Nome do novo checklist', timeout=8)
    c.type(SEL(f'{DLG} input'), 'Manutenção preventiva de split', at=c.A(4, 'dou', 0.3), cps=16, clear=True, label='nome: Manutenção preventiva de split')
    c.click(BTN('Criar checklist'), at=c.A(4, 'Criar', 0.5, nth=0), label='Criar checklist')
    c.waitfor(text='13 perguntas importadas!', timeout=10, optional=True)
    c.hover(TXT('13 perguntas · Todos os serviços'), 2.0, at=c.A(4, 'treze', 0.8), label='treze perguntas importadas')
    c.fim()
    return c


def cap09():
    c = Cap(9, pace=0.6, cps=12, start=(900, 480), prewarm=['/servicos', '/servicos?tab=checklists'], setup=setup_checklists(True))
    hab = SEL('button[role=combobox]', hasText='Todos os serviços')
    lab = lambda t: SEL(f'{POP} label:has-text("{t}")')
    c.mark(1)
    c.hover(TXT('Serviços habilitados'), 0.4, at=c.A(1, 'Serviços', 0.7), label='Serviços habilitados')
    c.click(hab, at=c.A(1, 'escolho', 0.5), label='abre Serviços habilitados')
    c.waitfor(selector=f'{POP} label', timeout=6)
    c.click(lab('Todos os serviços'), at=c.A(1, 'Todos', 0.6), label='desmarca Todos os serviços')
    c.click(lab('Manutenção Preventiva'), at=c.A(1, 'marco', 0.2), label='marca Manutenção Preventiva')
    c.click(lab('Carga de Gás'), at=c.A(1, 'Manutenção', 0.0), label='desmarca o serviço que o app marcou sozinho')
    c.click(TXT('Serviços habilitados'), at=c.A(1, 'Assim', 0.3), label='fecha a lista de serviços (clique fora)')
    c.hover(SEL('button[role=combobox]', hasText='Manutenção Preventiva'), 1.6, at=c.A(1, 'aparece', 0.1), label='checklist só nas ordens da Manutenção Preventiva')
    c.mark(2)
    c.click(BTN('Voltar à prévia'), at=c.L(2), label='Voltar à prévia')
    c.click(BTN('Novo checklist'), at=c.A(2, 'Novo', 0.8), label='Novo checklist')
    c.waitfor(text='Novo Checklist', timeout=8)
    c.type(SEL(f'{DLG} input'), 'Higienização de split', at=c.A(2, 'nome', 0.6), cps=14, label='nome: Higienização de split')
    c.click(SEL(f'{DLG} button[role=switch]'), at=c.A(2, 'desligo', 0.0), label='desliga Todos os serviços')
    c.click(TXT('Higienização de Split', within=DLG), at=c.A(2, 'marco', 0.0), label='marca Higienização de Split')
    c.click(BTN('Criar'), at=c.A(2, 'Criar', 0.9), label='Criar')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.mark(3)
    c.click(TXT('Higienização de split', within='main [role=list]'), at=c.L(3), label='abre o checklist novo na lista')
    c.click(BTN('Editar checklist'), label='abre o editor do checklist novo')
    c.waitfor(text='Nenhuma pergunta criada', timeout=8)
    c.hover(SEL('button[role=combobox]', hasText='Higienização de Split'), 1.6, at=c.A(3, 'serviço,', 0.3), label='sem serviço marcado, vale para todos')
    c.fim()
    return c


def cap10():
    c = Cap(10, pace=0.6, cps=14, start=(900, 480), prewarm=['/servicos', '/servicos?tab=checklists'], setup=setup_checklists(True, 'Higienização de split'))
    btn_nova = BTN('Nova Pergunta')
    foot = {'role': 'button', 'name': 'Nova Pergunta', 'exact': True, 'within': DLG}
    perg = SEL('#checklist-question-text')
    orient = SEL('#checklist-question-description')
    c.mark(1)
    c.click(btn_nova, at=c.A(1, 'Nova', 0.6), label='Nova Pergunta')
    c.waitfor(target={'role': 'dialog'}, timeout=8)
    c.hover(TXT('Escreva a pergunta', within=DLG), 1.0, at=c.A(1, 'esquerda', 0.7), label='bloco Escreva a pergunta')
    c.hover(TXT('Prévia na OS', within=DLG), 3.2, at=c.A(1, 'direita', 0.6), label='Prévia na OS')
    c.mark(2)
    c.type(perg, 'Estado da serpentina', at=c.A(2, 'Estado', 1.4), cps=16, label='pergunta: Estado da serpentina')
    c.type(orient, 'Observe se há sujeira ou amassados nas aletas.', at=c.A(2, 'orientação', 0.0), cps=26, label='orientação para o técnico')
    c.hover(TXT('Escolha como responder', within=DLG), 0.6, at=c.A(2, 'Escolha', 0.6), label='Escolha como responder')
    c.click(TIPO('Conformidade'), at=c.A(2, 'Conformidade', 0.7), label='marca Conformidade')
    c.click(TIPO('Verdadeiro/Falso'), label='desmarca Verdadeiro/Falso')
    c.hover(TXT('Não conforme', within=DLG, nth=0), 1.4, at=c.A(2, 'prévia', 0.7), label='a prévia mostra as três respostas')
    c.mark(3)
    c.hover(TXT('Escolha como responder', within=DLG), 0.3, at=c.L(3), label='oito jeitos de responder')
    for nome, palavra in [('Verdadeiro/Falso', 'Verdadeiro'), ('Conformidade', 'Conformidade'), ('Texto', 'Texto'), ('Número', 'Número'),
                          ('Foto', 'Foto'), ('Vídeo', 'Vídeo'), ('Seleção', 'Seleção'), ('Assinatura', 'Assinatura')]:
        c.hover(TIPO(nome), 0.1, at=c.A(3, palavra, 0.65), label=f'tipo de resposta: {nome}')
    c.mark(4)
    c.hover(RULEROW('Campo obrigatório'), 2.6, at=c.L(4), label='Campo obrigatório ligado')
    c.hover(TXT('Frequência', within=DLG, nth=0), 2.2, at=c.A(4, 'Frequência', 0.8), label='Frequência (é pros contratos)')
    c.click(foot, at=c.A(4, 'Nova', 0.6), label='Nova Pergunta (salva)')
    c.waitfor(text='Pergunta adicionada!', timeout=8, optional=True)
    c.hover(TXT('Estado da serpentina', within='main'), 0.3, at=c.A(4, 'ela', 0.6), label='a pergunta entra no checklist')
    c.click(btn_nova, at=c.A(4, 'entra', 0.0), label='Nova Pergunta (segunda)')
    c.waitfor(target={'role': 'dialog'}, timeout=8)
    c.mark(5)
    c.type(perg, 'Aspecto da água retirada', at=c.L(5), cps=14, noClick=True, label='pergunta: Aspecto da água retirada')
    c.click(TIPO('Seleção'), at=c.A(5, 'Seleção', 0.4), label='marca Seleção')
    c.click(TIPO('Verdadeiro/Falso'), label='desmarca Verdadeiro/Falso')
    # o campo das opções fica abaixo da dobra do modal; o foco por script evita a rolagem lenta do robô (o navegador ajusta a rolagem sozinho)
    c.ev("document.querySelector('input[placeholder=\"Adicionar opção...\"]').focus()", label='(foco no campo das opções)')
    c.type({'placeholder': 'Adicionar opção...'}, 'Limpa\nTurva\nSuja\n', at=c.A(5, 'limpa', 0.3), cps=14, noClick=True, label='opções: limpa, turva e suja')
    c.fim()
    c.click(foot, label='Nova Pergunta (salva a segunda)')
    c.waitfor(text='Pergunta adicionada!', timeout=8, optional=True)
    return c


def foco_regra(rotulo):
    """(bastidor) leva o foco ao interruptor da regra: o navegador rola o modal na hora, sem a rolagem lenta do robô"""
    return ("(() => { const l=[...document.querySelectorAll('[role=dialog] label')].find(x=>x.textContent.trim()==='" + rotulo + "');"
            "const b=l && l.closest('div.flex.items-start.gap-3') && l.closest('div.flex.items-start.gap-3').querySelector('button[role=switch]');"
            "if(b) b.focus(); return !!b; })()")


def cap11():
    c = Cap(11, pace=0.6, cps=14, start=(900, 480), prewarm=['/servicos', '/servicos?tab=checklists'], setup=setup_checklists(True, 'Higienização de split'))
    btn_nova = BTN('Nova Pergunta')
    foot = {'role': 'button', 'name': 'Nova Pergunta', 'exact': True, 'within': DLG}
    perg = SEL('#checklist-question-text')
    excl = {'role': 'button', 'name': 'Exclusivo', 'exact': True, 'within': DLG}
    cumu = {'role': 'button', 'name': 'Cumulativo', 'exact': True, 'within': DLG}
    c.mark(1)
    c.click(btn_nova, at=c.A(1, 'dá', 0.5), label='Nova Pergunta')
    c.waitfor(target={'role': 'dialog'}, timeout=8)
    c.type(perg, 'Filtros lavados?', at=c.A(1, 'Filtros', 0.2), cps=14, noClick=True, label='pergunta: Filtros lavados?')
    c.hover(TIPO('Verdadeiro/Falso'), 0.3, at=c.A(1, 'Verdadeiro', 0.0), label='deixa Verdadeiro/Falso marcado')
    c.click(TIPO('Foto'), at=c.A(1, 'Foto', 0.6), label='marca Foto também')
    c.hover(excl, 0.3, at=c.A(1, 'Aparece', 0.6), label='Modo de resposta múltipla: Exclusivo')
    c.hover(cumu, 0.3, at=c.A(1, 'Cumulativo', 0.6, nth=0), label='Cumulativo')
    c.click(cumu, at=c.A(1, 'Cumulativo', 0.6, nth=1), label='escolhe Cumulativo')
    c.hover(TXT('Tirar ou anexar foto', within=DLG), 1.5, at=c.A(1, 'ele', 0.2), label='a prévia: marca e anexa a foto')
    c.mark(2)
    c.click(RULESW('Exigir foto da câmera'), at=c.L(2), label='liga Exigir foto da câmera')
    c.hover(TXT('Tirar foto agora', within=DLG, exact=False), 0.8, at=c.A(2, 'a', 0.9), label='a prévia mostra Tirar foto agora')
    c.click(foot, at=c.A(2, 'sem', 0.5), label='Nova Pergunta (salva)')
    c.waitfor(text='Pergunta adicionada!', timeout=8, optional=True)
    c.mark(3)
    c.click(btn_nova, at=c.L(3), label='Nova Pergunta (quarta)')
    c.waitfor(target={'role': 'dialog'}, timeout=8)
    c.type(perg, 'Dreno escoando', at=c.A(3, 'técnico', 0.2), cps=14, noClick=True, label='pergunta: Dreno escoando')
    c.click(TIPO('Vídeo'), label='marca Vídeo')
    c.click(TIPO('Verdadeiro/Falso'), label='desmarca Verdadeiro/Falso')
    c.ev(foco_regra('Exigir gravação na hora'), label='(foco no interruptor)')
    c.click(RULESW('Exigir gravação na hora'), label='liga Exigir gravação na hora')
    c.hover(TXT('Gravar vídeo agora', within=DLG, exact=False), 0.4, at=c.A(3, 'clipe', 0.2, nth=1), label='a prévia mostra Gravar vídeo agora')
    c.fim()
    c.click(foot, label='Nova Pergunta (salva a quarta)')
    c.waitfor(text='Pergunta adicionada!', timeout=8, optional=True)
    return c


def cap12():
    c = Cap(12, pace=0.6, cps=9, start=(900, 480), prewarm=['/servicos', '/servicos?tab=checklists'], setup=setup_checklists(True, 'Higienização de split'))
    hand = lambda n: SEL(f'div[draggable=true]:has-text("{n}") svg.lucide-grip-vertical')
    row = lambda n: SEL(f'div[draggable=true]:has-text("{n}")')
    busca = {'placeholder': 'Pesquisar pergunta, descrição ou tipo...'}
    c.mark(1)
    c.scroll(row('Dreno escoando'), at=0.5, label='mostra todas as perguntas da lista')
    c.hover(TXT('Conformidade', within='main'), 0.5, at=c.A(1, 'jeito', 0.8), label='selo do tipo de resposta')
    c.hover(TXT('Cumulativo', within='main'), 0.4, at=c.A(1, 'Cumulativo', 0.6), label='selo Cumulativo')
    c.hover(TXT('Câmera', within='main'), 0.4, at=c.A(1, 'Câmera', 0.6), label='selo Câmera')
    c.hover(hand('Filtros lavados?'), 0.3, at=c.A(1, 'alça', 0.7), label='alça de arrastar')
    c.drag(hand('Filtros lavados?'), row('Aspecto da água retirada'), at=c.A(1, 'arrastar', 0.6), label='arrasta Filtros lavados? uma posição para cima')
    c.mark(2)
    c.type(busca, 'serpentina', at=c.A(2, 'busca', 1.0), cps=9, label="busca por 'serpentina'")
    c.click(SEL('button[role=combobox]', hasText='Todos os tipos'), at=c.A(2, 'ajudam', 0.5), label='filtro Todos os tipos')
    c.press('Escape', at=c.A(2, 'pergunta', 0.1), label='fecha o filtro')
    c.mark(3)
    c.click(BTN('Voltar à prévia'), at=c.L(3), label='Voltar à prévia')
    c.click(BTN('Ver'), at=c.A(3, 'botão', 0.3), label='botão Ver')
    c.waitfor(text='Como este checklist aparece para o técnico na Ordem de Serviço', timeout=8)
    c.hover(TXT('Esta é uma prévia', within=DLG, exact=False), 1.0, at=c.A(3, 'igualzinho', 0.6), label='é igual ao que o técnico vê')
    c.click({'role': 'button', 'name': 'Conforme', 'exact': True, 'within': DLG}, at=c.A(3, 'responder', 0.8), label='responde Conforme')
    c.click({'role': 'checkbox', 'name': 'Limpa', 'exact': True, 'within': DLG}, at=c.A(3, 'vontade', 0.8), label='responde Limpa')
    c.fim()
    c.click({'role': 'button', 'name': 'Fechar', 'exact': True, 'within': DLG}, label='Fechar a prévia')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    return c


def cap13():
    c = Cap(13, pace=0.6, cps=9, start=(900, 480), prewarm=['/servicos', '/servicos?tab=checklists'], setup=setup_checklists(False, 'Higienização de split'))
    alerta = {'role': 'alertdialog'}
    c.mark(1)
    c.hover(TXT('6 perguntas · 1 serviço'), 1.0, at=c.A(1, 'quantas', 0.7), label='Higienização de split: 6 perguntas · 1 serviço')
    c.hover(TXT('13 perguntas · 1 serviço'), 1.0, at=c.A(1, 'serviços', 0.7), label='Manutenção preventiva de split: 13 perguntas · 1 serviço')
    c.mark(2)
    c.click(BTN('Editar checklist'), at=c.L(2), label='Editar checklist')
    c.waitfor(text='Voltar à prévia', timeout=8)
    c.hover(SWROW('Ativo'), 0.5, at=c.A(2, 'só', 0.8), label='interruptor Ativo do checklist')
    c.hover(CK_TRASH, 0.2, at=c.A(2, 'desativar', 0.3), label='lixeira (desativar checklist)')
    c.click(CK_TRASH, at=c.A(2, 'ele', 0.4), label='clica na lixeira')
    c.waitfor(text='Desativar checklist?', timeout=8)
    c.hover(TXT('Desativar checklist?', within='[role=alertdialog]'), 0.6, at=c.A(2, 'ordens', 1.0), label='janela Desativar checklist?')
    c.hover(TXT('continuará preservado', exact=False, within='[role=alertdialog]'), 5.0, at=c.A(2, 'antigas', 0.6), label='as OSs antigas continuam com o roteiro')
    c.click(BTN('Cancelar'), at=c.A(2, 'cancelo', 0.3), label='Cancelar')
    c.waitfor(gone=alerta, timeout=8)
    c.fim()
    return c


def cap14():
    c = Cap(14, pace=0.5, cps=14, start=(900, 480), prewarm=['/servicos', '/servicos?tab=task-types', '/servicos?tab=checklists'], setup=setup_serv(SEIS))
    c.mark(1)
    c.hover(TXT(SEIS), 0.3, at=0.3, label='lista de serviços')
    c.click(BTN('Categorias'), at=c.A(1, 'categorias', 0.7), label='categorias')
    c.waitfor(selector=f'{DLG}', timeout=8)
    c.press('Escape', at=c.A(1, 'serviço,', 0.0), label='fecha as categorias')
    c.click(TXT('Manutenção Preventiva', within='main [role=list]'), at=c.A(1, 'serviço,', -0.3), label='ficha da Manutenção Preventiva')
    c.scroll({'placeholder': 'Ex: 350,00'}, at=c.A(1, 'cor,', -0.7), label='prefixo e preço padrão')
    c.click({'role': 'tab', 'name': 'Fiscal'}, at=c.A(1, 'padrão', -0.3), label='aba Fiscal')
    c.click(TAB_TASK, at=c.A(1, 'cadastrou', -0.1), label='aba Tipos de Tarefas')
    c.hover(TXT('Compra de peças', within='main [role=list]'), 0.4, at=c.A(1, 'Agenda', 0.3), label='tipos de tarefa da Agenda')
    c.mark(2)
    c.click(TAB_CHK, at=c.L(2), label='aba Checklists')
    c.click(BTN('Catálogo de Checklists'), at=c.A(2, 'modelo', 0.7), label='catálogo de modelos')
    c.waitfor(text='Estes são apenas modelos sugeridos.', timeout=8)
    c.press('Escape', at=c.A(2, 'outro', 0.1), label='fecha o catálogo')
    c.click(TXT('Higienização de split', within='main [role=list]'), at=c.A(2, 'zero', 0.3), label='checklist feito do zero')
    c.click(BTN('Editar checklist'), at=c.A(2, 'perguntas', -0.45), label='editor com as perguntas')
    c.hover(SEL('button[role=combobox]', hasText='Higienização de Split'), 1.0, at=c.A(2, 'cada', -0.5), label='ligado aos serviços certos')
    c.mark(3)
    c.click(BTN('Voltar à prévia'), at=c.L(3), label='Voltar à prévia')
    c.click(BTN('Ver'), at=c.A(3, 'roteiros', 0.0), label='botão Ver')
    c.waitfor(text='Como este checklist aparece para o técnico na Ordem de Serviço', timeout=8)
    c.click({'role': 'button', 'name': 'Fechar', 'exact': True, 'within': DLG}, at=c.A(3, 'tutorial', 0.0), label='fecha a prévia')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.click({'role': 'button', 'name': 'Operacional', 'exact': True}, at=c.A(3, 'abre', 0.0), label='menu Operacional (próximo tutorial)')
    c.hover(LINK('Agenda'), 0.6, at=c.A(3, 'organiza', 0.0), label='menu Agenda (próximo tutorial)')
    c.hover(LINK('Mapa e Rastreamento'), 1.2, at=c.A(3, 'acompanha', 0.0), label='Mapa e Rastreamento (próximo tutorial)')
    c.fim()
    return c


CAPS = {i: globals()[f'cap{i:02d}'] for i in range(15)}

if __name__ == '__main__':
    quais = [int(a) for a in sys.argv[1:]] or list(range(15))
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
