#!/usr/bin/env python3
"""T17 · Transporte, serviço e o contador: gera rec/t17/cap00..cap20.json (roteiros do robô) a partir da voz (t17/narracao/capNN.json).

EcoSistema 1.60.39 desde 28/11 (era 1.60.18; andamento_160.md, seção "28/11 · 1.60.39") no Supabase falso (mundo da Recicla Vale Metais), computador 1280x800, logado como Rafael Nogueira (MASTER).
Cada passo é preso a uma palavra da fala: `at` = início da palavra - folga (o custo do gesto, docs/04 "Custo real dos gestos"), e a marca
Ln entra no início de cada linha. Quando a voz chegar, rodar de novo com o capNN.json da voz (nada a reescrever).
Rodar de qualquer pasta: `python3 -I rec/t17/gerar.py [NN ...]`; ensaiar/gravar: `bash rec/t17/t17_grava.sh NN [--rapido]`.

Relógio: FAKE_NOW 10/11/2026 09:30 nos capítulos 0 a 4 (as NF-e 1255 e 1256 saíram às 09:05 e 09:12; o caminhão sai às 09:40),
14:20 do 5 ao 9 (a carga já foi entregue em Itamonte) e 14:40 do 10 em diante (as NFS-e recebidas chegaram às 14:24).
Cadeia de sementes (rec/mundo/seeds-extra/t17; inicio e as laterais = t17_sementes.py; as outras saem de t17_semente.py, do estado da
instância 54317 logo depois do ensaio do capítulo, cumulativas; reserva sem navegador: t17_semente_api.py): inicio -> apos-cap02
(FKD2E41 e Edson completos) -> apos-cap04 (MDF-e nº 1 autorizado) -> apos-cap05 (encerrado) -> apos-cap08 (NFS-e 14 autorizada) ->
apos-cap09 (NFS-e recebidas ativado) -> [+ lateral nfse-recebidas] apos-cap10 (conta da Balanças Tremembé) -> apos-cap14 (saldo
inicial fiscal da bateria: capítulo 14 desde 28/11, semente apos-cap14, era apos-cap13). Lateral mdfe2-rejeitado: só nos
capítulos 6 e 20; lateral compra-coop (o caixa #85 do Rafael aberto): só no 11 (1.60.39: a NF-e recebida da Cooperativa vira compra).
Os capítulos 12, 13 e 15 a 18 só leem; o 19 é só ilustração e o 20 é a montagem (o robô deixa uma tela parada com as marcas).
"""
import hashlib
import json
import os
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TUT = os.path.normpath(os.path.join(HERE, '..', '..'))
NARR = os.path.join(TUT, 't17', 'narracao')
N0930 = '2026-11-10T09:30:00-03:00'
N1420 = '2026-11-10T14:20:00-03:00'
N1440 = '2026-11-10T14:40:00-03:00'
FAKE_NOW = {n: (N0930 if n <= 4 else N1420 if n <= 9 else N1440) for n in range(21)}


def stable_id(chave):
    """o mesmo UUID estável do Supabase falso (core/util.mjs stableId)"""
    h = bytearray(hashlib.sha1(('domiflix-fake:' + chave).encode()).digest())
    h[6] = (h[6] & 0x0F) | 0x50
    h[8] = (h[8] & 0x3F) | 0x80
    x = h[:16].hex()
    return f'{x[:8]}-{x[8:12]}-{x[12:16]}-{x[16:20]}-{x[20:32]}'


RAFAEL = stable_id('user.rafael')
try:
    VERSAO = open(os.path.join(TUT, 'app', 'dist', '.versao-app'), encoding='utf8').read().strip() or '1.60.39'
except OSError:
    VERSAO = '1.60.39'
HOJE = '2026-11-10'
STORAGE = {
    'app_version': VERSAO, 'notification_shown_version': VERSAO, f'dominex:daily-tasks-shown:{RAFAEL}': HOJE,
    # o balão de dica do Cato fica calado (JUNCAO_160.md, regra do mundo: só a T00 e a T21 mostram)
    'cato_adoption_nudge_38814e47-876a-5977-a5f7-53af364c17bb_' + RAFAEL: '{"count":99,"lastShownAt":4102444800000}',
    'pwa-install-dismissed': 'true', 'theme': 'light', f'daily-tasks-reminder-last-shown-{RAFAEL}': HOJE, 'initial-preferences-set': 'true',
}
NOMES = ['Abertura', 'O que é o MDF-e', 'Veículo e motorista', 'Numeração e percurso', 'Emitir o manifesto', 'Encerrar no fim da viagem',
         'Quando o manifesto não passa', 'A nota de serviço', 'Emitir e acompanhar', 'O serviço que você tomou', 'Da nota recebida à despesa',
         'Da nota recebida à compra', 'Entrada, saída e saldo', 'O estoque pelas notas', 'O saldo inicial', 'Um dia do passado e as movimentações',
         'Cancelamento e devolução', 'Fiscal e operacional', 'O pacote do mês', 'O que o contador faz', 'Recapitulando']
# 28/11 (1.60.39): o capítulo 11 é novo (a NF-e recebida vira compra) e os de 11 a 19 viraram 12 a 20. A semente do saldo inicial
# (capítulo 14, era o 13) virou apos-cap14 (o arquivo foi renomeado); o 11 não deixa semente (os seguintes não veem a compra).
SEMENTE = {0: None, 1: None, 2: None, 3: 'apos-cap02', 4: 'apos-cap02', 5: 'apos-cap04', 6: 'apos-cap05', 7: 'apos-cap05', 8: 'apos-cap05',
           9: 'apos-cap08', 10: 'apos-cap09', 11: 'apos-cap10', 12: 'apos-cap10', 13: 'apos-cap10', 14: 'apos-cap10', 15: 'apos-cap14',
           16: 'apos-cap14', 17: 'apos-cap14', 18: 'apos-cap14', 19: 'apos-cap14', 20: 'apos-cap14'}
LATERAL = {6: 'mdfe2-rejeitado', 10: 'nfse-recebidas', 11: 'compra-coop', 20: 'mdfe2-rejeitado'}   # sementes que não seguem na cadeia


def sementes(n):
    """a semente de cada capítulo é cumulativa (tudo desde o início da aula): só a última da cadeia vai junto do início (+ a lateral)"""
    return ['t17/inicio'] + ([f't17/{SEMENTE[n]}'] if SEMENTE[n] else []) + ([f't17/{LATERAL[n]}'] if n in LATERAL else [])


def chave_884():
    """a chave de acesso da NF-e 884 do Depósito Irmãos Siqueira (Notas Recebidas), como está na semente t17/inicio"""
    d = json.load(open(os.path.join(TUT, 'rec', 'mundo', 'seeds-extra', 't17', 'inicio.json'), encoding='utf8'))
    return next(n['chave'] for n in d['inbound_nfe'] if str(n['numero']) == '884')


def norm(s):
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode().lower()
    return ''.join(ch for ch in s if ch.isalnum() or ch in '?')


def carregar_voz(n):
    d = json.load(open(os.path.join(NARR, f'cap{n:02d}.json'), encoding='utf8'))
    return d['words'], d['linhas'], float(d['dur']), bool(d.get('estimado'))


# Observador de avisos de erro na tela (aceite): "Não foi possível", "Erro ao", "Tente novamente", "indisponível", "Algo deu errado",
# "Falha ao", "não encontrad" e a faixa "Lembrete da trilha" da EcoFlix. O passo final devolve a lista (tem de sair vazia).
OBS = ("(()=>{window.__avisos=[];const re=/N[ãa]o foi poss[ií]vel|Erro ao|Tente novamente|indispon[ií]vel|Algo deu errado|Falha ao|"
       "n[ãa]o encontrad|recusou|rejeitad[ao]!/i;"
       "const chk=(t)=>{t=(t||'').trim();const m=t&&t.match(new RegExp('[^]{0,40}('+re.source+')[^]{0,40}','i'));"
       "if(m&&window.__avisos.length<10)window.__avisos.push(m[0].replace(/[\\n\\r\\t ]+/g,' '))};new MutationObserver(ms=>{for(const m of ms){"
       "m.addedNodes.forEach(n=>chk(n.textContent));if(m.type==='characterData')chk(m.target.textContent)}}).observe(document.body,"
       "{childList:true,subtree:true,characterData:true});chk(document.body.innerText);"
       "setInterval(()=>{const f=document.querySelector('section[aria-label^=\"Lembrete da trilha\"]');"
       "if(f&&window.__avisos.length<10&&!window.__avisos.includes('TRILHA ECOFLIX'))window.__avisos.push('TRILHA ECOFLIX')},300);return 1})()")

# Animação do framer-motion presa no futuro pelo relógio simulado (08-licoes, T5 cap. 10): a cada 100 ms, a animação presa começa agora.
ANIM_FIX = ("(()=>{if(window.__animFix)return 'ja';window.__animFix=setInterval(()=>{for(const a of document.getAnimations())"
            "if(a.currentTime!==null&&a.currentTime<0)a.startTime=document.timeline.currentTime},100);return 'anim fix'})()")


class Cap:
    def __init__(s, n, pace=0.5, cps=9, start=(900, 440), setup=None, noscroll=False, obs=True):
        s.n = n
        s.words, s.linhas, s.dur, s.estimada = carregar_voz(n)
        s.steps = []
        s.pace, s.cps, s.start = pace, cps, start
        s.noscroll = noscroll
        s.obs = obs   # obs=False: capítulo que MOSTRA um erro de propósito (o roteiro pede)
        s.setup = list(setup or []) + ([{'do': 'eval', 'js': OBS}] if obs else []) + [{'do': 'eval', 'js': ANIM_FIX}]
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
            # gesto que começaria até 0,8 s antes da marca de uma linha começa NA marca: a marca sai na hora (o gesto chega na 1ª palavra)
            lim = 0.8 if d.get('do') in ('hover', 'click', 'scroll') else 0.25
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

    def marca_ja(s, i):
        """marca a linha e a solta já (antes de passos sem `at`)"""
        s.mark(i)
        s.flush(1e9)

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

    def hover(s, target, seconds=0.3, at=None, label=None, **kw):
        """hover curto; se atravessa o início de uma linha já pendente, sai partido em dois (a marca entra no meio)"""
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

    def type(s, target, text, at=None, label=None, cps=None, **kw):
        d = {'do': 'type', 'target': target, 'text': text}
        if cps:
            d['cps'] = cps
        return s._p(d, at, label, kw)

    def digita(s, campo, texto, at_clique, at_texto, label, clique_label=None, **kw):
        """clica no campo (cursor chega na palavra) e digita sem esperar (noClick, cps 40)"""
        s.click(campo, at=at_clique, label=clique_label or f'{label} (campo)')
        return s.type(campo, texto, at=at_texto, label=label, cps=40, noClick=True, **kw)

    def colar(s, seletor, texto, at=None, label=None):
        """texto longo sem graça visual: entra de uma vez (execCommand insertText, ~0,05 s; o valor fica no actions.json)"""
        js = ("(()=>{const el=document.querySelector(%s);if(!el)return 'SEM ALVO';el.focus();el.select&&el.select();"
              "document.execCommand('insertText',false,%s);return 'colado: '+el.value.slice(0,60)})()") % (json.dumps(seletor), json.dumps(texto, ensure_ascii=False))
        return s.ev(js, at=at, label=label)

    def press(s, key, at=None, label=None, **kw):
        return s._p({'do': 'press', 'key': key}, at, label, kw)

    def rolar(s, by, at=None, label=None, ponto=(900, 440), duration=0.5, after=100):
        return s._p({'do': 'scroll', 'point': {'x': ponto[0], 'y': ponto[1]}, 'by': by, 'duration': duration, 'after': after}, at, label, {})

    def cursor(s, ponto, at=None, label=None):
        """leva o cursor a um ponto neutro (scroll de 0 px): tira o mouse de cima de um menu ou de um cartão"""
        return s._p({'do': 'scroll', 'point': {'x': ponto[0], 'y': ponto[1]}, 'by': 0, 'duration': 0.3, 'after': 0}, at, label, {})

    def registra(s, target, at=None, label=None):
        """registra o retângulo do alvo para a câmera (zoom/destaque) SEM mexer o mouse"""
        return s._p({'do': 'type', 'target': target, 'text': '', 'noClick': True, 'optional': True, 'timeout': 4}, at, label, {})

    def clicar_fixo(s, alvo, ponto, js, at, label):
        """Botão FIXO fora da faixa y 96..730: leva o cursor com `scroll by 0 point`, registra o retângulo do `alvo` e clica por `eval`."""
        s._p({'do': 'scroll', 'point': {'x': ponto[0], 'y': ponto[1]}, 'by': 0, 'duration': 0.3, 'after': 0}, round(max(0.0, at - 0.6), 2), label + ' (cursor)', {})
        s.add({'do': 'type', 'target': alvo, 'text': '', 'noClick': True, 'label': label, 'optional': True, 'timeout': 4})
        return s._p({'do': 'eval', 'js': js}, round(at, 2), label + ' (clique)', {})

    def pause(s, seconds):
        return s.add({'do': 'pause', 'seconds': seconds})

    def wait(s, seconds):
        return s.add({'do': 'wait', 'seconds': seconds})

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

    def fim(s):
        s.flush(1e9)
        if s.obs:
            s.steps.append({'do': 'eval', 'js': 'JSON.stringify(window.__avisos || "sem observador")', 'label': 'avisos de erro na tela'})
        s.steps.append({'do': 'mark', 'name': 'FIM', 'at': round(s.dur, 2)})

    def out(s):
        return {
            'name': f't17-cap{s.n:02d}',
            'title': f'T17 · Cap. {s.n} · {NOMES[s.n]} (narração {str(round(s.dur, 1)).replace(".", ",")} s{" ESTIMADA" if s.estimada else ""}; '
                     f'marcas L1..L{len(s.linhas)} = início de cada linha do roteiro; FAKE_NOW {FAKE_NOW[s.n]})',
            'seed': f't17-cap{s.n:02d}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
            'start': {'x': s.start[0], 'y': s.start[1]},
            'anonymous': True, 'storage': dict(STORAGE),
            'seedExtra': sementes(s.n),
            'prewarm': ['/login'], 'setup': s.setup, 'steps': s.steps,
        }


# ---------------------------------------------------------------- alvos
BTN = lambda n, **kw: {'role': 'button', 'name': n, 'exact': True, **kw}
BTNX = lambda n, **kw: {'role': 'button', 'name': n, **kw}
LINK = lambda n, **kw: {'role': 'link', 'name': n, 'exact': True, **kw}
TAB = lambda n, **kw: {'role': 'tab', 'name': n, 'exact': True, **kw}
TXT = lambda t, **kw: {'text': t, 'exact': True, **kw}
TXTX = lambda t, **kw: {'text': t, **kw}
SEL = lambda s, **kw: {'selector': s, **kw}
OPT = lambda n, **kw: {'role': 'option', 'name': n, 'exact': True, **kw}
OPTX = lambda n, **kw: {'role': 'option', 'name': n, **kw}
ITEM = lambda n, **kw: {'role': 'menuitem', 'name': n, **kw}
PH = lambda p, **kw: {'placeholder': p, **kw}
DLG = '[role=dialog]'
MENU = 'aside, [data-sidebar=sidebar]'
GRUPO = BTNX('Fiscal & Ambiental', within=MENU)
ITEM_MENU = lambda n: LINK(n, within=MENU)


def js_clicar(sel, texto=None):
    """clique por eval (botão fixo): o primeiro `sel` visível (com o texto, se dado)"""
    filtro = f"&&(b.textContent||'').includes({json.dumps(texto, ensure_ascii=False)})" if texto else ''
    return (f"(()=>{{const b=[...document.querySelectorAll({json.dumps(sel)})].find(b=>b.offsetParent!==null{filtro});"
            "if(!b)return 'SEM ALVO';b.click();return 'clicado'})()")


# ---------------------------------------------------------------- setup (fora do vídeo)
LOGIN = [
    {'do': 'waitFor', 'target': PH('seu@email.com'), 'timeout': 40},
    {'do': 'type', 'target': PH('seu@email.com'), 'text': '$TUT_USER', 'cps': 40},
    {'do': 'type', 'target': PH('••••••••'), 'text': '$TUT_SENHA', 'cps': 40},
    {'do': 'click', 'target': BTN('Entrar')},
    {'do': 'waitFor', 'url': '/dashboard', 'timeout': 40},
    {'do': 'waitFor', 'idle': True, 'timeout': 25},
]
PAGINAS = {
    '/dashboard': None,
    '/fiscal-ambiental/transporte': 'Manifesto Eletrônico de Documentos Fiscais (MDF-e)',
    '/fiscal-ambiental/transporte/frota': 'Frota (veículos e motoristas do MDF-e)',
    '/fiscal-ambiental/nfse': 'Nota Fiscal de Serviço (NFS-e)',
    '/fiscal-ambiental/nfe/saida': 'Notas Recebidas',
    '/fiscal-ambiental/nfe/recebidas-nfse': 'Notas Recebidas',
    '/fiscal-ambiental/nfe/recebidas': 'Notas emitidas contra o seu CNPJ',
    '/fiscal-ambiental/estoque-fiscal/relatorio-nfe': 'Pendentes + Rejeitadas',   # 1.60.15+: Relatório/Estoque Fiscal, aba NF-e
    '/compra': 'Voltar para o caixa',
    '/fiscal-ambiental/estoque-fiscal/posicao': 'Saldo fiscal atualizado, por material.',
}


def ir(rota, espera=0.8):
    st = [{'do': 'goto', 'url': rota}]
    if PAGINAS.get(rota):
        st.append({'do': 'waitFor', 'text': PAGINAS[rota], 'timeout': 30})
    return st + [{'do': 'waitFor', 'idle': True, 'timeout': 25}, {'do': 'wait', 'seconds': espera}]


def setup_em(rota, extra=(), aquece=(), menu=None):
    """login, aquece as rotas que o capítulo visita e para em `rota`; `menu` = item do grupo Fiscal & Ambiental que o capítulo clica
    (no 1.60.18 o grupo abre fechado mesmo nas páginas fiscais: o setup o deixa aberto antes de gravar)"""
    st = list(LOGIN)
    for r in aquece:
        st += ir(r, 0.3)
    abre = [{'do': 'eval', 'js': js_abrir_grupo('Fiscal & Ambiental', menu)}, {'do': 'wait', 'seconds': 0.8}] if menu else []
    return st + ir(rota) + abre + list(extra)


def js_abrir_grupo(grupo, filho):
    """abre o grupo do menu lateral só se o link filho ainda não está no DOM (o grupo da página atual já vem aberto)"""
    return (f"(()=>{{const tem=[...document.querySelectorAll('aside a, [data-sidebar=sidebar] a')].some(a=>a.textContent.trim()==={json.dumps(filho, ensure_ascii=False)});"
            f"if(tem)return 'ja aberto';const b=[...document.querySelectorAll('aside button, [data-sidebar=sidebar] button')].find(b=>b.textContent.trim()==={json.dumps(grupo, ensure_ascii=False)});"
            "if(!b)return 'SEM ALVO';b.click();return 'aberto'})()")


# rolagem suave do contêiner que rola o alvo (molde do T14/T11/T8/T12: ACHA_ROLAGEM + SUAVE): o cursor não se mexe
ACHA_ROLAGEM = ("const rolagem=(el)=>{let c=el&&el.parentElement;while(c&&c!==document.body){const s=getComputedStyle(c);"
                "if(/(auto|scroll)/.test(s.overflowY)&&c.scrollHeight>c.clientHeight+4)return c;c=c.parentElement;}"
                "const se=document.scrollingElement;return se&&se.scrollHeight>se.clientHeight+4?se:null};")
SUAVE = ("await new Promise(res=>{const f=t=>{const p=Math.min(1,(t-t0)/DUR),e=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;c.scrollTo({top:DESTINO,behavior:'instant'});"
         "p<1?requestAnimationFrame(f):res()};requestAnimationFrame(f)});")


def js_ate(texto, y=250, dur_ms=900, escopo='main', prefixo=False):
    """rola (suave) o contêiner do alvo até a folha do DOM cujo texto é `texto` ficar em y px CSS. Devolve o topo final do alvo,
    'ok' (já estava lá), 'SEM ALVO' ou 'SEM ROLAGEM'."""
    alvo = json.dumps(texto, ensure_ascii=False)
    sel = json.dumps(f'{escopo} *')
    busca = (f"[...document.querySelectorAll({sel})].filter(e=>e.offsetParent!==null&&e.textContent.trim().startsWith({alvo})).sort((a,b)=>a.textContent.length-b.textContent.length)[0]"
             if prefixo else f"[...document.querySelectorAll({sel})].find(e=>e.children.length===0&&e.offsetParent!==null&&e.textContent.trim()==={alvo})")
    return ("(async()=>{" + ACHA_ROLAGEM + "const el=" + busca + ";if(!el)return 'SEM ALVO';const c=rolagem(el);if(!c)return 'SEM ROLAGEM';"
            f"const dy=Math.round(el.getBoundingClientRect().top-{int(y)});if(Math.abs(dy)<3)return 'ok';const y0=c.scrollTop,t0=performance.now();"
            + SUAVE.replace('DUR', str(int(dur_ms))).replace('DESTINO', 'y0+dy*e') +
            "return Math.round(el.getBoundingClientRect().top)})()")


def rola_ate(c, texto, at, label, y=250, dur_ms=900, escopo='main', prefixo=False):
    return c.ev(js_ate(texto, y, dur_ms, escopo, prefixo), at=at, label=label)


# ================================================================ capítulos
CAPS_ROBO = {}


def capitulo(fn):
    CAPS_ROBO[int(fn.__name__[3:])] = fn
    return fn


# ---------------------------------------------------------------- alvos das telas fiscais (conferidos por exploração, rec/t17/_ex)
NAV = "[aria-label='Navegação da seção']"   # 1.60.39: div role=navigation (HorizontalScrollArrows), não é mais <nav>
SUBABA = lambda n: BTN(n, within=NAV)                                                  # sub-abas (Manifestos/Frota, Entrada/Saída...)
NEUTRO = (900, 470)                                                                    # ponto neutro (fora de menu, cartão e botão)
CARTAO = lambda t: TXT(t, within='main')
LINHA = lambda txt, sub='': SEL(f"main tbody tr:has-text('{txt}') {sub}".strip())
VEIC = lambda placa: SEL(f"main button:has-text('{placa}'):not([aria-label])")         # item da lista "Veículos da frota"


def escolhe(c, gatilho, opcao, at_g, at_o, label, teclas=None, fixo=False):
    """Select do Radix: clica o gatilho (cursor) e a opção; com `teclas`, escolhe pelo teclado (busca por digitação + Enter) quando a
    opção fica fora da parte visível da lista (o robô rolaria a lista ~2,5 s). `fixo`: gatilho fora da faixa y 96..730 (noScroll)."""
    c.click(gatilho, at=at_g, label=f'{label} (abre)', **({'noScroll': True} if fixo else {}))
    if teclas:
        for i, k in enumerate(teclas):
            c.press(k, at=round(at_o + 0.12 * i, 2) if i == 0 else None, label=label if i == 0 else None)
        return c.press('Enter', label=f'{label} (Enter)')
    return c.click(opcao if isinstance(opcao, dict) else OPT(opcao), at=at_o, label=label)


@capitulo
def cap00():
    """Abertura: ilustração sobre o Dashboard; depois o menu Fiscal & Ambiental com Transporte, Notas de Serviço e Relatório/Estoque Fiscal
    (uma tela só desde o 1.60.15)."""
    c = Cap(0, start=(760, 430), setup=setup_em('/dashboard'))
    c.mark(1)
    c.cursor((760, 440), at=0.5, label='cursor em repouso no Dashboard')
    c.marca_ja(2)
    c.mark(3)
    c.click(GRUPO, at=c.A(3, 'Fiscal', 0.8), label='abre Fiscal & Ambiental', unless=ITEM_MENU('Transporte (MDF-e)'))
    c.hover(ITEM_MENU('Transporte (MDF-e)'), 0.4, at=c.A(3, 'Transporte,', 0.6), label='Transporte (MDF-e)')
    c.hover(ITEM_MENU('Notas de Serviço (NFS-e)'), 0.4, at=c.A(3, 'Notas', 0.6), label='Notas de Serviço (NFS-e)')
    c.hover(ITEM_MENU('Relatório/Estoque Fiscal'), 1.0, at=c.A(3, 'Relatório', 0.6), label='Relatório/Estoque Fiscal (uma tela só)')
    c.mark(4)
    c.cursor((760, 460), at=c.L(4) - 0.2, label='cursor sai do menu (cartão do módulo)')
    c.marca_ja(5)
    c.fim()
    return c


@capitulo
def cap01():
    """O que é o MDF-e: Transporte > Manifestos vazio, as ilustrações (L2, L3), os quatro cartões e a dica."""
    c = Cap(1, start=(700, 430), setup=setup_em('/dashboard', extra=[{'do': 'eval', 'js': js_abrir_grupo('Fiscal & Ambiental', 'Transporte (MDF-e)')},
                                                                       {'do': 'wait', 'seconds': 0.8}], aquece=['/fiscal-ambiental/transporte']))
    c.mark(1)
    c.click(ITEM_MENU('Transporte (MDF-e)'), at=c.A(1, 'aqui,', 0.9), label='Transporte (MDF-e) no menu')
    c.waitfor(text=PAGINAS['/fiscal-ambiental/transporte'], timeout=15)
    c.hover(SUBABA('Manifestos'), 0.4, at=c.A(1, 'Manifestos.', 0.6), label='aba Manifestos')
    c.hover(TXT('Nenhum MDF-e encontrado'), 0.8, at=c.A(1, 'nenhum.', 0.6), label='lista vazia: Nenhum MDF-e encontrado')
    c.mark(2)
    c.cursor(NEUTRO, at=c.L(2) - 0.2, label='cursor em repouso (ilustração do manifesto)')
    c.marca_ja(3)
    c.mark(4)
    c.registra(CARTAO('MDF-e Pendentes'), at=c.A(4, 'cartões', 0.4), label='cartões do MDF-e (zoom)')
    c.hover(CARTAO('MDF-e Autorizados'), 0.2, at=c.A(4, 'autorizados,', 0.6), label='MDF-e Autorizados')
    c.hover(CARTAO('MDF-e Rejeitados'), 0.2, at=c.A(4, 'rejeitados', 0.6), label='MDF-e Rejeitados')
    c.hover(CARTAO('MDF-e Encerrados'), 0.4, at=c.A(4, 'encerrados.', 0.6), label='MDF-e Encerrados')
    c.mark(5)
    c.cursor(NEUTRO, at=c.L(5) - 0.2, label='câmera volta à tela inteira (dica)')
    c.fim()
    return c


@capitulo
def cap02():
    """Frota: o FKD2E41 ganha os dados de transporte e o Edson Moura, CPF, CNH e categoria."""
    c = Cap(2, start=(900, 440), setup=setup_em('/fiscal-ambiental/transporte', aquece=['/fiscal-ambiental/transporte/frota']))
    c.mark(1)
    c.click(SUBABA('Frota'), at=c.A(1, 'Frota.', 0.8), label='aba Frota')
    c.waitfor(text=PAGINAS['/fiscal-ambiental/transporte/frota'], timeout=15)
    # a lista abre com o primeiro da ordem (EZR4C63, Picape) no painel: o caminhão truck é escolhido na lista
    c.click(VEIC('FKD2E41'), at=c.A(1, 'caminhões', 0.7), label='FKD2E41 (Caminhão truck) na lista')
    c.hover(TXT('Mesma frota usada na pesagem de compra/venda.'), 0.6, at=c.A(1, 'pesagem.', 0.6), label='mesma frota da pesagem')
    c.mark(2)
    c.hover(TXT('Dados de transporte', within='main section'), 0.4, at=c.A(2, 'transporte', 0.6), label='painel: Dados de transporte')
    c.click(BTN('Editar', within='main'), at=c.A(2, 'Editar.', 0.7), label='Editar o FKD2E41')
    c.waitfor(text='Editar veículo', timeout=10)
    c.mark(3)
    rola_ate(c, 'Dados de transporte (MDF-e / NF-e)', round(max(c.L(3) - 0.2, c.W(2, 'Editar.') + 0.9), 2), 'janela desce até Dados de transporte', y=110, escopo=DLG)
    escolhe(c, SEL('#veiculo-uf'), 'SP', c.A(3, 'São', 0.9), c.A(3, 'Paulo.', 0.2), 'UF de licenciamento: SP', teclas=['S', 'P'])
    escolhe(c, SEL('#veiculo-categoria'), OPTX('Veículo único'), c.A(3, 'Tipo,', 0.6), c.A(3, 'único,', 0.4), 'Tipo: Veículo único')
    escolhe(c, SEL('#veiculo-rodado'), 'Truck', c.A(3, 'rodado', 0.6), c.A(3, 'truck,', 0.3), 'Tipo de rodado: Truck')
    escolhe(c, SEL('#veiculo-carroceria'), 'Aberta', c.A(3, 'carroceria', 0.6), c.A(3, 'aberta.', 0.3), 'Tipo de carroceria: Aberta')
    c.mark(4)
    c.hover(SEL('#veiculo-tara'), 0.8, at=c.A(4, 'tara,', 0.6), label='Tara (kg)')
    c.hover(SEL('#veiculo-cap-kg'), 0.8, at=c.A(4, 'catorze', 0.6), label='Capacidade (kg)')
    c.mark(5)
    c.digita(SEL('#veiculo-cap-m3'), '30', c.A(5, 'peso', 0.7), c.A(5, 'quilos.', 0.05), 'Capacidade (m³): 30')
    c.hover(TXTX('máx. 999 m³', within=DLG), 0.4, at=c.A(5, 'tonelada,', 0.9), label='ajuda: máx. 999 m³')
    c.mark(6)
    c.click(BTN('Salvar', within=DLG), at=c.A(6, 'Salvar,', 0.7), label='Salvar o veículo')
    c.waitfor(text='Veículo atualizado', timeout=10)
    c.hover(TXT('Dados de transporte', within='main section'), 0.6, at=c.A(6, 'pronto', 0.5), label='painel: Dados de transporte preenchido')
    c.mark(7)
    c.click(TAB('Motoristas'), at=c.A(7, 'motorista.', 0.8), label='aba Motoristas')
    # o nome na lista fica ao lado do "⋯" da linha (menu que abre ao passar o mouse e tranca a página): o cursor vai ao painel
    PAINEL = "main section[aria-label='Detalhes de Edson Moura']"
    c.hover(SEL(f'{PAINEL} h2'), 0.4, at=c.A(7, 'Edson', 0.6), label='Edson Moura (já na lista)')
    c.click(SEL(f'{PAINEL} button', hasText='Editar'), at=c.A(7, 'Editar.', 0.7), label='Editar o Edson')
    c.waitfor(text='Editar motorista', timeout=10)
    c.mark(8)
    # CPF e CNH entram colados (11 dígitos cada, o valor aparece de uma vez); o foco da data entra pelo rótulo (o dia primeiro)
    c.click(SEL('#motorista-doc'), at=c.A(8, 'CPF', 0.9), label='CPF (campo)')
    c.colar('#motorista-doc', '31847265090', at=c.A(8, 'CPF', -0.05), label='CPF: 318.472.650-90')
    c.click(SEL('#motorista-cnh'), at=c.A(8, 'então', 0.7), label='CNH (campo)')
    c.colar('#motorista-cnh', '04728193604', at=c.A(8, 'completo', 0.6), label='CNH: 04728193604')
    escolhe(c, SEL('#motorista-cnh-cat'), 'C', c.A(8, 'CNH,', 0.3), c.A(8, 'categoria', 0.3), 'Categoria: C')
    c.click(SEL("[role=dialog] label[for='motorista-cnh-val']"), at=c.A(8, 'validade.', 0.8), label='Validade da CNH (campo)')
    c.type(SEL('#motorista-cnh-val'), '18032029', at=c.A(8, 'validade.', 0.1), label='Validade da CNH: 18/03/2029', cps=40, noClick=True)
    c.mark(9)
    c.click(BTN('Salvar', within=DLG), at=c.A(9, 'Salvar.', 0.2), label='Salvar o motorista')
    c.waitfor(text='Motorista atualizado', timeout=10)
    c.hover(TXT('Carteira de habilitação', within='main section'), 0.8, at=c.A(9, 'motorista', 0.4), label='painel: Carteira de habilitação')
    c.fim()
    return c


@capitulo
def cap03():
    """Configurações do MDF-e: série 1, próximo 1; a ponte para a Frota; o percurso é ilustração (L4 a L6)."""
    c = Cap(3, start=(900, 440), setup=setup_em('/fiscal-ambiental/transporte/frota', aquece=['/fiscal-ambiental/transporte']))
    c.mark(1)
    c.click(SUBABA('Manifestos'), at=c.A(1, 'frota', 0.6), label='aba Manifestos')
    c.waitfor(text='Nenhum MDF-e encontrado', timeout=15)
    c.click(BTN('Configurações do MDF-e'), at=c.A(1, 'Configurações', 0.8), label='Configurações do MDF-e')
    c.waitfor(text='Útil quando a empresa já emitiu MDF-e em outro sistema.', timeout=10)
    c.hover(TXT('Próximo MDF-e', within=DLG), 0.8, at=c.A(1, 'série', 0.6), label='quadro Série / Próximo MDF-e')
    c.mark(2)
    c.hover(TXTX('Próximo Número', within=DLG), 0.6, at=c.A(2, 'um.', 0.6), label='Próximo Número: 1')
    c.hover(TXTX('Útil quando a empresa já emitiu MDF-e', within=DLG), 0.8, at=c.A(2, 'sistema,', 0.6), label='série e próximo número (outro sistema)')
    c.mark(3)
    c.hover(BTN('Ir para Frota', within=DLG), 0.6, at=c.A(3, 'Frota,', 0.6), label='Motoristas e veículos ficam na Frota')
    c.press('Escape', at=c.A(3, 'ver.', -0.2), label='fecha a janela')
    c.mark(4)
    c.cursor(NEUTRO, at=c.L(4) - 0.2, label='cursor em repouso (ilustração do percurso)')
    c.marca_ja(5)
    c.marca_ja(6)
    c.fim()
    return c


ORIGEM = "[role=dialog] div.rounded-xl:has(p:text-is('Carregamento (Origem)'))"
DESTINO = "[role=dialog] div.rounded-xl:has(p:text-is('Descarregamento (Destino)'))"
NOTA_MDFE = lambda num: SEL(f"[role=dialog] label:has-text('NF-e #{num}')")
MODO = lambda n: SEL("[role=dialog] button[aria-pressed]", hasText=n)
ACOES = lambda placa: LINHA(placa, 'button[aria-haspopup=menu]')
# rodapé das telas cheias (Novo MDF-e, Nova NFS-e): botões FIXOS embaixo da tela, fora da faixa de rolagem: sempre com noScroll=True

JS_TOPO = ("(async()=>{" + ACHA_ROLAGEM + "const el=document.querySelector('main h1, main h2, main table, main [role=tablist]');const c=rolagem(el);"
           "if(!c)return 'SEM ROLAGEM';const y0=c.scrollTop,t0=performance.now();if(y0<3)return 'ok';"
           + SUAVE.replace('DUR', '600').replace('DESTINO', 'y0*(1-e)') + "return 'topo'})()")


@capitulo
def cap04():
    """Novo MDF-e (tela cheia): as NF-e 1255 e 1256 da Serra Fina, a nota de outra empresa pela chave (entra e sai), a natureza da viagem
    e a categoria do transportador (1.60.39), FKD2E41 + Edson, reboques e CIOT (o "frete contratado?" vai a Sim e volta a Não), RJ no percurso, Itamonte/MG, 5.800 kg, contingência (abre e volta ao Normal); criar; autorizado."""
    c = Cap(4, start=(900, 440), setup=setup_em('/fiscal-ambiental/transporte'), obs=False)
    c.mark(1)
    c.click(BTN('Novo MDF-e'), at=c.A(1, 'Novo', 1.0), label='Novo MDF-e')
    c.waitfor(text='NF-ES VINCULADAS', timeout=10)
    c.hover(TXT('NF-ES VINCULADAS', within=DLG), 0.5, at=c.A(1, 'notas', 0.6), label='etapa Notas fiscais')
    c.mark(2)
    c.digita(PH('Buscar NF-e...'), 'Serra Fina', c.A(2, 'Busco', 0.7), c.A(2, 'Serra', 0.2), 'busca: Serra Fina')
    c.click(NOTA_MDFE(1255), at=c.A(2, 'perfil', 0.7), label='NF-e 1255 (alumínio perfil)')
    c.click(NOTA_MDFE(1256), at=c.A(2, 'bloco.', 0.7), label='NF-e 1256 (alumínio bloco)')
    c.hover(TXTX('NF-e(s) vinculada(s)', within=DLG), 1.0, at=c.A(2, 'Juntas,', 0.6), label='2 NF-e vinculadas: R$ 55.380,00')
    c.confere('dlg', ['2 NF-e(s) vinculada(s)', '55.380,00'], 'duas notas, R$ 55.380,00')
    c.mark(3)
    c.hover(TXT('Importar nota pela chave de acesso', within=DLG), 0.8, at=c.A(3, 'nota', 0.6), label='Importar nota pela chave de acesso')
    c.hover(TXTX('Use quando a NF-e foi emitida por outra empresa', within=DLG), 1.0, at=c.A(3, 'chave', 0.6), label='texto: nota emitida por outra empresa')
    c.mark(4)
    c.click(SEL('#mdfe-chave-externa'), at=c.A(4, 'Colo', 0.7), label='Cole os 44 dígitos da chave (campo)')
    c.colar('#mdfe-chave-externa', chave_884(), at=c.A(4, 'quarenta', 0.0), label='chave da NF-e 884 (Depósito Irmãos Siqueira)')
    c.click(BTN('Adicionar', within=DLG), at=c.A(4, 'Adicionar.', 0.7), label='Adicionar')
    c.waitfor(text='Nota recebida', timeout=10)
    c.hover(TXT('Nota recebida', within=DLG), 1.2, at=c.A(4, 'Recebidas,', 0.6), label='NF-e #884 com o selo Nota recebida')
    c.confere('dlg', ['NF-e #884', 'Depósito Irmãos Siqueira', '3 NF-e(s) vinculada(s)', '57.480,00'], 'a 884 entrou: 3 notas, R$ 57.480,00')
    c.mark(5)
    c.hover(TXTX('NF-e(s) vinculada(s)', within=DLG), 0.8, at=c.A(5, 'chave,', 0.6), label='3 NF-e vinculadas: R$ 57.480,00')
    c.hover(SEL("[role=dialog] input[aria-label='Valor da NF-e 884']"), 0.6, at=c.A(5, 'valor', 0.6), label='Valor (opcional) da nota externa')
    c.mark(6)
    c.click(SEL("[role=dialog] button[aria-label='Remover NF-e 884']"), at=c.A(6, 'tiro', 0.7), label='Remover NF-e 884')
    c.hover(TXTX('NF-e(s) vinculada(s)', within=DLG), 0.6, at=c.A(6, 'duas.', 0.6), label='de volta a 2 NF-e: R$ 55.380,00')
    c.confere('dlg', ['2 NF-e(s) vinculada(s)', '55.380,00'], 'de volta a duas notas')
    c.mark(7)
    c.click(BTN('Continuar'), at=c.A(7, 'Continuar.', 0.7), label='Continuar (veículo e motorista)', noScroll=True)
    # 1.60.39: a etapa abre com a natureza da viagem e a categoria do transportador (os padrões já servem: Carga própria e Próprio)
    c.waitfor(text='NATUREZA DA VIAGEM', timeout=10)
    c.hover(SEL("[role=dialog] [data-testid='mdfe-operation-carga_propria']"), 1.2, at=c.A(7, 'própria,', 0.6), label='zoom: Natureza da viagem: Carga própria (já escolhida)')
    c.hover(SEL("[role=dialog] [data-testid='mdfe-transporter-proprio']"), 1.2, at=c.A(7, 'Próprio,', 0.6), label='zoom: Categoria do transportador: Próprio')
    c.mark(8)
    escolhe(c, SEL('[role=dialog] button[role=combobox]', hasText='Selecione um veículo'), OPTX('FKD2E41'), c.A(8, 'veículo,', 0.7), c.A(8, 'truck,', 0.4), 'Veículo: Caminhão truck FKD2E41')
    escolhe(c, SEL('[role=dialog] button[role=combobox]', hasText='Selecione um motorista'), OPTX('Edson Moura'), c.A(8, 'motorista,', 0.7), c.A(8, 'Edson.', 0.4), 'Motorista: Edson Moura')
    c.hover(TXTX('Veículo único', within=DLG), 0.6, at=c.A(8, 'completa,', 0.6), label='composição completa')
    c.mark(9)
    c.hover(TXT('Reboques / Carretas (opcional)', within=DLG), 0.8, at=c.A(9, 'carreta,', 0.6), label='Reboques / Carretas (opcional)')
    c.hover(TXTX('Nenhuma carreta cadastrada', within=DLG), 1.0, at=c.A(9, 'Frota', 0.9), label='Nenhuma carreta cadastrada (Carreta / Reboque na Frota)')
    c.mark(10)
    FRETE = SEL("[role=dialog] [data-testid='mdfe-frete-contratado-control'] button[role=combobox]")
    rola_ate(c, 'CIOT e contratação do frete', c.A(10, 'Embaixo', 0.9), 'desce ao CIOT e contratação do frete', y=300, escopo=DLG)
    c.hover(TXT('Sem CIOT', within=DLG), 0.8, at=c.A(10, 'CIOT', 0.6), label='zoom: selo Sem CIOT')
    c.hover(FRETE, 1.4, at=c.A(10, 'código', 0.6), label='Esta viagem possui frete contratado? Não')
    c.mark(11)
    escolhe(c, FRETE, OPTX('Sim — transporte remunerado'), c.A(11, 'resposta', 0.7), c.A(11, 'Sim.', 0.3), 'frete contratado: Sim (só para mostrar os campos)')
    c.waitfor(text='Registro da operação de transporte', timeout=8)
    c.hover(PH('000000000000'), 0.6, at=c.A(11, 'código', 0.6), label='CIOT * (12 dígitos)')
    c.hover(TXT('CPF/CNPJ do gerador do CIOT *', within=DLG), 0.6, at=c.A(11, 'gerou', 0.6), label='CPF/CNPJ do gerador do CIOT *')
    c.hover(TXT('Contratante — CPF/CNPJ *', within=DLG), 0.6, at=c.A(11, 'contratou', 0.6), label='Contratante — CPF/CNPJ * e Nome *')
    c.hover(TXTX('RNTRC do emitente / transportador', within=DLG), 0.8, at=c.A(11, 'registro', 0.6), label='RNTRC do emitente / transportador *')
    c.mark(12)
    c.hover(PH('000000000000'), 1.2, at=c.A(12, 'código', 0.6), label='CIOT: gerado antes da viagem (sem abrir a ajuda)')
    c.mark(13)
    escolhe(c, FRETE, OPTX('Não — sem pagamento'), c.A(13, 'Hoje', 0.3), c.A(13, 'frete.', 0.3), 'frete contratado: Não (de volta)')
    c.waitfor(text='CIOT não se aplica a esta viagem', timeout=8)
    c.hover(TXT('CIOT não se aplica a esta viagem', within=DLG), 1.5, at=c.A(13, 'confirma:', 0.6), label='zoom: CIOT não se aplica a esta viagem')
    c.mark(14)
    c.click(BTN('Continuar'), at=c.A(14, 'Continuar.', 0.7), label='Continuar (trajeto e carga)', noScroll=True)
    c.hover(SEL(f'{ORIGEM} button[role=combobox] >> nth=1'), 0.8, at=c.A(14, 'Taubaté.', 0.6), label='origem: Taubaté/SP')
    c.mark(15)
    c.click(BTN('Adicionar UF ao percurso'), at=c.A(15, 'adiciono', 0.7), label='Adicionar UF ao percurso')
    escolhe(c, SEL('[role=dialog] button[role=combobox]', hasText='Selecione a UF'), 'RJ', c.A(15, 'Rio', 0.7), c.A(15, 'Janeiro,', 0.3), 'Percurso: 1ª UF RJ', teclas=['R', 'J'])
    # com a 1ª UF do percurso, o cartão do destino desce: a tela sobe antes
    rola_ate(c, 'Descarregamento (Destino)', round(c.L(16) - 0.9, 2), 'tela sobe até o destino', y=330, dur_ms=600, escopo=DLG)
    c.mark(16)
    escolhe(c, SEL(f'{DESTINO} button[role=combobox] >> nth=0'), 'MG', c.A(16, 'destino,', 0.6), c.A(16, 'Minas', 0.2), 'Destino: MG', teclas=['M', 'G'])
    escolhe(c, SEL(f'{DESTINO} button[role=combobox] >> nth=1'), 'Itamonte', c.A(16, 'cidade', 0.6), c.A(16, 'Itamonte.', 0.6), 'Destino: Itamonte')
    c.mark(17)
    rola_ate(c, 'Peso Bruto Total (kg)', c.A(17, 'peso', 0.9), 'tela desce até o peso', y=330, escopo=DLG)
    c.hover(SEL("[role=dialog] div:has(> label:text-is('Peso Bruto Total (kg)')) input"), 0.8, at=c.A(17, 'cinco', 0.5), label='Peso Bruto Total (kg): 5800')
    c.hover(SEL('#mdfe-valor-carga'), 0.8, at=c.A(17, 'valor', 0.5), label='Valor Total da Carga (R$): 55.380,00')
    c.hover(TXTX('Sugerido pelas notas', within=DLG), 1.0, at=c.A(17, 'sugerido', 0.3), label='Sugerido pelas notas — pode ajustar.')
    c.mark(18)
    c.hover(SEL('[role=dialog] textarea'), 1.0, at=c.A(18, 'observações,', 0.6), label='OBSERVAÇÕES (saem no DAMDFE)')
    c.mark(19)
    c.click(BTN('Continuar'), at=c.L(19) - 0.2, label='Continuar (revisão e emissão)', noScroll=True)
    c.hover(MODO('Normal'), 0.8, at=c.A(19, 'Normal,', 0.6), label='Como emitir: Normal')
    c.mark(20)
    c.click(MODO('Contingência'), at=c.A(20, 'contingência', 0.7), label='Contingência (só para mostrar)')
    c.hover(SEL('#contingency-reason'), 0.4, at=c.A(20, 'motivo,', 0.6), label='Motivo da contingência *')
    c.hover(SEL('#contingency-cargo'), 0.3, at=c.A(20, 'tipo', 0.6), label='Tipo de carga *')
    c.hover(SEL('#contingency-ncm'), 0.3, at=c.A(20, 'NCM', 0.5), label='NCM do produto *')
    c.hover(SEL('#contingency-product'), 0.6, at=c.A(20, 'produto', 0.5), label='Produto predominante *')
    c.mark(21)
    c.hover(TXTX('Imprima o DAMDFE em papel antes de liberar o caminhão', within=DLG), 2.0, at=c.A(21, 'impresso', 0.8), label='Imprima o DAMDFE em papel; prazo de regularização: até 168 horas')
    c.mark(22)
    c.click(MODO('Normal'), at=c.A(22, 'volto', 0.7), label='volta para Normal')
    c.hover(TXTX('Tudo pronto para criar e emitir o MDF-e', within=DLG), 0.6, at=c.A(22, 'Normal.', 0.2), label='Tudo pronto para criar e emitir o MDF-e')
    c.mark(23)
    c.click(BTN('Criar MDF-e'), at=c.A(23, 'Criar', 0.7), label='Criar MDF-e', noScroll=True)
    c.waitfor(target=LINHA('FKD2E41', ":text-is('Aguardando SEFAZ')"), timeout=10)
    c.hover(LINHA('FKD2E41', 'td >> nth=1'), 0.6, at=c.A(23, 'enviado', 0.5), label='nº 1 Aguardando SEFAZ')
    c.mark(24)
    c.waitfor(target=LINHA('FKD2E41', ":text-is('Autorizado')"), timeout=15)
    c.registra(LINHA('FKD2E41'), at=c.A(24, 'Pronto,', 0.2), label='linha do nº 1 Autorizado')
    c.hover(LINHA('FKD2E41', "td:has-text('Edson')"), 0.2, at=c.A(24, 'motorista,', 0.6), label='Motorista')
    c.hover(LINHA('FKD2E41', "td:has-text('FKD2E41')"), 0.2, at=c.A(24, 'placa,', 0.6), label='Placa')
    c.hover(LINHA('FKD2E41', "td:has-text('Itamonte')"), 0.2, at=c.A(24, 'trajeto,', 0.6), label='Trajeto')
    c.hover(LINHA('FKD2E41', "td:has-text('55.380')"), 0.2, at=c.A(24, 'valor', 0.6), label='Valor')
    c.hover(LINHA('FKD2E41', "td:has-text('5.800')"), 0.3, at=c.A(24, 'peso.', 0.6), label='Peso (kg)')
    c.mark(25)
    c.hover(ACOES('FKD2E41'), 0.4, at=c.A(25, 'ações', 0.7), label='Ações do nº 1')
    c.hover(ITEM('Baixar DAMDFE (PDF)'), 1.0, at=c.A(25, 'PDF', 0.6), label='Baixar DAMDFE (PDF)', noScroll=True)
    c.fim()
    return c


@capitulo
def cap05():
    """Corte da tarde: encerrar × cancelar (ilustração), o diálogo "Cancelar MDF-e #1" (abre e Voltar), Encerrar pelo menu,
    "Encerramento enviado" e "Encerrado" na consulta."""
    c = Cap(5, start=(900, 440), setup=setup_em('/fiscal-ambiental/transporte'))
    c.mark(1)
    c.hover(LINHA('FKD2E41', "td:has-text('Itamonte')"), 0.6, at=c.A(1, 'Itamonte.', 0.6), label='nº 1 para Itamonte, Autorizado')
    c.hover(CARTAO('MDF-e Autorizados'), 0.6, at=c.A(1, 'encerrar', 0.6), label='MDF-e Autorizados: 1')
    c.mark(2)
    c.cursor(NEUTRO, at=c.L(2) - 0.2, label='cursor em repouso (ilustração encerrar × cancelar)')
    c.mark(3)
    c.hover(ACOES('FKD2E41'), 0.3, at=c.L(3) - 0.2, label='Ações do nº 1 (cancelar)')
    c.click(ITEM('Cancelar'), at=c.A(3, 'cancelamento:', 0.5), label='Cancelar (abre o diálogo)', noScroll=True)
    c.waitfor(text='Cancelar MDF-e #1', timeout=10)
    c.hover(TXTX('O cancelamento será enviado à SEFAZ', within='[role=alertdialog]'), 0.6, at=c.A(3, 'volta,', 0.7), label='O cancelamento é irreversível')
    c.hover(TXTX('Motivo do cancelamento (mín. 15 caracteres)', within='[role=alertdialog]'), 0.8, at=c.A(3, 'motivo', 0.6), label='Motivo do cancelamento (mín. 15 caracteres)')
    c.hover(TXTX('O prazo para cancelamento geralmente é de 24 horas', within='[role=alertdialog]'), 1.2, at=c.A(3, 'prazo', 0.6), label='prazo: geralmente 24 horas após a autorização')
    c.mark(4)
    c.click(BTN('Voltar'), at=c.A(4, 'Voltar.', 0.6), label='Voltar (não cancela)')
    c.mark(5)
    c.hover(ACOES('FKD2E41'), 0.4, at=c.A(5, 'menu', 0.7), label='Ações do nº 1')
    c.click(ITEM('Encerrar'), at=c.A(5, 'Encerrar.', 0.6), label='Encerrar', noScroll=True)
    c.waitfor(target=LINHA('FKD2E41', ":text-is('Encerramento enviado')"), timeout=10)
    c.hover(LINHA('FKD2E41', "td:has-text('Encerramento enviado')"), 0.8, at=c.A(5, 'selo', 0.6), label='selo Encerramento enviado')
    c.mark(6)
    c.waitfor(target=LINHA('FKD2E41', ":text-is('Encerrado')"), timeout=15)
    c.hover(LINHA('FKD2E41', "td:has-text('Encerrado')"), 0.8, at=c.A(6, 'encerrado.', 0.6), label='selo Encerrado')
    c.hover(CARTAO('MDF-e Encerrados'), 1.0, at=c.A(6, 'encerrados.', 0.6), label='MDF-e Encerrados: 1')
    c.fim()
    return c


@capitulo
def cap06():
    """Quando o manifesto não passa: o nº 2 "Rejeitado" (lateral mdfe2-rejeitado), "Ver Erro", "Reemitir" e "Excluir" (sem clicar),
    a ilustração dos selos de recusa, a busca e os detalhes do nº 1. O erro na tela é o assunto: sem o observador de avisos."""
    c = Cap(6, start=(900, 440), setup=setup_em('/fiscal-ambiental/transporte'), obs=False)
    c.mark(1)
    c.hover(LINHA('GHT7B19', "td:has-text('Rejeitado')"), 1.0, at=c.A(1, 'rejeitado,', 0.6), label='nº 2 Rejeitado')
    c.hover(CARTAO('MDF-e Rejeitados'), 1.0, at=c.A(1, 'rejeitados.', 0.6), label='MDF-e Rejeitados: 1')
    c.mark(2)
    c.hover(ACOES('GHT7B19'), 0.4, at=c.A(2, 'menu', 0.7), label='Ações do nº 2')
    c.click(ITEM('Ver Erro'), at=c.A(2, 'Ver', 0.6), label='Ver Erro', noScroll=True)
    c.waitfor(text='Erro no MDF-e #2', timeout=10)
    c.hover(TXTX('CPF do condutor', within='[role=alertdialog]'), 1.5, at=c.A(2, 'CPF', 0.6), label='Erro no MDF-e #2: CPF do condutor')
    c.mark(3)
    c.click(BTN('Fechar'), at=c.A(3, 'Fechar.', 0.6), label='Fechar')
    c.hover(ACOES('GHT7B19'), 0.3, at=c.A(3, 'menu', 0.7), label='Ações do nº 2 (de novo)')
    c.hover(ITEM('Reemitir'), 0.4, at=c.A(3, 'Reemitir', 0.5), label='Reemitir', noScroll=True)
    c.hover(ITEM('Excluir'), 0.5, at=c.A(3, 'Excluir.', 0.5), label='Excluir', noScroll=True)
    c.mark(4)
    c.hover(ITEM('Reemitir'), 1.0, at=c.A(4, 'Reemitir.', 0.6), label='Reemitir (falha de momento)', noScroll=True)
    c.hover(ITEM('Excluir'), 1.2, at=c.A(4, 'excluir,', 0.6), label='Excluir (erro num dado do manifesto)', noScroll=True)
    c.cursor(NEUTRO, at=c.A(4, 'criar', 0.2), label='cursor sai do menu')
    c.mark(5)
    c.cursor(NEUTRO, at=c.L(5) - 0.1, label='cursor em repouso (ilustração dos selos de recusa)')
    c.mark(6)
    c.hover(PH('Buscar por nº, placa ou motorista...'), 0.8, at=c.A(6, 'busca', 0.6), label='Buscar por nº, placa ou motorista...')
    c.click(LINHA('FKD2E41', "td:has-text('Edson')"), at=c.A(6, 'clicando', 0.7), label='abre a linha do nº 1')
    c.waitfor(text='Detalhes do MDF-e #1', timeout=8)
    c.hover(TXTX('Detalhes do MDF-e #1', within='main'), 1.0, at=c.A(6, 'detalhes', 0.4), label='Detalhes do MDF-e #1')
    c.fim()
    return c


@capitulo
def cap07():
    """Notas de Serviço: a lista (14 ainda não existe: 13 e 12), mercadoria × serviço (ilustração), colunas e Configurações Fiscais."""
    c = Cap(7, start=(900, 440), setup=setup_em('/fiscal-ambiental/transporte', aquece=['/fiscal-ambiental/nfse'], menu='Notas de Serviço (NFS-e)'))
    c.mark(1)
    c.click(ITEM_MENU('Notas de Serviço (NFS-e)'), at=c.A(1, 'Notas', 0.9), label='Notas de Serviço (NFS-e) no menu')
    c.waitfor(text=PAGINAS['/fiscal-ambiental/nfse'], timeout=15)
    c.mark(2)
    c.cursor(NEUTRO, at=c.L(2) - 0.2, label='cursor em repouso (ilustração mercadoria × serviço)')
    c.marca_ja(3)
    c.mark(4)
    c.registra(SEL('main thead'), at=c.A(4, 'lista', 0.3), label='colunas da lista (zoom)')
    c.hover(SEL("main th:has-text('Número')"), 0.2, at=c.A(4, 'número,', 0.6), label='coluna Número')
    c.hover(SEL("main th:has-text('Tomador')"), 0.3, at=c.A(4, 'tomador,', 0.6), label='coluna Tomador')
    c.hover(SEL("main th:has-text('Valor')"), 0.2, at=c.A(4, 'valor', 0.6), label='coluna Valor')
    c.hover(SEL("main th:has-text('Status')"), 0.4, at=c.A(4, 'status.', 0.6), label='coluna Status')
    c.mark(5)
    c.hover(BTN('Configurações Fiscais'), 1.2, at=c.A(5, 'Configurações', 0.6), label='Configurações Fiscais', noScroll=True)
    c.cursor(NEUTRO, at=c.A(5, 'contador.', 0.2), label='cursor sai do botão')
    c.fim()
    return c


@capitulo
def cap08():
    """Nova NFS-e (tela cheia) para a Aços Quiririm: competência 06/11, série 1 e próxima DPS nº 14, coleta e remoção de resíduos,
    R$ 1.850,00, alíquota 3, ISS retido e retenções federais (só mostra), pré-visualização, emitir; nº 14 autorizada."""
    c = Cap(8, start=(900, 440), setup=setup_em('/fiscal-ambiental/nfse'))
    c.mark(1)
    c.click(BTN('Nova NFS-e'), at=c.A(1, 'Nova', 1.0), label='Nova NFS-e')
    c.waitfor(text='Data de competência', timeout=10)
    c.mark(2)
    c.click(SEL("[role=dialog] label[for='nfse-competencia']"), at=c.A(2, 'competência', 0.6), label='Data de competência (campo)')
    c.type(SEL('#nfse-competencia'), '06112026', at=c.A(2, 'seis', 0.1), label='Data de competência: 06/11/2026', cps=40, noClick=True)
    c.hover(TXT('Série da DPS', within=DLG), 0.5, at=c.A(2, 'série', 0.6), label='Série da DPS: Série 1')
    c.hover(TXTX('Próxima DPS: nº 14', within=DLG), 1.5, at=c.A(2, 'próximo', 0.5), label='Próxima DPS: nº 14')
    c.mark(3)
    c.click(SEL('[role=dialog] button', hasText='Cliente ou fornecedor'), at=c.A(3, 'tomador,', 0.7), label='Tomador: Cliente ou fornecedor')
    c.waitfor(text='Selecionar tomador', timeout=10)
    c.type(PH('Buscar por nome, CNPJ/CPF ou código...'), 'Aços', at=c.A(3, 'escolho', 0.2), label='busca: Aços', cps=12, noClick=True)
    c.click(TXTX('Aços Quiririm', within='[role=dialog] >> nth=-1'), at=c.A(3, 'Quiririm', 0.6), label='Aços Quiririm (a busca mostra a razão social)')
    c.hover(TXT('Buscar pelo CNPJ', within=DLG), 1.0, at=c.A(3, 'buscar', 0.6), label='Buscar pelo CNPJ (tomador sem cadastro)')
    c.mark(4)
    c.click(BTN('Avançar'), at=c.A(4, 'Avançar.', 0.7), label='Avançar (Serviço)', noScroll=True)
    c.hover(SEL('[role=dialog] button', hasText='Taubaté'), 0.2, at=c.A(4, 'Taubaté.', 0.8), label='Município: Taubaté')
    c.click(SEL('[role=dialog] button[role=combobox]', hasText='Selecionar código de tributação'), at=c.A(4, 'código', 0.7), label='Código de Tributação Nacional (abre)')
    c.type(PH('Buscar por código ou descrição...'), 'coleta', at=c.A(4, 'contador', 0.2), label='busca: coleta', cps=12, noClick=True)
    c.click(OPTX('Varrição, coleta, remoção'), at=c.A(4, 'coleta', 0.6), label='código: coleta e remoção de resíduos')
    c.mark(5)
    c.hover(SEL('[role=dialog] button', hasText='Puxar serviço salvo'), 0.6, at=c.A(5, 'puxar', 0.6), label='Puxar serviço salvo')
    c.mark(6)
    c.click(SEL('#nfse-discriminacao'), at=c.A(6, 'descrição,', 0.7), label='Descrição do serviço (campo)')
    c.colar('#nfse-discriminacao', 'Coleta e remoção de resíduos metálicos com caçamba no pátio da Aços Quiririm em 06/11/2026.',
            at=c.A(6, 'feito,', 0.1), label='Descrição do serviço')
    c.mark(7)
    c.click(BTN('Avançar'), at=c.A(7, 'Avançar.', 0.7), label='Avançar (Valores)', noScroll=True)
    c.click(SEL('#nfse-valor'), at=c.A(7, 'valor', 0.8), label='Valor do serviço (campo)')
    c.type(SEL('#nfse-valor'), '1850', at=c.A(7, 'mil', 0.3), label='Valor do serviço: 1850', cps=20, noClick=True)
    c.mark(8)
    # 1.60.18: a alíquota da lista do município continua sem chegar ao campo "Alíquota ISS %" (MELHORIAS): o robô digita os 3 %
    c.click(SEL('#nfse-iss-aliq'), at=c.A(8, 'alíquota', 0.7), label='Alíquota ISS % (campo)')
    c.type(SEL('#nfse-iss-aliq'), '3', at=c.A(8, 'três', 0.1), label='Alíquota ISS %: 3', cps=12, noClick=True, clear=True)
    c.hover(SEL('#nfse-iss-aliq'), 0.8, at=c.A(8, 'contador.', 0.9), label='Alíquota ISS %: 3,00 (o contador confirma)')
    c.mark(9)
    c.hover(TXT('ISS retido na fonte', within=DLG), 1.2, at=c.A(9, 'retido', 0.8), label='ISS retido na fonte (desligado)')
    c.hover(TXT('Retenções federais (R$)', within=DLG), 1.0, at=c.A(9, 'retenções', 0.6), label='Retenções federais (R$)')
    c.hover(TXTX('Informe o valor efetivamente retido de cada tributo', within=DLG), 1.0, at=c.A(9, 'descontou', 0.6), label='Informe o valor efetivamente retido de cada tributo.')
    c.mark(10)
    c.hover(TXT('Ajustes (deduções e descontos)', within=DLG), 0.8, at=c.A(10, 'retenção', 0.6), label='Ajustes (deduções e descontos)')
    c.hover(TXT('Valor líquido', within=DLG), 1.0, at=c.A(10, 'zerado.', 0.9), label='Valor líquido: R$ 1.850,00')
    c.mark(11)
    c.click(BTN('Avançar'), at=c.L(11) - 0.2, label='Avançar (Pré-visualização)', noScroll=True)
    c.hover(TXTX('Nº RPS (previsto)', within=DLG), 0.8, at=c.A(11, 'série', 0.6), label='Série 1 e Nº RPS (previsto) 14')
    c.hover(TXTX('Pronta pra emitir', within=DLG), 0.6, at=c.A(11, 'selo', 0.6), label='selo Pronta pra emitir', noScroll=True)
    c.confere('dlg', ['Pronta pra emitir'], 'nenhuma pendência')
    c.mark(12)
    c.hover(BTN('Salvar rascunho'), 1.2, at=c.A(12, 'salvar', 0.6), label='Salvar rascunho (sem clicar)', noScroll=True)
    c.mark(13)
    c.click(BTN('Emitir NFS-e'), at=c.A(13, 'Emitir', 0.7), label='Emitir NFS-e', noScroll=True)
    c.waitfor(target=LINHA('#14', ":text-is('Processando')"), timeout=10)
    c.hover(LINHA('#14', "td:has-text('Processando')"), 0.6, at=c.A(13, 'processando.', 0.6), label='nº 14 Processando')
    c.mark(14)
    c.waitfor(target=LINHA('#14', ":text-is('Autorizada')"), timeout=15)
    c.hover(LINHA('#14', 'td >> nth=0'), 1.0, at=c.A(14, 'catorze.', 0.6), label='nº 14 Autorizada')
    c.mark(15)
    c.click(LINHA('#14', 'button[aria-haspopup=menu]'), at=c.A(15, 'menu,', 0.8), label='Ações da nº 14 (menu)')
    c.hover(ITEM('Baixar PDF'), 0.6, at=c.A(15, 'PDF', 0.6), label='Baixar PDF', noScroll=True)
    c.hover(ITEM('Histórico'), 0.6, at=c.A(15, 'Histórico', 0.6), label='Histórico', noScroll=True)
    c.hover(ITEM('Cancelar'), 0.8, at=c.A(15, 'cancelamento.', 0.6), label='Cancelar', noScroll=True)
    c.press('Escape', at=round(c.W(15, 'cancelamento.') + 0.9, 2), label='fecha o menu')
    c.fim()
    return c


@capitulo
def cap09():
    """NFS-e recebidas: Notas Fiscais > Notas Recebidas > NFS-e, ativar; a busca fica pedida ao Ambiente Nacional (as notas só chegam
    depois: capítulo 10)."""
    c = Cap(9, start=(900, 440), setup=setup_em('/fiscal-ambiental/nfse', aquece=['/fiscal-ambiental/nfe/saida'], menu='Notas Fiscais (NF-e)'))
    c.mark(1)
    c.click(ITEM_MENU('Notas Fiscais (NF-e)'), at=c.A(1, 'Notas', 0.9), label='Notas Fiscais (NF-e) no menu')
    c.click(SUBABA('Notas Recebidas'), at=c.A(1, 'Recebidas,', 0.7), label='aba Notas Recebidas')
    c.click(TAB('NFS-e'), at=c.A(1, 'NFS-e.', 0.6), label='aba NFS-e')
    c.waitfor(text='Ative as Notas de Serviço Recebidas', timeout=10)
    c.mark(2)
    c.hover(TXTX('prestadores emitem contra o CNPJ', within='main'), 1.0, at=c.A(2, 'CNPJ:', 0.6), label='texto: notas emitidas contra o CNPJ')
    c.mark(3)
    c.click(BTN('Ativar NFS-e Recebidas'), at=c.A(3, 'Ativar', 0.8), label='Ativar NFS-e Recebidas')
    c.waitfor(text='Ativar o recebimento de notas de serviço?', timeout=10)
    c.hover(TXTX('cada nota de serviço recebida passa a contar', within='[role=alertdialog]'), 0.6, at=c.A(3, 'aviso:', 0.6), label='aviso da cota')
    c.mark(4)
    c.click(BTN('Ativar mesmo assim'), at=c.A(4, 'Ativar', 0.7), label='Ativar mesmo assim')
    # 28/11: com o motor próprio (nfse_dfe_fonte "sefin") a 1ª busca vai à edge plugnotas-nfse-dfe-sync, que só avisa que é automática
    c.waitfor(text='A consulta direta ao Ambiente Nacional é automática', timeout=15)
    c.hover(TXTX('A consulta direta ao Ambiente Nacional é automática', within='main'), 1.5, at=c.A(4, 'busca', 0.6), label='faixa: a consulta é automática')
    c.mark(5)
    c.hover(TXTX('A NFS-e é da prefeitura', within='main'), 1.2, at=c.A(5, 'cidade', 0.6), label='aviso: só chega nota de cidade do sistema nacional')
    c.fim()
    return c


@capitulo
def cap10():
    """Da nota recebida à despesa (14:40): as duas notas que o motor trouxe (lateral nfse-recebidas), "Sincronizar agora" (sem clicar),
    lançar a da balança como conta (vencimento 20/11, Manutenção de máquinas) e o selo "Lançada"."""
    c = Cap(10, start=(900, 440), setup=setup_em('/fiscal-ambiental/nfe/recebidas-nfse', extra=[
        {'do': 'waitFor', 'text': 'Balanças Tremembé Manutenção Ltda', 'timeout': 20}, {'do': 'wait', 'seconds': 0.8}]))
    c.mark(1)
    c.hover(SEL('main tbody'), 0.8, at=c.A(1, 'duas', 0.6), label='duas notas recebidas')
    c.mark(2)
    c.hover(LINHA('Contabilidade Manacá', 'td >> nth=0'), 0.6, at=c.A(2, 'honorários', 0.6), label='Contabilidade Manacá Ltda R$ 1.650,00')
    c.registra(SEL('main tbody'), label='colunas Prestador e Valor (zoom)')
    c.hover(LINHA('Balanças Tremembé', 'td >> nth=0'), 0.6, at=c.A(2, 'aferição', 0.6), label='Balanças Tremembé R$ 980,00')
    c.mark(3)
    c.hover(TXTX('Última sincronização', within='main'), 1.0, at=c.A(3, 'última', 0.6), label='Última sincronização', noScroll=True)
    c.hover(BTN('Sincronizar agora'), 1.2, at=c.A(3, 'Sincronizar', 0.6), label='Sincronizar agora (sem clicar)', noScroll=True)
    c.mark(4)
    c.click(LINHA('Balanças Tremembé', 'button[aria-haspopup]'), at=c.A(4, 'linha', 0.7), label='Ações da nota da balança')
    c.click(ITEM('Lançar despesa / conta'), at=c.A(4, 'Lançar', 0.6), label='Lançar despesa / conta', noScroll=True)
    c.waitfor(text='Nova conta', timeout=10)
    c.mark(5)
    c.hover(SEL('#bill-amount'), 0.6, at=c.A(5, 'valor', 0.6), label='Valor R$ 980,00 já preenchido')
    c.click(SEL('#bill-due'), at=c.A(5, 'vencimento,', 1.0), label='Vencimento (abre o calendário)')
    c.click(SEL("[data-radix-popper-content-wrapper] button[name=day]:text-is('20')"), at=c.A(5, 'dia', 0.5), label='Vencimento: 20/11/2026')
    c.click(SEL('#bill-category'), at=c.A(5, 'vinte,', 0.2), label='Categoria (abre)')
    c.type(PH('Pesquisar categoria...'), 'manut', at=c.A(5, 'categoria.', 0.6), label='busca: manut', cps=40, noClick=True)
    c.click(OPTX('Manutenção de máquinas'), at=c.A(5, 'categoria.', -0.1), label='Categoria: Manutenção de máquinas')
    c.click(BTN('Criar conta'), at=c.A(5, 'Criar', -0.1), label='Criar conta')
    c.waitfor(target=LINHA('Balanças Tremembé', ":text-is('Lançada')"), timeout=10)
    c.hover(LINHA('Balanças Tremembé', "td:has-text('Lançada')"), 1.0, at=c.A(5, 'lançada.', 0.6), label='selo Lançada')
    c.mark(6)
    c.hover(LINHA('Balanças Tremembé', "td:has-text('Lançada')"), 1.5, at=c.A(6, 'avisa', 0.6), label='selo Lançada (o sistema avisa antes de lançar de novo)')
    c.fim()
    return c


POSICAO = '/fiscal-ambiental/estoque-fiscal/posicao'
COOP = 'Cooperativa Recomeço'
TRIG_NFE = lambda t: SEL(f"main tr:has-text('{t}') button[title='Ações']")   # menu da NF-e recebida (DropdownMenu: abre no clique; T16)
TILE = lambda n: SEL(f"[role=dialog] button:has(span:text-is('{n}'))")       # formas de pagamento do Finalizar Pedido (T07)


@capitulo
def cap11():
    """Da nota recebida à compra (1.60.39; 14:40): Notas Recebidas > NF-e com a Cooperativa Recomeço (importada pelo XML na T16), o
    botão Importar XML (sem clicar), Lançar compra…, os totais (Produtos, Encargos/descontos, Total da nota), o casamento já feito,
    "Registrar também no estoque fiscal" marcada, Conferir na tela de compra, Finalizar com Pix e o selo "Lançada como compra".
    Lateral compra-coop: o caixa #85 do Rafael aberto (a tela de Compra pede caixa aberto). Não deixa semente."""
    c = Cap(11, start=(900, 440), setup=setup_em('/fiscal-ambiental/nfe/recebidas', extra=[
        {'do': 'waitFor', 'text': COOP, 'timeout': 20}, {'do': 'wait', 'seconds': 0.6}]))
    c.mark(1)
    c.hover(LINHA(COOP), 1.6, at=c.A(1, 'Cooperativa', 0.6), label='zoom: a nota da Cooperativa Recomeço (R$ 7.550,00, importada pelo XML na T16)')
    c.confere('main', [COOP, '7.550,00'], 'a nota 3871 da Cooperativa na lista')
    c.mark(2)
    c.hover(BTN('Importar XML', within='main'), 2.5, at=c.A(2, 'Importar', 0.6), label='zoom: Importar XML (sem clicar)')
    c.cursor(NEUTRO, at=c.A(2, 'serviço', 0.2), label='cursor em repouso (a NFS-e também entra pelo Importar XML)')
    c.mark(3)
    c.click(TRIG_NFE(COOP), at=c.A(3, 'linha', 0.7), label='Ações da nota da Cooperativa')
    c.click(ITEM('Lançar compra…'), at=c.A(3, 'Lançar', 0.6), label='Lançar compra…', noScroll=True)
    c.waitfor(text='Importar NF-e nº 3871', timeout=12)
    c.hover(SEL(f"{DLG} :text-matches('^Fornecedor:')"), 0.8, label='Fornecedor: Cooperativa Recomeço (por CNPJ/CPF)')
    c.mark(4)
    c.hover(SEL(f"{DLG} [aria-label='Totais da NF-e']"), 2.2, at=c.A(4, 'produtos,', 0.6), label='zoom: Produtos, Encargos/descontos e Total da nota')
    c.confere('dlg', ['Produtos', 'Encargos/descontos', 'Total da nota', '7.550,00'], 'os totais da NF-e (1.60.39)')
    c.hover(SEL(f"{DLG} :text-is('Total da nota')"), 1.4, at=c.A(4, 'sete', 0.6), label='Total da nota R$ 7.550,00 (sem encargo)')
    c.mark(5)
    c.hover(SEL(f"{DLG} :text-is('ALUMINIO LATINHA')"), 0.8, at=c.A(5, 'casados', 0.6), label='ALUMINIO LATINHA: Alumínio latinha (alta)')
    c.hover(SEL(f"{DLG} :text-is('PLASTICO PET PRENSADO')"), 0.8, at=c.A(5, 'PET.', 0.6), label='PLASTICO PET PRENSADO: Plástico PET (confira)')
    c.mark(6)
    c.hover(SEL(f"{DLG} label:has-text('Registrar também no estoque fiscal')"), 2.2, at=c.A(6, 'opção,', 0.6),
            label='zoom: Registrar também no estoque fiscal (não altera o saldo físico), marcada', noScroll=True)
    c.mark(7)
    c.click(SEL(f"{DLG} button:has-text('Conferir na tela de compra')"), at=c.A(7, 'Conferir', 0.7), label='Conferir na tela de compra', noScroll=True)
    c.waitfor(text='Voltar para o caixa', timeout=15)
    c.waitfor(text='Plástico PET', timeout=10)
    c.ev(ANIM_FIX, label='(animações da tela de Compra)')
    c.hover(SEL("main tbody tr:has-text('Alumínio latinha')"), 0.8, at=c.A(7, 'oitocentos', 0.6), label='Alumínio latinha 850 kg x R$ 6,20')
    c.hover(SEL("main tbody tr:has-text('Plástico PET')"), 0.8, at=c.A(7, 'PET.', 0.6), label='Plástico PET 1.200 kg x R$ 1,90')
    c.confere('main', ['Alumínio latinha', 'Plástico PET', '7.550,00'], 'compra com os itens da nota: R$ 7.550,00')
    c.mark(8)
    c.hover(BTN('Finalizar'), 0.6, at=c.A(8, 'valores', 0.6), label='Finalizar (o caixa #85 está aberto)')
    c.click(BTN('Finalizar'), at=c.A(8, 'Finalizar,', 0.7), label='Finalizar')
    c.waitfor(text='Finalizar Pedido', timeout=10)
    c.click(TILE('Pix/Transferência'), at=c.A(8, 'Pix,', 0.5, nth=1), label='Pix/Transferência (Conta Principal)')
    c.click(BTNX('CONFIRMAR PAGAMENTO'), at=c.A(8, 'confirmo', 0.6), label='CONFIRMAR PAGAMENTO')
    c.waitfor(text='Compra registrada!', timeout=12)
    c.press('Escape', label='fecha a pergunta do comprovante (sem imprimir)', when=SEL(DLG))
    # a volta pelo menu começa logo depois do pagamento (três cliques não cabem no começo da L9)
    c.click(GRUPO, label='abre Fiscal & Ambiental', unless=ITEM_MENU('Notas Fiscais (NF-e)'))
    c.click(ITEM_MENU('Notas Fiscais (NF-e)'), label='Notas Fiscais (NF-e) no menu')
    c.mark(9)
    c.click(SUBABA('Notas Recebidas'), at=c.A(9, 'volta', 0.4), label='aba Notas Recebidas')
    c.waitfor(text='Lançada como compra', timeout=12)
    c.hover(LINHA(COOP, ":text-is('Lançada como compra')"), 1.5, at=c.A(9, 'lançada', 0.6), label='zoom: selo Lançada como compra')
    c.click(TRIG_NFE(COOP), at=c.A(9, 'tentar', 0.7), label='Ações da Cooperativa (de novo)')
    c.hover(ITEM('Lançar compra de novo…'), 1.5, at=c.A(9, 'avisa', 0.6), label='Lançar compra de novo… (sem clicar)', noScroll=True)
    c.press('Escape', at=c.A(9, 'estoque.', 0.2), label='fecha o menu')
    c.fim()
    return c


PERIODO = SEL('main button[role=combobox]', hasText='Este mês')   # filtro de período do cabeçalho (y ~92, fora da faixa 96..730: fixo=True)


@capitulo
def cap12():
    """Relatório/Estoque Fiscal (uma tela só desde o 1.60.15) > aba NF-e de outubro (Entrada, Saída, Saldo R$ 71.625,00, Pendentes + Rejeitadas,
    o cartão Entrada aberto, gráficos e rankings) e aba NFS-e (cartões e rankings)."""
    c = Cap(12, start=(900, 440), setup=setup_em('/fiscal-ambiental/nfe/recebidas-nfse', aquece=['/fiscal-ambiental/estoque-fiscal/relatorio-nfe'], menu='Relatório/Estoque Fiscal'))
    c.mark(1)
    c.click(ITEM_MENU('Relatório/Estoque Fiscal'), at=c.A(1, 'Relatório', 0.9), label='Relatório/Estoque Fiscal no menu (abre no Saldo atual)')
    c.waitfor(text=PAGINAS[POSICAO], timeout=15)
    c.click(SUBABA('NF-e'), at=c.A(1, 'aba', 0.6), label='aba NF-e')
    c.waitfor(text='Pendentes + Rejeitadas', timeout=15)
    escolhe(c, PERIODO, 'Mês passado', c.A(1, 'Escolho', 0.7), c.A(1, 'passado,', 0.4), 'período: Mês passado', fixo=True)
    c.waitfor(text='R$ 71.625,00', timeout=15)
    c.mark(2)
    c.hover(CARTAO('Entrada'), 0.6, at=c.A(2, 'entrou', 0.6), label='cartão Entrada')
    c.hover(CARTAO('Saída'), 0.6, at=c.A(2, 'saiu', 0.6), label='cartão Saída')
    c.mark(3)
    c.hover(CARTAO('Saldo (Saída − Entrada)'), 1.4, at=c.A(3, 'saldo', 0.6), label='cartão Saldo (Saída − Entrada)')
    c.mark(4)
    c.hover(CARTAO('Pendentes + Rejeitadas'), 1.4, at=c.A(4, 'último', 0.6), label='cartão Pendentes + Rejeitadas')
    c.mark(5)
    c.click(CARTAO('Entrada'), at=c.A(5, 'Entrada,', 0.7), label='abre o cartão Entrada')
    c.waitfor(text='Emitidas por você', timeout=8)
    c.hover(TXT('Emitidas por você', within='main'), 1.5, at=c.A(5, 'nove', 0.6), label='Emitidas por você: 9 · R$ 97.315,00')
    c.confere('main', ['Emitidas por você', '97.315,00'], 'entrada de outubro: 9 notas próprias')
    c.mark(6)
    c.hover(TXT('Emitidas por você', within='main'), 1.0, at=c.A(6, 'fornecedor', 0.6), label='cartão Entrada aberto (notas de fornecedor entram em outra linha)')
    c.mark(7)
    rola_ate(c, 'Entrada × Saída no período', c.L(7) - 0.2, 'rola até o gráfico do mês', y=110, prefixo=True)
    c.hover(TXTX('Entrada × Saída no período', within='main'), 0.3, at=c.A(7, 'gráfico', 0.6), label='Entrada × Saída no período')
    c.hover(TXTX('Distribuição por status', within='main'), 0.3, at=c.A(7, 'status', 0.6), label='Distribuição por status')
    rola_ate(c, 'Top Fornecedores', c.A(7, 'ranking', 0.5), 'rola até os rankings', y=250, dur_ms=700, prefixo=True)
    c.hover(TXTX('Top Fornecedores', within='main'), 0.3, at=c.A(7, 'fornecedores', 0.6), label='Top Fornecedores')
    c.hover(TXTX('Top Clientes', within='main'), 0.6, at=c.A(7, 'clientes.', 0.6), label='Top Clientes')
    c.mark(8)
    c.ev(JS_TOPO, at=c.L(8) - 0.2, label='volta ao topo')
    c.click(SUBABA('NFS-e'), at=c.A(8, 'lado,', 0.3), label='aba NFS-e (do lado)')
    c.waitfor(text='Serviços autorizados', timeout=10)
    c.registra(CARTAO('ISS apurado'), label='cartões do relatório de NFS-e (zoom)')
    c.hover(CARTAO('Serviços autorizados'), 0.5, at=c.A(8, 'autorizado,', 0.6), label='Serviços autorizados')
    c.hover(CARTAO('ISS apurado'), 0.5, at=c.A(8, 'ISS', 0.6), label='ISS apurado')
    c.hover(CARTAO('Retenções federais'), 0.8, at=c.A(8, 'retenções.', 0.6), label='Retenções federais')
    c.confere('main', ['Serviços autorizados', '2.800,00', 'Tudo em dia'], 'NFS-e de outubro: R$ 2.800,00')
    c.mark(9)
    rola_ate(c, 'Top tomadores', c.L(9) - 0.2, 'rola até os rankings de serviço', y=250, dur_ms=700, prefixo=True)
    c.hover(TXTX('Top tomadores', within='main'), 0.6, at=c.A(9, 'contratou', 0.6), label='Top tomadores')
    c.hover(TXTX('Top serviços', within='main'), 0.8, at=c.A(9, 'serviços', 0.6), label='Top serviços')
    c.fim()
    return c


MATERIAIS = "main section[aria-label='Materiais do Kardex fiscal']"
SALDO = lambda nome, sub='': SEL(f"main tbody tr:has-text('{nome}') {sub}".strip())


@capitulo
def cap13():
    """Relatório/Estoque Fiscal > Saldo atual (a primeira aba, na mesma tela do relatório): a tabela, o alumínio já descontado, a busca, o saldo em vermelho (só fala) e a faixa amarela."""
    c = Cap(13, start=(900, 440), setup=setup_em('/fiscal-ambiental/estoque-fiscal/relatorio-nfe', aquece=[POSICAO]))
    c.mark(1)
    c.click(SUBABA('Saldo atual'), at=c.A(1, 'primeira', 0.6), label='aba Saldo atual (a primeira da mesma tela)')
    c.waitfor(text=PAGINAS[POSICAO], timeout=15)
    c.hover(SEL("main thead th:has-text('Saldo fiscal')"), 0.8, at=c.A(1, 'material.', 0.9), label='tabela: Código, Material, Saldo fiscal')
    c.mark(2)
    c.registra(SALDO('Alumínio perfil'), at=c.A(2, 'atualiza', 0.3), label='linhas do alumínio (zoom)')
    c.hover(SALDO('Alumínio bloco', 'td >> nth=2'), 0.6, at=c.A(2, 'alumínio', 0.6), label='Alumínio bloco: já sem os 2.600 kg de hoje')
    c.hover(SALDO('Alumínio perfil', 'td >> nth=2'), 1.0, at=c.A(2, 'descontadas', 0.6), label='Alumínio perfil: já sem os 3.200 kg de hoje')
    c.mark(3)
    c.digita(PH('Buscar material ou código'), 'cobre', c.A(3, 'buscar', 0.7), c.A(3, 'nome', 0.3), 'busca: cobre')
    c.press('Control+a', at=round(c.W(3, 'código.') + 0.5, 2), label='limpa a busca (seleciona)')
    c.press('Backspace', label='limpa a busca')
    c.mark(4)
    c.hover(SEL("main thead th:has-text('Saldo fiscal')"), 1.2, at=c.A(4, 'vermelho,', 0.6), label='coluna Saldo fiscal (negativo aparece em vermelho)')
    c.mark(5)
    c.hover(TXT('apurados pelas notas disponíveis', within='main'), 2.0, at=c.A(5, 'aviso', 0.6), label='faixa amarela: saldos sem saldo inicial informado')
    c.confere('main', ['apurados pelas notas disponíveis', 'Bateria automotiva'], 'faixa amarela e a bateria sem saldo inicial')
    c.fim()
    return c


@capitulo
def cap14():
    """Informar saldo inicial da bateria: menu da linha, data-base 31/10/2026, 3.320 kg, a aba Planilha (só mostra), confirmar;
    a faixa amarela some e a bateria vai a 3.960 kg."""
    c = Cap(14, start=(900, 440), setup=setup_em(POSICAO))
    c.mark(1)
    c.hover(SALDO('Bateria automotiva', 'td >> nth=1'), 0.8, at=c.A(1, 'bateria.', 0.6), label='Bateria automotiva (sem saldo inicial)')
    c.hover(SALDO('Bateria automotiva', "button[aria-label='Ações de Bateria automotiva']"), 0.3, at=c.A(1, 'linha', 0.7), label='menu ⋯ da bateria')
    c.click(ITEM('Informar saldo inicial'), at=c.A(1, 'Informar', 0.6), label='Informar saldo inicial', noScroll=True)
    c.waitfor(text='O saldo fica só no estoque fiscal', timeout=10)
    c.mark(2)
    c.click(SEL("[role=dialog] label[for='opening-date']"), at=c.A(2, 'data-base,', 0.7), label='Data-base (campo)')
    c.type(SEL('#opening-date'), '31102026', at=c.A(2, 'trinta', 0.1), label='Data-base: 31/10/2026', cps=40, noClick=True)
    c.digita(SEL('#opening-quantity'), '3320', c.A(2, 'quantidade:', 0.7), c.A(2, 'três', 0.2), 'Quantidade: 3320')
    c.mark(3)
    c.hover(TXTX('O saldo fica só no estoque fiscal', within=DLG), 1.5, at=c.A(3, 'fiscal.', 0.6), label='O saldo fica só no estoque fiscal')
    c.mark(4)
    c.click(BTN('Planilha', within=DLG), at=c.A(4, 'planilha:', 0.7), label='aba Planilha')
    c.hover(BTN('Baixar modelo', within=DLG), 0.8, at=c.A(4, 'modelo,', 0.6), label='Baixar modelo')
    c.hover(BTN('Escolher planilha', within=DLG), 0.8, at=c.A(4, 'envia.', 0.6), label='Escolher planilha')
    c.click(BTN('Manual', within=DLG), at=c.A(4, 'gravar.', 0.3), label='volta para Manual')
    c.mark(5)
    c.confere('dlg', ['Bateria automotiva'], 'material da linha já escolhido')
    c.click(BTN('Confirmar saldo inicial'), at=c.A(5, 'Confirmar', 0.7), label='Confirmar saldo inicial')
    c.waitfor(text='Saldo inicial registrado', timeout=10)
    c.cursor(NEUTRO, at=c.A(5, 'aviso', 0.3), label='a faixa amarela some')
    c.mark(6)
    c.hover(SALDO('Bateria automotiva', 'td >> nth=2'), 2.0, at=c.A(6, 'três', 0.6), label='Bateria automotiva: 3.960 kg')
    c.confere('main', ['3.960'], 'bateria com 3.960 kg')
    c.fim()
    return c


@capitulo
def cap15():
    """Posição em uma data (31/10 18:00) e Movimentações: o Kardex do metal amarelo, os Filtros (só mostra) e Geral (Todos)."""
    c = Cap(15, start=(900, 440), setup=setup_em(POSICAO))
    c.mark(1)
    c.click(SUBABA('Posição em uma data'), at=c.A(1, 'Posição', 0.8), label='aba Posição em uma data')
    c.click(SEL('main button', hasText='10/11/2026'), at=c.A(1, 'Escolho', 0.5), label='Data da posição (abre)')
    c.click(SEL('[data-radix-popper-content-wrapper] button[name=previous-month]'), at=c.A(1, 'hora,', 0.5), label='mês anterior')
    c.click(SEL("[data-radix-popper-content-wrapper] button[name=day]:text-is('31')"), at=c.A(1, 'fim', 0.6), label='dia 31/10')
    # a hora: o cursor vai ao campo e o foco entra pelo começo (clique no meio do campo cairia nos minutos)
    c.hover(SEL("main input[aria-label='Hora']"), 0.1, at=c.A(1, 'outubro,', 0.6), label='Hora (campo)')
    c.ev("(()=>{const i=document.querySelector(\"main input[aria-label='Hora']\");if(!i)return 'SEM ALVO';i.focus();return 'foco na hora'})()")
    c.type(SEL("main input[aria-label='Hora']"), '1800', label='Hora: 18:00', cps=14, noClick=True)
    c.click(BTN('Ver posição'), at=c.A(1, 'Ver', 0.7, nth=1), label='Ver posição')
    c.mark(2)
    c.hover(SEL('main tbody tr >> nth=0'), 1.0, at=c.A(2, 'número', 0.6), label='tabela da posição em 31/10')
    c.mark(3)
    c.hover(TXTX('Saldo fiscal em', within='main'), 1.5, at=c.A(3, 'consulta.', 0.6), label='Saldo fiscal em 31/10/2026 às 18:00')
    c.confere('main', ['Saldo fiscal em 31/10/2026'], 'posição de 31/10')
    c.mark(4)
    c.click(SUBABA('Movimentações'), at=c.A(4, 'Movimentações', 0.7), label='aba Movimentações')
    c.click(SEL(f"{MATERIAIS} button", hasText='Metal amarelo (latão)'), at=c.A(4, 'metal', 0.7), label='Materiais: Metal amarelo (latão)')
    c.hover(LINHA('1248', 'td >> nth=0'), 0.6, at=c.A(4, 'linha', 0.6), label='linha da NF-e 1248 (saída de 30/10, 600 kg)')
    c.hover(SEL("main th:has-text('Nota / CFOP')"), 0.3, at=c.A(4, 'CFOP,', 0.6), label='coluna Nota / CFOP')
    c.hover(SEL("main th:has-text('Antes')"), 0.5, at=c.A(4, 'antes', 0.6), label='colunas Antes e Depois')
    c.mark(5)
    c.click(SEL(f"{MATERIAIS} button[aria-expanded]"), at=c.A(5, 'filtros,', 0.7), label='Filtros (abre)')
    c.hover(SEL('#history-start'), 0.5, at=c.A(5, 'período,', 0.6), label='De / Até')
    c.click(SEL(f"{MATERIAIS} button[role=combobox]"), at=c.A(5, 'tipo', 0.6), label='Tipo (abre: Entrada, Saída, Saldo inicial, Ajuste, Estorno)')
    c.press('Escape', at=c.A(5, 'buscar', 0.5), label='fecha a lista de tipos')
    c.hover(SEL('#history-search'), 1.0, at=c.A(5, 'nota,', 0.4), label='Nota, chave ou parceiro')
    c.mark(6)
    c.click(SEL(f"{MATERIAIS} button", hasText='Geral (Todos)'), at=c.A(6, 'Geral', 0.7), label='Geral (Todos)')
    c.hover(TXTX('KARDEX FISCAL', within='main'), 1.0, at=c.A(6, 'todos', 0.5), label='KARDEX FISCAL — Geral')
    c.fim()
    return c


@capitulo
def cap16():
    """Cancelamento e devolução no Kardex: a NF-e 1249 (saída e estorno de 320 kg, com o motivo) e a 1253 (devolução da Fundição,
    +40 kg de cobre mel); as duas ilustrações (régua do estorno, setas da devolução)."""
    c = Cap(16, start=(900, 440), setup=setup_em(POSICAO, extra=[
        {'do': 'click', 'target': SUBABA('Movimentações')}, {'do': 'waitFor', 'text': 'KARDEX FISCAL', 'timeout': 15}, {'do': 'wait', 'seconds': 0.8}]))
    c.mark(1)
    c.click(SEL(f"{MATERIAIS} button[aria-expanded]"), at=c.A(1, 'Lembra', 0.5), label='Filtros (abre)')
    c.digita(SEL('#history-search'), '1249', c.A(1, 'busco', 0.9), c.A(1, 'ela', 0.1), 'Nota, chave ou parceiro: 1249')
    c.mark(2)
    c.waitfor(target=SEL("main tbody tr:has-text('Estorno')"), timeout=10)
    c.registra(SEL('main tbody'), at=c.A(2, 'saída', 0.9), label='as duas linhas da 1249 (zoom)')
    c.hover(SEL("main tbody tr:has-text('Nota fiscal') td >> nth=1"), 0.8, at=c.A(2, 'saída', 0.6), label='Nota fiscal 1249: saída de 320 kg')
    c.hover(SEL("main tbody tr:has-text('Estorno') td >> nth=1"), 0.8, at=c.A(2, 'estorno,', 0.6), label='Estorno 1249: +320 kg')
    c.hover(TXTX('Pedido alterado pelo cliente', within='main tbody'), 1.0, at=c.A(2, 'motivo', 0.6), label='motivo do cancelamento')
    c.confere('main', ['Estorno', 'Pedido alterado pelo cliente antes de a mercadoria sair do pátio', '320'], 'saída e estorno da 1249')
    c.mark(3)
    c.cursor(NEUTRO, at=c.L(3) - 0.1, label='cursor em repouso (ilustração: régua do estorno)')
    c.mark(4)
    c.hover(SEL("main tbody tr:has-text('Estorno') td >> nth=-1"), 1.5, at=c.A(4, 'saldo', 0.9), label='coluna Depois do estorno')
    c.mark(5)
    c.click(BTN('Limpar filtros'), at=c.A(5, 'devolução?', 0.6), label='Limpar filtros')
    c.click(SEL(f"{MATERIAIS} button", hasText='Cobre mel'), at=c.A(5, 'Fundição', 0.6), label='Materiais: Cobre mel')
    c.waitfor(target=LINHA('1253'), timeout=10)
    c.hover(LINHA('1253', 'td >> nth=1'), 0.8, at=c.A(5, 'quarenta', 0.6), label='NF-e 1253: devolução da Fundição')
    c.hover(LINHA('1253', "td:has-text('CFOP')"), 1.2, at=c.A(5, 'nota', 0.6), label='NF-e 1253, CFOP de devolução, +40 kg')
    c.confere('main', ['1253', 'CFOP 1202'], 'devolução (NF-e 1253) no Kardex do cobre mel')
    c.mark(6)
    c.cursor(NEUTRO, at=c.L(6) - 0.1, label='cursor em repouso (ilustração: setas da devolução)')
    c.mark(7)
    c.hover(LINHA('1253', 'td >> nth=-3'), 1.5, at=c.A(7, 'quantidade.', 0.9), label='Movimento: +40 kg')
    c.fim()
    return c


@capitulo
def cap17():
    """Fiscal × operacional de outubro (tela nova desde o 1.60.15: entradas e saídas separadas, diferença = notas − pedidos): os cartões,
    o metal amarelo (Entradas: compras 500 x notas 0 = −500 "sem nota"; Saídas: vendas 500 x notas 1.100 = +600 "nota a mais"; conferir
    no ensaio), a ilustração, o quadro "Como ler a diferença (notas − pedidos)" e Exportar."""
    c = Cap(17, start=(900, 440), setup=setup_em(POSICAO))
    c.mark(1)
    c.click(SUBABA('Fiscal × operacional'), at=c.A(1, 'compara', 0.7), label='aba Fiscal × operacional')
    c.hover(TXTX('Comparação por material', within='main'), 0.4, at=c.A(1, 'lado', 0.6), label='Comparação por material')
    escolhe(c, PERIODO, 'Mês passado', c.A(1, 'Escolho', 0.7), c.A(1, 'passado,', 0.4), 'período: Mês passado', fixo=True)
    c.mark(2)
    c.hover(CARTAO('Entradas com diferença'), 0.6, at=c.A(2, 'compras,', 0.6), label='Entradas com diferença (Compras × notas de entrada)')
    c.hover(CARTAO('Saídas com diferença'), 0.6, at=c.A(2, 'vendas,', 0.6), label='Saídas com diferença (Vendas × notas de saída)')
    c.hover(CARTAO('Materiais conferindo'), 0.6, at=c.A(2, 'conferem', 0.6), label='Materiais conferindo (Pedidos e notas batem)')
    c.hover(CARTAO('Alertas'), 0.8, at=c.A(2, 'alertas.', 0.6), label='Alertas')
    c.mark(3)
    rola_ate(c, 'Metal amarelo (latão)', c.L(3) - 0.2, 'rola até o metal amarelo', y=420, dur_ms=900)
    c.hover(LINHA('Metal amarelo', 'td >> nth=3'), 1.6, at=c.A(3, 'entradas,', 0.5), label='Metal amarelo, Entradas: compras 500, notas 0, diferença −500 sem nota')
    c.mark(4)
    c.hover(LINHA('Metal amarelo', 'td >> nth=3'), 1.2, at=c.A(4, 'pátio,', 0.6), label='(continua) compra de pessoa física sem nota')
    c.mark(5)
    c.hover(LINHA('Metal amarelo', 'td >> nth=6'), 1.6, at=c.A(5, 'saídas,', 0.5), label='Metal amarelo, Saídas: vendas 500, notas 1.100, diferença +600 nota a mais')
    c.confere('main', ['Metal amarelo (latão)', 'sem nota', 'nota a mais'], 'metal amarelo: sem nota nas entradas e nota a mais nas saídas')
    c.cursor(NEUTRO, at=c.A(5, 'Foi', 0.1), label='cursor em repouso (a ilustração fiscal × operacional entra)')
    c.mark(6)
    c.mark(7)
    rola_ate(c, 'Como ler a diferença (notas − pedidos)', c.L(7) - 0.2, 'rola até Como ler a diferença', y=260, prefixo=True)
    c.hover(TXTX('Como ler a diferença', within='main'), 2.0, at=c.A(7, 'quadro,', 0.6), label='Como ler a diferença: Sem nota, Nota a mais, Pedidos não finalizados')
    c.mark(8)
    c.ev(JS_TOPO, at=c.L(8) - 0.2, label='volta ao topo')
    c.click(BTN('Exportar'), at=c.A(8, 'exportar', 0.3), label='Exportar (abre)', noScroll=True)
    c.hover(ITEM('PDF'), 0.5, at=c.A(8, 'PDF', 0.5), label='Exportar estoque fiscal: PDF', noScroll=True)
    c.hover(ITEM('Excel'), 0.8, at=c.A(8, 'Excel', 0.5), label='Exportar estoque fiscal: Excel', noScroll=True)
    c.press('Escape', at=c.A(8, 'contador.', 0.2), label='fecha o menu (sem baixar)')
    c.fim()
    return c


@capitulo
def cap18():
    """Exportação Contábil: Notas Fiscais > Saída > ⋮ > Exportação Contábil, Emitente / CNPJ, Mês passado, notas destinadas marcadas,
    tudo marcado, 21 notas e "Destinadas: 0 XML(s)", Baixar Pacote."""
    c = Cap(18, start=(900, 440), setup=setup_em(POSICAO, aquece=['/fiscal-ambiental/nfe/saida'], menu='Notas Fiscais (NF-e)'))
    c.mark(1)
    c.click(ITEM_MENU('Notas Fiscais (NF-e)'), at=c.A(1, 'Notas', 0.9), label='Notas Fiscais (NF-e) no menu')
    c.click(SUBABA('Saída'), at=c.A(1, 'Fiscais,', 0.0), label='aba Saída')
    c.click(SEL("main button[aria-label='Mais opções de NF-e']"), at=c.A(1, 'três', 0.7), label='Mais opções de NF-e (⋮)')
    c.click(ITEM('Exportação Contábil'), at=c.A(1, 'Exportação', 0.6), label='Exportação Contábil', noScroll=True)
    c.waitfor(text='Baixar Pacote', timeout=10)
    c.mark(2)
    c.hover(TXTX('Gera um pacote ZIP com XMLs', within=DLG), 1.2, at=c.A(2, 'XML', 0.6), label='descrição do pacote')
    c.mark(3)
    c.hover(SEL('#export-fiscal-config'), 1.2, at=c.A(3, 'CNPJ,', 0.6), label='Emitente / CNPJ: Todos os CNPJs')
    c.mark(4)
    escolhe(c, SEL('[role=dialog] button[role=combobox] >> nth=1'), 'Mês passado', c.A(4, 'período,', 0.6), c.A(4, 'passado.', 0.3), 'Período: Mês passado')
    c.mark(5)
    c.click(TXT('Incluir notas destinadas ao CNPJ', within=DLG), at=c.A(5, 'incluir', 0.7), label='marca Incluir notas destinadas ao CNPJ')
    c.hover(TXTX('XMLs de NF-e emitidas por fornecedores', within=DLG), 1.5, at=c.A(5, 'XML', 0.6), label='XMLs de NF-e emitidas por fornecedores (xmls/destinadas)')
    c.mark(6)
    c.hover(TXT('Tipo de nota', within=DLG), 0.5, at=c.A(6, 'Saída', -0.2), label='Tipo de nota: Saída e Entrada')
    c.hover(TXT('Status', within=DLG), 0.8, at=c.A(6, 'status,', 0.6), label='Status: todos marcados')
    c.mark(7)
    c.hover(TXTX('Incluir DANFEs (PDFs)', within=DLG), 0.6, at=c.A(7, 'PDF', 0.6), label='Incluir DANFEs (PDFs)')
    c.hover(TXTX("Incluir MDF-e", within=DLG), 0.8, at=c.A(7, 'manifestos', 0.6), label="Incluir MDF-e's")
    c.mark(8)
    c.hover(TXTX('notas no período', within=DLG), 0.8, at=c.A(8, 'prévia', 0.6), label='prévia: 21 notas no período')
    c.hover(TXTX('Destinadas:', within=DLG), 1.5, at=c.A(8, 'destinadas', 0.6), label='Destinadas: 0 XML(s)')
    c.confere('dlg', ['21 notas no período', '12 saída', '9 entrada', 'Destinadas: 0 XML(s)'], 'prévia de outubro')
    c.mark(9)
    c.click(BTN('Baixar Pacote'), at=c.A(9, 'Baixar', 0.7), label='Baixar Pacote')
    c.waitfor(text='Exportação pronta', timeout=40)
    c.cursor(NEUTRO, at=c.A(9, 'computador.', 0.2), label='cursor em repouso (download)')
    c.fim()
    return c


@capitulo
def cap19():
    """O que o contador faz: só ilustração (o pacote, o caminho até o contador, a cópia guardada); a tela fica parada na lista de Saída."""
    c = Cap(19, start=(900, 470), setup=setup_em('/fiscal-ambiental/nfe/saida'))
    c.mark(1)
    c.cursor(NEUTRO, at=0.5, label='cursor em repouso (ilustração do pacote)')
    for i in (2, 3, 4):
        c.marca_ja(i)
    c.fim()
    return c


@capitulo
def cap20():
    """Recapitulando: montagem das gravações dos capítulos 2 a 18 por cima; a tela fica parada em Transporte com o nº 1 encerrado."""
    c = Cap(20, start=(900, 470), setup=setup_em('/fiscal-ambiental/transporte'), obs=False)
    c.mark(1)
    c.cursor(NEUTRO, at=0.5, label='cursor em repouso (montagem)')
    for i in (2, 3, 4):
        c.marca_ja(i)
    c.fim()
    return c


def main():
    quais = [int(a) for a in sys.argv[1:] if not a.startswith('-')] or sorted(CAPS_ROBO)
    json.dump({f'{n:02d}': FAKE_NOW[n] for n in FAKE_NOW}, open(os.path.join(HERE, 'fake_now.json'), 'w', encoding='utf8'), indent=1)
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
