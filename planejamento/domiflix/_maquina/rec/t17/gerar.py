#!/usr/bin/env python3
"""T17 · gera rec/t17/cap00..cap11.json (roteiros do robô) a partir da voz pronta (t17/narracao/capNN.json).

Dashboard, relatórios e exportações no COMPUTADOR (janela 1280x800), logada como Camila Duarte (admin, Glacial Cold Brasil), na Dominex 1.38.24.
FAKE_NOW 13/11/2026 16:30 (sexta) em todos os capítulos. A aula só lê e filtra: nenhum capítulo grava no banco (todos partem de `t17/inicio`).
Os `at` saem da palavra que anuncia cada passo (A(linha, palavra, folga)): o gesto "pousa" ~0,7 a 1 s depois do início do passo.
Rodar de qualquer pasta: `python3 -I rec/t17/gerar.py [NN ...]`. Depois: `node rec/record.mjs rec/t17/capNN.json --check`.
 - `confere*` LÊ a tela e compara com a fala (o `resumo.py` acusa DIFERENTE). `OBS` vigia aviso de erro, tela escura e faixa da trilha Domiflix.
"""
import json
import os
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TUT = os.path.normpath(os.path.join(HERE, '..', '..'))
NARR = os.path.join(TUT, 't17', 'narracao')
CAD = json.load(open(os.path.join(HERE, 'cadeia.json'), encoding='utf8'))
BASE = CAD['inicio']
STORAGE = {'dominex:portal-tickets-seen:d40f5787-1779-501f-900c-ddb2b90a36e5': '2031-01-01T00:00:00.000Z'}
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

NOMES = ['Abertura', 'Os números do topo', 'Equipe, caixa e evolução', 'Status, tipos e equipe', 'O que pede atenção', 'O período e a origem', 'Ordens de serviço e satisfação', 'Financeiro e estoque', 'Pessoas: o ponto', 'PDF, Excel e CSV', 'Exportar meus dados', 'Recapitulando']
# todos os capítulos partem do mesmo `t17/inicio` (já na cadeia): nenhum grava no banco


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
        s.prewarm = prewarm or ['/dashboard', '/configuracoes']
        s.phone, s.anonymous, s.storage = phone, anonymous, storage if storage is not None else STORAGE
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
        d = {
            'name': f't17-cap{s.n:02d}',
            'title': f'T17 · Cap. {s.n} · {NOMES[s.n]} (narração {str(round(s.dur, 1)).replace(".", ",")} s; marcas L1..L{len(s.linhas)} = início de cada linha do roteiro)',
            'seed': f't17-cap{s.n:02d}', 'pace': s.pace, 'cps': s.cps, 'tail': getattr(s, 'tail', 1.5),
            'start': {'x': s.start[0], 'y': s.start[1]},
            'seedExtra': list(BASE),
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




SALVAR = BTN('Salvar', within=DLG)


def escolhe(c, combo_txt, opcao, at, label, **kw):
    """abre o seletor da janela (pelo texto que ele mostra) e escolhe a opção"""
    return c.select(COMBO(combo_txt), opcao, at=at, label=label, **kw)




# ---------------------------------------------------------------- alvos próprios do T17 (Dashboard, relatórios e exportações)
TOAST = lambda t: SEL('.app-toast-viewport li', hasText=t)                  # o aviso (toast) que sobe no canto inferior direito
KPI = lambda t: SEL('main .rounded-2xl.cursor-pointer', hasText=t)          # um dos três cartões coloridos do topo
BLOCO = lambda t: SEL('main .rounded-2xl', hasText=t)                        # um bloco do Dashboard (o Card inteiro, para o zoom)
FILTRO = lambda t: SEL('main button', hasText=t)                             # o botão do filtro de período (mostra o período escolhido)
MENU_GRUPO = lambda g: BTN(g)                                                # grupo do menu lateral (Operacional, Gestão, Financeiro)
LINK_DASH = SEL('a[href="/dashboard"]')                                # com o menu recolhido (só ícones) o item Dashboard é só o ícone
ABA = lambda n: TAB(n)
JS_KPIS = 'document.getAnimations().filter(a=>a.currentTime<0).forEach(a=>{a.startTime=document.timeline.currentTime})'   # lição do T5, cap. 10
ROLA_DIALOGO = "(()=>{const d=document.querySelector('[role=dialog] .overflow-y-auto');if(!d)return 'sem rolagem';d.scrollTo({top:%s,behavior:'smooth'});return d.scrollHeight})()"
# o Exportar meus dados responde em milissegundos no backend falso e a barra "Exportando {sheet}... {rows} registros" nunca aparece:
# espera de 0,4 s por leitura (como o "Salvando…" do T1: latência de rede, nada na tela é desenhado por fora)
# fase 2 (06/11): 0,25 s por leitura (era 0,4: no ensaio a exportação levou 4,8 s e o aviso "Exportação concluída" passava do fim da fala)
LATENCIA_EXPORT = ("(()=>{const f=window.fetch.bind(window);window.fetch=async(...x)=>{const u=String(x[0]&&x[0].url||x[0]);"
                   "if(/\\/rest\\/v1\\/(customers|customer_contacts|service_orders|service_materials|financial_transactions|financial_accounts)/.test(u))"
                   "await new Promise(r=>setTimeout(r,250));return f(...x)};return 'ok'})()")


def js_abre_menu(sel, texto=None):
    """fase 2 (time-lapse do cap09): abre um menu Exportar (DropdownMenu do Radix) sem levar o cursor. O gatilho do Radix abre no
    `pointerdown` (um `click()` sintético não abre o menu)."""
    filtro = f'.filter(b=>b.textContent.trim()==={json.dumps(texto, ensure_ascii=False)})' if texto else ''
    return ("(()=>{const b=[...document.querySelectorAll(%s)]%s.find(x=>x.getClientRects().length);if(!b)return 'SEM BOTAO';"
            "b.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true,cancelable:true,button:0,buttons:1,pointerType:'mouse',isPrimary:true}));return 'ok'})()") % (json.dumps(sel), filtro)


def js_clica_aba(nome):
    """fase 2 (time-lapse do cap11): troca de aba sem cursor (as abas da tela são `role=tab` com onClick: o `click()` sintético vale)"""
    return ("(()=>{const t=[...document.querySelectorAll('[role=tab]')].find(x=>x.textContent.trim().startsWith(%s));if(!t)return 'SEM ABA';t.click();return 'ok'})()"
            % json.dumps(nome, ensure_ascii=False))


MENU_ABERTO = SEL('[role=menu]')   # o menu aberto (Excel, PDF, CSV): retângulo para o zoom da montagem


def registra(c, alvo, label, at=None):
    """fase 2: registra o retângulo de um alvo para a montagem (passo `type` sem clique e sem texto; o cursor não se mexe)"""
    d = {'do': 'type', 'target': alvo, 'text': '', 'noClick': True, 'label': label, 'timeout': 4}
    if at is not None:
        d['at'] = round(at, 2)
    return c.add(d)


def clicar_botao_fixo(c, sel, ponto, at, label, texto=None, ultimo=False, antes=0.9):
    """Botão fixo do app fora da faixa y 96..730 (rodapé do menu, "Aplicar" da folha de Filtros): o `click` do robô tentaria rolar em vão (2 a 6 s).
    Leva o cursor com `scroll by 0 point`, registra o rect com `type noClick` e clica por `eval`. Molde do `clicar_fixo` do T5.
    fase 2: `antes` = quanto o cursor parte antes do clique (o `type noClick` do "Configurações" do rodapé levou 0,57 s no ensaio)."""
    c._p({'do': 'scroll', 'point': {'x': ponto[0], 'y': ponto[1]}, 'by': 0, 'duration': 0.3, 'after': 0}, round(max(0.0, at - antes), 2), label + ' (cursor)', {})
    alvo = {'selector': sel, **({'hasText': texto} if texto else {}), **({'nth': 'last'} if ultimo else {})}
    c.add({'do': 'type', 'target': alvo, 'text': '', 'noClick': True, 'label': label})
    filtro = f'.filter(b=>/{texto}/i.test(b.textContent))' if texto else ''
    js = f'[...document.querySelectorAll({json.dumps(sel)})]{filtro}.{"pop()" if ultimo else "shift()"}.click()'
    return c._p({'do': 'eval', 'js': js}, round(at, 2), label + ' (clique)', {})


# time-lapse do recap: "Limpar seleção" e marca os três grupos da aula (sem cursor); o padrão da janela leva quase tudo e o arquivo leria tabelas que a aula não semeia
JS_TRES_GRUPOS = ("(()=>{const d=document.querySelector('[role=dialog]');const clica=t=>{const e=[...d.querySelectorAll('button,label')].find(x=>x.textContent.trim()===t);if(e)e.click();return !!e};"
                  "const a=clica('Limpar seleção');return new Promise(r=>setTimeout(()=>{const b=['Clientes','Ordens de Serviço','Financeiro'].map(clica);r(JSON.stringify([a,b]))},250))})()")


def js_grupo_e_link(grupo, filho):
    """time-lapse do menu: abre o grupo só se ainda estiver fechado e clica o item (sem cursor)"""
    return ("(()=>{const ln=()=>[...document.querySelectorAll('a')].find(a=>a.textContent.trim()===%s);"
            "if(!ln()){const b=[...document.querySelectorAll('button')].find(x=>x.textContent.trim()===%s);if(!b)return 'SEM GRUPO';b.click()}"
            "return new Promise(r=>setTimeout(()=>{const a=ln();if(!a)return r('SEM LINK');a.click();r('ok')},250))})()" % (json.dumps(filho), json.dumps(grupo)))


def setup_dash(recolher=True):
    """não filmado: Dashboard aberto em "Este mês"; nos capítulos do Dashboard o menu fica recolhido (só ícones): com o menu aberto o cartão
    Faturamento corta o valor ("R$ 2.300,...") na janela de 1280 px"""
    s = list(SETUP_DASH)
    if recolher:
        s += [{'do': 'click', 'target': MENU_LATERAL}, {'do': 'pause', 'seconds': 0.8}]
    s += [{'do': 'eval', 'js': JS_KPIS}, {'do': 'pause', 'seconds': 1.2}]
    return s


def setup_rota(rota, esperar, recolher=False):
    s = list(SETUP_DASH) + [{'do': 'goto', 'url': rota}, {'do': 'waitFor', 'text': esperar, 'timeout': 25}, AGUARDA]
    if recolher:
        s += [{'do': 'click', 'target': MENU_LATERAL}, {'do': 'pause', 'seconds': 0.8}]
    return s


def cap_novo(n, **kw):
    kw.setdefault('prewarm', ['/dashboard'])
    kw.setdefault('start', (760, 420))
    return Cap(n, pace=0.5, **kw)


PREWARM_TODOS = ['/dashboard', '/ordens-servico', '/financeiro/relatorios', '/estoque', '/funcionarios', '/financeiro/contas', '/financeiro/movimentacoes', '/configuracoes']
ONDE_FIM = 'Dashboard, relatórios e exportações'


# ================================================================ capítulos
def cap00():
    """Abertura: o Dashboard em "Este mês", a câmera desce devagar pelos três cartões e pelos blocos e volta ao topo (cartões discretos: edição)."""
    c = cap_novo(0, setup=setup_dash())
    c.mark(1)
    # fase 2: hovers mais curtos (saudação 1,4 -> 1,2 s; cartões 1,0 -> 0,7 s): a 1ª rolagem saía 0,5 s atrasada na prévia
    c.hover(P('Olá, Camila!'), 1.2, at=0.3, label='saudação: Olá, Camila e Boa tarde')
    c.confere('main', ['Olá, Camila!', 'Boa tarde. Veja como está o dia.', 'Este mês', 'OS Abertas', 'Taxa de Conclusão', 'Faturamento'], 'cabeçalho e os três cartões')
    c.hover(KPI('Faturamento'), 0.7, at=c.A(1, 'Dashboard,', 0.9), label='os três cartões do topo')
    c.rolar(330, at=c.A(1, 'encontrar', 0.4), label='desce até o mapa e o fluxo de caixa')
    c.rolar(330, at=c.A(1, 'levar', 0.6), label='desce até a evolução de OS')
    c.mark(2)
    c.hover(BLOCO('Evolução de OS'), 2.2, at=c.A(2, 'Ele', 0.9), label='bloco Evolução de OS')
    c.rolar(330, at=c.A(2, 'equipe,', 1.0), label='desce até a equipe')
    c.hover(BLOCO('Desempenho da Equipe'), 1.8, at=c.A(2, 'número', 0.8), label='bloco Desempenho da Equipe')
    c.mark(3)
    c.rolar(-1400, at=c.A(3, 'volta', 1.0), label='volta ao topo', duration=1.0)
    c.mark(4)
    c.hover(KPI('OS Abertas'), 1.2, at=c.A(4, 'números', 0.9), label='os números do topo')   # fase 2: 1,6 -> 1,2 s (o FIM saía 0,36 s atrasado)
    c.fim()
    return c


def cap01():
    """Os números do topo: OS Abertas, Taxa de Conclusão e Faturamento (seta de variação); clique em OS Abertas leva às Ordens de Serviço."""
    c = cap_novo(1, setup=setup_dash(), prewarm=['/dashboard', '/ordens-servico'])
    c.mark(1)
    c.confere('main', ['OS Abertas', 'pendentes', 'Taxa de Conclusão', 'concluídas este mês', 'Faturamento', 'no período selecionado'], 'os três cartões com os subtítulos')
    c.hover(KPI('OS Abertas'), 1.6, at=c.A(1, 'Abertas', 0.9), label='cartão OS Abertas (n pendentes)')
    c.mark(2)
    c.hover(KPI('Taxa de Conclusão'), 1.6, at=c.A(2, 'Conclusão', 0.9), label='cartão Taxa de Conclusão')
    c.mark(3)
    c.hover(KPI('Faturamento'), 2.4, at=c.A(3, 'Faturamento', 0.9), label='cartão Faturamento (no período selecionado)')
    c.ev("(()=>{const e=[...document.querySelectorAll('main .rounded-2xl.cursor-pointer')].find(x=>/Faturamento/i.test(x.textContent));return e?e.innerText.replace(/\\s+/g,' '):'sem cartão'})()", label='lê o cartão Faturamento (valor e seta)')
    c.hover(KPI('Faturamento'), 2.0, at=c.A(3, 'setinha,', 0.9), label='a setinha de variação do Faturamento')
    c.mark(4)
    c.hover(KPI('Faturamento'), 1.6, at=c.L(4) + 0.4, label='o Faturamento fica na tela')
    c.mark(5)
    c.click(KPI('OS Abertas'), at=c.A(5, 'Abertas', 0.9), label='clica no cartão OS Abertas')
    c.waitfor(text='Gerencie suas ordens de serviço', timeout=15)
    # fase 2: sem o waitFor idle (1,5 s no ensaio) e o clique de volta 1,4 s antes do fim da fala (era 0,2 s: o FIM saía 0,9 s atrasado;
    # com a lista de OS ainda desenhando, o clique levou 1,8 s até o gesto no ensaio 2)
    c.click(LINK_DASH, at=round(c.dur - 1.4, 2), label='volta ao Dashboard pelo menu', noScroll=True, optional=True)
    c.fim()
    return c


def cap02():
    """Equipe, caixa e evolução: Equipe em Campo (mapa vazio às 16:30, Abrir Mapa ao Vivo sem clicar), Fluxo de Caixa (resumo) e Evolução de OS em Diário."""
    c = cap_novo(2, setup=setup_dash())
    c.mark(1)
    c.confere('main', ['Equipe em Campo', 'Ao vivo', 'Nenhum técnico em campo agora', 'Abrir Mapa ao Vivo'], 'Equipe em Campo, mapa vazio e Abrir Mapa ao Vivo')
    c.hover(BLOCO('Equipe em Campo'), 2.6, at=c.A(1, 'Equipe', 0.9), label='bloco Equipe em Campo (mapa de Niterói)')
    c.hover(BTNX('Abrir Mapa ao Vivo'), 2.2, at=c.A(1, 'Abrir', 0.9), label='botão Abrir Mapa ao Vivo (sem clicar)')
    c.mark(2)
    c.hover(BLOCO('Equipe em Campo'), 2.4, at=c.L(2) + 0.3, label='o mapa fica na tela')
    c.mark(3)
    # fase 2: as rolagens começam NA marca (início da linha - 0,9 s); começando 0,3 s antes, a marca só entrava depois da rolagem (L3 0,76 s e L5 0,74 s atrasadas)
    c.rolar(330, at=round(c.L(3) - 0.9, 2), label='desce até o Fluxo de Caixa')
    c.confere('main', ['Fluxo de Caixa', 'Entradas', 'Saídas', 'Entradas:', 'Saídas:', 'Saldo:'], 'Fluxo de Caixa com entradas, saídas e saldo')
    c.hover(BLOCO('Fluxo de Caixa'), 1.8, at=c.A(3, 'Fluxo', 0.0), label='bloco Fluxo de Caixa')
    c.hover(TXT('Saldo:'), 0.8, at=c.A(3, 'saldo', 0.9), label='resumo: Entradas, Saídas e Saldo')   # fase 2: 1,6 -> 0,8 s (a marca L4 saía 1,0 s atrasada)
    c.mark(4)
    c.hover(TXT('Entradas:'), 2.2, at=c.A(4, 'faturamento', 0.9), label='resumo do Fluxo de Caixa (de novo)')
    c.mark(5)
    c.rolar(330, at=round(c.L(5) - 0.9, 2), label='desce até a Evolução de OS')
    c.hover(BLOCO('Evolução de OS'), 1.6, at=c.A(5, 'Evolução', 0.0), label='bloco Evolução de OS (Mensal)')
    c.click(BTN('Diário'), at=c.A(5, 'Diário,', 0.9), label='Diário')
    c.hover(BLOCO('Evolução de OS'), 1.6, at=c.A(5, 'ritmo', 0.9), label='Evolução de OS em Diário (Total e Concluídas)')   # fase 2: 2,0 -> 1,6 s (FIM)
    c.fim()
    return c


def cap03():
    """Status, tipos e equipe: OS por Status, OS por Tipo de Serviço (rosca) e Desempenho da Equipe (medalhas, nota, tempo médio; rodapé sem clicar)."""
    c = cap_novo(3, setup=setup_dash())
    c.mark(1)
    c.confere('main', ['OS por Status', 'Pendente', 'Agendada', 'A Caminho', 'Em Andamento', 'Concluída'], 'OS por Status com os status e as quantidades')
    c.hover(BLOCO('OS por Status'), 3.0, at=c.A(1, 'Status', 0.9), label='bloco OS por Status')
    c.mark(2)
    c.rolar(330, at=round(c.L(2) - 0.5, 2), label='desce até OS por Tipo de Serviço')
    c.confere('main', ['OS por Tipo de Serviço', 'total'], 'OS por Tipo de Serviço com o total no centro')
    c.hover(BLOCO('OS por Tipo de Serviço'), 3.0, at=c.A(2, 'Tipo', 0.9), label='bloco OS por Tipo de Serviço (rosca)')
    c.mark(3)
    # fase 2: rolagem NA marca e mais curta (0,8 -> 0,6 s): começando 0,5 s antes, a marca L3 só entrava depois dela (0,96 s atrasada)
    c.rolar(900, at=round(c.L(3) - 0.9, 2), label='desce até Desempenho da Equipe', duration=0.6)
    c.confere('main', ['Desempenho da Equipe', 'concluídas', 'médio', 'técnicos em campo', 'Ver relatório'], 'Desempenho da Equipe com concluídas, nota, tempo médio e rodapé')
    c.hover(BLOCO('Desempenho da Equipe'), 2.4, at=c.A(3, 'Desempenho', 0.0), label='bloco Desempenho da Equipe')
    c.hover(TXT('Ver relatório'), 1.4, at=c.A(3, 'check-in', 0.9), label='rodapé: técnicos em campo e Ver relatório (sem clicar)', optional=True)   # fase 2: 1,8 -> 1,4 s
    c.fim()
    return c


def cap04():
    """O que pede atenção: Requer Atenção (OS vencidas ainda abertas), Chamados abertos e o clique no chamado (abre a aba Chamados das OS)."""
    c = cap_novo(4, setup=setup_dash(), prewarm=['/dashboard', '/ordens-servico'])
    c.mark(1)
    c.rolar(990, at=0.2, label='desce até Requer Atenção e Chamados abertos', duration=0.8)
    c.confere('main', ['Requer Atenção', 'Atrasada', 'Chamados abertos', 'Mariana Lopes'], 'Requer Atenção com uma OS atrasada e o chamado da Mariana')
    c.hover(BLOCO('Requer Atenção'), 3.0, at=c.A(1, 'Requer', 0.9), label='bloco Requer Atenção')
    c.mark(2)
    c.hover(BLOCO('Chamados abertos'), 2.6, at=c.A(2, 'chamados', 0.9), label='Requer Atenção e Chamados abertos, sempre à vista')
    c.mark(3)
    c.hover(BLOCO('Chamados abertos'), 2.4, at=c.A(3, 'Chamados', 0.9), label='bloco Chamados abertos (chamado da Mariana Lopes)')
    c.mark(4)
    c.click(P('Chamado pelo portal'), at=c.A(4, 'chamado,', 1.0), label='clica no chamado')
    c.waitfor(text='OS #15', timeout=15)
    c.waitfor(idle=True)
    c.fim()
    return c


def cap05():
    """O período e a origem: filtro (Mês passado), Personalizado (calendário, Esc), volta ao Este mês, clique em Concluída (OS já no status) e em Faturamento (Visão Geral)."""
    c = cap_novo(5, setup=setup_dash(), prewarm=['/dashboard', '/ordens-servico', '/financeiro/relatorio'])
    c.mark(1)
    c.hover(FILTRO('Este mês'), 0.8, at=c.A(1, 'filtro', 0.9), label='filtro de período: Este mês')
    c.click(FILTRO('Este mês'), at=c.A(1, 'começa', 0.9), label='abre a lista de períodos')
    c.waitfor(text='Últimos 30 dias', timeout=8)
    c.confere('body', ['Todos os tempos', 'Hoje', 'Últimos 7 dias', 'Este mês', 'Mês passado', 'Últimos 30 dias', 'Este ano', 'Personalizado'], 'a lista dos oito períodos')
    c.click(TXT('Mês passado'), at=c.A(1, 'passado,', 0.9), label='escolhe Mês passado')
    c.waitfor(idle=True)
    c.hover(KPI('Faturamento'), 0.9, at=c.A(1, 'tela', 0.6), label='a tela inteira muda junto (Mês passado)')   # fase 2: 1,6 -> 0,9 s (a L2 inteira atrasava)
    c.mark(2)
    c.click(FILTRO('Mês passado'), at=round(c.L(2) - 0.8, 2), label='abre a lista de períodos de novo')
    c.click(TXT('Personalizado'), at=c.A(2, 'Personalizado,', 0.26), label='escolhe Personalizado')
    c.waitfor(text='Selecione o período', timeout=8)
    c.confere('body', ['Selecione o período', 'Início', 'Fim', 'Limpar', 'Aplicar'], 'Selecionar datas: calendário com Início e Fim')
    c.hover(P_('Selecione o período'), 1.1, at=c.A(2, 'datas', 0.9), label='calendário: Início e Fim')   # fase 2: 1,6 -> 1,1 s (o Esc saía 0,94 s atrasado)
    c.press('Escape', at=c.A(2, 'fim.', 0.3), label='fecha o calendário sem aplicar (Esc)')
    c.click(FILTRO('Personalizado'), at=c.A(2, 'Eu', 0.5), label='abre a lista de períodos (Personalizado)')
    # fase 2: `noScroll` (no ensaio o robô tentou rolar a página 4 vezes antes do clique: 2,0 s) e logo depois do "volto"
    c.click(TXT('Este mês'), at=round(c.W(2, 'volto') + 0.25, 2), label='volta ao Este mês', noScroll=True)
    c.waitfor(idle=True)
    c.mark(3)
    # fase 2 (gravação 1, 06:42): o clique em Concluída esperou 1,8 s parado (bloco ainda se ajustando depois da troca de período) e o hover
    # seguinte saiu 1,0 s atrasado. Agora o cursor vai antes ao bloco, no "Os blocos" (a espera cai aí, com folga), e o hover do "Mostrando"
    # fica no "lista" (absorve um clique lento).
    c.hover(BLOCO('OS por Status'), 0.6, at=c.A(3, 'blocos', 0.6), label='os blocos também levam pra origem (OS por Status)')
    c.click(SEL('main button', hasText='Concluída'), at=c.A(3, 'Concluída,', 1.0), label='clica em Concluída (OS por Status)')
    c.waitfor(text='Gerencie suas ordens de serviço', timeout=15)
    c.confere('main', ['Ordens de Serviço', 'Mostrando'], 'a lista de OS abre já filtrada (Mostrando n de N OS)')
    c.hover(P('Mostrando'), 0.7, at=c.A(3, 'lista', 0.0), label='a lista já abre nesse status (Mostrando n de N OS)')
    # fase 2: a marca L4 vem ANTES da volta ao Dashboard (a L4 começa colada no fim da L3: sem vão para a volta); clique no "nesse status"
    c.mark(4)
    c.click(LINK_DASH, at=round(c.L(4) - 0.9, 2), label='volta ao Dashboard', noScroll=True)
    c.waitfor(text='Olá, Camila!', timeout=15)
    # fase 2 (gravação 1): com o cursor parado no ícone, o menu recolhido abre por hover (components/layout/Sidebar.tsx: abre no mouseenter e
    # fecha 500 ms depois do mouseleave), estreita os cartões e o Faturamento chegou cortado ("R$ 2.29...") até o cursor sair, ~3 s depois.
    # O cursor sai do menu logo depois da volta (para o vão entre a saudação e o filtro de período) e o menu recolhe antes de a contagem terminar.
    c._p({'do': 'scroll', 'point': {'x': 1000, 'y': 75}, 'by': 0, 'duration': 0.2, 'after': 0}, None, 'cursor sai do menu (o menu recolhe)', {})
    c.ev(JS_KPIS, label='cartões do Dashboard (animação)')   # fase 2: como no setup (no ensaio o clique no Faturamento esperou 1,7 s parado)
    c.click(KPI('Faturamento'), at=c.A(4, 'leva', 0.4), label='clica no cartão Faturamento')
    c.waitfor(text='Saldo do período', timeout=15)
    c.waitfor(idle=True)
    c.fim()
    return c


def cap06():
    """Ordens de serviço e satisfação: Operacional > Ordens de Serviço > aba Relatório (cartões, gráficos, tops, saúde do agendamento) e aba NPS e Satisfação."""
    c = cap_novo(6, setup=setup_dash(recolher=False), prewarm=['/dashboard', '/ordens-servico'])
    c.mark(1)
    c.click(MENU_GRUPO('Operacional'), at=0.2, label='abre o grupo Operacional')
    c.click(LINK('Ordens de Serviço'), at=c.A(1, 'relatório.', 0.9), label='menu: Ordens de Serviço')
    c.waitfor(text='Gerencie suas ordens de serviço', timeout=15)
    # fase 2: a aba vai no 2º "Relatório" da linha (nth=1; com o 1º, "relatório.", o `at` era 1,86 s e o passo saía 2,5 s atrasado); o 1º clique
    # na tela nova leva ~1,7 s até o gesto
    c.click(TAB('Relatório'), at=c.A(1, 'Relatório,', 1.7, nth=1), label='aba Relatório')
    c.waitfor(text='Taxa de conclusão', timeout=15)
    c.ev(JS_KPIS, label='cartões do relatório (animação)')
    c.confere('main', ['Total de OS', 'Taxa de conclusão', 'Tempo médio', 'Faturamento', 'Volume de OS ao Longo do Tempo', 'Faturamento ao Longo do Tempo', 'OS por Dia da Semana'], 'o Relatório de OS: quatro cartões e os gráficos')
    # fase 2: a cadeia de hovers com o custo medido (deslocamento 1,2 s no 1º, ~0,45 s nos outros) e `seconds` menores
    c.hover(TXT('Total de OS', within='main'), 0.3, at=c.A(1, 'total,', 1.0), label='KPI Total de OS')
    c.hover(TXT('Taxa de conclusão', within='main'), 0.4, at=c.A(1, 'taxa', 0.2), label='KPI Taxa de conclusão')
    c.hover(TXT('Tempo médio', within='main'), 0.4, at=c.A(1, 'tempo', 0.6), label='KPI Tempo médio')
    c.hover(TXT('Faturamento', within='main'), 0.4, at=c.A(1, 'faturamento', 0.6), label='KPI Faturamento')
    # fase 2: o gráfico fica abaixo da dobra: no ensaio o robô rolou sozinho 632 px dentro do hover (1,5 s). Agora a rolagem é um passo.
    c.rolar(632, at=c.A(1, 'evolução', 0.9), label='desce até o gráfico Volume de OS')
    c.hover(TXT('Volume de OS ao Longo do Tempo', within='main'), 0.3, at=c.A(1, 'evolução', -0.1), label='gráfico Volume de OS ao Longo do Tempo')
    c.mark(2)
    c.rolar(560, at=round(c.L(2) - 0.5, 2), label='desce até os rankings')
    c.confere('main', ['Top 10 Clientes', 'Top Técnicos (Concluídas)', 'Saúde do agendamento'], 'Top 10 Clientes, Top Técnicos e Saúde do agendamento')
    c.hover(TXT('Top 10 Clientes', within='main'), 0.6, at=c.A(2, 'clientes', 0.6), label='Top 10 Clientes')
    c.hover(TXT('Top Técnicos (Concluídas)', within='main'), 0.6, at=c.A(2, 'técnicos', 0.9), label='Top Técnicos (Concluídas)')
    c.hover(TXT('Saúde do agendamento', within='main'), 1.4, at=c.A(2, 'agendamento,', 0.9), label='Saúde do agendamento')
    c.mark(3)
    c.rolar(-3000, at=round(c.L(3) - 0.9, 2), label='volta ao topo', duration=0.8)   # fase 2: na marca (a L3 saía 0,87 s atrasada)
    c.click(TAB('NPS e Satisfação'), at=c.A(3, 'NPS', 0.9), label='aba NPS e Satisfação')
    c.waitfor(text='Média por Categoria', timeout=15)
    c.ev(JS_KPIS, label='cartões do NPS (animação)')
    c.confere('main', ['NPS Score', 'Média Geral', 'Respostas', 'Taxa de Resposta', 'Distribuição NPS', 'Ranking de Técnicos', 'Feed de Feedbacks'], 'NPS e Satisfação: cartões, distribuição, ranking e feed')
    # fase 2: o fim da L3 ("a nota, a distribuição, o ranking dos técnicos e os comentários", ~4,4 s) com o custo medido: hovers curtos e duas
    # rolagens (no ensaio o Feed de Feedbacks fez o robô rolar sozinho 508 px dentro do hover e o FIM saía 2,7 s atrasado)
    c.hover(TXT('NPS Score', within='main', nth=0), 0.4, at=c.A(3, 'nota,', 0.9), label='KPI NPS Score')
    c.hover(TXT('Distribuição NPS', within='main'), 0.4, at=c.A(3, 'distribuição,', 0.5), label='Distribuição NPS')
    c.rolar(700, at=c.A(3, 'ranking', 0.75), label='desce até o ranking e os comentários')
    c.hover(TXT('Ranking de Técnicos', within='main'), 0.3, at=c.A(3, 'técnicos', 0.6), label='Ranking de Técnicos')
    c.rolar(508, at=c.A(3, 'técnicos', -0.05), label='desce até os comentários')
    c.hover(TXT('Feed de Feedbacks', within='main'), 0.5, at=c.A(3, 'comentários.', 0.0), label='Feed de Feedbacks')
    c.fim()
    return c


def cap07():
    """Financeiro e estoque: Financeiro > Relatórios (as cinco abas num passeio) e Gestão > Estoque (Posição de Estoque, Inventários, Relatório)."""
    c = cap_novo(7, setup=setup_dash(recolher=False), prewarm=['/dashboard', '/financeiro/relatorios', '/estoque'])
    c.mark(1)
    c.click(MENU_GRUPO('Financeiro'), at=0.2, label='abre o grupo Financeiro')
    c.click(LINK('Relatórios'), at=c.A(1, 'Relatórios,', 0.9, nth=1), label='menu: Relatórios')   # fase 2: nth=1 (o `at` saía do 1º "relatórios", 0,42 s)
    c.waitfor(text='Regime de Caixa', timeout=15)
    c.confere('main', ['Visão Geral', 'DRE - Resultado', 'DFC - Fluxo de Caixa', 'Contabilidade', 'Análise'], 'as cinco abas dos Relatórios')
    c.click(ABA('Visão Geral'), at=c.A(1, 'visão', 0.9), label='aba Visão Geral')
    c.click(ABA('DRE - Resultado'), at=c.A(1, 'dê', 0.9), label='aba DRE - Resultado')
    c.click(ABA('DFC - Fluxo de Caixa'), at=c.A(1, 'DFC,', 0.9), label='aba DFC - Fluxo de Caixa')
    c.click(ABA('Contabilidade'), at=c.A(1, 'pacote', 0.9), label='aba Contabilidade')
    c.click(ABA('Análise'), at=c.A(1, 'análise', 0.9), label='aba Análise')
    c.mark(2)
    c.click(ABA('DRE - Resultado'), at=round(c.L(2) + 0.2, 2), label='aba DRE - Resultado (zoom)')
    c.waitfor(text='Demonstrativo de Resultado', timeout=15)
    c.hover(ABA('DRE - Resultado'), 2.2, at=c.A(2, 'tutorial', 0.6), label='a leitura do DRE está no tutorial de Relatório Financeiro e DRE')   # fase 2: 3,0 -> 2,2 s
    c.mark(3)
    # fase 2: Gestão na marca e Estoque logo depois (cada clique no menu custa ~1 s; a L3 saía 0,5 s, Estoque 0,95 s e Posição 1,2 s atrasados)
    c.click(MENU_GRUPO('Gestão'), at=round(c.L(3) - 0.9, 2), label='abre o grupo Gestão')
    c.click(LINK('Estoque'), at=c.A(3, 'Estoque,', 0.15), label='menu: Estoque')
    c.waitfor(text='Controle de peças e materiais', timeout=15)
    c.click(ABA('Posição de Estoque'), at=round(c.W(3, 'Posição') + 0.4, 2), label='aba Posição de Estoque')
    c.waitfor(text='Valor em estoque', timeout=15)
    c.click(ABA('Inventários'), at=c.A(3, 'Inventários', 0.9), label='aba Inventários')
    # fase 2: a aba Relatório fica fora da faixa de abas visível e o robô rola a faixa (~1,4 s) antes do clique (2,2 s até o gesto no ensaio)
    c.click(ABA('Relatório'), at=c.A(3, 'Relatório', 2.1), label='aba Relatório (Compras)')
    c.waitfor(text='Relatório de estoque por material', timeout=15)
    c.fim()
    return c


def cap08():
    """Pessoas: o ponto: Gestão > Funcionários (RH) > Controle de Ponto > Histórico (jornadas, botão CSV sem baixar) e Relatório (calendário)."""
    c = cap_novo(8, setup=setup_dash(recolher=False), prewarm=['/dashboard', '/funcionarios'])
    c.mark(1)
    c.click(MENU_GRUPO('Gestão'), at=0.2, label='abre o grupo Gestão')
    # fase 2: `at` com o custo medido dos cliques (o 1º clique numa tela nova leva 1,0 a 1,3 s até o gesto; Histórico saía 0,52 s atrasado)
    c.click(LINK('Funcionários (RH)'), at=c.A(1, 'Funcionários,', 0.79), label='menu: Funcionários (RH)')
    c.waitfor(text='Gerencie funcionários', timeout=15)
    c.click(TAB('Controle de Ponto'), at=c.A(1, 'Controle', 0.34), label='aba Controle de Ponto')
    c.waitfor(text='Presentes', timeout=15)
    c.click(TAB('Histórico'), at=c.A(1, 'Histórico', 0.36), label='aba Histórico')
    c.waitfor(text='registros', timeout=10)
    c.confere('main', ['registros', 'Tatiane Ribeiro', 'Filtros', 'CSV', 'Entrada', 'Saída', 'Trabalhado', 'Saldo'], 'Histórico do ponto: jornadas, colunas e botão CSV')
    c.hover(BTN('CSV'), 2.2, at=c.A(1, 'CSV', 0.9), label='botão CSV (sem baixar)')
    c.mark(2)
    c.click(TAB('Relatório'), at=c.A(2, 'Relatório', 0.9), label='aba Relatório')
    c.waitfor(text='Calendário', timeout=10)
    c.confere('main', ['Calendário', 'Horas por dia'], 'Relatório do ponto: calendário e horas por dia')
    c.hover(P('Calendário'), 0.6, at=c.A(2, 'calendário,', 0.9), label='Calendário do mês')   # fase 2: 1,2 -> 0,6 s
    # o resumo com as horas e o saldo só aparece com UM funcionário escolhido (a visão geral só tem o calendário e as horas por dia)
    # fase 2: Filtros, Tatiane e Esc em fila, com o custo medido (o 1º clique na folha leva 1,2 s até o gesto; Esc saía 1,0 s e o resumo 1,5 s atrasados)
    c.click(BTNX('Filtros'), at=c.A(2, 'horas', 0.88), label='Filtros do relatório')
    c.click({'text': 'Tatiane Ribeiro', 'within': DLG}, at=c.A(2, 'saldo.', 0.74), label='escolhe a Tatiane')
    c.press('Escape', at=round(c.W(2, 'saldo.') + 0.71, 2), label='fecha os filtros')
    c.waitfor(text='Saldo do mês', timeout=10)
    c.confere('main', ['Relatório de Tatiane Ribeiro', 'Dias trabalhados', 'Total trabalhado', 'Saldo do mês'], 'com a Tatiane escolhida aparece o resumo com as horas e o saldo do mês')
    c.hover(P('Saldo do mês'), 1.6, at=round(c.W(2, 'ponto') + 0.45, 2), label='resumo: horas e saldo do mês')
    c.fim()
    return c


def cap09():
    """PDF, Excel e CSV: Contas a Pagar/Receber (A Receber, Filtros > Status > Pendentes, menu Exportar sem escolher) e os cortes rápidos nas Movimentações, no DRE e no Estoque."""
    c = cap_novo(9, setup=setup_dash(recolher=False), prewarm=PREWARM_TODOS)
    c.mark(1)
    c.click(MENU_GRUPO('Financeiro'), at=0.2, label='abre o grupo Financeiro')
    c.click(LINK('Contas a Pagar/Receber'), at=c.A(1, 'Contas', 0.9), label='menu: Contas a Pagar/Receber')
    c.waitfor(text='Contas a pagar e a receber', timeout=15)
    c.click(TAB('A Receber'), at=c.A(1, 'aba', 0.9), label='aba A Receber')
    c.click(BTNX('Filtros'), at=c.A(1, 'filtro', 0.9), label='Filtros')
    c.waitfor(text='Vazio = todas as categorias', timeout=8)
    # fase 2: respiro de 2,0 s na voz entre a L1 e a L2 (t17/narracao: `pausas.py 09 8.40:2.0`): Status, Pendentes, Aplicar e a folha fechando
    # levam ~3,4 s e a fala só deixava ~1,8 s (Exportar saía 1,5 s atrasado). Os `at` seguem o custo medido no ensaio.
    c.click(SEL(f'{DLG} button[role=combobox]', nth=0), at=round(c.W(1, 'filtro') + 0.2, 2), label='Status')
    c.click(OPT('Pendentes'), at=round(c.W(1, 'pendentes.') + 0.36, 2), label='Pendentes')
    c.mark(2)
    clicar_botao_fixo(c, f'{DLG} button', (1056, 768), at=round(c.L(2) - 1.3, 2), label='Aplicar o filtro', texto='Aplicar')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.click(BTN('Exportar'), at=c.A(2, 'Exportar', 0.9), label='Exportar')
    c.waitfor(text='CSV', timeout=6)
    c.hover(ITEM('PDF'), 2.2, at=c.A(2, 'Excel,', 0.9), label='Exportar: Excel, PDF e CSV (sem escolher)')
    c.mark(3)
    c.hover(ITEM('PDF'), 3.0, at=c.A(3, 'filtros', 0.9), label='o arquivo sai com o que está na tela')
    c.mark(4)
    c.press('Escape', at=round(c.L(4) - 0.3, 2), label='fecha o menu sem escolher')
    # cortes rápidos (time-lapse): cada tela com o menu Exportar aberto e fechado, sem escolher; navegação interna do app (SPA), sem recarregar
    # fase 2: a fala dá ~1,2 s por tela ("movimentações", "DRE", "estoque"; voz contínua, sem vão para respiro) e um clique com cursor custa
    # ~1,9 s por tela (FIM 3,9 s atrasado na prévia). Movimentações com cursor; DRE e Estoque com o menu aberto sem cursor (`js_abre_menu`).
    # O retângulo de cada menu fica no actions.json ("menu das Movimentações", "menu do DRE", "menu do Estoque") para o zoom da montagem.
    c.add({'do': 'goto', 'url': '/financeiro/movimentacoes', 'at': round(c.L(4) + 0.3, 2), 'label': 'vai às Movimentações Financeiras'})
    c.waitfor(text='Movimentações Financeiras', timeout=15)
    c.click(BTN('Exportar'), at=c.A(4, 'movimentações,', 0.9), label='Exportar das Movimentações (PDF, Excel, CSV)')
    registra(c, MENU_ABERTO, 'menu das Movimentações')
    c.pause(0.3)
    c.press('Escape', label='fecha o menu')
    c.add({'do': 'goto', 'url': '/financeiro/relatorios?tab=dre', 'label': 'vai ao DRE'})
    c.waitfor(text='Demonstrativo de Resultado', timeout=15)
    c.ev(js_abre_menu('main button', 'Exportar'), at=c.A(4, 'érri', 0.3), label='Exportar do DRE (Excel, PDF)')
    registra(c, MENU_ABERTO, 'menu do DRE')
    c.pause(0.25)
    c.press('Escape', label='fecha o menu')
    c.add({'do': 'goto', 'url': '/estoque', 'label': 'vai ao Estoque'})
    c.waitfor(text='Controle de peças e materiais', timeout=15)
    c.ev(js_abre_menu('button[aria-label="Exportar estoque"]'), at=c.A(4, 'estoque.', 0.2), label='Exportar do Estoque (PDF, Excel)')
    registra(c, MENU_ABERTO, 'menu do Estoque')   # o menu do Estoque fica aberto até o fim do capítulo
    c.fim()
    return c


def cap10():
    """Exportar meus dados: Configurações (rodapé do menu) > Empresa, fim da página: Exportar dados > janela, Limpar seleção, Clientes, Ordens de Serviço e Financeiro, Funcionários desmarcado, Exportar."""
    c = cap_novo(10, setup=setup_dash(recolher=False), prewarm=['/dashboard', '/configuracoes'])
    c.mark(1)
    # fase 2: o cursor parte 1,4 s antes do clique (o registro do botão levou 0,57 s no ensaio e o clique saía 0,86 s atrasado)
    clicar_botao_fixo(c, 'button', (80, 770), at=1.4, label='Configurações, no rodapé do menu', texto='Configurações', antes=1.4)
    c.waitfor(text='Gerencie as configurações do sistema', timeout=20)
    c.waitfor(idle=True)
    c.ev("(()=>{const b=[...document.querySelectorAll('button')].find(x=>x.innerText.trim()==='Exportar dados');if(!b)return 'SEM BOTAO';b.scrollIntoView({block:'center',behavior:'smooth'});return 1})()", at=c.A(1, 'fim', 0.6), label='rola até o cartão Exportar meus dados')
    c.confere('main', ['Exportar meus dados', 'Baixe uma planilha do Excel com os dados da sua empresa', 'Exportar dados'], 'o cartão Exportar meus dados, no fim da aba Empresa')
    c.hover(P('Exportar meus dados'), 2.4, at=c.A(1, 'Ele', 0.9), label='cartão Exportar meus dados')
    c.mark(2)
    c.click(BTN('Exportar dados'), at=round(c.L(2) - 0.4, 2), label='Exportar dados')
    c.waitfor(text='Escolha o que deseja incluir na planilha', timeout=10)
    c.confere('dlg', ['Exportar meus dados', 'Escolha o que deseja incluir na planilha. O arquivo é gerado na hora e baixado automaticamente.', 'Clientes', 'Ordens de Serviço', 'Financeiro', 'Funcionários', 'Exportar'], 'a janela Exportar meus dados com os grupos')
    c.click(BTN('Limpar seleção'), at=c.A(2, 'grupos.', 0.6), label='Limpar seleção')
    c.click(TXT('Clientes', within=DLG), at=c.A(2, 'clientes,', 0.9), label='marca Clientes')
    c.click(TXT('Ordens de Serviço', within=DLG), at=c.A(2, 'ordens', 0.9), label='marca Ordens de Serviço')
    c.click(TXT('Financeiro', within=DLG), at=c.A(2, 'financeiro.', 0.9), label='marca Financeiro')
    c.mark(3)
    c.ev(ROLA_DIALOGO % 999, at=round(c.L(3) - 0.2, 2), label='rola a lista até Funcionários')
    c.hover(TXT('Funcionários', within=DLG), 2.8, at=c.A(3, 'empresa', 0.9), label='grupo Funcionários, desmarcado')
    c.ev("(()=>{const e=[...document.querySelectorAll('[role=dialog] [role=checkbox]')];return e.map(x=>x.getAttribute('aria-checked')).join(',')})()", label='lê as caixas da janela (só três marcadas)')
    c.mark(4)
    c.ev(LATENCIA_EXPORT, at=round(c.L(4) - 0.9, 2), label='latência de rede nas leituras do arquivo (a barra de progresso aparece)')
    c.click(BTN('Exportar', within=DLG), at=c.A(4, 'Exportar,', 0.6), label='Exportar')
    c.waitfor(target=TOAST('Exportação concluída'), timeout=25)
    # fase 2: 1,6 -> 1,2 s e a espera de rede menor (LATENCIA_EXPORT 0,25 s): o FIM saía 1,5 s atrasado
    c.hover(TOAST('Exportação concluída'), 1.2, label='aviso: Exportação concluída! O arquivo foi baixado.', optional=True, noScroll=True)
    c.tail = 3.0
    c.fim()
    return c


def cap11():
    """Recapitulando (time-lapse): cartões e blocos do Dashboard; Relatório de OS, NPS, Relatórios do Financeiro; menu Exportar e o aviso de conclusão."""
    c = cap_novo(11, setup=setup_dash(), prewarm=PREWARM_TODOS)
    c.mark(1)
    c.hover(KPI('OS Abertas'), 0.6, at=0.8, label='os três cartões do Dashboard')
    c.rolar(330, at=c.A(1, 'período', 0.9), label='desce pelos blocos')
    c.rolar(330, at=c.A(1, 'comanda', 0.2), label='desce pelos blocos (2)')   # fase 2: depois da 1ª rolagem (saía 0,64 s atrasada)
    c.rolar(520, at=c.A(1, 'origem', 1.6), label='desce até a equipe e os chamados')
    c.mark(2)
    c.add({'do': 'goto', 'url': '/ordens-servico', 'at': round(c.L(2) - 0.3, 2), 'label': 'vai às Ordens de Serviço'})
    c.click(TAB('Relatório'), at=c.A(2, 'ordens', 1.0), label='aba Relatório')
    c.ev(JS_KPIS, label='cartões do relatório (animação)')
    # fase 2: NPS sem cursor (`js_clica_aba`; o clique com cursor levou 1,5 s até o gesto) e as idas em fila com o custo medido (a do
    # Estoque leva ~1,4 s até a rede assentar)
    c.ev(js_clica_aba('NPS e Satisfação'), at=c.A(2, 'satisfação,', 0.2), label='aba NPS e Satisfação')
    c.waitfor(text='Média por Categoria', timeout=10)
    c.ev(JS_KPIS, label='cartões do NPS (animação)')
    c.add({'do': 'goto', 'url': '/financeiro/relatorios?tab=dre', 'at': c.A(2, 'financeiro,', 0.25), 'label': 'vai aos Relatórios do Financeiro'})
    c.add({'do': 'goto', 'url': '/estoque', 'at': c.A(2, 'estoque', 0.45), 'label': 'vai ao Estoque'})
    c.mark(3)
    c.add({'do': 'goto', 'url': '/funcionarios', 'at': round(c.W(2, 'ponto.') + 0.25, 2), 'label': 'vai a Funcionários'})
    c.add({'do': 'goto', 'url': '/financeiro/contas', 'at': round(c.L(3) + 0.05, 2), 'label': 'vai às Contas a Pagar/Receber'})
    c.click(BTN('Exportar'), at=c.A(3, 'Exportar', 0.65), label='menu Exportar')
    registra(c, MENU_ABERTO, 'menu Exportar aberto')
    c.pause(0.3)
    c.press('Escape', label='fecha o menu')
    c.add({'do': 'goto', 'url': '/configuracoes', 'at': c.A(3, 'meus', 1.0), 'label': 'vai às Configurações'})
    c.waitfor(text='Gerencie as configurações do sistema', timeout=20)
    c.ev("(()=>{const b=[...document.querySelectorAll('button')].find(x=>x.innerText.trim()==='Exportar dados');if(!b)return 'SEM BOTAO';b.click();return 1})()", label='abre o Exportar meus dados')
    c.waitfor(text='Escolha o que deseja incluir na planilha', timeout=10)
    c.ev(JS_TRES_GRUPOS, label='só Clientes, Ordens de Serviço e Financeiro (time-lapse)')
    c.click(BTN('Exportar', within=DLG), label='Exportar')
    # fase 2: respiro de 1,2 s na voz entre a L3 e a L4 (`pausas.py 11 22.10:1.2`): a exportação leva ~1,5 s e o aviso de conclusão cai no
    # respiro, antes do "Esse foi o último tutorial". A marca L4 entra logo depois do Exportar (antes ela vinha depois do aviso: 4,1 s atrasada).
    c.mark(4)
    c.flush(1e9)
    c.waitfor(target=TOAST('Exportação concluída'), timeout=25)
    c.hover(TOAST('Exportação concluída'), 1.2, label='aviso de conclusão', optional=True, noScroll=True)
    c.fim()
    return c


CAPS = {n: globals()[f'cap{n:02d}'] for n in range(12) if f'cap{n:02d}' in globals()}


def principal():
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


if __name__ == '__main__':
    principal()
