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
PROPRIO = "(e=>e.children.length===0?e.textContent.trim():[...e.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent).join('').trim())"
FOLHA = "[...document.querySelectorAll('main *')].find(e=>e.getClientRects().length&&" + PROPRIO + "(e)===%s)"


def js_rola_texto(texto, y=300, dur_ms=800, nth=0):
    """rolagem suave do contêiner que rola a folha do DOM cujo texto é `texto` até ela ficar em y px CSS; devolve o topo final"""
    achar = FOLHA % json.dumps(texto) if not nth else ("[...document.querySelectorAll('main *')].filter(e=>e.getClientRects().length&&" + PROPRIO + "(e)===%s).at(%d)" % (json.dumps(texto), nth))
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
                      {'do': 'click', 'target': PERIODO('Este mês')}, {'do': 'click', 'target': OPT('Mês passado')},
                      {'do': 'waitFor', 'text': marca, 'timeout': 20}, AGUARDA] + list(extra)


FOLHA_CONTEM = "[...document.querySelectorAll('main *')].find(e=>e.getClientRects().length&&" + PROPRIO + "(e).includes(%s))"


def js_rola_contem(trecho, y=300, dur_ms=800):
    """como js_rola_texto, mas a folha só CONTÉM o trecho (avisos longos)"""
    return ("(async()=>{" + ACHA_ROLAGEM + "const el=" + (FOLHA_CONTEM % json.dumps(trecho)) + ";if(!el)return 'SEM ALVO';const c=rolagem(el);if(!c)return 'SEM ROLAGEM';"
            f"const dy=Math.round(el.getBoundingClientRect().top-{int(y)});if(Math.abs(dy)<3)return 'ok';const y0=c.scrollTop;"
            + (SUAVE.replace('DUR', str(int(dur_ms))).replace('DESTINO', 'y0+dy*e') if dur_ms else "c.scrollTop=y0+dy;")
            + "return Math.round(el.getBoundingClientRect().top)})()")


def js_clica_texto(texto, escopo='main', tag='button'):
    """clique por eval (sem cursor) no `tag` cujo texto visível é `texto` (ex.: trocar o regime enquanto a câmera fica na linha)"""
    return ("(()=>{const b=[...document.querySelectorAll(%s)].find(e=>e.offsetParent&&e.innerText.trim()===%s);if(!b)return 'SEM ALVO';b.click();return 'ok'})()"
            % (json.dumps(f'{escopo} {tag}'), json.dumps(texto)))


def js_colar(sel, texto):
    """escreve o texto de uma vez no campo já focado (execCommand insertText: o React recebe o input); devolve o valor"""
    return ("(()=>{const el=document.querySelector(%s);if(!el)return 'SEM ALVO';el.focus();document.execCommand('insertText',false,%s);return el.value})()"
            % (json.dumps(sel), json.dumps(texto, ensure_ascii=False)))


ANIMA = "(()=>{const a=document.getAnimations().filter(x=>x.currentTime<0);a.forEach(x=>x.startTime=document.timeline.currentTime);return a.length})()"
ABA_R = lambda v: SEL(f'#tab-btn-{v}')          # abas do Relatório (SettingsSidebarLayout): dashboard, dre, dfc, centros-custo, historico
ABA_C = lambda v: SEL(f'#tab-btn-{v}')          # Categorias Financeiras: categorias, centros-de-custo, grupos-dre


def js_rola_dlg(texto, y=300, dur_ms=600):
    """rolagem (suave) DENTRO da janela aberta até a folha `texto` ficar em y px"""
    return ("(async()=>{" + ACHA_ROLAGEM + "const el=[...document.querySelectorAll('[role=dialog] *')].find(e=>e.getClientRects().length&&" + PROPRIO + "(e)===%s);"
            "if(!el)return 'SEM ALVO';const c=rolagem(el);if(!c)return 'SEM ROLAGEM';" % json.dumps(texto)
            + f"const dy=Math.round(el.getBoundingClientRect().top-{int(y)});if(Math.abs(dy)<3)return 'ok';const y0=c.scrollTop;"
            + (SUAVE.replace('DUR', str(int(dur_ms))).replace('DESTINO', 'y0+dy*e') if dur_ms else "c.scrollTop=y0+dy;")
            + "return Math.round(el.getBoundingClientRect().top)})()")


COMBO_DLG = lambda t: SEL(f'[role=dialog] button[role=combobox]:has-text("{t}")')
PERIODO = lambda t: SEL(f'main button[role=combobox]:has-text("{t}")')
LINK = lambda n: {'role': 'link', 'name': n}
CARD = lambda nome: BTN(nome, within=MAIN)            # o nome do cartão da categoria é um botão
PONTOS = lambda nome: BTN(f'Ações de {nome}')


def menu_financeiro(c, at, link, label):
    c.click(BTN('Financeiro'), at=at, label='menu Financeiro', unless=LINK(link))


# ---------------------------------------------------------------- capítulos
def cap00():
    c = Cap(0, login(), pace=0.6)
    c.mark(1)
    c.mark(2)
    c.mark(3)
    c.hover(BTN('Financeiro'), seconds=0.8, at=c.A(3, 'categorias', 2.4), label='menu Financeiro (o caminho da aula)')
    c.mark(4)
    c.rolar(0, at=c.A(4, 'tutorial', 0.6), ponto=(760, 470), duration=0.6)
    c.fim()
    return c


def cap01():
    # folgas = o tempo medido até o gesto agir (gravação de 11/11 18:40, sem render ao lado): hover 0,6 a 0,9 s, clique 0,5 a 1,4 s
    c = Cap(1, login(), pace=0.5)
    c.mark(1)
    menu_financeiro(c, c.A(1, 'Financeiro', 1.4), 'Categorias Financeiras', 'menu Financeiro')
    c.click(LINK('Categorias Financeiras'), at=c.A(1, 'Categorias', 1.0, nth=1), label='Categorias Financeiras')
    c.mark(2)
    c.flush(1e9)
    c.waitfor(text='Gerencie as categorias de receitas e despesas', timeout=15)
    c.hover(CARD('Aluguel de caçamba'), seconds=0.6, at=c.A(2, 'aluguel', 0.8), label='Aluguel de caçamba (receita)')
    c.ev(js_rola_texto('Categorias de despesa', 120, 700), at=c.A(2, 'Embaixo', 0.3), label='desce para as despesas')
    c.hover(CARD('Folha salarial'), seconds=0.15, at=c.A(2, 'folha', 0.6), label='Folha salarial')
    c.hover(CARD('Combustível'), seconds=0.3, at=c.A(2, 'combustível', 0.75), label='Combustível')
    c.mark(3)
    c.mark(4)
    c.hover(TXTP('Impostos e deduções', within=MAIN), seconds=0.3, at=c.A(4, 'separadas', 0.75), label='divisória Impostos e deduções')
    c.hover(TXTP('Custos adicionais', within=MAIN), seconds=0.3, at=c.A(4, 'lugar', 0.85), label='divisória Custos adicionais')
    c.hover(TXTP('Despesas operacionais (OPEX)', within=MAIN), seconds=0.6, at=c.A(4, 'DRE', 0.7), label='divisória Despesas operacionais (OPEX)')
    c.mark(5)
    c.hover(CARD('Frete'), seconds=0.3, at=c.L(5) - 1.1, label='cartão Frete (frete de compra)')
    c.click(PONTOS('Frete'), at=c.A(5, 'criar', 0.9), label='Ações de Frete')
    c.click(ITEM('Adicionar subcategoria'), at=c.A(5, 'subcategoria', 0.4), label='Adicionar subcategoria')
    c.waitfor(text='Nova subcategoria', timeout=8)
    c.mark(6)
    c.type(SEL('#financial-category-name'), 'Frete de entrega', at=c.A(5, 'entrega', 0.05), label='Nome: Frete de entrega', noClick=True)
    c.hover(COMBO_DLG('Frete'), seconds=0.4, at=c.A(6, 'tudo', 0.9), label='Categoria principal: Frete')
    c.hover(COMBO_DLG('Custos adicionais'), seconds=0.6, at=c.A(6, 'lugar', 1.3), label='Onde aparece no DRE: Custos adicionais (do pai)')
    c.click(COMBO_DLG('Custos adicionais'), at=c.A(6, 'escolho', 0.5), label='abre Onde aparece no DRE')
    c.click(OPT('Despesas operacionais (OPEX)'), at=c.A(6, 'Despesas', 0.8), label='Despesas operacionais (OPEX)')
    c.hover(TXT('Prévia no DRE padrão', within=DLG), seconds=1.0, at=c.A(6, 'prévia', 0.4), label='Prévia no DRE padrão (ZOOM)')
    c.mark(7)
    c.click(BTN('Criar categoria'), at=c.L(7) - 0.2, label='Criar categoria')
    c.waitfor(text='Categoria criada', timeout=8)
    c.hover(TXTP('Subcategorias podem pertencer a outro grupo DRE', within=MAIN), seconds=0.8, at=c.A(7, 'lançamentos', 0.7), label='selo e nota do Frete de entrega (ZOOM)')
    c.confere('main', ['Frete de entrega', 'Subcategorias podem pertencer a outro grupo DRE'], 'subcategoria com o selo')
    c.hover(TXTP('Subcategorias podem pertencer a outro grupo DRE', within=MAIN), seconds=0.6, at=c.A(7, 'selo', 1.0), label='a nota do selo')
    c.mark(8)
    c.ev(js_rola_texto('Categorias de despesa', 170, 500), at=c.L(8) - 0.9, label='sobe até Categorias de despesa')
    c.click(BTN('Nova', nth=1), at=c.A(8, 'categoria', 0.8), label='Nova (despesa)')
    c.waitfor(text='Nova categoria', timeout=8)
    c.type(SEL('#financial-category-name'), 'Máquinas e veículos', at=c.A(8, 'cuidado', 0.0), label='Nome: Máquinas e veículos', noClick=True)
    c.mark(9)
    c.mark(10)
    c.mark(11)
    c.mark(12)
    c.click(COMBO_DLG('Despesas operacionais'), at=c.A(12, 'vai', 0.6), label='abre Onde aparece no DRE')
    c.click(OPT('Não compõe o DRE'), at=c.A(12, 'Não', 0.7), label='Não compõe o DRE')
    c.hover(TXT('Prévia no DRE padrão', within=DLG), seconds=0.8, at=c.A(12, 'resultado', 0.6), label='prévia: informativo, não altera o resultado (ZOOM)')
    c.ev(js_rola_dlg('Grupo no Fluxo de Caixa (DFC)', 330, 500), at=c.A(12, 'fluxo', 1.0), label='desce a janela até o DFC')
    c.click(COMBO_DLG('Atividades operacionais'), at=c.A(12, 'acompanha', 1.1), label='abre Grupo no Fluxo de Caixa (DFC)')
    c.click(OPT('Atividades de investimento'), at=c.A(12, 'Atividades', 0.65), label='Atividades de investimento')
    c.mark(13)
    c.click(BTN('Criar categoria'), at=c.L(13) - 1.1, label='Criar categoria')
    c.waitfor(text='Categoria criada', timeout=8)
    c.waitfor(target=CARD('Máquinas e veículos'), timeout=6)
    c.ev(js_rola_texto('Máquinas e veículos', 420, 700), at=c.A(13, 'registra', 0.0), label='desce até Não compõe o DRE')
    c.hover(CARD('Máquinas e veículos'), seconds=0.8, at=c.A(13, 'compra', 0.0), label='Máquinas e veículos em Não compõe o DRE')
    c.confere('main', ['Não compõe o DRE', 'Máquinas e veículos'], 'Máquinas e veículos na divisória Não compõe o DRE')
    c.fim()
    return c


def cap02():
    c = Cap(2, login() + [{'do': 'goto', 'url': '/categorias-financeiras'}, {'do': 'waitFor', 'text': 'Gerencie as categorias de receitas e despesas', 'timeout': 20}, AGUARDA], pace=0.5)
    c.mark(1)
    c.click(ABA_C('centros-de-custo'), at=c.A(1, 'centro', 0.6), label='Centros de custo')
    c.waitfor(text='Novo centro de custo', timeout=10)
    c.mark(2)
    c.mark(3)
    c.click(BTN('Novo centro de custo'), at=c.L(3) - 0.2, label='Novo centro de custo')
    c.waitfor(text='Defina um nome e uma cor para identificar o setor nos lançamentos.', timeout=8)
    c.type(SEL('#cost-center-name'), 'Produção', at=c.A(3, 'produção', 0.3), label='Nome: Produção')
    c.click(BTN('Cor #8B5CF6'), at=c.A(3, 'cor', 0.6), label='Cor #8B5CF6 (roxo)')
    c.click(SEL('#cost-center-description'), at=c.A(3, 'descrição', 0.6), label='Descrição')
    c.ev(js_colar('#cost-center-description', 'Prensa de latinha e papelão'), label='Descrição: Prensa de latinha e papelão')
    c.mark(4)
    c.hover(SEL('#cost-center-active'), seconds=1.0, at=c.A(4, 'desligar', 0.5), label='Ativo ligado (ZOOM)')
    c.mark(5)
    c.click(BTN('Salvar'), at=c.A(5, 'Salvei', 0.7), label='Salvar')
    c.waitfor(text='Centro de custo criado', timeout=8)
    c.hover(TXT('Produção', within=MAIN), seconds=0.8, at=c.A(5, 'Centro', 0.5), label='Produção na lista')
    c.confere('main', ['Produção', 'Prensa de latinha e papelão'], 'Produção criado')
    c.fim()
    return c


def cap03():
    c = Cap(3, login(), pace=0.5)
    c.mark(1)
    menu_financeiro(c, 0.3, 'Relatório Financeiro', 'menu Financeiro')
    c.click(LINK('Relatório Financeiro'), at=c.A(1, 'Relatório', 1.8, nth=1), label='Relatório Financeiro')
    c.mark(2)
    c.flush(1e9)
    c.waitfor(text='Visão completa das finanças do seu negócio', timeout=15)
    c.hover(PERIODO('Este mês'), seconds=0.5, at=c.A(2, 'período', 0.5), label='filtro de período: Este mês')
    c.click(PERIODO('Este mês'), at=c.A(2, 'novembro', 0.0), label='abre o filtro de período')
    c.click(OPT('Mês passado'), at=c.A(2, 'Mês', 1.0, nth=1), label='Mês passado')
    c.mark(3)
    c.hover(PERIODO('Mês passado'), seconds=0.5, at=c.A(3, 'período', 1.0), label='filtro em Mês passado')
    c.mark(4)
    c.hover(ABA_R('dashboard'), seconds=0.3, at=c.A(4, 'Dashboard', 0.5), label='aba Dashboard')
    c.hover(ABA_R('dre'), seconds=0.3, at=c.A(4, 'DRE', 0.5), label='aba DRE')
    c.hover(ABA_R('centros-custo'), seconds=0.3, at=c.A(4, 'Centros', 0.5), label='aba Centros de Custo')
    c.hover(ABA_R('historico'), seconds=0.4, at=c.A(4, 'Histórico', 0.5), label='aba Histórico')
    c.mark(5)
    c.click(ABA_R('centros-custo'), at=c.A(5, 'Centros', 0.6), label='Centros de Custo')
    c.waitfor(text='Ranking dos centros de custo', timeout=10)
    c.ev(js_rola_texto('Ranking dos centros de custo', 170, 900), at=c.A(5, 'outubro', 0.3), label='desce até o Ranking dos centros de custo')
    c.hover(TXT('Pátio', within=MAIN, nth=-1), seconds=0.5, at=c.A(5, 'pátio', 0.5), label='Pátio no ranking')
    c.hover(TXT('Coleta', within=MAIN, nth=-1), seconds=0.5, at=c.A(5, 'coleta', 0.5), label='Coleta no ranking')
    c.mark(6)
    c.ev(js_rola_contem('Esta visão considera receitas', 420, 700), at=c.L(6) - 0.9, label='desce até o aviso azul')
    c.hover(TXTP('Esta visão considera receitas', within=MAIN), seconds=1.0, at=c.A(6, 'aviso', 0.5), label='aviso azul dos centros de custo (ZOOM)')
    c.mark(7)
    c.ev(js_topo(800), at=c.A(7, 'dica', 0.4), label='sobe ao cabeçalho')
    c.hover(SEL('main h1'), seconds=0.8, at=c.A(7, 'permissão', 0.5), label='cabeçalho do Relatório Financeiro')
    c.fim()
    return c


def js_tab(nome):
    """troca a aba Radix (Regime de Caixa/Competência) por eval, sem cursor: o gatilho reage ao mousedown"""
    return ("(()=>{const b=[...document.querySelectorAll('main [role=tab]')].find(e=>e.offsetParent&&e.innerText.replace(/\\s+/g,' ').trim()===%s);if(!b)return 'SEM ALVO';"
            "for(const t of ['pointerdown','mousedown','pointerup','mouseup','click'])b.dispatchEvent(new (t.startsWith('pointer')?PointerEvent:MouseEvent)(t,{bubbles:true,cancelable:true,button:0}));"
            "return b.getAttribute('aria-selected')})()" % json.dumps(nome))


REGIME = lambda n: {'role': 'tab', 'name': n}
GRUPO = lambda cod: SEL(f'main button:has(span:text-is("{cod}"))')   # 04.01 custos, 06.01 despesas operacionais
LINHA = lambda t, nth=0: TXT(t, within=MAIN, nth=nth)


def cap04():
    c = Cap(4, setup_relatorio('Superávit'), pace=0.5)
    c.mark(1)
    c.hover(TXT('Resultado do Período', within=MAIN), seconds=0.5, at=c.A(1, 'Resultado', 0.8), label='Resultado do Período')
    c.hover(LINHA('R$ 6.500,00'), seconds=1.5, at=c.A(1, 'seis', 0.9), label='R$ 6.500,00 e Superávit (ZOOM)')
    c.confere('main', ['R$ 6.500,00', 'Superávit'], 'banner de outubro')
    c.mark(2)
    c.hover(LINHA('Superávit'), seconds=0.8, at=c.A(2, 'vermelho', 0.8), label='o banner inteiro')
    c.mark(3)
    c.ev(js_rola_texto('Despesas por Categoria', 110, 900), at=c.L(3) - 0.9, label='desce até Despesas por Categoria')
    c.hover(LINHA('Folha salarial'), seconds=0.8, at=c.A(3, 'folha', 0.8), label='Folha salarial R$ 19.800,00')
    c.confere('main', ['Total: R$ 40.705,90', 'R$ 19.800,00'], 'despesas por categoria de outubro')
    c.mark(4)
    c.hover(LINHA('Energia elétrica'), seconds=1.2, at=c.A(4, 'energia', 0.8), label='Energia elétrica R$ 7.700,00 (ZOOM)')
    c.confere('main', ['R$ 7.700,00'], 'energia em dobro')
    c.mark(5)
    c.hover(TXT('Receitas por Categoria', within=MAIN), seconds=0.6, at=c.A(5, 'receitas', 0.8), label='Receitas por Categoria')
    c.hover(LINHA('Aluguel de caçamba'), seconds=1.0, at=c.A(5, 'aluguel', 0.8), label='Aluguel de caçamba R$ 2.800,00')
    c.confere('main', ['Total: R$ 2.800,00'], 'receitas por categoria de outubro')
    c.mark(6)
    c.hover(TXT('Despesas por Categoria', within=MAIN), seconds=0.6, at=c.A(6, 'gráficos', 0.8), label='os dois gráficos')
    c.fim()
    return c


def cap05():
    c = Cap(5, setup_relatorio('Superávit'), pace=0.5)
    c.mark(1)
    c.ev(js_rola_texto('Ticket Médio Compra', 150, 1200), at=c.A(1, 'embaixo', 0.3), label='desce até os tickets médios')
    c.hover(LINHA('Ticket Médio Compra'), seconds=0.3, at=c.A(1, 'ticket', 2.0), label='Ticket Médio Compra')
    c.mark(2)
    c.mark(3)
    c.hover(LINHA('Ticket Médio Compra'), seconds=0.8, at=c.A(3, 'lotes', 0.8), label='Ticket Médio Compra (lotes)')
    c.mark(4)
    c.hover(LINHA('Top Fornecedores'), seconds=0.4, at=c.A(4, 'Fornecedores', 0.8), label='Top Fornecedores')
    c.hover(LINHA('Depósito Irmãos Siqueira'), seconds=0.8, at=c.A(4, 'Depósito', 0.8), label='1º fornecedor: Depósito Irmãos Siqueira')
    c.mark(5)
    c.hover(LINHA('Fundição Bandeira do Vale'), seconds=0.8, at=c.A(5, 'Fundição', 0.9), label='1º cliente em R$: Fundição Bandeira do Vale')
    c.mark(6)
    c.click(LINHA('Kg', nth=1), at=c.A(6, 'quilos', 0.7), label='Kg no Top Clientes')
    c.hover(LINHA('Aços Quiririm Ltda'), seconds=1.0, at=c.A(6, 'Aços', 0.9), label='1º cliente em kg: Aços Quiririm Ltda (ZOOM)')
    c.mark(7)
    c.hover(LINHA('Ver todos', nth=1), seconds=0.6, at=c.A(7, 'Ver', 0.8), label='Ver todos (Top Clientes)')
    c.mark(8)
    c.ev(js_rola_texto('Materiais + Comprados', 150, 900), at=c.L(8) - 0.9, label='desce até os materiais')
    c.hover(LINHA('Ferro pesado'), seconds=1.2, at=c.A(8, 'ferro', 0.8), label='Ferro pesado 50.000 kg R$ 47.500,00 (ZOOM)')
    c.confere('main', ['Ferro pesado', '50.000 kg', 'R$ 47.500,00'], 'ferro pesado comprado em outubro')
    c.mark(9)
    c.hover(LINHA('Cobre mel', nth=1), seconds=0.8, at=c.A(9, 'vendidos', 0.9), label='1º dos mais vendidos: Cobre mel')
    c.fim()
    return c


def cap06():
    c = Cap(6, setup_relatorio('Superávit'), pace=0.5)
    c.mark(1)
    c.click(ABA_R('dre'), at=c.A(1, 'DRE', 0.6), label='aba DRE')
    c.waitfor(text='Demonstrativo Financeiro (DRE)', timeout=10)
    c.mark(2)
    c.mark(3)
    c.mark(4)
    c.ev(js_rola_texto('(+) Receita Bruta', 110, 1500), at=c.L(4) - 0.9, label='desce pela tabela do DRE')
    c.mark(5)
    c.click(GRUPO('06.01'), at=c.A(5, 'grupo', 0.6), label='abre o grupo Despesas operacionais')
    c.ev(js_rola_texto('06.01', 230, 700), label='as categorias do grupo na tela')
    c.mark(6)
    c.hover(LINHA('Folha salarial'), seconds=1.0, at=c.A(6, 'pesa', 0.8), label='% da receita da Folha salarial (ZOOM)')
    c.mark(7)
    c.ev(js_rola_texto('= Resultado do Período', 420, 900), at=c.L(7) - 0.9, label='desce até o resultado')
    c.hover(LINHA('R$ 6.500,00', nth=-1), seconds=1.2, at=c.A(7, 'seis', 0.9), label='08 = Resultado do Período R$ 6.500,00 (ZOOM)')
    c.confere('main', ['= Resultado do Período', 'R$ 6.500,00'], 'resultado de outubro em competência')
    c.mark(8)
    c.hover(LINHA('(-) Despesas Operacionais'), seconds=0.8, at=c.A(8, 'aparece', 0.5), label='a tabela')
    c.fim()
    return c


def cap07():
    c = Cap(7, setup_relatorio('Demonstrativo Financeiro (DRE)'), pace=0.5)
    c.mark(1)
    c.hover(REGIME('Regime de Caixa'), seconds=0.4, at=c.A(1, 'Caixa', 0.5), label='Regime de Caixa')
    c.hover(REGIME('Regime de Competência'), seconds=0.6, at=c.A(1, 'Competência', 0.5), label='Regime de Competência (marcado)')
    c.mark(2)
    c.hover(REGIME('Regime de Caixa'), seconds=1.0, at=c.A(2, 'caixa', 0.5), label='dica do Regime de Caixa (ZOOM)')
    c.mark(3)
    # a dica do Caixa aberta deixa o ponteiro "em trânsito" (Radix): sem sair dela antes, a dica da Competência não abre (11/11)
    c.rolar(0, at=c.L(3) - 0.9, ponto=(1000, 250), duration=0.4)
    c.hover(REGIME('Regime de Competência'), seconds=1.0, at=c.A(3, 'competência', -0.1), label='dica do Regime de Competência (ZOOM)')
    c.mark(4)
    c.rolar(0, at=c.L(4) - 0.3, ponto=(1150, 200), duration=0.6)   # cursor fora do gráfico da Evolução Mensal (dica do Recharts)
    c.mark(5)
    c.mark(6)
    c.mark(7)
    c.mark(8)
    c.mark(9)
    c.ev(js_rola_texto('= Resultado do Período', 420, 900), at=c.L(9) - 0.9, label='desce até o resultado')
    c.hover(LINHA('R$ 6.500,00', nth=-1), seconds=1.0, at=c.A(9, 'seis', 0.9), label='competência: R$ 6.500,00 (ZOOM)')
    c.mark(10)
    c.ev(js_rola_texto('Demonstrativo Financeiro (DRE)', 110, 600), at=c.L(10) - 0.9, label='sobe ao cabeçalho do DRE')
    c.click(REGIME('Regime de Caixa'), at=c.A(10, 'Regime', 0.6), label='Regime de Caixa')
    c.waitfor(text='O detalhamento por centro de custo', timeout=10)
    c.ev(js_rola_texto('= Resultado do Período', 420, 900), at=c.A(10, 'prejuízo', 0.9), label='desce até o resultado em caixa')
    c.hover(LINHA('-R$ 31.500,00'), seconds=1.0, at=c.A(10, 'trinta', 0.5), label='caixa: -R$ 31.500,00 (ZOOM)')
    c.confere('main', ['-R$ 31.500,00'], 'resultado de outubro em caixa')
    c.mark(11)
    c.ev(js_rola_texto('04.01', 330, 800), at=c.L(11) - 0.9, label='sobe até 04 Custos Operacionais')
    c.click(GRUPO('04.01'), at=c.A(11, 'linha', 0.6), label='abre o grupo do custo')
    c.hover(LINHA('CMV / Compras de materiais'), seconds=1.0, at=c.A(11, 'Compras', 0.5), label='CMV / Compras de materiais (ZOOM)')
    c.confere('main', ['CMV / Compras de materiais', 'R$ 256.860,00'], 'CMV em caixa')
    c.ev(js_tab('Regime de Competência'), at=c.A(11, 'competência', 0.2), label='troca para competência (sem cursor)')
    c.confere('main', ['R$ 218.860,00'], 'CMV em competência')
    c.ev(js_tab('Regime de Caixa'), at=c.A(11, 'caixa', 0.2), label='troca para caixa (sem cursor)')
    c.confere('main', ['R$ 256.860,00'], 'CMV em caixa de novo')
    c.mark(12)
    c.hover(LINHA('CMV / Compras de materiais'), seconds=1.0, at=c.A(12, 'diferença', 0.5), label='a linha do CMV (mesmo zoom)')
    c.mark(13)
    c.ev(js_rola_texto('(+) Receita Bruta', 150, 900), at=c.L(13) - 0.9, label='a tabela inteira')
    c.hover(LINHA('(-) Custos Operacionais'), seconds=0.8, at=c.A(13, 'normal', 0.5), label='a tabela inteira')
    c.fim()
    return c


def cap08():
    c = Cap(8, setup_relatorio('Demonstrativo Financeiro (DRE)'), pace=0.5)
    c.mark(1)
    c.ev(js_rola_texto('Patrimônio Operacional Atual', 300, 1200), at=0.3, label='desce até o patrimônio')
    c.click(LINHA('Patrimônio Operacional Atual'), at=c.A(1, 'Clico', 0.6), label='abre Patrimônio Operacional Atual')
    c.waitfor(text='Saldo em Caixa (Dinheiro)', timeout=8)
    c.ev(js_rola_texto('Patrimônio Operacional Atual', 150, 700), label='o bloco inteiro na tela')
    c.mark(2)
    c.hover(LINHA('Saldo em Caixa (Dinheiro)'), seconds=0.4, at=c.A(2, 'dinheiro', 0.8), label='Saldo em Caixa (Dinheiro)')
    c.hover(LINHA('Saldo Bancário'), seconds=0.4, at=c.A(2, 'bancos', 0.8), label='Saldo Bancário')
    c.hover(LINHA('Contas a Receber'), seconds=0.6, at=c.A(2, 'clientes', 0.8), label='Contas a Receber')
    c.hover(LINHA('Estoque (Projeção de Venda)'), seconds=0.4, at=c.A(2, 'estoque', 0.8), label='Estoque (Projeção de Venda)')
    c.hover(LINHA('Contas a Pagar'), seconds=0.6, at=c.A(2, 'deve', 0.8), label='Contas a Pagar')
    c.mark(3)
    c.hover(LINHA('Estoque (Projeção de Venda)'), seconds=1.0, at=c.A(3, 'projeção', 0.8), label='Estoque (Projeção de Venda) (ZOOM)')
    c.mark(4)
    c.mark(5)
    c.mark(6)
    c.hover(SEL('[title="Exportar Patrimônio"]'), seconds=1.0, at=c.A(6, 'Exportar', 0.8), label='Exportar Patrimônio (ZOOM)')
    c.fim()
    return c


def cap09():
    pre = [{'do': 'click', 'target': BTN('Comparar períodos')}, {'do': 'waitFor', 'text': 'Prévia das colunas', 'timeout': 10},
           {'do': 'click', 'target': TXT('Período anterior', within=DLG)}, {'do': 'click', 'target': BTN('Aplicar comparação'), 'noScroll': True},
           {'do': 'waitFor', 'text': '31/10/26', 'timeout': 10}, {'do': 'waitFor', 'text': 'Demonstrativo Financeiro (DRE)', 'timeout': 15}, AGUARDA,
           {'do': 'eval', 'js': js_topo(0)}]
    c = Cap(9, setup_relatorio('Demonstrativo Financeiro (DRE)', pre), pace=0.5)
    c.mark(1)
    c.ev(js_rola_texto('Evolução Mensal', 110, 1500), at=0.3, label='desce até a Evolução Mensal')
    c.hover(LINHA('Evolução Mensal'), seconds=0.6, at=c.A(1, 'seis', 0.5), label='Evolução Mensal')
    c.mark(2)
    c.hover(LINHA('out/26', nth=-1), seconds=1.0, at=c.A(2, 'outubro', 0.8), label='linha out/26 (ZOOM)')
    c.mark(3)
    c.ev(js_rola_texto('Comparar períodos', 200, 900), at=c.L(3) - 0.9, label='sobe até o cabeçalho da tabela')
    c.click(BTN('Comparar períodos'), at=c.A(3, 'Comparar', 0.6, nth=1), label='Comparar períodos')
    c.waitfor(text='Prévia das colunas', timeout=8)
    c.click(TXT('Período anterior', within=DLG), at=c.A(3, 'Período', 0.6), label='Período anterior (setembro)')
    c.mark(4)
    c.click(BTN('Aplicar comparação'), at=c.A(4, 'Aplico', 0.6), label='Aplicar comparação', noScroll=True)
    c.ev(js_rola_texto('(+) Receita Bruta', 110, 1500), at=c.A(4, 'lado', 0.3), label='desce pelas linhas comparadas')
    c.confere('main', ['Setembro de 2026', 'Outubro de 2026'], 'as duas colunas lado a lado')
    c.mark(5)
    c.click(GRUPO('06.01'), at=c.A(5, 'categoria', 0.6), label='abre as categorias das despesas operacionais')
    c.hover(LINHA('Energia elétrica'), seconds=1.0, at=c.A(5, 'renomear', 0.5), label='linhas casadas pelo nome da categoria')
    c.fim()
    return c


def cap10():
    c = Cap(10, setup_relatorio('Demonstrativo Financeiro (DRE)'), pace=0.5)
    c.mark(1)
    c.click(ABA_R('historico'), at=0.2, label='aba Histórico')
    c.click({'role': 'tab', 'name': 'Despesas'}, at=c.A(1, 'despesas', 1.0), label='Despesas')
    c.mark(2)
    c.hover(TXT('Conta de energia', within=MAIN), seconds=0.6, at=c.A(2, 'lançamento', 0.8), label='os lançamentos de outubro')
    c.mark(3)
    c.click(BTN('Filtros'), at=c.A(3, 'Filtros', 0.9), label='Filtros')
    c.click(BTN('Categoria', within=DLG), at=c.A(3, 'categoria', 0.9), label='Categoria')
    c.click(TXT('Energia elétrica', within=POP), at=c.A(3, 'Energia', 0.6, nth=1), label='marca Energia elétrica')
    c.press('Escape', at=c.A(3, 'Dá', 0.1, nth=1), label='fecha a lista')
    c.hover(TXT('Cliente/Fornecedor', within=DLG), seconds=0.4, at=c.A(3, 'cliente', 0.8), label='Cliente/Fornecedor')
    c.hover(TXT('Centro de custo', within=DLG), seconds=0.4, at=c.A(3, 'centro', 0.8), label='Centro de custo')
    c.mark(4)
    c.click(BTN('Aplicar'), at=c.L(4) - 0.9, label='Aplicar', noScroll=True)
    c.hover(LINHA('Conta de energia'), seconds=1.2, at=c.A(4, 'dia', 0.9), label='as duas Conta de energia (ZOOM)')
    c.confere('main', ['2 lançamentos', '-R$ 7.700,00', 'Conta de energia'], 'duas contas de energia')
    c.mark(5)
    c.click(BTN('Excluir lançamento', nth=0), at=c.A(5, 'lixeira', 0.9), label='lixeira da conta das 16:40')
    c.waitfor(text='Excluir lançamento?', timeout=8)
    c.click(BTN('Excluir', within=ALERTA), at=c.A(5, 'Excluir', 0.7), label='Excluir')
    c.waitfor(text='Lançamento excluído.', timeout=8)
    c.confere('main', ['1 lançamento', '-R$ 3.850,00', '09:12'], 'ficou uma conta só (a das 09:12)')
    c.mark(6)
    c.hover(BTN('Excluir lançamento'), seconds=0.6, at=c.L(6) - 0.6, label='lixeira (ZOOM)')
    c.hover(BTN('Editar categoria'), seconds=0.8, at=c.A(6, 'lápis', 0.8), label='lápis Editar categoria')
    c.mark(7)
    c.fim()
    return c


def cap11():
    c = Cap(11, setup_relatorio('Exportar', [{'do': 'click', 'target': {'role': 'tab', 'name': 'Despesas'}}, AGUARDA]), pace=0.5)
    c.mark(1)
    c.click(BTN('Exportar'), at=c.A(1, 'Exportar', 1.0), label='Exportar do Histórico')
    c.mark(2)
    c.click(ITEM('PDF'), at=c.A(2, 'PDF', 0.8), label='PDF')
    c.waitfor(text='Exportar Histórico (PDF)', timeout=8)
    c.hover(TXT('Receitas', within=DLG), seconds=0.3, at=c.A(2, 'escolho', 1.0), label='Incluir no arquivo: Receitas')
    c.hover(TXT('Compras', within=DLG), seconds=0.3, at=c.A(2, 'despesas', 0.8), label='Incluir no arquivo: Compras')
    c.mark(3)
    c.click(BTN('Exportar PDF'), at=c.A(3, 'PDF', 0.8), label='Exportar PDF')
    c.waitfor(text='PDF gerado em nova aba', timeout=6, optional=True)
    c.mark(4)
    c.click(BTN('Exportar'), at=c.L(4) - 1.1, label='Exportar de novo')
    c.hover(ITEM('Fechamento completo (Excel)'), seconds=1.5, at=c.A(4, 'completo', 0.5), label='Fechamento completo (Excel) (ZOOM)')
    c.press('Escape', at=c.A(4, 'período', 0.3), label='fecha o menu')
    c.mark(5)
    c.click(ABA_R('dre'), at=c.L(5) - 1.1, label='aba DRE')
    c.waitfor(text='Demonstrativo Financeiro (DRE)', timeout=10)
    c.click(BTN('Exportar'), at=c.A(5, 'Exportar', 0.8), label='Exportar do DRE')
    c.hover(ITEM('Documento PDF'), seconds=1.5, at=c.A(5, 'Documento', 0.8), label='Planilha Excel e Documento PDF')
    c.press('Escape', at=c.A(5, 'regime', 0.2), label='fecha sem escolher')
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
        json.dump(d, open(os.path.join(HERE, f'cap{n:02d}.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
        nat = sum(1 for st in d['steps'] if st.get('do') != 'mark')
        feitos.append(f'cap{n:02d} {nat} passos, {len(c.linhas)} linhas, {c.dur:.1f} s{" (fala estimada)" if c.estimado else ""}')
        if os.environ.get('ANCORAS'):
            for i, p, t in c.anchors:
                print(f'   cap{n:02d} L{i} {p!r} -> {t}')
    print('\n'.join(feitos))


if __name__ == '__main__':
    main()
