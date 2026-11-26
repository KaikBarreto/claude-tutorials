#!/usr/bin/env python3
"""T12 · Coletas e Logística: gera rec/t12/cap00..cap17.json (roteiros do robô) a partir da voz (t12/narracao/capNN.json).

EcoSistema 1.60.18 no Supabase falso (mundo da Recicla Vale Metais), computador 1600x900, logado como Rafael Nogueira (MASTER).
Cada passo é preso a uma palavra da fala: `at` = início da palavra - folga (o custo do gesto, docs/04 "Custo real dos gestos"), e a marca
Ln entra no início de cada linha. Quando a voz chegar, rodar de novo com o capNN.json da voz (nada a reescrever).
O cap17 (Recapitulando) é um passeio calmo pelo estado final (quadro, Frota, Equipamentos, Rastreamento, Relatório e Configurações), como
na T08 e na T06 (fechamento de 21/11).
Rodar de qualquer pasta: `python3 -I rec/t12/gerar.py [NN ...]`; ensaiar em lote: `bash rec/t12/t12_lote.sh NN [NN ...]`.

Renumeração de 20/11 (aplicação do 1.60.18): novos 7 (editar, cancelar e excluir), 8 (relatório para o parceiro), 12 (movimentações e ficha do
parceiro), 13 (rastreamento) e 16 (checklist e assinaturas); o antigo 7 (portal) virou 9, 8 (frota) 10, 9 (caçambas) 11, 10 (relatório) 14, 11
(regras) 15 e 12 (recapitulando) 17.

Relógio (MUNDO_LINHA_DO_TEMPO.md, "O dia 10/11"): FAKE_NOW 10/11/2026 07:00 em todos os capítulos.
Cadeia de sementes (seeds-extra/t12; inicio = t12_sementes.py; as outras saem de t12_semente.py, do estado da instância 54312 logo depois do
ensaio do capítulo): inicio -> apos-cap05 (ordem 9) -> apos-cap06 (ordem 8 concluída com caçambas 03 e 05 e 10 bags) -> apos-cap07 (observação
da ordem 9) -> apos-cap09 (ordem 10 do portal, agendada) -> apos-cap10 (FVL8A52, Sérgio Paiva) -> apos-cap11 (tipo Palete, Caçamba 02 em
manutenção, Caçamba 06 na base) -> apos-cap12 (10 bags para a Cooperativa) -> apos-cap15 (prefixo COL- e antecedência de 24 h). O cap13 soma a
semente `rastreamento` (t12_rastreamento.py). Os caps 8, 14 só leem; o cap16 deixa o checklist e a assinatura (não vira semente: a T20 parte
do `apos-cap15`).
Particularidades:
 - A ordem interna nasce "Agendada" e o app não grava evento de criação: o Histórico da ordem 8 mostra só as mudanças de etapa.
 - Tela da ordem: o rodapé "Concluir coleta" é fixo (fora da faixa de clique): clicar_fixo.
 - GPS: o setup do cap06 dá ao navegador uma posição fictícia perto do Depósito Irmãos Siqueira (GPS_FICTICIO).
 - Portal (cap09): mesma aba (o vídeo grava uma aba só); o robô entra logado (setup), abre o portal da Cooperativa Recomeço e, depois do
   pedido, volta ao sistema pela rota /coletas/frota (o menu revalida as solicitações não vistas e mostra o ponto vermelho).
 - Mapa do cap13: Leaflet e tiles pelos handlers de rede externa (cdnjs, arcgisonline) do mundo.
"""
import hashlib
import json
import os
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TUT = os.path.normpath(os.path.join(HERE, '..', '..'))
NARR = os.path.join(TUT, 't12', 'narracao')
NOW = '2026-11-10T07:00:00-03:00'
FAKE_NOW = {n: NOW for n in range(18)}



def stable_id(chave):
    """o mesmo UUID estável do Supabase falso (core/util.mjs stableId)"""
    h = bytearray(hashlib.sha1(('domiflix-fake:' + chave).encode()).digest())
    h[6] = (h[6] & 0x0F) | 0x50
    h[8] = (h[8] & 0x3F) | 0x80
    x = h[:16].hex()
    return f'{x[:8]}-{x[8:12]}-{x[12:16]}-{x[16:20]}-{x[20:32]}'


RAFAEL = stable_id('user.rafael')
TOKEN_COOP = stable_id('t12.portal.recomeco')   # portal_token da Cooperativa Recomeço (t12_sementes.py)
try:
    VERSAO = open(os.path.join(TUT, 'app', 'dist', '.versao-app'), encoding='utf8').read().strip() or '1.60.18'
except OSError:
    VERSAO = '1.60.18'
HOJE = '2026-11-10'
EMPRESA = '38814e47-876a-5977-a5f7-53af364c17bb'
STORAGE = {
    f'cato_adoption_nudge_{EMPRESA}_{RAFAEL}': '{"count":99,"lastShownAt":4102444800000}',   # cala o balão de dica do Cato (regra do mundo)
    'app_version': VERSAO, 'notification_shown_version': VERSAO, f'dominex:daily-tasks-shown:{RAFAEL}': HOJE,
    'pwa-install-dismissed': 'true', 'theme': 'light', f'daily-tasks-reminder-last-shown-{RAFAEL}': HOJE, 'initial-preferences-set': 'true',
}
NOMES = ['Abertura', 'O que o módulo de Coletas resolve', 'O quadro das ordens', 'Criar uma ordem', 'Data e janela', 'Motorista e veículo',
         'Acompanhar até concluir', 'Editar, cancelar e excluir', 'O relatório para o parceiro', 'A coleta pedida pelo portal',
         'Veículos e motoristas', 'As caçambas e onde estão', 'Movimentações e a ficha do parceiro', 'Onde está o caminhão',
         'O relatório das coletas', 'As regras das coletas', 'Checklist e assinaturas', 'Recapitulando']
SEMENTE = {0: None, 1: None, 2: None, 3: None, 4: None, 5: None, 6: 'apos-cap05', 7: 'apos-cap06', 8: 'apos-cap07', 9: 'apos-cap07',
           10: 'apos-cap09', 11: 'apos-cap10', 12: 'apos-cap11', 13: 'apos-cap12', 14: 'apos-cap12', 15: 'apos-cap12', 16: 'apos-cap15', 17: 'apos-cap16'}


def sementes(n):
    """a semente de cada capítulo é cumulativa (tudo desde o início da aula): só a última da cadeia vai junto da base"""
    return ['t12/inicio'] + ([f't12/{SEMENTE[n]}'] if SEMENTE[n] else []) + (['t12/rastreamento'] if n in (13, 17) else [])


def norm(s):
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode().lower()
    return ''.join(ch for ch in s if ch.isalnum() or ch in '?')


def carregar_voz(n):
    d = json.load(open(os.path.join(NARR, f'cap{n:02d}.json'), encoding='utf8'))
    return d['words'], d['linhas'], float(d['dur']), bool(d.get('estimado'))


# Observador de avisos de erro na tela (aceite): "Não foi possível", "Erro ao", "Tente novamente", "indisponível", "Algo deu errado",
# "Falha ao", "Transição inválida", "não encontrad" e a faixa "Lembrete da trilha" da EcoFlix. O passo final devolve a lista.
OBS = ("(()=>{window.__avisos=[];const re=/N[ãa]o foi poss[ií]vel|Erro ao|Tente novamente|indispon[ií]vel|Algo deu errado|Falha ao|"
       "Transi[çc][ãa]o inv[áa]lida|n[ãa]o encontrad|Localiza[çc][ãa]o n[ãa]o registrada|Sem sinal de GPS/i;"
       "const chk=(t)=>{t=(t||'').trim();const m=t&&t.match(new RegExp('[^]{0,40}('+re.source+')[^]{0,40}','i'));"
       "if(m&&window.__avisos.length<10)window.__avisos.push(m[0].replace(/[\\n\\r\\t ]+/g,' '))};new MutationObserver(ms=>{for(const m of ms){"
       "m.addedNodes.forEach(n=>chk(n.textContent));if(m.type==='characterData')chk(m.target.textContent)}}).observe(document.body,"
       "{childList:true,subtree:true,characterData:true});chk(document.body.innerText);"
       "setInterval(()=>{const f=document.querySelector('section[aria-label^=\"Lembrete da trilha\"]');"
       "if(f&&window.__avisos.length<10&&!window.__avisos.includes('TRILHA ECOFLIX'))window.__avisos.push('TRILHA ECOFLIX')},300);return 1})()")

# Animação do framer-motion (opacity 0 inline) que o relógio simulado do Playwright deixa começar no futuro (currentTime < 0): a tela
# ficaria em branco por segundos (portal, cartões que entram). Efeito do ambiente, não do app (08-licoes, T5 cap. 10): a cada 100 ms,
# a animação presa começa agora.
ANIM_FIX = ("(()=>{if(window.__animFix)return 'ja';window.__animFix=setInterval(()=>{for(const a of document.getAnimations())"
            "if(a.currentTime!==null&&a.currentTime<0)a.startTime=document.timeline.currentTime},100);return 'anim fix'})()")

# GPS fictício (cap06): o navegador do robô no computador não tem permissão de localização; a posição fica perto do Depósito Irmãos
# Siqueira (Tremembé), nunca aparece na tela (o rastreamento está fora da aula) e só evita a nota "Localização não registrada".
GPS_FICTICIO = ("(()=>{const p=()=>({coords:{latitude:-22.9668,longitude:-45.5416,accuracy:12,altitude:null,altitudeAccuracy:null,heading:null,"
                "speed:null},timestamp:Date.now()});const g=navigator.geolocation;g.getCurrentPosition=(ok)=>setTimeout(()=>ok(p()),120);"
                "g.watchPosition=(ok)=>{setTimeout(()=>ok(p()),300);return 7};g.clearWatch=()=>{};return 'gps ficticio'})()")


class Cap:
    def __init__(s, n, pace=0.5, cps=9, start=(900, 440), setup=None, noscroll=False, sameTab=False):
        s.n = n
        s.words, s.linhas, s.dur, s.estimada = carregar_voz(n)
        s.steps = []
        s.pace, s.cps, s.start = pace, cps, start
        s.noscroll = noscroll
        s.sameTab = sameTab
        s.setup = list(setup or []) + [{'do': 'eval', 'js': OBS}, {'do': 'eval', 'js': ANIM_FIX}]
        s.anchors = []
        s.pending = []

    # ---- tempo
    def L(s, i):
        return round(s.linhas[i - 1]['s'], 2)

    def W(s, i, palavra, nth=0):
        q = norm(palavra)
        hits = [w for w in s.words if w['linha'] == i - 1 and norm(w['w']).startswith(q)]
        if hits and len(hits) <= nth:
            print(f'  aviso cap{s.n:02d}: "{palavra}" nth={nth} so tem {len(hits)} na linha {i}; usando a ultima')
            nth = len(hits) - 1
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
            d['at'] = round(max(d['at'], getattr(s, '_ult', 0.0)), 2)   # o `at` precisa ser crescente
            s._ult = d['at']
            lim = 0.8 if d.get('do') == 'hover' else 0.5   # gesto que começa até 0,5 s antes da linha espera a marca (marca no início da linha)
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

    def press(s, key, at=None, label=None, **kw):
        return s._p({'do': 'press', 'key': key}, at, label, kw)

    def rolar(s, by, at=None, label=None, ponto=(900, 440), duration=0.5, after=100):
        return s._p({'do': 'scroll', 'point': {'x': ponto[0], 'y': ponto[1]}, 'by': by, 'duration': duration, 'after': after}, at, label, {})

    def cursor(s, ponto, at=None, label=None):
        """leva o cursor a um ponto neutro (scroll de 0 px): tira o mouse de cima de um menu ou de um cartão"""
        return s._p({'do': 'scroll', 'point': {'x': ponto[0], 'y': ponto[1]}, 'by': 0, 'duration': 0.3, 'after': 0}, at, label, {})

    def aponta(s, ponto, at, label):
        """passeio: leva o cursor a um ponto fixo da tela (posições medidas na exploração, rec/t12/_ex); ~0,6 s contra ~1,5 s de um hover"""
        return s.cursor(ponto, at=round(max(0.0, at), 2), label=label)

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

    def confere_kpi(s, pares, label, rotulos='main *'):
        """LÊ cada cartão de número pelo rótulo (folha com o texto exato, entre os `rotulos`) e compara o número com o que a fala diz"""
        js = ("(async()=>{const pares=%s;let out='';for(let i=0;i<22;i++){const falta=[];for(const [rot,val] of pares){"
              "const el=[...document.querySelectorAll(" + json.dumps(rotulos) + ")].find(e=>e.children.length===0&&e.textContent.trim()===rot);"
              "if(!el){falta.push(rot+'=?');continue;}let c=el.parentElement,ok=false;for(let k=0;k<4&&c;k++,c=c.parentElement){"
              "const ls=c.innerText.split('\\n').map(x=>x.trim()).filter(Boolean);if(ls.length>1){ok=ls.includes(val);if(!ok)falta.push(rot+'='+ls.filter(x=>x!==rot).slice(0,2).join('/'));break;}}"
              "}if(!falta.length)return 'OK: '+pares.map(p=>p.join(' ')).join(' | ');out='DIFERENTE: '+falta.join(' | ');"
              "await new Promise(r=>setTimeout(r,300));}return out})()") % json.dumps(pares, ensure_ascii=False)
        return s.add({'do': 'eval', 'js': js, 'label': 'confere ' + label})

    def confere_item(s, sel, item, esperados, label):
        """LÊ o primeiro `sel` cujo texto tem `item` e compara com o que a fala diz"""
        esp = [esperados] if isinstance(esperados, str) else list(esperados)
        js = ("(async()=>{const esp=%s;let out='';for(let i=0;i<22;i++){const el=[...document.querySelectorAll(%s)].find(e=>e.innerText.includes(%s));"
              "if(!el){out='DIFERENTE: sem '+%s;}else{const t=el.innerText.replace(/\\s+/g,' ');const falta=esp.filter(e=>!t.includes(e));"
              "if(!falta.length)return 'OK: '+%s+' '+esp.join(' | ');out='DIFERENTE: faltou '+JSON.stringify(falta)+' em: '+t.slice(0,200);}"
              "await new Promise(r=>setTimeout(r,300));}return out})()") % (json.dumps(esp, ensure_ascii=False), json.dumps(sel), json.dumps(item),
                                                                           json.dumps(item), json.dumps(item))
        return s.add({'do': 'eval', 'js': js, 'label': 'confere ' + label})

    def fim(s):
        s.flush(1e9)
        s.steps.append({'do': 'eval', 'js': 'JSON.stringify(window.__avisos || "sem observador")', 'label': 'avisos de erro na tela'})
        s.steps.append({'do': 'mark', 'name': 'FIM', 'at': round(s.dur, 2)})

    def out(s):
        d = {
            'name': f't12-cap{s.n:02d}',
            'title': f'T12 · Cap. {s.n} · {NOMES[s.n]} (narração {str(round(s.dur, 1)).replace(".", ",")} s{" ESTIMADA" if s.estimada else ""}; '
                     f'marcas L1..L{len(s.linhas)} = início de cada linha do roteiro; FAKE_NOW {FAKE_NOW[s.n]})',
            'seed': f't12-cap{s.n:02d}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
            'start': {'x': s.start[0], 'y': s.start[1]},
            'anonymous': True, 'storage': dict(STORAGE),
            'seedExtra': sementes(s.n),
            'prewarm': ['/login'], 'setup': s.setup, 'steps': s.steps,
        }
        if s.sameTab:
            d['sameTab'] = True
        return d


# ---------------------------------------------------------------- alvos
BTN = lambda n, **kw: {'role': 'button', 'name': n, 'exact': True, **kw}
BTNX = lambda n, **kw: {'role': 'button', 'name': n, **kw}
LINK = lambda n, **kw: {'role': 'link', 'name': n, 'exact': True, **kw}
TAB = lambda n, **kw: {'role': 'tab', 'name': n, 'exact': True, **kw}
TXT = lambda t, **kw: {'text': t, 'exact': True, **kw}
TXTX = lambda t, **kw: {'text': t, **kw}
SEL = lambda s, **kw: {'selector': s, **kw}
OPT = lambda n, **kw: {'role': 'option', 'name': n, 'exact': True, **kw}
PH = lambda p, **kw: {'placeholder': p, **kw}
DLG = '[role=dialog]'
MENU = 'aside, [data-sidebar=sidebar]'
CARTAO = lambda num: f"main div.cursor-pointer.rounded-2xl:has(span.font-semibold:text-is('#{num}'))"     # cartão #N do quadro
COLUNA = lambda titulo: f"main div:has(> div :text-is('{titulo}'))"


def js_clicar(sel, texto=None):
    """clique por eval (botão fixo): o primeiro `sel` visível (com o texto, se dado)"""
    filtro = f"&&(b.textContent||'').includes({json.dumps(texto)})" if texto else ''
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
    '/coletas/ordens': 'Solicite, agende e acompanhe as ordens de coleta',
    '/coletas/frota': 'Veículos e motoristas disponíveis para as coletas',
    '/coletas/equipamentos': 'Caçambas, bags, caixas e paletes em campo',
    '/coletas/rastreamento': 'Acompanhe a frota em tempo real',
    '/coletas/relatorio': 'Indicadores e histórico das coletas',
    '/coletas/configuracoes': 'Ajuste a numeração, as janelas e as regras do portal de coletas',
}


def ir(rota, espera=0.8):
    st = [{'do': 'goto', 'url': rota}]
    if PAGINAS.get(rota):
        st.append({'do': 'waitFor', 'text': PAGINAS[rota], 'timeout': 30})
    return st + [{'do': 'waitFor', 'idle': True, 'timeout': 25}, {'do': 'wait', 'seconds': espera}]


def setup_em(rota, extra=(), aquece=()):
    """login, aquece as rotas que o capítulo visita e para em `rota`"""
    st = list(LOGIN)
    for r in aquece:
        st += ir(r, 0.3)
    return st + ir(rota) + list(extra)


# rolagem suave do contêiner que rola o alvo (molde do T14/T11/T8: ACHA_ROLAGEM + SUAVE): o cursor não se mexe
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


# ================================================================ capítulos
CAPS_ROBO = {}


def capitulo(fn):
    CAPS_ROBO[int(fn.__name__[3:])] = fn
    return fn


# Folga das âncoras (o custo do gesto até o cursor CHEGAR, docs/04): FC no clique, FH no hover. Medidas no ensaio rápido sem render ao
# lado (depois das 17:35 de 11/11); com a máquina carregada os gestos ficam 1,5 a 2x mais lentos (aviso do coordenador).
FC, FH = 0.6, 0.6        # ensaio rápido do cap06 às 21:00 (máquina sem render): clique e hover chegam em ~0,4 a 0,6 s
F1 = 1.8                 # 1º clique do capítulo (página recém-carregada): ~2 s até o cursor chegar
FJ = 1.0                 # 1º clique dentro de uma janela ou página recém-aberta

# ---------------------------------------------------------------- alvos das telas de Coletas (conferidos por exploração, rec/t12/_ex)
GRUPO = BTNX('Coletas & Logística', within=MENU)
ITEM_MENU = lambda n: LINK(n, within=MENU)
ORDENS_MENU = {'role': 'link', 'name': 'Ordens de Coleta', 'within': MENU}   # sem exact: com solicitações novas o ponto vermelho entra no nome (aria-label)
COL_T = lambda t: SEL(f"main h3:text-is('{t}')")                                  # título da coluna do quadro
CARD = lambda num, sub='': SEL(f"{CARTAO(num)} {sub}".strip())
CARD_TXT = lambda num, t: SEL(f"{CARTAO(num)} :text-is('{t}')")
CARD_BTN = lambda num, t: SEL(f"{CARTAO(num)} button:text-is('{t}')")
NOVA_ORDEM = BTN('Nova ordem')
PASSO = lambda t: SEL(f"{DLG} span:text-is('{t}')")                                # etapas da Nova ordem
AVANCAR = BTN('Avançar')
BUSCA_PARC = PH('Buscar por nome, apelido, CPF/CNPJ ou telefone...')
MOTORISTA, VEICULO = PH('Digite ou busque o motorista'), PH('Digite ou busque a placa')


def setup_nova_ordem(ate_etapa):
    """refaz fora do vídeo a Nova ordem da Auto Peças Vale Forte até a etapa pedida (2 = Coleta preenchida, 3 = Frota)"""
    st = [{'do': 'click', 'target': NOVA_ORDEM}, {'do': 'waitFor', 'text': 'Nova ordem de coleta', 'timeout': 10}, {'do': 'wait', 'seconds': 0.5},
          {'do': 'click', 'target': SEL(f"{DLG} button:has-text('Selecionar')")}, {'do': 'waitFor', 'target': BUSCA_PARC, 'timeout': 10},
          {'do': 'type', 'target': BUSCA_PARC, 'text': 'Vale Forte', 'cps': 40}, {'do': 'wait', 'seconds': 0.6},
          {'do': 'click', 'target': BTNX('Auto Peças Vale Forte', within=f'{DLG} >> nth=-1')}, {'do': 'wait', 'seconds': 0.6},
          {'do': 'click', 'target': AVANCAR}, {'do': 'waitFor', 'target': SEL('#ordem-material'), 'timeout': 10},
          {'do': 'type', 'target': SEL('#ordem-material'), 'text': '~400 kg de radiadores e baterias', 'cps': 40},
          {'do': 'type', 'target': SEL('#ordem-obs'), 'text': 'Retirar pelo portão lateral', 'cps': 40}]
    if ate_etapa >= 3:
        st += [{'do': 'type', 'target': SEL('#ordem-data'), 'text': '11112026', 'cps': 40},
               {'do': 'click', 'target': SEL('#ordem-janela')}, {'do': 'click', 'target': OPT('Manhã')}, {'do': 'wait', 'seconds': 0.4},
               {'do': 'click', 'target': AVANCAR}, {'do': 'waitFor', 'target': MOTORISTA, 'timeout': 10}]
    return st + [{'do': 'wait', 'seconds': 0.8}]


