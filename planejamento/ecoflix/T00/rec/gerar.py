#!/usr/bin/env python3
"""T0 · gera rec/t00/capNN.json (computador, 1280x800) e rec/t00/capNN.9x16.json (celular 390x844, `device: phone`) de cap00 a cap15,
a partir da voz ($TUT_HOME/t00/narracao/capNN.json, estimada ou da voz de verdade), logado como Rafael Nogueira (MASTER, Recicla Vale
Metais Ltda), no EcoSistema 1.60.18 (18/11: capítulos novos 8, o Cato, e 12, Montar o plano; os antigos 8..13 viraram 9, 10, 11, 13, 14, 15).

DUAS VERSÕES (planejamento/ecoflix/T00/plano.md, "Vertical"): mesmo áudio, mesma linha do tempo, os mesmos `label`. No 9:16 cada tela real é
gravada de novo no celular (390x844, toque), nunca o computador reduzido. O cap07 linha 6 usa a gravação do celular também no 16:9 (a edição
recorta a L6 do cap07.9x16: é a mesma linha do tempo e o mesmo gesto).
VARIANTES (mesma linha do tempo, outro estado; a edição usa só a linha indicada): cap40 = cap10 com a conta em teste (linha 2, "Ative sua
Assinatura"); cap41 = cap11 no S3, sem o CRM (linha 3, "Adicione ao seu plano").
O login roda no `setup` (não filmado), com "$TUT_USER"/"$TUT_SENHA" do ambiente; o capítulo abre o navegador sem sessão ("anonymous").

Estados de partida (rec/mundo/seeds-extra/t00/, gerados por rec/t00/t00_catalogo.mjs):
  S1    cap 1     empresa em teste, sem confirmação da introdução, T0 sem progresso: o portão abre sozinho sobre o Dashboard
  S2    caps 0,2,4..14  conta ativa (mensalidade 1.350,00, 3 usuários), T0 concluído e confirmado (sem portão), menu lateral
  S3    cap 3 e 41  S2 sem crm_kanban em company_modules (o selo "Não tem no seu plano"; "Adicione ao seu plano")
  TESTE cap 40    S2 com a empresa em teste (a tela Assinatura só com "Ative sua Assinatura"), sem portão
  S13   cap 15    S1 com o vídeo do T0 já visto: a caixa liga e o botão vira "Confirmar e começar a primeira aula"
Backend simulado: get_ecoflix_learning_status (lib/ecoflix_status.mjs), acknowledge_ecoflix_intro, save_ecoflix_progress,
count_fiscal_documents_in_month, fiscal_onboarding_status, track_cato_adoption_event e as tabelas ecoflix_* (legenda e material do T1 na
semente do catálogo); o player toca um vídeo fictício local, mudo (ext handler do "Drive").
Balão de dica do Cato: calado no `localStorage` em todos os capítulos, menos no cap08 (o `setup` recarrega o Dashboard e espera
BALAO_ESPERA para o balão subir na frase dele).

Abertos SEM confirmar (1.60.18, Kaik 18/11): "Gerenciar plano" (Montar plano; nunca "Ver valor e aplicar"), "Cancelar assinatura" (até
"Confirmar cancelamento"; nunca "Confirmar Cancelamento"), "Falar com o Suporte" (nunca "Falar no WhatsApp"), o aviso do Cato (nunca o aceite).
Nunca clicados (saem do app ou cobram): "Tirar dúvidas com o suporte", "Pagar Agora", "Adicionar ao meu plano", "Ativar meu CRM",
"Pular por agora" (só hover), "Baixar PDF", "Baixar XML", "Sair", "Falar com o Sucesso do Cliente".
Rodar de qualquer pasta: `python3 -I rec/t00/gerar.py [NN ...] [--so-d|--so-p] [--ens]` (--ens também escreve rec/t00/_ens/, o ensaio rápido).
Depois: `node rec/record.mjs rec/t00/capNN.json --check`.
"""
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TUT_HOME = os.path.normpath(os.path.join(HERE, '..', '..'))
NARR = os.path.join(TUT_HOME, 't00', 'narracao')

RAFAEL = '34c36c63-0890-5e89-8963-7c77b7996908'      # stableId('user.rafael') do mundo
EMPRESA = '38814e47-876a-5977-a5f7-53af364c17bb'     # stableId('company.reciclavale')
AGORA_MS = 1794310200000                             # FAKE_NOW em ms (2026-11-10T08:30:00-03:00)
try:
    VERSAO = open(os.path.join(TUT_HOME, 'app', 'dist', '.versao-app'), encoding='utf8').read().strip() or '1.60.18'
except OSError:
    VERSAO = '1.60.18'
FAKE_NOW = '2026-11-10T08:30:00-03:00'
HOJE = FAKE_NOW[:10]

NOMES = ['Abertura', 'Os combinados', 'Como funciona a trilha', 'Aulas de outros módulos', 'Assistir e tirar dúvidas', 'Do portão até a conta',
         'Um passeio pelo menu', 'Os menus e a sua conta', 'O Cato, o seu agente', 'As palavras do pátio', 'A sua assinatura', 'Módulos e permissões',
         'Montar o plano', 'Mudança de plano e usuários', 'Formas de pagamento', 'Recapitulando']
CAT = ['t00/catalogo']
S1 = CAT + ['t00/s1']
S2 = CAT + ['t00/s2', 't00/pagamentos']
S3 = S2 + ['t00/s3']
S13 = CAT + ['t00/s1', 't00/s13']
SEMENTE = {0: S2, 1: S1, 2: S2, 3: S3, 4: S2, 5: S2, 6: S2, 7: S2, 8: S2, 9: S2, 10: S2, 11: S2, 12: S2, 13: S2, 14: S2, 15: S13}
SIZE = {'d': (1280, 800), 'p': (390, 844)}


# ---------------------------------------------------------------- voz
def norm(s):
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode().lower()
    return ''.join(ch for ch in s if ch.isalnum() or ch in '?')


def carregar_voz(n):
    real = json.load(open(os.path.join(NARR, f'cap{n:02d}.json'), encoding='utf8'))
    return real['words'], real['linhas'], float(real['dur']), bool(real.get('estimado'))


# ---------------------------------------------------------------- observador de avisos de erro na tela (aceite)
OBS = ("(()=>{window.__avisos=[];const re=/N[ãa]o foi poss[ií]vel|Erro ao|Tente novamente|indispon[ií]vel|Algo deu errado|Falha ao|"
       "Something went wrong|N[ãa]o conseguimos/i;const chk=(t)=>{t=(t||'').trim();const m=t&&t.match(new RegExp('[^]{0,40}('+re.source+')[^]{0,40}','i'));"
       "if(m&&window.__avisos.length<10)window.__avisos.push(m[0].replace(/[\\n\\r\\t ]+/g,' '))};new MutationObserver(ms=>{for(const m of ms){"
       "m.addedNodes.forEach(n=>chk(n.textContent));if(m.type==='characterData')chk(m.target.textContent)}}).observe(document.body,"
       "{childList:true,subtree:true,characterData:true});chk(document.body.innerText);return 1})()")


class Cap:
    def __init__(s, n, v='d', pace=0.5, cps=22, start=None, setup=None, prewarm=None, login_espera='Olá, Rafael', arq=None, semente=None, balao=False):
        s.n, s.v = n, v
        s.arq = n if arq is None else arq      # número do ARQUIVO (variantes: 40, 41); s.n = capítulo da voz
        s.semente, s.balao = semente, balao
        s.words, s.linhas, s.dur, s.estimada = carregar_voz(n)
        s.steps = []
        s.pace, s.cps = pace, cps
        s.start = start or ((760, 470) if v == 'd' else (195, 600))
        s.prewarm = prewarm or ['/login']
        s.setup = login(login_espera) + list(setup or []) + [{'do': 'eval', 'js': OBS}]
        s.anchors, s.ambiguas, s.pending = [], [], []

    # ---- tempo
    def L(s, i):
        return round(s.linhas[i - 1]['s'], 2)

    def Lfim(s, i):
        return round(s.linhas[i - 1]['e'], 2)

    def _hits(s, i, palavra):
        q = norm(palavra)
        return [w for w in s.words if w['linha'] == i - 1 and norm(w['w']).startswith(q)]

    def W(s, i, palavra, nth=0):
        hits = s._hits(i, palavra)
        if len(hits) > 1 and nth == 0:
            s.ambiguas.append((i, palavra, len(hits)))
        if len(hits) <= nth:
            raise SystemExit(f'cap{s.n:02d}{s.v}: palavra "{palavra}" (#{nth}) não achada na linha {i}: ' + ' '.join(w['w'] for w in s.words if w['linha'] == i - 1))
        return hits[nth]['s']

    def A(s, i, palavra, folga=0.8, nth=0):
        t = round(max(0.0, s.W(i, palavra, nth) - folga), 2)
        s.anchors.append((i, palavra, t))
        return t

    def E(s, i, palavra, folga=0.0, nth=0):
        """fim da palavra (para um gesto que fecha a frase)"""
        hits = s._hits(i, palavra)
        if len(hits) <= nth:
            raise SystemExit(f'cap{s.n:02d}{s.v}: palavra "{palavra}" (#{nth}) não achada na linha {i}')
        return round(max(0.0, hits[nth]['e'] - folga), 2)

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
        if t <= 0 or i == 1:
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

    def hover(s, target, seconds=0.6, at=None, label=None, **kw):
        kw.setdefault('optional', True)
        kw.setdefault('timeout', 4)
        if at is not None:
            fim = at + 0.55 + seconds
            for mt, mi in sorted(s.pending):
                if at + 0.3 < mt < fim - 0.25:
                    s1 = max(0.1, round(mt - at - 0.55, 2))
                    s2 = max(0.2, round(fim - mt - 0.2, 2))
                    s._p({'do': 'hover', 'target': target, 'seconds': s1}, at, label, dict(kw))
                    return s._p({'do': 'hover', 'target': target, 'seconds': s2}, mt, (label + ' (continua)') if label else None, dict(kw))
        return s._p({'do': 'hover', 'target': target, 'seconds': seconds}, at, label, kw)

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

    def marcar(s, target, at=None, label=None, **kw):
        """registra o retângulo do alvo para a edição (zoom/destaque) SEM mexer o mouse"""
        kw.setdefault('optional', True)
        kw.setdefault('timeout', 4)
        return s._p({'do': 'type', 'target': target, 'text': '', 'noClick': True}, at, label, kw)

    def cursor(s, ponto, at=None, label=None):
        return s._p({'do': 'scroll', 'point': {'x': ponto[0], 'y': ponto[1]}, 'by': 0, 'duration': 0.2, 'after': 0}, at, label or 'cursor a um ponto neutro', {})

    def toque(s, target, at=None, label=None, **kw):
        """clique em alvo FIXO no celular (barra de baixo, y > altura - 70): clique de verdade, com anel e telemetria, sem rolar"""
        kw.setdefault('noScroll', True)
        return s.click(target, at=at, label=label, **kw)

    def confere(s, escopo, esperados, label, tentativas=22):
        sel = {'dlg': '[role=dialog]', 'main': 'main', 'body': 'body'}.get(escopo, escopo)
        esp = [esperados] if isinstance(esperados, str) else list(esperados)
        js = ("(async()=>{const norm=t=>t.replace(/[\\s\\u00a0]+/g,' ').toLowerCase();const esp=%s;let out='';"
              "for(let i=0;i<%d;i++){const els=[...document.querySelectorAll(%s)];const el=els[els.length-1];"
              "if(!el){out='DIFERENTE: sem elemento';}else{const t=norm(el.innerText);const falta=esp.filter(e=>!t.includes(norm(e)));"
              "if(!falta.length)return 'OK: '+esp.join(' | ');out='DIFERENTE: faltou '+JSON.stringify(falta)+' em: '+t.slice(0,260);}"
              "await new Promise(r=>setTimeout(r,300));}return out})()") % (json.dumps(esp, ensure_ascii=False), tentativas, json.dumps(sel))
        return s.add({'do': 'eval', 'js': js, 'label': 'confere ' + label})

    def fim(s):
        s.flush(1e9)
        s.apara_hovers()
        s.steps.append({'do': 'eval', 'js': 'JSON.stringify(window.__avisos || "sem observador")', 'label': 'avisos de erro na tela'})
        s.steps.append({'do': 'mark', 'name': 'FIM', 'at': round(s.dur, 2)})

    def apara_hovers(s, chegada=0.95):
        for k, st in enumerate(s.steps):
            if st.get('do') != 'hover' or st.get('at') is None:
                continue
            prox = next((x['at'] for x in s.steps[k + 1:] if x.get('at') is not None), None)
            if prox is None:
                continue
            cabe = round(prox - 0.05 - st['at'] - chegada, 2)
            if st.get('seconds', 0.6) > cabe:
                st['seconds'] = max(0.1, cabe)

    def out(s):
        est = 'ESTIMADA' if s.estimada else 'da voz'
        sufixo = '' if s.v == 'd' else 'b'
        d = {
            'name': f't00-cap{s.arq:02d}{sufixo}',
            'title': f'T0 · Cap. {s.n}{" (VARIANTE " + str(s.arq) + ")" if s.arq != s.n else ""} · {NOMES[s.n]} ({"computador 1280x800" if s.v == "d" else "celular 390x844, 9:16"}; narração {str(round(s.dur, 1)).replace(".", ",")} s, {est}; '
                     f'marcas L1..L{len(s.linhas)} = início de cada linha do roteiro; FAKE_NOW {FAKE_NOW})',
            'fakeNow': FAKE_NOW,
            'seed': f't00-cap{s.arq:02d}{sufixo}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
            'start': {'x': s.start[0], 'y': s.start[1]},
            'anonymous': True,
            'storage': storage(s.balao),
            'seedExtra': list(s.semente or SEMENTE[s.n]),
            'prewarm': s.prewarm, 'setup': s.setup, 'steps': s.steps,
        }
        if s.v == 'p':
            d['device'] = 'phone'
        return d


def storage(balao=False):
    """o que a primeira entrada do Rafael mostraria por cima da tela, já visto (o robô entra sem sessão: modo "anonymous").
    1.60: o balão de dica do Cato sobe sozinho 15 s depois de qualquer tela abrir; fica calado (contador no máximo, CatoFab.tsx:249-258) em
    todos os capítulos menos o do Cato (`balao=True`)."""
    # __mostrarCato: o gravador cala o balão no login pela tela (browser.mjs, calaCatoNaLeitura); aqui ele tem de aparecer
    cala = {'__mostrarCato': '1'} if balao else {f'cato_adoption_nudge_{EMPRESA}_{RAFAEL}': json.dumps({'count': 16, 'lastShownAt': AGORA_MS})}
    return {
        **cala,
        'app_version': VERSAO, 'notification_shown_version': VERSAO, 'pwa-install-dismissed': 'true', 'theme': 'light',
        f'daily-tasks-reminder-last-shown-{RAFAEL}': HOJE, 'initial-preferences-set': 'true',
        f'dominex:daily-tasks-shown:{RAFAEL}': HOJE,
    }


# ---------------------------------------------------------------- alvos
BTN = lambda n, **kw: {'role': 'button', 'name': n, 'exact': True, **kw}
BTNX = lambda n, **kw: {'role': 'button', 'name': n, **kw}
LINK = lambda n, **kw: {'role': 'link', 'name': n, 'exact': True, **kw}
TAB = lambda n, **kw: {'role': 'tab', 'name': n, **kw}
TXT = lambda t, **kw: {'text': t, 'exact': True, **kw}
TXTX = lambda t, **kw: {'text': t, **kw}
SEL = lambda s, **kw: {'selector': s, **kw}
ITEM = lambda n, **kw: {'role': 'menuitem', 'name': n, **kw}
DLG = '[role=dialog]'
PORTAO = '[role=dialog][aria-label^="Introdução"]'
MENU_CONTA = {'role': 'button', 'name': 'Menu da conta', 'exact': True}
EM_MAIN = lambda t, **kw: {'text': t, 'within': 'main', **kw}

# ---------------------------------------------------------------- trechos comuns (não filmados, no `setup`)
AGUARDA = {'do': 'waitFor', 'idle': True, 'timeout': 15}


def login(espera='Olá, Rafael'):
    return [
        {'do': 'goto', 'url': '/login'},
        {'do': 'waitFor', 'target': {'placeholder': 'seu@email.com'}, 'timeout': 40},
        {'do': 'type', 'target': {'placeholder': 'seu@email.com'}, 'text': '$TUT_USER', 'cps': 40},
        {'do': 'type', 'target': {'placeholder': '••••••••'}, 'text': '$TUT_SENHA', 'cps': 40},
        {'do': 'click', 'target': {'role': 'button', 'name': 'Entrar', 'exact': True}},
        {'do': 'waitFor', 'text': espera, 'timeout': 45},
        {'do': 'waitFor', 'idle': True, 'timeout': 20},
    ]


def vai(url, espera):
    return [{'do': 'goto', 'url': url}, {'do': 'waitFor', 'text': espera, 'timeout': 30}, AGUARDA]


TRILHA = vai('/ecoflix', 'Aprenda a usar o EcoSistema')
def assinatura(v):
    return vai('/assinatura', 'Gerencie seu plano, módulos e pagamentos' if v == 'd' else 'Uso da conta')

FECHAR_EVAL = (r"""(() => { const ds = [...document.querySelectorAll('[role=dialog]')]; const d = ds[ds.length - 1]; if (!d) return 'ja fechada'; """
               r"""const b = [...d.querySelectorAll('button')].find((x) => [x.textContent, x.getAttribute('aria-label')].some((v) => /^\s*fechar\s*$/i.test(v || ''))); """
               r"""if (!b) return 'sem botao Fechar'; b.click(); return 'fechada pelo botao'; })()""")

# rolagem suave do contêiner que rola (o ancestral com overflow-y, ou o documento) até o texto ficar em y px CSS da janela. Devolve o topo
# final do alvo, 'ok' (já estava lá), 'SEM ALVO' ou 'SEM ROLAGEM'. `dentro` limita a busca a um seletor (ex.: a gaveta, a janela).
_ACHA = ("const vis=e=>e.getClientRects().length>0&&getComputedStyle(e).visibility!=='hidden';const nz=t=>t.replace(/[\\s\\u00a0]+/g,' ').trim();"
         "const rolagem=(el)=>{let c=el.parentElement;while(c&&c!==document.body&&c!==document.documentElement){const s=getComputedStyle(c);"
         "if(/(auto|scroll)/.test(s.overflowY)&&c.scrollHeight>c.clientHeight+4)return c;c=c.parentElement;}return document.scrollingElement};")
_SUAVE = ("await new Promise(res=>{const f=t=>{const p=Math.min(1,(t-t0)/DUR),e=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;c.scrollTop=y0+dy*e;"
          "p<1?requestAnimationFrame(f):res()};requestAnimationFrame(f)});")


def js_rola_ate(texto, y=250, dur_ms=1000, prefixo=False, dentro='body', so_se_fora=False):
    alvo = json.dumps(texto)
    busca = (f"[...root.querySelectorAll('*')].filter(e=>vis(e)&&nz(e.textContent).startsWith({alvo})).sort((a,b)=>a.textContent.length-b.textContent.length)[0]"
             if prefixo else
             f"[...root.querySelectorAll('*')].filter(e=>vis(e)&&nz(e.textContent)==={alvo}&&![...e.children].some(k=>nz(k.textContent)==={alvo}))[0]")
    fora = ("const r0=el.getBoundingClientRect();const cr=c.getBoundingClientRect?c.getBoundingClientRect():{top:0,bottom:innerHeight};"
            "const top0=c===document.scrollingElement?0:cr.top,bot0=c===document.scrollingElement?innerHeight:cr.bottom;"
            "if(r0.top>=top0+8&&r0.bottom<=bot0-8)return 'ok';") if so_se_fora else ''
    return ("(async()=>{" + _ACHA + f"const root=document.querySelector({json.dumps(dentro)})||document.body;const el={busca};if(!el)return 'SEM ALVO';"
            "const c=rolagem(el);if(!c)return 'SEM ROLAGEM';" + fora +
            f"const dy=Math.round(el.getBoundingClientRect().top-{int(y)});if(Math.abs(dy)<3)return 'ok';const y0=c.scrollTop,t0=performance.now();"
            + _SUAVE.replace('DUR', str(int(dur_ms))) + "return Math.round(el.getBoundingClientRect().top)})()")


def rola_ate(c, texto, at, label, y=250, dur_ms=1000, prefixo=False, dentro='body', so_se_fora=False):
    return c.ev(js_rola_ate(texto, y, dur_ms, prefixo, dentro, so_se_fora), at=at, label=label)


def js_rola_topo(dur_ms=700, dentro='body'):
    return ("(async()=>{" + _ACHA + f"const root=document.querySelector({json.dumps(dentro)})||document.body;"
            "const pri=[...root.querySelectorAll('*')].filter(vis)[0];const c=rolagem(pri);const y0=c.scrollTop,t0=performance.now();const dy=-y0;if(y0<3)return 'ok';"
            + _SUAVE.replace('DUR', str(int(dur_ms))) + "return 'topo:'+Math.round(c.scrollTop)})()")


def rola_topo(c, at, label, dur_ms=700, dentro='body'):
    return c.ev(js_rola_topo(dur_ms, dentro), at=at, label=label)


def cap_novo(n, v, **kw):
    return Cap(n, v, **kw)


def so_ilustracao(n, v):
    """capítulo que é só ilustração na edição: a gravação fica no Dashboard, parada (a edição cobre a tela)"""
    c = cap_novo(n, v, setup=vai('/dashboard', 'Olá, Rafael!'), prewarm=['/login', '/dashboard'])
    for i in range(1, len(c.linhas) + 1):
        c.mark(i)
    c.fim()
    return c


# ================================================================ cap00 / cap05: só ilustração
def cap00(v):
    return so_ilustracao(0, v)


def cap05(v):
    return so_ilustracao(5, v)


# ================================================================ cap01 · Os combinados (S1: o portão)
def cap01(v):
    c = cap_novo(1, v, login_espera='Antes de usar o sistema', prewarm=['/login', '/dashboard'])
    ph = v == 'p'
    P = lambda t, **kw: {'text': t, 'within': PORTAO, **kw}
    c.mark(1)
    c.hover(P('Primeiro passo', exact=True), 0.5, at=c.A(1, 'primeiro', 0.9), label='selo Primeiro passo', noScroll=True)
    c.hover(P('Antes de usar o sistema'), 0.5, at=c.A(1, 'antes', 0.9), label='Antes de usar o sistema', noScroll=ph)
    c.mark(2)
    if ph:
        rola_ate(c, 'Antes de usar o sistema', at=c.A(2, 'Os', 1.4), label='sobe ao painel do portão', y=110, dur_ms=700, dentro=PORTAO)
    c.hover(P('Este vídeo explica os combinados', ), 0.8, at=c.A(2, 'Os', 0.8), label='Este vídeo explica os combinados importantes')
    c.mark(3)
    if ph:
        rola_ate(c, 'Assisti ao vídeo até o final e entendi os combinados.', at=c.A(3, 'No', 1.6), label='desce à caixa', y=300, dur_ms=800, dentro=PORTAO)
    c.hover(P('Assisti ao vídeo até o final e entendi os combinados.'), 0.8, at=c.A(3, 'marca', 0.9), label='caixa Assisti ao vídeo (ainda apagada)')
    c.hover(P('Assista até o final para confirmar'), 0.6, at=c.A(3, 'libera', 0.9), label='botão Assista até o final para confirmar')
    c.mark(4)
    if ph:
        rola_ate(c, 'Você pode pular durante o teste', at=c.A(4, 'Começou', 1.6), label='desce ao quadro do teste', y=260, dur_ms=800, dentro=PORTAO)
    c.hover(P('Você pode pular durante o teste'), 0.7, at=c.A(4, 'teste', 0.9), label='quadro Você pode pular durante o teste')
    if ph:
        rola_ate(c, 'Pular por agora', at=c.A(4, 'pular', 1.8), label='desce ao botão Pular por agora', y=520, dur_ms=700, dentro=PORTAO)
    c.hover(P('Pular por agora'), 0.8, at=c.A(4, 'pular', 0.9), label='botão Pular por agora (sem clicar)', **({'noScroll': True} if ph else {}))
    c.mark(5)
    c.cursor((760, 470) if not ph else (195, 600), at=c.A(5, 'Uma', 0.6), label='cursor sai de cima do botão')
    c.fim()
    return c


# ================================================================ cap02 · Como funciona a trilha (S2)
def abrir_trilha_pelo_menu_d(c, a_menu, a_item, a_clique):
    c.click(MENU_CONTA, at=a_menu, label='cartão Rafael Nogueira (menu da conta)')
    c.waitfor(target=ITEM('Tutoriais | EcoFlix'), timeout=8)
    c.hover(ITEM('Tutoriais | EcoFlix'), 0.4, at=a_item, label='Tutoriais | EcoFlix')
    c.click(ITEM('Tutoriais | EcoFlix'), at=a_clique, label='Tutoriais | EcoFlix (abre a trilha)')
    c.waitfor(text='Aprenda a usar o EcoSistema', timeout=25)


def abrir_trilha_pelo_menu_p(c, a_menu, a_conta, a_clique):
    c.toque(BTN('Menu'), at=a_menu, label='Menu (barra de baixo)')
    c.waitfor(text='Conta', timeout=8)
    rola_ate(c, 'Conta', at=a_conta, label='a gaveta desce até a seção Conta', y=160, dur_ms=800, dentro=DLG)
    c.click(BTN('Tutoriais | EcoFlix', within=DLG), at=a_clique, label='Tutoriais | EcoFlix (abre a trilha)')
    c.waitfor(text='Aprenda a usar o EcoSistema', timeout=25)


def cap02(v):
    c = cap_novo(2, v, setup=vai('/dashboard', 'Olá, Rafael!'), prewarm=['/login', '/dashboard', '/ecoflix'])
    if v == 'd':
        c.mark(1)
        abrir_trilha_pelo_menu_d(c, c.A(1, 'menu', 1.3), c.A(1, 'Tutoriais', 1.1), c.A(1, 'EcoFlix', 0.9))
        c.mark(2)
        c.hover(TXT('Aprenda a usar o EcoSistema'), 0.3, at=c.A(2, 'Aqui', 0.8), label='Aprenda a usar o EcoSistema')
        c.hover(TXT('Trilha do seu plano'), 0.4, at=c.A(2, 'aulas,', 0.9), label='Trilha do seu plano e a barra')
        c.mark(3)
        c.hover({'placeholder': 'Buscar aula'}, 0.6, at=c.A(3, 'buscar', 0.9), label='campo Buscar aula')
        c.hover(LINK('Minha Lista'), 0.8, at=c.A(3, 'Minha', 0.9), label='aba Minha Lista (sem clicar)', noScroll=True)
        c.mark(4)
        rola_ate(c, 'Bem-vindo ao EcoSistema', at=c.A(4, 'Primeiro', 1.2), label='desce aos primeiros módulos', y=120, dur_ms=900, dentro='main')
        c.hover(TXT('Formação básica'), 0.4, at=c.A(4, 'Formação', 0.9), label='selo Formação básica')
        c.mark(5)
        rola_ate(c, 'Nota Fiscal de mercadoria (NF-e)', at=max(0.0, c.L(5) - 0.9), label='desce ao primeiro módulo do plano (T16)', y=130, dur_ms=2200, dentro='main')
        c.hover(TXT('Tem no seu plano'), 0.5, at=c.A(5, 'selo', 0.9), label='selo Tem no seu plano')
        c.mark(6)
        rola_ate(c, 'Sua conta e sua empresa', at=max(0.0, c.L(6) - 0.9), label='volta ao T1', y=150, dur_ms=2200, dentro='main')
        c.hover(TXT('Próxima aula recomendada'), 0.6, at=c.A(6, 'marcada,', 0.9), label='Próxima aula recomendada')
        c.mark(7)
        rola_ate(c, 'Materiais e tabelas de preço', at=c.A(7, 'Precisa', 1.8), label='desce ao T3', y=330, dur_ms=900, dentro='main')
        c.click(BTNX('Materiais e tabelas de preço'), at=c.A(7, 'Pode', 1.1), label='aula Materiais e tabelas de preço (fora da ordem)')
        c.waitfor(text='Consultar fora da ordem?', timeout=8)
        c.marcar(TXT('Consultar fora da ordem?', within=DLG), label='diálogo Consultar fora da ordem?')
        c.click(BTN('Voltar à trilha'), at=c.E(7, 'marcada', 0.5), label='Voltar à trilha')
    else:
        c.mark(1)
        abrir_trilha_pelo_menu_p(c, c.A(1, 'menu', 1.4), c.A(1, 'sua', 1.0), c.A(1, 'EcoFlix', 1.0))
        c.mark(2)
        c.hover(TXT('Aprenda a usar o EcoSistema'), 0.3, at=c.A(2, 'Aqui', 0.8), label='Aprenda a usar o EcoSistema')
        c.hover(TXT('Trilha do seu plano'), 0.5, at=c.A(2, 'aulas,', 0.9), label='cartão Trilha do seu plano')
        c.mark(3)   # no celular a busca e a Minha Lista ficam fora da tela da trilha: a tela fica parada nesta frase
        c.mark(4)
        c.hover(TXTX('Formação básica:'), 0.5, at=c.A(4, 'Formação', 0.9), label='Formação básica: n de total')
        rola_ate(c, 'Sequência recomendada', at=c.A(4, 'o', 2.0, nth=0), label='desce à lista de aulas', y=110, dur_ms=800)
        c.mark(5)
        # a lista do celular não tem selos: na frase do selo, abre a 1ª aula e a gaveta "Ver trilha"
        c.click(BTNX('Sua conta e sua empresa'), at=c.A(5, 'Depois', 1.4), label='aula Sua conta e sua empresa (próxima recomendada)')
        c.waitfor(text='Ver trilha', timeout=25)
        c.toque(BTNX('Ver trilha'), at=c.A(5, 'módulos', 1.2), label='Ver trilha (gaveta com os selos)')
        c.waitfor(text='Sua trilha', timeout=8)
        rola_ate(c, 'Nota Fiscal de mercadoria (NF-e)', at=c.A(5, 'selo', 1.8), label='a gaveta desce ao módulo do plano (T16)', y=300, dur_ms=1600, dentro=DLG)
        c.marcar(TXT('Tem no seu plano', within=DLG), label='selo Tem no seu plano')
        c.mark(6)
        c.press('Escape', at=c.A(6, 'próxima', 1.0), label='fecha a gaveta da trilha')
        c.toque(BTNX('Voltar'), at=c.A(6, 'fica', 0.6), label='Voltar à trilha')
        c.waitfor(text='Aulas da trilha', timeout=15)
        c.hover(TXTX('Próxima recomendada'), 0.6, at=c.A(6, 'marcada,', 0.9), label='Próxima recomendada')
        c.mark(7)
        rola_ate(c, 'Materiais e tabelas de preço', at=c.A(7, 'Precisa', 1.8), label='desce ao T3', y=420, dur_ms=900)
        c.click(BTNX('Materiais e tabelas de preço'), at=c.A(7, 'Pode', 1.1), label='aula Materiais e tabelas de preço (fora da ordem)')
        c.waitfor(text='Consultar fora da ordem?', timeout=8)
        c.marcar(TXT('Consultar fora da ordem?', within=DLG), label='gaveta Consultar fora da ordem?')
        c.toque(BTN('Voltar à trilha'), at=c.E(7, 'marcada', 0.5), label='Voltar à trilha')
    c.fim()
    return c


# ================================================================ cap03 · Aulas de outros módulos (S3)
def cap03(v):
    c = cap_novo(3, v, setup=TRILHA, prewarm=['/login', '/dashboard', '/ecoflix'])
    if v == 'd':
        c.mark(1)
        rola_ate(c, 'CRM/Kanban', at=c.A(1, 'módulos', 1.4), label='desce ao último módulo (CRM/Kanban)', y=150, dur_ms=2200, dentro='main')
        c.hover(TXT('Não tem no seu plano'), 0.5, at=c.A(1, 'selo', 0.9), label='selo Não tem no seu plano')
        c.mark(2)
        c.mark(3)
        c.click(BTNX('CRM/Kanban'), at=c.A(3, 'Pode', 1.1), label='aula CRM/Kanban (Conheça este módulo)')
        c.waitfor(text='Consultar fora da ordem?', timeout=8)
        c.click(BTN('Consultar esta aula'), at=c.A(3, 'É', 1.3), label='Consultar esta aula')
        c.waitfor(text='Conheça outros módulos', timeout=25)
        rola_ate(c, 'Conheça outros módulos', at=c.A(3, 'jeito', 0.9), label='o painel da trilha desce a Conheça outros módulos', y=260, dur_ms=700)
        c.marcar(TXT('Conheça outros módulos'), label='painel Conheça outros módulos')
        c.mark(4)
        rola_ate(c, 'Conheça agora. Ative quando fizer sentido.', at=c.A(4, 'Se', 0.9), label='os detalhes descem ao cartão Conheça agora', y=260, dur_ms=900)
        c.hover(BTN('Adicionar ao meu plano'), 0.6, at=c.A(4, 'administrador', 0.9), label='botão Adicionar ao meu plano (sem clicar)')
        c.mark(5)
        c.cursor((900, 400), at=c.A(5, 'E', 0.6), label='cursor sai de cima do botão')
    else:
        c.mark(1)
        rola_ate(c, 'CRM/Kanban', at=c.A(1, 'módulos', 1.4), label='desce ao último módulo (CRM/Kanban)', y=170, dur_ms=2200, so_se_fora=False)
        c.marcar(TXT('Conheça este módulo'), label='Conheça este módulo')
        c.mark(2)
        c.mark(3)
        c.click(BTNX('CRM/Kanban'), at=c.A(3, 'Pode', 1.1), label='aula CRM/Kanban (Conheça este módulo)')
        c.waitfor(text='Consultar fora da ordem?', timeout=8)
        c.toque(BTN('Consultar esta aula'), at=c.A(3, 'É', 1.3), label='Consultar esta aula')
        c.waitfor(text='Ver trilha', timeout=25)
        c.marcar(TXT('Não tem no seu plano'), label='selo Não tem no seu plano (alto dos detalhes)')
        c.toque(BTNX('Ver trilha'), at=c.A(3, 'jeito', 0.5), label='Ver trilha (gaveta)')
        c.waitfor(text='Sua trilha', timeout=8)
        rola_ate(c, 'Conheça outros módulos', at=c.A(3, 'conhecer', 0.1), label='a gaveta desce a Conheça outros módulos', y=300, dur_ms=1500, dentro=DLG)
        c.marcar(TXT('Conheça outros módulos', within=DLG), label='gaveta Conheça outros módulos')
        c.mark(4)
        c.press('Escape', at=c.A(4, 'Se', 0.9), label='fecha a gaveta')
        rola_ate(c, 'Conheça agora. Ative quando fizer sentido.', at=c.A(4, 'contratação', 1.4), label='a página desce ao cartão Conheça agora', y=250, dur_ms=900)
        c.hover(BTN('Adicionar ao meu plano'), 0.6, at=c.A(4, 'administrador', 0.9), label='botão Adicionar ao meu plano (sem clicar)')
        c.mark(5)
    c.fim()
    return c


# ================================================================ cap04 · Dúvida depois da aula (S2)
def cap04(v):
    c = cap_novo(4, v, setup=TRILHA, prewarm=['/login', '/dashboard', '/ecoflix'])
    ph = v == 'p'
    LEG = SEL('button[aria-label="Ativar ou escolher legenda"]:visible, button[aria-label^="Trocar legenda"]:visible')
    c.mark(1)
    botao = BTNX('Começar trilha') if v == 'd' else BTNX('Começar pelos tutoriais')
    c.click(botao, at=0.0, label='Começar trilha (abre a aula Sua conta e sua empresa)')
    c.waitfor(text='Tirar dúvidas com o suporte', timeout=25)
    c.hover(SEL('video'), 0.3, at=c.A(1, 'player,', 0.9), label='o player (os controles aparecem)', noScroll=True)
    c.click(LEG, at=c.A(1, 'ligar', 1.2), label='Legendas (abre a faixa, o tamanho e o estilo)', noScroll=True)
    c.waitfor(text='Português', timeout=8)
    c.click({'role': 'radio', 'name': 'Português'}, at=c.A(1, 'legenda', 0.4), label='faixa Português (liga a legenda)', noScroll=True)
    c.hover(SEL('[role=radiogroup][aria-label="Tamanho da legenda"]:visible'), 0.5, at=c.A(1, 'tamanho', 0.9), label='Tamanho da legenda', noScroll=True)
    c.click(LEG, at=c.A(1, 'mudar', 1.3), label='fecha o quadro das legendas', noScroll=True)
    c.cursor((900, 300) if not ph else (195, 150), at=c.A(1, 'mudar', 0.5), label='o mouse no player (os controles voltam)')
    VEL = SEL('button[title="Velocidade"]:visible') if not ph else SEL('button[aria-label^="Velocidade de reprodução"]:visible')
    V10 = SEL('button.sm\\:block:has(svg):visible', nth=0) if not ph else SEL('button[aria-label="Voltar 10 segundos"]:visible')
    A10 = SEL('button.sm\\:block:has(svg):visible', nth=1) if not ph else SEL('button[aria-label="Avançar 10 segundos"]:visible')
    c.hover(VEL, 0.4, at=c.A(1, 'velocidade,', 0.5), label='Velocidade', noScroll=True)
    c.hover(V10, 0.3, at=c.A(1, 'voltar', 0.9), label='Voltar 10 segundos', noScroll=True)
    c.hover(A10, 0.3, at=c.A(1, 'avançar', 0.9), label='Avançar 10 segundos', noScroll=True)
    if not ph:   # no celular o botão de tela cheia não aparece no player em pé
        c.hover(SEL('button[aria-label="Abrir em tela cheia"]:visible'), 0.5, at=c.A(1, 'tela', 0.9), label='Abrir em tela cheia (sem entrar)', noScroll=True)
    c.mark(2)
    # o vídeo fictício (12 min, sem índice para saltar) recebe o evento de fim: o app abre "Aula concluída" sozinho (e avança em 4 s se o mouse não se mexer por cima)
    c.ev("(()=>{const v=document.querySelector('video');if(!v)return 'SEM ALVO: video';v.pause();v.dispatchEvent(new Event('ended'));return 'fim do vídeo (evento ended)'})()",
         at=max(0.0, c.L(2) - 1.2), label='o vídeo chega ao fim')
    c.waitfor(text='Aula concluída', timeout=12)
    c.hover(TXT('Vamos para a próxima'), 0.5, at=c.A(2, 'marca', 0.6), label='quadro Aula concluída · Vamos para a próxima', noScroll=True)
    c.hover(BTN('Próxima aula agora'), 0.8, at=c.A(2, 'oferece', 0.9), label='Próxima aula agora (sem clicar)', noScroll=True)
    c.click(BTN('Ficar nesta aula'), at=c.E(2, 'próxima.', 0.9), label='Ficar nesta aula', noScroll=True)
    c.mark(3)
    rola_ate(c, 'Materiais e extras', at=c.A(3, 'Embaixo', 0.6), label='os detalhes descem a Materiais e extras', y=420 if not ph else 480, dur_ms=900)
    c.hover(TXT('Materiais e extras'), 0.5, at=c.A(3, 'Materiais', 0.9), label='Materiais e extras')
    c.marcar(TXTX('Lista de conferência do cadastro da empresa'), at=c.A(3, 'arquivos', 0.5), label='material Lista de conferência do cadastro da empresa (sem abrir)')
    c.mark(4)
    rola_ate(c, 'Tirar dúvidas com o suporte', at=c.A(4, 'Ficou', 0.6), label='os detalhes no botão verde', y=330 if not ph else 380, dur_ms=700)
    c.hover(TXTX('Tirar dúvidas com o suporte'), 0.6, at=c.A(4, 'botão', 0.9), label='botão Tirar dúvidas com o suporte (sem clicar)')
    c.mark(5)
    c.mark(6)
    c.hover(TXTX('Tirar dúvidas com o suporte'), 0.6, at=c.A(6, 'Assim,', 0.9), label='o botão em destaque de novo')
    c.fim()
    return c


# ================================================================ cap06 · Um passeio pelo menu (S2)
SB = lambda t, **kw: {'text': t, 'within': '[data-sidebar=sidebar], aside, nav', **kw}
GRUPO = lambda n: {'role': 'button', 'name': n, 'exact': True}
ITEM_MENU = lambda n: {'role': 'link', 'name': n, 'exact': True}


FISCAIS = [('Notas Fiscais (NF-e)', 'notas'), ('Notas de Serviço (NFS-e)', 'serviço,'), ('Transporte (MDF-e)', 'transporte,'), ('Ambiental (MTR/CDF)', 'documentos'),
           ('Relatório/Estoque Fiscal', 'relatório')]


def cap06(v):
    c = cap_novo(6, v, setup=vai('/dashboard', 'Olá, Rafael!'), prewarm=['/login', '/dashboard'])
    if v == 'd':
        def vis(texto, at, label):
            """garante o item do menu dentro da área visível do menu lateral (rolagem suave do próprio menu)"""
            rola_ate(c, texto, at=at, label=label, y=300, dur_ms=500, so_se_fora=True)
        c.mark(1)
        c.hover(ITEM_MENU('Dashboard'), 0.5, at=c.A(1, 'Dashboard,', 0.9), label='menu: Dashboard', noScroll=True)
        c.mark(2)
        c.click(GRUPO('Financeiro'), at=c.A(2, 'Financeiro', 1.0), label='Financeiro (abre o grupo)')
        c.marcar(ITEM_MENU('Contas a Pagar/Receber'), at=c.A(2, 'contas', 0.2), label='subitens do Financeiro')
        c.mark(3)
        c.hover(ITEM_MENU('Pedidos'), 0.5, at=c.A(3, 'Pedidos,', 0.9), label='menu: Pedidos')
        c.mark(4)
        c.click(GRUPO('Fiscal & Ambiental'), at=c.A(4, 'Fiscal', 1.0), label='Fiscal & Ambiental (abre o grupo; o Financeiro fecha)')
        for item, palavra in FISCAIS:
            c.hover(ITEM_MENU(item), 0.3, at=c.A(4, palavra, 0.9), label=f'Fiscal & Ambiental: {item}')
        c.mark(5)
        c.click(GRUPO('Materiais'), at=c.A(5, 'Materiais,', 1.0), label='Materiais (abre o grupo; o Fiscal & Ambiental fecha)')
        c.marcar(ITEM_MENU('Ticket de Pesagem'), at=c.A(5, 'ticket', 0.2), label='subitens de Materiais')
        c.mark(6)
        vis('Coletas & Logística', c.A(6, 'Em', 1.4), 'o menu desce a Coletas & Logística')
        c.hover(GRUPO('Coletas & Logística'), 0.5, at=c.A(6, 'Coletas', 0.9), label='menu: Coletas & Logística (sem abrir)')
        c.mark(7)
        c.hover(ITEM_MENU('Clientes e Fornecedores'), 0.4, at=c.A(7, 'Clientes', 0.9), label='menu: Clientes e Fornecedores')
        c.hover(ITEM_MENU('Funcionários (RH)'), 0.4, at=c.A(7, 'Funcionários', 0.9), label='menu: Funcionários (RH)')
        c.hover(ITEM_MENU('CRM/Kanban'), 0.4, at=c.A(7, 'CRM.', 0.9), label='menu: CRM/Kanban')
        c.mark(8)
        vis('Gerencial (Filiais)', c.A(8, 'Na', 1.5), 'o menu desce ao Gerencial (Filiais)')
        c.hover(ITEM_MENU('Agenda'), 0.4, at=c.A(8, 'Agenda,', 0.9), label='menu: Agenda')
        c.hover(GRUPO('Gerencial (Filiais)'), 0.4, at=c.A(8, 'Gerencial', 0.9), label='menu: Gerencial (Filiais)')
        c.mark(9)
        c.hover(BTN('Configurações'), 0.6, at=c.A(9, 'Configurações', 0.9), label='rodapé: Configurações', noScroll=True)
        c.mark(10)
        c.hover(BTN('Buscar'), 0.6, at=c.A(10, 'busca,', 0.9), label='alto da tela: Buscar (sem abrir)', noScroll=True)
        c.hover(BTN('Notificações'), 0.6, at=c.A(10, 'sino', 0.9), label='alto da tela: Notificações (sem abrir)', noScroll=True)
        c.mark(11)
        rola_ate(c, 'Dashboard', at=c.A(11, 'Algumas', 0.8), label='o menu volta ao topo', y=120, dur_ms=600, so_se_fora=True)
        c.cursor((760, 470), at=c.A(11, 'dependem', 0.6), label='cursor sai do menu')
    else:
        c.mark(1)
        c.toque(BTN('Menu'), at=c.A(1, 'menu', 1.4), label='Menu (barra de baixo)')
        c.waitfor(text='Conta', timeout=8)
        c.hover(ITEM_MENU('Dashboard'), 0.5, at=c.A(1, 'Dashboard,', 0.9), label='gaveta: Dashboard', noScroll=True)
        c.mark(2)
        c.click(GRUPO('Financeiro'), at=c.A(2, 'Financeiro', 1.0), label='Financeiro (abre o grupo)')
        c.marcar(ITEM_MENU('Contas a Pagar/Receber'), at=c.A(2, 'contas', 0.2), label='subitens do Financeiro')
        c.mark(3)
        c.hover(ITEM_MENU('Pedidos'), 0.5, at=c.A(3, 'Pedidos,', 0.9), label='gaveta: Pedidos')
        c.mark(4)
        c.click(GRUPO('Fiscal & Ambiental'), at=c.A(4, 'Fiscal', 1.0), label='Fiscal & Ambiental (abre o grupo; o Financeiro fecha)')
        for item, palavra in FISCAIS:
            c.hover(ITEM_MENU(item), 0.3, at=c.A(4, palavra, 0.9), label=f'Fiscal & Ambiental: {item}')
        c.mark(5)
        c.click(GRUPO('Materiais'), at=c.A(5, 'Materiais,', 1.0), label='Materiais (abre o grupo; o Fiscal & Ambiental fecha)')
        c.marcar(ITEM_MENU('Ticket de Pesagem'), at=c.A(5, 'ticket', 0.2), label='subitens de Materiais')
        c.mark(6)
        rola_ate(c, 'Coletas & Logística', at=c.A(6, 'Em', 1.4), label='a gaveta desce a Coletas & Logística', y=420, dur_ms=600, dentro=DLG)
        c.hover(GRUPO('Coletas & Logística'), 0.5, at=c.A(6, 'Coletas', 0.9), label='gaveta: Coletas & Logística (sem abrir)')
        c.mark(7)
        c.hover(ITEM_MENU('Clientes e Fornecedores'), 0.4, at=c.A(7, 'Clientes', 0.9), label='gaveta: Clientes e Fornecedores')
        c.hover(ITEM_MENU('Funcionários (RH)'), 0.4, at=c.A(7, 'Funcionários', 0.9), label='gaveta: Funcionários (RH)')
        c.hover(ITEM_MENU('CRM/Kanban'), 0.4, at=c.A(7, 'CRM.', 0.9), label='gaveta: CRM/Kanban')
        c.mark(8)
        # no celular o "Gerencial (Filiais)" vem antes da "Agenda" (ordem do menuItems): a câmera rola até ele na frase dele
        rola_ate(c, 'Gerencial (Filiais)', at=c.A(8, 'Na', 1.5), label='a gaveta desce ao Gerencial (Filiais)', y=420, dur_ms=600, dentro=DLG)
        c.hover(ITEM_MENU('Agenda'), 0.4, at=c.A(8, 'Agenda,', 0.9), label='gaveta: Agenda')
        c.hover(GRUPO('Gerencial (Filiais)'), 0.4, at=c.A(8, 'Gerencial', 0.9), label='gaveta: Gerencial (Filiais)')
        c.mark(9)
        c.hover(BTN('Configurações', within=DLG), 0.6, at=c.A(9, 'Configurações', 0.9), label='rodapé da gaveta: Configurações', noScroll=True)
        c.mark(10)
        c.press('Escape', at=c.A(10, 'No', 0.9), label='fecha a gaveta do Menu (a busca e o sino são do computador)')
        c.mark(11)
    c.fim()
    return c


# ================================================================ cap07 · Os menus e a sua conta (S2)
def abrir_config_aba_d(c, a_cfg, a_aba, aba, espera):
    c.click(BTN('Configurações'), at=a_cfg, label='rodapé: Configurações', noScroll=True)
    c.waitfor(text='Gerencie as configurações', timeout=15, optional=True) if False else c.waitfor(target=TXT(aba, within='main'), timeout=15)
    c.click(TXT(aba), at=a_aba, label=f'aba {aba}')
    c.waitfor(text=espera, timeout=12)


def cap07(v):
    c = cap_novo(7, v, setup=vai('/dashboard', 'Olá, Rafael!'), prewarm=['/login', '/dashboard', '/configuracoes?tab=appearance'])
    if v == 'd':
        c.mark(1)
        c.click(MENU_CONTA, at=c.A(1, 'clicando', 1.0), label='cartão Rafael Nogueira (menu da conta)')
        c.waitfor(target=ITEM('Assinatura'), timeout=8)
        c.mark(2)
        c.hover(ITEM('Perfil'), 0.4, at=c.A(2, 'perfil,', 0.9), label='Meu Perfil')
        c.hover(ITEM('Assinatura'), 0.4, at=c.A(2, 'Assinatura,', 0.9), label='Assinatura')
        c.click(ITEM('Tema'), at=c.A(2, 'Tema,', 0.9), label='Tema (abre Claro, Escuro e Sistema)')
        c.marcar(TXT('Sistema'), at=c.A(2, 'aparelho.', 0.6), label='Tema: Claro, Escuro, Sistema (sem trocar)')
        c.mark(3)
        c.hover(ITEM('Tutoriais | EcoFlix'), 0.4, at=c.A(3, 'Tutoriais', 0.9), label='Tutoriais | EcoFlix')
        c.click(ITEM('Central de Ajuda'), at=c.A(3, 'Central', 1.0), label='Central de Ajuda (abre a gaveta de artigos)')
        c.waitfor(target={'placeholder': 'Pesquisar artigos...'}, timeout=10)
        c.marcar({'placeholder': 'Pesquisar artigos...'}, at=c.A(3, 'pesquisa', 0.5), label='Pesquisar artigos...')
        c.press('Escape', at=c.A(3, 'Falar', 2.7), label='fecha a Central de Ajuda')
        c.click(MENU_CONTA, at=c.A(3, 'Falar', 1.9), label='menu da conta de novo')
        c.waitfor(target=ITEM('Falar com o Suporte'), timeout=8)
        c.click(ITEM('Falar com o Suporte'), at=c.A(3, 'Falar', 1.0), label='Falar com o Suporte (abre a janela)')
        c.waitfor(text='Nos conte o que está acontecendo', timeout=10)
        c.hover(TXTX('Em qual tela/módulo?', within=DLG), 0.5, at=c.A(3, 'tela', 0.9), label='Em qual tela/módulo? *')
        c.hover(TXTX('O que aconteceu?', within=DLG), 0.5, at=c.A(3, 'aconteceu,', 0.9), label='O que aconteceu? Descreva com detalhes *')
        c.hover(BTNX('Falar no WhatsApp', within=DLG), 0.8, at=c.A(3, 'WhatsApp', 0.9), label='Falar no WhatsApp (apagado até preencher; sem clicar)')
        c.mark(4)
        c.ev(FECHAR_EVAL, at=c.E(3, 'isso.', 0.5), label='fecha a janela do suporte sem enviar')
        c.click(MENU_CONTA, at=c.A(4, 'No', 0.35), label='menu da conta')
        c.waitfor(target=BTN('Trocar de conta'), timeout=8)
        c.click(BTN('Trocar de conta'), at=c.A(4, 'dá', 0.9), label='cartão da conta (Trocar de conta): abre Adicionar conta')
        c.marcar(TXTX('Adicionar conta'), label='Adicionar conta')
        c.press('Escape', at=c.A(4, 'botão', 1.7), label='fecha o menu da conta')
        c.hover(BTN('Sair'), 0.8, at=c.A(4, 'Sair', 0.9), label='rodapé: Sair (NUNCA clicar)', noScroll=True)
        c.mark(5)
        c.press('Escape', at=c.A(5, 'Prefere', 0.6), label='fecha o menu da conta')
        c.click(BTN('Configurações'), at=c.A(5, 'Configurações,', 1.5), label='rodapé: Configurações', noScroll=True)
        c.waitfor(text='Aparência', timeout=15)
        c.click(TXT('Aparência'), at=c.A(5, 'Aparência,', 1.0), label='aba Aparência')
        c.waitfor(text='Estilo de Navegação (Desktop)', timeout=12)
        c.marcar(TXT('Estilo de Navegação (Desktop)'), label='Estilo de Navegação (Desktop)')
        c.click(SEL('label[for=topbar-nav]'), at=c.A(5, 'Superior', 1.0), label='Menu Superior (o menu passa para a barra do topo)')
        c.waitfor(text='Estilo de navegação alterado para Menu Superior', timeout=12)
        c.wait(1.0)
        c.mark(6)
        # a linha 5 é o celular (gravada em capNN.9x16.json e entra no centro do palco); aqui o menu superior continua na tela
        c.cursor((760, 470), at=c.A(6, 'No', 0.6), label='cursor ao centro')
    else:
        c.mark(1)
        c.toque(BTN('Menu'), at=c.A(1, 'menu', 1.4), label='Menu (barra de baixo)')
        c.waitfor(text='Conta', timeout=8)
        rola_ate(c, 'Conta', at=c.A(1, 'ele', 1.0), label='a gaveta desce à seção Conta', y=170, dur_ms=800, dentro=DLG)
        c.marcar(TXT('Conta', within=DLG), label='seção Conta')
        c.mark(2)
        c.hover(BTN('Perfil', within=DLG), 0.4, at=c.A(2, 'perfil,', 0.9), label='Perfil')
        c.hover(BTN('Assinatura', within=DLG), 0.4, at=c.A(2, 'Assinatura,', 0.9), label='Assinatura')
        c.hover(TXT('Tema', within=DLG), 0.4, at=c.A(2, 'Tema,', 0.9), label='Tema (rodapé da gaveta)')
        c.mark(3)
        c.hover(BTN('Tutoriais | EcoFlix', within=DLG), 0.4, at=c.A(3, 'Tutoriais', 0.9), label='Tutoriais | EcoFlix')
        c.hover(BTN('Central de Ajuda', within=DLG), 0.4, at=c.A(3, 'Central', 0.9), label='Central de Ajuda')
        c.hover(BTN('Falar com o Suporte', within=DLG), 0.4, at=c.A(3, 'Falar', 0.9), label='Falar com o Suporte (sem clicar)')
        c.mark(4)
        rola_ate(c, 'Sair', at=c.A(4, 'No', 0.6), label='a gaveta desce ao rodapé', y=700, dur_ms=600, dentro=DLG, so_se_fora=True)
        c.hover(BTNX('Sair', within=DLG), 0.8, at=c.A(4, 'Sair', 0.9), label='rodapé da gaveta: Sair (NUNCA clicar)', noScroll=True)
        c.mark(5)
        c.click(BTN('Configurações', within=DLG), at=c.A(5, 'Em', 1.2), label='Configurações (rodapé da gaveta)', noScroll=True)
        c.waitfor(text='Aparência', timeout=15)
        c.click(TXT('Aparência'), at=c.A(5, 'Aparência,', 1.2), label='aba Aparência')
        c.waitfor(text='Estilo de Navegação (Desktop)', timeout=12)
        c.marcar(TXT('Estilo de Navegação (Desktop)'), label='Estilo de Navegação (Desktop)')
        c.marcar(TXTX('Esta opção só afeta a visualização em desktop.'), at=c.A(5, 'Superior', 0.9), label='Esta opção só afeta a visualização em desktop.')
        c.mark(6)
        # a própria tela do celular: a barra de baixo e a gaveta
        # 1.60: o mouse parado sobre a barra de baixo demorava 5 s para achar o alvo (o botão do Cato fica por cima do canto): só marca
        c.marcar(TXT('Início', within='nav'), at=c.A(6, 'Início,', 0.4), label='barra de baixo: Início')
        c.marcar(TXT('Caixa', within='nav'), at=c.A(6, 'Caixa,', 0.4), label='barra de baixo: Caixa')
        c.toque(SEL('nav button:has(svg.lucide-plus)'), at=c.A(6, 'Novo,', 1.0), label='barra de baixo: Novo (abre o leque)')
        c.marcar(TXT('Ticket de pesagem'), at=c.A(6, 'ticket', 0.4), label='leque do Novo: Compra, Venda, Ticket de pesagem, Nota Fiscal')
        c.ev("(()=>{const e=document.elementFromPoint(195,150);if(!e)return 'SEM ALVO';e.dispatchEvent(new MouseEvent('pointerdown',{bubbles:true}));e.click();return 'toque fora: '+e.tagName})()", at=c.A(6, 'Estoque', 1.5), label='toque fora fecha o leque')
        c.marcar(TXT('Estoque', within='nav'), at=c.A(6, 'Estoque', 0.4), label='barra de baixo: Estoque')
        c.toque(BTN('Menu'), at=c.A(6, 'Menu,', 1.3, nth=1), label='Menu (abre a gaveta)')
        c.waitfor(text='Conta', timeout=8)
        rola_ate(c, 'Conta', at=c.A(6, 'conta.', 1.8), label='a gaveta desce à seção Conta', y=170, dur_ms=900, dentro=DLG)
    c.fim()
    return c


# ================================================================ cap09 · As palavras do pátio (S2)
def cap09(v):
    c = cap_novo(9, v, setup=vai('/dashboard', 'Olá, Rafael!'), prewarm=['/login', '/dashboard', '/configuracoes?tab=usability'])
    c.mark(1)
    c.mark(2)
    if v == 'd':
        c.click(BTN('Configurações'), at=c.A(2, 'Uma', 2.5), label='rodapé: Configurações', noScroll=True)
        c.waitfor(text='Usabilidade', timeout=15)
        c.click(TXT('Usabilidade'), at=c.A(2, 'dica:', 0.9), label='aba Usabilidade')
    else:
        c.toque(BTN('Menu'), at=c.A(2, 'Uma', 1.8), label='Menu (barra de baixo)')
        c.waitfor(text='Conta', timeout=8)
        c.click(BTN('Configurações', within=DLG), at=c.A(2, 'dica:', 0.9), label='Configurações (rodapé da gaveta)', noScroll=True)
        c.waitfor(text='Usabilidade', timeout=15)
        c.click(TXT('Usabilidade'), at=c.A(2, 'ao', 1.0), label='aba Usabilidade')
    c.waitfor(text='Inverter os termos Cliente e Fornecedor', timeout=12)
    alvo_sw = BTNX('Inverter os termos Cliente e Fornecedor') if False else TXT('Inverter os termos Cliente e Fornecedor')
    c.hover(alvo_sw, 0.9, at=c.A(2, 'inverter', 0.9), label='Inverter os termos Cliente e Fornecedor (só olhar)')
    rola_ate(c, 'Compra: Fornecedor', at=c.A(2, 'Por', 1.5),
             label='desce à frase da mesma lógica', y=360, dur_ms=700, prefixo=True)
    c.hover(TXTX('Compras, vendas, vínculos, saldos e documentos fiscais continuam com a mesma lógica.'), 0.8, at=c.A(2, 'nada', 0.9),
            label='Compras, vendas, vínculos, saldos e documentos fiscais continuam com a mesma lógica.')
    for i in range(3, len(c.linhas) + 1):
        c.mark(i)
    c.fim()
    return c


# ================================================================ cap10 a 14 · Assinatura (S2)
def abrir_assinatura(c, v, a_menu, a_item):
    if v == 'd':
        c.click(MENU_CONTA, at=a_menu, label='cartão Rafael Nogueira (menu da conta)')
        c.waitfor(target=ITEM('Assinatura'), timeout=8)
        c.click(ITEM('Assinatura'), at=a_item, label='Assinatura')
    else:
        c.toque(BTN('Menu'), at=a_menu, label='Menu (barra de baixo)')
        c.waitfor(text='Conta', timeout=8)
        rola_ate(c, 'Conta', at=round(a_menu + 0.9, 2), label='a gaveta desce à seção Conta', y=170, dur_ms=700, dentro=DLG)
        c.click(BTN('Assinatura', within=DLG), at=a_item, label='Assinatura')
    c.waitfor(text='Gerencie seu plano, módulos e pagamentos' if v == 'd' else 'Uso da conta', timeout=25)


def cap10(v):
    c = cap_novo(10, v, setup=vai('/dashboard', 'Olá, Rafael!'), prewarm=['/login', '/dashboard', '/assinatura'])
    c.mark(1)
    abrir_assinatura(c, v, c.A(1, 'fica', 1.4), c.A(1, 'Assinatura,', 1.0))
    c.waitfor(text='Uso da conta', timeout=15)
    c.mark(2)   # a linha 2 é a VARIANTE (cap40: conta em teste); aqui a tela fica parada
    c.mark(3)
    rola_ate(c, 'Recicla Vale Metais Ltda', at=c.A(3, 'No', 0.9), label='a página no alto do cartão do plano', y=170, dur_ms=500, dentro='main', so_se_fora=True)
    c.hover(EM_MAIN('Recicla Vale Metais Ltda', exact=True), 0.4, at=c.A(3, 'alto,', 0.9), label='nome da empresa')
    c.hover(EM_MAIN('Ativa', exact=True), 0.4, at=c.A(3, 'Ativa,', 0.9), label='selo Ativa')
    c.hover(EM_MAIN('Plano Personalizado', ), 0.4, at=c.A(3, 'plano,', 0.9), label='Plano Personalizado • 10 módulos')
    c.mark(4)
    c.hover(EM_MAIN('25 dias restantes'), 0.5, at=c.A(4, 'dias', 0.9), label='25 dias restantes')
    c.hover(EM_MAIN('Vencimento', exact=True), 0.6, at=c.A(4, 'vencimento:', 0.9), label='Vencimento 05/12/2026')
    c.mark(5)   # ilustração (os três selos de status)
    c.mark(6)
    rola_ate(c, 'Formas de pagamento', at=c.A(6, 'Embaixo,', 1.6), label='a página desce ao valor e às formas de pagamento', y=330, dur_ms=800, dentro='main')
    c.hover(EM_MAIN('Valor mensal', exact=True), 0.4, at=c.A(6, 'valor', 0.9), label='Valor mensal (sem zoom no valor)')
    c.hover(EM_MAIN('Formas de pagamento', exact=True), 0.5, at=c.A(6, 'formas', 0.9), label='Formas de pagamento: PIX, Boleto, Cartão')
    c.mark(7)
    rola_ate(c, 'Uso da conta', at=c.A(7, 'Em', 1.4), label='a página sobe a Uso da conta', y=150 if v == 'd' else 120, dur_ms=800, dentro='main')
    c.hover(EM_MAIN('Usuários', exact=True), 0.5, at=c.A(7, 'cadastrados', 0.9), label='Uso da conta: Usuários 1 / 3')
    c.hover(EM_MAIN('Notas fiscais este mês', exact=True), 0.5, at=c.A(7, 'notas', 0.9), label='Uso da conta: Notas fiscais este mês')
    c.mark(8)
    rola_ate(c, 'Pagar Agora', at=c.A(8, 'Uma', 1.6), label='a página desce a Pagar Agora', y=520 if v == 'd' else 380, dur_ms=800, dentro='main', prefixo=True)
    c.hover(BTNX('Pagar Agora'), 0.5, at=c.A(8, 'Pagar', 0.9), label='botão Pagar Agora (sem clicar)')
    rola_ate(c, 'Gerenciar plano', at=c.A(8, 'mudar', 1.7), label='a página desce a Gerenciar plano', y=520 if v == 'd' else 380, dur_ms=1200, dentro='main', prefixo=True)
    c.hover(BTNX('Gerenciar plano'), 0.6, at=c.A(8, 'plano', 0.9), label='botão Gerenciar plano (sem clicar)')
    c.fim()
    return c


def cap11(v):
    c = cap_novo(11, v, setup=assinatura(v), prewarm=['/login', '/dashboard', '/assinatura'])
    c.mark(1)
    rola_ate(c, 'Plano & módulos', at=c.A(1, 'Mais', 0.8), label='desce a Plano & módulos', y=140, dur_ms=700, dentro='main')
    c.marcar(EM_MAIN('Plano & módulos'), label='cartão Plano & módulos')
    rola_ate(c, 'Módulos ativos', at=c.A(1, 'Módulos', 0.9), label='desce a Módulos ativos', y=170, dur_ms=550, dentro='main')
    c.hover(EM_MAIN('Módulos ativos', exact=True), 0.6, at=c.A(1, 'libera', 0.9), label='Módulos ativos')
    c.mark(2)
    c.hover(EM_MAIN('· Nível 1'), 0.8, at=c.A(2, 'nível,', 0.9), label='Notas Fiscais · Nível 1 (Módulos ativos)')
    c.mark(3)   # a linha 3 é a VARIANTE (cap41: sem o CRM, com "Adicione ao seu plano"); aqui a tela fica parada
    c.cursor((900, 300) if v == 'd' else (195, 300), at=c.A(3, 'Se', 0.5), label='cursor sai de cima')
    for i in range(4, len(c.linhas) + 1):
        c.mark(i)
    c.fim()
    return c


def cap13(v):
    """só ilustrações (a régua do mês, os aparelhos, "Sua equipe cresceu!"): a gravação fica parada no cartão Plano & módulos"""
    c = cap_novo(13, v, setup=assinatura(v), prewarm=['/login', '/dashboard', '/assinatura'])
    c.mark(1)
    rola_ate(c, 'Plano & módulos', at=0.0, label='desce ao cartão Plano & módulos', y=140, dur_ms=1000, dentro='main')
    for i in range(2, len(c.linhas) + 1):
        c.mark(i)
    c.fim()
    return c


def cap14(v):
    c = cap_novo(14, v, setup=assinatura(v), prewarm=['/login', '/dashboard', '/assinatura'])
    c.mark(1)
    rola_ate(c, 'Formas de pagamento', at=0.0, label='a página no valor e nas formas de pagamento', y=300, dur_ms=600, dentro='main', so_se_fora=True)
    c.hover(EM_MAIN('Formas de pagamento', exact=True), 0.5, at=c.A(1, 'Pra', 0.4), label='Formas de pagamento: PIX, Boleto, Cartão')
    rola_ate(c, 'Pagar Agora', at=c.A(1, 'Pagar', 1.7), label='desce a Pagar Agora', y=520 if v == 'd' else 380, dur_ms=700, dentro='main', prefixo=True)
    c.hover(BTNX('Pagar Agora'), 0.8, at=c.A(1, 'Agora:', 0.9), label='botão Pagar Agora (sem clicar)')
    c.mark(2)
    rola_ate(c, 'Débito recorrente ativo no cartão de crédito', at=c.A(2, 'No', 1.4), label='desce à faixa Débito recorrente ativo', y=300, dur_ms=800, dentro='main', prefixo=True)
    c.hover(EM_MAIN('Débito recorrente ativo no cartão de crédito'), 0.8, at=c.A(2, 'repete', 0.9), label='Débito recorrente ativo no cartão de crédito')
    c.mark(3)
    c.mark(4)
    c.mark(5)
    rola_ate(c, 'Economize', at=c.A(5, 'Também', 1.4), label='desce ao cartão Economize por ano', y=330, dur_ms=900, dentro='main', prefixo=True)
    c.hover(EM_MAIN('Mude para o plano anual e pague 12 meses com 20% de desconto (Pix ou Boleto).'), 0.8, at=c.A(5, 'anual:', 0.9), label='Mude para o plano anual (sem zoom no valor)')
    c.mark(6)
    rola_ate(c, 'Histórico de Pagamentos', at=c.A(6, 'No', 2.5), label='desce ao Histórico de Pagamentos', y=130, dur_ms=1300, dentro='main')
    c.marcar(EM_MAIN('Histórico de Pagamentos'), label='Histórico de Pagamentos')
    c.hover(BTNX('Baixar PDF'), 0.5, at=c.A(6, 'PDF', 0.9), label='Baixar PDF do primeiro cartão (sem clicar)')
    c.hover(BTNX('Baixar XML'), 0.5, at=c.A(6, 'XML.', 0.9), label='Baixar XML do primeiro cartão (sem clicar)')
    c.cursor((900, 330) if v == 'd' else (195, 300), at=c.A(6, 'Se', 0.6), label='cursor sai de cima dos botões')
    c.mark(7)
    c.hover(BTNX('Baixar PDF'), 0.8, at=c.A(7, 'nota', 0.9), label='Baixar PDF (a nota da assinatura; sem clicar)')
    c.mark(8)
    rola_ate(c, 'Cancelar assinatura', at=max(0.0, c.L(8) - 2.2), label='sobe a Cancelar assinatura', y=420 if v == 'd' else 380, dur_ms=1200, dentro='main', prefixo=True)
    c.click(BTNX('Cancelar assinatura'), at=c.A(8, 'dia', 0.9), label='Cancelar assinatura (abre a janela; nada é confirmado)')
    c.waitfor(text='Nos ajude a entender o motivo', timeout=10)
    c.click({'role': 'combobox', 'within': DLG}, at=c.A(8, 'cancelar,', 0.6), label='Motivo do cancelamento (abre a lista)')
    c.click({'role': 'option', 'name': 'Dificuldade em usar o sistema'}, at=c.A(8, 'pede', 0.6), label='motivo: Dificuldade em usar o sistema')
    c.click(BTN('Continuar', within=DLG), at=c.A(8, 'mostra', 0.7), label='Continuar (abre Confirmar cancelamento)', **({'noScroll': True} if v == 'p' else {}))
    c.waitfor(text='Ao confirmar:', timeout=8)
    c.hover(TXTX('Você continuará tendo acesso até o vencimento', within=DLG), 0.5, at=c.A(8, 'acesso', 0.9), label='Você continuará tendo acesso até o vencimento')
    c.hover(TXTX('Cobranças em aberto referentes a períodos futuros', within=DLG), 0.5, at=c.A(8, 'cobranças', 0.9), label='Cobranças em aberto de períodos futuros serão canceladas')
    c.hover(TXTX('Você pode reativar a qualquer momento', within=DLG), 0.6, at=c.A(8, 'reativar', 0.9), label='Você pode reativar a qualquer momento')
    c.mark(9)
    c.click(BTN('Voltar', within=DLG), at=c.A(9, 'Antes', 0.9), label='Voltar ao motivo (sem confirmar)', **({'noScroll': True} if v == 'p' else {}))
    c.waitfor(text='Falar com o Sucesso do Cliente', timeout=8)
    c.hover(TXTX('Falar com o Sucesso do Cliente', within=DLG), 1.0, at=c.A(9, 'botão', 0.9), label='Falar com o Sucesso do Cliente (sem clicar)')
    (c.press('Escape', at=c.E(9, 'cancelar.', 0.3), label='fecha a janela sem cancelar') if v == 'p' else c.ev(FECHAR_EVAL, at=c.E(9, 'cancelar.', 0.3), label='fecha a janela sem cancelar'))
    c.confere('main', ['Plano & módulos'], 'a Assinatura continua ativa (Cancelar assinatura ainda na tela)')
    c.fim()
    return c


# ================================================================ cap15 · Recapitulando (S13: o portão já com o vídeo visto)
def cap15(v):
    c = cap_novo(15, v, login_espera='Antes de usar o sistema', prewarm=['/login', '/dashboard', '/ecoflix'])
    ph = v == 'p'
    P = lambda t, **kw: {'text': t, 'within': PORTAO, **kw}
    c.mark(1)
    c.mark(2)
    c.mark(3)
    c.mark(4)
    if ph:
        rola_ate(c, 'Assisti ao vídeo até o final e entendi os combinados.', at=c.A(4, 'Agora', 1.6), label='desce à caixa', y=300, dur_ms=800, dentro=PORTAO)
    c.click(P('Assisti ao vídeo até o final e entendi os combinados.'), at=c.A(4, 'marcar', 1.1), label='caixa Assisti ao vídeo (liga)')
    c.marcar(BTN('Confirmar e começar a primeira aula', within=PORTAO), at=c.A(4, 'clicar', 1.5), label='botão Confirmar e começar a primeira aula')
    c.click(BTN('Confirmar e começar a primeira aula', within=PORTAO), at=c.E(4, 'aula.', 2.3), label='Confirmar e começar a primeira aula', **({'noScroll': True} if ph else {}))
    c.waitfor(text='Tirar dúvidas com o suporte', timeout=25)
    c.mark(5)
    c.fim()
    return c


# ================================================================ cap08 · O Cato, o seu agente (S2; o único com o balão de dica ligado)
BALAO_ESPERA = {'d': 4.7, 'p': 5.3}   # medido no ensaio completo de 18/11 (com 1,5 s o balão subia 1,0 s e 1,5 s depois da frase). s parados no fim do `setup`, depois de recarregar o Dashboard: o balão sobe 15 s depois da tela abrir (CatoFab.tsx)
FAB_CATO = SEL('button[aria-expanded][aria-label*="Cato"]')


def cap08(v):
    recarrega = [{'do': 'goto', 'url': '/dashboard'}, {'do': 'waitFor', 'text': 'Olá, Rafael!', 'timeout': 30}, {'do': 'wait', 'seconds': BALAO_ESPERA[v]}]
    c = cap_novo(8, v, setup=recarrega, prewarm=['/login', '/dashboard'], balao=True)
    c.mark(1)
    c.hover(FAB_CATO, 1.2, at=c.A(1, 'botão', 0.9), label='botão do Cato (Abrir o Cato)', noScroll=True)
    c.mark(2)
    c.waitfor(text='Abrir Cato', timeout=24)
    c.hover(BTNX('Abrir Cato'), 0.9, at=c.A(2, 'balão', 0.9), label='balão de dica do Cato (Abrir Cato)', noScroll=True)
    c.hover(BTN('Fechar dica do Cato'), 0.5, at=c.A(2, 'xis.', 0.9), label='xis Fechar dica do Cato (sem fechar)', noScroll=True)
    c.mark(3)
    c.click(BTNX('Abrir Cato'), at=max(0.0, c.L(3) - 0.5), label='Abrir Cato (no balão): primeira vez do Rafael', noScroll=True, optional=True, timeout=3)
    c.ev("(()=>{if(document.querySelector('[role=dialog]'))return 'ok: janela aberta pelo balão';const b=document.querySelector('button[aria-expanded][aria-label*=\"Cato\"]');"
         "if(!b)return 'SEM ALVO: botão do Cato';b.click();return 'aberta pelo botão (o balão já tinha saído)'})()", label='garante a janela do Cato aberta')
    c.waitfor(text='Antes da primeira conversa com o Cato', timeout=10)
    c.marcar(TXT('Antes da primeira conversa com o Cato'), label='janela Antes da primeira conversa com o Cato')
    c.hover(TXTX('O Cato lê os dados da sua conta', within=DLG), 0.8, at=c.A(3, 'dados', 0.9), label='como o Cato trata os dados')
    c.hover(TXTX('Quer falar em vez de digitar?', within=DLG), 0.8, at=c.A(3, 'escrevendo', 0.9), label='Quer falar em vez de digitar?')
    c.cursor((1000, 420) if v == 'd' else (195, 760), at=c.A(3, 'números', 0.6), label='cursor sai de cima do texto')
    c.mark(4)
    c.ev(FECHAR_EVAL, at=c.A(4, 'Quem', 0.7), label='fecha a janela (sem aceitar: o aceite é da T21)')
    c.hover(FAB_CATO, 1.0, at=c.A(4, 'aula', 0.9), label='botão do Cato de novo', noScroll=True)
    c.fim()
    return c


# ================================================================ cap12 · Montar o plano (S2; nada é aplicado)
def cap12(v):
    c = cap_novo(12, v, setup=assinatura(v), prewarm=['/login', '/dashboard', '/assinatura'])
    ph = v == 'p'
    ym = 260 if not ph else 240
    NA = lambda t, **kw: {'text': t, 'within': DLG, **kw}
    c.mark(1)
    rola_ate(c, 'Plano & módulos', at=0.0, label='desce ao cartão Plano & módulos', y=140, dur_ms=1000, dentro='main')
    rola_ate(c, 'Gerenciar plano', at=c.A(1, 'Clicando', 1.6), label='desce a Gerenciar plano', y=440 if not ph else 380, dur_ms=1000, dentro='main', prefixo=True)
    c.click(BTNX('Gerenciar plano'), at=c.A(1, 'Gerenciar', 1.7), label='Gerenciar plano (abre a janela Montar plano)')
    c.waitfor(text='Monte seu plano e veja como fica ao vivo', timeout=12)
    c.marcar(NA('Monte seu plano e veja como fica ao vivo'), at=c.A(1, 'Montar', 0.3), label='janela Montar plano')
    c.mark(2)
    c.hover(NA('Escolha os módulos', exact=True), 0.5, at=c.A(2, 'módulos,', 0.9), label='Escolha os módulos')
    rola_ate(c, 'Nível de Notas Fiscais', at=c.A(2, 'nível', 1.6), label='a janela desce ao Nível de Notas Fiscais', y=ym, dur_ms=700, dentro=DLG)
    c.hover(NA('Nível de Notas Fiscais', exact=True), 0.5, at=c.A(2, 'nível', 0.9), label='Nível de Notas Fiscais')
    rola_ate(c, 'Usuários adicionais', at=c.A(2, 'usuários', 1.6), label='a janela desce a Usuários adicionais', y=ym + 120, dur_ms=600, dentro=DLG)
    c.hover(NA('Usuários adicionais', exact=True), 0.5, at=c.A(2, 'usuários', 0.9), label='Usuários adicionais: 3 usuários (2 base + 1 extra)')
    if ph:
        rola_ate(c, 'Seu plano', at=c.A(2, 'Do', 1.4), label='a janela desce ao resumo Seu plano', y=160, dur_ms=800, dentro=DLG)
    c.hover(NA('Seu plano', exact=True), 0.8, at=c.A(2, 'resumo', 0.9), label='resumo Seu plano (sem zoom no Total mensal)')
    c.mark(3)
    rola_ate(c, 'Ciclo', at=c.A(3, 'Dá', 0.9), label='o resumo no Ciclo', y=430 if not ph else 420, dur_ms=600, dentro=DLG, so_se_fora=True)
    c.hover(NA('Ciclo', exact=True), 0.8, at=c.A(3, 'mensal', 0.9), label='Ciclo: Mensal / Anual (sem trocar)')
    rola_ate(c, 'Voltar aos planos', at=c.A(3, 'voltar', 1.7), label='a janela volta ao alto', y=140, dur_ms=600, dentro=DLG, so_se_fora=True)
    c.click(BTNX('Voltar aos planos', within=DLG), at=c.A(3, 'voltar', 0.9), label='Voltar aos planos (a lista de planos prontos)')
    c.waitfor(text='Plano Start', timeout=8)
    c.marcar(NA('Plano Master'), label='planos prontos: Start, Avançado, Master e o cartão Personalizado')
    c.mark(4)
    rola_ate(c, 'Personalizado', at=c.A(4, 'Nada', 0.9), label='a lista no cartão Personalizado', y=420, dur_ms=600, dentro=DLG, so_se_fora=True)
    c.click(NA('Escolha módulo por módulo e monte o plano do seu jeito'), at=c.A(4, 'Nada', 0.2), label='cartão Personalizado (volta ao montador com o plano atual)')
    c.waitfor(text='Escolha os módulos', timeout=8)
    rola_ate(c, 'Ver valor e aplicar', at=c.A(4, 'clicar', 1.6), label='a janela desce ao botão Ver valor e aplicar', y=560 if not ph else 640, dur_ms=800, dentro=DLG, prefixo=True, so_se_fora=True)
    c.hover(BTNX('Ver valor e aplicar', within=DLG), 1.0, at=c.A(4, 'Ver', 0.9), label='botão Ver valor e aplicar (sem clicar)')
    c.mark(5)
    (c.press('Escape', at=c.A(5, 'fechou', 0.6), label='fecha a janela sem aplicar') if ph else c.ev(FECHAR_EVAL, at=c.A(5, 'fechou', 0.6), label='fecha a janela sem aplicar'))
    c.confere('main', ['Plano & módulos', 'Gerenciar plano'], 'a Assinatura volta igual')
    c.hover(BTNX('Gerenciar plano'), 0.8, at=c.A(5, 'próxima', 0.9), label='Gerenciar plano de novo (sem abrir)')
    c.fim()
    return c


# ================================================================ variantes: a mesma linha do tempo em outro estado (a edição usa só a linha indicada)
# cap40 = cap10 com a conta em TESTE (linha 2); cap41 = cap11 no S3, sem o CRM (linha 3). O número 40/41 é só o nome do arquivo (o kit do
# ensaio pede um inteiro); a voz é a do capítulo de origem (cópia em rec/t00/_voz/ para o resumo.py).
def cap40(v):
    c = Cap(10, v, setup=vai('/assinatura', 'Ative sua Assinatura'), prewarm=['/login', '/dashboard', '/assinatura'], arq=40, semente=CAT + ['t00/s2', 't00/teste'])
    c.mark(1)
    c.mark(2)
    c.hover(EM_MAIN('Ative sua Assinatura'), 0.8, at=c.A(2, 'período', 0.9), label='Ative sua Assinatura (conta em teste)')
    c.hover(BTNX('Escolher Plano e Ativar'), 1.0, at=c.A(2, 'escolher', 0.9), label='botão Escolher Plano e Ativar (sem clicar)')
    for i in range(3, len(c.linhas) + 1):
        c.mark(i)
    c.fim()
    return c


def cap41(v):
    c = Cap(11, v, setup=assinatura(v), prewarm=['/login', '/dashboard', '/assinatura'], arq=41, semente=S3)
    c.mark(1)
    rola_ate(c, 'Módulos ativos', at=0.0, label='desce a Módulos ativos', y=170, dur_ms=800, dentro='main')
    c.mark(2)
    c.mark(3)
    rola_ate(c, 'Adicione ao seu plano', at=c.A(3, 'Se', 0.9), label='desce a Adicione ao seu plano', y=300 if v == 'd' else 260, dur_ms=800, dentro='main')
    c.hover(EM_MAIN('Adicione ao seu plano', exact=True), 0.6, at=c.A(3, 'Adicione', 0.9), label='Adicione ao seu plano')
    c.hover(BTNX('Ativar meu CRM'), 0.9, at=c.A(3, 'botão', 0.9), label='botão Ativar meu CRM (sem clicar, sem zoom no valor)')
    for i in range(4, len(c.linhas) + 1):
        c.mark(i)
    c.fim()
    return c


VARIANTES = {40: 10, 41: 11}   # arquivo -> capítulo da voz
CAPS_ROBO = {n: globals()[f'cap{n:02d}'] for n in list(range(16)) + sorted(VARIANTES)}


def main():
    args = sys.argv[1:]
    versoes = ['d', 'p']
    if '--so-d' in args:
        versoes = ['d']
    if '--so-p' in args:
        versoes = ['p']
    quais = [int(a) for a in args if a.isdigit()] or sorted(CAPS_ROBO)
    for n in quais:
        for v in versoes:
            c = CAPS_ROBO[n](v)
            if n in VARIANTES:   # o resumo.py procura a voz pelo número do arquivo
                os.makedirs(os.path.join(HERE, '_voz'), exist_ok=True)
                with open(os.path.join(NARR, f'cap{VARIANTES[n]:02d}.json'), encoding='utf8') as f_in, open(os.path.join(HERE, '_voz', f'cap{n:02d}.json'), 'w', encoding='utf8') as f_out:
                    f_out.write(f_in.read())
            if os.environ.get('ANCHORS'):
                for i, w, t in c.anchors:
                    print(f'   anchor L{i} "{w}" -> {t}')
            d = c.out()
            last = -1
            for stp in d['steps']:
                if 'at' in stp:
                    if stp['at'] < last:
                        print(f'  aviso cap{n:02d}{v}: at {stp["at"]} < {last} em "{stp.get("label") or stp.get("name")}"')
                    last = max(last, stp['at'])
            path = os.path.join(HERE, f'cap{n:02d}.json' if v == 'd' else f'cap{n:02d}.9x16.json')
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(d, f, ensure_ascii=False, indent=1)
            if '--ens' in args:   # ensaio rápido: sem os `at` nem as marcas, cauda curta (rec/t00/_ens/)
                e = dict(d, steps=[{k: x for k, x in st.items() if k != 'at'} for st in d['steps'] if st.get('do') != 'mark'], tail=0.4)
                os.makedirs(os.path.join(HERE, '_ens'), exist_ok=True)
                with open(os.path.join(HERE, '_ens', os.path.basename(path)), 'w', encoding='utf-8') as f:
                    json.dump(e, f, ensure_ascii=False, indent=1)
            amb = f' (palavras ambíguas: {len(c.ambiguas)})' if c.ambiguas else ''
            print(f'cap{n:02d}{"" if v == "d" else ".9x16"}: {len(d["steps"])} passos, narração {c.dur:.1f} s{" ESTIMADA" if c.estimada else ""}{amb} -> {os.path.relpath(path, HERE)}')


if __name__ == '__main__':
    main()
