#!/usr/bin/env python3
"""T14 · Bancos, cofre e conciliação bancária (EcoFlix, EcoSistema 1.59.154): gera rec/t14/cap00..cap14.json (roteiros do robô) a partir
da fala ($TUT_HOME/t14/narracao/capNN.json: o estimado até a voz chegar; com a voz, o da voz, sem mudar nada aqui). O cap15
(Recapitulando) é montagem das gravações dos outros capítulos: não tem robô.

Computador 1280x800, Rafael Nogueira (MASTER) na Recicla Vale Metais; FAKE_NOW 2026-11-10T08:30:00-03:00 em todos os capítulos (o mesmo
no Supabase falso e no robô). Rodar de qualquer pasta: `python3 -I rec/t14/gerar.py [NN ...]` (ANCORAS=1 lista as âncoras). Depois:
`node rec/record.mjs rec/t14/capNN.json --check`; ensaio: `python3 -I rec/t14/ensaio.py NN` + `--rapido`; gravação: `rec/t14/t14_rodar.sh NN`.

LOGIN: todo capítulo é "anonymous" e o setup entra pela tela de login com "$TUT_USER"/"$TUT_SENHA" do ambiente (o Supabase falso aceita
qualquer senha; o valor nunca vai para arquivo nem log).

Cada passo é preso a uma palavra da fala: A(linha, 'palavra', folga) = início da palavra − folga (o custo do gesto até o cursor chegar:
clique ~0,6 s, 1º clique numa janela recém-aberta ~1,2 s, hover ~0,5 s; digitação sem clique na palavra − 0,05 s). A palavra casa
INTEIRA (sem acento e pontuação); repetida na linha pede `nth`. Marca Ln 0,9 s antes da linha; um passo que começa até 0,25 s antes da
marca a puxa para o início dele.

Estado de partida (rec/mundo/seeds-extra/t14/, escrito por rec/t14/t14_sementes.py, deltas em ordem): `inicio` (o fim do T13 que o T14
usa) → `apos-cap02` → `apos-cap03` → `apos-cap04` → `apos-cap06` → `apos-cap07` → ... → `apos-cap12`. O extrato OFX é fictício e sai do
rec/t14/t14_ofx.py (rec/t14/arquivos/Extrato_20261101_20261110.ofx).

RESPIRO (só com a fala ESTIMADA): pausas que a voz vai ganhar com o `pausas.py` (planejamento/ecoflix/T14/propostas_fala.md); com a voz
de verdade, as pausas já vêm nela e o RESPIRO deixa de valer.
"""
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TUT = os.path.normpath(os.path.join(HERE, '..', '..'))
AULA = 't14'
NARR = os.path.join(TUT, AULA, 'narracao')
FAKE_NOW = '2026-11-10T08:30:00-03:00'
VERSAO = '1.59.154'
HOJE = FAKE_NOW[:10]
NOMES = ['Abertura', 'A tela e as contas', 'Cadastrar e arquivar contas', 'O cofre e o ajuste de saldo', 'Movimentação, transferência e saque',
         'O que é conciliar', 'Importar o extrato', 'Casar com o sistema', 'Baixar uma conta', 'Criar um lançamento', 'Buscar e aceitar centavos',
         'Ignorar uma linha', 'Valores repetidos', 'Desfazer e cancelar', 'Fechar a conciliação']
_E = [f'{AULA}/inicio', f'{AULA}/apos-cap02', f'{AULA}/apos-cap03', f'{AULA}/apos-cap04', f'{AULA}/apos-cap06', f'{AULA}/apos-cap07', f'{AULA}/apos-cap08',
      f'{AULA}/apos-cap09', f'{AULA}/apos-cap10', f'{AULA}/apos-cap11', f'{AULA}/apos-cap12']
SEMENTE = {0: _E[:1], 1: _E[:1], 2: _E[:1], 3: _E[:2], 4: _E[:3], 5: _E[:4], 6: _E[:4], 7: _E[:5], 8: _E[:6], 9: _E[:7], 10: _E[:8], 11: _E[:9],
           12: _E[:10], 13: _E[:11], 14: _E[:11]}
# respiro na fala ESTIMADA: {cap: [(depois da linha N (1..), segundos)]} (o pausas.py põe o mesmo silêncio na voz de verdade)
RESPIRO = {}

sys.path.insert(0, NARR)
try:
    from tts_textos import CAPS   # noqa: E402
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
    t = re.sub(r'\[[a-z ]+\]', ' ', CAPS.get(n, ''))
    for fala, leg in sorted(TROCAS, key=lambda p: -len(p[0])):
        t = t.replace(fala, leg)
    return [norm(w) for w in t.split() if norm(w)]


def carregar_voz(n):
    d = json.load(open(os.path.join(NARR, f'cap{n:02d}.json'), encoding='utf8'))
    words = [dict(w) for w in d['words']]
    linhas = [dict(li) for li in d['linhas']]
    dur = float(d['dur'])
    if CAPS and texto_atual(n) != [norm(w['w']) for w in words if norm(w['w'])]:
        print(f'  AVISO cap{n:02d}: a fala do capNN.json não é a do tts_textos.py de hoje (rode o preparar_aula.sh de novo)')
    if d.get('estimado'):
        for depois, seg in sorted(RESPIRO.get(n, []), reverse=True):
            t0 = linhas[depois - 1]['e']
            for w in words:
                if w['s'] >= t0:
                    w['s'] = round(w['s'] + seg, 3); w['e'] = round(w['e'] + seg, 3)
            for li in linhas:
                if li['s'] >= t0:
                    li['s'] = round(li['s'] + seg, 3); li['e'] = round(li['e'] + seg, 3)
            dur += seg
    return words, linhas, dur, bool(d.get('estimado'))


def stable_id(chave):
    """o mesmo UUID do `@id:<chave>` das sementes (rec/fakebase/core/util.mjs, stableId)"""
    import hashlib
    h = bytearray(hashlib.sha1(('domiflix-fake:' + chave).encode()).digest())
    h[6] = (h[6] & 0x0F) | 0x50
    h[8] = (h[8] & 0x3F) | 0x80
    x = h[:16].hex()
    return f'{x[:8]}-{x[8:12]}-{x[12:16]}-{x[16:20]}-{x[20:32]}'


def storage():
    uid = stable_id('user.rafael')
    return {'app_version': VERSAO, 'notification_shown_version': VERSAO, 'pwa-install-dismissed': 'true', 'theme': 'light',
            f'daily-tasks-reminder-last-shown-{uid}': HOJE, 'initial-preferences-set': 'true'}


# ---------------------------------------------------------------- observador de avisos de erro (aceite: tem de sair vazio)
OBS = ("(()=>{window.__avisos=[];const re=/N[ãa]o foi poss[ií]vel|Erro ao|Tente novamente|Algo deu errado|Falha ao|Something went wrong|indispon[ií]vel/i;"
       "const chk=(t)=>{t=(t||'').trim();const m=t&&t.match(new RegExp('[^]{0,40}('+re.source+')[^]{0,40}','i'));"
       "if(m&&!/fica indispon/i.test(m[0])&&window.__avisos.length<10)window.__avisos.push(m[0].replace(/[\\n\\r\\t ]+/g,' '))};new MutationObserver(ms=>{for(const m of ms){"
       "m.addedNodes.forEach(n=>chk(n.textContent));if(m.type==='characterData')chk(m.target.textContent)}}).observe(document.body,"
       "{childList:true,subtree:true,characterData:true});chk(document.body.innerText);"
       "setInterval(()=>{document.querySelectorAll('[data-sonner-toast][data-type=error]').forEach(t=>{const s='TOAST DE ERRO: '+t.textContent.trim().slice(0,90);"
       "if(!window.__avisos.includes(s)&&window.__avisos.length<10)window.__avisos.push(s)})},300);return 1})()")


class Cap:
    def __init__(s, n, setup, pace=0.5, cps=40, start=(760, 470)):
        s.n = n
        s.words, s.linhas, s.dur, s.estimado = carregar_voz(n)
        s.steps, s.pending, s.anchors = [], [], []
        s.pace, s.cps, s.start = pace, cps, start
        s.setup = list(setup) + [{'do': 'eval', 'js': OBS}]

    # ---- tempo
    def L(s, i):
        return round(s.linhas[i - 1]['s'], 2)

    def W(s, i, palavra, nth=0, fim=False):
        q = norm(palavra)
        hits = [w for w in s.words if w['linha'] == i - 1 and norm(w['w']) == q]
        if len(hits) <= nth:
            raise SystemExit(f'cap{s.n:02d}: palavra "{palavra}" (#{nth}) não achada na linha {i}: ' + ' '.join(w['w'] for w in s.words if w['linha'] == i - 1))
        return hits[nth]['e' if fim else 's']

    def A(s, i, palavra, folga=0.6, nth=0):
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
            for mt, mi in s.pending:
                if d['at'] < mt <= d['at'] + 0.25:
                    d['at'] = round(mt, 2)
            s.flush(d['at'])
        s.steps.append(d)
        return d

    def mark(s, i):
        t = max(0.0, s.L(i) - 0.9)
        if t <= 0:
            s.steps.append({'do': 'mark', 'name': f'L{i}', 'at': 0})
        else:
            s.pending.append((round(t, 2), i))

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
        return s._p({'do': 'hover', 'target': target, 'seconds': seconds}, at, label, kw)

    def type(s, target, text, at=None, label=None, cps=None, **kw):
        d = {'do': 'type', 'target': target, 'text': text}
        if cps:
            d['cps'] = cps
        return s._p(d, at, label, kw)

    def press(s, key, at=None, label=None, **kw):
        return s._p({'do': 'press', 'key': key}, at, label, kw)

    def upload(s, target, arquivo, at=None, label=None, **kw):
        return s._p({'do': 'upload', 'target': target, 'file': arquivo}, at, label, kw)

    def ev(s, js, at=None, label=None, **kw):
        return s._p({'do': 'eval', 'js': js}, at, label, kw)

    def wait(s, seconds):
        return s.add({'do': 'wait', 'seconds': seconds})

    def waitfor(s, **kw):
        return s.add({'do': 'waitFor', **kw})

    def rolar(s, by, at=None, label=None, ponto=(800, 470), duration=0.5, after=100):
        return s._p({'do': 'scroll', 'point': {'x': ponto[0], 'y': ponto[1]}, 'by': by, 'duration': duration, 'after': after}, at, label, {})

    def confere(s, escopo, esperados, label, tentativas=20):
        """`eval` que LÊ a tela e compara com o que a fala diz ("OK: ..." ou "DIFERENTE: ..."); escopo 'dlg', 'main', 'body' ou CSS"""
        sel = {'dlg': '[role=dialog]', 'main': 'main', 'body': 'body'}.get(escopo, escopo)
        esp = [esperados] if isinstance(esperados, str) else list(esperados)
        js = ("(async()=>{const norm=t=>t.replace(/[\\s\\u00a0]+/g,' ').toLowerCase();const esp=%s;let out='';"
              "for(let i=0;i<%d;i++){const els=[...document.querySelectorAll(%s)];const el=els[els.length-1];"
              "if(!el){out='DIFERENTE: sem elemento';}else{const t=norm(el.innerText);const falta=esp.filter(e=>!t.includes(norm(e)));"
              "if(!falta.length)return 'OK: '+esp.join(' | ');out='DIFERENTE: faltou '+JSON.stringify(falta)+' em: '+t.slice(0,260);}"
              "await new Promise(r=>setTimeout(r,250));}return out})()") % (json.dumps(esp, ensure_ascii=False), tentativas, json.dumps(sel))
        return s.add({'do': 'eval', 'js': js, 'label': 'confere ' + label})

    def fim(s):
        s.flush(1e9)
        s.steps.append({'do': 'eval', 'js': 'JSON.stringify(window.__avisos || "sem observador")', 'label': 'avisos de erro na tela'})
        s.steps.append({'do': 'mark', 'name': 'FIM', 'at': round(s.dur, 2)})

    def out(s):
        est = ' ESTIMADA' if s.estimado else ''
        return {
            'name': f'{AULA}-cap{s.n:02d}',
            'title': f'T14 · Cap. {s.n} · {NOMES[s.n]} (narração{est} {str(round(s.dur, 1)).replace(".", ",")} s; marcas L1..L{len(s.linhas)} = início de cada '
                     f'linha do roteiro; FAKE_NOW {FAKE_NOW}; logado como Rafael Nogueira)',
            'seed': f'{AULA}-cap{s.n:02d}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
            'start': {'x': s.start[0], 'y': s.start[1]},
            'anonymous': True, 'storage': storage(),
            'seedExtra': list(SEMENTE[s.n]),
            'prewarm': ['/login'], 'setup': s.setup, 'steps': s.steps,
        }


# ---------------------------------------------------------------- alvos
MAIN = 'main'
DLG = '[role=dialog]'
ALERTA = '[role=alertdialog]'
BTN = lambda n, within=None, **kw: {'role': 'button', 'name': n, 'exact': True, **({'within': within} if within else {}), **kw}
BTNX = lambda n, within=None, **kw: {'role': 'button', 'name': n, **({'within': within} if within else {}), **kw}
TXT = lambda t, within=None, **kw: {'text': t, 'exact': True, **({'within': within} if within else {}), **kw}
SEL = lambda s, **kw: {'selector': s, **kw}
ITEM = lambda n, **kw: {'role': 'menuitem', 'name': n, **kw}
OPT = lambda n, **kw: {'role': 'option', 'name': n, **kw}
AGUARDA = {'do': 'waitFor', 'idle': True}
# lista lateral de contas (SettingsSidebarLayout): o botão da conta e, por cima dele, os "⋮" que só aparecem com o mouse na conta
CONTA = lambda nome: SEL(f'div[class*="group/tab"] button:has(span:text-is("{nome}"))')
PONTOS = lambda nome: SEL(f'div[class*="group/tab"]:has(span:text-is("{nome}")) div.absolute button')
# linha da conciliação (ReconciliationTable: uma grade de 2 colunas por linha do extrato) achada pelo memo exato
LINHA = lambda memo: f'div[class*="md:grid-cols-2"]:has(:text-is("{memo}"))'
NA_LINHA = lambda memo, botao: SEL(f'{LINHA(memo)} button:has-text("{botao}")')


def login():
    return [{'do': 'waitFor', 'target': {'label': 'E-mail'}, 'timeout': 30},
            {'do': 'type', 'target': {'label': 'E-mail'}, 'text': '$TUT_USER', 'cps': 40},
            {'do': 'type', 'target': {'label': 'Senha', 'exact': True}, 'text': '$TUT_SENHA', 'cps': 40},
            {'do': 'click', 'target': BTN('Entrar')},
            {'do': 'waitFor', 'text': 'Olá, Rafael!', 'timeout': 30}, AGUARDA]


def setup_mov(extra=()):
    """login, Dashboard e a tela Movimentações Financeiras (abre na Conta Principal)"""
    return login() + [{'do': 'goto', 'url': '/movimentacoes-bancarias'}, {'do': 'waitFor', 'text': 'Controle de pagamentos via Pix/Transferência', 'timeout': 30},
                      AGUARDA, {'do': 'waitFor', 'target': CONTA('Conta Principal'), 'timeout': 20}] + list(extra)


def setup_conc(extra=()):
    """... e a aba Conciliação com o extrato aberto (Continuar)"""
    return setup_mov([{'do': 'click', 'target': BTN('Conciliação')}, {'do': 'waitFor', 'text': 'Conta para conciliar', 'timeout': 20},
                      {'do': 'click', 'target': BTN('Continuar')}, {'do': 'waitFor', 'text': 'Linha do extrato', 'timeout': 20}, AGUARDA] + list(extra))


# ---------------------------------------------------------------- capítulos
def cap00():
    c = Cap(0, login(), pace=0.6)
    c.mark(1)
    c.mark(2)
    c.mark(3)
    c.hover(BTN('Financeiro'), seconds=0.8, at=c.A(3, 'caminho', 0.4), label='menu Financeiro')
    c.mark(4)
    c.hover(BTN('Financeiro'), seconds=0.6, at=c.A(4, 'tela', 0.5), label='menu Financeiro (vamos começar)')
    c.fim()
    return c


def cap01():
    c = Cap(1, login(), pace=0.55)
    c.mark(1)
    c.click(BTN('Financeiro'), at=c.A(1, 'Financeiro', 0.7), label='menu Financeiro', unless={'role': 'link', 'name': 'Movimentações Financeiras'})
    c.click({'role': 'link', 'name': 'Movimentações Financeiras'}, at=c.A(1, 'Movimentações', 0.6), label='menu Movimentações Financeiras')
    c.waitfor(text='Controle de pagamentos via Pix/Transferência', timeout=20)
    c.hover(SEL('main h1:has-text("Movimentações Financeiras")'), seconds=0.8, at=c.A(1, 'nome', 0.5), label='título Movimentações Financeiras')
    c.mark(2)
    c.hover(CONTA('Resumo'), seconds=0.3, at=c.A(2, 'lado', 0.5), label='lista de contas')
    c.hover(CONTA('DINHEIRO (COFRE)'), seconds=0.3, at=c.A(2, 'saldo', 0.5), label='saldo embaixo do nome')
    c.hover(CONTA('DINHEIRO (COFRE)'), seconds=0.2, at=c.A(2, 'cofre', 0.4), label='o cofre primeiro')
    c.hover(CONTA('Conta Principal'), seconds=0.2, at=c.A(2, 'principal', 0.5), label='a conta principal')
    c.hover(CONTA('Conta Secundária'), seconds=0.3, at=c.A(2, 'outras', 0.5), label='as outras contas')
    c.hover(BTNX('Nova Conta'), seconds=0.3, label='botões Nova Conta e Novo Cartão')
    c.mark(3)
    c.click(CONTA('Conta Principal'), at=c.A(3, 'Clicando', 0.5), label='abre a Conta Principal')
    c.hover(SEL('main div.text-4xl.font-bold'), seconds=0.4, at=c.A(3, 'saldo', 0.5), label='cartão da Conta Principal')
    c.hover(BTNX('Saque', within=MAIN), seconds=0.15, at=c.A(3, 'Saque', 0.45), label='Saque')
    c.hover(BTNX('Sangria', within=MAIN), seconds=0.15, at=c.A(3, 'Sangria', 0.45), label='Sangria')
    c.hover(BTNX('Nova Movimentação', within=MAIN), seconds=0.15, at=c.A(3, 'Nova', 0.45), label='Nova Movimentação')
    c.hover(BTNX('Extrato', within=MAIN), seconds=0.3, at=c.A(3, 'Extrato', 0.45), label='Extrato')
    c.mark(4)
    c.hover(TXT('Histórico de Movimentações', within=MAIN), seconds=0.4, at=c.A(4, 'histórico', 0.5), label='Histórico de Movimentações')
    c.hover(SEL('main button[role=combobox]:has-text("Este mês")'), seconds=0.2, at=c.A(4, 'mês', 0.5), label='período Este mês')
    c.hover({'placeholder': 'Buscar por descrição ou valor...'}, seconds=0.4, at=c.A(4, 'busca', 0.5), label='busca por descrição ou valor')
    c.mark(5)
    c.click(CONTA('Resumo'), at=c.A(5, 'Resumo', 0.6), label='Resumo')
    c.hover(TXT('Dinheiro e contas bancárias', within=MAIN), seconds=0.4, at=c.A(5, 'total', 0.5), label='total da empresa')
    c.hover(TXT('Dinheiro', within=MAIN), seconds=0.3, at=c.A(5, 'cofre', 0.5), label='Dinheiro (cofre)')
    c.hover(TXT('Contas bancárias', within=MAIN), seconds=0.4, at=c.A(5, 'banco', 0.5), label='Contas bancárias')
    c.mark(6)
    c.hover(BTN('Movimentações Financeiras', within=MAIN), seconds=0.4, at=c.A(6, 'Nesta', 0.5), label='aba Movimentações Financeiras')
    c.hover(BTN('Conciliação', within=MAIN), seconds=0.6, at=c.A(6, 'Conciliação', 0.5), label='aba Conciliação')
    c.fim()
    return c


# ---------------------------------------------------------------- main
def main():
    pedidos = [int(a) for a in sys.argv[1:] if a.isdigit()]
    fns = {n: globals().get(f'cap{n:02d}') for n in range(15)}
    feitos = []
    for n, fn in fns.items():
        if fn is None or (pedidos and n not in pedidos):
            continue
        c = fn()
        d = c.out()
        json.dump(d, open(os.path.join(HERE, f'cap{n:02d}.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
        nat = sum(1 for st in d['steps'] if st.get('do') != 'mark')
        feitos.append(f'cap{n:02d} {nat} passos, {len(c.linhas)} linhas, {c.dur:.1f} s{" (fala estimada)" if c.estimado else ""}')
        if os.environ.get('ANCORAS'):
            for i, p, t in c.anchors:
                print(f'   cap{n:02d} L{i} {p!r} -> {t}')
    print('\n'.join(feitos))


if __name__ == '__main__':
    main()
