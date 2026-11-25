#!/usr/bin/env python3
"""T21 · Cato, o assistente (EcoFlix, EcoSistema 1.60.22): gera rec/t21/cap00..cap17.json (+ cap02b e cap15b, os cortes do Marcos) a partir da
fala ($TUT_HOME/t21/narracao/capNN.json: o estimado até a voz chegar; com a voz, o da voz, sem mudar nada aqui). O cap17
(Recapitulando) é montagem das gravações dos outros capítulos: o robô só deixa um passeio de reserva pelo painel.

Computador 1600x900, Rafael Nogueira (MASTER) na Recicla Vale Metais, tela "Estoque" (/materiais: ali as quatro perguntas prontas
saem sem sorteio); FAKE_NOW 2026-11-10T08:30:00-03:00 em todos os capítulos (o mesmo no Supabase falso e no robô; porta 54321, mundo
da T21 em /dev/shm/t21_mundo montado por rec/t21/t21_mundo.py, com os handlers de rec/t21/overlay).
Rodar de qualquer pasta: `python3 -I rec/t21/gerar.py [NN ...] [2b] [15b]` (ANCORAS=1 lista as âncoras, PREVISTO=1 os tempos previstos das
respostas). Depois: `python3 -I rec/t21/ensaio.py NN`, `bash rec/t21/t21_lote.sh 00:r 01:r ...` (rápido) e `NN:c` (completo).

LOGIN: todo capítulo é "anonymous" e o setup entra pela tela de login com "$TUT_USER"/"$TUT_SENHA" do ambiente (o Supabase falso
aceita qualquer senha; o valor nunca vai para arquivo nem log). Os cortes do Marcos (cap02b, cap15b) entram com o e-mail dele (dado do
mundo fictício) e a mesma "$TUT_SENHA".

Cada passo é preso a uma palavra da fala: A(linha, 'palavra', folga) = início da palavra − folga (o custo do gesto até o cursor
chegar: clique ~0,6 s, 1º clique numa janela recém-aberta ~1,2 s, hover ~0,5 s; digitação sem clique na palavra − 0,05 s). A palavra
casa INTEIRA (sem acento e pontuação); repetida na linha pede `nth`. Marca Ln 0,9 s antes da linha; um passo que começa até 0,25 s
antes da marca a puxa para o início dele.

ESTADO DE PARTIDA (rec/mundo/seeds-extra/): o fim da T15 (cadeia T14 → T15 da junção: `t14/inicio`, os `t14/apos-capNN` e os `t15/*`) +
`t21/inicio` (Cato ligado, sem a autorização de IA, memória `pending`; o Marcos com "Usar o Cato") nos caps. 0 a 2 e no 2b; + `t21/apos-cap02`
(autorizado) no cap. 3; + `t21/apos-cap03` (memória aceita e ligada, com uma nota) nos caps. 4 a 6; + `t21/apos-cap06` (conversa dos caps. 4 a 6 em
cato_events, duas contas a pagar) do cap. 7 em diante. O que um capítulo pede dos anteriores (a venda lançada do cap. 13, os pedidos do
cap. 14) o `setup` refaz pela própria conversa, fora do vídeo (setup_compra, setup_venda).
CONVERSAS: caps. 5 e 6 restauram no `setup` as perguntas e respostas R1.. dos capítulos anteriores pelo sessionStorage
(`cato-conversation-v3:<empresa>:<usuário>`), com os números do mundo (CORRECOES, as mesmas do overlay); o cap. 7 abre a conversa R1..R8 e
clica em "Nova"; do cap. 8 em diante cada capítulo parte do painel vazio e a ação nasce da conversa.
RESPOSTAS DO CATO: simuladas no Supabase falso (overlay: rec/t21/overlay/lib/cato_t21.mjs, R1 a R8 em rec/mundo/lib/cato_respostas.json):
edge cato-background → jobId; cato_jobs de "processing" a "completed" (R1 ~4,8 s depois do clique, as outras ~1,7 s);
edge cato-assist (mode "followups") → as 3 sugestões. Os cartões gravam de verdade (RPC cato_confirm_*_action).
NÃO CLICAR: "Falar no WhatsApp", "Ouvir resposta", o microfone, "Apagar toda a minha memória" e "Confirmar fechamento".

PARTICULARIDADES DA 1.60.22 (explorações rec/t21/_ex/):
 - O painel do Cato é um `div[role=dialog][aria-label^="Cato.ai"]` fixo à direita (400 px): os alvos dentro dele usam o seletor PAINEL,
   nunca `[role=dialog]` sozinho (a janela de autorização, a da memória e a do suporte também são).
 - O botão do Cato (fixo no canto, y ~850) e o rodapé do painel ficam fora da faixa de clique do robô: `noScroll`.
 - A última resposta "digita" de novo quando o painel remonta (reabrir, recarregar): o setup espera o fim do texto.
 - Balão de dica do Cato (cap. 1): 15 s depois de montar o botão (se a chave `cato_adoption_nudge_<empresa>_<usuário>` falta), visível 11 s;
   o roteiro guarda a chave, recarrega sob a ilustração e avança o relógio do navegador para o balão cair na linha certa.
"""
import hashlib
import json
import math
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TUT = os.path.normpath(os.path.join(HERE, '..', '..'))
AULA = 't21'
NARR = os.path.join(TUT, AULA, 'narracao')
FAKE_NOW = '2026-11-10T08:30:00-03:00'
try:
    VERSAO = open(os.path.join(TUT, 'app', 'dist', '.versao-app'), encoding='utf8').read().strip() or '1.60.22'
except OSError:   # pragma: no cover
    VERSAO = '1.60.22'
HOJE = FAKE_NOW[:10]
NOMES = ['Abertura', 'Onde o Cato fica', 'Autorizar o Cato', 'A memória do Cato', 'Conhecendo o painel', 'O que ele responde bem',
         'Gráfico, tabela e de onde vêm os números', 'Lançar uma compra pela conversa', 'Venda, ticket e preços', 'Contas, caixa e banco',
         'Saldo de cliente e fornecedor', 'Cadastros', 'Fotos, planilhas e PDFs', 'Nota fiscal pelo Cato', 'Pedidos e revisões',
         'Limites e permissões', 'Avaliar e falar com o suporte', 'Recapitulando']
T14 = ['t14/inicio'] + [f't14/apos-cap{n:02d}' for n in (2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 14)]
T15 = ['t15/inicio', 't15/apos-cap01', 't15/apos-cap02', 't15/apos-cap10']
INICIO = T14 + T15 + [f'{AULA}/inicio']
S02 = INICIO + [f'{AULA}/apos-cap02']
S03 = S02 + [f'{AULA}/apos-cap03']
S06 = S03 + [f'{AULA}/apos-cap06']
SEMENTE = {0: INICIO, 1: INICIO, 2: INICIO, 3: S02, **{n: S03 for n in (4, 5, 6)}, **{n: S06 for n in range(7, 18)}}
EMAIL_MARCOS = 'marcos.antunes@reciclavalemetais.example'
RESPOSTAS = json.load(open(os.path.normpath(os.path.join(HERE, '..', 'mundo', 'lib', 'cato_respostas.json')), encoding='utf8'))['respostas']
# Números do mundo que o Cato lê e o texto-base de R1 e R4 citava com outro valor (as mesmas CORRECOES do overlay cato_t21.mjs)
CORRECOES = {
    'R1': [('R$ 30.249,20', 'R$ 37.384,20'), ('R$ 69.589,55', 'R$ 62.454,55')],
    'R4': [('R$ 132.448,67', 'R$ 125.313,67'), ('R$ 82.515,00', 'R$ 75.380,00'), ('R$ 53.554,10', 'R$ 60.689,10')],
}
for _r in RESPOSTAS:
    for _de, _para in CORRECOES.get(_r['chave'], []):
        _r['payload']['answer'] = _r['payload']['answer'].replace(_de, _para)
RESP = {r['chave']: r for r in RESPOSTAS}
# Respostas da série A (ações): o overlay devolve com espera de 1,6 s; o texto serve só para contar os pedaços que a tela "digita".
for _k, _t in {
    'A1a': 'Como esta compra será paga: dinheiro, Pix/transferência ou saldo com o fornecedor?\n\nNenhuma compra foi lançada.',
    'A1b': 'Preparei a compra aqui embaixo. Confira os dados e clique em Lançar compra.',
    'A2': 'Preparei a venda aqui embaixo. Confira os dados e clique em Lançar venda.',
    'A3': 'Preparei o ticket aqui embaixo. Confira os dados e finalize.',
    'A4': 'Preparei o reajuste de preços aqui embaixo. Confira e confirme.',
    'A5': 'Preparei a proposta aqui embaixo. Confira e confirme no cartão.',
    'A6': 'Preparei a proposta aqui embaixo. Confira e confirme no cartão.',
    'A7': 'Preparei a proposta aqui embaixo. Confira e confirme no cartão.',
    'A8': 'Preparei a proposta aqui embaixo. Confira e confirme no cartão.',
    'A9': 'Preparei a proposta aqui embaixo. Confira e confirme no cartão.',
    'A10a': 'O saldo é de um cliente ou de um fornecedor?',
    'A10b': 'Preparei o acerto aqui embaixo. Confira e confirme no cartão.',
    'A11': 'Preparei a proposta aqui embaixo. Confira e confirme no cartão.',
    'A12': 'Preparei o cadastro aqui embaixo. Confira e confirme no cartão.',
    'A13': 'Preparei o cadastro aqui embaixo. Confira e confirme no cartão.',
    'A15a': 'Li os dados da pesagem. O que você quer fazer com eles? Você pode pedir um ticket de compra ou de venda.',
    'A15b': 'Preparei o ticket aqui embaixo. Confira os dados e finalize.',
    'A16a': 'Li a tabela do anexo. Você quer consultar os preços ou preparar uma atualização?',
    'A16b': 'Esses valores são preços de compra ou de venda?',
    'A17a': 'Qual forma de pagamento deve constar na NF-e: dinheiro, PIX, transferência, boleto ou duplicata a prazo?',
    'A17b': 'Preparei o rascunho da NF-e aqui embaixo. Confira e confirme no cartão.',
    'A18': 'O que consigo fazer no seu acesso agora\n\n1. Ações com sua confirmação\n' + '\n'.join(['- uma ação do Cato'] * 18) + '\n\n2. Consultas\n\n3. Limites',
    'A19': 'Seu usuário não tem permissão para alterar preços. Peça ao administrador da empresa para conferir seu acesso. Nenhum preço foi alterado.',
}.items():
    RESP[_k] = {'chave': _k, 'espera': 1.6, 'payload': {'answer': _t}}
# A resposta do Cato no tempo (medido nos ensaios completos dos caps. 3 e 4, 11/11): o clique que manda a pergunta age ~0,47 s
# depois do `at` (viagem do cursor); a tela consulta cato_jobs logo e a cada ~1,03 s e mostra a resposta ~0,69 s + 1,03 s × (nº de
# consultas até a `espera` vencer) depois do `at` + 0,47; o texto "digita" a ~25 ms por pedaço (palavra ou espaço) com a conversa
# rolando junto até o fim (o alvo só para quando a digitação acaba: apontar antes faz o robô esperar ~2 s), e a rolagem suave assenta
# ~0,35 s depois. A digitação da pergunta: clique no campo + 0,75 s, 0,3 s + (1,6/cps + 0,03) s por letra.
CLIQUE, POR_PEDACO, ASSENTA = 0.47, 0.025, 0.35

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
        t = re.sub(r'(?<!\w)' + re.escape(fala) + r'(?!\w)', leg, t)
    return [norm(w) for w in t.split() if norm(w)]


def carregar_voz(n):
    d = json.load(open(os.path.join(NARR, f'cap{n:02d}.json'), encoding='utf8'))
    words = [dict(w) for w in d['words']]
    linhas = [dict(li) for li in d['linhas']]
    if CAPS and texto_atual(n) != [norm(w['w']) for w in words if norm(w['w'])]:
        print(f'  AVISO cap{n:02d}: a fala do capNN.json não é a do tts_textos.py de hoje (rode o preparar_aula.sh de novo)')
    return words, linhas, float(d['dur']), bool(d.get('estimado'))


def stable_id(chave):
    """o mesmo UUID do `@id:<chave>` das sementes (rec/fakebase/core/util.mjs, stableId)"""
    h = bytearray(hashlib.sha1(('domiflix-fake:' + chave).encode()).digest())
    h[6] = (h[6] & 0x0F) | 0x50
    h[8] = (h[8] & 0x3F) | 0x80
    x = h[:16].hex()
    return f'{x[:8]}-{x[8:12]}-{x[12:16]}-{x[16:20]}-{x[20:32]}'


EMPRESA = stable_id('company.reciclavale')
RAFAEL = stable_id('user.rafael')
MARCOS = stable_id('user.marcos')


def storage(uid=RAFAEL, mostrar_cato=False):
    d = {'app_version': VERSAO, 'notification_shown_version': VERSAO, 'pwa-install-dismissed': 'true', 'theme': 'light',
         f'daily-tasks-reminder-last-shown-{uid}': HOJE, 'initial-preferences-set': 'true'}
    if mostrar_cato:   # o gravador cala o balão de dica do Cato no login pela tela; aqui ele tem de aparecer (browser.mjs, __mostrarCato)
        d['__mostrarCato'] = '1'
    return d


# ---------------------------------------------------------------- observador de avisos de erro (aceite: tem de sair vazio)
OBS = ("(()=>{window.__avisos=[];const re=/N[ãa]o foi poss[ií]vel|Erro ao|Tente novamente|Algo deu errado|Falha ao|Something went wrong|indispon[ií]vel|"
       "SEM RESPOSTA SIMULADA|Deu um problema|N[ãa]o consegui/i;"
       "const chk=(t)=>{t=(t||'').trim();const m=t&&t.match(new RegExp('[^]{0,40}('+re.source+')[^]{0,40}','i'));"
       "if(m&&window.__avisos.length<10)window.__avisos.push(m[0].replace(/[\\n\\r\\t ]+/g,' '))};new MutationObserver(ms=>{for(const m of ms){"
       "m.addedNodes.forEach(n=>chk(n.textContent));if(m.type==='characterData')chk(m.target.textContent)}}).observe(document.body,"
       "{childList:true,subtree:true,characterData:true});chk(document.body.innerText);"
       "setInterval(()=>{document.querySelectorAll('[data-sonner-toast][data-type=error]').forEach(t=>{const s='TOAST DE ERRO: '+t.textContent.trim().slice(0,90);"
       "if(!window.__avisos.includes(s)&&window.__avisos.length<10)window.__avisos.push(s)})},300);return 1})()")


class Cap:
    def __init__(s, n, setup, pace=0.5, cps=40, start=(800, 450), prewarm=('/login',), sub='', voz_de=None, user='rafael', mostrar_cato=False):
        s.n, s.sub = n, sub
        s.nome = f'cap{n:02d}{sub}'
        s.words, s.linhas, s.dur, s.estimado = carregar_voz(n)
        s.voz_inicio = 0.0
        if voz_de:   # corte: só as linhas voz_de[0]..voz_de[1] da voz, com o tempo contado do início da primeira (T06 cap08b, T15 cap09b)
            a, b = voz_de
            off = s.linhas[a - 1]['s']
            s.voz_inicio = round(off, 2)
            s.words = [dict(w, s=round(w['s'] - off, 3), e=round(w['e'] - off, 3), linha=w['linha'] - (a - 1))
                       for w in s.words if a - 1 <= w['linha'] <= b - 1]
            fim = s.linhas[b - 1]['e'] + 0.4
            s.linhas = [dict(li, i=li['i'] - (a - 1), s=round(li['s'] - off, 3), e=round(li['e'] - off, 3)) for li in s.linhas[a - 1:b]]
            s.dur = round(fim - off, 2)
        s.steps, s.pending, s.anchors = [], [], []
        s.aparece, s.estavel, s.previsto = 0.0, 0.0, []
        s.pace, s.cps, s.start = pace, cps, start
        s.prewarm = list(prewarm)
        s.user = user
        s.mostrar_cato = mostrar_cato
        s.setup = list(setup) + [{'do': 'eval', 'js': OBS}]

    # ---- tempo
    def L(s, i):
        return round(s.linhas[i - 1]['s'], 2)

    def W(s, i, palavra, nth=0, fim=False):
        q = norm(palavra)
        hits = [w for w in s.words if w['linha'] == i - 1 and norm(w['w']) == q]
        if len(hits) <= nth:
            raise SystemExit(f'{s.nome}: palavra "{palavra}" (#{nth}) não achada na linha {i}: ' + ' '.join(w['w'] for w in s.words if w['linha'] == i - 1))
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
        if isinstance(d.get('target'), dict) and 'noScroll' in d['target']:   # BT/SEL(..., noScroll=True): a opção é do passo, não do alvo
            d['target'] = dict(d['target'])
            if d['target'].pop('noScroll'):
                kw = dict(kw, noScroll=True)
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

    def ev(s, js, at=None, label=None, **kw):
        return s._p({'do': 'eval', 'js': js}, at, label, kw)

    def wait(s, seconds):
        return s.add({'do': 'wait', 'seconds': seconds})

    def waitfor(s, **kw):
        return s.add({'do': 'waitFor', **kw})

    def rolar(s, by, at=None, label=None, ponto=(800, 450), duration=0.5, after=100):
        return s._p({'do': 'scroll', 'point': {'x': ponto[0], 'y': ponto[1]}, 'by': by, 'duration': duration, 'after': after}, at, label, {})

    def confere(s, escopo, esperados, label, tentativas=20):
        """`eval` que LÊ a tela e compara com o que a fala diz ("OK: ..." ou "DIFERENTE: ..."); escopo 'painel', 'dlg', 'main', 'body' ou CSS"""
        sel = {'painel': PAINEL, 'dlg': DLG_AUT, 'main': 'main', 'body': 'body'}.get(escopo, escopo)
        esp = [esperados] if isinstance(esperados, str) else list(esperados)
        js = ("(async()=>{const norm=t=>t.replace(/[\\s\\u00a0]+/g,' ').toLowerCase();const esp=%s;let out='';"
              "for(let i=0;i<%d;i++){const els=[...document.querySelectorAll(%s)];const el=els[els.length-1];"
              "if(!el){out='DIFERENTE: sem elemento';}else{const t=norm(el.innerText);const falta=esp.filter(e=>!t.includes(norm(e)));"
              "if(!falta.length)return 'OK: '+esp.join(' | ');out='DIFERENTE: faltou '+JSON.stringify(falta)+' em: '+t.slice(0,260);}"
              "await new Promise(r=>setTimeout(r,250));}return out})()") % (json.dumps(esp, ensure_ascii=False), tentativas, json.dumps(sel))
        return s.add({'do': 'eval', 'js': js, 'label': 'confere ' + label})

    def dur_pergunta(s, texto, cps=None):
        """do clique no campo ao clique em Enviar (o mínimo): clique 0,75 s, digitação 0,3 s + (1,6/cps + 0,03) s por letra, 0,15 s"""
        return 0.75 + 0.3 + len(texto) * (1.6 / (cps or s.cps) + 0.03) + 0.15

    def enviar_para(s, chave, assenta_em):
        """o `at` do Enviar para a resposta `chave` assentar (texto todo na tela, conversa parada) em `assenta_em`"""
        r = RESP[chave]
        consultas = math.ceil(max(0.0, r['espera'] - 0.15) / 1.03)
        pedacos = len(re.split(r'(\s+)', r['payload']['answer']))
        return round(assenta_em - (CLIQUE + 0.69 + 1.03 * consultas + pedacos * POR_PEDACO + ASSENTA), 2)

    def agenda(s, texto, enviar, cedo, cps=None):
        """(at do campo, at do Enviar): a digitação termina em `enviar`, mas nunca começa antes de `cedo` (o gesto anterior)"""
        d = s.dur_pergunta(texto, cps)
        campo = round(max(cedo, enviar - d), 2)
        return campo, round(max(enviar, campo + d), 2)

    def resposta(s, chave, at_clique):
        """prevê (ver CLIQUE, POR_PEDACO e ASSENTA) quando a resposta `chave` aparece (s.aparece) e assenta (s.estavel), a partir do
        `at` do clique que manda a pergunta (Enviar ou pergunta pronta)"""
        r = RESP[chave]
        consultas = math.ceil(max(0.0, r['espera'] - 0.15) / 1.03)
        pedacos = len(re.split(r'(\s+)', r['payload']['answer']))
        s.aparece = round(at_clique + CLIQUE + 0.69 + 1.03 * consultas, 2)
        s.estavel = round(s.aparece + pedacos * POR_PEDACO + ASSENTA, 2)
        s.previsto.append(f'{chave}: clique {at_clique:.2f} s, aparece ~{s.aparece:.2f}, assenta ~{s.estavel:.2f}')
        return s.estavel

    def depois(s, at, quem=''):
        """`at` de um gesto sobre a última resposta: nunca antes de ela assentar (anota quando a palavra vem antes)"""
        t = round(max(at, s.estavel), 2)
        if t - at > 0.05:
            s.previsto.append(f'   {quem or "gesto"}: palavra em {at:.2f}, a resposta assenta em {s.estavel:.2f} (+{t - at:.2f} s)')
        return t

    def pergunta(s, texto, at_campo, at_enviar=None, label='', cps=None):
        """clica no campo "Pergunte ao Cato…" (`at_campo`), digita a pergunta sem clicar de novo (~0,75 s depois: o custo do clique) e
        clica em "Enviar" em `at_enviar` (ou logo que a digitação acaba). Marca de linha que cai no clique ou na digitação entra no
        tempo dela: o clique (ou a digitação) começa nela, ou a digitação sai em dois pedaços com a marca no meio. Com `label` = R1..R9,
        prevê a resposta (s.aparece, s.estavel); marca que cai antes de a resposta aparecer entra logo depois do Enviar."""
        cps = cps or s.cps
        por_letra = 1.6 / cps + 0.03
        for mt, mi in sorted(s.pending):     # o clique no campo dura ~0,45 s
            if at_campo + 0.25 < mt <= at_campo + 0.45:
                at_campo = mt
        d0 = s.click(CAMPO, at=at_campo, label=f'campo Pergunte ao Cato ({label})', noScroll=True)
        s.ev("(()=>{const t=document.querySelector('textarea[aria-label=\"Mensagem para o Cato\"]');if(!t)return 'SEM ALVO: campo';t.focus();return document.activeElement===t?'foco no campo':'SEM FOCO'})()",
             at=round(d0['at'] + 0.4, 2), label='foco no campo (a digitação nunca vai para a página)')
        t, resto, pedaco = round(d0['at'] + 0.75, 2), texto, 0
        for mt, mi in sorted(s.pending):
            if not (t < mt < t + 0.3 + len(resto) * por_letra - 0.3):
                continue
            if mt - t < 0.6:      # perto do começo: a digitação começa na marca
                s.flush(mt)
                t = round(mt, 2)
                continue
            n1 = max(1, int((mt - t - 0.3) / por_letra))
            s.type(CAMPO, resto[:n1], at=t, label=f'digita{" (continua)" if pedaco else ""}: {resto[:n1]}', noClick=True, cps=cps)
            resto, t, pedaco = resto[n1:], round(mt, 2), pedaco + 1
            s.flush(mt)
        s.type(CAMPO, resto, at=t, label=f'digita{" (continua)" if pedaco else ""}: {resto}', noClick=True, cps=cps)
        fim_txt = t + 0.3 + len(resto) * por_letra
        if at_enviar is None or at_enviar < fim_txt + 0.1:
            if at_enviar is not None and at_enviar < fim_txt - 0.2:
                print(f'  AVISO {s.nome}: Enviar ({label}) pedido em {at_enviar} s, mas a digitação acaba ~{fim_txt:.2f} s')
            at_enviar = fim_txt + 0.15
        d = s.click(ENVIAR, at=round(at_enviar, 2), label=f'Enviar ({label})', noScroll=True)
        if label in RESP:
            s.resposta(label, d['at'])
            s.flush(s.aparece + 0.2)
        return d

    def fim(s):
        s.flush(1e9)
        s.steps.append({'do': 'eval', 'js': 'JSON.stringify(window.__avisos || "sem observador")', 'label': 'avisos de erro na tela'})
        s.steps.append({'do': 'mark', 'name': 'FIM', 'at': round(s.dur, 2)})

    def out(s):
        est = ' ESTIMADA' if s.estimado else ''
        corte = f'; corte das linhas da voz a partir de {str(s.voz_inicio).replace(".", ",")} s' if s.voz_inicio else ''
        quem = 'Marcos Antunes' if s.user == 'marcos' else 'Rafael Nogueira'
        d = {
            'name': f'{AULA}-{s.nome}',
            'title': f'T21 · Cap. {s.n}{s.sub} · {NOMES[s.n]} (narração{est} {str(round(s.dur, 1)).replace(".", ",")} s{corte}; marcas '
                     f'L1..L{len(s.linhas)} = início de cada linha do roteiro; FAKE_NOW {FAKE_NOW}; logado como {quem})',
            'seed': f'{AULA}-{s.nome}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
            'start': {'x': s.start[0], 'y': s.start[1]},
            'anonymous': True, 'storage': storage(MARCOS if s.user == 'marcos' else RAFAEL, s.mostrar_cato),
            'seedExtra': list(SEMENTE[s.n]),
            'prewarm': s.prewarm, 'setup': s.setup, 'steps': s.steps,
        }
        if s.voz_inicio:
            d['voz_inicio'] = s.voz_inicio      # a edição e o resumo.py contam a voz a partir daqui
        return d



# ---------------------------------------------------------------- alvos
MAIN = 'main'
PAINEL = '[role=dialog][aria-label^="Cato.ai"]'
DLG_AUT = '[role=dialog]:has-text("Antes da primeira conversa com o Cato")'
DLG_SUP = '[role=dialog]:has-text("Falar com o suporte")'
MSGS = PAINEL + ' div.h-full.overflow-y-auto'
BTN = lambda n, within=None, **kw: {'role': 'button', 'name': n, 'exact': True, **({'within': within} if within else {}), **kw}
TXT = lambda t, within=None, **kw: {'text': t, 'exact': True, **({'within': within} if within else {}), **kw}
TXTP = lambda t, within=None, **kw: {'text': t, **({'within': within} if within else {}), **kw}
SEL = lambda s, **kw: {'selector': s, **kw}
FAB = SEL('button[aria-label="Abrir o Cato"]')
CAMPO = SEL('textarea[aria-label="Mensagem para o Cato"]')
ENVIAR = SEL('button[aria-label="Enviar"]')
NO_PAINEL = lambda css: SEL(f'{PAINEL} {css}')
LI = lambda trecho: NO_PAINEL(f'li:has-text("{trecho}")')
FORTE = lambda trecho: NO_PAINEL(f'strong:has-text("{trecho}")')
PONTO = lambda trecho: SEL(f'{DLG_AUT} li:has-text("{trecho}")')
AGUARDA = {'do': 'waitFor', 'idle': True}
ABRE = {'do': 'eval', 'js': "(async()=>{if(!window.__guarda){window.__guarda=1;let ts=0;document.addEventListener('focusin',e=>{const t=document.querySelector('textarea[aria-label=\\\"Mensagem para o Cato\\\"]');if(!t)return;if(e.target===t){ts=Date.now();return}if(Date.now()-ts<1500&&!e.target.closest('[role=dialog]'))t.focus()},true)}for(let k=0;k<5;k++){if(document.querySelector('[role=dialog][aria-label^=\"Cato.ai\"]'))return 'painel aberto';"
        "const b=document.querySelector('button[aria-label^=\"Abrir\"][aria-label*=\"Cato\"]');if(b)b.click();"
        "for(let i=0;i<16;i++){await new Promise(r=>setTimeout(r,250));if(document.querySelector('[role=dialog][aria-label^=\"Cato.ai\"]'))return 'painel aberto'}}return 'SEM ALVO: painel do Cato'})()"}
PRONTA = lambda k: NO_PAINEL(f'[role=group][aria-label="{k + 1} de 4"]')   # as perguntas prontas do painel vazio, pela posição (1ª = 0)


def login(email='$TUT_USER'):
    return [{'do': 'waitFor', 'target': {'label': 'E-mail'}, 'timeout': 30},
            {'do': 'type', 'target': {'label': 'E-mail'}, 'text': email, 'cps': 40},
            {'do': 'type', 'target': {'label': 'Senha', 'exact': True}, 'text': '$TUT_SENHA', 'cps': 40},
            {'do': 'click', 'target': BTN('Entrar')},
            {'do': 'waitFor', 'selector': 'button[aria-label="Sair"]', 'timeout': 30}, AGUARDA]


IR_ESTOQUE = [{'do': 'goto', 'url': '/materiais'}, {'do': 'waitFor', 'selector': 'button[aria-label="Abrir o Cato"]', 'timeout': 30}, AGUARDA]




# ---------------------------------------------------------------- a conversa dos caps. 4 a 6 (sessionStorage do useCato)
def mensagens(ate, feedback=None):
    """as perguntas e respostas R1..R<ate> no formato CatoMessage (hooks/useCato.tsx), como a tela as guardou"""
    base = 1794310200000   # 10/11/2026 08:30:00 -03:00 em ms (só aparece no celular)
    out = []
    for k, r in enumerate(RESPOSTAS[:ate], start=1):
        p = json.loads(json.dumps(r['payload']))
        ctx = p.get('context')
        if ctx:
            ctx['updatedAt'] = f'{HOJE}T{int(r["hora"][:2]) + 3:02d}:{r["hora"][3:]}:00.000Z'
        t = base + k * 20000
        out.append({'role': 'user', 'content': r['pergunta'], 'createdAt': t})
        out.append({'role': 'assistant', 'content': p['answer'], 'toolsUsed': p.get('toolsUsed'), 'chart': p.get('chart'), 'table': p.get('table'),
                    'images': None, 'action': None, 'context': ctx, 'interactionId': stable_id(f't21.cato.r{k}'),
                    'feedback': (feedback or {}).get(k), 'budgetNotice': None, 'cacheHit': False, 'createdAt': t + 4000})
    return out


def fim_da_resposta(k):
    """o fim do texto da resposta k como a tela o mostra (sem markdown), para esperar a resposta terminar de 'digitar'"""
    t = re.sub(r'\*\*', '', RESPOSTAS[k - 1]['payload']['answer']).strip()
    return t.split('\n')[-1].strip()[-22:]


def js_espera_resposta(trecho, tentativas=80):
    """espera a última resposta do painel conter `trecho` (a resposta acabou de 'digitar'); 'SEM ALVO' se não chegar"""
    return ("(async()=>{for(let i=0;i<%d;i++){const b=[...document.querySelectorAll(%s)].pop();"
            "if(b&&b.innerText.replace(/\\s+/g,' ').includes(%s))return 'ok';await new Promise(r=>setTimeout(r,250));}"
            "return 'SEM ALVO: a resposta não terminou'})()") % (tentativas, json.dumps(MSGS + ' > div.items-start'), json.dumps(trecho, ensure_ascii=False))


def restaura(ate, aquecer=()):
    """setup dos caps. 5, 6, 7 e 17: login, conversa R1..R<ate> no sessionStorage, recarrega a /materiais (passando antes pelas rotas de
    `aquecer`, que o vídeo visita) e abre o painel no fim da conversa"""
    chave = f'cato-conversation-v3:{EMPRESA}:{RAFAEL}'
    js = ("(()=>{const v={savedAt:Date.now(),sessionId:%s,messages:%s,activeJobId:null,activeQuestion:null,activeJobStartedAt:null};"
          "sessionStorage.setItem(%s,JSON.stringify(v));return 'conversa '+v.messages.length})()") % (
        json.dumps(stable_id('t21.cato.sessao')), json.dumps(mensagens(ate), ensure_ascii=False), json.dumps(chave))
    passos = login() + IR_ESTOQUE + [{'do': 'eval', 'js': js},
                                      {'do': 'goto', 'url': '/materiais', 'reload': True},
                                      {'do': 'waitFor', 'selector': 'button[aria-label="Abrir o Cato"]', 'timeout': 30}, AGUARDA]
    for rota in aquecer:
        passos += [{'do': 'goto', 'url': rota}, AGUARDA, {'do': 'wait', 'seconds': 1.0}]
    if aquecer:
        passos += IR_ESTOQUE
    return passos + [
        ABRE,
        {'do': 'waitFor', 'selector': PAINEL, 'timeout': 10},
        {'do': 'eval', 'js': js_espera_resposta(fim_da_resposta(ate))},
        {'do': 'wait', 'seconds': 0.8},
        {'do': 'eval', 'js': js_fim_da_conversa()},
        {'do': 'wait', 'seconds': 3.0},
    ]


# ---------------------------------------------------------------- setups do que o capítulo pede dos anteriores (fora do vídeo)
S_BASE = login() + IR_ESTOQUE
S_PAINEL = S_BASE + [ABRE, {'do': 'waitFor', 'selector': PAINEL, 'timeout': 10}, {'do': 'wait', 'seconds': 0.8}]


def pede_setup(texto, espera, cps=140):
    """manda `texto` ao Cato (sem tempo de fala) e espera `espera` aparecer na tela"""
    return [{'do': 'click', 'target': CAMPO, 'noScroll': True},
            {'do': 'type', 'target': CAMPO, 'text': texto, 'cps': cps, 'noClick': True},
            {'do': 'click', 'target': ENVIAR, 'noScroll': True},
            {'do': 'waitFor', 'text': espera, 'timeout': 25}, {'do': 'wait', 'seconds': 1.2}]


def toca_setup(botao, espera):
    """clica no último botão `botao` do painel e espera `espera` aparecer"""
    return [{'do': 'click', 'target': NO_PAINEL(f'button:has-text("{botao}") >> nth=-1'), 'noScroll': True},
            {'do': 'waitFor', 'text': espera, 'timeout': 25}, {'do': 'wait', 'seconds': 1.2}]


PEDIDO_COMPRA = 'Lança uma compra de 120 kg de alumínio latinha da Aparecida Ramos, a 6,20'
PEDIDO_VENDA = 'Lança uma venda de 500 kg de alumínio perfil pra Serra Fina, a 10,40, no saldo, vencimento 10/12'


def setup_compra():
    return (pede_setup(PEDIDO_COMPRA, 'Nenhuma compra foi lançada') + pede_setup('Pix, pela Conta Principal', 'Lançar compra')
            + toca_setup('Lançar compra', 'Aparecida Ramos lançada'))


def setup_venda():
    return pede_setup(PEDIDO_VENDA, 'Lançar venda') + toca_setup('Lançar venda', 'Reciclagem lançada')


# PDF que o app abre em aba nova (a gravação filma uma aba só): devolvido em base64 para virar a ilustração da edição (padrão da T08)
POPS = "(()=>{const o=window.open;window.__pops=[];window.open=function(...a){const w=o.apply(this,a);window.__pops.push(w);return w};return 'ok'})()"
PDF_JS = ("(async()=>{const w=(window.__pops||[]).slice(-1)[0];if(!w)return 'SEM JANELA';for(let i=0;i<40;i++){let f=null;"
          "try{f=w.document&&w.document.querySelector('#pdf-frame')}catch(e){return 'ERRO '+e}"
          "if(f&&f.src){const b=await (await fetch(f.src.split('#')[0])).blob();const u=new Uint8Array(await b.arrayBuffer());let s='';"
          "for(let k=0;k<u.length;k+=8192)s+=String.fromCharCode.apply(null,u.subarray(k,k+8192));return 'PDF:'+btoa(s)}"
          "await new Promise(r=>setTimeout(r,250))}return 'SEM PDF'})()")


# ---------------------------------------------------------------- rolagem roteirizada dentro do painel (eval: o cursor não se mexe)
SUAVE = ("await new Promise(res=>{const t0=performance.now();const f=t=>{const p=Math.min(1,(t-t0)/DUR),e=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;"
         "c.scrollTop=DESTINO;p<1?requestAnimationFrame(f):res()};requestAnimationFrame(f)});")


def js_msgs_rola(achar_js, y=300, dur_ms=700):
    """rola a conversa do painel até o elemento `achar_js` (expressão JS) ficar com o topo em y px CSS; devolve o topo final"""
    return ("(async()=>{const c=document.querySelector(%s);if(!c)return 'SEM PAINEL';const el=%s;if(!el)return 'SEM ALVO';"
            "const dy=Math.round(el.getBoundingClientRect().top-%d);if(Math.abs(dy)<3)return 'ok';const y0=c.scrollTop;"
            % (json.dumps(MSGS), achar_js, int(y))
            + (SUAVE.replace('DUR', str(int(dur_ms))).replace('DESTINO', 'y0+dy*e') if dur_ms else "c.scrollTop=y0+dy;")
            + "await new Promise(r=>setTimeout(r,60));return Math.round(el.getBoundingClientRect().top)})()")


def js_fim_da_conversa(dur_ms=0):
    return ("(async()=>{const c=document.querySelector(%s);if(!c)return 'SEM PAINEL';const y0=c.scrollTop,dy=c.scrollHeight-c.clientHeight-y0;"
            % json.dumps(MSGS) + (SUAVE.replace('DUR', str(int(dur_ms))).replace('DESTINO', 'y0+dy*e') if dur_ms else "c.scrollTop=y0+dy;")
            + "return 'fim '+Math.round(c.scrollTop)})()")


def js_rola_el(achar_js, y=300, dur_ms=700):
    """rola o ancestral que rola de verdade (a página, a janela) até o elemento `achar_js` ficar com o topo em y px CSS"""
    return ("(async()=>{const el=%s;if(!el)return 'SEM ALVO';let c=el.parentElement;while(c&&c!==document.body){const s=getComputedStyle(c);"
            "if(/(auto|scroll)/.test(s.overflowY)&&c.scrollHeight>c.clientHeight+4)break;c=c.parentElement;}if(!c||c===document.body)c=document.scrollingElement;"
            "const dy=Math.round(el.getBoundingClientRect().top-%d);if(Math.abs(dy)<3)return 'ok';const y0=c.scrollTop;" % (achar_js, int(y))
            + (SUAVE.replace('DUR', str(int(dur_ms))).replace('DESTINO', 'y0+dy*e') if dur_ms else "c.scrollTop=y0+dy;")
            + "await new Promise(r=>setTimeout(r,60));return Math.round(el.getBoundingClientRect().top)})()")


def js_dlg_fundo(dur_ms=0, quem='Antes da primeira conversa com o Cato'):
    """rola o miolo da janela de autorização (max-h 80dvh, rolagem própria) até o fim: os últimos pontos e os botões à vista"""
    return ("(async()=>{const d=[...document.querySelectorAll('[role=dialog]')].find(x=>x.innerText.includes(%s));if(!d)return 'SEM ALVO';"
            "const c=[...d.querySelectorAll('*')].find(e=>/(auto|scroll)/.test(getComputedStyle(e).overflowY)&&e.scrollHeight>e.clientHeight+4);"
            "if(!c)return 'sem rolagem (cabe)';const y0=c.scrollTop,dy=c.scrollHeight-c.clientHeight-y0;" % json.dumps(quem)
            + (SUAVE.replace('DUR', str(int(dur_ms))).replace('DESTINO', 'y0+dy*e') if dur_ms else "c.scrollTop=y0+dy;")
            + "return 'fundo '+Math.round(c.scrollTop)})()")


def achar_folha(escopo, texto, contem=False):
    """expressão JS: a folha visível (sem filhos) dentro de `escopo` cujo texto é (ou contém) `texto`"""
    cond = "e.textContent.includes(%s)" if contem else "e.textContent.trim()===%s"
    return ("[...document.querySelectorAll(%s)].find(e=>e.children.length===0&&e.getClientRects().length&&" + cond + ")") % (
        json.dumps(escopo + ' *'), json.dumps(texto, ensure_ascii=False))


def achar_ultimo(css):
    """expressão JS: o último elemento visível da conversa que casa com `css` (ex.: a linha do período da última resposta)"""
    return "[...document.querySelectorAll(%s)].filter(e=>e.getClientRects().length).pop()" % json.dumps(f'{MSGS} {css}')


def achar_contem(css, trecho):
    return "[...document.querySelectorAll(%s)].filter(e=>e.getClientRects().length&&e.innerText.includes(%s)).pop()" % (
        json.dumps(f'{MSGS} {css}'), json.dumps(trecho, ensure_ascii=False))



# ---------------------------------------------------------------- capítulos
def cap00():
    """Abertura: ilustração do problema (L1 e L2); a tela Estoque e a câmera até o botão do Cato (L3); cartão "Antes" (L4)."""
    c = Cap(0, S_BASE, pace=0.6)
    for i in (1, 2, 3):
        c.mark(i)
    c.hover(FAB, seconds=2.5, at=c.A(3, 'Rafael', 0.7), label='botão do Cato (a câmera vai até ele)', noScroll=True)
    c.mark(4)
    c.rolar(0, at=c.A(4, 'tutoriais', 0.4), ponto=(520, 470), duration=0.8, label='cursor sai do botão (cartão Antes)')
    c.fim()
    return c


def cap01():
    """Onde o Cato fica: zoom no botão (L1), ilustração computador × celular (L2; sob ela a página recarrega), o balão de dica (L3),
    Usuários e Permissões (L4), clique: a janela de autorização (L5)."""
    c = Cap(1, S_BASE, pace=0.6, mostrar_cato=True)
    chave = f'cato_adoption_nudge_{EMPRESA}_{RAFAEL}'
    c.mark(1)
    c.hover(FAB, seconds=2.2, at=c.A(1, 'botão', 0.7), label='ZOOM botão redondo do Cato (Abrir o Cato)', noScroll=True)
    c.rolar(0, at=c.A(1, 'qualquer', 0.3), ponto=(520, 470), duration=0.8, label='cursor solta o botão (em qualquer tela)')
    c.mark(2)
    # o balão de dica nasce 15 s depois de o botão montar e some em 11 s: a ilustração (L2) esconde a tela, então a página recarrega
    # nela (sem a chave do armazenamento local, que o app grava quando mostra) e o relógio do navegador avança 15 s logo antes da L3
    c.ev(f"(()=>{{try{{localStorage.removeItem('{chave}')}}catch(e){{}}return 'chave do balão removida'}})()", at=c.L(2) + 0.3, label='sob a ilustração: o balão volta a ser inédito')
    c.add({'do': 'goto', 'url': '/materiais', 'reload': True, 'at': round(c.L(2) + 0.6, 2), 'label': 'sob a ilustração: recarrega a tela Estoque'})
    c.waitfor(selector='button[aria-label="Abrir o Cato"]', timeout=30)
    c.mark(3)
    c.add({'do': 'clock', 'forward': '00:00:16', 'at': round(c.L(3) - 0.5, 2), 'label': 'avança o relógio: o balão de dica aparece'})
    c.hover(SEL('[role=status]:has-text("Abrir Cato")'), seconds=1.0, at=c.A(3, 'dica', 0.3), label='balão de dica do Cato', noScroll=True, optional=True, timeout=6)
    c.hover(SEL('button[aria-label="Fechar dica do Cato"]'), seconds=1.2, at=c.A(3, 'xis', 0.6), label='ZOOM xis Fechar dica do Cato (sem clicar)', noScroll=True, optional=True, timeout=4)
    c.mark(4)
    c.add({'do': 'goto', 'url': '/configuracoes?tab=users', 'at': round(c.L(4) - 0.2, 2), 'label': 'Usuários e Permissões'})
    c.waitfor(text='Marcos Antunes', timeout=20)
    c.click(TXT('Marcos Antunes'), at=c.A(4, 'permissão', 0.8), label='escolhe Marcos Antunes na lista')
    c.waitfor(text='Permissões concedidas', timeout=10)
    c.ev(js_rola_el(achar_folha('main', 'Usar o Cato (assistente de IA)'), 430, 900), at=c.A(4, 'Usuários', 0.2), label='desce até a permissão Usar o Cato (assistente de IA)')
    c.hover(SEL('main p:text-is("Usar o Cato (assistente de IA)")'), seconds=3.0, at=c.A(4, 'Uma', 0.0) + 0.2, label='ZOOM descrição de Usar o Cato (assistente de IA): o Cato responde sobre dados gerais da empresa, mesmo de telas que este usuário não pode abrir')
    c.mark(5)
    c.add({'do': 'goto', 'url': '/materiais', 'at': round(c.L(5) - 0.2, 2), 'label': 'volta à tela Estoque'})
    c.waitfor(selector='button[aria-label^="Abrir"][aria-label*="Cato"]', timeout=30)
    c.click(SEL('button[aria-label^="Abrir"][aria-label*="Cato"]'), at=c.A(5, 'clicar', 0.8), label='clique no botão do Cato', noScroll=True)
    c.waitfor(text='Antes da primeira conversa com o Cato', timeout=8)
    c.hover(TXT('Antes da primeira conversa com o Cato'), seconds=1.2, at=c.A(5, 'autorização', 0.7), label='janela Antes da primeira conversa com o Cato')
    c.fim()
    return c


SETUP_AUTORIZACAO = S_BASE + [
    {'do': 'eval', 'js': "(async()=>{for(let k=0;k<5;k++){if(document.body.innerText.includes('Antes da primeira conversa com o Cato'))return 'janela aberta';"
                         "const b=document.querySelector('button[aria-label^=\\\"Abrir\\\"][aria-label*=\\\"Cato\\\"]');if(b)b.click();"
                         "for(let i=0;i<16;i++){await new Promise(r=>setTimeout(r,250));if(document.body.innerText.includes('Antes da primeira conversa com o Cato'))return 'janela aberta'}}return 'SEM ALVO: janela de autorização'})()"},
    {'do': 'waitFor', 'text': 'Antes da primeira conversa com o Cato', 'timeout': 10}, {'do': 'wait', 'seconds': 0.8}]


def cap02():
    """Autorizar o Cato: a janela (L1), ilustração do caminho da pergunta (L2), microfone e leitura (L3), "pode errar" (L4); L5 é o
    corte do Marcos (cap02b; aqui a janela fica parada); "Entendi e autorizo" → "Cato autorizado" e o painel (L6)."""
    c = Cap(2, SETUP_AUTORIZACAO, pace=0.5, start=(560, 300))
    c.mark(1)
    c.hover(TXT('Leia rapidinho como ele trata os dados da sua empresa.'), seconds=0.6, at=c.A(1, 'janela', 0.5), label='janela de autorização (subtítulo)')
    c.mark(2)
    c.hover(PONTO('O Cato lê os dados da sua conta'), seconds=0.8, at=c.A(2, 'lê', 0.6), label='a câmera desce pelos pontos (1º)')
    c.hover(PONTO('Pra montar a resposta, esses trechos passam'), seconds=0.6, at=c.A(2, 'trechos', 0.6), label='a câmera desce pelos pontos (2º)')
    c.ev(js_dlg_fundo(0), at=c.A(2, 'treinar', 0.0), label='sob a ilustração: o miolo da janela rola até o fim (pontos de voz, erros e botões)')
    c.mark(3)
    c.hover(PONTO('O microfone só liga quando você toca nele'), seconds=0.5, at=c.A(3, 'microfone', 0.7), label='ZOOM ponto do microfone')
    c.hover(PONTO('Ouvir a resposta'), seconds=1.5, at=c.A(3, 'leitura', 0.6), label='ZOOM ponto de Ouvir a resposta')
    c.mark(4)
    c.hover(PONTO('O Cato pode errar'), seconds=2.5, at=c.A(4, 'errar', 0.9), label='ZOOM O Cato pode errar. Use como apoio e confira os números antes de decidir.')
    c.mark(5)
    c.ev(js_dlg_fundo(0), at=c.A(5, 'dica', 0.0), label='sob o corte do Marcos: a janela no fim (o botão à vista)')
    c.rolar(0, at=c.A(5, 'aviso', 0.0), ponto=(700, 560), duration=0.5, label='sob o corte do Marcos: cursor perto do botão')
    c.mark(6)
    c.hover(BTN('Entendi e autorizo'), seconds=0.6, at=c.A(6, 'administrador', 0.6), label='Entendi e autorizo (o Rafael é o administrador)')
    c.click(BTN('Entendi e autorizo'), at=c.A(6, 'Entendi', 0.5), label='clique em Entendi e autorizo')
    c.waitfor(text='Cato autorizado', timeout=8)
    c.hover(SEL('[data-sonner-toast]:has-text("Cato autorizado")'), seconds=1.2, at=c.A(6, 'Pronto', 0.5), label='aviso Cato autorizado', noScroll=True, optional=True, timeout=4)
    c.fim()
    return c


def cap02b():
    """Corte do cap02, linha 5: o Marcos (não administrador) clica no botão do Cato e a janela mostra o aviso, sem o botão de autorizar."""
    setup = login(EMAIL_MARCOS) + IR_ESTOQUE
    c = Cap(2, setup, pace=0.5, start=(900, 520), sub='b', voz_de=(5, 5), user='marcos')
    c.mark(1)
    c.click(FAB, at=c.A(1, 'dica', 0.3), label='Marcos clica no botão do Cato', noScroll=True)
    c.waitfor(text='Só o administrador da empresa pode autorizar o Cato.', timeout=8)
    c.ev(js_dlg_fundo(900), at=c.A(1, 'janela', 0.3), label='a janela desce até o aviso')
    c.hover(TXTP('Só o administrador da empresa pode autorizar o Cato.'), seconds=1.3, at=c.A(1, 'aviso', 1.0), label='ZOOM aviso Só o administrador da empresa pode autorizar o Cato.')
    c.hover(BTN('Entendi'), seconds=1.2, at=c.A(1, 'pedir', 0.5), label='Entendi (a saída: pedir pro administrador)')
    c.fim()
    return c


def cap03():
    """A memória do Cato: o painel abre e, por cima, "Quer que o Cato lembre de você?" (L1); os dois avisos (L2, L3); "Usar memória" (L4);
    o botão Memória: nota, lápis, lixeira (L5); a expiração (L6); a aba "Da empresa" (L7)."""
    c = Cap(3, S_BASE, pace=0.5, start=(900, 560))
    DLG = '[role=dialog]:has-text("Quer que o Cato lembre de você?")'
    MEM = '[role=dialog]:has-text("Memória do Cato")'
    c.mark(1)
    c.click(FAB, at=0.25, label='abre o Cato', noScroll=True)
    c.add({'do': 'eval', 'label': 'garante a janela de memória aberta', 'js': "(async()=>{const has=()=>document.body.innerText.includes('Quer que o Cato lembre de você?');await new Promise(r=>setTimeout(r,700));if(has())return 'ok';"
           "const b=document.querySelector('button[aria-label^=\"Abrir\"][aria-label*=\"Cato\"]');if(b)b.click();for(let i=0;i<24;i++){await new Promise(r=>setTimeout(r,250));if(has())return 'abriu no segundo toque'}return 'SEM ALVO: janela de memória'})()"})
    c.waitfor(text='Quer que o Cato lembre de você?', timeout=8)
    c.hover(TXT('Quer que o Cato lembre de você?'), seconds=1.0, at=c.A(1, 'pergunta', 0.6), label='janela Quer que o Cato lembre de você?', optional=True)
    c.mark(2)
    c.hover(TXTP('Ele guarda apenas preferências declaradas', within=DLG), seconds=2.5, at=c.A(2, 'guarda', 0.6), label='ZOOM Ele guarda apenas preferências declaradas e assuntos recentes. Saldos, preços e quantidades são sempre consultados novamente no sistema.')
    c.mark(3)
    c.hover(TXTP('A memória é pessoal dentro desta empresa', within=DLG), seconds=2.0, at=c.A(3, 'memória', 0.5), label='ZOOM A memória é pessoal dentro desta empresa. Ela não é compartilhada com outros usuários e não guarda senhas, documentos ou autorizações.')
    c.mark(4)
    c.hover(SEL(f'{DLG} button:has-text("Usar memória")'), seconds=0.4, at=c.A(4, 'Usar', 0.5), label='Usar memória (aponta)')
    c.hover(SEL(f'{DLG} button:has-text("Agora não")'), seconds=0.4, at=c.A(4, 'Agora', 0.6), label='Agora não (sem clicar)')
    c.click(SEL(f'{DLG} button:has-text("Usar memória")'), at=c.A(4, 'depois', 0.4), label='clique em Usar memória')
    c.waitfor(gone=DLG, timeout=8)
    c.mark(5)
    c.click(NO_PAINEL('[role=toolbar] button:has-text("Memória")'), at=c.A(5, 'Memória', 0.8), label='botão Memória (embaixo do painel)', noScroll=True)
    c.add({'do': 'eval', 'label': 'garante a janela Memória do Cato aberta', 'js': "(async()=>{const has=()=>[...document.querySelectorAll('[role=dialog]')].some(e=>/Memória do Cato/.test(e.innerText||''));await new Promise(r=>setTimeout(r,600));if(has())return 'ok';"
           "const b=[...document.querySelectorAll('[role=toolbar] button')].find(x=>/Memória/.test(x.innerText));if(!b)return 'SEM ALVO: Memória';"
           "b.click();for(let i=0;i<20;i++){await new Promise(r=>setTimeout(r,250));if(has())return 'abriu no segundo toque'}return 'SEM ALVO: Memória do Cato'})()"})
    c.waitfor(text='Memória do Cato', timeout=8)
    c.hover(TXT('Lembrar entre conversas'), seconds=0.6, at=c.A(5, 'embaixo', 0.0), label='Memória do Cato, aba Minha memória, chave Lembrar entre conversas', optional=True)
    c.click(SEL(f'{MEM} button:has-text("Adicionar nota")'), at=c.A(5, 'escrever', 0.6), label='Adicionar nota')
    c.type(SEL('#cato-memory-note'), 'Prefiro os valores em tabela, do maior para o menor.', at=c.A(5, 'escrever', -0.1), label='digita a nota', cps=50)
    c.click(SEL(f'{MEM} button:has-text("Salvar nota")'), at=c.A(5, 'por', -0.5), label='Salvar nota')
    c.waitfor(text='Prefiro os valores em tabela', timeout=8)
    c.hover(SEL(f'{MEM} button[aria-label="Editar memória"] >> nth=0'), seconds=0.35, at=c.A(5, 'ou', 0.0), label='lápis (Editar memória)', optional=True)
    c.hover(SEL(f'{MEM} button[aria-label="Apagar memória"] >> nth=0'), seconds=0.35, at=c.A(5, 'apagar', 0.0, nth=1), label='lixeira (Apagar memória)', optional=True)
    c.hover(SEL(f'{MEM} button:has-text("Apagar toda a minha memória")'), seconds=0.6, at=c.A(5, 'tudo', 0.0, nth=1), label='Apagar toda a minha memória (sem clicar)', optional=True)
    c.mark(6)
    c.hover(TXTP('Notas e preferências expiram em 90 dias', within=MEM), seconds=2.0, at=c.A(6, 'valem', 0.5), label='ZOOM Notas e preferências expiram em 90 dias; assuntos recentes, em 30 dias. Pausar não apaga o que foi salvo.')
    c.mark(7)
    c.click(SEL(f'{MEM} button:has-text("Da empresa")'), at=c.A(7, 'aba', 0.6), label='aba Da empresa')
    c.hover(TXTP('A equipe com acesso total pode publicar', within=MEM), seconds=1.5, at=c.A(7, 'total', 0.6), label='ZOOM A equipe com acesso total pode publicar contexto útil para todos.', optional=True)
    c.press('Escape', at=c.L(7) + 9.0, label='fecha a janela da memória', optional=True)
    c.fim()
    return c


def cap04():
    """Conhecendo o painel: o painel abre com "Oi, Rafael 👋" e as quatro perguntas (L1); campo, clipe, microfone e Enviar (L2); "Conversas",
    "Nova" e "Memória" (L3); "Mais opções do Cato" (L4); a primeira pergunta (L5) e a resposta R1 (L6); as três sugestões (L7)."""
    c = Cap(4, S_BASE, pace=0.5, start=(900, 560))
    c.mark(1)
    c.click(FAB, at=0.25, label='abre o Cato (o painel abre à direita)', noScroll=True)
    c.waitfor(text='Pergunte o que quiser sobre seu negócio', timeout=8)
    c.ev("JSON.stringify({rota:location.pathname,prontas:[...document.querySelectorAll('%s button')].map(b=>b.innerText.trim()).filter(t=>t.endsWith('?')).slice(0,6)})" % PAINEL.replace('"', '\\"'), label='as perguntas prontas da tela')
    c.hover(PRONTA(0), seconds=0.3, at=c.A(1, 'painel', 0.6), label='as quatro perguntas prontas (1ª)')
    c.ev("(async()=>{const b=document.querySelector('button[aria-label=\"Próximo em Sugestões para começar\"]');if(!b)return 'SEM ALVO: seta do carrossel';"
         "for(let i=0;i<3;i++){if(!b.disabled)b.click();await new Promise(r=>setTimeout(r,420))}return 'quarta pergunta à vista'})()",
         at=c.A(1, 'prontas', 2.2), label='o carrossel passa até a 4ª pergunta pronta')
    c.hover(PRONTA(3), seconds=0.4, at=c.A(1, 'prontas', 0.5), label='as quatro perguntas prontas (4ª)')
    c.mark(2)
    c.hover(CAMPO, seconds=0.6, at=c.A(2, 'escreve', 0.6), label='campo Pergunte ao Cato…', noScroll=True)
    c.hover(SEL(f'{PAINEL} button[aria-label="Anexar foto, arquivo ou planilha"]'), seconds=0.6, at=c.A(2, 'clipe', 0.6), label='clipe Anexar foto, arquivo ou planilha', noScroll=True)
    c.hover(SEL(f'{PAINEL} button[aria-label="Falar"]'), seconds=0.6, at=c.A(2, 'microfone', 0.6), label='microfone Falar (sem clicar)', noScroll=True)
    c.hover(ENVIAR, seconds=0.6, at=c.A(2, 'enviar', 0.6), label='botão Enviar', noScroll=True)
    c.mark(3)
    c.hover(SEL(f'{PAINEL} [role=toolbar] button:has-text("Conversas")'), seconds=0.4, at=c.A(3, 'conversas', 0.6), label='botão Conversas', noScroll=True)
    c.click(SEL(f'{PAINEL} [role=toolbar] button:has-text("Conversas")'), at=c.A(3, 'conversas', 0.0), label='abre Conversas', noScroll=True)
    c.ev("(async()=>{const has=()=>[...document.querySelectorAll('h2,[role=dialog]')].some(e=>/Suas conversas/.test(e.innerText||''));if(has())return 'ok';"
         "const b=[...document.querySelectorAll('[role=toolbar] button')].find(x=>/Conversas/.test(x.innerText));if(!b)return 'SEM ALVO: Conversas';"
         "b.click();for(let i=0;i<20;i++){await new Promise(r=>setTimeout(r,250));if(has())return 'abriu no segundo toque'}return 'SEM ALVO: Suas conversas'})()",
         label='garante Suas conversas aberta')
    c.hover(TXT('Retome uma análise de onde parou.'), seconds=0.8, at=c.A(3, 'nova', 0.6), label='Suas conversas (Retome uma análise de onde parou)', optional=True)
    c.press('Escape', at=c.A(3, 'nova', 0.0), label='fecha Suas conversas', optional=True)
    c.hover(SEL(f'{PAINEL} [role=toolbar] button[aria-label="Nova conversa"]'), seconds=0.5, at=c.A(3, 'nova', 0.4), label='botão Nova (nova conversa)', noScroll=True)
    c.hover(SEL(f'{PAINEL} [role=toolbar] button:has-text("Memória")'), seconds=0.8, at=c.A(3, 'memória', 0.6), label='botão Memória', noScroll=True)
    c.mark(4)
    c.click(SEL(f'{PAINEL} button[aria-label="Mais opções do Cato"]'), at=c.A(4, 'pontinhos', 0.8), label='três pontinhos (Mais opções do Cato)', noScroll=True)
    c.waitfor(text='Acompanhar pedidos', timeout=6)
    c.hover(SEL('[role=menuitem]:has-text("Notificações")'), seconds=0.5, at=c.A(4, 'som', 0.5), label='menu: Notificações', noScroll=True)
    c.hover(SEL('[role=menuitemcheckbox]:has-text("Ler respostas automaticamente")'), seconds=0.5, at=c.A(4, 'leitura', 0.5), label='menu: Ler respostas automaticamente', noScroll=True)
    c.hover(SEL('[role=menuitem]:has-text("Acompanhar pedidos")'), seconds=0.5, at=c.A(4, 'pedidos', 0.5), label='menu: Acompanhar pedidos', noScroll=True)
    c.hover(SEL('[role=menuitem]:has-text("Falar com atendente")'), seconds=0.5, at=c.A(4, 'atendente', 0.5), label='menu: Falar com atendente', noScroll=True)
    c.press('Escape', at=c.A(4, 'volta', 0.0), label='fecha o menu', optional=True)
    c.mark(5)
    d = c.click(NO_PAINEL('button:has-text("Como tá indo meu negócio esse mês?")'), at=c.A(5, 'primeira', 0.7), label='clique em Como tá indo meu negócio esse mês?')
    c.resposta('R1', d['at'])
    c.waitfor(text='Pensando…', timeout=6)
    c.mark(6)
    c.flush(1e9)   # a marca entra já (antes da espera pela resposta), no tempo dela
    c.waitfor(text='Consultei seu resumo financeiro', timeout=12)
    c.hover(LI('Vendas: R$ 118.620,20'), seconds=1.2, at=c.depois(c.A(6, 'vendeu', 0.6), 'Vendas'), label='ZOOM Vendas R$ 118.620,20')
    c.hover(FORTE('R$ 62.454,55'), seconds=1.5, at=c.A(6, 'resultado', 0.6), label='ZOOM resultado R$ 62.454,55')
    c.confere('painel', ['Vendas: R$ 118.620,20', 'R$ 62.454,55', 'Regime de caixa'], 'R1 na tela')
    c.mark(7)
    c.flush(1e9)
    c.waitfor(text='Compara com outubro', timeout=6)
    c.hover(NO_PAINEL('button:has-text("Compara com outubro")'), seconds=0.4, at=c.A(7, 'sugere', 0.6), label='sugestões de próxima pergunta (1ª)')
    c.hover(NO_PAINEL('button:has-text("Quais despesas tive esse mês?")'), seconds=1.2, at=c.A(7, 'clicar', 0.6), label='sugestões (2ª; a 3ª fica fora da faixa, que rola de lado)')
    c.fim()
    return c


def cap05():
    """O que ele responde bem (a conversa do cap04, R1): R2 quem tá me devendo (L1, L2), R3 estoque (L3), R4 banco (L4), R5 caixa (L5);
    ilustração caixa do dia × mês (L6)."""
    c = Cap(5, restaura(1), pace=0.5, start=(900, 560))
    c.mark(1)
    c.pergunta('Quem tá me devendo?', c.A(1, 'perguntas', 0.3), None, 'R2')
    c.mark(2)
    c.flush(1e9)
    c.waitfor(text='Consultei os saldos dos parceiros', timeout=8)
    t = c.depois(c.A(2, 'somam', 0.0), 'sobe a conversa (R2)')
    c.ev(js_msgs_rola(achar_ultimo('div.items-end'), 165, 600), at=t, label='a conversa sobe até o começo da resposta (o gráfico empurrou)')
    c.hover(FORTE('R$ 17.540,00'), seconds=1.0, at=max(c.A(2, 'dezessete', -0.2), t + 0.75), label='ZOOM total R$ 17.540,00')
    t = c.A(2, 'Fundição', 0.6)
    c.hover(LI('Fundição Bandeira do Vale: R$ 14.370,00'), seconds=1.2, at=t, label='ZOOM Fundição Bandeira do Vale: R$ 14.370,00')
    livre = t + 0.45 + 1.2 + 0.3
    c.mark(3)
    # cada resposta "digita" ~2 a 3,5 s depois de ~1,7 s de "Pensando…", e a fala já descreve a resposta: a pergunta é digitada no fim
    # da linha anterior (depois do último gesto dela) e o Enviar cai para a resposta assentar na palavra que a fala aponta
    texto = 'Quanto tenho em estoque agora?'
    campo, enviar = c.agenda(texto, c.enviar_para('R3', c.A(3, 'noventa', 0.0)), livre)
    c.pergunta(texto, campo, enviar, 'R3')
    c.waitfor(text='Consultei seu estoque', timeout=8)
    c.hover(FORTE('R$ 96.076,00'), seconds=1.0, at=c.depois(c.A(3, 'noventa', 0.5), 'R$ 96.076,00'), label='valor pelo custo médio R$ 96.076,00')
    c.hover(NO_PAINEL('p:has-text("Os materiais que mais pesam no valor") >> nth=-1'), seconds=0.8, at=c.depois(c.A(3, 'materiais', 0.5)),
            label='os materiais que mais pesam no valor')
    t = c.depois(c.A(3, 'alumínio', 0.6))
    c.hover(LI('Alumínio perfil: 3.385 kg'), seconds=0.6, at=t, label='alumínio perfil na frente')
    livre = t + 0.45 + 0.6 + 0.3
    c.mark(4)
    texto = 'Qual o saldo das minhas contas no banco?'
    campo, enviar = c.agenda(texto, c.enviar_para('R4', c.A(4, 'três', 0.5)), livre, cps=60)
    c.pergunta(texto, campo, enviar, 'R4', cps=60)
    c.waitfor(text='Consultei seu resumo bancário', timeout=8)
    t = c.depois(c.A(4, 'três', 0.5), 'as três contas')
    c.hover(NO_PAINEL('ul:has-text("Conta Cooperativa") >> nth=-1'), seconds=0.5, at=t, label='as três contas')
    c.hover(FORTE('R$ 125.313,67'), seconds=0.5, at=max(c.depois(c.A(4, 'cento', 0.6)), t + 0.45 + 0.5 + 0.1), label='o total das três contas R$ 125.313,67')
    t = max(c.depois(c.A(4, 'entrou', 0.6)), t + 0.45 + 0.5 + 0.1 + 1.2)
    c.hover(NO_PAINEL('p:has-text("entraram") >> nth=-1'), seconds=0.5, at=t, label='o que entrou e saiu no mês')
    livre = t + 0.45 + 0.5 + 0.2
    c.mark(5)
    texto = 'Como tá meu caixa hoje?'
    campo, enviar = c.agenda(texto, c.enviar_para('R5', c.A(5, 'fecharam', 0.4)), livre, cps=60)
    c.pergunta(texto, campo, enviar, 'R5', cps=60)
    c.waitfor(text='Consultei seu caixa', timeout=8)
    c.hover(FORTE('R$ 640,00'), seconds=0.6, at=c.depois(c.A(5, 'fecharam', 0.4), 'os caixas de ontem'), label='os caixas de ontem (R$ 640,00 e R$ 1.250,00)')
    c.mark(6)
    c.fim()
    return c


def cap06():
    """Gráfico, tabela e de onde vêm os números (a conversa R1..R5): R6 três meses em linha (L1, L2), R7 vendas por cliente em outubro em
    barras (L3), ilustração saldo × movimentado (L4, L5), R8 estoque em tabela (L6), ilustração da regra (L7); de onde vêm os números e o
    botão "Abrir posição de estoque" (L8); a Posição de Estoque com o "Total geral" (L9); o painel de novo e o rodapé (L10)."""
    c = Cap(6, restaura(5), pace=0.5, start=(900, 560))
    c.mark(1)
    # a pergunta é digitada enquanto a fala a diz; a resposta digita ~3,3 s: o gráfico (que chega inteiro, embaixo do texto) é
    # apontado quando a conversa para, já em "outubro"
    c.pergunta('Compras e vendas dos últimos três meses', c.A(1, 'pergunta', 0.6), c.A(1, 'meses', 0.4), 'R6')
    c.waitfor(text='Olhando suas compras e vendas dos últimos três meses', timeout=8)
    c.mark(2)
    GRAF = 'div.rounded-2xl:has-text("Compras e vendas por mês")'
    c.hover(NO_PAINEL(f'{GRAF} circle.recharts-dot >> nth=1'), seconds=1.5, at=c.depois(c.A(2, 'outubro', 0.6), 'outubro no gráfico'),
            label='outubro: as compras quase alcançam as vendas (dica do gráfico)')
    t = c.A(2, 'novembro', 0.6)
    c.hover(NO_PAINEL(f'{GRAF} circle.recharts-dot >> nth=5'), seconds=1.5, at=t, label='novembro: as vendas passam longe das compras (dica do gráfico)')
    livre = t + 0.45 + 1.5 + 0.3
    c.mark(3)
    # R7: o zoom na Fundição em "oitocentos" pede a resposta parada ~0,6 s antes (a conversa ainda sobe até o começo dela)
    texto = 'Pra quem eu mais vendi em outubro?'
    campo, enviar = c.agenda(texto, c.enviar_para('R7', c.A(3, 'oitocentos', 0.4) - 0.6), livre)
    c.pergunta(texto, campo, enviar, 'R7')
    c.waitfor(text='Fundição Bandeira do Vale: R$ 112.800,00', timeout=8)
    t = c.depois(c.A(3, 'doze', 0.1), 'sobe a conversa (R7)')
    c.ev(js_msgs_rola(achar_ultimo('div.items-end'), 165, 500), at=t, label='a conversa sobe até o começo da resposta (o gráfico empurrou)')
    c.hover(LI('Fundição Bandeira do Vale: R$ 112.800,00'), seconds=0.7, at=max(c.A(3, 'oitocentos', 0.4), t + 0.6),
            label='ZOOM Fundição Bandeira do Vale: R$ 112.800,00')
    c.mark(4)
    c.mark(5)
    c.mark(6)
    # R8: a digitação começa sob a ilustração (L4 e L5) e termina à vista; a tabela chega em "monta uma tabela"
    texto = 'Lista meu estoque em tabela'
    campo, enviar = c.agenda(texto, c.enviar_para('R8', c.A(6, 'tabela', 0.15)), c.A(5, 'diferentes', 0.0))
    c.pergunta(texto, campo, enviar, 'R8')
    c.waitfor(text='Estoque em 10/11/2026', timeout=8)
    t = c.depois(c.A(6, 'tabela', 0.15), 'sobe a conversa (R8)')
    c.ev(js_msgs_rola(achar_ultimo('div.items-end'), 165, 500), at=t, label='a conversa sobe até o começo da resposta (a tabela empurrou)')
    t = max(c.A(6, 'material', 0.0), t + 0.6)
    c.hover(NO_PAINEL('th:has-text("Material") >> nth=-1'), seconds=0.15, at=t, label='tabela: Material')
    t = max(c.A(6, 'quantidade', 0.2), t + 0.65)
    c.hover(NO_PAINEL('th:has-text("Quantidade") >> nth=-1'), seconds=0.15, at=t, label='tabela: Quantidade (kg)')
    c.hover(NO_PAINEL('th:has-text("Valor em estoque") >> nth=-1'), seconds=0.15, at=max(c.A(6, 'valor', 0.5), t + 0.65), label='tabela: Valor em estoque')
    c.mark(7)
    c.mark(8)
    c.ev(js_msgs_rola(achar_contem('div.items-start', 'Aqui está o seu estoque de agora'), 150, 700), at=c.A(8, 'cima', 0.8), label='sobe a conversa até o topo da resposta da tabela')
    c.hover(NO_PAINEL('p:text-is("Consultei seu estoque") >> nth=-1'), seconds=0.6, at=c.A(8, 'tirou', 0.6), label='ZOOM Consultei seu estoque')
    c.hover(NO_PAINEL('span:has-text("Período 10 nov. 2026") >> nth=-1'), seconds=0.5, at=c.A(8, 'período', 0.5), label='ZOOM linha do período')
    c.hover(NO_PAINEL('span:has-text("Atualizado às") >> nth=-1'), seconds=0.8, at=c.A(8, 'hora', 0.5), label='ZOOM Atualizado às')
    c.ev(js_fim_da_conversa(900), at=c.A(8, 'lidos', 0.6), label='desce pela tabela')
    c.hover(NO_PAINEL('button:has-text("Abrir posição de estoque") >> nth=-1'), seconds=1.0, at=c.A(8, 'botão', 0.6), label='botão Abrir posição de estoque')
    c.mark(9)
    c.click(NO_PAINEL('button:has-text("Abrir posição de estoque") >> nth=-1'), at=c.A(9, 'Posição', 0.6), label='clique em Abrir posição de estoque')
    c.waitfor(text='Total geral', timeout=10)
    # cada página monta o próprio AppLayout: se a troca de rota já fechou o painel, o Fechar não roda (passo condicional)
    c.click(NO_PAINEL('button[aria-label="Fechar"]'), at=c.A(9, 'Estoque', 0.3), label='Fechar o painel', noScroll=True,
            when=NO_PAINEL('button[aria-label="Fechar"]'), optional=True, timeout=3)
    c.waitfor(gone=PAINEL, timeout=6)
    c.ev(js_rola_el(achar_folha('main', 'Total geral'), 430, 800), at=c.A(9, 'total', 0.0), label='desce até o Total geral')
    c.hover(SEL('main tr:has-text("Total geral")'), seconds=1.8, at=c.A(9, 'noventa', 0.7), label='ZOOM Total geral com Valor R$ 96.076,00')
    c.confere('main', ['Total geral', 'R$ 96.076,00'], 'Total geral igual ao da resposta')
    c.mark(10)
    c.click(FAB, at=c.L(10) - 0.4, label='abre o Cato de novo (a conversa volta)', noScroll=True)
    c.waitfor(selector=PAINEL, timeout=6)
    c.hover(NO_PAINEL('p:has-text("O Cato.ai pode cometer erros")'), seconds=1.5, at=c.A(10, 'erros', 0.9), label='rodapé O Cato.ai pode cometer erros', noScroll=True)
    c.hover(NO_PAINEL('button:has-text("Abrir posição de estoque") >> nth=-1'), seconds=1.0, at=c.A(10, 'botão', 0.6), label='confira na tela, por aquele botão')
    c.fim()
    return c


# ---------------------------------------------------------------- ações pela conversa (caps. 7 a 16)
T = lambda t: SEL(f'{PAINEL} :text("{t}") >> nth=-1')            # o último trecho de texto com `t` no painel (cartões, respostas)
BT = lambda t: SEL(f'{PAINEL} button:has-text("{t}") >> nth=-1', noScroll=True)   # o último botão com `t` no painel
NOVA = SEL(f'{PAINEL} [role=toolbar] button[aria-label="Nova conversa"]', noScroll=True)


def pede(c, texto, chave, assenta_em, cedo=0.0, cps=None):
    """digita `texto` e manda de modo que a resposta `chave` assente em `assenta_em` (a digitação nunca começa antes de `cedo`)"""
    campo, enviar = c.agenda(texto, c.enviar_para(chave, assenta_em), cedo, cps)
    return c.pergunta(texto, campo, enviar, chave, cps=cps)


def cap07():
    """Lançar uma compra: "Nova" e o pedido (L1), pergunta de pagamento (L2), cartão (L3, L4), ilustração (L5), Corrigir dados e Agora não (L6),
    "Lançar compra" (L7), próximos passos (L8), ilustração dos 10 minutos (L9)."""
    c = Cap(7, restaura(8) + [{'do': 'eval', 'js': POPS}], pace=0.5, start=(900, 560))
    c.mark(1)
    c.click(NOVA, at=c.A(1, 'parte', 0.6), label='Nova (conversa limpa)')
    c.waitfor(text='Pergunte o que quiser sobre seu negócio', timeout=8)
    c.mark(2)
    pede(c, PEDIDO_COMPRA, 'A1a', c.L(2) + 0.6, cedo=c.A(1, 'Vou', 0.0))
    c.waitfor(text='Nenhuma compra foi lançada', timeout=10)
    c.mark(3)
    pede(c, 'Pix, pela Conta Principal', 'A1b', c.L(3) + 0.3, cedo=c.A(2, 'respondo', 0.3))
    c.waitfor(text='Lançar compra', timeout=10)
    c.hover(T('Fornecedor: Aparecida Ramos'), seconds=0.5, at=c.depois(c.A(3, 'Fornecedor', 0.5)), label='cartão: Fornecedor')
    c.hover(T('Preços informados nesta conversa'), seconds=0.5, at=c.depois(c.A(3, 'preço', 0.5)), label='cartão: material, quantidade e preço')
    c.hover(T('Total da compra'), seconds=0.5, at=c.depois(c.A(3, 'total', 0.5)), label='cartão: Total da compra R$ 744,00')
    c.hover(T('Forma de pagamento'), seconds=0.8, at=c.depois(c.A(3, 'forma', 0.5)), label='cartão: Forma de pagamento Pix e Conta Principal')
    c.mark(4)
    c.hover(T('Estoque entra e o financeiro registra'), seconds=2.0, at=c.A(4, 'linha', 0.6), label='ZOOM Estoque entra e o financeiro registra R$ 744,00.')
    c.mark(5)
    c.mark(6)
    c.click(BT('Corrigir dados'), at=c.A(6, 'Corrigir', 0.6), label='Corrigir dados (o pedido volta ao campo)')
    c.confere('painel', ['Pergunte ao Cato'], 'painel depois de Corrigir dados')
    c.hover(BT('Agora não'), seconds=0.6, at=c.A(6, 'Agora', 0.6), label='Agora não (sem clicar)', optional=True)
    c.mark(7)
    c.ev(js_fim_da_conversa(), at=c.A(7, 'Lançar', 0.1), label='rola a conversa até o cartão (o campo cresceu com o pedido de volta)')
    c.click(BT('Lançar compra'), at=c.A(7, 'Lançar', 0.6), label='clique em Lançar compra')
    c.waitfor(text='Aparecida Ramos lançada', timeout=10)
    c.click(BT('Abrir comprovante'), at=c.A(7, 'comprovante', 0.6), label='clique em Abrir comprovante (o PDF abre em aba nova)', optional=True)
    c.ev(PDF_JS, at=c.A(7, 'guardar', 0.2), label='PDF do comprovante da compra (aba nova, para a ilustração)')
    c.mark(8)
    c.click(BT('Próximos passos'), at=c.A(8, 'passos', 0.6), label='Próximos passos do pedido (abre)', optional=True)
    c.mark(9)
    c.fim()
    return c


def cap08():
    """Venda, ticket e preços (painel vazio): venda (L1 a L3), ilustração sem estoque (L4), ticket (L5, L6), preços (L7, L8)."""
    c = Cap(8, S_PAINEL, pace=0.5, start=(900, 560))
    c.mark(1)
    pede(c, PEDIDO_VENDA, 'A2', c.L(2) + 0.2, cedo=c.A(1, 'Desta', 0.2))
    c.waitfor(text='Lançar venda', timeout=10)
    c.mark(2)
    c.hover(T('Total da venda'), seconds=0.8, at=c.depois(c.A(2, 'cartão', 0.6)), label='cartão da venda: Total da venda R$ 5.200,00')
    c.mark(3)
    c.hover(T('Vencimento'), seconds=0.5, at=c.depois(c.L(3) + 0.1), label='cartão: Forma de pagamento Saldo com cliente e Vencimento')
    c.click(BT('Lançar venda'), at=c.A(3, 'Lançar', 0.6), label='clique em Lançar venda')
    c.waitfor(text='Reciclagem lançada', timeout=10)
    c.click(BT('Próximos passos'), at=c.A(3, 'receber', 0.3), label='Próximos passos do pedido (abre)', optional=True)
    c.hover(T('A receber'), seconds=1.0, at=c.A(3, 'receber', 0.6), label='Próximos passos: A receber R$ 5.200,00', optional=True)
    c.mark(4)
    c.mark(5)
    pede(c, 'Faz um ticket de compra da Cooperativa Recomeço: plástico PET, bruto 1.480, tara 60, motorista Jair Lopes, placa GHT7B19', 'A3',
         c.A(5, 'líquido', 0.0), cedo=c.A(4, 'estoque', 0.0))
    c.waitfor(text='Finalizar ticket', timeout=10)
    c.hover(T('Peso líquido'), seconds=1.0, at=c.depois(c.A(5, 'líquido', 0.4)), label='cartão do ticket: Peso líquido 1.420 kg')
    c.mark(6)
    c.hover(T('Ao confirmar, o ticket recebe número'), seconds=2.0, at=c.A(6, 'registra', 0.6), label='ZOOM Ao confirmar, o ticket recebe número. Estoque e financeiro não mudam até a valorização.')
    c.click(BT('Finalizar ticket'), at=c.A(6, 'valorizado', 0.6), label='clique em Finalizar ticket')
    c.waitfor(text='Abrir comprovante', timeout=10)
    c.mark(7)
    pede(c, 'Sobe 50 centavos o preço de compra do cobre mel e do cobre misto', 'A4', c.A(7, 'cartão', 0.0), cedo=c.A(6, 'ticket', 0.0) + 5)
    c.waitfor(text='Sim, atualizar', timeout=10)
    c.hover(T('Cobre mel'), seconds=1.0, at=c.depois(c.A(7, 'hoje', 0.5)), label='cartão de preços: Cobre mel R$ 42,50 → R$ 43,00')
    c.mark(8)
    c.click(BT('Sim, atualizar'), at=c.A(8, 'Sim', 0.6), label='clique em Sim, atualizar')
    c.waitfor(text='Reajuste na tabela padrão', timeout=10)
    c.fim()
    return c


def cap09():
    """Contas, caixa e banco (painel vazio): baixa (L1, L2), ilustração (L3), abrir caixa (L4), saída (L5), transferência (L6), fechar (L7)."""
    c = Cap(9, S_PAINEL, pace=0.5, cps=90, start=(900, 560))
    c.mark(1)
    pede(c, 'Dá baixa na primeira parcela da Fundição Bandeira do Vale, recebi por Pix na Conta Principal', 'A5', c.A(1, 'recebi', 0.0), cedo=c.A(1, 'Fundição', 0.5))
    c.waitfor(text='Confirmar registro', timeout=10)
    c.hover(T('Fatura venda #1731'), seconds=0.6, at=c.depois(c.A(1, 'recebi', 0.5)), label='cartão: Registrar recebimento, Fatura venda #1731 (parcela 1/3), R$ 4.790,00')
    c.mark(2)
    c.click(BT('Confirmar registro'), at=c.A(2, 'Confirmar', 0.6), label='clique em Confirmar registro')
    c.waitfor(text='Conta baixada', timeout=10)
    c.mark(3)
    c.mark(4)
    pede(c, 'Abre o caixa com 1.500 reais', 'A6', c.A(4, 'valor', 0.0), cedo=c.A(3, 'banco', 0.0))
    c.waitfor(text='Confirmar abertura', timeout=10)
    c.click(BT('Confirmar abertura'), at=c.A(4, 'contado', 0.6), label='clique em Confirmar abertura')
    c.waitfor(text='Caixa aberto', timeout=10)
    c.mark(5)
    pede(c, 'Lança uma saída de 85 reais no caixa, gás da empilhadeira, categoria Combustível', 'A7', c.A(5, 'motivo', 0.0), cedo=c.L(5) - 3)
    c.waitfor(text='Confirmar lançamento', timeout=10)
    c.click(BT('Confirmar lançamento'), at=c.A(5, 'oitenta', 0.6), label='clique em Confirmar lançamento')
    c.waitfor(text='Lançamento no caixa registrado', timeout=10)
    c.mark(6)
    pede(c, 'Transfere 2.000 da Conta Secundária pra Conta Principal', 'A8', c.A(6, 'contas', 0.0), cedo=c.L(6) - 3)
    c.waitfor(text='Confirmar transferência', timeout=10)
    c.hover(T('Conta Secundária'), seconds=0.8, at=c.depois(c.A(6, 'cartão', 0.5)), label='cartão: saldo de cada conta antes e depois', optional=True)
    c.click(BT('Confirmar transferência'), at=c.depois(c.A(6, 'depois', 0.6)), label='clique em Confirmar transferência')
    c.waitfor(text='Transferência registrada', timeout=10)
    c.mark(7)
    pede(c, 'Fecha o caixa, contei 1.415', 'A9', c.A(7, 'diferença', 0.0), cedo=c.L(7) - 2)
    c.waitfor(text='Confirmar fechamento', timeout=10)
    c.hover(T('Saldo esperado'), seconds=1.0, at=c.depois(c.A(7, 'diferença', 0.5)), label='cartão: Saldo esperado e Saldo contado (diferença R$ 0,00)', optional=True)
    c.hover(BT('Confirmar fechamento'), seconds=1.2, at=c.A(7, 'confirmar', 0.6), label='Confirmar fechamento (sem clicar)')
    c.fim()
    return c


def cap10():
    """Saldo de parceiro (painel vazio): acerto do Valdir (L1, L2), recebimento da Aços Quiririm (L3), ilustração (L4)."""
    c = Cap(10, S_PAINEL, pace=0.5, cps=90, start=(900, 560))
    c.mark(1)
    pede(c, 'Abate 100 reais do saldo do Valdir Pereira, ele entregou uma bateria em troca', 'A10a', c.L(1) + 8.0, cedo=c.A(1, 'Valdir', 0.0))
    c.waitfor(text='O saldo é de um cliente ou de um fornecedor?', timeout=10)
    c.mark(2)
    pede(c, 'fornecedor', 'A10b', c.L(2) + 0.5, cedo=c.L(2) - 2.5)
    c.waitfor(text='Não movimenta caixa nem banco', timeout=10)
    c.hover(T('Hoje: Ele te deve'), seconds=0.6, at=c.depois(c.A(2, 'devia', 0.5)), label='cartão: Hoje: Ele te deve R$ 300,00.')
    c.hover(T('Ele ficará te devendo'), seconds=0.8, at=c.depois(c.A(2, 'dever', 0.5)), label='cartão: Ele ficará te devendo R$ 200,00.')
    c.hover(T('Não movimenta caixa nem banco'), seconds=1.5, at=c.depois(c.A(2, 'avisa', 0.5)), label='ZOOM Não movimenta caixa nem banco.')
    c.click(SEL(f'{PAINEL} button:text-is("Confirmar") >> nth=-1', noScroll=True), at=c.depois(c.A(2, 'caixa', 0.6)), label='clique em Confirmar')
    c.mark(3)
    pede(c, 'Registra o recebimento de 1.000 reais do saldo da Aços Quiririm, por Pix na Conta Principal', 'A11', c.A(3, 'saldo', 0.0), cedo=c.L(3) - 5)
    c.waitfor(text='Confirmar', timeout=10)
    c.hover(T('Saldo do parceiro'), seconds=1.0, at=c.depois(c.A(3, 'saldo', 0.5)), label='cartão: Saldo do parceiro R$ 1.000,00', optional=True)
    c.click(BT('Confirmar'), at=c.A(3, 'conta', 0.2), label='clique em Confirmar')
    c.mark(4)
    c.fim()
    return c


def cap11():
    """Cadastros (painel vazio): fornecedor (L1), material (L2), ilustração (L3, L4)."""
    c = Cap(11, S_PAINEL, pace=0.5, cps=90, start=(900, 560))
    c.mark(1)
    pede(c, 'Cadastra o fornecedor Sebastião Lima, telefone (12) 9 0000-0147', 'A12', c.A(1, 'conversa', 0.0), cedo=0.3)
    c.waitfor(text='Salvar cadastro', timeout=10)
    c.hover(T('Novo parceiro'), seconds=0.8, at=c.depois(c.A(1, 'nome', 0.5)), label='cartão: Novo parceiro', optional=True)
    c.click(BT('Salvar cadastro'), at=c.depois(c.A(1, 'dele', 0.6)), label='clique em Salvar cadastro')
    c.waitfor(text='Sebastião Lima', timeout=10)
    c.mark(2)
    pede(c, 'Cadastra o material Chumbo, em kg, compra a 6,50 e venda a 8,00', 'A13', c.A(2, 'unidade', 0.0), cedo=c.L(2) - 3)
    c.waitfor(text='Salvar cadastro', timeout=10)
    c.click(BT('Salvar cadastro'), at=c.depois(c.A(2, 'preços', 0.6)), label='clique em Salvar cadastro')
    c.waitfor(text='Chumbo', timeout=10)
    c.mark(3)
    c.mark(4)
    c.fim()
    return c


FOTO = 'arquivos/pesagem-cooperativa.jpg'
TABELA = 'arquivos/tabela-fundicao.png'
CLIPE = SEL(f'{PAINEL} button[aria-label="Anexar foto, arquivo ou planilha"]', noScroll=True)


def cap12():
    """Fotos, planilhas e PDFs (painel vazio): clipe e foto da pesagem (L1), ticket com "Arquivo usado" (L2), ilustração (L3), print de tabela (L4),
    ilustração dos formatos (L5)."""
    c = Cap(12, S_PAINEL, pace=0.5, cps=90, start=(900, 560))
    c.mark(1)
    c.click(CLIPE, at=c.A(1, 'clipe', 0.6), label='clipe (Anexar foto, arquivo ou planilha)')
    c.hover(SEL('[role=menuitem]:has-text("Tirar foto")'), seconds=0.5, at=c.A(1, 'foto', 0.6), label='menu: Escolher foto ou arquivo e Tirar foto', noScroll=True, optional=True)
    c.add({'do': 'upload', 'target': SEL('[role=menuitem]:has-text("Escolher foto ou arquivo")', noScroll=True), 'file': FOTO, 'at': round(c.A(1, 'pesagem', 0.6), 2),
           'label': 'escolhe pesagem-cooperativa.jpg (foto fictícia de um ticket de balança)'})
    c.waitfor(text='pesagem-cooperativa', timeout=10)
    c.mark(2)
    d = c.click(ENVIAR, at=c.L(2) - 3.3, label='Enviar (só a foto)', noScroll=True)
    c.resposta('A15a', d['at'])
    c.waitfor(text='Li os dados da pesagem', timeout=10)
    pede(c, 'Ticket de compra', 'A15b', c.A(2, 'cartão', 0.0), cedo=c.A(2, 'Eu', 0.3))
    c.waitfor(text='Arquivo usado', timeout=10)
    c.hover(T('Arquivo usado'), seconds=1.5, at=c.depois(c.A(2, 'pesos', 0.6)), label='cartão do ticket com Arquivo usado', optional=True)
    c.mark(3)
    c.mark(4)
    c.click(CLIPE, at=c.A(4, 'print', 0.6), label='clipe (segundo arquivo)')
    c.add({'do': 'upload', 'target': SEL('[role=menuitem]:has-text("Escolher foto ou arquivo")', noScroll=True), 'file': TABELA, 'at': round(c.A(4, 'print', 0.0) + 0.9, 2),
           'label': 'escolhe tabela-fundicao.png (print fictício de tabela de preços)'})
    c.waitfor(text='tabela-fundicao', timeout=10)
    d = c.click(ENVIAR, at=c.A(4, 'pergunta', 0.0), label='Enviar (só o print)', noScroll=True)
    c.resposta('A16a', d['at'])
    c.waitfor(text='Li a tabela do anexo', timeout=10)
    pede(c, 'Atualizar', 'A16b', c.A(4, 'compra', 0.0), cedo=c.A(4, 'atualizar', 0.5))
    c.waitfor(text='preços de compra ou de venda', timeout=10)
    c.mark(5)
    c.fim()
    return c


def cap13():
    """Nota fiscal pelo Cato (o `setup` lança a venda da Serra Fina): Preparar NF-e (L1), forma de pagamento (L2), rascunho (L3), prévia do
    DANFE (L4), Criar rascunho (L5), ilustração (L6), Emitir NF-e (L7), autorizada (L8), ilustração (L9)."""
    c = Cap(13, S_PAINEL + setup_venda() + toca_setup('Próximos passos', 'Sem NF-e vinculada') + [{'do': 'eval', 'js': POPS}], pace=0.5, start=(900, 560))
    c.mark(1)
    c.ev(js_fim_da_conversa(), at=c.A(1, 'Preparar', 0.0), label='rola a conversa até o botão Preparar NF-e')
    d = c.click(BT('Preparar NF-e'), at=c.A(1, 'Preparar', 0.6), label='clique em Preparar NF-e (nos próximos passos do pedido; o botão já manda o pedido)')
    c.resposta('A17a', d['at'])
    c.mark(2)
    c.waitfor(text='Qual forma de pagamento deve constar na NF-e', timeout=10)
    pede(c, 'Duplicata a prazo', 'A17b', c.L(3) + 0.3, cedo=c.A(2, 'Eu', 0.3))
    c.waitfor(text='Visualizar prévia do DANFE', timeout=10)
    c.mark(3)
    c.hover(T('item(ns) para Serra Fina'), seconds=0.6, at=c.depois(c.A(3, 'destinatário', 0.6)), label='cartão: Rascunho de NF-e, 1 item(ns) para Serra Fina Alumínio Reciclagem, R$ 5.200,00')
    c.hover(T('Forma de pagamento'), seconds=0.6, at=c.depois(c.A(3, 'valor', 0.6)), label='cartão: Operação, Forma de pagamento, Vencimento')
    c.mark(4)
    c.click(BT('Visualizar prévia do DANFE'), at=c.A(4, 'prévia', 0.6), label='clique em Visualizar prévia do DANFE')
    c.waitfor(text='PDF para revisão', timeout=15)
    c.ev(PDF_JS, label='PDF da prévia do DANFE (aba nova, para a ilustração)')
    c.hover(T('PDF para revisão'), seconds=2.0, at=c.A(4, 'revisar', 0.6), label='ZOOM PDF para revisão. Não transmite a nota.', optional=True)
    c.mark(5)
    c.click(BT('Criar rascunho'), at=c.A(5, 'Criar', 0.6), label='clique em Criar rascunho')
    c.waitfor(text='Rascunho preparado', timeout=10)
    c.hover(BT('Emitir NF-e'), seconds=0.8, at=c.A(5, 'segundo', 0.6), label='Emitir NF-e e Consultar situação (dois botões)', optional=True)
    c.mark(6)
    c.mark(7)
    c.click(BT('Emitir NF-e'), at=c.A(7, 'Emitir', 0.6), label='clique em Emitir NF-e')
    c.waitfor(text='Aguardando confirmação da SEFAZ', timeout=10)
    c.mark(8)
    c.wait(3.5)
    c.click(BT('Consultar situação'), at=c.A(8, 'Autorizada', 0.6), label='clique em Consultar situação')
    c.waitfor(text='NF-e autorizada', timeout=15)
    c.hover(BT('Abrir DANFE'), seconds=1.5, at=c.A(8, 'botão', 0.6), label='ZOOM botão Abrir DANFE (sem clicar)', optional=True)
    c.mark(9)
    c.fim()
    return c


def cap14():
    """Pedidos e revisões (o `setup` lança a compra e a venda): Acompanhar pedidos (L1), Respostas revisadas (L2)."""
    c = Cap(14, S_PAINEL + setup_compra() + setup_venda(), pace=0.5, start=(900, 560))
    MENU = SEL(f'{PAINEL} button[aria-label="Mais opções do Cato"]', noScroll=True)
    VOLTA = SEL(f'{PAINEL} button[aria-label="Voltar à conversa"]', noScroll=True)
    c.mark(1)
    c.click(MENU, at=c.A(1, 'pontinhos', 0.8), label='três pontinhos (Mais opções do Cato)')
    c.click(SEL('[role=menuitem]:has-text("Acompanhar pedidos")', noScroll=True), at=c.A(1, 'Acompanhar', 0.6), label='Acompanhar pedidos')
    c.waitfor(text='Pedidos lançados por você no Cato', timeout=10)
    c.hover(T('Para acompanhar'), seconds=1.0, at=c.A(1, 'receber', 0.6), label='Para acompanhar: a venda da Serra Fina e a compra da Aparecida', optional=True)
    c.mark(2)
    c.click(VOLTA, at=c.L(2) - 1.8, label='Voltar à conversa')
    c.click(MENU, at=c.L(2) - 0.9, label='três pontinhos (de novo)')
    c.click(SEL('[role=menuitem]:has-text("Respostas revisadas")', noScroll=True), at=c.A(2, 'Respostas', 0.4), label='Respostas revisadas')
    c.waitfor(text='Nenhuma resposta revisada', timeout=8)
    c.hover(T('Nenhuma resposta revisada'), seconds=1.5, at=c.A(2, 'revisadas', 0.5), label='Nenhuma resposta revisada', optional=True)
    c.fim()
    return c


def cap15():
    """Limites e permissões (painel vazio): "O que você consegue fazer?" (L1), corte do Marcos (L2; aqui a tela fica parada), ilustração (L3),
    Usuários e Permissões com a restrição (L4), ilustrações (L5, L6), rodapé (L7)."""
    c = Cap(15, S_PAINEL, pace=0.5, start=(900, 560))
    c.mark(1)
    pede(c, 'O que você consegue fazer?', 'A18', c.A(1, 'lista', 0.0), cedo=c.A(1, 'pergunte', 0.0))
    c.waitfor(text='Ações com sua confirmação', timeout=10)
    c.waitfor(text='não transferem dinheiro pela sua conta bancária', timeout=25)
    c.ev(js_rola_el(achar_folha(PAINEL, 'Pagamentos registram a operação', contem=True), 260, 700), at=c.depois(c.A(1, 'lista', 0.3)), label='sobe até o aviso sobre pagamentos')
    c.hover(T('Pagamentos registram a operação'), seconds=1.5, at=c.depois(c.A(1, 'pagamento', 0.6)), label='Pagamentos registram a operação no EcoSistema; não transferem dinheiro pela sua conta bancária.', optional=True)
    c.mark(2)
    c.mark(3)
    c.mark(4)
    c.press('Escape', at=c.L(4) - 1.4, label='fecha o painel', optional=True)
    c.add({'do': 'goto', 'url': '/configuracoes?tab=users', 'at': round(c.L(4) - 0.6, 2), 'label': 'Usuários e Permissões'})
    c.waitfor(text='Marcos Antunes', timeout=20)
    c.add({'do': 'eval', 'label': 'o painel do Cato volta fechado depois de recarregar', 'js': "(async()=>{for(let i=0;i<6;i++){const b=document.querySelector('button[aria-label=\"Fechar o Cato\"]');if(!b)return 'painel fechado';b.click();await new Promise(r=>setTimeout(r,400))}return 'painel fechado'})()"})
    c.click(TXT('Marcos Antunes'), at=c.A(4, 'quem', 0.8), label='escolhe Marcos Antunes na lista')
    c.waitfor(text='Permissões concedidas', timeout=2, optional=True)
    c.add({'do': 'eval', 'label': 'garante o detalhe do Marcos aberto', 'js': "(async()=>{const has=()=>document.body.innerText.includes('Permissões concedidas');if(has())return 'ok';"
           "const e=[...document.querySelectorAll('button,[role=button],div,li')].filter(x=>x.children.length<8&&/Marcos Antunes/.test(x.innerText||'')&&x.innerText.length<80).pop();if(!e)return 'SEM ALVO: linha do Marcos';"
           "e.click();for(let i=0;i<24;i++){await new Promise(r=>setTimeout(r,250));if(has())return 'abriu no segundo toque'}return 'SEM ALVO: detalhe do Marcos'})()"})
    c.click(BTN('Editar'), at=c.A(4, 'restrição', 0.8), label='Editar (permissões do Marcos)')
    c.waitfor(text='Perfis rápidos', timeout=10)
    c.ev(js_rola_el(achar_folha('[role=dialog]', 'Ver somente os pedidos que lançar'), 330, 900), at=c.A(4, 'pedidos', 0.9), label='desce até Ver somente os pedidos que lançar')
    c.hover(TXTP('o Cato fica indisponível para evitar exposição indireta', within='[role=dialog]'), seconds=3.0, at=c.A(4, 'sem', 0.3), label='ZOOM o Cato fica indisponível para evitar exposição indireta', optional=True)
    c.press('Escape', at=c.L(4) + 12.2, label='fecha a janela de edição', optional=True)
    c.mark(5)
    c.mark(6)
    c.mark(7)
    c.add({'do': 'goto', 'url': '/materiais', 'at': round(c.L(7) - 3.5, 2), 'label': 'volta à tela Estoque'})
    c.waitfor(selector='button[aria-label="Abrir o Cato"]', timeout=30)
    c.click(FAB, at=c.L(7) - 1.0, label='abre o Cato', noScroll=True)
    c.hover(NO_PAINEL('p:has-text("O Cato.ai pode cometer erros")'), seconds=1.5, at=c.A(7, 'errar', 0.9), label='rodapé O Cato.ai pode cometer erros', noScroll=True)
    c.fim()
    return c


def cap15b():
    """Corte do cap15, linha 2: o Marcos pede o preço do cobre mel e o Cato recusa."""
    c = Cap(15, login(EMAIL_MARCOS) + IR_ESTOQUE + [ABRE, {'do': 'waitFor', 'selector': PAINEL, 'timeout': 10}],
            pace=0.5, start=(900, 520), sub='b', voz_de=(2, 2), user='marcos')
    c.mark(1)
    pede(c, 'Atualiza o preço de compra do cobre mel pra 43 reais', 'A19', c.A(1, 'responde', 0.0), cedo=c.A(1, 'Marcos', 0.2))
    c.waitfor(text='Nenhum preço foi alterado', timeout=10)
    c.hover(T('Seu usuário não tem permissão para alterar preços'), seconds=2.0, at=c.depois(c.A(1, 'permissão', 0.6)), label='ZOOM Seu usuário não tem permissão para alterar preços.', optional=True)
    c.fim()
    return c


def cap16():
    """Avaliar e falar com o suporte (a conversa R1..R8): joinha e dedo (L1), pesquisa de fim de conversa (L2), Falar com atendente (L3), a janela (L4)."""
    c = Cap(16, restaura(8), pace=0.5, start=(900, 560))
    c.mark(1)
    c.ev(js_msgs_rola(achar_ultimo('button[aria-label="Resposta útil"]').replace('.pop()', '.at(-1)'), 460, 700), at=c.A(1, 'resposta', 0.5), label='sobe até as ações da última resposta')
    c.hover(SEL(f'{PAINEL} button[aria-label="Resposta útil"] >> nth=-1', noScroll=True), seconds=0.5, at=c.A(1, 'joinha', 0.5), label='joinha (Resposta útil)')
    c.click(SEL(f'{PAINEL} button[aria-label="Resposta útil"] >> nth=-1', noScroll=True), at=c.A(1, 'clicar', 0.6), label='clique no joinha')
    c.click(SEL(f'{PAINEL} button[aria-label="Resposta não útil"] >> nth=-2'), at=c.A(1, 'baixo', 0.6), label='dedo pra baixo (outra resposta)')
    c.waitfor(text='Faltou detalhe', timeout=5)
    c.hover(SEL(f'{PAINEL} button:text-is("Número errado")', noScroll=True), seconds=0.4, at=c.A(1, 'motivos', 0.5), label='os motivos')
    c.click(SEL(f'{PAINEL} button:text-is("Faltou detalhe")', noScroll=True), at=c.A(1, 'clique', 0.6), label='Faltou detalhe')
    c.mark(2)
    c.add({'do': 'clock', 'forward': '00:06:00', 'at': round(c.L(2) - 0.4, 2), 'label': 'avança o relógio 6 minutos (as mensagens restauradas têm hora à frente do relógio) (a pesquisa de fim de conversa aparece)'})
    c.waitfor(text='Consegui concluir', timeout=10)
    c.hover(T('Consegui concluir'), seconds=0.6, at=c.A(2, 'resolveu', 0.6), label='pesquisa: Sim / Consegui concluir', optional=True)
    c.click(T('Consegui concluir'), at=c.A(2, 'cliques', 0.6), label='clique em Sim / Consegui concluir', optional=True)
    c.mark(3)
    c.click(SEL(f'{PAINEL} button[aria-label="Mais opções do Cato"]', noScroll=True), at=c.A(3, 'pontinhos', 0.8), label='três pontinhos (Mais opções do Cato)')
    c.click(SEL('[role=menuitem]:has-text("Falar com atendente")', noScroll=True), at=c.A(3, 'Falar', 0.5), label='clique em Falar com atendente')
    c.waitfor(text='Nos conte o que está acontecendo pra resolvermos mais rápido.', timeout=8)
    c.mark(4)
    c.hover(TXTP('Em qual tela/módulo?', within=DLG_SUP), seconds=0.5, at=c.A(4, 'tela', 0.6), label='Em qual tela/módulo? *')
    c.hover(TXTP('O que aconteceu? Descreva com detalhes', within=DLG_SUP), seconds=0.5, at=c.A(4, 'aconteceu', 0.6), label='O que aconteceu? Descreva com detalhes *')
    c.hover(BTN('Falar no WhatsApp', within=DLG_SUP), seconds=1.5, at=c.A(4, 'WhatsApp', 0.7), label='Falar no WhatsApp (sem clicar)')
    c.press('Escape', at=c.L(4) + 8.5, label='fecha a janela')
    c.fim()
    return c


def cap17():
    """Recapitulando: a montagem usa trechos dos outros capítulos; este passeio pelo painel fica de reserva."""
    c = Cap(17, restaura(8), pace=0.5, start=(900, 560))
    for i in range(1, 7):
        c.mark(i)
    c.hover(NO_PAINEL('p:has-text("O Cato.ai pode cometer erros")'), seconds=1.0, at=c.A(1, 'Cato', 0.6), label='rodapé O Cato.ai pode cometer erros', noScroll=True, optional=True)
    c.hover(NO_PAINEL('button:has-text("Abrir posição de estoque") >> nth=-1'), seconds=1.0, at=c.A(2, 'tela', 0.6), label='confira na tela', optional=True)
    c.fim()
    return c


CAPITULOS = {'0': cap00, '1': cap01, '2': cap02, '2b': cap02b, '3': cap03, '4': cap04, '5': cap05, '6': cap06, '7': cap07, '8': cap08, '9': cap09,
             '10': cap10, '11': cap11, '12': cap12, '13': cap13, '14': cap14, '15': cap15, '15b': cap15b, '16': cap16, '17': cap17}


# ---------------------------------------------------------------- main
def main():
    pedidos = [a.lstrip('0') or '0' for a in sys.argv[1:] if re.fullmatch(r'\d+b?', a)]
    feitos = []
    for k, fn in CAPITULOS.items():
        if pedidos and k not in pedidos:
            continue
        c = fn()
        d = c.out()
        json.dump(d, open(os.path.join(HERE, f'{c.nome}.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
        nat = sum(1 for st in d['steps'] if st.get('do') != 'mark')
        feitos.append(f'{c.nome} {nat} passos, {len(c.linhas)} linhas, {c.dur:.1f} s{" (fala estimada)" if c.estimado else ""}')
        if os.environ.get('ANCORAS'):
            for i, p, t in c.anchors:
                print(f'   {c.nome} L{i} {p!r} -> {t}')
        if os.environ.get('PREVISTO'):
            for linha in c.previsto:
                print(f'   {c.nome} {linha}')
    print('\n'.join(feitos))


if __name__ == '__main__':
    main()
