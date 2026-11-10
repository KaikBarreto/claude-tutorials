#!/usr/bin/env python3
"""T15 · gera rec/t15/cap00..cap12.json (+ cap09b, o trecho do celular) a partir da voz pronta (t15/narracao/capNN.json).

Aula no COMPUTADOR (janela 1280x800), logada como Camila Duarte (admin, Glacial Cold Brasil), na Dominex 1.38.21, FAKE_NOW 11/11/2026 09:00
(o cap. 11 e o cap. 12 são "no dia seguinte": 12/11/2026 08:30). O trecho do celular do cap. 9 (link de ativação e batida, sem login) é o `cap09b`
("device": "phone"); a edição junta `cap09` (linhas 1 a 3) e `cap09b` (linhas 4 a 7).
Os `at` saem da palavra que anuncia cada passo (A(linha, palavra, folga)): o gesto "pousa" ~0,7 a 1 s depois do início do passo
(clique = deslocamento + ~0,85 s; digitação = clique + texto), então `at` = início da palavra - folga.
Rodar de qualquer pasta: `python3 -I rec/t15/gerar.py [NN ...]`. Depois: `node rec/record.mjs rec/t15/capNN.json --check`.

Cadeia de sementes: rec/t15/cadeia.json (semear.py: fim do T20 + fim do T2 + `t15/inicio`) e, a cada capítulo, o `t15/apos-capNN` do capítulo anterior
(cumulativo: guarda tudo o que mudou desde `t15/inicio`). O `apos-capNN` sai do ensaio (`rec/t15/snap.mjs diff NN`, na mesma trava).

Particularidades (lições deste tutorial, ver docs/08-licoes.md):
 - Os caps. 3, 4 e 5 continuam a janela "Novo Funcionário": o `setup` de cada um reabre a janela e refaz FORA do vídeo o que os anteriores preencheram.
 - Observador `OBS` guarda em `window.__avisos` todo aviso de erro do app, tela escura e faixa da trilha Domiflix; o passo final devolve a lista (tem de sair vazia).
 - `confere*` LÊ a tela e compara com a fala (o `resumo.py` acusa DIFERENTE).
"""
import hashlib
import json
import os
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TUT = os.path.normpath(os.path.join(HERE, '..', '..'))
NARR = os.path.join(TUT, 't15', 'narracao')
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

NOMES = ['Abertura', 'A tela de Funcionários', 'Os dados da funcionária', 'Salário e contrato', 'O dia do pagamento', 'Acesso ao sistema', 'Vale, bônus e falta',
         'O pagamento', 'As regras do ponto', 'O ponto no celular', 'Acompanhando o ponto', 'A folha em Contas a Pagar', 'Recapitulando']
# estado de partida de cada capítulo (sementes extras sobre a base; cada `apos-capNN` é cumulativo). O cap. 6 junta o corte dos salários; o cap. 10 parte
# do que o trecho do celular (cap. 9b) gravou; o cap. 11 e o cap. 12 juntam as folhas que o cron cria na madrugada de 12/11.
SEMENTE = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: ['apos-cap05', 'salarios'], 7: ['apos-cap06'], 8: ['apos-cap07'], 9: ['apos-cap08'],
           10: ['apos-cap09b'], 11: ['apos-cap10', 'folhas'], 12: ['apos-cap10', 'folhas']}


def norm(s):
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode().lower()
    return ''.join(ch for ch in s if ch.isalnum() or ch in '?')


class Cap:
    def __init__(s, n, pace=0.5, cps=9, start=(760, 420), prewarm=None, setup=None, user=None, nome=None, device=None, de=None, sem=None, anonymous=False):
        s.n = n
        s.nome = nome or f'cap{n:02d}'          # nome do arquivo do robô (cap09b = o trecho do celular do cap. 9)
        s.device, s.anonymous, s.sem = device, anonymous, sem
        d = json.load(open(f'{NARR}/cap{n:02d}.json', encoding='utf8'))
        s.words, s.linhas, s.dur = d['words'], d['linhas'], d['dur']
        s.steps = []
        s.pace, s.cps, s.start = pace, cps, start
        s.prewarm = prewarm or ['/dashboard', '/funcionarios']
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

    def mark(s, i, antecipa=0.9):
        # a marca vale "o robô chegou à linha": passo que antecipa a fala (até 0,9 s) não a atrasa. `antecipa` menor quando a linha anterior
        # termina de propósito num clique que fecha a fala dela (ex.: "Registrar Falta" no "reais."): a marca não acusa atraso à toa
        t = max(0.0, s.L(i) - antecipa) if s.L(i) > antecipa else s.L(i)
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
        js = ("(async()=>{const esp=%s;let out='';for(let i=0;i<12;i++){const v=[...document.querySelectorAll(%s+' input, '+%s+' textarea')].map(e=>e.value.replace(/\\u00a0/g,' ')).join(' | ');"
              "const falta=esp.filter(e=>!v.includes(e));if(!falta.length)return 'OK: '+esp.join(' | ');out='DIFERENTE: faltou '+JSON.stringify(falta)+' em: '+v.slice(0,260);"
              "await new Promise(r=>setTimeout(r,300));}return out})()") % (json.dumps(esp, ensure_ascii=False), json.dumps(escopo), json.dumps(escopo))
        return s.add({'do': 'eval', 'js': js, 'label': 'confere ' + label})

    def confere_campos_texto(s, escopo, esperados, label):
        return s.confere(escopo, esperados, label)

    def confere_ausente(s, escopo, texto, label, espera=None):
        """como `confere`, mas o texto NÃO pode aparecer (espera ~2 s para a tela terminar de atualizar).
        `espera` (s): em vez dos 1,8 s fixos, confere a cada 0,1 s e devolve OK assim que o texto some (DIFERENTE se ainda estiver lá
        depois de `espera`). Para o que some na hora (chave desligada): o passo não segura o robô (fase 2, 05/11)."""
        sel = {'dlg': '[role=dialog]', 'main': 'main', 'body': 'body'}.get(escopo, escopo)
        if espera:
            js = ("(async()=>{for(let i=0;i<=%d;i++){const el=document.querySelector(%s);const t=(el?el.innerText:'').replace(/[\\s\\u00a0]+/g,' ').toLowerCase();"
                  "if(!t.includes(%s))return 'OK: ausente '+%s;await new Promise(r=>setTimeout(r,100));}return 'DIFERENTE: apareceu '+%s})()") % (
                int(round(espera * 10)), json.dumps(sel), json.dumps(texto.lower()), json.dumps(texto), json.dumps(texto))
            return s.add({'do': 'eval', 'js': js, 'label': 'confere ' + label})
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
            'name': f't15-{s.nome}',
            'title': f'T15 · Cap. {s.n} · {NOMES[s.n]} (narração {str(round(s.dur, 1)).replace(".", ",")} s; marcas L1..L{len(s.linhas)} = início de cada linha do roteiro)',
            'seed': f't15-{s.nome}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
            'start': {'x': s.start[0], 'y': s.start[1]},
            'seedExtra': list(BASE) + [f't15/{x}' for x in (s.sem if s.sem is not None else SEMENTE[s.n])],
            'prewarm': s.prewarm, 'setup': s.setup, 'steps': s.steps,
            'storage': dict(STORAGE),
        }
        if s.user:
            d['user'] = s.user
        if getattr(s, 'voz_inicio', None):
            d['voz_inicio'] = s.voz_inicio      # cap09b: segundos da voz do cap. 9 em que o trecho começa (a edição e o resumo.py usam)
        if s.device:
            d['device'] = s.device
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




# ---------------------------------------------------------------- alvos próprios do T15 (funcionários)
SETUP_DASH = [{'do': 'goto', 'url': '/dashboard'}, {'do': 'waitFor', 'text': 'Olá, Camila!', 'timeout': 25}, AGUARDA]
SETUP_FUNC = [{'do': 'goto', 'url': '/funcionarios'}, {'do': 'waitFor', 'text': 'Lista de Funcionários', 'timeout': 25}, AGUARDA]
ABA_FUNC = lambda n: TAB(n)
NOVO_FUNC = BTN('Novo Funcionário')

DLGI = lambda ph, k=0: {'selector': f"{DLG} input[placeholder='{ph}']", 'nth': k}                       # campo da janela pelo placeholder
CAMPO_NOME, CAMPO_CPF, CAMPO_TEL = DLGI('Nome do funcionário'), DLGI('000.000.000-00'), DLGI('(00) 00000-0000')
CAMPO_CARGO, CAMPO_END = DLGI('Ex: Técnico'), DLGI('Endereço completo')
CAMPO_PIX = DLGI('CPF, email, telefone ou chave aleatória')
CAMPO_EMAIL = DLGI('email@exemplo.com')
MOEDA = lambda k=0: {'selector': f"{DLG} input[placeholder^='R$']", 'nth': k}   # o placeholder "R$ 0,00" usa espaço não separável: casa pelo prefixo
CAMPO_SAL, CAMPO_CUSTO = MOEDA(0), MOEDA(1)
CAMPO_CBO, CAMPO_MAT = DLGI('Ex: 7156-10'), DLGI('Ex: 00123')
DATA_ADM = {'selector': f"{DLG} div:has(> label:text-is('Data de Admissão')) > button"}
DIA = lambda d: {'selector': f'{POP} button:text-is("{d}") >> nth=0'}                                  # dia do calendário aberto (1º mês)
ABA_FORM = lambda n: {'role': 'tab', 'name': n, 'exact': True, 'within': DLG}
FOTO = {'text': 'Adicionar foto do funcionário', 'within': DLG}
# calculadora de custo mensal (janela por cima da janela do funcionário): campo pelo rótulo
CAMPO_TRANSP = {'selector': "div:has(> label:text-is('Transporte')) input"}
APLICAR = {'selector': "button:has-text('Aplicar R$')"}      # "Aplicar R$ ..." (nome por substring)


def setup_novo():
    """não filmado: abre a janela "Novo Funcionário" em branco (o `localStorage` do navegador novo não tem rascunho: P23)"""
    return SETUP_FUNC + [{'do': 'click', 'target': NOVO_FUNC}, {'do': 'waitFor', 'text': 'Nome Completo', 'timeout': 10}, {'do': 'pause', 'seconds': 0.6}]


def setup_dados():
    """não filmado: refaz a aba "Dados" do cap. 2 (a Tatiane); o e-mail mora na aba "Acesso" (1.38.19) e entra no cap. 5"""
    return setup_novo() + [
        {'do': 'type', 'target': CAMPO_NOME, 'text': 'Tatiane Ribeiro', 'cps': 40},
        {'do': 'type', 'target': CAMPO_CPF, 'text': '41837290687', 'cps': 40},
        {'do': 'type', 'target': CAMPO_TEL, 'text': '2130001008', 'cps': 40},
        {'do': 'type', 'target': CAMPO_CARGO, 'text': 'Assistente administrativa', 'cps': 40},
        {'do': 'type', 'target': CAMPO_END, 'text': 'Rua Gavião Peixoto, 120, apto 302, Icaraí, Niterói - RJ', 'cps': 60},
        {'do': 'click', 'target': DATA_ADM}, {'do': 'click', 'target': DIA(3)}, {'do': 'pause', 'seconds': 0.4},
        {'do': 'type', 'target': CAMPO_PIX, 'text': 'tatiane.ribeiro@glacialcold.example', 'cps': 60},
    ]


def setup_pagamento():
    """não filmado: refaz a aba "Pagamento" do cap. 3 (salário, custo pela calculadora, CLT, CBO, matrícula, VT)"""
    return setup_dados() + [
        {'do': 'click', 'target': ABA_FORM('Pagamento')}, {'do': 'pause', 'seconds': 0.5},
        {'do': 'type', 'target': CAMPO_SAL, 'text': '280000', 'cps': 40},
        {'do': 'click', 'target': BTN('Calcular', within=DLG)}, {'do': 'waitFor', 'text': 'Calcular Custo Mensal', 'timeout': 10}, {'do': 'pause', 'seconds': 0.6},
        {'do': 'type', 'target': CAMPO_TRANSP, 'text': '22000', 'cps': 40}, {'do': 'pause', 'seconds': 0.4},
        {'do': 'click', 'target': APLICAR}, {'do': 'pause', 'seconds': 0.8},
        {'do': 'click', 'target': BTN('CLT', within=DLG)},
        {'do': 'type', 'target': CAMPO_CBO, 'text': '4110-10', 'cps': 40}, {'do': 'type', 'target': CAMPO_MAT, 'text': '00008', 'cps': 40},
        {'do': 'click', 'target': BTN('Sim', within=DLG)}, {'do': 'pause', 'seconds': 0.4},
        {'do': 'type', 'target': {'selector': f"{DLG} div:has(> label:has-text('Valor mensal do VT')) input"}, 'text': '22000', 'cps': 40},
    ]


def setup_acesso():
    """não filmado: refaz os caps. 2 a 4 e põe o e-mail na aba "Acesso" (usado como login quando se cria acesso), voltando à aba "Pagamento", rolada até a configuração"""
    return setup_pagamento() + [
        {'do': 'click', 'target': ABA_FORM('Acesso')}, {'do': 'pause', 'seconds': 0.5},
        {'do': 'type', 'target': CAMPO_EMAIL, 'text': 'tatiane.ribeiro@glacialcold.example', 'cps': 60},
        {'do': 'click', 'target': ABA_FORM('Pagamento')}, {'do': 'pause', 'seconds': 0.5},
    ]


# ---- ficha, movimentações, pagamento (caps. 6 e 7), ponto (caps. 8 a 10) e folha (cap. 11)
FUNC = lambda nome: {'text': nome, 'within': 'main'}                                    # linha da lista de funcionários / texto da ficha
MOV = lambda n: BTN(n)                                                                  # Vale, Bônus, Falta, Pagamento, Extrato, Editar da ficha
TEXTAREA = {'selector': f'{DLG} textarea'}
TBTN = lambda nome, k: {'selector': f"main tbody tr:has-text('{nome}') td:last-child button", 'nth': k}   # "Hoje": 0 = olho, 1 = lápis
CHAVE = lambda rotulo: {'selector': f"xpath=//main//label[normalize-space()='{rotulo}']/following::button[@role='switch'][1]"}   # interruptor da aba Config (sem nome acessível)
DATA_HOJE = '2026-11-11'

MENU_FUNC = {'selector': "a[href='/funcionarios']:visible"}
MENU_CONTAS = {'selector': "a[href='/financeiro/contas']:visible"}
