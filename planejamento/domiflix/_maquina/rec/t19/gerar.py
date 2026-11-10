#!/usr/bin/env python3
"""T19 · gera rec/t19/cap00..cap13.json (roteiros do robô) a partir da voz pronta (t19/narracao/capNN.json).

Aula inteira no COMPUTADOR (janela 1280x800), logada como Camila Duarte (admin, Glacial Cold Brasil), na Dominex 1.38.19, FAKE_NOW 10/11/2026 10:00.
Exceção: o capítulo 8 abre o link de pagamento SEM login (`anonymous`), como o cliente.
Os `at` saem da palavra que anuncia cada passo (A(linha, palavra, folga)): o gesto "pousa" ~0,7 a 1 s depois do início do passo
(clique = deslocamento + ~0,85 s; digitação = clique + texto), então `at` = início da palavra - folga.
Rodar de qualquer pasta: `python3 -I rec/t19/gerar.py [NN ...]`. Depois: `node rec/record.mjs rec/t19/capNN.json --check`.

Cadeia de sementes: rec/t19/cadeia.json (semear.py: fim do T19 + `t19/inicio`) e, a cada capítulo, o último `t19/apos-capNN` do capítulo anterior
que mexeu no banco (SEMENTE abaixo). O `apos-capNN` sai da gravação (`rec/t19/snap.mjs diff NN`, na mesma trava).

Particularidades:
 - Todo capítulo logado parte do /dashboard (setup, não filmado) e só depois vai à tela do capítulo.
 - Menu lateral RECOLHIDO (`Toggle Sidebar`) nos capítulos de tabela larga (caps. 6 a 12); abertos: caps. 0 e 2 (a fala usa o menu).
 - Observador `OBS` guarda em `window.__avisos` todo aviso de erro do app, tela escura e faixa da trilha Domiflix; o passo final devolve a lista (tem de sair vazia).
 - Chave de API: SÓ a fictícia `$aact_exemplo_glacial_0000` (campo de senha: só pontos). Nada de chave ou token real.
"""
import json
import os
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TUT = os.path.normpath(os.path.join(HERE, '..', '..'))
NARR = os.path.join(TUT, 't19', 'narracao')
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

NOMES = ['Abertura', 'Como o dinheiro chega', 'Conectar a conta', 'Para onde vai o dinheiro', 'Taxas e preferências', 'O simulador', 'Uma cobrança avulsa',
         'A cobrança na lista', 'O que o cliente vê', 'Pago e baixado', 'Cobrança todo mês', 'Editar e cancelar', 'A parcela do contrato', 'Recapitulando']
# estado de partida de cada capítulo: o último apos-capNN (de capítulo anterior) que mexeu no banco
SEMENTE = {0: None, 1: None, 2: None, 3: 'apos-cap02', 4: 'apos-cap03', 5: 'apos-cap03', 6: 'apos-cap03', 7: 'apos-cap06', 8: 'apos-cap06',
           9: 'apos-cap08', 10: 'apos-cap08', 11: 'apos-cap10', 12: 'apos-cap10', 13: 'apos-cap12'}
CODIGO_COBRANCA = 'hn7xq3rmk4vp'   # código fixo da 1ª cobrança (handler tenant-asaas-create-charge): o link do cap. 8 e o "Link de pagamento" do cap. 6


def norm(s):
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode().lower()
    return ''.join(ch for ch in s if ch.isalnum() or ch in '?')


class Cap:
    def __init__(s, n, pace=0.5, cps=9, start=(760, 420), prewarm=None, setup=None, user=None, anonymous=False):
        s.n = n
        d = json.load(open(f'{NARR}/cap{n:02d}.json', encoding='utf8'))
        s.words, s.linhas, s.dur = d['words'], d['linhas'], d['dur']
        s.steps = []
        s.pace, s.cps, s.start = pace, cps, start
        s.prewarm = prewarm or ['/dashboard', '/financeiro/cobrancas']
        s.setup = list(setup or []) + [{'do': 'eval', 'js': OBS}]
        s.anchors = []
        s.pending = []
        s.user = user
        s.anonymous = anonymous

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
            'name': f't19-cap{s.n:02d}',
            'title': f'T19 · Cap. {s.n} · {NOMES[s.n]} (narração {str(round(s.dur, 1)).replace(".", ",")} s; marcas L1..L{len(s.linhas)} = início de cada linha do roteiro)',
            'seed': f't19-cap{s.n:02d}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
            'start': {'x': s.start[0], 'y': s.start[1]},
            'seedExtra': list(BASE) + ([f't19/{sem}'] if sem else []),
            'prewarm': s.prewarm, 'setup': s.setup, 'steps': s.steps,
            'storage': dict(STORAGE),
        }
        if s.user:
            d['user'] = s.user
        if s.anonymous:
            d['anonymous'] = True
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




# ---------------------------------------------------------------- trechos comuns deste tutorial
CHAVE = '$aact_exemplo_glacial_0000'   # chave FICTÍCIA (campo de senha: só pontos); a chave real nunca entra aqui
SETUP_COBRANCAS = SETUP_DASH + [{'do': 'goto', 'url': '/financeiro/cobrancas'}, {'do': 'waitFor', 'text': 'Cobranças e recorrências', 'timeout': 25}, AGUARDA]
ASAAS_URL = '/configuracoes?tab=integracoes&integration=asaas'
SETUP_ASAAS = SETUP_DASH + [{'do': 'goto', 'url': ASAAS_URL}, {'do': 'waitFor', 'text': 'Recebimentos (Asaas)', 'timeout': 25}, AGUARDA]
ROLA_PARA = ("(()=>{const t=%s;const el=[...document.querySelectorAll('main p, main h2, main h3, main label, main span')].find(e=>e.innerText&&e.innerText.trim().startsWith(t));"
             "if(!el)return 'sem '+t;el.scrollIntoView({behavior:'smooth',block:%s});return 'rolou'})()")


def rola_para(c, texto, at, label, bloco='center'):
    """rolagem suave (~1,6 s) da tela até o bloco que começa com `texto`; `at` = instante em que o `eval` dispara (antes da palavra)"""
    return c.ev(ROLA_PARA % (json.dumps(texto, ensure_ascii=False), json.dumps(bloco)), at=at, label=label)


# ================================================================ capítulos
def cap00():
    """Abertura: Dashboard, grupo Financeiro, item Cobranças: "Ative os recebimentos primeiro"."""
    c = Cap(0, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/financeiro/cobrancas'], setup=SETUP_DASH)
    c.mark(1)
    c.hover(LINK('Agenda'), 0.1, at=0.3, label='o cursor passa pelo menu lateral')
    c.click(BTN('Financeiro'), at=c.A(1, 'Financeiro.', 3.6), label='abre o grupo Financeiro do menu')
    c.mark(2)
    c.click(LINK('Cobranças'), at=c.A(2, 'Enquanto', 1.0), label='item Cobranças do grupo Financeiro')
    c.waitfor(text='Ative os recebimentos primeiro', timeout=20)
    c.hover(BTN('Ir para Integrações'), 1.4, at=c.A(2, 'ativar', 1.0), label='botão Ir para Integrações (sem clicar)')
    c.mark(3)
    c.hover(LINK('Cobranças'), 1.6, at=c.A(3, 'item', 0.9), label='o item Cobranças dentro do Financeiro')
    c.mark(4)
    c.fim()
    return c


def cap01():
    """Como o dinheiro chega: a ilustração entra na edição; por baixo, a tela Cobranças parada, com o cursor no item do menu."""
    c = Cap(1, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/financeiro/cobrancas'], setup=SETUP_COBRANCAS)
    c.mark(1)
    c.hover(BTN('Financeiro'), 1.0, at=c.A(1, 'cobrança', 0.9), label='o grupo Financeiro do menu')
    c.mark(2)
    c.mark(3)
    c.fim()
    return c


def cap02():
    """Conectar a conta: Configurações > Integrações > Cobranças (Asaas); a chave fictícia (só pontos); Ativar recebimentos; selo Ativo."""
    # a página de Configurações leva de 10 a 20 s para abrir com a máquina carregada (o clique no menu travava a tela e atrasava a voz toda): o capítulo já começa
    # nela (setup, não filmado) e o robô só passa o cursor pelo botão Configurações do menu
    c = Cap(2, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/configuracoes'],
            setup=SETUP_DASH + [{'do': 'goto', 'url': '/configuracoes'}, {'do': 'waitFor', 'text': 'Gerencie as configurações do sistema', 'timeout': 60}, AGUARDA])
    c.mark(1)
    c.hover(BTN('Configurações'), 0.2, at=c.A(1, 'Em', 3.5), label='Configurações, no rodapé do menu (a tela já está aberta: ver nota no cabeçalho; o 1º gesto custa ~7 s com a máquina carregada)')
    c.click(TAB('Integrações'), at=c.A(1, 'Integrações', 2.4), label='aba Integrações')
    c.click(TAB('Cobranças (Asaas)'), at=c.A(1, 'Cobranças.', 1.5), label='subaba Cobranças (Asaas)')
    c.waitfor(text='Recebimentos (Asaas)', timeout=15)
    c.confere('main', ['Cobre seus clientes por Pix, boleto e cartão usando sua própria conta Asaas.', 'Cole a chave de API da sua conta Asaas para ativar os recebimentos.',
                       'Como obter sua chave de API da Asaas', 'Ativar recebimentos'], 'o cartão pede a chave (sem selo de status)')
    c.mark(2)
    c.hover(P('Cole a chave de API da sua conta Asaas'), 1.8, at=c.A(2, 'ligação', 0.9), label='texto: cole a chave de API')
    c.hover(P('Como obter sua chave de API da Asaas'), 1.4, at=c.A(2, 'quadro', 0.9), label='quadro Como obter sua chave, com os quatro passos')
    c.mark(3)
    c.click({'placeholder': 'Cole aqui sua chave de API'}, at=c.A(3, 'colo', 1.2), label='campo Chave de API da Asaas')
    c.colar(CHAVE, at=c.A(3, 'colo', 0.3), label='cola a chave fictícia (campo de senha: só pontos)')
    c.ev("(()=>{const e=document.querySelector('#asaas-api-key');return e?e.type+' '+e.value.length+' caracteres':'sem campo'})()", label='o campo é de senha e recebeu a chave')
    c.hover(P('Chave de API da Asaas'), 1.4, at=c.A(3, 'pontinhos.', 1.2), label='o campo mostra só pontinhos')
    c.mark(4)
    c.click(BTN('Ativar recebimentos'), at=c.A(4, 'Ativar', 0.9), label='Ativar recebimentos')
    c.waitfor(text='Recebimentos ativos. Já é possível cobrar seus clientes.', timeout=15)
    c.confere('main', ['Ativo', 'Recebimentos ativos. Já é possível cobrar seus clientes.'], 'selo Ativo e a mensagem de recebimentos ativos')
    # no app real o cartão de taxas continua em "referência" depois de ativar (consulta guardada por 10 min, lida antes da ativação): a câmera não o filma assim;
    # o robô recarrega a página (corte na edição) e o cartão passa a mostrar as taxas da conta
    c.ev('location.reload()', at=c.A(4, 'Pronto,', 0.2), label='recarrega a página (o cartão de taxas só atualiza depois de recarregar)')
    c.waitfor(text='Taxas da sua conta Asaas, atualizadas em', timeout=25)
    c.waitfor(idle=True)
    c.confere('main', ['Ativo', 'Taxas da sua conta Asaas, atualizadas em'], 'depois de recarregar, o cartão mostra as taxas da conta (sem "referência")')
    c.confere_ausente('main', 'Taxas de referência', 'sem o aviso de taxas de referência')
    c.fim()
    return c


def cap03():
    """Para onde vai o dinheiro: aviso amarelo > Escolher agora > Conta Principal, Vendas de Serviços, Tarifas e Taxas > Salvar > os dois interruptores."""
    c = Cap(3, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/configuracoes'], setup=SETUP_ASAAS)
    c.mark(1)
    c.hover(P('Falta escolher a conta que recebe o dinheiro'), 1.6, at=c.A(1, 'aviso', 0.9), label='aviso amarelo: falta escolher a conta')
    c.click(TXT('Escolher agora'), at=c.A(1, 'Clico', 0.9), label='Escolher agora (a tela desce até o Lançamento no Financeiro)')
    c.mark(2)
    c.confere('main', ['Lançamento no Financeiro', 'Conta bancária de destino', 'Categoria da receita', 'Categoria da taxa (Asaas)'], 'a seção Lançamento no Financeiro')
    c.select({'selector': 'main button[role=combobox]', 'hasText': 'Escolha a conta'}, 'Conta Principal', at=c.A(2, 'Conta', 0.9), label='conta de destino: Conta Principal')
    # 1.38.19: "Categoria da receita" é um CAMPO DE TEXTO (placeholder "Nenhuma"), não uma lista: o filtro do app compara `type === 'income'` e o banco grava 'entrada'
    c.type({'selector': 'main input[placeholder="Nenhuma"]'}, 'Vendas de Serviços', at=c.A(2, 'receita', 1.0), cps=14, label='categoria da receita: Vendas de Serviços (campo de texto)')
    c.hover(P('Categoria da taxa (Asaas)'), 1.6, at=c.A(2, 'taxa', 0.9), label='categoria da taxa: Tarifas e Taxas')
    c.confere_campos('Tarifas e Taxas', 'categoria da taxa já vem em Tarifas e Taxas', escopo='main')
    c.mark(3)
    c.click(BTN('Salvar', nth='last'), at=c.A(3, 'Salvar.', 0.9), label='Salvar a seção Lançamento no Financeiro')
    c.waitfor(text='Configuração de lançamento salva.', timeout=8, optional=True)
    c.mark(4)
    rola_para(c, 'Lançar cobranças no Financeiro automaticamente', c.A(4, 'Repara', 1.6), 'a câmera sobe até os interruptores', bloco='center')
    c.hover(SW('Lançar cobranças no Financeiro automaticamente'), 1.4, at=c.A(4, 'primeiro', 0.9), label='interruptor: lançar cobranças no Financeiro')
    c.hover(SW('Lançar a taxa da Asaas como despesa'), 1.4, at=c.A(4, 'segundo', 0.9), label='interruptor: lançar a taxa da Asaas como despesa')
    c.fim()
    return c


def cap04():
    """Taxas e preferências: cartão Taxas da Asaas > Atualizar taxas > Multa e juros por atraso > Preferências de cobrança e Desconto por antecipação."""
    c = Cap(4, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/configuracoes'], setup=SETUP_ASAAS)
    c.mark(1)
    rola_para(c, 'Taxas da Asaas', c.A(1, 'Conta', 0.2), 'a câmera para no cartão Taxas da Asaas', bloco='start')
    c.confere('main', ['Taxas da Asaas', 'Pix', 'Boleto', 'Cartão de crédito', 'À vista (1x)', '2 a 6x', '7 a 12x', '13 a 21x', 'Antecipação',
                       'Prazo para o dinheiro cair', 'Taxas da sua conta Asaas, atualizadas em'], 'o cartão Taxas da Asaas com as faixas e o prazo')
    c.confere_ausente('main', 'não pagam tarifa', 'sem a nota de franquia do Pix (desmentiria a taxa do cap. 8)')
    c.hover(P('Taxas da Asaas'), 2.0, at=c.A(1, 'taxas', 0.9), label='cartão Taxas da Asaas')
    c.hover(P('Prazo para o dinheiro cair'), 0.6, at=c.A(1, 'prazo', 2.3), label='prazo pro dinheiro cair')
    c.mark(2)
    c.hover(P('As taxas são cobradas pela Asaas diretamente na sua conta.'), 1.8, at=c.A(2, 'sai', 0.9), label='nota: a Dominex não retém nada por transação')
    c.click(BTN('Atualizar taxas'), at=c.A(2, 'Atualizar', 2.0), label='Atualizar taxas')
    c.waitfor(text='Taxas atualizadas com a Asaas.', timeout=10, optional=True)
    c.mark(3)
    rola_para(c, 'Multa e juros por atraso', round(c.L(3) - 1.0, 2), 'a câmera desce até Multa e juros por atraso', bloco='center')
    c.confere_campos(['2', '1'], 'multa 2 e juros 1 ao mês', escopo='main')
    c.hover(P('Multa por atraso (%)'), 1.2, at=c.A(3, 'dois', 0.9), label='Multa por atraso (%) com 2')
    c.hover(P('Juros ao mês (%)'), 1.2, at=c.A(3, 'um', 0.9, nth=0), label='Juros ao mês (%) com 1')
    # 1.38.19: a dica "O limite máximo da Asaas é 10% ao mês." só aparece com juros acima de 10 (não com o 1 da conta): a câmera mostra o Salvar da seção
    c.hover(BTN('Salvar', nth=0), 0.4, at=c.A(3, 'salvar', 1.9), label='Salvar da seção Multa e juros por atraso (sem clicar)')
    c.mark(4)
    rola_para(c, 'Preferências de cobrança', round(c.L(4) - 1.0, 2), 'a câmera desce até Preferências de cobrança', bloco='start')
    c.hover(P('Meios de pagamento habilitados'), 1.6, at=c.A(4, 'meios', 0.9), label='Meios de pagamento habilitados')
    c.confere('main', ['Meios de pagamento habilitados', 'Pix', 'Boleto', 'Cartão de crédito'], 'Pix, boleto e cartão de crédito')
    rola_para(c, 'Desconto por antecipação', c.A(4, 'Desconto', 1.7), 'a câmera segue para Desconto por antecipação', bloco='center')
    c.hover(P('Desconto por antecipação'), 1.6, at=c.A(4, 'Desconto', 0.5), label='Desconto por antecipação')
    c.hover(P('Deixe em branco para não aplicar desconto.'), 1.6, at=c.A(4, 'Em', 0.9), label='em branco, não tem desconto')
    c.fim()
    return c


def cap05():
    """O simulador: botão Simulador > R$ 1.200,00 no cartão em 3x > resultado > Repassar ao cliente > Pix."""
    c = Cap(5, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/configuracoes'], setup=SETUP_ASAAS)
    c.mark(1)
    c.click(TAB('Simulador'), at=c.A(1, 'Simulador,', 0.9), label='botão Simulador, ao lado de Configurações')
    c.waitfor(text='Simulador de venda', timeout=10)
    c.mark(2)
    # 1.38.19: "Valor da venda" é um campo de texto SEM máscara (abre com 1000): digita "1200,00" por cima (com "120000" viraria R$ 120.000,00)
    c.digitar_num({'selector': '#sim-amount'}, '1200,00', at=c.A(2, 'mil', 0.9), label='Valor da venda: 1200,00')
    c.click(BTN('Cartão'), at=c.A(2, 'cartão,', 0.9), label='forma de pagamento: Cartão')
    c.select({'selector': 'main button[role=combobox]'}, '3x', at=c.A(2, 'três', 0.9), label='parcelas: 3x')
    c.mark(3)
    rola_para(c, 'Resultado da simulação', max(c.L(3) - 0.3, 0), 'a câmera desce até o Resultado da simulação', bloco='start')
    c.confere('main', ['Resultado da simulação', 'Valor bruto', 'R$ 1.200,00', 'Taxa da Asaas', 'Valor líquido na sua conta', 'R$ 1.157,63', 'Cada parcela para o cliente', 'R$ 400,00',
                       'Quando o dinheiro cai na sua conta', 'Parcela 3'], 'resultado: líquido R$ 1.157,63 e as três parcelas com a data')
    c.hover(P('Valor líquido na sua conta'), 0.5, at=c.A(3, 'valor', 1.2), label='Valor líquido na sua conta')
    rola_para(c, 'Quando o dinheiro cai na sua conta', c.A(3, 'embaixo,', 1.6), 'desce até Quando o dinheiro cai na sua conta (as três parcelas)', bloco='center')
    c.mark(4)
    rola_para(c, 'Valor da venda', round(c.L(4) - 1.5, 2), 'a câmera sobe até Quem paga a taxa', bloco='start')
    c.click(TXT('Repassar ao cliente'), at=round(c.L(4) + 0.1, 2), label='Repassar ao cliente')
    c.confere('main', ['O cliente paga', 'R$ 1.243,90', 'R$ 1.200,00'], 'no repasse o cliente paga mais e o líquido fica R$ 1.200,00')
    rola_para(c, 'Resultado da simulação', round(c.L(4) + 1.6, 2), 'a câmera desce até o resultado do repasse', bloco='start')
    c.hover(P('Valor líquido na sua conta'), 1.0, at=c.A(4, 'empresa', 0.5), label='o líquido fica igual ao valor da venda')
    c.mark(5)
    rola_para(c, 'Valor da venda', round(c.L(5) - 0.9, 2), 'sobe até Quem paga a taxa e a Forma de pagamento', bloco='start')
    c.click(TXT('A empresa absorve'), at=round(c.L(5) + 0.3, 2), label='volta para A empresa absorve')
    c.click(BTN('Pix'), at=round(c.L(5) + 1.3, 2), label='forma de pagamento: Pix')
    rola_para(c, 'Resultado da simulação', round(c.L(5) + 2.4, 2), 'desce até o resultado do Pix', bloco='start')
    c.confere('main', ['na hora', 'R$ 1.198,01'], 'no Pix o dinheiro cai na hora, líquido R$ 1.198,01')
    c.hover(P('Valor líquido na sua conta'), 0.3, at=round(c.L(5) + 2.7, 2), label='Valor líquido na sua conta (Pix) e na hora')
    c.hover(P('Estimativa. O valor final é calculado pela Asaas no momento da cobrança.'), 1.8, at=c.A(5, 'estimativa,', 1.6), label='dica: simulador é estimativa')
    c.fim()
    return c


SETUP_COBR_MENU = SETUP_COBRANCAS + [{'do': 'click', 'target': MENU_LATERAL}, {'do': 'pause', 'seconds': 0.8}]
NOVA_COBRANCA = BTN('Nova cobrança', nth=0)
ACOES_COBRANCA = {'selector': 'main button[aria-label="Ações da cobrança"]', 'nth': 0}
ACOES_ASSINATURA = {'selector': 'main button[aria-label="Ações da assinatura"]', 'nth': 0}
CLIENTE_COMBO = {'selector': f'{DLG} button[role=combobox]', 'nth': 0}
BUSCA_CLIENTE = {'placeholder': 'Buscar por cliente, telefone ou documento…'}


def escolhe_cliente(c, busca, nome, at, label):
    """abre o seletor de cliente da janela, busca e escolhe (clique + espera da lista)"""
    c.click(CLIENTE_COMBO, at=at, label=f'abre a lista de clientes ({label})')
    c.waitfor(target={'text': nome}, timeout=8)   # (o seletor da assinatura não tem campo de busca)
    # (sem digitar na busca: com teclado de verdade a lista filtrada não devolveu a opção no ensaio; a lista cheia traz o cliente e o clique rola até ele)
    c.pause(0.8)
    c.click({'text': nome}, label=f'cliente: {nome}')   # a opção traz o documento junto (texto exato não casa)


def dia_do_calendario(c, botao, dia, meses_a_frente, at, label):
    """abre o calendário do campo de data (`botao` = seletor), avança `meses_a_frente` meses e escolhe o `dia`"""
    c.click(botao, at=at, label=f'abre o calendário ({label})')
    for _ in range(meses_a_frente):
        c.click({'role': 'button', 'name': 'Go to next month'}, label=f'próximo mês ({label})')
    c.click(SEL(f'{POP} button:text-is("{dia}")'), label=f'escolhe o dia {dia} ({label})')


def cap06():
    """Uma cobrança avulsa: Nova cobrança (4 abas), Restaurante Sabor da Serra, R$ 450,00, vence em 13/11, Pagamento, Encargos, Financeiro, resumo, Gerar cobrança, copiar o link."""
    c = Cap(6, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/financeiro/cobrancas'], setup=SETUP_COBR_MENU)
    c.mark(1)
    c.hover(P('A RECEBER'), 0.8, at=c.A(1, 'totais', 0.9), label='cartões A receber, Recebido e Vencido')
    c.hover(P('Nenhuma cobrança'), 0.3, at=c.A(1, 'ainda', 2.2), label='a lista ainda vazia')
    c.mark(2)
    c.click(NOVA_COBRANCA, at=c.A(2, 'Clico', 1.6), label='Nova cobrança')
    c.waitfor(text='Gere um link de pagamento para enviar ao seu cliente.', timeout=10)
    c.hover(TAB('Encargos', within=DLG), 0.6, at=c.A(2, 'quatro', 0.9), label='as quatro abas da janela')
    escolhe_cliente(c, 'Sabor', 'Restaurante Sabor da Serra', c.A(2, 'Restaurante', 2.4), 'Restaurante Sabor da Serra')
    c.confere('dlg', ['Restaurante Sabor da Serra'], 'cliente escolhido')
    c.mark(3)
    c.confere_ausente('dlg', 'ainda não tem CPF ou CNPJ', 'sem aviso de documento (o restaurante tem CNPJ)')
    c.hover(CLIENTE_COMBO, 1.8, at=c.A(3, 'CPF', 0.9), label='campo Cliente preenchido, sem aviso de documento')
    c.mark(4)
    c.click({'selector': '#charge-amount'}, at=c.A(4, 'quatrocentos', 1.0), label='campo Valor')
    c.type({'selector': '#charge-amount'}, '45000', cps=8, noClick=True, label='Valor: 450,00')
    c.confere_campos('450,00', 'valor 450,00', escopo=DLG)
    c.confere('dlg', ['Resumo do recebimento'], 'o resumo do recebimento aparece embaixo (depois do cliente e do valor)')
    dia_do_calendario(c, {'selector': '#charge-due'}, 13, 0, c.A(4, 'vencimento', 0.9), 'vencimento 13/11/2026')
    c.confere('dlg', ['13/11/2026', 'a receita entra em 10/11/2026, o dia de hoje'], 'vencimento 13/11/2026 e a dica da competência em 10/11/2026')
    c.hover(P('Esta é a data em que o cliente deve pagar.', within=DLG), 0.5, at=c.A(4, 'dica:', 1.8), label='dica do regime de competência')
    c.click({'selector': '#charge-desc'}, at=c.A(4, 'Na', 4.6, nth=1), label='campo Descrição')
    c.type({'selector': '#charge-desc'}, 'Limpeza e higienização de 2 splits da cozinha', cps=16, noClick=True, label='Descrição: Limpeza e higienização de 2 splits da cozinha')
    c.mark(5)
    c.click(BTN('Avançar'), at=c.A(5, 'Avanço', 0.9), label='Avançar: aba Pagamento')
    c.waitfor(text='Forma de pagamento', timeout=8)
    c.click(COMBO('Cliente escolhe'), at=c.A(5, 'Deixo', 0.9), label='abre Forma de pagamento')
    c.waitfor(target=OPT('Cartão de crédito'), timeout=8)
    c.confere('body', ['Pix', 'Boleto', 'Cartão de crédito'], 'a lista traz Pix, Boleto e Cartão de crédito')
    c.press('Escape', at=c.A(5, 'decide', 0.9), label='fecha a lista sem trocar')
    c.pause(0.5)
    c.mark(6)
    c.click(BTN('Avançar'), at=c.A(6, 'Em', 0.9), label='Avançar: aba Encargos')
    c.waitfor(text='Multa (%)', timeout=8)
    c.confere_campos(['2', '1'], 'multa 2 e juros 1 já preenchidos', escopo=DLG)
    c.hover(P('Multa (%)', within=DLG), 1.6, at=c.A(6, 'multa', 0.9), label='Multa (%) e Juros ao mês (%) já preenchidos')
    c.mark(7)
    c.click(BTN('Avançar'), at=c.A(7, 'Na', 0.9), label='Avançar: aba Financeiro')
    c.waitfor(text='Lançar no financeiro', timeout=8)
    c.hover(P('Lançar no financeiro', within=DLG), 1.8, at=c.A(7, 'Lançar', 0.9), label='Lançar no financeiro: Sim')
    c.mark(8)
    c.click(P('Resumo do recebimento', within=DLG), at=c.A(8, 'Antes', 0.9), label='abre o Resumo do recebimento')
    c.confere('dlg', ['O cliente escolhe como pagar. Veja quanto sobra em cada forma:', 'R$ 448,01', 'R$ 436,05', 'Quanto o cliente paga', 'Pagando 30 dias depois do vencimento'],
              'resumo: Pix e boleto R$ 448,01, cartão à vista R$ 436,05 e o cenário de atraso')
    c.hover(P('Quanto o cliente paga', within=DLG), 1.8, at=c.A(8, 'quanto', 0.9, nth=1), label='Quanto o cliente paga, se atrasar')
    c.mark(9)
    c.click(BTN('Gerar cobrança'), at=c.A(9, 'Clico', 0.9), label='Gerar cobrança')
    c.waitfor(text='Aponte a câmera para pagar', timeout=15)
    c.confere('dlg', ['Cobrança gerada', 'Aponte a câmera para pagar', 'Link de pagamento', 'Enviar por WhatsApp'], 'cobrança gerada com o QR Code e o link de pagamento')
    c.confere_campos(f'/pagar/{CODIGO_COBRANCA}', 'o link de pagamento traz o código da cobrança', escopo=DLG)
    c.hover(P('Aponte a câmera para pagar', within=DLG), 1.6, at=c.A(9, 'QR', 0.9), label='QR Code da cobrança')
    c.mark(10)
    c.click(BTN('Copiar link'), at=c.A(10, 'copio', 0.9), label='Copiar link')
    c.waitfor(text='Link copiado!', timeout=6, optional=True)
    c.hover(BTN('Enviar por WhatsApp'), 2.0, at=c.A(10, 'WhatsApp,', 1.2), label='Enviar por WhatsApp (sem clicar)')
    c.fim()
    return c


def cap07():
    """A cobrança na lista: linha A receber, menu da cobrança (Copiar link, Editar, Excluir)."""
    c = Cap(7, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/financeiro/cobrancas'], setup=SETUP_COBR_MENU)
    c.mark(1)
    c.confere('main', ['Restaurante Sabor da Serra', '450,00', 'A receber', '13/11/2026', 'Cliente escolhe'], 'a linha da cobrança: A receber, 13/11/2026, Cliente escolhe')
    c.hover(SEL('main tbody tr', hasText='Restaurante Sabor da Serra'), 1.6, at=c.A(1, 'lista', 0.9), label='a linha do Restaurante Sabor da Serra, A receber')
    c.mark(2)
    c.click(ACOES_COBRANCA, at=c.A(2, 'menu', 0.9), label='menu ⋯ da cobrança')
    c.waitfor(target=ITEM('Copiar link'), timeout=8)
    c.click(ITEM('Copiar link'), at=c.A(2, 'Copiar', 0.9), label='Copiar link')
    c.waitfor(text='Link copiado!', timeout=6, optional=True)
    c.pause(0.8)
    c.mark(3)
    c.click(ACOES_COBRANCA, at=c.A(3, 'Editar', 1.6), label='menu ⋯ de novo')
    c.waitfor(target=ITEM('Editar'), timeout=8)
    c.click(ITEM('Editar'), at=c.A(3, 'Editar', 0.9), label='Editar')
    c.waitfor(text='As alterações são aplicadas na cobrança gerada.', timeout=8)
    c.hover(P('Vencimento', within=DLG), 1.2, at=c.A(3, 'valor,', 0.9), label='Editar cobrança: Valor, Vencimento e Descrição')
    c.click(BTN('Cancelar', within=DLG), at=c.A(3, 'Excluir', 2.2), label='Cancelar (fecha sem salvar)')
    c.pause(0.6)
    c.click(ACOES_COBRANCA, at=c.A(3, 'apaga', 1.4), label='menu ⋯ para mostrar o Excluir')
    c.waitfor(target=ITEM('Excluir'), timeout=8)
    c.hover(ITEM('Excluir'), 1.6, at=c.A(3, 'apaga', 0.2), label='Excluir (sem clicar)')
    c.press('Escape', label='fecha o menu')
    c.fim()
    return c


def cap08():
    """O que o cliente vê: link da cobrança SEM login (/pagar/<código>); Pix, Boleto, Cartão (sem pagar); corte: o pagamento é simulado fora da tela e a página mostra Pagamento confirmado."""
    link = f'/pagar/{CODIGO_COBRANCA}'
    setup = [{'do': 'goto', 'url': link}, {'do': 'waitFor', 'text': 'Valor a pagar', 'timeout': 25}, AGUARDA]
    c = Cap(8, pace=0.5, start=(760, 420), prewarm=['/dashboard'], setup=setup, anonymous=True)
    c.mark(1)
    c.confere('body', ['Glacial Cold Brasil', 'Valor a pagar', 'R$ 450,00', 'Vencimento', '13/11/2026', 'Limpeza e higienização de 2 splits da cozinha',
                       'Forma de pagamento', 'Pix', 'Aprovação na hora', 'Boleto', '1 a 2 dias úteis', 'Cartão', 'Aprovação imediata'], 'a página do cliente: marca, valor, vencimento, descrição e as três formas')
    c.hover(TXT('Valor a pagar'), 1.4, at=c.A(1, 'valor,', 0.9), label='Valor a pagar')
    c.hover({'text': 'Limpeza e higienização de 2 splits da cozinha'}, 1.4, at=c.A(1, 'descrição.', 0.9), label='a descrição do serviço (a página não traz o rótulo Descrição)')
    c.mark(2)
    c.click(TXT('Pix'), at=c.A(2, 'Pix,', 0.9), label='Pix')
    c.waitfor(text='Pague com Pix', timeout=8)
    c.confere('body', ['Escaneie o QR Code com o app do seu banco ou use o Pix copia e cola abaixo.', 'Copiar código Pix'], 'Pix: QR Code, copia e cola e o botão Copiar código Pix')
    c.click(BTN('Copiar código Pix'), at=c.A(2, 'copia', 0.9, nth=1), label='Copiar código Pix')
    c.waitfor(text='Código copiado!', timeout=6, optional=True)
    c.mark(3)
    c.click(TXT('Voltar'), at=round(c.L(3) - 1.7, 2), label='Voltar')
    c.click(TXT('Boleto'), at=c.A(3, 'boleto,', 1.0), label='Boleto')
    c.waitfor(text='Boleto bancário', timeout=8)
    c.hover({'text': 'Abrir boleto'}, 0.2, at=c.A(3, 'abre', 1.1), label='Abrir boleto (sem clicar)')
    c.click(TXT('Voltar'), at=c.A(3, 'cartão,', 3.0), label='Voltar')
    c.click(TXT('Cartão'), at=c.A(3, 'cartão,', 1.9), label='Cartão')
    c.waitfor(text='Pagamento com cartão', timeout=8)
    c.hover(SEL('button', hasText='Pagar R$ 450,00'), 0.4, at=c.A(3, 'preenche', 1.7), label='Pagar R$ 450,00 (sem preencher)')
    c.mark(4)
    c.ev("fetch(%s,{method:'POST',headers:{'content-type':'application/json'},body:'{}'}).then(r=>r.text())" % json.dumps(os.environ.get('FAKE_URL', 'http://127.0.0.1:54333') + '/functions/v1/asaas-simular-pagamento'),
         at=round(c.L(4) - 0.5, 2), label='CORTE: o Pix é pago fora da tela (o aviso do Asaas simulado)')
    # o robô navega por pushState (o `goto` na mesma rota não remonta a página nem consulta de novo): o foco do navegador (visibilitychange) refaz a consulta
    # (vale com a consulta já vencida, 15 s); se ainda não mostrou o pagamento, recarrega o mesmo link
    c.ev("document.dispatchEvent(new Event('visibilitychange'));window.dispatchEvent(new Event('focus'));'foco'", at=c.A(4, 'Abrindo', 2.4), label='volta ao mesmo link (a página consulta de novo)')
    c.pause(1.5)
    c.ev("(()=>{if(!document.body.innerText.includes('Pagamento confirmado')){location.reload();return 'recarregou'}return 'já mostra'})()", label='recarrega o link se ainda não mostrou o pagamento')
    c.waitfor(text='Pagamento confirmado', timeout=15)
    c.confere('body', ['Pagamento confirmado', 'Recebemos seu pagamento. Obrigado!'], 'Pagamento confirmado')
    c.hover(TXT('Pagamento confirmado'), 1.2, at=c.A(4, 'Pagamento', 1.6, nth=0), label='Pagamento confirmado')
    c.fim()
    return c


def cap09():
    """Pago e baixado: Cobranças com Pago e Recebido; Contas a Pagar/Receber (A Receber): bruto, taxa e líquido; Movimentações; menu da cobrança paga (Estornar)."""
    c = Cap(9, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/financeiro/cobrancas', '/financeiro/contas'], setup=SETUP_COBR_MENU)
    c.mark(1)
    c.confere('main', ['Pago', '450,00', 'RECEBIDO'], 'a cobrança está Pago e o Recebido soma 450,00')
    c.hover(SEL('main tbody tr', hasText='Restaurante Sabor da Serra'), 1.4, at=c.A(1, 'Pago,', 0.9), label='a linha Pago')
    c.hover(P('RECEBIDO'), 1.4, at=c.A(1, 'total', 0.9), label='cartão Recebido com R$ 450,00')
    c.mark(2)
    c.add({'do': 'goto', 'url': '/financeiro/contas', 'at': c.A(2, 'Em', 1.0), 'label': 'abre Contas a Pagar/Receber'})
    c.waitfor(target=TAB('A Receber'), timeout=20)
    c.click(TAB('A Receber'), label='aba A Receber')
    c.waitfor(text='Limpeza e higienização de 2 splits da cozinha', timeout=15)
    c.confere('main', ['Limpeza e higienização de 2 splits da cozinha', 'Bruto: R$ 450,00', 'Taxa: − R$ 1,99', 'Líquido: R$ 448,01', 'Pago'], 'a conta a receber paga com bruto, taxa e líquido')
    c.hover(P('Bruto: R$ 450,00'), 2.4, at=c.A(2, 'linha', 0.9), label='Bruto, Taxa e Líquido da conta a receber')
    c.mark(3)
    c.add({'do': 'goto', 'url': '/financeiro/movimentacoes', 'at': c.A(3, 'Nas', 1.0), 'label': 'abre Movimentações Financeiras'})
    c.waitfor(text='Tarifa de recebimento (Asaas)', timeout=20)
    c.confere('main', ['Limpeza e higienização de 2 splits da cozinha', 'Vendas de Serviços', 'Conta Principal', '+ R$ 450,00', 'Tarifa de recebimento (Asaas)', 'Tarifas e Taxas', '- R$ 1,99'],
              'a receita em Vendas de Serviços e a tarifa em Tarifas e Taxas')
    c.hover(SEL('main tr', hasText='Limpeza e higienização'), 0.7, at=c.A(3, 'receita', 1.1), label='a receita em Vendas de Serviços')
    c.hover(SEL('main tr', hasText='Tarifa de recebimento'), 1.6, at=c.A(3, 'taxa', 0.9, nth=0), label='a tarifa em Tarifas e Taxas')
    c.mark(4)
    c.add({'do': 'goto', 'url': '/financeiro/cobrancas', 'at': round(c.L(4) - 1.2, 2), 'label': 'volta para Cobranças'})
    c.waitfor(text='Restaurante Sabor da Serra', timeout=20)
    c.click(ACOES_COBRANCA, at=c.A(4, 'menu', 0.9), label='menu ⋯ da cobrança paga')
    c.waitfor(target=ITEM('Estornar'), timeout=8)
    c.hover(ITEM('Estornar'), 1.8, at=c.A(4, 'Estornar,', 0.9), label='Estornar (sem clicar)')
    c.press('Escape', label='fecha o menu')
    c.fim()
    return c


def cap10():
    """Cobrança todo mês: aba Assinaturas > Nova assinatura (Academia Ponto Forte, R$ 380,00, Mensal, 1º vencimento 10/12, Contínua) > resumo > Criar assinatura > MRR."""
    c = Cap(10, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/financeiro/cobrancas'], setup=SETUP_COBR_MENU)
    c.mark(1)
    c.click(TAB('Assinaturas'), at=c.A(1, 'Assinaturas,', 0.9), label='aba Assinaturas')
    c.waitfor(text='Nenhuma assinatura', timeout=10)
    c.click(BTN('Nova assinatura', nth=0), at=c.A(1, 'Clico', 1.9), label='Nova assinatura')
    c.waitfor(text='Configure uma cobrança recorrente para o seu cliente.', timeout=10)
    c.mark(2)
    escolhe_cliente(c, 'Academia', 'Academia Ponto Forte', c.A(2, 'Academia', 2.6), 'Academia Ponto Forte')
    c.click({'selector': f'{DLG} input[placeholder="0,00"]'}, at=c.A(2, 'trezentos', 1.2), label='campo Valor')
    c.type({'selector': f'{DLG} input[placeholder="0,00"]'}, '38000', cps=8, noClick=True, label='Valor: 380,00')
    c.click(COMBO('Mensal'), at=c.A(2, 'frequência', 0.9), label='abre Frequência')
    c.waitfor(target=OPT('Semanal'), timeout=8)
    c.hover(OPT('Anual'), 1.0, at=c.A(2, 'semanal', 0.9), label='a lista vai de Semanal a Anual')
    c.press('Escape', label='fecha a lista (fica em Mensal)')
    c.pause(0.5)
    c.mark(3)
    c.click(COMBO('Cliente escolhe'), at=c.A(3, 'forma', 0.9), label='abre Forma de pagamento')
    c.waitfor(target=OPT('Pix Automático'), timeout=8)
    c.hover(OPT('Cartão de crédito (recorrente)'), 0.8, at=c.A(3, 'cartão', 0.9), label='Cartão de crédito (recorrente)')
    c.hover(OPT('Pix Automático'), 1.2, at=c.A(3, 'Pix', 0.9, nth=0), label='Pix Automático')
    c.press('Escape', label='fecha a lista (fica em Cliente escolhe)')
    c.pause(0.5)
    c.mark(4)
    dia_do_calendario(c, SEL(f'{DLG} button[aria-haspopup]', hasText='/2026'), 10, 1, c.A(4, 'primeiro', 0.9), '1º vencimento 10/12/2026')
    c.confere('dlg', ['10/12/2026', 'Contínua', 'A assinatura segue gerando cobranças até você cancelar.', 'Número de ciclos'], '1º vencimento 10/12/2026, Duração Contínua e Número de ciclos')
    c.click({'placeholder': 'Ex.: Contrato de manutenção mensal'}, at=c.A(4, 'Duração,', 0.9), label='campo Descrição')
    c.type({'placeholder': 'Ex.: Contrato de manutenção mensal'}, 'Manutenção mensal dos splits', cps=16, noClick=True, label='Descrição: Manutenção mensal dos splits')
    c.hover(P('Número de ciclos', within=DLG), 0.4, at=c.A(4, 'ciclos', 1.4), label='Número de ciclos')
    c.mark(5)
    c.click(P('Resumo por cobrança', within=DLG), at=c.A(5, 'resumo', 0.9), label='abre o Resumo por cobrança')
    c.confere('dlg', ['Valores de UMA cobrança (Mensal), não o total da assinatura.', 'A assinatura não tem fim definido, então não existe total fechado.'], 'resumo por cobrança')
    c.hover(P('Valores de UMA cobrança', within=DLG), 1.8, at=c.A(5, 'cobrança,', 0.5), label='Valores de UMA cobrança')
    c.mark(6)
    c.click(BTN('Criar assinatura'), at=c.A(6, 'Clico', 0.9), label='Criar assinatura')
    c.waitfor(text='Receita recorrente mensal (MRR)', timeout=15)
    c.confere('main', ['Academia Ponto Forte', '380,00', 'Mensal', '10/12/2026', 'Cliente escolhe', 'Ativa', '1 assinatura ativa', 'Receita recorrente mensal (MRR): 380,00'],
              'a lista: Ativa, 1 assinatura ativa e MRR 380,00')
    c.hover(SEL('main tbody tr', hasText='Academia Ponto Forte'), 1.4, at=c.A(6, 'academia', 0.9), label='a assinatura Ativa na lista')
    c.hover(P('Receita recorrente mensal (MRR)'), 2.0, at=c.A(6, 'lá', 0.9), label='Receita recorrente mensal (MRR)')
    c.fim()
    return c


SETUP_ASSINATURAS = SETUP_COBR_MENU + [{'do': 'click', 'target': TAB('Assinaturas')}, {'do': 'waitFor', 'text': 'Academia Ponto Forte', 'timeout': 20}, AGUARDA]


def cap11():
    """Editar e cancelar: menu da assinatura > Editar (cliente travado) > Cancelar > Cancelar assinatura > Voltar; a assinatura segue Ativa."""
    c = Cap(11, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/financeiro/cobrancas'], setup=SETUP_ASSINATURAS)
    c.mark(1)
    c.click(ACOES_ASSINATURA, at=c.A(1, 'Editar', 1.6), label='menu ⋯ da assinatura')
    c.waitfor(target=ITEM('Editar'), timeout=8)
    c.click(ITEM('Editar'), at=c.A(1, 'Editar', 0.8), label='Editar')
    c.waitfor(text='O cliente não pode ser trocado depois que a recorrência é criada.', timeout=8)
    c.hover(P('O cliente não pode ser trocado', within=DLG), 0.4, at=c.A(1, 'cliente', 0.9), label='Cliente travado')
    c.mark(2)
    c.click(BTN('Cancelar', within=DLG), at=round(c.L(2) - 3.1, 2), label='Cancelar (fecha sem salvar)')
    c.pause(0.6)
    c.click(ACOES_ASSINATURA, at=c.A(2, 'Cancelar.', 1.4), label='menu ⋯ da assinatura')
    c.waitfor(target=ITEM('Cancelar'), timeout=8)
    c.click(ITEM('Cancelar'), at=c.A(2, 'Cancelar.', 0.5), label='Cancelar (abre a janela Cancelar assinatura)')
    c.waitfor(text='Esta ação não pode ser desfeita.', timeout=8)
    c.confere('body', ['Cancelar assinatura', 'as próximas cobranças desta assinatura deixam de ser geradas na Asaas', 'O histórico de cobranças já realizadas continua disponível no Financeiro'],
              'a janela Cancelar assinatura')
    c.hover(P('Ao cancelar, as próximas cobranças', within='[role=alertdialog],[role=dialog]'), 1.8, at=c.A(2, 'deixam', 0.9), label='aviso: as próximas cobranças deixam de ser geradas')
    c.mark(3)
    c.hover(BTN('Cancelar assinatura'), 0.3, at=round(c.L(3) - 0.4, 2), label='botões Cancelar assinatura e Voltar')
    c.click(BTN('Voltar'), at=c.A(3, 'Voltar', 0.9), label='Voltar')
    c.waitfor(gone={'text': 'Esta ação não pode ser desfeita.'}, timeout=8)
    c.confere('main', ['Academia Ponto Forte', 'Ativa'], 'a assinatura continua Ativa')
    c.mark(4)
    c.hover(SEL('main tbody tr', hasText='Academia Ponto Forte'), 2.0, at=c.A(4, 'lista', 0.5), label='a linha da assinatura (o selo de autorização ativa só aparece no Pix Automático)')
    c.fim()
    return c


SETUP_CONTRATO = SETUP_DASH + [{'do': 'goto', 'url': '/contratos'}, {'do': 'waitFor', 'text': 'PMOC - Hotel Mirante do Mar', 'timeout': 25}, AGUARDA,
                               {'do': 'click', 'target': MENU_LATERAL}, {'do': 'pause', 'seconds': 0.6},
                               {'do': 'click', 'target': TXT('PMOC - Hotel Mirante do Mar')}, {'do': 'waitFor', 'target': TAB('Financeiro'), 'timeout': 25}, AGUARDA,
                               {'do': 'click', 'target': TAB('Financeiro')}, {'do': 'waitFor', 'text': 'Mensalidade PMOC - jan/2027 (2/12)', 'timeout': 25}, AGUARDA]
COBRAR_ONLINE = {'selector': 'main button[aria-label="Cobrar online"]', 'nth': 0}   # a 1ª pendente é a jan/2027 (2/12): a dez/2026 já foi recebida (T13)


def cap12():
    """A parcela do contrato: Contratos > PMOC > Financeiro > Cobrar online da 2ª mensalidade > Gerar agora > selo Cobrança gerada; Cobrar o saldo em Contas a Receber."""
    c = Cap(12, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/contratos', '/financeiro/contas'], setup=SETUP_CONTRATO)
    c.mark(1)
    c.confere('main', ['Mensalidade PMOC - dez/2026 (1/12)', 'Pago', 'Mensalidade PMOC - jan/2027 (2/12)', 'Pendente'], 'a 1ª mensalidade paga e as seguintes Pendente')
    c.hover(COBRAR_ONLINE, 1.6, at=c.A(1, 'botão', 0.9), label='botão Cobrar online (só o ícone) ao lado da parcela')
    c.mark(2)
    c.click(COBRAR_ONLINE, at=c.A(2, 'Clico', 0.9), label='Cobrar online da 2ª mensalidade')
    c.waitfor(text='Esta cobrança é da parcela do contrato.', timeout=10)
    c.confere('dlg', ['Hotel Mirante do Mar', '1.200,00', 'O valor é o da parcela e não pode ser alterado.', '10/01/2027', 'Esta cobrança é da parcela do contrato. Quando o cliente pagar, a parcela é baixada automaticamente no seu financeiro, sem lançamento novo.'],
              'a janela já vem com o hotel, R$ 1.200,00 e o vencimento 10/01/2027')
    c.confere_ausente('dlg', 'Lançar no financeiro', 'sem a aba Financeiro')
    c.hover(P('Esta cobrança é da parcela do contrato.', within=DLG), 2.2, at=c.A(2, 'aviso:', 0.9), label='aviso: a própria parcela é baixada')
    c.mark(3)
    c.click(BTN('Gerar agora'), at=c.A(3, 'Gerar', 0.9), label='Gerar agora')
    c.waitfor(text='Aponte a câmera para pagar', timeout=15)
    c.click(BTN('Fechar'), at=c.A(3, 'selo', 1.0), label='Fechar o quadro com o link')
    c.waitfor(text='Cobrança gerada', timeout=10)
    c.confere('main', ['Cobrança gerada'], 'a parcela ganhou o selo Cobrança gerada')
    c.hover(P('Cobrança gerada'), 1.4, at=c.A(3, 'Cobrança', 1.3), label='selo Cobrança gerada na parcela')
    c.mark(4)
    c.add({'do': 'goto', 'url': '/financeiro/contas', 'at': round(c.L(4) - 0.4, 2), 'label': 'abre Contas a Pagar/Receber'})
    c.click(TAB('A Receber'), label='aba A Receber')
    c.waitfor(text='Orçamento #2 (1/3)', timeout=20)
    kebab = SEL("main tr:has-text('Orçamento #2 (1/3)') button[aria-haspopup='menu']")
    c.click(kebab, at=c.A(4, 'conta', 2.5), label='menu ⋮ da Orçamento #2 (1/3)')
    c.pause(0.6)
    c.click(kebab, label='menu ⋮ de novo (só se não abriu)', unless=ITEM('Cobrar o saldo'))
    c.waitfor(target=ITEM('Cobrar o saldo'), timeout=8)
    c.hover(ITEM('Cobrar o saldo'), 2.0, at=c.A(4, 'Cobrar', 0.9, nth=0), label='Cobrar o saldo (sem clicar)')
    c.press('Escape', label='fecha o menu')
    c.fim()
    return c


def cap13():
    """Recapitulando: base simples (Cobranças com a cobrança paga e a aba Assinaturas); os trechos da recapitulação entram na edição."""
    c = Cap(13, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/financeiro/cobrancas'], setup=SETUP_COBR_MENU)
    c.mark(1)
    c.hover(P('RECEBIDO'), 1.4, at=c.A(1, 'Recapitulando', 0.0), label='o quadro de Cobranças')
    c.mark(2)
    c.hover(SEL('main tbody tr', hasText='Restaurante Sabor da Serra'), 1.6, at=c.A(2, 'Gerou', 0.9), label='a cobrança Pago')
    c.mark(3)
    c.click(TAB('Assinaturas'), at=c.A(3, 'assinatura', 0.9), label='aba Assinaturas')
    c.hover(SEL('main tbody tr', hasText='Academia Ponto Forte'), 1.6, at=c.A(3, 'mensal', 0.9), label='a assinatura Ativa')
    c.mark(4)
    c.fim()
    return c


CAPS = {0: cap00, 1: cap01, 2: cap02, 3: cap03, 4: cap04, 5: cap05, 6: cap06, 7: cap07, 8: cap08, 9: cap09, 10: cap10, 11: cap11, 12: cap12, 13: cap13}


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
