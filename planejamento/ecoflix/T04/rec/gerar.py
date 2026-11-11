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

    def cola(s, campo, text, at_clique, at_texto, label):
        """clique no campo (ancorado) e o texto colado na palavra: nome ou chave longa que, digitado a ~0,17 s por letra (ensaio de
        11/11, máquina com outros agentes), não cabe na fala (docs/04, colar())"""
        s.click(campo, at=at_clique, label=label + ' (clique no campo)')
        return s.ev(js_colar(text), at=at_texto, label=label + ' (colado)')

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

    def encaixa_hovers(s, custo=0.9, minimo=0.15):
        """o hover termina antes do próximo passo com `at` (uma marca Ln, outro gesto): parada (`seconds`) encurtada até caber
        (custo medido no ensaio de 11/11: 0,5 a 1,4 s além da parada; 0,9 em média); passo que não cabe nem com o mínimo fica para o prever.py acusar"""
        for k, st in enumerate(s.steps):
            if st.get('do') != 'hover' or st.get('at') is None:
                continue
            prox = next((x['at'] for x in s.steps[k + 1:] if x.get('at') is not None), None)
            if prox is None:
                continue
            cabe = round(prox - 0.05 - st['at'] - custo, 2)
            if st['seconds'] > cabe:
                st['seconds'] = max(minimo, cabe)

    def out(s):
        s.encaixa_hovers()
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
TOGGLE = SEL("header button:has(svg[class*='panel-left'])")                         # recolher/abrir o menu lateral (sem rótulo; ícone PanelLeft/PanelLeftClose)
MENU_RECOLHIDO = SEL("header button svg[class*='panel-left']:not([class*='close'])")   # o ícone vira PanelLeft com o menu recolhido
ABA = lambda n: SEL(f"main div.no-scrollbar > button:has-text('{n}')")               # abas da tela (MobilePillTabs: <button>, não role=tab)
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
# o botão fica no cabeçalho (y ~27, fora da faixa 96..730 do clique): sem `noScroll` o robô tentava rolar e o menu ficava aberto
# (achado na folha de contato do ensaio de 11/11 19:00)
RECOLHE = [{'do': 'click', 'target': TOGGLE, 'noScroll': True}, {'do': 'waitFor', 'target': MENU_RECOLHIDO, 'timeout': 8}, {'do': 'wait', 'seconds': 0.6}]


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


def js_colar(texto):
    """cola o texto no campo em foco (execCommand insertText: o React recebe o input), ~0,05 s em vez de digitar letra a letra"""
    return ("(()=>{const e=document.activeElement;if(!e||!/^(INPUT|TEXTAREA)$/.test(e.tagName))return 'SEM ALVO (nada em foco)';"
            f"document.execCommand('insertText',false,{json.dumps(texto)});return e.value}})()")


def js_clica_botao(texto, escopo='main'):
    """clique sem cursor (el.click()) no botão do escopo cujo texto é exatamente `texto`: abre a janela na hora (docs/08, T5 cap15)"""
    return ("(()=>{const b=[...document.querySelectorAll(%s+' button')].find(x=>x.textContent.trim()===%s);if(!b)return 'SEM ALVO';b.click();return 'ok'})()"
            % (json.dumps(escopo), json.dumps(texto)))


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
    c.hover(MENU_CF, 0.4, at=c.L(5) - 0.9, label='o cursor desce pelo menu até Clientes e Fornecedores')
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
    c.confere('main aside', ['Aços Quiririm Ltda', '98.463.027/0001-15', 'R$ 4.870,00'], 'linha da Aços Quiririm com o saldo')
    c.add({'do': 'eval', 'js': js_cor('Aços Quiririm Ltda', 'verde'), 'label': 'confere cor: Aços Quiririm (cliente +) verde'})
    c.mark(4)
    c.hover(BUSCA('cliente'), 0.8, at=c.A(4, 'busca,', 0.5), label='busca Buscar cliente...')
    c.hover(SEL("main aside button[aria-label^='Filtros']"), 1.0, at=c.A(4, 'filtros', 0.9), label='Filtros (o Ordenar fica do lado)')
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
    c.hover(DUP('Aparecida Ramos'), 2.6, at=c.A(7, 'telefone', 0.6, nth=0), label='selo Mesmo telefone da Aparecida Ramos (tooltip)')
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
    c.hover(TXT('Fornecedores por compra'), 0.8, at=c.A(9, 'quem', 0.5, nth=1), label='Fornecedores por compra')
    c.ev(js_rola_texto('Saldos de clientes', 260, 800, escopo='main'), at=c.A(9, 'quanto', 0.9), label='desce até os saldos de clientes e fornecedores')
    c.hover(TXT('Saldos de clientes'), 0.6, at=c.A(9, 'receber', 0.5), label='Saldos de clientes (a receber)')
    c.hover(TXT('Saldos de fornecedores'), 0.6, at=c.A(9, 'pagar.', 0.5), label='Saldos de fornecedores (a pagar)')
    c.fim()
    return c


def js_dlg_topo(dur_ms=600):
    """sobe a rolagem da janela aberta até o topo (as abas da janela ficam à vista)"""
    return ("(async()=>{const d=document.querySelector('[role=dialog]');if(!d)return 'sem janela';const c=[...d.querySelectorAll('*')].find(e=>{const s=getComputedStyle(e);"
            "return /(auto|scroll)/.test(s.overflowY)&&e.scrollHeight>e.clientHeight+4});if(!c)return 'SEM ROLAGEM';const y0=c.scrollTop,dy=-y0;if(y0<3)return 'ok';"
            + SUAVE.replace('DUR', str(int(dur_ms))) + "return 'topo:'+Math.round(c.scrollTop)})()")


def js_ficha_topo(dur_ms=600):
    """sobe a rolagem do contêiner da ficha (ou da página) até o topo"""
    return ("(async()=>{" + ACHA_ROLAGEM + "const s=document.querySelector(\"main section[aria-label^='Detalhes de']\");if(!s)return 'SEM ALVO';"
            "const c=rolagem(s.firstElementChild||s);if(!c)return 'SEM ROLAGEM';const y0=c.scrollTop,dy=-y0;if(y0<3)return 'ok';"
            + SUAVE.replace('DUR', str(int(dur_ms))) + "return 'topo:'+Math.round(c.scrollTop)})()")


def js_sem_texto(texto, escopo='[role=dialog]'):
    """conferência: o texto NÃO está mais na tela (ex.: o aviso vermelho some depois de preencher o Número)"""
    return ("(async()=>{for(let i=0;i<10;i++){const el=document.querySelector(%s);const t=el?el.innerText:'';if(!t.includes(%s))return 'OK: sumiu '+%s;"
            "await new Promise(r=>setTimeout(r,300));}return 'DIFERENTE: ainda aparece '+%s})()") % (json.dumps(escopo), json.dumps(texto), json.dumps(texto), json.dumps(texto))


def js_cores_rel(nomes, cores, escopo='[role=dialog]', celula='td:nth-child(3)'):
    """conferência dos 4 casos de saldo: em cada linha (tr do escopo com o nome), o texto do saldo e a COR dele (texto ou fundo:
    verde, vermelho ou cinza); DIFERENTE quando a cor não é a que a fala diz."""
    return ("(async()=>{const esp=%s;const cor=e=>{for(const el of [e,...e.querySelectorAll('*')])for(const p of ['color','backgroundColor']){"
            "const m=(getComputedStyle(el)[p].match(/[\\d.]+/g)||[]).map(Number);if(m.length<3||(m.length>3&&m[3]===0))continue;const [r,g]=m;"
            "if(g>r+40)return 'verde';if(r>g+40)return 'vermelho'}return 'cinza'};let out=[],ok=true;"
            "for(const [n,c] of esp){const tr=[...document.querySelectorAll(%s+' tr')].find(t=>t.textContent.includes(n));const el=tr&&tr.querySelector(%s);"
            "if(!el){out.push(n+': SEM ALVO');ok=false;continue}const k=cor(el);if(k!==c)ok=false;out.push(n.split(' ')[0]+' '+el.textContent.trim()+' '+k)}"
            "return (ok?'OK: ':'DIFERENTE: ')+out.join(' | ')})()") % (json.dumps(list(zip(nomes, cores)), ensure_ascii=False), json.dumps(escopo), json.dumps(celula))

def js_abas_ficha(fim=True, dur_ms=500):
    """rola a faixa das 7 abas da ficha para o fim (Notas fiscais e Preços à vista) ou para o começo: a 1280 px, com o menu
    recolhido, "Preços" fica fora da faixa e "Notas fiscais" cortada (achado do ensaio de 11/11)"""
    destino = 's.scrollWidth-s.clientWidth' if fim else '0'
    return ("(async()=>{const s=document.querySelector(\"[aria-label='Seções da ficha']\");if(!s)return 'SEM ALVO';const x0=s.scrollLeft,dx=(%s)-x0;"
            "if(Math.abs(dx)<3)return 'ok';await new Promise(res=>{const t0=performance.now();const f=t=>{const p=Math.min(1,(t-t0)/%d),e=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;"
            "s.scrollLeft=x0+dx*e;p<1?requestAnimationFrame(f):res()};requestAnimationFrame(f)});return 'faixa:'+Math.round(s.scrollLeft)})()") % (destino, int(dur_ms))


def js_cor(nome, cor, linha='main aside button', alvo='.tabular-nums'):
    """conferência da cor de um saldo (os 4 casos): no 1º `linha` cujo texto tem `nome`, o elemento `alvo`; verde/vermelho/cinza pela cor
    do texto ou do fundo (a fala diz a cor)"""
    return ("(async()=>{const cor=e=>{for(const el of [e,...e.querySelectorAll('*')])for(const p of ['backgroundColor','color']){"
            "const m=(getComputedStyle(el)[p].match(/[\\d.]+/g)||[]).map(Number);if(m.length<3||(m.length>3&&m[3]===0))continue;const [r,g]=m;"
            "if(g>r+40)return 'verde';if(r>g+40)return 'vermelho'}return 'cinza'};for(let i=0;i<10;i++){"
            "const row=[...document.querySelectorAll(%s)].find(x=>x.textContent.includes(%s));const el=row&&row.querySelector(%s);"
            "if(el){const k=cor(el);return (k===%s?'OK: ':'DIFERENTE: ')+%s+' '+el.textContent.trim()+' '+k}await new Promise(r=>setTimeout(r,300))}"
            "return 'DIFERENTE: sem o saldo de '+%s})()") % (json.dumps(linha), json.dumps(nome), json.dumps(alvo), json.dumps(cor), json.dumps(nome), json.dumps(nome))


AVISO_NUMERO = 'Não veio da Receita — obrigatório para emitir NF-e'
TOAST_CNPJ = 'Dados preenchidos — confira antes de salvar'
CEP_IN = SEL(f"{DLG} input[placeholder='00000-000']")
CIDADE = SEL(f"{DLG} button[role=combobox]:has-text('Taubaté')")
IND_IE = SEL(f"{DLG} button[role=combobox]:has-text('Não Contribuinte')")                 # antes de escolher (o padrão da busca)
REGIME = SEL(f"{DLG} button[role=combobox]:has-text('Simples Nacional')")                # o regime que a consulta trouxe
TABELA_PADRAO = SEL(f"{DLG} div:has(> label:has-text('Tabela de Preços Padrão')) button")
AVISO_AZUL = TXT('Mudanças em nome, CPF/CNPJ, contato, endereço e tabela de preços padrão refletem automaticamente no cadastro de cliente vinculado.', within=DLG)
TAMBEM_CLIENTE = SEL(f"{DLG} #also-counterpart")                                          # caixa "Também é cliente" (Checkbox do Radix)
BTN_FICHA = lambda nome, b: BTN(b, FICHA_DE(nome))
SALDO_FICHA = lambda nome: SEL(f"{FICHA_DE(nome)} .tabular-nums", nth=0)
COOP = 'Cooperativa Recomeço'
FC = FICHA_DE(COOP)

# setup do cap04: refaz fora do vídeo o formulário do cap03 e para no Endereço Fiscal com o Número vermelho
REFAZ_CAP03 = [
    {'do': 'click', 'target': NOVO_FORN}, {'do': 'waitFor', 'text': 'Identificação e contato', 'timeout': 10},
    {'do': 'type', 'target': CAMPO('name'), 'text': 'Serralheria Bem-Te-Vi'},
    {'do': 'click', 'target': ABA_DLG('Dados Fiscais')}, {'do': 'click', 'target': BTN('Pessoa Jurídica', DLG)},
    {'do': 'type', 'target': CAMPO('cpf_cnpj'), 'text': '46280719000124'},
    {'do': 'click', 'target': LUPA}, {'do': 'waitFor', 'text': TOAST_CNPJ, 'timeout': 12},
    {'do': 'waitFor', 'text': AVISO_NUMERO, 'timeout': 8},
    {'do': 'waitFor', 'gone': {'text': TOAST_CNPJ}, 'timeout': 15},
    {'do': 'eval', 'js': js_rola_texto('Endereço Fiscal', 150, 300)}, {'do': 'wait', 'seconds': 0.5},
]


def cap02():
    """Pessoa física e pessoa jurídica: Novo Fornecedor do Rogério (nome, apelido, telefone, Pix, saldo inicial, CPF), Salvar; depois a
    Pessoa Jurídica de outro cadastro novo mostra CNPJ, razão social e inscrição estadual (sem salvar)."""
    c = cap_novo(2, start=(900, 300))
    c.mark(1)
    c.hover(ABA('Fornecedores'), 1.0, at=c.A(1, 'fornecedor', 0.5, nth=0), label='aba Fornecedores (já aberta)')
    c.click(NOVO_FORN, at=c.A(1, 'Em', 0.6), label='Novo Fornecedor')
    c.waitfor(text='Identificação e contato', timeout=10)
    c.mark(2)
    c.cola(CAMPO('name'), 'Rogério Alves Costa', c.A(2, 'único', 1.0), c.A(2, 'Nome.', 0.1), 'Nome Rogério Alves Costa')
    c.mark(3)
    c.cola(CAMPO('contact_name'), 'Rogério Eletricista', c.A(3, 'Apelido', 0.6, nth=0), c.A(3, 'Rogério', 0.05), 'Apelido Rogério Eletricista')
    c.mark(4)
    c.digita(CAMPO('phone'), '12900002611', c.A(4, 'telefone.', 0.6, nth=0), c.A(4, 'Se', 0.05), 'Telefone (12) 90000-2611')
    c.hover(SEL(f'{DLG} label[for=phone_unavailable]'), 1.0, at=c.A(4, 'marcar', 0.5), label='Não possui telefone (sem marcar)')
    c.mark(5)
    c.cola(CAMPO('pix_key'), 'rogerio.costa@pix.example', c.A(5, 'chave', 0.6), c.A(5, 'Pix', 0.05), 'Chave PIX rogerio.costa@pix.example')
    c.mark(6)
    c.ev(DLG_ROLA('Saldo inicial', 300, 900), at=c.L(6) - 0.9, label='desce a janela até o Saldo inicial (passa pelo Também é cliente)')
    c.hover(TXT('Saldo inicial', within=DLG), 1.0, at=c.A(6, 'Saldo', 0.5), label='Saldo inicial')
    c.hover({'role': 'button', 'name': 'Adicionar saldo inicial', 'within': DLG}, 1.2, at=c.A(6, 'registra', 0.5), label='+ Adicionar saldo inicial (sem clicar)')
    c.mark(7)
    c.ev(js_dlg_topo(), at=c.L(7) - 0.9, label='sobe a janela até as abas')
    c.click(ABA_DLG('Dados Fiscais'), at=c.A(7, 'Dados', 0.6), label='aba Dados Fiscais')
    c.hover(BTN('Pessoa Física', DLG), 1.0, at=c.A(7, 'Pessoa', 0.5), label='Tipo de Pessoa: Pessoa Física (já vem marcado)')
    c.digita(CAMPO('cpf_cnpj'), '41827356090', c.A(7, 'CPF,', 0.6, nth=0), c.A(7, 'como', 0.05), 'zoom: CPF 418.273.560-90 (L7)')
    c.confere_campos(['418.273.560-90'], 'CPF com a máscara')
    c.mark(8)
    c.click(SALVAR, at=c.A(8, 'Salvar.', 0.6), label='Salvar')
    c.waitfor(text='Fornecedor cadastrado com sucesso!', timeout=12)
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.marcar(NOME_LINHA('Rogério Alves Costa'), label='Rogério Alves Costa na lista (sem mexer o mouse)')
    c.mark(9)
    # defeito do app: o rascunho do formulário (sessionStorage) é regravado depois do clearDraft() do Salvar, e a janela nova abria com
    # "Rascunho encontrado" (folha de contato do ensaio de 11/11 22:11); o robô apaga a chave antes, como a página faria (Achados do app)
    c.ev("(()=>{sessionStorage.removeItem('form-draft:entity-form-supplier');return 'rascunho apagado'})()", label='apaga o rascunho regravado pelo app (defeito)')
    c.ev(js_clica_botao('Novo Fornecedor'), at=c.L(9) - 0.9, label='Novo Fornecedor por eval (o clique logo depois de salvar levou 3,5 s no ensaio)')
    c.waitfor(text='Identificação e contato', timeout=10)
    c.click(ABA_DLG('Dados Fiscais'), at=c.A(9, 'cadastro,', 0.8), label='aba Dados Fiscais')
    c.click(BTN('Pessoa Jurídica', DLG), at=c.A(9, 'Jurídica.', 0.6), label='Pessoa Jurídica')
    c.hover(CAMPO('cpf_cnpj'), 0.2, at=c.A(9, 'CNPJ,', 0.7, nth=0), label='CNPJ (com a lupa)')
    c.hover(CAMPO('inscricao_estadual'), 0.6, at=c.A(9, 'inscrição', 0.5), label='Inscrição Estadual')
    c.hover(LUPA, 1.0, at=c.A(9, 'atalho.', 0.5), label='a lupa do CNPJ (o atalho)')
    c.fim()
    return c


def cap03():
    """Buscar dados pelo CNPJ: Serralheria Bem-Te-Vi; CNPJ, lupa (consulta simulada), razão social e nome fantasia, endereço, contato."""
    c = cap_novo(3, start=(900, 300))
    c.mark(1)
    c.click(NOVO_FORN, at=c.A(1, 'Chegou', 1.0), label='Novo Fornecedor')
    c.waitfor(text='Identificação e contato', timeout=10)
    c.cola(CAMPO('name'), 'Serralheria Bem-Te-Vi', c.A(1, 'fornecedor:', -0.5), c.A(1, 'Bem-Te-Vi,', 0.0), 'Nome Serralheria Bem-Te-Vi')
    # as abas da janela custam 2 a 3 s por clique (ensaio de 11/11): a aba sai no fim da linha 1 e chega com "Em Dados Fiscais"
    c.click(ABA_DLG('Dados Fiscais'), at=c.A(1, 'sobra', 0.0), label='aba Dados Fiscais')
    c.mark(2)
    c.click(BTN('Pessoa Jurídica', DLG), at=c.A(2, 'Pessoa', 0.9), label='Pessoa Jurídica')
    c.mark(3)
    c.cola(CAMPO('cpf_cnpj'), '46280719000124', c.A(2, 'Jurídica,', 0.0), c.A(2, 'CNPJ.', 0.05),
           'zoom: CNPJ 46.280.719/0001-24 (L2; colado: 14 dígitos a ~0,16 s não cabem na frase)')
    c.confere_campos(['46.280.719/0001-24'], 'CNPJ com a máscara')
    c.hover(LUPA, 1.6, at=c.A(3, 'lupa:', 0.5), label='lupa: Buscar dados da empresa pelo CNPJ (dica nativa: aviso na edição)')
    c.ev(js_title(f"{DLG} button[aria-label='Buscar dados pelo CNPJ']"), label='texto da dica (title) da lupa')
    c.click(LUPA, at=c.A(3, 'clique,', 0.6), label='clica na lupa: consulta a Receita')
    c.waitfor(text=TOAST_CNPJ, timeout=12)
    c.mark(4)
    c.confere_campos(['BEM-TE-VI SERRALHERIA E ESTRUTURAS LTDA', 'SERRALHERIA BEM-TE-VI'], 'razão social e nome fantasia da busca')
    c.hover(CAMPO('razao_social'), 0.8, at=c.A(4, 'razão', 0.5), label='Razão Social (da busca)')
    c.hover(CAMPO('nome_fantasia'), 0.8, at=c.A(4, 'fantasia.', 0.5), label='Nome Fantasia (da busca)')
    c.mark(5)
    c.ev(DLG_ROLA('Endereço Fiscal', 150, 700), at=c.L(5) - 0.9, label='desce a janela até o Endereço Fiscal')
    c.hover(CEP_IN, 0.3, at=c.A(5, 'CEP,', 0.5), label='CEP 12062-150')
    c.hover(CIDADE, 0.6, at=c.A(5, 'cidade,', 0.5), label='Cidade Taubaté (rua e bairro logo abaixo)')
    c.confere('dlg', ['Taubaté'], 'a cidade casou com Taubaté')
    c.confere_campos(['12062150', 'RUA DAS PALMEIRAS', 'JARDIM SANTA LUZIA'], 'CEP (sem máscara: achado), rua e bairro da busca')
    c.mark(6)
    c.ev(js_dlg_topo(), at=c.L(6) - 0.9, label='sobe a janela até as abas')
    c.click(ABA_DLG('Dados de Contato'), at=c.A(6, 'Dados', 0.6), label='aba Dados de Contato')
    c.hover(CAMPO('phone'), 0.6, at=c.A(6, 'telefone', 0.5), label='Telefone e E-mail (da busca)')
    c.hover(CAMPO('name'), 0.8, at=c.A(6, 'nome', 0.5), label='Nome: Serralheria Bem-Te-Vi (o digitado)')
    c.confere_campos(['Serralheria Bem-Te-Vi', '(12) 90000-2742', 'contato@serralheriabemtevi.example'], 'nome, telefone e e-mail')
    c.mark(7)
    c.click(ABA_DLG('Dados Fiscais'), at=c.A(7, 'conferir', 0.6), label='volta à aba Dados Fiscais')
    c.ev(DLG_ROLA('Endereço Fiscal', 150, 800), at=c.A(7, 'repara', 0.9), label='desce até o Número (vermelho)')
    c.hover(CAMPO('numero'), 0.5, at=c.A(7, 'campo', 0.5), label='o campo Número, vermelho (sem zoom)')
    c.fim()
    return c


def cap04():
    """Dados fiscais e o campo vermelho: Número 418, inscrição estadual (Contribuinte ICMS), regime da consulta, Salvar; sinal verde,
    triângulo do Rogério e o botão de incompletos."""
    c = cap_novo(4, extra=REFAZ_CAP03, start=(640, 520))
    c.mark(1)
    c.marcar(CAMPO('numero'), at=0.35, label='zoom: Número vazio e o aviso vermelho (L1-L2)')
    c.hover(CAMPO('numero'), 1.4, at=c.A(1, 'Número.', 0.5, nth=0), label='o campo Número (vazio)')
    c.mark(2)
    c.hover(TXT(AVISO_NUMERO, within=DLG), 1.8, at=c.A(2, 'aviso', 0.5), label='aviso: Não veio da Receita — obrigatório para emitir NF-e')
    c.mark(3)   # ilustração: a nota leva o endereço
    c.mark(4)
    c.digita(CAMPO('numero'), '418', c.A(4, 'completo', 0.6), c.A(4, 'quatrocentos', 0.05), 'Número 418')
    c.add({'do': 'eval', 'js': js_sem_texto(AVISO_NUMERO), 'label': 'confere o vermelho do Número sumiu'})
    c.mark(5)
    c.ev(DLG_ROLA('Inscrição Estadual', 230, 800), at=c.L(5) - 0.9, label='sobe a janela até a inscrição estadual')
    c.hover(CAMPO('inscricao_estadual'), 0.3, at=c.A(5, 'inscrição', 0.5), label='Inscrição Estadual')
    c.hover(IND_IE, 0.3, at=c.A(5, 'indicador', 0.5), label='Indicador IE')
    c.hover(REGIME, 0.6, at=c.A(5, 'regime', 0.5), label='Regime tributário do fornecedor')
    c.click(IND_IE, at=c.A(5, 'Quem', 0.3), label='abre o Indicador IE')
    c.click(OPT('Contribuinte ICMS'), at=c.A(5, 'que', 0.3, nth=0), label='Contribuinte ICMS')
    c.cola(CAMPO('inscricao_estadual'), '688412573032', c.A(5, 'contador.', 0.3), c.A(5, 'Eu', 0.05), 'Inscrição Estadual 688412573032')
    c.mark(6)
    c.hover(REGIME, 1.2, at=c.A(6, 'Simples', 0.5), label='zoom: Regime Simples Nacional e a linha da consulta (L6)')
    c.hover(TXT('Preenchido pela consulta do CNPJ: a Receita informa que esta empresa é optante pelo Simples Nacional.', within=DLG, exact=False), 1.6,
            at=c.A(6, 'regime', 0.5, nth=1), label='Preenchido pela consulta do CNPJ')
    c.confere('dlg', ['Simples Nacional', 'Contribuinte ICMS'], 'regime e indicador')
    c.mark(7)
    c.click(SALVAR, at=c.A(7, 'Salvar.', 0.6), label='Salvar')
    c.waitfor(text='Fornecedor cadastrado com sucesso!', timeout=12)
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.hover(FISCAL_OK('Serralheria Bem-Te-Vi'), 2.0, at=c.A(7, 'verde:', 0.5), label='sinal verde da serralheria (Pronto para emitir NF-e)')
    c.confere('body', ['Pronto para emitir NF-e'], 'tooltip Pronto para emitir NF-e')
    c.mark(8)
    c.hover(INCOMPLETO('Rogério Alves Costa'), 4.0, at=c.A(8, 'triângulo', 0.5), label='triângulo do Rogério (o que falta para a NF-e)')
    c.confere('body', ['Faltam dados para emitir NF-e para este cadastro:'], 'tooltip do incompleto')
    c.mark(9)
    c.click(INCOMPLETOS, at=c.A(9, 'botão', 0.6), label='botão incompletos')
    c.confere('main aside', ['Rogério Alves Costa', 'Valdir Pereira'], 'só os incompletos')
    c.hover(NOME_LINHA('Rogério Alves Costa'), 1.0, at=c.A(9, 'mostra', 0.5), label='a lista só com os incompletos')
    c.mark(10)
    c.click(MOSTRAR_TODOS, at=c.A(10, 'Uma', 0.6), label='Mostrar todos (a lista volta)')
    c.hover(NOME_LINHA('Serralheria Bem-Te-Vi'), 1.0, at=c.A(10, 'nome,', 0.5), label='a lista inteira')
    c.fim()
    return c


def cap05():
    """Cliente e fornecedor ao mesmo tempo: Editar a serralheria e marcar Também é cliente; o selo roxo; o depósito (ilustração do saldo
    único) e a aba Clientes com o mesmo saldo."""
    c = cap_novo(5, start=(700, 400))
    c.mark(1)
    c.click(LINHA('Serralheria Bem-Te-Vi'), at=c.A(1, 'serralheria', 0.6), label='clica na Serralheria Bem-Te-Vi: a ficha abre ao lado')
    c.waitfor(target=SEL(FICHA_DE('Serralheria Bem-Te-Vi')), timeout=10)
    c.hover(SALDO_FICHA('Serralheria Bem-Te-Vi'), 1.0, at=c.A(1, 'fornecedora', 0.5), label='a ficha da serralheria (Fornecedor)')
    c.mark(2)
    c.click(BTN_FICHA('Serralheria Bem-Te-Vi', 'Editar'), at=c.A(2, 'Pra', 0.6), label='Editar')
    c.waitfor(text='Editar Fornecedor', timeout=10)
    c.ev(DLG_ROLA('Também é cliente', 420, 500), label='desce a janela até Também é cliente')
    c.click(TAMBEM_CLIENTE, at=c.A(2, 'Também', 0.6), label='marca Também é cliente')
    c.add({'do': 'eval', 'js': "(()=>{const e=document.querySelector('[role=dialog] #also-counterpart');return e?(e.getAttribute('data-state')==='checked'?'OK: marcada':'DIFERENTE: '+e.getAttribute('data-state')):'DIFERENTE: sem a caixa'})()", 'label': 'confere Também é cliente marcada'})
    c.mark(3)
    c.click(SALVAR, at=c.A(3, 'Salvar.', 0.6), label='Salvar')
    c.waitfor(text='Cadastro criado também como cliente.', timeout=12)
    c.confere(FICHA_DE('Serralheria Bem-Te-Vi'), ['Cliente+Fornecedor'], 'selo Cliente+Fornecedor na ficha')
    c.hover(TXT('Cliente+Fornecedor', within=FICHA_DE('Serralheria Bem-Te-Vi')), 1.4, at=c.A(3, 'roxo,', 0.5), label='selo roxo Cliente+Fornecedor')
    c.hover(ABA('Clientes'), 0.8, at=c.A(3, 'duas', 0.5), label='as duas abas')
    c.mark(4)
    c.click(LINHA('Depósito Irmãos Siqueira'), at=c.A(4, 'Depósito', 0.6), label='clica no Depósito Irmãos Siqueira')
    c.waitfor(target=SEL(FICHA_DE('Depósito Irmãos Siqueira')), timeout=10)
    c.confere(FICHA_DE('Depósito Irmãos Siqueira'), ['Cliente+Fornecedor', 'R$ 840,00', 'a pagar'], 'ficha do depósito')
    c.add({'do': 'eval', 'js': js_cor('Depósito Irmãos Siqueira', 'vermelho'), 'label': 'confere cor: depósito em Fornecedores (R$ 840,00) vermelho'})
    c.hover(SALDO_FICHA('Depósito Irmãos Siqueira'), 1.4, at=c.A(4, 'cliente', 0.5), label='ficha do depósito: R$ 840,00 a pagar')
    c.mark(5)   # ilustração do saldo unificado
    c.mark(6)
    c.mark(7)
    c.click(ABA('Clientes'), at=c.A(7, 'Clientes,', 0.6), label='aba Clientes')
    c.waitfor(target=BUSCA('cliente'), timeout=10)
    c.confere('main aside', ['Depósito Irmãos Siqueira', '-R$ 840,00'], 'o depósito em Clientes com -R$ 840,00')
    c.add({'do': 'eval', 'js': js_cor('Depósito Irmãos Siqueira', 'vermelho'), 'label': 'confere cor: depósito em Clientes (-R$ 840,00) vermelho'})
    c.hover(NOME_LINHA('Depósito Irmãos Siqueira'), 0.8, at=c.A(7, 'aparece', 0.5), label='zoom: linha do Depósito em Clientes (Cliente+Fornecedor)')
    c.hover(SALDO_ROW('Depósito Irmãos Siqueira'), 2.0, at=c.A(7, 'sinal', 0.5), label='-R$ 840,00 em vermelho')
    c.fim()
    return c


def cap06():
    """Tabela de preço do parceiro: Editar o depósito, Tabela de Preços Padrão Principal -> Tabela Depósitos, o aviso azul, Salvar;
    (ilustração da ordem dos preços) e a aba Preços da ficha."""
    c = cap_novo(6, start=(700, 400))
    c.mark(1)
    c.click(LINHA('Depósito Irmãos Siqueira'), at=c.A(1, 'Depósito', 0.6), label='clica no Depósito Irmãos Siqueira')
    c.waitfor(target=SEL(FICHA_DE('Depósito Irmãos Siqueira')), timeout=10)
    c.mark(2)
    c.click(BTN_FICHA('Depósito Irmãos Siqueira', 'Editar'), at=c.A(2, 'Editar,', 0.6), label='Editar')
    c.waitfor(text='Editar Fornecedor', timeout=10)
    c.ev(DLG_ROLA('Tabela de Preços Padrão', 360, 600), label='desce a janela até a Tabela de Preços Padrão')
    c.click(TABELA_PADRAO, at=c.A(2, 'Principal.', 0.6), label='Tabela de Preços Padrão: Principal (abre a lista)')
    c.click(OPT('Tabela Depósitos'), at=c.A(2, 'troco', 0.3), label='Tabela Depósitos')
    c.mark(3)
    c.ev(js_dlg_topo(), at=c.L(3) - 0.9, label='sobe a janela até o aviso azul')
    c.hover(AVISO_AZUL, 2.4, at=c.A(3, 'aviso', 0.5), label='zoom: aviso azul do cadastro vinculado')
    c.mark(4)
    c.click(SALVAR, at=c.A(4, 'Salvar.', 0.6), label='Salvar')
    c.waitfor(text='Fornecedor atualizado!', timeout=12)
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.mark(5)   # ilustração: qual preço vale na compra
    c.mark(6)
    c.ev(js_abas_ficha(True), at=c.L(6) - 0.9, label='rola a faixa das abas até Preços')
    c.hover(ABA_FICHA('Preços'), 0.6, at=c.A(6, 'ficha', 0.5), label='aba Preços')
    c.click(ABA_FICHA('Preços'), at=c.A(6, 'aba', 0.6), label='aba Preços da ficha: Preços Personalizados (Compra e Venda)')
    c.waitfor(text='Preços Personalizados', timeout=12)
    c.fim()
    return c


def cap07():
    """A ficha do parceiro: Cooperativa Recomeço, cabeçalho, as 7 abas, Visão geral, Acesso ao portal, a aba Lucro estimado."""
    c = cap_novo(7, start=(700, 400))
    c.mark(1)
    c.click(LINHA(COOP), at=c.A(1, 'Cooperativa', 0.6), label='clica na Cooperativa Recomeço: a ficha abre em Visão geral')
    c.waitfor(target=SEL(FC), timeout=10)
    c.confere(FC, ['Cooperativa Recomeço', 'Fornecedor', 'R$ 2.550,00', 'a pagar'], 'cabeçalho da ficha')
    c.mark(2)
    c.hover(SEL(f'{FC} h2, {FC} h1', nth=0), 0.4, at=c.A(2, 'nome,', 0.5), label='nome da cooperativa')
    c.hover(SALDO_FICHA(COOP), 0.5, at=c.A(2, 'saldo', 0.5), label='saldo R$ 2.550,00 a pagar')
    c.hover(BTN_FICHA(COOP, 'Editar'), 0.3, at=c.A(2, 'editar', 0.5), label='Editar')
    c.hover(BTN_FICHA(COOP, 'Nova Movimentação'), 0.6, at=c.A(2, 'lançar', 0.5), label='Nova Movimentação')
    c.mark(3)
    # cada hover custa ~1,1 s (ensaio de 11/11): o cursor para em 5 das 7 abas, na ordem da fala, e a faixa rola de lado antes de Notas fiscais
    for palavra, aba in [('Visão', 'Visão geral'), ('Conta-corrente,', 'Conta-corrente'), ('Lucro', 'Lucro estimado'), ('Notas', 'Notas fiscais'),
                         ('Preços.', 'Preços')]:
        if aba == 'Notas fiscais':
            c.ev(js_abas_ficha(True, 450), at=c.A(3, 'estimado,', -0.3), label='rola a faixa das abas até Preços')
        c.hover(ABA_FICHA(aba), 0.05 if aba == 'Preços' else 0.2, at=c.A(3, palavra, 0.45), label=f'aba {aba}')
    c.mark(4)
    c.hover(TXT('Cadastro', within=FC), 0.8, at=c.A(4, 'cadastro,', 0.5), label='Cadastro')
    c.hover(TXT('Contato e endereço', within=FC), 0.8, at=c.A(4, 'contato', 0.5), label='Contato e endereço')
    c.mark(5)
    c.hover(SEL("input[aria-label='Link do portal']"), 1.6, at=c.A(5, 'link', 0.5), label='zoom: Acesso ao portal, o link e Copiar')
    c.hover(BTN('Copiar', FC), 1.0, at=c.A(5, 'portal', 0.5, nth=1), label='Copiar (sem clicar)')
    c.mark(6)
    c.hover(ABA_FICHA('Lucro estimado'), 2.0, at=c.A(6, 'Lucro', 0.5), label='aba Lucro estimado (sem clicar)')
    c.fim()
    return c


PERIODO = SEL(f"{FC} button:has-text('Período')")
LINHA_LUCRO = lambda mat, col: SEL(f"{FC} tr:has-text('{mat}') td:nth-child({col})")   # 4 compra, 6 venda, 7 margem/kg, 8 margem total
AVISO_FUNGIVEL = 'Estimativa — sucata é fungível; a margem é calculada sobre o preço médio de venda do material no período, não é lucro realizado.'


def cap08():
    """Os materiais que ele mais movimenta: aba Pedidos (cartões, gráfico por peso, legenda), (ilustração peso x valor), Período e a lista."""
    c = cap_novo(8, ficha=COOP, start=(700, 400))
    c.mark(1)
    c.click(ABA_FICHA('Pedidos'), at=c.L(1), label='aba Pedidos')
    c.waitfor(text='Total Comprado', timeout=12)
    c.ev(ANIM, label='animações dos cartões')
    c.confere(FC, ['R$ 52.937,50', 'R$ 3.781,25'], 'cartões Total Comprado e Ticket Médio')
    c.hover(TXT('Total Comprado', within=FC), 0.8, at=c.A(1, 'Desde', 0.5), label='Total Comprado R$ 52.937,50')
    c.hover(TXT('Total de Pedidos', within=FC), 1.4, at=c.A(1, 'catorze', 0.5), label='Total de Pedidos 14')
    c.mark(2)
    c.ev(js_rola_texto('Top 5 Materiais Mais Comprados', 140, 800, escopo=FC), at=c.A(2, 'gráfico', 0.9), label='desce até o gráfico Top 5')
    c.hover(TXT('Top 5 Materiais Mais Comprados', within=FC), 1.2, at=c.A(2, 'peso,', 0.5), label='o gráfico (por peso)')
    c.mark(3)
    c.confere(FC, ['Papelão: 59%', 'Plástico PET: 18%', 'Alumínio latinha: 9%', 'Chaparia: 8%', 'Ferro misto: 6%'], 'legenda do gráfico')
    c.hover(TXT('Papelão: 59%', within=FC, exact=False), 2.0, at=c.A(3, 'papelão', 0.5), label='zoom: legenda, Papelão: 59%')
    c.mark(4)   # ilustração peso x valor
    c.mark(5)
    c.ev(js_ficha_topo(700), at=c.L(5) - 0.9, label='sobe a ficha até a faixa das abas')
    c.hover(PERIODO, 1.0, at=c.A(5, 'Período,', 0.5), label='Período (sem abrir)')
    c.ev(js_rola_texto('Histórico de Pedidos', 140, 800, escopo=FC), at=c.A(5, 'embaixo', 0.9), label='desce até o Histórico de Pedidos')
    c.hover(SEL(f'{FC} tbody tr', nth=0), 1.2, at=c.A(5, 'valor', 0.5), label='cada pedido, com o valor e a data')
    c.fim()
    return c


def cap09():
    """Conta-corrente: Saldo Atual R$ 2.550,00 (vermelho), (ilustração dos quatro casos), o extrato, a Movimentação (Pagar, R$ 1.200,00,
    Pix, observação), Confirmar: R$ 1.350,00; Exportar."""
    c = cap_novo(9, ficha=COOP, start=(700, 400))
    c.mark(1)
    c.click(ABA_FICHA('Conta-corrente'), at=c.A(1, 'conta-corrente.', 0.6), label='aba Conta-corrente')
    c.waitfor(text='Saldo Atual', timeout=12)
    c.confere(FC, ['R$ 2.550,00', 'Você deve a Cooperativa Recomeço'], 'Saldo Atual R$ 2.550,00')
    c.hover(TXT('Saldo Atual', within=FC), 1.4, at=c.A(1, 'deve', 0.5), label='zoom: Saldo Atual R$ 2.550,00 e a frase (L1-L2)')
    c.mark(2)
    c.hover(TXT('Você deve a Cooperativa Recomeço', within=FC, exact=False), 2.0, at=c.A(2, 'frase:', 0.5), label='Você deve a Cooperativa Recomeço')
    for i in (3, 4, 5):
        c.mark(i)   # ilustração: os quatro casos do saldo
    c.mark(6)
    c.ev(js_rola_texto('Histórico de Movimentações', 120, 900, escopo=FC), at=c.L(6) - 0.9, label='desce até o extrato')
    c.hover(SEL(f"{FC} tbody tr:has-text('Pedido')", nth=0), 1.0, at=c.A(6, 'pedido', 0.5), label='linha de Pedido (forma Saldo)')
    c.hover(SEL(f"{FC} tbody tr:has-text('Pagamento')", nth=0), 1.0, at=c.A(6, 'pagamento,', 0.5), label='linha de Pagamento (Pix/Transferência)')
    c.hover(TXT('Saldo Final', within=FC), 1.0, at=c.A(6, 'saldo', 0.5), label='coluna Saldo Final')
    c.mark(7)
    c.ev(js_ficha_topo(700), at=c.L(7) - 0.9, label='sobe até o Saldo Atual')
    c.click(BTN('Movimentação', FC), at=c.A(7, 'parte.', 0.3), label='Movimentação')
    c.waitfor(text='Nova Movimentação de Saldo', timeout=10)
    c.confere('dlg', ['Registre um pagamento ou cobrança para Cooperativa Recomeço', 'Pagar'], 'janela Nova Movimentação de Saldo')
    c.hover(SEL(f'{DLG} label[for=debit]'), 0.8, at=c.A(7, 'vem', 0.5), label='Tipo de Operação: Pagar (já marcado)')
    c.mark(8)
    c.digita(SEL(f'{DLG} #amount'), '1200', c.A(8, 'valor:', 0.6), c.A(8, 'mil', 0.05), 'zoom: Valor R$ 1.200,00')
    c.confere_campos(['1.200'], 'valor R$ 1.200 (o campo mostra 1.200 enquanto digita)')
    c.mark(9)
    c.hover(TXT('Pix/Transferência', within=DLG), 0.8, at=c.A(9, 'Pix', 0.5), label='Pix/Transferência (já marcado: nenhum caixa aberto)')
    c.hover(TXT('Conta bancária', within=DLG, exact=False), 0.6, at=c.A(9, 'conta', 0.5), label='Conta bancária (a principal)')
    c.click(SEL(f'{DLG} #description'), at=c.A(9, 'Observação,', 0.6), label='Observação (clique no campo)')
    c.ev(js_colar('Acerto parcial da entrega de 06/11'), at=c.A(9, 'anoto', 0.1), label='Observação: Acerto parcial da entrega de 06/11 (colado)')
    c.mark(10)
    c.click(BTN('Confirmar', DLG), at=c.A(10, 'Confirmar.', 0.6), label='Confirmar')
    c.waitfor(text='Movimentação registrada com sucesso!', timeout=12)
    c.confere(FC, ['R$ 1.350,00', 'Acerto parcial da entrega de 06/11'], 'saldo R$ 1.350,00 e o pagamento no extrato')
    c.hover(TXT('Saldo Atual', within=FC), 1.4, at=c.A(10, 'mil', 0.5), label='zoom: Saldo Atual R$ 1.350,00 (depois do toast)')
    c.hover(SEL(f"{FC} tbody tr:has-text('Acerto parcial')", nth=0), 1.0, at=c.A(10, 'pagamento', 0.5), label='o pagamento no extrato')
    c.mark(11)
    c.click(BTN('Exportar', FC), at=c.A(11, 'Exportar,', 0.6), label='Exportar (abre o menu)')
    c.hover(ITEM('Abrir Relatório (PDF)'), 0.6, at=c.A(11, 'PDF', 0.5), label='Abrir Relatório (PDF) (sem clicar)')
    c.hover(ITEM('Baixar Excel (.xlsx)'), 0.8, at=c.A(11, 'planilha,', 0.5), label='Baixar Excel (sem clicar)')
    c.press('Escape', at=c.A(11, 'parceiro.', 0.0), label='fecha o menu (Esc)')
    c.fim()
    return c


def cap10():
    """Lucro estimado: Mês passado; latinha e papelão; os cartões; o aviso âmbar; (ilustração sucata é fungível)."""
    c = cap_novo(10, ficha=COOP, start=(700, 400))
    c.mark(1)
    c.click(ABA_FICHA('Lucro estimado'), at=c.A(1, 'Lucro', 0.6), label='aba Lucro estimado')
    c.waitfor(text='Margem estimada por material', timeout=12)
    c.click(SEL(f"{FC} button:has-text('Este mês')"), at=c.A(1, 'escolho', 0.6), label='abre o período (Este mês)')
    c.click({'text': 'Mês passado', 'exact': True}, at=c.A(1, 'Mês', 0.5), label='Mês passado')
    c.waitfor(target=SEL(f"{FC} tr:has-text('Alumínio latinha')"), timeout=12)
    c.confere(FC, ['R$ 18.755,00', 'R$ 5.998,00', '24,2%'], 'cartões de outubro')
    c.mark(2)
    c.hover(LINHA_LUCRO('Alumínio latinha', 4), 0.8, at=c.A(2, 'pagou', 0.5), label='zoom: linhas latinha e papelão; latinha: Preço Médio Compra R$ 6,20')
    c.hover(LINHA_LUCRO('Alumínio latinha', 6), 0.8, at=c.A(2, 'vendeu,', 0.5), label='latinha: Preço Médio Venda R$ 7,40')
    c.hover(LINHA_LUCRO('Alumínio latinha', 7), 1.4, at=c.A(2, 'Sobra', 0.5), label='latinha: Margem R$/kg R$ 1,20')
    c.mark(3)
    c.hover(LINHA_LUCRO('Papelão', 8), 1.8, at=c.A(3, 'dois', 0.5), label='papelão: Margem Total R$ 2.100,00')
    c.mark(4)
    c.hover(TXT('Margem estimada total', within=FC), 1.8, at=c.A(4, 'margem', 0.5), label='cartão Margem estimada total R$ 5.998,00')
    c.mark(5)
    c.hover(TXT(AVISO_FUNGIVEL, within=FC, exact=False), 2.6, at=c.A(5, 'aviso', 0.5), label='zoom: aviso âmbar Estimativa — sucata é fungível')
    c.mark(6)   # ilustração: sucata é fungível
    c.mark(7)
    c.fim()
    return c


def cap11():
    """Financeiro e notas fiscais: Receitas e Despesas vinculadas (frete, sacos de ráfia) e Notas fiscais vazia."""
    c = cap_novo(11, ficha=COOP, start=(700, 400))
    c.mark(1)
    c.click(ABA_FICHA('Financeiro'), at=c.A(1, 'Financeiro.', 0.6), label='aba Financeiro')
    c.waitfor(text='Despesas & Receitas', timeout=12)
    c.ev(ANIM, label='animações dos cartões')
    c.confere(FC, ['Frete das entregas de outubro', 'Venda de sacos de ráfia usados', 'R$ 450,00', 'R$ 120,00'], 'as duas linhas do Financeiro')
    c.hover(TXT('Despesas vinculadas', within=FC), 0.8, at=c.A(1, 'despesas', 0.5), label='Despesas vinculadas')
    c.hover(TXT('Receitas vinculadas', within=FC), 0.8, at=c.A(1, 'receitas', 0.5), label='Receitas vinculadas')
    c.mark(2)
    c.hover(SEL(f"{FC} tr:has-text('Frete das entregas de outubro')"), 1.4, at=c.A(2, 'frete', 0.5), label='zoom: Despesa Frete das entregas de outubro R$ 450,00')
    c.hover(SEL(f"{FC} tr:has-text('Venda de sacos de ráfia usados')"), 1.6, at=c.A(2, 'venda', 0.5), label='Receita Venda de sacos de ráfia usados R$ 120,00')
    c.mark(3)
    c.hover(TXT('Despesas & Receitas', within=FC), 1.0, at=c.A(3, 'lançada', 0.5), label='a lista Despesas & Receitas')
    c.mark(4)
    c.ev(js_abas_ficha(True), at=c.L(4) - 0.9, label='rola a faixa das abas (Notas fiscais inteira)')
    c.click(ABA_FICHA('Notas fiscais'), at=c.A(4, 'Notas', 0.6, nth=0), label='aba Notas fiscais')
    c.waitfor(text='Nenhuma nota fiscal para este parceiro.', timeout=12)
    c.hover(TXT('Nenhuma nota fiscal para este parceiro.', within=FC), 2.0, at=c.A(4, 'nenhuma.', 0.5), label='Nenhuma nota fiscal para este parceiro.')
    c.fim()
    return c


REL = '[role=dialog]'
REL_LINHA = lambda nome: SEL(f"{REL} tr:has-text('{nome}')")
REL_SALDO = lambda nome: SEL(f"{REL} tr:has-text('{nome}') td:nth-child(3)")
OLHO = lambda nome: SEL(f"{REL} tr:has-text('{nome}') button:has(svg.lucide-eye)")


def cap12():
    """Relatório de saldos: A Receber (R$ 19.540,00) e A Pagar (R$ 3.690,00), um caso por frase; Exportar Relatório; o olho da Aços Quiririm
    abre a ficha cheia na conta-corrente."""
    c = cap_novo(12, aba='Clientes', start=(760, 300))
    c.mark(1)
    c.click(SEL("main button[aria-label='Relatório']"), at=c.A(1, 'Lá', 0.6), label='Relatório')
    c.mark(2)
    c.flush(1e9)   # a marca L2 entra antes da espera da janela (sem `at` na espera, ela só sairia no hover seguinte, atrasada)
    c.waitfor(text='Visualize todos os saldos a receber e a pagar', timeout=12)
    c.confere('dlg', ['A Receber', 'R$ 19.540,00', 'Fundição Bandeira do Vale', 'Aços Quiririm Ltda', 'Valdir Pereira'], 'bloco A Receber')
    c.hover(TXT('A Receber', within=REL, exact=False), 1.4, at=c.A(2, 'dezenove', 0.5), label='zoom: bloco A Receber, Total R$ 19.540,00 (L2-L4)')
    c.hover(REL_LINHA('Fundição Bandeira do Vale'), 1.6, at=c.A(2, 'Fundição', 0.5), label='Fundição Bandeira do Vale R$ 14.370,00')
    c.mark(3)
    c.hover(REL_LINHA('Aços Quiririm Ltda'), 1.0, at=c.A(3, 'Aços', 0.5), label='Aços Quiririm Ltda, Cliente')
    c.hover(REL_SALDO('Aços Quiririm Ltda'), 1.4, at=c.A(3, 'verde:', 0.5), label='R$ 4.870,00 em verde')
    c.mark(4)
    c.hover(REL_LINHA('Valdir Pereira'), 1.0, at=c.A(4, 'Valdir', 0.5), label='Valdir Pereira, Fornecedor')
    c.hover(REL_SALDO('Valdir Pereira'), 1.4, at=c.A(4, 'verde.', 0.5), label='-R$ 300,00 em verde')
    c.mark(5)
    c.ev(js_rola_texto('A Pagar', 150, 800, escopo=REL), at=c.L(5) - 0.9, label='desce até A Pagar')
    c.confere('dlg', ['A Pagar', 'R$ 3.690,00', 'Cooperativa Recomeço', 'Depósito Irmãos Siqueira', 'Serra Fina Alumínio Reciclagem'], 'bloco A Pagar')
    c.hover(TXT('A Pagar', within=REL, exact=False), 1.4, at=c.A(5, 'três', 0.5), label='zoom: bloco A Pagar, Total R$ 3.690,00 (L5-L8)')
    nomes = ['Fundição Bandeira do Vale', 'Aços Quiririm Ltda', 'Valdir Pereira', 'Cooperativa Recomeço', 'Depósito Irmãos Siqueira', 'Serra Fina Alumínio Reciclagem']
    c.add({'do': 'eval', 'label': 'confere as cores dos 6 saldos do relatório (os 4 casos)',
           'js': js_cores_rel(nomes, ['verde', 'verde', 'verde', 'vermelho', 'vermelho', 'vermelho'])})
    c.mark(6)
    c.hover(REL_LINHA('Cooperativa Recomeço'), 1.0, at=c.A(6, 'cooperativa', 0.5), label='Cooperativa Recomeço, Fornecedor')
    c.hover(REL_SALDO('Cooperativa Recomeço'), 1.4, at=c.A(6, 'vermelho:', 0.5), label='R$ 1.350,00 em vermelho')
    c.mark(7)
    c.hover(REL_LINHA('Depósito Irmãos Siqueira'), 1.0, at=c.A(7, 'depósito', 0.5), label='Depósito Irmãos Siqueira, Cliente+Fornecedor')
    c.hover(REL_SALDO('Depósito Irmãos Siqueira'), 1.4, at=c.A(7, 'saldo', 0.5), label='-R$ 840,00 em vermelho')
    c.mark(8)
    c.hover(REL_LINHA('Serra Fina Alumínio Reciclagem'), 1.0, at=c.A(8, 'Serra', 0.5), label='Serra Fina Alumínio Reciclagem, Cliente')
    c.hover(REL_SALDO('Serra Fina Alumínio Reciclagem'), 1.6, at=c.A(8, 'vermelho.', 0.5), label='-R$ 1.500,00 em vermelho')
    c.mark(9)
    c.ev(js_dlg_topo(700), at=c.L(9) - 0.9, label='sobe ao topo do relatório')
    c.click(BTN('Exportar Relatório', REL), at=c.A(9, 'Exportar', 0.6), label='Exportar Relatório (abre o menu)')
    c.hover(ITEM('Exportar em PDF'), 0.5, at=c.A(9, 'sai', 0.3), label='Exportar em PDF (sem clicar)')
    c.hover(ITEM('Exportar em Excel'), 0.3, at=c.A(9, 'ou', 0.3), label='Exportar em Excel (sem clicar)')
    c.mark(10)
    c.press('Escape', at=c.L(10) - 0.9, label='fecha o menu (Esc)')
    c.click(OLHO('Aços Quiririm Ltda'), at=c.A(10, 'olho,', 0.6), label='olho da Aços Quiririm: abre a conta-corrente')
    c.waitfor(text='Conta-Corrente do Cliente', timeout=15)
    c.confere('main', ['Aços Quiririm Ltda', 'R$ 4.870,00'], 'a ficha cheia na conta-corrente')
    c.hover(TXT('Conta-Corrente do Cliente', exact=False), 1.4, at=c.A(10, 'extrato', 0.5), label='Conta-Corrente do Cliente, com o extrato')
    c.fim()
    return c


def cap13():
    """Recapitulando (a montagem da edição usa trechos dos capítulos; este passeio pelo estado final fica de reserva): o Rogério e a
    serralheria na lista, o selo Cliente+Fornecedor, a ficha da cooperativa e o Relatório de Saldos. L6 é o cartão Próximo."""
    c = cap_novo(13, start=(760, 300))
    c.mark(1)
    c.hover(NOME_LINHA('Rogério Alves Costa'), 1.4, at=c.A(1, 'Rogério,', 0.5), label='Rogério Alves Costa (pessoa física)')
    c.mark(2)
    c.hover(FISCAL_OK('Serralheria Bem-Te-Vi'), 1.4, at=c.A(2, 'serralheria', 0.5), label='a serralheria com o sinal verde')
    c.mark(3)
    c.click(LINHA('Serralheria Bem-Te-Vi'), at=c.A(3, 'Marcou', 0.6), label='a ficha da serralheria (Cliente+Fornecedor)')
    c.waitfor(target=SEL(FICHA_DE('Serralheria Bem-Te-Vi')), timeout=10)
    c.hover(TXT('Cliente+Fornecedor', within=FICHA_DE('Serralheria Bem-Te-Vi')), 1.2, at=c.A(3, 'cliente', 0.5), label='selo Cliente+Fornecedor')
    c.mark(4)
    c.click(LINHA(COOP), at=c.A(4, 'Abriu', 0.6), label='a ficha da cooperativa')
    c.waitfor(target=SEL(FC), timeout=10)
    c.hover(ABA_FICHA('Pedidos'), 0.4, at=c.A(4, 'gráfico', 0.5), label='aba Pedidos')
    c.hover(ABA_FICHA('Conta-corrente'), 0.4, at=c.A(4, 'pagamento', 0.5), label='aba Conta-corrente')
    c.hover(ABA_FICHA('Lucro estimado'), 0.6, at=c.A(4, 'lucro', 0.5), label='aba Lucro estimado')
    c.mark(5)
    c.click(SEL("main button[aria-label='Relatório']"), at=c.A(5, 'relatório', 0.6), label='Relatório de Saldos')
    c.waitfor(text='Visualize todos os saldos a receber e a pagar', timeout=12)
    c.mark(6)
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
                if stp['at'] < last - 1e-9:
                    print(f'  aviso cap{n:02d}: at {stp["at"]} < {last} em "{stp.get("label") or stp.get("name")}"')
                last = max(last, stp['at'])
        path = os.path.join(HERE, f'cap{n:02d}.json')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
        est = ' (voz ESTIMADA)' if c.estimado else ''
        print(f'cap{n:02d}: {len(d["steps"])} passos, narração {c.dur:.1f} s{est} -> {os.path.relpath(path, HERE)}')
