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
_T = lambda hms: f'2026-11-10T{hms}-03:00'
FAKE_NOW = {0: MANHA, 1: MANHA, 2: _T('08:30:55'), 3: _T('08:41:50'), 4: _T('08:41:50'), 5: _T('08:41:50'), 6: _T('08:43:30'),
            7: _T('08:45:00'), 8: _T('08:45:00'), 9: _T('08:45:00'), 10: _T('08:45:00'), 11: _T('08:55:00'), 12: _T('17:30:00'),
            13: TARDE, 14: _T('17:42:40'), 15: _T('17:44:00')}
NOMES = ['Abertura', 'O caixa fechado', 'Abrir o caixa', 'Abrir com zero', 'O cofre da empresa', 'Saldo insuficiente',
         'Cofre zerado ou negativo', 'Os dois cartões', 'Cada um com o seu caixa', 'O caixa dos outros', 'Saque e sangria',
         'Despesa e receita do dia', 'Sangria no fim do dia', 'Fechar o caixa', 'Reabrir um caixa', 'Recapitulando']
# sementes (rec/mundo/seeds-extra/t06/): cada uma soma só o que o capítulo fez; o roteiro empilha
_C = [f'{AULA}/apos-cap02', f'{AULA}/apos-cap05', f'{AULA}/apos-cap10', f'{AULA}/apos-cap11', f'{AULA}/dia-10', f'{AULA}/apos-cap12',
      f'{AULA}/apos-cap13', f'{AULA}/apos-cap14']
SEMENTE = {0: [], 1: [], 2: [], 3: _C[:1], 4: _C[:1], 5: _C[:1], 6: _C[:2], 7: _C[:2], 8: _C[:2], 9: _C[:2], 10: _C[:2],
           11: _C[:3], 12: _C[:5], 13: _C[:6], 14: _C[:7], 15: _C[:8]}
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
    def __init__(s, n, setup, pace=0.5, cps=40, start=(760, 470), prewarm=('/login',), sub='', voz_de=None, user='rafael', erros_ok=(), sementes=()):
        s.n, s.sub = n, sub
        s.sementes = list(sementes)
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
            'seedExtra': list(SEMENTE[s.n]) + s.sementes,
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


VERSAO = '1.60.18'
HOJE = MANHA[:10]


def storage(user='rafael'):
    """localStorage que a sessão pronta do robô poria (mundo.json, navegador.localStorage): versão já vista, PWA dispensado, tema claro,
    lembrete de tarefas do dia já mostrado e preferências iniciais."""
    uid = stable_id(f'user.{user}')
    # o balão de adoção do Cato (1.60.0) cobriria a coluna Ações do histórico: já mostrado 99 vezes (mundo.json, navegador.localStorage)
    return {'app_version': VERSAO, 'notification_shown_version': VERSAO, 'pwa-install-dismissed': 'true', 'theme': 'light',
            f'daily-tasks-reminder-last-shown-{uid}': HOJE, 'initial-preferences-set': 'true',
            f'cato_adoption_nudge_{stable_id("company.reciclavale")}_{uid}': '{"count":99,"lastShownAt":0}'}


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
PONTINHOS_ABERTURA = SEL("main tbody tr:has-text('Abertura do Caixa #85') button[aria-label='Abrir ações da movimentação']")   # menu da linha de abertura
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
    # L5 e L6 (1.60.18, cobertura P3): a data retroativa e a primeira abertura da vida da empresa (só fala)
    c.mark(5)
    c.hover(SEL(f'{DLG} label[for=customOpenDatetime]'), at=c.A(5, 'Data', 0.5, nth=0), label='ZOOM Data e Hora de Abertura (L5)')
    c.hover(TXTX('Altere para abrir o caixa com data/hora retroativa', DLG), at=c.A(5, 'Ela', 0.5), label='Altere para abrir o caixa com data/hora retroativa')
    c.mark(6)
    c.hover(SEL(f'{DLG} #customOpenDatetime'), at=c.A(6, 'primeiro', 0.5), label='campo Data e Hora de Abertura (L6)')
    c.mark(7)
    t = c.A(7, 'Abrir', 1.2)
    c.marca_em(7, t)
    c.click(ABRIR_DLG, at=t, label='Abrir Caixa (janela)')
    c.waitfor(text='Caixa aberto com sucesso!', timeout=10)
    c.hover(TXT('R$ 1.500,00'), at=c.A(7, 'mil', 0.5), label='Dinheiro em Caixa R$ 1.500,00 (#85)')
    c.confere('main', ['#85 | Caixa - Rafael Nogueira', 'Dinheiro em Caixa', 'R$ 1.500,00', 'Aberto em: 10/11/2026 08:31'], 'caixa #85 aberto às 08:31')
    c.fim()
    return c


@cap
def cap03():
    """Abrir com zero: a linha de abertura no histórico e Editar saldo de abertura (L1 a L4); (ilustração do dia só de Pix, L5 e L6);
    o caixa do Marcos com o campo vazio (L7 a L9)."""
    c = Cap(3, setup_caixa([{'do': 'waitFor', 'text': 'Abertura do Caixa #85', 'timeout': 15}]))
    c.mark(1)
    c.ev(js_rola_ate('Abertura do Caixa #85', y=560, dur_ms=1100), at=0.2, label='rola até o Histórico de Transações')
    c.hover(LINHA('Abertura do Caixa #85'), at=c.A(1, 'linha', 0.5), label='ZOOM linha Abertura do Caixa #85 R$ 1.500,00 (L1)')
    c.mark(2)
    # cobertura P2: os três pontinhos da linha de abertura > Editar saldo de abertura (a janela só é aberta e cancelada)
    # 1.60.18: o menu da linha abre no HOVER (handleDropdownEnter em TransactionHistory.tsx); o clique logo depois o fechava
    c.hover(PONTINHOS_ABERTURA, 0.8, at=c.A(2, 'pontinhos', 0.6), label='três pontinhos da linha Abertura (o menu abre ao passar o mouse)')
    c.ev("(async()=>{for(let i=0;i<40;i++){const e=[...document.querySelectorAll('[role=menuitem]')].find(e=>/editar saldo de abertura/i.test(e.textContent||''));"
         "if(e){e.click();return 'ok'}await new Promise(r=>setTimeout(r,250))}return 'SEM ALVO: '+[...document.querySelectorAll('[role=menuitem]')].map(e=>e.textContent.trim()).join('|')})()",
         at=c.A(2, 'Editar', 0.2), label='Editar saldo de abertura')
    c.waitfor(text='Editar Saldo de Abertura', timeout=10)
    c.confere('dlg', ['Saldo de Abertura Atual', 'R$ 1.500,00', 'Novo Saldo de Abertura'], 'janela Editar Saldo de Abertura (R$ 1.500,00)')
    c.mark(3)
    c.hover(TXTX('alterar o saldo de abertura ajusta o Dinheiro em Caixa', DLG), at=c.A(3, 'Você', 0.5), label='ZOOM Atenção: alterar o saldo de abertura (L3)')
    c.click(BTN('Cancelar', DLG), at=c.A(3, 'cancelo', 0.6), label='Cancelar')
    c.waitfor(gone={'role': 'dialog'}, timeout=6)
    c.mark(4)
    c.hover(SEL("main input[placeholder='Buscar transação...']"), at=c.A(4, 'buscar', 0.5), label='Buscar transação...')
    c.hover(BTNX('Filtros', MAIN), at=c.A(4, 'filtrar', 0.5), label='Filtros')
    c.hover({'role': 'button', 'name': 'Pix/Transferência', 'exact': True, 'within': MAIN}, 0.4, at=c.A(4, 'corrigir', 0.5), label='abas Todas, Dinheiro e Pix/Transferência')
    c.mark(5)
    c.ev(js_rola_topo(900), at=c.A(5, 'Agora', -1.0), label='volta ao topo (sob a ilustração)')
    c.mark(6)
    c.mark(7)
    c.click(INICIO, at=c.A(7, 'Início', 0.6), label='aba Início')
    c.click(ABRIR, at=c.A(7, 'abre', 0.6), label='Abrir Caixa (para outro usuário)')
    c.waitfor(text='Informe o saldo inicial em dinheiro', exact=False, timeout=10)
    c.click(USUARIO, at=c.A(7, 'Abrir', 1.1), label='Abrir para o usuário (vem a Juliana)')
    c.click(OPT('Marcos Antunes'), at=c.A(7, 'Marcos', 0.5, nth=1), label='escolhe Marcos Antunes')
    c.mark(8)
    c.hover(TXTX('O caixa será aberto sem dinheiro em espécie', DLG), at=c.A(8, 'aviso', 0.5), label='ZOOM aviso amarelo do zero (L8)')
    c.mark(9)
    c.hover(CAMPO_ABERTURA, at=c.A(9, 'caixa', 0.5), label='campo Saldo de Abertura vazio')
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
    """Saldo insuficiente: 20.000,00 para o Marcos, o aviso do cofre, o link do tutorial, as duas saídas, "Usar disponível" e o #86 aberto."""
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
    c.confere('dlg', ['Ver tutorial: como funciona o dinheiro do caixa'], 'link Ver tutorial (handoff 19/11)')
    c.hover(TXTX('Ver tutorial: como funciona o dinheiro do caixa', ALERTA_COFRE), at=c.A(4, 'link', 0.5), label='link Ver tutorial: como funciona o dinheiro do caixa')
    c.mark(5)
    c.hover(BTNX('Usar disponível', ALERTA_COFRE), at=c.A(5, 'Usar', 0.5), label='Usar disponível (R$ 17.000,00)')
    c.mark(6)
    c.hover(BTN('Ajustar saldo do dinheiro', ALERTA_COFRE), at=c.A(6, 'Ajustar', 0.5), label='Ajustar saldo do dinheiro')
    c.mark(7)
    c.hover(BTN('Ajustar saldo do dinheiro', ALERTA_COFRE), at=c.A(7, 'ajuste', 0.5), label='ajuste o cofre uma vez só')
    c.mark(8)
    c.click(BTNX('Usar disponível', ALERTA_COFRE), at=c.A(8, 'Usar', 0.6), label='Usar disponível')
    c.confere_campo('#openingBalance', '17.000,00', 'campo com 17.000,00')
    c.click(ABRIR_DLG, at=c.A(8, 'Abrir', 0.6), label='Abrir Caixa (janela)')
    c.waitfor(text='Caixa aberto com sucesso!', timeout=10)
    c.hover(TXT('R$ 17.000,00'), at=c.A(8, 'aberto', 0.5), label='Dinheiro em Caixa R$ 17.000,00 (#86)')
    c.confere('main', ['#86 | Caixa - Marcos Antunes', 'R$ 17.000,00', 'Aberto em: 10/11/2026 08:42'], 'caixa #86 do Marcos aberto às 08:42')
    c.fim()
    return c


# o POST do robô ao /__dev/seed do Supabase falso, de dentro da página (o build chama o 54340; o runner desvia para a instância da aula)
SEMEIA = ("(async()=>{try{const r=await fetch('http://127.0.0.1:54340/__dev/seed',{method:'POST',headers:{'content-type':'application/json'},"
          "body:JSON.stringify({files:%s})});return r.ok?'seed ok':'SEED FALHOU '+r.status}catch(e){return 'SEED ERRO '+e}})()")
DATA_PAINEL = 'main button:has-text("Hoje")'                               # seletor de data do Painel Gerencial (CashRegisterHomePanel.tsx:654)
HOJE_PAINEL = 'main button:text-is("Hoje")'
DIA_9 = '[role=grid] button:text-is("9")'
OLHO_RESUMO = 'main button[aria-label="Ocultar valores"]'
OLHO_RESUMO2 = 'main button[aria-label="Mostrar valores"]'
TAB87 = BTNX('#87 | Caixa - Juliana Prado', MAIN)


@cap
def cap06():
    """Cofre zerado ou negativo (handoff 19/11, app 1.60.18): com os dois caixas abertos o disponível é zero; o aviso, "Abrir zerado"; depois
    o cofre negativo (saída de R$ 1.200,00 lançada fora do vídeo) e o caixa da Juliana aberto zerado, sem barrar."""
    setup = setup_caixa([{'do': 'waitFor', 'text': '#86 | Caixa - Marcos Antunes', 'timeout': 15},
                         {'do': 'click', 'target': INICIO}, {'do': 'waitFor', 'text': 'Abrir Caixa para Outro Usuário', 'timeout': 10},
                         {'do': 'click', 'target': ABRIR}, {'do': 'waitFor', 'text': 'Informe o saldo inicial em dinheiro', 'exact': False, 'timeout': 10},
                         {'do': 'waitFor', 'text': 'Disponível no cofre agora', 'exact': False, 'timeout': 10}, {'do': 'wait', 'seconds': 0.6}])
    c = Cap(6, setup)
    c.mark(1)
    c.confere('dlg', ['Disponível no cofre agora: R$ 0,00', 'de R$ 18.500,00 total', 'R$ 18.500,00 está dentro de caixas abertos'],
              'cofre: disponível 0 de 18.500 (todo em caixas abertos)')
    c.hover(TXTX('Disponível no cofre agora', DLG), at=c.A(1, 'disponível', 0.5), label='ZOOM Disponível no cofre agora R$ 0,00 (L1)')
    c.mark(2)
    c.click(CAMPO_ABERTURA, at=c.A(2, 'Digito', 0.6), label='campo Saldo de Abertura')
    c.type(CAMPO_ABERTURA, '500,00', at=c.A(2, 'quinhentos', 0.05, nth=1), label='ZOOM digita 500,00 (L2)', noClick=True)
    c.confere_campo('#openingBalance', '500,00', 'campo com 500,00')
    c.click(ABRIR_DLG, at=c.A(2, 'Abrir', 0.6, nth=1), label='Abrir Caixa (janela)')
    c.waitfor(text='Saldo insuficiente em dinheiro', exact=False, timeout=10)
    c.mark(3)
    c.confere('dlg', ['Você tentou abrir com R$ 500,00', 'há apenas R$ 0,00 disponíveis', 'R$ 18.500,00 já reservados em caixas abertos'],
              'aviso: 500 x 0 (18.500 reservados)')
    c.hover(TXTX('O caixa só pode abrir com o dinheiro', ALERTA_COFRE), at=c.A(3, 'aviso', 0.5), label='ZOOM texto do aviso, cofre zerado (L3)')
    c.mark(4)
    c.hover(BTNX('Abrir zerado', ALERTA_COFRE), at=c.A(4, 'botão', 0.5), label='Abrir zerado (R$ 0,00) no lugar de Usar disponível')
    c.hover(BTN('Ajustar saldo do dinheiro', ALERTA_COFRE), at=c.A(4, 'Ajustar', 0.5), label='Ajustar saldo do dinheiro')
    c.mark(5)
    # fora do vídeo: fecha o aviso (o campo segue com 500,00) e lança a saída de R$ 1.200,00 no cofre; o clique volta a barrar, agora negativo
    c.press('Escape', at=c.A(5, 'imagina', 0.3), label='fecha o aviso (o campo segue com 500,00)')
    c.ev(SEMEIA % json.dumps([f'{AULA}/cofre-negativo']), label='semente: saída de R$ 1.200,00 no cofre (fora do vídeo)')
    c.confere_campo('#openingBalance', '500,00', 'campo ainda com 500,00')
    c.click(ABRIR_DLG, at=c.A(5, 'Clico', 0.6), label='Abrir Caixa (de novo)')
    c.waitfor(text='o cofre está negativo', exact=False, timeout=10)
    c.mark(6)
    c.confere('dlg', ['Você tentou abrir com R$ 500,00', 'o cofre está negativo em R$ 1.200,00', 'não há dinheiro disponível',
                      'R$ 18.500,00 já reservados em caixas abertos', 'Abrir zerado (R$ 0,00)'], 'aviso: cofre negativo em 1.200,00')
    c.hover(TXTX('o cofre está negativo', ALERTA_COFRE), at=c.A(6, 'negativo', 0.5), label='ZOOM o cofre está negativo em R$ 1.200,00 (L6)')
    c.hover(BTNX('Abrir zerado', ALERTA_COFRE), at=c.A(6, 'Abrir', 0.5), label='Abrir zerado (R$ 0,00)')
    c.mark(7)
    c.hover(TXTX('ajuste o saldo do dinheiro abaixo', ALERTA_COFRE), at=c.A(7, 'texto', 0.5), label='texto de quem pode ajustar contas')
    c.hover(BTN('Ajustar saldo do dinheiro', ALERTA_COFRE), at=c.A(7, 'botão', 0.5), label='Ajustar saldo do dinheiro (só quem pode ajustar)')
    c.mark(8)
    c.click(BTNX('Abrir zerado', ALERTA_COFRE), at=c.A(8, 'Abrir', 0.6, nth=0), label='Abrir zerado')
    c.confere_campo('#openingBalance', '0,00', 'campo com 0,00')
    c.click(ABRIR_DLG, at=c.A(8, 'Abrir', 0.6, nth=1), label='Abrir Caixa (janela)')
    c.waitfor(text='Caixa aberto com sucesso!', timeout=10)
    c.confere('main', ['#87 | Caixa - Juliana Prado', 'Dinheiro em Caixa', 'R$ 0,00'], 'caixa #87 da Juliana aberto zerado')
    c.mark(9)
    c.hover(TAB87, at=c.A(9, 'zerado', 0.5), label='aba #87 da Juliana')
    c.hover(TXT('Dinheiro em Caixa'), at=c.A(9, 'dinheiro', 0.5), label='Dinheiro em Caixa R$ 0,00 (#87)')
    c.fim()
    return c


@cap
def cap07():
    """Os dois cartões: Dinheiro em Caixa (#85), Aberto em e Dinheiro total da empresa > o cofre e a barra; Saldo Bancário; o olho."""
    c = Cap(7, setup_caixa([{'do': 'waitFor', 'text': '#86 | Caixa - Marcos Antunes', 'timeout': 15}, {'do': 'click', 'target': TAB85},
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
def cap08():
    """Multi-caixa: as abas, o "?" (Como funcionam os Multi-Caixas?), a aba Início com o Painel Gerencial."""
    c = Cap(8, setup_caixa([{'do': 'waitFor', 'text': '#86 | Caixa - Marcos Antunes', 'timeout': 15}, {'do': 'click', 'target': TAB85},
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
    # cobertura P7: o painel de outro dia, as transações e os gráficos, o resumo do caixa atual e o atalho de saldo
    c.mark(7)
    c.click(SEL(DATA_PAINEL), at=c.A(7, 'calendário', 0.6), label='seletor de data do painel (Hoje)')
    c.waitfor(selector='[role=grid]', timeout=8)
    c.click(SEL(DIA_9), at=c.A(7, 'ontem', 0.6), label='dia 9 de novembro')
    c.confere('main', ['2 caixas encontrados', 'Resumo do Dia'], 'painel de 09/11: 2 caixas e o resumo do dia')
    c.hover(TXTX('Resumo do Dia'), at=c.A(7, 'resumo', 0.5), label='Resumo do Dia de ontem (09/11)')
    c.mark(8)
    c.ev(js_rola_ate('Transações do Dia', y=140, dur_ms=1100, prefixo=True), at=c.A(8, 'embaixo', 0.8), label='rola até Transações do Dia')
    c.hover(TXTX('Transações do Dia'), at=c.A(8, 'transações', 0.5), label='Transações do Dia (selo e operador em cada linha)')
    c.ev(js_rola_ate('Visão Geral', y=140, dur_ms=1000), at=c.A(8, 'gráficos', 0.8), label='rola até os gráficos')
    c.hover(TXT('Visão Geral'), at=c.A(8, 'dinheiro', 0.5, nth=0), label='gráfico Visão Geral')
    c.hover(TXT('Compras por Forma'), at=c.A(8, 'Pix', 0.5), label='gráficos Compras e Vendas por Forma')
    c.hover(TXT('Distribuição entre Caixas'), at=c.A(8, 'movimentou', 0.9), label='gráfico Distribuição entre Caixas')
    c.ev(js_rola_topo(700), at=c.A(8, 'Hoje', 1.4), label='sobe ao seletor de data')
    c.click(SEL(HOJE_PAINEL), at=c.A(8, 'Hoje', 0.6), label='volta para Hoje')
    c.mark(9)
    c.ev(js_rola_topo(700), at=c.L(9) - 0.9, label='volta ao topo')
    c.click(TAB85, at=c.A(9, 'Dentro', 0.6), label='aba #85')
    c.ev(js_rola_ate('Resumo do Caixa Atual', y=170, dur_ms=1100, prefixo=True), at=c.A(9, 'Resumo', 0.8), label='rola até o Resumo do Caixa Atual')
    c.hover(TXTX('Resumo do Caixa Atual'), at=c.A(9, 'Resumo', 0.5), label='ZOOM Resumo do Caixa Atual (L9)')
    c.hover(TXT('Total Comprado'), at=c.A(9, 'comprou', 0.5), label='Total Comprado')
    c.hover(TXT('Projeção de Lucro'), at=c.A(9, 'projeção', 0.5), label='Projeção de Lucro')
    c.click(SEL(OLHO_RESUMO), at=c.A(9, 'olhinho', 0.6), label='olho Ocultar valores')
    c.click(SEL(OLHO_RESUMO2), at=c.A(9, 'perto', 0.0), label='olho Mostrar valores')
    c.mark(10)
    c.ev(js_rola_topo(700), at=c.L(10) - 0.9, label='volta ao topo')
    c.hover(BTNX('Saldo de Cliente/Fornecedor', MAIN), at=c.A(10, 'botão', 0.5), label='botão Saldo de Cliente/Fornecedor')
    c.fim()
    return c


@cap
def cap09():
    """O caixa dos outros (Rafael, L1 a L3): a aba do Marcos e quem pode operá-la. O cap08b (Marcos) cobre L4 e L5."""
    c = Cap(9, setup_caixa([{'do': 'waitFor', 'text': '#86 | Caixa - Marcos Antunes', 'timeout': 15}, {'do': 'click', 'target': TAB85},
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
    c.mark(4)
    c.hover(TAB86, at=c.A(4, 'cadeado', 0.5), label='abas: abrir e fechar caixa também são permissões')
    c.dur = c.L(5)        # o trecho acaba no início da linha 5: a edição junta o cap09b (Marcos) daí em diante
    c.fim()
    return c


@cap
def cap09b():
    """Corte do cap08, linhas 4 e 5: o Marcos logado no computador da balança vê só o caixa dele (#86), sem as abas."""
    setup = login(EMAIL_MARCOS, None) + IR_CAIXA + [{'do': 'waitFor', 'text': 'Aberto em: 10/11/2026 08:42', 'timeout': 10}]
    c = Cap(9, setup, sub='b', voz_de=(5, 6), user='marcos')
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
def cap10():
    """Saque e sangria: (ilustração L1 a L4); saque de 3.000,00 + tarifa 6,50 para o #86; a opção Sangria; a tarifa mensal de 39,90."""
    c = Cap(10, setup_caixa([{'do': 'waitFor', 'text': '#86 | Caixa - Marcos Antunes', 'timeout': 15}, {'do': 'click', 'target': TAB85},
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
    c.click(OPT('Sim', exact=True), at=c.A(8, 'sim', 0.7), label='Sim')
    # ensaio completo de 11/11: com o clique no campo a tarifa saía 1,1 s atrasada; o foco vai por eval (sem cursor) e a digitação cai em "seis"
    c.waitfor(selector=f'{DLG} #fee', timeout=6)
    c.ev(f"(()=>{{const e=document.querySelector('{DLG} #fee');if(!e)return 'SEM ALVO';e.focus();return 'foco ok'}})()", label='foco no Valor da Tarifa')
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
    t = c.L(12) - 1.4
    c.marca_em(12, t)
    c.click(SAQUE_SANGRIA, at=t, label='Saque / Sangria (de novo)')
    c.waitfor(text='Transferir dinheiro do banco para o cofre ou para um caixa aberto', timeout=10)
    # cobertura P4a: o destino "Cofre (Conta DINHEIRO)" (só olha, sem escolher) e a data retroativa do lançamento
    c.click(COMBO(1), at=c.A(12, 'destino', 0.6), label='Destino do saque')
    c.hover(OPT('Cofre (Conta DINHEIRO)', exact=False), at=c.A(12, 'cofre', 0.5), label='Cofre (Conta DINHEIRO) (sem escolher)')
    c.mark(13)
    c.press('Escape', at=c.L(13) - 0.9, label='fecha a lista sem escolher')
    c.hover(SEL(f'{DLG} label[for=transactionDate], {DLG} :text("Data/hora do lançamento")'), at=c.A(13, 'dia', 0.5), label='ZOOM Data/hora do lançamento (L13)')
    c.click(BTN('Cancelar', DLG), at=c.A(13, 'faz', 0.5), label='Cancelar')
    c.waitfor(gone={'role': 'dialog'}, timeout=6)
    c.mark(14)
    c.click(NOVA_MOV, at=c.A(14, 'Nova', 0.6), label='Nova Movimentação Bancária')
    c.waitfor(text='Nova Movimentação Financeira', timeout=10)
    c.click(COMBO(0), at=c.A(14, 'Por', 0.6), label='Conta bancária')
    c.click(OPT('Conta Secundária'), at=c.A(14, 'tarifa', 0.6), label='Conta Secundária')
    c.mark(15)
    c.click(BTN('Saída', DLG), at=c.A(15, 'Saída', 0.6), label='Tipo Saída')
    c.click(DESCRICAO, at=c.A(15, 'descrição', 0.6), label='Descrição')
    colar(c, f'{DLG} #description', 'Tarifa mensal do pacote de serviços', label='cola a descrição')
    c.click(VALOR, at=c.A(15, 'trinta', 0.6), label='Valor')
    c.type(VALOR, '39,90', at=c.A(15, 'nove', 0.05, nth=0), label='digita R$ 39,90', noClick=True)
    c.click(COMBO(1), at=c.A(15, 'categoria', 0.9), label='Categoria')
    c.click(OPT('Tarifas', exact=True), at=c.A(15, 'Tarifas', 0.6), label='categoria Tarifas')
    c.mark(16)
    c.flush(1e9)
    c.confere_js("(async()=>{for(let i=0;i<10;i++){const d=document.querySelector('[role=dialog]');const t=d?d.innerText:'';"
                 "const v=d?[...d.querySelectorAll('input')].map(e=>e.value).join(' | '):'';"
                 "if(t.includes('Conta Secundária')&&t.includes('Tarifas')&&v.includes('Tarifa mensal do pacote de serviços')&&v.includes('R$ 39,90'))"
                 "return 'OK: Conta Secundária | Tarifas | Tarifa mensal do pacote de serviços | R$ 39,90';await new Promise(r=>setTimeout(r,150))}"
                 "return 'DIFERENTE: '+(document.querySelector('[role=dialog]')||{innerText:''}).innerText.slice(0,200)})()",
                 'conta, categoria, descrição e valor da saída')
    c.click(BTN('Salvar', DLG), at=c.A(16, 'Salvar', 0.6), label='Salvar')
    c.waitfor(text='Movimentação registrada com sucesso!', timeout=10)
    c.fim()
    return c


NOVA_DESPESA = BTNX('Nova Despesa', MAIN)
NOVA_RECEITA = BTNX('Nova Receita', MAIN)
COMBO_TXT = lambda t: {'role': 'combobox', 'hasText': t, 'within': DLG}
SUGESTAO = lambda t: SEL(f'{DLG} :text("{t}")')


def setup_aba(aba=TAB85, ate='Aberto em: 10/11/2026 08:31'):
    return setup_caixa([{'do': 'waitFor', 'text': '#86 | Caixa - Marcos Antunes', 'timeout': 15}, {'do': 'click', 'target': aba},
                        {'do': 'waitFor', 'text': ate, 'timeout': 10}])


@cap
def cap11():
    """Despesa e receita do dia (cobertura P1): "Nova Despesa" com o preenchimento inteligente (Gás da empilhadeira, R$ 50,00, dinheiro) e
    "Nova Receita" (Aluguel de caçamba, R$ 120,00 por Pix na Conta Principal). 08:55, #85 com R$ 1.500,00."""
    c = Cap(11, setup_aba())
    c.mark(1)
    c.hover(NOVA_DESPESA, at=c.A(1, 'botão', 0.5), label='NOVA DESPESA e NOVA RECEITA (ZOOM L1)')
    c.hover(NOVA_RECEITA, 0.3, at=c.A(1, 'próprio', 0.5), label='Nova Receita')
    c.mark(2)
    c.click(NOVA_DESPESA, at=c.A(2, 'Nova', 0.6), label='Nova Despesa')
    c.waitfor(text='Informe o valor e motivo da despesa', exact=False, timeout=10)
    c.mark(3)
    c.click(DESCRICAO, at=c.A(3, 'descrição', 0.6), label='Descrição')
    c.type(DESCRICAO, 'Gás da', at=c.A(3, 'sistema', 0.1), label='digita Gás da (o padrão abre na 3a letra)', noClick=True)
    c.waitfor(text='Padrão encontrado: Gás da empilhadeira', exact=False, timeout=10)
    c.confere('dlg', ['Padrão encontrado: Gás da empilhadeira', 'Usado 4 vezes', 'setembro de 2026', 'Preencher'], 'padrão do gás (4 usos, setembro)')
    c.hover(SUGESTAO('Padrão encontrado: Gás da empilhadeira'), at=c.A(3, 'padrão', 0.5), label='ZOOM lista Padrão encontrado e Preencher (L3)')
    c.mark(4)
    c.click(BTN('Preencher', DLG), at=c.A(4, 'Preencher', 0.6), label='Preencher')
    c.confere('dlg', ['Combustível', 'Pátio', 'Dinheiro (Caixa)', 'Campos preenchidos'], 'campos preenchidos (gás)')
    c.hover(SUGESTAO('Desfazer preenchimento'), at=c.A(4, 'Desfazer', 0.5), label='Desfazer preenchimento')
    c.click(VALOR, at=c.A(4, 'valor', 0.6, nth=0), label='Valor')
    c.type(VALOR, '50,00', at=c.A(4, 'cinquenta', 0.05), label='ZOOM digita R$ 50,00 (L4)', noClick=True)
    c.mark(5)
    c.click(COMBO_TXT('Dinheiro (Caixa)'), at=c.A(5, 'Pagou', 0.6), label='Pagou com')
    c.hover(OPT('Conta Principal'), 0.4, at=c.A(5, 'caixa', 0.5, nth=0), label='grupos Dinheiro e Contas')
    c.press('Escape', at=c.A(5, 'escolher', 0.1), label='fecha a lista sem trocar')
    c.mark(6)
    c.click(BTNX('Mais detalhes', DLG), at=c.A(6, 'Mais', 0.6), label='Mais detalhes')
    c.hover(SUGESTAO('Observação (opcional)'), at=c.A(6, 'observação', 0.5), label='Observação (opcional)')
    c.hover(SUGESTAO('Parcelar ou repetir'), at=c.A(6, 'Parcelar', 0.5), label='Parcelar ou repetir (sem abrir)')
    c.mark(7)
    c.click(BTN('Confirmar Despesa', DLG), at=c.A(7, 'Confirmar', 0.6), label='Confirmar Despesa')
    c.waitfor(text='Retirada realizada com sucesso!', timeout=10)
    c.confere('main', ['R$ 1.450,00', 'Gás da empilhadeira'], 'Dinheiro em Caixa R$ 1.450,00 e a despesa no histórico')
    c.hover(TXT('R$ 1.450,00'), at=c.A(7, 'caiu', 0.5), label='ZOOM Dinheiro em Caixa R$ 1.450,00 (L7)')
    c.mark(8)
    c.click(NOVA_RECEITA, at=c.A(8, 'Nova', 0.6), label='Nova Receita')
    c.waitfor(text='Informe o valor e motivo da receita', exact=False, timeout=10)
    c.click(DESCRICAO, at=c.A(8, 'sucata', 0.6), label='Descrição')
    c.type(DESCRICAO, 'Aluguel de', at=c.A(8, 'aluguel', 0.05), label='digita Aluguel de', noClick=True)
    c.waitfor(text='Padrão encontrado: Aluguel de caçamba', exact=False, timeout=10)
    c.click(BTN('Preencher', DLG), at=c.A(8, 'caçamba', 0.2), label='Preencher')
    c.confere('dlg', ['Aluguel de caçamba', 'Conta Principal', 'Campos preenchidos'], 'campos preenchidos (aluguel de caçamba)')
    c.click(VALOR, at=c.A(8, 'cento', 0.6), label='Valor')
    c.type(VALOR, '120,00', at=c.A(8, 'cento', 0.05), label='ZOOM digita R$ 120,00 (L8)', noClick=True)
    c.mark(9)
    c.click(BTN('Confirmar Receita', DLG), at=c.A(9, 'Confirmar', 0.6), label='Confirmar Receita')
    c.waitfor(text='Depósito realizado com sucesso!', timeout=10)
    c.mark(10)
    c.hover(TXT('Dinheiro em Caixa'), at=c.A(10, 'receita', 0.5), label='Dinheiro em Caixa R$ 1.450,00 (segue)')
    c.hover(TXT('Saldo Bancário'), at=c.A(10, 'saque', 0.5), label='Saldo Bancário (subiu R$ 120,00)')
    c.fim()
    return c


@cap
def cap12():
    """Sangria no fim do dia (cobertura P4b), 17:30: do caixa do Marcos (#86) R$ 5.000,00 para a Conta Principal."""
    c = Cap(12, setup_aba(TAB86, 'Aberto em: 10/11/2026 08:42'))
    c.mark(1)
    c.hover(TXT('Dinheiro em Caixa'), at=c.A(1, 'caixa', 0.5, nth=0), label='Dinheiro em Caixa do Marcos')
    c.mark(2)
    c.click(SAQUE_SANGRIA, at=c.A(2, 'Saque', 0.6), label='Saque / Sangria')
    c.waitfor(text='Transferir dinheiro do banco para o cofre ou para um caixa aberto', timeout=10)
    c.click(BTN('Sangria', DLG), at=c.A(2, 'opção', 0.6), label='opção Sangria')
    c.waitfor(text='Transferir dinheiro do cofre ou de um caixa aberto para uma conta bancária', timeout=8)
    c.click(COMBO(0), at=c.A(2, 'origem', 0.6), label='Origem da sangria')
    c.hover(OPT('Cofre (Conta DINHEIRO)', exact=False), 0.3, at=c.A(2, 'cofre', 0.5), label='Cofre (Conta DINHEIRO) com o saldo')
    c.click(OPT('Caixa de Marcos Antunes', exact=False), at=c.A(2, 'Marcos', 0.5), label='Caixa de Marcos Antunes')
    c.mark(3)
    c.click(COMBO(1), at=c.A(3, 'destino', 0.6), label='Conta de destino')
    c.click(OPT('Conta Principal', exact=False), at=c.A(3, 'principal', 0.6), label='Conta Principal')
    c.click(SEL(f'{DLG} #sangria-amount'), at=c.A(3, 'valor', 0.6, nth=0), label='Valor da Sangria')
    c.type(SEL(f'{DLG} #sangria-amount'), '5.000,00', at=c.A(3, 'cinco', 0.05), label='ZOOM digita R$ 5.000,00 (L3)', noClick=True)
    c.click(SEL(f'{DLG} #sangria-description'), at=c.A(3, 'depositar', 0.9), label='Descrição (Opcional)')
    colar(c, f'{DLG} #sangria-description', 'Depósito do fim do dia', label='cola a descrição')
    c.mark(4)
    c.ev(js_rola_ate('Efeitos desta transação:', y=300, dur_ms=700, esc=DLG), at=c.L(4) - 0.9, label='desce a janela até os efeitos')
    c.confere('dlg', ['Diminuirá em R$ 5.000,00', 'Aumentará em R$ 5.000,00'], 'efeitos da sangria')
    c.hover(TXT('Efeitos desta transação:', DLG), at=c.A(4, 'efeitos', 0.5), label='ZOOM Efeitos desta transação (L4)')
    c.hover(TXTX('Diminuirá em', DLG), at=c.A(4, 'diminui', 0.5), label='Diminuirá em R$ 5.000,00')
    c.hover(TXTX('Aumentará em', DLG), at=c.A(4, 'aumenta', 0.5), label='Aumentará em R$ 5.000,00')
    c.mark(5)
    c.click(BTN('Confirmar Sangria', DLG), at=c.A(5, 'Confirmar', 0.6), label='Confirmar Sangria')
    c.waitfor(text='Sangria realizada com sucesso!', timeout=10)
    c.hover(TXT('Dinheiro em Caixa'), at=c.A(5, 'gaveta', 0.5), label='Dinheiro em Caixa do #86 (menos R$ 5.000,00)')
    c.fim()
    return c


FECHAMENTO = SEL(f'{DLG} #closingBalance')                            # "Valor de Fechamento" (vem com o esperado; Caixa.tsx:3503)
LINHA_CX = lambda n: SEL(f"{DLG} button:has-text('#{n}')")             # linha da lista "Reabrir outro caixa" (a 1a; o rodapé tem "Reabrir #N")
LINHA = lambda txt: SEL(f"main tbody tr:has-text('{txt}')")


def _cap13(sub=''):
    """Fechar o caixa às 17:40 (semente apos-cap12): o movimento do dia (R$ 957,10), a trava na tela (L3 a L5, só no cap13a), a conta do dia,
    os cartões, a diferença de exemplo (950,00), a contagem certa (957,10) e o fechamento.
    cap13a = corte das linhas 3 a 5 da voz com o rascunho de compra do Valdir Pereira (a trava do Fechar Caixa)."""
    pre = [{'do': 'waitFor', 'text': '#86 | Caixa - Marcos Antunes', 'timeout': 15}, {'do': 'click', 'target': TAB85},
           {'do': 'waitFor', 'text': 'Aberto em: 10/11/2026 08:31', 'timeout': 10}, {'do': 'waitFor', 'text': 'Aços Quiririm Ltda', 'timeout': 10}]
    if sub == 'a':
        c = Cap(13, setup_caixa(pre), sub='a', voz_de=(3, 5), sementes=[f'{AULA}/dia-10-rascunho'])
        c.mark(1)
        c.ev(js_rola_ate('Pedidos Não Finalizados', y=200, dur_ms=1000, prefixo=True), at=0.3, label='desce até Pedidos Não Finalizados')
        c.hover(TXTX('Pedidos Não Finalizados'), at=c.A(1, 'painel', 0.5), label='ZOOM painel Pedidos Não Finalizados (L3)')
        c.hover(TXTX('Valdir Pereira'), at=c.A(1, 'Valdir', 0.5), label='compra do Valdir Pereira (rascunho)')
        c.mark(2)
        c.ev(js_rola_topo(900), at=c.L(2) - 0.9, label='volta ao topo')
        c.hover(BTNX('Fechar Caixa', MAIN), at=c.A(2, 'cadeado', 0.5), label='ZOOM Fechar Caixa com cadeado e a dica (L4)')
        c.hover(BTNX('Fechar Caixa', MAIN), 1.2, at=c.A(2, 'travando', 0.8), label='dica Finalize ou cancele antes de fechar o caixa')
        c.mark(3)
        c.fim()
        return c
    c = Cap(13, setup_caixa(pre))
    c.mark(1)
    c.confere('main', ['R$ 957,10', 'Aços Quiririm Ltda', 'Aparecida Ramos', 'Valdir Pereira', 'Gás da empilhadeira'], 'movimento do dia no #85 (957,10)')
    c.hover(TXT('R$ 957,10'), 0.3, at=0.4, label='Dinheiro em Caixa R$ 957,10')
    c.ev(js_rola_ate('Histórico de Transações', y=120, dur_ms=1000, prefixo=False), at=c.A(1, 'venda', 1.2), label='desce ao Histórico de Transações')
    c.hover(LINHA('Aços Quiririm Ltda'), at=c.A(1, 'Aços', 0.5), label='venda Aços Quiririm (Pix/Transferência)')
    c.hover(LINHA('Aparecida Ramos'), at=c.A(1, 'Aparecida', 0.5), label='compra da Aparecida (Dinheiro)')
    c.hover(LINHA('Valdir Pereira'), 0.3, at=c.A(1, 'Valdir', 0.5), label='compra do Valdir (Dinheiro)')
    c.hover(LINHA('Gás da empilhadeira'), 0.3, at=c.A(1, 'gás', 0.5), label='despesa gás da empilhadeira (Dinheiro)')
    c.mark(2)
    c.ev(js_rola_topo(900), at=c.L(2) - 0.9, label='volta ao topo')
    c.hover(BTN('Fechar Caixa', MAIN), at=c.A(2, 'Fechar', 0.5), label='Fechar Caixa (sem cadeado)')
    # L3 a L5: o trecho cap13a (rascunho do Valdir) entra no lugar; aqui o botão fica livre
    c.mark(3)
    c.mark(4)
    c.mark(5)
    c.mark(6)
    c.click(BTN('Fechar Caixa', MAIN), at=c.A(6, 'Fechar', 0.6), label='Fechar Caixa')
    c.waitfor(text='Fechar Caixa #85', timeout=10)
    c.waitfor(text='Valor esperado pelo sistema', timeout=15)
    c.mark(7)
    c.confere('dlg', ['Saldo de Abertura', 'R$ 1.500,00', 'Restante em Caixa', 'R$ 957,10', 'Compras', 'R$ 492,90', 'Despesas', 'R$ 50,00'],
              'conta do dia: 1.500,00 - 492,90 - 50,00 = 957,10')
    c.hover(TXT('Saldo de Abertura', DLG), at=c.A(7, 'Abriu', 0.5), label='ZOOM cartões do fechamento (L7 e L8)')
    c.hover(TXT('Compras', DLG), at=c.A(7, 'compras', 0.5), label='Compras R$ 492,90 (Dinheiro)')
    c.hover(TXT('Despesas', DLG), at=c.A(7, 'despesa', 0.5), label='Despesas R$ 50,00 (Dinheiro)')
    c.mark(8)
    c.hover(TXT('Restante em Caixa', DLG), at=c.A(8, 'Restante', 0.5), label='Restante em Caixa R$ 957,10')
    c.mark(9)
    c.hover(TXT('Entradas', DLG), at=c.A(9, 'cartão', 0.5), label='cartões Saídas e Entradas: Dinheiro e PIX/Transf. (L9)')
    c.hover(TXT('Receitas', DLG), at=c.A(9, 'Pix', 0.5), label='Receitas: PIX/Transf. R$ 120,00')
    c.mark(10)
    c.click(TXTX('Projeção de Lucro', DLG), at=c.A(10, 'Projeção', 0.6), label='Projeção de Lucro (abre a tabela por material)')
    c.confere('dlg', ['Comprado (kg)', 'Valor Compra', 'Vendido (kg)', 'Valor Venda'], 'tabela da Projeção de Lucro por material')
    c.mark(11)
    c.mark(12)
    # o corpo da janela (ResponsiveDialog max-w-4xl) rola: o campo desce até a vista ainda sob a ilustração (L11 e L12)
    c.ev(js_rola_ate('Valor de Fechamento', y=380, dur_ms=800, esc=DLG), at=c.L(13) - 2.2, label='desce a janela até o Valor de Fechamento')
    c.mark(13)
    c.confere_campo(f'{DLG} #closingBalance', '957,10', 'Valor de Fechamento já com o esperado')
    c.hover(FECHAMENTO, at=c.A(13, 'Valor', 0.5), label='Valor de Fechamento (já com o esperado)')
    c.mark(14)
    c.click(FECHAMENTO, at=c.A(14, 'olha', 0.6), label='campo Valor de Fechamento')
    c.type(FECHAMENTO, '950,00', at=c.A(14, 'novecentos', 0.05), label='digita 950,00', noClick=True, clear=True)
    c.confere('dlg', ['Diferença detectada', 'R$ 7,10', 'Registrar diferença no DRE'], 'diferença de 7,10 a menos (950,00 contra 957,10)')
    c.hover(TXTX('Diferença detectada', DLG), at=c.A(14, 'diferença', 0.5), label='ZOOM Diferença detectada -R$ 7,10 e a chave (L14 e L15)')
    c.mark(15)
    c.hover(TXTX('Registrar diferença no DRE', DLG), at=c.A(15, 'chave', 0.5), label='chave Registrar diferença no DRE')
    c.mark(16)
    c.click(FECHAMENTO, at=c.A(16, 'Contei', 0.6), label='campo Valor de Fechamento')
    c.type(FECHAMENTO, '957,10', at=c.A(16, 'novecentos', 0.05), label='ZOOM digita 957,10 e o valor esperado (L16)', noClick=True, clear=True)
    c.hover(TXTX('Valor esperado pelo sistema', DLG), at=c.A(16, 'Bateu', 0.5), label='Valor esperado pelo sistema: R$ 957,10')
    c.mark(17)
    c.mark(18)
    c.hover(TXTX('Altere para fechar o caixa com data/hora retroativa', DLG), at=c.A(18, 'retroativa', 0.5), label='ZOOM Data/hora do fechamento (L18)')
    c.mark(19)
    # rodapé fixo da janela (pode ficar abaixo de y 730): sem rolar à toa
    c.click(BTN('Confirmar Fechamento', DLG), at=c.A(19, 'Confirmar', 0.6), label='Confirmar Fechamento', noScroll=True)
    c.waitfor(text='Deseja imprimir o relatório de fechamento de caixa?', timeout=12)
    c.mark(20)
    c.click(BTN('Não, obrigado'), at=c.A(20, 'não', 0.6), label='Não, obrigado')
    c.waitfor(text='Meu Caixa', timeout=10)
    c.fim()
    return c


@cap
def cap13():
    return _cap13()


def cap13a():
    return _cap13('a')


@cap
def cap14():
    """Reabrir: o cartão amarelo do #85, "reabrir outro caixa" (todos os operadores), "Reabrir #85" e a confirmação."""
    c = Cap(14, setup_caixa([{'do': 'waitFor', 'text': 'Reabrir #85', 'timeout': 15}]))
    c.mark(1)
    c.hover(BTN('Reabrir #85', MAIN), at=c.A(1, 'reabrir', 0.5), label='Reabrir #85')
    c.mark(2)
    c.mark(3)
    c.confere('main', ['#85', 'R$ 957,10', 'reabrir outro caixa'], 'cartão amarelo do #85 com R$ 957,10')
    c.hover(CARD_AMARELO, at=c.A(3, 'cartão', 0.5), label='ZOOM cartão amarelo #85 (L2)')
    c.mark(4)
    c.click(BTN('reabrir outro caixa', MAIN), at=c.A(4, 'reabrir', 0.6), label='reabrir outro caixa')
    c.waitfor(text='Escolha qual caixa fechado deseja reabrir', timeout=10)
    c.confere('dlg', ['#85', 'R$ 957,10', '#84', 'R$ 1.250,00', '#83', 'Marcos Antunes', 'R$ 640,00'], 'lista: #85, #84 e #83 do Marcos')
    c.hover(LINHA_CX(84), at=c.A(4, 'operadores', 0.5), label='lista dos últimos caixas fechados (#84)')
    c.mark(5)
    c.hover(LINHA_CX(83), at=c.A(5, 'outra', 0.5), label='o #83 do Marcos (R$ 640,00)')
    c.mark(6)
    c.hover(LINHA_CX(85), at=c.A(6, 'meu', 0.5), label='o #85 já marcado')
    c.click(BTN('Reabrir #85', DLG), at=c.A(6, 'reabrir', 0.6), label='Reabrir #85 (lista)')
    c.waitfor(text='Reabrir caixa #85?', timeout=10)
    c.hover(TXTX('O caixa será reaberto exatamente como estava', ALERTA), at=c.A(6, 'confirma', 0.5), label='Reabrir caixa #85? (como estava)')
    c.mark(7)
    c.click(BTN('Reabrir Caixa'), at=c.A(7, 'Reabrir', 0.6), label='Reabrir Caixa')
    c.waitfor(text='Caixa reaberto com sucesso!', timeout=10)
    c.hover(TXT('R$ 957,10'), at=c.A(7, 'aberto', 0.5), label='Dinheiro em Caixa R$ 957,10 (#85 reaberto)')
    c.fim()
    return c


@cap
def cap15():
    """Recapitulando (a montagem da edição usa trechos dos capítulos): passeio de reserva pelo estado final (17:44, #85 reaberto)."""
    c = Cap(15, setup_aba())
    c.mark(1)
    c.hover(TAB85, at=c.A(1, 'caixa', 0.5, nth=0), label='aba #85')
    c.mark(2)
    c.hover(TXT('R$ 957,10'), at=c.A(2, 'dinheiro', 0.5), label='Dinheiro em Caixa')
    c.mark(3)
    c.hover(TOTAL, at=c.A(3, 'cofre', 0.5), label='Dinheiro total da empresa (o cofre)')
    c.mark(4)
    c.hover(TAB86, at=c.A(4, 'Marcos', 0.5), label='aba do Marcos')
    c.mark(5)
    c.hover(NOVA_DESPESA, at=c.A(5, 'despesa', 0.5), label='Nova Despesa')
    c.mark(6)
    c.hover(SAQUE_SANGRIA, at=c.A(6, 'saque', 0.5), label='Saque / Sangria')
    c.mark(7)
    c.mark(8)
    c.hover(BTN('Fechar Caixa', MAIN), at=c.A(8, 'fechou', 0.5), label='Fechar Caixa')
    c.mark(9)
    c.fim()
    return c


CAPS_FN['13a'] = cap13a


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
