#!/usr/bin/env python3
"""T10 · gera rec/t10/cap00..cap10.json (roteiros do robô) a partir da narração (t10/narracao/capNN.json) ou, ENQUANTO A VOZ NÃO EXISTE,
de tempos PROVISÓRIOS estimados do texto de planejamento/domiflix/T10/narracao/tts_textos.py (a fonte): ~2,6 palavras/s e 0,5 s de pausa entre
linhas ("[pause]" no meio de uma linha = 0,6 s). Roteiro provisório leva "PROVISÓRIO" no título e serve ao ensaio (--rapido, sem `at`) e a conferir
seletores e estado; NÃO serve para gravar. Quando a voz chegar: `python3 -I rec/t10/gerar.py` de novo (lê os capNN.json e usa os tempos reais).

Aula inteira no COMPUTADOR (janela 1280x800, 2x), logada como Camila Duarte (admin, Glacial Cold Brasil), na Dominex 1.38.19, FAKE_NOW 03/11/2026 09:00.
Os `at` saem da palavra que anuncia cada passo (A(linha, palavra, folga)): o gesto "pousa" ~0,7 a 1 s depois do início do passo
(clique = deslocamento + ~0,85 s; digitação = clique + texto), então `at` = início da palavra - folga. As palavras são buscadas pela GRAFIA DA LEGENDA
(`w` do capNN.json: CRM, Lead, Webhook, PMOC), como no T9/T12.
Rodar de qualquer pasta: `python3 -I rec/t10/gerar.py [NN ...]`. Depois: `node rec/record.mjs rec/t10/capNN.json --check`.

Cadeia de sementes: rec/t10/cadeia.json (gerado por rec/t10/semear.py: fim do T9 + CRM vazio + trilha Domiflix sem introdução = `t10/inicio`) e, a cada
capítulo, o último `t10/apos-capNN` do capítulo anterior que mexeu no banco (SEMENTE abaixo). O `apos-capNN` de cada capítulo sai do ensaio
(`rec/t10/snap.mjs diff NN`, na mesma trava); o `apos-cap03` ganha as 3 oportunidades do corte (`rec/t10/corte.py`).

Particularidades (lições deste tutorial, ver docs/08-licoes.md):
 - Todo capítulo começa pelo /dashboard (o 1º clique custa ~4 s: encadear o começo com `at` fixos já com esse custo).
 - Menu lateral RECOLHIDO ("Toggle Sidebar") do cap. 1 em diante: o quadro tem seis colunas de 300 px e a 1280 px só cabem ~4 com o menu aberto.
 - Observador `OBS`: guarda em `window.__avisos` todo aviso de erro do app, tela escura e faixa da trilha Domiflix; o eval final devolve (tem de sair vazio).
 - O arrasto nativo (HTML5) de cards e de linhas funciona com `drag` do robô; antes de arrastar para uma coluna fora da janela, o quadro rola na horizontal.
 - Não clicar: lixeira da oportunidade e troca de funil (confirm() do navegador), "WhatsApp" (abre outra aba), "Criar OS", "Criar Tarefa",
   "Sim, lançar receita", "Personalizar estágios".
"""
import json
import os
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TUT = os.path.normpath(os.path.join(HERE, '..', '..'))
NARR = os.path.join(TUT, 't10', 'narracao')
TTS = os.path.normpath(os.path.join(TUT, '..', 'claude-tutorials', 'planejamento', 'domiflix', 'T10', 'narracao', 'tts_textos.py'))
CFG = os.path.normpath(os.path.join(os.path.dirname(TTS), 'config_narracao.json'))
CAD = json.load(open(os.path.join(HERE, 'cadeia.json'), encoding='utf8'))
BASE = CAD['inicio']
STORAGE = {'dominex:portal-tickets-seen:d40f5787-1779-501f-900c-ddb2b90a36e5': '2031-01-01T00:00:00.000Z'}
PALAVRAS_POR_S = 2.6
PAUSA_LINHA = 0.5
PAUSA_TAG = 0.6

# Observador de avisos de erro na tela (aceite): guarda em window.__avisos todo texto que apareça com "Não foi possível", "erro",
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

NOMES = ['Abertura', 'O funil começa aqui', 'Ajustando as etapas', 'A primeira oportunidade', 'Andando no funil', 'Quando o cliente fecha',
         'Tudo do negócio num lugar', 'Achando rápido', 'Contatos que chegam sozinhos', 'Acompanhando a obra', 'Recapitulando']
# estado de partida de cada capítulo: o último apos-capNN (de capítulo anterior) que mexeu no banco. O cap. 7 só lê; o cap. 8 parte do mesmo estado dele.
SEMENTE = {0: None, 1: None, 2: 'apos-cap01', 3: 'apos-cap02', 4: 'apos-cap03', 5: 'apos-cap04', 6: 'apos-cap05', 7: 'apos-cap06', 8: 'apos-cap06',
           9: 'apos-cap08', 10: 'apos-cap09'}


def norm(s):
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode().lower()
    return ''.join(ch for ch in s if ch.isalnum() or ch in '?')


# ---------------------------------------------------------------- narração (real ou provisória)
def _legenda(tok, trocas):
    """grafia da legenda de uma palavra falada (cê-érre-ême -> CRM, Lide -> Lead...), preservando a pontuação do fim"""
    fim = ''
    core = tok
    while core and not core[-1].isalnum():
        fim = core[-1] + fim
        core = core[:-1]
    for de, para in trocas:
        if core.lower() == de.lower() and ' ' not in de:
            return para + fim
    return tok


def _provisoria(n):
    import importlib.util
    spec = importlib.util.spec_from_file_location('tts_textos', TTS)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    trocas = json.load(open(CFG, encoding='utf8'))['trocas']
    t = 0.0
    words, linhas = [], []
    for i, texto in enumerate([x for x in mod.CAPS[n].split('\n') if x.strip()]):
        ini = t
        for tok in texto.split():
            if tok == '[pause]':
                t += PAUSA_TAG
                continue
            dur = 1.0 / PALAVRAS_POR_S
            words.append({'w': _legenda(tok, trocas), 'fala': tok, 'linha': i, 's': round(t, 3), 'e': round(t + dur, 3), 'ok': 1.0})
            t += dur
        linhas.append({'i': i, 'texto': texto.replace('[pause]', '').strip(), 's': round(ini, 3), 'e': round(t, 3)})
        t += PAUSA_LINHA
    return {'cap': n, 'dur': round(t, 2), 'words': words, 'linhas': linhas, 'provisoria': True}


def narracao(n):
    """t10/narracao/capNN.json (voz real) quando existir; senão os tempos PROVISÓRIOS estimados do texto"""
    p = os.path.join(NARR, f'cap{n:02d}.json')
    if os.path.exists(p):
        return json.load(open(p, encoding='utf8'))
    return _provisoria(n)


class Cap:
    def __init__(s, n, pace=0.5, cps=9, start=(760, 420), prewarm=None, setup=None, user=None):
        s.n = n
        d = narracao(n)
        s.words, s.linhas, s.dur = d['words'], d['linhas'], d['dur']
        s.provisoria = bool(d.get('provisoria'))
        s.steps = []
        s.pace, s.cps, s.start = pace, cps, start
        s.prewarm = prewarm or ['/dashboard', '/crm']
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
        prov = ' · PROVISÓRIO: tempos estimados do texto, sem a voz' if s.provisoria else ''
        d = {
            'name': f't10-cap{s.n:02d}',
            'title': f'T10 · Cap. {s.n} · {NOMES[s.n]} (narração {str(round(s.dur, 1)).replace(".", ",")} s{prov}; marcas L1..L{len(s.linhas)} = início de cada linha do roteiro)',
            'seed': f't10-cap{s.n:02d}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
            'start': {'x': s.start[0], 'y': s.start[1]},
            'seedExtra': list(BASE) + ([f't10/{sem}'] if sem else []),
            'prewarm': s.prewarm, 'setup': s.setup, 'steps': s.steps,
            'storage': dict(STORAGE),
        }
        if s.user:
            d['user'] = s.user
        return d


# ---------------------------------------------------------------- alvos
BTN = lambda n, **kw: {'role': 'button', 'name': n, 'exact': True, **kw}
BTNX = lambda n, **kw: {'role': 'button', 'name': n, **kw}               # nome por substring
LINK = lambda n, **kw: {'role': 'link', 'name': n, 'exact': True, **kw}
TAB = lambda n, **kw: {'role': 'tab', 'name': n, 'exact': True, **kw}
TXT = lambda t, **kw: {'text': t, 'exact': True, **kw}                    # texto INTEIRO igual (e na mesma caixa)
P = lambda t, **kw: {'text': t, 'within': 'main', **kw}                   # texto por substring, sem diferenciar caixa
SEL = lambda s, **kw: {'selector': s, **kw}
DLG = '[role=dialog]'
PD = lambda t, **kw: {'text': t, 'within': DLG, **kw}                     # texto por substring DENTRO da janela aberta
POP = '[data-radix-popper-content-wrapper]'
OPT = lambda n, **kw: {'role': 'option', 'name': n, **kw}
ITEM = lambda n, **kw: {'role': 'menuitem', 'name': n, **kw}
AGUARDA = {'do': 'waitFor', 'idle': True}
SW = lambda n, **kw: {'role': 'switch', 'name': n, 'exact': True, **kw}


# ---------------------------------------------------------------- alvos do CRM/Projetos (1.38.19)
GRUPO = BTN('CRM e Projetos')   # grupo do menu lateral (abre a lista)
MENU_LATERAL = {'role': 'button', 'name': 'Toggle Sidebar', 'nth': 0}
CRM_KANBAN = LINK('CRM/Kanban')
PROJETOS = LINK('Projetos')
NOVA_OPORT = BTN('Nova oportunidade')
CONFIG_CRM = BTN('Configurações do CRM/Kanban')
BUSCA = {'placeholder': 'Buscar por título, cliente, telefone ou documento...'}
BOARD = 'main div.overflow-x-auto.pb-4'                                              # faixa com as colunas do funil
COLUNA = lambda nome: {'selector': 'main [draggable=true]', 'hasText': nome}  # cabeçalho (arrastável) da coluna: também é alvo de soltar
CARD = lambda titulo: {'selector': 'main [draggable=true]', 'hasText': titulo}  # card da oportunidade (o wrapper arrastável)
TITULO = lambda t: {'selector': 'main [draggable=true] h4', 'hasText': t}   # título dentro do card (alvo menor que o card)
DI = lambda ph, k=0: {'selector': f"{DLG} input[placeholder='{ph}']", 'nth': k}


# ---------------------------------------------------------------- trechos comuns (não filmados, no `setup`)
SETUP_DASH = [{'do': 'goto', 'url': '/dashboard'}, {'do': 'waitFor', 'text': 'Olá, Camila!', 'timeout': 25}, AGUARDA]
CRM_PRONTO = {'do': 'waitFor', 'text': 'Gerencie oportunidades e processos', 'timeout': 25}


def setup_crm(recolhido=True):
    """começa no Dashboard (aquece o app), vai ao CRM/Kanban e recolhe o menu lateral (6 colunas de 300 px não cabem a 1280 px com o menu aberto)"""
    s = SETUP_DASH + [{'do': 'goto', 'url': '/crm'}, CRM_PRONTO, AGUARDA]
    if recolhido:
        s += [{'do': 'click', 'target': MENU_LATERAL}, {'do': 'pause', 'seconds': 0.8}]
    return s


# a coluna de destino fica na ponta direita da janela (cortada pela borda): soltar num ponto DENTRO da parte visível da coluna (o robô sorteia um ponto do alvo,
# que podia cair fora da tela); y = corpo da coluna (vale com ou sem a linha de orientação acima das colunas)
SOLTAR_DIREITA = {'x': 1150, 'y': 620}


def rolar_quadro(esq, instantaneo=True):
    """JS: rola a faixa das colunas do funil para `esq` px (instantâneo: o clique/arrasto seguinte não espera a rolagem suave)"""
    return ("(()=>{const b=document.querySelector(%s);if(!b)return 'sem faixa';b.scrollTo({left:%d,behavior:%s});return b.scrollLeft})()"
            % (json.dumps(BOARD), esq, json.dumps('auto' if instantaneo else 'smooth')))


# ================================================================ capítulos
def cap00():
    """Abertura: o Dashboard; o cursor desce pelo menu lateral, para no grupo "CRM e Projetos" e abre a lista (CRM/Kanban e Projetos)."""
    c = Cap(0, pace=0.5, start=(760, 420), prewarm=['/dashboard'], setup=SETUP_DASH)
    c.mark(1)
    c.hover(LINK('Agenda'), 0.1, at=0.2, label='o cursor desce pelo menu lateral')
    c.hover(GRUPO, 0.4, at=c.A(1, 'funil', 0.8), label='o grupo "CRM e Projetos" do menu')
    c.click(GRUPO, at=c.A(1, 'oportunidade', 0.9), label='abre o grupo CRM e Projetos')
    c.mark(2)
    c.hover(CRM_KANBAN, 0.8, at=c.A(2, 'CRM', 0.8), label='item CRM/Kanban do grupo')
    c.hover(PROJETOS, 0.8, at=c.A(2, 'dono,', 0.9), label='item Projetos do grupo')
    c.mark(3)
    c.hover(GRUPO, 0.8, at=c.A(3, 'grupo', 0.9), label='a câmera fica no grupo CRM e Projetos')
    c.mark(4)
    c.hover(CRM_KANBAN, 0.6, at=c.A(4, 'abrir', 1.0), label='o cursor passa pelo CRM/Kanban (sem clicar)')
    c.fim()
    return c


def cap01():
    """O funil começa aqui: menu CRM e Projetos > CRM/Kanban, o cartão "Configure seu funil", estágios padrão, indicadores e o "+" (Novo funil)."""
    c = Cap(1, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/crm'], setup=SETUP_DASH)
    c.mark(1)
    c.click(GRUPO, at=0.3, label='abre o grupo CRM e Projetos')
    c.click(CRM_KANBAN, at=c.A(1, 'Kanban', 0.9), label='abre o CRM/Kanban')
    c.add(CRM_PRONTO)
    c.hover(TAB('Funil'), 0.4, at=c.A(1, 'Funil', 0.9, nth=1), label='aba Funil')
    c.hover(TAB('Tarefas'), 0.4, at=c.A(1, 'Tarefas', 0.9), label='aba Tarefas')
    c.hover({'text': 'Total no funil', 'exact': True, 'within': 'main'}, 0.4, at=c.A(1, 'indicadores', 0.9), label='indicador Total no funil', optional=True)
    c.click(MENU_LATERAL, at=c.A(1, 'alto.', 0.9), label='recolhe o menu lateral (o quadro ganha espaço)')
    c.pause(0.8)
    c.mark(2)
    c.hover(BTN('Começar com estágios padrão'), 0.5, at=c.A(2, 'cartão', 0.8), label='botão Começar com estágios padrão')
    c.hover(BTN('Personalizar estágios'), 0.5, at=c.A(2, 'parada', 0.9), label='botão Personalizar estágios (sem clicar)')
    c.mark(3)
    c.click(BTN('Começar com estágios padrão'), at=c.A(3, 'clico', 0.9), label='Começar com estágios padrão')
    c.waitfor(text='Fechado (Perdido)', timeout=15)
    c.confere('main', ['Funil de Vendas', 'Lead', 'Proposta', 'Negociação', 'Fechado (Ganho)', 'Fechado (Perdido)', 'Total no funil', 'Valor Total'],
              'funil com as cinco etapas padrão')
    c.mark(4)
    c.hover({'text': 'Total no funil', 'exact': True, 'within': 'main'}, 0.5, at=c.A(4, 'Total', 0.8), label='indicador Total no funil')
    c.hover({'text': 'Valor Total', 'exact': True, 'within': 'main'}, 0.5, at=c.A(4, 'Valor', 0.8), label='indicador Valor Total')
    c.hover({'text': 'Fechado (Ganho)', 'exact': True, 'within': 'main', 'nth': 0}, 0.5, at=c.A(4, 'Ganho', 0.8), label='indicador Fechado (Ganho)')
    c.hover({'text': 'Lead', 'exact': True, 'within': 'main', 'nth': 0}, 0.5, at=c.A(4, 'Lead', 0.8, nth=0), label='indicador Lead')
    c.mark(5)
    c.hover(BTN('Novo funil'), 1.2, at=c.A(5, 'botão', 0.8), label='o "+" Novo funil (sem clicar)')
    c.fim()
    return c


def drop_linha(src, dst):
    """JS: sequência de DragEvent reais (dragstart na origem; dragenter e vários dragover com clientX/Y no alvo; drop no alvo; dragend na origem) com um
    DataTransfer novo. Aciona os handlers do React (a lógica real do app). As linhas são buscadas DE NOVO antes de cada evento: a lista é um componente
    definido dentro do render (`EditableRow`), então o dragstart refaz as linhas e o nó de origem que o navegador segurava sai do DOM. É por isso que o
    arrasto de mouse nativo (mouse.down/up) trava o Chromium nessa janela (a origem some no meio do arrasto, e o fim do arrasto nunca chega)."""
    return ("(async()=>{const S=%s,D=%s;const rows=()=>[...document.querySelectorAll('[role=dialog] [draggable=true]')];"
            "const f=t=>rows().find(r=>r.innerText.includes(t));const w=ms=>new Promise(r=>setTimeout(r,ms));"
            "const nomes=()=>rows().slice(1).map(r=>r.innerText.trim().split('\\n')[0]);const pronto=()=>{const n=nomes();return n.indexOf(S)>=0&&n.indexOf(S)<n.indexOf(D)};"
            "if(!f(S)||!f(D))return 'sem linha';"
            "for(let t=0;t<3&&!pronto();t++){const dt=new DataTransfer();"
            "const ev=(ty,el,xy)=>el.dispatchEvent(new DragEvent(ty,Object.assign({bubbles:true,cancelable:true,dataTransfer:dt},xy||{})));"
            "ev('dragstart',f(S));await w(250);"
            "for(let k=0;k<6;k++){const b=f(D),r=b.getBoundingClientRect();const xy={clientX:r.x+30+k*8,clientY:r.y+r.height/2};if(k===0)ev('dragenter',b,xy);ev('dragover',b,xy);await w(90)}"
            "ev('drop',f(D),{clientX:f(D).getBoundingClientRect().x+60,clientY:f(D).getBoundingClientRect().y+10});await w(150);const o=f(S);if(o)ev('dragend',o);"
            "for(let k=0;k<8&&!pronto();k++)await w(250)}"
            "return (pronto()?'OK: ':'DIFERENTE: ')+nomes().join(' > ')})()") % (json.dumps(src), json.dumps(dst))


def cap02():
    """Ajustando as etapas: Configurações do CRM/Kanban > Funis, Novo estágio (Visita técnica), arrastar a linha, Editar (Ganho/Perdido), quadro com seis colunas."""
    c = Cap(2, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/crm'], setup=setup_crm())
    c.mark(1)
    c.click(CONFIG_CRM, at=c.A(1, 'Clico', 0.9), label='Configurações do CRM/Kanban')
    c.waitfor(text='Gerenciar Funis', timeout=15)
    for palavra, nome in [('Funis,', 'Funis'), ('Checklists,', 'Checklists'), ('Etiquetas', 'Etiquetas'), ('Webhooks.', 'Webhooks')]:
        c.hover(TAB(nome, within=DLG), 0.3, at=c.A(1, palavra, 0.8), label=f'seção {nome}')
    c.mark(2)
    c.click(BTN('Novo estágio', within=DLG), at=c.A(2, 'Novo', 1.6), label='Novo estágio')
    c.type({'placeholder': 'Nome do estágio', 'within': DLG}, 'Visita técnica', at=c.A(2, 'escrevo', 1.3), label='nome do estágio: Visita técnica', cps=40)
    c.click({'selector': f'{DLG} button:has(span.font-mono)'}, at=c.A(2, 'cor', 1.5), label='abre a cor')
    c.click({'selector': f'{POP} button[style*="rgb(139, 92, 246)"]'}, label='escolhe um tom de roxo')
    c.press('Escape', label='fecha a cor')
    c.pause(0.1)
    c.click(BTN('Adicionar estágio', within=DLG), at=c.A(2, 'Adicionar', 1.0), label='Adicionar estágio')
    c.waitfor(selector=f'{DLG} [draggable=true]', timeout=10)
    c.mark(3)
    # o arrasto por mouse numa linha DENTRO da janela (modal) trava o Chromium (o navegador fica preso no `mouse.up`, 03/11): o cursor vai até a
    # alça e até a linha de destino (hover), e o soltar é o evento de arrastar do próprio navegador, disparado por `eval` (o app recebe dragstart/drop).
    LINHA = lambda nome: {'selector': f'{DLG} [draggable=true]', 'hasText': nome}
    c.hover(LINHA('Visita técnica'), 0.5, at=c.A(3, 'arrastar', 1.4), label='cursor na alça da Visita técnica')
    c.hover(LINHA('Proposta'), 0.5, label='cursor sobre a linha de Proposta')
    c.ev(drop_linha('Visita técnica', 'Proposta'), label='solta: a Visita técnica fica logo depois do Lead')
    c.ev("(async()=>{let o='';for(let i=0;i<20;i++){o=[...document.querySelectorAll('[role=dialog] [draggable=true]')].slice(1).map(r=>r.innerText.trim().split('\\n')[0]).join(' > ');"
         "if(o.startsWith('Lead > Visita técnica > Proposta'))break;await new Promise(r=>setTimeout(r,300))}"
         "return (o.startsWith('Lead > Visita técnica > Proposta')?'OK: ':'DIFERENTE: ')+o})()", label='confere a ordem das etapas na janela: Lead, Visita técnica, Proposta')
    c.mark(4)
    ACOES = {'selector': f"{DLG} [draggable=true]:has-text('Fechado (Ganho)') button[aria-label='Ações']"}
    c.click(ACOES, at=c.A(4, 'Olha', 4.4), label='menu ⋮ da etapa Fechado (Ganho)')
    c.pause(0.6)
    c.click(ACOES, label='menu ⋮ de novo (só se não abriu)', unless=ITEM('Editar'))
    c.click(ITEM('Editar'), label='Editar')
    c.hover(SW('Ganho'), 0.2, at=c.A(4, 'Ganho', 1.4, nth=0), label='interruptor Ganho (ligado)')
    c.hover(SW('Perdido'), 0.6, at=c.A(4, 'Perdido', 0.5, nth=0), label='interruptor Perdido (desligado)')
    c.click({'selector': f'{DLG} div.bg-muted\\/30 button:has(svg.lucide-x)'}, at=c.A(4, 'Numa', 0.9), label='X do quadro de edição (cancela)')
    c.mark(5)
    c.press('Escape', at=c.A(5, 'Fechando', 0.9), label='fecha a janela')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.hover(COLUNA('Visita técnica'), 1.2, at=c.A(5, 'reordenar', 0.9), label='nome da coluna (arrastar reordena)')
    c.fim()
    return c


# ---------------------------------------------------------------- formulário "Nova Oportunidade" e detalhe da oportunidade
CMDK = {'selector': '[cmdk-input]'}
F = lambda i: {'selector': f'{DLG} #{i}'}                                    # campos com id: title, customer_id, source, stage_id, value, probability, expected_close_date, notes
COMBO_VEND = {'selector': f'{DLG} button[role=combobox]', 'hasText': 'Selecione...'}   # o seletor de responsáveis mostra "Selecione..." (o placeholder "Atribuir a vendedor" do roteiro não aparece)
COMBO_ORIGEM = {'selector': f'{DLG} button[role=combobox]', 'hasText': 'De onde veio?'}
DIA = lambda n: {'selector': f'{POP} button[name=day]', 'hasText': str(n)}
PROX_MES = {'selector': f'{POP} button[name=next-month]'}


def digitar_num(c, alvo, texto, at=None, label=None):
    """campo numérico com valor de partida (0 ou 50): clica, seleciona tudo (Ctrl+A) e digita POR CIMA (sem Backspace)"""
    c.click(alvo, at=at, label=(label + ' (clique)') if label else None)
    c.press('Control+A')
    return c.type(alvo, texto, noClick=True, label=label)


def cap03():
    """A primeira oportunidade: Nova oportunidade, título, cliente (e o "+"), vendedor, origem, estágio, valor, probabilidade, previsão, observações, Salvar."""
    c = Cap(3, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/crm'], setup=setup_crm())
    c.mark(1)
    c.click(NOVA_OPORT, at=c.A(1, 'Clico', 0.9), label='Nova oportunidade')
    c.waitfor(text='Título da Oportunidade *', timeout=15)
    c.mark(2)
    c.type(F('title'), 'Instalação de 6 splits - Colégio Monte Verde', at=c.A(2, 'escrevo', 0.9), label='título da oportunidade', cps=55)
    c.click(F('customer_id'), at=c.A(2, 'Cliente,', 0.9), label='campo Cliente')
    c.type(CMDK, 'Colégio', label='busca "Colégio"')
    c.click(OPT('Colégio Monte Verde'), label='Colégio Monte Verde')
    c.hover({'selector': f"{DLG} button[aria-label='Criar cliente']"}, 1.0, at=c.A(2, 'mais', 0.8), label='o "+" do seletor (cadastrar na hora; sem clicar)', optional=True)
    c.mark(3)
    c.click(COMBO_VEND, at=c.A(3, 'escolho', 0.9), label='campo Vendedor Responsável')
    c.click({'text': 'Camila Duarte', 'within': POP}, label='marca Camila Duarte')
    c.press('Escape', label='fecha a lista de vendedores')
    c.hover(PD('O primeiro selecionado vira o responsável principal'), 1.4, at=c.A(3, 'primeiro', 0.9), label='dica do Principal')
    c.mark(4)
    c.click(F('source'), at=c.A(4, 'Origem', 0.9), label='campo Origem')
    c.click(OPT('Indicação'), at=c.A(4, 'Indicação.', 0.9), label='origem Indicação')
    c.select({'selector': f'{DLG} button[role=combobox]', 'hasText': 'Lead'}, 'Visita técnica', at=c.A(4, 'Estágio,', 0.9), label='estágio Visita técnica')
    c.mark(5)
    digitar_num(c, F('value'), '18600', at=c.A(5, 'Valor', 0.9), label='Valor Estimado 18600')
    digitar_num(c, F('probability'), '60', at=c.A(5, 'coloco', 0.9), label='Probabilidade 60')
    c.click(F('expected_close_date'), at=c.A(5, 'Previsão', 0.9), label='campo Previsão Fechamento')
    c.click(PROX_MES, label='mês seguinte', noScroll=True)
    c.click(DIA(15), label='dia 15', noScroll=True)
    c.click(F('notes'), at=c.A(5, 'Observações', 1.4), label='campo Observações')
    c.colar('Instalação dos aparelhos nas salas de aula do Bloco B.', None, 'observações')
    c.mark(6)
    c.click(BTN('Salvar', within=DLG), at=c.A(6, 'Salvar,', 0.9), label='Salvar')
    c.waitfor(gone={'role': 'dialog'}, timeout=10)
    c.confere('main', ['Instalação de 6 splits - Colégio Monte Verde', 'Colégio Monte Verde', 'R$ 18.600,00', 'Probabilidade', '60%', 'Indicação'], 'card do colégio na Visita técnica')
    c.hover(CARD('Instalação de 6 splits'), 1.2, at=c.A(6, 'Ele', 0.9), label='o card no funil')
    c.hover({'text': 'Valor Total', 'exact': True, 'within': 'main'}, 1.2, at=c.A(6, 'indicadores', 0.9), label='indicadores contam a primeira oportunidade')
    c.fim()
    return c


def cap04():
    """Andando no funil: o Marcos de Proposta para Negociação; a Luana para Fechado (Perdido) com o Motivo da Perda (Preço alto)."""
    c = Cap(4, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/crm'], setup=setup_crm())
    c.mark(1)
    c.hover(TITULO('PMOC anual'), 0.6, at=c.A(1, 'hotel,', 0.9), label='card do hotel (Negociação)')
    c.hover(TITULO('Marcos Antônio Braga'), 0.6, at=c.A(1, 'Marcos', 0.9), label='card do Marcos (Proposta)')
    c.hover(COLUNA('Proposta'), 0.6, at=c.A(1, 'Luana.', 0.9), label='coluna Proposta (Marcos e Luana; o card da Luana fica abaixo da dobra)')
    c.mark(2)
    c.drag(CARD('Marcos Antônio Braga'), COLUNA('Negociação'), at=c.A(2, 'arrastar', 1.0), label='arrasta o Marcos de Proposta para Negociação')
    c.confere('main', ['Negociação'], 'o Marcos entrou em Negociação')
    c.mark(3)
    c.ev(rolar_quadro(632), at=c.A(3, 'Arrasto', 2.0), label='rola o quadro até Fechado (Perdido) ficar na janela')
    c.drag(CARD('Luana Martins'), SOLTAR_DIREITA, at=c.A(3, 'Arrasto', 1.0), label='arrasta a Luana para Fechado (Perdido)')
    c.waitfor(text='Motivo da Perda', timeout=10)
    c.select({'selector': f'{DLG} button[role=combobox]'}, 'Preço alto', at=c.A(3, 'Escolho', 0.9), label='Motivo: Preço alto')
    c.click({'placeholder': 'Adicione mais detalhes sobre a perda...', 'within': DLG}, at=c.A(3, 'escrevo', 1.0), label='campo Detalhes')
    c.colar('O cliente achou o valor da higienização acima do esperado.', None, 'detalhes da perda')
    c.click(BTN('Confirmar Perda'), at=c.A(3, 'Confirmar', 0.9), label='Confirmar Perda')
    c.waitfor(gone={'role': 'dialog'}, timeout=10)
    c.mark(4)
    c.hover(COLUNA('Fechado (Perdido)'), 1.4, at=c.A(4, 'motivo', 0.9), label='coluna Fechado (Perdido) (1 oportunidade, R$ 380,00)')
    c.confere('main', ['Fechado (Perdido)', 'Higienização de 2 splits - Luana Martins', 'R$ 380,00'], 'Luana em Fechado (Perdido) com R$ 380,00')
    c.fim()
    return c


def cap05():
    """Quando o cliente fecha: o colégio para Fechado (Ganho), "Oportunidade ganha", Agora não; indicador Fechado (Ganho) R$ 18.600,00."""
    c = Cap(5, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/crm'], setup=setup_crm())
    c.mark(1)
    c.ev(rolar_quadro(316), at=c.A(1, 'Arrasto', 2.0), label='rola o quadro até Fechado (Ganho) ficar na janela')
    c.drag(CARD('Instalação de 6 splits'), SOLTAR_DIREITA, at=c.A(1, 'Arrasto', 1.0), label='arrasta o colégio para Fechado (Ganho)')
    c.waitfor(text='Oportunidade ganha', timeout=10)
    c.confere(DLG, ['Oportunidade ganha', 'Quer lançar a receita desta venda?', 'Valor a lançar', 'Colégio Monte Verde'], 'janela Oportunidade ganha (Oportunidade, Cliente e Valor a lançar)')
    c.ev("(async()=>{let v='';for(let i=0;i<10;i++){v=(document.querySelector('[role=dialog] input')||{}).value||'';if(v)break;await new Promise(r=>setTimeout(r,300))}"
         "return (/18[.]?600/.test(v)?'OK: Valor a lançar ':'DIFERENTE: Valor a lançar ')+v})()", label='confere Valor a lançar R$ 18.600,00 (campo da janela)')
    c.hover(PD('Valor a lançar'), 1.0, at=c.A(1, 'Valor', 0.9, nth=0), label='Valor a lançar R$ 18.600,00')
    c.mark(2)
    c.hover(BTN('Sim, lançar receita'), 0.3, at=c.A(2, 'Sim,', 0.9), label='botão Sim, lançar receita (sem clicar)')
    c.click(BTN('Agora não'), at=c.A(2, 'Agora', 1.1), label='Agora não')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.mark(3)
    c.hover({'text': 'Fechado (Ganho)', 'exact': True, 'within': 'main', 'nth': 0}, 1.2, at=c.A(3, 'indicador', 0.9), label='indicador Fechado (Ganho)')
    c.confere('main', ['Fechado (Ganho)', 'R$ 18.600,00'], 'indicador Fechado (Ganho) R$ 18.600,00')
    c.hover(COLUNA('Fechado (Ganho)'), 1.2, at=c.A(3, 'etapa', 0.9), label='coluna Fechado (Ganho)')
    c.fim()
    return c


# ---------------------------------------------------------------- detalhe da oportunidade
TRASH = {'selector': f"{DLG} button:has(svg[class*='trash'])"}
ABA = lambda n: {'role': 'tab', 'name': n}                                   # "Histórico (1)": nome por substring
FOCO = "(()=>{window.dispatchEvent(new Event('focus'));document.dispatchEvent(new Event('visibilitychange'));return 'foco'})()"   # o quadro relê os cards (evento de foco da janela)
FAKE = os.environ.get('FAKE_URL', 'http://127.0.0.1:54328')


# O card do hotel (Negociação) vem DEPOIS do Marcos (arrastado no cap. 4, "atualizado agora") e fica abaixo da dobra (y ~ 800), onde o clique rola ~5 s.
# Antes do capítulo (fora do vídeo) o hotel recebe um PATCH sem mudança de dado (probabilidade 70, a mesma): o gancho carimba updated_at = agora (relógio
# congelado), empata com o Marcos, e o desempate pela ordem das linhas deixa o hotel em cima, como se a Tatiane tivesse mexido nele hoje.
TOCA_HOTEL = {'do': 'eval', 'js': ("(async()=>{const r=await fetch(%s+'/rest/v1/leads?title=like.PMOC*',{method:'PATCH',headers:{'Content-Type':'application/json',"
                                  "'Prefer':'return=minimal','apikey':'x'},body:JSON.stringify({probability:70})});return r.status})()") % json.dumps(FAKE)}


def cap06():
    """Tudo do negócio num lugar: detalhe do PMOC do hotel (estágio, responsáveis, botões, contato), Observações, Comentário, Histórico e Nova Interação (Reunião)."""
    c = Cap(6, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/crm'], setup=SETUP_DASH + [TOCA_HOTEL, {'do': 'goto', 'url': '/crm'}, CRM_PRONTO, AGUARDA, {'do': 'click', 'target': MENU_LATERAL}, {'do': 'pause', 'seconds': 0.8}])
    c.mark(1)
    c.click(CARD('PMOC anual'), at=c.A(1, 'Abro', 0.9), label='abre o PMOC anual do Hotel Mirante do Mar')
    c.waitfor(text='Responsáveis:', timeout=15)
    c.hover(PD('Estágio:'), 0.8, at=c.A(1, 'etapa', 0.8), label='Estágio: Negociação')
    c.hover(PD('Responsáveis:'), 0.8, at=c.A(1, 'cuida', 0.8), label='Responsáveis: Tatiane Ribeiro (Principal)')
    c.confere('dlg', ['Estágio:', 'Negociação', 'Responsáveis:', 'Tatiane Ribeiro', 'Principal'], 'estágio Negociação e responsável Tatiane Ribeiro (Principal)')
    c.mark(2)
    c.hover(BTN('Editar', within=DLG), 0.3, at=c.A(2, 'lixeira', 2.2), label='botão Editar (alto da janela)', noScroll=True)
    c.hover(TRASH, 1.0, at=c.A(2, 'lixeira', 0.4), label='a lixeira (sem clicar: pede confirmação do navegador)', noScroll=True)
    c.mark(3)
    c.hover(BTN('Criar OS', within=DLG), 0.6, at=c.A(3, 'Criar', 0.8, nth=0), label='botão Criar OS (sem clicar)')
    c.hover(BTN('Criar Tarefa', within=DLG), 0.6, at=c.A(3, 'Criar', 0.8, nth=1), label='botão Criar Tarefa (sem clicar)')
    c.hover(PD('Valor Estimado'), 0.6, at=c.A(3, 'valor', 0.8), label='quadro Valor Estimado')
    c.hover(PD('Previsão Fechamento'), 0.6, at=c.A(3, 'previsão', 0.8), label='quadro Previsão Fechamento')
    c.hover(PD('Origem'), 0.6, at=c.A(3, 'origem.', 0.8), label='quadro Origem')
    c.mark(4)
    c.hover(PD('Contato do Cliente'), 1.0, at=c.A(4, 'Contato', 0.8), label='quadro Contato do Cliente')
    c.hover({'selector': f"{DLG} a:has-text('WhatsApp'), {DLG} button:has-text('WhatsApp')"}, 0.8, at=c.A(4, 'WhatsApp', 0.8), label='botão verde WhatsApp (sem clicar)')
    c.mark(5)
    c.click({'placeholder': 'Adicione observações sobre esta oportunidade...', 'within': DLG}, at=c.A(5, 'Observações,', 0.9), label='campo Observações')
    c.colar('O hotel quer o contrato anual, com visita mensal em todos os aparelhos.', None, 'digita as observações')
    c.waitfor(text='Salvo', timeout=10)
    c.mark(6)
    c.hover({'selector': f"{DLG} section[aria-label='Etiquetas da oportunidade']"}, 0.3, at=c.A(6, 'Etiquetas', 0.8), label='bloco Etiquetas da oportunidade')
    c.hover({'selector': f"{DLG} section[aria-label^='Checklists']"}, 0.3, at=c.A(6, 'Checklists', 0.8), label='bloco Checklists da oportunidade')
    c.click({'placeholder': 'Escreva um comentário...', 'within': DLG}, at=c.A(6, 'escrevo', 0.9), label='campo de comentário')
    c.colar('A gerência pediu a minuta do contrato.', None, 'digita o comentário')
    c.click(BTN('Comentar', within=DLG), label='Comentar')
    c.waitfor(text='A gerência pediu a minuta do contrato.', timeout=10)
    c.mark(7)
    c.click(ABA('Histórico'), at=c.A(7, 'aba', 0.9), label='aba Histórico')
    c.click(BTN('Nova Interação', within=DLG), at=c.A(7, 'Nova', 0.9), label='Nova Interação')
    c.waitfor(text='Registrar Interação', timeout=10)
    c.select({'selector': f'{DLG} button[role=combobox]'}, 'Reunião', at=c.A(7, 'Reunião,', 0.9), label='Tipo de Interação: Reunião')
    c.click({'placeholder': 'Ex: Enviar proposta', 'within': DLG}, at=c.A(7, 'deixo', 1.0), label='campo Próxima Ação')
    c.colar('Enviar a minuta do contrato', None, 'Próxima Ação')
    c.click({'placeholder': 'Descreva o que foi conversado...', 'within': DLG}, label='campo Descrição')
    c.colar('Reunião com a gerência do hotel para alinhar o PMOC anual.', None, 'Descrição')
    c.click({'selector': f'{DLG} button:has(svg.lucide-calendar)'}, label='campo Data da Próxima Ação')
    c.click(PROX_MES, label='mês seguinte', noScroll=True)
    c.click(DIA(10), label='dia 10', noScroll=True)
    c.click(BTN('Registrar', within=DLG), at=c.A(7, 'Registrar.', 0.9), label='Registrar')
    c.waitfor(text='Próxima ação:', timeout=10)
    c.mark(8)
    c.hover(PD('Próxima ação:'), 1.2, at=c.A(8, 'próxima', 0.8), label='linha nova com Próxima ação:')
    c.hover(PD('Mudança de estágio'), 1.2, at=c.A(8, 'mudança', 0.8), label='Mudança de estágio (De Proposta, Para Negociação)')
    c.confere('dlg', ['Reunião', 'Próxima ação: Enviar a minuta do contrato', 'Mudança de estágio', 'Proposta', 'Negociação'], 'histórico: Reunião e Mudança de estágio')
    c.fim()
    return c


def cap07():
    """Achando rápido: busca "Mirante" (etapas sem resultado ocultas, Mostrar todas), filtro Vendedor (Tatiane Ribeiro), Sem responsável e Origem."""
    c = Cap(7, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/crm'], setup=setup_crm())
    c.mark(1)
    c.click(BUSCA, at=c.A(1, 'busca,', 0.9), label='campo de busca')
    c.type(BUSCA, 'Mirante', noClick=True, cps=12, label='digita Mirante')
    c.waitfor(text='5 etapas sem resultado estão ocultas.', timeout=10)
    c.confere('main', ['5 etapas sem resultado estão ocultas.', 'Mostrar todas', '1 de 4', 'PMOC anual - Hotel Mirante do Mar'], 'busca Mirante: só o hotel, 5 etapas ocultas, 1 de 4')
    c.mark(2)
    c.hover(BTN('Mostrar todas'), 0.6, at=c.A(2, 'Mostrar', 0.8), label='botão Mostrar todas')
    c.click(BTN('Mostrar todas'), label='Mostrar todas')
    c.type(BUSCA, '', clear=True, at=c.A(2, 'Apago', 0.9), label='apaga a busca')
    c.mark(3)
    c.click(BTNX('Filtros'), at=c.A(3, 'filtro,', 0.9), label='botão de filtro (dentro da busca)')
    c.waitfor(text='Valor Mínimo', timeout=10)
    c.hover(PD('Valor Mínimo'), 0.6, at=c.A(3, 'Valor', 0.8, nth=0), label='Valor Mínimo e Valor Máximo')
    c.click({'text': 'Tatiane Ribeiro', 'within': DLG}, at=c.A(3, 'Tatiane', 0.9), label='marca Tatiane Ribeiro em Vendedor')
    c.confere('dlg', ['Tatiane Ribeiro'], 'Tatiane na lista de Vendedor')
    c.mark(4)
    c.hover({'text': 'Sem responsável', 'within': DLG}, 0.8, at=c.A(4, 'Sem', 0.8), label='opção Sem responsável')
    c.hover({'text': 'Indicação', 'within': DLG}, 0.8, at=c.A(4, 'Indicação,', 0.8), label='lista de Origem')
    c.click(BTNX('limpar', within=DLG), at=c.A(4, 'encontra', 1.3), label='limpar o filtro', optional=True, noScroll=True)
    c.press('Escape', label='fecha o filtro', optional=True)
    c.fim()
    return c


WEBHOOK_URL_JS = ("(()=>{const e=[...document.querySelectorAll('input')].find(i=>/crm-lead-webhook\\?token=/.test(i.value));"
                  "if(!e)return 'sem campo';window.__tok=e.value.split('token=')[1];return window.__tok.length})()")
POST_JS = ("(async()=>{const r=await fetch(%s+'/functions/v1/crm-lead-webhook?token='+window.__tok,{method:'POST',headers:{'Content-Type':'application/json'},"
           "body:JSON.stringify({name:'Renato Assis',phone:'(21) 93000-1500',email:'renato.assis@email.example',title:'Orçamento pelo site - Renato Assis',"
           "notes:'Manutenção em 3 splits do escritório'})});return r.status+' '+(await r.text()).slice(0,120)})()") % json.dumps(FAKE)


FECHAR_EVAL = r"""(() => { const d = document.querySelector('[role=dialog]'); if (!d) return 'ja fechada'; const b = [...d.querySelectorAll('button')].find((x) => [x.textContent, x.getAttribute('aria-label'), x.title].some((v) => /^\s*fechar\s*$/i.test(v || ''))); if (!b) return 'sem botao Fechar'; b.click(); return 'fechada pelo botao'; })()"""


def cap08():
    """Contatos que chegam sozinhos: Webhooks (Site - Pedido de orçamento, Site > Funil de Vendas > Lead), copiar, Como usar, o contato chega (POST do robô) e Assumir oportunidade."""
    c = Cap(8, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/crm'], setup=setup_crm())
    c.mark(1)
    c.click(CONFIG_CRM, at=c.A(1, 'abro', 0.9), label='Configurações do CRM/Kanban')
    c.waitfor(text='Gerenciar Funis', timeout=15)
    c.click(TAB('Webhooks', within=DLG), at=c.A(1, 'Webhooks.', 0.9), label='seção Webhooks')
    c.waitfor(text='Webhooks de Leads Externos', timeout=10)
    c.mark(2)
    c.hover(PD('Webhooks de Leads Externos'), 1.2, at=c.A(2, 'endereço', 1.0), label='título Webhooks de Leads Externos')
    c.mark(3)
    c.hover(PD('Criar novo webhook'), 1.2, at=c.A(3, 'formulário', 0.9), label='quadro Criar novo webhook')
    c.mark(4)
    c.type({'placeholder': 'Ex: Meta Ads - Campanha Março', 'within': DLG}, 'Site - Pedido de orçamento', at=c.A(4, 'nome:', 0.9), label='Nome do webhook', cps=55)
    c.select({'role': 'combobox', 'name': 'Origem padrão'}, 'Site', at=c.A(4, 'Origem', 0.9), label='Origem padrão: Site')
    c.select({'role': 'combobox', 'name': 'Funil de destino'}, 'Funil de Vendas', at=c.A(4, 'Funil', 0.9, nth=1), label='Funil de destino')
    c.select({'role': 'combobox', 'name': 'Etapa de destino'}, 'Lead', at=c.A(4, 'Etapa', 0.9), label='Etapa de destino: Lead')
    c.click(BTN('Criar webhook'), at=c.A(4, 'Clico', 0.9), label='Criar webhook')
    c.waitfor(text='Webhooks configurados', timeout=10)
    c.mark(5)
    c.hover(PD('Site - Pedido de orçamento'), 1.0, at=c.A(5, 'aparece', 0.9), label='a linha do webhook novo (Ativo)')
    c.click({'selector': f'{DLG} button:has(svg.lucide-copy)'}, at=c.A(5, 'copiar,', 0.9), label='botão de copiar')
    c.waitfor(text='URL copiada!', timeout=8)
    c.ev(WEBHOOK_URL_JS, label='lê o token do campo da tela (para o POST do robô)')
    c.mark(6)
    c.hover(PD('Como usar o webhook'), 1.4, at=c.A(6, 'Como', 0.9), label='bloco Como usar o webhook')
    c.mark(7)
    c.press('Escape', at=round(c.L(7) - 10.4, 2), label='fecha a janela (começa na pausa da voz: o recarregamento vira corte na edição)')
    c.add({'do': 'wait', 'seconds': 0.4})
    c.ev(FECHAR_EVAL, label='Fechar (se o Esc não fechou)')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.ev(POST_JS, label='o site manda um contato (POST invisível ao webhook)')
    c.ev(FOCO, label='a janela volta ao foco: o quadro relê os cards')
    # o quadro NÃO relê sozinho com o foco (testado, 1.38.19): recarrega o CRM (corte na edição), recolhe o menu de novo e segue
    c.ev('JSON.stringify(window.__avisos || "sem observador")', label='avisos de erro na tela (antes de recarregar)')
    c.add({'do': 'goto', 'url': '/crm', 'reload': True, 'label': 'recarrega o CRM (o quadro relê os cards; cortar na edição)'})
    c.add(CRM_PRONTO)
    c.add(AGUARDA)
    c.ev(OBS, label='religa o observador de avisos (a página foi recarregada)')
    c.click(MENU_LATERAL, label='recolhe o menu lateral de novo')
    c.pause(0.8)
    c.waitfor(text='Orçamento pelo site - Renato Assis', timeout=15)
    c.hover(CARD('Renato Assis'), 1.2, at=c.A(7, 'aqui,', 0.9), label='o card novo na coluna Lead (Sem responsável, origem Site)')
    c.mark(8)
    c.click(CARD('Renato Assis'), at=c.A(8, 'Abro', 0.9), label='abre o card')
    c.waitfor(text='Assumir oportunidade', timeout=10)
    c.hover(PD('Observações'), 1.4, at=c.A(8, 'Observações.', 0.9), label='Observações (Nome, Telefone, Email e Origem)')
    c.click(BTN('Assumir oportunidade', within=DLG), at=c.A(8, 'clica', 0.9), label='Assumir oportunidade')
    c.waitfor(text='Camila Duarte', timeout=10)
    c.confere('dlg', ['Responsáveis:', 'Camila Duarte', 'Principal'], 'Camila Duarte assumiu (Principal)')
    c.fim()
    return c


# ---------------------------------------------------------------- Projetos
COLUNA_PROJ = lambda nome: {'selector': 'main div.rounded-t-lg', 'hasText': nome}   # cabeçalho da coluna de uma frente (não é arrastável; o soltar sobe até a coluna)


def cap09():
    """Acompanhando a obra: CRM e Projetos > Projetos, Novo projeto, detalhe, Criar frente (Infraestrutura), Novo card, arrastar até Concluído, Progresso da obra 100%."""
    c = Cap(9, pace=0.5, start=(760, 420), prewarm=['/dashboard', '/projetos'], setup=SETUP_DASH)
    c.mark(1)
    c.click(GRUPO, at=0.3, label='abre o grupo CRM e Projetos')
    c.click(PROJETOS, at=c.A(1, 'Projetos,', 0.9), label='abre Projetos')
    c.waitfor(text='Nenhum projeto ainda', timeout=15)
    c.mark(2)
    c.click(BTN('Novo projeto'), at=c.A(2, 'Novo', 0.9), label='Novo projeto')
    c.waitfor(text='Nome do projeto', timeout=10)
    c.click({'placeholder': 'Ex: Instalação de 80 splits, Indústria X', 'within': DLG}, at=c.A(2, 'nome,', 1.5), label='campo Nome do projeto')
    c.colar('Instalação de 6 splits - Colégio Monte Verde', None, 'Nome do projeto')
    c.click({'role': 'combobox', 'name': 'Cliente', 'within': DLG}, at=c.A(2, 'cliente', 0.9), label='campo Cliente')
    c.type(CMDK, 'Colégio', label='busca Colégio')
    c.click(OPT('Colégio Monte Verde'), label='Colégio Monte Verde')
    c.select({'role': 'combobox', 'name': 'Responsável', 'within': DLG}, 'Camila Duarte', label='Responsável: Camila Duarte')
    c.click({'selector': f'{DLG} #project-start, {DLG} button:has(svg.lucide-calendar)', 'nth': 0}, at=c.A(2, 'Início', 0.9), label='campo Início previsto')
    c.click(PROX_MES, label='mês seguinte', noScroll=True)
    c.click(DIA(5), label='dia 5', noScroll=True)
    c.click({'selector': f'{DLG} button:has(svg.lucide-calendar)', 'nth': 1}, label='campo Prazo final')
    c.click(PROX_MES, label='mês seguinte', noScroll=True)
    c.click(PROX_MES, label='mais um mês', noScroll=True)
    c.click(DIA(20), label='dia 20', noScroll=True)
    c.click(BTN('Salvar', within=DLG), at=c.A(2, 'Salvar,', 0.9), label='Salvar o projeto')
    c.waitfor(text='#1', timeout=10)
    c.mark(3)
    c.click({'text': 'Instalação de 6 splits - Colégio Monte Verde', 'within': 'main'}, at=c.A(3, 'Abro', 0.9), label='abre o projeto')
    c.waitfor(text='Nenhuma frente de trabalho ainda', timeout=15)
    c.click(MENU_LATERAL, label='recolhe o menu lateral (as quatro colunas cabem)')
    c.pause(0.8)
    c.hover(P('Progresso da obra'), 1.0, at=c.A(3, 'Progresso', 0.9), label='Progresso da obra (traço)')
    c.mark(4)
    c.click(BTN('Criar frente de trabalho'), at=c.A(4, 'Escrevo', 1.6), label='Criar frente de trabalho')
    c.type({'placeholder': 'Ex: Instalação, Elétrica, Dutos', 'within': DLG}, 'Infraestrutura', label='Nome da frente', cps=55)
    c.click(BTN('Salvar', within=DLG), label='Salvar a frente')
    c.waitfor(text='Em execução', timeout=10)
    c.mark(5)
    c.click(BTN('Novo card'), at=c.A(5, 'Novo', 0.9), label='Novo card')
    c.waitfor(text='Título do card *', timeout=10)
    c.type({'selector': f'{DLG} #title'}, 'Tubulação de cobre do Bloco B', at=c.A(5, 'escrevo', 0.9), label='Título do card', cps=55)
    c.click(COMBO_VEND, at=c.A(5, 'escolho', 0.9), label='campo Responsável')
    c.click({'text': 'Rafael Lima', 'within': POP}, label='marca Rafael Lima')
    c.press('Escape')
    c.click(BTN('Salvar', within=DLG), at=c.A(5, 'salvo.', 0.9), label='Salvar o card')
    c.waitfor(gone={'role': 'dialog'}, timeout=10)
    c.mark(6)
    c.drag(CARD('Tubulação de cobre'), COLUNA_PROJ('Em execução'), at=c.A(6, 'Em', 1.0), label='arrasta o card para Em execução')
    c.drag(CARD('Tubulação de cobre'), COLUNA_PROJ('Concluído'), at=c.A(6, 'Concluído', 1.0), label='arrasta o card para Concluído')
    c.mark(7)
    c.click(TAB('Visão geral'), at=c.A(7, 'Visão', 0.9), label='aba Visão geral')
    c.hover(P('Progresso da obra'), 1.4, at=c.A(7, 'Progresso', 0.9), label='Progresso da obra 100%')
    c.confere('main', ['Progresso da obra', '100%', 'Infraestrutura', '1 card'], 'Progresso da obra em 100% e a frente com 1 card')
    c.fim()
    return c


def cap10():
    """Recapitulando: base simples (o funil completo); a montagem da recapitulação entra na edição."""
    c = Cap(10, pace=0.4, start=(760, 420), prewarm=['/dashboard', '/crm'], setup=setup_crm())
    c.mark(1)
    c.hover(COLUNA('Visita técnica'), 1.2, at=c.A(1, 'Visita', 0.9), label='a etapa Visita técnica no funil')
    c.mark(2)
    c.hover(CARD('Higienização de 2 splits'), 1.2, at=c.A(2, 'motivo', 0.9), label='a oportunidade perdida')
    c.mark(3)
    c.hover(CARD('PMOC anual'), 1.2, at=c.A(3, 'Guardou', 0.9), label='o card do hotel')
    c.mark(4)
    c.hover(CARD('Renato Assis'), 1.2, at=c.A(4, 'Criou', 0.9), label='o contato que chegou pelo webhook')
    c.mark(5)
    c.mark(6)
    c.fim()
    return c


CAPS = {0: cap00, 1: cap01, 2: cap02, 3: cap03, 4: cap04, 5: cap05, 6: cap06, 7: cap07, 8: cap08, 9: cap09, 10: cap10}

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
        print(f'cap{n:02d}: {len(d["steps"])} passos, narração {c.dur:.1f} s{" (PROVISÓRIA)" if c.provisoria else ""} -> {os.path.relpath(path, HERE)}')
