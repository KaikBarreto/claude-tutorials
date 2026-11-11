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



def stable_id(chave):
    """o mesmo UUID estável do Supabase falso (core/util.mjs stableId)"""
    h = bytearray(hashlib.sha1(('domiflix-fake:' + chave).encode()).digest())
    h[6] = (h[6] & 0x0F) | 0x50
    h[8] = (h[8] & 0x3F) | 0x80
    x = h[:16].hex()
    return f'{x[:8]}-{x[8:12]}-{x[12:16]}-{x[16:20]}-{x[20:32]}'


RAFAEL = stable_id('user.rafael')
TOKEN_COOP = stable_id('t12.portal.recomeco')   # portal_token da Cooperativa Recomeço (t12_sementes.py)
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

# Animação do framer-motion (opacity 0 inline) que o relógio simulado do Playwright deixa começar no futuro (currentTime < 0): a tela
# ficaria em branco por segundos (portal, cartões que entram). Efeito do ambiente, não do app (08-licoes, T5 cap. 10): a cada 100 ms,
# a animação presa começa agora.
ANIM_FIX = ("(()=>{if(window.__animFix)return 'ja';window.__animFix=setInterval(()=>{for(const a of document.getAnimations())"
            "if(a.currentTime!==null&&a.currentTime<0)a.startTime=document.timeline.currentTime},100);return 'anim fix'})()")

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
        """passeio: leva o cursor a um ponto fixo da tela (posições medidas na exploração, rec/t12/_ex); ~0,6 s contra ~1,5 s de um hover"""
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
CARTAO = lambda num: f"main div.cursor-pointer.rounded-2xl:has(span.font-semibold:text-is('#{num}'))"     # cartão #N do quadro
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


# Folga das âncoras (o custo do gesto até o cursor CHEGAR, docs/04): FC no clique, FH no hover. Medidas no ensaio rápido sem render ao
# lado (depois das 17:35 de 11/11); com a máquina carregada os gestos ficam 1,5 a 2x mais lentos (aviso do coordenador).
FC, FH = 1.3, 1.4

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
    c.click(GRUPO, at=c.A(5, 'Coletas', 0.9), label='abre Coletas & Logística')
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
    """O quadro: colunas, cartões #8 e #7, filtros, Quadro/Lista e Nova ordem; a dica das concluídas e canceladas.
    Passeio com o cursor por pontos fixos (posições do quadro a 1280x800, rec/t12/_ex/e2): a fala cita um item por segundo."""
    c = Cap(2, start=(760, 470), setup=setup_em('/coletas/ordens'))
    c.mark(1)
    c.aponta((370, 256), c.A(1, 'Solicitada', 0.35), 'coluna Solicitada')
    c.aponta((562, 254), c.A(1, 'Agendada', 0.35), 'coluna Agendada')
    c.aponta((754, 254), c.A(1, 'caminho', 0.45), 'coluna A caminho')
    c.aponta((936, 254), c.A(1, 'Concluídas', 0.35), 'coluna Concluídas')
    c.aponta((1138, 254), c.A(1, 'canceladas', 0.35), 'coluna Cancelada')
    c.confere_kpi([['Solicitada', '0'], ['Agendada', '1'], ['A caminho', '1'], ['Concluídas', '5'], ['Cancelada', '1']], 'contagem das colunas',
                  rotulos='main h3')
    c.mark(2)
    c.hover(TXT('Nenhuma ordem', within='main'), 1.5, at=c.L(2) - 0.2, label='Solicitada vazia (Nenhuma ordem)')
    c.mark(3)
    c.aponta((522, 318), c.A(3, 'número', 0.35), 'cartão #8: número')
    c.aponta((585, 350), c.A(3, 'parceiro', 0.35), 'cartão #8: parceiro')
    c.aponta((592, 318), c.A(3, 'período', 0.35), 'cartão #8: período')
    c.aponta((566, 405), c.A(3, 'motorista', 0.35), 'cartão #8: motorista')
    c.aponta((556, 423), c.A(3, 'placa', 0.35), 'cartão #8: placa')
    c.hover(CARD(8), 1.6, at=c.A(3, 'troca', FH), label='cartão #8: a troca de caçamba do Depósito Irmãos Siqueira')
    c.mark(4)
    c.aponta((757, 405), c.A(4, 'Tiago', 0.35), 'cartão #7: Tiago Freitas')
    c.aponta((720, 350), c.A(4, 'Marcelo', 0.35), 'cartão #7: Marcelo Tavares')
    c.aponta((791, 350), c.A(4, 'cadastro', 0.6), 'cartão #7: Sem cadastro')
    c.mark(5)
    c.hover(BTNX('Filtros', within='main'), 0.5, at=c.A(5, 'filtros', FC), label='Filtros')
    c.aponta((1070, 196), c.A(5, 'troca', 0.35), 'Quadro / Lista')
    c.hover(NOVA_ORDEM, 0.8, at=c.A(5, 'Nova', FC), label='Nova ordem')
    c.mark(6)
    c.aponta((760, 470), c.A(6, 'anda', 0.35), 'cursor em repouso (a dica)')
    c.aponta((936, 254), c.A(6, 'Concluída', 0.35), 'dica: coluna Concluídas')
    c.aponta((1138, 254), c.A(6, 'cancelada', 0.35), 'dica: coluna Cancelada')
    c.aponta((760, 470), c.A(6, 'registro', 0.35), 'cursor em repouso')
    c.fim()
    return c


@capitulo
def cap03():
    """Criar uma ordem: Nova ordem, as etapas, Cadastrado/Sem cadastro, Tipo, Parceiro (Auto Peças Vale Forte), endereço do cadastro,
    Avançar, Material estimado e Observações."""
    c = Cap(3, start=(900, 300), setup=setup_em('/coletas/ordens'))
    c.mark(1)
    c.click(NOVA_ORDEM, at=c.A(1, 'Nova', FC), label='Nova ordem')
    c.waitfor(text='Nova ordem de coleta', timeout=10)
    c.aponta((455, 197), c.A(1, 'Parceiro', 0.35), 'etapa Parceiro')
    c.aponta((606, 197), c.A(1, 'Coleta', 0.35), 'etapa Coleta')
    c.aponta((760, 197), c.A(1, 'Frota', 0.35), 'etapa Frota')
    c.mark(2)
    c.hover(TXTX('Cadastrado', within=DLG, exact=True), 0.8, at=c.A(2, 'Cadastrado', FH), label='Cadastrado')
    c.hover(TXTX('Sem cadastro', within=DLG, exact=True), 1.2, at=c.A(2, 'Sem', FH), label='Sem cadastro')
    c.mark(3)
    c.hover(SEL('#ordem-tipo'), 0.8, at=c.L(3) - 0.2, label='Tipo: Fornecedor')
    c.click(SEL(f"{DLG} button:has-text('Selecionar')"), at=c.A(3, 'Parceiro', FC), label='Parceiro: Selecionar…')
    c.waitfor(target=BUSCA_PARC, timeout=10)
    c.type(BUSCA_PARC, 'Vale Forte', label='busca Vale Forte', cps=40, noClick=True)
    c.click(BTNX('Auto Peças Vale Forte', within=f'{DLG} >> nth=-1'), at=c.A(3, 'Vale', FC), label='escolhe Auto Peças Vale Forte')
    c.mark(4)
    c.hover(PH('Rua, Avenida, etc.'), 1.0, at=c.A(4, 'endereço', FH), label='endereço do cadastro')
    c.hover(SEL(f"{DLG} button[role=combobox] >> nth=2"), 0.8, at=c.A(4, 'mudar', FH), label='endereço do cadastro (cidade)')
    c.mark(5)
    c.click(AVANCAR, at=c.A(5, 'Avançar', FC), label='Avançar')
    c.click(SEL('#ordem-material'), at=c.A(5, 'Material', FC), label='Material estimado (campo)')
    c.type(SEL('#ordem-material'), '~400 kg de radiadores e baterias', at=c.A(5, 'uns', 0.05), label='Material estimado', cps=40, noClick=True)
    c.mark(6)
    c.click(SEL('#ordem-obs'), at=c.A(6, 'Observações', FC), label='Observações (campo)')
    c.type(SEL('#ordem-obs'), 'Retirar pelo portão lateral', at=c.A(6, 'retirar', 0.05), label='Observações', cps=40, noClick=True)
    c.fim()
    return c


@capitulo
def cap04():
    """Data e janela: Data agendada 11/11/2026, Período (Manhã, Tarde, Dia todo) -> Manhã, Avançar."""
    c = Cap(4, start=(900, 300), setup=setup_em('/coletas/ordens', extra=setup_nova_ordem(2)))
    c.mark(1)
    c.aponta((521, 355), c.A(1, 'Data', 0.35), 'Data agendada')
    c.aponta((758, 355), c.A(1, 'Período', 0.35, nth=1), 'Período')
    c.mark(2)
    c.click(SEL('#ordem-data'), at=c.A(2, 'amanhã', FC), label='Data agendada (campo)')
    c.type(SEL('#ordem-data'), '11112026', at=c.A(2, 'onze', 0.3), label='Data agendada 11/11/2026', cps=40, noClick=True)
    c.mark(3)
    c.click(SEL('#ordem-janela'), at=c.L(3) - 0.2, label='abre Período')
    c.hover(OPT('Tarde'), 2.2, at=c.A(3, 'tarde', FH), label='as janelas: Manhã, Tarde e Dia todo')
    c.mark(4)
    c.click(OPT('Manhã'), at=c.L(4) - 0.2, label='escolhe Manhã')
    c.hover(SEL('#ordem-janela'), 1.5, at=c.A(4, 'Configurações', FH), label='Período: Manhã (as janelas vêm das Configurações)')
    c.mark(5)
    c.click(AVANCAR, at=c.L(5) - 0.2, label='Avançar para a Frota')
    c.waitfor(target=MOTORISTA, timeout=10)
    c.fim()
    return c


@capitulo
def cap05():
    """Motorista e veículo: Jair Lopes e GHT7B19, a Revisão, Criar ordem e o cartão #9 em Agendada."""
    c = Cap(5, start=(900, 300), setup=setup_em('/coletas/ordens', extra=setup_nova_ordem(3)))
    c.mark(1)
    c.hover(MOTORISTA, 0.3, at=c.A(1, 'Motorista', FH), label='Motorista')
    c.hover(VEICULO, 0.6, at=c.A(1, 'Veículo', 0.8), label='Veículo')
    c.mark(2)
    c.click(MOTORISTA, at=c.L(2) - 0.2, label='Motorista (campo)')
    c.type(MOTORISTA, 'Jair', label='digita Jair', cps=40, noClick=True)
    c.click(OPT('Jair Lopes'), label='escolhe Jair Lopes')
    c.click(VEICULO, label='Veículo (campo)')
    c.type(VEICULO, 'GHT', label='digita GHT', cps=40, noClick=True)
    c.click(OPT('GHT7B19'), label='escolhe GHT7B19')
    c.mark(3)
    c.hover(SEL(f"{DLG} div.rounded-md:has(> :text-is('Revisão'))"), 6.0, at=c.A(3, 'Revisão', FH), label='Revisão: parceiro, cidade, material, data e período')
    c.mark(4)
    c.click(BTN('Criar ordem'), at=c.L(4) - 0.2, label='Criar ordem')
    c.waitfor(text='Ordem de coleta criada', timeout=10)
    c.confere_item('main div.cursor-pointer.rounded-2xl', '#9', ['Auto Peças Vale Forte', 'Manhã', 'Jair Lopes', 'GHT7B19'], 'cartão #9 (fala: ordem nove, Jair, três quartos)')
    c.hover(CARD(9), 2.5, label='cartão #9 em Agendada (Jair e o GHT7B19)')
    c.mark(5)
    c.hover(CARD_TXT(9, 'Jair Lopes'), 2.0, at=c.L(5) - 0.2, label='cartão #9: motorista e veículo')
    c.fim()
    return c


def escolhe_teclado(c, trigger, letras, at=None, label=None, idx=0):
    """seletor Radix sem cursor (passo sem graça para a fala): foco por eval (o `idx`-ésimo `trigger`), Enter abre, a letra procura a opção,
    Enter escolhe (~0,5 s)"""
    c.ev(f"(()=>{{const t=[...document.querySelectorAll({json.dumps(trigger)})][{int(idx)}];if(!t)return 'SEM ALVO';t.focus();return 'foco'}})()", at=at,
         label=(label or trigger) + ' (foco)')
    c.press('Enter', label=(label or trigger) + ' (abre)')
    c.waitfor(selector='[role=listbox]', timeout=5)
    c.type(SEL('[role=listbox]'), letras, label=(label or trigger) + ' (procura)', cps=40, noClick=True)
    return c.press('Enter', label=label or trigger)


@capitulo
def cap06():
    """Acompanhar até concluir: #8 A caminho, Preencher, Recolhi Caçamba 03, Entreguei Caçamba 05, Concluir coleta, o relatório, Voltar às
    ordens e a ficha (Equipamentos movimentados e Histórico)."""
    c = Cap(6, start=(760, 420), setup=setup_em('/coletas/ordens', extra=[{'do': 'eval', 'js': GPS_FICTICIO}]))
    c.mark(1)
    c.click(CARD_BTN(8, 'A caminho'), at=c.A(1, 'A', FC, nth=1), label='#8: A caminho')
    c.waitfor(text='Status alterado para A caminho', timeout=10)
    c.hover(CARD_TXT(8, '#8'), 1.0, at=c.A(1, 'anda', 1.2), label='#8 na coluna A caminho')
    c.mark(2)
    c.click(CARD_BTN(8, 'Preencher'), at=c.A(2, 'Preencher', FC), label='#8: Preencher')
    c.waitfor(text='Ordem #8', timeout=15)
    c.hover(TXTX('Agendamento', exact=True), 1.0, at=c.A(2, 'combinado', FH), label='tela da ordem: o combinado')
    c.mark(3)
    c.hover(TXTX('Equipamentos', exact=True), 0.3, at=c.L(3) - 0.2, label='bloco Equipamentos (Entreguei e Recolhi)')
    escolhe_teclado(c, 'button[role=combobox]', 'C', label='Recolhi: Caçamba 5 m³', idx=1)   # 2º seletor = Tipo do Recolhi
    c.click(SEL('button[role=combobox] >> nth=2'), at=c.A(3, 'Edson', FC), label='Recolhi: Unidade')
    c.click(OPT('Caçamba 03'), at=c.A(3, 'Caçamba', FC, nth=1), label='Recolhi: Caçamba 03')
    c.click(SEL("button:has-text('Adicionar') >> nth=1"), label='Recolhi: Adicionar')
    c.mark(4)
    escolhe_teclado(c, 'button[role=combobox]', 'C', label='Entreguei: Caçamba 5 m³', idx=0)   # 1º = Tipo do Entreguei
    c.click(SEL('button[role=combobox] >> nth=1'), at=c.L(4) - 0.2, label='Entreguei: Unidade (só as da base)')
    c.click(OPT('Caçamba 05'), at=c.A(4, 'base', FC), label='Entreguei: Caçamba 05')
    c.ev(js_clicar('button', 'Adicionar'), label='Entreguei: Adicionar (sem cursor)')
    c.mark(5)
    c.clicar_fixo(SEL("div.fixed button:has-text('Concluir coleta')"), (640, 766), js_clicar('div.fixed button', 'Concluir coleta'),
                  c.A(5, 'Concluir', 0.1), 'Concluir coleta')
    c.waitfor(text='Relatório de Coleta 8', timeout=15)
    c.hover(TXTX('Relatório de Coleta 8', exact=True), 1.5, at=c.A(5, 'relatório', FH), label='Relatório de Coleta 8')
    c.mark(6)
    c.cursor((760, 460), at=c.A(6, 'concluir', 0.3), label='cursor em repouso (a dica)')
    c.mark(7)
    c.click(BTNX('Voltar às ordens'), at=c.A(7, 'volta', FC), label='Voltar às ordens')
    c.waitfor(text=PAGINAS['/coletas/ordens'], timeout=15)
    c.hover(CARD_TXT(8, '#8'), 0.8, at=c.A(7, 'oito', FH), label='#8 em Concluídas')
    c.click(CARD_TXT(8, 'Depósito Irmãos Siqueira'), at=c.A(7, 'cartão', FC), label='abre a ficha da ordem 8')
    c.waitfor(text='Detalhes da ordem de coleta.', timeout=10)
    c.mark(8)
    c.hover(TXTX('Equipamentos movimentados', within=DLG, exact=True), 1.5, at=c.A(8, 'caçambas', FH), label='Equipamentos movimentados')
    c.confere('dlg', ['Recolhido', 'Caçamba 03', 'Entregue', 'Caçamba 05', 'A caminho → Concluída'], 'ficha da ordem 8 (caçambas 03 e 05)')
    c.mark(9)
    rola_ate(c, 'Histórico', c.L(9) - 0.2, 'ficha: Histórico', y=300, dur_ms=800, escopo=DLG)
    c.hover(TXTX('Histórico', within=DLG, exact=True), 2.0, at=c.A(9, 'mudança', FH), label='Histórico (cada mudança de etapa)')
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
    c.hover(TXTX('Cooperativa Recomeço', exact=True), 0.6, at=c.L(3) - 0.2, label='portal: Cooperativa Recomeço')
    c.click(SEL('#tab-btn-coletas'), at=c.A(3, 'aba', FC), label='aba Coletas')
    c.hover(TXTX('Minhas coletas', exact=True), 0.4, at=c.A(3, 'acompanha', 1.0), label='Minhas coletas')
    c.hover(BTN('Solicitar coleta'), 0.8, at=c.A(3, 'pede', FH), label='Solicitar coleta')
    c.mark(4)
    c.click(BTN('Solicitar coleta'), at=c.L(4) - 0.2, label='abre Solicitar coleta')
    c.waitfor(target=SEL('#coleta-material'), timeout=10)
    c.click(SEL('#coleta-material'), at=c.A(4, 'PET', FC), label='Material (campo)')
    c.type(SEL('#coleta-material'), 'PET prensado', at=c.A(4, 'PET', 0.05), label='Material: PET prensado', cps=40, noClick=True)
    c.click(SEL('#coleta-qtd'), at=c.A(4, 'quantidade', FC), label='Quantidade estimada (campo)')
    c.type(SEL('#coleta-qtd'), '800 kg', at=c.A(4, 'quantidade', 0.05), label='Quantidade estimada: 800 kg', cps=40, noClick=True)
    c.mark(5)
    c.click(SEL('#coleta-data'), at=c.L(5) - 0.2, label='Data preferida (campo)')
    c.type(SEL('#coleta-data'), '13112026', at=c.A(5, 'sexta', 0.3), label='Data preferida 13/11/2026', cps=40, noClick=True)
    c.click(SEL('#coleta-janela'), label='abre Período')
    c.type(SEL('[role=listbox]'), 'T', label='Período: procura Tarde', cps=40, noClick=True)
    c.press('Enter', label='Período: Tarde')
    rola_ate(c, 'Endereço da coleta', c.A(5, 'endereço', 0.4), 'desce ao Endereço da coleta (do cadastro)', y=150, dur_ms=700, escopo=DLG)
    c.registra(SEL(f"{DLG} input[placeholder='Rua, Avenida, etc.']"), label='Endereço da coleta: Rua do Trabalho, 57 (do cadastro)')
    c.mark(6)
    c.click(BTN('Solicitar coleta', within=DLG), at=c.A(6, 'Solicitar', FC), label='Solicitar coleta (enviar)')
    c.waitfor(text='Solicitação enviada (#10)', timeout=10)
    c.mark(7)
    c.add({'do': 'goto', 'url': '/coletas/frota', 'at': round(c.L(7) - 0.2, 2), 'label': 'de volta ao sistema (Frota)'})
    c.waitfor(text=PAGINAS['/coletas/frota'], timeout=15)
    c.hover(GRUPO, 1.4, at=c.A(7, 'menu', FH), label='o ponto vermelho no menu Coletas & Logística')
    c.click(GRUPO, label='abre Coletas & Logística')
    c.click(ITEM_MENU('Ordens de Coleta'), at=c.A(7, 'coluna', FC), label='Ordens de Coleta')
    c.waitfor(text=PAGINAS['/coletas/ordens'], timeout=15)
    c.hover(CARD(10), 1.0, at=c.A(7, 'pedido', FH), label='#10 na Solicitada')
    c.hover(CARD_TXT(10, 'via portal'), 0.8, at=c.A(7, 'via', FH), label='#10: via portal')
    c.mark(8)
    c.hover(CARD_BTN(10, 'Aprovar'), 0.3, at=c.A(8, 'aprovar', FH), label='Aprovar')
    c.hover(CARD_BTN(10, 'Recusar'), 1.5, label='Recusar')
    c.mark(9)
    c.click(CARD_BTN(10, 'Aprovar'), at=c.A(9, 'Aprovar', FC), label='Aprovar #10')
    c.waitfor(text='Agendar coleta', timeout=10)
    c.hover(TXTX('Data da coleta *', within=DLG, exact=True), 2.0, label='Agendar coleta: a data e a janela do pedido')
    c.mark(10)
    c.click(BTN('Agendar', within=DLG), at=c.A(10, 'Agendar', FC), label='Agendar')
    c.waitfor(text='Status alterado para Agendada', timeout=10)
    c.hover(CARD(10), 1.5, at=c.A(10, 'marcada', FH), label='#10 em Agendada')
    c.fim()
    return c


ABRE_GRUPO = [{'do': 'click', 'target': GRUPO}, {'do': 'waitFor', 'target': ITEM_MENU('Frota'), 'timeout': 8}, {'do': 'wait', 'seconds': 0.5}]


@capitulo
def cap08():
    """Veículos e motoristas: Frota, o FKD2E41 (tara e capacidade), Novo veículo FVL8A52 (poliguindaste) e Novo motorista Sérgio Paiva."""
    c = Cap(8, start=(760, 420), setup=setup_em('/coletas/ordens', aquece=['/coletas/frota'], extra=ABRE_GRUPO))
    c.mark(1)
    c.click(ITEM_MENU('Frota'), at=c.A(1, 'Frota', FC, nth=1), label='menu Frota')
    c.waitfor(text=PAGINAS['/coletas/frota'], timeout=15)
    c.aponta((340, 198), c.A(1, 'veículos', 0.35), 'aba Veículos')
    c.aponta((460, 198), c.A(1, 'motoristas', 0.35), 'aba Motoristas')
    c.hover(TXTX('Mesma frota usada na pesagem de compra/venda.', exact=True), 0.8, at=c.A(1, 'pesagem', FH), label='mesma frota da pesagem')
    c.mark(2)
    c.click(SEL("main button:has-text('FKD2E41'):has-text('Caminhão truck')"), at=c.A(2, 'caminhão', FC), label='FKD2E41')
    c.confere('main', ['6.380', '14.000'], 'FKD2E41: tara 6.380 e capacidade 14.000 (ilustração)')
    c.hover(SEL("main div:has(> h3:text-is('Capacidade operacional')) + div.grid"), 2.0, at=c.A(2, 'tara', FH), label='Tara e Capacidade do FKD2E41')
    c.mark(3)
    c.flush(1e9)
    c.mark(4)
    c.click(BTN('Novo veículo'), at=c.A(4, 'Novo', FC), label='Novo veículo')
    c.waitfor(target=SEL('#veiculo-placa'), timeout=10)
    c.click(SEL('#veiculo-placa'), label='Placa (campo)')
    c.type(SEL('#veiculo-placa'), 'FVL8A52', at=c.A(4, 'placa', 0.05), label='Placa FVL8A52', cps=40, noClick=True)
    c.click(SEL('#veiculo-descricao'), label='Descrição / Apelido (campo)')
    c.type(SEL('#veiculo-descricao'), 'Caminhão poliguindaste', label='Descrição: Caminhão poliguindaste', cps=40, noClick=True)
    c.mark(5)
    c.click(SEL('#veiculo-uf'), at=c.A(5, 'São', FC), label='abre UF de licenciamento')
    c.type(SEL('[role=listbox]'), 'SP', label='UF: procura SP', cps=40, noClick=True)
    c.press('Enter', label='UF: SP')
    rola_ate(c, 'Tipo de rodado', None, 'desce a janela do veículo', y=420, dur_ms=500, escopo=DLG)
    escolhe_teclado(c, '#veiculo-categoria', 'V', at=c.A(5, 'único', 0.3), label='Tipo: Veículo único')
    escolhe_teclado(c, '#veiculo-rodado', 'To', at=c.A(5, 'toco', 0.3), label='Tipo de rodado: Toco')
    c.mark(6)
    c.click(SEL('#veiculo-tara'), at=c.A(6, 'sete', FC), label='Tara (campo)')
    c.type(SEL('#veiculo-tara'), '7100', at=c.A(6, 'sete', 0.05), label='Tara (kg) 7100', cps=40, noClick=True)
    c.click(SEL('#veiculo-cap-kg'), at=c.A(6, 'oito', FC), label='Capacidade (campo)')
    c.type(SEL('#veiculo-cap-kg'), '8500', at=c.A(6, 'oito', 0.05), label='Capacidade (kg) 8500', cps=40, noClick=True)
    c.mark(7)
    c.clicar_fixo(SEL(f"{DLG} button:has-text('Cadastrar')"), (821, 736), js_clicar(f'{DLG} button', 'Cadastrar'), c.A(7, 'Cadastrar', 0.1),
                  'Cadastrar veículo')
    c.waitfor(text='Veículo cadastrado', timeout=10)
    c.hover(SEL("main button:has-text('FVL8A52')"), 1.0, at=c.A(7, 'poliguindaste', FH), label='FVL8A52 na frota')
    c.mark(8)
    c.click(TAB('Motoristas'), at=c.A(8, 'aba', FC), label='aba Motoristas')
    c.click(BTN('Novo motorista'), at=c.A(8, 'Novo', FC), label='Novo motorista')
    c.waitfor(target=SEL('#motorista-nome'), timeout=10)
    c.mark(9)
    c.click(SEL('#motorista-nome'), at=c.L(9) - 0.2, label='Nome (campo)')
    c.type(SEL('#motorista-nome'), 'Sérgio Paiva', label='Nome: Sérgio Paiva', cps=40, noClick=True)
    c.click(SEL('#motorista-doc'), at=c.A(9, 'CPF', FC), label='CPF (campo)')
    c.type(SEL('#motorista-doc'), '46371820508', label='CPF', cps=40, noClick=True)
    c.press('Tab', label='vai ao Telefone')
    c.type(SEL('#motorista-tel'), '12900004417', label='Telefone', cps=40, noClick=True)
    c.mark(10)
    c.click(SEL('#motorista-cnh'), at=c.A(10, 'CNH', FC), label='CNH (campo)')
    c.type(SEL('#motorista-cnh'), '04581273671', at=c.A(10, 'número', 0.05), label='CNH', cps=40, noClick=True)
    c.click(SEL('#motorista-cnh-cat'), label='abre Categoria')
    c.type(SEL('[role=listbox]'), 'C', label='Categoria: procura C', cps=40, noClick=True)
    c.press('Enter', label='Categoria C')
    c.click(SEL('#motorista-cnh-val'), at=c.A(10, 'validade', FC), label='Validade da CNH (campo)')
    c.type(SEL('#motorista-cnh-val'), '18062030', label='Validade da CNH 18/06/2030', cps=40, noClick=True)
    c.mark(11)
    c.click(BTN('Cadastrar', within=DLG), at=c.A(11, 'Cadastrar', 1.0), label='Cadastrar motorista')
    c.waitfor(text='Motorista cadastrado', timeout=10)
    c.hover(SEL("main button:has-text('Sérgio Paiva')"), 1.5, at=c.A(11, 'escalado', FH), label='Sérgio Paiva na lista')
    c.fim()
    return c


@capitulo
def cap09():
    """As caçambas e onde estão: Equipamentos, tipos, unidades, Nova unidade Caçamba 06, Movimentar (Externo -> Minha base), Onde tudo está
    agora e a aba Movimentações."""
    c = Cap(9, start=(760, 420), setup=setup_em('/coletas/ordens', aquece=['/coletas/equipamentos'], extra=ABRE_GRUPO))
    c.mark(1)
    c.click(ITEM_MENU('Equipamentos'), at=c.A(1, 'Equipamentos', FC), label='menu Equipamentos')
    c.waitfor(text=PAGINAS['/coletas/equipamentos'], timeout=15)
    c.hover(TXTX(PAGINAS['/coletas/equipamentos'], exact=True), 0.6, at=c.A(1, 'bags', FH), label='caçambas, bags, caixas e paletes')
    c.mark(2)
    c.hover(TXTX('Tipos de equipamento', within='main', exact=True), 0.3, at=c.L(2) - 0.2, label='Tipos de equipamento')
    c.hover(SEL("main tr:has-text('Caçamba 5 m³')"), 2.0, label='Caçamba 5 m³: uma a uma')
    c.hover(SEL("main tr:has-text('Bag 1 m³')"), 2.0, at=c.A(2, 'bag', FH), label='Bag 1 m³: por quantidade')
    c.mark(3)
    rola_ate(c, 'Unidades identificáveis', c.L(3) - 0.2, 'desce às Unidades identificáveis', y=140)
    c.confere_item('main [role=listitem]', 'Caçamba 05', ['Depósito Irmãos Siqueira'], 'Caçamba 05 no Depósito Irmãos Siqueira')
    c.hover(SEL("main [role=listitem]:has-text('Caçamba 05')"), 0.6, at=c.A(3, 'Caçamba', FH), label='Caçamba 05')
    c.hover(SEL("main [role=listitem]:has-text('Caçamba 05') :text-is('Depósito Irmãos Siqueira')"), 1.5, at=c.A(3, 'Depósito', FH),
            label='Caçamba 05 no Depósito Irmãos Siqueira')
    c.mark(4)
    c.click(BTN('Nova unidade'), at=c.A(4, 'Nova', FC), label='Nova unidade')
    c.waitfor(target=SEL('#equipamento-id'), timeout=10)
    c.click(SEL('#equipamento-id'), label='Identificação (campo)')
    c.type(SEL('#equipamento-id'), 'Caçamba 06', at=c.A(4, 'Caçamba', 0.05, nth=1), label='Identificação: Caçamba 06', cps=40, noClick=True)
    c.press('Tab', label='vai ao Tipo de equipamento')
    c.press('Enter', label='abre Tipo de equipamento')
    c.waitfor(selector='[role=listbox]', timeout=5)
    c.press('Enter', label='Tipo: Caçamba 5 m³')
    c.click(BTN('Cadastrar', within=DLG), at=c.A(4, 'Cadastrar', FC), label='Cadastrar unidade')
    c.waitfor(text='Unidade cadastrada', timeout=10)
    c.mark(5)
    rola_ate(c, 'Unidades identificáveis', c.L(5) - 0.4, 'sobe a lista (Caçamba 06 à vista)', y=24, dur_ms=600)
    c.click(SEL("main [role=listitem]:has-text('Caçamba 06')"), label='Caçamba 06 na lista')
    c.hover(TXTX('Ainda sem movimentação registrada', within='main', exact=False), 1.2, label='sem lugar (sem movimentação)')
    c.mark(6)
    c.click(BTN('Movimentar', within='main'), at=c.A(6, 'Movimentar', FC), label='Movimentar')
    c.waitfor(text='Nova movimentação', timeout=10)
    c.hover(BTNX('Externo', within=DLG), 0.6, at=c.A(6, 'fora', FH), label='De: Externo (compra nova)')
    c.click(SEL(f"{DLG} button:has-text('Minha base') >> nth=1"), at=c.A(6, 'Minha', FC), label='Para: Minha base')
    c.click(BTN('Registrar', within=DLG), label='Registrar')
    c.waitfor(text='Movimentação registrada', timeout=10)
    c.hover(TXTX('Posição atual', within='main', exact=True), 1.2, at=c.A(6, 'base', FH, nth=1), label='Posição atual: Minha base')
    c.mark(7)
    c.cursor((760, 460), at=c.A(7, 'dica', 0.3), label='cursor em repouso (ilustração)')
    c.mark(8)
    rola_ate(c, 'Onde tudo está agora', c.L(8) - 0.2, 'desce a Onde tudo está agora', y=120)
    c.hover(TXTX('Na base', within='main', exact=True), 0.3, at=c.A(8, 'base', FH), label='Na base')
    c.hover(TXTX('Em campo', within='main', exact=True), 0.3, at=c.A(8, 'campo', FH), label='Em campo')
    c.hover(TXTX('Com parceiros', within='main', exact=True), 0.3, at=c.A(8, 'parceiros', FH), label='Com parceiros')
    c.mark(9)
    rola_topo_js = ("(async()=>{" + ACHA_ROLAGEM + "const c=rolagem(document.querySelector('main [role=tab]'));if(!c)return 'SEM ROLAGEM';"
                    "const y0=c.scrollTop,t0=performance.now();if(y0<3)return 'ok';" + SUAVE.replace('DUR', '600').replace('DESTINO', 'y0*(1-e)') +
                    "return 'topo:'+Math.round(c.scrollTop)})()")
    c.ev(rola_topo_js, at=c.L(9) - 0.6, label='sobe às abas')
    c.click(TAB('Movimentações'), label='aba Movimentações')
    c.hover(TXTX('Ordem 8', within='main', exact=False), 1.2, at=c.A(9, 'ordem', FH), label='as da troca de hoje: Ordem 8')
    c.fim()
    return c


@capitulo
def cap10():
    """O relatório: Este mês (4 coletas, 1 concluída, 25%), Mês passado (6, 5, 1, 100%), por status, motorista, veículo e parceiro."""
    c = Cap(10, start=(760, 420), setup=setup_em('/coletas/ordens', aquece=['/coletas/relatorio'], extra=ABRE_GRUPO))
    KPIS = SEL("main div.grid:has(:text-is('Total de coletas')) >> nth=-1")   # a grade mais interna (os quatro cartões)
    c.mark(1)
    c.click(ITEM_MENU('Relatório'), at=c.A(1, 'relatório', FC), label='menu Relatório')
    c.waitfor(text=PAGINAS['/coletas/relatorio'], timeout=15)
    c.confere_kpi([['Total de coletas', '4'], ['Concluídas', '1'], ['Canceladas', '0'], ['Taxa de conclusão', '25%']], 'Este mês: 4, 1, 0, 25%')
    c.hover(SEL('main button[role=combobox]'), 0.3, at=c.A(1, 'mês', FH, nth=1), label='Período: Este mês')
    c.hover(KPIS, 3.5, at=c.A(1, 'total', 1.0), label='Este mês: os quatro números')
    c.mark(2)
    c.click(SEL('main button[role=combobox]'), at=c.A(2, 'outubro', FC), label='abre Período')
    c.click(OPT('Mês passado'), label='Período: Mês passado')
    c.confere_kpi([['Total de coletas', '6'], ['Concluídas', '5'], ['Canceladas', '1'], ['Taxa de conclusão', '100%']], 'outubro: seis, cinco, uma, cem por cento')
    c.hover(KPIS, 4.0, label='outubro: os quatro números')
    c.mark(3)
    c.cursor((760, 460), at=c.A(3, 'dica', 0.3), label='cursor em repouso (ilustração)')
    c.mark(4)
    rola_ate(c, 'Por status', c.L(4) - 0.2, 'desce às tabelas', y=130)
    c.hover(TXTX('Por status', within='main', exact=True), 0.6, at=c.A(4, 'status', FH), label='Por status')
    c.hover(TXTX('Por parceiro', within='main', exact=True), 1.5, at=c.A(4, 'parceiro', FH), label='Por motorista, veículo e parceiro')
    c.mark(5)
    rola_ate(c, 'Período', c.L(5) - 0.2, 'sobe ao Período', y=160, prefixo=True)
    c.hover(SEL('main button[role=combobox]'), 3.0, label='Período (em que mês cada coleta entra)')
    c.fim()
    return c


@capitulo
def cap11():
    """As regras: Configurações, Prefixo da numeração "COL-", Janelas, Exigir motorista e veículo, Exigir aprovação, Antecedência mínima 24
    e Dias aceitos."""
    c = Cap(11, start=(760, 420), setup=setup_em('/coletas/ordens', aquece=['/coletas/configuracoes'], extra=ABRE_GRUPO))
    c.mark(1)
    c.click(ITEM_MENU('Configurações'), at=c.A(1, 'Configurações', FC), label='menu Configurações (Coletas)')
    c.waitfor(text=PAGINAS['/coletas/configuracoes'], timeout=15)
    c.hover(TXTX('Operação', within='main', exact=True), 0.8, at=c.A(1, 'operação', FH), label='bloco Operação')
    c.mark(2)
    c.hover(SEL('#col-prefix'), 1.0, at=c.L(2) - 0.2, label='Prefixo da numeração')
    c.click(SEL('#col-prefix'), at=c.A(2, 'coloco', FC), label='Prefixo (campo)')
    c.type(SEL('#col-prefix'), 'COL-', at=c.A(2, 'prefixo', 0.05, nth=1), label='Prefixo: COL-', cps=40, noClick=True)
    c.press('Tab', at=c.A(2, 'ordens', 0.2), label='sai do campo (salva o prefixo)')
    c.waitfor(text='Prefixo da numeração salvo', timeout=8)
    c.mark(3)
    c.hover(TXTX('Janelas de coleta oferecidas', within='main', exact=True), 0.6, at=c.L(3) - 0.2, label='Janelas de coleta oferecidas')
    c.hover(SEL("main button:text-is('Dia todo')"), 1.2, at=c.A(3, 'períodos', FH), label='as janelas: Manhã, Tarde e Dia todo')
    c.hover(TXTX('Exigir motorista e veículo para agendar', within='main', exact=True), 1.5, at=c.A(3, 'exigir', FH),
            label='Exigir motorista e veículo para agendar')
    c.mark(4)
    rola_ate(c, 'Portal e solicitações', c.L(4) - 0.2, 'desce ao bloco Portal e solicitações', y=120)
    c.hover(TXTX('Exigir aprovação da solicitação', within='main', exact=True), 2.0, label='Exigir aprovação da solicitação')
    c.mark(5)
    c.hover(SEL('#col-lead'), 1.0, at=c.L(5) - 0.2, label='Antecedência mínima (horas)')
    c.click(SEL('#col-lead'), at=c.A(5, 'coloco', FC), label='Antecedência (campo)')
    c.type(SEL('#col-lead'), '24', at=c.A(5, 'vinte', 0.4), label='Antecedência: 24', cps=40, noClick=True, clear=True)
    c.press('Tab', label='sai do campo (salva a antecedência)')
    c.waitfor(text='Antecedência mínima salva', timeout=8)
    c.hover(TXTX('Dias aceitos para coleta', within='main', exact=True), 0.3, at=c.A(5, 'aceitos', FH), label='Dias aceitos para coleta')
    c.aponta((388, 516), c.A(5, 'segunda', 0.35), 'Seg')
    c.aponta((708, 516), c.A(5, 'sábado', 0.35), 'Sáb')
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
