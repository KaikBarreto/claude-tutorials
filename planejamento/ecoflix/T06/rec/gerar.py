#!/usr/bin/env python3
"""T6 · Caixa: abrir, fechar e o cofre (EcoFlix, EcoSistema 1.59.154): gera rec/t06/cap00..cap12.json (+ cap08b, o corte do Marcos)
a partir da fala ($TUT_HOME/t06/narracao/capNN.json: o estimado até a voz chegar; com a voz, o da voz, sem mudar nada aqui).

Computador 1280x800, Rafael Nogueira (master) na Recicla Vale Metais. FAKE_NOW (o mesmo no Supabase falso e no robô: rec/t06/t06_cap.sh
sobe a instância com o certo): 08:30:00 nos caps 0 e 1, 08:30:55 no cap 2 (o #85 abre às 08:31), 08:41:50 nos caps 3 a 5 (o #86 abre às
08:42), 08:45:00 nos caps 6 a 9 e no 8b, 17:40:00 no cap 10 (fecha às 17:42), 17:42:40 no 11 (reabre às 17:43) e 17:44:00 no 12
(todos em 10/11/2026, -03:00).
Rodar de qualquer pasta: `python3 -I rec/t06/gerar.py [NN ...] [8b]` (ANCORAS=1 lista as âncoras). Depois:
`node rec/record.mjs rec/t06/capNN.json --check`; ensaiar: `bash rec/t06/t06_cap.sh NN [--so-rapido]` (pela fila rec/fila.sh).

LOGIN: todo capítulo é "anonymous" e o setup entra pela tela de login com "$TUT_USER"/"$TUT_SENHA" do ambiente (o Supabase falso
aceita qualquer senha; o valor nunca vai para arquivo nem log). O corte do Marcos (cap08b, "o computador da balança") entra com o
e-mail dele (dado do mundo fictício) e a mesma "$TUT_SENHA".

Cada passo é preso a uma palavra da fala: A(linha, 'palavra', folga) = início da palavra - folga (o custo do gesto até o cursor
chegar: clique ~0,6 s, 1o clique numa janela recém-aberta ~1,1 s, hover ~0,5 s; digitação sem clique na palavra - 0,05 s).
A palavra casa INTEIRA (sem acento e pontuação); repetida na linha pede `nth`. Marca Ln 0,9 s antes da linha (molde do T14/T02);
um passo que começa até 0,25 s antes da marca a puxa para o início dele.

Estado de partida (rec/mundo/seeds-extra/t06/, escrito por rec/t06/t06_sementes.py): mundo base (nenhum caixa aberto; o #84 do
Rafael é o último) nos caps 0 a 2; + `apos-cap02` (#85 do Rafael, R$ 1.500,00, 08:31) nos caps 3 a 5 (o setup dos caps 4 e 5 abre
fora do vídeo "Início" > "Abrir Caixa" para o Marcos); + `apos-cap05` (#86 do Marcos, R$ 17.000,00, 08:42) nos caps 6 a 9 e no 8b;
+ `apos-cap09` (saque de 3.000,00 + 6,50 para o #86 e a tarifa mensal de 39,90) + `dia-10` (venda à Aços Quiririm, latinha da
Aparecida e ferro misto do Valdir no #85) no cap10; + `apos-cap10` (#85 fechado com R$ 1.007,10 às 17:42) no cap11;
+ `apos-cap11` (#85 reaberto) no cap12 (passeio de reserva da montagem).

PARTICULARIDADES DA 1.59.154 (explorações rec/t06/_ex/e1..e2, 11/11):
 - Sem caixa aberto a página não rola (cabe em 800 px); com caixa aberto quem rola é o <main> (overflow-y auto, ~356 px a mais).
 - Shift+C no /caixa vai ao /compra, que avisa "Abra o caixa antes de realizar compras" e volta sozinho ao /caixa em < 0,2 s.
 - "Saldo de Abertura (R$)" (#openingBalance) é máscara de milhar: "150000" vira "150.000"; digitar "1.500,00" (com vírgula).
 - Observador `OBS` guarda em window.__avisos todo aviso de erro do app (texto ou toast vermelho); o passo final devolve a lista.
"""
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TUT_HOME = os.path.normpath(os.path.join(HERE, '..', '..'))
NARR = os.path.join(TUT_HOME, 't06', 'narracao')
AULA = 't06'
MANHA = '2026-11-10T08:30:00-03:00'
TARDE = '2026-11-10T17:40:00-03:00'
# o relógio anda pela manhã como a história (MUNDO_LINHA_DO_TEMPO.md, "O dia 10/11"): o app grava a abertura com o minuto do campo
# "Data e Hora de Abertura" no instante em que a janela abre, e nenhum caixa abre antes das 08:31 (#85 às 08:31, #86 às 08:42)
FAKE_NOW = {0: MANHA, 1: MANHA, 2: '2026-11-10T08:30:55-03:00', 3: '2026-11-10T08:41:50-03:00', 4: '2026-11-10T08:41:50-03:00',
            5: '2026-11-10T08:41:50-03:00', 6: '2026-11-10T08:45:00-03:00', 7: '2026-11-10T08:45:00-03:00', 8: '2026-11-10T08:45:00-03:00',
            9: '2026-11-10T08:45:00-03:00', 10: TARDE, 11: '2026-11-10T17:42:40-03:00', 12: '2026-11-10T17:44:00-03:00'}
NOMES = ['Abertura', 'O caixa fechado', 'Abrir o caixa', 'Abrir com zero', 'O cofre da empresa', 'Saldo insuficiente',
         'Os dois cartões', 'Cada um com o seu caixa', 'O caixa dos outros', 'Saque e sangria', 'Fechar o caixa',
         'Reabrir um caixa', 'Recapitulando']
_C = [f'{AULA}/apos-cap02', f'{AULA}/apos-cap05', f'{AULA}/apos-cap09', f'{AULA}/dia-10', f'{AULA}/apos-cap10', f'{AULA}/apos-cap11']
SEMENTE = {0: [], 1: [], 2: [], 3: _C[:1], 4: _C[:1], 5: _C[:1], 6: _C[:2], 7: _C[:2], 8: _C[:2], 9: _C[:2],
           10: _C[:4], 11: _C[:5], 12: _C[:6]}
EMAIL_MARCOS = 'marcos.antunes@reciclavalemetais.example'

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
        atual = texto_atual(n)
        voz = [norm(w['w']) for w in words if norm(w['w'])]
        if atual != voz:
            print(f'  AVISO cap{n:02d}: a fala do capNN.json não é a do tts_textos.py de hoje (rode o preparar_aula.sh de novo)')
    return words, linhas, float(d['dur']), bool(d.get('estimado'))


# ---------------------------------------------------------------- observador de avisos de erro (aceite: tem de sair vazio)
OBS = ("(()=>{window.__avisos=[];const re=/N[ãa]o foi poss[ií]vel|Erro ao|Tente novamente|Algo deu errado|Falha ao|Something went wrong/i;"
       "const chk=(t)=>{t=(t||'').trim();const m=t&&t.match(new RegExp('[^]{0,40}('+re.source+')[^]{0,40}','i'));"
       "if(m&&window.__avisos.length<10)window.__avisos.push(m[0].replace(/[\\n\\r\\t ]+/g,' '))};new MutationObserver(ms=>{for(const m of ms){"
       "m.addedNodes.forEach(n=>chk(n.textContent));if(m.type==='characterData')chk(m.target.textContent)}}).observe(document.body,"
       "{childList:true,subtree:true,characterData:true});chk(document.body.innerText);"
       "setInterval(()=>{document.querySelectorAll('[data-sonner-toast][data-type=error]').forEach(t=>{const s='TOAST DE ERRO: '+t.textContent.trim().slice(0,90);"
       "if(!window.__avisos.includes(s)&&window.__avisos.length<10)window.__avisos.push(s)})},300);return 1})()")


def js_obs(erros_ok=()):
    """o OBS, sem os avisos que o roteiro pede na tela (ex.: o toast "Abra o caixa antes de realizar compras" do cap01)"""
    if not erros_ok:
        return OBS
    ok = json.dumps(list(erros_ok), ensure_ascii=False)
    return OBS.replace("window.__avisos.push(m[0]", f"!{ok}.some(x=>m[0].includes(x))&&window.__avisos.push(m[0]").replace(
        "if(!window.__avisos.includes(s)&&", f"if(!{ok}.some(x=>s.includes(x))&&!window.__avisos.includes(s)&&")


class Cap:
    def __init__(s, n, setup, pace=0.5, cps=40, start=(760, 470), prewarm=('/login',), sub='', voz_de=None, user='rafael', erros_ok=()):
        s.n, s.sub = n, sub
        s.nome = f'cap{n:02d}{sub}'
        s.words, s.linhas, s.dur, s.estimado = carregar_voz(n)
        s.voz_inicio = 0.0
        if voz_de:   # corte: só as linhas voz_de[0]..voz_de[1] da voz, com o tempo contado do início da primeira (T15 cap09b, T03 cap01b)
            a, b = voz_de
            off = s.linhas[a - 1]['s']
            s.voz_inicio = round(off, 2)
            s.words = [dict(w, s=round(w['s'] - off, 3), e=round(w['e'] - off, 3), linha=w['linha'] - (a - 1))
                       for w in s.words if a - 1 <= w['linha'] <= b - 1]
            fim = s.linhas[b - 1]['e'] + 0.4
            s.linhas = [dict(l, i=l['i'] - (a - 1), s=round(l['s'] - off, 3), e=round(l['e'] - off, 3)) for l in s.linhas[a - 1:b]]
            s.dur = round(fim - off, 2)
        s.steps, s.pending, s.anchors = [], [], []
        s.pace, s.cps, s.start = pace, cps, start
        s.prewarm = list(prewarm)
        s.user = user
        s.setup = list(setup) + [{'do': 'eval', 'js': js_obs(erros_ok)}]

    # ---- tempo
    def L(s, i):
        return round(s.linhas[i - 1]['s'], 2)

    def W(s, i, palavra, nth=None, fim=False):
        q = norm(palavra)
        hits = [w for w in s.words if w['linha'] == i - 1 and norm(w['w']) == q]
        if nth is None:
            if len(hits) > 1:
                print(f'  aviso {s.nome}: "{palavra}" aparece {len(hits)} vezes na linha {i}: usei a 1a (passe nth)')
            nth = 0
        if len(hits) <= nth:
            raise SystemExit(f'{s.nome}: palavra "{palavra}" (#{nth}) não achada na linha {i}: '
                             + ' '.join(w['w'] for w in s.words if w['linha'] == i - 1))
        return hits[nth]['e' if fim else 's']

    def A(s, i, palavra, folga=0.6, nth=None):
        t = round(max(0.0, s.W(i, palavra, nth) - folga), 2)
        s.anchors.append((i, palavra, t))
        return t

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

    def marca_em(s, i, at):
        """marca Ln já no início de um passo que começa antes da linha e dura até ela (clique lento que tem de agir NA palavra):
        sem isso a marca só sairia depois do passo, atrasada (docs/08, linhas 53 e 131)"""
        s.flush(at)
        s.pending = [(mt, mi) for mt, mi in s.pending if mi != i]
        s.steps.append({'do': 'mark', 'name': f'L{i}', 'at': round(at, 2)})

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

    def rolar(s, by, at=None, label=None, ponto=(800, 470), duration=0.5, after=100):
        return s._p({'do': 'scroll', 'point': {'x': ponto[0], 'y': ponto[1]}, 'by': by, 'duration': duration, 'after': after}, at, label, {})

    def confere(s, escopo, esperados, label, tentativas=20):
        """`eval` que LÊ a tela e compara com a fala: "OK: ..." ou "DIFERENTE: ..." (o resumo.py acusa). Escopo: 'dlg' (a última
        janela aberta), 'main', 'body' ou um seletor CSS. Tenta por ~tentativas x 0,3 s."""
        sel = {'dlg': '[role=dialog],[role=alertdialog]', 'main': 'main', 'body': 'body'}.get(escopo, escopo)
        esp = [esperados] if isinstance(esperados, str) else list(esperados)
        js = ("(async()=>{const norm=t=>t.replace(/[\\s\\u00a0]+/g,' ').toLowerCase();const esp=%s;let out='';"
              "for(let i=0;i<%d;i++){const els=[...document.querySelectorAll(%s)];const el=%s?els[els.length-1]:els[0];"
              "if(!el){out='DIFERENTE: sem elemento';}else{const t=norm(el.innerText);const falta=esp.filter(e=>!t.includes(norm(e)));"
              "if(!falta.length)return 'OK: '+esp.join(' | ');out='DIFERENTE: faltou '+JSON.stringify(falta)+' em: '+t.slice(0,240);}"
              "await new Promise(r=>setTimeout(r,300));}return out})()") % (json.dumps(esp, ensure_ascii=False), tentativas, json.dumps(sel),
                                                                            'true' if escopo == 'dlg' else 'false')
        return s.add({'do': 'eval', 'js': js, 'label': 'confere ' + label})

    def confere_campo(s, seletor, esperado, label):
        js = ("(async()=>{let v='';for(let i=0;i<12;i++){const e=document.querySelector(%s);v=e?e.value:'(sem campo)';if(v===%s)return 'OK: '+v;"
              "await new Promise(r=>setTimeout(r,250));}return 'DIFERENTE: '+v})()") % (json.dumps(seletor), json.dumps(esperado))
        return s.add({'do': 'eval', 'js': js, 'label': 'confere ' + label})

    def confere_js(s, js_ok_ou_diferente, label):
        """`eval` com uma expressão que devolve 'OK: ...' ou 'DIFERENTE: ...' (conferência pontual)"""
        return s.add({'do': 'eval', 'js': js_ok_ou_diferente, 'label': 'confere ' + label})

    def fim(s):
        s.flush(1e9)
        s.steps.append({'do': 'eval', 'js': 'JSON.stringify(window.__avisos || "sem observador")', 'label': 'avisos de erro na tela'})
        s.steps.append({'do': 'mark', 'name': 'FIM', 'at': round(s.dur, 2)})

    def out(s):
        est = ' ESTIMADA' if s.estimado else ''
        corte = f'; corte das linhas da voz a partir de {str(s.voz_inicio).replace(".", ",")} s' if s.voz_inicio else ''
        quem = 'Marcos Antunes' if s.user == 'marcos' else 'Rafael Nogueira'
        d = {
            'name': f'{AULA}-{s.nome}',
            'title': f'T6 · Cap. {s.n}{s.sub} · {NOMES[s.n]} (narração{est} {str(round(s.dur, 1)).replace(".", ",")} s{corte}; marcas '
                     f'L1..L{len(s.linhas)} = início de cada linha do roteiro; FAKE_NOW {FAKE_NOW[s.n]}; logado como {quem})',
            'seed': f'{AULA}-{s.nome}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
            'start': {'x': s.start[0], 'y': s.start[1]},
            'anonymous': True, 'storage': storage(s.user),
            'seedExtra': list(SEMENTE[s.n]),
            'prewarm': s.prewarm, 'setup': s.setup, 'steps': s.steps,
        }
        if s.voz_inicio:
            d['voz_inicio'] = s.voz_inicio      # a edição e o resumo.py contam a voz a partir daqui
        return d


# ---------------------------------------------------------------- alvos
MAIN = 'main'
DLG = '[role=dialog]'
ALERTA = '[role=alertdialog]'
BTN = lambda n, within=None, **kw: {'role': 'button', 'name': n, 'exact': True, **({'within': within} if within else {}), **kw}
BTNX = lambda n, within=None, **kw: {'role': 'button', 'name': n, **({'within': within} if within else {}), **kw}
TXT = lambda t, within=MAIN, **kw: {'text': t, 'exact': True, 'within': within, **kw}
TXTX = lambda t, within=MAIN, **kw: {'text': t, 'exact': False, 'within': within, **kw}
SEL = lambda s, **kw: {'selector': s, **kw}
OPT = lambda n, **kw: {'role': 'option', 'name': n, **kw}
LINK = lambda n, **kw: {'role': 'link', 'name': n, 'exact': True, **kw}
AGUARDA = {'do': 'waitFor', 'idle': True}
CAMPO_ABERTURA = SEL('#openingBalance')


# ---------------------------------------------------------------- trechos de setup (fora do vídeo)
def stable_id(chave):
    """o mesmo UUID do `@id:<chave>` das sementes (rec/fakebase/core/util.mjs, stableId)"""
    import hashlib
    h = bytearray(hashlib.sha1(('domiflix-fake:' + chave).encode()).digest())
    h[6] = (h[6] & 0x0F) | 0x50
    h[8] = (h[8] & 0x3F) | 0x80
    x = h[:16].hex()
    return f'{x[:8]}-{x[8:12]}-{x[12:16]}-{x[16:20]}-{x[20:32]}'


VERSAO = '1.59.154'
HOJE = MANHA[:10]


def storage(user='rafael'):
    """localStorage que a sessão pronta do robô poria (mundo.json, navegador.localStorage): versão já vista, PWA dispensado, tema claro,
    lembrete de tarefas do dia já mostrado e preferências iniciais."""
    uid = stable_id(f'user.{user}')
    return {'app_version': VERSAO, 'notification_shown_version': VERSAO, 'pwa-install-dismissed': 'true', 'theme': 'light',
            f'daily-tasks-reminder-last-shown-{uid}': HOJE, 'initial-preferences-set': 'true'}


def login(email='$TUT_USER', ola='Olá, Rafael!'):
    """tela de login (fora do vídeo); `ola` = texto que confirma a entrada (None: o botão Sair do menu, para quem não cai no Dashboard)"""
    entrou = {'do': 'waitFor', 'text': ola, 'timeout': 30} if ola else {'do': 'waitFor', 'selector': 'button[aria-label="Sair"]', 'timeout': 30}
    return [{'do': 'waitFor', 'target': {'label': 'E-mail'}, 'timeout': 30},
            {'do': 'type', 'target': {'label': 'E-mail'}, 'text': email, 'cps': 40},
            {'do': 'type', 'target': {'label': 'Senha', 'exact': True}, 'text': '$TUT_SENHA', 'cps': 40},
            {'do': 'click', 'target': {'role': 'button', 'name': 'Entrar', 'exact': True}},
            entrou, AGUARDA]


LOGIN = login()
IR_CAIXA = [{'do': 'goto', 'url': '/caixa'}, {'do': 'waitFor', 'text': 'Gestão financeira e movimentações', 'timeout': 25}, AGUARDA]


def setup_caixa(extra=()):
    return LOGIN + IR_CAIXA + list(extra)


# ---------------------------------------------------------------- JavaScript (rolagens suaves e cliques sem cursor)
ACHA_ROLAGEM = ("const rolagem=(el)=>{let c=el&&el.parentElement;while(c&&c!==document.body){const s=getComputedStyle(c);"
                "if(/(auto|scroll)/.test(s.overflowY)&&c.scrollHeight>c.clientHeight+4)return c;c=c.parentElement;}"
                "return [...document.querySelectorAll('main')].find(e=>/(auto|scroll)/.test(getComputedStyle(e).overflowY)&&e.scrollHeight>e.clientHeight+4)||null};")
SUAVE = ("await new Promise(res=>{const t0=performance.now();const f=t=>{const p=Math.min(1,(t-t0)/DUR),e=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;"
         "c.scrollTop=y0+dy*e;p<1?requestAnimationFrame(f):res()};requestAnimationFrame(f)});")


def js_rola_ate(texto, y=250, dur_ms=900, esc='main', prefixo=False):
    """rolagem suave do contêiner que rola, até a folha cujo texto é `texto` (ou começa com ele) ficar em y px CSS; o cursor não se mexe.
    Devolve o topo final do alvo, 'ok' (já estava), 'SEM ALVO' ou 'SEM ROLAGEM'."""
    alvo = json.dumps(texto)
    cond = f"e.textContent.trim().startsWith({alvo})" if prefixo else f"e.textContent.trim()==={alvo}"
    return ("(async()=>{" + ACHA_ROLAGEM + f"const el=[...document.querySelectorAll({json.dumps(esc + ' *')})].filter(e=>e.children.length===0&&{cond})[0];"
            "if(!el)return 'SEM ALVO';const c=rolagem(el);if(!c)return 'SEM ROLAGEM';"
            f"const y0=c.scrollTop;const dy=Math.round(el.getBoundingClientRect().top-{int(y)});if(Math.abs(dy)<3)return 'ok';"
            + SUAVE.replace('DUR', str(int(dur_ms))) + "return Math.round(el.getBoundingClientRect().top)})()")


def js_rola_topo(dur_ms=700):
    return ("(async()=>{" + ACHA_ROLAGEM + "const c=rolagem(null);if(!c)return 'SEM ROLAGEM';const y0=c.scrollTop;if(y0<3)return 'ok';const dy=-y0;"
            + SUAVE.replace('DUR', str(int(dur_ms))) + "return 'topo:'+Math.round(c.scrollTop)})()")


def js_rola_fundo(esc=DLG, dur_ms=600):
    """rolagem suave até o fim do contêiner que rola o conteúdo de `esc` (a janela aberta); devolve 'fim:<scrollTop>'"""
    return ("(async()=>{" + ACHA_ROLAGEM + f"const d=document.querySelector({json.dumps(esc)});const el=d&&d.querySelector('label,p,h2');"
            "if(!el)return 'SEM ALVO';const c=rolagem(el);if(!c)return 'SEM ROLAGEM';const y0=c.scrollTop;const dy=c.scrollHeight-c.clientHeight-y0;"
            "if(dy<3)return 'ok';" + SUAVE.replace('DUR', str(int(dur_ms))) + "return 'fim:'+Math.round(c.scrollTop)})()")


def js_clicar(seletor, texto=None):
    """clique sem cursor (`el.click()`): o primeiro `seletor` visível (com o texto, se dado)"""
    cond = f"&&e.textContent.trim().startsWith({json.dumps(texto)})" if texto else ''
    return (f"(()=>{{const e=[...document.querySelectorAll({json.dumps(seletor)})].find(e=>e.getClientRects().length{cond});"
            "if(!e)return 'SEM ALVO';e.click();return 'ok'})()")


# ================================================================ capítulos
CAPS_FN = {}


def cap(fn):
    CAPS_FN[fn.__name__[3:]] = fn
    return fn


# ---------------------------------------------------------------- alvos da tela do Caixa (explorações e1..e3)
FIN = {'text': 'Financeiro', 'exact': True}                               # grupo do menu lateral (abre o submenu)
ABRIR = BTN('Abrir Caixa', MAIN)
ABRIR_DLG = BTN('Abrir Caixa', DLG)
USUARIO = SEL(f'{DLG} button[role=combobox]')                            # "Abrir para o usuário" (1o seletor da janela)
INICIO = BTN('Início', MAIN)
TAB85 = BTNX('#85 | Caixa - Rafael Nogueira', MAIN)                       # nome acessível "#85 | Caixa - Rafael Nogueira(você)"
TAB86 = BTNX('#86 | Caixa - Marcos Antunes', MAIN)
AJUDA = SEL('main button[aria-haspopup="dialog"]:has(svg[class*="help"])')   # o "?" à direita das abas (HelpCircle, sem nome acessível)
TOTAL = BTN('Ver movimentações do dinheiro da empresa', MAIN)            # "Dinheiro total da empresa: R$ ... ›" (aria-label)
OLHO = SEL('main button[aria-label="Ocultar saldo"]')
OLHO2 = SEL('main button[aria-label="Mostrar saldo"]')
SAQUE_SANGRIA = BTNX('Saque / Sangria', MAIN)
NOVA_MOV = BTNX('Nova Movimentação Bancária', MAIN)
TOAST = SEL('[data-sonner-toast]')
CARD_AMARELO = SEL('main div[class*="border-amber-500/40"]')            # cartão "Reabrir #N" (CashRegisterHomePanel.tsx:596)
ALERTA_COFRE = '[role=dialog]:has-text("Saldo insuficiente em dinheiro")'   # 2a janela por cima do Abrir Caixa (o `within` pega a 1a que casa)
COMBO = lambda n: SEL(f'{DLG} button[role=combobox]', nth=n)            # seletores da janela, na ordem da tela
VALOR = SEL(f'{DLG} #amount')
DESCRICAO = SEL(f'{DLG} #description')
TARIFA = SEL(f'{DLG} #fee')                                             # "Valor da Tarifa" (aparece com "Sim"; WithdrawalForm.tsx:775)


def colar(c, seletor, texto, at=None, label=None):
    """texto longo sem graça visual: insertText no campo já focado (~0,05 s; o valor fica no actions.json)"""
    js = (f"(()=>{{const e=document.querySelector({json.dumps(seletor)});if(!e)return 'SEM ALVO';e.focus();"
          f"document.execCommand('insertText',false,{json.dumps(texto, ensure_ascii=False)});return e.value}})()")
    return c.ev(js, at=at, label=label or f'cola "{texto}"')


def abrir_dialogo_marcos():
    """setup dos caps 4 e 5 (fora do vídeo): Início > Abrir Caixa > Abrir para o usuário > Marcos Antunes"""
    return [{'do': 'click', 'target': INICIO}, {'do': 'waitFor', 'text': 'Abrir Caixa para Outro Usuário', 'timeout': 10},
            {'do': 'click', 'target': ABRIR}, {'do': 'waitFor', 'text': 'Informe o saldo inicial em dinheiro', 'exact': False, 'timeout': 10},
            {'do': 'click', 'target': USUARIO}, {'do': 'click', 'target': OPT('Marcos Antunes')},
            {'do': 'waitFor', 'text': 'Disponível no cofre agora', 'exact': False, 'timeout': 10}, {'do': 'wait', 'seconds': 0.6}]


# ================================================================ capítulos
@cap
def cap00():
    """Abertura: Dashboard parado sob a ilustração (L1 a L3); L4 o caminho Financeiro > Caixa; L5 o cartão "Antes:" (edição)."""
    c = Cap(0, LOGIN + [AGUARDA, {'do': 'wait', 'seconds': 1.0}], start=(760, 420))
    c.mark(1)
    c.mark(2)
    c.mark(3)
    c.mark(4)
    # 1o clique do capítulo: o cursor vem do meio da tela até o menu (~1,3 s até o clique, ensaio de 11/11)
    c.click(FIN, at=c.A(4, 'Financeiro', 1.6), label='menu Financeiro')
    c.click(LINK('Caixa'), at=c.A(4, 'Caixa', 1.0), label='menu Caixa')
    c.mark(5)
    c.flush(1e9)          # a marca L5 sai antes da espera da página (o /caixa leva ~2 s para carregar)
    c.waitfor(text='Gestão financeira e movimentações', timeout=15)
    c.fim()
    return c


@cap
def cap01():
    """O caixa fechado (aba Início do gestor, sem caixa aberto): Meu Caixa, cartão amarelo do #84, Painel Gerencial vazio, Shift+C."""
    c = Cap(1, setup_caixa([{'do': 'waitFor', 'text': 'Nenhum caixa foi aberto neste dia.', 'timeout': 15}]),
            erros_ok=('Abra o caixa antes de realizar compras',))     # o aviso que a L5 mostra de propósito
    c.mark(1)
    c.confere('main', ['Meu Caixa', 'Abrir Caixa', '#84', 'R$ 1.250,00', 'Rafael Nogueira', '09/11 07:58 → 09/11 17:44', 'reabrir outro caixa',
                       'Reabrir #84', '0 caixas encontrados'], 'tela do caixa fechado (#84, R$ 1.250,00)')
    # gravação de 11/11 (16:25, máquina carregada por renders: gestos 1,5 a 2x mais lentos): hover ~1,6 s até o cursor chegar;
    # sem a carga, ~1 s. Folgas no meio do caminho até a próxima gravação medir de novo.
    c.hover(ABRIR, at=c.A(1, 'Meu', 0.6), label='botão Abrir Caixa (Meu Caixa)')
    c.mark(2)
    c.hover(CARD_AMARELO, at=c.A(2, 'cartão', 0.5), label='ZOOM cartão amarelo #84 (L2)')
    c.hover(BTN('Reabrir #84', MAIN), at=c.A(2, 'reabrir', 1.0), label='Reabrir #84')
    c.mark(3)
    c.hover(TXT('Painel Gerencial'), at=c.A(3, 'Painel', 0.9), label='Painel Gerencial')
    c.hover(TXT('Nenhum caixa foi aberto neste dia.'), 0.3, at=c.A(3, 'Por', 0.5), label='Nenhum caixa foi aberto neste dia.')
    c.mark(4)
    c.hover(ABRIR, at=c.A(4, 'Quem', 0.3), label='volta ao topo (o mesmo botão Abrir Caixa)')
    c.mark(5)
    # o /compra aparece por ~3 s ("Nova Compra", sem caixa) antes do aviso e da volta: o atalho sai em "lançar" para o aviso
    # subir em "Abra o caixa..."
    c.press('Shift+C', at=c.A(5, 'lançar', 0.2), label='atalho Shift+C (Compra)')
    c.waitfor(text='Abra o caixa antes de realizar compras', timeout=8)
    c.marcar(TOAST, label='ZOOM aviso Abra o caixa antes de realizar compras (L5)')
    c.waitfor(text='Gestão financeira e movimentações', timeout=8)
    c.mark(6)
    c.hover(ABRIR, at=c.A(6, 'abrir', 0.5), label='Abrir Caixa (vamos abrir)')
    c.fim()
    return c


@cap
def cap02():
    """Abrir o caixa #85 com R$ 1.500,00 (a dica do #84 é só referência)."""
    c = Cap(2, setup_caixa([{'do': 'waitFor', 'text': 'Nenhum caixa foi aberto neste dia.', 'timeout': 15}]))
    c.mark(1)
    c.click(ABRIR, at=c.A(1, 'Abrir', 0.6), label='Abrir Caixa')
    c.waitfor(text='Informe o saldo inicial em dinheiro', exact=False, timeout=10)
    c.confere_campo('#customOpenDatetime', '2026-11-10T08:31', 'hora da abertura 08:31')
    c.hover(TXTX('Informe o saldo inicial em dinheiro', DLG), at=c.A(1, 'saldo', 0.5), label='a janela pede o saldo inicial')
    c.mark(2)
    c.hover(CAMPO_ABERTURA, at=c.A(2, 'campo', 0.5), label='ZOOM campo Saldo de Abertura vazio e a dica do #84 (L2 a L4)')
    c.hover(TXTX('foi o valor restante em dinheiro do último caixa', DLG), at=c.A(2, 'dica', 0.5), label='dica R$ 1.250,00 do último caixa (#84)')
    c.confere('dlg', ['R$ 1.250,00 foi o valor restante em dinheiro do último caixa (#84)', 'Disponível no cofre agora: R$ 18.500,00',
                      'O caixa será aberto sem dinheiro em espécie (R$ 0,00)'], 'dica do #84, cofre e aviso do zero')
    c.mark(3)
    c.hover(CAMPO_ABERTURA, at=c.A(3, 'digite', 0.5), label='campo (digite o que contou)')
    c.mark(4)
    # a digitação na máscara do campo leva ~0,2 s por caractere (ensaio de 11/11: 2,3 s para "1.500,00") e o clique em "Abrir Caixa"
    # da janela ~1,9 s até agir (a janela se ajeita quando o aviso do zero some): o campo começa cedo para o clique cair em "Abrir"
    c.click(CAMPO_ABERTURA, at=c.A(4, 'Hoje', 0.6), label='campo Saldo de Abertura')
    c.type(CAMPO_ABERTURA, '1.500,00', at=c.A(4, 'contei', 0.05), label='digita 1.500,00', noClick=True)
    c.confere_campo('#openingBalance', '1.500,00', 'campo com 1.500,00')
    t = c.A(5, 'Abrir', 1.2)
    c.marca_em(5, t)
    c.click(ABRIR_DLG, at=t, label='Abrir Caixa (janela)')
    c.waitfor(text='Caixa aberto com sucesso!', timeout=10)
    c.hover(TXT('R$ 1.500,00'), at=c.A(5, 'mil', 0.5), label='Dinheiro em Caixa R$ 1.500,00 (#85)')
    c.confere('main', ['#85 | Caixa - Rafael Nogueira', 'Dinheiro em Caixa', 'R$ 1.500,00', 'Aberto em: 10/11/2026 08:31'], 'caixa #85 aberto às 08:31')
    c.fim()
    return c


@cap
def cap03():
    """Abrir com zero: a linha de abertura no histórico; (ilustração do dia só de Pix); o caixa do Marcos com o campo vazio."""
    c = Cap(3, setup_caixa([{'do': 'waitFor', 'text': 'Abertura do Caixa #85', 'timeout': 15}]))
    c.mark(1)
    c.ev(js_rola_ate('Abertura do Caixa #85', y=560, dur_ms=1100), at=0.2, label='rola até o Histórico de Transações')
    c.hover(SEL("main tbody tr:has-text('Abertura do Caixa #85')"), at=c.A(1, 'linha', 0.5), label='ZOOM linha Abertura do Caixa #85 R$ 1.500,00 (L1)')
    c.mark(2)
    c.ev(js_rola_topo(900), at=c.A(2, 'Agora', -1.0), label='volta ao topo (sob a ilustração)')
    c.mark(3)
    c.mark(4)
    c.click(INICIO, at=c.A(4, 'Início', 0.6), label='aba Início')
    c.click(ABRIR, at=c.A(4, 'abre', 0.6), label='Abrir Caixa (para outro usuário)')
    c.waitfor(text='Informe o saldo inicial em dinheiro', exact=False, timeout=10)
    c.click(USUARIO, at=c.A(4, 'Abrir', 1.1), label='Abrir para o usuário (vem a Juliana)')
    c.click(OPT('Marcos Antunes'), at=c.A(4, 'Marcos', 0.5, nth=1), label='escolhe Marcos Antunes')
    c.mark(5)
    c.hover(TXTX('O caixa será aberto sem dinheiro em espécie', DLG), at=c.A(5, 'aviso', 0.5), label='ZOOM aviso amarelo do zero (L5)')
    c.mark(6)
    c.hover(CAMPO_ABERTURA, at=c.A(6, 'caixa', 0.5), label='campo Saldo de Abertura vazio')
    c.fim()
    return c


@cap
def cap04():
    """O cofre: "Disponível no cofre agora" no diálogo do Marcos (aberto no setup); ilustração cofre x caixa (L2 a L5)."""
    c = Cap(4, setup_caixa(abrir_dialogo_marcos()))
    c.mark(1)
    c.confere('dlg', ['Disponível no cofre agora: R$ 17.000,00', 'de R$ 18.500,00 total', 'R$ 1.500,00 está dentro de caixas abertos'],
              'cofre: 17.000 de 18.500, 1.500 em caixas abertos')
    c.hover(TXTX('Disponível no cofre agora', DLG), at=c.A(1, 'disponível', 0.5), label='ZOOM Disponível no cofre agora R$ 17.000,00 (L1)')
    c.mark(2)
    c.mark(3)
    c.mark(4)
    c.mark(5)
    c.mark(6)
    c.hover(CAMPO_ABERTURA, at=c.A(6, 'abrir', 0.5), label='campo Saldo de Abertura')
    c.fim()
    return c


@cap
def cap05():
    """Saldo insuficiente: 20.000,00 para o Marcos, o aviso do cofre, as duas saídas, "Usar disponível" e o #86 aberto."""
    c = Cap(5, setup_caixa(abrir_dialogo_marcos()))
    c.mark(1)
    c.click(CAMPO_ABERTURA, at=c.A(1, 'Digito', 0.6), label='campo Saldo de Abertura')
    c.type(CAMPO_ABERTURA, '20.000,00', at=c.A(1, 'vinte', 0.05, nth=1), label='ZOOM digita 20.000,00 (L1)', noClick=True)
    c.confere_campo('#openingBalance', '20.000,00', 'campo com 20.000,00')
    c.mark(2)
    c.click(ABRIR_DLG, at=c.A(2, 'Abrir', 0.6), label='Abrir Caixa (janela)')
    c.waitfor(text='Saldo insuficiente em dinheiro', exact=False, timeout=10)
    c.hover(TXTX('Saldo insuficiente em dinheiro', ALERTA_COFRE), at=c.A(2, 'Saldo', 0.5), label='aviso Saldo insuficiente em dinheiro')
    c.mark(3)
    c.confere('dlg', ['Você tentou abrir com R$ 20.000,00', 'há apenas R$ 17.000,00 disponíveis', 'R$ 1.500,00 já reservados em caixas abertos'],
              'aviso: 20.000 x 17.000 (1.500 reservados)')
    c.hover(TXTX('O caixa só pode abrir com o dinheiro', ALERTA_COFRE), at=c.A(3, 'caixa', 0.5, nth=0), label='ZOOM texto do aviso do cofre (L3)')
    c.mark(4)
    c.hover(BTNX('Usar disponível', ALERTA_COFRE), at=c.A(4, 'Usar', 0.5), label='Usar disponível (R$ 17.000,00)')
    c.mark(5)
    c.hover(BTN('Ajustar saldo do dinheiro', ALERTA_COFRE), at=c.A(5, 'Ajustar', 0.5), label='Ajustar saldo do dinheiro')
    c.mark(6)
    c.hover(BTN('Ajustar saldo do dinheiro', ALERTA_COFRE), at=c.A(6, 'ajuste', 0.5), label='ajuste o cofre uma vez só')
    c.mark(7)
    c.click(BTNX('Usar disponível', ALERTA_COFRE), at=c.A(7, 'Usar', 0.6), label='Usar disponível')
    c.confere_campo('#openingBalance', '17.000,00', 'campo com 17.000,00')
    c.click(ABRIR_DLG, at=c.A(7, 'Abrir', 0.6), label='Abrir Caixa (janela)')
    c.waitfor(text='Caixa aberto com sucesso!', timeout=10)
    c.hover(TXT('R$ 17.000,00'), at=c.A(7, 'aberto', 0.5), label='Dinheiro em Caixa R$ 17.000,00 (#86)')
    c.confere('main', ['#86 | Caixa - Marcos Antunes', 'R$ 17.000,00', 'Aberto em: 10/11/2026 08:42'], 'caixa #86 do Marcos aberto às 08:42')
    c.fim()
    return c


@cap
def cap06():
    """Os dois cartões: Dinheiro em Caixa (#85), Aberto em e Dinheiro total da empresa > o cofre e a barra; Saldo Bancário; o olho."""
    c = Cap(6, setup_caixa([{'do': 'waitFor', 'text': '#86 | Caixa - Marcos Antunes', 'timeout': 15}, {'do': 'click', 'target': TAB85},
                            {'do': 'waitFor', 'text': 'Aberto em: 10/11/2026 08:31', 'timeout': 10}]))
    c.mark(1)
    c.hover(TXT('Dinheiro em Caixa'), at=c.A(1, 'Dinheiro', 0.5, nth=0), label='cartão Dinheiro em Caixa')
    c.hover(TXT('R$ 1.500,00'), at=c.A(1, 'mil', 0.5), label='R$ 1.500,00 do meu caixa')
    c.mark(2)
    c.confere('main', ['Aberto em: 10/11/2026 08:31', 'Dinheiro total da empresa:', 'R$ 18.500,00'], 'aberto 08:31 e cofre R$ 18.500,00')
    c.hover(TXTX('Aberto em:'), at=c.A(2, 'hora', 0.5), label='ZOOM Aberto em e Dinheiro total da empresa (L2)')
    c.hover(TOTAL, at=c.A(2, 'Dinheiro', 0.5), label='Dinheiro total da empresa: R$ 18.500,00')
    c.mark(3)
    c.click(TOTAL, at=c.A(3, 'Clicando', 0.4), label='Dinheiro total da empresa (abre o cofre)')
    c.waitfor(text='O cofre da empresa', timeout=12)
    c.mark(4)
    c.confere('main', ['O cofre da empresa', 'R$ 18.500,00', 'Disponível no cofre: R$ 0,00 (0%)', 'Caixa de Rafael Nogueira: R$ 1.500,00 (8%)',
                       'Caixa de Marcos Antunes: R$ 17.000,00 (92%)'], 'barra do cofre (0 / 1.500 / 17.000)')
    c.hover(TXT('92%'), at=c.A(4, 'barra', 0.5), label='ZOOM barra e legenda do cofre (L4)')
    c.hover(BTNX('Caixa de Rafael Nogueira:', MAIN), at=c.A(4, 'mil', 0.5), label='Caixa de Rafael Nogueira: R$ 1.500,00 (8%)')
    c.hover(BTNX('Caixa de Marcos Antunes:', MAIN), at=c.A(4, 'dezessete', 0.5), label='Caixa de Marcos Antunes: R$ 17.000,00 (92%)')
    c.hover(BTNX('Disponível no cofre:', MAIN), at=c.A(4, 'nada', 0.5), label='Disponível no cofre: R$ 0,00 (0%)')
    c.mark(5)
    # no /movimentacoes-bancarias o grupo Financeiro do menu vem fechado: abre o grupo e clica em Caixa
    c.click(FIN, at=c.A(5, 'De', 0.6), label='menu Financeiro')
    c.click(LINK('Caixa'), at=c.A(5, 'caixa', 0.5, nth=0), label='menu Caixa (de volta)')
    c.waitfor(text='Gestão financeira e movimentações', timeout=12)
    c.hover(TXT('Saldo Bancário'), at=c.A(5, 'Saldo', 0.5), label='cartão Saldo Bancário')
    c.hover(SAQUE_SANGRIA, at=c.A(5, 'botões', 0.5), label='botões do Saldo Bancário')
    c.mark(6)
    c.click(OLHO, at=c.A(6, 'olhinho', 0.6), label='olho Ocultar saldo')
    c.marcar(TXT('R$ ••••••'), at=c.A(6, 'pontinhos', 0.3), label='ZOOM R$ •••••• (L6 e L7)')
    c.mark(7)
    c.click(OLHO2, at=c.A(7, 'Permissões', 0.6), label='olho Mostrar saldo')
    c.fim()
    return c


@cap
def cap07():
    """Multi-caixa: as abas, o "?" (Como funcionam os Multi-Caixas?), a aba Início com o Painel Gerencial."""
    c = Cap(7, setup_caixa([{'do': 'waitFor', 'text': '#86 | Caixa - Marcos Antunes', 'timeout': 15}, {'do': 'click', 'target': TAB85},
                            {'do': 'waitFor', 'text': 'Aberto em: 10/11/2026 08:31', 'timeout': 10}]))
    c.mark(1)
    c.hover(TAB85, at=c.A(1, 'meu', 0.5), label='ZOOM abas Início, #85 e #86 (L1 e L2)')
    c.hover(TAB86, at=c.A(1, 'Marcos', 0.5), label='aba #86 do Marcos')
    c.mark(2)
    c.mark(3)
    c.click(AJUDA, at=c.A(3, 'ponto', 0.6), label='? Como funcionam os Multi-Caixas')
    c.waitfor(text='Como funcionam os Multi-Caixas?', timeout=10)
    c.hover(TXTX('Transações de caixa (depósitos', DLG), at=c.A(3, 'principal', 0.5), label='item 1: transações de caixa só no caixa selecionado')
    c.mark(4)
    c.hover(TXTX('Saldo bancário (PIX/transferências)', DLG), at=c.A(4, 'banco', 0.5), label='item 2: saldo bancário compartilhado')
    c.hover(TXTX('Saldo de clientes/fornecedores também', DLG), at=c.A(4, 'clientes', 0.5), label='item 3: saldo de clientes/fornecedores')
    c.mark(5)
    c.press('Escape', at=c.L(5) - 0.9, label='fecha a ajuda')
    c.waitfor(gone={'role': 'dialog'}, timeout=6)
    c.click(INICIO, at=c.A(5, 'Início', 0.6), label='aba Início')
    c.waitfor(text='Abrir Caixa para Outro Usuário', timeout=10)
    c.hover(TXT('Painel Gerencial'), at=c.A(5, 'Painel', 0.5), label='Painel Gerencial')
    c.hover(TXT('Resumo do Dia'), at=c.A(5, 'resumo', 0.5), label='Resumo do Dia')
    c.hover(ABRIR, at=c.A(5, 'Abrir', 0.5), label='Abrir Caixa para Outro Usuário')
    c.mark(6)
    c.confere('main', ['2 caixas encontrados'], '2 caixas encontrados')
    c.hover(TXTX('caixas encontrados'), at=c.A(6, 'caixa', 0.5), label='2 caixas encontrados')
    c.fim()
    return c


@cap
def cap08():
    """O caixa dos outros (Rafael, L1 a L3): a aba do Marcos e quem pode operá-la. O cap08b (Marcos) cobre L4 e L5."""
    c = Cap(8, setup_caixa([{'do': 'waitFor', 'text': '#86 | Caixa - Marcos Antunes', 'timeout': 15}, {'do': 'click', 'target': TAB85},
                            {'do': 'waitFor', 'text': 'Aberto em: 10/11/2026 08:31', 'timeout': 10}]))
    c.mark(1)
    c.click(TAB86, at=c.A(1, 'clicar', 0.6), label='aba #86 do Marcos')
    c.waitfor(text='Aberto em: 10/11/2026 08:42', timeout=10)
    c.hover(TXT('R$ 17.000,00'), at=c.A(1, 'dezessete', 0.5), label='R$ 17.000,00 da gaveta do Marcos')
    c.hover(TXTX('Aberto em:'), at=c.A(1, 'hora', 0.5), label='Aberto em 08:42 (#86)')
    c.mark(2)
    c.hover(BTN('Nova Compra', MAIN), at=c.A(2, 'lançar', 0.5, nth=0), label='Nova Compra (vai pro caixa do Marcos)')
    c.hover(BTN('Nova Receita', MAIN), at=c.A(2, 'meu', 0.5), label='Nova Receita')
    c.hover(TAB86, 0.3, at=c.A(2, 'confira', 0.5), label='confira a aba')
    c.mark(3)
    c.hover(TAB85, at=c.A(3, 'administrador', 0.5), label='abas (quem vê e opera os caixas dos outros)')
    c.dur = c.L(4)        # o trecho acaba no início da linha 4: a edição junta o cap08b (Marcos) daí em diante
    c.fim()
    return c


@cap
def cap08b():
    """Corte do cap08, linhas 4 e 5: o Marcos logado no computador da balança vê só o caixa dele (#86), sem as abas."""
    setup = login(EMAIL_MARCOS, None) + IR_CAIXA + [{'do': 'waitFor', 'text': 'Aberto em: 10/11/2026 08:42', 'timeout': 10}]
    c = Cap(8, setup, sub='b', voz_de=(4, 5), user='marcos')
    c.mark(1)
    c.confere('main', ['Dinheiro em Caixa', 'R$ 17.000,00', 'Aberto em: 10/11/2026 08:42'], 'caixa do Marcos sem abas')
    c.confere_js("(()=>document.querySelector('main').innerText.includes('Caixa - Rafael Nogueira')?'DIFERENTE: aparece a aba do Rafael':'OK: sem as abas')()",
                 'sem as abas dos outros caixas')
    # título "Caixa" (y 76) e o selo "#86" (y 83) ficam acima da faixa de clique (y 96): noScroll
    c.hover(TXT('#86'), at=c.A(1, 'caixa', 0.5), label='ZOOM título Caixa com o selo #86, sem abas (L4)', noScroll=True)
    c.mark(2)
    c.hover(TXT('Dinheiro em Caixa'), at=c.A(2, 'Histórico', 0.5), label='o caixa dele (mesma tela)')
    c.fim()
    return c


@cap
def cap09():
    """Saque e sangria: (ilustração L1 a L4); saque de 3.000,00 + tarifa 6,50 para o #86; a opção Sangria; a tarifa mensal de 39,90."""
    c = Cap(9, setup_caixa([{'do': 'waitFor', 'text': '#86 | Caixa - Marcos Antunes', 'timeout': 15}, {'do': 'click', 'target': TAB85},
                            {'do': 'waitFor', 'text': 'Aberto em: 10/11/2026 08:31', 'timeout': 10}]))
    for i in (1, 2, 3, 4, 5):
        c.mark(i)
    c.click(SAQUE_SANGRIA, at=c.A(5, 'botão', 0.6), label='Saque / Sangria')
    c.waitfor(text='Transferir dinheiro do banco para o cofre ou para um caixa aberto', timeout=10)
    c.hover(BTN('Saque', DLG), at=c.A(5, 'Saque', 0.5, nth=1), label='opção Saque marcada')
    c.mark(6)
    c.hover(COMBO(0), at=c.A(6, 'conta', 0.5), label='Conta de origem: Conta Principal')
    c.click(COMBO(1), at=c.A(6, 'destino', 0.6), label='Destino do saque')
    c.click(OPT('Caixa de Marcos Antunes'), at=c.A(6, 'Marcos', 0.5), label='Caixa de Marcos Antunes')
    c.mark(7)
    c.click(VALOR, at=c.A(7, 'Valor', 0.6), label='Valor do Saque')
    c.type(VALOR, '3.000,00', at=c.A(7, 'três', 0.05), label='ZOOM digita R$ 3.000,00 (L7)', noClick=True)
    c.mark(8)
    c.ev(js_rola_ate('Tem tarifa no saque?', y=330, dur_ms=700, esc=DLG), at=c.L(8) - 0.9, label='desce a janela até a tarifa')
    c.click(COMBO(2), at=c.A(8, 'tarifa', 0.6), label='Tem tarifa no saque?')
    c.click(OPT('Sim', exact=True), at=c.A(8, 'sim', 0.5), label='Sim')
    c.click(TARIFA, label='Valor da Tarifa')
    c.type(TARIFA, '6,50', at=c.A(8, 'seis', 0.05), label='ZOOM digita R$ 6,50 (L8)', noClick=True)
    c.mark(9)
    c.ev(js_rola_ate('Efeitos desta transação:', y=300, dur_ms=700, esc=DLG), at=c.L(9) - 0.9, label='desce a janela até os efeitos')
    c.confere('dlg', ['Diminuirá em R$ 3006,50', '(Saque: R$ 3.000,00 + Tarifa: R$ 6,50)', 'Aumentará em R$ 3.000,00'], 'efeitos do saque')
    c.hover(TXT('Saldo da Conta Bancária', DLG), at=c.A(9, 'conta', 0.5), label='ZOOM Efeitos desta transação (L9 e L10)')
    c.hover(TXTX('Diminuirá em', DLG), at=c.A(9, 'diminui', 0.5), label='Diminuirá em R$ 3006,50')
    c.hover(TXTX('Aumentará em', DLG), at=c.A(9, 'aumenta', 0.5), label='Aumentará em R$ 3.000,00')
    c.mark(10)
    c.mark(11)
    c.click(BTN('Confirmar Saque', DLG), at=c.A(11, 'Confirmar', 0.6), label='Confirmar Saque')
    c.waitfor(text='Saque realizado com sucesso!', timeout=10)
    c.mark(12)
    c.click(SAQUE_SANGRIA, at=c.L(12) - 0.9, label='Saque / Sangria (de novo)')
    c.waitfor(text='Transferir dinheiro do banco para o cofre ou para um caixa aberto', timeout=10)
    c.click(BTN('Sangria', DLG), at=c.A(12, 'Sangria', 0.6), label='opção Sangria')
    c.waitfor(text='Transferir dinheiro do cofre ou de um caixa aberto para uma conta bancária', timeout=8)
    c.hover(COMBO(0), at=c.A(12, 'sai', 0.5), label='Origem da sangria')
    c.hover(COMBO(1), at=c.A(12, 'conta', 0.5), label='Conta de destino')
    # a sangria não é confirmada: Esc fecha a janela no fim da frase (o "Cancelar" fica abaixo da dobra, y 886: rolar e clicar não
    # cabe no vão entre as linhas 12 e 13)
    c.mark(13)
    c.press('Escape', at=c.A(12, 'recebe', -0.3), label='fecha a janela (sangria sem confirmar)')
    c.waitfor(gone={'role': 'dialog'}, timeout=6)
    c.click(NOVA_MOV, at=c.A(13, 'Nova', 0.6), label='Nova Movimentação Bancária')
    c.waitfor(text='Nova Movimentação Financeira', timeout=10)
    c.click(COMBO(0), at=c.A(13, 'tarifa', 0.6), label='Conta bancária')
    c.click(OPT('Conta Secundária'), at=c.A(13, 'conta', 0.5), label='Conta Secundária')
    c.mark(14)
    c.click(BTN('Saída', DLG), at=c.A(14, 'Saída', 0.6), label='Tipo Saída')
    c.click(DESCRICAO, at=c.A(14, 'descrição', 0.6), label='Descrição')
    colar(c, f'{DLG} #description', 'Tarifa mensal do pacote de serviços', label='cola a descrição')
    c.click(VALOR, at=c.A(14, 'trinta', 0.6), label='Valor')
    c.type(VALOR, '39,90', at=c.A(14, 'nove', 0.05, nth=0), label='digita R$ 39,90', noClick=True)
    c.click(COMBO(1), at=c.A(14, 'categoria', 0.6), label='Categoria')
    c.click(OPT('Tarifas', exact=True), at=c.A(14, 'Tarifas', 0.4), label='categoria Tarifas')
    c.mark(15)
    c.confere('dlg', ['Conta Secundária', 'Tarifas'], 'conta Secundária e categoria Tarifas')
    c.confere_campo(f'{DLG} #description', 'Tarifa mensal do pacote de serviços', 'descrição')
    c.confere_campo(f'{DLG} #amount', 'R$ 39,90', 'valor R$ 39,90')
    c.click(BTN('Salvar', DLG), at=c.A(15, 'Salvar', 0.6), label='Salvar')
    c.waitfor(text='Movimentação registrada com sucesso!', timeout=10)
    c.fim()
    return c


FECHAMENTO = SEL(f'{DLG} #closingBalance')                            # "Valor de Fechamento" (vem com o esperado; Caixa.tsx:3503)
LINHA_CX = lambda n: SEL(f"{DLG} button:has-text('#{n}')")             # linha da lista "Reabrir outro caixa" (a 1a; o rodapé tem "Reabrir #N")
LINHA = lambda txt: SEL(f"main tbody tr:has-text('{txt}')")


@cap
def cap10():
    """Fechar o caixa às 17:40 (semente dia-10): o movimento do dia, o botão sem cadeado, a conta do dia, conferir e fechar."""
    c = Cap(10, setup_caixa([{'do': 'waitFor', 'text': '#86 | Caixa - Marcos Antunes', 'timeout': 15}, {'do': 'click', 'target': TAB85},
                             {'do': 'waitFor', 'text': 'Aberto em: 10/11/2026 08:31', 'timeout': 10},
                             {'do': 'waitFor', 'text': 'Aços Quiririm Ltda', 'timeout': 10}]))
    c.mark(1)
    c.confere('main', ['R$ 1.007,10', 'Aços Quiririm Ltda', 'Aparecida Ramos', 'Valdir Pereira'], 'movimento do dia no #85')
    c.hover(TXT('R$ 1.007,10'), at=c.A(1, 'caixa', 0.5, nth=0), label='Dinheiro em Caixa R$ 1.007,10')
    c.ev(js_rola_ate('Histórico de Transações', y=120, dur_ms=1000, prefixo=False), at=c.A(1, 'venda', 1.2), label='desce ao Histórico de Transações')
    c.hover(LINHA('Aços Quiririm Ltda'), at=c.A(1, 'Aços', 0.5), label='venda Aços Quiririm (Pix/Transferência)')
    c.hover(LINHA('Aparecida Ramos'), at=c.A(1, 'Aparecida', 0.5), label='compra da Aparecida (Dinheiro)')
    c.hover(LINHA('Valdir Pereira'), at=c.A(1, 'Valdir', 0.5), label='compra do Valdir (Dinheiro)')
    c.mark(2)
    c.ev(js_rola_topo(900), at=c.L(2) - 0.9, label='volta ao topo')
    c.hover(BTN('Fechar Caixa', MAIN), at=c.A(2, 'Fechar', 0.5), label='Fechar Caixa (sem cadeado)')
    c.mark(3)
    c.mark(4)
    c.click(BTN('Fechar Caixa', MAIN), at=c.A(4, 'Fechar', 0.6), label='Fechar Caixa')
    c.waitfor(text='Fechar Caixa #85', timeout=10)
    c.waitfor(text='Valor esperado pelo sistema', timeout=15)
    c.mark(5)
    c.confere('dlg', ['Saldo de Abertura', 'R$ 1.500,00', 'Restante em Caixa', 'R$ 1.007,10', 'Compras', 'R$ 492,90'],
              'conta do dia: 1.500,00 - 492,90 = 1.007,10')
    c.hover(TXT('Saldo de Abertura', DLG), at=c.A(5, 'Abriu', 0.5), label='ZOOM cartões do fechamento (L5 e L6)')
    c.hover(TXT('Compras', DLG), at=c.A(5, 'compras', 0.5), label='Compras R$ 492,90 (Dinheiro)')
    c.mark(6)
    c.hover(TXT('Restante em Caixa', DLG), at=c.A(6, 'Restante', 0.5), label='Restante em Caixa R$ 1.007,10')
    c.mark(7)
    c.mark(8)
    c.mark(9)
    c.confere_campo(f'{DLG} #closingBalance', '1.007,10', 'Valor de Fechamento já com o esperado')
    c.hover(FECHAMENTO, at=c.A(9, 'Valor', 0.5), label='Valor de Fechamento (já com o esperado)')
    c.mark(10)
    c.click(FECHAMENTO, at=c.A(10, 'Contei', 0.6), label='campo Valor de Fechamento')
    c.type(FECHAMENTO, '1.007,10', at=c.A(10, 'mil', 0.05), label='ZOOM digita 1.007,10 e o valor esperado (L10)', noClick=True, clear=True)
    c.mark(11)
    c.hover(TXTX('Valor esperado pelo sistema', DLG), at=c.A(11, 'diferença', 0.5, nth=0), label='Valor esperado pelo sistema: R$ 1.007,10')
    c.mark(12)
    c.mark(13)
    c.click(BTN('Confirmar Fechamento', DLG), at=c.A(13, 'Confirmar', 0.6), label='Confirmar Fechamento')
    c.waitfor(text='Deseja imprimir o relatório de fechamento de caixa?', timeout=12)
    c.mark(14)
    c.click(BTN('Não, obrigado'), at=c.A(14, 'não', 0.6), label='Não, obrigado')
    c.waitfor(text='Meu Caixa', timeout=10)
    c.fim()
    return c


@cap
def cap11():
    """Reabrir: o cartão amarelo do #85, "reabrir outro caixa" (todos os operadores), "Reabrir #85" e a confirmação."""
    c = Cap(11, setup_caixa([{'do': 'waitFor', 'text': 'Reabrir #85', 'timeout': 15}]))
    c.mark(1)
    c.hover(BTN('Reabrir #85', MAIN), at=c.A(1, 'reabrir', 0.5), label='Reabrir #85')
    c.mark(2)
    c.confere('main', ['#85', 'R$ 1.007,10', 'reabrir outro caixa'], 'cartão amarelo do #85 com R$ 1.007,10')
    c.hover(CARD_AMARELO, at=c.A(2, 'cartão', 0.5), label='ZOOM cartão amarelo #85 (L2)')
    c.mark(3)
    c.click(BTN('reabrir outro caixa', MAIN), at=c.A(3, 'reabrir', 0.6), label='reabrir outro caixa')
    c.waitfor(text='Escolha qual caixa fechado deseja reabrir', timeout=10)
    c.confere('dlg', ['#85', 'R$ 1.007,10', '#84', 'R$ 1.250,00', '#83', 'Marcos Antunes', 'R$ 640,00'], 'lista: #85, #84 e #83 do Marcos')
    c.hover(LINHA_CX(84), at=c.A(3, 'operadores', 0.5), label='lista dos últimos caixas fechados (#84)')
    c.mark(4)
    c.hover(LINHA_CX(83), at=c.A(4, 'outra', 0.5), label='o #83 do Marcos (R$ 640,00)')
    c.mark(5)
    c.hover(LINHA_CX(85), at=c.A(5, 'meu', 0.5), label='o #85 já marcado')
    c.click(BTN('Reabrir #85', DLG), at=c.A(5, 'reabrir', 0.6), label='Reabrir #85 (lista)')
    c.waitfor(text='Reabrir caixa #85?', timeout=10)
    c.hover(TXTX('O caixa será reaberto exatamente como estava', ALERTA), at=c.A(5, 'confirma', 0.5), label='Reabrir caixa #85? (como estava)')
    c.mark(6)
    c.click(BTN('Reabrir Caixa'), at=c.A(6, 'Reabrir', 0.6), label='Reabrir Caixa')
    c.waitfor(text='Caixa reaberto com sucesso!', timeout=10)
    c.hover(TXT('R$ 1.007,10'), at=c.A(6, 'aberto', 0.5), label='Dinheiro em Caixa R$ 1.007,10 (#85 reaberto)')
    c.fim()
    return c


@cap
def cap12():
    """Recapitulando (a montagem da edição usa trechos dos capítulos): passeio de reserva pelo estado final (17:42, #85 reaberto)."""
    c = Cap(12, setup_caixa([{'do': 'waitFor', 'text': '#86 | Caixa - Marcos Antunes', 'timeout': 15}, {'do': 'click', 'target': TAB85},
                             {'do': 'waitFor', 'text': 'Aberto em: 10/11/2026 08:31', 'timeout': 10}]))
    c.mark(1)
    c.hover(TAB85, at=c.A(1, 'caixa', 0.5, nth=0), label='aba #85')
    c.mark(2)
    c.hover(TXT('R$ 1.007,10'), at=c.A(2, 'dinheiro', 0.5), label='Dinheiro em Caixa')
    c.mark(3)
    c.hover(TOTAL, at=c.A(3, 'cofre', 0.5), label='Dinheiro total da empresa (o cofre)')
    c.mark(4)
    c.hover(TAB86, at=c.A(4, 'Marcos', 0.5), label='aba do Marcos')
    c.mark(5)
    c.hover(SAQUE_SANGRIA, at=c.A(5, 'saque', 0.5), label='Saque / Sangria')
    c.mark(6)
    c.hover(BTN('Fechar Caixa', MAIN), at=c.A(6, 'fechou', 0.5), label='Fechar Caixa')
    c.mark(7)
    c.fim()
    return c


# ================================================================ saída
if __name__ == '__main__':
    pedidos = [a.lower() for a in sys.argv[1:]]
    quais = list(CAPS_FN) if not pedidos else [k for k in CAPS_FN if k in pedidos or k.lstrip('0') in [p.lstrip('0') for p in pedidos]]
    for k in quais:
        c = CAPS_FN[k]()
        d = c.out()
        caminho = os.path.join(HERE, f'{c.nome}.json')
        json.dump(d, open(caminho, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
        print(f'{c.nome}: {len(d["steps"])} passos, narração {c.dur:.1f} s{" (estimada)" if c.estimado else ""}, sementes {d["seedExtra"]}')
        if os.environ.get('ANCORAS'):
            for i, p, t in c.anchors:
                print(f'   L{i} "{p}" -> at {t}')
