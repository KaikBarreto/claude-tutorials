#!/usr/bin/env python3
"""T26 · gera rec/t26/cap00..cap13.json (roteiros do robô) a partir da voz ($TUT_HOME/t26/narracao/capNN.json).

CRM/Kanban no COMPUTADOR (janela 1280x800), logado como Rafael Nogueira (MASTER, Recicla Vale Metais), no EcoSistema 1.59.154.
O login roda no `setup` (não filmado), com "$TUT_USER"/"$TUT_SENHA" do ambiente: o capítulo abre o navegador sem sessão
("anonymous") e o `storage` só marca o que a primeira entrada mostraria por cima da tela (novidades da versão, lembrete das
tarefas do dia, preferências iniciais).
Relógio do mundo: FAKE_NOW 10/11/2026 08:30 nos capítulos 0 a 11 e 13; 17:30 no cap12 (o fim do dia). O mesmo FAKE_NOW no
Supabase falso e no robô (ver o campo "fakeNow" de cada capNN.json e rec/t26/t26_rodar.sh).
Os `at` saem da palavra que anuncia cada passo: A(linha, palavra, folga) = início da palavra - folga (o custo do gesto, docs/04).
Respiros (RESPIROS): um capítulo com "corte" (o cap09 recarrega a tela fora do vídeo) precisa de um vão na voz entre duas
linhas; com a voz sem o vão, o gerador desloca as linhas seguintes e AVISA (a voz pede `pausas.py NN T:DUR`, ver
planejamento/ecoflix/T26/propostas_fala.md). A voz com os respiros vai para rec/t26/_voz/capNN.json (o resumo.py lê de lá).
Rodar de qualquer pasta: `python3 -I rec/t26/gerar.py [NN ...]`. Depois: `node rec/record.mjs rec/t26/capNN.json --check`.

Cadeia de sementes (seeds-extra/t26/): inicio (caps 0 e 1) -> apos-cap01 (2 e 3) -> apos-cap03 (4) -> apos-cap04 (5) -> apos-cap05 (6)
-> apos-cap06 (7) -> apos-cap07 (8) -> apos-cap08 (9) -> apos-cap09 (10) -> apos-cap10 (11) -> apos-cap11-dia (12 e 13).
Cada apos-capNN sai do ensaio do capítulo (rec/t26/aux/t26_semente.mjs, na mesma trava), menos apos-cap11-dia (apos-cap11 + as
cinco oportunidades do dia, rec/t26/aux/t26_dia.py).

Particularidades (achadas na exploração, 10/11):
 - Menu lateral recolhido no `setup` a partir do cap02: a 1280 px com o menu aberto o cartão "Total de oportunidades" sai cortado
   ("Total de oportuni...") e o quadro mostra 3,5 colunas. Caps 0 e 1 ficam com o menu aberto (o item "CRM/Kanban" é o assunto).
 - Janelas empilhadas (Configurações > Configurar etapa): o `within` de cada janela é pelo campo que só ela tem (CFG, ETAPA...).
 - Campo de cor é <input type=color>: o seletor nativo não aparece na gravação; o cursor vai ao campo e a cor entra por `eval`
   (setter nativo + evento input, o que o React ouve), como se escolhida no seletor.
 - Arrastar linha de funil/estágio (HTML5) e cartão (@dnd-kit, alça "Mover oportunidade") funcionam com o `drag` do robô.
 - Trava (cap09): o quadro deixa o cartão desenhado no destino depois do erro (achado 3 do inventário). O "corte" recarrega a tela
   saindo e voltando ao CRM (navegação interna): o quadro remonta na verdade do banco; o selo de tarefas abertas só se atualiza
   com a consulta vencida (30 s), por isso o setup do cap09 espera ~30 s antes de gravar.
 - Observador `OBS` guarda em window.__avisos todo aviso de erro do app; o passo final devolve a lista (tem de sair vazia; no cap09
   o aviso da trava é o que o roteiro pede e não casa com os padrões de erro).
"""
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TUT_HOME = os.path.normpath(os.path.join(HERE, '..', '..'))
NARR = os.path.join(TUT_HOME, 't26', 'narracao')
VOZ_PROV = os.path.join(HERE, '_voz')

RAFAEL = '34c36c63-0890-5e89-8963-7c77b7996908'      # stableId('user.rafael') do mundo
try:
    VERSAO = open(os.path.join(TUT_HOME, 'app', 'dist', '.versao-app'), encoding='utf8').read().strip() or '1.59.154'
except OSError:
    VERSAO = '1.59.154'
FAKE_NOW = {n: '2026-11-10T08:30:00-03:00' for n in range(14)}
FAKE_NOW[12] = '2026-11-10T17:30:00-03:00'
HOJE = {n: FAKE_NOW[n][:10] for n in range(14)}

NOMES = ['Abertura', 'O funil de vendas', 'Funil, Tarefas e os cartões', 'Funis e estágios', 'Nome, cor e orientação',
         'Regras do estágio', 'Automações', 'Checklists e etiquetas', 'Nova oportunidade', 'Arrastar o cartão',
         'A ficha da oportunidade', 'Tarefas e Agenda', 'Filtros e busca', 'Recapitulando']
SEMENTE = {0: 'inicio', 1: 'inicio', 2: 'apos-cap01', 3: 'apos-cap01', 4: 'apos-cap03', 5: 'apos-cap04', 6: 'apos-cap05',
           7: 'apos-cap06', 8: 'apos-cap07', 9: 'apos-cap08', 10: 'apos-cap09', 11: 'apos-cap10', 12: 'apos-cap11-dia',
           13: 'apos-cap11-dia'}
# capítulos cujo estado final vira semente do seguinte (o ensaio grava seeds-extra/t26/apos-capNN.json)
GRAVA_SEMENTE = (1, 3, 4, 5, 6, 7, 8, 9, 10, 11)
# vão mínimo (s) na voz ANTES da linha (1-based): o corte do cap09 recarrega a tela entre a linha 1 e a 2 e entre a 3 e a 4
RESPIROS = {9: {2: 3.4, 4: 3.4}}


# ---------------------------------------------------------------- voz
def norm(s):
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode().lower()
    return ''.join(ch for ch in s if ch.isalnum() or ch in '?')


def carregar_voz(n):
    """voz do capítulo ($TUT_HOME/t26/narracao/capNN.json, estimada ou da voz de verdade) com os RESPIROS aplicados.
    Devolve (words, linhas, dur, estimada, respiros_pendentes)."""
    real = json.load(open(os.path.join(NARR, f'cap{n:02d}.json'), encoding='utf8'))
    words = [dict(w) for w in real['words']]
    linhas = [dict(l) for l in real['linhas']]
    dur = float(real['dur'])
    pend = []
    for li, need in sorted(RESPIROS.get(n, {}).items()):
        i = li - 1
        if i <= 0 or i >= len(linhas):
            continue
        gap = linhas[i]['s'] - linhas[i - 1]['e']
        if gap + 0.02 >= need:
            continue
        d = round(need - gap, 2)
        pend.append((li, round(linhas[i - 1]['e'], 2), d))
        for w in words:
            if w['linha'] >= i:
                w['s'] = round(w['s'] + d, 3)
                w['e'] = round(w['e'] + d, 3)
        for l in linhas[i:]:
            l['s'] = round(l['s'] + d, 3)
            l['e'] = round(l['e'] + d, 3)
        dur = round(dur + d, 3)
    prov = os.path.join(VOZ_PROV, f'cap{n:02d}.json')   # o resumo.py lê esta voz quando existe (senão a de narracao/)
    if pend:
        os.makedirs(VOZ_PROV, exist_ok=True)
        json.dump({'cap': n, 'estimado': bool(real.get('estimado')), 'respiros_pendentes': pend, 'dur': dur, 'words': words,
                   'linhas': linhas}, open(prov, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    elif os.path.exists(prov):
        os.remove(prov)
    return words, linhas, dur, bool(real.get('estimado')), pend


# ---------------------------------------------------------------- observador de avisos de erro na tela (aceite)
OBS = ("(()=>{window.__avisos=[];const re=/N[ãa]o foi poss[ií]vel|Erro ao|Tente novamente|indispon[ií]vel|Algo deu errado|Falha ao|"
       "Something went wrong/i;const chk=(t)=>{t=(t||'').trim();const m=t&&t.match(new RegExp('[^]{0,40}('+re.source+')[^]{0,40}','i'));"
       "if(m&&window.__avisos.length<10)window.__avisos.push(m[0].replace(/[\\n\\r\\t ]+/g,' '))};new MutationObserver(ms=>{for(const m of ms){"
       "m.addedNodes.forEach(n=>chk(n.textContent));if(m.type==='characterData')chk(m.target.textContent)}}).observe(document.body,"
       "{childList:true,subtree:true,characterData:true});chk(document.body.innerText);return 1})()")


class Cap:
    def __init__(s, n, pace=0.5, cps=22, start=(760, 470), setup=None, prewarm=None, recolhe=True):
        s.n = n
        s.words, s.linhas, s.dur, s.estimada, s.respiros = carregar_voz(n)
        s.steps = []
        s.pace, s.cps, s.start = pace, cps, start
        s.prewarm = prewarm or ['/login']
        s.setup = LOGIN + ([RECOLHE, {'do': 'wait', 'seconds': 0.7}] if recolhe else []) + list(setup or []) + [{'do': 'eval', 'js': OBS}]
        s.anchors = []
        s.pending = []

    # ---- tempo
    def L(s, i):
        return round(s.linhas[i - 1]['s'], 2)

    def Lfim(s, i):
        return round(s.linhas[i - 1]['e'], 2)

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

    def type(s, target, text, at=None, label=None, cps=None, **kw):
        d = {'do': 'type', 'target': target, 'text': text}
        if cps:
            d['cps'] = cps
        return s._p(d, at, label, kw)

    def select(s, target, option, at=None, label=None, **kw):
        return s._p({'do': 'select', 'target': target, 'option': option}, at, label, kw)

    def press(s, key, at=None, label=None, **kw):
        return s._p({'do': 'press', 'key': key}, at, label, kw)

    def drag(s, target, to, at=None, label=None, **kw):
        return s._p({'do': 'drag', 'target': target, 'to': to}, at, label, kw)

    def ev(s, js, at=None, label=None, **kw):
        return s._p({'do': 'eval', 'js': js}, at, label, kw)

    def pause(s, seconds):
        return s.add({'do': 'pause', 'seconds': seconds})

    def wait(s, seconds):
        return s.add({'do': 'wait', 'seconds': seconds})

    def waitfor(s, **kw):
        return s.add({'do': 'waitFor', **kw})

    def marcar(s, target, at=None, label=None, **kw):
        """registra o retângulo do alvo para a edição (zoom/destaque) SEM mexer o mouse (passo `type` sem clique e sem texto)"""
        kw.setdefault('optional', True)
        kw.setdefault('timeout', 4)
        return s._p({'do': 'type', 'target': target, 'text': '', 'noClick': True}, at, label, kw)

    def cursor(s, ponto, at=None, label=None, dur=0.4):
        """leva o cursor a um ponto neutro (scroll de 0 px): tira o cursor de cima do menu ou de um alvo"""
        return s._p({'do': 'scroll', 'point': {'x': ponto[0], 'y': ponto[1]}, 'by': 0, 'duration': 0.2, 'after': 0}, at,
                    label or 'cursor a um ponto neutro', {})

    def rolar(s, by, at=None, label=None, ponto=(760, 470), duration=0.5, after=100):
        return s._p({'do': 'scroll', 'point': {'x': ponto[0], 'y': ponto[1]}, 'by': by, 'duration': duration, 'after': after}, at, label, {})

    def confere(s, escopo, esperados, label, tentativas=22):
        """`eval` que LÊ a tela e compara com o que a fala diz: "OK: ..." ou "DIFERENTE: ..." (o resumo.py acusa)."""
        sel = {'dlg': '[role=dialog]', 'main': 'main', 'body': 'body'}.get(escopo, escopo)
        esp = [esperados] if isinstance(esperados, str) else list(esperados)
        js = ("(async()=>{const norm=t=>t.replace(/[\\s\\u00a0]+/g,' ').toLowerCase();const esp=%s;let out='';"
              "for(let i=0;i<%d;i++){const els=[...document.querySelectorAll(%s)];const el=els[els.length-1];"
              "if(!el){out='DIFERENTE: sem elemento';}else{const t=norm(el.innerText);const falta=esp.filter(e=>!t.includes(norm(e)));"
              "if(!falta.length)return 'OK: '+esp.join(' | ');out='DIFERENTE: faltou '+JSON.stringify(falta)+' em: '+t.slice(0,260);}"
              "await new Promise(r=>setTimeout(r,300));}return out})()") % (json.dumps(esp, ensure_ascii=False), tentativas, json.dumps(sel))
        return s.add({'do': 'eval', 'js': js, 'label': 'confere ' + label})

    def confere_campos(s, esperados, label, escopo='[role=dialog]'):
        """lê o VALOR dos campos (input/textarea) do escopo e compara com o que a fala diz"""
        esp = [esperados] if isinstance(esperados, str) else list(esperados)
        js = ("(async()=>{const esp=%s;let out='';for(let i=0;i<12;i++){const sc=[...document.querySelectorAll(%s)].pop();"
              "const v=sc?[...sc.querySelectorAll('input, textarea')].map(e=>e.value).join(' | '):'';"
              "const falta=esp.filter(e=>!v.includes(e));if(!falta.length)return 'OK: '+esp.join(' | ');out='DIFERENTE: faltou '+JSON.stringify(falta)+' em: '+v.slice(0,260);"
              "await new Promise(r=>setTimeout(r,300));}return out})()") % (json.dumps(esp, ensure_ascii=False), json.dumps(escopo))
        return s.add({'do': 'eval', 'js': js, 'label': 'confere ' + label})

    def fim(s):
        s.flush(1e9)
        s.steps.append({'do': 'eval', 'js': 'JSON.stringify(window.__avisos || "sem observador")', 'label': 'avisos de erro na tela'})
        s.steps.append({'do': 'mark', 'name': 'FIM', 'at': round(s.dur, 2)})

    def out(s):
        est = 'ESTIMADA' if s.estimada else 'da voz'
        resp = (' RESPIROS PENDENTES: ' + ', '.join(f'antes da L{li} +{d:.2f} s (fim da L{li - 1} em {t:.2f} s)' for li, t, d in s.respiros)) if s.respiros else ''
        return {
            'name': f't26-cap{s.n:02d}',
            'title': f'T26 · Cap. {s.n} · {NOMES[s.n]} (narração {str(round(s.dur, 1)).replace(".", ",")} s, {est}{resp}; '
                     f'marcas L1..L{len(s.linhas)} = início de cada linha do roteiro; FAKE_NOW {FAKE_NOW[s.n]})',
            'fakeNow': FAKE_NOW[s.n],
            'seed': f't26-cap{s.n:02d}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
            'start': {'x': s.start[0], 'y': s.start[1]},
            'anonymous': True,
            'storage': storage(s.n),
            'seedExtra': [f't26/{SEMENTE[s.n]}'],
            'prewarm': s.prewarm, 'setup': s.setup, 'steps': s.steps,
        }


def storage(n):
    """o que a primeira entrada do Rafael mostraria por cima da tela, já visto (o robô entra sem sessão: modo "anonymous")"""
    return {
        'app_version': VERSAO, 'notification_shown_version': VERSAO, 'pwa-install-dismissed': 'true', 'theme': 'light',
        f'daily-tasks-reminder-last-shown-{RAFAEL}': HOJE[n], 'initial-preferences-set': 'true',
        f'dominex:daily-tasks-shown:{RAFAEL}': HOJE[n],
    }


# ---------------------------------------------------------------- alvos
BTN = lambda n, **kw: {'role': 'button', 'name': n, 'exact': True, **kw}
BTNX = lambda n, **kw: {'role': 'button', 'name': n, **kw}
LINK = lambda n, **kw: {'role': 'link', 'name': n, 'exact': True, **kw}
TAB = lambda n, **kw: {'role': 'tab', 'name': n, **kw}
TXT = lambda t, **kw: {'text': t, 'exact': True, **kw}
TXTX = lambda t, **kw: {'text': t, **kw}
SEL = lambda s, **kw: {'selector': s, **kw}
OPT = lambda n, **kw: {'role': 'option', 'name': n, 'exact': True, **kw}
SW = lambda n, **kw: {'role': 'switch', 'name': n, 'exact': True, **kw}
# janelas (Radix: cada uma num portal; o `within` acha a janela pelo campo que só ela tem)
CFG = '[role=dialog]:has(#tab-btn-funis)'                  # Configurações do CRM/Kanban
ETAPA = '[role=dialog]:has(#crm-stage-name)'               # Novo estágio / Configurar <etapa>
FUNIL = '[role=dialog]:has(#crm-pipeline-name)'            # Novo funil
CHK = '[role=dialog]:has(#crm-checklist-name)'             # Nova checklist
ETQ = '[role=dialog]:has(#crm-label-name)'                 # Nova etiqueta
OPP = '[role=dialog]:has(#crm-title)'                      # Nova oportunidade / Editar oportunidade
FICHA = '[role=dialog]:has(textarea[placeholder^="Escreva um coment"])'   # ficha da oportunidade
TAREFA = '[role=dialog]:has(#crm-task-form-dialog)'        # Nova tarefa
FILTROS = '[role=dialog]:has(#crm-min-value)'              # Filtrar oportunidades
POP = '[data-radix-popper-content-wrapper]'
COMBO = lambda txt, esc='[role=dialog]': {'selector': f'{esc} button[role=combobox]', 'hasText': txt}
COLUNA = lambda nome: SEL(f"main section:has(> header h2:text-is('{nome}'))")
CAB = lambda nome: SEL(f"main section > header:has(h2:text-is('{nome}'))")
CARTAO = lambda titulo: SEL(f"main section div.rounded-lg:has(> div p:text-is('{titulo}'))")
ALCA = lambda titulo: SEL(f"main section div.rounded-lg:has(> div p:text-is('{titulo}')) button[aria-label='Mover oportunidade']")
TITULO_CARTAO = lambda titulo: SEL(f"main section button:has(> p:text-is('{titulo}'))")
SELO_TAREFAS = lambda titulo: SEL(f"main section div.rounded-lg:has(> div p:text-is('{titulo}')) span[title$='tarefa(s) aberta(s)']")
METRICA = lambda rotulo: SEL(f"main div.rounded-lg:has(> div > p:text-is('{rotulo}'))")
METRICA_X = lambda rotulo: SEL(f"main div.rounded-lg:has(> div > p:has-text('{rotulo}'))")
LINHA_FUNIL = lambda nome: SEL(f"{CFG} div[draggable=true]:has(span.truncate:text-is('{nome}'))")
LINHA_ETAPA = lambda nome: SEL(f"{CFG} div[draggable=true]:has(> span.flex-1:text-is('{nome}'))")
EDITAR_ETAPA = lambda nome: {'role': 'button', 'name': f'Editar estágio {nome}', 'exact': True}
JEQ = 'Retalho de chapa da Metalúrgica Jequitibá'

# ---------------------------------------------------------------- trechos comuns (não filmados, no `setup`)
LOGIN = [
    {'do': 'goto', 'url': '/login'},
    {'do': 'waitFor', 'target': {'placeholder': 'seu@email.com'}, 'timeout': 40},
    {'do': 'type', 'target': {'placeholder': 'seu@email.com'}, 'text': '$TUT_USER', 'cps': 40},
    {'do': 'type', 'target': {'placeholder': '••••••••'}, 'text': '$TUT_SENHA', 'cps': 40},
    {'do': 'click', 'target': {'role': 'button', 'name': 'Entrar', 'exact': True}},
    {'do': 'waitFor', 'text': 'Olá, Rafael', 'timeout': 45},
    {'do': 'waitFor', 'idle': True, 'timeout': 20},
]
RECOLHE = {'do': 'eval', 'js': ("(()=>{const sb=document.querySelector('[data-state][data-collapsible]');if(sb&&sb.getAttribute('data-state')==='collapsed')"
                                "return 'ja recolhido';const b=document.querySelector('header button.h-8.w-8');if(!b)return 'SEM ALVO';b.click();return 'recolhido'})()")}
AGUARDA = {'do': 'waitFor', 'idle': True, 'timeout': 15}


def vai(url, espera):
    return [{'do': 'goto', 'url': url}, {'do': 'waitFor', 'text': espera, 'timeout': 30}, AGUARDA]


CRM = vai('/crm', 'Gerencie oportunidades e acompanhe seu processo comercial.')
ABRE_CFG = [{'do': 'click', 'target': BTN('Configurações do CRM/Kanban')}, {'do': 'waitFor', 'text': 'Organize os funis comerciais e as etapas de cada Kanban.', 'timeout': 15}]
ABRE_SUCATA = [{'do': 'click', 'target': {'role': 'button', 'name': 'Expandir Sucata industrial', 'exact': True}},
               {'do': 'waitFor', 'text': 'Estágios deste funil', 'timeout': 10}, {'do': 'wait', 'seconds': 0.4}]
FECHAR_EVAL = (r"""(() => { const ds = [...document.querySelectorAll('[role=dialog]')]; const d = ds[ds.length - 1]; if (!d) return 'ja fechada'; """
               r"""const b = [...d.querySelectorAll('button')].find((x) => [x.textContent, x.getAttribute('aria-label')].some((v) => /^\s*fechar\s*$/i.test(v || ''))); """
               r"""if (!b) return 'sem botao Fechar'; b.click(); return 'fechada pelo botao'; })()""")


def js_cor(sel, cor):
    """<input type=color>: o valor entra pelo setter nativo + evento input (o onChange do React), como se escolhido no seletor"""
    return ("(()=>{const i=document.querySelector(%s);if(!i)return 'SEM ALVO';const set=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set;"
            "set.call(i,%s);i.dispatchEvent(new Event('input',{bubbles:true}));i.dispatchEvent(new Event('change',{bubbles:true}));return i.value})()") % (
        json.dumps(sel), json.dumps(cor))


def js_rola_quadro(x, dur_ms=700):
    """rolagem horizontal suave do quadro (a grade de colunas, overflow-x) até scrollLeft = x; devolve o scrollLeft final"""
    return ("(async()=>{const c=[...document.querySelectorAll('main div.overflow-x-auto')].find(e=>e.querySelector('section header h2'));if(!c)return 'SEM ALVO';"
            "const x0=c.scrollLeft,dx=%d-x0,t0=performance.now();if(Math.abs(dx)<3)return 'ok';await new Promise(res=>{const f=t=>{const p=Math.min(1,(t-t0)/%d),"
            "e=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;c.scrollLeft=x0+dx*e;p<1?requestAnimationFrame(f):res()};requestAnimationFrame(f)});return Math.round(c.scrollLeft)})()") % (
        int(x), int(dur_ms))


def js_dlg_ate(esc, texto, y=200, dur_ms=600):
    """rolagem suave da janela (o contêiner que rola dentro dela) até o rótulo `texto` ficar em y px CSS; devolve o topo final"""
    return ("(async()=>{const d=[...document.querySelectorAll(%s)].pop();if(!d)return 'SEM JANELA';const el=[...d.querySelectorAll('label, p, h3, span, button')]"
            ".filter(e=>e.textContent.trim().startsWith(%s)).sort((a,b)=>a.textContent.length-b.textContent.length)[0];if(!el)return 'SEM ALVO';"
            "let c=el.parentElement;while(c&&c!==d.parentElement){const s=getComputedStyle(c);if(/(auto|scroll)/.test(s.overflowY)&&c.scrollHeight>c.clientHeight+4)break;c=c.parentElement;}"
            "if(!c||c===d.parentElement)return 'SEM ROLAGEM';const dy=Math.round(el.getBoundingClientRect().top-%d);if(Math.abs(dy)<3)return 'ok';const y0=c.scrollTop,t0=performance.now();"
            "await new Promise(res=>{const f=t=>{const p=Math.min(1,(t-t0)/%d),e=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;c.scrollTop=y0+dy*e;p<1?requestAnimationFrame(f):res()};requestAnimationFrame(f)});"
            "return Math.round(el.getBoundingClientRect().top)})()") % (json.dumps(esc), json.dumps(texto), int(y), int(dur_ms))


def js_foco(sel):
    return "(()=>{const e=document.querySelector(%s);if(!e)return 'SEM ALVO';e.focus();return 'foco ok'})()" % json.dumps(sel)


def js_ultimo_item_foco():
    """foca o último campo "Texto do item N" da Nova checklist (o "Adicionar item" não foca a linha nova)"""
    return ("(()=>{const l=[...document.querySelectorAll(%s)];const e=l[l.length-1];if(!e)return 'SEM ALVO';e.focus();return e.getAttribute('aria-label')})()"
            % json.dumps(f"{CHK} input[aria-label^='Texto do item']"))


# saída e volta ao CRM por navegação interna (o "corte" do cap09): o quadro remonta na verdade do banco
JS_REMONTA = ("(async()=>{const t0=performance.now();history.pushState(null,'','/dashboard');dispatchEvent(new PopStateEvent('popstate'));"
              "await new Promise(r=>setTimeout(r,350));history.pushState(null,'','/crm');dispatchEvent(new PopStateEvent('popstate'));"
              "for(let i=0;i<80;i++){await new Promise(r=>setTimeout(r,100));if(document.querySelector('main section header h2'))break;}"
              "return Math.round(performance.now()-t0)})()")


def cap_novo(n, **kw):
    return Cap(n, **kw)
