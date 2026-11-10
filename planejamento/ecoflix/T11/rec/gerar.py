#!/usr/bin/env python3
"""T11 · Produção: gera rec/t11/cap00..cap14.json (roteiros do robô) a partir da voz (t11/narracao/capNN.json).

EcoSistema 1.59.154 no Supabase falso (mundo da Recicla Vale Metais), computador 1280x800, logado como Rafael Nogueira (MASTER).
Cada passo é preso a uma palavra da fala: `at` = início da palavra - folga (o custo do gesto, docs/04 "Custo real dos gestos"),
para o cursor CHEGAR na palavra. A voz ainda é a ESTIMADA (tempos_estimados.py): quando a voz de verdade chegar, o capNN.json da
voz substitui o estimado e este gerador roda de novo, sem reescrever nada. Rodar de qualquer pasta: `python3 -I rec/t11/gerar.py [NN ...]`.

Relógio do mundo (FAKE_NOW, igual no Supabase falso e no robô): 2026-11-10T08:30:00-03:00 nos caps 0 a 6 e 17:30 do 7 ao 14
(o lançamento é "no fim do dia"). O título de cada roteiro diz qual; a instância do Supabase falso sobe com o mesmo.

Estado de partida: sementes rec/mundo/seeds-extra/t11/ (rec/t11/t11_sementes.py), acumuladas por capítulo (SEMENTE abaixo).

Login: o capítulo abre SEM sessão ("anonymous") e o `setup` (fora do vídeo) entra pela tela de login com "$TUT_USER"/"$TUT_SENHA"
(variáveis de ambiente; o Supabase falso aceita qualquer senha). O `storage` leva as chaves de "já vi" que o modo logado do robô
punha sozinho (versão do app, tarefas do dia, preferências iniciais): sem elas, avisos do app abririam por cima da tela.

Particularidades (lições desta aula):
 - A 1280 px com o menu lateral aberto, o quadro corta a coluna "Concluída" e a ficha técnica transborda para os lados. O `setup`
   recolhe o menu (botão do cabeçalho); só o cap00 mostra o menu aberto e o recolhe na tela (aviso de edição explica).
 - Menu recolhido abre ao passar o mouse (Sidebar.tsx, fecha 500 ms depois de sair): o cursor nunca passa por x < 60 sem querer.
 - As abas da Produção são botões `#tab-btn-<valor>` (orders, quick, recipes, machines, report, settings).
 - Seletores de material (MaterialCombobox) são campos de texto que abrem a lista ao focar: clicar, digitar e escolher a opção.
 - Observador `OBS` guarda em `window.__avisos` todo aviso de erro do app, tela escura e a faixa "Lembrete da trilha"; o último
   passo de cada capítulo devolve a lista (tem de sair vazia). `confere*` LÊ a tela e compara com a fala (resumo.py acusa DIFERENTE).
"""
import hashlib
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TUT = os.path.normpath(os.path.join(HERE, '..', '..'))
NARR = os.path.join(TUT, 't11', 'narracao')
NOW_MANHA = '2026-11-10T08:30:00-03:00'
NOW_TARDE = '2026-11-10T17:30:00-03:00'
FAKE_NOW = {n: (NOW_TARDE if n >= 7 else NOW_MANHA) for n in range(15)}


def stable_id(chave):
    """o mesmo UUID estável do Supabase falso (core/util.mjs stableId)"""
    h = bytearray(hashlib.sha1(('domiflix-fake:' + chave).encode()).digest())
    h[6] = (h[6] & 0x0F) | 0x50
    h[8] = (h[8] & 0x3F) | 0x80
    x = h[:16].hex()
    return f'{x[:8]}-{x[8:12]}-{x[12:16]}-{x[16:20]}-{x[20:32]}'


RAFAEL = stable_id('user.rafael')
try:
    VERSAO = open(os.path.join(TUT, 'app', 'dist', '.versao-app'), encoding='utf8').read().strip() or '1.59.154'
except OSError:
    VERSAO = '1.59.154'
HOJE = '2026-11-10'
# "já vi" dos avisos que atrapalhariam a gravação (o que o robô põe sozinho na sessão logada; aqui a sessão nasce no login)
STORAGE = {
    'app_version': VERSAO, 'notification_shown_version': VERSAO, f'dominex:daily-tasks-shown:{RAFAEL}': HOJE,
    'pwa-install-dismissed': 'true', 'theme': 'light', f'daily-tasks-reminder-last-shown-{RAFAEL}': HOJE, 'initial-preferences-set': 'true',
}

NOMES = ['Abertura', 'O que a Produção resolve', 'A receita do produto', 'Quanto entra por unidade', 'Coprodutos',
         'Criar a ordem de produção', 'O Kanban', 'A produção do dia', 'O real contra o teórico', 'Perda acima da tolerância',
         'Finalizar e fechar o custo', 'Relatório de Produção', 'Os ajustes da Produção', 'Excluir uma ordem concluída', 'Recapitulando']
CADEIA = ['inicio', 'apos-cap03', 'apos-cap04', 'apos-cap05', 'apos-cap06', 'apos-cap09', 'apos-cap10', 'apos-cap12', 'apos-cap13']
# estado de partida de cada capítulo = a última semente da cadeia que ele recebe (as anteriores vêm junto)
SEMENTE = {0: 'inicio', 1: 'inicio', 2: 'inicio', 3: 'inicio', 4: 'apos-cap03', 5: 'apos-cap04', 6: 'apos-cap05', 7: 'apos-cap06',
           8: 'apos-cap06', 9: 'apos-cap06', 10: 'apos-cap09', 11: 'apos-cap10', 12: 'apos-cap10', 13: 'apos-cap12', 14: 'apos-cap13'}


def sementes(n):
    return [f't11/{s}' for s in CADEIA[:CADEIA.index(SEMENTE[n]) + 1]]


def norm(s):
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode().lower()
    return ''.join(ch for ch in s if ch.isalnum() or ch in '?')


def carregar_voz(n):
    d = json.load(open(os.path.join(NARR, f'cap{n:02d}.json'), encoding='utf8'))
    return d['words'], d['linhas'], float(d['dur']), bool(d.get('estimado'))


# Observador de avisos de erro na tela (aceite): textos com "Não foi possível", "Erro ao", "Tente novamente", "indisponível",
# "Algo deu errado", tela escura (div.fixed preta) e a faixa "Lembrete da trilha de tutoriais" da EcoFlix.
OBS = ("(()=>{window.__avisos=[];const re=/N[ãa]o foi poss[ií]vel|Erro ao|Tente novamente|indispon[ií]vel|Algo deu errado|Falha ao/i;"
       "const chk=(t)=>{t=(t||'').trim();const m=t&&t.match(new RegExp('[^]{0,40}('+re.source+')[^]{0,40}','i'));"
       "if(m&&window.__avisos.length<10)window.__avisos.push(m[0].replace(/[\\n\\r\\t ]+/g,' '))};new MutationObserver(ms=>{for(const m of ms){"
       "m.addedNodes.forEach(n=>chk(n.textContent));if(m.type==='characterData')chk(m.target.textContent)}}).observe(document.body,"
       "{childList:true,subtree:true,characterData:true});chk(document.body.innerText);"
       "setInterval(()=>{const f=document.querySelector('section[aria-label^=\"Lembrete da trilha\"]');"
       "if(f&&window.__avisos.length<10&&!window.__avisos.includes('TRILHA ECOFLIX'))window.__avisos.push('TRILHA ECOFLIX')},300);return 1})()")


class Cap:
    def __init__(s, n, pace=0.5, cps=9, start=(900, 440), setup=None, noscroll=False):
        s.n = n
        s.words, s.linhas, s.dur, s.estimada = carregar_voz(n)
        s.steps = []
        s.pace, s.cps, s.start = pace, cps, start
        s.noscroll = noscroll
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

    def A(s, i, palavra, folga=0.7, nth=0):
        """`at` = início da palavra - folga (folga = custo do gesto até o cursor chegar; negativa = depois da palavra)"""
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
        t = s.L(i)
        if t <= 0.5:
            s.steps.append({'do': 'mark', 'name': f'L{i}', 'at': 0})
        else:
            s.pending.append((round(t - 0.2, 2), i))

    def _p(s, d, at, label, kw):
        if s.noscroll and d.get('do') in ('click', 'hover', 'type', 'drag') and 'noScroll' not in kw:
            kw = {**kw, 'noScroll': True}
        if at is not None:
            d['at'] = round(at, 2)
        if label:
            d['label'] = label
        d.update(kw)
        return s.add(d)

    def click(s, target, at=None, label=None, **kw):
        return s._p({'do': 'click', 'target': target}, at, label, kw)

    def hover(s, target, seconds=0.4, at=None, label=None, **kw):
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

    def drag(s, target, to, at=None, label=None, **kw):
        return s._p({'do': 'drag', 'target': target, 'to': to}, at, label, kw)

    def rolar(s, by, at=None, label=None, ponto=(900, 440), duration=0.5, after=100):
        return s._p({'do': 'scroll', 'point': {'x': ponto[0], 'y': ponto[1]}, 'by': by, 'duration': duration, 'after': after}, at, label, {})

    def cursor(s, ponto, at=None, label=None):
        """leva o cursor a um ponto neutro (scroll de 0 px): tira o mouse de cima de um menu ou de um cartão"""
        return s._p({'do': 'scroll', 'point': {'x': ponto[0], 'y': ponto[1]}, 'by': 0, 'duration': 0.3, 'after': 0}, at, label, {})

    def registra(s, target, at=None, label=None):
        """registra o retângulo do alvo para a câmera (zoom/destaque) SEM mexer o mouse"""
        return s._p({'do': 'type', 'target': target, 'text': '', 'noClick': True, 'optional': True, 'timeout': 4}, at, label, {})

    def pause(s, seconds):
        return s.add({'do': 'pause', 'seconds': seconds})

    def waitfor(s, **kw):
        return s.add({'do': 'waitFor', **kw})

    def ev(s, js, at=None, label=None, **kw):
        return s._p({'do': 'eval', 'js': js}, at, label, kw)

    def confere(s, escopo, esperados, label):
        """`eval` que LÊ a tela e compara com o que a fala diz: "OK: ..." ou "DIFERENTE: ...". Escopo 'dlg' (a última janela), 'main',
        'body' ou um seletor CSS. Tenta por ~6,5 s."""
        sel = {'dlg': '[role=dialog]', 'main': 'main', 'body': 'body'}.get(escopo, escopo)
        esp = [esperados] if isinstance(esperados, str) else list(esperados)
        js = ("(async()=>{const norm=t=>t.replace(/[\\s\\u00a0]+/g,' ').toLowerCase();const esp=%s;let out='';"
              "for(let i=0;i<22;i++){const els=[...document.querySelectorAll(%s)];const el=%s?els[els.length-1]:els[0];"
              "if(!el){out='DIFERENTE: sem elemento';}else{const t=norm(el.innerText);const falta=esp.filter(e=>!t.includes(norm(e)));"
              "if(!falta.length)return 'OK: '+esp.join(' | ');out='DIFERENTE: faltou '+JSON.stringify(falta)+' em: '+t.slice(0,260);}"
              "await new Promise(r=>setTimeout(r,300));}return out})()") % (json.dumps(esp, ensure_ascii=False), json.dumps(sel), 'true' if escopo == 'dlg' else 'false')
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
        return {
            'name': f't11-cap{s.n:02d}',
            'title': f'T11 · Cap. {s.n} · {NOMES[s.n]} (narração {str(round(s.dur, 1)).replace(".", ",")} s{" ESTIMADA" if s.estimada else ""}; '
                     f'marcas L1..L{len(s.linhas)} = início de cada linha do roteiro; FAKE_NOW {FAKE_NOW[s.n]})',
            'seed': f't11-cap{s.n:02d}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
            'start': {'x': s.start[0], 'y': s.start[1]},
            'anonymous': True, 'storage': dict(STORAGE),
            'seedExtra': sementes(s.n),
            'prewarm': ['/login'], 'setup': s.setup, 'steps': s.steps,
        }


# ---------------------------------------------------------------- alvos
BTN = lambda n, **kw: {'role': 'button', 'name': n, 'exact': True, **kw}
BTNX = lambda n, **kw: {'role': 'button', 'name': n, **kw}
TXT = lambda t, **kw: {'text': t, 'exact': True, **kw}
TXTX = lambda t, **kw: {'text': t, **kw}
SEL = lambda s, **kw: {'selector': s, **kw}
OPT = lambda n, **kw: {'role': 'option', 'name': n, **kw}
DLG = '[role=dialog]'
ABA = lambda v: SEL(f'#tab-btn-{v}')          # abas da Produção: orders, quick, recipes, machines, report, settings
PH = lambda p, **kw: {'placeholder': p, **kw}

# ---------------------------------------------------------------- setup (fora do vídeo)
LOGIN = [
    {'do': 'waitFor', 'target': PH('seu@email.com'), 'timeout': 40},
    {'do': 'type', 'target': PH('seu@email.com'), 'text': '$TUT_USER', 'cps': 40},
    {'do': 'type', 'target': PH('••••••••'), 'text': '$TUT_SENHA', 'cps': 40},
    {'do': 'click', 'target': BTN('Entrar')},
    {'do': 'waitFor', 'url': '/dashboard', 'timeout': 40},
    {'do': 'waitFor', 'idle': True, 'timeout': 25},
]
RECOLHE_MENU = ("(()=>{const b=document.querySelector('header svg.lucide-panel-left-close')?.closest('button');"
                "if(!b)return document.querySelector('header svg.lucide-panel-left')?'ja recolhido':'sem botao';b.click();return 'recolhido'})()")
PROD_OK = 'Fichas técnicas, ordens de produção e custo por peça'


def setup_prod(extra=(), aquece=()):
    """login, aquece as rotas que o capítulo visita, recolhe o menu e para em Produção (aba Ordens de Produção)"""
    st = list(LOGIN)
    for r in aquece:
        st += [{'do': 'goto', 'url': r}, {'do': 'waitFor', 'idle': True, 'timeout': 25}]
    st += [{'do': 'goto', 'url': '/producao'}, {'do': 'waitFor', 'text': PROD_OK, 'timeout': 30}, {'do': 'waitFor', 'idle': True, 'timeout': 25},
           {'do': 'eval', 'js': RECOLHE_MENU}, {'do': 'wait', 'seconds': 0.8}]
    return st + list(extra)


# rolagem suave do contêiner que rola o alvo (molde do T14: ACHA_ROLAGEM + SUAVE): o cursor não se mexe
ACHA_ROLAGEM = ("const rolagem=(el)=>{let c=el&&el.parentElement;while(c&&c!==document.body){const s=getComputedStyle(c);"
                "if(/(auto|scroll)/.test(s.overflowY)&&c.scrollHeight>c.clientHeight+4)return c;c=c.parentElement;}"
                "const se=document.scrollingElement;return se&&se.scrollHeight>se.clientHeight+4?se:null};")
SUAVE = ("await new Promise(res=>{const f=t=>{const p=Math.min(1,(t-t0)/DUR),e=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;c.scrollTo({top:DESTINO,behavior:'instant'});"
         "p<1?requestAnimationFrame(f):res()};requestAnimationFrame(f)});")


def js_ate(texto, y=250, dur_ms=900, escopo='main', prefixo=False):
    """rola (suave) o contêiner do alvo até a folha do DOM cujo texto é `texto` ficar em y px CSS. Devolve o topo final do alvo,
    'ok' (já estava lá), 'SEM ALVO' ou 'SEM ROLAGEM'."""
    alvo = json.dumps(texto)
    sel = json.dumps(f'{escopo} *')
    busca = (f"[...document.querySelectorAll({sel})].filter(e=>e.textContent.trim().startsWith({alvo})).sort((a,b)=>a.textContent.length-b.textContent.length)[0]"
             if prefixo else f"[...document.querySelectorAll({sel})].find(e=>e.children.length===0&&e.textContent.trim()==={alvo})")
    return ("(async()=>{" + ACHA_ROLAGEM + "const el=" + busca + ";if(!el)return 'SEM ALVO';const c=rolagem(el);if(!c)return 'SEM ROLAGEM';"
            f"const dy=Math.round(el.getBoundingClientRect().top-{int(y)});if(Math.abs(dy)<3)return 'ok';const y0=c.scrollTop,t0=performance.now();"
            + SUAVE.replace('DUR', str(int(dur_ms))).replace('DESTINO', 'y0+dy*e') +
            "return Math.round(el.getBoundingClientRect().top)})()")


def rola_ate(c, texto, at, label, y=250, dur_ms=900, escopo='main', prefixo=False):
    return c.ev(js_ate(texto, y, dur_ms, escopo, prefixo), at=at, label=label)


def js_topo(escopo='main', dur_ms=700):
    sel = json.dumps(escopo)
    return ("(async()=>{" + ACHA_ROLAGEM + f"const raiz=document.querySelector({sel});let c=null;"
            "for(const e of [raiz,...(raiz?raiz.querySelectorAll('*'):[])]){if(!e)continue;const s=getComputedStyle(e);if(/(auto|scroll)/.test(s.overflowY)&&e.scrollHeight>e.clientHeight+4&&e.scrollTop>2){c=e;break}}"
            "if(!c){const se=document.scrollingElement;if(se&&se.scrollTop>2)c=se}if(!c)return 'ok';const y0=c.scrollTop,t0=performance.now();"
            + SUAVE.replace('DUR', str(int(dur_ms))).replace('DESTINO', 'y0*(1-e)') + "return 'topo:'+Math.round(c.scrollTop)})()")


def fechar_janela(c, at=None, espera=0.4):
    c.press('Escape', at=at, label='fecha a janela')
    c.add({'do': 'wait', 'seconds': espera})
    c.waitfor(gone={'role': 'dialog'}, timeout=8)


# ================================================================ capítulos
CAPS_ROBO = {}


def capitulo(fn):
    CAPS_ROBO[int(fn.__name__[3:])] = fn
    return fn


# ---------------------------------------------------------------- alvos da Produção (rec/t11/_ex: explorações de 10/11)
MENU = '[data-sidebar=sidebar]'
LISTA_FICHAS = "aside[aria-label='Lista de fichas técnicas']"
FICHA = lambda nome: SEL(f"{LISTA_FICHAS} button:has-text('{nome}')")
CARTAO_PRODUTO = SEL("main div.ring-2:has(p:text-is('Produto final'))")          # o cartão "Produto final" (em destaque)
NOME_PRODUTO = SEL("main div.ring-2 p.text-lg")
CONSUMO_POR = SEL("main div.ring-2 div.border-dashed")
MAIS_PRODUTO = SEL("main button[title='Criar novo produto']")
ROT_MP = SEL("main label:has-text('Matérias-primas')")
ROT_PF = SEL("main div.ring-2 p:text-is('Produto final')")
COPRODUTOS = SEL("main label:has-text('Coprodutos')")
QTD_COPRODUTO = TXT('Quantidade digitada no lançamento do dia')
CARTAO_INSUMO = lambda nome: SEL(f"main div.group:has(p:text-is('{nome}'))")    # cartão do insumo/coproduto na ficha
CABECALHO_PAGINA = SEL("main h1:has-text('Produção')")

# Ficha nova do cap02 refeita fora do vídeo (setup dos caps 3): Nova, Alumínio latinha, Fardo de alumínio, sem salvar
REFAZ_FICHA = [
    {'do': 'click', 'target': ABA('recipes')}, {'do': 'waitFor', 'text': 'Selecione uma ficha técnica', 'timeout': 15},
    {'do': 'click', 'target': BTN('Nova')}, {'do': 'waitFor', 'text': 'Nova ficha técnica', 'timeout': 10},
    {'do': 'click', 'target': PH('Escolher material')}, {'do': 'type', 'target': PH('Escolher material'), 'text': 'latinha', 'noClick': True, 'cps': 40},
    {'do': 'click', 'target': OPT('Alumínio latinha')}, {'do': 'wait', 'seconds': 0.5},
    {'do': 'click', 'target': PH('Selecione o produto')}, {'do': 'type', 'target': PH('Selecione o produto'), 'text': 'fardo', 'noClick': True, 'cps': 40},
    {'do': 'click', 'target': OPT('Fardo de alumínio')}, {'do': 'wait', 'seconds': 0.6},
]


def js_rola_main(y):
    """rolagem instantânea do contêiner principal (o <main> que rola) até scrollTop = y: só no setup (fora do vídeo)"""
    return ("(()=>{const m=[...document.querySelectorAll('main')].find(e=>/(auto|scroll)/.test(getComputedStyle(e).overflowY)&&e.scrollHeight>e.clientHeight+4);"
            f"if(!m)return 'SEM ROLAGEM';m.scrollTop={int(y)};return m.scrollTop}})()")


DLG_ROLA = "[role=dialog] div.overflow-y-auto"
CARTAO_OP = lambda n: SEL(f"main div.group:has(span:text-is('#{n}'))")         # cartão da ordem no quadro
PEGA_OP = lambda n: SEL(f"main div.group:has(span:text-is('#{n}')) p.font-medium")   # o nome do produto no cartão: ponto seguro para clicar e arrastar
# (o botão "Finalizar" e os ícones do canto param o arrasto no pointerdown e o clique neles abre outra coisa)
CAB_COLUNA = lambda nome: BTN(nome, within='main')                                  # nome da coluna no cabeçalho (abre "Editar coluna")
CORPO_COLUNA = lambda nome: SEL(f"main div.rounded-xl:has(> div button:text-is('{nome}')) > div.flex-1")   # corpo da coluna (onde se solta o cartão)
CHECK_CONCLUSAO = SEL("main span[title='Coluna de conclusão']")
POPPER = '[data-radix-popper-content-wrapper]'


def js_quadro_x(dx, dur_ms=700):
    """rola (suave) a faixa do quadro na horizontal: dx > 0 mostra o fim (botão "Coluna"), dx < 0 volta ao começo"""
    return ("(async()=>{const c=[...document.querySelectorAll('main div')].find(e=>/(auto|scroll)/.test(getComputedStyle(e).overflowX)&&e.scrollWidth>e.clientWidth+4);"
            "if(!c)return 'SEM ROLAGEM';const x0=c.scrollLeft,t0=performance.now();"
            f"const alvo=Math.max(0,Math.min(c.scrollWidth-c.clientWidth,x0+({int(dx)})));"
            "await new Promise(res=>{const f=t=>{const p=Math.min(1,(t-t0)/" + str(int(dur_ms)) + "),e=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;"
            "c.scrollLeft=x0+(alvo-x0)*e;p<1?requestAnimationFrame(f):res()};requestAnimationFrame(f)});return 'x:'+Math.round(c.scrollLeft)})()")


@capitulo
def cap00():
    """Abertura: Dashboard com o menu aberto; L3 Materiais > Produção pelo menu; L4 recolhe o menu (mais espaço para o quadro)."""
    setup = list(LOGIN) + [{'do': 'goto', 'url': '/producao'}, {'do': 'waitFor', 'text': PROD_OK, 'timeout': 30}, {'do': 'waitFor', 'idle': True, 'timeout': 25},
                           {'do': 'goto', 'url': '/dashboard'}, {'do': 'waitFor', 'idle': True, 'timeout': 25}, {'do': 'wait', 'seconds': 1.0}]
    c = Cap(0, setup=setup, start=(760, 470))
    c.mark(1)
    c.registra(SEL(MENU), at=0.4, label='menu lateral (câmera parada)')
    c.mark(2)
    c.mark(3)
    c.click(BTN('Materiais', within=MENU), at=c.A(3, 'Materiais,', 0.8), label='menu Materiais')
    c.click({'role': 'link', 'name': 'Produção', 'exact': True, 'within': MENU}, at=c.A(3, 'Produção,', 0.7, nth=1), label='menu Produção')
    c.waitfor(text=PROD_OK, timeout=15)
    c.confere('main', ['Produção', PROD_OK, 'Ordens de Produção', 'A fazer', 'Em produção', 'Concluída'], 'tela Produção no quadro')
    c.mark(4)
    c.click(SEL("header button:has(svg.lucide-panel-left-close)"), at=c.A(4, 'Se', 0.5), label='recolhe o menu lateral (aviso: mais espaço para o quadro)', noScroll=True)
    c.cursor((760, 470), at=c.A(4, 'dá', 0.3), label='cursor sai do menu')
    c.registra(SEL('main'), at=c.A(4, 'Vamos', 0.3), label='quadro da Produção inteiro')
    c.fim()
    return c


@capitulo
def cap01():
    """O que a Produção resolve: as abas (L1), ilustração (L2 a L4), a tela de volta (L5, dica falada da tela de bloqueio)."""
    c = Cap(1, setup=setup_prod())
    c.mark(1)
    c.registra(SEL("main nav:has(#tab-btn-orders)"), at=c.A(1, 'esquerdo', 0.2), label='[ZOOM] coluna de abas')
    c.hover(ABA('orders'), 0.3, at=c.A(1, 'Ordens', 0.6), label='aba Ordens de Produção')
    c.hover(ABA('recipes'), 0.3, at=c.A(1, 'Fichas', 0.6), label='aba Fichas Técnicas')
    c.hover(ABA('report'), 0.3, at=c.A(1, 'Relatório', 0.6), label='aba Relatório')
    c.hover(ABA('settings'), 0.5, at=c.A(1, 'Configurações.', 0.6), label='aba Configurações')
    c.cursor((780, 520), at=c.A(1, 'Configurações.', -0.6), label='cursor sai das abas')
    c.mark(2)
    c.mark(3)
    c.mark(4)
    c.mark(5)
    c.registra(CABECALHO_PAGINA, at=c.A(5, 'dica:', 0.2), label='a tela Produção de volta (dica falada)')
    c.fim()
    return c


@capitulo
def cap02():
    """A receita do produto: Fichas Técnicas, Nova, latinha entra, fardo sai, o "+" (sem clicar) e o Nome da ficha."""
    c = Cap(2, setup=setup_prod())
    c.mark(1)
    c.click(ABA('recipes'), at=c.A(1, 'ficha', 0.8), label='aba Fichas Técnicas')
    c.waitfor(text='Selecione uma ficha técnica', timeout=10)
    c.confere('main', ['Fichas técnicas', 'Cobre mel', 'Kg', 'Selecione uma ficha técnica'], 'lista com o Cobre mel')
    c.hover(FICHA('Cobre mel'), 0.6, at=c.A(1, 'receita', 0.6), label='a ficha do Cobre mel na lista')
    c.cursor((980, 470), at=c.A(1, 'sai.', 0.2), label='cursor ao painel da direita')
    c.mark(2)
    c.mark(3)
    c.click(BTN('Nova'), at=c.A(3, 'Nova.', 0.8), label='Nova')
    c.waitfor(text='Nova ficha técnica', timeout=10)
    c.confere('main', ['Nova ficha técnica', 'Monte a receita: matérias-primas entram, o produto final sai.', 'Produto final'], 'Nova ficha técnica')
    c.hover(ROT_MP, 0.5, at=c.A(3, 'matérias-primas', 0.6), label='Matérias-primas (entram)')
    c.hover(ROT_PF, 0.5, at=c.A(3, 'produto', 0.6), label='Produto final')
    c.mark(4)
    c.click(PH('Escolher material'), at=c.A(4, 'esquerdo,', 0.7), label='Escolher material')
    c.type(PH('Escolher material'), 'latinha', at=c.A(4, 'matéria-prima.', 0.05), noClick=True, cps=40, label='digita latinha')
    c.click(OPT('Alumínio latinha'), at=c.A(4, 'Alumínio', 0.6), label='Alumínio latinha')
    c.mark(5)
    c.click(PH('Selecione o produto'), at=c.A(5, 'direito,', 0.7), label='Selecione o produto')
    c.type(PH('Selecione o produto'), 'fardo', at=c.A(5, 'produto', 0.05), noClick=True, cps=40, label='digita fardo')
    c.click(OPT('Fardo de alumínio'), at=c.A(5, 'Fardo', 0.6), label='Fardo de alumínio')
    c.confere('main div.ring-2', ['Fardo de alumínio', 'unidade de produção: pç'], 'cartão Produto final com o fardo')
    # o cartão "Produto final" passa 48 px da borda do painel a 1280 px (achado do app): o foco no "+" faz o próprio navegador
    # rolar o painel e mostrar o cartão inteiro (como Tab faria para uma pessoa)
    c.press('Tab', at=c.A(5, 'cadastrado', 0.1), label='Tab: o foco vai ao "+" e o painel mostra o cartão inteiro')
    c.hover(NOME_PRODUTO, 0.6, at=c.A(5, 'material,', 0.6), label='o Fardo de alumínio no cartão')
    c.mark(6)
    c.hover(MAIS_PRODUTO, 1.4, at=c.A(6, 'botão', 0.6), label='[ZOOM] botão + (Criar novo produto), sem clicar')
    c.mark(7)
    c.hover(SEL('#recipe-name'), 1.2, at=c.A(7, 'nome', 0.6), label='Nome da ficha (vazio, o nome do produto de exemplo)')
    c.fim()
    return c


@capitulo
def cap03():
    """Quanto entra por unidade: unidade Kg, Qtd 1, Peças por unidade vazio, Salvar ficha, a ficha do Cobre mel (1,6)."""
    c = Cap(3, setup=setup_prod(REFAZ_FICHA + [{'do': 'eval', 'js': js_rola_main(100)}, {'do': 'wait', 'seconds': 0.4}]))
    c.mark(1)
    c.click(SEL('#recipe-unit'), at=c.A(1, 'unidade', 0.7), label='Unidade de produção')
    c.click(OPT('Kg — Quilograma'), at=c.A(1, 'quilo.', 0.6), label='Kg — Quilograma')
    c.confere('main div.ring-2', ['unidade de produção: Kg', 'Consumo por Kg'], 'cartão em Kg')
    c.mark(2)
    c.click(PH('Qtd'), at=c.A(2, 'quantidade', 0.7), label='[ZOOM] campo Qtd do Alumínio latinha')
    c.type(PH('Qtd'), '1', at=c.A(2, 'um.', 0.05, nth=3), noClick=True, cps=20, label='Qtd 1')
    c.confere(CONSUMO_POR['selector'], ['Consumo por Kg', '1 Kg'], 'Consumo por Kg 1 Kg')
    c.mark(3)
    c.hover(CONSUMO_POR, 1.2, at=c.A(3, 'perde', 0.6), label='o cartão Produto final (Consumo por Kg)')
    c.mark(4)
    c.hover(SEL('#recipe-pack'), 2.0, at=c.A(4, 'Peças', 0.6), label='Peças por unidade de venda (vazio)')
    rola_ate(c, 'Salvar ficha', at=c.A(4, 'fardo', 0.3), label='desce até Salvar ficha (o campo Peças continua na tela)', y=560)
    c.mark(5)
    c.click(BTN('Salvar ficha'), at=c.A(5, 'Salvar', 0.7), label='Salvar ficha')
    c.waitfor(text='Ficha técnica salva', timeout=10)
    c.ev(js_topo(), at=c.A(5, 'Pronto,', 0.2), label='sobe à lista')
    c.confere(LISTA_FICHAS, ['Fardo de alumínio', 'Cobre mel'], 'a lista com o fardo')
    c.hover(FICHA('Fardo de alumínio'), 0.9, at=c.A(5, 'lista.', 0.6), label='Fardo de alumínio na lista')
    c.mark(6)
    c.click(FICHA('Cobre mel'), at=c.A(6, 'Cobre', 0.7), label='a ficha do Cobre mel')
    c.waitfor(text='Editar ficha técnica', timeout=10)
    c.confere('main', ['Editar ficha técnica', 'Fio de cobre encapado', 'Cobre mel', 'Consumo por Kg'], 'ficha do Cobre mel')
    c.confere_campos(['1,6'], 'Qtd 1,6 do fio', escopo='main')
    c.hover(CARTAO_INSUMO('Fio de cobre encapado'), 1.6, at=c.A(6, 'quilo', 0.6, nth=1), label='[ZOOM] cartão Fio de cobre encapado com 1,6')
    c.mark(7)
    c.fim()
    return c


@capitulo
def cap04():
    """Coprodutos: a ficha do fardo, desce aos coprodutos, Adicionar coproduto > Chaparia, Salvar ficha."""
    c = Cap(4, setup=setup_prod([{'do': 'click', 'target': ABA('recipes')}, {'do': 'waitFor', 'text': 'Selecione uma ficha técnica', 'timeout': 15},
                                 {'do': 'wait', 'seconds': 0.4}]))
    c.mark(1)
    c.click(FICHA('Fardo de alumínio'), at=c.A(1, 'quando', 0.7), label='a ficha do Fardo de alumínio')
    c.waitfor(text='Editar ficha técnica', timeout=10)
    rola_ate(c, 'Use quando a produção gera mais de um material (ex.: sobra reaproveitável).', at=c.A(1, 'coproduto.', 1.0), label='desce até Coprodutos', y=330)
    c.mark(2)
    c.mark(3)
    c.click(BTNX('Adicionar coproduto'), at=c.A(3, 'entra', 0.7), label='Adicionar coproduto')
    c.click(PH('Escolher material'), at=c.A(3, 'quantidade.', 0.7), label='Escolher material (coproduto)')
    c.type(PH('Escolher material'), 'chap', at=c.A(3, 'Adiciono', 0.05), noClick=True, cps=40, label='digita chap')
    c.click(OPT('Chaparia'), at=c.A(3, 'Chaparia,', 0.6), label='Chaparia')
    c.confere('main', ['Chaparia', 'Quantidade digitada no lançamento do dia'], 'cartão da Chaparia')
    c.hover(QTD_COPRODUTO, 1.6, at=c.A(3, 'avisa:', 0.6), label='[ZOOM] cartão Chaparia: Quantidade digitada no lançamento do dia')
    c.mark(4)
    c.click(BTN('Salvar ficha'), at=c.A(4, 'Salvar', 0.7), label='Salvar ficha')
    c.waitfor(text='Ficha técnica salva', timeout=10)
    c.hover(CARTAO_INSUMO('Chaparia'), 0.8, at=c.A(4, 'completa.', 0.6), label='a receita completa')
    c.fim()
    return c


@capitulo
def cap05():
    """Criar a ordem de produção: Nova produção, ficha do fardo, 500, Marcos, equipe Cláudio e Diego, consumo e custo estimados, Criar ordem."""
    c = Cap(5, setup=setup_prod())
    c.mark(1)
    c.registra(SEL("main h2:has-text('Ordens de produção')"), at=c.A(1, 'ordem', 0.3), label='o quadro de ordens')
    c.mark(2)
    c.mark(3)
    c.click(BTN('Nova produção'), at=c.A(3, 'Nova', 0.8), label='Nova produção')
    c.waitfor(text='Nova ordem de produção', timeout=10)
    c.confere('dlg', ['Nova ordem de produção', 'Planeje a produção a partir de uma ficha técnica. Depois você vai lançando a produção dia a dia.'], 'janela Nova ordem')
    c.click(PH('Escreva o nome ou código do produto'), at=c.A(3, 'ficha,', 0.7), label='Ficha técnica *')
    c.type(PH('Escreva o nome ou código do produto'), 'fardo', at=c.A(3, 'escolho', 0.05), noClick=True, cps=40, label='digita fardo')
    c.click(OPT('Fardo de alumínio'), at=c.A(3, 'Fardo', 0.6), label='a ficha do Fardo de alumínio')
    c.mark(4)
    c.click(SEL('#prod-planned'), at=c.A(4, 'quantidade', 0.7), label='[ZOOM] Quantidade planejada *')
    c.type(SEL('#prod-planned'), '500', at=c.A(4, 'quinhentos', 0.05), noClick=True, cps=20, label='500')
    c.confere_campos(['500', '2026-11-10'], 'quantidade 500 e a data de hoje')
    c.mark(5)
    c.hover(SEL('#prod-date'), 0.8, at=c.A(5, 'data', 0.6), label='Data da produção (hoje)')
    c.click(SEL('#prod-responsible'), at=c.A(5, 'responsável,', 0.7), label='Responsável')
    c.click(OPT('Marcos Antunes'), at=c.A(5, 'Marcos,', 0.6), label='Marcos Antunes')
    c.mark(6)
    c.click(SEL('#prod-team'), at=c.A(6, 'equipe,', 0.7), label='Equipe (quem vai produzir)')
    c.click(TXTX('Cláudio Ferraz', within=POPPER), at=c.A(6, 'Cláudio', 0.6), label='Cláudio Ferraz')
    c.click(TXTX('Diego Morais', within=POPPER), at=c.A(6, 'Diego.', 0.6), label='Diego Morais')
    c.press('Escape', at=c.A(6, 'equipe', 0.1, nth=1), label='fecha a lista da equipe')
    c.waitfor(gone={'selector': POPPER}, timeout=5)
    c.confere('dlg', ['Marcos Antunes', '2 funcionários', 'Quem vai produzir esta ordem.'], 'responsável e equipe')
    c.hover(TXTX('Quem vai produzir esta ordem.', within=DLG), 1.0, at=c.A(6, 'lançamento', 0.6), label='a ajuda da equipe')
    c.mark(7)
    rola_ate(c, 'Custo estimado por peça', at=c.A(7, 'Embaixo', 0.2), label='desce ao consumo teórico estimado', y=560, escopo=DLG)
    c.confere('dlg', ['Consumo teórico estimado', 'Alumínio latinha', '500', 'R$ 3.100,00', 'Custo estimado por peça', 'R$ 6,20'], 'consumo e custo estimados')
    c.registra(SEL(f"{DLG} div.space-y-3:has(> div > label:text-is('Consumo teórico estimado'))"), at=c.A(7, 'consumo', 0.2),
               label='[ZOOM] bloco Consumo teórico estimado')
    c.hover(TXT('500', within=DLG), 0.8, at=c.A(7, 'quinhentos', 0.6), label='Qtd teórica 500')
    c.hover(TXT('R$ 6,20', within=DLG), 1.2, at=c.A(7, 'seis', 0.6), label='Custo estimado por peça R$ 6,20')
    c.mark(8)
    c.hover(TXT('Custo estimado por peça', within=DLG), 1.2, at=c.A(8, 'peça,', 0.6), label='"por peça" (vale quilo)')
    c.mark(9)
    c.click(BTN('Criar ordem'), at=c.A(9, 'Criar', 0.7), label='Criar ordem')
    c.waitfor(text='Ordem criada', timeout=10)
    c.waitfor(target=TXT('#3', within='main'), timeout=10)
    c.confere('main', ['#3', 'Rascunho', 'Fardo de alumínio', 'planejado:', '500', 'Kg', 'Rafael Nogueira', '10/11/2026', 'Equipe:', '2 funcionários'], 'cartão #3 em A fazer')
    c.hover(CARTAO_OP(3), 0.9, at=c.A(9, 'três', 0.6), label='o cartão #3 em A fazer')
    c.hover(TXT('Rascunho', within='main'), 0.8, at=c.A(9, 'rascunho.', 0.6), label='selo Rascunho')
    c.mark(10)
    c.registra(CARTAO_OP(3), at=c.A(10, 'dica:', 0.2), label='o cartão (dica das permissões)')
    c.cursor((780, 600), at=c.A(10, 'dica:', -0.6), label='cursor sai do cartão')
    c.fim()
    return c


@capitulo
def cap06():
    """O Kanban: as três colunas, "Em produção" vira "Na prensa", a chave Coluna de conclusão, o check, o botão Coluna, arrasta a #3."""
    c = Cap(6, setup=setup_prod())
    c.mark(1)
    c.registra(SEL("main div.overflow-x-auto"), at=c.A(1, 'quadro,', 0.2), label='o quadro (Kanban)')
    c.hover(CORPO_COLUNA('A fazer'), 0.5, at=c.A(1, 'coluna', 0.6), label='uma coluna é uma etapa')
    c.hover(CARTAO_OP(3), 0.5, at=c.A(1, 'cartão', 0.6), label='um cartão')
    c.hover(CAB_COLUNA('A fazer'), 0.3, at=c.A(1, 'fazer,', 0.6), label='A fazer')
    c.hover(CAB_COLUNA('Em produção'), 0.3, at=c.A(1, 'produção', 0.6), label='Em produção')
    c.hover(CAB_COLUNA('Concluída'), 0.4, at=c.A(1, 'Concluída.', 0.6), label='Concluída')
    c.mark(2)
    c.click(CAB_COLUNA('Em produção'), at=c.A(2, 'Clicando', 0.7), label='nome da coluna Em produção (abre Editar coluna)')
    c.waitfor(text='Editar coluna', timeout=8)
    c.hover(SEL(f"{DLG} button[aria-label='Escolher cor']"), 0.4, at=c.A(2, 'cor.', 0.6), label='Cor (continua laranja)')
    c.type(SEL('#col-edit-name'), 'Na prensa', at=c.A(2, 'vira', 0.3), clear=True, cps=20, label='Nome: Na prensa')
    c.confere_campos(['Na prensa'], 'nome Na prensa')
    c.mark(3)
    c.hover(SEL(f"{DLG} button[role=switch]"), 1.4, at=c.A(3, 'chave', 0.6), label='[ZOOM] chave Coluna de conclusão (desligada)')
    c.hover(TXTX('As ordens finalizadas vão automaticamente', within=DLG), 1.0, at=c.A(3, 'finalizadas,', 0.6), label='a explicação da chave')
    c.mark(4)
    c.click(BTN('Salvar', within=DLG), at=c.A(4, 'Salvar.', 0.7), label='Salvar')
    c.waitfor(text='Coluna atualizada', timeout=8)
    c.hover(CAB_COLUNA('Na prensa'), 0.8, at=c.A(4, 'nome.', 0.6), label='a coluna Na prensa')
    c.mark(5)
    c.hover(CAB_COLUNA('Concluída'), 0.5, at=c.A(5, 'Concluída.', 0.6), label='a coluna Concluída')
    c.hover(CHECK_CONCLUSAO, 1.4, at=c.A(5, 'check', 0.6), label='[ZOOM] sinal de check da Concluída (Coluna de conclusão)')
    c.mark(6)
    c.ev(js_quadro_x(300), at=c.A(6, 'etapa?', 0.4), label='a faixa do quadro mostra o fim (botão Coluna)')
    c.hover(BTN('Coluna', within='main'), 1.2, at=c.A(6, 'botão', 0.6), label='botão Coluna (sem clicar)')
    c.mark(7)
    c.ev(js_quadro_x(-300), at=c.A(7, 'Pra', 0.3), label='a faixa do quadro volta ao começo')
    c.drag(PEGA_OP(3), CORPO_COLUNA('Na prensa'), at=c.A(7, 'arrastar', 1.0), label='arrasta a #3 para Na prensa')
    c.mark(8)
    c.registra(SEL("main div.overflow-x-auto"), at=c.A(8, 'Arrastar', 0.2), label='o quadro inteiro')
    c.hover(CAB_COLUNA('Concluída'), 1.0, at=c.A(8, 'conclusão', 0.6), label='a coluna de conclusão')
    c.fim()
    return c


# ---------------------------------------------------------------- lançamento do dia (caps 7 a 9)
LANC = "[role=dialog]:has(#entry-date)"                                   # a janela "Lançar produção do dia" (por cima da "Produção #3")
LINHA_FUNC = lambda nome: SEL(f"{LANC} div.flex.items-center:has(> span:text-is('{nome}')) input")
SUB_QTD = SEL(f"{LANC} div.w-28 input")
REAL = SEL(f"{LANC} div.w-32 input")
SUGERIDO = SEL(f"{LANC} span:has-text('Sugerido pela ficha:')")
DIFERENCA = SEL(f"{LANC} div.w-20 > span")
MOTIVO = SEL(f"{LANC} button[role=combobox]:has-text('Motivo')")
SALVAR_LANC = BTN('Salvar lançamento')
ABRE_LANCAMENTO = [
    {'do': 'click', 'target': SEL("main div.group:has(span:text-is('#3')) p.font-medium")}, {'do': 'waitFor', 'text': 'Produção #3', 'timeout': 10},
    {'do': 'click', 'target': BTN('Lançar produção do dia')}, {'do': 'waitFor', 'text': 'Produzido (por funcionário) *', 'timeout': 12},
    {'do': 'wait', 'seconds': 0.5},
]
PREENCHE_DIA = [
    {'do': 'type', 'target': LINHA_FUNC('Cláudio Ferraz'), 'text': '260', 'cps': 40},
    {'do': 'type', 'target': LINHA_FUNC('Diego Morais'), 'text': '220', 'cps': 40},
    {'do': 'click', 'target': BTN('+ Adicionar')}, {'do': 'wait', 'seconds': 0.4},
    {'do': 'click', 'target': {'role': 'combobox', 'hasText': 'Selecione o subproduto'}}, {'do': 'click', 'target': OPT('Chaparia', exact=True)},
    {'do': 'wait', 'seconds': 0.4}, {'do': 'type', 'target': SUB_QTD, 'text': '14', 'cps': 40}, {'do': 'wait', 'seconds': 0.4},
]


@capitulo
def cap07():
    """A produção do dia (17:30): o cartão #3 abre a ordem; Lançar produção do dia; Cláudio 260, Diego 220 (Total 480); Chaparia 14."""
    c = Cap(7, setup=setup_prod())
    c.mark(1)
    c.click(PEGA_OP(3), at=c.A(1, 'Clico', 0.7), label='o cartão #3 em Na prensa')
    c.waitfor(text='Produção #3', timeout=10)
    c.confere('dlg', ['Produção #3', 'Fardo de alumínio', 'Meta (referência)', '500', 'Produzido até agora', 'Nenhum dia lançado ainda.'], 'a ordem aberta')
    c.hover(TXT('Meta (referência)', within=DLG), 0.6, at=c.A(1, 'meta', 0.6), label='Meta (referência) 500 Kg')
    c.hover(TXT('Produzido até agora', within=DLG), 0.6, at=c.A(1, 'produzido.', 0.6), label='Produzido até agora 0 Kg')
    c.mark(2)
    c.click(BTN('Lançar produção do dia'), at=c.A(2, 'Lançar', 0.7), label='Lançar produção do dia')
    c.waitfor(text='Produzido (por funcionário) *', timeout=12)
    c.confere(LANC, ['Lançar produção do dia', 'Fardo de alumínio · lançamento de 10/11/2026', 'Dia da produção *'], 'janela do lançamento')
    c.hover(SEL('#entry-date'), 0.8, at=c.A(2, 'hoje.', 0.6), label='Dia da produção (hoje)')
    c.mark(3)
    c.registra(SEL(f"{LANC} div.space-y-3:has(> div > label:text-is('Produzido (por funcionário) *'))"), at=c.A(3, 'Produzido,', 0.2),
               label='[ZOOM] Produzido (por funcionário) *')
    c.click(LINHA_FUNC('Cláudio Ferraz'), at=c.A(3, 'Cláudio', 0.7), label='Cláudio Ferraz')
    c.type(LINHA_FUNC('Cláudio Ferraz'), '260', at=c.A(3, 'duzentos', 0.05), noClick=True, cps=20, label='260')
    c.click(LINHA_FUNC('Diego Morais'), at=c.A(3, 'Diego,', 0.7), label='Diego Morais')
    c.type(LINHA_FUNC('Diego Morais'), '220', at=c.A(3, 'duzentos', 0.05, nth=1), noClick=True, cps=20, label='220')
    c.confere(LANC, ['Total do dia', '480'], 'Total do dia 480 Kg')
    c.hover(TXT('Total do dia', within=LANC), 1.0, at=c.A(3, 'soma:', 0.6), label='Total do dia 480 Kg')
    c.mark(4)
    c.click(BTN('+ Adicionar'), at=c.A(4, 'subprodutos.', 0.7), label='+ Adicionar (subproduto)')
    c.click({'role': 'combobox', 'hasText': 'Selecione o subproduto'}, at=c.A(4, 'coproduto', 0.7), label='Material (Selecione o subproduto)')
    c.click(OPT('Chaparia', exact=True), at=c.A(4, 'ficha:', 0.5), label='Chaparia')
    c.click(SUB_QTD, at=c.A(4, 'catorze', 0.8), label='Qtd (Kg) do subproduto')
    c.type(SUB_QTD, '14', at=c.A(4, 'chaparia,', 0.4), noClick=True, cps=20, label='14')
    c.confere_campos(['260', '220', '14'], 'os números do dia', escopo=LANC)
    c.hover(SUB_QTD, 0.8, at=c.A(4, 'ímã.', 0.6), label='Chaparia 14 Kg')
    c.fim()
    return c


@capitulo
def cap08():
    """O real contra o teórico (17:30): matéria-prima usada, Sugerido pela ficha 480, Real 498 com +18 em vermelho."""
    c = Cap(8, setup=setup_prod(ABRE_LANCAMENTO + PREENCHE_DIA))
    c.mark(1)
    rola_ate(c, 'Matéria-prima usada', at=c.A(1, 'Embaixo', 0.2), label='desce até Matéria-prima usada', y=300, escopo=LANC)
    c.confere(LANC, ['Matéria-prima usada', 'Alumínio latinha', 'Sugerido pela ficha:', '480'], 'sugerido 480')
    c.hover(SUGERIDO, 1.0, at=c.A(1, 'sugere', 0.6), label='[ZOOM] Sugerido pela ficha: 480 Kg')
    c.hover(REAL, 1.0, at=c.A(1, 'teórico.', 0.6), label='Real (Kg) com 480: o teórico')
    c.mark(2)
    c.mark(3)
    c.click(REAL, at=c.A(3, 'Real,', 0.7), label='[ZOOM] campo Real (Kg)')
    c.type(REAL, '498', at=c.A(3, 'quatrocentos', 0.05), noClick=True, clear=True, cps=20, label='Real 498')
    c.confere(LANC, ['+18'], 'a diferença +18')
    c.hover(DIFERENCA, 1.2, at=c.A(3, 'vermelho:', 0.6), label='+18 em vermelho')
    c.mark(4)
    c.registra(DIFERENCA, at=c.A(4, 'verde:', 0.2), label='a diferença (em verde quando dá menos)')
    c.mark(5)
    c.registra(SEL(f"{LANC} div.space-y-1:has(span:has-text('Sugerido pela ficha:'))"), at=c.A(5, 'dica:', 0.2), label='a linha inteira do Alumínio latinha')
    c.hover(REAL, 0.8, at=c.A(5, 'real,', 0.6), label='quem baixa é o real')
    c.hover(SUGERIDO, 0.8, at=c.A(5, 'ficha.', 0.6), label='e não o teórico da ficha')
    c.fim()
    return c


@capitulo
def cap09():
    """Perda acima da tolerância (17:30): Motivo da perda e Salvar lançamento apagado; Material reaproveitável; salvar."""
    prep = ABRE_LANCAMENTO + PREENCHE_DIA + [
        {'do': 'eval', 'js': js_ate('Matéria-prima usada', 300, 10, LANC)},
        {'do': 'type', 'target': REAL, 'text': '498', 'clear': True, 'cps': 40}, {'do': 'wait', 'seconds': 0.5},
        {'do': 'scroll', 'point': {'x': 640, 'y': 420}, 'by': 0, 'duration': 0.2, 'after': 0},
    ]
    c = Cap(9, setup=setup_prod(prep))
    c.mark(1)
    c.confere(LANC, ['Motivo da perda *', 'Informe o motivo da diferença'], 'motivo pedido')
    c.registra(SEL(f"{LANC} div.space-y-1:has(span:has-text('Sugerido pela ficha:'))"), at=0.4, label='[ZOOM] Motivo da perda * e Informe o motivo da diferença')
    c.hover(TXT('Motivo da perda *', within=LANC), 0.8, at=c.A(1, 'Motivo', 0.6), label='Motivo da perda *')
    c.hover(SALVAR_LANC, 1.0, at=c.A(1, 'Salvar', 0.6), label='Salvar lançamento apagado', noScroll=True)
    c.hover(TXT('Informe o motivo da diferença', within=LANC), 1.0, at=c.A(1, 'motivo', 0.6, nth=1), label='Informe o motivo da diferença')
    c.mark(2)
    c.mark(3)
    c.mark(4)
    c.click(MOTIVO, at=c.A(4, 'Escolho', 0.7), label='Motivo (abre a lista)')
    c.click(OPT('Material reaproveitável'), at=c.A(4, 'Material', 0.6), label='Material reaproveitável', noScroll=True)   # a opção fica em y 739 (abaixo da faixa 96..730)
    c.confere(LANC, ['Material reaproveitável'], 'motivo escolhido')
    c.hover(SALVAR_LANC, 1.0, at=c.A(4, 'acende.', 0.6), label='Salvar lançamento aceso', noScroll=True)
    c.mark(5)
    c.registra(SALVAR_LANC, at=c.A(5, 'dica:', 0.2), label='o botão Salvar lançamento')
    c.hover(MOTIVO, 1.0, at=c.A(5, 'motivo', 0.6), label='é lá que o motivo fica esperando')
    c.mark(6)
    c.click(SALVAR_LANC, at=c.A(6, 'Salvar', 0.7), label='Salvar lançamento', noScroll=True)
    c.waitfor(text='Lançamento salvo — estoque ajustado', timeout=12)
    c.waitfor(gone={'selector': LANC}, timeout=8)
    c.confere('dlg', ['Produção #3', 'Em andamento', '480', '480 de 500', '96%', '10/11', 'Cláudio Ferraz e Diego Morais'], 'o dia na ordem')
    c.hover(TXTX('Cláudio Ferraz e Diego Morais', within=DLG), 1.0, at=c.A(6, 'dia', 0.6), label='o dia lançado na ordem')
    c.hover(TXT('Produzido até agora', within=DLG), 0.8, at=c.A(6, 'produziu.', 0.6), label='Produzido até agora 480 Kg')
    c.fim()
    return c


# ---------------------------------------------------------------- finalizar (cap 10)
FINAL = "[role=dialog]:has(h2:has-text('Finalizar'))"


@capitulo
def cap10():
    """Finalizar e fechar o custo (17:30): arrasta a #3 para Concluída, Finalizar #3, 96% da meta, resumo do lote, custo, Finalizar ordem."""
    c = Cap(10, setup=setup_prod())
    c.mark(1)
    # solta no começo da coluna (sobre o "#2"): perto da borda direita da faixa o dnd-kit rola o quadro sozinho (autoScroll, 20% da largura)
    c.drag(PEGA_OP(3), SEL("main div.group:has(span:text-is('#2')) span:text-is('#2')"), at=c.A(1, 'Arrasto', 1.2), label='arrasta a #3 para Concluída')
    c.waitfor(text='Finalizar #3', timeout=10)
    c.confere('dlg', ['Finalizar #3', 'Fardo de alumínio', 'Meta (referência)', 'Produzido de verdade', '96% da meta'], 'janela de finalizar')
    c.mark(2)
    c.registra(SEL(f"{FINAL} div.grid.grid-cols-2"), at=c.A(2, 'meta', 0.7), label='[ZOOM] Meta (referência) 500 e Produzido de verdade 480 com 96% da meta')
    c.hover(TXT('Meta (referência)', within=DLG), 0.6, at=c.A(2, 'meta', 0.6), label='Meta (referência) 500 Kg')
    c.hover(TXT('Produzido de verdade', within=DLG), 0.6, at=c.A(2, 'saíram', 0.6), label='Produzido de verdade 480 Kg')
    c.hover(TXTX('96% da meta', within=DLG), 1.0, at=c.A(2, 'noventa', 0.6), label='96% da meta')
    c.mark(3)
    c.registra(SEL(f"{FINAL} div.space-y-2:has(> h3:text-is('Resumo do lote'))"), at=c.A(3, 'resumo', 0.2), label='[ZOOM] Resumo do lote')
    c.confere('dlg', ['Resumo do lote', 'Produto principal', 'Subprodutos', '14', 'Chaparia', 'Matéria-prima usada', '498', 'Perdas', '18'], 'resumo do lote')
    c.hover(TXT('Produto principal', within=DLG), 0.4, at=c.A(3, 'fardo,', 0.6), label='Produto principal 480 Kg · Fardo de alumínio')
    c.hover(TXT('Subprodutos', within=DLG), 0.4, at=c.A(3, 'chaparia,', 0.6), label='Subprodutos 14 Kg · Chaparia')
    c.hover(TXT('Matéria-prima usada', within=DLG), 0.4, at=c.A(3, 'latinha', 0.6), label='Matéria-prima usada 498 Kg')
    c.hover(TXT('Perdas', within=DLG), 0.6, at=c.A(3, 'dezoito', 0.6), label='Perdas 18 Kg')
    c.mark(4)
    c.confere('dlg', ['Custo total do lote', 'R$ 3.087,60', 'Custo por peça', 'R$ 6,43'], 'custo do lote')
    c.registra(SEL(f"{FINAL} div.rounded-lg:has(> div > div > p:text-is('Custo total do lote'))"), at=c.A(4, 'custo', 0.2), label='[ZOOM] Custo total do lote e Custo por peça')
    c.hover(TXT('R$ 3.087,60', within=DLG), 1.0, at=c.A(4, 'três', 0.6), label='Custo total do lote R$ 3.087,60')
    c.hover(TXT('R$ 6,43', within=DLG), 1.0, at=c.A(4, 'seis', 0.6), label='Custo por peça R$ 6,43')
    c.mark(5)
    c.mark(6)
    c.click(BTN('Finalizar ordem'), at=c.A(6, 'Finalizar', 0.7), label='Finalizar ordem', noScroll=True)
    c.waitfor(text='Ordem finalizada — custo/peça R$ 6,43', timeout=12)
    c.waitfor(gone={'selector': FINAL}, timeout=8)
    c.confere('main', ['#3', 'Concluída', 'R$ 3.087,60', 'R$ 6,43/peça', 'Produziu:', '2 funcionários'], 'o cartão #3 concluído')
    c.hover(CARTAO_OP(3), 1.2, at=c.A(6, 'custo', 0.6), label='o cartão #3 na Concluída com o custo')
    c.mark(7)
    c.registra(CARTAO_OP(3), at=c.A(7, 'finalizada', 0.2), label='o cartão (fica na coluna de conclusão)')
    c.cursor((640, 600), at=c.A(7, 'desfazer,', 0.3), label='cursor sai do cartão')
    c.fim()
    return c


# ---------------------------------------------------------------- relatório (cap 11)
KPI = lambda titulo: SEL(f"main div.rounded-xl:has(p:text-is('{titulo}')), main div[class*=shadow-lg]:has(p:text-is('{titulo}'))")
FAIXA_KPI = SEL("main div.grid:has(> div p:text-is('Ordens concluídas'))")
LINHA_TABELA = lambda nome: SEL(f"main table tr:has-text('{nome}')")
ABA_DETALHE = lambda nome: SEL(f"main div.border-b > button:text-is('{nome}')")


@capitulo
def cap11():
    """Relatório de Produção (17:30): filtros, PRODUTO = Fardo de alumínio, os quatro cartões, a tabela Por produto, Por funcionário e a meta."""
    c = Cap(11, setup=setup_prod())
    c.mark(1)
    c.click(ABA('report'), at=c.A(1, 'relatório.', 0.7), label='aba Relatório')
    c.waitfor(text='Relatório de produção', timeout=12)
    c.hover(TXT('PERÍODO', within='main'), 0.3, at=c.A(1, 'período,', 0.6), label='PERÍODO (Este mês)')
    c.hover(TXT('PRODUTO', within='main'), 0.3, at=c.A(1, 'produto', 0.6), label='PRODUTO')
    c.hover(TXT('FUNCIONÁRIO', within='main'), 0.3, at=c.A(1, 'funcionário.', 0.6), label='FUNCIONÁRIO')
    c.click(SEL('#prod-report-product'), at=c.A(1, 'Escolho', 0.7), label='PRODUTO (abre a lista)')
    c.click(OPT('Fardo de alumínio'), at=c.A(1, 'Fardo', 0.6), label='Fardo de alumínio')
    c.confere('main', ['Este mês', 'Fardo de alumínio', 'Ordens concluídas', 'R$ 3.087,60', '+3,8%', '96,4%'], 'filtro e cartões do fardo')
    c.mark(2)
    c.registra(FAIXA_KPI, at=c.A(2, 'cartões', 0.2), label='[ZOOM] os quatro cartões')
    c.hover(TXT('Ordens concluídas', within='main'), 0.3, at=c.A(2, 'ordens', 0.6), label='Ordens concluídas 1')
    c.hover(TXT('Custo de matéria-prima', within='main'), 0.3, at=c.A(2, 'custo', 0.6), label='Custo de matéria-prima R$ 3.087,60')
    c.hover(TXT('Perda média', within='main'), 0.3, at=c.A(2, 'perda', 0.6), label='Perda média +3,8%')
    c.hover(TXT('Rendimento médio', within='main'), 0.6, at=c.A(2, 'rendimento', 0.6), label='Rendimento médio 96,4%')
    c.mark(3)
    c.mark(4)
    c.mark(5)
    rola_ate(c, 'Teórico (kg)', at=c.A(5, 'aba', 0.4), label='desce à tabela Por produto', y=420)
    c.confere('main table', ['Fardo de alumínio', '480', '498', '+3,8%', '96,4%', 'R$ 3.087,60', 'R$ 6,43'], 'linha do fardo')
    c.registra(LINHA_TABELA('Fardo de alumínio'), at=c.A(5, 'tabela', 0.2), label='[ZOOM] a linha Fardo de alumínio da tabela')
    c.hover(TXT('Teórico (kg)', within='main'), 0.3, at=c.A(5, 'teórico,', 0.6), label='Teórico (kg) 480')
    c.hover(TXT('Real (kg)', within='main'), 0.3, at=c.A(5, 'real', 0.6), label='Real (kg) 498')
    c.hover(TXT('Custo/peça', within='main'), 0.8, at=c.A(5, 'custo', 0.6), label='Custo/peça R$ 6,43 (por quilo)')
    c.mark(6)
    c.click(ABA_DETALHE('Por funcionário'), at=c.A(6, 'Por', 0.7), label='Por funcionário')
    c.waitfor(text='Ranking de funcionários', timeout=10)
    c.hover(TXT('Ranking de funcionários', within='main'), 0.6, at=c.A(6, 'ranking', 0.6), label='Ranking de funcionários')
    rola_ate(c, 'Produção do dia', at=c.A(6, 'produção', 0.5), label='desce à Produção do dia', y=300)
    c.confere('main', ['Meta: 250/dia por funcionário.', 'Cláudio Ferraz', '260', 'bateu', 'Diego Morais', '220', 'faltam 30'], 'meta do dia')
    c.hover(TXTX('/dia por funcionário.', within='main'), 0.8, at=c.A(6, 'meta,', 0.6), label='Meta: 250/dia por funcionário')
    c.hover(TXT('bateu', within='main'), 0.8, at=c.A(6, 'bateu,', 0.6), label='Cláudio 260: bateu')
    c.hover(TXT('faltam 30', within='main'), 1.0, at=c.A(6, 'faltaram', 0.6), label='Diego 220: faltam 30')
    c.mark(7)
    c.ev(js_topo(), at=c.A(7, 'E', 0.4), label='sobe ao começo do relatório')
    c.hover(BTN('Exportar', within='main'), 1.2, at=c.A(7, 'Exportar', 0.6), label='botão Exportar (sem clicar)')
    c.fim()
    return c


# ---------------------------------------------------------------- configurações (cap 12)
CFG = lambda titulo: SEL(f"main div.rounded-lg:has(p:text-is('{titulo}'))")
CFG_CHAVE = lambda titulo: SEL(f"main div.rounded-lg:has(p:text-is('{titulo}')) button[role=switch]")
BLOQUEIO = 'Bloquear finalização quando faltar matéria-prima em estoque'


@capitulo
def cap12():
    """Os ajustes da Produção (17:30): multinível, Quando dar baixa no estoque, liga o bloqueio, tolerância 2 e meta 250."""
    c = Cap(12, setup=setup_prod())
    c.mark(1)
    c.click(ABA('settings'), at=c.A(1, 'configurações', 0.7), label='aba Configurações')
    c.waitfor(text='Custo de produção em cadeia (multinível)', timeout=10)
    c.mark(2)
    c.registra(CFG('Custo de produção em cadeia (multinível)'), at=c.A(2, 'custo', 0.2), label='[ZOOM] Custo de produção em cadeia (multinível), desligado')
    c.hover(TXT('Custo de produção em cadeia (multinível)', within='main'), 1.0, at=c.A(2, 'multinível,', 0.6), label='multinível')
    c.hover(CFG_CHAVE('Custo de produção em cadeia (multinível)'), 1.0, at=c.A(2, 'Ligado,', 0.6), label='a chave do multinível (desligada)')
    c.mark(3)
    rola_ate(c, 'Quando dar baixa no estoque', at=c.A(3, 'Quando', 0.5), label='desce até Quando dar baixa no estoque', y=200)
    c.confere('main', ['Quando dar baixa no estoque', 'Agora: baixa a cada lançamento do dia.'], 'baixa a cada lançamento')
    c.hover(TXT('Agora: baixa a cada lançamento do dia.', within='main'), 1.4, at=c.A(3, 'padrão:', 0.6), label='Agora: baixa a cada lançamento do dia.')
    c.mark(4)
    c.mark(5)
    c.hover(TXT(BLOQUEIO, within='main'), 0.8, at=c.A(5, 'Bloquear', 0.6), label='Bloquear finalização quando faltar matéria-prima em estoque')
    c.click(CFG_CHAVE(BLOQUEIO), at=c.A(5, 'liga.', 0.7), label='liga o bloqueio')
    c.waitfor(text='Passou a bloquear finalização sem estoque', timeout=8)
    c.mark(6)
    rola_ate(c, 'Tolerância de perda (%)', at=c.A(6, 'tolerância', 0.5), label='desce até a tolerância e a meta', y=330)
    c.confere_campos(['2', '250'], 'tolerância 2 e meta 250', escopo='main')
    c.registra(SEL("main div.rounded-lg:has(#prod-tolerance)"), at=c.A(6, 'tolerância', -0.6), label='[ZOOM 1/2] cartão Tolerância de perda (%) (o zoom pega os dois cartões, nesta frase e na seguinte)')
    c.registra(SEL("main div.rounded-lg:has(#prod-daily-goal)"), label='[ZOOM 2/2] cartão Meta de produção por dia')
    c.hover(SEL('#prod-tolerance'), 1.2, at=c.A(6, 'dois', 0.6), label='Tolerância de perda 2')
    c.hover(TXTX('0 = sempre pedir.', within='main'), 1.0, at=c.A(6, 'zero,', 0.6), label='0 = sempre pedir')
    c.mark(7)
    c.hover(SEL('#prod-daily-goal'), 1.4, at=c.A(7, 'duzentos', 0.6), label='Meta de produção por dia 250')
    c.fim()
    return c


# ---------------------------------------------------------------- excluir e Kardex (cap 13)
LIXEIRA_OP = lambda n: SEL(f"main div.group:has(span:text-is('#{n}')) button[aria-label='Excluir ordem']")
ALERTA = '[role=alertdialog]'


@capitulo
def cap13():
    """Excluir uma ordem concluída (17:30): #1 e #2 do Cobre mel, lixeira da #2, Excluir ordem, Kardex do fio com o estorno."""
    c = Cap(13, setup=setup_prod(aquece=['/historico-materiais']))
    c.mark(1)
    c.confere('main', ['#3', '#2', '#1', 'Cobre mel', 'R$ 1.440,00', 'R$ 28,80/peça', '03/11/2026'], 'as ordens 1 e 2 do Cobre mel')
    c.registra(SEL("main div.rounded-xl:has(span:text-is('#2'))"), at=c.A(1, 'Repara', 0.2), label='[ZOOM] os cartões #2 e #1 do Cobre mel')
    c.hover(CARTAO_OP(1), 0.5, at=c.A(1, 'um', 0.6, nth=1), label='a ordem #1')
    c.hover(PEGA_OP(2), 0.8, at=c.A(1, 'dois', 0.6), label='a ordem #2')
    c.mark(2)
    c.hover(PEGA_OP(2), 0.6, at=c.A(2, 'excluir.', 0.6), label='o mouse no cartão #2 (aparece a lixeira)')
    c.click(LIXEIRA_OP(2), at=c.A(2, 'lixeira', 0.6), label='lixeira Excluir ordem da #2')
    c.waitfor(text='Excluir ordem de produção?', timeout=8)
    c.confere(ALERTA, ['Excluir ordem de produção?', 'Atenção: esta produção já foi finalizada. Ao excluir, o estoque será estornado'], 'confirmação com o estorno')
    c.hover(TXTX('Ao excluir, o estoque será estornado', within=ALERTA), 1.6, at=c.A(2, 'estornado.', 0.6), label='[ZOOM] o texto da confirmação')
    c.mark(3)
    c.click(BTN('Excluir ordem', within=ALERTA), at=c.A(3, 'Excluir', 0.7), label='Excluir ordem')
    c.waitfor(text='Ordem excluída', timeout=10)
    c.waitfor(gone={'selector': ALERTA}, timeout=8)
    c.confere('main', ['#3', '#1'], 'a #2 saiu do quadro')
    c.mark(4)
    c.hover(BTN('Materiais', within=MENU), 0.5, at=c.A(3, 'saíram.', 0.6), label='menu Materiais (o menu recolhido abre)')
    c.click({'role': 'link', 'name': 'Histórico (Kardex)', 'exact': True, 'within': MENU}, at=c.A(4, 'histórico', 0.7), label='menu Histórico (Kardex)')
    c.waitfor(text='Buscar código ou material', timeout=12)
    c.cursor((700, 450), at=None, label='cursor sai do menu (ele recolhe)')
    c.click(PH('Buscar código ou material'), at=c.A(4, 'material,', 0.7), label='Buscar código ou material')
    c.type(PH('Buscar código ou material'), 'fio', at=c.A(4, 'Kardex,', 0.05), noClick=True, cps=20, label='digita fio')
    c.click(SEL("main [role=list] button:has-text('Fio de cobre encapado')"), at=c.A(4, 'tudo.', 0.6), label='Fio de cobre encapado')
    c.waitfor(text='Fio de cobre encapado', timeout=10)
    c.confere('main', ['KARDEX', 'Fio de cobre encapado', 'Produção'], 'Kardex do fio')
    c.hover(SEL("main tbody tr:has-text('Estorno')"), 1.0, at=c.A(4, 'estorno', 0.6), label='a linha do estorno (+80 Kg)')
    c.mark(5)
    c.mark(6)
    c.hover(SEL("main tbody tr td :text-is('Produção')"), 1.6, at=c.A(6, 'Produção.', 0.6), label='[ZOOM] o selo Produção')
    c.fim()
    return c


@capitulo
def cap14():
    """Recapitulando (17:30): o quadro no estado final (a edição monta os cortes dos capítulos por cima); o cartão Próximo no fim."""
    c = Cap(14, setup=setup_prod())
    c.mark(1)
    c.registra(SEL("main div.overflow-x-auto"), at=0.4, label='o quadro no estado final (base da montagem)')
    c.mark(2)
    c.hover(PEGA_OP(3), 1.0, at=c.A(2, 'ordem', 0.6), label='a ordem #3 (500 kg)')
    c.hover(CAB_COLUNA('Na prensa'), 0.8, at=c.A(2, 'coluna', 0.6), label='a coluna Na prensa')
    c.mark(3)
    c.mark(4)
    c.hover(TXT('R$ 6,43/peça', exact=False, within='main'), 1.0, at=c.A(4, 'custo', 0.6), label='o custo de cada quilo no cartão')
    c.hover(CAB_COLUNA('Concluída'), 0.8, at=c.A(4, 'excluiu', 0.6), label='a Concluída sem a ordem lançada em dobro')
    c.cursor((780, 600), at=c.A(4, 'estorno', 0.2), label='cursor descansa')
    c.mark(5)
    c.fim()
    return c


# @@CAPITULOS@@


def main():
    quais = [int(a) for a in sys.argv[1:] if not a.startswith('-')] or sorted(CAPS_ROBO)
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
        marcas = [s['name'] for s in d['steps'] if s.get('do') == 'mark']
        faltam = [f'L{i}' for i in range(1, len(c.linhas) + 1) if f'L{i}' not in marcas]
        if faltam:
            print(f'  aviso cap{n:02d}: sem marca {",".join(faltam)}')
        path = os.path.join(HERE, f'cap{n:02d}.json')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
        print(f'cap{n:02d}: {len(d["steps"])} passos, narração {c.dur:.1f} s{" (voz ESTIMADA)" if c.estimada else ""} -> {os.path.relpath(path, HERE)}')


if __name__ == '__main__':
    main()
