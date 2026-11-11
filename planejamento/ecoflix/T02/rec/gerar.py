#!/usr/bin/env python3
"""T2 · Usuários e permissões (EcoFlix, EcoSistema 1.59.154): gera rec/t02/cap00..cap10.json (roteiros do robô) a partir da fala
($TUT_HOME/t02/narracao/capNN.json: o estimado até a voz chegar; com a voz, o da voz, sem mudar nada aqui).

Computador 1280x800, Rafael Nogueira (master) na Recicla Vale Metais; FAKE_NOW 2026-11-10T08:30:00-03:00 em todos os capítulos
(o mesmo no Supabase falso e no robô). Rodar de qualquer pasta: `python3 -I rec/t02/gerar.py [NN ...]` (ANCORAS=1 lista as
âncoras). Depois: `node rec/record.mjs rec/t02/capNN.json --check`; gravar um capítulo: `bash rec/t02/t02_rodar.sh NN [--ens]`.
Login: todo capítulo é "anonymous" e o setup entra pela tela de login com "$TUT_USER"/"$TUT_SENHA" do ambiente (o Supabase
falso aceita qualquer senha; o token sai no relógio do mundo, então o "relógio adiantado" do app não barra). O app registra a
sessão do Rafael no login, e é ela que dá o "Online agora" do detalhe.

Cada passo é preso a uma palavra da fala: A(linha, 'palavra', folga) = início da palavra - folga (o custo do gesto até o cursor
chegar: clique ~0,6 s, 1o clique numa janela recém-aberta ~1,1 s, hover ~0,5 s; digitação sem clique na palavra - 0,05 s).
A palavra casa INTEIRA (sem acento e pontuação, sem prefixo); repetida na linha pede `nth`. Marca Ln 0,9 s antes da linha (molde
do T14); um passo que começa até 0,25 s antes da marca a puxa para o início dele.

Estado de partida (rec/mundo/seeds-extra/t02/, escrito por t02_sementes.py): `inicio` (só o Rafael: o mundo base já traz a Juliana
e o Marcos, e a aula os cria na tela) nos caps 0 a 3; + `apos-cap03` (Marcos, Operador Padrão) no cap04; + `apos-cap04` (Juliana) no
cap05; + `apos-cap05` (Marcos com foto, tela inicial Caixa e sem Ver Projeção de Lucro) nos caps 6 a 10. Os caps 6 a 9 terminam
no estado em que começam (ativa de novo, cancela, cancela, cancela).

O que este tutorial ensinou ao robô (explorações rec/t02/_ex/e1..e5, 10/11):
 - "Excluir usuário" e "Passar o controle da empresa?" são AlertDialog: `[role=alertdialog]`, não `[role=dialog]`.
 - A foto do Editar sobe inteira pelo desvio do robô (14.977 bytes conferidos no Supabase falso) e aparece na lista na hora.
 - O "Configurações" do rodapé do menu fica em y 752..788 (fora da faixa 96..730 do clique): `noScroll`. O Dashboard tem outro
   botão "Configurações" (o do painel, no alto): o do menu é `button[aria-label="Configurações"]`.
 - A janela Criar/Editar Usuário (1024x720) tem DUAS rolagens: o corpo da janela (553 px visíveis, desce 165 px) e a lista de
   permissões (ScrollArea de 368 px, ~2.170 px de conteúdo). Com o corpo no alto, só ~220 px da lista aparecem: os capítulos de
   permissão descem o corpo antes de mexer na lista (rolagem suave por `eval`, sem o robô procurar o alvo com a roda).
 - "Rafael Nogueira" também aparece no rodapé do menu (troca de conta): alvo da lista sempre `within: main`.
 - O menu "..." (HoverDropdownMenu) abre ao passar o mouse e fecha 250 ms depois de sair; o do detalhe é o 2o da página (`nth` 1).
 - A busca "nota" também mostra o bloco do Cato (a descrição dele fala em "notas"): abrir as ações do Fiscal & Ambiental logo em
   seguida empurra o bloco para fora da lista visível.
 - Observador `OBS` guarda em window.__avisos todo aviso de erro do app (texto ou toast vermelho); o passo final devolve a lista.
"""
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TUT_HOME = os.path.normpath(os.path.join(HERE, '..', '..'))
NARR = os.path.join(TUT_HOME, 't02', 'narracao')
FAKE_NOW = '2026-11-10T08:30:00-03:00'
NOMES = ['Abertura', 'Onde fica', 'Criar o usuário', 'Os três perfis rápidos', 'Telas e ações', 'O balanceiro e o escritório',
         'Desativar ou excluir', 'Passar o controle', 'O limite de usuários', 'Esconder o valor', 'Recapitulando']
_C = ['t02/inicio', 't02/apos-cap03', 't02/apos-cap04', 't02/apos-cap05']
SEMENTE = {0: _C[:1], 1: _C[:1], 2: _C[:1], 3: _C[:1], 4: _C[:2], 5: _C[:3], 6: _C, 7: _C, 8: _C, 9: _C, 10: _C}
# senhas FICTÍCIAS dos usuários criados na tela (plano.md do T2; aparecem em pontinhos e nunca são faladas). A senha de quem
# grava ($TUT_SENHA) não entra em arquivo nenhum.
SENHA_MARCOS = 'Balanca#2026'
SENHA_JULIANA = 'Escritorio#2026'
EMAIL_MARCOS = 'marcos.antunes@reciclavalemetais.example'
EMAIL_JULIANA = 'juliana.prado@reciclavalemetais.example'
FOTO_MARCOS = 'assets/marcos-antunes.jpg'   # t02_avatar_marcos.py (relativo a rec/t02/, a pasta do roteiro)

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
OBS = ("(()=>{window.__avisos=[];const re=/N[ãa]o foi poss[ií]vel|Erro ao|Tente novamente|Algo deu errado|Falha ao|Something went wrong/i;"
       "const chk=(t)=>{t=(t||'').trim();const m=t&&t.match(new RegExp('[^]{0,40}('+re.source+')[^]{0,40}','i'));"
       "if(m&&window.__avisos.length<10)window.__avisos.push(m[0].replace(/[\\n\\r\\t ]+/g,' '))};new MutationObserver(ms=>{for(const m of ms){"
       "m.addedNodes.forEach(n=>chk(n.textContent));if(m.type==='characterData')chk(m.target.textContent)}}).observe(document.body,"
       "{childList:true,subtree:true,characterData:true});chk(document.body.innerText);"
       "setInterval(()=>{document.querySelectorAll('[data-sonner-toast][data-type=error]').forEach(t=>{const s='TOAST DE ERRO: '+t.textContent.trim().slice(0,90);"
       "if(!window.__avisos.includes(s)&&window.__avisos.length<10)window.__avisos.push(s)})},300);return 1})()")


class Cap:
    def __init__(s, n, pace=0.5, cps=30, start=(760, 470), prewarm=None, setup=None):
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
        s._ancora = (t, f'L{i} {palavra}' + (f' #{nth}' if nth else ''))   # vai como `note` no passo (t02_confere.py mede o gesto x palavra)
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
        anc = getattr(s, '_ancora', None)
        if at is not None and anc and abs(anc[0] - at) < 1e-6:
            d['note'] = anc[1]
        s._ancora = None
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

    def marcar(s, target, at=None, label=None):
        """registra o retângulo do alvo para a câmera (zoom) sem mexer no mouse: `type` sem clique e sem texto"""
        return s._p({'do': 'type', 'target': target, 'text': '', 'noClick': True, 'optional': True, 'timeout': 4}, at, label, {})

    def select(s, target, option, at=None, label=None, **kw):
        return s._p({'do': 'select', 'target': target, 'option': option}, at, label, kw)

    def press(s, key, at=None, label=None, **kw):
        return s._p({'do': 'press', 'key': key}, at, label, kw)

    def upload(s, target, arquivo, at=None, label=None, **kw):
        return s._p({'do': 'upload', 'target': target, 'file': arquivo}, at, label, kw)

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

    def confere_js(s, js_bool_texto, label):
        """`eval` com uma expressão que devolve 'OK: ...' ou 'DIFERENTE: ...' (conferência pontual: interruptor, selo...)"""
        return s.add({'do': 'eval', 'js': js_bool_texto, 'label': 'confere ' + label})

    def fim(s):
        s.flush(1e9)
        s.steps.append({'do': 'eval', 'js': 'JSON.stringify(window.__avisos || "sem observador")', 'label': 'avisos de erro na tela'})
        s.steps.append({'do': 'mark', 'name': 'FIM', 'at': round(s.dur, 2)})

    def out(s):
        encurta_pausas(s.steps)
        est = ' ESTIMADA' if s.estimado else ''
        return {
            'name': f't02-cap{s.n:02d}',
            'title': f'T2 · Cap. {s.n} · {NOMES[s.n]} (narração{est} {str(round(s.dur, 1)).replace(".", ",")} s; marcas L1..L{len(s.linhas)} = '
                     f'início de cada linha do roteiro; FAKE_NOW {FAKE_NOW}; logado como Rafael Nogueira)',
            'seed': f't02-cap{s.n:02d}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
            'start': {'x': s.start[0], 'y': s.start[1]},
            'anonymous': True, 'storage': dict(STORAGE),
            'seedExtra': list(SEMENTE[s.n]),
            'prewarm': s.prewarm, 'setup': s.setup, 'steps': s.steps,
        }


# ---------------------------------------------------------------- alvos
MAIN = 'main'
DLG = '[role=dialog]'
ALERTA = '[role=alertdialog]'                                                # Excluir usuário e Passar o controle
BTN = lambda n, within=None, **kw: {'role': 'button', 'name': n, 'exact': True, **({'within': within} if within else {}), **kw}
TXT = lambda t, within=MAIN, **kw: {'text': t, 'exact': True, 'within': within, **kw}
SEL = lambda s, **kw: {'selector': s, **kw}
CONFIG_RODAPE = SEL('button[aria-label="Configurações"]')                    # rodapé do menu (y 752..788): noScroll
SAIR = SEL('button[aria-label="Sair"]')
ABA_USUARIOS = SEL('#tab-btn-users')
SELO = lambda txt: TXT(txt)                                                   # "1 / 3 usuários" (o selo do topo)
LINHA = lambda nome: TXT(nome)                                                # nome na lista (o 1o "nome" de main é o da lista)
COROA = SEL('main svg[aria-label="Usuário master"]')
ACOES = lambda nome, nth=1: SEL(f"main button[aria-label='Ações de {nome}']", nth=nth)   # "..." (0 = linha da lista, 1 = detalhe)
ITEM = lambda nome: {'role': 'menuitem', 'name': nome}
CRIAR = BTN('Criar Usuário', MAIN)
CRIAR_DLG = BTN('Criar Usuário', DLG)
EDITAR = BTN('Editar', MAIN)
CHIP = lambda nome: BTN(nome, DLG)                                            # perfis rápidos
PERSONALIZADO = SEL(f'{DLG} span.bg-amber-500')
SW = lambda nome: {'role': 'switch', 'name': nome, 'exact': True}             # interruptor de ação (o nome é o rótulo da ação)
TELA = lambda nome: SW(f'Acesso à tela {nome}')                               # interruptor da tela
VER = lambda nome: BTN(f'Ver ações de {nome}', DLG)                           # "Clique para ver N ações" (abre/fecha)
CONTADOR = lambda nome: SEL(f"{DLG} button[aria-label='Ver ações de {nome}'] div.tabular-nums")   # selo "x/N" da tela
ACAO = lambda nome: SEL(f"{DLG} div.items-start:has(> [role=switch][aria-label='{nome}'])")      # linha de uma ação (interruptor + texto)
BUSCA = {'placeholder': 'Buscar tela ou ação...', 'within': DLG}
LIMPAR = {'role': 'button', 'name': 'Limpar busca'}
AGUARDA = {'do': 'waitFor', 'idle': True}

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
# valor nunca vai para arquivo nem log). Sem a sessão pronta do robô, o localStorage que ele poria vai aqui: versão já vista,
# PWA dispensado, tema claro e as chaves do mundo (mundo.json "navegador.localStorage": lembrete de tarefas do dia e preferências).
STORAGE = {'app_version': VERSAO, 'notification_shown_version': VERSAO, 'pwa-install-dismissed': 'true', 'theme': 'light',
           f'daily-tasks-reminder-last-shown-{RAFAEL}': HOJE, 'initial-preferences-set': 'true'}
LOGIN = [{'do': 'waitFor', 'target': {'label': 'E-mail'}, 'timeout': 30},
         {'do': 'type', 'target': {'label': 'E-mail'}, 'text': '$TUT_USER', 'cps': 40},
         {'do': 'type', 'target': {'label': 'Senha', 'exact': True}, 'text': '$TUT_SENHA', 'cps': 40},
         {'do': 'click', 'target': {'role': 'button', 'name': 'Entrar', 'exact': True}},
         {'do': 'waitFor', 'text': 'Olá, Rafael!', 'timeout': 30}, AGUARDA]
# ?tab= por navegação interna só troca a aba se o app não estiver em /configuracoes: vem do Dashboard (lição do T2 da Domiflix).
# A ida às Configurações no setup do Dashboard carrega o módulo da página antes do vídeo (o cap01 a abre pelo menu, filmado).
IR_USUARIOS = [{'do': 'goto', 'url': '/configuracoes?tab=users'}, {'do': 'waitFor', 'text': 'Empresa: Recicla Vale Metais', 'timeout': 25}, AGUARDA]
SETUP_DASH = LOGIN + IR_USUARIOS + [{'do': 'goto', 'url': '/dashboard'}, {'do': 'waitFor', 'text': 'Olá, Rafael!', 'timeout': 25}, AGUARDA]
SETUP_USUARIOS = LOGIN + IR_USUARIOS

# ---------------------------------------------------------------- JavaScript (rolagens suaves e cliques sem cursor)
ACHA_ROLAGEM = ("const rolagem=(el)=>{let c=el&&el.parentElement;while(c&&c!==document.body){const s=getComputedStyle(c);"
                "if(/(auto|scroll)/.test(s.overflowY)&&c.scrollHeight>c.clientHeight+4)return c;c=c.parentElement;}return null};")
SUAVE = ("await new Promise(res=>{const t0=performance.now();const f=t=>{const p=Math.min(1,(t-t0)/DUR),e=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;"
         "c.scrollTop=y0+dy*e;p<1?requestAnimationFrame(f):res()};requestAnimationFrame(f)});")


def js_rola(seletor, y, dur_ms=700):
    """rolagem suave do contêiner que rola o elemento `seletor` (o mais próximo) até o topo dele ficar em y px CSS (limitado ao que
    o contêiner rola). Devolve o topo final, 'ok' (já estava), 'SEM ALVO' ou 'SEM ROLAGEM'."""
    return ("(async()=>{" + ACHA_ROLAGEM + f"const el=document.querySelector({json.dumps(seletor)});if(!el)return 'SEM ALVO';"
            "const c=rolagem(el);if(!c)return 'SEM ROLAGEM';"
            f"let dy=Math.round(el.getBoundingClientRect().top-{int(y)});const y0=c.scrollTop;dy=Math.max(-y0,Math.min(c.scrollHeight-c.clientHeight-y0,dy));"
            "if(Math.abs(dy)<3)return 'ok';" + SUAVE.replace('DUR', str(int(dur_ms))) + "return Math.round(el.getBoundingClientRect().top)})()")


def js_rola_texto(texto, y, dur_ms=700, escopo=DLG):
    """como js_rola, com o alvo achado pelo texto (o menor elemento do escopo cujo texto é exatamente `texto`)"""
    return ("(async()=>{" + ACHA_ROLAGEM + f"const el=[...document.querySelectorAll({json.dumps(escopo + ' *')})].filter(e=>e.textContent.trim()==={json.dumps(texto)})"
            ".sort((a,b)=>a.textContent.length-b.textContent.length||a.children.length-b.children.length)[0];if(!el)return 'SEM ALVO';"
            "const c=rolagem(el);if(!c)return 'SEM ROLAGEM';"
            f"let dy=Math.round(el.getBoundingClientRect().top-{int(y)});const y0=c.scrollTop;dy=Math.max(-y0,Math.min(c.scrollHeight-c.clientHeight-y0,dy));"
            "if(Math.abs(dy)<3)return 'ok';" + SUAVE.replace('DUR', str(int(dur_ms))) + "return Math.round(el.getBoundingClientRect().top)})()")


def js_colar(texto):
    """cola o texto no campo em foco (execCommand insertText: o React recebe o input), ~0,05 s em vez de digitar letra a letra"""
    return ("(()=>{const e=document.activeElement;if(!e||!/^(INPUT|TEXTAREA)$/.test(e.tagName))return 'SEM ALVO (nada em foco)';"
            f"document.execCommand('insertText',false,{json.dumps(texto)});return e.value}})()")


def js_corpo_abaixo(dur_ms=600):
    """desce o corpo da janela Criar/Editar Usuário até o fim (a lista de permissões aparece inteira: 368 px)"""
    return js_rola(f'{DLG} input[placeholder="Buscar tela ou ação..."]', 150, dur_ms)


def js_lista(nome_switch, y, dur_ms=700):
    """rola a lista de permissões até o interruptor `nome_switch` (aria-label) ficar em y"""
    return js_rola(f'{DLG} [role=switch][aria-label="{nome_switch}"]', y, dur_ms)


def js_liga(*nomes):
    """liga (sem cursor) os interruptores com esses aria-label que estiverem desligados: o time-lapse do que a fala não cita"""
    return ("(()=>{const r=[];for(const n of %s){const s=document.querySelector('[role=dialog] [role=switch][aria-label=\"'+n+'\"]');"
            "if(!s){r.push('SEM ALVO '+n);continue}if(s.getAttribute('data-state')!=='checked'){s.click();r.push('ligou '+n)}else r.push('já '+n)}"
            "return r.join(' | ')})()") % json.dumps(list(nomes), ensure_ascii=False)


def js_abre_acoes(*telas):
    """abre (sem cursor) as ações das telas, se ainda fechadas"""
    return ("(()=>{const r=[];for(const n of %s){const b=document.querySelector('[role=dialog] button[aria-label=\"Ver ações de '+n+'\"]');"
            "if(!b){r.push('SEM ALVO '+n);continue}if(b.getAttribute('data-state')!=='open'){b.click();r.push('abriu '+n)}else r.push('já '+n)}"
            "return r.join(' | ')})()") % json.dumps(list(telas), ensure_ascii=False)


def js_estado(*nomes):
    """confere o estado de interruptores: nomes 'X' (tem de estar ligado) e '-X' (desligado)"""
    return ("(()=>{const r=[];let ok=true;for(let n of %s){const off=n.startsWith('-');if(off)n=n.slice(1);"
            "const s=document.querySelector('[role=dialog] [role=switch][aria-label=\"'+n+'\"]');const st=s?s.getAttribute('data-state'):'sem';"
            "if(st!==(off?'unchecked':'checked'))ok=false;r.push(n+'='+st)}return (ok?'OK: ':'DIFERENTE: ')+r.join(' | ')})()") % json.dumps(list(nomes), ensure_ascii=False)


def js_selo(nome, esperado):
    return ("(()=>{const b=document.querySelector(\"[role=dialog] button[aria-label='Ver ações de %s'] div.tabular-nums\");"
            "const t=b?b.textContent.trim():'sem selo';return (t===%s?'OK: ':'DIFERENTE: ')+'%s '+t})()") % (nome, json.dumps(esperado), nome)


def _invisivel(d):
    return d['do'] in ('mark', 'waitFor') or (d['do'] == 'eval' and str(d.get('label', '')).startswith(('confere', 'avisos')))


def encurta_pausas(steps):
    """hover seguido (pulando marcas, esperas e conferências) de um gesto com `at`: a pausa no alvo não muda o vídeo (o cursor fica
    ali até o `at` seguinte), só empurra o gesto seguinte quando a máquina está carregada (ensaio de 11/11: ação e pausa ~2,5x mais
    lentas com render de cenas em paralelo). Fica 0,15 s. Os de ZOOM mantêm a pausa: a câmera usa o tEnd do passo."""
    for k, d in enumerate(steps):
        if d['do'] != 'hover' or 'ZOOM' in str(d.get('label', '')) or d.get('seconds', 0.9) <= 0.15:
            continue
        prox = next((x for x in steps[k + 1:] if not _invisivel(x)), None)
        if prox is None or prox.get('at') is not None:
            d['seconds'] = 0.15


def cap_novo(n, setup=None, **kw):
    return Cap(n, setup=setup if setup is not None else SETUP_USUARIOS, **kw)


# ================================================================ capítulos
def cap00():
    """Abertura: o Dashboard da Recicla Vale (sob a ilustração da equipe nas linhas 1 a 4); no fim o cursor vai ao Configurações."""
    c = cap_novo(0, setup=SETUP_DASH, start=(760, 300))
    c.mark(1)
    c.hover(TXT('Olá, Rafael!', exact=False), 1.2, at=0.4, label='Dashboard da Recicla Vale Metais (Olá, Rafael!)')
    for i in (2, 3, 4, 5):
        c.mark(i)
    c.hover(CONFIG_RODAPE, 1.0, at=c.A(5, 'onde', 0.5), label='Configurações do rodapé do menu (sem clicar)', noScroll=True)
    c.fim()
    return c


def cap01():
    """Onde fica: rodapé do menu > Configurações > aba Usuários e Permissões; selo, Criar Usuário e o Rafael (master)."""
    c = cap_novo(1, setup=SETUP_DASH, start=(700, 360))
    c.mark(1)
    c.hover(CONFIG_RODAPE, 2.2, at=c.A(1, 'Configurações,', 0.5), label='Configurações (rodapé do menu, do lado do Sair)', noScroll=True)
    c.mark(2)
    c.click(CONFIG_RODAPE, at=c.A(1, 'Sair.', 0.25), label='clica em Configurações', noScroll=True)
    c.waitfor(text='Configurações do Sistema', timeout=15)
    c.click(ABA_USUARIOS, at=c.A(2, 'aqui,', 0.6), label='aba Usuários e Permissões')
    c.waitfor(text='Gerencie usuários da empresa, papéis e permissões de acesso', timeout=12)
    c.confere('main', ['Empresa: Recicla Vale Metais', '1 / 3 usuários', 'Criar Usuário', 'Rafael Nogueira', 'Acesso total · Ativo'],
              'a aba com a empresa, o selo 1 / 3 e só o Rafael')
    c.mark(3)
    c.hover(TXT('Empresa: Recicla Vale Metais'), 0.3, at=c.A(3, 'Em', 0.45), label='Empresa: Recicla Vale Metais')
    c.hover(SELO('1 / 3 usuários'), 1.2, at=c.A(3, 'contador', 0.5), label='selo 1 / 3 usuários')
    c.hover(CRIAR, 1.0, at=c.A(3, 'Criar', 0.5), label='botão Criar Usuário')
    c.hover(LINHA('Rafael Nogueira'), 0.8, at=c.A(3, 'Rafael,', 0.5), label='Rafael na lista (Acesso total · Ativo)')
    c.mark(4)
    c.click(LINHA('Rafael Nogueira'), at=c.A(4, 'nome,', 0.6), label='clica no Rafael (abre o detalhe)')
    c.waitfor(target=TXT('Perfil de acesso'), timeout=10)
    c.confere('main', ['Master', 'Ativo', 'Perfil de acesso', 'Acesso Total', 'Online agora',
                       'Este usuário tem acesso a todas as telas e ações disponíveis nos módulos contratados pela empresa.'], 'detalhe do Rafael')
    c.hover(COROA, 1.0, at=c.A(4, 'coroa', 0.5), label='coroa do master na lista')
    c.hover(TXT('Master'), 2.2, at=c.A(4, 'master:', 0.5), label='selo Master no detalhe (o responsável pela conta)')
    c.mark(5)
    c.mark(6)
    c.fim()
    return c


def cap02():
    """Criar o usuário: Criar Usuário, nome, e-mail e senha do Marcos (Senha forte), a foto fica para o Editar; termina com a janela aberta."""
    c = cap_novo(2, start=(900, 470))
    c.mark(1)
    c.click(CRIAR, at=c.A(1, 'Criar', 0.6), label='Criar Usuário')
    c.waitfor(text='Preencha os dados do novo usuário', timeout=10)
    c.mark(2)
    # com a máquina carregada a digitação do robô cai a ~0,2 s por letra (ensaio de 11/11): o nome começa já no "nome", o e-mail (41
    # letras) entra colado e a senha vai mais rápida
    c.click(SEL('#fullName'), at=c.A(2, 'Primeiro', 0.8), label='campo Nome Completo')
    c.type(SEL('#fullName'), 'Marcos Antunes', at=c.A(2, 'nome', 0.05), noClick=True, cps=30, label='Nome Completo: Marcos Antunes')
    c.mark(3)
    c.click(SEL('#email'), at=c.A(3, 'e-mail.', 0.6), label='campo Email')
    c.ev(js_colar(EMAIL_MARCOS), at=c.A(3, 'e-mail.', -0.1), label='Email do Marcos (colado)')
    c.mark(4)
    c.click(SEL('#password'), at=c.A(4, 'senha', 0.6), label='campo Senha')
    c.type(SEL('#password'), SENHA_MARCOS, at=c.A(4, 'define,', 0.05), noClick=True, cps=20, label='Senha (aparece em pontinhos)')
    c.confere('dlg', ['Senha forte. Deve conter:', 'Pelo menos 8 caracteres', 'Pelo menos 1 número', 'Pelo menos 1 letra minúscula',
                      'Pelo menos 1 letra maiúscula', 'Pelo menos 1 caractere especial'], 'Senha forte e os cinco itens')
    c.marcar(TXT('Senha forte. Deve conter:', DLG), at=c.A(4, 'Repara', 0.0), label='ZOOM indicador Senha forte e os cinco itens')
    c.hover(TXT('Pelo menos 8 caracteres', DLG), 0.3, at=c.A(4, 'oito', 0.5), label='Pelo menos 8 caracteres')
    c.hover(TXT('Pelo menos 1 número', DLG), 0.3, at=c.A(4, 'número,', 0.5), label='Pelo menos 1 número')
    c.hover(TXT('Pelo menos 1 letra minúscula', DLG), 0.3, at=c.A(4, 'minúscula,', 0.5), label='Pelo menos 1 letra minúscula')
    c.hover(TXT('Pelo menos 1 letra maiúscula', DLG), 0.3, at=c.A(4, 'maiúscula', 0.5), label='Pelo menos 1 letra maiúscula')
    c.hover(TXT('Pelo menos 1 caractere especial', DLG), 0.8, at=c.A(4, 'caractere', 0.5), label='Pelo menos 1 caractere especial')
    c.mark(5)
    c.hover(BTN('Selecionar foto', DLG), 2.0, at=c.A(5, 'foto,', 0.5), label='Foto do Usuário: Selecionar foto (sem clicar)')
    c.mark(6)
    c.hover(TXT('Permissões', DLG), 1.6, at=c.A(6, 'Agora,', 0.5), label='coluna Permissões (sem clicar)')
    c.fim()
    return c


# setup do cap03: reabre Criar Usuário com nome, e-mail e senha do Marcos (continuação do cap02, fora do vídeo)
REABRE_MARCOS = SETUP_USUARIOS + [
    {'do': 'click', 'target': CRIAR}, {'do': 'waitFor', 'text': 'Preencha os dados do novo usuário', 'timeout': 10},
    {'do': 'type', 'target': SEL('#fullName'), 'text': 'Marcos Antunes', 'cps': 60},
    {'do': 'type', 'target': SEL('#email'), 'text': EMAIL_MARCOS, 'cps': 60},
    {'do': 'type', 'target': SEL('#password'), 'text': SENHA_MARCOS, 'cps': 60},
    {'do': 'waitFor', 'text': 'Senha forte. Deve conter:', 'timeout': 5},
    {'do': 'scroll', 'point': {'x': 1000, 'y': 140}, 'by': 0, 'duration': 0.2, 'after': 0},
]


def cap03():
    """Os três perfis rápidos: Acesso Total, Somente Visualização e Operador Padrão (fica); Criar Usuário: 2 / 3 usuários."""
    c = cap_novo(3, setup=REABRE_MARCOS, start=(1000, 140))
    c.mark(1)
    c.hover(TXT('Permissões', DLG), 1.0, at=c.A(1, 'permissões.', 0.5), label='coluna Permissões')
    c.hover(TXT('Perfis rápidos', DLG), 1.2, at=c.A(1, 'perfis', 0.5), label='Perfis rápidos')
    c.mark(2)
    # sob a ilustração dos chaveiros: o corpo da janela desce e a lista de permissões aparece inteira (368 px)
    c.ev(js_corpo_abaixo(600), at=c.L(2) + 0.6, label='desce o corpo da janela (sob a ilustração)')
    c.mark(3)
    c.click(CHIP('Acesso Total'), at=c.A(3, 'Acesso', 0.6), label='perfil Acesso Total')
    c.mark(4)
    c.click(CHIP('Somente Visualização'), at=c.A(4, 'Somente', 0.6), label='perfil Somente Visualização')
    c.mark(5)
    c.click(CHIP('Operador Padrão'), at=c.A(5, 'Operador', 0.6), label='perfil Operador Padrão (fica)')
    c.confere_js(js_estado('Acesso à tela Caixa', 'Acesso à tela Pedidos', 'Acesso à tela Estoque', 'Acesso à tela Ticket de Pesagem',
                           '-Acesso à tela Dashboard'), 'Operador Padrão: Caixa, Pedidos, Estoque e Ticket ligados')
    # a lista desce devagar: Caixa, Pedidos (compra e venda), Estoque e Ticket de Pesagem, ligados (duas rolagens: os quatro não
    # cabem juntos nos 368 px da lista)
    c.hover(TELA('Caixa'), 0.2, at=c.A(5, 'caixa,', 0.5), label='Caixa ligado')
    c.ev(js_lista('Acesso à tela Pedidos', 420, 450), at=c.A(5, 'caixa,', -0.2), label='a lista desce até Pedidos')
    c.hover(TELA('Pedidos'), 0.2, at=c.A(5, 'compra', 0.0), label='Pedidos ligado (compra e venda)')
    c.ev(js_lista('Acesso à tela Estoque', 400, 450), at=c.A(5, 'estoque', 0.9), label='a lista desce até Estoque')
    c.hover(TELA('Estoque'), 0.2, at=c.A(5, 'estoque', 0.4), label='Estoque ligado')
    c.hover(TELA('Ticket de Pesagem'), 1.0, at=c.A(5, 'ticket', 0.45), label='Ticket de Pesagem ligado')
    c.mark(6)
    c.hover(TXT('Ticket de Pesagem', DLG), 0.8, at=c.A(6, 'Marcos.', 0.5), label='o que serve pro Marcos')
    c.hover(TELA('Ticket de Pesagem'), 1.0, at=c.A(6, 'chave', 0.5, nth=0), label='chave por chave (o interruptor)')
    c.mark(7)
    c.click(CRIAR_DLG, at=c.A(7, 'Criar', 0.6), label='Criar Usuário (rodapé da janela)')
    c.waitfor(target=TXT('Marcos Antunes'), timeout=12)
    c.confere('main', ['2 / 3 usuários', 'Marcos Antunes', '32 permissões · Ativo'], 'Marcos na lista, ativo, e o selo 2 / 3')
    c.hover(LINHA('Marcos Antunes'), 0.6, at=c.A(7, 'Marcos', 0.5), label='Marcos na lista')
    c.hover(TXT('32 permissões · Ativo'), 0.8, at=c.A(7, 'ativo.', 0.5), label='32 permissões · Ativo')
    c.fim()
    return c


def cap04():
    """Telas e ações: a Juliana montada na mão (7 telas e 8 ações, sem o Caixa); Criar Usuário: 3 / 3 usuários.
    Posições da lista (corpo da janela embaixo; lista de 286 a 654): interruptor de cada tela no conteúdo da lista (tudo fechado)
    Ver Totais 41, Dashboard 139, Caixa 206, Histórico do Caixa 272, Movimentações Bancárias 339, Relatório Financeiro 416,
    Contas a Pagar/Receber 493, Pedidos 646, Fiscal & Ambiental 723, Estoque 846, Ticket de Pesagem 1035, Clientes e
    Fornecedores 1290; as ações abertas somam ~218 px (banco, 3) e ~229 px (contas, 4). A busca refaz a lista e fecha as ações."""
    c = cap_novo(4, start=(1000, 360))
    c.mark(1)
    c.click(CRIAR, at=0.4, label='Criar Usuário')
    c.waitfor(text='Preencha os dados do novo usuário', timeout=10)
    c.click(SEL('#fullName'), label='campo Nome Completo')
    c.type(SEL('#fullName'), 'Juliana Prado', noClick=True, cps=30, label='Nome Completo: Juliana Prado')
    c.click(SEL('#email'), label='campo Email')
    c.ev(js_colar(EMAIL_JULIANA), label='Email da Juliana (colado: 39 letras não cabem na fala)')
    c.click(SEL('#password'), label='campo Senha')
    c.type(SEL('#password'), SENHA_JULIANA, noClick=True, cps=30, label='Senha (Senha forte)')
    c.confere('dlg', ['Senha forte'], 'Senha forte da Juliana')
    c.mark(2)
    c.ev(js_corpo_abaixo(700), at=c.A(2, 'lista', 0.5), label='desce o corpo da janela: a lista aparece inteira')
    c.hover(TXT('Geral', DLG), 0.3, at=c.A(2, 'separada', 0.4), label='grupo Geral')
    c.hover(TXT('Financeiro', DLG), 0.2, at=c.A(2, 'grupos.', 0.5), label='grupo Financeiro')
    c.ev(js_rola_texto('Cadastros', 330, 1600), label='a lista desce pelos grupos (Materiais, Cadastros)')
    c.hover(TXT('Clientes e Fornecedores', DLG), 0.4, at=c.A(2, 'sistema,', 0.5), label='uma linha = uma tela (Clientes e Fornecedores)')
    c.hover(TELA('Clientes e Fornecedores'), 1.0, at=c.A(2, 'interruptor', 0.5), label='o interruptor do lado')
    c.mark(3)
    # sob a ilustração da porta: a lista volta até Contas a Pagar/Receber
    c.ev(js_lista('Acesso à tela Contas a Pagar/Receber', 330, 900), at=c.L(3) + 0.8, label='a lista volta até Contas a Pagar/Receber (sob a ilustração)')
    c.mark(4)
    c.click(TELA('Contas a Pagar/Receber'), at=c.A(4, 'Contas', 0.6), label='liga a tela Contas a Pagar/Receber')
    c.click(VER('Contas a Pagar/Receber'), at=c.A(4, 'Abro', 0.6), label='Clique para ver 4 ações (Contas a Pagar/Receber)')
    c.click(SW('Criar Conta a Pagar/Receber'), at=c.A(4, 'Criar', 0.6), label='liga Criar Conta a Pagar/Receber')
    c.click(SW('Dar Baixa em Conta'), at=c.A(4, 'Dar', 0.6), label='liga Dar Baixa em Conta')
    c.confere_js(js_selo('Contas a Pagar/Receber', '2/4'), 'selo 2/4')
    c.hover(CONTADOR('Contas a Pagar/Receber'), 1.8, at=c.A(4, 'contador', 0.5), label='ZOOM selo 2/4 e as duas ações ligadas')
    c.mark(5)
    c.hover(TELA('Contas a Pagar/Receber'), 0.8, at=c.A(5, 'tela,', 0.5, nth=0), label='primeiro a tela (interruptor de Contas a Pagar/Receber)')
    c.hover(SW('Criar Conta a Pagar/Receber'), 0.8, at=c.A(5, 'ações.', 0.5), label='depois as ações')
    c.ev(js_lista('Acesso à tela Caixa', 400, 700), at=c.A(5, 'tela.', 0.0, nth=1), label='a lista sobe até o Caixa')
    c.hover(TELA('Caixa'), 1.6, at=c.A(5, 'Caixa', 0.5, nth=0), label='a tela Caixa, desligada (sem abrir as ações)')
    c.mark(6)
    c.click(BUSCA, at=c.A(6, 'busca.', 0.6), label='Buscar tela ou ação...')
    c.type(BUSCA, 'nota', at=c.A(6, 'nota,', 0.05), noClick=True, cps=12, label='busca: nota')
    c.hover(TXT('Fiscal & Ambiental', DLG), 0.4, at=c.A(6, 'Fiscal', 0.5), label='aparece o Fiscal & Ambiental')
    c.click(TELA('Fiscal & Ambiental'), at=c.A(6, 'tela', 0.6), label='liga a tela Fiscal & Ambiental')
    c.click(VER('Fiscal & Ambiental'), at=c.A(6, 'ações', 0.6), label='Clique para ver 4 ações (Fiscal & Ambiental)')
    c.click(SW('Emitir NF-e (Produto)'), at=c.A(6, 'NF-e', 0.6), label='liga Emitir NF-e (Produto)')
    c.click(SW('Emitir NFS-e (Serviço)'), at=c.A(6, 'NFS-e.', 0.6), label='liga Emitir NFS-e (Serviço)')
    c.mark(7)
    c.click(LIMPAR, at=c.A(7, 'mesmo', 0.6), label='Limpar busca')
    c.ev(js_liga('Ver Totais e Valores Financeiros', 'Acesso à tela Dashboard'), at=c.A(7, 'resto', 0.4), label='liga Ver Totais e Dashboard (sem cursor)')
    c.ev(js_lista('Acesso à tela Movimentações Bancárias', 300, 450), at=c.A(7, 'escritório:', 0.5), label='a lista desce até o banco')
    c.click(TELA('Movimentações Bancárias'), at=c.A(7, 'banco,', 0.6), label='liga Movimentações Bancárias (o banco)')
    c.ev(js_abre_acoes('Movimentações Bancárias'), label='abre as ações do banco (sem cursor)')
    c.ev(js_liga('Gerenciar Contas Bancárias', 'Conciliar Extrato Bancário'), label='liga Gerenciar Contas e Conciliar Extrato (sem cursor)')
    c.click(TELA('Relatório Financeiro'), at=c.A(7, 'relatório', 0.6), label='liga Relatório Financeiro')
    c.ev(js_lista('Acesso à tela Pedidos', 400, 400), label='a lista desce até Pedidos')
    c.click(TELA('Pedidos'), at=c.A(7, 'pedidos', 0.6), label='liga Pedidos')
    c.ev(js_lista('Acesso à tela Clientes e Fornecedores', 400, 500), label='a lista desce até Clientes e Fornecedores')
    c.click(TELA('Clientes e Fornecedores'), at=c.A(7, 'clientes', 0.6), label='liga Clientes e Fornecedores')
    c.ev(js_abre_acoes('Clientes e Fornecedores'), label='abre as ações de Clientes e Fornecedores (sem cursor)')
    c.ev(js_liga('Ver saldos de cliente/fornecedor'), label='liga Ver saldos de cliente/fornecedor (sem cursor)')
    c.ev(js_lista('Acesso à tela Caixa', 400, 700), at=c.A(7, 'Caixa', 1.0), label='a lista sobe até o Caixa')
    c.hover(TELA('Caixa'), 1.2, at=c.A(7, 'Caixa', 0.3), label='o Caixa fica desligado')
    # as ações só existem na tela com a tela aberta: aqui confere as 7 telas e o Ver Totais; as 15 permissões, na lista depois de criar
    c.confere_js(js_estado('Acesso à tela Contas a Pagar/Receber', 'Acesso à tela Fiscal & Ambiental', 'Ver Totais e Valores Financeiros',
                           'Acesso à tela Dashboard', 'Acesso à tela Movimentações Bancárias', 'Acesso à tela Relatório Financeiro',
                           'Acesso à tela Pedidos', 'Acesso à tela Clientes e Fornecedores', '-Acesso à tela Caixa'), 'as 7 telas da Juliana, sem o Caixa')
    c.mark(8)
    c.mark(9)
    c.mark(10)
    c.click(CRIAR_DLG, at=c.A(10, 'Criar', 0.6), label='Criar Usuário (rodapé da janela)')
    c.waitfor(target=TXT('Juliana Prado'), timeout=12)
    c.confere('main', ['3 / 3 usuários', 'Juliana Prado', '15 permissões · Ativo'], 'Juliana na lista (15 permissões) e o selo 3 / 3')
    c.hover(LINHA('Juliana Prado'), 0.3, at=c.A(10, 'Juliana', 0.5), label='Juliana entra na equipe')
    c.hover(SELO('3 / 3 usuários'), 0.6, at=c.A(10, 'equipe.', 0.4), label='selo 3 / 3 usuários')
    c.fim()
    return c


def cap05():
    """O balanceiro e o escritório: Editar do Marcos (foto, tela inicial Caixa, sem Ver Projeção de Lucro: Personalizado), Atualizar;
    o detalhe da Juliana (Telas (7), Ações (8), sem Caixa)."""
    c = cap_novo(5, start=(560, 470))
    c.mark(1)
    c.click(LINHA('Marcos Antunes'), at=c.A(1, 'balanceiro:', 0.6), label='clica no Marcos')
    c.waitfor(target=TXT('Perfil de acesso'), timeout=8)
    c.click(EDITAR, at=c.A(1, 'Marcos', 0.6), label='Editar (detalhe do Marcos)')
    c.waitfor(text='Atualize os dados e permissões deste usuário', timeout=10)
    c.confere('dlg', ['Editar Usuário', 'Operador Padrão', 'Nova Senha (opcional)'], 'Editar Usuário com o Operador Padrão marcado')
    c.mark(2)
    c.upload(BTN('Selecionar foto', DLG), FOTO_MARCOS, at=c.A(2, 'foto', 0.9), label='Selecionar foto: marcos-antunes.jpg')
    c.waitfor(text='Foto atualizada com sucesso!', timeout=10)
    c.mark(3)
    c.click(SEL(f'{DLG} #initial-screen'), at=c.A(3, 'Tela', 0.6), label='Tela inicial (Automática)')
    c.click({'role': 'option', 'name': 'Caixa', 'exact': True}, at=c.A(3, 'Caixa.', 0.6, nth=0), label='Tela inicial: Caixa')
    c.mark(4)
    # o corpo da janela desce: Nova Senha, os perfis, a busca e a lista ficam juntos (com o corpo no alto, a ação do Caixa cairia
    # embaixo da borda da janela e o robô rolaria com a roda)
    c.ev(js_corpo_abaixo(600), at=c.L(4) - 0.1, label='desce o corpo da janela')
    c.hover(SEL(f'{DLG} #password'), 1.4, at=c.A(4, 'Nova', 0.5), label='Nova Senha (opcional) (sem digitar)')
    c.mark(5)
    c.click(BUSCA, at=c.A(5, 'Busco', 0.6), label='Buscar tela ou ação...')
    c.type(BUSCA, 'lucro', at=c.A(5, 'lucro,', 0.05, nth=0), noClick=True, cps=20, label='busca: lucro')
    c.click(VER('Caixa'), at=c.A(5, 'aparece', 0.0), label='Clique para ver 1 ação (Caixa)')
    c.hover(ACAO('Ver Projeção de Lucro'), 1.6, at=c.A(5, 'Projeção', 0.4), label='aparece o Ver Projeção de Lucro, dentro do Caixa')
    c.click(SW('Ver Projeção de Lucro'), at=c.A(5, 'Desligo.', 0.6), label='desliga Ver Projeção de Lucro')
    c.mark(6)
    c.confere_js("(()=>{const p=document.querySelector('[role=dialog] span.bg-amber-500');const a=[...document.querySelectorAll('[role=dialog] button.bg-primary')]"
                 ".filter(b=>['Acesso Total','Operador Padrão','Somente Visualização'].includes(b.textContent.trim()));"
                 "return (p&&!a.length?'OK: ':'DIFERENTE: ')+'Personalizado '+!!p+', perfis marcados '+a.length})()", 'perfil virou Personalizado')
    c.hover(PERSONALIZADO, 1.2, at=c.A(6, 'Personalizado.', 0.5), label='ZOOM Perfis rápidos com o selo Personalizado')
    c.hover(CHIP('Operador Padrão'), 1.0, at=c.A(6, 'Operador', 0.5), label='Operador Padrão (desmarcado)')
    c.mark(7)
    c.click(BTN('Atualizar', DLG), at=c.A(7, 'Atualizar.', 0.6), label='Atualizar')
    c.waitfor(text='Permissões atualizadas!', timeout=12)
    c.confere('body', ['Permissões atualizadas! O usuário precisa fazer login novamente para ver as mudanças.'], 'aviso de permissões')
    c.waitfor(target=TXT('31 permissões · Ativo'), timeout=10)
    c.hover(LINHA('Marcos Antunes'), 1.2, at=c.A(7, 'continua', 0.5), label='Marcos na lista: foto e 31 permissões')
    c.mark(8)
    c.click(LINHA('Juliana Prado'), at=c.A(8, 'escritório.', 0.6), label='clica na Juliana')
    c.waitfor(target=TXT('Telas (7)'), timeout=8)
    c.confere('main', ['Personalizado', '15 permissões configuradas individualmente.', 'Telas (7)', 'Ações (8)'], 'detalhe da Juliana')
    # o detalhe rola por dentro (406 a 800 na tela; a lista de telas começa em y 720): sobe "Telas (7)" para y 420
    c.ev(js_rola_texto('Telas (7)', 420, 500, MAIN), at=c.A(8, 'escritório.', -0.3), label='o detalhe desce até Telas (7)')
    c.hover(TXT('Contas a Pagar/Receber'), 0.2, at=c.A(8, 'contas,', 0.5), label='Contas a Pagar/Receber (as contas)')
    c.hover(TXT('Movimentações Bancárias'), 0.2, at=c.A(8, 'banco,', 0.5), label='Movimentações Bancárias (o banco)')
    c.hover(TXT('Relatório Financeiro'), 0.2, at=c.A(8, 'relatório', 0.5), label='Relatório Financeiro')
    c.ev(js_rola_texto('Telas (7)', 330, 350, MAIN), at=c.A(8, 'relatório', -0.35), label='o detalhe desce mais um pouco (Fiscal & Ambiental)')
    c.hover(TXT('Fiscal & Ambiental'), 2.0, at=c.A(8, 'notas.', 0.5), label='Fiscal & Ambiental (as notas); a lista não tem o Caixa')
    c.fim()
    return c


def menu(c, nome, item, at=None, label=None):
    """passa o mouse no "..." do detalhe (abre o menu) e clica no item; um 2o hover só se o menu ainda não abriu"""
    c.hover(ACOES(nome), 0.35, at=at, label=label or f'menu ... de {nome}', optional=False, timeout=8)
    c.hover(ACOES(nome), 0.3, label=f'menu ... de {nome} de novo (só se não abriu)', unless=ITEM(item))
    c.waitfor(target=ITEM(item), timeout=6)


def cap06():
    """Desativar ou excluir: menu do Marcos, Desativar (2 / 3), Ativar (3 / 3), Excluir (pede o e-mail) > Cancelar; a coroa do Rafael."""
    c = cap_novo(6, start=(560, 470))
    c.mark(1)
    c.click(LINHA('Marcos Antunes'), at=c.A(1, 'alguém', 0.6), label='clica no Marcos')
    c.waitfor(target=TXT('Perfil de acesso'), timeout=8)
    menu(c, 'Marcos Antunes', 'Desativar', at=c.A(1, 'menu', 0.5), label='menu ... do Marcos (Tornar master, Desativar, Excluir)')
    c.hover(ITEM('Desativar'), 0.25, at=c.A(1, 'desativar', 0.5), label='Desativar')
    c.hover(ITEM('Excluir'), 0.2, at=c.A(1, 'excluir.', 0.65), label='Excluir')
    c.mark(2)
    c.add({'do': 'scroll', 'point': {'x': 980, 'y': 600}, 'by': 0, 'duration': 0.3, 'after': 0, 'at': round(c.L(2) + 0.3, 2), 'label': 'cursor sai do menu (fecha)'})
    c.mark(3)
    menu(c, 'Marcos Antunes', 'Desativar', at=c.A(3, 'Desativo', 1.2), label='menu ... do Marcos')
    c.click(ITEM('Desativar'), at=c.A(3, 'Desativo', 0.3), label='Desativar')
    c.waitfor(text='Usuário desativado!', timeout=8)
    c.waitfor(target=SELO('2 / 3 usuários'), timeout=8)
    c.confere('main', ['Inativo', 'A conta está impedida de entrar.', '2 / 3 usuários', '31 permissões · Inativo'], 'Marcos inativo e o selo 2 / 3')
    c.hover(TXT('A conta está impedida de entrar.'), 1.0, at=c.A(3, 'acesso,', 0.5), label='A conta está impedida de entrar.')
    c.hover(SELO('2 / 3 usuários'), 2.4, at=c.A(3, 'contador:', 0.5), label='ZOOM selo 2 / 3 usuários')
    c.mark(4)
    menu(c, 'Marcos Antunes', 'Ativar', at=c.A(4, 'mesmo', 0.6), label='menu ... do Marcos')
    c.click(ITEM('Ativar'), at=c.A(4, 'Ativar.', 0.4), label='Ativar')
    c.waitfor(text='Usuário ativado!', timeout=8)
    c.waitfor(target=SELO('3 / 3 usuários'), timeout=8)
    c.hover(SELO('3 / 3 usuários'), 0.4, at=c.A(4, 'Marcos', 0.5), label='selo 3 / 3 usuários (de volta)')
    c.mark(5)
    menu(c, 'Marcos Antunes', 'Excluir', at=c.A(5, 'Excluir', 1.2), label='menu ... do Marcos')
    c.click(ITEM('Excluir'), at=c.A(5, 'Excluir', 0.1), label='Excluir')
    c.waitfor(text='Esta ação é irreversível', timeout=8)
    c.confere(ALERTA, ['Excluir usuário', 'Esta ação é irreversível', 'Para confirmar, digite o email do usuário:'], 'janela Excluir usuário')
    c.confere_js("(()=>{const b=[...document.querySelectorAll('[role=alertdialog] button')].find(x=>x.textContent.trim()==='Excluir Usuário');"
                 "return b?(b.disabled?'OK: Excluir Usuário apagado':'DIFERENTE: Excluir Usuário ligado'):'DIFERENTE: sem o botão'})()", 'Excluir Usuário apagado')
    c.hover(SEL('#confirmEmail'), 1.4, at=c.A(5, 'e-mail', 0.5), label='Email de confirmação')
    c.mark(6)
    c.click(BTN('Cancelar', ALERTA), at=c.A(6, 'cancelo.', 0.6), label='Cancelar')
    c.waitfor(gone=SEL(ALERTA), timeout=8)
    c.mark(7)
    c.hover(COROA, 1.6, at=c.A(7, 'master.', 0.5, nth=0), label='coroa do Rafael (o master)')
    c.mark(8)
    c.hover(LINHA('Rafael Nogueira'), 1.0, at=c.A(8, 'master', 0.5), label='Rafael na lista')
    c.fim()
    return c


def cap07():
    """Passar o controle: o Rafael (master); menu da Juliana > Tornar master > Passar o controle da empresa? > Cancelar."""
    c = cap_novo(7, start=(560, 470))
    c.mark(1)
    c.click(LINHA('Rafael Nogueira'), at=c.A(1, 'master?', 0.3), label='clica no Rafael')
    c.waitfor(target=TXT('Perfil de acesso'), timeout=8)
    c.hover(TXT('Master'), 1.6, at=c.A(1, 'responsável', 0.5), label='selo Master')
    c.hover(COROA, 1.0, at=c.A(1, 'exclui', 0.5), label='coroa na lista')
    c.mark(2)
    # sob a ilustração do bastão: abre o detalhe da Juliana
    c.click(LINHA('Juliana Prado'), at=c.A(2, 'serve', 0.6), label='clica na Juliana (sob a ilustração)')
    c.waitfor(target=TXT('Telas (7)'), timeout=8)
    c.mark(3)
    menu(c, 'Juliana Prado', 'Tornar master', at=c.A(3, 'menu', 0.5), label='menu ... da Juliana')
    c.click(ITEM('Tornar master'), at=c.A(3, 'Tornar', 0.6), label='Tornar master')
    c.waitfor(text='Passar o controle da empresa?', timeout=8)
    c.confere(ALERTA, ['Passar o controle da empresa?', 'Você vai tornar Juliana Prado o novo master da empresa.',
                                     'você deixará de ser o master', 'Esta ação é imediata.', 'Sim, passar o bastão'], 'janela Passar o controle')
    c.hover(SEL(f'{ALERTA} h2'), 0.8, at=c.A(3, 'janela', 0.5), label='Passar o controle da empresa?')
    c.hover(SEL(f'{ALERTA} p'), 1.2, at=c.A(3, 'controle', 0.5), label='o texto explica o que muda')
    c.mark(4)
    c.marcar(SEL(f'{ALERTA} p'), at=c.A(4, 'Você', 0.0, nth=1), label='ZOOM você deixará de ser o master (mantém as permissões, perde a proteção)')
    c.hover(SEL(f'{ALERTA} p'), 1.2, at=c.A(4, 'permissões,', 0.5), label='mantém suas permissões atuais')
    c.hover(SEL(f'{ALERTA} p'), 1.6, at=c.A(4, 'proteção:', 0.5), label='nem ficará protegido contra exclusão')
    c.mark(5)
    c.click(BTN('Cancelar', ALERTA), at=c.A(5, 'cancelo,', 0.6), label='Cancelar')
    c.waitfor(gone=SEL(ALERTA), timeout=8)
    c.hover(COROA, 1.0, at=c.A(5, 'master.', 0.5), label='o Rafael continua master (coroa)')
    c.fim()
    return c


def cap08():
    """O limite de usuários: selo 3 / 3; Criar Usuário abre "Sua equipe cresceu!"; + e - nos usuários extras; Cancelar."""
    c = cap_novo(8, start=(700, 470))
    c.mark(1)
    c.confere('main', ['3 / 3 usuários', 'Juliana Prado', 'Marcos Antunes', 'Rafael Nogueira'], 'selo 3 / 3 e os três usuários')
    c.hover(SELO('3 / 3 usuários'), 2.0, at=c.A(1, 'número', 0.5), label='ZOOM selo 3 / 3 usuários')
    c.hover(SELO('3 / 3 usuários'), 0.6, at=c.A(1, 'três', 0.5, nth=0), label='três de três')
    c.hover(LINHA('Rafael Nogueira'), 0.3, at=c.A(1, 'Rafael,', 0.5), label='o Rafael')
    c.hover(LINHA('Juliana Prado'), 0.3, at=c.A(1, 'Juliana', 0.5), label='a Juliana')
    c.hover(LINHA('Marcos Antunes'), 0.15, at=c.A(1, 'Marcos.', 0.6), label='o Marcos')
    c.mark(2)
    c.mark(3)
    c.click(CRIAR, at=c.A(3, 'Criar', 0.6), label='Criar Usuário (sem vaga)')
    c.waitfor(text='Sua equipe cresceu!', timeout=8)
    c.confere('dlg', ['Sua equipe cresceu!', '3 / 3', 'Usuários cadastrados', 'Adicionar usuários extras', 'Novo limite de usuários:',
                      '4 usuários', 'Seu plano será convertido para Personalizado'], 'janela do limite')
    c.mark(4)
    c.hover(TXT('Usuários cadastrados', DLG), 0.3, at=c.A(3, 'janela.', 0.5), label='3 / 3 Usuários cadastrados')
    c.hover(TXT('Adicionar usuários extras', DLG), 0.25, at=c.A(4, 'escolhe', 0.5), label='Adicionar usuários extras')
    c.click(SEL(f'{DLG} button:has(svg.lucide-plus)'), at=c.A(4, 'quantos', 0.5), label='+ (2 usuários)')
    c.click(SEL(f'{DLG} button:has(svg.lucide-minus)'), at=c.A(4, 'quer.', 0.6), label='- (1 usuário)')
    c.hover(TXT('Novo limite de usuários:', DLG), 1.6, at=c.A(4, 'extra', 0.5), label='Novo limite de usuários: 4 usuários')
    c.hover(SEL(f'{DLG} p:has(> span.font-medium)'), 0.5, at=c.A(4, 'estimativa.', 0.5), label='Seu plano será convertido para Personalizado')
    c.mark(5)
    # os botões da janela do limite ficam em y 714..754, fora da faixa de clique do robô (96..730): noScroll
    c.hover(BTN('Continuar', DLG), 1.4, at=c.A(5, 'Continuar', 0.5), label='Continuar (sem clicar)', noScroll=True)
    c.click(BTN('Cancelar', DLG), at=c.A(5, 'cancelo.', 0.6), label='Cancelar', noScroll=True)
    c.waitfor(gone=SEL('[role=dialog]'), timeout=8)
    c.fim()
    return c


def cap09():
    """Esconder o valor: Editar do Marcos; Geral > Ver Totais e Valores Financeiros; Caixa (Ver Dinheiro Total ligado, Projeção de Lucro
    desligada); Ticket de Pesagem (Criar Ticket de Pesagem com Valores desligado); Cancelar."""
    c = cap_novo(9, start=(560, 470))
    c.mark(1)
    c.click(LINHA('Marcos Antunes'), at=0.3, label='clica no Marcos')
    c.waitfor(target=TXT('Perfil de acesso'), timeout=8)
    c.click(EDITAR, at=c.A(1, 'valores.', 0.6, nth=0), label='Editar (detalhe do Marcos)')
    c.waitfor(text='Atualize os dados e permissões deste usuário', timeout=10)
    c.ev(js_corpo_abaixo(600), at=c.A(1, 'topo', -0.6), label='desce o corpo da janela: Geral no topo da lista')
    c.hover(TXT('Geral', DLG), 0.6, at=c.A(1, 'Geral,', 0.5), label='grupo Geral')
    c.hover(ACAO('Ver Totais e Valores Financeiros'), 3.0, at=c.A(1, 'Ver', 0.5), label='ZOOM Ver Totais e Valores Financeiros (ligado)')
    for i in (2, 3, 4):
        c.mark(i)
    # sob a ilustração (o que some e o que fica): abre as ações do Caixa e põe as duas de valor no meio da lista
    c.ev(js_abre_acoes('Caixa'), at=c.L(3), label='abre as ações do Caixa (sob a ilustração)')
    c.ev(js_lista('Ver Dinheiro Total em Caixa', 380, 600), label='a lista desce até os valores do caixa (sob a ilustração)')
    c.confere_js(js_estado('Ver Totais e Valores Financeiros', 'Ver Dinheiro Total em Caixa', '-Ver Projeção de Lucro'), 'valores do Marcos')
    c.mark(5)
    c.hover(ACAO('Ver Dinheiro Total em Caixa'), 1.2, at=c.A(5, 'ligados,', 0.5), label='Ver Dinheiro Total em Caixa (ligado)')
    c.hover(ACAO('Ver Projeção de Lucro'), 1.6, at=c.A(5, 'projeção', 0.5), label='Ver Projeção de Lucro (desligado)')
    c.mark(6)
    c.ev(js_lista('Acesso à tela Ticket de Pesagem', 330, 900), at=c.A(6, 'pesa,', 0.3), label='a lista desce até o Ticket de Pesagem')
    c.click(VER('Ticket de Pesagem'), at=c.A(6, 'Ticket', 0.6), label='Clique para ver 4 ações (Ticket de Pesagem)')
    c.confere_js(js_estado('-Criar Ticket de Pesagem com Valores'), 'Criar Ticket de Pesagem com Valores desligado')
    c.mark(7)
    c.hover(ACAO('Criar Ticket de Pesagem com Valores'), 3.0, at=c.A(7, 'Criar', 0.5), label='ZOOM Criar Ticket de Pesagem com Valores (desligado)')
    c.mark(8)
    c.click(BTN('Cancelar', DLG), at=c.A(8, 'cancelo.', 0.6), label='Cancelar (nada muda)')
    c.waitfor(gone=SEL('[role=dialog]'), timeout=8)
    c.fim()
    return c


def cap10():
    """Recapitulando: passeio calmo pela aba com os três (base para a montagem dos trechos dos capítulos 2 a 9)."""
    c = cap_novo(10, start=(760, 300))
    c.mark(1)
    c.hover(ABA_USUARIOS, 1.0, at=c.A(1, 'aba', 0.5), label='aba Usuários e Permissões')
    c.hover(TXT('Gerencie usuários da empresa, papéis e permissões de acesso'), 0.8, at=c.A(1, 'Gerenciar', 0.5), label='Gerenciar Usuários')
    c.mark(2)
    c.click(LINHA('Marcos Antunes'), at=c.A(2, 'Marcos', 0.6), label='o Marcos')
    c.hover(TXT('Perfil de acesso'), 0.6, at=c.A(2, 'deu', 0.5), label='perfil do Marcos')
    c.mark(3)
    c.click(LINHA('Juliana Prado'), at=c.A(3, 'Juliana,', 0.6), label='a Juliana (montada na mão)')
    c.hover(SEL("main p:has-text('permissões configuradas individualmente')"), 0.6, at=c.A(3, 'tela', 0.5, nth=0), label='15 permissões, tela por tela')
    c.mark(4)
    c.click(LINHA('Marcos Antunes'), at=c.A(4, 'Marcos', 0.6), label='o Marcos (foto e 31 permissões)')
    c.mark(5)
    c.hover(ACOES('Marcos Antunes', 0), 0.3, at=c.A(5, 'Desativou', 0.5), label='menu ... (desativar e ativar)')
    c.hover(COROA, 1.0, at=c.A(5, 'controle', 0.5), label='a coroa do master')
    c.mark(6)
    c.hover(SELO('3 / 3 usuários'), 1.6, at=c.A(6, 'limite', 0.5), label='selo 3 / 3 usuários')
    c.mark(7)
    c.add({'do': 'scroll', 'point': {'x': 960, 'y': 600}, 'by': 0, 'duration': 0.4, 'after': 0, 'at': c.A(7, 'próximo', 0.4), 'label': 'cursor descansa'})
    c.fim()
    return c


CAPS_ROBO = {n: globals()[f'cap{n:02d}'] for n in range(11)}

if __name__ == '__main__':
    quais = [int(a) for a in sys.argv[1:]] or sorted(CAPS_ROBO)
    for n in quais:
        c = CAPS_ROBO[n]()
        if os.environ.get('ANCORAS'):
            for i, w, t in c.anchors:
                print(f'   âncora L{i} "{w}" -> {t}')
        d = c.out()
        last = -1
        for stp in d['steps']:   # o `at` precisa ser crescente
            if 'at' in stp:
                if stp['at'] < last:
                    print(f'  aviso cap{n:02d}: at {stp["at"]} < {last} em "{stp.get("label") or stp.get("name")}"')
                last = max(last, stp['at'])
        path = os.path.join(HERE, f'cap{n:02d}.json')
        with open(path + '.tmp', 'w', encoding='utf-8') as f:   # troca atômica: um record.mjs na fila pode abrir o arquivo agora
            json.dump(d, f, ensure_ascii=False, indent=1)
        os.replace(path + '.tmp', path)
        print(f'cap{n:02d}: {len(d["steps"])} passos, narração {c.dur:.1f} s{" (ESTIMADA)" if c.estimado else ""} -> {os.path.relpath(path, HERE)}')
