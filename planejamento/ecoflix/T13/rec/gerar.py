#!/usr/bin/env python3
"""T13 · gera rec/t13/cap00..cap13.json (roteiros do robô) a partir da voz (t13/narracao/capNN.json).

Contas a Pagar e Receber no COMPUTADOR (janela 1280x800), logado como Rafael Nogueira (MASTER, Recicla Vale Metais), EcoSistema
1.59.154. FAKE_NOW 2026-11-10T08:30:00-03:00 (terça) em todos os capítulos.
Cada passo é preso a uma palavra da fala: `at` = início da palavra − o custo do gesto (A(linha, palavra, folga)), para o cursor CHEGAR
na palavra (docs/04, "Custo real dos gestos"). Hoje a voz é ESTIMADA (capNN.json do preparar_aula.sh); com a voz real, rode de novo.
Rodar de qualquer pasta: `python3 -I rec/t13/gerar.py [NN ...]`. Depois: t13_ensaio.sh NN (ensaio rápido), prever.py NN --ens,
t13_ensaio.sh NN completo.

Cadeia de sementes (rec/mundo/seeds-extra/t13/, t13_sementes.py): `inicio` (Hidráulica Moretti; paid_at do aluguel como data) nos caps
0 a 4; depois cada capítulo parte do `apos-capNN` do anterior que mexeu no banco (SEMENTE abaixo). O `apos-capNN` sai do ensaio do
capítulo NN com 0 falho (`t13_ensaio.sh NN rapido --semente`, na mesma instância, logo depois).

Particularidades (lidas no código da 1.59.154 e conferidas na exploração rec/t13/_ex/):
 - Abas da tela ("Todas", "A Pagar", "A Receber") são <button> simples; Lista/Calendário são ToggleGroup (role radio, "Visão em lista").
 - Busca: duas cópias do campo (celular e computador); o robô pega a visível (aria-label "Buscar contas").
 - Ações da linha: "Marcar pago"/"Receber" (texto), lápis title="Editar", lixeira title="Excluir".
 - Campos de data (DateField) no computador são botão + calendário (react-day-picker 8): dia = button[name=day] sem .day-outside.
 - Categoria e parceiro: Popover + cmdk (role option); Tipo, Centro de custo e Pagamento previsto: Select do Radix (role option).
 - Valor (BRNumberInput/MoneyInput): digitar como o cliente digita, com vírgula ("3480,00").
 - "Repetir até" preenchido: a RPC cria TODAS as contas até a data (migração 20260626130000), não só a janela de 3 meses.
 - Observador `OBS` guarda em `window.__avisos` texto de erro e toast de erro; o passo final devolve a lista (tem de sair vazia).
"""
import hashlib
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TUT_HOME = os.path.normpath(os.path.join(HERE, '..', '..'))
NARR = os.path.join(TUT_HOME, 't13', 'narracao')
FAKE_NOW = '2026-11-10T08:30:00-03:00'
NOMES = ['Abertura', 'A tela e as abas', 'Os quatro cartões do topo', 'Lista e calendário', 'Lançar uma conta', 'A conta que já nasce paga',
         'Parcelar uma conta', 'A conta que se repete', 'Só esta ou esta e as futuras', 'Dar baixa', 'O fiado na mesma lista',
         'Anexar o comprovante', 'Filtrar a lista', 'Recapitulando']
_I = ['t13/inicio']
SEMENTE = {0: _I, 1: _I, 2: _I, 3: _I, 4: _I, 5: _I + ['t13/apos-cap04'], 6: _I + ['t13/apos-cap05'], 7: _I + ['t13/apos-cap06'],
           8: _I + ['t13/apos-cap07'], 9: _I + ['t13/apos-cap08'], 10: _I + ['t13/apos-cap09'], 11: _I + ['t13/apos-cap10'],
           12: _I + ['t13/apos-cap11'], 13: _I + ['t13/apos-cap11']}
PDF = 'assets/comprovante-pix-energia-outubro.pdf'   # relativo ao roteiro (rec/t13/), fictício (t13_sementes.py pdf)

sys.path.insert(0, NARR)
try:
    from tts_textos import CAPS   # noqa: E402  (texto atual de cada capítulo, para conferir que a fala do capNN.json é a de hoje)
except Exception:   # pragma: no cover
    CAPS = {}
try:
    TROCAS = json.load(open(os.path.join(NARR, 'config_narracao.json'), encoding='utf8'))['trocas']
except Exception:   # pragma: no cover
    TROCAS = []


def norm(s):
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode().lower()
    return ''.join(ch for ch in s if ch.isalnum())


def texto_atual(n):
    """palavras (grafia da legenda) do texto de hoje do tts_textos.py: tags fora, trocas de pronúncia aplicadas"""
    t = re.sub(r'\[[a-z ]+\]', ' ', CAPS.get(n, ''))
    for fala, leg in sorted(TROCAS, key=lambda p: -len(p[0])):
        t = t.replace(fala, leg)
    return [norm(w) for w in t.split() if norm(w)]


def carregar_voz(n):
    d = json.load(open(os.path.join(NARR, f'cap{n:02d}.json'), encoding='utf8'))
    words, linhas = d['words'], d['linhas']
    if CAPS:
        if texto_atual(n) != [norm(w['w']) for w in words if norm(w['w'])]:
            print(f'  AVISO cap{n:02d}: a fala do capNN.json não é a do tts_textos.py de hoje (rode o preparar_aula.sh de novo)')
    return words, linhas, float(d['dur']), bool(d.get('estimado'))


# ---------------------------------------------------------------- observador de avisos de erro (aceite: tem de sair vazio)
OBS = ("(()=>{window.__avisos=[];const re=/N[ãa]o foi poss[ií]vel|Erro ao|Tente novamente|Algo deu errado|Falha ao|Something went wrong|inv[áa]lid/i;"
       "const chk=(t)=>{t=(t||'').trim();const m=t&&t.match(new RegExp('[^]{0,40}('+re.source+')[^]{0,40}','i'));"
       "if(m&&window.__avisos.length<10)window.__avisos.push(m[0].replace(/[\\n\\r\\t ]+/g,' '))};new MutationObserver(ms=>{for(const m of ms){"
       "m.addedNodes.forEach(n=>chk(n.textContent));if(m.type==='characterData')chk(m.target.textContent)}}).observe(document.body,"
       "{childList:true,subtree:true,characterData:true});chk(document.body.innerText);"
       "setInterval(()=>{document.querySelectorAll('[data-sonner-toast][data-type=error]').forEach(t=>{const s='TOAST DE ERRO: '+t.textContent.trim().slice(0,90);"
       "if(!window.__avisos.includes(s)&&window.__avisos.length<10)window.__avisos.push(s)})},300);return 1})()")
# animações do framer-motion montadas depois da carga começam "no futuro" com o relógio simulado (docs/08, T5 cap10): acerta o início
ANIM = "(()=>{const a=document.getAnimations().filter(x=>x.currentTime<0);a.forEach(x=>x.startTime=document.timeline.currentTime);return a.length})()"


class Cap:
    def __init__(s, n, pace=0.5, cps=40, start=(760, 470), prewarm=None, setup=None):
        s.n = n
        s.words, s.linhas, s.dur, s.estimado = carregar_voz(n)
        s.steps, s.pending, s.anchors = [], [], []
        s.pace, s.cps, s.start = pace, cps, start
        s.prewarm = prewarm or ['/login']
        s.setup = list(setup or []) + [{'do': 'eval', 'js': OBS}]

    # ---- tempo
    def L(s, i):
        return round(s.linhas[i - 1]['s'], 2)

    def W(s, i, palavra, nth=None, fim=False):
        q = norm(palavra)
        hits = [w for w in s.words if w['linha'] == i - 1 and norm(w['w']) == q]
        if nth is None:
            if len(hits) > 1:
                print(f'  aviso cap{s.n:02d}: "{palavra}" aparece {len(hits)} vezes na linha {i}: usei a 1a (passe nth)')
            nth = 0
        if len(hits) <= nth:
            raise SystemExit(f'cap{s.n:02d}: palavra "{palavra}" (#{nth}) não achada na linha {i}: '
                             + ' '.join(w['w'] for w in s.words if w['linha'] == i - 1))
        return hits[nth]['e' if fim else 's']

    def A(s, i, palavra, folga=0.6, nth=None):
        t = round(max(0.0, s.W(i, palavra, nth) - folga), 2)
        s.anchors.append((i, palavra, t))
        return t

    def A_ou(s, i, palavras, folga=0.6):
        """âncora na 1ª palavra da lista que existe na linha (fala de hoje ou a proposta em propostas_fala.md)"""
        for p in palavras:
            if any(w['linha'] == i - 1 and norm(w['w']) == norm(p) for w in s.words):
                return s.A(i, p, folga, nth=0)
        raise SystemExit(f'cap{s.n:02d}: nenhuma de {palavras} na linha {i}')

    # ---- marcas e passos
    def flush(s, ate):
        keep = []
        for mt, mi in s.pending:
            if round(mt, 2) <= ate + 1e-9:
                s.steps.append({'do': 'mark', 'name': f'L{mi}', 'at': round(mt, 2)})
            else:
                keep.append((mt, mi))
        s.pending = keep

    def add(s, d):
        if d.get('at') is not None:
            lim = 0.8 if d.get('do') == 'hover' else 0.25
            for mt, mi in s.pending:
                if d['at'] < mt <= d['at'] + lim:
                    d['at'] = round(mt, 2)
            if d.get('do') == 'type':
                for mt, mi in list(s.pending):
                    if d['at'] < mt <= d['at'] + 2.6:
                        s.steps.append({'do': 'mark', 'name': f'L{mi}', 'at': round(d['at'], 2)})
                        s.pending.remove((mt, mi))
            s.flush(d['at'])
        s.steps.append(d)
        return d

    def mark(s, i):
        t = s.L(i) - 0.9 if s.L(i) > 0.9 else s.L(i)
        if t <= 0:
            s.steps.append({'do': 'mark', 'name': f'L{i}', 'at': 0})
        else:
            s.pending.append((round(t, 2), i))

    def _p(s, d, at, label, kw):
        if at is not None:
            d['at'] = round(at, 2)
        if label:
            d['label'] = label
        d.update(kw)
        return s.add(d)

    def click(s, target, at=None, label=None, **kw):
        return s._p({'do': 'click', 'target': target}, at, label, kw)

    def hover(s, target, seconds=0.6, at=None, label=None, **kw):
        kw.setdefault('optional', True)
        kw.setdefault('timeout', 4)
        return s._p({'do': 'hover', 'target': target, 'seconds': seconds}, at, label, kw)

    def type(s, target, text, at=None, label=None, cps=None, **kw):
        d = {'do': 'type', 'target': target, 'text': text}
        if cps:
            d['cps'] = cps
        return s._p(d, at, label, kw)

    def digita(s, campo, text, at_clique, at_texto, label, cps=40, clear=False):
        """clique no campo (ancorado) e digitação sem novo clique, ancorada na palavra (docs/04, "Digitar sem esperar")"""
        s.click(campo, at=at_clique, label=label + ' (clique no campo)')
        kw = {'noClick': True}
        if clear:
            kw['clear'] = True
        return s.type(campo, text, at=at_texto, label=label, cps=cps, **kw)

    def marcar(s, target, at=None, label=None):
        """registra o retângulo do alvo para a câmera (zoom) sem mexer no mouse: `type` sem clique e sem texto"""
        return s._p({'do': 'type', 'target': target, 'text': '', 'noClick': True, 'optional': True, 'timeout': 4}, at, label, {})

    def press(s, key, at=None, label=None, **kw):
        return s._p({'do': 'press', 'key': key}, at, label, kw)

    def ev(s, js, at=None, label=None, **kw):
        return s._p({'do': 'eval', 'js': js}, at, label, kw)

    def pause(s, seconds):
        return s.add({'do': 'pause', 'seconds': seconds})

    def wait(s, seconds):
        return s.add({'do': 'wait', 'seconds': seconds})

    def waitfor(s, **kw):
        return s.add({'do': 'waitFor', **kw})

    def upload(s, target, arquivo, at=None, label=None, **kw):
        return s._p({'do': 'upload', 'target': target, 'file': arquivo}, at, label, kw)

    def rolar(s, by, at=None, label=None, ponto=(800, 470), duration=0.5, after=100):
        return s._p({'do': 'scroll', 'point': {'x': ponto[0], 'y': ponto[1]}, 'by': by, 'duration': duration, 'after': after}, at, label, {})

    def confere(s, escopo, esperados, label, tentativas=20):
        """`eval` que LÊ a tela e compara com a fala: "OK: ..." ou "DIFERENTE: ..." (o resumo.py acusa). Escopo: 'dlg' (a última
        janela aberta), 'main', 'body' ou um seletor CSS. Tenta por ~tentativas x 0,3 s."""
        linha = escopo[4:] if escopo.startswith('row:') else None   # 'row:<texto>': a linha da lista que contém o texto
        sel = 'main tbody tr' if linha is not None else {'dlg': '[role=dialog],[role=alertdialog]', 'main': 'main', 'body': 'body'}.get(escopo, escopo)
        esp = [esperados] if isinstance(esperados, str) else list(esperados)
        js = ("(async()=>{const norm=t=>t.replace(/[\\s\\u00a0]+/g,' ').toLowerCase();const esp=%s;let out='';"
              "for(let i=0;i<%d;i++){const els=[...document.querySelectorAll(%s)].filter(e=>!%s||e.innerText.includes(%s));const el=%s?els[els.length-1]:els[0];"
              "if(!el){out='DIFERENTE: sem elemento';}else{const t=norm(el.innerText);const falta=esp.filter(e=>!t.includes(norm(e)));"
              "if(!falta.length)return 'OK: '+esp.join(' | ');out='DIFERENTE: faltou '+JSON.stringify(falta)+' em: '+t.slice(0,240);}"
              "await new Promise(r=>setTimeout(r,300));}return out})()") % (json.dumps(esp, ensure_ascii=False), tentativas, json.dumps(sel),
                                                                            'true' if linha is not None else 'false', json.dumps(linha or ''),
                                                                            'true' if escopo == 'dlg' else 'false')
        return s.add({'do': 'eval', 'js': js, 'label': 'confere ' + label})

    def confere_ausente(s, escopo, texto, label, espera=0.6):
        """LÊ a tela depois de `espera` s e acusa se o texto apareceu"""
        sel = {'dlg': '[role=dialog]', 'main': 'main', 'body': 'body'}.get(escopo, escopo)
        js = ("(async()=>{await new Promise(r=>setTimeout(r,%d));" % int(espera * 1000) + "const el=document.querySelector(%s);"
              "const t=(el?el.innerText:'').replace(/[\\s\\u00a0]+/g,' ').toLowerCase();"
              "return t.includes(%s)?'DIFERENTE: apareceu '+%s:'OK: ausente '+%s})()") % (json.dumps(sel), json.dumps(texto.lower()), json.dumps(texto), json.dumps(texto))
        return s.add({'do': 'eval', 'js': js, 'label': 'confere ' + label})

    def fim(s):
        s.flush(1e9)
        s.steps.append({'do': 'eval', 'js': 'JSON.stringify(window.__avisos || "sem observador")', 'label': 'avisos de erro na tela'})
        s.steps.append({'do': 'mark', 'name': 'FIM', 'at': round(s.dur, 2)})

    def encaixa_hovers(s, custo=0.6, minimo=0.15):
        """o hover termina antes do próximo passo com `at` (uma marca Ln, outro gesto): parada (`seconds`) encurtada até caber"""
        for k, st in enumerate(s.steps):
            if st.get('do') != 'hover' or st.get('at') is None:
                continue
            prox = next((x['at'] for x in s.steps[k + 1:] if x.get('at') is not None), None)
            if prox is None:
                continue
            cabe = round(prox - 0.05 - st['at'] - custo, 2)
            if st['seconds'] > cabe:
                st['seconds'] = max(minimo, cabe)

    def out(s):
        s.encaixa_hovers()
        est = ' ESTIMADA' if s.estimado else ''
        return {
            'name': f't13-cap{s.n:02d}',
            'title': f'T13 · Cap. {s.n} · {NOMES[s.n]} (narração{est} {str(round(s.dur, 1)).replace(".", ",")} s; marcas L1..L{len(s.linhas)} = '
                     f'início de cada linha do roteiro; FAKE_NOW {FAKE_NOW}; logado como Rafael Nogueira)',
            'seed': f't13-cap{s.n:02d}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
            'start': {'x': s.start[0], 'y': s.start[1]},
            'anonymous': True, 'storage': dict(STORAGE),
            'seedExtra': list(SEMENTE[s.n]),
            'prewarm': s.prewarm, 'setup': s.setup, 'steps': s.steps,
        }


# ---------------------------------------------------------------- alvos
MAIN = 'main'
DLG = '[role=dialog]'
BTN = lambda n, within=None, **kw: {'role': 'button', 'name': n, 'exact': True, **({'within': within} if within else {}), **kw}
TXT = lambda t, within=MAIN, **kw: {'text': t, 'exact': True, 'within': within, **kw}
SEL = lambda s, **kw: {'selector': s, **kw}
OPT = lambda n, **kw: {'role': 'option', 'name': n, **kw}
AGUARDA = {'do': 'waitFor', 'idle': True}


def stable_id(chave):
    """o mesmo UUID do `@id:<chave>` das sementes (rec/fakebase/core/util.mjs, stableId)"""
    h = bytearray(hashlib.sha1(('domiflix-fake:' + chave).encode()).digest())
    h[6] = (h[6] & 0x0F) | 0x50
    h[8] = (h[8] & 0x3F) | 0x80
    x = h[:16].hex()
    return f'{x[:8]}-{x[8:12]}-{x[12:16]}-{x[16:20]}-{x[20:32]}'


RAFAEL = stable_id('user.rafael')
VERSAO = '1.59.154'
HOJE = FAKE_NOW[:10]
STORAGE = {'app_version': VERSAO, 'notification_shown_version': VERSAO, 'pwa-install-dismissed': 'true', 'theme': 'light',
           f'daily-tasks-reminder-last-shown-{RAFAEL}': HOJE, 'initial-preferences-set': 'true'}
LOGIN = [{'do': 'waitFor', 'target': {'label': 'E-mail'}, 'timeout': 30},
         {'do': 'type', 'target': {'label': 'E-mail'}, 'text': '$TUT_USER', 'cps': 40},
         {'do': 'type', 'target': {'label': 'Senha', 'exact': True}, 'text': '$TUT_SENHA', 'cps': 40},
         {'do': 'click', 'target': {'role': 'button', 'name': 'Entrar', 'exact': True}},
         {'do': 'waitFor', 'text': 'Olá, Rafael!', 'timeout': 30}, AGUARDA]
IR_TELA = [{'do': 'goto', 'url': '/contas-pagar-receber'}, {'do': 'waitFor', 'text': 'Água e esgoto de outubro', 'timeout': 30}, AGUARDA]


TOGGLE = SEL('header button.h-8.w-8')            # recolher/abrir o menu lateral (sem rótulo; o 1º botão do cabeçalho)
RECOLHE = [{'do': 'click', 'target': TOGGLE, 'noScroll': True}, {'do': 'wait', 'seconds': 0.8}]


def setup_tela(extra=()):
    """login e a tela Contas a Pagar/Receber (aba Todas, Lista) com o menu lateral recolhido (a 1280 px, aberto, a tabela corta a
    coluna Ações e quebra as descrições em 3 linhas: exploração e1); `extra` antes do acerto das animações"""
    return LOGIN + IR_TELA + RECOLHE + list(extra) + [{'do': 'eval', 'js': ANIM}]


# ---------------------------------------------------------------- JavaScript (rolagens suaves, colar)
ACHA_ROLAGEM = ("const rolagem=(el)=>{let c=el&&el.parentElement;while(c&&c!==document.body){const s=getComputedStyle(c);"
                "if(/(auto|scroll)/.test(s.overflowY)&&c.scrollHeight>c.clientHeight+4)return c;c=c.parentElement;}return null};")
SUAVE = ("await new Promise(res=>{const t0=performance.now();const f=t=>{const p=Math.min(1,(t-t0)/DUR),e=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;"
         "c.scrollTop=y0+dy*e;p<1?requestAnimationFrame(f):res()};requestAnimationFrame(f)});")


def js_rola(seletor, y, dur_ms=700):
    """rolagem suave do contêiner que rola o elemento `seletor` até o topo dele ficar em y px CSS (limitado ao que o contêiner rola).
    Devolve o topo final, 'ok' (já estava), 'SEM ALVO' ou 'SEM ROLAGEM'."""
    return ("(async()=>{" + ACHA_ROLAGEM + f"const el=[...document.querySelectorAll({json.dumps(seletor)})].filter(e=>e.offsetParent)[0];if(!el)return 'SEM ALVO';"
            "const c=rolagem(el);if(!c)return 'SEM ROLAGEM';"
            f"let dy=Math.round(el.getBoundingClientRect().top-{int(y)});const y0=c.scrollTop;dy=Math.max(-y0,Math.min(c.scrollHeight-c.clientHeight-y0,dy));"
            "if(Math.abs(dy)<3)return 'ok';" + SUAVE.replace('DUR', str(int(dur_ms))) + "return Math.round(el.getBoundingClientRect().top)})()")


def js_rola_texto(texto, y, dur_ms=700, escopo=DLG):
    """como js_rola, com o alvo achado pelo texto (o menor elemento do escopo cujo texto é exatamente `texto`)"""
    return ("(async()=>{" + ACHA_ROLAGEM + f"const el=[...document.querySelectorAll({json.dumps(escopo + ' *')})].filter(e=>e.textContent.trim()==={json.dumps(texto)}&&e.offsetParent)"
            ".sort((a,b)=>a.textContent.length-b.textContent.length||a.children.length-b.children.length)[0];if(!el)return 'SEM ALVO';"
            "const c=rolagem(el);if(!c)return 'SEM ROLAGEM';"
            f"let dy=Math.round(el.getBoundingClientRect().top-{int(y)});const y0=c.scrollTop;dy=Math.max(-y0,Math.min(c.scrollHeight-c.clientHeight-y0,dy));"
            "if(Math.abs(dy)<3)return 'ok';" + SUAVE.replace('DUR', str(int(dur_ms))) + "return Math.round(el.getBoundingClientRect().top)})()")


def js_topo(dur_ms=700):
    """rolagem suave do <main> (o contêiner que rola a tela) até o topo"""
    return ("(async()=>{const c=[...document.querySelectorAll('main')].find(e=>/(auto|scroll)/.test(getComputedStyle(e).overflowY)&&e.scrollHeight>e.clientHeight+4);"
            "if(!c)return 'SEM ROLAGEM';const y0=c.scrollTop,dy=-y0;if(y0<3)return 'ok';" + SUAVE.replace('DUR', str(int(dur_ms))) + "return 'topo:'+Math.round(c.scrollTop)})()")


def js_colar(texto):
    """cola o texto no campo em foco (execCommand insertText: o React recebe o input), ~0,05 s em vez de digitar letra a letra"""
    return ("(()=>{const e=document.activeElement;if(!e||!/^(INPUT|TEXTAREA)$/.test(e.tagName))return 'SEM ALVO (nada em foco)';"
            f"document.execCommand('insertText',false,{json.dumps(texto)});return e.value}})()")


# ---------------------------------------------------------------- alvos da tela Contas a Pagar/Receber
ABA = lambda n: SEL(f"main button:text-is('{n}')")                                   # abas Todas / A Pagar / A Receber (<button>)
BUSCA = SEL("main input[aria-label='Buscar contas']")                                # a cópia visível no computador
LISTA_BTN = {'role': 'radio', 'name': 'Visão em lista'}
CAL_BTN = {'role': 'radio', 'name': 'Visão em calendário'}
NOVA = BTN('Nova conta', MAIN)
FILTROS = SEL("main button:has-text('Filtros')")
LINHA = lambda t: SEL(f"main tbody tr:has-text('{t}')")
NA_LINHA = lambda t, s: SEL(f"main tbody tr:has-text('{t}') {s}")
TXT_LINHA = lambda t, x: SEL(f"main tbody tr:has-text('{t}') :text-is('{x}')")
COL = lambda n: SEL(f"main thead th:has-text('{n}')")
CARTAO = lambda t: {'text': t, 'exact': True, 'within': MAIN}
DIA_CAL = lambda d: SEL(f"main div.grid-cols-7 > button:has(span:text-is('{d}'))")    # dia do calendário da tela
ETIQ_CAL = lambda t: SEL(f"main div.grid-cols-7 > button span[title^='{t}']")       # etiqueta da conta no dia
TRIANGULO = SEL("main div.grid-cols-7 > button:has(svg[class*='triangle'])")
POP = '[data-radix-popper-content-wrapper]'
DIA = lambda d: SEL(f"{POP} button[name='day']:not(.day-outside):text-is('{d}')")      # dia no calendário de um campo de data
PROX_MES = SEL(f"{POP} button[name='next-month']")
COMBO = lambda txt: SEL(f"{DLG} button[role=combobox]:has-text('{txt}')")
CAMPO = lambda i: SEL(f'#{i}')
SECAO = lambda t: SEL(f"{DLG} button[aria-expanded]:has-text('{t}')")                 # "Mais detalhes", "Parcelar ou repetir"
DLG_BTN = lambda t: SEL(f"{DLG} button:has-text('{t}')")
RODAPE = lambda t: BTN(t)                                                            # botões do rodapé da janela (usar com noScroll)
CARTAO_PAG = lambda rot: SEL(f"{DLG} button[aria-label='{rot}']")                    # "Dinheiro (Caixa)", "Pix / Transferência (Banco)"


def colar(c, campo, texto, at_clique, at_texto, label):
    """clica no campo (cursor) e cola o texto (sem digitar letra a letra): texto longo que a fala só cita"""
    c.click(campo, at=at_clique, label=label + ' (clique no campo)')
    return c.ev(js_colar(texto), at=at_texto, label=label)


def js_avanca_meses(n, ms=170):
    """clica `n` vezes no "próximo mês" do calendário aberto, um a cada `ms` (o mês passa na tela, sem o custo de n cliques do robô)"""
    return ("(async()=>{const b=()=>document.querySelector(\"[data-radix-popper-content-wrapper] button[name='next-month']\");if(!b())return 'SEM ALVO';"
            f"for(let i=0;i<{int(n)};i++){{b().click();await new Promise(r=>setTimeout(r,{int(ms)}));}}"
            "const c=document.querySelector('[data-radix-popper-content-wrapper] [aria-live], [data-radix-popper-content-wrapper] .rdp-caption_label');"
            "return c?c.textContent.trim():'ok'})()")


def escolhe_dia(c, campo, dia, at_campo, at_dia, label, meses=0, at_meses=None):
    """campo de data do computador: abre o calendário, avança `meses` (cursor no botão do próximo mês, os cliques por eval) e clica o dia"""
    c.click(campo, at=at_campo, label=label + ' (abre o calendário)')
    if meses:
        c.hover(PROX_MES, 0.15, at=at_meses, label=f'{label}: o cursor no próximo mês')
        c.ev(js_avanca_meses(meses), label=f'{label}: avança {meses} meses')
    return c.click(DIA(dia), at=at_dia, label=label)


# ================================================================ capítulos
def cap00():
    """Abertura: o Dashboard sob a ilustração das contas espalhadas (L1 a L3) e o cartão Antes: (L4); na L5 o menu Financeiro >
    Contas a Pagar/Receber, filmado, e a tela abre na aba Todas."""
    setup = LOGIN + IR_TELA + [{'do': 'goto', 'url': '/dashboard'}, {'do': 'waitFor', 'text': 'Olá, Rafael!', 'timeout': 25}, AGUARDA,
                               {'do': 'eval', 'js': ANIM}]
    c = Cap(0, setup=setup, start=(760, 300))
    for i in (1, 2, 3, 4):
        c.mark(i)
    c.mark(5)
    c.hover(SEL("button:has(span:text-is('Financeiro'))"), 0.4, at=c.A(5, 'menu,', 0.5), label='o cursor vai ao menu lateral')
    c.click(SEL("button:has(span:text-is('Financeiro'))"), at=c.A(5, 'Financeiro,', 0.6), label='abre o grupo Financeiro (menu lateral)')
    c.click({'role': 'link', 'name': 'Contas a Pagar/Receber'}, at=c.A(5, 'Contas', 0.6), label='Contas a Pagar/Receber (menu lateral)')
    c.waitfor(text='Água e esgoto de outubro', timeout=15)
    c.ev(ANIM)
    c.click(TOGGLE, at=c.A(5, 'Vamos', 0.6), label='recolhe o menu lateral (aviso da edição: recolher o menu dá espaço para a lista)', noScroll=True)
    c.hover(ABA('Todas'), 1.0, at=c.A(5, 'conhecer', 0.4), label='a tela abre na aba Todas')
    c.fim()
    return c


def cap01():
    """A tela e as abas: caminho e título, as três abas (A Pagar fica vermelha), as colunas, a água vencida, a energia pendente, o
    aluguel pago e o botão Nova conta."""
    c = Cap(1, setup=setup_tela(), start=(760, 300))
    c.mark(1)
    c.hover(SEL('main h1'), 0.8, at=c.A(1, 'Esta', 0.3), label='título Contas a Pagar/Receber')
    c.hover(ABA('Todas'), 0.8, at=c.A(1, 'Todas,', 0.6), label='aba Todas')
    c.mark(2)
    c.click(ABA('A Pagar'), at=c.A(2, 'Pagar', 0.7), label='aba A Pagar (fica vermelha)')
    c.hover(ABA('A Pagar'), 0.8, at=c.A(2, 'vermelho,', 0.5), label='A Pagar em vermelho')
    c.click(ABA('A Receber'), at=c.A(2, 'Receber,', 0.7), label='aba A Receber')
    c.mark(3)
    c.click(ABA('Todas'), at=c.A(2, 'entra.', -0.4), label='volta para Todas')
    c.ev(js_rola('main thead', 110), at=c.A(3, 'Cada', -0.1), label='desce a tela até o cabeçalho da lista')
    c.hover(COL('Descrição'), 0.25, at=c.A(3, 'descrição,', 0.5), label='coluna Descrição')
    c.hover(COL('Categoria'), 0.25, at=c.A(3, 'categoria,', 0.5), label='coluna Categoria')
    c.hover(COL('Vencimento'), 0.25, at=c.A(3, 'vencimento,', 0.5), label='coluna Vencimento')
    c.hover(COL('Valor'), 0.2, at=c.A(3, 'valor', 0.5), label='coluna Valor')
    c.hover(COL('Status'), 0.6, at=c.A(3, 'status.', 0.4), label='coluna Status')
    c.mark(4)
    c.hover(TXT_LINHA('Água e esgoto de outubro', 'Água e esgoto de outubro'), 0.8, at=c.A(4, 'água', 0.6), label='a água de outubro')
    c.hover(TXT_LINHA('Água e esgoto de outubro', 'Vencida'), 0.8, at=c.A(4, 'Vencida,', 0.6), label='status Vencida')
    c.hover(TXT_LINHA('Água e esgoto de outubro', '05/11/2026'), 1.0, at=c.A(4, 'data', 0.6), label='vencimento 05/11/2026 em vermelho')
    c.mark(5)
    c.hover(TXT_LINHA('Energia elétrica de outubro', 'Energia elétrica de outubro'), 0.6, at=c.A(5, 'energia', 0.6), label='a energia de outubro')
    c.hover(TXT_LINHA('Energia elétrica de outubro', 'Pendente'), 0.6, at=c.A(5, 'Pendente.', 0.6), label='status Pendente')
    c.hover(TXT_LINHA('Aluguel do galpão de novembro', 'Aluguel do galpão de novembro'), 0.6, at=c.A(5, 'aluguel', 0.6), label='o aluguel do galpão')
    c.hover(TXT_LINHA('Aluguel do galpão de novembro', 'Paga'), 0.8, at=c.A(5, 'Paga.', 0.6), label='status Paga e Quitada em 05/11/2026')
    c.mark(6)
    c.hover(NOVA, 1.4, at=c.A(6, 'este:', 0.6), label='botão Nova conta')
    c.fim()
    return c


def cap02():
    """Os quatro cartões: o que cada um soma (zoom em Total a Pagar/Receber e em Vencidas/Vence em 7 dias), a ilustração da linha do
    tempo (L3) e a troca de aba com os números iguais."""
    c = Cap(2, setup=setup_tela(), start=(760, 400))
    c.mark(1)
    c.hover(CARTAO('Total a Pagar'), 0.6, at=c.A(1, 'cartões', 0.6), label='os quatro cartões lá de cima')
    c.hover(CARTAO('Total a Receber'), 0.6, at=c.A(1, 'quanto', 0.6, nth=1), label='quanto tem pra receber')
    c.hover(CARTAO('Vencidas'), 0.6, at=c.A(1, 'apertando.', 0.6), label='o que está apertando')
    c.mark(2)
    c.hover(CARTAO('Total a Pagar'), 1.6, at=c.A(2, 'Total', 0.6, nth=0), label='ZOOM cartões Total a Pagar e Total a Receber')
    c.hover(CARTAO('Total a Receber'), 1.6, at=c.A(2, 'Total', 0.6, nth=1), label='Total a Receber')
    c.mark(3)
    c.mark(4)
    c.hover(CARTAO('Vencidas'), 1.4, at=c.A(4, 'Esses', 0.4), label='ZOOM cartões Vencidas e Vence em 7 dias')
    c.hover(CARTAO('Vence em 7 dias'), 1.4, at=c.A(4, 'receber.', 0.6), label='Vence em 7 dias')
    c.mark(5)
    c.click(ABA('A Pagar'), at=c.A(5, 'troquei', 0.7), label='troca para a aba A Pagar')
    c.hover(CARTAO('Total a Pagar'), 0.8, at=c.A(5, 'números', 0.6), label='os números não mudaram')
    c.click(ABA('Todas'), at=c.A(5, 'inteira,', 0.7), label='volta para Todas')
    c.fim()
    return c


def cap03():
    """Lista e calendário: os botões Lista/Calendário, o calendário de novembro (vermelho a pagar, verde a receber), o triângulo do dia 5,
    o dia 10 com Marcar pago e Editar, o aviso do topo e a volta para a Lista."""
    c = Cap(3, setup=setup_tela(), start=(760, 400))
    c.mark(1)
    c.hover(LISTA_BTN, 0.8, at=c.A(1, 'Lista,', 0.6), label='Lista (marcado)')
    c.hover(CAL_BTN, 0.6, at=c.A(1, 'Calendário.', 0.6, nth=1), label='Calendário')
    c.mark(2)
    c.click(CAL_BTN, at=c.A(2, 'calendário,', 0.7), label='abre o Calendário')
    c.waitfor(target=DIA_CAL('10'), timeout=10)
    c.ev(ANIM)
    c.ev(js_rola('main div.grid.grid-cols-7', 290), at=c.A(2, 'cada', 0.0), label='desce a tela: o aviso e as quatro primeiras semanas')
    c.hover(ETIQ_CAL('Água e esgoto de outubro'), 0.6, at=c.A(2, 'Vermelho', 0.6), label='etiqueta vermelha: a pagar')
    c.hover(ETIQ_CAL('Fatura venda #'), 0.6, at=c.A(2, 'verde,', 0.6), label='etiqueta verde: a receber')
    c.mark(3)
    c.hover(TRIANGULO, 1.0, at=c.A(3, 'triângulo', 0.6), label='dia 5 com o triângulo de vencida')
    c.hover(ETIQ_CAL('Água e esgoto de outubro'), 0.8, at=c.A(3, 'água,', 0.6), label='a água, do dia cinco')
    c.mark(4)
    c.click(DIA_CAL('10'), at=c.A(4, 'Clicando', 0.6), label='clica no dia 10')
    c.waitfor(text='Contas de 10/11/2026', timeout=8)
    c.hover(DLG_BTN('Marcar pago'), 0.5, at=c.A(4, 'pagar', 0.6), label='Marcar pago (na janela do dia)')
    c.hover(DLG_BTN('Editar'), 0.6, at=c.A(4, 'editar.', 0.6), label='Editar (na janela do dia)')
    c.mark(5)
    c.press('Escape', at=c.L(5) - 0.9, label='fecha a janela do dia (Esc)')
    c.wait(0.5)
    c.hover({'text': 'Saldos de clientes/fornecedores', 'within': MAIN}, 2.0, at=c.A(5, 'saldo', 0.6), label='o aviso do topo')
    c.hover({'text': 'Saldos de clientes/fornecedores', 'within': MAIN}, 1.0, at=c.A(5, 'avisa.', 0.6), label='a própria tela avisa')
    c.mark(6)
    c.click(LISTA_BTN, at=c.A(6, 'Lista.', 0.7), label='volta para a Lista')
    c.fim()
    return c


def cap04():
    """Lançar uma conta: Nova conta da manutenção da prensa (Hidráulica Moretti, R$ 3.480,00, 19/11, Manutenção de máquinas, Pátio,
    previsto Conta Principal) e a linha nova na lista."""
    c = Cap(4, setup=setup_tela(), start=(760, 400))
    c.mark(1)
    c.click(NOVA, at=c.A(1, 'Nova', 0.7, nth=1), label='Nova conta')
    c.waitfor(text='Cadastre uma conta a pagar ou a receber com vencimento.', timeout=8)
    c.mark(2)
    c.hover(COMBO('A pagar (despesa)'), 1.6, at=c.A(2, 'Tipo', 0.8), label='Tipo: A pagar (despesa)')
    c.mark(3)
    c.digita(CAMPO('bill-amount'), '3480,00', c.A(3, 'Valor,', 0.8), c.A(3, 'três', 0.05), 'ZOOM Valor 3.480,00')
    c.mark(4)
    c.digita(CAMPO('bill-description'), 'Manutenção da prensa enfardadeira', c.A(4, 'Descrição,', 0.7), c.A(4, 'o', 0.0, nth=0), 'Descrição')
    escolhe_dia(c, CAMPO('bill-due'), '19', c.A(4, 'Vencimento,', 0.7), c.A(4, 'dezenove', 0.5), 'Vencimento 19/11/2026')
    c.mark(5)
    c.click(CAMPO('bill-category'), at=c.A(5, 'Categoria', 0.7), label='Categoria (abre a lista)')
    c.type({'placeholder': 'Pesquisar categoria...'}, 'Manut', at=c.A(5, 'gasto', 0.05), label='busca Manut', noClick=True)
    c.click(OPT('Manutenção de máquinas'), at=c.A(5, 'Manutenção', 0.6), label='Manutenção de máquinas')
    c.mark(6)
    c.hover(SEL(f"{DLG} button[role=combobox]:has(span:text-is('Fornecedor'))"), 0.8, at=c.A(6, 'Fornecedor.', 0.6), label='o tipo já vem em Fornecedor')
    c.click(COMBO('Selecione o fornecedor'), at=c.A(6, 'É', 0.6, nth=1), label='Selecione o fornecedor')
    c.type({'placeholder': 'Pesquisar fornecedor...'}, 'Moretti', at=c.A(6, 'escolher', 0.05), label='busca Moretti', noClick=True)
    c.waitfor(target=OPT('Hidráulica Moretti Ltda'), timeout=8)
    c.click(OPT('Hidráulica Moretti Ltda'), at=c.A(6, 'Moretti.', 0.3), label='Hidráulica Moretti Ltda')
    c.mark(7)
    c.hover(CAMPO('bill-cost-center'), 1.2, at=c.A(7, 'Centro', 0.6), label='Centro de custo')
    c.click(CAMPO('bill-cost-center'), at=c.A(7, 'pátio,', 0.7, nth=0), label='Centro de custo (abre a lista)')
    c.click(OPT('Pátio'), at=c.A(7, 'Pátio.', 0.5, nth=1), label='Pátio')
    c.mark(8)
    c.ev(js_rola_texto('Pagamento previsto', 300), at=c.L(8) - 0.9, label='desce a janela até o bloco Dinheiro')
    c.click(COMBO('Não definido'), at=c.A(8, 'previsto,', 0.7), label='Pagamento previsto (abre a lista)')
    c.click(OPT('Conta Principal'), at=c.A(8, 'Principal.', 0.6), label='Conta Principal (grupo Contas)')
    c.hover(COMBO('Conta Principal'), 1.5, at=c.A(8, 'sugerida.', 0.8), label='previsto: Conta Principal')
    c.mark(9)
    c.click(RODAPE('Criar conta'), at=c.A(9, 'Criar', 0.7), label='Criar conta', noScroll=True)
    c.waitfor(text='Conta criada', timeout=10)
    c.ev(js_rola("main tbody tr:has-text('Manutenção da prensa enfardadeira')", 420), at=c.A(9, 'Pronto:', 0.3), label='desce a tela até a linha nova')
    c.hover(TXT_LINHA('Manutenção da prensa enfardadeira', 'Manutenção da prensa enfardadeira'), 1.2, at=c.A(9, 'manutenção', 0.6),
            label='ZOOM a linha nova, com 19/11/2026 e R$ 3.480,00')
    c.hover(TXT_LINHA('Manutenção da prensa enfardadeira', 'Pendente'), 0.6, at=c.A(9, 'pendente,', 0.6), label='Pendente')
    c.hover(TXT_LINHA('Manutenção da prensa enfardadeira', '19/11/2026'), 0.4, at=c.A(9, 'data,', 0.6), label='vencimento 19/11/2026')
    c.hover(TXT_LINHA('Manutenção da prensa enfardadeira', 'Manutenção de máquinas'), 0.4, at=c.A(9, 'categoria', 0.6), label='categoria e Conta Principal')
    c.hover(TXT_LINHA('Manutenção da prensa enfardadeira', 'Hidráulica Moretti Ltda'), 0.8, at=c.A(9, 'fornecedor.', 0.6), label='Hidráulica Moretti Ltda')
    c.confere('row:Manutenção da prensa enfardadeira', ['19/11/2026', 'R$ 3.480,00', 'Pendente', 'Hidráulica Moretti Ltda'], 'a linha nova')
    c.fim()
    return c


def cap05():
    """A conta que já nasce paga: conserto do pneu da empilhadeira (R$ 180,00, 09/11, Manutenção de máquinas, Pátio, Conta Principal),
    "Já paguei essa conta" com a data de ontem; na busca "pneu", a linha Paga."""
    c = Cap(5, setup=setup_tela(), start=(760, 400))
    c.mark(1)
    c.click(NOVA, at=c.A(1, 'paga?', 0.7), label='Nova conta')
    c.waitfor(text='Cadastre uma conta a pagar ou a receber com vencimento.', timeout=8)
    c.mark(2)
    c.digita(CAMPO('bill-amount'), '180,00', c.A(2, 'Preencho', 0.2), c.A(2, 'como', 0.0), 'Valor 180,00')
    colar(c, CAMPO('bill-description'), 'Conserto do pneu da empilhadeira', c.A(2, 'conta:', 0.3), c.A(2, 'o', 0.0, nth=0), 'Descrição (colada)')
    escolhe_dia(c, CAMPO('bill-due'), '9', c.A(2, 'valor,', -0.1), c.A(2, 'descrição,', -0.1), 'Vencimento 09/11/2026 (ontem)')
    c.click(CAMPO('bill-category'), at=c.A(2, 'data', 0.0), label='Categoria (abre a lista)')
    c.type({'placeholder': 'Pesquisar categoria...'}, 'máquinas', at=c.A(2, 'ontem,', 0.0), label='busca máquinas', noClick=True)
    c.click(OPT('Manutenção de máquinas'), at=c.A(2, 'categoria', 0.0), label='Manutenção de máquinas')
    c.click(CAMPO('bill-cost-center'), at=c.A(2, 'e', 0.0), label='Centro de custo (abre a lista)')
    c.mark(3)
    c.click(OPT('Pátio'), at=c.A(2, 'custo.', 0.0), label='Pátio')
    c.ev(js_rola_texto('Pagamento previsto', 300), at=c.L(3) - 0.5, label='desce a janela até o bloco Dinheiro')
    c.click(COMBO('Não definido'), at=c.A(3, 'previsto,', 0.6), label='Pagamento previsto (abre a lista)')
    c.click(OPT('Conta Principal'), at=c.A(3, 'Principal.', 0.6), label='Conta Principal')
    c.mark(4)
    c.click(CAMPO('bill-pay-now'), at=c.A(4, 'ligo', 0.7), label='liga Já paguei essa conta')
    c.hover({'text': 'Registra o pagamento agora', 'within': DLG}, 1.2, at=c.A(4, 'registra', 0.6), label='Registra o pagamento agora: a conta já nasce quitada')
    escolhe_dia(c, CAMPO('bill-pay-date'), '9', c.A(4, 'Data', 0.7), c.A(4, 'ontem.', 0.5), 'Data do pagamento 09/11/2026')
    c.mark(5)
    c.click(RODAPE('Criar conta'), at=c.A(5, 'Criar', 0.7), label='Criar conta', noScroll=True)
    c.waitfor(text='Conta criada e paga', timeout=10)
    c.digita(BUSCA, 'pneu', c.A(5, 'Ela', 0.7), c.A(5, 'já', 0.05, nth=0), 'busca pneu')
    c.waitfor(target=LINHA('Conserto do pneu da empilhadeira'), timeout=8)
    c.hover(TXT_LINHA('Conserto do pneu da empilhadeira', 'Paga'), 1.0, at=c.A(5, 'Paga,', 0.5), label='ZOOM a linha Paga, Quitada em 09/11/2026')
    c.hover(TXT_LINHA('Conserto do pneu da empilhadeira', 'Conta Principal'), 1.2, at=c.A(5, 'Conta', 0.6, nth=1), label='Conta Principal')
    c.confere('row:Conserto do pneu da empilhadeira', ['R$ 180,00', 'Paga', '09/11/2026'], 'a conta nasceu paga')
    c.mark(6)
    c.hover(TXT_LINHA('Conserto do pneu da empilhadeira', '09/11/2026'), 1.5, at=c.A(6, 'opção', 0.6), label='a linha (a câmera fica)')
    c.fim()
    return c


def cap06():
    """Parcelar: pneus do caminhão truck, Auto Peças Vale Forte, R$ 7.080,00 em 3x (Configurar faturamento); três contas na busca
    "pneus". L8 e L9 sob a ilustração."""
    c = Cap(6, setup=setup_tela(), start=(760, 400))
    c.mark(1)
    c.click(NOVA, at=c.A(1, 'vezes.', 0.7, nth=0), label='Nova conta')
    c.waitfor(text='Cadastre uma conta a pagar ou a receber com vencimento.', timeout=8)
    c.mark(2)
    c.digita(CAMPO('bill-amount'), '7080,00', c.A(2, 'Valor', 0.8, nth=0), c.A(2, 'sete', 0.05), 'ZOOM Valor 7.080,00')
    colar(c, CAMPO('bill-description'), 'Pneus do caminhão truck', c.A(2, 'não', 0.6), c.A(2, 'valor', 0.0, nth=1), 'Descrição (colada)')
    c.mark(3)
    escolhe_dia(c, CAMPO('bill-due'), '23', c.A(3, 'Vencimento,', 0.7), c.A(3, 'vinte', 0.5), 'Vencimento 23/11/2026 (1ª parcela)')
    c.click(CAMPO('bill-category'), at=c.A(3, 'Categoria', 0.8), label='Categoria (abre a lista)')
    c.type({'placeholder': 'Pesquisar categoria...'}, 'veículos', at=c.A(3, 'Categoria', 0.05), label='Manutenção de veículos (busca + Enter)',
           noClick=True, submit=True)
    c.click(COMBO('Selecione o fornecedor'), at=c.A(3, 'fornecedor,', 0.3), label='Selecione o fornecedor')
    c.type({'placeholder': 'Pesquisar fornecedor...'}, 'Vale', at=c.A(3, 'como', 0.05), label='busca Vale', noClick=True)
    c.waitfor(target=OPT('Auto Peças Vale Forte'), timeout=8)
    c.mark(4)
    c.click(OPT('Auto Peças Vale Forte'), at=c.A(3, 'antes.', 0.0), label='Auto Peças Vale Forte')
    c.ev(js_rola_texto('Parcelar ou repetir', 260), at=c.A(4, 'Embaixo,', 0.0), label='desce a janela até Parcelar ou repetir')
    c.click(SECAO('Parcelar ou repetir'), at=c.A(4, 'Parcelar', 0.3, nth=0), label='abre Parcelar ou repetir')
    c.click(CAMPO('installment-toggle'), at=c.A(4, 'ligo', 0.7), label='liga Parcelar')
    c.waitfor(text='Configurar faturamento', timeout=8)
    c.mark(5)
    c.click(SEL(f"{DLG}:has-text('Nº de parcelas') button:text-is('3')"), at=c.A(5, 'três', 0.7), label='Nº de parcelas: 3')
    c.hover(SEL(f"{DLG}:has-text('Nº de parcelas') input[aria-label='Valor da parcela 2']"), 1.6, at=c.A(5, 'dois', 0.6),
            label='ZOOM as três linhas e a faixa Soma das parcelas')
    c.hover({'text': 'Soma das parcelas', 'within': f"{DLG}:has-text('Nº de parcelas')"}, 1.2, at=c.A(5, 'faixa', 0.6), label='faixa verde Soma das parcelas')
    c.mark(6)
    c.click(RODAPE('Aplicar faturamento'), at=c.A(6, 'Aplicar', 0.7), label='Aplicar faturamento', noScroll=True)
    c.hover({'text': '3x — 1º venc. 23/11/2026', 'within': DLG}, 1.6, at=c.A(6, 'resumo', 0.6), label='resumo 3x — 1º venc. 23/11/2026 — total R$ 7.080,00')
    c.mark(7)
    c.click(RODAPE('Criar conta'), at=c.A(7, 'Criar', 0.7), label='Criar conta', noScroll=True)
    c.waitfor(text='3 parcelas criadas', timeout=10)
    c.digita(BUSCA, 'pneus', c.A(7, 'Pronto,', 0.6), c.A(7, 'três', 0.05), 'busca pneus')
    c.waitfor(target=LINHA('Pneus do caminhão truck (parcela 3/3)'), timeout=8)
    c.hover(TXT_LINHA('Pneus do caminhão truck (parcela 2/3)', '23/12/2026'), 1.2, at=c.A(7, 'criadas.', 0.5), label='as três parcelas')
    c.confere('main tbody', ['23/11/2026', '23/12/2026', '23/01/2027', 'R$ 2.360,00'], 'três parcelas de R$ 2.360,00')
    c.mark(8)
    c.mark(9)
    c.fim()
    return c


def cap07():
    """Repetir: aluguel da empilhadeira, R$ 2.300,00, mensal, a partir de 12/11/2026 até 12/04/2027; na busca "aluguel da", as contas
    criadas. L7 sob a ilustração."""
    c = Cap(7, setup=setup_tela(), start=(760, 400))
    c.mark(1)
    c.click(NOVA, at=c.A(1, 'dois', 0.7), label='Nova conta')
    c.waitfor(text='Cadastre uma conta a pagar ou a receber com vencimento.', timeout=8)
    c.mark(2)
    c.digita(CAMPO('bill-amount'), '2300,00', c.L(2) - 0.9, c.A(2, 'Valor,', 0.3), 'ZOOM Valor 2.300,00')
    colar(c, CAMPO('bill-description'), 'Aluguel da empilhadeira', c.A(2, 'descrição', -0.1), c.A(2, 'e', 0.0, nth=0), 'Descrição (colada)')
    c.click(CAMPO('bill-category'), at=c.A(2, 'categoria,', 0.0), label='Categoria (abre a lista)')
    c.type({'placeholder': 'Pesquisar categoria...'}, 'Aluguel', at=c.A(2, 'como', 0.0), label='Aluguel (busca + Enter)', noClick=True, submit=True)
    escolhe_dia(c, CAMPO('bill-due'), '12', c.A(2, 'Vencimento', 0.5), c.A(2, 'doze', 0.5), 'Vencimento 12/11/2026')
    c.mark(3)
    c.ev(js_rola_texto('Parcelar ou repetir', 260), at=c.L(3) - 0.9, label='desce a janela até Parcelar ou repetir')
    c.click(SECAO('Parcelar ou repetir'), at=c.A(3, 'Parcelar', 0.6), label='abre Parcelar ou repetir')
    c.click(CAMPO('recurrence-toggle'), at=c.A(3, 'ligo', 0.7), label='liga Repete?')
    c.waitfor(target=CAMPO('recurrence-frequency'), timeout=6)
    c.ev(js_rola_texto('Repetir até (opcional)', 420), at=c.A(3, 'gera', 0.0), label='desce até Frequência e Repetir até')
    c.hover({'text': 'Gera contas automaticamente', 'within': DLG}, 1.0, at=c.A(3, 'frequência', 0.6), label='Gera contas automaticamente na frequência escolhida')
    c.mark(4)
    c.click(CAMPO('recurrence-frequency'), at=c.A(4, 'semanal,', 0.7), label='Frequência (abre: Semanal, Mensal, Anual)')
    c.click(OPT('Mensal'), at=c.A(4, 'mensal,', 0.6, nth=1), label='Mensal')
    c.hover(CAMPO('recurrence-interval'), 0.8, at=c.A(4, 'cada', 0.6), label='A cada 1')
    c.mark(5)
    escolhe_dia(c, CAMPO('recurrence-end'), '12', c.A(5, 'Repetir', 0.7), c.A(5, 'abril,', 0.4), 'Repetir até 12/04/2027',
                meses=5, at_meses=c.A(5, 'até,', 0.4))
    c.hover({'text': 'Deixe vazio para repetir sem data-fim.', 'within': DLG}, 1.4, at=c.A(5, 'Sem', 0.6, nth=0), label='Deixe vazio para repetir sem data-fim.')
    c.mark(6)
    c.click(RODAPE('Criar conta'), at=c.A(6, 'Criar', 0.7), label='Criar conta', noScroll=True)
    c.waitfor(text='Conta recorrente criada', timeout=10)
    c.digita(BUSCA, 'aluguel da', c.A(6, 'Repara:', 0.6), c.A(6, 'já', 0.05), 'busca aluguel da')
    c.waitfor(target=LINHA('12/01/2027'), timeout=8)
    c.hover(TXT_LINHA('12/11/2026', '12/11/2026'), 0.4, at=c.A(6, 'novembro,', 0.5), label='a conta de novembro')
    c.hover(TXT_LINHA('12/12/2026', '12/12/2026'), 0.4, at=c.A_ou(6, ['dezembro', 'até'], 0.5), label='a de dezembro')
    c.hover(TXT_LINHA('12/04/2027', '12/04/2027'), 1.0, at=c.A_ou(6, ['abril.', 'janeiro.'], 0.5), label='até a de abril (a RPC cria todas até a data de parar)')
    c.confere('main tbody', ['12/11/2026', '12/12/2026', '12/01/2027', '12/02/2027', '12/03/2027', '12/04/2027', 'R$ 2.300,00'], 'as seis contas do aluguel da empilhadeira')
    c.mark(7)
    c.fim()
    return c


def cap08():
    """Só esta ou esta e as futuras: na busca "aluguel da", Editar na de 12/12 (a pergunta da recorrência), Esta e as futuras com o
    vencimento 15/12 (o aviso do deslocamento), Salvar; Excluir mostra a mesma pergunta e é cancelado. L3 sob a ilustração."""
    c = Cap(8, setup=setup_tela(), start=(760, 400))
    c.mark(1)
    c.digita(BUSCA, 'aluguel da', c.A(1, 'locadora', 0.6), c.A(1, 'pediu', 0.05), 'busca aluguel da')
    c.waitfor(target=LINHA('12/12/2026'), timeout=8)
    c.hover(TXT_LINHA('12/12/2026', '12/12/2026'), 0.8, at=c.A(1, 'dezembro.', 0.6), label='a conta de dezembro')
    c.mark(2)
    c.click(NA_LINHA('12/12/2026', "button[title='Editar']"), at=c.A(2, 'editar', 0.7), label='lápis Editar na de dezembro')
    c.waitfor(text='Editar conta recorrente', timeout=8)
    c.hover(DLG_BTN('Só esta conta'), 0.6, at=c.A(2, 'só', 0.6), label='Só esta conta')
    c.hover(DLG_BTN('Esta e as futuras'), 0.8, at=c.A(2, 'esta', 0.6, nth=1), label='Esta e as futuras')
    c.mark(3)
    c.mark(4)
    c.click(DLG_BTN('Esta e as futuras'), at=c.A(4, 'Escolho', 0.6), label='Esta e as futuras')
    c.waitfor(text='Altere os dados da conta.', timeout=8)
    escolhe_dia(c, CAMPO('bill-due'), '15', c.A(4, 'mudo', 0.7), c.A(4, 'quinze', 0.5), 'Vencimento 15/12/2026')
    c.hover({'text': 'Esta data e as futuras serão deslocadas pelo mesmo período.', 'within': DLG}, 1.4, at=c.A(4, 'aviso:', 0.6),
            label='ZOOM aviso: as futuras andam o mesmo tanto')
    c.mark(5)
    c.click(RODAPE('Salvar'), at=c.A(5, 'Salvar.', 0.7), label='Salvar', noScroll=True)
    c.waitfor(text='Conta atualizada', timeout=10)
    c.hover(TXT_LINHA('12/11/2026', '12/11/2026'), 0.4, at=c.A(5, 'Novembro', 0.5), label='novembro ficou no dia 12')
    c.hover(TXT_LINHA('15/12/2026', '15/12/2026'), 0.4, at=c.A(5, 'dezembro', 0.5), label='dezembro no dia 15')
    c.hover(TXT_LINHA('15/04/2027', '15/04/2027'), 0.8, at=c.A_ou(5, ['diante', 'janeiro'], 0.5), label='de dezembro em diante no dia 15')
    c.confere('main tbody', ['12/11/2026', '15/12/2026', '15/01/2027', '15/02/2027', '15/03/2027', '15/04/2027'], 'vencimentos depois do Salvar')
    c.mark(6)
    c.click(NA_LINHA('15/01/2027', "button[title='Excluir']"), at=c.A(6, 'Excluir', 0.7), label='lixeira Excluir na de janeiro')
    c.waitfor(text='Excluir conta recorrente', timeout=8)
    c.hover(DLG_BTN('Esta e as futuras'), 1.2, at=c.A(6, 'Esta', 0.6), label='Esta e as futuras (vermelho)')
    c.click(DLG_BTN('Cancelar'), at=c.A(6, 'cancelo.', 0.6), label='Cancelar')
    c.fim()
    return c


def cap09():
    """Dar baixa: a energia inteira por Pix (Conta Principal) e a prensa em parte (R$ 1.740,00, o resto para 30/11). L6 e L7 sob a
    ilustração (a busca troca de "energia" para "prensa" por baixo dela)."""
    c = Cap(9, setup=setup_tela(), start=(760, 400))
    c.mark(1)
    c.click(ABA('A Pagar'), at=c.A(1, 'pagar.', 0.7), label='aba A Pagar')
    c.digita(BUSCA, 'energia', c.A(1, 'Dar', 0.6), c.A(1, 'baixa', 0.05), 'busca energia')
    c.waitfor(target=LINHA('Energia elétrica de outubro'), timeout=8)
    c.hover(TXT_LINHA('Energia elétrica de outubro', 'Energia elétrica de outubro'), 1.4, at=c.A(1, 'energia', 0.6),
            label='a energia: Conta Principal, 10/11/2026, R$ 1.874,30, Pendente')
    c.mark(2)
    c.click(NA_LINHA('Energia elétrica de outubro', "button[title='Marcar pago']"), at=c.A(2, 'Marcar', 0.7), label='Marcar pago (energia)')
    c.waitfor(text='Energia elétrica de outubro · Restante', timeout=8)
    c.hover(CARTAO_PAG('Pix / Transferência (Banco)'), 0.6, at=c.A(2, 'Pix', 0.6), label='Pix/Transferência já marcado')
    c.hover(COMBO('Conta Principal'), 0.8, at=c.A(2, 'Principal,', 0.6), label='Conta bancária: Conta Principal')
    c.hover(CAMPO('pay-amount-transfer'), 1.0, at=c.A(2, 'inteiro.', 0.6), label='o valor inteiro 1.874,30')
    c.mark(3)
    c.hover(CARTAO_PAG('Dinheiro (Caixa)'), 0.8, at=c.A(3, 'quem', 0.6), label='cartões Dinheiro e Pix (dica da permissão)')
    c.hover(CARTAO_PAG('Pix / Transferência (Banco)'), 0.6, at=c.A(3, 'Pix', 0.6), label='Pix')
    c.hover(CARTAO_PAG('Dinheiro (Caixa)'), 1.0, at=c.A(3, 'caixa,', 0.6), label='Dinheiro (Caixa)')
    c.mark(4)
    c.hover({'text': 'Quita a conta', 'within': DLG}, 1.6, at=c.A(4, 'confirma', 0.6), label='ZOOM o valor 1.874,30 e Quita a conta')
    c.mark(5)
    c.hover(CAMPO('pay-date'), 0.4, at=c.A(5, 'data', 0.6), label='Data do pagamento 10/11/2026')
    c.click(RODAPE('Confirmar pagamento'), at=c.A(5, 'Confirmar', 0.7), label='Confirmar pagamento', noScroll=True)
    c.waitfor(text='Pagamento registrado', timeout=10)
    c.hover(TXT_LINHA('Energia elétrica de outubro', 'Paga'), 1.0, at=c.A(5, 'Paga.', 0.5), label='a energia está Paga')
    c.confere('row:Energia elétrica de outubro', ['Paga', '10/11/2026'], 'energia paga')
    c.mark(6)
    c.digita(BUSCA, 'prensa', c.A(6, 'dica:', 0.0), c.A(6, 'baixa', 0.0), 'busca prensa (sob a ilustração)', clear=True)
    c.waitfor(target=LINHA('Manutenção da prensa enfardadeira'), timeout=8)
    c.mark(7)
    c.mark(8)
    c.hover(TXT_LINHA('Manutenção da prensa enfardadeira', 'Manutenção da prensa enfardadeira'), 0.8, at=c.A(8, 'Agora', 0.3),
            label='a prensa: 19/11/2026, R$ 3.480,00, Pendente')
    c.click(NA_LINHA('Manutenção da prensa enfardadeira', "button[title='Marcar pago']"), at=c.A(8, 'pediu', 0.7), label='Marcar pago (prensa)')
    c.waitfor(text='Manutenção da prensa enfardadeira · Restante', timeout=8)
    c.mark(9)
    c.digita(CAMPO('pay-amount-transfer'), '1740,00', c.A(9, 'valor,', 0.8), c.A(9, 'mil', 0.05), 'ZOOM o valor 1.740,00 e Falta R$ 1.740,00 para quitar',
             clear=True)
    c.hover({'text': 'Falta R$ 1.740,00 para quitar', 'within': DLG}, 1.0, at=c.A(9, 'falta', 0.6), label='Falta R$ 1.740,00 para quitar')
    c.mark(10)
    c.hover(CAMPO('remainder-due'), 0.8, at=c.A(10, 'Novo', 0.6), label='Novo vencimento do restante')
    escolhe_dia(c, CAMPO('remainder-due'), '30', c.A(10, 'Coloco', 0.7), c.A(10, 'trinta', 0.4), 'Novo vencimento 30/11/2026')
    c.mark(11)
    c.click(RODAPE('Confirmar pagamento'), at=c.A(11, 'Confirmar.', 0.7), label='Confirmar pagamento', noScroll=True)
    c.waitfor(text='Pagamento registrado', timeout=10)
    c.hover(TXT_LINHA('Manutenção da prensa enfardadeira', 'Parcial'), 0.8, at=c.A(11, 'Parcial:', 0.5),
            label='ZOOM Parcial, pago R$ 1.740,00 de R$ 3.480,00 e 30/11/2026')
    c.hover({'text': 'pago R$ 1.740,00 de R$ 3.480,00', 'within': MAIN}, 1.0, at=c.A(11, 'quanto', 0.5, nth=0), label='pago R$ 1.740,00 de R$ 3.480,00')
    c.hover(TXT_LINHA('Manutenção da prensa enfardadeira', '30/11/2026'), 0.8, at=c.A(11, 'trinta.', 0.6), label='vence dia 30')
    c.confere('row:Manutenção da prensa enfardadeira', ['Parcial', 'pago R$ 1.740,00 de R$ 3.480,00', '30/11/2026'], 'prensa parcial')
    c.fim()
    return c


def cap10():
    """O fiado: aba A Receber, busca "Quiririm" (linha Saldo R$ 4.870,00), Receber R$ 2.000,00 por Pix na Conta Principal (sobra
    R$ 2.870,00); busca "Fundição" (só as parcelas); L7 e L8 sob a ilustração; o lápis de uma parcela (sem clicar)."""
    c = Cap(10, setup=setup_tela(), start=(760, 400))
    c.mark(1)
    c.click(ABA('A Receber'), at=c.A(1, 'fiado.', 0.7), label='aba A Receber')
    c.digita(BUSCA, 'Quiririm', c.A(1, 'Ele', 0.6), c.A(1, 'aparece', 0.05), 'busca Quiririm')
    c.waitfor(target=LINHA('Aços Quiririm Ltda'), timeout=8)
    c.hover(TXT_LINHA('Aços Quiririm Ltda', 'Saldo'), 0.8, at=c.A(1, 'Saldo.', 0.6), label='chip roxo Saldo')
    c.hover(TXT_LINHA('Aços Quiririm Ltda', 'R$ 4.870,00'), 1.2, at=c.A(1, 'quatro', 0.6), label='R$ 4.870,00')
    c.mark(2)
    c.hover(TXT_LINHA('Aços Quiririm Ltda', 'Saldo'), 1.6, at=c.A(2, 'linha', 0.6), label='ZOOM o chip Saldo e o valor R$ 4.870,00')
    c.hover(TXT_LINHA('Aços Quiririm Ltda', 'Cliente'), 1.0, at=c.A(2, 'cliente', 0.6), label='Aços Quiririm Ltda, Cliente')
    c.confere('row:Aços Quiririm Ltda', ['Saldo', 'R$ 4.870,00', 'Cliente'], 'linha de saldo da Aços Quiririm')
    c.mark(3)
    c.click(NA_LINHA('Aços Quiririm Ltda', "button[title='Receber']"), at=c.A(3, 'Receber.', 0.7), label='Receber (saldo da Aços Quiririm)')
    c.waitfor(text='Receber de Aços Quiririm Ltda', timeout=8)
    c.click(COMBO('Dinheiro (Caixa)'), at=c.A(3, 'então', 0.4), label='Forma de recebimento (abre a lista)')
    c.click(OPT('Pix / Transferência (Banco)'), at=c.A(3, 'troco', -0.1), label='Pix / Transferência (Banco)')
    c.click(SEL(f"{DLG} button[role=combobox]", nth=1), at=c.A(3, 'Pix', 0.1, nth=1), label='Conta bancária (abre a lista)')
    c.click(OPT('Conta Principal'), at=c.A(3, 'Principal.', 0.6), label='Conta Principal')
    c.mark(4)
    c.digita(CAMPO('pay-fiado-amount'), '2000,00', c.A(4, 'pagou', 0.7), c.A(4, 'dois', 0.05, nth=0), 'ZOOM Valor 2.000,00 e Saldo após esta baixa', clear=True)
    c.hover({'text': 'Saldo após esta baixa', 'within': DLG}, 1.6, at=c.A(4, 'saldo', 0.6), label='Saldo após esta baixa: R$ 2.870,00')
    c.confere('dlg', ['Saldo após esta baixa: R$ 2.870,00'], 'saldo depois da baixa')
    c.mark(5)
    c.click(RODAPE('Confirmar recebimento'), at=c.A(5, 'Confirmar', 0.7), label='Confirmar recebimento', noScroll=True)
    c.waitfor(text='Recebimento registrado', timeout=10)
    c.hover(TXT_LINHA('Aços Quiririm Ltda', 'R$ 2.870,00'), 1.4, at=c.A(5, 'caiu', 0.5), label='o saldo caiu para R$ 2.870,00')
    c.confere('row:Aços Quiririm Ltda', ['R$ 2.870,00'], 'saldo de 2.870,00')
    c.mark(6)
    c.digita(BUSCA, 'Fundição', c.A(6, 'Agora', 0.2), c.A(6, 'repara', 0.05), 'busca Fundição', clear=True)
    c.waitfor(target=LINHA('18/01/2027'), timeout=8)
    c.hover(TXT_LINHA('17/11/2026', 'Fundição Bandeira do Vale'), 0.8, at=c.A(6, 'Bandeira', 0.6), label='Fundição Bandeira do Vale')
    c.hover(TXT_LINHA('17/12/2026', '17/12/2026'), 1.2, at=c.A(6, 'parcelas.', 0.6), label='só as três parcelas, nenhuma linha Saldo')
    c.confere_ausente('main tbody', 'Saldo', 'nenhuma linha Saldo da Fundição')
    c.mark(7)
    c.mark(8)
    c.mark(9)
    c.hover(NA_LINHA('17/11/2026', "button[title='Editar']"), 3.0, at=c.A(9, 'parcelas', 0.6), label='o lápis Editar de uma parcela (sem clicar)')
    c.fim()
    return c


def cap11():
    """Comprovante: busca "energia", Editar, Mais detalhes, Anexar o PDF fictício, Salvar; reabre e mostra a miniatura PDF."""
    c = Cap(11, setup=setup_tela(), start=(760, 400))
    c.mark(1)
    c.digita(BUSCA, 'energia', c.A(1, 'comprovante', 0.5), c.A(1, 'daquele', 0.05), 'busca energia')
    c.waitfor(target=LINHA('Energia elétrica de outubro'), timeout=8)
    c.hover(TXT_LINHA('Energia elétrica de outubro', 'Paga'), 1.0, at=c.A(1, 'guardado', 0.6), label='a energia, Paga')
    c.mark(2)
    c.click(NA_LINHA('Energia elétrica de outubro', "button[title='Editar']"), at=c.A(2, 'editar', 0.7), label='lápis Editar (energia)')
    c.waitfor(text='Altere os dados da conta.', timeout=8)
    c.ev(js_rola_texto('Mais detalhes', 300), at=c.A(2, 'e', 0.3, nth=0), label='desce a janela até Mais detalhes')
    c.click(SECAO('Mais detalhes'), at=c.A(2, 'Mais', 0.5), label='abre Mais detalhes')
    c.ev(js_rola_texto('Anexos (foto ou PDF)', 360), at=c.A(2, 'Aqui', 0.2), label='desce até Observações e Anexos')
    c.hover(CAMPO('bill-notes'), 0.6, at=c.A(2, 'observações', 0.6), label='Observações')
    c.hover({'text': 'Anexos (foto ou PDF)', 'within': DLG}, 0.6, at=c.A(2, 'anexos.', 0.6), label='Anexos (foto ou PDF)')
    c.mark(3)
    c.upload(DLG_BTN('Anexar'), PDF, at=c.A(3, 'Anexar,', 0.7), label='Anexar: comprovante-pix-energia-outubro.pdf')
    c.waitfor(target=SEL(f"{DLG} button[aria-label='Baixar anexo']"), timeout=10)
    c.hover(SEL(f"{DLG} button[aria-label='Baixar anexo']"), 1.2, at=c.A(3, 'PDF', 0.6), label='ZOOM a miniatura PDF')
    c.mark(4)
    c.click(RODAPE('Salvar'), at=c.A(4, 'Salvar.', 0.7), label='Salvar', noScroll=True)
    c.waitfor(text='Conta atualizada', timeout=10)
    c.mark(5)
    c.click(NA_LINHA('Energia elétrica de outubro', "button[title='Editar']"), at=c.A(5, 'abrir', 0.7), label='lápis Editar de novo')
    c.waitfor(text='Altere os dados da conta.', timeout=8)
    c.ev(js_rola_texto('Mais detalhes', 300), at=c.A(5, 'conta', 0.2), label='desce a janela até Mais detalhes')
    c.click(SECAO('Mais detalhes'), at=c.A(5, 'Mais', 0.5), label='abre Mais detalhes')
    c.ev(js_rola_texto('Anexos (foto ou PDF)', 360), at=c.A(5, 'detalhes.', -0.2), label='desce até os Anexos')
    c.waitfor(target=SEL(f"{DLG} button[aria-label='Baixar anexo']"), timeout=10)
    c.hover(SEL(f"{DLG} button[aria-label='Baixar anexo']"), 2.0, at=c.A(5, 'miniatura,', 0.6), label='a miniatura PDF (Baixar anexo), sem clicar')
    c.mark(6)
    c.fim()
    return c


def cap12():
    """Filtros: aba A Receber (linhas Saldo no fim), o painel Filtros, Status Pendente (as linhas de saldo saem, os cartões não mudam),
    Cliente/Fornecedor Fundição (as três parcelas) e Limpar filtros."""
    c = Cap(12, setup=setup_tela(), start=(760, 400))
    PAINEL = DLG
    ROT = lambda t: SEL(f"{PAINEL} label:text-is('{t}')")
    c.mark(1)
    c.click(ABA('A Receber'), at=c.A(1, 'Receber,', 0.7), label='aba A Receber')
    c.ev(js_rola('main tbody tr:last-child', 600), at=c.A(1, 'repara', 0.3), label='desce a tela até o fim da lista')
    c.hover(TXT_LINHA('Aços Quiririm Ltda', 'Saldo'), 1.2, at=c.A(1, 'saldo,', 0.6), label='as linhas de saldo, lá no fim')
    c.mark(2)
    c.click(FILTROS, at=c.A(2, 'Filtros.', 0.7), label='Filtros (abre o painel)')
    c.waitfor(target=ROT('Status'), timeout=8)
    c.hover(ROT('Status'), 0.25, at=c.A(2, 'status,', 0.5), label='Status')
    c.hover(ROT('Categoria'), 0.25, at=c.A(2, 'categoria,', 0.5), label='Categoria')
    c.hover(ROT('Cliente/Fornecedor'), 0.25, at=c.A(2, 'Cliente', 0.5), label='Cliente/Fornecedor')
    c.hover(ROT('Centro de custo'), 0.25, at=c.A(2, 'centro', 0.5), label='Centro de custo')
    c.hover(SEL(f"{PAINEL} label:has-text('Banco previsto')"), 0.25, at=c.A(2, 'banco', 0.5), label='Banco previsto')
    c.hover(ROT('Vencimento (período)'), 0.6, at=c.A(2, 'período', 0.5), label='Vencimento (período)')
    c.mark(3)
    c.click(SEL(f"{PAINEL} div:has(> label:text-is('Status')) button"), at=c.A(3, 'Status,', 0.7), label='Status (abre a lista)')
    c.click(SEL(f"{POP} label:has(span:text-is('Pendente'))"), at=c.A(3, 'Pendente', 0.6), label='marca Pendente')
    c.press('Escape', at=c.A(3, 'e', 0.3, nth=0), label='fecha a lista do Status (Esc)')
    c.click(RODAPE('Aplicar'), at=c.A(3, 'aplico.', 0.3), label='Aplicar', noScroll=True)
    c.hover(FILTROS, 1.6, at=c.A(3, 'botão', 0.6), label='ZOOM Filtros verde com o número 1')
    c.mark(4)
    c.hover(SEL('main tbody tr', nth='last'), 1.6, at=c.A(4, 'saíram.', 0.6), label='o fim da lista: sem as linhas de saldo')
    c.confere_ausente('main tbody', 'Saldo', 'as linhas de saldo saíram')
    c.mark(5)
    c.ev(js_topo(700), at=c.L(5) - 0.6, label='sobe a tela até os cartões')
    c.hover(CARTAO('Total a Receber'), 1.6, at=c.A(5, 'cartões', 0.4), label='os cartões continuam iguais')
    c.mark(6)
    c.click(FILTROS, at=c.A(6, 'Junto', 0.4), label='Filtros (de novo)')
    c.click(SEL(f"{PAINEL} button[role=combobox]:has-text('Todos')", nth=0), at=c.A(6, 'escolho', 0.7), label='Cliente/Fornecedor (abre a busca)')
    c.type({'placeholder': 'Buscar parceiro...'}, 'Fundição', at=c.A(6, 'a', 0.0, nth=0), label='busca Fundição', noClick=True)
    c.click(OPT('Fundição Bandeira do Vale'), at=c.A(6, 'Vale.', 0.6), label='Fundição Bandeira do Vale')
    c.click(RODAPE('Aplicar'), at=c.A(6, 'Pronto:', 0.3), label='Aplicar', noScroll=True)
    c.hover(SEL('main tbody tr', nth=1), 1.2, at=c.A(6, 'parcelas', 0.6), label='as três parcelas dela')
    c.confere('main tbody', ['Fundição Bandeira do Vale', '17/11/2026', '17/12/2026', '18/01/2027'], 'as três parcelas da Fundição')
    c.mark(7)
    c.click(FILTROS, at=c.A(7, 'ver', 0.6), label='Filtros (de novo)')
    c.click(RODAPE('Limpar filtros'), at=c.A(7, 'Limpar', 0.6), label='Limpar filtros', noScroll=True)
    c.click(RODAPE('Aplicar'), at=c.A(7, 'filtros.', 0.2), label='Aplicar', noScroll=True)
    c.ev(js_rola('main tbody tr:last-child', 600), at=c.A(7, 'E', 0.2), label='desce a tela até o fim da lista')
    c.hover(TXT_LINHA('Aços Quiririm Ltda', 'Saldo'), 1.0, at=c.A(7, 'voltam.', 0.6), label='as linhas de saldo voltam')
    c.fim()
    return c


def cap13():
    """Recapitulando (a montagem da edição usa trechos dos capítulos; este passeio pelo estado final fica de reserva). L7: cartão Próximo."""
    c = Cap(13, setup=setup_tela(), start=(760, 400))
    c.mark(1)
    c.hover(ABA('Todas'), 0.4, at=c.A(1, 'abas,', 0.6), label='as abas')
    c.hover(CARTAO('Total a Pagar'), 0.4, at=c.A(1, 'cartões', 0.6), label='os quatro cartões')
    c.hover(CAL_BTN, 0.6, at=c.A(1, 'calendário.', 0.6), label='o calendário')
    c.mark(2)
    c.ev(js_rola('main thead', 110), at=c.L(2) - 0.5, label='desce a tela até a lista')
    c.hover(TXT_LINHA('Manutenção da prensa enfardadeira', 'Manutenção da prensa enfardadeira'), 1.0, at=c.A(2, 'manutenção', 0.6), label='a manutenção da prensa')
    c.mark(3)
    c.hover(TXT_LINHA('Aluguel da empilhadeira', 'Aluguel da empilhadeira'), 1.0, at=c.A(3, 'aluguel', 0.6), label='o aluguel da empilhadeira')
    c.mark(4)
    c.hover(TXT_LINHA('Manutenção da prensa enfardadeira', 'Parcial'), 1.0, at=c.A(4, 'metade', 0.6), label='a prensa Parcial')
    c.mark(5)
    c.click(ABA('A Receber'), at=c.A(5, 'Recebeu', 0.6), label='aba A Receber')
    c.hover(TXT_LINHA('Aços Quiririm Ltda', 'R$ 2.870,00'), 1.0, at=c.A(5, 'Aços', 0.6), label='o saldo da Aços Quiririm')
    c.mark(6)
    c.hover(FILTROS, 1.0, at=c.A(6, 'filtrou', 0.6), label='Filtros')
    c.mark(7)
    c.fim()
    return c


CAPS_ROBO = {n: globals()[f'cap{n:02d}'] for n in range(14) if f'cap{n:02d}' in globals()}

if __name__ == '__main__':
    quais = [int(a) for a in sys.argv[1:]] or sorted(CAPS_ROBO)
    for n in quais:
        c = CAPS_ROBO[n]()
        if os.environ.get('ANCHORS'):
            for i, w, t in c.anchors:
                print(f'   anchor L{i} "{w}" -> {t}')
        d = c.out()
        last = -1
        for stp in d['steps']:   # o `at` precisa ser crescente
            if 'at' in stp:
                if stp['at'] < last - 1e-9:
                    print(f'  aviso cap{n:02d}: at {stp["at"]} < {last} em "{stp.get("label") or stp.get("name")}"')
                last = max(last, stp['at'])
        path = os.path.join(HERE, f'cap{n:02d}.json')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
        est = ' (voz ESTIMADA)' if c.estimado else ''
        print(f'cap{n:02d}: {len(d["steps"])} passos, narração {c.dur:.1f} s{est} -> {os.path.relpath(path, HERE)}')
