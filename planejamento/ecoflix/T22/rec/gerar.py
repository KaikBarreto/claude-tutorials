#!/usr/bin/env python3
"""T22 · Gerencial: matriz e filiais (EcoFlix, EcoSistema 1.59.154): gera rec/t22/cap00..cap11.json (roteiros do robô) a partir da fala
($TUT_HOME/t22/narracao/capNN.json: o estimado até a voz chegar; com a voz, o da voz, sem mudar nada aqui). O cap12 (Recapitulando) é
montagem das gravações dos outros capítulos: não tem robô.

Computador 1600x900, menu lateral aberto. Logado como Rafael Nogueira (MASTER, matriz Recicla Vale Metais) em todos os capítulos, menos o
cap03, gravado como Sandra Pires (MASTER da Filial Pindamonhangaba). FAKE_NOW 2026-11-10T08:30:00-03:00 em todos (o mesmo no Supabase
falso e no robô). Rodar de qualquer pasta: `python3 -I rec/t22/gerar.py [NN ...]` (ANCORAS=1 lista as âncoras). Depois:
`node rec/record.mjs rec/t22/capNN.json --check`; ensaio rápido: `python3 -I rec/t22/ensaio.py NN` + `--rapido`; gravação: sem `--rapido`.

LOGIN: todo capítulo é "anonymous" e o setup entra pela tela de login com "$TUT_USER"/"$TUT_SENHA" do ambiente (Rafael; o Supabase falso
aceita qualquer senha; o valor nunca vai para arquivo nem log). No cap03 o e-mail digitado é o da Sandra (fictício, do mundo) e a senha o
"$TUT_SENHA".

Cada passo é preso a uma palavra da fala: A(linha, 'palavra', folga) = início da palavra − folga (o custo do gesto até o cursor chegar:
clique ~0,6 s, 1º clique numa janela recém-aberta ~1,2 s, hover ~0,5 s; digitação sem clique na palavra − 0,05 s). A palavra casa
INTEIRA (sem acento e pontuação); repetida na linha pede `nth`. Marca Ln 0,9 s antes da linha; um passo que começa até 0,25 s antes da
marca a puxa para o início dele.

Estado de partida (rec/mundo/seeds-extra/t22/, rec/t22/t22_sementes.py e t22_estado.py): `inicio` (a filial, sem grupo) nos caps 0 a 2;
+ `apos-cap02` (o grupo, código GRP-7C4E9A) no cap03; + `apos-cap03` (a filial vinculada) nos caps 4 a 9; + `apos-cap09` (catálogo, tabelas,
categorias, a Fundição marcada e o envio feito) no cap10; + `apos-cap10` (aprovação ligada e a transferência concluída) no cap11;
`apos-cap11` (o pagamento do grupo confirmado) fecha a cadeia.
"""
import hashlib
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TUT = os.path.normpath(os.path.join(HERE, '..', '..'))
AULA = 't22'
NARR = os.path.join(TUT, AULA, 'narracao')
FAKE_NOW = '2026-11-10T08:30:00-03:00'
try:
    VERSAO = open(os.path.join(TUT, 'app', 'dist', '.versao-app'), encoding='utf8').read().strip() or '1.60.18'
except OSError:
    VERSAO = '1.60.18'
HOJE = FAKE_NOW[:10]
CODIGO = 'GRP-7C4E9A'   # generate_group_invite_code: 'GRP-' + 6 hexadecimais (o handler fixa este)
SANDRA_EMAIL = 'sandra.pires@reciclavalemetais.example'
NOMES = ['Abertura', 'Como o Gerencial funciona', 'Criar o grupo e o código', 'Do lado da filial', 'Quando o código não entra',
         'O Dashboard Gerencial', 'Ranking e resumo por unidade', 'A DRE do grupo', 'Caixa e competência', 'Além da DRE',
         'O estoque do grupo', 'Corrigir o estoque de uma unidade', 'Enviar Ativos', 'Preço diferente por unidade',
         'Transferência com aprovação', 'Lote, fila e o pedido da filial', 'Vender com o estoque da outra unidade', 'Assinaturas numa fatura só', 'Recapitulando']
# sementes de partida (nomes dos arquivos em rec/mundo/seeds-extra/t22/; os nomes apos-capNN seguem a numeração ANTIGA da cadeia, que não mudou):
#   inicio (a filial, sem grupo) | apos-cap02 (grupo criado) | apos-cap03 (filial vinculada) | apos-cap09 (catálogo, tabelas, categorias, envio)
#   | apos-cap10 (aprovação ligada, latinha transferida) | apos-cap11 (pagamento do grupo)
#   | codigo-vencido (grupo criado com o código vencido, filial sem vínculo) | venda-outra-unidade (apos-cap10 com a aprovação desligada)
_E = ['t22/inicio', 't22/apos-cap02', 't22/apos-cap03', 't22/apos-cap09', 't22/apos-cap10']
_A3 = _E[:3]
SEMENTE = {0: _E[:1], 1: _E[:1], 2: _E[:1], 3: _E[:2], 4: ['t22/inicio', 't22/codigo-vencido'],
           **{n: _A3 for n in (5, 6, 7, 8, 9, 10, 11, 12)}, 13: _E[:4], 14: _E[:4], 15: _E[:5], 16: _E[:5] + ['t22/venda-outra-unidade'], 17: _E[:5], 18: _E[:5]}

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


RAFAEL = stable_id('user.rafael')
SANDRA = stable_id('user.sandra')
GRUPO = stable_id('t22.grupo')


def storage(n, extra=None):
    # os capítulos 4 e 15 trocam de usuário no meio (Sandra e Rafael): a dica diária de tarefas fica calada para os dois
    d = {'app_version': VERSAO, 'notification_shown_version': VERSAO, 'pwa-install-dismissed': 'true', 'theme': 'light',
         f'daily-tasks-reminder-last-shown-{SANDRA}': HOJE, f'daily-tasks-reminder-last-shown-{RAFAEL}': HOJE, 'initial-preferences-set': 'true'}
    d.update(extra or {})
    return d


# ---------------------------------------------------------------- observador de avisos de erro (aceite: tem de sair vazio)
OBS = ("(()=>{window.__avisos=[];const re=/N[ãa]o foi poss[ií]vel|Erro ao|Tente novamente|Algo deu errado|Falha ao|Something went wrong|indispon[ií]vel|Access denied/i;"
       "const chk=(t)=>{t=(t||'').trim();const m=t&&t.match(new RegExp('[^]{0,40}('+re.source+')[^]{0,40}','i'));"
       "if(m&&!/fica indispon/i.test(m[0])&&window.__avisos.length<10)window.__avisos.push(m[0].replace(/[\\n\\r\\t ]+/g,' '))};new MutationObserver(ms=>{for(const m of ms){"
       "m.addedNodes.forEach(n=>chk(n.textContent));if(m.type==='characterData')chk(m.target.textContent)}}).observe(document.body,"
       "{childList:true,subtree:true,characterData:true});chk(document.body.innerText);"
       "setInterval(()=>{document.querySelectorAll('[data-sonner-toast][data-type=error]').forEach(t=>{const s='TOAST DE ERRO: '+t.textContent.trim().slice(0,90);"
       "if(!window.__avisos.includes(s)&&window.__avisos.length<10)window.__avisos.push(s)})},300);return 1})()")


class Cap:
    def __init__(s, n, setup, pace=0.5, cps=40, start=(760, 470), storage_extra=None):
        s.n = n
        s.words, s.linhas, s.dur, s.estimado = carregar_voz(n)
        s.steps, s.pending, s.anchors = [], [], []
        s.pace, s.cps, s.start = pace, cps, start
        s.setup = list(setup) + [{'do': 'eval', 'js': OBS}, {'do': 'eval', 'js': ANIMA_SEMPRE}]
        s.storage_extra = storage_extra

    # ---- tempo
    def L(s, i):
        return round(s.linhas[i - 1]['s'], 2)

    def W(s, i, palavra, nth=0, fim=False):
        q = norm(palavra)
        hits = [w for w in s.words if w['linha'] == i - 1 and norm(w['w']) == q]
        if len(hits) <= nth:
            raise SystemExit(f'cap{s.n:02d}: palavra "{palavra}" (#{nth}) não achada na linha {i}: ' + ' '.join(w['w'] for w in s.words if w['linha'] == i - 1))
        return hits[nth]['e' if fim else 's']

    def tem(s, i, palavra):
        """a palavra está na linha i da fala de hoje? (para um gesto que só existe se a fala citar o elemento)"""
        return any(w['linha'] == i - 1 and norm(w['w']) == norm(palavra) for w in s.words)

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

    def registra(s, target, at=None, label=None):
        """registra o retângulo do alvo para a câmera SEM mexer o mouse (passo `type` sem clique e sem texto)"""
        return s._p({'do': 'type', 'target': target, 'text': '', 'noClick': True, 'optional': True, 'timeout': 4}, at, label, {})

    def colar(s, seletor, texto, at=None, label=None):
        """"cola" o texto no campo (foco + insertText, ~0,05 s): o React recebe o input como de um Ctrl+V"""
        js = ("(()=>{const el=document.querySelector(%s);if(!el)return 'SEM ALVO';el.focus();el.select&&el.select();"
              "document.execCommand('insertText',false,%s);return el.value})()") % (json.dumps(seletor), json.dumps(texto))
        return s.ev(js, at=at, label=label)

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
        quem = 'Sandra Pires (Filial Pindamonhangaba)' if s.n == 3 else ('Sandra Pires e depois Rafael Nogueira' if s.n in (4, 15) else 'Rafael Nogueira (matriz)')
        return {
            'name': f'{AULA}-cap{s.n:02d}',
            'title': f'T22 · Cap. {s.n} · {NOMES[s.n]} (narração{est} {str(round(s.dur, 1)).replace(".", ",")} s; marcas L1..L{len(s.linhas)} = início de cada '
                     f'linha do roteiro; FAKE_NOW {FAKE_NOW}; logado como {quem})',
            'seed': f'{AULA}-cap{s.n:02d}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
            'start': {'x': s.start[0], 'y': s.start[1]},
            'anonymous': True, 'storage': storage(s.n, s.storage_extra),
            'seedExtra': list(SEMENTE[s.n]),
            'prewarm': ['/login'], 'setup': s.setup, 'steps': s.steps,
        }


# ---------------------------------------------------------------- alvos
MAIN = 'main'
DLG = '[role=dialog]'
ALERTA = '[role=alertdialog]'
BTN = lambda n, within=None, **kw: {'role': 'button', 'name': n, 'exact': True, **({'within': within} if within else {}), **kw}
BTNX = lambda n, within=None, **kw: {'role': 'button', 'name': n, **({'within': within} if within else {}), **kw}
TXT = lambda t, within=None, **kw: {'text': t, 'exact': True, **({'within': within} if within else {}), **kw}
TXTP = lambda t, within=None, **kw: {'text': t, **({'within': within} if within else {}), **kw}
SEL = lambda s, **kw: {'selector': s, **kw}
OPT = lambda n, **kw: {'role': 'option', 'name': n, **kw}
LINK = lambda n, **kw: {'role': 'link', 'name': n, **kw}
TAB = lambda v: SEL(f'#tab-btn-{v}')                 # abas das telas com SettingsSidebarLayout (Configurações do grupo, Financeiro, Estoque)
AGUARDA = {'do': 'waitFor', 'idle': True}
PERIODO = lambda t: SEL(f'main button[role=combobox]:has-text("{t}")')
MENU_GER = BTNX('Gerencial (Filiais)')
LINK_GER = lambda nome, rota: SEL(f'a[href="{rota}"]')   # itens do grupo "Gerencial (Filiais)" do menu lateral


def login(email='$TUT_USER', espera='Olá, Rafael!'):
    return [{'do': 'waitFor', 'target': {'label': 'E-mail'}, 'timeout': 30},
            {'do': 'type', 'target': {'label': 'E-mail'}, 'text': email, 'cps': 40},
            {'do': 'type', 'target': {'label': 'Senha', 'exact': True}, 'text': '$TUT_SENHA', 'cps': 40},
            {'do': 'click', 'target': BTN('Entrar')},
            {'do': 'waitFor', 'text': espera, 'timeout': 30}, AGUARDA]


def vai(url, espera, timeout=25):
    return [{'do': 'goto', 'url': url}, {'do': 'waitFor', 'text': espera, 'timeout': timeout}, AGUARDA]


# ---------------------------------------------------------------- rolagem roteirizada (eval: o cursor não se mexe)
ACHA_ROLAGEM = ("const rolagem=(el)=>{let c=el&&el.parentElement;while(c&&c!==document.body){const s=getComputedStyle(c);"
                "if(/(auto|scroll)/.test(s.overflowY)&&c.scrollHeight>c.clientHeight+4)return c;c=c.parentElement;}"
                "return [...document.querySelectorAll('main')].find(e=>/(auto|scroll)/.test(getComputedStyle(e).overflowY)&&e.scrollHeight>e.clientHeight+4)||document.scrollingElement};")
SUAVE = ("await new Promise(res=>{const t0=performance.now();const f=t=>{const p=Math.min(1,(t-t0)/DUR),e=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;"
         "c.scrollTop=DESTINO;p<1?requestAnimationFrame(f):res()};requestAnimationFrame(f)});")
FOLHA = "[...document.querySelectorAll('%s *')].find(e=>e.children.length===0&&e.textContent.trim()===%s&&e.getClientRects().length)"
# sem folha com o texto (ex.: <h2><svg/> Resumo por Unidade</h2>): o elemento com um nó de texto direto igual ao texto
FOLHA2 = ("[...document.querySelectorAll('%s *')].find(e=>[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()===%s)"
          "&&e.getClientRects().length)")


def js_rola_texto(texto, y=300, dur_ms=800, escopo='main'):
    """rolagem suave do contêiner que rola a folha do DOM cujo texto é `texto` até ela ficar em y px CSS; devolve o topo final"""
    achar = FOLHA % (escopo, json.dumps(texto)) + '||' + FOLHA2 % (escopo, json.dumps(texto))
    return ("(async()=>{" + ACHA_ROLAGEM + "const el=" + achar + ";if(!el)return 'SEM ALVO';const c=rolagem(el);if(!c)return 'SEM ROLAGEM';"
            f"const dy=Math.round(el.getBoundingClientRect().top-{int(y)});if(Math.abs(dy)<3)return 'ok';const y0=c.scrollTop;"
            + (SUAVE.replace('DUR', str(int(dur_ms))).replace('DESTINO', 'y0+dy*e') if dur_ms else "c.scrollTop=y0+dy;")
            + "return Math.round(el.getBoundingClientRect().top)})()")


def js_topo(dur_ms=600):
    """sobe a página até o topo"""
    return ("(async()=>{" + ACHA_ROLAGEM + "const el=document.querySelector('main h1')||document.querySelector('main *');const c=rolagem(el);if(!c)return 'SEM ROLAGEM';"
            "const y0=c.scrollTop;if(y0<3)return 'ok';const dy=-y0;"
            + (SUAVE.replace('DUR', str(int(dur_ms))).replace('DESTINO', 'y0+dy*e') if dur_ms else "c.scrollTop=0;") + "return 'topo'})()")


def rola_setup(texto, y=300):
    return {'do': 'eval', 'js': js_rola_texto(texto, y, 0)}


def js_clica_texto(texto, escopo='main', tag='button'):
    """clique por eval (sem cursor) no `tag` cujo texto visível é `texto`"""
    return ("(()=>{const b=[...document.querySelectorAll(%s)].find(e=>e.offsetParent&&e.innerText.trim()===%s);if(!b)return 'SEM ALVO';b.click();return 'ok'})()"
            % (json.dumps(f'{escopo} {tag}'), json.dumps(texto)))


ANIMA = "(()=>{const a=document.getAnimations().filter(x=>x.currentTime<0);a.forEach(x=>x.startTime=document.timeline.currentTime);return a.length})()"
# o mesmo conserto a cada 60 ms, a partir do setup (o relógio falso deixa animação do framer-motion/WAAPI parada antes do início: o checkout
# e o "Pagamento Confirmado!" ficavam em branco); não vale depois de um `goto` (nenhum capítulo navega por goto fora do setup)
ANIMA_SEMPRE = ("(()=>{if(window.__anima)return 'ja';window.__anima=setInterval(()=>{try{document.getAnimations().forEach(x=>{"
                "if(x.currentTime!==null&&x.currentTime<0)x.startTime=document.timeline.currentTime})}catch(e){}},60);return 'ok'})()")


# ---------------------------------------------------------------- alvos próprios do T22
CONFIG_RODAPE = SEL("button[aria-label='Configurações']")          # rodapé do menu lateral (fora da faixa de clique: noScroll)
COPIAR = SEL('main button:has(svg.lucide-copy)')                   # copiar o código de convite
REGERAR = SEL("main button[title='Gerar novo código (válido por 30 dias)']")
CODIGO_DIV = SEL(f'main div.font-mono:has-text("{CODIGO}")')
SWITCH_ROTULO = lambda rotulo: SEL(f'main div.flex:has(> div > label:text-is("{rotulo}")) > button[role=switch]')
SWITCH_TEXTO = lambda texto: SEL(f'main div.flex:has(> div > div > p:text-is("{texto}")) > button[role=switch], main div:has(> div > div > p:text-is("{texto}")) > button[role=switch]')
LINHA = lambda texto: SEL(f'main tbody tr:has-text("{texto}")')
CELULA = lambda texto, n: SEL(f'main tbody tr:has-text("{texto}") td:nth-child({n})')
KPI = lambda rotulo: SEL(f'main div.rounded-lg:has(> div > div > span:text-is("{rotulo}"))')
DRE_LINHA = lambda rotulo: SEL(f'main :is(div,button).flex:has(> span:text-is("{rotulo}"))')
DRE_VALOR = lambda rotulo: SEL(f'main div.flex:has(> span:text-is("{rotulo}")) > span:last-child')
DRE_RESULTADO = SEL('main div.flex:has(> div > div > span:text-is("(=) Resultado do Período"))')
LIXEIRA_FILIAL = SEL('main div.rounded-lg:has(p:text-is("Filial Pindamonhangaba")) button.text-destructive')
ENVIAR_ATIVOS = SEL('main div.rounded-lg:has(p:text-is("Filial Pindamonhangaba")) button:has-text("Enviar Ativos")')
COMBO = lambda txt, esc='main': SEL(f'{esc} button[role=combobox]:has-text("{txt}")')
CAMPO_QTD = SEL('main input[type=number]')
JS_SAIR = "(()=>{const a=document.activeElement;a&&a.blur&&a.blur();return 1})()"


def setup_dash(extra=()):
    """login e, fora do vídeo, as telas do Gerencial (carrega os módulos); termina no Dashboard do EcoSistema"""
    return login() + vai('/gerencial', 'Gerencial') + list(extra)


def js_menu_ger(abrir=True):
    """abre (ou fecha) o grupo "Gerencial (Filiais)" do menu lateral por eval, só se precisar (no setup o `when`/`unless` não vale: lição 155)"""
    return ("(async()=>{const aberto=()=>!!document.querySelector('a[href=\"/gerencial/configuracoes\"]');"
            "const b=[...document.querySelectorAll('button')].find(e=>e.textContent.trim().startsWith('Gerencial (Filiais)'));if(!b)return 'SEM ALVO';"
            f"if(aberto()!=={'true' if abrir else 'false'})b.click();await new Promise(r=>setTimeout(r,500));return aberto()?'aberto':'fechado'}})()")


def abre_menu_ger():
    """abre o grupo "Gerencial (Filiais)" do menu lateral (fora do vídeo), se ainda não estiver aberto"""
    return [{'do': 'eval', 'js': js_menu_ger(True)}, {'do': 'waitFor', 'target': SEL('a[href="/gerencial/configuracoes"]'), 'timeout': 8}]


def fecha_menu_ger():
    return [{'do': 'eval', 'js': js_menu_ger(False)}]


def js_menu_rola(rota, dur_ms=500):
    """rolagem suave (sem cursor) da lista do menu lateral até o item `rota` aparecer inteiro acima do cartão da conta"""
    return ("(async()=>{const a=document.querySelector('a[href=\"%s\"]');if(!a)return 'SEM ALVO';let c=a.parentElement;"
            "while(c&&c!==document.body){const s=getComputedStyle(c);if(/(auto|scroll)/.test(s.overflowY)&&c.scrollHeight>c.clientHeight+4)break;c=c.parentElement;}"
            "if(!c||c===document.body)return 'SEM ROLAGEM';const dy=Math.round(a.getBoundingClientRect().bottom-(c.getBoundingClientRect().bottom-8));"
            "if(dy<=0)return 'ok';const y0=c.scrollTop;" % rota
            + SUAVE.replace('DUR', str(int(dur_ms))).replace('DESTINO', 'y0+dy*e') + "return Math.round(a.getBoundingClientRect().top)})()")


def menu_mostra(rota):
    """rola (sem animação, fora do vídeo) a lista do menu lateral até o item `rota` aparecer inteiro acima do cartão da conta"""
    js = ("(()=>{const a=document.querySelector('a[href=\"%s\"]');if(!a)return 'SEM ALVO';let c=a.parentElement;"
          "while(c&&c!==document.body){const s=getComputedStyle(c);if(/(auto|scroll)/.test(s.overflowY)&&c.scrollHeight>c.clientHeight+4)break;c=c.parentElement;}"
          "if(!c||c===document.body)return 'SEM ROLAGEM';const dy=a.getBoundingClientRect().bottom-(c.getBoundingClientRect().bottom-8);"
          "if(dy>0)c.scrollTop+=dy;return Math.round(a.getBoundingClientRect().top)})()") % rota
    return [{'do': 'eval', 'js': js}]


def cap00():
    """Abertura: Dashboard do EcoSistema da matriz; o cursor abre o grupo "Gerencial (Filiais)" do menu (ilustração na L2)."""
    c = Cap(0, login() + vai('/gerencial', 'Configurar Grupo') + vai('/dashboard', 'Olá, Rafael!') + fecha_menu_ger(), pace=0.6, start=(760, 420))
    c.mark(1)
    c.hover(MENU_GER, 0.4, at=c.A(1, 'gente', 0.6), label='menu Gerencial (Filiais)')
    c.click(MENU_GER, at=c.A(1, 'Recicla', 0.6), label='abre o grupo Gerencial (Filiais)', unless=SEL('a[href="/gerencial/configuracoes"]'))
    c.waitfor(target=SEL('a[href="/gerencial/configuracoes"]'), timeout=8)
    c.ev(js_menu_rola('/gerencial/configuracoes'), label='a lista do menu desce até Configurações (os itens do grupo aparecem)')
    c.hover(LINK_GER('Dashboard', '/gerencial'), 0.2, at=c.A(1, 'Taubaté,', 0.6), label='Dashboard')
    c.hover(LINK_GER('Financeiro', '/gerencial/financeiro'), 0.1, label='Financeiro')
    c.hover(LINK_GER('Estoque', '/gerencial/estoque'), 0.1, label='Estoque')
    c.hover(LINK_GER('Assinaturas', '/gerencial/assinaturas'), 0.1, label='Assinaturas')
    c.hover(LINK_GER('Configurações', '/gerencial/configuracoes'), 0.4, label='Configurações')
    c.mark(2)
    c.mark(3)
    c.hover(MENU_GER, 1.2, at=c.A(3, 'Gerencial.', 0.5), label='Gerencial (Filiais) (cartão Módulo Gerencial)')
    c.mark(4)
    c.fim()
    return c


def cap01():
    """Como o Gerencial funciona: "Dashboard" do grupo Gerencial mostra "Módulo Gerencial" (sem grupo); ilustrações nas L2 a L4."""
    c = Cap(1, login() + vai('/gerencial', 'Configurar Grupo') + vai('/dashboard', 'Olá, Rafael!') + abre_menu_ger(), pace=0.5, start=(720, 300))
    c.mark(1)
    c.click(LINK_GER('Dashboard', '/gerencial'), at=0.1, label='Dashboard do Gerencial (menu)')
    c.waitfor(text='Módulo Gerencial', timeout=15)
    c.hover(TXT('Módulo Gerencial', within=MAIN), 0.4, at=c.A(1, 'começa', 0.5), label='Módulo Gerencial (sem grupo)')
    c.hover(BTNX('Configurar Grupo'), 0.5, at=c.A(1, 'pedindo', 0.4), label='Configurar Grupo')
    c.mark(2)
    c.mark(3)
    c.mark(4)
    c.fim()
    return c


def cap02():
    """Criar o grupo e o código: Configurar Grupo, "Grupo Recicla Vale", Criar Grupo; abas, passo a passo, o botão Como funciona (janela dos
    cinco passos), código de convite e validade, copiar, Unidades Ativas (1/11) só com a matriz. Vira apos-cap02."""
    c = Cap(2, login() + vai('/gerencial/configuracoes', 'Criar Grupo Gerencial') + vai('/gerencial', 'Configurar Grupo'), pace=0.5, start=(700, 300))
    c.mark(1)
    c.click(BTNX('Configurar Grupo'), at=c.A(1, 'Configurar', 0.7), label='Configurar Grupo')
    c.waitfor(text='Criar Grupo Gerencial', timeout=15)
    c.mark(2)
    c.click({'placeholder': 'Ex: Grupo Reciclagem Silva'}, at=c.A(2, 'nome,', 0.6), label='campo Nome do Grupo')
    c.type({'placeholder': 'Ex: Grupo Reciclagem Silva'}, 'Grupo Recicla Vale', at=c.A(2, 'Grupo', 0.05), noClick=True, label='Nome do Grupo: Grupo Recicla Vale')
    c.click(BTN('Criar Grupo'), at=c.A(2, 'Criar', 0.6), label='Criar Grupo')
    c.waitfor(text='Código de Convite', timeout=15)
    c.ev(ANIMA)
    c.mark(3)
    c.hover(TAB('unidades'), 0.3, at=c.A(3, 'Pronto.', 0.3), label='abas do grupo')
    c.hover(TAB('categorias'), 0.1, label='abas do grupo (até Categorias Financeiras)')
    c.hover(TXTP('Configure o grupo', within=MAIN), 1.0, at=c.A(3, 'passo', 0.5), label='passo a passo Configure o grupo')
    c.mark(4)
    c.click(BTNX('Como funciona'), at=c.A(4, 'Como', 0.6), label='Como funciona')
    c.waitfor(text='Relação Matriz × Filial', timeout=8)
    c.hover(TXTP('Como funciona o Gerencial de Filiais', within=DLG), 0.6, at=c.A(4, 'resumo', 0.5), label='janela Como funciona o Gerencial de Filiais')
    c.ev(js_rola_texto('Relação Matriz × Filial', 380, 1800, escopo=DLG), at=c.A(4, 'passos,', 0.2), label='a janela desce pelos cinco passos até Relação Matriz × Filial')
    c.press('Escape', at=round(c.L(5) - 1.5, 2), label='fecha a janela')
    c.mark(5)
    c.ev(js_rola_texto('Código de Convite', 170, 700), at=c.L(5) - 0.9, label='desce até o código de convite')
    c.hover(CODIGO_DIV, 1.0, at=c.A(5, 'código', 0.5), label='código de convite (ZOOM: código e validade)')
    c.hover(TXTP('Válido até', within=MAIN), 1.0, at=c.A(5, 'trinta', 0.5), label='Válido até 10/12/2026')
    c.hover(REGERAR, 1.0, at=c.A(5, 'botão', 0.5), label='botão Gerar novo código')
    c.mark(6)
    c.click(COPIAR, at=c.A(6, 'Copio', 0.6), label='copiar o código')
    c.waitfor(text='Código copiado!', timeout=6)
    c.registra(TXT('Código copiado!'), label='aviso Código copiado!')
    c.mark(7)
    c.ev(js_rola_texto('Nenhuma filial vinculada ainda. Compartilhe o código de convite acima.', 420, 700), at=c.L(7) - 0.9, label='desce até Unidades Ativas')
    c.hover(TXTP('Nenhuma filial vinculada ainda', within=MAIN), 1.2, at=c.A(7, 'unidades', 0.5), label='Unidades Ativas (1/11): só a matriz (ZOOM)')
    c.confere('main', ['Unidades Ativas (1/11)'], 'contador 1/11')
    c.hover(TXTP('Unidades Ativas', within=MAIN), 1.0, at=c.A(7, 'contador:', 0.5), label='o contador 1/11')
    c.fim()
    return c


def cap03():
    """Do lado da filial (Sandra Pires): Configurações (rodapé do menu) › Empresa › cartão Filial; liga É Filial, cola o código e Vincular.
    Vira apos-cap03."""
    c = Cap(3, login(SANDRA_EMAIL, 'Olá, Sandra!') + vai('/configuracoes', 'Configurações do Sistema') + vai('/dashboard', 'Olá, Sandra!'),
            pace=0.5, start=(700, 300))
    c.mark(1)
    c.hover(CONFIG_RODAPE, 0.8, at=c.A(1, 'sistema', 0.6), label='Configurações (rodapé do menu)', noScroll=True)
    c.click(CONFIG_RODAPE, at=c.A(1, 'Configurações,', 0.6), label='Configurações (rodapé do menu)', noScroll=True)
    c.waitfor(text='Configurações do Sistema', timeout=15)
    c.hover(TAB('company'), 0.3, at=c.A(1, 'na', 0.6), label='aba Empresa')
    c.mark(2)
    c.ev(js_rola_texto('Se esta empresa é uma filial, vincule-a à empresa-mãe usando o código de convite', 260, 900), at=c.L(2) - 0.9,
         label='desce até o cartão Filial')
    c.ev(ANIMA)
    c.hover(TXT('Filial', within=MAIN), 0.5, at=c.A(2, 'Filial.', 0.5), label='cartão Filial')
    c.click(SWITCH_ROTULO('É Filial'), at=c.A(2, 'liga', 0.6), label='liga É Filial')
    c.waitfor(target={'placeholder': 'GRP-XXXXXX'}, timeout=6)
    c.mark(3)
    c.click({'placeholder': 'GRP-XXXXXX'}, at=c.A(3, 'cola', 0.6), label='campo do código')
    c.colar('main input[placeholder="GRP-XXXXXX"]', CODIGO, at=c.A(3, 'código', 0.1), label='cola o código GRP-7C4E9A (ZOOM: o campo)')
    c.mark(4)
    c.click(BTNX('Vincular'), at=c.A(4, 'Vincular.', 0.6), label='Vincular')
    c.waitfor(text='Vinculada ao grupo', timeout=10)
    c.hover(TXT('Vinculada ao grupo', within=MAIN), 0.4, at=c.A(4, 'está', 0.5), label='Vinculada ao grupo · Grupo Recicla Vale · Ativa')
    c.mark(5)
    c.fim()
    return c


CODIGO2 = 'GRP-3F81B2'   # regenerate_group_invite_code: o gerador do mundo devolve o primeiro da lista que nenhum grupo usa
# sai da sessão SEM clicar em "Sair" (o "Sair" do rodapé vira o fim do vídeo): tira só as chaves do login e vai para /login; a página recarrega
JS_SAI_SESSAO = ("(()=>{Object.keys(localStorage).filter(k=>k.startsWith('sb-')).forEach(k=>localStorage.removeItem(k));"
                 "setTimeout(()=>location.assign('/login'),50);return 'saindo'})()")


def troca_para_rafael(c, at):
    """Sandra -> Rafael no meio do capítulo (a fala cobre com a ilustração): sai da sessão, entra como Rafael, abre o Gerencial; tudo rápido"""
    c.ev(JS_SAI_SESSAO, at=at, label='troca de usuário: sai da sessão da Sandra (coberto pela ilustração)')
    c.waitfor(target={'label': 'E-mail'}, timeout=25)
    c.type({'label': 'E-mail'}, '$TUT_USER', cps=90, label='troca de usuário: e-mail do Rafael')
    c.type({'label': 'Senha', 'exact': True}, '$TUT_SENHA', cps=90, label='troca de usuário: senha')
    c.click(BTN('Entrar'), label='troca de usuário: Entrar')
    c.waitfor(text='Olá, Rafael!', timeout=30)
    c.add(AGUARDA)
    c.ev(ANIMA_SEMPRE)
    c.ev(OBS)
    c.ev(js_menu_ger(True))
    c.waitfor(target=SEL('a[href="/gerencial/configuracoes"]'), timeout=10)
    c.click(LINK_GER('Configurações', '/gerencial/configuracoes'), label='troca de usuário: Configurações do Gerencial (menu)')
    c.waitfor(text='Código de Convite', timeout=20)
    c.add(AGUARDA)


def cap04():
    """Quando o código não entra: a Sandra cola o código VENCIDO e leva "Código de convite expirado"; (a ilustração cobre a troca de usuário);
    na matriz, o aviso vermelho "Código expirado"; o botão de girar gera GRP-3F81B2, válido por mais 30 dias. Semente codigo-vencido (não segue)."""
    setup = (login(SANDRA_EMAIL, 'Olá, Sandra!') + vai('/configuracoes', 'Configurações do Sistema')
             + [{'do': 'click', 'target': TAB('company')}, {'do': 'waitFor', 'text': 'Filial', 'timeout': 10}, rola_setup('Se esta empresa é uma filial, vincule-a à empresa-mãe usando o código de convite', 260),
                {'do': 'click', 'target': SWITCH_ROTULO('É Filial')}, {'do': 'waitFor', 'target': {'placeholder': 'GRP-XXXXXX'}, 'timeout': 8}, AGUARDA])
    c = Cap(4, setup, pace=0.5, start=(700, 300))
    c.mark(1)
    c.click({'placeholder': 'GRP-XXXXXX'}, at=c.A(1, 'código', 0.6), label='campo do código')
    c.colar('main input[placeholder="GRP-XXXXXX"]', CODIGO, at=c.A(1, 'código', 0.1), label='cola o código GRP-7C4E9A (o vencido)')
    c.click(BTNX('Vincular'), at=c.A(1, 'passou', 0.6), label='Vincular')
    c.waitfor(text='expirado', timeout=10)
    c.registra(TXTP('Código de convite expirado'), label='aviso: Código de convite expirado (ZOOM)')
    c.mark(2)
    troca_para_rafael(c, at=round(c.L(2) + 0.3, 2))
    c.mark(3)
    c.hover(TXTP('Código expirado', within=MAIN), 1.4, at=c.A(3, 'aviso', 0.5), label='⚠ Código expirado em vermelho (ZOOM)')
    c.mark(4)
    c.click(REGERAR, at=c.A(4, 'botão', 0.6), label='Gerar novo código (válido por 30 dias)')
    c.waitfor(text='Código de convite regenerado', timeout=8)
    c.waitfor(text=CODIGO2, timeout=8)
    c.hover(SEL(f'main div.font-mono:has-text("{CODIGO2}")'), 1.0, at=c.A(4, 'novo', 0.5), label=f'o código novo {CODIGO2}')
    c.hover(TXTP('Válido até', within=MAIN), 1.2, at=c.A(4, 'trinta', 0.5), label='Válido até 10/12/2026')
    c.confere('main', [CODIGO2, 'Válido até 10/12/2026'], 'código novo e validade')
    c.fim()
    return c


def setup_ger(url='/gerencial', espera='Dashboard Gerencial', extra=()):
    return login() + vai(url, espera) + list(extra)


POPPER = '[data-radix-popper-content-wrapper]'
SELETOR_UNID = lambda txt: SEL(f'main button:has-text("{txt}")')


def cap05():
    """O Dashboard Gerencial: do menu, Dashboard; Mês passado (e o Personalizado); o seletor de unidades (só a filial e volta a todas);
    cartões Receita Total e Despesa Total; o Lucro Líquido (o resultado da DRE em competência); setinha; Estoque Total; gráfico por unidade."""
    c = Cap(5, setup_ger(extra=vai('/dashboard', 'Olá, Rafael!') + abre_menu_ger()), pace=0.5, start=(700, 300))
    c.mark(1)
    c.click(LINK_GER('Dashboard', '/gerencial'), at=c.A(1, 'Dashboard', 0.7), label='Dashboard do Gerencial (menu)')
    c.waitfor(text='Receita Total', timeout=15)
    c.ev(ANIMA)
    c.hover(TXTP('unidades', within=MAIN), 0.6, at=c.A(1, 'mostra', 0.5), label='Grupo Recicla Vale • 2 unidades')
    c.mark(2)
    c.click(PERIODO('Este mês'), at=c.A(2, 'outubro', 0.6), label='período', noScroll=True)
    c.click(OPT('Mês passado'), at=c.A(2, 'Mês', 0.3), label='Mês passado')
    c.waitfor(text='R$ 344.040,00', timeout=10)
    c.ev(ANIMA)
    c.click(PERIODO('Mês passado'), at=c.A(2, 'atalhos,', 0.8), label='abre o período de novo', noScroll=True)
    c.hover(OPT('Personalizado'), 1.0, at=c.A(2, 'Personalizado', 0.5), label='Personalizado (qualquer intervalo de datas)')
    c.press('Escape', at=round(c.L(3) - 1.6, 2), label='fecha o período (continua em Mês passado)')
    c.mark(3)
    c.click(SELETOR_UNID('Todas as Unidades'), at=c.A(3, 'seletor', 0.6), label='seletor de unidades')
    c.click(SEL(f'{POPPER} button:has-text("Filial Pindamonhangaba")'), at=c.A(3, 'filial,', 0.6), label='marca só a Filial Pindamonhangaba')
    c.press('Escape', label='fecha o seletor')
    c.waitfor(text='R$ 72.000,00', timeout=10)
    c.hover(KPI('Receita Total'), 1.2, at=c.A(3, 'cartões', 0.5), label='só a filial: Receita Total R$ 72.000,00 e Despesa R$ 71.000,00 (ZOOM)')
    c.confere('main', ['R$ 72.000,00', 'R$ 71.000,00'], 'só a filial: receita e despesa')
    c.click(SELETOR_UNID('Filial Pindamonhangaba'), at=c.A(3, 'Financeiro', 0.9), label='seletor de unidades (de novo)')
    c.click(SEL(f'{POPPER} button:has-text("Todas as Unidades")'), label='volta a Todas as Unidades')
    c.press('Escape', label='fecha o seletor')
    c.waitfor(text='R$ 344.040,00', timeout=10)
    c.mark(4)
    c.hover(KPI('Receita Total'), 1.0, at=c.A(4, 'cartões', 0.5), label='cartões Receita Total e Despesa Total (ZOOM)')
    c.hover(KPI('Receita Total'), 0.8, at=c.A(4, 'receita', 0.5), label='Receita Total R$ 344.040,00')
    c.hover(KPI('Despesa Total'), 1.0, at=c.A(4, 'despesa,', 0.5), label='Despesa Total R$ 370.690,00')
    c.confere('main', ['R$ 344.040,00', 'R$ 370.690,00'], 'receita e despesa do grupo em outubro')
    c.mark(5)
    c.hover(KPI('Lucro Líquido'), 1.4, at=c.A(5, 'Lucro', 0.5), label='Lucro Líquido (ZOOM)')
    c.confere('main', ['R$ 18.336,70'], 'Lucro Líquido = resultado da DRE em competência')
    c.mark(6)
    c.hover(SEL('main div.rounded-lg:has(span:text-is("Receita Total")) span.inline-flex'), 0.8, at=c.A(6, 'setinha', 0.5), label='setinha da Receita Total')
    c.hover(KPI('Estoque Total'), 1.0, at=c.A(6, 'Estoque', 0.5), label='Estoque Total')
    c.mark(7)
    c.hover(SEL('main div.space-y-3:has(h2:has-text("Receita vs Despesa por Unidade")) .recharts-surface'), 1.0, at=c.A(7, 'unidade', 0.5),
            label='gráfico Receita vs Despesa por Unidade')
    c.hover(SEL('main .recharts-xAxis text:has-text("★")'), 1.0, at=c.A(7, 'estrela', 0.5), label='a estrela da matriz')
    c.fim()
    return c


def cap06():
    """Ranking e resumo por unidade: Ranking por Saldo (Receita − Despesa; filial na frente, matriz negativa); Resumo por Unidade, linha da matriz e da filial."""
    c = Cap(6, setup_ger(extra=[{'do': 'click', 'target': PERIODO('Este mês')}, {'do': 'click', 'target': OPT('Mês passado')},
                                {'do': 'waitFor', 'text': 'R$ 344.040,00', 'timeout': 10}, AGUARDA]),
            pace=0.5, start=(900, 300))
    c.mark(1)
    c.hover(TXTP('Ranking por Saldo', within=MAIN), 0.8, at=c.A(1, 'ranking', 0.5), label='Ranking por Saldo (Receita − Despesa)')
    c.hover(SEL('main .recharts-yAxis text:has-text("Filial")'), 0.8, at=c.A(1, 'filial', 0.5), label='a filial na frente')
    c.hover(SEL('main .recharts-yAxis text:has-text("Recicla")'), 0.8, at=c.A(1, 'matriz,', 0.5), label='a matriz no vermelho')
    c.mark(2)
    c.ev(js_rola_texto('Resumo por Unidade', 260, 800), at=c.A(2, 'Embaixo', 0.6), label='desce até Resumo por Unidade')
    c.hover(TXTP('Resumo por Unidade', within=MAIN), 0.6, at=c.A(2, 'resumo', 0.4), label='Resumo por Unidade')
    c.mark(3)
    c.hover(LINHA('Recicla Vale Metais'), 1.0, at=c.A(3, 'matriz', 0.5), label='linha da matriz (ZOOM)')
    c.confere('main tbody', ['R$ 272.040,00', 'R$ 299.690,00', 'R$ -27.650,00', '-10.2%'], 'linha da matriz')
    c.hover(CELULA('Recicla Vale Metais', 4), 1.0, at=c.A(3, 'negativa', 0.5), label='lucro da matriz R$ -27.650,00')
    c.mark(4)
    c.hover(LINHA('Filial Pindamonhangaba'), 1.0, at=c.A(4, 'filial', 0.5), label='linha da filial (ZOOM)')
    c.confere('main tbody', ['R$ 72.000,00', 'R$ 71.000,00', 'R$ 1.000,00', '1.4%'], 'linha da filial')
    c.mark(5)
    c.hover(CELULA('Recicla Vale Metais', 4), 1.2, at=c.A(5, 'vermelho', 0.5), label='o vermelho da matriz')
    c.fim()
    return c


def setup_fin(aba='dashboard', periodo=True):
    s = login() + vai('/gerencial/estoque', 'Estoque Gerencial') + vai('/gerencial', 'Dashboard Gerencial')
    if periodo:
        s += vai('/gerencial/financeiro', 'Financeiro Gerencial') + [{'do': 'click', 'target': PERIODO('Este mês')}, {'do': 'click', 'target': OPT('Mês passado')},
                                                                     {'do': 'waitFor', 'text': 'CMV (Custo da Mercadoria Vendida)', 'timeout': 15}, AGUARDA]
    return s


def cap07():
    """A DRE do grupo: Financeiro › DRE › Mês passado (Consolidado); Regime de Caixa: vendas, compras, resultado de caixa; impostos, despesas,
    outras receitas e o resultado do período; Comparativo e a linha Resultado por unidade."""
    c = Cap(7, setup_ger(url='/gerencial/financeiro', espera='Financeiro Gerencial', extra=vai('/gerencial', 'Dashboard Gerencial') + abre_menu_ger()),
            pace=0.5, start=(700, 300), storage_extra={'gerencial-financeiro-tab': 'dre'})
    c.mark(1)
    c.click(LINK_GER('Financeiro', '/gerencial/financeiro'), at=0.1, label='Financeiro do Gerencial (menu)')
    c.waitfor(text='Financeiro Gerencial', timeout=15)
    # o Financeiro abre na aba DRE (a última usada); o período sai de "Este mês" para "Mês passado" enquanto a fala diz "com outubro escolhido"
    c.click(PERIODO('Este mês'), at=c.A(1, 'DRE,', 0.3), label='período', noScroll=True)
    c.click(OPT('Mês passado'), at=c.A(1, 'escolhido,', 0.3), label='Mês passado')
    c.waitfor(text='CMV (Custo da Mercadoria Vendida)', timeout=15)
    c.hover(BTNX('Consolidado'), 0.6, at=c.A(1, 'grupo', 0.5), label='Consolidado: a DRE do grupo')
    c.mark(2)
    c.click({'role': 'tab', 'name': 'Regime de Caixa'}, at=c.A(2, 'caixa,', 0.6), label='Regime de Caixa')
    c.waitfor(text='Compras de Material', timeout=10)
    c.hover(DRE_LINHA('Vendas de Material'), 1.0, at=c.A(2, 'vendeu', 0.6), label='vendas e compras de material (ZOOM)')
    c.hover(DRE_LINHA('Compras de Material'), 1.0, at=c.A(2, 'comprou', 0.5), label='Compras de Material')
    c.confere('main', ['R$ 341.240,00', 'R$ 318.860,00', 'R$ 19.980,00'], 'vendas, compras e resultado de caixa')
    c.mark(3)
    c.ev(js_rola_texto('(-) Impostos e Deduções', 200, 800), at=c.L(3) - 0.9, label='desce até impostos e resultado')
    c.hover(DRE_LINHA('(-) Impostos e Deduções'), 0.3, at=c.A(3, 'impostos', 0.5), label='impostos, despesas, outras receitas e resultado (ZOOM)')
    c.hover(DRE_LINHA('Total Despesas'), 0.8, at=c.A(3, 'despesas', 0.5), label='Total Despesas')
    c.hover(DRE_LINHA('Receitas Diversas (Caixa + Banco)'), 0.8, at=c.A(3, 'aluguel', 0.5), label='Outras Receitas (aluguel de caçamba)')
    c.hover(DRE_RESULTADO, 1.2, at=c.A(3, 'vermelho:', 0.5), label='Resultado do Período')
    c.confere('main', ['R$ 3.574,10', 'R$ 45.855,90', 'R$ 2.800,00', 'R$ 26.650,00', 'Déficit'], 'impostos, despesas, outras receitas e resultado')
    c.mark(4)
    c.ev(js_topo(700), at=c.L(4) - 0.9, label='sobe para o alto da DRE')
    c.click(BTNX('Comparativo'), at=c.A(4, 'Comparativo', 0.6), label='Comparativo')
    c.waitfor(text='DRE Comparativo por Unidade', timeout=10)
    c.ev(js_rola_texto('DRE Comparativo por Unidade', 150, 600), label='desce até a tabela do Comparativo (a linha Resultado aparece)')
    c.mark(5)
    c.hover(LINHA('Resultado'), 0.6, at=c.A(5, 'vermelho', 0.5), label='linha Resultado (ZOOM)')
    c.hover(SEL('main tbody tr:has-text("Resultado") td:nth-child(2)'), 1.0, at=c.A(5, 'matriz,', 0.5), label='Resultado da matriz')
    c.hover(SEL('main tbody tr:has-text("Resultado") td:nth-child(3)'), 1.0, at=c.A(5, 'filial.', 0.5), label='Resultado da filial')
    c.confere('main tbody', ['R$ 27.650,00', 'R$ 1.000,00'], 'Resultado da matriz e da filial')
    c.fim()
    return c


def cap08():
    """Caixa e competência: a DRE do grupo em Regime de Competência (CMV, Lucro Bruto, resultado); depois Caixa e Competência de novo, com a
    câmera no resultado."""
    # roteiro: a DRE já abre em "Regime de Competência" (o padrão); a página desce um pouco para o Lucro Bruto sair de baixo do botão do Cato
    c = Cap(8, setup_fin() + [rola_setup('Vendas de Material', 330)], pace=0.5, start=(700, 300), storage_extra={'gerencial-financeiro-tab': 'dre'})
    c.mark(1)
    c.hover({'role': 'tab', 'name': 'Regime de Competência'}, 0.6, at=c.A(1, 'competência.', 0.5), label='Regime de Competência (o padrão)')
    c.hover(DRE_LINHA('CMV (Custo da Mercadoria Vendida)'), 1.0, at=c.A(1, 'CMV,', 0.5), label='CMV e Lucro Bruto (ZOOM)')
    c.hover(DRE_VALOR('CMV (Custo da Mercadoria Vendida)'), 1.2, at=c.A(1, 'duzentos', 0.5), label='CMV R$ 273.873,30')
    c.confere('main', ['R$ 273.873,30', 'R$ 64.966,70'], 'CMV e Lucro Bruto em competência')
    c.mark(2)
    c.ev(js_rola_texto('(=) Resultado do Período', 420, 800), at=c.L(2) - 0.9, label='desce até o resultado')
    c.hover(DRE_RESULTADO, 1.2, at=c.A(2, 'resultado', 0.5), label='Resultado do Período (ZOOM)')
    c.confere('main', ['R$ 18.336,70', 'Superávit'], 'resultado em competência')
    c.mark(3)
    c.mark(4)
    c.hover(DRE_RESULTADO, 0.4, at=c.L(4) - 0.6, label='o resultado (a câmera fica nele)')
    c.ev(js_clica_texto('Regime de Caixa'), at=c.A(4, 'caixa', 0.1), label='Regime de Caixa (o resultado vai para -R$ 26.650,00)')
    c.ev(js_clica_texto('Regime de Competência'), at=c.A(4, 'competência', 0.1), label='Regime de Competência (volta ao resultado positivo)')
    c.mark(5)
    c.ev(js_topo(600), at=c.L(5) - 0.9, label='sobe para o alto da DRE')
    c.click(BTNX('Comparativo'), at=c.A(5, 'Comparativo', 0.6), label='Comparativo (em competência)')
    c.waitfor(text='DRE Comparativo por Unidade', timeout=10)
    c.ev(js_rola_texto('DRE Comparativo por Unidade', 150, 600), label='desce até a tabela do Comparativo')
    # em competência a linha se chama "CMV" (em caixa, "Compras"); cada unidade chama a mesma RPC com a unidade sozinha e mostra o CMV dela
    c.waitfor(text='(-) CMV', timeout=12)
    c.hover(SEL('main tbody tr:has-text("(-) CMV")'), 2.5, at=c.A(5, 'CMV', 0.6), label='linha CMV de cada unidade (ZOOM)')
    c.confere('main tbody', ['(-) CMV'], 'linha CMV do Comparativo')
    c.mark(6)
    c.fim()
    return c


def cap09():
    """Além da DRE: as linhas da DRE que abrem (Total Despesas); o Exportar (sem clicar) e o Patrimônio Operacional Atual; a aba Dashboard (por
    categoria); a aba Histórico (Receitas, Despesas, Compras) com o filtro Conta bancária. Semente apos-cap03."""
    c = Cap(9, setup_fin() + [rola_setup('Vendas de Material', 330)], pace=0.5, start=(700, 300), storage_extra={'gerencial-financeiro-tab': 'dre'})
    c.mark(1)
    c.ev(js_rola_texto('Total Despesas', 300, 800), at=c.L(1) + 1.0, label='desce até Total Despesas')
    c.click(DRE_LINHA('Total Despesas'), at=c.A(1, 'despesas', 0.6), label='abre Total Despesas (as categorias)')
    c.hover(DRE_LINHA('Total Despesas'), 1.2, at=c.A(1, 'mostram', 0.5), label='as categorias da despesa (ZOOM)')
    c.mark(2)
    c.click(DRE_LINHA('Total Despesas'), at=round(c.L(2) - 0.6, 2), label='fecha Total Despesas')
    c.ev(js_topo(600), at=c.L(2) - 0.4, label='sobe ao alto da DRE')
    c.hover(BTNX('Exportar'), 1.4, at=c.A(2, 'Exportar', 0.6), label='Exportar (ZOOM, sem clicar)')
    c.ev(js_rola_texto('Patrimônio Operacional Atual', 380, 900), at=c.A(2, 'embaixo,', 0.6), label='desce até o Patrimônio Operacional Atual')
    c.click(TXTP('Patrimônio Operacional Atual', within=MAIN), at=c.A(2, 'Patrimônio', 0.6), label='abre o Patrimônio Operacional Atual')
    c.hover(TXTP('Contas a Receber', within=MAIN), 1.2, at=c.A(2, 'receber,', 0.5), label='Saldo em Caixa, Saldo Bancário, Contas a Receber, Estoque e Contas a Pagar (ZOOM)')
    c.mark(3)
    c.ev(js_topo(500), at=c.L(3) - 0.9, label='sobe')
    c.click(TAB('dashboard'), at=c.A(3, 'Dashboard', 0.6), label='aba Dashboard')
    c.waitfor(text='Despesas por Categoria', timeout=12)
    c.hover(TXTP('Despesas por Categoria', within=MAIN), 1.0, at=c.A(3, 'gasta', 0.5), label='Despesas por Categoria')
    c.hover(TXTP('Receitas por Categoria', within=MAIN), 1.0, at=c.A(3, 'receita,', 0.5), label='Receitas por Categoria')
    c.mark(4)
    c.click(TAB('historico'), at=c.A(4, 'Histórico', 0.6), label='aba Histórico')
    c.waitfor(text='Compras', timeout=12)
    c.hover(SEL('main [role=tab]:has-text("Compras")'), 0.8, at=c.A(4, 'lançamentos', 0.5), label='Receitas, Despesas e Compras')
    c.click(SEL('main button:has-text("Filtros")'), at=c.A(4, 'filtrar', 0.6), label='Filtros')
    c.waitfor(text='Conta bancária', timeout=8)
    c.click(SEL('[role=dialog] button[role=combobox]:has-text("Todas as contas")'), at=c.A(4, 'conta', 0.6), label='Conta bancária')
    c.hover(SEL('[role=option]:not(:has-text("Todas as contas"))'), 1.2, at=c.A(4, 'bancária', 0.3), label='as contas das unidades (ZOOM)')
    c.press('Escape', label='fecha a lista')
    c.fim()
    return c


DATA_BTN = lambda d: SEL(f"main button:has(svg.lucide-calendar):has-text('{d}')")
POP = '[data-radix-popper-content-wrapper]'
PREV_MES = SEL(f"{POP} button[name='previous-month']")
DIA = lambda d: SEL(f"{POP} button[name='day']:text-is('{d}')")
HORA = SEL("main input[aria-label='Hora']")


def cap10():
    """O estoque do grupo: Visão Geral (as duas unidades, latinha 640 + 1.850); Posição de Estoque em 31/10 (Ver posição, a linha abre por unidade,
    Por unidade); Histórico de Materiais com Filtros (material Alumínio latinha); Relatório de Estoque (o cartão Total Comprado abre, a linha do
    material abre por unidade, Usuários, Ocultar itens zerados, Exportar Relatório, sem clicar)."""
    c = Cap(10, setup_ger(url='/gerencial/estoque', espera='Estoque Gerencial', extra=vai('/gerencial', 'Dashboard Gerencial') + abre_menu_ger()),
            pace=0.5, start=(700, 300), storage_extra={'gerencial-estoque-tab': 'visao-geral'})
    c.mark(1)
    c.click(LINK_GER('Estoque', '/gerencial/estoque'), at=c.A(1, 'estoque.', 0.7), label='Estoque do Gerencial (menu)')
    c.waitfor(text='Tabela Unificada de Materiais', timeout=15)
    c.ev(ANIMA)
    c.hover(TAB('visao-geral'), 0.6, at=c.A(1, 'Visão', 0.5), label='Visão Geral')
    c.mark(2)
    c.hover(TXTP('Tabela Unificada de Materiais', within=MAIN), 0.6, at=c.A(2, 'tabela,', 0.4), label='Tabela Unificada de Materiais')
    c.hover(TXT('Filial Pindamonhangaba', within='main thead'), 0.6, at=c.A(2, 'unidade', 0.5), label='uma coluna por unidade')
    c.hover(LINHA('Alumínio latinha'), 1.0, at=c.A(2, 'alumínio', 0.5), label='linha do alumínio latinha (ZOOM)')
    c.confere('main tbody', ['640', '1.850', '2.490'], 'latinha 640, 1.850 e 2.490 kg')
    c.mark(3)
    c.click(TAB('posicao'), at=c.A(3, 'Posição', 0.6), label='Posição de Estoque')
    c.waitfor(text='Ver posição', timeout=10)
    c.click(DATA_BTN('10/11/2026'), at=c.A(3, 'Escolho', 0.6), label='data (abre o calendário de novembro)')
    c.waitfor(target=PREV_MES, timeout=6)
    c.click(PREV_MES, at=c.A(3, 'trinta', 0.4), label='mês anterior (outubro)')
    c.click(DIA('31'), at=c.A(3, 'outubro', 0.3), label='dia 31')
    c.registra(DATA_BTN('31/10/2026'), label='[ZOOM] Data e hora: 31/10/2026 (padrão 23:59)')
    c.click(BTN('Ver posição'), at=c.A(3, 'clico', 0.6), label='Ver posição')
    c.waitfor(text='31/10/2026 23:59', timeout=15)
    c.hover(TXT('Valor em estoque', within=MAIN), 1.0, at=c.A(3, 'custo', 0.6), label='cartões Saldo total, Valor em estoque e Projeção de venda (ZOOM)')
    c.mark(4)
    c.click(LINHA('Alumínio latinha'), at=c.A(4, 'material,', 0.6), label='abre o material: as duas unidades')
    c.hover(LINHA('Alumínio latinha'), 0.8, at=c.A(4, 'unidade', 0.5), label='unidade por unidade')
    c.click(BTN('Por unidade'), at=c.A(4, 'Por', 0.6, nth=0), label='Por unidade (a tabela inteira)')
    c.mark(5)
    c.click(TAB('historico'), at=c.A(5, 'Histórico', 0.6), label='Histórico de Materiais')
    c.waitfor(text='Filtros', timeout=10)
    c.click(SEL('main button:has-text("Filtros")'), at=c.A(5, 'Filtros', 0.6), label='Filtros')
    c.hover(TXT('Período', within=MAIN), 0.6, at=c.A(5, 'período', 0.5), label='Período')
    c.click(SEL('main button:has-text("Material")'), at=c.A(5, 'material.', 0.9), label='Material (lista)')
    c.click(SEL('[data-radix-popper-content-wrapper] label:has-text("Alumínio latinha")'), label='escolhe Alumínio latinha')
    c.press('Escape', label='fecha a lista')
    c.hover(SEL('main tbody tr:first-child'), 1.0, at=c.A(5, 'Cada', 0.5), label='as linhas: Compra, Venda e Transferência, com a Filial (ZOOM)')
    c.mark(6)
    c.click(TAB('relatorio'), at=c.A(6, 'Relatório', 0.6), label='Relatório de Estoque')
    c.waitfor(text='Total Comprado', timeout=12)
    c.click(SEL('main button[aria-label="Total Comprado"], main [aria-label="Total Comprado"]'), at=c.A(6, 'Total', 0.6), label='abre o cartão Total Comprado')
    c.hover(TXTP('Distribuição por forma de pagamento', within=MAIN), 1.6, at=c.A(6, 'preço', 0.6), label='Preço médio de compra e Distribuição por forma de pagamento (ZOOM)')
    c.mark(7)
    c.click(LINHA('Alumínio latinha'), at=c.A(7, 'linha', 0.6), label='abre a linha do material por unidade')
    c.hover(LINHA('Alumínio latinha'), 1.4, at=c.A(7, 'unidade', 0.5), label='Preço Médio Compra de cada unidade (ZOOM)')
    c.mark(8)
    c.hover(TXTP('Usuários', within=MAIN), 0.7, at=c.A(8, 'usuário,', 0.6), label='filtro Usuários')
    c.hover(TXTP('Ocultar itens zerados', within=MAIN), 0.7, at=c.A(8, 'esconder', 0.6), label='Ocultar itens zerados')
    c.hover(TXTP('Exportar Relatório', within=MAIN), 1.0, at=c.A(8, 'exportar', 0.6), label='Exportar Relatório (sem clicar)')
    c.fim()
    return c


ACOES_MAT = lambda nome: SEL(f'main button[aria-label^="Ações de {nome}"]')
ITEM_MENU = lambda nome: SEL(f'[role=menuitem]:has-text("{nome}")')


def cap11():
    """Corrigir o estoque de uma unidade: Estoque Gerencial › Visão Geral › ⋯ da linha Papelão › Corrigir saldo (Unidade: Filial Pindamonhangaba,
    Saída de 30, motivo, Registrar saída); depois Transferir entre materiais (só a janela, Cancelar). A ilustração do aviso de divergência é da
    coordenação. Semente apos-cap03 (não segue)."""
    c = Cap(11, setup_ger(url='/gerencial/estoque', espera='Tabela Unificada de Materiais', extra=vai('/gerencial', 'Dashboard Gerencial') + abre_menu_ger()
                          + vai('/gerencial/estoque', 'Tabela Unificada de Materiais')),
            pace=0.5, start=(700, 300), storage_extra={'gerencial-estoque-tab': 'visao-geral'})
    c.mark(1)
    c.hover(LINHA('Papelão'), 0.8, at=c.A(1, 'papelão', 0.5), label='a linha do Papelão')
    c.click(ACOES_MAT('Papelão'), at=c.A(1, 'menu', 0.6), label='⋯ da coluna Ações do Papelão')
    c.waitfor(target=ITEM_MENU('Corrigir saldo'), timeout=6)
    c.hover(ITEM_MENU('Transferir entre materiais'), 0.8, at=c.A(1, 'ações', 0.5), label='Corrigir saldo, Transferir entre unidades, Transferir entre materiais')
    c.mark(2)
    c.click(ITEM_MENU('Corrigir saldo'), at=c.A(2, 'Corrigir', 0.6), label='Corrigir saldo')
    c.waitfor(text='Ajuste de entrada ou saída em Papelão', timeout=8)
    c.ev(ANIMA)
    c.click(SEL(f'{DLG} #adjust-unit'), at=c.A(2, 'Escolho', 0.6), label='Unidade')
    c.click(SEL('[role=option]:has-text("Filial Pindamonhangaba")'), at=c.A(2, 'filial.', 0.5), label='Unidade: Filial Pindamonhangaba')
    c.mark(3)
    c.click(SEL(f'{DLG} button:has-text("Saída")'), at=c.A(3, 'saída', 0.6), label='Saída')
    c.click(SEL(f'{DLG} #adjust-quantity'), at=c.A(3, 'trinta', 0.6), label='Quantidade')
    c.type(SEL(f'{DLG} #adjust-quantity'), '30', at=c.A(3, 'trinta', 0.05), noClick=True, label='Quantidade 30')
    c.hover(TXT('Depois do ajuste', within=DLG), 1.4, at=c.A(3, 'saldo', 0.5), label='Saldo atual e Depois do ajuste (ZOOM)')
    c.confere('dlg', ['Saldo atual', 'Depois do ajuste', '__LER__'], 'LER: saldo atual e depois do ajuste do Papelão na filial')
    c.mark(4)
    c.click(SEL(f'{DLG} #adjust-description'), at=c.A(4, 'Escrevo', 0.6), label='Motivo da correção')
    c.colar(f'{DLG} #adjust-description'.replace('[role=dialog]', '[role=dialog]'), 'Inventário conferido no pátio', at=c.A(4, 'motivo.', 0.2), label='Motivo: Inventário conferido no pátio')
    c.hover(TXTP('A correção fica no kardex da unidade', within=DLG), 1.6, at=c.A(4, 'correção', 0.5), label='A correção fica no kardex da unidade (ZOOM)')
    c.mark(5)
    c.click(SEL(f'{DLG} button:has-text("Registrar saída")'), at=c.A(5, 'Registrar', 0.6), label='Registrar saída')
    c.waitfor(text='Saída de 30', timeout=10)
    c.registra(TXTP('Saída de 30'), label='aviso: Saída de 30 kg de Papelão')
    c.mark(6)
    c.click(ACOES_MAT('Papelão'), at=c.A(6, 'menu,', 0.6), label='⋯ da linha Papelão (de novo)')
    c.click(ITEM_MENU('Transferir entre materiais'), at=c.A(6, 'Transferir', 0.6), label='Transferir entre materiais')
    c.waitfor(text='Move saldo de', timeout=8)
    c.hover(TXTP('Move saldo de', within=DLG), 1.4, at=c.A(6, 'passa', 0.5), label='Move saldo de Papelão para outro material da MESMA unidade (ZOOM)')
    c.click(BTN('Cancelar', within=DLG), at=round(c.L(7) - 1.2, 2), label='Cancelar')
    c.mark(7)
    c.fim()
    return c


LINHA_CAT = lambda nome: SEL(f'main div.rounded-lg:has(p:text-is("{nome}"))')


def cap12():
    """Enviar Ativos: Configurações do grupo (o passo a passo) › Catálogo (Importar do Estoque da Matriz; Sucata eletrônica entra e sai pela lixeira),
    Tabelas de Preço (entram sozinhas), Clientes e Fornecedores (marca a Fundição; Fornecedores com busca: marca e desmarca a Cooperativa Recomeço),
    Categorias (o cadeado); Unidades › Enviar Ativos (Desmarcar todos, Marcar todos, Sobrescrever desligado) › Confirmar Envio; Histórico de Envios;
    a lixeira da filial (sem clicar). Vira apos-cap09."""
    c = Cap(12, setup_ger(url='/gerencial/configuracoes', espera='Código de Convite',
                          extra=vai('/gerencial', 'Dashboard Gerencial') + abre_menu_ger() + menu_mostra('/gerencial/configuracoes')),
            pace=0.5, start=(700, 300))
    c.mark(1)
    c.click(LINK_GER('Configurações', '/gerencial/configuracoes'), at=c.A(1, 'padronização.', 0.7), label='Configurações do Gerencial (menu)')
    c.waitfor(text='Código de Convite', timeout=15)
    c.hover(TXTP('etapas concluídas', within=MAIN), 1.2, at=c.A(1, 'passo', 0.5), label='passo a passo Configure o grupo (cada etapa leva à aba)')
    c.click(TAB('materiais'), at=c.A(1, 'catálogo', 0.6), label='Catálogo de Materiais')
    c.waitfor(text='Importar do Estoque da Matriz', timeout=10)
    c.mark(2)
    c.click(BTNX('Importar do Estoque da Matriz'), at=c.A(2, 'Importar', 0.6), label='Importar do Estoque da Matriz')
    c.waitfor(text='importado(s) do estoque', timeout=10)
    c.hover(TXT('Alumínio latinha', within=MAIN), 0.8, at=c.A(2, 'materiais', 0.5), label='os materiais da matriz no catálogo')
    c.mark(3)
    c.click({'placeholder': 'Ex: Papelão'}, at=c.A(3, 'dar', 0.6), label='Nome do Material')
    c.type({'placeholder': 'Ex: Papelão'}, 'Sucata eletrônica', at=c.A(3, 'nome', 0.5), noClick=True, label='Nome do Material: Sucata eletrônica')
    c.click(SEL('main button:has(svg.lucide-plus)'), at=c.A(3, 'unidade.', 0.6), label='+ (adiciona ao catálogo)')
    c.waitfor(text='Material adicionado ao catálogo', timeout=8)
    c.hover(LINHA_CAT('Sucata eletrônica'), 1.0, at=c.A(3, 'vínculos', 0.5), label='Sucata eletrônica: Sem vínculos (ZOOM)')
    c.click(SEL('main div.rounded-lg:has(p:text-is("Sucata eletrônica")) button.text-destructive'), at=c.A(3, 'lixeira', 0.6), label='lixeira (tira do catálogo)')
    c.waitfor(text='Material removido do catálogo', timeout=8)
    c.mark(4)
    c.click(TAB('precos'), at=c.A(4, 'tabelas', 0.6), label='Tabelas de Preço')
    c.hover(TXTP('Tabelas de Preço do Grupo', within=MAIN), 1.0, at=c.A(4, 'sozinhas,', 0.5), label='as tabelas da matriz entram sozinhas')
    c.mark(5)
    c.click(TAB('clientes'), at=c.A(5, 'Clientes', 0.6), label='Clientes e Fornecedores')
    c.hover(TXT('Fundição Bandeira do Vale', within=MAIN), 0.8, at=c.A(5, 'Fundição', 0.5), label='Fundição Bandeira do Vale')
    c.click(TXT('Fundição Bandeira do Vale', within=MAIN), at=c.A(5, 'então', 0.6), label='marca a Fundição Bandeira do Vale')
    c.waitfor(text='Disponibilizado para filiais', timeout=8)
    c.mark(6)
    c.click(SEL('main button:has-text("Fornecedores (")'), at=c.A(6, 'fornecedores', 0.6), label='aba Fornecedores')
    c.type({'placeholder': 'Buscar...'}, 'Coop', at=c.A(6, 'busca.', 0.8), label='busca: Coop')
    c.click(TXT('Cooperativa Recomeço', within=MAIN), at=c.A(6, 'Marcou,', 0.6), label='marca a Cooperativa Recomeço')
    c.waitfor(text='Disponibilizado para filiais', timeout=8)
    c.hover(TXTP('disponibilizado(s) para filiais', within=MAIN), 0.8, at=c.A(6, 'disponível.', 0.4), label='n de n disponibilizado(s) para filiais')
    c.click(TXT('Cooperativa Recomeço', within=MAIN), at=c.A(6, 'Desmarcou,', 0.6), label='desmarca a Cooperativa Recomeço')
    c.waitfor(text='Removido das filiais', timeout=8)
    c.mark(7)
    c.click(TAB('categorias'), at=c.A(7, 'categorias', 0.6), label='Categorias Financeiras')
    c.waitfor(text='Categorias usadas no DRE', timeout=10)
    c.hover(SEL('main svg.lucide-lock'), 1.4, at=c.A(7, 'cadeado', 0.5), label='o cadeado: Categoria obrigatória — usada no DRE (ZOOM)')
    c.mark(8)
    c.click(TAB('unidades'), at=c.A(8, 'Com', 0.3), label='Unidades')
    c.ev(js_rola_texto('Filial Pindamonhangaba', 360, 700), label='desce até a filial')
    c.click(ENVIAR_ATIVOS, at=c.A(8, 'Enviar', 0.9), label='Enviar Ativos')
    c.waitfor(text='Confirmar Envio', timeout=8)
    c.click(SEL(f'{DLG} button:has-text("Desmarcar todos")'), at=c.A(8, 'desmarcar', 0.6), label='Desmarcar todos')
    c.click(SEL(f'{DLG} button:has-text("Marcar todos")'), at=c.A(8, 'Aqui', 0.6), label='Marcar todos')
    c.mark(9)
    c.hover(TXT('Materiais', within=DLG), 0.6, at=c.A(9, 'tinha', 0.5), label='Materiais, Categorias, Tabelas, Clientes, Fornecedores')
    c.hover(TXT('Sobrescrever preços existentes', within=DLG), 1.6, at=c.A(9, 'Sobrescrever', 0.5), label='Sobrescrever preços existentes (desligado)')
    c.mark(10)
    c.click(BTN('Confirmar Envio'), at=c.A(10, 'Confirmar', 0.6), label='Confirmar Envio')
    c.waitfor(text='novo(s)', timeout=10)
    c.hover(TXT('Materiais', within=DLG), 0.6, at=c.A(10, 'mesmo', 0.5), label='n novo(s) por linha')
    c.click(BTN('Fechar', within=DLG), at=round(c.L(11) - 1.0, 2), label='Fechar')
    c.mark(11)
    c.ev(js_rola_texto('Histórico de Envios', 300, 800), at=c.L(11) - 0.5, label='desce até o Histórico de Envios')
    c.hover(TXTP('Histórico de Envios', within=MAIN), 0.8, at=c.A(11, 'Histórico', 0.5), label='Histórico de Envios')
    c.hover(SEL('main div.bg-muted\\/30:has(svg.lucide-send)'), 1.6, at=c.A(11, 'filial', 0.5, nth=0), label='a linha do envio: Filial, o que foi enviado e a data (ZOOM)')
    c.mark(12)
    c.ev(js_rola_texto('Filial Pindamonhangaba', 360, 700), at=c.L(12) - 0.9, label='sobe até a filial')
    c.hover(LIXEIRA_FILIAL, 1.5, at=c.A(12, 'tirar', 0.5), label='lixeira da linha da filial (ZOOM, sem clicar)')
    c.fim()
    return c


CAIXA_UNID = lambda nome: f'main div.rounded-lg:has(> div > span:text-is("{nome}"))'


def cap13():
    """Preço diferente por unidade: Configurações do grupo › Tabelas de Preço › a tabela Principal (a grade de preços); Alumínio latinha: compra
    6,20 -> 6,30 e Salvar; Vinculação por Unidade: liga a Filial Pindamonhangaba, Tipo %, Direção - (abaixo), Valor 5, Salvar; Aplicar; zoom em
    Importar da matriz e Excluir (sem clicar). Semente apos-cap09 (não segue: o cap14 parte do mesmo estado)."""
    c = Cap(13, setup_ger(url='/gerencial/configuracoes', espera='Código de Convite',
                          extra=[{'do': 'waitFor', 'text': 'Código de Convite', 'timeout': 20}, AGUARDA, {'do': 'click', 'target': TAB('precos')}, {'do': 'waitFor', 'text': 'Tabelas de Preço do Grupo', 'timeout': 10}, AGUARDA]),
            pace=0.5, start=(700, 300))
    c.mark(1)
    c.click(SEL('main div.cursor-pointer:has-text("Principal")'), at=c.A(1, 'Abrindo', 0.6), label='abre a tabela Principal')
    c.waitfor(text='Preço Compra (R$)', timeout=10)
    c.hover(TXT('Preço Venda (R$)', within=MAIN), 1.2, at=c.A(1, 'compra', 0.5), label='Material, Preço Compra e Preço Venda (ZOOM)')
    c.mark(2)
    c.ev(js_rola_texto('Alumínio latinha', 330, 700), at=c.L(2) - 0.9, label='desce até a linha do Alumínio latinha')
    c.click(SEL('main tbody tr:has-text("Alumínio latinha") td:nth-child(2) input'), at=c.A(2, 'compra', 0.6), label='Preço Compra da latinha')
    c.type(SEL('main tbody tr:has-text("Alumínio latinha") td:nth-child(2) input'), '6,30', at=c.A(2, 'seis', 0.1), noClick=True, clear=True, label='compra 6,30 (ZOOM: a linha)')
    c.click(SEL('main tbody tr:has-text("Alumínio latinha") button:has-text("Salvar")'), at=c.A(2, 'salvo.', 0.6), label='Salvar')
    c.waitfor(text='Preço atualizado', timeout=8)
    c.mark(3)
    c.ev(js_rola_texto('Vinculação por Unidade', 220, 800), at=c.L(3) - 0.9, label='desce até a Vinculação por Unidade')
    c.hover(TXT('Vinculação por Unidade', within=MAIN), 0.8, at=c.A(3, 'Vinculação', 0.5), label='Vinculação por Unidade')
    c.click(SEL(CAIXA_UNID('Filial Pindamonhangaba') + ' button[role=switch]'), at=c.A(3, 'Ligo', 0.6), label='liga a Filial Pindamonhangaba: Vinculada')
    c.waitfor(text='Direção', timeout=8)
    c.mark(4)
    c.click(SEL(CAIXA_UNID('Filial Pindamonhangaba') + ' div:has(> label:text-is("Direção")) button[role=combobox]'), at=c.A(4, 'Direção,', 0.6), label='Direção')
    c.click(SEL('[role=option]:has-text("- (abaixo)")'), at=c.A(4, 'abaixo', 0.5, nth=1), label='- (abaixo)')
    c.type(SEL(CAIXA_UNID('Filial Pindamonhangaba') + ' input[type=number]'), '5', at=c.A(4, 'cinco', 0.7, nth=1), clear=True, label='Valor 5 (ZOOM: os três campos)')
    c.click(SEL(CAIXA_UNID('Filial Pindamonhangaba') + ' button:has-text("Salvar")'), at=c.A(4, 'Salvar.', 0.6), label='Salvar')
    c.waitfor(text='Configuração atualizada', timeout=8)
    c.mark(5)
    c.click(SEL(CAIXA_UNID('Filial Pindamonhangaba') + ' button:has-text("Aplicar")'), at=c.A(5, 'Aplicar', 0.6), label='Aplicar')
    c.waitfor(text='aplicado(s) à unidade', timeout=8)
    c.confere('body', ['15 preço(s) aplicado(s) à unidade'], 'preços aplicados à filial')
    c.mark(6)
    c.mark(7)
    ev_topo = js_rola_texto('Preço Compra (R$)', 300, 700)
    c.ev(ev_topo, at=c.L(7) - 0.9, label='sobe até a barra de ações da tabela')
    c.hover(SEL('main button[role=combobox]:has-text("Importar da matriz")'), 1.0, at=c.A(7, 'puxa', 0.5), label='Importar da matriz... (ZOOM, sem escolher)')
    c.hover(SEL('main button.bg-destructive:has-text("Excluir"), main button:has-text("Excluir")'), 1.5, at=c.A(7, 'Excluir', 0.5, nth=0), label='o botão vermelho Excluir (ZOOM, sem clicar)')
    c.fim()
    return c


def cap14():
    """Transferência com aprovação: aba Transferências, liga "Exigir aprovação"; Nova: filial -> matriz, alumínio latinha 1.200 kg,
    observação; Solicitar; Pendente; Executar; Confirmar e Executar; o Estoque Gerencial com 1.840 e 650 kg. Vira apos-cap10."""
    c = Cap(14, setup_ger(url='/gerencial/estoque', espera='Estoque Gerencial',
                          extra=vai('/gerencial/configuracoes', 'Código de Convite') + abre_menu_ger()), pace=0.5, start=(700, 300),
            storage_extra={'gerencial-estoque-tab': 'visao-geral'})
    c.mark(1)
    c.click(TAB('transferencias'), at=c.A(1, 'transferências.', 0.6), label='aba Transferências')
    c.waitfor(text='Exigir aprovação em transferências', timeout=8)
    c.click(SWITCH_TEXTO('Exigir aprovação em transferências'), at=c.A(1, 'ligo', 0.6), label='liga Exigir aprovação em transferências')
    c.mark(2)
    c.click(BTN('Nova'), at=c.A(2, 'Nova,', 0.6), label='Nova')
    c.waitfor(text='Unidade de origem...', timeout=8)
    # o formulário abre embaixo dos dois cartões de configuração (Origem e Destino em y~770): a página desce até o título dele
    c.ev(js_rola_texto('Nova transferência em lote', 140, 500), label='desce até Nova transferência em lote')
    c.click(COMBO('Unidade de origem...'), at=c.A(2, 'origem', 0.6), label='Origem')
    c.click(OPT('Filial Pindamonhangaba'), at=c.A(2, 'filial', 0.3), label='Origem: Filial Pindamonhangaba')
    c.click(COMBO('Unidade de destino...'), at=c.A(2, 'destino,', 0.6), label='Destino')
    c.click(OPT('Recicla Vale Metais'), at=c.A(2, 'matriz.', 0.3), label='Destino: Recicla Vale Metais')
    c.mark(3)
    c.type({'placeholder': 'Buscar material...'}, 'latinha', at=c.A(3, 'material', 0.6), label='busca latinha')
    c.click(SEL('main label:has-text("Alumínio latinha") button[role=checkbox]'), at=c.A(3, 'alumínio', 0.6), label='marca Alumínio latinha')
    c.click(CAMPO_QTD, at=c.A(3, 'mil', 0.6), label='campo Quantidade')
    # o campo já vem com o saldo da origem (1.850): limpa (Ctrl+A, Backspace) antes de digitar
    c.type(CAMPO_QTD, '1200', at=c.A(3, 'mil', -0.2), noClick=True, clear=True, label='Quantidade 1200 (ZOOM)')
    c.mark(4)
    c.click({'placeholder': 'Ex: Transferência para suprir demanda...'}, at=c.L(4) - 0.2, label='Observações')
    c.colar('main textarea', 'Lote para a Serra Fina Alumínio Reciclagem', label='Observações: Lote para a Serra Fina Alumínio Reciclagem')
    c.hover(TXTP('Este grupo exige aprovação', within=MAIN), 1.2, at=c.A(4, 'aviso', 0.5), label='aviso do resumo')
    c.click(BTNX('Solicitar 1 transferência'), at=c.A(4, 'Solicitar', 0.6), label='Solicitar 1 transferência')
    c.waitfor(text='Pendente', timeout=10)
    # o formulário fecha e a página volta ao alto: a linha pendente fica no pé, com os botões embaixo do aviso "Solicitação criada"
    c.ev(js_rola_texto('Transferências Inter-Unidades', 150, 600), label='desce até a transferência pendente')
    c.mark(5)
    c.hover(TXT('Pendente', within=MAIN), 1.0, at=c.A(5, 'pendente.', 0.5), label='Pendente')
    c.click(BTN('Executar'), at=c.A(5, 'Executar.', 0.6), label='Executar')   # exato: "Executar todas (1)" vem antes no cabeçalho
    c.waitfor(text='Confirmar execução?', timeout=8)
    c.hover(TXTP('Este grupo exige aprovação antes de executar', within=ALERTA), 1.2, at=c.A(5, 'confirmar', 0.5), label='Confirmar execução? (destino de acordo)')
    c.mark(6)
    c.click(BTN('Confirmar e Executar'), at=c.A(6, 'Confirmar', 0.6), label='Confirmar e Executar')
    c.waitfor(text='Concluída', timeout=10)
    c.hover(TXT('Concluída', within=MAIN), 0.6, at=c.A(6, 'Pronto:', 0.5), label='Concluída')
    c.click(LINK_GER('Estoque', '/gerencial/estoque'), at=c.A(6, 'matriz', 0.6), label='Estoque do Gerencial (menu)')
    c.waitfor(text='Tabela Unificada de Materiais', timeout=12)
    c.hover(LINHA('Alumínio latinha'), 1.0, at=c.A(6, 'quarenta', 0.5), label='latinha: 1.840 na matriz e 650 na filial (ZOOM)')
    c.confere('main tbody', ['1.840', '650', '2.490'], 'latinha 1.840, 650 e 2.490 kg')
    c.mark(7)
    c.fim()
    return c


JS_DESMARCA_MENOS = ("(()=>{const alvo=%s;let n=0;document.querySelectorAll('main label').forEach(l=>{const cb=l.querySelector('button[role=checkbox]');"
                     "if(cb&&cb.getAttribute('data-state')==='checked'&&!l.innerText.includes(alvo)){cb.click();n++}});return n})()")
CARTAO_TRANSF = lambda mat: f'main div.p-3.rounded-lg:has(span:has-text("{mat}"))'


def cap15():
    """Lote, fila e o pedido da filial: a Sandra marca Papelão e Plástico PET no Materiais e pede a transferência (Transferir Estoque › Enviar 2
    Transferência(s)); (a ilustração cobre a troca para o Rafael); na matriz, Estoque Gerencial › Transferências (contador); Nova: lote (Selecionar
    todos com saldo; só Ferro misto; quantidade acima do saldo avisa; 500 kg; Solicitar); Cancelar o Plástico PET; Executar todas (2); Visão Geral › ⋯ do
    Inox › Transferir entre unidades. Semente apos-cap10 (não segue)."""
    setup = login(SANDRA_EMAIL, 'Olá, Sandra!') + vai('/materiais', 'Materiais') + [AGUARDA]
    c = Cap(15, setup, pace=0.5, start=(700, 300))
    c.mark(1)
    # a tabela mostra 10 materiais por página: "Itens por página" em 25 põe o Papelão e o Plástico PET (14 e 15) à vista (a busca não serve: a
    # janela do lote só leva os materiais que a busca está mostrando)
    c.click(SEL('main div:has(> span:text-is("Itens por página:")) button[role=combobox]'), at=c.A(1, 'estoque', 0.3), label='Itens por página')
    c.click(OPT('25'), label='25 por página')
    c.click(SEL('main tbody tr:has-text("Papelão") button[role=checkbox]'), label='marca o Papelão')
    c.click(SEL('main tbody tr:has-text("Plástico PET") button[role=checkbox]'), label='marca o Plástico PET')
    c.click(BTNX('Transferir Estoque'), at=c.A(1, 'Transferir', 0.6), label='Transferir Estoque (barra de baixo)')
    c.waitfor(text='Transferência em Lote', timeout=10)
    c.mark(2)
    c.click(SEL(f'{ALERTA} button[role=combobox]'), at=c.A(2, 'destino', 0.6), label='Destino')
    c.click(SEL('[role=option]:has-text("Recicla Vale Metais")'), at=c.A(2, 'destino', 0.1), label='Destino: Recicla Vale Metais')
    c.click(SEL(f'{ALERTA} div:has(> div > p:text-is("Papelão")) input[type=number], {ALERTA} div.p-3:has(p:text-is("Papelão")) input[type=number]'), at=c.A(2, 'quantidades.', 0.9), label='quantidade do Papelão')
    c.type(SEL(f'{ALERTA} div.p-3:has(p:text-is("Papelão")) input[type=number]'), '300', at=c.A(2, 'quantidades.', 0.5), noClick=True, clear=True, label='Papelão 300 kg')
    c.click(SEL(f'{ALERTA} div.p-3:has(p:text-is("Plástico PET")) input[type=number]'), label='quantidade do Plástico PET')
    c.type(SEL(f'{ALERTA} div.p-3:has(p:text-is("Plástico PET")) input[type=number]'), '150', noClick=True, clear=True, label='Plástico PET 150 kg')
    c.hover(SEL(f'{ALERTA} div.p-3:has(p:text-is("Papelão")) :text("Origem")'), 1.4, at=c.A(2, 'quanto', 0.5), label='os quadros Origem e Destino: quanto tem e quanto fica (ZOOM)')
    c.click(SEL(f'{ALERTA} button:has-text("Enviar 2 Transferência")'), at=c.A(2, 'pedido', 0.6), label='Enviar 2 Transferência(s)')
    c.waitfor(text='solicitações criadas', timeout=10)
    c.registra(TXTP('solicitações criadas'), label='aviso: 2 solicitações criadas — aguardando aprovação (ZOOM)')
    c.mark(3)
    troca_para_rafael(c, at=round(c.L(3) + 0.3, 2))
    c.click(LINK_GER('Estoque', '/gerencial/estoque'), label='Estoque do Gerencial (menu)')
    c.waitfor(text='Tabela Unificada de Materiais', timeout=15)
    c.mark(4)
    c.click(TAB('transferencias'), at=c.A(4, 'aba', 0.6), label='aba Transferências')
    c.waitfor(text='Transferências Inter-Unidades', timeout=10)
    c.hover(SEL('#tab-btn-transferencias'), 1.2, at=c.A(4, 'número', 0.5), label='o contador de pedidos esperando (ZOOM)')
    c.mark(5)
    c.click(BTN('Nova'), at=c.A(5, 'Nova,', 0.6), label='Nova')
    c.waitfor(text='Unidade de origem...', timeout=8)
    c.ev(js_rola_texto('Nova transferência em lote', 140, 500), label='desce até Nova transferência em lote')
    c.click(COMBO('Unidade de origem...'), label='Origem')
    c.click(OPT('Recicla Vale Metais'), label='Origem: Recicla Vale Metais')
    c.click(COMBO('Unidade de destino...'), label='Destino')
    c.click(OPT('Filial Pindamonhangaba'), label='Destino: Filial Pindamonhangaba')
    c.click(BTNX('Selecionar todos com saldo'), at=c.A(5, 'Selecionar', 0.6), label='Selecionar todos com saldo')
    c.ev(JS_DESMARCA_MENOS % json.dumps('Ferro misto'), at=c.A(5, 'tudo', 0.3), label='desmarca o resto: fica só o Ferro misto')
    c.click(SEL('main div.p-3:has(p:text-is("Ferro misto")) input[type=number]'), label='Quantidade do Ferro misto')
    c.type(SEL('main div.p-3:has(p:text-is("Ferro misto")) input[type=number]'), '999999', at=c.A(5, 'passar', 0.5), noClick=True, clear=True, label='quantidade acima do estoque')
    c.hover(TXTP('Saldo insuficiente na origem', within=MAIN), 1.4, at=c.A(5, 'avisa', 0.5), label='Saldo insuficiente na origem: disponível … (ZOOM)')
    c.mark(6)
    c.type(SEL('main div.p-3:has(p:text-is("Ferro misto")) input[type=number]'), '500', at=c.A(6, 'Corrijo', 0.6), noClick=True, clear=True, label='Quantidade 500')
    c.click(BTNX('Solicitar 1 transferência'), at=c.A(6, 'solicito.', 0.6), label='Solicitar 1 transferência')
    c.waitfor(text='Pendente', timeout=10)
    c.ev(js_rola_texto('Transferências Inter-Unidades', 150, 600), label='desce até a lista')
    c.hover(TXT('Pendente', within=MAIN), 0.8, at=c.A(6, 'três', 0.5), label='a lista fica com três pendentes')
    c.mark(7)
    c.click(SEL(CARTAO_TRANSF('Plástico PET') + ' button:has-text("Cancelar")'), at=c.A(7, 'Cancelar.', 0.6), label='Cancelar no Plástico PET')
    c.waitfor(text='Transferência cancelada', timeout=8)
    c.hover(TXT('Cancelada', within=MAIN), 1.0, at=c.A(7, 'marcada', 0.5), label='selo Cancelada')
    c.mark(8)
    c.click(BTNX('Executar todas'), at=c.A(8, 'Executar', 0.6), label='Executar todas (2)')
    c.waitfor(text='Executar 2 transferência(s)?', timeout=8)
    c.hover(TXTP('serão listadas depois com o motivo', within=ALERTA), 1.4, at=c.A(8, 'saldo', 0.5), label='as que não tiverem saldo serão listadas com o motivo (ZOOM)')
    c.click(BTN('Confirmar e Executar'), label='Confirmar e Executar')
    c.waitfor(text='2 transferências executadas', timeout=10)
    c.mark(9)
    c.ev(js_topo(500), at=c.L(9) - 0.9, label='sobe')
    c.click(TAB('visao-geral'), at=c.A(9, 'Visão', 0.6), label='Visão Geral')
    c.waitfor(text='Tabela Unificada de Materiais', timeout=10)
    c.click(ACOES_MAT('Inox'), at=c.A(9, 'menu', 0.6), label='⋯ da linha Inox')
    c.click(ITEM_MENU('Transferir entre unidades'), at=c.A(9, 'Transferir', 0.6), label='Transferir entre unidades')
    c.waitfor(text='De qual unidade sai o Inox?', timeout=8)
    c.hover(TXTP('De qual unidade sai o Inox?', within=DLG), 1.4, at=c.A(9, 'abre', 0.5), label='De qual unidade sai o Inox? (ZOOM)')
    c.click(BTN('Cancelar', within=DLG), at=round(c.dur - 1.0, 2), label='Cancelar')
    c.fim()
    return c


# alvos da venda (Sale.tsx, os mesmos da T07)
V_CLIENTE = SEL('#customer-desktop-top')
V_BUSCA = {'placeholder': 'Buscar por nome, apelido, CPF/CNPJ ou telefone...'}
V_MAT = {'placeholder': 'Escreva o nome ou código do material'}
V_QTD = SEL("main div:has(> div > label:has-text('Quantidade (Kg)')) input")
JS_ABRE_VENDA = ("(async()=>{let a=document.querySelector('a[href=\"/venda\"]');if(!a){const b=[...document.querySelectorAll('button')].find(e=>e.textContent.trim().startsWith('Pedidos'));"
                 "if(b){b.click();await new Promise(r=>setTimeout(r,500));a=document.querySelector('a[href=\"/venda\"]')}}"
                 "if(!a)return 'SEM ALVO';a.click();return 'ok'})()")


def cap16():
    """Vender com o estoque da outra unidade: Configurações do grupo › Transferências › liga "Usar estoque de outras unidades na venda" na matriz; Venda da
    matriz: cliente Serra Fina, Alumínio perfil 3.585 kg (faltam 200); Incluir Item › "Estoque insuficiente" › Origem do estoque › Outras unidades ›
    Filial Pindamonhangaba › Transferir e Adicionar (o item entra; a transferência sai ao finalizar, que o capítulo não faz). Semente apos-cap10 +
    venda-outra-unidade (aprovação desligada)."""
    c = Cap(16, setup_ger(url='/gerencial/configuracoes', espera='Código de Convite',
                          extra=vai('/gerencial', 'Dashboard Gerencial') + abre_menu_ger() + menu_mostra('/gerencial/configuracoes')
                          + [{'do': 'click', 'target': LINK_GER('Configurações', '/gerencial/configuracoes')}, {'do': 'waitFor', 'text': 'Código de Convite', 'timeout': 12},
                             {'do': 'click', 'target': TAB('transferencias')}, {'do': 'waitFor', 'text': 'Usar estoque de outras unidades na venda', 'timeout': 10}, AGUARDA]),
            pace=0.5, start=(700, 300))
    c.mark(1)
    c.hover(TXTP('Usar estoque de outras unidades na venda', within=MAIN), 1.2, at=c.A(1, 'Usar', 0.5, nth=0), label='Usar estoque de outras unidades na venda (ZOOM)')
    c.click(SEL('main div.flex:has(> div > p:text-is("Recicla Vale Metais")) button[role=switch]'), at=c.A(1, 'Ligo', 0.6), label='liga a chave da matriz')
    c.waitfor(text='Configuração atualizada', timeout=8)
    c.mark(2)
    c.ev(JS_ABRE_VENDA, at=c.L(2) - 0.5, label='Venda (menu)')
    c.waitfor(text='Voltar para o caixa', timeout=25)
    c.add(AGUARDA)
    c.ev(ANIMA_SEMPRE)
    c.click(V_CLIENTE, at=c.A(2, 'numa', 0.6), label='Cliente')
    c.waitfor(target=V_BUSCA, timeout=10)
    c.type(V_BUSCA, 'Serra', cps=40, label='busca: Serra')
    c.click(SEL("[role=dialog] button:has-text('Serra Fina')"), label='Serra Fina Alumínio Reciclagem')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.click(V_MAT, at=c.A(2, 'faltam', 0.6), label='Material')
    c.type(V_MAT, 'perfil', cps=40, noClick=True, label='material: perfil')
    c.click(OPT('Alumínio perfil', exact=False), label='Alumínio perfil')
    c.click(V_QTD, label='Quantidade (Kg)')
    c.type(V_QTD, '3585', noClick=True, clear=True, label='quantidade 3.585 kg: faltam 200')
    c.click(BTN('Incluir Item'), at=c.A(2, 'travar,', 0.7), label='Incluir Item')
    c.waitfor(text='Estoque insuficiente', timeout=10)
    c.hover(TXTP('Faltam', within=DLG), 1.4, at=c.A(2, 'janela', 0.5), label='Faltam 200 kg de Alumínio perfil (ZOOM)')
    c.mark(3)
    c.click(SEL(f'{DLG} button[role=combobox]'), at=c.A(3, 'lista', 0.6), label='Origem do estoque')
    c.hover(SEL('[role=option]:has-text("Filial Pindamonhangaba")'), 1.4, at=c.A(3, 'filial,', 0.6), label='o grupo Outras unidades: Filial Pindamonhangaba e o saldo (ZOOM)')
    c.click(SEL('[role=option]:has-text("Filial Pindamonhangaba")'), at=c.A(3, 'Escolho,', 0.6), label='escolhe a filial')
    c.hover(TXTP('Quantidade coberta', within=DLG), 1.2, at=c.A(3, 'coberta.', 0.6), label='Quantidade coberta')
    c.mark(4)
    c.click(BTN('Transferir e Adicionar', within=DLG), at=c.A(4, 'Transferir', 0.6), label='Transferir e Adicionar')
    c.waitfor(text='Itens do Pedido', timeout=10)
    c.hover(SEL("main tbody tr:has-text('Alumínio perfil')"), 1.6, at=c.A(4, 'item', 0.5), label='o item entrou na venda (ZOOM)')
    c.mark(5)
    c.fim()
    return c


# o "pagamento" do Pix do grupo é um passo de bastidor: o checkout pergunta a cada 5 s (check-asaas-payment); o setup anota o instante de
# cada pergunta e este eval espera a próxima e marca a cobrança como recebida ~0,4 s antes dela, por REST no Supabase falso (endereço do build;
# o robô desvia para a instância da aula). Devolve o status do PATCH.
BAKED = 'http://127.0.0.1:54340'
# as consultas vêm do supabase-js, que guardou o `fetch` original ao nascer: o instante de cada uma sai do Resource Timing (PerformanceObserver)
JS_ESCUTA_POLL = ("(()=>{if(window.__polls)return 'ja';window.__polls=[];try{performance.setResourceTimingBufferSize(5000)}catch(e){}"
                  "new PerformanceObserver(l=>{for(const e of l.getEntries()){if(String(e.name).includes('check-asaas-payment'))window.__polls.push(e.startTime)}})"
                  ".observe({type:'resource',buffered:true});return 'ok'})()")
JS_PAGA = ("(async()=>{await new Promise(r=>setTimeout(r,300));const p=window.__polls||[];let alvo;"
           "if(p.length){alvo=p[p.length-1]+5000-450;while(alvo<performance.now()+150)alvo+=5000;}else{alvo=performance.now()+1500;}"
           "await new Promise(r=>setTimeout(r,Math.max(0,alvo-performance.now())));"
           "const r=await fetch(%s,{method:'PATCH',headers:{'content-type':'application/json',Prefer:'return=minimal'},body:JSON.stringify({status:'RECEIVED'})});"
           "return r.status+' (consultas vistas: '+p.length+')'})()") % json.dumps(BAKED + '/rest/v1/subscription_payments?status=eq.PENDING')


def cap17():
    """Assinaturas numa fatura só: Assinaturas do grupo (a matriz e a filial; o botão Gerenciar sem abrir); Pagar tudo de uma vez; o aviso das
    cobranças; a chave Cobrança recorrente (ligada); PIX (QR fictício); o pagamento confirmado por um passo de bastidor. Vira apos-cap11."""
    c = Cap(17, setup_ger(url='/gerencial/assinaturas', espera='Assinaturas do grupo',
                          extra=vai(f'/checkout?mode=group&group={GRUPO}', 'Forma de pagamento') + vai('/gerencial', 'Dashboard Gerencial')
                          + abre_menu_ger() + menu_mostra('/gerencial/assinaturas') + [{'do': 'eval', 'js': JS_ESCUTA_POLL}]), pace=0.5, start=(700, 300))
    c.mark(1)
    c.click(LINK_GER('Assinaturas', '/gerencial/assinaturas'), at=c.A(1, 'assinaturas.', 0.7), label='Assinaturas do Gerencial (menu)')
    c.waitfor(text='Pagar tudo de uma vez', timeout=15)
    unid = lambda nome: f'main div.divide-y > div:has(p:text-is("{nome}"))'
    c.hover(SEL(unid('Recicla Vale Metais') + ' p:text-is("Recicla Vale Metais")'), 0.4, at=c.A(1, 'todas:', 0.5), label='a matriz e a filial')
    c.hover(SEL(unid('Filial Pindamonhangaba') + ' p.text-xs'), 0.6, at=c.A(1, 'plano,', 0.5), label='plano e vencimento de cada unidade (sem zoom nos valores)')
    c.hover(SEL(unid('Filial Pindamonhangaba') + ' span:text-is("Ativa")'), 0.6, at=c.A(1, 'ativa', 0.5), label='Ativa')
    c.mark(2)
    c.hover(SEL(unid('Filial Pindamonhangaba') + ' button:has-text("Gerenciar")'), 1.6, at=c.A(2, 'Gerenciar', 0.5), label='Gerenciar da linha da filial (ZOOM, sem abrir)')
    c.mark(3)
    c.hover(BTNX('Pagar tudo de uma vez'), 1.2, at=c.A(3, 'pagar', 0.5), label='Pagar tudo de uma vez (ZOOM)')
    c.mark(4)
    c.click(BTNX('Pagar tudo de uma vez'), at=c.A(3, 'na', 0.2), label='Pagar tudo de uma vez')
    c.waitfor(text='Unidades cobradas juntas', timeout=15)
    c.ev(ANIMA)
    c.hover(TXTP('Ao pagar, as cobranças individuais das unidades são canceladas'), 1.5, at=c.A(4, 'aviso:', 0.5), label='aviso das cobranças (ZOOM)')
    c.mark(5)
    c.hover(TXTP('Ao pagar, as cobranças individuais das unidades são canceladas'), 1.5, at=c.A(5, 'filial', 0.5), label='aviso das cobranças (continua)')
    c.mark(6)
    c.hover(TXTP('Cobrança recorrente'), 1.4, at=c.A(6, 'Cobrança', 0.5), label='Cobrança recorrente, ligada (ZOOM)')
    c.confere('main', ['Cobrança recorrente', 'Cobra o total do grupo automaticamente todo mês'], 'a chave Cobrança recorrente')
    c.mark(7)
    # o checkout pergunta a cada 5 s se o Pix foi pago, a contar da criação da cobrança: o clique em "Escolho" deixa a consulta que confirma
    # o pagamento ~0,5 s depois de "pronto:" (o bastidor marca a cobrança paga logo antes dela)
    c.click(BTNX('PIX'), at=c.A(7, 'Escolho', 0.4), label='PIX')
    c.waitfor(text='Aguardando confirmação do pagamento', timeout=12)   # PixPaymentView: QR, "Ou copie o código PIX:" e a espera
    c.hover(BTNX('Cartão de Crédito'), 0.5, at=c.A(7, 'cartão', 0.5), label='Cartão de Crédito (sem clicar)')
    c.mark(8)
    # com `at` na marca da L8 (sem ele a marca L8 só sairia no fim do capítulo); o eval espera a hora certa por dentro
    c.ev(JS_PAGA, at=c.L(8) - 0.9, label='bastidor: o Pix é pago (a cobrança fica RECEIVED antes da próxima consulta)')
    c.waitfor(text='Pagamento Confirmado!', timeout=8)
    c.registra(TXT('Pagamento Confirmado!'), label='Pagamento Confirmado!')
    c.mark(9)
    c.fim()
    return c


def cap18():
    """Recapitulando: a tela é só o Dashboard Gerencial com o menu do grupo; o cursor passa pelos itens do menu conforme a fala recapitula
    (Configurações, Dashboard, Financeiro, Estoque, Assinaturas). Sem clicar, sem mudar de tela: a ilustração do capítulo faz o resto."""
    c = Cap(18, setup_ger(extra=vai('/dashboard', 'Olá, Rafael!') + abre_menu_ger()), pace=0.5, start=(700, 300))
    c.mark(1)
    c.ev(js_menu_rola('/gerencial/configuracoes'), label='a lista do menu desce até Configurações (os itens do grupo aparecem)')
    c.hover(LINK_GER('Configurações', '/gerencial/configuracoes'), 0.6, at=c.A(1, 'criou', 0.6), label='Configurações (o grupo e o código)')
    c.mark(2)
    c.hover(LINK_GER('Configurações', '/gerencial/configuracoes'), 0.6, at=c.A(2, 'código', 0.6), label='Configurações (o código que vence)')
    c.mark(3)
    c.hover(LINK_GER('Dashboard', '/gerencial'), 0.8, at=c.A(3, 'Dashboard', 0.6), label='Dashboard')
    c.mark(4)
    c.hover(LINK_GER('Financeiro', '/gerencial/financeiro'), 0.8, at=c.A(4, 'Viu', 0.6), label='Financeiro')
    c.mark(5)
    c.hover(LINK_GER('Estoque', '/gerencial/estoque'), 0.8, at=c.A(5, 'estoque', 0.6), label='Estoque')
    c.mark(6)
    c.hover(LINK_GER('Estoque', '/gerencial/estoque'), 0.6, at=c.A(6, 'Transferiu', 0.6), label='Estoque (as transferências)')
    c.mark(7)
    c.hover(LINK_GER('Assinaturas', '/gerencial/assinaturas'), 0.8, at=c.A(7, 'assinaturas', 0.6), label='Assinaturas')
    c.mark(8)
    c.fim()
    return c


# ---------------------------------------------------------------- main
def main():
    pedidos = [int(a) for a in sys.argv[1:] if a.isdigit()]
    fns = {n: globals().get(f'cap{n:02d}') for n in range(19)}
    feitos = []
    for n, fn in fns.items():
        if fn is None or (pedidos and n not in pedidos):
            continue
        c = fn()
        d = c.out()
        last = -1
        for stp in d['steps']:   # o `at` precisa ser crescente
            if 'at' in stp:
                if stp['at'] < last - 1e-9:
                    print(f'  aviso cap{n:02d}: at {stp["at"]} < {last} em "{stp.get("label") or stp.get("name")}"')
                last = max(last, stp['at'])
        json.dump(d, open(os.path.join(HERE, f'cap{n:02d}.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
        nat = sum(1 for st in d['steps'] if st.get('do') != 'mark')
        feitos.append(f'cap{n:02d} {nat} passos, {len(c.linhas)} linhas, {c.dur:.1f} s{" (fala estimada)" if c.estimado else ""}')
        if os.environ.get('ANCORAS'):
            for i, p, t in c.anchors:
                print(f'   cap{n:02d} L{i} {p!r} -> {t}')
    print('\n'.join(feitos))


if __name__ == '__main__':
    main()
