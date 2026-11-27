#!/usr/bin/env python3
"""T25 · gera rec/t25/cap00..cap11.json (roteiros do robô) a partir da voz (t25/narracao/capNN.json).

Dashboard, Agenda e rotina no COMPUTADOR (janela 1600x900), logado como Rafael Nogueira (MASTER, Recicla Vale Metais), EcoSistema 1.60.22.
Capítulos (14): 0 Abertura, 1 Comprado/vendido/margem, 2 Seis meses, 3 Semanas e rankings, 4 Quem deve e como você paga (NOVO), 5 Painel do seu jeito,
6 Tarefas no calendário, 7 Concluir/editar/excluir (NOVO), 8 Avisos automáticos, 9 Atalhos e Ctrl+K, 10 a 12 Rotinas, 13 Recapitulando.
FAKE_NOW 2026-11-10T08:30:00-03:00 (terça) em todos os capítulos. Instância do Supabase falso na porta 54325.
Cada passo é preso a uma palavra da fala: `at` = início da palavra - o custo do gesto (A(linha, palavra, folga)), para o cursor CHEGAR na
palavra (docs/04, "Custo real dos gestos"). Hoje a voz é ESTIMADA (capNN.json do preparar_aula.sh); com a voz real, rode de novo.
Rodar de qualquer pasta: `python3 -I rec/t25/gerar.py [NN ...]`. Depois: t25_ensaio.sh NN (ensaio rápido), prever.py NN --ens,
t25_ensaio.sh NN completo.

Cadeia de sementes (rec/mundo/seeds-extra/): o fim da T21 (CADEIA: t14/*, t15/*, t21/*) + `t25/inicio` (a Agenda do plano, com as tarefas do contador e da lona)
nos caps 0 a 6; `t25/apos-cap06` (a revisão do caminhão no dia 13) no cap 7; `t25/apos-cap07` (contador concluída, revisão 10:30, lona excluída) nos caps 8 a 12 e
`t25/apos-cap12` (Fechamento de novembro) no cap 13 (t25_sementes.py; apos-cap06 e apos-cap12 saem do ensaio rápido do capítulo com 0 passo falho; apos-cap07 é escrito por `apos07`).

Particularidades (lidas no código da 1.59.154 e conferidas nas explorações rec/t25/_ex/):
 - Cartões do topo: <div role=button> com o rótulo num <p>; o clique abre "Ver detalhes". Cada seção do painel é um
   div.relative.group com um botão-alça (cursor-grab) filho direto: dnd-kit, PointerSensor com 8 px.
 - O filtro de período e a lista "R$ / Kg" dos rankings são Select/botões comuns; as opções do Select pedem ponteiro real.
 - Agenda: o dia do calendário é um <div> com o número num <span>; a tarefa é um <button> dentro de um <div draggable> (arrasto nativo);
   Data do formulário = botão + calendário (react-day-picker), Horário = roleta (clicar no número a leva ao centro).
 - "Tarefas para hoje" abre ao montar a página (AppLayout) quando a marca do dia no localStorage falta: o cap. 8 tira a marca e navega.
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
NARR = os.path.join(TUT_HOME, 't25', 'narracao')
FAKE_NOW = '2026-11-10T08:30:00-03:00'
NOMES = ['Abertura', 'Comprado, vendido e margem', 'Seis meses e o comparativo', 'Semanas e rankings', 'Quem deve e como você paga', 'O painel do seu jeito',
         'Tarefas no calendário', 'Concluir, editar e excluir', 'Os avisos automáticos', 'Atalhos e o Ctrl+K', 'A rotina diária', 'A rotina semanal',
         'A rotina mensal', 'Recapitulando']
_T13 = ['t13/inicio', 't13/apos-cap11']   # o fim da T13 (pneus em 3 parcelas, baixas): a linha do tempo é T13 → T14 → T15 → T21 → T25
_T14 = ['t14/inicio'] + [f't14/apos-cap{n:02d}' for n in (2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 14)]
_T15 = ['t15/inicio', 't15/apos-cap01', 't15/apos-cap02', 't15/apos-cap10']
CADEIA = _T13 + _T14 + _T15 + ['t21/inicio', 't21/apos-cap02']   # o fim da T21, de onde a T25 parte (MUNDO_LINHA_DO_TEMPO, seção 14)
_I = CADEIA + ['t25/inicio']
_6 = _I + ['t25/apos-cap06']
_7 = _6 + ['t25/apos-cap07']
SEMENTE = {**{n: _I for n in range(0, 7)}, 7: _6, **{n: _7 for n in range(8, 13)}, 13: _7 + ['t25/apos-cap12']}

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

    def confere_campos(s, esperados, label, escopo='[role=dialog]'):
        """lê o VALOR dos campos (input/textarea) do escopo e compara com a fala"""
        esp = [esperados] if isinstance(esperados, str) else list(esperados)
        js = ("(async()=>{const esp=%s;let out='';for(let i=0;i<12;i++){const v=[...document.querySelectorAll(%s+' input, '+%s+' textarea')].map(e=>e.value).join(' | ');"
              "const falta=esp.filter(e=>!v.includes(e));if(!falta.length)return 'OK: '+esp.join(' | ');out='DIFERENTE: faltou '+JSON.stringify(falta)+' em: '+v.slice(0,260);"
              "await new Promise(r=>setTimeout(r,300));}return out})()") % (json.dumps(esp, ensure_ascii=False), json.dumps(escopo), json.dumps(escopo))
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

    def encaixa_hovers(s, custo=0.9, minimo=0.15):
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
            'name': f't25-cap{s.n:02d}',
            'title': f'T25 · Cap. {s.n} · {NOMES[s.n]} (narração{est} {str(round(s.dur, 1)).replace(".", ",")} s; marcas L1..L{len(s.linhas)} = '
                     f'início de cada linha do roteiro; FAKE_NOW {FAKE_NOW}; logado como Rafael Nogueira)',
            'seed': f't25-cap{s.n:02d}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
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
try:
    VERSAO = open(os.path.join(TUT_HOME, 'app', 'dist', '.versao-app'), encoding='utf8').read().strip() or '1.60.22'
except OSError:   # pragma: no cover
    VERSAO = '1.60.22'
HOJE = FAKE_NOW[:10]
STORAGE = {'app_version': VERSAO, 'notification_shown_version': VERSAO, 'pwa-install-dismissed': 'true', 'theme': 'light',
           f'daily-tasks-reminder-last-shown-{RAFAEL}': HOJE, 'initial-preferences-set': 'true'}
LOGIN = [{'do': 'waitFor', 'target': {'label': 'E-mail'}, 'timeout': 30},
         {'do': 'type', 'target': {'label': 'E-mail'}, 'text': '$TUT_USER', 'cps': 40},
         {'do': 'type', 'target': {'label': 'Senha', 'exact': True}, 'text': '$TUT_SENHA', 'cps': 40},
         {'do': 'click', 'target': {'role': 'button', 'name': 'Entrar', 'exact': True}},
         {'do': 'waitFor', 'text': 'Olá, Rafael!', 'timeout': 30}, AGUARDA]


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


def js_rola_linha(texto, y, dur_ms=700):
    """como js_rola, com o alvo = a 1ª linha da lista (main tbody tr) cujo texto contém `texto` (CSS puro não tem :has-text)"""
    return ("(async()=>{" + ACHA_ROLAGEM + f"const acha=()=>[...document.querySelectorAll('main tbody tr')].filter(e=>e.offsetParent&&e.innerText.includes({json.dumps(texto)}))[0];"
            "let el=acha();for(let i=0;i<20&&!el;i++){await new Promise(r=>setTimeout(r,150));el=acha();}"
            "if(!el)return 'SEM ALVO';const c=rolagem(el);if(!c)return 'SEM ROLAGEM';"
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


def js_clica(css, texto=None, espera_ms=3000):
    """clique por eval (sem cursor) no 1º elemento visível que casa o CSS (e contém `texto`), esperando até `espera_ms`: abre Popover e
    escolhe item do cmdk (aceitam .click(); o gatilho do Select do Radix não: docs/08, T5). Devolve 'ok: <texto>' ou 'SEM ALVO'."""
    filtro = f"&&e.textContent.includes({json.dumps(texto)})" if texto else ''
    return ("(async()=>{const acha=()=>[...document.querySelectorAll(" + json.dumps(css) + ")].find(e=>e.offsetParent" + filtro + ");"
            f"let el=acha();for(let i=0;i<{int(espera_ms / 100)}&&!el;i++){{await new Promise(r=>setTimeout(r,100));el=acha();}}"
            "if(!el)return 'SEM ALVO';el.click();return 'ok: '+el.textContent.trim().slice(0,60)})()")


def js_colar(texto):
    """cola o texto no campo em foco (execCommand insertText: o React recebe o input), ~0,05 s em vez de digitar letra a letra"""
    return ("(()=>{const e=document.activeElement;if(!e||!/^(INPUT|TEXTAREA)$/.test(e.tagName))return 'SEM ALVO (nada em foco)';"
            f"document.execCommand('insertText',false,{json.dumps(texto)});return e.value}})()")



POP = '[data-radix-popper-content-wrapper]'
COL = lambda n: SEL(f"main thead th:has-text('{n}')")
CARTAO = lambda t: {'text': t, 'exact': True, 'within': MAIN}
ABA = lambda n: SEL(f"main button:text-is('{n}')")


def colar(c, campo, texto, at_clique, at_texto, label):
    """clica no campo (cursor) e cola o texto (sem digitar letra a letra): texto longo que a fala só cita"""
    c.click(campo, at=at_clique, label=label + ' (clique no campo)')
    return c.ev(js_colar(texto), at=at_texto, label=label)


# ---------------------------------------------------------------- alvos do Dashboard e da Agenda
LINK = lambda n: {'role': 'link', 'name': n, 'exact': True}
MARGEM = 'Margem (Vendas − Compras)'
STAT = lambda t: SEL(f"main div[role=button]:has(p:text-is('{t}'))")                 # cartão do topo (Total Compras, Total Vendas, Margem)
SEC_CSS = "main div.relative.group:has(> button.cursor-grab)"                        # cada seção do painel (arrastável)
SEC = lambda t: SEL(f"{SEC_CSS}:has-text('{t}')")
GRAF = lambda t: SEL(f"{SEC_CSS}:has-text('{t}') .recharts-wrapper")
ALCA = lambda t: SEL(f"{SEC_CSS}:has-text('{t}') > button.cursor-grab")
FILTRO = lambda v: {'role': 'combobox', 'hasText': v}
OPCAO = lambda n: {'role': 'option', 'name': n}
CONFIG = BTN('Configurações', MAIN)
DIA_AG = lambda d: SEL(f"main div.grid.grid-cols-7 > div:not(.opacity-40):has(> span:text-is('{d}'))")   # dia do calendário da Agenda
AG_TAREFA = lambda t: SEL(f"main div.grid.grid-cols-7 button:has-text('{t}')")
AG_FERIADO = lambda t: SEL(f"main div.grid.grid-cols-7 div:has-text('{t}'):not(:has(div:has-text('{t}')))")
MES_PROX = SEL("main .border-b > div > div > button:nth-of-type(2)")                  # seta do próximo mês (a 2ª do cabeçalho do calendário)
NOVA_TAREFA = SEL("main button:has-text('Nova Tarefa'):visible")
HORAS = lambda h: SEL(f"[role=listbox][aria-label='Horas'] button[role=option]:text-is('{h}')")


def js_rola_sec(titulo, y, dur_ms=700):
    """rolagem suave da tela até a seção do painel cujo texto contém `titulo` ficar com o topo em y px"""
    return ("(async()=>{" + ACHA_ROLAGEM + f"const el=[...document.querySelectorAll('main div.relative.group')].filter(e=>e.offsetParent&&e.querySelector(':scope > button.cursor-grab')&&e.innerText.includes({json.dumps(titulo)}))[0];"
            "if(!el)return 'SEM ALVO';const c=rolagem(el);if(!c)return 'SEM ROLAGEM';"
            f"let dy=Math.round(el.getBoundingClientRect().top-{int(y)});const y0=c.scrollTop;dy=Math.max(-y0,Math.min(c.scrollHeight-c.clientHeight-y0,dy));"
            "if(Math.abs(dy)<3)return 'ok';" + SUAVE.replace('DUR', str(int(dur_ms))) + "return Math.round(el.getBoundingClientRect().top)})()")


def setup_dash(extra=()):
    """login (cai no Dashboard, "Olá, Rafael!") e as animações acertadas"""
    return LOGIN + list(extra) + [{'do': 'eval', 'js': ANIM}]


def setup_agenda(extra=()):
    """login e a Agenda de novembro aberta pelo menu (fora do vídeo)"""
    return LOGIN + [{'do': 'click', 'target': LINK('Agenda')}, {'do': 'waitFor', 'text': 'Gerencie suas tarefas e compromissos', 'timeout': 30},
                    AGUARDA] + list(extra) + [{'do': 'eval', 'js': ANIM}]


# ---------------------------------------------------------------- alvos novos (1.60.22)
DIA_NUM = lambda d: SEL(f"main div.grid.grid-cols-7 > div:not(.opacity-40) > span:text-is('{d}')")   # só o número do dia (o centro da célula cai na tarefa)
def js_btn_tarefa(titulo, qual):
    """clique por eval no botão do cartão da tarefa na lateral do dia: 'circulo' (rounded-full), 'lapis' ou 'lixeira' (pelo ícone)"""
    return ("(async()=>{const acha=()=>{const p=[...document.querySelectorAll('main div.group.rounded-lg.border > div.flex-1 > p')].find(x=>x.textContent.trim()===%s);"
            "return p?p.parentElement.parentElement:null};let c=acha();for(let i=0;i<30&&!c;i++){await new Promise(r=>setTimeout(r,100));c=acha();}"
            "if(!c)return 'SEM ALVO';const q=%s;const b=q==='circulo'?c.querySelector(':scope > button.rounded-full'):[...c.querySelectorAll('button')].find(x=>x.querySelector(q==='lapis'?\"svg[class*='lucide-pencil']\":\"svg[class*='lucide-trash']\"));"
            "if(!b)return 'SEM ALVO (botão)';b.click();return 'ok: '+q})()") % (json.dumps(titulo), json.dumps(qual))


MINUTOS = lambda m: SEL(f"[role=listbox][aria-label='Minutos'] button[role=option]:text-is('{m}')")
CARD_TAREFA = lambda t: f"main div.group.rounded-lg.border:has(> div.flex-1 > p:text-is('{t}'))"   # tarefa na lateral do dia (TaskCard)
CIRCULO = lambda t: SEL(f"{CARD_TAREFA(t)} > button.rounded-full")
LAPIS = lambda t: SEL(f"{CARD_TAREFA(t)} button:has(svg[class*='lucide-pencil'])")
LIXEIRA = lambda t: SEL(f"{CARD_TAREFA(t)} button:has(svg[class*='lucide-trash'])")
ALERTA = "[role=alertdialog]"
LE_SEC = lambda titulo: ("(()=>{const e=[...document.querySelectorAll('main div.relative.group')].find(x=>x.querySelector(':scope > button.cursor-grab')&&x.innerText.includes(%s));"
                         "return e?('LIDO: '+e.innerText.replace(/[\\n\\r\\t ]+/g,' ').slice(0,700)):'SEM ALVO'})()") % json.dumps(titulo)


def js_riscada(titulo, esperado):
    """OK/DIFERENTE: o título da tarefa na lateral está (esperado=True) ou não (False) riscado"""
    return ("(async()=>{for(let i=0;i<20;i++){const p=[...document.querySelectorAll('main div.group.rounded-lg.border > div.flex-1 > p')].find(x=>x.textContent.trim()===%s);"
            "if(p&&p.className.includes('line-through')===%s)return 'OK: '+%s+(%s?' riscada':' pendente');await new Promise(r=>setTimeout(r,300));}"
            "return 'DIFERENTE: '+%s+(%s?' não ficou riscada':' continua riscada')})()") % (
        json.dumps(titulo), 'true' if esperado else 'false', json.dumps(titulo), 'true' if esperado else 'false', json.dumps(titulo), 'true' if esperado else 'false')


# ---------------------------------------------------------------- capítulos
def cap00():
    """Abertura: o Dashboard (cartões e a faixa "1 lembrete para hoje") sob a ilustração das três perguntas (L2) e o cartão Antes: (L4);
    na L3 o cursor vai ao Dashboard e à Agenda, no menu."""
    c = Cap(0, setup=setup_dash(), start=(760, 300))
    c.mark(1)
    c.hover(SEL("main button:has-text('para hoje')"), 0.5, at=c.A(1, 'Esta', 0.6), label='a faixa "1 lembrete para hoje"')
    c.hover(STAT('Total Compras'), 0.4, at=c.A(1, 'Formação', 0.6), label='cartão Total Compras')
    c.hover(STAT('Total Vendas'), 0.4, at=c.A(1, 'tutorial,', 0.6), label='cartão Total Vendas')
    c.hover(STAT(MARGEM), 0.5, at=c.A(1, 'números', 0.6), label='cartão Margem')
    c.mark(2)
    c.mark(3)
    c.hover(LINK('Dashboard'), 1.2, at=c.A(3, 'Dashboard,', 0.9), label='destaque: Dashboard (menu)', noScroll=True)
    c.hover(LINK('Agenda'), 1.2, at=c.A(3, 'Agenda,', 0.9), label='destaque: Agenda (menu)')
    c.mark(4)
    c.fim()
    return c


def cap01():
    """Comprado, vendido e margem (7 linhas): os três cartões de novembro, o filtro de período aberto (L2), a margem verde (L3), a ilustração
    margem x lucro (L4), outubro em "Mês passado" (L5), o "Ver detalhes" da margem (L6) e o do Total Compras com "Por forma de pagamento" (L7)."""
    c = Cap(1, setup=setup_dash(), start=(760, 300))
    c.mark(1)
    c.hover(STAT('Total Compras'), 0.4, at=c.A(1, 'Total', 0.6, nth=0), label='destaque: Total Compras')
    c.hover(STAT('Total Vendas'), 0.4, at=c.A(1, 'Total', 0.6, nth=1), label='destaque: Total Vendas')
    c.hover(STAT(MARGEM), 0.4, at=c.A(1, 'Margem.', 0.6), label='destaque: Margem')
    c.hover(FILTRO('Este mês'), 0.6, at=c.A(1, 'Este', 0.6), label='o filtro de período em Este mês')
    c.mark(2)
    c.click(FILTRO('Este mês'), at=c.A(2, 'filtro,', 0.9), label='abre a lista do filtro de período')
    c.hover(OPCAO('Hoje'), 0.4, at=c.A(2, 'hoje,', 0.6), label='destaque na lista: Hoje')
    c.hover(OPCAO('Últimos 7 dias'), 0.4, at=c.A(2, 'últimos', 0.6), label='destaque na lista: Últimos 7 dias')
    c.hover(OPCAO('Este ano'), 0.4, at=c.A(2, 'este', 0.6), label='destaque na lista: Este ano')
    c.hover(OPCAO('Personalizado'), 0.6, at=c.A(2, 'Personalizado,', 0.6), label='destaque na lista: Personalizado')
    c.press('Escape', at=round(c.L(3) - 1.0, 2), label='fecha a lista sem escolher')
    c.mark(3)
    c.hover(STAT(MARGEM), 1.4, at=c.A(3, 'margem:', 0.6), label='ZOOM cartão Margem de novembro (verde)')
    c.confere('main', ['99.838,75'], 'margem de novembro na tela')
    c.mark(4)
    c.mark(5)
    c.click(FILTRO('Este mês'), at=c.A(5, 'Agora,', 0.7), label='abre o filtro de período')
    c.click(OPCAO('Mês passado'), at=c.A(5, 'outubro', 0.7), label='escolhe Mês passado')
    c.waitfor(text='256.860,00', timeout=15)
    c.hover(STAT('Total Compras'), 0.5, at=c.A(5, 'inteiro.', 0.2), label='ZOOM cartões de outubro: Total Compras')
    c.hover(STAT('Total Vendas'), 0.5, at=c.A(5, 'passaram', 0.6), label='ZOOM cartões de outubro: Total Vendas')
    c.hover(STAT(MARGEM), 0.8, at=c.A(5, 'margem', 0.6), label='ZOOM cartões de outubro: Margem 12.380,00')
    c.confere('main', ['256.860,00', '269.240,00', '12.380,00'], 'outubro na tela (T15)')
    c.mark(6)
    c.click(STAT(MARGEM), at=c.A(6, 'detalhes,', 0.8), label='Ver detalhes da margem')
    c.waitfor(text='Como é calculado', timeout=10)
    c.hover(SEL(f"{DLG} :text-is('Como é calculado')"), 0.6, at=c.A(6, 'conta', 0.6), label='o bloco Como é calculado')
    c.press('Escape', at=round(c.L(7) - 1.0, 2), label='fecha a janela da margem')
    c.mark(7)
    c.click(STAT('Total Compras'), at=c.A(7, 'Total', 0.8, nth=0), label='Ver detalhes do Total Compras')
    c.waitfor(text='Por forma de pagamento', timeout=10)
    c.hover(SEL(f"{DLG} :text-is('Por forma de pagamento')"), 1.0, at=c.A(7, 'forma', 0.7), label='ZOOM Por forma de pagamento')
    c.ev("(()=>{const d=[...document.querySelectorAll('[role=dialog]')].pop();return d?('LIDO: '+d.innerText.replace(/[\\n\\r\\t ]+/g,' ').slice(0,600)):'SEM ALVO'})()", label='LER a janela do Total Compras (formas de pagamento de outubro)')
    c.press('Escape', at=round(c.dur - 1.0, 2), label='fecha a janela')
    c.fim()
    return c


def cap02():
    """Seis meses e o comparativo: Compras vs Vendas, Evolução da Margem, o filtro lá em cima (L3) e o Comparativo Mensal de vendas (zoom)."""
    c = Cap(2, setup=setup_dash(), start=(760, 300))
    c.mark(1)
    c.ev(js_rola_sec('Compras vs Vendas', 120, 900), at=round(c.L(1) + 0.4, 2), label='desce a tela até os gráficos')
    c.hover(GRAF('Compras vs Vendas'), 0.8, at=c.A(1, 'duas', 0.7), label='as duas barras de cada mês')
    c.mark(2)
    c.hover(GRAF('Evolução da Margem'), 0.8, at=c.A(2, 'Evolução', 0.7), label='Evolução da Margem')
    c.mark(3)
    c.hover(SEL(f"{SEC_CSS}:has-text('Compras vs Vendas') :text-is('Compras vs Vendas (Últimos 6 Meses)')"), 0.8, at=c.A(3, 'seis', 0.7), label='destaque: (Últimos 6 Meses)')
    c.ev(js_topo(700), at=c.A(3, 'filtro', 1.3, nth=0), label='sobe a tela até o filtro')
    c.hover(FILTRO('Este mês'), 0.8, at=c.A(3, 'filtro', 0.6, nth=1), label='o filtro em Este mês')
    c.mark(4)
    c.ev(js_rola_sec('Comparativo Mensal - Total Compras', 160, 900), at=round(c.L(4) + 0.1, 2), label='desce a tela até o Comparativo Mensal')
    c.hover(SEC('Comparativo Mensal - Total Vendas'), 1.6, at=c.A(4, 'mês', 0.6, nth=0), label='ZOOM Comparativo Mensal - Total Vendas')
    c.mark(5)
    c.fim()
    return c


def cap03():
    """Semanas e rankings (7 linhas): Volume Semanal (dica Peso), filtro em Mês passado, Materiais (R$ e Kg), Fornecedores, Clientes (R$ e Kg),
    "Todos os clientes" com o seletor Por Valor / Por Quantidade (L6) e o clique no nome do pódio, que abre o histórico do parceiro (L7)."""
    c = Cap(3, setup=setup_dash(), start=(760, 300))
    c.mark(1)
    c.ev(js_rola_sec('Volume Semanal de Compras', 130, 900), at=round(c.L(1) + 0.2, 2), label='desce a tela até o Volume Semanal')
    c.hover(SEC('Volume Semanal de Compras'), 0.6, at=c.A(1, 'oito', 0.7), label='as oito semanas')
    c.mark(2)
    c.hover(GRAF('Volume Semanal de Compras'), 1.2, at=c.A(2, 'mouse,', 0.7), label='a dica Peso de uma semana')
    c.ev(js_topo(700), at=c.A(2, 'seja', 0.6), label='sobe a tela até o filtro')
    c.click(FILTRO('Este mês'), at=c.A(2, 'filtro.', 0.9), label='abre o filtro de período')
    c.mark(3)
    c.click(OPCAO('Mês passado'), at=round(c.L(3) + 0.5, 2), label='escolhe Mês passado')
    c.ev(js_rola_sec('Materiais Mais Comprados', 130, 900), at=c.A(3, 'valer.', 0.5), label='desce a tela até os rankings')
    c.click(SEL(f"{SEC_CSS}:has-text('Materiais Mais Comprados') button:text-is('Kg')"), at=c.A(3, 'quilos:', 1.0), label='ranking de materiais em Kg')
    c.hover(SEC('Materiais Mais Comprados'), 1.2, at=c.A(3, 'cinquenta', 0.7), label='ZOOM Ferro pesado em primeiro, com o peso')
    c.confere('main', ['Ferro pesado', '50.000'], 'Ferro pesado, 50.000 kg')
    c.mark(4)
    c.hover(SEC('Principais Fornecedores'), 1.4, at=c.A(4, 'primeiro', 0.7), label='Principais Fornecedores: Depósito Irmãos Siqueira em primeiro')
    c.confere('main', ['Depósito Irmãos Siqueira'], 'primeiro fornecedor')
    c.mark(5)
    c.ev(js_rola_sec('Principais Clientes', 130, 900), at=round(c.L(5) + 0.1, 2), label='desce a tela até Principais Clientes')
    c.hover(SEC('Principais Clientes'), 1.0, at=c.A(5, 'Fundição', 0.7), label='Fundição Bandeira do Vale em primeiro, em reais')
    c.click(SEL(f"{SEC_CSS}:has-text('Principais Clientes') button:text-is('Kg')"), at=c.A(5, 'quilos,', 0.8), label='Principais Clientes em Kg: Aços Quiririm')
    c.mark(6)
    c.click(BTN('Ver todos os clientes'), at=c.A(6, 'Ver', 0.8), label='Ver todos os clientes')
    c.waitfor(text='Todos os clientes', timeout=10)
    c.click(SEL(f"{DLG} [role=combobox]"), at=c.A(6, 'valor', 1.0), label='abre o seletor Por Valor (R$)')
    c.click(OPCAO('Por Quantidade (kg)'), at=c.A(6, 'ou', 0.65), label='escolhe Por Quantidade (kg)')
    c.hover(SEL(f"{DLG} :text-is('Todos os clientes')"), 0.6, at=c.A(6, 'quilos.', 0.9), label='a lista por quantidade')
    c.press('Escape', at=round(c.L(7) - 1.0, 2), label='fecha a lista')
    c.mark(7)
    c.click(SEL(f"{SEC_CSS}:has-text('Principais Clientes') :text-is('Aços Quiririm Ltda')"), at=c.A(7, 'nome', 0.9), label='clica no nome no pódio: abre o histórico do parceiro')
    c.waitfor(idle=True)
    c.fim()
    return c


def cap04():
    """Quem deve e como você paga (8 linhas, novo): "Saldos em Aberto" (A receber, A pagar, Posição líquida), a dica do filtro, "Ver relatório"
    (Relatório de Saldos, Exportar Relatório aberto), "Métodos de Pagamento das Compras" (pizza e lista) e o fim do painel (DRE, Regime de Caixa)."""
    c = Cap(4, setup=setup_dash(), start=(760, 300))
    SALDOS = SEC('Saldos em Aberto')
    c.mark(1)
    c.ev(js_rola_sec('Saldos em Aberto', 130, 900), at=round(c.L(1) + 0.2, 2), label='desce a tela até Saldos em Aberto')
    c.hover(SALDOS, 0.8, at=c.A(1, 'Saldos', 0.7), label='o cartão Saldos em Aberto')
    c.ev(LE_SEC('Saldos em Aberto'), at=round(c.L(1) + 4.0, 2), label='LER o cartão Saldos em Aberto')
    c.mark(2)
    c.hover(SEL(f"{SEC_CSS}:has-text('Saldos em Aberto') p:text-is('A receber')"), 0.8, at=c.A(2, 'maiores', 0.7), label='coluna A receber')
    c.hover(SEL(f"{SEC_CSS}:has-text('Saldos em Aberto') p:text-is('A pagar')"), 0.8, at=c.A(2, 'valor', 0.7), label='coluna A pagar')
    c.hover(SEL(f"{SEC_CSS}:has-text('Saldos em Aberto') span:text-is('Fundição Bandeira do Vale')"), 1.0, at=c.A(2, 'Fundição', 0.8), label='ZOOM Fundição Bandeira do Vale, a que mais deve')
    c.mark(3)
    c.hover(SEL(f"{SEC_CSS}:has-text('Saldos em Aberto') span:text-is('Posição líquida')"), 1.2, at=c.A(3, 'Posição', 0.7), label='destaque: Posição líquida')
    c.mark(4)
    c.ev(js_topo(800), at=c.A(4, 'cartão', 0.8), label='sobe a tela até o filtro')
    c.hover(FILTRO('Este mês'), 0.8, at=c.A(4, 'filtro.', 0.8), label='o filtro em Este mês')
    c.ev(js_rola_sec('Saldos em Aberto', 130, 900), at=c.A(4, 'hoje,', 1.0), label='volta ao cartão Saldos em Aberto')
    c.hover(SALDOS, 1.0, at=c.A(4, 'seja', 0.6), label='o saldo de hoje, seja qual for o período')
    c.mark(5)
    c.click(SEL(f"{SEC_CSS}:has-text('Saldos em Aberto') button:text-is('Ver relatório')"), at=c.A(5, 'Ver', 0.9), label='Ver relatório')
    c.waitfor(text='Relatório de Saldos', timeout=10)
    c.click(SEL(f"{DLG} button:has-text('Exportar Relatório')"), at=c.A(5, 'exportar.', 1.0), label='abre o menu Exportar Relatório (sem escolher)')
    c.waitfor(text='Exportar em Excel', timeout=6)
    c.press('Escape', at=round(c.L(6) - 1.4, 2), label='fecha o menu de exportação')
    c.press('Escape', at=round(c.L(6) - 0.9, 2), label='fecha o Relatório de Saldos')
    c.mark(6)
    c.ev(js_rola_sec('Métodos de Pagamento das Compras', 130, 900), at=round(c.L(6) + 0.2, 2), label='desce a tela até Métodos de Pagamento das Compras')
    c.hover(SEC('Métodos de Pagamento das Compras'), 0.8, at=c.A(6, 'Métodos', 0.7), label='o cartão Métodos de Pagamento das Compras')
    c.hover(SEL(f"{SEC_CSS}:has-text('Métodos de Pagamento das Compras') span:text-is('Dinheiro')"), 0.6, at=c.A(6, 'dinheiro,', 0.7), label='linha Dinheiro')
    c.hover(SEL(f"{SEC_CSS}:has-text('Métodos de Pagamento das Compras') span:text-is('Pix/Transferência')"), 0.6, at=c.A(6, 'Pix', 0.7), label='linha Pix/Transferência')
    c.hover(SEL(f"{SEC_CSS}:has-text('Métodos de Pagamento das Compras') span:text-is('Saldo')"), 0.6, at=c.A(6, 'saldo,', 0.7), label='linha Saldo')
    c.ev(LE_SEC('Métodos de Pagamento das Compras'), at=round(c.L(6) + 9.0, 2), label='LER Métodos de Pagamento das Compras')
    c.mark(7)
    c.hover(SEL(f"{SEC_CSS}:has-text('Métodos de Pagamento das Compras') span:text-is('Dinheiro')"), 1.4, at=c.A(7, 'termômetro', 0.7), label='ZOOM linha Dinheiro')
    c.mark(8)
    c.ev(js_rola_sec('Demonstrativo Financeiro (DRE)', 110, 1000), at=round(c.L(8) + 0.1, 2), label='desce a tela até o fim do painel: DRE')
    c.hover(SEC('Demonstrativo Financeiro (DRE)'), 1.0, at=c.A(8, 'DRE', 0.6), label='o DRE resumido')
    c.hover(SEL(f"{SEC_CSS}:has-text('Demonstrativo Financeiro (DRE)') :text-is('Regime de Caixa')"), 1.0, at=c.A(8, 'tutorial', 0.9), label='destaque: Regime de Caixa (sem clicar)')
    c.fim()
    return c


def cap05():
    """O painel do seu jeito: Configurações, chave de Métodos de Pagamento, arrasto do Volume Semanal (dnd-kit) e Voltar ordem ao normal."""
    c = Cap(5, setup=setup_dash(), start=(760, 300))
    c.mark(1)
    c.hover(CONFIG, 0.6, at=c.A(1, 'Configurações,', 0.7), label='destaque: Configurações')
    c.click(CONFIG, at=c.A(1, 'ficam', 0.8), label='abre Configurações do Dashboard')
    c.waitfor(text='Configurações do Dashboard', timeout=10)
    c.mark(2)
    c.click(SEL(f"{DLG} div:has(> span:text-is('Métodos de Pagamento')) [role=switch]"), at=c.A(2, 'Desligo', 0.9), label='desliga Métodos de Pagamento')
    c.press('Escape', at=c.A(2, 'sai', 0.6), label='fecha a janela: o cartão sai do painel')
    c.mark(3)
    c.ev(js_rola_sec('Compras vs Vendas', 110, 900), at=c.A(3, 'ordem,', 0.4), label='ajusta a tela para o arrasto')
    c.hover(SEC('Volume Semanal de Compras'), 0.5, at=c.A(3, 'cantinho', 1.0), label='a alça do cartão Volume Semanal aparece')
    c.add({'do': 'drag', 'target': ALCA('Volume Semanal de Compras'), 'to': SEC('Compras vs Vendas'), 'at': c.A(3, 'arrastar.', 1.3), 'label': 'arrasta o Volume Semanal para depois dos cartões do topo'})
    c.mark(4)
    c.click(CONFIG, at=c.A(4, 'Voltar', 2.2), label='abre Configurações de novo')
    c.hover(BTN('Voltar ordem ao normal'), 1.4, at=c.A(4, 'Voltar', -0.45), label='destaque: Voltar ordem ao normal (sem clicar)')
    c.press('Escape', at=round(c.dur - 1.2, 2), label='fecha a janela')
    c.fim()
    return c


def cap06():
    """Tarefas no calendário: menu Agenda, Nova Tarefa (revisão do caminhão truck, 12/11 09:00, Lembrar no dia), Salvar, arrasto para o dia 13 e os feriados.
    Parte de `inicio` (que agora traz também as tarefas do contador, dia 9, e da lona, dia 18, para o cap07)."""
    c = Cap(6, setup=setup_dash(), start=(760, 300))
    c.mark(1)
    c.click(LINK('Agenda'), at=c.A(1, 'Agenda,', 0.9), label='menu Agenda')
    c.waitfor(text='Gerencie suas tarefas e compromissos', timeout=15)
    c.ev(ANIM)
    c.mark(2)
    c.click(NOVA_TAREFA, at=c.A(2, 'Nova', 1.7), label='Nova Tarefa')
    c.waitfor(text='Título', timeout=10)
    c.type(SEL(f"{DLG} input[placeholder='Título']"), 'Revisão do caminhão truck', at=c.A(2, 'revisão', 0.3), label='digita o título', cps=14, noClick=True)
    c.click(SEL(f"{DLG} button:has(svg.lucide-calendar)"), at=c.A(2, 'quinta,', 1.0), label='campo Data')
    c.click(SEL(f"{POP} button[name='day']:not(.day-outside):text-is('12')"), at=c.A(2, 'doze,', 0.7), label='dia 12')
    c.click(SEL(f"{DLG} button:has(svg.lucide-clock)"), at=c.A(2, 'nove', 2.2), label='campo Horário')
    c.click(HORAS('09'), at=c.A(2, 'nove', 1.0), label='hora 09')
    c.click(BTN('Concluir'), at=c.A(3, 'Com', 1.9), label='Concluir o horário')
    c.mark(3)
    c.hover(SEL(f"{DLG} div:has(> label:text-is('Lembrar no dia'))"), 1.2, at=c.A(3, 'Lembrar', 0.6), label='destaque: Lembrar no dia, ligado')
    c.click(SEL(f"{DLG} button:has-text('Salvar')"), at=c.A(3, 'Salvo,', 0.7), label='Salvar')
    c.waitfor(text='Tarefa criada com sucesso', timeout=10)
    c.mark(4)
    c.add({'do': 'drag', 'target': AG_TAREFA('Revisão do caminhão truck'), 'to': DIA_AG('13'), 'at': c.A(4, 'sexta?', 0.2), 'label': 'arrasta a tarefa do dia 12 para o dia 13'})
    c.mark(5)
    c.hover(AG_FERIADO('Proclamação da República'), 0.9, at=c.A(5, 'Proclamação', 0.7), label='destaque: Proclamação da República (dia 15)')
    c.hover(AG_FERIADO('Consciência Negra'), 0.9, at=c.A(5, 'Consciência', 0.7), label='destaque: Consciência Negra (dia 20)')
    c.mark(6)
    c.fim()
    return c


def cap07():
    """Concluir, editar e excluir (9 linhas, novo): círculo da tarefa do contador (dia 9: riscada, volta a pendente, conclui de novo), lápis na revisão do
    dia 13 (Horário 10:30), lixeira na lona do dia 18 (confirmação), a Coleta (Categoria e Cliente / Fornecedor), a Legenda, as vistas Semana, Dia, Mês e
    Hoje, e o duplo clique no dia 19. Parte de `apos-cap06`; termina em `apos-cap07` (escrito por t25_sementes.py apos07)."""
    c = Cap(7, setup=setup_agenda(), start=(760, 300))
    CONT = 'Ligar pro contador sobre as notas de outubro'
    REV = 'Revisão do caminhão truck'
    c.mark(1)
    c.click(DIA_NUM('9'), at=c.A(1, 'Ontem', 0.9), label='clica no dia 9')
    c.waitfor(selector=CARD_TAREFA(CONT), timeout=10)
    c.hover(SEL(CARD_TAREFA(CONT)), 0.8, at=c.A(1, 'contador,', 0.7), label='a tarefa do contador, ainda aberta')
    c.mark(2)
    c.ev(js_btn_tarefa(CONT, 'circulo'), at=c.A(2, 'círculo', 0.5), label='clica no círculo da tarefa')
    c.waitfor(text='Tarefa atualizada', timeout=8)
    c.ev(js_riscada(CONT, True), label='confere riscada')
    c.mark(3)
    c.ev(js_btn_tarefa(CONT, 'circulo'), at=c.A(3, 'Um', 0.5), label='clica de novo: volta a pendente')
    c.ev(js_riscada(CONT, False), label='confere pendente')
    c.ev(js_btn_tarefa(CONT, 'circulo'), at=c.A(3, 'Concluo', 0.4), label='conclui outra vez')
    c.ev(js_riscada(CONT, True), label='confere riscada de novo')
    c.mark(4)
    c.click(DIA_NUM('13'), at=c.A(4, 'Pra', 0.9), label='clica no dia 13')
    c.waitfor(selector=CARD_TAREFA(REV), timeout=10)
    c.hover(SEL(CARD_TAREFA(REV)), 0.8, at=c.A(4, 'mouse', 0.7), label='passa o mouse na revisão: aparecem o lápis e a lixeira')
    c.ev(js_btn_tarefa(REV, 'lapis'), at=c.A(4, 'lápis.', 0.5), label='clica no lápis')
    c.waitfor(text='Editar Tarefa', timeout=10)
    c.click(SEL(f"{DLG} button:has(svg.lucide-clock)"), at=c.A(4, 'horário', 0.9), label='campo Horário')
    c.click(HORAS('10'), at=c.A(4, 'dez', 0.8), label='hora 10')
    c.click(MINUTOS('30'), at=c.A(4, 'meia,', 0.8), label='minuto 30')
    c.click(BTN('Concluir'), at=c.A(4, 'salvo.', 1.7), label='Concluir o horário')
    c.click(SEL(f"{DLG} button:has-text('Salvar')"), at=c.A(4, 'salvo.', 0.6), label='Salvar')
    c.waitfor(text='Tarefa atualizada', timeout=8)
    c.mark(5)
    c.click(DIA_NUM('18'), at=c.A(5, 'E', 0.8), label='clica no dia 18')
    c.waitfor(selector=CARD_TAREFA('Buscar a lona nova do caminhão'), timeout=10)
    c.hover(SEL(CARD_TAREFA('Buscar a lona nova do caminhão')), 0.8, at=c.A(5, 'lixeira', 0.8), label='passa o mouse na lona')
    c.ev(js_btn_tarefa('Buscar a lona nova do caminhão', 'lixeira'), at=c.A(5, 'exclui.', 0.4), label='clica na lixeira')
    c.waitfor(text='Tem certeza que deseja excluir esta tarefa?', timeout=8)
    c.click(SEL("[role=alertdialog] button:text-is('Excluir Tarefa')"), at=c.A(5, 'sai', 0.9), label='confirma: Excluir Tarefa')
    c.waitfor(text='Tarefa excluída', timeout=8)
    c.mark(6)
    c.hover(AG_TAREFA('Coleta na Auto Peças Vale Forte'), 1.0, at=c.A(6, 'Cada', 0.7), label='cartão da tarefa Coleta (categoria e cor)')
    c.click(AG_TAREFA('Coleta na Auto Peças Vale Forte'), at=c.A(6, 'Na', 1.2), label='abre a tarefa Coleta em Editar Tarefa')
    c.waitfor(text='Editar Tarefa', timeout=10)
    c.hover(SEL(f"{DLG} label:text-is('Categoria')"), 0.8, at=c.A(6, 'categoria', 0.7, nth=1), label='destaque: Categoria (Coleta)')
    c.hover(SEL(f"{DLG} label:has-text('Cliente / Fornecedor')"), 1.0, at=c.A(6, 'campo', 0.7), label='destaque: Cliente / Fornecedor')
    c.confere('dlg', ['Cliente / Fornecedor', 'Auto Peças Vale Forte'], 'Coleta com Cliente / Fornecedor')
    c.click(BTN('Cancelar', DLG), at=round(c.L(7) - 1.9, 2), label='Cancelar')
    c.mark(7)
    c.ev("(()=>{const e=[...document.querySelectorAll('span')].find(x=>x.textContent.trim()==='Legenda:');if(!e)return 'SEM ALVO';e.scrollIntoView({block:'center',behavior:'smooth'});return 'ok'})()",
         at=round(c.L(7) + 0.1, 2), label='mostra a Legenda')
    c.hover(SEL("main span:text-is('Legenda:')"), 1.2, at=c.A(7, 'legenda,', 0.8), label='destaque: Legenda')
    c.mark(8)
    c.click(SEL("main button:text-is('Semana')"), at=c.A(8, 'semana,', 0.9), label='vista Semana')
    c.click(SEL("main button:text-is('Dia')"), at=c.A(8, 'dia', 0.8), label='vista Dia')
    c.click(SEL("main button:text-is('Mês')"), at=c.A(8, 'mês.', 0.8), label='vista Mês')
    c.click(SEL("main button:text-is('Hoje')"), at=c.A(8, 'Hoje', 0.8), label='botão Hoje')
    c.mark(9)
    c.add({'do': 'dblclick', 'target': DIA_NUM('19'), 'at': c.A(9, 'dois', 0.9), 'label': 'duplo clique no dia 19'})
    c.waitfor(text='Nova Tarefa', timeout=8)
    c.confere('dlg', ['19/11/2026'], 'Nova Tarefa já em 19/11/2026')
    c.click(BTN('Cancelar', DLG), at=round(c.dur - 1.0, 2), label='Cancelar')
    c.fim()
    return c


def cap08():
    """Os avisos automáticos: A Pagar e A Receber (zoom no 17 e no 23), o clique no aviso (Contas), Shift+A, dezembro e o Shift+D."""
    c = Cap(8, setup=setup_agenda(), start=(760, 300))
    c.mark(1)
    c.hover(SEL("main div.grid.grid-cols-7 button:has-text('A Pagar')"), 0.8, at=c.A(1, 'pagar', 0.7), label='destaque: avisos A Pagar (vermelho)')
    c.hover(SEL("main div.grid.grid-cols-7 button:has-text('A Receber')"), 0.8, at=c.A(1, 'receber', 0.7), label='destaque: avisos A Receber (verde)')
    c.mark(2)
    c.hover(SEL("main div.grid.grid-cols-7 button:has-text('A Receber: R$ 4.790,00')"), 1.4, at=c.A(2, 'dezessete,', 0.7), label='ZOOM A Receber: R$ 4.790,00, no dia 17')
    c.mark(3)
    c.hover(SEL("main div.grid.grid-cols-7 button:has-text('A Pagar: R$ 2.360,00')"), 1.4, at=c.A(3, 'três,', 0.7), label='ZOOM A Pagar: R$ 2.360,00, no dia 23')
    c.mark(4)
    c.mark(5)
    c.click(SEL("main div.grid.grid-cols-7 button:has-text('A Receber: R$ 4.790,00')"), at=c.A(5, 'aviso,', 0.8), label='clica no aviso do dia 17')
    c.waitfor(text='Contas a Pagar/Receber', timeout=15)
    c.mark(6)
    c.press('Shift+A', at=round(c.L(6) - 1.2, 2), label='Shift+A volta à Agenda')
    c.waitfor(text='Gerencie suas tarefas e compromissos', timeout=15)
    c.click(MES_PROX, at=c.A(6, 'vencimento', 0.9), label='seta do próximo mês: dezembro')
    c.hover(AG_TAREFA('Vencimento - Assinatura EcoSistema'), 1.2, at=c.A(6, 'laranja:', 0.6), label='ZOOM Vencimento - Assinatura EcoSistema (laranja), dia 5')
    c.mark(7)
    c.press('Shift+D', at=c.A(7, 'Dashboard,', 1.0), label='Shift+D abre o Dashboard')
    c.waitfor(text='lembrete', timeout=15)
    c.fim()
    return c


def cap09():
    """Atalhos e o Ctrl+K (10 linhas): a busca, "cobre" -> Cobre mel (preços), Enter (L3), "fundi" -> Fundição (telefone e Saldo, L4), as Ações Rápidas
    com a busca vazia (L5), "atalho" -> Atalhos de Teclado (L6), a lista com Compra, Venda, Caixa, Pedidos, Ver Estoque, Configurações e Agenda (L7),
    Shift+X e Shift+D (L8) e Shift+S -> Configurações -> Atalhos (L10)."""
    c = Cap(9, setup=setup_dash(), start=(760, 300))
    BUSCA = SEL("[role=dialog] input")
    c.mark(1)
    c.ev("(()=>{const a=document.activeElement;if(a&&a!==document.body)a.blur();return 'foco fora de campo'})()", at=0.2, label='foco fora de campo')
    c.press('Control+k', at=c.A(1, 'Ctrl+K', 0.2), label='Ctrl+K abre a busca')
    c.waitfor(selector='[role=dialog] input', timeout=10)
    c.mark(2)
    c.type(BUSCA, 'cobre', at=c.A(2, 'cobre,', 0.6), label='digita cobre', cps=8, noClick=True)
    c.hover(SEL("[role=dialog] [cmdk-item]:has-text('Cobre mel')"), 1.0, at=c.A(2, 'Cobre', 0.8, nth=1), label='passa o mouse em Cobre mel')
    c.hover(SEL("[role=dialog] :text-is('P. Compra')"), 1.2, at=c.A(2, 'quarenta', 0.9), label='ZOOM P. Compra e P. Venda do Cobre mel')
    c.confere('dlg', ['42,50', '47,90'], 'preços do Cobre mel')
    c.mark(3)
    c.hover(SEL("[role=dialog] div.border-t:has(> kbd)"), 0.8, at=c.A(3, 'Enter,', 0.7), label='Pressione Enter para abrir')
    c.mark(4)
    c.type(BUSCA, 'fundi', at=c.A(4, 'Fundição,', 0.6), label='digita fundi', cps=8, clear=True, noClick=True)
    c.hover(SEL("[role=dialog] [cmdk-item]:has-text('Fundição Bandeira do Vale')"), 1.0, at=c.A(4, 'painel', 0.8), label='passa o mouse em Fundição Bandeira do Vale')
    c.hover(SEL("[role=dialog] :text-is('Saldo')"), 1.2, at=c.A(4, 'saldo', 0.8), label='ZOOM o telefone e o Saldo do cliente')
    c.ev("(()=>{const d=document.querySelector('[role=dialog]');return d?('LIDO: '+d.innerText.replace(/[\\n\\r\\t ]+/g,' ').slice(0,400)):'SEM ALVO'})()", at=round(c.L(4) + 6.0, 2), label='LER o painel de Fundição')
    c.hover(SEL("[role=dialog] div.border-t:has(> kbd)"), 0.8, at=c.A(4, 'Enter,', 0.7), label='Pressione Enter para abrir o histórico')
    c.mark(5)
    c.press('Control+a', at=round(c.L(5) - 0.1, 2), label='seleciona a busca')
    c.press('Backspace', at=round(c.L(5) + 0.2, 2), label='apaga a busca')
    c.hover(SEL("[role=dialog] :text-is('Ações Rápidas')"), 0.8, at=c.A(5, 'Ações', 0.7), label='destaque: Ações Rápidas')
    c.hover(SEL("[role=dialog] [cmdk-item]:has-text('Nova Compra')"), 0.6, at=c.A(5, 'compra,', 0.6), label='Nova Compra')
    c.hover(SEL("[role=dialog] [cmdk-item]:has-text('Nova Venda')"), 0.6, at=c.A(5, 'venda', 0.6), label='Nova Venda')
    c.hover(SEL("[role=dialog] [cmdk-item]:has-text('Abrir Caixa')"), 0.6, at=c.A(5, 'caixa,', 0.6), label='Abrir Caixa')
    c.mark(6)
    c.type(BUSCA, 'atalho', at=c.A(6, 'atalho,', 0.6), label='digita atalho', cps=8, clear=True, noClick=True)
    c.hover(SEL("[role=dialog] [cmdk-item]:has-text('Ver Atalhos de Teclado')"), 0.8, at=c.A(6, 'Ver', 0.8), label='Ver Atalhos de Teclado')
    c.press('Enter', at=c.A(6, 'lista', 0.5), label='Enter abre a lista de atalhos')
    c.waitfor(text='Atalhos Globais', timeout=10)
    c.mark(7)
    for rot, tecla in (('Compra', 'Shift+C'), ('Venda', 'Shift+V'), ('Caixa', 'Shift+X'), ('Pedidos', 'Shift+P'), ('Ver Estoque', 'Shift+E'), ('Configurações', 'Shift+S'), ('Agenda', 'Shift+A')):
        c.hover(SEL(f"{DLG} :text-is('{rot}')"), 0.5, at=c.A(7, tecla, 0.6), label=f'destaque: {rot} {tecla}')
    c.mark(8)
    c.press('Escape', at=round(c.L(8) - 0.3, 2), label='fecha a lista')
    c.press('Shift+X', at=c.A(8, 'Shift+X,', 0.2), label='Shift+X abre o Caixa')
    c.waitfor(text='Caixa', timeout=15)
    c.press('Shift+D', at=c.A(8, 'Shift+D,', 0.2), label='Shift+D volta ao Dashboard')
    c.waitfor(text='Olá, Rafael!', timeout=15)
    c.mark(9)
    c.mark(10)
    c.press('Shift+S', at=c.A(10, 'É', 0.3), label='Shift+S abre as Configurações')
    c.waitfor(text='Configurações', timeout=15)
    c.click(SEL("nav[aria-label='Navegação da seção'] button:has-text('Atalhos')"), at=c.A(10, 'Atalhos.', 0.9, nth=1), label='aba Atalhos')
    c.waitfor(text='Atalhos estão ativados', timeout=10)
    c.hover(SEL("main :text-is('Atalhos estão ativados')"), 1.2, at=c.A(10, 'Atalhos.', 0.0, nth=1), label='destaque: Atalhos estão ativados')
    c.fim()
    return c


def cap10():
    """A rotina diária (7 linhas): ilustração (L1), a faixa de lembretes do Dashboard (L2; a janela "Tarefas para hoje" não abre na gravação do 1.60.22), Histórico do Caixa pelo Ctrl+K (L3), Contas (L4),
    o painel de Filtros de Contas com "Próximos 7 dias" e "Até o fim do mês" (L5) e a Agenda de amanhã (L6)."""
    c = Cap(10, setup=setup_dash([{'do': 'goto', 'url': '/historico-caixa'}, {'do': 'waitFor', 'text': 'Caixas Fechados', 'timeout': 30}, AGUARDA]), start=(760, 300))
    c.mark(1)
    c.mark(2)
    c.click(LINK('Dashboard'), at=round(c.L(2) - 0.2, 2), label='abre o Dashboard de manhã', noScroll=True)
    c.waitfor(text='Olá, Rafael!', timeout=15)
    c.hover(SEL("main button:has-text('para hoje')"), 1.4, at=c.A(2, 'cotação', 0.8), label='ZOOM a faixa de lembretes: a cotação do cobre, 14:00')
    c.mark(3)
    c.press('Control+k', at=c.A(3, 'Primeiro,', 0.2), label='Ctrl+K')
    c.waitfor(selector='[role=dialog] input', timeout=10)
    c.type(SEL('[role=dialog] input'), 'histórico', at=c.A(3, 'Histórico', 1.2), label='digita histórico', cps=12, noClick=True)
    c.press('Enter', at=c.A(3, 'Caixa,', 0.4, nth=1), label='Enter abre o Histórico do Caixa')
    c.waitfor(text='Caixas Fechados', timeout=15)
    c.hover(COL('Saldo Final'), 1.0, at=c.A(3, 'saldo', 0.7), label='destaque: Saldo Final dos caixas de ontem')
    c.mark(4)
    c.click(BTN('Financeiro'), at=c.A(4, 'contas.', 0.9), label='menu Financeiro', unless=LINK('Contas a Pagar/Receber'))
    c.click(LINK('Contas a Pagar/Receber'), at=c.A(4, 'Contas', 0.6, nth=1), label='Contas a Pagar/Receber')
    c.waitfor(text='Vence em 7 dias', timeout=15)
    c.hover(CARTAO('Vencidas'), 0.8, at=c.A(4, 'Vencidas', 0.6), label='cartão Vencidas')
    c.hover(CARTAO('Vence em 7 dias'), 0.8, at=c.A(4, 'Vence', 0.6), label='cartão Vence em 7 dias')
    c.mark(5)
    c.click(SEL("main button:has-text('Filtros')"), at=c.A(5, 'filtros', 0.9), label='abre o painel de Filtros')
    c.waitfor(text='Vencimento (período)', timeout=10)
    c.ev("(()=>{const b=[...document.querySelectorAll('[role=dialog] button')].find(x=>x.textContent.trim()==='Até o fim do mês');if(!b)return 'SEM ALVO';b.scrollIntoView({block:'center',behavior:'smooth'});return 'ok'})()",
         at=round(c.L(5) + 0.8, 2), label='rola o painel até Vencimento (período)')
    c.hover(SEL("[role=dialog] button:text-is('Próximos 7 dias')"), 0.8, at=c.A(5, 'sete', 0.8), label='destaque: Próximos 7 dias')
    c.hover(SEL("[role=dialog] button:text-is('Até o fim do mês')"), 0.8, at=c.A(5, 'fim', 0.8), label='destaque: Até o fim do mês')
    c.press('Escape', at=round(c.L(6) - 1.0, 2), label='fecha o painel de Filtros')
    c.mark(6)
    c.press('Shift+A', at=c.A(6, 'Agenda,', 0.2), label='Shift+A abre a Agenda')
    c.waitfor(text='Gerencie suas tarefas e compromissos', timeout=15)
    c.click(DIA_AG('11'), at=c.A(6, 'amanhã:', 0.8), label='clica no dia 11')
    c.hover(SEL(CARD_TAREFA('Coleta na Auto Peças Vale Forte')), 1.2, at=c.A(6, 'coleta', 0.6), label='ZOOM Coleta na Auto Peças Vale Forte, 08:00')
    c.mark(7)
    c.fim()
    return c


def cap11():
    """A rotina semanal: ilustração (L1), Shift+E (Estoque, cobre e latinha, L2), Contas a Pagar/Receber na aba A Receber e a coluna Status (L4, L5).
    No 1.60.22 a aba A Receber mostra os cartões "Total a Receber" e "Total recebido" (só muda a imagem)."""
    c = Cap(11, setup=setup_dash(), start=(760, 300))
    c.mark(1)
    c.mark(2)
    c.press('Shift+E', at=c.A(2, 'Shift+E', 0.2), label='Shift+E abre o Estoque')
    c.waitfor(text='Estoque', timeout=15)
    c.hover(SEL("main tbody tr:has-text('Cobre mel')"), 0.8, at=c.A(2, 'cobre', 0.7), label='saldo do Cobre mel')
    c.mark(3)
    c.hover(SEL("main tbody tr:has-text('Alumínio latinha')"), 0.8, at=c.A(2, 'latinha.', 0.7), label='saldo do Alumínio latinha')
    c.mark(4)
    c.click(BTN('Financeiro'), at=c.A(4, 'Depois,', 0.9), label='menu Financeiro', unless=LINK('Contas a Pagar/Receber'))
    c.click(LINK('Contas a Pagar/Receber'), at=c.A(4, 'Contas', 0.6), label='Contas a Pagar/Receber')
    c.waitfor(text='Vence em 7 dias', timeout=15)
    c.click(ABA('A Receber'), at=c.A(4, 'aba', 0.7), label='aba A Receber')
    c.mark(5)
    c.hover(COL('Status'), 1.6, at=c.A(5, 'Vencida,', 0.7), label='destaque: coluna Status')
    c.fim()
    return c


def cap12():
    """A rotina mensal: ilustrações (L1 a L3), Shift+A, dezembro, dia 1 (L4) e a Nova Tarefa "Fechamento de novembro" (L5)."""
    c = Cap(12, setup=setup_dash(), start=(760, 300))
    c.mark(1)
    c.mark(2)
    c.mark(3)
    c.mark(4)
    c.press('Shift+A', at=c.A(4, 'Agenda,', 0.3), label='Shift+A abre a Agenda')
    c.waitfor(text='Gerencie suas tarefas e compromissos', timeout=15)
    c.click(MES_PROX, at=c.A(4, 'primeiro', 1.0), label='seta do próximo mês: dezembro')
    c.click(DIA_AG('1'), at=c.A(4, 'terça,', 0.8), label='clica no dia 1')
    c.mark(5)
    c.click(NOVA_TAREFA, at=c.A(5, 'Nova', 1.7), label='Nova Tarefa')
    c.waitfor(text='Título', timeout=10)
    c.type(SEL(f"{DLG} input[placeholder='Título']"), 'Fechamento de novembro', at=c.A(5, 'Fechamento', 0.3), label='digita o título', cps=14, noClick=True)
    colar(c, SEL(f"{DLG} textarea"), 'Conciliar o banco, conferir o DRE, mandar o pacote ao contador e ver MTR e CDF pendentes',
          c.A(5, 'quatro', 1.4), c.A(5, 'passos', 0.2), 'descrição com os quatro passos')
    c.click(SEL(f"{DLG} button:has(svg.lucide-clock)"), at=c.A(5, 'às', 1.2), label='campo Horário')
    c.click(HORAS('08'), at=c.A(5, 'oito', 0.9), label='hora 08')
    c.click(BTN('Concluir'), at=c.A(5, 'Lembrar', 1.6), label='Concluir o horário')
    c.hover(SEL(f"{DLG} div:has(> label:text-is('Lembrar no dia'))"), 0.8, at=c.A(5, 'Lembrar', 0.6), label='destaque: Lembrar no dia, ligado')
    c.click(SEL(f"{DLG} button:has-text('Salvar')"), at=c.A(5, 'ligado.', 0.0), label='Salvar')
    c.waitfor(text='Tarefa criada com sucesso', timeout=10)
    c.fim()
    return c


def cap13():
    """Recapitulando: a montagem da edição usa trechos dos capítulos; este passeio pelo Dashboard fica de reserva."""
    c = Cap(13, setup=setup_dash(), start=(760, 300))
    for i in range(1, 7):
        c.mark(i)
    c.hover(STAT(MARGEM), 0.6, at=c.A(1, 'Dashboard', 0.6), label='o Dashboard')
    c.hover(CONFIG, 0.6, at=c.A(2, 'painel', 0.6), label='Configurações do Dashboard')
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
