#!/usr/bin/env python3
"""T17 · Transporte, serviço e o contador: gera rec/t17/cap00..cap13.json (roteiros do robô) a partir da voz (t17/narracao/capNN.json).

EcoSistema 1.59.154 no Supabase falso (mundo da Recicla Vale Metais), computador 1280x800, logado como Rafael Nogueira (MASTER).
Cada passo é preso a uma palavra da fala: `at` = início da palavra - folga (o custo do gesto, docs/04 "Custo real dos gestos"), e a marca
Ln entra no início de cada linha. Quando a voz chegar, rodar de novo com o capNN.json da voz (nada a reescrever).
Rodar de qualquer pasta: `python3 -I rec/t17/gerar.py [NN ...]`; ensaiar/gravar: `bash rec/t17/t17_grava.sh NN [--rapido]`.

Relógio (MUNDO_LINHA_DO_TEMPO.md, seção 14): FAKE_NOW 10/11/2026 09:30 nos capítulos 0 a 4 (as NF-e 1252 e 1253 saíram às 09:05 e
09:12; o caminhão sai às 09:40) e 14:20 do 5 ao 13 (a carga já foi entregue em Itamonte).
Cadeia de sementes (rec/mundo/seeds-extra/t17; inicio = t17_sementes.py; as outras saem de t17_semente.py, do estado da instância 54317
logo depois do ensaio do capítulo, cumulativas): inicio -> apos-cap02 (FKD2E41 e Edson completos) -> apos-cap04 (MDF-e nº 1 autorizado)
-> apos-cap05 (encerrado) -> apos-cap07 (NFS-e 14 autorizada) -> apos-cap08 (NFS-e recebidas ligadas, conta da Balanças Tremembé).
Os capítulos 9 a 11 só leem; o 12 é só ilustração e o 13 é a montagem (o robô deixa uma tela parada com as marcas).
"""
import hashlib
import json
import os
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TUT = os.path.normpath(os.path.join(HERE, '..', '..'))
NARR = os.path.join(TUT, 't17', 'narracao')
N0930 = '2026-11-10T09:30:00-03:00'
N1420 = '2026-11-10T14:20:00-03:00'
FAKE_NOW = {n: (N0930 if n <= 4 else N1420) for n in range(14)}


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
NOMES = ['Abertura', 'O que é o MDF-e', 'Veículo e motorista', 'Numeração e percurso', 'Emitir o manifesto', 'Encerrar no fim da viagem',
         'A nota de serviço', 'Emitir e acompanhar', 'O serviço que você tomou', 'Entrada, saída e saldo', 'O estoque pelas notas',
         'O pacote do mês', 'O que o contador faz', 'Recapitulando']
SEMENTE = {0: None, 1: None, 2: None, 3: 'apos-cap02', 4: 'apos-cap02', 5: 'apos-cap04', 6: 'apos-cap05', 7: 'apos-cap05', 8: 'apos-cap07',
           9: 'apos-cap08', 10: 'apos-cap08', 11: 'apos-cap08', 12: 'apos-cap08', 13: 'apos-cap08'}


def sementes(n):
    """a semente de cada capítulo é cumulativa (tudo desde o início da aula): só a última da cadeia vai junto do início"""
    return ['t17/inicio'] + ([f't17/{SEMENTE[n]}'] if SEMENTE[n] else [])


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
        return s.type(campo, texto, at=at_texto, label=label, cps=40, noClick=True, **kw)

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
            'name': f't17-cap{s.n:02d}',
            'title': f'T17 · Cap. {s.n} · {NOMES[s.n]} (narração {str(round(s.dur, 1)).replace(".", ",")} s{" ESTIMADA" if s.estimada else ""}; '
                     f'marcas L1..L{len(s.linhas)} = início de cada linha do roteiro; FAKE_NOW {FAKE_NOW[s.n]})',
            'seed': f't17-cap{s.n:02d}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
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
PAGINAS = {
    '/dashboard': None,
    '/fiscal-ambiental/transporte': 'Manifesto Eletrônico de Documentos Fiscais (MDF-e)',
    '/fiscal-ambiental/transporte/frota': 'Frota (veículos e motoristas do MDF-e)',
    '/fiscal-ambiental/nfse': 'Nota Fiscal de Serviço (NFS-e)',
    '/fiscal-ambiental/nfe/saida': 'Notas Recebidas',
    '/fiscal-ambiental/nfe/recebidas-nfse': 'Notas Recebidas',
    '/fiscal-ambiental/estoque-fiscal/relatorio': 'Pendentes + Rejeitadas',
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


# ---------------------------------------------------------------- alvos das telas fiscais (conferidos por exploração, rec/t17/_ex)
NAV = "nav[aria-label='Navegação da seção']"
SUBABA = lambda n: BTN(n, within=NAV)                                                  # sub-abas (Manifestos/Frota, Entrada/Saída...)
NEUTRO = (900, 470)                                                                    # ponto neutro (fora de menu, cartão e botão)
CARTAO = lambda t: TXT(t, within='main')
LINHA = lambda txt, sub='': SEL(f"main tbody tr:has-text('{txt}') {sub}".strip())
VEIC = lambda placa: SEL(f"main button:has-text('{placa}'):not([aria-label])")         # item da lista "Veículos da frota"


def escolhe(c, gatilho, opcao, at_g, at_o, label, teclas=None, fixo=False):
    """Select do Radix: clica o gatilho (cursor) e a opção; com `teclas`, escolhe pelo teclado (busca por digitação + Enter) quando a
    opção fica fora da parte visível da lista (o robô rolaria a lista ~2,5 s). `fixo`: gatilho fora da faixa y 96..730 (noScroll)."""
    c.click(gatilho, at=at_g, label=f'{label} (abre)', **({'noScroll': True} if fixo else {}))
    if teclas:
        for i, k in enumerate(teclas):
            c.press(k, at=round(at_o + 0.12 * i, 2) if i == 0 else None, label=label if i == 0 else None)
        return c.press('Enter', label=f'{label} (Enter)')
    return c.click(opcao if isinstance(opcao, dict) else OPT(opcao), at=at_o, label=label)


@capitulo
def cap00():
    """Abertura: ilustração sobre o Dashboard; depois o menu Fiscal & Ambiental com Transporte, Notas de Serviço e Estoque Fiscal."""
    c = Cap(0, start=(760, 430), setup=setup_em('/dashboard'))
    c.mark(1)
    c.cursor((760, 440), at=0.5, label='cursor em repouso no Dashboard')
    c.marca_ja(2)
    c.mark(3)
    c.click(GRUPO, at=c.A(3, 'Fiscal', 0.8), label='abre Fiscal & Ambiental', unless=ITEM_MENU('Transporte (MDF-e)'))
    c.hover(ITEM_MENU('Transporte (MDF-e)'), 0.4, at=c.A(3, 'Transporte,', 0.6), label='Transporte (MDF-e)')
    c.hover(ITEM_MENU('Notas de Serviço (NFS-e)'), 0.4, at=c.A(3, 'Notas', 0.6), label='Notas de Serviço (NFS-e)')
    c.hover(ITEM_MENU('Estoque Fiscal'), 0.7, at=c.A(3, 'Estoque', 0.6), label='Estoque Fiscal')
    c.mark(4)
    c.cursor((760, 460), at=c.L(4) - 0.2, label='cursor sai do menu (cartão do módulo)')
    c.marca_ja(5)
    c.fim()
    return c


@capitulo
def cap01():
    """O que é o MDF-e: Transporte > Manifestos vazio, as ilustrações (L2, L3), os quatro cartões e a dica."""
    c = Cap(1, start=(700, 430), setup=setup_em('/dashboard', extra=[{'do': 'eval', 'js': js_abrir_grupo('Fiscal & Ambiental', 'Transporte (MDF-e)')},
                                                                       {'do': 'wait', 'seconds': 0.8}], aquece=['/fiscal-ambiental/transporte']))
    c.mark(1)
    c.click(ITEM_MENU('Transporte (MDF-e)'), at=c.A(1, 'aqui,', 0.9), label='Transporte (MDF-e) no menu')
    c.waitfor(text=PAGINAS['/fiscal-ambiental/transporte'], timeout=15)
    c.hover(SUBABA('Manifestos'), 0.4, at=c.A(1, 'Manifestos.', 0.6), label='aba Manifestos')
    c.hover(TXT('Nenhum MDF-e encontrado'), 0.8, at=c.A(1, 'nenhum.', 0.6), label='lista vazia: Nenhum MDF-e encontrado')
    c.mark(2)
    c.cursor(NEUTRO, at=c.L(2) - 0.2, label='cursor em repouso (ilustração do manifesto)')
    c.marca_ja(3)
    c.mark(4)
    c.registra(CARTAO('MDF-e Pendentes'), at=c.A(4, 'cartões', 0.4), label='cartões do MDF-e (zoom)')
    c.hover(CARTAO('MDF-e Autorizados'), 0.2, at=c.A(4, 'autorizados,', 0.6), label='MDF-e Autorizados')
    c.hover(CARTAO('MDF-e Rejeitados'), 0.2, at=c.A(4, 'rejeitados', 0.6), label='MDF-e Rejeitados')
    c.hover(CARTAO('MDF-e Encerrados'), 0.4, at=c.A(4, 'encerrados.', 0.6), label='MDF-e Encerrados')
    c.mark(5)
    c.cursor(NEUTRO, at=c.L(5) - 0.2, label='câmera volta à tela inteira (dica)')
    c.fim()
    return c


@capitulo
def cap02():
    """Frota: o FKD2E41 ganha os dados de transporte e o Edson Moura, CPF, CNH e categoria."""
    c = Cap(2, start=(900, 440), setup=setup_em('/fiscal-ambiental/transporte', aquece=['/fiscal-ambiental/transporte/frota']))
    c.mark(1)
    c.click(SUBABA('Frota'), at=c.A(1, 'Frota.', 0.8), label='aba Frota')
    c.waitfor(text=PAGINAS['/fiscal-ambiental/transporte/frota'], timeout=15)
    # a lista abre com o primeiro da ordem (EZR4C63, Picape) no painel: o caminhão truck é escolhido na lista
    c.click(VEIC('FKD2E41'), at=c.A(1, 'caminhões', 0.7), label='FKD2E41 (Caminhão truck) na lista')
    c.hover(TXT('Mesma frota usada na pesagem de compra/venda.'), 0.6, at=c.A(1, 'pesagem.', 0.6), label='mesma frota da pesagem')
    c.mark(2)
    c.hover(TXT('Dados de transporte', within='main section'), 0.4, at=c.A(2, 'transporte', 0.6), label='painel: Dados de transporte')
    c.click(BTN('Editar', within='main'), at=c.A(2, 'Editar.', 0.7), label='Editar o FKD2E41')
    c.waitfor(text='Editar veículo', timeout=10)
    c.mark(3)
    rola_ate(c, 'Dados de transporte (MDF-e / NF-e)', round(max(c.L(3) - 0.2, c.W(2, 'Editar.') + 0.9), 2), 'janela desce até Dados de transporte', y=110, escopo=DLG)
    escolhe(c, SEL('#veiculo-uf'), 'SP', c.A(3, 'São', 0.9), c.A(3, 'Paulo.', 0.2), 'UF de licenciamento: SP', teclas=['S', 'P'])
    escolhe(c, SEL('#veiculo-categoria'), OPTX('Veículo único'), c.A(3, 'Tipo,', 0.6), c.A(3, 'único,', 0.4), 'Tipo: Veículo único')
    escolhe(c, SEL('#veiculo-rodado'), 'Truck', c.A(3, 'rodado', 0.6), c.A(3, 'truck,', 0.3), 'Tipo de rodado: Truck')
    escolhe(c, SEL('#veiculo-carroceria'), 'Aberta', c.A(3, 'carroceria', 0.6), c.A(3, 'aberta.', 0.3), 'Tipo de carroceria: Aberta')
    c.mark(4)
    c.hover(SEL('#veiculo-tara'), 0.8, at=c.A(4, 'tara,', 0.6), label='Tara (kg)')
    c.hover(SEL('#veiculo-cap-kg'), 0.8, at=c.A(4, 'catorze', 0.6), label='Capacidade (kg)')
    c.mark(5)
    c.digita(SEL('#veiculo-cap-m3'), '30', c.A(5, 'peso', 0.7), c.A(5, 'quilos.', 0.05), 'Capacidade (m³): 30')
    c.hover(TXTX('máx. 999 m³', within=DLG), 0.8, at=c.A(5, 'tonelada,', 0.6), label='ajuda: máx. 999 m³')
    c.mark(6)
    c.click(BTN('Salvar', within=DLG), at=c.A(6, 'Salvar,', 0.7), label='Salvar o veículo')
    c.waitfor(text='Veículo atualizado', timeout=10)
    c.hover(TXT('Dados de transporte', within='main section'), 0.6, at=c.A(6, 'pronto', 0.5), label='painel: Dados de transporte preenchido')
    c.mark(7)
    c.click(TAB('Motoristas'), at=c.A(7, 'motorista.', 0.8), label='aba Motoristas')
    c.hover(TXTX('Edson Moura', within='main'), 0.4, at=c.A(7, 'Edson', 0.6), label='Edson Moura na lista')
    c.click(BTN('Editar', within='main'), at=c.A(7, 'Editar.', 0.7), label='Editar o Edson')
    c.waitfor(text='Editar motorista', timeout=10)
    c.mark(8)
    c.digita(SEL('#motorista-doc'), '31847265090', c.A(8, 'CPF', 0.9), c.A(8, 'CPF', -0.05), 'CPF: 318.472.650-90')
    c.digita(SEL('#motorista-cnh'), '04728193604', c.A(8, 'completo', 0.9), c.A(8, 'completo', 0.0), 'CNH: 04728193604')
    escolhe(c, SEL('#motorista-cnh-cat'), 'C', c.A(8, 'CNH', 0.3), c.A(8, 'categoria.', 0.2), 'Categoria: C')
    # validade (a fala não cita; está no roteiro): o foco entra pelo rótulo (dia primeiro), sem cair no meio do campo de data
    c.click(SEL("[role=dialog] label[for='motorista-cnh-val']"), at=round(c.W(8, 'categoria.') + 0.45, 2), label='Validade da CNH (campo)')
    c.type(SEL('#motorista-cnh-val'), '18032029', label='Validade da CNH: 18/03/2029', cps=40, noClick=True)
    c.mark(9)
    c.click(BTN('Salvar', within=DLG), at=c.A(9, 'Salvar.', 0.3), label='Salvar o motorista')
    c.waitfor(text='Motorista atualizado', timeout=10)
    c.hover(TXT('Carteira de habilitação', within='main section'), 0.8, at=c.A(9, 'motorista', 0.4), label='painel: Carteira de habilitação')
    c.fim()
    return c


@capitulo
def cap03():
    """Configurações do MDF-e: série 1, próximo 1; a ponte para a Frota; o percurso é ilustração (L4 a L6)."""
    c = Cap(3, start=(900, 440), setup=setup_em('/fiscal-ambiental/transporte/frota', aquece=['/fiscal-ambiental/transporte']))
    c.mark(1)
    c.click(SUBABA('Manifestos'), at=c.A(1, 'frota', 0.6), label='aba Manifestos')
    c.waitfor(text='Nenhum MDF-e encontrado', timeout=15)
    c.click(BTN('Configurações do MDF-e'), at=c.A(1, 'Configurações', 0.8), label='Configurações do MDF-e')
    c.waitfor(text='Útil quando a empresa já emitiu MDF-e em outro sistema.', timeout=10)
    c.hover(TXT('Próximo MDF-e', within=DLG), 0.8, at=c.A(1, 'série', 0.6), label='quadro Série / Próximo MDF-e')
    c.mark(2)
    c.hover(TXTX('Próximo Número', within=DLG), 0.6, at=c.A(2, 'um.', 0.6), label='Próximo Número: 1')
    c.hover(TXTX('Útil quando a empresa já emitiu MDF-e', within=DLG), 0.8, at=c.A(2, 'sistema,', 0.6), label='série e próximo número (outro sistema)')
    c.mark(3)
    c.hover(BTN('Ir para Frota', within=DLG), 0.6, at=c.A(3, 'Frota,', 0.6), label='Motoristas e veículos ficam na Frota')
    c.press('Escape', at=c.A(3, 'ver.', -0.2), label='fecha a janela')
    c.mark(4)
    c.cursor(NEUTRO, at=c.L(4) - 0.2, label='cursor em repouso (ilustração do percurso)')
    c.marca_ja(5)
    c.marca_ja(6)
    c.fim()
    return c


ORIGEM = "[role=dialog] div.rounded-xl:has(p:text-is('Carregamento (Origem)'))"
DESTINO = "[role=dialog] div.rounded-xl:has(p:text-is('Descarregamento (Destino)'))"
NOTA_MDFE = lambda num: SEL(f"[role=dialog] label:has-text('NF-e #{num}')")


@capitulo
def cap04():
    """Novo MDF-e: as duas NF-e da Serra Fina, FKD2E41 + Edson, RJ no percurso, Itamonte/MG, 5.800 kg; Normal; criar; autorizado."""
    c = Cap(4, start=(900, 440), setup=setup_em('/fiscal-ambiental/transporte'))
    c.mark(1)
    c.click(BTN('Novo MDF-e'), at=c.A(1, 'Novo', 1.0), label='Novo MDF-e')
    c.waitfor(text='NF-ES VINCULADAS', timeout=10)
    c.hover(TXT('NF-ES VINCULADAS', within=DLG), 0.5, at=c.A(1, 'notas', 0.6), label='etapa Notas fiscais')
    c.mark(2)
    c.digita(PH('Buscar NF-e...'), 'Serra Fina', c.A(2, 'Busco', 0.7), c.A(2, 'Serra', 0.2), 'busca: Serra Fina')
    c.click(NOTA_MDFE(1252), at=c.A(2, 'perfil', 0.7), label='NF-e 1252 (alumínio perfil)')
    c.click(NOTA_MDFE(1253), at=c.A(2, 'bloco.', 0.7), label='NF-e 1253 (alumínio bloco)')
    c.hover(TXTX('NF-e(s) selecionada(s)', within=DLG), 1.0, at=c.A(2, 'Juntas,', 0.6), label='2 NF-e selecionadas: R$ 55.380,00')
    c.mark(3)
    c.click(BTN('Continuar'), at=c.A(3, 'Continuar.', 0.7), label='Continuar (veículo e motorista)')
    escolhe(c, SEL('[role=dialog] button[role=combobox]', hasText='Selecione um veículo'), OPTX('FKD2E41'), c.A(3, 'veículo,', 0.7), c.A(3, 'truck,', 0.4), 'Veículo: Caminhão truck FKD2E41')
    escolhe(c, SEL('[role=dialog] button[role=combobox]', hasText='Selecione um motorista'), OPTX('Edson Moura'), c.A(3, 'motorista,', 0.7), c.A(3, 'Edson.', 0.4), 'Motorista: Edson Moura')
    c.hover(TXTX('Veículo único', within=DLG), 0.6, at=c.A(3, 'completa,', 0.6), label='composição completa')
    c.mark(4)
    c.click(BTN('Continuar'), at=c.A(4, 'Continuar.', 0.7), label='Continuar (trajeto e carga)')
    c.hover(SEL(f'{ORIGEM} button[role=combobox] >> nth=1'), 0.8, at=c.A(4, 'Taubaté.', 0.6), label='origem: Taubaté/SP')
    c.mark(5)
    c.click(BTN('Adicionar UF ao percurso'), at=c.A(5, 'adiciono', 0.7), label='Adicionar UF ao percurso')
    escolhe(c, SEL('[role=dialog] button[role=combobox]', hasText='Selecione a UF'), 'RJ', c.A(5, 'Rio', 0.7), c.A(5, 'Janeiro,', 0.3), 'Percurso: 1ª UF RJ', teclas=['R', 'J'])
    # com a 1ª UF do percurso, o cartão do destino desce (cidade em y ~754, fora da faixa de clique): a janela sobe antes
    rola_ate(c, 'Descarregamento (Destino)', round(c.L(6) - 0.9, 2), 'janela sobe até o destino', y=330, dur_ms=600, escopo=DLG)
    c.mark(6)
    escolhe(c, SEL(f'{DESTINO} button[role=combobox] >> nth=0'), 'MG', c.A(6, 'destino,', 0.6), c.A(6, 'Minas', 0.2), 'Destino: MG', teclas=['M', 'G'])
    escolhe(c, SEL(f'{DESTINO} button[role=combobox] >> nth=1'), 'Itamonte', c.A(6, 'cidade', 0.6), c.A(6, 'Itamonte.', 0.3), 'Destino: Itamonte',
            teclas=['I', 't', 'a', 'm'])
    c.mark(7)
    rola_ate(c, 'Peso Bruto Total (kg)', c.A(7, 'peso', 0.9), 'janela desce até o peso', y=330, escopo=DLG)
    c.hover(SEL("[role=dialog] div:has(> label:text-is('Peso Bruto Total (kg)')) input"), 0.8, at=c.A(7, 'cinco', 0.5), label='Peso Bruto Total (kg): 5800')
    c.hover(TXT('Valor Total da Carga', within=DLG), 0.8, at=c.A(7, 'valor', 0.5), label='Valor Total da Carga: R$ 55.380,00')
    c.mark(8)
    c.click(BTN('Continuar'), at=c.L(8) - 0.2, label='Continuar (revisão e emissão)')
    c.hover(SEL("[role=dialog] button[aria-pressed]", hasText='Normal'), 0.8, at=c.A(8, 'Normal,', 0.6), label='Como emitir: Normal')
    c.mark(9)
    c.hover(SEL("[role=dialog] button[aria-pressed]", hasText='Contingência'), 1.2, at=c.A(9, 'contingência', 0.6), label='botão Contingência')
    c.mark(10)
    c.hover(TXTX('Tudo pronto para criar e emitir o MDF-e', within=DLG), 0.5, at=c.A(10, 'Tudo', 0.6), label='Tudo pronto para criar e emitir o MDF-e')
    c.click(BTN('Criar MDF-e'), at=c.A(10, 'Criar', 0.7), label='Criar MDF-e')
    c.waitfor(target=LINHA('FKD2E41', ":text-is('Aguardando SEFAZ')"), timeout=10)
    c.hover(LINHA('FKD2E41', 'td >> nth=0'), 0.6, at=c.A(10, 'enviado', 0.5), label='nº 1 Aguardando SEFAZ')
    c.mark(11)
    c.waitfor(target=LINHA('FKD2E41', ":text-is('Autorizado')"), timeout=15)
    c.registra(LINHA('FKD2E41'), at=c.A(11, 'Pronto,', 0.2), label='linha do nº 1 Autorizado')
    c.hover(LINHA('FKD2E41', "td:has-text('Edson')"), 0.2, at=c.A(11, 'motorista,', 0.6), label='Motorista')
    c.hover(LINHA('FKD2E41', "td:has-text('FKD2E41')"), 0.2, at=c.A(11, 'placa,', 0.6), label='Placa')
    c.hover(LINHA('FKD2E41', "td:has-text('Itamonte')"), 0.2, at=c.A(11, 'trajeto,', 0.6), label='Trajeto')
    c.hover(LINHA('FKD2E41', "td:has-text('55.380')"), 0.2, at=c.A(11, 'valor', 0.6), label='Valor')
    c.hover(LINHA('FKD2E41', "td:has-text('5.800')"), 0.3, at=c.A(11, 'peso.', 0.6), label='Peso (kg)')
    c.mark(12)
    c.hover(LINHA('FKD2E41', 'button[aria-haspopup=menu]'), 0.4, at=c.A(12, 'ações', 0.7), label='Ações do nº 1')
    c.hover(ITEM('Baixar DAMDFE (PDF)'), 1.0, at=c.A(12, 'PDF', 0.6), label='Baixar DAMDFE (PDF)', noScroll=True)
    c.fim()
    return c


@capitulo
def cap05():
    """Corte da tarde: encerrar × cancelar (ilustração), Encerrar pelo menu, "Encerramento enviado" e "Encerrado" na consulta."""
    c = Cap(5, start=(900, 440), setup=setup_em('/fiscal-ambiental/transporte'))
    c.mark(1)
    c.hover(LINHA('FKD2E41', "td:has-text('Itamonte')"), 0.6, at=c.A(1, 'Itamonte.', 0.6), label='nº 1 para Itamonte, Autorizado')
    c.hover(CARTAO('MDF-e Autorizados'), 0.6, at=c.A(1, 'encerrar', 0.6), label='MDF-e Autorizados: 1')
    c.mark(2)
    c.cursor(NEUTRO, at=c.L(2) - 0.2, label='cursor em repouso (ilustração encerrar × cancelar)')
    c.mark(3)
    c.hover(LINHA('FKD2E41', 'button[aria-haspopup=menu]'), 0.4, at=c.A(3, 'menu', 0.7), label='Ações do nº 1')
    c.click(ITEM('Encerrar'), at=c.A(3, 'Encerrar.', 0.6), label='Encerrar', noScroll=True)
    c.waitfor(target=LINHA('FKD2E41', ":text-is('Encerramento enviado')"), timeout=10)
    c.hover(LINHA('FKD2E41', "td:has-text('Encerramento enviado')"), 0.8, at=c.A(3, 'selo', 0.6), label='selo Encerramento enviado')
    c.mark(4)
    c.waitfor(target=LINHA('FKD2E41', ":text-is('Encerrado')"), timeout=15)
    c.hover(LINHA('FKD2E41', "td:has-text('Encerrado')"), 0.8, at=c.A(4, 'encerrado.', 0.6), label='selo Encerrado')
    c.hover(CARTAO('MDF-e Encerrados'), 1.0, at=c.A(4, 'encerrados.', 0.6), label='MDF-e Encerrados: 1')
    c.fim()
    return c


@capitulo
def cap06():
    """Notas de Serviço: a lista (14 ainda não existe: 13 e 12), mercadoria × serviço (ilustração), colunas e Configurações Fiscais."""
    c = Cap(6, start=(900, 440), setup=setup_em('/fiscal-ambiental/transporte', aquece=['/fiscal-ambiental/nfse']))
    c.mark(1)
    c.click(ITEM_MENU('Notas de Serviço (NFS-e)'), at=c.A(1, 'Notas', 0.9), label='Notas de Serviço (NFS-e) no menu')
    c.waitfor(text=PAGINAS['/fiscal-ambiental/nfse'], timeout=15)
    c.mark(2)
    c.cursor(NEUTRO, at=c.L(2) - 0.2, label='cursor em repouso (ilustração mercadoria × serviço)')
    c.marca_ja(3)
    c.mark(4)
    c.registra(SEL('main thead'), at=c.A(4, 'lista', 0.3), label='colunas da lista (zoom)')
    c.hover(SEL("main th:has-text('Número')"), 0.2, at=c.A(4, 'número,', 0.6), label='coluna Número')
    c.hover(SEL("main th:has-text('Tomador')"), 0.3, at=c.A(4, 'tomador,', 0.6), label='coluna Tomador')
    c.hover(SEL("main th:has-text('Valor')"), 0.2, at=c.A(4, 'valor', 0.6), label='coluna Valor')
    c.hover(SEL("main th:has-text('Status')"), 0.4, at=c.A(4, 'status.', 0.6), label='coluna Status')
    c.mark(5)
    c.hover(BTN('Configurações Fiscais'), 1.2, at=c.A(5, 'Configurações', 0.6), label='Configurações Fiscais', noScroll=True)
    c.cursor(NEUTRO, at=c.A(5, 'contador.', 0.2), label='cursor sai do botão')
    c.fim()
    return c


@capitulo
def cap07():
    """Nova NFS-e para a Aços Quiririm: competência 06/11, coleta e remoção de resíduos, R$ 1.850,00, emitir; nº 14 autorizada."""
    c = Cap(7, start=(900, 440), setup=setup_em('/fiscal-ambiental/nfse'))
    c.mark(1)
    c.click(BTN('Nova NFS-e'), at=c.A(1, 'Nova', 1.0), label='Nova NFS-e')
    c.waitfor(text='Data de competência', timeout=10)
    c.mark(2)
    c.click(SEL("[role=dialog] label[for='nfse-competencia']"), at=c.A(2, 'competência', 0.6), label='Data de competência (campo)')
    c.type(SEL('#nfse-competencia'), '06112026', at=c.A(2, 'seis', 0.1), label='Data de competência: 06/11/2026', cps=40, noClick=True)
    c.click(SEL('[role=dialog] button', hasText='Cliente ou fornecedor'), at=c.A(2, 'tomador,', 0.7), label='Tomador: Cliente ou fornecedor')
    c.waitfor(text='Selecionar tomador', timeout=10)
    c.type(PH('Buscar por nome, CNPJ/CPF ou código...'), 'Aços', at=c.A(2, 'escolho', 0.2), label='busca: Aços', cps=12, noClick=True)
    c.click(TXTX('Aços Quiririm Ltda', within='[role=dialog] >> nth=-1'), at=c.A(2, 'Quiririm', 0.6), label='Aços Quiririm Ltda')
    c.mark(3)
    c.click(BTN('Avançar'), at=c.A(3, 'Avançar.', 0.7), label='Avançar (Serviço)')
    c.hover(SEL('[role=dialog] button', hasText='Taubaté'), 0.6, at=c.A(3, 'Taubaté.', 0.6), label='Município: Taubaté')
    c.click(SEL('[role=dialog] button[role=combobox]', hasText='Selecionar código de tributação'), at=c.A(3, 'código', 0.7), label='Código de Tributação Nacional (abre)')
    c.type(PH('Buscar por código ou descrição...'), 'coleta', at=c.A(3, 'contador', 0.2), label='busca: coleta', cps=12, noClick=True)
    c.click(OPTX('Varrição, coleta, remoção'), at=c.A(3, 'coleta', 0.6), label='código: coleta e remoção de resíduos')
    c.mark(4)
    c.hover(SEL('[role=dialog] button', hasText='Puxar serviço salvo'), 1.2, at=c.A(4, 'puxar', 0.6), label='Puxar serviço salvo')
    c.mark(5)
    c.click(SEL('#nfse-discriminacao'), at=c.A(5, 'descrição,', 0.7), label='Descrição do serviço (campo)')
    c.colar('#nfse-discriminacao', 'Coleta e remoção de resíduos metálicos com caçamba no pátio da Aços Quiririm em 06/11/2026.',
            at=c.A(5, 'feito,', 0.1), label='Descrição do serviço')
    c.mark(6)
    c.click(BTN('Avançar'), at=c.A(6, 'Avançar.', 0.7), label='Avançar (Valores)')
    c.click(SEL('#nfse-valor'), at=c.A(6, 'valor', 0.6), label='Valor do serviço (campo)')
    c.type(SEL('#nfse-valor'), '1850', at=c.A(6, 'mil', 0.1), label='Valor do serviço: 1850', cps=12, noClick=True)
    c.mark(7)
    # 1.59.154: a alíquota da lista do município fica em service.issAliquota e não chega ao campo "Alíquota ISS %" da aba Valores
    # (NovaNfseModal.tsx: estado issAliquota separado; vem 0,00). O robô digita os 3 % que o contador passou (proposta de fala).
    c.click(SEL('#nfse-iss-aliq'), at=c.A(7, 'alíquota', 0.7), label='Alíquota ISS % (campo)')
    c.type(SEL('#nfse-iss-aliq'), '3', at=c.A(7, 'alíquota', -0.5), label='Alíquota ISS %: 3', cps=12, noClick=True, clear=True)
    c.hover(SEL('#nfse-iss-aliq'), 0.8, at=c.A(7, 'contador.', 0.9), label='Alíquota ISS %: 3,00 (o contador confirma)')
    c.mark(8)
    c.click(BTN('Avançar'), at=c.L(8) - 0.2, label='Avançar (Pré-visualização)')
    c.hover(TXTX('Pronta pra emitir', within=DLG), 0.8, at=c.A(8, 'selo', 0.6), label='selo Pronta pra emitir')
    c.mark(9)
    c.click(BTN('Emitir NFS-e'), at=c.A(9, 'Emitir', 0.7), label='Emitir NFS-e')
    c.waitfor(target=LINHA('#14', ":text-is('Processando')"), timeout=10)
    c.hover(LINHA('#14', "td:has-text('Processando')"), 0.6, at=c.A(9, 'processando.', 0.6), label='nº 14 Processando')
    c.mark(10)
    c.waitfor(target=LINHA('#14', ":text-is('Autorizada')"), timeout=15)
    c.hover(LINHA('#14', 'td >> nth=0'), 1.0, at=c.A(10, 'catorze.', 0.6), label='nº 14 Autorizada')
    c.mark(11)
    c.click(LINHA('#14', 'button[aria-haspopup=menu]'), at=c.A(11, 'menu,', 0.8), label='Ações da nº 14 (menu)')
    c.hover(ITEM('Baixar PDF'), 0.6, at=c.A(11, 'PDF', 0.6), label='Baixar PDF', noScroll=True)
    c.hover(ITEM('Histórico'), 0.8, at=c.A(11, 'Histórico.', 0.6), label='Histórico', noScroll=True)
    c.press('Escape', at=round(c.W(11, 'Histórico.') + 0.9, 2), label='fecha o menu')
    c.fim()
    return c


@capitulo
def cap08():
    """NFS-e recebidas: Notas Fiscais > Notas Recebidas > NFS-e, ativar, 2 notas chegam, lançar a da balança como conta."""
    c = Cap(8, start=(900, 440), setup=setup_em('/fiscal-ambiental/nfse', aquece=['/fiscal-ambiental/nfe/saida']))
    c.mark(1)
    c.click(ITEM_MENU('Notas Fiscais (NF-e)'), at=c.A(1, 'Notas', 0.9), label='Notas Fiscais (NF-e) no menu')
    c.click(SUBABA('Notas Recebidas'), at=c.A(1, 'Recebidas,', 0.7), label='aba Notas Recebidas')
    c.click(TAB('NFS-e'), at=c.A(1, 'NFS-e.', 0.6), label='aba NFS-e')
    c.waitfor(text='Ative as Notas de Serviço Recebidas', timeout=10)
    c.mark(2)
    c.hover(TXTX('prestadores emitem contra o CNPJ', within='main'), 1.0, at=c.A(2, 'CNPJ:', 0.6), label='texto: notas emitidas contra o CNPJ')
    c.mark(3)
    c.click(BTN('Ativar NFS-e Recebidas'), at=c.A(3, 'Ativar', 0.8), label='Ativar NFS-e Recebidas')
    c.waitfor(text='Ativar o recebimento de notas de serviço?', timeout=10)
    c.hover(TXTX('cada nota de serviço recebida passa a contar', within=DLG), 1.0, at=c.A(3, 'aviso:', 0.6), label='aviso da cota')
    c.mark(4)
    c.click(BTN('Ativar mesmo assim'), at=c.A(4, 'Ativar', 0.7), label='Ativar mesmo assim')
    c.waitfor(text='Balanças Tremembé Manutenção Ltda', timeout=15)
    c.hover(SEL('main tbody'), 0.6, at=c.A(4, 'duas.', 0.6), label='duas notas recebidas')
    c.mark(5)
    c.hover(LINHA('Contabilidade Manacá', 'td >> nth=0'), 0.6, at=c.A(5, 'honorários', 0.6), label='Contabilidade Manacá Ltda R$ 1.650,00')
    c.registra(SEL('main tbody'), label='colunas Prestador e Valor (zoom)')
    c.hover(LINHA('Balanças Tremembé', 'td >> nth=0'), 0.6, at=c.A(5, 'aferição', 0.6), label='Balanças Tremembé R$ 980,00')
    c.mark(6)
    c.hover(TXTX('A NFS-e é da prefeitura', within='main'), 1.2, at=c.A(6, 'cidade', 0.6), label='aviso: só chega nota de cidade do sistema nacional')
    c.mark(7)
    c.click(LINHA('Balanças Tremembé', 'button[aria-haspopup]'), at=c.A(7, 'linha', 0.7), label='Ações da nota da balança')
    c.click(ITEM('Lançar despesa / conta'), at=c.A(7, 'Lançar', 0.6), label='Lançar despesa / conta', noScroll=True)
    c.waitfor(text='Nova conta', timeout=10)
    c.mark(8)
    c.hover(SEL('#bill-amount'), 0.6, at=c.A(8, 'valor', 0.6), label='Valor R$ 980,00 já preenchido')
    c.click(SEL('#bill-due'), at=c.A(8, 'vencimento,', 0.7), label='Vencimento (abre o calendário)')
    c.click(SEL("[data-radix-popper-content-wrapper] button[name=day]:text-is('20')"), at=c.A(8, 'vinte,', 0.5), label='Vencimento: 20/11/2026')
    c.click(SEL('#bill-category'), at=c.A(8, 'categoria.', 0.9), label='Categoria (abre)')
    c.type(PH('Pesquisar categoria...'), 'manut', at=c.A(8, 'categoria.', 0.3), label='busca: manut', cps=40, noClick=True)
    c.click(OPTX('Manutenção de máquinas'), at=c.A(8, 'Criar', 0.5), label='Categoria: Manutenção de máquinas')
    c.click(BTN('Criar conta'), at=c.A(8, 'Criar', 0.0), label='Criar conta')
    c.waitfor(target=LINHA('Balanças Tremembé', ":text-is('Lançada')"), timeout=10)
    c.hover(LINHA('Balanças Tremembé', "td:has-text('Lançada')"), 1.0, at=c.A(8, 'lançada.', 0.6), label='selo Lançada')
    c.fim()
    return c


PERIODO = SEL('main button[role=combobox]', hasText='Este mês')   # filtro de período do cabeçalho (y ~92, fora da faixa 96..730: fixo=True)


@capitulo
def cap09():
    """Estoque Fiscal > Relatório fiscal de outubro: Entrada, Saída, Saldo R$ 71.625,00, Pendentes + Rejeitadas e os gráficos."""
    c = Cap(9, start=(900, 440), setup=setup_em('/fiscal-ambiental/nfe/recebidas-nfse', aquece=['/fiscal-ambiental/estoque-fiscal/relatorio']))
    c.mark(1)
    c.click(ITEM_MENU('Estoque Fiscal'), at=c.A(1, 'Estoque', 0.9), label='Estoque Fiscal no menu')
    c.waitfor(text='Pendentes + Rejeitadas', timeout=15)
    c.hover(SUBABA('Relatório fiscal'), 0.5, at=c.A(1, 'Relatório', 0.6), label='aba Relatório fiscal')
    escolhe(c, PERIODO, 'Mês passado', c.A(1, 'Escolho', 0.7), c.A(1, 'passado,', 0.4), 'período: Mês passado', fixo=True)
    c.mark(2)
    c.hover(CARTAO('Entrada'), 0.6, at=c.A(2, 'entrou', 0.6), label='cartão Entrada')
    c.hover(CARTAO('Saída'), 0.6, at=c.A(2, 'saiu', 0.6), label='cartão Saída')
    c.mark(3)
    c.hover(CARTAO('Saldo (Saída − Entrada)'), 1.4, at=c.A(3, 'saldo', 0.6), label='cartão Saldo (Saída − Entrada)')
    c.mark(4)
    c.hover(CARTAO('Pendentes + Rejeitadas'), 1.4, at=c.A(4, 'último', 0.6), label='cartão Pendentes + Rejeitadas')
    c.mark(5)
    rola_ate(c, 'Entrada × Saída no período', c.L(5) - 0.2, 'rola até o gráfico do mês', y=110, prefixo=True)
    c.hover(TXTX('Entrada × Saída no período', within='main'), 0.3, at=c.A(5, 'gráfico', 0.6), label='Entrada × Saída no período')
    c.hover(TXTX('Distribuição por status', within='main'), 0.3, at=c.A(5, 'status', 0.6), label='Distribuição por status')
    rola_ate(c, 'Top Fornecedores', c.A(5, 'ranking', 0.5), 'rola até os rankings', y=250, dur_ms=700, prefixo=True)
    c.hover(TXTX('Top Fornecedores', within='main'), 0.3, at=c.A(5, 'fornecedores', 0.6), label='Top Fornecedores')
    c.hover(TXTX('Top Clientes', within='main'), 0.6, at=c.A(5, 'clientes.', 0.6), label='Top Clientes')
    c.fim()
    return c


@capitulo
def cap10():
    """Posição do estoque (agora e 31/10 18:00), Histórico fiscal do metal amarelo e Fiscal × operacional (Delta) com a dica."""
    # o período do cabeçalho (o mesmo das abas Relatório e Fiscal × operacional) fica em "Mês passado" desde o cap09: escolhido no setup
    c = Cap(10, start=(900, 440), setup=setup_em('/fiscal-ambiental/estoque-fiscal/relatorio', extra=[
        {'do': 'click', 'target': PERIODO, 'noScroll': True}, {'do': 'click', 'target': OPT('Mês passado')},
        {'do': 'waitFor', 'text': 'R$ 71.625,00', 'timeout': 15}, {'do': 'wait', 'seconds': 0.8}]))
    c.mark(1)
    c.click(SUBABA('Posição do estoque'), at=c.A(1, 'Posição', 0.8), label='aba Posição do estoque')
    c.hover(TXTX('Saldo fiscal agora, por material.', within='main'), 0.8, at=c.A(1, 'saldo', 0.6), label='Saldo fiscal agora, por material')
    c.hover(SEL('main tbody tr >> nth=0'), 0.6, at=c.A(1, 'material,', 0.6), label='tabela do saldo fiscal')
    c.mark(2)
    c.click(SEL('main button', hasText='10/11/2026'), at=c.A(2, 'data', 0.7), label='Data da posição (abre)')
    c.click(SEL('[data-radix-popper-content-wrapper] button[name=previous-month]'), at=c.A(2, 'hora,', 0.5), label='mês anterior')
    c.click(SEL("[data-radix-popper-content-wrapper] button[name=day]:text-is('31')"), at=c.A(2, 'fim', 0.6), label='dia 31/10')
    # a hora: o cursor vai ao campo e o foco entra pelo começo (clique no meio do campo cairia nos minutos)
    c.hover(SEL("main input[aria-label='Hora']"), 0.1, at=c.A(2, 'outubro,', 0.6), label='Hora (campo)')
    c.ev("(()=>{const i=document.querySelector(\"main input[aria-label='Hora']\");if(!i)return 'SEM ALVO';i.focus();return 'foco na hora'})()")
    c.type(SEL("main input[aria-label='Hora']"), '1800', label='Hora: 18:00', cps=14, noClick=True)
    c.click(BTN('Ver posição'), at=c.A(2, 'Ver', 0.7, nth=1), label='Ver posição')
    c.mark(3)
    c.hover(TXTX('Saldo fiscal em', within='main'), 0.8, at=c.A(3, 'consulta.', 0.6), label='Saldo fiscal em 31/10')
    c.hover(BTN('Voltar para agora'), 1.0, at=c.A(3, 'passado,', 0.6), label='Voltar para agora')
    c.click(BTN('Voltar para agora'), at=c.A(3, 'futuro.', 0.2), label='volta para agora')
    c.mark(4)
    c.click(SUBABA('Histórico fiscal'), at=c.A(4, 'Histórico', 0.7), label='aba Histórico fiscal')
    c.click(TXTX('Metal amarelo (latão)', within='main'), at=c.A(4, 'metal', 0.7), label='Materiais: Metal amarelo (latão)')
    c.hover(LINHA('1248', 'td >> nth=0'), 0.6, at=c.A(4, 'saída,', 0.6), label='saída de 30/10 (NF-e 1248, 600 kg)')
    c.hover(SEL("main th:has-text('Antes')"), 0.6, at=c.A(4, 'antes', 0.6), label='colunas Antes e Depois')
    c.mark(5)
    c.click(SUBABA('Fiscal × operacional'), at=c.A(5, 'última', 0.7), label='aba Fiscal × operacional')
    c.hover(TXTX('Comparação por material', within='main'), 0.4, at=c.A(5, 'lado', 0.6), label='Comparação por material')
    rola_ate(c, 'Metal amarelo (latão)', c.A(5, 'Repara', 0.9), 'rola até o metal amarelo', y=420, dur_ms=900)
    c.hover(LINHA('Metal amarelo', "td >> nth=-1"), 1.2, at=c.A(5, 'amarelo:', 0.5), label='Metal amarelo: Mov. Fiscal, Mov. Operacional e Delta')
    c.mark(6)
    c.cursor(NEUTRO, at=c.L(6) - 0.2, label='cursor em repouso (ilustração fiscal × operacional)')
    c.marca_ja(7)
    c.mark(8)
    rola_ate(c, 'Como ler o Delta (fiscal − operacional)', c.L(8) - 0.2, 'rola até Como ler o Delta', y=260, prefixo=True)
    c.hover(TXTX('Pedidos ainda não finalizados', within='main'), 1.4, at=c.A(8, 'quadro,', 0.6), label='Como ler o Delta')
    c.fim()
    return c


@capitulo
def cap11():
    """Exportação Contábil: Notas Fiscais > Saída > ⋮ > Exportação Contábil, Mês passado, tudo marcado, 21 notas, Baixar Pacote."""
    c = Cap(11, start=(900, 440), setup=setup_em('/fiscal-ambiental/estoque-fiscal/relatorio', aquece=['/fiscal-ambiental/nfe/saida']))
    c.mark(1)
    c.click(ITEM_MENU('Notas Fiscais (NF-e)'), at=c.A(1, 'Notas', 0.9), label='Notas Fiscais (NF-e) no menu')
    c.click(SUBABA('Saída'), at=c.A(1, 'Fiscais,', 0.0), label='aba Saída')
    c.click(SEL("main button[aria-label='Mais opções de NF-e']"), at=c.A(1, 'três', 0.7), label='Mais opções de NF-e (⋮)')
    c.click(ITEM('Exportação Contábil'), at=c.A(1, 'Exportação', 0.6), label='Exportação Contábil', noScroll=True)
    c.waitfor(text='Baixar Pacote', timeout=10)
    c.mark(2)
    c.hover(TXTX('Gera um pacote ZIP com XMLs', within=DLG), 1.2, at=c.A(2, 'XML', 0.6), label='descrição do pacote')
    c.mark(3)
    escolhe(c, SEL('[role=dialog] button[role=combobox] >> nth=0'), 'Mês passado', c.A(3, 'período,', 0.6), c.A(3, 'passado.', 0.3), 'Período: Mês passado')
    c.mark(4)
    c.hover(TXT('Tipo de nota', within=DLG), 0.6, at=c.A(4, 'Saída', 0.6), label='Tipo de nota: Saída e Entrada')
    c.hover(TXT('Status', within=DLG), 0.8, at=c.A(4, 'status,', 0.6), label='Status: todos marcados')
    c.mark(5)
    c.hover(TXTX('Incluir DANFEs (PDFs)', within=DLG), 0.6, at=c.A(5, 'PDF', 0.6), label='Incluir DANFEs (PDFs)')
    c.hover(TXTX("Incluir MDF-e", within=DLG), 0.8, at=c.A(5, 'manifestos', 0.6), label="Incluir MDF-e's")
    c.mark(6)
    c.hover(TXTX('notas no período', within=DLG), 1.4, at=c.A(6, 'prévia', 0.6), label='prévia: 21 notas no período')
    c.mark(7)
    c.click(BTN('Baixar Pacote'), at=c.A(7, 'Baixar', 0.7), label='Baixar Pacote')
    c.waitfor(text='Exportação pronta', timeout=40)
    c.cursor(NEUTRO, at=c.A(7, 'computador.', 0.2), label='cursor em repouso (download)')
    c.fim()
    return c


@capitulo
def cap12():
    """O que o contador faz: só ilustração (o pacote, o caminho até o contador, a cópia guardada); a tela fica parada na lista de Saída."""
    c = Cap(12, start=(900, 470), setup=setup_em('/fiscal-ambiental/nfe/saida'))
    c.mark(1)
    c.cursor(NEUTRO, at=0.5, label='cursor em repouso (ilustração do pacote)')
    for i in (2, 3, 4):
        c.marca_ja(i)
    c.fim()
    return c


@capitulo
def cap13():
    """Recapitulando: montagem das gravações dos capítulos 2 a 11 por cima; a tela fica parada em Transporte com o nº 1 encerrado."""
    c = Cap(13, start=(900, 470), setup=setup_em('/fiscal-ambiental/transporte'))
    c.mark(1)
    c.cursor(NEUTRO, at=0.5, label='cursor em repouso (montagem)')
    for i in (2, 3, 4):
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
