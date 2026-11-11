#!/usr/bin/env python3
"""T27 · gera rec/t27/cap00..cap07.json (roteiros do robô) a partir da voz (t27/narracao/capNN.json).

EcoFlix T27 "White Label": EcoSistema 1.59.154 no COMPUTADOR (janela 1280x800, tema claro, menu lateral aberto e escuro),
Supabase falso com o mundo da Recicla Vale Metais, logado como Rafael Nogueira (MASTER); no cap06, como Juliana Prado.
FAKE_NOW 2026-11-10T08:30:00-03:00 em todos os capítulos.
Os `at` saem da palavra que anuncia cada passo: A(linha, palavra, folga) = início da palavra - folga (folga = custo do gesto,
docs/04-gravacao.md "Custo real dos gestos"). Hoje a voz é ESTIMADA (capNN.json com "estimado"); quando a voz chegar, roda-se
de novo com o capNN.json da voz e o roteiro sai preso às palavras de verdade, sem reescrever nada aqui.
Rodar de qualquer pasta: `python3 -I rec/t27/gerar.py [NN ...]`. Depois: `node rec/record.mjs rec/t27/capNN.json --check`.

Login: todo capítulo abre SEM sessão ("anonymous": true) e o `setup` entra pelo formulário do /login com "$TUT_USER"/"$TUT_SENHA"
(nunca no vídeo; a senha nunca vai para arquivo). O cap06 entra como a Juliana: o e-mail fictício dela no lugar do $TUT_USER.

Sementes (rec/mundo/seeds-extra/t27/): `inicio` (logo e ícone do T1, White Label desligado; caps 0 a 3), `apos-cap03` (+ White
Label ligado; cap04) e `apos-cap04` (+ Cor Primária #1F5FAD; caps 5 a 7), em cadeia por cima do mundo base.

Particularidades (app 1.59.154):
 - Logo do topo do menu (img alt "EcoSistema", mesmo com o logo da empresa), botão de recolher o menu (cabeçalho), "Configurações" e o
   card da conta (rodapé do menu) ficam fora da faixa y 96..730 do robô: `noScroll`.
 - Menu recolhido abre ao passar o mouse (Sidebar.tsx): depois de recolher, o cursor vai para o meio da tela e o ícone só é
   registrado (retângulo para o zoom), nunca apontado.
 - "Ver comprovante" abre uma janela nova (o vídeo grava uma aba só): o gancho do `setup` guarda o PDF que o app gera
   (URL.createObjectURL) e as janelas abertas; o passo "captura o PDF" devolve o PDF em base64 no actions.json e
   `t27_pdf.py` grava o arquivo para a edição (o comprovante entra como ilustração com o PDF real do app; docs/04, "sameTab").
 - A tabela de Pedidos rola na horizontal: o "⋮" da última coluna fica cortado na borda; uma rolagem suave por `eval` mostra a
   coluna antes do hover (sem ela o robô rola dentro do passo).
 - Observador `OBS` guarda em `window.__avisos` todo aviso de erro do app e as janelas que não podem aparecer na chegada; o passo
   final devolve a lista (tem de sair vazia).
"""
import hashlib
import json
import os
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TUT = os.path.normpath(os.path.join(HERE, '..', '..'))
NARR = os.path.join(TUT, 't27', 'narracao')
VERSAO = '1.59.154'
FAKE_NOW = '2026-11-10T08:30:00-03:00'
HOJE = '2026-11-10'
EMAIL_JULIANA = 'juliana.prado@reciclavalemetais.example'   # usuária fictícia do mundo (T2); a senha vem de $TUT_SENHA


def stable_id(chave):
    """o mesmo UUID do Supabase falso (core/util.mjs stableId) para @id:<chave>"""
    h = bytearray(hashlib.sha1(('domiflix-fake:' + chave).encode()).digest())
    h[6] = (h[6] & 0x0f) | 0x50
    h[8] = (h[8] & 0x3f) | 0x80
    x = h[:16].hex()
    return f'{x[:8]}-{x[8:12]}-{x[12:16]}-{x[16:20]}-{x[20:32]}'


RAFAEL, JULIANA = stable_id('user.rafael'), stable_id('user.juliana')
assert RAFAEL == '34c36c63-0890-5e89-8963-7c77b7996908'


def storage(uid):
    """localStorage de quem entra pela tela de login: sem aviso de versão nova, sem convite para instalar, sem "Personalize sua
    experiência" e sem o lembrete das tarefas do dia (as chaves que a sessão pronta do robô poria)"""
    return {'app_version': VERSAO, 'notification_shown_version': VERSAO, 'pwa-install-dismissed': 'true', 'theme': 'light',
            'initial-preferences-set': 'true', f'daily-tasks-reminder-last-shown-{uid}': HOJE, f'dominex:daily-tasks-shown:{uid}': HOJE}


NOMES = ['Abertura', 'O que muda', 'O logo e o ícone', 'Ligar o White Label', 'A cor da marca', 'Onde a marca aparece',
         'A empresa toda, na hora', 'Recapitulando']
CADEIA = ['t27/inicio', 't27/apos-cap03', 't27/apos-cap04']
ATE = {0: 1, 1: 1, 2: 1, 3: 1, 4: 2, 5: 3, 6: 3, 7: 3}
SEMENTE = {n: CADEIA[:k] for n, k in ATE.items()}

# Observador de avisos na tela (aceite do ensaio): erro do app e janela que não pode aparecer na chegada ao sistema.
OBS = ("(()=>{window.__avisos=[];const re=/N[ãa]o foi poss[ií]vel|Erro ao|Tente novamente|indispon[ií]vel|Algo deu errado|Falha ao carregar|"
       "Popup bloqueado|Personalize sua experi[êe]ncia|Voc[êe] j[áa] est[áa] conectado|Sistema atualizado|O rel[óo]gio deste computador|Sess[ãa]o expirou/i;"
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
    """voz do capítulo (t27/narracao/capNN.json: a estimada agora, a de verdade depois): (words, linhas, dur, estimada)"""
    d = json.load(open(os.path.join(NARR, f'cap{n:02d}.json'), encoding='utf8'))
    return d['words'], d['linhas'], float(d['dur']), bool(d.get('estimado'))


class Cap:
    def __init__(s, n, pace=0.5, cps=14, start=(720, 150), setup=None, uid=RAFAEL, tail=1.5):
        s.n = n
        s.words, s.linhas, s.dur, s.estimada = carregar_voz(n)
        s.steps = []
        s.pace, s.cps, s.start, s.tail = pace, cps, start, tail
        s.uid = uid
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
        """hover que atravessa o início de uma linha sai partido em dois (a marca entra entre os pedaços)"""
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

    def rolar(s, by, at=None, label=None, ponto=(760, 420), duration=0.5, after=100):
        return s._p({'do': 'scroll', 'point': {'x': ponto[0], 'y': ponto[1]}, 'by': by, 'duration': duration, 'after': after}, at, label, {})

    def cursor(s, ponto, at=None, label=None):
        """leva o cursor a um ponto neutro sem clicar (scroll de 0 px)"""
        return s.rolar(0, at=at, label=label, ponto=ponto, duration=0.3, after=0)

    def registra(s, target, at=None, label=None, **kw):
        """registra o retângulo do alvo para a câmera SEM mexer o mouse (type vazio sem clique)"""
        return s._p({'do': 'type', 'target': target, 'text': '', 'noClick': True, 'optional': True, 'timeout': 4}, at, label, kw)

    def confere(s, escopo, esperados, label):
        """`eval` que LÊ a tela e compara com o que a fala diz: "OK: ..." ou "DIFERENTE: ...". Tenta por ~6,5 s."""
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

    def pause(s, seconds):
        return s.add({'do': 'pause', 'seconds': seconds})

    def waitfor(s, **kw):
        return s.add({'do': 'waitFor', **kw})

    def ev(s, js, at=None, label=None, **kw):
        return s._p({'do': 'eval', 'js': js}, at, label, kw)

    def encaixa(s):
        """hover que invade o próximo gesto com `at` encolhe o `seconds`: sem isso o atraso de um hover se soma ao do seguinte"""
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
        usuario = 'Juliana Prado' if s.uid == JULIANA else 'Rafael Nogueira'
        return {
            'name': f't27-cap{s.n:02d}',
            'title': f'T27 · Cap. {s.n} · {NOMES[s.n]} (narração {str(round(s.dur, 1)).replace(".", ",")} s{" ESTIMADA" if s.estimada else ""}; '
                     f'marcas L1..L{len(s.linhas)} = início de cada linha do roteiro; FAKE_NOW {FAKE_NOW}; usuário {usuario})',
            'seed': f't27-cap{s.n:02d}', 'pace': s.pace, 'cps': s.cps, 'tail': s.tail,
            'start': {'x': s.start[0], 'y': s.start[1]},
            'anonymous': True,
            'seedExtra': list(SEMENTE[s.n]),
            'storage': storage(s.uid),
            'prewarm': ['/login'], 'setup': s.setup, 'steps': s.steps,
        }


# ---------------------------------------------------------------- alvos
BTN = lambda n, **kw: {'role': 'button', 'name': n, 'exact': True, **kw}
LINK = lambda n, **kw: {'role': 'link', 'name': n, 'exact': True, **kw}
TXT = lambda t, **kw: {'text': t, 'exact': True, **kw}
PH = lambda p, **kw: {'placeholder': p, **kw}
SEL = lambda s_, **kw: {'selector': s_, **kw}
AGUARDA = {'do': 'waitFor', 'idle': True}

LOGO_MENU = SEL("img[alt='EcoSistema']")                 # logo do topo do menu aberto (o alt é "EcoSistema" mesmo com o logo da empresa)
ICONE_MENU = SEL("img[alt='Icon']")                      # ícone do topo do menu recolhido
TOGGLE_MENU = SEL('header button:has(svg.lucide-panel-left-close), header button:has(svg.lucide-panel-left)')   # recolher/abrir (y 27)
CONFIG_RODAPE = SEL("button[aria-label='Configurações']")  # rodapé do menu (y 752..788)
CARD_CONTA = SEL("[aria-label='Menu da conta']")          # card da conta no rodapé do menu
ABA_EMPRESA = SEL('#tab-btn-company')
IDENTIDADE = TXT('Identidade Visual')
LOGO_IMG, ICONE_IMG = SEL("main img[alt='Logo']"), SEL("main img[alt='Ícone']")
SUBST = lambda k: BTN('Substituir', nth=k)                # 0 = do logo, 1 = do ícone
REMOVER = lambda k: BTN('Remover', nth=k)
ICONE_TITULO = TXT('Ícone da Empresa (1:1)')
REC_LOGO = TXT('Recomendado: formato horizontal, PNG ou JPG, máximo 5MB')
REC_ICONE = TXT('Recomendado: formato quadrado (1:1), PNG transparente, 128×128px')
WL_GAVETA = SEL("main button:has(h3:text-is('White Label'))")
WL_SELO = SEL("main button:has(h3:text-is('White Label')) div:text-is('Ativo')")
WL_SWITCH = SEL("main div.rounded-xl:has(p:text-is('White Label Desativado')) > button[role=switch], "
                "main div.rounded-xl:has(p:text-is('White Label Ativo')) > button[role=switch]")
PERSONALIZACOES = TXT('Personalizações')
NOME_WL = SEL('#wl-company-name')
COR_ROTULO = TXT('Cor Primária')
COR_PICKER = SEL('#wl-primary-color')
COR_TEXTO = SEL("input[placeholder='#22c55e']")
PREVIEW = SEL("main div:text-is('Preview')")
RESET = BTN('Reset')
SALVAR_WL = BTN('Salvar Personalizações')
PEDIDOS_MENU = LINK('Pedidos')
DASH_MENU = LINK('Dashboard')
MENU_LINHA1 = SEL("main tbody tr:first-child button[aria-haspopup=menu]")   # "⋮" do pedido mais recente (abre ao passar o mouse)
VER_COMPROVANTE = {'role': 'menuitem', 'name': 'Ver comprovante'}

# ---------------------------------------------------------------- trechos comuns (não filmados, no `setup`)
EMAIL_LOGIN = PH('seu@email.com')
SENHA_LOGIN = SEL('input[type=password]')


def login(email='$TUT_USER', espera='Olá, Rafael!'):
    """entra pelo formulário do /login com as variáveis do ambiente (fora do vídeo)"""
    return [
        {'do': 'goto', 'url': '/login'},
        {'do': 'waitFor', 'target': EMAIL_LOGIN, 'timeout': 30},
        {'do': 'type', 'target': EMAIL_LOGIN, 'text': email, 'cps': 40},
        {'do': 'type', 'target': SENHA_LOGIN, 'text': '$TUT_SENHA', 'cps': 40},
        {'do': 'click', 'target': BTN('Entrar')},
        {'do': 'waitFor', 'text': espera, 'timeout': 40},
        AGUARDA,
    ]


LOGIN = login()


def setup_config():
    return LOGIN + [{'do': 'goto', 'url': '/configuracoes'}, {'do': 'waitFor', 'text': 'Configurações do Sistema', 'timeout': 30}, AGUARDA,
                    {'do': 'waitFor', 'target': LOGO_IMG, 'timeout': 15}]


def abre_wl(estado):
    """(setup) abre a gaveta White Label e espera o cartão do interruptor no estado da semente"""
    return [{'do': 'click', 'target': WL_GAVETA}, {'do': 'waitFor', 'text': estado, 'timeout': 10}, {'do': 'pause', 'seconds': 0.6},
            {'do': 'scroll', 'point': {'x': 1240, 'y': 300}, 'by': 0, 'duration': 0.2, 'after': 0}]


# rolagem suave do contêiner que rola o alvo (molde do T14: ACHA_ROLAGEM + SUAVE); o cursor não se mexe
ACHA_ROLAGEM = ("const rolagem=(el)=>{let c=el&&el.parentElement;while(c&&c!==document.body){const s=getComputedStyle(c);"
                "if(/(auto|scroll)/.test(s.overflowY)&&c.scrollHeight>c.clientHeight+4)return c;c=c.parentElement;}"
                "const m=[...document.querySelectorAll('main')].find(e=>/(auto|scroll)/.test(getComputedStyle(e).overflowY)&&e.scrollHeight>e.clientHeight+4);"
                "return m||document.scrollingElement};")
SUAVE = ("await new Promise(res=>{const f=t=>{const p=Math.min(1,(t-t0)/DUR),e=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;c.scrollTo({top:DESTINO,behavior:'instant'});"
         "p<1?requestAnimationFrame(f):res()};requestAnimationFrame(f)});")


def js_ate(texto, y=250, dur_ms=1000, escopo='main'):
    """rola até a folha do DOM cujo texto é `texto` ficar em y px CSS. Devolve o topo final, 'ok', 'SEM ALVO' ou 'SEM ROLAGEM'."""
    alvo = json.dumps(texto, ensure_ascii=False)
    busca = f"[...document.querySelectorAll('{escopo} *')].find(e=>e.children.length===0&&e.textContent.trim()==={alvo}&&e.offsetParent)"
    return ("(async()=>{" + ACHA_ROLAGEM + "const el=" + busca + ";if(!el)return 'SEM ALVO';const c=rolagem(el);if(!c)return 'SEM ROLAGEM';"
            f"const dy=Math.round(el.getBoundingClientRect().top-{int(y)});if(Math.abs(dy)<3)return 'ok';const y0=c.scrollTop,t0=performance.now();"
            + SUAVE.replace('DUR', str(int(dur_ms))).replace('DESTINO', 'y0+dy*e') +
            "return Math.round(el.getBoundingClientRect().top)})()")


def rola_ate(c, texto, at, label, y=250, dur_ms=1000):
    return c.ev(js_ate(texto, y, dur_ms), at=at, label=label)


def js_tabela_direita(dur_ms=450):
    """rola a tabela de Pedidos na horizontal até a última coluna (Ações), suave; devolve a borda direita do "⋮" da 1ª linha"""
    return ("(async()=>{const b=document.querySelector('main tbody tr:first-child button[aria-haspopup=menu]');if(!b)return 'SEM ALVO';"
            "let c=b.parentElement;while(c&&c!==document.body){const s=getComputedStyle(c);if(/(auto|scroll)/.test(s.overflowX)&&c.scrollWidth>c.clientWidth+2)break;c=c.parentElement;}"
            "if(!c||c===document.body)return 'sem rolagem: '+Math.round(b.getBoundingClientRect().right);const x0=c.scrollLeft,dx=c.scrollWidth-c.clientWidth-x0;"
            "if(dx<3)return 'ok';const t0=performance.now();"
            "await new Promise(res=>{const f=t=>{const p=Math.min(1,(t-t0)/%d),e=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;c.scrollTo({left:x0+dx*e,behavior:'instant'});"
            "p<1?requestAnimationFrame(f):res()};requestAnimationFrame(f)});return 'direita:'+Math.round(b.getBoundingClientRect().right)})()") % int(dur_ms)


# PDF do comprovante: o app abre uma janela nova (window.open) e escreve nela o PDF que gerou (URL.createObjectURL). O gancho guarda
# os PDFs e as janelas; o passo de captura devolve o ÚLTIMO PDF (o desenhado de fato) em base64 para o actions.json (t27_pdf.py grava).
JS_GANCHO = ("(()=>{if(window.__pdfs)return 'ja';window.__pdfs=[];window.__janelas=[];const o=URL.createObjectURL.bind(URL);"
             "URL.createObjectURL=(b)=>{try{if(b&&b.type==='application/pdf')window.__pdfs.push(b)}catch(e){}return o(b)};"
             "const wo=window.open;window.open=function(...a){const w=wo.apply(this,a);if(w)window.__janelas.push(w);return w};return 'gancho'})()")
JS_PDF = ("(async()=>{let n=-1,parado=0;for(let i=0;i<50;i++){const k=(window.__pdfs||[]).length;if(k&&k===n){if(++parado>=3)break}else parado=0;n=k;"
          "await new Promise(r=>setTimeout(r,200))}const b=window.__pdfs&&window.__pdfs[window.__pdfs.length-1];if(!b)return 'SEM PDF';"
          "const u=new Uint8Array(await b.arrayBuffer());let s='';for(let i=0;i<u.length;i+=8192)s+=String.fromCharCode.apply(null,u.subarray(i,i+8192));"
          "let t='';try{t=window.__janelas.map(w=>w.document.title).join(' | ')}catch(e){t=String(e)}"
          "return {pdf:'t27-cap05.comprovante.pdf',janela:t,pdfs:window.__pdfs.length,bytes:u.length,b64:btoa(s)}})()")
JS_FECHA = ("(()=>{const j=window.__janelas||[];let k=0;for(const w of j){try{if(!w.closed){w.close();k++}}catch(e){}}return 'janelas fechadas: '+k})()")
JS_COR = "(()=>getComputedStyle(document.documentElement).getPropertyValue('--primary').trim()||'sem --primary')()"


# ================================================================ capítulos
def cap00():
    """Abertura: o Dashboard da Recicla Vale (Rafael), com o logo do EcoSistema no menu. L1 vai sob a ilustração "o sistema trocando de
    marca"; L2 e L3 apontam o logo do topo do menu; L4 (cartão do módulo) e L5 (cartão Antes) com o cursor parado fora do menu."""
    c = Cap(0, setup=LOGIN, start=(720, 150))   # fora dos gráficos do painel (a dica do gráfico abriria sozinha)
    c.mark(1)
    c.mark(2)
    c.hover(LOGO_MENU, 2.4, at=c.A(2, 'logo', 0.6), label='logo do EcoSistema no topo do menu', noScroll=True)
    c.mark(3)
    c.hover(LOGO_MENU, 3.2, at=c.A(3, 'equipe', 0.6), label='o menu: com o White Label, a marca da Recicla Vale', noScroll=True)
    c.mark(4)
    c.cursor((720, 150), at=c.A(4, 'módulo,', 0.6), label='cursor fora do menu (cartão "Módulo White Label")')
    c.mark(5)
    c.fim()
    return c


def cap01():
    """O que muda: do Dashboard ao botão Configurações do rodapé do menu, aba Empresa, Identidade Visual, a gaveta White Label aberta
    ("White Label Desativado"). L3 e L4 vão sob a ilustração "muda × continua"."""
    c = Cap(1, setup=LOGIN, start=(720, 150))
    c.mark(1)
    c.click(CONFIG_RODAPE, at=c.A(1, 'Configurações,', 1.5), label='Configurações (rodapé do menu)', noScroll=True)   # cursor cruza a tela: ~1,5 s
    c.waitfor(text='Configurações do Sistema', timeout=15)
    c.hover(ABA_EMPRESA, 0.4, at=c.A(1, 'Empresa,', 1.0), label='aba Empresa')
    c.hover(IDENTIDADE, 0.6, at=c.A(1, 'Identidade', 0.9), label='Identidade Visual')
    c.mark(2)
    c.hover(WL_GAVETA, 0.3, at=c.A(2, 'gaveta', 0.7), label='gaveta White Label (Personalize o sistema com sua marca)')
    c.click(WL_GAVETA, at=c.A(2, 'aqui.', 0.5), label='abre a gaveta White Label')
    c.waitfor(text='White Label Desativado', timeout=8)
    c.hover(TXT('White Label Desativado'), 0.4, at=c.A(2, 'desativado.', 1.4), label='White Label Desativado e o interruptor desligado')
    c.confere('main', ['White Label Desativado', 'O logo da EcoSistema está sendo exibido'], 'cartão do interruptor desligado')
    c.mark(3)
    c.mark(4)
    c.fim()
    return c


def cap02():
    """O logo e o ícone (sem enviar nada: os dois vieram do T1): o logo e o Substituir/Remover, a ilustração "qual imagem vai onde" (L3,
    com a rolagem até o Ícone por baixo), o ícone e o Substituir dele, o zoom no recomendado do ícone (L5) e no do logo (L6, 5MB)."""
    c = Cap(2, setup=setup_config(), start=(1000, 300))
    c.mark(1)
    c.hover(LOGO_IMG, 2.2, at=c.A(1, 'logo', 0.6), label='Logo da Empresa: o logo da Recicla Vale (enviado no tutorial da empresa)')
    c.hover(LOGO_IMG, 2.0, at=c.A(1, 'ligado,', 0.6), label='o logo: é ele que aparece no menu aberto')
    c.mark(2)
    c.hover(SUBST(0), 1.0, at=c.A(2, 'clicar', 0.6), label='Substituir do logo (sem clicar)')
    c.hover(REMOVER(0), 0.6, at=c.A(2, 'mandar', 0.6), label='Remover do logo (sem clicar)')
    c.mark(3)
    rola_ate(c, 'Ícone da Empresa (1:1)', at=c.A(3, 'ícone,', 0.0), label='desce até o Ícone da Empresa (sob a ilustração)', y=300, dur_ms=700)
    c.mark(4)
    c.hover(ICONE_TITULO, 1.0, at=c.A(4, 'abaixo,', 0.6), label='Ícone da Empresa (1:1): Usado no menu lateral quando recolhido')
    c.hover(ICONE_IMG, 2.2, at=c.A(4, 'Ícone', 0.6, nth=1), label='o ícone da Recicla Vale (também do tutorial da empresa)')
    c.mark(5)
    c.hover(SUBST(1), 0.8, at=c.A(5, 'Substituir.', 0.6), label='Substituir do ícone (sem clicar)')
    c.hover(REC_ICONE, 3.6, at=c.A(5, 'recomenda', 0.6), label='Recomendado: formato quadrado (1:1), PNG transparente, 128×128px')
    c.mark(6)
    c.hover(REC_LOGO, 8.5, at=c.A(6, 'Uma', 0.6), label='Recomendado: formato horizontal, PNG ou JPG, máximo 5MB')
    c.fim()
    return c


def cap03():
    """Ligar o White Label: a gaveta aberta no setup ("White Label Desativado"), o zoom no cartão do interruptor (dica do logo), liga,
    "White Label Ativo" e o selo, o logo da Recicla Vale no menu, recolhe o menu (ícone; zoom em L5 e L6) e abre de novo. Vira apos-cap03."""
    c = Cap(3, setup=setup_config() + abre_wl('White Label Desativado'), start=(1240, 300))
    c.mark(1)
    c.hover(TXT('White Label Desativado'), 0.5, at=c.A(1, 'hora', 0.9), label='cartão White Label Desativado')
    c.mark(2)
    c.hover(WL_SWITCH, 1.2, at=c.A(2, 'interruptor', 0.6), label='cartão do interruptor (White Label Desativado): quem libera é o logo')
    c.hover(WL_SWITCH, 2.3, at=c.A(2, 'travado,', 0.6), label='o interruptor: sem logo enviado, fica travado')
    c.mark(3)
    c.click(WL_SWITCH, at=c.A(3, 'interruptor.', 0.6), label='liga o interruptor do White Label')
    c.waitfor(text='White Label Ativo', timeout=8)
    c.hover(TXT('White Label Ativo'), 0.4, at=c.A(3, 'White', 0.9), label='White Label Ativo e o selo Ativo da gaveta (aviso "White Label ativado!")')
    c.confere('main', ['White Label Ativo', 'Seu logo está sendo exibido no lugar do logo EcoSistema'], 'White Label ligado')
    c.mark(4)
    c.hover(LOGO_MENU, 4.4, at=c.A(4, 'menu:', 0.6), label='logo da Recicla Vale no topo do menu (no lugar do EcoSistema)', noScroll=True)
    c.mark(5)
    c.click(TOGGLE_MENU, at=c.A(5, 'ícone?', 0.7), label='recolhe o menu (botão de painel no cabeçalho)', noScroll=True)
    c.cursor((760, 420), at=c.A(5, 'aparece', 0.6), label='mouse longe do menu recolhido')
    c.registra(ICONE_MENU, label='ícone da Recicla Vale no topo do menu recolhido')
    c.mark(6)
    c.mark(7)
    c.click(TOGGLE_MENU, at=c.A(7, 'Abro', 0.7), label='abre o menu de novo', noScroll=True)
    c.hover(LOGO_MENU, 1.2, at=c.A(7, 'volta', 0.6), label='volta o logo da Recicla Vale', noScroll=True)
    c.fim()
    return c


def cap04():
    """A cor da marca: as Personalizações (gaveta aberta no setup, com o selo Ativo), o Nome Exibido (sem zoom, sem digitar), a Cor
    Primária #1F5FAD digitada e o Preview, Salvar Personalizações (botão, interruptor e barrinha do menu no azul) e o Reset (sem clicar).
    Vira apos-cap04."""
    c = Cap(4, setup=setup_config() + abre_wl('White Label Ativo'), start=(1240, 300))
    c.mark(1)
    rola_ate(c, 'Personalizações', at=c.A(1, 'aparecem', 0.9), label='desce até as Personalizações', y=250, dur_ms=900)
    c.hover(PERSONALIZACOES, 0.9, at=c.A(1, 'Personalizações.', 0.6), label='Personalizações')
    c.mark(2)
    c.hover(NOME_WL, 2.8, at=c.A(2, 'Nome', 0.6), label='Nome Exibido no Sistema (vazio; sem zoom)')
    c.mark(3)
    c.hover(COR_ROTULO, 0.6, at=c.A(3, 'Cor', 0.6), label='Cor Primária')
    c.hover(COR_PICKER, 0.5, at=c.A(3, 'seletor', 0.6), label='seletor de cor (sem abrir)')
    c.click(COR_TEXTO, at=c.A(3, 'digitar', 0.7), label='campo do código da Cor Primária')
    c.type(COR_TEXTO, '#1F5FAD', at=c.A(3, 'digito', 0.05), noClick=True, label='digita #1F5FAD na Cor Primária')
    c.hover(PREVIEW, 2.6, at=c.A(3, 'quadradinho', 0.6), label='Preview no azul da Recicla Vale')
    c.confere_campos(['#1F5FAD'], 'Cor Primária digitada')
    c.mark(4)
    c.click(SALVAR_WL, at=c.A(4, 'Salvar', 0.7), label='Salvar Personalizações')
    c.waitfor(text='Configurações de White Label salvas!', timeout=8)
    c.ev(JS_COR, label='cor --primary aplicada (azul)')
    c.hover(SALVAR_WL, 0.5, at=c.A(4, 'botões,', 0.6), label='botão no azul')
    c.hover(WL_SWITCH, 0.8, at=c.A(4, 'interruptores', 0.6), label='interruptor no azul')
    c.hover(CONFIG_RODAPE, 2.2, at=c.A(4, 'barrinha', 0.6), label='barrinha azul do item ativo no menu (Configurações)', noScroll=True)
    c.mark(5)
    c.hover(COR_TEXTO, 1.4, at=c.A(5, 'Cor', 0.6), label='Cor Primária (vazia = verde padrão)')
    c.hover(RESET, 1.6, at=c.A(5, 'Reset', 0.6), label='Reset (sem clicar: só limpa o campo)')
    c.hover(SALVAR_WL, 1.2, at=c.A(5, 'Salvar', 0.6), label='Salvar Personalizações (a volta pro verde vale depois dele)')
    c.fim()
    return c


def cap05():
    """Onde a marca aparece: L1 e L2 sob a ilustração do mapa (o Dashboard com o logo e o azul por baixo); L3 Pedidos, o "⋮" do pedido
    mais recente e "Ver comprovante" (janela nova: o PDF real do app vai para a edição); L4 e L5 sob a ilustração do Portal e do
    remover × desligar."""
    c = Cap(5, setup=LOGIN + [{'do': 'eval', 'js': JS_GANCHO}], start=(720, 150))
    c.mark(1)
    c.mark(2)
    c.mark(3)
    c.click(PEDIDOS_MENU, at=c.A(3, 'Olha', 0.8), label='Pedidos no menu')
    c.waitfor(selector='main tbody tr', timeout=15)
    c.ev(js_tabela_direita(), label='mostra a coluna Ações da tabela (rolagem horizontal suave)')
    c.hover(MENU_LINHA1, 0.3, at=c.A(3, 'um', 0.7), label='menu ⋮ do pedido mais recente (abre ao passar o mouse)')
    c.click(VER_COMPROVANTE, at=c.A(3, 'pedido.', 0.5), label='Ver comprovante (abre a janela nova)', noScroll=True)
    c.ev(JS_PDF, label='captura o PDF do comprovante (a edição mostra o PDF real)')
    c.cursor((760, 250), label='cursor fora da tabela')
    c.mark(4)
    c.ev(JS_FECHA, at=c.A(4, 'Portal', 0.0), label='fecha a janela do comprovante (sob a ilustração)')
    c.mark(5)
    c.fim()
    return c


def cap06():
    """A empresa toda, na hora: sessão da Juliana (login fora do vídeo) no Dashboard dela, com o logo da Recicla Vale e a barrinha
    azul; L3 sob a ilustração "a troca chegando a todos"."""
    c = Cap(6, setup=login(EMAIL_JULIANA, 'Olá, Juliana!'), start=(720, 150), uid=JULIANA)
    c.mark(1)
    c.hover(CARD_CONTA, 1.6, at=c.A(1, 'Juliana,', 0.6), label='card da conta: Juliana Prado', noScroll=True)
    c.mark(2)
    c.hover(LOGO_MENU, 1.0, at=c.A(2, 'Mesmo', 0.6), label='o logo da Recicla Vale no topo do menu da Juliana', noScroll=True)
    c.hover(DASH_MENU, 1.6, at=c.A(2, 'cor,', 0.6), label='barrinha azul do item ativo (Dashboard)', noScroll=True)
    c.mark(3)
    c.mark(4)
    c.hover(CARD_CONTA, 1.6, at=c.A(4, 'Juliana', 0.6), label='Juliana: só vê o resultado', noScroll=True)
    c.fim()
    return c


def cap07():
    """Recapitulando (a montagem da edição usa trechos dos capítulos; este passeio pelo estado final fica de reserva): a gaveta, o logo
    e o ícone, o interruptor ligado e o logo no menu, a Cor Primária, os Pedidos com o menu do comprovante. L6 é o cartão Próximo."""
    c = Cap(7, setup=setup_config() + abre_wl('White Label Ativo'), start=(1240, 300))
    c.mark(1)
    c.hover(WL_GAVETA, 1.0, at=c.A(1, 'White', 0.6), label='a gaveta White Label na aba Empresa')
    c.hover(LOGO_IMG, 0.6, at=c.A(1, 'logo', 0.6), label='o logo')
    c.hover(ICONE_IMG, 1.6, at=c.A(1, 'ícone', 0.6), label='o ícone quadrado')
    c.mark(2)
    c.hover(WL_SWITCH, 0.8, at=c.A(2, 'interruptor,', 0.6), label='o interruptor ligado')
    c.hover(LOGO_MENU, 1.8, at=c.A(2, 'logo', 0.6), label='o logo da Recicla Vale no menu', noScroll=True)
    c.mark(3)
    rola_ate(c, 'Personalizações', at=c.A(3, 'Salvou', 0.9), label='desce até as Personalizações', y=250, dur_ms=700)
    c.hover(COR_TEXTO, 1.4, at=c.A(3, 'cor', 0.6), label='a Cor Primária #1F5FAD')
    c.mark(4)
    c.click(PEDIDOS_MENU, at=c.A(4, 'Viu', 0.8), label='Pedidos no menu')
    c.waitfor(selector='main tbody tr', timeout=15)
    c.ev(js_tabela_direita(), label='mostra a coluna Ações da tabela (rolagem horizontal suave)')
    c.hover(MENU_LINHA1, 1.0, at=c.A(4, 'rodapé', 0.6), label='o menu do pedido com Ver comprovante')
    c.mark(5)
    c.cursor((760, 150), at=c.A(5, 'viu', 0.6), label='cursor fora da tabela (a equipe toda)')
    c.mark(6)
    c.fim()
    return c


CAPS_ROBO = {n: globals()[f'cap{n:02d}'] for n in range(8) if f'cap{n:02d}' in globals()}

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
