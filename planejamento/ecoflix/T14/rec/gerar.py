#!/usr/bin/env python3
"""T14 · Bancos, cofre e conciliação bancária (EcoFlix, EcoSistema 1.60.18): gera rec/t14/cap00..cap17.json (roteiros do robô) a partir
da fala ($TUT_HOME/t14/narracao/capNN.json: o estimado até a voz chegar; com a voz, o da voz, sem mudar nada aqui). O cap18
(Recapitulando) é montagem das gravações dos outros capítulos: não tem robô.

Computador 1600x900 (padrão do mundo.json), Rafael Nogueira (MASTER) na Recicla Vale Metais; FAKE_NOW 2026-11-10T08:30:00-03:00 em todos os capítulos (o mesmo
no Supabase falso e no robô). Rodar de qualquer pasta: `python3 -I rec/t14/gerar.py [NN ...]` (ANCORAS=1 lista as âncoras). Depois:
`node rec/record.mjs rec/t14/capNN.json --check`; ensaio: `python3 -I rec/t14/ensaio.py NN` + `--rapido`; gravação: `rec/t14/t14_rodar.sh NN`.

LOGIN: todo capítulo é "anonymous" e o setup entra pela tela de login com "$TUT_USER"/"$TUT_SENHA" do ambiente (o Supabase falso aceita
qualquer senha; o valor nunca vai para arquivo nem log).

Cada passo é preso a uma palavra da fala: A(linha, 'palavra', folga) = início da palavra − folga (o custo do gesto até o cursor chegar:
clique ~0,6 s, 1º clique numa janela recém-aberta ~1,2 s, hover ~0,5 s; digitação sem clique na palavra − 0,05 s). A palavra casa
INTEIRA (sem acento e pontuação); repetida na linha pede `nth`. Marca Ln 0,9 s antes da linha; um passo que começa até 0,25 s antes da
marca a puxa para o início dele.

Estado de partida (rec/mundo/seeds-extra/t14/, escrito por rec/t14/t14_sementes.py, deltas em ordem): `inicio` (o fim do T13 que o T14
usa) → `apos-cap02` → `apos-cap03` → `apos-cap04` → `apos-cap06` → `apos-cap07` → ... → `apos-cap12`. O extrato OFX é fictício e sai do
rec/t14/t14_ofx.py (rec/t14/arquivos/Extrato_20261101_20261110.ofx).

RESPIRO (só com a fala ESTIMADA): pausas que a voz vai ganhar com o `pausas.py` (planejamento/ecoflix/T14/propostas_fala.md); com a voz
de verdade, as pausas já vêm nela e o RESPIRO deixa de valer.
"""
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TUT = os.path.normpath(os.path.join(HERE, '..', '..'))
AULA = 't14'
NARR = os.path.join(TUT, AULA, 'narracao')
FAKE_NOW = '2026-11-10T08:30:00-03:00'
VERSAO = '1.60.18'
HOJE = FAKE_NOW[:10]
# Numeração de 20/11/2026 (1.60.18): as funções capNN abaixo guardam o número ANTIGO (o das sementes apos-capNN) e NOVO leva ao capítulo de hoje;
# os três capítulos novos têm nome (cartao, corrigir, outros). 0 1 2 | 3 cartão | 4 cofre(3) | 5 movimentação(4) | 6 corrigir | 7 (5) ... 16 (14) | 17 outros | 18 recap
NOVO = {0: 0, 1: 1, 2: 2, 'cartao': 3, 3: 4, 4: 5, 'corrigir': 6, 5: 7, 6: 8, 7: 9, 8: 10, 9: 11, 10: 12, 11: 13, 12: 14, 13: 15, 14: 16, 'outros': 17}
NOMES = ['Abertura', 'A tela e as contas', 'Cadastrar e arquivar contas', 'O cartão de crédito da empresa', 'O cofre e o ajuste de saldo',
         'Movimentação, transferência e saque', 'Corrigir e excluir lançamentos', 'O que é conciliar', 'Importar o extrato', 'Casar com o sistema',
         'Baixar uma conta', 'Criar um lançamento', 'Buscar e aceitar centavos', 'Ignorar uma linha', 'Valores repetidos', 'Desfazer e cancelar',
         'Fechar a conciliação', 'Outros casos do extrato']
_E = [f'{AULA}/inicio', f'{AULA}/apos-cap02', f'{AULA}/apos-cap03', f'{AULA}/apos-cap04', f'{AULA}/apos-cap06', f'{AULA}/apos-cap07', f'{AULA}/apos-cap08',
      f'{AULA}/apos-cap09', f'{AULA}/apos-cap10', f'{AULA}/apos-cap11', f'{AULA}/apos-cap12']
_LOTE = f'{AULA}/lote'
_FIM14 = f'{AULA}/apos-cap14'
SEMENTE = {0: _E[:1], 1: _E[:1], 2: _E[:1], 3: _E[:2], 4: _E[:3], 5: _E[:4], 6: _E[:4], 7: _E[:5], 8: _E[:6], 9: _E[:7], 10: _E[:8], 11: _E[:9],
           12: _E[:10], 13: _E[:11], 14: _E[:11], 'cartao': _E[:2], 'corrigir': _E[:4] + [_LOTE], 'outros': _E[:11] + [_FIM14]}
# respiro na fala ESTIMADA: {cap: [(depois da linha N (1..), segundos)]} (o pausas.py põe o mesmo silêncio na voz de verdade)
RESPIRO = {}

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
        t = t.replace(fala, leg)
    return [norm(w) for w in t.split() if norm(w)]


def carregar_voz(n):
    d = json.load(open(os.path.join(NARR, f'cap{n:02d}.json'), encoding='utf8'))
    words = [dict(w) for w in d['words']]
    linhas = [dict(li) for li in d['linhas']]
    dur = float(d['dur'])
    if CAPS and texto_atual(n) != [norm(w['w']) for w in words if norm(w['w'])]:
        print(f'  AVISO cap{n:02d}: a fala do capNN.json não é a do tts_textos.py de hoje (rode o preparar_aula.sh de novo)')
    if d.get('estimado'):
        for depois, seg in sorted(RESPIRO.get(n, []), reverse=True):
            t0 = linhas[depois - 1]['e']
            for w in words:
                if w['s'] >= t0:
                    w['s'] = round(w['s'] + seg, 3); w['e'] = round(w['e'] + seg, 3)
            for li in linhas:
                if li['s'] >= t0:
                    li['s'] = round(li['s'] + seg, 3); li['e'] = round(li['e'] + seg, 3)
            dur += seg
    return words, linhas, dur, bool(d.get('estimado'))


def stable_id(chave):
    """o mesmo UUID do `@id:<chave>` das sementes (rec/fakebase/core/util.mjs, stableId)"""
    import hashlib
    h = bytearray(hashlib.sha1(('domiflix-fake:' + chave).encode()).digest())
    h[6] = (h[6] & 0x0F) | 0x50
    h[8] = (h[8] & 0x3F) | 0x80
    x = h[:16].hex()
    return f'{x[:8]}-{x[8:12]}-{x[12:16]}-{x[16:20]}-{x[20:32]}'


def storage():
    uid = stable_id('user.rafael')
    return {'app_version': VERSAO, 'notification_shown_version': VERSAO, 'pwa-install-dismissed': 'true', 'theme': 'light',
            f'daily-tasks-reminder-last-shown-{uid}': HOJE, 'initial-preferences-set': 'true'}


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
        s.old = n                      # chave antiga/nome (sementes); s.n = número de hoje (fala, arquivos)
        s.n = NOVO[n]
        s.words, s.linhas, s.dur, s.estimado = carregar_voz(s.n)
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

    def upload(s, target, arquivo, at=None, label=None, **kw):
        return s._p({'do': 'upload', 'target': target, 'file': arquivo}, at, label, kw)

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
              "if(!el){out='DIFERENTE: sem elemento';}else{const t=norm(el.innerText+' '+[...el.querySelectorAll('input,textarea')].map(i=>i.value).join(' '));const falta=esp.filter(e=>!t.includes(norm(e)));"
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
            'title': f'T14 · Cap. {s.n} · {NOMES[s.n]} (narração{est} {str(round(s.dur, 1)).replace(".", ",")} s; marcas L1..L{len(s.linhas)} = início de cada '
                     f'linha do roteiro; FAKE_NOW {FAKE_NOW}; logado como Rafael Nogueira)',
            'seed': f'{AULA}-cap{s.n:02d}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
            'start': {'x': s.start[0], 'y': s.start[1]},
            'anonymous': True, 'storage': storage(),
            'seedExtra': list(SEMENTE[s.old]),
            'prewarm': ['/login'], 'setup': s.setup, 'steps': s.steps,
        }


# ---------------------------------------------------------------- alvos
MAIN = 'main'
DLG = '[role=dialog]'
ALERTA = '[role=alertdialog]'
BTN = lambda n, within=None, **kw: {'role': 'button', 'name': n, 'exact': True, **({'within': within} if within else {}), **kw}
BTNX = lambda n, within=None, **kw: {'role': 'button', 'name': n, **({'within': within} if within else {}), **kw}
TXT = lambda t, within=None, **kw: {'text': t, 'exact': True, **({'within': within} if within else {}), **kw}
SEL = lambda s, **kw: {'selector': s, **kw}
ITEM = lambda n, **kw: {'role': 'menuitem', 'name': n, **kw}
OPT = lambda n, **kw: {'role': 'option', 'name': n, **kw}
AGUARDA = {'do': 'waitFor', 'idle': True}
# lista lateral de contas (SettingsSidebarLayout): o botão da conta e, por cima dele, os "⋮" que só aparecem com o mouse na conta
CONTA = lambda nome: SEL(f'div[class*="group/tab"] button:has(span:text-is("{nome}"))')
PONTOS = lambda nome: SEL(f'div[class*="group/tab"]:has(span:text-is("{nome}")) div.absolute button')
# linha da conciliação (ReconciliationTable: uma grade de 2 colunas por linha do extrato) achada pelo memo exato
LINHA = lambda memo: f'div[class*="md:grid-cols-2"]:has(:text-is("{memo}"))'
NA_LINHA = lambda memo, botao: SEL(f'{LINHA(memo)} button:has-text("{botao}")')
DIF_CASADAS = SEL('main div:has(> p:text-is("Diferenças casadas")) button')   # o valor âmbar do rodapé abre o quadro


# o relatório do Extrato abre numa aba nova (HTML com "Salvar PDF") e a gravação filma uma aba só: o robô devolve o HTML da aba (base64) para a ilustração da edição
POPS = "(()=>{const o=window.open;window.__pops=[];window.open=function(...a){const w=o.apply(this,a);window.__pops.push(w);return w};return 'ok'})()"
HTML_JS = ("(async()=>{const w=(window.__pops||[]).slice(-1)[0];if(!w)return 'SEM JANELA';for(let i=0;i<40;i++){let h='';"
           "try{h=w.document&&w.document.body?w.document.documentElement.outerHTML:''}catch(e){return 'ERRO '+e}"
           "if(h.length>2000)return 'HTML:'+btoa(unescape(encodeURIComponent(h)));await new Promise(r=>setTimeout(r,250))}return 'SEM HTML'})()")
FECHA_POP = "(()=>{const w=(window.__pops||[]).slice(-1)[0];try{w&&w.close()}catch(e){}return 'fechada'})()"


def login():
    return [{'do': 'waitFor', 'target': {'label': 'E-mail'}, 'timeout': 30},
            {'do': 'type', 'target': {'label': 'E-mail'}, 'text': '$TUT_USER', 'cps': 40},
            {'do': 'type', 'target': {'label': 'Senha', 'exact': True}, 'text': '$TUT_SENHA', 'cps': 40},
            {'do': 'click', 'target': BTN('Entrar')},
            {'do': 'waitFor', 'text': 'Olá, Rafael!', 'timeout': 30}, AGUARDA]


def setup_mov(extra=()):
    """login, Dashboard e a tela Movimentações Financeiras (abre na Conta Principal)"""
    return login() + [{'do': 'goto', 'url': '/movimentacoes-bancarias'}, {'do': 'waitFor', 'text': 'Controle de pagamentos via Pix/Transferência', 'timeout': 30},
                      AGUARDA, {'do': 'waitFor', 'target': CONTA('Conta Principal'), 'timeout': 20}] + list(extra)


def setup_conc(extra=()):
    """... e a aba Conciliação com o extrato aberto (Continuar)"""
    return setup_mov([{'do': 'click', 'target': BTN('Conciliação')}, {'do': 'waitFor', 'text': 'Conta para conciliar', 'timeout': 20},
                      {'do': 'click', 'target': BTN('Continuar')}, {'do': 'waitFor', 'text': 'Linha do extrato', 'timeout': 20}, AGUARDA] + list(extra))


# ---------------------------------------------------------------- rolagem roteirizada (eval: o cursor não se mexe)
# Contêiner que rola de verdade: o ancestral com overflowY auto/scroll e conteúdo maior (a tabela da conciliação rola dentro de uma
# caixa de 60vh; a página rola no <main> de dentro).
ACHA_ROLAGEM = ("const rolagem=(el)=>{let c=el&&el.parentElement;while(c&&c!==document.body){const s=getComputedStyle(c);"
                "if(/(auto|scroll)/.test(s.overflowY)&&c.scrollHeight>c.clientHeight+4)return c;c=c.parentElement;}"
                "return [...document.querySelectorAll('main')].find(e=>/(auto|scroll)/.test(getComputedStyle(e).overflowY)&&e.scrollHeight>e.clientHeight+4)||null};")
SUAVE = ("await new Promise(res=>{const t0=performance.now();const f=t=>{const p=Math.min(1,(t-t0)/DUR),e=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;"
         "c.scrollTop=DESTINO;p<1?requestAnimationFrame(f):res()};requestAnimationFrame(f)});")
FOLHA = "[...document.querySelectorAll('main *')].find(e=>e.children.length===0&&e.textContent.trim()===%s)"


def js_rola_texto(texto, y=300, dur_ms=800):
    """rolagem suave do contêiner que rola a folha do DOM cujo texto é `texto` até ela ficar em y px CSS; devolve o topo final"""
    return ("(async()=>{" + ACHA_ROLAGEM + "const el=" + (FOLHA % json.dumps(texto)) + ";if(!el)return 'SEM ALVO';const c=rolagem(el);if(!c)return 'SEM ROLAGEM';"
            f"const dy=Math.round(el.getBoundingClientRect().top-{int(y)});if(Math.abs(dy)<3)return 'ok';const y0=c.scrollTop;"
            + (SUAVE.replace('DUR', str(int(dur_ms))).replace('DESTINO', 'y0+dy*e') if dur_ms else "c.scrollTop=y0+dy;")
            + "return Math.round(el.getBoundingClientRect().top)})()")


def js_main_fim(dur_ms=0):
    """leva o <main> que rola até o fim (a caixa da tabela da conciliação inteira acima do rodapé fixo); 0 = instantâneo"""
    return ("(async()=>{const c=[...document.querySelectorAll('main')].find(e=>/(auto|scroll)/.test(getComputedStyle(e).overflowY)&&e.scrollHeight>e.clientHeight+4);"
            "if(!c)return 'SEM ROLAGEM';const y0=c.scrollTop,dy=c.scrollHeight-c.clientHeight-y0;if(dy<3)return 'ok';"
            + (SUAVE.replace('DUR', str(int(dur_ms))).replace('DESTINO', 'y0+dy*e') if dur_ms else "c.scrollTop=y0+dy;") + "return 'fim:'+Math.round(c.scrollTop)})()")


def js_main_topo(dur_ms=0):
    return ("(async()=>{const c=[...document.querySelectorAll('main')].find(e=>/(auto|scroll)/.test(getComputedStyle(e).overflowY)&&e.scrollHeight>e.clientHeight+4);"
            "if(!c)return 'SEM ROLAGEM';const y0=c.scrollTop;if(y0<3)return 'ok';const dy=-y0;"
            + (SUAVE.replace('DUR', str(int(dur_ms))).replace('DESTINO', 'y0+dy*e') if dur_ms else "c.scrollTop=0;") + "return 'topo'})()")


def rola_setup(texto, y=300):
    """no setup (fora do vídeo): a linha `texto` em y, sem animação"""
    return {'do': 'eval', 'js': js_rola_texto(texto, y, 0)}


# ---------------------------------------------------------------- capítulos
def cap00():
    c = Cap(0, login(), pace=0.6)
    c.mark(1)
    c.mark(2)
    c.mark(3)
    c.hover(BTN('Financeiro'), seconds=0.8, at=c.A(3, 'caminho', 0.4), label='menu Financeiro')
    c.mark(4)
    c.hover(BTN('Financeiro'), seconds=0.6, at=c.A(4, 'tela', 0.5), label='menu Financeiro (vamos começar)')
    c.fim()
    return c


def cap01():
    c = Cap(1, login() + [{'do': 'eval', 'js': POPS}], pace=0.55)
    c.mark(1)
    c.click(BTN('Financeiro'), at=c.A(1, 'Financeiro', 1.0), label='menu Financeiro', unless={'role': 'link', 'name': 'Movimentações Financeiras'})
    c.click({'role': 'link', 'name': 'Movimentações Financeiras'}, at=c.A(1, 'Movimentações', 0.9), label='menu Movimentações Financeiras')
    c.waitfor(text='Controle de pagamentos via Pix/Transferência', timeout=20)
    c.hover(SEL('main h1:has-text("Movimentações Financeiras")'), seconds=0.8, at=c.A(1, 'nome', 0.5), label='título Movimentações Financeiras')
    c.mark(2)
    c.hover(CONTA('Resumo'), seconds=0.3, at=c.A(2, 'lado', 0.5), label='lista de contas')
    c.hover(CONTA('DINHEIRO (COFRE)'), seconds=0.3, at=c.A(2, 'saldo', 0.5), label='saldo embaixo do nome')
    c.hover(CONTA('DINHEIRO (COFRE)'), seconds=0.2, at=c.A(2, 'cofre', 0.4), label='o cofre primeiro')
    c.hover(CONTA('Conta Principal'), seconds=0.2, at=c.A(2, 'principal', 0.5), label='a conta principal')
    c.hover(CONTA('Conta Secundária'), seconds=0.15, at=c.A(2, 'outras', 0.6), label='as outras contas')
    c.mark(3)
    c.click(CONTA('Conta Principal'), at=c.A(3, 'Clicando', 0.5), label='abre a Conta Principal')
    c.hover(SEL('main div.text-4xl.font-bold'), seconds=0.4, at=c.A(3, 'saldo', 0.5), label='cartão da Conta Principal')
    c.hover(BTNX('Saque', within=MAIN), seconds=0.15, at=c.A(3, 'Saque', 0.45), label='Saque')
    c.hover(BTNX('Sangria', within=MAIN), seconds=0.15, at=c.A(3, 'Sangria', 0.45), label='Sangria')
    c.hover(BTNX('Nova Movimentação', within=MAIN), seconds=0.15, at=c.A(3, 'Nova', 0.45), label='Nova Movimentação')
    c.hover(BTNX('Extrato', within=MAIN), seconds=0.15, at=c.A(3, 'Extrato', 0.5), label='Extrato')
    c.mark(4)
    c.hover(TXT('Histórico de Movimentações', within=MAIN), seconds=0.4, at=c.A(4, 'histórico', 0.5), label='Histórico de Movimentações')
    c.hover(SEL('main button[role=combobox]:has-text("Este mês")'), seconds=0.2, at=c.A(4, 'período', 0.5), label='período Este mês')
    c.hover({'placeholder': 'Buscar por descrição ou valor...'}, seconds=0.4, at=c.A(4, 'buscar', 0.5), label='busca por descrição ou valor')
    c.hover(SEL('main button:has-text("Selecionar lançamentos")'), seconds=0.6, at=c.A(4, 'Selecionar', 0.5), label='botão Selecionar lançamentos')
    c.mark(5)
    c.click(SEL('main button[aria-label="Ver detalhes"]'), at=c.A(5, 'abre', 0.6), label='abre a linha de pedido (itens)')
    c.hover(SEL('main button[aria-label="Ocultar detalhes"]'), seconds=0.8, at=c.A(5, 'itens', 0.5), label='itens do pedido e forma de pagamento')
    c.click(SEL('main button[aria-label="Ocultar detalhes"]'), at=c.A(5, 'E', 0.7, nth=1), label='fecha a linha')
    c.hover(SEL('main button[aria-label="Ocultar valores"]'), seconds=0.8, at=c.A(5, 'olho', 0.5), label='o olho que esconde os valores')
    c.mark(6)
    c.click(BTNX('Extrato', within=MAIN), at=c.A(6, 'Extrato', 0.6), label='Extrato')
    c.waitfor(text='Exportar Extrato Bancário', timeout=10)
    c.hover({'text': 'Formato', 'exact': True, 'within': DLG}, seconds=0.5, at=c.A(6, 'PDF', 0.5), label='Formato PDF ou Excel (ZOOM Formato e Período)')
    c.click(SEL('[role=dialog] button[role=combobox]:has-text("Este mês")'), at=c.A(6, 'período', 0.6), label='lista do período')
    c.hover(OPT('Mês passado'), seconds=0.6, at=c.A(6, 'escolher', 0.4), label='Mês passado, Personalizado')
    c.press('Escape', at=c.A(6, 'contador', 0.9), label='fecha a lista')
    c.click(BTN('Exportar', within=DLG), at=c.A(6, 'arquivo', 0.6), label='Exportar o PDF (aba nova)')
    c.ev(HTML_JS, label='HTML do relatório do Extrato (aba nova, para a ilustração)', optional=True)
    c.ev(FECHA_POP, at=c.A(6, 'fechamento', 0.2), label='fecha a aba do relatório', optional=True)
    c.press('Escape', label='fecha a janela', optional=True)
    c.waitfor(gone={'role': 'dialog'}, timeout=8, optional=True)
    c.mark(7)
    c.hover(CONTA('Conta Principal'), seconds=0.4, at=c.A(7, 'Usuários', 0.5), label='lista lateral (contas liberadas)')
    c.hover(CONTA('DINHEIRO (COFRE)'), seconds=0.4, at=c.A(7, 'cofre', 0.5), label='o cofre não muda')
    c.mark(8)
    c.click(CONTA('Resumo'), at=c.A(8, 'Resumo', 0.6), label='Resumo')
    c.hover(TXT('Dinheiro e contas bancárias', within=MAIN), seconds=0.4, at=c.A(8, 'total', 0.5), label='total da empresa')
    c.hover(TXT('Dinheiro', within=MAIN), seconds=0.3, at=c.A(8, 'cofre', 0.5), label='Dinheiro (cofre)')
    c.hover(TXT('Contas bancárias', within=MAIN), seconds=0.3, at=c.A(8, 'contas', 0.5), label='Contas bancárias')
    c.mark(9)
    c.hover(BTN('Movimentações Financeiras', within=MAIN), seconds=0.4, at=c.A(9, 'Nesta', 0.5), label='aba Movimentações Financeiras')
    c.hover(BTN('Conciliação', within=MAIN), seconds=0.6, at=c.A(9, 'Conciliação', 0.5), label='aba Conciliação')
    c.fim()
    return c


def cap02():
    c = Cap(2, setup_mov(), pace=0.5)
    c.mark(1)
    c.click(BTNX('Nova Conta'), at=c.A(1, 'Nova', 0.6), label='Nova Conta')
    c.waitfor(text='Nova Conta Bancária', timeout=10)
    c.mark(2)
    c.click({'placeholder': 'Ex: Bradesco PJ'}, at=c.A(2, 'nome', 1.2), label='Nome da conta')
    c.type({'placeholder': 'Ex: Bradesco PJ'}, 'Conta Cooperativa', at=c.A(2, 'Conta', 0.05, nth=1), noClick=True, label='digita Conta Cooperativa')
    c.hover({'text': 'Selecione a instituição...', 'within': DLG}, seconds=0.6, at=c.A(2, 'instituição', 0.5), label='Instituição (opcional)')
    c.mark(3)
    c.click({'placeholder': 'R$ 0,00', 'within': DLG}, at=c.A(3, 'Valor', 0.6), label='Valor em conta')
    c.type({'placeholder': 'R$ 0,00', 'within': DLG}, '5000,00', at=c.A(3, 'cinco', 0.4), noClick=True, clear=True, label='digita 5.000,00 (ZOOM Valor em conta e Data desse saldo)')
    c.hover({'text': 'Data desse saldo', 'within': DLG}, seconds=0.6, at=c.A(3, 'data', 0.5), label='Data desse saldo')
    c.confere('dlg', ['Conta Cooperativa', 'R$ 5.000,00', 'Data desse saldo'], 'nome, valor em conta e data do saldo')
    c.mark(4)
    c.click(SEL('[role=dialog] button[style*="rgb(20, 184, 166)"]'), at=c.A(4, 'cor', 0.6), label='cor verde-azulada')
    c.mark(5)
    c.click(BTN('Criar Conta'), at=c.A(5, 'Criar', 0.6), label='Criar Conta')
    c.waitfor(text='Conta criada com sucesso', timeout=10)
    c.click(CONTA('Conta Cooperativa'), at=c.A(5, 'histórico', 0.9), label='abre a Conta Cooperativa')
    c.hover(TXT('Ajuste de saldo - Saldo inicial', within=MAIN), seconds=0.8, at=c.A(5, 'Ajuste', 0.5), label='linha do ajuste: etiqueta e valor (ZOOM)')
    c.hover(TXT('Ajuste', within=MAIN), seconds=0.6, at=c.A(5, 'receita', 0.5), label='etiqueta Ajuste')
    c.confere('main', ['Conta Cooperativa', 'R$ 5.000,00', 'Ajuste de saldo - Saldo inicial'], 'conta nova com o ajuste inicial')
    c.mark(6)
    c.hover(CONTA('Conta Cooperativa'), seconds=0.2, at=c.A(6, 'edite', 1.3), label='conta (mostra os três pontinhos)')
    c.click(PONTOS('Conta Cooperativa'), label='três pontinhos da Conta Cooperativa')
    c.click(ITEM('Editar'), label='Editar')
    c.waitfor(text='Editar Conta Bancária', timeout=10)
    c.hover({'text': 'Alterar este valor gerará um ajuste automático no saldo', 'within': DLG}, seconds=1.0, at=c.A(6, 'Correção', 0.5), label='dica do ajuste (ZOOM)')
    c.click(BTN('Cancelar', within=DLG), at=c.A(6, 'inventada', 0.6), label='Cancelar (sem salvar)')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.mark(7)
    c.hover(CONTA('Conta Cooperativa'), seconds=0.2, at=c.A(7, 'menu', 1.0), label='conta (de novo)')
    c.click(PONTOS('Conta Cooperativa'), label='três pontinhos (Tornar principal)')
    c.hover(ITEM('Tornar principal'), seconds=1.0, at=c.A(7, 'Tornar', 0.5), label='Tornar principal (sem clicar)')
    c.press('Escape', at=c.A(7, 'Aqui', 0.3), label='fecha o menu')
    c.wait(0.4)
    c.mark(8)
    c.hover(CONTA('Poupança antiga'), seconds=0.3, at=c.A(8, 'poupança', 0.5), label='Poupança antiga')
    c.click(PONTOS('Poupança antiga'), label='três pontinhos da Poupança antiga')
    c.click(ITEM('Excluir'), at=c.A(8, 'Excluir', 0.6), label='Excluir')
    c.waitfor(text='Remover conta bancária', timeout=10)
    c.hover(SEL('[role=alertdialog] button:has-text("Oculta a conta mantendo todo o histórico")'), seconds=0.4, at=c.A(8, 'Arquivar', 0.5), label='as duas opções (ZOOM)')
    c.hover(SEL('[role=alertdialog] button:has-text("Transfere transações para outra conta")'), seconds=0.6, at=c.A(8, 'Migrar', 0.5), label='Migrar e Excluir')
    c.mark(9)
    c.click(SEL('[role=alertdialog] button:has-text("Oculta a conta mantendo todo o histórico")'), at=c.A(9, 'arquivar', 0.6), label='opção Arquivar')
    c.waitfor(text='Arquivar conta', timeout=8)
    c.hover({'text': 'A conta será ocultada das listagens'}, seconds=1.0, at=c.A(9, 'listas', 0.5), label='a conta será ocultada (ZOOM)')
    c.mark(10)
    c.click(SEL('[role=alertdialog] button:text-is("Arquivar")'), at=c.A(10, 'Arquivar', 0.6), label='Arquivar')
    c.waitfor(text='Conta arquivada com sucesso', timeout=10)
    c.hover(CONTA('Conta Secundária'), seconds=0.8, at=c.A(10, 'lista', 0.5), label='a lista sem a poupança')
    c.fim()
    return c


def cap03():
    c = Cap(3, setup_mov(), pace=0.5)
    c.mark(1)
    c.mark(2)
    c.click(CONTA('DINHEIRO (COFRE)'), at=c.A(2, 'cofre', 0.6), label='DINHEIRO (COFRE)')
    c.waitfor(text='O cofre da empresa', timeout=10)
    c.hover(SEL('main p.text-3xl'), seconds=0.8, at=c.A(2, 'dezoito', 0.5), label='R$ 18.500,00 e Saldo Total em Dinheiro (ZOOM)')
    c.hover({'text': 'Disponível no cofre', 'within': MAIN}, seconds=0.5, at=c.A(2, 'aberto', 0.5), label='Disponível no cofre')
    c.confere('main', ['O cofre da empresa', 'R$ 18.500,00', 'Saldo Total em Dinheiro'], 'cofre com R$ 18.500,00')
    c.mark(3)
    c.hover(SEL('main p.text-3xl'), seconds=0.8, at=c.A(3, 'cofre', 0.5), label='o saldo que o sistema mostra')
    c.mark(4)
    c.hover(CONTA('DINHEIRO (COFRE)'), seconds=0.2, at=c.A(4, 'três', 1.1), label='cofre (mostra os três pontinhos)')
    c.click(PONTOS('DINHEIRO (COFRE)'), label='três pontinhos do cofre')
    c.hover(ITEM('Ajustar saldo'), seconds=0.3, label='Ajustar saldo (a única opção)')
    c.click(ITEM('Ajustar saldo'), at=c.A(4, 'Ajustar', 0.4), label='Ajustar saldo')
    c.waitfor(text='Saldo atual', timeout=10)
    c.hover({'text': 'Saldo atual', 'within': DLG}, seconds=0.6, at=c.A(4, 'única', 0.5), label='Saldo atual R$ 18.500,00')
    c.mark(5)
    c.click(SEL('#new-balance'), at=c.A(5, 'Novo', 1.0), label='Novo saldo')
    c.type(SEL('#new-balance'), '18560,00', at=c.A(5, 'valor', 0.3), noClick=True, clear=True, label='digita 18.560,00 (ZOOM Novo saldo e Diferença)')
    c.hover({'text': 'Diferença', 'within': DLG}, seconds=0.8, at=c.A(5, 'Diferença', 0.5), label='Diferença +R$ 60,00')
    c.confere('dlg', ['R$ 18.500,00', '+R$ 60,00'], 'saldo atual e diferença +60')
    c.mark(6)
    c.click(SEL('#motivo'), at=c.A(6, 'motivo', 0.6), label='Motivo')
    c.type(SEL('#motivo'), 'Contagem do cofre', at=c.A(6, 'obrigatório', 0.0), noClick=True, label='digita Contagem do cofre')
    c.click(BTN('Confirmar ajuste'), at=c.A(6, 'Confirmar', 0.6), label='Confirmar ajuste')
    c.waitfor(text='Saldo ajustado', timeout=10)
    c.mark(7)
    c.rolar(320, at=c.A(7, 'histórico', 0.9), label='desce ao histórico do cofre', ponto=(900, 520))
    c.hover({'text': 'Ajuste de saldo — Contagem do cofre', 'within': MAIN}, seconds=0.5, at=c.A(7, 'etiqueta', 0.6), label='a linha do ajuste')
    c.hover(TXT('Ajuste', within=MAIN), seconds=1.0, at=c.A(7, 'acerto', 0.5), label='etiqueta Ajuste')
    c.confere('main', ['R$ 18.560,00', 'Ajuste de saldo — Contagem do cofre'], 'cofre com R$ 18.560,00 e o ajuste no histórico')
    c.fim()
    return c


def cap04():
    c = Cap(4, setup_mov(), pace=0.5)
    c.mark(1)
    c.click(CONTA('Conta Principal'), at=c.A(1, 'banco', 0.6), label='Conta Principal')
    c.hover(BTNX('Nova Movimentação', within=MAIN), seconds=0.4, at=c.A(1, 'combustível', 0.5), label='combustível: Nova Movimentação')
    c.hover(CONTA('Conta Secundária'), seconds=0.4, at=c.A(1, 'Secundária', 0.5), label='dinheiro da Conta Secundária')
    c.hover(BTNX('Saque', within=MAIN), seconds=0.6, at=c.A(1, 'sacou', 0.5), label='saque no caixa eletrônico')
    c.mark(2)
    c.click(BTNX('Nova Movimentação', within=MAIN), at=c.A(2, 'Nova', 0.6), label='Nova Movimentação')
    c.waitfor(text='Nova Movimentação Financeira', timeout=10)
    c.click(BTN('Saída', within=DLG), at=c.A(2, 'Saída', 1.1), label='tipo Saída')
    c.hover({'text': 'Conta bancária', 'within': DLG}, seconds=0.5, at=c.A(2, 'Principal', 0.5), label='Conta bancária: Conta Principal')
    c.mark(3)
    c.click(SEL('#description'), at=c.A(3, 'Descrição', 0.6), label='Descrição')
    c.type(SEL('#description'), 'Combustível da picape', at=c.A(3, 'combustível', 0.05), noClick=True, label='digita Combustível da picape')
    c.click(SEL('#amount'), at=c.A(3, 'Valor', 0.6), label='Valor')
    c.type(SEL('#amount'), '350,00', at=c.A(3, 'trezentos', 0.4), noClick=True, clear=True, label='digita 350,00 (ZOOM Valor)')
    # a janela já abre com a 1ª categoria de sistema escolhida (NewBankTransactionModal.tsx:207-213): o gatilho mostra um nome, não o "Selecione"
    c.click(SEL('[role=dialog] div.space-y-2:has(> label:has-text("Categoria")) button[role=combobox]'), at=c.A(3, 'Categoria', 0.6), label='Categoria')
    c.click(OPT('Combustível', exact=True), at=c.A(3, 'Combustível', 0.5, nth=1), label='Combustível')
    c.click(SEL('#cost-center'), at=c.A(3, 'centro', 0.6), label='Centro de custo')
    c.click(OPT('Frota', exact=True), at=c.A(3, 'Frota', 0.5), label='Frota')
    c.mark(4)
    c.hover({'text': 'Não contar na DRE (saldo herdado / histórico)', 'within': DLG}, seconds=0.8, at=c.A(4, 'opção', 0.5), label='Não contar na DRE (desmarcada)')
    c.click(BTN('Salvar', within=DLG), at=c.A(4, 'Salvar', 0.6), label='Salvar')
    c.waitfor(text='Movimentação registrada com sucesso!', timeout=10)
    c.mark(5)
    c.click(BTNX('Nova Movimentação', within=MAIN), at=c.A(5, 'Entrada', 1.8), label='Nova Movimentação (Entrada)')
    c.waitfor(text='Nova Movimentação Financeira', timeout=10)
    c.hover(BTN('Entrada', within=DLG), seconds=0.4, at=c.A(5, 'Entrada', 0.5), label='tipo Entrada (verde)')
    c.hover({'text': 'Data/hora do lançamento', 'within': DLG}, seconds=0.5, at=c.A(5, 'data', 0.5), label='Data/hora do lançamento')
    c.hover({'text': 'Vincular a fornecedor/cliente (opcional)', 'within': DLG}, seconds=0.6, at=c.A(5, 'vincular', 0.5), label='vincular a cliente ou fornecedor')
    c.mark(6)
    c.mark(7)
    c.click(BTN('Transferência', within=DLG), at=c.A(7, 'transferência', 0.9), label='tipo Transferência')
    c.click(SEL('[role=dialog] button[role=combobox]', hasText='Conta Principal'), at=c.A(7, 'saiu', 0.6), label='Conta de origem')
    c.click(OPT('Conta Secundária'), at=c.A(7, 'Secundária', 0.5), label='Conta Secundária')
    c.click(SEL('[role=dialog] button[role=combobox]', hasText='Selecione a conta de destino'), at=c.A(7, 'foi', 0.6), label='Conta de destino')
    c.click(OPT('Conta Principal'), at=c.A(7, 'Principal', 0.5), label='Conta Principal')
    c.click(SEL('#amount'), at=c.A(7, 'Oito', 0.6), label='Valor da transferência')
    c.type(SEL('#amount'), '8000,00', at=c.A(7, 'mil', 0.4), noClick=True, clear=True, label='digita 8.000,00')
    c.hover({'text': 'Prévia da transferência:', 'within': DLG}, seconds=0.8, at=c.A(7, 'prévia', 0.5), label='Prévia da transferência (ZOOM)')
    c.confere('dlg', ['Conta Secundária', 'Conta Principal', 'R$ 8.000,00'], 'prévia da transferência')
    c.mark(8)
    c.click(BTN('Transferir', within=DLG), at=c.A(8, 'Transferir', 0.6), label='Transferir')
    c.waitfor(text='Transferência realizada com sucesso!', timeout=10)
    c.mark(9)
    c.click(BTNX('Saque', within=MAIN), at=c.A(9, 'saque', 0.6), label='Saque')
    c.waitfor(text='Destino do saque', timeout=10)
    c.hover({'text': 'Destino do saque', 'within': DLG}, seconds=0.6, at=c.A(9, 'cofre', 0.6), label='Destino do saque: o cofre')
    c.mark(10)
    c.click(SEL('#amount'), at=c.A(10, 'Dois', 0.9), label='Valor do Saque')
    c.type(SEL('#amount'), '2000,00', at=c.A(10, 'mil', 0.4), noClick=True, clear=True, label='digita 2.000,00 (ZOOM Saque e Tarifa)')
    c.click(SEL('[role=dialog] button[role=combobox]', hasText='Não'), at=c.A(10, 'tarifa', 0.6), label='Tem tarifa no saque?')
    c.click(OPT('Sim', exact=True), at=c.A(10, 'Sim', 0.5), label='Sim')
    c.click(SEL('#fee'), at=c.A(10, 'seis', 0.6), label='Valor da Tarifa')
    c.type(SEL('#fee'), '6,50', at=c.A(10, 'cinquenta', 0.4), noClick=True, clear=True, label='digita 6,50')
    c.mark(11)
    c.hover({'text': 'Efeitos desta transação:', 'within': DLG}, seconds=0.5, at=c.A(11, 'efeitos', 0.5), label='Efeitos desta transação (ZOOM)')
    c.hover({'text': 'Saldo da Conta Bancária', 'within': DLG}, seconds=0.6, at=c.A(11, 'banco', 0.5), label='banco perde saque + tarifa')
    c.hover({'text': 'Cofre (Conta DINHEIRO)', 'exact': True, 'within': DLG, 'nth': 'last'}, seconds=0.6, at=c.A(11, 'cofre', 0.5), label='cofre ganha só o saque')
    c.confere('dlg', ['Saque: R$ 2.000,00 + Tarifa: R$ 6,50', 'Aumentará em R$ 2.000,00'], 'efeitos do saque')
    c.mark(12)
    c.click(BTN('Confirmar Saque'), at=c.A(12, 'Confirmar', 0.6), label='Confirmar Saque')
    c.waitfor(text='Saque realizado com sucesso!', timeout=10)
    c.hover(BTNX('Sangria', within=MAIN), seconds=0.8, at=c.A(12, 'Sangria', 0.5), label='Sangria, aqui do lado')
    c.mark(13)
    c.hover(BTNX('Saque', within=MAIN), seconds=1.0, at=c.A(13, 'saque', 0.5), label='Saque (dica do caixa aberto)')
    c.fim()
    return c


def cap05():
    c = Cap(5, setup_mov(), pace=0.5)
    c.mark(1)
    c.mark(2)
    c.mark(3)
    c.mark(4)
    c.click(BTN('Conciliação', within=MAIN), at=c.A(4, 'Conciliação', 0.6), label='aba Conciliação')
    c.waitfor(text='Nenhum extrato em conciliação', timeout=15)
    c.hover(SEL('main button[role=combobox]:has-text("Conta Principal")'), seconds=0.6, at=c.A(4, 'escolhida', 0.5), label='Conta para conciliar: Conta Principal')
    c.mark(5)
    c.click(BTN('Como funciona?'), at=c.A(5, 'Como', 0.6), label='Como funciona?')
    c.waitfor(text='Como funciona a conciliação bancária', timeout=10)
    c.hover(TXT('O que é conciliar?', within=DLG), seconds=1.0, at=c.A(5, 'explica', 1.0), label='O que é conciliar? (ZOOM)')
    c.press('Escape', at=c.A(5, 'Primeiro', 0.3), label='fecha o Como funciona')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.fim()
    return c


def cap06():
    c = Cap(6, setup_mov([{'do': 'click', 'target': BTN('Conciliação')}, {'do': 'waitFor', 'text': 'Nenhum extrato em conciliação', 'timeout': 20}, AGUARDA]), pace=0.5)
    c.mark(1)
    c.mark(2)
    c.click(BTN('Importar novo extrato'), at=c.A(2, 'Importar', 0.6), label='Importar novo extrato')
    c.waitfor(text='Importar extrato OFX', timeout=10)
    c.click(TXT('Como pegar o arquivo do seu banco?', within=DLG), at=c.A(2, 'ensina', 1.2), label='Como pegar o arquivo do seu banco?')
    c.hover({'text': 'Escolha o formato OFX', 'within': DLG}, seconds=1.2, at=c.A(2, 'alguns', 0.5), label='passo a passo (ZOOM)')
    c.mark(3)
    c.upload(TXT('Arraste o arquivo .ofx aqui ou clique para selecionar', within=DLG), 'arquivos/Extrato_20261101_20261110.ofx', at=c.A(3, 'Escolho', 0.7),
             label='entrega o Extrato_20261101_20261110.ofx')
    c.waitfor(text='Prévia do extrato', timeout=10)
    c.mark(4)
    c.hover(TXT('Prévia do extrato', within=DLG), seconds=0.3, at=c.A(4, 'prévia', 0.5), label='Prévia do extrato')
    c.hover(TXT('Período', within=DLG), seconds=0.3, at=c.A(4, 'período', 0.5), label='Período, Transações e Saldo final (ZOOM)')
    c.hover(TXT('Transações', within=DLG), seconds=0.3, at=c.A(4, 'dezessete', 0.5), label='Transações 17')
    c.hover(TXT('Saldo final do extrato', within=DLG), seconds=0.6, at=c.A(4, 'saldo', 0.5), label='Saldo final do extrato')
    c.confere('dlg', ['01/11/2026 — 10/11/2026', '17', 'R$ 44.933,47'], 'prévia: período, 17 transações e saldo final')
    c.mark(5)
    c.click(BTN('Importar', within=DLG), at=c.A(5, 'Importar', 0.6), label='Importar')
    c.waitfor(text='17 de 17 linhas importadas', timeout=15)
    c.hover(TXT('Tudo certo — nenhuma linha estava repetida.', within=DLG), seconds=0.8, at=c.A(5, 'reconhece', 0.5), label='nenhuma linha repetida')
    c.click(BTN('Concluir'), at=c.A(5, 'duplica', 0.6), label='Concluir')
    c.waitfor(text='Linha do extrato', timeout=15)
    c.mark(6)
    c.ev(js_main_fim(600), at=c.A(6, 'Pronto', 0.3), label='desce a página até a tabela')
    c.hover(TXT('PIX ENVIADO DEPOSITO IRMAOS SIQUEIRA', within=MAIN), seconds=0.3, at=c.A(6, 'esquerda', 0.5), label='linha do banco (esquerda)')
    c.hover(TXT('−R$ 2.250,00', within=MAIN), seconds=0.3, at=c.A(6, 'valor', 0.5), label='data e valor da linha')
    c.hover(TXT('Casa com um lançamento no sistema', within=MAIN), seconds=0.6, at=c.A(6, 'direita', 0.5), label='o que fazer com ela (direita)')
    c.mark(7)
    c.ev(js_rola_texto('PIX RECEBIDO SERRA FINA ALUMINIO', 330, 900), at=c.A(7, 'repara', 0.9), label='rola até o Pix da Serra Fina')
    c.hover(TXT('+R$ 4.815,00', within=MAIN), seconds=0.5, at=c.A(7, 'verde', 0.5), label='entrada em verde, com mais')
    c.hover(TXT('−R$ 180,00', within=MAIN), seconds=0.6, at=c.A(7, 'vermelho', 0.5), label='saída em vermelho, com menos')
    c.mark(8)
    c.hover(TXT('Saldo do banco', within=MAIN), seconds=0.4, at=c.A(8, 'rodapé', 0.5), label='rodapé: os três números')
    c.hover(TXT('Diferença', within=MAIN), seconds=0.4, at=c.A(8, 'três', 0.4), label='Diferença')
    c.hover(BTN('Finalizar conciliação'), seconds=0.6, at=c.A(8, 'fim', 0.5), label='Finalizar conciliação (desabilitado)')
    c.confere('main', ['Saldo do banco', 'R$ 44.933,47', 'Ainda há 17 linhas pendentes'], 'rodapé depois da importação')
    c.fim()
    return c


SIQ, ALUG, APAR, VFORTE = 'PIX ENVIADO DEPOSITO IRMAOS SIQUEIRA', 'PIX ENVIADO ALUGUEL GALPAO NOV', 'PIX ENVIADO APARECIDA RAMOS', 'PIX ENVIADO AUTO PECAS VALE FORTE'
AGUA, SERRA, PNEU, TARIFA = 'PAGTO BOLETO AGUA E ESGOTO', 'PIX RECEBIDO SERRA FINA ALUMINIO', 'PIX ENVIADO BORRACHARIA DOIS IRMAOS', 'TARIFA PACOTE SERVICOS'
AVULSA, ESTORNO, ENERGIA, MORETTI = 'TARIFA AVULSA', 'ESTORNO TARIFA AVULSA', 'PIX ENVIADO CONCESSIONARIA ENERGIA', 'PIX ENVIADO HIDRAULICA MORETTI LTDA'
POSTO, ACOS, TRANSF, SAQUE, TSAQUE = ('PIX ENVIADO AUTO POSTO BOA VIAGEM', 'PIX RECEBIDO ACOS QUIRIRIM LTDA', 'PIX RECEBIDO RECICLA VALE METAIS LTDA',
                                      'SAQUE CAIXA ELETRONICO', 'TARIFA SAQUE')
MEMO = lambda m: SEL(f'{LINHA(m)} :text-is("{m}")')


def conc(memo, y=250):
    """setup dos capítulos da conciliação: extrato aberto, página no fim (a caixa da tabela inteira acima do rodapé) e a linha do capítulo em y"""
    return setup_conc([{'do': 'eval', 'js': js_main_fim()}, {'do': 'wait', 'seconds': 0.3}, rola_setup(memo, y), {'do': 'wait', 'seconds': 0.4}])


def confirma(c, memo, at=None, label=None, y=300):
    """sugestão verde de uma linha: rola até ela e clica em Confirmar / Casar com ..."""
    c.ev(js_rola_texto(memo, y, 500), at=at, label=f'rola até {memo}')
    c.click(SEL(f'{LINHA(memo)} button:has-text("Confirmar"), {LINHA(memo)} button:has-text("Casar com ")'), label=label or f'Confirmar ({memo})')
    c.waitfor(target=SEL(f'{LINHA(memo)} :text-is("Casada")'), timeout=10)


def cap07():
    c = Cap(7, conc(SIQ, 250), pace=0.5)
    c.mark(1)
    c.hover(MEMO(SIQ), seconds=0.4, at=c.A(1, 'linha', 0.5), label='Pix do Depósito Irmãos Siqueira')
    c.hover(SEL(f'{LINHA(SIQ)} :text-is("Casa com um lançamento no sistema")'), seconds=1.0, at=c.A(1, 'achou', 0.5), label='sugestão da compra (ZOOM)')
    c.confere('main', ['PIX ENVIADO DEPOSITO IRMAOS SIQUEIRA', '−R$ 2.250,00', 'Depósito Irmãos Siqueira', '03/11/2026'], 'Pix de 2.250,00 e a compra do dia 3')
    c.mark(2)
    c.hover(SEL(f'{LINHA(SIQ)} :text("Depósito Irmãos Siqueira")'), seconds=0.4, at=c.A(2, 'parceiro', 0.5), label='data e parceiro')
    c.click(NA_LINHA(SIQ, 'Casar com'), at=c.A(2, 'caso', 0.6), label='Casar com Compra (Depósito Irmãos Siqueira)')
    c.waitfor(target=SEL(f'{LINHA(SIQ)} :text-is("Casada")'), timeout=10)
    c.mark(3)
    confirma(c, ALUG, at=c.A(3, 'outras', 0.9), label='Confirmar o aluguel')
    for m in (PNEU, ENERGIA, MORETTI, POSTO, ACOS, SAQUE, TSAQUE):
        confirma(c, m)
    c.mark(4)
    c.ev(js_rola_texto(TRANSF, 260, 600), label='rola até os oito mil')
    c.hover(MEMO(TRANSF), seconds=0.4, at=c.A(4, 'oito', 0.5), label='Pix de 8.000,00 da Conta Secundária')
    c.hover(SEL(f'{LINHA(TRANSF)} :text-is("Transferência: Conta Secundária → Conta Principal")'), seconds=0.6, at=c.A(4, 'transferência', 0.5),
            label='a transferência registrada')
    c.mark(5)
    c.click(NA_LINHA(TRANSF, 'Mais ações'), at=c.A(5, 'Mais', 0.6), label='Mais ações (linha da transferência)')
    c.click(ITEM('Casar com transferência'), at=c.A(5, 'Casar', 0.6), label='Casar com transferência')
    c.waitfor(text='Escolha a transferência entre suas contas que corresponde às linhas do extrato.', timeout=10)
    c.hover(SEL('[role=dialog] :text("Conta Secundária → Conta Principal")'), seconds=0.6, at=c.A(5, 'certa', 1.0), label='a candidata (ZOOM)')
    c.click(SEL('[role=dialog] :text("Conta Secundária → Conta Principal")'), label='marca a candidata')
    c.hover({'text': 'Isso só cria o vínculo da conciliação', 'within': DLG}, seconds=0.6, label='só cria o vínculo')
    c.confere('dlg', ['+R$ 8.000,00', 'Conta Secundária', 'Conta Principal'], 'candidata da transferência de 8.000,00')
    c.mark(6)
    c.click(BTN('Casar transferência'), at=c.A(6, 'Casar', 0.6), label='Casar transferência')
    c.waitfor(target=SEL(f'{LINHA(TRANSF)} :text-is("Casada")'), timeout=10)
    c.hover(SEL(f'{LINHA(TRANSF)} :text-is("Casada")'), seconds=0.8, at=c.A(6, 'liga', 0.5), label='selo Casada')
    c.mark(7)
    c.hover(MEMO(TRANSF), seconds=1.0, at=c.A(7, 'dica', 0.5), label='dica: transferência')
    c.fim()
    return c


def cap08():
    c = Cap(8, conc(AGUA, 250), pace=0.5)
    c.mark(1)
    c.hover(MEMO(AGUA), seconds=0.5, at=c.A(1, 'boleto', 0.5), label='boleto da água')
    c.hover(SEL(f'{LINHA(AGUA)} :text-is("−R$ 238,40")'), seconds=0.6, at=c.A(1, 'duzentos', 0.5), label='R$ 238,40')
    c.mark(2)
    c.click(NA_LINHA(AGUA, 'Baixar conta'), at=c.A(2, 'Baixar', 0.6), label='Baixar conta')
    c.click(SEL(f'{LINHA(AGUA)} [role=combobox]'), at=c.A(2, 'lista', 1.0), label='Selecione a conta')
    c.hover(OPT('Água e esgoto de outubro'), seconds=0.6, at=c.A(2, 'água', 0.5), label='Água e esgoto de outubro')
    c.click(OPT('Água e esgoto de outubro'), label='escolhe a água')
    c.confere('main', ['−R$ 238,40', 'Dar baixa de R$ 238,40'], 'boleto de 238,40')
    c.mark(3)
    c.click(NA_LINHA(AGUA, 'Dar baixa'), at=c.A(3, 'Dar', 0.6), label='Dar baixa de R$ 238,40 (ZOOM)')
    c.waitfor(target=SEL(f'{LINHA(AGUA)} :text-is("Baixada")'), timeout=10)
    c.hover(SEL(f'{LINHA(AGUA)} :text-is("Baixada")'), seconds=0.8, at=c.A(3, 'Baixada', 0.5), label='selo Baixada')
    c.mark(4)
    c.hover(SEL(f'{LINHA(AGUA)} :text-is("Baixada")'), seconds=1.0, at=c.A(4, 'inteiro', 0.5), label='baixa do valor inteiro')
    c.fim()
    return c


def cap09():
    c = Cap(9, conc(TARIFA, 250), pace=0.5)
    c.mark(1)
    c.hover(MEMO(TARIFA), seconds=0.5, at=c.A(1, 'linha', 0.5), label='tarifa do pacote')
    c.hover(SEL(f'{LINHA(TARIFA)} :text-is("−R$ 64,90")'), seconds=0.6, at=c.A(1, 'sessenta', 0.5), label='R$ 64,90')
    c.mark(2)
    c.click(NA_LINHA(TARIFA, 'Mais ações'), at=c.A(2, 'Mais', 0.6), label='Mais ações (todos os destinos)')
    c.hover(ITEM('Funcionário'), seconds=0.6, at=c.A(2, 'Funcionário', 0.5), label='Funcionário')
    c.hover(ITEM('Ajuste'), seconds=1.0, at=c.A(2, 'Ajuste', 0.5), label='Ajuste (não contar na DRE)')
    c.hover(ITEM('Saldo do cliente/fornecedor'), seconds=0.8, at=c.A(2, 'Saldo', 0.5), label='Saldo do cliente ou fornecedor (fiado)')
    c.mark(3)
    c.hover(ITEM('Buscar lançamento'), seconds=0.5, at=c.A(3, 'Buscar', 0.5), label='Buscar lançamento')
    c.hover(ITEM('Funcionário'), seconds=0.5, at=c.A(3, 'painel', 0.5), label='o painel do Funcionário')
    c.press('Escape', at=c.A(3, 'lembra', 0.2), label='fecha o menu')
    c.wait(0.5)
    c.mark(4)
    c.click(NA_LINHA(TARIFA, 'Criar despesa'), at=c.A(4, 'Criar', 0.6), label='Criar despesa')
    c.waitfor(text='Criar lançamento de saída', timeout=10)
    c.hover(SEL(f'{LINHA(TARIFA)} input', nth='last'), seconds=0.5, at=c.A(4, 'descrição', 0.5), label='Descrição vem do extrato')
    c.hover(SEL(f'{LINHA(TARIFA)} [role=switch]'), seconds=0.6, at=c.A(4, 'chave', 0.5), label='Não é receita nem despesa (desligada)')
    c.mark(5)
    c.click(SEL(f'{LINHA(TARIFA)} [role=combobox]', hasText='Selecione a categoria'), at=c.A(5, 'categoria', 0.6), label='Categoria')
    c.click(OPT('Tarifas', exact=True), at=c.A(5, 'Tarifas', 0.6), label='Tarifas')
    c.confere('main', ['−R$ 64,90', 'Criar R$ 64,90'], 'tarifa de 64,90')
    c.hover(NA_LINHA(TARIFA, 'Criar R$ 64,90'), seconds=0.6, at=c.A(5, 'botão', 0.5), label='Categoria Tarifas e o botão Criar R$ 64,90 (ZOOM)')
    c.mark(6)
    c.click(NA_LINHA(TARIFA, 'Criar R$ 64,90'), at=c.A(6, 'Criar', 0.6), label='Criar R$ 64,90')
    c.waitfor(target=SEL(f'{LINHA(TARIFA)} :text-is("Criada")'), timeout=10)
    c.hover(SEL(f'{LINHA(TARIFA)} :text-is("Criada")'), seconds=0.8, at=c.A(6, 'Criada', 0.5), label='selo Criada')
    c.fim()
    return c


def cap10():
    c = Cap(10, conc(SERRA, 250), pace=0.5)
    c.mark(1)
    c.hover(MEMO(SERRA), seconds=0.4, at=c.A(1, 'Pix', 0.5), label='Pix da Serra Fina')
    c.hover(SEL(f'{LINHA(SERRA)} :text-is("+R$ 4.815,00")'), seconds=0.4, at=c.A(1, 'quatro', 0.5), label='R$ 4.815,00')
    c.hover(SEL(f'{LINHA(SERRA)} :text("Sem casamento automático")'), seconds=0.6, at=c.A(1, 'nada', 0.5), label='sem sugestão')
    c.mark(2)
    c.mark(3)
    c.hover(NA_LINHA(SERRA, 'Criar receita'), seconds=0.4, at=c.A(3, 'criar', 0.5), label='Criar receita (não)')
    c.click(NA_LINHA(SERRA, 'Mais ações'), at=c.A(3, 'Mais', 0.6), label='Mais ações')
    c.click(ITEM('Buscar lançamento'), at=c.A(3, 'Buscar', 0.6), label='Buscar lançamento')
    c.mark(4)
    c.click({'placeholder': 'Nome do cliente/fornecedor, nº do pedido...'}, at=c.A(4, 'Digito', 0.7), label='campo da busca')
    c.type({'placeholder': 'Nome do cliente/fornecedor, nº do pedido...'}, 'Serra', at=c.A(4, 'Serra', 0.05), noClick=True, label='digita Serra')
    c.hover({'text': 'Mostra lançamentos de R$ 4.815,00', 'within': MAIN}, seconds=0.5, at=c.A(4, 'busca', 0.5), label='até R$ 2,00 de diferença')
    c.hover(SEL(f'{LINHA(SERRA)} [aria-label="Lançamentos encontrados"] :text("Serra Fina")'), seconds=0.6, at=c.A(4, 'venda', 0.5), label='a venda com dif. −R$ 0,20 (ZOOM)')
    c.click(SEL(f'{LINHA(SERRA)} [aria-label="Lançamentos encontrados"] :text("Serra Fina")'), label='marca a venda')
    c.confere('main', ['+R$ 4.815,00', '+R$ 4.815,20', 'dif. −R$ 0,20', '03/11/2026'], 'Pix de 4.815,00 e a venda de 4.815,20 do dia 3')
    c.mark(5)
    c.click(NA_LINHA(SERRA, 'Casar com selecionado'), at=c.A(5, 'Casar', 0.6), label='Casar com selecionado')
    c.waitfor(text='Casar com valor diferente?', timeout=10)
    c.hover(TXT('Casar com valor diferente?'), seconds=0.6, at=c.A(5, 'confirma', 0.5), label='Casar com valor diferente?')
    c.mark(6)
    c.click(BTN('Casar assim'), at=c.A(6, 'Casar', 1.0), label='Casar assim')
    c.waitfor(target=SEL(f'{LINHA(SERRA)} :text-is("Casada")'), timeout=10)
    c.hover(DIF_CASADAS, seconds=0.8, at=c.A(6, 'rodapé', 0.5), label='Diferenças casadas (ZOOM)')
    c.mark(7)
    c.hover(SEL(f'{LINHA(SERRA)} :text-is("Casada")'), seconds=1.2, at=c.A(7, 'aviso', 0.5), label='selo Casada (dica dos avisos automáticos)')
    c.fim()
    return c


def cap11():
    c = Cap(11, conc(AVULSA, 250), pace=0.5)
    c.mark(1)
    c.hover(MEMO(AVULSA), seconds=0.4, at=c.A(1, 'linhas', 0.5), label='tarifa avulsa')
    c.hover(MEMO(ESTORNO), seconds=0.6, at=c.A(1, 'devolveu', 0.5), label='estorno da tarifa')
    c.mark(2)
    c.mark(3)
    c.click(SEL(f'{LINHA(AVULSA)} button[role=checkbox]'), at=c.A(3, 'Marco', 0.6), label='marca a tarifa avulsa')
    c.click(SEL(f'{LINHA(ESTORNO)} button[role=checkbox]'), label='marca o estorno')
    c.hover({'text': 'Soma: +R$ 0,00', 'within': MAIN}, seconds=0.6, at=c.A(3, 'soma', 0.5), label='2 selecionadas e Soma: +R$ 0,00 (ZOOM)', noScroll=True)
    c.confere('main', ['2 selecionadas', 'Soma: +R$ 0,00', '−R$ 12,00', '+R$ 12,00'], 'tarifa e estorno de 12,00, soma zero')
    c.mark(4)
    c.click(BTN('Ignorar (2)'), at=c.A(4, 'Ignorar', 0.6), label='Ignorar (2)')
    c.waitfor(text='Ignorar 2 linhas?', timeout=10)
    c.click(SEL('[role=alertdialog] button:text-is("Ignorar"), [role=dialog] button:text-is("Ignorar")'), at=c.A(4, 'confirma', 1.0), label='confirma Ignorar')
    c.waitfor(target=SEL(f'{LINHA(AVULSA)} :text-is("Ignorada")'), timeout=10)
    c.hover(SEL(f'{LINHA(AVULSA)} :text-is("Ignorada")'), seconds=0.6, at=c.A(4, 'Ignorada', 0.5), label='selo Ignorada')
    c.mark(5)
    c.hover(SEL(f'{LINHA(ESTORNO)} :text-is("Ignorada")'), seconds=1.0, at=c.A(5, 'dica', 0.5), label='as duas ignoradas')
    c.fim()
    return c


def cap12():
    c = Cap(12, conc(APAR, 250), pace=0.5)
    c.mark(1)
    c.hover(SEL(f'{LINHA(APAR)} :text("Atenção: há 2 lançamentos")'), seconds=0.6, at=c.A(1, 'parecidas', 0.5), label='aviso âmbar da primeira linha (ZOOM)')
    c.hover(MEMO(APAR), seconds=0.3, at=c.A(1, 'Um', 0.5), label='Pix de um')
    c.hover(MEMO(VFORTE), seconds=0.6, at=c.A(1, 'outro', 0.5), label='Pix do outro')
    c.confere('main', ['há 2 lançamentos de R$ 380,00', 'PIX ENVIADO APARECIDA RAMOS', 'PIX ENVIADO AUTO PECAS VALE FORTE'], 'dois Pix de 380,00')
    c.mark(2)
    c.mark(3)
    c.click(NA_LINHA(APAR, 'Escolher lançamento'), at=c.A(3, 'Escolher', 0.6), label='Escolher lançamento')
    c.hover(SEL(f'{LINHA(APAR)} [aria-label="Lançamentos que podem casar"]'), seconds=0.5, at=c.A(3, 'lista', 0.5), label='as duas compras')
    c.hover(MEMO(APAR), seconds=0.3, at=c.A(3, 'extrato', 0.5), label='o nome no extrato')
    c.hover(SEL(f'{LINHA(APAR)} [aria-label="Lançamentos que podem casar"] :text("Aparecida Ramos")'), seconds=0.5, at=c.A(3, 'qual', 0.4), label='a compra da Aparecida')
    c.mark(4)
    c.click(SEL(f'{LINHA(APAR)} [aria-label="Lançamentos que podem casar"] :text("Aparecida Ramos")'), at=c.A(4, 'Marco', 0.6), label='marca a compra da Aparecida')
    c.click(NA_LINHA(APAR, 'Casar com o selecionado'), at=c.A(4, 'Casar', 0.6), label='Casar com o selecionado')
    c.waitfor(target=SEL(f'{LINHA(APAR)} :text-is("Casada")'), timeout=10)
    c.mark(5)
    c.hover(SEL(f'{LINHA(VFORTE)} :text-is("Casa com um lançamento no sistema")'), seconds=0.6, at=c.A(5, 'outra', 0.5), label='a outra linha com a sugestão certa')
    c.click(NA_LINHA(VFORTE, 'Casar com'), at=c.A(5, 'casar', 0.6), label='Casar com Compra (Auto Peças Vale Forte)')
    c.waitfor(target=SEL(f'{LINHA(VFORTE)} :text-is("Casada")'), timeout=10)
    c.mark(6)
    c.hover(SEL(f'{LINHA(APAR)} :text-is("Casada")'), seconds=0.5, at=c.A(6, 'dica', 0.5), label='os dois selos Casada')
    c.hover(SEL(f'{LINHA(VFORTE)} :text-is("Casada")'), seconds=0.8, at=c.A(6, 'nome', 0.5), label='Casada (Auto Peças)')
    c.fim()
    return c


def cap13():
    c = Cap(13, conc(SIQ, 250), pace=0.5)
    c.mark(1)
    c.hover(SEL(f'{LINHA(SIQ)} :text-is("Casada")'), seconds=0.4, at=c.A(1, 'resolvida', 0.5), label='linha resolvida')
    c.click(NA_LINHA(SIQ, 'Desfazer'), at=c.A(1, 'Desfazer', 0.6), label='Desfazer (Casada)')
    c.waitfor(target=NA_LINHA(SIQ, 'Casar com'), timeout=10)
    c.mark(2)
    c.click(NA_LINHA(SIQ, 'Casar com'), at=c.A(2, 'caso', 0.6), label='casa de novo')
    c.waitfor(target=SEL(f'{LINHA(SIQ)} :text-is("Casada")'), timeout=10)
    c.mark(3)
    c.ev(js_rola_texto(TARIFA, 280, 800), at=c.A(3, 'Criada', 0.9), label='rola até a Criada')
    c.hover(SEL(f'{LINHA(TARIFA)} :text-is("Criada")'), seconds=0.4, at=c.A(3, 'Baixada', 0.3), label='selo Criada')
    c.hover(NA_LINHA(TARIFA, 'Desfazer'), seconds=1.0, at=c.A(3, 'confirmação', 0.5), label='Desfazer da Criada (pede confirmação)')
    c.mark(4)
    c.click(BTN('Cancelar conciliação'), at=c.A(4, 'Cancelar', 0.6), label='Cancelar conciliação')
    c.waitfor(text='Cancelar esta conciliação?', timeout=10)
    c.hover({'text': 'vínculo(s) com lançamento existente', 'within': DLG}, seconds=0.6, at=c.A(4, 'vínculos', 0.8), label='o que volta (ZOOM)')
    c.hover({'placeholder': 'CANCELAR'}, seconds=0.6, at=c.A(4, 'digitar', 0.5), label='Digite CANCELAR para confirmar')
    c.confere('dlg', ['17 linha(s) do extrato serão canceladas', '13 vínculo(s)', '1 conta(s) a pagar/receber', '1 lançamento(s) criado(s)', '2 linha(s) ignorada(s)'],
              'o que o cancelamento reverte')
    c.click(BTN('Manter conciliação'), at=c.A(4, 'mantenho', 0.6), label='Manter conciliação')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.mark(5)
    c.ev(js_main_topo(500), label='sobe a página')
    c.click(BTN('Voltar'), at=c.A(5, 'Voltar', 0.6), label='Voltar')
    c.waitfor(text='Continuar conciliação', timeout=10)
    c.hover({'text': 'Continuar conciliação', 'within': MAIN}, seconds=0.6, at=c.A(5, 'progresso', 0.5), label='Continuar conciliação')
    c.click(BTN('Continuar'), at=c.A(5, 'Continuar', 0.6), label='Continuar')
    c.waitfor(text='Linha do extrato', timeout=10)
    c.mark(6)
    c.ev(js_main_fim(600), at=c.A(6, 'dica', 0.3), label='desce até a tabela')
    c.hover(SEL(f'{LINHA(SIQ)} :text-is("Casada")'), seconds=1.0, at=c.A(6, 'Excluir', 0.5), label='lançamento conciliado')
    c.fim()
    return c


def cap14():
    c = Cap(14, conc(SIQ, 250), pace=0.5)
    c.mark(1)
    c.hover(TXT('Saldo do banco', within=MAIN), seconds=0.5, at=c.A(1, 'Saldo', 0.5), label='Saldo do banco e Saldo conciliado (ZOOM)')
    c.hover(TXT('Saldo conciliado', within=MAIN), seconds=0.6, at=c.A(1, 'conciliado', 0.5), label='Saldo conciliado')
    c.mark(2)
    c.hover(TXT('Diferença', within=MAIN), seconds=0.8, at=c.A(2, 'zero', 0.5), label='Diferença R$ 0,00')
    c.confere('main', ['R$ 44.933,47', 'R$ 0,00', 'Diferenças casadas'], 'rodapé: banco = conciliado, diferença zero')
    c.mark(3)
    c.click(DIF_CASADAS, at=c.A(3, 'vinte', 0.6), label='Diferenças casadas')
    c.waitfor(text='Diferenças de valor casadas', timeout=8)
    c.confere('body', ['Diferenças de valor casadas', 'R$ 4.815,00', 'R$ 4.815,20'], 'os 20 centavos da Serra Fina')
    c.press('Escape', at=c.A(3, 'travam', 0.2), label='fecha o quadro')
    c.mark(4)
    c.hover(BTN('Finalizar conciliação'), seconds=1.0, at=c.A(4, 'dica', 0.5), label='Finalizar conciliação habilitado')
    c.mark(5)
    c.click(BTN('Finalizar conciliação'), at=c.A(5, 'Finalizar', 0.6), label='Finalizar conciliação')
    c.waitfor(text='Conciliação finalizada', timeout=10)
    c.ev(js_main_topo(500), label='sobe a página')
    c.hover({'text': 'Conciliação finalizada', 'within': MAIN}, seconds=0.6, at=c.A(5, 'selado', 0.5), label='faixa Conciliação finalizada')
    c.mark(6)
    c.click(BTN('Fechar', within=MAIN), at=c.A(6, 'Ele', 0.6), label='Fechar')
    c.click({'text': 'Conciliações anteriores (1)', 'within': MAIN}, at=c.A(6, 'anteriores', 0.6), label='Conciliações anteriores (1)')
    c.hover({'text': 'Conciliado', 'exact': True, 'within': MAIN}, seconds=0.8, at=c.A(6, 'Conciliado', 0.5), label='selo Conciliado')
    c.fim()
    return c


# ---------------------------------------------------------------- capítulos novos (1.60.18)
def cap_cartao():
    """cap03 · O cartão de crédito da empresa (variante: parte de apos-cap02; o cartão criado não segue adiante)"""
    c = Cap('cartao', setup_mov(), pace=0.5)
    c.mark(1)
    c.click(BTNX('Novo Cartão'), at=c.A(1, 'Novo', 0.6), label='Novo Cartão')
    c.waitfor(text='Novo Cartão de Crédito', timeout=10)
    c.mark(2)
    c.click(SEL('#card-name'), at=c.A(2, 'nome', 0.6), label='Nome do cartão')
    c.type(SEL('#card-name'), 'Cartão Empresa', at=c.A(2, 'nome', 0.0), noClick=True, label='digita Cartão Empresa')
    c.click(SEL('#card-closing-day'), at=c.A(2, 'fecha', 0.6), label='Dia do fechamento')
    c.type(SEL('#card-closing-day'), '25', at=c.A(2, 'vinte', 0.4), noClick=True, label='digita 25')
    c.click(SEL('#card-due-day'), at=c.A(2, 'vence', 0.6, nth=1), label='Dia do vencimento')
    c.type(SEL('#card-due-day'), '5', at=c.A(2, 'cinco', 0.4, nth=1), noClick=True, label='digita 5')
    c.hover({'text': 'A fatura que fecha no dia 25 vence no dia 5', 'within': DLG}, seconds=1.0, at=c.A(2, 'explica', 0.6), label='a frase da fatura (ZOOM)')
    c.confere('dlg', ['Cartão Empresa', 'A fatura que fecha no dia 25 vence no dia 5 do mês seguinte'], 'nome, fechamento e vencimento')
    c.mark(3)
    c.click(SEL('#card-limit'), at=c.A(3, 'limite', 0.6), label='Limite do cartão')
    c.type(SEL('#card-limit'), '10000,00', at=c.A(3, 'opcional', 0.3), noClick=True, clear=True, label='digita 10.000,00')
    c.confere('dlg', ['R$ 10.000,00'], 'limite de 10.000,00')
    c.click(BTN('Criar Cartão', within=DLG), at=c.A(3, 'Criar', 0.6), label='Criar Cartão')
    c.waitfor(gone={'role': 'dialog'}, timeout=10)
    c.mark(4)
    c.click(CONTA('Cartão Empresa'), at=c.A(4, 'Ele', 0.6), label='abre o Cartão Empresa')
    c.hover(TXT('Fatura em aberto', within=MAIN), seconds=0.6, at=c.A(4, 'fatura', 0.5), label='Fatura em aberto')
    c.hover(SEL('main :text("Limite total:")'), seconds=0.4, at=c.A(4, 'limite', 0.5), label='Limite total e Disponível')
    c.confere('main', ['Fatura em aberto', 'R$ 0,00', 'Limite total:', 'R$ 10.000,00', 'fecha dia 25 · vence dia 5'], 'cartão novo: fatura zerada e limite')
    c.mark(5)
    c.click(BTNX('Nova despesa', within=MAIN), at=c.A(5, 'Nova', 0.6), label='Nova despesa')
    c.waitfor(target=SEL('#description'), timeout=10)
    c.click(SEL('#description'), at=c.A(5, 'comecei', 1.0), label='Descrição')
    c.type(SEL('#description'), 'Con', at=c.A(5, 'comecei', 0.05), noClick=True, label='digita Con')
    c.waitfor(text='Padrão encontrado: Conserto do pneu da empilhadeira', timeout=12)
    c.hover({'text': 'Padrão encontrado', 'within': DLG}, seconds=0.8, at=c.A(5, 'lembrou', 0.5), label='o padrão encontrado (ZOOM)')
    c.confere('dlg', ['Padrão encontrado: Conserto do pneu da empilhadeira', 'Preencher'], 'sugestão do conserto do pneu')
    c.mark(6)
    c.click(BTN('Preencher', within=DLG), at=c.A(6, 'Preencher', 0.6), label='Preencher')
    c.waitfor(text='Campos preenchidos.', timeout=8)
    c.hover({'text': 'Campos preenchidos.', 'within': DLG}, seconds=0.8, at=c.A(6, 'respeita', 0.5), label='Pagou com e a frase (ZOOM)')
    c.confere('dlg', ['Cartão Empresa', 'Campos preenchidos.', 'Desfazer preenchimento'], 'o pagamento continua no cartão')
    c.mark(7)
    c.click(SEL('#amount'), at=c.A(7, 'Cento', 0.6), label='Valor')
    c.type(SEL('#amount'), '180,00', at=c.A(7, 'oitenta', 0.4), noClick=True, clear=True, label='digita 180,00')
    c.click(BTN('Confirmar Despesa'), at=c.A(7, 'Confirmar', 0.6), label='Confirmar Despesa')
    c.waitfor(gone={'role': 'dialog'}, timeout=12)
    c.waitfor(text='Aberta', timeout=12)
    c.hover(SEL('main :text("Disponível:")'), seconds=0.8, at=c.A(7, 'fatura', 0.5), label='a fatura Aberta e o Disponível (ZOOM)')
    c.confere('main', ['Aberta', 'R$ 180,00', 'R$ 9.820,00'], 'fatura de 180,00 e disponível de 9.820,00')
    c.mark(8)
    c.click(BTN('Pagar Fatura', within=MAIN), at=c.A(8, 'Pagar', 0.6), label='Pagar Fatura')
    c.waitfor(text='Origem do pagamento', timeout=10)
    c.hover(TXT('Origem do pagamento', within=DLG), seconds=0.8, at=c.A(8, 'conta', 0.5), label='Origem do pagamento (ZOOM)')
    c.hover({'text': 'Este pagamento quita a fatura.', 'within': DLG}, seconds=0.8, at=c.A(8, 'tudo', 0.5), label='quita a fatura')
    c.confere('dlg', ['Origem do pagamento', 'Este pagamento quita a fatura.'], 'janela Pagar Fatura')
    c.click(BTN('Cancelar', within=DLG), at=c.A(8, 'Aqui', 0.6), label='Cancelar (só mostrei)')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.mark(9)
    c.hover(SEL('main :text("Aberta")'), seconds=1.2, at=c.A(9, 'fatura', 0.5), label='a fatura Aberta')
    c.fim()
    return c


BTN_EXCL = SEL('[role=alertdialog] button:text-is("Excluir selecionados"), [role=dialog] button:text-is("Excluir selecionados")')
LOTE = ('Internet do pátio (teste)', 'Seguro da picape (teste)', 'Rastreador (teste)')
PONTOS_LINHA = lambda desc: SEL(f'main tr:has-text("{desc}") button[aria-label="Ações do lançamento"]')


def cap_corrigir():
    """cap06 · Corrigir e excluir lançamentos (variante `lote`: apos-cap04 + três despesas de teste; não segue adiante)"""
    c = Cap('corrigir', setup_mov([{'do': 'eval', 'js': js_rola_texto('Histórico de Movimentações', 120, 0)}]), pace=0.5)
    c.mark(1)
    c.hover(TXT(LOTE[0], within=MAIN), seconds=0.4, at=c.A(1, 'três', 0.5), label='Internet do pátio (teste)')
    c.hover(TXT(LOTE[1], within=MAIN), seconds=0.4, at=c.A(1, 'despesas', 0.5), label='Seguro da picape (teste)')
    c.hover(TXT(LOTE[2], within=MAIN), seconds=0.5, at=c.A(1, 'teste', 0.5), label='Rastreador (teste)')
    c.ev(js_main_topo(500), at=c.A(1, 'saldo', 0.9), label='sobe ao cartão')
    c.hover(SEL('main div.text-4xl.font-bold'), seconds=0.6, at=c.A(1, 'saldo', 0.5), label='o saldo menor do que devia')
    c.confere('main', ['R$ 44.684,77', 'Rastreador (teste)'], 'saldo de 44.684,77 e as três linhas de teste')
    c.mark(2)
    c.ev(js_rola_texto('Histórico de Movimentações', 120, 600), label='desce ao histórico')
    c.hover(TXT('Rastreador (teste)', within=MAIN), seconds=0.3, at=c.A(2, 'lançamento', 0.5), label='linha Rastreador (teste)')
    c.click(PONTOS_LINHA('Rastreador (teste)'), at=c.A(2, 'três', 0.6), label='três pontinhos (Ações do lançamento)')
    c.hover(ITEM('Excluir'), seconds=0.6, at=c.A(2, 'Excluir', 0.5), label='Editar e Excluir')
    c.mark(3)
    c.click(ITEM('Editar'), at=c.A(3, 'Editar', 0.6), label='Editar')
    c.waitfor(text='Editar lançamento', timeout=10)
    c.hover({'text': 'Valor (R$)', 'within': DLG}, seconds=0.6, at=c.A(3, 'valor', 0.5), label='Valor (R$) (ZOOM)')
    c.hover({'text': 'Conta', 'exact': True, 'within': DLG}, seconds=0.6, at=c.A(3, 'conta', 0.5), label='Conta')
    c.click(BTN('Cancelar', within=DLG), at=c.A(3, 'aqui', 0.6), label='Cancelar')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.mark(4)
    c.hover(SEL('main tr:has-text("Rastreador (teste)") button[title="Transferir para outra conta"]'), seconds=1.0, at=c.A(4, 'ícone', 0.5), label='Transferir para outra conta (sem clicar)')
    c.mark(5)
    c.click(PONTOS_LINHA('Rastreador (teste)'), at=c.A(5, 'Excluir', 1.2), label='três pontinhos')
    c.click(ITEM('Excluir'), at=c.A(5, 'Excluir', 0.6), label='Excluir')
    c.waitfor(text='Excluir lançamento?', timeout=10)
    c.hover({'text': 'Essa ação não pode ser desfeita.', 'within': ALERTA}, seconds=0.8, at=c.A(5, 'devolve', 0.5), label='o texto da janela (ZOOM)')
    c.confere('body', ['Rastreador (teste) será removido', 'R$ 89,90', 'Essa ação não pode ser desfeita.'], 'janela Excluir lançamento? com R$ 89,90')
    c.click(SEL('[role=alertdialog] button:text-is("Cancelar")'), at=c.A(5, 'vamos', 0.6), label='Cancelar')
    c.waitfor(gone={'role': 'alertdialog'}, timeout=8)
    c.mark(6)
    c.click({'placeholder': 'Buscar por descrição ou valor...'}, at=c.A(6, 'busco', 0.9), label='busca')
    c.type({'placeholder': 'Buscar por descrição ou valor...'}, 'teste', at=c.A(6, 'teste', 0.05), noClick=True, label='digita teste')
    c.mark(7)
    c.click(SEL('main button:has-text("Selecionar lançamentos")'), at=c.A(7, 'Selecionar', 0.6), label='Selecionar lançamentos')
    c.waitfor(text='Selecione até 100 itens', timeout=8)
    c.hover(SEL('main :text("Selecione até 100 itens")'), seconds=1.0, at=c.A(7, 'barra', 0.5), label='a barra de seleção (ZOOM)')
    c.mark(8)
    c.click(SEL('main [aria-label="Selecionar lançamentos elegíveis desta página"]'), at=c.A(8, 'caixinha', 0.6), label='marca todas pelo cabeçalho')
    c.waitfor(text='3 lançamentos selecionados', timeout=8)
    c.hover(SEL('main :text("3 lançamentos selecionados")'), seconds=0.8, at=c.A(8, 'selecionados', 0.5), label='3 lançamentos selecionados')
    c.mark(9)
    c.click(BTN('Alterar categoria', within=MAIN), at=c.A(9, 'Alterar', 0.6), label='Alterar categoria')
    c.waitfor(text='Alterar categoria de 3 lançamentos', timeout=10)
    c.hover({'text': 'Despesas selecionadas', 'within': DLG}, seconds=0.8, at=c.A(9, 'troca', 0.5), label='Despesas selecionadas (ZOOM)')
    c.hover({'text': 'Nova categoria (despesa)', 'within': DLG}, seconds=0.8, at=c.A(9, 'rápido', 0.5), label='Nova categoria (despesa)')
    c.confere('dlg', ['Despesas selecionadas', 'Valores e saldos não mudam.', 'Nova categoria (despesa)'], 'janela Alterar categoria')
    c.click(BTN('Cancelar', within=DLG), at=c.A(9, 'Só', 0.6), label='Cancelar')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.mark(10)
    c.click(BTN('Excluir selecionados', within=MAIN), at=c.A(10, 'Excluir', 0.6), label='Excluir selecionados')
    c.waitfor(text='Excluir 3 lançamentos?', timeout=10)
    c.hover({'text': 'Saídas selecionadas', 'within': ALERTA}, seconds=1.0, at=c.A(10, 'quinhentos', 0.5), label='Saídas selecionadas (ZOOM)')
    c.confere('body', ['Excluir 3 lançamentos?', 'Entradas selecionadas', 'Saídas selecionadas', 'R$ 552,20', 'em uma única operação'], 'janela Excluir 3 lançamentos? com R$ 552,20')
    c.mark(11)
    c.hover({'text': 'Essa ação não pode ser desfeita.', 'within': ALERTA}, seconds=0.5, at=c.A(10, 'Confiro', 0.5), label='aviso âmbar e Essa ação não pode ser desfeita')
    c.click(BTN_EXCL, at=c.A(11, 'Excluir', 0.6), label='Excluir selecionados (confirma)')
    c.waitfor(text='3 lançamentos excluídos.', timeout=12)
    c.hover(SEL('main div.text-4xl.font-bold'), seconds=1.0, at=c.A(11, 'saldo', 0.5), label='o saldo volta pro lugar (ZOOM)')
    c.confere('main', ['R$ 45.236,97'], 'saldo da Conta Principal de volta em 45.236,97')
    c.mark(12)
    c.click({'placeholder': 'Buscar por descrição ou valor...'}, at=c.A(12, 'caixinha', 1.4), label='busca')
    c.press('Control+a', label='seleciona o texto')
    c.press('Backspace', label='limpa a busca')
    c.hover(SEL('main tr:has-text("Compra #") , main tr:has-text("Venda #")'), seconds=1.0, at=c.A(12, 'pedido', 0.5), label='linha de pedido sem caixa (ZOOM)')
    c.press('Escape', at=c.A(12, 'conciliado', 0.5), label='fecha a seleção')
    c.fim()
    return c


def cap_outros():
    """cap17 · Outros casos do extrato (Conta Secundária; extrato de 8 linhas; não finaliza e não segue para a T15)"""
    c = Cap('outros', setup_mov([{'do': 'click', 'target': BTN('Conciliação')}, {'do': 'waitFor', 'text': 'Conta para conciliar', 'timeout': 20}, AGUARDA]), pace=0.5)
    SERR1, ACOS, COOPR, FUND, SIQ2 = 'PIX RECEBIDO SERRA FINA ALUMINIO RECICLAGEM', 'PIX RECEBIDO ACOS QUIRIRIM LTDA', 'PIX ENVIADO COOPERATIVA RECOMECO', 'PIX RECEBIDO FUNDICAO BANDEIRA DO VALE', 'PIX ENVIADO DEPOSITO IRMAOS SIQUEIRA'
    F1, F2 = 'PIX ENVIADO FOLHA DE PAGAMENTO LOTE 1', 'PIX ENVIADO FOLHA DE PAGAMENTO LOTE 2'
    c.mark(1)
    c.click(SEL('main button[role=combobox]:has-text("Conta Principal")'), at=c.A(1, 'Secundária', 0.9), label='Conta para conciliar')
    c.click(OPT('Conta Secundária'), label='Conta Secundária')
    c.click(BTN('Importar novo extrato'), at=c.A(1, 'importo', 0.6), label='Importar novo extrato')
    c.waitfor(text='Importar extrato OFX', timeout=10)
    c.upload(TXT('Arraste o arquivo .ofx aqui ou clique para selecionar', within=DLG), 'arquivos/Extrato_Secundaria_20261106_20261109.ofx', at=c.A(1, 'arquivo', 0.7),
             label='entrega o Extrato_Secundaria_20261106_20261109.ofx')
    c.waitfor(text='Prévia do extrato', timeout=10)
    c.click(BTN('Importar', within=DLG), label='Importar')
    c.waitfor(text='8 de 8 linhas importadas', timeout=15)
    c.click(BTN('Concluir'), label='Concluir')
    c.waitfor(text='Linha do extrato', timeout=15)
    c.ev(js_main_fim(0), label='desce até a tabela')
    for m in (SERR1, COOPR, FUND, '__SIQ_817__'):
        if m == '__SIQ_817__':
            c.click(SEL(f'{LINHA(SIQ2)}:has(:text-is("−R$ 817,00")) button:has-text("Casar com"), {LINHA(SIQ2)}:has(:text-is("−R$ 817,00")) button:has-text("Confirmar")'), label='Confirmar (R$ 817,00)')
            c.waitfor(target=SEL(f'{LINHA(SIQ2)}:has(:text-is("−R$ 817,00")) :text-is("Casada")'), timeout=10)
        else:
            confirma(c, m, label=f'Confirmar ({m})')
    c.mark(2)
    c.ev(js_rola_texto(SIQ2, 260, 600), at=c.A(2, 'acerto', 0.9), label='rola até o Pix de R$ 340,00')
    c.click(SEL(f'{LINHA(SIQ2)}:has(:text-is("−R$ 340,00")) button:has-text("Mais ações")'), at=c.A(2, 'Mais', 0.6), label='Mais ações (R$ 340,00)')
    c.click(ITEM('Saldo do cliente/fornecedor'), at=c.A(2, 'Saldo', 0.6, nth=0), label='Saldo do cliente/fornecedor')
    c.waitfor(text='Baixar na conta-corrente', timeout=10)
    c.click(SEL('main [role=combobox]:has-text("Selecione")'), at=c.A(2, 'Escolho', 0.7), label='Cliente ou fornecedor')
    c.click(OPT('Depósito Irmãos Siqueira', exact=False), label='escolhe o Depósito Irmãos Siqueira')
    c.hover(SEL('main :text("Dar baixa de R$ 340,00")'), seconds=0.8, at=c.A(2, 'saldo', 0.5, nth=1), label='o saldo do parceiro e o botão Dar baixa (ZOOM)')
    c.confere('main', ['Baixar na conta-corrente', 'Dar baixa de R$ 340,00'], 'painel Baixar na conta-corrente')
    c.mark(3)
    c.click(SEL('main button:has-text("Dar baixa de R$ 340,00")'), at=c.A(3, 'Dar', 0.6), label='Dar baixa de R$ 340,00')
    c.waitfor(text='Baixa na conta-corrente registrada', timeout=10)
    c.mark(4)
    c.ev(js_rola_texto(ACOS, 260, 600), at=c.A(4, 'segundo', 0.9), label='rola até o Pix da Aços Quiririm')
    c.click(NA_LINHA(ACOS, 'Mais ações'), at=c.A(4, 'Mais', 0.6), label='Mais ações (R$ 50.215,00)')
    c.click(ITEM('Casar com vários lançamentos'), at=c.A(4, 'Casar', 0.6), label='Casar com vários lançamentos')
    c.waitfor(text='Um Pix que pagou dois pedidos', timeout=10, optional=True)
    c.hover(TXT('Casar com vários lançamentos', within=MAIN), seconds=0.4, label='o painel')
    c.click({'placeholder': 'Nome do cliente/fornecedor, nº do pedido...'}, label='campo da busca')
    c.type({'placeholder': 'Nome do cliente/fornecedor, nº do pedido...'}, 'Quiririm', noClick=True, label='digita Quiririm')
    c.click(SEL(f'{LINHA(ACOS)} [role=checkbox], {LINHA(ACOS)} :text("48.740,00")', nth=0), at=c.A(4, 'marco', 0.6), label='marca a venda de 48.740,00')
    c.click(SEL(f'{LINHA(ACOS)} :text("1.475,00")'), label='marca a venda de 1.475,00')
    c.hover(SEL(f'{LINHA(ACOS)} button:has-text("Casar com 2 lançamentos")'), seconds=0.8, at=c.A(4, 'soma', 0.5), label='as duas vendas e a soma (ZOOM)')
    c.click(SEL(f'{LINHA(ACOS)} button:has-text("Casar com 2 lançamentos")'), at=c.A(4, 'libera', 0.9), label='Casar com 2 lançamentos')
    c.waitfor(target=SEL(f'{LINHA(ACOS)} :text-is("Casada")'), timeout=10)
    c.mark(5)
    c.ev(js_rola_texto(F1, 260, 600), at=c.A(5, 'contrário', 0.9), label='rola até a folha')
    c.click(SEL(f'{LINHA(F1)} button[role=checkbox]'), at=c.A(5, 'Marco', 0.6), label='marca LOTE 1')
    c.click(SEL(f'{LINHA(F2)} button[role=checkbox]'), label='marca LOTE 2')
    c.hover({'text': 'Soma:', 'within': MAIN}, seconds=0.8, at=c.A(5, 'soma', 0.5), label='Soma e Casar 2 linhas com um lançamento (ZOOM)', noScroll=True)
    c.click(BTNX('Casar 2 linhas com um lançamento', within=MAIN), at=c.A(5, 'Casar', 0.6), label='Casar 2 linhas com um lançamento')
    c.waitfor(text='Escolha o lançamento no sistema', timeout=10)
    c.click(SEL('[role=dialog] :text("Folha de outubro")'), label='escolhe o lançamento da folha')
    c.click(BTN('Casar 2 linhas', within=DLG), label='Casar 2 linhas')
    c.waitfor(target=SEL(f'{LINHA(F1)} :text-is("Casada")'), timeout=10)
    c.mark(6)
    c.hover(SEL(f'{LINHA(F1)} :text-is("Casada")'), seconds=1.5, at=c.A(6, 'outra', 0.5), label='(ilustração) o Pix na conta errada')
    c.mark(7)
    c.ev(js_rola_texto('Linha do extrato', 120, 400), label='sobe à tabela')
    c.fim()
    return c


# ---------------------------------------------------------------- main
def main():
    pedidos = [int(a) for a in sys.argv[1:] if a.isdigit()]
    chaves = {chave: (globals().get(f'cap{chave:02d}') if isinstance(chave, int) else globals().get(f'cap_{chave}')) for chave in NOVO}
    fns = {NOVO[k]: fn for k, fn in chaves.items()}
    feitos = []
    for n, fn in sorted(fns.items()):
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
