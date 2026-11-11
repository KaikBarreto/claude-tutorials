#!/usr/bin/env python3
"""T04 · gera rec/t04/cap00..cap13.json (roteiros do robô) a partir da voz (t04/narracao/capNN.json).

Clientes, fornecedores e a ficha do parceiro, no COMPUTADOR (janela 1280x800: modo compacto da tela, selos da lista só com ícone),
logado como Rafael Nogueira (MASTER, Recicla Vale Metais), EcoSistema 1.59.154. FAKE_NOW 2026-11-10T08:30:00-03:00 em todos.
Cada passo é preso a uma palavra da fala: `at` = início da palavra − o custo do gesto (A(linha, palavra, folga)), para o cursor CHEGAR
na palavra (docs/04, "Custo real dos gestos"). Hoje a voz é ESTIMADA (capNN.json do preparar_aula.sh); com a voz real, rode de novo.
Rodar de qualquer pasta: `python3 -I rec/t04/gerar.py [NN ...]`. Depois: ensaio.py NN, gravação --rapido, resumo.py NN --ens, prever.py.

Cadeia de sementes (rec/mundo/seeds-extra/t04/, t04_sementes.py): `inicio` (Cida Ramos, links do portal, depósito na tabela padrão)
nos caps 0 a 2; `apos-cap02` (Rogério) nos 3 e 4; `apos-cap04` (serralheria) no 5; `apos-cap05` (serralheria cliente+fornecedor) no 6;
`apos-cap06` (Tabela Depósitos no depósito) nos 7, 8 e 9; `apos-cap09` (pagamento de 1.200,00) nos 10 a 13. Cada `apos-capNN` sai do
ensaio do capítulo NN com 0 falho (`t04_sementes.py captura NN`, logo depois, na mesma instância).

Particularidades:
 - Menu lateral recolhido no `setup` do cap01 em diante (botão de ícone do topo, sem rótulo); no cap00 o recolher é filmado.
 - Lista + ficha ao lado (ClientsListView): a linha é um <button> com "código · nome"; a ficha abre ao lado com 7 abas.
 - A dica da lupa do CNPJ é `title` nativo (não aparece no vídeo): o robô passa o mouse e lê o texto (`eval`) para o aviso da edição.
 - Selos da linha (Mesmo telefone, aptidão fiscal) são Tooltip do Radix (aparecem com o mouse parado, 150 ms).
 - Observador `OBS` guarda em `window.__avisos` texto de erro e toast de erro; o passo final devolve a lista (tem de sair vazia).
"""
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TUT_HOME = os.path.normpath(os.path.join(HERE, '..', '..'))
NARR = os.path.join(TUT_HOME, 't04', 'narracao')
FAKE_NOW = '2026-11-10T08:30:00-03:00'
NOMES = ['Abertura', 'Como a tela está organizada', 'Pessoa física e pessoa jurídica', 'Buscar dados pelo CNPJ', 'Dados fiscais e o campo vermelho',
         'Cliente e fornecedor ao mesmo tempo', 'Tabela de preço do parceiro', 'A ficha do parceiro', 'Os materiais que ele mais movimenta',
         'Conta-corrente: saldo e extrato', 'Lucro estimado', 'Financeiro e notas fiscais', 'Relatório de saldos', 'Recapitulando']
_I = ['t04/inicio']
SEMENTE = {0: _I, 1: _I, 2: _I, 3: _I + ['t04/apos-cap02'], 4: _I + ['t04/apos-cap02'], 5: _I + ['t04/apos-cap04'],
           6: _I + ['t04/apos-cap05'], 7: _I + ['t04/apos-cap06'], 8: _I + ['t04/apos-cap06'], 9: _I + ['t04/apos-cap06'],
           10: _I + ['t04/apos-cap09'], 11: _I + ['t04/apos-cap09'], 12: _I + ['t04/apos-cap09'], 13: _I + ['t04/apos-cap09']}

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
OBS = ("(()=>{window.__avisos=[];const re=/N[ãa]o foi poss[ií]vel|Erro ao|Tente novamente|Algo deu errado|Falha ao|Something went wrong|inv[áa]lid/i;"
       "const chk=(t)=>{t=(t||'').trim();const m=t&&t.match(new RegExp('[^]{0,40}('+re.source+')[^]{0,40}','i'));"
       "if(m&&window.__avisos.length<10)window.__avisos.push(m[0].replace(/[\\n\\r\\t ]+/g,' '))};new MutationObserver(ms=>{for(const m of ms){"
       "m.addedNodes.forEach(n=>chk(n.textContent));if(m.type==='characterData')chk(m.target.textContent)}}).observe(document.body,"
       "{childList:true,subtree:true,characterData:true});chk(document.body.innerText);"
       "setInterval(()=>{document.querySelectorAll('[data-sonner-toast][data-type=error]').forEach(t=>{const s='TOAST DE ERRO: '+t.textContent.trim().slice(0,90);"
       "if(!window.__avisos.includes(s)&&window.__avisos.length<10)window.__avisos.push(s)})},300);return 1})()")
# animações do framer-motion montadas depois da carga começam "no futuro" com o relógio simulado (docs/08, T5 cap10): acerta o início
ANIM = "(()=>{const a=document.getAnimations().filter(x=>x.currentTime<0);a.forEach(x=>x.startTime=document.timeline.currentTime);return a.length})()"


class Cap:
    def __init__(s, n, pace=0.5, cps=40, start=(760, 470), prewarm=None, setup=None):
        s.n = n
        s.words, s.linhas, s.dur, s.estimado = carregar_voz(n)
        s.steps, s.pending, s.anchors = [], [], []
        s.pace, s.cps, s.start = pace, cps, start
        s.prewarm = prewarm or ['/login']
        s.setup = list(setup or []) + [{'do': 'eval', 'js': OBS}]

    # ---- tempo
    def L(s, i):
        return round(s.linhas[i - 1]['s'], 2)

    def W(s, i, palavra, nth=None, fim=False):
        q = norm(palavra)
        hits = [w for w in s.words if w['linha'] == i - 1 and norm(w['w']) == q]
        if nth is None:
            if len(hits) > 1:
                print(f'  aviso cap{s.n:02d}: "{palavra}" aparece {len(hits)} vezes na linha {i}: usei a 1a (passe nth)')
            nth = 0
        if len(hits) <= nth:
            raise SystemExit(f'cap{s.n:02d}: palavra "{palavra}" (#{nth}) não achada na linha {i}: '
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

    def digita(s, campo, text, at_clique, at_texto, label, cps=40):
        """clique no campo (ancorado) e digitação sem novo clique, ancorada na palavra (docs/04, "Digitar sem esperar")"""
        s.click(campo, at=at_clique, label=label + ' (clique no campo)')
        return s.type(campo, text, at=at_texto, label=label, cps=cps, noClick=True)

    def marcar(s, target, at=None, label=None):
        """registra o retângulo do alvo para a câmera (zoom) sem mexer no mouse: `type` sem clique e sem texto"""
        return s._p({'do': 'type', 'target': target, 'text': '', 'noClick': True, 'optional': True, 'timeout': 4}, at, label, {})

    def press(s, key, at=None, label=None, **kw):
        return s._p({'do': 'press', 'key': key}, at, label, kw)

    def ev(s, js, at=None, label=None, **kw):
        return s._p({'do': 'eval', 'js': js}, at, label, kw)

    def pause(s, seconds):
        return s.add({'do': 'pause', 'seconds': seconds})

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

    def confere_campos(s, esperados, label, escopo='[role=dialog]'):
        """lê o VALOR dos campos (input/textarea) do escopo e compara com a fala"""
        esp = [esperados] if isinstance(esperados, str) else list(esperados)
        js = ("(async()=>{const esp=%s;let out='';for(let i=0;i<12;i++){const v=[...document.querySelectorAll(%s+' input, '+%s+' textarea')].map(e=>e.value).join(' | ');"
              "const falta=esp.filter(e=>!v.includes(e));if(!falta.length)return 'OK: '+esp.join(' | ');out='DIFERENTE: faltou '+JSON.stringify(falta)+' em: '+v.slice(0,260);"
              "await new Promise(r=>setTimeout(r,300));}return out})()") % (json.dumps(esp, ensure_ascii=False), json.dumps(escopo), json.dumps(escopo))
        return s.add({'do': 'eval', 'js': js, 'label': 'confere ' + label})

    def fim(s):
        s.flush(1e9)
        s.steps.append({'do': 'eval', 'js': 'JSON.stringify(window.__avisos || "sem observador")', 'label': 'avisos de erro na tela'})
        s.steps.append({'do': 'mark', 'name': 'FIM', 'at': round(s.dur, 2)})

    def out(s):
        est = ' ESTIMADA' if s.estimado else ''
        return {
            'name': f't04-cap{s.n:02d}',
            'title': f'T4 · Cap. {s.n} · {NOMES[s.n]} (narração{est} {str(round(s.dur, 1)).replace(".", ",")} s; marcas L1..L{len(s.linhas)} = '
                     f'início de cada linha do roteiro; FAKE_NOW {FAKE_NOW}; logado como Rafael Nogueira)',
            'seed': f't04-cap{s.n:02d}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
            'start': {'x': s.start[0], 'y': s.start[1]},
            'anonymous': True, 'storage': dict(STORAGE),
            'seedExtra': list(SEMENTE[s.n]),
            'prewarm': s.prewarm, 'setup': s.setup, 'steps': s.steps,
        }


# ---------------------------------------------------------------- alvos
MAIN = 'main'
DLG = '[role=dialog]'
BTN = lambda n, within=None, **kw: {'role': 'button', 'name': n, 'exact': True, **({'within': within} if within else {}), **kw}
TXT = lambda t, within=MAIN, **kw: {'text': t, 'exact': True, 'within': within, **kw}
SEL = lambda s, **kw: {'selector': s, **kw}
OPT = lambda n, **kw: {'role': 'option', 'name': n, **kw}
ITEM = lambda n, **kw: {'role': 'menuitem', 'name': n, **kw}
AGUARDA = {'do': 'waitFor', 'idle': True}
TOGGLE = SEL('header button.h-8.w-8')                                                # recolher/abrir o menu lateral (sem rótulo)
ABA = lambda n: {'role': 'tab', 'name': n, 'exact': True}                            # abas da tela (Clientes, Fornecedores, Visão geral)
LINHA = lambda nome: SEL(f"main aside button:has-text('{nome}')")                    # a linha da lista (o <button> inteiro)
NOME_LINHA = lambda nome: SEL(f"main aside button:has-text('{nome}') p.font-medium")  # "código · nome" da linha
SALDO_LINHA = lambda nome: SEL(f"main aside div:has(> button:has-text('{nome}')) span.tabular-nums", nth=0)   # etiqueta do saldo (a conferir)
FICHA = "main section[aria-label^='Detalhes de']"
ABA_FICHA = lambda n: SEL(f"[aria-label='Seções da ficha'] button:has-text('{n}')")
BUSCA = lambda tipo: {'placeholder': f'Buscar {tipo}...'}
CAMPO = lambda i: SEL(f'{DLG} #{i}')
ABA_DLG = lambda n: {'role': 'tab', 'name': n, 'within': DLG}
SALVAR = BTN('Salvar', DLG)
LUPA = SEL(f"{DLG} button[aria-label='Buscar dados pelo CNPJ']")

# ---------------------------------------------------------------- trechos de setup (fora do vídeo)
def stable_id(chave):
    """o mesmo UUID do `@id:<chave>` das sementes (rec/fakebase/core/util.mjs, stableId)"""
    import hashlib
    h = bytearray(hashlib.sha1(('domiflix-fake:' + chave).encode()).digest())
    h[6] = (h[6] & 0x0F) | 0x50
    h[8] = (h[8] & 0x3F) | 0x80
    x = h[:16].hex()
    return f'{x[:8]}-{x[8:12]}-{x[12:16]}-{x[16:20]}-{x[20:32]}'


RAFAEL = stable_id('user.rafael')
VERSAO = '1.59.154'
HOJE = FAKE_NOW[:10]
# Capítulo "anonymous": o robô abre o app sem sessão e o setup entra pela tela de login com $TUT_USER e $TUT_SENHA do ambiente (o
# valor nunca vai para arquivo nem log). O localStorage da sessão vem aqui: versão já vista, PWA dispensado, tema claro e as chaves
# do mundo (mundo.json "navegador.localStorage").
STORAGE = {'app_version': VERSAO, 'notification_shown_version': VERSAO, 'pwa-install-dismissed': 'true', 'theme': 'light',
           f'daily-tasks-reminder-last-shown-{RAFAEL}': HOJE, 'initial-preferences-set': 'true'}
LOGIN = [{'do': 'waitFor', 'target': {'label': 'E-mail'}, 'timeout': 30},
         {'do': 'type', 'target': {'label': 'E-mail'}, 'text': '$TUT_USER', 'cps': 40},
         {'do': 'type', 'target': {'label': 'Senha', 'exact': True}, 'text': '$TUT_SENHA', 'cps': 40},
         {'do': 'click', 'target': {'role': 'button', 'name': 'Entrar', 'exact': True}},
         {'do': 'waitFor', 'text': 'Olá, Rafael!', 'timeout': 30}, AGUARDA]
IR_TELA = [{'do': 'goto', 'url': '/clientes-fornecedores'}, {'do': 'waitFor', 'text': 'Aços Quiririm Ltda', 'timeout': 30}, AGUARDA]
RECOLHE = [{'do': 'click', 'target': TOGGLE}, {'do': 'wait', 'seconds': 0.8}]


def setup_tela(aba=None, ficha=None, extra=()):
    """login, a tela Clientes e Fornecedores com o menu recolhido, a aba do capítulo e (opcional) a ficha de um parceiro aberta"""
    s = LOGIN + IR_TELA + RECOLHE
    if aba and aba != 'Clientes':
        s += [{'do': 'click', 'target': ABA(aba)}, {'do': 'waitFor', 'target': BUSCA('fornecedor' if aba == 'Fornecedores' else 'cliente'), 'timeout': 15}, AGUARDA]
    if ficha:
        s += [{'do': 'click', 'target': LINHA(ficha)}, {'do': 'waitFor', 'target': SEL(f"{FICHA}[aria-label='Detalhes de {ficha}']"), 'timeout': 15}, AGUARDA]
    s += list(extra) + [{'do': 'eval', 'js': ANIM}]
    return s


# ---------------------------------------------------------------- JavaScript (rolagens suaves, leituras)
ACHA_ROLAGEM = ("const rolagem=(el)=>{let c=el&&el.parentElement;while(c&&c!==document.body){const s=getComputedStyle(c);"
                "if(/(auto|scroll)/.test(s.overflowY)&&c.scrollHeight>c.clientHeight+4)return c;c=c.parentElement;}return null};")
SUAVE = ("await new Promise(res=>{const t0=performance.now();const f=t=>{const p=Math.min(1,(t-t0)/DUR),e=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;"
         "c.scrollTop=y0+dy*e;p<1?requestAnimationFrame(f):res()};requestAnimationFrame(f)});")


def js_rola(seletor, y, dur_ms=700):
    """rolagem suave do contêiner que rola o elemento `seletor` (o mais próximo) até o topo dele ficar em y px CSS (limitado ao que
    o contêiner rola). Devolve o topo final, 'ok' (já estava), 'SEM ALVO' ou 'SEM ROLAGEM'."""
    return ("(async()=>{" + ACHA_ROLAGEM + f"const el=[...document.querySelectorAll({json.dumps(seletor)})].filter(e=>e.offsetParent)[0];if(!el)return 'SEM ALVO';"
            "const c=rolagem(el);if(!c)return 'SEM ROLAGEM';"
            f"let dy=Math.round(el.getBoundingClientRect().top-{int(y)});const y0=c.scrollTop;dy=Math.max(-y0,Math.min(c.scrollHeight-c.clientHeight-y0,dy));"
            "if(Math.abs(dy)<3)return 'ok';" + SUAVE.replace('DUR', str(int(dur_ms))) + "return Math.round(el.getBoundingClientRect().top)})()")


def js_rola_texto(texto, y, dur_ms=700, escopo=DLG):
    """como js_rola, com o alvo achado pelo texto (o menor elemento do escopo cujo texto é exatamente `texto`)"""
    return ("(async()=>{" + ACHA_ROLAGEM + f"const el=[...document.querySelectorAll({json.dumps(escopo + ' *')})].filter(e=>e.textContent.trim()==={json.dumps(texto)}&&e.offsetParent)"
            ".sort((a,b)=>a.textContent.length-b.textContent.length||a.children.length-b.children.length)[0];if(!el)return 'SEM ALVO';"
            "const c=rolagem(el);if(!c)return 'SEM ROLAGEM';"
            f"let dy=Math.round(el.getBoundingClientRect().top-{int(y)});const y0=c.scrollTop;dy=Math.max(-y0,Math.min(c.scrollHeight-c.clientHeight-y0,dy));"
            "if(Math.abs(dy)<3)return 'ok';" + SUAVE.replace('DUR', str(int(dur_ms))) + "return Math.round(el.getBoundingClientRect().top)})()")


def js_title(seletor):
    """lê o `title` (dica nativa do navegador, que não aparece no vídeo) para o aviso da edição"""
    return f"(()=>{{const e=document.querySelector({json.dumps(seletor)});return e?(e.getAttribute('title')||'SEM TITLE'):'SEM ALVO'}})()"


def js_limpa_busca(placeholder):
    """apaga a busca (o React recebe o input vazio): a lista volta inteira"""
    return ("(()=>{const e=document.querySelector('input[placeholder=\"%s\"]');if(!e)return 'SEM ALVO';e.focus();e.select();"
            "document.execCommand('delete');return 'busca: '+JSON.stringify(e.value)})()") % placeholder


# ---------------------------------------------------------------- alvos próprios do T04 (lista, selos, ficha)
DUP = lambda nome: SEL(f"main aside button:has-text('{nome}') .cursor-help:has(svg.lucide-phone)")                  # selo "Mesmo telefone" (só ícone)
FISCAL_OK = lambda nome: SEL(f"main aside button:has-text('{nome}') .cursor-help:has(svg.lucide-badge-check)")     # sinal verde
INCOMPLETO = lambda nome: SEL(f"main aside button:has-text('{nome}') .cursor-help:has(svg[class*=triangle])")      # triângulo âmbar
SALDO_ROW = lambda nome: SEL(f"main aside button:has-text('{nome}') .tabular-nums")                                 # etiqueta do saldo
FICHA_DE = lambda nome: f"main section[aria-label='Detalhes de {nome}']"
MENU_CF = {'role': 'link', 'name': 'Clientes e Fornecedores'}
INCOMPLETOS = SEL("main button[aria-pressed]:has-text('incompletos')")
MOSTRAR_TODOS = SEL("main button[aria-pressed]:has-text('Mostrar todos')")
NOVO_FORN = BTN('Novo Fornecedor', MAIN)
DLG_ROLA = lambda texto, y=300, dur=700: js_rola_texto(texto, y, dur)


def cap_novo(n, aba='Fornecedores', ficha=None, extra=(), **kw):
    return Cap(n, setup=setup_tela(aba, ficha, extra), prewarm=['/login'], **kw)


# ================================================================ capítulos
def cap00():
    """Abertura: o Dashboard (sob a ilustração do pátio nas linhas 1 a 3, cartão Antes: na 4); na 5 o menu Clientes e Fornecedores
    e o recolher do menu lateral, filmados."""
    setup = LOGIN + IR_TELA + [{'do': 'goto', 'url': '/dashboard'}, {'do': 'waitFor', 'text': 'Olá, Rafael!', 'timeout': 25}, AGUARDA, {'do': 'eval', 'js': ANIM}]
    c = Cap(0, setup=setup, start=(760, 300))
    for i in (1, 2, 3, 4):
        c.mark(i)
    c.mark(5)
    c.hover(MENU_CF, 0.8, at=c.A(5, 'menu,', 0.5, nth=0), label='o cursor desce pelo menu até Clientes e Fornecedores')
    c.click(MENU_CF, at=c.A(5, 'Clientes', 0.6), label='Clientes e Fornecedores (menu lateral)')
    c.waitfor(text='Aços Quiririm Ltda', timeout=15)
    c.click(TOGGLE, at=c.A(5, 'recolho', 0.6), label='recolhe o menu lateral (botão do topo)', noScroll=True)
    c.hover(LINHA('Aços Quiririm Ltda'), 0.8, at=c.A(5, 'larga.', 0.6), label='a lista, agora mais larga')
    c.hover(ABA('Clientes'), 0.6, at=c.A(5, 'organizada.', 0.5), label='as abas da tela')
    c.fim()
    return c


def cap01():
    """Como a tela está organizada: abas, (ilustração cliente x fornecedor), a linha e o saldo, busca/filtros/ordem, a ficha ao lado,
    Relatório e Novo Cliente, o selo Mesmo telefone, a busca pelo telefone e a Visão geral."""
    c = cap_novo(1, aba='Clientes', start=(760, 300))
    c.mark(1)
    c.hover(ABA('Clientes'), 0.5, at=c.A(1, 'Clientes', 0.5), label='aba Clientes')
    c.hover(ABA('Fornecedores'), 0.8, at=c.A(1, 'Fornecedores.', 0.5), label='aba Fornecedores (sem clicar)')
    c.mark(2)   # ilustração cliente x fornecedor
    c.mark(3)
    c.hover(NOME_LINHA('Aços Quiririm Ltda'), 1.0, at=c.A(3, 'nome,', 0.5), label='linha Aços Quiririm: nome e CNPJ')
    c.hover(SALDO_ROW('Aços Quiririm Ltda'), 1.6, at=c.A(3, 'saldo,', 0.5), label='linha Aços Quiririm: saldo R$ 4.870,00')
    c.confere(f"main aside button:has(p)", ['Aços Quiririm Ltda', '98.463.027/0001-15', 'R$ 4.870,00'], 'linha da Aços Quiririm com o saldo')
    c.mark(4)
    c.hover(BUSCA('cliente'), 0.8, at=c.A(4, 'busca,', 0.5), label='busca Buscar cliente...')
    c.hover(SEL("main aside button:has(svg.lucide-funnel), main aside button:has(svg.lucide-filter)"), 0.5, at=c.A(4, 'filtros', 0.5), label='Filtros')
    c.hover(SEL("main aside button:has(svg.lucide-sliders-horizontal)"), 0.6, at=c.A(4, 'ordem', 0.5), label='Ordenar')
    c.mark(5)
    c.click(LINHA('Aços Quiririm Ltda'), at=c.A(5, 'Clicando', 0.6), label='clica na Aços Quiririm: a ficha abre ao lado')
    c.waitfor(target=SEL(FICHA_DE('Aços Quiririm Ltda')), timeout=10)
    c.confere(FICHA_DE('Aços Quiririm Ltda'), ['Aços Quiririm Ltda', 'Cliente', 'R$ 4.870,00', 'a receber'], 'ficha da Aços Quiririm')
    c.hover(SEL(FICHA_DE('Aços Quiririm Ltda') + ' h2, ' + FICHA_DE('Aços Quiririm Ltda') + ' h1'), 1.0, at=c.A(5, 'ficha', 0.5), label='a ficha ao lado')
    c.mark(6)
    c.hover(SEL("main button[aria-label='Relatório']"), 1.0, at=c.A(6, 'Relatório,', 0.5), label='Relatório (sem clicar)')
    c.hover(BTN('Novo Cliente', MAIN), 0.8, at=c.A(6, 'Novo', 0.5), label='Novo Cliente (sem clicar)')
    c.mark(7)
    c.click(ABA('Fornecedores'), at=c.A(7, 'Fornecedores,', 0.6), label='aba Fornecedores')
    c.waitfor(target=BUSCA('fornecedor'), timeout=10)
    c.hover(DUP('Aparecida Ramos'), 2.6, at=c.A(7, 'telefone', 0.6), label='selo Mesmo telefone da Aparecida Ramos (tooltip)')
    c.confere('body', ['Mesmo telefone em outro cadastro', 'Também está em: Cida Ramos'], 'tooltip Mesmo telefone')
    c.mark(8)
    c.digita(BUSCA('fornecedor'), '90000-1201', c.A(8, 'Buscando', 0.6), c.A(8, 'telefone,', 0.05), 'busca pelo telefone da Aparecida')
    c.confere("main aside", ['Aparecida Ramos', 'Cida Ramos'], 'a busca pelo telefone mostra as duas')
    c.hover(LINHA('6 · Cida Ramos'), 0.8, at=c.A(8, 'juntos,', 0.5), label='Aparecida Ramos e Cida Ramos juntas')
    c.ev(js_limpa_busca('Buscar fornecedor...'), at=c.A(8, 'confere.', 0.0), label='apaga a busca (a lista volta inteira)')
    c.mark(9)
    c.click(ABA('Visão geral'), at=c.A(9, 'Visão', 0.6), label='aba Visão geral')
    c.waitfor(text='Ranking do período', timeout=12)
    c.ev(ANIM, label='animações da Visão geral')
    c.hover(TXT('Clientes por venda'), 0.8, at=c.A(9, 'comprou', 0.5, nth=0), label='Clientes por venda')
    c.hover(TXT('Fornecedores por compra'), 0.8, at=c.A(9, 'quem', 0.5, nth=0), label='Fornecedores por compra')
    c.ev(js_rola_texto('Saldos de clientes', 260, 800, escopo='main'), at=c.A(9, 'quanto', 0.9), label='desce até os saldos de clientes e fornecedores')
    c.hover(TXT('Saldos de clientes'), 0.6, at=c.A(9, 'receber', 0.5), label='Saldos de clientes (a receber)')
    c.hover(TXT('Saldos de fornecedores'), 0.6, at=c.A(9, 'pagar.', 0.5), label='Saldos de fornecedores (a pagar)')
    c.fim()
    return c
