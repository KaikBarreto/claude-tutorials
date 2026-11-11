#!/usr/bin/env python3
"""T21 · Cato, o assistente (EcoFlix, EcoSistema 1.59.154): gera rec/t21/cap00..cap08.json (+ cap02b, o corte do Marcos) a partir da
fala ($TUT_HOME/t21/narracao/capNN.json: o estimado até a voz chegar; com a voz, o da voz, sem mudar nada aqui). O cap09
(Recapitulando) é montagem das gravações dos outros capítulos: não tem robô.

Computador 1280x800, Rafael Nogueira (MASTER) na Recicla Vale Metais, tela "Estoque" (/materiais: ali as quatro perguntas prontas
saem sem sorteio); FAKE_NOW 2026-11-10T08:30:00-03:00 em todos os capítulos (o mesmo no Supabase falso e no robô).
Rodar de qualquer pasta: `python3 -I rec/t21/gerar.py [NN ...] [2b]` (ANCORAS=1 lista as âncoras). Depois:
`node rec/record.mjs rec/t21/capNN.json --check`; ensaio: `python3 -I rec/t21/ensaio.py NN` + `--rapido`; gravação: sem `--rapido`.

LOGIN: todo capítulo é "anonymous" e o setup entra pela tela de login com "$TUT_USER"/"$TUT_SENHA" do ambiente (o Supabase falso
aceita qualquer senha; o valor nunca vai para arquivo nem log). O corte do Marcos (cap02b) entra com o e-mail dele (dado do mundo
fictício) e a mesma "$TUT_SENHA".

Cada passo é preso a uma palavra da fala: A(linha, 'palavra', folga) = início da palavra − folga (o custo do gesto até o cursor
chegar: clique ~0,6 s, 1º clique numa janela recém-aberta ~1,2 s, hover ~0,5 s; digitação sem clique na palavra − 0,05 s). A palavra
casa INTEIRA (sem acento e pontuação); repetida na linha pede `nth`. Marca Ln 0,9 s antes da linha; um passo que começa até 0,25 s
antes da marca a puxa para o início dele.

ESTADO DE PARTIDA (rec/mundo/seeds-extra/): o fim da T15, de onde o T21 parte (cadeia T13 → T14 → T15 → T21 da junção: `t14/inicio`,
os `t14/apos-capNN` e os `t15/*`, a mesma lista do rec/t15/gerar.py) + `t21/inicio` (Cato ligado, sem a autorização de IA; o Marcos
com "Usar o Cato") nos caps. 0 a 2 e no 2b; + `t21/apos-cap02` (autorizado, versão 2.0) nos caps. 3 a 8.
RESPOSTAS DO CATO: simuladas no Supabase falso (rec/mundo/lib/cato.mjs, com as respostas R1 a R9 do plano.md copiadas por
rec/t21/t21_respostas.py): edge cato-background → jobId; cato_jobs de "processing" a "completed" (R1 em ~4 s, as outras em ~1 s);
edge cato-assist (mode "followups") → as 3 sugestões. Os caps. 3 a 8 são UMA conversa: cada capítulo da 4 em diante restaura, no
setup, as perguntas e respostas dos anteriores pelo sessionStorage (`cato-conversation-v3:<empresa>:<usuário>`, o formato do
hooks/useCato.tsx), recarrega a página e abre o painel; o "Atualizado às" de cada resposta é fixo (08:30 de R1 a R5, 08:31 de R6 a
R8), para a conversa sair igual em todos os capítulos.
NÃO CLICAR: "Falar no WhatsApp", "Ouvir resposta", o microfone, "Memória" e "Conversas".

PARTICULARIDADES DA 1.59.154 (explorações rec/t21/_ex/):
 - O painel do Cato é um `div[role=dialog][aria-label^="Cato.ai"]` fixo à direita (400 px, por cima do app abaixo de 1536 px): os
   alvos dentro dele usam o seletor PAINEL, nunca `[role=dialog]` sozinho (a janela de autorização e a do suporte também são).
 - O botão do Cato (fixo no canto, y ~748) e o rodapé do painel ficam fora da faixa de clique do robô (y 96 a 730): `noScroll`.
 - A última resposta "digita" de novo quando o painel remonta (reabrir, recarregar): o setup espera o fim do texto.
 - O convite "Essa resposta ajudou?" aparece uma vez por painel montado, na última resposta de dado (nunca na 1ª).
"""
import hashlib
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TUT = os.path.normpath(os.path.join(HERE, '..', '..'))
AULA = 't21'
NARR = os.path.join(TUT, AULA, 'narracao')
FAKE_NOW = '2026-11-10T08:30:00-03:00'
VERSAO = '1.59.154'
HOJE = FAKE_NOW[:10]
NOMES = ['Abertura', 'Onde o Cato fica', 'Autorizar o Cato', 'As perguntas prontas', 'O que ele responde bem', 'Gráfico ou tabela',
         'De onde vêm os números', 'Os limites do Cato', 'Avaliar e falar com o suporte', 'Recapitulando']
T14 = ['t14/inicio'] + [f't14/apos-cap{n:02d}' for n in (2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 14)]
T15 = ['t15/inicio', 't15/apos-cap01', 't15/apos-cap02', 't15/apos-cap10']
INICIO = T14 + T15 + [f'{AULA}/inicio']
AUTORIZADO = INICIO + [f'{AULA}/apos-cap02']
SEMENTE = {0: INICIO, 1: INICIO, 2: INICIO, **{n: AUTORIZADO for n in range(3, 9)}}
EMAIL_MARCOS = 'marcos.antunes@reciclavalemetais.example'
RESPOSTAS = json.load(open(os.path.normpath(os.path.join(HERE, '..', 'mundo', 'lib', 'cato_respostas.json')), encoding='utf8'))['respostas']

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
    h = bytearray(hashlib.sha1(('domiflix-fake:' + chave).encode()).digest())
    h[6] = (h[6] & 0x0F) | 0x50
    h[8] = (h[8] & 0x3F) | 0x80
    x = h[:16].hex()
    return f'{x[:8]}-{x[8:12]}-{x[12:16]}-{x[16:20]}-{x[20:32]}'


EMPRESA = stable_id('company.reciclavale')
RAFAEL = stable_id('user.rafael')
MARCOS = stable_id('user.marcos')


def storage(uid=RAFAEL):
    return {'app_version': VERSAO, 'notification_shown_version': VERSAO, 'pwa-install-dismissed': 'true', 'theme': 'light',
            f'daily-tasks-reminder-last-shown-{uid}': HOJE, 'initial-preferences-set': 'true'}


# ---------------------------------------------------------------- observador de avisos de erro (aceite: tem de sair vazio)
OBS = ("(()=>{window.__avisos=[];const re=/N[ãa]o foi poss[ií]vel|Erro ao|Tente novamente|Algo deu errado|Falha ao|Something went wrong|indispon[ií]vel|"
       "SEM RESPOSTA SIMULADA|Deu um problema|N[ãa]o consegui/i;"
       "const chk=(t)=>{t=(t||'').trim();const m=t&&t.match(new RegExp('[^]{0,40}('+re.source+')[^]{0,40}','i'));"
       "if(m&&window.__avisos.length<10)window.__avisos.push(m[0].replace(/[\\n\\r\\t ]+/g,' '))};new MutationObserver(ms=>{for(const m of ms){"
       "m.addedNodes.forEach(n=>chk(n.textContent));if(m.type==='characterData')chk(m.target.textContent)}}).observe(document.body,"
       "{childList:true,subtree:true,characterData:true});chk(document.body.innerText);"
       "setInterval(()=>{document.querySelectorAll('[data-sonner-toast][data-type=error]').forEach(t=>{const s='TOAST DE ERRO: '+t.textContent.trim().slice(0,90);"
       "if(!window.__avisos.includes(s)&&window.__avisos.length<10)window.__avisos.push(s)})},300);return 1})()")


class Cap:
    def __init__(s, n, setup, pace=0.5, cps=40, start=(640, 470), prewarm=('/login',), sub='', voz_de=None, user='rafael'):
        s.n, s.sub = n, sub
        s.nome = f'cap{n:02d}{sub}'
        s.words, s.linhas, s.dur, s.estimado = carregar_voz(n)
        s.voz_inicio = 0.0
        if voz_de:   # corte: só as linhas voz_de[0]..voz_de[1] da voz, com o tempo contado do início da primeira (T06 cap08b, T15 cap09b)
            a, b = voz_de
            off = s.linhas[a - 1]['s']
            s.voz_inicio = round(off, 2)
            s.words = [dict(w, s=round(w['s'] - off, 3), e=round(w['e'] - off, 3), linha=w['linha'] - (a - 1))
                       for w in s.words if a - 1 <= w['linha'] <= b - 1]
            fim = s.linhas[b - 1]['e'] + 0.4
            s.linhas = [dict(li, i=li['i'] - (a - 1), s=round(li['s'] - off, 3), e=round(li['e'] - off, 3)) for li in s.linhas[a - 1:b]]
            s.dur = round(fim - off, 2)
        s.steps, s.pending, s.anchors = [], [], []
        s.pace, s.cps, s.start = pace, cps, start
        s.prewarm = list(prewarm)
        s.user = user
        s.setup = list(setup) + [{'do': 'eval', 'js': OBS}]

    # ---- tempo
    def L(s, i):
        return round(s.linhas[i - 1]['s'], 2)

    def W(s, i, palavra, nth=0, fim=False):
        q = norm(palavra)
        hits = [w for w in s.words if w['linha'] == i - 1 and norm(w['w']) == q]
        if len(hits) <= nth:
            raise SystemExit(f'{s.nome}: palavra "{palavra}" (#{nth}) não achada na linha {i}: ' + ' '.join(w['w'] for w in s.words if w['linha'] == i - 1))
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

    def rolar(s, by, at=None, label=None, ponto=(640, 470), duration=0.5, after=100):
        return s._p({'do': 'scroll', 'point': {'x': ponto[0], 'y': ponto[1]}, 'by': by, 'duration': duration, 'after': after}, at, label, {})

    def confere(s, escopo, esperados, label, tentativas=20):
        """`eval` que LÊ a tela e compara com o que a fala diz ("OK: ..." ou "DIFERENTE: ..."); escopo 'painel', 'dlg', 'main', 'body' ou CSS"""
        sel = {'painel': PAINEL, 'dlg': DLG_AUT, 'main': 'main', 'body': 'body'}.get(escopo, escopo)
        esp = [esperados] if isinstance(esperados, str) else list(esperados)
        js = ("(async()=>{const norm=t=>t.replace(/[\\s\\u00a0]+/g,' ').toLowerCase();const esp=%s;let out='';"
              "for(let i=0;i<%d;i++){const els=[...document.querySelectorAll(%s)];const el=els[els.length-1];"
              "if(!el){out='DIFERENTE: sem elemento';}else{const t=norm(el.innerText);const falta=esp.filter(e=>!t.includes(norm(e)));"
              "if(!falta.length)return 'OK: '+esp.join(' | ');out='DIFERENTE: faltou '+JSON.stringify(falta)+' em: '+t.slice(0,260);}"
              "await new Promise(r=>setTimeout(r,250));}return out})()") % (json.dumps(esp, ensure_ascii=False), tentativas, json.dumps(sel))
        return s.add({'do': 'eval', 'js': js, 'label': 'confere ' + label})

    def pergunta(s, texto, at_campo, at_enviar=None, label='', cps=None):
        """clica no campo "Pergunte ao Cato…" (`at_campo`), digita a pergunta sem clicar de novo (~0,75 s depois: o custo do clique) e
        clica em "Enviar" em `at_enviar` (ou logo que a digitação acaba: ~0,066 s por letra a cps 40, 0,054 a cps 60)"""
        cps = cps or s.cps
        s.click(CAMPO, at=at_campo, label=f'campo Pergunte ao Cato ({label})', noScroll=True)
        t_txt = round(at_campo + 0.75, 2)
        s.type(CAMPO, texto, at=t_txt, label=f'digita: {texto}', noClick=True, cps=cps)
        fim_txt = t_txt + 0.3 + len(texto) * (1.45 / cps + 0.03)
        if at_enviar is None or at_enviar < fim_txt + 0.1:
            if at_enviar is not None:
                print(f'  AVISO {s.nome}: Enviar ({label}) pedido em {at_enviar} s, mas a digitação acaba ~{fim_txt:.2f} s')
            at_enviar = fim_txt + 0.15
        return s.click(ENVIAR, at=round(at_enviar, 2), label=f'Enviar ({label})', noScroll=True)

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
            'title': f'T21 · Cap. {s.n}{s.sub} · {NOMES[s.n]} (narração{est} {str(round(s.dur, 1)).replace(".", ",")} s{corte}; marcas '
                     f'L1..L{len(s.linhas)} = início de cada linha do roteiro; FAKE_NOW {FAKE_NOW}; logado como {quem})',
            'seed': f'{AULA}-{s.nome}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
            'start': {'x': s.start[0], 'y': s.start[1]},
            'anonymous': True, 'storage': storage(MARCOS if s.user == 'marcos' else RAFAEL),
            'seedExtra': list(SEMENTE[s.n]),
            'prewarm': s.prewarm, 'setup': s.setup, 'steps': s.steps,
        }
        if s.voz_inicio:
            d['voz_inicio'] = s.voz_inicio      # a edição e o resumo.py contam a voz a partir daqui
        return d


# ---------------------------------------------------------------- alvos
MAIN = 'main'
PAINEL = '[role=dialog][aria-label^="Cato.ai"]'
DLG_AUT = '[role=dialog]:has-text("Antes da primeira conversa com o Cato")'
DLG_SUP = '[role=dialog]:has-text("Falar com o suporte")'
MSGS = PAINEL + ' div.h-full.overflow-y-auto'
BTN = lambda n, within=None, **kw: {'role': 'button', 'name': n, 'exact': True, **({'within': within} if within else {}), **kw}
TXT = lambda t, within=None, **kw: {'text': t, 'exact': True, **({'within': within} if within else {}), **kw}
TXTP = lambda t, within=None, **kw: {'text': t, **({'within': within} if within else {}), **kw}
SEL = lambda s, **kw: {'selector': s, **kw}
FAB = SEL('button[aria-label="Abrir o Cato"]')
CAMPO = SEL('textarea[aria-label="Mensagem para o Cato"]')
ENVIAR = SEL('button[aria-label="Enviar"]')
NO_PAINEL = lambda css: SEL(f'{PAINEL} {css}')
LI = lambda trecho: NO_PAINEL(f'li:has-text("{trecho}")')
FORTE = lambda trecho: NO_PAINEL(f'strong:has-text("{trecho}")')
PONTO = lambda trecho: SEL(f'{DLG_AUT} li:has-text("{trecho}")')
AGUARDA = {'do': 'waitFor', 'idle': True}


def login(email='$TUT_USER'):
    return [{'do': 'waitFor', 'target': {'label': 'E-mail'}, 'timeout': 30},
            {'do': 'type', 'target': {'label': 'E-mail'}, 'text': email, 'cps': 40},
            {'do': 'type', 'target': {'label': 'Senha', 'exact': True}, 'text': '$TUT_SENHA', 'cps': 40},
            {'do': 'click', 'target': BTN('Entrar')},
            {'do': 'waitFor', 'selector': 'button[aria-label="Sair"]', 'timeout': 30}, AGUARDA]


IR_ESTOQUE = [{'do': 'goto', 'url': '/materiais'}, {'do': 'waitFor', 'selector': 'button[aria-label="Abrir o Cato"]', 'timeout': 30}, AGUARDA]


# ---------------------------------------------------------------- a conversa dos caps. 3 a 8 (sessionStorage do useCato)
def mensagens(ate, feedback=None):
    """as perguntas e respostas R1..R<ate> no formato CatoMessage (hooks/useCato.tsx), como a tela as guardou"""
    base = 1794310200000   # 10/11/2026 08:30:00 -03:00 em ms (só aparece no celular)
    out = []
    for k, r in enumerate(RESPOSTAS[:ate], start=1):
        p = json.loads(json.dumps(r['payload']))
        ctx = p.get('context')
        if ctx:
            ctx['updatedAt'] = f'{HOJE}T{int(r["hora"][:2]) + 3:02d}:{r["hora"][3:]}:00.000Z'
        t = base + k * 20000
        out.append({'role': 'user', 'content': r['pergunta'], 'createdAt': t})
        out.append({'role': 'assistant', 'content': p['answer'], 'toolsUsed': p.get('toolsUsed'), 'chart': p.get('chart'), 'table': p.get('table'),
                    'images': None, 'action': None, 'context': ctx, 'interactionId': stable_id(f't21.cato.r{k}'),
                    'feedback': (feedback or {}).get(k), 'budgetNotice': None, 'cacheHit': False, 'createdAt': t + 4000})
    return out


def fim_da_resposta(k):
    """o fim do texto da resposta k como a tela o mostra (sem markdown), para esperar a resposta terminar de 'digitar'"""
    t = re.sub(r'\*\*', '', RESPOSTAS[k - 1]['payload']['answer']).strip()
    return t.split('\n')[-1].strip()[-22:]


def js_espera_resposta(trecho, tentativas=80):
    """espera a última resposta do painel conter `trecho` (a resposta acabou de 'digitar'); 'SEM ALVO' se não chegar"""
    return ("(async()=>{for(let i=0;i<%d;i++){const b=[...document.querySelectorAll(%s)].pop();"
            "if(b&&b.innerText.replace(/\\s+/g,' ').includes(%s))return 'ok';await new Promise(r=>setTimeout(r,250));}"
            "return 'SEM ALVO: a resposta não terminou'})()") % (tentativas, json.dumps(MSGS + ' > div.items-start'), json.dumps(trecho, ensure_ascii=False))


def restaura(ate, aquecer=()):
    """setup dos caps. 4 a 8: login, conversa R1..R<ate> no sessionStorage, recarrega a /materiais (passando antes pelas rotas de
    `aquecer`, que o vídeo visita) e abre o painel no fim da conversa"""
    chave = f'cato-conversation-v3:{EMPRESA}:{RAFAEL}'
    js = ("(()=>{const v={savedAt:Date.now(),sessionId:%s,messages:%s,activeJobId:null,activeQuestion:null,activeJobStartedAt:null};"
          "sessionStorage.setItem(%s,JSON.stringify(v));return 'conversa '+v.messages.length})()") % (
        json.dumps(stable_id('t21.cato.sessao')), json.dumps(mensagens(ate), ensure_ascii=False), json.dumps(chave))
    passos = login() + IR_ESTOQUE + [{'do': 'eval', 'js': js},
                                      {'do': 'goto', 'url': '/materiais', 'reload': True},
                                      {'do': 'waitFor', 'selector': 'button[aria-label="Abrir o Cato"]', 'timeout': 30}, AGUARDA]
    for rota in aquecer:
        passos += [{'do': 'goto', 'url': rota}, AGUARDA, {'do': 'wait', 'seconds': 1.0}]
    if aquecer:
        passos += IR_ESTOQUE
    return passos + [
        {'do': 'click', 'target': FAB, 'noScroll': True},
        {'do': 'waitFor', 'selector': PAINEL, 'timeout': 10},
        {'do': 'eval', 'js': js_espera_resposta(fim_da_resposta(ate))},
        {'do': 'wait', 'seconds': 0.8},
        {'do': 'eval', 'js': js_fim_da_conversa()},
    ]


# ---------------------------------------------------------------- rolagem roteirizada dentro do painel (eval: o cursor não se mexe)
SUAVE = ("await new Promise(res=>{const t0=performance.now();const f=t=>{const p=Math.min(1,(t-t0)/DUR),e=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;"
         "c.scrollTop=DESTINO;p<1?requestAnimationFrame(f):res()};requestAnimationFrame(f)});")


def js_msgs_rola(achar_js, y=300, dur_ms=700):
    """rola a conversa do painel até o elemento `achar_js` (expressão JS) ficar com o topo em y px CSS; devolve o topo final"""
    return ("(async()=>{const c=document.querySelector(%s);if(!c)return 'SEM PAINEL';const el=%s;if(!el)return 'SEM ALVO';"
            "const dy=Math.round(el.getBoundingClientRect().top-%d);if(Math.abs(dy)<3)return 'ok';const y0=c.scrollTop;"
            % (json.dumps(MSGS), achar_js, int(y))
            + (SUAVE.replace('DUR', str(int(dur_ms))).replace('DESTINO', 'y0+dy*e') if dur_ms else "c.scrollTop=y0+dy;")
            + "await new Promise(r=>setTimeout(r,60));return Math.round(el.getBoundingClientRect().top)})()")


def js_fim_da_conversa(dur_ms=0):
    return ("(async()=>{const c=document.querySelector(%s);if(!c)return 'SEM PAINEL';const y0=c.scrollTop,dy=c.scrollHeight-c.clientHeight-y0;"
            % json.dumps(MSGS) + (SUAVE.replace('DUR', str(int(dur_ms))).replace('DESTINO', 'y0+dy*e') if dur_ms else "c.scrollTop=y0+dy;")
            + "return 'fim '+Math.round(c.scrollTop)})()")


def js_rola_el(achar_js, y=300, dur_ms=700):
    """rola o ancestral que rola de verdade (a página, a janela) até o elemento `achar_js` ficar com o topo em y px CSS"""
    return ("(async()=>{const el=%s;if(!el)return 'SEM ALVO';let c=el.parentElement;while(c&&c!==document.body){const s=getComputedStyle(c);"
            "if(/(auto|scroll)/.test(s.overflowY)&&c.scrollHeight>c.clientHeight+4)break;c=c.parentElement;}if(!c||c===document.body)c=document.scrollingElement;"
            "const dy=Math.round(el.getBoundingClientRect().top-%d);if(Math.abs(dy)<3)return 'ok';const y0=c.scrollTop;" % (achar_js, int(y))
            + (SUAVE.replace('DUR', str(int(dur_ms))).replace('DESTINO', 'y0+dy*e') if dur_ms else "c.scrollTop=y0+dy;")
            + "await new Promise(r=>setTimeout(r,60));return Math.round(el.getBoundingClientRect().top)})()")


def js_dlg_fundo(dur_ms=0, quem='Antes da primeira conversa com o Cato'):
    """rola o miolo da janela de autorização (max-h 80dvh, rolagem própria) até o fim: os últimos pontos e os botões à vista"""
    return ("(async()=>{const d=[...document.querySelectorAll('[role=dialog]')].find(x=>x.innerText.includes(%s));if(!d)return 'SEM ALVO';"
            "const c=[...d.querySelectorAll('*')].find(e=>/(auto|scroll)/.test(getComputedStyle(e).overflowY)&&e.scrollHeight>e.clientHeight+4);"
            "if(!c)return 'sem rolagem (cabe)';const y0=c.scrollTop,dy=c.scrollHeight-c.clientHeight-y0;" % json.dumps(quem)
            + (SUAVE.replace('DUR', str(int(dur_ms))).replace('DESTINO', 'y0+dy*e') if dur_ms else "c.scrollTop=y0+dy;")
            + "return 'fundo '+Math.round(c.scrollTop)})()")


def achar_folha(escopo, texto, contem=False):
    """expressão JS: a folha visível (sem filhos) dentro de `escopo` cujo texto é (ou contém) `texto`"""
    cond = "e.textContent.includes(%s)" if contem else "e.textContent.trim()===%s"
    return ("[...document.querySelectorAll(%s)].find(e=>e.children.length===0&&e.getClientRects().length&&" + cond + ")") % (
        json.dumps(escopo + ' *'), json.dumps(texto, ensure_ascii=False))


def achar_ultimo(css):
    """expressão JS: o último elemento visível da conversa que casa com `css` (ex.: a linha do período da última resposta)"""
    return "[...document.querySelectorAll(%s)].filter(e=>e.getClientRects().length).pop()" % json.dumps(f'{MSGS} {css}')


def achar_contem(css, trecho):
    return "[...document.querySelectorAll(%s)].filter(e=>e.getClientRects().length&&e.innerText.includes(%s)).pop()" % (
        json.dumps(f'{MSGS} {css}'), json.dumps(trecho, ensure_ascii=False))


# ---------------------------------------------------------------- capítulos
def cap00():
    """Abertura: ilustração do problema (L1 e L2); a tela Estoque e a câmera até o botão do Cato (L3); cartão "Antes" (L4)."""
    c = Cap(0, login() + IR_ESTOQUE, pace=0.6, start=(640, 420))
    c.mark(1)
    c.mark(2)
    c.mark(3)
    c.hover(FAB, seconds=2.5, at=c.A(3, 'Cato', 0.7), label='botão do Cato (a câmera vai até ele)', noScroll=True)
    c.mark(4)
    c.rolar(0, at=c.A(4, 'tutorial', 0.4), ponto=(420, 470), duration=0.8, label='cursor sai do botão (cartão Antes)')
    c.fim()
    return c


def cap01():
    """Onde o Cato fica: zoom no botão (L1), ilustração computador × celular (L2), clique: a janela de autorização (L3)."""
    c = Cap(1, login() + IR_ESTOQUE, pace=0.6, start=(760, 420))
    c.mark(1)
    c.hover(FAB, seconds=2.2, at=c.A(1, 'botão', 0.7), label='ZOOM botão redondo do Cato (Abrir o Cato)', noScroll=True)
    c.rolar(0, at=c.A(1, 'qualquer', 0.3), ponto=(420, 470), duration=0.8, label='cursor solta o botão (em qualquer tela)')
    c.mark(2)
    c.mark(3)
    c.click(FAB, at=c.A(3, 'clicar', 0.8), label='clique no botão do Cato', noScroll=True)
    c.waitfor(text='Antes da primeira conversa com o Cato', timeout=8)
    c.hover(TXT('Antes da primeira conversa com o Cato'), seconds=1.2, at=c.A(3, 'autorização', 0.7), label='janela Antes da primeira conversa com o Cato')
    c.fim()
    return c


SETUP_AUTORIZACAO = login() + IR_ESTOQUE + [
    {'do': 'click', 'target': FAB, 'noScroll': True},
    {'do': 'waitFor', 'text': 'Antes da primeira conversa com o Cato', 'timeout': 10}, {'do': 'wait', 'seconds': 0.8}]


def cap02():
    """Autorizar o Cato: a janela (L1), ilustração do caminho da pergunta (L2), microfone e leitura (L3), "pode errar" (L4); L5 é o
    corte do Marcos (cap02b; aqui a janela fica parada); "Entendi e autorizo" → "Cato autorizado" e o painel (L6)."""
    c = Cap(2, SETUP_AUTORIZACAO, pace=0.5, start=(560, 300))
    c.mark(1)
    c.hover(TXT('Leia rapidinho como ele trata os dados da sua empresa.'), seconds=0.6, at=c.A(1, 'janela', 0.5), label='janela de autorização (subtítulo)')
    c.hover(PONTO('O Cato lê os dados da sua conta'), seconds=0.8, at=c.A(1, 'linhas', 0.6), label='a câmera desce pelos pontos (1º)')
    c.hover(PONTO('Pra montar a resposta, esses trechos passam'), seconds=0.6, at=c.A(1, 'trata', 0.6), label='a câmera desce pelos pontos (2º)')
    c.mark(2)
    c.ev(js_dlg_fundo(0), at=c.A(2, 'serviços', 0.0), label='sob a ilustração: o miolo da janela rola até o fim (pontos de voz, erros e botões)')
    c.mark(3)
    c.hover(PONTO('O microfone só liga quando você toca nele'), seconds=0.5, at=c.A(3, 'microfone', 0.7), label='ZOOM ponto do microfone')
    c.hover(PONTO('Ouvir a resposta'), seconds=1.5, at=c.A(3, 'leitura', 0.6), label='ZOOM ponto de Ouvir a resposta')
    c.mark(4)
    c.hover(PONTO('O Cato pode errar'), seconds=2.5, at=c.A(4, 'errar', 0.9), label='ZOOM O Cato pode errar. Use como apoio e confira os números antes de decidir.')
    c.mark(5)
    c.ev(js_dlg_fundo(0), at=c.A(5, 'janela', 0.0), label='sob o corte do Marcos: a janela no fim (o botão à vista)')
    c.rolar(0, at=c.A(5, 'aviso', 0.0), ponto=(700, 560), duration=0.5, label='sob o corte do Marcos: cursor perto do botão')
    c.mark(6)
    c.hover(BTN('Entendi e autorizo'), seconds=0.6, at=c.A(6, 'administrador', 0.6), label='Entendi e autorizo (o Rafael é o administrador)')
    c.click(BTN('Entendi e autorizo'), at=c.A(6, 'Entendi', 0.5), label='clique em Entendi e autorizo')
    c.waitfor(text='Cato autorizado', timeout=8)
    c.waitfor(selector=PAINEL, timeout=8)
    c.hover(SEL('[data-sonner-toast]:has-text("Cato autorizado")'), seconds=1.2, at=c.A(6, 'Pronto', 0.5), label='aviso Cato autorizado', noScroll=True)
    c.hover(NO_PAINEL('p:has-text("Oi, Rafael")'), seconds=1.0, at=c.A(6, 'empresa', 0.6), label='o painel do Cato abre à direita')
    c.fim()
    return c


def cap02b():
    """Corte do cap02, linha 5: o Marcos (não administrador) clica no botão do Cato e a janela mostra o aviso, sem o botão de autorizar."""
    setup = login(EMAIL_MARCOS) + IR_ESTOQUE
    c = Cap(2, setup, pace=0.5, start=(900, 520), sub='b', voz_de=(5, 5), user='marcos')
    c.mark(1)
    c.click(FAB, at=c.A(1, 'Uma', 0.3), label='Marcos clica no botão do Cato', noScroll=True)
    c.waitfor(text='Só o administrador da empresa pode autorizar o Cato.', timeout=8)
    c.ev(js_dlg_fundo(900), at=c.A(1, 'Pra', 0.3), label='a janela desce até o aviso')
    c.hover(TXTP('Só o administrador da empresa pode autorizar o Cato.'), seconds=1.3, at=c.A(1, 'aviso', 1.0), label='ZOOM aviso Só o administrador da empresa pode autorizar o Cato.')
    c.hover(BTN('Entendi'), seconds=1.2, at=c.A(1, 'pedir', 0.5), label='Entendi (a saída: pedir pro administrador)')
    c.fim()
    return c


SETUP_PAINEL = login() + IR_ESTOQUE


def cap03():
    """As perguntas prontas: o painel abre com "Oi, Rafael 👋" e as quatro perguntas (L1); campo e Enviar (L2); a primeira pergunta
    (L3) e a resposta R1 com vendas e resultado (L4); as três sugestões (L5)."""
    c = Cap(3, SETUP_PAINEL, pace=0.5, start=(900, 560))
    c.mark(1)
    c.click(FAB, at=c.A(1, 'painel', 0.7), label='abre o Cato (o painel abre à direita)', noScroll=True)
    c.waitfor(text='Pergunte o que quiser sobre seu negócio', timeout=8)
    c.ev("JSON.stringify({rota:location.pathname,prontas:[...document.querySelectorAll('%s button')].map(b=>b.innerText.trim()).filter(t=>t.endsWith('?')).slice(0,6)})" % PAINEL.replace('"', '\\"'), label='as perguntas prontas da tela')
    c.hover(NO_PAINEL('button:has-text("Como tá indo meu negócio esse mês?")'), seconds=0.3, at=c.A(1, 'quatro', 0.6), label='as quatro perguntas prontas (1ª)')
    c.hover(NO_PAINEL('button:has-text("Qual material me deu mais faturamento?")'), seconds=0.4, at=c.A(1, 'prontas', 0.5), label='as quatro perguntas prontas (4ª)')
    c.mark(2)
    c.hover(NO_PAINEL('button:has-text("Quanto tenho em estoque agora?")'), seconds=0.3, at=c.A(2, 'clicar', 0.6), label='clicar numa delas')
    c.hover(CAMPO, seconds=0.8, at=c.A(2, 'escrever', 0.6), label='campo Pergunte ao Cato…', noScroll=True)
    c.hover(ENVIAR, seconds=0.8, at=c.A(2, 'jeito', 0.6), label='botão Enviar', noScroll=True)
    c.mark(3)
    c.click(NO_PAINEL('button:has-text("Como tá indo meu negócio esse mês?")'), at=c.A(3, 'primeira', 0.7), label='clique em Como tá indo meu negócio esse mês?')
    c.waitfor(text='Pensando…', timeout=6)
    c.mark(4)
    c.waitfor(text='Consultei seu resumo financeiro', timeout=12)
    c.hover(LI('Vendas: R$ 118.620,20'), seconds=1.2, at=c.A(4, 'vendeu', 0.6), label='ZOOM Vendas R$ 118.620,20')
    c.hover(FORTE('R$ 69.589,55'), seconds=1.5, at=c.A(4, 'resultado', 0.6), label='ZOOM resultado R$ 69.589,55')
    c.confere('painel', ['Vendas: R$ 118.620,20', 'R$ 69.589,55', 'Regime de caixa'], 'R1 na tela')
    c.mark(5)
    c.waitfor(text='Compara com outubro', timeout=6)
    c.hover(NO_PAINEL('button:has-text("Compara com outubro")'), seconds=0.4, at=c.A(5, 'sugere', 0.6), label='sugestões de próxima pergunta (1ª)')
    c.hover(NO_PAINEL('button:has-text("Quais despesas tive esse mês?")'), seconds=1.2, at=c.A(5, 'clicar', 0.6), label='sugestões (2ª; a 3ª fica fora da faixa, que rola de lado)')
    c.fim()
    return c


def cap04():
    """O que ele responde bem (a conversa do cap03): R2 quem tá me devendo (L1, L2), R3 estoque (L3), R4 banco (L4), R5 caixa (L5);
    ilustração caixa do dia × mês (L6)."""
    c = Cap(4, restaura(1), pace=0.5, start=(900, 560))
    c.mark(1)
    c.pergunta('Quem tá me devendo?', c.A(1, 'perguntas', 0.3), None, 'R2')
    c.mark(2)
    c.waitfor(text='Consultei os saldos dos parceiros', timeout=8)
    c.ev(js_msgs_rola(achar_ultimo('div.items-end'), 165, 600), at=c.A(2, 'somam', 0.0), label='a conversa sobe até o começo da resposta (o gráfico empurrou)')
    c.hover(FORTE('R$ 17.540,00'), seconds=1.0, at=c.A(2, 'dezessete', 0.2), label='ZOOM total R$ 17.540,00')
    c.hover(LI('Fundição Bandeira do Vale: R$ 14.370,00'), seconds=1.2, at=c.A(2, 'Fundição', 0.6), label='ZOOM Fundição Bandeira do Vale: R$ 14.370,00')
    c.mark(3)
    c.pergunta('Quanto tenho em estoque agora?', c.A(3, 'No', 0.6), None, 'R3')
    c.waitfor(text='Consultei seu estoque', timeout=8)
    c.hover(FORTE('R$ 96.076,00'), seconds=1.0, at=c.A(3, 'noventa', 0.5), label='valor pelo custo médio R$ 96.076,00')
    c.hover(LI('Alumínio perfil: 3.385 kg'), seconds=1.0, at=c.A(3, 'alumínio', 0.6), label='alumínio perfil na frente')
    c.mark(4)
    c.pergunta('Qual o saldo das minhas contas no banco?', c.A(4, 'No', 0.9), None, 'R4')
    c.waitfor(text='Consultei seu resumo bancário', timeout=8)
    c.hover(FORTE('R$ 132.448,67'), seconds=0.8, at=c.A(4, 'dois', 0.5), label='saldo de agora R$ 132.448,67')
    c.hover(LI('Conta Cooperativa'), seconds=0.6, at=c.A(4, 'três', 0.5), label='as três contas')
    c.hover(NO_PAINEL('p:has-text("entraram")'), seconds=0.8, at=c.A(4, 'entrou', 0.6), label='o que entrou e saiu no mês')
    c.mark(5)
    c.pergunta('Como tá meu caixa hoje?', c.A(4, 'mês', -0.2), None, 'R5')
    c.waitfor(text='Consultei seu caixa', timeout=8)
    c.hover(FORTE('não tem caixa aberto'), seconds=0.6, at=c.A(5, 'ele', 0.3), label='hoje ainda não tem caixa aberto')
    c.hover(FORTE('R$ 640,00'), seconds=1.0, at=c.A(5, 'fecharam', 0.4), label='os caixas de ontem')
    c.mark(6)
    c.fim()
    return c


def cap05():
    """Gráfico ou tabela: R6 três meses em linha (L1, L2), R7 vendas por cliente em outubro em barras (L3), ilustração saldo ×
    movimentado (L4, L5), R8 estoque em tabela (L6), ilustração da regra (L7)."""
    c = Cap(5, restaura(5), pace=0.5, start=(900, 560))
    c.mark(1)
    c.pergunta('Compras e vendas dos últimos três meses', c.A(1, 'pergunta', 0.6), c.A(1, 'meses', 0.4), 'R6')
    c.waitfor(text='Consultei suas compras e vendas', timeout=8)
    c.hover(NO_PAINEL('div.rounded-2xl:has-text("Compras e vendas por mês")'), seconds=1.0, at=c.A(1, 'linha', 0.6), label='gráfico de linha Compras e vendas por mês')
    c.mark(2)
    c.hover(NO_PAINEL('div.rounded-2xl:has-text("Compras e vendas por mês") circle.recharts-dot >> nth=1'), seconds=1.5, at=c.A(2, 'outubro', 0.6), label='outubro: as compras quase alcançam as vendas (dica do gráfico)')
    c.hover(NO_PAINEL('div.rounded-2xl:has-text("Compras e vendas por mês") circle.recharts-dot >> nth=5'), seconds=1.5, at=c.A(2, 'novembro', 0.6), label='novembro: as vendas passam longe das compras (dica do gráfico)')
    c.mark(3)
    c.pergunta('Pra quem eu mais vendi em outubro?', c.A(3, 'Agora', 0.7), None, 'R7')
    c.waitfor(text='Fundição Bandeira do Vale: R$ 112.800,00', timeout=8)
    c.ev(js_msgs_rola(achar_ultimo('div.items-end'), 165, 500), at=c.A(3, 'com', 0.1), label='a conversa sobe até o começo da resposta (o gráfico empurrou)')
    c.hover(LI('Fundição Bandeira do Vale: R$ 112.800,00'), seconds=1.2, at=c.A(3, 'doze', 0.3), label='ZOOM Fundição Bandeira do Vale: R$ 112.800,00')
    c.mark(4)
    c.mark(5)
    c.mark(6)
    c.pergunta('Lista meu estoque em tabela', c.A(5, 'diferentes', -0.4), None, 'R8')
    c.waitfor(text='Estoque em 10/11/2026', timeout=8)
    c.ev(js_msgs_rola(achar_ultimo('div.items-end'), 165, 500), at=c.A(6, 'com', 0.0), label='a conversa sobe até o começo da resposta (a tabela empurrou)')
    c.hover(NO_PAINEL('th:has-text("Material")'), seconds=0.15, at=c.A(6, 'material', 0.0), label='tabela: Material')
    c.hover(NO_PAINEL('th:has-text("Quantidade")'), seconds=0.15, at=c.A(6, 'quantidade', 0.2), label='tabela: Quantidade (kg)')
    c.hover(NO_PAINEL('th:has-text("Valor em estoque")'), seconds=0.15, at=c.A(6, 'valor', 0.5), label='tabela: Valor em estoque')
    c.mark(7)
    c.fim()
    return c


def cap06():
    """De onde vêm os números (a resposta da tabela, R8): "Consultei seu estoque", período e hora (L1); o botão "Abrir posição de
    estoque" (L2); a Posição de Estoque com o "Total geral" (L3); ilustração (L4); o painel de novo e o rodapé (L5)."""
    c = Cap(6, restaura(8, aquecer=('/materiais/posicao-estoque',)), pace=0.5, start=(900, 560))
    c.mark(1)
    c.ev(js_msgs_rola(achar_contem('div.items-start', 'Aqui está o seu estoque de agora'), 150, 700), at=c.A(1, 'cima', 0.8), label='sobe a conversa até o topo da resposta da tabela')
    c.hover(NO_PAINEL('p:text-is("Consultei seu estoque") >> nth=-1'), seconds=0.6, at=c.A(1, 'tirou', 0.6), label='ZOOM Consultei seu estoque')
    c.hover(NO_PAINEL('span:has-text("Período 10 nov. 2026") >> nth=-1'), seconds=0.5, at=c.A(1, 'período', 0.5), label='ZOOM linha do período')
    c.hover(NO_PAINEL('span:has-text("Atualizado às") >> nth=-1'), seconds=0.8, at=c.A(1, 'hora', 0.5), label='ZOOM Atualizado às')
    c.mark(2)
    c.ev(js_fim_da_conversa(900), at=c.A(2, 'lidos', 0.6), label='desce pela tabela')
    c.hover(NO_PAINEL('button:has-text("Abrir posição de estoque") >> nth=-1'), seconds=1.0, at=c.A(2, 'botão', 0.6), label='botão Abrir posição de estoque')
    c.mark(3)
    c.click(NO_PAINEL('button:has-text("Abrir posição de estoque") >> nth=-1'), at=c.A(3, 'Posição', 0.6), label='clique em Abrir posição de estoque')
    c.waitfor(text='Total geral', timeout=10)
    c.click(NO_PAINEL('button[aria-label="Fechar"]'), at=c.A(3, 'Estoque', 0.3), label='Fechar o painel', noScroll=True)
    c.waitfor(gone=PAINEL, timeout=6)
    c.ev(js_rola_el(achar_folha('main', 'Total geral'), 430, 800), at=c.A(3, 'total', 0.5), label='desce até o Total geral')
    c.hover(SEL('main tr:has-text("Total geral")'), seconds=1.8, at=c.A(3, 'noventa', 0.7), label='ZOOM Total geral com Valor R$ 96.076,00')
    c.confere('main', ['Total geral', 'R$ 96.076,00'], 'Total geral igual ao da resposta')
    c.mark(4)
    c.mark(5)
    c.click(FAB, at=c.L(5) - 0.4, label='abre o Cato de novo (a conversa volta)', noScroll=True)
    c.waitfor(selector=PAINEL, timeout=6)
    c.hover(NO_PAINEL('p:has-text("O Cato.ai pode cometer erros")'), seconds=1.5, at=c.A(5, 'erros', 0.9), label='rodapé O Cato.ai pode cometer erros', noScroll=True)
    c.hover(NO_PAINEL('button:has-text("Abrir posição de estoque") >> nth=-1'), seconds=1.0, at=c.A(5, 'botão', 0.6), label='confira na tela, por aquele botão')
    c.fim()
    return c


def cap07():
    """Os limites: R9 "Emite a nota da venda pra Fundição Bandeira do Vale" (L1) e a orientação (L2); ilustrações consulta × executa
    (L3) e limites de uso (L4)."""
    c = Cap(7, restaura(8), pace=0.5, start=(900, 560))
    c.mark(1)
    c.mark(2)
    c.pergunta('Emite a nota da venda pra Fundição Bandeira do Vale', 0.0, None, 'R9', cps=60)
    c.waitfor(text='Consultei a central de ajuda', timeout=8)
    c.hover(FORTE('Emitir nota fica com você'), seconds=0.8, at=c.A(2, 'fica', 0.6), label='Emitir nota fica com você')
    c.hover(NO_PAINEL('ol >> nth=-1'), seconds=1.5, at=c.A(2, 'caminho', 0.6), label='o caminho no sistema, passo a passo')
    c.mark(3)
    c.mark(4)
    c.fim()
    return c


def cap08():
    """Avaliar e falar com o suporte: 👍 na resposta da tabela (L1), 👎 na da nota com "Faltou detalhe" (L2), "Falar com atendente"
    (L3) e a janela "Falar com o suporte" até "Falar no WhatsApp", sem clicar (L4)."""
    c = Cap(8, restaura(9), pace=0.5, start=(900, 560))
    c.mark(1)
    c.ev(js_msgs_rola(achar_ultimo('button[aria-label="Resposta útil"]') .replace('.pop()', '.at(-2)'), 260, 700), at=c.A(1, 'resposta', 0.5), label='sobe até as ações da resposta da tabela')
    c.hover(NO_PAINEL('button[aria-label="Resposta útil"] >> nth=7'), seconds=0.5, at=c.A(1, 'joinha', 0.5), label='joinha (Resposta útil)')
    c.hover(NO_PAINEL('button[aria-label="Resposta não útil"] >> nth=7'), seconds=0.5, at=c.A(1, 'dedo', 0.5), label='dedo pra baixo (Resposta não útil)')
    c.click(NO_PAINEL('button[aria-label="Resposta útil"] >> nth=7'), at=c.A(1, 'clicar', 0.6), label='clique no joinha da resposta da tabela')
    c.mark(2)
    c.ev(js_fim_da_conversa(600), at=c.A(2, 'não', 0.5), label='desce até a resposta da nota')
    c.click(NO_PAINEL('button[aria-label="Resposta não útil"] >> nth=8'), at=c.A(2, 'dedo', 0.6), label='dedo pra baixo na resposta da nota')
    c.waitfor(text='Faltou detalhe', timeout=5)
    c.hover(NO_PAINEL('button:text-is("Número errado")'), seconds=0.4, at=c.A(2, 'motivos', 0.5), label='os motivos')
    c.click(NO_PAINEL('button:text-is("Faltou detalhe")'), at=c.A(2, 'clique', 0.6), label='Faltou detalhe')
    c.mark(3)
    c.hover(NO_PAINEL('button:has-text("Falar com atendente")'), seconds=0.6, at=c.A(3, 'embaixo', 0.6), label='Falar com atendente', noScroll=True)
    c.click(NO_PAINEL('button:has-text("Falar com atendente")'), at=c.A(3, 'Falar', 0.5), label='clique em Falar com atendente', noScroll=True)
    c.waitfor(text='Nos conte o que está acontecendo pra resolvermos mais rápido.', timeout=8)
    c.mark(4)
    c.hover(TXTP('Em qual tela/módulo?', within=DLG_SUP), seconds=0.5, at=c.A(4, 'tela', 0.6), label='Em qual tela/módulo? *')
    c.hover(TXTP('O que aconteceu? Descreva com detalhes', within=DLG_SUP), seconds=0.5, at=c.A(4, 'aconteceu', 0.6), label='O que aconteceu? Descreva com detalhes *')
    c.hover(BTN('Falar no WhatsApp', within=DLG_SUP), seconds=1.5, at=c.A(4, 'WhatsApp', 0.7), label='Falar no WhatsApp (sem clicar)')
    c.press('Escape', at=c.A(4, 'escrito', -0.6), label='fecha a janela')
    c.fim()
    return c


CAPITULOS = {'0': cap00, '1': cap01, '2': cap02, '2b': cap02b, '3': cap03, '4': cap04, '5': cap05, '6': cap06, '7': cap07, '8': cap08}


# ---------------------------------------------------------------- main
def main():
    pedidos = [a.lstrip('0') or '0' for a in sys.argv[1:] if re.fullmatch(r'\d+b?', a)]
    feitos = []
    for k, fn in CAPITULOS.items():
        if pedidos and k not in pedidos:
            continue
        c = fn()
        d = c.out()
        json.dump(d, open(os.path.join(HERE, f'{c.nome}.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
        nat = sum(1 for st in d['steps'] if st.get('do') != 'mark')
        feitos.append(f'{c.nome} {nat} passos, {len(c.linhas)} linhas, {c.dur:.1f} s{" (fala estimada)" if c.estimado else ""}')
        if os.environ.get('ANCORAS'):
            for i, p, t in c.anchors:
                print(f'   {c.nome} L{i} {p!r} -> {t}')
    print('\n'.join(feitos))


if __name__ == '__main__':
    main()
