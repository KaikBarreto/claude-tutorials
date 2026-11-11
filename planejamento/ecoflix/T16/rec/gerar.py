#!/usr/bin/env python3
"""T16 · gera rec/t16/cap00..cap18.json (roteiros do robô) a partir da voz (t16/narracao/capNN.json).

Nota Fiscal de mercadoria (NF-e) no COMPUTADOR (janela 1280x800), logado como Rafael Nogueira (MASTER, Recicla Vale Metais), EcoSistema
1.59.154. FAKE_NOW 2026-11-10T08:30:00-03:00 (terça) em todos os capítulos. Emissão, certificado, SEFAZ e notas recebidas simulados no
Supabase falso (rec/mundo/handlers: plugnotas-*, get_invoices_paged, get_next_invoice_number, search_orders_for_invoice,
certificate_vault_status, dfe_inbound_import_enqueue + a fila dfe_inbound_import_jobs; lib/nfe.mjs): nada sai da máquina.
Cada passo é preso a uma palavra da fala: `at` = início da palavra − o custo do gesto (A(linha, palavra, folga)), para o cursor CHEGAR
na palavra (docs/04, "Custo real dos gestos"). Hoje a voz é ESTIMADA (capNN.json do preparar_aula.sh); com a voz real, rode de novo.
Rodar de qualquer pasta: `python3 -I rec/t16/gerar.py [NN ...]`. Depois: t16_ensaio.sh NN (ensaio rápido; --semente grava o
apos-capNN), prever.py NN --ens, t16_ensaio.sh NN completo.

Cadeia de sementes (rec/mundo/seeds-extra/t16/, t16_sementes.py): `inicio` (a demonstração fiscal sobre B: configuração da matriz sem
certificado nem dados, sem série, notas, transportadora e cenário; as notas recebidas 2157 e 884) nos caps 0 a 3; depois cada capítulo
parte do `apos-capNN` do anterior que mexeu no banco (SEMENTE abaixo).
"""
import hashlib
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TUT_HOME = os.path.normpath(os.path.join(HERE, '..', '..'))
NARR = os.path.join(TUT_HOME, 't16', 'narracao')
FAKE_NOW = '2026-11-10T08:30:00-03:00'
NOMES = ['Abertura', 'Onde ficam as notas', 'O certificado vem primeiro', 'Subindo o certificado A1', 'Empresa e impostos',
         'Cenários fiscais', 'Série e numeração', 'Transportadora e serviços', 'A cota de documentos', 'Nota avulsa, do zero',
         'Nota a partir de um pedido', 'Nota de um caixa fechado', 'Cancelar e corrigir', 'Inutilizar numeração', 'DANFE e XML',
         'As notas recebidas', 'Manifestar a nota', 'Importar pelo XML', 'Recapitulando']
_I = ['t16/inicio']
_A = lambda n: _I + [f't16/apos-cap{n:02d}']
# cadeia (plano.md): 00-03 partem de `inicio`; cada um dos outros parte do estado deixado pelo anterior que mexeu no banco
SEMENTE = {0: _I, 1: _I, 2: _I, 3: _I, 4: _A(3), 5: _A(4), 6: _A(5), 7: _A(6), 8: _A(7), 9: _A(7), 10: _A(9), 11: _A(10),
           12: _A(11), 13: _A(12), 14: _A(13), 15: _A(14), 16: _A(15), 17: _A(16), 18: _A(17)}
PFX = 'assets/recicla-vale-metais-a1.pfx'                  # relativos ao roteiro (rec/t16/): t16_sementes.py assets
XML_COOP = 'assets/NFe-3871-Cooperativa-Recomeco.xml'

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
        if texto_atual(n) != [norm(w['w']) for w in words if norm(w['w'])]:
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

    def tem(s, i, palavra):
        return any(w['linha'] == i - 1 and norm(w['w']) == norm(palavra) for w in s.words)

    def A_ou(s, i, palavras, folga=0.6):
        """âncora na 1ª palavra da lista que existe na linha (fala de hoje ou a proposta em propostas_fala.md)"""
        for p in palavras:
            if any(w['linha'] == i - 1 and norm(w['w']) == norm(p) for w in s.words):
                return s.A(i, p, folga, nth=0)
        raise SystemExit(f'cap{s.n:02d}: nenhuma de {palavras} na linha {i}')

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

    def digita(s, campo, text, at_clique, at_texto, label, cps=40, clear=False):
        """clique no campo (ancorado) e digitação sem novo clique, ancorada na palavra (docs/04, "Digitar sem esperar")"""
        s.click(campo, at=at_clique, label=label + ' (clique no campo)')
        kw = {'noClick': True}
        if clear:
            kw['clear'] = True
        return s.type(campo, text, at=at_texto, label=label, cps=cps, **kw)

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

    def upload(s, target, arquivo, at=None, label=None, **kw):
        return s._p({'do': 'upload', 'target': target, 'file': arquivo}, at, label, kw)

    def rolar(s, by, at=None, label=None, ponto=(800, 470), duration=0.5, after=100):
        return s._p({'do': 'scroll', 'point': {'x': ponto[0], 'y': ponto[1]}, 'by': by, 'duration': duration, 'after': after}, at, label, {})

    def confere(s, escopo, esperados, label, tentativas=20):
        """`eval` que LÊ a tela e compara com a fala: "OK: ..." ou "DIFERENTE: ..." (o resumo.py acusa). Escopo: 'dlg' (a última
        janela aberta), 'main', 'body' ou um seletor CSS. Tenta por ~tentativas x 0,3 s."""
        linha = escopo[4:] if escopo.startswith('row:') else None   # 'row:<texto>': a linha da lista que contém o texto
        sel = 'main tbody tr' if linha is not None else {'dlg': '[role=dialog],[role=alertdialog]', 'main': 'main', 'body': 'body'}.get(escopo, escopo)
        esp = [esperados] if isinstance(esperados, str) else list(esperados)
        js = ("(async()=>{const norm=t=>t.replace(/[\\s\\u00a0]+/g,' ').toLowerCase();const esp=%s;let out='';"
              "for(let i=0;i<%d;i++){const els=[...document.querySelectorAll(%s)].filter(e=>!%s||e.innerText.includes(%s));const el=%s?els[els.length-1]:els[0];"
              "if(!el){out='DIFERENTE: sem elemento';}else{const t=norm(el.innerText);const falta=esp.filter(e=>!t.includes(norm(e)));"
              "if(!falta.length)return 'OK: '+esp.join(' | ');out='DIFERENTE: faltou '+JSON.stringify(falta)+' em: '+t.slice(0,240);}"
              "await new Promise(r=>setTimeout(r,300));}return out})()") % (json.dumps(esp, ensure_ascii=False), tentativas, json.dumps(sel),
                                                                            'true' if linha is not None else 'false', json.dumps(linha or ''),
                                                                            'true' if escopo == 'dlg' else 'false')
        return s.add({'do': 'eval', 'js': js, 'label': 'confere ' + label})

    def confere_campos(s, esperados, label, escopo='[role=dialog]'):
        """lê o VALOR dos campos (input/textarea) do escopo e compara com a fala"""
        esp = [esperados] if isinstance(esperados, str) else list(esperados)
        js = ("(async()=>{const esp=%s;let out='';for(let i=0;i<12;i++){const v=[...document.querySelectorAll(%s+' input, '+%s+' textarea')].map(e=>e.value).join(' | ');"
              "const falta=esp.filter(e=>!v.includes(e));if(!falta.length)return 'OK: '+esp.join(' | ');out='DIFERENTE: faltou '+JSON.stringify(falta)+' em: '+v.slice(0,260);"
              "await new Promise(r=>setTimeout(r,300));}return out})()") % (json.dumps(esp, ensure_ascii=False), json.dumps(escopo), json.dumps(escopo))
        return s.add({'do': 'eval', 'js': js, 'label': 'confere ' + label})

    def confere_ausente(s, escopo, texto, label, espera=0.6):
        """LÊ a tela depois de `espera` s e acusa se o texto apareceu"""
        sel = {'dlg': '[role=dialog]', 'main': 'main', 'body': 'body'}.get(escopo, escopo)
        js = ("(async()=>{await new Promise(r=>setTimeout(r,%d));" % int(espera * 1000) + "const el=document.querySelector(%s);"
              "const t=(el?el.innerText:'').replace(/[\\s\\u00a0]+/g,' ').toLowerCase();"
              "return t.includes(%s)?'DIFERENTE: apareceu '+%s:'OK: ausente '+%s})()") % (json.dumps(sel), json.dumps(texto.lower()), json.dumps(texto), json.dumps(texto))
        return s.add({'do': 'eval', 'js': js, 'label': 'confere ' + label})

    def fim(s):
        s.flush(1e9)
        s.steps.append({'do': 'eval', 'js': 'JSON.stringify(window.__avisos || "sem observador")', 'label': 'avisos de erro na tela'})
        s.steps.append({'do': 'mark', 'name': 'FIM', 'at': round(s.dur, 2)})

    def encaixa_hovers(s, custo=0.9, minimo=0.15):
        """o hover termina antes do próximo passo com `at` (uma marca Ln, outro gesto): parada (`seconds`) encurtada até caber"""
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
            'name': f't16-cap{s.n:02d}',
            'title': f'T16 · Cap. {s.n} · {NOMES[s.n]} (narração{est} {str(round(s.dur, 1)).replace(".", ",")} s; marcas L1..L{len(s.linhas)} = '
                     f'início de cada linha do roteiro; FAKE_NOW {FAKE_NOW}; logado como Rafael Nogueira)',
            'seed': f't16-cap{s.n:02d}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
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
AGUARDA = {'do': 'waitFor', 'idle': True}


def stable_id(chave):
    """o mesmo UUID do `@id:<chave>` das sementes (rec/fakebase/core/util.mjs, stableId)"""
    h = bytearray(hashlib.sha1(('domiflix-fake:' + chave).encode()).digest())
    h[6] = (h[6] & 0x0F) | 0x50
    h[8] = (h[8] & 0x3F) | 0x80
    x = h[:16].hex()
    return f'{x[:8]}-{x[8:12]}-{x[12:16]}-{x[16:20]}-{x[20:32]}'


RAFAEL = stable_id('user.rafael')
VERSAO = '1.59.154'
HOJE = FAKE_NOW[:10]
STORAGE = {'app_version': VERSAO, 'notification_shown_version': VERSAO, 'pwa-install-dismissed': 'true', 'theme': 'light',
           f'daily-tasks-reminder-last-shown-{RAFAEL}': HOJE, 'initial-preferences-set': 'true'}
LOGIN = [{'do': 'waitFor', 'target': {'label': 'E-mail'}, 'timeout': 30},
         {'do': 'type', 'target': {'label': 'E-mail'}, 'text': '$TUT_USER', 'cps': 40},
         {'do': 'type', 'target': {'label': 'Senha', 'exact': True}, 'text': '$TUT_SENHA', 'cps': 40},
         {'do': 'click', 'target': {'role': 'button', 'name': 'Entrar', 'exact': True}},
         {'do': 'waitFor', 'text': 'Olá, Rafael!', 'timeout': 30}, AGUARDA]


# ---------------------------------------------------------------- JavaScript (rolagens suaves, colar)
ACHA_ROLAGEM = ("const rolagem=(el)=>{let c=el&&el.parentElement;while(c&&c!==document.body){const s=getComputedStyle(c);"
                "if(/(auto|scroll)/.test(s.overflowY)&&c.scrollHeight>c.clientHeight+4)return c;c=c.parentElement;}return null};")
SUAVE = ("await new Promise(res=>{const t0=performance.now();const f=t=>{const p=Math.min(1,(t-t0)/DUR),e=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;"
         "c.scrollTop=y0+dy*e;p<1?requestAnimationFrame(f):res()};requestAnimationFrame(f)});")


def js_rola(seletor, y, dur_ms=700):
    """rolagem suave do contêiner que rola o elemento `seletor` até o topo dele ficar em y px CSS (limitado ao que o contêiner rola).
    Devolve o topo final, 'ok' (já estava), 'SEM ALVO' ou 'SEM ROLAGEM'."""
    return ("(async()=>{" + ACHA_ROLAGEM + f"const el=[...document.querySelectorAll({json.dumps(seletor)})].filter(e=>e.offsetParent)[0];if(!el)return 'SEM ALVO';"
            "const c=rolagem(el);if(!c)return 'SEM ROLAGEM';"
            f"let dy=Math.round(el.getBoundingClientRect().top-{int(y)});const y0=c.scrollTop;dy=Math.max(-y0,Math.min(c.scrollHeight-c.clientHeight-y0,dy));"
            "if(Math.abs(dy)<3)return 'ok';" + SUAVE.replace('DUR', str(int(dur_ms))) + "return Math.round(el.getBoundingClientRect().top)})()")


def js_rola_linha(texto, y, dur_ms=700):
    """como js_rola, com o alvo = a 1ª linha da lista (main tbody tr) cujo texto contém `texto` (CSS puro não tem :has-text)"""
    return ("(async()=>{" + ACHA_ROLAGEM + f"const acha=()=>[...document.querySelectorAll('main tbody tr')].filter(e=>e.offsetParent&&e.innerText.includes({json.dumps(texto)}))[0];"
            "let el=acha();for(let i=0;i<20&&!el;i++){await new Promise(r=>setTimeout(r,150));el=acha();}"
            "if(!el)return 'SEM ALVO';const c=rolagem(el);if(!c)return 'SEM ROLAGEM';"
            f"let dy=Math.round(el.getBoundingClientRect().top-{int(y)});const y0=c.scrollTop;dy=Math.max(-y0,Math.min(c.scrollHeight-c.clientHeight-y0,dy));"
            "if(Math.abs(dy)<3)return 'ok';" + SUAVE.replace('DUR', str(int(dur_ms))) + "return Math.round(el.getBoundingClientRect().top)})()")


def js_rola_texto(texto, y, dur_ms=700, escopo=DLG):
    """como js_rola, com o alvo achado pelo texto (o menor elemento do escopo cujo texto é exatamente `texto`)"""
    return ("(async()=>{" + ACHA_ROLAGEM + f"const el=[...document.querySelectorAll({json.dumps(escopo + ' *')})].filter(e=>e.textContent.trim()==={json.dumps(texto)}&&e.offsetParent)"
            ".sort((a,b)=>a.textContent.length-b.textContent.length||a.children.length-b.children.length)[0];if(!el)return 'SEM ALVO';"
            "const c=rolagem(el);if(!c)return 'SEM ROLAGEM';"
            f"let dy=Math.round(el.getBoundingClientRect().top-{int(y)});const y0=c.scrollTop;dy=Math.max(-y0,Math.min(c.scrollHeight-c.clientHeight-y0,dy));"
            "if(Math.abs(dy)<3)return 'ok';" + SUAVE.replace('DUR', str(int(dur_ms))) + "return Math.round(el.getBoundingClientRect().top)})()")


def js_topo(dur_ms=700):
    """rolagem suave do <main> (o contêiner que rola a tela) até o topo"""
    return ("(async()=>{const c=[...document.querySelectorAll('main')].find(e=>/(auto|scroll)/.test(getComputedStyle(e).overflowY)&&e.scrollHeight>e.clientHeight+4);"
            "if(!c)return 'SEM ROLAGEM';const y0=c.scrollTop,dy=-y0;if(y0<3)return 'ok';" + SUAVE.replace('DUR', str(int(dur_ms))) + "return 'topo:'+Math.round(c.scrollTop)})()")


def js_colar(texto):
    """cola o texto no campo em foco (execCommand insertText: o React recebe o input), ~0,05 s em vez de digitar letra a letra"""
    return ("(()=>{const e=document.activeElement;if(!e||!/^(INPUT|TEXTAREA)$/.test(e.tagName))return 'SEM ALVO (nada em foco)';"
            f"document.execCommand('insertText',false,{json.dumps(texto)});return e.value}})()")



# ---------------------------------------------------------------- alvos da NF-e (EcoSistema 1.59.154; conferidos em rec/t16/_ex/)
MENU_FISCAL = SEL("button:has(span:text-is('Fiscal & Ambiental'))")      # grupo do menu lateral
SUBMENU = lambda n: SEL(f"a:has-text('{n}')")                            # itens do submenu (links)
SUBABA_ID = {'Entrada': 'entrada', 'Saída': 'saida', 'Notas Recebidas': 'notas-recebidas', 'Inutilizadas': 'inutilizadas'}
SUBABA = lambda t: SEL(f"#tab-btn-{SUBABA_ID[t]}")                       # sub-abas da NF-e (botões underline com id; e2)
CFG_BTN = BTN('Configurações Fiscais', MAIN)
NOVA_NOTA = BTN('Nova Nota', MAIN)
MAIS = SEL("main button[aria-label='Mais opções de NF-e']")
COTA = SEL("main :text-matches('^[0-9.]+/[0-9.]+ Documentos$')")
CARTAO = lambda t: SEL(f"main :text-is('{t}')")
SECAO_ID = {'Certificado': 'certificado', 'Empresa': 'empresa', 'Impostos (padrão)': 'impostos', 'Cenários': 'cenarios',
            'Numeração': 'numeracao', 'Transportadora': 'transportadora', 'Serviços': 'servicos'}
TRILHO = lambda t: SEL(f"#tab-btn-{SECAO_ID[t]}")                        # seções da Configuração Fiscal: abas no alto (underline; e2)
VAZIO = 'Nenhuma nota fiscal encontrada'                                 # lista vazia (Entrada e Saída)
LINHA = lambda t: SEL(f"main tbody tr:has-text('{t}')")
TRIG = lambda t: SEL(f"main tbody tr:has-text('{t}') td:last-child button")   # "⋯" da linha (HoverDropdownMenu: abre no hover)
ITEM = lambda n: {'role': 'menuitem', 'name': n}
TRIG_REC = lambda t: SEL(f"main tr:has-text('{t}') button[title='Ações']")   # menu da nota recebida (DropdownMenu: abre no clique)
DLG_BTN = lambda t: SEL(f"{DLG} button:has-text('{t}')")
DLG_TXT = lambda t: SEL(f"{DLG} :text-is('{t}')")
CAMPO = lambda i: SEL(f'#{i}')
COMBO = lambda escopo, txt: SEL(f"{escopo} button[role=combobox]:has-text('{txt}')")
ROD = lambda t: SEL(f"{DLG} button:text-is('{t}')")                      # rodapé fixo da nota (y ~731): noScroll


def setup_nfe(aba='saida', espera='Notas Fiscais (NF-e)', extra=()):
    return LOGIN + [{'do': 'goto', 'url': f'/fiscal-ambiental/nfe/{aba}'}, {'do': 'waitFor', 'text': espera, 'timeout': 30}, AGUARDA,
                    *extra, {'do': 'eval', 'js': ANIM}]


def setup_cfg(secao, espera, extra=()):
    return LOGIN + [{'do': 'goto', 'url': f'/fiscal-ambiental/configuracao/{secao}'}, {'do': 'waitFor', 'text': espera, 'timeout': 30},
                    AGUARDA, *extra, {'do': 'eval', 'js': ANIM}]


def colar(c, campo, texto, at_clique, at_texto, label):
    """clica no campo (cursor) e cola o texto (sem digitar letra a letra): texto longo que a fala só cita"""
    c.click(campo, at=at_clique, label=label + ' (clique no campo)')
    return c.ev(js_colar(texto), at=at_texto, label=label)


def menu_item(c, linha, item, at, label, at_menu=None):
    """menu "⋯" de uma linha da lista (HoverDropdownMenu: abre no hover e um clique no gatilho FECHA): hover no gatilho, hover
    condicional logo antes do item (o menu pode ter fechado) e clique no item sem rolar (docs/08, T14 cap09)"""
    if at_menu is not None:
        c.hover(TRIG(linha), 0.3, at=at_menu, label=f'abre o menu da linha {linha}', noScroll=True)
    c.hover(TRIG(linha), 0.15, label=f'(menu {linha} aberto)', noScroll=True, unless=ITEM(item))
    return c.click(ITEM(item), at=at, label=label, noScroll=True)


def espera_status(c, linha, status, label, timeout=20):
    """espera o selo da linha (o polling de status do app roda a cada 5 s)"""
    return c.waitfor(selector=f"main tbody tr:has-text('{linha}'):has-text('{status}')", timeout=timeout)


# ================================================================ capítulos
def cap00():
    """Abertura: o Dashboard sob a ilustração (L1, L2); na L3 o cursor passa pelo grupo "Fiscal & Ambiental" do menu lateral (o cartão
    "Módulo Notas Fiscais" e o "Antes:" são da edição)."""
    setup = LOGIN + [{'do': 'eval', 'js': ANIM}]
    c = Cap(0, setup=setup, start=(700, 360))
    for i in (1, 2, 3):
        c.mark(i)
    c.hover(MENU_FISCAL, 2.0, at=c.A(3, 'Fiscal', 0.7), label='o grupo Fiscal & Ambiental no menu lateral')
    c.mark(4)
    c.rolar(0, at=c.A(4, 'Se', 0.2), ponto=(760, 420), label='o cursor sai do menu')
    c.fim()
    return c


def cap01():
    """Onde ficam as notas: o grupo Fiscal & Ambiental (L1), os itens do submenu (L2), Notas Fiscais (NF-e) (L3), as sub-abas (L4),
    a ilustração entrada x saída (L5), Notas Recebidas e Inutilizadas (L6) e o cabeçalho: Configurações Fiscais, cota, cartões e Nova
    Nota (L7)."""
    setup = LOGIN + [{'do': 'eval', 'js': ANIM}]
    c = Cap(1, setup=setup, start=(700, 360))
    c.mark(1)
    c.click(MENU_FISCAL, at=c.A(1, 'Fiscal', 0.8), label='abre o grupo Fiscal & Ambiental')
    c.mark(2)
    c.hover(SUBMENU('Notas Fiscais (NF-e)'), 0.3, at=c.A(2, 'mercadoria,', 0.6), label='Notas Fiscais (NF-e)')
    c.hover(SUBMENU('Notas de Serviço (NFS-e)'), 0.3, at=c.A(2, 'serviço,', 0.6), label='Notas de Serviço (NFS-e)')
    c.hover(SUBMENU('Transporte (MDF-e)'), 0.3, at=c.A(2, 'transporte,', 0.6), label='Transporte (MDF-e)')
    c.hover(SUBMENU('Ambiental (MTR/CDF)'), 0.3, at=c.A(2, 'ambiental', 0.6), label='Ambiental (MTR/CDF)')
    c.hover(SUBMENU('Estoque Fiscal'), 0.3, at=c.A(2, 'estoque', 0.6), label='Estoque Fiscal')
    c.hover(SUBMENU('Notas Fiscais (NF-e)'), 0.5, at=c.A(2, 'mercadoria.', 0.6, nth=1), label='volta às Notas Fiscais (NF-e)')
    c.mark(3)
    c.click(SUBMENU('Notas Fiscais (NF-e)'), at=c.A(3, 'Notas', 0.6), label='Notas Fiscais (NF-e) (tela abre na sub-aba Entrada)')
    c.waitfor(text=VAZIO, timeout=15)
    c.ev(ANIM)
    c.mark(4)
    c.hover(SUBABA('Entrada'), 0.3, at=c.A(4, 'Entrada,', 0.6), label='sub-aba Entrada')
    c.hover(SUBABA('Saída'), 0.3, at=c.A(4, 'Saída,', 0.6), label='sub-aba Saída')
    c.hover(SUBABA('Notas Recebidas'), 0.3, at=c.A(4, 'Recebidas', 0.6), label='sub-aba Notas Recebidas')
    c.hover(SUBABA('Inutilizadas'), 0.6, at=c.A(4, 'Inutilizadas.', 0.6), label='sub-aba Inutilizadas')
    c.mark(5)
    c.mark(6)
    c.hover(SUBABA('Notas Recebidas'), 0.8, at=c.A(6, 'Recebidas', 0.6), label='zoom: Notas Recebidas')
    c.hover(SUBABA('Inutilizadas'), 0.8, at=c.A(6, 'Inutilizadas', 0.6), label='zoom: Inutilizadas')
    c.mark(7)
    c.hover(CFG_BTN, 0.5, at=c.A(7, 'Configurações', 0.6), label='Configurações Fiscais')
    c.hover(COTA, 0.4, at=c.A(7, 'cota', 0.6), label='selo da cota 0/1.000 Documentos', noScroll=True)
    c.hover(CARTAO('Notas Emitidas'), 0.3, at=c.A(7, 'emitidas,', 0.6), label='cartão Notas Emitidas')
    c.hover(CARTAO('Notas Pendentes'), 0.3, at=c.A(7, 'pendentes', 0.6), label='cartão Notas Pendentes')
    c.hover(CARTAO('Rejeitadas/Canceladas'), 0.3, at=c.A(7, 'rejeitadas', 0.6), label='cartão Rejeitadas/Canceladas')
    c.hover(NOVA_NOTA, 1.2, at=c.A(7, 'Nova', 0.6), label='botão Nova Nota (sem clicar)')
    c.fim()
    return c


def cap02():
    """O certificado vem primeiro: Configurações Fiscais (L1), os grupos do trilho (L2), as seções apagadas (L3), ilustração (L4), o
    aviso "Passo 1 de 3" (L5) e o cartão do certificado (L6)."""
    c = Cap(2, setup=setup_nfe('entrada', VAZIO), start=(760, 400))
    c.mark(1)
    c.click(CFG_BTN, at=c.A(1, 'Configurações', 0.7), label='Configurações Fiscais')
    c.waitfor(text='Tudo que a SEFAZ precisa saber antes da primeira nota.', timeout=15)
    c.ev(ANIM)
    c.mark(2)
    if c.tem(2, 'emissão,'):   # fala de hoje ("em três grupos"): na 1.59.154 as seções são abas no alto, sem grupos (propostas_fala.md)
        c.hover(TRILHO('Certificado'), 0.3, at=c.A(2, 'seções,', 0.6), label='as seções no alto (abas)')
        c.hover(TRILHO('Empresa'), 0.3, at=c.A(2, 'emissão,', 0.6), label='Certificado e Empresa')
        c.hover(TRILHO('Cenários'), 0.3, at=c.A(2, 'regras', 0.6), label='Impostos e Cenários')
        c.hover(TRILHO('Serviços'), 0.6, at=c.A(2, 'documentos.', 0.6), label='Numeração, Transportadora e Serviços')
    else:                      # fala proposta: "Em cima ficam as seções, na ordem em que se preenche: do certificado até os serviços."
        c.hover(TRILHO('Certificado'), 0.5, at=c.A(2, 'certificado', 0.6), label='as seções no alto: Certificado')
        c.hover(TRILHO('Serviços'), 0.8, at=c.A(2, 'serviços.', 0.6), label='até Serviços')
    c.mark(3)
    c.hover(TRILHO('Empresa'), 0.3, at=c.A(3, 'Empresa,', 0.6), label='Empresa (apagada)')
    c.hover(TRILHO('Impostos (padrão)'), 0.3, at=c.A(3, 'Impostos,', 0.6), label='Impostos (apagada)')
    c.hover(TRILHO('Numeração'), 0.3, at=c.A(3, 'Numeração', 0.6), label='Numeração (apagada)')
    c.hover(TRILHO('Transportadora'), 0.6, at=c.A(3, 'Transportadora', 0.6), label='Transportadora (apagada)')
    c.marcar(TRILHO('Empresa'), at=c.A(3, 'precisa', 0.3), label='zoom: as seções apagadas com "precisa do certificado digital"')
    c.mark(4)
    c.mark(5)
    c.hover(TXT('Passo 1 de 3:', exact=False), 1.0, at=c.A(5, 'ordem', 0.6), label='zoom: aviso Passo 1 de 3')
    c.mark(6)
    c.hover(TXT('Certificado Digital A1'), 1.2, at=c.A(6, 'dica:', 0.4), label='o cartão Certificado Digital A1')
    c.fim()
    return c


def cap03():
    """Subindo o certificado A1: o cartão vazio (L1), Selecionar arquivo + o .pfx (L2), a senha (mascarada) e a ajuda (L3), Validar
    Certificado (L4), o nome e a validade (L5, zoom), ilustração (L6), Substituir e Próximo (L7)."""
    c = Cap(3, setup=setup_cfg('certificado', 'Certificado não configurado'), start=(760, 400))
    c.mark(1)
    c.hover(TXT('Certificado não configurado'), 0.6, at=c.A(1, 'certificado.', 0.5), label='Certificado não configurado')
    c.hover(TXT('Certificado Digital A1'), 0.8, at=c.A(1, 'A1,', 0.6), label='Certificado Digital A1')
    c.mark(2)
    c.hover(TXT('Arquivo do Certificado (.pfx ou .p12)'), 0.3, at=c.A(2, 'Arquivo', 0.6), label='Arquivo do Certificado')
    c.upload(BTN('Selecionar arquivo', MAIN), PFX, at=c.A(2, 'Selecionar', 0.8), label='Selecionar arquivo: recicla-vale-metais-a1.pfx')
    c.mark(3)
    c.click(CAMPO('certificado-senha'), at=c.A(3, 'Senha', 0.7), label='Senha do Certificado (clique no campo)')
    c.type(CAMPO('certificado-senha'), '$TUT_SENHA', at=c.A(3, 'senha', 0.05, nth=1), label='digita a senha (pontos)', cps=40, noClick=True)
    c.hover(CAMPO('certificado-senha-ajuda'), 0.8, at=c.A(3, 'empresa.', 0.7), label='zoom: Use a senha do próprio certificado')
    c.mark(4)
    c.click(BTN('Validar Certificado', MAIN), at=c.A(4, 'Validar', 0.7), label='Validar Certificado')
    c.waitfor(text='Certificado validado!', timeout=15)
    c.mark(5)
    c.marcar(TXT('RECICLA VALE METAIS LTDA', exact=False), at=c.A(5, 'Embaixo', 0.3), label='zoom: nome do certificado e Válido até 14/09/2027')
    c.hover(TXT('Válido até 14/09/2027'), 1.2, at=c.A(5, 'catorze', 0.6), label='chip Válido até 14/09/2027')
    c.mark(6)
    c.mark(7)
    c.hover(BTN('Substituir Certificado', MAIN), 0.8, at=c.A(7, 'Substituir', 0.6), label='zoom: Substituir Certificado')
    c.hover(BTN('Próximo: Configurar Empresa', MAIN), 1.2, at=c.A(7, 'Próximo', 0.6), label='zoom: Próximo: Configurar Empresa (sem clicar)')
    c.fim()
    return c


IE_RECICLA = '688123456117'          # a do mundo base (company_fiscal_config de B), dígitos de SP válidos


def cap04():
    """Empresa e impostos: Próximo (L1), Importar dados (L2), razão social completa e IE (L3, zoom CNPJ e IE), Endereço Fiscal (L4),
    Impostos: regime Lucro Real (L5), o quadro (L6), ICMS (L7), CFOPs (L8), IBS/CBS ligado com os códigos (L9), ilustração (L10),
    Salvar configuração (L11)."""
    c = Cap(4, setup=setup_cfg('certificado', 'Certificado validado!'), start=(760, 400))
    c.mark(1)
    c.click(BTN('Próximo: Configurar Empresa', MAIN), at=c.A(1, 'dados', 0.7), label='Próximo: Configurar Empresa')
    c.waitfor(text='Passo 2 de 3:', timeout=10)
    c.mark(2)
    c.click(BTN('Importar dados', MAIN), at=c.A(2, 'Importar', 0.7), label='Importar dados')
    c.hover(CAMPO('empresa-razao-social'), 0.25, at=c.A(2, 'nome,', 0.6), label='o nome importado')
    c.hover(CAMPO('empresa-cnpj'), 0.25, at=c.A(2, 'CNPJ,', 0.6), label='o CNPJ importado')
    c.hover(CAMPO('empresa-telefone'), 0.25, at=c.A(2, 'telefone', 0.6), label='o telefone importado')
    c.hover(CAMPO('empresa-email'), 0.4, at=c.A(2, 'e-mail.', 0.6), label='o e-mail importado')
    c.mark(3)
    c.click(CAMPO('empresa-razao-social'), at=c.A(3, 'razão', 0.7), label='Razão Social (clique no campo)')
    c.press('End')
    c.type(CAMPO('empresa-razao-social'), ' Ltda', at=c.A(3, 'completa', 0.05), label='completa: Recicla Vale Metais Ltda', cps=30, noClick=True)
    c.click(CAMPO('empresa-ie'), at=c.A(3, 'digito', 0.6), label='Inscrição Estadual (clique no campo)')
    c.type(CAMPO('empresa-ie'), IE_RECICLA, at=c.A(3, 'inscrição', 0.05), label='digita a inscrição estadual', cps=40, noClick=True)
    c.marcar(CAMPO('empresa-cnpj'), at=c.A(3, 'CNPJ', 0.2), label='zoom: CNPJ * e Inscrição Estadual')
    c.mark(4)
    c.ev(js_rola_texto('Endereço Fiscal', 150, 700, MAIN), at=c.A(4, 'endereço', 0.9), label='desce a Endereço Fiscal')
    c.hover(TXT('Editar em Configurações › Empresa', exact=False), 1.0, at=c.A(4, 'mudar,', 0.6), label='Editar em Configurações › Empresa')
    c.mark(5)
    c.click(TRILHO('Impostos (padrão)'), at=c.A(5, 'impostos.', 0.7), label='Impostos (padrão)')
    c.waitfor(text='Passo 3 de 3:', timeout=10)
    c.click(SEL("main button[role=combobox]", nth=0), at=c.A(5, 'regime', 0.7), label='Regime Tributário (abre a lista)')
    c.click(OPT('Lucro Real'), at=c.A(5, 'Lucro', 0.7), label='Lucro Real', noScroll=True)
    c.mark(6)
    c.marcar(TXT('Lucro Real:'), at=c.A(6, 'Olha:', 0.2), label='zoom: o quadro Lucro Real:')
    c.hover(TXT('PIS: 1,65% | COFINS: 7,60% (Regime Não Cumulativo)', exact=False), 1.0, at=c.A(6, 'PIS', 0.6), label='PIS e COFINS ajustados')
    c.mark(7)
    c.ev(js_rola_texto('Contribuinte de ICMS', 140, 800, MAIN), at=c.A(7, 'embaixo', 0.9), label='desce ao ICMS')
    c.hover(TXT('Alíquota do ICMS interno, sem o FCP (%)', exact=False), 0.6, at=c.A(7, 'alíquota', 0.6), label='zoom: Alíquota do ICMS interno')
    c.hover(TXT('CST Saída', exact=False), 0.6, at=c.A(7, 'códigos', 0.6), label='os CST do ICMS')
    c.mark(8)
    c.ev(js_rola_texto('CFOPs Padrão', 140, 800, MAIN), at=c.A(8, 'CFOP', 0.9, nth=0), label='desce aos CFOPs Padrão')
    c.hover(TXT('CFOP Saída Interna', exact=False), 0.4, at=c.A(8, 'venda,', 0.6), label='CFOP de venda')
    c.hover(TXT('CFOP Entrada Interna', exact=False), 0.6, at=c.A(8, 'compra,', 0.6), label='CFOP de compra')
    c.mark(9)
    c.ev(js_rola_texto('Reforma Tributária (IBS/CBS)', 120, 800, MAIN), at=c.A(9, 'fim,', 0.9), label='desce à Reforma Tributária (IBS/CBS)')
    c.click(SEL("div.border.rounded-lg:has(label:text-is('Calcular IBS e CBS automaticamente')) button[role=switch]"),
            at=c.A(9, 'Ligado', 0.7), label='liga Calcular IBS e CBS automaticamente')
    c.click(SEL("input[placeholder='Ex: 000']", nth=0), at=c.A(9, 'sistema', 0.7), label='CST-IBS/CBS de Saída (clique no campo)')
    c.type(SEL("input[placeholder='Ex: 000']", nth=0), '000', at=c.A(9, 'calcula', 0.05), label='CST-IBS/CBS 000', cps=40, noClick=True)
    c.ev(js_preenche_ph([("Ex: 000001", 0, '000001'), ("Ex: 000", 1, '000'), ("Ex: 000001", 1, '000001')]), at=c.A(9, 'códigos', 0.3),
         label='cClassTrib 000001 e a Entrada (sem cursor, trecho acelerado)')
    c.mark(10)
    c.mark(11)
    c.click(BTN('Salvar configuração'), at=c.A(11, 'Salvar', 0.7), label='Salvar configuração', noScroll=True)
    c.waitfor(text='Empresa cadastrada no sistema de NF-e!', timeout=15)
    c.fim()
    return c


def cap05():
    """Cenários fiscais: o cabeçalho e o vazio (L1), o aviso fixo (L2), Criar o primeiro cenário e o nome (L3), Quando aplicar (L4),
    O que aplicar (L5), Criar cenário e o selo Não revisado (L6), ilustração (L7)."""
    c = Cap(5, setup=setup_cfg('cenarios', 'Nenhum cenário cadastrado'), start=(760, 400))
    c.mark(1)
    c.hover(TXT('Cenários fiscais'), 0.6, at=c.A(1, 'cenários.', 0.6), label='Cenários fiscais')
    c.hover(TXT('Nenhum cenário cadastrado'), 1.0, at=c.A(1, 'exceção', 0.6), label='Nenhum cenário cadastrado')
    c.mark(2)
    c.hover(TXT('O que você preenche aqui vai impresso na nota fiscal.', exact=False), 1.5, at=c.A(2, 'aviso', 0.6),
            label='zoom: aviso fixo O que você preenche aqui vai impresso na nota fiscal')
    c.mark(3)
    c.click(BTN('Criar o primeiro cenário', MAIN), at=c.A(3, 'Criar', 0.7), label='Criar o primeiro cenário')
    colar(c, SEL("[id$='-nome']"), 'Venda para a Fundição Bandeira do Vale',
          c.A(3, 'nome', 0.8), c.A(3, 'situação.', 0.3), 'Nome do cenário: Venda para a Fundição Bandeira do Vale')
    c.mark(4)
    c.hover(SEL("[id$='-operacao']"), 0.6, at=c.A(4, 'venda,', 0.6), label='Operação: Venda (já vem assim)')
    c.click(SEL("[id$='-parceiro_tipo']"), at=c.A(4, 'cliente', 0.7), label='Cliente da nota (abre a lista)')
    c.click(OPT('Um cliente/fornecedor específico'), at=c.A(4, 'só:', 0.6), label='Um cliente/fornecedor específico', noScroll=True)
    c.click(SEL("[id$='-parceiro_valor']"), at=c.A(4, 'Fundição,', 0.6), label='CNPJ da Fundição (clique no campo)')
    c.type(SEL("[id$='-parceiro_valor']"), '94716352000191', at=c.A(4, 'CNPJ.', 0.05), label='zoom: o CNPJ da Fundição', cps=40, noClick=True)
    c.hover(TXT('Qualquer', exact=False), 0.6, at=c.A(4, 'Qualquer.', 0.6), label='o resto em Qualquer')
    c.mark(5)
    c.ev(js_rola_texto('O que aplicar', 120, 800, MAIN), at=c.A(5, 'aplicar', 0.9), label='desce a O que aplicar')
    c.click(SEL("main div:has(> label:text-is('CST do ICMS')) button[role=combobox]"), at=c.A(5, 'muda,', 0.7), label='CST do ICMS (abre a lista)')
    c.click(SEL("[role=option]:has-text('51')"), at=c.A(5, 'jeito', 0.5), label='CST do ICMS 51', noScroll=True)
    c.click(SEL("[id$='-diferimento']"), at=c.A(5, 'contador', 0.7), label='Diferimento (%) (clique no campo)')
    c.type(SEL("[id$='-diferimento']"), '100', at=c.A(5, 'passou.', 0.05), label='Diferimento 100', cps=40, noClick=True)
    c.hover(TXT('Usar a configuração de Impostos', exact=False), 0.8, at=c.A(5, 'branco', 0.6), label='campo em branco: usa o padrão')
    c.mark(6)
    c.click(BTN('Criar cenário', MAIN), at=c.A(6, 'Criar', 0.7), label='Criar cenário')
    c.waitfor(text='Cenário criado', timeout=10)
    c.hover(TXT('Não revisado'), 0.6, at=c.A(6, 'revisado,', 0.6), label='selo Não revisado')
    c.hover(BTN('Marcar como revisado', MAIN), 1.2, at=c.A(6, 'marcar', 0.6), label='zoom: Marcar como revisado (sem clicar)')
    c.mark(7)
    c.fim()
    return c


def cap06():
    """Série e numeração: Série padrão (L1), a mesma série e a série 1 (L2), ilustração (L3), Adicionar série com 1 e 1248 (L4, zoom),
    a ajuda do zero (L5), Adicionar e a linha "Série 1" (L6)."""
    c = Cap(6, setup=setup_cfg('numeracao', 'Série padrão das suas notas'), start=(760, 400))
    c.mark(1)
    c.hover(TXT('Série padrão das suas notas'), 1.0, at=c.A(1, 'série', 0.6), label='Série padrão das suas notas')
    c.mark(2)
    c.hover(TXT('Entrada e saída usam a mesma série'), 0.8, at=c.A(2, 'entrada', 0.6), label='zoom: Entrada e saída usam a mesma série')
    c.hover(TXT('Série padrão'), 0.8, at=c.A(2, 'um.', 0.6), label='zoom: Série padrão 1')
    c.mark(3)
    c.mark(4)
    c.click(BTN('Adicionar série', MAIN), at=c.A(4, 'Adicionar', 0.7), label='Adicionar série')
    c.click(CAMPO('serie-number'), at=c.A(4, 'informo', 0.9), label='Número da série (clique no campo)')
    c.type(CAMPO('serie-number'), '1', at=c.A(4, 'um', 0.05), label='série 1', cps=40, noClick=True)
    c.click(CAMPO('last-number'), at=c.A(4, 'emitida', 0.7), label='Última nota emitida nessa série (clique no campo)')
    c.type(CAMPO('last-number'), '1248', at=c.A(4, 'mil', 0.05), label='zoom: Última nota emitida nessa série 1248', cps=40, noClick=True, clear=True)
    c.mark(5)
    c.hover(DLG_TXT('Se você nunca emitiu nada nessa série, deixe em 0. O sistema vai começar a próxima do nº 1.'), 1.0,
            at=c.A(5, 'zero,', 0.6), label='zoom: ajuda do zero')
    c.mark(6)
    c.click(SEL(f"{DLG} button:text-is('Adicionar')"), at=c.A(6, 'Adicionar.', 0.7), label='Adicionar')
    c.waitfor(text='Série adicionada com sucesso', timeout=10)
    c.hover(TXT('Série 1'), 1.2, at=c.A(6, 'próxima', 0.6), label='a linha Série 1 com Última nota emitida: 1248')
    c.fim()
    return c


TRANSP = [('Razão Social *', 'Cargas Vale do Sol Ltda'), ('CPF/CNPJ', '41826537000192'), ('Inscrição Estadual', '688.115.922.408')]


def js_preenche(pares):
    """preenche campos do formulário pelo rótulo (sem cursor: trecho acelerado da fala), com o setter nativo + evento input do React"""
    return ("(()=>{const set=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set;const out=[];"
            f"for(const [rot,val] of {json.dumps(pares, ensure_ascii=False)}){{const l=[...document.querySelectorAll('main label')].find(x=>x.textContent.trim()===rot);"
            "const i=l&&(l.htmlFor?document.getElementById(l.htmlFor):l.parentElement.querySelector('input'));if(!i){out.push('SEM ALVO '+rot);continue;}"
            "set.call(i,val);i.dispatchEvent(new Event('input',{bubbles:true}));out.push(rot+'='+i.value)}return out.join(' | ')})()")


def js_preenche_ph(itens):
    """preenche campos pelo placeholder (e a ordem entre os iguais), sem cursor: trecho acelerado"""
    return ("(()=>{const set=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set;const out=[];"
            f"for(const [ph,k,val] of {json.dumps(itens, ensure_ascii=False)}){{const i=[...document.querySelectorAll('input')].filter(x=>x.placeholder===ph&&x.offsetParent)[k];"
            "if(!i){out.push('SEM ALVO '+ph);continue;}set.call(i,val);i.dispatchEvent(new Event('input',{bubbles:true}));out.push(ph+'='+i.value)}return out.join(' | ')})()")


def js_select_teclado(rotulo, opcao):
    """Select do Radix sem cursor (docs/08, T5): foco no gatilho do rótulo; o robô aperta Enter e outro eval clica a opção"""
    foco = ("(()=>{const l=[...document.querySelectorAll('main label')].find(x=>x.textContent.trim()===%s);"
            "const b=l&&l.parentElement.querySelector('button[role=combobox]');if(!b)return 'SEM ALVO';b.focus();return 'foco ok'})()") % json.dumps(rotulo)
    escolhe = ("(async()=>{for(let k=0;k<20;k++){const o=[...document.querySelectorAll('[role=option]')].find(x=>x.textContent.trim()===%s);"
               "if(o){o.click();return 'escolhido '+%s}await new Promise(r=>setTimeout(r,50))}return 'SEM ALVO'})()") % (json.dumps(opcao), json.dumps(opcao))
    return foco, escolhe


def cap07():
    """Transportadora e serviços: o formulário vazio (L1), razão social, CNPJ e IE com o cursor e o endereço sem cursor (L2, trecho
    acelerado), a placa (L3), Adicionar (L4) e Serviços (L5)."""
    c = Cap(7, setup=setup_cfg('transportadora', 'Nenhuma transportadora cadastrada'), start=(760, 400))
    c.mark(1)
    c.hover(TXT('Nova transportadora'), 1.0, at=c.A(1, 'transportadora', 0.6), label='Nova transportadora')
    c.mark(2)
    for k, (rot, val) in enumerate(TRANSP):
        campo = SEL(f"main input:near(:text-is('{rot}'))")
        pal = ['Cargas', 'CNPJ,', 'inscrição'][k]
        c.click(campo, at=c.A(2, pal, 0.7), label=f'{rot} (clique no campo)')
        c.ev(js_colar(val), label=f'{rot}: {val}' + (' (zoom: CPF/CNPJ)' if k == 1 else ''))
    foco, escolhe = js_select_teclado('UF', 'SP')
    c.ev(foco, label='UF (foco no seletor, sem cursor)')
    c.press('Enter', label='UF (abre a lista pelo teclado)')
    c.ev(escolhe, label='UF SP (trecho acelerado)')
    c.ev(js_preenche([('Logradouro', 'Rua dos Ferroviários'), ('Número', '380'), ('Bairro', 'Vila São José'), ('Cidade', 'Taubaté')]),
         at=c.A(2, 'endereço.', 0.3), label='endereço (sem cursor, trecho acelerado)')
    c.mark(3)
    c.click(SEL("main input[placeholder='ABC1D23']"), at=c.A(3, 'placa', 0.7), label='Placa (clique no campo)')
    c.type(SEL("main input[placeholder='ABC1D23']"), 'FJR3B27', at=c.A(3, 'caminhão', 0.05), label='Placa FJR3B27', cps=40, noClick=True)
    foco, escolhe = js_select_teclado('UF Veículo', 'SP')
    c.ev(foco, at=c.A(3, 'entrega.', 0.3), label='UF Veículo (foco no seletor, sem cursor)')
    c.press('Enter', label='UF Veículo (abre a lista pelo teclado)')
    c.ev(escolhe, label='UF Veículo SP')
    c.mark(4)
    c.click(SEL("main button:text-is('Adicionar')"), at=c.A(4, 'Adicionar,', 0.7), label='Adicionar')
    c.waitfor(text='Transportadora cadastrada!', timeout=10)
    c.hover(TXT('Cargas Vale do Sol Ltda', exact=False), 0.8, at=c.A(4, 'lista.', 0.6), label='a linha Cargas Vale do Sol Ltda')
    c.mark(5)
    c.click(TRILHO('Serviços'), at=c.A(5, 'Serviços', 0.7), label='Serviços')
    c.hover(TXT('Nenhum serviço cadastrado'), 1.5, at=c.A(5, 'próximo', 0.6), label='Nenhum serviço cadastrado')
    c.fim()
    return c


def cap08():
    """A cota: o selo verde (L1, zoom), a dica do mouse (L2); L3 a L6 são ilustração (a tela fica parada)."""
    c = Cap(8, setup=setup_nfe('saida', VAZIO), start=(760, 400))
    c.mark(1)
    c.marcar(COTA, at=c.A(1, 'selo', 0.3), label='zoom: selo 0/1.000 Documentos')
    c.hover(COTA, 1.0, at=c.A(1, 'usados:', 0.6), label='o selo da cota', noScroll=True)
    c.mark(2)
    c.hover(COTA, 4.0, at=c.A(2, 'Passando', 0.4), label='a dica do selo: Nível 1, até 1.000 documentos, você emitiu 0', noScroll=True)
    c.mark(3)
    c.rolar(0, at=c.A(3, 'Toda', 0.3), ponto=(760, 470), label='o cursor sai do selo (ilustração)')
    for i in (4, 5, 6):
        c.mark(i)
    c.fim()
    return c


# ---------------------------------------------------------------- a janela da nota (NovaNotaModal)
ABA_NOTA = lambda t: SEL(f"{DLG} button:text-is('{t}')")                 # Dados, Itens, Transporte...
SEL_PERTO = lambda rot: SEL(f"{DLG} div:has(> label:text-is('{rot}')) button[role=combobox]")
CLIENTE_BTN = SEL(f"{DLG} button:has-text('Selecione o cliente')")            # abre a janela "Selecionar Cliente" (EntitySearchModal)
BUSCA_PARC = SEL("[role=dialog]:has-text('Selecionar Cliente') input")
ESCOLHE_PARC = lambda n: SEL(f"[role=dialog]:has-text('Selecionar Cliente') button:has-text('{n}')")
MATERIAL = SEL(f"{DLG} input[placeholder='Selecionar material...']")
QTD = SEL(f"{DLG} tr.bg-primary\\/5 input", nth=2)                        # linha de inserção: NCM, CFOP, Qtd, Vl. Unit., Desconto
RESUMO = SEL(f"{DLG} :text-is('Total da nota')")


def js_valor_campo(material):
    """lê a linha do item (os valores ficam em inputs, fora do innerText): 'OK: ...' ou 'DIFERENTE: ...'"""
    return ("(()=>{const rs=[...document.querySelectorAll('[role=dialog] tr')].filter(r=>[...r.querySelectorAll('input')].some(i=>i.value.includes(%s)));"
            "if(!rs.length)return 'DIFERENTE: sem a linha';const v=[...rs[rs.length-1].querySelectorAll('input')].map(i=>i.value).join(' | ');"
            "const t=document.querySelector('[role=dialog]').innerText;return (v.includes('500,00')&&t.includes('23.950,00')?'OK: ':'DIFERENTE: ')+v})()") % json.dumps(material)


def emite_e_espera(c, num, at, label, linha_aut=None, at_aut=None):
    """Emitir Nota (rodapé fixo, sem rolar): a janela fecha, a linha #num aparece "Aguardando SEFAZ" e, no polling de 5 s, "Autorizada"."""
    c.click(ROD('Emitir Nota'), at=at, label=label, noScroll=True)
    c.waitfor(selector=f"main tbody tr:has-text('#{num}')", timeout=20)
    c.hover(SEL(f"main tbody tr:has-text('#{num}') td:has-text('SEFAZ')"), 0.6, label=f'#{num} Aguardando SEFAZ')
    c.waitfor(selector=f"main tbody tr:has-text('#{num}'):has-text('Autorizada')", timeout=25)
    if linha_aut is not None:
        c.hover(SEL(f"main tbody tr:has-text('#{num}') td:has-text('Autorizada')"), 1.0, at=at_aut, label=f'#{num} Autorizada')


def cap09():
    """Nota avulsa: Nova Nota (L1), NF-e de Saída e os passos Dados/Itens (L2), o cliente Serra Fina (L3), a natureza e o CFOP 6102 (L4),
    a numeração 1249 (L5, zoom), Avançar (L6), o alumínio perfil 320 kg (L7, zoom), Incluir e o total (L8, zoom), o rodapé (L9),
    ilustração (L10), Emitir Nota e "Aguardando SEFAZ" (L11), "Autorizada" (L12) e Visualizar com chave e protocolo (L13, zoom)."""
    c = Cap(9, setup=setup_nfe('saida', VAZIO), start=(760, 400))
    c.mark(1)
    c.click(NOVA_NOTA, at=c.A(1, 'Clico', 0.6), label='Nova Nota')
    c.mark(2)
    c.click(DLG_TXT('NF-e de Saída'), at=c.A(2, 'NF-e', 0.9), label='NF-e de Saída')
    c.waitfor(text='Para quem', timeout=15)
    c.hover(ABA_NOTA('Dados'), 0.4, at=c.A(2, 'Dados', 0.6), label='passo Dados')
    c.hover(ABA_NOTA('Itens'), 0.6, at=c.A(2, 'Itens.', 0.6), label='passo Itens')
    c.mark(3)
    c.click(CLIENTE_BTN, at=round(c.L(3) - 0.2, 2), label='Cliente: Selecione o cliente (abre a busca)')
    c.type(BUSCA_PARC, 'Serra Fina', at=c.A(3, 'cliente:', 0.05), label='busca Serra Fina', cps=40, noClick=True)
    c.click(ESCOLHE_PARC('Serra Fina Alumínio Reciclagem'), at=c.A(3, 'Serra', 0.6), label='escolhe Serra Fina Alumínio Reciclagem')
    c.waitfor(gone={'selector': "[role=dialog]:has-text('Selecionar Cliente')"}, timeout=8)
    c.mark(4)
    c.hover(SEL_PERTO('Natureza da Operação'), 0.6, at=c.A(4, 'natureza', 0.6), label='Natureza da Operação: Venda de mercadorias (já vem assim)')
    c.hover(SEL(f"{DLG} label:text-is('CFOP')"), 1.0, at=c.A(4, 'CFOP', 0.6), label='zoom: CFOP 6102 (Serra Fina em Itamonte, MG)')
    c.confere('dlg', ['6102'], 'CFOP 6102 da Serra Fina (MG)')
    c.mark(5)
    c.marcar(SEL(f"{DLG} label:text-is('Número previsto')"), at=c.A(5, 'numeração:', 0.3), label='zoom: Número previsto 1249 e "Série 1 / Nº 1249"')
    c.hover(SEL(f"{DLG} :text-matches('Esta nota será emitida como')"), 1.0, at=c.A(5, 'mil', 0.6), label='Esta nota será emitida como Série 1 / Nº 1249')
    c.confere('dlg', ['Série 1 / Nº 1249'], 'Série 1 / Nº 1249')
    c.hover(SEL(f"{DLG} label:text-is('Data e hora da emissão')"), 0.8, at=c.A(5, 'data', 0.6), label='Data e hora da emissão em branco')
    c.mark(6)
    c.click(ROD('Avançar'), at=c.A(6, 'Avançar,', 0.7), label='Avançar', noScroll=True)
    c.mark(7)
    c.click(MATERIAL, at=c.A(7, 'Escolho', 0.7), label='Selecionar material...')
    c.type(MATERIAL, 'perfil', label='busca perfil', cps=40, noClick=True)
    c.click(SEL("[cmdk-item]:has-text('Alumínio perfil'), [role=option]:has-text('Alumínio perfil')"), at=c.A(7, 'perfil.', 0.4), label='Alumínio perfil', noScroll=True)
    c.hover(SEL(f"{DLG} th:text-is('NCM')"), 0.4, at=c.A(7, 'NCM,', 0.6), label='NCM 7602.00.00 do cadastro')
    c.hover(SEL(f"{DLG} th:text-is('Vl. Unit.')"), 0.4, at=c.A(7, 'preço', 0.6), label='preço de venda 10,40 do cadastro')
    c.click(QTD, at=c.A(7, 'Trezentos', 0.7), label='Qtd (clique no campo)')
    c.type(QTD, '320', at=c.A(7, 'quilos,', 0.05), label='zoom: Qtd 320 e Vl. Unit. 10,40', cps=30, noClick=True, clear=True)
    c.mark(8)
    c.click(SEL(f"{DLG} button:has-text('Incluir')"), at=c.A(8, 'Incluir.', 0.7), label='Incluir')
    c.marcar(RESUMO, at=c.A(8, 'nota', 0.3), label='zoom: Total da nota R$ 3.328,00 e Pronta pra emitir')
    c.hover(SEL(f"{DLG} :text-is('Pronta pra emitir')"), 1.0, at=c.A(8, 'Pronta', 0.6), label='selo Pronta pra emitir')
    c.confere('dlg', ['3.328,00', 'Pronta pra emitir'], 'total R$ 3.328,00 e Pronta pra emitir')
    c.mark(9)
    c.hover(ROD('Emitir Nota'), 1.0, at=c.A(9, 'dica:', 0.4), label='o rodapé: Voltar, Salvar Rascunho, Emitir Nota', noScroll=True)
    c.mark(10)
    c.mark(11)
    emite_e_espera(c, 1249, c.A(11, 'Emitir', 0.7), 'Emitir Nota')
    c.mark(12)
    c.hover(SEL("main tbody tr:has-text('#1249') td:has-text('Autorizada')"), 0.6, at=c.A(12, 'autorizada', 0.6, nth=1), label='#1249 Autorizada')
    c.mark(13)
    menu_item(c, '#1249', 'Visualizar', c.A(13, 'Visualizar', 0.6), 'Visualizar', at_menu=round(c.L(13) - 1.8, 2))
    c.waitfor(text='NF-e #1249', timeout=10)
    c.marcar(SEL(f"{DLG} :text-is('Chave de Acesso')"), at=c.A(13, 'chave', 0.3), label='zoom: Chave de Acesso e Protocolo')
    c.hover(SEL(f"{DLG} :text-is('Protocolo')"), 1.0, at=c.A(13, 'protocolo', 0.6), label='Protocolo da SEFAZ')
    c.fim()
    return c


def cap10():
    """Nota a partir de um pedido: Nova Nota > NF-e de Saída (L1), Pedido e a venda de 09/11 da Fundição (L2), Importar (L3), Avançar e
    a quantidade 500 (L4, zoom), ilustração (L5, L6), Transporte: frete e transportadora (L7), Emitir Nota e 1250 autorizada (L8)."""
    c = Cap(10, setup=setup_nfe('saida', '#1249'), start=(760, 400))
    c.mark(1)
    c.click(NOVA_NOTA, at=c.A(1, 'nasce', 0.6), label='Nova Nota')
    c.click(DLG_TXT('NF-e de Saída'), at=c.A(1, 'venda', 0.6, nth=0), label='NF-e de Saída')
    c.waitfor(text='Para quem', timeout=15)
    c.hover(SEL(f"{DLG} button:text-is('Pedido')"), 1.0, at=c.A(1, 'puxa', 0.6), label='Importar de: Pedido')
    c.mark(2)
    c.click(SEL(f"{DLG} button:text-is('Pedido')"), at=c.A(2, 'Pedido,', 0.7), label='Pedido')
    c.waitfor(text='Importar de Pedido de Venda', timeout=10)
    c.hover(SEL(f"{DLG}:has-text('Importar de Pedido de Venda') :text('Fundição Bandeira do Vale')", nth=0), 1.0, at=c.A(2, 'Esta', 0.6),
            label='o pedido de 09/11 da Fundição Bandeira do Vale (R$ 23.950,00)')
    c.mark(3)
    c.click(SEL(f"{DLG}:has-text('Importar de Pedido de Venda') button:text-is('Importar')", nth=0), at=c.A(3, 'Importar.', 0.7), label='Importar')
    c.waitfor(text='Pedido importado', timeout=10)
    c.hover(SEL(f"{DLG} button:has-text('Fundição Bandeira do Vale')", nth=0), 0.8, at=c.A(3, 'cliente', 0.6), label='o cliente veio do pedido')
    c.mark(4)
    c.click(ROD('Avançar'), at=round(c.L(4) - 0.2, 2), label='Avançar', noScroll=True)
    c.marcar(SEL(f"{DLG} th:text-is('Qtd')", nth=-1), at=c.A(4, 'quantidade:', 0.2), label='zoom: Qtd 500 (Cobre mel)')
    c.ev(js_valor_campo('Cobre mel'), label='confere Qtd do Cobre mel (500,00) e o total R$ 23.950,00')
    c.mark(5)
    c.mark(6)
    c.mark(7)
    c.click(ABA_NOTA('Transporte'), at=c.A(7, 'Transporte,', 0.7), label='aba Transporte')
    c.click(SEL_PERTO('Modalidade do Frete'), at=c.A(7, 'modalidade', 0.7), label='Modalidade do Frete (abre a lista)')
    c.click(SEL("[role=option]:has-text('Frete por conta do Remetente (CIF)')"), at=c.A(7, 'frete', 0.5), label='0 - Frete por conta do Remetente (CIF)', noScroll=True)
    c.click(SEL(f"{DLG} button[role=combobox]:has-text('Selecionar...')"), at=c.A(7, 'Cargas', 0.7), label='Transportadora (abre a lista)')
    c.click(SEL("[role=option]:has-text('Cargas Vale do Sol')"), at=c.A(7, 'Sol,', 0.5), label='Cargas Vale do Sol Ltda (FJR3B27)', noScroll=True)
    c.hover(SEL(f"{DLG} :text-is('Dados da Transportadora')"), 0.8, at=c.A(7, 'placa.', 0.6), label='Dados da Transportadora preenchidos')
    c.mark(8)
    emite_e_espera(c, 1250, c.A(8, 'Emitir', 0.7), 'Emitir Nota')
    c.fim()
    return c


def cap11():
    """Nota de um caixa fechado: sub-aba Entrada, Nova Nota > NF-e de Entrada (L1), Emissão em Massa (Caixa) (L2), 9 de novembro e o
    caixa do Marcos (L3), Selecionar todos sem NF-e (L4), Uma nota consolidada e a faixa (L5, zoom), ilustração (L6), Montar nota
    consolidada e a natureza (L7), Avançar, Emitir Nota e 1251 autorizada (L8)."""
    c = Cap(11, setup=setup_nfe('entrada', VAZIO), start=(760, 400))
    c.mark(1)
    c.click(NOVA_NOTA, at=c.A(1, 'Dona', 0.6), label='Nova Nota')
    c.click(DLG_TXT('NF-e de Entrada'), at=c.A(1, 'nota', 0.6, nth=1), label='NF-e de Entrada')
    c.waitfor(text='Para quem', timeout=15)
    c.mark(2)
    c.click(SEL(f"{DLG} button:has-text('Emissão em Massa (Caixa)')"), at=c.A(2, 'Emissão', 0.7), label='Emissão em Massa (Caixa)')
    c.waitfor(text='Emitir NF-e em massa', timeout=10)
    c.mark(3)
    c.click(SEL(f"{DLG}:has-text('Emitir NF-e em massa') button:has-text('Hoje')"), at=c.A(3, 'Escolho', 0.7), label='data (abre o calendário)')
    c.click(SEL("[data-radix-popper-content-wrapper] button[name='day']:not(.day-outside):text-is('9')"), at=c.A(3, 'nove', 0.6),
            label='9 de novembro', noScroll=True)
    c.click(SEL(f"{DLG} :text-is('Marcos Antunes')"), at=c.A(3, 'Marcos,', 0.6), label='o caixa do Marcos (Fechado, 09/11 07:02)')
    c.mark(4)
    c.click(SEL(f"{DLG} button:has-text('Selecionar todos sem NF-e')"), at=c.A(4, 'Seleciono', 0.7), label='Selecionar todos sem NF-e (3/3)')
    c.confere('dlg', ['3/3 selecionados'], '3/3 selecionados')
    c.mark(5)
    c.click(SEL(f"{DLG} :text-is('Uma nota consolidada')"), at=c.A(5, 'Uma', 0.7, nth=0), label='Uma nota consolidada')
    c.marcar(SEL(f"{DLG} :text-is('Faixa prevista para este lote')"), at=c.A(5, 'faixa:', 0.3), label='zoom: Faixa prevista NF-e nº 1251 e Valor dos pedidos R$ 803,30')
    c.confere('dlg', ['1251', '803,30'], 'faixa 1251 e R$ 803,30')
    c.mark(6)
    c.mark(7)
    c.click(SEL(f"{DLG} button:has-text('Montar nota consolidada')"), at=c.A(7, 'Montar', 0.7), label='Montar nota consolidada', noScroll=True)
    c.waitfor(text='pedido(s) importado(s) com sucesso', timeout=10)
    c.hover(SEL(f"{DLG} :text-is('Consumidor Final / Não Identificado')"), 0.6, at=c.A(7, 'consumidor', 0.6), label='Consumidor Final / Não Identificado')
    c.click(SEL_PERTO('Natureza da Operação'), at=c.A(7, 'natureza', 0.7), label='Natureza da Operação (abre a lista)')
    c.click(OPT('Entrada de sucata para revenda (pessoa física)'), at=c.A(7, 'sucata', 0.5), label='Entrada de sucata para revenda (pessoa física)', noScroll=True)
    c.mark(8)
    c.click(ROD('Avançar'), at=c.A(8, 'Confiro', 0.6), label='Avançar (os três itens)', noScroll=True)
    emite_e_espera(c, 1251, c.A(8, 'Emitir', 0.7), 'Emitir Nota')
    c.fim()
    return c


MOTIVO = 'Pedido alterado pelo cliente antes de a mercadoria sair do pátio'
CCE = "Onde se lê 'Placa FJR3B27', leia-se 'Placa GKM5D18'. A transportadora trocou o veículo da carga."


def cap12():
    """Cancelar e corrigir: as duas autorizadas (L1), menu da 1249 > Cancelar e o motivo (L2), Confirmar Cancelamento (L3), ilustração
    (L4), menu da 1250 > Carta de Correção e o aviso (L5), o texto (L6), Enviar CC-e (L7)."""
    c = Cap(12, setup=setup_nfe('saida', '#1251' if False else '#1250'), start=(760, 400))
    c.mark(1)
    c.hover(LINHA('#1249'), 1.0, at=c.A(1, 'mil', 0.6), label='a nota 1249 (Serra Fina, Autorizada)')
    c.mark(2)
    menu_item(c, '#1249', 'Cancelar', c.A(2, 'Cancelar.', 0.6), 'Cancelar', at_menu=c.A(2, 'menu', 0.6))
    c.waitfor(text='Cancelar Nota Fiscal #1249', timeout=10)
    colar(c, SEL(f"{DLG} textarea"), MOTIVO, c.A(2, 'motivo', 0.7), c.A(2, 'obrigatório,', 0.2), 'Motivo do Cancelamento')
    c.mark(3)
    c.click(SEL(f"{DLG} button:has-text('Confirmar Cancelamento')"), at=c.A(3, 'Confirmar', 0.7), label='Confirmar Cancelamento')
    c.waitfor(selector="main tbody tr:has-text('#1249'):has-text('Cancelada')", timeout=15)
    c.hover(SEL("main tbody tr:has-text('#1249') td:has-text('Cancelada')"), 1.0, at=c.A(3, 'cancelada.', 0.5), label='#1249 Cancelada')
    c.mark(4)
    c.mark(5)
    menu_item(c, '#1250', 'Carta de Correção', c.A(5, 'Ela', 0.5), 'Carta de Correção', at_menu=round(c.L(5) - 2.4, 2))
    c.waitfor(text='Carta de Correção - NF-e #1250', timeout=10)
    c.hover(SEL(f"{DLG} :text-matches('permite corrigir erros em campos')"), 2.0, at=c.A(5, 'tela', 0.6), label='zoom: aviso Importante (o que não dá pra corrigir)')
    c.mark(6)
    colar(c, SEL(f"{DLG} textarea"), CCE, c.A(6, 'texto,', 0.7), c.A(6, 'formato', 0.2), 'Texto da Correção')
    c.hover(SEL(f"{DLG} :text-matches('Dica: Use o formato')"), 1.0, at=c.A(6, 'leia-se', 0.6), label='zoom: Dica do formato')
    c.mark(7)
    c.click(SEL(f"{DLG} button:has-text('Enviar CC-e')"), at=c.A(7, 'Enviar', 0.7), label='Enviar CC-e')
    c.waitfor(text='Carta de Correção enviada com sucesso!', timeout=10)
    c.fim()
    return c


JUSTIF = 'Numeração pulada na emissão de outubro e não utilizada'


def cap13():
    """Inutilizar: a lista (L1), ilustração (L2), três pontinhos > Inutilizar numeração e o aviso (L3, zoom), Por Faixa 1246 a 1247 e o
    resumo (L4, zoom), a aba Inutilizar Rejeitadas (L5), a justificativa e Inutilizar na SEFAZ (L6), a sub-aba Inutilizadas (L7)."""
    c = Cap(13, setup=setup_nfe('saida', '#1250'), start=(760, 400))
    c.mark(1)
    c.mark(2)
    c.mark(3)
    c.click(MAIS, at=c.A(3, 'três', 0.7), label='três pontinhos (Mais opções de NF-e)')
    c.click(ITEM('Inutilizar numeração'), at=c.A(3, 'Inutilizar', 0.6), label='Inutilizar numeração', noScroll=True)
    c.waitfor(text='Inutilizar Numeração de NF-e', timeout=10)
    c.hover(SEL(f"{DLG} :text-is('Operação irreversível!')"), 0.8, at=c.A(3, 'aviso:', 0.6), label='zoom: Operação irreversível!')
    c.hover(SEL(f"{DLG} :text-matches('NUNCA foram autorizados')"), 0.8, at=c.A(3, 'nunca', 0.6), label='Só funciona em números que NUNCA foram autorizados')
    c.hover(SEL(f"{DLG} :text-matches('use Cancelamento')"), 0.8, at=c.A(3, 'cancelamento.', 0.6), label='Para anular nota emitida, use Cancelamento')
    c.mark(4)
    c.click(CAMPO('numero-inicial'), at=c.A(4, 'mil', 0.7, nth=0), label='Número Inicial (clique no campo)')
    c.type(CAMPO('numero-inicial'), '1246', at=c.A(4, 'quarenta', 0.05, nth=0), label='Número Inicial 1246', cps=40, noClick=True, clear=True)
    c.click(CAMPO('numero-final'), at=c.A(4, 'ao', 0.6), label='Número Final (clique no campo)')
    c.type(CAMPO('numero-final'), '1247', at=c.A(4, 'quarenta', 0.05, nth=1), label='Número Final 1247', cps=40, noClick=True, clear=True)
    c.hover(SEL(f"{DLG} :text-matches('Inutilizará as Notas')"), 1.5, at=c.A(4, 'Dá', 0.6), label='zoom: Inutilizará as Notas #1246 até #1247 da Série 1, ano 2026')
    c.confere('dlg', ['#1246 até #1247', 'Série 1', '2026'], 'faixa 1246 a 1247 da série 1, 2026')
    c.mark(5)
    c.hover(SEL(f"{DLG} [role=tab]:has-text('Inutilizar Rejeitadas'), {DLG} button:has-text('Inutilizar Rejeitadas')"), 1.2,
            at=c.A(5, 'Inutilizar', 0.6), label='zoom: aba Inutilizar Rejeitadas (sem clicar)')
    c.mark(6)
    colar(c, SEL(f"{DLG} textarea"), JUSTIF, c.A(6, 'Escrevo', 0.7), c.A(6, 'justificativa', 0.2), 'Justificativa')
    c.click(SEL(f"{DLG} button:has-text('Inutilizar na SEFAZ')"), at=c.A(6, 'clico', 0.6), label='Inutilizar na SEFAZ')
    c.waitfor(text='Numeração inutilizada com sucesso', timeout=10)
    c.mark(7)
    c.click(SUBABA('Inutilizadas'), at=c.A(7, 'números', 0.7), label='sub-aba Inutilizadas')
    c.waitfor(text='Numerações Inutilizadas', timeout=10)
    c.hover(LINHA('#1246'), 0.6, at=c.A(7, 'aqui,', 0.6), label='#1246 e #1247 Inutilizada')
    c.fim()
    return c


def cap14():
    """DANFE e XML: (L1), ilustração (L2), o menu da 1250 (L3, zoom), Download DANFE (L4: o PDF abre em outra aba, fora da gravação),
    Download XML (L5), Visualizar > aba XML (L6), o menu da 1249 cancelada (L7), Exportação Contábil nos três pontinhos (L8)."""
    c = Cap(14, setup=setup_nfe('saida', '#1250'), start=(760, 400))
    c.mark(1)
    c.mark(2)
    c.mark(3)
    c.hover(TRIG('#1250'), 1.6, at=c.A(3, 'menu', 0.6), label='zoom: o menu da 1250 (Download XML, Download DANFE, Comprovante, Carta de Correção)', noScroll=True)
    c.mark(4)
    menu_item(c, '#1250', 'Download DANFE', c.A(4, 'DANFE', 0.6), 'Download DANFE (o PDF abre em outra aba)')
    c.mark(5)
    menu_item(c, '#1250', 'Download XML', c.A(5, 'XML', 0.6), 'Download XML', at_menu=c.A(5, 'Download', 0.9))
    c.mark(6)
    menu_item(c, '#1250', 'Visualizar', c.A(6, 'Visualizar,', 0.6), 'Visualizar', at_menu=round(c.L(6) - 2.0, 2))
    c.waitfor(text='NF-e #1250', timeout=10)
    c.click(SEL(f"{DLG} [role=tab]:has-text('XML')"), at=c.A(6, 'XML', 0.6), label='aba XML')
    c.hover(SEL(f"{DLG} :text-is('XML da nota')"), 1.2, at=c.A(6, 'arquivo', 0.6), label='zoom: XML da nota (Mesmo arquivo enviado à SEFAZ) e Copiar XML')
    c.mark(7)
    c.press('Escape', at=c.A(7, 'menu', 0.3), label='fecha o Visualizar')
    c.pause(0.6)
    c.hover(TRIG('#1249'), 0.3, at=c.A(7, 'cancelada,', 0.6), label='abre o menu da 1249 (Cancelada)', noScroll=True)
    c.hover(ITEM('XML de Cancelamento'), 1.0, at=c.A(7, 'XML', 0.5), label='zoom: XML de Cancelamento (sem clicar)', noScroll=True)
    c.mark(8)
    c.press('Escape', at=c.A(8, 'mandar', 0.6), label='fecha o menu')
    c.click(MAIS, at=c.A(8, 'contador,', 0.7), label='três pontinhos (Mais opções de NF-e)')
    c.hover(ITEM('Exportação Contábil'), 1.2, at=c.A(8, 'Exportação', 0.6), label='zoom: Exportação Contábil (sem clicar)', noScroll=True)
    c.press('Escape', at=c.A(8, 'tutorial.', 0.3), label='fecha o menu')
    c.fim()
    return c


def cap15():
    """As notas recebidas: sub-aba Notas Recebidas e o bloco "Ative" (L1), ilustração (L2), Ativar Notas Recebidas e o aviso da cota (L3,
    zoom), Ativar mesmo assim e as duas notas (L4), as colunas (L5, zoom), Sincronizar agora (L6, zoom)."""
    c = Cap(15, setup=setup_nfe('saida', '#1250'), start=(760, 400))
    c.mark(1)
    c.click(SUBABA('Notas Recebidas'), at=c.A(1, 'recebe.', 0.7), label='sub-aba Notas Recebidas')
    c.waitfor(text='Ative as Notas Recebidas', timeout=10)
    c.mark(2)
    c.mark(3)
    c.click(BTN('Ativar Notas Recebidas', MAIN), at=c.A(3, 'Ativar', 0.7), label='Ativar Notas Recebidas')
    c.waitfor(text='Ativar consulta de notas recebidas?', timeout=10)
    c.hover(SEL("[role=alertdialog] :text-matches('Ao ativar, cada nota fiscal recebida'), [role=dialog] :text-matches('Ao ativar, cada nota fiscal recebida')"),
            2.0, at=c.A(3, 'avisa:', 0.6), label='zoom: Ao ativar, cada nota fiscal recebida passa a contar na sua cota')
    c.mark(4)
    c.click(SEL("[role=alertdialog] button:has-text('Ativar mesmo assim'), [role=dialog] button:has-text('Ativar mesmo assim')"),
            at=c.A(4, 'Ativar', 0.7), label='Ativar mesmo assim')
    c.waitfor(text='Notas emitidas contra o seu CNPJ', timeout=10)
    c.waitfor(text='Auto Peças Vale Forte', timeout=10)
    c.hover(LINHA('Auto Peças Vale Forte'), 0.8, at=c.A(4, 'Auto', 0.6), label='Auto Peças Vale Forte R$ 1.984,00')
    c.hover(LINHA('Depósito Irmãos Siqueira'), 0.8, at=c.A(4, 'Depósito', 0.6), label='Depósito Irmãos Siqueira R$ 2.100,00')
    c.mark(5)
    for col, pal in (('Emitente', 'emitiu,'), ('Valor', 'valor,'), ('Emissão', 'data,'), ('SEFAZ', 'SEFAZ'), ('Manifestação', 'manifestação.')):
        c.hover(SEL(f"main thead th:has-text('{col}')"), 0.3, at=c.A(5, pal, 0.6), label=f'zoom: coluna {col}')
    c.mark(6)
    c.hover(BTN('Sincronizar agora', MAIN), 1.5, at=c.A(6, 'Sincronizar', 0.6), label='zoom: Sincronizar agora (sem clicar)')
    c.fim()
    return c


def cap16():
    """Manifestar: a coluna Manifestação com Ciência (L1, zoom), ilustração (L2), Buscar documento na nota do Depósito (L3), o grupo
    Manifestar da Auto Peças (L4, L5) e Confirmar operação (L6)."""
    c = Cap(16, setup=setup_nfe('recebidas', 'Notas emitidas contra o seu CNPJ'), start=(760, 400))
    c.mark(1)
    c.marcar(SEL("main thead th:has-text('Manifestação')"), at=c.A(1, 'coluna', 0.3), label='zoom: coluna Manifestação com Ciência nas duas')
    c.hover(SEL("main tbody tr:has-text('Auto Peças Vale Forte') :text-is('Ciência')"), 1.0, at=c.A(1, 'Ciência.', 0.6), label='Ciência')
    c.mark(2)
    c.mark(3)
    c.click(TRIG_REC('Depósito Irmãos Siqueira'), at=c.A(3, 'Depósito', 0.7), label='abre o menu da nota do Depósito')
    c.marcar(ITEM('Ver XML'), at=c.A(3, 'XML', 0.3), label='zoom: Ver XML apagado (XML ainda não disponível)')
    c.hover(ITEM('Buscar documento'), 0.6, at=c.A(3, 'Buscar', 0.6), label='Buscar documento (baixa o XML e o DANFE)', noScroll=True)
    c.click(ITEM('Buscar documento'), at=c.A(3, 'nada.', 0.5), label='Buscar documento', noScroll=True)
    c.mark(4)
    c.click(TRIG_REC('Auto Peças Vale Forte'), at=c.A(4, 'respostas', 0.7), label='abre o menu da Auto Peças')
    c.hover(ITEM('Confirmar operação'), 0.6, at=c.A(4, 'Confirmar', 0.6), label='zoom: Confirmar operação', noScroll=True)
    c.hover(ITEM('Desconhecer operação'), 0.6, at=c.A(4, 'Desconhecer', 0.6), label='Desconhecer operação', noScroll=True)
    c.hover(ITEM('Operação não realizada'), 0.6, at=c.A(4, 'Operação', 0.6, nth=1), label='Operação não realizada', noScroll=True)
    c.mark(5)
    c.hover(ITEM('Desconhecer operação'), 0.6, at=c.A(5, 'últimas', 0.6), label='as duas últimas pedem justificativa', noScroll=True)
    c.hover(ITEM('Operação não realizada'), 0.8, at=c.A(5, 'desfeitas.', 0.6), label='e não podem ser desfeitas', noScroll=True)
    c.mark(6)
    c.click(ITEM('Confirmar operação'), at=c.A(6, 'confirmo', 0.6), label='Confirmar operação', noScroll=True)
    c.waitfor(text='Operação confirmada junto à SEFAZ', timeout=10)
    c.hover(SEL("main tbody tr:has-text('Auto Peças Vale Forte') :text-is('Confirmada')"), 1.0, at=c.A(6, 'confirmada.', 0.6), label='Confirmada')
    c.fim()
    return c


def cap17():
    """Importar pelo XML: Importar nota (L1, L2), a aba Arquivo XML e o arquivo da cooperativa (L2), Importar nota > Processando > Nota
    importada > Concluir (L3), Lançar compra… (L4), o casamento "alta" (L5) e "confira" (L6), a frase do peso líquido e Conferir na tela
    de compra (L7, sem clicar)."""
    c = Cap(17, setup=setup_nfe('recebidas', 'Notas emitidas contra o seu CNPJ'), start=(760, 400))
    c.mark(1)
    c.hover(BTN('Importar nota recebida', MAIN), 1.0, at=c.A(1, 'arquivo.', 0.6), label='Importar nota')
    c.mark(2)
    c.click(BTN('Importar nota recebida', MAIN), at=c.A(2, 'Importar', 0.7), label='Importar nota')
    c.waitfor(text='Importar nota recebida', timeout=10)
    c.click(SEL(f"{DLG} [role=tab]:has-text('Arquivo XML'), {DLG} button:has-text('Arquivo XML')"), at=c.A(2, 'Arquivo', 0.6), label='aba Arquivo XML')
    c.upload(SEL(f"{DLG} button:has-text('Selecione o XML'), {DLG} label:has-text('Selecione o XML')"), XML_COOP, at=c.A(2, 'escolho', 0.7),
             label='o XML da Cooperativa (NFe-3871-Cooperativa-Recomeco.xml)')
    c.mark(3)
    c.click(SEL(f"{DLG} button:text-is('Importar nota')"), at=c.A(3, 'Importar', 0.7), label='Importar nota (janela)')
    c.waitfor(text='Nota importada', timeout=15)
    c.click(SEL(f"{DLG} button:text-is('Concluir')"), at=c.A(3, 'entra', 0.6), label='Concluir')
    c.waitfor(text='Cooperativa Recomeço', timeout=10)
    c.hover(LINHA('Cooperativa Recomeço'), 0.8, at=c.A(3, 'outras.', 0.6), label='a linha Cooperativa Recomeço R$ 7.550,00')
    c.mark(4)
    c.click(TRIG_REC('Cooperativa Recomeço'), at=c.A(4, 'Agora,', 0.6), label='abre o menu da nota da Cooperativa')
    c.click(ITEM('Lançar compra…'), at=c.A(4, 'Lançar', 0.6), label='Lançar compra…', noScroll=True)
    c.waitfor(text='Importar NF-e nº 3871', timeout=10)
    c.hover(SEL(f"{DLG} :text-matches('^Fornecedor:')"), 1.0, at=c.A(4, 'fornecedor', 0.6), label='Fornecedor: Cooperativa Recomeço por CNPJ/CPF')
    c.mark(5)
    c.marcar(SEL(f"{DLG} :text-is('ALUMINIO LATINHA')"), at=c.A(5, 'casa', 0.3), label='zoom: ALUMINIO LATINHA, selo alta, Alumínio latinha')
    c.hover(SEL(f"{DLG} :text-is('alta')", nth=0), 1.0, at=c.A(5, 'alta.', 0.6), label='selo alta')
    c.mark(6)
    c.marcar(SEL(f"{DLG} :text-is('PLASTICO PET PRENSADO')"), at=c.A(6, 'PET', 0.3, nth=0), label='zoom: PLASTICO PET PRENSADO, selo confira, Plástico PET')
    c.hover(SEL(f"{DLG} :text-is('confira')", nth=0), 1.0, at=c.A(6, 'conferir.', 0.6), label='selo confira')
    c.mark(7)
    c.hover(SEL(f"{DLG} :text-matches('A NF-e traz só o peso líquido')"), 1.0, at=c.A(7, 'líquido.', 0.6), label='zoom: A NF-e traz só o peso líquido')
    c.hover(SEL(f"{DLG} button:has-text('Conferir na tela de compra')"), 1.5, at=c.A(7, 'Conferir', 0.6), label='Conferir na tela de compra (sem clicar)', noScroll=True)
    c.fim()
    return c


def cap18():
    """Recapitulando: um passeio pelo estado final (certificado e Lucro Real, cenário, série, transportadora, a cota, as três notas, a
    cancelada, as inutilizadas, as recebidas com a confirmada e a importada). A edição monta os trechos sobre este passeio."""
    c = Cap(18, setup=setup_cfg('certificado', 'Certificado validado!'), start=(760, 400))
    c.mark(1)
    c.hover(TXT('Certificado validado!'), 0.6, at=c.A(1, 'certificado', 0.6), label='Certificado validado!')
    c.click(TRILHO('Impostos (padrão)'), at=c.A(1, 'impostos', 0.7), label='Impostos (padrão)')
    c.hover(TXT('Lucro Real:'), 0.6, at=c.A(1, 'Lucro', 0.6), label='o quadro Lucro Real:')
    c.click(TRILHO('Cenários'), at=c.A(1, 'cenário,', 0.7), label='Cenários')
    c.mark(2)
    c.click(TRILHO('Numeração'), at=c.A(2, 'numeração', 0.7), label='Numeração (Série 1)')
    c.click(TRILHO('Transportadora'), at=c.A(2, 'transportadora', 0.7), label='Transportadora (Cargas Vale do Sol)')
    c.click(MENU_FISCAL, at=c.A(2, 'viu', 0.7), label='Fiscal & Ambiental', unless=SUBMENU('Notas Fiscais (NF-e)'))
    c.click(SUBMENU('Notas Fiscais (NF-e)'), at=c.A(2, 'cota', 0.6), label='Notas Fiscais (NF-e)')
    c.click(SUBABA('Saída'), at=c.A(2, 'tolerância', 0.6), label='sub-aba Saída')
    c.hover(COTA, 0.6, at=c.A(2, 'cinco', 0.6), label='o selo da cota', noScroll=True)
    c.mark(3)
    c.hover(LINHA('#1249'), 0.4, at=c.A(3, 'zero,', 0.6), label='#1249 (do zero)')
    c.hover(LINHA('#1250'), 0.4, at=c.A(3, 'pedido', 0.6), label='#1250 (do pedido)')
    c.click(SUBABA('Entrada'), at=c.A(3, 'caixa', 0.7), label='sub-aba Entrada')
    c.hover(LINHA('#1251'), 0.6, at=c.A(3, 'fechado.', 0.4), label='#1251 (do caixa fechado)')
    c.mark(4)
    c.click(SUBABA('Saída'), at=c.A(4, 'Cancelou', 0.7), label='sub-aba Saída')
    c.hover(SEL("main tbody tr:has-text('#1249') td:has-text('Cancelada')"), 0.5, at=c.A(4, 'nota,', 0.6), label='#1249 Cancelada')
    c.hover(LINHA('#1250'), 0.4, at=c.A(4, 'correção,', 0.6), label='#1250 com a carta de correção')
    c.click(SUBABA('Inutilizadas'), at=c.A(4, 'inutilizou', 0.7), label='sub-aba Inutilizadas (1246 e 1247)')
    c.mark(5)
    c.click(SUBABA('Notas Recebidas'), at=c.A(5, 'ativou', 0.7), label='sub-aba Notas Recebidas')
    c.hover(SEL("main tbody tr:has-text('Auto Peças Vale Forte') :text-is('Confirmada')"), 0.6, at=c.A(5, 'confirmou', 0.6), label='Confirmada')
    c.hover(LINHA('Cooperativa Recomeço'), 0.8, at=c.A(5, 'importou', 0.6), label='a nota importada da Cooperativa')
    c.mark(6)
    c.fim()
    return c


CAPS_ROBO = {n: globals()[f'cap{n:02d}'] for n in range(19) if f'cap{n:02d}' in globals()}

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
