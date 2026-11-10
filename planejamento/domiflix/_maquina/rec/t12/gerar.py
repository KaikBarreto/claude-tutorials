#!/usr/bin/env python3
"""T12 · gera rec/t12/cap00..cap11.json (roteiros do robô) a partir da voz pronta (t12/narracao/capNN.json).

Portal do Cliente e Portal do Contrato, no COMPUTADOR (janela 1280x800, 2x), Dominex 1.38.19, FAKE_NOW 2026-11-10T10:00:00-03:00.
Logada como Camila Duarte (admin, Glacial Cold Brasil) nos capítulos 0, 1, 4 a 8 e 11; "vista como o cliente" (sem sessão,
`anonymous`) nos capítulos 2, 3, 9 e 10; o capítulo 5 começa logado e passa para público no meio (limpa o localStorage e recarrega).
Gravar SEMPRE com APP_ORIGIN=https://www.dominex.app (o link do portal e o do contrato saem com o domínio real) e FAKE_URL da porta 54327.
Os `at` saem da palavra que anuncia cada passo (A(linha, palavra, folga)): o gesto "pousa" ~0,7 a 1 s depois do início do passo.
Rodar de qualquer pasta: `python3 -I rec/t12/gerar.py [NN ...]`. Depois: `node rec/record.mjs rec/t12/capNN.json --check`.

Estado de cada capítulo (cadeia.json): 0-3 partem de `inicio`; 4-7 de `apos-cap03` (chamado do hotel); 8 de `apos-cap07` ("Cobranças"
oculto); 9-11 de `apos-cap08` (documentos liberados). O aviso "Você tem N chamados" do Dashboard só aparece no cap. 4 (os outros
levam a marca `dominex:portal-tickets-seen`). A trilha Domiflix entra com `is_onboarding: false` (G1, em `inicio`): sem tela escura.

Particularidades (lições deste tutorial, docs/08-licoes.md):
 - Link do portal na tela: com APP_ORIGIN o campo mostra https://www.dominex.app/portal/<token>.
 - Nada de clique que abre outra aba, baixa arquivo ou chama aplicativo: "Abrir portal", "Abrir link", "Imprimir QR Code", "Baixar PDF",
   "Ligar", "WhatsApp", "E-mail", "Acompanhar" e "Ver relatório" só levam o cursor (hover).
 - A janela "Abrir Chamado" do portal tem o seletor do equipamento em "Nenhum" (não "Selecione...").
"""
import json, os, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
NARR = os.path.normpath(os.path.join(HERE, '..', '..', 't12', 'narracao'))
CAD = json.load(open(os.path.join(HERE, 'cadeia.json'), encoding='utf8'))
BASE = CAD['inicio']
APOS = CAD['apos']
HOTEL = CAD['hotel']
COLEGIO = CAD['colegio']
CONTRATO_HOTEL = '34306a37-c1a7-58a1-b713-244525163500'
# localStorage de partida de todo capítulo (menos o 4): o aviso "Você tem N chamado(s) de cliente aguardando" (Dashboard) já foi visto
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

NOMES = ['Abertura', 'O link de cada cliente', 'O que o hotel vê', 'O cliente abre um chamado', 'Onde o chamado cai',
         'O QR Code do equipamento', 'O link da unidade', 'Quem vê o quê', 'Os documentos no portal', 'A página da unidade',
         'Qual link mandar', 'Recapitulando']

def norm(s):
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode().lower()
    return ''.join(ch for ch in s if ch.isalnum() or ch in '?')


class Cap:
    def __init__(s, n, pace=0.5, cps=9, start=(760, 420), prewarm=None, setup=None, user=None, anonymous=False, same_tab=False, apos=None, storage=True):
        s.n = n
        d = json.load(open(f'{NARR}/cap{n:02d}.json', encoding='utf8'))
        s.words, s.linhas, s.dur = d['words'], d['linhas'], d['dur']
        s.steps = []
        s.pace, s.cps, s.start = pace, cps, start
        s.prewarm = prewarm or ['/dashboard']
        s.setup = list(setup or []) + [{'do': 'eval', 'js': OBS}]
        s.anchors = []
        s.pending = []
        s.user = user
        s.anonymous, s.same_tab, s.apos, s.storage = anonymous, same_tab, apos, storage

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
        s.steps.append({'do': 'eval', 'js': 'JSON.stringify(window.__avisos || "sem observador")', 'label': 'avisos de erro na tela'})
        s.steps.append({'do': 'mark', 'name': 'FIM', 'at': round(s.dur, 2)})

    def out(s):
        # estado de partida do capítulo: o fim do capítulo anterior que mudou o mundo (3: chamado; 7: cobranças oculto; 8: documentos)
        seed = list(BASE) + ([s.apos] if s.apos else [])
        d = {
            'name': f't12-cap{s.n:02d}',
            'title': f'T12 · Cap. {s.n} · {NOMES[s.n]} (narração {str(round(s.dur, 1)).replace(".", ",")} s; marcas L1..L{len(s.linhas)} = início de cada linha do roteiro)',
            'seed': f't12-cap{s.n:02d}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
            'start': {'x': s.start[0], 'y': s.start[1]},
            'seedExtra': seed,
            'prewarm': s.prewarm, 'setup': s.setup, 'steps': s.steps,
            'storage': dict(STORAGE) if s.storage else {},
        }
        if s.anonymous:
            d['anonymous'] = True
        if s.same_tab:
            d['sameTab'] = True
        if s.user:
            d['user'] = s.user
        return d


# ---------------------------------------------------------------- alvos
BTN = lambda n, **kw: {'role': 'button', 'name': n, 'exact': True, **kw}
BTNX = lambda n, **kw: {'role': 'button', 'name': n, **kw}               # nome por substring
LINK = lambda n: {'role': 'link', 'name': n, 'exact': True}
TAB = lambda n, **kw: {'role': 'tab', 'name': n, 'exact': True, **kw}
ITEM = lambda n: {'role': 'menuitem', 'name': n, 'exact': True}
SW = lambda n: {'role': 'switch', 'name': n, 'exact': True}
TXT = lambda t, **kw: {'text': t, 'exact': True, **kw}                   # texto INTEIRO igual
P = lambda t, **kw: {'text': t, **kw}                                    # texto por substring, sem diferenciar caixa
SEL = lambda s, **kw: {'selector': s, **kw}
DLG = '[role=dialog]'
# portal do cliente / da unidade (sem sessão): botões do menu lateral e cartões
MENU = lambda n: {'role': 'button', 'name': n, 'exact': True}
# "Quem vê o quê": linha da seção (grupo com aria-label) e pílula Oculto / Sem senha / Com senha
GRUPO = lambda sec: {'role': 'group', 'name': sec, 'exact': True}
PILULA = lambda sec, op: {'selector': f"[role=group][aria-label='{sec}'] button", 'hasText': op}
SECOES = ['Visão geral', 'Equipamentos', 'Cronograma', 'Ocorrências', 'Documentos', 'Histórico', 'Histórico PMOC', 'Cobranças']

# ---------------------------------------------------------------- trechos comuns (não filmados, no `setup`)
SETUP_APP = lambda rota, esperar: [
    {'do': 'goto', 'url': rota}, {'do': 'waitFor', 'text': esperar, 'timeout': 25}, {'do': 'waitFor', 'idle': True}]
SETUP_DASH = SETUP_APP('/dashboard', 'Olá, Camila!')
PORTAL_HOTEL = f"/portal/{HOTEL['portal_token']}"
PORTAL_COLEGIO_EQ = f"/portal/{COLEGIO['portal_token']}?eq={COLEGIO['hiwall']}"
UNIDADE_HOTEL = f"/contrato/unidade/pmoc-hotel-mirante-do-mar-{HOTEL['codigo_contrato']}"
SETUP_PORTAL = SETUP_APP(PORTAL_HOTEL, 'Olá, Hotel Mirante do Mar')
SETUP_FICHA = SETUP_APP(f"/clientes/{HOTEL['cliente']}", 'Informações')
SETUP_CONTRATO = SETUP_APP(f'/contratos/{CONTRATO_HOTEL}', 'Portal do Contrato')
PREWARM_APP = ['/dashboard', '/clientes', '/contratos', '/ordens-servico']
FICHA_ABAS = ['Geral', 'Equipamentos', 'Histórico', 'Tarefas', 'Estoque', 'Chamados', 'Contratos', 'Documentos', 'Financeiro', 'Cobranças']


# ================================================================ capítulos
def cap00():
    """Abertura: do Dashboard para a ficha do Hotel Mirante do Mar; a câmera percorre as abas e para em "Chamados"."""
    c = Cap(0, pace=0.5, start=(760, 420), prewarm=PREWARM_APP + [f"/clientes/{HOTEL['cliente']}"], setup=SETUP_DASH)
    c.mark(1)
    c.click(BTN('Gestão'), at=0.3, label='grupo Gestão do menu')
    c.click(LINK('Clientes e Fornecedores'), at=4.7, label='menu Clientes e Fornecedores')
    c.waitfor(text='Lista de Clientes', timeout=15)
    c.click(TXT('Hotel Mirante do Mar', within='main'), at=8.7, label='abre a ficha do Hotel Mirante do Mar')
    c.waitfor(target=TAB('Chamados'), timeout=15)
    c.mark(2)
    t0 = c.A(2, 'dois', 0.2)
    for i, aba in enumerate(['Geral', 'Equipamentos', 'Histórico', 'Contratos', 'Documentos', 'Financeiro']):
        c.hover(TAB(aba), 0.1, at=round(t0 + i * 1.15, 2), label=f'aba {aba} da ficha')
    c.click(TAB('Chamados'), at=c.A(2, 'chamados', 0.7), label='para na aba Chamados')
    c.mark(3)
    c.fim()
    return c


def cap01():
    """O link de cada cliente: Ações > Editar > aba Portal (chave, link, senha, o que o cliente vê), Cancelar, Copiar link do portal."""
    c = Cap(1, pace=0.5, start=(760, 420), prewarm=PREWARM_APP, setup=SETUP_FICHA)
    LINHA = lambda nome: TXT(nome, within=DLG)
    c.mark(1)
    c.click(BTN('Ações'), at=c.A(1, 'Ações,', 2.1), label='botão Ações da ficha')
    # o 1º clique em Ações logo depois de carregar a ficha não abre o menu (medido, 04/11): 2º clique só se o menu ainda não abriu
    c.pause(0.6)
    c.click(BTN('Ações'), label='Ações de novo (só se o menu não abriu)', unless=ITEM('Editar'))
    c.click(ITEM('Editar'), at=c.A(1, 'Editar,', 1.3), label='Editar no menu Ações')
    c.click(TAB('Portal'), at=c.A(1, 'aba', 0.9), label='aba Portal da janela Editar Cliente')
    c.mark(2)
    c.hover(SW('Portal ativo'), 2.4, at=c.A(2, 'Portal', 0.8), label='chave Portal ativo')
    c.hover(SEL(f'{DLG} input:not([type=checkbox])'), 2.6, at=c.A(2, 'Link', 0.8), label='campo Link do portal')
    c.mark(3)
    c.click(SW('Exigir senha para entrar'), at=c.A(3, 'Exigir', 1.0), label='liga Exigir senha para entrar')
    c.hover({'label': 'Senha', 'exact': True, 'within': DLG}, 0.6, at=c.A(3, 'campos', 0.4), label='campo Senha')
    c.hover({'label': 'Confirmar senha', 'exact': True, 'within': DLG}, 0.6, at=c.A(3, 'Confirmar', 0.9), label='campo Confirmar senha')
    c.hover(SEL(f'{DLG} button', hasText='Oculto'), 2.4, at=c.A(3, 'ganha', 0.9), label='opções Oculto, Sem senha e Com senha de uma seção')
    c.mark(4)
    c.hover(SEL(f'{DLG} button', hasText='Sem senha'), 1.5, at=c.A(4, 'proteger', 0.8), label='as três opções de Ordens de serviço')
    c.click(SW('Exigir senha para entrar'), at=c.A(4, 'desligo', 2.0), label='desliga Exigir senha para entrar')
    c.mark(5)
    c.scroll(by=420, point={'x': 640, 'y': 450}, at=c.A(5, 'Embaixo,', 1.0), label='desce até O que o cliente pode ver', duration=0.8)
    for palavra, nome in [('Ordens', 'Ordens de serviço'), ('Equipamentos,', 'Equipamentos'), ('Contratos,', 'Contratos'), ('Cobranças,', 'Cobranças'),
                          ('Notas', 'Notas fiscais'), ('Documentos', 'Documentos'), ('Abrir', 'Abrir chamados')]:
        c.hover(LINHA(nome), 0.2, at=c.A(5, palavra, 0.7), label=f'linha {nome} de O que o cliente pode ver')
    c.mark(6)
    c.click(BTN('Cancelar'), at=c.A(6, 'Cancelar', 0.9), label='Cancelar (fecha sem salvar)')
    c.click(BTN('Ações'), at=c.A(6, 'abro', 0.9), label='abre Ações de novo')
    c.pause(0.6)
    c.click(BTN('Ações'), label='Ações de novo (só se o menu não abriu)', unless=ITEM('Copiar link do portal'))
    c.click(ITEM('Copiar link do portal'), at=c.A(6, 'Copiar', 0.9), label='Copiar link do portal')
    c.fim()
    return c


def cap02():
    """O que o hotel vê: portal do cliente SEM sessão. Menu, ordens (com a busca e a página 2), equipamentos, contratos, Falar com a empresa."""
    c = Cap(2, pace=0.4, start=(760, 420), prewarm=PREWARM_APP, setup=SETUP_PORTAL, anonymous=True)
    c.mark(1)
    c.hover(TXT('Glacial Cold Brasil'), 1.0, at=c.A(1, 'nome', 0.8), label='nome da empresa no alto')
    c.hover(TXT('Olá, Hotel Mirante do Mar'), 2.0, at=c.A(1, 'saudação:', 0.9), label='saudação Olá, Hotel Mirante do Mar')
    c.mark(2)
    c.hover(MENU('Ordens de Serviço'), 0.1, at=c.A(2, 'Ordens', 0.8), label='menu Ordens de Serviço')
    c.hover(MENU('Equipamentos'), 0.1, at=c.A(2, 'Equipamentos', 0.8), label='menu Equipamentos')
    c.hover(MENU('Contratos'), 0.1, at=c.A(2, 'Contratos.', 0.8), label='menu Contratos')
    c.mark(3)
    c.hover(SEL('main p', hasText='Visita 12'), 1.2, at=c.A(3, 'ordens', 0.8, nth=1), label='as visitas do PMOC na lista de ordens')
    c.hover({'placeholder': 'Buscar ordens de servico...'}, 0.5, at=c.A(3, 'buscar.', 0.9), label='campo de busca das ordens')
    c.click(BTN('Próxima'), at=c.A(3, 'caminho', 1.0), label='página 2 da lista (onde está a ordem A caminho)')
    c.hover(BTN('Acompanhar'), 2.2, at=c.A(3, 'Acompanhar.', 1.3), label='botão Acompanhar da ordem A caminho (sem clicar)')
    c.mark(4)
    c.click(MENU('Equipamentos'), at=c.A(4, 'Equipamentos,', 0.8), label='clica em Equipamentos')
    for i, (palavra, nome) in enumerate([('quatro', 'Cassete 36.000 BTUs - Lobby'), ('aparelhos', 'Cassete 36.000 BTUs - Restaurante do hotel'),
                                         ('hotel,', 'Hi-Wall 12.000 BTUs - Recepção'), ('cada', 'Piso-Teto 48.000 BTUs - Salão de eventos')]):
        c.hover(TXT(nome), 0.2, at=c.A(4, palavra, 0.7), label=f'equipamento {nome}')
    c.mark(5)
    c.click(MENU('Contratos'), at=c.A(5, 'Contratos,', 0.8), label='clica em Contratos')
    c.hover(TXT('PMOC - Hotel Mirante do Mar'), 1.4, at=c.A(5, 'PMOC', 0.8), label='linha do contrato PMOC - Hotel Mirante do Mar')
    c.hover(TXT('PMOC', within='main'), 1.4, at=c.A(5, 'selo', 0.9), label='selo PMOC')
    c.mark(6)
    c.click(BTN('Falar com a empresa'), at=c.A(6, 'Falar', 0.9), label='Falar com a empresa', noScroll=True)
    c.hover(TXT('Ligar', within=DLG), 0.1, at=c.A(6, 'Ligar,', 0.8), label='Ligar (sem clicar)')
    c.hover(TXT('WhatsApp', within=DLG), 0.1, at=c.A(6, 'WhatsApp', 0.8), label='WhatsApp (sem clicar)')
    c.hover(TXT('E-mail', within=DLG), 0.1, at=c.A(6, 'E-mail,', 0.7), label='E-mail (sem clicar)')
    c.press('Escape', at=c.A(6, 'contatos', 0.0), label='fecha o Falar com a empresa')
    c.mark(7)
    c.hover(BTN('Abrir Chamado'), 2.6, at=c.A(7, 'Abrir', 0.9), label='botão fixo Abrir Chamado')
    c.fim()
    return c


def cap03():
    """O cliente abre um chamado: janela Abrir Chamado, texto, equipamento (o seletor mostra "Nenhum"), Enviar; a OS nova no topo, Pendente."""
    c = Cap(3, pace=0.4, start=(760, 420), prewarm=PREWARM_APP, setup=SETUP_PORTAL, anonymous=True)
    DESC = 'O ar do restaurante está pingando água perto da janela.'
    c.mark(1)
    c.click(BTN('Abrir Chamado'), at=c.A(1, 'Abrir', 0.9), label='Abrir Chamado')
    c.waitfor(text='Descreva o problema', timeout=10)
    c.mark(2)
    c.type({'placeholder': 'Descreva o problema que você está enfrentando...'}, DESC, at=c.A(2, 'escreve', 1.3), cps=15, label='digita a descrição do chamado')
    c.mark(3)
    c.click(SEL(f'{DLG} button[role=combobox]'), at=c.A(3, 'escolhe', 0.9), label='abre a lista de Equipamento (opcional)')
    c.click({'role': 'option', 'name': 'Cassete 36.000 BTUs - Restaurante do hotel'}, at=c.A(3, 'Cassete', 1.0), label='escolhe o Cassete 36.000 BTUs do restaurante')
    c.mark(4)
    c.click(BTN('Enviar Chamado'), at=c.A(4, 'Enviar', 0.9), label='Enviar Chamado')
    c.waitfor(text=DESC, timeout=15)
    c.hover(TXT(DESC), 2.8, at=c.A(4, 'ordem', 0.9), label='a ordem nova no topo da lista, Pendente')
    c.mark(5)
    c.hover(TXT(DESC), 4.5, at=c.A(5, 'chamado', 1.0), label='o cartão do chamado: número, descrição e o selo Pendente')
    c.fim()
    return c


def cap04():
    """Onde o chamado cai: Dashboard (aviso com os 2 chamados) > Ver chamados > aba Chamados > filtros > OS > Kanban > ficha do cliente."""
    setup = SETUP_APP('/clientes', 'Lista de Clientes')
    c = Cap(4, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/ordens-servico', '/clientes'], setup=setup, apos=APOS['3'], storage=False)
    c.mark(1)
    c.click(LINK('Dashboard'), at=c.A(1, 'Dashboard,', 1.0), label='abre o Dashboard')
    c.waitfor(text='chamados de cliente aguardando', timeout=15)
    c.hover(TXT('Ver chamados', within=DLG), 0.4, at=c.A(1, 'dois:', 0.9), label='a janela Você tem 2 chamados de cliente aguardando')
    c.mark(2)
    c.click(BTN('Ver chamados'), at=c.A(2, 'Ver', 0.9), label='Ver chamados')
    c.waitfor(text='Chamados abertos', timeout=15)
    c.hover(SEL('main tbody tr', hasText='Hotel Mirante do Mar'), 1.6, at=c.A(2, 'hotel.', 0.9), label='a linha do chamado do hotel')
    for palavra, alvo in [('ordem,', 'Pendente')]:
        c.hover(TXT(alvo, within='main'), 0.8, at=c.A(2, 'status.', 0.9), label='o status Pendente do chamado')
    c.mark(3)
    c.hover(TXT('Chamados abertos', within='main'), 1.2, at=c.A(3, 'abertos', 0.9), label='filtro Chamados abertos')
    c.click(SEL('main button[role=combobox]', nth=1), at=c.A(3, 'portal', 0.9), label='abre o filtro Todos os portais')
    c.press('Escape', at=c.A(3, 'veio,', 0.2), label='fecha o filtro')
    c.mark(4)
    c.click(SEL('main tbody tr', hasText='Hotel Mirante do Mar'), at=c.A(4, 'Clicando', 0.9), label='abre a ordem do chamado')
    c.hover(BTN('Editar', within=DLG), 2.2, at=c.A(4, 'Editar,', 1.0), label='botão Editar da ordem (sem clicar)')
    c.press('Escape', at=c.A(4, 'Serviço.', 0.4, nth=1), label='fecha a ordem')
    c.mark(5)
    c.click(TAB('Ordens de Serviço'), at=c.A(5, 'Kanban,', 0.9), label='aba Ordens de Serviço (Kanban)')
    c.hover(P('Chamados do Portal', within='main'), 2.2, at=c.A(5, 'Chamados', 1.0), label='coluna Chamados do Portal')
    c.mark(6)
    c.click(BTN('Gestão'), at=round(c.L(6) - 1.2, 2), label='grupo Gestão do menu')
    c.click(LINK('Clientes e Fornecedores'), at=round(c.L(6) - 0.0, 2), label='menu Clientes e Fornecedores')
    c.click(TXT('Hotel Mirante do Mar', within='main'), at=round(c.L(6) + 1.2, 2), label='ficha do Hotel Mirante do Mar')
    c.click(TAB('Chamados'), at=c.A(6, 'ficha', 0.4), label='aba Chamados da ficha do cliente')
    c.fim()
    return c


def cap05():
    """O QR Code do equipamento: ficha do Hi-Wall do Colégio (logada) e o portal do colégio aberto no aparelho (sem sessão)."""
    c = Cap(5, pace=0.5, start=(760, 420), prewarm=PREWARM_APP + [f"/equipamentos/{COLEGIO['hiwall']}"], setup=SETUP_DASH, apos=APOS['3'])
    c.mark(1)
    c.click(BTN('Gestão'), at=0.3, label='grupo Gestão do menu')
    c.click(LINK('Clientes e Fornecedores'), at=4.4, label='menu Clientes e Fornecedores')
    c.click(TXT('Colégio Monte Verde', within='main'), at=6.6, label='ficha do Colégio Monte Verde')
    c.click(TAB('Equipamentos'), at=8.1, label='aba Equipamentos da ficha')
    c.click(TXT('Hi-Wall 18.000 BTUs - Sala dos professores', within='main'), at=9.3, label='abre o Hi-Wall 18.000 BTUs da sala dos professores')
    c.hover(TXT('QR Code do equipamento', within='main'), 1.6, at=c.A(1, 'Colégio', 1.1), label='cartão QR Code do equipamento')
    c.mark(2)
    c.hover(BTN('Gerar Etiqueta'), 0.3, at=c.A(2, 'câmera', 0.7), label='botão Gerar Etiqueta')
    c.hover(BTN('Baixar QR (PNG)'), 0.3, at=c.A(2, 'QR', 0.7), label='botão Baixar QR (PNG)')
    c.hover(BTN('Abrir link'), 0.3, at=c.A(2, 'aparelho,', 0.7), label='botão Abrir link (sem clicar)')
    c.mark(3)
    c.click(BTN('Copiar link'), at=c.A(3, 'Copiar', 0.9), label='Copiar link do QR')
    c.mark(4)
    c.ev('JSON.stringify(window.__avisos || "sem observador")', label='avisos de erro na tela (1ª parte, logada)')
    # vira "o cliente": limpa a sessão e recarrega no link que o QR abre (mesma aba)
    c.ev("localStorage.clear(); sessionStorage.clear(); 1", at=c.A(4, 'escaneia.', 1.6), label='limpa a sessão (vira o cliente)')
    c.add({'do': 'goto', 'url': PORTAL_COLEGIO_EQ, 'reload': True, 'at': c.A(4, 'escaneia.', 1.3), 'label': 'abre o link do QR sem sessão'})
    c.waitfor(text='Visão geral', timeout=25)
    c.ev(OBS)
    c.hover(BTN('Visão geral'), 0.3, at=c.A(4, 'Visão', 0.8), label='aba Visão geral do aparelho')
    c.hover(TXT('Aerovento', within='main'), 1.0, at=c.A(4, 'Aerovento,', 0.8), label='a marca Aerovento')
    c.mark(5)
    c.click(BTN('Histórico'), at=c.A(5, 'Histórico,', 0.9), label='aba Histórico do aparelho')
    c.hover(SEL('main p', hasText='Ocorrência 1'), 1.4, at=c.A(5, 'inclusive', 0.8), label='as visitas do contrato no histórico')
    c.mark(6)
    c.click(BTN('Anexos'), at=c.A(6, 'Anexos,', 0.9), label='aba Anexos do aparelho')
    c.hover(P('Manual Aerovento AV-HW18.pdf'), 1.8, at=c.A(6, 'manual', 0.8), label='o anexo Manual Aerovento AV-HW18.pdf')
    c.mark(7)
    c.hover(BTN('Voltar para lista'), 0.3, at=c.A(7, 'Voltar', 0.8), label='botão Voltar para lista')
    c.click(BTN('Voltar para lista'), at=c.A(7, 'aparelhos', 0.9), label='Voltar para lista')
    c.fim()
    return c


def cap06():
    """O link da unidade: Gestão > Contratos > PMOC - Hotel Mirante do Mar > cartão Portal do Contrato (chave, QR, Copiar link, Imprimir QR)."""
    c = Cap(6, pace=0.5, start=(760, 420), prewarm=PREWARM_APP + [f'/contratos/{CONTRATO_HOTEL}'], setup=SETUP_DASH, apos=APOS['3'])
    c.mark(1)
    c.click(BTN('Gestão'), at=0.3, label='grupo Gestão do menu')
    c.click(LINK('Contratos'), at=4.2, label='menu Contratos')
    c.click(TXT('PMOC - Hotel Mirante do Mar', within='main'), at=7.6, label='abre o PMOC - Hotel Mirante do Mar')
    c.scroll(TXT('Portal do Contrato', within='main'), at=8.9, label='desce até o cartão Portal do Contrato', duration=1.2)
    c.mark(2)
    c.hover(SW('Portal Público'), 1.1, at=c.A(2, 'Portal', 0.9), label='chave Portal Público')
    c.hover(P('Qualquer pessoa com o link'), 2.4, at=c.A(2, 'qualquer', 0.9), label='texto Qualquer pessoa com o link vê o portal')
    c.mark(3)
    c.scroll(by=380, point={'x': 700, 'y': 450}, at=c.A(3, 'Aqui', 1.2), label='desce até o QR Code e o link da unidade', duration=0.8)
    c.click(BTN('Copiar link'), at=c.A(3, 'Copiar', 0.9), label='Copiar link da unidade')
    c.mark(4)
    c.hover(BTN('Imprimir QR Code'), 3.4, at=c.A(4, 'Imprimir', 0.9), label='botão Imprimir QR Code (sem clicar)')
    c.fim()
    return c


def cap07():
    """Quem vê o quê: as oito seções com Oculto / Sem senha / Com senha; Cobranças em Oculto; o aviso da senha e o atalho do cadastro."""
    setup = SETUP_CONTRATO + [{'do': 'eval', 'js': "document.evaluate(\"//*[normalize-space(text())='Quem vê o quê no portal']\", document, null, 9, null).singleNodeValue?.scrollIntoView({block: 'start'}); 1"},
                              {'do': 'wait', 'seconds': 0.5}]
    c = Cap(7, pace=0.5, start=(760, 420), prewarm=PREWARM_APP + [f'/contratos/{CONTRATO_HOTEL}'], setup=setup, apos=APOS['3'])
    c.mark(1)
    c.hover(TXT('Quem vê o quê no portal', within='main'), 1.4, at=c.A(1, 'Quem', 0.9), label='cartão Quem vê o quê no portal')
    c.hover(SEL('[role=group] button', hasText='Oculto'), 0.3, at=c.A(1, 'Oculto:', 0.8), label='opção Oculto')
    c.hover(SEL('[role=group] button', hasText='Sem senha'), 0.3, at=c.A(1, 'Sem', 0.8), label='opção Sem senha')
    c.hover(SEL('[role=group] button', hasText='Com senha'), 0.3, at=c.A(1, 'Com', 0.8), label='opção Com senha')
    c.mark(2)
    for palavra, nome, nth in [('Visão', 'Visão geral', 0), ('Equipamentos,', 'Equipamentos', 0), ('Cronograma,', 'Cronograma', 0), ('Ocorrências,', 'Ocorrências', 0),
                               ('Documentos,', 'Documentos', 0), ('Histórico,', 'Histórico', 0), ('Histórico', 'Histórico PMOC', 1), ('Cobranças.', 'Cobranças', 0)]:
        c.hover(GRUPO(nome), 0.1, at=c.A(2, palavra, 0.8, nth=nth), label=f'seção {nome}')
    c.mark(3)
    c.click(PILULA('Cobranças', 'Oculto'), at=c.A(3, 'Oculto,', 1.0), label='Cobranças em Oculto')
    c.mark(4)
    c.hover(P('Este cliente ainda não tem senha'), 2.6, at=c.A(4, 'Com', 0.9), label='aviso: o cliente ainda não tem senha no Portal do Cliente')
    c.hover(BTN('Abrir cadastro do cliente'), 2.4, at=c.A(4, 'Abrir', 0.9), label='botão Abrir cadastro do cliente (sem clicar)')
    c.mark(5)
    c.fim()
    return c


def cap08():
    """Os documentos no portal: aba Documentos do contrato; Liberar documentos no portal do cliente; selo Oculto > Liberado."""
    c = Cap(8, pace=0.5, start=(760, 420), prewarm=PREWARM_APP + [f'/contratos/{CONTRATO_HOTEL}'], setup=SETUP_CONTRATO, apos=APOS['7'])
    c.mark(1)
    c.click(TAB('Documentos'), at=c.A(1, 'aba', 0.9), label='aba Documentos do contrato')
    c.hover(TXT('Documentos no portal do cliente', within='main'), 1.4, at=c.A(1, 'cartão', 0.8), label='cartão Documentos no portal do cliente')
    c.hover(TXT('Oculto', within='main'), 1.2, at=c.A(1, 'selo', 0.9), label='selo Oculto')
    c.mark(2)
    c.click(BTN('Liberar documentos no portal do cliente'), at=c.A(2, 'Liberar', 1.0), label='Liberar documentos no portal do cliente')
    c.hover(TXT('Liberado', within='main'), 1.4, at=c.A(2, 'selo', 0.9), label='selo Liberado')
    c.hover(BTN('Ocultar documentos do portal'), 2.4, at=c.A(2, 'Ocultar', 0.9), label='botão Ocultar documentos do portal (sem clicar)')
    c.mark(3)
    for palavra, nome in [('Dossiê,', 'Dossiê PMOC'), ('Termo,', 'Termo de Responsabilidade Técnica'), ('Certificado', 'Certificado de Conformidade'), ('Cronograma', 'Planilha PMOC')]:
        c.hover(P(nome, within='main'), 0.2, at=c.A(3, palavra, 0.7), label=f'cartão {nome}')
    c.fim()
    return c


def cap09():
    """A página da unidade: link público do contrato, sem sessão; Visão Geral, Equipamentos, Cronograma, Ocorrências, Documentos, Histórico, rodapé."""
    setup = SETUP_APP(UNIDADE_HOTEL, 'Em dia')
    c = Cap(9, pace=0.4, start=(760, 420), prewarm=PREWARM_APP, setup=setup, apos=APOS['8'], anonymous=True)
    c.mark(1)
    c.hover(TXT('Plano de Manutenção'), 1.0, at=c.A(1, 'Plano', 0.9), label='subtítulo Plano de Manutenção')
    c.hover(TXT('Em dia'), 1.4, at=c.A(1, 'selo', 0.9), label='selo Em dia')
    c.mark(2)
    c.click(BTN('Visão Geral'), at=c.A(2, 'Visão', 0.8), label='aba Visão Geral')
    c.hover(P('Conforme Lei Federal 13.589/2018'), 1.2, at=c.A(2, 'conformidade', 0.9), label='conformidade com a lei')
    c.scroll(by=330, point={'x': 700, 'y': 450}, at=c.A(2, 'Embaixo,', 1.3), label='desce até o bloco Responsável Técnico', duration=0.8)
    c.hover(TXT('Responsável Técnico'), 2.6, at=c.A(2, 'Responsável', 0.9), label='bloco Responsável Técnico')
    c.mark(3)
    c.click(BTN('Equipamentos'), at=c.A(3, 'Equipamentos,', 0.8), label='aba Equipamentos')
    c.mark(4)
    c.click(BTN('Cronograma'), at=c.A(4, 'Cronograma,', 0.8), label='aba Cronograma')
    c.click(BTN('Próximo período'), at=c.A(4, 'Avanço', 0.9), label='Próximo período (o calendário abre em novembro; a primeira visita é em dezembro)')
    c.hover(P('Toque em uma manutenção do calendário'), 1.6, at=c.A(4, 'Quem', 0.9), label='dica do calendário')
    c.mark(5)
    c.click(BTN('Ocorrências'), at=c.A(5, 'Ocorrências,', 0.8), label='aba Ocorrências')
    c.hover(TXT('Agendada'), 1.4, at=c.A(5, 'Agendada.', 0.9), label='selo Agendada das visitas')
    c.mark(6)
    c.click(BTN('Documentos'), at=c.A(6, 'Documentos,', 0.8), label='aba Documentos')
    c.hover(P('Válido até'), 1.2, at=c.A(6, 'Válido', 0.9), label='Válido até dos documentos')
    c.hover(P('Baixar PDF'), 1.8, at=c.A(6, 'Baixar', 0.9), label='botão Baixar PDF (sem clicar)')
    c.mark(7)
    c.hover(BTN('Histórico'), 1.5, at=c.A(7, 'Histórico', 0.9), label='aba Histórico (sem clicar)')
    c.mark(8)
    c.scroll(by=900, point={'x': 700, 'y': 450}, at=round(c.L(8) - 1.0, 2), label='rola até o rodapé', duration=0.8)
    c.hover(BTN('Abrir chamado nesta unidade'), 3.0, at=c.A(8, 'Abrir', 0.5), label='botão Abrir chamado nesta unidade (sem clicar)')
    c.fim()
    return c


def cap10():
    """Qual link mandar: portal do cliente sem sessão, seção Contratos, clique na linha do PMOC (mesma aba); a ilustração entra na edição."""
    c = Cap(10, pace=0.5, start=(760, 420), prewarm=PREWARM_APP, setup=SETUP_PORTAL, apos=APOS['8'], anonymous=True, same_tab=True)
    c.mark(1)
    c.click(MENU('Contratos'), at=c.A(1, 'seção', 1.2), label='seção Contratos do portal')
    c.hover(TXT('PMOC - Hotel Mirante do Mar'), 0.4, at=c.A(1, 'Contratos.', 0.5), label='linha do contrato PMOC com o selo PMOC')
    c.click(TXT('PMOC - Hotel Mirante do Mar'), at=c.A(1, 'Clicando', 0.9), label='clica na linha do contrato (abre a página da unidade)')
    c.waitfor(text='Em dia', timeout=25)
    c.ev(OBS)
    c.mark(2)
    c.mark(3)
    c.fim()
    return c


def cap11():
    """Recapitulando: base simples (a ficha do hotel, com o cursor nas abas); os trechos da recapitulação entram na edição."""
    c = Cap(11, pace=0.4, start=(760, 420), prewarm=PREWARM_APP, setup=SETUP_FICHA, apos=APOS['8'])
    c.mark(1)
    c.hover(BTN('Ações'), 1.4, at=c.A(1, 'link', 0.9), label='o menu Ações da ficha')
    c.mark(2)
    c.hover(TAB('Chamados'), 1.4, at=c.A(2, 'Chamados.', 0.9), label='aba Chamados da ficha')
    c.mark(3)
    c.hover(TAB('Equipamentos'), 1.4, at=c.A(3, 'equipamento', 0.9), label='aba Equipamentos da ficha')
    c.mark(4)
    c.hover(TAB('Contratos'), 1.4, at=c.A(4, 'Contrato', 0.9), label='aba Contratos da ficha')
    c.mark(5)
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
