#!/usr/bin/env python3
"""T10 · gera rec/t10/capNN.json (roteiros do robô) a partir da voz (t10/narracao/capNN.json). Estoque: saldo, histórico e posição.

EcoSistema 1.60.18 no COMPUTADOR (tela 1600x900), Recicla Vale Metais, Rafael Nogueira (MASTER), FAKE_NOW 10/11/2026 08:30 (todos os
capítulos). 15 capítulos (20/11: cap07 "Achar uma movimentação" e cap11 "Clientes, usuários e grupos" são novos; o antigo 7-10 virou 8-10 e 12; 11 virou 13; 12 virou 14). Uso, de qualquer pasta:  python3 -I rec/t10/gerar.py [NN ...]   (sem argumento: todos)
Antes (e sempre que o mundo base mudar): python3 -I rec/t10/t10_sementes.py  (sementes t10/inicio e t10/apos-cap03 e as 2 fotos).
Depois: ensaio.py NN (rápido) -> record.mjs --rapido -> resumo.py NN --ens -> prever.py NN --ens -> gravação com os tempos -> resumo.py NN.

Forma e regras: as do gerador-molde da trilha (rec/t03/gerar.py), copiadas aqui (cada aula tem o seu):
 - A voz vem de t10/narracao/capNN.json (hoje ESTIMADA; amanhã a do proc.py); o gerador confere as palavras de cada linha com o
   tts_textos.py e para se a voz estiver velha (rode de novo planejamento/ecoflix/preparar_aula.sh T10).
 - Todo gesto que a fala cita tem `w=(linha, 'palavra'[, nth][, folga])`: at = início da palavra - folga do gesto (FOLGA), para o cursor
   CHEGAR na palavra. Palavra repetida na linha exige `nth`. As marcas L1..Ln entram sozinhas (at = início da linha - 0,9).
 - Rótulo "[ZOOM] ..." = as marcações [ZOOM: ...] do roteiro (a edição aponta para o rótulo). `confere*` LÊ a tela e compara com a fala;
   o observador `OBS` guarda em window.__avisos todo aviso de erro do app e o último passo devolve a lista (tem de sair vazia).
 - Ilustração que cobre a janela ([ILUSTRAÇÃO] do roteiro): o robô fica parado ou mexe só por `eval` (sem cursor).

LOGIN: cada capítulo grava sem sessão pronta ("anonymous": true) e entra pela tela de login no `setup` (fora do vídeo) com "$TUT_USER" e
"$TUT_SENHA" do ambiente (o valor nunca vai para arquivo nem log).

PARTICULARIDADES DA 1.59.154 (T03 e este ensaio):
 - A 1280 px com o menu lateral aberto a lista do Estoque perde colunas: o cap01 recolhe o menu por baixo da ilustração (L3) e os
   capítulos 2 a 12 começam com ele recolhido (setup). Menu recolhido abre ao passar o mouse (fecha 500 ms depois de sair): depois de
   navegar por ele, o cursor sai para um ponto neutro. O item do menu é "Histórico (Kardex)" (o roteiro diz "Histórico").
 - A barra de seleção do Estoque ("2 selecionados", "Transferir Estoque") é fixa no pé da tela (y ~750, fora da faixa 96..730): noScroll.
 - Menu recolhido aberto pelo mouse traz o grupo Materiais FECHADO (mesmo com a página dentro dele): clique no grupo só se o item ainda não
   aparece (`unless`), depois o item.
 - Quantidades sem casas fixas: "6.420 Kg", "42 Kg", "+320 Kg"; o aviso é "Transferido 320 Kg de Ferro misto para Ferro pesado".
 - Kardex: o "Filtros" abre uma folha (role=dialog) e os filtros valem na hora; "Aplicar filtros" só fecha a folha. "Aplicar filtros" e
   "Limpar filtros" ficam no rodapé da folha (y ~770, fora da faixa 96..730): noScroll (sem ele, ~7 s rolando em vão). Linha de compra ou
   venda abre o pedido numa tabela de dentro (main table table); a de Edição Manual abre Observação, Estoque antes -> depois, usuário e hora.
 - Relatório: os cartões são CollapsibleTrigger com aria-label (botão "Total Comprado"...); o cabeçalho "Lucro s/ Vendas" ORDENA ao clicar
   (só passar o mouse). Fornecedores é um "chip" (o nome do botão vira o do fornecedor marcado).
 - Posição de Estoque: data no calendário (react-day-picker 8: seta button[name=previous-month], dia button[name=day]); "Ver posição" só
   acende depois de trocar a data. O PDF abre noutra aba (o vídeo grava uma aba só): o roteiro guarda o PDF que o app gerou (gancho no
   URL.createObjectURL) e o devolve no actions.json, para a edição mostrar a aba como ilustração.
"""
import hashlib
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))           # $TUT_HOME/rec/t10
AULA = os.path.basename(HERE)                                # t10
TUT = os.path.normpath(os.path.join(HERE, '..', '..'))       # $TUT_HOME
NARR = os.path.join(TUT, AULA, 'narracao')
MUNDO = json.load(open(os.path.join(TUT, 'rec', 'mundo', 'mundo.json'), encoding='utf8'))
FAKE_NOW = '2026-11-10T08:30:00-03:00'                        # plano.md (igual no Supabase falso e no robô)
HOJE = FAKE_NOW[:10]

sys.path.insert(0, NARR)
from tts_textos import CAPS as TEXTOS  # noqa: E402  (texto atual de cada capítulo, grafia do TTS)

NOMES = ['Abertura', 'As quatro portas do estoque', 'O saldo de cada material', 'Transferir entre materiais', 'O Kardex, linha a linha',
         'Os tipos de movimentação', 'O pedido por trás da linha', 'Achar uma movimentação', 'Comprado, vendido e lucro',
         'Material por material', 'O filtro de fornecedor', 'Clientes, usuários e grupos', 'A foto do estoque numa data',
         'Exportar para o contador', 'Recapitulando']
# estado de partida: t10/inicio (as 2 fotos da compra de 09/11) e, do cap04 em diante, t10/apos-cap03 (a transferência de 320 kg)
SEMENTE = {n: (['inicio'] if n <= 3 else ['inicio', 'apos-cap03']) for n in range(15)}

# folga de cada gesto (pace 0,5; medido no T03 e na tabela "Custo real dos gestos" do docs/04): at = palavra - folga
FOLGA = {'click': 0.7, 'click1': 1.3, 'hover': 0.55, 'type': 0.95, 'typen': 0.05, 'press': 0.05, 'scroll': 0.15, 'eval': 0.0, 'goto': 0.9}
CPS = 14


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
        return '1.60.18'


def storage_de(usuario):
    """localStorage de quem entra pela tela de login: as chaves de "já vi" que a sessão pronta do robô poria + as do mundo"""
    uid, v = stable_id(usuario), versao_app()
    t = {'user_id': uid, 'company_id': stable_id(MUNDO['config']['empresa']), 'hoje': HOJE, 'versao': v}
    troca = lambda s: re.sub(r'\{(\w+)\}', lambda m: t.get(m.group(1), m.group(0)), str(s))
    st = {'app_version': v, 'notification_shown_version': v, 'pwa-install-dismissed': 'true', 'theme': 'light'}
    st.update({troca(k): troca(val) for k, val in MUNDO.get('navegador', {}).get('localStorage', {}).items()})
    return st


def falas_do_texto(n):
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
    def __init__(s, n, setup, prewarm=('/login',), pace=0.5, cps=CPS, start=(700, 300), user='rafael', erros_ok=()):
        s.n = n
        s.nome = f'cap{n:02d}'
        s.words, s.linhas, s.dur, s.estimada = carregar_voz(n)
        s.pace, s.cps, s.start = pace, cps, start
        s.prewarm = list(prewarm)
        s.user = user
        s.setup = list(setup) + [{'do': 'eval', 'js': js_obs(erros_ok)}]
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
            if d.get('do') == 'type':
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
            for mt, mi in sorted(s.pending):
                if at < mt <= at + 0.8:
                    at = round(mt, 2)
            fim = at + 0.55 + seconds
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

    def cursor(s, ponto, w=None, label='cursor para um ponto neutro'):
        """leva o cursor a um ponto da tela sem clicar (roda com by 0): tira o mouse do menu lateral recolhido"""
        return s._p({'do': 'scroll', 'point': {'x': ponto[0], 'y': ponto[1]}, 'by': 0, 'duration': 0.3, 'after': 0}, w, 'scroll', label, {})

    def goto(s, url, w=None, label=None):
        return s._p({'do': 'goto', 'url': url}, w, 'goto', label or f'vai para {url} (sem cursor)', {})

    def ev(s, js, w=None, label=None, **kw):
        return s._p({'do': 'eval', 'js': js}, w, 'eval', label, kw)

    def waitfor(s, **kw):
        return s.add({'do': 'waitFor', **kw})

    def pause(s, seconds):
        return s.add({'do': 'pause', 'seconds': seconds})

    def registra(s, alvo, w=None, label=None, **kw):
        """retângulo do alvo para a câmera (zoom/destaque da edição) SEM mexer o mouse: `type` sem clique e sem texto"""
        return s._p({'do': 'type', 'target': alvo, 'text': '', 'noClick': True, 'optional': True, 'timeout': 4, **kw}, w, 'typen', label, {})

    def confere(s, escopo, esperados, label):
        """LÊ a tela e compara com o que a fala diz: 'OK: ...' ou 'DIFERENTE: ...'. Escopo 'dlg' (a última janela), 'main', 'body',
        'row:<texto>' (a linha da tabela com esse texto) ou um seletor CSS. Tenta por ~6 s."""
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

    def confere_ausente(s, escopo, texto, label, espera=0.3):
        sel = {'dlg': '[role=dialog]', 'main': 'main', 'body': 'body'}.get(escopo, escopo)
        js = ("(async()=>{await new Promise(r=>setTimeout(r,%d));" % int(espera * 1000) + "const el=document.querySelector(%s);"
              "const t=(el?el.innerText:'').replace(/[\\s\\u00a0]+/g,' ').toLowerCase();"
              "return t.includes(%s)?'DIFERENTE: apareceu '+%s:'OK: ausente '+%s})()") % (json.dumps(sel), json.dumps(texto.lower(), ensure_ascii=False),
                                                                                         json.dumps(texto, ensure_ascii=False), json.dumps(texto, ensure_ascii=False))
        return s.add({'do': 'eval', 'js': js, 'label': 'confere ' + label})

    def fim(s):
        s.flush(1e9)
        s.steps.append({'do': 'eval', 'js': 'JSON.stringify(window.__avisos || "sem observador")', 'label': 'avisos de erro na tela'})
        s.steps.append({'do': 'mark', 'name': 'FIM', 'at': round(s.dur, 2)})

    def out(s):
        return {
            'name': f'{AULA}-{s.nome}',
            'title': f'T10 · Cap. {s.n} · {NOMES[s.n]} (narração {str(round(s.dur, 1)).replace(".", ",")} s{" ESTIMADA" if s.estimada else ""}; '
                     f'marcas L1..L{len(s.linhas)} = início de cada linha do roteiro; FAKE_NOW {FAKE_NOW}; usuário {s.user})',
            'seed': f'{AULA}-{s.nome}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
            'start': {'x': s.start[0], 'y': s.start[1]},
            'anonymous': True, 'storage': storage_de(f'user.{s.user}'),
            'seedExtra': [f'{AULA}/{x}' for x in SEMENTE[s.n]],
            'prewarm': s.prewarm, 'setup': s.setup, 'steps': s.steps,
        }


# ---------------------------------------------------------------- alvos
BTN = lambda n, **kw: {'role': 'button', 'name': n, 'exact': True, **kw}
BTNX = lambda n, **kw: {'role': 'button', 'name': n, **kw}
TXT = lambda t, **kw: {'text': t, 'exact': True, **kw}
P = lambda t, **kw: {'text': t, 'within': 'main', **kw}
SEL = lambda s_, **kw: {'selector': s_, **kw}
DLG = '[role=dialog]'
PD = lambda t, **kw: {'text': t, 'within': DLG, **kw}
OPT = lambda n, **kw: {'role': 'option', 'name': n, **kw}
ITEM = lambda n, **kw: {'role': 'menuitem', 'name': n, **kw}
POP = '[data-radix-popper-content-wrapper]'
MENU = '[data-sidebar=sidebar]'                                         # menu lateral do app
MENU_GRUPO = lambda n: BTN(n, within=MENU)                              # "Materiais" (abre o grupo; recolhido: abre o menu ao passar)
MENU_LINK = lambda n: {'role': 'link', 'name': n, 'exact': True, 'within': MENU}
TOGGLE_MENU = SEL('header button:has(svg.lucide-panel-left-close), header button:has(svg.lucide-panel-left)')   # fixo no topo (y 27)
ACOES = lambda nome: SEL(f"main tbody tr:has-text('{nome}') td:last-child button")
CELULA = lambda nome, col: SEL(f"main tbody tr:has-text('{nome}') td:nth-child({col})")   # Estoque: 1 caixa, 2 Código, 3 Nome, 4 Estoque Atual, 5 Valor Pago, 6 Preço médio pago
TH = lambda t: SEL(f"main thead th:has-text('{t}')")
CHK = lambda nome: {'role': 'checkbox', 'name': f'Selecionar {nome}', 'exact': True}
BARRA = lambda t: SEL(f"div.fixed button:has-text('{t}')")                          # barra de seleção (pé da tela)
# Kardex
KMAT = lambda nome: SEL(f"main [role=list] button:has-text('{nome}')")              # coluna Materiais
KROW = lambda txt: SEL(f"main tbody tr:has-text('{txt}')")                          # linha da tabela (1ª que tem o texto)
KCEL = lambda txt, col: SEL(f"main tbody tr:has-text('{txt}') > td:nth-child({col})")   # 3 Data, 4 Tipo, 7 Inicial, 8 Movimentação, 9 Final
KBADGE = lambda tipo: SEL(f"main tbody tr > td:nth-child(4) :text-is('{tipo}')", nth=0)
FILTROS = SEL('main button:has(> svg.lucide-list-filter)')                          # "Filtros" (com o contador quando há filtro)
OPCAO = lambda t: SEL(f"{POP} label:has-text('{t}')")                               # opção de um FilterMultiSelect
ITEM_CEL = lambda k: SEL(f"main table table tbody tr:has-text('Ferro pesado') > td:nth-child({k})")   # 1 Material, 2 Peso, 3 Valor Unit., 4 Total
FOTO = lambda k: SEL(f"main button:has(img[alt='compra-0911-{k}.jpg'])")
COMBO = lambda txt, esc='main': SEL(f'{esc} button[role=combobox]', hasText=txt)
# Relatório
RCEL = lambda nome, col: SEL(f"main tbody tr:has-text('{nome}') > td:nth-child({col})")   # 2 Material, 3 Qtd.C, 4 Valor C, 5 PM C, 6 Qtd.V, 7 Valor V, 8 PM V, 9 Lucro s/V, 10 Resultado, 11 Margem
# Posição
PCEL = lambda nome, col: SEL(f"main tbody tr:has-text('{nome}') > td:nth-child({col})")   # 1 Código, 2 Material, 3 Unidade, 4 Saldo, 5 Valor, 6 Projeção venda
DATA_BTN = lambda d: SEL(f"main button:has(svg.lucide-calendar):has-text('{d}')")
HORA = SEL("main input[aria-label='Hora']")
PREV_MES = SEL(f"{POP} button[name='previous-month']")
DIA = lambda d: SEL(f"{POP} button[name='day']:text-is('{d}')")


# ---------------------------------------------------------------- JS
def js_obs(ok=()):
    """observador de avisos de erro na tela (aceite: a lista sai vazia). `ok` = textos legítimos do capítulo"""
    erros = r"N[ãa]o foi poss[ií]vel|Erro ao|Tente novamente|indispon[ií]vel|Algo deu errado|Something went wrong|Falha ao|Pop-up bloqueado|Popup bloqueado|Sem permiss[ãa]o"
    ign = '|'.join(re.escape(x) for x in ok) or '$^'
    return ("(()=>{window.__avisos=[];const re=new RegExp(%s,'i');const ign=new RegExp(%s,'i');const chk=(t)=>{t=(t||'').trim();"
            "const m=t&&t.match(new RegExp('[^]{0,40}('+re.source+')[^]{0,40}','i'));"
            "if(m&&!ign.test(m[0])&&window.__avisos.length<10)window.__avisos.push(m[0].replace(/[\\n\\r\\t ]+/g,' '))};new MutationObserver(ms=>{for(const m of ms){"
            "m.addedNodes.forEach(n=>chk(n.textContent));if(m.type==='characterData')chk(m.target.textContent)}}).observe(document.body,"
            "{childList:true,subtree:true,characterData:true});chk(document.body.innerText);return 1})()") % (json.dumps(erros), json.dumps(ign))


ACHA_ROLAGEM = ("const rolagem=(el)=>{let c=el&&el.parentElement;while(c&&c!==document.body){const s=getComputedStyle(c);"
                "if(/(auto|scroll)/.test(s.overflowY)&&c.scrollHeight>c.clientHeight+4)return c;c=c.parentElement;}"
                "const se=document.scrollingElement;return se&&se.scrollHeight>se.clientHeight+4?se:null};")
SUAVE = ("await new Promise(res=>{const t0=performance.now();const f=()=>{const p=Math.min(1,(performance.now()-t0)/DUR),e=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;"
         "c.scrollTop=DESTINO;p<1?requestAnimationFrame(f):res()};requestAnimationFrame(f)});")


def js_rola_ate(texto, y=250, escopo='main', dur_ms=700, prefixo=False):
    """rolagem suave do contêiner que rola o alvo (o menor elemento visível com o texto) até ele ficar em y px CSS; o cursor não se mexe.
    Devolve o topo final do alvo (px CSS), 'ok' (já estava lá), 'SEM ALVO' ou 'SEM ROLAGEM'."""
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


def js_clicar(seletor, texto=None):
    """clique por eval (sem cursor): para o que acontece por baixo de uma ilustração"""
    filtro = f".filter(e=>e.textContent.trim()==={json.dumps(texto, ensure_ascii=False)})" if texto else ''
    return (f"(()=>{{const el=[...document.querySelectorAll({json.dumps(seletor)})]{filtro}.filter(e=>e.offsetParent!==null)[0];"
            "if(!el)return 'SEM ALVO';el.click();return 'ok'})()")


JS_TIPOS = ("(()=>{const t=[...document.querySelectorAll('main tbody tr > td:nth-child(4)')].map(e=>e.innerText.trim()).filter(Boolean);"
            "return 'tipos na lista: '+[...new Set(t)].join(', ')+' ('+t.length+' linhas)'})()")
JS_PAPELAO = ("(()=>{const v=[...document.querySelectorAll('main tbody tr')].filter(r=>/Papel[ãa]o/.test(r.innerText)&&/-370|-30 Kg/.test(r.innerText));"
              "if(!v.length)return 'OK: papelão negativo fora da lista';const r=v[0].getBoundingClientRect();"
              "return (r.top<innerHeight&&r.bottom>0?'DIFERENTE: papelão negativo VISÍVEL ':'OK: papelão negativo só abaixo da dobra ')+'(y '+Math.round(r.top)+')'})()")
JS_PDF_GANCHO = ("(()=>{if(window.__pdfs)return 'ja';window.__pdfs=[];const o=URL.createObjectURL.bind(URL);"
                 "URL.createObjectURL=(b)=>{try{if(b&&b.type==='application/pdf')window.__pdfs.push(b)}catch(e){}return o(b)};return 'gancho'})()")


def js_pdf(k, nome):
    """devolve o k-ésimo PDF que o app gerou (base64) para o actions.json (a edição mostra a aba do PDF como ilustração)"""
    return ("(async()=>{for(let i=0;i<30&&!(window.__pdfs&&window.__pdfs.length>%d);i++)await new Promise(r=>setTimeout(r,200));"
            "const b=window.__pdfs&&window.__pdfs[%d];if(!b)return 'SEM PDF';const u=new Uint8Array(await b.arrayBuffer());let s='';"
            "for(let i=0;i<u.length;i+=8192)s+=String.fromCharCode.apply(null,u.subarray(i,i+8192));return {pdf:%s,bytes:u.length,b64:btoa(s)}})()") % (
        k, k, json.dumps(nome))


# ---------------------------------------------------------------- PDF e HTML na tela (20/11): a gravação filma uma aba só
POPS = "(()=>{const o=window.open;window.__pops=[];window.open=function(...a){const w=o.apply(this,a);window.__pops.push(w);return w};return 'ok'})()"
# o PDF do Kardex que o app abre na aba nova (iframe #pdf-frame), devolvido em base64 ('PDF:<base64>') para a ilustração da edição
PDF_JS = ("(async()=>{const w=(window.__pops||[]).slice(-1)[0];if(!w)return 'SEM JANELA';for(let i=0;i<60;i++){let f=null;"
          "try{f=w.document&&w.document.querySelector('#pdf-frame')}catch(e){return 'ERRO '+e}"
          "if(f&&f.src){const b=await (await fetch(f.src.split('#')[0])).blob();const u=new Uint8Array(await b.arrayBuffer());let s='';"
          "for(let k=0;k<u.length;k+=8192)s+=String.fromCharCode.apply(null,u.subarray(k,k+8192));return 'PDF:'+btoa(s)}"
          "await new Promise(r=>setTimeout(r,250))}return 'SEM PDF'})()")
# o Relatório de Estoque abre uma aba com HTML escrito pelo app: devolvido ('HTML:<base64>') quando o texto esperado aparece
HTML_JS = ("(async()=>{let w;for(let i=0;i<60&&!(w=(window.__pops||[]).slice(-1)[0]);i++)await new Promise(r=>setTimeout(r,250));if(!w)return 'SEM JANELA';const espera=%s;for(let i=0;i<60;i++){let t='';"
           "try{t=(w.document&&w.document.documentElement&&w.document.documentElement.textContent)||''}catch(e){return 'ERRO '+e}"
           "if(t&&espera.every(x=>t.toLowerCase().includes(x.toLowerCase()))){const h='<!doctype html>'+w.document.documentElement.outerHTML;const u=new TextEncoder().encode(h);let s='';"
           "for(let k=0;k<u.length;k+=8192)s+=String.fromCharCode.apply(null,u.subarray(k,k+8192));return 'HTML:'+btoa(s)}"
           "await new Promise(r=>setTimeout(r,250))}let d='';try{d=' pops='+window.__pops.length+' fechada='+w.closed+' texto='+((w.document.documentElement&&w.document.documentElement.textContent)||'').slice(0,160)}catch(e){d=' '+e}return 'SEM HTML'+d})()")


def html_js(espera):
    return HTML_JS % json.dumps(list(espera), ensure_ascii=False)


# troca a hora da Posição de Estoque (input type=time): o valor entra pelo setter nativo e o React recebe o evento
JS_HORA = ("(()=>{const el=document.querySelector(\"input[aria-label='Hora']\");if(!el)return 'SEM HORA';"
           "const set=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set;set.call(el,'%s');"
           "el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true}));return el.value})()")


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
HIST = vai('/historico-materiais', 'Geral (Todos)')
REL = vai('/relatorio-estoque', 'Análise detalhada de compras, vendas e lucro por material')
POS = vai('/materiais/posicao-estoque', 'Escolha a data')
RECOLHE = [{'do': 'click', 'target': TOGGLE_MENU, 'noScroll': True}, {'do': 'pause', 'seconds': 0.8},
           {'do': 'scroll', 'point': {'x': 700, 'y': 420}, 'by': 0, 'duration': 0.2, 'after': 0}]


def setup_estoque(extra=()):
    """login, Estoque com o menu lateral recolhido"""
    return setup_login() + ESTOQUE + RECOLHE + list(extra)


def setup_kardex(material='Ferro pesado', periodo=None):
    st = setup_login() + ESTOQUE + RECOLHE + HIST + [
        {'do': 'click', 'target': KMAT(material)}, {'do': 'waitFor', 'target': KROW('Compra'), 'timeout': 15}, {'do': 'waitFor', 'idle': True}]
    if periodo:
        st += [{'do': 'click', 'target': FILTROS}, {'do': 'waitFor', 'text': 'Filtros do Kardex', 'timeout': 8},
               {'do': 'click', 'target': COMBO('Este mês', DLG)}, {'do': 'click', 'target': OPT(periodo)}, {'do': 'pause', 'seconds': 0.6},
               {'do': 'click', 'target': BTN('Aplicar filtros'), 'noScroll': True}, {'do': 'waitFor', 'gone': {'role': 'dialog'}, 'timeout': 8},
               {'do': 'waitFor', 'idle': True}]
    return st + [{'do': 'scroll', 'point': {'x': 700, 'y': 420}, 'by': 0, 'duration': 0.2, 'after': 0}]


def setup_relatorio(periodo=None):
    st = setup_login() + ESTOQUE + RECOLHE + REL
    if periodo:
        st += [{'do': 'click', 'target': COMBO('Este mês')}, {'do': 'click', 'target': OPT(periodo)}, {'do': 'waitFor', 'idle': True},
               {'do': 'pause', 'seconds': 0.8}]
    return st + [{'do': 'scroll', 'point': {'x': 700, 'y': 420}, 'by': 0, 'duration': 0.2, 'after': 0}]


def escolhe_31_10():
    """Posição de Estoque: calendário -> outubro -> dia 31 (a hora fica 23:59) -> Ver posição (no setup)"""
    return [{'do': 'click', 'target': DATA_BTN('10/11/2026')}, {'do': 'waitFor', 'target': PREV_MES, 'timeout': 8},
            {'do': 'click', 'target': PREV_MES}, {'do': 'pause', 'seconds': 0.4}, {'do': 'click', 'target': DIA('31')},
            {'do': 'pause', 'seconds': 0.5}, {'do': 'click', 'target': BTN('Ver posição')},
            {'do': 'waitFor', 'text': 'Posição de estoque em 31/10/2026 23:59', 'timeout': 15}, {'do': 'waitFor', 'idle': True}]


def abre_acoes(c, nome, item, w, label=None, w_item=None):
    """menu "..." da linha (HoverDropdownMenu: abre ao PASSAR o mouse; um clique no gatilho FECHARIA o menu aberto pelo hover): hover,
    um 2º hover só se o item ainda não apareceu, e o clique no item"""
    c.hover(ACOES(nome), 0.4, w=w, label=label or f'"..." da linha {nome}', optional=False, timeout=8)
    c.hover(ACOES(nome), 0.3, label='"..." de novo (só se não abriu)', unless=ITEM(item))
    c.waitfor(target=ITEM(item), timeout=6)
    return c.click(ITEM(item), w=w_item, label=item)


# ================================================================ capítulos
def cap00():
    """Abertura: Dashboard (menu aberto); L1-L2 sob a ilustração das três perguntas; L3 o cursor no menu Materiais (sem abrir); L4 cartão
    "Antes" (edição) e o cursor sai do menu."""
    c = Cap(0, setup_login() + vai('/materiais', 'Gerencie os materiais do estoque') + vai('/dashboard', 'Olá, Rafael!'), start=(760, 420))
    c.hover(MENU_GRUPO('Materiais'), 2.2, w=(3, 'Materiais,', None, 1.2), label='[ZOOM] menu Materiais (sem abrir)')
    c.cursor((760, 420), w=(4, 'Se', None, 0.0), label='o cursor sai do menu')
    c.fim()
    return c


def cap01():
    """As quatro portas: Materiais abre o grupo (Estoque, Histórico (Kardex), Relatório, Ticket de Pesagem, Produção); Estoque; a coluna
    Tabelas de Preço até "Posição de Estoque" (sem clicar); L3 (1.60.18) só falada: o botão da empresa com uma tabela só; L4 sob a
    ilustração (o menu recolhe por eval); L5 quadro geral."""
    c = Cap(1, setup_login() + vai('/materiais', 'Gerencie os materiais do estoque') + vai('/dashboard', 'Olá, Rafael!'), start=(760, 420))
    c.click(MENU_GRUPO('Materiais'), w=(1, 'Materiais,'), primeiro=True, label='menu Materiais (abre o grupo)')
    c.waitfor(target=MENU_LINK('Relatório'), timeout=6)
    c.registra(MENU_LINK('Histórico (Kardex)'), w=(1, 'três'), label='[ZOOM] submenu: Estoque, Histórico (Kardex), Relatório (o do meio)')
    c.hover(MENU_LINK('Relatório'), 1.0, w=(1, 'Estoque,', None, 0.9), label='o cursor desce por Estoque e Histórico (Kardex) até Relatório')
    c.click(MENU_LINK('Estoque'), w=(2, 'Estoque,', 0), label='Estoque')
    c.waitfor(text='Gerencie os materiais do estoque', timeout=15)
    c.registra(P('Tabelas de Preço', exact=True), w=(2, 'coluna'), label='coluna Tabelas de Preço')
    c.hover(BTN('Posição de Estoque'), 1.0, w=(2, 'Posição'), label='[ZOOM] Posição de Estoque, embaixo de Nova Tabela (sem clicar)')
    c.confere('main', ['Tabelas de Preço', 'Tabela Depósitos', 'Nova Tabela', 'Posição de Estoque'], 'coluna das tabelas com a Posição de Estoque')
    # L3 (só falada): o botão do cabeçalho de quem tem uma tabela de preço só não é gravado; o cursor segue na Posição de Estoque
    c.hover(BTN('Posição de Estoque'), 2.4, w=(3, 'tabela'), label='(L3 só falada) o cursor segue na Posição de Estoque da coluna')
    # L4: ilustração das quatro portas cobre a janela; por baixo, o menu lateral recolhe (sem cursor)
    c.ev(js_clicar('header button:has(svg.lucide-panel-left-close)'), w=(4, 'Histórico', None, 0.0), label='recolhe o menu lateral (por baixo da ilustração)')
    c.registra(SEL('main'), w=(5, 'gente', None, 0.0), label='quadro geral da tela Estoque')
    c.fim()
    return c


def cap02():
    """O saldo: os três cartões; Peso Total; Total Pago e Projeção; Cobre mel (42 Kg e R$ 42,50) com a explicação do preço médio; o selo
    estimativa; L6 (1.60.18) dica do triângulo amarelo (só falada: o mundo não tem material sem compra); L7 ilustração; Ferro misto 6.420 Kg."""
    c = Cap(2, setup_estoque())
    c.hover(P('Total Pago', exact=True), 1.4, w=(1, 'cartões'), label='os três cartões de cima')
    c.hover(P('Peso Total em Estoque', exact=True), 2.4, w=(2, 'Peso'), label='[ZOOM] Peso Total em Estoque')
    c.hover(P('Total Pago', exact=True), 1.8, w=(3, 'Total'), label='Total Pago')
    c.hover(P('Projeção de Vendas', exact=True), 2.2, w=(3, 'Projeção'), label='Projeção de Vendas')
    c.ev(js_rola_ate('Lista de Materiais', y=110), w=(4, 'Olha', None, 0.9), label='desce até a Lista de Materiais')
    c.hover(CELULA('Cobre mel', 3), 0.5, w=(4, 'cobre'), label='linha Cobre mel')
    c.hover(CELULA('Cobre mel', 4), 1.4, w=(4, 'quilos'), label='[ZOOM] Estoque Atual do Cobre mel (42 Kg)')
    c.confere('row:Cobre mel', ['Cobre mel', ' 42Kg', 'R$ 42,50'], 'Cobre mel 42 Kg pagos a R$ 42,50')
    # a explicação ("Custo médio ponderado do estoque atual ... Estimativa.") abre ao passar o mouse no VALOR, não no cabeçalho: o cursor
    # fica no R$ 42,50 do L4 até o fim do L5 (a explicação na tela enquanto a fala a resume) e a câmera vai ao selo do cabeçalho
    c.hover(CELULA('Cobre mel', 6), 6.6, w=(4, 'média'), label='[ZOOM] Preço médio pago do Cobre mel (R$ 42,50) e a explicação')
    c.registra(SEL("main thead th:has-text('Preço médio pago') :text-is('estimativa')"), w=(5, 'selo'), label='[ZOOM] selo estimativa')
    # L6 (só falada): diz se algum material do mundo mostra o aviso "Sem histórico de compra" (informativo; o roteiro não depende dele)
    c.ev("(()=>{const t=document.querySelector('main')?.innerText||'';return /Sem histórico de compra/i.test(t)?'AVISO amarelo presente na lista':'sem aviso amarelo na lista (a dica fica só falada)'})()",
         w=(6, 'Uma', None, 0.0), label='confere se algum material mostra o triângulo "Sem histórico de compra"')
    # L7: ilustração "o que mexe no saldo" (robô parado)
    c.hover(CELULA('Ferro misto', 4), 3.0, w=(8, 'ferro'), label='[ZOOM] Estoque Atual do Ferro misto (6.420 Kg)')
    c.confere('row:Ferro misto', ['Ferro misto', ' 6.420Kg'], 'Ferro misto 6.420 Kg')
    c.fim()
    return c


def cap03():
    """Transferir: (L1-L2 ilustração; por baixo a lista sobe) "..." do Ferro misto > Transferir estoque; 6.420 Kg; destino Ferro pesado,
    320; Transferir: 6.100 e 2.500 Kg; marca Cobre mel e Cobre misto: a barra com Transferir Estoque (sem clicar); desmarca."""
    c = Cap(3, setup_estoque())
    c.ev(js_rola_ate('Lista de Materiais', y=110), w=(2, 'entra', None, 0.0), label='a lista sobe (por baixo da ilustração)')
    abre_acoes(c, 'Ferro misto', 'Transferir estoque', w=(3, 'ferro'), w_item=(3, 'clico'))   # hover no "..." custou 2,5 s com a máquina carregada
    c.waitfor(text='Transferir quantidade de Ferro misto', timeout=8)
    c.hover(SEL(f"{DLG} div:has(> label:has-text('Estoque Atual de Ferro misto'))"), 2.4, w=(4, 'estoque'),
            label='[ZOOM] Estoque Atual de Ferro misto 6.420 Kg')
    c.confere('dlg', ['Transferir Estoque', 'Estoque Atual de Ferro misto', '6.420'], 'janela: Estoque Atual de Ferro misto 6.420 Kg')
    c.click(SEL(f'{DLG} #target-material'), w=(5, 'material'), primeiro=True, label='Material de Destino')
    c.type(SEL(f'{DLG} #target-material'), 'ferro pes', w=(5, 'destino,', None, 0.0), clicar=False, cps=24, label='Material de Destino: ferro pes')
    c.click(OPT('Ferro pesado', exact=False), w=(5, 'pesado.'), label='Ferro pesado')
    c.click(SEL(f'{DLG} #transfer-quantity'), w=(5, 'quantidade,'), label='Quantidade a Transferir (Kg)')
    c.type(SEL(f'{DLG} #transfer-quantity'), '320', w=(5, 'trezentos'), clicar=False, label='[ZOOM] Quantidade a Transferir (Kg) 320')
    c.click(BTN('Transferir', within=DLG), w=(6, 'Transferir.'), label='Transferir')
    c.waitfor(text='Transferido 320 Kg de Ferro misto para Ferro pesado', timeout=10)
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.hover(CELULA('Ferro misto', 4), 1.2, w=(6, 'misto'), label='[ZOOM] Ferro misto 6.100 Kg')
    c.hover(CELULA('Ferro pesado', 4), 1.6, w=(6, 'pesado,'), label='[ZOOM] Ferro pesado 2.500 Kg')
    c.confere('main tbody', [' 6.100Kg', ' 2.500Kg'], 'Ferro misto 6.100 Kg e Ferro pesado 2.500 Kg')
    c.click(CHK('Cobre mel'), w=(7, 'quando'), label='marca Cobre mel')
    c.click(CHK('Cobre misto'), w=(7, 'vários'), label='marca Cobre misto')
    c.hover(BARRA('Transferir Estoque'), 2.6, w=(7, 'barra'), noScroll=True, label='[ZOOM] barra de baixo: 2 selecionados e Transferir Estoque (sem clicar)')
    c.confere('div.fixed.bottom-20', ['2', 'selecionados', 'Transferir Estoque'], 'barra: 2 selecionados, Transferir Estoque')
    c.click(CHK('Cobre mel'), w=(7, 'Gerencial,'), label='desmarca Cobre mel')
    c.click(CHK('Cobre misto'), w=(7, 'plano'), label='desmarca Cobre misto')
    c.fim()
    return c


def cap04():
    """Kardex: menu (recolhido) Materiais > Histórico (Kardex); L2 ilustração; Ferro pesado; a Transferência (2.180 > +320 > 2.500) e a
    Compra de 09/11 (+860, final 2.180); L6 ilustração; L7 (1.60.18) colunas Usuário e Pedido da Compra; Filtros sem contador (Este mês);
    Filtros > Período > Este ano > Aplicar."""
    c = Cap(4, setup_estoque())
    c.hover(MENU_GRUPO('Materiais'), 0.3, w=(1, 'Agora', None, 0.4), noScroll=True, label='menu lateral (o menu recolhido abre)')
    # aberto pelo mouse, o menu traz o grupo Materiais FECHADO (ensaio de 11/11): abre o grupo, só se o item ainda não aparece
    c.click(MENU_GRUPO('Materiais'), noScroll=True, unless=MENU_LINK('Histórico (Kardex)'), label='abre o grupo Materiais')
    c.click(MENU_LINK('Histórico (Kardex)'), w=(1, 'Kardex'), noScroll=True, label='Histórico (Kardex)')
    c.waitfor(text='Geral (Todos)', timeout=15)
    c.ev(JS_PAPELAO, label='confere o papelão negativo (Kardex Geral) fora da tela')
    c.cursor((760, 420), w=(1, 'estoque.', None, 0.0), label='o cursor sai do menu (ele recolhe)')
    # L2: ilustração "Kardex é um extrato" (robô parado)
    c.click(KMAT('Ferro pesado'), w=(3, 'ferro'), label='Ferro pesado na coluna Materiais')
    c.waitfor(target=KROW('Transferência'), timeout=10)
    c.hover(KBADGE('Transferência'), 1.6, w=(3, 'transferência'), label='a Transferência de hoje, em cima')
    c.confere('row:Transferência', ['Transferência', '2.180 Kg', '+320 Kg', '2.500 Kg'], 'Transferência: 2.180 > +320 > 2.500 Kg')
    c.registra(KROW('Transferência'), w=(4, 'esquerda'), label='[ZOOM] linha Transferência: Estoque Inicial, Movimentação e Estoque Final')
    c.hover(KCEL('Transferência', 7), 1.4, w=(4, 'tinha'), label='Estoque Inicial 2.180 Kg')
    c.hover(KCEL('Transferência', 8), 1.2, w=(4, 'entraram'), label='Movimentação +320 Kg')
    c.hover(KCEL('Transferência', 9), 1.4, w=(4, 'ficou'), label='Estoque Final 2.500 Kg')
    c.hover(KCEL('+860 Kg', 8), 1.4, w=(5, 'compra'), label='a Compra de ontem: +860 Kg')
    c.confere('row:+860 Kg', ['Compra', '1.320 Kg', '+860 Kg', '2.180 Kg'], 'Compra de 09/11: 1.320 > +860 > 2.180 Kg')
    c.hover(KCEL('+860 Kg', 9), 1.4, w=(5, 'final'), label='[ZOOM] Estoque Final da compra 2.180 Kg')
    c.hover(KCEL('Transferência', 7), 1.2, w=(5, 'inicial'), label='Estoque Inicial da transferência 2.180 Kg')
    # L6: ilustração "a corrente" (robô parado)
    c.hover(KCEL('+860 Kg', 2), 1.0, w=(7, 'quem'), label='[ZOOM] coluna Usuário da Compra de 09/11')
    c.hover(KCEL('+860 Kg', 5), 1.2, w=(7, 'número'), label='[ZOOM] coluna Pedido da Compra de 09/11 (o número do pedido)')
    c.confere('row:+860 Kg', ['Compra', '#'], 'a Compra de 09/11 mostra usuário e o número do pedido')
    c.hover(FILTROS, 1.0, w=(8, 'Este'), label='Filtros (sem contador): o Histórico abre em Este mês')
    c.hover(TH('Data'), 0.6, w=(8, 'dez', 1), label='coluna Data: só novembro')
    c.click(FILTROS, w=(9, 'ver'), label='Filtros')
    c.waitfor(text='Filtros do Kardex', timeout=8)
    c.click(COMBO('Este mês', DLG), w=(9, 'período'), primeiro=True, label='Período (abre a lista)')
    c.hover(OPT('Este ano'), 0.3, w=(9, 'Este'), label='Este ano')
    c.hover(OPT('Todos os tempos'), 0.5, w=(9, 'Todos'), label='Todos os tempos')
    c.click(OPT('Este ano'), w=(9, 'Assim,'), label='escolhe Este ano')
    c.click(BTN('Aplicar filtros'), noScroll=True, w=(9, 'abre'), label='Aplicar filtros')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.hover(FILTROS, 1.2, w=(9, 'histórico'), label='[ZOOM] Filtros com 1')
    c.ev(js_rola_ate('Edição Manual', y=420), w=(9, 'sumiu:', None, 0.0), label='desce: entram as linhas de outubro')
    c.confere('main', ['Edição Manual', '31/10'], 'Este ano: entram as linhas de outubro')
    c.fim()
    return c


def cap05():
    """Tipos: (setup: Ferro pesado em Este ano) os selos; Filtros > Tipo de movimentação (os sete); L3-L5 ilustração; marca Edição Manual e
    Exclusão; a linha de 31/10 aberta; L8 (1.60.18) dica do Editar (só falada); a Exclusão de 22/10; Fornecedores = Siqueira (desde a
    1.60.18 só ficam as COMPRAS dele: sem Transferência, Edição Manual, Exclusão nem Venda); Limpar."""
    c = Cap(5, setup_kardex('Ferro pesado', 'Este ano'))
    c.hover(KBADGE('Transferência'), 0.3, w=(1, 'Cada', None, 0.4), label='selo Transferência')
    c.hover(KBADGE('Compra'), 0.3, w=(1, 'tipo,'), label='selo Compra')
    c.hover(KBADGE('Venda'), 0.4, w=(1, 'cor.'), label='selo Venda')
    c.click(FILTROS, w=(2, 'filtro'), label='Filtros')
    c.waitfor(text='Filtros do Kardex', timeout=8)
    c.click(BTN('Tipo de movimentação', within=DLG), w=(2, 'todos'), primeiro=True, label='Tipo de movimentação (abre a lista)')
    c.waitfor(target=OPCAO('Saldo inicial'), timeout=6)
    c.confere(POP, ['Compra', 'Venda', 'Transferência', 'Edição Manual', 'Exclusão', 'Produção', 'Saldo inicial'], 'os sete tipos na lista')
    # L3-L5: ilustração dos tipos (robô parado, a lista aberta por baixo)
    c.click(OPCAO('Edição Manual'), w=(6, 'deixar'), label='marca Edição Manual')
    c.click(OPCAO('Exclusão'), w=(6, 'dois'), label='marca Exclusão')
    c.click(BTN('Aplicar filtros'), noScroll=True, w=(6, 'No'), label='Aplicar filtros (fecha a lista e a folha)')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.ev(JS_TIPOS, label='tipos na lista (Edição Manual e Exclusão)')
    c.hover(KCEL('Edição Manual', 3), 0.8, w=(6, 'sábado,'), label='Data 31/10 da Edição Manual')
    c.hover(KCEL('Edição Manual', 8), 1.4, w=(6, 'menos'), label='[ZOOM] Edição Manual de 31/10: -14 Kg')
    c.confere('row:Edição Manual', ['31/10', '41.874 Kg', '-14 Kg', '41.860 Kg'], 'Edição Manual de 31/10: 41.874 > -14 > 41.860 Kg')
    c.click(KCEL('Edição Manual', 6), w=(7, 'Abrindo'), label='abre a linha da Edição Manual')
    c.waitfor(text='Contagem do pátio no fechamento do mês', timeout=8)
    c.hover(SEL("main div.items-start:has(> div > div:text-is('Observação'))"), 1.4, w=(7, 'observação'), label='[ZOOM] Observação: Contagem do pátio no fechamento do mês')
    c.hover(SEL("main div.items-center:has(> span:text-is('Estoque'))"), 1.2, w=(7, 'estoque'), label='[ZOOM] Estoque 41.874 Kg -> 41.860 Kg')
    c.hover(SEL('main div.flex-wrap:has(svg.lucide-clock)'), 1.0, w=(7, 'quem'), label='Rafael Nogueira e a hora')
    c.confere('main', ['Saída', 'Contagem do pátio no fechamento do mês', '41.874 Kg', '41.860 Kg', 'Rafael Nogueira', '31/10/2026'],
              'linha aberta: Saída, observação, 41.874 > 41.860, Rafael, 31/10')
    # L8 (só falada): a dica do Editar; a linha aberta segue na tela, o cursor parado
    c.hover(SEL('main div.flex-wrap:has(svg.lucide-clock)'), 6.0, w=(8, 'Edição', None, 0.2), label='(L8 só falada) a linha aberta segue na tela')
    c.hover(KCEL('Exclusão', 8), 1.6, w=(9, 'aqui,'), label='[ZOOM] Exclusão de 22/10: -180 Kg')
    c.hover(KCEL('Exclusão', 3), 1.0, w=(9, 'repetida'), label='Data 22/10 da Exclusão')
    c.confere('row:Exclusão', ['22/10', '-180 Kg'], 'Exclusão de 22/10: -180 Kg')
    c.click(FILTROS, w=(10, 'Uma'), label='Filtros')
    c.waitfor(text='Filtros do Kardex', timeout=8)
    c.click(BTNX('Tipo de movimentação', within=DLG), w=(10, 'filtros'), primeiro=True, label='Tipo de movimentação')
    c.click(SEL(f"{POP} button:has-text('Desmarcar todos')"), w=(10, 'Fornecedores'), label='Desmarcar todos')
    c.press('Escape', label='fecha a lista dos tipos (o painel dos filtros segue aberto)')
    c.waitfor(gone={'selector': POP}, timeout=4, optional=True)
    c.click(BTN('Fornecedores', within=DLG), w=(10, 'Clientes:'), label='Fornecedores (abre a lista)')
    c.click(BTN('Fornecedores', within=DLG), label='Fornecedores de novo (só se a lista não abriu)', unless=OPCAO('Depósito Irmãos Siqueira'))
    c.waitfor(target=OPCAO('Depósito Irmãos Siqueira'), timeout=8)
    c.click(OPCAO('Depósito Irmãos Siqueira'), w=(10, 'fornecedor'), label='marca Depósito Irmãos Siqueira')
    c.press('Escape', label='fecha a lista dos fornecedores')
    c.click(BTN('Aplicar filtros'), noScroll=True, w=(10, 'compras'), label='Aplicar filtros')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.ev(JS_TIPOS, label='tipos na lista (só Compra)')
    c.registra(SEL('main tbody'), w=(11, 'saem'), label='a lista só com Compra: sem Transferência, Edição Manual, Exclusão nem Venda')
    c.hover(KBADGE('Compra'), 1.2, w=(11, 'cliente.'), label='só as compras do Siqueira')
    c.click(FILTROS, w=(12, 'ver'), label='Filtros')
    c.waitfor(text='Filtros do Kardex', timeout=8)
    c.click(BTN('Limpar filtros'), noScroll=True, w=(12, 'limpar'), label='Limpar filtros')
    c.click(BTN('Aplicar filtros'), noScroll=True, w=(12, 'filtros.'), label='fecha a folha (a lista volta em Este mês)')
    c.fim()
    return c


def cap06():
    """O pedido: (setup: Kardex do Ferro pesado, Este mês) a compra de 09/11 aberta: item (860 Kg, R$ 0,95, R$ 817,00); Fornecedor,
    Formas de Pagamento (Pix), Total do Pedido; Fotos anexadas: a 1ª amplia e fecha."""
    c = Cap(6, setup_kardex('Ferro pesado'))
    c.hover(KCEL('+860 Kg', 4), 0.8, w=(1, 'compra', 0), label='linha Compra de 09/11')
    c.hover(KBADGE('Venda'), 0.6, w=(1, 'venda'), label='linha Venda')
    c.click(KCEL('+860 Kg', 6), w=(1, 'Clicando'), label='abre a compra de ontem')
    c.waitfor(text='Valor Unit.', timeout=10)
    c.registra(SEL("main table table tbody tr:has-text('Ferro pesado')"), w=(2, 'Oitocentos', 0), label='[ZOOM] item: Ferro pesado, Peso 860 Kg, Valor Unit. R$ 0,95, Total R$ 817,00')
    c.hover(ITEM_CEL(2), 1.4, w=(2, 'sessenta'), label='Peso 860 Kg')
    c.hover(ITEM_CEL(3), 1.4, w=(2, 'noventa'), label='Valor Unit. R$ 0,95')
    c.hover(ITEM_CEL(4), 1.2, w=(2, 'dezessete'), label='Total R$ 817,00')
    # `row:` e a tabela de dentro: o seletor `:has-text` é do Playwright e não vale no querySelectorAll do `confere` (varredura 1.60.18)
    c.confere('main table table', ['Ferro pesado', '860 Kg', 'R$ 0,95', 'R$ 817,00'], 'item 860 Kg a R$ 0,95 = R$ 817,00')
    c.ev(js_rola_ate('Fornecedor:', y=300), w=(3, 'Embaixo,', None, 0.3), label='desce até o Fornecedor')
    c.hover(SEL("main table table div:has(> span:text-is('Fornecedor:'))"), 1.8, w=(3, 'fornecedor,'), label='[ZOOM] Fornecedor: Depósito Irmãos Siqueira')
    c.hover(SEL("main table table div:text-is('Formas de Pagamento')"), 1.2, w=(3, 'pago,'), label='Formas de Pagamento: Pix/Transferência R$ 817,00')
    c.hover(SEL("main table table td:text-is('Total do Pedido:')"), 1.2, w=(3, 'total'), label='[ZOOM] Total do Pedido: R$ 817,00')
    c.confere('main table table', ['Depósito Irmãos Siqueira', 'Pix/Transferência: R$ 817,00', 'Total do Pedido:'], 'Siqueira, Pix R$ 817,00, total')
    c.hover(P('Fotos anexadas', exact=True), 1.0, w=(4, 'fotos'), label='Fotos anexadas (duas miniaturas)')
    c.click(FOTO(1), w=(4, 'Clicando,'), label='a primeira foto (amplia)')
    c.waitfor(target=SEL('div[role=dialog] img'), timeout=8)
    c.press('Escape', w=(5, 'Quando'), label='fecha a foto')
    c.waitfor(gone={'selector': 'div[role=dialog] img'}, timeout=6)
    c.registra(SEL('main tbody tr:has(table)'), w=(5, 'aqui:'), label='o pedido, o pagamento e as fotos na mesma linha')
    c.fim()
    return c


def cap07():
    """(NOVO 1.60.18) Achar uma movimentação: (setup: Kardex Geral) busca "cobre" e Ordenar > Nome; Ferro pesado; Filtros > Período >
    Personalizado 01 a 07/11; volta a Este mês e Quantidade movimentada Igual a 860; Clientes = Aços Quiririm: a venda de 04/11 aberta;
    Limpar filtros; Exportar > PDF (janela do Kardex); Exportar PDF (o PDF vai para o actions.json); Exportar > Excel; Como funciona?."""
    c = Cap(7, setup_login() + ESTOQUE + RECOLHE + HIST + [{'do': 'eval', 'js': POPS},
                                                           {'do': 'scroll', 'point': {'x': 700, 'y': 420}, 'by': 0, 'duration': 0.3, 'after': 0}])
    BUSCA = SEL("main input[placeholder='Buscar código ou material']")
    # L1: a busca e o Ordenar da coluna Materiais
    c.ev(JS_PAPELAO, label='confere o papelão negativo (Kardex Geral) fora da tela')
    c.type(BUSCA, 'cobre', w=(1, 'busca'), label='[ZOOM] Buscar código ou material: cobre')
    c.confere('main [role=list]', ['Cobre mel', 'Cobre misto', 'Fio de cobre encapado'], 'a busca "cobre" deixa os três cobres')
    c.press('Control+a', w=(1, 'ou'), label='seleciona a busca')
    c.press('Backspace', label='limpa a busca')
    c.click(BTNX('Ordenar', within='main'), w=(1, 'Ordenar'), label='[ZOOM] Ordenar (Ordenar materiais: Código e Nome)')
    c.waitfor(text='Ordenar materiais', timeout=6)
    c.click(SEL(f"{POP} button:has-text('Nome')"), w=(1, 'pra', None, 0.4), label='Nome')
    c.press('Escape', label='fecha o Ordenar')
    # L2: Ferro pesado e o período Personalizado
    c.click(KMAT('Ferro pesado'), w=(2, 'No', None, 0.3), label='Ferro pesado')
    c.waitfor(target=KROW('Transferência'), timeout=10)
    c.click(FILTROS, w=(2, 'período'), label='Filtros')
    c.waitfor(text='Filtros do Kardex', timeout=8)
    c.click(COMBO('Este mês', DLG), w=(2, 'opções'), primeiro=True, label='Período (abre a lista)')
    c.click(OPT('Personalizado'), w=(2, 'Personalizado'), label='Personalizado')
    c.waitfor(target=SEL("table[role=grid]"), timeout=8)
    c.click(SEL("table[role=grid] button[name='day']:text-is('1')", nth=0), w=(2, 'um'), label='dia 1 (início)')
    c.click(SEL("table[role=grid] button[name='day']:text-is('7')", nth=0), w=(2, 'sete'), label='dia 7 (fim)')
    c.pause(0.6)
    c.press('Escape', label='fecha o calendário')
    c.ev("(()=>{const d=[...document.querySelectorAll('main tbody tr > td:nth-child(3)')].map(e=>e.innerText.trim().slice(0,5));return 'datas na lista: '+[...new Set(d)].join(', ')+' ('+d.length+' linhas)'})()",
         label='datas das linhas (a primeira semana de novembro)')
    # L3: volta a Este mês e a quantidade movimentada
    c.click(SEL(f'{DLG} button[role=combobox]', nth=0), w=(3, 'quando'), label='Período (abre a lista)')
    c.click(OPT('Este mês'), label='volta a Este mês')
    c.click(SEL(f"{DLG} button[aria-label='Operador da quantidade']"), w=(3, 'filtro'), label='Operador da quantidade')
    c.click(OPT('Igual a'), w=(3, 'Igual'), label='Igual a')
    c.type(SEL(f'{DLG} #kardex-quantity'), '860', w=(3, 'oitocentos'), label='[ZOOM] Quantidade movimentada: Igual a 860')
    c.registra(SEL(f"{DLG} #kardex-quantity-help"), w=(3, 'ignora'), label='[ZOOM] Considera o valor sem sinal: 40 encontra +40 e -40.')
    c.ev(JS_TIPOS, label='linhas com 860 (a compra de 09/11)')
    c.confere('main tbody', ['+860 Kg'], 'sobra a compra de 09/11 (+860 Kg)')
    # L4: clientes e a venda aberta
    c.press('Control+a', w=round(c.L(4) - 1.6, 2), label='seleciona a quantidade')
    c.press('Backspace', label='limpa a quantidade')
    c.click(BTN('Clientes', within=DLG), w=(4, 'clientes'), label='Clientes (abre a lista)')
    c.click(OPCAO('Aços Quiririm Ltda'), w=(4, 'pra'), label='marca Aços Quiririm Ltda')
    c.press('Escape', label='fecha a lista dos clientes')
    c.click(BTN('Aplicar filtros'), noScroll=True, w=(4, 'Abrindo', None, 1.4), label='Aplicar filtros')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.ev(JS_TIPOS, label='tipos na lista (só as vendas dele)')
    c.click(KCEL('-38.992 Kg', 6), w=(4, 'dia'), label='abre a venda de 04/11')
    c.waitfor(text='Total do Pedido:', timeout=10)
    c.registra(SEL("main table table"), w=(4, 'cliente,'), label='[ZOOM] a venda aberta: Cliente, itens, Formas de Pagamento e Total do Pedido')
    c.confere('main table table', ['Aços Quiririm', 'Formas de Pagamento', 'Total do Pedido:'], 'venda de 04/11: cliente, pagamento e total')
    # L5: limpar e abrir a janela do Exportar
    c.click(FILTROS, w=round(c.L(5) - 3.4, 2), label='Filtros')
    c.waitfor(text='Filtros do Kardex', timeout=8)
    c.click(BTN('Limpar filtros'), noScroll=True, label='Limpar filtros')
    c.click(BTN('Aplicar filtros'), noScroll=True, label='fecha a folha')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.click(BTN('Exportar'), w=(5, 'Exportar,'), label='Exportar (abre o menu)')
    c.waitfor(target=ITEM('PDF'), timeout=6)
    c.click(ITEM('PDF'), w=(5, 'janela'), label='PDF')
    c.waitfor(text='Exportar Kardex (PDF)', timeout=8)
    c.registra(PD('Escolha o recorte do extrato', exact=False), w=(5, 'mudar'), label='[ZOOM] Escolha o recorte do extrato. Mudar os filtros aqui não altera os filtros da tela.')
    c.confere('dlg', ['Exportar Kardex (PDF)', 'Escolha o recorte do extrato', 'Ferro pesado'], 'janela do Kardex (PDF) com o Ferro pesado')
    # L6: exportar o PDF; depois o Excel
    c.click(BTN('Exportar PDF', within=DLG), w=(6, 'Exportar,'), label='Exportar PDF (o PDF abre noutra aba)')
    c.waitfor(text='Kardex exportado em PDF', timeout=25)
    c.ev(PDF_JS, label='PDF do Kardex do Ferro pesado (aba nova, para a ilustração)')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.pause(0.5)
    c.click(BTN('Exportar'), w=(6, 'Excel,'), label='Exportar (abre o menu)')
    c.click(BTN('Exportar'), label='Exportar de novo (só se o menu não abriu)', unless=ITEM('Excel'))
    c.waitfor(target=ITEM('Excel'), timeout=8)
    c.click(ITEM('Excel'), w=(6, 'caminho'), label='Excel')
    c.waitfor(text='Exportar Kardex (Excel)', timeout=8)
    c.click(BTN('Exportar Excel', within=DLG), label='Exportar Excel (o arquivo baixa)')
    c.waitfor(text='Kardex exportado em Excel', timeout=15)
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    # L7: o aviso do recorte grande e o Como funciona?
    c.hover(BTNX('Como funciona?'), 2.4, w=(7, 'Como', None, 0.6), label='[ZOOM] Como funciona? (sem abrir)')
    c.fim()
    return c


def cap08():
    """Relatório: menu (recolhido) Materiais > Relatório; Este mês > Mês passado; os quatro cartões; Total Comprado aberto; L6 (1.60.18)
    Total Vendido e Lucro abertos e a Distribuição por forma de pagamento; Projeção de Lucro (estimativa) aberta; L8-L10 ilustrações."""
    c = Cap(8, setup_estoque())
    c.hover(MENU_GRUPO('Materiais'), 0.3, w=(1, 'Agora', None, 0.4), noScroll=True, label='menu lateral (o menu recolhido abre)')
    c.click(MENU_GRUPO('Materiais'), noScroll=True, unless=MENU_LINK('Relatório'), label='abre o grupo Materiais')
    c.click(MENU_LINK('Relatório'), w=(1, 'Estoque:'), noScroll=True, label='Relatório')
    c.waitfor(text='Análise detalhada de compras, vendas e lucro por material', timeout=15)
    c.cursor((760, 420), w=(1, 'comprou'), label='o cursor sai do menu (ele recolhe)')
    c.hover(COMBO('Este mês'), 0.6, w=(2, 'Este'), label='período Este mês')
    c.click(COMBO('Este mês'), w=(2, 'escolho'), label='período (abre a lista)')
    c.click(OPT('Mês passado'), w=(2, 'Mês', 1), label='Mês passado')
    c.hover(COMBO('Mês passado'), 3.0, w=(3, 'dica:'), label='[ZOOM] período Mês passado')
    c.hover(BTN('Total Comprado'), 0.5, w=(4, 'Total', 0), label='cartão Total Comprado')
    c.hover(BTN('Total Vendido'), 0.4, w=(4, 'Total', 1), label='cartão Total Vendido')
    c.hover(BTN('Lucro'), 0.2, w=(4, 'Lucro', 0), label='cartão Lucro')
    c.hover(BTN('Projeção de Lucro'), 0.8, w=(4, 'Projeção'), label='cartão Projeção de Lucro')
    c.click(BTN('Total Comprado'), w=(5, 'Clicando'), label='abre Total Comprado')
    c.waitfor(text='Preço médio de compra', timeout=6)
    c.hover(P('Preço médio de compra', exact=True), 1.0, w=(5, 'preço'), label='Preço médio de compra')
    c.hover(P('Material que mais comprou', exact=True), 1.2, w=(5, 'material'), label='Material que mais comprou')
    # L6 (1.60.18): Total Vendido e Lucro abrem do mesmo jeito; a Distribuição por forma de pagamento
    c.click(BTN('Total Vendido'), w=(6, 'Total'), label='abre Total Vendido')
    c.waitfor(text='Material que mais vendeu', timeout=6)
    c.click(BTN('Lucro'), w=(6, 'Lucro'), label='abre Lucro')
    c.waitfor(text='Material mais lucrativo', timeout=6)
    c.hover(P('Material que mais vendeu', exact=True), 1.0, w=(6, 'vendeu'), label='Material que mais vendeu')
    c.hover(P('Material mais lucrativo', exact=True), 1.0, w=(6, 'lucrativo,'), label='Material mais lucrativo e a margem')
    c.ev(js_rola_ate('Distribuição por forma de pagamento', y=300, prefixo=True), w=(6, 'embaixo', None, 0.3), label='desce até a Distribuição por forma de pagamento')
    c.hover(P('Distribuição por forma de pagamento', exact=True, nth=0), 2.6, w=(6, 'dinheiro,'), label='[ZOOM] Distribuição por forma de pagamento: Dinheiro, Pix/Transferência, Saldo e Em aberto')
    c.confere('main', ['Distribuição por forma de pagamento', 'Dinheiro', 'Pix/Transferência', 'Saldo', 'Em aberto'], 'a distribuição por forma de pagamento')
    c.ev(js_rola_topo(), w=(7, 'A', None, 0.9), label='volta ao topo')
    c.click(BTN('Projeção de Lucro'), w=(7, 'Projeção'), label='abre Projeção de Lucro')
    c.hover(P('Estimativa: assume a venda', exact=False), 1.6, w=(7, 'estimativa.'), label='[ZOOM] explicação da Projeção de Lucro (estimativa)')
    c.confere('main', ['Total Comprado', 'Total Vendido', 'Lucro', 'Projeção de Lucro', 'Preço médio de compra', 'Material que mais comprou'], 'os quatro cartões e os detalhes')
    # L8-L10: ilustrações (robô parado)
    c.fim()
    return c


def cap09():
    """Material por material: (setup: Mês passado) Detalhamento; Cobre mel 980,000 / R$ 41.650,00 / R$ 42,50; L3 ilustração; 1.000,000 /
    R$ 47.900,00 / R$ 47,90; L5 ilustração; Lucro s/ Vendas (cabeçalho e R$ 5.400,00); Bateria automotiva 1.320,000 e 0,000; L8 (1.60.18) o
    balão do Resultado da bateria (R$ 0,00, nunca negativo)."""
    c = Cap(9, setup_relatorio('Mês passado'))
    c.ev(js_rola_ate('Detalhamento por Material', y=110, dur_ms=900), w=(1, 'Embaixo', None, 0.0), label='desce até o Detalhamento por Material')
    c.hover(RCEL('Cobre mel', 2), 0.6, w=(2, 'cobre'), label='linha Cobre mel')
    c.registra(SEL("main tbody tr:has-text('Cobre mel')"), w=(2, 'outubro:'), label='[ZOOM] Cobre mel: Qtd. Comprada 980,000, Valor Comprado R$ 41.650,00, Preço Médio Compra R$ 42,50')
    c.hover(RCEL('Cobre mel', 3), 1.0, w=(2, 'novecentos'), label='Qtd. Comprada 980,000')
    c.hover(RCEL('Cobre mel', 4), 1.4, w=(2, 'quarenta', 0), label='Valor Comprado R$ 41.650,00')
    c.hover(RCEL('Cobre mel', 5), 2.4, w=(2, 'preço'), label='Preço Médio Compra R$ 42,50')
    c.confere('row:Cobre mel', ['980,000', 'R$ 41.650,00', 'R$ 42,50', '1.000,000', 'R$ 47.900,00', 'R$ 47,90', 'R$ 5.400,00', 'R$ 6.250,00', '13,05'],
              'Cobre mel de outubro (compra, venda, lucro s/ vendas, resultado, margem)')
    # L3: ilustração do peso líquido (robô parado)
    c.hover(RCEL('Cobre mel', 6), 1.0, w=(4, 'vendeu'), label='[ZOOM] Qtd. Vendida 1.000,000')
    c.hover(RCEL('Cobre mel', 7), 1.4, w=(4, 'quarenta', 0), label='[ZOOM] Valor Vendido R$ 47.900,00')
    c.hover(RCEL('Cobre mel', 8), 2.0, w=(4, 'quarenta', 1), label='[ZOOM] Preço Médio Venda R$ 47,90')
    # L5: ilustração resultado e margem (robô parado)
    c.hover(TH('Lucro s/ Vendas'), 2.0, w=(6, 'Lucro'), label='cabeçalho Lucro s/ Vendas (abre a explicação; não clicar: ordena)')
    c.hover(RCEL('Cobre mel', 9), 2.0, w=(6, 'cinco'), label='[ZOOM] Lucro s/ Vendas do Cobre mel R$ 5.400,00')
    c.ev(js_rola_ate('Bateria automotiva', y=430), w=(7, 'Uma', None, 0.3), label='desce até a Bateria automotiva')
    c.hover(RCEL('Bateria automotiva', 2), 0.8, w=(7, 'bateria'), label='linha Bateria automotiva')
    c.hover(RCEL('Bateria automotiva', 3), 1.4, w=(7, 'trezentos'), label='[ZOOM] Bateria automotiva: Qtd. Comprada 1.320,000')
    c.hover(RCEL('Bateria automotiva', 6), 1.4, w=(7, 'erro.'), label='[ZOOM] Bateria automotiva: Qtd. Vendida 0,000')
    c.confere('row:Bateria automotiva', ['1.320,000', 'R$ 4.092,00', '0,000'], 'Bateria automotiva 1.320,000 comprados e 0,000 vendidos')
    # L8 (1.60.18): o balão do Resultado (R$ 0,00 e a conta inteira)
    c.hover(RCEL('Bateria automotiva', 10), 4.0, w=(8, 'Resultado', 0), label='[ZOOM] Resultado da bateria (R$ 0,00) e o balão da conta')
    c.confere(POP, ['vendidos', 'comprados', 'prejuízo', 'R$ 0,00'], 'o balão do Resultado: vendidos, comprados, prejuízo e Lucro exibido R$ 0,00')
    c.fim()
    return c


def cap10():
    """Fornecedor: (setup: Mês passado) Fornecedores > Depósito Irmãos Siqueira: só Total Comprado e as colunas de compra; L2 ilustração;
    a tabela só de compra; tira o filtro."""
    c = Cap(10, setup_relatorio('Mês passado'))
    c.click(BTN('Fornecedores'), w=(1, 'filtro'), label='filtro Fornecedores (abre a lista)')
    c.waitfor(target=OPCAO('Depósito Irmãos Siqueira'), timeout=6)
    c.click(OPCAO('Depósito Irmãos Siqueira'), w=(1, 'Depósito'), label='marca Depósito Irmãos Siqueira')
    c.press('Escape', w=(1, 'Ficam'), label='fecha a lista')
    c.hover(BTN('Total Comprado'), 0.8, w=(1, 'compras.'), label='[ZOOM] só o Total Comprado')
    c.confere_ausente('main', 'Total Vendido', 'sem Total Vendido nem Lucro')
    c.hover(SEL('main thead'), 1.2, w=(1, 'colunas'), label='cabeçalho só com as colunas de compra')
    # L2: ilustração "a pilha não tem dono" (robô parado)
    c.registra(SEL('main table'), w=(3, 'Então,'), label='[ZOOM] tabela: Código, Material, Qtd. Comprada, Valor Comprado e Preço Médio Compra')
    c.confere('main thead', ['Código', 'Material', 'Qtd. Comprada', 'Valor Comprado', 'Preço Médio Compra'], 'colunas de compra')
    c.hover(TH('Qtd. Comprada'), 0.8, w=(3, 'comprou'), label='Qtd. Comprada')
    c.hover(TH('Preço Médio Compra'), 1.0, w=(3, 'preço.'), label='Preço Médio Compra')
    c.click(BTN('Depósito Irmãos Siqueira'), w=(4, 'ver'), label='filtro (Depósito Irmãos Siqueira)')
    c.click(OPCAO('Depósito Irmãos Siqueira'), w=(4, 'tirar'), label='desmarca Depósito Irmãos Siqueira')
    c.press('Escape', w=(4, 'filtro.'), label='fecha a lista')
    c.confere('main', ['Total Vendido', 'Lucro', 'Projeção de Lucro'], 'voltam os quatro cartões')
    c.fim()
    return c


def cap11():
    """(NOVO 1.60.18) Clientes, usuários e grupos: (setup: Relatório em Mês passado) Clientes = Fundição Bandeira do Vale; Usuários = Marcos
    Antunes; Grupos = Cobre; Por grupo (Subtotal ...); Ocultar itens zerados; ordena pelo título Resultado e desce até TOTAL. Cada filtro
    é desmarcado (chip, opção, Escape) nos ~2 s antes do seguinte."""
    c = Cap(11, setup_relatorio('Mês passado'))

    def solta(chip, opcao_label, prox):
        """desmarca o filtro (o chip leva o nome do que foi marcado): chip, opção, Escape, nos 2,2 s antes da linha `prox`"""
        c.click(BTN(chip), w=round(c.L(prox) - 2.2, 2), label=f'chip {chip} (abre a lista)')
        c.click(OPCAO(opcao_label), w=round(c.L(prox) - 1.4, 2), label=f'desmarca {opcao_label}')
        c.press('Escape', w=round(c.L(prox) - 0.7, 2), label='fecha a lista')
    # L1: clientes
    c.click(BTN('Clientes'), w=(1, 'clientes'), label='Clientes (abre a lista)')
    c.waitfor(target=OPCAO('Fundição Bandeira do Vale'), timeout=6)
    c.click(OPCAO('Fundição Bandeira do Vale'), w=(1, 'Fundição'), label='marca Fundição Bandeira do Vale')
    c.press('Escape', w=(1, 'Vale,'), label='fecha a lista')
    c.hover(TH('Qtd. Vendida'), 1.2, w=(1, 'quanto'), label='[ZOOM] as colunas de venda só com a Fundição; as de compra não mudam')
    solta('Fundição Bandeira do Vale', 'Fundição Bandeira do Vale', 2)
    # L2: usuários
    c.click(BTN('Usuários'), w=(2, 'usuários'), label='Usuários (abre a lista)')
    c.waitfor(target=OPCAO('Marcos Antunes'), timeout=6)
    c.click(OPCAO('Marcos Antunes'), w=(2, 'pessoa'), label='marca Marcos Antunes')
    c.press('Escape', w=(2, 'lançou.'), label='fecha a lista')
    c.hover(BTN('Total Comprado'), 1.2, w=(2, 'compras'), label='[ZOOM] só o que o Marcos lançou')
    solta('Marcos Antunes', 'Marcos Antunes', 3)
    # L3: grupos
    c.click(BTN('Grupos'), w=(3, 'grupos'), label='Grupos (abre a lista)')
    c.waitfor(target=OPCAO('Cobre'), timeout=6)
    c.click(OPCAO('Cobre'), w=(3, 'Cobre', 0), label='marca o grupo Cobre')
    c.press('Escape', (3, 'e', 1), label='fecha a lista')
    c.hover(BTN('Total Comprado'), 1.0, w=(3, 'cartões'), label='[ZOOM] os cartões somam só o cobre')
    solta('Cobre', 'Cobre', 4)
    # L4: Por grupo
    c.click(SEL("main [aria-label='Ver por grupo']"), w=(4, 'Por'), label='Por grupo')
    c.ev(js_rola_ate('Subtotal Cobre', y=420, prefixo=True), w=(4, 'cada', None, 0.3), label='desce até o Subtotal Cobre')
    c.hover(P('Subtotal Cobre', nth=0, exact=False), 1.2, w=(4, 'faixa'), label='[ZOOM] Subtotal Cobre')
    c.confere('main', ['Subtotal Ferrosos', 'Subtotal Cobre'], 'Por grupo: Subtotal Ferrosos e Subtotal Cobre')
    # L5: volta a Por material e Ocultar itens zerados
    c.ev(js_rola_ate('Detalhamento por Material', y=110), w=round(c.L(5) - 1.8, 2), label='volta ao cabeçalho do Detalhamento')
    c.click(SEL("main [aria-label='Ver por material']"), w=round(c.L(5) - 0.8, 2), label='Por material')
    c.click(BTN('Ocultar itens zerados'), w=(5, 'Ocultar'), label='[ZOOM] Ocultar itens zerados')
    c.hover(SEL('main tbody'), 1.6, w=(5, 'lembra'), label='some o que não girou no mês')
    # L6: ordena por Resultado e a linha TOTAL
    c.click(TH('Resultado'), w=(6, 'Resultado'), label='ordena pelo título Resultado')
    c.ev(js_rola_ate('TOTAL', y=470), w=(6, 'última', None, 0.3), label='desce até a linha TOTAL')
    c.hover(SEL("main tbody tr:has-text('TOTAL')", nth=-1), 1.6, w=(6, 'soma'), label='[ZOOM] a linha TOTAL')
    c.fim()
    return c


def cap12():
    """Posição: Estoque > Posição de Estoque (hoje 23:59); Ferro pesado 2.500,000; L3 ilustração; calendário > outubro > 31; Ver posição;
    Ferro pesado 41.860,000; L7 (1.60.18) hora 12:00 (41.874,000) e volta a 23:59; Valor e Projeção venda; Por grupo; Total geral; a nota
    do rodapé inteira."""
    c = Cap(12, setup_estoque())
    c.click(BTN('Posição de Estoque'), w=(1, 'Posição'), label='Posição de Estoque (coluna Tabelas de Preço)')
    c.waitfor(text='Escolha a data', timeout=15)
    c.hover(DATA_BTN('10/11/2026'), 0.8, w=(1, 'hoje,'), label='data de hoje: 10/11/2026')
    c.hover(HORA, 0.8, w=(1, 'fim'), label='hora 23:59')
    c.confere('main', ['Posição de estoque em 10/11/2026 23:59'], 'título: Posição de estoque em 10/11/2026 23:59')
    c.hover(PCEL('Ferro pesado', 4), 2.6, w=(2, 'ferro'), label='[ZOOM] Ferro pesado, Saldo 2.500,000')
    c.confere('row:Ferro pesado', ['Ferro pesado', '2.500,000'], 'Ferro pesado hoje 2.500,000')
    # L3: ilustração "a foto numa data" (robô parado)
    c.click(DATA_BTN('10/11/2026'), w=(4, 'calendário'), label='data (abre o calendário de novembro)')
    c.waitfor(target=PREV_MES, timeout=6)
    c.click(PREV_MES, w=(4, 'outubro'), label='mês anterior (outubro)')
    c.click(DIA('31'), w=(4, 'trinta'), label='dia 31')
    c.registra(DATA_BTN('31/10/2026'), w=(4, 'hora', None, 0.3), label='[ZOOM] Data e hora (padrão: fim do dia): 31/10/2026 e 23:59')
    c.hover(HORA, 2.0, w=(4, 'vinte'), label='hora 23:59')
    c.click(BTN('Ver posição'), w=(5, 'Ver'), label='Ver posição')
    c.waitfor(text='Posição de estoque em 31/10/2026 23:59', timeout=15)
    c.hover(PCEL('Ferro pesado', 4), 3.0, w=(6, 'ferro'), label='[ZOOM] Ferro pesado, Saldo 41.860,000 em 31/10')
    c.confere('row:Ferro pesado', ['Ferro pesado', '41.860,000'], 'Ferro pesado em 31/10: 41.860,000')
    # L7 (1.60.18): a hora 12:00 (antes da contagem das 12:40) e de volta a 23:59
    c.hover(HORA, 1.0, w=(7, 'mudar'), label='[ZOOM] Hora')
    c.ev(JS_HORA % '12:00', w=(7, 'hora.', None, 0.0), label='troca a hora para 12:00')
    c.click(BTN('Ver posição'), w=(7, 'Ao'), label='Ver posição (12:00)')
    c.waitfor(text='Posição de estoque em 31/10/2026 12:00', timeout=15)
    c.hover(PCEL('Ferro pesado', 4), 3.0, w=(7, 'quarenta'), label='[ZOOM] Ferro pesado, Saldo ao meio-dia de 31/10')
    c.confere('row:Ferro pesado', ['Ferro pesado', '41.874,000'], 'Ferro pesado às 12:00 de 31/10: 41.874,000')
    c.ev(JS_HORA % '23:59', w=round(c.L(8) - 2.6, 2), label='volta a hora para 23:59')
    c.click(BTN('Ver posição'), w=round(c.L(8) - 1.6, 2), label='Ver posição (23:59)')
    c.waitfor(text='Posição de estoque em 31/10/2026 23:59', timeout=15)
    # L8: Valor e Projeção venda
    c.hover(TH('Valor'), 1.2, w=(8, 'valor'), label='coluna Valor')
    c.hover(TH('Projeção venda'), 1.2, w=(8, 'projeção,'), label='coluna Projeção venda')
    # L9: Por grupo
    c.click(SEL("main [aria-label='Ver por grupo']"), w=(9, 'Por', 0), label='Por grupo')
    c.confere('main', ['Subtotal Ferrosos'], 'Por grupo: Subtotal Ferrosos')
    c.hover(P('Subtotal Ferrosos', nth=0, exact=False), 1.6, w=(9, 'subtotal'), label='[ZOOM] Subtotal Ferrosos')
    c.click(SEL("main [aria-label='Ver por material']"), w=round(c.L(10) - 1.6, 2), label='Por material')
    # L10: Total geral
    c.ev(js_rola_ate('Total geral', y=470), w=(10, 'Embaixo,', None, 0.6), label='desce até o Total geral')
    c.hover(TXT('Total geral'), 1.0, w=(10, 'total'), label='[ZOOM] linha Total geral')
    c.confere('main', ['Total geral'], 'Total geral')
    # L11: a nota do rodapé
    c.hover(SEL("main p:has-text('Valores negativos indicam')", nth=0), 3.0, w=(11, 'negativo'), label='[ZOOM] a nota do rodapé inteira')
    c.confere('main', ['Valor = saldo × custo médio das compras até a data', 'Projeção = saldo × preço de venda atual',
                       'Valores negativos indicam movimentações lançadas fora da ordem cronológica',
                       'Itens sem compra registrada até a data aparecem sem valorização'], 'a nota do rodapé: as quatro frases')
    c.fim()
    return c


def cap13():
    """Exportar: (setup: Posição em 31/10 23:59) Exportar > PDF: colunas (tira e põe "Valor do estoque") e materiais; Exportar (o PDF vai
    para o actions.json); Exportar > Excel > Exportar; Relatório de Estoque de outubro: Exportar Relatório (a aba HTML vai para o
    actions.json); Estoque Fiscal só falado."""
    st = setup_estoque() + POS + escolhe_31_10() + [{'do': 'eval', 'js': JS_PDF_GANCHO},
                                                    {'do': 'scroll', 'point': {'x': 700, 'y': 420}, 'by': 0, 'duration': 0.2, 'after': 0}]
    c = Cap(13, st)
    c.click(BTN('Exportar'), w=(1, 'Exportar,', 1), label='Exportar (abre o menu)')
    c.waitfor(target=ITEM('PDF'), timeout=6)
    c.click(ITEM('PDF'), w=(1, 'PDF.'), label='PDF')
    c.waitfor(text='Exportar estoque (PDF)', timeout=8)
    c.hover(PD('Colunas do arquivo', exact=True), 1.0, w=(2, 'colunas'), label='Colunas do arquivo')
    c.confere('dlg', ['Código', 'Material', 'Unidade', 'Saldo', 'Valor do estoque', 'Projeção de venda', 'materiais'], 'as seis colunas e o rodapé')
    COL = {'role': 'checkbox', 'name': 'Valor do estoque', 'exact': True, 'within': DLG}
    c.hover(PD('Grupos', exact=True), 0.8, w=(2, 'arquivo'), label='Grupos (a escolha por família)')
    c.hover(BTNX('Marcar todos', within=DLG), 0.8, w=(2, 'Não'), label='Marcar todos / Desmarcar todos')
    c.click(COL, w=(2, 'tirar'), label='[ZOOM] desmarca a coluna Valor do estoque')
    c.click(COL, w=(2, 'guarda', None, 1.8), label='marca a coluna Valor do estoque de novo')
    c.hover(SEL(f"{DLG} span:has-text(' materiais')"), 1.6, w=(2, 'escolha'), label='rodapé: N de N materiais')
    c.confere('dlg', ['Valor do estoque', 'materiais'], 'a coluna Valor do estoque marcada de novo')
    c.click(BTN('Exportar', within=DLG), w=(3, 'Exportar,'), label='Exportar (o PDF abre noutra aba)')
    c.waitfor(text='Posição de estoque exportada em PDF', timeout=15)
    c.ev(js_pdf(0, 'posicao-estoque-31-10-pdf'), label='PDF da posição de 31/10 (para a edição mostrar a aba)')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.pause(0.5)
    c.click(BTN('Exportar'), w=(4, 'contador'), label='Exportar (abre o menu)')
    c.click(BTN('Exportar'), label='Exportar de novo (só se o menu não abriu)', unless=ITEM('Excel'))
    c.waitfor(target=ITEM('Excel'), timeout=8)
    c.click(ITEM('Excel'), w=(4, 'mesmo'), label='Excel')
    c.waitfor(text='Exportar estoque (Excel)', timeout=8)
    c.click(BTN('Exportar', within=DLG), w=(4, 'baixa'), primeiro=True, label='Exportar (o arquivo baixa)')
    c.waitfor(text='Posição de estoque exportada em Excel', timeout=15)
    # L5: o Relatório de Estoque de outubro e o Exportar Relatório
    c.goto('/relatorio-estoque', w=(5, 'O', 0, 1.4), label='corte: Relatório de Estoque')
    c.waitfor(text='Análise detalhada de compras, vendas e lucro por material', timeout=15)
    c.ev(POPS, label='guarda as abas que o app abrir')
    c.click(COMBO('Este mês'), w=(5, 'Histórico'), label='período (abre a lista)')
    c.click(OPT('Mês passado'), w=(5, 'já'), label='Mês passado')
    c.pause(0.8)
    c.click(BTN('Exportar Relatório'), w=(5, 'pelo'), label='Exportar Relatório (a aba abre)')
    c.ev(html_js(['Relatório de Estoque', 'Cobre mel']), label='HTML do Relatório de Estoque de outubro (aba nova, para a ilustração)')
    # L6: o Estoque Fiscal só falado
    c.cursor((760, 420), w=(6, 'Quem', None, 0.0), label='o cursor sai do botão')
    c.fim()
    return c


def cap14():
    """Recapitulando (a edição monta por cima): Estoque depois da transferência; Kardex do Ferro pesado com a compra aberta e as fotos;
    L3 a busca por 860 e a venda de 04/11 (montagem); Relatório de outubro no Cobre mel e o filtro Fornecedores; L5 clientes, usuários e
    grupos; Posição de 31/10 e o Exportar."""
    c = Cap(14, setup_estoque())
    c.ev(js_rola_ate('Lista de Materiais', y=110), w=(1, 'conferiu', None, 0.3), label='a Lista de Materiais')
    c.hover(CELULA('Ferro misto', 4), 1.4, w=(1, 'transferiu'), label='Ferro misto 6.100 Kg')
    c.hover(CELULA('Ferro pesado', 4), 0.6, w=(1, 'ferro', 1), label='Ferro pesado 2.500 Kg')
    c.goto('/historico-materiais', w=(2, 'Leu', None, 0.0), label='Histórico de Materiais')
    c.ev(JS_PAPELAO, label='confere o papelão negativo (Kardex Geral) fora da tela')
    c.click(KMAT('Ferro pesado'), w=(2, 'linha', 1), label='Ferro pesado')
    c.waitfor(target=KROW('Transferência'), timeout=10)
    c.hover(KBADGE('Transferência'), 0.6, w=(2, 'tipos'), label='os tipos')
    c.click(KCEL('+860 Kg', 6), w=(2, 'abriu'), label='abre a compra de 09/11')
    c.waitfor(text='Fotos anexadas', timeout=10)
    c.ev(js_rola_ate('Fotos anexadas', y=420), w=(2, 'pagamento', None, 0.3), label='o pedido, o pagamento e as fotos')
    # L3: ilustração/montagem (a busca por 860 e a venda aberta): o robô fica na compra aberta
    c.goto('/relatorio-estoque', w=(4, 'No', None, 0.9), label='Relatório de Estoque')
    c.click(COMBO('Este mês'), w=(4, 'comprado,'), label='período')
    c.click(OPT('Mês passado'), w=(4, 'vendido,'), label='Mês passado')
    c.ev(js_rola_ate('Cobre mel', y=420), w=(4, 'resultado', None, 0.5), label='a linha do Cobre mel')
    c.hover(RCEL('Cobre mel', 10), 0.8, w=(4, 'margem'), label='Resultado e Margem do Cobre mel')
    c.ev(js_rola_topo(), w=(4, 'por', None, 0.3), label='volta ao topo')
    c.hover(BTN('Fornecedores'), 0.8, w=(4, 'fornecedor'), label='filtro Fornecedores')
    c.hover(BTN('Clientes'), 0.6, w=(5, 'cliente,'), label='filtro Clientes')
    c.hover(BTN('Usuários'), 0.6, w=(5, 'usuário'), label='filtro Usuários')
    c.hover(BTN('Grupos'), 0.6, w=(5, 'grupo'), label='filtro Grupos')
    c.goto('/materiais/posicao-estoque', w=(6, 'E', 0, 0.9), label='Posição de Estoque')
    c.click(DATA_BTN('10/11/2026'), w=(6, 'foto'), label='data')
    c.click(PREV_MES, w=(6, 'estoque'), label='outubro')
    c.click(DIA('31'), w=(6, 'trinta'), label='dia 31')
    c.click(BTN('Ver posição'), w=(6, 'exportada'), label='Ver posição')
    c.waitfor(text='Posição de estoque em 31/10/2026 23:59', timeout=15)
    c.hover(BTN('Exportar'), 1.0, w=(6, 'Excel'), label='Exportar (PDF e Excel)')
    c.fim()
    return c


CAPS = {f'{n:02d}': globals()[f'cap{n:02d}'] for n in range(15)}

if __name__ == '__main__':
    pedidos = sys.argv[1:] or sorted(CAPS)
    for a in pedidos:
        c = CAPS[f'{int(a):02d}']()
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
