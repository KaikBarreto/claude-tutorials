#!/usr/bin/env python3
"""T22 · gera rec/t22/cap00..cap11.json (roteiros do robô) a partir da voz pronta (t22/narracao/capNN.json).

Ferramentas de RH (DISC, Organograma, Fluxograma) no COMPUTADOR (janela 1280x800), logada como Camila Duarte (admin, Glacial Cold Brasil), na Dominex 1.38.21,
FAKE_NOW 12/11/2026 10:00 (fim do T15). Exceção: o cap02 é no CELULAR, sem login (link do teste do Rafael).
Os `at` saem da palavra que anuncia cada passo (A(linha, palavra, folga)): o gesto "pousa" ~0,7 a 1 s depois do início do passo
(clique = deslocamento + ~0,85 s; digitação = clique + texto), então `at` = início da palavra - folga.
Rodar de qualquer pasta: `python3 -I rec/t22/gerar.py [NN ...]`. Depois: `node rec/record.mjs rec/t22/capNN.json --check`.

Cadeia de sementes: rec/t22/cadeia.json (semear.py: fim do T15 + `t22/inicio`) e, a cada capítulo, o último `t22/apos-capNN` do capítulo anterior que mexeu
no banco (SEMENTE abaixo). O `apos-capNN` sai do ensaio (`rec/t22/snap.mjs diff NN`, na mesma trava).

Particularidades (lições deste tutorial, ver docs/08-licoes.md):
 - Menu lateral RECOLHIDO (`Toggle Sidebar`) no `setup` de todo capítulo no computador (as sete abas de Funcionários e a barra do fluxograma só cabem a 1280 px assim).
 - A aba "Perfil Comportamental" abre em LISTA (padrão do app, sem "Gerar link"): o cap01 troca para "Ver como grade" (cartões) à vista; os demais capítulos já partem da grade (`storage`).
 - Observador `OBS` guarda em `window.__avisos` todo aviso de erro do app, tela escura e faixa da trilha Domiflix; o passo final devolve a lista (tem de sair vazia).
 - `confere*` LÊ a tela e compara com a fala (o `resumo.py` acusa DIFERENTE).
"""
import json
import os
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TUT = os.path.normpath(os.path.join(HERE, '..', '..'))
NARR = os.path.join(TUT, 't22', 'narracao')
CAD = json.load(open(os.path.join(HERE, 'cadeia.json'), encoding='utf8'))
BASE = CAD['inicio']
STORAGE = {'dominex:portal-tickets-seen:d40f5787-1779-501f-900c-ddb2b90a36e5': '2031-01-01T00:00:00.000Z'}
STORAGE_GRADE = {**STORAGE, 'disc-overview-view-mode': 'grid'}
# Observador de avisos de erro na tela (aceite da fase 1): guarda em window.__avisos todo texto que apareça com "Não foi possível", "erro",
# "Tente novamente" ou "indisponível"; o passo final de cada capítulo devolve a lista (o resumo imprime) e ela tem de sair vazia.
OBS = ("(()=>{window.__avisos=[];const re=/N[ãa]o foi poss[ií]vel|Erro ao|Tente novamente|indispon[ií]vel/i;const chk=(t)=>{t=(t||'').trim();"
       "const m=t&&t.match(new RegExp('[^]{0,40}('+re.source+')[^]{0,40}','i'));"
       "if(m&&window.__avisos.length<10)window.__avisos.push(m[0].replace(/[\\n\\r\\t ]+/g,' '))};new MutationObserver(ms=>{for(const m of ms){"
       "m.addedNodes.forEach(n=>chk(n.textContent));if(m.type==='characterData')chk(m.target.textContent)}}).observe(document.body,"
       "{childList:true,subtree:true,characterData:true});chk(document.body.innerText);"
       # tela escura de introdução e faixa de lembrete da trilha Domiflix (G1)
       "setInterval(()=>{const f=document.querySelector('section[aria-label^=\"Lembrete da trilha\"]');"
       "const e=[...document.querySelectorAll('div.fixed')].some(x=>getComputedStyle(x).backgroundColor==='rgb(17, 17, 17)');"
       "if((f||e)&&window.__avisos.length<10&&!window.__avisos.includes('TRILHA DOMIFLIX'))window.__avisos.push('TRILHA DOMIFLIX')},300);return 1})()")

NOMES = ['Abertura', 'O teste DISC', 'Respondendo pelo celular', 'Lendo o perfil', 'Interações e comparação', 'A evolução do perfil', 'Montando a estrutura',
         'Organizar e encontrar', 'Desenhando a rotina', 'Raias e responsáveis', 'Conferência e POP', 'Recapitulando']
# estado de partida de cada capítulo: o último apos-capNN (de capítulo anterior) que mexeu no banco. cap01 gera a avaliação pendente (entrada do 2), cap02 a respondida (3 a 6),
# cap06 o organograma (7), cap07 o arranjo e a caixa (8), cap08 o fluxograma desenhado (9), cap09 as raias (10), cap10 "Sobre o processo" (11). Os capítulos 3, 4, 5 e 11 só leem.
SEMENTE = {0: None, 1: None, 2: 'apos-cap01', 3: 'apos-cap02', 4: 'apos-cap02', 5: 'apos-cap02', 6: 'apos-cap02', 7: 'apos-cap06', 8: 'apos-cap07', 9: 'apos-cap08',
           10: 'apos-cap09', 11: 'apos-cap10'}


def short_code(seed, n=12):
    """igual a shortCode() do fakebase (core/util.mjs): sha1 do texto, alfabeto base32 sem ambíguos"""
    import hashlib
    a = 'abcdefghjkmnpqrstuvwxyz23456789'
    d = hashlib.sha1(str(seed).encode()).digest()
    return ''.join(a[d[i] % len(a)] for i in range(n))


# link do teste do Rafael: o 1º link dele (hooks/disc_assessments.mjs: código = nome + ordem do link) e as 28 perguntas que o sorteio mostra nele
CODIGO_RAFAEL = short_code('disc_assessments:Rafael Lima:0')


def form_rafael():
    import subprocess
    out = subprocess.run(['node', os.path.join(HERE, 'disc_form.mjs'), CODIGO_RAFAEL], capture_output=True, check=True, text=True).stdout
    return json.loads(out)


def norm(s):
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode().lower()
    return ''.join(ch for ch in s if ch.isalnum() or ch in '?')


class Cap:
    def __init__(s, n, pace=0.5, cps=9, start=(760, 420), prewarm=None, setup=None, user=None, phone=False, anonymous=False, storage=None, noscroll=False):
        s.n = n
        d = json.load(open(f'{NARR}/cap{n:02d}.json', encoding='utf8'))
        s.words, s.linhas, s.dur = d['words'], d['linhas'], d['dur']
        s.steps = []
        s.pace, s.cps, s.start = pace, cps, start
        s.prewarm = prewarm or ['/dashboard', '/funcionarios']
        s.phone, s.anonymous, s.storage = phone, anonymous, storage if storage is not None else STORAGE_GRADE
        s.noscroll = noscroll   # quadros em tela cheia (organograma, fluxograma): barra de botões em y ~30, fora da faixa 96..H-70 do robô; sem isto cada clique tenta rolar ~6 s
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
        if s.noscroll and d.get('do') in ('click', 'hover', 'type', 'drag') and 'noScroll' not in kw:
            kw = {**kw, 'noScroll': True}
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

    def digitar_num(s, target, texto, at=None, label=None, cps=None, **kw):
        """Campo `type=number` com 0 de partida (o app reescreve 0 ao apagar: "032"): clica, seleciona tudo (Ctrl+A) e digita POR CIMA, sem Backspace.
        `cps` (opcional, fase 2): velocidade da digitação deste campo (padrão: a do capítulo)."""
        s._p({'do': 'click', 'target': target}, at, (label + ' (clique)') if label else None, dict(kw))
        s.add({'do': 'press', 'key': 'Control+A'})
        d = {'do': 'type', 'target': target, 'text': texto, 'noClick': True, 'label': label}
        if cps:
            d['cps'] = cps
        return s.add(d)

    def clicar_colar(s, target, texto, at=None, label=None, **kw):
        """clica no campo (no `at`) e o preenche de uma vez, como um "colar" (`colar`, ~0,05 s): texto longo que não cabe digitado na fala (fase 2)"""
        s._p({'do': 'click', 'target': target}, at, (label + ' (clique)') if label else None, dict(kw))
        s.add({'do': 'press', 'key': 'Control+A'})
        return s.colar(texto, None, label)

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
        js = ("(async()=>{await new Promise(r=>setTimeout(r,1800));const el=document.querySelector(%s);const t=(el?el.innerText:'').replace(/[\\s\\u00a0]+/g,' ').toLowerCase();"
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
            'name': f't22-cap{s.n:02d}',
            'title': f'T22 · Cap. {s.n} · {NOMES[s.n]} (narração {str(round(s.dur, 1)).replace(".", ",")} s; marcas L1..L{len(s.linhas)} = início de cada linha do roteiro)',
            'seed': f't22-cap{s.n:02d}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
            'start': {'x': s.start[0], 'y': s.start[1]},
            'seedExtra': list(BASE) + ([f't22/{sem}'] if sem else []),
            'prewarm': s.prewarm, 'setup': s.setup, 'steps': s.steps,
            'storage': dict(s.storage),
        }
        if s.user:
            d['user'] = s.user
        if s.phone:
            d['device'] = 'phone'
        if s.anonymous:
            d['anonymous'] = True
        return d


# ---------------------------------------------------------------- alvos
BTN = lambda n, **kw: {'role': 'button', 'name': n, 'exact': True, **kw}
BTNX = lambda n, **kw: {'role': 'button', 'name': n, **kw}               # nome por substring ("Filtros" vira "Filtros, 1 ativo" com filtro ativo)
LINK = lambda n, **kw: {'role': 'link', 'name': n, 'exact': True, **kw}
TAB = lambda n, **kw: {'role': 'tab', 'name': n, 'exact': True, **kw}
TXT = lambda t, **kw: {'text': t, 'exact': True, **kw}                    # texto INTEIRO igual (e na mesma caixa)
P = lambda t, **kw: {'text': t, 'within': 'main', **kw}
P_ = lambda t, **kw: {'text': t, **kw}                                        # texto por substring em qualquer parte (página pública, sem <main>)                   # texto por substring, sem diferenciar caixa
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




SETUP_FUNC = SETUP_DASH + [{'do': 'goto', 'url': '/funcionarios'}, {'do': 'waitFor', 'text': 'Funcionários (RH)', 'timeout': 25}, AGUARDA,
                            {'do': 'click', 'target': MENU_LATERAL}, {'do': 'pause', 'seconds': 0.8}]   # tela de Funcionários, menu lateral recolhido
SALVAR = BTN('Salvar', within=DLG)


def escolhe(c, combo_txt, opcao, at, label, **kw):
    """abre o seletor da janela (pelo texto que ele mostra) e escolhe a opção"""
    return c.select(COMBO(combo_txt), opcao, at=at, label=label, **kw)


# ---------------------------------------------------------------- alvos próprios do T22 (RH: DISC, organograma, fluxograma)
ABA = lambda n: TAB(n)                                                     # abas de Funcionários (role tab)
CARTAO = lambda nome: SEL(f"main div[role=button]:has-text('{nome}')")      # cartão de um funcionário na grade do Perfil Comportamental
CARTAO_BTN = lambda nome, texto: SEL(f"main div[role=button]:has-text('{nome}') button:has-text('{texto}')")
GRADE = BTN('Ver como grade')
OPCAO = lambda nome: {'role': 'option', 'name': nome}                      # item do seletor de funcionário (cmdk): nome por substring
QUADRO = '.react-flow'                                                      # tela do React Flow (organograma e fluxograma)
NO = lambda texto: SEL('.react-flow__node', hasText=texto)                  # caixa do quadro pelo texto que mostra


def setup_func(aba=None, extra=()):
    """não filmado: Funcionários (RH) com o menu lateral recolhido, já na aba (o capítulo que a mostra abrindo faz o clique à vista)"""
    s = list(SETUP_FUNC)
    if aba:
        s += [{'do': 'click', 'target': ABA(aba)}, AGUARDA, {'do': 'pause', 'seconds': 0.6}]
    return s + list(extra)


def cap_novo(n, **kw):
    kw.setdefault('prewarm', ['/dashboard', '/funcionarios'])
    kw.setdefault('start', (760, 420))
    return Cap(n, pace=0.5, **kw)


# ================================================================ capítulos
def cap00():
    """Abertura: Dashboard, menu Gestão > Funcionários (RH), a câmera passa pelas três abas."""
    c = cap_novo(0, setup=SETUP_DASH, storage=STORAGE)
    c.mark(1)
    # fase 2 (ritmo, gravação de 05/11 23:57): o 1º gesto leva ~2,7 s (o painel ainda se acomoda) e o clique em Funcionários ~2,4 s (navegação):
    # sem o hover de passagem pelo menu, o Gestão sai em 0,5 s, sem a pausa depois de recolher o menu; respiro na voz depois de "da Dominex:"
    c.click(BTN('Gestão'), at=0.5, label='abre o grupo Gestão do menu')
    c.click(LINK('Funcionários (RH)'), at=c.A(1, 'RH', 0.9), label='abre Funcionários (RH)')
    c.waitfor(text='Perfil Comportamental', timeout=20)
    c.click(MENU_LATERAL, at=c.A(1, 'perfil', 1.6), label='recolhe o menu lateral')
    c.hover(ABA('Perfil Comportamental'), 0.3, at=c.A(1, 'perfil', 0.9), label='aba Perfil Comportamental')
    c.hover(ABA('Organograma'), 0.3, at=c.A(1, 'organograma', 0.9), label='aba Organograma')
    c.hover(ABA('Fluxograma'), 0.3, at=c.A(1, 'fluxograma.', 0.9), label='aba Fluxograma')
    c.mark(2)
    c.hover(ABA('Perfil Comportamental'), 0.9, at=c.A(2, 'Uma', 0.9), label='Perfil Comportamental (entender cada pessoa)')
    c.hover(ABA('Organograma'), 0.9, at=c.A(2, 'outra', 0.9), label='Organograma (quem responde a quem)')
    c.hover(ABA('Fluxograma'), 0.9, at=c.A(2, 'terceira', 0.9), label='Fluxograma (como o trabalho acontece)')
    c.mark(3)
    c.hover(P('Funcionários (RH)'), 0.9, at=c.A(3, 'Funcionários', 0.9), label='tela Funcionários (RH)')
    c.mark(4)
    c.fim()
    return c


def cap01():
    """O teste DISC: aba Perfil Comportamental, grade de cartões, Gerar link do Rafael, janela com a opção de ver o resultado, link copiado."""
    c = cap_novo(1, setup=setup_func(), storage=STORAGE)
    c.mark(1)
    c.click(ABA('Perfil Comportamental'), at=0.3, label='aba Perfil Comportamental')
    c.waitfor(text='Sem teste', timeout=15)
    c.mark(2)
    # fala nova (1.38.21): "Troco pra grade, e cada pessoa da equipe ganha um cartão." -> a L1 fica na LISTA e a troca é na L2, no "grade"
    c.click(GRADE, at=c.A(2, 'grade', 1.0), label='troca para a grade (cartões)')
    c.waitfor(text='Gerar link', timeout=10)
    c.confere('main', ['Bruno Alves', 'Rafael Lima', 'Sem teste', 'Respondido em 05/11/2026'], 'cartões da equipe (Bruno respondido em 05/11/2026)')
    c.hover(P('Bruno Alves'), 1.2, at=c.A(2, 'Bruno', 0.9), label='cartão do Bruno Alves', optional=True)
    c.mark(3)
    c.click(CARTAO_BTN('Rafael Lima', 'Gerar link'), at=c.A(3, 'Clico', 1.2), label='Gerar link do Rafael')
    c.waitfor(text='Gerar link de avaliação', timeout=10)
    c.confere('dlg', ['Gerar link de avaliação', 'Funcionário vê o resultado ao final', 'Você pode mudar isso a cada avaliação'], 'janela Gerar link de avaliação (opção ligada)')
    c.hover(SW('Funcionário vê o resultado ao final', within=DLG), 1.0, at=c.A(3, 'decide', 0.9), label='opção Funcionário vê o resultado ao final')
    c.hover(PD('O padrão vem das configurações da empresa'), 0.9, at=c.A(3, 'padrão', 0.9), label='dica: o padrão vem das configurações da empresa')
    c.mark(4)
    c.click(BTN('Gerar link', within=DLG), at=c.A(4, 'link', 1.0), label='Gerar link (confirma)')
    c.waitfor(text='Link gerado e copiado!', timeout=10)
    c.confere('body', ['Link gerado e copiado!', '/avaliacao/rafael-lima-'], 'aviso Link gerado e copiado!')
    c.confere('main', ['Aguardando resposta', 'Copiar link'], 'cartão do Rafael: Aguardando resposta e Copiar link')
    c.hover(CARTAO_BTN('Rafael Lima', 'Copiar link'), 1.2, at=c.A(4, 'Ele', 0.9), label='cartão do Rafael: Aguardando resposta', optional=True)
    c.fim()
    return c




def cap02():
    """Respondendo pelo celular: link do Rafael (sem login), intro, Começar, 28 perguntas (escala pelo teclado, alternativas por toque), Enviar respostas, resultado."""
    form = form_rafael()
    rota = f'/avaliacao/rafael-lima-{CODIGO_RAFAEL}'
    setup = [{'do': 'goto', 'url': rota}, {'do': 'waitFor', 'text': 'Olá, Rafael!', 'timeout': 25}, AGUARDA]
    c = cap_novo(2, setup=setup, phone=True, anonymous=True, start=(195, 420), prewarm=[rota], storage={})
    c.mark(1)
    c.hover(TXT('Teste de Perfil Comportamental (DISC)'), 1.2, at=c.A(1, 'celular', 0.9), label='Teste de Perfil Comportamental (DISC)')
    c.hover(P_('Olá, Rafael!'), 1.0, at=c.A(1, 'Leva', 0.9), label='Olá, Rafael!')
    c.mark(2)
    c.rolar(260, at=c.A(2, 'perguntas', 0.9), label='desce até Como funciona', ponto=(195, 420), duration=0.8)
    c.hover(P_('Como funciona'), 1.2, at=c.A(2, 'escala,', 0.9), label='Como funciona')
    c.hover(P_('Não existe resposta certa ou errada'), 1.4, at=c.A(2, 'vale', 0.9), label='Não existe resposta certa ou errada')
    c.mark(3)
    c.click(BTN('Começar'), at=c.A(3, 'Começar.', 0.9), label='Começar')
    c.waitfor(text='Pergunta 1 de 28', timeout=10)
    total = form['total']
    for k, p in enumerate(form['passos'], 1):
        ult = k == total
        if p['tipo'] == 'escala':
            c.pause(0.45)
            c.ev("[...document.querySelectorAll('[role=slider]')].pop().focus()", label=f'rápido (4x): pergunta {k}, foco na escala')
            c.press(str(p['resposta']), label=f'rápido (4x): pergunta {k}, nota {p["resposta"]}')
            if not ult:
                c.press('Enter', label=f'rápido (4x): pergunta {k}, avança')
        else:
            c.click(SEL('[role=radio]', nth=p['posicao']), label=f'rápido (4x): pergunta {k}, escolhe a alternativa {p["posicao"] + 1}')
        if not ult:
            c.waitfor(text=f'Pergunta {k + 1} de {total}', timeout=8)
    c.mark(4)
    c.click(BTN('Enviar respostas'), at=c.A(4, 'Enviar', 0.9), label='Enviar respostas')
    c.waitfor(text='Seu perfil comportamental', timeout=15)
    c.confere('body', ['Seu perfil comportamental', form['perfil']['profileCode']], f'resultado do Rafael: perfil {form["perfil"]["profileCode"]}')
    c.fim()
    return c


# ---- ficha do funcionário (Perfil Comportamental): alvos e rolagem
SUBABA = lambda n: {'role': 'tab', 'name': n, 'exact': True}               # Visão geral / Interações / Histórico
VER_DET = lambda nome: SEL(f"main div[role=button]:has-text('{nome}') >> text=Ver detalhes")
FORA = (1268, 520)    # px CSS: margem direita da página (padding do <main>), longe de qualquer gráfico DISC (o tooltip dele cita pessoas reais, P6)


def js_main_ate(texto, y=250, dur_ms=1000, prefixo=False):
    """rolagem suave até a folha do DOM cujo texto é `texto` (procurada dentro do <main>) ficar em y px CSS; o cursor não se mexe.
    Rola o CONTÊINER QUE ROLA de verdade (o ancestral mais próximo com overflow auto/scroll e conteúdo maior que a caixa): o 1º <main> do
    documento é o SidebarInset (overflow hidden, não rola); quem rola é o <main> interno do AppLayout (fase 2, 05/11: na fase 1 a rolagem
    pelo 1º <main> não mexia em nada e o eval devolvia o topo do alvo ainda fora da tela, 1674 px).
    Devolve o topo final do alvo (deve sair perto de `y`), 'ok' (já estava lá) ou 'SEM ALVO' (o texto não existe)."""
    busca = ("[...m.querySelectorAll('*')].filter(e=>e.textContent.trim().startsWith(%s)).sort((a,b)=>a.textContent.length-b.textContent.length)[0]" if prefixo
             else "[...m.querySelectorAll('*')].find(e=>e.children.length===0&&e.textContent.trim()===%s)") % json.dumps(texto)
    return ("(async()=>{const m=document.querySelector('main');const el=" + busca + ";"
            "if(!el)return 'SEM ALVO';const sc=(()=>{for(let p=el.parentElement;p;p=p.parentElement){const s=getComputedStyle(p);"
            "if(/(auto|scroll)/.test(s.overflowY)&&p.scrollHeight>p.clientHeight+4)return p}return document.scrollingElement})();"
            "const dy=Math.round(el.getBoundingClientRect().top-%d);if(Math.abs(dy)<3)return 'ok';const y0=sc.scrollTop,t0=performance.now();"
            "await new Promise(res=>{const f=t=>{const p=Math.min(1,(t-t0)/%d),e=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;sc.scrollTo({top:y0+dy*e,behavior:'instant'});"
            "p<1?requestAnimationFrame(f):res()};requestAnimationFrame(f)});return Math.round(el.getBoundingClientRect().top)})()") % (y, dur_ms)


def rola_ate(c, texto, at, label, y=250, dur_ms=1000, prefixo=False):
    return c.ev(js_main_ate(texto, y, dur_ms, prefixo), at=at, label=label)


def rola_topo(c, at, label, dur_ms=700):
    """sobe ao topo todo contêiner rolado dentro do <main> (o <main> interno do AppLayout; ver js_main_ate)"""
    js = ("(async()=>{const ms=[...document.querySelectorAll('main, main *')].filter(e=>e.scrollTop>2);if(!ms.length)return 'ok';"
          "const y0=ms.map(e=>e.scrollTop),t0=performance.now();await new Promise(res=>{const f=t=>{const p=Math.min(1,(t-t0)/%d),"
          "e=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;ms.forEach((m,i)=>m.scrollTo({top:y0[i]*(1-e),behavior:'instant'}));p<1?requestAnimationFrame(f):res()};"
          "requestAnimationFrame(f)});return 'topo '+y0.join(',')})()") % dur_ms
    return c.ev(js, at=at, label=label)


def estaciona(c, at, label='cursor na margem direita (fora dos gráficos)'):
    """leva o cursor à margem direita da página, sem rolar nada: gráficos que passem sob ele não mostram tooltip"""
    return c._p({'do': 'scroll', 'point': {'x': FORA[0], 'y': FORA[1]}, 'by': 0, 'duration': 0.4, 'after': 0}, round(max(0.0, at), 2), label, {})


def abre_ficha(c, nome, at, label):
    """clica em "Ver detalhes" do cartão e espera a ficha (sub-aba Visão geral)"""
    c.click(VER_DET(nome), at=at, label=label)
    c.waitfor(text='Visão geral', timeout=15)
    c.add(AGUARDA)


def setup_ficha(nome, subaba=None):
    """não filmado: abre a ficha do funcionário (e a sub-aba) fora do vídeo"""
    s = setup_func('Perfil Comportamental') + [{'do': 'click', 'target': VER_DET(nome)}, {'do': 'waitFor', 'text': 'Visão geral', 'timeout': 15}, AGUARDA,
                                               {'do': 'pause', 'seconds': 0.8}]
    if subaba:
        s += [{'do': 'click', 'target': SUBABA(subaba)}, AGUARDA, {'do': 'pause', 'seconds': 0.8}]
    return s


def cap03():
    """Lendo o perfil: cartão do Rafael respondido, Ver detalhes, ficha (Visão geral), rolagem pelas seções, aviso, Ver PDF (só zoom)."""
    c = cap_novo(3, setup=setup_func('Perfil Comportamental'))
    c.mark(1)
    c.confere('main', ['Rafael Lima', 'Respondido em 12/11/2026'], 'cartão do Rafael: Respondido em 12/11/2026')
    c.hover(P('Respondido em 12/11/2026'), 0.8, at=c.A(1, 'perfil', 0.9), label='cartão do Rafael respondido', optional=True)
    # fase 2 (gravação de 06/11 00:03): o clique em "Ver detalhes" leva ~1,9 s e a ficha ~1 s para abrir: o clique sai 0,6 s antes e a marca L2 entra
    # logo depois dele (a ficha aparece no "No alto vem o perfil dele"); o cursor vai para a margem quando a ficha já abriu
    c.click(VER_DET('Rafael Lima'), at=c.A(1, 'Ver', 1.6), label='Ver detalhes do Rafael')
    c.mark(2)
    c._p({'do': 'waitFor', 'text': 'Visão geral', 'timeout': 15}, round(c.L(2) - 0.9, 2), None, {})
    c.add(AGUARDA)
    c.confere('main', ['O Metódico', 'Sobre o seu perfil', 'Gráfico DISC', 'Qualidades', 'Pontos de atenção', 'Motivadores de carreira'], 'ficha do Rafael: O Metódico, Sobre o seu perfil, Gráfico DISC, Qualidades...')
    c.hover(P('Sobre o seu perfil'), 0.5, at=c.A(2, 'resumo', 1.3), label='perfil e resumo do estilo')
    # fase 2 (gravação de 06/11 00:26): com a rolagem consertada, o gráfico DISC passava por baixo do cursor parado no "Sobre o seu perfil" e
    # abria o tooltip do fator, que cita uma pessoa real (P6). O cursor volta à margem ANTES de rolar
    estaciona(c, at=c.A(2, 'gráfico', 1.6), label='cursor de volta à margem (o gráfico DISC vai passar por baixo)')
    rola_ate(c, 'Gráfico DISC', at=c.A(2, 'gráfico', 1.2), label='desce até o Gráfico DISC (cursor fora)', y=200)
    c.mark(3)
    rola_ate(c, 'Qualidades', at=c.A(3, 'Logo', 0.9), label='desce até Qualidades e Pontos de atenção', y=200)
    c.mark(4)
    for rot, pal in [('Competências Comportamentais', 'competências,'), ('Perfil emocional', 'emocional,'), ('Onde brilha', 'brilha'), ('Como liderar e comunicar', 'liderar')]:
        rola_ate(c, rot, at=c.A(4, pal, 0.9), label=f'desce até {rot}', y=200)
    c.mark(5)
    rola_ate(c, 'Motivadores de carreira', at=c.A(5, 'motivadores', 0.9), label='desce até Motivadores de carreira', y=200)
    rola_ate(c, 'Esta é uma ferramenta de autoconhecimento e comunicação de equipe. Não é um teste clínico nem um diagnóstico. Nenhum perfil é melhor ou pior que outro.',
             at=c.A(5, 'aviso:', 0.9), label='aviso: ferramenta de autoconhecimento', y=420)
    c.mark(6)
    rola_topo(c, at=c.A(6, 'Ver', 1.4), label='sobe ao cabeçalho da ficha')
    c.hover(BTN('Ver PDF'), 1.6, at=c.A(6, 'PDF', 0.9), label='Ver PDF (só zoom, sem clicar)')
    c.fim()
    return c


def cap04():
    """Interações e comparação: sub-aba Interações, Bruno, Atritos/Sinergias/Melhor comunicação, Ver comparação (zoom), Voltar, Comparar Rafael x Bruno."""
    c = cap_novo(4, setup=setup_ficha('Rafael Lima'))
    c.mark(1)
    c.click(SUBABA('Interações'), at=c.A(1, 'Interações,', 0.9), label='sub-aba Interações')
    c.waitfor(text='Como se comporta com', timeout=10)
    c.click(SEL('button[role=combobox]', hasText='Selecione um funcionário'), at=c.A(1, 'escolho', 0.9), label='seletor de funcionário')
    c.click(OPCAO('Bruno Alves'), label='escolhe Bruno Alves')
    c.waitfor(text='Atritos', timeout=10)
    c.confere('main', ['Atritos', 'Sinergias', 'Melhor comunicação', 'Ver comparação', 'O Metódico', 'O Especialista'], 'interações Rafael x Bruno')
    c.mark(2)
    estaciona(c, at=max(0.0, c.L(2) - 1.5))
    # fala nova (1.38.21): "Aparecem os dois perfis no mesmo gráfico, os atritos..." -> primeiro os gráficos cruzados (o título fica em y ~590
    # logo depois de escolher o Bruno, com os gráficos abaixo da dobra), depois Atritos, Sinergias e Melhor comunicação
    rola_ate(c, 'Gráfico DISC cruzado', at=c.A(2, 'Aparecem', 0.4), label='desce até os gráficos cruzados (cursor fora)', y=200)
    rola_ate(c, 'Atritos', at=c.A(2, 'atritos', 0.6), label='desce até Atritos (cursor fora dos gráficos)', y=220)
    rola_ate(c, 'Sinergias', at=c.A(2, 'sinergias', 1.2), label='desce até Sinergias', y=220)
    rola_ate(c, 'Melhor comunicação', at=c.A(2, 'melhor', 1.2), label='desce até Melhor comunicação', y=220)
    c.mark(3)
    rola_topo(c, at=c.A(3, 'Ver', 1.4), label='sobe ao cabeçalho')
    c.hover(BTN('Ver comparação'), 1.4, at=c.A(3, 'comparação', 0.9), label='Ver comparação (só zoom, sem clicar)')
    c.mark(4)
    # fala nova (1.38.21): "Volto pra aba Perfil Comportamental. Com dois perfis respondidos, ela ganha o Comparar." (o Voltar da ficha sai para a
    # aba Funcionários). Âncoras: "Volto" e "Perfil" (o "Com" casaria com "Comportamental", que vem antes, e "perfis" com o "Com dois perfis")
    c.click(BTN('Voltar'), at=c.A(4, 'Volto', 0.9), label='Voltar (sai para a aba Funcionários)')
    c.waitfor(text='Novo Funcionário', timeout=10)
    c.click(ABA('Perfil Comportamental'), at=c.A(4, 'Perfil', 0.8), label='volta à aba Perfil Comportamental (o Voltar sai para Funcionários)')
    c.waitfor(text='Comparar', timeout=10)
    # os 4 cliques da escolha (dois seletores, duas opções) levam ~3,6 s e a fala "Escolho o Rafael e o Bruno" tem ~2 s: o Comparar entra no
    # "ganha", o 1º seletor 1,4 s antes do "Escolho" e a opção do Bruno na virada para a L5 ("Os dois perfis ficam no mesmo gráfico")
    c.click(BTN('Comparar'), at=c.A(4, 'ganha', 1.0), label='Comparar')
    c.waitfor(text='Comparar perfis', timeout=10)
    c.click(SEL('button[role=combobox]', hasText='Selecione um funcionário', nth=0), at=c.A(4, 'Escolho', 1.4), label='Primeiro funcionário')
    c.click(OPCAO('Rafael Lima'), at=c.A(4, 'Rafael', 0.9), label='escolhe Rafael Lima')
    c.click(SEL('button[role=combobox]', hasText='Selecione um funcionário', nth=0), label='Segundo funcionário')
    c.mark(5)
    c.click(OPCAO('Bruno Alves'), at=round(c.L(5) - 0.9, 2), label='escolhe Bruno Alves')
    c.waitfor(text='Gráfico DISC cruzado', timeout=10)
    estaciona(c, at=c.L(5) + 0.1)
    rola_ate(c, 'Gráfico DISC cruzado', at=c.A(5, 'gráfico,', 1.2), label='Gráfico DISC cruzado (cursor fora)', y=200)
    rola_ate(c, 'Radar de competências cruzado', at=c.A(5, 'competências', 1.2), label='Radar de competências cruzado (cursor fora)', y=200)
    rola_ate(c, 'Atritos', at=c.A(5, 'lado', 2.0), label='desce por Atritos, Sinergias e Melhor comunicação', y=220)
    c.click(BTN('Voltar'), label='Voltar')
    c.fim()
    return c


def cap05():
    """A evolução do perfil: ficha do Bruno, Histórico, Evolução do perfil, Linha do tempo, Nova avaliação (só zoom)."""
    c = cap_novo(5, setup=setup_func('Perfil Comportamental'))
    c.mark(1)
    abre_ficha(c, 'Bruno Alves', at=c.A(1, 'Bruno', 0.9), label='Ver detalhes do Bruno')
    c.click(SUBABA('Histórico'), at=c.A(1, 'Histórico', 0.9), label='sub-aba Histórico')
    c.waitfor(text='Evolução do perfil', timeout=10)
    c.confere('main', ['Ao responder a nova avaliação', 'Evolução do perfil', 'Comparando com a avaliação anterior', 'Sua Influência subiu', 'Linha do tempo', 'Ver desta data'], 'histórico do Bruno')
    c.mark(2)
    estaciona(c, at=max(0.0, c.L(2) - 1.5))
    rola_ate(c, 'Evolução do perfil', at=c.A(2, 'evolução', 1.0), label='Evolução do perfil (cursor fora dos gráficos)', y=200)
    rola_ate(c, 'Comparando com a avaliação anterior:', at=c.A(2, 'explica', 1.2), label='texto: Comparando com a avaliação anterior', y=300, prefixo=True)
    c.mark(3)
    rola_ate(c, 'Linha do tempo', at=c.A(3, 'linha', 0.9), label='desce até a Linha do tempo', y=200)
    c.mark(4)
    rola_topo(c, at=c.A(4, 'dica:', 0.9), label='sobe ao cabeçalho')
    c.hover(BTN('Nova avaliação'), 1.6, at=c.A(4, 'Nova', 0.9), label='Nova avaliação (só zoom, sem clicar)')
    c.fim()
    return c


# ---- organograma e fluxograma (React Flow): alvos e gestos
IN = lambda rotulo, tag='input': SEL(f"label:text-is('{rotulo}') + {tag}")        # campo logo abaixo do rótulo (os <label> do painel não são associados ao campo)
COR = lambda k: SEL("label:text-is('Cor do setor') ~ div button", nth=k)           # bolinha de cor do painel "Editar nó" (0 = "Sem cor")
PLUS = lambda no, i: SEL(f".react-flow__node:has-text('{no}') button[aria-label='Adicionar nó'] >> nth={i}")   # "+" de uma caixa: 0 cima, 1 baixo, 2 esquerda, 3 direita
HANDLE = lambda no, lado, tipo: SEL(f".react-flow__node:has-text('{no}') .react-flow__handle-{lado}.{tipo}")
FORMA = lambda nome: SEL('[data-radix-popper-content-wrapper] button', hasText=nome)   # item da lista "Adicionar forma"
SALVO = {'text': 'Salvo'}


def js_clique_ponto(x, y):
    """clique sintético (ponteiro + mouse + click COM coordenadas) no que estiver sob (x, y): serve para o fundo do quadro, onde o clique do robô cairia numa caixa"""
    return (f"(()=>{{const x={x},y={y};const el=document.elementFromPoint(x,y);if(!el)return 'SEM ALVO';const o={{bubbles:true,cancelable:true,composed:true,clientX:x,clientY:y,button:0,view:window}};"
            "const pe=(t,b)=>new PointerEvent(t,{...o,pointerId:1,pointerType:'mouse',isPrimary:true,buttons:b});const me=(t,b)=>new MouseEvent(t,{...o,buttons:b,detail:1});"
            "el.dispatchEvent(pe('pointerdown',1));el.dispatchEvent(me('mousedown',1));el.dispatchEvent(pe('pointerup',0));el.dispatchEvent(me('mouseup',0));el.dispatchEvent(me('click',0));return el.className.toString().slice(0,40)})()")


def clique_ponto(c, x, y, at, label):
    c._p({'do': 'scroll', 'point': {'x': x, 'y': y}, 'by': 0, 'duration': 0.4, 'after': 0}, round(max(0.0, at - 0.9), 2), label + ' (cursor)', {})
    return c._p({'do': 'eval', 'js': js_clique_ponto(x, y)}, round(at, 2), label, {})


JS_POS = ("JSON.stringify([...document.querySelectorAll('.react-flow__node')].map(n=>{const r=n.getBoundingClientRect();return [n.textContent.slice(0,22),Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height)]}))")
JS_ARESTA = ("(()=>{const p=document.querySelectorAll('.react-flow__edge-path')[%d];if(!p)return 'SEM ARESTA';const L=p.getTotalLength();const q=p.getPointAtLength(L/2);const m=p.getScreenCTM();"
             "const x=q.x*m.a+q.y*m.c+m.e,y=q.x*m.b+q.y*m.d+m.f;const el=document.elementFromPoint(x,y);if(!el)return 'SEM ALVO';const o={bubbles:true,cancelable:true,composed:true,clientX:x,clientY:y,button:0,view:window};"
             "const pe=(t,b)=>new PointerEvent(t,{...o,pointerId:1,pointerType:'mouse',isPrimary:true,buttons:b});const me=(t,b)=>new MouseEvent(t,{...o,buttons:b,detail:1});"
             "el.dispatchEvent(pe('pointerdown',1));el.dispatchEvent(me('mousedown',1));el.dispatchEvent(pe('pointerup',0));el.dispatchEvent(me('mouseup',0));el.dispatchEvent(me('click',0));return [Math.round(x),Math.round(y)]})()")
JS_PONTO_ARESTA = ("(()=>{const p=document.querySelectorAll('.react-flow__edge-path')[%d];if(!p)return [10,10];const L=p.getTotalLength();const q=p.getPointAtLength(L/2);const m=p.getScreenCTM();return [q.x*m.a+q.y*m.c+m.e,q.x*m.b+q.y*m.d+m.f]})()")


CARTAO_FLUXO = SEL('button', hasText='Atendimento de chamado do portal')    # na lista de fluxogramas o cartão inteiro é o botão (sem "Abrir")


# Bug do app (1.38.21 e 1.38.24, achado na fase 2): ao ABRIR um organograma já salvo, o editor cria uma "Nova caixa" no centro e abre o painel
# dela (OrgChartFullscreen passa addBoxSignal=0 e o OrgChartCanvas chama addBox() na montagem, porque lastAddBoxSignal começa undefined).
# A semente apos-cap07 da fase 1 já guardou uma dessas caixas. Fora do vídeo, o setup a exclui pelo próprio app ("Excluir nó", sem confirmação).
APAGA_CAIXA_NOVA = [{'do': 'click', 'target': BTN('Excluir nó'), 'when': {'text': 'Texto da caixa'}, 'label': 'setup: exclui a "Nova caixa" criada ao abrir (bug)'},
                    AGUARDA, {'do': 'pause', 'seconds': 1.2}, {'do': 'waitFor', 'text': 'Salvo', 'timeout': 10}]
APAGA_CAIXA_DA_SEMENTE = [{'do': 'click', 'target': NO('Nova caixa'), 'when': {'selector': ".react-flow__node:has-text('Nova caixa')"}, 'label': 'setup: seleciona a "Nova caixa" da semente'},
                          {'do': 'pause', 'seconds': 0.5}] + APAGA_CAIXA_NOVA


def setup_quadro(aba, nome_card=None):
    """não filmado: abre a aba e o quadro salvo (botão Abrir do cartão), com o menu lateral recolhido; no organograma, exclui a caixa do bug"""
    s = setup_func(aba) + [{'do': 'click', 'target': CARTAO_FLUXO if aba == 'Fluxograma' else BTN('Abrir')}, AGUARDA, {'do': 'waitFor', 'text': 'Salvo', 'timeout': 20}, {'do': 'pause', 'seconds': 1.0}]
    if aba == 'Organograma':
        s += APAGA_CAIXA_NOVA
    return s


def cap06():
    """Montando a estrutura: Novo Organograma, caixa Direção (Camila), + embaixo (Tatiane), setor/cor, Rafael e os técnicos (4x), Aplicar aos de baixo, selo Salvo."""
    c = cap_novo(6, noscroll=True, setup=setup_func())
    c.mark(1)
    c.click(ABA('Organograma'), at=c.A(1, 'organograma.', 0.9), label='aba Organograma')
    c.waitfor(text='Nenhum organograma ainda', timeout=10)
    c.click(BTN('Novo Organograma'), at=c.A(1, 'Novo', 0.9), label='Novo Organograma')
    # fase 2 (ritmo): digitação a 18-20 letras/s (a 9 o nome levava 3,9 s e cada campo da Camila ~2 s); a marca L2 antes do Criar (o quadro leva
    # ~2 s para abrir e aparece no "a primeira caixa, a Direção"); clique direto na Direção (sem o hover); o setor Direção, que a fala não cita,
    # entra de uma vez (colar). O que ainda falta de tempo vai num respiro na voz entre a L2 e a L3 (pausas.py).
    c.type(SEL(f"{DLG} input"), 'Estrutura 2026', at=c.A(1, 'Estrutura', 1.3), label='nome Estrutura 2026', cps=18)
    c.mark(2)
    c.click(BTN('Criar', within=DLG), at=c.A(1, 'seis.', 0.3), label='Criar')
    c.waitfor(text='Salvo', timeout=20)
    c.click(NO('Direção'), at=c.A(2, 'Direção.', 0.6), label='abre Editar nó da Direção')
    c.waitfor(text='Editar nó', timeout=8)
    c.digitar_num(IN('Nome'), 'Camila Duarte', at=c.A(2, 'Camila,', 1.9), label='Nome: Camila Duarte', cps=20)
    c.digitar_num(IN('Cargo'), 'Diretora', at=c.A(2, 'diretora.', 1.0), label='Cargo: Diretora', cps=20)
    c.clicar_colar(IN('Setor'), 'Direção', label='Setor: Direção')
    c.mark(3)
    c.hover(NO('Camila Duarte'), 0.5, at=c.A(3, 'botão', 0.9), label='cursor na caixa da Camila')
    c.click(PLUS('Camila Duarte', 1), at=c.A(3, 'embaixo', 0.9), label='+ de baixo da caixa da Camila', force=True)
    c.waitfor(target=SEL(f"{DLG} input[placeholder='Buscar funcionário...']"), timeout=8)
    c.type(SEL(f"{DLG} input[placeholder='Buscar funcionário...']"), 'Tatiane', at=c.A(3, 'Escolho', 1.6), label='busca Tatiane', cps=18)
    c.click(SEL(f'{DLG} button', hasText='Tatiane Ribeiro'), at=c.A(3, 'lista', 0.9), label='escolhe Tatiane Ribeiro (entra ligada)')
    c.waitfor(target=NO('Tatiane Ribeiro'), timeout=8)
    c.mark(4)
    c.click(NO('Tatiane Ribeiro'), at=c.A(4, 'nome,', 0.9), label='abre Editar nó da Tatiane')
    c.waitfor(text='Nome, cargo e foto vêm do cadastro do funcionário.', timeout=8)
    c.hover(P_('Nome, cargo e foto vêm do cadastro do funcionário.'), 1.0, at=c.A(4, 'cadastro.', 0.9), label='dica: nome, cargo e foto vêm do cadastro')
    c.digitar_num(IN('Setor'), 'Escritório', at=c.A(4, 'setor,', 1.8), label='Setor: Escritório', cps=16)
    c.click(COR(1), at=c.A(4, 'cor.', 0.9), label='escolhe a cor do setor')
    c.confere('body', ['Escritório', 'Tatiane Ribeiro'], 'caixa da Tatiane com o setor Escritório')
    c.mark(5)
    c.hover(NO('Camila Duarte'), 0.3, at=c.A(5, 'campo,', 1.0), label='cursor na caixa da Camila')
    c.click(PLUS('Camila Duarte', 1), at=c.A(5, 'Rafael', 1.0), label='+ de baixo da Camila (Rafael)', force=True)
    c.type(SEL(f"{DLG} input[placeholder='Buscar funcionário...']"), 'Rafael', label='rápido (4x): busca Rafael', cps=30)
    c.click(SEL(f'{DLG} button', hasText='Rafael Lima'), label='rápido (4x): escolhe Rafael Lima')
    for nome, busca in [('Bruno Alves', 'Bruno'), ('Júlia Santos', 'Júlia'), ('Lucas Ferreira', 'Lucas'), ('Marina Costa', 'Marina'), ('Paulo Souza', 'Paulo')]:
        c.hover(NO('Rafael Lima'), 0.3, label=f'rápido (4x): cursor no Rafael ({nome})')
        c.click(PLUS('Rafael Lima', 1), label=f'rápido (4x): + de baixo do Rafael ({nome})', force=True)
        c.type(SEL(f"{DLG} input[placeholder='Buscar funcionário...']"), busca, label=f'rápido (4x): busca {busca}', cps=30)
        c.click(SEL(f'{DLG} button', hasText=nome), label=f'rápido (4x): escolhe {nome}')
        c.waitfor(target=NO(nome), timeout=8)
    c.mark(6)
    # fase 2 (ritmo): a caixa do Rafael abre no "Coloco" e o setor entra no "setor Campo" (antes: no "Rafael", e o Aplicar saía 1,6 s atrasado)
    c.click(NO('Rafael Lima'), at=c.A(6, 'Coloco', 0.9), label='abre Editar nó do Rafael')
    c.digitar_num(IN('Setor'), 'Campo', at=c.A(6, 'setor', 0.9), label='Setor: Campo', cps=16)
    c.click(COR(2), label='cor do setor Campo')
    c.click(BTN('Aplicar aos de baixo'), at=c.A(6, 'Aplicar', 0.9), label='Aplicar aos de baixo')
    c.pause(0.8)
    c.confere('body', ['Campo', 'Paulo Souza', 'Júlia Santos'], 'as caixas de baixo ficaram no setor Campo')
    c.mark(7)
    c.hover(SALVO, 1.4, at=c.A(7, 'selo:', 0.9), label='selo Salvo')
    c.pause(1.6)   # o quadro grava ~0,8 s depois da última mudança (a semente do capítulo sai logo depois do ensaio)
    c.fim()
    return c


def cap07():
    """Organizar e encontrar: Organizar, Adicionar caixa (Equipe Alfa), Tela cheia, Árvore, Destacar por setor, Buscar pessoa, Exportar (sem clicar)."""
    c = cap_novo(7, noscroll=True, setup=setup_quadro('Organograma'))
    c.mark(1)
    c.click(BTN('Organizar'), at=c.A(1, 'Organizar', 0.9), label='Organizar')
    c.pause(0.3)
    c.mark(2)
    clique_ponto(c, 900, 690, at=c.A(2, 'Adicionar', 2.2), label='clica no fundo do quadro (tira a seleção)')
    c.click(SEL("button[aria-label='Adicionar caixa']"), at=c.A(2, 'Adicionar', 0.6), label='Adicionar caixa')
    c.waitfor(text='Texto da caixa', timeout=8)
    # fase 2: o texto da anotação entra logo no "põe uma anotação" (a 24 letras/s; a 9, a digitação levava 5,5 s) e a caixa é levada para perto
    # do Bruno e do Lucas no "o Bruno e o Lucas formam a Equipe Alfa" (antes: hover + digitação no "Aqui" e arrasto 6 s atrasado)
    c.digitar_num(IN('Texto da caixa'), 'Equipe Alfa: Bruno e Lucas', at=c.A(2, 'caixa', 0.3), label='Texto da caixa: Equipe Alfa', cps=24)
    c.click(BTN('Fechar'), label='fecha o painel')
    c.drag(NO('Equipe Alfa'), {'x': 495, 'y': 610}, at=c.A(2, 'Equipe', 0.0), label='arrasta a caixa para perto do Bruno e do Lucas', hold=0.15, after=150)
    c.mark(3)
    # fala nova (1.38.21): "Na lateral ficam as ferramentas pra ler um organograma grande, e em Tela cheia o quadro ocupa a tela toda." -> o cursor
    # desce pelos ícones da lateral (Árvore, Destacar por setor, Buscar pessoa) e clica em Tela cheia no "Tela" (1º "tela" da linha)
    c.hover(SEL("button[aria-label='Árvore']"), 0.3, at=c.A(3, 'lateral', 0.9), label='ferramentas da lateral: Árvore')
    c.hover(SEL("button[aria-label='Destacar por setor']"), 0.3, at=c.A(3, 'ferramentas', 0.6), label='ferramentas da lateral: Destacar por setor')
    c.hover(SEL("button[aria-label='Buscar pessoa']"), 0.3, at=c.A(3, 'ler', 0.6), label='ferramentas da lateral: Buscar pessoa')
    # fase 2: a Tela cheia do app é a Fullscreen API do navegador (document.documentElement.requestFullscreen) e o gravador a captura DEFORMADA
    # (a barra do quadro em ~2,5x e só o canto do quadro à vista: gravação de 06/11 00:09). Fica só o zoom no botão, como os PDFs (decisão 2), e
    # as ferramentas da L4 a L7 rodam no quadro normal
    c.hover(BTN('Tela cheia'), 1.0, at=c.A(3, 'Tela', 0.9), label='Tela cheia (só zoom, sem clicar)')
    c.mark(4)
    # fase 2 (ritmo): sem o hover antes do clique (a L3 já passou pelo ícone; partido pela marca L4, ele atrasava o clique 1 s)
    c.click(SEL("button[aria-label='Árvore']"), at=c.A(4, 'Árvore', 0.9), label='Árvore')
    c.waitfor(text='Hierarquia', timeout=8)
    c.confere('body', ['Hierarquia', 'Expandir tudo', 'Recolher tudo', 'pessoas'], 'painel Hierarquia')
    c.mark(5)
    # fase 2: o app deixa UMA ferramenta aberta e, ao trocar de ferramenta, fecha o painel anterior e limpa o destaque (OrgChartFullscreen:
    # setActiveTool + useEffect que zera o spotlight). Sem "fecha a Árvore", "Limpar destaque" e "fecha o Destacar": a Hierarquia fica à vista
    # durante toda a L4 (antes fechava 0,6 s depois de abrir) e o setor Campo aceso durante o "acende um setor só"
    c.click(SEL("button[aria-label='Destacar por setor']"), at=c.A(5, 'Destacar', 0.9), label='Destacar por setor')
    c.click(SEL(f'{DLG} button', hasText='Campo'), at=c.A(5, 'setor', 0.9), label='escolhe o setor Campo')
    c.mark(6)
    c.click(SEL("button[aria-label='Buscar pessoa']"), at=c.A(6, 'Buscar', 0.9), label='Buscar pessoa')
    c.type(SEL(f"{DLG} input[placeholder='Nome ou cargo...']"), 'Júlia', at=c.A(6, 'leva', 1.0), label='busca Júlia', cps=14)
    c.confere('dlg', ['Júlia Santos'], 'Buscar pessoa: resultado Júlia Santos')
    # fase 2 (ritmo): o Exportar é clicado ainda em Tela cheia (a barra do quadro continua à vista; sair da tela cheia custava ~0,6 s e o
    # Exportar esperava a animação, ~2 s); a marca L7 entra antes de fechar a Busca, no "Pra imprimir"
    c.mark(7)
    c.click(SEL("button[aria-label='Buscar pessoa']"), at=round(c.L(7) - 0.9, 2), label='fecha a Busca')
    c.click(BTN('Exportar'), at=c.A(7, 'Exportar', 0.9), label='Exportar')
    c.waitfor(text='Baixar imagem (PNG)', timeout=8)
    c.hover(P_('Baixar PDF'), 1.2, at=c.A(7, 'imagem', 0.9), label='Baixar imagem (PNG) e Baixar PDF (sem clicar)')
    c.press('Escape', at=c.A(7, 'PDF.', 0.3), label='fecha o menu sem escolher')
    c.pause(0.3)
    c.fim()
    return c


# posições (px CSS) das formas do fluxograma com o quadro reduzido a ~0,48 (4 cliques em "Zoom Out"); o painel "Editar etapa" cobre x < 436
SLOTS = {'Chamado aberto no portal': (530, 190), 'Triagem do chamado': (690, 190), 'Precisa de visita?': (845, 190), 'Agendar visita e técnico': (1000, 190),
         'Executar a visita': (1155, 190), 'Relatório de Serviço': (1155, 400), 'Orientar o cliente por telefone': (845, 400), 'Chamado encerrado': (1000, 590)}
LIGACOES = [('Chamado aberto', 'right', 'Triagem', 'left'), ('Triagem', 'right', 'Precisa', 'left'), ('Precisa', 'right', 'Agendar', 'left'),
            ('Agendar', 'right', 'Executar', 'left'), ('Executar', 'bottom', 'Relatório', 'top'), ('Relatório', 'left', 'Chamado encerrado', 'top'),
            ('Precisa', 'bottom', 'Orientar', 'top'), ('Orientar', 'right', 'Chamado encerrado', 'left')]


# tamanho (px CSS) de cada forma com o quadro a ~0,43; a alça de destino é calculada a partir do centro do lugar (a alça é pequena demais para o arrasto achar sozinha)
TAMANHO = {'Chamado aberto no portal': (104, 26), 'Triagem do chamado': (113, 66), 'Precisa de visita?': (83, 83), 'Agendar visita e técnico': (113, 66),
           'Executar a visita': (113, 66), 'Relatório de Serviço': (104, 49), 'Orientar o cliente por telefone': (113, 66), 'Chamado encerrado': (104, 26)}


def ponto_alca(parte, lado):
    nome = next(n for n in SLOTS if n.startswith(parte))
    x, y = SLOTS[nome]
    w, h = TAMANHO[nome]
    dx, dy = {'left': (-w / 2, 0), 'right': (w / 2, 0), 'top': (0, -h / 2), 'bottom': (0, h / 2)}[lado]
    return {'x': round(x + dx), 'y': round(y + dy)}


ROTULO_NO = lambda nome: SEL(f'.react-flow__node >> text="{nome}"')   # o texto da forma (agarrar por ele evita pegar uma alça de ligação na borda)


def nova_forma(c, forma, nome, at=None, label_pre='', **kw):
    """Adicionar forma > forma; nomeia pelo "Editar etapa" (que abre sozinho) e arrasta para o lugar"""
    c.click(BTN('Adicionar forma'), at=at, label=f'{label_pre}Adicionar forma ({forma})', **kw)
    c.click(FORMA(forma), label=f'{label_pre}escolhe {forma}')
    c.waitfor(text='Editar etapa', timeout=8)
    c.clicar_colar(IN('Nome da etapa'), nome, label=f'{label_pre}nome: {nome}')   # fase 2: trecho rápido (cortado na montagem): digitados a 9 letras/s, os 7 nomes levavam ~28 s


def arrasta_forma(c, nome, label_pre=''):
    x, y = SLOTS[nome]
    c.drag(ROTULO_NO(nome), {'x': x, 'y': y}, label=f'{label_pre}arrasta {nome} para o lugar')


def cap08():
    """Desenhando a rotina: Novo fluxograma, Início renomeado, quadro reduzido, Adicionar forma (lista), as 8 formas (4x), ligações por arrasto e rótulos Sim/Não."""
    c = cap_novo(8, noscroll=True, setup=setup_func())
    c.mark(1)
    c.click(ABA('Fluxograma'), at=c.A(1, 'fluxograma.', 0.9), label='aba Fluxograma')
    c.waitfor(text='Nenhum fluxograma ainda', timeout=10)
    c.click(BTN('Novo fluxograma'), at=c.A(1, 'Novo', 0.9), label='Novo fluxograma')
    # fase 2 (ritmo): o nome (32 letras, 4,8 s digitado) entra de uma vez no "dou o nome" e o quadro abre no "Ele já nasce com o Início";
    # o nome do Início é digitado a 20 letras/s no "escrevo o que dá a largada"
    c.clicar_colar(SEL(f"{DLG} input"), 'Atendimento de chamado do portal', at=c.A(1, 'dou', 0.9), label='nome do fluxograma')
    c.mark(2)   # fase 2: a marca antes do Criar (o quadro leva ~1 s para abrir e aparece no "Ele já nasce com o Início")
    c.click(BTN('Criar fluxograma', within=DLG), at=c.A(1, 'nome.', 0.4), label='Criar fluxograma')
    c.waitfor(target=NO('Início'), timeout=20)
    c.click(NO('Início'), at=c.A(2, 'Clico', 0.9), label='abre Editar etapa do Início')
    c.waitfor(text='Editar etapa', timeout=8)
    c.digitar_num(IN('Nome da etapa'), 'Chamado aberto no portal', at=c.A(2, 'escrevo', 0.9), label='Nome da etapa: Chamado aberto no portal', cps=20)
    c.click(BTN('Fechar'), label='fecha o painel (para alcançar o zoom)', optional=True)
    for k in range(2):   # os botões de zoom do quadro não respondem (comando de viewport no-op, centerViewport.ts); a roda do mouse sobre o quadro dá zoom (~0,66 por volta)
        c.rolar(300, label=f'rápido (4x): reduz o quadro com a roda ({k + 1}/2)', ponto=(900, 600), duration=0.3)
    c.drag(ROTULO_NO('Chamado aberto no portal'), {'x': SLOTS['Chamado aberto no portal'][0], 'y': SLOTS['Chamado aberto no portal'][1]}, label='arrasta o Início para o lugar')
    c.ev(JS_POS, label='diagnóstico: posições das formas')
    c.mark(3)
    c.click(BTN('Adicionar forma'), at=c.A(3, 'Adicionar', 0.9), label='Adicionar forma (lista)')
    c.waitfor(target=FORMA('Decisão'), timeout=8)
    c.confere('body', ['Início', 'Tarefa', 'Decisão', 'Subproc', 'Docum', 'Espera', 'Fim', 'Observa'], 'lista de formas')
    # fala nova (1.38.21): "No Adicionar forma ficam as formas do desenho: início, tarefa, decisão, subprocesso, documento, espera, fim e observação.
    # A Tarefa é uma etapa comum, e a Decisão é quando o caminho muda" -> o cursor passa por cada forma da lista enquanto ela é dita; depois pousa
    # na Tarefa e na Decisão da 2ª frase (nth=1: o 1º "tarefa"/"decisão" da linha é o da lista)
    for nome, pal in [('Início', 'início,'), ('Tarefa', 'tarefa,'), ('Decisão', 'decisão,'), ('Subproc', 'subprocesso,'), ('Docum', 'documento,'),
                      ('Espera', 'espera,'), ('Fim', 'fim'), ('Observa', 'observação.')]:
        c.hover(FORMA(nome), 0.2, at=c.A(3, pal, 0.6), label=f'formas do desenho: {nome}')
    c.hover(FORMA('Tarefa'), 1.2, at=c.A(3, 'Tarefa', 0.9, nth=1), label='forma Tarefa (lista)')
    c.hover(FORMA('Decisão'), 1.2, at=c.A(3, 'Decisão', 0.9, nth=1), label='forma Decisão (lista)')
    c.mark(4)
    c.click(FORMA('Tarefa'), at=c.A(3, 'não.', 0.3), label='escolhe Tarefa')
    c.waitfor(text='Editar etapa', timeout=8)
    c.clicar_colar(IN('Nome da etapa'), 'Triagem do chamado', label='rápido (4x): nome: Triagem do chamado')
    arrasta_forma(c, 'Triagem do chamado', 'rápido (4x): ')
    for forma, nome in [('Decisão', 'Precisa de visita?'), ('Tarefa', 'Agendar visita e técnico'), ('Tarefa', 'Executar a visita'), ('Documento', 'Relatório de Serviço'),
                        ('Tarefa', 'Orientar o cliente por telefone'), ('Fim', 'Chamado encerrado')]:
        nova_forma(c, forma, nome, label_pre='rápido (4x): ')
        arrasta_forma(c, nome, 'rápido (4x): ')
    c.ev(JS_POS, label='diagnóstico: posições das formas')
    c.mark(5)
    # PLANO B (decisão do Kaik, 05/11): o robô faz só a primeira ligação (Chamado aberto -> Triagem) no "As setas ligam uma etapa na próxima: é só
    # puxar da borda de uma forma até a outra"; no "E na decisão, cada saída ganha um rótulo, sim ou não" a montagem CORTA para o desenho já ligado
    # (8 ligações com Sim e Não: semente apos-cap08, a mesma que abre o cap09). Fase 2: as ligações que tocam a Decisão falham (as alças ficam sob o
    # texto da forma; na gravação de 06/11 00:12 a Triagem -> Decisão falhou duas vezes) e o arrasto que erra a alça MOVE a forma e bagunça o
    # desenho; o rótulo ia para a última ligação, que podia ser a errada (ensaio: "Sim" na Triagem -> Decisão).
    for i, (a, ha, b, hb) in enumerate(LIGACOES[:1]):
        de, para = HANDLE(a, ha, 'source'), HANDLE(b, hb, 'target')
        c.drag(de, para, at=c.A(5, 'puxar', 0.9) if i == 0 else None, label=f'liga {a} a {b}')
        # a repetição só roda se a ligação não pegou (ainda não há a (i+1)-ésima ligação no quadro): cada arrasto custa ~2,4 s
        c.drag(de, para, label=f'liga {a} a {b} (repete: se a primeira não pegou; o quadro ignora ligação repetida)',
               unless={'selector': '.react-flow__edge', 'nth': i})
    c.ev("document.querySelectorAll('.react-flow__edge').length", label='diagnóstico: número de ligações (1)')
    c.waitfor(text='Salvo', timeout=10)
    c.pause(1.0)
    c.fim()
    return c


RAIA = lambda nome: SEL('.react-flow__node-lane', hasText=nome)
RAIA_N = lambda k: SEL('.react-flow__node-lane', nth=k)


def cap09():
    """Raias e responsáveis: Adicionar raia (Escritório e Campo), etapas para dentro das raias, Editar etapa da triagem, Formatar, Organizar (zoom), selo Salvo."""
    c = cap_novo(9, noscroll=True, setup=setup_quadro('Fluxograma'))
    c.mark(1)
    c.click(BTN('Adicionar raia'), at=c.A(1, 'Adicionar', 0.9), label='Adicionar raia (1)')
    c.click(SEL('.react-flow__node-lane button', nth=0), label='nome da raia 1')
    c.type(SEL("input[placeholder='Nome da raia (setor ou responsável)']"), 'Escritório', noClick=True, label='raia: Escritório', cps=12)
    c.press('Enter', label='confirma a raia 1')
    c.click(BTN('Adicionar raia'), at=c.A(1, 'Escritório', 1.2), label='Adicionar raia (2)')
    c.click(SEL('.react-flow__node-lane button', nth=1), label='nome da raia 2')
    c.type(SEL("input[placeholder='Nome da raia (setor ou responsável)']"), 'Campo', noClick=True, label='raia: Campo', cps=12)
    c.press('Enter', label='confirma a raia 2')
    c.ev(JS_POS, label='diagnóstico: posições (raias e formas)')
    for nome, raia in [('Triagem do chamado', 'Escritório'), ('Agendar visita e técnico', 'Escritório'), ('Orientar o cliente por telefone', 'Escritório'),
                       ('Executar a visita', 'Campo'), ('Relatório de Serviço', 'Campo')]:
        c.drag(ROTULO_NO(nome), RAIA(raia), label=f'arrasta {nome} para a raia {raia}')
    c.click(BTN('Organizar'), label='Organizar (arruma as faixas e as etapas dentro delas)')
    c.pause(1.0)
    c.ev("JSON.stringify([...document.querySelectorAll('.react-flow__node')].map(n=>[n.textContent.slice(0,18),n.className.includes('lane')]))", label='diagnóstico: formas e raias')
    c.mark(2)
    c.click(NO('Triagem do chamado'), at=c.A(2, 'Na', 1.0), label='abre Editar etapa da triagem')
    c.waitfor(text='Editar etapa', timeout=8)
    # fala nova (1.38.21): "Na triagem, escrevo como fazer e escolho a Tatiane como responsável." (sem a duração). O "Como fazer" (70 letras)
    # digitado a 9 por segundo levava ~12 s e atrasava o Responsável: entra de uma vez (colar) no "escrevo"
    c.clicar_colar(IN('Como fazer', 'textarea'), 'Ler o chamado, conferir o equipamento e decidir se precisa de visita.', at=c.A(2, 'escrevo', 1.0), label='Como fazer da triagem')
    c.click(SEL(f'button[role=combobox]', hasText='Cargo ou setor'), at=c.A(2, 'escolho', 0.9), label='seletor Responsável')
    c.click({'role': 'option', 'name': 'Tatiane Ribeiro'}, label='escolhe Tatiane Ribeiro')
    c.confere_ausente('body', 'Duração', 'não existe o campo Duração em uma Tarefa')
    c.mark(3)
    c.click(BTN('Fechar'), label='fecha o painel', optional=True)
    # fala nova (1.38.21): "Com as etapas nas faixas, o Organizar refaz o arranjo da esquerda pra direita. Depois, o Formatar só alinha..." -> clica
    # no Organizar (o arranjo já é o automático, feito no fim da L1 para as caixas não se sobreporem) e depois no Formatar
    c.click(BTN('Organizar'), at=c.A(3, 'Organizar', 0.9), label='Organizar (refaz o arranjo da esquerda para a direita)')
    c.click(BTN('Formatar'), at=c.A(3, 'Formatar', 0.9), label='Formatar')
    c.mark(4)
    # fase 2: o cursor leva ~1,8 s até o selo (ele passa por "Salvando…" depois do Formatar): sai no "aqui"; sem semente nesta fase, a pausa final é curta
    c.hover(SALVO, 1.0, at=c.A(4, 'aqui', 0.9), label='selo Salvo')
    c.pause(0.3)
    c.fim()
    return c


def cap10():
    """Conferência e POP: Conferência do fluxograma, Sobre o processo (5 campos), Exportar (POP em PDF, sem clicar)."""
    c = cap_novo(10, noscroll=True, setup=setup_quadro('Fluxograma'))
    c.mark(1)
    # fala nova (1.38.21): "No ícone do escudo, a Conferência do fluxograma procura..." (o botão só tem o ícone): clique no "escudo"
    c.click(SEL("button[aria-label='Conferência do fluxograma']"), at=c.A(1, 'escudo,', 0.7), label='Conferência do fluxograma')
    c.waitfor(text='Nenhum problema encontrado', timeout=8)
    c.confere('body', ['Nenhum problema encontrado'], 'Conferência: Nenhum problema encontrado')
    c.hover(P_('Nenhum problema encontrado'), 1.2, at=c.A(1, 'Aqui', 0.9), label='Nenhum problema encontrado')
    c.press('Escape', label='fecha a conferência')
    c.mark(2)
    # fala nova (1.38.21): "No ícone da prancheta, o Sobre o processo guarda o objetivo, o que dispara o processo, o dono, a área e a frequência.
    # Aqui, escrevo a Tatiane como dona." -> clique na "prancheta"; os campos longos entram de uma vez (colar) na palavra de cada um; o Dono é
    # DIGITADO no "escrevo a Tatiane" (por isso Área e Frequência vêm antes dele). 129 letras a 9 por segundo não cabiam nos 9 s da fala.
    c.click(SEL("button[aria-label='Sobre o processo']"), at=c.A(2, 'prancheta,', 0.8), label='Sobre o processo')
    c.waitfor(text='Dono do processo', timeout=8)
    c.clicar_colar(IN('Objetivo', 'textarea'), 'Responder todo chamado do portal em até um dia útil', at=c.A(2, 'objetivo,', 1.0), label='Objetivo')
    c.clicar_colar(IN('Disparo'), 'Cliente abre chamado no Portal do Cliente', at=c.A(2, 'dispara', 1.0), label='Disparo')
    c.ev("document.querySelector(\"label:is(:not(x))\")&&[...document.querySelectorAll('label')].find(l=>l.textContent.trim()==='Dono do processo').scrollIntoView({block:'center'})", label='rola o painel até Dono do processo')
    c.clicar_colar(IN('Área'), 'Atendimento', at=c.A(2, 'dono,', 0.9), label='Área')   # "a área e a frequência" cabem em 0,7 s: a Área sai no "o dono"
    c.clicar_colar(IN('Frequência'), 'Por demanda', at=c.A(2, 'frequência.', 1.0), label='Frequência')
    c.digitar_num(IN('Dono do processo'), 'Tatiane Ribeiro', at=c.A(2, 'escrevo', 1.2), label='Dono do processo', cps=20)
    c.press('Escape', label='fecha o painel', optional=True)
    c.mark(3)
    c.click(SEL("button[title='Exportar']"), at=c.A(3, 'POP,', 0.9), label='Exportar')
    c.waitfor(text='Baixar POP em PDF', timeout=8)
    c.hover(P_('Baixar POP em PDF'), 1.6, at=c.A(3, 'Baixar', 0.9), label='Baixar POP em PDF (sem clicar)')
    c.mark(4)
    c.press('Escape', at=c.A(4, 'manter', 0.9), label='fecha o menu sem escolher')
    c.pause(1.6)   # o quadro grava ~0,8 s depois da última mudança (a semente do capítulo sai logo depois do ensaio)
    c.fim()
    return c


def cap11():
    """Recapitulando: montagem pelas telas (perfil do Rafael, Interações com a comparação da dupla, Histórico do Bruno, organograma,
    fluxograma e Exportar)."""
    # setup (fora do vídeo): abre o organograma e exclui as caixas "Nova caixa" (a da semente da fase 1 e a que o app cria ao abrir); volta à lista
    limpa_org = ([{'do': 'click', 'target': ABA('Organograma')}, AGUARDA, {'do': 'pause', 'seconds': 0.6}, {'do': 'click', 'target': BTN('Abrir')}, AGUARDA,
                  {'do': 'waitFor', 'text': 'Salvo', 'timeout': 20}, {'do': 'pause', 'seconds': 1.0}] + APAGA_CAIXA_NOVA + APAGA_CAIXA_DA_SEMENTE +
                 [{'do': 'click', 'target': BTN('Voltar'), 'noScroll': True}, {'do': 'waitFor', 'text': 'Novo Organograma', 'timeout': 10}, AGUARDA,
                  {'do': 'pause', 'seconds': 1.5}])   # o editor sai com animação e só DEPOIS chama o onBack: um clique de aba antes disso volta para Funcionários
    # 06/11 (coordenador): as gravações das 00:30 e 00:46 abriram em Funcionários. Causa (pages/Employees.tsx, 1.38.24): o Voltar do editor
    # deixa a rota /funcionarios/organograma; trocar de aba a partir dela faz navigate('/funcionarios'), a página remonta e a aba volta para a
    # lista. O mesmo motivo do segundo clique em Fluxograma no roteiro. No setup não há `when`/`unless`: passar pela aba Funcionários (a
    # navegação acontece aqui) e só então abrir o Perfil Comportamental, já na rota /funcionarios, onde a troca de aba não navega.
    c = cap_novo(11, setup=SETUP_FUNC + limpa_org + [
        {'do': 'click', 'target': ABA('Funcionários')}, AGUARDA, {'do': 'waitFor', 'text': 'Selecione um funcionário', 'timeout': 10},
        {'do': 'pause', 'seconds': 1.0},
        {'do': 'click', 'target': ABA('Perfil Comportamental')}, AGUARDA, {'do': 'waitFor', 'text': 'Ver detalhes', 'timeout': 10},
        {'do': 'pause', 'seconds': 0.6}])
    c.mark(1)
    abre_ficha(c, 'Rafael Lima', at=c.A(1, 'perfil', 0.9), label='ficha do Rafael')
    estaciona(c, at=c.A(1, 'qualidades,', 0.5))
    c.mark(2)
    # fase 2 (ritmo): a fase 1 passava por Interações, Voltar, aba, Comparar com os dois seletores e de novo Voltar e ficha do Bruno (13 cliques,
    # ~11 s) numa fala de 6 s. Agora: Interações com o Bruno (os dois perfis e o "Ver comparação" no alto), a ficha do Bruno pela lista da
    # esquerda e o Histórico dele
    c.click(SUBABA('Interações'), at=c.A(2, 'Depois', 0.6), label='Interações')
    c.click(SEL('button[role=combobox]', hasText='Selecione um funcionário'), label='seletor')
    c.click(OPCAO('Bruno Alves'), label='escolhe Bruno')
    c.waitfor(text='Atritos', timeout=10)
    c.hover(BTN('Ver comparação'), 0.6, at=c.A(2, 'comparação', 0.9), label='a comparação da dupla (Ver comparação)')
    c.click({'text': 'Bruno Alves', 'exact': True, 'within': 'main div.overscroll-contain'}, at=c.A(2, 'evolução', 0.9), label='ficha do Bruno (lista da esquerda)')
    c.waitfor(text='Visão geral', timeout=10)
    c.click(SUBABA('Histórico'), label='Histórico')
    c.waitfor(text='Evolução do perfil', timeout=10)
    c.mark(3)
    c.click(BTN('Voltar'), at=c.A(3, 'No', 1.0), label='Voltar (sair da ficha)')
    c.waitfor(text='Novo Funcionário', timeout=10)
    c.click(ABA('Organograma'), at=c.A(3, 'organograma,', 0.5), label='aba Organograma')
    c.click(BTN('Abrir'), label='abre a Estrutura 2026')
    c.waitfor(text='Salvo', timeout=15)
    # o app cria uma "Nova caixa" ao abrir (bug): o robô a exclui logo (~1 s; dá para cortar na montagem). Sem Tela cheia (sai deformada na gravação)
    # 06/11 (coordenador): "Excluir nó" fica na barra do quadro (fora da faixa do robô): sem noScroll o clique levou 5,6 s e atrasou a L4 em 4,8 s
    c.click(BTN('Excluir nó'), label='exclui a "Nova caixa" que o app cria ao abrir (bug)', when={'text': 'Texto da caixa'}, noScroll=True)
    c.hover(SEL("button[aria-label='Buscar pessoa']"), 0.8, at=c.A(3, 'encontrar', 0.9), label='ferramenta Buscar pessoa ("como encontrar cada pessoa")')
    c.mark(4)
    # barra do quadro em y ~30, fora da faixa 96..H-70 do robô: noScroll (sem ele cada clique tentava rolar ~6 s)
    c.click(BTN('Voltar'), at=c.A(4, 'fluxograma,', 1.2), label='volta à lista', noScroll=True)
    c.waitfor(text='Novo Organograma', timeout=10)
    c.click(ABA('Fluxograma'), label='aba Fluxograma')
    c.pause(0.8)
    c.click(ABA('Fluxograma'), label='aba Fluxograma (de novo, só se a primeira caiu em Funcionários)', unless={'text': 'Novo fluxograma'})
    c.waitfor(text='Novo fluxograma', timeout=10)
    c.click(CARTAO_FLUXO, label='abre o fluxograma')
    c.waitfor(text='Salvo', timeout=15)
    c.click(SEL("button[title='Exportar']"), at=c.A(4, 'POP.', 1.2), label='Exportar', noScroll=True)
    c.waitfor(text='Baixar POP em PDF', timeout=8)
    c.mark(5)
    c.press('Escape', at=round(c.L(5) + 0.3, 2), label='fecha o menu')   # fase 2: o menu fica à vista ~1,5 s (antes fechava em 0,1 s)
    c.fim()
    return c
CAPS = {n: globals()[f'cap{n:02d}'] for n in range(12) if f'cap{n:02d}' in globals()}

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
