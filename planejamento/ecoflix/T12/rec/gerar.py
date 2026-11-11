#!/usr/bin/env python3
"""T12 · Coletas e Logística: gera rec/t12/cap00..cap11.json (roteiros do robô) a partir da voz (t12/narracao/capNN.json).

EcoSistema 1.59.154 no Supabase falso (mundo da Recicla Vale Metais), computador 1280x800, logado como Rafael Nogueira (MASTER).
Cada passo é preso a uma palavra da fala: `at` = início da palavra - folga (o custo do gesto, docs/04 "Custo real dos gestos"), e a marca
Ln entra no início de cada linha. Quando a voz chegar, rodar de novo com o capNN.json da voz (nada a reescrever).
O cap12 (Recapitulando) é montagem das gravações dos capítulos 2 a 11: sem robô.
Rodar de qualquer pasta: `python3 -I rec/t12/gerar.py [NN ...]`; gravar/ensaiar: `bash rec/t12/t12_grava.sh NN [--rapido]`.

Relógio (MUNDO_LINHA_DO_TEMPO.md, "O dia 10/11"): FAKE_NOW 10/11/2026 07:00 em todos os capítulos (a troca da caçamba é antes da balança do
T8, 08:40, e da viagem da T17, 09:40).
Cadeia de sementes (seeds-extra/t12; inicio = t12_sementes.py; as outras saem de t12_semente.py, do estado da instância 54312 logo depois do
ensaio do capítulo): inicio -> apos-cap05 (ordem 9) -> apos-cap06 (ordem 8 concluída, caçambas 03 e 05) -> apos-cap07 (ordem 10 do portal,
agendada) -> apos-cap08 (FVL8A52, Sérgio Paiva) -> apos-cap09 (Caçamba 06 na base). O cap10 só lê; o cap11 parte de apos-cap09.
Particularidades:
 - A ordem interna nasce "Agendada" e o app não grava evento de criação: o Histórico da ordem 8 mostra só as mudanças de etapa.
 - Tela da ordem: o rodapé "Concluir coleta" é fixo (y ~770, fora da faixa 96..730 do clique): clicar_fixo.
 - GPS: o computador do robô não tem permissão de localização; o `setup` do cap06 dá ao navegador uma posição fictícia perto do Depósito
   Irmãos Siqueira (GPS_FICTICIO), para a tela da ordem registrar a posição sem a nota "Localização não registrada".
 - Portal (cap07): mesma aba (o vídeo grava uma aba só); o robô entra logado (setup), abre o portal da Cooperativa Recomeço e, depois do
   pedido, volta ao sistema pela rota /coletas/frota (o menu revalida as solicitações não vistas e mostra o ponto vermelho).
"""
import hashlib
import json
import os
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TUT = os.path.normpath(os.path.join(HERE, '..', '..'))
NARR = os.path.join(TUT, 't12', 'narracao')
NOW = '2026-11-10T07:00:00-03:00'
FAKE_NOW = {n: NOW for n in range(12)}
TOKEN_COOP = hashlib.sha1(b'ecoflix-t12-portal-recomeco').hexdigest()[:32]   # o mesmo de t12_sementes.py


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
NOMES = ['Abertura', 'O que o módulo de Coletas resolve', 'O quadro das ordens', 'Criar uma ordem', 'Data e janela', 'Motorista e veículo',
         'Acompanhar até concluir', 'A coleta pedida pelo portal', 'Veículos e motoristas', 'As caçambas e onde estão', 'O relatório das coletas',
         'As regras das coletas']
SEMENTE = {0: None, 1: None, 2: None, 3: None, 4: None, 5: None, 6: 'apos-cap05', 7: 'apos-cap06', 8: 'apos-cap07', 9: 'apos-cap08',
           10: 'apos-cap09', 11: 'apos-cap09'}


def sementes(n):
    """a semente de cada capítulo é cumulativa (tudo desde o início da aula): só a última da cadeia vai junto da base"""
    return ['t12/inicio'] + ([f't12/{SEMENTE[n]}'] if SEMENTE[n] else [])


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

# GPS fictício (cap06): o navegador do robô no computador não tem permissão de localização; a posição fica perto do Depósito Irmãos
# Siqueira (Tremembé), nunca aparece na tela (o rastreamento está fora da aula) e só evita a nota "Localização não registrada".
GPS_FICTICIO = ("(()=>{const p=()=>({coords:{latitude:-22.9668,longitude:-45.5416,accuracy:12,altitude:null,altitudeAccuracy:null,heading:null,"
                "speed:null},timestamp:Date.now()});const g=navigator.geolocation;g.getCurrentPosition=(ok)=>setTimeout(()=>ok(p()),120);"
                "g.watchPosition=(ok)=>{setTimeout(()=>ok(p()),300);return 7};g.clearWatch=()=>{};return 'gps ficticio'})()")


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
        d = {
            'name': f't12-cap{s.n:02d}',
            'title': f'T12 · Cap. {s.n} · {NOMES[s.n]} (narração {str(round(s.dur, 1)).replace(".", ",")} s{" ESTIMADA" if s.estimada else ""}; '
                     f'marcas L1..L{len(s.linhas)} = início de cada linha do roteiro; FAKE_NOW {FAKE_NOW[s.n]})',
            'seed': f't12-cap{s.n:02d}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
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
CARTAO = lambda num: f"main div.rounded-lg:has(> div span.font-semibold:text-is('#{num}'))"     # cartão #N do quadro
COLUNA = lambda titulo: f"main div:has(> div :text-is('{titulo}'))"


def js_clicar(sel, texto=None):
    """clique por eval (botão fixo): o primeiro `sel` visível (com o texto, se dado)"""
    filtro = f"&&(b.textContent||'').includes({json.dumps(texto)})" if texto else ''
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
    '/coletas/ordens': 'Solicite, agende e acompanhe as ordens de coleta',
    '/coletas/frota': 'Veículos e motoristas disponíveis para as coletas',
    '/coletas/equipamentos': 'Caçambas, bags, caixas e paletes em campo',
    '/coletas/relatorio': 'Indicadores e histórico das coletas',
    '/coletas/configuracoes': 'Ajuste a numeração, as janelas e as regras do portal de coletas',
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


# rolagem suave do contêiner que rola o alvo (molde do T14/T11/T8: ACHA_ROLAGEM + SUAVE): o cursor não se mexe
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


# ---------------------------------------------------------------- alvos das telas de Coletas (conferidos por exploração, rec/t12/_ex)
GRUPO = BTNX('Coletas & Logística', within=MENU)
ITEM_MENU = lambda n: LINK(n, within=MENU)
COL_T = lambda t: SEL(f"main h3:text-is('{t}')")                                  # título da coluna do quadro
CARD = lambda num, sub='': SEL(f"{CARTAO(num)} {sub}".strip())
CARD_TXT = lambda num, t: SEL(f"{CARTAO(num)} :text-is('{t}')")
CARD_BTN = lambda num, t: SEL(f"{CARTAO(num)} button:text-is('{t}')")
NOVA_ORDEM = BTN('Nova ordem')
PASSO = lambda t: SEL(f"{DLG} span:text-is('{t}')")                                # etapas da Nova ordem
AVANCAR = BTN('Avançar')
BUSCA_PARC = PH('Buscar por nome, apelido, CPF/CNPJ ou telefone...')
MOTORISTA, VEICULO = PH('Digite ou busque o motorista'), PH('Digite ou busque a placa')


def setup_nova_ordem(ate_etapa):
    """refaz fora do vídeo a Nova ordem da Auto Peças Vale Forte até a etapa pedida (2 = Coleta preenchida, 3 = Frota)"""
    st = [{'do': 'click', 'target': NOVA_ORDEM}, {'do': 'waitFor', 'text': 'Nova ordem de coleta', 'timeout': 10}, {'do': 'wait', 'seconds': 0.5},
          {'do': 'click', 'target': SEL(f"{DLG} button:has-text('Selecionar')")}, {'do': 'waitFor', 'target': BUSCA_PARC, 'timeout': 10},
          {'do': 'type', 'target': BUSCA_PARC, 'text': 'Vale Forte', 'cps': 40}, {'do': 'wait', 'seconds': 0.6},
          {'do': 'click', 'target': BTNX('Auto Peças Vale Forte', within=f'{DLG} >> nth=-1')}, {'do': 'wait', 'seconds': 0.6},
          {'do': 'click', 'target': AVANCAR}, {'do': 'waitFor', 'target': SEL('#ordem-material'), 'timeout': 10},
          {'do': 'type', 'target': SEL('#ordem-material'), 'text': '~400 kg de radiadores e baterias', 'cps': 40},
          {'do': 'type', 'target': SEL('#ordem-obs'), 'text': 'Retirar pelo portão lateral', 'cps': 40}]
    if ate_etapa >= 3:
        st += [{'do': 'type', 'target': SEL('#ordem-data'), 'text': '11112026', 'cps': 40},
               {'do': 'click', 'target': SEL('#ordem-janela')}, {'do': 'click', 'target': OPT('Manhã')}, {'do': 'wait', 'seconds': 0.4},
               {'do': 'click', 'target': AVANCAR}, {'do': 'waitFor', 'target': MOTORISTA, 'timeout': 10}]
    return st + [{'do': 'wait', 'seconds': 0.8}]


@capitulo
def cap00():
    """Abertura: ilustração e cartões sobre o Dashboard; depois o menu Coletas & Logística > Ordens de Coleta."""
    c = Cap(0, start=(700, 430), setup=setup_em('/dashboard', aquece=['/coletas/ordens']))
    c.mark(1)
    c.cursor((720, 440), at=0.5, label='cursor em repouso no Dashboard')
    for i in (2, 3, 4):
        c.mark(i)
        c.flush(1e9)
    c.mark(5)
    c.hover(GRUPO, 0.3, at=c.A(5, 'menu', 0.5), label='menu Coletas & Logística')
    c.click(GRUPO, at=c.A(5, 'Coletas', 0.3), label='abre Coletas & Logística')
    c.click(ITEM_MENU('Ordens de Coleta'), at=c.A(5, 'Ordens', 0.8), label='Ordens de Coleta')
    c.waitfor(text=PAGINAS['/coletas/ordens'], timeout=15)
    c.cursor((760, 470), at=c.A(5, 'Antes', 0.2), label='cursor sai do menu (o quadro abre)')
    c.fim()
    return c


@capitulo
def cap01():
    """O que o módulo resolve: a câmera passa pelo quadro, sem clicar; as ilustrações cobrem as linhas 2 a 4."""
    c = Cap(1, start=(760, 420), setup=setup_em('/coletas/ordens'))
    c.mark(1)
    c.hover(COL_T('Agendada'), 0.6, at=c.A(1, 'buscar', 0.5), label='quadro: coluna Agendada')
    c.hover(CARD_TXT(8, 'Depósito Irmãos Siqueira'), 0.8, at=c.A(1, 'caçamba', 0.5), label='cartão da troca de caçamba (#8)')
    c.hover(CARD_TXT(7, 'Marcelo Tavares'), 0.8, at=c.A(1, 'combina', 0.5), label='cartão do Marcelo (#7)')
    c.cursor((760, 460), at=c.A(1, 'dele', 0.3), label='cursor em repouso')
    for i in (2, 3, 4):
        c.mark(i)
        c.flush(1e9)
    c.fim()
    return c


@capitulo
def cap02():
    """O quadro: colunas, cartões #8 e #7, filtros, Quadro/Lista e Nova ordem; a dica das concluídas e canceladas."""
    c = Cap(2, start=(760, 420), setup=setup_em('/coletas/ordens'))
    c.mark(1)
    c.hover(COL_T('Solicitada'), 0.25, at=c.A(1, 'Solicitada', 0.5), label='coluna Solicitada')
    c.hover(COL_T('Agendada'), 0.25, at=c.A(1, 'Agendada', 0.5), label='coluna Agendada')
    c.hover(COL_T('A caminho'), 0.2, at=c.A(1, 'caminho', 0.6), label='coluna A caminho')
    c.hover(COL_T('Concluídas'), 0.4, at=c.A(1, 'Concluídas', 0.5), label='coluna Concluídas')
    c.hover(COL_T('Cancelada'), 0.6, at=c.A(1, 'canceladas', 0.5), label='coluna Cancelada')
    c.mark(2)
    c.hover(TXT('Nenhuma ordem', within='main'), 1.2, at=c.A(2, 'Solicitada', 0.5), label='Solicitada vazia (Nenhuma ordem)')
    c.mark(3)
    c.hover(CARD_TXT(8, '#8'), 0.3, at=c.A(3, 'número', 0.5), label='cartão #8: número')
    c.hover(CARD_TXT(8, 'Depósito Irmãos Siqueira'), 0.3, at=c.A(3, 'parceiro', 0.5), label='cartão #8: parceiro')
    c.hover(CARD(8, ":text-is('Manhã')"), 0.3, at=c.A(3, 'período', 0.5), label='cartão #8: período')
    c.hover(CARD_TXT(8, 'Edson Moura'), 0.3, at=c.A(3, 'motorista', 0.5), label='cartão #8: motorista')
    c.hover(CARD_TXT(8, 'FKD2E41'), 0.6, at=c.A(3, 'placa', 0.5), label='cartão #8: placa')
    c.hover(CARD_TXT(8, 'Depósito Irmãos Siqueira'), 1.0, at=c.A(3, 'Depósito', 0.5), label='cartão #8: a troca de caçamba do Siqueira')
    c.mark(4)
    c.hover(CARD_TXT(7, 'Tiago Freitas'), 0.6, at=c.A(4, 'Tiago', 0.5), label='cartão #7: Tiago Freitas')
    c.hover(CARD_TXT(7, 'Marcelo Tavares'), 0.8, at=c.A(4, 'Marcelo', 0.5), label='cartão #7: Marcelo Tavares')
    c.hover(CARD_TXT(7, 'Sem cadastro'), 1.0, at=c.A(4, 'cadastro', 0.9), label='cartão #7: Sem cadastro')
    c.mark(5)
    c.hover(BTNX('Filtros', within='main'), 0.6, at=c.A(5, 'filtros', 0.5), label='Filtros')
    c.hover(SEL("main [aria-label='Lista']"), 0.6, at=c.A(5, 'troca', 0.5), label='Quadro / Lista')
    c.hover(NOVA_ORDEM, 0.8, at=c.A(5, 'Nova', 0.5), label='Nova ordem')
    c.mark(6)
    c.cursor((760, 470), at=c.A(6, 'anda', 0.3), label='cursor em repouso (a dica)')
    c.hover(COL_T('Concluídas'), 0.4, at=c.A(6, 'Concluída', 0.5), label='dica: coluna Concluídas')
    c.hover(COL_T('Cancelada'), 1.2, at=c.A(6, 'cancelada', 0.5), label='dica: coluna Cancelada')
    c.fim()
    return c


@capitulo
def cap03():
    """Criar uma ordem: Nova ordem, as etapas, Cadastrado/Sem cadastro, Tipo, Parceiro (Auto Peças Vale Forte), endereço do cadastro,
    Avançar, Material estimado e Observações."""
    c = Cap(3, start=(900, 300), setup=setup_em('/coletas/ordens'))
    c.mark(1)
    c.click(NOVA_ORDEM, at=c.A(1, 'Nova', 0.8), label='Nova ordem')
    c.waitfor(text='Nova ordem de coleta', timeout=10)
    c.hover(PASSO('Parceiro'), 0.2, at=c.A(1, 'Parceiro', 0.5), label='etapa Parceiro')
    c.hover(PASSO('Coleta'), 0.2, at=c.A(1, 'Coleta', 0.5), label='etapa Coleta')
    c.hover(PASSO('Frota'), 0.5, at=c.A(1, 'Frota', 0.5), label='etapa Frota')
    c.mark(2)
    c.hover(TXTX('Cadastrado', within=DLG, exact=True), 0.8, at=c.A(2, 'Cadastrado', 0.5), label='Cadastrado')
    c.hover(TXTX('Sem cadastro', within=DLG, exact=True), 1.2, at=c.A(2, 'Sem', 0.5), label='Sem cadastro')
    c.mark(3)
    c.hover(SEL('#ordem-tipo'), 0.8, at=c.A(3, 'Fornecedor', 0.5), label='Tipo: Fornecedor')
    c.click(SEL(f"{DLG} button:has-text('Selecionar')"), at=c.A(3, 'Parceiro', 0.8), label='Parceiro: Selecionar…')
    c.waitfor(target=BUSCA_PARC, timeout=10)
    c.type(BUSCA_PARC, 'Vale Forte', at=c.A(3, 'busco', 0.05), label='busca Vale Forte', cps=40, noClick=True)
    c.click(BTNX('Auto Peças Vale Forte', within=f'{DLG} >> nth=-1'), at=c.A(3, 'Vale', 0.8, nth=0), label='escolhe Auto Peças Vale Forte')
    c.mark(4)
    c.hover(SEL(f"{DLG} input[placeholder='Rua']"), 0.8, at=c.A(4, 'endereço', 0.5), label='endereço do cadastro')
    c.hover(SEL(f"{DLG} input[placeholder='Cidade']"), 0.8, at=c.A(4, 'cadastro', 0.5), label='endereço do cadastro (cidade)')
    c.mark(5)
    c.click(AVANCAR, at=c.A(5, 'Avançar', 0.8), label='Avançar')
    c.click(SEL('#ordem-material'), at=c.A(5, 'Material', 0.8), label='Material estimado (campo)')
    c.type(SEL('#ordem-material'), '~400 kg de radiadores e baterias', at=c.A(5, 'uns', 0.05), label='Material estimado', cps=40, noClick=True)
    c.mark(6)
    c.click(SEL('#ordem-obs'), at=c.A(6, 'Observações', 0.8), label='Observações (campo)')
    c.type(SEL('#ordem-obs'), 'Retirar pelo portão lateral', at=c.A(6, 'retirar', 0.05), label='Observações', cps=40, noClick=True)
    c.fim()
    return c


@capitulo
def cap04():
    """Data e janela: Data agendada 11/11/2026, Período (Manhã, Tarde, Dia todo) -> Manhã, Avançar."""
    c = Cap(4, start=(900, 300), setup=setup_em('/coletas/ordens', extra=setup_nova_ordem(2)))
    c.mark(1)
    c.hover(SEL('#ordem-data'), 0.4, at=c.A(1, 'Data', 0.5), label='Data agendada')
    c.hover(SEL('#ordem-janela'), 0.4, at=c.A(1, 'Período', 0.5, nth=1), label='Período')
    c.mark(2)
    c.click(SEL('#ordem-data'), at=c.A(2, 'amanhã', 0.8), label='Data agendada (campo)')
    c.type(SEL('#ordem-data'), '11112026', at=c.A(2, 'onze', 0.3), label='Data agendada 11/11/2026', cps=40, noClick=True)
    c.mark(3)
    c.click(SEL('#ordem-janela'), at=c.A(3, 'Período', 0.8), label='abre Período')
    c.hover(OPT('Manhã'), 0.2, at=c.A(3, 'manhã', 0.5), label='opção Manhã')
    c.hover(OPT('Tarde'), 0.2, at=c.A(3, 'tarde', 0.5), label='opção Tarde')
    c.hover(OPT('Dia todo'), 0.6, at=c.A(3, 'dia', 0.5, nth=1), label='opção Dia todo')
    c.mark(4)
    c.click(OPT('Manhã'), at=c.A(4, 'manhã', 0.8), label='escolhe Manhã')
    c.hover(SEL('#ordem-janela'), 1.0, at=c.A(4, 'Configurações', 0.5), label='Período: Manhã (as janelas vêm das Configurações)')
    c.mark(5)
    c.click(AVANCAR, at=c.A(5, 'Avanço', 0.8), label='Avançar para a Frota')
    c.waitfor(target=MOTORISTA, timeout=10)
    c.fim()
    return c


@capitulo
def cap05():
    """Motorista e veículo: Jair Lopes e GHT7B19, a Revisão, Criar ordem e o cartão #9 em Agendada."""
    c = Cap(5, start=(900, 300), setup=setup_em('/coletas/ordens', extra=setup_nova_ordem(3)))
    c.mark(1)
    c.hover(MOTORISTA, 0.4, at=c.A(1, 'Motorista', 0.5), label='Motorista')
    c.hover(VEICULO, 0.4, at=c.A(1, 'Veículo', 0.5), label='Veículo')
    c.mark(2)
    c.click(MOTORISTA, at=c.A(2, 'Jair', 0.6), label='Motorista (campo)')
    c.type(MOTORISTA, 'Jair', at=c.A(2, 'Jair', 0.05), label='digita Jair', cps=40, noClick=True)
    c.click(OPT('Jair Lopes'), at=c.A(2, 'com', 0.6), label='escolhe Jair Lopes')
    c.click(VEICULO, at=c.A(2, 'três', 0.6), label='Veículo (campo)')
    c.type(VEICULO, 'GHT', at=c.A(2, 'que', 0.4), label='digita GHT', cps=40, noClick=True)
    c.click(OPT('GHT7B19'), at=c.A(2, 'quatrocentos', 0.6), label='escolhe GHT7B19')
    c.mark(3)
    c.hover(TXTX('Revisão', within=DLG, exact=True), 0.4, at=c.A(3, 'Revisão', 0.5), label='Revisão')
    c.hover(TXTX('Auto Peças Vale Forte', within=DLG, exact=True), 0.3, at=c.A(3, 'parceiro', 0.5), label='Revisão: parceiro')
    c.hover(TXTX('Cidade:', within=DLG, exact=True), 0.3, at=c.A(3, 'cidade', 0.5), label='Revisão: cidade')
    c.hover(TXTX('~400 kg de radiadores e baterias', within=DLG, exact=True), 0.3, at=c.A(3, 'material', 0.5), label='Revisão: material')
    c.hover(TXTX('Data:', within=DLG, exact=True), 0.6, at=c.A(3, 'data', 0.5), label='Revisão: data e período')
    c.mark(4)
    c.click(BTN('Criar ordem'), at=c.A(4, 'Criar', 0.8), label='Criar ordem')
    c.waitfor(text='Ordem de coleta criada', timeout=10)
    c.hover(CARD_TXT(9, '#9'), 0.6, at=c.A(4, 'nove', 0.5), label='cartão #9 em Agendada')
    c.hover(CARD_TXT(9, 'Jair Lopes'), 0.4, at=c.A(4, 'Jair', 0.5), label='cartão #9: Jair Lopes')
    c.hover(CARD_TXT(9, 'GHT7B19'), 0.8, at=c.A(4, 'caminhão', 0.5), label='cartão #9: GHT7B19')
    c.mark(5)
    c.hover(CARD(9), 1.5, at=c.A(5, 'Motorista', 0.5), label='cartão #9 (frota pode ficar pra depois)')
    c.fim()
    return c


@capitulo
def cap06():
    """Acompanhar até concluir: #8 A caminho, Preencher, Recolhi Caçamba 03, Entreguei Caçamba 05, Concluir coleta, o relatório, Voltar às
    ordens e a ficha (Equipamentos movimentados e Histórico)."""
    c = Cap(6, start=(760, 420), setup=setup_em('/coletas/ordens', extra=[{'do': 'eval', 'js': GPS_FICTICIO}]))
    c.mark(1)
    c.click(CARD_BTN(8, 'A caminho'), at=c.A(1, 'A', 0.8, nth=1), label='#8: A caminho')
    c.waitfor(text='Status alterado para A caminho', timeout=10)
    c.hover(CARD_TXT(8, '#8'), 0.8, at=c.A(1, 'cartão', 0.5), label='#8 na coluna A caminho')
    c.mark(2)
    c.click(CARD_BTN(8, 'Preencher'), at=c.A(2, 'Preencher', 0.8), label='#8: Preencher')
    c.waitfor(text='Ordem #8', timeout=15)
    c.hover(TXTX('Agendamento', exact=True), 0.6, at=c.A(2, 'combinado', 0.5), label='tela da ordem: o combinado')
    c.mark(3)
    rola_ate(c, 'Equipamentos', c.A(3, 'bloco', 0.2), 'desce ao bloco Equipamentos', y=190, escopo='body')
    c.click(SEL("div:has(> :text-is('Recolhi')) button[role=combobox] >> nth=0"), at=c.A(3, 'Edson', 0.8), label='Recolhi: Tipo de equipamento')
    c.click(OPT('Caçamba 5 m³'), at=c.A(3, 'recolheu', 0.6), label='Recolhi: Caçamba 5 m³')
    c.click(SEL("div:has(> :text-is('Recolhi')) button[role=combobox] >> nth=1"), at=c.A(3, 'Caçamba', 0.8, nth=1), label='Recolhi: Unidade')
    c.click(OPT('Caçamba 03'), at=c.A(3, 'três', 0.5), label='Recolhi: Caçamba 03')
    c.click(SEL("div:has(> :text-is('Recolhi')) button:has-text('Adicionar')"), at=c.A(3, 'cheia', 0.6), label='Recolhi: Adicionar')
    c.mark(4)
    c.click(SEL("div:has(> :text-is('Entreguei')) button[role=combobox] >> nth=0"), at=c.A(4, 'deixou', 0.8), label='Entreguei: Tipo de equipamento')
    c.click(OPT('Caçamba 5 m³'), at=c.A(4, 'Caçamba', 0.6), label='Entreguei: Caçamba 5 m³')
    c.click(SEL("div:has(> :text-is('Entreguei')) button[role=combobox] >> nth=1"), at=c.A(4, 'vazia', 0.8), label='Entreguei: Unidade (só as da base)')
    c.hover(OPT('Caçamba 05'), 1.2, at=c.A(4, 'lista', 0.5), label='Entreguei: lista só com as da base')
    c.click(OPT('Caçamba 05'), at=c.A(4, 'base', 0.8), label='Entreguei: Caçamba 05')
    c.click(SEL("div:has(> :text-is('Entreguei')) button:has-text('Adicionar')"), label='Entreguei: Adicionar')
    c.mark(5)
    c.clicar_fixo(SEL("div.fixed button:has-text('Concluir coleta')"), (640, 770), js_clicar('div.fixed button', 'Concluir coleta'),
                  c.A(5, 'Concluir', 0.1), 'Concluir coleta')
    c.waitfor(text='Relatório de Coleta 8', timeout=15)
    c.hover(TXTX('Relatório de Coleta 8', exact=True), 1.0, at=c.A(5, 'relatório', 0.5), label='Relatório de Coleta 8')
    c.mark(6)
    c.cursor((760, 460), at=c.A(6, 'concluir', 0.3), label='cursor em repouso (a dica)')
    c.mark(7)
    c.click(BTNX('Voltar às ordens'), at=c.A(7, 'volta', 0.8), label='Voltar às ordens')
    c.waitfor(text=PAGINAS['/coletas/ordens'], timeout=15)
    c.hover(CARD_TXT(8, '#8'), 0.8, at=c.A(7, 'Concluídas', 0.5), label='#8 em Concluídas')
    c.click(CARD_TXT(8, 'Depósito Irmãos Siqueira'), at=c.A(7, 'cartão', 0.8), label='abre a ficha da ordem 8')
    c.waitfor(text='Detalhes da ordem de coleta.', timeout=10)
    c.mark(8)
    rola_ate(c, 'Equipamentos movimentados', c.A(8, 'Aqui', 0.3), 'ficha: Equipamentos movimentados', y=200, escopo=DLG)
    c.hover(TXTX('Equipamentos movimentados', within=DLG, exact=True), 1.0, at=c.A(8, 'caçambas', 0.5), label='Equipamentos movimentados')
    c.mark(9)
    rola_ate(c, 'Histórico', c.A(9, 'Histórico', 0.6), 'ficha: Histórico', y=200, escopo=DLG)
    c.hover(TXTX('Histórico', within=DLG, exact=True), 1.0, at=c.A(9, 'guarda', 0.5), label='Histórico')
    c.fim()
    return c


@capitulo
def cap07():
    """A coleta pedida pelo portal: o portal da Cooperativa Recomeço (aba Coletas, Solicitar coleta de PET prensado, 800 kg, 13/11, Tarde);
    de volta ao sistema, o ponto vermelho no menu, o cartão #10 "via portal", Aprovar e Agendar."""
    portal = f'/portal/{TOKEN_COOP}'
    c = Cap(7, start=(760, 420), setup=setup_em('/coletas/frota', extra=[{'do': 'goto', 'url': portal},
                                                                          {'do': 'waitFor', 'text': 'Portal do Cliente', 'timeout': 30},
                                                                          {'do': 'waitFor', 'idle': True, 'timeout': 25}, {'do': 'wait', 'seconds': 0.8}]))
    c.mark(1)
    c.cursor((760, 440), at=0.5, label='cursor em repouso (ilustração)')
    c.mark(2)
    c.flush(1e9)
    c.mark(3)
    c.hover(TXTX('Cooperativa Recomeço', exact=True), 0.8, at=c.A(3, 'Cooperativa', 0.5), label='portal: Cooperativa Recomeço')
    c.click(SEL("button:text-is('Coletas'), [role=tab]:text-is('Coletas')"), at=c.A(3, 'aba', 0.8), label='aba Coletas')
    c.hover(TXTX('Minhas coletas', exact=True), 0.6, at=c.A(3, 'acompanha', 0.5), label='Minhas coletas')
    c.hover(BTN('Solicitar coleta'), 0.6, at=c.A(3, 'pede', 0.5), label='Solicitar coleta')
    c.mark(4)
    c.click(BTN('Solicitar coleta'), at=c.A(4, 'cooperativa', 0.6), label='abre Solicitar coleta')
    c.waitfor(target=SEL('#coleta-material'), timeout=10)
    c.click(SEL('#coleta-material'), at=c.A(4, 'PET', 0.8), label='Material (campo)')
    c.type(SEL('#coleta-material'), 'PET prensado', at=c.A(4, 'PET', 0.05), label='Material: PET prensado', cps=40, noClick=True)
    c.click(SEL('#coleta-qtd'), at=c.A(4, 'quantidade', 0.8), label='Quantidade estimada (campo)')
    c.type(SEL('#coleta-qtd'), '800 kg', at=c.A(4, 'quantidade', 0.05), label='Quantidade estimada: 800 kg', cps=40, noClick=True)
    c.mark(5)
    c.click(SEL('#coleta-data'), at=c.A(5, 'dia', 0.8), label='Data preferida (campo)')
    c.type(SEL('#coleta-data'), '13112026', at=c.A(5, 'sexta', 0.3), label='Data preferida 13/11/2026', cps=40, noClick=True)
    c.click(SEL('#coleta-janela'), at=c.A(5, 'período', 0.8), label='abre Período')
    c.click(OPT('Tarde'), at=c.A(5, 'tarde', 0.6), label='Período: Tarde')
    c.hover(TXTX('Endereço da coleta', within=DLG, exact=True), 0.8, at=c.A(5, 'endereço', 0.5), label='Endereço da coleta (do cadastro)')
    c.mark(6)
    c.click(BTN('Solicitar coleta', within=DLG), at=c.A(6, 'Solicitar', 0.8), label='Solicitar coleta (enviar)')
    c.waitfor(text='Solicitação enviada (#10)', timeout=10)
    c.mark(7)
    c.add({'do': 'goto', 'url': '/coletas/frota', 'at': round(c.L(7) - 0.2, 2), 'label': 'de volta ao sistema (Frota)'})
    c.waitfor(text=PAGINAS['/coletas/frota'], timeout=15)
    c.hover(GRUPO, 1.0, at=c.A(7, 'menu', 0.5), label='o ponto vermelho no menu Coletas & Logística')
    c.click(ITEM_MENU('Ordens de Coleta'), at=c.A(7, 'coluna', 0.8), label='Ordens de Coleta')
    c.waitfor(text=PAGINAS['/coletas/ordens'], timeout=15)
    c.hover(CARD_TXT(10, '#10'), 0.4, at=c.A(7, 'pedido', 0.5), label='#10 na Solicitada')
    c.hover(CARD_TXT(10, 'via portal'), 0.8, at=c.A(7, 'via', 0.5), label='#10: via portal')
    c.mark(8)
    c.hover(CARD_BTN(10, 'Aprovar'), 0.4, at=c.A(8, 'aprovar', 0.5), label='Aprovar')
    c.hover(CARD_BTN(10, 'Recusar'), 1.0, at=c.A(8, 'recusar', 0.5), label='Recusar')
    c.mark(9)
    c.click(CARD_BTN(10, 'Aprovar'), at=c.A(9, 'Aprovar', 0.8), label='Aprovar #10')
    c.waitfor(text='Agendar coleta', timeout=10)
    c.hover(TXTX('Data da coleta *', within=DLG, exact=True), 0.3, at=c.A(9, 'data', 0.5), label='Agendar coleta: data do pedido')
    c.hover(TXTX('Janela *', within=DLG, exact=True), 0.6, at=c.A(9, 'janela', 0.5), label='Agendar coleta: janela do pedido')
    c.mark(10)
    c.click(BTN('Agendar', within=DLG), at=c.A(10, 'Agendar', 0.8), label='Agendar')
    c.waitfor(text='Status alterado para Agendada', timeout=10)
    c.hover(CARD_TXT(10, '#10'), 1.2, at=c.A(10, 'cooperativa', 0.5), label='#10 em Agendada')
    c.fim()
    return c


@capitulo
def cap08():
    """Veículos e motoristas: Frota, o FKD2E41 (tara e capacidade), Novo veículo FVL8A52 (poliguindaste) e Novo motorista Sérgio Paiva."""
    c = Cap(8, start=(760, 420), setup=setup_em('/coletas/ordens', aquece=['/coletas/frota']))
    c.mark(1)
    c.click(ITEM_MENU('Frota'), at=c.A(1, 'Frota', 0.8), label='menu Frota')
    c.waitfor(text=PAGINAS['/coletas/frota'], timeout=15)
    c.hover(TAB('Veículos'), 0.3, at=c.A(1, 'veículos', 0.5), label='aba Veículos')
    c.hover(TAB('Motoristas'), 0.3, at=c.A(1, 'motoristas', 0.5), label='aba Motoristas')
    c.hover(TXTX('Mesma frota usada na pesagem de compra/venda.', exact=True), 0.8, at=c.A(1, 'pesagem', 0.5), label='mesma frota da pesagem')
    c.mark(2)
    c.click(TXTX('FKD2E41', within='main', exact=True), at=c.A(2, 'caminhão', 0.8), label='FKD2E41')
    c.hover(TXTX('Tara', within='main', exact=True), 0.3, at=c.A(2, 'tara', 0.5), label='Tara do FKD2E41')
    c.hover(TXTX('Capacidade', within='main', exact=True), 1.0, at=c.A(2, 'capacidade', 0.5), label='Capacidade do FKD2E41')
    c.mark(3)
    c.flush(1e9)
    c.mark(4)
    c.click(BTN('Novo veículo'), at=c.A(4, 'Novo', 0.9), label='Novo veículo')
    c.waitfor(target=SEL('#veiculo-placa'), timeout=10)
    c.click(SEL('#veiculo-placa'), at=c.A(4, 'digito', 0.6), label='Placa (campo)')
    c.type(SEL('#veiculo-placa'), 'FVL8A52', at=c.A(4, 'placa', 0.05), label='Placa FVL8A52', cps=40, noClick=True)
    c.click(SEL('#veiculo-descricao'), at=c.A(4, 'apelido', 0.6), label='Descrição / Apelido (campo)')
    c.type(SEL('#veiculo-descricao'), 'Caminhão poliguindaste', label='Descrição: Caminhão poliguindaste', cps=40, noClick=True)
    c.mark(5)
    c.click(SEL('#veiculo-uf'), at=c.A(5, 'servem', 0.6), label='abre UF de licenciamento')
    c.click(OPT('SP'), at=c.A(5, 'São', 0.6), label='UF: SP')
    c.click(SEL('#veiculo-categoria'), at=c.A(5, 'Paulo', 0.3), label='abre Tipo')
    c.click(OPT('Veículo único (truck, toco, utilitário)'), at=c.A(5, 'único', 0.5), label='Tipo: Veículo único')
    c.click(SEL('#veiculo-rodado'), label='abre Tipo de rodado')
    c.click(OPT('Toco'), at=c.A(5, 'toco', 0.5), label='Tipo de rodado: Toco')
    c.mark(6)
    c.click(SEL('#veiculo-tara'), at=c.A(6, 'tara', 0.6), label='Tara (campo)')
    c.type(SEL('#veiculo-tara'), '7100', at=c.A(6, 'sete', 0.05), label='Tara (kg) 7100', cps=40, noClick=True)
    c.click(SEL('#veiculo-cap-kg'), at=c.A(6, 'capacidade', 0.6), label='Capacidade (campo)')
    c.type(SEL('#veiculo-cap-kg'), '8500', at=c.A(6, 'oito', 0.05), label='Capacidade (kg) 8500', cps=40, noClick=True)
    c.mark(7)
    c.click(BTN('Cadastrar', within=DLG), at=c.A(7, 'Cadastrar', 0.8), label='Cadastrar veículo')
    c.waitfor(text='Veículo cadastrado', timeout=10)
    c.hover(TXTX('FVL8A52', within='main', exact=True), 1.0, at=c.A(7, 'poliguindaste', 0.5), label='FVL8A52 na frota')
    c.mark(8)
    c.click(TAB('Motoristas'), at=c.A(8, 'aba', 0.8), label='aba Motoristas')
    c.click(BTN('Novo motorista'), at=c.A(8, 'Novo', 0.8), label='Novo motorista')
    c.waitfor(target=SEL('#motorista-nome'), timeout=10)
    c.mark(9)
    c.click(SEL('#motorista-nome'), at=c.A(9, 'Sérgio', 0.7), label='Nome (campo)')
    c.type(SEL('#motorista-nome'), 'Sérgio Paiva', at=c.A(9, 'Sérgio', 0.05), label='Nome: Sérgio Paiva', cps=40, noClick=True)
    c.click(SEL('#motorista-doc'), at=c.A(9, 'Nome', 0.6), label='CPF (campo)')
    c.type(SEL('#motorista-doc'), '46371820508', at=c.A(9, 'CPF', 0.05), label='CPF', cps=40, noClick=True)
    c.click(SEL('#motorista-tel'), label='Telefone (campo)')
    c.type(SEL('#motorista-tel'), '12900004417', label='Telefone', cps=40, noClick=True)
    c.mark(10)
    c.click(SEL('#motorista-cnh'), at=c.A(10, 'CNH', 0.8), label='CNH (campo)')
    c.type(SEL('#motorista-cnh'), '04581273671', at=c.A(10, 'número', 0.05), label='CNH', cps=40, noClick=True)
    c.click(SEL('#motorista-cnh-cat'), at=c.A(10, 'categoria', 0.8), label='abre Categoria')
    c.click(OPT('C'), at=c.A(10, 'C', 0.5, nth=3), label='Categoria C')
    c.click(SEL('#motorista-cnh-val'), at=c.A(10, 'validade', 0.8), label='Validade da CNH (campo)')
    c.type(SEL('#motorista-cnh-val'), '18062030', at=c.A(10, 'validade', 0.05), label='Validade da CNH 18/06/2030', cps=40, noClick=True)
    c.mark(11)
    c.click(BTN('Cadastrar', within=DLG), at=c.A(11, 'Cadastrar', 0.8), label='Cadastrar motorista')
    c.waitfor(text='Motorista cadastrado', timeout=10)
    c.hover(TXTX('Sérgio Paiva', within='main', exact=True), 1.2, at=c.A(11, 'escalado', 0.5), label='Sérgio Paiva na lista')
    c.fim()
    return c


@capitulo
def cap09():
    """As caçambas e onde estão: Equipamentos, tipos, unidades, Nova unidade Caçamba 06, Movimentar (Externo -> Minha base), Onde tudo está
    agora e a aba Movimentações."""
    c = Cap(9, start=(760, 420), setup=setup_em('/coletas/ordens', aquece=['/coletas/equipamentos']))
    c.mark(1)
    c.click(ITEM_MENU('Equipamentos'), at=c.A(1, 'Equipamentos', 0.8), label='menu Equipamentos')
    c.waitfor(text=PAGINAS['/coletas/equipamentos'], timeout=15)
    c.hover(TXTX(PAGINAS['/coletas/equipamentos'], exact=True), 0.8, at=c.A(1, 'bags', 0.5), label='caçambas, bags, caixas e paletes')
    c.mark(2)
    c.hover(TXTX('Tipos de equipamento', within='main', exact=True), 0.4, at=c.A(2, 'tipo', 0.5), label='Tipos de equipamento')
    c.hover(SEL("main tr:has-text('Caçamba 5 m³')"), 1.6, at=c.A(2, 'caçamba', 0.5), label='Caçamba 5 m³: uma a uma')
    c.hover(SEL("main tr:has-text('Bag 1 m³')"), 1.6, at=c.A(2, 'bag', 0.5), label='Bag 1 m³: por quantidade')
    c.mark(3)
    rola_ate(c, 'Unidades identificáveis', c.A(3, 'Embaixo', 0.3), 'desce às Unidades identificáveis', y=140)
    c.hover(TXTX('Caçamba 05', within='main', exact=True), 0.6, at=c.A(3, 'Caçamba', 0.5), label='Caçamba 05')
    c.hover(SEL("main :text-is('Caçamba 05') >> xpath=ancestor::*[contains(., 'Depósito Irmãos Siqueira')][1]"), 1.2, at=c.A(3, 'Depósito', 0.5),
            label='Caçamba 05 no Depósito Irmãos Siqueira')
    c.mark(4)
    c.click(BTN('Nova unidade'), at=c.A(4, 'Nova', 0.9), label='Nova unidade')
    c.waitfor(target=SEL('#equipamento-id'), timeout=10)
    c.click(SEL('#equipamento-id'), at=c.A(4, 'identificação', 0.6), label='Identificação (campo)')
    c.type(SEL('#equipamento-id'), 'Caçamba 06', at=c.A(4, 'Caçamba', 0.05, nth=1), label='Identificação: Caçamba 06', cps=40, noClick=True)
    c.click(SEL('#equipamento-tipo'), at=c.A(4, 'tipo', 0.9), label='abre Tipo de equipamento')
    c.click(OPT('Caçamba 5 m³'), label='Tipo: Caçamba 5 m³')
    c.click(BTN('Cadastrar', within=DLG), at=c.A(4, 'Cadastrar', 0.5), label='Cadastrar unidade')
    c.waitfor(text='Unidade cadastrada', timeout=10)
    c.mark(5)
    c.click(TXTX('Caçamba 06', within='main', exact=True), at=c.A(5, 'Ela', 0.8), label='Caçamba 06 na lista')
    c.hover(TXTX('Ainda sem movimentação registrada', within='main', exact=False), 1.2, at=c.A(5, 'lugar', 0.5), label='sem lugar (sem movimentação)')
    c.mark(6)
    c.click(BTN('Movimentar', within='main'), at=c.A(6, 'Movimentar', 0.8), label='Movimentar')
    c.waitfor(text='Nova movimentação', timeout=10)
    c.hover(BTNX('Externo', within=DLG), 0.8, at=c.A(6, 'Externo', 0.5), label='De: Externo')
    c.click(SEL(f"{DLG} button:has-text('Minha base') >> nth=1"), at=c.A(6, 'Minha', 0.8), label='Para: Minha base')
    c.click(BTN('Registrar', within=DLG), at=c.A(6, 'Registrar', 0.8), label='Registrar')
    c.waitfor(text='Movimentação registrada', timeout=10)
    c.hover(TXTX('Posição atual', within='main', exact=True), 1.2, at=c.A(6, 'base', 0.5, nth=1), label='Posição atual: Minha base')
    c.mark(7)
    c.cursor((760, 460), at=c.A(7, 'dica', 0.3), label='cursor em repouso (ilustração)')
    c.mark(8)
    rola_ate(c, 'Onde tudo está agora', c.A(8, 'Onde', 0.6), 'desce a Onde tudo está agora', y=120)
    c.hover(TXTX('Na base', within='main', exact=True), 0.6, at=c.A(8, 'base', 0.5), label='Na base')
    c.hover(TXTX('Em campo', within='main', exact=True), 0.4, at=c.A(8, 'campo', 0.5), label='Em campo')
    c.hover(TXTX('Com parceiros', within='main', exact=True), 0.8, at=c.A(8, 'parceiros', 0.6), label='Com parceiros')
    c.mark(9)
    c.click(TAB('Movimentações'), at=c.A(9, 'Movimentações', 0.8), label='aba Movimentações')
    c.hover(TXTX('Ordem 8', within='main', exact=False), 1.2, at=c.A(9, 'ordem', 0.5), label='as da troca de hoje: Ordem 8')
    c.fim()
    return c


@capitulo
def cap10():
    """O relatório: Este mês (4 coletas, 1 concluída, 25%), Mês passado (6, 5, 1, 100%), por status, motorista, veículo e parceiro."""
    c = Cap(10, start=(760, 420), setup=setup_em('/coletas/ordens', aquece=['/coletas/relatorio']))
    c.mark(1)
    c.click(ITEM_MENU('Relatório'), at=c.A(1, 'relatório', 0.8), label='menu Relatório')
    c.waitfor(text=PAGINAS['/coletas/relatorio'], timeout=15)
    c.hover(TXTX('Total de coletas', within='main', exact=True), 0.4, at=c.A(1, 'total', 0.5), label='Este mês: Total de coletas')
    c.hover(TXTX('Concluídas', within='main', exact=True), 0.4, at=c.A(1, 'concluídas', 0.5), label='Este mês: Concluídas')
    c.hover(TXTX('Canceladas', within='main', exact=True), 0.4, at=c.A(1, 'canceladas', 0.5), label='Este mês: Canceladas')
    c.hover(TXTX('Taxa de conclusão', within='main', exact=True), 0.6, at=c.A(1, 'taxa', 0.5), label='Este mês: Taxa de conclusão')
    c.mark(2)
    c.click(SEL("main button[role=combobox]"), at=c.A(2, 'Em', 0.6), label='abre Período')
    c.click(OPT('Mês passado'), at=c.A(2, 'outubro', 0.6), label='Período: Mês passado')
    c.hover(TXTX('Total de coletas', within='main', exact=True), 0.4, at=c.A(2, 'seis', 0.5), label='outubro: Total de coletas')
    c.hover(TXTX('Concluídas', within='main', exact=True), 0.4, at=c.A(2, 'cinco', 0.5), label='outubro: Concluídas')
    c.hover(TXTX('Canceladas', within='main', exact=True), 0.4, at=c.A(2, 'uma', 0.5), label='outubro: Canceladas')
    c.hover(TXTX('Taxa de conclusão', within='main', exact=True), 1.0, at=c.A(2, 'taxa', 0.5), label='outubro: Taxa de conclusão')
    c.mark(3)
    c.cursor((760, 460), at=c.A(3, 'dica', 0.3), label='cursor em repouso (ilustração)')
    c.mark(4)
    rola_ate(c, 'Por status', c.A(4, 'Embaixo', 0.3), 'desce às tabelas', y=130)
    c.hover(TXTX('Por status', within='main', exact=True), 0.3, at=c.A(4, 'status', 0.5), label='Por status')
    c.hover(TXTX('Por motorista', within='main', exact=True), 0.3, at=c.A(4, 'motorista', 0.5), label='Por motorista')
    c.hover(TXTX('Por veículo', within='main', exact=True), 0.3, at=c.A(4, 'veículo', 0.5), label='Por veículo')
    c.hover(TXTX('Por parceiro', within='main', exact=True), 1.2, at=c.A(4, 'parceiro', 0.5), label='Por parceiro')
    c.mark(5)
    rola_ate(c, 'Período', c.A(5, 'Uma', 0.3), 'sobe ao Período', y=160)
    c.hover(SEL("main button[role=combobox]"), 1.5, at=c.A(5, 'cada', 0.5), label='Período (em que mês cada coleta entra)')
    c.fim()
    return c


@capitulo
def cap11():
    """As regras: Configurações, Prefixo da numeração "COL-", Janelas, Exigir motorista e veículo, Exigir aprovação, Antecedência mínima 24
    e Dias aceitos."""
    c = Cap(11, start=(760, 420), setup=setup_em('/coletas/ordens', aquece=['/coletas/configuracoes']))
    c.mark(1)
    c.click(ITEM_MENU('Configurações'), at=c.A(1, 'Configurações', 0.8), label='menu Configurações (Coletas)')
    c.waitfor(text=PAGINAS['/coletas/configuracoes'], timeout=15)
    c.hover(TXTX('Operação', within='main', exact=True), 0.6, at=c.A(1, 'operação', 0.5), label='bloco Operação')
    c.mark(2)
    c.hover(SEL('#col-prefix'), 0.6, at=c.A(2, 'Prefixo', 0.5), label='Prefixo da numeração')
    c.click(SEL('#col-prefix'), at=c.A(2, 'coloco', 0.6), label='Prefixo (campo)')
    c.type(SEL('#col-prefix'), 'COL-', at=c.A(2, 'prefixo', 0.05, nth=1), label='Prefixo: COL-', cps=40, noClick=True)
    c.press('Tab', at=c.A(2, 'ordens', 0.2), label='sai do campo (salva o prefixo)')
    c.waitfor(text='Prefixo da numeração salvo', timeout=8)
    c.mark(3)
    c.hover(TXTX('Janelas de coleta oferecidas', within='main', exact=True), 0.5, at=c.A(3, 'Janelas', 0.5), label='Janelas de coleta oferecidas')
    c.hover(SEL("main button:text-is('Dia todo')"), 0.8, at=c.A(3, 'períodos', 0.5), label='as janelas: Manhã, Tarde e Dia todo')
    c.hover(TXTX('Exigir motorista e veículo para agendar', within='main', exact=True), 1.2, at=c.A(3, 'exigir', 0.5),
            label='Exigir motorista e veículo para agendar')
    c.mark(4)
    rola_ate(c, 'Portal e solicitações', c.A(4, 'bloco', 0.6), 'desce ao bloco Portal e solicitações', y=120)
    c.hover(TXTX('Exigir aprovação da solicitação', within='main', exact=True), 1.5, at=c.A(4, 'Exigir', 0.5), label='Exigir aprovação da solicitação')
    c.mark(5)
    c.hover(SEL('#col-lead'), 0.6, at=c.A(5, 'Antecedência', 0.5), label='Antecedência mínima (horas)')
    c.click(SEL('#col-lead'), at=c.A(5, 'coloco', 0.6), label='Antecedência (campo)')
    c.type(SEL('#col-lead'), '24', at=c.A(5, 'vinte', 0.05), label='Antecedência: 24', cps=40, noClick=True, clear=True)
    c.press('Tab', at=c.A(5, 'Dias', 0.6), label='sai do campo (salva a antecedência)')
    c.hover(TXTX('Dias aceitos para coleta', within='main', exact=True), 0.4, at=c.A(5, 'aceitos', 0.5), label='Dias aceitos para coleta')
    c.hover(SEL("main button:text-is('Seg')"), 0.3, at=c.A(5, 'segunda', 0.5), label='Seg')
    c.hover(SEL("main button:text-is('Sáb')"), 0.6, at=c.A(5, 'sábado', 0.5), label='Sáb')
    c.mark(6)
    c.cursor((760, 460), at=c.A(6, 'dica', 0.3), label='cursor em repouso (ilustração)')
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
