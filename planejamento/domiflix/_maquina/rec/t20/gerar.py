#!/usr/bin/env python3
"""T20 · gera rec/t20/cap00..cap12.json (roteiros do robô) a partir da voz pronta (t20/narracao/capNN.json).

Aula inteira no COMPUTADOR (janela 1280x800), logada como Camila Duarte (admin, Glacial Cold Brasil), na Dominex 1.38.21, FAKE_NOW 10/11/2026 10:00.
Os `at` saem da palavra que anuncia cada passo (A(linha, palavra, folga)): o gesto "pousa" ~0,7 a 1 s depois do início do passo
(clique = deslocamento + ~0,85 s; digitação = clique + texto), então `at` = início da palavra - folga.
Rodar de qualquer pasta: `python3 -I rec/t20/gerar.py [NN ...]`. Depois: `node rec/record.mjs rec/t20/capNN.json --check`.

Cadeia de sementes: rec/t20/cadeia.json (semear.py: fim do T19 + `t20/inicio`) e, a cada capítulo, o último `t20/apos-capNN` do capítulo anterior
que mexeu no banco (SEMENTE abaixo; só o cap. 3 muda o banco: a estrutura do DRE). O `apos-capNN` sai do ensaio (`rec/t20/snap.mjs diff NN`, na mesma trava).

Particularidades (lições deste tutorial, ver docs/08-licoes.md):
 - Menu lateral RECOLHIDO (`Toggle Sidebar`) no `setup` de todo capítulo (a 1280 px o cabeçalho escuro do DRE não cabe com o menu aberto).
 - Observador `OBS` guarda em `window.__avisos` todo aviso de erro do app, tela escura e faixa da trilha Domiflix; o passo final devolve a lista (tem de sair vazia).
 - `confere*` LÊ a tela e compara com a fala (o `resumo.py` acusa DIFERENTE): valores do DRE/DFC/Análise dependem do histórico semeado.
"""
import json
import os
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TUT = os.path.normpath(os.path.join(HERE, '..', '..'))
NARR = os.path.join(TUT, 't20', 'narracao')
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

NOMES = ['Abertura', 'A visão geral', 'O resultado do mês', 'Organizar os grupos', 'Caixa ou competência', 'A compra no cartão', 'Comparar e projetar',
         'O caixa dos próximos dias', 'O que de fato entrou e saiu', 'O pacote do contador', 'Comparar meses e clientes', 'Fechar o mês', 'Recapitulando']
# estado de partida de cada capítulo: o último apos-capNN (de capítulo anterior) que mexeu no banco (só o cap. 3, a estrutura do DRE)
SEMENTE = {n: ('apos-cap03' if n >= 4 else None) for n in range(13)}


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
        s.prewarm = prewarm or ['/dashboard', '/financeiro/relatorios']
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
            'name': f't20-cap{s.n:02d}',
            'title': f'T20 · Cap. {s.n} · {NOMES[s.n]} (narração {str(round(s.dur, 1)).replace(".", ",")} s; marcas L1..L{len(s.linhas)} = início de cada linha do roteiro)',
            'seed': f't20-cap{s.n:02d}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
            'start': {'x': s.start[0], 'y': s.start[1]},
            'seedExtra': list(BASE) + ([f't20/{sem}'] if sem else []),
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



# ---------------------------------------------------------------- alvos próprios do T20 (relatórios)
POPW = '[data-radix-popper-content-wrapper]'
OPC = lambda txt: SEL(f'{POPW} button', hasText=txt)                       # opção do filtro de período (popover)
ABA = lambda n: TAB(n)                                                      # abas do Relatórios
ESTA = BTN('Este mês')
MES_PASSADO = BTN('Mês passado')
CAIXA = TAB('Regime de Caixa')
COMPET = TAB('Regime de Competência')
LINHA = lambda txt: SEL('main button', hasText=txt)                         # linha clicável do DRE (grupo ou categoria)
DIA_ESQ = lambda d: SEL(f'{POPW} table >> nth=0 >> button:text-is("{d}") >> nth=0')   # dia do 1º mês do calendário de intervalo
MES_ANT = {'role': 'button', 'name': 'Go to previous month'}
MES_PROX = {'role': 'button', 'name': 'Go to next month'}
ESPERA_TAB = {'visao-geral': 'Visão geral dos relatórios', 'dre': 'Demonstrativo de Resultado', 'dfc': 'Saldo atual',
              'contabilidade': 'Pacote para Contabilidade', 'analise': 'Compara períodos'}


def setup_rel(tab='visao-geral', preset=None, regime=None, menu_aberto=False):
    """não filmado: abre Relatórios na aba, recolhe o menu lateral, escolhe o período e o regime que o capítulo anterior deixou"""
    s = SETUP_DASH + [{'do': 'goto', 'url': f'/financeiro/relatorios?tab={tab}'},
                      {'do': 'waitFor', 'text': ESPERA_TAB[tab], 'timeout': 25}, AGUARDA]
    if not menu_aberto:
        s += [{'do': 'click', 'target': MENU_LATERAL}, {'do': 'pause', 'seconds': 0.8}]
    if preset:
        s += [{'do': 'click', 'target': ESTA}, {'do': 'click', 'target': OPC(preset)}, AGUARDA, {'do': 'pause', 'seconds': 1.0}]
    if regime:
        s += [{'do': 'click', 'target': TAB(regime)}, AGUARDA, {'do': 'pause', 'seconds': 0.8}]
    return s


def periodo(c, de, para, at, label):
    c.click(BTN(de), at=at, label=f'abre o filtro de período ({label})')
    c.click(OPC(para), label=f'escolhe {para}')
    c.add({'do': 'waitFor', 'idle': True})


def intervalo(c, ini_voltas, dia_ini, fim_avancos, dia_fim, at, label, de='Este mês', tab_fim=0):
    """Personalizado: volta `ini_voltas` meses, marca `dia_ini` no 1º mês; avança `fim_avancos`, marca `dia_fim` (no mês `tab_fim` da tela); Aplicar"""
    c.click(BTN(de), at=at, label=f'abre o filtro de período ({label})')
    c.click(OPC('Personalizado'), label='Personalizado')
    c.waitfor(text='Selecione o período', timeout=8)
    for k in range(ini_voltas):
        c.click(MES_ANT, label=f'mês anterior ({k + 1})')
    c.click(DIA_ESQ(dia_ini), label=f'dia inicial {dia_ini}')
    for k in range(fim_avancos):
        c.click(MES_PROX, label=f'mês seguinte ({k + 1})')
    alvo = DIA_ESQ(dia_fim) if tab_fim == 0 else SEL(f'{POPW} table >> nth={tab_fim} >> button:text-is("{dia_fim}") >> nth=0')
    c.click(alvo, label=f'dia final {dia_fim}')
    c.click(BTN('Aplicar'), label='Aplicar o período')
    c.add({'do': 'waitFor', 'idle': True})


# Fase 2 (05/11, Opus): navegar meses do calendário sem cursor. Os 5 cliques de "mês anterior/seguinte" custavam ~3,7 s e atrasavam a L2
# do cap. 1 em 1,7 s (lição 40: etapas "aceleradas" por eval; o vídeo mostra o calendário pulando e só os dias levam cursor).
NAV_MES = ("(async()=>{const P='[data-radix-popper-content-wrapper]';const lab=%s;for(let i=0;i<%d;i++){"
           "const b=document.querySelector(P+' button[aria-label=\"'+lab+'\"]');if(!b)return 'sem botao '+lab;b.click();"
           "await new Promise(r=>setTimeout(r,170));}const p=document.querySelector(P);return p?p.innerText.replace(/\\s+/g,' ').slice(0,70):'sem calendario'})()")


def js_botao_dlg(texto):
    """clica, por eval, o botão da janela aberta cujo texto é exatamente `texto` (botão do rodapé fixo, fora da faixa do click)"""
    return ("(()=>{const b=[...document.querySelectorAll('[role=dialog] button')].find(x=>x.textContent.trim()===%s);"
            "if(!b)return 'sem botao';b.click();return 'clicou'})()") % json.dumps(texto, ensure_ascii=False)


def intervalo_rapido(c, ini_voltas, dia_ini, fim_avancos, dia_fim, at, label, de='Este mês', at_ini=None, at_fim=None, at_aplicar=None):
    """como `intervalo`, mas a troca de mês é por eval (sem cursor); os dias e o Aplicar levam cursor e `at` próprios"""
    c.click(BTN(de), at=at, label=f'abre o filtro de período ({label})')
    c.click(OPC('Personalizado'), label='Personalizado')
    c.waitfor(text='Selecione o período', timeout=8)
    if ini_voltas:
        c.ev(NAV_MES % (json.dumps('Go to previous month'), ini_voltas), label=f'volta {ini_voltas} meses no calendário (sem cursor)')
    c.click(DIA_ESQ(dia_ini), at=at_ini, label=f'dia inicial {dia_ini}')
    if fim_avancos:
        c.ev(NAV_MES % (json.dumps('Go to next month'), fim_avancos), label=f'avança {fim_avancos} meses no calendário (sem cursor)')
    c.click(DIA_ESQ(dia_fim), at=at_fim, label=f'dia final {dia_fim}')
    c.click(BTN('Aplicar'), at=at_aplicar, label='Aplicar o período')
    c.add({'do': 'waitFor', 'idle': True})


MOVER = lambda cat: SEL(f'{DLG} button[role=combobox][aria-label="Mover {cat} para outro grupo DRE"]')
NATUREZA = SEL(f'{DLG} button[role=combobox][aria-label="Natureza na DRE"]', nth=0)
PONTO_DLG = (700, 420)   # meio do corpo rolável da janela Configurar DRE (div.overflow-y-auto do ResponsiveModal)


def cap_novo(n, **kw):
    kw.setdefault('prewarm', ['/dashboard', '/financeiro/relatorios'])
    return Cap(n, pace=0.5, start=(760, 420), **kw)


# ================================================================ capítulos
def cap00():
    """Abertura: Dashboard, menu Financeiro > Relatórios, a câmera passa pelas cinco abas."""
    c = cap_novo(0, setup=SETUP_DASH)
    c.mark(1)
    c.hover(LINK('Agenda'), 0.1, at=0.3, label='o cursor passa pelo menu lateral')
    c.click(BTN('Financeiro'), at=c.A(1, 'Financeiro', 0.9), label='abre o grupo Financeiro do menu')
    c.click(LINK('Relatórios'), at=c.A(1, 'resultado', 0.9), label='abre Relatórios')
    c.waitfor(text='Visão geral dos relatórios', timeout=20)
    c.mark(2)
    for palavra, nome, nth in [('Visão', 'Visão Geral', 0), ('Resultado.', 'DRE - Resultado', 0), ('DFC', 'DFC - Fluxo de Caixa', 0),
                               ('Contabilidade', 'Contabilidade', 0), ('Análise.', 'Análise', 0)]:
        c.hover(ABA(nome), 0.5, at=c.A(2, palavra, 0.9, nth=1 if palavra == 'Visão' and False else 0), label=f'aba {nome}')
    c.mark(3)
    c.hover(ABA('Visão Geral'), 1.0, at=c.A(3, 'Vamos', 0.9), label='volta à Visão Geral')
    c.fim()
    return c


def cap01():
    """A visão geral: período Personalizado (ago a out), regime, cartões, gráfico e categorias."""
    c = cap_novo(1, setup=setup_rel('visao-geral'))
    c.mark(1)
    intervalo_rapido(c, 3, 1, 2, 31, at=0.4, label='ago a out', at_ini=c.A(1, 'escolho,', 0.4), at_fim=c.A(1, 'três', 0.9),
                     at_aplicar=c.A(1, 'fecharam.', 0.9))
    c.confere('main', ['01/08/2026', '31/10/2026'], 'período 01/08 a 31/10')
    c.mark(2)
    c.hover(P('Visão geral dos relatórios'), 0.8, at=c.A(2, 'Repara', 0.8), label='título Visão geral dos relatórios')
    c.hover(CAIXA, 1.0, at=c.A(2, 'Caixa,', 0.9), label='Regime de Caixa (marcado)')
    c.hover(COMPET, 0.8, at=c.A(2, 'competência.', 1.2), label='Regime de Competência')
    c.mark(3)
    c.confere('main', ['Margem', 'Faturamento', 'Resultado', 'R$ 47.900,00'], 'cartões do período (faturamento ago a out em Caixa)')
    c.hover(TXT('Faturamento'), 1.0, at=c.A(3, 'faturamento,', 0.9), label='cartões Margem, Faturamento e Resultado')
    c.hover(TXT('Margem'), 0.8, at=c.A(3, 'margem', 0.9, nth=0), label='cartão Margem')
    c.mark(4)
    c.rolar(380, at=c.A(4, 'gráfico', 0.9), label='desce até o gráfico Receita × despesa', duration=1.4)
    c.hover(P('Receita × despesa'), 0.8, at=c.A(4, 'dá', 0.9), label='gráfico Receita × despesa')
    c.mark(5)
    c.rolar(520, at=c.A(5, 'embaixo,', 0.9), label='desce até as categorias', duration=1.6)
    c.hover(P('Receitas por categoria'), 1.0, at=c.A(5, 'receita', 0.9), label='Receitas por categoria')
    c.hover(P('Despesas por categoria'), 1.0, at=c.A(5, 'despesa,', 0.9), label='Despesas por categoria')
    c.fim()
    return c


def cap02():
    """O resultado do mês: aba DRE, Mês passado, cartões, tabela, grupo Custos diretos aberto, % da receita."""
    c = cap_novo(2, setup=setup_rel('visao-geral'))
    c.mark(1)
    c.click(ABA('DRE - Resultado'), at=c.A(1, 'Agora', 0.9), label='aba DRE - Resultado')
    c.waitfor(text='Demonstrativo de Resultado', timeout=20)
    periodo(c, 'Este mês', 'Mês passado', c.A(1, 'escolho', 1.0), 'Mês passado')
    c.confere('main', ['Outubro de 2026', '(+) Receita Bruta', 'R$ 13.950,00'], 'DRE de outubro: receita bruta 13.950,00')
    c.mark(2)
    # a DRE desta versão não tem cartões nem gráfico no alto: a fala (emenda 1.38.21) cita o que existe em cima da tabela
    c.hover(BTN('Configurar DRE'), 0.4, at=c.A(2, 'Configurar', 0.9), label='Configurar DRE')
    c.hover(CAIXA, 0.4, at=c.A(2, 'regime,', 0.9), label='escolha do regime')
    c.hover(SEL('main label', hasText='Incluir projeções'), 0.4, at=c.A(2, 'Incluir', 0.9), label='Incluir projeções')
    c.hover(BTN('Exportar'), 0.4, at=c.A(2, 'Exportar.', 0.9), label='Exportar')
    c.mark(3)
    c.rolar(300, at=c.A(3, 'tabela', 0.9), label='a câmera desce pela tabela do DRE', duration=1.5)
    c.confere('main', ['= Receita Líquida', '= Lucro Bruto', '= Resultado Líquido'], 'linhas de resultado da tabela')
    c.rolar(260, at=c.A(3, 'Menos', 0.9, nth=0), label='continua descendo', duration=1.5)
    c.rolar(260, at=c.A(3, 'E,', 0.9), label='até o resultado líquido', duration=1.5)
    c.mark(4)
    c.rolar(-700, at=c.A(4, 'Clicando', 1.6), label='sobe até o custo dos serviços', duration=1.2)
    c.click(LINHA('Custos diretos'), at=c.A(4, 'grupo,', 0.9), label='abre Custos diretos')
    c.confere('main', ['CSP - Materiais', 'CSP - Mão de Obra Avulsa', 'Peças e componentes'], 'categorias de Custos diretos')
    c.hover(P('Peças e componentes'), 1.0, at=c.A(4, 'peças', 0.9, nth=0), label='Peças e componentes')
    c.mark(5)
    c.hover(P('% receita'), 1.4, at=c.A(5, 'coluna', 0.9), label='coluna % da receita')
    c.fim()
    return c


def cap03():
    """Organizar os grupos: Configurar DRE, Novo subgrupo (Despesas administrativas e Despesas com veículos), mover categorias."""
    c = cap_novo(3, setup=setup_rel('dre', preset='Mês passado'))
    c.mark(1)
    c.click(BTN('Configurar DRE'), at=c.A(1, 'Configurar', 0.9), label='abre Configurar DRE')
    c.waitfor(text='Novo subgrupo', timeout=15)
    c.confere('dlg', ['Organize os grupos', 'Novo subgrupo', 'Despesa operacional'], 'janela Configurar DRE')
    c.mark(2)
    c.hover(P('Despesas com pessoal', within=DLG), 1.4, at=c.A(2, 'Repara', 0.9), label='subgrupo Despesas com pessoal')
    c.hover(BTN('Editar Despesas com pessoal'), 1.2, at=c.A(2, 'lápis,', 0.9), label='lápis do subgrupo (sem clicar)')
    # Fase 2 (05/11): a janela rola por inteiro e cada alvo fora da parte visível custava ~2 s de rolagem automática; agora a roda
    # (rolar, ~1,1 s) vai antes da palavra, os nomes entram por "colar" (eram 2,1 a 4,6 s de digitação) e a L5 (3,65 s de fala) ganhou
    # um respiro de 2,6 s na voz (pausas.py 03 49.2:2.6): criar o 2º subgrupo e mover o combustível não cabem na frase.
    c.mark(3)
    c.rolar(-2400, at=round(c.L(3) - 0.85, 2), label='volta ao topo da janela', ponto=PONTO_DLG)
    c.select(NATUREZA, 'Despesa operacional', at=c.A(3, 'natureza', 1.2), label='natureza Despesa operacional')
    c.click(SEL('#new-dre-group-name'), at=c.A(3, 'nome,', 0.9), label='campo do nome do subgrupo')
    c.colar('Despesas administrativas', c.A(3, 'Despesas', 0.0), 'nome do subgrupo (colado)')
    c.click(BTN('Adicionar', within=DLG), at=c.A(3, 'Adicionar.', 0.8), label='Adicionar')
    c.waitfor(text='Nenhuma categoria neste grupo', timeout=10)
    c.mark(4)
    c.rolar(800, at=round(c.L(4) - 0.85, 2), label='desce até as despesas operacionais', ponto=PONTO_DLG)
    for cat, palavra, folga in [('Aluguel', 'aluguel', 0.9), ('Luz/Energia', 'categoria', 0.0), ('Ferramentas e Equipamentos', 'ferramentas', 1.1)]:
        c.select(MOVER(cat), 'Despesas administrativas', at=c.A(4, palavra, folga), label=f'move {cat} para Despesas administrativas')
    c.mark(5)
    c.rolar(-2400, at=round(c.L(5) - 0.85, 2), label='volta ao topo da janela (2º subgrupo)', ponto=PONTO_DLG)
    c.click(SEL('#new-dre-group-name'), at=round(c.L(5) - 0.85 + 1.0, 2), label='campo do nome do 2º subgrupo')
    c.colar('Despesas com veículos', c.A(5, 'Despesas', 0.05), 'nome do 2º subgrupo (colado)')
    c.click(BTN('Adicionar', within=DLG), at=c.A(5, 'veículos,', 0.5), label='Adicionar o 2º subgrupo')
    c.waitfor(text='Nenhuma categoria neste grupo', timeout=10)
    c.rolar(800, label='desce até o combustível', ponto=PONTO_DLG)
    c.select(MOVER('Combustível/Transporte'), 'Despesas com veículos', label='move Combustível/Transporte para Despesas com veículos')
    c.mark(6)
    c.rolar(640, at=c.A(6, 'Repara', 0.6), label='mostra os subgrupos novos', ponto=PONTO_DLG)
    c.rolar(3000, at=c.A(6, 'E,', 1.3), label='desce até o fim da janela', ponto=PONTO_DLG)
    c.hover(P('Precisa de outra forma de ver o DRE?', within=DLG), 0.4, at=c.A(6, 'precisar,', 0.6), label='quadro Precisa de outra forma de ver o DRE?')
    c.hover(BTN('Outras visões', within=DLG), 1.6, at=c.A(6, 'Outras', 0.8), label='botão Outras visões (sem clicar)')
    fechar_janela(c, c.L(7) - 1.3, 0.4)
    c.mark(7)
    c.confere('main', ['Despesas administrativas', 'Despesas com veículos'], 'subgrupos no DRE')
    c.hover(P('Despesas administrativas'), 0.8, at=c.A(7, 'dois', 1.4), label='Despesas administrativas')
    c.hover(P('Despesas com veículos'), 1.2, at=c.A(7, 'operacionais.', 1.2), label='Despesas com veículos')
    c.fim()
    return c


def cap04():
    """Caixa ou competência: dicas dos regimes, o mês passado nos dois regimes e Este mês em caixa."""
    c = cap_novo(4, setup=setup_rel('dre', preset='Mês passado'))
    c.mark(1)
    c.hover(CAIXA, 0.8, at=c.A(1, 'Agora', 0.9), label='botões dos regimes')
    # Fase 2 (05/11): o W() casa por prefixo e sem pontuação, então "Competência," (nth 0) era o "competência." da 1ª frase e
    # "caixa," (nth 0) era o "Caixa." de "Regime de Caixa." (a rolagem marcada para 22,8 s saiu 3,2 s atrasada): nth=1 nos dois.
    c.hover(COMPET, 2.4, at=c.A(1, 'Competência,', 0.9, nth=1), label='dica do Regime de Competência')
    c.mark(2)
    c.click(LINHA('Despesas administrativas'), at=c.A(2, 'competência,', 0.9), label='abre Despesas administrativas')
    c.confere('main', ['Ferramentas e Equipamentos', 'R$ 430,00'], 'Ferramentas e Equipamentos (parcela 1/3) no mês passado em competência')
    c.hover(P('(+) Receita Bruta'), 1.2, at=c.A(2, 'Condomínio', 0.9), label='Receita Bruta com a instalação do Condomínio')
    c.hover(P('Ferramentas e Equipamentos'), 1.0, at=c.A(2, 'bomba', 0.9), label='Ferramentas e Equipamentos')
    c.mark(3)
    c.click(CAIXA, at=c.A(3, 'Agora,', 0.9), label='Regime de Caixa')
    c.confere('main', ['Regime de Caixa: cada lançamento entra no mês em que o dinheiro entrou ou saiu da conta'], 'rodapé do Regime de Caixa')
    c.hover(P('(+) Receita Bruta'), 0.8, at=c.A(3, 'receita', 0.9), label='Receita Bruta em caixa (diminuiu)')
    c.hover(P('Despesas administrativas'), 1.0, at=c.A(3, 'bomba', 0.9), label='Despesas administrativas sem a bomba de vácuo')
    c.rolar(900, at=c.A(3, 'caixa,', 0.9, nth=1), label='até o rodapé', duration=1.6)
    c.hover(P('* Regime de Caixa'), 1.8, label='rodapé do Regime de Caixa')
    c.mark(4)
    c.rolar(-1200, at=c.A(4, 'foram', 0.9), label='volta ao topo', duration=1.0)
    periodo(c, 'Mês passado', 'Este mês', c.A(4, 'Este', 0.9), 'Este mês')
    c.click(LINHA('Despesas administrativas'), label='abre Despesas administrativas (se fechou)', optional=True, unless=P('Ferramentas e Equipamentos'))
    c.confere('main', ['Ferramentas e Equipamentos', 'R$ 430,00'], 'Este mês em caixa: a parcela paga com a fatura')
    c.hover(P('(+) Receita Bruta'), 1.2, at=c.A(4, 'condomínio', 0.9), label='Receita Bruta de Este mês com o Condomínio')
    c.hover(P('Ferramentas e Equipamentos'), 1.0, at=c.A(4, 'cartão', 1.2, nth=0), label='Ferramentas e Equipamentos em Este mês')
    c.mark(5)
    c.hover(CAIXA, 1.2, at=c.A(5, 'visões', 0.9), label='as duas visões')
    c.hover(COMPET, 1.2, at=c.A(5, 'Competência', 0.9, nth=0), label='Competência')
    c.hover(CAIXA, 1.2, at=c.A(5, 'caixa', 0.9), label='Caixa')
    c.fim()
    return c


def cap05():
    """A compra no cartão: três linhas de ilustração; na tela, o DRE de Este mês em caixa com Ferramentas e Equipamentos."""
    c = cap_novo(5, setup=setup_rel('dre', regime='Regime de Caixa'))
    c.mark(1)
    c.mark(2)
    c.mark(3)
    c.mark(4)
    # Fase 2 (05/11): o clique (1,7 s) ia a L(4) - 1,4 e atrasava a L4 em 1,2 s; agora sai 3 s antes, ainda sob a ilustração (repouso)
    c.click(LINHA('Despesas administrativas'), at=round(c.L(4) - 3.0, 2), label='abre Despesas administrativas')
    c.hover(P('Ferramentas e Equipamentos'), 1.6, at=c.A(4, 'bomba', 0.5), label='Ferramentas e Equipamentos')
    c.mark(5)
    c.rolar(520, at=c.A(5, 'transferência', 0.9), label='desce pela tabela: nada de transferência nem de fatura', duration=2.5)
    c.confere_ausente('main', 'Pagamento de Fatura', 'sem Pagamento de Fatura no DRE')
    c.confere_ausente('main', 'Transferência entre contas', 'sem Transferência entre contas no DRE')
    c.fim()
    return c


def cap06():
    """Comparar e projetar: Comparar períodos (Período anterior), depois Personalizado até o fim do mês seguinte com Incluir projeções."""
    c = cap_novo(6, setup=setup_rel('dre'))
    c.mark(1)
    periodo(c, 'Este mês', 'Mês passado', c.A(1, 'Volto', 0.9), 'Mês passado')
    c.click(BTN('Comparar períodos'), at=c.A(1, 'Comparar', 0.9), label='Comparar períodos')
    c.waitfor(text='Comparar com', timeout=10)
    # Fase 2 (05/11): "Período" (nth 0) era o "períodos." de "Comparar períodos." (o clique saía 1,6 s antes da fala); "Aplicar comparação"
    # e "Remover comparações" ficam no rodapé fixo da janela (y CSS ~723, fora da faixa 96..730): 2,2 a 2,4 s de rolagem em vão por
    # clique. Agora vão por clicar_fixo (cursor + eval). A comparação sai no "E agora pra frente" (L3), e não durante a L2, que fala dela.
    c.click(SEL(f'{DLG} button', hasText='Período anterior'), at=c.A(1, 'Período', 0.9, nth=1), label='Período anterior')
    c.clicar_fixo(BTN('Aplicar comparação'), (968, 723), js_botao_dlg('Aplicar comparação'), c.A(1, 'Aplicar', 0.2), 'Aplicar comparação')
    c.waitfor(gone={'role': 'dialog'}, timeout=10)
    c.confere('main', ['Setembro de 2026', 'Outubro de 2026', 'R$ 19.850,00', 'R$ 13.950,00'], 'colunas de setembro e outubro (receita bruta)')
    c.mark(2)
    c.hover(P('(+) Receita Bruta'), 1.8, at=c.A(2, 'Assim', 0.9), label='as duas colunas lado a lado')
    c.mark(3)
    # a comparação continua na tela e bagunça a projeção: tira antes de seguir (Comparar períodos > Remover comparações)
    c.click(BTN('Comparar períodos'), at=c.A(3, 'E', 0.2), label='Comparar períodos de novo')
    c.waitfor(text='Remover comparações', timeout=10)
    c.clicar_fixo(BTN('Remover comparações'), (323, 723), js_botao_dlg('Remover comparações'), round(c.L(3) + 1.4, 2), 'Remover comparações')
    c.waitfor(gone={'role': 'dialog'}, timeout=10)
    c.type(COMPET, '', noClick=True, label='Regime de Competência', optional=True, timeout=4)   # só o retângulo (destaque na edição)
    intervalo(c, 0, 1, 0, 31, at=round(c.L(3) + 1.7, 2), label='01/11 a 31/12', de='Personalizado', tab_fim=1)
    c.click({'role': 'switch', 'name': 'Incluir projeções'}, at=c.A(3, 'Ligado', 0.9), label='liga Incluir projeções')
    c.confere('main', ['1 ciclo(s) previsto(s)', 'R$ 380,00'], 'projeção de um ciclo de R$ 380,00')
    c.mark(4)
    c.rolar(900, at=c.A(4, 'rodapé,', 0.9), label='até o rodapé', duration=1.6)
    c.confere('main', ['Inclui R$ 380,00 de assinaturas identificadas como previstas; nenhuma transação foi criada.'], 'rodapé das projeções')
    c.hover(P('Inclui R$ 380,00'), 1.8, label='rodapé das projeções')
    c.fim()
    return c


def cap07():
    """O caixa dos próximos dias: DFC previsto, 30 dias, valor do dia, coluna Dívida."""
    c = cap_novo(7, setup=setup_rel('visao-geral'))
    c.mark(1)
    c.click(ABA('DFC - Fluxo de Caixa'), at=c.A(1, 'DFC,', 0.9), label='aba DFC - Fluxo de Caixa')
    c.waitfor(text='Saldo atual', timeout=20)
    c.confere('main', ['Saldo atual', 'A receber · 15 dias', 'A pagar · 15 dias', 'Dívidas a receber', 'Dívidas a pagar'], 'cartões do DFC previsto')
    c.hover(P('Saldo atual'), 1.2, at=c.A(1, 'saldo', 0.9, nth=0), label='Saldo atual')
    c.hover(P('A receber · 15 dias'), 1.2, at=c.A(1, 'entrar', 0.9), label='A receber e A pagar em 15 dias')
    c.mark(2)
    c.click(BTN('30 dias'), at=c.A(2, 'trinta', 0.9), label='30 dias')
    c.confere('main', ['Saldo inicial', 'Recebimentos', 'Total de saídas', 'Saldo final', 'Dívida'], 'matriz dia a dia')
    c.hover(P('Saldo inicial'), 1.0, at=c.A(2, 'saldo', 0.9, nth=0), label='Saldo inicial')
    c.hover(P('Recebimentos'), 1.0, at=c.A(2, 'entra,', 0.9), label='Recebimentos')
    c.hover(P('Total de saídas'), 1.0, at=c.A(2, 'sai,', 0.9), label='Total de saídas')
    c.mark(3)
    c.click(SEL('main td[role=button]', hasText='R$ 2.800,00'), at=c.A(3, 'valor,', 0.9), label='valor das saídas de hoje (aluguel)')
    c.waitfor(text='Total do dia', timeout=10)
    c.confere('dlg', ['Aluguel do galpão', 'R$ 2.800,00'], 'lista do dia com o aluguel')
    fechar_janela(c, c.A(3, 'Assim', 0.9))
    c.mark(4)
    c.hover(SEL('main thead th', hasText='Dívida'), 1.4, at=c.A(4, 'separado,', 0.9), label='coluna Dívida (vazia)')
    c.hover(P('Previsão otimista'), 2.0, at=c.A(4, 'vazia,', 0.9), label='texto Previsão otimista')
    c.fim()
    return c


def cap08():
    """O que de fato entrou e saiu: DFC Realizado, Mês passado, atividades, Exportar."""
    c = cap_novo(8, setup=setup_rel('dfc'))
    c.mark(1)
    c.click(BTN('Realizado'), at=0.2, label='Realizado')
    periodo(c, 'Este mês', 'Mês passado', 0.4, 'Mês passado')
    c.confere('main', ['Saldo inicial', 'Variação líquida', 'Saldo final'], 'cartões do DFC realizado')
    c.hover(P('Saldo inicial'), 0.4, at=c.A(1, 'saldo', 0.9, nth=0), label='Saldo inicial')
    c.hover(P('Variação líquida'), 0.4, at=c.A(1, 'variação', 0.9), label='Variação líquida')
    c.hover(P('Saldo final'), 0.4, at=c.A(1, 'fim.', 0.9), label='Saldo final')
    c.mark(2)
    c.rolar(420, at=c.A(2, 'entradas', 0.9), label='a câmera desce pelas atividades operacionais', duration=3.0)
    c.mark(3)
    c.rolar(-420, at=c.A(3, 'Exportar', 2.0), label='volta ao topo', duration=1.0)
    c.click(BTN('Exportar'), at=c.A(3, 'Exportar', 0.9), label='Exportar')
    c.waitfor(text='CSV', timeout=8)
    c.hover(ITEM('CSV'), 1.2, at=c.A(3, 'CSV.', 1.0), label='Excel, PDF e CSV')
    c.press('Escape', at=c.A(3, 'Uma', 0.6), label='fecha o menu sem escolher')
    c.fim()
    return c


def cap09():
    """O pacote do contador: aba Contabilidade em Mês passado, os quatro cartões, Exportar pacote."""
    c = cap_novo(9, setup=setup_rel('dfc', preset='Mês passado'))
    c.mark(1)
    c.click(ABA('Contabilidade'), at=c.A(1, 'aba', 0.9), label='aba Contabilidade')
    c.waitfor(text='Pacote para Contabilidade', timeout=20)
    c.confere('main', ['Pacote para Contabilidade', 'Excel multiabas', 'Período selecionado'], 'faixa do pacote')
    c.hover(P('Excel multiabas'), 1.4, at=c.A(1, 'Excel,', 0.9), label='selo Excel multiabas')
    c.mark(2)
    for texto, palavra in [('Lançamentos completos', 'lançamentos'), ('DRE e DFC reconciliados', 'DFC,'), ('Saldos e obrigações', 'saldos'), ('Plano gerencial', 'plano')]:
        c.hover(P(texto), 0.9, at=c.A(2, palavra, 0.9), label=texto)
    c.mark(3)
    c.hover(P('Período selecionado'), 1.0, at=c.A(3, 'período', 0.9), label='período selecionado')
    c.click(BTN('Exportar pacote'), at=c.A(3, 'clico', 0.9), label='Exportar pacote')
    c.waitfor(text='Pacote para Contabilidade exportado!', timeout=20)
    c.pause(2.0)
    c.fim()
    return c


def cap10():
    """Comparar meses e clientes: aba Análise, tabela, ranking por faturamento e por margem."""
    c = cap_novo(10, setup=setup_rel('dre'))
    c.mark(1)
    c.click(ABA('Análise'), at=c.A(1, 'última', 0.9), label='aba Análise')
    c.waitfor(text='Compara períodos', timeout=20)
    c.confere('main', ['Mês a mês', '3 meses', 'set/26', 'out/26', 'nov/26', 'Variação'], 'tabela de meses')
    c.hover(P('Período'), 1.4, at=c.A(1, 'mês', 0.9), label='tabela mês a mês')
    c.mark(2)
    c.rolar(520, at=c.A(2, 'Embaixo,', 0.9), label='desce até os clientes', duration=1.6)
    c.confere('main', ['Maior faturamento', 'Top 5', 'Hotel Mirante do Mar'], 'ranking por faturamento')
    c.hover(P('Hotel Mirante do Mar'), 1.4, at=c.A(2, 'Hotel', 0.9), label='Hotel Mirante do Mar em primeiro')
    c.mark(3)
    c.click(SEL('main button[role=combobox][aria-label="Ordenar clientes por"]'), at=c.A(3, 'trocando', 0.9), label='ordenar clientes por')
    c.click(OPT('Melhor margem'), at=c.A(3, 'margem,', 0.9), label='Melhor margem')
    c.confere('main', ['Padaria Bom Grão'], 'Padaria Bom Grão no ranking por margem')
    c.confere_ausente('main', 'Hotel Mirante do Mar', 'o hotel fora do Top 5 por margem')
    c.hover(P('Padaria Bom Grão'), 1.4, at=c.A(3, 'Padaria', 0.9), label='Padaria Bom Grão no topo')
    c.mark(4)
    c.hover(P('Custo direto'), 1.4, at=c.A(4, 'receita', 0.9), label='coluna Custo direto')
    c.fim()
    return c


def cap11():
    """Fechar o mês: DRE em Mês passado e Competência, zoom no período, no regime e em Exportar (Excel e PDF)."""
    c = cap_novo(11, setup=setup_rel('dre', preset='Mês passado'))
    c.mark(1)
    c.hover(MES_PASSADO, 0.3, at=0.0, label='período Mês passado')
    c.hover(COMPET, 0.3, at=max(0.6, c.A(1, 'fechar,', 0.9)), label='Regime de Competência')
    c.click(BTN('Exportar'), at=c.A(1, 'sai', 0.9), label='Exportar')
    c.waitfor(text='PDF', timeout=8)
    c.hover(ITEM('PDF'), 1.4, at=c.A(1, 'PDF,', 0.9), label='Excel e PDF')
    c.press('Escape', at=c.A(1, 'tela.', 0.4), label='fecha o menu sem escolher')
    c.mark(2)
    c.mark(3)
    c.hover(MES_PASSADO, 0.5, at=c.A(3, 'período', 0.9), label='período')
    c.hover(COMPET, 0.5, at=c.A(3, 'regime', 0.9), label='regime')
    c.fim()
    return c


def cap12():
    """Recapitulando: montagem pelas abas (Visão Geral, DRE, troca de regime, DFC, Contabilidade, Análise)."""
    c = cap_novo(12, setup=setup_rel('visao-geral'))
    c.mark(1)
    c.hover(P('Margem'), 1.2, at=c.A(1, 'visão', 0.9), label='Visão Geral')
    c.click(ABA('DRE - Resultado'), at=c.A(1, 'resultado,', 0.9), label='aba DRE')
    c.waitfor(text='Demonstrativo de Resultado', timeout=20)
    c.mark(2)
    c.click(CAIXA, at=c.A(2, 'caixa', 0.9, nth=0), label='Regime de Caixa')
    c.click(COMPET, at=c.A(2, 'aconteceu,', -0.6), label='Regime de Competência')
    c.mark(3)
    c.click(ABA('DFC - Fluxo de Caixa'), at=c.A(3, 'DFC', 0.9), label='aba DFC')
    c.waitfor(text='Saldo atual', timeout=20)
    c.click(ABA('Contabilidade'), at=c.A(3, 'pacote', 0.9), label='aba Contabilidade')
    c.mark(4)
    c.click(ABA('Análise'), at=c.A(4, 'Análise', 0.9), label='aba Análise')
    c.waitfor(text='Compara períodos', timeout=20)
    c.mark(5)
    c.hover(P('Maior faturamento'), 1.2, at=c.A(5, 'fiscal', 0.4), label='ranking de clientes', optional=True)
    c.fim()
    return c


CAPS = {n: globals()[f'cap{n:02d}'] for n in range(13)}

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
