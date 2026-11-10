#!/usr/bin/env python3
"""T9 · gera rec/t9/cap00..cap16.json (roteiros do robô) a partir da voz pronta (t9/narracao/capNN.json).

Aula inteira no COMPUTADOR (janela 1280x800, 2x), logada como Camila Duarte (admin, Glacial Cold Brasil), na Dominex 1.38.19.
Os `at` saem da palavra que anuncia cada passo (A(linha, palavra, folga)): o gesto "pousa" ~0,7 a 1 s depois do início do passo
(clique = deslocamento + ~0,85 s; digitação = clique + texto), então `at` = início da palavra - folga.
Rodar de qualquer pasta: `python3 -I rec/t9/gerar.py [NN ...]`. Depois: `node rec/record.mjs rec/t9/capNN.json --check`.

Cadeia de sementes: rec/t9/cadeia.json (gerado por rec/t9/semear.py: fim do T5 + estoque do T8 + bastidor do T9 = `t9/inicio`) e, a cada
capítulo, o último `t9/apos-capNN` do capítulo anterior que mexeu no banco (SEMENTE abaixo). O `apos-capNN` de cada capítulo sai da gravação
(`rec/t9/snap.mjs diff NN`, na mesma trava da gravação).

Particularidades (lições deste tutorial, ver docs/08-licoes.md):
 - O aviso "Você tem 1 chamado de cliente aguardando" (Dashboard) sai por `storage` (marca de "visto" em localStorage), como no T18.
 - Rótulos em MAIÚSCULAS na tela (EM ABERTO, CONVERSÃO, STATUS...) são só CSS: o texto do DOM tem outra caixa (alvo por `hasText`/`text` sem `exact`).
 - O assistente "Novo Orçamento" (1.38.19: 3 etapas, a 1ª rola numa tela só) não guarda os itens: cada capítulo de cap06 a cap09 refaz, no `setup`
   (sem filmar), o que vem antes.
 - Observador `OBS` (como o T12): guarda em `window.__avisos` todo aviso de erro do app, tela escura e faixa da trilha Domiflix; o eval final do capítulo devolve.
 - O 2º clique em diante numa janela é rápido; o 1º clique de uma janela ou folha recém-aberta custa 0,9 a 2,1 s (folga >= 1,5 s).
"""
import json
import os
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TUT = os.path.normpath(os.path.join(HERE, '..', '..'))
NARR = os.path.join(TUT, 't9', 'narracao')
CAD = json.load(open(os.path.join(HERE, 'cadeia.json'), encoding='utf8'))
BASE = CAD['inicio']
TOKEN9 = CAD['token9']
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

NOMES = ['Abertura', 'A tela e as quatro abas', 'O BDI da empresa', 'O custo da Van 01', 'Quanto custa executar um serviço',
         'Primeira etapa: o destinatário', 'Segunda etapa: serviços e preço', 'Terceira etapa: materiais e deslocamento',
         'Quarta etapa: desconto e condições', 'Quinta etapa: validade e revisão', 'Configurar a proposta', 'Visualizar e gerar o link',
         'O que o cliente vê', 'Quem abriu a proposta', 'Aprovar por dentro', 'Gerar a ordem de serviço', 'Recapitulando']
# estado de partida de cada capítulo: o último apos-capNN (de capítulo anterior) que mexeu no banco
SEMENTE = {0: None, 1: None, 2: None, 3: 'apos-cap02', 4: 'apos-cap03', 5: 'apos-cap04', 6: 'apos-cap04', 7: 'apos-cap04', 8: 'apos-cap04',
           9: 'apos-cap04', 10: 'apos-cap09', 11: 'apos-cap10', 12: 'apos-cap11', 13: 'apos-cap12', 14: 'apos-cap12', 15: 'apos-cap14',
           16: 'apos-cap15'}


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
        s.prewarm = prewarm or ['/dashboard', '/orcamentos']
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
            raise SystemExit(f'cap{s.n:02d}: palavra "{palavra}" (#{nth}) não achada na linha {i}: ' + ' '.join(w['w'] for w in s.words if w['linha'] == i - 1))
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
            lim = 0.8 if d.get('do') == 'hover' else 0.25   # hover (só mostra) que começaria até 0,8 s antes da linha começa junto com ela
            for mt, mi in s.pending:  # passo que começaria até 0,25 s antes da linha começa junto com ela (a marca vem antes)
                if d['at'] < mt <= d['at'] + lim:
                    d['at'] = round(mt, 2)
            if d.get('do') == 'type':   # digitação longa que antecipa a linha: a marca entra antes dela, já no instante do passo
                for mt, mi in list(s.pending):
                    if d['at'] < mt <= d['at'] + 2.6:
                        s.steps.append({'do': 'mark', 'name': f'L{mi}', 'at': round(d['at'], 2)})
                        s.pending.remove((mt, mi))
            s.flush(d['at'])
        s.steps.append(d)
        return d

    def mark(s, i):
        t = max(0.0, s.L(i) - 0.9) if s.L(i) > 0.9 else s.L(i)   # a marca vale "o robô chegou à linha": passo que antecipa a fala (até 0,9 s) não a atrasa
        if t <= 0:
            s.steps.append({'do': 'mark', 'name': f'L{i}', 'at': 0})
        else:
            s.pending.append((t, i))

    def marcas(s):
        for i in range(1, len(s.linhas) + 1):
            s.mark(i)

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
                if at + 0.3 < mt < fim - 0.25:
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

    def rolar(s, by, at=None, label=None, ponto=(760, 420), duration=0.5, after=100):
        """roda do mouse sobre `ponto` (px CSS): ~1,1 s, sem a rolagem automática do robô (que leva 2,5 s)"""
        return s._p({'do': 'scroll', 'point': {'x': ponto[0], 'y': ponto[1]}, 'by': by, 'duration': duration, 'after': after}, at, label, {})

    def digitar_num(s, target, texto, at=None, label=None, **kw):
        """Campo `type=number` com 0 de partida (o app reescreve 0 ao apagar: "032"): clica, seleciona tudo (Ctrl+A) e digita POR CIMA, sem Backspace."""
        s._p({'do': 'click', 'target': target}, at, (label + ' (clique)') if label else None, dict(kw))
        s.add({'do': 'press', 'key': 'Control+A'})
        return s.add({'do': 'type', 'target': target, 'text': texto, 'noClick': True, 'label': label})

    def confere(s, escopo, esperados, label):
        """Passo `eval` que LÊ a tela e compara com o que a fala diz: devolve "OK: <trecho>" ou "DIFERENTE: <trecho lido> (faltou ...)".
        `escopo`: 'dlg' (a ÚLTIMA janela aberta, ex.: seletor de materiais), 'wiz' (a PRIMEIRA, o assistente), 'main', 'body' ou um seletor CSS. Comparação sem diferenciar caixa e com espaços normalizados.
        O resumo.py imprime o valor inteiro e acusa DIFERENTE (aceite da fase 1: os valores da tela batem com a fala).
        Tenta por até ~6,5 s (a tela termina de pintar depois do clique), então o ensaio rápido não acusa falso DIFERENTE."""
        sel = {'dlg': "[role=dialog]", 'wiz': "[role=dialog]", 'main': 'main', 'body': 'body'}.get(escopo, escopo)
        linha = escopo[4:] if escopo.startswith('row:') else None          # 'row:Pousada Brisa do Mar' = a linha da lista com esse texto
        if linha is not None:
            sel = 'main tbody tr'
        esp = [esperados] if isinstance(esperados, str) else list(esperados)
        js = ("(async()=>{const norm=t=>t.replace(/[\\s\\u00a0]+/g,' ').toLowerCase();const esp=%s;let out='';"
              "for(let i=0;i<22;i++){const els=[...document.querySelectorAll(%s)].filter(e=>!%s||e.innerText.includes(%s));const el=%s?els[els.length-1]:els[0];"
              "if(!el){out='DIFERENTE: sem elemento';}else{const t=norm(el.innerText);const falta=esp.filter(e=>!t.includes(norm(e)));"
              "if(!falta.length)return 'OK: '+esp.join(' | ');out='DIFERENTE: faltou '+JSON.stringify(falta)+' em: '+t.slice(0,260);}"
              "await new Promise(r=>setTimeout(r,300));}return out})()") % (json.dumps(esp, ensure_ascii=False), json.dumps(sel), 'true' if linha is not None else 'false', json.dumps(linha or ''), 'true' if escopo == 'dlg' else 'false')
        return s.add({'do': 'eval', 'js': js, 'label': 'confere ' + label})

    def abrir_menu(s, cliente, item, at=None, label=None):
        """"⋮" da linha: o 1º clique logo depois de carregar a lista pode não abrir o menu (T12); 2º clique só se o item esperado ainda não apareceu."""
        s.click(ACOES(cliente), at=at, label=label or f'menu ⋮ da linha de {cliente}')
        s.pause(0.6)
        return s.click(ACOES(cliente), label=f'menu ⋮ de {cliente} de novo (só se não abriu)', unless=ITEM(item))

    def pause(s, seconds):
        return s.add({'do': 'pause', 'seconds': seconds})

    def waitfor(s, **kw):
        return s.add({'do': 'waitFor', **kw})

    def drag(s, target, to, at=None, label=None, **kw):
        return s._p({'do': 'drag', 'target': target, 'to': to}, at, label, kw)

    def ev(s, js, at=None, label=None, **kw):
        return s._p({'do': 'eval', 'js': js}, at, label, kw)

    def clicar_fixo(s, alvo, ponto, js, at, label):
        """Botão FIXO fora da faixa y 96..730: o `click` do robô tentaria rolar em vão e atrasaria alguns segundos. Leva o cursor com
        `scroll by 0 point`, registra o retângulo do `alvo` (passo `type` sem clique) e clica por `eval`. `at` = instante do clique;
        o cursor parte 0,9 s antes. Molde do T5/T7/T18."""
        s._p({'do': 'scroll', 'point': {'x': ponto[0], 'y': ponto[1]}, 'by': 0, 'duration': 0.3, 'after': 0}, round(max(0.0, at - 0.9), 2), label + ' (cursor)', {})
        s.add({'do': 'type', 'target': alvo, 'text': '', 'noClick': True, 'label': label, 'optional': True, 'timeout': 4})
        return s._p({'do': 'eval', 'js': js}, round(at, 2), label + ' (clique)', {})

    def colar(s, texto, at, label):
        """Preenche o campo em foco de uma vez, como um "colar" (`execCommand('insertText')`, ~0,05 s); o valor fica no actions.json."""
        js = f"(() => {{ document.execCommand('insertText', false, {json.dumps(texto)}); const e = document.activeElement; return e && e.value; }})()"
        return s._p({'do': 'eval', 'js': js}, at, label, {})

    def fim(s):
        s.flush(1e9)
        s.steps.append({'do': 'eval', 'js': 'JSON.stringify(window.__avisos || "sem observador")', 'label': 'avisos de erro na tela'})
        s.steps.append({'do': 'mark', 'name': 'FIM', 'at': round(s.dur, 2)})

    def out(s):
        sem = SEMENTE[s.n]
        d = {
            'name': f't9-cap{s.n:02d}',
            'title': f'T9 · Cap. {s.n} · {NOMES[s.n]} (narração {str(round(s.dur, 1)).replace(".", ",")} s; marcas L1..L{len(s.linhas)} = início de cada linha do roteiro)',
            'seed': f't9-cap{s.n:02d}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
            'start': {'x': s.start[0], 'y': s.start[1]},
            'seedExtra': list(BASE) + ([f't9/{sem}'] if sem else []),
            'prewarm': s.prewarm, 'setup': s.setup, 'steps': s.steps,
            'storage': dict(STORAGE),
        }
        if s.user:
            d['user'] = s.user
        return d


# ---------------------------------------------------------------- alvos
BTN = lambda n, **kw: {'role': 'button', 'name': n, 'exact': True, **kw}
BTNX = lambda n, **kw: {'role': 'button', 'name': n, **kw}               # nome por substring ("Filtros" vira "Filtros, 1 ativo" com filtro ativo)
LINK = lambda n, **kw: {'role': 'link', 'name': n, 'exact': True, **kw}
TAB = lambda n, **kw: {'role': 'tab', 'name': n, 'exact': True, **kw}
TXT = lambda t, **kw: {'text': t, 'exact': True, **kw}                    # texto INTEIRO igual (e na mesma caixa)
P = lambda t, **kw: {'text': t, 'within': 'main', **kw}                   # texto por substring, sem diferenciar caixa
SEL = lambda s, **kw: {'selector': s, **kw}
DLG = '[role=dialog]'
PD = lambda t, **kw: {'text': t, 'within': DLG, **kw}                     # texto por substring DENTRO da janela aberta (assistente)
POP = '[data-radix-popper-content-wrapper]'
OPT = lambda n, **kw: {'role': 'option', 'name': n, **kw}
ITEM = lambda n, **kw: {'role': 'menuitem', 'name': n, **kw}
CARD = lambda nome: {'selector': 'main .grid > *', 'hasText': nome}      # cartões Em Aberto / Conversão / Ticket Médio
TH = lambda k: {'selector': 'main thead th', 'nth': k}                    # cabeçalho da lista: 0 Nº, 1 Cliente, 2 Data, 3 Custo, 4 Valor, 5 Margem, 6 Status
BUSCA = {'placeholder': 'Buscar por cliente, número ou telefone...'}
LINHA = lambda cliente: {'selector': 'main tbody tr', 'hasText': cliente}   # linha da lista de orçamentos
ACOES = lambda cliente: {'selector': f"main tbody tr:has-text('{cliente}') button[aria-label='Ações']"}   # "⋮" da linha
AGUARDA = {'do': 'waitFor', 'idle': True}
SW = lambda n, **kw: {'role': 'switch', 'name': n, 'exact': True, **kw}
I = lambda k, esc='main': {'selector': f'{esc} input', 'nth': k}          # k-ésimo campo (Precificação: 0 Imposto, 1 Adm., 2 Lucro, 3 km, 4 à vista, 5 parcelas)
DI = lambda ph, k=0: {'selector': f"{DLG} input[placeholder='{ph}']", 'nth': k}   # campo da janela pelo placeholder
ROLA_DLG = "(()=>{const d=document.querySelector('[role=dialog] .overflow-y-auto');if(!d)return 'sem rolagem';d.scrollTo({top:%s,behavior:'smooth'});return d.scrollHeight})()"

# ---------------------------------------------------------------- trechos comuns (não filmados, no `setup`)
SETUP_DASH = [{'do': 'goto', 'url': '/dashboard'}, {'do': 'waitFor', 'text': 'Olá, Camila!', 'timeout': 25}, AGUARDA]
MENU_LATERAL = {'role': 'button', 'name': 'Toggle Sidebar', 'nth': 0}
# menu lateral recolhido do cap. 1 em diante: aberto, a 1280 px o botão "Configurar Proposta" cobre a aba Precificação (cap. 0 mostra o recolhimento)
SETUP_LISTA = [{'do': 'goto', 'url': '/orcamentos'}, {'do': 'waitFor', 'text': 'Gerencie orçamentos, custos e precificação', 'timeout': 25}, AGUARDA,
               {'do': 'click', 'target': MENU_LATERAL}, {'do': 'pause', 'seconds': 0.8}]
LIMPA_RASCUNHO = {'do': 'eval', 'js': "(() => { try { sessionStorage.clear(); } catch (e) {} return 'sessionStorage limpo'; })()"}


def setup_aba(aba):
    """abre /orcamentos e vai para uma das abas do topo (sem filmar)"""
    return SETUP_LISTA + [{'do': 'click', 'target': TAB(aba)}, AGUARDA]


# Plano B do Esc: clicar o "Fechar" da janela por `eval` (instantâneo). Um `click` condicional no botão Fechar pode travar 30 s.
FECHAR_EVAL = r"""(() => { const d = document.querySelector('[role=dialog]'); if (!d) return 'ja fechada'; const b = [...d.querySelectorAll('button')].find((x) => [x.textContent, x.getAttribute('aria-label'), x.title].some((v) => /^\s*fechar\s*$/i.test(v || ''))); if (!b) return 'sem botao Fechar'; b.click(); return 'fechada pelo botao'; })()"""


def fechar_janela(c, at, espera=0.4):
    """Esc fecha a janela; se o Esc não bastar, o botão Fechar por `eval`. Termina com a janela fechada."""
    c.press('Escape', at=at, label='fecha a janela')
    c.add({'do': 'wait', 'seconds': espera})
    c.ev(FECHAR_EVAL, label='Fechar (se o Esc não fechou)')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)


# ================================================================ capítulos
def cap00():
    """Abertura: o Dashboard; o cursor desce pelo menu lateral, clica em "Orçamentos" e percorre as quatro abas."""
    c = Cap(0, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/orcamentos'], setup=SETUP_DASH)
    c.mark(1)
    c.hover(LINK('Agenda'), 0.1, at=0.2, label='o cursor desce pelo menu lateral')
    c.click(LINK('Orçamentos'), at=3.0, label='abre a tela Orçamentos')
    c.waitfor(text='Gerencie orçamentos, custos e precificação', timeout=20)
    c.mark(2)
    c.hover(TAB('Orçamentos'), 0.4, at=c.A(2, 'Primeiro', -0.6), label='aba Orçamentos')
    c.hover(TAB('Custos dos Serviços'), 0.4, at=c.A(2, 'calcular', 0.9), label='aba Custos dos Serviços')
    c.hover(TAB('Custos Globais'), 0.4, at=c.A(2, 'custos', 0.8), label='aba Custos Globais')
    c.hover(TAB('Precificação'), 0.4, at=c.A(2, 'Depois', 0.8), label='aba Precificação')
    c.hover({'selector': 'main h1'}, 1.0, at=c.A(2, 'aprova', 1.0), label='o título da tela Orçamentos')
    c.mark(3)
    c.click(MENU_LATERAL, at=c.A(3, 'Vamos', 0.9), label='recolhe o menu lateral (a tela ganha espaço)')
    c.pause(0.8)
    c.fim()
    return c


def cap01():
    """A tela e as quatro abas: abas, botões do topo, cartões, filtro por cartão, colunas da lista e busca."""
    c = Cap(1, pace=0.5, start=(760, 420), setup=SETUP_LISTA)
    c.mark(1)
    c.hover({'selector': 'main h1'}, 0.3, at=0.2, label='título Orçamentos')
    c.hover(TAB('Orçamentos'), 0.1, at=c.A(1, 'Orçamentos', 0.75), label='aba Orçamentos')
    c.hover(TAB('Custos dos Serviços'), 0.1, at=c.A(1, 'Custos', 0.75, nth=0), label='aba Custos dos Serviços')
    c.hover(TAB('Custos Globais'), 0.1, at=c.A(1, 'Custos', 0.75, nth=1), label='aba Custos Globais')
    c.hover(TAB('Precificação'), 0.1, at=c.A(1, 'Precificação', 0.8), label='aba Precificação')
    c.hover(TAB('Orçamentos'), 0.1, at=c.A(1, 'primeira', 0.7), label='a primeira aba é a lista')
    c.hover(BTN('Configurar Proposta'), 0.1, at=c.A(1, 'Configurar', 0.8), label='botão Configurar Proposta')
    c.hover(BTN('Novo Orçamento'), 0.4, at=c.A(1, 'Novo', 0.8), label='botão Novo Orçamento')
    c.mark(2)
    c.hover(CARD('Em Aberto'), 0.3, at=c.A(2, 'cartões', 0.6), label='cartão Em Aberto')
    c.hover(CARD('Em Aberto'), 0.6, at=c.A(2, 'Aberto', 0.7), label='cartão Em Aberto (soma dos enviados)')
    c.hover(CARD('Ticket Médio'), 0.5, at=c.A(2, 'Ticket', 0.8), label='cartão Ticket Médio')
    c.hover(CARD('Conversão'), 0.5, at=c.A(2, 'Conversão', 0.8), label='cartão Conversão')
    c.mark(3)
    c.click(CARD('Em Aberto'), at=c.A(3, 'Em', 0.9), label='clique no cartão Em Aberto')
    c.hover(CARD('Conversão'), 0.4, at=c.A(3, 'Conversão', 0.8), label='cartão Conversão (filtra por Aprovado)')
    c.click(BTNX('Filtros'), at=c.A(3, 'Para', 0.9), label='botão Filtros (dentro da busca)')
    c.click(BTN('Enviado', within=DLG), at=c.A(3, 'marca', 0.9), label='desmarca Enviado no filtro de Status')
    c.press('Escape', at=round(c.L(4) - 0.1, 2), label='fecha o filtro')
    c.mark(4)
    for k, palavra, nome in [(0, 'número', 'Nº'), (1, 'cliente', 'Cliente'), (2, 'data', 'Data'), (3, 'custo', 'Custo'), (4, 'valor', 'Valor'),
                             (5, 'margem', 'Margem'), (6, 'status', 'Status')]:
        c.hover(TH(k), 0.1, at=c.A(4, palavra, 0.7), label=f'coluna {nome}')
    c.click(BUSCA, at=c.A(4, 'buscar', 0.9), label='campo de busca')
    c.type(BUSCA, 'hotel', at=c.A(4, 'por', 0.05), noClick=True, cps=40, label='digita "hotel" na busca')
    c.type(BUSCA, '', at=c.A(4, 'telefone', 0.6), noClick=True, clear=True, label='limpa a busca')
    c.fim()
    return c


def cap02():
    """O BDI da empresa: aba Precificação, taxas 6/12/22, deslocamento e pagamento, Salvar, Simulador (R$ 1.666,67)."""
    c = Cap(2, pace=0.45, start=(760, 420), setup=SETUP_LISTA)
    c.mark(1)
    c.click(TAB('Precificação'), at=c.A(1, 'Precificação,', 2.0), label='aba Precificação')
    c.hover(P('Método BDI'), 0.8, at=c.A(1, 'método', 0.9), label='cartão Método BDI')
    c.hover(TXT('Preço = Custo Total ÷ BDI', within='main'), 1.2, at=c.A(1, 'preço', 0.9, nth=1), label='fórmula Preço = Custo Total ÷ BDI')
    c.mark(2)
    c.hover(P('BDI atual'), 1.0, at=c.A(2, 'zerado,', 0.9), label='BDI atual 1.0000 (tudo zerado)')
    c.type(I(0), '6', at=c.A(2, 'Imposto,', 1.0), clear=True, label='Imposto 6')
    c.type(I(1), '12', at=c.A(2, 'Administração', 1.0), clear=True, label='Adm. Indireta 12')
    c.type(I(2), '22', at=c.A(2, 'Lucro', 1.0), clear=True, label='Lucro Padrão 22')
    c.confere('main', 'BDI atual 0.6000', 'BDI atual 0.6000 depois de 6 + 12 + 22')
    c.mark(3)
    c.hover(P('BDI atual'), 1.4, at=c.A(3, 'BDI', 0.8), label='BDI atual 0.6000')
    c.hover(TXT('Adm. Indireta'), 1.2, at=c.A(3, 'barra', 0.9), label='barra de composição do preço')
    c.mark(4)
    c.rolar(380, at=c.A(4, 'Embaixo,', 1.0), label='desce até Deslocamento e Pagamento')
    c.type(I(3), '1,5', at=c.A(4, 'um', 0.9), clear=True, label='Custo por KM 1,5')
    c.type(I(4), '5', at=c.A(4, 'cinco', 0.9), clear=True, label='Desconto à vista 5')
    c.type(I(5), '10', at=c.A(4, 'dez', 0.9), clear=True, label='Parcelas (cartão) 10')
    c.click(BTN('Salvar'), at=c.A(4, 'Clico', 0.8), label='Salvar as taxas')
    c.confere('main', ['Configurações de precificação atualizadas.', 'R$ 1.666,67', 'R$ 1.000,00 ÷ 0.6000 = R$ 1.666,67', 'À vista (5% desc.)', 'Cartão (10x sem juros)'], 'taxas salvas e Simulador (R$ 1.666,67)')
    c.ev("[...document.querySelectorAll('main input')].slice(0,6).map(i=>i.value).join('|')", label='confere campos 6|12|22|1.5|5|10')
    c.mark(5)
    c.hover(P('Simulador de Preço'), 1.0, at=c.A(5, 'Simulador', 0.9), label='Simulador de Preço')
    c.hover(TXT('R$ 1.666,67'), 1.6, at=c.A(5, 'mil', 0.9, nth=1), label='Preço Final (BDI) R$ 1.666,67')
    c.hover(P('R$ 1.000,00 ÷ 0.6000'), 1.2, at=c.A(5, 'dividido', 0.9), label='linha Preço = R$ 1.000,00 ÷ 0.6000')
    c.fim()
    return c


def cap03():
    """O custo da Van 01: aba Custos Globais, Novo Recurso > Veículos, os campos, Total mensal e custo/hora, Salvar, composição."""
    c = Cap(3, pace=0.45, start=(760, 420), setup=SETUP_LISTA)
    c.mark(1)
    c.click(TAB('Custos Globais'), at=c.A(1, 'Custos', 1.9), label='aba Custos Globais')
    c.hover(P('Centro de Custos'), 0.8, at=c.A(1, 'Centro', 0.9), label='título Centro de Custos')
    c.hover(P('Custo/hora Veículos'), 1.0, at=c.A(1, 'veículos,', 0.9), label='faixa Custo/hora Veículos')
    c.mark(2)
    c.click(BTN('Novo Recurso'), at=c.A(2, 'Novo', 0.9), label='Novo Recurso')
    c.hover(BTN('Ferramentas'), 0.2, at=c.A(2, 'ferramentas,', 0.8), label='opção Ferramentas')
    c.hover(BTN('Brindes'), 0.2, at=c.A(2, 'brindes,', 0.8), label='opção Brindes')
    c.hover(BTN('EPIs'), 0.2, at=c.A(2, 'EPIs', 0.8), label='opção EPIs')
    c.click(BTN('Veículos'), at=c.A(2, 'veículo.', 0.9, nth=1), label='opção Veículos')
    c.mark(3)
    c.type(DI('Ex: Spin 2024'), 'Van 01', at=c.A(3, 'nome,', 1.0), label='Nome do veículo: Van 01')
    c.digitar_num({'selector': f'{DLG} input[inputmode=numeric]'}, '176', at=c.A(3, 'horas', 0.9), label='Horas de uso mensal 176')
    c.type(DI('Valor mensal', 0), '1400', at=c.A(3, 'mil', 0.9, nth=0), label='Depreciação mensal 1.400')
    c.type(DI('Valor mensal', 1), '1620', at=c.A(3, 'mil', 0.9, nth=1), label='Manutenção + Combustível 1.620')
    c.mark(4)
    c.type(DI('Valor anual', 0), '3600', at=c.A(4, 'três', 0.9), label='Seguro 3.600 (anual)')
    c.type(DI('Valor anual', 1), '2400', at=c.A(4, 'dois', 0.9), label='Documentação / IPVA 2.400 (anual)')
    c.confere('dlg', ['Total mensal: R$ 3.520,00', 'Horas mensais: 176h', 'Custo/hora: R$ 20,00/h'], 'Resumo da Van 01 (3.520,00 por mês, 176h, R$ 20,00/h)')
    c.ev(ROLA_DLG % "d.scrollHeight", at=c.A(4, 'No', 0.9), label='desce até o Resumo da janela')
    c.hover(TXT('Total mensal:', within=DLG), 1.0, at=c.A(4, 'total', 0.8), label='Resumo: Total mensal R$ 3.520,00')
    c.hover(TXT('Custo/hora:', within=DLG), 1.2, at=c.A(4, 'custo', 0.8), label='Resumo: Custo/hora R$ 20,00')
    c.mark(5)
    c.click(BTN('Salvar', within=DLG), at=c.A(5, 'Salvo.', 0.9), label='Salvar a Van 01')
    c.hover(P('Custo/hora Veículos'), 1.0, at=c.A(5, 'alto,', 0.9), label='Custo/hora Veículos R$ 20,00/h')
    c.click(TXT('Van 01', within='main'), at=c.A(5, 'clicando', 0.9), label='abre a Van 01 na lista')
    c.hover(P('Composição do custo'), 1.4, at=c.A(5, 'composição', 0.9), label='Composição do custo')
    c.confere('main', ['Custo/hora Veículos R$ 20,00/h', 'Custo por hora R$ 20,00', 'Custo mensal R$ 3.520,00', 'Horas mensais 176'], 'Van 01 na lista e na ficha')
    c.fim()
    return c


SUBABA = lambda n: {'role': 'button', 'name': n, 'exact': True, 'within': 'main'}        # sub-abas Mão de obra / Recursos / Materiais / Resumo
ESTOQUE = {'selector': 'main div:has(> label:has-text("Item do estoque")) button'}   # o rótulo some do botão depois de escolher um item


def cap04():
    """Quanto custa executar um serviço: lista + ficha (1.38.19), Mão de obra, Calcular, Recursos (Van 01), Materiais, Resumo (R$ 108,00 / R$ 180,00)."""
    c = Cap(4, pace=0.3, start=(760, 420), setup=SETUP_LISTA)
    c.mark(1)
    c.click(TAB('Custos dos Serviços'), at=c.A(1, 'Custos', 2.0), label='aba Custos dos Serviços')
    c.click(TXT('Higienização de Split', within='main'), at=c.A(1, 'Higienização', 0.9), label='escolhe Higienização de Split na lista')
    c.hover(SUBABA('Mão de obra'), 0.2, at=c.A(1, 'mão', 0.8), label='sub-aba Mão de obra')
    c.hover(SUBABA('Recursos'), 0.2, at=c.A(1, 'recursos,', 0.8), label='sub-aba Recursos')
    c.hover(SUBABA('Materiais'), 0.2, at=c.A(1, 'materiais', 0.8), label='sub-aba Materiais')
    c.hover(SUBABA('Resumo'), 0.2, at=c.A(1, 'resumo.', 0.8), label='sub-aba Resumo')
    c.mark(2)
    c.click(SUBABA('Mão de obra'), at=c.A(2, 'Na', 0.9), label='volta à sub-aba Mão de obra')
    c.digitar_num({'selector': 'main input[type=number]'}, '32', at=c.A(2, 'trinta', 1.0), label='Custo / hora 32')
    c.type({'selector': 'main input[type=text]'}, '1,5', at=c.A(2, 'uma', 1.0), clear=True, label='Horas 1,5')
    c.confere('main', 'Custo HH R$ 48,00', 'Custo HH R$ 48,00')
    c.hover(P('Custo HH'), 1.4, at=c.A(2, 'Custo', 0.9), label='Custo HH R$ 48,00')
    c.mark(3)
    c.click(BTN('Calcular'), at=c.A(3, 'Calcular', 0.9), label='botão Calcular')
    c.click({'selector': f'{DLG} button:has(svg.lucide-chevrons-up-down)'}, at=c.A(3, 'custo', 0.9), label='lista de funcionários da calculadora')
    c.press('Escape', at=c.A(3, 'funcionário.', 0.4), label='fecha a lista de funcionários')
    c.click(BTN('Cancelar'), at=c.A(3, 'fecho.', 0.9), label='Cancelar (sem aplicar)')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.mark(4)
    c.click(SUBABA('Recursos'), at=c.A(4, 'Recursos,', 0.9), label='sub-aba Recursos')
    c.click({'role': 'checkbox'}, at=c.A(4, 'vinculo', 0.9), label='marca a Van 01')
    c.hover(P('1.5h × R$ 20,00'), 1.4, at=c.A(4, 'trinta', 0.9), label='conta 1.5h × R$ 20,00 = R$ 30,00')
    c.confere('main', ['1.5h × R$ 20,00 = R$ 30,00', 'Total recursos vinculados R$ 30,00'], 'Van 01 vinculada (R$ 30,00)')
    c.mark(5)
    c.click(SUBABA('Materiais'), at=c.A(5, 'Materiais,', 0.9), label='sub-aba Materiais')
    for palavra, nome in [('limpa-evaporador', 'Limpa-evaporador em spray'), ('fita', 'Fita isolante'), ('mangueira', 'Mangueira de dreno')]:
        # o aviso "Material adicionado!" cai sobre o botão Adicionar quando ele fica no pé da tela: centraliza o botão antes de cada item
        c.ev("(()=>{const b=[...document.querySelectorAll('main button')].find(x=>x.innerText.trim()==='Adicionar');if(b)b.scrollIntoView({block:'center',behavior:'smooth'});return !!b})()", at=(c.A(5, palavra, 2.4) if palavra == 'limpa-evaporador' else None), label=f'centraliza o botão Adicionar ({nome})')
        c.click(ESTOQUE, label=f'abre Selecione do estoque ({nome})')
        c.click(OPT(nome), label=f'escolhe {nome}')
        c.click(BTN('Adicionar', within='main'), label=f'Adicionar {nome}')
    c.confere('main', ['Seu custo total R$ 30,00', 'Limpa-evaporador', 'Fita isolante', 'Mangueira de dreno'], 'materiais (R$ 30,00)')
    c.mark(6)
    c.click(SUBABA('Resumo'), at=c.A(6, 'Resumo,', 0.9), label='sub-aba Resumo')
    c.hover(P('Seu custo total para executar'), 1.6, at=c.A(6, 'cento', 0.9), label='Seu custo total para executar R$ 108,00')
    c.hover(P('Cliente paga com BDI'), 1.6, at=c.A(6, 'Dividido', 0.9), label='Cliente paga com BDI R$ 180,00')
    c.confere('main', ['Mão de obra R$ 48,00', 'Materiais R$ 30,00', 'Recursos R$ 30,00', 'Seu custo total para executar R$ 108,00', 'Cliente paga com BDI R$ 180,00'], 'Resumo (48 + 30 + 30 = 108; preço 180)')
    c.mark(7)
    c.fim()
    return c


# ---------------------------------------------------------------- assistente "Novo Orçamento" (1.38.19: 3 etapas; a 1ª, "Montagem", rola numa tela só)
CMDK = {'selector': '[cmdk-input]'}
COMBO_CLIENTE = {'role': 'combobox', 'name': 'Selecione o cliente'}
COMBO_SERVICO = {'role': 'combobox', 'name': 'Selecionar tipo de serviço...'}
QTD_SERVICO = {'selector': f'{DLG} input.w-16'}
PRECO_LINHA = lambda nome, k=1: {'selector': f"{DLG} table tr:has-text('{nome}') input[type=number]", 'nth': k}   # k=0 qtd, k=1 preço unit. da linha
KM = {'selector': f"{DLG} input[placeholder='0 km']"}
DESCONTO = {'selector': f"{DLG} input[placeholder='0']"}


def rola_ate(texto, margem=14):
    """JS: rola o corpo da janela até o título `texto` (folha do DOM com esse texto) ficar no alto (suave)."""
    return ("(()=>{const d=document.querySelector('[role=dialog] .overflow-y-auto');if(!d)return 'sem rolagem';"
            "const h=[...d.querySelectorAll('*')].find(e=>e.children.length===0&&e.textContent.trim().toLowerCase()===%s);"
            "if(!h)return 'sem titulo';const r=h.getBoundingClientRect(),dr=d.getBoundingClientRect();"
            "d.scrollTo({top:d.scrollTop+(r.top-dr.top)-%d,behavior:'smooth'});return d.scrollTop})()") % (json.dumps(texto.lower()), margem)


TOPO = "(()=>{const d=document.querySelector('[role=dialog] .overflow-y-auto');if(d)d.scrollTo({top:0});return 1})()"
DESC_TIPO = {'selector': f"{DLG} button[role=combobox]", 'hasText': 'R$'}    # tipo do desconto (R$ ou %): o Select do Radix não tem nome acessível


def rola_pag(texto, margem=110):
    """JS: rola a PÁGINA (a proposta pública rola na janela) até o título `texto` ficar perto do alto (suave)."""
    return ("(()=>{const h=[...document.querySelectorAll('body *')].find(e=>e.children.length===0&&e.textContent.trim().toLowerCase()===%s);"
            "if(!h)return 'sem titulo';const r=h.getBoundingClientRect();window.scrollTo({top:window.scrollY+r.top-%d,behavior:'smooth'});return r.top})()") % (json.dumps(texto.lower()), margem)


def wiz_abrir():
    """setup: abre /orcamentos, limpa o rascunho da sessão e abre o assistente Novo Orçamento"""
    return SETUP_LISTA + [LIMPA_RASCUNHO, {'do': 'click', 'target': BTN('Novo Orçamento')},
                          {'do': 'waitFor', 'text': 'Condições comerciais', 'timeout': 20}, {'do': 'wait', 'seconds': 0.6}]


def wiz_cliente():
    return [{'do': 'click', 'target': COMBO_CLIENTE}, {'do': 'type', 'target': CMDK, 'text': 'Pousada'},
            {'do': 'click', 'target': OPT('Pousada Brisa do Mar')}, {'do': 'waitFor', 'gone': {'role': 'listbox'}, 'timeout': 8, 'optional': True},
            {'do': 'wait', 'seconds': 0.5}]


def wiz_servico(nome, qtd=1):
    passos = [{'do': 'select', 'target': COMBO_SERVICO, 'option': nome}]
    if qtd != 1:
        passos += [{'do': 'click', 'target': QTD_SERVICO}, {'do': 'press', 'key': 'Control+A'},
                   {'do': 'type', 'target': QTD_SERVICO, 'text': str(qtd), 'noClick': True}]
    passos += [{'do': 'click', 'target': BTN('Adicionar', within=DLG)}, {'do': 'wait', 'seconds': 1.0}]
    return passos


def wiz_servicos():
    return wiz_servico('Higienização de Split', 3) + wiz_servico('Carga de Gás')


def wiz_material():
    return [{'do': 'click', 'target': BTN('Adicionar materiais')}, {'do': 'type', 'target': {'placeholder': 'Buscar por nome, código ou categoria...'}, 'text': 'gás'},
            {'do': 'click', 'target': {'selector': "[role=dialog] div[role=button]:has-text('R-410A') button", 'nth': 1}},
            {'do': 'click', 'target': BTN('Adicionar ao orçamento')}, {'do': 'wait', 'seconds': 1.0}]


def wiz_km():
    return [{'do': 'type', 'target': KM, 'text': '18'}, {'do': 'wait', 'seconds': 0.6}]


def wiz_proximo():
    return [{'do': 'click', 'target': BTN('Próximo')}, {'do': 'wait', 'seconds': 1.0}, {'do': 'eval', 'js': TOPO}, {'do': 'wait', 'seconds': 0.5}]


def wiz_condicoes():
    return [{'do': 'type', 'target': DESCONTO, 'text': '85'},
            {'do': 'type', 'target': {'placeholder': 'Observações internas'}, 'text': 'Atendimento de segunda a sexta, das 8h às 17h.', 'cps': 40},
            {'do': 'type', 'target': {'placeholder': 'Condições de pagamento, garantia, etc.'}, 'text': 'Serviço executado após a aprovação, com data combinada com o cliente.', 'cps': 40},
            {'do': 'wait', 'seconds': 0.6}]


def cap05():
    """Primeira etapa: abre o assistente, mostra as três etapas, prospecto x cliente cadastrado e escolhe a Pousada."""
    c = Cap(5, pace=0.45, start=(760, 420), setup=SETUP_LISTA + [LIMPA_RASCUNHO] + [
        {'do': 'click', 'target': BTN('Novo Orçamento')}, {'do': 'waitFor', 'text': 'Condições comerciais', 'timeout': 20}, {'do': 'wait', 'seconds': 0.8},
        {'do': 'press', 'key': 'Escape'}, {'do': 'waitFor', 'gone': {'role': 'dialog'}, 'timeout': 8}, LIMPA_RASCUNHO])
    c.mark(1)
    c.click(BTN('Novo Orçamento'), at=c.A(1, 'Novo', 2.0), label='Novo Orçamento')
    c.waitfor(text='Condições comerciais', timeout=15)
    c.hover(TXT('Montagem', within=DLG), 0.1, at=c.A(1, 'três', 0.9), label='etapa Montagem')
    c.hover(TXT('Condições comerciais', within=DLG), 0.1, at=c.A(1, 'etapas,', 0.8), label='etapa Condições comerciais')
    c.hover(TXT('Revisão e envio', within=DLG), 0.1, at=c.A(1, 'e', 0.8, nth=1), label='etapa Revisão e envio')
    c.hover(TXT('Montagem', within=DLG), 0.1, at=c.A(1, 'Montagem,', 0.9), label='a primeira etapa: Montagem')
    c.hover({'text': 'Destinatário', 'within': DLG}, 0.8, at=c.A(1, 'destinatário.', 0.9), label='bloco Destinatário')
    c.mark(2)
    c.click(TXT('Novo prospecto', within=DLG), at=c.A(2, 'prospecto,', 0.9), label='Novo prospecto')
    c.hover({'text': 'Nome *', 'within': DLG}, 0.3, at=c.A(2, 'só', 0.6), label='campos Nome, Telefone e E-mail do prospecto')
    c.click(TXT('Cliente cadastrado', within=DLG), at=c.A(2, 'Ainda', 1.0, nth=1), label='volta para Cliente cadastrado')
    c.mark(3)
    c.click(COMBO_CLIENTE, label='campo Cliente')
    c.type(CMDK, 'Pousada', cps=16, label='busca Pousada')
    c.click(OPT('Pousada Brisa do Mar'), at=c.A(3, 'Pousada', 1.4), label='escolhe a Pousada Brisa do Mar')
    c.add({'do': 'wait', 'seconds': 0.9})
    c.confere('wiz', ['Cliente * Pousada Brisa do Mar', 'Montagem', 'Condições comerciais', 'Revisão e envio'], 'Pousada escolhida e as três etapas')
    c.fim()
    return c


def cap06():
    """Segunda etapa: BDI recolhido ("Ajustar taxas"), Higienização × 3 (R$ 180,00), detalhe da linha, Carga de Gás (selo âmbar), subtotal R$ 890,00."""
    c = Cap(6, pace=0.45, start=(760, 420), setup=wiz_abrir() + wiz_cliente())
    c.mark(1)
    c.hover(TXT('Configurações BDI', within=DLG), 0.8, at=c.A(1, 'Configurações', 0.9), label='bloco Configurações BDI')
    c.click(BTN('Ajustar taxas e entender o BDI'), at=c.A(1, 'Ajustar', 1.9), label='Ajustar taxas e entender o BDI')
    c.hover({'selector': f'{DLG} input[type=number]', 'nth': 0}, 0.3, at=c.A(1, 'salvei', 0.9), label='Imposto 6')
    c.hover({'selector': f'{DLG} input[type=number]', 'nth': 2}, 0.3, at=c.A(1, 'Precificação.', 0.9), label='Lucro 22')
    c.hover({'selector': f'{DLG} input[type=number]', 'nth': 3}, 0.3, at=c.A(1, 'Elas', 0.9), label='Custo / km 1,5')
    c.mark(2)
    c.ev(rola_ate('Serviços e Mão de Obra'), at=c.A(2, 'Escolho', 1.3), label='rola até Serviços e Mão de Obra')
    c.add({'do': 'wait', 'seconds': 0.7})
    c.select(COMBO_SERVICO, 'Higienização de Split', at=c.A(2, 'Escolho', 0.7), label='escolhe Higienização de Split')
    c.click(QTD_SERVICO, at=c.A(2, 'quantidade,', 0.9), label='campo Qtd')
    c.press('Control+A', label='seleciona a quantidade')
    c.type(QTD_SERVICO, '3', noClick=True, label='Qtd 3')
    c.click(BTN('Adicionar', within=DLG), at=c.A(2, 'splits', 1.0), label='Adicionar a Higienização')
    c.hover(PRECO_LINHA('Higienização de Split'), 1.4, at=c.A(2, 'cento', 0.9), label='Preço unit. R$ 180,00 (custo + BDI)')
    c.ev("[...document.querySelectorAll(\"[role=dialog] table input[type=number]\")].map(i=>(i.getAttribute('aria-label')||'qtd')+'='+i.value).join('|')", label='confere qtd 3 e preço 180')
    c.confere('wiz', ['Custo do serviço + BDI', 'R$ 108,00', 'R$ 540,00'], 'Higienização: 3 × 180,00 = 540,00 (custo 108,00)')
    c.mark(3)
    c.click(TXT('Higienização de Split', within=f'{DLG} table'), at=c.A(3, 'Clicando', 0.9), label='abre os detalhes da linha')
    c.hover(PD('Custo total unit.'), 1.4, at=c.A(3, 'custo', 0.9, nth=1), label='Custo total unit. R$ 108,00')
    c.click(TXT('Higienização de Split', within=f'{DLG} table'), at=c.A(4, 'Agora', 1.0), label='fecha os detalhes')
    c.mark(4)
    c.select(COMBO_SERVICO, 'Carga de Gás', at=c.A(4, 'Carga', 1.0), label='escolhe Carga de Gás')
    c.click(BTN('Adicionar', within=DLG), label='Adicionar a Carga de Gás')
    c.hover(TXT('Sem custos configurados', within=DLG), 1.2, at=c.A(4, 'Sem', 0.9), label='selo Sem custos configurados')
    c.hover(PRECO_LINHA('Carga de Gás'), 1.4, at=c.A(4, 'trezentos', 0.9), label='Preço unit. R$ 350,00 (preço cadastrado)')
    c.mark(5)
    c.confere('wiz', ['Sem custos configurados', 'Preço cadastrado do serviço', 'Subtotal Serviços R$ 890,00'], 'Carga de Gás 350,00 e subtotal R$ 890,00')
    c.hover(PD('Subtotal Serviços'), 1.6, at=c.A(5, 'subtotal', 0.9), label='Subtotal Serviços R$ 890,00')
    c.mark(6)
    c.hover(PRECO_LINHA('Higienização de Split'), 1.6, at=c.A(6, 'digita', 0.9), label='campo Preço unit. (editável, sem digitar)')
    c.fim()
    return c


def cap07():
    """Terceira etapa: Adicionar materiais (R-410A, R$ 150,00/kg), Adicionar ao orçamento, Deslocamento 18 km (custo R$ 27,00, preço R$ 45,00)."""
    c = Cap(7, pace=0.45, start=(760, 420), setup=wiz_abrir() + wiz_cliente() + wiz_servicos())
    c.confere('wiz', ['Subtotal Serviços R$ 890,00', 'Pousada Brisa do Mar'], 'partida do cap. 7: serviços R$ 890,00 já no assistente')
    c.mark(1)
    c.ev(rola_ate('Materiais'), at=0.2, label='rola até Materiais')
    c.add({'do': 'wait', 'seconds': 0.7})
    c.click(BTN('Adicionar materiais'), at=c.A(1, 'Adicionar', 1.9), label='Adicionar materiais')
    c.type({'placeholder': 'Buscar por nome, código ou categoria...'}, 'gás', at=c.A(1, 'busco', 0.9), cps=14, label='busca gás')
    c.hover({'selector': "[role=dialog] div[role=button]:has-text('R-410A')"}, 0.6, at=c.A(1, 'escolho', 0.3), label='Gás refrigerante R-410A')
    c.hover({'selector': "[role=dialog] div[role=button]:has-text('R-410A') p:has-text('/ kg')"}, 1.2, at=c.A(1, 'cento', 0.9), label='R$ 150,00 / kg')
    c.mark(2)
    c.click({'selector': "[role=dialog] div[role=button]:has-text('R-410A') button", 'nth': 1}, at=c.A(2, 'um', 0.9), label='+ um quilo')
    c.click(BTN('Adicionar ao orçamento'), at=c.A(2, 'adiciono', 0.9), label='Adicionar ao orçamento')
    c.waitfor(gone={'text': 'Adicionar ao orçamento'}, timeout=8)
    c.confere('wiz', ['Gás refrigerante R-410A', 'Subtotal Materiais R$ 150,00', 'Custo R$ 90,00 · Preço R$ 150,00'], 'R-410A 1 kg a R$ 150,00 (preço de venda)')
    c.hover(PD('Subtotal Materiais'), 1.2, at=c.A(2, 'material', 0.9), label='Subtotal Materiais R$ 150,00')
    c.mark(3)
    c.ev(rola_ate('Deslocamento'), at=c.A(3, 'Embaixo,', 1.0), label='rola até Deslocamento')
    c.add({'do': 'wait', 'seconds': 0.7})
    c.type(KM, '18', at=c.A(3, 'dezoito', 1.2), label='Distância 18 km')
    c.hover({'text': 'Modalidade', 'within': DLG}, 0.6, at=c.A(3, 'modalidade', 0.9), label='Modalidade Custo por km + BDI')
    c.hover({'text': 'Preço resultante', 'within': DLG}, 1.6, at=c.A(3, 'quarenta', 0.9), label='Custo R$ 27,00 · Preço resultante R$ 45,00')
    c.confere('wiz', ['Custo por km + BDI', 'Custo R$ 27,00 · Preço resultante R$ 45,00'], 'deslocamento 18 km: custo 27,00, preço 45,00')
    c.fim()
    return c


def cap08():
    """Quarta etapa: Próximo, Condições comerciais, desconto R$ 85,00 (alterna %), brindes e parcelas, Observações e Condições / Termos."""
    c = Cap(8, pace=0.45, start=(760, 420), setup=wiz_abrir() + wiz_cliente() + wiz_servicos() + wiz_material() + wiz_km())
    c.confere('wiz', ['Subtotal Serviços R$ 890,00', 'Subtotal Materiais R$ 150,00', 'Custo R$ 27,00 · Preço resultante R$ 45,00'], 'partida do cap. 8: serviços 890,00, material 150,00, deslocamento 45,00')
    c.mark(1)
    c.click(BTN('Próximo'), at=c.A(1, 'Próximo,', 1.9), label='Próximo: Condições comerciais')
    c.waitfor(text='Cobrança após aprovação', timeout=15)
    c.ev(TOPO, label='volta ao topo da etapa')
    c.click(DESC_TIPO, at=1.3, label='tipo do desconto: R$')
    c.click(OPT('%'), label='alterna para %')
    c.click({'selector': f"{DLG} button[role=combobox]", 'hasText': '%'}, label='tipo do desconto: %')
    c.click(OPT('R$'), label='volta para R$')
    c.type(DESCONTO, '85', at=c.A(1, 'oitenta', 1.2), label='Desconto R$ 85,00')
    c.hover(PD('Preço praticado'), 1.6, at=c.A(1, 'Preço', 0.9), label='Preço praticado R$ 1.000,00')
    c.confere('wiz', ['Preço praticado R$ 1.000,00', 'Preço sugerido R$ 1.085,00', 'Desconto − R$ 85,00', 'Deslocamento R$ 27,00'], 'desconto 85,00: preço praticado 1.000,00 (sugerido 1.085,00)')
    c.mark(2)
    c.hover({'text': 'Incluir brindes neste orçamento', 'within': DLG}, 1.0, at=c.A(2, 'caixa', 0.9), label='Incluir brindes neste orçamento')
    c.hover({'text': 'Nº de parcelas', 'within': DLG}, 1.0, at=c.A(2, 'número', 0.9), label='Nº de parcelas: À vista')
    c.mark(3)
    c.type({'placeholder': 'Observações internas'}, 'Atendimento de segunda a sexta, das 8h às 17h.', at=c.A(3, 'Observações,', 2.2), cps=28, label='Observações')
    c.type({'placeholder': 'Condições de pagamento, garantia, etc.'}, 'Serviço executado após a aprovação, com data combinada com o cliente.',
           at=c.A(3, 'Condições', 1.0), cps=28, label='Condições / Termos')
    c.mark(4)
    c.hover({'placeholder': 'Observações internas'}, 1.2, at=c.A(4, 'textos', 0.9), label='os dois textos saem na proposta')
    c.hover({'placeholder': 'Condições de pagamento, garantia, etc.'}, 1.2, at=c.A(4, 'Informações', 0.9), label='Condições e Termos viram Informações adicionais')
    c.fim()
    return c


def cap09():
    """Quinta etapa: Próximo, Válido até (+15 dias), Clean, resumo (Preço sugerido/praticado, O que entra no BDI), pagamentos, Criar Orçamento."""
    c = Cap(9, pace=0.45, start=(760, 420), setup=wiz_abrir() + wiz_cliente() + wiz_servicos() + wiz_material() + wiz_km() + wiz_proximo() + wiz_condicoes())
    c.mark(1)
    c.click(BTN('Próximo'), at=c.A(1, 'última', 1.5), label='Próximo: Revisão e envio')
    c.waitfor(text='Template da Proposta', timeout=15)
    c.ev(TOPO, label='volta ao topo da etapa')
    c.click({'selector': f"{DLG} button:has-text('dd/mm/aaaa')"}, at=c.A(1, 'Válido', 0.9), label='campo Válido até')
    c.click({'role': 'gridcell', 'name': '18', 'exact': True}, at=c.A(1, 'quinze', 0.9), label='marca 18/11 (15 dias à frente)')
    c.confere('wiz', ['Válido até', '18/11/2026', 'Template da Proposta'], 'Válido até 18/11/2026 (15 dias à frente)')
    c.hover({'text': 'Template da Proposta', 'within': DLG}, 0.8, at=c.A(1, 'modelo', 0.9), label='Template da Proposta: Clean')
    c.hover(PD('Capa da proposta'), 0.8, at=c.A(1, 'Capa', 0.9), label='Capa da proposta')
    c.mark(2)
    c.hover(PD('Preço sugerido'), 1.2, at=c.A(2, 'Preço', 0.9), label='Preço sugerido R$ 1.085,00')
    c.hover(PD('O que entra no BDI?'), 1.4, at=c.A(2, 'guia', 0.9), label='guia O que entra no BDI?')
    c.hover(PD('Fora do BDI automático'), 1.4, at=c.A(2, 'Carga', 0.9), label='Fora do BDI automático (Carga de Gás e gás)')
    c.mark(3)
    c.hover(PD('Preço praticado'), 1.6, at=c.A(3, 'Preço', 0.9), label='Preço praticado R$ 1.000,00')
    c.confere('wiz', ['Preço praticado R$ 1.000,00', 'Preço sugerido R$ 1.085,00', 'À vista R$ 950,00', '10x R$ 100,00', 'Fora do BDI automático', '2 preços cadastrados', 'R$ 500,00'],
              'Revisão: sugerido 1.085,00, praticado 1.000,00, à vista 950,00, 10x 100,00')
    c.mark(4)
    c.hover(PD('Pagamentos'), 1.8, at=c.A(4, 'Embaixo,', 0.9), label='Pagamentos: à vista R$ 950,00 e 10x R$ 100,00')
    c.mark(5)
    c.click(BTN('Criar Orçamento'), at=c.A(5, 'Clico', 0.8), label='Criar Orçamento')
    c.waitfor(gone={'role': 'dialog'}, timeout=15)
    c.hover(LINHA('Pousada Brisa do Mar'), 1.6, at=c.A(5, 'Ele', 0.9), label='a linha nova entra como Rascunho')
    c.confere("main tbody tr", ['#9', 'Pousada Brisa do Mar', 'R$ 441,00', 'R$ 1.000,00', 'Rascunho'], 'linha #9: custo 441,00, valor 1.000,00, Rascunho')
    c.fim()
    return c


def cap16():
    """Recapitulando: base simples (a lista de orçamentos com o #9 Convertido e o #2 No financeiro); a montagem da recapitulação entra na edição."""
    c = Cap(16, pace=0.4, start=(760, 420), setup=SETUP_LISTA)
    c.mark(1)
    c.hover(TAB('Precificação'), 1.0, at=c.A(1, 'Precificação,', 0.9), label='aba Precificação')
    c.hover(TAB('Custos Globais'), 1.0, at=c.A(1, 'Custos', 0.9), label='aba Custos Globais')
    c.hover(TAB('Custos dos Serviços'), 1.0, at=c.A(1, 'higienização,', 1.3), label='aba Custos dos Serviços')
    c.mark(2)
    c.hover(BTN('Novo Orçamento'), 1.4, at=c.A(2, 'orçamento', 0.9), label='botão Novo Orçamento')
    c.mark(3)
    c.hover(BTN('Configurar Proposta'), 1.4, at=c.A(3, 'proposta,', 0.9), label='botão Configurar Proposta')
    c.mark(4)
    c.hover(LINHA('Hotel Mirante do Mar'), 1.6, at=c.A(4, 'Aprovou', 0.9), label='a linha do Hotel Mirante do Mar (No financeiro)')
    c.hover(LINHA('Pousada Brisa do Mar'), 1.6, at=c.A(4, 'aprovado', 0.9), label='a linha da Pousada Brisa do Mar (Convertido)')
    c.mark(5)
    c.fim()
    return c


# ---------------------------------------------------------------- Configurar Proposta, menu da linha, janelas de aprovação e de distribuição
MODELO = lambda n: {'selector': f'{DLG} button', 'hasText': n, 'nth': 0}                  # cartões Clean / Vanguarda / Aurora / Prisma
SECAO = lambda nome: f"{DLG} div.rounded-lg:has(button[aria-label='{nome}'])"            # bloco de uma seção da proposta (interruptor com o nome dela)
TOAST = {'selector': 'li[role=status]', 'nth': 0}                                           # aviso (toast) do Radix


def cap10():
    """Configurar a proposta: Modelo (Clean), Personalização (logo 120%, cores, chaves, seção Garantia), Revisão (páginas) e Salvar."""
    c = Cap(10, pace=0.45, start=(760, 420), setup=SETUP_LISTA + [LIMPA_RASCUNHO])
    c.mark(1)
    c.click(BTN('Configurar Proposta'), at=c.A(1, 'Configurar', 2.0), label='Configurar Proposta')
    c.waitfor(text='Escolha o estilo visual da proposta enviada ao cliente.', timeout=15)
    c.hover(MODELO('Clean'), 0.2, at=c.A(1, 'Clean,', 0.8), label='modelo Clean')
    c.hover(MODELO('Vanguarda'), 0.2, at=c.A(1, 'Vanguarda,', 0.8), label='modelo Vanguarda')
    c.hover(MODELO('Aurora'), 0.2, at=c.A(1, 'Aurora', 0.8), label='modelo Aurora')
    c.hover(MODELO('Prisma'), 0.2, at=c.A(1, 'Prisma,', 0.8), label='modelo Prisma')
    c.mark(2)
    c.click(MODELO('Clean'), at=c.A(2, 'Clean.', 0.9), label='fica com o Clean')
    c.mark(3)
    c.click(BTN('Próximo', within=DLG), at=c.A(3, 'Personalização,', 0.9), label='Próximo: Personalização')
    c.waitfor(text='Tamanho do logo', timeout=15)
    c.click({'role': 'slider'}, at=c.A(3, 'tamanho', 0.9), label='controle Tamanho do logo')
    c.press('ArrowRight', times=2, label='Tamanho do logo 120%')
    c.confere('dlg', '120%', 'Tamanho do logo 120%')
    c.ev("(()=>{const d=document.querySelector('[role=dialog] .overflow-y-auto');if(d)d.scrollBy({top:300,behavior:'smooth'});return 1})()", at=c.A(3, 'Mais', 0.6), label='desce a janela até as cores')
    c.add({'do': 'wait', 'seconds': 0.5})
    c.hover({'text': 'Cor Primária', 'within': DLG}, 0.4, at=c.A(3, 'cores,', 0.9), label='Cor Primária', noScroll=True)
    c.hover({'text': 'Cor de Destaque', 'within': DLG}, 0.4, at=c.A(3, 'destaque', 0.9), label='Cor de Destaque', noScroll=True)
    c.hover({'text': 'Fundo do Cabeçalho', 'within': DLG}, 0.4, at=c.A(3, 'cabeçalho,', 0.9), label='Fundo do Cabeçalho', noScroll=True)
    c.ev("(()=>{const d=document.querySelector('[role=dialog] .overflow-y-auto');if(d)d.scrollBy({top:260,behavior:'smooth'});return 1})()", at=c.A(3, 'chaves', 1.4), label='desce a janela até as chaves')
    c.add({'do': 'wait', 'seconds': 0.5})
    c.hover(SW('Mostrar paginação?'), 0.6, at=c.A(3, 'paginação', 0.9), label='chave Mostrar paginação?', noScroll=True)
    c.hover(SW('Mostrar deslocamento'), 0.6, at=c.A(3, 'deslocamento.', 0.9), label='chave Mostrar deslocamento', noScroll=True)
    c.mark(4)
    c.ev(rola_ate('Seções da proposta', 20), at=c.A(4, 'Seções', 1.0), label='rola até Seções da proposta')
    # as sete seções vêm ligadas de fábrica (getProposalSections): "desligo" e "ligo" a Garantia na tela, para a fala fazer sentido
    c.click(SW('Garantia', within=DLG), at=c.A(4, 'desligo', 0.9), label='desliga a seção Garantia')
    c.hover({'selector': f"{SECAO('Garantia')} button[aria-label='Mover para cima']"}, 0.3, at=c.A(4, 'setas,', 0.9), label='setas ▲▼ de uma seção')
    c.click(SW('Garantia', within=DLG), at=c.A(4, 'Ligo', 0.9, nth=1), label='liga a seção Garantia de novo')
    c.type({'selector': f"{SECAO('Garantia')} textarea"}, 'Garantia de 90 dias sobre o serviço.', at=c.A(4, 'escrevo:', 0.9), cps=28, label='texto da Garantia')
    c.ev("[...document.querySelectorAll(\"[role=dialog] textarea\")].map(t=>t.value).filter(v=>/Garantia/.test(v)).join('|')", label='confere texto da Garantia digitado')
    c.click({'selector': f"{SECAO('Garantia')} button[aria-label='Mover para cima']"}, at=c.A(4, 'Esse', 0.9), label='▲ sobe a Garantia')
    c.mark(5)
    c.click(BTN('Próximo', within=DLG), at=c.A(5, 'Revisão,', 0.9), label='Próximo: Revisão')
    c.waitfor(text='Veja como a proposta vai chegar ao cliente.', timeout=15)
    c.click({'selector': f"{DLG} button[aria-label*='róxim']"}, at=c.A(5, 'folheio', 0.9), label='folheia: próxima página')
    c.click({'selector': f"{DLG} button[aria-label*='róxim']"}, at=c.A(5, 'vejo', 0.9), label='folheia: próxima página', optional=True)
    c.mark(6)
    c.click(BTN('Salvar', within=DLG), at=c.A(6, 'Salvo.', 1.0), label='Salvar a configuração')
    c.waitfor(target={'selector': 'li[role=status]'}, timeout=10)
    c.confere('li[role=status]', 'Configuração da proposta salva', 'aviso Configuração da proposta salva')
    c.click({'selector': f"{DLG} button:has-text('Fechar')"}, at=c.A(6, 'fecho.', 1.0), label='fecha a janela no X', noScroll=True)
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.fim()
    return c


def cap11():
    """Visualizar e gerar o link: Visualizar (Clean), botões WhatsApp/PDF/Gerar cobrança (só passam), Gerar link da proposta, o selo vira Enviado."""
    c = Cap(11, pace=0.45, start=(760, 420), setup=SETUP_LISTA)
    c.mark(1)
    c.abrir_menu('Pousada Brisa do Mar', 'Visualizar', at=c.A(1, 'menu', 1.9), label='menu ⋮ da linha da Pousada')
    c.click(ITEM('Visualizar'), at=c.A(1, 'Visualizar', 0.9), label='Visualizar')
    c.waitfor(text='Proposta #9', timeout=15)
    c.hover({'text': 'Não visualizada pelo cliente ainda', 'within': DLG}, 1.2, at=c.A(1, 'primeira', 0.9), label='Não visualizada pelo cliente ainda')
    c.confere('dlg', ['Proposta #9', 'Não visualizada pelo cliente ainda', 'Gerar cobrança', 'WhatsApp', 'PDF', 'Pousada Brisa do Mar', 'R$ 1.000,00'], 'Visualizar: proposta #9 de R$ 1.000,00')
    c.mark(2)
    c.hover(BTN('WhatsApp', within=DLG), 0.4, at=c.A(2, 'WhatsApp,', 0.9), label='botão WhatsApp')
    c.hover(BTN('PDF', within=DLG), 0.4, at=c.A(2, 'PDF,', 0.9), label='botão PDF')
    c.hover(BTN('Gerar cobrança', within=DLG), 0.4, at=c.A(2, 'Gerar', 0.9), label='botão Gerar cobrança')
    fechar_janela(c, at=c.A(2, 'manual,', 0.9))
    c.mark(3)
    c.abrir_menu('Pousada Brisa do Mar', 'Gerar link da proposta', at=c.A(3, 'Para', 0.9), label='menu ⋮ da linha da Pousada')
    c.click(ITEM('Gerar link da proposta'), at=c.A(3, 'Gerar', 0.9), label='Gerar link da proposta')
    c.waitfor(target={'selector': 'li[role=status]'}, timeout=10)
    c.confere('li[role=status]', ['Link gerado e copiado!', 'Já pode colar e enviar pro cliente.'], 'aviso Link gerado e copiado')
    c.confere('row:Pousada Brisa do Mar', ['R$ 1.000,00', 'Enviado'], 'linha da Pousada: Enviado')
    c.hover({'selector': "main tbody tr:has-text('Pousada Brisa do Mar') td", 'hasText': 'Enviado'}, 1.0, at=c.A(3, 'Enviado.', 0.9), label='o selo da linha passa a Enviado')
    c.mark(4)
    c.hover(CARD('Em Aberto'), 1.6, at=c.A(4, 'cartão', 0.9), label='cartão Em Aberto sobe')
    c.confere('main', 'Em Aberto R$ 6.630,00', 'Em Aberto sobe de 5.630,00 para 6.630,00')
    c.fim()
    return c


def cap12():
    """O que o cliente vê: página pública da proposta (Clean), rolagem, Baixar PDF (só passa), Aprovar, volta para /orcamentos (Pousada Aprovado)."""
    c = Cap(12, pace=0.45, start=(760, 420), setup=SETUP_LISTA, prewarm=['/dashboard', '/orcamentos', f'/proposta/{TOKEN9}?preview=1'])
    c.mark(1)
    c.add({'do': 'goto', 'url': f'/proposta/{TOKEN9}?preview=1', 'at': c.A(1, 'Ele', 1.0), 'label': 'abre o link da proposta (o que o cliente recebe)'})
    c.waitfor(text='Glacial Cold Brasil', timeout=25)
    c.hover(TXT('Glacial Cold Brasil'), 0.8, at=c.A(1, 'empresa,', 0.9), label='no alto: a empresa', noScroll=True)
    c.hover({'text': 'Proposta válida até'}, 1.4, at=c.A(1, 'validade.', 0.9), label='a validade da proposta', noScroll=True)
    c.mark(2)
    c.ev(rola_pag('Cliente'), at=c.A(2, 'Mais', 0.4), label='desce até Cliente')
    c.ev(rola_pag('Serviços'), at=c.A(2, 'serviços', 0.9), label='desce até Serviços')
    c.ev(rola_pag('Total dos serviços'), at=c.A(2, 'totais,', 0.9), label='desce até os totais')
    c.hover({'text': 'Descontos'}, 0.6, at=c.A(2, 'desconto.', 0.9), label='deslocamento e desconto')
    c.hover({'text': 'R$ 1.000,00', 'exact': True}, 1.4, at=c.A(2, 'mil', 0.9), label='TOTAL R$ 1.000,00')
    c.confere('body', ['Proposta válida até 18/11/2026', 'Higienização de Split', 'R$ 180,00 3 R$ 540,00', 'Carga de Gás', 'R$ 350,00 1 R$ 350,00', 'Gás refrigerante R-410A R$ 150,00 1 R$ 150,00',
                       'Total dos serviços R$ 890,00', 'Total de materiais R$ 150,00', 'Deslocamento (18 km) R$ 45,00', 'Descontos − R$ 85,00', 'TOTAL R$ 1.000,00'], 'página do cliente: totais (890 + 150 + 45 − 85 = 1.000,00)')
    c.mark(3)
    c.ev(rola_pag('Formas de pagamento'), at=c.A(3, 'formas', 1.0), label='desce até Formas de pagamento')
    c.ev(rola_pag('Informações adicionais'), at=c.A(3, 'informações', 1.0), label='desce até Informações adicionais')
    c.ev(rola_pag('Observações'), at=c.A(3, 'observações', 1.0), label='desce até Observações')
    c.ev(rola_pag('Garantia'), at=c.A(3, 'garantia', 1.0), label='desce até Garantia')
    c.confere('body', ['À vista no PIX', '5% de desconto', 'R$ 950,00', 'Em até 10x de R$ 100,00', 'Serviço executado após a aprovação, com data combinada com o cliente.',
                       'Atendimento de segunda a sexta, das 8h às 17h.', 'Garantia de 90 dias sobre o serviço.'], 'página do cliente: pagamento, informações, observações e garantia')
    c.mark(4)
    c.hover(BTN('Baixar PDF'), 0.6, at=c.A(4, 'PDF.', 0.9), label='botão Baixar PDF (só passa)', noScroll=True)
    c.ev("(()=>{window.scrollTo({top:document.documentElement.scrollHeight,behavior:'smooth'});return 1})()", at=c.A(4, 'fim,', 1.0), label='desce até o fim')
    c.hover(BTN('Aprovar'), 0.5, at=c.A(4, 'Aprovar', 0.9), label='botão Aprovar', noScroll=True)
    c.hover(BTN('Rejeitar'), 0.5, at=c.A(4, 'Rejeitar,', 0.9), label='botão Rejeitar (só passa)', noScroll=True)
    c.mark(5)
    c.click(BTN('Aprovar'), at=c.A(5, 'basta', 0.9), label='Aprovar', noScroll=True)
    c.waitfor(text='Proposta aprovada', timeout=15)
    c.confere('body', 'Proposta aprovada', 'página do cliente depois de Aprovar')
    c.mark(6)
    c.add({'do': 'goto', 'url': '/orcamentos', 'at': c.A(6, 'De', 0.9), 'label': 'volta para a lista de orçamentos'})
    c.waitfor(text='Gerencie orçamentos, custos e precificação', timeout=25)
    c.hover({'selector': "main tbody tr:has-text('Pousada Brisa do Mar')", 'hasText': 'Aprovado'}, 1.8, at=c.A(6, 'Aprovado.', 0.9), label='a linha da Pousada: Aprovado')
    c.confere('row:Pousada Brisa do Mar', ['R$ 1.000,00', 'Aprovado'], 'linha da Pousada: Aprovado (sem No financeiro)')
    c.fim()
    return c


def cap13():
    """Quem abriu a proposta: o olho da lista (Hotel Mirante do Mar: 3 visualizações; Casa de Repouso: Não visualizada) e o item "Abrir proposta em nova guia"."""
    c = Cap(13, pace=0.45, start=(760, 420), setup=SETUP_LISTA)
    OLHO = lambda cliente: {'selector': f"main tbody tr:has-text('{cliente}') td:nth-child(2) svg"}
    CEL = lambda cliente: {'selector': f"main tbody tr:has-text('{cliente}') td:nth-child(2)"}
    c.mark(1)
    c.hover(CEL('Hotel Mirante do Mar'), 1.2, at=c.A(1, 'Embaixo', 1.9), label='coluna Cliente do Hotel Mirante do Mar')
    # a dica do olho é o `title` nativo: o navegador não a desenha na gravação. O robô pousa no olho ~2,5 s e LÊ o texto exato por eval
    # (actions.json, label "title do olho"); a edição põe um aviso "Ao passar o mouse: <title>" com esse texto.
    c.hover(OLHO('Hotel Mirante do Mar'), 2.5, at=c.A(1, 'passando', 1.0), label='olho: pousa para a dica (title)')
    c.ev("(()=>{const t=[...document.querySelectorAll(\"main tbody tr\")].find(r=>r.innerText.includes('Hotel Mirante do Mar'));const e=t&&t.querySelector('td:nth-child(2) [title]');const v=e?e.getAttribute('title'):'sem title';return /Visualizada 3× · última vez/.test(v)?'OK: '+v:'DIFERENTE: '+v})()", label='confere title do olho (texto exato da dica)')
    c.mark(2)
    c.hover(CEL('Casa de Repouso'), 1.0, at=c.A(2, 'Já', 0.9), label='linha da Casa de Repouso Vida Mansa (prospecto)')
    c.hover(OLHO('Casa de Repouso'), 1.6, at=c.A(2, 'olho', 0.9), label='olho apagado: Não visualizada')
    c.confere('row:Casa de Repouso', ['(prospecto)', 'Não visualizada', 'Enviado'], 'Casa de Repouso Vida Mansa: prospecto, Não visualizada')
    c.mark(3)
    c.abrir_menu('Hotel Mirante do Mar', 'Abrir proposta em nova guia', at=c.A(3, 'Quando', 0.9), label='menu ⋮ de uma linha')
    c.hover(ITEM('Abrir proposta em nova guia'), 1.6, at=c.A(3, 'Abrir', 0.9), label='item Abrir proposta em nova guia (sem clicar)')
    c.press('Escape', at=c.A(3, 'conta.', 0.3), label='fecha o menu')
    c.fim()
    return c


def cap14():
    """Aprovar por dentro: Hotel Mirante do Mar (R$ 3.200,00), Vou receber depois (3x, 1º vencimento 20/11/2026), Já recebi (só mostra), Aprovar e gerar conta a receber."""
    c = Cap(14, pace=0.45, start=(760, 420), setup=SETUP_LISTA)
    c.mark(1)
    c.abrir_menu('Hotel Mirante do Mar', 'Aprovar orçamento', at=c.A(1, 'abro', 1.9), label='menu ⋮ do Hotel Mirante do Mar')
    c.click(ITEM('Aprovar orçamento'), at=c.A(1, 'Aprovar', 0.9), label='Aprovar orçamento')
    c.waitfor(text='Valor: R$ 3.200,00', timeout=15)
    c.mark(2)
    c.hover({'text': 'Valor: R$ 3.200,00', 'within': DLG}, 1.2, at=c.A(2, 'três', 0.9), label='Valor: R$ 3.200,00')
    c.hover(BTN('Já recebi', within=DLG), 0.4, at=c.A(2, 'recebi', 1.1), label='botão Já recebi')
    c.hover(BTN('Vou receber depois', within=DLG), 0.4, at=c.A(2, 'Vou', 0.8), label='botão Vou receber depois')
    c.mark(3)
    c.hover({'selector': f"{DLG} button[role=combobox]", 'hasText': '3x'}, 0.8, at=c.A(3, 'parcelas', 0.9), label='Parcelas 3x (vêm do orçamento)')
    c.click({'selector': f"{DLG} button:has-text('03/11/2026')"}, at=c.A(3, 'Escolho', 0.9), label='campo Primeiro vencimento')
    c.click({'role': 'gridcell', 'name': '20', 'exact': True}, at=c.A(3, 'vencimento,', 0.9), label='marca 20/11/2026')
    c.hover({'text': 'Parcelas que serão criadas', 'within': DLG}, 1.6, at=c.A(3, 'lista', 0.9), label='lista Parcelas que serão criadas')
    c.confere('dlg', ['Primeiro vencimento * 20/11/2026', 'Parcela 1/3 · 20/11/2026 R$ 1.066,67', 'Parcela 2/3 · 20/12/2026 R$ 1.066,67', 'Parcela 3/3 · 20/01/2027 R$ 1.066,66', 'Total R$ 3.200,00'],
              'parcelas do #2: 20/11, 20/12 e 20/01 (T13 parte delas)')
    c.mark(4)
    c.click(BTN('Já recebi', within=DLG), at=c.A(4, 'recebi', 1.1), label='Já recebi')
    c.hover({'text': 'Forma de pagamento *', 'within': DLG}, 0.8, at=c.A(4, 'forma', 0.9), label='Forma de pagamento')
    c.hover({'text': 'Caixa / Conta bancária *', 'within': DLG}, 0.8, at=c.A(4, 'conta', 0.9), label='Caixa / Conta bancária')
    c.hover({'text': 'Tarifa de máquina/gateway', 'within': DLG}, 0.8, at=c.A(4, 'tarifa,', 0.9), label='Tarifa de máquina/gateway')
    c.click(BTN('Vou receber depois', within=DLG), at=c.A(4, 'volto.', 1.0), label='volta para Vou receber depois')
    c.mark(5)
    c.click(BTN('Aprovar e gerar conta a receber', within=DLG), at=c.A(5, 'Aprovar', 0.9), label='Aprovar e gerar conta a receber')
    c.waitfor(gone={'role': 'dialog'}, timeout=15)
    c.confere('row:Hotel Mirante do Mar', ['R$ 3.200,00', 'Aprovado', 'No financeiro'], 'linha do Hotel: Aprovado, No financeiro')
    c.hover({'selector': "main tbody tr:has-text('Hotel Mirante do Mar')", 'hasText': 'No financeiro'}, 1.2, at=c.A(5, 'selo', 0.9), label='a linha ganha o selo No financeiro')
    c.abrir_menu('Hotel Mirante do Mar', 'Ver lançamento no financeiro', at=c.A(5, 'menu,', 0.9), label='menu ⋮ da linha aprovada')
    c.hover(ITEM('Ver lançamento no financeiro'), 1.4, at=c.A(5, 'existir', 0.9), label='item Ver lançamento no financeiro')
    c.press('Escape', at=c.A(5, 'financeiro.', 0.1, nth=1), label='fecha o menu')
    c.mark(6)
    c.hover({'selector': "main tbody tr:has-text('Hotel Mirante do Mar')"}, 2.0, at=c.A(6, 'receita.', 0.9), label='a linha aprovada')
    c.fim()
    return c


def cap15():
    """Gerar a ordem de serviço: Pousada (Aprovado) > Gerar OS, distribui os serviços pelos equipamentos, OS #17 na lista de Ordens de Serviço."""
    c = Cap(15, pace=0.45, start=(760, 420), setup=SETUP_LISTA)
    c.mark(1)
    c.abrir_menu('Pousada Brisa do Mar', 'Gerar OS', at=c.A(1, 'menu', 1.9), label='menu ⋮ da linha da Pousada')
    c.click(ITEM('Gerar OS'), at=c.A(1, 'Gerar', 0.9, nth=1), label='Gerar OS')
    c.waitfor(text='Distribuir serviços', timeout=15)
    c.hover({'text': 'Defina em qual equipamento', 'within': DLG}, 1.4, at=c.A(1, 'equipamento', 0.9), label='Defina em qual equipamento cada serviço será executado')
    c.mark(2)
    c.click(BTN('Todos', within=DLG), at=c.A(2, 'Todos', 0.9), label='Todos: a higienização nos três splits')
    c.click({'selector': f"{DLG} label:has-text('Hi-Wall 12.000 BTUs - Recepção')", 'nth': 1}, at=c.A(2, 'recepção.', 1.2), label='Carga de Gás só no split da recepção')
    c.ev("[...document.querySelectorAll('[role=dialog] button[role=checkbox]')].map(b=>b.getAttribute('aria-checked')).join(',')", label='confere caixas: Higienização nos 3, Carga de Gás só na Recepção (true,true,true,true,false,false)')
    c.mark(3)
    c.click(BTN('Gerar OS', within=DLG), at=c.A(3, 'Clico', 0.9), label='Gerar OS')
    c.waitfor(gone={'role': 'dialog'}, timeout=15)
    c.confere('row:Pousada Brisa do Mar', ['R$ 1.000,00', 'Convertido'], 'linha da Pousada: Convertido')
    c.hover({'selector': "main tbody tr:has-text('Pousada Brisa do Mar')", 'hasText': 'Convertido'}, 0.5, at=c.A(3, 'Convertido.', 0.9), label='a linha passa a Convertido')
    c.mark(4)
    c.add({'do': 'goto', 'url': '/ordens-servico', 'at': c.A(4, 'Na', 0.9) + 0.02, 'label': 'abre Ordens de Serviço (menu lateral recolhido)'})
    c.waitfor(text='HIG-2026-17', timeout=20)
    c.click({'selector': 'main button:has(svg.lucide-layout-list)'}, at=c.A(4, 'OS', -0.2, nth=0), label='visão em lista')
    c.confere('row:HIG-2026-17', ['HIG-2026-17', 'Pousada Brisa do Mar', 'Higienização de Split', 'Agendada'], 'OS #17 na lista: Pousada, Higienização de Split, Agendada')
    # a lista de OS não tem coluna de valor: o valor está no "Visualizar OS" (Total para faturamento)
    KEBAB = {'selector': "main tbody tr:has-text('HIG-2026-17') button[aria-haspopup='menu']"}
    c.click(KEBAB, at=c.A(4, 'agendada,', 1.0), label='menu ⋮ da OS #17')
    c.pause(0.6)
    c.click(KEBAB, label='menu ⋮ da OS #17 de novo (só se não abriu)', unless=ITEM('Visualizar OS'))
    c.click(ITEM('Visualizar OS'), at=c.A(4, 'valor', 0.0), label='Visualizar OS')
    c.waitfor(text='Total para faturamento', timeout=15)
    c.hover(PD('Total para faturamento'), 1.4, label='Total para faturamento R$ 1.000,00')
    c.confere('dlg', ['OS #17', 'Agendada', 'Pousada Brisa do Mar', 'Higienização de Split 3 serviço(s) R$ 180,00 R$ 540,00', 'Carga de Gás 1 serviço(s) R$ 350,00 R$ 350,00', 'Total para faturamento R$ 1.000,00'],
              'OS #17: Agendada, total para faturamento R$ 1.000,00')
    c.mark(5)
    fechar_janela(c, at=c.A(5, 'Uma', 0.3))
    c.fim()
    return c


CAPS = {0: cap00, 1: cap01, 2: cap02, 3: cap03, 4: cap04, 5: cap05, 6: cap06, 7: cap07, 8: cap08, 9: cap09, 10: cap10, 11: cap11, 12: cap12, 13: cap13, 14: cap14, 15: cap15, 16: cap16}

if __name__ == '__main__':
    quais = [int(a) for a in sys.argv[1:]] or sorted(CAPS)
    for n in quais:
        c = CAPS[n]()
        if os.environ.get('ANCHORS'):
            for i, w, t in c.anchors:
                print(f'   anchor L{i} "{w}" -> {t}')
        d = c.out()
        last = -1
        for stp in d['steps']:   # o `at` precisa ser crescente
            if 'at' in stp:
                if stp['at'] < last:
                    print(f'  aviso cap{n:02d}: at {stp["at"]} < {last} em "{stp.get("label") or stp.get("name")}"')
                last = max(last, stp['at'])
        path = os.path.join(HERE, f'cap{n:02d}.json')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
        print(f'cap{n:02d}: {len(d["steps"])} passos, narração {c.dur:.1f} s -> {os.path.relpath(path, HERE)}')
