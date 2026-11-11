#!/usr/bin/env python3
"""T01 · gera rec/t01/cap00..cap13.json (roteiros do robô) a partir da voz (t01/narracao/capNN.json).

EcoFlix T1 "Sua conta e sua empresa": EcoSistema 1.59.154 no COMPUTADOR (janela 1280x800, tema claro), Supabase falso com o mundo
da Recicla Vale Metais, logado como Rafael Nogueira (MASTER). FAKE_NOW 2026-11-10T08:30:00-03:00 em todos os capítulos.
Os `at` saem da palavra que anuncia cada passo: A(linha, palavra, folga) = início da palavra - folga (folga = custo do gesto,
docs/04-gravacao.md "Custo real dos gestos"). Hoje a voz é ESTIMADA (capNN.json com "estimado"); quando a voz chegar, roda-se
de novo com o capNN.json da voz e o roteiro sai preso às palavras de verdade, sem reescrever nada aqui.
Rodar de qualquer pasta: `python3 -I rec/t01/gerar.py [NN ...]`. Depois: `node rec/record.mjs rec/t01/capNN.json --check`.

Todos os capítulos abrem SEM sessão ("anonymous": true): os caps 0 a 4 são as páginas públicas (/cadastro, /login), e dos caps 5
a 13 o `setup` entra pelo formulário do /login com "$TUT_USER"/"$TUT_SENHA" (nunca no vídeo; a senha nunca vai para arquivo).
O cap03 entra pela tela de propósito: é o login pelo formulário que salva a sessão do trocador de contas.

Cadeia de sementes (rec/mundo/seeds-extra/t01/): `inicio` (a empresa como sai de um cadastro novo) e, a cada capítulo que mexe no
banco, o `apos-capNN` (SEMENTE abaixo). O `apos-capNN` vem do que o robô digita no capítulo (conferido no estado do ensaio).

Particularidades (lições deste tutorial, app 1.59.154):
 - O app recusa o login pela tela quando o `iat` do token difere mais de 5 min do relógio do navegador (Auth.tsx,
   detectAuthClockSkew): o Supabase falso assina o token no relógio do mundo (FAKE_NOW), igual ao navegador do robô.
 - Botões do rodapé do menu lateral ("Configurações", "Sair", o card da conta) ficam em y 690 a 788: `noScroll`.
 - Observador `OBS` guarda em `window.__avisos` todo aviso de erro do app e as janelas que não podem aparecer na chegada
   (preferências, outro acesso, versão nova, relógio, lembrete da trilha); o passo final devolve a lista (tem de sair vazia).
 - `confere*` LÊ a tela e compara com a fala (o `resumo.py` acusa DIFERENTE).
"""
import json
import os
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TUT = os.path.normpath(os.path.join(HERE, '..', '..'))
NARR = os.path.join(TUT, 't01', 'narracao')
RAFAEL = '34c36c63-0890-5e89-8963-7c77b7996908'
EMPRESA_ID = '38814e47-876a-5977-a5f7-53af364c17bb'
VERSAO = '1.59.154'
FAKE_NOW = '2026-11-10T08:30:00-03:00'
# localStorage de quem abre o navegador sem sessão: sem aviso de versão nova, sem o convite para instalar o app, sem a janela
# "Personalize sua experiência" e sem o lembrete das tarefas do dia (a mesma lista que o robô põe numa sessão logada)
STORAGE = {'app_version': VERSAO, 'notification_shown_version': VERSAO, 'pwa-install-dismissed': 'true', 'theme': 'light',
           'initial-preferences-set': 'true', f'daily-tasks-reminder-last-shown-{RAFAEL}': '2026-11-10'}

NOMES = ['Abertura', 'Criar a conta', 'Os 7 dias de teste', 'Entrar no sistema', 'Esqueci minha senha', 'Logo, ícone, nome e CNPJ',
         'Contato e endereço', 'Numeração de pedidos', 'A frase do comprovante', 'O jeito do pátio', 'Condições de pagamento',
         'Aparência e atalhos', 'Senha, termos e Zona de Perigo', 'Recapitulando']
# estado de partida de cada capítulo (sementes por cima do mundo base, na ordem). Os caps 7, 9, 11, 12 e 13 só leem.
CADEIA = ['t01/inicio', 't01/apos-cap05', 't01/apos-cap06', 't01/apos-cap08', 't01/apos-cap10']
ATE = {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 2, 7: 3, 8: 3, 9: 4, 10: 4, 11: 5, 12: 5, 13: 5}
SEMENTE = {n: CADEIA[:k] for n, k in ATE.items()}

# Observador de avisos na tela (aceite do ensaio): erro do app e janela que não pode aparecer na chegada ao sistema.
OBS = ("(()=>{window.__avisos=[];const re=/N[ãa]o foi poss[ií]vel|Erro ao|Tente novamente|indispon[ií]vel|Algo deu errado|Falha ao carregar|"
       "Personalize sua experi[êe]ncia|Voc[êe] j[áa] est[áa] conectado|Sistema atualizado|O rel[óo]gio deste computador|Sess[ãa]o expirou/i;"
       "const chk=(t)=>{t=(t||'').trim();const m=t&&t.match(new RegExp('[^]{0,40}('+re.source+')[^]{0,40}','i'));"
       "if(m&&window.__avisos.length<10)window.__avisos.push(m[0].replace(/[\\n\\r\\t ]+/g,' '))};new MutationObserver(ms=>{for(const m of ms){"
       "m.addedNodes.forEach(n=>chk(n.textContent));if(m.type==='characterData')chk(m.target.textContent)}}).observe(document.body,"
       "{childList:true,subtree:true,characterData:true});chk(document.body.innerText);"
       "setInterval(()=>{const f=document.querySelector('section[aria-label^=\"Lembrete da trilha\"]');"
       "if(f&&window.__avisos.length<10&&!window.__avisos.includes('LEMBRETE DA TRILHA'))window.__avisos.push('LEMBRETE DA TRILHA')},300);return 1})()")


def norm(s):
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode().lower()
    return ''.join(ch for ch in s if ch.isalnum() or ch in '?')


def carregar_voz(n):
    """voz do capítulo (t01/narracao/capNN.json: a estimada agora, a de verdade depois): (words, linhas, dur, estimada)"""
    d = json.load(open(os.path.join(NARR, f'cap{n:02d}.json'), encoding='utf8'))
    return d['words'], d['linhas'], float(d['dur']), bool(d.get('estimado'))


class Cap:
    def __init__(s, n, pace=0.5, cps=14, start=(900, 440), prewarm=None, setup=None, storage=None, tail=1.5):
        s.n = n
        s.words, s.linhas, s.dur, s.estimada = carregar_voz(n)
        s.steps = []
        s.pace, s.cps, s.start, s.tail = pace, cps, start, tail
        s.prewarm = prewarm or ['/login']
        s.storage = dict(STORAGE, **(storage or {}))
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

    def A(s, i, palavra, folga=0.8, nth=0):
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
            if d.get('do') == 'type':
                for mt, mi in list(s.pending):
                    if d['at'] < mt <= d['at'] + 2.6:
                        s.steps.append({'do': 'mark', 'name': f'L{mi}', 'at': round(d['at'], 2)})
                        s.pending.remove((mt, mi))
            s.flush(d['at'])
        s.steps.append(d)
        return d

    def mark(s, i):
        t = max(0.0, s.L(i) - 0.9) if s.L(i) > 0.9 else s.L(i)
        if t <= 0:
            s.steps.append({'do': 'mark', 'name': f'L{i}', 'at': 0})
        else:
            s.pending.append((t, i))

    def _p(s, d, at, label, kw):
        if at is not None:
            d['at'] = round(at, 2)
        if label:
            d['label'] = label
        d.update(kw)
        return s.add(d)

    def click(s, target, at=None, label=None, **kw):
        return s._p({'do': 'click', 'target': target}, at, label, kw)

    def hover(s, target, seconds=0.9, at=None, label=None, **kw):
        kw.setdefault('optional', True)
        kw.setdefault('timeout', 3)
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

    def press(s, key, at=None, label=None, **kw):
        return s._p({'do': 'press', 'key': key}, at, label, kw)

    def upload(s, target, arquivo, at=None, label=None, **kw):
        return s._p({'do': 'upload', 'target': target, 'file': arquivo}, at, label, kw)

    def rolar(s, by, at=None, label=None, ponto=(760, 420), duration=0.5, after=100):
        return s._p({'do': 'scroll', 'point': {'x': ponto[0], 'y': ponto[1]}, 'by': by, 'duration': duration, 'after': after}, at, label, {})

    def cursor(s, ponto, at=None, label=None):
        """leva o cursor a um ponto neutro sem clicar (scroll de 0 px)"""
        return s.rolar(0, at=at, label=label, ponto=ponto, duration=0.3, after=0)

    def registra(s, target, at=None, label=None, **kw):
        """registra o retângulo do alvo para a câmera SEM mexer o mouse (type vazio sem clique)"""
        return s._p({'do': 'type', 'target': target, 'text': '', 'noClick': True, 'optional': True, 'timeout': 4}, at, label, kw)

    def confere(s, escopo, esperados, label):
        """`eval` que LÊ a tela e compara com o que a fala diz: "OK: ..." ou "DIFERENTE: ...". Escopo 'dlg' (a última janela), 'main',
        'body' ou um seletor CSS. Tenta por ~6,5 s."""
        sel = {'dlg': "[role=dialog]", 'main': 'main', 'body': 'body'}.get(escopo, escopo)
        esp = [esperados] if isinstance(esperados, str) else list(esperados)
        js = ("(async()=>{const norm=t=>t.replace(/[\\s\\u00a0]+/g,' ').toLowerCase();const esp=%s;let out='';"
              "for(let i=0;i<22;i++){const els=[...document.querySelectorAll(%s)];const el=%s?els[els.length-1]:els[0];"
              "if(!el){out='DIFERENTE: sem elemento';}else{const t=norm(el.innerText);const falta=esp.filter(e=>!t.includes(norm(e)));"
              "if(!falta.length)return 'OK: '+esp.join(' | ');out='DIFERENTE: faltou '+JSON.stringify(falta)+' em: '+t.slice(0,260);}"
              "await new Promise(r=>setTimeout(r,300));}return out})()") % (json.dumps(esp, ensure_ascii=False), json.dumps(sel), 'true' if escopo == 'dlg' else 'false')
        return s.add({'do': 'eval', 'js': js, 'label': 'confere ' + label})

    def confere_campos(s, esperados, label, escopo='main'):
        """lê o VALOR dos campos (input/textarea) do escopo e compara com o que a fala diz"""
        esp = [esperados] if isinstance(esperados, str) else list(esperados)
        js = ("(async()=>{const esp=%s;let out='';for(let i=0;i<12;i++){const v=[...document.querySelectorAll(%s+' input, '+%s+' textarea')].map(e=>e.value).join(' | ');"
              "const falta=esp.filter(e=>!v.includes(e));if(!falta.length)return 'OK: '+esp.join(' | ');out='DIFERENTE: faltou '+JSON.stringify(falta)+' em: '+v.slice(0,260);"
              "await new Promise(r=>setTimeout(r,300));}return out})()") % (json.dumps(esp, ensure_ascii=False), json.dumps(escopo), json.dumps(escopo))
        return s.add({'do': 'eval', 'js': js, 'label': 'confere ' + label})

    def confere_ausente(s, escopo, texto, label, espera=0.6):
        sel = {'dlg': '[role=dialog]', 'main': 'main', 'body': 'body'}.get(escopo, escopo)
        js = ("(async()=>{await new Promise(r=>setTimeout(r,%d));" % int(espera * 1000) + "const el=document.querySelector(%s);const t=(el?el.innerText:'').replace(/[\\s\\u00a0]+/g,' ').toLowerCase();"
              "return t.includes(%s)?'DIFERENTE: apareceu '+%s:'OK: ausente '+%s})()") % (json.dumps(sel), json.dumps(texto.lower()), json.dumps(texto), json.dumps(texto))
        return s.add({'do': 'eval', 'js': js, 'label': 'confere ' + label})

    def pause(s, seconds):
        return s.add({'do': 'pause', 'seconds': seconds})

    def wait(s, seconds):
        return s.add({'do': 'wait', 'seconds': seconds})

    def waitfor(s, **kw):
        return s.add({'do': 'waitFor', **kw})

    def ev(s, js, at=None, label=None, **kw):
        return s._p({'do': 'eval', 'js': js}, at, label, kw)

    def encaixa(s):
        """hover que invade o próximo gesto com `at` encolhe o `seconds` (deslocamento do cursor ~0,6 s a pace 0,5, ~0,8 s a 0,6):
        sem isso o atraso de um hover se soma ao do seguinte (docs/08, T7 cap. 1)"""
        mov = 0.6 if s.pace <= 0.5 else 0.8
        timed = [st for st in s.steps if st.get('do') != 'mark' and 'at' in st]
        for st, nx in zip(timed, timed[1:]):
            if st['do'] == 'hover':
                livre = round(nx['at'] - st['at'] - mov - 0.05, 2)
                if st.get('seconds', 0.9) > livre:
                    st['seconds'] = max(0.2, livre)

    def fim(s):
        s.flush(1e9)
        s.encaixa()
        s.steps.append({'do': 'eval', 'js': 'JSON.stringify(window.__avisos || "sem observador")', 'label': 'avisos de erro na tela'})
        s.steps.append({'do': 'mark', 'name': 'FIM', 'at': round(s.dur, 2)})

    def out(s):
        sem = SEMENTE[s.n]
        d = {
            'name': f't01-cap{s.n:02d}',
            'title': f'T01 · Cap. {s.n} · {NOMES[s.n]} (narração {str(round(s.dur, 1)).replace(".", ",")} s{" ESTIMADA" if s.estimada else ""}; '
                     f'marcas L1..L{len(s.linhas)} = início de cada linha do roteiro; FAKE_NOW {FAKE_NOW})',
            'seed': f't01-cap{s.n:02d}', 'pace': s.pace, 'cps': s.cps, 'tail': s.tail,
            'start': {'x': s.start[0], 'y': s.start[1]},
            'anonymous': True,
            'seedExtra': list(sem),
            'storage': dict(s.storage),
            'prewarm': s.prewarm, 'setup': s.setup, 'steps': s.steps,
        }
        return d


# ---------------------------------------------------------------- alvos
BTN = lambda n, **kw: {'role': 'button', 'name': n, 'exact': True, **kw}
BTNX = lambda n, **kw: {'role': 'button', 'name': n, **kw}
LINK = lambda n, **kw: {'role': 'link', 'name': n, 'exact': True, **kw}
TAB = lambda n, **kw: {'role': 'tab', 'name': n, 'exact': True, **kw}
TXT = lambda t, **kw: {'text': t, 'exact': True, **kw}
TXTP = lambda t, **kw: {'text': t, **kw}                       # texto contido (o elemento traz mais coisa)
PH = lambda p, **kw: {'placeholder': p, **kw}
SEL = lambda s_, **kw: {'selector': s_, **kw}
SW = lambda n, **kw: {'role': 'switch', 'name': n, **kw}
CHK = lambda n, **kw: {'role': 'checkbox', 'name': n, **kw}
DLG = '[role=dialog]'
AGUARDA = {'do': 'waitFor', 'idle': True}

# ---------------------------------------------------------------- trechos comuns (não filmados, no `setup`)
EMAIL_LOGIN = PH('seu@email.com')
SENHA_LOGIN = SEL('input[type=password]')
CARD_CONTA = SEL("[aria-label='Menu da conta']")
LOGIN = [  # entra pelo formulário do /login com as variáveis do ambiente (fora do vídeo)
    {'do': 'goto', 'url': '/login'},
    {'do': 'waitFor', 'target': EMAIL_LOGIN, 'timeout': 30},
    {'do': 'type', 'target': EMAIL_LOGIN, 'text': '$TUT_USER', 'cps': 40},
    {'do': 'type', 'target': SENHA_LOGIN, 'text': '$TUT_SENHA', 'cps': 40},
    {'do': 'click', 'target': BTN('Entrar')},
    {'do': 'waitFor', 'text': 'Olá, Rafael!', 'timeout': 40},
    AGUARDA,
]


def setup_config():
    return LOGIN + [{'do': 'goto', 'url': '/configuracoes'}, {'do': 'waitFor', 'text': 'Configurações do Sistema', 'timeout': 30}, AGUARDA]


# rolagem suave do contêiner que rola o alvo (molde do T14: ACHA_ROLAGEM + SUAVE); o cursor não se mexe
ACHA_ROLAGEM = ("const rolagem=(el)=>{let c=el&&el.parentElement;while(c&&c!==document.body){const s=getComputedStyle(c);"
                "if(/(auto|scroll)/.test(s.overflowY)&&c.scrollHeight>c.clientHeight+4)return c;c=c.parentElement;}"
                "const m=[...document.querySelectorAll('main')].find(e=>/(auto|scroll)/.test(getComputedStyle(e).overflowY)&&e.scrollHeight>e.clientHeight+4);"
                "return m||document.scrollingElement};")
SUAVE = ("await new Promise(res=>{const f=t=>{const p=Math.min(1,(t-t0)/DUR),e=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;c.scrollTo({top:DESTINO,behavior:'instant'});"
         "p<1?requestAnimationFrame(f):res()};requestAnimationFrame(f)});")


def js_ate(texto, y=250, dur_ms=1000, prefixo=False, escopo='body'):
    """rola até a folha do DOM cujo texto é `texto` ficar em y px CSS. Devolve o topo final, 'ok', 'SEM ALVO' ou 'SEM ROLAGEM'."""
    alvo = json.dumps(texto, ensure_ascii=False)
    busca = (f"[...document.querySelectorAll('{escopo} *')].filter(e=>e.textContent.trim().startsWith({alvo})&&e.offsetParent).sort((a,b)=>a.textContent.length-b.textContent.length)[0]"
             if prefixo else f"[...document.querySelectorAll('{escopo} *')].find(e=>e.children.length===0&&e.textContent.trim()==={alvo}&&e.offsetParent)")
    return ("(async()=>{" + ACHA_ROLAGEM + "const el=" + busca + ";if(!el)return 'SEM ALVO';const c=rolagem(el);if(!c)return 'SEM ROLAGEM';"
            f"const dy=Math.round(el.getBoundingClientRect().top-{int(y)});if(Math.abs(dy)<3)return 'ok';const y0=c.scrollTop,t0=performance.now();"
            + SUAVE.replace('DUR', str(int(dur_ms))).replace('DESTINO', 'y0+dy*e') +
            "return Math.round(el.getBoundingClientRect().top)})()")


def js_topo(dur_ms=800):
    return ("(async()=>{const c=document.scrollingElement;const y0=c.scrollTop,t0=performance.now();if(y0<3)return 'ok';"
            + SUAVE.replace('DUR', str(int(dur_ms))).replace('DESTINO', 'y0*(1-e)') + "return 'topo:'+Math.round(c.scrollTop)})()")


def js_centro(texto, prefixo=True):
    """(setup) põe o alvo no meio da tela, sem animação"""
    alvo = json.dumps(texto, ensure_ascii=False)
    return ("(()=>{const el=[...document.querySelectorAll('body *')].filter(e=>e.textContent.trim().startsWith(%s)&&e.offsetParent)"
            ".sort((a,b)=>a.textContent.length-b.textContent.length)[0];if(!el)return 'SEM ALVO';el.scrollIntoView({block:'center'});"
            "return Math.round(el.getBoundingClientRect().top)})()") % alvo


def rola_ate(c, texto, at, label, y=250, dur_ms=1000, prefixo=False, escopo='body'):
    return c.ev(js_ate(texto, y, dur_ms, prefixo, escopo), at=at, label=label)


# ---------------------------------------------------------------- alvos do cadastro e do login
CAD_EMPRESA, CAD_NOME, CAD_EMAIL, CAD_FONE = PH('Ex: Minha Empresa Ltda'), PH('Ex: João Silva'), PH('email@exemplo.com'), PH('(21) 98765-4321')
CAD_SENHA, CAD_CONFIRMA = PH('Mínimo 8 caracteres'), PH('Digite a senha novamente')
CAD_DADOS = [  # setup do cap02: a etapa "Dados" como no cap01, fora do vídeo
    {'do': 'goto', 'url': '/cadastro'}, {'do': 'waitFor', 'target': CAD_EMPRESA, 'timeout': 30},
    {'do': 'type', 'target': CAD_EMPRESA, 'text': 'Recicla Vale Metais', 'cps': 40},
    {'do': 'type', 'target': CAD_NOME, 'text': 'Rafael Nogueira', 'cps': 40},
    {'do': 'type', 'target': CAD_EMAIL, 'text': '$TUT_USER', 'cps': 40},
    {'do': 'type', 'target': CAD_FONE, 'text': '12900004410', 'cps': 40},
    {'do': 'click', 'target': BTNX('Continuar')},
    {'do': 'waitFor', 'text': 'Email de acesso:', 'timeout': 15}, AGUARDA,
]


# ================================================================ capítulos
def cap00():
    """Abertura: as duas primeiras linhas são ilustração (a janela fica parada); na L3 o cursor desce devagar pelo /cadastro."""
    c = Cap(0, pace=0.5, setup=[{'do': 'goto', 'url': '/cadastro'}, {'do': 'waitFor', 'target': CAD_EMPRESA, 'timeout': 30}, AGUARDA],
            prewarm=['/cadastro'], start=(1040, 300))
    c.mark(1)
    c.mark(2)
    c.mark(3)
    c.hover(TXT('Cadastro'), 0.8, at=c.A(3, 'Então', 0.5), label='título Cadastro')
    c.hover(TXTP('Teste grátis por 7 dias'), 1.0, at=c.A(3, 'criar', 0.7), label='Teste grátis por 7 dias · Sem compromisso · Acesso total')
    c.hover(TXT('Dados'), 0.5, at=c.A(3, 'entrar', 0.4), label='etapas Dados e Acesso')
    c.hover(CAD_EMPRESA, 1.2, at=c.A(3, 'preencher', 0.4), label='Nome da Empresa (o cursor desce pelo formulário)')
    c.hover(CAD_EMAIL, 0.6, at=c.A(3, 'Depois,', 0.5), label='Email')
    c.hover(CAD_FONE, 0.5, at=c.A(3, 'pedido,', 0.4), label='Telefone')
    c.hover(BTNX('Continuar'), 1.6, at=c.A(3, 'comprovante', 0.4, nth=0), label='Continuar (sem clicar)')
    c.mark(4)
    c.cursor((1060, 330), at=c.A(4, 'Se', 0.6), label='cursor sai do formulário (cartão Antes: Bem-vindo ao EcoSistema)')
    c.fim()
    return c


def cap01():
    """Criar a conta: as duas etapas e a barra, Dados (nome, e-mail, telefone), o link de indicação, Continuar, Acesso (senha com
    o indicador de força), o aviso dos termos e Criar Conta (toast; o capítulo corta no toast, antes do painel)."""
    c = Cap(1, pace=0.5, setup=[{'do': 'goto', 'url': '/cadastro'}, {'do': 'waitFor', 'target': CAD_EMPRESA, 'timeout': 30}, AGUARDA],
            prewarm=['/cadastro'], start=(1040, 300))
    c.mark(1)
    c.confere('body', ['Cadastro', 'Teste grátis por 7 dias · Sem compromisso · Acesso total', 'Dados', 'Acesso', 'Preenchimento obrigatório', '0%'],
              'etapas Dados e Acesso e a barra em 0%')
    c.hover(TXT('Dados'), 0.3, at=c.A(1, 'Dados', 0.6), label='etapa Dados')
    c.hover(TXT('Acesso'), 0.5, at=c.A(1, 'Acesso.', 0.5), label='etapa Acesso')
    c.hover(TXT('Preenchimento obrigatório'), 1.6, at=c.A(1, 'Preenchimento', 0.7), label='barra Preenchimento obrigatório em 0%')
    c.mark(2)
    c.click(CAD_EMPRESA, at=c.A(2, 'nome', 0.9), label='Nome da Empresa')
    c.type(CAD_EMPRESA, 'Recicla Vale Metais', at=c.A(2, 'Recicla', 0.1), cps=16, noClick=True, label='digita Recicla Vale Metais')
    c.click(CAD_NOME, at=c.A(2, 'nome', 0.8, nth=1), label='Seu Nome Completo')
    c.type(CAD_NOME, 'Rafael Nogueira', at=c.A(2, 'Rafael', 0.2), cps=16, noClick=True, label='digita Rafael Nogueira (a barra sobe)')
    c.mark(3)
    c.click(CAD_EMAIL, at=c.A(3, 'e-mail', 0.8), label='Email')
    c.type(CAD_EMAIL, '$TUT_USER', at=c.A(3, 'que', 0.1), cps=40, noClick=True, label='digita o e-mail do Rafael')
    c.click(CAD_FONE, at=c.A(3, 'telefone', 0.7), label='Telefone')
    c.type(CAD_FONE, '12900004410', at=c.A(3, 'arruma', 0.3), cps=12, noClick=True, label='digita o telefone (a máscara forma (12) 90000-4410)')
    c.confere_campos(['Recicla Vale Metais', 'Rafael Nogueira', 'rafael@reciclavalemetais.example', '(12) 90000-4410'], 'os quatro campos da etapa Dados', escopo='body')
    c.mark(4)
    c.hover(TXT('Recebeu um código de indicação?'), 2.2, at=c.A(4, 'código', 0.7), label='link Recebeu um código de indicação? (sem clicar)')
    c.mark(5)
    c.cursor((1120, 470), at=c.A(5, 'Repara', 0.4), label='a etapa Dados inteira (sem campo de CNPJ)')
    c.confere_ausente('body', 'CNPJ', 'nenhum campo de CNPJ no cadastro', espera=0.2)
    c.mark(6)
    c.click(BTNX('Continuar'), at=c.A(6, 'Continuar,', 0.8), label='Continuar')
    c.waitfor(text='Email de acesso:', timeout=12)
    c.mark(7)
    c.click(CAD_SENHA, at=c.A(7, 'senha', 0.8), label='Senha')
    c.type(CAD_SENHA, '$TUT_SENHA', at=c.A(7, 'oito', 0.4), cps=14, noClick=True, label='digita a senha (pontinhos; o indicador de força enche)')
    c.confere('body', ['Senha forte.'], 'indicador Senha forte')
    c.hover(TXTP('Senha forte.'), 1.2, at=c.A(7, 'indicador', 0.6), label='indicador de força: Senha forte')
    c.click(CAD_CONFIRMA, at=c.A(7, 'repito', 0.8), label='Confirmar Senha')
    c.type(CAD_CONFIRMA, '$TUT_SENHA', at=c.A(7, 'mesma', 0.2), cps=20, noClick=True, label='repete a senha')
    c.mark(8)
    c.rolar(380, at=c.A(8, 'Ao', 1.0), label='desce até o aviso dos termos', ponto=(640, 520))
    c.hover(TXTP('Ao criar sua conta, você concorda com os'), 1.0, at=c.A(8, 'concorda', 0.6), label='aviso Termos de Uso e Política de Privacidade')
    c.hover(BTN('Termos de Uso'), 0.6, at=c.A(8, 'Termos', 0.6), label='Termos de Uso (sem clicar)')
    c.hover(LINK('Política de Privacidade'), 1.2, at=c.A(8, 'Política', 0.6), label='Política de Privacidade (sem clicar)')
    c.mark(9)
    c.click(BTN('Criar Conta'), at=c.A(9, 'Criar', 0.8), label='Criar Conta')
    c.waitfor(text='Cadastro realizado com sucesso! Redirecionando...', timeout=12)
    c.registra(TXT('Cadastro realizado com sucesso! Redirecionando...'), label='toast Cadastro realizado com sucesso! Redirecionando...')
    c.fim()
    return c


def cap02():
    """Os 7 dias de teste: o cartão da etapa Acesso (o setup passa da etapa Dados fora do vídeo); L2 e L3 são ilustração; na L4 a
    página sobe ao subtítulo do teste grátis."""
    setup = CAD_DADOS + [{'do': 'eval', 'js': js_centro('Teste Grátis · Acesso Total')}, {'do': 'wait', 'seconds': 0.4}]
    c = Cap(2, pace=0.5, setup=setup, prewarm=['/cadastro'], start=(1060, 420))
    c.mark(1)
    c.confere('body', ['Teste Grátis · Acesso Total', '7 dias grátis', 'com acesso a todos os módulos', '5 usuários', 'inclusos durante o teste'],
              'cartão do teste grátis')
    c.hover(TXT('Teste Grátis · Acesso Total'), 0.6, at=c.A(1, 'cartão,', 0.7), label='cartão Teste Grátis · Acesso Total')
    c.hover(BTN('Criar Conta'), 0.6, at=c.A(1, 'Criar', 0.7), label='botão Criar Conta, logo abaixo')
    c.hover(TXTP('7 dias grátis'), 1.4, at=c.A(1, 'resume', 0.6), label='7 dias grátis e 5 usuários')
    c.mark(2)
    c.mark(3)
    c.mark(4)
    c.ev(js_topo(900), at=c.A(4, 'Uma', 0.9), label='a página sobe ao subtítulo')
    c.hover(TXTP('Teste grátis por 7 dias'), 3.0, at=c.A(4, 'link', 0.6), label='subtítulo Teste grátis por 7 dias · Sem compromisso · Acesso total')
    c.hover(TXTP('Teste grátis por 7 dias'), 1.6, at=c.A(4, 'escrito', 0.5), label='subtítulo: o que vale é o que está escrito aqui')
    c.fim()
    return c


def cap03():
    """Entrar no sistema: /login sem sessão, e-mail, senha, Lembrar de mim, Entrar com Google (sem clicar), Entrar; o card da conta,
    o menu e o trocador de contas (que guarda a sessão que o login pela tela acabou de salvar). L8 é ilustração."""
    c = Cap(3, pace=0.5, setup=[{'do': 'goto', 'url': '/login'}, {'do': 'waitFor', 'target': EMAIL_LOGIN, 'timeout': 30}, AGUARDA],
            prewarm=['/login'], start=(300, 560))
    c.mark(1)
    c.confere('body', ['Acesse sua conta', 'Entre para continuar no EcoSistema.'], 'tela de login')
    c.hover(TXT('Acesse sua conta'), 0.8, at=c.A(1, 'entrar.', 0.6), label='Acesse sua conta')
    c.click(EMAIL_LOGIN, at=c.A(1, 'todo', 0.8), label='E-mail')
    c.mark(2)
    c.type(EMAIL_LOGIN, '$TUT_USER', at=c.A(2, 'Aqui', 0.9), cps=40, noClick=True, label='digita o e-mail do Rafael')
    c.click(SENHA_LOGIN, at=c.A(2, 'cadastro.', 0.6), label='Senha')
    c.type(SENHA_LOGIN, '$TUT_SENHA', at=c.A(2, 'Marcando', 0.6), cps=40, noClick=True, label='digita a senha (pontinhos)')
    c.click(CHK('Lembrar de mim'), at=c.A(2, 'Lembrar', 0.5), label='marca Lembrar de mim')
    c.mark(3)
    c.hover(BTNX('Entrar com Google'), 2.4, at=c.A(3, 'Google,', 0.7), label='Entrar com Google (sem clicar)')
    c.hover(BTNX('Entrar com Google'), 1.6, at=c.A(3, 'existe', 0.5), label='Entrar com Google: entra na conta que já existe')
    c.hover(LINK('Cadastre-se'), 1.0, at=c.A(3, 'Cadastre-se.', 0.6), label='Cadastre-se')
    c.mark(4)
    c.click(BTN('Entrar'), at=c.A(4, 'Entrar,', 0.8), label='Entrar')
    c.waitfor(text='Olá, Rafael!', timeout=20)
    c.mark(5)
    c.hover(CARD_CONTA, 2.6, at=c.A(5, 'card', 0.6), label='card da conta: Rafael Nogueira e Recicla Vale Metais', noScroll=True)
    c.mark(6)
    c.click(CARD_CONTA, at=c.A(6, 'Clicando', 0.5), label='abre o menu da conta', noScroll=True)
    c.waitfor(target={'role': 'menuitem', 'name': 'Meu Perfil'}, timeout=8)
    c.hover({'role': 'menuitem', 'name': 'Meu Perfil'}, 1.2, at=c.A(6, 'Perfil', 0.6), label='Meu Perfil')
    c.mark(7)
    c.click(SEL("[aria-label='Trocar de conta']", nth=0), at=c.A(7, 'trocador', 0.7), label='trocador de contas (o card cresce)')
    c.waitfor(text='Adicionar conta', timeout=8)
    c.confere('body', ['Apenas essa conta está salva.', 'Adicionar conta', 'Sair de todas as contas'], 'trocador aberto com a conta ativa')
    c.hover(TXTP('Apenas essa conta está salva'), 1.4, at=c.A(7, 'guarda', 0.6), label='Apenas essa conta está salva')
    c.mark(8)
    c.mark(9)
    c.hover(TXT('Adicionar conta'), 2.4, at=c.A(9, 'Adicionar', 0.7), label='Adicionar conta (sem clicar)')
    c.hover(TXT('Adicionar conta'), 1.2, at=c.A(9, 'Cabem', 0.5), label='Adicionar conta: até cinco contas')
    c.press('Escape', at=c.A(9, 'contas.', -0.3), label='Esc fecha o menu')
    c.fim()
    return c


OTP = SEL("input[autocomplete='one-time-code']")


# Navegador que o Rafael já usou (o app grava este instantâneo em toda sessão): sem ele, o login que o código do e-mail faz no meio do
# "Esqueci minha senha" troca a tela inteira por "Carregando empresa..." (EntityTerminologyContext.tsx:141-148), o login é remontado
# e o app entra no sistema SEM pedir a senha nova (achado do app, propostas_fala.md). Com ele, o fluxo segue como foi feito.
SNAPSHOT_TERMOS = {'entity_terminology_snapshot': json.dumps({'userId': RAFAEL, 'companyId': EMPRESA_ID, 'inverted': False, 'at': 1794247200000})}


def cap04():
    """Esqueci minha senha: /login sem sessão, o e-mail, Enviar Código, as seis casas (L4 é ilustração), o código 481207, a caixa
    laranja e o reenvio, Verificar e a senha nova."""
    c = Cap(4, pace=0.5, setup=[{'do': 'goto', 'url': '/login'}, {'do': 'waitFor', 'target': EMAIL_LOGIN, 'timeout': 30}, AGUARDA],
            prewarm=['/login'], start=(300, 560), storage=SNAPSHOT_TERMOS)
    c.mark(1)
    c.hover(TXT('Acesse sua conta'), 0.8, at=c.A(1, 'esquecer', 0.6), label='tela de login')
    c.click(BTN('Esqueci minha senha'), at=c.A(1, 'Esqueci', 0.8), label='Esqueci minha senha')
    c.waitfor(text='Recuperar Senha', timeout=8)
    c.mark(2)
    c.click(SEL('input[type=email]'), at=c.A(2, 'Digito', 0.8), label='E-mail')
    c.type(SEL('input[type=email]'), '$TUT_USER', at=c.A(2, 'e-mail', 0.4), cps=40, noClick=True, label='digita o e-mail da conta')
    c.click(BTN('Enviar Código'), at=c.A(2, 'Enviar', 0.5), label='Enviar Código')
    c.waitfor(text='Verificar Código', timeout=10)
    c.mark(3)
    c.confere('body', ['Se o email existir no sistema, um código será enviado.', 'Digite o código de 6 dígitos enviado para', 'rafael@reciclavalemetais.example'],
              'toast e o passo Verificar Código')
    c.hover(TXTP('Digite o código de 6 dígitos'), 1.0, at=c.A(3, 'código', 0.6), label='Digite o código de 6 dígitos enviado para o e-mail')
    c.hover(OTP, 1.4, at=c.A(3, 'seis', 0.6), label='as seis casas do código')
    c.mark(4)
    c.mark(5)
    c.click(OTP, at=c.A(5, 'Uma', 0.8), label='primeira casa do código')
    c.type(OTP, '481207', at=c.A(5, 'dica:', 0.2), cps=10, noClick=True, label='digita 481207 nas seis casas')
    c.hover(TXTP('Não recebeu? Confira também a pasta de'), 2.0, at=c.A(5, 'confere', 0.6), label='caixa laranja Não recebeu? Confira a pasta de Spam')
    c.hover(TXTP('Reenviar código em'), 2.0, at=c.A(5, 'minuto,', 0.6), label='Reenviar código em ...s')
    c.mark(6)
    c.click(BTN('Verificar'), at=c.A(6, 'Verificar.', 0.8), label='Verificar')
    c.waitfor(text='Nova Senha', timeout=10)
    c.mark(7)
    # o campo Nova Senha já vem com o foco (autoFocus): digita sem clicar, ainda no fim da L6
    c.type(SEL('input[type=password]', nth=0), '$TUT_SENHA', at=c.A(6, 'nova.', 0.0), cps=40, noClick=True, label='digita a nova senha (Nova Senha)')
    c.click(SEL('input[type=password]', nth=1), at=c.A(7, 'duas', 0.5), label='Confirmar Nova Senha')
    c.type(SEL('input[type=password]', nth=1), '$TUT_SENHA', at=c.A(7, 'vezes', 0.0), cps=40, noClick=True, label='repete a nova senha')
    c.click(BTN('Alterar Senha e Entrar'), at=c.A(7, 'Alterar', 0.1), label='Alterar Senha e Entrar')
    c.waitfor(text='Senha alterada com sucesso! Você já está logado.', timeout=12)
    c.registra(TXT('Senha alterada com sucesso! Você já está logado.'), label='toast Senha alterada com sucesso! Você já está logado.')
    c.fim()
    return c


# ---------------------------------------------------------------- Configurações › Empresa (o <main> de dentro é quem rola)
CONFIG_RODAPE = SEL("button[aria-label='Configurações']")       # botão do rodapé do menu (o do painel não tem aria-label)
ABA = lambda id_: SEL(f'#tab-btn-{id_}')
LOGO_IMG, ICONE_IMG = SEL("main img[alt='Logo']"), SEL("main img[alt='Ícone']")
COMBO_ROTULO = lambda rotulo: SEL(f'main div:has(> label:text-is("{rotulo}")) button[role=combobox]')
PREVIA = SEL('main p.font-mono')
OPC = lambda n: {'role': 'option', 'name': n, 'exact': True}


def cap05():
    """Logo, ícone, nome e CNPJ: do painel ao botão Configurações do rodapé do menu, o passeio pelas abas, o logo e o ícone (upload),
    o White Label recolhido (só menção), o nome com "Exibir nos documentos" e o CNPJ (salva sozinho). Vira apos-cap05."""
    c = Cap(5, pace=0.5, setup=LOGIN, start=(720, 150))   # fora dos gráficos do painel (a dica do gráfico abriria sozinha)
    c.mark(1)
    c.hover(CONFIG_RODAPE, 1.0, at=c.A(1, 'Configurações,', 0.7), label='botão Configurações no rodapé do menu', noScroll=True)
    c.hover(CARD_CONTA, 0.5, at=c.A(1, 'abaixo', 0.6), label='card com o seu nome, logo acima', noScroll=True)
    c.click(CONFIG_RODAPE, at=c.A(1, 'card', 0.4), label='Configurações (rodapé do menu)', noScroll=True)
    c.waitfor(text='Configurações do Sistema', timeout=15)
    c.mark(2)
    c.hover(ABA('company'), 0.6, at=c.A(2, 'abas.', 0.7), label='abas das Configurações')
    c.hover(ABA('company'), 0.3, at=c.A(2, 'Empresa,', 0.6), label='aba Empresa')
    c.hover(ABA('usability'), 0.4, at=c.A(2, 'Usabilidade,', 0.6), label='aba Usabilidade')
    c.hover(ABA('condicoes-pagamento'), 0.8, at=c.A(2, 'Condições', 0.6), label='aba Condições de Pagamento')
    c.hover(ABA('appearance'), 0.3, at=c.A(2, 'Aparência', 0.6), label='aba Aparência')
    c.hover(SEL('#tab-btn-shortcuts svg'), 0.3, at=c.A(2, 'Atalhos.', 0.6), label='aba Atalhos (na borda da faixa)', noScroll=True)
    c.hover(ABA('users'), 1.6, at=c.A(2, 'Usuários', 0.5), label='aba Usuários e Permissões (próximo tutorial)')
    c.mark(3)
    c.hover(TXT('Identidade Visual'), 1.0, at=c.A(3, 'Identidade', 0.6), label='Identidade Visual')
    c.upload(TXT('Nenhum logo enviado'), 'assets/recicla-vale-logo.png', at=c.A(3, 'Clico', 0.7), label='escolhe o logo recicla-vale-logo.png')
    c.waitfor(text='Logo atualizado com sucesso!', timeout=10)
    c.hover(LOGO_IMG, 1.4, at=c.A(3, 'comprovantes', 0.6), label='o logo da Recicla Vale na tela')
    c.mark(4)
    c.upload(TXT('1:1'), 'assets/recicla-vale-icone.png', at=c.A(4, 'ícone', 0.8), label='escolhe o ícone recicla-vale-icone.png')
    c.waitfor(text='Ícone atualizado com sucesso!', timeout=10)
    c.ev("JSON.stringify([...document.querySelectorAll('main img')].map(i=>[i.alt,i.naturalWidth]))", label='confere logo e ícone carregados (largura > 0)')
    c.hover(TXTP('Usado no menu lateral quando recolhido'), 1.8, at=c.A(4, 'menu', 0.6), label='Usado no menu lateral quando recolhido (White Label)')
    c.mark(5)
    c.hover(BTNX('White Label'), 2.6, at=c.A(5, 'White', 0.6), label='cartão White Label (recolhido, sem abrir)')
    c.hover(BTNX('White Label'), 2.4, at=c.A(5, 'depende', 0.5), label='White Label: depende do plano contratado')
    c.mark(6)
    rola_ate(c, 'Nome da Empresa', at=c.A(6, 'O', 0.9), label='desce até o nome e o CNPJ', y=330, dur_ms=700, escopo='main')
    c.hover(SEL('#company-name'), 1.2, at=c.A(6, 'nome', 0.5), label='Nome da Empresa: Recicla Vale Metais')
    c.hover(SEL('#show-name'), 2.8, at=c.A(6, 'chave', 0.6), label='chave Exibir nos documentos (ligada)')
    c.mark(7)
    c.click(SEL('#company-cnpj'), at=c.A(7, 'CNPJ.', 0.8), label='CNPJ/CPF')
    c.type(SEL('#company-cnpj'), '47318506000107', at=c.A(7, 'dica:', 0.0), cps=10, noClick=True, label='digita o CNPJ: 47.318.506/0001-07')
    c.confere_campos(['47.318.506/0001-07'], 'máscara do CNPJ')
    c.hover(SEL('#company-cnpj'), 1.8, at=c.A(7, 'confere', 0.6), label='CNPJ conferido número por número')
    c.mark(8)
    c.mark(9)
    rola_ate(c, 'Salvar alterações', at=c.A(9, 'Não', 0.9), label='desce ao rodapé do cartão Empresa', y=560, dur_ms=1400, prefixo=True, escopo='main')
    c.hover(BTN('Salvar alterações'), 2.2, at=c.A(9, 'Salvar', 0.6), label='botão Salvar alterações (sem clicar)')
    c.fim()
    return c


def cap06():
    """Contato e endereço: o e-mail de contato no lugar do do Rafael, as chaves Exibir nos documentos, o CEP que acha o endereço,
    número e complemento, a nota da nota fiscal, a Prévia no comprovante e o Complemento desmarcado. Vira apos-cap06."""
    c = Cap(6, pace=0.5, setup=setup_config(), start=(760, 420))
    c.mark(1)
    rola_ate(c, 'Informações de Contato', at=0.3, label='desce até Informações de Contato', y=140, dur_ms=1000, escopo='main')
    c.hover(SEL('#company-phone'), 0.6, at=c.A(1, 'telefone', 0.6), label='Telefone (12) 90000-4410')
    c.hover(SEL('#company-email'), 1.2, at=c.A(1, 'e-mail', 0.6), label='E-mail do cadastro')
    c.mark(2)
    c.hover(SEL('#company-email'), 1.4, at=c.A(2, 'e-mail', 0.6), label='o e-mail do cadastro é o do Rafael')
    c.click(SEL('#company-email'), at=c.A(2, 'comprovante,', 0.7), label='E-mail')
    c.type(SEL('#company-email'), 'contato@reciclavalemetais.example', at=c.A(2, 'comprovante,', -0.3), cps=40, noClick=True, clear=True,
           label='apaga e digita contato@reciclavalemetais.example')
    c.confere_campos(['contato@reciclavalemetais.example'], 'e-mail de contato')
    c.mark(3)
    c.hover(SEL('#show-phone'), 0.4, at=c.A(3, 'chave', 0.6), label='chave Exibir nos documentos do Telefone')
    c.hover(SEL('#show-email'), 1.0, at=c.A(3, 'documentos.', 0.6), label='chave Exibir nos documentos do E-mail')
    c.mark(4)
    c.mark(5)
    rola_ate(c, 'Endereço', at=c.A(5, 'No', 0.9), label='desce até o Endereço', y=120, dur_ms=900, escopo='main')
    c.click(PH('00000-000', exact=True), at=c.A(5, 'digitar', 0.8), label='CEP')
    c.type(PH('00000-000', exact=True), '12086410', at=c.A(5, 'CEP.', 0.1), cps=10, noClick=True, label='digita o CEP 12086-410')
    c.waitfor(text='Endereço encontrado!', timeout=8)
    c.confere_campos(['12086-410', 'Rua das Oficinas', 'Parque Industrial'], 'endereço achado pelo CEP')
    c.confere('main', ['SP - São Paulo', 'Taubaté'], 'Estado e Cidade')
    c.hover(PH('Rua, Avenida, etc.'), 0.3, at=c.A(5, 'rua,', 0.5), label='Logradouro: Rua das Oficinas')
    c.hover(PH('Bairro', exact=True), 0.4, at=c.A(5, 'bairro,', 0.5), label='Bairro: Parque Industrial')
    c.hover(COMBO_ROTULO('Cidade'), 0.3, at=c.A(5, 'cidade', 0.5), label='Cidade: Taubaté')
    c.hover(COMBO_ROTULO('Estado'), 0.6, at=c.A(5, 'estado', 0.5), label='Estado: SP - São Paulo')
    c.mark(6)
    c.click(PH('Nº', exact=True), at=c.A(6, 'número,', 0.8), label='Número')
    c.type(PH('Nº', exact=True), '1250', at=c.A(6, 'mil', 0.1), cps=8, noClick=True, label='digita 1250')
    c.click(PH('Sala, Galpão, etc. (opcional)'), at=c.A(6, 'complemento:', 0.8), label='Complemento')
    c.type(PH('Sala, Galpão, etc. (opcional)'), 'Galpão 2', at=c.A(6, 'galpão', 0.1), cps=10, noClick=True, label='digita Galpão 2')
    c.mark(7)
    c.hover(TXTP('É este endereço que sai na nota fiscal.'), 3.4, at=c.A(7, 'aviso:', 0.6), label='nota: é este endereço que sai na nota fiscal')
    c.hover(TXTP('É este endereço que sai na nota fiscal.'), 2.4, at=c.A(7, 'Configuração', 0.5), label='nota: a Configuração Fiscal usa o que estiver aqui')
    c.mark(8)
    rola_ate(c, 'Prévia no comprovante', at=c.A(8, 'Mais', 0.9), label='desce até a Prévia no comprovante', y=210, dur_ms=900, escopo='main')
    c.confere('main', ['Rua das Oficinas, 1250 - Galpão 2 - Parque Industrial - Taubaté/SP - CEP: 12086-410'], 'prévia com o galpão')
    c.hover(PREVIA, 3.0, at=c.A(8, 'Prévia', 0.6), label='Prévia no comprovante: o endereço como sai impresso')
    c.mark(9)
    c.hover(CHK('Logradouro'), 0.5, at=c.A(9, 'escolher', 0.6), label='caixas da prévia, pedaço por pedaço')
    c.hover(CHK('CEP'), 0.5, at=c.A(9, 'pedaço.', 0.5), label='caixa CEP')
    c.click(CHK('Complemento'), at=c.A(9, 'desmarco', 0.8), label='desmarca o Complemento')
    c.confere('main', ['Rua das Oficinas, 1250 - Parque Industrial - Taubaté/SP - CEP: 12086-410'], 'prévia sem o galpão')
    c.hover(PREVIA, 1.4, at=c.A(9, 'some', 0.6), label='a prévia sem o galpão')
    c.fim()
    return c


def cap07():
    """Numeração de pedidos: o reinício (abre a lista e fica em Nenhum), os modelos (Barras, Zeros e volta ao Padrão) e a numeração
    separada (a janela de confirmação, Cancelar). L3 e L8 são ilustração. Nada muda no fim (o modelo volta ao Padrão)."""
    c = Cap(7, pace=0.5, setup=setup_config(), start=(760, 420))
    c.mark(1)
    rola_ate(c, 'Numeração de pedidos', at=0.4, label='desce até Numeração de pedidos', y=120, dur_ms=1200, escopo='main')
    c.hover(TXT('Numeração de pedidos'), 1.2, at=c.A(1, 'Numeração', 0.6), label='Numeração de pedidos')
    c.hover(SEL('#order-number-template'), 1.6, at=c.A(1, 'escolhe', 0.6), label='o formato do número')
    c.mark(2)
    c.click(SEL('#order-number-reset'), at=c.A(2, 'Reinício', 0.8), label='Reinício da numeração (abre a lista)')
    c.waitfor(target=OPC('Nenhum (segue direto)'), timeout=6)
    c.hover(OPC('Nenhum (segue direto)'), 1.6, at=c.A(2, 'Nenhum,', 0.6), label='Nenhum (segue direto)', noScroll=True)
    c.hover(OPC('Mensal (zera todo mês)'), 1.6, at=c.A(2, 'Mensal,', 0.6), label='Mensal (zera todo mês)', noScroll=True)
    c.hover(OPC('Anual (zera todo ano)'), 0.4, at=c.A(2, 'Anual,', 0.6), label='Anual (zera todo ano)', noScroll=True)
    c.click(OPC('Nenhum (segue direto)'), at=c.A(2, 'ano.', 0.2), label='fica em Nenhum (segue direto)', noScroll=True)
    c.waitfor(gone=OPC('Anual (zera todo ano)'), timeout=6)
    c.mark(3)
    c.mark(4)
    c.hover(TXT('Formato do número'), 0.8, at=c.A(4, 'Formato', 0.6), label='Formato do número')
    c.hover(BTNX('Padrão'), 0.4, at=c.A(4, 'modelo', 0.6), label='modelo Padrão #30')
    c.hover(BTNX('Pontos'), 0.5, at=c.A(4, 'exemplo', 0.6), label='os modelos, cada um com o exemplo')
    c.mark(5)
    c.click(BTNX('Barras'), at=c.A(5, 'Barras,', 0.8), label='modelo Barras')
    c.confere('main', ['Exemplo: 30/11/26'], 'exemplo do Barras')
    c.registra(SEL("main span:text-is('Exemplo:') >> xpath=.."), label='Exemplo: 30/11/26')
    c.mark(6)
    c.click(BTNX('Zeros'), at=c.A(6, 'Zeros,', 0.8), label='modelo Zeros')
    c.confere('main', ['Exemplo: 0030'], 'exemplo do Zeros')
    c.click(BTNX('Padrão'), at=c.A(6, 'Padrão,', 0.8), label='volta ao Padrão')
    c.confere('main', ['Exemplo: #30'], 'de volta ao Padrão')
    c.confere_campos(['#{NUM}'], 'formato #{NUM}')
    c.mark(7)
    c.hover(TXT('Numeração separada para compras e vendas'), 1.6, at=c.A(7, 'Numeração', 0.6), label='Numeração separada para compras e vendas (desligada)')
    c.hover(TXT('Cada tipo passa a ter sua própria contagem.'), 2.0, at=c.A(7, 'Ligando,', 0.6), label='Cada tipo passa a ter sua própria contagem.')
    c.mark(8)
    c.mark(9)
    c.click(SEL('#order-number-scope'), at=c.A(9, 'ligar,', 0.8), label='chave Numeração separada (pede confirmação)')
    c.waitfor(text='Ativar numeração separada?', timeout=8)
    c.hover(TXTP('Compras e vendas passarão a contar separadamente'), 2.6, at=c.A(9, 'números', 0.6), label='janela Ativar numeração separada?')
    c.hover(TXTP('Compras e vendas passarão a contar separadamente'), 1.4, at=c.A(9, 'pedidos', 0.5), label='Os pedidos que você já fez não mudam')
    c.click(BTN('Cancelar'), at=c.A(9, 'Cancelar.', 0.8), label='Cancelar (a chave fica desligada)')
    c.waitfor(gone=TXT('Ativar numeração separada?'), timeout=8)
    c.ev("(()=>{const s=document.querySelector('#order-number-scope');return s?s.getAttribute('data-state'):'sem chave'})()", label='confere chave desligada (unchecked)')
    c.fim()
    return c


FRASE = 'Obrigado pela parceria! Atendemos de segunda a sexta, das 7h às 17h.'   # 68 caracteres (junção: sem sábado)


def cap08():
    """A frase do comprovante: liga No comprovante, digita a frase (68 caracteres), o contador, Alinhar à esquerda (desligada) e
    Salvar alterações. L5 é ilustração. Vira apos-cap08."""
    c = Cap(8, pace=0.5, setup=setup_config(), start=(760, 420))
    c.mark(1)
    rola_ate(c, 'Comprovantes e Documentos', at=0.4, label='desce até Comprovantes e Documentos', y=120, dur_ms=1300, escopo='main')
    c.hover(TXT('Comprovantes e Documentos'), 1.0, at=c.A(1, 'Comprovantes', 0.6), label='Comprovantes e Documentos')
    c.hover(TXT('Frase Personalizada'), 1.0, at=c.A(1, 'frase', 0.6, nth=1), label='Frase Personalizada')
    c.mark(2)
    c.click(SEL('#show-phrase'), at=c.A(2, 'ligo', 0.8), label='liga a chave No comprovante')
    c.click(SEL('#receipt-phrase'), at=c.A(2, 'papel.', 0.3), label='caixa da frase')
    c.mark(3)
    c.type(SEL('#receipt-phrase'), FRASE, at=c.A(3, 'A', 0.0), cps=40, noClick=True, label='digita a frase do comprovante')
    c.confere('main', ['68/2000 caracteres'], 'contador 68/2000')
    c.hover(TXTP('/2000 caracteres'), 0.8, at=c.A(3, 'foram.', 0.3), label='contador 68/2000 caracteres')
    c.mark(4)
    c.hover(TXT('Alinhar à esquerda'), 2.6, at=c.A(4, 'Alinhar', 0.6), label='Alinhar à esquerda (desligada)')
    c.hover(SEL('#phrase-align-left'), 1.0, at=c.A(4, 'curta,', 0.6), label='chave Alinhar à esquerda: fica no centro')
    c.mark(5)
    c.mark(6)
    c.click(BTN('Salvar alterações'), at=c.A(6, 'Salvar', 0.8), label='Salvar alterações')
    c.waitfor(text='Configurações salvas', timeout=10)
    c.registra(TXT('Configurações salvas'), label='toast Configurações salvas')
    c.fim()
    return c


# ---------------------------------------------------------------- Usabilidade (linha = div com label, ajuda (svg) e chave)
AJUDA = lambda rotulo: SEL(f'main div:has(> label:text-is("{rotulo}")) > svg')                       # ícone (?) ao lado do rótulo
CHAVE = lambda rotulo: SEL(f'main div:has(> div > div > label:text-is("{rotulo}")) > button[role=switch]')   # chave da linha
CHAVE_SUB = lambda rotulo: SEL(f'main div:has(> label:text-is("{rotulo}")) > button[role=switch]')          # Na Venda / Na Compra
COMBO_LINHA = lambda texto: SEL(f'main div:has(> span:text-is("{texto}")) button[role=combobox]')           # Computador / Celular/Tablet


def cap09():
    """O jeito do pátio (aba Usabilidade, nada muda): nomenclatura (inverter os termos), Multi-Caixas, cofre, Formato do Comprovante
    (abre e fica no Térmico), Forma de Pagamento Padrão (abre e fica em Perguntar sempre), Arredondar, Impureza/Tara (com a dica),
    Lucro no Comprovante, as opções gravadas no usuário e Exigir cliente/fornecedor no ticket. L11, L13 a L15 são ilustração."""
    c = Cap(9, pace=0.5, setup=setup_config(), start=(760, 420))
    c.mark(1)
    c.click(ABA('usability'), at=c.A(1, 'Usabilidade.', 0.8), label='aba Usabilidade')
    c.waitfor(text='Configure preferências gerais de usabilidade do sistema', timeout=10)
    c.hover(TXT('Configure preferências gerais de usabilidade do sistema'), 1.6, at=c.A(1, 'ajusta', 0.6), label='Usabilidade: preferências gerais do sistema')
    c.mark(2)
    c.hover(TXT('Nomenclatura de clientes e fornecedores'), 1.8, at=c.A(2, 'Nomenclatura', 0.6), label='Nomenclatura de clientes e fornecedores')
    c.hover(SEL('#invert-customer-supplier-terms'), 2.2, at=c.A(2, 'Inverter', 0.6), label='chave Inverter os termos Cliente e Fornecedor (desligada, sem clicar)')
    c.hover(TXT('Inverter os termos Cliente e Fornecedor'), 1.0, at=c.A(2, 'troca', 0.5), label='troca as palavras na tela')
    c.mark(3)
    c.hover(TXTP('continuam com a mesma lógica'), 4.0, at=c.A(3, 'Muda', 0.6), label='descrição: compras, vendas, vínculos, saldos e documentos fiscais continuam iguais')
    c.mark(4)
    rola_ate(c, 'Caixa', at=c.A(4, 'Na', 0.9), label='desce até a seção Caixa', y=120, dur_ms=900, prefixo=True, escopo='main')
    c.hover(TXT('Multi-Caixas'), 1.6, at=c.A(4, 'Multi-Caixas.', 0.6), label='Multi-Caixas (ligado)')
    c.hover(TXTP('Cada operador abre e gerencia seu próprio caixa'), 3.4, at=c.A(4, 'Ligado,', 0.5), label='Multi-Caixas: cada operador, o próprio caixa')
    c.hover(CHAVE('Multi-Caixas'), 1.0, at=c.A(4, 'Aqui', 0.6), label='chave Multi-Caixas ligada')
    c.mark(5)
    c.hover(TXT('Rastreabilidade do dinheiro físico (Cofre)'), 2.4, at=c.A(5, 'cofre,', 0.6), label='Rastreabilidade do dinheiro físico (Cofre), ligada')
    c.mark(6)
    c.hover(TXT('Formato do Comprovante'), 0.8, at=c.A(6, 'Formato', 0.6), label='Formato do Comprovante')
    c.click(COMBO_LINHA('Computador'), at=c.A(6, 'papel:', 0.8), label='abre o formato do Computador')
    c.waitfor(target=OPC('A4 (PDF em folha)'), timeout=6)
    c.hover(OPC('Térmico (58/80mm)'), 1.6, at=c.A(6, 'Térmico,', 0.6), label='Térmico (58/80mm)', noScroll=True)
    c.hover(OPC('A4 (PDF em folha)'), 2.0, at=c.A(6, 'A4,', 0.6), label='A4 (PDF em folha)', noScroll=True)
    c.click(OPC('Térmico (58/80mm)'), at=c.A(6, 'comum.', 0.5), label='fica no Térmico (58/80mm)', noScroll=True)
    c.waitfor(gone=OPC('A4 (PDF em folha)'), timeout=6)
    c.mark(7)
    c.hover(COMBO_LINHA('Computador'), 0.6, at=c.A(7, 'computador', 0.6), label='Computador: Térmico')
    c.hover(COMBO_LINHA('Celular/Tablet'), 1.0, at=c.A(7, 'celular,', 0.6), label='Celular/Tablet: Térmico')
    c.hover(TXTP('(preferência por usuário)'), 1.2, at=c.A(7, 'pessoa', 0.6), label='(preferência por usuário)')
    c.mark(8)
    c.hover(TXT('Pedidos e Pagamentos'), 0.8, at=c.A(8, 'Pedidos', 0.6), label='Pedidos e Pagamentos')
    c.hover(TXT('Forma de Pagamento Padrão'), 1.6, at=c.A(8, 'Forma', 0.6), label='Forma de Pagamento Padrão')
    c.click(SEL('#default-payment'), at=c.A(8, 'finaliza', 0.8), label='abre a Forma de Pagamento Padrão')
    c.waitfor(target=OPC('Dinheiro'), timeout=6)
    c.hover(OPC('Dinheiro'), 0.4, at=c.A(8, 'Dinheiro,', 0.5), label='Dinheiro', noScroll=True)
    c.hover(OPC('Pix/Transferência'), 1.0, at=c.A(8, 'Pix', 0.5), label='Pix/Transferência', noScroll=True)
    c.hover(OPC('Perguntar sempre'), 0.6, at=c.A(8, 'Perguntar', 0.5), label='Perguntar sempre', noScroll=True)
    c.mark(9)
    c.click(OPC('Perguntar sempre'), at=c.A(9, 'Perguntar', 0.6), label='fica em Perguntar sempre', noScroll=True)
    c.waitfor(gone=OPC('Dinheiro'), timeout=6)
    c.hover(SEL('#default-payment'), 1.6, at=c.A(9, 'fornecedor', 0.6), label='Perguntar sempre: cada fornecedor recebe de um jeito')
    c.mark(10)
    rola_ate(c, 'Arredondar Pagamentos', at=c.A(10, 'O', 1.0), label='desce até Arredondar Pagamentos', y=300, dur_ms=600, escopo='main')
    c.hover(AJUDA('Arredondar Pagamentos'), 2.0, at=c.A(10, 'Arredondar', 0.5), label='Arredondar Pagamentos: a dica aparece')
    c.hover(CHAVE_SUB('Na Venda'), 0.4, at=c.A(10, 'Venda', 0.6), label='Na Venda (desligada)')
    c.hover(CHAVE_SUB('Na Compra'), 0.8, at=c.A(10, 'Compra.', 0.5), label='Na Compra (desligada)')
    c.mark(11)
    c.mark(12)
    c.hover(TXT('Impureza/Tara Desconta no Valor'), 1.6, at=c.A(12, 'Impureza', 0.6), label='Impureza/Tara Desconta no Valor (ligada)')
    c.hover(AJUDA('Impureza/Tara Desconta no Valor'), 3.4, at=c.A(12, 'sujeira', 0.6), label='Impureza/Tara: a dica (Ex: compra de 100kg com 5kg de impureza)')
    c.hover(CHAVE('Impureza/Tara Desconta no Valor'), 1.6, at=c.A(12, 'material,', 0.6), label='chave Impureza/Tara ligada')
    c.mark(13)
    c.mark(14)
    c.mark(15)
    c.mark(16)
    c.hover(TXT('Lucro no Comprovante'), 1.6, at=c.A(16, 'Lucro', 0.6), label='Lucro no Comprovante (desligado)')
    c.hover(TXTP('Exibe o lucro estimado no PDF do comprovante de venda'), 2.0, at=c.A(16, 'estimado', 0.6), label='Exibe o lucro estimado no comprovante de venda')
    c.hover(AJUDA('Lucro no Comprovante'), 1.4, at=c.A(16, 'permissão', 0.6), label='Lucro no Comprovante: só para quem vê a projeção de lucro')
    c.mark(17)
    rola_ate(c, 'Forma de Pagamento Padrão', at=c.A(17, 'Repara:', 0.9), label='as opções de pedido, de Forma de Pagamento Padrão a Lucro no Comprovante', y=120, dur_ms=900, escopo='main')
    c.hover(CARD_CONTA, 1.2, at=c.A(17, 'Rafael.', 0.6), label='aqui o Rafael (o card da conta)', noScroll=True)
    c.mark(18)
    rola_ate(c, 'Exigir cliente/fornecedor no Ticket de Pesagem', at=c.A(18, 'Por', 0.9), label='desce até Exigir cliente/fornecedor no Ticket de Pesagem', y=300, dur_ms=1100, escopo='main')
    c.hover(TXT('Exigir cliente/fornecedor no Ticket de Pesagem'), 2.0, at=c.A(18, 'Exigir', 0.6), label='Exigir cliente/fornecedor no Ticket de Pesagem (desligado)')
    c.hover(TXTP('Quando ligado, o funcionário não consegue salvar um ticket'), 3.0, at=c.A(18, 'Ligado,', 0.6), label='Quando ligado, ninguém salva um ticket sem escolher com quem foi')
    c.hover(CHAVE('Exigir cliente/fornecedor no Ticket de Pesagem'), 1.2, at=c.A(18, 'Esse', 0.6), label='chave Exigir cliente/fornecedor (vale pra empresa toda)')
    c.ev("JSON.stringify([...document.querySelectorAll('main button[role=switch]')].map(s=>s.getAttribute('data-state')[0]).join(''))", label='estado das chaves da Usabilidade (nada mudou)')
    c.fim()
    return c


DIAS = lambda i: SEL(f'{DLG} input[inputmode=numeric]', nth=i)
PCT = lambda i: SEL(f'{DLG} input[inputmode=decimal]', nth=i)


def cap10():
    """Condições de pagamento: a aba vazia, Nova condição, o nome 30/60/90 dias, Definir como condição padrão, desmarca À vista,
    as três parcelas (30/60/90 e 33,33 + 33,33 + 33,34), a Soma dos percentuais 100% e Criar condição. L2 é ilustração. Vira apos-cap10."""
    c = Cap(10, pace=0.5, setup=setup_config(), start=(760, 420))
    c.mark(1)
    c.click(ABA('condicoes-pagamento'), at=c.A(1, 'Condições', 0.8), label='aba Condições de Pagamento')
    c.waitfor(text='Nenhuma condição cadastrada ainda.', timeout=10)
    c.hover(TXTP('Defina parcelamentos padrão'), 2.0, at=c.A(1, 'parcelamentos', 0.6), label='Defina parcelamentos padrão (à vista, 30/60/90…)')
    c.hover(TXT('Nenhuma condição cadastrada ainda.'), 1.4, at=c.A(1, 'prontos', 0.6), label='Nenhuma condição cadastrada ainda.')
    c.mark(2)
    c.mark(3)
    c.click(BTN('Nova condição'), at=c.A(3, 'Clico', 0.6), label='Nova condição')
    c.waitfor(text='Nova condição de pagamento', timeout=8)
    # o Nome já vem com o foco quando a janela abre (o 1º clique numa janela custaria 0,9 a 1,6 s)
    c.type(SEL('#pc-name'), '30/60/90 dias', at=c.A(3, 'trinta,', 0.0), cps=14, noClick=True, label='digita 30/60/90 dias (Nome)')
    c.click(CHK('Definir como condição padrão'), at=c.A(3, 'Definir', 0.8), label='marca Definir como condição padrão')
    c.mark(4)
    c.hover(CHK('À vista (parcela única, 0 dias, 100%)'), 1.2, at=c.A(4, 'Toda', 0.5), label='À vista (parcela única, 0 dias, 100%) marcada')
    c.click(CHK('À vista (parcela única, 0 dias, 100%)'), at=c.A(4, 'desmarco', 0.8), label='desmarca À vista (as linhas destravam)')
    c.mark(5)
    c.hover(TXT('Dias após emissão'), 0.6, at=c.A(5, 'dias', 0.6), label='Dias após emissão')
    c.hover(TXT('% do total'), 0.6, at=c.A(5, 'total.', 0.6), label='% do total')
    c.type(DIAS(0), '30', at=c.A(5, 'Trinta', 0.8), cps=8, clear=True, label='1ª parcela: 30 dias')
    c.type(PCT(0), '33,33', at=c.A(5, 'trinta', 0.8, nth=1), cps=10, clear=True, label='1ª parcela: 33,33%')
    c.click(BTNX('Adicionar parcela'), at=c.A(5, 'Sessenta', 0.9), label='Adicionar parcela (2ª)')
    c.type(DIAS(1), '60', at=c.A(5, 'Sessenta', -0.2), cps=8, label='2ª parcela: 60 dias')
    c.type(PCT(1), '33,33', at=c.A(5, 'mesmo', 0.3), cps=10, label='2ª parcela: 33,33%')
    c.click(BTNX('Adicionar parcela'), at=c.A(5, 'noventa', -0.3), label='Adicionar parcela (3ª)')
    c.type(DIAS(2), '90', at=c.A(5, 'noventa', -1.2), cps=8, label='3ª parcela: 90 dias')
    c.type(PCT(2), '33,34', at=c.A(5, 'três', 0.4, nth=2), cps=10, label='3ª parcela: 33,34%')
    c.mark(6)
    c.confere('dlg', ['Soma dos percentuais', '100%'], 'Soma dos percentuais 100%')
    c.hover(TXT('Soma dos percentuais'), 3.2, at=c.A(6, 'Soma', 0.6), label='Soma dos percentuais 100%, em verde')
    c.mark(7)
    c.click(BTN('Criar condição'), at=c.A(7, 'Criar', 0.8), label='Criar condição')
    c.waitfor(text='Condição criada', timeout=10)
    c.waitfor(gone=TXT('Nova condição de pagamento'), timeout=8)
    c.confere('main', ['30/60/90 dias', 'Padrão', '30 / 60 / 90 dias · 3 parcelas'], 'a condição na lista com o selo Padrão')
    c.hover(TXT('30/60/90 dias'), 1.0, at=c.A(7, 'lista', 0.6), label='30/60/90 dias na lista')
    c.hover(TXTP('3 parcelas'), 0.8, at=c.A(7, 'Padrão.', 0.6), label='selo Padrão e 30 / 60 / 90 dias · 3 parcelas')
    c.mark(8)
    c.hover(SEL('main [role=switch]'), 2.0, at=c.A(8, 'chave', 0.6), label='chave da condição (desliga sem apagar, sem clicar)')
    c.hover(SEL('main button:has-text("Editar"), main button[aria-label="Editar"], main button[title="Editar"]'), 0.5, at=c.A(8, 'E', 0.6), label='Editar (sem clicar)')
    c.hover(SEL('main button:has-text("Excluir"), main button[aria-label="Excluir"], main button[title="Excluir"]'), 0.6, label='Excluir (sem clicar)')
    c.hover(TXT('30/60/90 dias'), 1.4, at=c.A(8, 'marca', 0.6), label='a condição padrão aparece no alto da lista')
    c.fim()
    return c


def cap11():
    """Aparência e atalhos: Menu Superior e volta ao Menu Lateral, o menu escuro, Tema Escuro e volta ao Claro, a aba Atalhos, Ctrl+K
    e a busca "cobre", Esc."""
    c = Cap(11, pace=0.5, setup=setup_config(), start=(760, 420))
    c.mark(1)
    c.click(ABA('appearance'), at=c.A(1, 'Aparência,', 0.8), label='aba Aparência')
    c.waitfor(text='Estilo de Navegação (Desktop)', timeout=10)
    c.hover(TXT('Estilo de Navegação (Desktop)'), 1.4, at=c.A(1, 'escolhe', 0.6), label='Estilo de Navegação (Desktop): Menu Lateral marcado')
    c.mark(2)
    c.click(TXT('Menu Superior'), at=c.A(2, 'troca', 0.8), label='Menu Superior (o menu vai para o alto)')
    c.waitfor(text='Estilo de navegação alterado para Menu Superior', timeout=8)
    c.click(TXT('Menu Lateral'), at=c.A(2, 'Menu', 0.8, nth=1), label='volta ao Menu Lateral')
    c.waitfor(text='Estilo de navegação alterado para Menu Lateral', timeout=8)
    c.mark(3)
    c.hover(TXT('Escuro (recomendado)'), 1.6, at=c.A(3, 'escuro,', 0.6), label='Menu: Escuro (recomendado)')
    c.hover(TXT('Seguir o tema'), 1.0, at=c.A(3, 'seguir', 0.6), label='Menu: Seguir o tema')
    c.mark(4)
    rola_ate(c, 'Tema do Sistema', at=c.A(4, 'E', 0.9), label='desce até o Tema do Sistema', y=200, dur_ms=700, prefixo=True, escopo='main')
    c.click(BTNX('Tema Escuro'), at=c.A(4, 'escuro.', 0.8), label='Tema Escuro')
    c.click(BTNX('Tema Claro'), at=c.A(4, 'cansa', 0.8), label='volta ao Tema Claro')
    c.mark(5)
    c.click(SEL('#tab-btn-shortcuts svg'), at=c.A(5, 'Atalhos.', 0.8), label='aba Atalhos', noScroll=True)
    c.waitfor(text='Atalhos de Teclado', timeout=10)
    c.hover(TXT('Navegação'), 0.6, at=c.A(5, 'tela', 0.6), label='lista Navegação')
    c.hover(SEL("main button:text-is('D')"), 1.4, at=c.A(5, 'Shift', 0.6), label='Dashboard: Shift + D')
    c.hover(SEL("main button:text-is('C')"), 1.6, at=c.A(5, 'Clicando', 0.6), label='clicando na letra, troca por outra (sem clicar)')
    c.mark(6)
    c.press('Control+k', at=c.A(6, 'Ctrl+K.', 0.1), label='Ctrl+K abre a busca')
    c.waitfor(target=PH('Buscar páginas, clientes, fornecedores, materiais, funcionários...'), timeout=8)
    c.type(PH('Buscar páginas, clientes, fornecedores, materiais, funcionários...'), 'cobre', at=c.A(6, 'Digito', 0.0), cps=8, noClick=True, label='digita cobre')
    c.waitfor(text='Fio de cobre encapado', timeout=8)
    c.hover(TXT('Cobre mel'), 1.6, at=c.A(6, 'materiais', 0.6), label='Cobre mel, Cobre misto e Fio de cobre encapado')
    c.mark(7)
    c.hover(TXT('Resultados da Busca'), 1.6, at=c.A(7, 'clientes,', 0.6), label='Resultados da Busca')
    c.press('Escape', at=c.A(7, 'Esc', 0.1), label='Esc fecha a busca')
    c.fim()
    return c


ALERTA = '[role=alertdialog], [role=dialog]'
NO_DLG = lambda t, **kw: {'text': t, 'within': '[role=dialog]', **kw}


def js_dlg_fim(dur_ms=900):
    """rolagem suave da janela aberta até o fim (a do Zerar Sistema rola por dentro: a lista, o que fica e o nome da empresa)"""
    return ("(async()=>{const d=[...document.querySelectorAll('[role=dialog]')].pop();if(!d)return 'sem janela';"
            "const c=[d,...d.querySelectorAll('*')].find(e=>/(auto|scroll)/.test(getComputedStyle(e).overflowY)&&e.scrollHeight>e.clientHeight+4);"
            "if(!c)return 'SEM ROLAGEM';const y0=c.scrollTop,dy=c.scrollHeight-c.clientHeight-y0,t0=performance.now();if(dy<3)return 'ok';"
            + SUAVE.replace('DUR', str(int(dur_ms))).replace('DESTINO', 'y0+dy*e') + "return 'fim:'+Math.round(c.scrollTop)})()")


def js_main_topo(dur_ms=700):
    """sobe o <main> que rola até o topo (as abas das Configurações ficam lá em cima, dentro da rolagem)"""
    return ("(async()=>{" + ACHA_ROLAGEM + "const c=rolagem(document.querySelector('main h1'));if(!c)return 'SEM ROLAGEM';const y0=c.scrollTop,t0=performance.now();"
            "if(y0<3)return 'ok';" + SUAVE.replace('DUR', str(int(dur_ms))).replace('DESTINO', 'y0*(1-e)') + "return 'topo:'+Math.round(c.scrollTop)})()")


def cap12():
    """Senha, termos e Zona de Perigo: Alterar Senha (abre e cancela), Ver Contrato (Aceito em, Baixar PDF sem clicar, Fechar) e o
    Zerar Sistema mostrado com calma (Tem certeza? > Sim, continuar > a lista toda marcada, o que fica, o nome da empresa) e
    Cancelar sem digitar nada. As RPCs reset_company_* nunca são chamadas."""
    c = Cap(12, pace=0.5, setup=setup_config(), start=(760, 420))
    c.mark(1)
    rola_ate(c, 'Segurança', at=0.4, label='desce pelo fim do cartão Empresa e pelo Filial até Segurança', y=150, dur_ms=2600, prefixo=True, escopo='main')
    c.hover(BTN('Alterar Senha'), 1.0, at=c.A(1, 'Alterar', 0.6), label='Segurança: Alterar Senha')
    c.mark(2)
    c.click(BTN('Alterar Senha'), at=c.A(2, 'É', 0.5), label='Alterar Senha (abre)')
    c.waitfor(text='Digite sua nova senha abaixo. Certifique-se de usar uma senha forte.', timeout=8)
    c.hover(NO_DLG('Nova Senha', exact=True), 0.6, at=c.A(2, 'senha', 0.6), label='Nova Senha')
    c.hover(NO_DLG('Confirmar Nova Senha', exact=True), 0.8, at=c.A(2, 'vezes.', 0.6), label='Confirmar Nova Senha')
    c.click(BTN('Cancelar'), at=c.A(2, 'Perfil.', 0.6), label='Cancelar (o mesmo botão fica no Perfil)')
    c.waitfor(gone=TXT('Digite sua nova senha abaixo. Certifique-se de usar uma senha forte.'), timeout=8)
    c.mark(3)
    c.click(BTN('Ver Contrato'), at=c.A(3, 'Ver', 0.8), label='Ver Contrato')
    c.waitfor(text='Termos de Uso e Responsabilidade', timeout=10)
    c.hover(NO_DLG('Aceito em'), 2.4, at=c.A(3, 'data', 0.6), label='Aceito em ... (data e hora do aceite)')
    c.mark(4)
    c.hover(BTN('Baixar PDF'), 2.0, at=c.A(4, 'baixar', 0.6), label='Baixar PDF (sem clicar)')
    c.click(SEL('[role=dialog] button:not([type=button]):text-is("Fechar")'), at=c.A(4, 'cópia.', 0.5), label='Fechar o contrato')
    c.waitfor(gone=TXT('Termos de Uso e Responsabilidade'), timeout=8)
    c.mark(5)
    rola_ate(c, 'Zona de Perigo', at=c.A(5, 'E', 0.9), label='desce até a Zona de Perigo', y=300, dur_ms=900, prefixo=True, escopo='main')
    c.hover(TXT('Zona de Perigo'), 1.4, at=c.A(5, 'Zona', 0.6), label='Zona de Perigo, em vermelho')
    c.hover(TXT('Zerar Sistema'), 0.8, at=c.A(5, 'Zerar', 0.6), label='Zerar Sistema')
    c.hover(TXTP('Exclui dados operacionais selecionados'), 2.0, at=c.A(5, 'apaga', 0.6), label='Zerar Sistema: exclui os dados de operação escolhidos')
    c.mark(6)
    c.click(BTN('Zerar Sistema'), at=c.A(6, 'Primeiro,', 0.8), label='Zerar Sistema (abre Tem certeza?)')
    c.waitfor(text='Tem certeza?', timeout=8)
    c.hover(TXTP('Você está prestes a acessar a função de zerar o sistema.'), 1.6, at=c.A(6, 'pergunta', 0.6), label='Tem certeza?')
    c.mark(7)
    c.click(BTN('Sim, continuar'), at=c.A(7, 'Depois,', 0.7), label='Sim, continuar')
    c.waitfor(text='Zerar Sistema - Ação Irreversível', timeout=8)
    c.hover(TXT('Clientes e Fornecedores'), 0.8, at=c.A(7, 'clientes', 0.6), label='Clientes e Fornecedores (marcado)')
    c.hover(TXT('Cadastro de Materiais'), 0.5, at=c.A(7, 'materiais,', 0.5), label='Cadastro de Materiais')
    c.hover(TXT('Estoque de Materiais'), 0.4, at=c.A(7, 'estoque,', 0.5), label='Estoque de Materiais')
    c.hover(TXT('Movimentações Financeiras'), 0.5, at=c.A(7, 'financeiro,', 0.5), label='Movimentações Financeiras')
    c.hover(TXT('Pedidos (Vendas e Compras)'), 0.3, at=c.A(7, 'pedidos', 0.5), label='Pedidos (Vendas e Compras)')
    c.hover(TXT('Notas Fiscais e Config. Fiscal'), 0.4, at=c.A(7, 'notas.', 0.5), label='Notas Fiscais e Config. Fiscal')
    c.hover(TXT('Selecionar tudo'), 0.8, at=c.A(7, 'marcado.', 0.6), label='tudo já vem marcado (Selecionar tudo)')
    c.mark(8)
    c.ev(js_dlg_fim(900), at=c.A(8, 'Ficam', 0.9), label='a janela desce até o que fica e o nome da empresa')
    c.hover(TXTP('Serão mantidos:'), 3.6, at=c.A(8, 'dados', 0.6), label='Serão mantidos: dados básicos, usuários, histórico de pagamentos')
    c.mark(9)
    c.hover(TXTP('Esta ação NÃO PODE ser desfeita!'), 2.0, at=c.A(9, 'Uma', 0.6), label='Esta ação NÃO PODE ser desfeita!')
    c.hover(PH('Nome da empresa'), 2.4, at=c.A(9, 'confirmar,', 0.6), label='PARA CONFIRMAR, DIGITE O NOME DA EMPRESA (campo vazio)')
    c.mark(10)
    c.click(SEL('[role=dialog] button:text-is("Cancelar")'), at=c.A(10, 'Cancelar,', 0.8), label='Cancelar sem digitar nada')
    c.waitfor(gone=TXT('Zerar Sistema - Ação Irreversível'), timeout=8)
    c.fim()
    return c


def cap13():
    """Recapitulando (a montagem da edição usa trechos dos capítulos; este passeio pelo estado final fica de reserva): o card da conta,
    logo, ícone e CNPJ, a prévia do endereço, a numeração, a frase, a Usabilidade e a condição 30/60/90 padrão, a Aparência e a
    Zona de Perigo. L6 é o cartão Próximo."""
    c = Cap(13, pace=0.5, setup=setup_config(), start=(760, 420))
    c.mark(1)
    c.hover(CARD_CONTA, 2.0, at=c.A(1, 'conta', 0.6), label='a conta da Recicla Vale', noScroll=True)
    c.hover(CARD_CONTA, 1.6, at=c.A(1, 'trocador', 0.6), label='o card da conta (trocador de contas no menu)', noScroll=True)
    c.mark(2)
    c.hover(LOGO_IMG, 0.6, at=c.A(2, 'logo,', 0.6), label='o logo')
    c.hover(ICONE_IMG, 0.4, at=c.A(2, 'ícone', 0.6), label='o ícone')
    rola_ate(c, 'CNPJ/CPF', at=c.A(2, 'CNPJ,', 0.7), label='o CNPJ, o contato e o endereço', y=160, dur_ms=700, escopo='main')
    c.hover(SEL('#company-cnpj'), 0.6, at=c.A(2, 'preencheu', 0.5), label='CNPJ 47.318.506/0001-07')
    rola_ate(c, 'Prévia no comprovante', at=c.A(2, 'escolhendo', 0.9), label='a Prévia no comprovante', y=280, dur_ms=800, escopo='main')
    c.hover(PREVIA, 0.8, at=c.A(2, 'comprovante.', 0.5), label='o endereço sem o galpão')
    c.mark(3)
    rola_ate(c, 'Numeração de pedidos', at=c.A(3, 'Viu', 0.6), label='a Numeração de pedidos', y=150, dur_ms=700, escopo='main')
    c.hover(BTNX('Padrão'), 0.8, at=c.A(3, 'pedido', 0.5), label='modelo Padrão')
    rola_ate(c, 'Frase Personalizada', at=c.A(3, 'frase', 0.9), label='a frase do comprovante', y=200, dur_ms=700, escopo='main')
    c.hover(SEL('#receipt-phrase'), 0.8, at=c.A(3, 'Recicla', 0.5), label='a frase da Recicla Vale')
    c.mark(4)
    c.ev(js_main_topo(700), at=c.A(4, 'Conferiu', 0.9), label='sobe às abas')
    c.click(ABA('usability'), at=c.A(4, 'Usabilidade,', 0.7), label='aba Usabilidade')
    c.waitfor(text='Impureza/Tara Desconta no Valor', timeout=10)
    rola_ate(c, 'Impureza/Tara Desconta no Valor', at=c.A(4, 'impureza', 0.8), label='Impureza/Tara Desconta no Valor', y=300, dur_ms=700, escopo='main')
    c.hover(TXT('Impureza/Tara Desconta no Valor'), 0.4, at=c.A(4, 'tara,', 0.5), label='Impureza/Tara (ligada)')
    c.ev(js_main_topo(600), at=c.A(4, 'criou', 0.8), label='sobe às abas (de novo)')
    c.click(ABA('condicoes-pagamento'), at=c.A(4, 'condição', 0.6), label='aba Condições de Pagamento')
    c.waitfor(text='30/60/90 dias', timeout=10)
    c.hover(TXT('30/60/90 dias'), 0.6, at=c.A(4, 'padrão.', 0.5), label='30/60/90 dias com o selo Padrão')
    c.mark(5)
    c.click(ABA('appearance'), at=c.A(5, 'aparência,', 0.7), label='aba Aparência')
    c.waitfor(text='Estilo de Navegação (Desktop)', timeout=10)
    c.click(ABA('company'), at=c.A(5, 'termos,', 0.7), label='aba Empresa')
    c.waitfor(text='Identidade Visual', timeout=10)
    rola_ate(c, 'Zona de Perigo', at=c.A(5, 'Zona', 1.2), label='a Zona de Perigo', y=300, dur_ms=1000, prefixo=True, escopo='main')
    c.mark(6)
    c.cursor((1060, 300), at=c.A(6, 'No', 0.6), label='cursor parado (cartão Próximo: Usuários e permissões)')
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
                if stp['at'] < last:
                    print(f'  aviso cap{n:02d}: at {stp["at"]} < {last} em "{stp.get("label") or stp.get("name")}"')
                last = max(last, stp['at'])
        path = os.path.join(HERE, f'cap{n:02d}.json')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
        print(f'cap{n:02d}: {len(d["steps"])} passos, narração {c.dur:.1f} s{" (voz ESTIMADA)" if c.estimada else ""} -> {os.path.relpath(path, HERE)}')
