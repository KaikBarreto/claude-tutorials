#!/usr/bin/env python3
"""T07 · Comprar e vender sucata · gera rec/t07/capNN.json (roteiros do robô) a partir da voz (t07/narracao/capNN.json).

EcoSistema 1.59.154 no COMPUTADOR (janela 1280x800), Recicla Vale Metais, Rafael Nogueira (MASTER), FAKE_NOW 10/11/2026 08:35 (todos os
capítulos; a junção: depois do #85 da T6, aberto às 08:31). Uso, de qualquer pasta:  python3 -I rec/t07/gerar.py [NN ...]
Depois: ensaio.py NN (rápido) -> record.mjs --rapido -> resumo.py NN --ens -> t07_semente.py NN -> prever.py NN --ens -> gravação -> resumo.py NN.

Molde: rec/t03/gerar.py (âncoras pela palavra, marcas sozinhas, hover partido, confere*, observador de avisos). As regras de lá valem aqui.

PARTICULARIDADES DA T07:
 - Balança e impressora pelo EcoTray falso do robô ("Balança do pátio", a do mundo; semente base/balanca-ativada: leitura contínua, 1 casa).
   O peso entra ~2,4 s antes de escolher o material (sobe, oscila e estabiliza) e volta a 0 depois de cada "Incluir Item"; com o campo
   vazio e o material escolhido, a leitura contínua preenche a quantidade ("AO VIVO"). Na Pesagem avançada não há leitura contínua: o
   robô clica o botão da balança dentro de "1ª Pesagem" e "2ª Pesagem".
 - Estado de partida: cada capítulo parte de t07/inicio (caixa #85 das 08:31, preço especial da Vale Forte) + base/balanca-ativada + o
   apos-capNN do último capítulo que gravou no banco; o que não é semente (pedido em andamento, janela aberta) o setup refaz pela tela,
   fora do vídeo, com os mesmos passos do capítulo (funções it_*).
 - Menu lateral recolhido a partir do cap02 (setup); o cap01 usa o menu aberto.
 - Atalhos (Shift+V, Shift+C, Ctrl+K) só com o foco fora de campo: o robô tira o foco por eval (sem clique à toa).
 - Sem internet (cap15): navigator.onLine e os eventos offline/online por eval (o backend falso e o EcoTray continuam de pé; o app decide
   pela flag e pelo evento, hooks/useOnlineStatus.ts). Na volta, o app confirma com 2 pings (~3 s) e sincroniza sozinho.
 - PDF do comprovante sem valores (cap14): abre noutra aba, que o robô não grava; o PDF que o app gerou vai para o actions.json.
"""
import hashlib
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))           # $TUT_HOME/rec/t03
AULA = os.path.basename(HERE)                                # t03
TUT = os.path.normpath(os.path.join(HERE, '..', '..'))       # $TUT_HOME
NARR = os.path.join(TUT, AULA, 'narracao')
MUNDO = json.load(open(os.path.join(TUT, 'rec', 'mundo', 'mundo.json'), encoding='utf8'))
FAKE_NOW = '2026-11-10T08:35:00-03:00'                        # plano.md (igual no Supabase falso e no robô)
HOJE = FAKE_NOW[:10]

sys.path.insert(0, NARR)
from tts_textos import CAPS as TEXTOS  # noqa: E402  (texto atual de cada capítulo, grafia do TTS)

TROCAS = json.load(open(os.path.join(NARR, 'config_narracao.json'), encoding='utf8'))['trocas']

NOMES = ['Abertura', 'A tela Estoque', 'Cadastrar um material', 'O código do material', 'O NCM e a nota fiscal', 'Grupos de material',
         'Editar preços em massa', 'Várias tabelas de preço', 'Movimentar, transferir e zerar', 'Exportar estoque e tabela',
         'Excluir um material', 'Recapitulando']
# estado de partida (sementes extras sobre o mundo base): t03/inicio + o último apos-capNN; o cap07 abre o caixa do Rafael (base)
SEMENTE = {0: [], 1: [], 2: [], 3: ['apos-cap02'], 4: ['apos-cap03'], 5: ['apos-cap04'], 6: ['apos-cap05'], 7: ['apos-cap06'],
           8: ['apos-cap07'], 9: ['apos-cap08'], 10: ['apos-cap08'], 11: ['apos-cap08']}
EXTRA_BASE = {7: ['base/caixa-aberto']}

# folga de cada gesto: segundos entre o início do passo e o instante em que ele age (pace 0,5; medido no ensaio do T03 e na tabela
# "Custo real dos gestos" do docs/04). O `at` = palavra - folga faz o cursor CHEGAR na palavra.
FOLGA = {'click': 0.7, 'click1': 1.3, 'hover': 0.55, 'type': 0.95, 'typen': 0.05, 'press': 0.05, 'scroll': 0.15, 'eval': 0.0}
CPS = 14            # digitação "de gente" (0,17 s por letra); textos longos sem graça visual a 40


# ---------------------------------------------------------------- utilitários
def norm(s):
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode().lower()
    return ''.join(ch for ch in s if ch.isalnum())


def stable_id(chave):
    """o mesmo UUID do Supabase falso (core/util.mjs stableId) para @id:<chave>"""
    h = bytearray(hashlib.sha1(('domiflix-fake:' + chave).encode()).digest())
    h[6] = (h[6] & 0x0f) | 0x50
    h[8] = (h[8] & 0x3f) | 0x80
    x = h[:16].hex()
    return f'{x[:8]}-{x[8:12]}-{x[12:16]}-{x[16:20]}-{x[20:32]}'


def versao_app():
    try:
        return open(os.path.join(TUT, 'app', 'dist', '.versao-app'), encoding='utf8').read().strip()
    except OSError:
        return '1.59.154'


def storage_de(usuario):
    """localStorage de quem entra pela tela de login: as chaves de "já vi" que a sessão pronta do robô poria (browser.mjs) + as do mundo"""
    uid, v = stable_id(usuario), versao_app()
    t = {'user_id': uid, 'company_id': stable_id(MUNDO['config']['empresa']), 'hoje': HOJE, 'versao': v}
    troca = lambda s: re.sub(r'\{(\w+)\}', lambda m: t.get(m.group(1), m.group(0)), str(s))
    st = {'app_version': v, 'notification_shown_version': v, 'pwa-install-dismissed': 'true', 'theme': 'light'}
    st.update({troca(k): troca(val) for k, val in MUNDO.get('navegador', {}).get('localStorage', {}).items()})
    return st


def falas_do_texto(n):
    """palavras faladas (grafia do TTS) de cada linha do texto atual, sem as tags [pause], como o proc.py e o tempos_estimados.py"""
    out = []
    for linha in TEXTOS[n].split('\n'):
        linha = re.sub(r'\[[a-z ]+\]', ' ', linha)
        out.append([norm(w) for w in linha.split() if norm(w)])
    return out


def carregar_voz(n):
    d = json.load(open(os.path.join(NARR, f'cap{n:02d}.json'), encoding='utf8'))
    texto = falas_do_texto(n)
    voz = [[norm(w.get('fala', w['w'])) for w in d['words'] if w['linha'] == i] for i in range(len(d['linhas']))]
    voz = [[x for x in l if x] for l in voz]
    if len(texto) != len(voz) or any(a != b for a, b in zip(texto, voz)):
        ruins = [i + 1 for i in range(max(len(texto), len(voz))) if i >= len(texto) or i >= len(voz) or texto[i] != voz[i]]
        raise SystemExit(f'cap{n:02d}: a voz (narracao/cap{n:02d}.json) não bate com o tts_textos.py nas linhas {ruins}: '
                         f'rode de novo  bash planejamento/ecoflix/preparar_aula.sh T{AULA[1:]}  (voz estimada) ou o proc.py (voz real)')
    return d['words'], d['linhas'], d['dur'], bool(d.get('estimado'))


# ---------------------------------------------------------------- capítulo
class Cap:
    def __init__(s, n, setup, prewarm=('/login',), pace=0.5, cps=CPS, start=(700, 300), sub='', user='rafael', erros_ok=(),
                 voz_de=None, seed_extra=None):
        s.n, s.sub = n, sub
        s.nome = f'cap{n:02d}{sub}'
        s.words, s.linhas, s.dur, s.estimada = carregar_voz(n)
        s.voz_inicio = 0.0
        if voz_de:   # corte: só as linhas voz_de[0]..voz_de[1] da voz, com o tempo contado do início da primeira (T15, cap09b)
            a, b = voz_de
            off = s.linhas[a - 1]['s']
            fim = s.linhas[b - 1]['e'] + 0.4
            s.voz_inicio = round(off, 2)
            s.words = [dict(w, s=round(w['s'] - off, 3), e=round(w['e'] - off, 3), linha=w['linha'] - (a - 1)) for w in s.words if a - 1 <= w['linha'] <= b - 1]
            s.linhas = [dict(l, i=l['i'] - (a - 1), s=round(l['s'] - off, 3), e=round(l['e'] - off, 3)) for l in s.linhas[a - 1:b]]
            s.dur = round(fim - off, 2)
        s.pace, s.cps, s.start = pace, cps, start
        s.prewarm = list(prewarm)
        s.user = user
        s.setup = list(setup) + [{'do': 'eval', 'js': js_obs(erros_ok)}]
        s.seed_extra = seed_extra
        s.steps, s.anchors = [], []
        s.pending = [(0.0 if l['s'] <= 0.9 else round(l['s'] - 0.9, 2), l['i'] + 1) for l in s.linhas]

    # ---- tempo
    def L(s, i):
        return round(s.linhas[i - 1]['s'], 2)

    def W(s, i, palavra, nth=None):
        q = norm(palavra)
        hits = [w for w in s.words if w['linha'] == i - 1 and norm(w['w']) == q]
        linha = ' '.join(w['w'] for w in s.words if w['linha'] == i - 1)
        if not hits:
            raise SystemExit(f'{s.nome}: palavra "{palavra}" não achada na linha {i}: {linha}')
        if nth is None and len(hits) > 1:
            raise SystemExit(f'{s.nome}: "{palavra}" aparece {len(hits)} vezes na linha {i}: passe o nth. Linha: {linha}')
        k = nth or 0
        if k >= len(hits):
            raise SystemExit(f'{s.nome}: "{palavra}" #{k} não existe na linha {i} ({len(hits)} ocorrências): {linha}')
        return hits[k]['s']

    def at(s, w, gesto):
        """w = (linha, 'palavra'[, nth][, folga]) ou um número (segundos); devolve o `at` = palavra - folga do gesto"""
        if w is None:
            return None
        if isinstance(w, (int, float)):
            return round(max(0.0, w), 2)
        i, palavra = w[0], w[1]
        nth = w[2] if len(w) > 2 else None
        folga = w[3] if len(w) > 3 else FOLGA[gesto]
        t = round(max(0.0, s.W(i, palavra, nth) - folga), 2)
        s.anchors.append((i, palavra, gesto, t))
        return t

    # ---- marcas (sozinhas) e passos
    def flush(s, ate):
        keep = []
        for mt, mi in sorted(s.pending):
            if round(mt, 2) <= ate + 1e-9:
                s.steps.append({'do': 'mark', 'name': f'L{mi}', 'at': round(mt, 2)})
            else:
                keep.append((mt, mi))
        s.pending = keep

    def add(s, d):
        if d.get('at') is not None:
            ult = max([x['at'] for x in s.steps if 'at' in x] or [0])
            if d['at'] < ult - 1e-9:
                print(f"  aviso {s.nome}: \"{d.get('label')}\" at {d['at']} antes do passo anterior ({ult}): vai {ult}")
                d['at'] = ult
            lim = 0.8 if d.get('do') == 'hover' else 0.25
            for mt, mi in s.pending:
                if d['at'] < mt <= d['at'] + lim:
                    d['at'] = round(mt, 2)
            if d.get('do') == 'type':   # digitação que antecipa a linha: a marca entra antes dela, já no instante do passo
                for mt, mi in list(s.pending):
                    if d['at'] < mt <= d['at'] + 2.6:
                        s.steps.append({'do': 'mark', 'name': f'L{mi}', 'at': round(d['at'], 2)})
                        s.pending.remove((mt, mi))
            s.flush(d['at'])
        s.steps.append(d)
        return d

    def _p(s, d, w, gesto, label, kw):
        at = s.at(w, gesto)
        if at is not None:
            d['at'] = at
        if label:
            d['label'] = label
        d.update(kw)
        return s.add(d)

    def click(s, alvo, w=None, label=None, primeiro=False, **kw):
        return s._p({'do': 'click', 'target': alvo}, w, 'click1' if primeiro else 'click', label, kw)

    def hover(s, alvo, seconds=0.6, w=None, label=None, **kw):
        kw.setdefault('optional', True)
        kw.setdefault('timeout', 4)
        at = s.at(w, 'hover')
        if at is not None:
            for mt, mi in sorted(s.pending):   # marca logo depois do início: o hover começa junto com a linha (a marca vem antes)
                if at < mt <= at + 0.8:
                    at = round(mt, 2)
            fim = at + 0.55 + seconds   # hover que atravessa o início de uma linha sai partido (a marca entra no meio)
            for mt, mi in sorted(s.pending):
                if at + 0.3 < mt < fim - 0.25:
                    s1 = max(0.1, round(mt - at - 0.55, 2))
                    s2 = max(0.2, round(fim - mt - 0.2, 2))
                    s._p({'do': 'hover', 'target': alvo, 'seconds': s1}, at, 'hover', label, dict(kw))
                    return s._p({'do': 'hover', 'target': alvo, 'seconds': s2}, mt, 'hover', (label + ' (continua)') if label else None, dict(kw))
        return s._p({'do': 'hover', 'target': alvo, 'seconds': seconds}, at, 'hover', label, kw)

    def type(s, alvo, texto, w=None, label=None, cps=None, clicar=True, **kw):
        d = {'do': 'type', 'target': alvo, 'text': texto}
        if cps:
            d['cps'] = cps
        if not clicar:
            d['noClick'] = True
        return s._p(d, w, 'type' if clicar else 'typen', label, kw)

    def press(s, tecla, w=None, label=None, **kw):
        return s._p({'do': 'press', 'key': tecla}, w, 'press', label, kw)

    def rolar(s, by, ponto=(700, 420), w=None, label=None, duration=0.5, after=100, **kw):
        return s._p({'do': 'scroll', 'point': {'x': ponto[0], 'y': ponto[1]}, 'by': by, 'duration': duration, 'after': after}, w, 'scroll', label, kw)

    def ev(s, js, w=None, label=None, **kw):
        return s._p({'do': 'eval', 'js': js}, w, 'eval', label, kw)

    def waitfor(s, **kw):
        return s.add({'do': 'waitFor', **kw})

    def pause(s, seconds):
        return s.add({'do': 'pause', 'seconds': seconds})

    def registra(s, alvo, w=None, label=None):
        """retângulo do alvo para a câmera (zoom/destaque da edição) SEM mexer o mouse: `type` sem clique e sem texto"""
        return s._p({'do': 'type', 'target': alvo, 'text': '', 'noClick': True, 'optional': True, 'timeout': 4}, w, 'typen', label, {})

    def confere(s, escopo, esperados, label):
        """LÊ a tela e compara com o que a fala diz: 'OK: ...' ou 'DIFERENTE: ...'. Escopo 'dlg' (a última janela), 'main', 'body',
        'row:<texto>' (a linha da lista com esse texto) ou um seletor CSS. Tenta por ~6 s."""
        sel = {'dlg': '[role=dialog]', 'main': 'main', 'body': 'body'}.get(escopo, escopo)
        linha = escopo[4:] if escopo.startswith('row:') else None
        if linha is not None:
            sel = 'main tbody tr'
        esp = [esperados] if isinstance(esperados, str) else list(esperados)
        js = ("(async()=>{const norm=t=>t.replace(/[\\s\\u00a0]+/g,' ').toLowerCase();const esp=%s;let out='';"
              "for(let i=0;i<20;i++){const els=[...document.querySelectorAll(%s)].filter(e=>!%s||e.innerText.includes(%s));const el=%s?els[els.length-1]:els[0];"
              "if(!el){out='DIFERENTE: sem elemento';}else{const t=norm(el.innerText);const falta=esp.filter(e=>!t.includes(norm(e)));"
              "if(!falta.length)return 'OK: '+esp.join(' | ');out='DIFERENTE: faltou '+JSON.stringify(falta)+' em: '+t.slice(0,260);}"
              "await new Promise(r=>setTimeout(r,300));}return out})()") % (json.dumps(esp, ensure_ascii=False), json.dumps(sel), 'true' if linha is not None else 'false',
                                                                           json.dumps(linha or '', ensure_ascii=False), 'true' if escopo == 'dlg' else 'false')
        return s.add({'do': 'eval', 'js': js, 'label': 'confere ' + label})

    def confere_campos(s, esperados, label, escopo='[role=dialog]'):
        """lê o VALOR dos campos (input/textarea) do escopo e compara com o que a fala diz"""
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
        sem = s.seed_extra if s.seed_extra is not None else ([f'{AULA}/inicio'] + [f'{AULA}/{x}' for x in SEMENTE[s.n]] + EXTRA_BASE.get(s.n, []))
        corte = f'; corte das linhas da voz a partir de {str(s.voz_inicio).replace(".", ",")} s' if s.voz_inicio else ''
        d = {
            'name': f'{AULA}-{s.nome}',
            'title': f'T07 · Cap. {s.n}{s.sub} · {NOMES[s.n]} (narração {str(round(s.dur, 1)).replace(".", ",")} s{" ESTIMADA" if s.estimada else ""}{corte}; '
                     f'marcas L1..L{len(s.linhas)} = início de cada linha do roteiro; FAKE_NOW {FAKE_NOW}; usuário {s.user})',
            'seed': f'{AULA}-{s.nome}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
            'start': {'x': s.start[0], 'y': s.start[1]},
            'anonymous': True, 'storage': storage_de(f'user.{s.user}'),
            'seedExtra': sem,
            'prewarm': s.prewarm, 'setup': s.setup, 'steps': s.steps,
        }
        if s.voz_inicio:
            d['voz_inicio'] = s.voz_inicio      # a edição e o resumo.py contam a voz a partir daqui
        return d


# ---------------------------------------------------------------- alvos
BTN = lambda n, **kw: {'role': 'button', 'name': n, 'exact': True, **kw}
BTNX = lambda n, **kw: {'role': 'button', 'name': n, **kw}
TAB = lambda n, **kw: {'role': 'tab', 'name': n, 'exact': True, **kw}
TXT = lambda t, **kw: {'text': t, 'exact': True, **kw}
P = lambda t, **kw: {'text': t, 'within': 'main', **kw}
SEL = lambda s_, **kw: {'selector': s_, **kw}
DLG = '[role=dialog]'
PD = lambda t, **kw: {'text': t, 'within': DLG, **kw}
OPT = lambda n, **kw: {'role': 'option', 'name': n, **kw}
ITEM = lambda n, **kw: {'role': 'menuitem', 'name': n, **kw}
POP = '[data-radix-popper-content-wrapper]'
TOGGLE_MENU = SEL('header button:has(svg.lucide-panel-left-close), header button:has(svg.lucide-panel-left)')   # fixo no topo (y 27): noScroll
BUSCA = {'placeholder': 'Buscar material por código ou nome...'}
ACOES = lambda nome: SEL(f"main tbody tr:has-text('{nome}') td:last-child button")
CELULA = lambda nome, col: SEL(f"main tbody tr:has-text('{nome}') td:nth-child({col})")   # 2 Código, 3 Nome, 4 Estoque, ... 8 Venda
TH = lambda t: SEL(f"main thead th:has-text('{t}')")
CARTAO = lambda t: SEL(f"main div.rounded-xl:has(> div p:text-is('{t}')), main [class*=Card]:has-text('{t}')")
CAMPO = lambda id_: SEL(f'{DLG} #{id_}')
MENU = lambda href: SEL(f"a[href='{href}']")                       # item do menu lateral (recolhido: abre ao passar o mouse)
VALOR_KG = SEL("main div:has(> label:has-text('Valor/')) input")                     # Valor/kg da compra
GRADE = lambda nome, k: SEL(f"{DLG} tbody tr:has-text('{nome}') input", nth=k)   # Editar Preços em Massa: 0 compra, 1 venda


# ---------------------------------------------------------------- JS
def js_obs(ok=()):
    """observador de avisos de erro na tela (aceite: a lista sai vazia). `ok` = textos legítimos do capítulo (ex.: o cadeado do Marcos)"""
    erros = r"N[ãa]o foi poss[ií]vel|Erro ao|Tente novamente|indispon[ií]vel|Algo deu errado|Something went wrong|Falha ao|Pop-up bloqueado|Sem permiss[ãa]o"
    ign = '|'.join(re.escape(x) for x in ok) or '$^'
    return ("(()=>{window.__avisos=[];const re=new RegExp(%s,'i');const ign=new RegExp(%s,'i');const chk=(t)=>{t=(t||'').trim();"
            "const m=t&&t.match(new RegExp('[^]{0,40}('+re.source+')[^]{0,40}','i'));"
            "if(m&&!ign.test(m[0])&&window.__avisos.length<10)window.__avisos.push(m[0].replace(/[\\n\\r\\t ]+/g,' '))};new MutationObserver(ms=>{for(const m of ms){"
            "m.addedNodes.forEach(n=>chk(n.textContent));if(m.type==='characterData')chk(m.target.textContent)}}).observe(document.body,"
            "{childList:true,subtree:true,characterData:true});chk(document.body.innerText);return 1})()") % (json.dumps(erros), json.dumps(ign))


# rolagem: o contêiner que rola de verdade é o ancestral com overflow auto/scroll e conteúdo maior (T14: o 1º <main> pode não rolar);
# sem ele, a página (document.scrollingElement)
ACHA_ROLAGEM = ("const rolagem=(el)=>{let c=el&&el.parentElement;while(c&&c!==document.body){const s=getComputedStyle(c);"
                "if(/(auto|scroll)/.test(s.overflowY)&&c.scrollHeight>c.clientHeight+4)return c;c=c.parentElement;}"
                "const se=document.scrollingElement;return se&&se.scrollHeight>se.clientHeight+4?se:null};")
SUAVE = ("await new Promise(res=>{const t0=performance.now();const f=()=>{const p=Math.min(1,(performance.now()-t0)/DUR),e=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;"
         "c.scrollTop=DESTINO;p<1?requestAnimationFrame(f):res()};requestAnimationFrame(f)});")


def js_rola_ate(texto, y=250, escopo='main', dur_ms=700, prefixo=False):
    """rolagem suave do contêiner que rola o alvo (folha do DOM com o texto, dentro do escopo) até ele ficar em y px CSS; o cursor não se
    mexe. Devolve o topo final do alvo (px CSS), 'ok' (já estava lá), 'SEM ALVO' ou 'SEM ROLAGEM'."""
    alvo = json.dumps(texto, ensure_ascii=False)
    cond = f"e.textContent.trim().startsWith({alvo})" if prefixo else f"e.textContent.trim()==={alvo}"
    busca = (f"[...document.querySelectorAll({json.dumps(escopo + ' *')})].filter(e=>e.offsetParent!==null&&{cond})"
             ".sort((a,b)=>a.textContent.length-b.textContent.length)[0]")
    return ("(async()=>{" + ACHA_ROLAGEM + "const el=" + busca + ";if(!el)return 'SEM ALVO';const c=rolagem(el);if(!c)return 'SEM ROLAGEM';"
            f"const dy=Math.round(el.getBoundingClientRect().top-{int(y)});if(Math.abs(dy)<3)return 'ok';const y0=c.scrollTop;"
            + SUAVE.replace('DUR', str(int(dur_ms))).replace('DESTINO', 'y0+dy*e') +
            "return Math.round(el.getBoundingClientRect().top)})()")


def js_rola_topo(escopo='main', dur_ms=700):
    return ("(async()=>{" + ACHA_ROLAGEM + f"const c=rolagem(document.querySelector({json.dumps(escopo)}+' *'));if(!c)return 'SEM ROLAGEM';"
            "const y0=c.scrollTop;if(y0<3)return 'ok';" + SUAVE.replace('DUR', str(int(dur_ms))).replace('DESTINO', 'y0*(1-e)') +
            "return 'topo:'+Math.round(c.scrollTop)})()")


def js_valor(seletor, valor):
    """põe o valor num <input> controlado pelo React (setter nativo + input/change), sem teclado: a cor do grupo (sem a janela nativa
    do <input type=color>) e a busca feita por baixo de uma ilustração"""
    return ("(()=>{const el=document.querySelector(%s);if(!el)return 'SEM ALVO';const set=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set;"
            "set.call(el,%s);el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true}));return el.value})()") % (
        json.dumps(seletor), json.dumps(valor, ensure_ascii=False))


def js_clicar(seletor, texto=None):
    """clique por eval (sem cursor): para o que acontece por baixo de uma ilustração"""
    filtro = f".filter(e=>e.textContent.trim()==={json.dumps(texto, ensure_ascii=False)})" if texto else ''
    return (f"(()=>{{const el=[...document.querySelectorAll({json.dumps(seletor)})]{filtro}.filter(e=>e.offsetParent!==null)[0];"
            "if(!el)return 'SEM ALVO';el.click();return 'ok'})()")


JS_PDF_GANCHO = ("(()=>{if(window.__pdfs)return 'ja';window.__pdfs=[];const o=URL.createObjectURL.bind(URL);"
                 "URL.createObjectURL=(b)=>{try{if(b&&b.type==='application/pdf')window.__pdfs.push(b)}catch(e){}return o(b)};return 'gancho'})()")


def js_pdf(k, nome):
    """devolve o k-ésimo PDF que o app gerou (base64) para o actions.json: t03_pdfs.py grava o arquivo para a edição"""
    return ("(async()=>{for(let i=0;i<30&&!(window.__pdfs&&window.__pdfs.length>%d);i++)await new Promise(r=>setTimeout(r,200));"
            "const b=window.__pdfs&&window.__pdfs[%d];if(!b)return 'SEM PDF';const u=new Uint8Array(await b.arrayBuffer());let s='';"
            "for(let i=0;i<u.length;i+=8192)s+=String.fromCharCode.apply(null,u.subarray(i,i+8192));return {pdf:%s,bytes:u.length,b64:btoa(s)}})()") % (
        k, k, json.dumps(nome))


# ---------------------------------------------------------------- setup (fora do vídeo)
def setup_login(email='$TUT_USER', espera='Olá, Rafael!'):
    return [
        {'do': 'goto', 'url': '/login'}, {'do': 'waitFor', 'target': SEL('input[type=email]'), 'timeout': 30},
        {'do': 'type', 'target': SEL('input[type=email]'), 'text': email, 'cps': 40},
        {'do': 'type', 'target': SEL('input[type=password]'), 'text': '$TUT_SENHA', 'cps': 40},
        {'do': 'click', 'target': SEL('button[type=submit]')},
        {'do': 'waitFor', 'text': espera, 'timeout': 40}, {'do': 'waitFor', 'idle': True},
    ]


def vai(url, espera, timeout=25):
    return [{'do': 'goto', 'url': url}, {'do': 'waitFor', 'text': espera, 'timeout': timeout}, {'do': 'waitFor', 'idle': True}]


ESTOQUE = vai('/materiais', 'Gerencie os materiais do estoque')
RECOLHE = [{'do': 'click', 'target': TOGGLE_MENU, 'noScroll': True}, {'do': 'pause', 'seconds': 0.8}]


def setup_estoque(busca=None, extra=(), aquecer=()):
    """login, aquece as rotas do capítulo (o prewarm roda sem sessão), Estoque com o menu lateral recolhido"""
    st = setup_login()
    for url, espera in aquecer:
        st += vai(url, espera)
    st += ESTOQUE + RECOLHE
    if busca:
        st += [{'do': 'type', 'target': BUSCA, 'text': busca, 'cps': 40}, {'do': 'waitFor', 'target': P('Radiador de cobre'), 'timeout': 10}]
    return st + list(extra)


def fecha_janela(c, w=None, label='fecha a janela'):
    c.press('Escape', w=w, label=label)
    c.pause(0.5)
    c.ev("(()=>{const d=document.querySelector('[role=dialog]');if(!d)return 'ja fechada';const b=[...d.querySelectorAll('button')].find(x=>"
         "[x.textContent,x.getAttribute('aria-label')].some(v=>/^\\s*(fechar|close)\\s*$/i.test(v||'')));if(!b)return 'sem botao Fechar';b.click();return 'fechada pelo botao'})()",
         label='Fechar (se o Esc não fechou)')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)


def abre_acoes(c, nome, item, w, label=None, w_item=None):
    """menu "..." da linha (HoverDropdownMenu: abre ao PASSAR o mouse; um clique no gatilho FECHARIA o menu aberto pelo hover, T14): hover,
    um 2º hover só se o item ainda não apareceu, e o clique no item"""
    c.hover(ACOES(nome), 0.4, w=w, label=label or f'"..." da linha {nome}', optional=False, timeout=8)
    c.hover(ACOES(nome), 0.3, label='"..." de novo (só se não abriu)', unless=ITEM(item))
    c.waitfor(target=ITEM(item), timeout=6)
    return c.click(ITEM(item), w=w_item, label=item)


def js_menu_item(nome, item):
    """abre o "..." da linha e clica no item SEM cursor (por baixo de uma ilustração): o gatilho do Radix abre no pointerdown (T17) e o
    item aceita .click()"""
    return ("(async()=>{const tr=[...document.querySelectorAll('main tbody tr')].find(r=>r.innerText.includes(%s));if(!tr)return 'SEM ALVO: linha';"
            "const b=tr.querySelector('td:last-child button');if(!b)return 'SEM ALVO: botao';"
            "b.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true,cancelable:true,button:0,pointerType:'mouse'}));"
            "for(let i=0;i<30;i++){const it=[...document.querySelectorAll('[role=menuitem]')].find(e=>e.textContent.trim()===%s);"
            "if(it){it.click();return 'ok'}await new Promise(r=>setTimeout(r,100));}return 'SEM ALVO: item'})()") % (
        json.dumps(nome, ensure_ascii=False), json.dumps(item, ensure_ascii=False))




# ================================================================ T07 (o que vem acima é o molde do T03; daqui para baixo, a aula)
NOMES = ['Abertura', 'Onde ficam a compra e a venda', 'Escolher o fornecedor', 'Cadastrar o fornecedor na hora', 'Qual preço vale',
         'O peso da balança', 'Tara, impureza e dupla pesagem', 'Mesclar pesagens', 'Desconto e conferência', 'Finalizar o pedido',
         'Até três formas de pagamento', 'Fiado com parcelas', 'O cupom e o cupom sem valor', 'A tela de venda', 'Estoque insuficiente',
         'Sem internet', 'Recapitulando']
# estado de partida: t07/inicio + o último apos-capNN que mudou o banco (t07_semente.py) + base/balanca-ativada; o resto o setup refaz
SEMENTE = {0: [], 1: [], 2: [], 3: [], 4: ['apos-cap03'], 5: ['apos-cap03'], 6: ['apos-cap03'], 7: ['apos-cap03'], 8: ['apos-cap03'],
           9: ['apos-cap03'], 10: ['apos-cap09'], 11: ['apos-cap09'], 12: ['apos-cap09'], 13: ['apos-cap12'], 14: ['apos-cap12'],
           15: ['apos-cap14'], 16: ['apos-cap15']}
EXTRA_BASE = {n: ['base/balanca-ativada'] for n in range(17)}
FOLGA.update({'balanca': 0.0})

# ---------------------------------------------------------------- alvos da compra e da venda (Purchase.tsx / Sale.tsx, 1.59.154)
MAT = {'placeholder': 'Escreva o nome ou código do material'}
QTD = SEL("main div:has(> label:has-text('Quantidade (Kg)')) input")
TARA = SEL("main div:has(> label:has-text('Tara/Imp.')) input")
CAPTURA = SEL("main div:has(> label:has-text('Quantidade (Kg)')) button[aria-label='Capturar peso da balança']")
VALOR_KG = SEL("main div:has(> label:has-text('Valor/Kg')) input")
VISOR = SEL("main button:has-text('Balança do pátio')")
AO_VIVO = {'text': 'ao vivo', 'within': 'main'}
ESTOQUE_DISP = SEL("main label:has-text('Estoque Disponível')")
VALOR_ITEM = SEL("main label:has-text('Valor Total do Item')")
INCLUIR = BTN('Incluir Item')
FORN = SEL('#supplier-desktop-top')
CLIENTE = SEL('#customer-desktop-top')
CAD_FORN = SEL("main button[aria-label='Cadastrar novo fornecedor']")
TABELA = SEL("main button:has-text('Principal')")
CARTAO_PESAGEM = P('Pesagem', exact=True)
SELO = SEL("main button[aria-label='Trocar caixa']")
ITENS = SEL("main :text-matches('^Itens do Pedido')")
TOTAL_C = P('Total da Compra')
TOTAL_V = P('Total da Venda')
FINALIZAR = BTN('Finalizar')
OPCOES = BTNX('Opções avançadas')
LINHA = lambda nome, k=0: SEL(f"main tbody tr:has-text('{nome}')", nth=k)
CEL_MAT = lambda nome, k=0: SEL(f"main tbody tr:has-text('{nome}') td:nth-child(2)", nth=k)
MESCLAR = lambda nome: SEL(f"main tbody tr:has-text('{nome}') button:has(svg.lucide-merge)")
DESMESCLAR = SEL("main button[aria-label='Desmesclar pesagens']")
ACOES_ITEM = lambda nome: SEL(f"main tbody tr:has-text('{nome}') button[aria-label='Ações do item']")
LAPIS_TOTAL = SEL("main button[aria-label='Editar valor total']")
BUSCA_PARC = {'placeholder': 'Buscar por nome, apelido, CPF/CNPJ ou telefone...'}
PARCEIRO = lambda nome: SEL(f"[role=dialog] button:has-text('{nome}')")
NAO_INF = SEL("[role=dialog] button:has-text('Não informado')")
INDICADOR = lambda nome: SEL(f"[role=dialog] button[aria-label*='pendências cadastrais de {nome}']")
ALFINETE = lambda nome: SEL(f"[role=dialog] div:has(> button:has-text('{nome}')) button:has(svg.lucide-pin)")
MAIS_MODAL = SEL("[role=dialog] button:has(svg.lucide-plus)")
# Pesagem avançada (AdvancedWeighingDialog.tsx)
DCAMPO = lambda rot: SEL(f"[role=dialog] div:has(> label:text-is('{rot}'))")
CAP_PES = lambda rot: SEL(f"[role=dialog] div:has(> label:text-is('{rot}')) button[aria-label='Capturar peso da balança']")
BRUTO = SEL("[role=dialog] div:has(> label:has-text('Peso Bruto'))")
IMP_BOX = "[role=dialog] div:has(> div > label:text-is('Impureza'))"
IMP_PCT = SEL(f"{IMP_BOX} button:text-is('%')")
IMP_KG = SEL(f"{IMP_BOX} button:text-is('kg')")
IMP_IN = SEL(f"{IMP_BOX} input")
TARA_DLG = SEL("[role=dialog] div:has(> label:has-text('Tara (')) input")
LIQUIDO = SEL("[role=dialog] div:has(> label:has-text('Líquido'))")
VALOR_EST = PD('Valor estimado', exact=False)
DESCONTO = SEL("[role=dialog] div:has(> label:text-is('Desconto (R$)')) input")
VFINAL = SEL("[role=dialog] div:has(> label:text-is('Valor final')) input")
COMPLETO = SEL('label[for=wm-two]')
CONFIRMAR = BTN('Confirmar', within=DLG)
# Finalizar Pedido (MultiPaymentDialog.tsx)
TILE = lambda n: SEL(f"[role=dialog] button:has(span:text-is('{n}'))")
MULTI = SEL('#multiple-payments')
V_DIN, V_PIX, V_SALDO = SEL('#cash-amount'), SEL('#transfer-amount'), SEL('#balance-amount')
CONFIRMA_PAG = BTNX('CONFIRMAR PAGAMENTO')
VENC = SEL('label[for=balance-due-date]')
FATURAR = BTNX('Configurar faturamento (parcelas)')
SUB = "[role=dialog]:has-text('Nº de parcelas')"
INFO_SEM_VALOR = SEL("button[aria-label='Sobre comprovante sem valores']")
SW_SEM_VALOR = SEL(f"{POP} div:has(p:text-is('Comprovante sem valores')) > button[role=switch]")
VOLTAR = SEL("main a:has-text('Voltar para o caixa')")
ACAO_RAPIDA = lambda n: SEL(f"[cmdk-group]:has([cmdk-group-heading]:text-is('Ações Rápidas')) [cmdk-item]:has(span:text-is('{n}'))")
LINHA_SEM_VALOR = SEL(f"{POP} div:has(> div > p:text-is('Comprovante sem valores'))")

JS_BLUR = "(()=>{const a=document.activeElement;if(a&&a!==document.body)a.blur();return 'foco fora: '+(document.activeElement&&document.activeElement.tagName)})()"
JS_OFFLINE = ("(()=>{Object.defineProperty(navigator,'onLine',{configurable:true,get:()=>false});window.dispatchEvent(new Event('offline'));"
              "return 'offline'})()")
JS_ONLINE = ("(()=>{Object.defineProperty(navigator,'onLine',{configurable:true,get:()=>true});window.dispatchEvent(new Event('online'));"
             "return 'online'})()")


def kg(peso):
    """o valor que a leitura contínua põe no campo (1 casa: base/balanca-ativada)"""
    return f'{peso:.1f}'.replace('.', ',')


def js_espera_valor(sel, valor, ms=7000):
    """espera o <input> chegar ao valor (a leitura contínua da balança) e devolve OK/DIFERENTE"""
    return ("(async()=>{let v='';for(let i=0;i<%d;i++){const el=document.querySelector(%s);v=el?el.value:'SEM ALVO';if(v===%s)return 'OK: '+v;"
            "await new Promise(r=>setTimeout(r,200));}return 'DIFERENTE: '+v})()") % (ms // 200, json.dumps(sel), json.dumps(valor))


QTD_CSS = "main div:has(> label:has-text('Quantidade (Kg)')) input"


def js_rola_form(px=140, dur_ms=0):
    """rola a página da compra/venda para o cartão Pesagem caber inteiro na faixa de clique do robô (y 96..730: "Incluir Item" fica em
    y ~761 com a página no topo) e o "Total da Compra" sair de baixo do botão do Cato; o Fornecedor continua em y ~119"""
    if not dur_ms:
        return ("(()=>{" + ACHA_ROLAGEM + "const c=rolagem(document.querySelector('main *'));if(!c)return 'SEM ROLAGEM';c.scrollTop=%d;"
                "return 'rolado:'+Math.round(c.scrollTop)})()") % px
    return ("(async()=>{" + ACHA_ROLAGEM + "const c=rolagem(document.querySelector('main *'));if(!c)return 'SEM ROLAGEM';const y0=c.scrollTop;"
            + SUAVE.replace('DUR', str(int(dur_ms))).replace('DESTINO', 'y0+(%d-y0)*e' % px) + "return 'rolado:'+Math.round(c.scrollTop)})()")


# ---------------------------------------------------------------- setup: login e o que não é semente, refeito pela tela (fora do vídeo)
def setup_tela(url='/compra', espera='Voltar para o caixa', recolhe=True, extra=()):
    st = setup_login() + vai(url, espera)
    if recolhe:
        st += RECOLHE
    if url in ('/compra', '/venda'):
        st += [{'do': 'eval', 'js': js_rola_form()}, {'do': 'pause', 'seconds': 0.4}]
    return st + list(extra)


def st_balanca(peso, pausa=2.4):
    s = [{'do': 'balanca', 'peso': peso, 'subir': 0.6, 'oscilar': 0.6}]
    return s + ([{'do': 'pause', 'seconds': pausa}] if pausa else [])


def st_parceiro(busca, nome, botao=FORN):
    return [{'do': 'click', 'target': botao}, {'do': 'waitFor', 'target': BUSCA_PARC, 'timeout': 10},
            {'do': 'type', 'target': BUSCA_PARC, 'text': busca, 'cps': 40}, {'do': 'click', 'target': PARCEIRO(nome)},
            {'do': 'waitFor', 'gone': {'role': 'dialog'}, 'timeout': 8}, {'do': 'pause', 'seconds': 0.8}]


def st_material(busca, nome):
    return [{'do': 'click', 'target': MAT}, {'do': 'type', 'target': MAT, 'text': busca, 'noClick': True, 'cps': 40},
            {'do': 'click', 'target': OPT(nome, exact=False)}, {'do': 'pause', 'seconds': 0.6}]


def st_item(busca, nome, peso, tara=None):
    s = st_balanca(peso) + st_material(busca, nome) + [{'do': 'eval', 'js': js_espera_valor(QTD_CSS, kg(peso))}]
    if tara:
        s += [{'do': 'click', 'target': TARA}, {'do': 'type', 'target': TARA, 'text': tara, 'noClick': True, 'cps': 40}]
    return s + [{'do': 'click', 'target': INCLUIR}, {'do': 'pause', 'seconds': 0.8}] + st_balanca(0, 0.8)


def st_ferro():
    s = st_material('ferro mi', 'Ferro misto') + [{'do': 'click', 'target': BTN('Pesagem avançada')},
                                                  {'do': 'waitFor', 'text': 'Registre pesagem dupla', 'timeout': 10}]
    s += st_balanca(412) + [{'do': 'click', 'target': CAP_PES('1ª Pesagem')}, {'do': 'pause', 'seconds': 0.6}]
    s += st_balanca(96) + [{'do': 'click', 'target': CAP_PES('2ª Pesagem')}, {'do': 'pause', 'seconds': 0.6}]
    s += [{'do': 'click', 'target': IMP_PCT}, {'do': 'click', 'target': IMP_IN}, {'do': 'type', 'target': IMP_IN, 'text': '3', 'noClick': True},
          {'do': 'click', 'target': COMPLETO}, {'do': 'click', 'target': CONFIRMAR}, {'do': 'waitFor', 'gone': {'role': 'dialog'}, 'timeout': 8}]
    return s + st_balanca(0, 0.6)


def st_mescla():
    return st_item('latinha', 'Alumínio latinha', 18.4, '0,4') + [
        {'do': 'click', 'target': MESCLAR('Alumínio latinha')}, {'do': 'waitFor', 'text': 'Mesclar pesagens', 'timeout': 8},
        {'do': 'click', 'target': BTN('Mesclar Todas')}, {'do': 'waitFor', 'text': 'pesagens mescladas com sucesso', 'timeout': 8},
        {'do': 'waitFor', 'gone': {'role': 'dialog'}, 'timeout': 8}]


def st_desconto():
    return [{'do': 'click', 'target': ACOES_ITEM('Ferro misto')}, {'do': 'click', 'target': ITEM('Adicionar tara / pesagem avançada')},
            {'do': 'waitFor', 'text': 'Registre pesagem dupla', 'timeout': 10}, {'do': 'click', 'target': VFINAL},
            {'do': 'type', 'target': VFINAL, 'text': '225,00', 'noClick': True, 'clear': True, 'cps': 40},
            {'do': 'click', 'target': CONFIRMAR}, {'do': 'waitFor', 'text': 'Pesagem do item atualizada', 'timeout': 10},
            {'do': 'waitFor', 'gone': {'role': 'dialog'}, 'timeout': 8}]


ZE = st_parceiro('moreira', 'José Carlos Moreira')
ZE_DOIS = ZE + st_item('cobre mi', 'Cobre misto', 12.4) + st_item('latinha', 'Alumínio latinha', 21.6, '0,6')
VALE_FORTE = (st_parceiro('vale forte', 'Auto Peças Vale Forte') + st_item('bateria', 'Bateria automotiva', 186)
              + st_item('cobre mi', 'Cobre misto', 64))
TRES_FORMAS = [{'do': 'click', 'target': FINALIZAR}, {'do': 'waitFor', 'text': 'Finalizar Pedido', 'timeout': 10},
               {'do': 'click', 'target': MULTI}, {'do': 'pause', 'seconds': 0.5}, {'do': 'click', 'target': TILE('Pix/Transferência')},
               {'do': 'click', 'target': TILE('Saldo do Fornecedor')}, {'do': 'click', 'target': V_DIN},
               {'do': 'type', 'target': V_DIN, 'text': '200,00', 'noClick': True, 'clear': True, 'cps': 40},
               {'do': 'click', 'target': V_SALDO}, {'do': 'type', 'target': V_SALDO, 'text': '2000,00', 'noClick': True, 'clear': True, 'cps': 40},
               {'do': 'pause', 'seconds': 0.8}]
PARCELAS = [{'do': 'click', 'target': FATURAR}, {'do': 'waitFor', 'text': 'Parcelar R$', 'timeout': 8},
            {'do': 'click', 'target': SEL(f"{SUB} button:text-is('2')")}, {'do': 'click', 'target': SEL('#installment-due-1')},
            {'do': 'click', 'target': SEL(f"{POP} button:text-is('25')")}, {'do': 'pause', 'seconds': 0.5},
            {'do': 'click', 'target': BTNX('Aplicar faturamento')}, {'do': 'waitFor', 'text': '1ª em 25/11/2026', 'timeout': 8}]


# ================================================================ capítulos
def cap00():
    """Abertura: Dashboard parado sob a ilustração do pátio (L1, L2) e o cartão "Antes" (L3)."""
    c = Cap(0, setup_login() + vai('/dashboard', 'Olá, Rafael!'), start=(760, 420))
    c.hover(P('Olá, Rafael!', exact=False), 1.2, w=(3, 'caixa', 1), label='Dashboard (cartão Antes na edição)')
    c.fim()
    return c


def cap01():
    """Caixa pelo menu, Nova Compra (selo), Shift+V, Ctrl+K e Ações Rápidas, tour da Nova Compra (menu lateral aberto)."""
    c = Cap(1, setup_login() + vai('/dashboard', 'Olá, Rafael!'), start=(700, 300))
    c.click(BTN('Financeiro'), w=(1, 'Financeiro,'), label='menu Financeiro')
    c.click(MENU('/caixa'), w=(1, 'Caixa.', 1), label='Caixa (submenu)')
    c.waitfor(text='Nova Venda', timeout=15)
    c.hover(BTN('Nova Compra'), 0.5, w=(1, 'Compra'), label='Nova Compra')
    c.hover(BTN('Nova Venda'), 0.6, w=(1, 'Venda.'), label='Nova Venda')
    c.click(BTN('Nova Compra'), w=(2, 'Clicando'), label='Nova Compra (abre a compra)')
    c.waitfor(text='Voltar para o caixa', timeout=15)
    c.hover(SELO, 2.0, w=(2, 'selo'), label='selo do caixa Caixa #85 · Você (zoom)')
    c.click(VOLTAR, w=(3, 'Também'), noScroll=True, label='Voltar para o caixa')
    c.waitfor(text='Nova Venda', timeout=15)
    c.ev(JS_BLUR, w=(3, 'Shift+V', None, 0.3), label='foco fora de campo')
    c.press('Shift+V', w=(3, 'Shift+V'), label='Shift+V (abre a venda)')
    c.waitfor(text='Selecionar cliente', timeout=15)
    c.ev(JS_BLUR, w=(4, 'Ctrl+K', None, 0.3), label='foco fora de campo')
    c.press('Control+k', w=(4, 'Ctrl+K'), label='Ctrl+K (abre a busca)')
    c.waitfor(text='Ações Rápidas', timeout=10)
    c.hover(ACAO_RAPIDA('Nova Compra'), 0.5, w=(4, 'Compra'), label='Ações Rápidas: Nova Compra (zoom)')
    c.hover(ACAO_RAPIDA('Nova Venda'), 0.4, w=(4, 'Venda.'), label='Ações Rápidas: Nova Venda')
    c.click(ACAO_RAPIDA('Nova Compra'), w=(4, 'Venda.', None, -0.6), label='Nova Compra (pela busca)')
    c.waitfor(text='Voltar para o caixa', timeout=15)
    c.hover(FORN, 0.5, w=(5, 'fornecedor'), label='Fornecedor')
    c.hover(TABELA, 0.5, w=(5, 'tabela'), label='Tabela de Preços')
    c.hover(CARTAO_PESAGEM, 0.8, w=(5, 'pesagem,'), label='cartão Pesagem')
    c.hover(ITENS, 0.8, w=(5, 'itens'), label='Itens do Pedido')
    c.ev(js_rola_ate('Total da Compra', y=420), w=(5, 'embaixo,', None, 0.9), label='rola até o total')
    c.hover(TOTAL_C, 0.5, w=(5, 'total'), label='Total da Compra')
    c.hover(FINALIZAR, 0.8, w=(5, 'Finalizar.'), label='Finalizar')
    c.fim()
    return c


def cap02():
    """Selecionar Fornecedor: Não informado (zoom; ilustração L3), o indicador do Valdir (L4-L5), o alfinete, a busca Moreira."""
    c = Cap(2, setup_tela())
    c.click(FORN, w=(1, 'Clicando'), label='Selecionar fornecedor')
    c.waitfor(target=NAO_INF, timeout=10)
    c.hover(NAO_INF, 6.0, w=(1, 'Nao'), label='Não informado (zoom)')
    c.hover(INDICADOR('Valdir'), 20.0, w=(4, 'aviso'), label='indicador e balão Cadastro incompleto do Valdir (zoom)')
    c.confere(POP, ['Cadastro incompleto', 'CPF/CNPJ não informado', 'Endereço não informado', 'Use o menu ao lado'], 'balão do Valdir')
    c.hover(INDICADOR('Valdir'), 8.0, w=(5, 'telefone,', 0), label='o balão sem linha de telefone')
    c.hover(ALFINETE('Aparecida Ramos'), 2.4, w=(6, 'alfinete'), label='alfinete Fixar como padrão (Aparecida)')
    c.click(BUSCA_PARC, w=(7, 'busca,', None, 1.0), label='busca')
    c.type(BUSCA_PARC, 'Moreira', w=(7, 'busca,'), clicar=False, cps=14, label='busca Moreira')
    c.confere('dlg', ['Nenhum resultado encontrado.'], 'Nenhum resultado encontrado.')
    c.hover(PD('Nenhum resultado encontrado.'), 1.0, w=(7, 'ninguem.'), label='Nenhum resultado encontrado.')
    c.fim()
    return c


def cap03():
    """Novo Fornecedor pelo "+" do modal: nome, apelido, telefone, Chave PIX; tabela e "Também é cliente"; Salvar."""
    c = Cap(3, setup_tela(extra=[{'do': 'click', 'target': FORN}, {'do': 'waitFor', 'target': BUSCA_PARC, 'timeout': 10},
                                 {'do': 'type', 'target': BUSCA_PARC, 'text': 'Moreira', 'cps': 40},
                                 {'do': 'waitFor', 'text': 'Nenhum resultado encontrado.', 'timeout': 8}]))
    c.click(MAIS_MODAL, w=(1, 'mais.'), label='+ (cadastrar)')
    c.waitfor(text='Novo Fornecedor', timeout=10)
    c.hover(TAB('Dados de Contato'), 0.8, w=(1, 'cadastro'), label='Novo Fornecedor, Dados de Contato')
    c.click(SEL('#name'), w=(2, 'nome:'), primeiro=True, label='Nome')
    c.type(SEL('#name'), 'José Carlos Moreira', w=(2, 'Jose'), clicar=False, clear=True, cps=24, label='Nome: José Carlos Moreira')
    c.click(SEL('#contact_name'), w=(2, 'apelido,'), label='Pessoa de Contato ou Apelido')
    c.type(SEL('#contact_name'), 'Zé Moreira', w=(2, 'Ze'), clicar=False, cps=24, label='apelido: Zé Moreira')
    c.click(SEL('#phone'), w=(2, 'telefone.'), label='Telefone')
    c.type(SEL('#phone'), '12900004471', clicar=False, cps=30, label='Telefone (12) 90000-4471')
    c.click(SEL('#pix_key'), w=(3, 'chave'), label='Chave PIX')
    c.type(SEL('#pix_key'), '(12) 90000-4471', w=(3, 'Pix'), clicar=False, cps=30, label='Chave PIX (12) 90000-4471')
    c.hover(SEL(f"{DLG} div:has(> label:has-text('Tabela de Preços Padrão')) button"), 0.8, w=(3, 'tabela'), label='Tabela de Preços Padrão')
    c.hover(SEL(f"{DLG} label[for=also-counterpart]"), 0.8, w=(3, 'cliente.'), label='Também é cliente (desmarcado)')
    c.click(BTN('Salvar', within=DLG), w=(4, 'Salvar.'), label='Salvar')
    c.waitfor(text='Fornecedor cadastrado com sucesso!', timeout=10)
    c.hover(FORN, 1.2, w=(4, 'escolhido'), label='fornecedor José Carlos Moreira já escolhido')
    c.confere('main', ['José Carlos Moreira'], 'fornecedor escolhido')
    c.fim()
    return c


def cap04():
    """Tabela de Preços (lista com a estrela e a Tabela Depósitos; Esc); ilustração da hierarquia (L2, L3); o Zé na tabela principal."""
    c = Cap(4, setup_tela(extra=ZE))
    c.click(TABELA, w=(1, 'tabela'), label='Tabela de Preços (abre a lista)')
    c.waitfor(text='Tabela Depósitos', timeout=8)
    c.hover(OPT('Principal', exact=False), 1.2, w=(1, 'principal,'), label='Principal com a estrela (zoom)')
    c.hover(OPT('Tabela Depósitos', exact=False), 0.4, w=(1, 'estrela.', None, 0.2), label='Tabela Depósitos')
    c.press('Escape', w=(1, 'estrela.', None, -0.6), label='fecha a lista (fica a Principal)')
    c.hover(FORN, 0.8, w=(4, 'Ze'), label='José Carlos Moreira')
    c.hover(TABELA, 0.8, w=(4, 'principal,'), label='tabela Principal')
    c.hover(FORN, 0.6, w=(4, 'fornecedor'), label='o fornecedor antes')
    c.hover(MAT, 0.8, w=(4, 'materiais,'), label='depois o material')
    c.fim()
    return c


def cap05():
    """Cobre misto pela balança (12,4 kg, AO VIVO), cena de Windows na edição (L2), botão azul da balança, Incluir; latinha com tara 0,6."""
    c = Cap(5, setup_tela(extra=ZE))
    c.add({'do': 'balanca', 'peso': 12.4, 'subir': 0.6, 'oscilar': 0.6, 'at': c.at((1, 'Agora', None, 0.2), 'balanca'), 'label': 'cobre na balança (12,4 kg)'})
    c.click(MAT, w=(1, 'cobre'), label='Material')
    c.type(MAT, 'cobre mi', w=(1, 'misto', 0, 0.3), clicar=False, cps=30, label='material: cobre mi')
    c.click(OPT('Cobre misto', exact=False), w=(1, 'Ze.'), label='Cobre misto')
    c.ev(js_espera_valor(QTD_CSS, '12,4'), label='confere Quantidade 12,4 da balança')
    c.registra(VALOR_KG, w=(1, 'trinta'), label='Valor/Kg 36,00 (zoom)')
    c.confere_campos(['36,00'], 'Valor/Kg 36,00', escopo='main')
    c.hover(VISOR, 1.2, w=(1, 'peso:'), label='visor da balança 12,4 kg, Quantidade (Kg) e AO VIVO (zoom)')
    c.registra(QTD, w=(1, 'doze'), label='Quantidade (Kg) 12,4 da balança')
    c.registra(AO_VIVO, w=(2, 'AO'), label='selo AO VIVO')
    c.hover(CAPTURA, 3.0, w=(3, 'botao'), label='botão azul da balança dentro do campo (zoom)')
    c.hover(ESTOQUE_DISP, 0.8, w=(4, 'estoque'), label='Estoque Disponível')
    c.hover(VALOR_ITEM, 1.2, w=(4, 'valor'), label='Valor Total do Item R$ 446,40 (zoom)')
    c.confere('main', ['446,40'], 'Valor Total do Item R$ 446,40')
    c.click(INCLUIR, w=(4, 'Incluir'), label='Incluir Item (cobre)')
    c.waitfor(text='Itens do Pedido (1)', timeout=8)
    c.add({'do': 'balanca', 'peso': 0, 'subir': 0.5, 'oscilar': 0.3, 'label': 'tira o cobre da balança'})
    c.add({'do': 'balanca', 'peso': 21.6, 'subir': 0.6, 'oscilar': 0.6, 'at': c.at((5, 'Agora', None, 0.6), 'balanca'), 'label': 'latinha na balança (21,6 kg)'})
    c.click(MAT, w=(5, 'latinha,'), label='Material')
    c.type(MAT, 'latinha', w=(5, 'sacos', None, 0.3), clicar=False, cps=30, label='material: latinha')
    c.click(OPT('Alumínio latinha', exact=False), w=(5, 'rafia:'), label='Alumínio latinha')
    c.ev(js_espera_valor(QTD_CSS, '21,6'), label='confere Quantidade 21,6 da balança')
    c.registra(QTD, w=(5, 'vinte'), label='Quantidade (Kg) 21,6 e Tara/Imp. (zoom)')
    c.click(TARA, w=(5, 'Tara/Imp.,'), label='Tara/Imp.')
    c.type(TARA, '0,6', w=(5, 'zero'), clicar=False, cps=10, label='tara 0,6')
    c.hover(VALOR_ITEM, 1.2, w=(6, 'valor'), label='Valor Total do Item R$ 130,20 (zoom)')
    c.confere('main', ['130,20'], 'Valor Total do Item R$ 130,20')
    c.click(INCLUIR, w=(6, 'Incluir'), label='Incluir Item (latinha)')
    c.waitfor(text='Itens do Pedido (2)', timeout=8)
    c.add({'do': 'balanca', 'peso': 0, 'subir': 0.5, 'oscilar': 0.3, 'label': 'tira a latinha da balança'})
    c.hover(LINHA('Alumínio latinha'), 0.8, w=(6, 'Item.', None, -0.6), label='latinha na lista, com a tara 0,6')
    c.fim()
    return c


def cap06():
    """Ilustrações (L1-L3); Ferro misto e Pesagem avançada: 1ª 412, 2ª 96, bruto 316; impureza 3 % (9,48), líquido 306,52; Completo; Confirmar."""
    c = Cap(6, setup_tela(extra=ZE_DOIS))
    c.click(MAT, w=(4, 'Escolho'), label='Material')
    c.type(MAT, 'ferro mi', w=(4, 'ferro', 1, 0.2), clicar=False, cps=30, label='material: ferro mi')
    c.click(OPT('Ferro misto', exact=False), w=(4, 'misto'), label='Ferro misto')
    c.click(BTN('Pesagem avançada'), w=(4, 'Pesagem'), label='Pesagem avançada')
    c.waitfor(text='Registre pesagem dupla', timeout=10)
    c.add({'do': 'balanca', 'peso': 412, 'subir': 0.8, 'oscilar': 0.8, 'at': c.at((5, 'Carroca', 0, 2.0), 'balanca'), 'label': 'carroça cheia na balança (412 kg)'})
    c.click(CAP_PES('1ª Pesagem'), w=(5, 'primeira'), primeiro=True, label='balança da 1ª Pesagem (412)')
    c.add({'do': 'balanca', 'peso': 96, 'subir': 0.8, 'oscilar': 0.8, 'at': c.at((5, 'Carroca', 1, 1.5), 'balanca'), 'label': 'carroça vazia na balança (96 kg)'})
    c.click(CAP_PES('2ª Pesagem'), w=(5, 'segunda'), label='balança da 2ª Pesagem (96)')
    c.hover(BRUTO, 2.0, w=(5, 'bruto'), label='1ª Pesagem, 2ª Pesagem e Peso Bruto (Kg) 316 (zoom)')
    c.confere('dlg', ['412', '96', '316'], '1ª 412, 2ª 96, bruto 316')
    c.add({'do': 'balanca', 'peso': 0, 'subir': 0.5, 'oscilar': 0.3, 'label': 'carroça sai da balança'})
    c.click(IMP_PCT, w=(6, 'por'), label='Impureza em %')
    c.click(IMP_IN, w=(6, 'impureza.', None, 0.9), label='campo Impureza')
    c.type(IMP_IN, '3', w=(6, 'impureza.'), clicar=False, label='impureza 3 %')
    c.hover(SEL(f"{DLG} :text-matches('sobre bruto')"), 1.2, w=(6, 'converte:'), label='Impureza = 9,48 Kg e Líquido (Kg) 306,52 (zoom)')
    c.hover(LIQUIDO, 1.2, w=(6, 'liquido'), label='Líquido (Kg) 306,52')
    c.confere('dlg', ['9,48', '306,52'], 'impureza 9,48 kg e líquido 306,52')
    c.hover(TARA_DLG, 0.8, w=(7, 'Tara'), label='Tara (Kg) vazio')
    c.hover(IMP_KG, 0.6, w=(7, 'chave'), label='chave kg / %')
    c.hover(VALOR_EST, 1.2, w=(7, 'estimado'), label='Valor estimado R$ 229,89')
    c.confere('dlg', ['229,89'], 'Valor estimado R$ 229,89')
    c.ev(js_rola_ate('Como exibir no comprovante', y=180, escopo=DLG), w=(8, 'Aqui', None, 0.9), label='rola a janela até o comprovante')
    c.click(COMPLETO, w=(8, 'Completo,'), label='Completo')
    c.hover(DCAMPO('Motorista'), 0.6, w=(8, 'Motorista'), label='Motorista (vazio)')
    c.hover(SEL(f"{DLG} label:has-text('Placa')"), 0.5, w=(8, 'placa'), label='Placa do veículo (vazio)')
    c.click(CONFIRMAR, w=(8, 'Confirmar,'), label='Confirmar')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.hover(LINHA('Ferro misto'), 3.0, w=(9, 'Pesou'), label='linha Ferro misto 316 e 9,48 (zoom)')
    c.confere('row:Ferro misto', ['316', '9,48'], 'ferro 316 com 9,48 de impureza')
    c.fim()
    return c


def cap07():
    """2ª latinha (18,4 kg, tara 0,4), mesclar as 2 pesagens (Total mesclado 40 kg), Mesclar Todas, Desmesclar pesagens."""
    c = Cap(7, setup_tela(extra=ZE_DOIS + st_ferro()))
    c.add({'do': 'balanca', 'peso': 18.4, 'subir': 0.6, 'oscilar': 0.6, 'at': 0.0, 'label': 'latinha na balança (18,4 kg)'})
    c.click(MAT, w=(1, 'sacos'), label='Material')
    c.type(MAT, 'latinha', w=(1, 'latinha:', 0, 0.3), clicar=False, cps=30, label='material: latinha')
    c.click(OPT('Alumínio latinha', exact=False), w=(1, 'dezoito'), label='Alumínio latinha')
    c.click(TARA, w=(1, 'quatrocentos', 1), label='Tara/Imp.')
    c.type(TARA, '0,4', w=(1, 'gramas'), clicar=False, cps=10, label='tara 0,4')
    c.click(INCLUIR, w=(1, 'Agora'), label='Incluir Item (2ª latinha)')
    c.waitfor(text='Itens do Pedido (4)', timeout=8)
    c.add({'do': 'balanca', 'peso': 0, 'subir': 0.5, 'oscilar': 0.3, 'label': 'tira a latinha da balança'})
    c.hover(LINHA('Alumínio latinha', 1), 0.8, w=(1, 'duas'), label='a latinha duas vezes na lista')
    c.hover(MESCLAR('Alumínio latinha'), 1.4, w=(2, 'botao'), label='Mesclar 2 pesagens deste material')
    c.click(MESCLAR('Alumínio latinha'), w=(2, 'janela'), label='mesclar')
    c.waitfor(text='Pesagens atuais:', timeout=8)
    c.hover(PD('Pesagens atuais:'), 1.0, w=(2, 'cada'), label='Pesagens atuais: e Total mesclado: (zoom)')
    c.hover(PD('Total mesclado:', exact=False), 2.0, w=(2, 'total:'), label='Total mesclado: 40 kg (tara: 1), R$ 6,20/kg (média)')
    c.confere('dlg', ['40', '6,20'], 'Total mesclado 40 kg, R$ 6,20/kg')
    c.click(BTN('Mesclar Todas'), w=(3, 'Mesclar'), label='Mesclar Todas')
    c.waitfor(text='pesagens mescladas com sucesso', timeout=8)
    c.hover(LINHA('Alumínio latinha'), 1.4, w=(3, 'valor'), label='uma linha de latinha, R$ 241,80')
    c.confere('row:Alumínio latinha', ['241,80'], 'latinha mesclada R$ 241,80')
    c.hover(DESMESCLAR, 2.0, w=(4, 'botao'), label='Desmesclar pesagens (zoom)')
    c.fim()
    return c


def cap08():
    """Ações do item > pesagem avançada do ferro; Valor final 225,00 (Desconto 4,89); Confirmar; Total R$ 913,20; detalhe da linha; lápis."""
    c = Cap(8, setup_tela(extra=ZE_DOIS + st_ferro() + st_mescla()))
    c.click(ACOES_ITEM('Ferro misto'), w=(1, 'menu'), label='Ações do item (ferro)')
    c.click(ITEM('Adicionar tara / pesagem avançada'), w=(1, 'pesagem'), label='Adicionar tara / pesagem avançada')
    c.waitfor(text='Registre pesagem dupla', timeout=10)
    c.confere('dlg', ['412', '96', '316'], 'abre com 412, 96 e 316')
    c.ev(js_rola_ate('Valor final', y=330, escopo=DLG), w=(1, 'estava.', None, 0.2), label='rola a janela até o valor')
    c.click(VFINAL, w=(2, 'final:'), primeiro=True, label='Valor final')
    c.type(VFINAL, '225,00', w=(2, 'duzentos'), clicar=False, clear=True, cps=5, label='Valor final 225,00 (devagar)')
    c.hover(DESCONTO, 1.6, w=(2, 'desconto'), label='Desconto (R$) 4,89 e Valor final (zoom)')
    c.confere_campos(['4,89', '225,00'], 'desconto 4,89 e valor final 225,00')
    c.hover(VFINAL, 3.0, w=(3, 'dica:'), label='os dois campos (dica do ponto)')
    c.click(CONFIRMAR, w=(4, 'Confirmar.'), label='Confirmar')
    c.waitfor(text='Pesagem do item atualizada', timeout=10)
    c.hover(LINHA('Ferro misto'), 0.8, w=(4, 'ferro'), label='ferro R$ 225,00')
    c.hover(TOTAL_C, 1.6, w=(4, 'total'), label='Total da Compra R$ 913,20 (zoom)')
    c.confere('main', ['913,20'], 'Total da Compra R$ 913,20')
    c.click(CEL_MAT('Ferro misto'), w=(5, 'Clicando'), label='linha do ferro (abre o detalhe)')
    c.waitfor(text='1ª pesagem', timeout=8)
    c.hover(SEL("main tr:has-text('1ª pesagem')"), 3.0, w=(5, 'duas'), label='detalhe da pesagem (zoom)')
    c.hover(LAPIS_TOTAL, 2.0, w=(6, 'lapis'), label='lápis Editar valor total (zoom)')
    c.fim()
    return c


def cap09():
    """Finalizar: resumo; (ilustração L2) Pix com a chave; Saldo "Você deverá a ele"; Dinheiro com o saldo do caixa; confirmar; Imprimir direto."""
    c = Cap(9, setup_tela(extra=ZE_DOIS + st_ferro() + st_mescla() + st_desconto()))
    c.click(FINALIZAR, w=(1, 'Finalizar'), label='Finalizar')
    c.waitfor(text='Finalizar Pedido', timeout=10)
    c.hover(PD('Fornecedor:', exact=False), 0.6, w=(1, 'fornecedor,'), label='Resumo: fornecedor')
    c.hover(PD('Material', exact=True), 0.6, w=(1, 'itens'), label='Resumo: itens')
    c.hover(PD('Valor total', exact=False), 0.8, w=(1, 'total.'), label='Resumo: Valor total R$ 913,20')
    c.click(TILE('Pix/Transferência'), w=(3, 'Pix,', 0), label='Pix/Transferência')
    c.hover(PD('Chave PIX do fornecedor', exact=False), 2.0, w=(3, 'chave'), label='Chave PIX do fornecedor (zoom)')
    c.click(TILE('Saldo do Fornecedor'), w=(4, 'saldo,'), label='Saldo do Fornecedor')
    c.hover(PD('Saldo após o pedido:', exact=False), 2.0, w=(4, 'resumo'), label='Saldo após o pedido: Você deverá a ele (zoom)')
    c.confere('dlg', ['Você deverá a ele'], 'Você deverá a ele')
    c.click(TILE('Dinheiro'), w=(5, 'Dinheiro,', 1), label='Dinheiro')
    c.hover(PD('Saldo atual do caixa', exact=False), 1.2, w=(5, 'caixa'), label='Saldo atual do caixa')
    c.click(CONFIRMA_PAG, w=(6, 'Confirmar'), label='CONFIRMAR PAGAMENTO')
    c.waitfor(text='Compra registrada!', timeout=12)
    c.waitfor(text='Imprimir Comprovante', timeout=10)
    c.click(BTNX('Imprimir direto'), w=(6, 'cupom'), label='Imprimir direto')
    c.waitfor(text='Comprovante enviado para impressora', timeout=10)
    c.fim()
    return c


def cap10():
    """Auto Peças Vale Forte: bateria com preço especial 3,40 (186 kg), cobre misto 64 kg, total 2.936,40; Finalizar com 3 formas."""
    c = Cap(10, setup_tela())
    c.click(FORN, w=(1, 'Chegou'), label='Selecionar fornecedor')
    c.type(BUSCA_PARC, 'vale forte', w=(1, 'Auto'), cps=30, label='busca vale forte')
    c.click(PARCEIRO('Auto Peças Vale Forte'), w=(1, 'oficina.'), label='Auto Peças Vale Forte')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.add({'do': 'balanca', 'peso': 186, 'subir': 0.6, 'oscilar': 0.6, 'label': 'bateria na balança (186 kg)'})
    c.click(MAT, label='Material')
    c.type(MAT, 'bateria', clicar=False, cps=40, label='material: bateria')
    c.click(OPT('Bateria automotiva', exact=False), w=(2, 'Repara', None, 0.5), label='Bateria automotiva')
    c.hover(SEL('[data-sonner-toast]'), 1.6, w=(2, 'aviso:', None, 0.3), label='aviso Preço especial aplicado (o mouse segura o aviso)')
    c.confere('body', ['Preço especial aplicado para Bateria automotiva'], 'aviso Preço especial aplicado')
    c.registra(VALOR_KG, w=(2, 'tres', 0), label='Valor/Kg 3,40 (zoom)')
    c.confere_campos(['3,40'], 'Valor/Kg 3,40', escopo='main')
    c.click(INCLUIR, w=(3, 'cento'), label='Incluir Item (bateria)')
    c.add({'do': 'balanca', 'peso': 64, 'subir': 0.6, 'oscilar': 0.6, 'label': 'cobre na balança (64 kg)'})
    c.click(MAT, label='Material')
    c.type(MAT, 'cobre mi', clicar=False, cps=40, label='material: cobre mi')
    c.click(OPT('Cobre misto', exact=False), w=(3, 'sessenta'), label='Cobre misto')
    c.ev(js_espera_valor(QTD_CSS, '64,0'), label='confere Quantidade 64,0 da balança')
    c.click(INCLUIR, w=(3, 'Total:', None, 1.0), label='Incluir Item (cobre)')
    c.add({'do': 'balanca', 'peso': 0, 'subir': 0.5, 'oscilar': 0.3, 'label': 'tira o cobre da balança'})
    c.hover(TOTAL_C, 1.6, w=(3, 'dois'), label='Total da Compra R$ 2.936,40 (zoom)')
    c.confere('main', ['2.936,40'], 'Total da Compra R$ 2.936,40')
    c.click(FINALIZAR, w=(4, 'dono'), label='Finalizar')
    c.waitfor(text='Finalizar Pedido', timeout=10)
    c.click(MULTI, w=(4, 'Multiplas'), primeiro=True, label='Múltiplas formas de pagamento')
    c.hover(TILE('Dinheiro'), 0.3, w=(5, 'Escolho', 0), label='Dinheiro (já vem marcado)')
    c.click(TILE('Pix/Transferência'), w=(5, 'tres'), label='Pix/Transferência')
    c.confere('dlg', ['Formas de pagamento (máx. 3)'], 'rótulo Formas de pagamento (máx. 3)')
    c.click(TILE('Saldo do Fornecedor'), w=(5, 'formas.'), label='Saldo do Fornecedor')
    c.click(V_DIN, w=(5, 'Duzentos'), label='valor do Dinheiro')
    c.type(V_DIN, '200,00', w=(5, 'dinheiro,'), clicar=False, clear=True, cps=14, label='Dinheiro 200,00')
    c.click(V_SALDO, w=(5, 'dois'), label='valor do Saldo')
    c.type(V_SALDO, '2000,00', w=(5, 'saldo,'), clicar=False, clear=True, cps=14, label='Saldo 2000,00')
    c.hover(V_PIX, 2.0, w=(5, 'setecentos'), label='os três valores: Pix completa 736,40 (zoom)')
    c.confere_campos(['200,00', '736,40', '2.000,00'], 'Dinheiro 200, Pix 736,40, Saldo 2.000')
    c.hover(PD('Chave PIX do fornecedor', exact=False), 0.8, w=(5, 'conta.'), label='a conta do Pix')
    c.hover(PD('Total', exact=True), 1.4, w=(6, 'soma'), label='bloco Total (sem Faltam nem Excesso)')
    c.hover(PD('Distribuição do pagamento', exact=False), 1.2, w=(6, 'Faltam'), label='Distribuição do pagamento')
    c.hover(CONFIRMA_PAG, 1.0, w=(6, 'botao'), label='CONFIRMAR PAGAMENTO liberado')
    c.fim()
    return c


def cap11():
    """Vencimento (opcional); Configurar faturamento: 2 parcelas, a 1ª em 25/11; (ilustração L4) Aplicar; confirmar."""
    c = Cap(11, setup_tela(extra=VALE_FORTE + TRES_FORMAS))
    c.hover(VENC, 2.0, w=(1, 'Vencimento.'), label='Vencimento (opcional) (zoom)')
    c.click(FATURAR, w=(2, 'Configurar'), label='Configurar faturamento (parcelas)')
    c.waitfor(text='Parcelar R$', timeout=8)
    c.hover(SEL(f"{SUB} label:has-text('Condição de pagamento')"), 0.8, w=(2, 'partes,'), label='Condição de pagamento: Manual')
    c.click(SEL(f"{SUB} button:text-is('2')"), w=(3, 'Duas'), primeiro=True, label='Nº de parcelas: 2')
    c.click(SEL('#installment-due-1'), w=(3, 'mudo'), label='data da 1ª parcela')
    c.click(SEL(f"{POP} button:text-is('25')"), w=(3, 'vinte'), label='25 de novembro')
    c.hover(SEL('#installment-due-2'), 0.8, w=(3, 'dez'), label='2ª parcela 10/12/2026')
    c.hover(SEL(f"{SUB} :text-is('Soma das parcelas')"), 1.4, w=(3, 'soma'), label='as duas linhas e a Soma das parcelas (zoom)')
    c.confere(SUB, ['25/11/2026', '10/12/2026', '1.000,00'], 'parcelas 25/11 e 10/12 de R$ 1.000,00')
    c.click(BTNX('Aplicar faturamento'), w=(5, 'Aplicar'), label='Aplicar faturamento')
    c.waitfor(text='1ª em 25/11/2026', timeout=8)
    c.hover(PD('1ª em 25/11/2026', exact=False), 2.0, w=(5, 'parcelas,', 0), label='2 parcelas, 1ª em 25/11/2026 (zoom)')
    c.hover(PD('Faturamento a prazo', exact=False), 2.0, w=(5, 'dica:'), label='resumo: Faturamento a prazo')
    c.click(CONFIRMA_PAG, w=(6, 'Confirmar'), label='CONFIRMAR PAGAMENTO')
    c.waitfor(text='Compra registrada!', timeout=12)
    c.waitfor(text='Imprimir Comprovante', timeout=10)
    c.fim()
    return c


def cap12():
    """Imprimir Comprovante (Imprimir direto / Visualizar), (ilustração L3) Opções avançadas: Comprovante sem valores e o balão."""
    c = Cap(12, setup_tela(extra=VALE_FORTE + TRES_FORMAS + PARCELAS + [
        {'do': 'click', 'target': CONFIRMA_PAG}, {'do': 'waitFor', 'text': 'Compra registrada!', 'timeout': 12},
        {'do': 'waitFor', 'text': 'Deseja imprimir o comprovante', 'timeout': 10}, {'do': 'pause', 'seconds': 1.0}]))
    c.hover(BTNX('Imprimir direto'), 1.2, w=(1, 'Imprimir'), label='Imprimir direto')
    c.hover(BTN('Visualizar', within=DLG), 1.2, w=(1, 'Visualizar,'), label='Visualizar')
    c.click(BTNX('Imprimir direto'), w=(2, 'Imprimir'), label='Imprimir direto')
    c.waitfor(text='Comprovante enviado para impressora', timeout=10)
    c.click(OPCOES, w=(4, 'preco?'), label='Opções avançadas')
    c.waitfor(text='Ajustes usados de vez em quando', timeout=8)
    c.hover(LINHA_SEM_VALOR, 1.2, w=(4, 'Comprovante'), label='Comprovante sem valores (zoom)')
    c.hover(OPCOES, 0.6, w=(4, 'Opcoes'), label='botão Opções avançadas, do lado do Finalizar')
    c.hover(INFO_SEM_VALOR, 6.0, w=(5, 'pedido', 0), label='balão: o pedido é salvo normalmente (zoom)')
    c.hover(LINHA_SEM_VALOR, 4.0, w=(5, 'dica:'), label='Comprovante sem valores (desligado)')
    c.press('Escape', w=(5, 'venda.', None, -0.4), label='fecha o menu sem ligar nada')
    c.fim()
    return c


def cap13():
    """Shift+V: Nova Venda; Fundição; latão 152 kg (Lucro 668,80); (ilustração L3) o olho; Estoque Disponível 62; Comprovante sem valores."""
    c = Cap(13, setup_tela())
    c.ev(JS_BLUR, w=(1, 'vender.', None, 0.3), label='foco fora de campo')
    c.press('Shift+V', w=(1, 'vender.'), label='Shift+V (Nova Venda)')
    c.waitfor(text='Selecionar cliente', timeout=15)
    c.ev(js_rola_form(dur_ms=500), label='rola o formulário (o cartão Pesagem inteiro)')
    c.click(CLIENTE, w=(1, 'cliente,'), label='Selecionar cliente')
    c.type(BUSCA_PARC, 'bandeira', w=(1, 'preco', None, 0.3), cps=30, label='busca bandeira')
    c.click(PARCEIRO('Fundição Bandeira do Vale'), w=(2, 'Fundicao'), label='Fundição Bandeira do Vale')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.add({'do': 'balanca', 'peso': 152, 'subir': 0.6, 'oscilar': 0.6, 'at': c.at((2, 'leva'), 'balanca'), 'label': 'latão na balança (152 kg)'})
    c.click(MAT, w=(2, 'cinquenta'), label='Material')
    c.type(MAT, 'latão', clicar=False, cps=30, label='material: latão')
    c.click(OPT('Metal amarelo (latão)', exact=False), w=(2, 'trinta'), label='Metal amarelo (latão)')
    c.ev(js_espera_valor(QTD_CSS, '152,0'), label='confere Quantidade 152,0 da balança')
    c.click(INCLUIR, w=(2, 'Repara'), label='Incluir Item (latão)')
    c.add({'do': 'balanca', 'peso': 0, 'subir': 0.5, 'oscilar': 0.3, 'label': 'tira o latão da balança'})
    c.hover(SEL("main thead th:has-text('Lucro')"), 1.6, w=(2, 'coluna'), label='coluna Lucro R$ 668,80 e Lucro estimado (zoom)')
    c.hover(P('Lucro estimado', exact=False), 1.6, w=(2, 'estimado'), label='Lucro estimado R$ 668,80')
    c.confere('main', ['668,80', '4.848,80'], 'lucro 668,80 e total 4.848,80')
    c.hover(SEL("main button:has(svg.lucide-eye), main button:has(svg.lucide-eye-off)"), 1.2, w=(3, 'olho'), label='o olho do lucro estimado')
    c.click(MAT, w=(4, 'dica:'), label='Material')
    c.type(MAT, 'latão', w=(4, 'Estoque', 0, 0.6), clicar=False, cps=30, label='material: latão de novo')
    c.click(OPT('Metal amarelo (latão)', exact=False), w=(4, 'Estoque', 0, 0.2), label='Metal amarelo (latão), sem incluir')
    c.hover(ESTOQUE_DISP, 4.0, w=(4, 'Tinha'), label='Estoque Disponível 62, Em estoque 214, Nesta venda -152 (zoom)')
    c.confere('main', ['Em estoque: 214', '152'], 'Estoque Disponível: 214 em estoque, -152 nesta venda')
    c.click(OPCOES, w=(5, 'Opcoes'), label='Opções avançadas')
    c.waitfor(text='Ajustes usados de vez em quando', timeout=8)
    c.click(SW_SEM_VALOR, w=(5, 'ligo'), label='liga Comprovante sem valores')
    c.press('Escape', w=(5, 'valores.', None, -0.5), label='fecha o menu')
    c.fim()
    return c


def cap14():
    """Cobre mel 60 kg x 42 em estoque: Estoque insuficiente, origem Cobre misto 18 kg, Transferir e Adicionar; Pix; PDF sem valores."""
    c = Cap(14, setup_tela('/venda', 'Selecionar cliente', extra=st_parceiro('bandeira', 'Fundição Bandeira do Vale', CLIENTE)
                           + st_item('latão', 'Metal amarelo (latão)', 152) + [
                               {'do': 'click', 'target': OPCOES}, {'do': 'waitFor', 'text': 'Ajustes usados de vez em quando', 'timeout': 8},
                               {'do': 'click', 'target': SW_SEM_VALOR}, {'do': 'press', 'key': 'Escape'}, {'do': 'pause', 'seconds': 0.6},
                               {'do': 'eval', 'js': JS_PDF_GANCHO}]))
    c.add({'do': 'balanca', 'peso': 60, 'subir': 0.6, 'oscilar': 0.6, 'at': 0.0, 'label': 'cobre mel na balança (60 kg)'})
    c.click(MAT, w=(1, 'cobre'), label='Material')
    c.type(MAT, 'cobre mel', w=(1, 'mel,', None, 0.4), clicar=False, cps=30, label='material: cobre mel')
    c.click(OPT('Cobre mel', exact=False), w=(1, 'sistema'), label='Cobre mel')
    c.hover(ESTOQUE_DISP, 1.0, w=(1, 'quarenta'), label='Estoque Disponível 42')
    c.click(INCLUIR, w=(1, 'incluir,'), label='Incluir Item (cobre mel)')
    c.waitfor(text='Estoque insuficiente nesta unidade', timeout=8)
    c.hover(PD('Faltam', exact=False), 2.4, w=(1, 'faltam'), label='Faltam 18 Kg de Cobre mel. (zoom)')
    c.confere('dlg', ['Faltam 18 Kg de Cobre mel.'], 'Faltam 18 Kg de Cobre mel.')
    c.click(SEL(f"{DLG} button[role=combobox]"), w=(2, 'origem,'), primeiro=True, label='Origem do estoque (abre a lista)')
    c.waitfor(text='Esta unidade', timeout=8)
    c.hover(SEL(f"{POP} :text-is('Esta unidade')"), 1.2, w=(2, 'materiais'), label='grupo Esta unidade')
    c.click(OPT('Cobre misto', exact=False), w=(3, 'puxo'), label='Cobre misto')
    c.click(SEL(f"{DLG} div:has(> label:has-text('Quantidade')) input"), w=(3, 'dezoito', None, 0.9), label='Quantidade (Kg)')
    c.type(SEL(f"{DLG} div:has(> label:has-text('Quantidade')) input"), '18', w=(3, 'dezoito'), clicar=False, label='18 kg')
    c.hover(PD('Quantidade coberta', exact=False), 1.2, w=(3, 'misto.', 1), label='Quantidade coberta')
    c.click(BTNX('Transferir e Adicionar'), w=(5, 'Transferir'), label='Transferir e Adicionar')
    c.waitfor(text='agendada para a finalização da venda', timeout=8)
    c.add({'do': 'balanca', 'peso': 0, 'subir': 0.5, 'oscilar': 0.3, 'label': 'tira o cobre da balança'})
    c.hover(LINHA('Cobre mel'), 1.2, w=(5, 'agendada'), label='linha Cobre mel (Lucro R$ 324,00)')
    c.hover(TOTAL_V, 1.6, w=(5, 'sete'), label='Total da Venda R$ 7.722,80 e Lucro estimado R$ 992,80 (zoom)')
    c.hover(P('Lucro estimado', exact=False), 1.4, w=(5, 'lucro'), label='Lucro estimado R$ 992,80')
    c.confere('main', ['7.722,80', '992,80'], 'total 7.722,80 e lucro 992,80')
    c.hover(ITENS, 3.0, w=(6, 'Se'), label='a lista (Cancelar, Inserir mesmo assim: só na fala)')
    c.click(FINALIZAR, w=(7, 'Fundicao'), label='Finalizar')
    c.waitfor(text='Finalizar Pedido', timeout=10)
    c.click(TILE('Pix/Transferência'), w=(7, 'Pix.'), primeiro=True, label='Pix/Transferência')
    c.click(CONFIRMA_PAG, w=(7, 'Confirmar'), label='CONFIRMAR PAGAMENTO')
    c.waitfor(text='Venda registrada!', timeout=12)
    c.waitfor(text='Deseja imprimir o comprovante de venda?', timeout=10)
    c.click(BTN('Visualizar', within=DLG), w=(7, 'Como'), label='Visualizar')
    c.click(BTNX('Visualizar PDF'), w=(7, 'comprovante', 1), label='Visualizar PDF (o PDF abre noutra aba)')
    c.ev(js_pdf(0, 'venda-fundicao-sem-valores'), label='PDF sem valores (para a edição)')
    c.fim()
    return c


def cap15():
    """A internet cai: faixa e Modo Offline; Shift+C, Dona Cida com 14,6 kg de latinha em dinheiro: Compra salva localmente; Pendências no
    caixa; a internet volta e sincroniza; (ilustração L5)."""
    c = Cap(15, setup_tela('/venda', 'Selecionar cliente'))
    c.ev(JS_OFFLINE, w=(1, 'cair'), label='a internet cai (navigator.onLine e evento offline)')
    c.waitfor(text='Sem conexão', timeout=8)
    c.hover(P('Sem conexão', exact=False), 1.6, w=(1, 'faixa'), label='faixa Sem conexão (zoom)')
    c.hover(P('Modo Offline', exact=False), 1.0, w=(1, 'trabalho'), label='Modo Offline')
    c.ev(JS_BLUR, w=(1, 'internet.', 1, 0.4), label='foco fora de campo')
    c.press('Shift+C', w=(1, 'internet.', 1, 0.2), label='Shift+C (Nova Compra)')
    c.waitfor(text='Voltar para o caixa', timeout=15)
    c.ev(js_rola_form(dur_ms=500), label='rola o formulário (o cartão Pesagem inteiro)')
    c.click(FORN, w=(2, 'Chegou'), label='Selecionar fornecedor')
    c.type(BUSCA_PARC, 'cida', w=(2, 'Dona'), cps=30, label='busca cida')
    c.click(PARCEIRO('Aparecida Ramos'), w=(2, 'latinha.'), label='Aparecida Ramos')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.add({'do': 'balanca', 'peso': 14.6, 'subir': 0.6, 'oscilar': 0.6, 'at': c.at((2, 'latinha.', None, -0.2), 'balanca'), 'label': 'latinha na balança (14,6 kg)'})
    c.click(MAT, w=(2, 'continua'), label='Material')
    c.type(MAT, 'latinha', clicar=False, cps=40, label='material: latinha')
    c.click(OPT('Alumínio latinha', exact=False), w=(2, 'EcoTray'), label='Alumínio latinha')
    c.ev(js_espera_valor(QTD_CSS, '14,6'), label='confere Quantidade 14,6 da balança')
    c.registra(QTD, w=(2, 'catorze'), label='Quantidade 14,6 com o EcoTray (zoom)')
    c.click(INCLUIR, w=(2, 'seiscentos.'), label='Incluir Item')
    c.add({'do': 'balanca', 'peso': 0, 'subir': 0.5, 'oscilar': 0.3, 'label': 'tira a latinha da balança'})
    c.click(FINALIZAR, w=(2, 'Finalizo'), label='Finalizar')
    c.waitfor(text='Finalizar Pedido', timeout=10)
    c.click(TILE('Dinheiro'), w=(2, 'dinheiro,'), primeiro=True, label='Dinheiro')
    c.click(CONFIRMA_PAG, w=(2, 'guardada'), label='CONFIRMAR PAGAMENTO')
    c.waitfor(text='Compra salva localmente', timeout=12)
    c.hover(SEL("[data-sonner-toast]:has-text('salva localmente')"), 1.8, w=(2, 'numero'), label='aviso Compra salva localmente (OFFLINE-C-...) (zoom)')
    c.click(VOLTAR, w=(3, 'No', None, 1.2), noScroll=True, label='Voltar para o caixa')
    c.waitfor(text='Pendências de Sincronização', timeout=12)
    c.hover(P('Aparecida Ramos', exact=False), 2.0, w=(3, 'Pendencias'), label='cartão Aparecida Ramos em Pendências de Sincronização (zoom)')
    c.ev(JS_ONLINE, w=(4, 'Quando', None, 1.6), label='a internet volta (evento online)')
    c.waitfor(text='sincronizadas com sucesso', timeout=20)
    c.hover(P('sincronizadas com sucesso', exact=False), 1.6, w=(4, 'Pronto:'), label='Operações sincronizadas com sucesso! (zoom)')
    c.fim()
    return c


def cap16():
    """Recapitulando: a montagem é da edição; o robô passa pelo caixa do dia."""
    c = Cap(16, setup_tela('/caixa', 'Nova Venda', recolhe=False))
    c.hover(BTN('Nova Compra'), 1.0, w=(1, 'caixa,'), label='Nova Compra')
    c.hover(BTN('Nova Venda'), 1.0, w=(4, 'vendeu'), label='Nova Venda')
    c.fim()
    return c


CAPS = {f'{n:02d}': globals()[f'cap{n:02d}'] for n in range(17)}

if __name__ == '__main__':
    pedidos = sys.argv[1:] or sorted(CAPS)
    for a in pedidos:
        k = f'{int(a):02d}'
        c = CAPS[k]()
        d = c.out()
        ult = -1
        for st in d['steps']:   # o `at` precisa ser crescente
            if 'at' in st:
                if st['at'] < ult - 1e-9:
                    print(f'  aviso {c.nome}: at {st["at"]} < {ult} em "{st.get("label") or st.get("name")}"')
                ult = max(ult, st['at'])
        if os.environ.get('ANCORAS'):
            for i, w, g, t in c.anchors:
                print(f'   L{i} "{w}" ({g}) -> at {t}')
        caminho = os.path.join(HERE, f'{c.nome}.json')
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
        print(f'{c.nome}: {len(d["steps"])} passos, narração {c.dur:.1f} s{" (ESTIMADA)" if c.estimada else ""} -> {os.path.relpath(caminho, TUT)}')
