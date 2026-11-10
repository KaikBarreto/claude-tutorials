#!/usr/bin/env python3
"""T21 · gera rec/t21/cap00..cap10.json (roteiros do robô) a partir da voz pronta (t21/narracao/capNN.json).

Integração com WhatsApp no COMPUTADOR (janela 1280x800), logada como Camila Duarte (admin, Glacial Cold Brasil), na Dominex 1.38.24.
FAKE_NOW 12/11/2026 14:00 (caps 0 a 7 e 9) e 13/11/2026 15:00 (caps 8 e 10: o corte do dia seguinte). WhatsApp e celular SIMULADOS (nenhum número, QR ou conta real).
Os `at` saem da palavra que anuncia cada passo (A(linha, palavra, folga)): o gesto "pousa" ~0,7 a 1 s depois do início do passo.
Rodar de qualquer pasta: `python3 -I rec/t21/gerar.py [NN ...]`. Depois: `node rec/record.mjs rec/t21/capNN.json --check`.
Cadeia de sementes: rec/t21/cadeia.json (semear.py: fim do T22 + `t21/inicio`) e o último `t21/apos-capNN` do capítulo anterior que mexeu no banco (SEMENTE abaixo).
 - `confere*` LÊ a tela e compara com a fala (o `resumo.py` acusa DIFERENTE). `OBS` vigia aviso de erro, tela escura e faixa da trilha Domiflix.
 - A "leitura do QR" é um passo de bastidor: POST na função `whatsapp-bastidor-leitura-qr` do fake (rec/fakebase/handlers/functions/).
"""
import json
import os
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TUT = os.path.normpath(os.path.join(HERE, '..', '..'))
NARR = os.path.join(TUT, 't21', 'narracao')
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

NOMES = ['Abertura', 'O que a integração faz', 'Preparando o número', 'Lendo o QR Code', 'Horários de envio', 'Os avisos da OS', 'Os avisos de cobrança',
         'A autorização do cliente', 'Acompanhando os envios', 'Reconectar e desconectar', 'Recapitulando']
# estado de partida de cada capítulo: o último apos-capNN que mexeu no banco. cap03 conecta (apos-cap03, entrada do 4), cap04 salva os horários (apos-cap04, entrada do 5),
# cap05 liga as automações (apos-cap05, entrada do 6 e 7). Os caps 8 e 10 somam o corte do dia 13 (CORTE); os demais só leem.
SEMENTE = {0: None, 1: None, 2: None, 3: None, 4: 'apos-cap03', 5: 'apos-cap04', 6: 'apos-cap05', 7: 'apos-cap05', 8: 'apos-cap05', 9: 'apos-cap05', 10: 'apos-cap05'}
CORTE = 't21/corte-dia13'
CAPS_DIA13 = (8, 10)


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
        sem = SEMENTE[s.n]
        d = {
            'name': f't21-cap{s.n:02d}',
            'title': f'T21 · Cap. {s.n} · {NOMES[s.n]} (narração {str(round(s.dur, 1)).replace(".", ",")} s; marcas L1..L{len(s.linhas)} = início de cada linha do roteiro)',
            'seed': f't21-cap{s.n:02d}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
            'start': {'x': s.start[0], 'y': s.start[1]},
            'seedExtra': list(BASE) + ([f't21/{sem}'] if sem else []) + ([CORTE] if s.n in CAPS_DIA13 else []),
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


# ---------------------------------------------------------------- alvos próprios do T21 (Integração com WhatsApp)
WA_URL = '/configuracoes?tab=integracoes&integration=whatsapp'

TABX = lambda n, **kw: {'role': 'tab', 'name': n, **kw}                      # os botões das seções levam o cadeado no nome: busca por substring
SUBABA_WA = SEL('[role=tab]', hasText='WhatsApp')                              # subaba WhatsApp (o nome acessível do botão não casa por papel+nome)
RADIO = lambda n, **kw: {'role': 'radio', 'name': n, **kw}                    # "Ordens de serviço" | "Cobranças" (controle segmentado)
CHECK = SEL('main button[role=checkbox]')                                     # caixa do aceite (a única da tela de Conexão)
SELO = lambda t: SEL('main span, main div', hasText=t)
EVENTO = lambda nome: BTNX(nome)                                              # linha da lista "Escolha quando enviar"
LISTA_OS = SEL('main div.rounded-lg.border.overflow-hidden')                  # a lista de momentos (quatro linhas)
JANELA_OS = SEL('main h4', hasText='Avisos de serviço')
JANELA_COB = SEL('main h4', hasText='Lembretes de cobrança')
BASTIDOR_LEITURA = ("fetch(%s,{method:'POST',headers:{'content-type':'application/json'},body:'{}'}).then(r=>r.text())"
                    % json.dumps(os.environ.get('FAKE_URL', 'http://127.0.0.1:54340') + '/functions/v1/whatsapp-bastidor-leitura-qr'))
ROLA_CARTAO = "(()=>{const e=document.querySelector('#whatsapp-automation-master');if(!e)return 'sem cartão';e.scrollIntoView({block:'center'});return 'ok'})()"


def js_main_ate(texto, y=250, dur_ms=900):
    """(fase 2, molde do rec/t22/_caps.py) rolagem suave até a folha do DOM cujo texto é `texto` (dentro do <main>) ficar em y px CSS; o
    cursor não se mexe. Rola o CONTÊINER QUE ROLA de verdade (o ancestral mais próximo com overflow auto/scroll e conteúdo maior que a
    caixa; o 1º <main> do documento é o SidebarInset, que não rola). O eval só termina depois da rolagem (`dur_ms`).
    Devolve 'topo N' (topo final do alvo, deve sair perto de `y`), 'ok' (já estava lá) ou 'SEM ALVO'."""
    busca = "[...m.querySelectorAll('*')].find(e=>e.children.length===0&&e.textContent.trim()===%s)" % json.dumps(texto)
    return ("(async()=>{const m=document.querySelector('main');const el=" + busca + ";"
            "if(!el)return 'SEM ALVO';const sc=(()=>{for(let p=el.parentElement;p;p=p.parentElement){const s=getComputedStyle(p);"
            "if(/(auto|scroll)/.test(s.overflowY)&&p.scrollHeight>p.clientHeight+4)return p}return document.scrollingElement})();"
            "const dy=Math.round(el.getBoundingClientRect().top-%d);if(Math.abs(dy)<3)return 'ok';const y0=sc.scrollTop,t0=performance.now();"
            "await new Promise(res=>{const f=t=>{const p=Math.min(1,(t-t0)/%d),e=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;sc.scrollTo({top:y0+dy*e,behavior:'instant'});"
            "p<1?requestAnimationFrame(f):res()};requestAnimationFrame(f)});return 'topo '+Math.round(el.getBoundingClientRect().top)})()") % (y, dur_ms)


def rola_ate(c, texto, at, label, y=250, dur_ms=900):
    return c.ev(js_main_ate(texto, y, dur_ms), at=at, label=label)


def setup_wa(espera, aceite=False, rolar_ate_cartao=False):
    """não filmado: Configurações > Integrações > WhatsApp já aberta (a URL abre direto na subaba); `espera` = texto que mostra que a tela carregou"""
    s = SETUP_DASH + [{'do': 'goto', 'url': WA_URL}, {'do': 'waitFor', 'text': espera, 'timeout': 25}, AGUARDA, {'do': 'pause', 'seconds': 0.6}]
    if aceite:   # a caixa do aceite é só estado da tela (não grava nada): o capítulo 3 a marca de novo fora do vídeo
        s += [{'do': 'click', 'target': CHECK}, {'do': 'pause', 'seconds': 0.4}]
    if rolar_ate_cartao:
        s += [{'do': 'eval', 'js': ROLA_CARTAO}, {'do': 'pause', 'seconds': 0.6}]
    return s


def cap_novo(n, **kw):
    kw.setdefault('prewarm', ['/dashboard', '/configuracoes'])
    kw.setdefault('start', (760, 420))
    return Cap(n, pace=0.5, **kw)


# ================================================================ capítulos
def cap00():
    """Abertura: Dashboard > Configurações (rodapé do menu) > Integrações > WhatsApp: o cartão "Conexão com o WhatsApp" (selo Desconectado)."""
    c = cap_novo(0, setup=SETUP_DASH)
    c.mark(1)
    # fase 2 (06/11): sem o hover em "Agenda" (custava 1,6 s e a subaba atrasava 1,5 s na prévia); o cursor vai direto ao rodapé e os
    # dois primeiros cliques têm `at` fixo, já com o custo deles (docs/08-licoes.md, T12)
    c.click(BTN('Configurações'), at=0.6, label='Configurações, no rodapé do menu', noScroll=True)   # o botão fica no rodapé fixo (fora da faixa de clique do robô)
    c.waitfor(text='Gerencie as configurações do sistema', timeout=20)
    c.waitfor(idle=True)
    c.click(TAB('Integrações'), at=2.9, label='aba Integrações')
    c.pause(0.6)
    c.click(TAB('Integrações'), label='aba Integrações de novo (só se a subaba ainda não apareceu)', unless=SUBABA_WA)
    c.click(SUBABA_WA, at=c.A(1, 'automáticos', 1.0), label='subaba WhatsApp')
    c.waitfor(text='Conexão com o WhatsApp', timeout=15)
    c.confere('main', ['Conexão com o WhatsApp', 'Conecte o WhatsApp atual da empresa por QR Code. A API Oficial da Meta será adicionada depois, sem misturar os canais.', 'Desconectado'],
              'o cartão Conexão com o WhatsApp, com o selo Desconectado')
    c.mark(2)
    c.hover(P('Conexão com o WhatsApp'), 2.6, at=c.A(2, 'serviço', 0.9), label='cartão Conexão com o WhatsApp')
    c.hover(TXT('Desconectado'), 2.0, at=c.A(2, 'cobrança', 0.9), label='selo Desconectado')
    c.mark(3)
    c.hover(TAB('Integrações'), 0.9, at=c.A(3, 'Integrações,', 0.9), label='aba Integrações (de novo, na fala)')
    c.mark(4)   # fase 2: antes do hover que atravessa o início da L4 (o hover() o parte em dois na marca; antes a L4 atrasava 0,6 s)
    c.hover(SUBABA_WA, 0.9, at=c.A(3, 'WhatsApp.', 0.9, nth=1), label='subaba WhatsApp (de novo, na fala)')
    c.fim()
    return c


def cap01():
    """O que a integração faz: as seis áreas (cadeado nas que dependem da conexão) e o cartão "Conectar por QR Code"."""
    c = cap_novo(1, setup=setup_wa('Conexão com o WhatsApp'))
    c.mark(1)
    c.confere('main', ['Automações', 'Atendimento', 'Modelos', 'Campanhas', 'Histórico', 'Conexão', 'Desconectado'], 'as seis áreas e o selo Desconectado')
    c.hover(TABX('Automações'), 1.0, at=c.A(1, 'Automações', 0.9), label='área Automações (com cadeado)')
    c.hover(TABX('Histórico'), 1.0, at=c.A(1, 'Histórico', 0.9), label='área Histórico (com cadeado)')
    c.hover(TABX('Conexão'), 1.0, at=c.A(1, 'Conexão', 0.9), label='área Conexão (aberta)')
    c.mark(2)
    c.hover(TABX('Automações'), 0.9, at=c.A(2, 'automações', 0.9), label='cadeado de Automações')   # fase 2: 1,2 -> 0,9 s (o do Histórico atrasava 0,73 s)
    c.hover(TABX('Histórico'), 1.2, at=c.A(2, 'histórico', 0.9), label='cadeado de Histórico')
    c.mark(3)
    c.hover(P('Conectar por QR Code'), 2.0, at=c.A(3, 'QR', 0.9), label='cartão Conectar por QR Code')
    c.hover(P('Leva menos de um minuto'), 2.4, at=c.A(3, 'Leva', 0.9), label='Leva menos de um minuto')
    c.hover(TXT('Desconectado'), 1.4, at=c.A(3, 'quem', 1.0), label='selo Desconectado')
    c.fim()
    return c


def cap02():
    """Preparando o número: passo a passo, dica do chip separado, aceite do risco (marca a caixa) e o botão que libera."""
    c = cap_novo(2, setup=setup_wa('Conexão com o WhatsApp'))
    c.mark(1)
    c.confere('main', ['Abra o WhatsApp', 'Toque em Mais opções', 'Toque em Dispositivos conectados', 'Conectar dispositivo', 'Aponte a câmera para o QR Code desta tela.'], 'o passo a passo de quatro itens')
    c.hover(SEL('main ol'), 5.0, at=c.A(1, 'passo', 0.9), label='passo a passo de quatro itens')
    c.hover(P('Toque em Dispositivos conectados'), 1.6, at=c.A(1, 'Dispositivos', 0.9), label='passo 3: Dispositivos conectados')
    c.mark(2)
    c.hover(P('Pode ser melhor usar um número secundário'), 3.0, at=c.A(2, 'chip', 1.2), label='dica: um número secundário')
    c.mark(3)
    c.hover(P('Entendo que toda automação'), 0.9, at=c.A(3, 'Antes', 0.3), label='texto do aceite do risco')
    c.click(CHECK, at=c.A(3, 'marca', 0.9), label='marca a caixa do aceite')
    c.confere('main', ['Entendo que toda automação de WhatsApp fora da API Oficial da Meta tem um risco'], 'o texto do aceite')
    c.ev("document.querySelector('main button[role=checkbox]').getAttribute('aria-checked')", label='a caixa ficou marcada (true)')
    c.mark(4)
    c.hover(BTN('Conectar meu WhatsApp'), 2.4, at=c.A(4, 'botão', 0.9), label='botão Conectar meu WhatsApp (liberado)')
    c.ev("String(!document.evaluate(\"//button[contains(.,'Conectar meu WhatsApp')]\", document, null, 9, null).singleNodeValue.disabled)", label='o botão está liberado (true)')
    c.fim()
    return c


def cap03():
    """Lendo o QR Code: Conectar meu WhatsApp, QR e selo "Aguardando leitura do QR"; [ilustração]; leitura simulada por bastidor; Conectado, número, Canal ativo, Automações."""
    c = cap_novo(3, setup=setup_wa('Conexão com o WhatsApp', aceite=True))
    c.mark(1)
    c.click(BTN('Conectar meu WhatsApp'), at=c.A(1, 'Conectar', 0.9, nth=1), label='Conectar meu WhatsApp')
    c.waitfor(text='Aguardando leitura do QR', timeout=15)
    c.confere('main', ['Aguardando leitura do QR', 'WhatsApp → Aparelhos conectados → Conectar aparelho', 'Gerar novo QR Code'], 'QR na tela, selo Aguardando leitura do QR e botão Gerar novo QR Code')
    c.hover(SEL('main div.bg-white svg'), 2.0, at=c.A(1, 'QR', 0.9), label='o QR Code gerado (texto fictício)')
    c.hover(TXT('Aguardando leitura do QR'), 2.0, at=c.A(1, 'selo', 0.9), label='selo Aguardando leitura do QR')
    c.mark(2)
    # [ILUSTRAÇÃO na edição, 13 a 19 s] bastidor: o "celular lê o QR" (o webhook marcaria a conexão como conectada); a tela percebe na consulta de 4 s e vai sozinha para Automações
    c.ev(BASTIDOR_LEITURA, at=round(c.L(2) + 2.0, 2), label='bastidor: o celular lê o QR (leitura simulada)')
    c.waitfor(text='Automação de mensagens', timeout=20)
    c.mark(3)
    c.click(TABX('Conexão'), at=c.A(3, 'tela', 0.9), label='abre a área Conexão (Conectado)')
    c.confere('main', ['Conectado', 'Número: +552130001000', 'Desconectar', 'Canal ativo'], 'selo Conectado, número +552130001000, Desconectar e Canal ativo')
    c.hover(P('Número:'), 1.1, at=c.A(3, 'número', 0.9), label='Número: +552130001000')   # fase 2: 1,4 -> 1,1 s (o Canal ativo atrasava 0,73 s)
    c.hover(TXT('Canal ativo'), 1.4, at=c.A(3, 'canal', 0.9), label='selo Canal ativo')
    c.click(TABX('Automações'), at=c.A(3, 'Automações.', 0.9), label='abre as Automações')
    c.waitfor(text='Proteção do número', timeout=10)
    c.fim()
    return c


def cap04():
    """Horários de envio: Proteção do número, Avisos de serviço 07:00 às 22:00, Lembretes de cobrança (padrão), fila, Salvar configurações."""
    c = cap_novo(4, setup=setup_wa('Proteção do número'))
    c.mark(1)
    c.confere('main', ['Proteção do número', 'Regras que fazem os avisos saírem no ritmo de uma pessoa, e não de um robô.', 'Horários de envio', 'Fuso horário configurado para a empresa.'], 'cartão Proteção do número')
    c.hover(P('Proteção do número'), 2.6, at=c.A(1, 'Proteção', 0.9), label='cartão Proteção do número')
    c.hover(P('Horários de envio'), 1.6, at=c.A(1, 'respeita', 1.4), label='Horários de envio')
    c.mark(2)
    c.confere('main', ['Avisos de serviço', 'Técnico a caminho, serviço iniciado e serviço concluído.', 'Lembretes de cobrança', 'Cobrança gerada, lembrete de vencimento e aviso de atraso.', '06:00', '23:00', '08:00', '20:00'], 'as duas janelas, com os padrões 06:00 às 23:00 e 08:00 às 20:00')
    c.hover(JANELA_OS, 3.6, at=c.A(2, 'janelas.', 0.9), label='janela Avisos de serviço (06:00 às 23:00, todos os dias)')
    c.mark(3)
    # fase 2: cada escolha custa ~1,8 s; a 1ª começa mais cedo e a 2ª mais perto da palavra (na fase 1 o "Termina" atrasava 0,81 s)
    c.select(SEL('#whatsapp-window-os-start'), '07:00', at=c.A(3, 'sete', 2.3), label='Começa às 07:00')
    c.select(SEL('#whatsapp-window-os-end'), '22:00', at=c.A(3, 'dez', 1.5), label='Termina às 22:00')
    c.confere('main', ['Alterações não salvas'] if False else ['07:00', '22:00'], 'Avisos de serviço das 07:00 às 22:00')
    c.mark(4)
    c.hover(JANELA_COB, 3.2, at=c.A(4, 'lembretes', 0.9), label='janela Lembretes de cobrança (08:00 às 20:00, segunda a sábado)')
    c.ev("(()=>{const d=[...document.querySelectorAll('main button[aria-pressed]')].filter(b=>(b.getAttribute('aria-label')||'').startsWith('Lembretes de cobrança'));return d.map(b=>b.textContent+':'+b.getAttribute('aria-pressed')).join(' ')})()", label='dias dos lembretes (Seg a Sáb marcados, Dom não)')
    c.mark(5)
    c.hover(P('Fora do horário, a mensagem fica na fila e sai na próxima abertura.'), 2.6, at=c.A(5, 'Fora', 0.9), label='Fora do horário a mensagem fica na fila')
    c.mark(6)
    c.click(BTN('Salvar configurações'), at=c.A(6, 'Salvar', 0.9), label='Salvar configurações')
    c.waitfor(text='Configurações de WhatsApp salvas.', timeout=15)
    c.confere('main', ['Configurações salvas'], 'selo Configurações salvas')
    c.fim()
    return c


def cap05():
    """Os avisos da OS: Ativar automações, aba Ordens de serviço, Técnico a caminho em Cordial, link e prévia, lembrete de visita 1 dia antes, Salvar."""
    c = cap_novo(5, setup=setup_wa('Proteção do número'))
    c.mark(1)
    c.rolar(520, at=c.A(1, 'cartão', 1.2), label='desce até Automação de mensagens')
    c.click(SEL('#whatsapp-automation-master'), at=c.A(1, 'Ativar', 0.9), label='liga Ativar automações')
    c.confere('main', ['Automação de mensagens', 'Defina quais avisos serão enviados e como cada mensagem será montada.', 'Ativar automações', 'Alterações não salvas'], 'cartão Automação de mensagens, com Alterações não salvas')
    c.ev("document.querySelector('#whatsapp-automation-master').getAttribute('aria-checked')", label='Ativar automações ligado (true)')
    c.mark(2)
    c.hover(RADIO('Ordens de serviço'), 0.8, at=c.A(2, 'Ordens', 0.9), label='aba Ordens de serviço')
    c.confere('main', ['Escolha quando enviar', 'Lembrete de visita agendada', 'Técnico a caminho', 'Serviço iniciado', 'OS concluída'], 'a lista dos quatro momentos da OS')
    # fase 2: 0,8 -> 0,6 s nos dois primeiros (o robô rola a lista no hover do Técnico a caminho e o Serviço iniciado atrasava 0,76 s)
    c.hover(EVENTO('Lembrete de visita agendada'), 0.6, at=c.A(2, 'lembrete', 0.9), label='momento: Lembrete de visita agendada')
    c.hover(EVENTO('Técnico a caminho'), 0.6, at=c.A(2, 'técnico', 0.9), label='momento: Técnico a caminho')
    c.hover(EVENTO('Serviço iniciado'), 0.8, at=c.A(2, 'serviço', 0.9, nth=1), label='momento: Serviço iniciado')
    c.hover(EVENTO('OS concluída'), 0.8, at=c.A(2, 'OS', 0.9, nth=1), label='momento: OS concluída')
    c.ev("[...document.querySelectorAll('main button[role=switch][aria-label^=\"Enviar esta mensagem:\"]')].map(s=>s.getAttribute('aria-label').replace('Enviar esta mensagem: ','')+'='+s.getAttribute('aria-checked')).join(' | ')", label='interruptores dos quatro momentos (só o lembrete desligado)')
    c.mark(3)
    c.click(EVENTO('Técnico a caminho'), at=c.A(3, 'Clicando', 0.9), label='clica em Técnico a caminho (Editando)')
    c.confere('main', ['Editando', 'Enviar esta mensagem', 'Modelo da mensagem'], 'Técnico a caminho em edição')
    c.click(SEL('#whatsapp-template'), at=c.A(3, 'estilos', 0.9), label='abre Modelo da mensagem')
    c.confere('body', ['Rotação automática · recomendada', 'Objetiva', 'Cordial', 'Detalhada'], 'a lista dos modelos da mensagem')
    c.click(OPT('Cordial'), at=c.A(3, 'fixo', 0.7), label='escolhe Cordial')
    c.confere('main', ['Cordial'], 'Modelo da mensagem em Cordial')
    c.mark(4)
    c.hover(P('Incluir link de acompanhamento da OS'), 1.6, at=c.A(4, 'link', 0.9), label='Incluir link de acompanhamento da OS (ligado)')
    c.hover(P('Prévia ilustrativa'), 3.0, at=c.A(4, 'prévia', 0.9), label='Prévia da mensagem (Prévia ilustrativa)')
    c.confere('main', ['Prévia da mensagem', 'Prévia ilustrativa', 'o técnico Carlos já está a caminho para atender você na OS #1048'], 'a prévia Cordial cita o nome do técnico e o número da OS')
    c.mark(5)
    c.click(EVENTO('Lembrete de visita agendada'), at=c.A(5, 'Ligo', 0.9), label='clica em Lembrete de visita agendada')
    c.click(SEL('#whatsapp-selected-event'), at=c.A(5, 'lembrete', 0.9), label='liga Enviar esta mensagem')
    c.confere('main', ['Quando enviar o lembrete', '1 dia antes · recomendado'], 'Quando enviar o lembrete: 1 dia antes · recomendado')
    c.hover(P('Quando enviar o lembrete'), 2.0, at=c.A(5, 'dia', 0.9), label='Quando enviar o lembrete: 1 dia antes')
    c.mark(6)
    c.click(BTN('Salvar configurações'), at=c.A(6, 'Salvar', 0.9), label='Salvar configurações')
    c.waitfor(text='Configurações de WhatsApp salvas.', timeout=15)
    c.confere('main', ['Configurações salvas'], 'selo Configurações salvas')
    c.fim()
    return c


def cap06():
    """Os avisos de cobrança: aba Cobranças, os quatro momentos, 3 dias antes, valor e link, 2 dias depois. Só mostra, não salva."""
    c = cap_novo(6, setup=setup_wa('Automação de mensagens', rolar_ate_cartao=True))
    c.mark(1)
    # fase 2 (06/11): a aba no "Na aba Cobranças" e, logo depois, a página desce até a lista (título "Escolha quando enviar" em y 76) para a
    # lista E o editor (Quantos dias, Informações da cobrança) caberem na tela: na fase 1 o robô rolava sozinho 3 vezes (~1,5 s cada,
    # câmera pulando) e os passos atrasavam até 1,8 s. Hovers da lista mais curtos (0,8 -> 0,5/0,6 s).
    c.click(RADIO('Cobranças'), at=c.A(1, 'Cobranças', 0.9, nth=1), label='aba Cobranças')
    c.confere('main', ['Cobrança gerada', 'Manual ou criada por uma assinatura', 'Antes do vencimento', 'No vencimento', 'Após o vencimento', 'Somente se a cobrança continuar pendente'], 'os quatro momentos de cobrança')
    rola_ate(c, 'Escolha quando enviar', at=c.A(1, 'quatro', 0.6), label='desce até a lista e o editor das cobranças', y=76, dur_ms=900)
    c.hover(EVENTO('Cobrança gerada'), 0.6, at=c.A(1, 'gerada,', 0.9), label='momento: Cobrança gerada')
    c.hover(EVENTO('Antes do vencimento'), 0.6, at=c.A(1, 'antes', 0.9), label='momento: Antes do vencimento')
    c.hover(EVENTO('No vencimento'), 0.5, at=c.A(1, 'no', 0.9), label='momento: No vencimento')
    c.hover(EVENTO('Após o vencimento'), 0.5, at=c.A(1, 'depois.', 0.9), label='momento: Após o vencimento')
    c.mark(2)
    c.click(EVENTO('Antes do vencimento'), at=c.A(2, 'Antes', 0.9), label='clica em Antes do vencimento')
    c.ev("document.querySelector('#whatsapp-offset-days').value", label='Quantos dias antes = 3')
    c.confere('main', ['Quantos dias antes', 'dias'], 'Quantos dias antes')
    c.hover(P('Quantos dias antes'), 1.6, at=c.A(2, 'quantos', 0.9), label='Quantos dias antes (3)')
    c.hover(P('Informações da cobrança'), 2.2, at=c.A(2, 'leva', 0.9), label='Informações da cobrança: Valor e Link de pagamento')
    c.confere('main', ['Informações da cobrança', 'Valor', 'Link de pagamento'], 'Informações da cobrança: Valor e Link de pagamento')
    c.mark(3)
    c.click(EVENTO('Após o vencimento'), at=c.A(3, 'atraso', 1.2), label='clica em Após o vencimento')
    c.ev("document.querySelector('#whatsapp-offset-days').value", label='Quantos dias depois = 2')
    c.hover(P('Quantos dias depois'), 1.8, at=c.A(3, 'dois', 0.9), label='Quantos dias depois (2)')
    c.mark(4)
    c.ev("[...document.querySelectorAll('main button[role=switch][aria-label^=\"Enviar esta mensagem:\"]')].map(s=>s.getAttribute('aria-label').replace('Enviar esta mensagem: ','')+'='+s.getAttribute('aria-checked')).join(' | ')", label='interruptores das quatro cobranças (todos ligados)')
    c.hover(EVENTO('Cobrança gerada'), 0.5, at=c.A(4, 'quatro', 0.9), label='lista dos quatro momentos')
    c.hover(EVENTO('Após o vencimento'), 1.0, at=c.A(4, 'ligados,', 0.9), label='os quatro ligados')
    c.confere('main', ['Configurações salvas'], 'o selo segue Configurações salvas (nada a salvar)')
    c.fim()
    return c


def cap07():
    """A autorização do cliente: o texto da regra; Gestão > Clientes e Fornecedores > Hotel Mirante do Mar > Editar: "Receber mensagens pelo WhatsApp" ligado; Cancelar.
    Fase 2 (06/11): a navegação do Gestão até a janela Editar Cliente custa ~10 s e a fala não tinha vão para ela (na prévia pelo ensaio da
    fase 1 a L2 chegava 10,6 s atrasada). Respiro na voz entre a L1 e a L2 (pausas.py, original em t21/narracao/emendas/cap07.orig.json): a
    navegação corre no silêncio, a L2 começa com a janela aberta, e a montagem corta as esperas do caminho (rec/t21/ESTADO.md)."""
    c = cap_novo(7, setup=setup_wa('Automação de mensagens', rolar_ate_cartao=True))
    c.mark(1)
    c.hover(P('Somente clientes com a opção'), 2.6, at=0.3, label='Somente clientes com a opção Receber mensagens pelo WhatsApp')
    c.click(BTN('Gestão'), at=4.4, label='grupo Gestão do menu')
    c.click(LINK('Clientes e Fornecedores'), label='menu Clientes e Fornecedores')
    c.waitfor(text='Lista de Clientes', timeout=15)
    c.click(TXT('Hotel Mirante do Mar', within='main'), label='abre a ficha do Hotel Mirante do Mar')
    c.waitfor(target=TAB('Chamados'), timeout=15)
    c.click(BTN('Ações'), label='botão Ações da ficha')
    c.pause(0.5)
    c.click(BTN('Ações'), label='Ações de novo (só se o menu não abriu)', unless=ITEM('Editar'))
    c.click(ITEM('Editar'), label='Editar no menu Ações')
    c.waitfor(text='Editar Cliente', timeout=10)
    c.waitfor(idle=True)
    c.confere('dlg', ['Celular', 'Receber mensagens pelo WhatsApp', 'Permite avisos de ordens de serviço, cobranças e vencimentos. Pedidos de cancelamento do cliente sempre prevalecem.'], 'janela Editar Cliente: Celular e Receber mensagens pelo WhatsApp')
    c.confere_campos(['(21) 93000-2102'], 'o campo Celular do Hotel é (21) 93000-2102')
    c.ev("(()=>{const s=document.querySelector('[role=dialog] button[role=switch][aria-label=\"Receber mensagens pelo WhatsApp\"]');return s?s.getAttribute('aria-checked'):'sem interruptor'})()", label='Receber mensagens pelo WhatsApp ligado no Hotel (true)')
    c.mark(2)
    c.hover(SW('Receber mensagens pelo WhatsApp', within=DLG), 1.0, at=c.A(2, 'Ela', 0.5), label='a opção Receber mensagens pelo WhatsApp, no cadastro')
    c.hover(PD('Celular'), 3.0, at=c.A(2, 'lado', 0.9), label='campo Celular')
    c.mark(3)   # antes do hover que atravessa o início da L3: o hover() só parte em dois na marca que já está pendente
    c.hover(SW('Receber mensagens pelo WhatsApp', within=DLG), 2.6, at=c.A(2, 'Hotel', 1.0), label='interruptor Receber mensagens pelo WhatsApp (ligado)')
    c.hover(PD('Pedidos de cancelamento do cliente sempre prevalecem.'), 3.0, at=c.A(3, 'pedindo', 0.9), label='Pedidos de cancelamento do cliente sempre prevalecem')
    c.click(BTN('Cancelar', within=DLG), at=round(c.dur - 1.8, 2), label='Cancelar')
    c.waitfor(gone={'role': 'dialog'}, timeout=10)
    c.fim()
    return c


def cap08():
    """Acompanhando os envios (dia 13): Histórico, contadores e a lista (hotel: Lido, Lido, Entregue; academia: Ignorado com o motivo)."""
    c = cap_novo(8, setup=setup_wa('Automação de mensagens'))
    c.mark(1)
    c.click(TABX('Histórico'), at=c.A(1, 'Histórico', 0.9), label='abre o Histórico')
    c.waitfor(text='Fila e histórico de envios', timeout=15)
    c.confere('main', ['Fila e histórico de envios', 'Últimos 50 avisos transacionais. Mensagens ignoradas mostram o motivo.', 'Na fila', 'Enviado', 'Entregue', 'Lido', 'Ignorado', 'Falhou'], 'o cartão Fila e histórico de envios e os seis contadores')
    c.mark(2)
    c.hover(SEL('main div.grid.grid-cols-2'), 3.4, at=c.A(2, 'contadores', 0.9), label='os seis contadores (Entregue 1, Lido 2, Ignorado 1)')
    c.confere('main', ['Lido 2', 'Entregue 1', 'Ignorado 1', 'Enviado 0', 'Na fila 0', 'Falhou 0'], 'contadores: Lido 2, Entregue 1, Ignorado 1, Enviado 0')
    c.mark(3)
    SELO_LINHA = lambda k: SEL(f'main div.divide-y > div:nth-child({k + 1}) .inline-flex')   # só o selo da linha: o nome técnico do evento ("OS · a_caminho") fica fora do zoom (P1)
    c.confere('main', ['13/11/2026', 'Lido', 'Entregue', 'Ignorado'], 'as quatro linhas da lista, com a data')
    # fase 2: o 1º selo custa ~1,4 s até o gesto (vem dos contadores); começa antes e os `seconds` caem (na fase 1 o 2º e o 3º atrasavam 1,5 e 1,1 s)
    c.hover(SELO_LINHA(3), 1.0, at=c.A(3, 'técnico', 1.6), label='selo Lido do aviso do técnico a caminho')
    c.hover(SELO_LINHA(2), 1.2, at=c.A(3, 'iniciado', 0.9), label='selo Lido do aviso de serviço iniciado')
    c.mark(4)   # antes do hover que atravessa o início da L4 (na fase 1 a marca L4 só entrava depois dele e atrasava 1,3 s)
    c.hover(SELO_LINHA(1), 1.6, at=c.A(3, 'concluído', 0.9), label='selo Entregue do aviso de concluído')
    c.hover(SELO_LINHA(0), 1.2, at=c.A(4, 'ignorado,', 1.2), label='selo Ignorado do aviso da academia')
    c.hover(P('O cliente não autorizou mensagens pelo WhatsApp.'), 3.6, at=c.A(4, 'motivo', 0.9), label='o motivo: O cliente não autorizou mensagens pelo WhatsApp.')
    c.confere('main', ['O cliente não autorizou mensagens pelo WhatsApp.'], 'o motivo do Ignorado')
    c.fim()
    return c


def cap09():
    """Reconectar e desconectar: área Conexão (Conectado, número, Desconectar, Canal ativo); só zoom, sem clicar em Desconectar."""
    c = cap_novo(9, setup=setup_wa('Automação de mensagens'))
    c.mark(1)
    c.click(TABX('Conexão'), at=c.A(1, 'Conexão', 0.9), label='abre a área Conexão')
    c.confere('main', ['Conectado', 'Número: +552130001000', 'Desconectar', 'Canal ativo'], 'Conectado, número, Desconectar e Canal ativo')
    c.mark(2)
    c.hover(BTN('Desconectar'), 3.0, at=c.A(2, 'Desconectar', 0.9), label='botão Desconectar (sem clicar)')
    c.hover(P('O Dominex reduz o risco com consentimento, fila, aquecimento e limites.'), 3.2, at=c.A(2, 'lendo', 0.9), label='rodapé: O Dominex reduz o risco com consentimento, fila...')
    c.mark(3)
    c.hover(TXT('Canal ativo'), 3.0, at=c.A(3, 'canal', 0.9), label='selo Canal ativo')
    c.fim()
    return c


def cap10():
    """Recapitulando (dia 13): Conexão (Conectado), Automações (Proteção e prévia), o interruptor do cliente e o Histórico."""
    c = cap_novo(10, setup=setup_wa('Automação de mensagens'))
    c.mark(1)
    c.click(TABX('Conexão'), at=0.3, label='abre a área Conexão')
    c.hover(TXT('Canal ativo'), 1.6, at=c.A(1, 'QR', 0.9), label='selo Conectado e Canal ativo')
    c.mark(2)
    # fase 2 (06/11, voz 1.38.24): a L2 nova termina em "escolheu o estilo da mensagem do técnico a caminho" (+0,81 s). A página desce por
    # rolagem suave (título "Escolha quando enviar" em y 330: o cartão com a aba, a lista e a prévia inteiros na tela, sem o robô rolar
    # sozinho) e o cursor acompanha a fala: aba Ordens de serviço, aba Cobranças (só aponta), Técnico a caminho (Editando, Cordial) e a prévia.
    c.click(TABX('Automações'), at=c.A(2, 'Definiu', 0.9), label='abre as Automações')
    c.hover(P('Proteção do número'), 0.9, at=c.A(2, 'horários', 0.9), label='Proteção do número')
    rola_ate(c, 'Escolha quando enviar', at=c.A(2, 'ligou', 0.5), label='desce até Automação de mensagens', y=330, dur_ms=900)
    c.hover(RADIO('Ordens de serviço'), 0.9, at=c.A(2, 'ordem', 0.9), label='aba Ordens de serviço (avisos da OS ligados)')
    c.hover(RADIO('Cobranças'), 0.7, at=c.A(2, 'cobranças', 0.9), label='aba Cobranças (só aponta)')
    c.hover(EVENTO('Técnico a caminho'), 1.2, at=c.A(2, 'escolheu', 0.9), label='Técnico a caminho (Editando, Cordial)')
    c.mark(3)   # antes do hover que atravessa o início da L3 (o hover() só parte em dois na marca pendente)
    c.hover(P('Prévia ilustrativa'), 1.4, at=c.A(2, 'técnico', 0.9), label='aba Ordens de serviço com a prévia')
    # o interruptor do cliente (L3, "Viu que recebe quem está autorizado no cadastro") é montagem: a edição reaproveita o trecho "interruptor
    # Receber mensagens pelo WhatsApp (ligado)" do capítulo 7 (navegar até a ficha leva ~10 s); aqui o robô vai ao Histórico no começo da L3
    # (o clique sobe a página, ~1,9 s) e aponta os contadores no "acompanhou cada envio".
    c.click(TABX('Histórico'), at=round(c.L(3) + 0.1, 2), label='abre o Histórico')
    c.waitfor(text='Fila e histórico de envios', timeout=15)
    c.confere('main', ['Fila e histórico de envios', 'Lido 2', 'Entregue 1', 'Ignorado 1'], 'Histórico com os quatro avisos do dia 13')
    c.mark(4)   # antes do hover que atravessa o início da L4 (na fase 1 a marca só entrava no fim e atrasava 5,8 s)
    c.hover(SEL('main div.grid.grid-cols-2'), 2.6, at=c.A(3, 'acompanhou', 0.9), label='contadores do Histórico')
    c.fim()
    return c


CAPS = {n: globals()[f'cap{n:02d}'] for n in range(11) if f'cap{n:02d}' in globals()}

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
