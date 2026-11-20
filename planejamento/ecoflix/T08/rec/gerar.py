#!/usr/bin/env python3
"""T08 · Ticket de Pesagem: gera rec/t08/cap00..cap13.json (roteiros do robô) a partir da voz (t08/narracao/capNN.json).

EcoSistema 1.60.18 no Supabase falso (mundo da Recicla Vale Metais), computador 1280x800, logado como Rafael Nogueira (MASTER),
EcoTray falso ligado (semente base/balanca-ativada: "Balança do pátio" e a térmica POS-58) e o caixa do Rafael aberto (base/caixa-aberto).
Cada passo é preso a uma palavra da fala: `at` = início da palavra - folga (o custo do gesto, docs/04 "Custo real dos gestos"), e a marca
Ln entra no início de cada linha. Quando a voz chegar, rodar de novo com o capNN.json da voz (nada a reescrever).
Rodar de qualquer pasta: `python3 -I rec/t08/gerar.py [NN ...]`; ensaiar: `bash rec/t08/t08_grava.sh NN [--rapido]` ou o lote `t08_lote160.sh`.

18/11 (app 1.60.18, cobertura_160 + JUNCAO_160): 14 capítulos. Novos: 07 (ticket com valores), 11 (pesagem avulsa com cobrança) e
12 (sem internet); os antigos 07, 08, 09 e 10 viraram 08, 09, 10 e 13.
Relógio (MUNDO_LINHA_DO_TEMPO.md, "O dia 10/11"): o ticket #58 é das 08:40 às 09:00. FAKE_NOW por capítulo (fake_now.json, que o
t08_grava.sh usa para religar a instância 54308): 08:40 (caps 0 a 3), 08:49 (caps 4 e 5), 08:51 (cap 6: o #58 nasce às 08:52),
08:55 (cap 7: o #59 do Jair é salvo com valores), 08:58 (caps 8 a 10: valorizar e finalizar perto das 09:00), 09:12 (cap 11, a
pesagem avulsa #60) e 09:20 (caps 12 e 13).
Cadeia de sementes (seeds-extra/t08, apos-capNN = estado depois do capítulo NN, cumulativo desde a base; as de 07 em diante são
feitas por t08_semente.py a partir da instância logo depois do ensaio do capítulo):
inicio (mundo base + #57 com item + #56 pendente da cooperativa + um rascunho na lixeira) -> apos-cap02 -> apos-cap03 -> apos-cap04 ->
apos-cap05 -> apos-cap06 (#58 salvo, rascunho do Jair) -> apos-cap07 (#59 salvo com valores, R$ 4.964,00) -> apos-cap08 (compra do
#58 em rascunho) -> apos-cap10 (compra finalizada, #58 valorizado) -> apos-cap11 (pesagem avulsa #60 cobrada por Pix, R$ 60,00).
Nada disso segue para a T09 (JUNCAO_160: "A, não segue").
"""
import hashlib
import json
import os
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TUT = os.path.normpath(os.path.join(HERE, '..', '..'))
NARR = os.path.join(TUT, 't08', 'narracao')
N08_40, N08_49, N08_51, N08_55, N08_58, N09_12, N09_20 = (f'2026-11-10T{h}:00-03:00' for h in ('08:40', '08:49', '08:51', '08:55', '08:58', '09:12', '09:20'))
FAKE_NOW = {0: N08_40, 1: N08_40, 2: N08_40, 3: N08_40, 4: N08_49, 5: N08_49, 6: N08_51, 7: N08_55, 8: N08_58, 9: N08_58, 10: N08_58,
            11: N09_12, 12: N09_20, 13: N09_20}


def stable_id(chave):
    """o mesmo UUID estável do Supabase falso (core/util.mjs stableId)"""
    h = bytearray(hashlib.sha1(('domiflix-fake:' + chave).encode()).digest())
    h[6] = (h[6] & 0x0F) | 0x50
    h[8] = (h[8] & 0x3F) | 0x80
    x = h[:16].hex()
    return f'{x[:8]}-{x[8:12]}-{x[12:16]}-{x[16:20]}-{x[20:32]}'


RAFAEL = stable_id('user.rafael')
try:
    VERSAO = open(os.path.join(TUT, 'app', 'dist', '.versao-app'), encoding='utf8').read().strip() or '1.60.18'
except OSError:
    VERSAO = '1.60.18'
HOJE = '2026-11-10'
EMPRESA = '38814e47-876a-5977-a5f7-53af364c17bb'
STORAGE = {
    f'cato_adoption_nudge_{EMPRESA}_{RAFAEL}': '{"count":99,"lastShownAt":4102444800000}',   # cala o balão de dica do Cato (JUNCAO_160, regra do mundo)
    'app_version': VERSAO, 'notification_shown_version': VERSAO, f'dominex:daily-tasks-shown:{RAFAEL}': HOJE,
    'pwa-install-dismissed': 'true', 'theme': 'light', f'daily-tasks-reminder-last-shown-{RAFAEL}': HOJE, 'initial-preferences-set': 'true',
}
NOMES = ['Abertura', 'Quando usar o ticket', 'Criar o ticket', 'A primeira pesagem e o rascunho', 'Descarregar e a segunda pesagem',
         'Impureza em porcentagem ou em quilos', 'Vários veículos ao mesmo tempo', 'Ticket com valores', 'Valorizar o ticket',
         'Imprimir o comprovante', 'Quando o ticket sai dos pendentes', 'Pesagem avulsa com cobrança', 'Sem internet', 'Recapitulando']
BASE = ['base/balanca-ativada', 'base/caixa-aberto', 't08/inicio']
CADEIA = ['apos-cap02', 'apos-cap03', 'apos-cap04', 'apos-cap05', 'apos-cap06', 'apos-cap07', 'apos-cap08', 'apos-cap10', 'apos-cap11']
SEMENTE = {0: None, 1: None, 2: None, 3: 'apos-cap02', 4: 'apos-cap03', 5: 'apos-cap04', 6: 'apos-cap05', 7: 'apos-cap06', 8: 'apos-cap07',
           9: 'apos-cap08', 10: 'apos-cap08', 11: 'apos-cap10', 12: 'apos-cap11', 13: 'apos-cap11'}


def sementes(n):
    """a semente de cada capítulo é cumulativa (tudo desde o mundo base): só a última da cadeia vai junto da base"""
    return list(BASE) + ([f't08/{SEMENTE[n]}'] if SEMENTE[n] else [])


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
    def __init__(s, n, pace=0.5, cps=9, start=(900, 440), setup=None, noscroll=False, sameTab=False):
        s.n = n
        s.words, s.linhas, s.dur, s.estimada = carregar_voz(n)
        s.steps = []
        s.pace, s.cps, s.start = pace, cps, start
        s.noscroll = noscroll
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

    def fim(s):
        s.flush(1e9)
        s.steps.append({'do': 'eval', 'js': 'JSON.stringify(window.__avisos || "sem observador")', 'label': 'avisos de erro na tela'})
        s.steps.append({'do': 'mark', 'name': 'FIM', 'at': round(s.dur, 2)})

    def out(s):
        d = {
            'name': f't08-cap{s.n:02d}',
            'title': f'T08 · Cap. {s.n} · {NOMES[s.n]} (narração {str(round(s.dur, 1)).replace(".", ",")} s{" ESTIMADA" if s.estimada else ""}; '
                     f'marcas L1..L{len(s.linhas)} = início de cada linha do roteiro; FAKE_NOW {FAKE_NOW[s.n]})',
            'seed': f't08-cap{s.n:02d}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
            'start': {'x': s.start[0], 'y': s.start[1]},
            'anonymous': True, 'storage': dict(STORAGE),
            'seedExtra': sementes(s.n),
            'prewarm': ['/login'], 'setup': s.setup, 'steps': s.steps,
        }
        if s.sameTab:
            d['sameTab'] = True
        return d


# ---------------------------------------------------------------- alvos
BTN = lambda n, **kw: {'role': 'button', 'name': n, 'exact': True, **kw}
BTNX = lambda n, **kw: {'role': 'button', 'name': n, **kw}
TXT = lambda t, **kw: {'text': t, 'exact': True, **kw}
TXTX = lambda t, **kw: {'text': t, **kw}
SEL = lambda s, **kw: {'selector': s, **kw}
OPT = lambda n, **kw: {'role': 'option', 'name': n, **kw}
ITEM = lambda n, **kw: {'role': 'menuitem', 'name': n, **kw}
PH = lambda p, **kw: {'placeholder': p, **kw}
DLG = '[role=dialog]'

# ---------------------------------------------------------------- setup (fora do vídeo)
LOGIN = [
    {'do': 'waitFor', 'target': PH('seu@email.com'), 'timeout': 40},
    {'do': 'type', 'target': PH('seu@email.com'), 'text': '$TUT_USER', 'cps': 40},
    {'do': 'type', 'target': PH('••••••••'), 'text': '$TUT_SENHA', 'cps': 40},
    {'do': 'click', 'target': BTN('Entrar')},
    {'do': 'waitFor', 'url': '/dashboard', 'timeout': 40},
    {'do': 'waitFor', 'idle': True, 'timeout': 25},
]
TICKET_OK = 'Gerencie tickets de pesagem rodoviária'
CRIAR_OK = 'Preencha o ticket. Use as abas para atender vários veículos.'


def setup_lista(extra=(), aquece=()):
    """login, aquece as rotas que o capítulo visita e para na lista do Ticket de Pesagem"""
    st = list(LOGIN)
    for r in aquece:
        st += [{'do': 'goto', 'url': r}, {'do': 'waitFor', 'idle': True, 'timeout': 25}]
    st += [{'do': 'goto', 'url': '/ticket-pesagem'}, {'do': 'waitFor', 'text': TICKET_OK, 'timeout': 30}, {'do': 'waitFor', 'idle': True, 'timeout': 25},
           {'do': 'wait', 'seconds': 0.8}]
    return st + list(extra)


# rolagem suave do contêiner que rola o alvo (molde do T14/T11: ACHA_ROLAGEM + SUAVE): o cursor não se mexe
ACHA_ROLAGEM = ("const rolagem=(el)=>{let c=el&&el.parentElement;while(c&&c!==document.body){const s=getComputedStyle(c);"
                "if(/(auto|scroll)/.test(s.overflowY)&&c.scrollHeight>c.clientHeight+4)return c;c=c.parentElement;}"
                "const se=document.scrollingElement;return se&&se.scrollHeight>se.clientHeight+4?se:null};")
SUAVE = ("await new Promise(res=>{const f=t=>{const p=Math.min(1,(t-t0)/DUR),e=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;c.scrollTo({top:DESTINO,behavior:'instant'});"
         "p<1?requestAnimationFrame(f):res()};requestAnimationFrame(f)});")


def js_ate(texto, y=250, dur_ms=900, escopo='main', prefixo=False):
    """rola (suave) o contêiner do alvo até a folha do DOM cujo texto é `texto` ficar em y px CSS. Devolve o topo final do alvo,
    'ok' (já estava lá), 'SEM ALVO' ou 'SEM ROLAGEM'."""
    alvo = json.dumps(texto)
    sel = json.dumps(f'{escopo} *')
    busca = (f"[...document.querySelectorAll({sel})].filter(e=>e.textContent.trim().startsWith({alvo})).sort((a,b)=>a.textContent.length-b.textContent.length)[0]"
             if prefixo else f"[...document.querySelectorAll({sel})].find(e=>e.children.length===0&&e.textContent.trim()==={alvo})")
    return ("(async()=>{" + ACHA_ROLAGEM + "const el=" + busca + ";if(!el)return 'SEM ALVO';const c=rolagem(el);if(!c)return 'SEM ROLAGEM';"
            f"const dy=Math.round(el.getBoundingClientRect().top-{int(y)});if(Math.abs(dy)<3)return 'ok';const y0=c.scrollTop,t0=performance.now();"
            + SUAVE.replace('DUR', str(int(dur_ms))).replace('DESTINO', 'y0+dy*e') +
            "return Math.round(el.getBoundingClientRect().top)})()")


def rola_ate(c, texto, at, label, y=250, dur_ms=900, escopo='main', prefixo=False):
    return c.ev(js_ate(texto, y, dur_ms, escopo, prefixo), at=at, label=label)


# ================================================================ capítulos
CAPS_ROBO = {}


def capitulo(fn):
    CAPS_ROBO[int(fn.__name__[3:])] = fn
    return fn


# ---------------------------------------------------------------- alvos do Ticket de Pesagem (rec/t08/_ex: explorações de 11/11)
MENU = '[data-sidebar=sidebar]'
NEUTRO = (1000, 560)          # ponto neutro para o cursor descansar (fora de menu, cartão e botão)
TOPO_DASH = (760, 120)        # no Dashboard, o neutro fica no alto: em (1000, 560) o gráfico "Evolução da Margem" abre a dica
COL_AGUARDA = SEL("main h3:text-is('Aguardando valorização')")
COL_VALORIZ = SEL("main h3:text-is('Valorizados')")
ABA_AVULSAS = {'role': 'tab', 'name': 'Pesagens avulsas'}
ABA_PADRAO = {'role': 'tab', 'name': 'Tickets padrão'}


def dashboard_setup(extra=()):
    return list(LOGIN) + [{'do': 'goto', 'url': '/ticket-pesagem'}, {'do': 'waitFor', 'text': TICKET_OK, 'timeout': 30},
                          {'do': 'waitFor', 'idle': True, 'timeout': 25}, {'do': 'goto', 'url': '/dashboard'},
                          {'do': 'waitFor', 'idle': True, 'timeout': 25}, {'do': 'wait', 'seconds': 1.0}] + list(extra)


@capitulo
def cap00():
    """Abertura: o Dashboard parado (a ilustração do caminhão cobre L2 e L3; o cartão "Antes" entra na L4)."""
    c = Cap(0, start=TOPO_DASH, setup=dashboard_setup())
    c.mark(1)
    c.cursor(TOPO_DASH, at=0.3, label='cursor descansa no alto (fora dos gráficos: a dica do gráfico abriria)')
    for i in range(2, len(c.linhas) + 1):
        c.mark(i)
    c.fim()
    return c


@capitulo
def cap01():
    """Onde fica (Materiais > Ticket de Pesagem), os três casos de uso do ticket padrão, as duas colunas do kanban e a aba Pesagens avulsas."""
    c = Cap(1, start=TOPO_DASH, setup=dashboard_setup())
    c.mark(1)
    c.click(SEL(f"{MENU} button:has-text('Materiais')"), at=0.3, label='menu Materiais')
    c.click({'role': 'link', 'name': 'Ticket de Pesagem'}, at=c.A(1, 'Ticket', 0.6, nth=1), label='menu Ticket de Pesagem')
    c.waitfor(text=TICKET_OK, timeout=15)
    c.mark(2)   # L2 e L3: ilustração "compra direta x ticket" por cima da lista
    c.cursor(NEUTRO, at=c.L(2) + 1.0, label='cursor sai do menu')
    c.mark(3)
    # L4 a L6 (18/11, pedido do Kaik): os três casos de uso do ticket padrão, com a lista parada (gestos poucos e calmos)
    c.mark(4)
    c.hover(SEL(CARTAO(57)), 0.8, at=c.A(4, 'preço', 0.6), label='caso 1: um ticket esperando o preço (cartão #57)')
    c.mark(5)
    c.hover(BTN('Novo Ticket de Pesagem'), 0.8, at=c.A(5, 'cada', 0.6), label='caso 2: um ticket por caminhão (Novo Ticket de Pesagem, sem clicar)')
    c.mark(6)
    c.cursor(NEUTRO, at=c.L(6) + 0.3, label='caso 3: ticket de venda (cursor descansa)')
    c.mark(7)
    c.registra(SEL('main div:has(> h3:text-is("Aguardando valorização"))'), at=c.A(7, 'Os', 0.1), label='kanban: as duas colunas')
    c.hover(COL_AGUARDA, 0.5, at=c.A(7, 'Aguardando', 1.6), label='coluna Aguardando valorização (com o #57)')
    c.hover(COL_VALORIZ, 0.5, at=c.A(7, 'Valorizados', 1.2), label='coluna Valorizados')
    c.mark(8)
    c.click(ABA_AVULSAS, at=c.A(8, 'Pesagens', 1.0), label='aba Pesagens avulsas')
    c.hover(BTN('Nova Pesagem Avulsa'), 0.6, at=c.A(8, 'balança', 0.6), label='Nova Pesagem Avulsa (sem clicar)')
    c.click(ABA_PADRAO, at=c.A(8, 'adiante', 1.2), label='volta para Tickets padrão')
    c.fim()
    return c


# ---------------------------------------------------------------- a criação (WeighingTicketCreator / WeighingTicketForm)
POP = '[data-radix-popper-content-wrapper]'
BARRA = SEL("main button[aria-expanded]:has-text('Seu rascunho')")          # barra escura das abas (abre a lista)
LINHA_ABA = lambda n: SEL(f"{POP} button:has-text('#{n}')")
X_ABA = SEL(f"{POP} button[aria-label='Descartar ticket']")
NOVO_TICKET = SEL("main button[aria-label='Novo ticket de pesagem']")
CHAVES = SEL("main div:has(> div > label:has-text('Modalidade')):has(> div > label:has-text('Valores'))")
SEL_FORN = TXT('Selecionar fornecedor')
FORN = lambda nome: {'text': nome, 'within': DLG}
PINO = lambda nome: SEL(f"[role=dialog] button:has(+ button[aria-label='Ações de {nome}'])")
MAT = PH('Escreva o nome ou código do material')
MOT = PH('Digite ou busque o motorista')
PLACA = PH('Digite ou busque a placa')
PES_AV = BTN('Pesagem avançada')
CAMPO = lambda rot: SEL(f"[role=dialog] div:has(> label:has-text('{rot}')) input")
C1, C2 = CAMPO('1ª Pesagem'), CAMPO('2ª Pesagem')
BRUTO = SEL("[role=dialog] div:has(> label:has-text('Peso Bruto'))")
LIQUIDO = SEL("[role=dialog] div:has(> label:has-text('Líquido'))")
TARA = CAMPO('Tara')
IMP = SEL("[role=dialog] div:has(> div > label:has-text('Impureza')) input")
IMP_CONTA = TXTX('sobre bruto', within=DLG)
BAL_1A = SEL("[role=dialog] div:has(> label:has-text('1ª Pesagem')) button[aria-label='Capturar peso da balança']")
DICA = TXTX('Preencha 1ª e 2ª pesagem', within=DLG)
COMPLETO = {'text': 'Completo', 'within': DLG}
CONFIRMAR = BTN('Confirmar')
ACOES_ITEM = SEL("main button[aria-label='Ações do item']")
ADD_TARA = ITEM('Adicionar tara / pesagem avançada')
DETALHE = SEL("main button[aria-label='Ver detalhes da pesagem']")
LINHA_ITEM = SEL("main tr:has-text('Alumínio latinha')")
SALVAR = BTN('Salvar Ticket de Pesagem')
RASCUNHOS = TXTX('Rascunhos abertos')
APAGADOS = SEL("main button:has-text('Rascunhos apagados')")
CARTAO = lambda n: (f"main div.rounded-lg:has([aria-label='Selecionar ticket #{n}'])"
                    f":not(:has(div.rounded-lg [aria-label='Selecionar ticket #{n}']))")
ACOES = lambda n: {'role': 'button', 'name': 'Ações', 'within': CARTAO(n)}
ROLA_FORM = 120          # px: com a página 120 px abaixo, material, motorista, placa, "Pesagem avançada" e a barra das abas cabem na faixa do robô

REABRE = [{'do': 'click', 'target': RASCUNHOS}, {'do': 'waitFor', 'text': CRIAR_OK, 'timeout': 20}, {'do': 'waitFor', 'idle': True, 'timeout': 20},
          {'do': 'wait', 'seconds': 1.0}]
MATERIAL_LATINHA = [{'do': 'type', 'target': MAT, 'text': 'latinha', 'cps': 40}, {'do': 'click', 'target': OPT('Alumínio latinha')},
                    {'do': 'wait', 'seconds': 1.0}]


def js_clica(sel, texto):
    """clique sem cursor (`el.click()`) no primeiro `sel` cujo texto contém `texto`: opção de lista num trecho acelerado"""
    return ("(()=>{const e=[...document.querySelectorAll(%s)].find(x=>x.textContent.includes(%s));if(!e)return 'SEM ALVO';e.click();return 'ok'})()"
            % (json.dumps(sel), json.dumps(texto)))


def abre_pesagem_item(c, at, rot='item'):
    """menu "Ações do item" (⋮) e "Adicionar tara / pesagem avançada": a janela abre com as pesagens do item"""
    c.click(ACOES_ITEM, at=at, label=f'Ações do {rot} (⋮)')
    c.click(ADD_TARA, label='Adicionar tara / pesagem avançada')
    c.waitfor(text='Registre pesagem dupla, tara, impureza e dados do transporte', timeout=8)


@capitulo
def cap02():
    """Criar o ticket: Novo Ticket de Pesagem, as três chaves, fornecedor, material, motorista e placa; a aba à direita."""
    c = Cap(2, start=(1000, 330), setup=setup_lista())
    c.mark(1)
    c.click(BTN('Novo Ticket de Pesagem'), at=c.A(1, 'Novo', 0.8), label='Novo Ticket de Pesagem')
    c.waitfor(text=CRIAR_OK, timeout=15)
    c.mark(2)
    c.registra(CHAVES, at=c.A(2, 'três', 0.2), label='barra de cima: Modalidade, Tipo e Valores')
    c.hover(BTN('Ticket padrão'), 0.4, at=c.A(2, 'ticket', 0.6), label='Ticket padrão')
    c.hover(BTN('Compra'), 0.4, at=c.A(2, 'compra', 0.6), label='Compra')
    c.hover(BTN('Sem valores'), 0.5, at=c.A(2, 'sem', 0.6), label='Sem valores')
    c.mark(3)
    c.hover(BTN('Com valores'), 0.6, at=c.A(3, 'valores', 0.6), label='Com valores (sem clicar)')
    c.mark(4)
    c.click(SEL_FORN, at=c.A(4, 'fornecedor', 1.0), label='Selecionar fornecedor')
    c.waitfor(text='Selecionar Fornecedor', timeout=8)
    c.hover(BTN('Não informado', within=DLG), 0.6, at=c.A(4, 'Não', 0.6), label='opção Não informado')
    c.hover(PINO('Cooperativa Recomeço'), 0.9, at=c.A(4, 'pino', 0.6), label='pino Fixar como padrão (sem clicar)')
    c.mark(5)
    c.click(FORN('Cooperativa Recomeço'), at=c.A(5, 'Recomeço', 0.9), label='Cooperativa Recomeço')
    c.mark(6)
    c.click(MAT, at=c.A(6, 'material', 1.0), label='campo Material')
    c.type(MAT, 'latinha', cps=40, noClick=True, label='digita latinha')
    c.click(OPT('Alumínio latinha'), at=c.A(6, 'latinha', 0.3), label='Alumínio latinha')
    c.mark(7)
    c.rolar(ROLA_FORM, at=c.A(7, 'E', 0.1), ponto=(700, 460), duration=0.4, after=0, label='desce até motorista e placa')
    c.click(MOT, at=c.A(7, 'motorista', 1.0), label='campo Motorista')
    c.type(MOT, 'Edson', cps=40, noClick=True, label='digita Edson')
    c.click(OPT('Edson Moura'), at=c.A(7, 'Moura', 0.3), label='Edson Moura')
    c.click(PLACA, label='campo Placa do Veículo')
    c.type(PLACA, 'FKD', cps=40, noClick=True, label='digita FKD')
    c.click(OPT('FKD2E41'), at=c.A(7, 'escolher', 0.5), label='FKD2E41')
    c.mark(8)
    c.hover(SEL("main button[aria-label='Gerenciar motoristas']"), 0.8, at=c.A(8, 'botão', 0.6), label='botão + do Motorista (Gerenciar motoristas), sem clicar')
    c.hover(SEL("main button[aria-label='Gerenciar placas']"), 0.6, at=c.A(8, 'placa', 0.6), label='botão + da Placa (Gerenciar placas), sem clicar')
    c.mark(9)
    c.hover(BARRA, 0.8, at=c.A(9, 'aba', 0.7), label='aba deste ticket: número, peso e fornecedor')
    c.registra(BARRA, at=c.A(9, 'número', 0.2), label='barra das abas: #58, 0 kg, Cooperativa Recomeço, Seu rascunho')
    c.cursor(NEUTRO, at=c.A(9, 'fornecedor', -0.6), label='cursor sai da barra')
    c.fim()
    return c


@capitulo
def cap03():
    """A primeira pesagem (9.460 kg) na Pesagem avançada, o modo Completo, o rascunho salvo sozinho e Rascunhos abertos."""
    c = Cap(3, start=(430, 560), setup=setup_lista(REABRE + MATERIAL_LATINHA))
    c.mark(1)
    c.click(PES_AV, at=c.A(1, 'Pesagem', 1.0, nth=1), label='Pesagem avançada')
    c.waitfor(text='Registre pesagem dupla, tara, impureza e dados do transporte', timeout=8)
    c.mark(2)
    c.click(C1, at=c.A(2, 'primeira', 0.8), label='campo 1ª Pesagem')
    c.type(C1, '9460', at=c.A(2, 'nove', 0.1), noClick=True, label='digita 9460 na 1ª Pesagem')
    c.registra(BRUTO, at=c.A(2, 'bruto', 0.4), label='1ª Pesagem e Peso Bruto 9.460 (= 1ª pesagem)')
    c.confere('dlg', ['9.460', '= 1ª pesagem'], 'bruto 9.460 (só a 1ª pesagem)')
    c.mark(3)
    c.hover(BAL_1A, 0.8, at=c.A(3, 'botão', 0.6), label='botão da balança dentro do campo 1ª Pesagem')
    c.mark(4)
    c.hover(DICA, 0.8, at=c.A(4, 'dica', 0.6), label='dica dos três jeitos')
    c.mark(5)
    c.hover(TXTX('Como exibir no comprovante', within=DLG), 0.3, at=c.A(5, 'Como', 0.6), label='Como exibir no comprovante')
    c.click(COMPLETO, at=c.A(5, 'Completo', 0.6), label='Completo')
    c.mark(6)
    c.click(CONFIRMAR, at=c.A(6, 'Confirmar', 0.7), label='Confirmar')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.mark(7)   # L7: ilustração do rascunho salvo
    c.cursor(NEUTRO, at=c.L(7) + 0.4, label='cursor descansa')
    c.mark(8)
    c.hover(BARRA, 0.8, at=c.A(8, 'aqui', 0.6), label='aba #58 com Seu rascunho')
    c.registra(BARRA, at=c.A(8, 'número', 0.3), label='número previsto #58')
    c.mark(9)
    c.click(BTN('Voltar'), at=c.A(9, 'saindo', 0.8), label='Voltar')
    c.waitfor(text=TICKET_OK, timeout=15)
    c.click(RASCUNHOS, at=c.A(9, 'Rascunhos', 0.9), label='Rascunhos abertos (1): abre o rascunho')
    c.waitfor(text=CRIAR_OK, timeout=15)
    c.mark(10)
    c.hover(LINHA_ITEM, 0.8, at=c.A(10, 'confira', 0.6), label='item reaberto: Alumínio latinha 9.460')
    c.fim()
    return c


@capitulo
def cap04():
    """A segunda pesagem (6.380 kg): a 1ª (9.460) já está no campo dela (app 1.60.18, commit 4d19302a3: a 1ª pesagem sozinha não
    vira mais bruto ao reabrir); o bruto sai sozinho (3.080), a tara em branco e o detalhe."""
    c = Cap(4, start=(1100, 420), setup=setup_lista(REABRE))
    c.mark(1)   # L1: ilustração entrada e saída
    c.mark(2)
    abre_pesagem_item(c, c.A(2, 'item', 0.8))
    c.registra(C1, at=c.A(2, 'primeira', 0.3), label='1ª Pesagem 9.460 (o peso da entrada)')
    c.confere('dlg', ['9.460'], '1ª pesagem 9.460 já preenchida')
    c.mark(3)
    c.click(C2, at=c.A(3, 'segunda', 0.8), label='campo 2ª Pesagem')
    c.type(C2, '6380', at=c.A(3, 'seis', 0.1), noClick=True, label='digita 6380 na 2ª Pesagem')
    c.mark(4)
    c.registra(BRUTO, at=c.A(4, 'bruto', 0.4), label='Peso Bruto 3.080 |9.460 − 6.380|')
    c.confere('dlg', ['3.080', '|9.460 − 6.380|'], 'bruto 3.080 = |9.460 − 6.380|')
    c.hover(BRUTO, 0.6, at=c.A(4, 'Três', 0.6), label='o bruto, a diferença das duas')
    c.mark(5)
    c.hover(TARA, 0.8, at=c.A(5, 'tara', 0.6), label='Tara (Kg) em branco')
    c.mark(6)
    c.click(CONFIRMAR, at=c.A(6, 'Confirmar', 0.7), label='Confirmar')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.mark(7)
    c.click(DETALHE, at=c.A(7, 'setinha', 0.7), label='setinha: Ver detalhes da pesagem')
    c.registra(SEL("main tr:has-text('1ª pesagem')"), at=c.A(7, 'pesagens', 0.3), label='detalhe: 1ª pesagem, 2ª pesagem e Bruto')
    c.confere('main', ['1ª pesagem: 9.460', '2ª pesagem: 6.380', 'Bruto: 3.080'], 'detalhe da pesagem')
    c.fim()
    return c


@capitulo
def cap05():
    """A impureza em porcentagem (2 % = 61,6 kg sobre bruto − tara) e o líquido (3.018,4 kg)."""
    c = Cap(5, start=(1100, 420), setup=setup_lista(REABRE))
    c.mark(1)
    abre_pesagem_item(c, c.A(1, 'impureza', 0.8))
    c.mark(2)
    c.click({'role': 'radio', 'name': '%'}, at=c.A(2, 'porcentagem', 0.9), label='Impureza em %')
    c.click(IMP, label='campo Impureza')
    c.type(IMP, '2', noClick=True, label='digita 2 (%)')
    c.registra(IMP_CONTA, at=c.A(2, 'sessenta', 0.6), label='Impureza 2 % = 61,6 Kg (sobre bruto − tara)')
    c.confere('dlg', ['= 61,6 Kg (sobre bruto − tara)', '3.018,4 Kg'], 'impureza 61,6 e líquido 3.018,4')
    c.mark(3)
    c.hover({'role': 'radio', 'name': 'kg'}, 0.8, at=c.A(3, 'quilos', 0.6), label='seletor kg / %')
    c.mark(4)   # L4: ilustração da conta do líquido
    c.cursor((640, 520), at=c.L(4) + 0.3, label='cursor descansa na janela')
    c.mark(5)
    c.registra(LIQUIDO, at=c.A(5, 'Três', 0.3), label='Líquido (Kg) 3.018,4')
    c.mark(6)
    c.click(CONFIRMAR, at=c.A(6, 'Confirmar', 0.7), label='Confirmar')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.fim()
    return c


@capitulo
def cap06():
    """Um segundo caminhão numa aba nova (Jair, bateria, 5.640 kg), a troca de aba, salvar o #58 e o x que pergunta antes de descartar."""
    c = Cap(6, start=(1150, 330), setup=setup_lista(REABRE))
    c.mark(1)   # L1: ilustração dos dois caminhões
    c.mark(2)
    c.click(NOVO_TICKET, at=c.A(2, 'Novo', 0.7), label='+ Novo ticket')
    c.waitfor(text='Sem cliente/fornecedor', timeout=8)
    # L3: o preenchimento (que a edição pode acelerar) começa logo depois da aba nova; as opções das listas são clicadas por `eval`
    # (sem levar o cursor), como um time-lapse, para caber antes da L4 (só os campos levam o cursor). A página desce 120 px antes
    # (a barra das abas continua na faixa do robô, e motorista e placa entram nela).
    c.rolar(ROLA_FORM, ponto=(700, 460), duration=0.4, after=0, label='desce o formulário (a barra das abas segue à vista)')
    c.click(SEL_FORN, label='Selecionar fornecedor (aba do Jair)')
    c.waitfor(text='Selecionar Fornecedor', timeout=8)
    c.ev(js_clica('[role=dialog] button', 'Auto Peças Vale Forte'), label='Auto Peças Vale Forte (clique sem cursor)')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.mark(3)
    c.click(MAT, at=round(c.L(3) - 0.2, 2), label='campo Material')
    c.type(MAT, 'bateria', cps=40, noClick=True, label='digita bateria')
    c.press('Enter', label='Enter escolhe Bateria automotiva')
    c.click(MOT, label='campo Motorista')
    c.type(MOT, 'Jair', cps=40, noClick=True, label='digita Jair')
    c.ev(js_clica('[role=option]', 'Jair Lopes'), label='Jair Lopes (clique sem cursor)')
    c.pause(0.3)
    c.click(PLACA, label='campo Placa do Veículo')
    c.type(PLACA, 'GHT', cps=40, noClick=True, label='digita GHT')
    c.ev(js_clica('[role=option]', 'GHT7B19'), label='GHT7B19 (clique sem cursor)')
    c.pause(0.3)
    c.click(PES_AV, label='Pesagem avançada (Jair)')
    c.waitfor(text='Registre pesagem dupla, tara, impureza e dados do transporte', timeout=8)
    c.pause(0.3)
    c.type(C1, '5640', noClick=True, label='digita 5640 na 1ª Pesagem (o campo já vem com o foco)')
    c.click(CONFIRMAR, label='Confirmar (Jair)')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.confere('main', ['#59', '5.640 kg', 'Auto Peças Vale Forte'], 'aba do Jair: #59 com 5.640 kg')
    c.mark(4)
    c.click(BARRA, at=c.A(4, 'barra', 0.7), label='barra das abas: a lista dos dois tickets')
    c.registra(SEL(POP), at=c.A(4, 'troca', 0.2), label='lista das abas: #58 Cooperativa e #59 Auto Peças')
    c.hover(LINHA_ABA(58), 0.4, at=c.A(4, 'caminhão', 0.6), label='aba #58')
    c.hover(LINHA_ABA(59), 0.4, at=c.A(4, 'outro', 0.6), label='aba #59')
    c.mark(5)
    c.click(LINHA_ABA(58), at=c.A(5, 'cooperativa', 0.6), label='troca para o #58')
    c.click(SALVAR, at=c.A(5, 'salvo', 0.8), label='Salvar Ticket de Pesagem')
    c.waitfor(text='O que deseja fazer com este ticket de pesagem?', timeout=12)
    c.registra(SEL(DLG), at=c.A(5, 'número', 0.3), label='Ticket #58 salvo (Imprimir comprovante, Valorizar, Fechar)')
    c.confere('dlg', ['Ticket #58 salvo'], 'número de verdade: #58')
    c.mark(6)
    c.click({'role': 'button', 'name': 'Fechar', 'exact': True, 'within': DLG, 'nth': 0}, at=c.A(6, 'depois', 0.7), label='Fechar')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.hover(BARRA, 0.8, at=c.A(6, 'Jair', 0.6), label='fica a aba do Jair (#59)')
    c.mark(7)
    c.click(BARRA, at=c.A(7, 'fechar', 0.7), label='abre a lista das abas')
    c.hover(X_ABA, 0.8, at=c.A(7, 'x', 0.6), label='o x da aba (Descartar ticket), sem clicar')
    c.press('Escape', at=c.A(7, 'ticket', -0.4), label='fecha a lista')
    c.mark(8)
    c.click(BTN('Voltar'), at=c.A(8, 'E', 0.1), label='Voltar para a tela dos tickets')
    c.waitfor(text=TICKET_OK, timeout=15)
    c.click(APAGADOS, at=c.A(8, 'Rascunhos', 0.8), label='Rascunhos apagados (1)')
    c.waitfor(text='Recupere um rascunho que foi apagado por engano.', timeout=8)
    c.confere('dlg', ['Valdir Pereira', 'Ferro misto', 'Recuperar'], 'lixeira de rascunhos')
    c.hover(BTN('Recuperar', within=DLG), 0.8, at=c.A(8, 'recuperar', 0.6), label='Recuperar (sem clicar)')
    c.press('Escape', label='fecha Rascunhos apagados')
    c.fim()
    return c


# ---------------------------------------------------------------- ticket com valores (aba do Jair)
VKG = CAMPO('Valor/Kg')
USAB = '/configuracoes?tab=usability'


@capitulo
def cap07():
    """Ticket com valores: a aba do Jair vira "Com valores", 2ª pesagem 4.180 kg e R$ 3,40/kg (R$ 4.964,00); salva o #59."""
    c = Cap(7, start=(1150, 330), setup=setup_lista(REABRE))
    c.mark(1)
    c.hover(BTN('Com valores'), 0.6, at=c.A(1, 'valores', 0.6), label='chave Valores (sem clicar)')
    c.mark(2)
    c.click(BTN('Com valores'), at=c.A(2, 'Com', 0.7), label='Com valores')
    # 1.60.18 (commit 12e026efd): item sem preço -> "Colocar os preços?" com o preço achado; o da bateria vem do PREÇO DO FORNECEDOR
    # (R$ 3,40/kg, o combinado com a Auto Peças): "Preencher 1 preço". A 1ª pesagem (5.640) já está no campo dela (commit 4d19302a3).
    c.waitfor(text='Colocar os preços?', timeout=8)
    c.registra(SEL(DLG), at=c.A(2, 'pergunta', 0.2), label='Colocar os preços? (Bateria automotiva · Preço do fornecedor · R$ 3,40/kg)')
    c.hover(SEL(f"{DLG} li:has-text('Bateria automotiva')"), 0.6, at=c.A(2, 'combinado', 0.4), label='Bateria automotiva · Preço do fornecedor · R$ 3,40/kg')
    c.click(BTNX('Preencher 1 preço', within=DLG), at=c.A(2, 'Preencher', 0.6), label='Preencher 1 preço')
    c.waitfor(text='Total geral', timeout=8)
    c.mark(3)
    c.hover(SEL("main div:has(> label:has-text('Tabela de Preços')) button[role=combobox]"), 0.6, at=c.A(3, 'Tabela', 0.6), label='Tabela de Preços (Principal)')
    c.registra(SEL("main th:has-text('Valor/Kg')"), at=c.A(3, 'colunas', 0.3), label='colunas Valor/Kg, Desc. (R$) e Total')
    abre_pesagem_item(c, c.A(3, 'itens', 0.3))
    c.mark(4)
    c.registra(C1, at=c.A(4, 'pesagem', 0.2), label='1ª Pesagem 5.640 (a entrada)')
    c.click(C2, at=c.A(4, 'segunda', 0.8), label='campo 2ª Pesagem')
    c.type(C2, '4180', at=c.A(4, 'quatro', 0.1), noClick=True, label='digita 4180 na 2ª Pesagem')
    c.registra(VKG, at=c.A(4, 'preço', 0.3), label='Valor/Kg 3,40 (já preenchido)')
    c.confere('dlg', ['1.460', '|5.640 − 4.180|', 'R$ 4.964,00'], 'bruto 1.460 e valor estimado R$ 4.964,00')
    c.mark(5)
    c.click(CONFIRMAR, at=c.A(5, 'Confirmar', 0.7), label='Confirmar')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.hover(SEL("main tr:has-text('Bateria automotiva')"), 0.5, at=c.A(5, 'mil', 0.6), label='item: 1.460 kg de bateria a 3,40')
    c.registra(SEL("main tr:has-text('Total geral')"), at=c.A(5, 'total', 0.3), label='Total geral: R$ 4.964,00')
    c.hover(SEL("main tr:has-text('Total geral')"), 0.8, at=c.A(5, 'embaixo', 0.6), label='Total geral')
    c.confere('main', ['Total geral: R$ 4.964,00'], 'total do ticket R$ 4.964,00')
    c.mark(6)
    c.cursor(NEUTRO, at=c.L(6) + 0.4, label='cursor descansa')
    c.mark(7)
    c.click(SALVAR, at=round(c.L(7) - 0.2, 2), label='Salvar Ticket de Pesagem')
    c.waitfor(text='O que deseja fazer com este ticket de pesagem?', timeout=12)
    c.confere('dlg', ['Ticket #59 salvo'], 'número do ticket do Jair: #59')
    c.click({'role': 'button', 'name': 'Fechar', 'exact': True, 'within': DLG, 'nth': 0}, at=c.A(7, 'valor', 0.7), label='Fechar')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.mark(8)
    c._p({'do': 'goto', 'url': USAB}, c.A(8, 'E', 0.1), 'Configurações > Usabilidade', {})
    c.waitfor(text='Permitir forma de pagamento no ticket de pesagem', timeout=15)
    c.ev(js_ate('Permitir forma de pagamento no ticket de pesagem', y=380, dur_ms=900), at=c.A(8, 'balanceiro', 0.3), label='rola até a opção')
    c.hover(TXT('Permitir forma de pagamento no ticket de pesagem'), 0.8, at=c.A(8, 'forma', 0.6), label='Permitir forma de pagamento no ticket de pesagem (desligada)')
    c.registra(TXT('Permitir forma de pagamento no ticket de pesagem'), at=c.A(8, 'ligar', 0.3), label='a opção, em Configurações > Usabilidade')
    c.fim()
    return c


# ---------------------------------------------------------------- valorizar, comprovante e finalizar
RECOLHE_MENU = ("(()=>{const w=document.querySelector('[data-state][data-collapsible]');if(w&&w.getAttribute('data-state')==='collapsed')return 'ja recolhido';"
                "const b=document.querySelector(\"button[aria-label='Toggle Sidebar']\");if(!b)return 'sem botao';b.click();return 'recolhido'})()")
LINHA_COMPRA = "main tr:has-text('Alumínio latinha')"
CEL = lambda k: SEL(f'{LINHA_COMPRA} td:nth-child({k})')        # 3 peso líquido, 4 tara/imp., 5 valor/kg, 6 valor total
POPS = "(()=>{const o=window.open;window.__pops=[];window.open=function(...a){const w=o.apply(this,a);window.__pops.push(w);return w};return 'ok'})()"
# o PDF do comprovante que o app abre na aba nova (a gravação filma uma aba só): devolvido em base64 para virar a ilustração da edição
PDF_JS = ("(async()=>{const w=(window.__pops||[]).slice(-1)[0];if(!w)return 'SEM JANELA';for(let i=0;i<40;i++){let f=null;"
          "try{f=w.document&&w.document.querySelector('#pdf-frame')}catch(e){return 'ERRO '+e}"
          "if(f&&f.src){const b=await (await fetch(f.src.split('#')[0])).blob();const u=new Uint8Array(await b.arrayBuffer());let s='';"
          "for(let k=0;k<u.length;k+=8192)s+=String.fromCharCode.apply(null,u.subarray(k,k+8192));return 'PDF:'+btoa(s)}"
          "await new Promise(r=>setTimeout(r,250))}return 'SEM PDF'})()")
SELEC = lambda n: SEL(f"[aria-label='Selecionar ticket #{n}']")
BARRA_SEL = "div.fixed:has-text('selecionad')"       # barra flutuante "2 selecionados | Valorizar 2 tickets | x"
ROLA_KANBAN = 270                                    # o #56 é o 4º cartão da coluna: fica abaixo da dobra


def setup_valorizar(extra=()):
    return setup_lista([{'do': 'eval', 'js': RECOLHE_MENU}, {'do': 'wait', 'seconds': 0.8}] + list(extra))


@capitulo
def cap08():
    """Valorizar: a dica do Valorizar 2 tickets (#58 e #56, mesmo fornecedor) e Ações > Valorizar abre a compra (R$ 6,20/kg, R$ 18.714,08)."""
    c = Cap(8, start=(700, 420), setup=setup_valorizar())
    c.mark(1)
    c.hover(SEL(CARTAO(58)), 0.8, at=c.A(1, 'valorizar', 0.6), label='cartão do Ticket #58')
    c.mark(2)
    c.click(SELEC(58), at=c.A(2, 'Selecionar', 1.0), label='Selecionar no #58')
    c.rolar(ROLA_KANBAN, at=c.A(2, 'Selecionar', -0.2), ponto=(420, 500), duration=0.5, after=100, label='desce até o #56')
    c.click(SELEC(56), at=c.A(2, 'cada', 0.3), label='Selecionar no #56 (o outro ticket da cooperativa)')
    c.registra(SEL(BARRA_SEL), at=c.A(2, 'Valorizar', 0.8), label='barra: 2 selecionados, Valorizar 2 tickets')   # a barra é fixa no pé da tela: noScroll nos gestos nela
    c.hover(BTNX('Valorizar 2 tickets'), 0.8, at=c.A(2, 'Valorizar', 0.6), noScroll=True, label='Valorizar 2 tickets (sem clicar)')
    c.confere('body', ['2 selecionados', 'Valorizar 2 tickets'], 'barra da seleção em conjunto')
    c.hover(SELEC(57), 1.0, at=c.A(2, 'Precisa', 0.6), label='#57, de outro fornecedor, fica apagado (dica: mesmo cliente ou fornecedor)')
    c.mark(3)
    c.click(SEL(f'{BARRA_SEL} > button'), at=round(c.L(3) - 0.2, 2), noScroll=True, label='x da barra: limpa a seleção')
    c.rolar(-ROLA_KANBAN, ponto=(420, 500), duration=0.4, after=100, label='volta ao alto da coluna')
    c.click(ACOES(58), at=c.A(3, 'Ações', 0.7), label='Ações do #58')
    c.click(ITEM('Valorizar'), label='Valorizar')
    c.waitfor(text='Origem: Ticket de Pesagem', timeout=15)
    c.confere('main', ['Origem: Ticket de Pesagem #58', 'R$ 18.714,08'], 'compra do #58: total R$ 18.714,08')
    c.confere_campos(['6,20', '61,6'], 'Valor/Kg 6,20 e Tara/Imp. 61,6', escopo='main tbody')
    c.hover(TXTX('Cooperativa Recomeço', within='main'), 0.3, at=c.A(3, 'cooperativa', 1.0), label='compra: fornecedor Cooperativa Recomeço')
    c.hover(CEL(2), 0.3, at=c.A(3, 'latinha', 0.8), label='compra: Alumínio latinha')
    c.hover(CEL(4), 0.5, at=c.A(3, 'impureza', 0.8), label='compra: peso líquido e Tara/Imp. 61,6')
    c.mark(4)
    c.registra(CEL(5), at=c.A(4, 'seis', 0.3), label='Valor/Kg 6,20')
    c.hover(CEL(6), 0.6, at=c.A(4, 'dezoito', 0.6), label='total da linha R$ 18.714,08')
    c.mark(5)
    c.hover(CEL(5), 0.8, at=c.A(5, 'preço', 0.6), label='Valor/Kg: de onde vem o preço')
    c.mark(6)
    c.hover(CEL(5), 0.8, at=c.A(6, 'aqui', 0.6), label='célula Valor/Kg')
    c.mark(7)   # L7: ilustração do caminho até o estoque e o caixa
    c.cursor((760, 560), at=c.L(7) + 0.3, label='cursor descansa')
    c.fim()
    return c


def linha_conf(rot, antes_de):
    """a linha de uma opção de Configurações > Usabilidade (o rótulo `rot`, sem a opção seguinte `antes_de`)"""
    return f"main div:has(label:text-is('{rot}')):not(:has(label:text-is('{antes_de}')))"


SW_ASSINA = SEL(linha_conf('Assinaturas no comprovante', 'Marca de ticket não valorizado') + ' button[role=switch]')
QUEM = SEL('#receipt-signature-mode')


@capitulo
def cap09():
    """O comprovante do ticket (Térmico, PDF na aba nova), a impressão sozinha em Integrações e, em Usabilidade, as assinaturas
    (liga, mostra Quem assina e desliga de novo: regra do mundo), a marca de não valorizado e o exigir fornecedor."""
    c = Cap(9, start=(700, 420), setup=setup_valorizar([{'do': 'eval', 'js': POPS}]))
    c.mark(1)
    c.click(ACOES(58), at=c.A(1, 'Ações', 0.7), label='Ações do #58')
    c.click(ITEM('Ver comprovante'), label='Ver comprovante')
    c.waitfor(text='Escolha o formato do comprovante deste ticket de pesagem.', timeout=8)
    c.hover(BTNX('Térmico', within=DLG), 0.4, at=c.A(1, 'Térmico', 0.6), label='Térmico (80mm)')
    c.hover(BTNX('A4', within=DLG), 0.4, at=c.A(1, 'A4', 0.6), label='A4 (Folha)')
    c.click(BTNX('Térmico', within=DLG), at=c.A(1, 'folha', -0.3), label='Térmico: o PDF abre na aba nova')
    c.mark(2)
    c.ev(PDF_JS, at=c.L(2), label='PDF do comprovante térmico (aba nova, para a ilustração)')
    c.mark(3)
    c.mark(4)
    c._p({'do': 'goto', 'url': '/configuracoes?tab=integrations'}, c.A(4, 'E', 0.2), 'Configurações > Integrações', {})
    c.waitfor(text='Imprimir comprovante do Ticket de Pesagem', timeout=15)
    c.ev(js_ate('Imprimir comprovante do Ticket de Pesagem', y=400, dur_ms=900), at=c.A(4, 'cupom', 0.3), label='rola até a chave')
    c.hover(TXT('Imprimir comprovante do Ticket de Pesagem'), 0.8, at=c.A(4, 'Imprimir', 0.6), label='chave Imprimir comprovante do Ticket de Pesagem (desligada)')
    c.mark(5)
    c._p({'do': 'goto', 'url': USAB}, c.A(5, 'Quer', 0.2), 'Configurações > Usabilidade', {})
    c.waitfor(text='Assinaturas no comprovante', timeout=15)
    c.ev(js_ate('Assinaturas no comprovante', y=300, dur_ms=700), at=c.A(5, 'assine', 0.2), label='rola até Assinaturas no comprovante')
    c.click(SW_ASSINA, at=c.A(5, 'ligue', 0.7), label='liga Assinaturas no comprovante')
    c.waitfor(text='Quem assina', timeout=8)
    c.click(QUEM, at=c.A(5, 'escolha', 0.7), label='Quem assina (abre a lista)')
    c.hover(OPT('Operador e cliente/fornecedor'), 0.4, at=c.A(5, 'dois', 0.5), label='Operador e cliente/fornecedor')
    c.hover(OPT('Só o cliente/fornecedor'), 0.4, at=c.A(5, 'fornecedor', 0.5), label='Só o cliente/fornecedor')
    c.hover(OPT('Só o operador'), 0.4, at=c.A(5, 'operador', 0.5), label='Só o operador')
    c.mark(6)
    c.click(OPT('Só o cliente/fornecedor'), at=round(c.L(6) - 0.2, 2), label='escolhe Só o cliente/fornecedor')
    c.hover(TXTX('o operador aparece como Empresa'), 0.8, at=c.A(6, 'operador', 0.6), label='No ticket de pesagem, o operador aparece como Empresa.')
    c.mark(7)
    c.hover(TXT('Marca de ticket não valorizado'), 0.6, at=c.A(7, 'tirar', 0.6), label='Marca de ticket não valorizado (ligada)')
    c.ev(js_ate('Exigir cliente/fornecedor no Ticket de Pesagem', y=420, dur_ms=800), at=c.A(7, 'exigir', 1.4), label='rola até Exigir cliente/fornecedor')
    c.hover(TXT('Exigir cliente/fornecedor no Ticket de Pesagem'), 0.8, at=c.A(7, 'exigir', 0.5), label='Exigir cliente/fornecedor no Ticket de Pesagem (desligada)')
    c.mark(8)   # L8: ilustração das pesagens mescladas; por baixo, o robô devolve as assinaturas ao padrão do mundo (desligadas)
    c.ev(js_ate('Assinaturas no comprovante', y=300, dur_ms=500), at=c.L(8) + 0.3, label='volta até Assinaturas no comprovante')
    c.click(QUEM, label='Quem assina (de volta ao padrão)')
    c.click(OPT('Operador e cliente/fornecedor'), label='Operador e cliente/fornecedor')
    c.click(SW_ASSINA, label='desliga Assinaturas no comprovante (mundo: assinatura desligada)')
    c.ev("(async()=>{await new Promise(r=>setTimeout(r,900));const l=[...document.querySelectorAll('main label')].find(x=>x.textContent.trim()==='Assinaturas no comprovante');"
         "let e=l;for(let i=0;i<6&&e;i++){const s=e.querySelector('[role=switch]');if(s)return s.getAttribute('aria-checked')==='false'?'OK: assinaturas desligadas':'DIFERENTE: assinaturas ligadas';e=e.parentElement}"
         "return 'SEM ALVO'})()", label='confere assinaturas desligadas')
    c.cursor((800, 560), label='cursor descansa')
    c.fim()
    return c


FILTRO = lambda rot: SEL(f"[role=dialog] button[aria-haspopup=dialog]:has-text('{rot}')")   # os três botões do painel Filtros (popover com role=dialog)


@capitulo
def cap10():
    """Editar/Excluir enquanto espera; valorizar de novo retoma a compra; finalizar com Pix; Valorizados e Ver pedido; a lista com
    os status, o período, os filtros e o Exportar; o ticket do Jair segue pendente."""
    c = Cap(10, start=(700, 420), setup=setup_valorizar())
    c.mark(1)
    c.hover(SEL(CARTAO(58)), 0.8, at=c.A(1, 'aqui', 0.6), label='cartão #58 ainda em Aguardando valorização')
    c.mark(2)
    c.click(ACOES(58), at=c.A(2, 'corrigir', 0.9), label='Ações do #58')
    c.hover(ITEM('Editar'), 0.5, at=c.A(2, 'Editar', 0.5), label='Editar (sem clicar)')
    c.hover(ITEM('Excluir'), 0.5, at=c.A(2, 'Excluir', 0.5), label='Excluir (sem clicar)')
    c.mark(3)
    c.click(ITEM('Valorizar'), at=c.A(3, 'retoma', 0.8), label='Valorizar de novo (retomando)')
    c.waitfor(text='Origem: Ticket de Pesagem', timeout=15)
    c.confere('body', ['retomando', '1 item, R$ 18.714,08'], 'aviso: retoma a mesma compra')
    c.mark(4)
    c.click(BTN('Finalizar'), at=c.A(4, 'Finalizo', 0.7), label='Finalizar')
    c.waitfor(text='Finalizar Pedido', timeout=10)
    c.click({'text': 'Pix/Transferência', 'within': DLG}, at=c.A(4, 'Pix', 0.6), label='Pix/Transferência')
    c.click(BTN('CONFIRMAR PAGAMENTO'), at=c.A(4, 'confirmar', 0.7), label='CONFIRMAR PAGAMENTO')
    c.waitfor(text='Valorizado pelo pedido', timeout=20)
    c.mark(5)
    c.hover(TXTX('Valorizado pelo pedido'), 0.8, at=c.A(5, 'número', 0.6), label='Valorizado pelo pedido #…')
    c.confere('main', ['Valorizados', 'Valorizado pelo pedido', '3.018,4 kg'], 'o #58 em Valorizados')
    c.click(SEL("main button:has-text('Ações') >> nth=-1"), at=c.A(5, 'Ações', 0.7), label='Ações do #58 (valorizado: o último cartão, na coluna Valorizados)')
    c.hover(ITEM('Ver pedido'), 0.8, at=c.A(5, 'Ver', 0.5), label='Ver pedido (sem clicar)')
    c.press('Escape', at=c.A(5, 'compra', -0.5, nth=1), label='fecha o menu')
    c.mark(6)
    c.click({'role': 'radio', 'name': 'Lista'}, at=c.A(6, 'lista', 0.7), label='Lista')
    c.hover(TXT('Aguardando valorização', within='main tbody', nth=0), 0.4, at=c.A(6, 'Aguardando', 0.6), label='selo Aguardando valorização')
    c.hover(TXT('Valorizado', within='main tbody'), 0.3, at=c.A(6, 'Valorizado', 0.6), label='selo Valorizado (#58)')
    c.click(BTN('Filtros'), at=c.A(6, 'verde', 0.3), label='Filtros')
    c.click(FILTRO('Status'), label='Status')
    c.hover(SEL("[role=dialog] :text-is('Cancelado') >> nth=-1"), 0.5, at=c.A(6, 'Cancelado', 0.6, nth=0), label='status Cancelado (opção do filtro)')
    c.mark(7)
    c.press('Escape', at=round(c.L(7) - 0.2, 2), label='fecha a lista de status')
    # 18/11: o painel Filtros fica aberto da linha 6 para a 7 (fechar com Escape e reabrir deixava o painel invisível no 1.60.18)
    c.hover(SEL("main button[role=combobox]:has-text('Este mês')"), 0.8, at=c.A(7, 'período', 0.7), label='período (Este mês), só na Lista')
    c.hover(FILTRO('Tipo'), 0.3, at=c.A(7, 'tipo', 0.5), label='filtro Tipo')
    c.hover(FILTRO('Status'), 0.3, at=c.A(7, 'situação', 0.5), label='filtro Status')
    c.hover(FILTRO('Usuário'), 0.4, at=c.A(7, 'usuário', 0.5), label='filtro Usuário')
    c.mark(8)
    c.press('Escape', at=round(c.L(8) - 0.2, 2), label='fecha Filtros')
    c.click(BTN('Exportar'), at=c.A(8, 'Exportar', 0.6), label='Exportar')
    c.hover(ITEM('Excel'), 0.3, at=c.A(8, 'relatório', 0.4), label='Excel')
    c.click(ITEM('PDF'), at=c.A(8, 'pê', 0.5), label='PDF')
    c.waitfor(text='Escolha quais tickets serão incluídos no relatório', timeout=8)
    c.registra(SEL(DLG), at=c.A(8, 'período', 0.3), label='Exportar PDF: Período, Tipo de Ticket, Status, Usuário que criou')
    c.hover(TXTX('Usuário que criou', within=DLG, nth=0), 0.6, at=c.A(8, 'usuário', 0.6), label='Usuário que criou')
    c.mark(9)
    c.press('Escape', at=round(c.L(9) - 0.2, 2), label='fecha o Exportar sem gerar')
    c.cursor(NEUTRO, label='cursor descansa')
    c.mark(10)
    c.click({'role': 'radio', 'name': 'Kanban'}, at=round(c.L(10) - 0.2, 2), label='volta ao Kanban')
    c.hover(SEL(CARTAO(59)), 0.8, at=c.A(10, 'Jair', 0.6), label='Ticket #59 do Jair: Aguardando valorização, R$ 4.964,00')
    c.confere('main', ['Ticket #59', 'R$ 4.964,00'], 'o #59 segue pendente com o valor')
    c.fim()
    return c


# ---------------------------------------------------------------- pesagem avulsa com cobrança
AVULSA_OK = 'Preencha a pesagem avulsa. Use as abas para atender vários veículos.'
BUSCA_CLI = SEL("[role=dialog] input[placeholder^='Buscar por nome']")
CADASTRAR = SEL("[role=dialog] button:has-text('Cadastrar «')")
DESC = PH('Ex.: Areia, terra, entulho')
TIPO_CAM = SEL('#standalone-vehicle-type')
TAXA = SEL('#standalone-weighing-fee')
LINHA_60 = "main tbody tr:has-text('#60')"


@capitulo
def cap11():
    """Pesagem avulsa da Areal Boa Vista, enxuta (18/11, pedido do Kaik: 13 -> 6 linhas): cadastra o cliente pela busca só com o nome,
    areia média, 23.840 − 9.120 = 14.720 kg, R$ 60,00 por Pix na Conta Principal; ticket #60 e o comprovante (PDF para a
    ilustração). Saíram: os campos do cadastro rápido, a placa, o tipo de caminhão, o "Completo" e o valor travado no Editar."""
    c = Cap(11, start=(700, 420), setup=setup_lista([{'do': 'eval', 'js': POPS}]))
    c.mark(1)   # L1: ilustração do caminhão de areia
    c.cursor(NEUTRO, at=0.3, label='cursor descansa')
    c.mark(2)
    c.click(ABA_AVULSAS, at=c.A(2, 'Pesagens', 0.8), label='aba Pesagens avulsas')
    c.click(BTN('Nova Pesagem Avulsa'), at=c.A(2, 'Nova', 0.7), label='Nova Pesagem Avulsa')
    c.waitfor(text=AVULSA_OK, timeout=15)
    c.registra(TXT('Serviço ao cliente'), label='Modalidade Pesagem avulsa, Tipo Serviço ao cliente')
    c.click(TXT('Selecionar cliente'), at=c.A(2, 'O', 1.0), label='Selecionar cliente')
    c.waitfor(text='Selecionar Cliente', timeout=8)
    c.type(BUSCA_CLI, 'Areal Boa Vista', at=c.A(2, 'caminhão', 0.3), cps=16, label='busca Areal Boa Vista')
    c.waitfor(text='Nenhum resultado encontrado.', timeout=8)
    c.click(CADASTRAR, at=c.A(2, 'hora', 0.7), label='Cadastrar «Areal Boa Vista»')
    c.waitfor(text='Cadastre um novo cliente rapidamente', timeout=8)
    c.confere_campos(['Areal Boa Vista'], 'Nome já preenchido')
    c.click(BTN('Criar Cliente'), at=c.A(2, 'nome', 0.5), label='Criar Cliente (só com o nome)')
    c.waitfor(gone={'role': 'dialog'}, timeout=10)
    c.confere('main', ['Areal Boa Vista', '#60'], 'cliente escolhido no ticket')
    c.mark(3)
    c.click(DESC, at=round(c.L(3) - 0.2, 2), label='Descrição do material')
    c.type(DESC, 'Areia média', noClick=True, cps=14, label='digita Areia média')
    c.click(PES_AV, at=c.A(3, 'peso', 0.2), label='Pesagem avançada')
    c.waitfor(text='Registre pesagem dupla, tara, impureza e dados do transporte', timeout=8)
    c.pause(0.3)
    c.type(C1, '23840', at=c.A(3, 'entrada', 0.0), noClick=True, label='digita 23840 na 1ª Pesagem')
    c.click(C2, label='campo 2ª Pesagem')
    c.type(C2, '9120', at=c.A(3, 'saída', -0.9), noClick=True, label='digita 9120 na 2ª Pesagem')
    c.registra(BRUTO, at=c.A(3, 'catorze', -0.6), label='Peso Bruto 14.720 |23.840 − 9.120|')
    c.confere('dlg', ['14.720', '|23.840 − 9.120|'], 'bruto 14.720')
    c.click(CONFIRMAR, at=c.A(3, 'vinte', 0.2), label='Confirmar')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.mark(4)
    c.rolar(300, at=round(c.L(4) - 0.2, 2), ponto=(700, 460), duration=0.4, after=0, label='desce até o valor cobrado')
    c.click(TAXA, at=c.A(4, 'cobrado', 0.3), label='Valor cobrado pela pesagem')
    c.type(TAXA, '60', at=c.A(4, 'sessenta', 0.1), noClick=True, label='digita 60')
    c.press('Tab', label='sai do campo (vira 60,00)')
    c.registra(SEL("main div.grid:has(#standalone-weighing-fee)"), at=c.A(4, 'reais', 0.2), label='Valor cobrado pela pesagem R$ 60,00')
    c.confere_campos(['60,00'], 'valor cobrado', escopo='main')
    c.mark(5)
    c.click(BTN('Salvar Pesagem Avulsa'), at=c.A(5, 'salvar', 0.6), label='Salvar Pesagem Avulsa')
    c.waitfor(text='Finalizar Pedido', timeout=10)
    c.confere('dlg', ['Total: R$ 60,00', 'Cliente: Areal Boa Vista'], 'pagamento da pesagem: R$ 60,00')
    c.click(BTN('Pix/Transferência', within=DLG), at=c.A(5, 'Pix', 0.8), label='Pix/Transferência (Conta Principal já escolhida)')
    c.confere('dlg', ['Conta Principal'], 'Conta Principal já escolhida')
    c.hover(BTN('Dinheiro', within=DLG), 0.4, at=c.A(5, 'dinheiro', 0.6), label='Dinheiro (sem clicar)')
    c.hover(BTN('Saldo do Cliente', within=DLG), 0.5, at=c.A(5, 'saldo', 0.6), label='Saldo do Cliente (sem clicar)')
    c.mark(6)
    c.click(BTN('CONFIRMAR PAGAMENTO'), at=round(c.L(6) - 0.2, 2), label='CONFIRMAR PAGAMENTO')
    c.waitfor(text='O que deseja fazer com este ticket de pesagem?', timeout=12)
    c.registra(SEL(DLG), at=c.A(6, 'valor', 0.2), label='Ticket #60 salvo, PESAGEM AVULSA (Imprimir comprovante, Fechar)')
    c.confere('dlg', ['Ticket #60 salvo', 'PESAGEM AVULSA', 'Serviço de pesagem cobrado: R$ 60,00'], 'pesagem avulsa #60 salva (1.60.18)')
    # 1.60.18: o aviso diz o que foi cobrado ("Serviço de pesagem cobrado: R$ 60,00. Não vira pedido de compra nem de venda.")
    c.registra(TXTX('Serviço de pesagem cobrado', within=DLG), at=c.A(6, 'sem', 0.2), label='Serviço de pesagem cobrado: R$ 60,00 (não vira pedido)')
    # o PDF do app vira a ilustração do comprovante; depois o robô volta à lista das avulsas e para
    c.click(BTN('Imprimir comprovante', within=DLG), at=c.A(6, 'estoque', 0.9), label='Imprimir comprovante')
    c.waitfor(text='Escolha o formato do comprovante deste ticket de pesagem.', timeout=8)
    c.click(BTNX('Térmico', within=DLG), at=c.A(6, 'comprovante', 0.5), label='Térmico: o PDF abre na aba nova')
    c.ev(PDF_JS, label='PDF do comprovante da pesagem avulsa (aba nova, para a ilustração)')
    c.click(BTN('Voltar'), at=c.A(6, 'marcado', 0.3), label='Voltar para a lista (aba Pesagens avulsas)')
    c.waitfor(text=TICKET_OK, timeout=15)
    c.confere('main', ['#60', 'Areal Boa Vista', '14.720 kg'], 'a #60 na lista das avulsas')
    c.cursor(NEUTRO, label='cursor descansa')
    c.fim()
    return c


# ---------------------------------------------------------------- sem internet
# Queda DE VERDADE (passo `rede` do runner, acréscimo de 18/11): toda requisição ao backend é abortada na rede e o navegador segue
# se dizendo online (roteador ligado, link caído). O app decide por ping (/auth/v1/health, hooks/useOnlineStatus.ts): 2 falhas
# seguidas do ping de 1 em 1 minuto. No `setup` o relógio do navegador é adiantado 2 x 61 s para o app medir (a tela começa 09:22);
# na volta, `avisar` dispara o evento `online`, que só faz o app medir na hora (2 pings bons, ~3 s) em vez de esperar até 2 min.
# NÃO usar `modo: navegador` (setOffline): com o evento `offline` do navegador o react-query pausa a mutação do Salvar e o botão
# fica girando até a rede voltar (defeito do app, andamento_160.md). Explorado em _ex/e9 (t08_ex3.py).
# Semente: apos-cap11 (o ticket novo ganha o #61). Para ensaiar sem ela: T08_SEM12=apos-cap08 (aí o número é o #60).
SEM12 = os.environ.get('T08_SEM12') or SEMENTE[12]
SEMENTE[12] = SEM12
NUM12 = 61 if SEM12 == 'apos-cap11' else 60
AVISO_FORM = TXTX('Você pode pesar e finalizar normalmente')
AVISO_LISTA = TXTX('Valorizar, editar ticket já salvo e anexar foto precisam de internet')
AVISO_PROV = SEL("[role=dialog] p:has-text('sem número oficial')")
TOAST = lambda t: SEL(f"[data-sonner-toast]:has-text('{t}')")
CAI = [{'do': 'rede', 'offline': True}, {'do': 'clock', 'forward': '01:01'}, {'do': 'wait', 'seconds': 1.5}, {'do': 'clock', 'forward': '01:01'},
       {'do': 'waitFor', 'text': 'Você pode pesar e finalizar normalmente', 'timeout': 30}]


@capitulo
def cap12():
    """Sem internet: o aviso, pesar e salvar (Ticket OFF-01 guardado neste aparelho, comprovante provisório), as três coisas que esperam
    a internet com o motivo da tela (Anexar, Valorizar, Editar) e a volta da conexão: o ticket sobe sozinho e ganha o número."""
    prep = [{'do': 'click', 'target': BTN('Novo Ticket de Pesagem')}, {'do': 'waitFor', 'text': CRIAR_OK, 'timeout': 20}, {'do': 'waitFor', 'idle': True, 'timeout': 20},
            {'do': 'click', 'target': SEL_FORN}, {'do': 'waitFor', 'text': 'Selecionar Fornecedor', 'timeout': 8},
            {'do': 'click', 'target': FORN('Cooperativa Recomeço')}, {'do': 'waitFor', 'gone': {'role': 'dialog'}, 'timeout': 8},
            *MATERIAL_LATINHA,
            {'do': 'type', 'target': MOT, 'text': 'Edson', 'cps': 40}, {'do': 'click', 'target': OPT('Edson Moura')},
            {'do': 'type', 'target': PLACA, 'text': 'FKD', 'cps': 40}, {'do': 'click', 'target': OPT('FKD2E41')},
            {'do': 'wait', 'seconds': 2.5}, {'do': 'waitFor', 'idle': True, 'timeout': 20},      # o rascunho sobe antes da queda
            *CAI,
            {'do': 'eval', 'js': js_ate('Sem internet.', y=272, dur_ms=200)}, {'do': 'wait', 'seconds': 1.0}]
    c = Cap(12, start=(900, 520), setup=setup_lista(prep))
    c.mark(1)   # L1: ilustração do caminhão na balança com o sinal cortado
    c.cursor((1000, 600), at=0.3, label='cursor descansa')
    c.mark(2)
    # a faixa vermelha só é registrada para a câmera (o cursor não vai até ela: fica fora da faixa do robô, y 18)
    c.registra(SEL('div.bg-red-600'), at=c.A(2, 'avisa', 0.6), label='faixa vermelha: Sem conexão — operações serão salvas localmente')
    c.hover(AVISO_FORM, 0.8, at=c.A(2, 'avisa', 0.5), label='aviso: Sem internet. Você pode pesar e finalizar normalmente')
    c.registra(AVISO_FORM, label='aviso âmbar de sem internet na criação do ticket')
    c.confere('main', ['Sem internet.', 'o ticket fica guardado neste aparelho', 'provisório'], 'aviso de sem internet na criação')
    # desce 220 px: "Pesagem avançada" e "Salvar Ticket de Pesagem" ficam os dois à vista (o Salvar sem rolagem custa ~1 s, não 2,7 s)
    c.rolar(220, at=round(c.A(2, 'pesar', 0.9) - 1.1, 2), ponto=(960, 600), duration=0.4, after=0, label='desce até a pesagem e o Salvar')
    c.click(PES_AV, at=c.A(2, 'pesar', 0.9), noScroll=True, label='Pesagem avançada')
    c.waitfor(text='Registre pesagem dupla, tara, impureza e dados do transporte', timeout=8)
    c.pause(0.3)
    c.type(C1, '7210', at=c.A(2, 'finalizar', -0.25), noClick=True, label='digita 7210 na 1ª Pesagem')
    c.mark(3)
    c.click(CONFIRMAR, at=c.A(3, 'mesmo', 0.9), label='Confirmar')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.click(SALVAR, at=c.A(3, 'salva', 0.9), noScroll=True, label='Salvar Ticket de Pesagem (sem internet)')
    c.waitfor(text='O que deseja fazer com este ticket de pesagem?', timeout=12)
    c.registra(SEL(DLG), at=c.A(3, 'guardado', 0.3), label='Ticket OFF-01 guardado neste aparelho')
    c.confere('dlg', ['Ticket OFF-01 guardado neste aparelho', 'Comprovante provisório (sem número oficial)', 'Valorizar (precisa de internet)'],
              'salvo sem internet: OFF-01, provisório')
    c.hover(AVISO_PROV, 1.0, at=c.A(3, 'provisório', 0.9), label='Comprovante provisório (sem número oficial)')
    c.registra(AVISO_PROV, at=c.A(3, 'número', 0.2), label='sem número oficial: a 2ª via já sai numerada')
    c.mark(4)
    c.click({'role': 'button', 'name': 'Fechar', 'exact': True, 'within': DLG, 'nth': 0}, at=round(c.L(4) - 0.2, 2), label='Fechar')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.click(BTNX('Opções avançadas'), at=c.A(4, 'Anexar', 0.8), noScroll=True, label='Opções avançadas (o sinal cortado no botão)')
    c.hover(TXTX('Disponível com internet'), 0.6, at=c.A(4, 'disponível', 1.3), label='Fotos do pedido · Anexar: Disponível com internet.')
    c.registra(SEL(POP), label='Anexar foto: Disponível com internet.')
    c.confere(POP, ['Anexar', 'Disponível com internet.'], 'anexar foto espera a internet')
    c.press('Escape', at=c.A(4, 'com', 0.5), label='fecha as opções')
    c.rolar(-220, ponto=(960, 600), duration=0.4, after=0, label='volta ao alto (o Voltar à vista)')
    c.click(BTN('Voltar'), at=c.A(4, 'com', -0.5), noScroll=True, label='Voltar para a lista')
    c.waitfor(text=TICKET_OK, timeout=15)
    c.mark(5)
    # o #59 é o primeiro cartão da coluna nas duas sementes: o "Ações" dele está à vista sem rolar
    c.click(ACOES(59), at=c.A(5, 'Valorizar', -0.5), noScroll=True, label='Ações do Ticket #59')
    c.click(ITEM('Valorizar'), at=c.A(5, 'o', -0.3), label='Valorizar (sem internet)')
    c.registra(TOAST('valorizar agora'), at=c.A(5, 'avisa', -0.1), label='Sem internet: não é possível valorizar agora. Valorize quando a conexão voltar.')
    c.confere('body', ['Sem internet: não é possível valorizar agora.', 'Valorize quando a conexão voltar.'], 'motivo do Valorizar')
    c.click(ACOES(59), at=c.A(5, 'E', 0.9, nth=1), noScroll=True, label='Ações do Ticket #59 (de novo)')
    c.click(ITEM('Editar'), at=c.A(5, 'editar', -0.1), label='Editar (sem internet)')
    c.registra(TOAST('editar um ticket'), at=c.A(5, 'salvo', 0.0), label='Sem internet: não é possível editar um ticket já salvo.')
    c.confere('body', ['Sem internet: não é possível editar um ticket já salvo.', 'Você pode criar tickets novos normalmente.'], 'motivo do Editar')
    c.hover(AVISO_LISTA, 0.8, at=c.A(5, 'coisa', 0.6), label='Valorizar, editar ticket já salvo e anexar foto precisam de internet')
    c.registra(SEL("main div.border-amber-300"), label='aviso da lista: 1 ticket aguardando; as três coisas que precisam de internet')
    c.confere('main', ['1 ticket aguardando', 'Valorizar, editar ticket já salvo e anexar foto precisam de internet'], 'aviso da lista sem internet')
    c.mark(6)
    # a volta: o app mede (2 pings, ~3 s), sincroniza e a lista recarrega (~4 s no ensaio): disparada 0,6 s antes da linha
    c.add({'do': 'rede', 'offline': False, 'avisar': True, 'at': round(c.L(6) - 0.8, 2), 'label': 'a conexão volta'})
    c.cursor(NEUTRO, at=round(c.L(6) - 0.2, 2), label='cursor descansa')
    c.waitfor(text=f'Ticket #{NUM12}', timeout=20)
    c.hover(SEL(CARTAO(NUM12)), 1.0, at=c.A(6, 'número', 0.6), label=f'Ticket #{NUM12}: subiu sozinho e ganhou o número')
    c.confere('main', [f'Ticket #{NUM12}', 'Cooperativa Recomeço', '7.210 kg'], f'o ticket sem internet virou o #{NUM12}')
    c.confere('body', ['Aguardando valorização'], 'lista de volta, sem aviso')
    c.fim()
    return c


@capitulo
def cap13():
    """Recapitulando: a montagem é da edição; o robô só deixa a lista parada (o #58 em Valorizados) com as marcas."""
    c = Cap(13, setup=setup_lista())
    c.mark(1)
    c.cursor(NEUTRO, at=0.3, label='cursor descansa')
    for i in range(2, len(c.linhas) + 1):
        c.mark(i)
    c.fim()
    return c


# @@CAPITULOS@@


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


if __name__ == '__main__':
    main()
