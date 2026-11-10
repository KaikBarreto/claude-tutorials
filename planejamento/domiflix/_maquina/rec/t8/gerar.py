#!/usr/bin/env python3
"""T8 · gera rec/t8/cap00..cap15.json (roteiros do robô) a partir da voz pronta (t8/narracao/capNN.json).

Aula inteira no COMPUTADOR (janela 1280x800, 2x), logada como Camila Duarte (admin, Glacial Cold Brasil), na Dominex 1.38.19. Os `at`
saem da palavra que anuncia cada passo (A(linha, palavra, folga)): o gesto "pousa" ~0,7 a 1 s depois do início do passo (clique =
deslocamento + 0,85 s; digitação = clique + texto), então `at` = início da palavra - folga.
Rodar de qualquer pasta: `python3 -I rec/t8/gerar.py [NN ...]`. Depois: `node rec/record.mjs rec/t8/capNN.json --check`.

Estado de partida: rec/t8/cadeia.json (a cadeia de sementes até o fim do T2/T7 + `t8/inicio`, gerado por rec/t8/semear.py). Cada capítulo
que mexe no banco deixa `t8/apos-capNN` (rec/t8/snap.mjs) e o seguinte parte dele: SEMENTE[n] é o último que existe.

Particularidades (lições deste tutorial, ver docs/08-licoes.md):
 - Menus das linhas (RowActionsMenu, botão "Ações") abrem por hover (80 ms) e fecham 200 ms depois de sair: `hover` no gatilho e,
   por garantia, `click` com `unless` o item do menu.
 - Selects do Radix: passo `select`. Selects com busca (Grupo, Fornecedor, grupo do configurador) são botões que abrem uma lista
   com busca: clique no gatilho e clique na opção.
 - Material novo nasce com TODOS os locais marcados em "Locais deste material" (padrão da 1.38.9): o robô só digita o mínimo.
 - Local novo (Van 01) mostra TODOS os materiais marcados no configurador até alguém configurar: o robô clica em "Desmarcar todos"
   (sem fala) antes de "Adicionar grupo".
1.38.19 (fase 1, 04/11):
 - O Estoque abre em "Estoque geral" (somente leitura); os locais são a lista lateral "Locais de estoque" (LOCAL_ABA, ENGRENAGEM =
   botão "Configurar local: <nome>"). Cadastrar/entrada/saída pedem um local: SETUP_LOCAL já clica em "Estoque Principal".
 - Menu lateral recolhido no `setup` (botão "Toggle Sidebar"): aberto, a 1280 px a tabela perde colunas e a aba Relatório sai do quadro.
 - Material novo só aparece na lista depois que a consulta `accessible-inventory-ids` (staleTime 30 s, sem invalidação ao salvar) é
   refeita: `c.refocar()` simula o foco da janela (só vale com a consulta vencida, >30 s da carga; o ensaio rápido espera 31 s).
 - Compras: lista + detalhe lado a lado; "Nova compra" é um menu; o detalhe não tem "Voltar" no computador (esperar "Nova cotação").
   CARD_ORDEM precisa de "Itens:" (a cotação do mesmo fornecedor tem o mesmo formato de cartão).
 - Inventário: depois de "Criar inventário" a janela fecha e o inventário só abre ao clicar na linha; "Finalizar" fecha a janela sozinha.
 - Kardex: o período saiu dos Filtros (seletor "Este mês" no topo); o filtro Consumo continua ligado e esconde o histórico do material:
   tirar antes de escolher o Gás. A faixa de Filtros só abre se o mouse passou pelo botão (hover antes do clique).
 - Relatório: a rolagem é a do `main` interno (roda do mouse funciona); a linha do material abre o histórico ali mesmo (sem janela).
 - Menu aberto deixa o resto da tela oculto para o robô: `pause 0.5` depois do Escape (no ensaio rápido, sem `at`, o clique seguinte falha).
"""
import json, os, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
NARR = os.path.normpath(os.path.join(HERE, '..', '..', 't8', 'narracao'))
CAD = json.load(open(os.path.join(HERE, 'cadeia.json'), encoding='utf8'))
BASE = CAD['inicio']
# estado de partida de cada capítulo: o último apos-capNN que existe (só os capítulos que mudam o banco geram um)
SEMENTE = {0: None, 1: None, 2: None}
for _n in range(3, 16):
    SEMENTE[_n] = f'apos-cap{_n - 1:02d}'
# sementes extras só deste capítulo (não encadeiam)
EXTRA = {}
# localStorage de partida de todo capítulo: o aviso "Você tem 1 chamado de cliente aguardando" (Dashboard) já foi visto
STORAGE = {'dominex:portal-tickets-seen:d40f5787-1779-501f-900c-ddb2b90a36e5': '2031-01-01T00:00:00.000Z'}

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

NOMES = ['Abertura', 'A tela e as seis abas', 'Cadastrar um material', 'Entrada, saída e estoque baixo', 'Locais e grupos de material',
         'Transferir para a van', 'Quem enxerga cada local', 'Todo movimento no Kardex', 'Requisição de compra',
         'Cotações e fornecedor por material', 'Ordem de compra e recebimento', 'A nota fiscal em XML', 'Contar e ajustar',
         'O saldo numa data', 'Compras, média paga e preço', 'Recapitulando']

# foco da janela: a janela some (hidden) e volta (visible); o react-query refaz as consultas vencidas (staleTime de 30 s)
REFOCAR_JS = ('(()=>{const d=document,set=(v)=>{Object.defineProperty(d,"visibilityState",{configurable:true,get:()=>v});'
              'Object.defineProperty(d,"hidden",{configurable:true,get:()=>v==="hidden"});window.dispatchEvent(new Event("visibilitychange"))};'
              'set("hidden");set("visible");delete d.visibilityState;delete d.hidden;return 1})()')
# rolagem suave do contêiner interno da página (o `main` que tem overflow-y auto): evita o clique rolar sozinho por ~2 s (lição do T3 v2)
ROLAR = lambda y: ('(()=>{const m=[...document.querySelectorAll("main")].find(e=>getComputedStyle(e).overflowY==="auto");'
                   f'if(m)m.scrollTo({{top:{y},behavior:"smooth"}});return 1}})()')
MICRO = 'µ'   # o "µ" do material semeado ("Capacitor 35 µF") e da nota fiscal fictícia: o mesmo caractere


def norm(s):
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode().lower()
    return ''.join(ch for ch in s if ch.isalnum() or ch in '?')


class Cap:
    def __init__(s, n, pace=0.5, cps=11, start=(760, 420), prewarm=None, setup=None, user=None):
        s.n = n
        d = json.load(open(f'{NARR}/cap{n:02d}.json', encoding='utf8'))
        s.words, s.linhas, s.dur = d['words'], d['linhas'], d['dur']
        s.steps = []
        s.pace, s.cps, s.start = pace, cps, start
        s.prewarm = prewarm or ['/dashboard', '/estoque']
        s.setup = list(setup or []) + [{'do': 'eval', 'js': OBS}]
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

    def A(s, i, palavra, folga=0.9, nth=0):
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
        if at is not None:
            d['at'] = round(at, 2)
        if label:
            d['label'] = label
        d.update(kw)
        return s.add(d)

    def click(s, target, at=None, label=None, **kw):
        return s._p({'do': 'click', 'target': target}, at, label, kw)

    def hover(s, target, seconds=0.9, at=None, label=None, **kw):
        kw.setdefault('optional', True)   # cosmético: se o alvo não existir, o robô segue (o ensaio acusa)
        kw.setdefault('timeout', 4)
        # O robô é sequencial: um hover longo que atravessa o início de uma linha atrasaria a marca Ln (e a narração dessa linha, na
        # montagem). Então ele é partido em dois, com a marca no meio (o segundo trecho leva o rótulo + " (continua)").
        if at is not None:
            fim = at + 0.55 + seconds
            for mt, mi in sorted(s.pending):
                if at + 0.7 < mt < fim - 0.25:
                    s1 = max(0.1, round(mt - at - 0.55, 2))
                    s2 = max(0.2, round(fim - mt - 0.2, 2))
                    s._p({'do': 'hover', 'target': target, 'seconds': s1}, at, label, dict(kw))
                    return s._p({'do': 'hover', 'target': target, 'seconds': s2}, mt, (label + ' (continua)') if label else None, dict(kw))
        return s._p({'do': 'hover', 'target': target, 'seconds': seconds}, at, label, kw)

    def type(s, target, text, at=None, label=None, cps=None, **kw):
        d = {'do': 'type', 'target': target, 'text': text}
        if cps:
            d['cps'] = cps
        return s._p(d, at, label, kw)

    def select(s, target, option, at=None, label=None, **kw):
        return s._p({'do': 'select', 'target': target, 'option': option}, at, label, kw)

    def press(s, key, at=None, label=None, **kw):
        return s._p({'do': 'press', 'key': key}, at, label, kw)

    def scroll(s, target=None, by=None, at=None, label=None, **kw):
        d = {'do': 'scroll'}
        if target is not None:
            d['target'] = target
        if by is not None:
            d['by'] = by
        return s._p(d, at, label, kw)

    def pause(s, seconds):
        return s.add({'do': 'pause', 'seconds': seconds})

    def waitfor(s, **kw):
        return s.add({'do': 'waitFor', **kw})

    def upload(s, target, arquivo, at=None, label=None, **kw):
        return s._p({'do': 'upload', 'target': target, 'file': arquivo}, at, label, kw)

    def ev(s, js, at=None, label=None, **kw):
        return s._p({'do': 'eval', 'js': js}, at, label, kw)

    def clicar_fixo(s, sel, ponto, at, label, ultimo=False, texto=None):
        """Botão fixo do app fora da faixa y 96..730 (ex.: o rodapé "Salvar" de uma janela alta): o `click` do robô tentaria rolar em
        vão e atrasaria 2 a 6 s (lição do T1). Leva o cursor com `scroll by 0 point`, registra o rect com `type noClick` e clica por
        `eval`. `at` = instante do clique; o cursor parte 0,9 s antes. `ultimo`: o último botão que casa (janela aninhada).
        `texto`: só os elementos de `sel` cujo texto casa (sem diferenciar maiúsculas), ex.: o botão "Salvar"."""
        s._p({'do': 'scroll', 'point': {'x': ponto[0], 'y': ponto[1]}, 'by': 0, 'duration': 0.3, 'after': 0}, round(max(0.0, at - 0.9), 2), label + ' (cursor)', {})
        alvo = {'selector': sel, **({'hasText': texto.strip('^$')} if texto else {}), **({'nth': 'last'} if ultimo else {})}
        s.add({'do': 'type', 'target': alvo, 'text': '', 'noClick': True, 'label': label, 'optional': True, 'timeout': 4})
        filtro = f'.filter(b=>new RegExp({json.dumps(texto)},"i").test(b.textContent))' if texto else ''
        js = f'[...document.querySelectorAll({json.dumps(sel)})]{filtro}.{"pop()" if ultimo else "shift()"}.click()'
        return s._p({'do': 'eval', 'js': js}, round(at, 2), label + ' (clique)', {})

    def refocar(s, at=None, label='atualiza as listas (o app refaz a consulta ao voltar o foco da janela)'):
        """Material novo não aparece na lista até a consulta `accessible-inventory-ids` (staleTime 30 s, sem invalidação ao salvar:
        achado para o time do app) ser refeita. O gatilho do próprio app é o foco da janela (REFOCAR_JS); só vale com a consulta vencida (>30 s da carga, sempre o caso no vídeo)."""
        return s._p({'do': 'eval', 'js': REFOCAR_JS}, at, label, {})

    def fim(s):
        s.flush(1e9)
        s.steps.append({'do': 'eval', 'js': 'JSON.stringify(window.__avisos || "sem observador")', 'label': 'avisos de erro na tela'})
        s.steps.append({'do': 'mark', 'name': 'FIM', 'at': round(s.dur, 2)})

    def out(s):
        sem = SEMENTE[s.n]
        d = {
            'name': f't8-cap{s.n:02d}',
            'title': f'T8 · Cap. {s.n} · {NOMES[s.n]} (narração {str(round(s.dur, 1)).replace(".", ",")} s; marcas L1..L{len(s.linhas)} = início de cada linha do roteiro)',
            'seed': f't8-cap{s.n:02d}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
            'start': {'x': s.start[0], 'y': s.start[1]},
            'seedExtra': list(BASE) + ([f't8/{sem}'] if sem else []) + EXTRA.get(s.n, []),
            'prewarm': s.prewarm, 'setup': s.setup, 'steps': s.steps,
            'storage': dict(STORAGE),
        }
        if s.user:
            d['user'] = s.user
        return d


# ---------------------------------------------------------------- alvos
BTN = lambda n, **kw: {'role': 'button', 'name': n, 'exact': True, **kw}
BTNX = lambda n, **kw: {'role': 'button', 'name': n, **kw}               # nome por substring ("Filtros" vira "Filtros 1" com filtro ativo)
LINK = lambda n: {'role': 'link', 'name': n, 'exact': True}
TAB = lambda n, **kw: {'role': 'tab', 'name': n, 'exact': True, **kw}
TXT = lambda t, **kw: {'text': t, 'exact': True, **kw}                    # texto INTEIRO igual (e na mesma caixa)
P = lambda t, **kw: {'text': t, 'within': 'main', **kw}                   # texto por substring, sem diferenciar caixa
SEL = lambda s, **kw: {'selector': s, **kw}
ITEM = lambda n: {'role': 'menuitem', 'name': n}
OPCAO = lambda n: {'role': 'option', 'name': n}
DLG = '[role=dialog]'
GESTAO = BTN('Gestão')

# abas principais da tela de Estoque (role=tab)
ABA_ATUAL = TAB('Estoque Atual')
ABA_KARDEX = TAB('Histórico de Materiais (Kardex)')
ABA_COMPRAS = TAB('Compras de Material')
ABA_INVENT = TAB('Inventários')
ABA_POSICAO = TAB('Posição de Estoque')
ABA_RELAT = TAB('Relatório')
# cabeçalho
BTN_IMPORTAR = {'role': 'button', 'name': 'Importar XML de NF-e', 'exact': True}   # aria-label do botão (o texto visível é "Importar XML (NF-e)")
BTN_CONFIG = BTN('Configurações', within='main')
# Estoque Atual
BUSCA = {'placeholder': 'Buscar material...', 'exact': True}
FILTROS = BTNX('Filtros', within='main')
EXPORTAR = BTN('Exportar estoque', within='main')
CADASTRAR = BTN('Cadastrar Material', within='main')
LINHA = lambda nome: f'main tbody tr:has-text("{nome}")'                # linha da tabela "Itens do Estoque"
GATILHO = lambda nome: SEL(f'{LINHA(nome)} button[aria-label="Ações"]')   # botão "Ações" da linha (abre por hover)
TRIANGULO = lambda nome: SEL(f'{LINHA(nome)} span[aria-label^="Estoque abaixo do mínimo"]')
CARTAO = lambda nome: TXT(nome)                                           # cartão de resumo (Total de itens, Valor investido (R$), Estoque baixo)
# formulário de material / janelas com campo rotulado: o rótulo não está ligado ao campo, então acha-se o campo dentro do bloco do rótulo
CAMPO_ROT = lambda rot, ctl='input': SEL(f'{DLG} div:has(> label:text-is("{rot}")) {ctl}')
# 1.38.19: os locais viraram a lista lateral "Locais de estoque" (botão do local + botão "Configurar local: <nome>")
LOCAL_ABA = lambda nome: SEL(f'aside[aria-label="Locais de estoque"] button:has-text("{nome}")')
GERAL = SEL('aside[aria-label="Locais de estoque"] button:has-text("Estoque geral")')
ENGRENAGEM = lambda nome: {'role': 'button', 'name': f'Configurar local: {nome}', 'exact': True}
MENU_LATERAL = {'role': 'button', 'name': 'Toggle Sidebar', 'nth': 0}

SETUP_APP = lambda rota, esperar: [
    {'do': 'goto', 'url': rota}, {'do': 'waitFor', 'text': esperar, 'timeout': 25}, {'do': 'waitFor', 'idle': True}]
SETUP_DASH = SETUP_APP('/dashboard', 'Olá, Camila!')
# menu lateral recolhido: com ele aberto, a 1280 px a tabela perde colunas e a aba Relatório sai do quadro
SETUP_ESTOQUE = SETUP_APP('/estoque', 'Controle de peças e materiais') + [{'do': 'click', 'target': MENU_LATERAL}, {'do': 'pause', 'seconds': 0.8}]
# a visão abre em "Estoque geral" (somente leitura); quem cadastra ou movimenta escolhe o local antes
SETUP_LOCAL = SETUP_ESTOQUE + [{'do': 'click', 'target': LOCAL_ABA('Estoque Principal')}, {'do': 'pause', 'seconds': 0.6}]

ALERTA = '[role=alertdialog]'
CARTAO_REQ = SEL('main button:has-text("Reposição de gás, cobre e capacitor")')   # cartão da requisição na lista de Compras
CARD_ORDEM = lambda forn: f'main div.rounded-lg.border.p-3:has-text("Itens:"):has-text("{forn}")'    # cartão de uma ordem de compra (tela da requisição)
GAT_ORDEM = lambda forn: SEL(f'{CARD_ORDEM(forn)} button[aria-label="Ações"]')
LINHA_MATERIAL = lambda nome: f'main div.rounded-md.border.p-2:has-text("{nome}")'  # bloco de um material (tela da requisição)
LINHA_USUARIO = lambda nome: f'{DLG} div.flex.items-center.gap-3:has(p:text-is("{nome}"))'
PRECO_UNIT = lambda mat: SEL(f'{DLG} tbody tr:has-text("{mat}") td:nth-child(3) input')   # cotação: valor unitário do material


def setup_aba(aba, esperar):
    return SETUP_LOCAL + [{'do': 'click', 'target': TAB(aba)}, {'do': 'waitFor', 'text': esperar, 'timeout': 20}, {'do': 'waitFor', 'idle': True}]


SETUP_COMPRAS = setup_aba('Compras de Material', 'Requisições de Compra')
SETUP_REQUISICAO = SETUP_COMPRAS + [{'do': 'click', 'target': CARTAO_REQ}, {'do': 'waitFor', 'text': 'Nova cotação', 'timeout': 15},
                                    {'do': 'waitFor', 'idle': True}]
SETUP_INVENT = setup_aba('Inventários', 'Novo inventário')
SETUP_POSICAO = setup_aba('Posição de Estoque', 'Valor em estoque')


def menu_linha(c, nome, item, t_menu, t_item, rot):
    """Menu da linha (botão "Ações") que abre por hover: hover no gatilho, `click` de garantia (só se o menu não abriu) e clique no item."""
    gat = GATILHO(nome)
    c.hover(gat, 0.3, at=t_menu, label=f'menu da linha {rot}')
    c.click(gat, unless=ITEM(item), label=f'abre o menu de {rot} se ainda não abriu')
    return c.click(ITEM(item), at=t_item, label=f'{item} ({rot})')


# ================================================================ capítulos
def cap00():
    """Abertura: o Dashboard; o cursor vai ao grupo Gestão do menu, abre o Estoque e passa pelas seis abas.
    `at` fixos com o custo medido na gravação (1ª interação ~2,3 s, abrir o grupo ~2,7 s, abrir o Estoque ~4,2 s: lição do T12)."""
    c = Cap(0, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/estoque'], setup=SETUP_DASH)
    c.mark(1)
    c.click(GESTAO, at=3.0, label='abre o grupo Gestão')
    c.click(LINK('Estoque'), at=6.6, label='abre o Estoque')
    c.waitfor(text='Controle de peças e materiais', timeout=20)
    c.mark(2)
    c.click(MENU_LATERAL, at=c.L(2) + 0.5, label='recolhe o menu lateral (a tela ganha espaço)')
    t0 = c.L(2) + 2.4
    for i, aba in enumerate([ABA_ATUAL, ABA_KARDEX, ABA_COMPRAS, ABA_INVENT, ABA_POSICAO, ABA_RELAT]):
        c.hover(aba, 0.2, at=t0 + i * 1.45, label=f'aba {aba["name"]}')
    c.mark(3)
    t = c.L(3) + 0.8
    c.hover(P('Controle de peças e materiais'), round(max(2.0, c.dur - t - 1.4), 1), at=t, label='o título da tela de Estoque')
    c.fim()
    return c


def cap01():
    c = Cap(1, pace=0.5, start=(760, 420), prewarm=['/estoque'], setup=SETUP_ESTOQUE)
    c.mark(1)
    abas = [('Estoque', 0, ABA_ATUAL), ('Histórico', 0, ABA_KARDEX), ('Compras', 0, ABA_COMPRAS), ('Inventários,', 0, ABA_INVENT),
            ('Posição', 0, ABA_POSICAO), ('Relatório.', 0, ABA_RELAT)]
    for palavra, nth, aba in abas:
        c.hover(aba, 0.15, at=c.A(1, palavra, 0.85, nth), label=f'aba {aba["name"]}')
    c.hover(BTN_IMPORTAR, 0.3, at=c.A(1, 'Importar', 0.9), label='o botão Importar XML da NF-e')
    c.hover(BTN_CONFIG, 0.3, at=c.A(1, 'Configurações,', 0.9), label='o botão Configurações')
    c.mark(2)
    c.hover(CARTAO('Total de itens'), 0.3, at=c.A(2, 'total', 0.9), label='cartão Total de itens')
    c.hover(CARTAO('Valor investido (R$)'), 0.3, at=c.A(2, 'valor', 0.9), label='cartão Valor investido')
    c.hover(CARTAO('Estoque baixo'), 0.5, at=c.A(2, 'quantos', 0.9), label='cartão Estoque baixo')
    c.click(LOCAL_ABA('Estoque Principal'), at=c.L(3) - 1.5, label='escolhe o local Estoque Principal (mínimo e custo por local)')
    c.mark(3)
    c.click(BUSCA, at=c.A(3, 'buscar', 0.9), label='clica na busca')
    c.type(BUSCA, 'fita', at=c.A(3, 'buscar', 0.1), cps=8, noClick=True, label='digita "fita" na busca')
    c.type(BUSCA, '', at=c.A(3, 'código', 0.2), clear=True, noClick=True, label='limpa a busca')
    c.click(FILTROS, at=c.A(3, 'Filtros,', 0.5), label='abre Filtros')
    c.hover(TXT('Estoque abaixo do mínimo', within=DLG), 0.5, at=c.A(3, 'abaixo', 0.8), label='a caixa "Estoque abaixo do mínimo"')
    c.hover(TXT('Grupo', within=DLG), 0.5, at=c.A(3, 'grupo.', 0.8), label='a lista de grupos')
    c.press('Escape', at=c.A(3, 'grupo.', -0.5), label='fecha Filtros')
    c.mark(4)
    for palavra, rot in [('nome,', 'Nome'), ('código,', 'SKU'), ('grupo,', 'Categoria'), ('quantidade,', 'Quantidade'),
                         ('mínima', 'Qtd. mínima'), ('custo', 'Custo Unit.')]:
        c.hover(SEL('main thead th', hasText=rot), 0.15, at=c.A(4, palavra, 0.7), label=f'coluna {rot}')
    c.ev(ROLAR(260), at=c.A(4, 'Repara', 1.6), label='rola a lista para ver as duas linhas em falta')
    c.hover(TRIANGULO('Gás refrigerante R-410A'), 0.5, at=c.A(4, 'Repara', 0.8), label='o triângulo do R-410A')
    c.hover(TRIANGULO('Tubo de cobre 3/8'), 0.5, at=c.A(4, 'duas,', 0.8), label='o triângulo do Tubo de cobre 3/8"')
    c.hover(TRIANGULO('Gás refrigerante R-410A'), 3.0, at=c.A(4, 'gás', 0.9), label='dica do triângulo: 8,5 de 10')
    c.ev(ROLAR(0), at=c.L(5) - 0.3, label='volta ao topo da lista')
    c.mark(5)
    c.click(EXPORTAR, at=c.A(5, 'Exportar', 0.9), label='abre Exportar')
    c.click(ITEM('PDF'), at=c.A(5, 'PDF', 0.8), label='escolhe PDF')
    c.waitfor(text='Selecionar materiais', timeout=10)
    c.hover(SEL(f'{DLG} thead, {DLG} [role=checkbox]'), 1.0, at=c.A(5, 'planilha', 0.8), label='a janela Selecionar materiais')
    c.press('Escape', at=c.A(5, 'escolher.', 0.5), label='fecha a janela (sem gerar arquivo)')
    c.fim()
    return c


def cap02():
    c = Cap(2, pace=0.4, cps=11, start=(760, 420), prewarm=['/estoque'], setup=SETUP_LOCAL)
    NOME = {'placeholder': 'Nome do item', 'exact': True, 'within': DLG}
    SKU = {'placeholder': 'Ex: FLT-001', 'within': DLG}
    c.mark(1)
    c.click(CADASTRAR, at=c.A(1, 'Cadastrar', 0.9, 1), label='clica em Cadastrar Material')
    c.waitfor(text='Novo Item de Estoque', timeout=10)
    c.type(NOME, f'Capacitor 40 {MICRO}F', at=c.A(1, 'Capacitor', 0.9), cps=9, label='digita o nome: Capacitor 40 µF')
    c.mark(2)
    c.hover(SKU, 0.8, at=c.A(2, 'código', 0.2), label='o código EST-010, já preenchido')
    c.hover(BTN('Auto', within=DLG), 0.6, at=c.A(2, 'sequência.', 0.8), label='o botão Auto')
    c.hover(P('Código sequencial sugerido automaticamente', within=DLG), 2.0, at=c.A(2, 'dica:', 0.8), label='a dica do código', optional=True)
    c.mark(3)
    c.click(CAMPO_ROT('Grupo', 'button'), at=c.A(3, 'Grupo,', 0.9), label='abre o campo Grupo')
    c.click(OPCAO('Elétrica'), at=c.A(3, 'Elétrica.', 0.8), label='escolhe Elétrica')
    c.click(SEL(f'{DLG} #inventory-supplier'), at=c.A(3, 'Fornecedor', 0.9), label='abre o campo Fornecedor')
    c.click(OPCAO('Polar Distribuidora de Peças Ltda'), at=c.A(3, 'Polar', 0.8), label='escolhe a Polar Distribuidora de Peças')
    c.mark(4)
    c.type(CAMPO_ROT('Quantidade'), '6', at=c.A(4, 'quantidade', 0.1), label='quantidade inicial: 6')
    c.hover(CAMPO_ROT('Unidade', 'button'), 0.6, at=c.A(4, 'unidade.', 0.8), label='a unidade: Unidade (un)')
    c.type(CAMPO_ROT('Preço de Custo (R$)'), '38,90', at=c.A(4, 'trinta', 1.2), label='preço de custo: 38,90')
    c.type(CAMPO_ROT('Preço de Venda (R$)'), '70,00', at=c.A(4, 'setenta', 1.2), label='preço de venda: 70,00')
    c.mark(5)
    MIN = SEL(f'{DLG} input[placeholder="Mín."]')
    c.scroll(P('Locais deste material', within=DLG), at=c.A(5, 'Locais', 1.1), label='desce até Locais deste material', duration=0.8)
    c.hover(SEL(f'{DLG} label:text-is("Estoque Principal")'), 0.6, at=c.A(5, 'Estoque', 0.9), label='o Estoque Principal (já marcado)')
    c.type(MIN, '4', at=c.A(5, 'mínimo', 1.0), label='mínimo: 4')
    c.mark(6)
    c.scroll(P('Foto do item', within=DLG), at=c.A(6, 'foto,', 0.5), label='volta à foto do item', duration=0.8)
    c.hover(P('Código de barras', within=DLG), 0.5, at=c.A(6, 'código', 0.9), label='o código de barras')
    c.hover(P('Vendável na loja', within=DLG), 1.2, at=c.A(6, 'Vendável', 0.9), label='a chave Vendável na loja')
    c.mark(7)
    c.clicar_fixo(f'{DLG} button', (800, 768), at=c.A(7, 'Salvo,', 0.5), label='Salvar', texto='Salvar')
    c.refocar(at=c.A(7, 'capacitor', 0.9))
    c.hover(SEL(LINHA('Capacitor 40')), 3.0, at=c.A(7, 'capacitor', 0.5), label='a linha Capacitor 40 µF na lista', timeout=8)
    c.fim()
    return c


def cap03():
    c = Cap(3, pace=0.4, cps=11, start=(760, 420), prewarm=['/estoque'], setup=SETUP_LOCAL)
    QTD = {'placeholder': 'Qtd.', 'exact': True, 'within': DLG}
    c.mark(1)
    menu_linha(c, 'Fita isolante', 'Registrar entrada', c.A(1, 'menu', 0.9), c.A(1, 'Registrar', 0.9), 'Fita isolante')
    c.waitfor(text='Saldo atual', timeout=10)
    c.type(QTD, '10', at=c.A(1, 'dez', 1.2), label='quantidade: 10')
    c.type(CAMPO_ROT('Observação', 'textarea'), 'Compra no balcão', at=c.A(1, 'Observação,', 1.1), cps=12, label='observação: Compra no balcão')
    c.hover(P('Saldo após', within=DLG), 2.0, at=c.A(1, 'Saldo', 0.6), label='o Saldo após: 38')
    c.click(BTN('Confirmar', within=DLG), at=c.A(1, 'Confirmo.', 0.9), label='Confirmar a entrada')
    c.mark(2)
    menu_linha(c, 'Capacitor 40', 'Registrar saída', c.A(2, 'capacitor,', 0.9), c.A(2, 'Registrar', 0.9), 'Capacitor 40 µF')
    c.waitfor(text='Saldo atual', timeout=10)
    c.type(QTD, '3', at=c.A(2, 'três.', 1.3), label='quantidade: 3')
    c.hover(P('Saldo após', within=DLG), 2.0, at=c.A(2, 'Saldo', 0.8), label='o Saldo após: 3')
    c.click(BTN('Confirmar', within=DLG), at=c.A(2, 'saldo.', 1.2, 1), label='Confirmar a saída')
    c.mark(3)
    c.hover(TRIANGULO('Capacitor 40'), 1.5, at=c.A(3, 'abaixo', 0.9), label='o triângulo do Capacitor 40 µF: 3 de 4')
    c.hover(CARTAO('Estoque baixo'), 1.5, at=c.A(3, 'cartão', 0.9), label='o cartão Estoque baixo: de 2 para 3')
    c.mark(4)
    BAIXO = TXT('Estoque abaixo do mínimo', within=DLG)
    c.click(FILTROS, at=c.A(4, 'Filtros,', 0.9), label='abre Filtros')
    c.click(BAIXO, at=c.A(4, 'Estoque', 0.9), label='marca "Estoque abaixo do mínimo"')
    c.click(BAIXO, at=c.A(4, 'Esse', 0.6), label='desmarca "Estoque abaixo do mínimo"')
    c.press('Escape', at=c.A(4, 'daqui', 0.2), label='fecha Filtros')
    c.mark(5)
    gat = GATILHO('Mangueira de dreno')
    c.hover(gat, 0.3, at=c.L(5) + 0.1, label='menu da linha Mangueira de dreno')
    c.click(gat, unless=ITEM('Excluir'), label='abre o menu se ainda não abriu')
    c.hover(ITEM('Editar'), 0.2, at=c.A(5, 'existe', 0.0), label='menu: Editar')
    c.hover(ITEM('Registrar entrada'), 0.2, label='menu: Registrar entrada')
    c.hover(ITEM('Registrar saída'), 0.2, label='menu: Registrar saída')
    c.hover(ITEM('Excluir'), 5.0, at=c.A(5, 'Para', 0.0), label='menu: Excluir (sem clicar)')
    c.press('Escape', at=c.A(5, 'apagado.', 0.0), label='fecha o menu')
    c.fim()
    return c


def cap04():
    c = Cap(4, pace=0.4, cps=11, start=(760, 420), prewarm=['/estoque'], setup=SETUP_ESTOQUE)
    NOVO = {'placeholder': 'Nome do local...', 'exact': True, 'within': DLG}
    c.mark(1)
    c.click(BTN_CONFIG, at=c.A(1, 'Configurações,', 0.9), label='abre Configurações')
    c.waitfor(text='Configurações do Estoque', timeout=10)
    for palavra, nome in [('Gases,', 'Gases'), ('Cobre', 'Cobre e tubos'), ('Elétrica', 'Elétrica'), ('Consumíveis.', 'Consumíveis')]:
        c.hover(TXT(nome, within=DLG), 0.25, at=c.A(1, palavra, 0.8), label=f'grupo {nome}')
    c.mark(2)
    c.click(BTN('Locais de estoque', within=DLG), at=c.A(2, 'Locais', 0.9), label='aba Locais de estoque')
    c.hover(TXT('Estoque Principal', within=DLG), 0.8, at=c.A(2, 'Estoque', 0.9), label='o Estoque Principal, local padrão')
    c.type(NOVO, 'Van 01', at=c.A(2, 'digito', 1.0), label='digita Van 01')
    c.click(SEL(f'{DLG} div.flex.gap-2:has(input[placeholder="Nome do local..."]) button'), at=c.A(2, 'clico', 0.9), label='botão de mais: cria o local')
    c.waitfor(text='Van 01', timeout=10)
    c.mark(3)
    c.click(BTN('Fechar', within=DLG), at=c.A(3, 'Fechando', 0.9), label='fecha Configurações')
    c.hover(LOCAL_ABA('Estoque Principal'), 0.4, at=c.A(3, 'principal', 0.9), label='a aba Estoque Principal, com a estrela')
    c.hover(LOCAL_ABA('Van 01'), 0.4, at=c.A(3, 'estrela.', 0.9), label='a aba Van 01')
    c.mark(4)
    c.click(ENGRENAGEM('Van 01'), at=c.A(4, 'Na', 0.9), label='engrenagem da aba Van 01')
    c.waitfor(text='Configurar Van 01', timeout=10)
    c.click(BTN('Desmarcar todos', within=DLG), at=c.A(4, 'Adicionar', 1.2), label='desmarca todos (a Van começa com tudo marcado)')
    c.click(SEL(f'{DLG} button[role=combobox]'), at=c.A(4, 'escolho', 1.1), label='abre Adicionar por grupo')
    c.click(OPCAO('Gases'), at=c.A(4, 'Gases,', 0.65), label='escolhe Gases')
    c.click(BTN('Adicionar grupo', within=DLG), at=c.A(4, 'gases', 0.6, 1), label='Adicionar grupo')
    c.click(SEL(f'{DLG} label:has-text("Fita isolante")'), at=c.A(4, 'Fita', 1.0), label='marca a Fita isolante')
    c.clicar_fixo(f'{DLG} button', (800, 700), at=c.A(4, 'salvo.', 0.7), label='Salvar', texto='Salvar')
    c.mark(5)
    c.click(LOCAL_ABA('Van 01'), at=c.A(5, 'Uma', 0.0), label='abre a aba Van 01')
    c.hover(SEL(LINHA('Fita isolante')), 4.0, at=c.A(5, 'tirar', 0.6), label='os três materiais da Van 01')
    c.fim()
    return c


def cap05():
    c = Cap(5, pace=0.4, cps=11, start=(760, 420), prewarm=['/estoque'], setup=SETUP_ESTOQUE)
    c.mark(1)
    c.click(LOCAL_ABA('Estoque Principal'), at=c.A(1, 'Estoque', 0.9), label='aba Estoque Principal')
    menu_linha(c, 'Gás refrigerante R-410A', 'Transferir', c.A(1, 'menu', 0.9), c.A(1, 'Transferir.', 0.9), 'R-410A')
    c.waitfor(text='Transferir entre locais de estoque', timeout=10)
    c.mark(2)
    c.hover(P('Disponível', within=DLG), 1.2, at=c.A(2, 'disponíveis.', 1.6), label='origem: Estoque Principal, 8,5 disponíveis', optional=True)
    c.select(CAMPO_ROT('Local de destino', 'button[role=combobox]'), 'Van 01', at=c.A(2, 'Escolho', 0.9), label='destino: Van 01')
    c.type(CAMPO_ROT('Quantidade'), '2', at=c.A(2, 'digito', 1.0), label='quantidade: 2')
    c.type(CAMPO_ROT('Observações', 'textarea'), 'Carga da van do Rafael', at=c.A(2, 'anoto:', 1.1), cps=12, label='observação: Carga da van do Rafael')
    c.mark(3)
    c.click(BTN('Transferir', within=DLG), at=c.A(3, 'Clico', 0.9), label='Transferir')
    c.click(LOCAL_ABA('Van 01'), at=c.A(3, 'Clico', 0.9, 1), label='o local Van 01 na lista')
    c.hover(SEL(LINHA('Gás refrigerante R-410A')), 1.2, at=c.A(3, 'aparece', 0.9), label='R-410A com 2 kg na Van 01')
    c.click(LOCAL_ABA('Estoque Principal'), at=c.A(3, 'Estoque', 0.9), label='o local Estoque Principal na lista')
    c.hover(SEL(LINHA('Gás refrigerante R-410A')), 3.0, at=c.A(3, 'sobram', 0.9), label='R-410A com 6,5 no Estoque Principal')
    c.fim()
    return c


def cap06():
    c = Cap(6, pace=0.4, cps=11, start=(760, 420), prewarm=['/estoque'], setup=SETUP_ESTOQUE)
    CHAVE = {'role': 'switch', 'name': 'Restringir acesso a este local'}
    c.mark(1)
    c.click(ENGRENAGEM('Van 01'), at=c.A(1, 'engrenagem', 0.9), label='engrenagem da aba Van 01')
    c.waitfor(text='Configurar Van 01', timeout=10)
    c.click(TAB('Acesso', within=DLG), at=c.A(1, 'abro', 0.9), label='aba Acesso')
    c.hover(P('Todos os usuários da empresa veem este local', within=DLG), 2.0, at=c.A(1, 'padrão,', 0.9), label='por padrão, todos veem o local')
    c.mark(2)
    c.click(CHAVE, at=c.A(2, 'Restringir', 0.9), label='liga "Restringir acesso a este local"')
    c.hover(P('Apenas os usuários marcados veem e movimentam este local', within=DLG), 1.0, at=c.A(2, 'aparece', 0.9), label='o texto novo e a lista de pessoas')
    c.hover(SEL(LINHA_USUARIO('Camila Duarte')), 2.0, at=c.A(2, 'Camila,', 0.9), label='Camila Duarte: Sempre tem acesso')
    c.mark(3)
    c.click(SEL(LINHA_USUARIO('Rafael Lima') + ' button[role=switch]'), at=c.A(3, 'Marco', 0.9), label='liga o acesso do Rafael Lima')
    c.click(BTN('Salvar acesso', within=DLG), at=c.A(3, 'Salvar', 0.9), label='Salvar acesso')
    c.mark(4)
    c.click(ENGRENAGEM('Van 01'), at=c.L(4) - 0.6, label='reabre a engrenagem da Van 01')
    c.waitfor(text='Configurar Van 01', timeout=10)
    c.click(TAB('Acesso', within=DLG), at=c.L(4) + 1.0, label='aba Acesso, já restrita')
    c.hover(SEL(LINHA_USUARIO('Rafael Lima')), 1.2, at=c.A(4, 'ninguém', 0.0), label='a lista com o Rafael Lima marcado')
    c.fim()
    return c


def cap07():
    c = Cap(7, pace=0.4, cps=11, start=(760, 420), prewarm=['/estoque'], setup=SETUP_ESTOQUE)
    c.mark(1)
    c.click(ABA_KARDEX, at=c.A(1, 'Kardex,', 0.9), label='aba Histórico de Materiais (Kardex)')
    c.waitfor(text='Kardex geral', timeout=15)
    c.hover(P('Geral (Todos)'), 1.0, at=c.A(1, 'esquerda', 0.9), label='a coluna Materiais, com "Geral (Todos)"')
    c.hover(P('Kardex geral'), 1.5, at=c.A(1, 'direita', 0.9), label='o Kardex geral')
    c.mark(2)
    for palavra, rot in [('quando', 'Data e Hora'), ('tipo', 'Tipo'), ('material', 'Material e origem'), ('local,', 'Local'),
                         ('alteração', 'Alteração')]:
        c.hover(SEL('main thead th', hasText=rot), 0.15, at=c.A(2, palavra, 0.8), label=f'coluna {rot}')
    c.hover(SEL('main thead th', hasText='Saldo final'), 0.15, at=c.A(2, 'depois.', 1.0), label='coluna Saldo final')
    LIN = lambda *textos: SEL('main tbody tr' + ''.join(f':has-text("{t}")' for t in textos))
    c.hover(LIN('Fita isolante', 'Compra no balcão'), 0.3, at=c.A(2, 'entrada', 0.9), label='a entrada da Fita isolante')
    c.hover(LIN('Capacitor 40', 'Cadastro inicial'), 0.3, at=c.A(2, 'capacitor', 0.9), label='o cadastro inicial do Capacitor 40 µF')
    c.hover(LIN('Capacitor 40', 'Saída'), 0.3, at=c.A(2, 'saída', 0.9), label='a saída do Capacitor 40 µF')
    c.hover(LIN('Transferência'), 2.0, at=c.A(2, 'transferência', 0.9), label='a transferência: Estoque Principal → Van 01')
    c.mark(3)
    c.hover(SEL('main tbody tr:has-text("OS #16")', nth=0), 0.6, at=c.A(3, 'Estas', 0.0), label='a primeira linha de Consumo (OS #16)')
    c.hover(P('OS #16'), 2.0, at=c.A(3, 'dezesseis,', 0.2), label='a origem OS #16')
    c.mark(4)
    # 1.38.19: o período saiu da janela Filtros e virou o seletor "Este mês" no topo do Kardex
    c.hover(SEL('main [aria-label="Período"]'), 0.6, at=c.L(4) + 0.1, label='o seletor de período: Este mês')
    c.click(FILTROS, at=c.A(4, 'mês', 0.5), label='abre Filtros do Kardex')
    c.hover(TXT('Tipo de movimento', within=DLG), 0.3, at=c.A(4, 'tipo', 0.4), label='Tipo de movimento')
    c.hover(TXT('Local', within=DLG), 0.3, at=c.A(4, 'local.', 0.5), label='Local')
    c.click(TXT('Consumo', within=DLG), at=c.A(4, 'Consumo,', 0.9), label='filtra por Consumo')
    c.press('Escape', at=c.A(4, 'linhas.', 0.5), label='fecha Filtros')
    # o filtro Consumo continua ligado e esconderia o histórico do material: tira antes de escolher o material
    # o botão Filtros é uma faixa que se abre ao passar o mouse (o ponteiro não estabiliza: 4 s): abre por eval, sem o cursor
    JS_FILTROS = 'document.querySelector("main button[aria-label^=\\"Filtros\\"]").click()'
    c.pause(0.6)   # a janela de Filtros acabou de fechar: um clique logo em seguida no gatilho é ignorado
    c.ev(JS_FILTROS, at=c.L(5) - 0.6, label='abre Filtros de novo')
    c.mark(5)
    c.click(TXT('Consumo', within=DLG), at=c.L(5) + 0.5, label='tira o filtro Consumo')
    c.press('Escape', at=c.L(5) + 1.3, label='fecha Filtros')
    MAT = 'main button:has-text("Gás refrigerante R-410A")'
    c.ev('[...document.querySelectorAll("main button")].find(b=>/Gás refrigerante R-410A/.test(b.textContent)).scrollIntoView({block:"center",behavior:"smooth"})',
         at=c.L(5) + 1.5, label='rola a lista de materiais até o Gás')
    c.click(SEL(MAT), at=c.A(5, 'Gás', 0.0), label='escolhe o Gás refrigerante R-410A na coluna Materiais')
    c.hover(SEL('main h2', hasText='Gás refrigerante R-410A'), 2.0, at=c.A(5, 'histórico', 0.9), label='Histórico deste material')
    c.fim()
    return c


def cap08():
    c = Cap(8, pace=0.4, cps=12, start=(760, 420), prewarm=['/estoque'], setup=SETUP_ESTOQUE)
    c.mark(1)
    c.click(ABA_COMPRAS, at=c.A(1, 'Compras', 0.9, 1), label='aba Compras de Material')
    c.waitfor(text='Requisições de Compra', timeout=15)
    c.hover(P('materiais abaixo do mínimo'), 2.0, at=c.A(1, 'faixa', 0.9), label='a faixa vermelha: 3 materiais abaixo do mínimo')
    c.mark(2)
    c.hover(BTN('Fornecedores', within='main'), 0.5, at=c.A(2, 'Fornecedores', 0.9), label='o botão Fornecedores')
    # 1.38.19: "Nova requisição de compra" e "Registrar compra direta" viraram itens do menu "Nova compra"
    c.click(BTN('Nova compra', within='main'), at=c.A(2, 'Nova', 0.9), label='abre o menu Nova compra')
    c.hover(ITEM('Criar requisição'), 0.4, at=c.A(2, 'Criar', 0.9), label='menu: Criar requisição')
    c.hover(ITEM('Registrar compra direta'), 2.5, at=c.A(2, 'Registrar', 0.9), label='menu: Registrar compra direta (sem clicar)')
    c.press('Escape', at=c.A(2, 'Esse', 0.3), label='fecha o menu')
    c.pause(0.5)   # com o menu aberto o resto da tela fica oculto para o robô
    c.mark(3)
    c.click(TXT('Criar requisição', within='main'), at=c.A(3, 'Criar', 0.9), label='Criar requisição')
    c.waitfor(text='Nova Requisição de Compra', timeout=10)
    c.type({'placeholder': 'Ex.: Reposição de materiais, Junho', 'within': DLG}, 'Reposição de gás, cobre e capacitor', at=c.A(3, 'título:', 1.1), cps=14,
           label='título: Reposição de gás, cobre e capacitor', optional=False)
    c.hover(P('Os materiais recebidos entram neste local de estoque', within=DLG), 2.5, at=c.A(3, 'destino', 0.9), label='Local de destino: Estoque Principal')
    c.mark(4)
    c.click(BTN('Adicionar itens abaixo do mínimo', within=DLG), at=c.A(4, 'Adicionar', 0.9), label='Adicionar itens abaixo do mínimo')
    c.waitfor(text='Itens abaixo do mínimo', timeout=10)
    c.select(SEL(f'{ALERTA} button[role=combobox]'), 'Estoque Principal', at=c.A(4, 'Escolho', 0.9), label='escolhe o local: Estoque Principal')
    c.hover(P('Deficit', within=ALERTA), 2.0, at=c.A(4, 'déficit', 0.9), label='o déficit de cada material', optional=True)
    c.click(BTN('Adicionar à requisição', within=ALERTA), at=c.A(4, 'Adiciono', 0.9), label='Adicionar à requisição')
    c.mark(5)
    QTD = lambda mat: SEL(f'{DLG} div.rounded-lg.border:has-text("{mat}") input')
    c.type(QTD('Gás refrigerante R-410A'), '10', at=c.A(5, 'dez', 1.3), label='R-410A: 10')
    c.type(QTD('Tubo de cobre 3/8'), '20', at=c.A(5, 'vinte', 1.3), label='Tubo de cobre 3/8": 20')
    c.type(QTD('Capacitor 40'), '6', at=c.A(5, 'seis', 1.3), label='Capacitor 40 µF: 6')
    c.mark(6)
    c.click(BTN('Salvar', within=DLG), at=c.A(6, 'Salvo,', 0.9), label='Salvar a requisição')
    c.hover(CARTAO_REQ, 1.5, at=c.A(6, 'criada.', 0.9), label='o cartão da requisição criada', timeout=8)
    c.fim()
    return c


def cap09():
    c = Cap(9, pace=0.25, cps=14, start=(760, 420), prewarm=['/estoque'], setup=SETUP_COMPRAS)
    PRECOS = {  # fornecedor -> (R-410A, Tubo de cobre 3/8", Capacitor 40 µF)
        'Ventura Gás e Tubos': ('94,00', '29,50', '39,00'),
        'Cobre Sul Suprimentos Ltda': ('98,00', '27,00', '38,00'),
        'Polar Distribuidora de Peças Ltda': ('99,00', '31,00', '36,00'),
    }
    MATS = ['Gás refrigerante R-410A', 'Tubo de cobre 3/8', 'Capacitor 40']
    NOVA = BTN('Nova cotação', within='main')
    SALVAR = BTN('Salvar cotação', within=DLG)
    c.mark(1)
    c.click(CARTAO_REQ, at=c.A(1, 'Clico', 0.9), label='abre a requisição')
    c.waitfor(text='Nova cotação', timeout=15)
    for palavra, h in [('Materiais:', 'Materiais'), ('Cotações', 'Cotações'), ('Ordens', 'Ordens de compra')]:
        c.hover(SEL('main h2', hasText=h), 0.2, at=c.A(1, palavra, 0.8), label=f'bloco {h}')
    c.mark(2)
    c.click(NOVA, at=c.A(2, 'Nova', 0.9), label='Nova cotação')
    c.waitfor(text='Fornecedor', timeout=10)
    c.click(SEL(f'{DLG} button[role=combobox]'), at=c.A(2, 'escolho', 0.9), label='abre o campo Fornecedor')
    c.click(OPCAO('Ventura Gás e Tubos'), at=c.A(2, 'Ventura', 0.8), label='escolhe a Ventura Gás e Tubos')
    for (mat, valor, palavra) in [(MATS[0], PRECOS['Ventura Gás e Tubos'][0], 'noventa'), (MATS[1], PRECOS['Ventura Gás e Tubos'][1], 'vinte'),
                                  (MATS[2], PRECOS['Ventura Gás e Tubos'][2], 'trinta')]:
        c.type(PRECO_UNIT(mat), valor, at=c.A(2, palavra, 1.2), label=f'valor unitário de {mat}: {valor}')
    c.hover(P('Total geral', within=DLG), 1.5, at=c.A(2, 'total.', 1.4), label='Total geral')
    c.mark(3)
    c.click(SALVAR, at=c.A(3, 'Salvo,', 0.9), label='Salvar cotação (Ventura)')
    for k, forn in enumerate(['Cobre Sul Suprimentos Ltda', 'Polar Distribuidora de Peças Ltda']):
        # o 1º passo da cadeia leva `at` (depois do início da linha 3): sem isso a marca L3 sai depois de toda a cadeia
        c.click(NOVA, at=(c.L(3) + 0.6) if k == 0 else None, label=f'Nova cotação ({forn})')
        c.waitfor(text='Fornecedor', timeout=10)
        c.click(SEL(f'{DLG} button[role=combobox]'), label=f'abre o campo Fornecedor ({forn})')
        c.click(OPCAO(forn), label=f'escolhe {forn}')
        for mat, valor in zip(MATS, PRECOS[forn]):
            c.type(PRECO_UNIT(mat), valor, cps=24, label=f'{forn}: {mat} {valor}')
        c.click(SALVAR, label=f'Salvar cotação ({forn})')
    c.mark(4)
    c.hover(SEL('main div.rounded-lg.border:has-text("3/3")', nth=0), 0.4, at=c.A(4, 'cartão', 0.9), label='o cartão de uma cotação: 3/3 materiais com preço', optional=True)
    c.hover(P('Mais barata'), 2.5, at=c.A(4, 'barata', 0.9), label='o selo Mais barata', optional=True)
    c.mark(5)
    ESCOLHA = lambda mat: SEL(f'{LINHA_MATERIAL(mat)} button[role=combobox]')
    c.select(ESCOLHA(MATS[0]), 'Ventura Gás e Tubos', at=c.A(5, 'gás', 1.2), label='fornecedor escolhido do R-410A: Ventura')
    c.select(ESCOLHA(MATS[1]), 'Cobre Sul Suprimentos Ltda', at=c.A(5, 'tubo', 1.2), label='fornecedor escolhido do Tubo: Cobre Sul')
    c.select(ESCOLHA(MATS[2]), 'Polar Distribuidora de Peças Ltda', at=c.A(5, 'capacitor', 1.2), label='fornecedor escolhido do Capacitor: Polar')
    c.mark(6)
    c.hover(SEL('main h2', hasText='Materiais'), 3.0, at=c.A(6, 'Uma', -0.1), label='os três materiais com fornecedor escolhido')
    c.fim()
    return c


def cap10():
    c = Cap(10, pace=0.4, cps=12, start=(760, 420), prewarm=['/estoque'], setup=SETUP_REQUISICAO)
    def menu_ordem(forn, item, t_menu, t_item, rot):
        gat = GAT_ORDEM(forn)
        c.hover(gat, 0.3, at=t_menu, label=f'menu da ordem {rot}')
        c.click(gat, unless=ITEM(item), label=f'abre o menu da ordem {rot} se ainda não abriu')
        return c.click(ITEM(item), at=t_item, label=f'{item} ({rot})')
    c.mark(1)
    c.click(BTN('Gerar ordens de compra', within='main'), at=c.A(1, 'Gerar', 0.9), label='Gerar ordens de compra')
    c.waitfor(text='Rascunho', timeout=10)
    for i, forn in enumerate(['Ventura Gás e Tubos', 'Cobre Sul Suprimentos Ltda', 'Polar Distribuidora de Peças Ltda']):
        c.hover(SEL(CARD_ORDEM(forn)), 0.3, at=c.A(1, 'uma', 0.9) + i * 1.0, label=f'ordem da {forn}: Rascunho')
    c.mark(2)
    menu_ordem('Ventura', 'Marcar como enviada', c.A(2, 'ordem', 0.9), c.A(2, 'Marcar', 0.9), 'Ventura')
    gat = GAT_ORDEM('Ventura')
    c.hover(gat, 0.3, at=c.A(2, 'menu', 0.9), label='menu da ordem Ventura')
    c.click(gat, unless=ITEM('Baixar PDF'), label='abre o menu se ainda não abriu')
    c.hover(ITEM('Baixar PDF'), 3.0, at=c.A(2, 'Baixar', 0.9), label='Baixar PDF (sem clicar)')
    c.press('Escape', at=c.A(2, 'fornecedor.', 0.6), label='fecha o menu')
    c.mark(3)
    menu_ordem('Ventura', 'Registrar recebimento', c.A(3, 'gás.', 0.9), c.A(3, 'Registrar', 0.9), 'Ventura')
    c.waitfor(text='Informe só o que chegou agora', timeout=10)
    c.hover(P('Qtd. pendente', within=DLG), 2.5, at=c.A(3, 'vejo', 0.9), label='pedido, recebido e pendente')
    c.click(BTN('Receber tudo', within=DLG), at=c.A(3, 'Receber', 0.9), label='Receber tudo')
    c.click(BTN('Confirmar recebimento', within=DLG), at=c.A(3, 'confirmo.', 0.9), label='Confirmar recebimento (Ventura)')
    c.mark(4)
    menu_ordem('Cobre Sul', 'Marcar como enviada', c.L(4) - 0.3, c.L(4) + 0.4, 'Cobre Sul')
    menu_ordem('Cobre Sul', 'Registrar recebimento', c.L(4) + 1.6, c.L(4) + 2.2, 'Cobre Sul')
    c.waitfor(text='Informe só o que chegou agora', timeout=10)
    c.type(SEL(f'{DLG} div.rounded-lg.border:has-text("Tubo de cobre 3/8") input'), '10', at=c.A(4, 'vinte.', 0.4), label='tubo: 10 dos 20 pedidos')
    c.hover(P('Qtd. pendente', within=DLG), 1.5, at=c.A(4, 'resto', 0.9), label='o resto continua pendente')
    c.click(BTN('Confirmar recebimento', within=DLG), at=c.A(4, 'fica', 0.9), label='Confirmar recebimento (Cobre Sul)')
    c.mark(5)
    c.hover(SEL(CARD_ORDEM('Polar')), 1.6, at=c.A(5, 'Polar', 0.9), label='a ordem da Polar: Rascunho')
    c.mark(6)
    c.click(ABA_ATUAL, at=c.L(6) + 0.05, label='volta ao Estoque Atual')
    c.hover(SEL(LINHA('Gás refrigerante R-410A')), 0.8, at=c.A(6, 'subiu', 0.0), label='R-410A com 16,5')
    c.hover(SEL(LINHA('Tubo de cobre 3/8')), 0.8, at=c.A(6, 'tubo', 0.6), label='Tubo de cobre 3/8" com 22')
    c.hover(CARTAO('Estoque baixo'), 1.0, at=c.A(6, 'cartão', -0.5), label='o cartão Estoque baixo cai para 1')
    c.fim()
    return c


def cap11():
    c = Cap(11, pace=0.4, cps=12, start=(760, 420), prewarm=['/estoque'], setup=SETUP_ESTOQUE)
    c.mark(1)
    c.click(BTN_IMPORTAR, at=c.A(1, 'Importar', 0.9), label='Importar XML da NF-e')
    c.waitfor(text='Selecione o arquivo .xml da nota fiscal eletrônica', timeout=10)
    c.upload(BTN('Escolher arquivo XML', within=DLG), 'assets/nfe-gelo-norte.xml', at=c.A(1, 'escolho', 1.0), label='escolhe o arquivo XML da nota')
    c.waitfor(text='Gelo Norte Componentes', timeout=15)
    c.mark(2)
    c.hover(P('Gelo Norte Componentes', within=DLG), 1.0, at=c.A(2, 'fornecedor,', 0.9), label='o fornecedor: Gelo Norte Componentes')
    c.hover(P('Vinculado', within=DLG), 1.0, at=c.A(2, 'selo', 0.9), label='o selo Vinculado')
    c.hover(P('91.345.602/0001-36', within=DLG), 1.5, at=c.A(2, 'CNPJ', 0.9), label='o CNPJ da nota')
    c.mark(3)
    c.hover(P('Produtos da nota', within=DLG), 0.6, at=c.A(3, 'Produtos', 0.9), label='Produtos da nota')
    c.hover(SEL(f'{DLG} input[aria-label]', nth=0), 0.3, at=c.A(3, 'nome,', 0.9), label='o nome do primeiro produto')
    c.hover(P('Qtd', within=DLG), 0.3, at=c.A(3, 'quantidade,', 0.9), label='a quantidade')
    c.hover(P('Unidade', within=DLG), 0.3, at=c.A(3, 'unidade', 0.9), label='a unidade')
    c.hover(P('Custo un.', within=DLG), 0.3, at=c.A(3, 'custo.', 0.9), label='o custo unitário')
    c.hover(P('Destino no estoque', within=DLG), 0.6, at=c.A(3, 'Destino', 0.9), label='Destino no estoque')
    c.hover(SEL(f'{DLG} button[role=combobox]', nth=0), 1.5, at=c.A(3, 'capacitor', 0.9), label='o capacitor ligado ao Capacitor 40 µF (EST-010)')
    c.hover(SEL(f'{DLG} button[role=combobox]', nth=1), 0.8, at=c.A(3, 'contator', 0.9), label='o contator: Criar novo item')
    c.hover(SEL(f'{DLG} button[role=combobox]', nth=2), 1.2, at=c.A(3, 'filtro', 0.9), label='o filtro secador: Criar novo item')
    c.mark(4)
    c.hover(P('3 itens', within=DLG), 0.8, at=c.A(4, 'Confirmo', 1.8), label='3 itens • R$ 731,00')
    c.click(BTN('Confirmar entrada', within=DLG), at=c.A(4, 'Confirmo', 0.9), label='Confirmar entrada')
    c.mark(5)
    c.refocar(at=c.L(5) + 0.1)
    c.hover(SEL(LINHA('Contator')), 1.2, at=c.A(5, 'cadastra', 0.9), label='o Contator 25 A na lista', timeout=8)
    c.hover(SEL(LINHA('Filtro secador')), 3.0, at=c.A(5, 'Para', 0.9), label='o Filtro secador na lista', timeout=8)
    c.fim()
    return c


def cap12():
    c = Cap(12, pace=0.4, cps=12, start=(760, 420), prewarm=['/estoque'], setup=SETUP_ESTOQUE)
    AVANCAR = BTN('Avançar', within=DLG)
    c.mark(1)
    c.click(ABA_INVENT, at=c.A(1, 'Inventários,', 0.9), label='aba Inventários')
    c.click(BTN('Novo inventário', within='main'), at=c.A(1, 'Novo', 0.9), label='Novo inventário')
    c.waitfor(text='Selecione os locais de estoque que serão contados', timeout=10)
    c.click(SEL(f'{DLG} label:has-text("Estoque Principal")'), at=c.A(1, 'Estoque', 0.9, 1), label='marca o Estoque Principal')
    c.click(AVANCAR, at=c.A(1, 'Principal.', 0.5), label='Avançar')
    c.mark(2)
    for palavra, rot in [('tudo,', 'Todos os materiais'), ('grupos', 'Por grupo'), ('itens', 'Itens específicos')]:
        c.hover(SEL(f'{DLG} button.rounded-xl', hasText=rot), 0.2, at=c.A(2, palavra, 0.9), label=f'escopo: {rot}', optional=True)
    c.click(SEL(f'{DLG} button.rounded-xl', hasText='Por grupo'), at=c.A(2, 'grupo:', 0.0), label='escolhe Por grupo de material')
    c.click(SEL(f'{DLG} label:has-text("Gases")'), at=c.A(2, 'Gases', 0.9), label='marca Gases')
    c.click(SEL(f'{DLG} label:has-text("Elétrica")'), at=c.A(2, 'Elétrica.', 0.9), label='marca Elétrica')
    c.click(AVANCAR, at=c.L(3) - 0.9, label='Avançar')
    c.mark(3)
    c.hover(P('Resumo do inventário', within=DLG), 1.0, at=c.A(3, 'resumo', 0.9), label='o resumo do inventário')
    c.type({'selector': f'{DLG} textarea'}, 'Contagem do mês', at=c.A(3, 'observação:', 1.0), cps=12, label='observação: Contagem do mês')
    c.click(BTN('Criar inventário', within=DLG), at=c.A(3, 'Clico', 0.9), label='Criar inventário')
    c.waitfor(text='Contagem do mês', timeout=15)   # 1.38.19: o inventário criado aparece na lista; a janela dele abre ao clicar na linha
    c.mark(4)
    c.click(SEL('main tbody tr:has-text("Contagem do mês")'), at=c.L(4), label='abre o inventário criado (clique na linha)')
    c.waitfor(text='Esperado', timeout=15)
    c.hover(SEL(f'{DLG} thead th', hasText='Esperado'), 1.2, at=c.A(4, 'esperado', 0.9), label='a coluna Esperado')
    c.hover(SEL(f'{DLG} thead th', hasText='Contado'), 1.8, at=c.A(4, 'Contado', 0.9), label='os campos Contado, vazios')
    c.mark(5)
    CONT = lambda mat: SEL(f'{DLG} tbody tr:has-text("{mat}") input')
    c.type(CONT('Gás refrigerante R-410A'), '16', at=c.A(5, 'dezesseis', 1.3), label='R-410A contado: 16')
    c.press('Tab', label='sai do campo (salva)')
    c.type(CONT('Gás refrigerante R-32'), '6', at=c.A(5, 'seis', 1.3), label='R-32 contado: 6')
    c.press('Tab', label='sai do campo (salva)')
    c.type(CONT('Capacitor 35'), '8', at=c.A(5, 'oito', 1.3), label='Capacitor 35 µF contado: 8')
    c.press('Tab', label='sai do campo (salva)')
    c.type(CONT('Capacitor 40'), '13', at=c.A(5, 'treze', 1.3), label='Capacitor 40 µF contado: 13')
    c.press('Tab', label='sai do campo (salva)')
    c.hover(P('Divergências encontradas', within=DLG), 0.6, at=c.A(5, 'Dois', 0.9, 1), label='a faixa: Divergências encontradas, 2 itens')
    c.mark(6)
    c.click(BTN('Divergências (2)', within=DLG), at=c.A(6, 'Divergências', 0.9), label='aba Divergências (2)')
    c.hover(SEL(f'{DLG} thead th', hasText='Valor divergência'), 0.8, at=c.A(6, 'valor', 0.9), label='o valor de cada divergência')
    c.mark(7)
    c.click(BTN('Finalizar inventário', within=DLG), at=c.A(7, 'Clico', 0.9), label='Finalizar inventário')
    c.waitfor(text='Finalizar inventário?', timeout=10)
    c.click(BTN('Finalizar', within=ALERTA), at=c.A(7, 'itens', 0.8), label='Finalizar')
    c.mark(8)
    # 1.38.19: ao finalizar, a janela do inventário fecha sozinha e a lista mostra o selo Finalizado
    c.hover(P('Finalizado', within='main'), 1.2, at=c.A(8, 'Finalizado,', 0.9), label='Inventário #1: Finalizado')
    c.hover(ABA_KARDEX, 0.4, at=c.A(8, 'Kardex.', 0.9), label='aba Histórico de Materiais (Kardex)')
    c.fim()
    return c


def cap13():
    c = Cap(13, pace=0.4, cps=12, start=(760, 420), prewarm=['/estoque'], setup=SETUP_INVENT)
    PICKER = SEL('main button[aria-haspopup="dialog"]', nth=0)
    POP = '[data-radix-popper-content-wrapper]'
    c.mark(1)
    c.click(ABA_POSICAO, at=c.A(1, 'Posição', 0.9), label='aba Posição de Estoque')
    c.waitfor(text='Valor em estoque', timeout=15)
    c.hover(P('Valor em estoque'), 0.4, at=c.A(1, 'valor', 0.9), label='o cartão Valor em estoque (custo)')
    c.hover(P('Projeção de venda'), 0.4, at=c.A(1, 'projeção', 0.9), label='o cartão Projeção de venda')
    c.hover(SEL('main tr:has-text("Total")', nth='last'), 0.2, at=c.A(1, 'total', 0.9), label='a linha Total')
    c.hover(PICKER, 0.4, at=c.A(1, 'padrão,', 0.9), label='o seletor de data e hora (agora)')
    c.mark(2)
    c.click(PICKER, at=c.A(2, 'calendário.', 0.9), label='abre o calendário')
    c.waitfor(text='Concluir', timeout=10)
    c.click(SEL(f'{POP} button[name="previous-month"]'), at=c.A(2, 'Escolho', 0.9), label='mês anterior (outubro)')
    c.click(SEL(f'{POP} button[name="day"]:text-is("3")'), at=c.A(2, 'mês', 0.9), label='escolhe o dia 3 de outubro')
    c.click(BTN('Concluir', within=POP), at=c.A(2, 'recalculam', 1.2), label='Concluir')
    c.hover(SEL(LINHA('R-410A')), 0.4, at=c.L(3) - 2.3, label='o R-410A com o saldo daquele dia')
    c.mark(3)
    BUSCA_POS = {'placeholder': 'Buscar material ou SKU...', 'exact': True}
    c.click(BUSCA_POS, at=c.A(3, 'busca', 0.9), label='clica na busca')
    c.type(BUSCA_POS, 'R-410A', at=c.A(3, 'busca', 0.1), cps=8, noClick=True, label='digita R-410A na busca')
    c.click(BTN('Exportar', within='main'), at=c.A(3, 'Exportar', 0.9), label='abre Exportar (PDF ou Excel)')
    c.hover(ITEM('PDF'), 2.0, at=c.A(3, 'PDF', 0.8), label='o menu Exportar: PDF e Excel (sem clicar)')
    c.press('Escape', at=c.A(3, 'dica:', 0.2), label='fecha o menu')
    c.hover(P('Valor (custo)'), 2.0, at=c.A(3, 'custo', 0.9, 1), label='a coluna Valor (custo)')
    c.fim()
    return c


def cap14():
    c = Cap(14, pace=0.4, cps=12, start=(760, 420), prewarm=['/estoque'], setup=SETUP_POSICAO)
    CARD = lambda nome: SEL(f'main button:has-text("{nome}")', nth=0)
    c.mark(1)
    c.click(ABA_RELAT, at=c.A(1, 'Relatório.', 0.9), label='aba Relatório')
    c.waitfor(text='Total comprado', timeout=15)
    c.hover(CARD('Total comprado'), 0.6, at=c.A(1, 'Total', 0.9), label='o cartão Total comprado')
    c.hover(P('Ticket médio por compra'), 1.5, at=c.A(1, 'ticket', 0.9), label='o ticket médio de cada compra')
    c.mark(2)
    c.hover(CARD('Total vendido'), 0.5, at=c.A(2, 'vendido', 0.9), label='o cartão Total vendido (PDV)')
    c.hover(CARD('Lucro bruto'), 0.5, at=c.A(2, 'bruto', 0.9), label='o cartão Lucro bruto (PDV)')
    c.hover(CARD('Projeção de lucro'), 2.0, at=c.A(2, 'Projeção', 0.9), label='o cartão Projeção de lucro (estimativa)')
    c.mark(3)
    c.scroll(P('Evolução do preço de compra'), at=c.A(3, 'Evolução', 1.6), label='desce até a Evolução do preço de compra', duration=1.0)
    c.hover(P('Maiores altas e quedas'), 0.4, at=c.A(3, 'maiores', 0.9), label='Visão geral: maiores altas e quedas')
    c.mark(4)
    c.click(SEL('main button:has-text("EST-001 · kg")'), at=c.L(4), label='escolhe o Gás refrigerante R-410A')
    c.waitfor(text='Último preço', timeout=10)
    c.hover(P('Último preço'), 0.5, at=c.A(4, 'último', 0.9), label='Último preço: R$ 94,00')
    c.hover(P('Menor preço'), 0.5, at=c.A(4, 'menor', 0.9), label='Menor preço: R$ 86,00')
    c.hover(P('Maior preço'), 0.5, at=c.A(4, 'maior,', 0.9), label='Maior preço: R$ 94,00')
    c.hover(P('Média do período'), 0.5, at=c.A(4, 'média', 0.9), label='Média do período (ponderada)')
    c.hover(P('Variação'), 1.5, at=c.A(4, 'variação', 0.9), label='Variação do último preço')
    c.mark(5)
    c.scroll(SEL('main th', hasText='Média paga'), at=c.L(5) + 0.2, label='desce até a lista por material', duration=1.0)
    c.hover(SEL('main th', hasText='Média paga'), 1.2, at=c.A(5, 'Média', 0.9), label='a coluna Média paga')
    c.click(SEL('main tbody tr:has-text("Gás refrigerante R-410A")', nth=0), at=c.A(5, 'Clicando', 0.9), label='abre a linha do R-410A')
    c.waitfor(text='Histórico de compras', timeout=10)   # 1.38.19: a linha se abre ali mesmo, com o histórico de compras do material
    c.scroll(P('Histórico de compras'), at=c.A(5, 'vejo', 0.9), label='desce até o histórico de compras', duration=1.0)
    c.hover(P('Histórico de compras'), 3.0, at=c.A(5, 'cada', 0.9), label='Histórico de compras do R-410A')
    c.mark(6)
    c.hover(P('O.C. #4'), 4.0, at=c.L(6) + 0.5, label='as compras: data, fornecedor, ordem, quantidade e preço', optional=True)
    c.fim()
    return c


def cap15():
    c = Cap(15, pace=0.3, cps=14, start=(760, 420), prewarm=['/estoque'], setup=SETUP_ESTOQUE)
    # recapitulação: o robô só passeia pelas abas (a edição monta a recapitulação com trechos dos capítulos anteriores)
    c.mark(1)
    c.hover(ABA_ATUAL, 0.4, at=c.A(1, 'cadastrou', 0.9), label='aba Estoque Atual')
    c.mark(2)
    c.hover(ABA_KARDEX, 0.4, at=c.A(2, 'Kardex.', 0.9), label='aba Histórico de Materiais (Kardex)')
    c.mark(3)
    c.hover(ABA_COMPRAS, 0.4, at=c.A(3, 'requisição,', 0.9), label='aba Compras de Material')
    c.mark(4)
    c.hover(ABA_INVENT, 0.4, at=c.A(4, 'inventário,', 0.9), label='aba Inventários')
    c.hover(ABA_POSICAO, 0.4, at=c.A(4, 'posição', 0.9), label='aba Posição de Estoque')
    c.hover(ABA_RELAT, 0.4, at=c.A(4, 'relatório', 0.9), label='aba Relatório')
    c.mark(5)
    c.hover(P('Controle de peças e materiais'), 3.0, at=c.L(5) + 0.5, label='o título da tela de Estoque')
    c.fim()
    return c

CAPS = {0: cap00, 1: cap01, 2: cap02, 3: cap03, 4: cap04, 5: cap05, 6: cap06, 7: cap07, 8: cap08, 9: cap09, 10: cap10, 11: cap11,
        12: cap12, 13: cap13, 14: cap14, 15: cap15}

if __name__ == '__main__':
    quais = [int(a) for a in sys.argv[1:]] or sorted(CAPS)
    for n in quais:
        c = CAPS[n]()
        if os.environ.get('ANCHORS'):
            for i, w, t in c.anchors:
                print(f'   anchor L{i} "{w}" -> {t}')
        d = c.out()
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
