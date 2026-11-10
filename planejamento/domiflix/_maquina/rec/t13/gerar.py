#!/usr/bin/env python3
"""T13 · gera rec/t13/cap00..cap14.json (roteiros do robô) a partir da voz pronta (t13/narracao/capNN.json).

Aula inteira no COMPUTADOR (janela 1280x800), logada como Camila Duarte (admin, Glacial Cold Brasil), na Dominex 1.38.19, FAKE_NOW 10/11/2026 10:00.
Os `at` saem da palavra que anuncia cada passo (A(linha, palavra, folga)): o gesto "pousa" ~0,7 a 1 s depois do início do passo
(clique = deslocamento + ~0,85 s; digitação = clique + texto), então `at` = início da palavra - folga.
Rodar de qualquer pasta: `python3 -I rec/t13/gerar.py [NN ...]`. Depois: `node rec/record.mjs rec/t13/capNN.json --check`.

Cadeia de sementes: rec/t13/cadeia.json (semear.py: fim do T12 + `t13/inicio`) e, a cada capítulo, o último `t13/apos-capNN` do capítulo anterior
que mexeu no banco (SEMENTE abaixo). O `apos-capNN` sai da gravação (`rec/t13/snap.mjs diff NN`, na mesma trava).

Particularidades (lições deste tutorial, ver docs/08-licoes.md):
 - Menu lateral RECOLHIDO (`Toggle Sidebar`) no `setup` de todo capítulo de tela cheia (a 1280 px o botão "Nova movimentação" sai do quadro com o menu aberto).
 - 1.38.19: "Conciliação bancária (OFX)" no cabeçalho; "Nova conta"/"Novo cartão" são o "+" do título de cada grupo; "Nova compra" no Estoque é um menu.
 - Observador `OBS` guarda em `window.__avisos` todo aviso de erro do app, tela escura e faixa da trilha Domiflix; o passo final devolve a lista (tem de sair vazia).
"""
import json
import os
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TUT = os.path.normpath(os.path.join(HERE, '..', '..'))
NARR = os.path.join(TUT, 't13', 'narracao')
CAD = json.load(open(os.path.join(HERE, 'cadeia.json'), encoding='utf8'))
BASE = CAD['inicio']
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

NOMES = ['Abertura', 'Onde fica cada coisa', 'O caixa e o banco', 'Entrou dinheiro', 'Saiu dinheiro', 'A compra direta', 'De uma conta pra outra',
         'O cartão da empresa', 'Compra parcelada', 'Pagar a fatura', 'O que vai vencer', 'Pagar e receber', 'Organizar as categorias',
         'A visão geral do mês', 'Recapitulando']
# estado de partida de cada capítulo: o último apos-capNN (de capítulo anterior) que mexeu no banco
SEMENTE = {0: None, 1: None, 2: None, 3: 'apos-cap02', 4: 'apos-cap03', 5: 'apos-cap04', 6: 'apos-cap05', 7: 'apos-cap06', 8: 'apos-cap07',
           9: 'apos-cap08', 10: 'apos-cap09', 11: 'apos-cap10', 12: 'apos-cap11', 13: 'apos-cap12', 14: 'apos-cap12'}


# pausas de voz inseridas na fase 2 (capítulo, linha 1-based) -> segundos de silêncio antes da linha; o gesto sai (pausa - 0,2 s) mais cedo
PAUSAS = {0: {2: 1.6}, 3: {3: 2.1}, 4: {3: 1.4, 4: 1.0}, 5: {2: 2.3}, 6: {2: 2.4}, 7: {2: 0.9, 4: 2.0}, 8: {3: 0.9}, 10: {6: 2.5, 8: 6.0}, 11: {2: 1.4, 3: 2.1, 6: 0.4}}
LEAD = {(n, i): max(0.0, min(d - 0.2, 2.5)) for n, ls in PAUSAS.items() for i, d in ls.items()}


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
        s.prewarm = prewarm or ['/dashboard', '/financeiro/movimentacoes']
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
        # linha que ganhou pausa de voz (pausas.py) antes dela: os gestos dela começam dentro do silêncio (fase 2: o encadeamento de selects/digitação da linha
        # é mais lento que a fala; a pausa sozinha só desloca tudo por igual)
        t = round(max(0.0, s.W(i, palavra, nth) - folga - LEAD.get((s.n, i), 0.0)), 2)
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
        seconds = min(seconds, 0.9)   # o robô é sequencial: hover longo atrasa as marcas das linhas seguintes (lateBy de 1 a 2,5 s nos primeiros takes); a câmera/destaque seguram o quadro na edição
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
        if len(text) > 10 and not kw.get('noClick') and not kw.get('clear'):
            # texto longo: clique no campo e "colar" (execCommand insertText, ~0,05 s): digitar 50 letras levava 3,8 s e atrasava os gestos seguintes da linha
            s._p({'do': 'click', 'target': target}, at, (label + ' (clique)') if label else None, {})
            return s.colar(text, None, (label + ' (colado)') if label else None)
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

    def confere_campos(s, esperados, label, escopo='[role=dialog]'):
        """lê o VALOR dos campos (input/textarea) do escopo e compara com o que a fala diz (`confere` só lê texto, não o valor digitado)"""
        esp = [esperados] if isinstance(esperados, str) else list(esperados)
        js = ("(async()=>{const esp=%s;let out='';for(let i=0;i<12;i++){const v=[...document.querySelectorAll(%s+' input, '+%s+' textarea')].map(e=>e.value).join(' | ');"
              "const falta=esp.filter(e=>!v.includes(e));if(!falta.length)return 'OK: '+esp.join(' | ');out='DIFERENTE: faltou '+JSON.stringify(falta)+' em: '+v.slice(0,260);"
              "await new Promise(r=>setTimeout(r,300));}return out})()") % (json.dumps(esp, ensure_ascii=False), json.dumps(escopo), json.dumps(escopo))
        return s.add({'do': 'eval', 'js': js, 'label': 'confere ' + label})

    def confere_campos_texto(s, escopo, esperados, label):
        return s.confere(escopo, esperados, label)

    def confere_ausente(s, escopo, texto, label):
        """como `confere`, mas o texto NÃO pode aparecer (espera ~2 s para a tela terminar de atualizar)"""
        sel = {'dlg': '[role=dialog]', 'main': 'main', 'body': 'body'}.get(escopo, escopo)
        js = ("(async()=>{await new Promise(r=>setTimeout(r,900));const el=document.querySelector(%s);const t=(el?el.innerText:'').replace(/[\\s\\u00a0]+/g,' ').toLowerCase();"
              "return t.includes(%s)?'DIFERENTE: apareceu '+%s:'OK: ausente '+%s})()") % (json.dumps(sel), json.dumps(texto.lower()), json.dumps(texto), json.dumps(texto))
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
            'name': f't13-cap{s.n:02d}',
            'title': f'T13 · Cap. {s.n} · {NOMES[s.n]} (narração {str(round(s.dur, 1)).replace(".", ",")} s; marcas L1..L{len(s.linhas)} = início de cada linha do roteiro)',
            'seed': f't13-cap{s.n:02d}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
            'start': {'x': s.start[0], 'y': s.start[1]},
            'seedExtra': list(BASE) + ([f't13/{sem}'] if sem else []),
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
ACOES = lambda cliente: {'selector': f"main tbody tr:has-text('{cliente}') button[aria-label='Ações']"}   # "⋮" da linha
AGUARDA = {'do': 'waitFor', 'idle': True}
SW = lambda n, **kw: {'role': 'switch', 'name': n, 'exact': True, **kw}
DI = lambda ph, k=0: {'selector': f"{DLG} input[placeholder='{ph}']", 'nth': k}   # campo da janela pelo placeholder
COMBO = lambda txt, esc=DLG: {'selector': f'{esc} button[role=combobox]', 'hasText': txt}   # seletor da janela pelo texto que ele mostra (placeholder ou valor)
ACOES_CONTA = lambda nome: {'role': 'button', 'name': f'Ações de {nome}', 'exact': True}   # "⋮" de uma conta na coluna Contas e cartões
CONTA = lambda nome: {'selector': 'aside[aria-label="Contas e cartões"] button', 'hasText': nome}   # linha de uma conta/cartão na coluna
BTN_MAIS = lambda nome: {'role': 'button', 'name': nome, 'exact': True}
ROLA_DLG = "(()=>{const d=document.querySelector('[role=dialog] .overflow-y-auto');if(!d)return 'sem rolagem';d.scrollTo({top:%s,behavior:'smooth'});return d.scrollHeight})()"

# ---------------------------------------------------------------- trechos comuns (não filmados, no `setup`)
SETUP_DASH = [{'do': 'goto', 'url': '/dashboard'}, {'do': 'waitFor', 'text': 'Olá, Camila!', 'timeout': 25}, AGUARDA]
MENU_LATERAL = {'role': 'button', 'name': 'Toggle Sidebar', 'nth': 0}
# Plano B do Esc: clicar o "Fechar" da janela por `eval` (instantâneo). Um `click` condicional no botão Fechar pode travar 30 s.
FECHAR_EVAL = r"""(() => { const d = document.querySelector('[role=dialog]'); if (!d) return 'ja fechada'; const b = [...d.querySelectorAll('button')].find((x) => [x.textContent, x.getAttribute('aria-label'), x.title].some((v) => /^\s*fechar\s*$/i.test(v || ''))); if (!b) return 'sem botao Fechar'; b.click(); return 'fechada pelo botao'; })()"""


def fechar_janela(c, at, espera=0.4):
    """Esc fecha a janela; se o Esc não bastar, o botão Fechar por `eval`. Termina com a janela fechada."""
    c.press('Escape', at=at, label='fecha a janela')
    c.add({'do': 'wait', 'seconds': espera})
    c.ev(FECHAR_EVAL, label='Fechar (se o Esc não fechou)')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)




SETUP_MOV = SETUP_DASH + [{'do': 'goto', 'url': '/financeiro/movimentacoes'}, {'do': 'waitFor', 'text': 'Contas e cartões', 'timeout': 25}, AGUARDA,
                          {'do': 'click', 'target': MENU_LATERAL}, {'do': 'pause', 'seconds': 0.8}]
CLICA_CONTA = lambda nome: [{'do': 'click', 'target': CONTA(nome)}, AGUARDA, {'do': 'pause', 'seconds': 0.6}]
NOVA_MOV = {'role': 'button', 'name': 'Nova movimentação', 'exact': True, 'nth': 0}   # a do alto do extrato (a 2ª é a do estado vazio)
SALVAR = BTN('Salvar', within=DLG)


def escolhe(c, combo_txt, opcao, at, label, **kw):
    """abre o seletor da janela (pelo texto que ele mostra) e escolhe a opção"""
    return c.select(COMBO(combo_txt), opcao, at=at, label=label, **kw)


# ================================================================ capítulos
def cap00():
    """Abertura: Dashboard, abre o grupo Financeiro e a Visão Geral; a câmera desce pelos blocos."""
    c = Cap(0, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/financeiro/relatorio'], setup=SETUP_DASH)
    c.mark(1)
    c.hover(LINK('Agenda'), 0.1, at=0.3, label='o cursor passa pelo menu lateral')
    c.click(BTN('Financeiro'), at=3.4, label='abre o grupo Financeiro do menu')
    c.click(LINK('Visão Geral'), at=c.A(1, 'sai', 0.9), label='abre a Visão Geral')
    c.waitfor(text='Saldo do Período', timeout=20)
    c.hover(P('Saldo do Período'), 0.5, at=c.A(1, 'lugar', 0.9), label='cartão escuro Saldo do Período')
    c.mark(2)
    c.rolar(260, at=round(c.L(2) + 0.2, 2), label='a câmera desce devagar pelos blocos', duration=2.4)
    c.rolar(260, at=round(c.L(2) + 3.3, 2), label='continua descendo', duration=2.4)
    c.mark(3)
    c.rolar(-560, at=c.A(3, 'Vamos', 1.5), label='sobe de volta ao topo', duration=1.2)
    c.fim()
    return c


def cap01():
    """Onde fica cada coisa: o grupo Financeiro e as cinco telas, o filtro de período e Configurações Financeiras."""
    c = Cap(1, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/financeiro/relatorio'],
            setup=SETUP_DASH + [{'do': 'goto', 'url': '/financeiro/relatorio'}, {'do': 'waitFor', 'text': 'Saldo do Período', 'timeout': 25}, AGUARDA,
                                {'do': 'click', 'target': BTN('Financeiro')}, {'do': 'waitFor', 'target': LINK('Relatórios'), 'timeout': 15}])
    c.mark(1)
    c.hover(BTN('Financeiro'), 0.6, at=c.A(1, 'Financeiro', 0.7), label='o grupo Financeiro do menu')
    c.hover(LINK('Relatórios'), 0.4, at=c.A(1, 'cinco', 0.6), label='as cinco telas do grupo')
    c.mark(2)
    c.hover(LINK('Visão Geral'), 0.5, at=c.A(2, 'Visão', 0.8), label='Visão Geral')
    c.hover(LINK('Movimentações Financeiras'), 0.5, at=c.A(2, 'Movimentações', 0.8), label='Movimentações Financeiras')
    c.hover(LINK('Contas a Pagar/Receber'), 0.5, at=c.A(2, 'Contas', 0.8), label='Contas a Pagar/Receber')
    c.mark(3)
    c.hover(LINK('Cobranças'), 0.5, at=c.A(3, 'Cobranças', 0.8), label='Cobranças')
    c.hover(LINK('Relatórios'), 0.5, at=c.A(3, 'Relatórios', 0.8), label='Relatórios')
    c.mark(4)
    c.hover(BTN('Este mês'), 0.8, at=c.A(4, 'filtro', 0.9), label='filtro de período em Este mês')
    c.hover(BTN('Configurações Financeiras'), 0.8, at=c.A(4, 'Configurações', 0.9), label='botão Configurações Financeiras')
    c.mark(5)
    c.click(BTN('Este mês'), at=c.A(5, 'período', 0.9), label='abre o filtro de período')
    c.waitfor(text='Últimos 7 dias', timeout=8)
    c.hover(P('Personalizado', within=POP), 1.2, at=c.A(5, 'vale', 0.4), label='as opções do período', optional=True)
    c.press('Escape', at=c.A(5, 'escolhido.', 0.2), label='fecha sem trocar')
    c.fim()
    return c


def cap02():
    """O caixa e o banco: Movimentações Financeiras, Conciliação (só zoom), saldo inicial da Conta Principal e do Caixa."""
    c = Cap(2, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/financeiro/movimentacoes'],
            setup=SETUP_DASH + [{'do': 'goto', 'url': '/financeiro/relatorio'}, {'do': 'waitFor', 'text': 'Saldo do Período', 'timeout': 25}, AGUARDA,
                                {'do': 'click', 'target': BTN('Financeiro')}, {'do': 'waitFor', 'target': LINK('Movimentações Financeiras'), 'timeout': 15}])
    c.mark(1)
    c.click(LINK('Movimentações Financeiras'), at=0.6, label='abre Movimentações Financeiras')
    c.waitfor(text='Contas e cartões', timeout=20)
    c.click(MENU_LATERAL, at=c.A(1, 'sabe', 0.7), label='recolhe o menu lateral (a tela ganha espaço)')
    c.pause(0.8)
    c.hover(SEL('aside[aria-label="Contas e cartões"] h2, aside[aria-label="Contas e cartões"] p', nth=0), 1.4, at=c.A(1, 'coluna,', 1.0), label='coluna Contas e cartões')
    c.mark(2)
    c.hover(CONTA('Caixa'), 0.8, at=c.A(2, 'Caixa,', 0.9), label='linha Caixa')
    c.hover(CONTA('Conta Principal'), 0.8, at=c.A(2, 'Principal,', 0.9), label='linha Conta Principal')
    c.hover(BTN('Conciliação bancária (OFX)'), 1.6, at=c.A(2, 'Conciliação', 0.9), label='botão Conciliação bancária (OFX), sem clicar')
    c.mark(3)
    c.click(ACOES_CONTA('Conta Principal'), at=c.A(3, 'menu', 1.0), label='menu ⋮ da Conta Principal')
    c.click(ITEM('Editar'), at=c.A(3, 'Editar', 0.9), label='Editar')
    c.waitfor(text='Editar Conta', timeout=10)
    c.hover(P('Instituição', within=DLG), 0.6, at=c.A(3, 'Saldo', 1.4, nth=2), label='passa por Tipo e Instituição (sem abrir)')
    c.type(DI('0,00'), '1850000', at=c.A(3, 'dezoito', 1.0), cps=20, label='Saldo Inicial 18.500,00')
    c.confere_campos('18.500,00', 'Saldo Inicial 18.500,00')
    c.hover(P('Editar o saldo inicial recalcula', within=DLG), 0.3, label='aviso: Editar o saldo inicial recalcula o saldo atual')
    c.mark(4)
    c.hover(SW('Faz parte do caixa da empresa'), 1.0, at=c.A(4, 'Repara', 0.8), label='interruptor Faz parte do caixa da empresa (ligado)')
    c.hover(P('Ligado, o dinheiro desta conta', within=DLG), 2.0, at=c.A(4, 'Ligado,', 0.9), label='explicação do interruptor')
    c.click(SALVAR, at=c.A(4, 'Já', 0.9), label='Salvar')
    c.waitfor(gone={'role': 'dialog'}, timeout=10)
    c.confere('main', 'Saldo R$ 18.500,00', 'Conta Principal com Saldo R$ 18.500,00')
    c.hover(BTN_MAIS('Nova conta bancária'), 2.0, at=c.A(4, 'Nova', 0.9, nth=0), label='o + do grupo Contas (rótulo Nova conta), sem clicar')
    c.mark(5)
    c.click(ACOES_CONTA('Caixa'), at=c.A(5, 'No', 0.5), label='menu ⋮ do Caixa')
    c.click(ITEM('Editar'), label='Editar')
    c.waitfor(text='Editar Conta', timeout=10)
    c.type(DI('0,00'), '80000', cps=20, label='Saldo Inicial 800,00')
    c.confere_campos('800,00', 'Saldo Inicial 800,00')
    c.click(SALVAR, label='Salvar')
    c.waitfor(gone={'role': 'dialog'}, timeout=10)
    c.confere('main', ['Saldo R$ 800,00', 'Saldo R$ 18.500,00'], 'Caixa 800,00 e Conta Principal 18.500,00')
    c.hover(CONTA('Caixa'), 1.2, at=c.A(5, 'Pronto,', 0.5), label='as duas contas mostram o saldo')
    c.fim()
    return c


def cap03():
    """Entrou dinheiro: Conta Principal, Nova movimentação > Receita, formulário completo, Salvar, extrato."""
    c = Cap(3, pace=0.5, start=(760, 420), setup=SETUP_MOV)
    c.mark(1)
    c.click(CONTA('Conta Principal'), at=c.A(1, 'Abro', 0.9), label='abre a Conta Principal')
    c.confere('main', ['Conta Principal', 'R$ 18.500,00'], 'cabeçalho da conta com o saldo')
    c.hover(P('Conta Principal', nth=1), 1.0, at=c.A(1, 'saldo,', 0.9), label='em cima o saldo', optional=True)
    c.mark(2)
    c.click(NOVA_MOV, at=c.A(2, 'Clico', 0.9), label='Nova movimentação')
    c.waitfor(text='Escolha como o dinheiro se movimenta.', timeout=10)
    c.hover(BTN_MAIS('Despesa Dinheiro que sai da empresa.'), 0.4, at=c.A(2, 'Despesa', 0.8), label='opção Despesa', optional=True)
    c.click({'selector': f'{DLG} button', 'hasText': 'Dinheiro que entra na empresa.'}, at=c.A(2, 'Receita.', 0.9, nth=1), label='Receita')
    c.waitfor(text='Registre uma receita ou despesa', timeout=10)
    c.mark(3)
    escolhe(c, 'Selecione uma categoria', 'Vendas de Serviços', c.A(3, 'Categoria', 0.9), 'categoria Vendas de Serviços')
    c.type({'placeholder': 'Descreva a movimentação', 'within': DLG}, 'Instalação de split 12.000 BTUs - Mercado Vila Nova', at=c.A(3, 'Descrição', 0.9), cps=45, label='descrição')
    escolhe(c, 'Selecione um cliente', 'Mercado Vila Nova', c.A(3, 'Cliente', 0.9), 'cliente Mercado Vila Nova')
    c.mark(4)
    c.hover(COMBO('Sem ordem de serviço'), 1.8, at=c.A(4, 'Ordem', 0.9), label='campo Ordem de serviço, sem escolher')
    c.mark(5)
    c.type(DI('0,00'), '185000', at=c.A(5, 'valor,', 1.2), cps=20, label='Valor 1.850,00')
    c.confere_campos('1.850,00', 'Valor 1.850,00')
    escolhe(c, 'Selecione uma conta', 'Conta Principal', c.A(5, 'conta', 0.9, nth=0), 'conta Conta Principal')
    escolhe(c, 'Selecione a forma de pagamento', 'PIX', c.A(5, 'PIX.', 1.0), 'forma de pagamento PIX')
    c.mark(6)
    c.hover(P('Quando isso aconteceu', within=DLG), 1.8, at=c.A(6, 'lançamento', 1.0), label='Data do lançamento e a dica')
    c.hover(P('Será registrado como recebido', within=DLG), 1.0, at=c.A(6, 'recebido', 0.9), label='Já foi recebido ligado')
    c.hover(P('Quando o dinheiro realmente saiu', within=DLG), 2.0, at=c.A(6, 'recebimento', 0.9), label='Data do recebimento e a dica')
    c.mark(7)
    c.click(SALVAR, at=c.A(7, 'Salvo,', 0.9), label='Salvar')
    c.waitfor(gone={'role': 'dialog'}, timeout=12)
    c.confere('main', ['Instalação de split 12.000 BTUs - Mercado Vila Nova', '1.850,00'], 'a receita no extrato')
    c.hover(P('Saldo: R$'), 2.5, at=c.A(7, 'Saldo', 0.9), label='o Saldo sob o Valor (na janela de 1280 px a coluna Saldo Após não aparece: só a partir de 1440 px)')
    c.fim()
    return c


def cap04():
    """Saiu dinheiro: Despesa com vencimento (Já foi pago desligado), Mais detalhes, Salvar; fica em Contas a Pagar."""
    c = Cap(4, pace=0.5, start=(760, 420), setup=SETUP_MOV + CLICA_CONTA('Conta Principal'))
    c.mark(1)
    c.click(NOVA_MOV, at=c.A(1, 'Nova', 0.9, nth=0), label='Nova movimentação')
    c.waitfor(text='Escolha como o dinheiro se movimenta.', timeout=10)
    c.click({'selector': f'{DLG} button', 'hasText': 'Dinheiro que sai da empresa.'}, at=c.A(1, 'Despesa.', 0.9), label='Despesa')
    c.waitfor(text='Registre uma receita ou despesa', timeout=10)
    c.mark(2)
    escolhe(c, 'Selecione uma categoria', 'CSP - Materiais', c.A(2, 'Categoria', 0.9), 'categoria CSP - Materiais')
    c.type({'placeholder': 'Descreva a movimentação', 'within': DLG}, 'Gás R-410A e tubos de cobre', at=c.A(2, 'material', 0.9), cps=45, label='descrição')
    escolhe(c, 'Selecione um fornecedor', 'Ventura Gás e Tubos', c.A(2, 'Fornecedor', 0.9, nth=0), 'fornecedor Ventura Gás e Tubos')
    c.mark(3)
    c.type(DI('0,00'), '64000', at=c.A(3, 'Seiscentos', 0.9), cps=20, label='Valor 640,00')
    c.confere_campos('640,00', 'Valor 640,00')
    escolhe(c, 'Selecione uma conta', 'Conta Principal', c.A(3, 'Conta', 0.9), 'conta Conta Principal')
    escolhe(c, 'Selecione a forma de pagamento', 'Boleto', c.A(3, 'boleto.', 1.0), 'forma de pagamento Boleto')
    c.mark(4)
    c.click(SW('Já foi pago', within=DLG), at=c.A(4, 'desligo', 0.9), label='desliga o Já foi pago')
    c.waitfor(text='Irá para contas a pagar', timeout=8)
    c.hover(P('Irá para contas a pagar', within=DLG), 1.2, at=c.A(4, 'aviso:', 0.9), label='aviso: irá para contas a pagar')
    c.click(SEL(f'{DLG} button[aria-haspopup]', hasText='Selecione a data'), at=c.A(4, 'Vencimento,', 0.9), label='abre o calendário do Vencimento')
    c.click(SEL(f'{POP} button:text-is("20")'), at=c.A(4, 'boleto', 0.9, nth=1), label='escolhe o dia 20 (20/11/2026)')
    c.confere('dlg', '20/11/2026', 'Vencimento 20/11/2026')
    c.mark(5)
    c.click(BTN_MAIS('Mais detalhes'), at=c.A(5, 'Mais', 0.9), label='abre Mais detalhes')
    c.ev(ROLA_DLG % '600', at=c.A(5, 'guardar', 0.8), label='rola a janela até Comprovantes')
    c.hover(P('Aceita imagens (JPG, PNG) e PDFs', within=DLG), 2.0, at=c.A(5, 'Comprovantes', 0.9), label='Comprovantes / Notas Fiscais: Anexar comprovantes, sem anexar')
    c.mark(6)
    c.click(SALVAR, at=c.A(6, 'Salvo.', 0.9), label='Salvar')
    c.waitfor(gone={'role': 'dialog'}, timeout=12)
    c.confere_ausente('main', 'Gás R-410A e tubos de cobre', 'a despesa a pagar NÃO entra no extrato da Conta Principal')
    c.hover(SEL('main', hasText='Instalação de split'), 2.5, at=c.A(6, 'extrato,', 0.9), label='o extrato continua só com a receita', optional=True)
    c.fim()
    return c


SETUP_ESTOQUE = SETUP_DASH + [{'do': 'goto', 'url': '/estoque'}, {'do': 'waitFor', 'text': 'Controle de peças e materiais', 'timeout': 25}, AGUARDA,
                              {'do': 'click', 'target': MENU_LATERAL}, {'do': 'pause', 'seconds': 0.8}]
CAMPO = lambda label, tag='button[role=combobox]', nth=0: {'selector': f"{DLG} div:has(> label:has-text('{label}')) {tag}", 'nth': nth}   # campo da janela pelo rótulo dele
FIM_SETUP_CONTA = lambda nome: [{'do': 'click', 'target': CONTA(nome)}, AGUARDA, {'do': 'pause', 'seconds': 0.6}]


def escolhe_tecla(c, combo, teclas, at, label):
    """Select do Radix com lista longa (Dia 1..31, parcelas): o ponteiro passa pelas setas de rolagem da lista e a lista anda sob o clique (virou "Dia 6" e "4x").
    Abre com o clique e escolhe pelo teclado (digitar o começo do texto da opção e Enter), sem deixar a seleção ao acaso."""
    c.click(combo, at=at, label=f'abre a lista ({label})')
    c.pause(0.5)
    c.press(teclas, label=f'{label} (pelo teclado)')


def data_do_dia(c, gatilho_txt, dia, meses_atras, at, label):
    """abre o calendário do campo de data (botão que mostra `gatilho_txt`), volta `meses_atras` meses e escolhe o `dia`"""
    c.click(SEL(f'{DLG} button[aria-haspopup]', hasText=gatilho_txt), at=at, label=f'abre o calendário ({label})')
    for k in range(meses_atras):
        c.click({'role': 'button', 'name': 'Go to previous month'}, label=f'mês anterior ({label})')
    c.click(SEL(f'{POP} button:text-is("{dia}")'), label=f'escolhe o dia {dia} ({label})')


def cap05():
    """A compra direta: Estoque > Compras de Material > Nova compra > Registrar compra direta; a compra dá entrada no estoque e lança a despesa."""
    c = Cap(5, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/estoque'], setup=SETUP_ESTOQUE)
    c.mark(1)
    c.click(TAB('Compras de Material'), at=c.A(1, 'Compras', 0.9), label='aba Compras de Material')
    c.waitfor(text='Nova compra', timeout=15)
    c.click(BTN('Nova compra', within='main'), at=c.A(1, 'Material', 0.5, nth=1), label='abre o menu Nova compra (1.38.19: o botão virou menu)')
    c.hover(ITEM('Registrar compra direta'), 1.2, label='item Registrar compra direta')
    c.mark(2)
    c.click(ITEM('Registrar compra direta'), at=c.A(2, 'Registrar', 0.9), label='Registrar compra direta')
    c.waitfor(text='Registre a entrada no estoque e a despesa financeira em uma única operação.', timeout=10)
    c.type({'placeholder': 'Ex.: Reposição de cobre', 'within': DLG}, 'Reposição de dreno', at=c.A(2, 'Escrevo', 0.9), cps=16, label='descrição: Reposição de dreno')
    c.select(COMBO('Selecione o fornecedor'), 'Distribuidora Aurora de Peças Ltda', at=c.A(2, 'Distribuidora', 1.0), label='fornecedor: Distribuidora Aurora')
    c.confere('dlg', ['Estoque Principal'], 'o local de estoque já vem em Estoque Principal')
    c.hover(CAMPO('Local de estoque'), 1.2, at=c.A(2, 'Estoque', 0.9, nth=1), label='Local de estoque: Estoque Principal')
    c.mark(3)
    c.click(CAMPO('Material 1'), at=c.A(3, 'mangueira', 1.4), label='abre o campo Material 1')
    c.waitfor(target=OPT('Mangueira de dreno'), timeout=8)
    c.pause(0.4)
    c.click(OPT('Mangueira de dreno'), label='Material 1: Mangueira de dreno')
    c.ev("(()=>{const b=document.querySelector('[role=dialog] button[role=combobox]:not([aria-expanded=true])');return [...document.querySelectorAll('[role=dialog] button[role=combobox]')].map(x=>x.innerText.trim().slice(0,40)).join(' | ')})()", label='confere campos de seleção depois de escolher o material')
    c.type(DI('0'), '30', at=c.A(3, 'trinta', 1.0), label='Quantidade 30')
    c.type(DI('0,00'), '3,50', at=c.A(3, 'três', 1.0), label='Preço unitário 3,50')
    c.confere('dlg', ['Subtotal: R$ 105,00', 'Total da compra'], 'Subtotal e Total da compra R$ 105,00')
    c.hover(P('Total da compra', within=DLG), 1.4, at=c.A(3, 'total', 0.9), label='Total da compra R$ 105,00')
    c.mark(4)
    c.ev(ROLA_DLG % '2000', at=c.A(4, 'Embaixo', 0.8), label='rola a janela até o lado do Financeiro')
    c.confere('dlg', ['CSP - Materiais'], 'a categoria financeira já vem em CSP - Materiais')
    c.hover(CAMPO('Categoria financeira'), 1.0, at=c.A(4, 'categoria', 0.9), label='Categoria financeira CSP - Materiais')
    c.select(COMBO('Caixa'), 'Conta Principal', at=c.A(4, 'Escolho', 0.9), label='Conta financeira: Conta Principal (a lista abre em Caixa)')
    c.hover(P('Situação do pagamento', within=DLG), 0.8, at=c.A(4, 'Pago,', 0.9), label='Situação do pagamento: Pago')
    c.select(COMBO('Selecione a forma de pagamento'), 'PIX', at=c.A(4, 'PIX,', 0.9), label='forma de pagamento: PIX')
    c.mark(5)
    c.pause(0.5)   # o seletor/calendário anterior ainda está fechando: sem a pausa o clique de envio pode ser engolido
    c.click(BTN('Registrar compra', within=DLG), at=c.A(5, 'Registrar', 0.9), label='Registrar compra')
    c.pause(1.5)
    c.ev("(()=>{const d=document.querySelector('[role=dialog]');return (d?'DIALOGO ABERTO: '+d.innerText.slice(-500)+' || ':'')+document.body.innerText.slice(0,300)})()", label='o que aparece depois do clique em Registrar compra')
    c.waitfor(gone={'role': 'dialog'}, timeout=15)
    c.confere('main', ['Reposição de dreno', 'Compra direta', 'R$ 105,00', 'Concluída'], 'a compra aparece na lista: Reposição de dreno, Compra direta, R$ 105,00')
    c.ev("(()=>{const t=document.body.innerText;return t.slice(-700)})()", label='texto da tela no fim (aviso do app)')
    c.hover(SEL('main button', hasText='Compra direta'), 2.0, at=c.A(5, 'Pronto:', 0.9), label='a compra direta na lista', optional=True)
    c.fim()
    return c


def cap06():
    """De uma conta pra outra: extrato da Conta Principal, menu da linha, Transferir (Troco do caixa), extrato do Caixa, Ajustar saldo."""
    c = Cap(6, pace=0.5, start=(760, 420), setup=SETUP_MOV)
    c.mark(1)
    c.click(CONTA('Conta Principal'), at=c.A(1, 'extrato', 1.0), label='abre a Conta Principal')
    c.confere('main', ['Reposição de dreno', 'Instalação de split 12.000 BTUs - Mercado Vila Nova', 'Saldo do dia'], 'extrato com a compra direta e a receita')
    c.hover(SEL('main', hasText='Reposição de dreno'), 1.4, at=c.A(1, 'compra', 0.9), label='a compra direta no extrato', optional=True)
    c.mark(2)
    KEB = SEL("main tbody tr:has-text('Instalação de split') button[aria-label='Ações']")
    c.click(KEB, at=c.A(2, 'Editar', 1.4), label='menu ⋮ da linha da receita')
    c.pause(0.6)
    c.click(KEB, label='menu ⋮ da linha de novo (só se não abriu)', unless=ITEM('Editar'))
    c.hover(ITEM('Excluir'), 1.4, at=c.A(2, 'Excluir.', 0.9), label='Excluir (sem clicar)')
    c.press('Escape', at=c.A(2, 'Quem', -0.5), label='fecha o menu')
    c.mark(3)
    c.click(ACOES_CONTA('Conta Principal'), at=c.A(3, 'menu', 0.9), label='menu ⋮ da Conta Principal')
    c.click(ITEM('Transferir'), at=c.A(3, 'Transferir', 0.9), label='Transferir')
    c.waitfor(text='Transferência entre Contas', timeout=10)
    c.mark(4)
    c.select(SEL(f'{DLG} button[role=combobox]', nth=0), 'Conta Principal', at=c.A(4, 'Origem,', 0.9), label='Origem: Conta Principal')
    c.select(SEL(f'{DLG} button[role=combobox]', nth=1), 'Caixa', at=c.A(4, 'Destino,', 0.9), label='Destino: Caixa')
    c.type(DI('0,00'), '30000', at=c.A(4, 'Trezentos', 0.9), cps=20, label='Valor 300,00')
    c.confere_campos('300,00', 'Valor 300,00')
    c.type({'placeholder': 'Ex: Transferência para pagar fornecedor', 'within': DLG}, 'Troco do caixa', at=c.A(4, 'descrição', 0.9), cps=18, label='descrição: Troco do caixa')
    c.pause(0.5)   # o seletor/calendário anterior ainda está fechando: sem a pausa o clique de envio pode ser engolido
    c.click(BTN('Transferir', within=DLG), at=c.A(4, 'Transferir.', 0.9), label='Transferir')
    c.waitfor(gone={'role': 'dialog'}, timeout=12)
    c.mark(5)
    c.click(CONTA('Caixa'), at=c.A(5, 'aparece', 0.9), label='abre o Caixa')
    c.confere('main', ['Troco do caixa', 'R$ 1.100,00'], 'o extrato do Caixa: Troco do caixa e saldo R$ 1.100,00')
    c.hover(SEL('main', hasText='Troco do caixa'), 2.0, at=c.A(5, 'saiu', 0.9), label='a entrada Troco do caixa no Caixa', optional=True)
    c.mark(6)
    c.click(ACOES_CONTA('Caixa'), at=c.A(6, 'menu', 0.9), label='menu ⋮ do Caixa')
    c.hover(ITEM('Ajustar saldo'), 2.5, at=c.A(6, 'Ajustar', 0.9), label='Ajustar saldo (sem clicar)')
    c.press('Escape', at=c.A(6, 'diferença.', 0.1), label='fecha o menu')
    c.fim()
    return c


def cap07():
    """O cartão da empresa: "+" do grupo Cartões, Novo Cartão (fecha dia 5, vence dia 15, limite R$ 10.000,00), Criar Cartão."""
    c = Cap(7, pace=0.5, start=(760, 420), setup=SETUP_MOV)
    c.mark(1)
    c.click(BTN_MAIS('Novo cartão de crédito'), at=c.A(1, 'Clico', 0.9), label='o + do grupo Cartões (rótulo Novo cartão)')
    c.waitfor(text='Novo Cartão', timeout=10)
    c.type(DI('Ex: Nubank Crédito'), 'Cartão Empresarial', at=c.A(1, 'nome:', 0.9), cps=16, label='nome: Cartão Empresarial')
    c.mark(2)
    escolhe_tecla(c, CAMPO('Dia de fechamento'), ['D', 'i', 'a', ' ', '5', 'Enter'], c.A(2, 'fechamento,', 1.0), 'Dia de fechamento: Dia 5')
    escolhe_tecla(c, CAMPO('Dia de vencimento'), ['D', 'i', 'a', ' ', '1', '5', 'Enter'], c.A(2, 'vencimento,', 1.0), 'Dia de vencimento: Dia 15')
    c.confere_campos_texto('dlg', ['Fecha dia 5', 'Vence dia 15'], 'o cartão fecha no dia 5 e vence no dia 15 (pré-visualização)')
    c.confere('dlg', ['do mesmo mês', 'Compras feitas no dia do fechamento já entram na próxima fatura.'], 'a frase da regra do cartão')
    c.hover(P('do mesmo mês', within=DLG), 2.5, at=c.A(2, 'frase', 0.9), label='a frase da regra: fecha dia 5, vence dia 15 do mesmo mês')
    c.mark(3)
    c.hover(P('Compras feitas no dia do fechamento', within=DLG), 3.0, at=c.A(3, 'Uma', 0.5), label='compra no dia do fechamento entra na fatura seguinte')
    c.mark(4)
    c.type(DI('0,00'), '1000000', at=c.A(4, 'coloco', 0.9), cps=20, label='Limite de crédito 10.000,00')
    c.confere_campos('10.000,00', 'Limite de crédito 10.000,00')
    c.hover(SEL(f"{DLG} :text('Vence dia 15')"), 1.4, at=c.A(4, 'dez', 0.9), label='Pré-visualização: Fecha dia 5 · Vence dia 15')
    c.click(BTN('Criar Cartão', within=DLG), at=c.A(4, 'Criar', 0.9), label='Criar Cartão')
    c.waitfor(gone={'role': 'dialog'}, timeout=12)
    c.confere('main', ['Cartão Empresarial', 'Fatura em aberto R$ 0,00'], 'o cartão no grupo Cartões com a fatura em aberto')
    c.hover(CONTA('Cartão Empresarial'), 2.0, at=c.A(4, 'grupo', 0.9), label='o cartão no grupo Cartões')
    c.fim()
    return c


def cap08():
    """Compra parcelada: cartão aberto, Geral > Nova movimentação > Despesa no cartão, 3x, faturas de novembro, dezembro e janeiro."""
    c = Cap(8, pace=0.5, start=(760, 420), setup=SETUP_MOV)
    c.mark(1)
    c.click(CONTA('Cartão Empresarial'), at=0.5, label='abre o Cartão Empresarial')
    c.confere('main', ['Fatura em aberto', 'Limite total', 'Disponível', 'Fecha dia 5', 'Vence dia 15', 'Nenhuma fatura registrada'], 'o cartão vazio, sem faturas')
    c.hover(P('Nenhuma fatura registrada'), 2.0, at=c.A(1, 'faturas', 0.9), label='Nenhuma fatura registrada', optional=True)
    c.mark(2)
    c.click(CONTA('Geral (Todos)'), at=c.A(2, 'Vou', 0.9), label='Geral (Todos)')
    c.click(NOVA_MOV, at=c.A(2, 'Nova', 0.9), label='Nova movimentação')
    c.waitfor(text='Escolha como o dinheiro se movimenta.', timeout=10)
    c.click({'selector': f'{DLG} button', 'hasText': 'Dinheiro que sai da empresa.'}, at=c.A(2, 'Despesa,', 0.9), label='Despesa')
    c.waitfor(text='Registre uma receita ou despesa', timeout=10)
    c.select(COMBO('Selecione uma conta'), 'Cartão Empresarial', at=c.A(2, 'Cartão', 0.9, nth=1), label='conta: Cartão Empresarial')
    c.waitfor(text='Despesa no Cartão de Crédito', timeout=8)
    c.hover(P('Despesa no Cartão de Crédito', within=DLG), 1.6, at=c.A(2, 'bloco', 0.9), label='bloco Despesa no Cartão de Crédito')
    c.mark(3)
    c.click(COMBO('Selecione uma categoria'), at=c.A(3, 'categoria,', 0.9), label='abre a lista de categorias')
    c.type({'placeholder': 'Buscar categoria...'}, 'Ferram', at=c.A(3, 'Ferramentas', 0.9), cps=10, label='busca "Ferram"')
    c.click(OPT('Ferramentas e Equipamentos'), label='escolhe Ferramentas e Equipamentos')
    c.hover(SEL(f'{DLG} button:has(svg.lucide-plus)', nth=0), 1.6, at=c.A(3, 'botão', 0.9), label='o + colado ao campo (Nova categoria), sem clicar', optional=True)
    c.mark(4)
    c.type({'placeholder': 'Descreva a movimentação', 'within': DLG}, 'Bomba de vácuo e vacuômetro', at=c.A(4, 'descrição,', 0.9), cps=45, label='descrição')
    c.type(DI('0,00'), '129000', at=c.A(4, 'mil', 0.9), cps=20, label='Valor 1.290,00')
    c.confere_campos('1.290,00', 'Valor 1.290,00')
    data_do_dia(c, '10/11/2026', 20, 1, c.A(4, 'data', 0.9), 'Data do lançamento 20/10/2026')
    c.confere('dlg', ['20/10/2026'], 'Data do lançamento 20/10/2026')
    c.mark(5)
    c.ev(ROLA_DLG % '3000', at=c.A(5, 'Parcelas,', 1.2), label='rola até Parcelas')
    c.click(BTN_MAIS('Parcelas'), at=c.A(5, 'Parcelas,', 0.8), label='abre Parcelas')
    escolhe_tecla(c, COMBO('À vista'), ['3', 'Enter'], c.A(5, 'vezes.', 0.9), 'Parcelas: 3x')
    c.confere('dlg', ['3 parcelas distribuídas nas faturas do cartão Cartão Empresarial', '1/3', 'fatura de novembro 2026', 'fatura de dezembro 2026', 'fatura de janeiro 2027', 'R$ 430,00'], 'as 3 parcelas nas faturas de novembro, dezembro e janeiro')
    c.hover(P('3 parcelas distribuídas', within=DLG), 2.5, at=c.A(5, 'bloco', 0.9), label='o bloco mostra a fatura de cada parcela')
    c.mark(6)
    c.hover(P('Compra no cartão não sai', within=DLG), 2.0, at=c.A(6, 'não', 0.9), label='lembrete: compra no cartão não sai do caixa nem do banco')
    c.click(SALVAR, at=c.A(6, 'Salvar.', 0.9), label='Salvar')
    c.waitfor(gone={'role': 'dialog'}, timeout=12)
    c.fim()
    return c


def cap09():
    """Pagar a fatura: três faturas, a de novembro fechada (Pagar Fatura), pagar tudo pela Conta Principal, lista geral, Configurações > Usabilidade."""
    c = Cap(9, pace=0.5, start=(760, 420), setup=SETUP_MOV)
    c.mark(1)
    c.click(CONTA('Cartão Empresarial'), at=0.5, label='abre o Cartão Empresarial')
    c.confere('main', ['R$ 430,00', 'Fechada', 'Aberta', 'Pagar Fatura'], 'as três faturas de R$ 430,00, novembro Fechada e as outras Abertas')
    c.hover(SEL('main button', hasText='Novembro 2026', nth=0), 1.6, at=c.A(1, 'novembro', 0.9), label='fatura de novembro: Fechada, Pagar Fatura liberado', optional=True)
    c.mark(2)
    PAGAR = BTN('Pagar Fatura', within='main', nth=0)   # a linha da fatura também é um botão: o do nome exato é o da linha de novembro (a 1ª, a única liberada)
    c.click(PAGAR, at=c.A(2, 'Clico', 0.9), label='Pagar Fatura (novembro)')
    c.pause(0.8)
    c.click(PAGAR, label='Pagar Fatura de novo (só se a janela não abriu)', unless={'text': 'Restante a pagar'})
    c.waitfor(text='Restante a pagar', timeout=10)
    c.select(CAMPO('Pagar com'), 'Conta Principal', at=c.A(2, 'Conta', 0.9), label='Pagar com: Conta Principal')
    c.hover(P('Fatura será completamente quitada', within=DLG), 2.0, at=c.A(2, 'aviso', 0.9), label='aviso: Fatura será completamente quitada')
    c.mark(3)
    c.hover(CAMPO('Valor a pagar', tag='input'), 3.0, at=c.A(3, 'Pagando', 0.9), label='Valor a pagar já vem com o total (430,00)', optional=True)
    c.mark(4)
    c.click(BTN('Confirmar Pagamento', within=DLG), at=c.A(4, 'Confirmar', 0.9), label='Confirmar Pagamento')
    c.waitfor(gone={'role': 'dialog'}, timeout=12)
    c.confere('main', ['Paga'], 'a fatura de novembro ganha o selo Paga')
    c.mark(5)
    c.click(CONTA('Geral (Todos)'), at=c.A(5, 'Repara', 0.9), label='Geral (Todos)')
    c.confere('main', ['Pagamento de fatura'], 'a lista geral traz o pagamento da fatura')
    c.hover(SEL('main', hasText='Pagamento de fatura'), 2.0, at=c.A(5, 'pagamento', 0.9, nth=0), label='a linha do pagamento da fatura', optional=True)
    c.mark(6)
    c.add({'do': 'goto', 'url': '/configuracoes?tab=usabilidade', 'at': c.A(6, 'lembra', 0.9), 'label': 'abre Configurações > Usabilidade'})
    c.waitfor(text='Movimentações financeiras', timeout=20)
    c.hover(P('Incluir compras no cartão'), 3.0, at=c.A(6, 'Incluir', 0.9), label='Incluir compras no cartão e a dica, sem mexer')
    c.fim()
    return c


SETUP_CONTAS = SETUP_DASH + [{'do': 'goto', 'url': '/financeiro/contas'}, {'do': 'waitFor', 'text': 'Faturas de Cartão', 'timeout': 25, 'optional': True}, AGUARDA,
                             {'do': 'click', 'target': MENU_LATERAL}, {'do': 'pause', 'seconds': 0.8},
                             # 25 por página: com 10 as doze parcelas da busca ficavam em duas páginas e "aparecem todas" não batia com a tela
                             {'do': 'click', 'target': SEL('main button[role=combobox]', hasText='10')}, {'do': 'click', 'target': {'role': 'option', 'name': '25', 'exact': True}},
                             {'do': 'pause', 'seconds': 0.6}]
BUSCA_CONTAS = {'placeholder': 'Buscar por nome, descrição, categoria ou valor...'}
LINHA_CONTA = lambda txt: f"main tr:has-text('{txt}'), main [role=row]:has-text('{txt}')"
STATUS_LINHA = lambda txt: ("(async()=>{await new Promise(r=>setTimeout(r,900));const r=[...document.querySelectorAll('main tbody tr')].find(x=>x.innerText.includes(%s));"
                            "return r?r.innerText.replace(/\\s+/g,' ').slice(0,200):'linha não está na lista: '+document.querySelector('main').innerText.replace(/\\s+/g,' ').slice(300,600)})()") % json.dumps(txt)
KEBAB_CONTA = lambda txt: SEL(f"main tr:has-text('{txt}') button[aria-haspopup='menu']")


def abrir_kebab(c, kebab, item, at, label):
    """o 1º clique no ⋮ da linha logo depois de carregar a lista pode não abrir o menu (T12): pausa e 2º clique só se o item esperado ainda não apareceu"""
    c.click(kebab, at=at, label=label)
    c.pause(0.6)
    c.click(kebab, label=label + ' de novo (só se não abriu)', unless=ITEM(item))


def cap10():
    """O que vai vencer: Contas a Pagar/Receber (abas, faixa de horizonte, calendário, Exportar) e o aluguel do galpão (12 parcelas mensais)."""
    c = Cap(10, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/financeiro/contas'], setup=SETUP_CONTAS)
    c.mark(1)
    c.confere('main', ['A pagar', 'A receber', 'Vencidas', 'Próximos 7 dias', 'De 8 a 30 dias', 'Gás R-410A e tubos de cobre', 'Pendente', 'Orçamento #2 (1/3)', 'Faturas de Cartão', 'Paga'],
              'a tela: cartões, faixa de horizonte, gás pendente, orçamento #2 e a fatura de novembro Paga')
    c.hover(TAB('Todas'), 1.0, at=c.A(1, 'aba', 0.9), label='a aba Todas')
    c.mark(2)
    c.hover(TAB('A Pagar'), 0.4, at=c.A(2, 'Pagar', 0.9), label='aba A Pagar')
    c.hover(TAB('A Receber'), 0.4, at=c.A(2, 'Receber', 0.9), label='aba A Receber')
    c.hover(P('Próximos 7 dias'), 1.6, at=c.A(2, 'faixa', 0.9), label='faixa: Vencidas, Próximos 7 dias, De 8 a 30 dias')
    c.mark(3)
    c.hover(SEL(LINHA_CONTA('Gás R-410A')), 1.4, at=c.A(3, 'boleto', 0.9), label='a linha do gás')
    c.hover(SEL(LINHA_CONTA('Orçamento #2 (1/3)')), 1.6, at=c.A(3, 'primeira', 0.9), label='a linha Orçamento #2 (1/3) do Hotel Mirante do Mar')
    c.mark(4)
    c.hover(SEL('main button', hasText='Calendário'), 0.8, at=c.A(4, 'calendário,', 0.9), label='alternador Lista / Calendário')
    c.click(BTN('Exportar'), at=c.A(4, 'Exportar', 0.9), label='Exportar')
    c.waitfor(text='CSV', timeout=6)
    c.hover(ITEM('PDF'), 1.4, at=c.A(4, 'Excel,', 0.9), label='Excel, PDF e CSV')
    c.press('Escape', at=c.A(4, 'CSV.', 0.3), label='fecha sem escolher')
    c.pause(0.5)
    c.mark(5)
    c.click(BTN('Nova Conta'), at=c.A(5, 'Clico', 0.9), label='Nova Conta')
    c.waitfor(text='Nova Conta', timeout=10)
    c.type({'placeholder': 'Ex: Aluguel do escritório', 'within': DLG}, 'Aluguel do galpão', at=c.A(5, 'descrição', 0.9), cps=16, label='descrição: Aluguel do galpão')
    c.mark(6)
    c.click(COMBO('Selecione uma categoria'), at=c.A(6, 'categoria', 0.9), label='abre a lista de categorias')
    c.type({'placeholder': 'Buscar categoria...'}, 'Aluguel', at=c.A(6, 'Aluguel', 0.9), cps=10, label='busca "Aluguel"')
    c.click(OPT('Aluguel', exact=True), label='escolhe Aluguel')
    c.type(DI('0,00'), '280000', at=c.A(6, 'dois', 0.9), cps=20, label='Valor 2.800,00')
    c.confere_campos('2.800,00', 'Valor 2.800,00')
    c.hover(SEL(f'{DLG} button[aria-haspopup]', hasText='10/11/2026'), 1.2, at=c.A(6, 'dia', 0.9), label='Vencimento: hoje (dia 10)')
    c.select(COMBO('Selecione uma conta'), 'Conta Principal', at=c.A(6, 'Conta', 0.9, nth=0), label='Conta Bancária / Caixa: Conta Principal')
    c.mark(7)
    c.ev(ROLA_DLG % '2000', at=round(c.L(7) - 1.7, 2), label='rola até Parcelar ou repetir')
    c.click(BTN_MAIS('Parcelar ou repetir'), at=c.A(7, 'Parcelar', 0.9), label='abre Parcelar ou repetir')
    c.select(COMBO('Única'), 'Mensal', at=c.A(7, 'Mensal,', 0.9), label='Recorrência: Mensal')
    c.confere('dlg', ['Mensal'], 'Recorrência Mensal')
    c.ev("[...document.querySelectorAll('[role=dialog] input')].map(i=>i.value).join('|')", label='confere campos da janela (parcelas 12)')
    c.pause(0.5)   # o seletor/calendário anterior ainda está fechando: sem a pausa o clique de envio pode ser engolido
    c.click(BTN('Criar Conta', within=DLG), at=c.A(7, 'Criar', 0.9), label='Criar Conta')
    c.waitfor(gone={'role': 'dialog'}, timeout=30)
    c.mark(8)
    c.confere('main', ['Aluguel do galpão (1/12)'], 'a primeira parcela do aluguel entra na lista do mês')
    c.type(BUSCA_CONTAS, 'aluguel', at=c.A(8, 'buscando', 0.9), cps=12, label='busca "aluguel"')
    c.confere('main', ['Aluguel do galpão (1/12)', 'Aluguel do galpão (12/12)', 'de 12'], 'as doze parcelas do aluguel aparecem na busca')
    c.hover(SEL(LINHA_CONTA('Aluguel do galpão (12/12)')), 2.0, at=c.A(8, 'todos', 0.9), label='as doze parcelas, uma por mês', optional=True)
    c.type(BUSCA_CONTAS, '', at=c.A(8, 'meses.', 0.5), clear=True, label='limpa a busca')
    c.fim()
    return c


def cap11():
    """Pagar e receber: baixa do boleto do gás (Marcar como pago) e recebimento da 1ª mensalidade do PMOC (Marcar como recebido)."""
    c = Cap(11, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/financeiro/contas'], setup=SETUP_CONTAS)
    c.mark(1)
    c.click(TAB('A Pagar'), at=c.A(1, 'aba', 0.9), label='aba A Pagar')
    abrir_kebab(c, KEBAB_CONTA('Gás R-410A'), 'Marcar como pago', c.A(1, 'menu', 0.9), 'menu ⋮ da linha do gás')
    c.click(ITEM('Marcar como pago'), at=c.A(1, 'Marcar', 0.9), label='Marcar como pago')
    c.waitfor(text='Confirmar pagamento', timeout=10)
    c.confere('dlg', ['Gás R-410A e tubos de cobre', 'R$ 640,00'], 'Confirmar pagamento: Gás R-410A e tubos de cobre — R$ 640,00')
    c.mark(2)
    c.select(CAMPO('Pago com'), 'Conta Principal', at=c.A(2, 'Conta', 0.9), label='Pago com: Conta Principal')
    c.select(CAMPO('Forma de pagamento'), 'Boleto', at=c.A(2, 'boleto,', 0.9), label='Forma de pagamento: Boleto')
    c.pause(0.5)   # o seletor/calendário anterior ainda está fechando: sem a pausa o clique de envio pode ser engolido
    c.click(BTN('Confirmar', within=DLG), at=c.A(2, 'Confirmar,', 0.9), label='Confirmar')
    c.waitfor(gone={'role': 'dialog'}, timeout=12)
    c.click(TAB('Todas'), at=c.A(2, 'fica', 1.0), label='aba Todas: a baixa fica na lista com o status')
    c.hover(SEL(LINHA_CONTA('Gás R-410A')), 1.4, at=c.A(2, 'Pago.', 0.9), label='a conta do gás fica como Pago')
    c.mark(3)
    c.click(TAB('A Receber'), at=c.A(3, 'aba', 0.9), label='aba A Receber')
    c.type(BUSCA_CONTAS, 'PMOC', at=c.A(3, 'PMOC,', 0.9, nth=1), cps=10, label='busca "PMOC"')
    c.confere('main', ['Mensalidade PMOC - dez/2026 (1/12)', 'Mensalidade PMOC - nov/2027 (12/12)', 'de 12'], 'as doze mensalidades do PMOC')
    c.hover(SEL(LINHA_CONTA('Mensalidade PMOC - nov/2027 (12/12)')), 1.6, at=c.A(3, 'doze', 0.9), label='as doze mensalidades', optional=True)
    c.mark(4)
    abrir_kebab(c, KEBAB_CONTA('Mensalidade PMOC - dez/2026 (1/12)'), 'Marcar como recebido', c.A(4, 'menu', 0.9), 'menu ⋮ da mensalidade (1/12)')
    c.click(ITEM('Marcar como recebido'), at=c.A(4, 'Marcar', 0.9), label='Marcar como recebido')
    c.waitfor(text='Como foi recebido?', timeout=10)
    c.hover(P('Restante a receber', within=DLG), 2.5, at=c.A(4, 'Valor', 0.9), label='Valor recebido 1.200,00 e a dica do recebimento parcial')
    c.mark(5)
    c.select(CAMPO('Forma de pagamento'), 'PIX', at=c.A(5, 'PIX,', 0.9), label='Forma de pagamento: PIX')
    c.select(CAMPO('Caixa / Conta bancária'), 'Conta Principal', at=c.A(5, 'Conta', 0.9), label='Caixa / Conta bancária: Conta Principal')
    c.hover(P('Tarifa de máquina/gateway', within=DLG), 2.5, at=c.A(5, 'tarifa', 0.9), label='Tarifa de máquina/gateway e a dica')
    c.mark(6)
    c.pause(0.5)   # o seletor/calendário anterior ainda está fechando: sem a pausa o clique de envio pode ser engolido
    c.click(BTN('Confirmar recebimento', within=DLG), at=c.A(6, 'Confirmar', 0.9), label='Confirmar recebimento')
    c.waitfor(gone={'role': 'dialog'}, timeout=12)
    c.hover(P('Total recebido'), 0.8, at=c.A(6, 'Pronto,', 0.9), label='o Total recebido sobe: a mensalidade (1/12) foi recebida')
    c.fim()
    return c


def cap12():
    """Organizar as categorias: Configurações Financeiras > Categorias, selo Sistema, Nova categoria "Peças e componentes" (Custos diretos), subcategoria, abas."""
    c = Cap(12, pace=0.5, start=(760, 420), setup=SETUP_MOV)
    c.mark(1)
    c.click(BTN('Configurações Financeiras'), at=c.A(1, 'Configurações', 0.9), label='Configurações Financeiras')
    c.waitfor(text='Categorias de Despesa', timeout=15)
    c.hover(P('Categorias de Receita'), 1.0, at=c.A(1, 'receita', 0.9), label='Categorias de Receita')
    c.hover(P('Categorias de Despesa'), 1.0, at=c.A(1, 'despesa,', 0.9), label='Categorias de Despesa')
    c.mark(2)
    LOCK = lambda nome: SEL(f"main :text-is('{nome}') >> xpath=.. >> svg.lucide-lock")
    c.hover(LOCK('Vendas de Serviços'), 2.0, at=c.A(2, 'cadeado', 0.9), label='o cadeado de Vendas de Serviços (Categoria do sistema)', optional=True)
    c.hover(LOCK('CSP - Materiais'), 2.0, at=c.A(2, 'automáticos', 0.9), label='o cadeado de CSP - Materiais (Categoria do sistema)', optional=True)
    c.mark(3)
    c.click(BTN('Nova categoria', nth=1), at=c.A(3, 'Vou', 0.9), label='Nova categoria (despesa)')
    c.waitfor(text='Nova Categoria', timeout=10)
    c.type({'placeholder': 'Ex: Serviços', 'within': DLG}, 'Peças e componentes', at=c.A(3, 'Peças', 0.9, nth=1), cps=16, label='nome: Peças e componentes')
    c.mark(4)
    c.select(CAMPO('Onde aparece no DRE'), 'Custos diretos', at=c.A(4, 'escolho', 0.9), label='Onde aparece no DRE: Custos diretos')
    c.hover(P('Prévia no DRE', within=DLG), 2.5, at=c.A(4, 'Prévia', 0.9), label='Prévia no DRE: reduz o lucro bruto')
    c.mark(5)
    c.hover(P('Atividades operacionais', within=DLG), 1.4, at=c.A(5, 'categoria', 0.5), label='Grupo DFC, Cor e Ícone')
    c.pause(0.5)   # o seletor/calendário anterior ainda está fechando: sem a pausa o clique de envio pode ser engolido
    c.click(BTN('Criar', within=DLG), at=c.A(5, 'Criar,', 0.9), label='Criar')
    c.waitfor(gone={'role': 'dialog'}, timeout=12)
    c.confere('main', ['Peças e componentes'], 'Peças e componentes entra em Categorias de Despesa')
    c.mark(6)
    abrir_kebab(c, {'role': 'button', 'name': 'Ações de Peças e componentes', 'exact': True}, 'Adicionar subcategoria', c.A(6, 'menu', 0.9), 'menu ⋮ de Peças e componentes')
    c.hover(ITEM('Adicionar subcategoria'), 2.0, at=c.A(6, 'subcategorias,', 0.9), label='Adicionar subcategoria (sem clicar)')
    c.press('Escape', at=c.A(6, 'componentes.', 0.2), label='fecha o menu')
    c.mark(7)
    c.hover(TAB('Centro de Custo'), 1.2, at=c.A(7, 'Centro', 0.9), label='aba Centro de Custo')
    c.hover(TAB('Grupos do DRE'), 1.2, at=c.A(7, 'Grupos', 0.9), label='aba Grupos do DRE')
    c.fim()
    return c


def centrar(c, titulo, at, label, seg=0.9):
    """rola o contêiner `main` (a página não rola: AppLayout 1.38.19) até o bloco e aponta para ele; hover sem rolagem automática do robô"""
    js = ("(()=>{const els=[...document.querySelectorAll('main h2,main h3,main p,main span')].filter(e=>e.textContent.trim()===%s);const e=els[0];"
          "if(!e)return 'sem '+%s;e.scrollIntoView({block:'center',behavior:'auto'});return 'ok'})()") % (json.dumps(titulo), json.dumps(titulo))
    c.ev(js, at=round(at - 0.6, 2), label=f'rola até {label}')
    c.pause(0.3)
    c.hover(P(titulo, nth=0), seg, label=label, noScroll=True)


def cap13():
    """A visão geral do mês: Visão Geral com o mês fechado (Saldo do Período, A Receber, A Pagar, Saldo por Conta, gráficos, Últimas Movimentações)."""
    c = Cap(13, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/financeiro/relatorio'],
            setup=SETUP_DASH + [{'do': 'goto', 'url': '/financeiro/relatorio'}, {'do': 'waitFor', 'text': 'Saldo do Período', 'timeout': 25}, AGUARDA,
                                {'do': 'click', 'target': MENU_LATERAL}, {'do': 'pause', 'seconds': 0.8}])
    c.mark(1)
    c.hover(P('Saldo do Período'), 0.8, at=c.A(1, 'Saldo', 0.9), label='cartão escuro Saldo do Período')
    c.hover(BTN('Nova movimentação', within='main'), 0.6, at=c.A(1, 'lançar', 0.9), label='botões Nova movimentação e Transferir entre contas')
    c.mark(2)
    c.hover(P('A RECEBER'), 0.8, at=c.A(2, 'entrar', 0.9), label='cartão A Receber')
    c.hover(P('A PAGAR'), 0.8, at=c.A(2, 'sair', 0.9), label='cartão A Pagar')
    c.mark(3)
    c.hover(P('Saldo por Conta'), 0.9, at=c.A(3, 'Saldo', 0.9), label='Saldo por Conta, Projeção e as abas')
    c.mark(4)
    centrar(c, 'Fluxo realizado e resultado', c.A(4, 'fluxo', 0.9), 'Fluxo realizado e resultado')
    centrar(c, 'Projeção do caixa', c.A(4, 'projeção', 0.9), 'Projeção do caixa')
    centrar(c, 'Agenda de vencimentos', c.A(4, 'agenda', 0.9), 'Agenda de vencimentos')
    c.mark(5)
    centrar(c, 'Concentração das despesas', c.A(5, 'despesas', 0.9), 'Concentração das despesas')
    centrar(c, 'Evolução do resultado', c.A(5, 'evolução', 0.9), 'Evolução do resultado')
    centrar(c, 'Últimas Movimentações', c.A(5, 'últimas', 0.9), 'Últimas Movimentações')
    c.fim()
    return c


def cap14():
    """Recapitulando: montagem rápida pelas telas (contas, cartão, contas a pagar e receber, categorias, visão geral)."""
    c = Cap(14, pace=0.45, start=(760, 420), prewarm=['/dashboard', '/financeiro/movimentacoes'], setup=SETUP_MOV)
    c.mark(1)
    c.click(CONTA('Conta Principal'), at=c.A(1, 'saldo', 0.9), label='extrato da Conta Principal')
    c.hover(CONTA('Cartão Empresarial'), 0.8, at=c.A(1, 'compra', 0.9), label='coluna: Caixa, Conta Principal e Cartão Empresarial')
    c.mark(2)
    c.click(CONTA('Cartão Empresarial'), at=c.A(2, 'cartão', 0.9, nth=0), label='o cartão e as três faturas')
    c.mark(3)
    c.add({'do': 'goto', 'url': '/financeiro/contas', 'at': c.A(3, 'Contas', 0.9), 'label': 'abre Contas a Pagar/Receber'})
    c.waitfor(text='Faturas de Cartão', timeout=20, optional=True)
    c.type(BUSCA_CONTAS, 'aluguel', at=c.A(3, 'aluguel', 0.9), cps=14, label='busca "aluguel"')
    c.type(BUSCA_CONTAS, '', at=c.A(3, 'baixa', 0.9), clear=True, label='limpa a busca')
    c.mark(4)
    c.add({'do': 'goto', 'url': '/financeiro/configuracoes-financeiras?tab=categorias', 'at': c.A(4, 'organizou', 0.9), 'label': 'abre Configurações Financeiras > Categorias'})
    c.waitfor(text='Peças e componentes', timeout=20)
    c.hover(P('Peças e componentes'), 1.6, at=c.A(4, 'dê', 0.9), label='Peças e componentes em Categorias de Despesa')
    c.add({'do': 'goto', 'url': '/financeiro/relatorio', 'at': c.A(4, 'Visão', 0.9), 'label': 'abre a Visão Geral'})
    c.waitfor(text='Saldo do Período', timeout=20)
    c.mark(5)
    c.hover(P('Saldo do Período'), 2.0, at=c.A(5, 'contas', 0.9), label='a Visão Geral do mês')
    c.fim()
    return c


CAPS = {0: cap00, 1: cap01, 2: cap02, 3: cap03, 4: cap04, 5: cap05, 6: cap06, 7: cap07, 8: cap08, 9: cap09, 10: cap10, 11: cap11, 12: cap12, 13: cap13, 14: cap14}

if __name__ == '__main__':
    quais = [int(a) for a in sys.argv[1:]] or sorted(CAPS)
    for n in quais:
        c = CAPS[n]()
        if os.environ.get('ANCHORS'):
            for i, w, t in c.anchors:
                print(f'   anchor L{i} "{w}" -> {t}')
        d = c.out()
        # ajustes de `at` medidos na gravação (rec/t13/ajustes_at.json): passo que sempre chega atrasado sai mais tarde; `at` segue crescente
        aj = json.load(open(os.path.join(HERE, 'ajustes_at.json'), encoding='utf8')).get(str(n), {}) if os.path.exists(os.path.join(HERE, 'ajustes_at.json')) else {}
        if aj:
            piso = 0.0
            for stp in d['steps']:
                if 'at' in stp:
                    if stp.get('label') in aj:
                        stp['at'] = round(stp['at'] + aj[stp['label']], 2)
                    stp['at'] = round(max(stp['at'], piso), 2)
                    piso = stp['at']
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
