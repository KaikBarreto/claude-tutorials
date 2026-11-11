#!/usr/bin/env python3
"""T05 · Balança e impressora: o EcoTray. Gera rec/t05/cap00..cap11.json (roteiros do robô) a partir da voz (t05/narracao/capNN.json),
mais cap02w, cap04w, cap06w e cap09w (os trechos com "device": "windows", 1280x712, para as cenas de Windows).

EcoSistema 1.59.154 no Supabase falso (mundo da Recicla Vale Metais), computador 1280x800, logado como Rafael Nogueira (MASTER),
FAKE_NOW 2026-11-10T08:30:00-03:00 em todos os capítulos. O EcoTray (programa de Windows) é o EcoTray falso do robô
(rec/recorder/ecotray-falso.mjs, ws 8053 e 8054): desligado nos caps. 0 a 2, ligado sem balança nos caps. 3 a 6 (a "Balança do pátio" entra no
"Gravar" da cena, cap. 6), com a balança nos caps. 7 a 10; o resto (instalador, painel, bandeja) é cena de Windows montada por outro agente.
Cada passo é preso a uma palavra da fala: `at` = início da palavra - folga (o custo do gesto, docs/04 "Custo real dos gestos"), e a marca
Ln entra no início de cada linha. Quando a voz chegar, rodar de novo com o capNN.json da voz (nada a reescrever).
Rodar de qualquer pasta: `python3 -I rec/t05/gerar.py [NN ...]`.

Cadeia de sementes (seeds-extra/t05, perfil do Rafael): inicio (= apos-cap02) -> apos-cap04 (impressão direta com a POS-58) -> apos-cap05 (papel de
58 mm) -> apos-cap06 (balança ligada; os caps. 7 a 11 partem daqui). O cap. 3 e o cap. 4 partem de apos-cap02 (nada mudou no perfil).
"""
import json
import os
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TUT = os.path.normpath(os.path.join(HERE, '..', '..'))
NARR = os.path.join(TUT, 't05', 'narracao')
FN = '2026-11-10T08:30:00-03:00'
FAKE_NOW = {n: FN for n in range(12)}
NOMES = ['Abertura', 'O que é o EcoTray', 'Baixar e instalar', 'O pareamento automático', 'Conectar a impressora',
         'Largura do papel e impressão turbo', 'Conectar a balança', 'Peso somente pela balança', 'O indicador de peso',
         'Quando o EcoTray cai', 'Driver incompatível', 'Recapitulando']
SEMENTE = {0: 'inicio', 1: 'inicio', 2: 'inicio', 3: 'apos-cap02', 4: 'apos-cap02', 5: 'apos-cap04', 6: 'apos-cap05', 7: 'apos-cap06',
           8: 'apos-cap06', 9: 'apos-cap06', 10: 'apos-cap06', 11: 'apos-cap06'}


def stable_id(chave):
    """o mesmo UUID estável do Supabase falso (core/util.mjs stableId)"""
    import hashlib
    h = bytearray(hashlib.sha1(('domiflix-fake:' + chave).encode()).digest())
    h[6] = (h[6] & 0x0F) | 0x50
    h[8] = (h[8] & 0x3F) | 0x80
    x = h[:16].hex()
    return f'{x[:8]}-{x[8:12]}-{x[12:16]}-{x[16:20]}-{x[20:32]}'


RAFAEL = stable_id('user.rafael')
try:
    VERSAO = open(os.path.join(TUT, 'app', 'dist', '.versao-app'), encoding='utf8').read().strip() or '1.59.154'
except OSError:
    VERSAO = '1.59.154'
HOJE = '2026-11-10'
STORAGE = {
    'app_version': VERSAO, 'notification_shown_version': VERSAO, f'dominex:daily-tasks-shown:{RAFAEL}': HOJE,
    'pwa-install-dismissed': 'true', 'theme': 'light', f'daily-tasks-reminder-last-shown-{RAFAEL}': HOJE, 'initial-preferences-set': 'true',
}

# EcoTray falso por capítulo (rec/recorder/ecotray-falso.mjs): False = EcoTray fechado
BAL = {'id': 'bal-patio', 'name': 'Balança do pátio', 'connected': True, 'porta': 'COM3'}
ECO_SEM_BAL = {'balancas': [], 'casas': 3}                                    # caps. 3 a 6: ligado, sem balança cadastrada
ECO_PATIO = {'balancas': [BAL], 'padrao': 'bal-patio', 'casas': 3}            # caps. 7 a 11: com a "Balança do pátio"
GENERIC = {'name': 'Generic / Text Only', 'driver': 'Generic / Text Only', 'is_compatible': False, 'incompatible_reason': (
    'Driver "Generic / Text Only" só imprime texto puro — não suporta o cupom térmico (que é gerado como imagem). '
    'Troque pelo driver térmico real da sua impressora (ex: POS-58, GP-58, Elgin i9, Bematech, ou o driver oficial do fabricante).')}
ECO = {0: False, 1: False, 2: False, 3: ECO_SEM_BAL, 4: ECO_SEM_BAL, 5: ECO_SEM_BAL, 6: ECO_SEM_BAL,
       7: ECO_PATIO, 8: {**ECO_PATIO, 'mudo': True}, 9: {**ECO_PATIO, 'pesoInicial': 312}, 10: {**ECO_PATIO, 'impressoras': ['POS-58', GENERIC]},
       11: ECO_PATIO}


def sementes(n):
    return [f't05/{SEMENTE[n]}']


def norm(s):
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode().lower()
    return ''.join(ch for ch in s if ch.isalnum() or ch in '?')


def carregar_voz(n):
    d = json.load(open(os.path.join(NARR, f'cap{n:02d}.json'), encoding='utf8'))
    return d['words'], d['linhas'], float(d['dur']), bool(d.get('estimado'))


# Observador de avisos de erro na tela (aceite): "Não foi possível", "Erro ao", "Tente novamente", "indisponível", "Algo deu errado",
# "Falha ao", "Balança desconectada", "Pop-up bloqueado" e a faixa "Lembrete da trilha" da EcoFlix. O passo final devolve a lista.
OBS = ("(()=>{window.__avisos=[];const re=/N[ãa]o foi poss[ií]vel|Erro ao|Tente novamente|indispon[ií]vel|Algo deu errado|Falha ao|"
       "Balan[çc]a desconectada|Pop-up bloqueado|Popup bloqueado/i;"
       "const chk=(t)=>{t=(t||'').trim();const m=t&&t.match(new RegExp('[^]{0,40}('+re.source+')[^]{0,40}','i'));"
       "if(m&&window.__avisos.length<10)window.__avisos.push(m[0].replace(/[\\n\\r\\t ]+/g,' '))};new MutationObserver(ms=>{for(const m of ms){"
       "m.addedNodes.forEach(n=>chk(n.textContent));if(m.type==='characterData')chk(m.target.textContent)}}).observe(document.body,"
       "{childList:true,subtree:true,characterData:true});chk(document.body.innerText);"
       "setInterval(()=>{const f=document.querySelector('section[aria-label^=\"Lembrete da trilha\"]');"
       "if(f&&window.__avisos.length<10&&!window.__avisos.includes('TRILHA ECOFLIX'))window.__avisos.push('TRILHA ECOFLIX')},300);return 1})()")


class Cap:
    def __init__(s, n, pace=0.5, cps=9, start=(900, 440), setup=None, noscroll=False, sameTab=False, eco=None):
        s.n = n
        s.words, s.linhas, s.dur, s.estimada = carregar_voz(n)
        s.steps = []
        s.pace, s.cps, s.start = pace, cps, start
        s.noscroll = noscroll
        s.eco = eco   # EcoTray falso do capítulo: False = desligado; dict = configuração (rec/recorder/ecotray-falso.mjs)
        s.sameTab = sameTab
        s.setup = list(setup or []) + [{'do': 'eval', 'js': OBS}]
        s.anchors = []
        s.pending = []

    # ---- tempo
    def L(s, i):
        return round(s.linhas[i - 1]['s'], 2)

    def W(s, i, palavra, nth=0):
        q = norm(palavra)
        hits = [w for w in s.words if w['linha'] == i - 1 and norm(w['w']).startswith(q)]
        if len(hits) <= nth:
            raise SystemExit(f'cap{s.n:02d}: palavra "{palavra}" (#{nth}) não achada na linha {i}: ' + ' '.join(w['w'] for w in s.words if w['linha'] == i - 1))
        return hits[nth]['s']

    def A(s, i, palavra, folga=0.7, nth=0):
        """`at` = início da palavra - folga (folga = custo do gesto até o cursor chegar; negativa = depois da palavra)"""
        t = round(max(0.0, s.W(i, palavra, nth) - folga), 2)
        if i > 1 or s.L(i) > 0.5:
            t = max(t, round(s.L(i) - 0.2, 2))   # nunca antes da marca da linha (docs/08: o 1º gesto da linha em L(n) - 0,2)
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
        if d.get('at') is not None:
            lim = 0.8 if d.get('do') == 'hover' else 0.25
            for mt, mi in s.pending:
                if d['at'] < mt <= d['at'] + lim:
                    d['at'] = round(mt, 2)
            s.flush(d['at'])
        s.steps.append(d)
        return d

    def mark(s, i):
        t = s.L(i)
        if t <= 0.5:
            s.steps.append({'do': 'mark', 'name': f'L{i}', 'at': 0})
        else:
            s.pending.append((round(t - 0.2, 2), i))

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

    def hover(s, target, seconds=0.4, at=None, label=None, **kw):
        kw.setdefault('optional', True)
        kw.setdefault('timeout', 4)
        return s._p({'do': 'hover', 'target': target, 'seconds': seconds}, at, label, kw)

    def type(s, target, text, at=None, label=None, cps=None, **kw):
        d = {'do': 'type', 'target': target, 'text': text}
        if cps:
            d['cps'] = cps
        return s._p(d, at, label, kw)

    def press(s, key, at=None, label=None, **kw):
        return s._p({'do': 'press', 'key': key}, at, label, kw)

    def rolar(s, by, at=None, label=None, ponto=(900, 440), duration=0.5, after=100):
        return s._p({'do': 'scroll', 'point': {'x': ponto[0], 'y': ponto[1]}, 'by': by, 'duration': duration, 'after': after}, at, label, {})

    def cursor(s, ponto, at=None, label=None):
        """leva o cursor a um ponto neutro (scroll de 0 px): tira o mouse de cima de um menu ou de um cartão"""
        return s._p({'do': 'scroll', 'point': {'x': ponto[0], 'y': ponto[1]}, 'by': 0, 'duration': 0.3, 'after': 0}, at, label, {})

    def registra(s, target, at=None, label=None):
        """registra o retângulo do alvo para a câmera (zoom/destaque) SEM mexer o mouse"""
        return s._p({'do': 'type', 'target': target, 'text': '', 'noClick': True, 'optional': True, 'timeout': 4}, at, label, {})

    def pause(s, seconds):
        return s.add({'do': 'pause', 'seconds': seconds})

    def wait(s, seconds):
        return s.add({'do': 'wait', 'seconds': seconds})

    def waitfor(s, **kw):
        return s.add({'do': 'waitFor', **kw})

    def ev(s, js, at=None, label=None, **kw):
        return s._p({'do': 'eval', 'js': js}, at, label, kw)

    def confere(s, escopo, esperados, label):
        """`eval` que LÊ a tela e compara com o que a fala diz: "OK: ..." ou "DIFERENTE: ...". Escopo 'dlg' (a última janela), 'main',
        'body' ou um seletor CSS. Tenta por ~6,5 s."""
        sel = {'dlg': '[role=dialog]', 'main': 'main', 'body': 'body'}.get(escopo, escopo)
        esp = [esperados] if isinstance(esperados, str) else list(esperados)
        js = ("(async()=>{const norm=t=>t.replace(/[\\s\\u00a0]+/g,' ').toLowerCase();const esp=%s;let out='';"
              "for(let i=0;i<22;i++){const els=[...document.querySelectorAll(%s)];const el=%s?els[els.length-1]:els[0];"
              "if(!el){out='DIFERENTE: sem elemento';}else{const t=norm(el.innerText);const falta=esp.filter(e=>!t.includes(norm(e)));"
              "if(!falta.length)return 'OK: '+esp.join(' | ');out='DIFERENTE: faltou '+JSON.stringify(falta)+' em: '+t.slice(0,260);}"
              "await new Promise(r=>setTimeout(r,300));}return out})()") % (json.dumps(esp, ensure_ascii=False), json.dumps(sel), 'true' if escopo == 'dlg' else 'false')
        return s.add({'do': 'eval', 'js': js, 'label': 'confere ' + label})

    def confere_campos(s, esperados, label, escopo='[role=dialog]'):
        """lê o VALOR dos campos (input/textarea) do escopo e compara com o que a fala diz"""
        esp = [esperados] if isinstance(esperados, str) else list(esperados)
        js = ("(async()=>{const esp=%s;let out='';for(let i=0;i<12;i++){const v=[...document.querySelectorAll(%s+' input, '+%s+' textarea')].map(e=>e.value).join(' | ');"
              "const falta=esp.filter(e=>!v.includes(e));if(!falta.length)return 'OK: '+esp.join(' | ');out='DIFERENTE: faltou '+JSON.stringify(falta)+' em: '+v.slice(0,260);"
              "await new Promise(r=>setTimeout(r,300));}return out})()") % (json.dumps(esp, ensure_ascii=False), json.dumps(escopo), json.dumps(escopo))
        return s.add({'do': 'eval', 'js': js, 'label': 'confere ' + label})

    # ---- EcoTray falso (rec/recorder/ecotray-falso.mjs; passos `balanca` e `ecotray` do robô)
    def peso(s, kg, at=None, label=None, subir=0.8, oscilar=0.8):
        d = {'do': 'balanca', 'peso': kg, 'subir': subir, 'oscilar': oscilar}
        return s._p(d, at, label, {})

    def ecotray(s, at=None, label=None, **kw):
        return s._p({'do': 'ecotray'}, at, label, kw)

    def fim(s):
        s.flush(1e9)
        s.steps.append({'do': 'eval', 'js': 'JSON.stringify(window.__avisos || "sem observador")', 'label': 'avisos de erro na tela'})
        s.steps.append({'do': 'mark', 'name': 'FIM', 'at': round(s.dur, 2)})

    def out(s):
        d = {
            'name': f't05-cap{s.n:02d}',
            'title': f'T05 · Cap. {s.n} · {NOMES[s.n]} (narração {str(round(s.dur, 1)).replace(".", ",")} s{" ESTIMADA" if s.estimada else ""}; '
                     f'marcas L1..L{len(s.linhas)} = início de cada linha do roteiro; FAKE_NOW {FAKE_NOW[s.n]})',
            'seed': f't05-cap{s.n:02d}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
            'start': {'x': s.start[0], 'y': s.start[1]},
            'anonymous': True, 'storage': dict(STORAGE),
            'seedExtra': sementes(s.n),
            'prewarm': ['/login'], 'setup': s.setup, 'steps': s.steps,
        }
        if s.sameTab:
            d['sameTab'] = True
        d['ecotray'] = s.eco if s.eco is not None else False
        return d



# ---------------------------------------------------------------- alvos
BTN = lambda n, **kw: {'role': 'button', 'name': n, 'exact': True, **kw}
BTNX = lambda n, **kw: {'role': 'button', 'name': n, **kw}
TXT = lambda t, **kw: {'text': t, 'exact': True, **kw}
TXTX = lambda t, **kw: {'text': t, **kw}
SEL = lambda s, **kw: {'selector': s, **kw}
OPT = lambda n, **kw: {'role': 'option', 'name': n, **kw}
PH = lambda p, **kw: {'placeholder': p, **kw}
DLG = '[role=dialog]'
NEUTRO = (1000, 560)          # ponto neutro para o cursor descansar (fora de menu, cartão e botão)
TOPO_DASH = (760, 120)        # no Dashboard o neutro fica no alto: em (1000, 560) o gráfico "Evolução da Margem" abre a dica

# ---------------------------------------------------------------- setup (fora do vídeo)
LOGIN = [
    {'do': 'waitFor', 'target': PH('seu@email.com'), 'timeout': 40},
    {'do': 'type', 'target': PH('seu@email.com'), 'text': '$TUT_USER', 'cps': 40},
    {'do': 'type', 'target': PH('••••••••'), 'text': '$TUT_SENHA', 'cps': 40},
    {'do': 'click', 'target': BTN('Entrar')},
    {'do': 'waitFor', 'url': '/dashboard', 'timeout': 40},
    {'do': 'waitFor', 'idle': True, 'timeout': 25},
]
INTEG_OK = 'Configure integrações com impressora e balança digital'


def dash_setup(espera=1.0, extra=()):
    return list(LOGIN) + [{'do': 'wait', 'seconds': espera}] + list(extra)


def integ_setup(espera=1.5, extra=()):
    """login, passa pelo Dashboard (o ?tab= só troca a aba numa página que remonta) e para em Configurações > Integrações"""
    return list(LOGIN) + [{'do': 'goto', 'url': '/dashboard'}, {'do': 'waitFor', 'idle': True, 'timeout': 25},
                          {'do': 'goto', 'url': '/configuracoes?tab=integrations'}, {'do': 'waitFor', 'text': INTEG_OK, 'timeout': 30},
                          {'do': 'waitFor', 'idle': True, 'timeout': 25}, {'do': 'wait', 'seconds': espera}] + list(extra)


# rolagem suave do contêiner que rola o alvo (molde do T14/T11): o cursor não se mexe
ACHA_ROLAGEM = ("const rolagem=(el)=>{let c=el&&el.parentElement;while(c&&c!==document.body){const s=getComputedStyle(c);"
                "if(/(auto|scroll)/.test(s.overflowY)&&c.scrollHeight>c.clientHeight+4)return c;c=c.parentElement;}"
                "const se=document.scrollingElement;return se&&se.scrollHeight>se.clientHeight+4?se:null};")
SUAVE = ("await new Promise(res=>{const f=t=>{const p=Math.min(1,(t-t0)/DUR),e=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;c.scrollTo({top:DESTINO,behavior:'instant'});"
         "p<1?requestAnimationFrame(f):res()};requestAnimationFrame(f)});")


def js_h3(texto, y=150, dur_ms=900, tag='h3'):
    """rola (suave) o contêiner até o título (<h3>, ou a tag pedida) `texto` ficar em y px CSS. Devolve o topo final, 'ok', 'SEM ALVO' ou 'SEM ROLAGEM'."""
    busca = "[...document.querySelectorAll('main %s')].find(e=>e.textContent.trim()===%s)" % (tag, json.dumps(texto, ensure_ascii=False))
    return ("(async()=>{" + ACHA_ROLAGEM + "const el=" + busca + ";if(!el)return 'SEM ALVO';const c=rolagem(el);if(!c)return 'SEM ROLAGEM';"
            f"const dy=Math.round(el.getBoundingClientRect().top-{int(y)});if(Math.abs(dy)<3)return 'ok';const y0=c.scrollTop,t0=performance.now();"
            + SUAVE.replace('DUR', str(int(dur_ms))).replace('DESTINO', 'y0+dy*e') +
            "return Math.round(el.getBoundingClientRect().top)})()")


def js_rotulo(texto, y=150, dur_ms=900):
    """igual, para a <label> `texto` (a linha de uma chave)"""
    return js_h3(texto, y, dur_ms, tag='label')


def js_topo(dur_ms=900):
    """volta o contêiner da página ao topo (suave)"""
    return ("(async()=>{" + ACHA_ROLAGEM + "const el=document.querySelector('main h1, main h2, main h3')||document.querySelector('main');"
            "const c=rolagem(el);if(!c)return 'SEM ROLAGEM';if(c.scrollTop<3)return 'ok';const y0=c.scrollTop,t0=performance.now();"
            + SUAVE.replace('DUR', str(int(dur_ms))).replace('DESTINO', 'y0*(1-e)') + "return c.scrollTop})()")


# alvos de Configurações > Integrações (SettingsIntegrationsContent.tsx)
def CHAVE(rotulo):
    """a chave (Switch) da linha cujo <label> é `rotulo`"""
    return SEL(f'main div:has(> div > div > label:text-is("{rotulo}")) > button[role=switch]')


def AJUDA(rotulo):
    """o "?" (HelpCircle) ao lado do <label> `rotulo`"""
    return SEL(f'main label:text-is("{rotulo}") ~ svg')


SW_IMP, SW_BAL = CHAVE('Integração com Impressora'), CHAVE('Integração com Balança Digital')
SW_PESO, SW_CONT = CHAVE('Peso somente pela balança'), CHAVE('Leitura contínua')
SELO_NAO = TXT('EcoTray não detectado nesta estação')
SELO_V = TXT('v1.7.22')
COMBO = {'role': 'combobox'}
COMO = lambda n: BTNX('Como funciona?', nth=n)
ESCALA_BTN = BTN('Ajustar Escala')
TURBO_LABEL = SEL('main label:text-is("Impressão térmica turbo (beta)")')
BAL_CARTAO = SEL('main div.rounded-lg:has(> div > div > span:text-matches("^Conectada"))')
RODAPE_BAL = SEL('footer span.tabular-nums')


# ================================================================ capítulos
CAPS_ROBO = {}


def capitulo(fn):
    CAPS_ROBO[int(fn.__name__[3:])] = fn
    return fn


def marcas_ate_o_fim(c, de=2):
    """capítulo sem gesto (ilustrações e cartões cobrem a tela): só as marcas L<de>.."""
    for i in range(de, len(c.linhas) + 1):
        c.mark(i)


@capitulo
def cap00():
    """Abertura: o Dashboard parado (as ilustrações, o cartão do plano e o cartão "Antes" cobrem; o cursor descansa)."""
    c = Cap(0, start=TOPO_DASH, setup=dash_setup(), eco=ECO[0])
    c.mark(1)
    c.cursor(TOPO_DASH, at=0.3, label='cursor descansa no alto (fora dos gráficos: a dica do gráfico abriria)')
    marcas_ate_o_fim(c)
    c.fim()
    return c


@capitulo
def cap01():
    """O que é o EcoTray: Configurações > Integrações pelo menu; ilustração da ponte (L2 a L4); zoom no cartão e no selo; desce às seções e volta."""
    c = Cap(1, start=TOPO_DASH, setup=dash_setup(), eco=ECO[1])
    c.mark(1)
    c.click(BTNX('Configurações'), at=c.A(1, 'Configurações', 0.9), label='engrenagem Configurações (rodapé do menu)', noScroll=True)
    c.waitfor(text='Configurações do Sistema', timeout=15)
    c.click({'role': 'tab', 'name': 'Integrações'}, at=c.A(1, 'Integrações', 0.9), label='aba Integrações')
    c.waitfor(text=INTEG_OK, timeout=15)
    c.mark(2)
    c.cursor(NEUTRO, at=c.L(2) + 0.3, label='cursor sai da aba')
    c.mark(3)
    c.mark(4)
    c.mark(5)
    c.registra(TXTX('Programa para Windows e macOS que conecta impressora térmica'), at=c.A(5, 'Windows', 0.2), label='texto do cartão do EcoTray')
    c.mark(6)
    c.registra(SELO_NAO, at=c.A(6, 'selo', 0.2), label='selo "EcoTray não detectado nesta estação"')
    c.mark(7)
    c.ev(js_h3('Impressora', 150, 1000), at=c.A(7, 'Embaixo', 0.2), label='desce até a seção Impressora')
    c.hover(COMO(0), 0.5, at=c.A(7, 'impressora', 0.5), label='Como funciona? da impressora (sem clicar)')
    c.ev(js_h3('Integração com Balança Digital', 150, 1000), at=c.A(7, 'balança', 0.8), label='desce até a seção Integração com Balança Digital')
    c.hover(COMO(1), 0.5, at=c.A(7, 'Como', 0.5), label='Como funciona? da balança (sem clicar)')
    c.ev(js_topo(1000), at=c.A(7, 'tudo', 0.8), label='volta ao topo')
    c.hover(BTN('Baixar Instalador'), 0.5, at=c.A(7, 'Baixar', 0.6), label='Baixar Instalador (sem clicar)')
    c.fim()
    return c


@capitulo
def cap02():
    """Baixar e instalar: Baixar Instalador > Windows (L1); as cenas de Windows cobrem L2 a L11 (a página fica parada); no fim, o Mac (L12)."""
    c = Cap(2, start=NEUTRO, setup=integ_setup(), eco=ECO[2])
    c.mark(1)
    c.click(BTN('Baixar Instalador'), at=c.A(1, 'Baixar', 0.9), label='Baixar Instalador')
    c.waitfor(text='Selecione o sistema operacional do seu computador', timeout=10)
    c.click(BTNX('Windows'), at=c.A(1, 'Windows', 1.0), label='Windows (.exe instalador)')
    c.cursor(NEUTRO, label='cursor descansa; a aba do download não entra no vídeo (a cena de Windows cobre)')
    for i in range(2, 12):
        c.mark(i)
    c.mark(12)
    c.click(BTN('Baixar Instalador'), at=c.A(12, 'No', 0.9), label='Baixar Instalador de novo (Mac)')
    c.waitfor(text='Selecione o sistema operacional do seu computador', timeout=10)
    c.hover(BTNX('macOS'), 0.5, at=c.A(12, 'Mac', 0.8, nth=1), label='macOS (.dmg instalador), sem clicar')
    c.press('Escape', at=c.A(12, 'Lá,', 0.2), label='fecha a janela')
    c.pause(0.5)
    c.fim()
    return c


@capitulo
def cap03():
    """O pareamento automático: o selo mostra "v1.7.22" (EcoTray falso ligado desde o início); ilustrações cobrem L3 e L4."""
    c = Cap(3, start=NEUTRO, setup=integ_setup(extra=[{'do': 'waitFor', 'text': 'v1.7.22', 'timeout': 20}]), eco=ECO[3])
    c.mark(1)
    c.cursor(NEUTRO, at=0.3, label='cursor descansa')
    c.mark(2)
    c.registra(SELO_V, at=c.A(2, 'selo', 0.2), label='selo "v1.7.22"')
    c.mark(3)
    c.mark(4)
    c.mark(5)
    c.registra(SELO_V, at=c.A(5, 'selo', 0.2), label='selo da versão (de volta à tela)')
    c.fim()
    return c


@capitulo
def cap04():
    """Conectar a impressora: liga a Integração com Impressora, escolhe a POS-58 e Testar (a cena de Windows 4 mostra o painel do EcoTray)."""
    c = Cap(4, start=NEUTRO, setup=integ_setup(extra=[{'do': 'waitFor', 'text': 'v1.7.22', 'timeout': 20}]), eco=ECO[4])
    c.mark(1)
    c.ev(js_h3('Impressora', 120, 900), at=c.A(1, 'Agora', 0.0) + 0.3, label='mostra a seção Impressora')
    c.mark(2)
    c.click(SW_IMP, at=c.A(2, 'ligo', 0.9), label='chave Integração com Impressora')
    c.waitfor(text='Conectado ao EcoTray', timeout=15)
    c.mark(3)
    c.click(COMBO, at=c.A(3, 'lista', 0.9), label='lista Selecione a impressora')
    c.click(OPT('POS-58'), at=c.A(3, 'Escolho', 0.9), label='impressora POS-58')
    c.waitfor(target=BTN('Testar'), timeout=10)
    c.mark(4)
    c.click(BTN('Testar'), at=c.A(4, 'Testar', 0.9), label='Testar')
    c.waitfor(text='Comprovante enviado para a impressora!', timeout=10)
    c.mark(5)
    c.cursor(NEUTRO, at=c.L(5) + 0.5, label='cursor descansa')
    c.mark(6)
    c.hover(BTN('Atualizar'), 0.6, at=c.A(6, 'Atualizar', 0.9), label='Atualizar (sem clicar)')
    c.fim()
    return c


@capitulo
def cap05():
    """Largura do papel e impressão turbo: Ajustar Escala > 58 mm, Testar impressão, Salvar; o turbo só mostrado."""
    c = Cap(5, start=NEUTRO, setup=integ_setup(extra=[{'do': 'waitFor', 'text': 'Conectado ao EcoTray', 'timeout': 20}]), eco=ECO[5])
    c.mark(1)
    c.ev(js_rotulo('Escala e Largura do Comprovante', 200, 900), at=0.3, label='mostra Escala e Largura do Comprovante')
    c.registra(TXTX('Papel 80mm · Escala 100%'), at=c.A(1, 'largura', 0.2), label='Escala e Largura do Comprovante: Papel 80mm · Escala 100%')
    c.mark(2)
    c.mark(3)
    c.click(ESCALA_BTN, at=c.A(3, 'Ajustar', 0.9), label='Ajustar Escala')
    c.waitfor(text='Ajuste do Comprovante Térmico', timeout=10)
    c.click(TXT('58 mm', within=DLG), at=c.A(3, 'cinquenta', 1.2), label='58 mm (bobina pequena)')
    c.mark(4)
    c.registra(TXTX('O comprovante será gerado no tamanho exato do papel selecionado', within=DLG), at=c.A(4, 'sistema', 0.2), label='nota: tamanho exato do papel')
    c.mark(5)
    c.registra(TXT('Escala fina', within=DLG), at=c.A(5, 'escala', 0.2), label='Escala fina (100%)')
    c.mark(6)
    c.click(BTN('Testar impressão'), at=c.A(6, 'Testar', 0.9), label='Testar impressão')
    c.waitfor(text='Comprovante de teste enviado para a impressora!', timeout=10)
    c.click(BTN('Salvar'), at=c.A(6, 'salvo', 1.0), label='Salvar')
    c.waitfor(text='Papel 58mm · Escala 100%', timeout=10)
    c.mark(7)
    c.ev(js_rotulo('Impressão térmica turbo (beta)', 300, 900), at=c.L(7) - 0.3, label='mostra a impressão térmica turbo')
    c.registra(TURBO_LABEL, at=c.A(7, 'turbo', 0.2), label='Impressão térmica turbo (beta)')
    c.hover(AJUDA('Impressão térmica turbo (beta)'), 0.8, at=c.A(7, 'teste:', 0.9), label='? do turbo')
    c.fim()
    return c


@capitulo
def cap06():
    """Conectar a balança: liga a chave (L3); as cenas de Windows 5 e 6 cobrem L4 a L8 (no "Gravar" a Balança do pátio entra no EcoTray);
    de volta ao sistema o peso sobe a 18,6 kg (L10); unidade, casas, leitura contínua; sobe às chaves."""
    c = Cap(6, start=NEUTRO, setup=integ_setup(extra=[{'do': 'waitFor', 'text': 'Conectado ao EcoTray', 'timeout': 20}]), eco=ECO[6])
    c.mark(1)
    c.ev(js_h3('Integração com Balança Digital', 120, 1000), at=0.4, label='desce até Integração com Balança Digital')
    c.mark(2)
    c.registra(SW_BAL, at=c.A(2, 'chave', 0.2), label='chave Integração com Balança Digital (desligada)')
    c.mark(3)
    c.click(SW_BAL, at=c.A(3, 'Ligada', 0.9), label='liga a chave Integração com Balança Digital')
    c.waitfor(text='Nenhuma balança configurada no EcoTray', timeout=15)
    c.cursor(NEUTRO, label='cursor descansa durante as cenas de Windows')
    for i in range(4, 9):
        c.mark(i)
    c.ecotray(at=c.A(8, 'Gravar', -0.3), label='Gravar: a Balança do pátio passa a existir no EcoTray', balancas=[BAL], padrao='bal-patio')
    c.mark(9)
    c.registra(SEL('main label:has-text("Balança do pátio")'), at=c.A(9, 'Balança', 0.2), label='Balança do pátio na lista (Conectada, padrão)')
    c.mark(10)
    c.registra(TXTX('Peso atual:'), label='Peso atual (ao vivo)')
    c.peso(18.6, at=c.A(10, 'põe', 0.3), label='saco de latinha na balança: 18,6 kg', subir=0.8, oscilar=0.8)
    c.mark(11)
    c.registra(SEL('main div:has(> label:text-is("Unidade de medida padrão"))'), at=c.A(11, 'unidade', 0.2), label='Unidade de medida padrão')
    c.registra(SEL('main div:has(> label:text-is("Casas decimais no peso"))'), at=c.A(11, 'casas', 0.2), label='Casas decimais no peso')
    c.mark(12)
    c.registra(SW_CONT, at=c.A(12, 'leitura', 0.2), label='Leitura contínua (desligada)')
    c.hover(AJUDA('Leitura contínua'), 0.8, at=c.A(12, 'fixo.', 1.6), label='? da leitura contínua')
    c.mark(13)
    c.ev(js_rotulo('Integração com Impressora', 200, 1100), at=c.A(13, 'repara', 0.4), label='sobe até as chaves da impressora e da balança')
    c.cursor(NEUTRO, label='cursor sai do "?"')
    c.fim()
    return c


@capitulo
def cap07():
    """Peso somente pela balança: a chave (desligada) e o "?"; a ilustração (L2) cobre a tela."""
    c = Cap(7, start=NEUTRO, setup=integ_setup(extra=[{'do': 'waitFor', 'text': 'Conectada', 'timeout': 20}]), eco=ECO[7])
    c.mark(1)
    c.ev(js_rotulo('Peso somente pela balança', 220, 900), at=0.3, label='mostra Peso somente pela balança')
    c.registra(SW_PESO, at=c.A(1, 'Peso', 0.2), label='chave Peso somente pela balança (desligada)')
    c.mark(2)
    c.mark(3)
    c.hover(AJUDA('Peso somente pela balança'), 1.0, at=c.A(3, 'regra', 1.1), label='? do Peso somente pela balança')
    c.mark(4)
    c.cursor(NEUTRO, at=c.L(4) - 0.1, label='cursor sai do "?"')
    c.mark(5)
    c.fim()
    return c


@capitulo
def cap08():
    """O indicador de peso: rodapé "Balança do pátio · Aguardando peso" no Dashboard; o peso chega (312 kg) na L3."""
    c = Cap(8, start=TOPO_DASH, setup=dash_setup(espera=7.0, extra=[{'do': 'waitFor', 'text': 'Aguardando peso', 'timeout': 20}]), eco=ECO[8])
    c.mark(1)
    c.registra(RODAPE_BAL, at=c.A(1, 'indicador', 0.2), label='rodapé: Balança do pátio · Aguardando peso')
    c.mark(2)
    c.mark(3)
    c.peso(312, at=c.A(3, 'sobe', 0.5), label='carroça do Valdir na balança: 312 kg', subir=1.2, oscilar=1.0)
    c.registra(RODAPE_BAL, at=c.A(3, 'trezentos', 0.2), label='rodapé: Balança do pátio · 312 kg')
    c.mark(4)
    c.mark(5)
    c.mark(6)
    c.fim()
    return c


@capitulo
def cap09():
    """Quando o EcoTray cai: a cena 7 fecha o EcoTray (L1); o sistema avisa e o rodapé muda (L2); L5 mostra "EcoTray não encontrado" em Integrações;
    a cena 8 reabre (L6); a balança volta sozinha e o "Tentar conectar" conecta a impressora (L7)."""
    c = Cap(9, start=NEUTRO, setup=integ_setup(espera=3.0, extra=[{'do': 'waitFor', 'text': 'Conectado ao EcoTray', 'timeout': 20},
                                                                  {'do': 'waitFor', 'text': 'Peso atual', 'timeout': 20}]), eco=ECO[9])
    c.mark(1)
    c.cursor(NEUTRO, at=0.3, label='cursor descansa (a cena 7 mostra o clique em Sair)')
    c.ecotray(at=c.L(2) - 0.3, label='EcoTray fechado: 8053 e 8054 recusam conexão', ligado=False)
    c.mark(2)
    c.registra(RODAPE_BAL, at=c.A(2, 'rodapé', 0.2), label='rodapé: Balança desconectada')
    c.mark(3)
    c.mark(4)
    c.mark(5)
    c.ev(js_h3('Impressora', 120, 900), at=c.L(5) - 0.3, label='mostra a seção Impressora')
    c.registra(TXTX('EcoTray não encontrado'), at=c.A(5, 'EcoTray', 0.2), label='EcoTray não encontrado')
    c.mark(6)
    c.ecotray(at=c.A(6, 'atalho', 0.3), label='EcoTray aberto de novo: só o peso volta; os comandos (impressora) demoram', ligado=True, comandos=False)
    c.mark(7)
    c.ecotray(at=c.A(7, 'Tentar', 1.3), label='os comandos do EcoTray voltam', comandos=True)
    c.click(BTN('Tentar conectar'), at=c.A(7, 'Tentar', 0.7), label='Tentar conectar')
    c.waitfor(text='Conectado ao EcoTray!', timeout=10)
    c.mark(8)
    c.ev(js_topo(900), at=c.L(8) - 0.2, label='volta ao topo')
    c.registra(TXTX('Programa para Windows e macOS que conecta impressora térmica'), at=c.A(8, 'abre', 0.2), label='texto do cartão: inicia automaticamente com o computador')
    c.fim()
    return c


@capitulo
def cap10():
    """Driver incompatível: a lista com o triângulo, escolhe a "Generic / Text Only" (caixa âmbar), volta à POS-58."""
    c = Cap(10, start=NEUTRO, setup=integ_setup(extra=[{'do': 'waitFor', 'text': 'Conectado ao EcoTray', 'timeout': 20}]), eco=ECO[10])
    c.mark(1)
    c.ev(js_h3('Impressora', 120, 900), at=0.3, label='mostra a seção Impressora')
    c.click(COMBO, at=c.A(1, 'Imagina', 0.9), label='abre Selecione a impressora')
    c.registra(OPT('Generic / Text Only'), at=c.A(1, 'triângulo', 0.2), label='lista: POS-58 e Generic / Text Only (triângulo amarelo)')
    c.mark(2)
    c.mark(3)
    c.click(OPT('Generic / Text Only'), at=c.A(3, 'Escolhendo', 0.8), label='escolhe Generic / Text Only')
    c.waitfor(text='Driver incompatível', timeout=10)
    c.registra(TXTX('Driver incompatível (Generic / Text Only)'), at=c.A(3, 'Driver', 0.2), label='caixa: Driver incompatível (Generic / Text Only)')
    c.mark(4)
    c.registra(TXTX('Troque pelo driver térmico real da sua impressora'), at=c.A(4, 'instalar', 0.2), label='Troque pelo driver térmico real da sua impressora')
    c.mark(5)
    c.click(COMBO, at=c.A(5, 'Volto', 1.4), label='abre Selecione a impressora')
    c.click(OPT('POS-58'), at=c.A(5, 'nossa', 0.8), label='volta para a POS-58')
    c.mark(6)
    c.cursor(NEUTRO, at=c.L(6) - 0.1, label='cursor descansa')
    c.mark(7)
    c.fim()
    return c


@capitulo
def cap11():
    """Recapitulando: a montagem é da edição; o robô só deixa o Dashboard parado com as marcas."""
    c = Cap(11, start=TOPO_DASH, setup=dash_setup(), eco=ECO[11])
    c.mark(1)
    c.cursor(TOPO_DASH, at=0.3, label='cursor descansa')
    marcas_ate_o_fim(c)
    c.fim()
    return c


# ---------------------------------------------------------------- trechos com "device": "windows" (1280x712) para as cenas de Windows
# o navegador aparece dentro da área de trabalho simulada: grava-se o mesmo roteiro até onde a cena cobre (a telemetria e as ações do robô
# entram na cena deslocadas no tempo, docs/10-cena-windows.md). cap -> linha do fim (o último passo é o anterior à marca dela)
TRECHOS_WINDOWS = {2: 12, 4: 7, 6: 10, 9: 9}


def trecho_windows(n, d):
    ate = TRECHOS_WINDOWS[n]
    dentro = []
    for st in d['steps']:
        if st.get('do') == 'mark' and st.get('name') == f'L{ate}':
            break
        if st.get('do') == 'mark' and st.get('name') == 'FIM':
            break
        dentro.append(st)
    # cauda: mantém o que vem antes da marca da linha de corte; fecha com o avisos e a marca FIM nesse instante
    fim = [s for s in d['steps'] if s.get('do') == 'mark' and s.get('name') == f'L{ate}']
    t_fim = fim[0]['at'] if fim else d['steps'][-1].get('at', 0)
    w = dict(d)
    w['name'] = f't05-cap{n:02d}w'
    w['title'] = d['title'] + f' · SÓ O TRECHO COM O NAVEGADOR NA CENA DE WINDOWS (até a linha {ate - 1}; device windows, 1280x712)'
    w['device'] = 'windows'
    w['steps'] = dentro + [{'do': 'eval', 'js': 'JSON.stringify(window.__avisos || "sem observador")', 'label': 'avisos de erro na tela'},
                           {'do': 'mark', 'name': 'FIM', 'at': round(t_fim, 2)}]
    return w


def main():
    quais = [int(a) for a in sys.argv[1:] if not a.startswith('-')] or sorted(CAPS_ROBO)
    json.dump({f'{n:02d}': FAKE_NOW[n] for n in FAKE_NOW}, open(os.path.join(HERE, 'fake_now.json'), 'w', encoding='utf8'), indent=1)
    for n in quais:
        c = CAPS_ROBO[n]()
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
        marcas = [s['name'] for s in d['steps'] if s.get('do') == 'mark']
        faltam = [f'L{i}' for i in range(1, len(c.linhas) + 1) if f'L{i}' not in marcas]
        if faltam:
            print(f'  aviso cap{n:02d}: sem marca {",".join(faltam)}')
        path = os.path.join(HERE, f'cap{n:02d}.json')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
        print(f'cap{n:02d}: {len(d["steps"])} passos, narração {c.dur:.1f} s{" (voz ESTIMADA)" if c.estimada else ""} -> {os.path.relpath(path, HERE)}')
        if n in TRECHOS_WINDOWS:
            w = trecho_windows(n, d)
            pw = os.path.join(HERE, f'cap{n:02d}w.json')
            with open(pw, 'w', encoding='utf-8') as f:
                json.dump(w, f, ensure_ascii=False, indent=1)
            print(f'cap{n:02d}w: {len(w["steps"])} passos (device windows, até a linha {TRECHOS_WINDOWS[n] - 1}) -> {os.path.relpath(pw, HERE)}')


if __name__ == '__main__':
    main()
