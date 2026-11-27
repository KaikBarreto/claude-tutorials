#!/usr/bin/env python3
"""T15 · Relatório Financeiro e DRE (EcoFlix, EcoSistema 1.60.18): gera rec/t15/cap00..cap15.json (roteiros do robô) a partir da fala
($TUT_HOME/t15/narracao/capNN.json: o estimado até a voz chegar; com a voz, o da voz, sem mudar nada aqui). O cap16 (Recapitulando) é
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
→ `apos-cap02` (o centro de custo Produção) → `apos-cap10` (a cópia excluída: estado final, de onde o T21 parte) → `lote-categoria` (só o cap14: três diesel em Outras Despesas).
Capítulos 4 a 15: o setup abre o relatório (aba de partida pelo localStorage "financial-report-tab") e escolhe "Mês passado" fora do vídeo.
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
VERSAO = '1.60.18'
HOJE = FAKE_NOW[:10]
NOMES = ['Abertura', 'O plano de contas', 'Centros de custo', 'O Relatório Financeiro', 'O Dashboard do mês', 'Fornecedores, clientes e ticket médio',
         'Lendo o DRE', 'Organizando o DRE', 'Caixa ou competência', 'O patrimônio de hoje', 'Mês a mês', 'Vai ter dinheiro? A DFC prevista',
         'Por onde o dinheiro passou: a DFC realizada', 'O Histórico', 'Vários lançamentos de uma vez', 'Exportar em Excel e PDF']
T14 = ['t14/inicio'] + [f't14/apos-cap{n:02d}' for n in (2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 14)]
_E = T14 + [f'{AULA}/inicio', f'{AULA}/apos-cap01', f'{AULA}/apos-cap02', f'{AULA}/apos-cap10']
# o nome apos-capNN é o do capítulo de ORIGEM (Histórico era o cap 10) e não muda: a T21 e a T25 leem `t15/apos-cap10`
_N = len(T14)
SEMENTE = {0: _E[:_N + 1], 1: _E[:_N + 1], 2: _E[:_N + 2], 14: _E[:_N + 4] + [f'{AULA}/lote-categoria'], 15: _E[:_N + 4],
            **{n: _E[:_N + 3] for n in range(3, 14)}}
SEMENTE[11] = _E[:_N + 3] + [f'{AULA}/previsto']   # a DFC prevista precisa de contas abertas: água vencida e o telefone de outubro
ABA = {4: 'dashboard', 5: 'dashboard', 6: 'dashboard', 7: 'dre', 8: 'dre', 9: 'dre', 10: 'dre', 11: 'dashboard', 12: 'dfc', 13: 'dre', 14: 'historico', 15: 'historico'}

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


BUSCA = SEL('input[placeholder^="Buscar por descrição"]')
CHECK = lambda n: SEL(f'main [role=checkbox][aria-label^="Selecionar lançamento "] >> nth={n}')   # linhas marcáveis do Histórico (ordem da lista)
# o app abre PDF em aba nova e a gravação filma uma aba só: POPS guarda cada window.open e PDF_JS devolve o PDF em base64 (padrão do t08/gerar.py)
POPS = "(()=>{const o=window.open;window.__pops=[];window.open=function(...a){const w=o.apply(this,a);window.__pops.push(w);return w};return 'ok'})()"
PDF_JS = ("(async()=>{const w=(window.__pops||[]).slice(-1)[0];if(!w)return 'SEM JANELA';for(let i=0;i<40;i++){let f=null;"
          "try{f=w.document&&w.document.querySelector('#pdf-frame')}catch(e){return 'ERRO '+e}"
          "if(f&&f.src){const b=await (await fetch(f.src.split('#')[0])).blob();const u=new Uint8Array(await b.arrayBuffer());let s='';"
          "for(let k=0;k<u.length;k+=8192)s+=String.fromCharCode.apply(null,u.subarray(k,k+8192));return 'PDF:'+btoa(s)}"
          "await new Promise(r=>setTimeout(r,250))}return 'SEM PDF'})()")
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
    c.ev("(()=>{const i=document.querySelector('#financial-category-name');if(!i)return 'SEM CAMPO';i.focus();return document.activeElement===i})()", label='foco no campo Nome')
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
    c.click(PONTOS('Frete de entrega'), at=c.A(8, 'pontos', 0.9), label='Ações de Frete de entrega')
    c.hover(ITEM('Editar'), seconds=0.3, at=c.A(8, 'editar', 0.7), label='menu: Editar')
    c.hover(ITEM('Tornar principal'), seconds=0.8, at=c.A(8, 'Tornar', 0.7), label='menu: Tornar principal')
    c.press('Escape', at=c.A(8, 'lista', 0.2), label='fecha o menu sem escolher')
    c.mark(9)
    c.ev(js_rola_texto('Telefone e internet', 330, 700), at=c.L(9) - 0.9, label='desce até Telefone e internet')
    c.click(PONTOS('Telefone e internet'), at=c.L(9) - 0.2, label='Ações de Telefone e internet')
    c.click(ITEM('Excluir'), at=c.A(9, 'Excluir', 0.7), label='Excluir')
    c.waitfor(text='Excluir categoria?', timeout=8)
    c.hover(TXTP('Os lançamentos não serão apagados', within=ALERTA), seconds=1.5, at=c.A(9, 'apaga', 0.9), label='texto do Excluir categoria? (ZOOM)')
    c.click(BTN('Cancelar', within=ALERTA), at=c.A(9, 'Excluir', 0.7, nth=1), label='Cancelar')
    c.mark(10)
    c.ev(js_rola_texto('Categorias de despesa', 170, 600), at=c.L(10) - 0.9, label='sobe até Categorias de despesa')
    c.hover(TXTP('arraste para reordenar', within=MAIN, nth=-1), seconds=1.0, at=c.A(10, 'ordem', 0.8), label='arraste para reordenar')
    c.mark(11)
    c.ev(js_rola_texto('Categorias de despesa', 170, 500), at=c.L(11) - 0.9, label='sobe até Categorias de despesa')
    c.click(BTN('Nova', nth=1), at=c.A(11, 'categoria', 0.8), label='Nova (despesa)')
    c.waitfor(text='Nova categoria', timeout=8)
    c.ev("(()=>{const i=document.querySelector('#financial-category-name');if(!i)return 'SEM CAMPO';i.focus();return document.activeElement===i})()", label='foco no campo Nome')
    c.type(SEL('#financial-category-name'), 'Máquinas e veículos', at=c.A(11, 'cuidado', 0.0), label='Nome: Máquinas e veículos', noClick=True)
    c.mark(12)
    c.mark(13)
    c.mark(14)
    c.mark(15)
    c.click(COMBO_DLG('Despesas operacionais'), at=c.A(15, 'vai', 0.6), label='abre Onde aparece no DRE')
    c.click(OPT('Não compõe o DRE'), at=c.A(15, 'Não', 0.7), label='Não compõe o DRE')
    c.hover(TXT('Prévia no DRE padrão', within=DLG), seconds=0.8, at=c.A(15, 'resultado', 0.6), label='prévia: informativo, não altera o resultado (ZOOM)')
    c.ev(js_rola_dlg('Grupo no Fluxo de Caixa (DFC)', 330, 500), at=c.A(15, 'fluxo', 1.0), label='desce a janela até o DFC')
    c.click(COMBO_DLG('Atividades operacionais'), at=c.A(15, 'acompanha', 1.1), label='abre Grupo no Fluxo de Caixa (DFC)')
    c.click(OPT('Atividades de investimento'), at=c.A(15, 'Atividades', 0.65), label='Atividades de investimento')
    c.mark(16)
    c.click(BTN('Criar categoria'), at=c.L(16) - 1.1, label='Criar categoria')
    c.waitfor(text='Categoria criada', timeout=8)
    c.waitfor(target=CARD('Máquinas e veículos'), timeout=6)
    c.ev(js_rola_texto('Máquinas e veículos', 420, 700), at=c.A(16, 'registra', 0.0), label='desce até Não compõe o DRE')
    c.hover(CARD('Máquinas e veículos'), seconds=0.8, at=c.A(16, 'compra', 0.0), label='Máquinas e veículos em Não compõe o DRE')
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
    c.hover(BTN('Editar centro de custo', nth=-1), seconds=0.5, at=c.A(5, 'lápis', 0.8), label='lápis Editar centro de custo')
    c.hover(BTN('Excluir centro de custo', nth=-1), seconds=0.5, at=c.A(5, 'lixeira', 0.8), label='lixeira Excluir centro de custo')
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
    c.hover(OPT('Personalizado'), seconds=0.5, at=c.A(2, 'Personalizado', 0.7), label='Personalizado')
    c.hover(OPT('Todos os tempos'), seconds=0.5, at=c.A(2, 'Todos', 0.7), label='Todos os tempos')
    c.click(OPT('Mês passado'), at=c.A(2, 'Mês', 1.0, nth=1), label='Mês passado')
    c.mark(3)
    c.hover(PERIODO('Mês passado'), seconds=0.5, at=c.A(3, 'período', 1.0), label='filtro em Mês passado')
    c.mark(4)
    c.hover(ABA_R('dashboard'), seconds=0.3, at=c.A(4, 'Dashboard', 0.5), label='aba Dashboard')
    c.hover(ABA_R('dre'), seconds=0.3, at=c.A(4, 'DRE', 0.5), label='aba DRE')
    c.hover(ABA_R('dfc'), seconds=0.3, at=c.A(4, 'DFC', 0.5), label='aba DFC')
    c.hover(ABA_R('centros-custo'), seconds=0.3, at=c.A(4, 'Centros', 0.5), label='aba Centros de Custo')
    c.hover(ABA_R('historico'), seconds=0.4, at=c.A(4, 'Histórico', 0.5), label='aba Histórico')
    c.mark(5)
    c.click(ABA_R('centros-custo'), at=c.A(5, 'Centros', 0.6), label='Centros de Custo')
    c.waitfor(text='Ranking dos centros de custo', timeout=10)
    c.mark(6)
    c.hover(TXTP('vs. período anterior', within=MAIN, nth=0), seconds=1.0, at=c.A(6, 'cartão', 0.8), label='vs. período anterior nos cartões')
    c.mark(7)
    c.ev(js_rola_texto('Receitas x despesas por centro', 120, 700), at=c.L(7) - 0.9, label='desce até o gráfico por centro')
    c.click(SEL('main .recharts-bar-rectangle path[fill="#dc2626"]'), at=c.A(7, 'numa', 0.7), label='coluna do Pátio do gráfico (despesas)', timeout=6)
    c.confere('main', ['Folha salarial', 'Aluguel', 'Energia elétrica'], 'categorias do Pátio no detalhe')
    c.mark(8)
    c.ev(js_rola_texto('Ranking dos centros de custo', 170, 900), at=c.L(8) - 0.9, label='desce até o Ranking dos centros de custo')
    c.hover(TXT('Pátio', within=MAIN, nth=-1), seconds=0.5, at=c.A(8, 'pátio', 0.5), label='Pátio no ranking')
    c.hover(TXT('Coleta', within=MAIN, nth=-1), seconds=0.5, at=c.A(8, 'coleta', 0.5), label='Coleta no ranking')
    c.mark(9)
    c.click(BTN('Movimentações', within=MAIN, nth=0), at=c.A(9, 'Movimentações', 0.7), label='Movimentações (histórico do centro)')
    c.waitfor(target={'placeholder': 'Buscar por descrição, categoria ou valor'}, timeout=10)
    c.hover(TXTP('lançamentos', within=MAIN), seconds=0.6, at=c.A(9, 'filtrado', 0.8), label='o Histórico já filtrado')
    c.click(ABA_R('centros-custo'), at=c.L(10) - 1.4, label='volta para Centros de Custo')
    c.waitfor(text='Ranking dos centros de custo', timeout=10)
    c.mark(10)
    c.ev(js_rola_contem('Esta visão considera receitas', 420, 700), at=c.L(10) - 0.9, label='desce até o aviso azul')
    c.hover(TXTP('Esta visão considera receitas', within=MAIN), seconds=1.0, at=c.A(10, 'aviso', 0.5), label='aviso azul dos centros de custo (ZOOM)')
    c.mark(11)
    c.ev(js_topo(800), at=c.A(11, 'dica', 0.4), label='sobe ao cabeçalho')
    c.hover(SEL('main h1'), seconds=0.8, at=c.A(11, 'permissão', 0.5), label='cabeçalho do Relatório Financeiro')
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
    c.click(LINHA('Ver todos', nth=1), at=c.A(7, 'Ver', 0.8), label='Ver todos (Top Clientes)')
    c.waitfor(target=SEL('[role=dialog]'), timeout=8)
    c.hover(SEL('[role=dialog]'), seconds=1.0, label='a lista completa')
    c.press('Escape', label='fecha a lista')
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
    c.hover(LINHA('Energia elétrica'), seconds=1.2, at=c.A(7, 'categoria', 0.8), label='valor da Energia elétrica (ZOOM)')
    c.mark(8)
    c.click(SEL('main button[aria-label^="Recolher"][aria-label*="Despesas Operacionais"]'), at=c.A(8, 'recolhe', 0.7), label='Recolher a faixa 06')
    c.click(SEL('main button[aria-label^="Expandir"][aria-label*="Despesas Operacionais"]'), at=c.L(9) - 1.6, label='Expandir a faixa 06')
    c.mark(9)
    c.ev(js_rola_texto('= Resultado do Período', 420, 900), at=c.L(9) - 0.9, label='desce até o resultado')
    c.hover(LINHA('R$ 6.500,00', nth=-1), seconds=1.2, at=c.A(9, 'seis', 0.9), label='08 = Resultado do Período R$ 6.500,00 (ZOOM)')
    c.confere('main', ['= Resultado do Período', 'R$ 6.500,00'], 'resultado de outubro em competência')
    c.mark(10)
    c.hover(LINHA('(-) Despesas Operacionais'), seconds=0.8, at=c.A(10, 'aparece', 2.4), label='a tabela')
    c.fim()
    return c


def cap07():
    c = Cap(7, setup_relatorio('Demonstrativo Financeiro (DRE)'), pace=0.5)
    c.mark(1)
    c.click(BTN('Organizar categorias'), at=c.A(1, 'Organizar', 0.6), label='Organizar categorias')
    c.waitfor(text='Prévia da estrutura', timeout=10)
    c.mark(2)
    c.ev(js_rola_dlg('Receita Bruta', 200, 700), at=c.A(2, 'faixas', 0.3), label='a prévia: 01 Receita Bruta')
    c.ev(js_rola_dlg('Despesas Operacionais', 150, 1200), at=c.A(2, 'grupos', 0.3), label='a prévia: 06 Despesas Operacionais')
    c.mark(3)
    c.ev(js_rola_dlg('Novo subgrupo', 160, 700), at=c.L(3) - 0.9, label='sobe ao Novo subgrupo')
    c.click(SEL('[role=dialog] button[role=combobox] >> nth=0'), at=c.A(3, 'subgrupo', 0.9), label='abre Natureza')
    c.click(OPT('06 · Despesas Operacionais'), at=c.A(3, 'nas', 0.7), label='06 · Despesas Operacionais')
    c.type(SEL('#new-dre-group'), 'Despesas com pessoal', at=c.A(3, 'Operacionais', 0.6), label='Novo subgrupo: Despesas com pessoal')
    c.click(BTN('Adicionar', within=DLG), at=c.A(3, 'pessoal', 0.0, nth=0), label='Adicionar')
    c.waitfor(text='Grupo criado', timeout=8)
    c.mark(4)
    c.ev(js_rola_dlg('Folha salarial', 300, 700), at=c.L(4) - 0.9, label='desce até a Folha salarial')
    c.click(SEL('[role=dialog] button[aria-label="Mover Folha salarial para outro grupo DRE"]'), at=c.A(4, 'escolhendo', 0.8), label='lista Mover Folha salarial')
    c.click(OPT('06 · Despesas com pessoal'), at=c.A(4, 'lista', 0.8), label='06 · Despesas com pessoal')
    c.waitfor(text='Categoria movida', timeout=8)
    c.hover(TXT('Despesas com pessoal', within=DLG, nth=-1), seconds=1.5, at=c.A(4, 'Nenhum', 0.8), label='o grupo novo com a folha dentro (ZOOM)')
    c.mark(5)
    c.hover(SEL('[role=dialog] button[aria-label="Editar grupo Despesas com pessoal"]'), seconds=0.6, at=c.A(5, 'renomear', 0.8), label='lápis do grupo')
    c.hover(SEL('[role=dialog] button[aria-label="Excluir grupo Despesas com pessoal"]'), seconds=0.8, at=c.A(5, 'excluir', 0.8), label='lixeira do grupo')
    c.mark(6)
    c.ev(js_rola_dlg('Precisa enxergar este DRE de outra forma?', 300, 800), at=c.L(6) - 0.9, label='desce até Outras visões')
    c.click(BTN('Outras visões', within=DLG), at=c.A(6, 'Outras', 0.7), label='Outras visões')
    c.waitfor(text='Outras visões do mesmo DRE', timeout=10)
    c.hover(TXT('Criar outra visão', within=DLG), seconds=0.8, at=c.A(6, 'Quem', 0.8), label='Criar outra visão')
    c.hover(TXT('DRE padrão do sistema', within=DLG), seconds=0.8, at=c.A(6, 'padrão', 0.8, nth=0), label='DRE padrão do sistema (Em uso)')
    c.mark(7)
    c.click(BTN('Voltar à organização padrão', within=DLG), at=c.L(7) - 0.4, label='Voltar à organização padrão')
    c.click(BTN('Fechar', within=DLG), at=c.A(7, 'Fecho', 0.6), label='Fechar')
    c.ev(js_rola_texto('Despesas com pessoal', 300, 900), at=c.A(7, 'DRE', 0.4), label='o grupo novo no DRE')
    c.click(GRUPO('06.02'), at=c.A(7, 'grupo', 0.8), label='abre o grupo Despesas com pessoal (06.02)')
    c.confere('main', ['Despesas com pessoal', 'Folha salarial'], 'grupo novo no DRE')
    c.fim()
    return c


def cap08():
    c = Cap(8, setup_relatorio('Demonstrativo Financeiro (DRE)'), pace=0.5)
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
    c.ev(js_rola_contem('O detalhamento por centro de custo', 330, 800), at=c.L(11) - 0.9, label='sobe até a faixa cinza do regime de caixa')
    c.hover(TXTP('O detalhamento por centro de custo', within=MAIN), seconds=1.5, at=c.A(11, 'detalhamento', 0.8), label='faixa cinza: detalhamento por centro de custo')
    c.mark(12)
    c.ev(js_rola_texto('04.01', 330, 800), at=c.L(12) - 0.9, label='sobe até 04 Custos Operacionais')
    c.click(GRUPO('04.01'), at=c.A(12, 'linha', 0.6), label='abre o grupo do custo')
    c.hover(LINHA('CMV / Compras de materiais'), seconds=1.0, at=c.A(12, 'Compras', 0.5), label='CMV / Compras de materiais (ZOOM)')
    c.confere('main', ['CMV / Compras de materiais', 'R$ 256.860,00'], 'CMV em caixa')
    c.ev(js_tab('Regime de Competência'), at=c.A(12, 'competência', 0.2), label='troca para competência (sem cursor)')
    c.confere('main', ['R$ 218.860,00'], 'CMV em competência')
    c.ev(js_tab('Regime de Caixa'), at=c.A(12, 'caixa', 0.2), label='troca para caixa (sem cursor)')
    c.confere('main', ['R$ 256.860,00'], 'CMV em caixa de novo')
    c.mark(13)
    c.hover(LINHA('CMV / Compras de materiais'), seconds=1.0, at=c.A(13, 'diferença', 0.5), label='a linha do CMV (mesmo zoom)')
    c.mark(14)
    c.ev(js_rola_texto('(+) Receita Bruta', 150, 900), at=c.L(14) - 0.9, label='a tabela inteira')
    c.hover(LINHA('(-) Custos Operacionais'), seconds=0.8, at=c.A(14, 'normal', 0.5), label='a tabela inteira')
    c.mark(15)
    c.hover(LINHA('(-) Despesas Operacionais'), seconds=0.8, at=c.A(15, 'estoque', 0.8), label='a tabela (dica do estoque sem custo)')
    c.fim()
    return c


def cap09():
    c = Cap(9, setup_relatorio('Demonstrativo Financeiro (DRE)'), pace=0.5)
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


def cap10():
    pre = [{'do': 'click', 'target': BTN('Comparar períodos')}, {'do': 'waitFor', 'text': 'Prévia das colunas', 'timeout': 10},
           {'do': 'click', 'target': TXT('Período anterior', within=DLG)}, {'do': 'click', 'target': BTN('Aplicar comparação'), 'noScroll': True},
           {'do': 'waitFor', 'text': '31/10/26', 'timeout': 10}, {'do': 'waitFor', 'text': 'Demonstrativo Financeiro (DRE)', 'timeout': 15}, AGUARDA,
           {'do': 'eval', 'js': js_topo(0)}]
    c = Cap(10, setup_relatorio('Demonstrativo Financeiro (DRE)', pre), pace=0.5)
    c.mark(1)
    c.ev(js_rola_texto('Evolução Mensal', 110, 1500), at=0.3, label='desce até a Evolução Mensal')
    c.hover(LINHA('Evolução Mensal'), seconds=0.6, at=c.A(1, 'seis', 0.5), label='Evolução Mensal')
    c.mark(2)
    c.hover(LINHA('out/26', nth=-1), seconds=1.0, at=c.A(2, 'outubro', 0.8), label='linha out/26 (ZOOM)')
    c.mark(3)
    c.ev(js_rola_texto('Comparar períodos', 200, 900), at=c.L(3) - 0.9, label='sobe até o cabeçalho da tabela')
    c.click(BTN('Comparar períodos'), at=c.A(3, 'Comparar', 0.6, nth=1), label='Comparar períodos')
    c.waitfor(text='Prévia das colunas', timeout=8)
    c.ev("(()=>[...document.querySelectorAll('[role=dialog] button')].some(b=>/Remover Setembro de 2026/.test(b.getAttribute('aria-label')||b.innerText))?'ja marcado':'desmarcado')()", label='estado do Período anterior ao abrir')
    c.hover(TXT('Período anterior', within=DLG), seconds=0.3, at=c.A(3, 'Período', 0.8), label='Período anterior (setembro)')
    c.click(TXT('Período anterior', within=DLG), label='marca Período anterior', unless={'role': 'button', 'name': 'Remover Setembro de 2026'})
    c.mark(4)
    c.hover(TXT('Mesmo período no ano passado', within=DLG), seconds=0.6, at=c.A(4, 'ano', 0.8), label='Mesmo período no ano passado')
    c.hover(TXT('Outro período', within=DLG), seconds=0.6, at=c.A(4, 'outras', 0.8), label='Outro período')
    c.mark(5)
    c.click(BTN('Aplicar comparação'), at=c.A(5, 'Aplico', 0.6), label='Aplicar comparação', noScroll=True)
    c.ev(js_rola_texto('(+) Receita Bruta', 110, 1500), at=c.A(5, 'lado', 0.3), label='desce pelas linhas comparadas')
    c.confere('body', ['Setembro de 2026', 'Outubro de 2026'], 'as duas colunas lado a lado')   # o cabeçalho fixo da tabela sai do <main> ao rolar
    c.mark(6)
    c.click(GRUPO('06.01'), at=c.A(6, 'categoria', 0.6), label='abre as categorias das despesas operacionais')
    c.hover(LINHA('Energia elétrica'), seconds=1.0, at=c.A(6, 'renomear', 0.5), label='linhas casadas pelo nome da categoria')
    c.mark(7)
    c.ev(js_rola_texto('Comparar períodos', 200, 900), at=c.L(7) - 0.9, label='sobe até o cabeçalho da tabela')
    c.click(BTN('Comparar períodos'), at=c.A(7, 'voltar', 0.8), label='Comparar períodos')
    c.waitfor(text='Prévia das colunas', timeout=8)
    c.click(BTN('Remover comparações'), at=c.A(7, 'Remover', 0.7), label='Remover comparações', noScroll=True)
    c.confere('body', ['Outubro de 2026'], 'a tabela volta a uma coluna')
    c.fim()
    return c


def cap11():
    c = Cap(11, setup_relatorio('Superávit'), pace=0.5)
    c.mark(1)
    c.click(ABA_R('dfc'), at=c.A(1, 'DFC', 0.6), label='aba DFC')
    c.waitfor(text='Saldo atual', timeout=15)
    c.hover(BTN('Previsto'), seconds=0.6, at=c.A(1, 'Previsto', 0.6), label='Previsto (marcado)')
    c.mark(2)
    c.mark(3)
    c.hover(TXT('Saldo atual', within=MAIN), seconds=0.4, at=c.A(3, 'saldo', 0.8), label='Saldo atual')
    c.hover(TXT('A receber · 15 dias', within=MAIN), seconds=0.4, at=c.A(3, 'entra', 0.8), label='A receber · 15 dias')
    c.hover(TXT('A pagar · 15 dias', within=MAIN), seconds=0.4, at=c.A(3, 'sai', 0.8), label='A pagar · 15 dias')
    c.hover(TXT('Dívidas a receber', within=MAIN), seconds=1.0, at=c.A(3, 'dívidas', 0.8), label='Dívidas a receber e a pagar (ZOOM)')
    c.mark(4)
    c.ev(js_rola_texto('Saldo inicial', 330, 900), at=c.L(4) - 0.9, label='desce até a tabela do fluxo de caixa')
    c.hover(TXT('Saldo inicial', within=MAIN), seconds=0.5, at=c.A(4, 'final', 1.2), label='Saldo inicial')
    c.hover(TXT('Saldo final', within=MAIN), seconds=0.8, at=c.A(4, 'final', 0.6, nth=0), label='Saldo final')
    c.mark(5)
    c.click(SEL('main button[aria-label$="categorias de saída"]'), at=c.A(5, 'seta', 0.7), label='seta do Total de saídas')
    c.mark(6)
    c.click(SEL('main tr:has(button[aria-label$="categorias de saída"]) td[role=button] >> nth=0'), at=c.A(6, 'clicando', 0.7), label='um valor do Total de saídas')
    c.waitfor(text='Para editar ou dar baixa, abra o lançamento em Contas a Pagar/Receber.', timeout=8)
    c.hover(TXT('Para editar ou dar baixa, abra o lançamento em Contas a Pagar/Receber.', within=DLG), seconds=1.0, at=c.A(6, 'Pra', 0.8), label='lançamentos do dia (ZOOM)')
    c.press('Escape', at=c.L(7) - 1.6, label='fecha a janela')
    c.mark(7)
    c.ev(js_rola_texto('Saldo por conta', 160, 800), at=c.L(7) - 0.9, label='desce até Saldo por conta')
    c.ev(js_rola_texto('Evolução do saldo', 160, 900), at=c.A(7, 'gráfico', 0.9), label='Evolução do saldo')
    c.ev(js_rola_texto('O que já venceu e não foi baixado', 160, 900), at=c.A(7, 'lista', 0.9), label='O que já venceu e não foi baixado')
    c.mark(8)
    c.ev(js_topo(700), at=c.L(8) - 0.9, label='sobe ao topo')
    c.click(BTN('30 dias'), at=c.A(8, 'trinta', 0.8), label='30 dias')
    c.mark(9)
    c.ev(js_rola_contem('Previsão otimista', 420, 900), at=c.L(9) - 0.9, label='desce até a Previsão otimista')
    c.hover(TXTP('Previsão otimista', within=MAIN), seconds=1.5, at=c.A(9, 'otimista', 0.8), label='Previsão otimista (ZOOM)')
    c.mark(10)
    c.ev(js_topo(700), at=c.L(10) - 0.9, label='sobe ao topo')
    c.fim()
    return c


def cap12():
    c = Cap(12, setup_relatorio('Saldo atual'), pace=0.5)
    c.mark(1)
    c.click(BTN('Realizado'), at=c.A(1, 'Realizado', 0.6), label='Realizado')
    c.waitfor(text='Variação líquida', timeout=15)
    c.hover(TXTP('Realizado em', within=MAIN), seconds=0.8, at=c.A(1, 'segue', 0.8), label='Realizado em Outubro de 2026')
    c.mark(2)
    c.hover(TXT('Variação líquida', within=MAIN, nth=0), seconds=1.5, at=c.A(2, 'saiu', 0.8), label='Variação líquida (ZOOM)')
    c.ev("(async()=>{for(let i=0;i<20;i++){const t=document.querySelector('main').innerText;const m=t.match(/Varia[çc][ãa]o l[íi]quida\\s*\\n?\\s*(R\\$\\s?-?[\\d.,]+|-R\\$\\s?[\\d.,]+)/i);if(m)return (m[1].includes('-')?'OK: saiu mais do que entrou: ':'DIFERENTE: entrou mais do que saiu: ')+m[1];await new Promise(r=>setTimeout(r,250));}return 'DIFERENTE: sem Variação líquida'})()", label='confere saiu mais do que entrou em outubro')
    c.mark(3)
    c.ev(js_rola_texto('Estrutura do DFC', 160, 900), at=c.L(3) - 0.9, label='desce até a Estrutura do DFC')
    c.mark(4)
    c.click(SEL('main button[data-dfc-group-icon] >> nth=0'), at=c.A(4, 'decide', 0.6), label='recolhe uma atividade')
    c.click(SEL('main button[data-dfc-group-icon] >> nth=0'), at=c.L(5) - 1.6, label='abre a atividade de novo')
    c.mark(5)
    c.ev(js_rola_texto('Realizado dia a dia', 160, 1000), at=c.A(5, 'embaixo', 0.8), label='Realizado dia a dia')
    c.mark(6)
    ev_topo = c.ev(js_topo(700), at=c.L(6) - 0.9, label='sobe ao topo')
    c.click(BTN('Filtros'), at=c.A(6, 'filtrar', 0.7), label='Filtros')
    c.click(SEL('[role=menuitemcheckbox]:has-text("Coleta")'), at=c.A(6, 'centro', 0.7), label='marca Coleta')
    c.press('Escape', at=c.A(6, 'vale', 0.4), label='fecha o menu')
    c.hover(TXT('Filtro aplicado ao realizado e às exportações.', within=MAIN), seconds=0.8, at=c.A(6, 'arquivo', 0.8), label='Filtro aplicado (ZOOM)')
    c.mark(7)
    c.click(BTN('Filtros (1)'), at=c.L(7) - 1.4, label='abre Filtros')
    c.click(ITEM('Limpar filtros'), at=c.L(7) - 0.9, label='Limpar filtros')
    c.click(BTN('Exportar'), at=c.A(7, 'Exportar', 0.8), label='Exportar')
    c.hover(ITEM('CSV'), seconds=1.0, at=c.A(7, 'Excel', 0.8), label='Excel, PDF e CSV')
    c.press('Escape', at=c.A(7, 'CSV', 0.2), label='fecha sem escolher')
    c.mark(8)
    c.fim()
    return c


def cap13():
    c = Cap(13, setup_relatorio('Demonstrativo Financeiro (DRE)'), pace=0.5)
    c.mark(1)
    c.click(ABA_R('historico'), at=0.2, label='aba Histórico')
    c.click({'role': 'tab', 'name': 'Despesas'}, at=c.A(1, 'despesas', 1.0), label='Despesas')
    c.mark(2)
    c.hover(TXTP('lançamentos', within=MAIN), seconds=0.6, at=c.A(2, 'lançamento', 0.8), label='os lançamentos de outubro')
    c.mark(3)
    c.type(BUSCA, '3850', at=c.A(3, 'três', 0.3), label='busca: 3850')
    c.confere('main', ['Conta de energia', '2 lançamentos'], 'a busca por valor acha as duas contas')
    c.press('Control+a', at=c.L(4) - 1.6, label='seleciona a busca')
    c.press('Backspace', at=c.L(4) - 1.4, label='apaga a busca')
    c.mark(4)
    c.click(BTN('Filtros'), at=c.L(4) - 0.9, label='Filtros')
    c.click(BTN('Categoria', within=DLG), at=c.A(4, 'categoria', 0.9), label='Categoria')
    c.click(TXT('Energia elétrica', within=POP), at=c.A(4, 'Energia', 0.6, nth=1), label='marca Energia elétrica')
    c.press('Escape', at=c.A(4, 'Dá', 0.1, nth=1), label='fecha a lista')
    c.hover(TXT('Cliente/Fornecedor', within=DLG), seconds=0.4, at=c.A(4, 'cliente', 0.8), label='Cliente/Fornecedor')
    c.hover(TXT('Centro de custo', within=DLG), seconds=0.4, at=c.A(4, 'centro', 0.8), label='Centro de custo')
    c.hover(TXT('Conta bancária', within=DLG), seconds=0.4, at=c.A(4, 'conta', 0.8), label='Conta bancária', optional=True, timeout=3)
    c.mark(5)
    c.click(BTN('Aplicar'), at=c.L(5) - 0.9, label='Aplicar', noScroll=True)
    c.hover(LINHA('Conta de energia'), seconds=1.2, at=c.A(5, 'dia', 0.9), label='as duas Conta de energia (ZOOM)')
    c.confere('main', ['2 lançamentos', '-R$ 7.700,00', 'Conta de energia'], 'duas contas de energia')
    c.mark(6)
    c.click(BTN('Ver detalhes', nth=1), at=c.A(6, 'abro', 0.7), label='seta Ver detalhes da conta das 09:12')
    c.waitfor(text='Registrado em', timeout=8)
    c.hover(TXT('Registrado em', within=MAIN), seconds=1.5, at=c.A(6, 'Aparece', 0.8), label='o detalhe do lançamento (ZOOM)')
    c.click(BTN('Ocultar detalhes'), at=c.A(6, 'cópia', 0.9), label='fecha o detalhe')
    c.mark(7)
    c.click(BTN('Excluir lançamento', nth=0), at=c.A(7, 'lixeira', 0.9), label='lixeira da conta das 16:40')
    c.waitfor(text='Excluir lançamento?', timeout=8)
    c.click(BTN('Excluir', within=ALERTA), at=c.A(7, 'Excluir', 0.7), label='Excluir')
    c.waitfor(text='Lançamento excluído.', timeout=8)
    c.confere('main', ['1 lançamento', '-R$ 3.850,00', '09:12'], 'ficou uma conta só (a das 09:12)')
    c.mark(8)
    c.hover(BTN('Excluir lançamento'), seconds=0.6, at=c.L(8) - 0.6, label='lixeira (ZOOM)')
    c.hover(BTN('Editar categoria'), seconds=0.8, at=c.A(8, 'lápis', 0.8), label='lápis Editar categoria')
    c.mark(9)
    c.mark(10)
    c.click(SEL('main [role=tab]:has-text("Compras")'), at=c.L(10) - 0.2, label='aba Compras')
    c.click(BTN('Ver detalhes do pedido', nth=0), at=c.A(10, 'seta', 0.8), label='seta Ver detalhes do pedido')
    c.waitfor(text='Formas de pagamento', timeout=8)
    c.hover(TXT('Formas de pagamento', within=MAIN, nth=0), seconds=1.2, at=c.A(10, 'formas', 0.8), label='itens e formas de pagamento')
    c.fim()
    return c


def cap14():
    c = Cap(14, setup_relatorio('Exportar', [{'do': 'click', 'target': {'role': 'tab', 'name': 'Despesas'}}, AGUARDA]), pace=0.5)
    c.mark(1)
    c.click(BUSCA, at=0.4, label='campo de busca')
    c.type(BUSCA, 'Diesel', at=c.A(1, 'diesel', 0.9), label='busca: Diesel', noClick=True)
    c.confere('main', ['Diesel do caminhão', 'Outras Despesas', 'Combustível'], 'os diesel com a categoria errada')
    c.hover(TXT('Outras Despesas', within=MAIN, nth=0), seconds=1.0, at=c.A(1, 'Outras', 0.8), label='selo Outras Despesas')
    c.mark(2)
    c.click(BTN('Editar categoria', nth=1), at=c.A(2, 'lápis', 0.8), label='lápis da linha de 16/10')
    c.waitfor(text='Editar categoria', timeout=6)
    c.click(SEL('[role=dialog] button[role=combobox]'), at=c.A(2, 'escolho', 0.7), label='abre a lista de categorias')
    c.click(OPT('Combustível'), at=c.A(2, 'certa', 0.8), label='Combustível')
    c.click(BTN('Salvar', within=DLG), at=c.A(2, 'pronto', 0.7), label='Salvar')
    c.waitfor(text='Categoria atualizada', timeout=8)
    c.mark(3)
    c.click(BTN('Selecionar lançamentos'), at=c.A(3, 'Selecionar', 0.8), label='Selecionar')
    c.waitfor(text='Selecione até 100 lançamentos manuais de caixa ou banco.', timeout=6)
    c.click(CHECK(2), at=c.A(3, 'marco', 0.8), label='marca o diesel de 09/10')
    c.click(CHECK(3), at=c.A(3, 'dois', 0.3, nth=1), label='marca o diesel de 02/10')
    c.confere('main', ['2 lançamentos selecionados'], 'dois lançamentos marcados')
    c.mark(4)
    c.click(BTN('Alterar categoria'), at=c.L(4) - 0.2, label='Alterar categoria')
    c.waitfor(text='Alterar categoria de 2 lançamentos', timeout=8)
    c.click(SEL('[role=dialog] button[role=combobox]'), at=c.A(4, 'escolho', 0.7), label='abre a lista de categorias')
    c.click(OPT('Combustível'), at=c.A(4, 'categoria', 0.6, nth=1), label='Combustível')
    c.hover(TXTP('Valores e saldos não mudam', within=DLG), seconds=1.5, at=c.A(4, 'janela', 0.8), label='o resumo da janela (ZOOM)')
    c.mark(5)
    c.click(BTN('Aplicar categoria'), at=c.L(5) - 0.2, label='Aplicar categoria')
    c.waitfor(text='Categoria de 2 lançamentos atualizada.', timeout=8)
    c.confere('main', ['Combustível'], 'as linhas com o selo novo')
    c.mark(6)
    c.click(BTN('Selecionar lançamentos'), at=c.L(6) - 0.2, label='Selecionar de novo')
    c.click(CHECK(0), at=c.A(6, 'apagar', 0.8), label='marca uma linha de banco')
    c.click(CHECK(1), label='marca outra linha de banco')
    c.hover(BTN('Excluir selecionados'), seconds=1.2, at=c.A(6, 'Excluir', 0.7), label='Excluir selecionados (ativo)')
    c.click(BTN('Cancelar seleção de lançamentos'), at=c.A(6, 'nenhum', 0.8), label='Cancelar seleção')
    c.mark(7)
    c.fim()
    return c


def cap15():
    c = Cap(15, setup_relatorio('Exportar', [{'do': 'click', 'target': {'role': 'tab', 'name': 'Despesas'}}, AGUARDA, {'do': 'eval', 'js': POPS}]), pace=0.5)
    c.mark(1)
    c.click(BTN('Exportar'), at=c.A(1, 'Exportar', 1.0), label='Exportar do Histórico')
    c.mark(2)
    c.click(ITEM('PDF'), at=c.A(2, 'PDF', 0.8), label='PDF')
    c.waitfor(text='Exportar Histórico (PDF)', timeout=8)
    c.hover(TXT('Conta bancária', within=DLG), seconds=0.6, at=c.A(2, 'período', 0.8), label='campo Conta bancária', optional=True, timeout=3)
    c.hover(TXT('Receitas', within=DLG), seconds=0.3, at=c.A(2, 'escolho', 1.0), label='Incluir no arquivo: Receitas')
    # na aba Despesas a janela abre com Receitas e Despesas marcadas e Compras desmarcada (11/11): "eu escolho o que entra" = marcar Compras
    c.click(TXT('Compras', within=DLG), at=c.A(2, 'despesas', 0.8), label='marca Compras')
    c.ev("(async()=>{for(let i=0;i<8;i++){const c=[...document.querySelectorAll('[role=dialog] [role=checkbox]')].map(x=>x.getAttribute('data-state'));"
         "if(c.length>=3&&c.slice(0,3).every(v=>v==='checked'))return 'OK: receitas, despesas e compras marcadas';await new Promise(r=>setTimeout(r,150))}"
         "return 'DIFERENTE: '+[...document.querySelectorAll('[role=dialog] [role=checkbox]')].map(x=>x.getAttribute('data-state')).join(',')})()", label='confere Incluir no arquivo: as três marcadas')
    c.mark(3)
    c.click(BTN('Exportar PDF'), at=c.A(3, 'PDF', 0.8), label='Exportar PDF')
    c.waitfor(text='PDF gerado em nova aba', timeout=6, optional=True)
    c.ev(PDF_JS, at=c.L(3) + 3.0, label='PDF do histórico (aba nova, para a ilustração)')
    c.mark(4)
    c.click(BTN('Exportar'), at=c.L(4) - 1.1, label='Exportar de novo')
    c.hover(ITEM('Fechamento completo (Excel)'), seconds=0.8, at=c.A(4, 'completo', 0.9), label='Fechamento completo (Excel)')
    c.click(ITEM('Fechamento completo (Excel)'), at=c.A(4, 'pacote', 0.7), label='clica no Fechamento completo')
    c.waitfor(text='Fechamento gerado', timeout=15, optional=True)
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
    fns = {n: globals().get(f'cap{n:02d}') for n in range(16)}
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
