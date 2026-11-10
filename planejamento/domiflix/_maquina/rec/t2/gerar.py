#!/usr/bin/env python3
"""T2 · gera rec/t2/cap00..cap11.json (roteiros do robô na Dominex 1.38.9) a partir da voz pronta (t2/narracao/capNN.json).

Aula "Usuários, cargos e permissões": Camila Duarte (admin) cria os cargos Técnico de Campo e Escritório e os usuários Rafael Lima e
Tatiane Ribeiro; só o cap08 é gravado logado como o Rafael. Estado de partida: base própria do T2 (FAKE_SEEDS_DIR=seeds-extra/t2/_base, só a
Camila) + t1/apos-cap13 + t2/inicio; cada capítulo parte de t2/apos-cap(NN-1) (ver rec/t2/gerar_sementes.py).
As marcas L1..Ln saem da voz; os `at` saem da palavra que anuncia cada passo: A(linha, palavra, folga). O gesto "pousa" ~1 s depois do
início do passo, então `at` = início da palavra - folga (docs/04-gravacao.md, "Custo real dos gestos").

Rodar de qualquer pasta: `python3 -I rec/t2/gerar.py [NN ...]`. Depois: `node rec/record.mjs rec/t2/capNN.json --check`.
"""
import json
import os
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TUT = os.path.normpath(os.path.join(HERE, '..', '..'))
NARR = os.environ.get('T2_NARR') or os.path.join(TUT, 't2', 'narracao')  # T2_NARR: pasta com vozes sintéticas, só para testar o gerador

NOMES = ['Abertura', 'Onde ficam os usuários', 'Montando um cargo', 'A ação sem a tela', 'O cargo do escritório', 'Cadastrando um técnico',
         'Acesso Total ou personalizado', 'Conferindo o acesso', 'O que o técnico vê', 'Desativar e reativar', 'Vagas do plano', 'Recapitulando']
BASE_SEMENTES = ['t1/apos-cap13', 't2/inicio']  # identidade da empresa (fim do T1) + Camila com acesso total
# estado de partida de cada capítulo: o último apos-capNN que existe (cargos e usuários nascem na aula)
SEMENTE = {0: None, 1: None, 2: None, 3: None, 4: 'apos-cap03', 5: 'apos-cap04', 6: 'apos-cap05', 7: 'apos-cap06', 8: 'apos-cap07',
           9: 'apos-cap08', 10: 'apos-cap09', 11: 'apos-cap09'}
USUARIO = {8: 'rafael.lima@glacialcold.example'}  # o cap08 é gravado logado como o Rafael


def norm(s):
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode().lower()
    return ''.join(ch for ch in s if ch.isalnum() or ch in '?')


def carregar(nome):
    p = os.path.join(NARR, nome)
    return json.load(open(p, encoding='utf8')) if os.path.exists(p) else None


class Cap:
    def __init__(s, n, pace=0.5, cps=40, start=(700, 420), prewarm=None, setup=None, linhas_esperadas=None, tail=1.5):
        s.n = n
        d = carregar(f'cap{n:02d}.json')
        if d is None:
            raise SystemExit(f'cap{n:02d}: falta t2/narracao/cap{n:02d}.json (a voz ainda não foi processada)')
        s.words, s.linhas, s.dur = d['words'], d['linhas'], d['dur']
        if linhas_esperadas and len(s.linhas) != linhas_esperadas:
            raise SystemExit(f'cap{n:02d}: a voz tem {len(s.linhas)} linhas, esperava {linhas_esperadas}')
        s.steps, s.pace, s.cps, s.start, s.tail = [], pace, cps, start, tail
        s.prewarm, s.setup = prewarm, setup
        s.anchors, s.pending = [], []

    # ---- tempo
    def L(s, i):
        return round(s.linhas[i - 1]['s'], 2)

    def W(s, i, palavra, nth=0):
        q = norm(palavra)
        hits = [w for w in s.words if w['linha'] == i - 1 and norm(w['w']).startswith(q)]
        if len(hits) <= nth:
            raise SystemExit(f'cap{s.n:02d}: palavra "{palavra}" (#{nth}) não achada na linha {i}: ' + ' '.join(w['w'] for w in s.words if w['linha'] == i - 1))
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

    def marcas(s):
        for i in range(1, len(s.linhas) + 1):
            t = s.L(i)
            if t <= 0:
                s.steps.append({'do': 'mark', 'name': f'L{i}', 'at': 0})
            else:
                s.pending.append((t, i))

    def _p(s, d, at, label, kw):
        if at is not None:
            d['at'] = at
        if label:
            d['label'] = label
        d.update(kw)
        return s.add(d)

    def click(s, target, at=None, label=None, **kw):
        return s._p({'do': 'click', 'target': target}, at, label, kw)

    def hover(s, target, seconds=0.9, at=None, label=None, **kw):
        return s._p({'do': 'hover', 'target': target, 'seconds': seconds}, at, label, kw)

    def type(s, target, text, at=None, label=None, cps=None, **kw):
        d = {'do': 'type', 'target': target, 'text': text}
        if cps:
            d['cps'] = cps
        return s._p(d, at, label, kw)

    def press(s, key, at=None, label=None, **kw):
        return s._p({'do': 'press', 'key': key}, at, label, kw)

    def scroll(s, point, by, at=None, label=None, duration=0.5, **kw):
        return s._p({'do': 'scroll', 'point': {'x': point[0], 'y': point[1]}, 'by': by, 'duration': duration, 'after': 100}, at, label, kw)

    def pause(s, seconds):
        return s.add({'do': 'pause', 'seconds': seconds})

    def waitfor(s, **kw):
        return s.add({'do': 'waitFor', **kw})

    def ev(s, js, at=None, label=None, **kw):
        return s._p({'do': 'eval', 'js': js}, at, label, kw)

    def clicar_fixo(s, sel, ponto, at, label, texto=None, ultimo=False):
        """Botão fixo do app fora da faixa y 96..730 (rodapé de uma janela, X do cabeçalho): o `click` do robô tentaria rolar em vão e
        atrasaria 2 a 6 s (lição do T1/T3 v2). Leva o cursor com `scroll by 0 point`, registra o rect com `type noClick` e clica por `eval`.
        `at` = instante do clique; o cursor parte 0,9 s antes. `texto`: só os elementos de `sel` cujo texto casa (regex, sem diferenciar
        maiúsculas); `ultimo`: o último que casa."""
        s._p({'do': 'scroll', 'point': {'x': ponto[0], 'y': ponto[1]}, 'by': 0, 'duration': 0.3, 'after': 0}, round(max(0.0, at - 0.9), 2), label + ' (cursor)', {})
        alvo = {'selector': sel, **({'hasText': texto} if texto else {}), **({'nth': 'last'} if ultimo else {})}
        s.add({'do': 'type', 'target': alvo, 'text': '', 'noClick': True, 'label': label})
        filtro = f'.filter(b=>/{texto}/i.test(b.textContent))' if texto else ''
        js = f'[...document.querySelectorAll({json.dumps(sel)})]{filtro}.{"pop()" if ultimo else "shift()"}.click()'
        return s._p({'do': 'eval', 'js': js}, round(at, 2), label + ' (clique)', {})

    def cursor_fixo(s, sel, ponto, at, label, texto=None):
        """Leva o cursor a um botão fixo fora da faixa de clique (rodapé do menu, rodapé de janela) SEM clicar: `scroll by 0 point` move o cursor e
        `type noClick` registra o rect para a câmera (padrão do T1)."""
        s._p({'do': 'scroll', 'point': {'x': ponto[0], 'y': ponto[1]}, 'by': 0, 'duration': 0.3, 'after': 0}, round(max(0.0, at), 2), label + ' (cursor)', {})
        alvo = {'selector': sel, **({'hasText': texto} if texto else {})}
        return s.add({'do': 'type', 'target': alvo, 'text': '', 'noClick': True, 'label': label})

    def fim(s):
        s.flush(1e9)
        s.steps.append({'do': 'mark', 'name': 'FIM', 'at': round(s.dur, 2)})

    def out(s):
        sem = SEMENTE[s.n]
        d = {
            'name': f't2-cap{s.n:02d}',
            'title': f'T2 · Cap. {s.n} · {NOMES[s.n]} (narração {str(round(s.dur, 1)).replace(".", ",")} s; marcas L1..L{len(s.linhas)} = início de cada linha do roteiro)',
            'seed': f't2-cap{s.n:02d}', 'pace': s.pace, 'cps': s.cps, 'tail': s.tail,
            'start': {'x': s.start[0], 'y': s.start[1]},
            'seedExtra': BASE_SEMENTES + ([f't2/{sem}'] if sem else []),
            **({'user': USUARIO[s.n]} if s.n in USUARIO else {}),
            'prewarm': s.prewarm or ['/dashboard', '/configuracoes'], 'setup': s.setup or [], 'steps': s.steps,
        }
        return d


# ---------------------------------------------------------------- alvos
def st(do, **kw):
    """passo solto; o `at` já é do relógio novo"""
    return {'do': do, **{k: v for k, v in kw.items() if v is not None}}


BTN = lambda n, **kw: {'role': 'button', 'name': n, 'exact': True, **kw}
LINK = lambda n, **kw: {'role': 'link', 'name': n, 'exact': True, **kw}
TAB = lambda n, **kw: {'role': 'tab', 'name': n, **kw}
TXT = lambda t, **kw: {'text': t, 'exact': True, **kw}
SEL = lambda s, **kw: {'selector': s, **kw}
SW = lambda n, **kw: {'role': 'switch', 'name': n, 'exact': True, **kw}
DLG = '[role=dialog]'
AGUARDA = {'do': 'waitFor', 'idle': True}

# menu lateral (a barra tem um <aside>/<nav>; os itens soltos são links e os grupos são botões)
MENU_LINK = lambda n: LINK(n)
MENU_GRUPO = lambda n: BTN(n)
RODAPE_CONFIG = BTN('Configurações', within='aside')  # botão "Configurações" do rodapé do menu
RODAPE_SAIR = BTN('Sair', within='aside')
ABA_USUARIOS = TAB('Usuários e Permissões')
CARGOS = BTN('Configurações', within='main')           # botão da aba: abre "Configurações de Cargos"
CRIAR_USUARIO = BTN('Criar Usuário', within='main')
NOVO_CARGO = BTN('Novo Cargo')
CAMPO_NOME_CARGO = {'placeholder': 'Ex: Técnico de Campo'}
CAMPO_DESC_CARGO = {'placeholder': 'Descrição opcional'}
BUSCA = {'placeholder': 'Buscar tela ou ação...'}
LIMPAR_BUSCA = BTN('Limpar busca')
TELA = lambda n: SW(f'Acesso à tela {n}')
SETA = lambda n: BTN(f'Ver ações de {n}')
ACAO = lambda n: SW(n)
CHIP = lambda n: BTN(n)
CAMPO_NOME = {'placeholder': 'Nome do usuário'}
CAMPO_SENHA = {'placeholder': 'Crie uma senha segura'}
CAMPO_EMAIL = {'placeholder': 'email@exemplo.com'}
CAMPO_FONE = {'placeholder': '(00) 00000-0000'}
TIPO_USUARIO = SEL(f'{DLG} button[role=switch]:not([aria-label])')


def fechar_eval(texto=r'^\s*fechar\s*$'):
    return (r"(() => { const d = document.querySelector('[role=dialog]'); if (!d) return 'ja fechada'; const b = [...d.querySelectorAll('button')]"
            r".find((x) => [x.textContent, x.getAttribute('aria-label'), x.title].some((v) => /" + texto + r"/i.test(v || ''))); "
            r"if (!b) return 'sem botao Fechar'; b.click(); return 'fechada pelo botao'; })()")


def foco(sel):
    return f"(() => {{ const e = document.querySelector({json.dumps(sel)}); if (!e) return 'sem campo'; e.focus(); return document.activeElement === e ? 'foco ok' : 'foco nao pegou'; }})()"


def colar(texto, at, label):
    """Preenche o campo em foco de uma vez, como um "colar" (execCommand insertText dispara os mesmos eventos de input; ~0,05 s)."""
    js = f"(() => {{ document.execCommand('insertText', false, {json.dumps(texto)}); const e = document.activeElement; return e && e.value; }})()"
    return st('eval', js=js, at=at, label=label)



# ---- alvos da tela de usuários (1.38.9)
URL_USUARIOS = '/configuracoes?tab=usuarios'
SUBTITULO = SEL('main p', hasText='usuários •')                      # "1/15 usuários • 1 ativos"
LINHA = lambda nome: {'role': 'button', 'name': nome, 'within': 'main'}  # linha da lista de usuários (o nome acessível traz cargo e etiqueta)
CONFIG_RODAPE = '[data-sidebar=sidebar] button[aria-label="Configurações"]'  # botão "Configurações" do rodapé do menu (y 770: fora da faixa de clique)
# o app não relê ?tab= quando já está em /configuracoes (navegação interna só muda a query): sai pelo dashboard para a página remontar na aba certa
SETUP_USUARIOS = [{'do': 'goto', 'url': '/dashboard'}, {'do': 'goto', 'url': URL_USUARIOS}, {'do': 'waitFor', 'target': SUBTITULO, 'timeout': 15}, AGUARDA]
ABRE_CARGOS = [{'do': 'click', 'target': CARGOS}, {'do': 'waitFor', 'text': 'Configurações de Cargos', 'timeout': 10}, AGUARDA]
SETUP_CARGOS = SETUP_USUARIOS + ABRE_CARGOS
POP = '[data-radix-popper-content-wrapper]'


def rolar_ate(aria, bloco='center', suave=True):
    """`eval` que rola suave (scrollIntoView) o elemento da janela com esse aria-label para o meio da área rolável: o clique seguinte já o
    encontra à vista (o `click` do robô rolaria por conta própria, 1 a 2,5 s)."""
    return ("(() => { const e = [...document.querySelectorAll('[role=dialog] [aria-label]')].find((x) => x.getAttribute('aria-label') === "
            + json.dumps(aria) + "); if (!e) return 'alvo nao achado: ' + " + json.dumps(aria) + "; e.scrollIntoView({ block: " + json.dumps(bloco)
            + ", behavior: " + ("'smooth'" if suave else "'auto'") + " }); return 'rolando ate ' + " + json.dumps(aria) + "; })()")


def rolar_ate_campo(sel, bloco='center'):
    """Como `rolar_ate`, mas por seletor CSS dentro da janela (campos sem aria-label: e-mail, Tipo de Usuário...)."""
    return ("(() => { const e = document.querySelector('[role=dialog] ' + " + json.dumps(sel) + "); if (!e) return 'alvo nao achado: ' + " + json.dumps(sel)
            + "; e.scrollIntoView({ block: " + json.dumps(bloco) + ", behavior: 'smooth' }); return 'rolando ate ' + " + json.dumps(sel) + "; })()")


# a janela de usuário rola inteira (as duas colunas): volta ao topo, onde ficam os Perfis rápidos
ROLAR_TOPO = ("(() => { const d = document.querySelector('[role=dialog] .overflow-y-auto'); if (!d) return 'sem area rolavel'; "
              "d.scrollTo({ top: 0, behavior: 'smooth' }); return 'topo da janela'; })()")
# cartão da conta no rodapé do menu e itens do menu da conta (cap. 10): conferir na exploração (rec/t2/_ex/c04.mjs)
CARTAO_CONTA = SEL('[data-sidebar=sidebar] button', hasText='Camila Duarte')
ITEM_MENU = lambda n: {'role': 'menuitem', 'name': n}



# ================================================================ capítulos
def cap00():
    """Abertura: o cursor passa pelo menu (Agenda para o técnico; Operacional, Orçamentos e Financeiro para o escritório) e termina no botão Configurações."""
    c = Cap(0, pace=0.6, start=(700, 430), prewarm=['/dashboard'],
            setup=[{'do': 'goto', 'url': '/dashboard'}, {'do': 'waitFor', 'text': 'Olá, Camila!', 'timeout': 15}, AGUARDA])
    c.marcas()
    c.hover({'text': 'Olá, Camila!'}, 1.1, at=0.3, label='tela inicial da Dominex, logada como Camila')
    c.hover(LINK('Dashboard'), 0.2, at=c.A(1, 'equipe', 0.7), label='menu lateral: Dashboard')
    c.hover(LINK('Área do Técnico™'), 0.2, at=c.A(1, 'dando', 0.7), label='menu lateral: Área do Técnico')
    c.hover(BTN('Gestão'), 0.2, at=c.A(1, 'exatamente', 0.7), label='menu lateral: Gestão')
    c.hover(LINK('Agenda'), 0.6, at=c.A(2, 'agenda', 0.7), label='menu: Agenda (o técnico em campo)')
    c.hover(BTN('Operacional'), 0.1, at=c.A(2, 'ordem', 0.7), label='menu: Operacional (a ordem de serviço)')
    c.hover(LINK('Orçamentos'), 0.1, at=c.A(2, 'orçamento', 0.7), label='menu: Orçamentos')
    c.hover(BTN('Financeiro'), 0.8, at=c.A(2, 'financeiro', 0.7), label='menu: Financeiro')
    c.cursor_fixo(CONFIG_RODAPE, (80, 770), at=c.A(3, 'Vamos', 1.2), label='botão Configurações no rodapé do menu')
    c.fim()
    return c


def cap01():
    """Onde ficam os usuários: Configurações (rodapé do menu) > aba Usuários e Permissões; contador, lista, painel e os dois botões."""
    c = Cap(1, pace=0.6, start=(640, 430), prewarm=['/dashboard', '/configuracoes'],
            setup=[{'do': 'goto', 'url': '/dashboard'}, {'do': 'waitFor', 'text': 'Olá, Camila!', 'timeout': 15}, AGUARDA])
    c.marcas()
    # L1: o botão do rodapé fica em y 770 (fora da faixa de clique do robô): cursor por `scroll by 0`, clique por `eval` (padrão do T1)
    c.cursor_fixo(CONFIG_RODAPE, (80, 770), at=0.5, label='botão Configurações no rodapé do menu')
    c.ev(f"document.querySelector('{CONFIG_RODAPE}').click()", at=3.9, label='clica em Configurações (rodapé do menu)')
    c.waitfor(text='Gerencie as configurações do sistema', timeout=12)
    # L2: a aba e o contador
    c.click(ABA_USUARIOS, at=c.A(2, 'Usuários', 0.7), label='aba Usuários e Permissões')
    c.waitfor(target=SUBTITULO, timeout=12)
    c.hover(SUBTITULO, 4.5, at=c.A(2, 'contador', 0.7), label='contador de usuários e vagas')
    # L3: a lista e o painel
    c.hover(LINHA('Camila Duarte'), 1.2, at=c.A(3, 'Camila', 0.7), label='a Camila na lista')
    c.hover(TXT('Selecione um usuário'), 2.0, at=c.A(3, 'painel', 0.7), label='painel: Selecione um usuário')
    # L4: os dois botões
    c.hover(CRIAR_USUARIO, 1.3, at=c.A(4, 'Criar', 0.7), label='botão Criar Usuário')
    c.hover(CARGOS, 4.0, at=c.A(4, 'Configurações', 0.7), label='botão Configurações (cargos)')
    c.fim()
    return c


def cap02():
    """Montando um cargo: Configurações > Novo Cargo > nome, descrição, editor por categoria, Agenda (0/4, a seta e Ver Toda a Agenda) e Área do Técnico."""
    c = Cap(2, pace=0.5, start=(900, 300), prewarm=['/dashboard', '/configuracoes'], setup=SETUP_USUARIOS)
    c.marcas()
    # L1
    c.click(CARGOS, at=c.A(1, 'Configurações', 0.6), label='abre Configurações (cargos)')
    c.waitfor(text='Configurações de Cargos', timeout=10)
    c.hover(TXT('Nenhum cargo cadastrado'), 1.2, at=c.A(1, 'ainda', 0.8), label='a janela de cargos, ainda vazia')
    # L2
    c.click(NOVO_CARGO, at=c.A(2, 'primeiro', 1.2), label='Novo Cargo')
    c.click(CAMPO_NOME_CARGO, at=c.A(2, 'Dou', 0.9), label='clica no campo Nome')
    c.type(CAMPO_NOME_CARGO, 'Técnico de Campo', at=round(c.W(2, 'Técnico', 1) - 0.05, 2), cps=60, noClick=True, label='nome do cargo: Técnico de Campo')
    c.click(CAMPO_DESC_CARGO, at=c.A(2, 'descrição', 0.9), label='clica no campo Descrição')
    c.type(CAMPO_DESC_CARGO, 'Agenda, ferramentas e OS pelo link', cps=60, noClick=True, label='descrição do cargo')
    # L3: a câmera desce pelo editor (categorias) e volta ao topo
    c.scroll((640, 420), 380, at=c.A(3, 'telas', 1.0), label='desce pelo editor: categorias', duration=1.1)
    c.scroll((640, 420), 380, at=c.A(3, 'categoria', 1.0), label='desce pelo editor: mais categorias', duration=1.1)
    c.scroll((640, 420), -760, at=c.A(3, 'cada', 0.6), label='volta ao topo do editor', duration=1.3)
    # L4: a Agenda
    c.hover(SETA('Agenda'), 0.5, at=c.A(4, 'agenda', 0.7), label='linha da Agenda')
    c.click(TELA('Agenda'), at=c.A(4, 'ligo', 0.8), label='liga a tela Agenda')
    # L5: contador 0/4, a seta e Ver Toda a Agenda
    c.hover(TXT('0/4', within=DLG), 0.8, at=c.A(5, 'zero', 0.7), label='contador 0/4 da Agenda')
    c.click(SETA('Agenda'), at=c.A(5, 'Clicando', 0.8), label='abre a seta da Agenda')
    c.hover(ACAO('Ver Toda a Agenda'), 2.2, at=c.A(5, 'Ver', 0.7), label='Ver Toda a Agenda (desligada)')
    c.click(SETA('Agenda'), at=c.A(5, 'deixo', 0.9), label='fecha a seta da Agenda')
    # L6: Área do Técnico
    c.ev(rolar_ate('Acesso à tela Área do Técnico™'), at=c.A(6, 'Ligo', 0.5), label='rola até Operacional')
    c.click(TELA('Área do Técnico™'), at=c.A(6, 'Área', 0.9), label='liga a Área do Técnico')
    c.fim()
    return c


# o que o cap02 deixa pronto (feito sem filmar no `setup` do cap03): janela de cargos aberta no formulário, nome, descrição, Agenda e Área do Técnico ligadas
SETUP_CARGO_TECNICO = SETUP_CARGOS + [
    {'do': 'click', 'target': NOVO_CARGO},
    {'do': 'click', 'target': CAMPO_NOME_CARGO},
    {'do': 'type', 'target': CAMPO_NOME_CARGO, 'text': 'Técnico de Campo', 'noClick': True, 'cps': 60},
    {'do': 'click', 'target': CAMPO_DESC_CARGO},
    {'do': 'type', 'target': CAMPO_DESC_CARGO, 'text': 'Agenda, ferramentas e OS pelo link', 'noClick': True, 'cps': 60},
    {'do': 'click', 'target': TELA('Agenda')},
    {'do': 'eval', 'js': rolar_ate('Acesso à tela Área do Técnico™')},
    {'do': 'wait', 'seconds': 0.8},
    {'do': 'click', 'target': TELA('Área do Técnico™')},
    AGUARDA,
]


def cap03():
    """A ação sem a tela: abre a seta de Ordens de Serviço sem ligar a tela, liga só Editar OS em campo (aviso em itálico, 1/6) e cria o cargo."""
    c = Cap(3, pace=0.5, start=(900, 420), prewarm=['/dashboard', '/configuracoes'], setup=SETUP_CARGO_TECNICO)
    c.marcas()
    # L1: sobe até Serviços e abre a seta de Ordens de Serviço, sem ligar a tela
    c.ev(rolar_ate('Ver ações de Ordens de Serviço'), at=c.A(1, 'lista', 0.6), label='rola até Ordens de Serviço')
    c.hover(SETA('Ordens de Serviço'), 0.5, at=c.A(1, 'Ordens', 0.7, nth=1), label='linha Ordens de Serviço (a tela fica desligada)')
    c.click(SETA('Ordens de Serviço'), at=c.A(1, 'seta', 0.8), label='abre a seta de Ordens de Serviço')
    # L2: liga só Editar OS em campo
    c.ev(rolar_ate('Editar OS em campo'), at=c.A(2, 'Ligo', 0.5), label='rola até a última ação')
    c.click(ACAO('Editar OS em campo'), at=c.A(2, 'Editar', 0.8), label='liga Editar OS em campo')
    c.hover(TXT('A tela está desligada, mas estas ações continuam valendo por conta própria.'), 4.2, at=c.A(2, 'aviso', 0.7),
            label='aviso em itálico: a tela está desligada, mas a ação continua valendo')
    c.hover(TXT('1/6', within=DLG), 1.4, at=c.A(2, 'preenche', 0.7), label='contador 1/6')
    # L3: Criar Cargo (botão do rodapé da janela)
    c.clicar_fixo(f'{DLG} button', (880, 742), c.A(3, 'Criar', 0.0), 'Criar Cargo', texto='Criar Cargo')
    c.waitfor(text='Cargo criado com sucesso!', timeout=8, optional=True)
    c.hover(TXT('Técnico de Campo', within=DLG), 0.6, at=c.A(3, 'Técnico', 0.6), label='o cargo Técnico de Campo na lista')
    c.hover(TXT('3 permissões', within=DLG), 1.2, at=c.A(3, 'três', 0.6), label='etiqueta: 3 permissões')
    c.fim()
    return c


def cap04():
    """O cargo do escritório: Novo Cargo, a busca (orcamento sem acento, financeiro), o resto do dia a dia e Criar Cargo; os dois cargos na lista."""
    c = Cap(4, pace=0.3, start=(900, 420), prewarm=['/dashboard', '/configuracoes'], setup=SETUP_CARGOS)
    c.marcas()
    # L1
    c.click(NOVO_CARGO, at=0.4, label='Novo Cargo')
    c.click(CAMPO_NOME_CARGO, at=c.A(1, 'Chamo', 0.8), label='clica no campo Nome')
    c.type(CAMPO_NOME_CARGO, 'Escritório', at=round(c.W(1, 'Escritório', 1) - 0.05, 2), cps=40, noClick=True, label='nome do cargo: Escritório')
    c.click(CAMPO_DESC_CARGO, at=c.A(1, 'descrição', 0.7), label='clica no campo Descrição')
    c.add(colar('Atendimento, OS, orçamentos e financeiro do dia a dia', None, 'descrição do cargo'))
    # L2: busca sem acento
    c.click(BUSCA, at=c.A(2, 'busca', 0.8), label='clica na busca')
    c.type(BUSCA, 'orcamento', at=round(c.W(2, 'orcamento') - 0.05, 2), cps=14, noClick=True, label='digita orcamento (sem acento)')
    c.click(TELA('Orçamentos'), at=c.A(2, 'Ligo', 0.8), label='liga a tela Orçamentos')
    # L3: busca financeiro
    c.click(BUSCA, at=round(c.L(3) - 0.7, 2), label='clica na busca')
    c.type(BUSCA, 'financeiro', at=round(c.W(3, 'digito') - 0.05, 2), cps=14, clear=True, noClick=True, label='digita financeiro')
    c.click(TELA('Financeiro'), at=c.A(3, 'Ligo', 0.8), label='liga a tela Financeiro')
    c.click(ACAO('Gerenciar Financeiro'), at=c.A(3, 'Gerenciar', 0.8), label='liga Gerenciar Financeiro')
    c.hover(ACAO('Excluir Lançamento Financeiro'), 3.2, at=c.A(3, 'Excluir', 0.7), label='Excluir Lançamento Financeiro fica desligado')
    # L4: limpa a busca e liga o resto
    c.click(LIMPAR_BUSCA, at=c.A(4, 'Limpo', 0.8), label='Limpar busca')
    c.click(TELA('Dashboard'), at=c.A(4, 'Dashboard', 0.8), label='liga Dashboard')
    c.click(TELA('Agenda'), at=c.A(4, 'Agenda', 0.8), label='liga Agenda')
    c.click(SETA('Agenda'), at=c.A(4, 'com', 0.5), label='abre a seta da Agenda')
    c.click(ACAO('Ver Toda a Agenda'), at=c.A(4, 'ver', 0.8), label='liga Ver Toda a Agenda')
    c.ev(rolar_ate('Acesso à tela Ordens de Serviço', 'center'), at=c.A(4, 'Ordens', 1.2), label='rola até Ordens de Serviço')
    c.click(TELA('Ordens de Serviço'), at=c.A(4, 'Ordens', 0.8), label='liga Ordens de Serviço')
    c.click(SETA('Ordens de Serviço'), at=c.A(4, 'Serviço', 0.4), label='abre a seta de Ordens de Serviço')
    c.click(ACAO('Criar OS'), at=c.A(4, 'criar', 0.8), label='liga Criar OS')
    c.click(ACAO('Editar OS'), at=c.A(4, 'editar', 0.8), label='liga Editar OS')
    c.ev(rolar_ate('Acesso à tela Clientes e Fornecedores', 'center', suave=False), at=c.A(4, 'Clientes', 1.2), label='rola até Clientes e Fornecedores')
    c.click(TELA('Clientes e Fornecedores'), at=c.A(4, 'Clientes', 0.8), label='liga Clientes e Fornecedores')
    c.click(SETA('Clientes e Fornecedores'), at=c.A(4, 'Fornecedores', 0.4), label='abre a seta de Clientes e Fornecedores')
    c.click(ACAO('Criar Cliente'), at=c.A(4, 'criar', 0.8, nth=1), label='liga Criar Cliente')
    c.click(ACAO('Editar Cliente'), at=c.A(4, 'editar', 0.8, nth=1), label='liga Editar Cliente')
    c.ev(rolar_ate('Acesso à tela Equipamentos', 'center', suave=False), at=c.A(4, 'Equipamentos', 1.4), label='rola até Equipamentos')
    c.click(TELA('Equipamentos'), at=c.A(4, 'Equipamentos', 0.8), label='liga Equipamentos')
    # L5: Criar Cargo e os dois cargos na lista
    c.clicar_fixo(f'{DLG} button', (880, 742), c.A(5, 'Criar', 0.0), 'Criar Cargo', texto='Criar Cargo')
    c.waitfor(text='Cargo criado com sucesso!', timeout=8, optional=True)
    c.hover(TXT('13 permissões', within=DLG), 0.8, at=c.A(5, 'dois', 0.7), label='etiqueta: 13 permissões (Escritório)')
    c.hover(TXT('3 permissões', within=DLG), 0.8, at=c.A(5, 'cada', 0.7), label='etiqueta: 3 permissões (Técnico de Campo)')
    c.hover(SEL(f'{DLG} button:has(svg.lucide-pencil)', nth=0), 1.0, at=c.A(5, 'lápis', 0.7), label='o lápis edita um cargo (não clica na lixeira)')
    c.fim()
    return c


def cap05():
    """Cadastrando um técnico: Criar Usuário, nome, senha forte (indicador), e-mail, telefone, Vincular a Funcionário (Nenhum), Tipo Técnico, perfil rápido Técnico de Campo."""
    c = Cap(5, pace=0.3, start=(900, 420), prewarm=['/dashboard', '/configuracoes'], setup=SETUP_CARGOS)
    c.marcas()
    # L1: fecha os cargos e abre o formulário
    c.press('Escape', at=0.5, label='fecha a janela de cargos')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.click(CRIAR_USUARIO, at=c.A(1, 'Criar', 0.8), label='Criar Usuário')
    c.waitfor(text='Preencha os dados do novo usuário', timeout=10)
    c.hover(TXT('Foto do Usuário', within=DLG), 1.0, at=c.A(1, 'esquerda', 0.7), label='à esquerda: os dados da pessoa')
    c.hover({'role': 'heading', 'name': 'Permissões', 'within': DLG}, 1.0, at=c.A(1, 'direita', 0.7), label='à direita: as permissões')
    # L2: nome e senha (digitada devagar: o indicador acende os itens na ordem da voz)
    c.click(CAMPO_NOME, at=round(c.L(2) - 0.9, 2), label='clica no campo Nome')
    c.type(CAMPO_NOME, 'Rafael Lima', at=round(c.L(2) - 0.05, 2), cps=40, noClick=True, label='nome: Rafael Lima')
    c.click(CAMPO_SENHA, at=c.A(2, 'crio', 0.8), label='clica no campo Senha')
    c.type(CAMPO_SENHA, '$TUT_SENHA', at=c.A(2, 'senha', 0.05), cps=1.3, noClick=True, label='senha (mascarada): o indicador acende item por item')
    # L3: e-mail, telefone, Vincular a Funcionário
    c.ev(rolar_ate_campo('input[type=email]'), at=c.A(3, 'Agora', 0.5), label='rola até o e-mail')
    c.click(CAMPO_EMAIL, at=c.A(3, 'e-mail', 0.8), label='clica no campo Email')
    c.add(colar('rafael.lima@glacialcold.example', round(c.W(3, 'e-mail') + 0.5, 2), 'e-mail: rafael.lima@glacialcold.example'))
    c.click(CAMPO_FONE, at=c.A(3, 'telefone', 0.8), label='clica no campo Telefone')
    c.type(CAMPO_FONE, '2130001002', at=round(c.W(3, 'telefone') + 0.1, 2), cps=40, noClick=True, label='telefone: (21) 3000-1002')
    c.hover({'role': 'combobox', 'hasText': 'Nenhum', 'within': DLG}, 1.5, at=c.A(3, 'Vincular', 0.9), label='Vincular a Funcionário (fica em Nenhum)')
    # L4: Tipo de Usuário
    c.ev(rolar_ate_campo('button[role=switch]:not([aria-label])'), at=c.A(4, 'Em', 0.5), label='rola até Tipo de Usuário')
    c.hover(TIPO_USUARIO, 0.5, at=c.A(4, 'Tipo', 0.5), label='Tipo de Usuário (Interno)')
    c.click(TIPO_USUARIO, at=c.A(4, 'escolho', 0.8), label='escolhe Técnico')
    c.hover(TXT('Aparece na listagem de técnicos da OS e pode ser adicionado a equipes', within=DLG), 2.0, at=c.A(4, 'aparecer', 0.7), label='legenda do Técnico')
    # L5: perfil rápido Técnico de Campo
    c.ev(ROLAR_TOPO, at=c.A(5, 'prática', 0.6), label='volta ao topo (Perfis rápidos)')
    c.hover(TXT('Perfis rápidos', within=DLG), 0.5, at=c.A(5, 'Perfis', 0.8), label='Perfis rápidos')
    c.click(CHIP('Técnico de Campo'), at=c.A(5, 'Técnico', 0.8), label='clica no perfil rápido Técnico de Campo')
    c.hover(SETA('Agenda'), 0.5, at=c.A(5, 'Agenda', 0.7), label='a Agenda ligou')
    c.ev(rolar_ate('Acesso à tela Área do Técnico™', suave=False), at=c.A(5, 'Área', 1.2), label='rola até a Área do Técnico')
    c.hover(TELA('Área do Técnico™'), 0.4, at=c.A(5, 'Área', 0.6), label='a Área do Técnico ligou')
    c.ev(rolar_ate('Ver ações de Ordens de Serviço', suave=False), at=c.A(5, 'ação', 1.6), label='rola até Ordens de Serviço')
    c.click(SETA('Ordens de Serviço'), at=c.A(5, 'ação', 0.9), label='abre a seta de Ordens de Serviço (tela desligada)')
    c.hover(ACAO('Editar OS em campo'), 1.2, at=c.A(5, 'editar', 0.7), label='Editar OS em campo ligada')
    # L6: Criar Usuário (recarrega a página; a lista volta com o Rafael)
    # pausa de 10 s na voz (pausas.py) no fim da linha 5: o clique cai no começo dela, o app recarrega a página (3 a 10 s) e a linha 6 só marca com a lista já carregada
    c.clicar_fixo(f'{DLG} button', (1060, 742), round(c.linhas[4]['e'], 2), 'Criar Usuário', texto='Criar Usuário')
    c.waitfor(target=LINHA('Rafael Lima'), timeout=30)
    c.hover(LINHA('Rafael Lima'), 1.5, at=c.A(6, 'cargo', 0.7), label='o Rafael na lista, com o cargo Técnico de Campo')
    c.fim()
    return c


def cap06():
    """Acesso Total ou personalizado: Tatiane (Interno), perfil Escritório, Contratos (vira Personalizado), Acesso Total, volta ao Escritório, Criar Usuário."""
    c = Cap(6, pace=0.3, start=(900, 420), prewarm=['/dashboard', '/configuracoes'], setup=SETUP_USUARIOS)
    c.marcas()
    # L1: Criar Usuário e os dados (etapas rápidas)
    c.click(CRIAR_USUARIO, at=0.0, label='Criar Usuário')
    c.waitfor(text='Preencha os dados do novo usuário', timeout=10)
    c.click(CAMPO_NOME, label='clica no campo Nome')
    c.add(colar('Tatiane Ribeiro', None, 'nome: Tatiane Ribeiro'))
    c.click(CAMPO_SENHA, label='clica no campo Senha')
    c.type(CAMPO_SENHA, '$TUT_SENHA', cps=80, noClick=True, label='senha (mascarada)')
    c.click(CAMPO_EMAIL, label='clica no campo Email')
    c.add(colar('tatiane.ribeiro@glacialcold.example', None, 'e-mail: tatiane.ribeiro@glacialcold.example'))
    c.click(CAMPO_FONE, label='clica no campo Telefone')
    c.type(CAMPO_FONE, '2130001008', cps=120, noClick=True, label='telefone: (21) 3000-1008')
    c.ev(rolar_ate_campo('button[role=switch]:not([aria-label])'), at=c.A(1, 'Interno', 0.5), label='rola até Tipo de Usuário')
    c.hover(TIPO_USUARIO, 1.2, at=c.A(1, 'Interno', 0.2), label='Tipo de Usuário fica em Interno')
    # L2: perfil Escritório
    c.ev(ROLAR_TOPO, at=c.A(2, 'Em', 0.6), label='volta ao topo (Perfis rápidos)')
    c.click(CHIP('Escritório'), at=c.A(2, 'Escritório', 0.8), label='clica no perfil rápido Escritório')
    c.scroll((640, 420), 360, at=c.A(2, 'ligam', 1.2), label='percorre as telas ligadas', duration=1.0)
    # L3: Contratos vira Personalizado
    c.click(BUSCA, at=c.A(3, 'Procuro', 0.9), label='clica na busca')
    c.type(BUSCA, 'contratos', at=round(c.W(3, 'Contratos', 1) - 0.1, 2), cps=14, noClick=True, label='digita contratos')
    c.click(TELA('Contratos'), at=c.A(3, 'ligo', 0.8), label='liga a tela Contratos')
    c.hover(CHIP('Escritório'), 0.5, at=c.A(3, 'Escritório', 0.7), label='o chip Escritório apagou')
    c.hover(CHIP('Personalizado'), 1.2, at=c.A(3, 'Personalizado', 0.7), label='o chip Personalizado acendeu')
    c.click(LIMPAR_BUSCA, at=c.A(3, 'cargo', 0.8), label='Limpar busca')
    # L4: Acesso Total
    c.click(CHIP('Acesso Total'), at=c.A(4, 'Acesso', 0.8), label='clica no perfil rápido Acesso Total')
    c.hover(CHIP('Acesso Total'), 5.0, at=c.A(4, 'Acesso', -0.2), label='o cursor fica no Acesso Total')
    # L5: volta ao Escritório
    c.click(CHIP('Escritório'), at=c.A(5, 'Escritório', 0.8), label='clica de novo em Escritório')
    # L6: Criar Usuário
    # pausa de 10 s na voz (pausas.py) no fim da linha 5: clique no começo dela; a linha 6 só marca com a lista já carregada
    c.clicar_fixo(f'{DLG} button', (1060, 742), round(c.linhas[4]['e'], 2), 'Criar Usuário', texto='Criar Usuário')
    c.waitfor(target=LINHA('Tatiane Ribeiro'), timeout=30)
    c.hover(LINHA('Tatiane Ribeiro'), 0.6, at=c.A(6, 'cargo', 0.7), label='a Tatiane na lista, com o cargo Escritório')
    c.fim()
    return c


def cap07():
    """Conferindo o acesso: painel do Rafael (Perfil de acesso, Dados do usuário, Permissões concedidas) e a janela Editar (só olha e cancela)."""
    c = Cap(7, pace=0.5, start=(900, 420), prewarm=['/dashboard', '/configuracoes'], setup=SETUP_USUARIOS)
    c.marcas()
    # L1: clica no Rafael
    c.click(LINHA('Rafael Lima'), at=c.A(1, 'clicar', 0.8), label='clica no Rafael Lima na lista')
    c.waitfor(text='Perfil de acesso', timeout=10)
    c.hover(TXT('Perfil de acesso', within='main'), 1.4, at=c.A(1, 'Perfil', 0.7), label='Perfil de acesso: Técnico de Campo')
    c.hover(TXT('Dados do usuário', within='main'), 1.8, at=c.A(1, 'Dados', 0.7), label='Dados do usuário: Técnico e telefone')
    # L2: Permissões concedidas
    c.scroll((960, 500), 300, at=c.A(2, 'Mais', 0.8), label='desce até Permissões concedidas', duration=0.9)
    c.hover(TXT('Telas (2)', within='main'), 0.8, at=c.A(2, 'duas', 0.7), label='Telas (2): Agenda e Área do Técnico')
    c.hover(TXT('Ações (1)', within='main'), 1.2, at=c.A(2, 'ação', 0.7), label='Ações (1): Editar OS em campo')
    # L3: Editar abre a mesma janela, preenchida; Cancelar
    c.scroll((960, 500), -300, at=c.A(3, 'Editar', 1.9), label='volta ao topo do painel', duration=0.9)
    c.click(BTN('Editar', within='main'), at=c.A(3, 'Editar', 0.8), label='clica em Editar')
    c.waitfor(text='Atualize os dados e permissões do usuário', timeout=10)
    c.hover(CHIP('Técnico de Campo'), 1.2, at=c.A(3, 'preenchida', 0.8), label='a janela vem preenchida, com o chip Técnico de Campo aceso')
    c.clicar_fixo(f'{DLG} button', (960, 742), c.A(3, 'cancelo', 0.0), 'Cancelar', texto='Cancelar')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.fim()
    return c


def cap08():
    """O que o técnico vê: a Dominex aberta como Rafael Lima (gravação à parte): abre na Agenda, menu só com Agenda e Área do Técnico, Área do Técnico e volta."""
    c = Cap(8, pace=0.6, start=(900, 420), prewarm=['/agenda', '/area-tecnico'],
            setup=[{'do': 'goto', 'url': '/agenda'}, {'do': 'waitFor', 'text': 'Rafael Lima', 'timeout': 20}, AGUARDA])
    c.marcas()
    # L1: o cartão da conta mostra o Rafael; abre na Agenda
    c.hover(TXT('Rafael Lima', within='[data-sidebar=sidebar]'), 1.0, at=c.A(1, 'Rafael', 0.8), label='o cartão da conta: Rafael Lima')
    c.hover(LINK('Agenda'), 0.8, at=c.A(1, 'Agenda', 0.7), label='abre na Agenda')
    # L2: o menu
    c.hover(LINK('Agenda'), 0.4, at=c.A(2, 'Agenda', 0.7), label='menu: Agenda')
    c.hover(LINK('Área do Técnico™'), 1.0, at=c.A(2, 'Área', 0.7), label='menu: Área do Técnico')
    c.hover(SEL('[data-sidebar=sidebar]'), 1.5, at=c.A(2, 'apenas', 0.8), label='o menu só tem o que o trabalho pede')
    # L3: Área do Técnico e volta à Agenda
    c.click(LINK('Área do Técnico™'), at=c.A(3, 'Área', 0.8), label='abre a Área do Técnico')
    c.waitfor(idle=True)
    c.click(LINK('Agenda'), at=c.A(3, 'Agenda', 0.8), label='volta para a Agenda')
    c.fim()
    return c


def cap09():
    """Desativar e reativar: o Paulo Souza (8 ativos -> 7 -> 8), Excluir só até a janela de confirmação (Cancelar) e a Camila (só Editar)."""
    c = Cap(9, pace=0.5, start=(900, 420), prewarm=['/dashboard', '/configuracoes'], setup=SETUP_USUARIOS)
    c.marcas()
    # L1: a lista tem oito pessoas
    c.hover(LINHA('Bruno Alves'), 0.8, at=c.A(1, 'lista', 0.7), label='a lista: Bruno Alves')
    c.hover(LINHA('Tatiane Ribeiro'), 1.2, at=c.A(1, 'cadastrei', 0.8), label='a lista: Tatiane Ribeiro (oito pessoas)')
    # L2: o Paulo e o contador
    c.click(LINHA('Paulo Souza'), at=c.A(2, 'Paulo', 0.8), label='clica no Paulo Souza')
    c.hover(SUBTITULO, 2.0, at=c.A(2, 'contador', 0.7), label='contador: 8 usuários ativos')
    # L3: Desativar
    c.click(BTN('Desativar', within='main'), at=c.A(3, 'Desativar', 0.8), label='Desativar')
    c.hover(SUBTITULO, 1.4, at=c.A(3, 'contador', 0.7), label='contador cai para 7')
    c.hover(LINHA('Paulo Souza'), 1.2, at=c.A(3, 'etiqueta', 0.7), label='etiqueta Inativo na lista')
    # L4: Reativar
    c.click(BTN('Reativar', within='main'), at=c.A(4, 'Reativar', 0.8), label='Reativar')
    c.hover(SUBTITULO, 1.4, at=c.A(4, 'contador', 0.7), label='contador sobe para 8')
    # L5: Excluir (só a janela de confirmação)
    c.click(BTN('Excluir', within='main'), at=c.A(5, 'Excluir', 0.8), label='Excluir')
    c.hover(TXT('Excluir usuário permanentemente?'), 1.5, at=c.A(5, 'apaga', 0.7), label='janela: Excluir usuário permanentemente?')
    c.click(BTN('Cancelar'), at=c.A(5, 'cancelo', 0.8), label='Cancelar')
    # L6: a conta da Camila
    c.click(LINHA('Camila Duarte'), at=c.A(6, 'Camila', 0.8), label='clica na Camila Duarte')
    c.hover(BTN('Editar', within='main'), 1.4, at=c.A(6, 'Editar', 0.7), label='só o botão Editar')
    c.fim()
    return c


def cap10():
    """Vagas do plano: o contador e o menu da conta (Assinatura), sem navegar."""
    c = Cap(10, pace=0.5, start=(900, 420), prewarm=['/dashboard', '/configuracoes'], setup=SETUP_USUARIOS)
    c.marcas()
    c.hover(SUBTITULO, 7.0, at=c.A(1, 'contador', 0.7), label='contador: ativos e vagas do plano')
    c.click(CARTAO_CONTA, at=c.A(2, 'Assinatura', 0.9), label='abre o menu da conta')
    c.hover(ITEM_MENU('Assinatura'), 1.8, at=c.A(2, 'menu', 0.6), label='Assinatura (sem clicar)')
    c.press('Escape', at=c.A(2, 'aumenta', 0.2), label='fecha o menu da conta')
    c.fim()
    return c


def cap11():
    """Recapitulando: passeio curto pelas mesmas telas (cargos, formulário com perfis rápidos, lista, painel, Desativar, contador); só olha, não grava nada."""
    c = Cap(11, pace=0.4, start=(900, 420), prewarm=['/dashboard', '/configuracoes'], setup=SETUP_USUARIOS)
    c.marcas()
    # L1: os dois cargos
    c.click(CARGOS, at=c.A(1, 'montou', 1.0), label='abre Configurações (cargos)')
    c.waitfor(text='Configurações de Cargos', timeout=10)
    c.hover(TXT('3 permissões', within=DLG), 0.6, at=c.A(1, 'Técnico', 0.7), label='cargo Técnico de Campo (3 permissões)')
    c.hover(TXT('13 permissões', within=DLG), 0.6, at=c.A(1, 'Escritório', 0.7), label='cargo Escritório (13 permissões)')
    c.hover(SEL(f'{DLG} button:has(svg.lucide-pencil)', nth=0), 0.8, at=c.A(1, 'ações', 0.7), label='o lápis edita o cargo')
    c.press('Escape', at=round(c.L(2) - 0.5, 2), label='fecha a janela de cargos')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    # L2: Rafael e Tatiane, perfis rápidos
    c.hover(LINHA('Rafael Lima'), 0.3, at=c.A(2, 'Rafael', 1.0), label='o Rafael na lista')
    c.hover(LINHA('Tatiane Ribeiro'), 0.3, at=c.A(2, 'Tatiane', 0.1), label='a Tatiane na lista')
    c.click(CRIAR_USUARIO, at=c.A(2, 'aplicando', 0.3), label='abre Criar Usuário')
    c.waitfor(text='Preencha os dados do novo usuário', timeout=10)
    c.hover(CHIP('Personalizado'), 0.8, at=c.A(2, 'Personalizado', 0.6), label='chip Personalizado')
    c.hover(CHIP('Acesso Total'), 0.8, at=c.A(2, 'Acesso', 0.6), label='chip Acesso Total')
    c.clicar_fixo(f'{DLG} button', (960, 742), c.A(2, 'tudo', 0.0), 'Cancelar', texto='Cancelar')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    # L3: conferir, ativar e desativar, vagas
    c.click(LINHA('Rafael Lima'), at=c.A(3, 'pode', 0.8), label='abre o painel do Rafael')
    c.waitfor(text='Perfil de acesso', timeout=10)
    c.hover(TXT('Permissões concedidas', within='main'), 0.8, at=c.A(3, 'fazer', 0.5), label='Permissões concedidas do Rafael')
    c.click(LINHA('Paulo Souza'), at=c.A(3, 'desativar', 0.8), label='abre o painel do Paulo Souza')
    c.hover(BTN('Desativar', within='main'), 0.8, at=c.A(3, 'perder', 0.6), label='Desativar fica no painel')
    c.hover(SUBTITULO, 1.0, at=c.A(3, 'vagas', 0.7), label='contador de vagas')
    c.fim()
    return c


CAPS = {0: cap00, 1: cap01, 2: cap02, 3: cap03, 4: cap04, 5: cap05, 6: cap06, 7: cap07, 8: cap08, 9: cap09, 10: cap10, 11: cap11}

if __name__ == '__main__':
    quais = [int(a) for a in sys.argv[1:]] or sorted(CAPS)
    for n in quais:
        c = CAPS[n]()
        if os.environ.get('ANCHORS'):
            for i, w, t in c.anchors:
                print(f'   anchor L{i} "{w}" -> {t}')
        d = c.out()
        last = -1  # o `at` precisa ser crescente
        for stp in d['steps']:
            if 'at' in stp:
                if stp['at'] < last:
                    print(f'  aviso cap{n:02d}: at {stp["at"]} < {last} em "{stp.get("label") or stp.get("name")}"')
                last = max(last, stp['at'])
        path = os.path.join(os.environ.get('T2_OUT') or HERE, f'cap{n:02d}.json')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
        print(f'cap{n:02d}: {len(d["steps"])} passos, narração {c.dur:.1f} s -> {os.path.relpath(path, HERE)}')
