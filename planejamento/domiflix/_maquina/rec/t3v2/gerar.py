#!/usr/bin/env python3
"""T3 v2 · gera rec/t3v2/cap00..cap13.json (roteiros do robô na Dominex 1.38.9) a partir da voz pronta (t3v2/narracao/capNN.json).

Os capítulos que já existiam no T3 partem dos passos do robô do T3 (rec/t3/capNN.json, os que gravaram sem falha): o gerador copia os passos,
descarta as marcas Ln antigas, desloca os `at` quando a voz ganhou frases inseridas (mapa linha antiga -> linha nova) e troca só os passos
que a 1.38.9 mudou (`subst`: índice do passo no T3 -> passos novos; `antes`: passos novos inseridos antes do índice). As marcas L1..Ln
saem da voz nova. Capítulos novos (cap06, cap07) e o recap (cap13) são escritos do zero, com os `at` saindo da palavra que anuncia cada
passo (A(linha, palavra, folga)): o gesto "pousa" ~1 s depois do início do passo, então `at` = início da palavra - folga.

Rodar de qualquer pasta: `python3 -I rec/t3v2/gerar.py [NN ...]`. Depois: `node rec/record.mjs rec/t3v2/capNN.json --check`.
A cadeia de sementes: capNN parte de t3v2/apos-cap(NN-1) (cap00 a cap02 partem do banco vazio do mundo da aula).
"""
import copy
import json
import os
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TUT = os.path.normpath(os.path.join(HERE, '..', '..'))
NARR = os.environ.get('T3V2_NARR') or os.path.join(TUT, 't3v2', 'narracao')  # T3V2_NARR: pasta com vozes sintéticas, só para testar o gerador
T3 = os.path.join(TUT, 'rec', 't3')

NOMES = ['Abertura', 'A tela de Clientes', 'Cliente empresa pelo CNPJ', 'Cliente pessoa física pelo CEP', 'Origens', 'A ficha do cliente',
         'Etiquetas', 'Campos personalizados', 'Formulário de captação', 'Fornecedores', 'Preparando os equipamentos',
         'Cadastrando um equipamento', 'QR Code e etiqueta', 'Recap e próximo']
# estado de partida de cada capítulo: o último apos-capNN que existe (os capítulos que mexem no banco geram um)
SEMENTE = {0: None, 1: None, 2: None, 3: 'apos-cap02', 4: 'apos-cap03', 5: 'apos-cap04', 6: 'apos-cap05', 7: 'apos-cap06', 8: 'apos-cap07',
           9: 'apos-cap08', 10: 'apos-cap09', 11: 'apos-cap10', 12: 'apos-cap11', 13: 'apos-cap12'}


def norm(s):
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode().lower()
    return ''.join(ch for ch in s if ch.isalnum() or ch in '?')


def carregar(nome):
    p = os.path.join(NARR, nome)
    return json.load(open(p, encoding='utf8')) if os.path.exists(p) else None


class Cap:
    def __init__(s, n, pace=1.0, cps=9, start=(700, 420), prewarm=None, setup=None, linhas_esperadas=None):
        s.n = n
        d = carregar(f'cap{n:02d}.json')
        if d is None:
            raise SystemExit(f'cap{n:02d}: falta t3v2/narracao/cap{n:02d}.json (a voz ainda não foi processada: rodar proc.py)')
        s.words, s.linhas, s.dur = d['words'], d['linhas'], d['dur']
        if linhas_esperadas and len(s.linhas) != linhas_esperadas:
            raise SystemExit(f'cap{n:02d}: a voz tem {len(s.linhas)} linhas, esperava {linhas_esperadas} (o áudio novo ainda não foi processado?)')
        s.antigo = carregar(f'cap{n:02d}.v1.json')  # a voz do T3 antes das emendas (existe só nos capítulos refeitos)
        s.steps, s.pace, s.cps, s.start = [], pace, cps, start
        s.prewarm, s.setup = prewarm, setup  # None: vêm do robô do T3 (adotar) ou, se não houver, do padrão em out()
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
        d = fechar_seguro(d)
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
            s.mark(i)

    def mark(s, i):
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

    def scroll(s, target=None, at=None, label=None, **kw):
        d = {'do': 'scroll'}
        if target is not None:
            d['target'] = target
        return s._p(d, at, label, kw)

    def pause(s, seconds):
        return s.add({'do': 'pause', 'seconds': seconds})

    def waitfor(s, **kw):
        return s.add({'do': 'waitFor', **kw})

    def ev(s, js, at=None, label=None, **kw):
        return s._p({'do': 'eval', 'js': js}, at, label, kw)

    def clicar_fixo(s, sel, ponto, at, label, ultimo=False, texto=None):
        """Botão fixo do app fora da faixa y 96..730 (ex.: o Fechar do cabeçalho de uma janela, o "Aplicar (1)" do rodapé de uma folha): o
        `click` do robô tentaria rolar em vão e atrasaria 2 a 6 s (lição do T1). Leva o cursor com `scroll by 0 point`, registra o rect com
        `type noClick` e clica por `eval`. `at` = instante do clique; o cursor parte 0,9 s antes. `ultimo`: o último botão que casa.
        `texto`: só os elementos de `sel` cujo texto casa (sem diferenciar maiúsculas)."""
        s._p({'do': 'scroll', 'point': {'x': ponto[0], 'y': ponto[1]}, 'by': 0, 'duration': 0.3, 'after': 0}, round(max(0.0, at - 0.9), 2), label + ' (cursor)', {})
        alvo = {'selector': sel, **({'hasText': texto} if texto else {}), **({'nth': 'last'} if ultimo else {})}
        s.add({'do': 'type', 'target': alvo, 'text': '', 'noClick': True, 'label': label})
        filtro = f'.filter(b=>/{texto}/i.test(b.textContent))' if texto else ''
        js = f'[...document.querySelectorAll({json.dumps(sel)})]{filtro}.{"pop()" if ultimo else "shift()"}.click()'
        return s._p({'do': 'eval', 'js': js}, round(at, 2), label + ' (clique)', {})

    def fim(s):
        s.flush(1e9)
        s.steps.append({'do': 'mark', 'name': 'FIM', 'at': round(s.dur, 2)})

    # ---- passos do T3 (rec/t3/capNN.json)
    def deslocamento(s, mapa, extras=None):
        """t (relógio do T3) -> quanto a voz andou (s) naquele ponto, dado o mapa linha antiga -> linha nova. Sem mapa, nada anda.
        `extras`: [(linha antiga, palavra)]: pontos de deslocamento DENTRO de uma linha (a emenda que empurrou o resto da linha, como no cap. 5)."""
        if not mapa or not s.antigo:
            return lambda t: 0.0
        pts = []
        for k, l in enumerate(s.antigo['linhas'], 1):
            nk = mapa.get(k, k)
            pts.append((l['s'], round(s.linhas[nk - 1]['s'] - l['s'], 3)))
        for li, palavra in (extras or []):
            q = norm(palavra)
            velho = next(w for w in s.antigo['words'] if w['linha'] == li - 1 and norm(w['w']).startswith(q))
            novo = next(w for w in s.words if w['linha'] == mapa.get(li, li) - 1 and norm(w['w']).startswith(q))
            pts.append((velho['s'], round(novo['s'] - velho['s'], 3)))
        pts.sort()

        def f(t):
            d = 0.0
            for s0, dl in pts:
                if t + 0.3 >= s0:
                    d = dl
            return d
        return f

    def adotar(s, n_t3, mapa=None, subst=None, antes=None, depois=None, modif=None, extras=None):
        """Copia os passos do robô do T3. `subst[i]`: None (descarta) | passo | lista de passos (já no relógio novo) no lugar do passo i do T3.
        `antes[i]`: lista de passos novos inseridos antes do passo i. `modif[i]`: chaves a mudar no passo i copiado (o `at` ainda é deslocado).
        `depois`: lista de passos novos no fim. As marcas do T3 não entram."""
        t3 = json.load(open(os.path.join(T3, f'cap{n_t3:02d}.json'), encoding='utf8'))
        if s.prewarm is None:
            s.prewarm = t3['prewarm']
        if s.setup is None:
            s.setup = t3['setup']
        desloc = s.deslocamento(mapa, extras)
        subst, antes, modif = subst or {}, antes or {}, modif or {}
        for i, st in enumerate(t3['steps']):
            for novo in antes.get(i, []):
                s.add(copy.deepcopy(novo))
            if st['do'] == 'mark':
                continue
            if i in subst:
                v = subst[i]
                for novo in ([] if v is None else [v] if isinstance(v, dict) else v):
                    s.add(copy.deepcopy(novo))
                continue
            d = copy.deepcopy(st)
            if d.get('at') is not None:
                d['at'] = round(d['at'] + desloc(d['at']), 2)
            d.update(modif.get(i, {}))
            s.add(d)
        for novo in (depois or []):
            s.add(copy.deepcopy(novo))
        return t3

    def out(s):
        sem = SEMENTE[s.n]
        d = {
            'name': f't3v2-cap{s.n:02d}',
            'title': f'T3 v2 · Cap. {s.n} · {NOMES[s.n]} (narração {str(round(s.dur, 1)).replace(".", ",")} s; marcas L1..L{len(s.linhas)} = início de cada linha do roteiro)',
            'seed': f't3v2-cap{s.n:02d}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
            'start': {'x': s.start[0], 'y': s.start[1]},
            **({'seedExtra': [f't3v2/{sem}']} if sem else {}),
            'prewarm': s.prewarm or ['/clientes'], 'setup': s.setup or [], 'steps': s.steps,
        }
        return d


# ---------------------------------------------------------------- alvos
def st(do, **kw):
    """passo solto (para `subst`/`antes`); o `at` já é do relógio novo"""
    return {'do': do, **{k: v for k, v in kw.items() if v is not None}}


BTN = lambda n, **kw: {'role': 'button', 'name': n, 'exact': True, **kw}
LINK = lambda n, **kw: {'role': 'link', 'name': n, 'exact': True, **kw}
TAB = lambda n, **kw: {'role': 'tab', 'name': n, **kw}
TXT = lambda t, **kw: {'text': t, 'exact': True, **kw}
SEL = lambda s, **kw: {'selector': s, **kw}
DLG = '[role=dialog]'
POP = '[data-radix-popper-content-wrapper]'
AGUARDA = {'do': 'waitFor', 'idle': True}
SETUP_CLIENTES = [{'do': 'goto', 'url': '/clientes'}, {'do': 'waitFor', 'text': 'Lista de Clientes'}, {'do': 'waitFor', 'idle': True}]
SETUP_FICHA_COLEGIO = SETUP_CLIENTES + [
    {'do': 'click', 'target': {'text': 'Colégio Monte Verde', 'exact': True}},
    {'do': 'waitFor', 'text': 'Responsável no Local', 'timeout': 10}, {'do': 'waitFor', 'idle': True}]
# o botão "Configurações" do topo da página de Clientes e Fornecedores (o menu lateral também tem uma "Configurações": `within: main`)
CONFIG = BTN('Configurações', within='main')
# "Ações" do cabeçalho da ficha (menu que abre ao passar o mouse e fecha 200 ms depois de sair)
ACOES = SEL("button[aria-haspopup='menu'][aria-label='Ações']", nth=0)
ITEM = lambda n: {'role': 'menuitem', 'name': n}
# botões do menu lateral das janelas de Configurações: o nome acessível traz a descrição junto ("Etiquetas Cores e classificações"),
# então o alvo NÃO pode ser `exact` (o BTN() daria "não achado")
NAV = lambda n: {'role': 'button', 'name': n, 'within': DLG}
CAMPOS_PERSONALIZADOS = NAV('Campos personalizados')
MENU_ETIQUETAS = NAV('Etiquetas')
MENU_CATEGORIAS = NAV('Categorias')
FECHAR_JANELA = 'Fechar'


def fechar_seguro(d):
    """O `click` condicional do botão Fechar (idioma herdado do T3: `when` janela + alvo Fechar) vira `eval` (ver FECHAR_EVAL): na 1.38.9 ele
    travava 30 s quando a janela sumia durante o passo. Vale para os passos adotados do robô do T3 e para os escritos aqui."""
    t = d.get('target') or {}
    if d.get('do') == 'click' and d.get('when') == {'role': 'dialog'} and t.get('role') == 'button' and t.get('name') == 'Fechar':
        novo = {'do': 'eval', 'js': FECHAR_EVAL}
        for k in ('at', 'label'):
            if d.get(k) is not None:
                novo[k] = d[k]
        return novo
    return d


def sem_estas(*sels):
    return sels


# ================================================================ capítulos que vêm do T3
def cap00():
    c = Cap(0, pace=1.0, start=(700, 420), prewarm=['/dashboard'], setup=[{'do': 'goto', 'url': '/dashboard'}, AGUARDA])
    c.marcas()
    # o último hover (menu Gestão) chega ~2 s depois do início do passo na 1.38.9 e segurava 1,5 s: passava do FIM da narração em 1,2 s
    c.adotar(0, modif={10: {'seconds': 0.7}})
    c.fim()
    return c


def cap01():
    """A tela de Clientes: o selo PJ (a voz diz "selo") e o botão "Configurações" (era "Configurar origens")."""
    c = Cap(1, start=(640, 430), prewarm=['/dashboard', '/clientes'], setup=[{'do': 'goto', 'url': '/dashboard'}, AGUARDA])
    c.marcas()
    c.adotar(1, subst={
        23: st('hover', target=CONFIG, seconds=1.0, at=c.A(6, 'Configurações', 0.9), label='botão Configurações'),
        24: st('hover', target=BTN('Formulários de captação'), seconds=1.0, at=c.A(6, 'Formulários', 0.8), label='botão Formulários de captação'),
        25: st('hover', target=BTN('Novo Cliente'), seconds=2.2, at=c.A(6, 'Novo', 0.6), label='botão Novo Cliente'),
    })
    c.fim()
    return c


def cap02():
    """Cliente empresa pelo CNPJ: igual ao T3; o "Criar" fica desabilitado enquanto as etiquetas carregam, então espera a rede ociosa."""
    # pace 0,6 (era 1,0) e digitação/esperas menores: na 1.38.9 cada gesto leva ~0,3 s a mais e a digitação o dobro (a observação de 41 letras levava 8,5 s
    # a cps 16, o celular 5,3 s e o complemento 3,4 s): as marcas L5 a L10 saíam até 3 s atrasadas. O que a fala espera (esperas dos hovers) encurta.
    c = Cap(2, pace=0.6, start=(960, 520), prewarm=['/clientes'], setup=SETUP_CLIENTES[:2] + [AGUARDA])
    c.marcas()
    c.adotar(2, antes={43: [AGUARDA]}, modif={
        23: {'cps': 20}, 27: {'seconds': 1.0}, 28: {'seconds': 1.0}, 30: {'cps': 14}, 31: {'seconds': 1.0}, 33: {'seconds': 4.5}, 38: {'cps': 30}})
    c.fim()
    return c


def cap03():
    c = Cap(3, start=(960, 520), prewarm=['/clientes'], setup=SETUP_CLIENTES[:2] + [AGUARDA])
    c.marcas()
    c.adotar(3, antes={31: [AGUARDA]})
    c.fim()
    return c



def cap04():
    """Origens: agora é a seção "Origens" da janela "Configurações de clientes e fornecedores" (abre nela)."""
    c = Cap(4, pace=0.6, start=(980, 330))   # pace 0,6 (era 1,0): na 1.38.9 a cadeia de hovers e o fechar da janela saíam 0,5 a 0,8 s atrasados (maxLate 0,83)
    c.marcas()
    # os hovers do menu da origem (Site, Editar, Excluir) seguravam 0,7 + 0,6 + 0,6 s e a marca L4 saiu 0,84 s atrasada na 1.38.9: holds menores;
    # Editar e Excluir ganham `at` para o cursor pousar nas mesmas palavras de antes (17,7 s e 18,9 s)
    c.adotar(4, subst={
        1: st('click', target=CONFIG, at=c.A(1, 'Configurações', 1.0), label='botão Configurações'),
        2: st('waitFor', text='Configurações de clientes e fornecedores', timeout=10),
    }, modif={12: {'seconds': 0.4}, 14: {'seconds': 0.35, 'at': 17.0}, 15: {'seconds': 0.35, 'at': 18.3},
              20: {'duration': 2.5}, 21: {'duration': 2.0}})   # as duas rolagens da lista cabem com folga antes do FIM (27,6 s)
    c.fim()
    return c


# Rolagem por `eval` (instantânea para o robô: o cursor não anda e o passo não espera a roda): a lista de clientes até o Marcos (no meio do painel) e de
# volta ao topo; a faixa de abas da ficha até a última aba e de volta à primeira. `scrollIntoView` de um elemento rola só o ancestral que tem rolagem.
def _lista(topo):
    return r"""(() => { const el = [...document.querySelectorAll('p, span, div, h3, h4')].find((e) => e.children.length === 0 && e.textContent.trim() === 'Marcos Antônio Braga'); if (!el) return 'Marcos não achado'; let p = el.parentElement; while (p && p.scrollHeight <= p.clientHeight + 2) p = p.parentElement; if (!p) return 'sem rolagem'; const r = el.getBoundingClientRect(); const q = p.getBoundingClientRect(); p.scrollTo({ top: """ + ("0" if topo else "p.scrollTop + (r.top - q.top) - q.height / 2 + r.height / 2") + r""", behavior: 'smooth' }); return 'lista em ' + Math.round(p.scrollTop); })()"""


LISTA_ATE_MARCOS, LISTA_AO_TOPO = _lista(False), _lista(True)


def _abas(nome, fim):
    return r"""(() => { const t = [...document.querySelectorAll('[role=tab]')].find((x) => /^""" + nome + r"""/.test(x.textContent.trim())); if (!t) return 'aba não achada'; t.scrollIntoView({ behavior: 'smooth', inline: '""" + ('end' if fim else 'start') + r"""', block: 'nearest' }); return 'faixa de abas até """ + nome + r"""'; })()"""


ABAS_ATE_COBRANCAS, ABAS_ATE_GERAL = _abas('Cobranças', True), _abas('Geral', False)


def cap05():
    """A ficha do cliente: "Editar" e "Excluir" foram para o menu "Ações" (abre ao passar o mouse; só passa por cima, sem clicar em item)."""
    # pace 0,6 (era 1,0): na 1.38.9 cada gesto leva ~0,25 s a mais e os grupos de hovers/abas sem folga saíam até 1,6 s atrasados
    c = Cap(5, pace=0.6, start=(980, 480), linhas_esperadas=8)
    c.marcas()
    contato = SEL("button[aria-haspopup='menu'][aria-label='Ações']", nth='last')  # o menu da linha do contato é o último "Ações" da tela
    # a frase nova da linha 2 ("...o menu Ações, com Editar e Excluir.") não coube na janela e o `emendar.py` abriu 0,55 s de silêncio depois dela
    # (`empurra`): o resto da linha 2 e tudo o que vem depois andou, então os passos copiados do T3 acompanham (extras = ponto dentro da linha)
    c.adotar(5, mapa={i: i for i in range(1, 9)}, extras=[(2, 'clicando')], subst={
        6: [st('hover', target=ACOES, seconds=0.5, at=c.A(2, 'Ações', 0.9), label='menu Ações do cabeçalho (abre ao passar o mouse)'),
            st('click', target=ACOES, unless={'role': 'menuitem', 'name': 'Editar'}, label='abre o menu se ainda não abriu'),
            st('hover', target=ITEM('Editar'), seconds=0.4, at=c.A(2, 'Editar', 0.5), label='Editar (só passa o mouse)')],
        7: [st('hover', target=ITEM('Excluir'), seconds=0.5, at=c.A(2, 'Excluir', 0.5), label='Excluir (só passa o mouse)'),
            st('press', key='Escape', label='fecha o menu sem escolher')],
        # fim (linha 8): a fala cita 6 abas em 5,5 s e o `click` de uma aba leva ~1,4 s na 1.38.9 (a rolagem da faixa 2,3 s e o clique de volta à Geral 4 s,
        # com a faixa rolada): as abas depois de Tarefas só recebem o cursor (hover ~0,6 s, sem trocar de painel), a faixa rola por `eval` (~0,4 s, sem
        # esperar) e o clique de volta à Geral vem com a faixa já recolhida (1,3 s). Antes: marcas até 4,7 s atrasadas.
        49: st('eval', js=ABAS_ATE_COBRANCAS, at=round(c.W(8, 'tem') - 1.6, 2), label='faixa de abas rola para a direita'),
        50: st('hover', target=TAB('Estoque'), seconds=0.05, at=c.A(8, 'Estoque', 1.3), label='aba Estoque'),
        51: st('hover', target=TAB('Chamados'), seconds=0.05, at=c.A(8, 'Chamados', 0.6), label='aba Chamados'),
        52: st('hover', target=TAB('Contratos'), seconds=0.05, at=c.A(8, 'Contratos', 0.6), label='aba Contratos'),
        53: st('hover', target=TAB('Documentos'), seconds=0.05, at=c.A(8, 'Documentos', 0.6), label='aba Documentos'),
        54: st('hover', target=TAB('Financeiro'), seconds=0.05, at=c.A(8, 'Financeiro', 1.0), label='aba Financeiro'),
        55: None,
        56: st('hover', target=TAB('Cobranças'), seconds=0.05, at=c.A(8, 'Cobranças', 0.6), label='aba Cobranças'),
        57: [st('eval', js=ABAS_ATE_GERAL, at=round(c.W(8, 'importante') - 1.0, 2), label='faixa de abas volta ao início'),
             st('click', target=TAB('Geral'), at=round(c.W(8, 'importante') - 0.3, 2), label='volta para a aba Geral')],
    }, modif={
        37: {'target': contato}, 38: {'target': contato},
        9: {'seconds': 1.0},   # o campo de busca fica aberto 1 s (eram 1,9: o Esc saía 1 s atrasado)
    })
    c.fim()
    return c


def cap08():
    """Formulário de captação (era o cap. 6 do T3): os mesmos passos. Na 1.38.9 cada gesto leva ~0,25 s a mais e a digitação do título 2,3 s (era 1,2 s):
    `pace` 0,5 (era 0,75) e uma pausa de 1,5 s na voz depois de "título." (`narracao/pausas.py 8 15.20:1.5`), que desloca as linhas 3 a 8
    (`mapa` identidade: o `deslocamento` lê o capNN.v1.json, a voz antes da pausa)."""
    c = Cap(8, pace=0.5, start=(980, 480))
    c.marcas()
    # A volta ao Dominex (Enviar -> "Cadastro enviado" -> espera -> goto /clientes de 1,6 s) levava ~2,6 s a mais do que a fala dá entre "envia." e "E de
    # volta no Dominex": 2ª pausa na voz de 2,4 s nessa fronteira (`pausas.py 8 15.20:1.5 44.932:2.4`, o vão de silêncio entre as duas frases), Celular e
    # CEP digitados mais depressa (cps 60) e a espera da tela de sucesso de 0,9 para 0,5 s. Antes: a marca L8 saía 3,5 s atrasada e a Luana, 3,6 s.
    c.adotar(6, mapa={i: i for i in range(1, 9)}, modif={41: {'cps': 60}, 43: {'cps': 60}, 50: {'seconds': 0.5}})
    c.fim()
    return c


def cap09():
    """Fornecedores (era o cap. 7 do T3): "Etiquetas" é o 2º campo do formulário (Nome, Etiquetas, CNPJ...); a frase nova ("Lá em cima, em
    Etiquetas, escolho a Preferencial.") cabe no buraco de 4 s que a emenda do T3 deixou, entre as observações e o "Salvar"."""
    c = Cap(9, pace=0.6, start=(980, 480), linhas_esperadas=6)
    c.marcas()
    # Na 1.38.9 a digitação custa ~0,1 s por caractere (era ~0,06): os 7 campos (14,8 s) não cabiam nos 11 s que a voz dá ao cadastro e as marcas
    # saíam até 4,4 s atrasadas. Nome, CNPJ, contato e telefone seguem digitados (cps 60, cada um na palavra da voz); e-mail, endereço e observações
    # entram de uma vez, como um "colar" (`colar()`), cada um na palavra da voz. Os Tab ganham `at` na ordem nova.
    c.adotar(7, mapa={1: 1, 2: 2, 3: 3, 4: 5, 5: 6}, modif={
        13: {'at': 15.9, 'cps': 60}, 14: {'times': 2, 'at': 17.5}, 15: {'at': 17.6, 'cps': 60}, 16: {'at': 18.9}, 17: {'at': 19.0, 'cps': 30},
        18: {'at': 19.7}, 19: {'at': 19.8, 'cps': 60}, 20: {'at': 20.9}, 22: {'at': 21.8}, 24: {'at': 23.2},
        # a ficha do fornecedor abre ~1,6 s depois do clique (T3: 1 s) e a cadeia de hovers saía 0,6 a 0,8 s atrasada: `at` no ritmo real e esperas menores
        33: {'at': 32.9, 'seconds': 0.2}, 34: {'at': 33.85, 'seconds': 0.9}, 35: {'at': 35.45, 'seconds': 2.5},
    }, subst={
        21: colar('vendas@venturagas.example', 21.1, 'E-mail'),
        23: colar('Rua das Palmeiras, 45, Niterói', 22.0, 'Endereço'),
        25: colar('Gás R-410A e tubo de cobre', 23.4, 'Observações: o que compro dele'),
        26: [st('click', target=BTN('Sem etiquetas'), at=c.A(4, 'Etiquetas', 0.9), label='abre a lista de etiquetas'),
             st('click', target=BTN('Preferencial', within=POP), at=c.A(4, 'Preferencial', 0.8), label='marca a Preferencial'),
             st('press', key='Escape', at=c.A(4, 'Preferencial', -0.6), label='fecha a lista')],
    })
    c.fim()
    return c


# Lista de opções do campo personalizado (equipamentos, 1.38.9): foco e "Adicionar opção" por `eval` (instantâneo e sem depender de onde o foco está).
# O T3 usava `press Tab` e Tab,Tab,Enter,Shift+Tab,Shift+Tab: na 1.38.9 o Radix devolve o foco ao seletor de tipo DEPOIS do Tab (a fala "127 V" caiu no
# seletor e o "Opção 2" nunca apareceu). O botão é achado pelo texto; a linha nova é a última `input[placeholder^="Opção"]`.
OPCAO1_FOCO = r"""(() => { const e = document.querySelector('[role=dialog] input[placeholder="Opção 1"]'); if (!e) return 'sem Opção 1'; e.focus(); return document.activeElement === e ? 'foco na Opção 1' : 'foco não pegou'; })()"""
ADD_OPCAO = r"""(async () => { const d = document.querySelector('[role=dialog]'); const sel = 'input[placeholder^="Opção"]'; const antes = d.querySelectorAll(sel).length; const b = [...d.querySelectorAll('button')].find((x) => /Adicionar opção/.test(x.textContent || '')); if (!b) return 'sem botão Adicionar opção'; b.click(); for (let i = 0; i < 60; i++) { const ins = d.querySelectorAll(sel); if (ins.length > antes) { const u = ins[ins.length - 1]; u.focus(); return 'nova: ' + u.placeholder + (document.activeElement === u ? ' (foco ok)' : ' (foco não pegou)'); } await new Promise((r) => setTimeout(r, 10)); } return 'a opção nova não apareceu'; })()"""


def cap10():
    """Preparando os equipamentos (era o cap. 8 do T3): "Configurar Campos" abre "Configurações de equipamentos" (Categorias, Etiquetas, Campos
    personalizados); as categorias passaram a ser uma seção dela (sem aba, sem "Nova Categoria" nem "Criar"); frase nova no fim: Etiquetas.
    Pace 0.5 e `seconds` curtos (a 0.9 a cadeia de hovers atrasou 3 s); opções da lista por `eval`; digitação a 40 cps."""
    c = Cap(10, pace=0.5, start=(960, 620), linhas_esperadas=6)
    c.marcas()
    c.adotar(8, subst={
        11: [st('waitFor', text='Configurações de equipamentos', timeout=10),
             st('click', target=CAMPOS_PERSONALIZADOS, at=16.85, label='seção Campos personalizados (a janela abre em Categorias)'),
             st('waitFor', target={'selector': '[role=dialog] textarea'}, timeout=8)],
        26: st('eval', js=OPCAO1_FOCO, at=34.7, label='foco na primeira opção'),
        28: st('eval', js=ADD_OPCAO, at=36.0, label='Adicionar opção (a linha nova já recebe o foco)'),
        30: st('eval', js=ADD_OPCAO, at=37.35, label='Adicionar opção (a linha nova já recebe o foco)'),
        32: None,
        38: st('click', target=MENU_CATEGORIAS, at=c.A(4, 'categorias', 0.9), label='seção Categorias (sem fechar a janela)'),
        39: None, 40: None, 41: None, 43: None,
        48: None,
        49: st('type', target={'placeholder': 'Nome da categoria'}, text='Multi Split', cps=40, at=55.15, label='nome da categoria: Multi Split'),
        52: st('click', target=SEL('[role=dialog] input[type=color] + button'), at=58.35, label='o botão + cria a categoria'),
    }, modif={
        12: {'seconds': 0.2, 'at': 18.55}, 13: {'seconds': 0.15, 'at': 19.4}, 14: {'seconds': 0.15, 'at': 20.15},
        15: {'seconds': 0.15, 'at': 21.3}, 16: {'seconds': 0.15, 'at': 22.3}, 17: {'seconds': 0.9, 'at': 23.1},
        18: {'seconds': 0.3, 'at': 24.85}, 19: {'seconds': 0.2, 'at': 25.75}, 20: {'seconds': 0.3, 'at': 26.7},
        23: {'cps': 14}, 27: {'cps': 40}, 29: {'cps': 40}, 31: {'cps': 40},
        50: {'at': 57.35},
    }, depois=[
        st('click', target=MENU_ETIQUETAS, at=c.A(6, 'Etiquetas', 0.9), label='seção Etiquetas'),
        # a cadeia final (Nova etiqueta -> campo -> nome -> seletor de cor -> verde -> Salvar) leva ~6 s na 1.38.9 e a fala só dá ~5,7: começa ~0,8 s antes (o
        # nome é digitado quando o locutor diz "crio") e os dois últimos cliques seguem o ritmo real (verde logo depois de "cor", Salvar com "etiqueta")
        st('click', target=BTN('Nova etiqueta'), at=c.A(6, 'crio', 1.7), label='Nova etiqueta'),
        st('click', target={'placeholder': 'Ex.: BLOQUEADO'}, at=c.A(6, 'Em', 1.4), label='clica no campo do nome'),
        st('type', target={'placeholder': 'Ex.: BLOQUEADO'}, text='Em garantia', cps=40, noClick=True, at=round(c.W(6, 'Em') - 0.8, 2), label='nome da etiqueta: Em garantia'),
        st('click', target=SEL(f'{DLG} button:has(span.font-mono)'), at=c.A(6, 'escolho', 0.9), label='abre o seletor de cor'),
        st('click', target=preset('#22C55E'), at=round(c.W(6, 'uma') + 0.35, 2), label='verde'),
        st('click', target=BTN('Salvar etiqueta'), at=round(c.W(6, 'Salvar') + 0.3, 2), label='Salvar etiqueta'),
        st('waitFor', text='Etiqueta criada', timeout=6, optional=True),
    ])
    c.fim()
    return c


def cap11():
    """Cadastrando um equipamento (era o cap. 9 do T3): a página não tem mais abas; duas frases inseridas (as etiquetas do cliente na hora de
    escolher; o campo Etiquetas do equipamento, logo abaixo da Categoria), que deslocam o resto da voz."""
    c = Cap(11, pace=0.6, start=(880, 500), linhas_esperadas=12,
            prewarm=['/equipamentos', '/clientes'], setup=[{'do': 'goto', 'url': '/equipamentos'}, {'do': 'waitFor', 'text': 'Lista de Equipamentos'}, AGUARDA])
    c.marcas()
    c.pending = [(64.3 if mi == 12 else mt, mi) for mt, mi in c.pending]  # a volta à ficha começa na pausa da voz, antes da linha 12: a marca L12 sai junto (senão sairia "atrasada")
    opcao = {'role': 'option', 'name': 'Colégio Monte Verde'}
    mapa = {1: 1, 2: 2, 3: 4, 4: 6, 5: 7, 6: 8, 7: 9, 8: 10, 9: 11, 10: 12}
    c.adotar(9, mapa=mapa, subst={
        1: None,
        # `at` = L3 - 0,2: o primeiro gesto da linha começa até 0,25 s antes dela, senão a marca L3 sobe só depois do hover (2,5 s de atraso falso)
        8: [st('hover', target=opcao, seconds=round(max(0.5, c.L(4) - c.L(3) - 1.8), 2), at=round(c.L(3) - 0.2, 2), label='as etiquetas do cliente aparecem na lista'),
            st('click', target=opcao, at=round(c.L(4) - 1.0, 2), label='escolhe o Colégio Monte Verde')],
        # com a etiqueta marcada o campo Etiquetas tem um tab stop a mais (o Tab do T3 caía um campo antes e todo o preenchimento saía deslocado:
        # Marca no Modelo, Modelo no Nº de Série...): o foco vai direto ao campo Marca; e, no 2º equipamento, direto ao campo Tensão (era Tab x7)
        16: st('eval', js="document.querySelector('[role=dialog] input[placeholder=\"Marca\"]').focus()", at=round(c.L(6) - 0.05, 2), label='foco no campo Marca'),
        54: st('eval', js="[...document.querySelectorAll('[role=dialog] [role=combobox]')].find((e) => /^Selecione$/.test(e.textContent.trim())).focus()", label='foco no campo Tensão'),
        # a digitação da 1.38.9 (~0,09 s por caractere) não cabe nos 6 s da fala "Marca, modelo, ..., data": os dois valores longos entram de uma vez
        # (o foco já está no campo, pelo Tab); Marca, Modelo e Nº de Série continuam digitados
        23: colar('18.000 BTUs', None, 'Capacidade'),
        25: colar('Sala dos professores', None, 'Local'),
        # atalho do cliente novo (L10): o nome do 2º aparelho também entra de uma vez (30 letras levavam 2,3 s e a fala "Termino o aparelho e crio" saía 1,9 s atrasada)
        50: colar('Cassete 36.000 BTUs - Recepção', None, 'Nome: Cassete 36.000 BTUs - Recepção'),
    }, modif={
        # o nome do aparelho (42 letras) a cps 16 levava 5,6 s e a fala diz "Hi-Wall dezoito mil BTUs, sala dos professores" em 4,2: cps 40 (~4,2 s)
        12: {'cps': 40},
        44: {'cps': 60},  # "Pousada Sol Nascente" na busca do cliente
        # a volta à ficha (goto + ficha + aba levam 5,6 s na 1.38.9, 3,5 s no T3) começa logo depois do "Criar", dentro da pausa de 2,5 s da voz
        # (`pausas.py 11 64.0:2.5`); a aba chega junto do "O aparelho já tá lá"
        60: {'at': 64.3},
    }, antes={
        16: [st('click', target=BTN('Selecione uma ou mais etiquetas'), at=c.A(5, 'Etiquetas', 0.9), label='campo Etiquetas (logo abaixo da Categoria)'),
             st('click', target=BTN('Em garantia', within=POP), at=c.A(5, 'garantia', 0.8), label='marca Em garantia'),
             st('press', key='Escape', at=c.A(5, 'garantia', -0.5), label='fecha a lista')],
    })
    c.fim()
    return c


def cap12():
    """QR Code e etiqueta (era o cap. 10 do T3): igual (o Hi-Wall agora tem o selo Em garantia embaixo do nome e o menu Ações)."""
    # pace 0,6 (era 0,9): os gestos da 1.38.9 levam ~0,25 s a mais e a marca L4 saiu 1,1 s atrasada
    c = Cap(12, pace=0.6, start=(1060, 560))
    c.marcas()
    # depois do Enviar (T3 41..44) os gestos da 1.38.9 levam ~1 s a mais (clique na aba Anexos ~1,8 s, envio ~2,2 s, clique na lista ~1,5 s): o `at`
    # acompanha o que o app consegue (a tela já saía na palavra certa da fala; só a marca de atraso passava de 0,8 s) e a espera do anexo encurta
    c.adotar(10, modif={41: {'at': 53.95}, 43: {'at': 56.6}, 44: {'at': 58.1, 'seconds': 2.8}})
    c.fim()
    return c


def colar(texto, at, label):
    """Preenche o campo em foco de uma vez, como um "colar": `execCommand('insertText')` dispara os mesmos eventos de input da digitação (o React
    atualiza o campo) e leva ~0,05 s, qualquer que seja o texto; o valor do campo fica no `actions.json` (`value`) para conferir. Usar nos campos
    longos quando a digitação (~0,1 s por caractere na 1.38.9) não cabe na fala."""
    js = f"(() => {{ document.execCommand('insertText', false, {json.dumps(texto)}); const e = document.activeElement; return e && e.value; }})()"
    return st('eval', js=js, at=at, label=label)


# Plano B do Esc: clicar o "Fechar" da janela por `eval` (instantâneo). O `click` condicional do T3 (`when: dialog` + alvo Fechar) travava 30 s na 1.38.9: o
# `when` ainda via a janela na animação de saída, o alvo sumia entre o `waitFor visible` e o `boundingBox` (sem timeout) e o capítulo todo atrasava.
FECHAR_EVAL = r"""(() => { const d = document.querySelector('[role=dialog]'); if (!d) return 'ja fechada'; const b = [...d.querySelectorAll('button')].find((x) => [x.textContent, x.getAttribute('aria-label'), x.title].some((v) => /^\s*fechar\s*$/i.test(v || ''))); if (!b) return 'sem botao Fechar'; b.click(); return 'fechada pelo botao'; })()"""


def fechar_janela(at, espera=0.5):
    """Esc fecha a janela; se o Esc não bastar, o botão Fechar por `eval` (lição do T3 + a da 1.38.9: nada de `click` condicional). Termina com a janela fechada.
    `espera`: segundos entre o Esc e o plano B (0,25 nos capítulos apertados: a janela já saiu em ~0,2 s)."""
    return [st('press', key='Escape', at=at, label='fecha a janela'), st('wait', seconds=espera),
            st('eval', js=FECHAR_EVAL, label='Fechar (se o Esc não fechou)'),
            st('waitFor', gone={'role': 'dialog'}, timeout=8)]


def cap13():
    """Recap (era o cap. 11 do T3): o tour é reescrito na ordem da fala (a frase nova das etiquetas e do campo Horário de acesso entra no meio);
    a parte do QR Code (linhas 2 e 3) é a do T3, deslocada."""
    c = Cap(13, pace=0.5, start=(1000, 520), prewarm=['/clientes', '/equipamentos'], setup=SETUP_CLIENTES[:2] + [AGUARDA], linhas_esperadas=3)
    c.marcas()
    colegio, marcos = TXT('Colégio Monte Verde'), TXT('Marcos Antônio Braga')
    selos_ficha = {'title': 'Contrato PMOC', 'exact': True, 'nth': 1}  # nth 0 é o selo da linha da lista
    L1 = [
        st('hover', target=TXT('Lista de Clientes'), seconds=0.9, at=0.8, label='lista de clientes'),
        st('click', target=colegio, at=c.A(1, 'empresa', 0.7), label='cliente empresa pelo CNPJ'),
        st('waitFor', text='Responsável no Local', timeout=10),
        # Marcos está no fim da lista: o `click` rolaria a lista sozinho (~2,5 s) e a roda do mouse levava 1,1 s (e, com a rolagem a mais, o clique 3 s):
        # a lista rola por `eval` (Marcos no meio do painel) e volta ao topo enquanto a janela de origens está aberta
        st('eval', js=LISTA_ATE_MARCOS, at=4.6, label='desce a lista de clientes até o pessoa física'),
        st('click', target=marcos, at=5.45, label='cliente pessoa física pelo CEP'),
        st('click', target=CONFIG, at=c.A(1, 'organizou', 0.6), label='organizou as origens (Configurações)'),
        st('waitFor', target={'role': 'dialog'}, timeout=8),
        st('eval', js=LISTA_AO_TOPO, at=8.9, label='volta ao topo da lista de clientes'),
        *fechar_janela(round(c.W(1, 'colocou'), 2), espera=0.25),
        st('click', target=colegio, at=9.9, label='responsável no local com WhatsApp'),
        st('hover', target={'label': 'Abrir WhatsApp do cliente', 'nth': 1}, seconds=0.3, at=11.5, timeout=5, optional=True, label='ícone verde do WhatsApp (só passa o mouse)'),
        # frase nova: etiquetas coloridas e o campo Horário de acesso (a ficha do colégio já está aberta)
        st('hover', target=selos_ficha, seconds=0.6, at=13.2, label='os selos coloridos da ficha'),
        st('hover', target=TXT('Horário de acesso', within='main'), seconds=0.6, at=c.A(1, 'Horário', 0.9), label='a linha Horário de acesso'),
        st('click', target=BTN('Formulários de captação'), at=c.A(1, 'Criou', 0.1, nth=1), label='formulário de captação'),
        st('waitFor', text='Cadastro de novos clientes', timeout=8),
        *fechar_janela(round(c.W(1, 'cadastrar') + 0.4, 2), espera=0.25),
        st('click', target=TAB('Fornecedores'), at=c.A(1, 'cadastrou', 0.2, nth=1), label='aba Fornecedores'),
        # (sem o clique na ficha do fornecedor: a lista de fornecedores já mostra o Ventura com a etiqueta e o clique custava 1,6 s)
        # os 3 cliques da janela de Configurações de equipamentos levam ~1,4 s cada na 1.38.9: `at` espaçados pelo tempo real e a cadeia começa antes
        st('click', target=LINK('Equipamentos'), at=c.A(1, 'equipamentos', 0.85), label='equipamentos prontos'),
        st('waitFor', text='Lista de Equipamentos', timeout=10),
        st('click', target=BTN('Configurar Campos'), at=c.A(1, 'categoria', 1.08), label='Configurar Campos (abre em Categorias: com categoria)'),
        st('waitFor', text='Configurações de equipamentos', timeout=8),
        st('click', target=CAMPOS_PERSONALIZADOS, at=c.A(1, 'personalizado', 0.78), label='Campos personalizados'),
        st('click', target=MENU_ETIQUETAS, at=c.A(1, 'etiqueta', 0.26, nth=1), label='Etiquetas'),
        *fechar_janela(round(c.W(1, 'QR') + 0.1, 2), espera=0.25),
    ]
    # L2 (passos 33..40 do T3, deslocados): cada clique leva 1,1 a 1,8 s; os `at` seguem a cadeia (ficha 29,6, aba 31,1, equipamento 33,1, QR 34,1) e a
    # voz ganhou 1 s depois de "sistema." (`pausas.py 13 35.14:1.0`) para a marca L3 e o hover do QR não passarem de 0,8 s
    c.adotar(11, mapa={1: 1, 2: 2, 3: 3}, subst={i: None for i in range(1, 33)}, antes={1: L1},
             modif={35: {'at': 29.6}, 36: {'at': 31.1}, 38: {'at': 33.1}, 40: {'at': 34.1, 'seconds': 0.3}})
    c.fim()
    return c


# selos de etiqueta: o selo "cheio" (ficha, cartão Informações, janelas) traz o nome no `title`; a linha da lista usa o resumo (primeira etiqueta + "+N")
SELO_RESUMO = SEL("span[aria-label^='Etiquetas:']", nth=0)
COR = SEL(f'{DLG} button:has(span.font-mono)')  # o botão do seletor de cor (mostra o hexadecimal)
SELECT_ETIQUETAS = BTN('Sem etiquetas')  # o campo "Etiquetas" dos formulários (lista de várias)


def preset(hexa):
    return {'title': hexa, 'exact': True}


def fechar_config(at):
    """Fecha a janela de Configurações logo depois de "Salvar etiqueta" (T3 v2): o 1º Esc fecha o seletor de cor, se ainda estiver aberto, e o 2º a
    janela; o botão Fechar só entra se sobrar janela (lição da exploração: o Esc não fecha a janela quando o foco saiu dela)."""
    return [st('press', key='Escape', at=at, label='fecha o seletor de cor'), st('wait', seconds=0.3),
            st('press', key='Escape', when={'role': 'dialog'}, label='fecha a janela de Configurações'), st('wait', seconds=0.5),
            st('eval', js=FECHAR_EVAL, label='Fechar (se o Esc não fechou)'),
            st('waitFor', gone={'role': 'dialog'}, timeout=8)]


def cap06():
    """Etiquetas (capítulo novo): Configurações > Etiquetas, criar "Contrato PMOC", marcar no Colégio Monte Verde (e na Preferencial), ver na ficha,
    na lista e no filtro. A voz ganhou 4 pausas (`narracao/pausas.py 6 18.56:1.2 24.84:1.2 30.96:3.0 34.20:1.0`): o robô leva ~1 s por clique e a
    fala cita 3 cliques em 2,5 s (cor, Salvar), o formulário de edição abre e rola, e o Salvar espera ~3 s a gravação. `pace` 0,5 e digitação a cps 40
    (a digitação real anda a ~0,1 s por caractere). Os `at` vão para onde o gesto POUSA na palavra (folga = tempo do gesto: clique ~0,8 s, hover ~0,55 s)."""
    c = Cap(6, pace=0.5, start=(980, 480), prewarm=['/clientes'], setup=SETUP_FICHA_COLEGIO, linhas_esperadas=5)
    c.marcas()
    NOME = {'placeholder': 'Ex.: BLOQUEADO'}
    # L1: o cursor aponta o botão
    c.hover(CONFIG, 0.6, at=c.A(1, 'fornecedores', 1.0), label='o botão Configurações')
    # L2: Configurações > Etiquetas (o cursor já está no botão: o clique pousa quase na hora)
    c.click(CONFIG, at=c.A(2, 'Configurações', 0.5), label='abre Configurações')
    c.waitfor(text='Configurações de clientes e fornecedores', timeout=10)
    c.click(MENU_ETIQUETAS, at=c.A(2, 'Etiquetas', 1.0), label='seção Etiquetas')
    c.waitfor(text='Classifique clientes e fornecedores com cores fáceis de reconhecer.', timeout=8)
    c.hover(TXT('Preferencial', within=DLG), 0.7, at=c.A(2, 'Preferencial', 0.8), label='a etiqueta Preferencial já está lá')
    # L3: Nova etiqueta, nome (clica no campo antes e digita na palavra), cor, Salvar etiqueta
    c.click(BTN('Nova etiqueta'), at=c.A(3, 'Nova', 0.9), label='Nova etiqueta')
    c.click(NOME, at=c.A(3, 'escrevo', 0.8), label='clica no campo do nome')
    c.type(NOME, 'Contrato PMOC', at=round(c.W(3, 'Contrato', 1) - 0.05, 2), cps=40, noClick=True, label='nome da etiqueta: Contrato PMOC')
    c.click(COR, at=c.A(3, 'escolho', 0.4), label='abre o seletor de cor')
    c.click(preset('#3B82F6'), at=round(c.W(3, 'cor') + 0.0, 2), label='azul')   # cai na pausa depois de "cor"
    # (o "Salvar etiqueta" funciona com o seletor de cor ainda aberto: explorado na 1.38.9, e1)
    c.click(BTN('Salvar etiqueta'), at=c.A(3, 'Salvar', 0.85), label='Salvar etiqueta')
    c.waitfor(text='Etiqueta criada', timeout=6, optional=True)
    for d in fechar_config(round(c.L(4) - 0.05, 2)):  # a janela fecha no silêncio entre a frase e o "Pra usar"
        c.add(d)
    # L4: ficha > Ações > Editar > Etiquetas
    c.hover(ACOES, 0.4, at=c.A(4, 'Ações', 0.8), label='menu Ações da ficha')
    c.click(ACOES, unless={'role': 'menuitem', 'name': 'Editar'}, label='abre o menu se ainda não abriu')
    c.click(ITEM('Editar'), at=c.A(4, 'Editar', 0.6), label='Editar')
    c.waitfor(text='Editar Cliente', timeout=10)
    c.waitfor(idle=True)
    # o formulário abre no topo: a roda até o fim traz o campo Etiquetas (o `scroll` por alvo levava 2,6 s)
    c.scroll(point={'x': 640, 'y': 400}, by=700, duration=0.5, after=100, label='desce até o campo Etiquetas')
    c.click(SELECT_ETIQUETAS, at=c.A(4, 'Etiquetas', 0.5), label='abre a lista de etiquetas')
    c.click(BTN('Contrato PMOC', within=POP), at=c.A(4, 'nova', 0.6), label='marca Contrato PMOC')
    c.click(BTN('Preferencial', within=POP), at=c.A(4, 'Preferencial', 0.7), label='marca a Preferencial (dá pra marcar mais de uma)')
    c.press('Escape', at=round(c.W(4, 'mais') - 0.1, 2), label='fecha a lista')
    c.click(BTN('Salvar'), at=c.A(4, 'Salvar', 0.85), label='Salvar')
    c.waitfor(gone={'role': 'dialog'}, timeout=12)
    # L5: aparecem na ficha, na lista e no filtro
    c.hover({'title': 'Contrato PMOC', 'exact': True, 'nth': 1}, 0.35, at=c.A(5, 'ficha', 0.55), label='os selos na ficha')
    c.hover(SELO_RESUMO, 0.4, at=c.A(5, 'lista', 0.55), label='na lista: o selo e o +1')
    c.click(BTN('Filtros'), at=c.A(5, 'Filtros', 1.5), label='Filtros')  # o 1º clique da folha leva ~1,6 s: sai 0,6 s antes (o Aplicar chegava 0,9 s atrasado)
    c.click(BTN('Contrato PMOC', within=DLG), at=c.A(5, 'ver', 0.9), label='marca Contrato PMOC no filtro')
    # "Aplicar (1)" fica no rodapé fixo da folha (y 748..788, fora da faixa de clique do robô): leva o cursor e clica por eval
    c.clicar_fixo(f'{DLG} button', (1056, 768), round(c.W(5, 'etiqueta') + 0.1, 2), 'Aplicar o filtro', texto='Aplicar')
    c.fim()
    return c


def cap07():
    """Campos personalizados (capítulo novo): Configurações > Campos personalizados, criar "Horário de acesso" (Texto), tipos, clientes x fornecedores,
    preencher na ficha do Colégio Monte Verde. A voz ganhou 4 pausas (`narracao/pausas.py 7 14.24:1.0 27.36:1.0 30.31:2.5 32.56:5.0`): a espera do
    Salvar campo, o fechamento da janela, o formulário de edição que abre, rola e recebe o clique no campo, e os ~3 a 6 s que a gravação do
    cliente leva (a pausa final sai da edição com `cortes`). `pace` 0,5, digitação a cps 40."""
    c = Cap(7, pace=0.5, start=(980, 480), prewarm=['/clientes'], setup=SETUP_FICHA_COLEGIO, linhas_esperadas=5)
    c.marcas()
    TIPO = {'role': 'combobox', 'within': DLG}
    NOME_CAMPO = SEL(f'{DLG} section input', nth=0)
    CAMPO_HORARIO = {'label': 'Horário de acesso'}
    # L1: abre Configurações > Campos personalizados
    c.click(CONFIG, at=c.A(1, 'campos', 1.0), label='abre Configurações')
    c.waitfor(text='Configurações de clientes e fornecedores', timeout=10)
    c.click(CAMPOS_PERSONALIZADOS, at=c.A(1, 'informação', 1.0), label='seção Campos personalizados')
    c.waitfor(text='Crie informações adicionais para cadastro, ficha e portal.', timeout=8)
    # L2: Novo campo, nome (clica antes e digita na palavra), tipo Texto, Salvar campo
    c.click(BTN('Novo campo'), at=c.A(2, 'Novo', 0.9), label='Novo campo')
    c.click(NOME_CAMPO, at=c.A(2, 'escrevo', 0.85), label='clica no campo do nome')
    c.type(NOME_CAMPO, 'Horário de acesso', at=round(c.W(2, 'Horário', 1) - 0.25, 2), cps=40, noClick=True, label='nome do campo: Horário de acesso')
    c.hover(TIPO, 0.5, at=c.A(2, 'tipo', 0.7), label='o tipo continua em Texto')
    c.click(BTN('Salvar campo'), at=c.A(2, 'Salvar', 0.85), label='Salvar campo')
    c.waitfor(text='Campo criado', timeout=6, optional=True)
    # L3: os outros tipos; Obrigatório e Portal; Cancelar (cada hover de opção custa ~0,75 s)
    c.click(TIPO, at=c.A(3, 'Número', 0.9), label='abre a lista de tipos')
    c.hover({'role': 'option', 'name': 'Número'}, 0.2, at=round(c.W(3, 'Número') - 0.3, 2), label='Número')
    c.hover({'role': 'option', 'name': 'Data'}, 0.2, at=round(c.W(3, 'Data') - 0.35, 2), label='Data')
    c.hover({'role': 'option', 'name': 'Lista de opções'}, 0.2, at=round(c.W(3, 'Lista') - 0.35, 2), label='Lista de opções')
    c.hover({'role': 'option', 'name': 'Sim/Não'}, 0.2, at=round(c.W(3, 'Sim') - 0.4, 2), label='Sim/Não')
    # NÃO usar Esc aqui: com uma opção em foco (o mouse passou por ela) o Esc fecha a lista E a janela inteira (e2b); clicar em "Texto" (o tipo atual) só fecha a lista
    c.click({'role': 'option', 'name': 'Texto'}, at=round(c.W(3, 'Não') + 0.3, 2), label='volta ao Texto (fecha a lista sem trocar o tipo)')
    c.hover({'role': 'switch', 'name': 'Obrigatório'}, 0.4, at=c.A(3, 'obrigatório', 0.7), label='interruptor Obrigatório', optional=True)
    c.hover({'role': 'switch', 'name': 'Mostrar no Portal do Cliente'}, 0.4, at=c.A(3, 'Portal', 0.7), label='interruptor Mostrar no Portal do Cliente', optional=True)
    c.click(BTN('Cancelar'), at=round(c.L(4) - 0.9, 2), label='Cancelar (fecha o formulário)')
    # L4: clientes x fornecedores
    c.click(BTN('Fornecedores', within=DLG), at=c.A(4, 'deles', 0.85), label='Fornecedores')
    c.click(BTN('Clientes', within=DLG), at=c.A(4, 'aqui', 0.5), label='volta para Clientes')
    # L5: a janela fecha na pausa antes do "Pra preencher"; depois, na ficha: Ações, Editar, campo novo, Salvar
    for d in fechar_janela(round(c.L(5) - 1.0, 2)):  # Esc (o foco está no botão Clientes, dentro da janela) e, se não fechar, Fechar
        c.add(d)
    c.hover(ACOES, 0.4, at=c.A(5, 'Ações', 0.8), label='menu Ações da ficha')
    c.click(ACOES, unless={'role': 'menuitem', 'name': 'Editar'}, label='abre o menu se ainda não abriu')
    c.click(ITEM('Editar'), at=c.A(5, 'Editar', 0.7), label='Editar')
    c.waitfor(text='Editar Cliente', timeout=10)
    c.waitfor(idle=True)
    # a roda até o fim traz o campo novo (o `scroll` por alvo levava 2,7 s); o clique no campo cai na pausa e a digitação sai na palavra "escrevo"
    c.scroll(point={'x': 640, 'y': 400}, by=900, duration=0.55, after=100, label='desce até o campo Horário de acesso')
    c.click(CAMPO_HORARIO, at=round(c.W(5, 'escrevo') - 0.9, 2), label='clica no campo Horário de acesso')
    c.type(CAMPO_HORARIO, 'Depois das 17h', at=c.W(5, 'escrevo'), cps=40, noClick=True, label='o horário no campo novo')
    c.click(BTN('Salvar'), at=c.A(5, 'Salvar', 0.5), label='Salvar')
    c.waitfor(gone={'role': 'dialog'}, timeout=15)
    c.hover(TXT('Horário de acesso', within='main'), 1.0, at=c.A(5, 'Informações', 0.7), label='a linha Horário de acesso no cartão Informações')
    c.fim()
    return c

CAPS = {0: cap00, 1: cap01, 2: cap02, 3: cap03, 4: cap04, 5: cap05, 6: cap06, 7: cap07, 8: cap08, 9: cap09, 10: cap10, 11: cap11, 12: cap12, 13: cap13}

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
        for stp in d['steps']:
            if 'at' in stp:
                if stp['at'] < last:
                    print(f'  aviso cap{n:02d}: at {stp["at"]} < {last} em "{stp.get("label") or stp.get("name")}"')
                last = max(last, stp['at'])
        path = os.path.join(os.environ.get('T3V2_OUT') or HERE, f'cap{n:02d}.json')  # T3V2_OUT: saída de teste (voz sintética)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
        print(f'cap{n:02d}: {len(d["steps"])} passos, narração {c.dur:.1f} s -> {os.path.relpath(path, HERE)}')
