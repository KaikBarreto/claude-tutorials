#!/usr/bin/env python3
"""T19 · gera rec/t19/cap00..cap13.json (roteiros do robô) a partir da voz ($TUT_HOME/t19/narracao/capNN.json).

Funcionários e ponto eletrônico no COMPUTADOR (janela 1280x800, menu lateral aberto), logado como Rafael Nogueira (MASTER, Recicla
Vale Metais), no EcoSistema 1.59.154; o cap09 é inteiro no CELULAR ("device": "phone", sem login: o link pessoal do Gabriel).
O login roda no `setup` (não filmado), com "$TUT_USER"/"$TUT_SENHA" do ambiente: o capítulo abre o navegador sem sessão ("anonymous").
Relógio do mundo: FAKE_NOW 10/11/2026 08:30 (terça) em todos os capítulos, o mesmo no Supabase falso e no robô.
Os `at` saem da palavra que anuncia cada passo: A(linha, palavra, folga) = início da palavra - folga (o custo do gesto, docs/04).
Respiros (RESPIROS): onde a tela precisa de mais tempo que a fala dá (o preenchimento da jornada no cap11), o gerador abre o vão
na voz estimada e AVISA (a voz pede `pausas.py NN T:DUR`); a voz com os respiros vai para rec/t19/_voz/capNN.json (o resumo.py lê).
Rodar de qualquer pasta: `python3 -I rec/t19/gerar.py [NN ...]`. Depois: `node rec/record.mjs rec/t19/capNN.json --check`.

Cadeia de sementes (rec/mundo/seeds-extra/t19/, todas por cima do mundo base): inicio (caps 0 a 2, rec/t19/t19_sementes.py) ->
apos-cap02 (3) -> apos-cap03 (4) -> apos-cap04 (5) -> apos-cap05 (6) -> apos-cap06 (7 e 8) -> apos-cap08 (9) -> apos-cap09 (10) ->
apos-cap10 (11) -> apos-cap11 (12) -> apos-cap12 (13). Cada apos-capNN sai do ensaio do capítulo (rec/t19/t19_semente.mjs, na mesma
trava): as tabelas do RH inteiras, o que a aula criou nas outras (caixa, banco) e os acertos de inicio (slug do tablet, categoria).

Particularidades (código 1.59.154, planejamento/ecoflix/T19/inventario.md):
 - Abas da página: botões em nav[aria-label="Navegação da seção"] (não são role=tab). Lista "Equipe": cada pessoa é um
   role=listitem com um botão (abre a ficha à direita) e o menu "Ações de <nome>" (HoverDropdownMenu: abre ao passar o mouse; um
   clique no gatilho FECHA o menu aberto pelo hover).
 - Campos do cadastro por id (#name, #cpf, #phone, #position, #department, #hire_date, #salary, #monthly_cost, #dependents,
   #vt-enabled, #vt-value, #pix_key); dinheiro é digitado como o cliente digita ("2520,00").
 - Horas da jornada individual: TimeField (botão + roleta em Popover, listbox "Horas"/"Minutos"); o preenchimento dos cinco dias é
   um time-lapse por `eval` (o roteiro marca o trecho acelerado, selo 4x).
 - Celular (cap09): câmera falsa no `setup` (getUserMedia devolve um canvas com um avatar ilustrado, nenhum rosto real), posição no
   pátio (passo geo) e o Nominatim do mundo devolve "Rua das Oficinas, 1250 - Parque Industrial - Taubaté".
 - Observador `OBS` guarda em window.__avisos todo aviso de erro do app; o passo final devolve a lista (tem de sair vazia).
"""
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TUT_HOME = os.path.normpath(os.path.join(HERE, '..', '..'))
NARR = os.path.join(TUT_HOME, 't19', 'narracao')
VOZ_PROV = os.path.join(HERE, '_voz')
sys.path.insert(0, HERE)
from t19_sementes import t19_slug  # noqa: E402  (o mesmo slug do handler rpc/generate_ponto_slug.mjs)

RAFAEL = '34c36c63-0890-5e89-8963-7c77b7996908'      # stableId('user.rafael') do mundo
try:
    VERSAO = open(os.path.join(TUT_HOME, 'app', 'dist', '.versao-app'), encoding='utf8').read().strip() or '1.59.154'
except OSError:
    VERSAO = '1.59.154'
FAKE_NOW = {n: '2026-11-10T08:30:00-03:00' for n in range(14)}
HOJE = {n: FAKE_NOW[n][:10] for n in range(14)}

NOMES = ['Abertura', 'A tela Funcionários e suas abas', 'Cadastrar o funcionário', 'Campos de folha', 'Departamentos',
         'Lançar vale, bônus e falta', 'Pagar e receber do funcionário', 'O extrato do funcionário', 'Ligar o ponto e gerar o link',
         'O ponto pelo celular', 'Registro e folha de ponto', 'Configurações do ponto', 'Arquivar ou excluir', 'Recapitulando']
SEMENTE = {0: 'inicio', 1: 'inicio', 2: 'inicio', 3: 'apos-cap02', 4: 'apos-cap03', 5: 'apos-cap04', 6: 'apos-cap05', 7: 'apos-cap06',
           8: 'apos-cap06', 9: 'apos-cap08', 10: 'apos-cap09', 11: 'apos-cap10', 12: 'apos-cap11', 13: 'apos-cap12'}
# capítulos cujo estado final vira semente (o ensaio grava seeds-extra/t19/apos-capNN.json)
GRAVA_SEMENTE = (2, 3, 4, 5, 6, 8, 9, 10, 11, 12)
# vão mínimo (s) na voz ANTES de uma palavra: {cap: [(linha 1-based, palavra ou None = início da linha, nth, segundos)]}
RESPIROS = {11: [(5, 'Salvar', 0, 7.0)]}
GABRIEL_SLUG = t19_slug('Gabriel Rocha')


# ---------------------------------------------------------------- voz
def norm(s):
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode().lower()
    return ''.join(ch for ch in s if ch.isalnum() or ch in '?')


def carregar_voz(n):
    """voz do capítulo ($TUT_HOME/t19/narracao/capNN.json, estimada ou da voz de verdade) com os RESPIROS aplicados.
    Devolve (words, linhas, dur, estimada, respiros_pendentes)."""
    real = json.load(open(os.path.join(NARR, f'cap{n:02d}.json'), encoding='utf8'))
    words = [dict(w) for w in real['words']]
    linhas = [dict(l) for l in real['linhas']]
    dur = float(real['dur'])
    pend = []   # (linha, T do pausas.py (fim da palavra anterior no take original), segundos que faltam)
    for li, palavra, nth, need in RESPIROS.get(n, []):
        i = li - 1
        if i >= len(linhas):
            continue
        if palavra is None:
            if i <= 0:
                continue
            ini, fim_ant, t_take = linhas[i]['s'], linhas[i - 1]['e'], real['linhas'][i - 1]['e']
            k0 = next(k for k, w in enumerate(words) if w['linha'] == i)
        else:
            hits = [k for k, w in enumerate(words) if w['linha'] == i and norm(w['w']).startswith(norm(palavra))]
            if len(hits) <= nth:
                raise SystemExit(f'cap{n:02d}: respiro antes de "{palavra}" (L{li}) sem a palavra')
            k0 = hits[nth]
            ini, fim_ant = words[k0]['s'], words[k0 - 1]['e']
            t_take = real['words'][k0 - 1]['e']
        gap = ini - fim_ant
        if gap + 0.02 >= need:
            continue
        d = round(need - gap, 2)
        pend.append((li, round(t_take, 2), d))
        for w in words[k0:]:
            w['s'] = round(w['s'] + d, 3)
            w['e'] = round(w['e'] + d, 3)
        for l in linhas[i + (1 if palavra is not None else 0):]:
            l['s'] = round(l['s'] + d, 3)
            l['e'] = round(l['e'] + d, 3)
        if palavra is not None:
            linhas[i]['e'] = round(linhas[i]['e'] + d, 3)
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
       "Something went wrong|inv[áa]lido/i;const chk=(t)=>{t=(t||'').trim();const m=t&&t.match(new RegExp('[^]{0,40}('+re.source+')[^]{0,40}','i'));"
       "if(m&&window.__avisos.length<10)window.__avisos.push(m[0].replace(/[\\n\\r\\t ]+/g,' '))};new MutationObserver(ms=>{for(const m of ms){"
       "m.addedNodes.forEach(n=>chk(n.textContent));if(m.type==='characterData')chk(m.target.textContent)}}).observe(document.body,"
       "{childList:true,subtree:true,characterData:true});chk(document.body.innerText);return 1})()")


class Cap:
    def __init__(s, n, pace=0.5, cps=40, start=(760, 470), setup=None, prewarm=None, phone=False, recolhe=True):
        s.n = n
        s.words, s.linhas, s.dur, s.estimada, s.respiros = carregar_voz(n)
        s.steps = []
        s.pace, s.cps, s.start = pace, cps, start
        s.phone = phone
        s.prewarm = prewarm or (['/dashboard'] if phone else ['/login'])
        s.setup = (list(setup or []) if phone else LOGIN + ([RECOLHE, {'do': 'wait', 'seconds': 0.7}] if recolhe else []) + list(setup or [])) + [{'do': 'eval', 'js': OBS}]
        s.anchors = []
        s.ambiguas = []
        s.pending = []

    # ---- tempo
    def L(s, i):
        return round(s.linhas[i - 1]['s'], 2)

    def Lfim(s, i):
        return round(s.linhas[i - 1]['e'], 2)

    def tem(s, i, palavra):
        return any(w['linha'] == i - 1 and norm(w['w']).startswith(norm(palavra)) for w in s.words)

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

    def hover(s, target, seconds=0.5, at=None, label=None, **kw):
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

    def digita(s, campo, texto, palavra_t, label, folga_clique=0.9, clear=False):
        """clica no campo antes e digita sem clique na palavra (docs/04: cps 40, at = palavra - 0,05)"""
        s.click(campo, at=round(max(0.0, palavra_t - folga_clique), 2), label=f'campo {label}')
        kw = {'noClick': True}
        if clear:
            kw['clear'] = True
        return s.type(campo, texto, at=round(max(0.0, palavra_t - 0.05), 2), label=label, cps=40, **kw)

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
        """registra o retângulo do alvo para a edição (zoom/destaque) SEM mexer o mouse (passo `type` sem clique e sem texto)"""
        kw.setdefault('optional', True)
        kw.setdefault('timeout', 4)
        return s._p({'do': 'type', 'target': target, 'text': '', 'noClick': True}, at, label, kw)

    def cursor(s, ponto, at=None, label=None):
        """leva o cursor a um ponto neutro (scroll de 0 px): tira o cursor de cima do menu ou de um alvo"""
        return s._p({'do': 'scroll', 'point': {'x': ponto[0], 'y': ponto[1]}, 'by': 0, 'duration': 0.2, 'after': 0}, at,
                    label or 'cursor a um ponto neutro', {})

    def rolar(s, by, at=None, label=None, ponto=(760, 470), duration=0.5, after=100):
        return s._p({'do': 'scroll', 'point': {'x': ponto[0], 'y': ponto[1]}, 'by': by, 'duration': duration, 'after': after}, at, label, {})

    def toque(s, alvo, expr, ponto, at, label):
        """celular: toque num elemento fixo (rodapé): cursor ao ponto, retângulo do alvo e o toque sintético por eval no `at`"""
        s.cursor(ponto, at=round(max(0.0, at - 0.6), 2), label=label + ' (dedo)')
        s.marcar(alvo, label=label)
        return s.ev(f"(()=>{{const b={expr};if(!b)return 'SEM ALVO';b.click();return 'tocado'}})()", at=at, label=label + ' (toque)')

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
        """um hover com `at` termina antes do próximo passo com `at`: o tempo parado não empurra a marca seguinte (T26)"""
        for k, st in enumerate(s.steps):
            if st.get('do') != 'hover' or st.get('at') is None:
                continue
            prox = next((x['at'] for x in s.steps[k + 1:] if x.get('at') is not None), None)
            if prox is None:
                continue
            cabe = round(prox - 0.05 - st['at'] - chegada, 2)
            if st.get('seconds', 0.5) > cabe:
                st['seconds'] = max(0.1, cabe)

    def out(s):
        est = 'ESTIMADA' if s.estimada else 'da voz'
        resp = (' RESPIROS PENDENTES: ' + ', '.join(f'na L{li} +{d:.2f} s (T {t:.2f} s no take)' for li, t, d in s.respiros)) if s.respiros else ''
        d = {
            'name': f't19-cap{s.n:02d}',
            'title': f'T19 · Cap. {s.n} · {NOMES[s.n]} (narração {str(round(s.dur, 1)).replace(".", ",")} s, {est}{resp}; '
                     f'marcas L1..L{len(s.linhas)} = início de cada linha do roteiro; FAKE_NOW {FAKE_NOW[s.n]})',
            'fakeNow': FAKE_NOW[s.n],
            'seed': f't19-cap{s.n:02d}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
            'start': {'x': s.start[0], 'y': s.start[1]},
            'anonymous': True,
            'storage': storage(s.n, s.phone),
            'seedExtra': [f't19/{SEMENTE[s.n]}'],
            'prewarm': s.prewarm, 'setup': s.setup, 'steps': s.steps,
        }
        if s.phone:
            d['device'] = 'phone'
        return d


def storage(n, phone=False):
    """o que a primeira entrada do Rafael mostraria por cima da tela, já visto (o robô entra sem sessão: modo "anonymous")"""
    if phone:
        return {'pwa-install-dismissed': 'true'}
    return {
        'app_version': VERSAO, 'notification_shown_version': VERSAO, 'pwa-install-dismissed': 'true', 'theme': 'light',
        f'daily-tasks-reminder-last-shown-{RAFAEL}': HOJE[n], 'initial-preferences-set': 'true',
        f'dominex:daily-tasks-shown:{RAFAEL}': HOJE[n],
    }


# ---------------------------------------------------------------- alvos
BTN = lambda n, **kw: {'role': 'button', 'name': n, 'exact': True, **kw}
LINK = lambda n, **kw: {'role': 'link', 'name': n, 'exact': True, **kw}
TXT = lambda t, **kw: {'text': t, 'exact': True, **kw}
TXTX = lambda t, **kw: {'text': t, **kw}
SEL = lambda s, **kw: {'selector': s, **kw}
ITEM = lambda n, **kw: {'role': 'menuitem', 'name': n, **kw}
OPT = lambda n, **kw: {'role': 'option', 'name': n, 'exact': True, **kw}
DLG = '[role=dialog]'
POP = '[data-radix-popper-content-wrapper]'
ABAS = {'Funcionários': 'employees', 'Registro de Ponto': 'registro-ponto', 'Folha de Ponto': 'espelho-ponto', 'Ausências': 'ausencias',
        'Configurações de Ponto': 'config-ponto', 'Configurações de RH': 'config-rh', 'Dashboard': 'dashboard'}
ABA = lambda t: SEL(f"#tab-btn-{ABAS[t]}")
CALC = "[role=dialog]:has(h2:text-is('Calcular custo mensal'))"     # a calculadora abre POR CIMA do cadastro (duas janelas)
LINHA = lambda nome: SEL(f"main [role=listitem] > button:has(p:text-is('{nome}'))")
ACOES = lambda nome: SEL(f"main [role=listitem] button[aria-label='Ações de {nome}']")
FICHA = "main section[aria-label^='Detalhes de']"
BOTAO_FICHA = lambda t: SEL(f"{FICHA} button:text-is('{t}')")
RESUMO = lambda rot: SEL(f"{FICHA} div:has(> p:text-is('{rot}'))")
DADO = lambda rot: SEL(f"{FICHA} dl > div:has(> dt:text-is('{rot}'))")
CAMPO = lambda cid, esc=DLG: SEL(f'{esc} #{cid}')
BDLG = lambda t, esc=DLG: SEL(f"{esc} button:text-is('{t}'):not(.absolute)")
DTAB = lambda t: SEL(f"{DLG} [role=tab]:has-text('{t}')")
SALDO_LINHA = lambda nome, valor: SEL(f"main [role=listitem]:has(p:text-is('{nome}')) :text-is('{valor}')")

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
AGUARDA = {'do': 'waitFor', 'idle': True, 'timeout': 15}
# menu lateral recolhido (a 1280 px com o menu aberto a faixa de abas corta "Configurações de RH" e esconde "Dashboard", e a ficha
# corta o nome: "Ed..."); o cap00 fica com o menu aberto (o item "Funcionários (RH)" é o assunto)
RECOLHE = {'do': 'eval', 'js': ("(()=>{const sb=document.querySelector('[data-state][data-collapsible]');if(sb&&sb.getAttribute('data-state')==='collapsed')"
                                "return 'ja recolhido';const b=document.querySelector('header button.h-8.w-8');if(!b)return 'SEM ALVO';b.click();return 'recolhido'})()")}
SUBTITULO = 'Gerencie sua equipe e controle de pagamentos'


def vai(url, espera):
    return [{'do': 'goto', 'url': url}, {'do': 'waitFor', 'text': espera, 'timeout': 30}, AGUARDA]


RH = vai('/funcionarios', SUBTITULO) + [{'do': 'waitFor', 'target': LINHA('Rafael Nogueira'), 'timeout': 20}, {'do': 'wait', 'seconds': 0.6}]


def aba_setup(t, espera):
    return [{'do': 'click', 'target': ABA(t)}, {'do': 'waitFor', 'text': espera, 'timeout': 20}, {'do': 'wait', 'seconds': 0.8}]


FECHAR_EVAL = (r"""(() => { const ds = [...document.querySelectorAll('[role=dialog]')]; const d = ds[ds.length - 1]; if (!d) return 'ja fechada'; """
               r"""const b = [...d.querySelectorAll('button')].find((x) => [x.textContent, x.getAttribute('aria-label')].some((v) => /^\s*(fechar|close)\s*$/i.test(v || ''))); """
               r"""if (!b) return 'sem botao Fechar'; b.click(); return 'fechada pelo botao'; })()""")


def fechar_janela(c, at=None, label='fecha a janela'):
    c.press('Escape', at=at, label=label)
    c.wait(0.4)
    c.ev(FECHAR_EVAL, label='Fechar (se o Esc não fechou)')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)


def js_cor(sel, cor):
    """<input type=color>: o valor entra pelo setter nativo + evento input (o onChange do React), como se escolhido no seletor"""
    return ("(()=>{const i=document.querySelector(%s);if(!i)return 'SEM ALVO';const set=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set;"
            "set.call(i,%s);i.dispatchEvent(new Event('input',{bubbles:true}));i.dispatchEvent(new Event('change',{bubbles:true}));return i.value})()") % (
        json.dumps(sel), json.dumps(cor))


JS_COLAR = ("(()=>{const e=document.activeElement;if(!e||!/^(INPUT|TEXTAREA)$/.test(e.tagName))return 'SEM FOCO';"
            "document.execCommand('insertText',false,%s);return e.value})()")


def colar(texto):
    """texto longo e sem graça visual: entra de uma vez no campo focado (insertText, o React ouve o input)"""
    return JS_COLAR % json.dumps(texto)


ACHA_ROLAGEM = ("const rolagem=(el)=>{let c=el&&el.parentElement;while(c&&c!==document.body){const s=getComputedStyle(c);"
                "if(/(auto|scroll)/.test(s.overflowY)&&c.scrollHeight>c.clientHeight+4)return c;c=c.parentElement;}"
                "return document.scrollingElement};")


def js_rola_ate(esc, texto, y=200, dur_ms=700, prefixo=True):
    """rolagem suave do contêiner que rola o alvo (folha do DOM, dentro de `esc`, cujo texto começa com `texto`) até ele ficar em y px
    CSS; o cursor não se mexe. Devolve o topo final, 'ok', 'SEM ALVO' ou 'SEM ROLAGEM'."""
    cmp = 'startsWith' if prefixo else '=='
    busca = (f"[...document.querySelectorAll({json.dumps(esc + ' *')})].filter(e=>e.textContent.trim().startsWith({json.dumps(texto)}))"
             ".sort((a,b)=>a.textContent.length-b.textContent.length)[0]") if prefixo else \
            f"[...document.querySelectorAll({json.dumps(esc + ' *')})].find(e=>e.children.length===0&&e.textContent.trim()==={json.dumps(texto)})"
    del cmp
    return ("(async()=>{" + ACHA_ROLAGEM + "const el=" + busca + ";if(!el)return 'SEM ALVO';const c=rolagem(el);if(!c)return 'SEM ROLAGEM';"
            f"const dy=Math.round(el.getBoundingClientRect().top-{int(y)});if(Math.abs(dy)<3)return 'ok';const y0=c.scrollTop,t0=performance.now();"
            "await new Promise(res=>{const f=t=>{const p=Math.min(1,(t-t0)/" + str(int(dur_ms)) + "),e=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;"
            "c.scrollTop=y0+dy*e;p<1?requestAnimationFrame(f):res()};requestAnimationFrame(f)});"
            "return Math.round(el.getBoundingClientRect().top)})()")


def rola_ate(c, esc, texto, at, label, y=200, dur_ms=700, prefixo=True):
    return c.ev(js_rola_ate(esc, texto, y, dur_ms, prefixo), at=at, label=label)


def menu_linha(c, nome, item, at=None, label=None, rola=True):
    """menu "Ações de <nome>" da linha (HoverDropdownMenu: abre ao passar o mouse; clicar no gatilho fecharia o menu). Antes, a lista
    rola (eval, sem cursor) até a linha ficar no meio: com a linha na borda de baixo da lista o robô rolava a lista ao ir ao item,
    o menu fechava e o clique não achava o item (cap03, 11/11)."""
    if rola:
        rola_ate(c, 'main [role=list]', nome, round(max(0.0, at - 0.6), 2) if at is not None else None, f'a lista mostra {nome} no meio',
                 y=430, dur_ms=400, prefixo=False)
    c.hover(ACOES(nome), 0.5, at=at, label=label or f'menu ⋯ de {nome}', optional=False, timeout=8)
    c.hover(ACOES(nome), 0.4, label=f'menu ⋯ de {nome} de novo (só se não abriu)', unless=ITEM(item))
    return c.waitfor(target=ITEM(item), timeout=6)


def item_menu(c, nome, item, at=None, label=None):
    """clica no item do menu da linha: antes, um passar do mouse no "⋯" só se o item sumiu (o menu fecha 200 ms depois que o cursor
    sai), e o clique sem rolar (T14)"""
    c.hover(ACOES(nome), 0.2, label=f'menu ⋯ de {nome} (só se fechou)', unless=ITEM(item))
    return c.click(ITEM(item), at=at, label=label or item, noScroll=True)


def escolhe(c, combo, opcao, at_abre, at_opcao, label):
    """Select do Radix: o gatilho pede ponteiro de verdade; a opção pelo papel"""
    c.click(combo, at=at_abre, label=f'{label} (abre a lista)')
    c.waitfor(target=OPT(opcao), timeout=6)
    return c.click(OPT(opcao), at=at_opcao, label=label, noScroll=True)


def cap_novo(n, **kw):
    return Cap(n, **kw)


# ================================================================ capítulos
def cap00():
    """Abertura: Dashboard; o cursor vai ao menu lateral e abre Funcionários (RH); ilustração na L2; cartões do módulo e do Antes."""
    c = cap_novo(0, start=(760, 300), recolhe=False)
    c.mark(1)
    c.confere('main', ['Olá, Rafael'], 'Dashboard da Recicla Vale Metais')
    c.hover(LINK('Funcionários (RH)'), 0.4, at=c.A(1, 'colocar', 0.9), label='o cursor vai ao menu lateral')
    c.click(LINK('Funcionários (RH)'), at=c.A(1, 'equipe', 0.6), label='Funcionários (RH) (menu lateral)')
    c.waitfor(text=SUBTITULO, timeout=20)
    c.waitfor(target=LINHA('Rafael Nogueira'), timeout=20)
    c.confere('main', ['Funcionários (RH)', SUBTITULO, 'Equipe', 'Diego Morais', 'Edson Moura'], 'a tela Funcionários (RH) com a lista Equipe')
    c.hover(SEL("main [role=list]"), 1.2, at=c.A(1, 'ganha,', 0.7), label='a lista Equipe')
    c.mark(2)
    c.cursor((900, 140), at=c.A(2, 'Num', 0.3), label='cursor descansa (ilustração do caderninho)')
    c.mark(3)
    c.hover(LINK('Funcionários (RH)'), 2.0, at=c.A(3, 'Funcionários', 0.7), label='Funcionários (RH): módulo do plano (cartão discreto)')
    c.mark(4)
    c.cursor((900, 140), at=c.A(4, 'Os', 0.3), label='cursor sai do menu (cartão Antes)')
    c.hover(ABA('Funcionários'), 0.8, at=c.A(4, 'Vamos', 0.6), label='as abas do topo')
    c.fim()
    return c


def cap01():
    """A tela e suas abas: as abas (sem clicar), Ativos/Inativos e os botões, a lista com o saldo, a ficha do Diego e o Dashboard."""
    c = cap_novo(1, setup=RH)
    c.mark(1)
    c.hover(ABA('Funcionários'), 1.6, at=c.A(1, 'abas.', 0.75), label='aba Funcionários (cadastro e dinheiro)')
    c.hover(ABA('Registro de Ponto'), 0.2, at=c.A(1, 'Registro', 0.75), label='aba Registro de Ponto')
    c.hover(ABA('Folha de Ponto'), 0.2, at=c.A(1, 'Folha', 0.75), label='aba Folha de Ponto')
    c.hover(ABA('Ausências'), 0.2, at=c.A(1, 'Ausências', 0.75), label='aba Ausências')
    c.hover(ABA('Configurações de Ponto'), 0.6, at=c.A(1, 'Configurações', 0.75), label='aba Configurações de Ponto')
    c.mark(2)
    c.hover(ABA('Folha de Ponto'), 1.0, at=c.A(2, 'quatro', 0.75), label='as quatro abas do ponto (Gerenciar Ponto Eletrônico)')
    c.mark(3)
    c.hover(ABA('Configurações de RH'), 0.4, at=c.A(3, 'Configurações', 0.75), label='aba Configurações de RH')
    c.hover(ABA('Dashboard'), 0.3, at=c.A(3, 'Dashboard.', 0.75), label='aba Dashboard')
    c.hover(SEL("main button:text-is('Ativos')"), 0.3, at=c.A(3, 'Ativos,', 0.75), label='Ativos / Inativos')
    c.hover(SEL("main button:has-text('Gerenciar departamentos')"), 0.1, at=c.A(3, 'departamentos,', 0.75), label='Gerenciar departamentos')
    c.hover(SEL("main button:has-text('Exportar Relatório')"), 0.1, at=c.A(3, 'relatório', 0.75), label='Exportar Relatório')
    c.hover(SEL("main button:has-text('Novo Funcionário')"), 0.6, at=c.A(3, 'Novo', 0.75), label='Novo Funcionário')
    c.mark(4)
    c.hover(SEL("main [role=listitem] p:text-is('Cláudio Ferraz')"), 0.4, at=c.A(4, 'cargo', 0.75), label='nome e cargo na lista Equipe')
    c.marcar(SALDO_LINHA('Cláudio Ferraz', 'R$ 2.100,00'), at=c.A(4, 'saldo:', 0.3), label='o saldo na lista Equipe (selo verde)')
    c.hover({'placeholder': 'Buscar por nome ou cargo...'}, 0.8, at=c.A(4, 'buscar', 0.75), label='busca Buscar por nome ou cargo...')
    c.mark(5)
    c.click(LINHA('Diego Morais'), at=c.A(5, 'Diego,', 0.8), label='Diego Morais (abre a ficha)')
    c.waitfor(target=SEL(f"{FICHA} h3:text-is('Resumo financeiro')"), timeout=10)
    c.confere(FICHA, ['Diego Morais', 'Ativo', 'Movimentações', 'Resumo financeiro', 'Dados profissionais'], 'a ficha do Diego')
    c.hover(BOTAO_FICHA('Vale'), 0.2, at=c.A(5, 'vale,', 0.75), label='botões de Movimentações (Vale)')
    c.hover(BOTAO_FICHA('Pagamento'), 0.2, at=c.A(5, 'pagamento,', 0.75), label='botão Pagamento')
    c.hover(RESUMO('Saldo atual'), 0.3, at=c.A(5, 'resumo', 0.75), label='Resumo financeiro')
    c.hover(SEL(f"{FICHA} h3:text-is('Dados profissionais')"), 0.6, at=c.A(5, 'dados', 0.75), label='Dados profissionais')
    c.mark(6)
    c.click(ABA('Dashboard'), at=c.A(6, 'Dashboard', 0.8), label='aba Dashboard')
    c.waitfor(text='Saldo Total a Pagar', timeout=10)
    c.confere('main', ['Funcionários Ativos', 'Folha de Pagamento', 'Média Salarial', 'Saldo Total a Pagar'], 'os cartões do Dashboard')
    c.hover(TXTX('Funcionários Ativos', within='main'), 0.3, at=c.A(6, 'ativos,', 0.75), label='Funcionários Ativos')
    c.hover(TXTX('Folha de Pagamento', within='main'), 0.3, at=c.A(6, 'salários', 0.75), label='Folha de Pagamento')
    c.hover(TXTX('Saldo Total a Pagar', within='main'), 0.4, at=c.A(6, 'saldo', 0.75), label='Saldo Total a Pagar')
    c.click(ABA('Funcionários'), label='volta para Funcionários')
    c.fim()
    return c


def cap02():
    """Cadastrar o Gabriel: Dados, Remuneração, a calculadora do custo (Lucro Real, EPI 600/ano -> R$ 4.264,00), a chave Pix e Cadastrar."""
    c = cap_novo(2, setup=RH)
    c.mark(1)
    c.click(SEL("main button:has-text('Novo Funcionário')"), at=c.A(1, 'Novo', 0.9), label='Novo Funcionário')
    c.waitfor(target=CAMPO('name'), timeout=10)
    c.hover(DTAB('Dados'), 0.6, at=c.A(1, 'Dados.', 0.9), label='janela Novo Funcionário, aba Dados')
    c.mark(2)
    t_nome = c.W(2, 'nome,')
    c.click(CAMPO('name'), at=round(c.L(2) - 1.2, 2), label='campo Nome *')
    c.type(CAMPO('name'), 'Gabriel Rocha', at=round(t_nome - 0.3, 2), label='Nome: Gabriel Rocha', cps=40, noClick=True)
    c.click(CAMPO('cpf'), at=round(max(c.W(2, 'CPF') - 0.9, t_nome + 1.0), 2), label='campo CPF')
    t_cpf = max(c.W(2, 'CPF') - 0.05, t_nome + 1.8)
    c.type(CAMPO('cpf'), '41827395664', at=round(t_cpf, 2), label='CPF 418.273.956-64', cps=40, noClick=True)
    c.click(CAMPO('phone'), at=round(max(c.W(2, 'sai') - 0.9, t_cpf + 1.2), 2), label='campo Telefone (sai do CPF: o CPF é conferido)')
    c.type(CAMPO('phone'), '12900004107', at=round(max(c.W(2, 'sai') - 0.05, t_cpf + 2.0), 2), label='Telefone (12) 90000-4107', cps=40, noClick=True)
    c.confere_campos(['Gabriel Rocha', '418.273.956-64', '(12) 90000-4107'], 'nome, CPF e telefone com máscara')
    c.mark(3)
    rola_ate(c, DLG, 'Cargo', round(c.L(3) - 0.9, 2), 'rola a janela até Cargo', y=300, dur_ms=500)
    c.click(CAMPO('position'), at=c.A(3, 'cargo', 0.9), label='campo Cargo')
    c.ev(colar('Operador de empilhadeira'), at=c.A(3, 'operador', 0.05), label='Cargo: Operador de empilhadeira')
    escolhe(c, CAMPO('department'), 'Pátio', c.A(3, 'departamento', 0.9), c.A(3, 'Pátio,', 0.6), 'Departamento: Pátio')
    c.digita(CAMPO('hire_date'), '10112026', c.W(3, 'hoje,'), 'Data de Admissão 10/11/2026')
    c.confere_campos(['2026-11-10'], 'admissão hoje')
    c.mark(4)
    c.click(DTAB('Remuneração'), at=c.A(4, 'Remuneração', 0.9), label='aba Remuneração')
    c.digita(CAMPO('salary'), '2520,00', c.W(4, 'salário:'), 'Salário R$ 2.520,00')
    c.mark(5)
    c.cursor((900, 140), at=c.A(5, 'E', 0.3), label='cursor descansa (ilustração do iceberg)')
    c.mark(6)
    c.click(BDLG('Calcular'), at=c.A(6, 'Calcular', 0.9), label='Calcular (custo mensal)')
    c.waitfor(text='Composição do custo mensal', timeout=10)
    c.confere('dlg', ['Calcular custo mensal', 'Lucro Real / Presumido', 'R$ 2.520,00'], 'calculadora em Lucro Real com o salário')
    c.hover(SEL(f"{CALC} button:has-text('Lucro Real')"), 1.0, at=c.A(6, 'Lucro', 0.75), label='Regime tributário: Lucro Real / Presumido')
    c.mark(7)
    EPI = SEL(f"{CALC} div.space-y-1:has(> label:text-is('EPI e uniformes')) input")
    c.ev(js_rola_ate(DLG, 'Custos anuais', 140, 600), at=c.A(7, 'Coloco', 0.4), label='rola até Custos anuais')
    c.digita(EPI, '600,00', c.W(7, 'seiscentos'), 'EPI e uniformes: 600,00 por ano')
    c.confere('dlg', ['Mensal: R$ 50,00'], 'EPI 600,00 por ano = 50,00 por mês')
    c.ev(js_rola_ate(DLG, 'Custo total mensal', 520, 800), at=c.A(7, 'calculadora', 0.3), label='rola até o resumo do custo')
    c.hover(TXTX('FGTS (8%)', within=CALC), 0.2, at=c.A(7, 'fundo', 0.75), label='+ FGTS (8%)')
    c.hover(TXTX('13º (provisão)', within=CALC), 0.2, at=c.A(7, 'décimo', 0.75), label='+ 13º (provisão)')
    c.hover(TXTX('Férias + 1/3 (provisão)', within=CALC), 0.2, at=c.A(7, 'férias,', 0.75), label='+ Férias + 1/3 (provisão)')
    c.hover(TXTX('INSS patronal (28', within=CALC), 0.3, at=c.A(7, 'INSS', 0.75), label='+ INSS patronal (28,8%)')
    c.hover(TXT('Custo total mensal', within=CALC), 1.2, at=c.A(7, 'Custo', 0.75), label='Custo total mensal R$ 4.264,00')
    c.confere('dlg', ['R$ 4.264,00'], 'Custo total mensal R$ 4.264,00')
    c.mark(8)
    c.hover(TXTX('Valores estimados com base', within=CALC), 1.0, at=c.A(8, 'estimados,', 0.75), label='rodapé Valores estimados (contador)')
    c.click(SEL(f"{CALC} button:has-text('Aplicar R$')"), at=c.A(8, 'Aplicar,', 0.9), label='Aplicar R$ 4.264,00')
    c.waitfor(gone={'text': 'Composição do custo mensal'}, timeout=8)
    c.hover(CAMPO('monthly_cost'), 0.8, at=c.A(8, 'cadastro,', 0.75), label='Custo mensal total R$ 4.264,00 no cadastro')
    c.confere_campos(['R$ 4.264,00'], 'custo aplicado no cadastro')
    c.mark(9)
    c.digita(CAMPO('pix_key'), '(12) 90000-4107', c.W(9, 'Pix,'), 'Chave PIX (12) 90000-4107')
    c.click(BDLG('Cadastrar'), at=c.A(9, 'Cadastrar.', 0.9), label='Cadastrar')
    c.waitfor(gone={'role': 'dialog'}, timeout=12)
    c.waitfor(target=LINHA('Gabriel Rocha'), timeout=10)
    # o cursor NÃO entra na lista: no caminho até a linha ele passava no "⋯" (menu que abre ao passar o mouse) e o menu cobria a lista
    rola_ate(c, 'main [role=list]', 'Gabriel Rocha', c.A(9, 'Pronto,', 0.3), 'a lista mostra o Gabriel no meio', y=470, dur_ms=500, prefixo=False)
    c.marcar(LINHA('Gabriel Rocha'), at=c.A(9, 'lista.', 0.3), label='o Gabriel na lista Equipe')
    c.mark(10)
    c.confere('main [role=list]', ['Gabriel Rocha', 'R$ 2.520,00'], 'saldo do Gabriel = salário')
    c.marcar(SALDO_LINHA('Gabriel Rocha', 'R$ 2.520,00'), at=c.A(10, 'saldo', 0.3), label='selo de saldo do Gabriel R$ 2.520,00')
    c.fim()
    return c


def cap03():
    """Campos de folha: Editar o Gabriel, CLT, 1 dependente, vale-transporte R$ 220,00, Atualizar; ilustração Informal x CLT."""
    c = cap_novo(3, setup=RH)
    c.mark(1)
    menu_linha(c, 'Gabriel Rocha', 'Editar', at=c.A(1, 'editando', 1.0), label='menu ⋯ do Gabriel')
    item_menu(c, 'Gabriel Rocha', 'Editar', at=c.A(1, 'cadastro,', 0.6), label='Editar')
    c.waitfor(target=CAMPO('name'), timeout=10)
    c.click(DTAB('Remuneração'), at=c.A(1, 'Regime', 1.2), label='aba Remuneração')
    c.click(BDLG('CLT'), at=c.A(1, 'CLT.', 0.8), label='Regime de contratação: CLT')
    c.waitfor(target=CAMPO('dependents'), timeout=6)
    c.mark(2)
    c.hover(SEL(f"{DLG} label:text-is('Nº de dependentes (IRRF)')"), 0.4, at=c.A(2, 'Aparecem', 0.5), label='campos de folha do CLT')
    c.digita(CAMPO('dependents'), '1', c.W(2, 'coloco'), 'Nº de dependentes (IRRF): 1', clear=True)
    c.mark(3)
    c.click(CAMPO('vt-enabled'), at=c.A(3, 'ligo', 0.8), label='Desconta vale-transporte (até 6%)')
    c.waitfor(target=CAMPO('vt-value'), timeout=6)
    c.digita(CAMPO('vt-value'), '220,00', c.W(3, 'duzentos'), 'Valor mensal do VT R$ 220,00')
    c.hover(SEL(f"{DLG} label:text-is('Desconta vale-transporte (até 6%)')"), 1.2, at=c.A(3, 'seis', 0.75), label='até 6% do salário')
    c.confere_campos(['1', 'R$ 220,00'], 'dependente e VT')
    c.confere('dlg', ['Desconta vale-transporte (até 6%)'], 'até 6% do salário')
    c.mark(4)
    c.click(BDLG('Atualizar'), at=c.A(4, 'Atualizar,', 0.9), label='Atualizar')
    c.waitfor(gone={'role': 'dialog'}, timeout=12)
    c.mark(5)
    c.cursor((900, 140), at=c.A(5, 'Esses', 0.3), label='cursor descansa (ilustração Informal x CLT)')
    c.fim()
    return c


def cap04():
    """Departamentos: cria Transporte (laranja, caminhão); Edson no Transporte; os Filtros da lista."""
    c = cap_novo(4, setup=RH)
    c.mark(1)
    c.click(SEL("main button:has-text('Gerenciar departamentos')"), at=c.A(1, 'departamentos.', 0.9), label='Gerenciar departamentos')
    c.waitfor(text='Organize seus funcionários em departamentos por cor e ícone.', timeout=10)
    c.hover(TXT('Escritório', within=DLG), 0.3, at=c.A(1, 'Escritório', 0.75), label='Escritório (azul, maleta)')
    c.hover(TXT('Pátio', within=DLG), 0.4, at=c.A(1, 'Pátio.', 0.75), label='Pátio (verde, chave)')
    c.mark(2)
    NOME = SEL(f"{DLG} input[placeholder='Ex: Produção, Administrativo, Pátio']")
    c.digita(NOME, 'Transporte', c.W(2, 'Transporte,'), 'Nome: Transporte')
    COR = f"{DLG} input[type=color]"
    c.hover(SEL(COR), 0.2, at=c.A(2, 'cor,', 0.75), label='Cor')
    c.ev(js_cor(COR, '#ea580c'), at=c.A(2, 'laranja,', 0.1), label='Cor: laranja #EA580C')
    c.click(SEL(f"{DLG} div.space-y-2:has(> label:text-is('Ícone')) button"), at=c.A(2, 'ícone', 0.9), label='Ícone (abre a grade)')
    c.click(SEL(f"{POP} button:has(svg.lucide-truck)"), at=c.A(2, 'caminhão.', 0.6), label='ícone do caminhão', noScroll=True)
    c.mark(3)
    c.click(BDLG('Adicionar'), at=c.A(3, 'Adicionar,', 0.9), label='Adicionar')
    c.waitfor(target=TXT('Transporte', within=DLG), timeout=8)
    c.hover(TXT('Transporte', within=DLG), 0.5, at=c.A(3, 'lista.', 0.75), label='Transporte na lista de departamentos')
    fechar_janela(c)
    c.mark(4)
    menu_linha(c, 'Edson Moura', 'Editar', at=c.A(4, 'Edson,', 1.0), label='menu ⋯ do Edson')
    item_menu(c, 'Edson Moura', 'Editar', at=c.A(4, 'motorista,', 0.6), label='Editar o Edson')
    c.waitfor(target=CAMPO('department'), timeout=10)
    escolhe(c, CAMPO('department'), 'Transporte', c.A(4, 'Departamento,', 0.9), c.A(4, 'Transporte', 0.6), 'Departamento: Transporte')
    c.click(BDLG('Atualizar'), at=c.A(4, 'atualizo.', 0.9), label='Atualizar')
    c.waitfor(gone={'role': 'dialog'}, timeout=12)
    c.waitfor(target=SEL("main [role=listitem]:has(p:text-is('Edson Moura')) span:has-text('Transporte')"), timeout=10)
    c.hover(SEL("main [role=listitem]:has(p:text-is('Edson Moura')) span:has-text('Transporte')"), 1.0, at=c.A(4, 'cor', 0.75),
            label='o Edson com o caminhão laranja e Transporte')
    c.mark(5)
    c.click(SEL("main button[aria-label^='Filtros']"), at=c.A(5, 'Filtros', 0.9), label='Filtros da lista')
    c.waitfor(target=SEL(f"{POP} button[role=combobox]"), timeout=6)
    c.click(SEL(f"{POP} button[role=combobox]"), at=c.A(5, 'departamento', 0.9), label='Departamento (a lista dos departamentos)', noScroll=True)
    c.waitfor(target=OPT('Transporte'), timeout=6)
    c.hover(OPT('Transporte'), 0.8, label='os departamentos no filtro', noScroll=True)
    c.press('Escape', label='fecha a lista sem filtrar')
    c.pause(0.4)
    c.press('Escape', label='fecha os Filtros')
    c.fim()
    return c


def cap05():
    """Vale de R$ 200,00 e falta de R$ 90,00 do Diego (saldo 1.690,00); bônus de R$ 150,00 do Cláudio (2.250,00)."""
    c = cap_novo(5, setup=RH)
    c.mark(1)
    c.click(LINHA('Diego Morais'), at=c.A(1, 'Diego', 0.8), label='Diego Morais')
    c.waitfor(target=RESUMO('Saldo atual'), timeout=10)
    c.confere(FICHA, ['Salário', 'R$ 1.980,00', 'Saldo atual'], 'Diego com saldo 1.980,00')
    c.hover(RESUMO('Saldo atual'), 1.2, at=c.A(1, 'saldo', 0.75), label='Resumo financeiro: Salário e Saldo atual R$ 1.980,00')
    c.mark(2)
    c.click(BOTAO_FICHA('Vale'), at=c.A(2, 'Vale,', 0.9, nth=1), label='Vale')
    c.waitfor(target=CAMPO('amount'), timeout=10)
    c.hover(SEL(f"{DLG} label[for='vale-dinheiro']"), 0.4, at=c.A(2, 'Dinheiro,', 0.9), label='Origem do Pagamento: Dinheiro (Caixa)')
    c.digita(CAMPO('amount'), '200,00', c.W(2, 'valor'), 'Valor R$ 200,00')
    c.digita(CAMPO('description'), 'Adiantamento', c.W(2, 'descrição.'), 'Descrição: Adiantamento')
    c.mark(3)
    c.click(BDLG('Confirmar'), at=c.A(3, 'Confirmar.', 0.9), label='Confirmar o vale')
    c.waitfor(gone={'role': 'dialog'}, timeout=12)
    c.confere(FICHA, ['R$ 1.780,00'], 'saldo do Diego 1.780,00')
    c.hover(RESUMO('Saldo atual'), 0.8, at=c.A(3, 'saldo', 0.75), label='Saldo atual R$ 1.780,00')
    c.mark(4)
    c.hover(RESUMO('Vales'), 2.0, at=c.A(4, 'vale', 0.75), label='Vales R$ 200,00 (dica: não lançar de novo no banco)')
    c.mark(5)
    c.click(BOTAO_FICHA('Falta'), at=c.A(5, 'Falta,', 0.9), label='Falta')
    c.waitfor(target=CAMPO('amount'), timeout=10)
    c.digita(CAMPO('amount'), '90,00', c.W(5, 'noventa'), 'Valor R$ 90,00', folga_clique=1.2)
    c.click(CAMPO('description'), at=c.A(5, 'reais.', 0.4), label='campo Descrição')
    c.ev(colar('Faltou sexta, 06/11, sem avisar'), label='Descrição: Faltou sexta, 06/11, sem avisar')
    c.click(BDLG('Confirmar'), label='Confirmar a falta')
    c.waitfor(gone={'role': 'dialog'}, timeout=12)
    c.mark(6)
    c.confere(FICHA, ['R$ 1.690,00', 'R$ 200,00', 'R$ 90,00'], 'saldo 1.690,00, vales 200,00, faltas 90,00')
    c.hover(RESUMO('Salário'), 0.3, at=c.A(6, 'salário,', 0.75), label='Salário R$ 1.980,00')
    c.hover(RESUMO('Vales'), 0.3, at=c.A(6, 'vale,', 0.75), label='Vales R$ 200,00')
    c.hover(RESUMO('Faltas'), 0.3, at=c.A(6, 'falta.', 0.75), label='Faltas R$ 90,00')
    c.hover(RESUMO('Saldo atual'), 1.2, at=c.A(6, 'Saldo:', 0.75), label='Saldo atual R$ 1.690,00')
    c.mark(7)
    c.cursor((900, 140), at=c.A(7, 'Uma', 0.3), label='cursor descansa (ilustração da conta do saldo)')
    c.mark(8)
    c.click(LINHA('Cláudio Ferraz'), at=c.A(8, 'Cláudio,', 0.8), label='Cláudio Ferraz')
    c.waitfor(target=SEL(f"{FICHA} h2:text-is('Cláudio Ferraz')"), timeout=10)
    c.click(BOTAO_FICHA('Bônus'), at=c.A(8, 'meta', 0.9), label='Bônus')
    c.waitfor(target=CAMPO('amount'), timeout=10)
    c.digita(CAMPO('amount'), '150,00', c.W(8, 'cento'), 'Valor R$ 150,00', folga_clique=1.2)
    c.click(CAMPO('description'), at=c.A(8, 'reais.', 0.5), label='campo Descrição')
    c.ev(colar('Meta de prensagem de outubro'), label='Descrição: Meta de prensagem de outubro')
    c.click(BDLG('Confirmar'), label='Confirmar o bônus')
    c.waitfor(gone={'role': 'dialog'}, timeout=12)
    c.confere(FICHA, ['R$ 2.250,00'], 'saldo do Cláudio 2.250,00')
    c.hover(RESUMO('Saldo atual'), 1.0, at=c.A(8, 'dois', 0.75), label='Saldo atual R$ 2.250,00')
    c.fim()
    return c


def cap06():
    """Edson: Recebimento de R$ 100,00 (vales 500 -> 400) e Pagamento de R$ 2.750,00 por Pix (CLT de relance); saldo volta a 2.900,00."""
    c = cap_novo(6, setup=RH)
    c.mark(1)
    c.click(LINHA('Edson Moura'), at=c.A(1, 'Edson', 0.8), label='Edson Moura')
    c.waitfor(target=RESUMO('Saldo atual'), timeout=10)
    c.confere(FICHA, ['R$ 2.900,00', 'R$ 2.650,00', 'R$ 500,00', 'R$ 250,00'], 'Edson: salário 2.900, saldo 2.650, vales 500, bônus 250')
    c.hover(RESUMO('Saldo atual'), 0.4, at=c.A(1, 'recebe', 0.75), label='Resumo financeiro do Edson')
    c.hover(RESUMO('Vales'), 0.4, at=c.A(1, 'quinhentos', 0.75), label='Vales R$ 500,00')
    c.hover(RESUMO('Bônus'), 0.6, at=c.A(1, 'duzentos', 0.75), label='Bônus R$ 250,00')
    c.mark(2)
    c.click(BOTAO_FICHA('Recebimento'), at=c.A(2, 'Antes,', 0.5), label='Recebimento')
    c.waitfor(text='Registrar devolução de valor pelo funcionário', timeout=10)
    VR = SEL(f"{DLG} input[placeholder='0,00']")
    c.digita(VR, '100,00', c.W(2, 'cem'), 'Valor a receber 100,00 (Máximo: R$ 500,00)', folga_clique=1.3)
    c.hover(SEL(f"{DLG} label[for='recv-cash']"), 0.3, at=c.A(2, 'caixa', 0.75), label='Forma de Recebimento: Dinheiro (entra no caixa)')
    c.click(SEL(f"{DLG} textarea, {DLG} input[placeholder='Informações adicionais...']"), at=c.A(2, 'abate', 0.6), label='campo Observações')
    c.ev(colar('Sobra do vale da viagem'), label='Observações: Sobra do vale da viagem')
    c.mark(3)
    c.click(BDLG('Confirmar Recebimento'), at=c.A(3, 'Confirmado:', 0.9), label='Confirmar Recebimento')
    c.waitfor(text='Recebimento confirmado!', timeout=10)
    c.confere('dlg', ['Vales antes', 'R$ 500,00', 'Abatido', 'Vales restantes', 'R$ 400,00'], 'vales 500 -> 400')
    c.hover(TXT('Vales restantes', within=DLG), 0.6, at=c.A(3, 'quatrocentos.', 0.75), label='Vales restantes R$ 400,00')
    c.click(BDLG('Fechar'), label='Fechar')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.mark(4)
    c.click(BOTAO_FICHA('Pagamento'), at=c.A(4, 'Pagamento.', 0.9), label='Pagamento')
    c.waitfor(text='Pagamento ao funcionário', timeout=10)
    c.confere('body', ['Salário:', 'R$ 2.900,00', 'Total de Bônus:', 'R$ 250,00', 'Descontos:', 'R$ 400,00'], 'resumo do pagamento')
    c.confere_campos(['400,00', '2.750,00'], 'vales a descontar 400,00 e valor 2.750,00')
    c.hover(TXT('Salário:'), 0.2, at=c.A(4, 'salário,', 0.75), label='Resumo: Salário')
    c.hover(TXT('Total de Bônus:'), 0.2, at=c.A(4, 'bônus', 0.75), label='Resumo: Total de Bônus')
    c.hover(TXT('Descontos:'), 0.5, at=c.A(4, 'descontos.', 0.75), label='Resumo: Descontos (vales)')
    c.mark(5)
    c.hover(TXTX('Quanto você quer descontar dos vales', within=DLG), 1.0, at=c.A(5, 'quanto', 0.75), label='Quanto você quer descontar dos vales (400,00)')
    c.hover(TXTX('Valor padrão: 100% dos vales', within=DLG), 1.2, at=c.A(5, 'padrão', 0.75), label='Valor padrão: 100% dos vales (R$ 400,00)')
    c.mark(6)
    c.click(BDLG('CLT (com folha)'), at=c.A(6, 'CLT,', 0.9), label='Modo de pagamento: CLT (com folha)')
    c.waitfor(text='Valores estimados; confirme com seu contador.', timeout=6)
    c.hover(TXTX('- INSS'), 0.3, at=c.A(6, 'INSS', 0.75), label='CLT: - INSS e - IRRF (estimados)')
    c.hover(TXTX('Líquido'), 0.3, at=c.A(6, 'líquido.', 0.75), label='CLT: Líquido')
    c.hover(TXT('Valores estimados; confirme com seu contador.'), 1.2, at=c.A(6, 'estimados,', 0.75), label='Valores estimados; confirme com seu contador.')
    c.click(BDLG('Normal'), at=c.A(6, 'Normal.', 0.9), label='Modo de pagamento: Normal')
    c.mark(7)
    c.hover(TXTX('Valor efetivamente pago', within=DLG), 1.0, at=c.A(7, 'valor', 0.75), label='Valor efetivamente pago R$ 2.750,00')
    c.confere('dlg', ['Calculado: R$ 2.750,00'], 'Calculado: R$ 2.750,00')
    c.hover(TXTX('Calculado: R$', within=DLG), 1.0, at=c.A(7, 'salário,', 0.75), label='Calculado: R$ 2.750,00')
    c.mark(8)
    rola_ate(c, DLG, 'Forma de Pagamento', c.A(8, 'Ele', 0.4), 'rola até a Forma de Pagamento', y=260, dur_ms=500)
    c.click(SEL(f"{DLG} label[for='payment-pix']"), at=c.A(8, 'Pix,', 0.9), label='Forma de Pagamento: PIX/Transferência')
    c.hover(SEL(f"{DLG} label:has-text('Conta')"), 0.3, at=c.A(8, 'conta', 0.75), label='Conta bancária: Conta Principal')
    c.click(BDLG('Confirmar Pagamento'), at=c.A(8, 'Confirmar', 0.9), label='Confirmar Pagamento')
    c.waitfor(gone={'role': 'dialog'}, timeout=15)
    c.mark(9)
    c.confere(FICHA, ['R$ 2.900,00'], 'saldo do Edson volta a 2.900,00')
    c.hover(RESUMO('Saldo atual'), 1.0, at=c.A(9, 'saldo:', 0.75), label='Saldo atual R$ 2.900,00')
    c.hover(DADO('Último pagamento'), 0.8, at=c.A(9, 'salário', 0.75), label='Último pagamento: hoje')
    c.mark(10)
    c.cursor((900, 140), at=c.A(10, 'O', 0.3), label='cursor descansa (ilustração do ciclo do pagamento)')
    c.fim()
    return c


def cap07():
    """O extrato do Edson: cartões do mês, o pagamento detalhado com Gerar Recibo, o ajuste, o recebimento, os vales, o bônus e o ajuste de
    salário; a lixeira de um vale (sem clicar); Fechar."""
    setup = RH + [{'do': 'click', 'target': LINHA('Edson Moura')}, {'do': 'waitFor', 'target': RESUMO('Saldo atual'), 'timeout': 10}, {'do': 'wait', 'seconds': 0.6}]
    c = cap_novo(7, setup=setup)
    c.mark(1)
    c.click(SEL(f"{FICHA} button:has-text('Extrato')"), at=c.A(1, 'Extrato.', 0.9), label='Extrato')
    c.waitfor(text='Extrato - Edson Moura', timeout=10)
    c.confere('dlg', ['Bônus', 'Vales', 'Faltas', 'Saldo', 'R$ 2.900,00'], 'cartões do mês novo')
    c.hover(TXT('Vales', within=DLG), 0.2, at=c.A(1, 'vale,', 0.75), label='cartão Vales R$ 0,00')
    c.hover(TXT('Bônus', within=DLG), 0.2, at=c.A(1, 'bônus,', 0.75), label='cartão Bônus R$ 0,00')
    c.hover(TXT('Saldo', within=DLG), 0.5, at=c.A(1, 'saldo', 0.75), label='cartão Saldo R$ 2.900,00')
    c.mark(2)
    c.hover(TXTX('Valor pago', within=DLG), 0.8, at=c.A(2, 'conta', 0.75), label='Valor pago R$ 2.750,00 (pagamento detalhado)')
    c.hover(SEL(f"{DLG} button:has-text('Gerar Recibo')"), 0.6, at=c.A(2, 'Gerar', 0.75), label='Gerar Recibo')
    c.hover(TXTX('Reset para salário base', within=DLG), 0.8, at=c.A(2, 'ajuste', 0.75), label='Ajuste: Reset para salário base')
    c.mark(3)
    c.ev(js_rola_ate(DLG, 'Recebimento do funcionário', 220, 800), at=c.A(3, 'baixo,', 0.4), label='rola a lista do extrato')
    c.hover(TXTX('Recebimento do funcionário', within=DLG), 0.3, at=c.A(3, 'recebimento', 0.75), label='Recebimento +R$ 100,00')
    c.hover(TXTX('Viagens extras', within=DLG), 0.3, at=c.A(3, 'bônus', 0.75), label='o bônus de outubro')
    c.ev(js_rola_ate(DLG, 'Ajuste de salário', 420, 600), at=c.A(3, 'repara', 0.5), label='rola até o ajuste de salário')
    c.confere('dlg', ['Ajuste de salário: R$ 2.800,00 → R$ 2.900,00', 'Recebimento do funcionário - Sobra do vale da viagem'], 'o ajuste de salário e o recebimento')
    c.hover(TXTX('Ajuste de salário', within=DLG), 2.0, at=c.A(3, 'Ajuste', 0.75), label='Ajuste de salário: R$ 2.800,00 → R$ 2.900,00')
    c.mark(4)
    c.hover(TXTX('Ajuste de salário', within=DLG), 3.0, at=c.A(4, 'sistema', 0.75), label='Ajuste de salário (continua)')
    c.mark(5)
    LIXO = SEL("xpath=//div[@role='dialog']//*[normalize-space(text())='Vale']/ancestor::div[.//button//*[contains(@class,'lucide-trash')]][1]"
               "//button[.//*[contains(@class,'lucide-trash')]]")
    c.hover(LIXO, 1.6, at=c.A(5, 'excluir', 0.75), label='lixeira de uma linha Vale (sem clicar)')
    c.mark(6)
    c.cursor((1000, 140), at=c.A(6, 'A', 0.3), label='cursor sai da lixeira (ilustração)')
    c.click(BDLG('Fechar'), at=round(c.dur - 1.4, 2), label='Fechar o extrato')
    c.fim()
    return c


def cap08():
    """Ponto: a aba Ponto eletrônico do Gabriel (ligado, PIN), Copiar link do ponto, Ativar ponto da Juliana e o Tablet da empresa."""
    c = cap_novo(8, setup=RH)
    c.mark(1)
    menu_linha(c, 'Gabriel Rocha', 'Editar', at=c.A(1, 'cadastro,', 1.2), label='menu ⋯ do Gabriel')
    item_menu(c, 'Gabriel Rocha', 'Editar', at=c.A(1, 'aba', 0.7), label='Editar')
    c.waitfor(target=CAMPO('name'), timeout=10)
    c.click(DTAB('Ponto eletrônico'), at=c.A(1, 'Ponto', 0.9, nth=1), label='aba Ponto eletrônico')
    c.waitfor(target=CAMPO('ponto-enabled'), timeout=6)
    c.confere('dlg', ['Ativar ponto eletrônico', 'Gera um link público pro funcionário bater ponto sem login.'], 'ponto ligado')
    c.hover(CAMPO('ponto-enabled'), 1.0, at=c.A(1, 'ligado.', 0.75), label='Ativar ponto eletrônico (ligado)')
    c.mark(2)
    c.hover(TXTX('Sem PIN. Qualquer um com o link', within=DLG), 1.2, at=c.A(2, 'link', 0.75), label='PIN do ponto (opcional): Sem PIN')
    c.hover(SEL(f"{DLG} button:has-text('Definir PIN')"), 1.4, at=c.A(2, 'PIN', 0.75), label='Definir PIN (sem clicar)')
    c.click(BDLG('Cancelar'), at=c.A(2, 'dele.', 0.4, nth=1), label='Cancelar')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.mark(3)
    menu_linha(c, 'Gabriel Rocha', 'Copiar link do ponto', at=c.A(3, 'menu', 0.9), label='menu ⋯ do Gabriel')
    item_menu(c, 'Gabriel Rocha', 'Copiar link do ponto', at=c.A(3, 'Copiar', 0.6), label='Copiar link do ponto')
    c.waitfor(text='Link copiado', timeout=6)
    c.mark(4)
    c.cursor((1000, 140), at=c.A(4, 'Aí', 0.3), label='cursor descansa (ilustração do link no celular)')
    c.mark(5)
    c.click(ABA('Configurações de Ponto'), at=c.A(5, 'Configurações', 0.9), label='aba Configurações de Ponto')
    c.waitfor(text='Jornada Padrão da Empresa', timeout=10)
    rola_ate(c, 'main', 'Marque quem vai bater ponto', c.A(5, 'Juliana,', 1.0), 'rola até o cartão Ativar ponto eletrônico', y=250)
    c.click(SEL("main div.cursor-pointer:has(p:text-is('Juliana Prado'))"), at=c.A(5, 'marco', 0.8), label='marca Juliana Prado')
    c.click(SEL("main button:has-text('Ativar ponto (1)')"), at=c.A(5, 'Ativar', 0.9), label='Ativar ponto (1)')
    c.waitfor(text='1 funcionário com ponto ativado', timeout=8)
    c.mark(6)
    rola_ate(c, 'main', 'Tablet da empresa', c.A(6, 'cima', 0.8), 'sobe até o cartão Tablet da empresa', y=150)
    c.hover(TXTX('/ponto/empresa/', within='main'), 1.2, at=c.A(6, 'tablet', 0.75), label='link do tablet /ponto/empresa/...')
    c.hover(SEL("main svg[role=img], main canvas, main img[alt*='QR']"), 1.0, at=c.A(6, 'lista', 0.75), label='QR Code do tablet')
    c.mark(7)
    c.cursor((1000, 140), at=c.A(7, 'Uma', 0.3), label='cursor descansa (ilustração dos dois links)')
    c.fim()
    return c


# câmera falsa do celular (cap09): getUserMedia devolve o vídeo de um canvas com um avatar ilustrado (nenhum rosto real), animado de leve
JS_CAMERA = r"""(()=>{const cv=document.createElement('canvas');cv.width=720;cv.height=720;const g=cv.getContext('2d');let t0=performance.now();
const pinta=()=>{const t=(performance.now()-t0)/1000;const W=720,cx=360+Math.sin(t*1.3)*4,cy=380+Math.sin(t*0.9)*3;
const gr=g.createLinearGradient(0,0,0,W);gr.addColorStop(0,'#c6d6de');gr.addColorStop(1,'#94a8b2');g.fillStyle=gr;g.fillRect(0,0,W,W);
g.fillStyle='#78808a';g.fillRect(0,W*0.72,W,W);g.fillStyle='#f27820';g.beginPath();g.ellipse(cx,W*0.98,W*0.36,W*0.3,0,0,Math.PI*2);g.fill();
g.fillStyle='#e6e6dc';g.fillRect(cx-W*0.30,W*0.86,W*0.6,W*0.03);g.fillStyle='#c69670';g.fillRect(cx-W*0.06,cy+W*0.16,W*0.12,W*0.14);
g.beginPath();g.ellipse(cx,cy,W*0.17,W*0.2,0,0,Math.PI*2);g.fill();g.fillStyle='#facc15';g.beginPath();g.ellipse(cx,cy-W*0.09,W*0.19,W*0.16,0,Math.PI,0);g.fill();
g.fillRect(cx-W*0.22,cy-W*0.1,W*0.44,W*0.03);g.fillStyle='#282830';for(const d of[-1,1]){g.beginPath();g.arc(cx+d*W*0.07,cy+W*0.02,9,0,Math.PI*2);g.fill();}
g.strokeStyle='#96463c';g.lineWidth=7;g.beginPath();g.arc(cx,cy+W*0.06,W*0.06,0.35,Math.PI-0.35);g.stroke();requestAnimationFrame(pinta)};pinta();
let st=null;window.__t19cam={chamadas:0,abortados:0};
const fake=async()=>{window.__t19cam.chamadas++;if(!st){st=cv.captureStream(24);st.getTracks().forEach(t=>{t.stop=()=>{}})}return st};
if(!navigator.mediaDevices)Object.defineProperty(navigator,'mediaDevices',{value:{}});
navigator.mediaDevices.getUserMedia=fake;navigator.mediaDevices.enumerateDevices=async()=>[{kind:'videoinput',deviceId:'cam-falsa',label:'Câmera frontal',groupId:'g'}];
const play0=HTMLMediaElement.prototype.play;HTMLMediaElement.prototype.play=function(){const nossa=st&&this.srcObject===st;const p=play0.call(this);
return nossa?p.catch(e=>{if(e&&e.name==='AbortError'){window.__t19cam.abortados++;return undefined}throw e}):p};
return 'camera falsa'})()"""
# A câmera do app reinicia a cada segundo: o PontoScreen re-renderiza com o relógio (setNow a cada 1 s) e passa onCapture sem
# useCallback, então o efeito do CenteredSelfieCapture (deps [captureFrame, copy, stopCamera]) para e reabre a câmera; um play()
# interrompido (AbortError) vira "Não foi possível abrir a câmera." (achado do app). A câmera falsa devolve sempre o mesmo stream,
# ignora o stop() e engole o AbortError do play() dela (uma câmera "instantânea"); window.__t19cam conta as reaberturas.


def js_botao(texto, sel='button'):
    return f"[...document.querySelectorAll({json.dumps(sel)})].filter(b=>b.textContent.trim().includes({json.dumps(texto)})&&b.getClientRects().length).pop()"


def cap09():
    """No celular do Gabriel (sem login): Registrar Entrada, localização, selfie (Tirar foto agora), confirmação e Confirmar registro."""
    setup = [{'do': 'geo', 'lat': -23.0105, 'lng': -45.5412},
             {'do': 'goto', 'url': f'/ponto/{GABRIEL_SLUG}'}, {'do': 'waitFor', 'text': 'Gabriel Rocha', 'timeout': 30},
             {'do': 'waitFor', 'text': 'Registrar Entrada', 'timeout': 20}, {'do': 'eval', 'js': JS_CAMERA}, {'do': 'wait', 'seconds': 0.8}]
    c = cap_novo(9, setup=setup, phone=True, start=(195, 600), pace=0.6, prewarm=[f'/ponto/{GABRIEL_SLUG}'])
    c.mark(1)
    c.confere('body', ['Gabriel Rocha', 'Operador de empilhadeira', 'Recicla Vale Metais', 'PONTO ELETRÔNICO'], 'tela do ponto do Gabriel')
    c.marcar(TXT('Gabriel Rocha'), at=c.A(1, 'nome', 0.3), label='nome do Gabriel e cargo (cabeçalho)')
    c.marcar(TXTX('Recicla Vale Metais'), at=c.A(1, 'empresa', 0.3), label='a empresa e a data')
    c.marcar(TXTX('Você ainda não bateu o ponto hoje'), at=c.A(1, 'relógio.', 0.3), label='o relógio do ponto (rodapé)')
    c.mark(2)
    c.click(SEL("button:has-text('Registrar Entrada')"), at=c.A(2, 'toca', 0.9), label='Registrar Entrada', noScroll=True)
    c.waitfor(text='Confirme localização e selfie para registrar o ponto', timeout=8)
    c.marcar(TXTX('Confirme localização e selfie'), at=c.A(2, 'localização.', 0.4), label='Obtendo sua localização...')
    c.waitfor(text='Tirar foto agora', timeout=15)
    if c.tem(3, 'selfie.'):   # a fala do roteiro (L3 "Depois vem a selfie ... Tirar foto agora")
        c.mark(3)
        c.marcar(SEL("video"), at=c.A(3, 'selfie.', 0.3), label='Selfie do ponto (câmera)')
        c.click(SEL("button:has-text('Tirar foto agora')"), at=c.A(3, 'Tirar', 0.9), label='Tirar foto agora', noScroll=True,
                when=SEL("button:has-text('Tirar foto agora')"))
        nc = 4
    else:   # voz antiga (sem a linha da selfie): a foto sai antes da confirmação
        c.marcar(SEL("video"), label='Selfie do ponto (câmera)')
        c.click(SEL("button:has-text('Tirar foto agora')"), at=round(c.L(3) - 1.3, 2), label='Tirar foto agora', noScroll=True,
                when=SEL("button:has-text('Tirar foto agora')"))
        nc = 3
    c.waitfor(text='Confirmar registro', timeout=12)
    c.mark(nc)
    c.confere('body', ['Entrada', 'Horário', 'Local', 'Rua das Oficinas, 1250 - Parque Industrial - Taubaté'], 'confirmação com o local do pátio')
    c.marcar(TXT('Tipo'), at=c.A(nc, 'tipo,', 0.3), label='confirmação: Tipo Entrada')
    c.marcar(TXT('Horário'), at=c.A(nc, 'horário,', 0.3), label='Horário e Local (zoom)')
    c.marcar(TXTX('Rua das Oficinas, 1250'), at=c.A(nc, 'local', 0.3), label='Local: Rua das Oficinas, 1250')
    c.marcar(SEL("[role=dialog] img"), at=c.A(nc, 'foto.', 0.3), label='miniatura da selfie')
    c.ev("JSON.stringify(window.__t19cam||null)", label='câmera falsa: reaberturas do app (achado: reinicia a cada segundo)')
    c.mark(nc + 1)
    c.click(SEL("button:has-text('Confirmar registro')"), at=c.A(nc + 1, 'Confirmar', 0.9), label='Confirmar registro', noScroll=True)
    c.waitfor(text='Ponto registrado', timeout=10)
    c.waitfor(text='Registros de hoje', timeout=8)
    c.marcar(TXTX('Registros de hoje'), at=c.A(nc + 1, 'gravada,', 0.3), label='Registros de hoje: Entrada')
    c.marcar(SEL("button:has-text('Iniciar Intervalo')"), at=c.A(nc + 1, 'intervalo', 0.3), label='Iniciar Intervalo')
    c.marcar(SEL("button:has-text('Registrar Saída')"), at=c.A(nc + 1, 'saída.', 0.3), label='Registrar Saída')
    c.mark(nc + 2)
    c.fim()
    return c


def cap10():
    """Folha de Ponto do Cláudio (novembro): a falta de 05/11 vira Atestado; rodapé e aviso do dia aberto; Exportar; Registro de Ponto
    com a batida do Gabriel; Lançar manual."""
    setup = RH + aba_setup('Folha de Ponto', 'Todos os funcionários') + [
        {'do': 'click', 'target': SEL("main button[role=combobox]:has-text('Todos os funcionários')")},
        {'do': 'waitFor', 'target': OPT('Cláudio Ferraz'), 'timeout': 8}, {'do': 'click', 'target': OPT('Cláudio Ferraz')},
        {'do': 'waitFor', 'text': 'Total do mês', 'timeout': 10}, {'do': 'wait', 'seconds': 0.8}]
    c = cap_novo(10, setup=setup)
    c.mark(1)
    c.confere('main', ['Cláudio Ferraz', 'Entrada → Saída', 'Trabalhado', 'Saldo', 'Status', 'Falta', 'Feriado', 'Completo'], 'folha de novembro do Cláudio')
    c.hover(SEL("main button[role=combobox]:has-text('Cláudio Ferraz')"), 0.4, at=c.A(1, 'Cláudio:', 0.75), label='a folha do Cláudio')
    c.hover(TXTX('Entrada → Saída', within='main'), 0.3, at=c.A(1, 'entrada', 0.75), label='coluna Entrada → Saída')
    c.hover(TXT('Trabalhado', within='main'), 0.3, at=c.A(1, 'trabalhadas', 0.75), label='coluna Trabalhado')
    c.hover(TXT('Saldo', within='main'), 0.4, at=c.A(1, 'saldo', 0.75), label='coluna Saldo')
    c.mark(2)
    LINHA05 = "main tr:has-text('05/11')"
    rola_ate(c, 'main', '05/11', c.A(2, 'Repara', 0.6), 'rola até o dia 05/11', y=380)
    c.hover(SEL(f"{LINHA05} :text-is('Falta')"), 2.4, at=c.A(2, 'Falta,', 0.75), label='a linha de 05/11: Falta (Lançar)')
    c.mark(3)
    c.cursor((1000, 140), at=c.A(3, 'É', 0.3), label='cursor descansa (ilustração da falta que aparece sozinha)')
    c.mark(4)
    c.click(SEL(f"{LINHA05} button:has-text('Lançar')"), at=c.A(4, 'Lançar,', 0.9), label='Lançar (05/11)')
    c.waitfor(text='Registre quem não veio', timeout=10)
    escolhe(c, CAMPO('absence-type'), 'Atestado', c.A(4, 'escolho', 0.9), c.A(4, 'Atestado', 0.6, nth=1), 'Tipo: Atestado')
    c.click(CAMPO('absence-notes'), at=c.A(4, 'coloco', 0.6), label='campo Observação')
    c.type(CAMPO('absence-notes'), 'Consulta médica', at=c.A(4, 'observação.', 0.3), label='Observação: Consulta médica', cps=40, noClick=True)
    c.click(SEL(f"{DLG} button:text-is('Lançar ausência')"), at=c.A(4, 'Lançar', 0.9, nth=1), label='Lançar ausência')
    c.waitfor(gone={'role': 'dialog'}, timeout=10)
    c.waitfor(target=SEL(f"{LINHA05} :text-is('Atestado')"), timeout=10)
    c.hover(SEL(f"{LINHA05} :text-is('Atestado')"), 0.6, at=c.A(4, 'Atestado.', 0.75, nth=2), label='05/11 agora Atestado')
    c.mark(5)
    rola_ate(c, 'main', 'Total do mês', c.A(5, 'rodapé', 0.6), 'rola até o rodapé da folha', y=520)
    c.confere('main', ['Total do mês', '1 com atestado', '1 dia(s) sem saída registrada não entram no saldo'], 'rodapé e aviso do dia aberto')
    c.hover(TXTX('Total do mês', within='main'), 0.8, at=c.A(5, 'total', 0.75), label='Total do mês (1 com atestado)')
    c.hover(TXTX('sem saída registrada', within='main'), 2.0, at=c.A(5, 'aviso:', 0.75), label='aviso: 1 dia(s) sem saída registrada não entram no saldo')
    c.mark(6)
    c.click(SEL("main button:has-text('Exportar')"), at=c.A(6, 'Exportar:', 0.9), label='Exportar')
    c.waitfor(text='Exportar Folha de Ponto', timeout=8)
    c.hover(SEL(f"{DLG} label[for='time-sheet-mode-pdf']"), 0.4, at=c.A(6, 'espelho', 0.75), label='Espelho de Ponto (PDF)')
    c.hover(SEL(f"{DLG} label[for='time-sheet-mode-excel']"), 0.4, at=c.A(6, 'planilha.', 0.75), label='Planilha para contabilidade (Excel)')
    c.hover(TXTX('Não substitui arquivos fiscais', within=DLG), 1.2, at=c.A(6, 'substitui', 0.75), label='Não substitui arquivos fiscais AEJ ou AFD.')
    c.click(BDLG('Cancelar'), at=round(c.Lfim(6) - 1.0, 2), label='Cancelar')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.mark(7)
    c.click(ABA('Registro de Ponto'), at=c.A(7, 'Registro', 0.9), label='aba Registro de Ponto')
    c.waitfor(text='Lançar manual', timeout=10)
    c.waitfor(text='Gabriel Rocha', timeout=10)
    CARD_G = SEL("xpath=//main//*[normalize-space(text())='Gabriel Rocha']/following::div[contains(@class,'border')][1]")
    rola_ate(c, 'main', 'Gabriel Rocha', c.A(7, 'uma', 0.4), 'rola até a batida do Gabriel', y=330, dur_ms=600, prefixo=False)
    c.hover(CARD_G, 1.6, at=c.A(7, 'Gabriel', 0.75), label='a batida do Gabriel: selfie, Entrada, hora, endereço, Mobile - Chrome')
    c.mark(8)
    c.hover(SEL("main button:has-text('Lançar manual')"), 2.0, at=c.A(8, 'Lançar', 0.75), label='Lançar manual')
    c.fim()
    return c


JS_JORNADA = r"""(async()=>{const dorme=ms=>new Promise(r=>setTimeout(r,ms));const dlg=[...document.querySelectorAll('[role=dialog]')].pop();if(!dlg)return 'SEM JANELA';
const linhas=[...dlg.querySelectorAll('div.rounded-lg.border')].filter(d=>/^(Seg|Ter|Qua|Qui|Sex)$/.test((d.querySelector('span.w-10')||{}).textContent||''));
if(linhas.length!==5)return 'SEM ALVO: '+linhas.length+' dias';let feito=[];
const escolhe=async(bt,hh)=>{bt.click();let lb=null;for(let i=0;i<30&&!lb;i++){await dorme(60);lb=[...document.querySelectorAll('[role=listbox]')].find(x=>/hora/i.test(x.getAttribute('aria-label')||''));}
if(!lb)return false;const op=[...lb.querySelectorAll('[role=option]')].find(o=>o.textContent.trim()===hh);if(!op)return false;op.click();await dorme(120);
const ok=[...document.querySelectorAll('[data-radix-popper-content-wrapper] button')].find(b=>b.textContent.trim()==='Concluir');if(ok)ok.click();
for(let i=0;i<30&&document.querySelector('[role=listbox]');i++)await dorme(50);return true};
for(const l of linhas){const bts=[...l.querySelectorAll('button')].filter(b=>/^\s*\d\d:\d\d\s*$|--:--/.test(b.textContent));if(bts.length<2)return 'SEM ALVO: horas de '+l.textContent;
if(!await escolhe(bts[0],'08'))return 'falhou entrada';if(!await escolhe(bts[1],'17'))return 'falhou saida';feito.push(l.querySelector('span.w-10').textContent);await dorme(150);}
return 'ok '+feito.join(',')})()"""


def cap11():
    """Configurações do ponto: selfie e localização, jornada padrão e dias; a jornada individual da Juliana (08:00 às 17:00)."""
    c = cap_novo(11, setup=RH)
    c.mark(1)
    c.click(ABA('Configurações de Ponto'), at=c.A(1, 'Configurações', 0.9), label='aba Configurações de Ponto')
    c.waitfor(text='Jornada Padrão da Empresa', timeout=10)
    rola_ate(c, 'main', 'Jornada Padrão da Empresa', c.A(1, 'regras.', 0.4), 'o cartão Jornada Padrão da Empresa', y=120)
    c.confere('main', ['Exigir selfie', 'Exigir localização', 'Dias em que a empresa trabalha'], 'regras do ponto')
    c.confere_campos(['60', '10'], 'intervalo 60 e tolerância 10', escopo='main')
    c.hover(TXT('Exigir selfie', within='main'), 0.4, at=c.A(1, 'selfie', 0.75), label='Exigir selfie (ligado)')
    c.hover(TXT('Exigir localização', within='main'), 0.8, at=c.A(1, 'localização', 0.75), label='Exigir localização (ligado)')
    c.mark(2)
    c.hover(CAMPO('default-in', 'main'), 0.3, at=c.A(2, 'sete,', 0.75), label='Entrada padrão 07:00')
    c.hover(CAMPO('default-out', 'main'), 0.3, at=c.A(2, 'quatro', 0.75), label='Saída padrão 16:00')
    c.hover(CAMPO('default-break', 'main'), 0.3, at=c.A(2, 'hora', 0.75), label='Intervalo padrão (min) 60')
    c.hover(CAMPO('late-tol', 'main'), 0.6, at=c.A(2, 'dez', 0.75), label='Tolerância de atraso (min) 10')
    c.mark(3)
    rola_ate(c, 'main', 'Dias em que a empresa trabalha', c.A(3, 'E', 0.4), 'rola até os dias da empresa', y=330, dur_ms=600)
    c.hover(SEL("main #work-weekday-1"), 0.3, at=c.A(3, 'segunda', 0.75), label='Dias em que a empresa trabalha: Seg')
    c.hover(SEL("main #work-weekday-5"), 1.0, at=c.A(3, 'sexta.', 0.75), label='Seg a Sex ligados')
    c.mark(4)
    rola_ate(c, 'main', 'Jornada Individual', c.A(4, 'jornada', 0.6), 'rola até a Jornada Individual', y=160)
    LAPIS = SEL("main tr:has-text('Juliana Prado') button:has(svg.lucide-pencil)")
    c.hover(SEL("main tr:has-text('Juliana Prado')"), 0.3, at=c.A(4, 'Juliana,', 0.75), label='a linha da Juliana (horários herdados em cinza)')
    c.mark(5)
    c.click(LAPIS, at=c.A(5, 'lápis', 0.9), label='lápis da Juliana Prado')
    c.waitfor(text='Sobrescreve o padrão da empresa para este funcionário.', timeout=8)
    c.ev(JS_JORNADA, at=c.A(5, 'troco', 0.3), label='Seg a Sex: 08:00 às 17:00 (trecho acelerado, selo 4x)')
    c.confere('dlg', ['08:00', '17:00'], 'jornada da Juliana 08:00 às 17:00')
    c.click(SEL(f"{DLG} button:has-text('Salvar jornada')"), at=c.A(5, 'Salvar', 0.9), label='Salvar jornada')
    c.waitfor(text='Jornada salva', timeout=8)
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.confere("main table", ['08:00-17:00'], 'a jornada da Juliana na tabela')
    c.hover(SEL("main tr:has-text('Juliana Prado')"), 1.0, at=c.A(5, 'folha', 0.75), label='a linha da Juliana: 08:00-17:00 (1h int.)')
    c.mark(6)
    c.cursor((1000, 140), at=c.A(6, 'A', 0.3), label='cursor descansa (ilustração da jornada)')
    c.fim()
    return c


def cap12():
    """Arquivar o Rogério, Inativos (Reativar) e o diálogo do Excluir definitivamente (Cancelar)."""
    c = cap_novo(12, setup=RH)
    c.mark(1)
    rola_ate(c, 'main [role=list]', 'Rogério Batista', c.A(1, 'sai', 0.4), 'rola a lista até o Rogério', y=520, dur_ms=600, prefixo=False)
    c.click(LINHA('Rogério Batista'), at=c.A(1, 'Rogério,', 0.8), label='Rogério Batista')
    c.waitfor(target=DADO('Último pagamento'), timeout=10)
    c.confere(FICHA, ['Ajudante de pátio', '30/10/2026'], 'Rogério: último pagamento 30/10')
    c.hover(DADO('Último pagamento'), 1.0, at=c.A(1, 'recebeu', 0.75), label='Último pagamento 30/10/2026')
    c.mark(2)
    menu_linha(c, 'Rogério Batista', 'Arquivar', at=c.A(2, 'arquivar.', 1.0), label='menu ⋯ do Rogério')
    c.hover(ITEM('Arquivar'), 3.0, at=c.A(2, 'Assim', 0.5), label='Arquivar em destaque (sem clicar)', noScroll=True)
    c.mark(3)
    item_menu(c, 'Rogério Batista', 'Arquivar', at=c.A(3, 'Arquivar.', 0.6), label='Arquivar')
    c.waitfor(text='Funcionário arquivado', timeout=8)
    c.waitfor(gone=LINHA('Rogério Batista'), timeout=8)
    c.mark(4)
    c.click(SEL("main button:text-is('Inativos')"), at=c.A(4, 'Inativos.', 0.9), label='Inativos')
    c.waitfor(target=LINHA('Rogério Batista'), timeout=8)
    menu_linha(c, 'Rogério Batista', 'Reativar', at=c.A(4, 'voltar', 0.8), label='menu ⋯ do Rogério (Inativos)')
    c.hover(ITEM('Reativar'), 0.6, at=c.A(4, 'Reativar.', 0.6), label='Reativar (sem clicar)', noScroll=True)
    c.mark(5)
    item_menu(c, 'Rogério Batista', 'Excluir definitivamente', at=c.A(5, 'Excluir', 0.6), label='Excluir definitivamente')
    c.waitfor(text='Atenção: esta ação é irreversível.', timeout=8)
    c.hover(TXTX('Atenção: esta ação é irreversível.', within='[role=alertdialog], [role=dialog]'), 2.0, at=c.A(5, 'histórico', 0.75),
            label='o texto do Excluir definitivamente (zoom)')
    c.mark(6)
    c.cursor((1000, 140), at=c.A(6, 'Pra', 0.3), label='cursor descansa (ilustração arquivo x lixeira)')
    c.mark(7)
    c.click(SEL("[role=alertdialog] button:text-is('Cancelar'), [role=dialog] button:text-is('Cancelar')"), at=c.A(7, 'Cancelar.', 0.9), label='Cancelar')
    c.waitfor(gone={'role': 'alertdialog'}, timeout=8)
    c.fim()
    return c


def cap13():
    """Recapitulando: passeio rápido pelo estado final (o editor monta os trechos): cadastro e custo do Gabriel, Transporte, Diego,
    Cláudio, o extrato do Edson, Copiar link do ponto, a folha com Atestado e os Inativos."""
    c = cap_novo(13, setup=RH)
    c.mark(1)
    menu_linha(c, 'Gabriel Rocha', 'Editar', at=c.A(1, 'Gabriel', 1.0), label='menu ⋯ do Gabriel')
    item_menu(c, 'Gabriel Rocha', 'Editar', label='Editar o Gabriel')
    c.waitfor(target=CAMPO('name'), timeout=10)
    c.click(DTAB('Remuneração'), at=c.A(1, 'custo', 0.9), label='Remuneração: salário, custo mensal R$ 4.264,00 e CLT')
    c.hover(CAMPO('monthly_cost'), 0.8, label='Custo mensal total R$ 4.264,00')
    c.click(BDLG('Cancelar'), at=c.A(1, 'regime', 0.6), label='Cancelar')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.mark(2)
    c.hover(SEL("main [role=listitem]:has(p:text-is('Edson Moura')) span:has-text('Transporte')"), 0.4, at=c.A(2, 'Transporte,', 0.75), label='o departamento Transporte')
    c.click(LINHA('Diego Morais'), at=c.A(2, 'Diego', 0.8), label='Diego: vale e falta')
    c.hover(RESUMO('Faltas'), 0.3, label='Diego: Vales 200 e Faltas 90')
    c.click(LINHA('Cláudio Ferraz'), at=c.A(2, 'Cláudio.', 0.8), label='Cláudio: bônus')
    c.hover(RESUMO('Bônus'), 0.3, label='Cláudio: Bônus 150')
    c.mark(3)
    c.click(LINHA('Edson Moura'), at=c.A(3, 'Edson,', 0.8), label='Edson')
    c.click(SEL(f"{FICHA} button:has-text('Extrato')"), at=c.A(3, 'extrato.', 1.2), label='Extrato - Edson Moura')
    c.waitfor(text='Extrato - Edson Moura', timeout=10)
    c.mark(4)
    c.click(BDLG('Fechar'), at=c.A(4, 'Ligou', 0.6), label='Fechar o extrato')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    menu_linha(c, 'Gabriel Rocha', 'Copiar link do ponto', at=c.A(4, 'ponto', 0.6), label='menu ⋯ do Gabriel: Copiar link do ponto')
    c.press('Escape', label='fecha o menu')
    c.click(ABA('Folha de Ponto'), at=c.A(4, 'falta', 1.2), label='Folha de Ponto')
    c.waitfor(text='Todos os funcionários', timeout=10)
    c.mark(5)
    c.click(ABA('Funcionários'), at=c.A(5, 'arquivou', 0.9), label='Funcionários')
    c.waitfor(target=LINHA('Rafael Nogueira'), timeout=10)
    c.click(SEL("main button:text-is('Inativos')"), at=c.A(5, 'Rogério,', 0.6), label='Inativos com o Rogério')
    c.waitfor(target=LINHA('Rogério Batista'), timeout=8)
    c.mark(6)
    c.cursor((1000, 140), at=c.A(6, 'No', 0.3), label='cursor descansa (cartão Próximo)')
    c.fim()
    return c


CAPS_ROBO = {n: globals()[f'cap{n:02d}'] for n in range(14) if f'cap{n:02d}' in globals()}

if __name__ == '__main__':
    quais = [int(a) for a in sys.argv[1:]] or sorted(CAPS_ROBO)
    for n in quais:
        c = CAPS_ROBO[n]()
        if os.environ.get('AMBIGUAS'):
            for i, w, k, tot in c.ambiguas:
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
        resp = ''.join(f'\n    RESPIRO PENDENTE: a voz precisa de +{dd:.2f} s na L{li} (T {t:.2f} s no take): pausas.py {n:02d} {t:.2f}:{dd:.2f}'
                       for li, t, dd in c.respiros)
        print(f'cap{n:02d}: {len(d["steps"])} passos, narração {c.dur:.1f} s ({"estimada" if c.estimada else "da voz"}), FAKE_NOW {FAKE_NOW[n]}{resp}')
