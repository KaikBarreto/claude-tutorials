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
   com a consulta vencida (30 s), por isso o setup do cap09 espera 31 s antes de gravar (vale também no ensaio rápido).
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
FAKE_NOW[12] = FAKE_NOW[13] = '2026-11-10T17:30:00-03:00'   # o fim do dia (cap12) e o passeio do resumo no mesmo estado
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
    pend = []   # (linha, fim da linha anterior NO TAKE ORIGINAL (o T do pausas.py), segundos que faltam)
    for li, need in sorted(RESPIROS.get(n, {}).items()):
        i = li - 1
        if i <= 0 or i >= len(linhas):
            continue
        gap = linhas[i]['s'] - linhas[i - 1]['e']
        if gap + 0.02 >= need:
            continue
        d = round(need - gap, 2)
        pend.append((li, round(real['linhas'][i - 1]['e'], 2), d))
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
        s.ambiguas = []
        s.pending = []

    # ---- tempo
    def L(s, i):
        return round(s.linhas[i - 1]['s'], 2)

    def Lfim(s, i):
        return round(s.linhas[i - 1]['e'], 2)

    def W(s, i, palavra, nth=0):
        q = norm(palavra)
        hits = [w for w in s.words if w['linha'] == i - 1 and norm(w['w']).startswith(q)]
        if len(hits) > 1:
            s.ambiguas.append((i, palavra, nth, len(hits)))
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
        if t <= 0 or i == 1:   # a L1 entra no começo (a voz começa em ~0,4 s; um passo em 0 não pode vir antes da marca)
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
        s.apara_hovers()
        s.steps.append({'do': 'eval', 'js': 'JSON.stringify(window.__avisos || "sem observador")', 'label': 'avisos de erro na tela'})
        s.steps.append({'do': 'mark', 'name': 'FIM', 'at': round(s.dur, 2)})

    def apara_hovers(s, chegada=0.95):
        """um hover com `at` termina antes do próximo passo com `at` (marca ou gesto): o tempo parado não pode empurrar a marca seguinte
        (cap00, 10/11: L5 e L6 saíram 0,3 e 0,9 s atrasadas). `chegada` = o tempo médio até o cursor chegar ao alvo."""
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
ETAPA = "[role=dialog]:has([role=tab][id$='-trigger-rules'])"   # Novo estágio / Configurar <etapa> (as abas Regras/Automações desmontam o #crm-stage-name)
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


JS_COLAR = ("(()=>{const e=document.activeElement;if(!e||!/^(INPUT|TEXTAREA)$/.test(e.tagName))return 'SEM FOCO';"
            "document.execCommand('insertText',false,%s);return e.value})()")


def colar(texto):
    """texto longo e sem graça visual (ex.: o e-mail): entra de uma vez no campo focado (insertText, o React ouve o input)"""
    return JS_COLAR % json.dumps(texto)


JS_FECHA_TOAST = ("(()=>{const b=[...document.querySelectorAll('[data-sonner-toast] button[aria-label]')].filter(x=>/close/i.test(x.getAttribute('aria-label')));"
                  "b.forEach(x=>x.click());return b.length})()")


def fecha_janela(c, esc, at=None, label='fecha a janela (Esc)'):
    """Esc na janela de cima e, se ela ainda estiver aberta, o botão Fechar DELA (nunca o da janela de baixo)"""
    c.press('Escape', at=at, label=label)
    c.wait(0.4)
    js = ("(()=>{const d=[...document.querySelectorAll(%s)].pop();if(!d)return 'ja fechada';const b=[...d.querySelectorAll('button')].find(x=>"
          "[x.textContent,x.getAttribute('aria-label')].some(v=>/^\\s*fechar\\s*$/i.test(v||'')));if(!b)return 'sem botao Fechar';b.click();return 'fechada pelo botao'})()") % json.dumps(esc)
    c.ev(js, label=label + ' (plano B)')
    c.waitfor(gone={'selector': esc}, timeout=8)


# ================================================================ capítulos
def cap00():
    """Abertura: Dashboard (menu aberto); ilustração nas linhas 1 a 3; o item CRM/Kanban do menu lateral, sem clicar."""
    c = cap_novo(0, recolhe=False, start=(760, 150))
    c.mark(1)
    c.mark(2)
    c.mark(3)
    c.confere('main', ['Olá, Rafael', 'Total Compras', 'Total Vendas'], 'Dashboard da Recicla Vale Metais')
    c.mark(4)
    c.hover(LINK('CRM/Kanban'), 2.4, at=c.A(4, 'menu', 0.6), label='item CRM/Kanban do menu lateral (zoom, sem clicar)')
    c.mark(5)
    c.hover(LINK('CRM/Kanban'), 2.6, at=c.A(5, 'depende', 0.6), label='CRM/Kanban (módulo do plano)')
    c.mark(6)
    c.cursor((760, 150), at=c.A(6, 'Se', 0.2), label='cursor sai do menu (cartão Antes)')
    c.fim()
    return c


def cap01():
    """O funil de vendas: primeira abertura (o banco cria o Funil de vendas), as cinco colunas, ilustração, Nova oportunidade tracejado."""
    # aquece a rota do CRM fora do vídeo (sem isso, o clique no menu mostrou a tela branca "Carregando..." por ~1,3 s com a máquina cheia);
    # o banco já cria o Funil de vendas aqui, no preparo: na tela é igual
    c = cap_novo(1, recolhe=False, start=(760, 150), setup=CRM + vai('/dashboard', 'Olá, Rafael') + [{'do': 'wait', 'seconds': 1.5}])
    c.mark(1)
    c.click(LINK('CRM/Kanban'), at=c.A(1, 'abre', 1.0), label='CRM/Kanban (menu lateral)')
    c.waitfor(target=CAB('Perdido'), timeout=25)
    c.confere('main', ['CRM/Kanban', 'Gerencie oportunidades e acompanhe seu processo comercial.', 'Funil de vendas', 'Novo', 'Em contato',
                       'Proposta', 'Ganho', 'Perdido'], 'o Funil de vendas com as cinco colunas')
    c.hover(SEL("main button:has-text('Funil de vendas')"), 1.0, at=c.A(1, 'Funil', 0.6, nth=1), label='Funil de vendas (barra dos funis)')
    c.mark(2)
    c.hover(CAB('Novo'), 0.1, at=c.A(2, 'Novo,', 0.75), label='coluna Novo')
    c.hover(CAB('Em contato'), 0.1, at=c.A(2, 'Em', 0.75), label='coluna Em contato')
    c.hover(CAB('Proposta'), 0.1, at=c.A(2, 'Proposta,', 0.8), label='coluna Proposta')
    c.ev(js_rola_quadro(2000, 600), at=c.A(2, 'Ganho', 0.95), label='o quadro rola para a direita (Ganho e Perdido)')
    c.hover(CAB('Perdido'), 0.9, at=c.A(2, 'Perdido.', 0.75), label='coluna Perdido')
    c.mark(3)
    c.ev(js_rola_quadro(0, 600), at=c.A(3, 'entram', 0.0), label='o quadro volta ao começo (sob a ilustração)')
    c.cursor((760, 180), label='cursor descansa (ilustração)')
    c.mark(4)
    c.mark(5)
    c.hover(SEL("main section:has(> header h2:text-is('Novo')) button.border-dashed"), 2.0, at=c.A(5, 'aqui,', 0.6),
            label='botão tracejado Nova oportunidade da coluna Novo (zoom)')
    c.fim()
    return c


def cap02():
    """Funil, Tarefas e os cartões: as abas, os quatro cartões zerados (ilustração), busca, filtros, Nova oportunidade e a barra dos funis."""
    c = cap_novo(2, setup=CRM)
    c.mark(1)
    c.hover(BTN('Funil'), 1.0, at=c.A(1, 'Funil,', 0.6), label='aba Funil (zoom nas abas)')
    c.hover(BTN('Tarefas'), 1.6, at=c.A(1, 'Tarefas,', 0.6), label='aba Tarefas')
    c.mark(2)
    c.marcar(SEL("main div.grid:has(> div > div > p:text-is('Total de oportunidades'))"), at=c.A(2, 'quatro', 0.3), label='os quatro cartões (zoom)')
    c.hover(METRICA('Total de oportunidades'), 0.6, at=c.A(2, 'Total', 0.6), label='Total de oportunidades 0')
    c.hover(METRICA('Valor total'), 0.3, at=c.A(2, 'Valor', 0.6), label='Valor total R$ 0,00')
    c.hover(METRICA('Ganhos'), 0.05, at=c.A(2, 'Ganhos', 0.6), label='Ganhos R$ 0,00')
    c.hover(METRICA('Em negociação'), 1.6, at=c.A(2, 'Em', 0.5), label='Em negociação R$ 0,00')
    c.confere('main', ['Total de oportunidades', 'Valor total', 'R$ 0,00', 'Ganhos', 'Em negociação'], 'os quatro cartões zerados')
    c.mark(3)
    c.cursor((660, 650), at=c.A(3, 'Total', 0.3), label='cursor descansa (ilustração)')
    c.mark(4)
    c.hover(SEL("main input[placeholder^='Buscar por título']"), 0.3, at=c.A(4, 'busca,', 0.6), label='busca')
    c.hover(BTNX('Filtros'), 0.2, at=c.A(4, 'filtros', 0.6), label='Filtros')
    c.hover(BTN('Nova oportunidade', nth=0), 0.6, at=c.A(4, 'Nova', 0.6), label='Nova oportunidade')
    c.hover(SEL("main button:has-text('Funil de vendas')"), 0.4, at=c.A(4, 'barra,', 0.6), label='barra dos funis: Funil de vendas')
    c.hover(BTN('Configurar estágios'), 0.2, at=c.A(4, 'funis', 0.6), label='engrenagem Configurar estágios')
    c.hover(BTN('Criar funil'), 0.4, at=c.A(4, 'empresa.', 0.6), label='+ Criar funil')
    c.mark(5)
    c.cursor((660, 600), at=c.A(5, 'Uma', 0.3), label='cursor sai (plano geral)')
    c.fim()
    return c


LINHA_FUNIL_S = lambda nome: f"{CFG} div[draggable=true]:has(span.truncate:text-is('{nome}'))"


def cap03():
    """Funis e estágios: Configurações, Novo funil Sucata industrial (azul), Tornar padrão, arrastar a linha; Novo estágio Visita técnica e arrastar."""
    c = cap_novo(3, setup=CRM)
    c.mark(1)
    c.click(BTN('Configurações do CRM/Kanban'), at=c.A(1, 'Configurações', 1.0, nth=1), label='Configurações do CRM/Kanban')
    c.waitfor(text='Organize os funis comerciais e as etapas de cada Kanban.', timeout=12)
    c.hover(SEL('#tab-btn-funis'), 0.4, at=c.A(1, 'Funis,', 0.6), label='menu Funis')
    c.hover(LINHA_FUNIL('Funil de vendas'), 0.4, at=c.A(1, 'Funil', 0.6), label='linha Funil de vendas')
    c.hover(TXT('Padrão', within=LINHA_FUNIL_S('Funil de vendas')), 0.9, at=c.A(1, 'Padrão.', 0.6), label='selo Padrão')
    c.mark(2)
    c.click(BTN('Novo funil'), at=c.A(2, 'Novo', 0.9), label='Novo funil')
    c.waitfor(selector='#crm-pipeline-name', timeout=8)
    c.type(SEL('#crm-pipeline-name'), 'Sucata industrial', at=c.A(2, 'Sucata', 0.6, nth=1), noClick=True, cps=30, label='Nome: Sucata industrial')
    c.hover(SEL('#crm-pipeline-color'), 0.05, at=c.A(2, 'cor.', 0.9), label='Cor (o seletor de cor)')
    c.ev(js_cor('#crm-pipeline-color', '#0ea5e9'), label='Cor: azul #0ea5e9')
    c.click(BTN('Salvar', within=FUNIL), at=c.A(2, 'Salvar.', 0.9), label='Salvar (Novo funil)')
    c.waitfor(text='Funil criado', timeout=10)
    c.mark(3)
    c.hover(SEL(f"{LINHA_FUNIL_S('Sucata industrial')} span.block"), 0.6, at=c.A(3, 'cinco', 0.6), label='Sucata industrial: 5 etapas')
    c.click(BTN('Tornar "Sucata industrial" o funil padrão'), at=c.A(3, 'Tornar', 0.8), label='Tornar padrão')
    c.waitfor(text='Funil padrão atualizado', timeout=10)
    c.hover(TXT('Padrão', within=LINHA_FUNIL_S('Sucata industrial')), 0.8, at=c.A(3, 'primeiro', 0.6), label='selo Padrão no Sucata industrial')
    c.mark(4)
    c.drag(LINHA_FUNIL('Sucata industrial'), LINHA_FUNIL('Funil de vendas'), at=c.A(4, 'Arrastando', 0.3), hold=0.45,
           label='arrasta a linha Sucata industrial para cima do Funil de vendas')
    c.waitfor(target=SEL(f"{CFG} div[draggable=true]:first-of-type:has(span.truncate:text-is('Sucata industrial'))"), timeout=8)
    c.hover(LINHA_FUNIL('Sucata industrial'), 1.2, at=c.A(4, 'Sucata', 0.6), label='Sucata industrial vai pra frente')
    c.mark(5)
    c.click(SEL(f"{LINHA_FUNIL_S('Sucata industrial')} button:has(span.truncate)"), at=c.A(5, 'Abrindo', 0.8), label='abre o funil Sucata industrial')
    c.waitfor(text='Estágios deste funil', timeout=8)
    c.hover(TXTX('Estágios deste funil', within=CFG), 0.5, at=c.A(5, 'estágios.', 0.6), label='Estágios deste funil')
    c.hover(LINHA_ETAPA('Em contato'), 0.2, at=c.A(5, 'contato', 0.6), label='estágio Em contato')
    c.hover(LINHA_ETAPA('Proposta'), 0.5, at=c.A(5, 'proposta,', 0.6), label='estágio Proposta')
    c.click(BTN('Novo estágio'), at=c.A(5, 'Novo', 1.1), label='Novo estágio')
    c.waitfor(selector='#crm-stage-name', timeout=8)
    c.ev(js_foco('#crm-stage-name'), label='foco no Nome (a janela abre com o foco nas abas)')
    c.type(SEL('#crm-stage-name'), 'Visita técnica', at=c.A(5, 'Visita', 0.6, nth=1), noClick=True, cps=30, label='Nome: Visita técnica')
    c.click(BTN('Salvar etapa'), at=c.A(5, 'Salvar', 0.9), label='Salvar etapa (Novo estágio)')
    c.waitfor(text='Estágio criado.', timeout=10)
    c.mark(6)
    c.hover(LINHA_ETAPA('Visita técnica'), 0.5, at=c.A(6, 'fim.', 0.6), label='Visita técnica entra no fim da lista')
    c.drag(LINHA_ETAPA('Visita técnica'), LINHA_ETAPA('Proposta'), at=c.A(6, 'arrasto', 0.4), hold=0.45,
           label='arrasta Visita técnica para depois de Em contato')
    c.confere(CFG, ['Novo\nEm contato\nVisita técnica\nProposta'], 'ordem Novo, Em contato, Visita técnica, Proposta')
    c.mark(7)
    c.hover(TXT('Ganho', within=LINHA_ETAPA('Ganho')['selector']), 0.5, at=c.A(7, 'Ganho', 0.6), label='selo Ganho')
    c.hover(TXT('Perdido', within=LINHA_ETAPA('Perdido')['selector']), 0.8, at=c.A(7, 'Perdido', 0.6), label='selo Perdido')
    c.fim()
    return c


SW_CARD = lambda nome: SEL(f"{ETAPA} div.rounded-xl:has(> div > label:text-is('{nome}'))")


def cap04():
    """Nome, cor e orientação: lápis da Visita técnica, abas, cor verde-azulada, Orientação para o time, Salvar etapa; a lixeira (sem clicar)."""
    c = cap_novo(4, setup=CRM + ABRE_CFG + ABRE_SUCATA)
    c.mark(1)
    c.click(EDITAR_ETAPA('Visita técnica'), at=c.A(1, 'lápis.', 0.8), label='lápis Editar estágio Visita técnica')
    c.waitfor(text='Configurar Visita técnica', timeout=8)
    c.hover(TAB('Coluna'), 0.2, at=c.A(1, 'Coluna,', 0.6), label='aba Coluna')
    c.hover(TAB('Regras'), 0.2, at=c.A(1, 'Regras', 0.6), label='aba Regras')
    c.hover(TAB('Automações'), 0.6, at=c.A(1, 'Automações.', 0.6), label='aba Automações')
    c.mark(2)
    c.hover(SEL('#crm-stage-name'), 0.3, at=c.A(2, 'nome', 0.6), label='Nome * Visita técnica')
    c.hover(SEL('#crm-stage-color'), 0.9, at=c.A(2, 'cor', 0.6, nth=1), label='Cor * (veio cinza)')
    c.ev(js_cor('#crm-stage-color', '#0d9488'), at=c.A(2, 'escolho', 0.0), label='Cor: verde-azulado #0d9488')
    c.mark(3)
    c.click(SEL('#crm-stage-description'), at=c.A(3, 'Orientação', 0.8), label='Orientação para o time')
    c.type(SEL('#crm-stage-description'), 'Visitar a indústria, ver o volume e o tipo de sucata e combinar a retirada.', at=c.A(3, 'combinado', 0.3),
           noClick=True, cps=40, label='Orientação: Visitar a indústria, ver o volume e o tipo de sucata e combinar a retirada.')
    c.confere_campos(['#0d9488', 'Visitar a indústria, ver o volume e o tipo de sucata e combinar a retirada.'], 'cor e orientação no formulário', escopo=ETAPA)
    c.mark(4)
    c.click(BTN('Salvar etapa'), at=c.A(4, 'Salvar', 0.8), label='Salvar etapa')
    c.waitfor(text='Configuração da etapa salva', timeout=10)
    c.waitfor(gone={'selector': ETAPA}, timeout=8)
    c.click(EDITAR_ETAPA('Visita técnica'), at=c.A(4, 'aqui,', 0.8), label='lápis de novo: o texto fica na configuração da etapa')
    c.waitfor(text='Configurar Visita técnica', timeout=8)
    c.hover(SEL('#crm-stage-description'), 1.4, at=c.A(4, 'referência', 0.6), label='Orientação para o time salva (zoom)')
    c.mark(5)
    fecha_janela(c, ETAPA, at=c.A(5, 'Uma', 0.3), label='fecha a configuração (Esc)')
    c.hover({'role': 'button', 'name': 'Excluir estágio Visita técnica', 'exact': True}, 2.4, at=c.A(5, 'excluir', 0.6),
            label='lixeira Excluir estágio Visita técnica (zoom, sem clicar)')
    c.cursor((780, 600), at=c.A(5, 'move', 0.2), label='cursor sai da lixeira')
    c.fim()
    return c


def cap05():
    """Regras do estágio: lápis do Em contato > Regras (ilustração), as seis chaves, liga Tarefas e Responsável, os campos por nome, Salvar etapa."""
    c = cap_novo(5, setup=CRM + ABRE_CFG + ABRE_SUCATA)
    c.mark(1)
    c.click(EDITAR_ETAPA('Em contato'), at=c.A(1, 'abrir', 0.8), label='lápis Editar estágio Em contato')
    c.waitfor(text='Configurar Em contato', timeout=8)
    c.click(TAB('Regras'), at=c.A(1, 'Regras.', 0.8, nth=1), label='aba Regras')
    c.waitfor(text='Antes de sair desta etapa', timeout=8)
    c.mark(2)
    c.cursor((640, 300), at=c.A(2, 'Pensa', 0.2), label='cursor descansa (ilustração)')
    c.mark(3)
    c.hover(SW_CARD('Tarefas'), 0.4, at=c.A(3, 'tarefas', 0.6), label='chave Tarefas')
    c.hover(SW_CARD('Checklists'), 0.4, at=c.A(3, 'checklists', 0.6), label='chave Checklists')
    c.hover(SW_CARD('Responsável'), 0.4, at=c.A(3, 'responsável,', 0.6), label='chave Responsável')
    c.hover(SW_CARD('Prazo'), 0.4, at=c.A(3, 'previsão', 0.6), label='chave Prazo')
    c.hover(SW_CARD('Empresa'), 0.3, at=c.A(3, 'empresa', 0.6), label='chave Empresa')
    c.hover(SW_CARD('Observações'), 0.6, at=c.A(3, 'observações', 0.6), label='chave Observações')
    c.mark(4)
    c.click(SW('Tarefas'), at=c.A(4, 'Tarefas', 0.8), label='liga Tarefas')
    c.click(SW('Responsável'), at=c.A(4, 'Responsável.', 0.8), label='liga Responsável')
    c.ev("(()=>[...document.querySelectorAll('%s button[role=switch]')].map(s=>s.id+'='+s.getAttribute('aria-checked')).join(' '))()" % ETAPA.replace("'", "\\'"),
         label='confere chaves: Tarefas e Responsável ligadas')
    c.mark(5)
    c.hover(SEL('#required-task-names'), 0.6, at=c.A(5, 'tarefa', 0.6), label='Tarefas obrigatórias por nome (zoom)')
    c.hover(SEL('#required-checklist-names'), 2.0, at=c.A(5, 'checklist', 0.6), label='Checklists obrigatórios por nome (zoom)')
    c.mark(6)
    c.click(BTN('Salvar etapa'), at=c.A(6, 'Salvar', 0.8), label='Salvar etapa')
    c.waitfor(text='Configuração da etapa salva', timeout=10)
    c.fim()
    return c


OPC = lambda nome: SEL(f"[role=option]:has-text('{nome}')")


def cap06():
    """Automações: aba Automações (ilustração), Nova automação Agendar a visita, gatilho, as sete ações, Criar tarefa, título com {CLIENTE},
    1 dia útil, Pausada > Ativa, Salvar automação (ilustração no fim)."""
    abre = [{'do': 'click', 'target': EDITAR_ETAPA('Em contato')}, {'do': 'waitFor', 'text': 'Configurar Em contato', 'timeout': 10}, {'do': 'wait', 'seconds': 0.5}]
    c = cap_novo(6, setup=CRM + ABRE_CFG + ABRE_SUCATA + abre)
    c.mark(1)
    c.click(TAB('Automações'), at=c.A(1, 'automações.', 0.8), label='aba Automações')
    c.waitfor(text='Fluxos desta etapa', timeout=8)
    c.hover(TXT('Novas automações nascem pausadas para revisão.'), 0.6, at=c.A(1, 'fazem', 0.6), label='Novas automações nascem pausadas para revisão.')
    c.hover(TXT('Nenhuma automação nesta etapa'), 1.0, at=c.A(1, 'quando', 0.6), label='Nenhuma automação nesta etapa')
    c.mark(2)
    c.cursor((640, 300), at=c.A(2, 'sempre', 0.2), label='cursor descansa (ilustração)')
    c.mark(3)
    c.click(BTN('Nova automação'), at=c.A(3, 'Nova', 0.9), label='Nova automação')
    c.waitfor(text='Use {NOME} e {CLIENTE} nos textos dinâmicos.', timeout=8)
    c.type(SEL(f"{ETAPA} input[placeholder='Ex.: Preparar contato comercial']"), 'Agendar a visita', at=c.A(3, 'Agendar', 0.9), cps=30,
           label='Nome: Agendar a visita')
    c.click(COMBO('Ao entrar nesta etapa', ETAPA), at=c.A(3, 'gatilho,', 0.5), label='Gatilho (abre a lista)')
    c.hover(OPC('Ao entrar nesta etapa'), 0.3, at=c.A(3, 'entra', 0.6), label='Ao entrar nesta etapa', noScroll=True)
    c.hover(OPC('Ao concluir uma tarefa'), 0.2, at=c.A(3, 'tarefa', 0.6), label='Ao concluir uma tarefa', noScroll=True)
    c.hover(OPC('Ao concluir um checklist'), 0.3, at=c.A(3, 'checklist', 0.6), label='Ao concluir um checklist', noScroll=True)
    c.hover(OPC('Quando tudo estiver concluído'), 0.6, at=c.A(3, 'tudo', 0.6), label='Quando tudo estiver concluído', noScroll=True)
    c.click(OPC('Ao entrar nesta etapa'), at=c.A(3, 'Fico', 0.6), label='fica em Ao entrar nesta etapa', noScroll=True)
    c.mark(4)
    c.click(COMBO('Criar tarefa', ETAPA), at=c.A(4, 'ações', 0.8), label='ação 1 (abre a lista das ações)')
    c.hover(OPC('Criar tarefa'), 0.1, at=c.A(4, 'Criar', 0.6), label='Criar tarefa', noScroll=True)
    c.hover(OPC('Aplicar checklist'), 0.3, at=c.A(4, 'Aplicar', 0.6), label='Aplicar checklist', noScroll=True)
    c.hover(OPC('Definir prazo do cartão'), 0.5, at=c.A(4, 'Definir', 0.6), label='Definir prazo do cartão', noScroll=True)
    c.hover(OPC('Atribuir responsável'), 0.5, at=c.A(4, 'Atribuir', 0.6), label='Atribuir responsável', noScroll=True)
    c.hover(OPC('Adicionar etiqueta'), 0.4, at=c.A(4, 'Adicionar', 0.6), label='Adicionar etiqueta', noScroll=True)
    c.hover(OPC('Mover cartão'), 0.2, at=c.A(4, 'Mover', 0.6), label='Mover cartão', noScroll=True)
    c.hover(OPC('Copiar cartão'), 0.4, at=c.A(4, 'Copiar', 0.6), label='Copiar cartão', noScroll=True)
    c.click(OPC('Criar tarefa'), at=c.A(4, 'Criar', 0.6, nth=1), label='fica em Criar tarefa', noScroll=True)
    c.mark(5)
    titulo = SEL(f"{ETAPA} input[placeholder='Ex.: Ligar para {{NOME}}']")
    c.click(titulo, at=c.A(5, 'título', 0.8), label='Título da tarefa *')
    c.type(titulo, 'Agendar visita na ', at=c.A(5, 'Agendar', 0.3), noClick=True, clear=True, cps=30, label='título: Agendar visita na')
    c.type(titulo, '{CLIENTE}', at=c.A(5, 'marcador', 0.1), noClick=True, cps=22, label='título: {CLIENTE}')
    c.confere_campos(['Agendar visita na {CLIENTE}'], 'título da tarefa', escopo=ETAPA)
    c.hover(TXT('Use {NOME} e {CLIENTE} nos textos dinâmicos.'), 1.6, at=c.A(5, 'vira', 0.6), label='Use {NOME} e {CLIENTE} nos textos dinâmicos. (zoom)')
    c.mark(6)
    c.hover(SEL(f"{ETAPA} input[type=number]"), 0.1, at=c.A(6, 'prazo', 1.0), label='Prazo em dias: 1')
    c.select(COMBO('Dias corridos', ETAPA), 'Dias úteis', at=c.A(6, 'prazo', 0.2), label='Contagem: Dias úteis')
    c.mark(7)
    c.hover(SEL(f"{ETAPA} div.rounded-xl.shadow-sm:has(input[type=number])"), 3.0, at=c.A(7, 'tarefa', 0.6), label='a ação inteira (título, prazo e contagem)')
    c.mark(8)
    c.hover(SEL(f"{ETAPA} label[for=automation-enabled]"), 1.6, at=c.A(8, 'pausada.', 0.6), label='chave em Pausada (zoom)')
    c.click(SEL('#automation-enabled'), at=c.A(8, 'ligo', 0.8), label='liga a chave (Ativa)')
    c.waitfor(target=TXT('Ativa', within=ETAPA), timeout=6)
    c.mark(9)
    c.click(BTN('Salvar automação'), at=c.A(9, 'Salvar', 0.8), label='Salvar automação')
    c.waitfor(text='Automação salva e ativa', timeout=10)
    c.confere(ETAPA, ['Agendar a visita', 'Ativa', 'Ao entrar nesta etapa · 1 ação'], 'a automação ativa na lista')
    c.hover(SEL(f"{ETAPA} div.rounded-xl:has(p:text-is('Agendar a visita'))"), 1.2, at=c.A(9, 'ativa', 0.6), label='Agendar a visita, Ativa (zoom)')
    c.mark(10)
    c.cursor((640, 300), at=c.A(10, 'Uma', 0.2), label='cursor descansa (ilustração)')
    c.fim()
    return c


def cap07():
    """Checklists e etiquetas: Checklists, Nova checklist com três itens, ilustração, Etiquetas, Nova etiqueta Indústria (#6366f1)."""
    c = cap_novo(7, setup=CRM + ABRE_CFG)
    c.mark(1)
    c.click(SEL('#tab-btn-checklists'), at=c.A(1, 'Checklists', 0.8), label='menu Checklists')
    c.waitfor(text='Modelos reutilizáveis de checklist pra aplicar em oportunidades.', timeout=8)
    c.hover(TXTX('O modelo é só o ponto de partida', within=CFG), 1.2, at=c.A(1, 'prontas', 0.6), label='aviso: o modelo é só o ponto de partida')
    c.mark(2)
    c.click(BTN('Nova checklist'), at=c.A(2, 'Nova', 0.9), label='Nova checklist')
    c.waitfor(selector='#crm-checklist-name', timeout=8)
    c.type(SEL('#crm-checklist-name'), 'Documentos do fornecedor', at=c.A(2, 'Documentos', 0.9), cps=30, label='Nome: Documentos do fornecedor')
    c.click(BTN('Adicionar item'), at=c.A(2, 'três', 0.8), label='Adicionar item (1)')
    c.click(BTN('Adicionar item'), label='Adicionar item (2)')
    c.click(BTN('Adicionar item'), label='Adicionar item (3)')
    # três itens em ~5 s de fala: o texto entra colado (insertText) logo depois do clique no campo; digitado não cabe (71 letras)
    for k, (item, palavra) in enumerate((('CNPJ conferido', 'CNPJ'), ('Local de retirada combinado', 'local'), ('Frequência da coleta combinada', 'frequência')), 1):
        c.click(SEL(f"{CHK} input[aria-label='Texto do item {k}']"), at=c.A(2, palavra, 0.7), label=f'item {k}')
        c.ev(colar(item), label=f'item {k}: {item}')
    c.confere_campos(['Documentos do fornecedor', 'CNPJ conferido', 'Local de retirada combinado', 'Frequência da coleta combinada'], 'nome e itens', escopo=CHK)
    c.click(BTN('Salvar', within=CHK), at=c.A(2, 'Salvar.', 0.7), label='Salvar (Nova checklist)')
    c.waitfor(text='Checklist criada', timeout=10)
    c.mark(3)
    c.hover(TXTX('Documentos do fornecedor', within=CFG), 0.6, at=c.A(3, 'modelo', 0.6), label='o modelo Documentos do fornecedor na lista')
    c.mark(4)
    c.click(SEL('#tab-btn-etiquetas'), at=c.A(4, 'Etiquetas,', 0.8), label='menu Etiquetas')
    c.waitfor(text='Etiquetas ajudam a classificar oportunidades no Kanban.', timeout=8)
    c.click(BTN('Nova etiqueta'), at=c.A(4, 'Nova', 0.9), label='Nova etiqueta')
    c.waitfor(selector='#crm-label-name', timeout=8)
    c.type(SEL('#crm-label-name'), 'Indústria', at=c.A(4, 'Indústria,', 0.3), cps=22, label='Nome: Indústria')
    c.hover(SEL('#crm-label-color'), 0.2, at=c.A(4, 'cor.', 0.6), label='Cor (o seletor de cor)')
    c.ev(js_cor('#crm-label-color', '#6366f1'), label='Cor: #6366f1')
    c.click(BTN('Salvar', within=ETQ), at=c.A(4, 'Salvar.', 0.7), label='Salvar (Nova etiqueta)')
    c.waitfor(text='Etiqueta criada', timeout=10)
    c.mark(5)
    c.hover(TXT('Indústria', within=CFG), 2.0, at=c.A(5, 'modelos', 0.6), label='a etiqueta Indústria na lista')
    c.mark(6)
    c.cursor((640, 600), at=c.A(6, 'Uma', 0.2), label='cursor sai (plano geral da janela)')
    c.fim()
    return c


EMAIL_PAULO = 'paulo.lacerda@metalurgicajequitiba.example'
COMBO_OPP = lambda txt: SEL(f'{OPP} [role=combobox]', hasText=txt)


def cap08():
    """Nova oportunidade: o quadro do Sucata industrial; título, etapa, valor 8400, sem responsável, empresa avulsa, contato, material,
    quantidade, transporte, previsão 30/11/2026, observações; Salvar; o cartão em Novo."""
    c = cap_novo(8, setup=CRM)
    c.mark(1)
    c.hover(SEL("main button:has-text('Sucata industrial')"), 0.9, at=c.A(1, 'Sucata', 0.6), label='o quadro abre no Sucata industrial')
    c.hover(CAB('Visita técnica'), 1.4, at=c.A(1, 'Visita', 0.6), label='coluna Visita técnica no lugar certo')
    c.mark(2)
    c.click(BTN('Nova oportunidade', nth=0), at=c.A(2, 'Nova', 0.9), label='Nova oportunidade')
    c.waitfor(selector='#crm-title', timeout=8)
    c.type(SEL('#crm-title'), JEQ, at=c.A(2, 'título,', 0.5), cps=40, label='Título: Retalho de chapa da Metalúrgica Jequitibá')
    c.hover(COMBO_OPP('Novo'), 1.0, at=c.A(2, 'etapa', 0.6), label='Etapa *: Novo')
    c.mark(3)
    c.click(SEL('#crm-value'), at=c.A(3, 'valor', 0.8), label='Valor')
    c.press('Control+A', label='seleciona o 0')
    c.type(SEL('#crm-value'), '8400', at=c.A(3, 'oito', 0.1), noClick=True, cps=12, label='Valor 8400 (zoom)')
    c.mark(4)
    c.select(COMBO_OPP('Rafael Nogueira'), 'Sem responsável', at=c.A(4, 'responsável', 0.9), label='Responsável: Sem responsável')
    c.mark(5)
    c.click(COMBO_OPP('Selecionar empresa'), at=c.A(5, 'Empresa,', 0.8), label='Empresa (abre a busca)')
    c.type({'placeholder': 'Buscar cliente ou fornecedor...'}, 'Metalúrgica Jequitibá', at=c.A(5, 'Ela', 0.2), noClick=True, cps=30,
           label='busca: Metalúrgica Jequitibá')
    c.click(OPC('como empresa avulsa'), at=c.A(5, 'avulsa.', 0.7), label='Usar "Metalúrgica Jequitibá" como empresa avulsa', noScroll=True)
    c.type(SEL('#crm-contact'), 'Paulo Lacerda', at=c.A(5, 'Paulo', 0.8), cps=30, label='Contato: Paulo Lacerda')
    c.type(SEL('#crm-contact-role'), 'Suprimentos', at=c.A(5, 'suprimentos.', 0.8), cps=30, label='Área/Setor: Suprimentos')
    c.marcar(SEL('#crm-email'), label='E-mail (sem mexer o cursor)')
    c.ev(js_foco('#crm-email'), label='foco no E-mail')
    c.ev(colar(EMAIL_PAULO), label='E-mail: paulo.lacerda@metalurgicajequitiba.example (colado)')
    c.mark(6)
    c.ev(js_dlg_ate(OPP, 'Operação', 150, 600), at=c.A(6, 'operação,', 0.6), label='a janela desce até Operação')
    c.click(COMBO_OPP('Selecionar material'), at=c.A(6, 'material', 0.8), label='Tipo de material (abre a busca)')
    c.type({'placeholder': 'Buscar material...'}, 'Chap', noClick=True, cps=14, label='busca: Chap')
    c.click(OPC('Chaparia'), at=c.A(6, 'chaparia,', 0.5), label='Chaparia', noScroll=True)
    c.type(SEL('#crm-quantity'), '12000', at=c.A(6, 'doze', 0.8), cps=14, label='Quantidade estimada 12000 Kg (zoom)')
    c.select(COMBO_OPP('Não definido'), 'Frota própria', at=c.A(6, 'frota', 1.0), label='Meio de transporte: Frota própria')
    c.mark(7)
    c.click(SEL('#crm-date'), at=c.A(7, 'trinta', 0.8), label='Previsão de fechamento')
    c.type(SEL('#crm-date'), '30112026', noClick=True, cps=14, label='Previsão de fechamento 30/11/2026')
    c.click(SEL('#crm-notes'), at=c.A(7, 'observações,', 0.8), label='Observações')
    c.type(SEL('#crm-notes'), 'Quer retirada a cada quinze dias, com caçamba.', at=c.A(7, 'que', 0.3), noClick=True, cps=40,
           label='Observações: Quer retirada a cada quinze dias, com caçamba.')
    c.confere_campos([JEQ, '8400', 'Paulo Lacerda', 'Suprimentos', EMAIL_PAULO, '12.000', '2026-11-30', 'Quer retirada a cada quinze dias, com caçamba.'],
                     'campos da Nova oportunidade', escopo=OPP)
    c.confere(OPP, ['Metalúrgica Jequitibá', 'Chaparia', 'Frota própria', 'Sem responsável', 'Novo'], 'escolhas da Nova oportunidade')
    c.mark(8)
    c.click(BTN('Salvar', within=OPP), at=c.A(8, 'Salvar,', 0.8), label='Salvar (Nova oportunidade)')
    c.waitfor(text='Oportunidade criada', timeout=10)
    c.waitfor(target=CARTAO(JEQ), timeout=10)
    c.confere(CARTAO(JEQ)['selector'], [JEQ, 'Paulo Lacerda', 'Metalúrgica Jequitibá', 'Chaparia', '12.000 Kg', 'R$ 8.400,00', '30/11/2026'],
              'o cartão em Novo')
    c.hover(CARTAO(JEQ), 2.4, at=c.A(8, 'Novo,', 0.6), label='o cartão no Novo: material, valor e previsão')
    c.mark(9)
    c.hover(CARTAO(JEQ), 5.0, at=c.A(9, 'Quando', 0.3), label='o cartão (a compra se lança no caixa)')
    c.fim()
    return c


EM = lambda etapa, titulo: SEL(f"main section:has(> header h2:text-is('{etapa}')) p:text-is('{titulo}')")


def cap09():
    """Arrastar o cartão: Novo > Em contato (a automação cria a tarefa); corte (o quadro remonta: selo 1); Em contato > Visita técnica: a trava;
    corte (o cartão volta ao Em contato); ilustração; o cartão."""
    espera = [{'do': 'wait', 'seconds': 31, 'why': 'o selo de tarefas abertas só se atualiza com a consulta vencida (30 s depois da carga)'}]
    c = cap_novo(9, setup=CRM + espera)
    c.mark(1)
    c.drag(ALCA(JEQ), COLUNA('Em contato'), at=round(c.W(1, 'contato.') - 3.4, 2), hold=0.5, label='arrasta o cartão pela alça até Em contato')
    c.waitfor(target=EM('Em contato', JEQ), timeout=8)
    c.wait(0.6)
    c.ev(JS_REMONTA, at=round(c.Lfim(1) + 0.5, 2), label='corte: sai e volta ao CRM (o quadro busca de novo)')
    c.waitfor(target=SELO_TAREFAS(JEQ), timeout=12)
    c.mark(2)
    c.hover(SELO_TAREFAS(JEQ), 4.2, at=c.A(2, 'automação', 0.6), label='selo de tarefas abertas 1 (zoom)')
    c.mark(3)
    c.drag(ALCA(JEQ), COLUNA('Visita técnica'), at=round(c.W(3, 'agora?') - 2.8, 2), hold=0.5, label='arrasta para Visita técnica (a trava)')
    c.waitfor(text='Conclua as tarefas pendentes. Defina um responsável.', timeout=8)
    c.hover(SEL("[data-sonner-toast]:has-text('Conclua as tarefas pendentes')"), 4.0, at=c.A(3, 'mostra', 0.6), noScroll=True,
            label='aviso: Conclua as tarefas pendentes. Defina um responsável. (zoom)')
    c.ev(JS_FECHA_TOAST, at=round(c.Lfim(3) + 0.3, 2), label='corte: fecha o aviso')
    c.cursor((660, 420), label='corte: cursor volta ao quadro')
    c.ev(JS_REMONTA, label='corte: o quadro remonta (o cartão volta ao Em contato)')
    c.waitfor(target=EM('Em contato', JEQ), timeout=12)
    c.mark(4)
    c.hover(CARTAO(JEQ), 1.6, at=c.A(4, 'continua', 0.6), label='o cartão continua em Em contato')
    c.mark(5)
    c.cursor((900, 300), at=c.A(5, 'Uma', 0.2), label='cursor descansa (ilustração)')
    c.mark(6)
    c.hover(CARTAO(JEQ), 3.4, at=c.A(6, 'destravar,', 0.6), label='o cartão (pra destravar, a ficha)')
    c.fim()
    return c


FICHA_SCROLL = lambda texto, y=180: js_dlg_ate(FICHA, texto, y, 600)


def cap10():
    """A ficha: Detalhes (responsável Rafael), valores, etiqueta Indústria, Aplicar modelo (sem clicar), Tarefas (concluir), Histórico;
    fecha e arrasta o cartão para Visita técnica."""
    c = cap_novo(10, setup=CRM)
    c.mark(1)
    c.click(TITULO_CARTAO(JEQ), at=c.A(1, 'Clicando', 0.8), label='clique no cartão (abre a ficha)')
    c.waitfor(text='Comentários e atividades', timeout=10)
    c.hover(TAB('Detalhes'), 0.3, at=c.A(1, 'Detalhes,', 0.6), label='aba Detalhes')
    c.hover(TAB('Tarefas'), 0.2, at=c.A(1, 'Tarefas', 0.6), label='aba Tarefas (1)')
    c.hover(TAB('Histórico'), 0.6, at=c.A(1, 'Histórico.', 0.6), label='aba Histórico')
    c.mark(2)
    c.hover(SEL(f'{FICHA} [role=combobox]', hasText='Sucata industrial'), 0.2, at=c.A(2, 'funil,', 0.6), label='Funil: Sucata industrial')
    c.hover(SEL(f'{FICHA} [role=combobox]', hasText='Em contato'), 0.3, at=c.A(2, 'estágio', 0.6), label='Estágio: Em contato')
    c.hover(SEL(f'{FICHA} [role=combobox]', hasText='Sem responsável'), 0.3, at=c.A(2, 'responsável.', 0.6), label='Responsável: Sem responsável')
    c.select(SEL(f'{FICHA} [role=combobox]', hasText='Sem responsável'), 'Rafael Nogueira', at=c.A(2, 'Rafael,', 0.9), label='Responsável: Rafael Nogueira')
    c.waitfor(target=SEL(f'{FICHA} [role=combobox]', hasText='Rafael Nogueira'), timeout=8)
    c.mark(3)
    c.ev(FICHA_SCROLL('Valor Estimado', 160), at=c.A(3, 'Embaixo,', 0.5), label='a ficha desce até os valores')
    c.hover(TXT('Valor Estimado', within=FICHA), 0.2, at=c.A(3, 'valor,', 0.6), label='Valor Estimado R$ 8.400,00')
    c.hover(TXT('Previsão Fechamento', within=FICHA), 0.2, at=c.A(3, 'previsão,', 0.6), label='Previsão Fechamento 30/11/2026')
    c.hover(TXT('Material', within=FICHA), 0.2, at=c.A(3, 'material', 0.6), label='Material: Chaparia')
    c.hover(TXT('Empresa', within=FICHA), 0.2, at=c.A(3, 'empresa.', 0.6), label='Empresa: Metalúrgica Jequitibá')
    c.ev(FICHA_SCROLL('Observações', 300), at=c.A(3, 'observações,', 0.9), label='a ficha desce até as Observações')
    c.hover(SEL('#opportunity-notes'), 3.0, at=c.A(3, 'salvam', 0.6), label='Observações (salvam sozinhas; o motivo da perda vai aqui)')
    c.mark(4)
    c.ev(FICHA_SCROLL('Etiquetas', 380), at=c.A(4, 'Em', 0.3), label='a ficha desce até Etiquetas e Checklists')
    c.click(BTN('Gerenciar', within=FICHA), at=c.A(4, 'aplico', 0.8), label='Etiquetas: Gerenciar')
    c.click(SEL(f"{POP} button:has-text('Indústria')"), at=c.A(4, 'Indústria,', 0.6), label='marca Indústria', noScroll=True)
    c.waitfor(target=SEL(f"{FICHA} span:text-is('Indústria')"), timeout=6)
    c.press('Escape', label='fecha a lista das etiquetas')
    c.wait(0.4)
    c.hover(BTNX('Aplicar modelo', within=FICHA), 1.6, at=c.A(4, 'Aplicar', 0.6), label='Checklists: Aplicar modelo (sem clicar)')
    c.mark(5)
    c.ev(FICHA_SCROLL('Detalhes', 140), at=c.A(5, 'Na', 0.6), label='a ficha sobe até as abas')
    c.click(TAB('Tarefas'), at=c.A(5, 'Tarefas', 0.8), label='aba Tarefas')
    c.waitfor(text='Agendar visita na Metalúrgica Jequitibá', timeout=8)
    c.confere(FICHA, ['Agendar visita na Metalúrgica Jequitibá', '11/11'], 'a tarefa da automação, 11/11')
    c.hover(SEL(f"{FICHA} p:text-is('Agendar visita na Metalúrgica Jequitibá')"), 1.2, at=c.A(5, 'Agendar', 0.6),
            label='tarefa da automação: Agendar visita na Metalúrgica Jequitibá (11/11)')
    c.click(BTN('Concluir tarefa', within=FICHA), at=c.A(5, 'concluo.', 0.8), label='Concluir tarefa')
    c.waitfor(target=BTN('Reabrir tarefa', within=FICHA), timeout=8)
    c.mark(6)
    c.click(TAB('Histórico'), at=c.A(6, 'Histórico', 0.8), label='aba Histórico')
    c.waitfor(text='Etapa alterada de "Novo" para "Em contato".', timeout=8)
    c.hover(TXT('Etapa alterada de "Novo" para "Em contato".', within=FICHA), 2.0, at=c.A(6, 'mudança', 0.6),
            label='Histórico: Etapa alterada de "Novo" para "Em contato". (quem e quando)')
    c.mark(7)
    c.click(BTN('Fechar', within=FICHA), at=c.A(7, 'Fechando', 0.8), label='fecha a ficha', noScroll=True)
    c.waitfor(gone={'selector': FICHA}, timeout=8)
    c.drag(ALCA(JEQ), COLUNA('Visita técnica'), at=round(c.W(7, 'Visita') - 2.6, 2), hold=0.5, label='arrasta o cartão para Visita técnica (agora passa)')
    c.waitfor(target=EM('Visita técnica', JEQ), timeout=10)
    c.confere('main', ['Visita técnica'], 'o cartão em Visita técnica')
    c.fim()
    return c


COL_TAREFA = lambda nome: SEL(f"main div.rounded-xl:has(> div > h3:text-is('{nome}'))")
CAB_TAREFA = lambda nome: SEL(f"main div:has(> h3:text-is('{nome}'))")
TH = lambda nome: SEL(f"main th:has-text('{nome}')")
AGENDA_CRM = ['/agenda']


def cap11():
    """Tarefas e Agenda: aba Tarefas (Kanban), Nova tarefa Enviar proposta (Jequitibá, Rafael, 12/11, Alta), Lista, Calendário, Agenda (selo CRM,
    ilustração), clique leva ao CRM (Editar oportunidade > Cancelar)."""
    aquece_agenda = vai('/agenda', 'Agenda') + CRM
    c = cap_novo(11, setup=CRM + aquece_agenda)
    c.mark(1)
    c.click(BTN('Tarefas'), at=c.A(1, 'Tarefas.', 0.8), label='aba Tarefas')
    c.waitfor(text='Tarefas vinculadas às oportunidades do funil', timeout=10)
    c.hover(TXT('Tarefas vinculadas às oportunidades do funil'), 1.0, at=c.A(1, 'junta', 0.6), label='Tarefas vinculadas às oportunidades do funil')
    c.hover(CAB_TAREFA('Pendente'), 0.3, at=c.A(1, 'pendente,', 0.6), label='coluna Pendente')
    c.hover(CAB_TAREFA('Em andamento'), 0.3, at=c.A(1, 'andamento,', 0.6), label='coluna Em andamento')
    c.hover(CAB_TAREFA('Concluída'), 0.2, at=c.A(1, 'concluída', 0.6), label='coluna Concluída (a tarefa da visita)')
    c.hover(CAB_TAREFA('Cancelada'), 0.6, at=c.A(1, 'cancelada.', 0.6), label='coluna Cancelada')
    c.mark(2)
    c.click(BTN('Nova tarefa'), at=c.A(2, 'Nova', 0.9), label='Nova tarefa')
    c.waitfor(selector=TAREFA, timeout=8)
    c.type({'placeholder': 'Descreva a tarefa...'}, 'Enviar proposta', at=c.A(2, 'Enviar', 0.8), cps=30, label='Título: Enviar proposta')
    c.click(SEL(f'{TAREFA} button[role=combobox]', hasText='Selecionar...'), at=c.A(2, 'ligada', 0.8), label='Oportunidade * (abre a busca)')
    c.click(OPC(JEQ), at=c.A(2, 'Jequitibá,', 0.6), label='Retalho de chapa da Metalúrgica Jequitibá', noScroll=True)
    c.click(SEL(f'{TAREFA} button[role=combobox]', hasText='Sem responsável'), at=c.A(2, 'com', 0.8, nth=0), label='Responsável (abre a busca)')
    c.click(OPC('Rafael Nogueira'), at=c.A(2, 'Rafael,', 0.5), label='Rafael Nogueira', noScroll=True)
    c.click(SEL(f"{TAREFA} button:has-text('/2026')"), at=c.A(2, 'quinta,', 0.8), label='Data * (abre o calendário)')
    c.click(SEL(f"{POP} button[name=day]:text-is('12')"), at=c.A(2, 'doze,', 0.6), label='dia 12', noScroll=True)
    c.select(SEL(f'{TAREFA} button[role=combobox]', hasText='Média'), 'Alta', at=c.A(2, 'prioridade', 0.9), label='Prioridade: Alta')
    c.confere(TAREFA, ['Enviar proposta', JEQ, 'Rafael Nogueira', '12/11/2026', 'Alta'], 'Nova tarefa preenchida')
    c.click(BTN('Salvar', within=TAREFA), at=c.A(2, 'Salvar.', 0.8), label='Salvar (Nova tarefa)')
    c.waitfor(text='Tarefa criada', timeout=10)
    c.mark(3)
    c.hover(SEL("main div.rounded-xl:has(> div > h3:text-is('Pendente')) p:text-is('Enviar proposta')"), 0.8, at=c.A(3, 'Pendente.', 0.6),
            label='Enviar proposta em Pendente')
    c.click(SEL("[aria-label='Lista']"), at=c.A(3, 'Lista,', 0.8), label='visão Lista')
    c.hover(TH('Oportunidade'), 0.4, at=c.A(3, 'oportunidade,', 0.6), label='coluna Oportunidade')
    c.hover(TH('Responsável'), 0.4, at=c.A(3, 'responsável,', 0.6), label='coluna Responsável')
    c.hover(TH('Data'), 0.2, at=c.A(3, 'data', 0.6), label='coluna Data')
    c.hover(TH('Prioridade'), 0.6, at=c.A(3, 'prioridade.', 0.6), label='coluna Prioridade')
    c.mark(4)
    c.click(SEL("[aria-label='Calendário']"), at=c.A(4, 'Calendário,', 0.8), label='visão Calendário')
    c.hover(SEL("main button[title^='Enviar proposta']"), 1.2, at=c.A(4, 'tarefa', 0.6), label='Enviar proposta no dia 12 (calendário)')
    c.mark(5)
    c.click(SEL("a[href='/agenda']"), at=c.A(5, 'Agenda,', 0.9), label='Agenda (menu lateral)', noScroll=True)
    c.waitfor(target=SEL("main button:has-text('Enviar proposta')"), timeout=15)
    c.hover(SEL("main button:has-text('Enviar proposta')"), 2.4, at=c.A(5, 'selo', 0.6), label='Enviar proposta no dia 12, selo CRM (zoom)')
    c.mark(6)
    c.cursor((900, 160), at=c.A(6, 'É', 0.2), label='cursor descansa (ilustração)')
    c.mark(7)
    c.click(SEL("main button:has-text('Enviar proposta')"), at=c.A(7, 'Clicando', 0.8), label='clique na tarefa (leva ao CRM)')
    c.waitfor(text='Editar oportunidade', timeout=15)
    c.hover(SEL('#crm-title'), 1.4, at=c.A(7, 'oportunidade', 0.6), label='Editar oportunidade da Jequitibá')
    c.click(BTN('Cancelar', within=OPP), at=c.A(7, 'CRM.', 0.4, nth=1), label='Cancelar')
    c.waitfor(gone={'selector': OPP}, timeout=8)
    c.fim()
    return c


FILTRO_COMBO = lambda k: SEL(f'{FILTROS} button[role=combobox]', nth=k)


def cap12():
    """Filtros e busca (17:30, seis cartões): os quatro cartões; busca alumínio; Filtros: Rafael + Em negociação = R$ 26.200,00; Limpar filtros."""
    c = cap_novo(12, setup=CRM)
    c.mark(1)
    c.confere('main', ['Total de oportunidades', '6', 'R$ 62.300,00', 'R$ 19.000,00', 'R$ 41.650,00'], 'seis oportunidades, R$ 62.300,00')
    c.hover(METRICA('Total de oportunidades'), 1.2, at=c.A(1, 'seis', 0.6), label='Total de oportunidades 6 (zoom)')
    c.hover(METRICA('Valor total'), 2.4, at=c.A(1, 'sessenta', 0.6), label='Valor total R$ 62.300,00 (zoom)')
    c.mark(2)
    c.hover(METRICA('Ganhos'), 2.6, at=c.A(2, 'dezenove', 0.6), label='Ganhos R$ 19.000,00 (zoom)')
    c.hover(METRICA('Em negociação'), 3.0, at=c.A(2, 'quarenta', 0.6), label='Em negociação R$ 41.650,00 (zoom)')
    c.mark(3)
    busca = SEL("main input[placeholder^='Buscar por título']")
    c.click(busca, at=c.A(3, 'busca,', 0.8), label='Busca')
    c.type(busca, 'alumínio', at=c.A(3, 'Digitando', 0.1), noClick=True, cps=14, label='busca: alumínio')
    c.waitfor(gone=SEL("main p:text-is('Ferro de demolição da Construtora Pilar')"), timeout=8)
    c.confere('main', ['Perfis de alumínio da Esquadrias Horizonte', 'Total de oportunidades (filtrado)', 'R$ 17.800,00'], 'sobra a Esquadrias Horizonte (filtrado)')
    c.hover(CARTAO('Perfis de alumínio da Esquadrias Horizonte'), 1.0, at=c.A(3, 'Esquadrias', 0.6), label='o cartão da Esquadrias Horizonte')
    c.hover(METRICA_X('Total de oportunidades (filtrado)'), 1.6, at=c.A(3, 'cima', 0.6), label='cartões de cima dizem filtrado')
    c.mark(4)
    c.type(busca, '', at=c.A(4, 'Nos', 0.8), clear=True, label='apaga a busca')
    c.click(BTNX('Filtros'), at=c.A(4, 'Filtros,', 0.8), label='Filtros')
    c.waitfor(selector=FILTROS, timeout=8)
    c.hover(FILTRO_COMBO(0), 0.3, at=c.A(4, 'situação,', 0.6), label='Status')
    c.hover(SEL('#crm-min-value'), 0.2, at=c.A(4, 'faixa', 0.6), label='Valor mínimo / Valor máximo')
    c.hover(FILTRO_COMBO(1), 0.3, at=c.A(4, 'responsável,', 0.6), label='Responsável')
    c.hover(FILTRO_COMBO(2), 0.2, at=c.A(4, 'material', 0.6), label='Material')
    c.hover(FILTRO_COMBO(3), 0.6, at=c.A(4, 'transporte.', 0.6), label='Meio de transporte')
    c.mark(5)
    c.select(FILTRO_COMBO(1), 'Rafael Nogueira', at=c.A(5, 'Rafael', 0.9), label='Responsável: Rafael Nogueira')
    c.select(FILTRO_COMBO(0), 'Em negociação', at=c.A(5, 'negociação.', 0.9), label='Status: Em negociação')
    c.click(BTN('Aplicar'), at=c.A(5, 'Aplicar,', 0.8), label='Aplicar')
    c.waitfor(gone={'selector': FILTROS}, timeout=8)
    c.confere('main', ['Valor total (filtrado)', 'R$ 26.200,00', JEQ, 'Perfis de alumínio da Esquadrias Horizonte'], 'ficam dois cartões: R$ 26.200,00')
    c.hover(METRICA_X('Valor total (filtrado)'), 2.0, at=c.A(5, 'vinte', 0.6), label='Valor total (filtrado) R$ 26.200,00 (zoom)')
    c.mark(6)
    c.click(BTNX('Filtros'), at=c.A(6, 'ver', 0.8), label='Filtros (2)')
    c.waitfor(selector=FILTROS, timeout=8)
    c.click(BTN('Limpar filtros'), at=c.A(6, 'Limpar', 0.8), label='Limpar filtros')
    c.click(BTN('Aplicar'), label='Aplicar (voltam os seis)')
    c.waitfor(gone={'selector': FILTROS}, timeout=8)
    c.confere('main', ['Total de oportunidades', '6', 'R$ 62.300,00'], 'voltam os seis')
    c.fim()
    return c


def cap13():
    """Recapitulando (passeio pelo estado final, 17:30): Funil de vendas, abas e cartões; Configurações (Sucata industrial padrão, Visita técnica
    com cor e orientação; regras e automação do Em contato; checklist e etiqueta); o cartão da Jequitibá, a aba Tarefas e a Agenda.
    O roteiro pede montagem com trechos dos capítulos: esta gravação é a reserva (estado final, sem refazer as ações)."""
    aquece_agenda = vai('/agenda', 'Agenda') + CRM
    c = cap_novo(13, setup=CRM + aquece_agenda)
    c.mark(1)
    c.hover(SEL("main button:has-text('Funil de vendas')"), 0.8, at=c.A(1, 'Funil', 0.6), label='Funil de vendas (montado sozinho)')
    c.hover(BTN('Funil'), 0.2, at=c.A(1, 'abas', 0.6), label='abas Funil e Tarefas')
    c.hover(METRICA('Total de oportunidades'), 1.0, at=c.A(1, 'quatro', 0.6), label='os quatro cartões')
    c.mark(2)
    c.click(BTN('Configurações do CRM/Kanban'), at=c.A(2, 'Criou', 0.9), label='Configurações do CRM/Kanban')
    c.waitfor(text='Organize os funis comerciais e as etapas de cada Kanban.', timeout=12)
    c.hover(TXT('Padrão', within=LINHA_FUNIL_S('Sucata industrial')), 0.5, at=c.A(2, 'padrão,', 0.6), label='Sucata industrial, Padrão')
    c.click(BTN('Expandir Sucata industrial'), at=c.A(2, 'pôs', 0.8), label='abre o Sucata industrial')
    c.waitfor(text='Estágios deste funil', timeout=8)
    c.click(EDITAR_ETAPA('Visita técnica'), at=c.A(2, 'cor', 0.8), label='Configurar Visita técnica (cor e orientação)')
    c.waitfor(text='Configurar Visita técnica', timeout=8)
    c.mark(3)
    fecha_janela(c, ETAPA, at=c.A(3, 'Ligou', 0.4), label='fecha a Visita técnica')
    c.click(EDITAR_ETAPA('Em contato'), label='Configurar Em contato')
    c.waitfor(text='Configurar Em contato', timeout=8)
    c.click(TAB('Regras'), at=c.A(3, 'saída', 0.8), label='aba Regras (Tarefas e Responsável ligadas)')
    c.click(TAB('Automações'), at=c.A(3, 'automação', 0.8), label='aba Automações (Agendar a visita, Ativa)')
    fecha_janela(c, ETAPA, at=c.A(3, 'além', 0.5), label='fecha o Em contato')
    c.click(SEL('#tab-btn-checklists'), at=c.A(3, 'checklist', 0.8), label='Checklists')
    c.click(SEL('#tab-btn-etiquetas'), at=c.A(3, 'etiqueta.', 0.8), label='Etiquetas')
    c.mark(4)
    fecha_janela(c, CFG, at=c.A(4, 'Cadastrou', 0.6), label='fecha as Configurações')
    c.hover(CARTAO(JEQ), 1.2, at=c.A(4, 'Metalúrgica', 0.6), label='o cartão da Jequitibá em Visita técnica')
    c.click(BTN('Tarefas'), at=c.A(4, 'Tarefas', 0.9), label='aba Tarefas')
    c.waitfor(text='Tarefas vinculadas às oportunidades do funil', timeout=10)
    c.click(SEL("a[href='/agenda']"), at=c.A(4, 'Agenda,', 0.9), label='Agenda', noScroll=True)
    c.waitfor(target=SEL("main button:has-text('Enviar proposta')"), timeout=15)
    c.cursor((900, 300), label='cursor sai do menu')
    c.mark(5)
    c.fim()
    return c


CAPS_ROBO = {n: globals()[f'cap{n:02d}'] for n in range(14) if f'cap{n:02d}' in globals()}

if __name__ == '__main__':
    quais = [int(a) for a in sys.argv[1:]] or sorted(CAPS_ROBO)
    for n in quais:
        c = CAPS_ROBO[n]()
        for i, w, k, tot in c.ambiguas:
            if os.environ.get('AMBIGUAS'):
                print(f'   palavra repetida: L{i} "{w}" nth={k} de {tot}')
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
        path = os.path.join(HERE, f'cap{n:02d}.json')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
        resp = ''.join(f'\n    RESPIRO PENDENTE: a voz precisa de +{dd:.2f} s antes da L{li} (fim da L{li - 1} em {t:.2f} s): pausas.py {n:02d} {t:.2f}:{dd:.2f}'
                       for li, t, dd in c.respiros)
        print(f'cap{n:02d}: {len(d["steps"])} passos, narração {c.dur:.1f} s ({"estimada" if c.estimada else "da voz"}), FAKE_NOW {FAKE_NOW[n]}{resp}')
