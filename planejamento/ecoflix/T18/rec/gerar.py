#!/usr/bin/env python3
"""T18 · Ambiental: MTR e CDF: gera rec/t18/cap00..cap10.json (roteiros do robô) a partir da voz (t18/narracao/capNN.json).

EcoSistema 1.59.154 no Supabase falso (mundo da Recicla Vale Metais), computador 1280x800, logado como Rafael Nogueira (MASTER).
Cada passo é preso a uma palavra da fala: `at` = início da palavra - folga (o custo do gesto, docs/04 "Custo real dos gestos"), e a marca
Ln entra no início de cada linha. Quando a voz chegar, rodar de novo com o capNN.json da voz (nada a reescrever).
Rodar de qualquer pasta: `python3 -I rec/t18/gerar.py [NN ...]`; ensaiar/gravar: `bash rec/t18/t18_job.sh NN r|c`.

Dois relógios (plano.md): FAKE_NOW 10/11/2026 09:30 nos capítulos 0 a 5 (depois das NF-e do T16 e do T17; o MTR da carga sai às 09:3x)
e 10:40 do 6 ao 10 (o MTR da tarde, 2611000325, foi emitido às 09:40 pelo modelo).
Cadeia de sementes (rec/mundo/seeds-extra/t18; `t18_sementes.py` escreve inicio e, com --cadeia, as apos-capNN sintéticas; cumulativas):
inicio (NF-e 1254 da chaparia) -> apos-cap03 (acesso validado, listas, resíduo "Sucata de ferro" ligado aos três ferros)
-> apos-cap04 (parceiros e MTR 2611000318 emitido) -> apos-cap05 (MTR 2611000325 emitido) -> apos-cap06 (325 cancelado)
-> apos-cap07 (CDF 2611000041 emitido). Os capítulos 8 a 10 só leem; o 10 é a montagem (o robô deixa a tela parada com as marcas).
As ilustrações (cap01, cap02, partes do 0, 5, 7, 8 e 9) são de outro agente: nesses trechos o cursor fica em repouso.
"""
import hashlib
import json
import os
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TUT = os.path.normpath(os.path.join(HERE, '..', '..'))
NARR = os.path.join(TUT, 't18', 'narracao')
N0930 = '2026-11-10T09:30:00-03:00'
N1040 = '2026-11-10T10:40:00-03:00'
FAKE_NOW = {n: (N0930 if n <= 5 else N1040) for n in range(11)}


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
HOJE = '2026-11-10'
STORAGE = {
    'app_version': VERSAO, 'notification_shown_version': VERSAO, f'dominex:daily-tasks-shown:{RAFAEL}': HOJE,
    'pwa-install-dismissed': 'true', 'theme': 'light', f'daily-tasks-reminder-last-shown-{RAFAEL}': HOJE, 'initial-preferences-set': 'true',
}
NOMES = ['Abertura', 'O que é MTR e CDF', 'Licença e fiscalização', 'Acesso e resíduos', 'Emitir o MTR da carga', 'Acompanhar e baixar o PDF',
         'Cancelar um MTR', 'O certificado do destino', 'Baixar e guardar', 'A nota da mesma carga', 'Recapitulando']
SEMENTE = {0: None, 1: None, 2: None, 3: None, 4: 'apos-cap03', 5: 'apos-cap04', 6: 'apos-cap05', 7: 'apos-cap06', 8: 'apos-cap07',
           9: 'apos-cap07', 10: 'apos-cap07'}


def sementes(n):
    """a semente de cada capítulo é cumulativa (tudo desde o início da aula): só a última da cadeia vai junto do início"""
    return ['t18/inicio'] + ([f't18/{SEMENTE[n]}'] if SEMENTE[n] else [])


def norm(s):
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode().lower()
    return ''.join(ch for ch in s if ch.isalnum() or ch in '?')


def carregar_voz(n):
    d = json.load(open(os.path.join(NARR, f'cap{n:02d}.json'), encoding='utf8'))
    return d['words'], d['linhas'], float(d['dur']), bool(d.get('estimado'))


# Observador de avisos de erro na tela (aceite): "Não foi possível", "Erro ao", "Tente novamente", "indisponível", "Algo deu errado",
# "Falha ao", "não encontrad" e a faixa "Lembrete da trilha" da EcoFlix. O passo final devolve a lista (tem de sair vazia).
OBS = ("(()=>{window.__avisos=[];const re=/N[ãa]o foi poss[ií]vel|Erro ao|Tente novamente|indispon[ií]vel|Algo deu errado|Falha ao|"
       "n[ãa]o encontrad|recusou|rejeitad[ao]!/i;"
       "const chk=(t)=>{t=(t||'').trim();const m=t&&t.match(new RegExp('[^]{0,40}('+re.source+')[^]{0,40}','i'));"
       "if(m&&window.__avisos.length<10)window.__avisos.push(m[0].replace(/[\\n\\r\\t ]+/g,' '))};new MutationObserver(ms=>{for(const m of ms){"
       "m.addedNodes.forEach(n=>chk(n.textContent));if(m.type==='characterData')chk(m.target.textContent)}}).observe(document.body,"
       "{childList:true,subtree:true,characterData:true});chk(document.body.innerText);"
       "setInterval(()=>{const f=document.querySelector('section[aria-label^=\"Lembrete da trilha\"]');"
       "if(f&&window.__avisos.length<10&&!window.__avisos.includes('TRILHA ECOFLIX'))window.__avisos.push('TRILHA ECOFLIX')},300);return 1})()")

# Animação do framer-motion presa no futuro pelo relógio simulado (08-licoes, T5 cap. 10): a cada 100 ms, a animação presa começa agora.
ANIM_FIX = ("(()=>{if(window.__animFix)return 'ja';window.__animFix=setInterval(()=>{for(const a of document.getAnimations())"
            "if(a.currentTime!==null&&a.currentTime<0)a.startTime=document.timeline.currentTime},100);return 'anim fix'})()")


class Cap:
    def __init__(s, n, pace=0.5, cps=9, start=(900, 440), setup=None, noscroll=False):
        s.n = n
        s.words, s.linhas, s.dur, s.estimada = carregar_voz(n)
        s.steps = []
        s.pace, s.cps, s.start = pace, cps, start
        s.noscroll = noscroll
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

    def marca_ja(s, i):
        """marca a linha e a solta já (antes de passos sem `at`)"""
        s.mark(i)
        s.flush(1e9)

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
        return s.type(campo, texto, at=None, label=label, cps=40, noClick=True, **kw)   # T18: a digitação segue o clique (sem `at` próprio)

    def colar(s, seletor, texto, at=None, label=None):
        """texto longo sem graça visual: entra de uma vez (execCommand insertText, ~0,05 s; o valor fica no actions.json)"""
        js = ("(()=>{const el=document.querySelector(%s);if(!el)return 'SEM ALVO';el.focus();el.select&&el.select();"
              "document.execCommand('insertText',false,%s);return 'colado: '+el.value.slice(0,60)})()") % (json.dumps(seletor), json.dumps(texto, ensure_ascii=False))
        return s.ev(js, at=at, label=label)

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

    def fim(s):
        s.flush(1e9)
        s.steps.append({'do': 'eval', 'js': 'JSON.stringify(window.__avisos || "sem observador")', 'label': 'avisos de erro na tela'})
        s.steps.append({'do': 'mark', 'name': 'FIM', 'at': round(s.dur, 2)})

    def out(s):
        return {
            'name': f't18-cap{s.n:02d}',
            'title': f'T18 · Cap. {s.n} · {NOMES[s.n]} (narração {str(round(s.dur, 1)).replace(".", ",")} s{" ESTIMADA" if s.estimada else ""}; '
                     f'marcas L1..L{len(s.linhas)} = início de cada linha do roteiro; FAKE_NOW {FAKE_NOW[s.n]})',
            'seed': f't18-cap{s.n:02d}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
            'start': {'x': s.start[0], 'y': s.start[1]},
            'anonymous': True, 'storage': dict(STORAGE),
            'seedExtra': sementes(s.n),
            'prewarm': ['/login'], 'setup': s.setup, 'steps': s.steps,
        }


# ---------------------------------------------------------------- alvos
BTN = lambda n, **kw: {'role': 'button', 'name': n, 'exact': True, **kw}
BTNX = lambda n, **kw: {'role': 'button', 'name': n, **kw}
LINK = lambda n, **kw: {'role': 'link', 'name': n, 'exact': True, **kw}
TAB = lambda n, **kw: {'role': 'tab', 'name': n, 'exact': True, **kw}
TXT = lambda t, **kw: {'text': t, 'exact': True, **kw}
TXTX = lambda t, **kw: {'text': t, **kw}
SEL = lambda s, **kw: {'selector': s, **kw}
OPT = lambda n, **kw: {'role': 'option', 'name': n, 'exact': True, **kw}
OPTX = lambda n, **kw: {'role': 'option', 'name': n, **kw}
ITEM = lambda n, **kw: {'role': 'menuitem', 'name': n, **kw}
PH = lambda p, **kw: {'placeholder': p, **kw}
DLG = '[role=dialog]'
MENU = 'aside, [data-sidebar=sidebar]'
GRUPO = BTNX('Fiscal & Ambiental', within=MENU)
ITEM_MENU = lambda n: LINK(n, within=MENU)


def js_clicar(sel, texto=None):
    """clique por eval (botão fixo): o primeiro `sel` visível (com o texto, se dado)"""
    filtro = f"&&(b.textContent||'').includes({json.dumps(texto, ensure_ascii=False)})" if texto else ''
    return (f"(()=>{{const b=[...document.querySelectorAll({json.dumps(sel)})].find(b=>b.offsetParent!==null{filtro});"
            "if(!b)return 'SEM ALVO';b.click();return 'clicado'})()")


# ---------------------------------------------------------------- setup (fora do vídeo)
LOGIN = [
    {'do': 'waitFor', 'target': PH('seu@email.com'), 'timeout': 40},
    {'do': 'type', 'target': PH('seu@email.com'), 'text': '$TUT_USER', 'cps': 40},
    {'do': 'type', 'target': PH('••••••••'), 'text': '$TUT_SENHA', 'cps': 40},
    {'do': 'click', 'target': BTN('Entrar')},
    {'do': 'waitFor', 'url': '/dashboard', 'timeout': 40},
    {'do': 'waitFor', 'idle': True, 'timeout': 25},
]
ROTA_MTR = '/fiscal-ambiental/ambiental/mtr'
ROTA_CDF = '/fiscal-ambiental/ambiental/cdf'
PAGINAS = {
    '/dashboard': None,
    ROTA_MTR: 'Manifestos de Transporte de Resíduos',
    ROTA_CDF: 'Certificados de Destinação Final',
    '/materiais': None,
    '/fiscal-ambiental/nfe/saida': None,
}


def ir(rota, espera=0.8):
    st = [{'do': 'goto', 'url': rota}]
    if PAGINAS.get(rota):
        st.append({'do': 'waitFor', 'text': PAGINAS[rota], 'timeout': 30})
    return st + [{'do': 'waitFor', 'idle': True, 'timeout': 25}, {'do': 'wait', 'seconds': espera}]


def setup_em(rota, extra=(), aquece=()):
    """login, aquece as rotas que o capítulo visita e para em `rota`"""
    st = list(LOGIN)
    for r in aquece:
        st += ir(r, 0.3)
    return st + ir(rota) + list(extra)


def js_abrir_grupo(grupo, filho):
    """abre o grupo do menu lateral só se o link filho ainda não está no DOM (o grupo da página atual já vem aberto)"""
    return (f"(()=>{{const tem=[...document.querySelectorAll('aside a, [data-sidebar=sidebar] a')].some(a=>a.textContent.trim()==={json.dumps(filho, ensure_ascii=False)});"
            f"if(tem)return 'ja aberto';const b=[...document.querySelectorAll('aside button, [data-sidebar=sidebar] button')].find(b=>b.textContent.trim()==={json.dumps(grupo, ensure_ascii=False)});"
            "if(!b)return 'SEM ALVO';b.click();return 'aberto'})()")


# rolagem suave do contêiner que rola o alvo (molde do T14/T11/T8/T12: ACHA_ROLAGEM + SUAVE): o cursor não se mexe
ACHA_ROLAGEM = ("const rolagem=(el)=>{let c=el&&el.parentElement;while(c&&c!==document.body){const s=getComputedStyle(c);"
                "if(/(auto|scroll)/.test(s.overflowY)&&c.scrollHeight>c.clientHeight+4)return c;c=c.parentElement;}"
                "const se=document.scrollingElement;return se&&se.scrollHeight>se.clientHeight+4?se:null};")
SUAVE = ("await new Promise(res=>{const f=t=>{const p=Math.min(1,(t-t0)/DUR),e=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;c.scrollTo({top:DESTINO,behavior:'instant'});"
         "p<1?requestAnimationFrame(f):res()};requestAnimationFrame(f)});")


def js_ate(texto, y=250, dur_ms=900, escopo='main', prefixo=False):
    """rola (suave) o contêiner do alvo até a folha do DOM cujo texto é `texto` ficar em y px CSS. Devolve o topo final do alvo,
    'ok' (já estava lá), 'SEM ALVO' ou 'SEM ROLAGEM'."""
    alvo = json.dumps(texto, ensure_ascii=False)
    sel = json.dumps(f'{escopo} *')
    busca = (f"[...document.querySelectorAll({sel})].filter(e=>e.offsetParent!==null&&e.textContent.trim().startsWith({alvo})).sort((a,b)=>a.textContent.length-b.textContent.length)[0]"
             if prefixo else f"[...document.querySelectorAll({sel})].find(e=>e.children.length===0&&e.offsetParent!==null&&e.textContent.trim()==={alvo})")
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


# ---------------------------------------------------------------- alvos das telas ambientais (conferidos por exploração, rec/t18/_ex)
NAV = "nav[aria-label='Navegação da seção']"
SUBABA = lambda n: BTN(n, within=NAV)                                                  # sub-abas da seção (MTR/CDF)
NEUTRO = (900, 470)                                                                    # ponto neutro (fora de menu, cartão e botão)
ADLG = '[role=alertdialog]'
LINHA = lambda txt, sub='': SEL(f"main tbody tr:has-text('{txt}') {sub}".strip())
ABA_MTR = lambda n: SEL(f"main div.border-b button:text-is('{n}')")                    # sublinhadas: Manifestos | Configurações
NOVO_MTR_DICA = SEL("main span[tabindex='0']:has-text('Novo MTR')")                    # o botão desligado fica dentro deste span
CAMPO = lambda rotulo, tag='input': SEL(f"[role=dialog] div:has(> label:text-is('{rotulo}')) {tag}")
GATILHO = lambda rotulo, esc='main': SEL(f"{esc} div:has(> label:text-is('{rotulo}')) button[role=combobox]")   # o formulário do resíduo é um cartão (main)
COTA = SEL(r"div:text-matches('^[\d.]+/[\d.]+ Documentos$')")                          # selo da cota no cabeçalho
CPF_RAFAEL = '27491350879'                                                             # 274.913.508-79 (fictício, mundo)
CNPJ_RECICLA = '47318506000107'
CNPJ_QUIRIRIM = '98463027000115'
CNPJ_VALE_FORTE = '96384120000109'


def sel_teclado(c, gatilho, at_g, at_o, label, tecla=None, fixo=False):
    """Select do Radix pelo teclado: abre (clique com cursor) e escolhe com Enter (a 1ª opção) ou com a letra + Enter."""
    c.click(gatilho, at=at_g, label=f'{label} (abre)', **({'noScroll': True} if fixo else {}))
    if at_o is None:
        c.pause(0.4)   # a lista fica à vista um instante antes da escolha
    if tecla:
        c.press(tecla, at=at_o, label=label)
        return c.press('Enter', label=f'{label} (Enter)')
    return c.press('Enter', at=at_o, label=label)


def abre_grupo(c, grupo, filho, at, label):
    """abre o grupo do menu (se o filho ainda não está no DOM) e deixa o clique pronto"""
    return c.click(BTNX(grupo, within=MENU), at=at, label=label, unless=ITEM_MENU(filho))


@capitulo
def cap00():
    """Abertura: ilustração sobre o Dashboard; depois o menu Fiscal & Ambiental > Ambiental (MTR/CDF)."""
    c = Cap(0, start=(760, 430), setup=setup_em('/dashboard'))
    c.mark(1)
    c.cursor((760, 440), at=0.5, label='cursor em repouso no Dashboard')
    c.marca_ja(2)
    c.mark(3)
    c.hover(GRUPO, 0.3, at=c.A(3, 'menu', 0.6), label='menu Fiscal & Ambiental')
    c.click(GRUPO, at=c.A(3, 'Fiscal', 0.3), label='abre Fiscal & Ambiental', unless=ITEM_MENU('Ambiental (MTR/CDF)'))
    c.click(ITEM_MENU('Ambiental (MTR/CDF)'), at=c.A(3, 'Ambiental.', 0.8), label='Ambiental (MTR/CDF)')
    c.waitfor(text=PAGINAS[ROTA_MTR], timeout=20)
    c.mark(4)
    c.cursor(NEUTRO, at=c.L(4) - 0.2, label='cursor em repouso (cartão do módulo)')
    c.marca_ja(5)
    c.fim()
    return c


@capitulo
def cap01():
    """O que é MTR e CDF: só ilustração; a tela Ambiental fica parada com o cursor em repouso (a voz não traz a linha das abas)."""
    c = Cap(1, start=(900, 470), setup=setup_em(ROTA_MTR))
    c.mark(1)
    c.cursor(NEUTRO, at=0.5, label='cursor em repouso (ilustração da cadeia)')
    for i in range(2, len(c.linhas) + 1):
        c.marca_ja(i)
    c.fim()
    return c


@capitulo
def cap02():
    """Licença e fiscalização: Manifestos vazio na tela; as ilustrações cobrem a fala."""
    c = Cap(2, start=(900, 470), setup=setup_em(ROTA_MTR))
    c.mark(1)
    c.cursor(NEUTRO, at=0.5, label='cursor em repouso (ilustração da licença)')
    for i in range(2, len(c.linhas) + 1):
        c.marca_ja(i)
    c.fim()
    return c


@capitulo
def cap03():
    """Acesso ao SIGOR (CPF, senha, unidade), testar, sincronizar, resíduo "Sucata de ferro" e os três ferros em Materiais."""
    c = Cap(3, start=(900, 470), setup=setup_em(ROTA_MTR, aquece=['/materiais']))
    c.mark(1)
    c.hover(NOVO_MTR_DICA, 1.8, at=c.A(1, 'Novo', 0.9), label='dica: Novo MTR desligado (Configure o acesso ao SIGOR primeiro)')
    c.mark(2)
    c.cursor(NEUTRO, at=c.L(2) - 0.2, label='a dica some (cartão: estado e acesso)')
    c.mark(3)
    c.click(ABA_MTR('Configurações'), at=c.A(3, 'Configurações,', 0.8), label='aba Configurações')
    c.waitfor(text='Configuração do MTR', timeout=15)
    c.registra(TXTX('Sistema:', within='main'), at=c.A(3, 'sistema', 0.4), label='Sistema: SIGOR (zoom)')
    c.mark(4)
    c.digita(SEL('#mtr-cpf'), CPF_RAFAEL, c.A(4, 'CPF', 0.9), c.A(4, 'CPF', -0.1), 'CPF da pessoa usuária do SIGOR (zoom)')
    c.digita(SEL('#mtr-senha'), '$TUT_SENHA', c.A(4, 'senha', 0.9), c.A(4, 'senha', -0.1), 'Senha do SIGOR (pontinhos)')
    c.mark(5)
    c.digita(SEL('#mtr-cod-unidade'), '203918', c.A(5, 'código', 0.9), c.A(5, 'código', -0.1), 'Código da unidade geradora: 203918')
    c.hover(SEL('#mtr-ambiente'), 0.5, at=c.A(5, 'número', 0.6), label='Ambiente: Produção')
    c.mark(6)
    c.click(BTN('Salvar acesso'), at=c.A(6, 'Salvar', 0.7), label='Salvar acesso')
    c.click(BTN('Testar acesso salvo'), at=c.A(6, 'Testar', 0.7), label='Testar acesso salvo')
    c.waitfor(text='Acesso validado', timeout=15)
    c.mark(7)
    c.click(BTN('Sincronizar dados do SIGOR'), at=c.A(7, 'Sincronizar', 0.7), label='Sincronizar dados do SIGOR')
    c.waitfor(text='Resíduos salvos', timeout=20)
    c.mark(8)
    c.click(BTN('Novo resíduo'), at=c.A(8, 'Resíduos', 0.8), label='Novo resíduo')
    c.waitfor(target=SEL('#mtr-preset-apelido'), timeout=10)
    c.digita(SEL('#mtr-preset-apelido'), 'Sucata de ferro', c.A(8, 'sucata', 0.9), c.A(8, 'sucata', -0.1), 'Nome do resíduo: Sucata de ferro')
    c.mark(9)
    ibama = SEL("main button[role=combobox]", hasText='Buscar código IBAMA')
    c.click(ibama, at=c.A(9, 'IBAMA,', 0.8), label='Código IBAMA (abre)')
    c.type(PH('Digite o código ou descrição...'), 'ferrosos', at=None, label='busca: ferrosos', cps=40, noClick=True)
    c.press('Enter', label='escolhe o de metais ferrosos')
    sel_teclado(c, GATILHO('Classe *'), c.A(9, 'classe,', 0.8), None, 'Classe: a da licença (II A)')
    sel_teclado(c, GATILHO('Estado físico *'), c.A(9, 'estado', 0.8), None, 'Estado físico: Sólido')
    sel_teclado(c, GATILHO('Acondicionamento *'), c.A(9, 'acondicionamento', 0.8), None, 'Acondicionamento: Granel', tecla='G')
    sel_teclado(c, GATILHO('Tratamento *'), c.A(9, 'tratamento', 0.8), None, 'Tratamento: Reciclação', tecla='R')
    c.mark(10)
    sel_teclado(c, GATILHO('Unidade *'), c.A(10, 'escreve,', 0.8), c.A(10, 'tonelada.', -0.2), 'Unidade: TON - Tonelada')
    c.registra(GATILHO('Unidade *'), at=None, label='Unidade com TON - Tonelada (zoom)')
    c.mark(11)
    c.click(BTN('Salvar resíduo'), at=c.A(11, 'Salvar', 0.7), label='Salvar resíduo')
    c.waitfor(text='Resíduo salvo', timeout=10)
    c.mark(12)
    abre_grupo(c, 'Materiais', 'Estoque', c.A(12, 'Materiais,', 0.9), 'menu Materiais')
    c.click(ITEM_MENU('Estoque'), at=c.A(12, 'ligo', 0.9), label='Materiais › Estoque')
    c.waitfor(text='Chaparia', timeout=20)
    for nome in ('Ferro pesado', 'Ferro misto', 'Chaparia'):
        c.click(LINHA(nome, '[role=checkbox]'), label=f'marca {nome}')
    # a barra de ações é fixa no rodapé e o botão fica atrás do botão flutuante do Cato (clique de verdade abriria o Cato): clique por eval
    c.cursor((1150, 765), label='cursor vai ao botão Definir resíduo do MTR (barra fixa)')
    c.ev(js_clicar('button', 'Definir resíduo do MTR'), label='Definir resíduo do MTR (clique)')
    c.waitfor(target=SEL('#bulk-material-mtr-residuo'), timeout=10)
    c.click(SEL('#bulk-material-mtr-residuo'), label='Resíduo do MTR (abre)')
    c.press('Enter', at=None, label='Sucata de ferro')
    c.click(BTN('Definir resíduo em 3'), label='Definir resíduo em 3')
    c.waitfor(text='Resíduo do MTR definido em 3', timeout=15)
    c.fim()
    return c


@capitulo
def cap04():
    """Novo MTR: parceiros cadastrados na hora, Jair + GHT7B19, Puxar da nota fiscal (3,6 TON), responsável, Emitir, cota."""
    c = Cap(4, start=(900, 470), setup=setup_em('/materiais', aquece=[ROTA_MTR]))
    c.mark(1)
    abre_grupo(c, 'Fiscal & Ambiental', 'Ambiental (MTR/CDF)', c.A(1, 'Hora', 0.2), 'abre Fiscal & Ambiental')
    c.click(ITEM_MENU('Ambiental (MTR/CDF)'), at=c.A(1, 'Hoje', 0.5), label='Ambiental (MTR/CDF)')
    c.waitfor(text=PAGINAS[ROTA_MTR], timeout=20)
    c.click(BTN('Novo MTR'), at=c.A(1, 'Novo', 0.8), label='Novo MTR')
    c.waitfor(text='TRANSPORTE E DESTINO', timeout=10)
    c.mark(2)
    c.click(SEL("[role=dialog] button[role=combobox]", hasText='Selecione o transportador'), at=c.A(2, 'transportador', 1.0), label='Transportador (abre)')
    c.click(OPTX('Cadastrar novo transportador'), at=c.A(2, 'própria', 0.7), label='Cadastrar novo transportador')
    c.digita(PH('Razão social do parceiro'), 'Recicla Vale Metais Ltda', c.A(2, 'Recicla', 0.8), c.A(2, 'Recicla', -0.1), 'Razão social: Recicla Vale Metais Ltda')
    c.digita(PH('00.000.000/0000-00'), CNPJ_RECICLA, c.A(2, 'CNPJ', 0.8), c.A(2, 'CNPJ', -0.1), 'CNPJ da Recicla Vale')
    c.digita(PH('Ex: 123456'), '203918', c.A(2, 'código', 0.8), None, 'Código da unidade no SIGOR: 203918')
    c.click(BTN('Salvar e usar'), at=c.A(2, 'SIGOR.', 0.8), label='Salvar e usar (transportador)')
    c.waitfor(text='Parceiro salvo', timeout=10)
    c.mark(3)
    c.click(SEL("[role=dialog] button[role=combobox]", hasText='Selecione o destinador'), at=c.A(3, 'destinador', 0.9), label='Destinador (abre)')
    c.click(OPTX('Cadastrar novo destinador'), at=c.A(3, 'Aços', 0.7), label='Cadastrar novo destinador')
    c.digita(PH('Razão social do parceiro'), 'Aços Quiririm Ltda', c.A(3, 'Quiririm,', 0.8), c.A(3, 'Quiririm,', -0.1), 'Razão social: Aços Quiririm Ltda')
    c.digita(PH('00.000.000/0000-00'), CNPJ_QUIRIRIM, c.A(3, 'reciclar', 0.8), c.A(3, 'reciclar', -0.1), 'CNPJ da Aços Quiririm (zoom)')
    c.digita(PH('Ex: 123456'), '187402', c.A(3, 'unidade', 0.8), c.A(3, 'unidade', -0.1), 'Código da unidade do destinador: 187402')
    c.click(BTN('Salvar e usar'), at=c.A(3, 'SIGOR.', 0.8), label='Salvar e usar (destinador)')
    c.mark(4)
    c.digita(PH('Digite ou busque o motorista'), 'Jair', c.A(4, 'Motorista', 0.9), c.A(4, 'Motorista', -0.1), 'Motorista: Jair')
    c.ev(js_clicar('[cmdk-item]', 'Jair Lopes'), label='escolhe Jair Lopes')
    c.click(PH('Digite ou busque a placa'), at=c.A(4, 'frota', 0.8), label='Veículo / placa (campo)')
    c.ev(js_clicar('[cmdk-item]', 'GHT7B19'), label='escolhe GHT7B19')
    c.hover(CAMPO('Data de expedição *', 'button'), 0.6, at=c.A(4, 'expedição', 0.6), label='Data de expedição: hoje')
    c.mark(5)
    c.click(BTN('Avançar', within=DLG), at=c.A(5, 'Avançar.', 0.7), label='Avançar (Resíduos)')
    c.click(BTN('Puxar da nota fiscal', within=DLG), at=c.A(5, 'puxo', 0.8), label='Puxar da nota fiscal')
    c.waitfor(target=PH('Buscar por número, parceiro ou chave...'), timeout=10)
    c.digita(PH('Buscar por número, parceiro ou chave...'), 'Quiririm', c.A(5, 'Busco', 0.9), c.A(5, 'Quiririm,', 0.0), 'busca: Quiririm')
    c.click(SEL("[role=dialog] label:has-text('1254')"), at=c.A(5, 'marco', 0.7), label='marca a NF-e de hoje (1254)')
    c.click(BTN('Conferir (1)'), at=c.A(5, 'Conferir.', 0.7), label='Conferir (1)')
    c.mark(6)
    c.registra(TXTX('3,6 TON'), at=c.A(6, 'quantidade', 0.5), label='3,6 TON - Tonelada (zoom)')
    c.hover(TXTX('1 item convertido de quilo para tonelada'), 1.0, at=c.A(6, 'tonelada:', 0.6), label='1 item convertido de quilo para tonelada (zoom)')
    c.hover(TXTX('Vai pra Observações do Gerador'), 0.8, at=c.A(6, 'chave', 0.6), label='Vai pra Observações do Gerador (chave)')
    c.mark(7)
    c.click(BTN('Usar no MTR'), at=c.A(7, 'Usar', 0.7), label='Usar no MTR')
    c.hover(TXTX('Puxado da nota fiscal', within=DLG), 1.0, at=c.A(7, 'linha', 0.6), label='Puxado da nota fiscal')
    c.mark(8)
    c.click(BTN('Avançar', within=DLG), at=c.A(8, 'Avançar.', 0.7), label='Avançar (Responsável)')
    c.digita(PH('Nome completo'), 'Rafael Nogueira', c.A(8, 'Rafael,', 0.9), c.A(8, 'Rafael,', -0.1), 'Nome do responsável: Rafael Nogueira')
    c.digita(PH('Ex: Gerente ambiental'), 'Sócio-administrador', c.A(8, 'sócio', 0.9), None, 'Cargo: Sócio-administrador')
    c.hover(CAMPO('Observação', 'textarea'), 0.8, at=c.A(8, 'observação', 0.6), label='Observação com a chave da NF-e')
    c.mark(9)
    c.cursor(NEUTRO, at=c.L(9) - 0.2, label='cursor sai dos campos (Resumo do MTR ao lado)')
    c.hover(TXTX('Tudo pronto para emitir o MTR', within=DLG), 0.6, at=None, label='Tudo pronto para emitir o MTR')
    c.click(BTN('Emitir MTR'), at=c.A(9, 'Emitir', 0.7), label='Emitir MTR')
    c.waitfor(text='MTR emitido com sucesso', timeout=25)
    c.registra(TXTX('Nº do manifesto', within=DLG), at=c.A(9, 'número', 0.4), label='Nº do manifesto: 2611000318 (zoom)')
    c.mark(10)
    c.click(BTN('Concluir'), at=c.L(10) - 0.1, label='Concluir')
    c.registra(COTA, at=c.A(10, 'cota', 0.5), label='selo da cota (zoom)')
    c.fim()
    return c


@capitulo
def cap05():
    """Lista com o 2611000318, Ver tentativas, Baixar PDF (aba nova; a câmera fica no app) e o ícone Usar como modelo (sem clicar)."""
    c = Cap(5, start=(900, 470), setup=setup_em(ROTA_MTR))
    c.mark(1)
    c.registra(LINHA('2611000318'), at=c.A(1, 'aparece', 0.4), label='linha do 2611000318')
    c.hover(LINHA('2611000318', "td:has-text('Aços Quiririm')"), 0.3, at=c.A(1, 'destinador,', 0.6), label='Destinador')
    c.hover(LINHA('2611000318', 'td >> nth=2'), 0.3, at=c.A(1, 'resíduo,', 0.6), label='Resíduo')
    c.hover(LINHA('2611000318', "td:has-text('10/11/2026')"), 0.3, at=c.A(1, 'data', 0.6), label='Data')
    c.hover(LINHA('2611000318', 'td >> nth=4'), 0.5, at=c.A(1, 'emitido', 0.6, nth=1), label='Status: Emitido')
    c.mark(2)
    c.click(LINHA('2611000318', "button[title='Ver tentativas']"), at=c.A(2, 'Ver', 0.8), label='Ver tentativas')
    c.waitfor(text='Histórico de tentativas', timeout=10)
    c.hover(TXTX('Autorizada', within=DLG), 0.8, at=c.A(2, 'autorizado.', 0.6), label='tentativa Autorizada')
    c.click(SEL("[role=dialog] button:text-is('Fechar') >> nth=-1"), at=c.A(2, 'erro,', 0.2), label='Fechar')
    c.mark(3)
    c.click(LINHA('2611000318', "button[title='Baixar PDF']"), at=c.A(3, 'Baixar', 0.7), label='Baixar PDF (abre aba nova)')
    c.cursor(NEUTRO, at=c.A(3, 'motorista,', 0.1), label='cursor em repouso (ilustração do PDF com o motorista)')
    c.mark(4)
    c.hover(LINHA('2611000318', "button[title='Usar como modelo']"), 1.2, at=c.A(4, 'Usar', 0.7), label='ícone Usar como modelo (zoom, sem clicar)')
    c.fim()
    return c


@capitulo
def cap06():
    """Corte 10:40: o MTR da tarde (2611000325) é cancelado; selo da cota."""
    c = Cap(6, start=(900, 470), setup=setup_em(ROTA_MTR))
    c.mark(1)
    c.registra(LINHA('2611000325'), at=c.A(1, 'Mais', 0.4), label='linha do 2611000325')
    c.mark(2)
    c.hover(LINHA('2611000325', "button[title='Cancelar MTR']"), 1.2, at=c.A(2, 'cancelado.', 1.4), label='ícone Cancelar MTR (zoom)')
    c.mark(3)
    c.click(LINHA('2611000325', "button[title='Cancelar MTR']"), at=c.A(3, 'cancelamento', 0.9), label='Cancelar MTR (ícone)')
    c.waitfor(text='O cancelamento será enviado ao sistema ambiental', timeout=10)
    c.registra(TXTX('O cancelamento será enviado ao sistema ambiental', within=ADLG), at=c.A(3, 'sistema', 0.0), label='texto do diálogo (zoom)')
    c.mark(4)
    c.click(BTN('Cancelar MTR', within=ADLG), at=c.A(4, 'Cancelar', 0.8), label='Cancelar MTR (confirma)')
    c.waitfor(target=LINHA('2611000325', ":text-is('Cancelado')"), timeout=15)
    c.hover(LINHA('2611000325', "td >> nth=4"), 0.8, at=c.A(4, 'cancelado.', 0.6), label='selo Cancelado')
    c.mark(5)
    c.registra(COTA, at=c.A(5, 'cota', 0.5), label='selo da cota (zoom)')
    c.fim()
    return c


@capitulo
def cap07():
    """CDF: Novo CDF de outubro (01/10 a 31/10) para a Auto Peças Vale Forte, três MTR, Emitir; nº 2611000041; a lista."""
    c = Cap(7, start=(900, 470), setup=setup_em(ROTA_MTR, aquece=[ROTA_CDF]))
    c.mark(1)
    c.click(SUBABA('CDF'), at=c.A(1, 'CDF,', 0.8), label='sub-aba CDF')
    c.waitfor(text='Nenhum CDF emitido ainda.', timeout=15)
    c.mark(2)
    c.cursor(NEUTRO, at=c.L(2) - 0.2, label='cursor em repouso (ilustração das cargas de outubro)')
    c.marca_ja(3)
    c.mark(4)
    c.click(BTN('Novo CDF'), at=c.A(4, 'Novo', 0.8), label='Novo CDF')
    c.waitfor(text='PERÍODO', timeout=10)
    data_ini = SEL("[role=dialog] button:has-text('dd/mm/aaaa') >> nth=0")
    c.click(data_ini, at=c.A(4, 'período,', 0.9), label='Data inicial (abre o calendário)')
    c.ev(js_clicar('button[name=previous-month]'), label='mês anterior (outubro)')
    c.ev(DIA_JS(1), label='dia 01/10/2026')
    c.click(data_ini, at=c.A(4, 'outubro', 0.8), label='Data final (abre o calendário)')
    c.ev(js_clicar('button[name=previous-month]'), label='mês anterior (outubro)')
    c.ev(DIA_JS(31), label='dia 31/10/2026')
    c.mark(5)
    c.click(BTN('Avançar', within=DLG), at=c.L(5) - 0.4, label='Avançar (Destinador)')
    c.registra(CAMPO('CNPJ do destinador *'), at=c.A(5, 'CNPJ', 0.5), label='CNPJ do destinador já preenchido (zoom)')
    c.digita(PH('Nome completo'), 'Rafael Nogueira', c.A(5, 'Rafael.', 0.9), c.A(5, 'Rafael.', -0.1), 'Nome do responsável: Rafael Nogueira')
    c.mark(6)
    c.click(BTN('Avançar', within=DLG), at=c.L(6) - 0.4, label='Avançar (Gerador)')
    c.digita(CAMPO('CNPJ do gerador'), CNPJ_VALE_FORTE, c.A(6, 'CNPJ', 0.8), c.A(6, 'CNPJ', -0.1), 'CNPJ da Auto Peças Vale Forte')
    c.digita(CAMPO('Unidade no SIGOR'), '184527', c.A(6, 'unidade', 0.8), None, 'Unidade no SIGOR: 184527')
    c.mark(7)
    c.click(BTN('Avançar', within=DLG), at=c.L(7) - 0.4, label='Avançar (MTRs incluídos)')
    c.click(PH('Um número por linha, ou separados por vírgula'), at=None, label='Números dos MTRs (campo)')
    c.colar("[role=dialog] textarea", '2610001542\n2610001877\n2610002203', at=c.A(7, 'três', 0.1), label='os três números de MTR')
    c.hover(TXTX('MTR(s) informado(s)', within=DLG), 0.6, at=c.A(7, 'cargas.', 0.3), label='3 MTR(s) informado(s)')
    c.mark(8)
    c.click(BTN('Avançar', within=DLG), at=c.L(8) - 0.4, label='Avançar (Confirmar)')
    c.registra(TXTX('os MTRs informados', within=DLG), at=c.A(8, 'aviso:', 0.5), label='aviso: MTR já recebido no SIGOR (zoom)')
    c.mark(9)
    rola_ate(c, 'A emissão do CDF é', c.L(9) - 0.1, 'desce até o aviso de emissão definitiva', y=300, escopo=DLG, prefixo=True)
    c.hover(TXTX('Período:', within=DLG), 1.0, at=c.A(9, 'resumo', 0.6), label='resumo: Período, Destinador, Gerador, MTRs')
    c.mark(10)
    c.click(BTN('Emitir CDF'), at=c.A(10, 'Emitir', 0.7), label='Emitir CDF')
    c.waitfor(text='CDF emitido com sucesso', timeout=25)
    c.registra(TXTX('Nº do certificado', within=DLG), at=c.A(10, 'número', 0.4), label='Nº do certificado: 2611000041 (zoom)')
    c.mark(11)
    c.click(BTN('Concluir'), at=c.L(11) - 0.1, label='Concluir')
    c.registra(LINHA('2611000041'), at=c.A(11, 'período,', 0.4), label='linha do CDF 2611000041 (zoom)')
    c.hover(LINHA('2611000041', 'td >> nth=3'), 0.6, at=c.A(11, 'status.', 0.6), label='Status: Emitido')
    c.hover(LINHA('2611000041', "button[title='Ações']"), 0.8, at=c.A(11, 'menu', 0.6), label='menu de ações')
    c.fim()
    return c


def DIA_JS(n):
    """clica o dia `n` do mês visível do calendário (ignora os dias de fora do mês)"""
    return ("(()=>{const b=[...document.querySelectorAll('button[name=day]')].find(b=>b.textContent.trim()===%s&&"
            "!b.disabled&&!b.className.includes('day-outside')&&b.getAttribute('aria-hidden')!=='true');"
            "if(!b)return 'SEM ALVO';b.click();return 'dia '+%s})()") % (json.dumps(str(n)), json.dumps(str(n)))


@capitulo
def cap08():
    """Ações > Baixar PDF na linha do CDF (aba nova; a câmera fica no app); o resto é ilustração."""
    c = Cap(8, start=(900, 470), setup=setup_em(ROTA_CDF))
    c.mark(1)
    c.click(LINHA('2611000041', "button[title='Ações']"), at=c.A(1, 'menu', 0.8), label='Ações da linha do CDF')
    c.click(ITEM('Baixar PDF'), at=c.A(1, 'Baixar', 0.6), label='Baixar PDF (abre aba nova)', noScroll=True)
    c.cursor(NEUTRO, at=c.A(1, 'PDF', -0.5, nth=1), label='cursor em repouso (ilustração da pasta da licença)')
    c.marca_ja(2)
    c.marca_ja(3)
    c.fim()
    return c


@capitulo
def cap09():
    """Notas Fiscais > Saída (a NF-e 1254 da Aços Quiririm, R$ 3.528,00); depois Ambiental > MTR com o 2611000318."""
    c = Cap(9, start=(900, 470), setup=setup_em(ROTA_CDF, aquece=['/fiscal-ambiental/nfe/saida', ROTA_MTR]))
    c.mark(1)
    abre_grupo(c, 'Fiscal & Ambiental', 'Notas Fiscais (NF-e)', c.A(1, 'conversa', 0.6), 'abre Fiscal & Ambiental')
    c.click(ITEM_MENU('Notas Fiscais (NF-e)'), at=c.A(1, 'nota', 0.9), label='Notas Fiscais (NF-e) no menu')
    c.click(SUBABA('Saída'), at=c.A(1, 'carga', 0.8), label='aba Saída')
    c.registra(LINHA('1254'), at=c.A(1, 'venda', 0.4), label='NF-e 1254 da Aços Quiririm (R$ 3.528,00, Autorizada)')
    c.mark(2)
    c.cursor(NEUTRO, at=c.L(2) - 0.2, label='cursor em repouso (ilustração das três faixas)')
    for i in (3, 4):
        c.marca_ja(i)
    c.mark(5)
    c.click(ITEM_MENU('Ambiental (MTR/CDF)'), at=c.L(5) - 0.9, label='Ambiental (MTR/CDF)')
    c.waitfor(text=PAGINAS[ROTA_MTR], timeout=20)
    c.hover(LINHA('2611000318'), 1.2, at=c.A(5, 'ligados', 0.7), label='linha do 2611000318 (ligada pela chave)')
    c.fim()
    return c


@capitulo
def cap10():
    """Recapitulando: montagem das gravações dos capítulos 3 a 8 por cima; a tela fica parada em Ambiental > MTR."""
    c = Cap(10, start=(900, 470), setup=setup_em(ROTA_MTR))
    c.mark(1)
    c.cursor(NEUTRO, at=0.5, label='cursor em repouso (montagem)')
    for i in range(2, len(c.linhas) + 1):
        c.marca_ja(i)
    c.fim()
    return c


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
