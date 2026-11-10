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


# ================================================================ capítulos
def cap_novo(n, **kw):
    return Cap(n, pace=0.5, start=(760, 420), **kw)


def cap00():
    """Abertura: Dashboard, menu lateral, grupo Gestão, "Funcionários (RH)"."""
    c = cap_novo(0, setup=SETUP_DASH)
    c.mark(1)
    c.hover(LINK('Agenda'), 0.1, at=0.3, label='o cursor passa pelo menu lateral')
    c.click(BTN('Gestão'), at=c.A(1, 'cadastro', 1.5), label='abre o grupo Gestão do menu')   # 1º clique do capítulo: ~2,5 s (app ainda carregando)
    c.click(MENU_FUNC, at=c.A(1, 'dinheiro', 0.9), label='abre Funcionários')
    c.waitfor(text='Lista de Funcionários', timeout=20)
    c.mark(2)
    c.hover(P('Funcionários (RH)'), 1.0, at=c.A(2, 'Com', 0.2), label='o cabeçalho Funcionários (RH)')
    c.mark(3)
    c.hover(MENU_FUNC, 1.2, at=c.A(3, 'item', 0.9), label='o item Funcionários (RH) do menu, em Gestão')
    c.mark(4)
    c.hover(P('Funcionários (RH)'), 1.0, at=c.A(4, 'Vamos', 0.9), label='volta ao cabeçalho')
    c.fim()
    return c


def cap01():
    """A tela de Funcionários: abas da lateral, lista com os seis técnicos."""
    c = cap_novo(1, setup=SETUP_FUNC)
    c.mark(1)
    c.hover(ABA_FUNC('Funcionários'), 0.5, at=c.A(1, 'Funcionários', 0.9), label='aba Funcionários')
    c.hover(ABA_FUNC('PJ/MEI'), 0.6, at=c.A(1, 'PJ', 0.9), label='aba PJ/MEI')
    c.mark(2)
    c.hover(ABA_FUNC('Equipes'), 0.6, at=c.A(2, 'Equipes', 0.9), label='aba Equipes')
    c.hover(ABA_FUNC('Controle de Ponto'), 0.6, at=c.A(2, 'Controle', 0.9), label='aba Controle de Ponto')
    c.mark(3)
    c.hover(ABA_FUNC('Perfil Comportamental'), 0.5, at=c.A(3, 'ferramentas', 0.9), label='aba Perfil Comportamental')
    c.hover(ABA_FUNC('Organograma'), 0.4, label='aba Organograma')
    c.hover(ABA_FUNC('Fluxograma'), 0.4, label='aba Fluxograma')
    c.mark(4)
    c.hover(P('Bruno Alves'), 1.0, at=c.A(4, 'lista', 0.9), label='a lista de funcionários')
    c.confere('main', ['Lista de Funcionários', 'Bruno Alves', 'Júlia Santos', 'Lucas Ferreira', 'Marina Costa', 'Paulo Souza', 'Rafael Lima',
                       'Selecione um funcionário', 'Técnico de refrigeração'], 'a lista tem os seis técnicos e nenhuma ficha aberta')
    c.mark(5)
    c.hover(NOVO_FUNC, 0.9, at=c.A(5, 'bora', 0.9), label='botão Novo Funcionário')
    c.fim()
    return c


def cap02():
    """Os dados da funcionária: janela "Novo Funcionário", aba Dados (o e-mail mora na aba Acesso desde a 1.38.19)."""
    c = cap_novo(2, setup=SETUP_FUNC)
    c.mark(1)
    c.hover(P('Lista de Funcionários'), 0.3, at=0.3, label='o cursor passa pela lista')
    c.click(NOVO_FUNC, at=c.A(1, 'cadastro', 1.0), label='Novo Funcionário')
    c.waitfor(text='Nome Completo', timeout=10)
    c.mark(2)
    for palavra, nome in [('Dados,', 'Dados'), ('Pagamento,', 'Pagamento'), ('Acesso,', 'Acesso'), ('Ponto', 'Ponto eletrônico'), ('Perfil.', 'Perfil')]:
        c.hover(ABA_FORM(nome), 0.15, at=c.A(2, palavra, 0.9), label=f'aba {nome}')
    c.hover(FOTO, 1.2, at=c.A(2, 'foto', 0.9), label='foto vazia (opcional)')
    c.mark(3)
    # sem o "e-mail" na fala (1.38.21), telefone e cargo ficam a ~1 s um do outro: a cadeia começa mais cedo (nome 1,8 s antes da palavra)
    c.type(CAMPO_NOME, 'Tatiane Ribeiro', at=c.A(3, 'nome', 1.8), cps=30, label='Nome Completo')
    c.type(CAMPO_CPF, '41837290687', at=c.A(3, 'CPF,', 1.4), cps=30, label='CPF')
    c.type(CAMPO_TEL, '2130001008', at=c.A(3, 'telefone', 1.4), cps=30, label='Telefone')
    c.type(CAMPO_CARGO, 'Assistente administrativa', at=c.A(3, 'cargo,', 1.3), cps=30, label='Cargo')
    c.mark(4)
    c.click(CAMPO_END, at=c.A(4, 'endereço', 1.0), label='campo Endereço')
    c.colar('Rua Gavião Peixoto, 120, apto 302, Icaraí, Niterói - RJ', at=c.A(4, 'endereço', 0.1), label='cola o endereço')
    c.click(DATA_ADM, at=c.A(4, 'data', 0.9), label='abre o calendário da Data de Admissão')
    c.click(DIA(3), at=c.A(4, 'admissão.', 0.9), label='escolhe o dia 3 de novembro')
    c.mark(5)
    c.type(CAMPO_PIX, 'tatiane.ribeiro@glacialcold.example', at=c.A(5, 'chave', 0.9), cps=22, label='Chave PIX')
    c.confere_campos(['Tatiane Ribeiro', '418.372.906-87', '(21) 3000-1008', 'Assistente administrativa', 'Rua Gavião Peixoto, 120, apto 302, Icaraí, Niterói - RJ', 'tatiane.ribeiro@glacialcold.example'], 'campos da aba Dados')
    c.confere('dlg', ['03/11/2026'], 'Data de Admissão 03/11/2026')
    c.fim()
    return c


def cap03():
    """Salário e contrato: aba Pagamento, calculadora do custo mensal, regime CLT, CBO, matrícula, vale-transporte."""
    c = cap_novo(3, setup=setup_dados())
    c.mark(1)
    c.click(ABA_FORM('Pagamento'), at=c.A(1, 'Pagamento.', 0.9), label='aba Pagamento')
    c.type(CAMPO_SAL, '280000', at=c.A(1, 'dois', 1.1), cps=14, label='Salário R$ 2.800,00')
    c.mark(2)
    c.hover({'text': 'Custo mensal total', 'within': DLG}, 0.8, at=c.A(2, 'custo', 0.9), label='Custo mensal total')
    c.click(BTN('Calcular', within=DLG), at=c.A(2, 'Calcular', 0.9), label='Calcular')
    c.waitfor(text='Calcular Custo Mensal', timeout=10)
    c.type(CAMPO_TRANSP, '22000', at=c.A(2, 'benefícios,', 1.3), cps=14, label='Transporte R$ 220,00')
    # fase 2: o cursor leva ~1,4 s até o "Custo Total Mensal" (janela da calculadora): sai logo depois da digitação, e o Aplicar pousa no "Aplico"
    c.hover({'text': 'Custo Total Mensal'}, 0.5, at=c.A(2, 'como', 0.9), label='Custo Total Mensal e Hora Homem')
    c.confere('dlg', ['Calcular Custo Mensal', 'Custo Total Mensal', 'Hora Homem'], 'a calculadora mostra o custo total e a hora homem')
    c.mark(3)
    c.click(APLICAR, at=c.A(3, 'Aplico,', 0.6), label='Aplicar o custo')
    c.waitfor(gone={'text': 'Calcular Custo Mensal'}, timeout=8)
    c.confere_campos(['R$ 2.800,00'], 'salário R$ 2.800,00 e custo mensal preenchido')
    c.mark(4)
    c.hover({'text': 'Regime', 'within': DLG, 'exact': True}, 0.6, at=c.A(4, 'regime.', 0.9), label='Regime')
    c.click(BTN('CLT', within=DLG), at=c.A(4, 'CLT.', 0.9), label='CLT')
    c.mark(5)
    c.type(CAMPO_CBO, '4110-10', at=c.A(5, 'CBO', 1.0), cps=22, label='CBO')
    c.type(CAMPO_MAT, '00008', at=c.A(5, 'matrícula', 1.0), cps=22, label='Matrícula')
    c.hover({'text': 'Dependentes (IRRF)', 'within': DLG}, 0.8, at=c.A(5, 'dependentes', 0.9), label='Dependentes (IRRF)')
    c.mark(6)
    c.click(BTN('Sim', within=DLG), at=c.A(6, 'vale-transporte', 0.9), label='Vale-transporte Sim')
    c.type({'selector': f"{DLG} div:has(> label:has-text('Valor mensal do VT')) input"}, '22000', at=c.A(6, 'duzentos', 1.1), cps=14, label='Valor mensal do VT')
    c.confere('dlg', ['Valor mensal do VT', 'CLT', 'CBO', 'Matrícula', 'Dependentes (IRRF)'], 'campos CLT e VT na tela')
    c.fim()
    return c


def cap04():
    """O dia do pagamento: Configuração de Pagamento (mensal, dia útil, 5º dia útil) e a dica."""
    c = cap_novo(4, setup=setup_pagamento())
    c.mark(1)
    c.ev(ROLA_DLG % 420, at=0.1, label='desce até a Configuração de Pagamento')
    c.hover({'text': 'Configuração de Pagamento', 'within': DLG}, 1.0, at=c.A(1, 'configuração', 0.9), label='Configuração de Pagamento')
    c.mark(2)
    c.click(COMBO('Mensal'), at=c.A(2, 'pagar', 0.9), label='abre Frequência (Mensal, Quinzenal, Semanal)')
    c.click(OPT('Mensal'), at=c.A(2, 'semana.', 0.7), label='fica em Mensal')
    c.mark(3)
    c.hover({'selector': f"{DLG} div:has(> label:text-is('N° dia útil do mês')) input"}, 0.9, at=c.A(3, 'quinto', 0.9), label='N° dia útil do mês (5)')
    c.click(COMBO('Dia útil'), at=c.A(3, 'corrido', 1.3), label='abre Tipo de dia (Dia útil, Dia corrido)')
    c.click(OPT('Dia útil'), at=c.A(3, 'mês.', 0.6), label='volta para Dia útil')
    c.mark(4)
    c.hover({'text': 'Valor da folha aparece automaticamente', 'within': DLG}, 1.4, at=c.A(4, 'dica:', 0.9), label='a dica da folha automática')
    c.confere('dlg', ['Frequência', 'Mensal', 'Tipo de dia', 'Dia útil', 'N° dia útil do mês', 'Valor da folha aparece automaticamente em Contas a Pagar conforme essa configuração.'], 'configuração de pagamento na tela')
    c.fim()
    return c


def cap05():
    """Acesso ao sistema (fala nova, 1.38.21; voz `T15 emendas 1.38.21`): aba Acesso SEM vínculo, e-mail, liga "Criar acesso ao sistema"
    (Papel no sistema e Permissões), desliga, vincula a Tatiane, Criar Funcionário."""
    c = cap_novo(5, setup=setup_acesso())
    CHAVE_ACESSO = {'role': 'switch', 'name': 'Criar acesso ao sistema', 'within': DLG}
    c.mark(1)
    c.click(ABA_FORM('Acesso'), at=c.A(1, 'aba', 0.9), label='aba Acesso')
    c.hover(CAMPO_EMAIL, 1.5, at=c.A(1, 'e-mail', 0.9), label='e-mail dela, que serve de login')
    c.confere_campos(['tatiane.ribeiro@glacialcold.example'], 'e-mail preenchido na aba Acesso')
    c.mark(2)
    c.hover({'text': 'Criar acesso ao sistema', 'within': DLG, 'exact': True}, 1.0, at=c.A(2, 'Criar', 0.9), label='Criar acesso ao sistema')
    c.click(CHAVE_ACESSO, at=c.A(2, 'Ligado,', 1.1), label='liga Criar acesso ao sistema')
    c.confere('dlg', ['Papel no sistema', 'Permissões'], 'ligada, a chave mostra Papel no sistema e Permissões')
    c.hover({'text': 'Papel no sistema', 'within': DLG}, 2.0, at=c.A(2, 'Papel', 0.9), label='Papel no sistema e Permissões')
    c.click(CHAVE_ACESSO, at=c.A(2, 'desligo', 0.9), label='desliga Criar acesso ao sistema')
    c.confere_ausente('dlg', 'Papel no sistema', 'desligada, a chave esconde Papel no sistema e Permissões (nenhum acesso criado)', espera=1.5)
    c.click({'selector': f"{DLG} button[role=combobox]", 'nth': 0}, at=c.A(2, 'vinculo:', 0.9), label='abre a lista de usuários')
    c.click(OPT('Tatiane Ribeiro'), at=c.A(2, 'nome', 0.9), label='escolhe Tatiane Ribeiro')
    c.confere('dlg', ['Usuário vinculado: Tatiane Ribeiro'], 'usuária vinculada')
    c.mark(3)
    c.click(BTN('Criar Funcionário'), at=c.A(3, 'Funcionário.', 0.9), label='Criar Funcionário')
    c.waitfor(gone={'role': 'dialog'}, timeout=15)
    c.confere('body', ['Funcionário criado!'], 'aviso Funcionário criado!')
    c.confere('main', ['Tatiane Ribeiro', 'Assistente administrativa'], 'a Tatiane entrou na lista')
    c.fim()
    return c


def cap06():
    """Vale, bônus e falta do Rafael: ficha, três janelas de movimentação, saldo atual."""
    c = cap_novo(6, setup=SETUP_FUNC)
    c.mark(1)
    c.hover(FUNC('Tatiane Ribeiro'), 0.8, at=c.A(1, 'Tatiane', 0.9), label='a lista agora tem a Tatiane')
    c.hover(FUNC('Bruno Alves'), 0.8, at=c.A(1, 'salário', 0.9), label='salário de cada técnico na lista')
    c.confere('main', ['R$ 3.080,00', 'R$ 2.860,00', 'R$ 2.640,00', 'R$ 2.800,00', 'Tatiane Ribeiro'], 'a lista mostra o salário de cada um (Tatiane R$ 2.800,00; técnicos R$ 2.640 a 3.080)')
    c.mark(2)
    c.click(FUNC('Rafael Lima'), at=c.A(2, 'Rafael,', 0.9), label='Rafael Lima')
    c.hover(P('Movimentações'), 1.0, at=c.A(2, 'movimentações,', 0.9), label='faixa Movimentações')
    c.hover(P('Saldo atual'), 1.2, at=c.A(2, 'saldo', 0.9), label='salário e saldo atual')
    c.confere('main', ['Rafael Lima', 'Informal', 'Vale', 'Bônus', 'Falta', 'Pagamento', 'Salário', 'R$ 3.080,00', 'Saldo atual'], 'ficha do Rafael: salário R$ 3.080,00')
    c.mark(3)
    c.click(MOV('Vale'), at=c.A(3, 'Vale,', 0.9), label='Vale')
    c.click(COMBO('Caixa'), at=c.A(3, 'conta', 0.9), label='abre "De qual conta sai o vale?"')
    c.click(OPT('Caixa (em dinheiro)'), at=c.A(3, 'caixa,', 0.9), label='escolhe Caixa (em dinheiro)')
    c.type(MOEDA(0), '30000', at=c.A(3, 'valor.', 2.0), cps=14, label='valor R$ 300,00')
    c.click(TEXTAREA, at=c.A(3, 'valor.', 0.8), label='campo Descrição')
    c.colar('Adiantamento', at=c.A(3, 'valor.', 0.5), label='descrição Adiantamento')
    c.confere('dlg', ['Registrar Vale', 'Saldo atual: R$ 3.080,00', 'De qual conta sai o vale?', 'Caixa (em dinheiro)'], 'janela Registrar Vale com saldo R$ 3.080,00')
    c.mark(4)
    c.click(BTN('Registrar Vale'), at=c.A(4, 'Registrar', 1.0), label='Registrar Vale')
    c.confere('body', ['Vale registrado!'], 'aviso Vale registrado!')
    c.waitfor(gone={'role': 'dialog'}, timeout=10)
    c.hover(P('Vales'), 1.2, at=c.A(4, 'caixa', 0.9), label='Vales na ficha')
    c.mark(5)
    c.click(MOV('Bônus'), at=c.A(5, 'bônus', 0.9), label='Bônus')
    c.type(MOEDA(0), '15000', at=c.A(5, 'cento', 1.2), cps=14, label='valor R$ 150,00')
    c.click(TEXTAREA, at=c.A(5, 'cinquenta', 0.9), label='campo Descrição')
    c.colar('Bônus por produtividade', at=c.A(5, 'produtividade.', 1.3), label='descrição Bônus por produtividade')
    c.click(BTN('Registrar Bônus'), at=c.A(5, 'produtividade.', 0.4), label='Registrar Bônus')
    c.confere('body', ['Movimentação registrada!'], 'aviso Movimentação registrada! (bônus)')
    c.waitfor(gone={'role': 'dialog'}, timeout=10)
    c.mark(6)
    c.click(MOV('Falta'), at=c.A(6, 'falta.', 0.9), label='Falta')
    c.hover(P('Descontar do salário', within=DLG), 1.0, at=c.A(6, 'Descontar', 0.9), label='Descontar do salário')
    c.hover(MOEDA(0), 1.2, at=c.A(6, 'valor', 0.9), label='valor de um dia já calculado')
    c.confere_campos(['R$ 140,00'], 'a falta já vem com R$ 140,00')
    c.confere('dlg', ['Sugestão: R$ 140,00/dia', 'Descontar do salário'], 'sugestão R$ 140,00/dia')
    c.click(TEXTAREA, at=c.A(6, 'quarenta', 1.0), label='campo Descrição')
    c.colar('Falta em 06/11', at=c.A(6, 'quarenta', 0.3), label='descrição Falta em 06/11')
    c.click(BTN('Registrar Falta'), at=c.A(6, 'reais.', 0.3), label='Registrar Falta')
    c.confere('body', ['Movimentação registrada!'], 'aviso Movimentação registrada! (falta)')
    c.waitfor(gone={'role': 'dialog'}, timeout=10)
    c.mark(7, antecipa=0.3)   # o "Registrar Falta" fecha o "reais." da linha 6 e o aviso termina ~0,3 s depois do início da linha 7
    c.hover(P('Saldo atual'), 1.4, at=c.A(7, 'saldo', 0.9), label='Saldo atual')
    c.hover(P('Faltas'), 0.8, at=c.A(7, 'falta', 0.9), label='Vales, Bônus e Faltas')
    c.confere('main', ['Saldo atual', 'R$ 2.790,00', 'Vales', 'R$ 300,00', 'Bônus', 'R$ 150,00', 'Faltas', 'R$ 140,00'], 'saldo atual R$ 2.790,00 = 3.080 - 300 + 150 - 140')
    c.fim()
    return c


def cap07():
    """O pagamento: informal do Rafael (R$ 2.790,00), Extrato, CLT da Tatiane (cancelado)."""
    c = cap_novo(7, setup=SETUP_FUNC + [{'do': 'click', 'target': FUNC('Rafael Lima')}, {'do': 'waitFor', 'text': 'Movimentações', 'timeout': 10}, {'do': 'pause', 'seconds': 0.6}])
    c.mark(1)
    c.click(MOV('Pagamento'), at=c.A(1, 'Pagamento.', 0.9), label='Pagamento')
    c.hover({'text': 'Tipo de pagamento', 'within': DLG}, 1.0, at=c.A(1, 'regime', 0.9), label='abre no regime Normal / Informal')
    c.hover({'text': 'Descontar dos Vales', 'within': DLG}, 1.0, at=c.A(1, 'vale', 0.9), label='Descontar dos Vales (100%)')
    c.hover({'text': 'Pagar com', 'within': DLG}, 1.0, at=c.A(1, 'Conta', 0.9), label='Pagar com Conta Principal')
    c.confere('dlg', ['Pagamento, Rafael Lima', 'Normal / Informal', 'Total de vales: R$ 300,00, Padrão: 100%', 'Conta Principal', 'R$ 20.525,00'], 'janela Pagamento do Rafael: vales R$ 300,00 e Conta Principal R$ 20.525,00')
    c.mark(2)
    c.hover({'text': 'Subtotal', 'within': DLG}, 1.0, at=c.A(2, 'resumo:', 0.9), label='resumo do pagamento')
    c.hover({'text': 'Valor a Pagar', 'within': DLG}, 1.2, at=c.A(2, 'Ficam', 0.9), label='Valor a Pagar')
    c.confere('dlg', ['Salário', 'R$ 3.080,00', 'Total de Bônus', 'R$ 150,00', 'Vales', 'R$ 300,00', 'Faltas', 'R$ 140,00', 'Subtotal', 'R$ 2.790,00', 'Valor a Pagar'], 'resumo: valor a pagar R$ 2.790,00')
    c.mark(3)
    c.click(BTN('Confirmar Pagamento'), at=c.A(3, 'Confirmo,', 0.9), label='Confirmar Pagamento')
    c.waitfor(text='Deseja gerar Recibo?', timeout=10)
    c.click(BTN('Não'), at=c.A(3, 'Agora', 0.9), label='Recibo: Não')
    c.waitfor(gone={'text': 'Deseja gerar Recibo?'}, timeout=10)
    c.mark(4)
    c.click(MOV('Extrato'), at=c.A(4, 'Extrato', 0.9), label='Extrato')
    c.waitfor(text='Saldo após', timeout=10)
    c.hover({'text': 'Saldo após', 'within': DLG}, 1.0, at=c.A(4, 'saldo', 0.9), label='Saldo após de cada movimento')
    c.hover({'text': 'Gerar Recibo', 'within': DLG}, 1.2, at=c.A(4, 'Gerar', 0.9), label='Gerar Recibo no pagamento')
    c.confere('dlg', ['Extrato, Rafael Lima', 'Vale', 'Bônus', 'Falta', 'Pagamento', 'Ajuste', 'Saldo após', 'Gerar Recibo'], 'extrato com vale, bônus, falta, pagamento e ajuste')
    fechar_janela(c, at=c.A(4, 'quiser.', 0.6))
    c.mark(5)
    c.click(FUNC('Tatiane Ribeiro'), at=c.A(5, 'Tatiane,', 0.9), label='Tatiane Ribeiro')
    c.click(MOV('Pagamento'), at=c.A(5, 'janela', 1.0), label='Pagamento (modo CLT)')
    c.hover({'text': 'Proventos', 'within': DLG}, 0.8, at=c.A(5, 'modo', 0.9), label='Proventos')
    c.hover({'text': 'INSS', 'within': DLG, 'exact': True}, 0.5, at=c.A(5, 'INSS,', 0.9), label='INSS')
    c.hover({'text': 'IRRF', 'within': DLG, 'exact': True}, 0.5, at=c.A(5, 'imposto', 0.9), label='IRRF')
    c.hover({'text': 'Vale-transporte', 'within': DLG, 'exact': True}, 0.5, at=c.A(5, 'vale-transporte', 0.9), label='Vale-transporte')
    c.hover({'text': 'Líquido a pagar', 'within': DLG}, 1.0, at=c.A(5, 'líquido', 0.9), label='Líquido a pagar')
    c.confere('dlg', ['Pagamento, Tatiane Ribeiro', 'CLT', 'Proventos', 'Descontos', 'INSS', 'IRRF', 'Vale-transporte', 'Líquido a pagar', 'Conta Principal', 'R$ 17.735,00'], 'modo CLT da Tatiane; Conta Principal R$ 17.735,00')
    c.mark(6)
    c.hover({'text': 'Valores calculados com base nas tabelas vigentes', 'within': DLG}, 1.5, at=c.A(6, 'dica:', 0.9), label='aviso: confira com o contador')
    c.click(BTN('Cancelar'), at=c.A(6, 'cancelo.', 0.9), label='Cancelar o pagamento da Tatiane')
    c.waitfor(gone={'role': 'dialog'}, timeout=10)
    c.fim()
    return c


def cap08():
    """As regras do ponto: Controle de Ponto > Config, selfie desligada, salvar, quiosque, Jornada Individual."""
    c = cap_novo(8, setup=SETUP_FUNC)
    c.mark(1)
    c.click(ABA_FUNC('Controle de Ponto'), at=c.A(1, 'Controle', 0.9), label='Controle de Ponto')
    c.click(TAB('Config'), at=c.A(1, 'Config,', 0.9), label='Config')
    c.hover(P('Jornada Padrão da Empresa'), 0.8, at=c.A(1, 'jornada', 0.9), label='Jornada Padrão da Empresa')
    c.hover(P('Entrada padrão'), 0.5, at=c.A(1, 'oito', 0.9), label='Entrada padrão')
    c.hover(P('Saída padrão'), 0.5, at=c.A(1, 'cinco,', 0.9), label='Saída padrão')
    c.hover(P('Intervalo (min)'), 0.6, at=c.A(1, 'hora', 0.9), label='Intervalo 60 min')
    c.mark(2)
    c.hover(P('Exigir selfie'), 0.7, at=c.A(2, 'selfie', 0.9), label='Exigir selfie')
    c.hover(P('Exigir geolocalização'), 0.7, at=c.A(2, 'localização.', 0.9), label='Exigir geolocalização')
    c.click(CHAVE('Exigir selfie'), at=c.A(2, 'Glacial', 0.9), label='desliga Exigir selfie')
    c.mark(3)
    c.rolar(260, at=c.A(3, 'pra', 0.9), label='desce até a madrugada')
    c.hover(P('Batidas da madrugada'), 1.2, at=c.A(3, 'madrugada', 0.9), label='Batidas da madrugada')
    c.mark(4)
    c.click(BTN('Salvar configurações'), at=c.A(4, 'Salvar', 0.9), label='Salvar configurações')
    c.confere('body', ['Configurações salvas!'], 'aviso Configurações salvas!')
    c.mark(5)
    c.rolar(600, at=c.A(5, 'Se', 0.9), label='desce até o ponto em grupo')
    c.hover(P('Ponto em grupo (quiosque)'), 1.5, at=c.A(5, 'grupo:', 0.9), label='Ponto em grupo (quiosque)')
    c.mark(6)
    c.rolar(600, at=c.A(6, 'E', 0.9), label='desce até a Jornada Individual')
    c.hover(P('Jornada Individual'), 1.0, at=c.A(6, 'Jornada', 0.9), label='Jornada Individual')
    c.hover(TBTN('Bruno Alves', 0), 1.0, at=c.A(6, 'horário,', 0.9), label='lápis de uma linha da jornada', optional=True)
    c.fim()
    return c


def cap09():
    """O ponto no celular, parte 1 (computador): Editar a Tatiane > Ponto eletrônico > Ativado > Salvar > link de ativação copiado.
    A parte do celular (linhas 4 a 7) é o `cap09b`. Este trecho acaba no início da linha 4."""
    c = cap_novo(9, setup=SETUP_FUNC + [{'do': 'eval', 'js': "navigator.clipboard && (navigator.clipboard.writeText = () => Promise.resolve()); 1"}])
    c.mark(1)
    c.click(FUNC('Tatiane Ribeiro'), at=c.A(1, 'Tatiane.', 1.0), label='Tatiane Ribeiro')
    c.click(MOV('Editar'), at=c.A(1, 'Editar', 0.9), label='Editar')
    c.click(ABA_FORM('Ponto eletrônico'), at=c.A(1, 'Ponto', 0.9, nth=1), label='aba Ponto eletrônico')
    c.click(BTN('Ativado', within=DLG), at=c.A(1, 'ativar.', 0.9), label='Ativado')
    c.mark(2)
    c.hover({'text': 'PIN do ponto', 'within': DLG}, 1.2, at=c.A(2, 'PIN,', 0.9), label='PIN do ponto')
    c.hover({'text': 'Acesso individual ao ponto', 'within': DLG}, 1.2, at=c.A(2, 'acesso', 0.9), label='Acesso individual ao ponto')
    c.confere('dlg', ['PIN do ponto', 'Acesso individual ao ponto'], 'blocos PIN e acesso individual depois de ativar')
    c.mark(3)
    c.click(BTN('Salvar', within=DLG), at=c.A(3, 'Salvo,', 0.9), label='Salvar')
    c.confere('body', ['Link de ativação copiado!'], 'aviso Link de ativação copiado!')
    c.dur = c.L(4)      # a edição junta este trecho (até o início da linha 4) com o cap09b (celular)
    c.fim()
    return c


TOKEN_TATIANE = hashlib.sha256('t15-ativacao:Tatiane Ribeiro'.encode()).hexdigest()   # o mesmo token que o RPC create_employee_face_enrollment_link devolve


def cap09b():
    """O ponto no celular, parte 2 (celular, sem login): cadastro facial > Continuar sem biometria > ponto > Registrar Entrada > Confirmar registro.
    É a voz do cap. 9 a partir da linha 4: aqui as linhas se chamam L1..L4 (= L4..L7 do cap. 9) e os tempos são contados do início da linha 4."""
    c = Cap(9, pace=0.5, start=(195, 420), nome='cap09b', device='phone', anonymous=True, sem=['apos-cap09'], setup=[
        {'do': 'geo', 'lat': -22.90240, 'lng': -43.11094},
        {'do': 'clock', 'set': '2026-11-11T09:02:00-03:00'},
        {'do': 'goto', 'url': f'/ativar-ponto/{TOKEN_TATIANE}'}, {'do': 'waitFor', 'text': 'Cadastro facial', 'timeout': 25}, AGUARDA,
    ])
    off = c.L(4)
    c.voz_inicio = off
    c.words = [dict(w, s=round(w['s'] - off, 2), linha=w['linha'] - 3) for w in c.words if w['linha'] >= 3]
    c.linhas = [dict(l, s=round(l['s'] - off, 2), e=round(l['e'] - off, 2)) for l in c.linhas[3:]]
    c.dur = round(c.dur - off, 2)
    c.mark(1)
    c.hover(P('Olá, Tatiane', within='body'), 1.0, at=c.A(1, 'cadastro', 0.9), label='Cadastro facial: Olá, Tatiane')
    c.click(BTN('Continuar sem biometria', noScroll=True), at=c.A(1, 'Continuar', 0.9), label='Continuar sem biometria')
    c.waitfor(text='Você ainda não bateu o ponto hoje', timeout=20)
    c.mark(2)
    c.hover(P('Tatiane Ribeiro', within='body'), 1.2, at=c.A(2, 'nome,', 0.9), label='nome, cargo e marca da empresa')
    c.mark(3)
    c.click(BTN('Registrar Entrada', noScroll=True), at=c.A(3, 'Registrar', 0.9), label='Registrar Entrada')
    c.waitfor(text='Confirmar registro', timeout=15)
    c.confere('body', ['Tipo', 'Horário', 'Local', 'Confirmar registro'], 'resumo da batida: tipo, horário e local')
    c.hover(P('Local', within='body'), 1.2, at=c.A(3, 'local.', 0.9), label='Local da batida')
    c.mark(4)
    c.click(BTN('Confirmar registro', noScroll=True), at=c.A(4, 'Confirmar', 0.9), label='Confirmar registro')
    c.confere('body', ['Entrada registrada'], 'aviso Entrada registrada')
    c.confere('body', ['Registros de hoje', 'Iniciar Intervalo'], 'registros de hoje e botão Iniciar Intervalo')
    c.fim()
    return c


def cap10():
    """Acompanhando o ponto: Hoje (olho e lápis), Histórico (Filtros e CSV), Relatório."""
    c = cap_novo(10, setup=SETUP_FUNC + [{'do': 'clock', 'set': '2026-11-11T09:10:00-03:00'}, {'do': 'pause', 'seconds': 0.4}])
    c.mark(1)
    c.click(ABA_FUNC('Controle de Ponto'), at=c.A(1, 'escritório,', 0.9), label='Controle de Ponto')
    c.waitfor(text='Presentes', timeout=15)
    c.hover(FUNC('Tatiane Ribeiro'), 1.4, at=c.A(1, 'Tatiane', 0.9), label='linha da Tatiane: entrada e Presente')
    c.confere('main', ['Presentes', 'Tatiane Ribeiro', 'Presente', '09:02'], 'Hoje: Tatiane presente, entrada 09:02')
    c.mark(2)
    c.click(TBTN('Tatiane', 0), at=c.A(2, 'olho', 0.9), label='olho da linha')
    c.waitfor(text='Registros do dia', timeout=10)
    c.hover({'text': 'Rua Moreira César', 'within': DLG}, 0.7, at=c.A(2, 'endereço', 0.9), label='endereço da batida')
    c.confere('dlg', ['Registros do dia, Tatiane Ribeiro', 'Entrada', 'Trabalhado', 'Intervalo', 'Saldo'], 'registros do dia com o endereço')
    fechar_janela(c, at=c.A(2, 'batida.', 0.2))
    c.mark(3)
    c.click(TBTN('Tatiane', 1), at=c.A(3, 'lápis', 0.9), label='lápis da linha')
    c.waitfor(text='Registro manual', timeout=10)
    # fase 2: nesta tela cada gesto leva 1,3 a 2 s até o alvo (o "Histórico" ~2 s): justificativa e Cancelar saem mais cedo, para o Histórico não atrasar
    c.hover({'text': 'Justificativa', 'within': DLG}, 0.9, at=c.A(3, 'escreve', 0.9), label='Justificativa (obrigatória)')
    c.confere('dlg', ['Registro manual, Tatiane Ribeiro', 'Tipo de registro', 'Horário', 'Justificativa *'], 'registro manual: tipo, horário e justificativa (sem campo Data)')
    c.click(BTN('Cancelar'), at=c.A(3, 'obrigatória.', 0.9), label='Cancelar o registro manual')
    c.waitfor(gone={'role': 'dialog'}, timeout=10)
    c.mark(4)
    c.click(TAB('Histórico'), at=c.A(4, 'Histórico', 0.9), label='Histórico')
    c.waitfor(text='registro', timeout=10)
    c.click(BTNX('Filtros'), at=c.A(4, 'filtro', 0.9), label='Filtros (funcionário, período e status)')
    c.confere('body', ['Funcionário', 'Período', 'Status'], 'painel de filtros')
    c.press('Escape', at=c.A(4, 'período,', 0.5), label='fecha os filtros')
    c.hover(BTN('CSV'), 1.2, at=c.A(4, 'CSV', 0.9), label='botão CSV (sem baixar)')
    c.mark(5)
    c.click(TAB('Relatório'), at=c.A(5, 'Relatório', 0.9), label='Relatório')
    c.waitfor(text='Calendário', timeout=10)
    c.hover(P('Calendário'), 0.6, at=c.A(5, 'calendário,', 0.9), label='Calendário do mês')
    c.hover(P('Horas por dia'), 1.0, at=c.A(5, 'horas', 0.9), label='Horas por dia')
    c.confere('main', ['Calendário', 'Horas por dia'], 'relatório: calendário e horas por dia')
    c.click(BTNX('Filtros'), at=c.A(5, 'Filtrando', 0.9), label='Filtros do relatório')
    c.click({'text': 'Tatiane Ribeiro', 'within': DLG}, at=c.A(5, 'pessoa,', 1.1), label='filtra a Tatiane')
    c.press('Escape', at=c.A(5, 'você', 0.3), label='fecha os filtros')
    c.hover(P('Saldo do mês'), 1.4, at=c.A(5, 'saldo', 0.9), label='saldo do mês da Tatiane')
    c.confere('main', ['Relatório de Tatiane Ribeiro', 'Dias trabalhados', 'Total trabalhado', 'Saldo do mês'], 'filtrando a Tatiane aparece o saldo do mês')
    c.fim()
    return c


def cap11():
    """A folha em Contas a Pagar (12/11, de manhã): Financeiro > Contas a Pagar/Receber > A Pagar > busca "Folha" > Marcar como pago > Cancelar."""
    c = cap_novo(11, setup=SETUP_DASH, prewarm=['/dashboard', '/financeiro/contas'])
    c.mark(1)
    c.click(BTN('Financeiro'), at=c.A(1, 'folha', 0.9), label='grupo Financeiro do menu')
    c.click(MENU_CONTAS, at=c.A(1, 'Contas', 0.9), label='Contas a Pagar/Receber')
    c.waitfor(text='Contas a pagar e a receber', timeout=20)
    # fase 2: Contas a Pagar/Receber fica clicável entre 5,6 e 6,0 s (duas tomadas): a aba e a busca ancoram no que a tela permite
    c.click(TAB('A Pagar'), at=c.A(1, 'Procuro', 0.3), label='aba A Pagar')
    c.type({'placeholder': 'Buscar por nome, descrição, categoria ou valor...'}, 'Folha', at=c.A(1, 'folha', 0.2, nth=1), cps=12, label='busca "Folha"')
    c.waitfor(text='Folha Rafael Lima', timeout=10)
    c.mark(2)
    c.hover(P('Folha Rafael Lima'), 1.0, at=c.A(2, 'folha', 0.9), label='folha de cada um')
    c.hover(P('07/12/2026'), 1.2, at=c.A(2, 'quinto', 0.9), label='vencimento 07/12/2026')
    c.confere('main', ['Folha Rafael Lima — 2026-12', 'Folha de Pagamento', '07/12/2026', 'R$ 3.080,00', 'Pendente', 'Folha Tatiane Ribeiro — 2026-12', 'R$ 2.800,00'], 'as folhas de dezembro, vencimento 07/12/2026')
    c.mark(3)
    c.abrir_menu('Rafael Lima', 'Marcar como pago', at=c.A(3, 'Marcar', 1.4), label='menu ⋮ da folha do Rafael')
    c.click(ITEM('Marcar como pago'), at=c.A(3, 'pago', 0.9), label='Marcar como pago')
    c.waitfor(text='Quitando folha pendente', timeout=10)
    c.hover({'text': 'Quitando folha pendente', 'within': DLG}, 0.8, at=c.A(3, 'quitando', 0.5), label='Quitando folha pendente, período 2026-12')
    c.confere('dlg', ['Pagamento, Rafael Lima', 'Quitando folha pendente, período 2026-12'], 'janela de pagamento quitando a folha de 2026-12')
    c.mark(4)
    c.click(BTN('Cancelar'), at=c.A(4, 'cancelo.', 0.9), label='Cancelar')
    c.waitfor(gone={'role': 'dialog'}, timeout=10)
    c.fim()
    return c


def cap12():
    """Recapitulando (12/11): passa pelas telas do tutorial, só leitura."""
    # aquece também Contas a Pagar/Receber (fora do vídeo), como o cap. 11: a frio, o "A Pagar" levou 3 s para ficar clicável (fase 2)
    c = cap_novo(12, setup=SETUP_FUNC, prewarm=['/dashboard', '/financeiro/contas', '/funcionarios'])
    c.mark(1)
    c.click(FUNC('Tatiane Ribeiro'), at=c.A(1, 'Tatiane', 0.9), label='ficha da Tatiane (CLT, Controle de Ponto)')
    c.click(MOV('Editar'), at=c.A(1, 'salário,', 1.2), label='Editar')
    c.click(ABA_FORM('Pagamento'), at=c.A(1, 'custo', 0.9), label='aba Pagamento')
    c.hover({'text': 'Regime', 'within': DLG, 'exact': True}, 0.8, at=c.A(1, 'regime', 0.9), label='regime CLT')
    fechar_janela(c, at=c.A(1, 'vinculou', 0.4))
    c.mark(2)
    c.click(FUNC('Rafael Lima'), at=c.A(2, 'Rafael,', 0.9), label='ficha do Rafael')
    c.hover(P('Saldo atual'), 1.0, at=c.A(2, 'vale,', 0.9), label='vale, bônus e falta')
    c.click(MOV('Extrato'), at=c.A(2, 'extrato.', 1.0), label='Extrato')
    c.waitfor(text='Saldo após', timeout=10)
    fechar_janela(c, at=c.A(2, 'extrato.', 0.1))
    c.mark(3)
    c.click(ABA_FUNC('Controle de Ponto'), at=c.A(3, 'regras', 0.9), label='Controle de Ponto')
    c.click(TAB('Config'), at=c.A(3, 'ponto,', 0.9), label='Config')
    c.click(TAB('Hoje'), at=c.A(3, 'Hoje,', 0.9), label='Hoje')
    c.click(TAB('Histórico'), at=c.A(3, 'Histórico', 0.9), label='Histórico')
    c.click(TAB('Relatório'), at=c.A(3, 'Relatório.', 0.9), label='Relatório')
    c.mark(4)
    c.ev("(()=>{history.pushState({},'','/financeiro/contas');window.dispatchEvent(new PopStateEvent('popstate'));return location.pathname})()", at=c.A(4, 'folha', 1.2), label='vai para Contas a Pagar')
    c.waitfor(text='Contas a pagar e a receber', timeout=20)
    c.click(TAB('A Pagar'), at=c.A(4, 'sozinha', 0.9), label='aba A Pagar')
    c.type({'placeholder': 'Buscar por nome, descrição, categoria ou valor...'}, 'Folha', at=c.A(4, 'Contas', 0.9), cps=10, label='busca "Folha"')
    c.mark(5)
    c.hover(P('Folha Rafael Lima'), 1.2, at=c.A(5, 'Com', 0.9), label='as folhas, fim do tutorial')
    c.fim()
    return c


CAPS = {str(n): globals()[f'cap{n:02d}'] for n in range(13) if f'cap{n:02d}' in globals()}
if 'cap09b' in globals():
    CAPS['9b'] = globals()['cap09b']

if __name__ == '__main__':
    quais = [a.lstrip('0') or '0' for a in sys.argv[1:]] or sorted(CAPS, key=lambda k: (int(k.rstrip('b')), k))
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
                    print(f'  aviso {c.nome}: at {stp["at"]} < {last} em "{stp.get("label") or stp.get("name")}"')
                last = max(last, stp['at'])
        path = os.path.join(HERE, f'{c.nome}.json')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
        print(f'{c.nome}: {len(d["steps"])} passos, narração {c.dur:.1f} s -> {os.path.relpath(path, HERE)}')
