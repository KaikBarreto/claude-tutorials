#!/usr/bin/env python3
"""T11 · gera rec/t11/cap00..cap14.json (roteiros do robô) a partir da voz pronta (t11/narracao/capNN.json).

Contratos e PMOC, no COMPUTADOR (janela 1280x800, 2x), logada como Camila Duarte (admin, Glacial Cold Brasil), Dominex 1.38.19,
FAKE_NOW 2026-11-10T10:00:00-03:00 (backend 54329 E robô). Gravar com APP_ORIGIN=https://www.dominex.app (o cartão "Portal do Contrato" mostra o link).
Os `at` saem da palavra que anuncia cada passo (A(linha, palavra, folga)); o gesto "pousa" ~0,7 a 1 s depois do início do passo.
Rodar de qualquer pasta: `python3 -I rec/t11/gerar.py [NN ...]`. Depois: `node rec/record.mjs rec/t11/capNN.json --check`.

Cadeia de sementes (rec/t11/cadeia.json, de rec/t11/semear.py): fim do T5 + `t11/inicio` (fim do T10 para esta aula); depois, o último
`t11/apos-capNN` (gerado por `rec/t11/rodar.sh NN --seed`, na mesma trava da gravação). Estado de cada capítulo em SEMENTE.

O assistente "Novo Contrato" (1.38.19: 5 etapas, a mesma para comum e PMOC) atravessa os capítulos 4 a 9 e cada capítulo recomeça num navegador novo:
o `setup` (sem filmar) devolve o rascunho que o capítulo anterior deixou. O rascunho do assistente vive em `sessionStorage['form-draft:contract-form']`
(useFormDraft); o último passo de cada capítulo de 4 a 8 o devolve em `eval` rotulado "rascunho" e `rec/t11/colher.py NN` o guarda em
`rec/t11/_rascunhos/capNN.json`. O `setup` do capítulo seguinte o grava de volta no sessionStorage, abre "Novo Contrato" e aceita "Retomar rascunho".

Particularidades (lições deste tutorial, ver docs/08-licoes.md):
 - Observador `OBS`: guarda em `window.__avisos` todo aviso de erro do app, tela escura e faixa da trilha Domiflix; o eval final do capítulo devolve.
 - O cliente do seletor é um item `cmdk`: clicar por `[cmdk-item]`+texto (o nome do contrato digitado também contém o nome do cliente).
 - Nada de clique que abre outra aba ou baixa arquivo ("Imprimir PDF Anual", "Baixar TRT", "Imprimir QR Code" só recebem o cursor).
"""
import json
import os
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TUT = os.path.normpath(os.path.join(HERE, '..', '..'))
NARR = os.path.join(TUT, 't11', 'narracao')
CAD = json.load(open(os.path.join(HERE, 'cadeia.json'), encoding='utf8'))
BASE = CAD['inicio']
IDS = CAD['ids']
RASC = os.path.join(HERE, '_rascunhos')
STORAGE = {'dominex:portal-tickets-seen:d40f5787-1779-501f-900c-ddb2b90a36e5': '2031-01-01T00:00:00.000Z'}
CARIMBO = 'assets/carimbo-rt.png'  # relativo a esta pasta (o `upload` resolve pela pasta do roteiro)

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

NOMES = ['Abertura', 'Onde fica o PMOC', 'O Responsável Técnico', 'Um contrato comum', 'Ligando o PMOC', 'Unidade e responsável técnico',
         'Ambientes climatizados', 'A frequência da norma', 'Equipe e cobrança', 'Revisão e criação', 'O contrato por dentro', 'O cronograma do ano',
         'Os documentos da norma', 'Renovar, pausar e excluir', 'Recapitulando']
# estado de partida de cada capítulo: o último apos-capNN (de capítulo anterior) que mexeu no banco
SEMENTE = {0: None, 1: None, 2: None, 3: 'apos-cap02', 4: 'apos-cap03', 5: 'apos-cap03', 6: 'apos-cap03', 7: 'apos-cap03', 8: 'apos-cap03',
           9: 'apos-cap03', 10: 'apos-cap09', 11: 'apos-cap09', 12: 'apos-cap09', 13: 'apos-cap12', 14: 'apos-cap12'}


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
        s.prewarm = prewarm or ['/dashboard', '/contratos']
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

    def upload(s, target, file, at=None, label=None, **kw):
        return s._p({'do': 'upload', 'target': target, 'file': file}, at, label, kw)

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
            'name': f't11-cap{s.n:02d}',
            'title': f'T11 · Cap. {s.n} · {NOMES[s.n]} (narração {str(round(s.dur, 1)).replace(".", ",")} s; marcas L1..L{len(s.linhas)} = início de cada linha do roteiro)',
            'seed': f't11-cap{s.n:02d}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
            'start': {'x': s.start[0], 'y': s.start[1]},
            'seedExtra': list(BASE) + ([f't11/{sem}'] if sem else []),
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
AGUARDA = {'do': 'waitFor', 'idle': True}
SETUP_DASH = [{'do': 'goto', 'url': '/dashboard'}, {'do': 'waitFor', 'text': 'Olá, Camila!', 'timeout': 25}, AGUARDA]
SETUP_LISTA = [{'do': 'goto', 'url': '/dashboard'}, {'do': 'waitFor', 'text': 'Olá, Camila!', 'timeout': 25}, AGUARDA,
               {'do': 'goto', 'url': '/contratos'}, {'do': 'waitFor', 'text': 'Gerencie contratos recorrentes e manutenções programadas', 'timeout': 25}, AGUARDA]
PREWARM = ['/dashboard', '/contratos']
RASCUNHO = "sessionStorage.getItem('form-draft:contract-form')"
BTN = lambda n, **kw: {'role': 'button', 'name': n, 'exact': True, **kw}
BTNX = lambda n, **kw: {'role': 'button', 'name': n, **kw}
LINK = lambda n, **kw: {'role': 'link', 'name': n, 'exact': True, **kw}
TAB = lambda n, **kw: {'role': 'tab', 'name': n, 'exact': True, **kw}
ITEM = lambda n, **kw: {'role': 'menuitem', 'name': n, **kw}
OPT = lambda n, **kw: {'role': 'option', 'name': n, **kw}
SW = lambda n, **kw: {'role': 'switch', 'name': n, 'exact': True, **kw}
TXT = lambda t, **kw: {'text': t, 'exact': True, **kw}
P = lambda t, **kw: {'text': t, 'within': 'main', **kw}
PD = lambda t, **kw: {'text': t, 'within': DLG, **kw}
SEL = lambda s, **kw: {'selector': s, **kw}
DLG = '[role=dialog]'
POP = '[data-radix-popper-content-wrapper]'
CLIENTE = lambda nome: {'selector': '[cmdk-item]', 'hasText': nome}
ACOES = lambda nome: {'selector': f"main tbody tr:has-text('{nome}') button[aria-label='Ações']"}
LINHA = lambda nome: {'selector': 'main tbody tr', 'hasText': nome}
ROLA_DLG = "(()=>{const d=document.querySelector('[role=dialog] .overflow-y-auto');if(!d)return 'sem rolagem';d.scrollTo({top:%s,behavior:'%s'});return d.scrollHeight})()"
TOPO = ROLA_DLG % (0, 'auto')

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
    """Abertura: o Dashboard; o cursor desce pelo menu lateral, abre o grupo Gestão e para em Contratos (sem clicar)."""
    c = Cap(0, pace=0.5, start=(760, 420), prewarm=PREWARM, setup=SETUP_DASH)
    c.mark(1)
    c.click(BTN('Gestão'), at=0.3, label='grupo Gestão do menu')
    c.hover(LINK('Contratos'), 0.8, at=c.A(1, 'contratos', 0.8), label='o cursor para em Contratos (sem clicar)')
    c.mark(2)
    c.hover(LINK('Contratos'), 2.0, at=c.A(2, 'PMOC,', 0.9), label='Contratos no grupo Gestão (PMOC)')
    c.mark(3)
    c.hover(LINK('Contratos'), 2.0, at=c.A(3, 'Contratos', 0.9, nth=1), label='Contratos no menu (módulo Gestão de Contratos e PMOC)')
    c.mark(4)
    c.fim()
    return c


def cap01():
    """Onde fica o PMOC: Gestão > Contratos (lista vazia); botões do topo e busca; Filtros: Tipo (PMOC e Comum), Saúde e Status; Aplicar."""
    c = Cap(1, pace=0.5, start=(760, 420), prewarm=PREWARM, setup=SETUP_DASH)
    c.mark(1)
    c.click(BTN('Gestão'), at=0.2, label='grupo Gestão do menu')
    c.click(LINK('Contratos'), at=2.8, label='menu Contratos')
    c.waitfor(text='Nenhum contrato cadastrado', timeout=20)
    c.mark(2)
    c.hover(BTN('Configurações de Contrato'), 0.5, at=c.A(2, 'Configurações', 0.8), label='botão Configurações de Contrato')
    c.hover(BTN('Novo Contrato'), 0.5, at=c.A(2, 'Novo', 0.8), label='botão Novo Contrato')
    c.hover({'placeholder': 'Buscar por nome, cliente ou telefone...'}, 0.5, at=c.A(2, 'busca', 0.8), label='campo de busca')
    c.mark(3)
    c.click(BTNX('Filtros'), at=c.A(3, 'Filtros', 1.4), label='abre o painel Filtros')
    c.waitfor(text='Aplicar', timeout=8)
    c.hover(PD('Tipo', exact=True), 1.2, at=c.A(3, 'Tipo,', 0.9, nth=1), label='filtro Tipo (PMOC e Comum)')
    c.mark(4)
    c.hover(PD('Saúde', exact=True), 0.9, at=c.A(4, 'Saúde', 0.9), label='filtro Saúde')
    c.hover(PD('Status', exact=True), 0.9, at=c.A(4, 'Status', 0.9), label='filtro Status')
    c.click(BTN('Aplicar'), at=round(c.dur - 2.4, 2), label='Aplicar (fecha o painel sem filtrar)', noScroll=True)
    c.fim()
    return c


def cap02():
    """O Responsável Técnico: Configurações de Contrato (Documentos), aba Responsáveis Técnicos, Novo Responsável, assinatura desenhada, carimbo, Cadastrar."""
    c = Cap(2, pace=0.5, start=(760, 420), prewarm=PREWARM + ['/contratos'], setup=SETUP_LISTA)
    c.mark(1)
    c.click(BTN('Configurações de Contrato'), at=c.A(1, 'Abro', 0.9), label='Configurações de Contrato')
    c.waitfor(text='Documentos e responsáveis técnicos', timeout=15)
    c.hover(TXT('Modelos padrão de documentos PMOC'), 1.4, at=c.A(1, 'modelos', 0.9), label='Modelos padrão de documentos PMOC')
    c.scroll(TXT('Validade dos documentos'), at=c.A(1, 'Validade', 1.6), label='desce até Validade dos documentos', duration=1.0)
    c.hover(TXT('Validade dos documentos'), 1.6, at=c.A(1, 'Validade', 0.5), label='Validade dos documentos (12 meses)')
    c.mark(2)
    c.click(TAB('Responsáveis Técnicos'), at=c.A(2, 'segunda', 1.0), label='aba Responsáveis Técnicos')
    c.waitfor(text='Nenhum responsável técnico cadastrado', timeout=10)
    c.hover(BTN('Novo Responsável'), 1.4, at=c.A(2, 'engenheiro', 0.9), label='botão Novo Responsável')
    c.mark(3)
    c.click(BTN('Novo Responsável'), at=c.A(3, 'Clico', 1.0), label='Novo Responsável')
    c.waitfor(text='Novo Responsável Técnico', timeout=10)
    CAMPO = lambda ph: {'selector': f"{DLG} input[placeholder='{ph}']"}
    c.type(CAMPO('Ex: João da Silva'), 'Ricardo Tavares Albuquerque', at=c.A(3, 'Nome', 0.5), cps=40, label='Nome completo')
    c.type(CAMPO('Ex: CREA-SP 1234567'), 'CREA-RJ 9000012345', at=c.A(3, 'CFT', 0.4), cps=40, label='CFT/CREA')
    c.type(CAMPO('Ex: Engenheiro Mecânico'), 'Engenheiro Mecânico', at=c.A(3, 'Modalidade', 0.4), cps=40, label='Modalidade')
    c.type(CAMPO('Ex: ART 1234567/2026'), 'ART 9000001234/2026', at=c.A(3, 'Número', 0.4), cps=40, label='Número de registro')
    c.type(CAMPO('email@exemplo.com.br'), 'ricardo@glacialcold.example', at=c.A(3, 'Email', 1.6), cps=40, label='Email')
    c.type(CAMPO('(21) 99999-9999'), '2130001009', at=c.A(3, 'Telefone', 0.4), cps=40, label='Telefone')
    c.mark(4)
    c.hover(TAB('Enviar imagem'), 1.0, at=c.A(4, 'Assinatura', 0.9), label='aba Enviar imagem (recomendada)')
    c.click(TAB('Desenhar'), at=c.A(4, 'Desenhar', 1.0), label='aba Desenhar')
    c.waitfor(text='Desenhe acima usando o dedo, mouse ou caneta.', timeout=8)
    # assinatura: alguns arrastos curtos sobre o quadro (cada um parte de um ponto perto do centro)
    CANVAS = SEL(f'{DLG} canvas')
    for k, (x, y) in enumerate([(450, 600), (850, 655)]):   # px CSS dentro do quadro (x 367..917, y 549..689)
        c.drag(CANVAS, {'x': x, 'y': y}, at=round(c.A(4, 'assino', 0.7) + k * 0.5, 2) if k == 0 else None, label=f'assina no quadro ({k + 1})')
    c.click(BTN('Salvar imagem'), at=c.A(4, 'Salvar', 1.0), label='Salvar imagem')
    c.mark(5)
    c.ev("'dump RT: ' + [...document.querySelector('[role=dialog]').querySelectorAll('label,button')].map(e => e.tagName + ':' + e.innerText.trim().slice(0, 40)).join(' | ')", label='dump RT depois da assinatura')
    c.upload(SEL(f"{DLG} label:has-text('Selecionar') >> nth=-1"), CARIMBO, at=c.A(5, 'envio', 1.0), label='Carimbo do responsável (Selecionar)')
    c.click(BTN('Cadastrar responsável'), at=c.A(5, 'Cadastrar', 1.0), label='Cadastrar responsável')
    c.waitfor(text='Ricardo Tavares Albuquerque', timeout=15)
    c.mark(6)
    c.hover(TXT('Ricardo Tavares Albuquerque', within='main'), 1.6, at=c.A(6, 'Ricardo', 0.9), label='o Ricardo na lista')
    c.fim()
    return c


def passar_pela_barra(c, at, label='a barra de cinco etapas', passo=0.45):
    """o cursor passa pelos nomes das cinco etapas do assistente"""
    for k, nome in enumerate(['Dados do contrato', 'Escopo técnico', 'Agenda', 'Operação e cobrança', 'Revisão']):
        c.hover(SEL(f'{DLG} button', hasText=nome, nth=0), 0.1, at=round(at + k * passo, 2), label=f'{label}: {nome}')


def abrir_assistente(c, at, label='Novo Contrato'):
    c.click(BTN('Novo Contrato'), at=at, label=label)
    c.waitfor(text='Dados do contrato', timeout=15)


def confere_campos(c, esperados, label):
    """como `confere`, mas lê os VALORES dos campos (input/textarea) da primeira janela: DIFERENTE se algum esperado não aparece em nenhum campo"""
    js = ("(async()=>{const esp=%s;let out='';for(let i=0;i<14;i++){const d=document.querySelector('[role=dialog]');"
          "const vs=d?[...d.querySelectorAll('input,textarea')].map(x=>x.value.trim().toLowerCase()):[];"
          "const falta=esp.filter(e=>{e=e.toLowerCase();return !vs.some(x=>x===e||(e.length>3&&x.includes(e)))});"
          "if(!falta.length)return 'OK: '+esp.join(' | ');out='DIFERENTE: faltou '+JSON.stringify(falta)+' nos campos: '+vs.join(' | ').slice(0,260);"
          "await new Promise(r=>setTimeout(r,300));}return out})()") % json.dumps(esperados, ensure_ascii=False)
    return c.add({'do': 'eval', 'js': js, 'label': 'confere ' + label})


TOASTS_OBS = ("(()=>{window.__toasts=[];new MutationObserver(ms=>{for(const m of ms)m.addedNodes.forEach(n=>{const t=(n.textContent||'').trim();"
              "if(t&&t.length<300&&/OSs?\\b|parcelas|Gerando|criado/i.test(t))window.__toasts.push(t.replace(/\\s+/g,' '))})}).observe(document.body,{childList:true,subtree:true});return 1})()")


def confere_aviso(c, ancora, esperados, label):
    """lê os avisos (toasts) que apareceram desde o observador `TOASTS_OBS` (guardados em window.__toasts) e compara com o que a fala diz:
    "OK: <aviso>" ou "DIFERENTE: <avisos lidos>" (procura por `ancora`, espera até ~10 s)"""
    js = ("(async()=>{const esp=%s;let ctx='sem aviso';for(let i=0;i<40;i++){const l=(window.__toasts||[]).filter(t=>t.includes(%s));"
          "if(l.length){ctx=l[0].slice(0,170);const falta=esp.filter(e=>!l.some(t=>t.includes(e)));"
          "return (falta.length?'DIFERENTE: faltou '+JSON.stringify(falta)+' em: ':'OK: ')+ctx}await new Promise(r=>setTimeout(r,250));}"
          "return 'DIFERENTE: sem aviso com '+%s+' | todos: '+JSON.stringify(window.__toasts||[]).slice(0,300)})()") % (json.dumps(esperados, ensure_ascii=False), json.dumps(ancora), json.dumps(ancora))
    return c.add({'do': 'eval', 'js': js, 'label': 'confere ' + label})


def escolher_cliente(c, nome, busca, at_abre, at_busca, at_escolhe):
    c.click(TXT('Selecione o cliente', within=DLG), at=at_abre, label='abre a lista de Cliente')
    c.type({'placeholder': 'Buscar cliente...'}, busca, at=at_busca, cps=40, label=f'busca "{busca}"', noScroll=True)
    c.click(CLIENTE(nome), at=at_escolhe, label=f'escolhe {nome}', noScroll=True)


NOME_CONTRATO = SEL(f'{DLG} input', nth=0)
# placeholder EXATO: 'Ex: 12' (ocupantes fixos) também casa por substring com 'Ex: 120,5' (área)
CAMPO_FIXOS = SEL(f"{DLG} input[placeholder='Ex: 12']")
CAMPO_FLUT = SEL(f"{DLG} input[placeholder='Ex: 30']")
CAMPO_TR = SEL(f"{DLG} input[placeholder='Ex: 5,0']")
CALC_LARGURA = SEL("[role=dialog]:has-text('Calcular área climatizada') input", nth=0)
CALC_COMPRIMENTO = SEL("[role=dialog]:has-text('Calcular área climatizada') input", nth=1)
CHAVE_PMOC = SEL(f'{DLG} [role=switch]', nth=0)
PROXIMO = BTN('Próximo')


def cap03():
    """Um contrato comum: Novo Contrato > Dados > Escopo técnico (Hi-Wall do colégio) > Agenda (Trimestral) > Operação e cobrança > Revisão > Criar Contrato."""
    c = Cap(3, pace=0.5, start=(760, 420), prewarm=PREWARM, setup=SETUP_LISTA)
    c.mark(1)
    abrir_assistente(c, c.A(1, 'Clico', 1.6))
    c.mark(2)
    c.type(NOME_CONTRATO, 'Manutenção preventiva trimestral - Colégio Monte Verde', at=c.A(2, 'escrevo', 0.9), cps=40, label='Nome do Contrato')
    escolher_cliente(c, 'Colégio Monte Verde', 'Colégio', c.A(2, 'Cliente', 1.3), c.A(2, 'Cliente', 0.4), c.A(2, 'escolho', 0.2))
    c.hover(CHAVE_PMOC, 1.4, at=c.A(2, 'chave', 0.9), label='chave É um contrato PMOC? (desligada)')
    passar_pela_barra(c, c.A(2, 'cinco', 0.7))
    c.click(PROXIMO, at=round(c.L(3) - 1.3, 2), label='Próximo (Escopo técnico)')
    c.mark(3)
    c.waitfor(text='Equipamentos e escopo', timeout=10)
    c.click(BTN('Adicionar equipamento sem ambiente'), at=c.A(3, 'Adicionar', 0.9), label='Adicionar equipamento sem ambiente')
    c.waitfor(text='Adicionar equipamento ao contrato', timeout=10)
    c.click(TXT('Hi-Wall 18.000 BTUs - Sala dos professores'), at=c.A(3, 'Hi-Wall', 0.9), label='marca o Hi-Wall 18.000 BTUs da sala dos professores')
    c.click(BTN('Adicionar 1 equipamento'), at=c.A(3, 'professores.', 0.8), label='Adicionar 1 equipamento')
    c.waitfor(text='Equipamentos não atribuídos', timeout=10)
    c.click(PROXIMO, at=round(c.L(4) - 1.3, 2), label='Próximo (Agenda)')
    c.mark(4)
    c.waitfor(text='Defina a cadência', timeout=10)
    c.click(BTN('Trimestral'), at=c.A(4, 'Trimestral', 0.9), label='atalho Trimestral')
    c.click(SEL(f'{DLG} button', hasText='/2026', nth=0), at=c.A(4, 'Escolho', 0.9), label='Data de Início (abre o calendário)')
    c.click(SEL(f'{POP} button', nth=1), at=c.A(4, 'Data', 1.0), label='próximo mês no calendário')
    c.click({'role': 'gridcell', 'name': '15', 'exact': True}, at=c.A(4, 'Início', 0.4), label='escolhe o dia 15')
    c.hover(PD('Prévia das datas'), 1.0, at=c.A(4, 'Prévia', 0.8), label='Prévia das datas')
    c.confere('wiz', ['Prévia das datas (5)', '15/12/2026'], 'cap03: a prévia mostra cada visita com o dia da semana (5 datas)')
    c.ev("(() => { const t = document.querySelector('[role=dialog]').innerText; return 'dump prévia: ' + (t.match(/Prévia das datas \\(\\d+\\)/) || ['?'])[0] + ' | ' + (t.match(/= \\d+ [a-zç()]+/) || ['?'])[0] + ' | ' + (t.match(/\\d\\d\\/\\d\\d\\/\\d{4}/g) || []).join(' '); })()", label='dump prévia das datas')
    c.click(PROXIMO, at=round(c.L(5) - 2.3, 2), label='Próximo (Operação e cobrança)')
    c.mark(5)
    c.waitfor(text='Técnicos Executores', timeout=10)
    c.ev("(()=>JSON.stringify({dump:'executores', html:(document.querySelector('[data-contract-validation=executors]')||{}).innerHTML?.slice(0,900)}))()", label='dump executores')
    c.click(SEL(f'{DLG} [data-contract-validation=executors] button[role=combobox]', nth=0), at=c.A(5, 'Executor', 0.9), label='abre Técnicos Executores')
    c.ev("'dump executores aberto: ' + [...document.querySelectorAll('[data-radix-popper-content-wrapper]')].map(e => e.innerText.replace(/\\s+/g, ' ').slice(0, 300)).join(' ## ')", label='dump lista de técnicos')
    c.click(TXT('Rafael Lima', within=POP), at=c.A(5, 'Rafael', 0.9), label='marca Rafael Lima')
    c.press('Escape', at=c.A(5, 'Lima.', 0.2), label='fecha a lista de técnicos')
    c.click(SEL(f'{DLG} button[role=combobox]', nth=2), at=c.A(5, 'Tipo', 0.9), label='abre Tipo de Serviço')
    c.click(OPT('Manutenção Preventiva', exact=False), at=c.A(5, 'Manutenção', 0.9), label='Manutenção Preventiva')
    # o Checklist Padrão mora na etapa anterior (Escopo técnico): volta pela barra, escolhe e retorna
    c.click(SEL(f'{DLG} button', hasText='Escopo técnico', nth=0), at=c.A(5, 'Checklist', 1.0), label='volta ao Escopo técnico (onde mora o Checklist Padrão)')
    c.click(SEL(f'{DLG} button[role=combobox]', hasText='Nenhum', nth=0), at=c.A(5, 'Padrão,', 0.4), label='abre Checklist Padrão')
    c.click(OPT('Manutenção preventiva de split', exact=False), at=c.A(5, 'manutenção', 0.3, nth=1), label='Manutenção preventiva de split')
    c.click(SEL(f'{DLG} button', hasText='Operação e cobrança', nth=0), at=c.A(5, 'tutorial', 0.9), label='volta a Operação e cobrança')
    c.hover(P('Contrato Ativo', within=DLG), 1.6, at=c.A(5, 'Ativo', 0.9), label='chave Contrato Ativo')
    c.mark(6)
    c.rolar(520, at=c.A(6, 'embaixo,', 0.9), label='desce até a Configuração financeira', ponto=(760, 480))
    c.hover(PD('Já gerar as parcelas a receber'), 2.2, at=c.A(6, 'Já', 0.9), label='Já gerar as parcelas a receber (desligado)')
    c.click(PROXIMO, at=round(c.L(7) - 1.3, 2), label='Próximo (Revisão)')
    c.mark(7)
    c.waitfor(text='Revisão final', timeout=10)
    c.hover(PD('Revisão final'), 0.4, at=c.A(7, 'Revisão', 0.9), label='Revisão final')
    c.ev(TOASTS_OBS, label='observador dos avisos')
    c.click(BTNX('Criar Contrato'), at=c.A(7, 'Criar', 0.9), label='Criar Contrato')
    c.waitfor(text='Visão Geral', timeout=30)
    confere_aviso(c, 'OSs geradas', ['5 OSs geradas'], 'cap03: o aviso diz 5 OSs (a fala não cita o número)')
    c.fim()
    return c


# ---------------------------------------------------------------- assistente do PMOC (capítulos 4 a 9): retomada do rascunho (sem filmar)
def rascunho_de(n):
    """rascunho que o capítulo `n` deixou no sessionStorage (rec/t11/colher.py n); sem ele o setup avisa e o ensaio falha de propósito"""
    p = os.path.join(RASC, f'cap{n:02d}.json')
    if not os.path.exists(p):
        print(f'  AVISO: falta {os.path.relpath(p, HERE)}: rode o capítulo {n} (--rapido) e `python3 -I rec/t11/colher.py {n}`')
        return None
    return json.load(open(p, encoding='utf8'))['draft']


def setup_retomar(n_anterior, avancar=0):
    """lista de Contratos > Novo Contrato > Retomar rascunho (o que o capítulo anterior deixou) > `avancar` cliques em Próximo"""
    raw = rascunho_de(n_anterior)
    passos = list(SETUP_LISTA)
    passos.append({'do': 'eval', 'js': f"(() => {{ sessionStorage.setItem('form-draft:contract-form', {json.dumps(raw if raw else '{}')}); return 'rascunho gravado'; }})()"})
    passos += [{'do': 'click', 'target': BTN('Novo Contrato')}, {'do': 'waitFor', 'text': 'Rascunho encontrado', 'timeout': 15},
               {'do': 'click', 'target': BTN('Retomar rascunho')}, {'do': 'waitFor', 'text': 'Dados do contrato', 'timeout': 15}, AGUARDA,
               {'do': 'pause', 'seconds': 1.0}]
    for _ in range(avancar):
        passos += [{'do': 'click', 'target': PROXIMO}, {'do': 'pause', 'seconds': 1.2}]
    return passos


def rascunho_fim(c):
    """último passo de um capítulo da cadeia do assistente: devolve o rascunho (rec/t11/colher.py o guarda)"""
    c.s_rascunho = True
    return c.ev(RASCUNHO, label='rascunho')


def cap04():
    """Ligando o PMOC: Novo Contrato > nome e cliente do hotel > chave "É um contrato PMOC?" > a Unidade e o RT aparecem em Dados do contrato (não avança)."""
    c = Cap(4, pace=0.5, start=(760, 420), prewarm=PREWARM, setup=SETUP_LISTA)
    c.mark(1)
    abrir_assistente(c, c.A(1, 'Clico', 1.6))
    c.mark(2)
    c.type(NOME_CONTRATO, 'PMOC - Hotel Mirante do Mar', at=c.A(2, 'PMOC,', 0.9), cps=18, label='Nome do Contrato')
    escolher_cliente(c, 'Hotel Mirante do Mar', 'Hotel', c.A(2, 'Cliente.', 1.6), c.A(2, 'Cliente.', 0.7), c.A(2, 'próprio', 0.3))
    c.mark(3)
    c.hover(CHAVE_PMOC, 1.2, at=c.A(3, 'chave', 0.9), label='chave É um contrato PMOC?')
    c.click(CHAVE_PMOC, at=c.A(3, 'Ligando,', 0.9), label='liga É um contrato PMOC?')
    c.mark(4)
    c.rolar(430, at=c.A(4, 'Repara', 0.6), label='desce até o RT e a Identificação da Unidade', ponto=(640, 470), duration=0.7)
    c.hover(PD('Identificação da Unidade'), 2.2, at=c.A(4, 'Unidade', 0.8), label='Identificação da Unidade')
    c.hover(SEL(f'{DLG} button', hasText='Revisão', nth=0), 1.2, at=c.A(4, 'cinco', 0.9), label='a barra segue com as cinco etapas')
    rascunho_fim(c)
    c.fim()
    return c


def cap05():
    """Unidade e RT: escolhe o Ricardo, a dica do ícone, o nome da unidade, o selo da lei e "O que o PMOC desbloqueia"; Próximo (Escopo técnico)."""
    c = Cap(5, pace=0.5, start=(760, 420), prewarm=PREWARM, setup=setup_retomar(4))
    c.mark(1)
    c.rolar(430, at=0.3, label='desce até o RT e a Identificação da Unidade', ponto=(640, 470), duration=0.7)
    c.click({'selector': f'{DLG} button[role=combobox]', 'hasText': 'Sem RT atribuído'}, at=c.A(1, 'escolho', 0.9), label='abre Responsável Técnico (RT)')
    c.click(OPT('Ricardo', exact=False), at=c.A(1, 'Ricardo,', 0.8), label='escolhe o Ricardo')
    c.hover(BTN('Cadastrar novo Responsável Técnico'), 1.4, at=c.A(1, 'botão', 0.8), label='botão + (Cadastrar novo Responsável Técnico, sem clicar)')
    c.mark(2)
    c.hover(BTN('O que é Responsável Técnico?'), 3.6, at=c.A(2, 'Passando', 0.9), label='ícone de informação do RT (a dica)')
    c.mark(3)
    c.rolar(260, at=c.A(3, 'Embaixo,', 0.8), label='desce até a Identificação da Unidade', ponto=(640, 470), duration=0.6)
    c.hover(PD('Endereço (logradouro)'), 1.6, at=c.A(3, 'endereço', 0.9), label='endereço da unidade')
    confere_campos(c, ['Avenida Quintino Bocaiúva', '770', 'São Francisco', 'Niterói'], 'cap05: a unidade já vem com o endereço do hotel (a fala diz que vem preenchido)')
    c.type({'placeholder': 'Ex: Loja Centro, Galpão 2…'}, 'Hotel Mirante do Mar - São Francisco', at=c.A(3, 'nome', 0.8, nth=0), cps=40, label='Nome da unidade / local')
    c.mark(4)
    c.rolar(300, at=c.A(4, 'Conforme', 1.0), label='desce até o selo da lei', ponto=(640, 470), duration=0.6)
    c.hover(PD('Conforme Lei Federal 13.589/2018'), 2.2, at=c.A(4, 'Conforme', 0.6), label='selo Conforme Lei Federal 13.589/2018')
    c.hover(PD('O que o PMOC desbloqueia'), 3.0, at=c.A(4, 'quadro', 0.9), label='quadro O que o PMOC desbloqueia')
    c.click(PROXIMO, at=round(c.dur - 1.6, 2), label='Próximo (Escopo técnico)')
    c.waitfor(text='Ambientes e equipamentos', timeout=10)
    rascunho_fim(c)
    c.fim()
    return c


def montar_ambiente(c, ident, tipo, largura, comprimento, tr, fixos, flut, equipamentos, em=None):
    """Monta um ambiente PMOC sem esperar a fala (os trechos 'em' = dict de instantes opcionais); usado para o Restaurante e o Salão (corte 4x)."""
    c.click(BTN('Adicionar ambiente'), label=f'Adicionar ambiente ({ident})')
    c.waitfor(text='Voltar aos ambientes', timeout=10)
    c.type({'placeholder': 'Ex: 2º andar — Sala 201'}, ident, cps=40, label=f'identificação: {ident}')
    c.type({'placeholder': 'Ex: Escritório administrativo'}, tipo, cps=40, label=f'tipo de atividade: {tipo}')
    c.click(SEL(f'{DLG} button', hasText='Calcular', nth=0), label='Calcular a área')
    c.waitfor(text='Calcular área climatizada', timeout=8)
    c.digitar_num(CALC_LARGURA, str(largura), label='largura')
    c.digitar_num(CALC_COMPRIMENTO, str(comprimento), label='comprimento')
    c.click(BTN('Usar'), label='Usar a área calculada')
    c.digitar_num(CAMPO_TR, str(tr), label='carga térmica (TR)')
    c.digitar_num(CAMPO_FIXOS, str(fixos), label='ocupantes fixos')
    c.digitar_num(CAMPO_FLUT, str(flut), label='ocupantes flutuantes')
    confere_campos(c, [ident, tipo, str(round(largura * comprimento)), str(tr), str(fixos), str(flut)], f'cap06: campos do ambiente {ident}')
    c.click(SEL(f'{DLG} button', hasText='Adicionar equipamento', nth=0), label='Adicionar equipamento ao ambiente')
    c.waitfor(text='Adicionar equipamento ao ambiente', timeout=8)
    for nome in equipamentos:
        c.click(TXT(nome), label=f'marca {nome}')
    c.click(BTNX('Adicionar', exact=False, name='Adicionar ' + str(len(equipamentos)) + (' equipamento' if len(equipamentos) == 1 else ' equipamentos')),
            label=f'Adicionar {len(equipamentos)} equipamento(s)')


def cap06():
    """Ambientes climatizados: Adicionar ambiente (Lobby e recepção: área pela calculadora, TR, ocupantes, duas máquinas), a rotina da norma da máquina; Restaurante e Salão (corte 4x)."""
    c = Cap(6, pace=0.5, start=(760, 420), prewarm=PREWARM, setup=setup_retomar(5))
    c.mark(1)
    c.waitfor(text='Ambientes climatizados', timeout=10)
    c.click(BTN('Adicionar ambiente'), at=c.A(1, 'Adicionar', 0.9), label='Adicionar ambiente')
    c.waitfor(text='Voltar aos ambientes', timeout=10)
    c.type({'placeholder': 'Ex: 2º andar — Sala 201'}, 'Lobby e recepção', at=c.A(1, 'Lobby', 1.5), cps=40, label='Identificação do ambiente')
    c.type({'placeholder': 'Ex: Escritório administrativo'}, 'Recepção de hotel', at=c.A(1, 'Recepção', 1.0), cps=40, label='Tipo de atividade')
    c.mark(2)
    c.click(SEL(f'{DLG} button', hasText='Calcular', nth=0), at=c.A(2, 'Calcular', 1.0), label='Calcular a área')
    c.waitfor(text='Calcular área climatizada', timeout=8)
    c.digitar_num(CALC_LARGURA, '12', at=c.A(2, 'Largura', 0.8), label='largura 12')
    c.digitar_num(CALC_COMPRIMENTO, '15', at=c.A(2, 'comprimento', 0.8), label='comprimento 15')
    c.hover(PD('Área climatizada'), 1.0, at=c.A(2, 'resultado', 0.8), label='o resultado: 180 m²')
    c.confere('dlg', ['180'], 'cap06: o cálculo dá 180 m²')
    c.click(BTN('Usar'), at=c.A(2, 'Usar.', 0.9), label='Usar')
    c.mark(3)
    c.digitar_num(CAMPO_TR, '4', at=c.A(3, 'escrevo', 0.9), label='Carga térmica 4 TR')
    c.hover(BTN('O que é TR?'), 2.4, at=c.A(3, 'Cada', 0.9), label='dica do TR (1 TR = 12.000 BTU/h)')
    c.hover(PD('= 48.000 BTUs'), 1.6, at=c.A(3, 'próprio', 0.5), label='o campo mostra 48.000 BTUs', optional=True)
    c.confere('wiz', ['48.000 BTUs'], 'cap06: o campo da carga térmica mostra 48.000 BTUs')
    c.mark(4)
    c.digitar_num(CAMPO_FIXOS, '4', at=c.A(4, 'quatro', 0.9), label='ocupantes fixos 4')
    c.digitar_num(CAMPO_FLUT, '40', at=c.A(4, 'quarenta', 0.9), label='ocupantes flutuantes 40')
    confere_campos(c, ['Lobby e recepção', 'Recepção de hotel', '180', '4', '40'], 'cap06: os campos do ambiente (180 m², 4 TR, 4 e 40 ocupantes)')
    c.mark(5)
    c.click(SEL(f'{DLG} button', hasText='Adicionar equipamento', nth=0), at=c.A(5, 'Adicionar', 0.9), label='Adicionar equipamento')
    c.waitfor(text='Adicionar equipamento ao ambiente', timeout=8)
    c.click(TXT('Cassete 36.000 BTUs - Lobby'), at=c.A(5, 'Cassete', 0.9), label='marca o Cassete 36.000 BTUs do lobby')
    c.click(TXT('Hi-Wall 12.000 BTUs - Recepção'), at=c.A(5, 'Hi-Wall', 0.9), label='marca o Hi-Wall 12.000 BTUs da recepção')
    c.click(BTN('Adicionar 2 equipamentos'), at=c.A(5, 'confirmo.', 0.9), label='Adicionar 2 equipamentos')
    c.mark(6)
    c.click(TXT('Cassete 36.000 BTUs - Lobby', within=DLG), at=c.A(6, 'Abrindo', 0.9), label='abre o Cassete 36.000 BTUs do lobby')
    c.hover(PD('Escopo da norma'), 1.0, at=c.A(6, 'Escopo', 0.8), label='Escopo da norma')
    c.hover(PD('Expansão Direta'), 2.0, at=c.A(6, 'Expansão', 0.8), label='Expansão Direta (marcada)')
    c.confere('wiz', ['Escopo da norma', 'Expansão Direta', 'Sistemas Centrais'], 'cap06: a máquina mostra o Escopo da norma')
    c.hover(PD('Sistemas Centrais'), 1.6, at=c.A(6, 'Sistemas', 0.8), label='Sistemas Centrais (não troca)')
    c.mark(7)
    c.waitfor(text='Checklists da norma', timeout=15)
    c.hover(PD('Checklists da norma'), 2.4, at=c.A(7, 'checklist', 0.8), label='Checklists da norma desta máquina (Essencial)')
    c.confere('wiz', ['Essencial'], 'cap06: o checklist Essencial da norma já vem escolhido')
    c.hover(PD('Na 1ª OS?'), 1.6, at=c.A(7, 'primeira', 0.9), label='coluna Na 1ª OS?', optional=True)
    c.rolar(350, at=c.A(7, 'Checklists', 2.4), label='desce até Checklists personalizados', ponto=(760, 470), duration=0.7)
    c.hover(PD('Checklists personalizados'), 0.5, at=c.A(7, 'Checklists', 0.9), label='Checklists personalizados desta máquina')
    c.mark(8)
    c.rolar(-350, at=c.A(8, 'Restaurante', 1.2), label='volta ao topo da máquina', ponto=(760, 470), duration=0.6)
    c.click(BTN('Voltar aos ambientes'), at=c.A(8, 'seguem', 0.6), label='Voltar aos ambientes')
    # corte 4x: o robô monta os outros dois ambientes sem esperar a fala
    montar_ambiente(c, 'Restaurante', 'Restaurante do hotel', 20, 11, 3, 10, 80, ['Cassete 36.000 BTUs - Restaurante do hotel'])
    c.click(BTN('Voltar aos ambientes'), label='Voltar aos ambientes')
    montar_ambiente(c, 'Salão de eventos', 'Salão de eventos', 15, 20, 4, 2, 150, ['Piso-Teto 48.000 BTUs - Salão de eventos'])
    c.click(BTN('Voltar aos ambientes'), label='Voltar aos ambientes')
    c.hover(PD('equipamento(s) no total entram neste contrato'), 2.0, label='4 equipamentos no total')
    rascunho_fim(c)
    c.fim()
    return c


def cap07():
    """A frequência da norma: Agenda (Mensal marcado, faixa Cadência das visitas), Data de Início 01/12, Horizonte 12, Prévia (Lista e Calendário), Rotina por equipamento."""
    c = Cap(7, pace=0.5, start=(760, 420), prewarm=PREWARM, setup=setup_retomar(6, avancar=1))
    c.mark(1)
    c.waitfor(text='Defina a cadência', timeout=10)
    c.hover(BTN('Mensal'), 1.6, at=c.A(1, 'atalho', 0.9), label='atalho Mensal (já marcado)')
    c.hover(PD('Cadência das visitas'), 2.4, at=c.A(1, 'Cadência', 0.9), label='faixa Cadência das visitas')
    c.mark(2)
    c.hover(PD('Cadência das visitas'), 3.0, at=c.A(2, 'norma', 0.9), label='a norma recomenda mensal')
    c.mark(3)
    c.click(SEL(f'{DLG} button', hasText='/2026', nth=0), at=c.A(3, 'Escolho', 0.9), label='Data de Início (abre o calendário)')
    c.click(SEL(f'{POP} button', nth=1), at=c.A(3, 'Data', 0.9), label='próximo mês no calendário')
    c.click({'role': 'gridcell', 'name': '1', 'exact': True}, at=c.A(3, 'Início', 0.4), label='escolhe o dia 1')
    c.hover(PD('Horizonte (meses)'), 1.2, at=c.A(3, 'Horizonte', 0.8), label='Horizonte (meses)')
    c.ev("(() => { const t = document.querySelector('[role=dialog]').innerText; const i = t.indexOf('Horizonte'); return 'dump agenda: ' + t.slice(i, i + 1600).replace(/\\s+/g, ' ') + ' || botoes: ' + [...document.querySelectorAll('[role=dialog] button')].map(b => (b.getAttribute('aria-label') || b.innerText).trim().slice(0, 30)).join(' | '); })()", label='dump agenda pmoc')
    c.mark(4)
    c.hover(PD('Prévia das datas'), 1.6, at=c.A(4, 'Prévia', 0.8), label='Prévia das datas (a tela traz só a lista de datas, sem Lista/Calendário)')
    c.confere('wiz', ['Prévia das datas (13)', '01/12/2026'], 'cap07: a prévia mostra cada visita com o dia da semana (13 datas)')
    c.rolar(300, at=c.A(4, 'Fim', 1.8, nth=0), label='mostra o selo Fim de semana', ponto=(640, 470), duration=0.6)
    c.hover(PD('Fim de semana'), 1.6, at=c.A(4, 'Fim', 0.6, nth=0), label='selo Fim de semana')
    c.mark(5)
    c.rolar(600, at=c.A(5, 'Embaixo,', 0.8), label='desce até Rotina por equipamento', ponto=(640, 470), duration=0.8)
    c.hover(PD('Rotina por equipamento'), 3.0, at=c.A(5, 'Rotina', 0.9), label='faixa Rotina por equipamento')
    c.click(PROXIMO, at=round(c.dur - 1.3, 2), label='Próximo (Operação e cobrança)')
    c.waitfor(text='Técnicos Executores', timeout=10)
    rascunho_fim(c)
    c.fim()
    return c


def cap08():
    """Equipe e cobrança: Rafael e Bruno, Tatiane, Contrato Ativo; Configuração financeira (parcelas de R$ 1.200,00, 10/12, 12 parcelas, Conta Principal, Contratos PMOC); Como vai ficar."""
    c = Cap(8, pace=0.5, start=(760, 420), prewarm=PREWARM, setup=setup_retomar(7))
    c.mark(1)
    c.waitfor(text='Técnicos Executores', timeout=10)
    EXEC = SEL(f'{DLG} [data-contract-validation=executors] button[role=combobox]', nth=0)
    c.click(EXEC, at=c.A(1, 'Técnicos', 0.9), label='abre Técnicos Executores')
    c.click(TXT('Rafael Lima', within=POP), at=c.A(1, 'Rafael', 0.9), label='marca Rafael Lima')
    c.click(TXT('Bruno Alves', within=POP), at=c.A(1, 'Bruno', 0.9), label='marca Bruno Alves')
    c.press('Escape', at=c.A(1, 'campo.', 0.2), label='fecha a lista')
    c.click(SEL(f'{DLG} button[role=combobox]', nth=1), at=c.A(1, 'Responsáveis', 0.9), label='abre Responsáveis Financeiros (Cobrança)')
    c.click(TXT('Tatiane Ribeiro', within=POP), at=c.A(1, 'Tatiane', 0.9), label='marca Tatiane Ribeiro')
    c.press('Escape', at=c.A(1, 'cobrança.', 0.2, nth=1), label='fecha a lista')
    c.hover(P('Contrato Ativo', within=DLG), 1.4, at=c.A(1, 'Ativo', 0.9), label='chave Contrato Ativo (ligada)')
    c.mark(2)
    c.rolar(520, at=c.A(2, 'embaixo,', 0.9), label='desce até a Configuração financeira', ponto=(640, 470), duration=0.8)
    c.click(SEL(f'{DLG} [data-contract-validation=finance] [role=switch]', nth=0), at=c.A(2, 'ligo', 0.9), label='liga Já gerar as parcelas a receber')
    c.mark(3)
    c.digitar_num({'placeholder': 'Mensalidade do contrato'}, 'Mensalidade PMOC', at=c.A(3, 'Descrição', 0.9), label='Descrição da parcela')
    c.type(SEL(f'{DLG} [data-contract-validation=finance] input', nth=1), '120000', at=c.A(3, 'Valor', 0.9), cps=9, label='Valor de cada parcela')
    c.hover(PD('Cada parcela nasce com este valor'), 1.6, at=c.A(3, 'Esse', 0.8), label='dica: não é um total dividido')
    c.mark(4)
    c.click(SEL(f'{DLG} [data-contract-validation=finance] button', hasText='/', nth=0), at=c.A(4, 'Primeiro', 0.9), label='Primeiro vencimento (abre o calendário)')
    c.ev("'dump data vencimento: ' + [...document.querySelectorAll('[data-radix-popper-content-wrapper], [role=dialog]')].map(e => e.getAttribute('role') + ':' + e.innerText.replace(/\\s+/g, ' ').slice(0, 120) + '|btns=' + e.querySelectorAll('button').length).join(' ## ')", label='dump data de vencimento')
    c.click({'role': 'gridcell', 'name': '10', 'exact': True}, at=c.A(4, 'define', 0.9), label='escolhe o dia 10 (o calendário já abre em dezembro, a data de início)')
    c.hover(PD('Quantas parcelas'), 1.6, at=c.A(4, 'Quantas', 0.8), label='Quantas parcelas (já vem 12)')
    c.mark(5)
    c.click(SEL(f'{DLG} [data-contract-validation=finance] button[role=combobox]', hasText='Selecione a conta', nth=0), at=c.A(5, 'Conta', 0.9), label='Conta de recebimento')
    c.click(OPT('Conta Principal', exact=False), at=c.A(5, 'Principal,', 0.8), label='Conta Principal')
    c.click(SEL(f'{DLG} [data-contract-validation=finance] button[role=combobox]', hasText='Selecione a categoria', nth=0), at=c.A(5, 'Categoria,', 0.9), label='Categoria')
    c.click(OPT('Contratos PMOC', exact=False), at=c.A(5, 'Contratos', 0.8), label='Contratos PMOC')
    c.hover(PD('Duração da cobrança'), 2.4, at=c.A(5, 'Duração', 0.9), label='Duração da cobrança (Por um período)', optional=True)
    c.mark(6)
    c.hover(PD('Como vai ficar'), 4.0, at=c.A(6, 'Como', 0.9), label='Como vai ficar: 12 parcelas de R$ 1.200,00, R$ 14.400,00')
    c.confere('wiz', ['12 parcelas de R$ 1.200,00', 'R$ 14.400,00'], 'cap08: Como vai ficar fecha 12 x 1.200,00 = 14.400,00')
    c.click(PROXIMO, at=round(c.dur - 1.3, 2), label='Próximo (Revisão)')
    c.waitfor(text='Revisão final', timeout=10)
    rascunho_fim(c)
    c.fim()
    return c


def cap09():
    """Revisão e criação: Revisão final (blocos), Criar Contrato, avisos (12 OSs, 12 parcelas, documentos), detalhe do contrato."""
    # o rascunho não guarda quem executa e quem cobra (selectedUserIds/billingUserIds ficam fora do ContractDraft): o setup (sem filmar) refaz essas escolhas
    # na etapa Operação e cobrança e volta para a Revisão
    refaz_equipe = [
        {'do': 'click', 'target': SEL(f'{DLG} button', hasText='Operação e cobrança', nth=0)}, {'do': 'pause', 'seconds': 1.0},
        {'do': 'click', 'target': SEL(f'{DLG} [data-contract-validation=executors] button[role=combobox]', nth=0)},
        {'do': 'click', 'target': TXT('Rafael Lima', within=POP)}, {'do': 'click', 'target': TXT('Bruno Alves', within=POP)},
        {'do': 'press', 'key': 'Escape'}, {'do': 'pause', 'seconds': 0.5},
        {'do': 'click', 'target': SEL(f'{DLG} button[role=combobox]', nth=1)},
        {'do': 'click', 'target': TXT('Tatiane Ribeiro', within=POP)}, {'do': 'press', 'key': 'Escape'}, {'do': 'pause', 'seconds': 0.5},
        {'do': 'click', 'target': SEL(f'{DLG} button', hasText='Revisão', nth=0)}, {'do': 'pause', 'seconds': 1.0},
        {'do': 'waitFor', 'text': 'Revisão final', 'timeout': 10}]
    c = Cap(9, pace=0.5, start=(760, 420), prewarm=PREWARM + ['/contratos'], setup=setup_retomar(8) + refaz_equipe)
    c.mark(1)
    c.waitfor(text='Revisão final', timeout=10)
    for k, (palavra, bloco) in enumerate([('Dados', 'Identificação'), ('Escopo', 'Ambientes e equipamentos'), ('Operação', 'Equipe responsável')]):
        c.hover(PD(bloco), 0.5, at=c.A(1, palavra, 0.9), label=f'bloco {bloco} da Revisão')
    c.mark(2)
    c.ev(TOASTS_OBS, label='observador dos avisos')
    c.click(BTNX('Criar Contrato'), at=c.A(2, 'Criar', 0.9), label='Criar Contrato')
    c.mark(3)
    c.waitfor(text='Visão Geral', timeout=40)
    confere_aviso(c, 'OSs geradas', ['13 OSs geradas'], 'cap09: o aviso diz 13 OSs (a fala não cita o número)')
    confere_aviso(c, 'parcelas', ['12 parcelas lançadas'], 'cap09: 12 parcelas lançadas no Financeiro')
    c.mark(4)
    c.hover(SEL('main h1'), 2.0, at=c.A(4, 'Lembra:', 0.8), label='cabeçalho do contrato')
    c.fim()
    return c


# ---------------------------------------------------------------- o contrato do hotel (capítulos 10 a 13)
SETUP_CONTRATO = SETUP_LISTA + [
    {'do': 'click', 'target': LINHA('PMOC - Hotel Mirante do Mar')}, {'do': 'waitFor', 'text': 'Visão Geral', 'timeout': 25}, AGUARDA]


def abrir_contrato_hotel(c, at, label='abre o contrato PMOC - Hotel Mirante do Mar'):
    c.click(LINHA('PMOC - Hotel Mirante do Mar'), at=at, label=label)
    c.waitfor(text='Visão Geral', timeout=20)


def cap10():
    """O contrato por dentro: Filtros > Tipo PMOC; a linha do hotel (Saúde); o detalhe: abas, Visão Geral, Ocorrências, Ambientes e Equipamentos, Histórico PMOC, Financeiro."""
    c = Cap(10, pace=0.5, start=(760, 420), prewarm=PREWARM + ['/contratos'], setup=SETUP_LISTA)
    c.mark(1)
    c.click(BTNX('Filtros'), at=c.A(1, 'Filtros', 1.2), label='abre o painel Filtros')
    c.waitfor(text='Aplicar', timeout=8)
    c.click(SEL(f'{DLG} button, {DLG} label, {DLG} [role=checkbox]', hasText='PMOC', nth=0), at=c.A(1, 'PMOC:', 1.0), label='marca PMOC em Tipo')
    c.click(BTN('Aplicar'), at=c.A(1, 'sobra', 1.2), label='Aplicar', noScroll=True)
    c.hover(LINHA('PMOC - Hotel Mirante do Mar'), 1.4, at=c.A(1, 'contrato', 0.9, nth=1), label='sobra só o contrato do hotel')
    c.hover(SEL('main thead th', hasText='Saúde'), 2.6, at=c.A(1, 'Saúde', 0.9), label='coluna Saúde')
    c.mark(2)
    abrir_contrato_hotel(c, c.A(2, 'Abro', 0.9))
    c.hover(BTNX('Editar contrato'), 0.8, at=c.A(2, 'Editar', 0.9), label='botão Editar contrato (sem clicar)')
    c.hover(BTNX('Excluir contrato'), 0.8, at=c.A(2, 'Excluir', 0.9), label='botão Excluir contrato (sem clicar)')
    for k, aba in enumerate(['Visão Geral', 'Ocorrências', 'Ambientes e Equipamentos', 'Histórico PMOC', 'Financeiro', 'Documentos', 'Cronograma']):
        c.hover(TAB(aba), 0.1, at=round(c.A(2, 'abas.', 0.2) + k * 0.4, 2) if k == 0 else None, label=f'aba {aba}', optional=True)
    c.mark(3)
    c.hover(TXT('Informações', within='main'), 1.2, at=c.A(3, 'Informações', 0.9), label='cartão Informações')
    c.hover(TXT('Resumo', within='main'), 1.4, at=c.A(3, 'Resumo,', 0.9), label='cartão Resumo')
    c.hover(TXT('Portal do Contrato', within='main'), 1.4, at=c.A(3, 'Portal', 0.9), label='cartão Portal do Contrato (só passa)')
    c.hover(TXT('Progresso', within='main'), 1.6, at=c.A(3, 'Progresso', 0.9), label='cartão Progresso')
    c.confere('main', ['Total de ocorrências', '0 de 13 concluídas'], 'cap10: 13 ocorrências, 0 concluídas')
    c.mark(4)
    c.click(TAB('Ocorrências'), at=c.A(4, 'Ocorrências,', 0.9), label='aba Ocorrências')
    c.waitfor(text='Vincular OS existente', timeout=20)
    c.waitfor(selector="main tbody tr button:not([disabled])", timeout=20)
    c.hover(SEL('main thead th', hasText='Prevista', nth=0), 1.0, at=c.A(4, 'Prevista', 0.9), label='coluna Prevista')
    c.hover(SEL('main thead th', hasText='Agenda', nth=0), 1.0, at=c.A(4, 'Agenda', 0.9), label='coluna Agenda')
    c.hover(SEL('main tbody tr', nth=2), 1.4, at=c.A(4, 'Cada', 0.9), label='uma visita da lista (OS normal)')
    c.hover(SEL("main tbody tr button[title*='Pular'], main tbody tr button[aria-label*='Pular']", nth=1), 1.2, at=c.A(4, 'Pular', 0.9), label='botão Pular da visita (sem clicar)', optional=True)
    c.mark(5)
    c.click(SEL('main tbody tr button', hasText='Planejar visita', nth=0), at=c.A(5, 'Planejar', 0.9), label='Planejar visita (1ª visita)')
    c.waitfor(text='Planejar visita do contrato', timeout=15)
    c.click(SEL(f'{DLG} button', hasText='Próximo', nth=0), at=c.A(5, 'Abre', 0.5), label='Próximo (Escopo técnico)')
    c.waitfor(text='Escopo técnico', timeout=10)
    c.click(SEL(f'{DLG} button', hasText='Próximo', nth=0), at=c.A(5, 'ajustar', 1.2), label='Próximo (Equipe e agenda)')
    c.waitfor(text='Período do atendimento', timeout=10)
    c.hover(PD('Período do atendimento'), 0.4, at=c.A(5, 'datas', 0.9), label='Período do atendimento')
    c.hover(PD('Jornadas por dia'), 1.0, at=c.A(5, 'horários,', 1.2), label='Jornadas por dia')
    c.hover(PD('Adicionar outra data'), 1.0, at=c.A(5, 'seguidos,', 0.9), label='botão Adicionar outra data (sem clicar)')
    c.hover(SEL(f'{DLG} button', hasText='Adicionar dia', nth=0), 1.0, at=c.A(5, 'Adicionar', 0.9), label='botão Adicionar dia (sem clicar)')
    c.click(SEL(f'{DLG} button', hasText='Cancelar', nth=0), at=c.A(5, 'cancelo.', 0.9), label='Cancelar (nada grava)')
    c.mark(6)
    c.waitfor(selector="main button:not([disabled])", timeout=10)
    c.click(SEL('main button', hasText='Vincular OS existente', nth=0), at=c.A(6, 'Vincular', 0.9), label='Vincular OS existente')
    c.waitfor(text='Vincular OS existente ao contrato', timeout=15)
    c.click(SEL(f'{DLG} [role=radio], {DLG} button, {DLG} label', hasText='OS #10', nth=0), at=c.A(6, 'escolho', 0.9), label='marca a OS #10 do hotel')
    c.click(SEL(f'{DLG} button[role=combobox]', nth=0), at=c.A(6, 'visita', 0.9), label='abre Competência do contrato')
    c.click(OPT('01/12/2026', exact=False), at=c.A(6, 'vai', 0.9), label='escolhe a visita 01/12/2026')
    c.hover(SEL(f'{DLG} button', hasText='Vincular OS', nth=0), 1.2, at=c.A(6, 'substituída', 1.2), label='botão Vincular OS (sem clicar)')
    c.click(SEL(f'{DLG} button', hasText='Cancelar', nth=0), at=c.A(6, 'cancelo.', 0.9), label='Cancelar (nada grava)')
    c.mark(7)
    c.click(TAB('Ambientes e Equipamentos'), at=c.A(7, 'Ambientes', 0.9), label='aba Ambientes e Equipamentos')
    c.mark(8)
    c.click(TAB('Histórico PMOC'), at=c.A(8, 'Histórico', 0.9), label='aba Histórico PMOC')
    c.mark(9)
    c.click(TAB('Financeiro'), at=c.A(9, 'Financeiro,', 0.9), label='aba Financeiro')
    c.hover(SEL("main button[title='Marcar como pago']", nth=0), 2.2, at=c.A(9, 'Marcar', 0.9), label='botão Marcar como pago da parcela (sem clicar; o title nativo não aparece na gravação: aviso na edição)')
    c.confere('main', ['R$ 14.400,00', 'Pendente'], 'cap10: Previsto R$ 14.400,00 e parcelas Pendente')
    c.fim()
    return c


def cap11():
    """O cronograma do ano: aba Cronograma, Próximo período, etiquetas laranja, clique no dia, Dia/Semana/Mês, Imprimir PDF Anual (sem clicar)."""
    c = Cap(11, pace=0.5, start=(760, 420), prewarm=PREWARM + ['/contratos'], setup=SETUP_CONTRATO)
    c.mark(1)
    c.click(TAB('Cronograma'), at=c.A(1, 'Cronograma,', 0.9), label='aba Cronograma')
    c.click(BTN('Próximo período'), at=c.A(1, 'Avanço', 0.9), label='Próximo período (a primeira visita é em dezembro)')
    c.mark(2)
    c.hover(SEL("main [style*='--warning']", nth=0), 2.4, at=c.A(2, 'laranja', 0.9), label='etiqueta laranja (visita a fazer)', optional=True)
    c.mark(3)
    c.click(SEL("main [style*='--warning']", nth=0), at=c.A(3, 'Clicando', 0.9), label='clica no dia da visita', optional=True)
    c.click(TXT('Semana', within='main'), at=c.A(3, 'Semana', 0.9), label='Semana')
    c.click(TXT('Mês', within='main'), at=c.A(3, 'Mês.', 0.9), label='Mês')
    c.mark(4)
    c.hover(BTNX('Imprimir PDF Anual'), 3.4, at=c.A(4, 'Imprimir', 0.9), label='Imprimir PDF Anual (sem clicar)')
    c.fim()
    return c


def cap12():
    """Os documentos da norma: aba Documentos, Dossiê PMOC, Válido até, Gerar TRT individual, Histórico de versões, Planilha PMOC, Editar texto, Liberar documentos (sem clicar)."""
    c = Cap(12, pace=0.5, start=(760, 420), prewarm=PREWARM + ['/contratos'], setup=SETUP_CONTRATO)
    c.mark(1)
    c.click(TAB('Documentos'), at=c.A(1, 'aba', 0.9), label='aba Documentos')
    c.waitfor(text='Dossiê PMOC', timeout=15)
    c.hover(TXT('Documentos no portal do cliente', within='main'), 1.2, at=c.A(1, 'Pra', 0.8), label='cartão Documentos no portal do cliente')
    c.rolar(260, at=c.A(1, 'completar.', 1.2), label='desce pela aba', ponto=(760, 470), duration=0.7)
    c.mark(2)
    c.hover(P('Dossiê PMOC'), 2.2, at=c.A(2, 'Dossiê', 0.9), label='cartão Dossiê PMOC')
    c.hover(P('Assinado'), 1.6, at=c.A(2, 'Assinado', 0.9), label='selo Assinado', optional=True)
    c.mark(3)
    c.hover(P('Válido até'), 1.8, at=c.A(3, 'Válido', 0.9), label='Válido até do Termo e do Certificado', optional=True)
    c.click(BTN('Gerar TRT individual'), at=c.A(3, 'Gerar', 0.9), label='Gerar TRT individual')
    c.waitfor(text='TRT gerado!', timeout=15)
    c.confere('body', ['TRT gerado!'], 'cap12: o aviso diz TRT gerado!')
    c.mark(4)
    c.click(BTNX('Histórico de versões'), at=c.A(4, 'Histórico', 0.9), label='Histórico de versões', optional=True)
    c.confere('main', ['Histórico de versões (5)'], 'cap12: o histórico tem 5 versões (4 da criação + o TRT individual)')
    c.hover(P('Planilha PMOC'), 2.4, at=c.A(4, 'Planilha', 0.9), label='Planilha PMOC (sem clicar)')
    c.mark(5)
    c.hover(BTNX('Editar texto', nth=0), 0.5, at=c.A(5, 'Editar', 0.9), label='Editar texto (sem clicar)', optional=True)
    c.mark(6)
    c.rolar(-900, at=c.A(6, 'Liberar', 1.8), label='volta ao topo da aba', ponto=(760, 470), duration=0.7)
    c.hover(BTNX('Liberar documentos no portal do cliente'), 3.0, at=c.A(6, 'Liberar', 0.9), label='Liberar documentos no portal do cliente (sem clicar)')
    c.fim()
    return c


def cap13():
    """Renovar, pausar e excluir: menu da linha (Pausar), Renovar / Estender (+6 meses > Cancelar), Excluir contrato (a lista do que sai > Cancelar)."""
    c = Cap(13, pace=0.5, start=(760, 420), prewarm=PREWARM + ['/contratos'], setup=SETUP_LISTA)
    c.mark(1)
    c.hover(LINHA('PMOC - Hotel Mirante do Mar'), 0.6, at=c.A(1, 'dica:', 0.9), label='a linha do hotel')
    c.click(ACOES('PMOC - Hotel Mirante do Mar'), at=c.A(1, 'linha,', 1.9), label='menu da linha')
    c.pause(0.6)
    c.click(ACOES('PMOC - Hotel Mirante do Mar'), label='menu da linha de novo (só se não abriu)', unless=ITEM('Pausar'))
    c.hover(ITEM('Pausar'), 1.8, at=c.A(1, 'Pausar', 0.9), label='Pausar (sem clicar)')
    c.press('Escape', at=round(c.L(2) - 1.2, 2), label='fecha o menu')
    c.pause(0.5)
    c.mark(2)
    abrir_contrato_hotel(c, c.A(2, 'abro', 3.4))
    c.hover(BTNX('Renovar / Estender'), 0.8, at=c.A(2, 'Renovar', 1.0), label='botão Renovar / Estender')
    c.click(BTNX('Renovar / Estender'), at=c.A(2, 'Estender.', 0.9), label='abre Renovar / Estender')
    c.waitfor(text='Estender por', timeout=10)
    c.click(BTNX('+6 meses'), at=c.A(2, 'seis', 0.9), label='+6 meses', optional=True)
    c.click(BTNX('+12 meses'), at=c.A(2, 'doze', 0.9), label='+12 meses', optional=True)
    c.hover(PD('Horizonte atual'), 1.6, at=c.A(2, 'gera', 0.9), label='Horizonte atual e novo horizonte', optional=True)
    c.click(BTN('Cancelar'), at=c.A(2, 'Cancelar.', 0.9), label='Cancelar (fecha sem renovar)')
    c.mark(3)
    c.click(BTNX('Excluir contrato'), at=c.A(3, 'Excluir', 0.9, nth=1), label='abre Excluir contrato')
    c.waitfor(text='Serão excluídos junto com o contrato', timeout=10)
    ALERTA = '[role=alertdialog]'   # a janela Excluir contrato é um AlertDialog (não role=dialog)
    c.hover({'text': 'ordens de serviço vinculadas', 'within': ALERTA}, 2.4, at=c.A(3, 'ordens', 0.9), label='a lista do que sai junto')
    c.confere(ALERTA, ['13 ordens de serviço vinculadas', '4 itens do contrato'], 'cap13: a janela de excluir lista as 13 OSs e os 4 itens')
    c.hover({'text': 'Tenho certeza que desejo excluir', 'within': ALERTA}, 2.2, at=c.A(3, 'marcar', 0.9), label='caixa de confirmação (sem marcar)')
    c.click(BTN('Cancelar'), at=c.A(3, 'cancelo.', 0.9), label='Cancelar (fecha sem excluir)')
    c.fim()
    return c


def cap14():
    """Recapitulando: passeio sem alterar nada (lista com Filtros > Tipo, Configurações de Contrato > Responsáveis Técnicos, o contrato do hotel: Ocorrências, Documentos, Financeiro, Cronograma)."""
    c = Cap(14, pace=0.5, start=(760, 420), prewarm=PREWARM + ['/contratos'], setup=SETUP_LISTA)
    c.mark(1)
    c.hover(LINHA('PMOC - Hotel Mirante do Mar'), 1.2, at=0.3, label='a lista de Contratos (os dois contratos)')
    c.click(BTNX('Filtros'), at=c.A(1, 'tipo', 1.2), label='abre o painel Filtros')
    c.hover(PD('Tipo', exact=True), 0.8, at=c.A(1, 'tipo', 0.0) + 0.9, label='filtro Tipo (PMOC e Comum)')
    c.press('Escape', label='fecha o painel Filtros')
    c.click(BTN('Configurações de Contrato'), at=c.A(1, 'Configurações', 1.3), label='Configurações de Contrato')
    c.mark(2)
    c.click(TAB('Responsáveis Técnicos'), at=c.A(2, 'aparelho,', 0.6), label='aba Responsáveis Técnicos')
    c.hover(TXT('Ricardo Tavares Albuquerque', within='main'), 1.4, at=c.A(2, 'executor', 0.9), label='o Ricardo cadastrado')
    c.click(BTN('Voltar'), at=c.A(2, 'PMOC', 1.0), label='Voltar para a lista de Contratos')
    c.hover(BTN('Novo Contrato'), 1.2, at=c.A(2, 'ambientes', 0.9), label='Novo Contrato (Unidade e RT, ambientes)')
    c.mark(3)
    c.click(LINHA('PMOC - Hotel Mirante do Mar'), at=c.A(3, 'criar,', 0.9), label='abre o contrato do hotel')
    c.waitfor(text='Visão Geral', timeout=20)
    c.click(TAB('Ocorrências'), at=c.A(3, 'agenda', 1.0), label='aba Ocorrências (as visitas na agenda)')
    c.click(TAB('Documentos'), at=c.A(3, 'documentos', 0.9), label='aba Documentos')
    c.hover(P('Dossiê PMOC'), 0.5, at=c.A(3, 'Dossiê.', 0.9), label='Dossiê PMOC (Termo, Certificado, Cronograma)')
    c.mark(4)
    c.click(TAB('Financeiro'), at=c.A(4, 'financeiro,', 1.5), label='aba Financeiro')
    c.click(TAB('Cronograma'), at=c.A(4, 'cronograma', 1.3), label='aba Cronograma')
    c.mark(5)
    c.click(TAB('Visão Geral'), at=c.A(4, 'versões', 0.9), label='aba Visão Geral')
    c.hover(BTNX('Renovar / Estender'), 1.6, at=c.A(4, 'renovar.', 1.0), label='Renovar / Estender (sem clicar)')
    c.fim()
    return c


CAPS = {0: cap00, 1: cap01, 2: cap02, 3: cap03, 4: cap04, 5: cap05, 6: cap06, 7: cap07, 8: cap08, 9: cap09, 10: cap10, 11: cap11, 12: cap12, 13: cap13, 14: cap14}

if __name__ == '__main__':
    quais = [int(a) for a in sys.argv[1:]] or sorted(CAPS)
    for n in quais:
        cap = CAPS[n]()
        if os.environ.get('ANCHORS'):
            for i, w, t in cap.anchors:
                print(f'   anchor L{i} "{w}" -> {t}')
        d = cap.out()
        last = -1
        for st in d['steps']:
            if 'at' in st:
                if st['at'] < last:
                    print(f'  aviso cap{n:02d}: at {st["at"]} < {last} em "{st.get("label") or st.get("name")}"')
                last = max(last, st['at'])
        path = os.path.join(HERE, f'cap{n:02d}.json')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
        print(f'cap{n:02d}: {len(d["steps"])} passos, narração {cap.dur:.1f} s -> {os.path.relpath(path, HERE)}')
