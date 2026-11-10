#!/usr/bin/env python3
"""T18 · gera rec/t18/cap00..cap15.json (roteiros do robô) a partir da voz pronta (t18/narracao/capNN.json).

Aula inteira no COMPUTADOR (janela 1280x800, 2x), logada como Camila Duarte (admin, Glacial Cold Brasil). Os `at` saem da palavra que
anuncia cada passo (A(linha, palavra, folga)): o gesto "pousa" ~0,7 a 1 s depois do início do passo (clique = deslocamento + 0,85 s;
digitação = clique + texto), então `at` = início da palavra - folga.
Rodar de qualquer pasta: `python3 -I rec/t18/gerar.py [NN ...]`. Depois: `node rec/record.mjs rec/t18/capNN.json --check`.
O T18 não cria nem altera dado da empresa (só cálculo e consulta): todo capítulo parte da MESMA semente (rec/t18/cadeia.json: fim do T7 +
catálogo global fictício) e cada um começa com os campos nos padrões da ferramenta (contexto novo = sessionStorage vazio).

Particularidades (lições deste tutorial, ver docs/08-licoes.md):
 - Selo do nicho: Popover + cmdk (`[cmdk-item]`); os itens são `role=option`, o clique do robô funciona.
 - O botão redondo da OS (aria-label "Área do Técnico™", canto inferior esquerdo, y 672-728) fica dentro da faixa do robô (96..730);
   o botão vermelho "Voltar para OS" do overlay (y ~768) está FORA: vai por `clicar_fixo_alvo` (cursor + retângulo + clique por eval).
 - OS aberta como técnico pede GPS: o stub de geolocalização (geo_stub.js) entra no `setup` para o app não registrar aviso de erro.
 - Chaves LabeledSwitch (BTU/TR, psi/bar, Dew/Bubble, mL/L, Monofásico/Trifásico...) são dois botões com o texto + um Switch no meio:
   clicar no BTN do texto escolhe o lado.
 - Selects do Radix: passo `select` (clica no gatilho e depois na opção `role=option`).
 - Placeholders "Ex: 12" (temperatura) e "Ex: 120" (pressão) do Superaquecimento: `getByPlaceholder` casa por SUBSTRING; sem `exact` o
   robô digitaria a temperatura no campo da pressão. Sempre `exact: True` neles.
 - As abas do Catálogo são botões comuns (não `role=tab`); as do Conversão e da Agenda, sim.
 - Dentro de um modelo/marca/ficha o Catálogo esconde as abas: para trocar de aba, o menu "Catálogo" da esquerda volta à lista (e à aba
   Ar Condicionado).
 - "Limpar filtros" não fecha a janela de filtros: o robô fecha com Escape.
 - Telas longas (Carga Térmica, Superaquecimento, Diluição, Cabo, Retrofit, ficha do compressor, linha branca, detalhes do controle,
   ficha do gás): o que a fala cita fica abaixo da dobra de 800 px; um `scroll` curto antes (duração explícita) evita a rolagem automática
   do robô (~1 s) no meio do gesto.
 - Rótulos em MAIÚSCULAS na tela (DIAGNÓSTICO, AMPER, MAIS INDICADO...) são só CSS: o texto do DOM tem outra caixa. Alvo por `text` SEM
   `exact` (casa sem diferenciar caixa) ou por `hasText`.
"""
import json, os, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
NARR = os.path.normpath(os.path.join(HERE, '..', '..', 't18', 'narracao'))
CAD = json.load(open(os.path.join(HERE, 'cadeia.json'), encoding='utf8'))
BASE = CAD['inicio']
STUB = open(os.path.join(HERE, 'geo_stub.js'), encoding='utf8').read()
OS9 = '48833d34-7e78-5497-9bd8-c25c454e69b2'   # OS #9 (Júlia Santos, Em Andamento, check-in 08:31): a do T5, a mesma em toda a trilha
# localStorage de partida de todo capítulo: o aviso "Você tem 1 chamado de cliente aguardando" (Dashboard) já foi visto
STORAGE = {'dominex:portal-tickets-seen:d40f5787-1779-501f-900c-ddb2b90a36e5': '2031-01-01T00:00:00.000Z'}

NOMES = ['Abertura', 'O segmento define as ferramentas', 'O Início', 'Dentro da ordem de serviço', 'Marcas, modelos e códigos de erro',
         'Compressores, linha branca, controles e fluidos', 'Quantos BTUs o ambiente pede', 'Pressão, temperatura, potência e medidas',
         'Capacitor', 'Cabo e disjuntor', 'Superaquecimento e subresfriamento', 'Régua de Gases', 'Retrofit de Gás',
         'Ciclo de Refrigeração e termos', 'Produto e água', 'Recapitulando']

# rotas das ferramentas (prewarm: o módulo da rota já está na memória quando o capítulo clica no menu)
ROTA = {'Catálogo': 'catalogo', 'Carga Térmica': 'carga-termica', 'Conversão': 'conversao', 'Cálculo de Capacitor': 'calculo-capacitor',
        'Cabo Elétrico': 'cabo-eletrico', 'Superaquecimento': 'superaquecimento', 'Régua de Gases': 'regua-gases',
        'Retrofit de Gás': 'retrofit-gas', 'Ciclo de Refrigeração': 'ciclo-refrigeracao', 'Diluição de Produto': 'diluicao-produto'}


def norm(s):
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode().lower()
    return ''.join(ch for ch in s if ch.isalnum() or ch in '?')


class Cap:
    def __init__(s, n, pace=0.5, cps=9, start=(760, 420), prewarm=None, setup=None, user=None):
        s.n = n
        d = json.load(open(f'{NARR}/cap{n:02d}.json', encoding='utf8'))
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

    def A(s, i, palavra, folga=0.8, nth=0):
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
        kw.setdefault('timeout', 3)
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

    def drag(s, target, to, at=None, label=None, **kw):
        return s._p({'do': 'drag', 'target': target, 'to': to}, at, label, kw)

    def ev(s, js, at=None, label=None, **kw):
        return s._p({'do': 'eval', 'js': js}, at, label, kw)

    def clicar_fixo_alvo(s, alvo, ponto, js, at, label):
        """Botão FIXO fora da faixa y 96..730 (aqui, o "Voltar para OS" do overlay, y ~768): o `click` do robô tentaria rolar em vão e
        atrasaria alguns segundos. Leva o cursor com `scroll by 0 point`, registra o retângulo do `alvo` (passo `type` sem clique) e clica
        por `eval`. `at` = instante do clique; o cursor parte 0,9 s antes. Molde do T5/T7."""
        s._p({'do': 'scroll', 'point': {'x': ponto[0], 'y': ponto[1]}, 'by': 0, 'duration': 0.3, 'after': 0}, round(max(0.0, at - 0.9), 2), label + ' (cursor)', {})
        s.add({'do': 'type', 'target': alvo, 'text': '', 'noClick': True, 'label': label, 'optional': True, 'timeout': 4})
        return s._p({'do': 'eval', 'js': js}, round(at, 2), label + ' (clique)', {})

    def fim(s):
        s.flush(1e9)
        s.steps.append({'do': 'mark', 'name': 'FIM', 'at': round(s.dur, 2)})

    def out(s):
        d = {
            'name': f't18-cap{s.n:02d}',
            'title': f'T18 · Cap. {s.n} · {NOMES[s.n]} (narração {str(round(s.dur, 1)).replace(".", ",")} s; marcas L1..L{len(s.linhas)} = início de cada linha do roteiro)',
            'seed': f't18-cap{s.n:02d}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
            'start': {'x': s.start[0], 'y': s.start[1]},
            'seedExtra': list(BASE),
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
TAB = lambda n, **kw: {'role': 'tab', 'name': n, **kw}
TXT = lambda t, **kw: {'text': t, 'exact': True, **kw}                    # texto INTEIRO igual (e na mesma caixa)
P = lambda t, **kw: {'text': t, 'within': 'main', **kw}                   # texto por substring, sem diferenciar caixa
SEL = lambda s, **kw: {'selector': s, **kw}
CAMPO = lambda n: {'label': n, 'exact': True}
NAV = lambda n: {'selector': 'nav button', 'hasText': n}                 # menu das ferramentas (esquerda), fora do overlay
BADGE = lambda n: {'selector': 'main button', 'hasText': n}              # selo do nicho
ITEM = lambda n: {'selector': '[cmdk-item]', 'hasText': n}               # item da lista de nichos
AT = 'Área do Técnico™'
# cartões do Início: o texto da descrição não se repete (o nome sozinho também está no menu da esquerda)
CARTAO = {
    'Catálogo': 'Consulte modelos', 'Carga Térmica': 'Calcule os BTUs', 'Conversão': 'Converta pressão',
    'Cálculo de Capacitor': 'Encontre o capacitor', 'Cabo Elétrico': 'Bitola do cabo', 'Superaquecimento': 'Calcule SH',
    'Régua de Gases': 'Pressão de saturação dos gases', 'Retrofit de Gás': 'Gases drop-in', 'Ciclo de Refrigeração': 'Entenda o ciclo',
    'Diluição de Produto': 'Calcule produto',
}
CARD = lambda nome: {'selector': 'main button', 'hasText': CARTAO[nome]}
CARD_OV = lambda nome: {'selector': 'button', 'hasText': CARTAO[nome]}   # cartão no overlay (fora do <main>)
FAB = {'selector': "button[aria-label='Área do Técnico™']"}          # botão redondo da OS do técnico
COMBO = lambda n=0: {'selector': 'main button[role=combobox]', 'nth': n}   # gatilho de um Select do Radix
TABC = lambda n: {'selector': 'main button', 'hasText': n}               # aba do Catálogo (botão comum)
PRESSAO = {'placeholder': 'Ex: 120', 'exact': True}                       # Superaquecimento: pressão (exact: "Ex: 12" é substring)
TEMPERATURA = {'placeholder': 'Ex: 12', 'exact': True}
SELO = lambda t: {'selector': 'main span.rounded-full', 'hasText': t}     # selo Baixo/Ideal/Alto do Superaquecimento
RESULT5 = {'selector': 'main p.text-5xl'}                                 # número grande do resultado (Carga Térmica, SH/SC)

# ---------------------------------------------------------------- trechos comuns (não filmados, no `setup`)
SETUP_APP = lambda rota, esperar: [
    {'do': 'goto', 'url': rota}, {'do': 'waitFor', 'text': esperar, 'timeout': 25}, {'do': 'waitFor', 'idle': True}]
SETUP_DASH = SETUP_APP('/dashboard', 'Olá, Camila!')
SETUP_INICIO = SETUP_APP('/area-tecnico', 'Termos Técnicos Explicados')
SETUP_CATALOGO = SETUP_APP('/area-tecnico/catalogo', 'Catálogo - Ar Condicionado')
PREWARM_AT = ['/dashboard', '/area-tecnico']


def prewarm(*tools):
    return PREWARM_AT + [f'/area-tecnico/{ROTA[t]}' for t in tools]


# ================================================================ capítulos
def cap00():
    """Abertura: o Dashboard; o cursor aponta o item "Área do Técnico™" do menu (o capítulo seguinte clica nele)."""
    c = Cap(0, pace=0.5, start=(760, 420), prewarm=['/dashboard'], setup=SETUP_DASH)
    c.mark(1)
    c.hover(LINK(AT), 6.0, at=c.A(1, 'Área', 0.9), label='o item "Área do Técnico™" do menu')
    c.mark(2)
    c.mark(3)
    c.fim()
    return c


def cap01():
    c = Cap(1, pace=0.5, start=(760, 420), prewarm=PREWARM_AT, setup=SETUP_DASH)
    c.mark(1)
    c.hover(LINK(AT), 0.6, at=c.A(1, 'menu', 1.0), label='"Área do Técnico™" no menu da esquerda')
    c.hover(BTN('Operacional'), 0.3, at=c.A(1, 'Operacional', 1.0), label='o grupo Operacional')
    c.click(LINK(AT), at=c.A(1, 'Quando', 0.9), label='clica em "Área do Técnico™" no menu')
    c.waitfor(text='Termos Técnicos Explicados', timeout=20)
    c.hover(BADGE('Refrigeração e Climatização'), 2.2, at=c.A(1, 'selo', 0.9), label='o selo do segmento: Refrigeração e Climatização')
    c.mark(2)
    c.click(BADGE('Refrigeração e Climatização'), at=c.A(2, 'Clicando', 0.8), label='clica no selo do segmento')
    c.hover(ITEM('Incluído'), 2.0, at=c.A(2, 'primeiro,', 0.9), label='a marca "Incluído" no nicho da empresa')
    c.mark(3)
    c.click(ITEM('Energia Solar'), at=c.A(3, 'Energia', 1.0), label='escolhe Energia Solar')
    c.hover(BADGE('Dimensionamento Fotovoltaico'), 0.8, at=c.A(3, 'ferramentas', 0.8), label='as ferramentas com cadeado')
    c.hover(BTN('Falar com representante'), 1.6, at=c.A(3, 'botão', 0.8), label='o botão "Falar com representante" (sem clicar)')
    c.mark(4)
    c.click(BADGE('Energia Solar'), at=c.A(4, 'Volto', 0.9), label='abre o selo de novo')
    c.click(ITEM('Refrigeração e Climatização'), at=c.A(4, 'segmento,', 0.8), label='volta para Refrigeração e Climatização')
    c.hover(NAV('Catálogo'), 2.0, at=c.A(4, 'refrigeração', 0.9), label='o menu com as ferramentas de refrigeração')
    c.fim()
    return c


def cap02():
    c = Cap(2, pace=0.35, start=(760, 420), prewarm=PREWARM_AT, setup=SETUP_INICIO)
    BUSCA = {'placeholder': 'Buscar termo (ex: BTU, capacitor, pressão)'}
    c.mark(1)
    c.hover(NAV('Início'), 0.5, at=0.4, label='o Início, porta de entrada das ferramentas')
    t0 = c.A(1, 'Ferramentas', 0.8)
    ordem = ['Catálogo', 'Carga Térmica', 'Conversão', 'Cálculo de Capacitor', 'Cabo Elétrico', 'Superaquecimento', 'Régua de Gases',
             'Retrofit de Gás', 'Ciclo de Refrigeração', 'Diluição de Produto']
    passo = (c.A(1, 'hoje', 0.4) - t0) / len(ordem)
    for i, nome in enumerate(ordem):
        c.hover(CARD(nome), 0.1, at=t0 + i * passo, label=f'cartão {nome}')
    c.mark(2)
    c.scroll(by=650, at=c.A(2, 'Logo', 0.1), label='desce até os Termos Técnicos Explicados', duration=1.4)
    c.type(BUSCA, 'capacitor', at=c.A(2, 'Digito', 1.0), label='digita "capacitor" na busca do glossário', cps=8)
    c.click(SEL('main button', hasText='Capacitor (µF'), at=c.A(2, 'abro', 0.8), label='abre o termo Capacitor')
    c.scroll(by=170, at=c.A(2, 'explicação', 0.4), label='desce até o exemplo do termo', duration=0.8)
    c.hover(P('Um compressor de 18.000 BTUs'), 7.0, at=c.A(2, 'exemplo', 0.8), label='o Exemplo: compressor de 18.000 BTUs, capacitor de ~40 µF')
    c.mark(3)
    c.type(BUSCA, '', at=c.A(3, 'Sem', 0.9), label='limpa a busca', clear=True)
    for palavra, titulo in [('Medidas', 'Medidas e Unidades'), ('Ciclo', 'Ciclo Básico de Refrigeração'),
                            ('Elétrica', 'Elétrica e Instalação'), ('Gases', 'Gases e Nomenclatura')]:
        alvo = SEL('main h3', hasText=titulo)
        c.scroll(alvo, at=c.A(3, palavra, 1.6), label=f'rola até o grupo {titulo}')
        c.hover(alvo, 0.15, at=c.A(3, palavra, 0.5), label=f'grupo {titulo}')
    c.fim()
    return c


def cap03():
    setup = SETUP_APP('/agenda', 'Visualize e gerencie os agendamentos') + [{'do': 'eval', 'js': STUB}]
    c = Cap(3, pace=0.5, start=(700, 420), prewarm=['/agenda', f'/os-tecnico/{OS9}', '/area-tecnico'], setup=setup)
    c.mark(1)
    c.click(TXT('#9', within='main'), at=0.0, label='abre a OS #9, em andamento, na Agenda')
    c.waitfor(text='Resumo da OS', timeout=10)
    c.hover(TXT('Em Andamento', within='main'), 0.3, at=1.3, label='o resumo da OS: Em Andamento')
    c.scroll(BTN('Preencher OS'), at=1.9, label='rola o resumo até o botão Preencher OS', duration=0.8)
    c.click(BTN('Preencher OS'), at=2.7, label='clica em Preencher OS')
    c.waitfor(text='Glacial Cold Brasil', timeout=20)
    c.hover(FAB, 2.0, at=c.A(1, 'canto', 0.9), label='o botão redondo da Área do Técnico, no canto da ordem')
    c.mark(2)
    c.click(FAB, at=c.A(2, 'Um', 0.9), label='clica no botão redondo')
    c.waitfor(text='Voltar para OS', timeout=15)
    c.hover(CARD_OV('Catálogo'), 0.2, at=c.A(2, 'mesmas', 2.0), label='as mesmas ferramentas do Início')
    c.mark(3)
    c.click(CARD_OV('Conversão'), at=c.A(3, 'Abro', 2.7), label='abre a Conversão')
    c.clicar_fixo_alvo(SEL('button', hasText='Voltar para OS'), (640, 768),
                       "[...document.querySelectorAll('button')].find(b=>/Voltar para OS/.test(b.textContent)).click()",
                       c.A(3, 'Voltar', 0.2), 'botão vermelho Voltar para OS')
    c.mark(4)
    t = c.A(3, 'continua', 0.5)
    c.hover(TXT('Checklists'), round(max(2.0, c.dur - t - 1.2), 1), at=t, label='a ordem continua do ponto onde parou: o cartão Checklists')
    c.fim()
    return c


def cap04():
    c = Cap(4, pace=0.5, start=(760, 420), prewarm=prewarm('Catálogo'), setup=SETUP_INICIO)
    BUSCA = {'placeholder': 'Buscar por marca, equipamento ou código de erro'}
    CARTAO18 = TXT('Hi-Wall 18.000 BTUs', within='main')
    AJUSTAR = SEL('main button', hasText='Ajustar', nth=2)
    CODIGOS = SEL('main button', hasText='Códigos de erro', nth=2)
    BAIXAR = SEL('main button', hasText='Baixar manual', nth=2)
    DLG = '[role=dialog]'
    c.mark(1)
    c.click(NAV('Catálogo'), at=0.0, label='abre o Catálogo')
    c.waitfor(text='Catálogo - Ar Condicionado', timeout=20)
    for palavra, nome, nth in [('Ar', 'Ar Condicionado', 0), ('Compressores,', 'Compressores', 0), ('Linha', 'Linha Branca', 0),
                               ('Controles', 'Controles Remotos', 0), ('Fluidos', 'Fluidos Refrigerantes', 0)]:
        c.hover(TABC(nome), 0.2, at=c.A(1, palavra, 0.7, nth=nth), label=f'aba {nome}')
    c.hover(TABC('Ar Condicionado'), 0.5, at=c.A(1, 'Ar', 0.7, nth=1), label='começa pela aba Ar Condicionado')
    c.mark(2)
    c.type(BUSCA, 'E1', at=c.A(2, 'digitar', 1.0), label='digita E1 na busca', cps=6)
    c.hover(SEL('main button', hasText='Hi-Wall 9.000 BTUs'), 0.3, at=c.A(2, 'mostra', 0.8), label='os aparelhos em que o E1 existe')
    c.hover(SEL('main button', hasText='Cristalar'), 0.5, at=c.A(2, 'aparelhos', 0.6), label='o aparelho da Cristalar com E1')
    c.mark(3)
    c.type(BUSCA, '', at=c.A(2, 'existe.', 0.3), label='limpa a busca', clear=True)
    c.click(BTNX('Filtros'), at=c.A(3, 'Também', 0.0) + 0.3, label='abre os Filtros')
    c.hover(P('Potência', within=DLG), 0.15, at=c.A(3, 'potência,', 0.0) - 0.3, label='grupo Potência')
    c.hover(P('Tipo', within=DLG), 0.15, at=c.A(3, 'tipo', 1.0), label='grupo Tipo')
    c.hover(P('Gás refrigerante', within=DLG), 0.15, at=c.A(3, 'gás', 1.0), label='grupo Gás refrigerante')
    c.click(SEL(DLG + ' button', hasText='18.000 BTUs'), at=c.A(3, 'dezoito', 0.8), label='marca 18.000 BTUs')
    c.click(BTN('Ver resultados'), at=c.A(3, 'Ver', 0.8), label='Ver resultados')
    c.hover(CARTAO18, 0.3, at=c.A(3, 'modelos', 0.8), label='os modelos dessa potência')
    c.mark(4)
    c.click(BTNX('Filtros'), at=c.L(4) - 1.9, label='reabre os Filtros para limpar')
    c.click(BTN('Limpar filtros'), at=c.L(4) - 0.9, label='Limpar filtros')
    c.press('Escape', at=c.L(4) + 0.1, label='fecha a janela de Filtros')
    c.click(SEL('main button', hasText='Aerovento'), at=c.A(4, 'Aerovento,', 0.8), label='entra na marca Aerovento')
    c.scroll(CARTAO18, at=c.A(4, 'ordem', 0.3), label='rola até o cartão Hi-Wall 18.000 BTUs')
    c.hover(CARTAO18, 0.4, at=c.A(4, 'Hi-Wall', 0.8), label='o cartão do Hi-Wall 18.000 BTUs')
    c.hover(TXT('18.000 BTUs', within='main', nth=0), 0.2, at=c.A(4, 'potência,', 0.7, nth=1), label='selo de potência')
    c.hover(TXT('Split Hi-Wall', within='main', nth=2), 0.2, at=c.A(4, 'tipo,', 0.7), label='selo de tipo')
    c.hover(TXT('R-410A', within='main', nth=2), 0.2, at=c.A(4, 'refrigerante', 0.9), label='selo do gás')
    c.hover(TXT('Cód.: AV-HW18', within='main'), 0.2, at=c.A(4, 'código', 0.7), label='selo do código do modelo')
    c.mark(5)
    c.hover(P('Por hora', nth=2), 0.6, at=c.A(5, 'consumo', 0.8), label='o consumo estimado do cartão')
    c.click(AJUSTAR, at=c.A(5, 'Ajustar,', 1.1), label='clica em Ajustar')
    c.type(SEL(DLG + ' input'), '0,95', at=c.A(5, 'tarifa', 1.3), label='tarifa 0,95', clear=True, cps=7)
    c.click(SEL(DLG + ' [role=slider]'), at=c.A(5, 'horas', 1.0), label='pega o controle deslizante das horas de uso')
    c.press('ArrowRight', at=c.A(5, 'uso', 0.3), label='horas de uso +1')
    c.press('ArrowRight', at=c.A(5, 'por', 0.0), label='horas de uso +1 (2)')
    c.press('ArrowRight', at=c.A(5, 'dia,', 0.0), label='horas de uso +1 (3)')
    c.click(BTN('Aplicar'), at=c.A(5, 'Aplicar,', 0.9), label='Aplicar')
    c.hover(P('Por mês', nth=2), 1.0, at=c.A(5, 'mês', 0.8), label='o valor por mês atualizado')
    c.mark(6)
    c.click(CODIGOS, at=c.A(6, 'Códigos', 0.8), label='clica em Códigos de erro')
    c.type({'placeholder': 'Ex: E1, F0, P4...', 'exact': True}, 'E1', at=c.A(6, 'Digito', 0.9), label='digita E1 no campo do display', cps=5)
    c.hover(TXT('E1', within='main'), 0.2, at=c.A(6, 'abro', 0.8), label='o código E1')
    c.hover(P('Diagnóstico'), 0.2, at=c.A(6, 'Diagnóstico', 0.8), label='Diagnóstico em passos')
    c.scroll(by=210, at=c.A(6, 'Solução', 1.7), label='desce até a Solução e o componente', duration=0.5)
    c.hover(P('Solução'), 0.2, at=c.A(6, 'Solução', 0.8), label='Solução')
    c.hover(P('Componente'), 0.3, at=c.A(6, 'componente', 1.0), label='o componente envolvido')
    c.mark(7)
    c.click(SEL('main button:has(svg.lucide-arrow-left)'), at=c.L(7) - 1.9, label='volta ao cartão')
    c.scroll(BAIXAR, at=c.A(7, 'manual,', 0.8), label='rola até o botão Baixar manual')
    c.hover(BAIXAR, 1.2, at=c.A(7, 'Baixar', 0.7), label='o botão Baixar manual (sem clicar)')
    c.fim()
    return c


def cap05():
    c = Cap(5, pace=0.3, start=(760, 420), prewarm=prewarm('Catálogo'), setup=SETUP_CATALOGO)
    c.mark(1)
    c.click(TABC('Compressores'), at=c.A(1, 'Compressores,', 1.4), label='aba Compressores')
    c.click(SEL('main button', hasText='Nortec'), at=c.A(1, 'Ficha', 1.2), label='entra na marca Nortec')
    c.click(SEL('main button', hasText='Ficha técnica', nth=1), at=c.A(1, 'técnica', 0.4), label='Ficha técnica do compressor de 18.000 BTUs')
    c.scroll(by=400, at=c.A(1, 'procura', 0.0), label='desce até os capacitores, o óleo e as equivalências', duration=0.9)
    c.hover(P('Capacitor de trabalho'), 0.5, at=c.A(1, 'capacitores', 0.8), label='Capacitor de trabalho')
    c.hover(P('Capacitor de partida'), 0.5, at=c.A(1, 'partida,', 0.8), label='Capacitor de partida')
    c.hover(TXT('Óleo', within='main'), 0.4, at=c.A(1, 'óleo', 0.8), label='Óleo')
    c.hover(P('Equivalências'), 0.6, at=c.A(1, 'equivalências', 0.8), label='Equivalências')
    c.mark(2)
    c.click(NAV('Catálogo'), at=c.L(2) - 1.9, label='volta à lista do Catálogo')
    c.click(TABC('Linha Branca'), at=c.A(2, 'Branca,', 0.9), label='aba Linha Branca')
    c.click(SEL('main button', hasText='Brisamar'), at=c.A(2, 'geladeiras', 0.7), label='entra na marca Brisamar')
    c.scroll(by=330, at=c.A(2, 'freezers', 0.0), label='desce até o consumo e os códigos de erro', duration=0.9)
    c.hover(SEL('main button', hasText='Códigos de erro'), 0.4, at=c.A(2, 'códigos', 0.8), label='botão Códigos de erro da geladeira')
    c.hover(P('Por mês'), 0.4, at=c.A(2, 'consumo,', 0.8), label='Consumo de energia')
    c.hover(P('24 h/dia'), 0.8, at=c.A(2, 'vinte', 0.8), label='estimado em 24 h/dia')
    c.mark(3)
    c.click(NAV('Catálogo'), at=c.L(3) - 1.0, label='volta à lista do Catálogo')
    c.click(TABC('Controles Remotos'), at=c.A(3, 'Remotos,', 0.9), label='aba Controles Remotos')
    c.click(SEL('main button', hasText='Ver detalhes técnicos', nth=0), at=c.A(3, 'Detalhes', 0.9), label='Ver detalhes técnicos do controle')
    c.hover(P('Como configurar'), 0.5, at=c.A(3, 'configurar', 0.8), label='Como configurar')
    c.scroll(by=300, at=c.A(3, 'controle', 0.6, nth=1), label='desce até o Código universal', duration=0.9)
    c.mark(4)
    c.click(NAV('Catálogo'), at=c.L(4) - 1.5, label='volta à lista do Catálogo')
    c.click(TABC('Fluidos Refrigerantes'), at=c.A(4, 'Fluidos', 1.1), label='aba Fluidos Refrigerantes')
    c.hover(P('Puros'), 0.4, at=c.A(4, 'Puros', 0.8), label='seção Puros')
    c.hover(P('Misturas'), 0.4, at=c.A(4, 'Misturas.', 0.7), label='seção Misturas')
    c.click(SEL('main button', hasText='R-32', nth=0), at=c.A(4, 'trinta', 1.0), label='abre o R-32')
    c.hover(TXT('GWP', within='main'), 0.6, at=c.A(4, 'potencial', 0.7), label='GWP (potencial de aquecimento global)')
    c.scroll(by=120, at=c.A(4, 'global,', 0.6), label='desce até o que ele substitui', duration=0.7)
    c.hover(P('Classe de segurança'), 0.6, at=c.A(4, 'classe', 0.7), label='Classe de segurança')
    c.hover(TXT('Substitui', within='main'), 1.0, at=c.A(4, 'substitui.', 0.7), label='Substitui')
    c.fim()
    return c


def cap06():
    c = Cap(6, pace=0.5, start=(760, 420), prewarm=prewarm('Carga Térmica'), setup=SETUP_INICIO)
    c.mark(1)
    c.click(NAV('Carga Térmica'), at=c.A(1, 'Carga', 0.9), label='abre a Carga Térmica')
    c.waitfor(text='Dimensione a capacidade em BTUs do ambiente.', timeout=15)
    c.scroll(by=250, at=c.A(1, 'sala', 1.2), label='sobe a tela: campos e resultado juntos', duration=0.9)
    c.mark(2)
    c.type(CAMPO('Altura (metros)'), '2,8', at=c.A(2, 'dois', 1.15), label='altura 2,8', cps=7)
    c.type(CAMPO('Largura (metros)'), '4', at=c.A(2, 'quatro', 1.15), label='largura 4', cps=7)
    c.type(CAMPO('Comprimento (metros)'), '5', at=c.A(2, 'cinco', 1.15), label='comprimento 5', cps=7)
    c.type(CAMPO('Quantidade de pessoas'), '4', at=c.A(2, 'quatro', 1.15, nth=1), label='4 pessoas', cps=7)
    c.type(CAMPO('Eletroeletrônicos'), '3', at=c.A(2, 'três', 1.15), label='3 eletroeletrônicos', cps=7)
    c.type(CAMPO('Janelas (2 x 1,5 metros)'), '1', at=c.A(2, 'uma', 1.15), label='1 janela', cps=7)
    c.hover(RESULT5, 2.4, at=c.A(2, 'dezesseis', 0.9), label='o resultado: 16.800 BTUs')
    c.mark(3)
    c.click(BTN('TR'), at=c.A(3, 'TR,', 0.9), label='chave BTU / TR: TR')
    c.hover(RESULT5, 1.2, at=c.A(3, 'aqui,', 0.8), label='resultado em TR: 1,4')
    c.click(BTN('BTU'), at=c.L(4) - 0.9, label='volta para BTU')
    c.mark(4)
    c.click({'role': 'switch', 'name': 'Ambiente ensolarado?'}, at=c.A(4, 'ligar', 0.9), label='liga Ambiente ensolarado?')
    c.hover(RESULT5, 1.6, at=c.A(4, 'vinte', 0.9), label='o resultado sobe: 21.200 BTUs')
    c.hover(P('Recomenda-se'), 3.0, at=c.A(4, 'nota', 0.8), label='a nota abaixo do resultado')
    c.hover(P('Ferramenta de apoio'), 6.0, at=c.A(4, 'rodapé', 0.8), label='o rodapé "Ferramenta de apoio..."')
    c.fim()
    return c


def cap07():
    c = Cap(7, pace=0.5, start=(760, 420), prewarm=prewarm('Conversão'), setup=SETUP_INICIO)
    ESQ = {'placeholder': '0', 'exact': True, 'nth': 0}
    DIR = {'placeholder': '0', 'exact': True, 'nth': 1}
    c.mark(1)
    c.click(NAV('Conversão'), at=0.0, label='abre a Conversão')
    c.waitfor(text='Converta entre unidades de medida.', timeout=15)
    c.type(ESQ, '10', at=c.A(1, 'digito', 1.2), label='digita 10 bar', clear=True, cps=7)
    c.hover(DIR, 1.0, at=c.A(1, 'vejo', 0.8), label='145 psi no campo Para')
    c.click(BTN('Inverter unidades'), at=c.A(1, 'Inverter', 0.9), label='Inverter unidades')
    c.hover(TAB('Temperatura'), 0.2, at=c.A(1, 'Temperatura,', 0.7), label='aba Temperatura')
    c.hover(TAB('Potência'), 0.2, at=c.A(1, 'Potência', 0.7), label='aba Potência')
    c.hover(TAB('Comprimento'), 0.2, at=c.A(1, 'Comprimento', 0.7), label='aba Comprimento')
    c.mark(2)
    c.hover(P('Mais usadas'), 0.6, at=c.A(2, 'Mais', 0.9), label='o bloco Mais usadas')
    c.hover(BTN('HP → BTU/h'), 0.3, at=c.A(2, 'HP', 0.7), label='atalho HP → BTU/h (mostra)')
    c.hover(BTN('mm → pol'), 0.3, at=c.A(2, 'milímetros', 0.7), label='atalho mm → pol (mostra)')
    c.click(BTN('HP → BTU/h'), at=c.A(2, 'HP', 0.9, nth=1), label='atalho HP → BTU/h')
    c.hover(P('Modo de cálculo'), 1.0, at=c.A(2, 'Modo', 0.8), label='Modo de cálculo: Refrigeração e Energia')
    c.hover(BTNX('Refrigeração'), 0.5, at=c.A(2, 'Refrigeração,', 0.8), label='modo Refrigeração')
    c.type(ESQ, '2', at=c.A(2, 'dois', 1.2), label='2 HP', clear=True, cps=7)
    c.hover(DIR, 1.0, at=c.A(2, 'dezoito', 0.8), label='18.000 BTU/h em Refrigeração')
    c.click(BTNX('Energia'), at=c.A(2, 'Energia,', 0.9), label='modo Energia')
    c.hover(DIR, 0.4, at=c.A(2, 'cinco', 0.8), label='5.088 BTU/h em Energia')
    c.mark(3)
    c.click(BTN('mm → pol'), at=c.L(3) - 1.9, label='atalho mm → pol')
    c.type(ESQ, '6,35', at=c.A(3, 'seis', 1.2), label='6,35 mm', clear=True, cps=7)
    c.hover(DIR, 1.2, at=c.A(3, 'um', 0.8, nth=0), label='0,25 pol')
    c.mark(4)
    c.click(BTN('Favoritar conversão'), at=c.A(4, 'estrela', 0.9), label='a estrela Favoritar conversão')
    c.hover(P('Favoritas'), 2.2, at=c.A(4, 'Favoritas,', 0.8), label='a lista Favoritas')
    c.fim()
    return c


def cap08():
    c = Cap(8, pace=0.5, start=(760, 420), prewarm=prewarm('Cálculo de Capacitor'), setup=SETUP_INICIO)
    USE = SEL('main p.leading-tight')
    c.mark(1)
    c.click(NAV('Cálculo de Capacitor'), at=c.A(1, 'capacitor.', 1.0), label='abre o Cálculo de Capacitor')
    c.waitfor(text='Capacitor recomendado pela fase, BTU/LRA e tensão.', timeout=15)
    c.select(COMBO(0), '18.000 BTUs', at=c.A(1, 'Escolho', 0.9), label='escolhe 18.000 BTUs')
    c.click(BTN('220V'), at=c.A(1, 'tensão,', 0.9), label='tensão 220V')
    c.hover(USE, 2.4, at=c.A(1, 'recomenda', 0.8), label='Use o capacitor de 40 µF')
    c.hover(P('Amper'), 0.6, at=c.A(1, 'corrente', 0.8), label='Amper')
    c.hover(P('Potência', nth=0), 0.6, at=c.A(1, 'potência', 0.8), label='Potência')
    c.mark(2)
    c.click({'role': 'button', 'name': 'Ampliar foto'}, at=c.A(2, 'ampliar.', 1.0), label='amplia a foto do capacitor')
    c.mark(3)
    c.press('Escape', at=c.L(3) + 0.3, label='fecha a foto ampliada')
    c.click(BTN('Preciso (LRA)'), at=c.A(3, 'Preciso', 0.9), label='modo Preciso (LRA)')
    c.type({'placeholder': 'Ex: 40', 'exact': True}, '30', at=c.A(3, 'trinta', 1.2), label='LRA 30', cps=7)
    c.hover(USE, 2.0, at=c.A(3, 'resultado', 0.8), label='31 µF')
    c.click(BTN('Estimativa (BTU)'), at=c.A(3, 'Estimativa', 0.9), label='Estimativa (BTU)')
    c.mark(4)
    c.click(BTN('Trifásico'), at=c.A(4, 'Trifásico', 0.9), label='chave Fase: Trifásico')
    c.hover(P('Máquina trifásica não usa capacitor'), 0.3, at=c.A(4, 'máquina', 0.8), label='a máquina trifásica não usa capacitor')
    c.type({'placeholder': 'Ex: 2,9', 'exact': True}, '9', at=c.A(4, 'capacitor,', 0.9), label='corrente nominal 9 A', cps=7)
    c.hover(P('Contator recomendado'), 0.8, at=c.A(4, 'contator', 0.8), label='Contator recomendado')
    c.hover(P('Relé térmico:'), 1.0, at=c.A(4, 'relé', 0.8), label='Relé térmico')
    c.fim()
    return c


def cap09():
    c = Cap(9, pace=0.5, start=(760, 420), prewarm=prewarm('Cabo Elétrico'), setup=SETUP_INICIO)
    RESULTADO = SEL('main p.leading-snug')
    DIST = {'placeholder': 'Ex: 40', 'exact': True}
    c.mark(1)
    c.click(NAV('Cabo Elétrico'), at=c.A(1, 'cabo', 1.0), label='abre o Cabo Elétrico')
    c.waitfor(text='Seleção de seção do cabo elétrico para ar-condicionado em geral.', timeout=15)
    c.select(COMBO(0), '18.000 BTUs', at=c.A(1, 'Escolho', 0.9), label='escolhe 18.000 BTUs')
    c.click(BTN('220V'), at=c.A(1, 'duzentos', 0.2), label='tensão 220V')
    c.type(DIST, '20', at=c.A(1, 'vinte', 1.2, nth=1), label='distância 20 m', cps=7)
    c.hover(RESULTADO, 2.6, at=c.A(1, 'quatro', 0.9), label='cabo 4 mm² e disjuntor de 16 A')
    c.scroll(by=260, at=c.A(1, 'queda', 1.5), label='desce: queda de tensão e foto do disjuntor', duration=0.9)
    c.hover(P('Queda de tensão'), 0.7, at=c.A(1, 'tensão', 0.8), label='queda de tensão')
    c.hover({'role': 'button', 'name': 'Ampliar foto'}, 1.0, at=c.A(1, 'foto', 0.8), label='a foto do disjuntor')
    c.mark(2)
    c.type(DIST, '30', at=c.A(2, 'mudar', 1.0), label='distância 30 m', clear=True, cps=7)
    c.hover(RESULTADO, 2.2, at=c.A(2, 'seis', 0.9), label='cabo de 6 mm²')
    c.fim()
    return c


def cap10():
    c = Cap(10, pace=0.5, start=(760, 420), prewarm=prewarm('Superaquecimento'), setup=SETUP_INICIO)
    c.mark(1)
    c.click(NAV('Superaquecimento'), at=c.A(1, 'Superaquecimento,', 0.9), label='abre o Superaquecimento')
    c.waitfor(text='Calcule SH e SC pela pressão e temperatura medidas em campo.', timeout=15)
    c.hover(COMBO(0), 1.0, at=c.A(1, 'Modelo', 0.9), label='o campo Modelo / fabricante')
    c.click(COMBO(0), at=c.A(1, 'está', 0.9), label='abre a lista de modelos / fabricantes')
    c.click({'role': 'option', 'name': 'Padrão'}, at=c.A(1, 'sugere', 0.0), label='escolhe Padrão')
    c.hover(COMBO(1), 0.8, at=c.A(1, 'gás', 0.8, nth=2), label='Fluido Refrigerante: R-410A')
    c.hover(BTN('psi'), 0.6, at=c.A(1, 'unidade', 0.9), label='Unidade de pressão: psi')
    c.scroll(by=330, at=c.A(1, 'pressão,', 0.4, nth=1), label='desce até os campos e a nota', duration=1.0)
    c.mark(2)
    c.hover(P('Valor genérico de referência'), 4.6, at=c.L(2), label='a nota do modelo Padrão')
    c.mark(3)
    c.type(PRESSAO, '118', at=c.A(3, 'cento', 1.2), label='pressão de baixa 118 psi', cps=7)
    c.type(TEMPERATURA, '12', at=c.A(3, 'doze', 1.2), label='temperatura da linha de sucção 12', cps=7)
    c.hover(RESULT5, 1.4, at=c.A(3, 'sete', 0.9), label='superaquecimento 7,7 °C')
    c.hover(SELO('Ideal'), 1.6, at=c.A(3, 'selo', 0.8), label='selo Ideal')
    c.mark(4)
    c.type(PRESSAO, '125', at=c.L(4), label='pressão 125 psi', clear=True, cps=7)
    c.type(TEMPERATURA, '15', at=c.A(4, 'quinze', 1.0), label='temperatura 15', clear=True, cps=7)
    c.hover(RESULT5, 1.2, at=c.A(4, 'nove', 0.9), label='9,1 °C')
    c.hover(SELO('Alto'), 1.8, at=c.A(4, 'selo', 0.8), label='selo Alto')
    c.mark(5)
    c.scroll(by=-330, at=c.L(5) - 1.6, label='sobe até as abas', duration=0.7)
    c.click(BTN('Subresfriamento (SC)'), at=c.A(5, 'Subresfriamento', 0.9), label='aba Subresfriamento (SC)')
    c.scroll(by=330, at=c.A(5, 'é', 0.3), label='desce até os campos', duration=0.8)
    c.type(PRESSAO, '350', at=c.A(5, 'trezentos', 1.2), label='pressão de alta 350 psi', cps=7)
    c.type(TEMPERATURA, '35', at=c.A(5, 'trinta', 1.2), label='temperatura da linha de líquido 35', cps=7)
    c.hover(RESULT5, 1.0, at=c.A(5, 'seis', 0.9), label='6,4 °C')
    c.hover(SELO('Ideal'), 1.0, at=c.A(5, 'Ideal.', 0.8), label='selo Ideal do subresfriamento')
    c.mark(6)
    c.hover(BTN('psi'), 5.0, at=c.A(6, 'unidade', 0.9), label='a chave psi / bar da Unidade de pressão (sem trocar)')
    c.fim()
    return c


def cap11():
    c = Cap(11, pace=0.35, start=(760, 420), prewarm=prewarm('Régua de Gases'), setup=SETUP_INICIO)
    PSI = {'label': 'Pressão em PSI (g)', 'exact': True}
    KNOB = SEL('[role=slider] div.border-primary')
    CHAMA = SEL('button[aria-label="Levemente inflamável (A2L)"]')   # dentro do gatilho do select: fora da árvore de acessibilidade (sem role)
    c.mark(1)
    c.click(NAV('Régua de Gases'), at=0.2, label='abre a Régua de Gases')
    c.waitfor(text='Pressão de saturação dos refrigerantes por temperatura.', timeout=15)
    c.hover(KNOB, 1.2, at=c.A(1, 'Começo', 0.9), label='a régua em 5 °C (R-410A)')
    c.hover(PSI, 0.8, at=c.A(1, 'cento', 0.8), label='121 psi no campo da pressão')
    c.mark(2)
    c.type(PSI, '150', at=c.A(2, 'digito', 1.2), label='digita 150 psi', clear=True, cps=7)
    c.hover({'label': 'Temperatura em graus Celsius', 'exact': True}, 0.3, at=c.A(2, 'temperatura', 0.6), label='a temperatura acompanha')
    c.drag(KNOB, {'x': 768, 'y': 540}, at=c.A(2, 'arrasto', 1.4), label='arrasta a régua')
    c.hover(PSI, 0.6, at=c.A(2, 'campos', 0.8), label='os dois campos se ajustam')
    c.mark(3)
    c.click(BTN('bar'), at=c.A(3, 'bar', 0.9), label='Unidade: bar')
    c.mark(4)
    c.select(COMBO(0), 'R-404A', at=c.A(4, 'quatrocentos', 1.7), label='Gás: R-404A')
    c.click(BTN('Dew'), at=c.A(4, 'vapor', 0.9), label='Fórmula: vapor (Dew)')
    c.click(BTN('Bubble'), at=c.A(4, 'líquido,', 0.9), label='Fórmula: líquido (Bubble)')
    c.click(BTN('Dew'), at=c.A(4, 'conforme', 0.3), label='volta para vapor (Dew)')
    c.click(COMBO(0), at=c.L(5) - 1.4, label='abre a lista de gases')
    c.mark(5)
    c.click({'role': 'option', 'name': 'R-32'}, at=c.L(5), label='Gás: R-32')
    c.hover(CHAMA, 3.0, at=c.A(5, 'passando', 0.9), label='o ícone de chama do R-32 (passa o mouse)')
    c.fim()
    return c


def cap12():
    c = Cap(12, pace=0.5, start=(760, 420), prewarm=prewarm('Retrofit de Gás'), setup=SETUP_INICIO)
    c.mark(1)
    c.click(NAV('Retrofit de Gás'), at=0.2, label='abre o Retrofit de Gás')
    c.waitfor(text='Gases drop-in para trocar o refrigerante direto na mesma máquina.', timeout=15)
    c.select(COMBO(0), 'R-22', at=c.A(1, 'Gás', 1.3, nth=1), label='Gás atual: R-22')
    c.hover(P('Mais indicado'), 2.0, at=c.A(1, 'selo', 0.9), label='o selo Mais indicado no R-438A (MO99)')
    c.mark(2)
    c.scroll(by=300, at=c.L(2) - 0.6, label='desce até as opções', duration=0.9)
    c.hover(TXT('Óleo', within='main'), 0.4, at=c.A(2, 'óleo,', 0.8), label='Óleo')
    c.hover(TXT('Cuidados', within='main'), 0.4, at=c.A(2, 'cuidados', 0.8), label='Cuidados')
    c.hover(P('Pressão de trabalho'), 0.4, at=c.A(2, 'pressão', 0.8), label='Pressão de trabalho')
    c.click(BTN('bar'), at=c.A(2, 'bar.', 1.1), label='Unidade: bar')
    c.click(BTN('psi'), at=c.A(2, 'bar.', 0.1), label='volta para psi')
    c.mark(3)
    c.hover(P('é a troca de gás no mesmo equipamento'), 6.0, at=c.L(3) + 0.8, label='a nota Drop-in')
    c.scroll(by=-300, at=c.A(3, 'compressor.', 1.2), label='volta ao topo (Gás atual)', duration=0.8)
    c.select(COMBO(0), 'R-404A', at=c.A(3, 'Mudando', 0.4), label='Gás atual: R-404A')
    c.fim()
    return c


def cap13():
    c = Cap(13, pace=0.5, start=(760, 420), prewarm=prewarm('Superaquecimento', 'Ciclo de Refrigeração'), setup=SETUP_INICIO)
    c.mark(1)
    c.click(NAV('Superaquecimento'), at=c.A(1, 'Superaquecimento', 1.3), label='abre o Superaquecimento')
    c.waitfor(text='Ver o ciclo de refrigeração', timeout=15)
    c.click(SEL('main button', hasText='Ver o ciclo de refrigeração'), at=c.A(1, 'Ver', 1.0), label='link Ver o ciclo de refrigeração')
    c.waitfor(text='Ciclo Básico de Refrigeração', timeout=15)
    c.hover(NAV('Ciclo de Refrigeração'), 0.5, at=c.A(1, 'menu', 0.9), label='também pelo menu')
    c.hover(BTN('Ilustração'), 0.4, at=c.A(1, 'Ilustração', 0.8), label='a Ilustração animada do ciclo')
    for palavra, texto, nome in [('compressor,', 'COMPRESSOR', 'compressor'), ('condensador,', 'CONDENSADOR', 'condensador'),
                                 ('válvula', 'VÁLVULA DE EXPANSÃO', 'válvula de expansão'), ('evaporador.', 'EVAPORADOR', 'evaporador')]:
        c.hover(SEL('main svg text', hasText=texto), 0.4, at=c.A(1, palavra, 0.7), label=f'o {nome} na ilustração')
    c.mark(2)
    c.click(BTN('Imagem 2D'), at=c.A(2, 'Imagem', 0.9), label='Imagem 2D')
    c.click(BTN('Ilustração'), at=c.A(2, 'parado.', 1.0), label='volta para a Ilustração')
    c.scroll(TXT('Termos do ciclo', within='main'), at=c.A(2, 'Termos', 1.3), label='rola até os Termos do ciclo')
    c.click(SEL('main button', hasText='Compressor'), at=c.A(2, 'componente', 0.9), label='abre o termo Compressor')
    c.click(SEL('main button', hasText='Evaporador'), at=c.A(2, 'exemplo', 0.9), label='abre o termo Evaporador')
    c.fim()
    return c


def cap14():
    c = Cap(14, pace=0.5, start=(760, 420), prewarm=prewarm('Diluição de Produto'), setup=SETUP_INICIO)
    c.mark(1)
    c.click(NAV('Diluição de Produto'), at=0.0, label='abre a Diluição de Produto')
    c.waitfor(text='Quanto de produto e de água para chegar no volume desejado.', timeout=15)
    c.scroll(by=200, at=4.0, label='desce: campos e resultado juntos', duration=0.9)
    c.hover(BTN('Preparar solução'), 0.4, at=c.A(1, 'Preparar', 0.8), label='Modo de Diluição: Preparar solução')
    c.type({'placeholder': '10', 'exact': True}, '10', at=c.A(1, 'proporção', 1.2), label='proporção 1 para 10', clear=True, cps=7)
    c.type({'placeholder': 'Ex: 500', 'exact': True}, '500', at=c.A(1, 'final.', 1.2), label='volume final 500 mL', cps=7)
    c.hover(P('Produto', nth=0), 2.0, at=c.A(1, 'quarenta', 0.9), label='45,45 mL de produto')
    c.hover(P('Água', nth=0), 2.4, at=c.A(1, 'quatrocentos', 0.9), label='454,55 mL de água')
    c.mark(2)
    c.hover({'role': 'img', 'name': 'Galão com'}, 1.4, at=c.L(2), label='o galão desenhado mostra a proporção')
    c.hover(BTN('mL'), 1.0, at=c.A(2, 'mililitros', 0.8), label='a chave de Unidade: mL / L (sem trocar)')
    c.mark(3)
    c.click(BTN('Tenho X de produto'), at=c.A(3, 'Tenho', 0.9), label='modo Tenho X de produto')
    c.type({'placeholder': 'Ex: 50', 'exact': True}, '50', at=c.A(3, 'diz', 1.2), label='50 mL de produto', cps=7)
    c.hover(P('Água a adicionar'), 1.0, at=c.A(3, 'adicionar.', 0.9), label='Água a adicionar')
    c.fim()
    return c


def cap15():
    """Recapitulando: base simples (o Início da Área do Técnico, com o cursor passando pelos cartões na ordem em que a fala os cita);
    os trechos da recapitulação entram na edição (montagem rápida a partir dos outros capítulos)"""
    c = Cap(15, pace=0.4, start=(760, 420), prewarm=PREWARM_AT, setup=SETUP_INICIO)
    c.mark(1)
    c.hover(BADGE('Refrigeração e Climatização'), 1.4, at=c.A(1, 'segmento', 0.9), label='o selo do segmento')
    c.hover(CARD('Catálogo'), 1.4, at=c.A(1, 'Catálogo,', 0.9), label='o Catálogo')
    c.mark(2)
    for palavra, nome in [('carga', 'Carga Térmica'), ('conversão,', 'Conversão'), ('capacitor,', 'Cálculo de Capacitor'),
                          ('cabo', 'Cabo Elétrico'), ('superaquecimento', 'Superaquecimento'), ('régua', 'Régua de Gases'),
                          ('retrofit.', 'Retrofit de Gás')]:
        c.hover(CARD(nome), 0.3, at=c.A(2, palavra, 0.7), label=f'cartão {nome}')
    c.mark(3)
    c.hover(CARD('Ciclo de Refrigeração'), 0.5, at=c.A(3, 'ciclo', 0.8), label='cartão Ciclo de Refrigeração')
    c.hover(CARD('Diluição de Produto'), 0.5, at=c.A(3, 'diluição', 0.8), label='cartão Diluição de Produto')
    c.mark(4)
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
