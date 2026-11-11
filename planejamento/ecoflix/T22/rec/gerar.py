#!/usr/bin/env python3
"""T22 · Gerencial: matriz e filiais (EcoFlix, EcoSistema 1.59.154): gera rec/t22/cap00..cap11.json (roteiros do robô) a partir da fala
($TUT_HOME/t22/narracao/capNN.json: o estimado até a voz chegar; com a voz, o da voz, sem mudar nada aqui). O cap12 (Recapitulando) é
montagem das gravações dos outros capítulos: não tem robô.

Computador 1280x800, menu lateral aberto. Logado como Rafael Nogueira (MASTER, matriz Recicla Vale Metais) em todos os capítulos, menos o
cap03, gravado como Sandra Pires (MASTER da Filial Pindamonhangaba). FAKE_NOW 2026-11-10T08:30:00-03:00 em todos (o mesmo no Supabase
falso e no robô). Rodar de qualquer pasta: `python3 -I rec/t22/gerar.py [NN ...]` (ANCORAS=1 lista as âncoras). Depois:
`node rec/record.mjs rec/t22/capNN.json --check`; ensaio rápido: `python3 -I rec/t22/ensaio.py NN` + `--rapido`; gravação: sem `--rapido`.

LOGIN: todo capítulo é "anonymous" e o setup entra pela tela de login com "$TUT_USER"/"$TUT_SENHA" do ambiente (Rafael; o Supabase falso
aceita qualquer senha; o valor nunca vai para arquivo nem log). No cap03 o e-mail digitado é o da Sandra (fictício, do mundo) e a senha o
"$TUT_SENHA".

Cada passo é preso a uma palavra da fala: A(linha, 'palavra', folga) = início da palavra − folga (o custo do gesto até o cursor chegar:
clique ~0,6 s, 1º clique numa janela recém-aberta ~1,2 s, hover ~0,5 s; digitação sem clique na palavra − 0,05 s). A palavra casa
INTEIRA (sem acento e pontuação); repetida na linha pede `nth`. Marca Ln 0,9 s antes da linha; um passo que começa até 0,25 s antes da
marca a puxa para o início dele.

Estado de partida (rec/mundo/seeds-extra/t22/, rec/t22/t22_sementes.py e t22_estado.py): `inicio` (a filial, sem grupo) nos caps 0 a 2;
+ `apos-cap02` (o grupo, código GRP-7C4E9A) no cap03; + `apos-cap03` (a filial vinculada) nos caps 4 a 9; + `apos-cap09` (catálogo, tabelas,
categorias, a Fundição marcada e o envio feito) no cap10; + `apos-cap10` (aprovação ligada e a transferência concluída) no cap11;
`apos-cap11` (o pagamento do grupo confirmado) fecha a cadeia.
"""
import hashlib
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TUT = os.path.normpath(os.path.join(HERE, '..', '..'))
AULA = 't22'
NARR = os.path.join(TUT, AULA, 'narracao')
FAKE_NOW = '2026-11-10T08:30:00-03:00'
VERSAO = '1.59.154'
HOJE = FAKE_NOW[:10]
CODIGO = 'GRP-7C4E9A'   # generate_group_invite_code: 'GRP-' + 6 hexadecimais (o handler fixa este)
SANDRA_EMAIL = 'sandra.pires@reciclavalemetais.example'
NOMES = ['Abertura', 'Como o Gerencial funciona', 'Criar o grupo e o código', 'Do lado da filial', 'O Dashboard Gerencial',
         'Ranking e resumo por unidade', 'A DRE do grupo', 'Caixa e competência', 'O estoque do grupo', 'Enviar Ativos',
         'Transferência com aprovação', 'Assinaturas numa fatura só']
_E = ['t22/inicio', 't22/apos-cap02', 't22/apos-cap03', 't22/apos-cap09', 't22/apos-cap10']
SEMENTE = {0: _E[:1], 1: _E[:1], 2: _E[:1], 3: _E[:2], **{n: _E[:3] for n in range(4, 10)}, 10: _E[:4], 11: _E[:5]}

sys.path.insert(0, NARR)
try:
    from tts_textos import CAPS   # noqa: E402
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
    t = re.sub(r'\[[a-z ]+\]', ' ', CAPS.get(n, ''))
    for fala, leg in sorted(TROCAS, key=lambda p: -len(p[0])):
        t = re.sub(r'(?<!\w)' + re.escape(fala) + r'(?!\w)', leg, t)
    return [norm(w) for w in t.split() if norm(w)]


def carregar_voz(n):
    d = json.load(open(os.path.join(NARR, f'cap{n:02d}.json'), encoding='utf8'))
    words = [dict(w) for w in d['words']]
    linhas = [dict(li) for li in d['linhas']]
    if CAPS and texto_atual(n) != [norm(w['w']) for w in words if norm(w['w'])]:
        print(f'  AVISO cap{n:02d}: a fala do capNN.json não é a do tts_textos.py de hoje (rode o preparar_aula.sh de novo)')
    return words, linhas, float(d['dur']), bool(d.get('estimado'))


def stable_id(chave):
    """o mesmo UUID do `@id:<chave>` das sementes (rec/fakebase/core/util.mjs, stableId)"""
    h = bytearray(hashlib.sha1(('domiflix-fake:' + chave).encode()).digest())
    h[6] = (h[6] & 0x0F) | 0x50
    h[8] = (h[8] & 0x3F) | 0x80
    x = h[:16].hex()
    return f'{x[:8]}-{x[8:12]}-{x[12:16]}-{x[16:20]}-{x[20:32]}'


RAFAEL = stable_id('user.rafael')
SANDRA = stable_id('user.sandra')
GRUPO = stable_id('t22.grupo')


def storage(n, extra=None):
    uid = SANDRA if n == 3 else RAFAEL
    d = {'app_version': VERSAO, 'notification_shown_version': VERSAO, 'pwa-install-dismissed': 'true', 'theme': 'light',
         f'daily-tasks-reminder-last-shown-{uid}': HOJE, 'initial-preferences-set': 'true'}
    d.update(extra or {})
    return d


# ---------------------------------------------------------------- observador de avisos de erro (aceite: tem de sair vazio)
OBS = ("(()=>{window.__avisos=[];const re=/N[ãa]o foi poss[ií]vel|Erro ao|Tente novamente|Algo deu errado|Falha ao|Something went wrong|indispon[ií]vel|Access denied/i;"
       "const chk=(t)=>{t=(t||'').trim();const m=t&&t.match(new RegExp('[^]{0,40}('+re.source+')[^]{0,40}','i'));"
       "if(m&&!/fica indispon/i.test(m[0])&&window.__avisos.length<10)window.__avisos.push(m[0].replace(/[\\n\\r\\t ]+/g,' '))};new MutationObserver(ms=>{for(const m of ms){"
       "m.addedNodes.forEach(n=>chk(n.textContent));if(m.type==='characterData')chk(m.target.textContent)}}).observe(document.body,"
       "{childList:true,subtree:true,characterData:true});chk(document.body.innerText);"
       "setInterval(()=>{document.querySelectorAll('[data-sonner-toast][data-type=error]').forEach(t=>{const s='TOAST DE ERRO: '+t.textContent.trim().slice(0,90);"
       "if(!window.__avisos.includes(s)&&window.__avisos.length<10)window.__avisos.push(s)})},300);return 1})()")


class Cap:
    def __init__(s, n, setup, pace=0.5, cps=40, start=(760, 470), storage_extra=None):
        s.n = n
        s.words, s.linhas, s.dur, s.estimado = carregar_voz(n)
        s.steps, s.pending, s.anchors = [], [], []
        s.pace, s.cps, s.start = pace, cps, start
        s.setup = list(setup) + [{'do': 'eval', 'js': OBS}]
        s.storage_extra = storage_extra

    # ---- tempo
    def L(s, i):
        return round(s.linhas[i - 1]['s'], 2)

    def W(s, i, palavra, nth=0, fim=False):
        q = norm(palavra)
        hits = [w for w in s.words if w['linha'] == i - 1 and norm(w['w']) == q]
        if len(hits) <= nth:
            raise SystemExit(f'cap{s.n:02d}: palavra "{palavra}" (#{nth}) não achada na linha {i}: ' + ' '.join(w['w'] for w in s.words if w['linha'] == i - 1))
        return hits[nth]['e' if fim else 's']

    def A(s, i, palavra, folga=0.6, nth=0):
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
        if d.get('at') is not None:
            for mt, mi in s.pending:
                if d['at'] < mt <= d['at'] + 0.25:
                    d['at'] = round(mt, 2)
            s.flush(d['at'])
        s.steps.append(d)
        return d

    def mark(s, i):
        t = max(0.0, s.L(i) - 0.9)
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

    def hover(s, target, seconds=0.5, at=None, label=None, **kw):
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

    def ev(s, js, at=None, label=None, **kw):
        return s._p({'do': 'eval', 'js': js}, at, label, kw)

    def wait(s, seconds):
        return s.add({'do': 'wait', 'seconds': seconds})

    def waitfor(s, **kw):
        return s.add({'do': 'waitFor', **kw})

    def rolar(s, by, at=None, label=None, ponto=(800, 470), duration=0.5, after=100):
        return s._p({'do': 'scroll', 'point': {'x': ponto[0], 'y': ponto[1]}, 'by': by, 'duration': duration, 'after': after}, at, label, {})

    def registra(s, target, at=None, label=None):
        """registra o retângulo do alvo para a câmera SEM mexer o mouse (passo `type` sem clique e sem texto)"""
        return s._p({'do': 'type', 'target': target, 'text': '', 'noClick': True, 'optional': True, 'timeout': 4}, at, label, {})

    def colar(s, seletor, texto, at=None, label=None):
        """"cola" o texto no campo (foco + insertText, ~0,05 s): o React recebe o input como de um Ctrl+V"""
        js = ("(()=>{const el=document.querySelector(%s);if(!el)return 'SEM ALVO';el.focus();el.select&&el.select();"
              "document.execCommand('insertText',false,%s);return el.value})()") % (json.dumps(seletor), json.dumps(texto))
        return s.ev(js, at=at, label=label)

    def confere(s, escopo, esperados, label, tentativas=20):
        """`eval` que LÊ a tela e compara com o que a fala diz ("OK: ..." ou "DIFERENTE: ..."); escopo 'dlg', 'main', 'body' ou CSS"""
        sel = {'dlg': '[role=dialog]', 'main': 'main', 'body': 'body'}.get(escopo, escopo)
        esp = [esperados] if isinstance(esperados, str) else list(esperados)
        js = ("(async()=>{const norm=t=>t.replace(/[\\s\\u00a0]+/g,' ').toLowerCase();const esp=%s;let out='';"
              "for(let i=0;i<%d;i++){const els=[...document.querySelectorAll(%s)];const el=els[els.length-1];"
              "if(!el){out='DIFERENTE: sem elemento';}else{const t=norm(el.innerText);const falta=esp.filter(e=>!t.includes(norm(e)));"
              "if(!falta.length)return 'OK: '+esp.join(' | ');out='DIFERENTE: faltou '+JSON.stringify(falta)+' em: '+t.slice(0,260);}"
              "await new Promise(r=>setTimeout(r,250));}return out})()") % (json.dumps(esp, ensure_ascii=False), tentativas, json.dumps(sel))
        return s.add({'do': 'eval', 'js': js, 'label': 'confere ' + label})

    def fim(s):
        s.flush(1e9)
        s.steps.append({'do': 'eval', 'js': 'JSON.stringify(window.__avisos || "sem observador")', 'label': 'avisos de erro na tela'})
        s.steps.append({'do': 'mark', 'name': 'FIM', 'at': round(s.dur, 2)})

    def out(s):
        est = ' ESTIMADA' if s.estimado else ''
        quem = 'Sandra Pires (Filial Pindamonhangaba)' if s.n == 3 else 'Rafael Nogueira (matriz)'
        return {
            'name': f'{AULA}-cap{s.n:02d}',
            'title': f'T22 · Cap. {s.n} · {NOMES[s.n]} (narração{est} {str(round(s.dur, 1)).replace(".", ",")} s; marcas L1..L{len(s.linhas)} = início de cada '
                     f'linha do roteiro; FAKE_NOW {FAKE_NOW}; logado como {quem})',
            'seed': f'{AULA}-cap{s.n:02d}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
            'start': {'x': s.start[0], 'y': s.start[1]},
            'anonymous': True, 'storage': storage(s.n, s.storage_extra),
            'seedExtra': list(SEMENTE[s.n]),
            'prewarm': ['/login'], 'setup': s.setup, 'steps': s.steps,
        }


# ---------------------------------------------------------------- alvos
MAIN = 'main'
DLG = '[role=dialog]'
ALERTA = '[role=alertdialog]'
BTN = lambda n, within=None, **kw: {'role': 'button', 'name': n, 'exact': True, **({'within': within} if within else {}), **kw}
BTNX = lambda n, within=None, **kw: {'role': 'button', 'name': n, **({'within': within} if within else {}), **kw}
TXT = lambda t, within=None, **kw: {'text': t, 'exact': True, **({'within': within} if within else {}), **kw}
TXTP = lambda t, within=None, **kw: {'text': t, **({'within': within} if within else {}), **kw}
SEL = lambda s, **kw: {'selector': s, **kw}
OPT = lambda n, **kw: {'role': 'option', 'name': n, **kw}
LINK = lambda n, **kw: {'role': 'link', 'name': n, **kw}
TAB = lambda v: SEL(f'#tab-btn-{v}')                 # abas das telas com SettingsSidebarLayout (Configurações do grupo, Financeiro, Estoque)
AGUARDA = {'do': 'waitFor', 'idle': True}
PERIODO = lambda t: SEL(f'main button[role=combobox]:has-text("{t}")')
MENU_GER = BTNX('Gerencial (Filiais)')
LINK_GER = lambda nome, rota: SEL(f'a[href="{rota}"]')   # itens do grupo "Gerencial (Filiais)" do menu lateral


def login(email='$TUT_USER', espera='Olá, Rafael!'):
    return [{'do': 'waitFor', 'target': {'label': 'E-mail'}, 'timeout': 30},
            {'do': 'type', 'target': {'label': 'E-mail'}, 'text': email, 'cps': 40},
            {'do': 'type', 'target': {'label': 'Senha', 'exact': True}, 'text': '$TUT_SENHA', 'cps': 40},
            {'do': 'click', 'target': BTN('Entrar')},
            {'do': 'waitFor', 'text': espera, 'timeout': 30}, AGUARDA]


def vai(url, espera, timeout=25):
    return [{'do': 'goto', 'url': url}, {'do': 'waitFor', 'text': espera, 'timeout': timeout}, AGUARDA]


# ---------------------------------------------------------------- rolagem roteirizada (eval: o cursor não se mexe)
ACHA_ROLAGEM = ("const rolagem=(el)=>{let c=el&&el.parentElement;while(c&&c!==document.body){const s=getComputedStyle(c);"
                "if(/(auto|scroll)/.test(s.overflowY)&&c.scrollHeight>c.clientHeight+4)return c;c=c.parentElement;}"
                "return [...document.querySelectorAll('main')].find(e=>/(auto|scroll)/.test(getComputedStyle(e).overflowY)&&e.scrollHeight>e.clientHeight+4)||document.scrollingElement};")
SUAVE = ("await new Promise(res=>{const t0=performance.now();const f=t=>{const p=Math.min(1,(t-t0)/DUR),e=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;"
         "c.scrollTop=DESTINO;p<1?requestAnimationFrame(f):res()};requestAnimationFrame(f)});")
FOLHA = "[...document.querySelectorAll('%s *')].find(e=>e.children.length===0&&e.textContent.trim()===%s&&e.getClientRects().length)"


def js_rola_texto(texto, y=300, dur_ms=800, escopo='main'):
    """rolagem suave do contêiner que rola a folha do DOM cujo texto é `texto` até ela ficar em y px CSS; devolve o topo final"""
    achar = FOLHA % (escopo, json.dumps(texto))
    return ("(async()=>{" + ACHA_ROLAGEM + "const el=" + achar + ";if(!el)return 'SEM ALVO';const c=rolagem(el);if(!c)return 'SEM ROLAGEM';"
            f"const dy=Math.round(el.getBoundingClientRect().top-{int(y)});if(Math.abs(dy)<3)return 'ok';const y0=c.scrollTop;"
            + (SUAVE.replace('DUR', str(int(dur_ms))).replace('DESTINO', 'y0+dy*e') if dur_ms else "c.scrollTop=y0+dy;")
            + "return Math.round(el.getBoundingClientRect().top)})()")


def js_topo(dur_ms=600):
    """sobe a página até o topo"""
    return ("(async()=>{" + ACHA_ROLAGEM + "const el=document.querySelector('main h1')||document.querySelector('main *');const c=rolagem(el);if(!c)return 'SEM ROLAGEM';"
            "const y0=c.scrollTop;if(y0<3)return 'ok';const dy=-y0;"
            + (SUAVE.replace('DUR', str(int(dur_ms))).replace('DESTINO', 'y0+dy*e') if dur_ms else "c.scrollTop=0;") + "return 'topo'})()")


def rola_setup(texto, y=300):
    return {'do': 'eval', 'js': js_rola_texto(texto, y, 0)}


def js_clica_texto(texto, escopo='main', tag='button'):
    """clique por eval (sem cursor) no `tag` cujo texto visível é `texto`"""
    return ("(()=>{const b=[...document.querySelectorAll(%s)].find(e=>e.offsetParent&&e.innerText.trim()===%s);if(!b)return 'SEM ALVO';b.click();return 'ok'})()"
            % (json.dumps(f'{escopo} {tag}'), json.dumps(texto)))


ANIMA = "(()=>{const a=document.getAnimations().filter(x=>x.currentTime<0);a.forEach(x=>x.startTime=document.timeline.currentTime);return a.length})()"


# ---------------------------------------------------------------- alvos próprios do T22
CONFIG_RODAPE = SEL("button[aria-label='Configurações']")          # rodapé do menu lateral (fora da faixa de clique: noScroll)
COPIAR = SEL('main button:has(svg.lucide-copy)')                   # copiar o código de convite
REGERAR = SEL("main button[title='Gerar novo código (válido por 30 dias)']")
CODIGO_DIV = SEL(f'main div.font-mono:has-text("{CODIGO}")')
SWITCH_ROTULO = lambda rotulo: SEL(f'main div.flex:has(> div > label:text-is("{rotulo}")) > button[role=switch]')
SWITCH_TEXTO = lambda texto: SEL(f'main div.flex:has(> div > div > p:text-is("{texto}")) > button[role=switch], main div:has(> div > div > p:text-is("{texto}")) > button[role=switch]')
LINHA = lambda texto: SEL(f'main tbody tr:has-text("{texto}")')
CELULA = lambda texto, n: SEL(f'main tbody tr:has-text("{texto}") td:nth-child({n})')
KPI = lambda rotulo: SEL(f'main div.rounded-lg:has(> div > div > span:text-is("{rotulo}"))')
DRE_LINHA = lambda rotulo: SEL(f'main div.flex:has(> span:text-is("{rotulo}"))')
LIXEIRA_FILIAL = SEL('main div.rounded-lg:has(p:text-is("Filial Pindamonhangaba")) button.text-destructive')
ENVIAR_ATIVOS = SEL('main div.rounded-lg:has(p:text-is("Filial Pindamonhangaba")) button:has-text("Enviar Ativos")')
COMBO = lambda txt, esc='main': SEL(f'{esc} button[role=combobox]:has-text("{txt}")')
CAMPO_QTD = SEL('main input[type=number]')
JS_SAIR = "(()=>{const a=document.activeElement;a&&a.blur&&a.blur();return 1})()"


def setup_dash(extra=()):
    """login e, fora do vídeo, as telas do Gerencial (carrega os módulos); termina no Dashboard do EcoSistema"""
    return login() + vai('/gerencial', 'Gerencial') + list(extra)


def abre_menu_ger():
    """abre o grupo "Gerencial (Filiais)" do menu lateral (fora do vídeo), se ainda não estiver aberto"""
    return [{'do': 'click', 'target': MENU_GER, 'unless': SEL('a[href="/gerencial/configuracoes"]')},
            {'do': 'waitFor', 'target': SEL('a[href="/gerencial/configuracoes"]'), 'timeout': 8}]


def cap00():
    """Abertura: Dashboard do EcoSistema da matriz; o cursor abre o grupo "Gerencial (Filiais)" do menu (ilustração na L2)."""
    c = Cap(0, login() + vai('/gerencial', 'Configurar Grupo') + vai('/dashboard', 'Olá, Rafael!'), pace=0.6, start=(760, 420))
    c.mark(1)
    c.hover(MENU_GER, 0.6, at=c.A(1, 'matriz', 0.6), label='menu Gerencial (Filiais)')
    c.click(MENU_GER, at=c.A(1, 'enxergar', 0.5), label='abre o grupo Gerencial (Filiais)', unless=SEL('a[href="/gerencial/configuracoes"]'))
    c.waitfor(target=SEL('a[href="/gerencial/configuracoes"]'), timeout=8)
    c.hover(LINK_GER('Dashboard', '/gerencial'), 0.3, at=c.A(1, 'filial', 0.5), label='Dashboard')
    c.hover(LINK_GER('Financeiro', '/gerencial/financeiro'), 0.2, label='Financeiro')
    c.hover(LINK_GER('Estoque', '/gerencial/estoque'), 0.2, label='Estoque')
    c.hover(LINK_GER('Assinaturas', '/gerencial/assinaturas'), 0.2, label='Assinaturas')
    c.hover(LINK_GER('Configurações', '/gerencial/configuracoes'), 0.6, label='Configurações')
    c.mark(2)
    c.mark(3)
    c.hover(MENU_GER, 1.2, at=c.A(3, 'Gerencial.', 0.5), label='Gerencial (Filiais) (cartão Módulo Gerencial)')
    c.mark(4)
    c.fim()
    return c


def cap01():
    """Como o Gerencial funciona: "Dashboard" do grupo Gerencial mostra "Módulo Gerencial" (sem grupo); ilustrações nas L2 a L4."""
    c = Cap(1, login() + vai('/gerencial', 'Configurar Grupo') + vai('/dashboard', 'Olá, Rafael!') + abre_menu_ger(), pace=0.5, start=(720, 300))
    c.mark(1)
    c.click(LINK_GER('Dashboard', '/gerencial'), at=0.1, label='Dashboard do Gerencial (menu)')
    c.waitfor(text='Módulo Gerencial', timeout=15)
    c.hover(TXT('Módulo Gerencial', within=MAIN), 0.6, at=c.A(1, 'começa', 0.5), label='Módulo Gerencial (sem grupo)')
    c.hover(BTNX('Configurar Grupo'), 1.0, at=c.A(1, 'criar', 0.5), label='Configurar Grupo')
    c.mark(2)
    c.mark(3)
    c.mark(4)
    c.fim()
    return c


def cap02():
    """Criar o grupo e o código: Configurar Grupo, "Grupo Recicla Vale", Criar Grupo; abas, passo a passo, código de convite e validade,
    copiar, Unidades Ativas só com a matriz. Vira apos-cap02."""
    c = Cap(2, login() + vai('/gerencial/configuracoes', 'Criar Grupo Gerencial') + vai('/gerencial', 'Configurar Grupo'), pace=0.5, start=(700, 300))
    c.mark(1)
    c.click(BTNX('Configurar Grupo'), at=c.A(1, 'Configurar', 0.7), label='Configurar Grupo')
    c.waitfor(text='Criar Grupo Gerencial', timeout=15)
    c.mark(2)
    c.click({'placeholder': 'Ex: Grupo Reciclagem Silva'}, at=c.A(2, 'nome,', 0.6), label='campo Nome do Grupo')
    c.type({'placeholder': 'Ex: Grupo Reciclagem Silva'}, 'Grupo Recicla Vale', at=c.A(2, 'Grupo', 0.05), noClick=True, label='Nome do Grupo: Grupo Recicla Vale')
    c.click(BTN('Criar Grupo'), at=c.A(2, 'Criar', 0.6), label='Criar Grupo')
    c.waitfor(text='Código de Convite', timeout=15)
    c.ev(ANIMA)
    c.mark(3)
    c.hover(TAB('unidades'), 0.3, at=c.A(3, 'abas', 0.5), label='abas do grupo')
    c.hover(TAB('transferencias'), 0.3, label='abas do grupo (até Transferências)')
    c.hover(TXTP('Configure o grupo', within=MAIN), 1.0, at=c.A(3, 'passo', 0.5), label='passo a passo Configure o grupo')
    c.mark(4)
    c.hover(CODIGO_DIV, 1.0, at=c.A(4, 'código', 0.5), label='código de convite (ZOOM: código e validade)')
    c.hover(TXTP('Válido até', within=MAIN), 1.0, at=c.A(4, 'trinta', 0.5), label='Válido até 10/12/2026')
    c.hover(REGERAR, 1.0, at=c.A(4, 'botão', 0.5), label='botão Gerar novo código')
    c.mark(5)
    c.click(COPIAR, at=c.A(5, 'Copio', 0.6), label='copiar o código')
    c.waitfor(text='Código copiado!', timeout=6)
    c.registra(TXT('Código copiado!'), label='aviso Código copiado!')
    c.mark(6)
    c.ev(js_rola_texto('Nenhuma filial vinculada ainda. Compartilhe o código de convite acima.', 420, 700), at=c.L(6) - 0.9, label='desce até Unidades Ativas')
    c.hover(TXTP('Nenhuma filial vinculada ainda', within=MAIN), 1.2, at=c.A(6, 'unidades', 0.5), label='Unidades Ativas: só a matriz (ZOOM)')
    c.fim()
    return c


def cap03():
    """Do lado da filial (Sandra Pires): Configurações (rodapé do menu) › Empresa › cartão Filial; liga É Filial, cola o código e Vincular.
    Vira apos-cap03."""
    c = Cap(3, login(SANDRA_EMAIL, 'Olá, Sandra!') + vai('/configuracoes', 'Configurações do Sistema') + vai('/dashboard', 'Olá, Sandra!'),
            pace=0.5, start=(700, 300))
    c.mark(1)
    c.hover(CONFIG_RODAPE, 0.8, at=c.A(1, 'sistema', 0.6), label='Configurações (rodapé do menu)', noScroll=True)
    c.click(CONFIG_RODAPE, at=c.A(1, 'Configurações,', 0.6), label='Configurações (rodapé do menu)', noScroll=True)
    c.waitfor(text='Configurações do Sistema', timeout=15)
    c.hover(TAB('company'), 0.8, at=c.A(1, 'Empresa.', 0.5), label='aba Empresa')
    c.mark(2)
    c.ev(js_rola_texto('Se esta empresa é uma filial, vincule-a à empresa-mãe usando o código de convite', 260, 900), at=c.L(2) - 0.9,
         label='desce até o cartão Filial')
    c.ev(ANIMA)
    c.hover(TXT('Filial', within=MAIN), 0.5, at=c.A(2, 'Filial.', 0.5), label='cartão Filial')
    c.click(SWITCH_ROTULO('É Filial'), at=c.A(2, 'liga', 0.6), label='liga É Filial')
    c.waitfor(target={'placeholder': 'GRP-XXXXXX'}, timeout=6)
    c.mark(3)
    c.click({'placeholder': 'GRP-XXXXXX'}, at=c.A(3, 'cola', 0.6), label='campo do código')
    c.colar('main input[placeholder="GRP-XXXXXX"]', CODIGO, at=c.A(3, 'código', 0.1), label='cola o código GRP-7C4E9A (ZOOM: o campo)')
    c.mark(4)
    c.click(BTNX('Vincular'), at=c.A(4, 'Vincular.', 0.6), label='Vincular')
    c.waitfor(text='Vinculada ao grupo', timeout=10)
    c.hover(TXT('Vinculada ao grupo', within=MAIN), 1.0, at=c.A(4, 'Grupo', 0.5), label='Vinculada ao grupo · Grupo Recicla Vale · Ativa')
    c.mark(5)
    c.fim()
    return c


def setup_ger(url='/gerencial', espera='Dashboard Gerencial', extra=()):
    return login() + vai(url, espera) + list(extra)


def cap04():
    """O Dashboard Gerencial: do menu, Dashboard; Mês passado; Todas as Unidades; cartões Receita Total e Despesa Total; setinha; Estoque
    Total; o gráfico por unidade com a estrela da matriz."""
    c = Cap(4, setup_ger(extra=vai('/dashboard', 'Olá, Rafael!') + abre_menu_ger()), pace=0.5, start=(700, 300))
    c.mark(1)
    c.click(LINK_GER('Dashboard', '/gerencial'), at=c.A(1, 'Dashboard', 0.7), label='Dashboard do Gerencial (menu)')
    c.waitfor(text='Receita Total', timeout=15)
    c.ev(ANIMA)
    c.hover(TXTP('unidades', within=MAIN), 1.0, at=c.A(1, 'duas', 0.5), label='Grupo Recicla Vale • 2 unidades')
    c.mark(2)
    c.click(PERIODO('Este mês'), at=c.A(2, 'outubro', 0.6), label='período')
    c.click(OPT('Mês passado'), at=c.A(2, 'Mês', 0.3), label='Mês passado')
    c.waitfor(text='R$ 344.040,00', timeout=10)
    c.ev(ANIMA)
    c.hover(TXTP('Todas as Unidades', within=MAIN), 1.0, at=c.A(2, 'todas', 0.5), label='Todas as Unidades')
    c.mark(3)
    c.hover(KPI('Receita Total'), 1.0, at=c.A(3, 'cartões', 0.5), label='cartões Receita Total e Despesa Total (ZOOM)')
    c.hover(KPI('Receita Total'), 0.8, at=c.A(3, 'receita', 0.5), label='Receita Total R$ 344.040,00')
    c.hover(KPI('Despesa Total'), 1.0, at=c.A(3, 'despesa,', 0.5), label='Despesa Total R$ 370.690,00')
    c.confere('main', ['R$ 344.040,00', 'R$ 370.690,00'], 'receita e despesa do grupo em outubro')
    c.mark(4)
    c.hover(SEL('main div.rounded-lg:has(span:text-is("Receita Total")) span.inline-flex'), 0.8, at=c.A(4, 'setinha', 0.5), label='setinha da Receita Total')
    c.hover(KPI('Estoque Total'), 1.0, at=c.A(4, 'Estoque', 0.5), label='Estoque Total')
    c.mark(5)
    c.ev(js_rola_texto('Receita vs Despesa por Unidade', 150, 800), at=c.L(5) - 0.9, label='desce até o gráfico por unidade')
    c.hover(SEL('main div.space-y-3:has(h2:has-text("Receita vs Despesa por Unidade")) .recharts-surface'), 1.0, at=c.A(5, 'unidade', 0.5),
            label='gráfico Receita vs Despesa por Unidade')
    c.hover(SEL('main .recharts-xAxis text:has-text("★")'), 1.0, at=c.A(5, 'estrela', 0.5), label='a estrela da matriz')
    c.fim()
    return c


def cap05():
    """Ranking e resumo por unidade: Ranking por Lucro (filial na frente, matriz negativa); Resumo por Unidade, linha da matriz e da filial."""
    c = Cap(5, setup_ger(extra=[{'do': 'click', 'target': PERIODO('Este mês')}, {'do': 'click', 'target': OPT('Mês passado')},
                                {'do': 'waitFor', 'text': 'R$ 344.040,00', 'timeout': 10}, AGUARDA, rola_setup('Ranking por Lucro', 140)]),
            pace=0.5, start=(900, 300))
    c.mark(1)
    c.hover(TXTP('Ranking por Lucro', within=MAIN), 0.8, at=c.A(1, 'ranking', 0.5), label='Ranking por Lucro')
    c.hover(SEL('main .recharts-yAxis text:has-text("Filial")'), 0.8, at=c.A(1, 'filial', 0.5), label='a filial na frente')
    c.hover(SEL('main .recharts-yAxis text:has-text("Recicla")'), 0.8, at=c.A(1, 'matriz,', 0.5), label='a matriz no vermelho')
    c.mark(2)
    c.ev(js_rola_texto('Resumo por Unidade', 260, 800), at=c.A(2, 'Embaixo', 0.6), label='desce até Resumo por Unidade')
    c.hover(TXTP('Resumo por Unidade', within=MAIN), 0.6, at=c.A(2, 'resumo', 0.4), label='Resumo por Unidade')
    c.mark(3)
    c.hover(LINHA('Recicla Vale Metais'), 1.0, at=c.A(3, 'matriz', 0.5), label='linha da matriz (ZOOM)')
    c.confere('main tbody', ['R$ 272.040,00', 'R$ 299.690,00', '-R$ 27.650,00', '-10.2%'], 'linha da matriz')
    c.hover(CELULA('Recicla Vale Metais', 4), 1.0, at=c.A(3, 'negativa', 0.5), label='lucro da matriz -R$ 27.650,00')
    c.mark(4)
    c.hover(LINHA('Filial Pindamonhangaba'), 1.0, at=c.A(4, 'filial', 0.5), label='linha da filial (ZOOM)')
    c.confere('main tbody', ['R$ 72.000,00', 'R$ 71.000,00', 'R$ 1.000,00', '1.4%'], 'linha da filial')
    c.mark(5)
    c.fim()
    return c


def setup_fin(aba='dashboard', periodo=True):
    s = login() + vai('/gerencial/estoque', 'Estoque Gerencial') + vai('/gerencial', 'Dashboard Gerencial')
    if periodo:
        s += vai('/gerencial/financeiro', 'Financeiro Gerencial') + [{'do': 'click', 'target': PERIODO('Este mês')}, {'do': 'click', 'target': OPT('Mês passado')},
                                                                     {'do': 'waitFor', 'text': 'CMV (Custo da Mercadoria Vendida)', 'timeout': 15}, AGUARDA]
    return s


def cap06():
    """A DRE do grupo: Financeiro › DRE › Mês passado (Consolidado); Regime de Caixa: vendas, compras, resultado de caixa; impostos, despesas,
    outras receitas e o resultado do período; Comparativo e a linha Resultado por unidade."""
    c = Cap(6, setup_ger(url='/gerencial/financeiro', espera='Financeiro Gerencial', extra=vai('/gerencial', 'Dashboard Gerencial')),
            pace=0.5, start=(700, 300), storage_extra={'gerencial-financeiro-tab': 'dashboard'})
    c.mark(1)
    c.click(LINK_GER('Financeiro', '/gerencial/financeiro'), at=0.1, label='Financeiro do Gerencial (menu)')
    c.waitfor(text='Financeiro Gerencial', timeout=15)
    c.click(TAB('dre'), at=c.A(1, 'DRE,', 0.7), label='aba DRE')
    c.click(PERIODO('Este mês'), at=c.A(1, 'outubro', 0.6), label='período')
    c.click(OPT('Mês passado'), at=c.A(1, 'escolhido,', 0.3), label='Mês passado')
    c.waitfor(text='CMV (Custo da Mercadoria Vendida)', timeout=15)
    c.hover(BTNX('Consolidado'), 0.6, at=c.A(1, 'grupo', 0.5), label='Consolidado: a DRE do grupo')
    c.mark(2)
    c.click({'role': 'tab', 'name': 'Regime de Caixa'}, at=c.A(2, 'caixa,', 0.6), label='Regime de Caixa')
    c.waitfor(text='Compras de Material', timeout=10)
    c.hover(DRE_LINHA('Vendas de Material'), 1.0, at=c.A(2, 'vendeu', 0.6), label='vendas, compras e resultado de caixa (ZOOM)')
    c.hover(DRE_LINHA('Compras de Material'), 1.0, at=c.A(2, 'comprou', 0.5), label='Compras de Material')
    c.confere('main', ['R$ 341.240,00', 'R$ 318.860,00', 'R$ 19.980,00'], 'vendas, compras e resultado de caixa')
    c.mark(3)
    c.ev(js_rola_texto('(-) Impostos e Deduções', 200, 800), at=c.L(3) - 0.9, label='desce até impostos e resultado')
    c.hover(DRE_LINHA('(-) Impostos e Deduções'), 0.8, at=c.A(3, 'impostos', 0.5), label='impostos, despesas, outras receitas e resultado (ZOOM)')
    c.hover(DRE_LINHA('Total Despesas'), 0.8, at=c.A(3, 'despesas', 0.5), label='Total Despesas')
    c.hover(DRE_LINHA('(+) Outras Receitas'), 0.8, at=c.A(3, 'aluguel', 0.5), label='Outras Receitas (aluguel de caçamba)')
    c.hover(DRE_LINHA('(=) Resultado do Período'), 1.2, at=c.A(3, 'vermelho:', 0.5), label='Resultado do Período')
    c.confere('main', ['R$ 3.574,10', 'R$ 45.855,90', 'R$ 2.800,00', 'R$ 26.650,00', 'Déficit'], 'impostos, despesas, outras receitas e resultado')
    c.mark(4)
    c.ev(js_topo(700), at=c.L(4) - 0.9, label='sobe para o alto da DRE')
    c.click(BTNX('Comparativo'), at=c.A(4, 'Comparativo', 0.6), label='Comparativo')
    c.waitfor(text='DRE Comparativo por Unidade', timeout=10)
    c.mark(5)
    c.hover(LINHA('Resultado'), 1.0, at=c.A(5, 'vermelho', 0.5), label='linha Resultado (ZOOM)')
    c.hover(SEL('main tbody tr:has-text("Resultado") td:nth-child(2)'), 1.0, at=c.A(5, 'matriz,', 0.5), label='Resultado da matriz')
    c.hover(SEL('main tbody tr:has-text("Resultado") td:nth-child(3)'), 1.0, at=c.A(5, 'filial.', 0.5), label='Resultado da filial')
    c.confere('main tbody', ['R$ 27.650,00', 'R$ 1.000,00'], 'Resultado da matriz e da filial')
    c.fim()
    return c


def cap07():
    """Caixa e competência: a DRE do grupo em Regime de Competência (CMV, Lucro Bruto, resultado); depois Caixa e Competência de novo, com a
    câmera no resultado."""
    c = Cap(7, setup_fin(), pace=0.5, start=(700, 300), storage_extra={'gerencial-financeiro-tab': 'dre'})
    c.mark(1)
    c.hover(DRE_LINHA('CMV (Custo da Mercadoria Vendida)'), 1.0, at=c.A(1, 'CMV,', 0.5), label='CMV e Lucro Bruto (ZOOM)')
    c.hover(DRE_LINHA('CMV (Custo da Mercadoria Vendida)'), 1.0, at=c.A(1, 'vendido:', 0.5), label='CMV (Custo da Mercadoria Vendida)')
    c.hover(DRE_LINHA('(=) Lucro Bruto'), 1.0, at=c.A(1, 'oitocentos', 0.5), label='Lucro Bruto')
    c.mark(2)
    c.ev(js_rola_texto('(=) Resultado do Período', 420, 800), at=c.L(2) - 0.9, label='desce até o resultado')
    c.hover(DRE_LINHA('(=) Resultado do Período'), 1.2, at=c.A(2, 'resultado', 0.5), label='Resultado do Período (ZOOM)')
    c.mark(3)
    c.mark(4)
    c.hover(DRE_LINHA('(=) Resultado do Período'), 0.4, at=c.L(4) - 0.6, label='o resultado (a câmera fica nele)')
    c.ev(js_clica_texto('Regime de Caixa'), at=c.A(4, 'caixa', 0.1), label='Regime de Caixa (o resultado vai para -R$ 26.650,00)')
    c.ev(js_clica_texto('Regime de Competência'), at=c.A(4, 'competência', 0.1), label='Regime de Competência (volta ao resultado positivo)')
    c.mark(5)
    c.fim()
    return c


def cap08():
    """O estoque do grupo: Estoque Gerencial › Visão Geral (as duas unidades, a Tabela Unificada e a linha do alumínio latinha); Posição de
    Estoque; Histórico de Materiais; Relatório de Estoque."""
    c = Cap(8, setup_ger(url='/gerencial/estoque', espera='Estoque Gerencial', extra=vai('/gerencial', 'Dashboard Gerencial')),
            pace=0.5, start=(700, 300), storage_extra={'gerencial-estoque-tab': 'visao-geral'})
    c.mark(1)
    c.click(LINK_GER('Estoque', '/gerencial/estoque'), at=c.A(1, 'estoque.', 0.7), label='Estoque do Gerencial (menu)')
    c.waitfor(text='Tabela Unificada de Materiais', timeout=15)
    c.ev(ANIMA)
    c.hover(TAB('visao-geral'), 0.6, at=c.A(1, 'Visão', 0.5), label='Visão Geral')
    c.mark(2)
    c.ev(js_rola_texto('Tabela Unificada de Materiais', 120, 800), at=c.L(2) - 0.9, label='desce até a Tabela Unificada de Materiais')
    c.hover(TXTP('Tabela Unificada de Materiais', within=MAIN), 0.6, at=c.A(2, 'tabela,', 0.4), label='Tabela Unificada de Materiais')
    c.hover(LINHA('Alumínio latinha'), 1.0, at=c.A(2, 'alumínio', 0.5), label='linha do alumínio latinha (ZOOM)')
    c.confere('main tbody', ['640', '1.850', '2.490'], 'latinha 640, 1.850 e 2.490 kg')
    c.mark(3)
    c.ev(js_topo(600), at=c.L(3) - 0.9, label='sobe até as abas')
    c.click(TAB('posicao'), at=c.A(3, 'Posição', 0.6), label='Posição de Estoque')
    c.hover(TXT('Custo médio', within=MAIN), 0.6, at=c.A(3, 'custo', 0.5), label='Custo médio')
    c.hover(TXT('Valor em estoque', within=MAIN), 0.6, at=c.A(3, 'valor.', 0.5), label='Valor em estoque')
    c.mark(4)
    c.click(TAB('historico'), at=c.A(4, 'Histórico', 0.6), label='Histórico de Materiais')
    c.hover(TXT('Filial', within='main thead'), 0.8, at=c.A(4, 'unidade', 0.5), label='coluna Filial')
    c.mark(5)
    c.click(TAB('relatorio'), at=c.A(5, 'Relatório', 0.6), label='Relatório de Estoque')
    c.hover(TXT('Lucro', within='main thead'), 0.6, at=c.A(5, 'lucro', 0.5), label='coluna Lucro')
    c.hover(TXT('Margem', within='main thead'), 0.8, at=c.A(5, 'margem.', 0.5), label='coluna Margem')
    c.fim()
    return c


def cap09():
    """Enviar Ativos: Configurações do grupo › Catálogo (Importar do Estoque da Matriz), Tabelas de Preço (entram sozinhas), Clientes e
    Fornecedores (marca a Fundição Bandeira do Vale), Categorias Financeiras; Unidades › Enviar Ativos › Confirmar Envio; a lixeira da
    filial (sem clicar). Vira apos-cap09."""
    c = Cap(9, setup_ger(url='/gerencial/configuracoes', espera='Código de Convite', extra=vai('/gerencial', 'Dashboard Gerencial')),
            pace=0.5, start=(700, 300))
    c.mark(1)
    c.click(LINK_GER('Configurações', '/gerencial/configuracoes'), at=c.A(1, 'padronização.', 0.7), label='Configurações do Gerencial (menu)')
    c.waitfor(text='Código de Convite', timeout=15)
    c.click(TAB('materiais'), at=c.A(1, 'catálogo', 0.6), label='Catálogo de Materiais')
    c.waitfor(text='Importar do Estoque da Matriz', timeout=10)
    c.mark(2)
    c.click(BTNX('Importar do Estoque da Matriz'), at=c.A(2, 'Importar', 0.6), label='Importar do Estoque da Matriz')
    c.waitfor(text='importado(s) do estoque', timeout=10)
    c.hover(TXT('Alumínio latinha', within=MAIN), 0.8, at=c.A(2, 'materiais', 0.5), label='os materiais da matriz no catálogo')
    c.mark(3)
    c.click(TAB('precos'), at=c.A(3, 'tabelas', 0.6), label='Tabelas de Preço')
    c.hover(TXTP('Tabelas de Preço do Grupo', within=MAIN), 1.0, at=c.A(3, 'sozinhas,', 0.5), label='as tabelas da matriz entram sozinhas')
    c.mark(4)
    c.click(TAB('clientes'), at=c.A(4, 'Clientes', 0.6), label='Clientes e Fornecedores')
    c.hover(TXT('Fundição Bandeira do Vale', within=MAIN), 0.8, at=c.A(4, 'Fundição', 0.5), label='Fundição Bandeira do Vale')
    c.click(TXT('Fundição Bandeira do Vale', within=MAIN), at=c.A(4, 'marco.', 0.6), label='marca a Fundição Bandeira do Vale')
    c.waitfor(text='Disponibilizado para filiais', timeout=8)
    c.mark(5)
    c.click(TAB('categorias'), at=c.A(5, 'categorias', 0.6), label='Categorias Financeiras')
    c.mark(6)
    c.click(TAB('unidades'), at=c.A(6, 'Unidades,', 0.6), label='Unidades')
    c.ev(js_rola_texto('Filial Pindamonhangaba', 360, 700), at=c.A(6, 'Enviar', 1.6), label='desce até a filial')
    c.click(ENVIAR_ATIVOS, at=c.A(6, 'Enviar', 0.6), label='Enviar Ativos')
    c.waitfor(text='Confirmar Envio', timeout=8)
    c.hover(TXT('Materiais', within=DLG), 0.6, at=c.A(6, 'tinha', 0.5), label='Materiais, Categorias, Tabelas, Clientes, Fornecedores')
    c.hover(TXT('Sobrescrever preços existentes', within=DLG), 1.2, at=c.A(6, 'Sobrescrever', 0.5), label='Sobrescrever preços existentes (desligado)')
    c.mark(7)
    c.click(BTN('Confirmar Envio'), at=c.A(7, 'Confirmar', 0.6), label='Confirmar Envio')
    c.waitfor(text='novo(s)', timeout=10)
    c.hover(TXT('Materiais', within=DLG), 1.0, at=c.A(7, 'mesmo', 0.5), label='n novo(s) por linha')
    c.click(BTN('Fechar', within=DLG), at=c.A(7, 'nome.', 0.6), label='Fechar')
    c.mark(8)
    c.hover(LIXEIRA_FILIAL, 1.5, at=c.A(8, 'tirar', 0.5), label='lixeira da linha da filial (ZOOM, sem clicar)')
    c.fim()
    return c


def cap10():
    """Transferência com aprovação: aba Transferências, liga "Exigir aprovação"; Nova: filial -> matriz, alumínio latinha 1.200 kg,
    observação; Solicitar; Pendente; Executar; Confirmar e Executar; o Estoque Gerencial com 1.840 e 650 kg. Vira apos-cap10."""
    c = Cap(10, setup_ger(url='/gerencial/estoque', espera='Estoque Gerencial',
                          extra=vai('/gerencial/configuracoes', 'Código de Convite')), pace=0.5, start=(700, 300),
            storage_extra={'gerencial-estoque-tab': 'visao-geral'})
    c.mark(1)
    c.click(TAB('transferencias'), at=c.A(1, 'transferências.', 0.6), label='aba Transferências')
    c.waitfor(text='Exigir aprovação em transferências', timeout=8)
    c.click(SWITCH_TEXTO('Exigir aprovação em transferências'), at=c.A(1, 'ligo', 0.6), label='liga Exigir aprovação em transferências')
    c.mark(2)
    c.click(BTNX('Nova'), at=c.A(2, 'Nova,', 0.6), label='Nova')
    c.waitfor(text='Unidade de origem...', timeout=8)
    c.click(COMBO('Unidade de origem...'), at=c.A(2, 'origem', 0.6), label='Origem')
    c.click(OPT('Filial Pindamonhangaba'), at=c.A(2, 'filial', 0.3), label='Origem: Filial Pindamonhangaba')
    c.click(COMBO('Unidade de destino...'), at=c.A(2, 'destino,', 0.6), label='Destino')
    c.click(OPT('Recicla Vale Metais'), at=c.A(2, 'matriz.', 0.3), label='Destino: Recicla Vale Metais')
    c.mark(3)
    c.type({'placeholder': 'Buscar material...'}, 'latinha', at=c.A(3, 'material', 0.6), label='busca latinha')
    c.click(SEL('main label:has-text("Alumínio latinha") button[role=checkbox]'), at=c.A(3, 'alumínio', 0.6), label='marca Alumínio latinha')
    c.click(CAMPO_QTD, at=c.A(3, 'mil', 0.6), label='campo Quantidade')
    c.type(CAMPO_QTD, '1200', at=c.A(3, 'duzentos', 0.05), noClick=True, label='Quantidade 1200 (ZOOM)')
    c.mark(4)
    c.click({'placeholder': 'Ex: Transferência para suprir demanda...'}, at=c.L(4) - 0.2, label='Observações')
    c.colar('main textarea', 'Lote para a Serra Fina Alumínio Reciclagem', label='Observações: Lote para a Serra Fina Alumínio Reciclagem')
    c.hover(TXTP('Este grupo exige aprovação', within=MAIN), 1.2, at=c.A(4, 'aviso', 0.5), label='aviso do resumo')
    c.click(BTNX('Solicitar 1 transferência'), at=c.A(4, 'Solicitar', 0.6), label='Solicitar 1 transferência')
    c.waitfor(text='Pendente', timeout=10)
    c.mark(5)
    c.hover(TXT('Pendente', within=MAIN), 1.0, at=c.A(5, 'pendente.', 0.5), label='Pendente')
    c.click(BTNX('Executar'), at=c.A(5, 'Executar.', 0.6), label='Executar')
    c.waitfor(text='Confirmar execução?', timeout=8)
    c.hover(TXTP('Este grupo exige aprovação antes de executar', within=ALERTA), 1.2, at=c.A(5, 'confirmar', 0.5), label='Confirmar execução? (destino de acordo)')
    c.mark(6)
    c.click(BTN('Confirmar e Executar'), at=c.A(6, 'Confirmar', 0.6), label='Confirmar e Executar')
    c.waitfor(text='Concluída', timeout=10)
    c.hover(TXT('Concluída', within=MAIN), 0.6, at=c.A(6, 'Pronto:', 0.5), label='Concluída')
    c.click(LINK_GER('Estoque', '/gerencial/estoque'), at=c.A(6, 'matriz', 0.6), label='Estoque do Gerencial (menu)')
    c.waitfor(text='Tabela Unificada de Materiais', timeout=12)
    c.ev(js_rola_texto('Tabela Unificada de Materiais', 120, 700), label='desce até a tabela')
    c.hover(LINHA('Alumínio latinha'), 1.0, at=c.A(6, 'quarenta', 0.5), label='latinha: 1.840 na matriz e 650 na filial (ZOOM)')
    c.confere('main tbody', ['1.840', '650', '2.490'], 'latinha 1.840, 650 e 2.490 kg')
    c.mark(7)
    c.fim()
    return c


# o "pagamento" do Pix do grupo é um passo de bastidor: o checkout pergunta a cada 5 s (check-asaas-payment); o setup anota o instante de
# cada pergunta e este eval espera a próxima e marca a cobrança como recebida ~0,4 s antes dela, por REST no Supabase falso (endereço do build;
# o robô desvia para a instância da aula). Devolve o status do PATCH.
BAKED = 'http://127.0.0.1:54340'
JS_ESCUTA_POLL = ("(()=>{if(window.__polls)return 'ja';window.__polls=[];const f=window.fetch;window.fetch=function(u,o){try{const s=String(u&&u.url||u);"
                  "if(s.includes('check-asaas-payment'))window.__polls.push(performance.now())}catch(e){}return f.apply(this,arguments)};return 'ok'})()")
JS_PAGA = ("(async()=>{const p=window.__polls||[];const ult=p.length?p[p.length-1]:performance.now();let alvo=ult+5000-450;"
           "while(alvo<performance.now()+150)alvo+=5000;await new Promise(r=>setTimeout(r,Math.max(0,alvo-performance.now())));"
           "const r=await fetch(%s,{method:'PATCH',headers:{'content-type':'application/json',Prefer:'return=minimal'},body:JSON.stringify({status:'RECEIVED'})});"
           "return r.status})()") % json.dumps(BAKED + '/rest/v1/subscription_payments?status=eq.PENDING')


def cap11():
    """Assinaturas numa fatura só: Assinaturas do grupo; Pagar tudo de uma vez; o aviso das cobranças; PIX (QR fictício); o pagamento
    confirmado por um passo de bastidor. Vira apos-cap11."""
    c = Cap(11, setup_ger(url='/gerencial/assinaturas', espera='Assinaturas do grupo',
                          extra=vai(f'/checkout?mode=group&group={GRUPO}', 'Forma de pagamento') + vai('/gerencial', 'Dashboard Gerencial')
                          + [{'do': 'eval', 'js': JS_ESCUTA_POLL}]), pace=0.5, start=(700, 300))
    c.mark(1)
    c.click(LINK_GER('Assinaturas', '/gerencial/assinaturas'), at=c.A(1, 'assinaturas.', 0.7), label='Assinaturas do Gerencial (menu)')
    c.waitfor(text='Pagar tudo de uma vez', timeout=15)
    c.hover(TXT('Recicla Vale Metais', within=MAIN), 0.6, at=c.A(1, 'todas:', 0.5), label='a matriz e a filial')
    c.hover(TXT('Filial Pindamonhangaba', within=MAIN), 0.6, at=c.A(1, 'plano,', 0.5), label='plano de cada unidade (sem zoom nos valores)')
    c.hover(TXT('Ativa', within=MAIN, nth=1), 0.6, at=c.A(1, 'ativa', 0.5), label='Ativa')
    c.mark(2)
    c.hover(BTNX('Pagar tudo de uma vez'), 1.2, at=c.A(2, 'pagar', 0.5), label='Pagar tudo de uma vez (ZOOM)')
    c.mark(3)
    c.click(BTNX('Pagar tudo de uma vez'), at=c.A(3, 'Repara', 0.6), label='Pagar tudo de uma vez')
    c.waitfor(text='Unidades cobradas juntas', timeout=15)
    c.ev(ANIMA)
    c.hover(TXTP('Ao pagar, as cobranças individuais das unidades são canceladas'), 1.5, at=c.A(3, 'aviso:', 0.5), label='aviso das cobranças (ZOOM)')
    c.mark(4)
    c.hover(TXTP('Ao pagar, as cobranças individuais das unidades são canceladas'), 1.5, at=c.A(4, 'filial', 0.5), label='aviso das cobranças (continua)')
    c.mark(5)
    # o checkout pergunta a cada 5 s se o Pix foi pago, a contar da criação da cobrança: o clique em "Escolho" deixa a consulta que confirma
    # o pagamento ~0,5 s depois de "pronto:" (o bastidor marca a cobrança paga logo antes dela)
    c.click(BTNX('PIX'), at=c.A(5, 'Escolho', 0.4), label='PIX')
    c.waitfor(text='Copia e Cola', timeout=12)
    c.mark(6)
    c.ev(JS_PAGA, label='bastidor: o Pix é pago (a cobrança fica RECEIVED antes da próxima consulta)')
    c.waitfor(text='Pagamento Confirmado!', timeout=8)
    c.registra(TXT('Pagamento Confirmado!'), label='Pagamento Confirmado!')
    c.fim()
    return c


# ---------------------------------------------------------------- main
def main():
    pedidos = [int(a) for a in sys.argv[1:] if a.isdigit()]
    fns = {n: globals().get(f'cap{n:02d}') for n in range(12)}
    feitos = []
    for n, fn in fns.items():
        if fn is None or (pedidos and n not in pedidos):
            continue
        c = fn()
        d = c.out()
        last = -1
        for stp in d['steps']:   # o `at` precisa ser crescente
            if 'at' in stp:
                if stp['at'] < last - 1e-9:
                    print(f'  aviso cap{n:02d}: at {stp["at"]} < {last} em "{stp.get("label") or stp.get("name")}"')
                last = max(last, stp['at'])
        json.dump(d, open(os.path.join(HERE, f'cap{n:02d}.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
        nat = sum(1 for st in d['steps'] if st.get('do') != 'mark')
        feitos.append(f'cap{n:02d} {nat} passos, {len(c.linhas)} linhas, {c.dur:.1f} s{" (fala estimada)" if c.estimado else ""}')
        if os.environ.get('ANCORAS'):
            for i, p, t in c.anchors:
                print(f'   cap{n:02d} L{i} {p!r} -> {t}')
    print('\n'.join(feitos))


if __name__ == '__main__':
    main()
