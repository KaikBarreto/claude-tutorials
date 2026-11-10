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

    def fim(s):
        s.flush(1e9)
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
    c = Cap(0, pace=0.6, setup=[{'do': 'goto', 'url': '/cadastro'}, {'do': 'waitFor', 'target': CAD_EMPRESA, 'timeout': 30}, AGUARDA],
            prewarm=['/cadastro'], start=(1040, 300))
    c.mark(1)
    c.mark(2)
    c.mark(3)
    c.hover(TXT('Cadastro'), 1.0, at=c.A(3, 'começo:', 0.7), label='título Cadastro')
    c.hover(TXTP('Teste grátis por 7 dias'), 1.6, at=c.A(3, 'criar', 0.7), label='Teste grátis por 7 dias · Sem compromisso · Acesso total')
    c.hover(TXT('Dados'), 0.8, at=c.A(3, 'entrar', 0.7), label='etapas Dados e Acesso')
    c.hover(CAD_EMPRESA, 1.2, at=c.A(3, 'preencher', 0.7), label='Nome da Empresa (o cursor desce pelo formulário)')
    c.hover(CAD_EMAIL, 1.0, at=c.A(3, 'Depois,', 0.7), label='Email')
    c.hover(CAD_FONE, 1.0, at=c.A(3, 'pedido,', 0.7), label='Telefone')
    c.hover(BTNX('Continuar'), 1.4, at=c.A(3, 'comprovante', 0.7, nth=0), label='Continuar (sem clicar)')
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
    c.hover(BTN('Entrar com Google'), 2.4, at=c.A(3, 'Google,', 0.7), label='Entrar com Google (sem clicar)')
    c.hover(BTN('Entrar com Google'), 1.6, at=c.A(3, 'existe', 0.5), label='Entrar com Google: entra na conta que já existe')
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


def cap04():
    """Esqueci minha senha: /login sem sessão, o e-mail, Enviar Código, as seis casas (L4 é ilustração), o código 481207, a caixa
    laranja e o reenvio, Verificar e a senha nova."""
    c = Cap(4, pace=0.5, setup=[{'do': 'goto', 'url': '/login'}, {'do': 'waitFor', 'target': EMAIL_LOGIN, 'timeout': 30}, AGUARDA],
            prewarm=['/login'], start=(300, 560))
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
    c.click(SEL('input[type=password]', nth=0), at=c.A(7, 'Digito', 0.8), label='Nova Senha')
    c.type(SEL('input[type=password]', nth=0), '$TUT_SENHA', at=c.A(7, 'nova', 0.3), cps=40, noClick=True, label='digita a nova senha')
    c.click(SEL('input[type=password]', nth=1), at=c.A(7, 'vezes', 0.5), label='Confirmar Nova Senha')
    c.type(SEL('input[type=password]', nth=1), '$TUT_SENHA', at=c.A(7, 'e', 0.1), cps=40, noClick=True, label='repete a nova senha')
    c.click(BTN('Alterar Senha e Entrar'), at=c.A(7, 'Alterar', 0.6), label='Alterar Senha e Entrar')
    c.waitfor(text='Senha alterada com sucesso! Você já está logado.', timeout=12)
    c.registra(TXT('Senha alterada com sucesso! Você já está logado.'), label='toast Senha alterada com sucesso! Você já está logado.')
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
