#!/usr/bin/env python3
"""T15 · Relatório Financeiro e DRE (EcoFlix, EcoSistema 1.59.154): gera rec/t15/cap00..cap11.json (roteiros do robô) a partir da fala
($TUT_HOME/t15/narracao/capNN.json: o estimado até a voz chegar; com a voz, o da voz, sem mudar nada aqui). O cap12 (Recapitulando) é
montagem das gravações dos outros capítulos: não tem robô.

Computador 1280x800, Rafael Nogueira (MASTER) na Recicla Vale Metais; FAKE_NOW 2026-11-10T08:30:00-03:00 em todos os capítulos (o mesmo
no Supabase falso e no robô). Rodar de qualquer pasta: `python3 -I rec/t15/gerar.py [NN ...]` (ANCORAS=1 lista as âncoras). Depois:
`node rec/record.mjs rec/t15/capNN.json --check`; ensaio: `python3 -I rec/t15/ensaio.py NN` + `--rapido`; gravação: sem `--rapido`.

LOGIN: todo capítulo é "anonymous" e o setup entra pela tela de login com "$TUT_USER"/"$TUT_SENHA" do ambiente (o Supabase falso aceita
qualquer senha; o valor nunca vai para arquivo nem log).

Cada passo é preso a uma palavra da fala: A(linha, 'palavra', folga) = início da palavra − folga (o custo do gesto até o cursor chegar:
clique ~0,6 s, 1º clique numa janela recém-aberta ~1,2 s, hover ~0,5 s; digitação sem clique na palavra − 0,05 s). A palavra casa
INTEIRA (sem acento e pontuação); repetida na linha pede `nth`. Marca Ln 0,9 s antes da linha; um passo que começa até 0,25 s antes da
marca a puxa para o início dele.

Estado de partida (rec/mundo/seeds-extra/t15/): o fim do T14 (`t14/inicio` + os `apos-capNN` do T14, na ordem) → `t15/inicio` (a cópia
da "Conta de energia" das 16:40 de 13/10, só no estado do T15) → `apos-cap01` (Frete de entrega e Máquinas e veículos, como o app grava)
→ `apos-cap02` (o centro de custo Produção) → `apos-cap10` (a cópia excluída: estado final, de onde o T21 parte).
Capítulos 4 a 11: o setup abre o relatório (aba de partida pelo localStorage "financial-report-tab") e escolhe "Mês passado" fora do vídeo.
"""
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TUT = os.path.normpath(os.path.join(HERE, '..', '..'))
AULA = 't15'
NARR = os.path.join(TUT, AULA, 'narracao')
FAKE_NOW = '2026-11-10T08:30:00-03:00'
VERSAO = '1.59.154'
HOJE = FAKE_NOW[:10]
NOMES = ['Abertura', 'O plano de contas', 'Centros de custo', 'O Relatório Financeiro', 'O Dashboard do mês', 'Fornecedores, clientes e ticket médio',
         'Lendo o DRE', 'Caixa ou competência', 'O patrimônio de hoje', 'Mês a mês', 'O Histórico', 'Exportar em Excel e PDF']
T14 = ['t14/inicio'] + [f't14/apos-cap{n:02d}' for n in (2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 14)]
_E = T14 + [f'{AULA}/inicio', f'{AULA}/apos-cap01', f'{AULA}/apos-cap02', f'{AULA}/apos-cap10']
_N = len(T14)
SEMENTE = {0: _E[:_N + 1], 1: _E[:_N + 1], 2: _E[:_N + 2], 11: _E[:_N + 4], **{n: _E[:_N + 3] for n in range(3, 11)}}
ABA = {4: 'dashboard', 5: 'dashboard', 6: 'dashboard', 7: 'dre', 8: 'dre', 9: 'dre', 10: 'dre', 11: 'historico'}

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
    import hashlib
    h = bytearray(hashlib.sha1(('domiflix-fake:' + chave).encode()).digest())
    h[6] = (h[6] & 0x0F) | 0x50
    h[8] = (h[8] & 0x3F) | 0x80
    x = h[:16].hex()
    return f'{x[:8]}-{x[8:12]}-{x[12:16]}-{x[16:20]}-{x[20:32]}'


def storage(n):
    uid = stable_id('user.rafael')
    d = {'app_version': VERSAO, 'notification_shown_version': VERSAO, 'pwa-install-dismissed': 'true', 'theme': 'light',
         f'daily-tasks-reminder-last-shown-{uid}': HOJE, 'initial-preferences-set': 'true'}
    if n in ABA:
        d['financial-report-tab'] = ABA[n]
    return d


# ---------------------------------------------------------------- observador de avisos de erro (aceite: tem de sair vazio)
OBS = ("(()=>{window.__avisos=[];const re=/N[ãa]o foi poss[ií]vel|Erro ao|Tente novamente|Algo deu errado|Falha ao|Something went wrong|indispon[ií]vel/i;"
       "const chk=(t)=>{t=(t||'').trim();const m=t&&t.match(new RegExp('[^]{0,40}('+re.source+')[^]{0,40}','i'));"
       "if(m&&!/fica indispon/i.test(m[0])&&window.__avisos.length<10)window.__avisos.push(m[0].replace(/[\\n\\r\\t ]+/g,' '))};new MutationObserver(ms=>{for(const m of ms){"
       "m.addedNodes.forEach(n=>chk(n.textContent));if(m.type==='characterData')chk(m.target.textContent)}}).observe(document.body,"
       "{childList:true,subtree:true,characterData:true});chk(document.body.innerText);"
       "setInterval(()=>{document.querySelectorAll('[data-sonner-toast][data-type=error]').forEach(t=>{const s='TOAST DE ERRO: '+t.textContent.trim().slice(0,90);"
       "if(!window.__avisos.includes(s)&&window.__avisos.length<10)window.__avisos.push(s)})},300);return 1})()")


class Cap:
    def __init__(s, n, setup, pace=0.5, cps=40, start=(760, 470)):
        s.n = n
        s.words, s.linhas, s.dur, s.estimado = carregar_voz(n)
        s.steps, s.pending, s.anchors = [], [], []
        s.pace, s.cps, s.start = pace, cps, start
        s.setup = list(setup) + [{'do': 'eval', 'js': OBS}]

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
        return {
            'name': f'{AULA}-cap{s.n:02d}',
            'title': f'T15 · Cap. {s.n} · {NOMES[s.n]} (narração{est} {str(round(s.dur, 1)).replace(".", ",")} s; marcas L1..L{len(s.linhas)} = início de cada '
                     f'linha do roteiro; FAKE_NOW {FAKE_NOW}; logado como Rafael Nogueira)',
            'seed': f'{AULA}-cap{s.n:02d}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
            'start': {'x': s.start[0], 'y': s.start[1]},
            'anonymous': True, 'storage': storage(s.n),
            'seedExtra': list(SEMENTE[s.n]),
            'prewarm': ['/login'], 'setup': s.setup, 'steps': s.steps,
        }


# ---------------------------------------------------------------- alvos
MAIN = 'main'
DLG = '[role=dialog]'
ALERTA = '[role=alertdialog]'
POP = '[data-radix-popper-content-wrapper]'
BTN = lambda n, within=None, **kw: {'role': 'button', 'name': n, 'exact': True, **({'within': within} if within else {}), **kw}
BTNX = lambda n, within=None, **kw: {'role': 'button', 'name': n, **({'within': within} if within else {}), **kw}
TXT = lambda t, within=None, **kw: {'text': t, 'exact': True, **({'within': within} if within else {}), **kw}
TXTP = lambda t, within=None, **kw: {'text': t, **({'within': within} if within else {}), **kw}
SEL = lambda s, **kw: {'selector': s, **kw}
ITEM = lambda n, **kw: {'role': 'menuitem', 'name': n, **kw}
OPT = lambda n, **kw: {'role': 'option', 'name': n, **kw}
COMBO = lambda n, **kw: {'role': 'combobox', 'name': n, **kw}
AGUARDA = {'do': 'waitFor', 'idle': True}


def login():
    return [{'do': 'waitFor', 'target': {'label': 'E-mail'}, 'timeout': 30},
            {'do': 'type', 'target': {'label': 'E-mail'}, 'text': '$TUT_USER', 'cps': 40},
            {'do': 'type', 'target': {'label': 'Senha', 'exact': True}, 'text': '$TUT_SENHA', 'cps': 40},
            {'do': 'click', 'target': BTN('Entrar')},
            {'do': 'waitFor', 'text': 'Olá, Rafael!', 'timeout': 30}, AGUARDA]


# ---------------------------------------------------------------- rolagem roteirizada (eval: o cursor não se mexe)
ACHA_ROLAGEM = ("const rolagem=(el)=>{let c=el&&el.parentElement;while(c&&c!==document.body){const s=getComputedStyle(c);"
                "if(/(auto|scroll)/.test(s.overflowY)&&c.scrollHeight>c.clientHeight+4)return c;c=c.parentElement;}"
                "return [...document.querySelectorAll('main')].find(e=>/(auto|scroll)/.test(getComputedStyle(e).overflowY)&&e.scrollHeight>e.clientHeight+4)||document.scrollingElement};")
SUAVE = ("await new Promise(res=>{const t0=performance.now();const f=t=>{const p=Math.min(1,(t-t0)/DUR),e=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;"
         "c.scrollTop=DESTINO;p<1?requestAnimationFrame(f):res()};requestAnimationFrame(f)});")
FOLHA = "[...document.querySelectorAll('main *')].find(e=>e.children.length===0&&e.textContent.trim()===%s&&e.getClientRects().length)"


def js_rola_texto(texto, y=300, dur_ms=800, nth=0):
    """rolagem suave do contêiner que rola a folha do DOM cujo texto é `texto` até ela ficar em y px CSS; devolve o topo final"""
    achar = FOLHA % json.dumps(texto) if not nth else ("[...document.querySelectorAll('main *')].filter(e=>e.children.length===0&&e.textContent.trim()===%s&&e.getClientRects().length)[%d]" % (json.dumps(texto), nth))
    return ("(async()=>{" + ACHA_ROLAGEM + "const el=" + achar + ";if(!el)return 'SEM ALVO';const c=rolagem(el);if(!c)return 'SEM ROLAGEM';"
            f"const dy=Math.round(el.getBoundingClientRect().top-{int(y)});if(Math.abs(dy)<3)return 'ok';const y0=c.scrollTop;"
            + (SUAVE.replace('DUR', str(int(dur_ms))).replace('DESTINO', 'y0+dy*e') if dur_ms else "c.scrollTop=y0+dy;")
            + "return Math.round(el.getBoundingClientRect().top)})()")


def js_topo(dur_ms=600):
    """sobe a página (o contêiner que rola o cabeçalho do relatório) até o topo"""
    return ("(async()=>{" + ACHA_ROLAGEM + "const el=document.querySelector('main h1')||document.querySelector('main *');const c=rolagem(el);if(!c)return 'SEM ROLAGEM';"
            "const y0=c.scrollTop;if(y0<3)return 'ok';const dy=-y0;"
            + (SUAVE.replace('DUR', str(int(dur_ms))).replace('DESTINO', 'y0+dy*e') if dur_ms else "c.scrollTop=0;") + "return 'topo'})()")


def rola_setup(texto, y=300):
    """no setup (fora do vídeo): a linha `texto` em y, sem animação"""
    return {'do': 'eval', 'js': js_rola_texto(texto, y, 0)}


def setup_relatorio(marca, extra=()):
    """login, Relatório Financeiro (aba de partida pelo localStorage) e "Mês passado", fora do vídeo; `marca` = texto que só aparece com outubro"""
    return login() + [{'do': 'goto', 'url': '/relatorio-financeiro'}, {'do': 'waitFor', 'text': 'Visão completa das finanças do seu negócio', 'timeout': 30}, AGUARDA,
                      {'do': 'click', 'target': COMBO('Este mês')}, {'do': 'click', 'target': OPT('Mês passado')},
                      {'do': 'waitFor', 'text': marca, 'timeout': 20}, AGUARDA] + list(extra)
