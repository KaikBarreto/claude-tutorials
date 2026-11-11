#!/usr/bin/env python3
"""T03 · gera rec/t03/capNN.json (roteiros do robô) a partir da voz (t03/narracao/capNN.json). Aula-molde da trilha EcoFlix.

EcoSistema 1.59.154 no COMPUTADOR (janela 1280x800), Recicla Vale Metais, Rafael Nogueira (MASTER), FAKE_NOW 10/11/2026 08:30 (todos os
capítulos). Uso, de qualquer pasta:  python3 -I rec/t03/gerar.py [NN ...] [1b]   (sem argumento: todos, mais o corte cap01b)
Depois: ensaio.py NN (rápido) -> record.mjs --rapido -> resumo.py NN --ens -> prever.py NN --ens -> gravação com os tempos -> resumo.py NN.

COMO O GERADOR PRENDE O ROBÔ À FALA (regras que valem para toda aula):
 - A voz é lida de t03/narracao/capNN.json, que hoje é ESTIMADA (tempos_estimados.py, "estimado": true) e amanhã é a do proc.py; o
   gerador confere as palavras de cada linha com o texto atual do tts_textos.py e para se a voz estiver velha (rode preparar_aula.sh).
 - Todo gesto que a fala cita tem `w=(linha, 'palavra'[, nth])`: at = início da palavra - folga do gesto (FOLGA: o tempo medido entre o
   início do passo e o instante em que ele age; o cursor CHEGA na palavra). A palavra casa INTEIRA (sem acento e pontuação) e, se ela
   aparece mais de uma vez na linha, o gerador para até que o `nth` seja dado (T20/T17: prefixo e repetição ancoraram na palavra errada).
 - As marcas L1..Ln entram sozinhas (todas pendentes desde o início, at = início da linha - 0,9): cada uma sai antes do primeiro passo
   cujo `at` já passou dela; passo que começaria até 0,25 s antes da marca (0,8 s num hover) é puxado para ela; hover que atravessa o
   início de uma linha é partido em dois (T14/T15/T21). Nunca se chama mark() à mão.
 - Passo sem `w` corre logo depois do anterior (espera do app, conferência, segundo clique de um menu).
 - `confere*` LÊ a tela e compara com a fala ("OK"/"DIFERENTE", o resumo.py acusa); `OBS` guarda em window.__avisos todo aviso de erro
   do app e o último passo devolve a lista (tem de sair vazia).
 - Ilustração que cobre a janela (roteiro [ILUSTRAÇÃO]): o robô fica parado ou mexe só por `eval` (sem cursor, sem zoom automático).

LOGIN: cada capítulo grava sem sessão pronta ("anonymous": true) e entra pela tela de login no `setup` (fora do vídeo) com "$TUT_USER" e
"$TUT_SENHA" do ambiente (o Supabase falso aceita qualquer senha; o valor nunca vai para arquivo nem log). O `storage` leva as chaves de
"já vi" que a sessão pronta do robô poria (mundo.json, navegador.localStorage). O corte do Marcos (cap01b) entra com o e-mail dele
(dado do mundo fictício) e a mesma "$TUT_SENHA".

PARTICULARIDADES DA 1.59.154 (achadas no ensaio do T03):
 - A 1280 px com o menu lateral aberto a lista de materiais perde "Preço de Venda" e "Ações" (rolagem horizontal): o cap00 recolhe o menu
   na tela (fim da fala dele; a edição põe um aviso) e os outros capítulos já começam com ele recolhido (setup). Menu recolhido abre ao
   passar o mouse: o cursor não passa de x 48 sem querer (start e pontos de descanso longe da borda).
 - Botões fixos fora da faixa y 96..730 do robô: "Salvar" do Editar Preços em Massa (y ~731) leva noScroll; o "Adicionar" do Grupos fica
   abaixo da dobra da janela até a janela rolar (o robô rola a janela no começo da frase).
 - O "Desfazer" da exclusão e o aviso "Preço especial aplicado" somem em 5 s e 2 s: o cursor PARA EM CIMA do aviso (o sonner pausa o
   tempo com o mouse em cima) e o clique vem na palavra.
 - PDF (cap09) abre noutra aba, que o robô não grava (aba única, Chromium sem leitor de PDF): o roteiro guarda o PDF que o app gerou
   (URL.createObjectURL embrulhado no setup) e o devolve no actions.json; t03_pdfs.py extrai para a edição montar a ilustração.

SEMENTES (rec/t03/t03_sementes.py escreve rec/mundo/seeds-extra/t03/): cada capítulo = mundo base + t03/inicio + o apos-capNN do anterior.
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
FAKE_NOW = '2026-11-10T08:30:00-03:00'                        # plano.md (igual no Supabase falso e no robô)
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
            'title': f'T03 · Cap. {s.n}{s.sub} · {NOMES[s.n]} (narração {str(round(s.dur, 1)).replace(".", ",")} s{" ESTIMADA" if s.estimada else ""}{corte}; '
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


# ================================================================ capítulos
def cap00():
    """Abertura: Dashboard; ilustração do cardápio (L1, L2); menu Materiais > Estoque (L3); cartão "Antes" e o menu lateral recolhido (L4)."""
    c = Cap(0, setup_login() + vai('/materiais', 'Gerencie os materiais do estoque') + vai('/dashboard', 'Olá, Rafael!'), start=(700, 140))
    # L1 e L2: a ilustração do cardápio cobre a janela; o robô fica parado no Dashboard
    c.click(BTN('Materiais'), w=(3, 'Materiais,'), label='menu Materiais (abre o grupo)')
    c.click(SEL("a[href='/materiais']"), w=(3, 'Estoque.'), label='Estoque (submenu)')
    c.waitfor(text='Gerencie os materiais do estoque', timeout=15)
    c.confere('main', ['Estoque', 'Tabelas de Preço', 'Principal', 'Movimentar estoque', 'Lista de Materiais'], 'tela Estoque carregada')
    c.hover(P('Gerencie os materiais do estoque'), 0.6, w=(4, 'você'), label='título Estoque (o cursor sai do menu)')
    c.click(TOGGLE_MENU, w=(4, 'antes.'), noScroll=True, label='recolhe o menu lateral (aviso na edição: mais espaço para a lista)')
    c.hover(P('Lista de Materiais'), 0.8, w=(4, 'Vamos'), label='a tela inteira: Lista de Materiais')
    c.fim()
    return c


def cap01():
    """A tela Estoque: coluna das tabelas, barra, cartões (ilustração no L4), lista e colunas, corte do Marcos (cap01b, L6), cabeçalho."""
    c = Cap(1, setup_estoque())
    c.hover(P('Tabelas de Preço'), 0.6, w=(1, 'coluna'), label='coluna Tabelas de Preço')
    c.hover(BTN('Principal'), 0.8, w=(1, 'principal,'), label='Principal com a estrela')
    c.hover(BTN('Nova Tabela'), 0.6, w=(1, 'outra.'), label='Nova Tabela')
    c.hover(BTN('Movimentar estoque'), 0.2, w=(2, 'Movimentar'), label='Movimentar estoque')
    c.hover(BTN('Editar Tabela'), 0.2, w=(2, 'Editar'), label='Editar Tabela')
    c.hover(BTN('Grupos'), 0.15, w=(2, 'Grupos,'), label='Grupos')
    c.hover(BTNX('Exportar'), 0.15, w=(2, 'Exportar'), label='Exportar')
    c.hover(BTN('Zerar Estoque'), 0.6, w=(2, 'Zerar'), label='Zerar Estoque')
    c.hover(P('Peso Total em Estoque'), 1.2, w=(3, 'primeiro'), label='cartão Peso Total em Estoque')
    # L4: ilustração Total Pago x Projeção de Vendas cobre a janela (robô parado)
    c.ev(js_rola_ate('Lista de Materiais', y=110), w=(5, 'Embaixo,', None, 0.6), label='desce até a Lista de Materiais')
    c.hover(TH('Código'), 0.2, w=(5, 'código,'), label='coluna Código')
    c.hover(TH('Nome'), 0.2, w=(5, 'nome,'), label='coluna Nome')
    c.hover(TH('Estoque'), 0.2, w=(5, 'estoque'), label='coluna Estoque Atual')
    c.hover(TH('Preço de Compra'), 0.4, w=(5, 'preços'), label='colunas de preço')
    c.hover(P('estimativa'), 1.2, w=(5, 'estimativa,'), label='selo estimativa do Preço médio pago')
    c.confere('main', ['Código', 'Nome', 'Estoque', 'Valor', 'Preço médio pago', 'estimativa', 'Preço de', 'Compra', 'Venda', 'Ações'], 'colunas da lista')
    # L6: corte para o Marcos (cap01b); aqui a página volta ao topo por baixo do corte, para o L7 começar igual ao corte
    c.ev(js_rola_topo(), w=(6, 'quem'), label='volta ao topo (por baixo do corte do Marcos)')
    c.hover(BTNX('Todos os Materiais'), 0.3, w=(7, 'filtro,'), label='filtro Todos os Materiais')
    c.hover(BTN('Importar planilha'), 0.3, w=(7, 'importação'), label='Importar planilha')
    c.hover(BTNX('Novo Material'), 0.3, w=(7, 'Novo', 0), label='Novo Material')
    c.hover(BUSCA, 0.3, w=(7, 'busca.'), label='busca Buscar material por código ou nome...')
    c.hover(BTNX('Novo Material'), 1.0, w=(7, 'Novo', 1), label='Novo Material (é por ele que a gente começa)')
    c.fim()
    return c


def cap01b():
    """Corte do cap01, linha 6: a mesma tela logada como Marcos Antunes, sem "Ver Totais e Valores Financeiros" (semente
    t03/marcos-sem-valores, SÓ neste corte: o mundo dá a ele a permissão; conflito no relatório). Pesos aparecem; cadeados nos valores."""
    setup = setup_login('marcos.antunes@reciclavalemetais.example', 'Marcos Antunes') + ESTOQUE + RECOLHE
    c = Cap(1, setup, sub='b', user='marcos', voz_de=(6, 6), erros_ok=('Sem permissão',),
            seed_extra=[f'{AULA}/inicio', f'{AULA}/marcos-sem-valores'])
    c.confere('main', ['Peso Total em Estoque', 'Total Pago', 'Sem permissão', 'Projeção de Vendas', '***'], 'cadeados do Marcos nos valores')
    c.hover(P('Peso Total em Estoque'), 1.0, w=(1, 'pesos.'), label='peso total aparece')
    c.hover(P('Sem permissão', nth=0), 1.0, w=(1, 'dinheiro,'), label='cadeado Sem permissão (Total Pago)')
    c.hover(SEL("main tbody tr:first-child td:nth-child(5)"), 1.0, w=(1, 'cadeado.'), label='cadeado *** na coluna Valor Pago')
    c.fim()
    return c


def cap02():
    """Cadastrar um material: Novo Material, abas, nome, unidade, preços, estoque, resumo, Criar, busca; Importar planilha aberto e fechado."""
    c = Cap(2, setup_estoque())
    c.click(BTNX('Novo Material'), w=(1, 'cadastrar'), label='Novo Material')
    c.waitfor(text='Valores e estoque', timeout=10)
    c.hover(TAB('Produção'), 0.8, w=(2, 'Produção', 0), label='aba Produção (sem clicar)')
    c.hover(TAB('Dados'), 0.3, w=(2, 'Dados.'), label='aba Dados')
    c.click(CAMPO('name'), w=(3, 'nome,'), label='campo Nome')
    c.type(CAMPO('name'), 'Radiador de cobre', w=(3, 'pátio:', None, 0.0), clicar=False, cps=30, label='Nome: Radiador de cobre')
    c.click(CAMPO('unit'), w=(3, 'unidade'), label='Unidade (abre a lista)')
    c.hover(OPT('pç — Peça'), 0.5, w=(3, 'peça'), label='pç — Peça (o "fardo" fica abaixo da dobra da lista: rolar custava 2 s)')
    c.click(OPT('Kg — Quilograma'), w=(3, 'aqui.'), label='fica em Kg — Quilograma')
    c.click(CAMPO('purchase_price'), w=(4, 'compra,'), label='P. Compra')
    c.type(CAMPO('purchase_price'), '21,00', w=(4, 'vinte', 0), clicar=False, label='P. Compra 21,00 (zoom: P. Compra e P. Venda)')
    c.click(CAMPO('sale_price'), w=(4, 'venda,'), label='P. Venda')
    c.type(CAMPO('sale_price'), '24,50', w=(4, 'vinte', 1), clicar=False, label='P. Venda 24,50')
    c.click(CAMPO('current_stock'), w=(5, 'quantidade'), label='Quantidade em Estoque')
    c.type(CAMPO('current_stock'), '120', w=(5, 'cento'), clicar=False, label='Quantidade em Estoque 120 (zoom)')
    c.confere('[aria-label="Resumo do material"]', ['Radiador de cobre', '16 · Kg', 'R$ 21,00', 'R$ 24,50', '120 Kg'], 'Resumo: nome, 16 · Kg, preços e estoque')
    c.hover(SEL('[aria-label="Resumo do material"]'), 1.6, w=(6, 'resumo'), label='Resumo do material')
    c.click(BTN('Criar', within=DLG), w=(7, 'Criar,'), label='Criar')
    c.waitfor(text='Material criado!', timeout=10)
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.type(BUSCA, 'radiador', w=(7, 'buscar'), cps=CPS, label='busca radiador')
    c.confere('row:Radiador de cobre', ['16', 'Radiador de cobre', '120', 'R$ 21,00', 'R$ 24,50'], 'linha 16 Radiador de cobre 120 Kg R$ 21,00 R$ 24,50')
    c.ev(js_valor('main input[placeholder="Buscar material por código ou nome..."]', ''), w=(8, 'E', 0, 0.0), label='limpa a busca (sem cursor)')
    c.click(BTN('Importar planilha'), w=(8, 'trazer'), label='Importar planilha')
    c.waitfor(text='Importar materiais por planilha', timeout=8)
    c.hover(BTN('Baixar modelo'), 0.8, w=(8, 'baixa'), label='1. Baixe o modelo: Baixar modelo')
    c.hover(PD('Arraste a planilha aqui ou clique para selecionar'), 1.0, w=(8, 'envia'), label='2. Envie a planilha preenchida')
    c.hover(PD('O sistema confere tudo antes de cadastrar.'), 2.0, w=(9, 'tudo', 0), label='O sistema confere tudo antes de cadastrar.')
    fecha_janela(c, w=(9, 'duplica'), label='fecha a janela sem enviar nada')
    c.fim()
    return c


def cap03():
    """O código do material: busca radiador, código 16 (ilustração nos L2 e L3), Editar, 0-7-0 vira 70, Atualizar."""
    c = Cap(3, setup_estoque())
    c.type(BUSCA, 'radiador', w=(1, 'Agora,', None, 0.9), cps=CPS, label='busca radiador')
    c.waitfor(target=P('Radiador de cobre'), timeout=8)
    c.hover(CELULA('Radiador de cobre', 2), 1.6, w=(1, 'dezesseis'), label='célula Código 16 (zoom)')
    c.confere('row:Radiador de cobre', ['16', 'Radiador de cobre'], 'código 16')
    # L2 e L3: ilustração do código (fichas, caderno); o robô fica parado
    abre_acoes(c, 'Radiador de cobre', 'Editar', w=(3, 'setenta.', None, 0.8), w_item=(4, 'Editar'))   # hover no fim da ilustração do L3
    c.waitfor(text='Editar Material', timeout=8)
    c.click(CAMPO('code'), w=(4, 'digito', None, 1.0), label='campo Código', primeiro=True)
    c.type(CAMPO('code'), '0', w=(4, 'zero', 0, 0.35), clicar=False, clear=True, label='apaga o 16 e digita 0: o campo fica vazio (zoom: Código e Fica assim)')
    c.type(CAMPO('code'), '7', w=(4, 'sete,'), clicar=False, label='digita 7')
    c.type(CAMPO('code'), '0', w=(4, 'zero', 1), clicar=False, label='digita 0: 70')
    c.confere_campos(['70'], 'campo Código 70')
    c.confere('dlg', ['Fica assim: 70'], 'Fica assim: 70')
    c.hover(PD('Fica assim:'), 1.4, w=(5, 'código'), label='Fica assim: 70')
    c.click(BTN('Atualizar', within=DLG), w=(6, 'Atualizar,'), label='Atualizar')
    c.waitfor(text='Material atualizado!', timeout=10)
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.hover(CELULA('Radiador de cobre', 2), 1.4, w=(6, 'setenta.'), label='célula Código 70')
    c.confere('row:Radiador de cobre', ['70', 'Radiador de cobre'], 'código 70')
    c.fim()
    return c


def cap04():
    """O NCM e a nota fiscal: (ilustração L1, por baixo dela o Editar abre sem cursor) NCM pela busca do seletor (7404.00.00),
    Identificação/Produto Fiscal e a ajuda, (ilustrações L6, L7) Atualizar, (ilustração L9)."""
    c = Cap(4, setup_estoque(busca='radiador'))
    c.ev(js_menu_item('Radiador de cobre', 'Editar'), w=(1, 'dentro'), label='abre o Editar do radiador (por baixo da ilustração, sem cursor)')
    c.waitfor(text='Editar Material', timeout=8)
    c.ev(js_rola_ate('Fiscal e organização', y=380, escopo=DLG), w=(2, 'cadastro,', None, 0.3), label='desce até Fiscal e organização')
    c.hover(CAMPO('ncm'), 0.6, w=(2, 'NCM.'), label='NCM (Nota Fiscal), vazio')
    c.hover(SEL(f"{DLG} button[title='Selecionar NCM padrão']"), 0.6, w=(2, 'interrogação'), label='interrogação Selecionar NCM padrão')
    c.click(SEL(f"{DLG} button[title='Selecionar NCM padrão']"), w=(3, 'janela'), label='abre Selecionar NCM para Materiais Recicláveis')
    c.waitfor(text='Selecionar NCM para Materiais Recicláveis', timeout=8)
    c.type({'placeholder': 'Buscar por código NCM ou descrição...'}, 'cobre', w=(3, 'Busco'), cps=CPS, label='busca cobre')
    c.confere('dlg', ['Cobre', '7404.00.00'], 'cartão Cobre 7404.00.00')
    c.click(SEL(f"{DLG} div.space-y-2:has(span:text-is('7404.00.00')) button:has-text('Selecionar')"), w=(3, 'escolho'), label='Selecionar 7404.00.00')
    c.waitfor(gone=TXT('Selecionar NCM para Materiais Recicláveis'), timeout=8)
    c.confere_campos(['7404.00.00'], 'NCM 7404.00.00 no campo')
    c.hover(CAMPO('ncm'), 2.0, w=(4, 'NCM'), label='NCM (Nota Fiscal) 7404.00.00 (zoom)')
    c.ev(js_rola_ate('Identificação/Produto Fiscal', y=330, escopo=DLG), w=(5, 'Outro', None, 0.6), label='sobe até Identificação/Produto Fiscal')
    c.hover(CAMPO('fiscal_name'), 0.6, w=(5, 'Identificação,'), label='Identificação/Produto Fiscal, vazio')
    c.hover(SEL(f"{DLG} button[aria-label='Para que serve este campo']"), 4.0, w=(5, 'Ele'), label='ajuda: Como funciona, Para que serve, Exemplo, Se deixar vazio')
    c.confere('body', ['Para que serve', 'Exemplo', 'Se deixar vazio'], 'ajuda aberta')
    c.hover(PD('Fiscal e organização'), 0.4, w=(6, 'Por'), label='cursor sai da ajuda (ilustração do nome fiscal)')
    # L6 e L7: ilustrações do nome fiscal; o robô fica parado
    c.hover(CAMPO('fiscal_name'), 0.8, w=(8, 'vazio,'), label='Identificação/Produto Fiscal fica vazio')
    c.click(BTN('Atualizar', within=DLG), w=(8, 'Atualizar.'), label='Atualizar')
    c.waitfor(text='Material atualizado!', timeout=10)
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    # L9: ilustração (o que fica no material e nos cenários fiscais)
    c.fim()
    return c


def cap05():
    """Grupos de material: Grupos, (ilustração L2) Radiadores com cor e o carro, Adicionar; Editar o radiador > Grupo; o filtro só no Cobre."""
    c = Cap(5, setup_estoque())
    c.click(BTN('Grupos'), w=(1, 'grupos.'), label='Grupos')
    c.waitfor(text='Grupos de materiais', timeout=8)
    c.hover(PD('Ferrosos'), 0.4, w=(1, 'ferrosos,'), label='Ferrosos')
    c.hover(PD('Outros'), 0.6, w=(1, 'outros.'), label='Outros (os cinco grupos)')
    # L2: ilustração das gavetas; o robô fica parado
    c.ev(js_rola_ate('Novo grupo', y=180, escopo=DLG), w=(3, 'No', None, 0.6), label='desce até Novo grupo (Adicionar fica na tela)')
    c.click(SEL(f"{DLG} input[placeholder='Ex: Metais, Plásticos, Papéis']"), w=(3, 'nome,'), label='Nome do grupo')
    c.type(SEL(f"{DLG} input[placeholder='Ex: Metais, Plásticos, Papéis']"), 'Radiadores', clicar=False, cps=30, label='Nome: Radiadores')
    c.hover(SEL(f"{DLG} input[type=color]"), 0.2, label='Cor')
    c.ev(js_valor(f"{DLG} input[type=color]", '#0f766e'), label='Cor verde-petróleo #0F766E (valor do campo, sem a janela nativa)')
    c.click(SEL(f"{DLG} button.rounded-full.w-12"), label='Ícone (abre a grade)')
    c.waitfor(target=SEL(f"{POP} button:has(svg.lucide-car)"), timeout=6)
    c.click(SEL(f"{POP} button:has(svg.lucide-car)"), w=(3, 'carro', 0), label='ícone carro')
    c.click(BTN('Adicionar', within=DLG), w=(4, 'Adicionar,'), label='Adicionar')
    c.waitfor(text='Grupo criado', timeout=8)
    c.confere('dlg', ['Radiadores'], 'Radiadores na lista de grupos')
    c.hover(PD('Radiadores', exact=True), 0.5, w=(4, 'criado.'), label='Radiadores na lista')
    fecha_janela(c, w=(5, 'Agora', None, 0.6))
    c.type(BUSCA, 'radiador', w=(5, 'radiador'), cps=30, label='busca radiador')
    c.waitfor(target=P('Radiador de cobre'), timeout=8)
    abre_acoes(c, 'Radiador de cobre', 'Editar', w=(5, 'nele,', None, 0.8))
    c.waitfor(text='Editar Material', timeout=8)
    c.ev(js_rola_ate('Fiscal e organização', y=380, escopo=DLG), label='desce até o campo Grupo')
    c.click(CAMPO('group_id'), w=(5, 'Grupo', 0), label='campo Grupo (abre a lista)')
    c.click(OPT('Radiadores'), w=(5, 'repara', None, 0.6), label='Radiadores')
    c.hover(SEL(f"{DLG} button[aria-label='Criar grupo']"), 1.4, w=(5, 'mais,'), label='botão + Criar grupo (sem clicar)')
    c.click(BTN('Atualizar', within=DLG), w=(6, 'Atualizar.'), label='Atualizar')
    c.waitfor(text='Material atualizado!', timeout=10)
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.hover(CELULA('Radiador de cobre', 3), 1.2, w=(6, 'grupo'), label='Radiadores embaixo do nome, com a bolinha')
    c.confere('row:Radiador de cobre', ['Radiador de cobre', 'Radiadores'], 'grupo Radiadores na linha')
    # L7: o filtro abre no começo da pergunta para os cinco cliques caberem antes dos cartões (L8)
    c.ev(js_valor('main input[placeholder="Buscar material por código ou nome..."]', ''), w=(6, 'dele.', None, -0.3), label='limpa a busca (sem cursor)')
    c.click(BTNX('Todos os Materiais'), w=(7, 'E', None, 0.4), label='filtro Todos os Materiais')
    c.waitfor(target=SEL(f"{POP} label:has-text('Alumínio')"), timeout=6)
    for k, g in enumerate(('Alumínio', 'Ferrosos', 'Metais', 'Outros', 'Radiadores')):
        c.click(SEL(f"{POP} label:has-text('{g}') button[role=checkbox]"), label=f'desmarca {g}')
    c.confere(POP, ['Cobre'], 'só o Cobre marcado')
    c.press('Escape', w=(7, 'cobre.', None, -0.4), label='fecha o filtro (botão: 3 materiais)')
    c.pause(0.4)
    c.confere('main', ['3 materiais'], 'botão do filtro: 3 materiais')
    c.hover(P('Peso Total em Estoque'), 0.5, w=(8, 'peso'), label='cartões só do cobre (zoom)')
    c.hover(P('Total Pago'), 1.0, w=(8, 'valor'), label='Total Pago do cobre')
    c.click(BTNX('3 materiais'), w=(9, 'voltar,'), label='abre o filtro')
    c.click(SEL(f"{POP} label:has-text('Todos os Materiais') button[role=checkbox]"), w=(9, 'Todos'), label='Todos os Materiais')
    c.press('Escape', label='fecha o filtro')
    c.pause(0.4)
    c.confere('main', ['Todos os Materiais'], 'filtro de volta em Todos os Materiais')
    c.fim()
    return c


def cap06():
    """Editar preços em massa: Editar Tabela, busca cobre, +0,50 na compra e na venda dos três cobres, Salvar."""
    c = Cap(6, setup_estoque())
    c.hover(BTN('Editar Tabela'), 0.6, w=(1, 'Editar'), label='Editar Tabela')
    c.click(BTN('Editar Tabela'), w=(2, 'Abre'), label='abre Editar Preços em Massa')
    c.waitfor(text='Editar Preços em Massa', timeout=10)
    c.hover(PD('Compra (R$)'), 0.3, w=(2, 'compra'), label='Compra (R$)')
    c.hover(PD('Venda (R$)'), 0.3, w=(2, 'venda'), label='Venda (R$)')
    c.hover(PD('Tabela principal'), 0.6, w=(2, 'esquerda'), label='Tabelas disponíveis: Principal (Padrão)')
    c.type(SEL(f"{DLG} input[placeholder='Buscar por código ou nome...']"), 'cobre', w=(3, 'Busco'), cps=CPS, label='busca cobre')
    c.confere('dlg', ['Cobre mel', 'Cobre misto', 'Fio de cobre encapado', 'Radiador de cobre'], 'ficam só os cobres')
    c.click(GRADE('Cobre mel', 0), w=(4, 'compra'), label='Cobre mel: Compra')
    c.type(GRADE('Cobre mel', 0), '42,50', w=(4, 'quarenta', 0), clicar=False, clear=True, label='Cobre mel compra 42,50 (zoom: linha Cobre mel)')
    c.click(GRADE('Cobre mel', 1), w=(4, 'venda'), label='Cobre mel: Venda')
    c.type(GRADE('Cobre mel', 1), '47,90', w=(4, 'quarenta', 1), clicar=False, clear=True, label='Cobre mel venda 47,90')
    for k, (nome, comp, vend) in enumerate((('Cobre misto', '36,00', '41,50'), ('Fio de cobre encapado', '18,00', '22,00'))):
        w0 = (5, 'Faço') if k == 0 else None
        c.type(GRADE(nome, 0), comp, w=w0, clear=True, cps=24, label=f'{nome} compra {comp} (selo 4x)')
        c.type(GRADE(nome, 1), vend, clear=True, cps=24, label=f'{nome} venda {vend} (selo 4x)')
    c.press('Tab', label='sai da célula (o valor assenta)')
    c.confere('dlg', ['3 material(is) com alterações pendentes'], 'aviso 3 material(is) com alterações pendentes')
    c.hover(GRADE('Cobre misto', 0), 0.8, w=(6, 'células'), label='células alteradas destacadas')
    c.hover(PD('com alterações pendentes'), 1.4, w=(6, 'aviso'), label='aviso 3 material(is) com alterações pendentes')
    c.click(BTN('Salvar', within=DLG), w=(7, 'Salvar,'), noScroll=True, label='Salvar (rodapé da janela)')
    c.waitfor(text='Preços atualizados!', timeout=10)
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.hover(SEL('[data-sonner-toast]'), 2.0, w=(7, 'aviso'), label='aviso Preços atualizados! As tabelas vinculadas... (o mouse segura o aviso)')
    c.confere('main', ['R$ 42,50', 'R$ 47,90'], 'Cobre mel 42,50 e 47,90 na lista')
    c.fim()
    return c


def cap07():
    """Várias tabelas de preço: Nova Tabela vinculada +4 %, Cobre mel 44,20; Depósito Irmãos Siqueira > Editar > Tabela de Preços Padrão;
    (ilustração da ordem, L8) compra só para ver o preço: tabela no cobre mel, preço personalizado no bronze."""
    st = setup_estoque(aquecer=(('/clientes-fornecedores', 'Clientes e Fornecedores'), ('/caixa', 'Nova Compra')))
    c = Cap(7, st)
    c.hover(P('Tabelas de Preço'), 0.6, w=(1, 'tabela'), label='coluna Tabelas de Preço')
    c.hover(BTN('Principal'), 1.0, w=(1, 'principal.'), label='só a Principal')
    c.click(BTN('Nova Tabela'), w=(2, 'Nova'), label='Nova Tabela')
    c.waitfor(text='Nova Tabela de Preços', timeout=8)
    c.type({'placeholder': 'Ex: Atacado, Varejo, Premium...'}, 'Tabela Depósitos', w=(2, 'nome'), cps=30, label='Nome da Tabela: Tabela Depósitos')
    c.click(SEL(f"{DLG} #is-linked"), w=(2, 'Marco'), label='Vincular à tabela principal')
    c.waitfor(text='Exemplo de cálculo', timeout=6)
    c.type(SEL(f"{DLG} input[inputmode=decimal]"), '4', w=(2, 'quatro'), clear=True, label='Valor da variação 4')
    c.confere('dlg', ['Porcentagem', 'Aumenta', 'R$ 10,40'], 'Porcentagem, Aumenta, R$ 10,40')
    c.hover(PD('Exemplo de cálculo'), 2.2, w=(3, 'exemplo'), label='Exemplo de cálculo: R$ 10,00 > R$ 10,40 (+4%) (zoom)')
    # L4: ilustração da tabela vinculada; o robô fica parado
    c.click(BTN('Criar Tabela', within=DLG), w=(5, 'Criar'), label='Criar Tabela')
    c.waitfor(text='Tabela de preço criada com sucesso!', timeout=10)
    c.waitfor(text='Exibindo preços da tabela: Tabela Depósitos', timeout=8)
    c.ev(js_rola_ate('Cobre mel', y=430), w=(5, 'lista'), label='desce até o Cobre mel')
    c.confere('row:Cobre mel', ['Cobre mel', 'R$ 44,20', 'R$ 47,90'], 'Cobre mel R$ 44,20 na Tabela Depósitos, venda R$ 47,90')
    c.hover(CELULA('Cobre mel', 7), 1.4, w=(5, 'quarenta'), label='Cobre mel Preço de Compra R$ 44,20 (zoom: linha Cobre mel)')
    c.hover(CELULA('Cobre mel', 8), 1.0, w=(5, 'venda,'), label='Preço de Venda R$ 47,90 (o da principal)')
    # L6: menu lateral recolhido (abre ao passar o mouse) > Clientes e Fornecedores > Fornecedores > o depósito (na lista, sem busca) > Editar
    c.hover(MENU('/clientes-fornecedores'), 0.6, w=(6, 'ligar'), noScroll=True, label='menu lateral (abre ao passar o mouse)')
    c.click(MENU('/clientes-fornecedores'), w=(6, 'Clientes'), noScroll=True, label='Clientes e Fornecedores')
    c.rolar(0, ponto=(760, 420), duration=0.3, after=0, label='cursor sai do menu (ele recolhe)')
    c.waitfor(target=BTN('Fornecedores', within='main'), timeout=12)
    c.pause(0.5)
    c.click(BTN('Fornecedores', within='main'), label='aba Fornecedores')
    c.waitfor(target=P('Depósito Irmãos Siqueira'), timeout=8)
    c.click(P('Depósito Irmãos Siqueira'), w=(6, 'Depósito'), label='Depósito Irmãos Siqueira')
    c.waitfor(text='1 preço personalizado', timeout=10)
    c.click(BTN('Editar', within='main'), w=(6, 'Editar.'), label='Editar')
    c.waitfor(text='Editar Fornecedor', timeout=10)
    c.ev(js_rola_ate('Tabela de Preços Padrão', y=380, escopo=DLG), w=(7, 'Em', None, 0.6), label='desce até Tabela de Preços Padrão')
    c.click(SEL(f"{DLG} div.space-y-2:has(> label:has-text('Tabela de Preços Padrão')) button[role=combobox]"), w=(7, 'escolho'), label='Tabela de Preços Padrão (abre)')
    c.click(OPT('Tabela Depósitos'), w=(7, 'Depósitos'), label='Tabela Depósitos (zoom)')
    c.click(BTN('Salvar', within=DLG), w=(7, 'salvo.'), noScroll=True, label='Salvar')
    c.waitfor(text='Fornecedor atualizado!', timeout=10)
    # L8: ilustração da escada de prioridade; por baixo dela o robô vai ao Caixa sem cursor
    c.ev("(()=>{history.pushState({},'','/caixa');window.dispatchEvent(new PopStateEvent('popstate'));return location.pathname})()", w=(8, 'Uma'), label='vai ao Caixa (por baixo da ilustração)')
    c.waitfor(text='Nova Compra', timeout=15)
    c.click(SEL("main button:has-text('Nova Compra')"), w=(9, 'abro'), label='Nova Compra')
    c.waitfor(target=SEL('#supplier-desktop-top'), timeout=15)
    c.click(SEL('#supplier-desktop-top'), w=(9, 'Escolho', None, 1.6), label='Selecionar Fornecedor')
    c.type({'placeholder': 'Buscar por nome, apelido, CPF/CNPJ ou telefone...'}, 'Depósito', clicar=False, cps=30, label='busca Depósito')
    c.click(PD('Depósito Irmãos Siqueira'), w=(9, 'depósito,'), label='Depósito Irmãos Siqueira')
    c.confere('main', ['Tabela Depósitos'], 'Tabela de Preços passou para Tabela Depósitos')
    c.registra(SEL("main button[role=combobox]:has-text('Tabela Depósitos')"), w=(9, 'tabela'), label='Tabela de Preços: Tabela Depósitos (zoom, sem o mouse)')
    c.click({'placeholder': 'Escreva o nome ou código do material'}, w=(9, 'selecionada.'), label='campo do material')
    c.type({'placeholder': 'Escreva o nome ou código do material'}, 'cobre', w=(10, 'No'), clicar=False, cps=30, label='material: cobre')
    c.click(OPT('Cobre mel', exact=False), w=(10, 'mel,'), label='Cobre mel')
    c.confere('body', ['Preço da tabela aplicado para Cobre mel'], 'aviso Preço da tabela aplicado')
    c.registra(VALOR_KG, w=(10, 'quarenta'), label='Valor/kg 44,20 (zoom)')
    c.confere_campos(['44,2'], 'Valor/kg 44,20', escopo='main')
    c.click({'placeholder': 'Escreva o nome ou código do material'}, w=(10, 'vinte.', None, -0.1), label='campo do material de novo')
    c.type({'placeholder': 'Escreva o nome ou código do material'}, 'bronze', w=(11, 'Já', None, 0.3), clicar=False, clear=True, cps=30, label='troca para bronze')
    c.click(OPT('Bronze', exact=False), w=(11, 'bronze,', None, 0.3), label='Bronze')
    c.confere('body', ['Preço especial aplicado para Bronze'], 'aviso Preço especial aplicado para Bronze')
    # o aviso vive 2 s: o cursor vai direto para ele e fica em cima (o sonner pausa) até o fim de "Preço especial aplicado."
    ini = round(c.W(11, 'bronze,') + 0.9, 2)
    c.hover(SEL('[data-sonner-toast]'), round(c.W(11, 'aplicado.') + 0.6 - ini - 0.55, 2), w=ini,
            label='aviso Preço especial aplicado (o mouse segura o aviso) (zoom: Valor/kg 30,50 com o aviso)')
    c.confere_campos(['30,5'], 'Valor/kg 30,50', escopo='main')
    c.fim()
    return c


def cap08():
    """Movimentar, transferir e zerar: saída de 2 kg do radiador, (ilustração L4) transferência de 8 kg para o Ferro misto, Zerar só mostrado."""
    c = Cap(8, setup_estoque())
    c.hover(BTN('Movimentar estoque'), 1.2, w=(1, 'ajuste'), label='Movimentar estoque')
    c.click(BTN('Movimentar estoque'), w=(2, 'Em'), label='Movimentar estoque')
    c.waitfor(text='Registre uma entrada ou saída manual', timeout=8)
    c.click(BTN('Saída', within=DLG), w=(2, 'estoque,'), primeiro=True, label='Saída')
    c.type({'placeholder': 'Escreva o nome ou código do material'}, 'radiador', w=(2, 'escolho'), cps=40, label='Material: radiador')
    c.click(OPT('Radiador de cobre', exact=False), label='Radiador de cobre')
    c.type(SEL('#movement-quantity'), '2', w=(2, 'dois'), label='Quantidade 2')
    c.confere('dlg', ['Estoque de Radiador de cobre', 'Estoque atual', '120', '2 Kg', 'Após a movimentação', '118'], 'antes 120, -2 Kg, depois 118')
    c.hover(PD('Após a movimentação'), 2.0, w=(2, 'antes'), label='Estoque de Radiador de cobre: 120 > -2 Kg > 118 (zoom)')
    c.type(SEL('#movement-description'), 'Ajuste de inventário', w=(3, 'escrevo'), cps=40, label='Descrição: Ajuste de inventário')
    c.click(BTN('Registrar saída', within=DLG), w=(3, 'Registrar'), label='Registrar saída')
    c.waitfor(text='Saída de 2 Kg de Radiador de cobre', timeout=10)
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    # L4: ilustração da transferência; por baixo dela, a busca do radiador sem cursor
    c.ev(js_valor('main input[placeholder="Buscar material por código ou nome..."]', 'radiador'), w=(4, 'Na'), label='busca radiador (por baixo da ilustração)')
    c.waitfor(target=P('Radiador de cobre'), timeout=8)
    abre_acoes(c, 'Radiador de cobre', 'Transferir estoque', w=(5, 'pontinhos'), w_item=(5, 'Transferir'))
    c.waitfor(text='Transferir quantidade de Radiador de cobre', timeout=8)
    c.confere('dlg', ['Transferir quantidade de Radiador de cobre (Código: 70)', '118 Kg'], 'Transferir Estoque: código 70, 118 Kg')
    c.type({'placeholder': 'Escreva o nome ou código do material'}, 'ferro misto', w=(5, 'Destino,'), cps=40, label='Material de Destino: ferro misto')
    c.click(OPT('Ferro misto', exact=False), label='Ferro misto')
    c.type(SEL('#transfer-quantity'), '8', w=(5, 'oito'), label='Quantidade a Transferir 8 (zoom)')
    c.click(BTN('Transferir', within=DLG), w=(6, 'Transferir:'), label='Transferir')
    c.waitfor(text='Transferido 8 Kg de Radiador de cobre para Ferro misto', timeout=10)
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.confere('row:Radiador de cobre', ['110'], 'radiador com 110 Kg')
    c.ev(js_valor('main input[placeholder="Buscar material por código ou nome..."]', ''), w=(7, 'E', 0, 0.9), label='limpa a busca (sem cursor)')
    c.click(BTN('Zerar Estoque'), w=(7, 'Zerar'), label='Zerar Estoque')
    c.waitfor(text='Zerar Todo o Estoque', timeout=8)
    c.confere('dlg', ['Atenção: Ação irreversível', '16 de 16 selecionados'], 'todos marcados: 16 de 16 selecionados')
    c.hover(PD('selecionados'), 1.0, w=(7, 'marcados,'), label='16 de 16 selecionados')
    c.hover(SEL(f"{DLG} label:has-text('Ferro pesado')"), 0.8, w=(7, 'desmarca'), label='um material (dá para desmarcar)')
    c.hover(PD('Para confirmar, digite'), 1.6, w=(8, 'confirmar,'), label='Para confirmar, digite Zerar todo o meu estoque (zoom)')
    c.hover(BTNX('Zerar selecionados'), 1.0, w=(8, 'volta.'), label='Zerar selecionados apagado')
    c.click(BTN('Cancelar', within=DLG), w=(8, 'cancelo.'), label='Cancelar')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.fim()
    return c


def cap09():
    """Exportar: o menu; Estoque (PDF) com as colunas, Exportar (aba nova: o PDF fica no actions.json); Tabela Depósitos > Tabela de
    Preços (PDF) > Exportar PDF > A4."""
    c = Cap(9, setup_estoque(extra=[{'do': 'eval', 'js': JS_PDF_GANCHO}]))
    c.click(BTNX('Exportar'), w=(1, 'Exportar.'), label='Exportar (abre o menu)')
    c.waitfor(target=ITEM('Estoque (PDF)'), timeout=6)
    c.hover(ITEM('Estoque (PDF)'), 0.5, w=(1, 'PDF', 0), label='Estoque (PDF)')
    c.hover(ITEM('Estoque (Excel)'), 0.5, w=(1, 'Excel,'), label='Estoque (Excel)')
    c.hover(ITEM('Tabela de Preços (PDF)'), 0.6, w=(1, 'tabela'), label='Tabela de Preços (PDF)')
    c.click(ITEM('Estoque (PDF)'), w=(2, 'estoque,'), label='Estoque (PDF)')
    c.waitfor(text='Colunas do arquivo', timeout=8)
    c.hover(PD('Materiais', exact=True), 0.6, w=(2, 'materiais'), label='Materiais')
    c.hover(PD('Colunas do arquivo'), 0.6, w=(2, 'colunas'), label='Colunas do arquivo')
    c.click(BTN('Exportar', within=DLG), w=(2, 'Exportar,'), label='Exportar (o PDF abre noutra aba)')
    c.waitfor(text='Lista exportada como PDF!', timeout=15)
    c.ev(js_pdf(0, 'lista-materiais'), label='PDF do estoque (para a edição)')
    c.click(BTNX('Tabela Depósitos'), w=(3, 'Seleciono'), label='Tabela Depósitos (coluna)')
    c.waitfor(text='Exibindo preços da tabela: Tabela Depósitos', timeout=8)
    c.click(BTNX('Exportar'), w=(3, 'escolho', None, 1.2), label='Exportar')
    c.click(ITEM('Tabela de Preços (PDF)'), label='Tabela de Preços (PDF)')
    c.waitfor(text='Exportar tabela de preços em PDF', timeout=8)
    c.click(BTNX('Exportar PDF', within=DLG), w=(3, 'formato:'), label='Exportar PDF')
    c.waitfor(text='Formato da tabela de preços', timeout=8)
    c.hover(BTNX('A4', within=DLG), 0.4, w=(3, 'A4'), label='A4 (folha)')
    c.hover(BTNX('Térmico', within=DLG), 0.3, w=(3, 'impressora'), label='Térmico')
    c.click(BTNX('A4', within=DLG), w=(4, 'Pronto:'), label='A4 (o PDF abre noutra aba)')
    c.waitfor(text='exportada!', timeout=15)
    c.ev(js_pdf(1, 'tabela-precos-depositos-a4'), label='PDF da Tabela Depósitos A4 (para a edição: título e Cobre mel R$ 44,20)')
    c.fim()
    return c


def cap10():
    """Excluir um material: (ilustração L1; no fim dela o Excluir abre sem cursor) aviso de 110 kg, Sim, Excluir; o aviso com Desfazer; Desfazer."""
    c = Cap(10, setup_estoque(busca='radiador'))
    c.ev(js_menu_item('Radiador de cobre', 'Excluir'), w=(1, 'continuam', None, 0.3), label='abre o Excluir do radiador (fim da ilustração, sem cursor)')
    c.waitfor(text='Confirmar Exclusão', timeout=8)
    c.confere('dlg', ['Radiador de cobre', 'Código: 70', 'Atenção: Este material possui 110 Kg em estoque.'], 'aviso 110 Kg em estoque')
    c.hover(PD('Atenção: Este material possui'), 2.4, w=(2, 'cento'), label='aviso: possui 110 Kg em estoque (zoom)')
    c.click(BTN('Sim, Excluir'), w=(3, 'Sim,'), label='Sim, Excluir')
    c.waitfor(text='excluído', timeout=10)
    c.hover(SEL('[data-sonner-toast] button:has-text("Desfazer")'), 0.4, w=(3, 'Desfazer.'), label='aviso "Radiador de cobre" excluído com Desfazer (o mouse segura o aviso)')
    c.click(SEL('[data-sonner-toast] button:has-text("Desfazer")'), w=(4, 'Clicando'), label='Desfazer')
    c.waitfor(text='restaurado!', timeout=10)
    c.waitfor(target=P('Radiador de cobre'), timeout=10)
    c.hover(CELULA('Radiador de cobre', 4), 1.4, w=(4, 'saldo'), label='o radiador volta com 110 Kg')
    c.confere('row:Radiador de cobre', ['70', 'Radiador de cobre', '110'], 'radiador de volta, 110 Kg')
    c.fim()
    return c


def cap11():
    """Recapitulando: passa pelo estado final (radiador 70 no grupo Radiadores, Tabela Depósitos +4 %); a edição monta os trechos dos
    capítulos por cima."""
    c = Cap(11, setup_estoque())
    c.type(BUSCA, 'radiador', w=(1, 'cadastrou'), cps=24, label='busca radiador')
    c.hover(CELULA('Radiador de cobre', 7), 1.0, w=(1, 'preços'), label='preços do radiador')
    c.hover(CELULA('Radiador de cobre', 2), 1.0, w=(1, 'código', 0), label='código 70')
    c.hover(CELULA('Radiador de cobre', 3), 1.2, w=(2, 'grupo'), label='grupo Radiadores')
    c.ev(js_valor('main input[placeholder="Buscar material por código ou nome..."]', ''), w=(3, 'Reajustou', None, 0.3), label='limpa a busca (sem cursor)')
    c.click(BTNX('Tabela Depósitos'), w=(3, 'Tabela', 0), label='Tabela Depósitos +4%')
    c.waitfor(text='Exibindo preços da tabela: Tabela Depósitos', timeout=8)
    c.hover(P('Exibindo preços da tabela: Tabela Depósitos'), 1.2, w=(3, 'Siqueira'), label='Exibindo preços da tabela: Tabela Depósitos')
    c.click(BTN('Principal'), w=(4, 'Ajustou'), label='volta à Principal')
    c.hover(BTN('Movimentar estoque'), 0.6, w=(4, 'transferiu'), label='Movimentar estoque')
    c.hover(BTNX('Exportar'), 0.6, w=(4, 'exportou'), label='Exportar')
    c.hover(P('Lista de Materiais'), 0.8, w=(4, 'excluir'), label='a lista')
    c.fim()
    return c


CAPS = {f'{n:02d}': globals()[f'cap{n:02d}'] for n in range(12)}
CAPS['01b'] = cap01b

if __name__ == '__main__':
    pedidos = sys.argv[1:] or sorted(CAPS, key=lambda k: (int(k[:2]), k))
    for a in pedidos:
        k = f'{int(a[:-1]):02d}b' if a.endswith('b') else f'{int(a):02d}'
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
