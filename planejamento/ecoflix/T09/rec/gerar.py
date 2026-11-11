#!/usr/bin/env python3
"""T09 · Pedidos e histórico do caixa: gera rec/t09/cap00..cap10.json (roteiros do robô) a partir da voz (t09/narracao/capNN.json).

EcoSistema 1.59.154 no Supabase falso (mundo da Recicla Vale Metais), computador 1280x800, logado como Rafael Nogueira (MASTER).
Cada passo é preso a uma palavra da fala: `at` = início da palavra - folga (o custo do gesto, docs/04 "Custo real dos gestos"),
para o cursor CHEGAR na palavra. A voz ainda é a ESTIMADA: quando a voz de verdade chegar, o capNN.json da voz substitui o
estimado e este gerador roda de novo, sem reescrever nada. Rodar de qualquer pasta: `python3 -I rec/t09/gerar.py [NN ...]`.

Relógio do mundo (FAKE_NOW, igual no Supabase falso e no robô): 2026-11-11T08:30:00-03:00 (quarta) em todos os capítulos; a
instância do Supabase falso da aula é a 54309.

Estado de partida: sementes rec/mundo/seeds-extra/t09/ (rec/t09/t09_sementes.py), acumuladas por capítulo (SEMENTE abaixo).

Login: o capítulo abre SEM sessão ("anonymous") e o `setup` (fora do vídeo) entra pela tela de login com "$TUT_USER"/"$TUT_SENHA"
(variáveis de ambiente; o Supabase falso aceita qualquer senha). O `storage` leva as chaves de "já vi" (versão do app, tarefas do
dia, preferências iniciais): sem elas, avisos do app abririam por cima da tela.

Particularidades desta aula:
 - PDFs e relatórios abrem em aba nova (window.open). O vídeo grava uma aba só: o `setup` instala ganchos que guardam cada PDF
   (URL.createObjectURL) e cada aba aberta (window.open); passos `eval` devolvem o PDF (base64) e o HTML do relatório para o
   actions.json, e rec/t09/t09_pdfs.py grava os arquivos para a edição mostrar como ilustração (o PDF/relatório do próprio app).
 - "Popup bloqueado" (cap06): o gancho do window.open devolve null UMA vez quando `window.__bloqueia` está ligado (o navegador
   "bloqueou"); o aviso é o do app.
 - Observador `OBS` guarda em `window.__avisos` todo aviso de erro do app, tela escura e a faixa "Lembrete da trilha"; o último
   passo de cada capítulo devolve a lista (tem de sair vazia). `confere*` LÊ a tela e compara com a fala (resumo.py acusa DIFERENTE).
"""
import hashlib
import json
import os
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TUT = os.path.normpath(os.path.join(HERE, '..', '..'))
NARR = os.path.join(TUT, 't09', 'narracao')
FAKE_NOW = '2026-11-11T08:30:00-03:00'


def stable_id(chave):
    """o mesmo UUID estável do Supabase falso (core/util.mjs stableId)"""
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
HOJE = '2026-11-11'
STORAGE = {
    'app_version': VERSAO, 'notification_shown_version': VERSAO, f'dominex:daily-tasks-shown:{RAFAEL}': HOJE,
    'pwa-install-dismissed': 'true', 'theme': 'light', f'daily-tasks-reminder-last-shown-{RAFAEL}': HOJE, 'initial-preferences-set': 'true',
}

NOMES = ['Abertura', 'Duas telas, dois trabalhos', 'A tela Pedidos', 'Filtrar até achar', 'Editar um pedido', 'Excluir e o selo de estornado',
         'Reimprimir e cupom sem valor', 'O Histórico do Caixa', 'Relatórios do caixa', 'Reabrir um caixa antigo', 'Recapitulando']
CADEIA = ['inicio', 'apos-cap04', 'apos-cap05', 'apos-cap06', 'apos-cap09']
SEMENTE = {0: 'inicio', 1: 'inicio', 2: 'inicio', 3: 'inicio', 4: 'inicio', 5: 'apos-cap04', 6: 'apos-cap05', 7: 'apos-cap06', 8: 'apos-cap06',
           9: 'apos-cap06', 10: 'apos-cap09'}


def sementes(n):
    return [f't09/{s}' for s in CADEIA[:CADEIA.index(SEMENTE[n]) + 1]]


def norm(s):
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode().lower()
    return ''.join(ch for ch in s if ch.isalnum() or ch in '?')


def carregar_voz(n):
    d = json.load(open(os.path.join(NARR, f'cap{n:02d}.json'), encoding='utf8'))
    return d['words'], d['linhas'], float(d['dur']), bool(d.get('estimado'))


# Observador de avisos de erro na tela (aceite): textos com "Não foi possível", "Erro ao", "Tente novamente", "indisponível",
# "Algo deu errado", tela escura (div.fixed preta) e a faixa "Lembrete da trilha de tutoriais" da EcoFlix.
OBS = ("(()=>{window.__avisos=[];const re=/N[ãa]o foi poss[ií]vel|Erro ao|Tente novamente|indispon[ií]vel|Algo deu errado|Falha ao/i;"
       "const chk=(t)=>{t=(t||'').trim();const m=t&&t.match(new RegExp('[^]{0,40}('+re.source+')[^]{0,40}','i'));"
       "if(m&&window.__avisos.length<10)window.__avisos.push(m[0].replace(/[\\n\\r\\t ]+/g,' '))};new MutationObserver(ms=>{for(const m of ms){"
       "m.addedNodes.forEach(n=>chk(n.textContent));if(m.type==='characterData')chk(m.target.textContent)}}).observe(document.body,"
       "{childList:true,subtree:true,characterData:true});chk(document.body.innerText);"
       "setInterval(()=>{const f=document.querySelector('section[aria-label^=\"Lembrete da trilha\"]');"
       "if(f&&window.__avisos.length<10&&!window.__avisos.includes('TRILHA ECOFLIX'))window.__avisos.push('TRILHA ECOFLIX')},300);return 1})()")

# Ganchos das abas novas: guarda cada PDF (blob application/pdf) e cada janela aberta; `window.__bloqueia` = o próximo window.open
# devolve null (o navegador "bloqueou" o pop-up). A aba aberta de verdade fica em segundo plano (o vídeo grava só esta).
GANCHOS = ("(()=>{if(window.__abas)return 'ja';window.__abas=[];window.__pdfs=[];const o=URL.createObjectURL.bind(URL);"
           "URL.createObjectURL=(b)=>{try{if(b&&b.type==='application/pdf')window.__pdfs.push(b)}catch(e){}return o(b)};"
           "const wo=window.open.bind(window);window.open=(...a)=>{if(window.__bloqueia){window.__bloqueia=0;return null}"
           "const w=wo(...a);window.__abas.push(w);return w};return 'ganchos'})()")


def js_pdf(k, nome):
    """devolve o k-ésimo PDF que o app gerou (base64) para o actions.json: t09_pdfs.py grava o arquivo para a edição"""
    return ("(async()=>{for(let i=0;i<40&&!(window.__pdfs&&window.__pdfs.length>%d);i++)await new Promise(r=>setTimeout(r,200));"
            "const b=window.__pdfs&&window.__pdfs[%d];if(!b)return 'SEM PDF';const u=new Uint8Array(await b.arrayBuffer());let s='';"
            "for(let i=0;i<u.length;i+=8192)s+=String.fromCharCode.apply(null,u.subarray(i,i+8192));return {pdf:%s,bytes:u.length,b64:btoa(s)}})()") % (
        k, k, json.dumps(nome))


def js_aba_html(k, nome, espera_txt):
    """devolve o HTML da k-ésima aba aberta (relatório em HTML escrito pelo app) quando ele já tem `espera_txt`"""
    return ("(async()=>{let w=null,h='';for(let i=0;i<50;i++){w=window.__abas&&window.__abas[%d];try{h=w&&w.document&&w.document.documentElement.outerHTML||''}catch(e){h=''}"
            "if(h.includes(%s))break;await new Promise(r=>setTimeout(r,200));}if(!h.includes(%s))return 'SEM ABA: '+h.slice(0,120);"
            "return {html:%s,chars:h.length,b64:btoa(unescape(encodeURIComponent(h)))}})()") % (k, json.dumps(espera_txt), json.dumps(espera_txt), json.dumps(nome))


class Cap:
    def __init__(s, n, pace=0.5, cps=9, start=(900, 440), setup=None, noscroll=False):
        s.n = n
        s.words, s.linhas, s.dur, s.estimada = carregar_voz(n)
        s.steps = []
        s.pace, s.cps, s.start = pace, cps, start
        s.noscroll = noscroll
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
        """leva o cursor a um ponto neutro (scroll de 0 px): tira o mouse de cima de um menu ou de uma linha"""
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
        return {
            'name': f't09-cap{s.n:02d}',
            'title': f'T09 · Cap. {s.n} · {NOMES[s.n]} (narração {str(round(s.dur, 1)).replace(".", ",")} s{" ESTIMADA" if s.estimada else ""}; '
                     f'marcas L1..L{len(s.linhas)} = início de cada linha do roteiro; FAKE_NOW {FAKE_NOW})',
            'seed': f't09-cap{s.n:02d}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
            'start': {'x': s.start[0], 'y': s.start[1]},
            'anonymous': True, 'storage': dict(STORAGE),
            'seedExtra': sementes(s.n),
            'prewarm': ['/login'], 'setup': s.setup, 'steps': s.steps,
        }


# ---------------------------------------------------------------- alvos
BTN = lambda n, **kw: {'role': 'button', 'name': n, 'exact': True, **kw}
BTNX = lambda n, **kw: {'role': 'button', 'name': n, **kw}
TXT = lambda t, **kw: {'text': t, 'exact': True, **kw}
TXTX = lambda t, **kw: {'text': t, **kw}
SEL = lambda s, **kw: {'selector': s, **kw}
OPT = lambda n, **kw: {'role': 'option', 'name': n, **kw}
ITEM = lambda n, **kw: {'role': 'menuitem', 'name': n, **kw}
DLG = '[role=dialog]'
PH = lambda p, **kw: {'placeholder': p, **kw}
MENU = '[data-sidebar=sidebar]'

# ---------------------------------------------------------------- setup (fora do vídeo)
LOGIN = [
    {'do': 'waitFor', 'target': PH('seu@email.com'), 'timeout': 40},
    {'do': 'type', 'target': PH('seu@email.com'), 'text': '$TUT_USER', 'cps': 40},
    {'do': 'type', 'target': PH('••••••••'), 'text': '$TUT_SENHA', 'cps': 40},
    {'do': 'click', 'target': BTN('Entrar')},
    {'do': 'waitFor', 'url': '/dashboard', 'timeout': 40},
    {'do': 'waitFor', 'idle': True, 'timeout': 25},
    {'do': 'eval', 'js': GANCHOS},
]

# rolagem suave do contêiner que rola o alvo (molde do T14: ACHA_ROLAGEM + SUAVE): o cursor não se mexe
ACHA_ROLAGEM = ("const rolagem=(el)=>{let c=el&&el.parentElement;while(c&&c!==document.body){const s=getComputedStyle(c);"
                "if(/(auto|scroll)/.test(s.overflowY)&&c.scrollHeight>c.clientHeight+4)return c;c=c.parentElement;}"
                "const se=document.scrollingElement;return se&&se.scrollHeight>se.clientHeight+4?se:null};")
SUAVE = ("await new Promise(res=>{const f=t=>{const p=Math.min(1,(t-t0)/DUR),e=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;c.scrollTo({top:DESTINO,behavior:'instant'});"
         "p<1?requestAnimationFrame(f):res()};requestAnimationFrame(f)});")


def js_ate_el(expr, y=250, dur_ms=900):
    """rola (suave) o contêiner do elemento `expr` (expressão JS) até ele ficar em y px CSS. Devolve o topo final, 'ok', 'SEM ALVO'."""
    return ("(async()=>{" + ACHA_ROLAGEM + "const el=" + expr + ";if(!el)return 'SEM ALVO';const c=rolagem(el);if(!c)return 'SEM ROLAGEM';"
            f"const dy=Math.round(el.getBoundingClientRect().top-{int(y)});if(Math.abs(dy)<3)return 'ok';const y0=c.scrollTop,t0=performance.now();"
            + SUAVE.replace('DUR', str(int(dur_ms))).replace('DESTINO', 'y0+dy*e') +
            "return Math.round(el.getBoundingClientRect().top)})()")


def js_topo(escopo='main', dur_ms=700):
    sel = json.dumps(escopo)
    return ("(async()=>{" + ACHA_ROLAGEM + f"const raiz=document.querySelector({sel});let c=null;"
            "for(const e of [raiz,...(raiz?raiz.querySelectorAll('*'):[])]){if(!e)continue;const s=getComputedStyle(e);if(/(auto|scroll)/.test(s.overflowY)&&e.scrollHeight>e.clientHeight+4&&e.scrollTop>2){c=e;break}}"
            "if(!c){const se=document.scrollingElement;if(se&&se.scrollTop>2)c=se}if(!c)return 'ok';const y0=c.scrollTop,t0=performance.now();"
            + SUAVE.replace('DUR', str(int(dur_ms))).replace('DESTINO', 'y0*(1-e)') + "return 'topo:'+Math.round(c.scrollTop)})()")


# ---------------------------------------------------------------- alvos da aula (rec/t09/_ex: explorações de 11/11)
RECOLHE_MENU = ("(()=>{const b=document.querySelector('header svg.lucide-panel-left-close')?.closest('button');"
                "if(!b)return document.querySelector('header svg.lucide-panel-left')?'ja recolhido':'sem botao';b.click();return 'recolhido'})()")
PEDIDOS_OK = 'Histórico completo de compras e vendas'
PERIODO = lambda txt: SEL(f"main [role=combobox]:has-text('{txt}')")          # o período da tela (Radix Select: clique real)
LINHA = lambda txt: f"main tbody tr:has-text('{txt}')"                        # a linha do pedido (data e hora são da semente)
MENU_LINHA = lambda txt: SEL(f"{LINHA(txt)} button")                          # o "⋮" (HoverDropdownMenu: abre ao passar o mouse)
L_CIDA, L_VALDIR, L_DUP = '11/11/2026 07:22', '11/11/2026 07:41', '11/11/2026 07:42'
L_BATERIA = "Depósito Irmãos Siqueira'):has-text('744,00"                     # a compra de 21/10 (fecha o :has-text de LINHA)
LINK = lambda n: {'role': 'link', 'name': n, 'exact': True, 'within': MENU}


def setup_pedidos(periodo=None, extra=(), recolhe=True):
    """login, Pedidos (aquece a lista), menu recolhido (a tabela inteira cabe a 1280 px), período escolhido fora do vídeo"""
    st = list(LOGIN) + [{'do': 'goto', 'url': '/pedidos'}, {'do': 'waitFor', 'text': PEDIDOS_OK, 'timeout': 30}, {'do': 'waitFor', 'idle': True, 'timeout': 25}]
    if recolhe:
        st += [{'do': 'eval', 'js': RECOLHE_MENU}, {'do': 'wait', 'seconds': 0.8}]
    if periodo:
        st += [{'do': 'click', 'target': PERIODO('Este mês')}, {'do': 'click', 'target': OPT(periodo)},
               {'do': 'waitFor', 'target': PERIODO(periodo), 'timeout': 10}, {'do': 'waitFor', 'idle': True, 'timeout': 15}, {'do': 'wait', 'seconds': 0.8}]
    return st + list(extra)


def abre_menu_linha(c, linha, at, rotulo):
    """passa o mouse no "⋮" da linha: o menu do pedido abre (HoverDropdownMenu, fecha 300 ms depois que o mouse sai)"""
    c.hover(MENU_LINHA(linha), 0.3, at=at, label=rotulo, optional=False, timeout=8)
    c.waitfor(target=ITEM('Ver comprovante'), timeout=6)

# ================================================================ capítulos
CAPS_ROBO = {}


def capitulo(fn):
    CAPS_ROBO[int(fn.__name__[3:])] = fn
    return fn


@capitulo
def cap00():
    """Abertura: o Dashboard com o menu aberto (L1-L2 sob a ilustração do telefonema); L3 Pedidos e Financeiro > Histórico do Caixa no
    menu, sem navegar (o grupo Financeiro só se abre para o item aparecer); L4 o cartão "Antes" (edição)."""
    setup = list(LOGIN) + [{'do': 'goto', 'url': '/pedidos'}, {'do': 'waitFor', 'text': PEDIDOS_OK, 'timeout': 30}, {'do': 'waitFor', 'idle': True, 'timeout': 25},
                           {'do': 'goto', 'url': '/dashboard'}, {'do': 'waitFor', 'idle': True, 'timeout': 25}, {'do': 'wait', 'seconds': 1.0}]
    c = Cap(0, setup=setup, start=(760, 470))
    c.mark(1)
    c.registra(SEL('main'), at=0.4, label='Dashboard (sob a ilustração do telefonema)')
    c.mark(2)
    c.mark(3)
    c.hover(LINK('Pedidos'), 0.5, at=c.A(3, 'Pedidos,', 0.7), label='menu Pedidos (sem clicar)')
    c.click(BTN('Financeiro', within=MENU), at=c.A(3, 'Histórico', 1.4), label='abre o grupo Financeiro (sem navegar)')
    c.hover(LINK('Histórico do Caixa'), 0.6, at=c.A(3, 'Caixa,', 0.6), label='menu Financeiro > Histórico do Caixa (sem clicar)')
    c.hover(BTN('Financeiro', within=MENU), 0.4, at=c.A(3, 'Financeiro.', 0.6), label='grupo Financeiro')
    c.mark(4)
    c.cursor((760, 470), at=c.A(4, 'Se', 0.3), label='cursor descansa (cartão "Antes: Ticket de Pesagem")')
    c.fim()
    return c


@capitulo
def cap01():
    """Duas telas, dois trabalhos: ilustração pedido x caixa (L1-L3) sobre o Dashboard; L4 clica em Pedidos no menu."""
    setup = list(LOGIN) + [{'do': 'goto', 'url': '/pedidos'}, {'do': 'waitFor', 'text': PEDIDOS_OK, 'timeout': 30}, {'do': 'waitFor', 'idle': True, 'timeout': 25},
                           {'do': 'goto', 'url': '/dashboard'}, {'do': 'waitFor', 'idle': True, 'timeout': 25}, {'do': 'wait', 'seconds': 1.0}]
    c = Cap(1, setup=setup, start=(760, 470))
    c.mark(1)
    c.registra(SEL('main'), at=0.4, label='Dashboard (sob a ilustração pedido x caixa)')
    c.mark(2)
    c.mark(3)
    c.mark(4)
    c.click(LINK('Pedidos'), at=c.A(4, 'pedidos.', 0.8), label='menu Pedidos')
    c.waitfor(text=PEDIDOS_OK, timeout=15)
    c.confere('main', ['Pedidos', PEDIDOS_OK, 'Todas as Ordens'], 'tela Pedidos')
    c.fim()
    return c


@capitulo
def cap02():
    """A tela Pedidos (menu recolhido no setup): período e lista (L1), o Resumo do período aberto (L2, zoom), as colunas (L3),
    a linha da latinha da Aparecida aberta com os 24 kg (L4) e o "⋮" sem abrir (L5)."""
    c = Cap(2, setup=setup_pedidos())
    c.mark(1)
    c.hover(PERIODO('Este mês'), 0.5, at=c.A(1, 'mês', 0.7), label='período "Este mês"')
    c.hover(TXT('Todas as Ordens', within='main'), 0.5, at=c.A(1, 'todas', 0.7, nth=0), label='"Todas as Ordens" com a contagem')
    c.mark(2)
    c.click(TXT('Resumo do período filtrado', within='main'), at=c.A(2, 'resumo', 0.8), label='abre o Resumo do período filtrado')
    c.registra(RESUMO, at=c.A(2, 'quanto', 0.2), label='[ZOOM] Resumo do período filtrado: Compras e Vendas por forma de pagamento')
    c.hover(RESUMO_COMPRAS, 0.4, at=c.A(2, 'compras', 0.6), label='Compras')
    c.hover(RESUMO_VENDAS, 0.4, at=c.A(2, 'vendas,', 0.6), label='Vendas')
    c.cursor((780, 470), at=c.A(2, 'saldo.', 0.2), label='cursor sai do resumo')
    c.mark(3)
    for col, palavra, nth in (('Usuário', 'quem', 0), ('Data', 'data,', 0), ('Tipo', 'compra', 0), ('N° Pedidos', 'número,', 0),
                              ('Cliente/Fornecedor', 'cliente', 0), ('Pagamento', 'pago', 0), ('Valor', 'valor.', 0)):
        c.hover(SEL(f"main thead th:has-text('{col}')"), 0.2, at=c.A(3, palavra, 0.6, nth=nth), label=f'coluna {col}')
    c.mark(4)
    c.click(TXT(L_CIDA, within='main'), at=c.A(4, 'Clicando', 0.6), label='abre a linha da latinha da Aparecida (hoje 07:22)')
    c.hover(TXT('Alumínio latinha', within=f"main tbody tr:has-text('Fornecedor:')"), 0.4, at=c.A(4, 'materiais,', 0.6), label='o material da linha')
    c.hover(TXTX('24.00 Kg', within='main'), 0.8, at=c.A(4, 'vinte', 0.6), label='[ZOOM] o peso: 24 kg')
    c.mark(5)
    c.registra(MENU_LINHA(L_CIDA), at=c.A(5, 'menu', 0.3), label='[DESTAQUE] o "⋮" no fim da linha (sem abrir)')
    c.cursor((1120, 541), at=c.A(5, 'menu', 0.6), label='cursor perto do "⋮" (passar por cima abriria o menu)')
    c.fim()
    return c


POP = '[data-radix-popper-content-wrapper]'
FILTROS = BTNX('Filtros', within='main')                                      # abre "Filtrar pedidos" (Popover, à direita)
PAINEL = f"{POP}:has-text('Filtrar pedidos')"
BUSCA_PED = PH('Pedido, cliente, operador, placa...')
CAMPO_FILTRO = lambda n: SEL(f"{PAINEL} button:has-text('{n}')")              # "Tipo", "Material", "Forma de Pagamento" (multiseleção)
OPCAO = lambda n: SEL(f"{POP} label:has-text('{n}')")                         # opção com caixa de marcar (o clique no rótulo marca)
BUSCA_OPCAO = PH('Buscar...')


def filtros_bateria(c=None, ats=None):
    """Tipo: Compras, Material: Bateria automotiva, Forma de Pagamento: Com Pix/Transferência (o painel Filtros já aberto). Sem `c`,
    devolve os passos para o setup."""
    passos = [('click', CAMPO_FILTRO('Tipo'), 'Tipo'), ('click', OPCAO('Compras'), 'Compras'),
              ('click', CAMPO_FILTRO('Material'), 'Material'), ('type', BUSCA_OPCAO, 'bat'), ('click', OPCAO('Bateria automotiva'), 'Bateria automotiva'),
              ('click', CAMPO_FILTRO('Forma de Pagamento'), 'Forma de Pagamento'), ('click', OPCAO('Com Pix/Transferência'), 'Com Pix/Transferência')]
    if c is None:
        out = []
        for g, alvo, txt in passos:
            out.append({'do': 'click', 'target': alvo} if g == 'click' else {'do': 'type', 'target': alvo, 'text': txt, 'noClick': True, 'cps': 40})
            out.append({'do': 'wait', 'seconds': 0.4})
        return out
    for (g, alvo, txt), at in zip(passos, ats):
        if g == 'click':
            c.click(alvo, at=at, label=f'filtro: {txt}')
        else:
            c.type(alvo, txt, at=at, noClick=True, cps=40, label=f'digita "{txt}" na busca do Material')


@capitulo
def cap03():
    """Filtrar até achar: Mês passado (L1); Filtros e a busca "Vale Forte" (L2); o painel fecha e as compras da Vale Forte ficam à mostra
    (L3, zoom); Tipo, Material e Forma de Pagamento (L4); a linha que sobra aberta (L5, zoom); as etiquetas e o Limpar todos (L6)."""
    c = Cap(3, setup=setup_pedidos())
    c.mark(1)
    c.click(PERIODO('Este mês'), at=c.A(1, 'período:', 0.9), label='período')
    c.click(OPT('Mês passado'), at=c.A(1, 'Mês', 0.6), label='Mês passado')
    c.waitfor(target=PERIODO('Mês passado'), timeout=8)
    c.mark(2)
    c.click(FILTROS, at=c.A(2, 'Filtros,', 0.8), label='Filtros')
    c.waitfor(text='Filtrar pedidos', timeout=8)
    c.hover(BUSCA_PED, 0.5, at=c.A(2, 'busca', 0.6), label='a busca do painel (pedido, cliente, operador, placa)')
    c.click(BUSCA_PED, at=c.A(2, 'Digito', 0.7), label='clica na busca')
    c.type(BUSCA_PED, 'Vale Forte', at=c.A(2, 'Vale', 0.05), noClick=True, cps=14, label='digita Vale Forte')
    c.mark(3)
    c.press('Escape', at=c.A(3, 'No', 0.3), label='fecha o painel (a lista fica à mostra)')
    c.registra(SEL('main tbody'), at=c.A(3, 'nome', 0.2), label='[ZOOM] as compras de outubro da Auto Peças Vale Forte (nenhuma de bateria)')
    c.cursor((700, 600), at=c.A(3, 'Auto', 0.6), label='cursor passa pelas linhas da Vale Forte')
    c.mark(4)
    c.click(FILTROS, at=c.A(4, 'procuro', 0.8), label='Filtros de novo')
    c.click(BUSCA_PED, at=c.A(4, 'sei', 0.6), label='busca')
    c.type(BUSCA_PED, '', at=c.A(4, 'compra.', 0.3), noClick=True, clear=True, label='apaga a busca')
    filtros_bateria(c, [c.A(4, 'Tipo,', 0.7), c.A(4, 'Compras.', 0.6), c.A(4, 'Material,', 0.7), c.A(4, 'Bateria', 0.4),
                        c.A(4, 'automotiva.', 0.4), c.A(4, 'forma', 0.7), c.A(4, 'Pix.', 0.6)])
    c.mark(5)
    c.press('Escape', at=c.A(5, 'Achou:', 0.6), label='fecha a lista da forma de pagamento')
    c.press('Escape', at=c.A(5, 'Achou:', 0.3), label='fecha o painel Filtros')
    c.click(TXTX('21/10/2026', within='main tbody'), at=c.A(5, 'vinte', 0.6), label='abre a linha de 21/10 (Depósito Irmãos Siqueira, R$ 744,00)')
    c.confere('main tbody', ['21/10/2026', 'Depósito Irmãos Siqueira', 'Bateria automotiva', '744,00'], 'a linha da bateria (21/10, Siqueira, R$ 744,00)')
    c.registra(SEL("main tbody"), at=c.A(5, 'quilos', 0.2), label='[ZOOM] a linha e o item: Bateria automotiva, 240 kg, R$ 744,00')
    c.hover(TXTX('Bateria automotiva', within='main tbody'), 0.5, at=c.A(5, 'bateria,', 0.6), label='o item Bateria automotiva')
    c.hover(TXTX('Depósito Irmãos Siqueira', within='main tbody'), 0.6, at=c.A(5, 'Depósito', 0.6), label='o fornecedor errado: Depósito Irmãos Siqueira')
    c.mark(6)
    c.hover(TXTX('Filtrando por', within='main'), 0.5, at=c.A(6, 'etiqueta', 0.6), label='[DESTAQUE] as etiquetas "Filtrando por"')
    c.hover(TXTX('Limpar todos', within='main'), 0.8, at=c.A(6, 'Limpar', 0.6), label='Limpar todos (sem clicar)')
    c.fim()
    return c


HIST_OK = 'Todos os registros de fechamento do caixa'
BUSCA_CX = PH('Buscar por responsável, data ou código...')
LINHA_CX = lambda n: f"main tbody tr:has-text('#{n}')"
ACOES_CX = lambda n: SEL(f"{LINHA_CX(n)} button[aria-label='Ações']")


def setup_historico(busca=None, extra=()):
    st = list(LOGIN) + [{'do': 'goto', 'url': '/historico-caixa'}, {'do': 'waitFor', 'text': HIST_OK, 'timeout': 30}, {'do': 'waitFor', 'idle': True, 'timeout': 25}]
    if busca:
        st += [{'do': 'type', 'target': BUSCA_CX, 'text': busca, 'cps': 40}, {'do': 'waitFor', 'target': SEL(LINHA_CX(70)), 'timeout': 10},
               {'do': 'wait', 'seconds': 0.8}]
    return st + list(extra)


@capitulo
def cap07():
    """O Histórico do Caixa: Financeiro > Histórico do Caixa pelo menu (L1); as colunas (L2); a correntinha dos caixas de ontem (L3, zoom);
    o resumo de um caixa (L4); a busca "21/10" e o #70 do Marcos (L5, zoom); o botão Filtros (L6)."""
    setup = list(LOGIN) + [{'do': 'goto', 'url': '/historico-caixa'}, {'do': 'waitFor', 'text': HIST_OK, 'timeout': 30}, {'do': 'waitFor', 'idle': True, 'timeout': 25},
                           {'do': 'goto', 'url': '/dashboard'}, {'do': 'waitFor', 'idle': True, 'timeout': 25}, {'do': 'wait', 'seconds': 1.0}]
    c = Cap(7, setup=setup, start=(760, 470))
    c.mark(1)
    c.click(BTN('Financeiro', within=MENU), at=c.A(1, 'Histórico', 1.2), label='menu Financeiro')
    c.click(LINK('Histórico do Caixa'), at=c.A(1, 'Financeiro.', 0.7), label='menu Histórico do Caixa')
    c.waitfor(text=HIST_OK, timeout=15)
    c.hover(SEL(LINHA_CX(85)), 0.6, at=c.A(1, 'cada', 0.6), label='cada caixa fechado, um por linha')
    c.mark(2)
    for col, palavra in (('Código', 'número'), ('Abertura', 'abriu'), ('Fechamento', 'fechou,'), ('Aberto por', 'quem'),
                         ('Saldo Inicial', 'inicial'), ('Saldo Final', 'final.')):
        c.hover(SEL(f"main thead th:has-text('{col}')"), 0.2, at=c.A(2, palavra, 0.6), label=f'coluna {col}')
    c.mark(3)
    c.hover(SEL(f"{LINHA_CX(85)} svg.lucide-link2"), 1.6, at=c.A(3, 'correntinha', 0.6), label='[ZOOM] a correntinha entre o #85 e o #86 (dica "Caixas fechados no mesmo dia")')
    c.hover(SEL(f"{LINHA_CX(86)} svg.lucide-link2"), 0.8, at=c.A(3, 'Marcos,', 0.6), label='o #86 do Marcos, de ontem')
    c.mark(4)
    c.click(TXT('10/11/2026 08:31', within='main'), at=c.A(4, 'Clicando', 0.6), label='abre o resumo do #85 (o caixa do Rafael de ontem)')
    c.waitfor(text='Total Compras', timeout=10)
    for rot, palavra in (('Total Compras', 'compras,'), ('Total Vendas', 'vendas,'), ('Receitas', 'receitas,'), ('Despesas', 'despesas'), ('Lucro Projetado', 'lucro')):
        c.hover(TXTX(rot, within='main tbody'), 0.2, at=c.A(4, palavra, 0.6), label=f'resumo: {rot}')
    c.mark(5)
    c.click(BUSCA_CX, at=c.A(5, 'busca', 0.7), label='a busca')
    c.type(BUSCA_CX, '21/10', at=c.A(5, 'vinte', 0.05), noClick=True, cps=9, label='digita 21/10')
    c.waitfor(target=SEL(LINHA_CX(70)), timeout=10)
    c.confere(LINHA_CX(70), ['#70', '21/10/2026', 'Marcos Antunes', '800,00', '612,50'], 'o #70 do Marcos (21/10, R$ 800,00 e R$ 612,50)')
    c.hover(SEL(LINHA_CX(70)), 1.0, at=c.A(5, 'Marcos', 0.6), label='[ZOOM] a linha do #70 do Marcos')
    c.mark(6)
    c.hover(BTN('Filtros', within='main'), 0.8, at=c.A(6, 'Filtros,', 0.6), label='Filtros (sem abrir)')
    c.cursor((760, 600), at=c.A(6, 'grande.', 0.2), label='cursor descansa')
    c.fim()
    return c


TOAST = lambda t: SEL(f"[data-sonner-toast]:has-text('{t}')")
PREVIA = "[role=alertdialog]:has-text('Vou desfazer tudo que este pedido criou:')"
L_ESTORNO = "03/11/2026'):has-text('Estornado em"                            # a cópia de 03/11 da Aparecida (fecha o :has-text de LINHA)


@capitulo
def cap05():
    """Excluir e o selo de estornado: as duas compras do Valdir (L1); a prévia da exclusão (L2, zoom); Excluir pedido (L3); Este mês e o
    selo "Estornado em 05/11" com a dica (L4-L5, zoom); (ilustração L6); Configurações > Empresa > Ver histórico (L7)."""
    c = Cap(5, setup=setup_pedidos('Hoje', extra=ITENS_50))
    c.mark(1)
    c.hover(SEL(LINHA(L_VALDIR)), 0.5, at=c.A(1, 'Valdir', 0.6), label='a compra do Valdir das 07:41')
    c.hover(SEL(LINHA(L_DUP)), 0.8, at=c.A(1, 'duas', 0.6), label='[DESTAQUE] a mesma compra às 07:42 (duplicada)')
    c.mark(2)
    abre_menu_linha(c, L_DUP, c.A(2, 'Excluir,', 1.5), 'menu da compra das 07:42')
    c.click(ITEM('Excluir'), at=c.A(2, 'Excluir,', 0.6), label='Excluir')
    c.waitfor(text='Vou desfazer tudo que este pedido criou:', timeout=8)
    c.waitfor(target=SEL(f"{PREVIA} :text-is('Estoque')"), timeout=10)
    c.confere(PREVIA, ['Ferro misto', '280', 'Pagamento em dinheiro', '210,00', '(apaga)'], 'prévia: 280 kg de ferro misto e R$ 210,00 em dinheiro')
    c.registra(SEL(f"{PREVIA} div.space-y-4"), at=c.A(2, 'mostra', 0.2), label='[ZOOM] os blocos Estoque e Financeiro da prévia')
    c.hover(TXTX('Ferro misto', within=PREVIA), 0.6, at=c.A(2, 'duzentos', 0.6, nth=0), label='− Ferro misto 280 Kg')
    c.hover(TXTX('Pagamento em dinheiro', within=PREVIA), 0.6, at=c.A(2, 'duzentos', 0.6, nth=1), label='− Pagamento em dinheiro R$ 210,00 (apaga)')
    c.mark(3)
    c.click(BTN('Excluir pedido'), at=c.A(3, 'Excluir', 0.7), label='Excluir pedido')
    c.waitfor(text='Pedido excluído', timeout=10)
    c.registra(TOAST('Pedido excluído'), at=c.A(3, 'aberto,', 0.2), label='aviso "Pedido excluído"')
    c.mark(4)
    c.click(PERIODO('Hoje'), at=c.A(4, 'Agora', 0.7), label='período')
    c.click(OPT('Este mês'), at=c.A(4, 'repara', 0.5), label='Este mês')
    c.waitfor(target=SEL(LINHA(L_ESTORNO)), timeout=10)
    c.ev(js_ate_el("[...document.querySelectorAll('main tbody tr')].find(t=>t.innerText.includes('Estornado em'))", y=430, dur_ms=1100),
         at=c.A(4, 'compra', 0.9, nth=0), label='rola a lista até as compras de 03/11 da Aparecida')
    c.hover(SEL(f"{LINHA(L_ESTORNO)} :text('Estornado em')"), 2.6, at=c.A(4, 'cópia', 0.6), label='[ZOOM] o selo "Estornado em 05/11" e a dica')
    c.mark(5)
    c.hover(SEL(f"{LINHA(L_ESTORNO)} :text('Estornado em')"), 3.0, at=c.A(5, 'Ele', 0.2), label='a dica continua (correção no caixa do dia em que excluiu)')
    c.mark(6)
    c.cursor((700, 300), at=c.A(6, 'O', 0.2), label='cursor sai do selo (ilustração excluir x estornar)')
    c.mark(7)
    c.click(CONFIG_MENU, at=c.A(7, 'Só', 0.8), label='Configurações (rodapé do menu)', noScroll=True)
    c.waitfor(text='Histórico de Exclusões', timeout=15)
    c.ev(js_ate_el("[...document.querySelectorAll('main h3, main h2, main p, main div')].find(e=>e.children.length===0&&e.textContent.trim()==='Histórico de Exclusões')", y=360, dur_ms=800),
         at=c.A(7, 'Configurações,', 0.5), label='desce até o cartão Histórico de Exclusões')
    c.click(BTNX('Ver histórico'), at=c.A(7, 'Ver', 0.7), label='Ver histórico')
    c.waitfor(text='Excluiu compra', timeout=15)
    c.confere('main', ['Histórico de Exclusões', 'Excluiu compra', 'Valdir Pereira', 'rafael@reciclavalemetais.example'], 'a linha de hoje no Histórico de Exclusões')
    c.registra(SEL("main :is(div,li):has(> * :text('Excluiu compra')):has-text('Valdir Pereira')"), at=c.A(7, 'histórico.', -0.6),
               label='[ZOOM] a linha "Excluiu compra "Valdir Pereira"", com a hora e o e-mail')
    c.fim()
    return c


@capitulo
def cap06():
    """Reimprimir e cupom sem valor: o 1º "Ver comprovante" cai no aviso "Popup bloqueado" (L1); (ilustração L2-L3); o 2º abre o PDF (L4,
    o PDF vai para a edição); Cupom sem valor no Valdir (L5) e o selo (L6); o PDF sem valores (L7); a opção Mostrar valores (L8)."""
    c = Cap(6, setup=setup_pedidos('Hoje'))
    c.mark(1)
    c.ev('(()=>{window.__bloqueia=1;return "o próximo pop-up sai bloqueado"})()', label='o navegador "bloqueia" o 1º pop-up (o aviso é o do app)')
    c.hover(SEL(LINHA(L_CIDA)), 0.6, at=c.A(1, 'Aparecida', 0.6), label='a compra da Aparecida (42 kg, R$ 260,40)')
    abre_menu_linha(c, L_CIDA, c.A(1, 'menu', 0.9), 'menu da compra da Aparecida')
    c.click(ITEM('Ver comprovante'), at=c.A(1, 'Ver', 0.6), label='Ver comprovante (bloqueado)')
    c.waitfor(target=TOAST('Popup bloqueado'), timeout=8)
    c.registra(TOAST('Popup bloqueado'), at=c.A(1, 'aviso:', 0.2), label='[ZOOM] aviso "Popup bloqueado. Permita popups para gerar comprovantes."')
    c.cursor((700, 300), at=c.A(1, 'Popup', -0.8), label='cursor descansa')
    c.mark(2)
    c.mark(3)
    c.mark(4)
    abre_menu_linha(c, L_CIDA, c.A(4, 'Pronto:', 1.6), 'menu da compra da Aparecida')
    c.click(ITEM('Ver comprovante'), at=c.A(4, 'Pronto:', 0.7), label='Ver comprovante (abre a aba nova: o PDF entra na edição)')
    c.ev(js_pdf(0, 'comprovante-aparecida'), label='PDF do comprovante da Aparecida (para a edição: 42 kg, R$ 260,40)')
    c.mark(5)
    c.hover(SEL(LINHA(L_VALDIR)), 0.6, at=c.A(5, 'Valdir.', 0.6), label='a compra do Valdir')
    abre_menu_linha(c, L_VALDIR, c.A(5, 'menu,', 1.0), 'menu da compra do Valdir')
    c.click(ITEM('Cupom sem valor'), at=c.A(5, 'Cupom', 0.6), label='Cupom sem valor')
    c.waitfor(text='Cupom sem valor ativado', timeout=8)
    c.mark(6)
    c.hover(TXTX('Comprovante sem valores', within=LINHA(L_VALDIR)), 1.0, at=c.A(6, 'selo', 0.6), label='[ZOOM] o selo "Comprovante sem valores"')
    c.mark(7)
    abre_menu_linha(c, L_VALDIR, c.A(7, 'comprovante', 1.5), 'menu da compra do Valdir')
    c.click(ITEM('Ver comprovante'), at=c.A(7, 'comprovante', 0.6), label='Ver comprovante do Valdir (PDF sem valores, para a edição)')
    c.ev(js_pdf(1, 'comprovante-valdir-sem-valores'), label='PDF do comprovante do Valdir (para a edição: Ferro misto 280 kg, sem valores)')
    c.mark(8)
    abre_menu_linha(c, L_VALDIR, c.A(8, 'opção', 0.8), 'menu da compra do Valdir')
    c.hover(ITEM('Mostrar valores no comprovante'), 1.2, at=c.A(8, 'Mostrar', 0.6), label='[DESTAQUE] "Mostrar valores no comprovante" (sem clicar)')
    c.press('Escape', at=c.A(8, 'comprovante.', -0.6), label='fecha o menu')
    c.cursor((700, 300), at=c.A(8, 'comprovante.', -0.9), label='cursor sai do menu')
    c.fim()
    return c


# @@CAPITULOS@@


def main():
    quais = [int(a) for a in sys.argv[1:] if not a.startswith('-')] or sorted(CAPS_ROBO)
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
