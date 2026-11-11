#!/usr/bin/env python3
"""T20 · Portal do Cliente e Fornecedor: gera rec/t20/cap00..cap10.json (roteiros do robô) a partir da voz (t20/narracao/capNN.json).

EcoSistema 1.59.154 no Supabase falso (mundo da Recicla Vale Metais), computador 1280x800, FAKE_NOW 10/11/2026 15:00 (plano.md), logado como
Rafael Nogueira (MASTER). Cada passo é preso a uma palavra da fala: `at` = início da palavra - folga (o custo do gesto, docs/04 "Custo real dos
gestos"), e a marca Ln entra no início de cada linha. Quando a voz chegar, rodar de novo com o capNN.json da voz (nada a reescrever).
O cap11 (Recapitulando) é montagem das gravações dos capítulos 0 a 10: sem robô.
Rodar de qualquer pasta: `python3 -I rec/t20/gerar.py [NN ...]`; gravar/ensaiar: `bash rec/t20/t20_grava.sh NN [--rapido]`.

DOIS NAVEGADORES (plano.md, "Gravação"): o gravador (rec/recorder/runner.mjs) filma UMA página de UM contexto; não há passo para trocar de
contexto nem de aba. O "navegador do parceiro" e o "do sistema" são, aqui, o MESMO contexto e a mesma aba: o robô troca de rota por dentro do
app (goto interno; o portal público e o sistema são rotas do mesmo app, o `localStorage` do portal `portal_session_<token>` fica de um lado e o
login do Rafael do outro) e a edição trata a troca como corte entre os dois navegadores. A abertura de uma "segunda aba" (Fundição, caps 5 e 7)
é só outra rota. Detalhes e o que falta no gravador: propostas_fala.md, "Achados do app".
Cadeia de sementes (rec/mundo/seeds-extra/t20, geradas por t20_sementes.py, cumulativas sobre o inicio): inicio (caps 0 a 3) -> apos-cap03 (cap04)
-> apos-cap04 (caps 5 e 6) -> apos-cap06 (caps 7 e 8) -> apos-cap08 (caps 9 e 10).
"""
import hashlib
import json
import os
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TUT = os.path.normpath(os.path.join(HERE, '..', '..'))
NARR = os.path.join(TUT, 't20', 'narracao')
NOW = '2026-11-10T15:00:00-03:00'
FAKE_NOW = {n: NOW for n in range(12)}


def stable_id(chave):
    """o mesmo UUID estável do Supabase falso (core/util.mjs stableId)"""
    h = bytearray(hashlib.sha1(('domiflix-fake:' + chave).encode()).digest())
    h[6] = (h[6] & 0x0F) | 0x50
    h[8] = (h[8] & 0x3F) | 0x80
    x = h[:16].hex()
    return f'{x[:8]}-{x[8:12]}-{x[12:16]}-{x[16:20]}-{x[20:32]}'


B62 = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'


def encurta(uuid):
    """uuid -> 22 letras (shortenId do app): o código no fim dos links públicos"""
    def b(n):
        r = ''
        while n > 0:
            r = B62[n % 62] + r
            n //= 62
        return r.rjust(11, '0')
    c = uuid.replace('-', '')
    return b(int(c[:16], 16)) + b(int(c[16:], 16))


RAFAEL = stable_id('user.rafael')
PORTAL_COOP = '/portal/recicla-vale-metais-cooperativa-' + encurta(stable_id('t20.portal.recomeco'))
PORTAL_FUND = '/portal/recicla-vale-metais-fundicao-' + encurta(stable_id('t20.portal.bandeira'))
FOTOS_1749 = '/fotos/recicla-vale-metais-compra-1749-' + encurta(stable_id('t20.fotos.compra1749'))
try:
    VERSAO = open(os.path.join(TUT, 'app', 'dist', '.versao-app'), encoding='utf8').read().strip() or '1.59.154'
except OSError:
    VERSAO = '1.59.154'
HOJE = '2026-11-10'
STORAGE = {
    'app_version': VERSAO, 'notification_shown_version': VERSAO, f'dominex:daily-tasks-shown:{RAFAEL}': HOJE,
    'pwa-install-dismissed': 'true', 'theme': 'light', f'daily-tasks-reminder-last-shown-{RAFAEL}': HOJE, 'initial-preferences-set': 'true',
}
NOMES = ['Abertura', 'O que o parceiro vê', 'Pegar o link do portal', 'Escolher as abas', 'Usuário e senha', 'Histórico de pedidos',
         'O saldo do parceiro', 'Notas e relatório', 'O parceiro pede a coleta', 'O comprovante do portal', 'As fotos do pedido', 'Recapitulando']
SEMENTE = {0: None, 1: None, 2: None, 3: None, 4: 'apos-cap03', 5: 'apos-cap04', 6: 'apos-cap04', 7: 'apos-cap06', 8: 'apos-cap06', 9: 'apos-cap08',
           10: 'apos-cap08', 11: 'apos-cap08'}


def sementes(n):
    """a semente de cada capítulo é cumulativa (tudo desde o início da aula): só a última da cadeia vai junto da base"""
    return ['t20/inicio'] + ([f't20/{SEMENTE[n]}'] if SEMENTE[n] else [])

def norm(s):
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode().lower()
    return ''.join(ch for ch in s if ch.isalnum() or ch in '?')


def carregar_voz(n):
    d = json.load(open(os.path.join(NARR, f'cap{n:02d}.json'), encoding='utf8'))
    return d['words'], d['linhas'], float(d['dur']), bool(d.get('estimado'))


# Observador de avisos de erro na tela (aceite): "Não foi possível", "Erro ao", "Tente novamente", "indisponível", "Algo deu errado",
# "Falha ao", "Transição inválida", "não encontrad" e a faixa "Lembrete da trilha" da EcoFlix. O passo final devolve a lista.
OBS = ("(()=>{window.__avisos=[];const re=/N[ãa]o foi poss[ií]vel|Erro ao|Tente novamente|indispon[ií]vel|Algo deu errado|Falha ao|"
       "Transi[çc][ãa]o inv[áa]lida|n[ãa]o encontrad|Localiza[çc][ãa]o n[ãa]o registrada|Sem sinal de GPS/i;"
       "const chk=(t)=>{t=(t||'').trim();const m=t&&t.match(new RegExp('[^]{0,40}('+re.source+')[^]{0,40}','i'));"
       "if(m&&window.__avisos.length<10)window.__avisos.push(m[0].replace(/[\\n\\r\\t ]+/g,' '))};new MutationObserver(ms=>{for(const m of ms){"
       "m.addedNodes.forEach(n=>chk(n.textContent));if(m.type==='characterData')chk(m.target.textContent)}}).observe(document.body,"
       "{childList:true,subtree:true,characterData:true});chk(document.body.innerText);"
       "setInterval(()=>{const f=document.querySelector('section[aria-label^=\"Lembrete da trilha\"]');"
       "if(f&&window.__avisos.length<10&&!window.__avisos.includes('TRILHA ECOFLIX'))window.__avisos.push('TRILHA ECOFLIX')},300);return 1})()")

# Animação do framer-motion (opacity 0 inline) que o relógio simulado do Playwright deixa começar no futuro (currentTime < 0): a tela
# ficaria em branco por segundos (portal, cartões que entram). Efeito do ambiente, não do app (08-licoes, T5 cap. 10): a cada 100 ms,
# a animação presa começa agora.
ANIM_FIX = ("(()=>{if(window.__animFix)return 'ja';window.__animFix=setInterval(()=>{for(const a of document.getAnimations())"
            "if(a.currentTime!==null&&a.currentTime<0)a.startTime=document.timeline.currentTime},100);return 'anim fix'})()")

class Cap:
    def __init__(s, n, pace=0.5, cps=9, start=(900, 440), setup=None, noscroll=False, sameTab=False):
        s.n = n
        s.words, s.linhas, s.dur, s.estimada = carregar_voz(n)
        s.steps = []
        s.pace, s.cps, s.start = pace, cps, start
        s.noscroll = noscroll
        s.sameTab = sameTab
        s.setup = list(setup or []) + [{'do': 'eval', 'js': OBS}, {'do': 'eval', 'js': ANIM_FIX}]
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

    def hover(s, target, seconds=0.3, at=None, label=None, **kw):
        """hover curto; se atravessa o início de uma linha já pendente, sai partido em dois (a marca entra no meio)"""
        kw.setdefault('optional', True)
        kw.setdefault('timeout', 4)
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

    def digita(s, campo, texto, at_clique, at_texto, label, clique_label=None, **kw):
        """clica no campo (cursor chega na palavra) e digita sem esperar (noClick, cps 40)"""
        s.click(campo, at=at_clique, label=clique_label or f'{label} (campo)')
        return s.type(campo, texto, at=at_texto, label=label, cps=40, noClick=True, **kw)

    def press(s, key, at=None, label=None, **kw):
        return s._p({'do': 'press', 'key': key}, at, label, kw)

    def rolar(s, by, at=None, label=None, ponto=(900, 440), duration=0.5, after=100):
        return s._p({'do': 'scroll', 'point': {'x': ponto[0], 'y': ponto[1]}, 'by': by, 'duration': duration, 'after': after}, at, label, {})

    def cursor(s, ponto, at=None, label=None):
        """leva o cursor a um ponto neutro (scroll de 0 px): tira o mouse de cima de um menu ou de um cartão"""
        return s._p({'do': 'scroll', 'point': {'x': ponto[0], 'y': ponto[1]}, 'by': 0, 'duration': 0.3, 'after': 0}, at, label, {})

    def aponta(s, ponto, at, label):
        """passeio: leva o cursor a um ponto fixo da tela (posições medidas na exploração, rec/t20/_ex); ~0,6 s contra ~1,5 s de um hover"""
        return s.cursor(ponto, at=round(max(0.0, at), 2), label=label)

    def registra(s, target, at=None, label=None):
        """registra o retângulo do alvo para a câmera (zoom/destaque) SEM mexer o mouse"""
        return s._p({'do': 'type', 'target': target, 'text': '', 'noClick': True, 'optional': True, 'timeout': 4}, at, label, {})

    def clicar_fixo(s, alvo, ponto, js, at, label):
        """Botão FIXO fora da faixa y 96..730: leva o cursor com `scroll by 0 point`, registra o retângulo do `alvo` e clica por `eval`."""
        s._p({'do': 'scroll', 'point': {'x': ponto[0], 'y': ponto[1]}, 'by': 0, 'duration': 0.3, 'after': 0}, round(max(0.0, at - 0.6), 2), label + ' (cursor)', {})
        s.add({'do': 'type', 'target': alvo, 'text': '', 'noClick': True, 'label': label, 'optional': True, 'timeout': 4})
        return s._p({'do': 'eval', 'js': js}, round(at, 2), label + ' (clique)', {})

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

    def confere_kpi(s, pares, label, rotulos='main *'):
        """LÊ cada cartão de número pelo rótulo (folha com o texto exato, entre os `rotulos`) e compara o número com o que a fala diz"""
        js = ("(async()=>{const pares=%s;let out='';for(let i=0;i<22;i++){const falta=[];for(const [rot,val] of pares){"
              "const el=[...document.querySelectorAll(" + json.dumps(rotulos) + ")].find(e=>e.children.length===0&&e.textContent.trim()===rot);"
              "if(!el){falta.push(rot+'=?');continue;}let c=el.parentElement,ok=false;for(let k=0;k<4&&c;k++,c=c.parentElement){"
              "const ls=c.innerText.split('\\n').map(x=>x.trim()).filter(Boolean);if(ls.length>1){ok=ls.includes(val);if(!ok)falta.push(rot+'='+ls.filter(x=>x!==rot).slice(0,2).join('/'));break;}}"
              "}if(!falta.length)return 'OK: '+pares.map(p=>p.join(' ')).join(' | ');out='DIFERENTE: '+falta.join(' | ');"
              "await new Promise(r=>setTimeout(r,300));}return out})()") % json.dumps(pares, ensure_ascii=False)
        return s.add({'do': 'eval', 'js': js, 'label': 'confere ' + label})

    def confere_item(s, sel, item, esperados, label):
        """LÊ o primeiro `sel` cujo texto tem `item` e compara com o que a fala diz"""
        esp = [esperados] if isinstance(esperados, str) else list(esperados)
        js = ("(async()=>{const esp=%s;let out='';for(let i=0;i<22;i++){const el=[...document.querySelectorAll(%s)].find(e=>e.innerText.includes(%s));"
              "if(!el){out='DIFERENTE: sem '+%s;}else{const t=el.innerText.replace(/\\s+/g,' ');const falta=esp.filter(e=>!t.includes(e));"
              "if(!falta.length)return 'OK: '+%s+' '+esp.join(' | ');out='DIFERENTE: faltou '+JSON.stringify(falta)+' em: '+t.slice(0,200);}"
              "await new Promise(r=>setTimeout(r,300));}return out})()") % (json.dumps(esp, ensure_ascii=False), json.dumps(sel), json.dumps(item),
                                                                           json.dumps(item), json.dumps(item))
        return s.add({'do': 'eval', 'js': js, 'label': 'confere ' + label})

    def fim(s):
        s.flush(1e9)
        s.steps.append({'do': 'eval', 'js': 'JSON.stringify(window.__avisos || "sem observador")', 'label': 'avisos de erro na tela'})
        s.steps.append({'do': 'mark', 'name': 'FIM', 'at': round(s.dur, 2)})

    def out(s):
        d = {
            'name': f't20-cap{s.n:02d}',
            'title': f'T20 · Cap. {s.n} · {NOMES[s.n]} (narração {str(round(s.dur, 1)).replace(".", ",")} s{" ESTIMADA" if s.estimada else ""}; '
                     f'marcas L1..L{len(s.linhas)} = início de cada linha do roteiro; FAKE_NOW {FAKE_NOW[s.n]})',
            'seed': f't20-cap{s.n:02d}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
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
LINK = lambda n, **kw: {'role': 'link', 'name': n, 'exact': True, **kw}
TAB = lambda n, **kw: {'role': 'tab', 'name': n, 'exact': True, **kw}
TXT = lambda t, **kw: {'text': t, 'exact': True, **kw}
TXTX = lambda t, **kw: {'text': t, **kw}
SEL = lambda s, **kw: {'selector': s, **kw}
OPT = lambda n, **kw: {'role': 'option', 'name': n, 'exact': True, **kw}
PH = lambda p, **kw: {'placeholder': p, **kw}
DLG = '[role=dialog]'
MENU = 'aside, [data-sidebar=sidebar]'
CARTAO = lambda num: f"main div.cursor-pointer.rounded-2xl:has(span.font-semibold:text-is('#{num}'))"     # cartão #N do quadro
COLUNA = lambda titulo: f"main div:has(> div :text-is('{titulo}'))"


def js_clicar(sel, texto=None):
    """clique por eval (botão fixo): o primeiro `sel` visível (com o texto, se dado)"""
    filtro = f"&&(b.textContent||'').includes({json.dumps(texto)})" if texto else ''
    return (f"(()=>{{const b=[...document.querySelectorAll({json.dumps(sel)})].find(b=>b.offsetParent!==null{filtro});"
            "if(!b)return 'SEM ALVO';b.click();return 'clicado'})()")



# ---------------------------------------------------------------- alvos do sistema (Clientes e Fornecedores: conferidos no T4, rec/t04/gerar.py)
ITEM = lambda n, **kw: {'role': 'menuitem', 'name': n, **kw}
MAIN = 'main'
TOGGLE = SEL('header button.h-8.w-8')                                                # recolher/abrir o menu lateral (sem rótulo)
ABA = lambda n: SEL(f"main div.no-scrollbar > button:has-text('{n}')")               # abas da tela (MobilePillTabs: <button>, não role=tab)
LINHA = lambda nome: SEL(f"main aside button:has-text('{nome}')")                    # a linha da lista (o <button> inteiro)
ABA_FICHA = lambda n: SEL(f"[aria-label='Seções da ficha'] button:has-text('{n}')")
BUSCA = lambda tipo: {'placeholder': f'Buscar {tipo}...'}
FICHA_DE = lambda nome: f"main section[aria-label='Detalhes de {nome}']"
BTN_FICHA = lambda nome, b, **kw: BTN(b, within=FICHA_DE(nome), **kw)
COOP = 'Cooperativa Recomeço'
FC = FICHA_DE(COOP)
SALVAR = BTN('Salvar', within=DLG)
LOGIN = [{'do': 'waitFor', 'target': {'label': 'E-mail'}, 'timeout': 30},
         {'do': 'type', 'target': {'label': 'E-mail'}, 'text': '$TUT_USER', 'cps': 40},
         {'do': 'type', 'target': {'label': 'Senha', 'exact': True}, 'text': '$TUT_SENHA', 'cps': 40},
         {'do': 'click', 'target': {'role': 'button', 'name': 'Entrar', 'exact': True}},
         {'do': 'waitFor', 'text': 'Olá, Rafael!', 'timeout': 30}, {'do': 'waitFor', 'idle': True}]
AGUARDA = {'do': 'waitFor', 'idle': True}
RECOLHE = [{'do': 'click', 'target': TOGGLE}, {'do': 'wait', 'seconds': 0.8}]


def setup_tela(aba=None, ficha=None, extra=(), recolhe=True):
    """login, a tela Clientes e Fornecedores (menu recolhido), a aba do capítulo e (opcional) a ficha de um parceiro aberta"""
    s = list(LOGIN) + [{'do': 'goto', 'url': '/clientes-fornecedores'}, {'do': 'waitFor', 'text': 'Aços Quiririm Ltda', 'timeout': 30}, AGUARDA]
    if recolhe:
        s += RECOLHE
    if aba and aba != 'Clientes':
        s += [{'do': 'click', 'target': ABA(aba)}, {'do': 'waitFor', 'target': BUSCA('fornecedor' if aba == 'Fornecedores' else 'cliente'), 'timeout': 15}, AGUARDA]
    if ficha:
        s += [{'do': 'click', 'target': LINHA(ficha)}, {'do': 'waitFor', 'target': SEL(f"main section[aria-label='Detalhes de {ficha}']"), 'timeout': 15}, AGUARDA]
    return s + list(extra)


def js_colar(texto):
    """cola o texto no campo em foco (execCommand insertText: o React recebe o input), ~0,05 s em vez de digitar letra a letra"""
    return ("(()=>{const e=document.activeElement;if(!e||!/^(INPUT|TEXTAREA)$/.test(e.tagName))return 'SEM ALVO (nada em foco)';"
            f"document.execCommand('insertText',false,{json.dumps(texto)});return e.value}})()")


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



# ================================================================ alvos do portal (EntityPortal.tsx 1.59.154)
TABP = lambda k: SEL(f'#tab-btn-{k}')                                       # barra lateral do portal: historico, saldo, notas, relatorio, coletas
SAIR = SEL("button[title='Sair']")
ATUALIZAR = SEL("button[title='Atualizar dados']")
IMPRESSORA = lambda linha: SEL(f"main tbody tr:has-text('{linha}') button[title='Gerar comprovante']")
LINHA_PEDIDO = lambda texto: SEL(f"main tbody tr:has-text('{texto}')", nth=0)
COMPRA_0611 = "R$ 3.700,00"                                                  # a compra de 06/11 da cooperativa (a única de R$ 3.700,00)
POPS = "(()=>{const o=window.open;window.__pops=[];window.open=function(...a){const w=o.apply(this,a);window.__pops.push(w);return w};return 'ok'})()"
# o PDF do comprovante que o app abre na janela nova (a gravação filma uma aba só): base64 no actions.json, para a ilustração da edição (molde T8)
PDF_JS = ("(async()=>{const w=(window.__pops||[]).slice(-1)[0];if(!w)return 'SEM JANELA';for(let i=0;i<40;i++){let f=null;"
          "try{f=w.document&&w.document.querySelector('#pdf-frame')}catch(e){return 'ERRO '+e}"
          "if(f&&f.src){const b=await (await fetch(f.src.split('#')[0])).blob();const u=new Uint8Array(await b.arrayBuffer());let s='';"
          "for(let k=0;k<u.length;k+=8192)s+=String.fromCharCode.apply(null,u.subarray(k,k+8192));return 'PDF:'+btoa(s)}"
          "await new Promise(r=>setTimeout(r,250))}return 'SEM PDF'})()")
USUARIO_PORTAL = 'cooperativa.recomeco'


def portal_entra(url, senha=False):
    """abre o portal `url`; com `senha`, entra pelo formulário "Acesso restrito" (usuário + $PORTAL_SENHA do ambiente; a senha nunca vai para arquivo)"""
    s = [{'do': 'goto', 'url': url}]
    if not senha:
        return s + [{'do': 'waitFor', 'text': 'Portal do Cliente', 'timeout': 30}, AGUARDA, {'do': 'wait', 'seconds': 0.8}]
    return s + [{'do': 'waitFor', 'text': 'Acesso restrito', 'timeout': 30}, {'do': 'click', 'target': SEL('#portal-user')},
                {'do': 'type', 'target': SEL('#portal-user'), 'text': USUARIO_PORTAL, 'cps': 40, 'noClick': True},
                {'do': 'click', 'target': SEL('#portal-pass')},
                {'do': 'type', 'target': SEL('#portal-pass'), 'text': '$PORTAL_SENHA', 'cps': 40, 'noClick': True},
                {'do': 'click', 'target': BTN('Entrar')}, {'do': 'waitFor', 'text': 'Histórico de Pedidos', 'timeout': 30}, AGUARDA, {'do': 'wait', 'seconds': 0.8}]


def editar_portal(nome=COOP):
    """setup: Editar do parceiro > aba Portal (fora do vídeo)"""
    return [{'do': 'click', 'target': BTN_FICHA(nome, 'Editar')}, {'do': 'waitFor', 'text': 'Editar Fornecedor', 'timeout': 15},
            {'do': 'click', 'target': TAB('Portal', within=DLG)}, {'do': 'waitFor', 'text': 'O que exibir no portal', 'timeout': 15}, AGUARDA,
            {'do': 'wait', 'seconds': 0.6}]


def setup_sistema(extra=(), ficha=True, recolhe=True):
    return setup_tela('Fornecedores', COOP if ficha else None, extra, recolhe=recolhe)


def cap_(n, setup, start=(900, 440), **kw):
    return Cap(n, setup=setup, start=start, **kw)


def troca_para(c, url, at, label, espera):
    """troca de navegador (corte na edição): vai a outra rota do mesmo app e espera o texto `espera`"""
    c._p({'do': 'goto', 'url': url}, at, label, {})
    c.waitfor(text=espera, timeout=30)
    c.waitfor(idle=True, timeout=25)


# ================================================================ capítulos
@capitulo
def cap00():
    """Abertura: Dashboard sob a ilustração (linhas 1 a 3); na 4 o menu Clientes e Fornecedores, a aba Fornecedores, a ficha da cooperativa e o Acesso ao portal."""
    setup = LOGIN + [{'do': 'goto', 'url': '/dashboard'}, {'do': 'waitFor', 'text': 'Olá, Rafael!', 'timeout': 25}, AGUARDA]
    c = cap_(0, setup, start=(760, 300))
    for i in (1, 2, 3):
        c.mark(i)
    c.mark(4)
    c.hover(SEL("a:has-text('Clientes e Fornecedores')", nth=0), 0.4, at=c.A(4, 'Em', 0.9), label='o cursor desce pelo menu até Clientes e Fornecedores')
    c.click(SEL("a:has-text('Clientes e Fornecedores')", nth=0), at=c.A(4, 'Clientes', 0.6), label='Clientes e Fornecedores (menu lateral)')
    c.waitfor(text='Aços Quiririm Ltda', timeout=15)
    c.click(ABA('Fornecedores'), at=c.A(4, 'Fornecedores,', 0.6), label='aba Fornecedores')
    c.waitfor(target=BUSCA('fornecedor'), timeout=15)
    c.click(LINHA(COOP), at=c.A(4, 'cooperativa,', 0.6), label='clica na Cooperativa Recomeço: a ficha abre em Visão geral')
    c.waitfor(target=SEL(FC), timeout=12)
    rola_ate(c, 'Acesso ao portal', c.A(4, 'ele', 0.9), 'a câmera desce até Acesso ao portal', y=330, dur_ms=800)
    c.hover(SEL("input[aria-label='Link do portal']"), 1.6, at=c.A(4, 'Acesso', 0.5), label='[ZOOM] Acesso ao portal: o link e o botão Copiar (sem clicar)')
    c.mark(5)
    c.mark(6)
    c.cursor((900, 440), at=c.L(6) + 0.5, label='cursor em repouso')
    c.fim()
    return c


@capitulo
def cap01():
    """O que o parceiro vê: o portal da cooperativa (sem senha, tudo visível): cabeçalho, cartão do parceiro, as cinco abas."""
    c = cap_(1, portal_entra(PORTAL_COOP), start=(700, 420))
    c.mark(1)
    c.hover(TXT('Recicla Vale Metais', nth=0), 1.6, at=c.A(1, 'logo,', 0.5), label='[ZOOM] cabeçalho: logo, nome e contato da Recicla Vale')
    c.mark(2)
    c.hover(TXT('Cooperativa Recomeço', nth=0), 1.2, at=c.A(2, 'nome', 0.5), label='[ZOOM] cartão do parceiro: Cooperativa Recomeço, Fornecedor')
    c.mark(3)
    for palavra, aba in [('Histórico,', 'historico'), ('Saldo,', 'saldo'), ('Notas', 'notas'), ('Relatório', 'relatorio'), ('Coletas.', 'coletas')]:
        c.hover(TABP(aba), 0.2, at=c.A(3, palavra, 0.5), label=f'aba {aba} (sem clicar)')
    c.mark(4)
    c.cursor((700, 520), at=c.L(4) + 0.3, label='cursor em repouso (ilustração)')
    c.mark(5)
    c.mark(6)
    c.cursor((700, 380), at=c.L(6) + 0.3, label='plano geral do portal')
    c.fim()
    return c


@capitulo
def cap02():
    """Pegar o link: ficha da cooperativa > Acesso ao portal, Copiar (toast), menu "..." > Portal do Fornecedor, o fim do endereço, Editar > aba Portal."""
    c = cap_(2, setup_sistema(), start=(760, 420))
    c.mark(1)
    rola_ate(c, 'Acesso ao portal', c.L(1) + 0.3, 'a câmera desce até Acesso ao portal', y=330, dur_ms=800)
    c.hover(SEL("input[aria-label='Link do portal']"), 1.6, at=c.A(1, 'Acesso', 0.5), label='[ZOOM] Acesso ao portal: o link e o botão Copiar')
    c.mark(2)
    c.click(BTN('Copiar', within=FC), at=c.A(2, 'Copiar,', 0.6), label='Copiar')
    c.waitfor(text='Link do portal copiado', timeout=8)
    c.mark(3)
    c.ev("(()=>{const e=document.querySelector('main section[aria-label^=\"Detalhes de\"]');e&&e.scrollTo&&e.scrollTo(0,0);return 'ok'})()", at=c.L(3) - 0.9, label='sobe ao cabeçalho da ficha')
    c.hover(SEL(f"button[aria-label='Ações de {COOP}']"), 0.8, at=c.A(3, 'menu', 0.8), label='o "..." do cabeçalho da ficha abre o menu')
    c.hover(ITEM('Portal do Fornecedor'), 1.2, at=c.A(3, 'Portal', 0.6), label='Portal do Fornecedor (sem clicar)')
    c.mark(4)
    c.press('Escape', at=c.L(4) - 0.1, label='fecha o menu')
    rola_ate(c, 'Acesso ao portal', c.L(4) + 0.2, 'a câmera volta ao Acesso ao portal', y=330, dur_ms=700)
    c.hover(SEL("input[aria-label='Link do portal']"), 2.4, at=c.A(4, 'fim', 0.5), label='[ZOOM] o fim do endereço: recicla-vale-metais-cooperativa- e o código')
    c.mark(5)
    c.cursor((900, 520), at=c.L(5) + 0.3, label='cursor em repouso (ilustração)')
    c.mark(6)
    c.click(BTN_FICHA(COOP, 'Editar'), at=c.A(6, 'Editar,', 0.8), label='Editar')
    c.waitfor(text='Editar Fornecedor', timeout=12)
    c.click(TAB('Portal', within=DLG), at=c.A(6, 'Portal.', 0.6), label='aba Portal')
    c.waitfor(text='Link do portal', timeout=10)
    c.hover(TXT('Link do portal', within=DLG), 1.2, at=c.A(6, 'escolhe', 0.5), label='Link do portal (sem clicar em Abrir portal)')
    c.fim()
    return c


@capitulo
def cap03():
    """Escolher as abas: Editar > Portal, "O que exibir no portal" (tudo ligado), os cartões do Histórico, Valores financeiros, as outras abas, A4, Salvar exibição."""
    c = cap_(3, setup_sistema(editar_portal()), start=(760, 420), noscroll=False)
    c.mark(1)
    rola_ate(c, 'O que exibir no portal', c.L(1) + 0.1, 'rola até O que exibir no portal', y=130, dur_ms=800, escopo=DLG)
    c.hover(TXT('Tudo vem ligado. Desligue o que não quiser mostrar neste portal.', within=DLG), 1.2, at=c.A(1, 'tudo', 0.5), label='Tudo vem ligado')
    c.mark(2)
    c.hover(TXT('Aba Histórico', within=DLG), 0.3, at=c.A(2, 'Histórico,', 0.5), label='Aba Histórico')
    c.hover(TXT('Cards de resumo (totais, ticket médio)', within=DLG), 0.3, at=c.A(2, 'cartões', 0.5), label='Cards de resumo')
    c.hover(TXT('Gráfico de materiais', within=DLG), 0.3, at=c.A(2, 'gráfico', 0.5), label='Gráfico de materiais')
    c.hover(TXT('Valores financeiros (preços e totais)', within=DLG), 0.3, at=c.A(2, 'valores', 0.5), label='Valores financeiros')
    c.hover(TXT('Fotos dos pedidos', within=DLG), 0.3, at=c.A(2, 'fotos', 0.5), label='Fotos dos pedidos')
    c.mark(3)
    c.hover(TXT('Valores financeiros (preços e totais)', within=DLG), 2.4, at=c.A(3, 'Valores', 0.5), label='[ZOOM] Valores financeiros (preços e totais) e a chave')
    c.mark(4)
    rola_ate(c, 'Aba Saldo', c.L(4) - 0.9, 'rola até Aba Saldo', y=170, dur_ms=800, escopo=DLG)
    c.hover(TXT('Aba Saldo', within=DLG), 0.3, at=c.A(4, 'Saldo,', 0.5), label='Aba Saldo')
    c.hover(TXT('Aba Notas Fiscais', within=DLG), 0.3, at=c.A(4, 'Notas', 0.5), label='Aba Notas Fiscais')
    c.hover(TXT('Aba Relatório', within=DLG), 0.3, at=c.A(4, 'Relatório,', 0.5), label='Aba Relatório')
    c.hover(TXT('Mostrar valores (R$ e preço médio)', within=DLG), 0.3, at=c.A(4, 'Relatório,', -0.3), label='Mostrar valores (R$ e preço médio)')
    c.hover(TXT('Mostrar aba Coletas', within=DLG), 0.3, at=c.A(4, 'Coletas,', 0.5), label='Mostrar aba Coletas')
    c.hover(TXT('Permitir solicitar coleta', within=DLG), 0.3, at=c.A(4, 'chave.', 0.8), label='Permitir solicitar coleta')
    c.mark(5)
    rola_ate(c, 'Formato do comprovante no portal', c.L(5) - 0.9, 'rola até Formato do comprovante no portal', y=170, dur_ms=800, escopo=DLG)
    c.hover(TXT('Automático (segue o formato da empresa)', within=DLG), 0.5, at=c.A(5, 'comprovante', 0.5), label='Automático (marcado)')
    c.click(SEL(f'{DLG} label[for=rf-a4]'), at=c.A(5, 'A4.', 0.6), label='A4')
    c.mark(6)
    c.click(BTN('Salvar exibição', within=DLG), at=c.A(6, 'Salvar', 0.6), label='Salvar exibição')
    c.waitfor(text='Exibição do portal salva', timeout=10)
    c.mark(7)
    c.mark(8)
    c.cursor((760, 420), at=c.L(7) + 0.5, label='cursor em repouso (ilustração)')
    c.fim()
    return c


@capitulo
def cap04():
    """Usuário e senha: Editar > Portal, Pedir login no portal, Usuário e Senha, Salvar acesso, as pílulas Oculto/Livre/Com senha; o portal vira Acesso restrito; o parceiro entra; Sair."""
    c = cap_(4, setup_sistema(editar_portal()), start=(760, 420))
    c.mark(1)
    rola_ate(c, 'Exigir senha', c.L(1) + 0.1, 'rola até Exigir senha', y=130, dur_ms=800, escopo=DLG)
    c.hover(TXT('Quando ligado, o portal pede usuário e senha antes de mostrar os dados.', within=DLG), 1.2, at=c.A(1, 'Pra', 0.9), label='Exigir senha: a chave Pedir login no portal (desligada)')
    c.mark(2)
    c.click(SEL('#portal-password-enabled'), at=c.A(2, 'Ligo', 0.6), label='liga Pedir login no portal')
    c.waitfor(target=SEL('#portal-username'), timeout=8)
    c.digita(SEL('#portal-username'), USUARIO_PORTAL, c.A(2, 'Usuário,', 0.7), c.A(2, 'nome', 0.05), 'Usuário: cooperativa.recomeco')
    c.click(SEL('#portal-password'), at=c.A(2, 'senha,', 0.6), label='Senha (campo)')
    c.type(SEL('#portal-password'), '$PORTAL_SENHA', at=c.A(2, 'combino', 0.05), label='Senha (pontinhos)', cps=40, noClick=True)
    c.mark(3)
    c.click(BTN('Salvar acesso', within=DLG), at=c.A(3, 'Salvar', 0.6), label='Salvar acesso')
    c.waitfor(text='Acesso salvo', timeout=10)
    c.mark(4)
    rola_ate(c, 'O que exibir no portal', c.L(4) - 0.6, 'rola até O que exibir no portal', y=130, dur_ms=800, escopo=DLG)
    c.hover(SEL(f"{DLG} [role=radiogroup][aria-label='Aba Histórico']"), 2.2, at=c.A(4, 'cada', 0.5), label='[ZOOM] as pílulas Oculto, Livre e Com senha da Aba Histórico')
    c.mark(5)
    c.cursor((760, 420), at=c.L(5) + 0.3, label='cursor em repouso (ilustração)')
    c.mark(6)
    troca_para(c, PORTAL_COOP, c.L(6) - 0.6, 'navegador do parceiro: abre o link da cooperativa', 'Acesso restrito')
    c.hover(TXT('Acesso restrito'), 1.2, at=c.A(6, 'Acesso', 0.5), label='Acesso restrito')
    c.mark(7)
    c.click(SEL('#portal-user'), at=c.A(7, 'usuário', 0.8), label='Usuário (campo)')
    c.type(SEL('#portal-user'), USUARIO_PORTAL, at=c.A(7, 'usuário', 0.05), label='Usuário: cooperativa.recomeco', cps=40, noClick=True)
    c.click(SEL('#portal-pass'), at=c.A(7, 'senha,', 0.6), label='Senha (campo)')
    c.type(SEL('#portal-pass'), '$PORTAL_SENHA', at=c.A(7, 'senha,', 0.05), label='Senha (pontinhos)', cps=40, noClick=True)
    c.click(BTN('Entrar'), at=c.A(7, 'Entrar,', 0.6), label='Entrar')
    c.waitfor(text='Histórico de Pedidos', timeout=20)
    c.mark(8)
    c.hover(SAIR, 2.2, at=c.A(8, 'ícone.', 0.9), label='[ZOOM] o ícone Sair no cartão do parceiro (sem clicar)')
    c.fim()
    return c


def setup_portal_coop(sistema=False, extra=()):
    """setup dos capítulos 5 a 10: (opcional) login do Rafael no sistema, e o portal da cooperativa com a sessão já aberta (fora do vídeo)"""
    return (list(LOGIN) if sistema else []) + portal_entra(PORTAL_COOP, senha=True) + list(extra)


@capitulo
def cap05():
    """Histórico de pedidos: cartões, gráfico, a compra de 06/11 com os materiais e as fotos; o portal da Fundição (venda sem valor)."""
    c = cap_(5, setup_portal_coop(), start=(900, 440))
    c.mark(1)
    c.hover(TXT('Total Comprado'), 1.0, at=c.A(1, 'cartões,', 0.5), label='[ZOOM] os três cartões do Histórico (linhas 1 e 2)')
    c.mark(2)
    c.hover(TXT('Total de Pedidos'), 1.0, at=c.A(2, 'quinze', 0.5), label='Total de Pedidos: 15')
    c.mark(3)
    rola_ate(c, 'Top 5 Materiais Mais Comprados', c.L(3) - 0.5, 'desce ao gráfico', y=140, dur_ms=800)
    c.hover(TXTX('Papelão: 55%'), 0.3, at=c.A(3, 'papelão', 0.5), label='Papelão: 55%')
    c.hover(TXTX('Plástico PET: 17%'), 0.3, at=c.A(3, 'PET', 0.5), label='Plástico PET: 17%')
    c.hover(TXTX('Alumínio latinha: 15%'), 0.3, at=c.A(3, 'latinha.', 0.5), label='Alumínio latinha: 15%')
    c.mark(4)
    rola_ate(c, 'Histórico de Pedidos', c.L(4) - 0.5, 'desce ao Histórico de Pedidos', y=150, dur_ms=800)
    c.click(LINHA_PEDIDO(COMPRA_0611), at=c.A(4, 'sexta,', 0.7), label='clica na compra de 06/11')
    c.waitfor(text='Total do Pedido:', timeout=10)
    c.mark(5)
    rola_ate(c, 'Fotos do pedido', c.L(5) - 0.5, 'desce às fotos do pedido', y=360, dur_ms=800)
    c.click(SEL("main button:has(img[src*='order-attachments'])", nth=0), at=c.A(5, 'fotos', 0.7), label='abre a primeira foto em tela cheia')
    c.press('Escape', at=c.A(5, 'pedido.', 0.0), label='fecha a foto')
    c.mark(6)
    troca_para(c, PORTAL_FUND, c.L(6) - 0.6, 'outra aba do navegador do parceiro: o portal da Fundição Bandeira do Vale', 'Total Vendido')
    c.hover(TXT('Fundição Bandeira do Vale', nth=0), 1.0, at=c.A(6, 'Fundição', 0.5), label='Fundição Bandeira do Vale (Cliente)')
    c.mark(7)
    rola_ate(c, 'Histórico de Pedidos', c.L(7) - 0.5, 'desce ao Histórico de Pedidos', y=150, dur_ms=800)
    c.hover(SEL("main tbody tr:has-text('R$ 0,00') [aria-label='Valores deste comprovante estão ocultos']", nth=0), 1.8, at=c.A(7, 'zero', 0.5),
            label='[ZOOM] R$ 0,00 e o cadeado')
    c.mark(8)
    c.click(SEL("main tbody tr:has-text('R$ 0,00')", nth=0), at=c.A(8, 'pedido', 0.7), label='abre a venda de hoje')
    c.waitfor(text='Total do Pedido:', timeout=10)
    c.hover(TXT('Cobre mel', nth=0), 1.0, at=c.A(8, 'cobre', 0.5), label='latão e cobre mel com o peso e R$ 0,00')
    c.fim()
    return c


@capitulo
def cap06():
    """O saldo do parceiro: Saldo R$ 1.350,00 a receber, o extrato; no sistema o Pix de R$ 1.350,00; de volta ao portal, Em dia; Atualizar dados."""
    c = cap_(6, setup_portal_coop(sistema=True), start=(900, 440))
    c.mark(1)
    c.click(TABP('saldo'), at=c.A(1, 'saldo', 0.7), label='aba Saldo')
    c.waitfor(text='Saldo Atual', timeout=10)
    c.confere('main', ['R$ 1.350,00', 'Você tem a receber'], 'Saldo Atual R$ 1.350,00 a receber')
    c.hover(TXT('Saldo Atual'), 2.0, at=c.A(1, 'mil', 0.5), label='[ZOOM] o valor R$ 1.350,00, o selo e a frase')
    c.mark(2)
    c.mark(3)
    rola_ate(c, 'Histórico de Movimentações', c.L(3) - 0.5, 'desce ao extrato', y=150, dur_ms=800)
    c.hover(SEL("main tbody tr:has-text('Pedido')", nth=0), 0.6, at=c.A(3, 'entrega', 0.5), label='linha de Pedido')
    c.hover(SEL("main tbody tr:has-text('Pagamento')", nth=0), 0.6, at=c.A(3, 'pagamento,', 0.5), label='linha de Pagamento')
    c.mark(4)
    troca_para(c, '/clientes-fornecedores', c.L(4) - 3.2, 'navegador do sistema: Clientes e Fornecedores (corte)', 'Aços Quiririm Ltda')
    c.click(ABA('Fornecedores'), at=c.L(4) - 1.4, label='aba Fornecedores')
    c.click(LINHA(COOP), at=c.L(4) - 0.4, label='Cooperativa Recomeço')
    c.waitfor(target=SEL(FC), timeout=12)
    c.click(ABA_FICHA('Conta-corrente'), at=c.L(4) + 0.6, label='aba Conta-corrente')
    c.waitfor(text='Saldo Atual', timeout=12)
    c.click(BTN('Movimentação', within=FC), at=c.A(4, 'Movimentação,', 0.7), label='Movimentação')
    c.waitfor(text='Nova Movimentação de Saldo', timeout=10)
    c.digita(SEL(f'{DLG} #amount'), '1350', c.A(4, 'pago', 0.7), c.A(4, 'mil', 0.05), '[ZOOM] Valor R$ 1.350,00')
    c.click(SEL(f'{DLG} #description'), at=c.A(4, 'reais', 0.7), label='Observação (campo)')
    c.ev(js_colar('Acerto da entrega de 06/11'), at=c.A(4, 'reais', 0.0), label='Observação: Acerto da entrega de 06/11 (colado)')
    c.hover(TXT('Pix/Transferência', within=DLG), 0.6, at=c.A(4, 'Pix.', 0.5), label='Pix/Transferência')
    c.mark(5)
    c.click(BTN('Confirmar', within=DLG), at=c.A(5, 'Confirmar,', 0.6), label='Confirmar')
    c.waitfor(text='Movimentação registrada com sucesso!', timeout=12)
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.confere(FC, ['R$ 0,00'], 'Saldo Atual R$ 0,00 no sistema')
    c.hover(TXT('Saldo Atual', within=FC), 1.4, at=c.A(5, 'zerou', 0.5), label='zoom: Saldo Atual R$ 0,00')
    c.mark(6)
    troca_para(c, PORTAL_COOP, c.L(6) - 0.2, 'navegador do parceiro: volta ao portal da cooperativa', 'Histórico de Pedidos')
    c.click(TABP('saldo'), at=c.L(6) + 0.8, label='aba Saldo')
    c.waitfor(text='Saldo Atual', timeout=10)
    c.confere('main', ['R$ 0,00', 'Em dia'], 'Saldo Atual R$ 0,00 Em dia no portal')
    c.hover(TXT('Em dia', nth=0), 2.0, at=c.A(6, 'dia.', 0.5), label='[ZOOM] o saldo R$ 0,00, o selo Em dia e a frase')
    c.mark(7)
    c.hover(ATUALIZAR, 2.4, at=c.A(7, 'botão', 0.6), label='[ZOOM] o ícone Atualizar dados (sem clicar)')
    c.fim()
    return c


@capitulo
def cap07():
    """Notas e relatório: NF-e 1250 da Fundição; na cooperativa o Relatório de Mês passado, o total R$ 18.755,00 e o Baixar PDF (sem clicar)."""
    setup = portal_entra(PORTAL_COOP, senha=True) + portal_entra(PORTAL_FUND)
    c = cap_(7, setup, start=(900, 440))
    c.mark(1)
    c.click(TABP('notas'), at=c.A(1, 'Notas', 0.7), label='aba Notas Fiscais')
    c.waitfor(text='Autorizada', timeout=10)
    c.confere('main', ['1250', 'R$ 23.950,00', 'Autorizada'], 'NF-e 1250')
    c.hover(SEL("main tbody tr:has-text('1250')", nth=0), 1.6, at=c.A(1, 'mil', 0.5), label='[ZOOM] o número 1250 e o valor')
    c.mark(2)
    c.hover(TXT('Série'), 0.5, at=c.A(2, 'série,', 0.5), label='a tabela inteira (Tipo, Nº, Série, Data, Valor, Status)')
    c.mark(3)
    troca_para(c, PORTAL_COOP, c.L(3) - 1.6, 'navegador da cooperativa (com sessão, corte)', 'Histórico de Pedidos')
    c.click(TABP('relatorio'), at=c.A(3, 'Relatório', 0.7), label='aba Relatório')
    c.waitfor(text='Relatório por Material', timeout=10)
    c.mark(4)
    c.click(TXTX('Últimos 30 dias', nth=0), at=c.A(4, 'escolho', 0.8), label='Período')
    c.click(OPT('Mês passado'), at=c.A(4, 'passado.', 0.7), label='Mês passado')
    c.waitfor(text='Papelão', timeout=10)
    c.hover(SEL("main tbody tr:has-text('Papelão')", nth=0), 0.8, at=c.A(4, 'papelão', 0.5), label='papelão: oito mil e quatrocentos quilos')
    c.hover(SEL("main tbody tr:has-text('PET')", nth=0), 0.8, at=c.A(4, 'PET,', 0.5), label='PET: dois mil e seiscentos')
    c.mark(5)
    c.hover(SEL("main tfoot tr, main tr:has-text('Total')", nth=-1), 2.0, at=c.A(5, 'No', 0.3), label='[ZOOM] a linha Total: R$ 18.755,00')
    c.mark(6)
    c.hover(BTN('Baixar PDF'), 2.4, at=c.A(6, 'Baixar', 0.6), label='[ZOOM] o botão Baixar PDF (sem clicar)')
    c.fim()
    return c


@capitulo
def cap08():
    """O parceiro pede a coleta: aba Coletas, Solicitar coleta (material, quantidade, data, período, observações), a solicitação enviada; o sino do sistema."""
    c = cap_(8, setup_portal_coop(sistema=True), start=(900, 440))
    c.mark(1)
    c.click(TABP('coletas'), at=c.A(1, 'Coletas', 0.7), label='aba Coletas')
    c.waitfor(text='Minhas coletas', timeout=10)
    c.hover(TXT('Minhas coletas'), 1.2, at=c.A(1, 'sozinha.', 1.0), label='Minhas coletas')
    c.mark(2)
    c.click(BTN('Solicitar coleta'), at=c.A(2, 'Solicitar', 0.8), label='Solicitar coleta')
    c.waitfor(target=SEL('#coleta-material'), timeout=10)
    c.mark(3)
    c.digita(SEL('#coleta-material'), 'Papelão e PET prensados', c.A(3, 'material,', 0.9), c.A(3, 'papelão', 0.05), 'Material: Papelão e PET prensados')
    c.digita(SEL('#coleta-qtd'), '2.500 kg', c.A(3, 'quantidade,', 0.9), c.A(3, 'dois', 0.05), '[ZOOM] Quantidade estimada: 2.500 kg')
    c.mark(4)
    c.click(SEL('#coleta-data'), at=c.A(4, 'dia', 0.8), label='Data preferida (campo)')
    c.type(SEL('#coleta-data'), '12112026', at=c.A(4, 'quinta', 0.3), label='Data preferida 12/11/2026', cps=40, noClick=True)
    c.click(SEL('#coleta-janela'), at=c.A(4, 'manhã.', 0.9), label='abre Período')
    c.click(OPT('Manhã'), at=c.A(4, 'manhã.', 0.1), label='Período: Manhã')
    rola_ate(c, 'Endereço da coleta', c.A(4, 'endereço', 0.5), 'desce ao Endereço da coleta (do cadastro)', y=170, dur_ms=700, escopo=DLG)
    c.click(SEL('#coleta-obs'), at=c.A(4, 'observações,', 0.7), label='Observações (campo)')
    c.type(SEL('#coleta-obs'), 'Os fardos ficam na doca do galpão.', at=c.A(4, 'fardos.', 1.0), label='Observações: Os fardos ficam na doca do galpão.', cps=40, noClick=True)
    c.mark(5)
    c.click(BTN('Solicitar coleta', within=DLG), at=c.A(5, 'Solicitar', 0.7), label='Solicitar coleta (enviar)')
    c.waitfor(text='Solicitação enviada', timeout=10)
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.hover(SEL("main :text-is('Solicitada')", nth=0), 1.2, at=c.A(5, 'entra', 0.5), label='[ZOOM] o cartão da nova coleta com o selo Solicitada')
    c.mark(6)
    c.ev("(()=>{location.assign('/dashboard');return 'recarrega o sistema'})()", at=c.L(6) - 0.6, label='navegador do sistema: recarrega a tela (sem realtime no falso)')
    c.waitfor(text='Olá, Rafael!', timeout=30)
    c.waitfor(idle=True, timeout=25)
    c.click(SEL("button[aria-label^='Notificações'], button[aria-label*='notificações não lidas']", nth=0), at=c.A(6, 'sino:', 0.8), label='o sino de notificações')
    c.waitfor(text='Nova solicitação de coleta', timeout=10)
    c.hover(TXT('Nova solicitação de coleta', nth=0), 1.6, at=c.A(6, 'solicitação', 0.4), label='[ZOOM] Nova solicitação de coleta no sino')
    c.mark(7)
    c.press('Escape', at=c.L(7) + 0.3, label='fecha o sino')
    c.fim()
    return c


@capitulo
def cap09():
    """O comprovante do portal: a impressora da compra de 06/11 abre o comprovante A4 em janela nova (capturado em base64 para a ilustração)."""
    c = cap_(9, setup_portal_coop(extra=[{'do': 'eval', 'js': POPS}]), start=(900, 440))
    c.mark(1)
    rola_ate(c, 'Histórico de Pedidos', c.L(1) - 0.1, 'desce ao Histórico de Pedidos', y=150, dur_ms=700)
    c.hover(IMPRESSORA(COMPRA_0611), 1.0, at=c.A(1, 'impressora', 0.5), label='a impressora Gerar comprovante da compra de 06/11')
    c.mark(2)
    c.click(IMPRESSORA(COMPRA_0611), at=c.L(2) - 0.2, label='clica na impressora: abre o comprovante A4 na janela nova')
    c.ev(PDF_JS, at=c.L(2) + 2.5, label='PDF do comprovante A4 (janela nova, para a ilustração)')
    c.mark(3)
    c.mark(4)
    c.cursor((900, 440), at=c.L(4) + 0.3, label='de volta ao portal')
    c.fim()
    return c


@capitulo
def cap10():
    """As fotos do pedido: a página pública /fotos/ da compra de 06/11: cabeçalho, carrossel (Próxima foto, tela cheia), Dados do Pedido."""
    c = cap_(10, [{'do': 'goto', 'url': FOTOS_1749}, {'do': 'waitFor', 'text': 'Fotos do pedido', 'timeout': 30}, AGUARDA, {'do': 'wait', 'seconds': 0.8}], start=(900, 440))
    c.mark(1)
    c.mark(2)
    c.mark(3)
    c.hover(TXT('Fotos do pedido', nth=0), 1.2, at=c.A(3, 'Em', 0.9), label='cabeçalho: Recicla Vale Metais e Fotos do pedido')
    c.hover(TXT('Fotos', nth=0), 1.2, at=c.A(3, 'fotos', 0.5), label='Fotos (carrossel)')
    c.mark(4)
    c.click(SEL("button[aria-label='Próxima foto']", nth=0), at=c.A(4, 'passar', 0.7), label='Próxima foto')
    c.click(SEL("button[aria-label='Próxima foto']", nth=0), at=c.A(4, 'outra,', 0.7), label='Próxima foto')
    c.click(SEL("button:has(img[src*='order-attachments'])", nth=0), at=c.A(4, 'abrir', 0.7), label='abre a foto em tela cheia')
    c.press('Escape', at=c.A(4, 'cheia.', -0.2), label='fecha a foto')
    c.mark(5)
    rola_ate(c, 'Dados do Pedido', c.L(5) - 0.5, 'desce a Dados do Pedido', y=150, dur_ms=800)
    c.hover(TXT('Total', nth=0), 1.8, at=c.A(5, 'total:', 0.5), label='[ZOOM] Total R$ 3.700,00')
    c.mark(6)
    c.mark(7)
    c.cursor((900, 440), at=c.L(7) + 0.3, label='cursor em repouso')
    c.fim()
    return c


@capitulo
def cap11():
    """Recapitulando: montagem das gravações dos capítulos 0 a 10, sem robô (só o relógio das marcas)."""
    c = cap_(11, [], start=(900, 440))
    for i in range(1, len(c.linhas) + 1):
        c.mark(i)
    c.fim()
    return c


def main():
    quais = [int(a) for a in sys.argv[1:] if a.isdigit()] or sorted(k for k in CAPS_ROBO if k != 11)
    for n in quais:
        if n == 11:
            continue
        c = CAPS_ROBO[n]()
        caminho = os.path.join(HERE, f'cap{n:02d}.json')
        json.dump(c.out(), open(caminho, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
        print(f'cap{n:02d}: {len(c.steps)} passos, narração {c.dur:.1f} s -> {caminho}')


if __name__ == '__main__':
    main()
