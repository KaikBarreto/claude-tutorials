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
 - O 1º gesto com cursor do capítulo ganha AQUECE (0,9 s) a mais de folga: a 1ª busca de alvo numa página nova custa ~1,5 s até agir.
 - Calibre as folgas pelo ensaio rápido (tAct - tStart no actions.json) e confira com o prever.py antes do completo; medida tirada com a
   máquina carregada (renders, 11/11 13:30-17:35) não vale: grave de novo antes de mexer em âncora.
 - `confere*` LÊ a tela e compara com a fala ("OK"/"DIFERENTE", o resumo.py acusa); `OBS` guarda em window.__avisos todo aviso de erro
   do app e o último passo devolve a lista (tem de sair vazia).
 - Ilustração que cobre a janela (roteiro [ILUSTRAÇÃO]): o robô fica parado ou mexe só por `eval` (sem cursor, sem zoom automático).
 - Aviso (sonner, embaixo à direita, y ~700-780): fica ABAIXO da faixa útil do robô (96..730 px). Hover/clique nele SEMPRE com
   `noScroll=True`, senão o robô rola a página, leva o cursor para o meio e o aviso some (as falhas de aviso do T03 eram isso). O cursor
   vai até ele por coordenada (`rolar(0, ponto=(990, 748))`, sem depender da página) logo depois do gesto que o cria; com o mouse em
   cima o sonner segura o aviso até a palavra. Alvo pelo TEXTO (o Radix ainda marca a página aria-hidden enquanto uma janela sai).

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
 - PDF (cap09) abre noutra aba, que o robô não grava (aba única, Chromium sem leitor de PDF): o roteiro pega o PDF que o app gerou
   (URL.createObjectURL embrulhado no setup) e o guarda no Supabase falso (tabela t03_pdfs); t03_pdfs.py, logo depois da gravação, grava
   $TUT_HOME/t03/pdf/*.pdf e a 1ª página em PNG para a edição montar a "aba nova" (fora de rec/: não vai para o git).

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
         'Editar preços em massa', 'Margem automática: a tabela toda', 'Margem automática: uma por material', 'O resumo e a margem fora da regra',
         'A margem no cadastro do material', 'Várias tabelas de preço', 'Duplicar, fixar e trocar a principal', 'Movimentar, transferir e zerar',
         'Exportar estoque e tabela', 'Excluir um material', 'Recapitulando']
# estado de partida (sementes extras sobre o mundo base): t03/inicio + o último apos-capNN; o cap07 (Nova Compra) abre o caixa #85 do
# Rafael às 08:30 (MUNDO_LINHA_DO_TEMPO §9; o base/caixa-aberto é o das 08:05 da T6)
SEMENTE = {0: [], 1: [], 2: [], 3: ['apos-cap02'], 4: ['apos-cap03'], 5: ['apos-cap04'], 6: ['apos-cap05'], 7: ['apos-cap06'], 8: ['apos-cap06'],
           9: ['apos-cap06', 'margem-fora'], 10: ['apos-cap06', 'margem-material'], 11: ['apos-cap06'], 12: ['apos-cap07'], 13: ['apos-cap07'],
           14: ['apos-cap08'], 15: ['apos-cap08'], 16: ['apos-cap08']}
# (os nomes apos-capNN das sementes são os da numeração antiga, de antes da margem automática; ver plano.md)
EXTRA_BASE = {11: ['caixa-0830']}

# folga de cada gesto: segundos entre o início do passo e o instante em que ele age (pace 0,5; medido no ensaio do T03 e na tabela
# "Custo real dos gestos" do docs/04). O `at` = palavra - folga faz o cursor CHEGAR na palavra.
AQUECE = 0.9   # folga a mais do 1º gesto com cursor de cada capítulo (ver Cap._p)
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
        s.aquecido = False
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

    def at(s, w, gesto, extra=0.0):
        """w = (linha, 'palavra'[, nth][, folga]) ou um número (segundos); devolve o `at` = palavra - folga do gesto (- extra)"""
        if w is None:
            return None
        if isinstance(w, (int, float)):
            return round(max(0.0, w), 2)
        i, palavra = w[0], w[1]
        nth = w[2] if len(w) > 2 else None
        folga = (w[3] if len(w) > 3 else FOLGA[gesto]) + extra
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
        # 1º gesto com cursor do capítulo: o robô ainda aquece (1ª busca de alvo na página nova), ~0,9 s a mais até agir (ensaios rápidos
        # de 11/11 após 17:35: 1,4 a 1,7 s no cap00, cap06 e cap07, contra 0,7 a 0,8 s dos outros gestos)
        extra = 0.0
        if 'target' in d and d['do'] in ('click', 'hover', 'type') and not s.aquecido:
            s.aquecido = True
            extra = AQUECE
        at = s.at(w, gesto, extra)
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
        extra = 0.0
        if not s.aquecido:   # 1º gesto com cursor do capítulo (ver _p)
            s.aquecido = True
            extra = AQUECE
        at = s.at(w, 'hover', extra)
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
        """lê o VALOR dos campos (input/textarea) do escopo e compara com o que a fala diz (escopo pode ser 'CSS tr:has-text(\'X\')': linha com o texto)"""
        esp = [esperados] if isinstance(esperados, str) else list(esperados)
        m = re.match(r"^(.*? tr):has-text\('(.*)'\)$", escopo)
        base, txt = (m.group(1), m.group(2)) if m else (escopo, '')
        js = ("(async()=>{const esp=%s;let out='';for(let i=0;i<12;i++){const nos=[...document.querySelectorAll(%s)].filter(n=>!%s||n.innerText.includes(%s));"
              "const v=nos.flatMap(n=>[...n.querySelectorAll('input, textarea')]).map(e=>e.value).join(' | ');"
              "const falta=esp.filter(e=>!v.includes(e));if(!falta.length)return 'OK: '+esp.join(' | ');out='DIFERENTE: faltou '+JSON.stringify(falta)+' em: '+v.slice(0,260);"
              "await new Promise(r=>setTimeout(r,300));}return out})()") % (json.dumps(esp, ensure_ascii=False), json.dumps(base), json.dumps(txt, ensure_ascii=False), json.dumps(txt, ensure_ascii=False))
        return s.add({'do': 'eval', 'js': js, 'label': 'confere ' + label})

    def marca(s, i):
        """solta já as marcas até a da linha i (no tempo delas): esperas e conferências que vêm depois não as atrasam"""
        s.flush(max(0.0, s.L(i) - 0.9))

    def fim(s):
        s.flush(1e9)
        s.steps.append({'do': 'eval', 'js': 'JSON.stringify(window.__avisos || "sem observador")', 'label': 'avisos de erro na tela'})
        s.steps.append({'do': 'mark', 'name': 'FIM', 'at': round(s.dur, 2)})

    def out(s):
        sem = s.seed_extra if s.seed_extra is not None else ([f'{AULA}/inicio'] + [f'{AULA}/{x}' for x in SEMENTE[s.n]] + [f'{AULA}/{x}' for x in EXTRA_BASE.get(s.n, [])])
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


JS_PDF_GANCHO = ("(()=>{if(window.__pdfs)return 'ja';window.__pdfs=[];window.__abas=[];const o=URL.createObjectURL.bind(URL);"
                 "URL.createObjectURL=(b)=>{try{if(b&&b.type==='application/pdf')window.__pdfs.push(b)}catch(e){}return o(b)};"
                 "const wo=window.open.bind(window);window.open=(...a)=>{const w=wo(...a);if(w)window.__abas.push(w);return w};return 'gancho'})()")


def js_pdf(k, nome):
    """guarda o k-ésimo PDF que o app gerou numa tabela de bastidor do Supabase falso (t03_pdfs, base64; o fetch para o endereço do build é
    desviado para a MINHA instância): o actions.json fica pequeno (o PDF A4 da tabela tem ~15 MB) e o t03_pdfs.py, logo depois da
    gravação, grava o arquivo e a 1ª página em PNG para a edição"""
    url = MUNDO['env']['fakeUrl'].rstrip('/') + '/rest/v1/t03_pdfs'
    return ("(async()=>{for(let i=0;i<30&&!(window.__pdfs&&window.__pdfs.length>%d);i++)await new Promise(r=>setTimeout(r,200));"
            "const b=window.__pdfs&&window.__pdfs[%d];if(!b)return 'SEM PDF';const u=new Uint8Array(await b.arrayBuffer());let s='';"
            "for(let i=0;i<u.length;i+=8192)s+=String.fromCharCode.apply(null,u.subarray(i,i+8192));"
            "const r=await fetch(%s,{method:'POST',headers:{'content-type':'application/json',apikey:%s,Prefer:'return=minimal'},"
            "body:JSON.stringify({nome:%s,bytes:u.length,b64:btoa(s)})});(window.__abas||[]).forEach(w=>{try{w.close()}catch(e){}});"
            "return {pdf:%s,bytes:u.length,guardado:r.status}})()") % (
        k, k, json.dumps(url), json.dumps(MUNDO['env']['anonKey']), json.dumps(nome), json.dumps(nome))


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
    c.marca(4)  # a tela carrega já na L4
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
    c.hover(SEL("main button[title='Como funciona']"), 0.9, w=(1, 'interrogação'), label='interrogação Como funciona (os tipos de tabela)')
    c.hover(BTN('Movimentar estoque'), 0.2, w=(2, 'Movimentar'), label='Movimentar estoque')
    c.hover(BTN('Editar Preços'), 0.2, w=(2, 'Editar'), label='Editar Preços')
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
    c.click(TH('Estoque'), w=(5, 'título'), label='clique em Estoque Atual: ordena a lista')
    c.click(TH('Código'), w=(5, 'ordena'), label='clique em Código: volta à ordem do código')
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
    c.click(OPT('Kg — Quilograma'), w=(3, 'trocar'), label='fica em Kg — Quilograma')  # no "aqui." a L4 (preços) já chegava
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
    c.waitfor(gone={'text': 'Valores e estoque'}, timeout=8)
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
    # o menu abre ainda por baixo da ilustração do L3 (a L4 "Abro o Editar e digito zero, sete, zero" não tem folga para ele)
    abre_acoes(c, 'Radiador de cobre', 'Editar', w=(3, 'radiador', None, 0.8), w_item=(4, 'Abro', None, 0.7))
    c.waitfor(text='Editar Material', timeout=8)
    c.click(CAMPO('code'), w=(4, 'digito', None, 0.7), label='campo Código', primeiro=True)
    c.type(CAMPO('code'), '0', w=(4, 'zero', 0, 0.35), clicar=False, clear=True, label='apaga o 16 e digita 0: o campo fica vazio (zoom: Código e Fica assim)')
    c.type(CAMPO('code'), '7', w=(4, 'sete,'), clicar=False, label='digita 7')
    c.type(CAMPO('code'), '0', w=(4, 'zero', 1), clicar=False, label='digita 0: 70')
    c.confere_campos(['70'], 'campo Código 70')
    c.confere('dlg', ['Fica assim: 70'], 'Fica assim: 70')
    c.hover(PD('Fica assim:'), 1.4, w=(5, 'código'), label='Fica assim: 70')
    # F10 (decisão de 20/11): o Prefixo. Digita P (Fica assim: P70), a L7 explica, e o P é apagado ANTES do Atualizar (o mundo segue com o código 70)
    c.type(CAMPO('code_prefix'), 'P', w=(6, 'P,'), label='campo Prefixo: P')   # a voz real escreve "Digito P," (troca do config_narracao)
    c.confere('dlg', ['Fica assim: P70', 'O prefixo aparece na tela, no comprovante e na nota fiscal. O número no banco não muda.'], 'Fica assim: P70 e o aviso do prefixo')
    c.hover(PD('O prefixo aparece na tela'), 1.4, w=(7, 'prefixo'), label='aviso: o prefixo aparece na tela, no comprovante e na nota fiscal')
    c.ev(js_valor(f'{DLG} #code_prefix', ''), w=(7, 'apago.', None, 0.0), label='apaga o P (sem cursor)')
    c.confere('dlg', ['Fica assim: 70'], 'volta a Fica assim: 70')
    c.click(BTN('Atualizar', within=DLG), w=(8, 'Atualizar,'), label='Atualizar')
    c.waitfor(text='Material atualizado!', timeout=10)
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.hover(CELULA('Radiador de cobre', 2), 1.4, w=(8, 'setenta.'), label='célula Código 70')
    c.confere('row:Radiador de cobre', ['70', 'Radiador de cobre'], 'código 70')
    c.fim()
    return c


def cap04():
    """O NCM e a nota fiscal: (ilustração L1, por baixo dela o Editar abre sem cursor) NCM pela busca do seletor (7404.00.00),
    Identificação/Produto Fiscal e a ajuda, (ilustrações L6, L7) Atualizar, (ilustração L9)."""
    c = Cap(4, setup_estoque(busca='radiador'))
    c.ev(js_menu_item('Radiador de cobre', 'Editar'), w=(1, 'vai', None, 1.0), label='abre o Editar do radiador (por baixo da ilustração, sem cursor)')
    c.waitfor(text='Editar Material', timeout=8)
    c.ev(js_rola_ate('Fiscal e organização', y=380, escopo=DLG), w=(2, 'cadastro,', None, 0.3), label='desce até Fiscal e organização')
    c.hover(CAMPO('ncm'), 0.6, w=(2, 'NCM.'), label='NCM (Nota Fiscal), vazio')
    c.hover(SEL(f"{DLG} button[title='Selecionar NCM padrão']"), 0.6, w=(2, 'interrogação'), label='interrogação Selecionar NCM padrão')
    c.click(SEL(f"{DLG} button[title='Selecionar NCM padrão']"), w=(3, 'janela'), label='abre Selecionar NCM para Materiais Recicláveis')
    c.waitfor(text='Selecionar NCM para Materiais Recicláveis', timeout=8)
    c.type({'placeholder': 'Buscar por código NCM ou descrição...'}, 'cobre', w=(3, 'Busco', None, 1.2), cps=30, label='busca cobre')
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
    c.marca(9)   # L9 é ilustração: a marca sai no tempo, as esperas vêm depois
    c.waitfor(text='Material atualizado!', timeout=10)
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
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
    # L3 "o nome, a cor e o ícone" cabe em 1,6 s: clique+digitação num passo só, e cada gesto na sua palavra
    c.ev(js_rola_ate('Novo grupo', y=180, escopo=DLG, dur_ms=500), w=(3, 'No', None, 0.9), label='desce até Novo grupo (Adicionar fica na tela)')
    c.type(SEL(f"{DLG} input[placeholder='Ex: Metais, Plásticos, Papéis']"), 'Radiadores', w=(3, 'novo'), cps=40, label='Nome do grupo: Radiadores')
    c.hover(SEL(f"{DLG} input[type=color]"), 0.2, w=(3, 'cor'), label='Cor')
    c.ev(js_valor(f"{DLG} input[type=color]", '#0f766e'), label='Cor verde-petróleo #0F766E (valor do campo, sem a janela nativa)')
    c.click(SEL(f"{DLG} button.rounded-full.w-12"), w=(3, 'ícone.'), label='Ícone (abre a grade)')
    c.waitfor(target=SEL(f"{POP} button:has(svg.lucide-car)"), timeout=6)
    c.click(SEL(f"{POP} button:has(svg.lucide-car)"), w=(3, 'carro', 0), label='ícone carro')
    c.click(BTN('Adicionar', within=DLG), w=(4, 'Adicionar,'), label='Adicionar')
    c.waitfor(text='Grupo criado', timeout=8)
    c.confere('dlg', ['Radiadores'], 'Radiadores na lista de grupos')
    fecha_janela(c, w=(4, 'está', None, 0.3))
    # L5 é apertada (busca, menu, Editar, Grupo, a lista e o "+" em ~10 s): a busca, que a fala não cita, vai sem cursor
    c.ev(js_valor('main input[placeholder="Buscar material por código ou nome..."]', 'radiador'), label='busca radiador (sem cursor: a fala não cita)')
    c.waitfor(target=P('Radiador de cobre'), timeout=8)
    abre_acoes(c, 'Radiador de cobre', 'Editar', w=(5, 'Agora', None, 0.9))
    c.waitfor(text='Editar Material', timeout=8)
    c.ev(js_rola_ate('Fiscal e organização', y=250, escopo=DLG, dur_ms=450), label='desce até o campo Grupo')
    c.click(CAMPO('group_id'), w=(5, 'Grupo', 0), label='campo Grupo (abre a lista)')
    c.click(OPT('Radiadores'), noScroll=True, label='Radiadores')   # 1.60.22: a opção fica abaixo da faixa do robô (y ~847): sem noScroll ele esperava ~7 s
    c.hover(SEL(f"{DLG} button[aria-label='Criar grupo']"), 1.4, w=(5, 'mais,'), label='botão + Criar grupo (sem clicar)')
    c.click(BTN('Atualizar', within=DLG), w=(6, 'Atualizar.'), label='Atualizar')
    c.waitfor(gone={'role': 'dialog'}, timeout=10)  # a janela só fecha depois de salvar; o confere da linha prova o grupo
    c.hover(CELULA('Radiador de cobre', 3), 0.2, w=(6, 'grupo'), label='Radiadores embaixo do nome, com a bolinha')
    c.confere('row:Radiador de cobre', ['Radiador de cobre', 'Radiadores'], 'grupo Radiadores na linha')
    # L7 tem 5 s e o filtro pede 6 cliques (~1,05 s cada): ele abre no fim da L6 ("com a cor dele") e os 5 desmarques ficam na L7
    c.ev(js_valor('main input[placeholder="Buscar material por código ou nome..."]', ''), w=(6, 'nome,', None, 0.7), label='limpa a busca (sem cursor)')
    c.click(BTNX('Todos os Materiais'), label='filtro Todos os Materiais')
    c.waitfor(target=SEL(f"{POP} label:has-text('Alumínio')"), timeout=6)
    c.marca(7)
    for k, g in enumerate(('Alumínio', 'Ferrosos', 'Metais', 'Outros', 'Radiadores')):
        c.click(SEL(f"{POP} label:has-text('{g}') button[role=checkbox]"), label=f'desmarca {g}')
    c.confere(POP, ['Cobre'], 'só o Cobre marcado')
    c.press('Escape', w=(7, 'cobre.', None, -0.4), label='fecha o filtro (botão: 3 materiais)')
    c.pause(0.4)
    c.confere('main', ['3 materiais'], 'botão do filtro: 3 materiais')
    c.hover(P('Peso Total em Estoque'), 0.5, w=(8, 'peso', None, 1.1), label='cartões só do cobre (zoom)')  # peso e valor a 0,7 s um do outro
    c.hover(P('Total Pago'), 1.0, w=(8, 'valor'), label='Total Pago do cobre')
    c.click(BTNX('3 materiais'), w=(9, 'voltar,'), label='abre o filtro')
    c.click(SEL(f"{POP} label:has-text('Todos os Materiais') button[role=checkbox]"), w=(9, 'Todos'), label='Todos os Materiais')
    c.press('Escape', label='fecha o filtro')
    c.pause(0.4)
    c.confere('main', ['Todos os Materiais'], 'filtro de volta em Todos os Materiais')
    c.fim()
    return c


# ---------------------------------------------------------------- Editar Preços (1.60.18: tela cheia) e Margem automática
CHAVE = {'role': 'switch', 'name': 'Margem automática'}
ASIDE = SEL(f"{DLG} aside[aria-label='Resumo e regras da tabela']")
BUSCA_PRECOS = SEL(f"{DLG} input[placeholder='Buscar por código ou nome...']")
ALERTA = '[role=alertdialog]'
LINHA = lambda nome: SEL(f"{DLG} tbody tr:has-text('{nome}')")
CAMPOS = lambda nome, k: SEL(f"{DLG} tbody tr:has-text('{nome}') input", nth=k)   # com margem ligada: 0 compra, 1 margem, 2 venda; sem: 0 compra, 1 venda
TABELA_TODA = {'role': 'button', 'name': 'Tabela toda', 'exact': False, 'within': DLG}
RESUMO_LINHA = lambda rotulo: SEL(f"{DLG} aside button:has-text('{rotulo}'), {DLG} aside div:has(> span:text-is('{rotulo}'))")
GRADE_LINHA = lambda i: f"{DLG} tbody tr:nth-child({i})"


def abre_editar_precos(c, w, label='Editar Preços (tela cheia)'):
    c.click(BTN('Editar Preços'), w=w, label=label)
    c.waitfor(text='Editar Tabelas de Preço', timeout=10)
    c.waitfor(target=LINHA('Ferro pesado'), timeout=10)


def sair_cancelando(c, w, label='Cancelar (nada é salvo)'):
    c.click(BTN('Cancelar', within=DLG), w=w, noScroll=True, label=label)
    c.waitfor(gone={'role': 'dialog'}, timeout=8)


def cap06():
    """Editar preços em massa (1.60.18): Editar Preços em tela cheia, busca cobre, +0,50 nos três cobres, dica da venda abaixo da compra
    (bronze: 28,00, Salvar, aviso, Cancelar, volta a 33,50), Salvar."""
    c = Cap(6, setup_estoque())
    c.hover(BTN('Editar Preços'), 0.6, w=(1, 'Editar'), label='Editar Preços')
    abre_editar_precos(c, (2, 'abre'), 'abre Editar Tabelas de Preço (tela cheia)')
    c.hover(PD('Tabelas disponíveis'), 0.5, w=(2, 'esquerda'), label='Tabelas disponíveis: Principal (Padrão)')
    c.hover(SEL(f"{DLG} thead th:has-text('Compra')"), 0.3, w=(2, 'compra'), label='Compra (R$)')
    c.hover(SEL(f"{DLG} thead th:has-text('Venda')"), 0.3, w=(2, 'venda'), label='Venda (R$)')
    c.hover(ASIDE, 0.6, w=(2, 'resumo'), label='Resumo da tabela (coluna da direita)')
    c.hover(BTN('Sair da edição', within=DLG, exact=False), 0.3, w=(2, 'Sair'), noScroll=True, label='Sair')
    c.hover(BTN('Cancelar', within=DLG), 0.4, w=(2, 'Cancelar'), noScroll=True, label='Cancelar')
    c.type(BUSCA_PRECOS, 'cobre', w=(3, 'Busco'), cps=CPS, label='busca cobre')
    c.confere('dlg', ['Cobre mel', 'Cobre misto', 'Fio de cobre encapado', 'Radiador de cobre'], 'ficam só os cobres')
    c.click(CAMPOS('Cobre mel', 0), w=(4, 'compra'), label='Cobre mel: Compra')
    c.type(CAMPOS('Cobre mel', 0), '42,50', w=(4, 'quarenta', 0), clicar=False, clear=True, label='Cobre mel compra 42,50 (zoom: linha Cobre mel)')
    c.click(CAMPOS('Cobre mel', 1), w=(4, 'venda'), label='Cobre mel: Venda')
    c.type(CAMPOS('Cobre mel', 1), '47,90', w=(4, 'quarenta', 1), clicar=False, clear=True, label='Cobre mel venda 47,90')
    for k, (nome, comp, vend) in enumerate((('Cobre misto', '36,00', '41,50'), ('Fio de cobre encapado', '18,00', '22,00'))):
        w0 = (5, 'Faço') if k == 0 else None
        c.type(CAMPOS(nome, 0), comp, w=w0, clear=True, cps=40, label=f'{nome} compra {comp} (selo 4x)')
        c.type(CAMPOS(nome, 1), vend, clear=True, cps=40, label=f'{nome} venda {vend} (selo 4x)')
    c.press('Tab', label='sai da célula (o valor assenta)')
    c.confere('dlg', ['3 material(is) com alterações pendentes'], 'aviso 3 material(is) com alterações pendentes')
    c.hover(CAMPOS('Cobre misto', 0), 0.8, w=(6, 'células'), label='células alteradas com a marca')
    c.hover(PD('com alterações pendentes'), 1.4, w=(6, 'aviso'), noScroll=True, label='aviso 3 material(is) com alterações pendentes (rodapé)')
    # L7 e L8: venda abaixo da compra (nada disso é salvo: o robô desfaz)
    c.type(BUSCA_PRECOS, 'bronze', w=(7, 'bronze'), clear=True, cps=CPS, label='busca bronze')
    c.type(CAMPOS('Bronze', 1), '28,00', w=(7, 'oito'), clear=True, label='Bronze venda 28,00 (abaixo da compra de 29,00)')
    c.press('Tab', label='sai da célula')
    c.confere('dlg', ['Venda abaixo da compra'], 'resumo: Venda abaixo da compra')
    c.hover(PD('Venda abaixo da compra'), 1.2, w=(7, 'resumo'), label='Resumo: Venda abaixo da compra 1 (zoom)')
    c.click(BTN('Salvar', within=DLG), w=(8, 'Salvar', 0), noScroll=True, label='Salvar (com a venda abaixo da compra)')
    c.waitfor(text='Preço de venda abaixo do custo', timeout=8)
    c.hover({'text': 'Preço de venda abaixo do custo'}, 1.6, w=(8, 'prejuízo'), label='Preço de venda abaixo do custo (zoom: a janela)')
    c.click(BTN('Cancelar', within=ALERTA), w=(8, 'cancelo'), label='Cancelar (a janela fecha, nada foi salvo)')
    c.waitfor(gone={'role': 'alertdialog'}, timeout=6)
    c.type(CAMPOS('Bronze', 1), '33,50', w=(8, 'volto'), clear=True, label='Bronze venda de volta a 33,50')
    c.press('Tab', label='sai da célula')
    c.ev(js_valor(f"{DLG} input[placeholder='Buscar por código ou nome...']", ''), w=(8, 'Se', 1), label='limpa a busca (sem cursor)')
    c.confere('dlg', ['3 material(is) com alterações pendentes'], 'voltou a 3 alterações')
    # L9: Salvar (o aviso vive 4 s: o cursor vai direto a ele)
    c.click(BTN('Salvar', within=DLG), w=(9, 'Salvar.'), noScroll=True, label='Salvar (rodapé da tela)')
    c.waitfor(text='Preços atualizados!', timeout=10)
    ini = round(c.W(9, 'Salvar.') + 1.4, 2)
    c.rolar(0, ponto=(990, 748), duration=0.3, after=0, label='cursor no lugar do aviso (embaixo à direita)')
    c.hover({'text': 'As tabelas vinculadas serão recalculadas'}, round(c.W(9, 'vinculadas:') + 0.6 - ini - 0.55, 2), timeout=8, noScroll=True,
            label='aviso Preços atualizados! As tabelas vinculadas... (o mouse segura o aviso)')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.confere('main', ['R$ 42,50', 'R$ 47,90'], 'Cobre mel 42,50 e 47,90 na lista')
    c.fim()
    return c


def cap07():
    """Margem automática, alcance Tabela toda: liga a chave, Tabela toda, 15 %, Compra fica, Aplicar; compra 38 > venda 43,70; venda 46 > compra 40;
    Editar margem 20 %; cadeado do Ferro misto (40 %); Cancelar (nada é salvo)."""
    c = Cap(7, setup_estoque())
    abre_editar_precos(c, (1, 'Editar'), 'abre Editar Preços')
    c.hover(CHAVE, 0.8, w=(1, 'cartão'), label='cartão Margem automática (a chave)')
    c.click(CHAVE, w=(2, 'Ligo'), label='liga a chave Margem automática')
    c.waitfor(text='Alcance da margem', timeout=6)
    c.hover(TABELA_TODA, 0.4, w=(2, 'Tabela', 0), label='alcance Tabela toda')
    c.hover({'role': 'button', 'name': 'Por material', 'exact': False, 'within': DLG}, 0.4, w=(2, 'Por'), label='alcance Por material')
    c.click(TABELA_TODA, w=(2, 'Escolho'), label='escolhe Tabela toda')
    c.waitfor(target=SEL('input[aria-label="Margem da tabela"]'), timeout=6)
    c.hover(PD('Sobre a compra:'), 1.0, w=(3, 'dez'), label='Sobre a compra: R$ 10,00 com 30% vira R$ 13,00 (zoom)')
    c.type(SEL('input[aria-label="Margem da tabela"]'), '15', w=(3, 'quinze'), clear=True, label='margem da tabela 15')
    c.hover(SEL(f"{DLG} button[aria-pressed]:text-is('R$')"), 0.6, w=(3, 'reais', 2), label='botão R$ (margem em reais por quilo)')
    c.hover(SEL(f"{DLG} button[aria-pressed]:has-text('A venda é recalculada')"), 0.4, w=(4, 'compra', 0), label='Qual preço fica como está: Compra')
    c.hover(SEL(f"{DLG} button[aria-pressed]:has-text('A compra é recalculada')"), 0.4, w=(4, 'venda', 1), label='Qual preço fica como está: Venda')
    c.click(SEL(f"{DLG} button[aria-pressed]:has-text('A venda é recalculada')"), w=(4, 'Deixo'), label='Compra fica como está')
    c.click(BTN('Aplicar', within=DLG), w=(4, 'Aplicar'), label='Aplicar')
    c.waitfor(text='Tabela toda · 15%', timeout=8)
    c.hover(CAMPOS('Cobre misto', 0), 0.6, w=(5, 'cobre'), label='Cobre misto: compra 36,00')
    c.confere_campos(['36,00', '41,40'], 'Cobre misto 36,00 e 41,40', escopo=LINHA('Cobre misto')['selector'])
    c.hover(CAMPOS('Cobre misto', 2), 1.0, w=(5, 'quarenta', 0), label='Cobre misto: venda 41,40 (zoom: linha Cobre misto)')
    c.hover(CAMPOS('Ferro pesado', 2), 1.0, w=(5, 'milésimo'), label='Ferro pesado: venda 1,093 (o milésimo)')
    c.hover(PD('com alterações pendentes'), 1.2, w=(5, 'aviso'), noScroll=True, label='aviso: margem automática com alterações pendentes (rodapé)')
    c.type(CAMPOS('Cobre misto', 0), '38,00', w=(6, 'trinta'), clear=True, label='Cobre misto compra 38,00')
    c.press('Tab', label='sai da célula')
    c.confere_campos(['38,00', '43,70'], 'Cobre misto 38,00 e 43,70', escopo=LINHA('Cobre misto')['selector'])
    c.hover(CAMPOS('Cobre misto', 2), 1.0, w=(6, 'quarenta'), label='Cobre misto: venda 43,70 (zoom)')
    c.type(CAMPOS('Cobre misto', 2), '46,00', w=(7, 'quarenta', 0), clear=True, label='Cobre misto venda 46,00')
    c.press('Tab', label='sai da célula')
    c.confere_campos(['40,00', '46,00'], 'Cobre misto 40,00 e 46,00', escopo=LINHA('Cobre misto')['selector'])
    c.hover(CAMPOS('Cobre misto', 0), 1.0, w=(7, 'quarenta', 1), label='Cobre misto: compra 40,00 (zoom)')
    c.click(BTN('Editar margem', within=DLG, exact=False), w=(8, 'Editar'), label='Editar margem')
    c.waitfor(target=SEL('input[aria-label="Margem da tabela"]'), timeout=6)
    c.type(SEL('input[aria-label="Margem da tabela"]'), '20', w=(8, 'vinte'), clear=True, label='margem da tabela 20')
    c.confere_campos(['40,00', '48,00'], 'Cobre misto 40,00 e 48,00', escopo=LINHA('Cobre misto')['selector'])
    c.hover(CAMPOS('Cobre misto', 2), 1.0, w=(8, 'tabela', 0), label='venda recalculada na hora')
    cad = lambda n: SEL(f"{DLG} tbody tr:has-text('{n}') button[aria-label='Personalizar a margem deste material']")
    c.click(cad('Ferro misto'), w=(9, 'cadeado', 0), label='abre o cadeado do Ferro misto')
    c.type(CAMPOS('Ferro misto', 1), '40', w=(9, 'quarenta'), clear=True, label='Ferro misto margem 40')
    c.press('Tab', label='sai da célula')
    c.confere('dlg', ['personalizada'], 'selo personalizada no Ferro misto')
    c.hover(LINHA('Ferro misto'), 1.2, w=(9, 'personalizada'), label='Ferro misto: selo personalizada (zoom na linha)')
    c.click(SEL(f"{DLG} tbody tr:has-text('Ferro misto') button[aria-label='Voltar à margem da tabela']"), w=(9, 'Fechando'), label='fecha o cadeado do Ferro misto')
    c.hover(BTN('Salvar', within=DLG), 0.5, w=(10, 'Salvar'), noScroll=True, label='Salvar')
    sair_cancelando(c, (10, 'Cancelar.'))
    c.fim()
    return c


def cap08():
    """Margem automática, alcance Por material: liga a chave, unidade %, Aplicar (nenhum preço muda); cobre misto 15 %; bronze em R$ (5,00); compra 30;
    Mesma margem em vários materiais (busca alumínio, 20 %); Cancelar."""
    c = Cap(8, setup_estoque())
    abre_editar_precos(c, (1, 'Abro'), 'abre Editar Preços')
    c.click(CHAVE, w=(1, 'ligo'), label='liga a chave Margem automática')
    c.waitfor(text='Manter a margem que cada material já tem hoje', timeout=6)
    c.hover(SEL(f"{DLG} aside button[aria-pressed='true']:text-is('%')"), 0.5, w=(2, 'porcentagem', 0), label='unidade %')
    c.hover(SEL(f"{DLG} aside button[aria-pressed='false']:text-is('R$')"), 0.5, w=(2, 'reais'), label='unidade R$')
    c.click(BTN('Aplicar', within=DLG), w=(2, 'Aplicar'), label='Aplicar')
    c.waitfor(text='Por material · cada material com a sua margem', timeout=8)
    c.hover(SEL(f"{DLG} thead th:has-text('Margem')"), 0.4, w=(3, 'coluna'), label='coluna Margem')
    c.hover(CAMPOS('Cobre mel', 1), 0.8, w=(3, 'cobre'), label='Cobre mel: margem 12,71 (zoom)')
    c.hover(CAMPOS('Ferro misto', 1), 0.8, w=(3, 'ferro'), label='Ferro misto: margem 40')
    c.hover(CAMPOS('Cobre misto', 1), 0.5, w=(4, 'cobre'), label='Cobre misto: margem 15,28')
    c.type(CAMPOS('Cobre misto', 1), '15', w=(4, 'quinze', 1), clear=True, label='Cobre misto margem 15')
    c.press('Tab', label='sai da célula')
    c.confere_campos(['36,00', '15', '41,40'], 'Cobre misto 36,00, 15% e 41,40', escopo=LINHA('Cobre misto')['selector'])
    c.hover(CAMPOS('Cobre misto', 2), 0.9, w=(4, 'quarenta', 0), label='Cobre misto: venda 41,40 (zoom)')
    c.click(SEL(f"{DLG} tbody tr:has-text('Bronze') button[title^='Margem em porcentagem']"), w=(5, 'clico'), label='botão de reais da linha do Bronze')
    c.confere_campos(['29,00', '4,50', '33,50'], 'Bronze 29,00, R$ 4,50 e 33,50', escopo=LINHA('Bronze')['selector'])
    c.hover(CAMPOS('Bronze', 1), 0.9, w=(5, 'quatro', 0), label='Bronze: margem 4,50 (zoom)')
    c.type(CAMPOS('Bronze', 1), '5', w=(5, 'digito'), clear=True, label='Bronze margem R$ 5')
    c.press('Tab', label='sai da célula')
    c.confere_campos(['29,00', '5', '34,00'], 'Bronze 29,00, R$ 5 e 34,00', escopo=LINHA('Bronze')['selector'])
    c.type(CAMPOS('Bronze', 0), '30,00', w=(6, 'compra', 0), clear=True, label='Bronze compra 30,00')
    c.press('Tab', label='sai da célula')
    c.confere_campos(['30,00', '35,00'], 'Bronze 30,00 e 35,00', escopo=LINHA('Bronze')['selector'])
    c.hover(CAMPOS('Bronze', 2), 1.0, w=(6, 'trinta', 1), label='Bronze: venda 35,00 (zoom)')
    c.type(BUSCA_PRECOS, 'alumínio', w=(7, 'busco', None, 1.6), clear=True, cps=24, label='busca alumínio')   # voz real: começa 0,65 s antes e digita mais rápido
    c.click(BTN('Editar margem', within=DLG, exact=False), w=(7, 'abro'), label='Editar margem')
    c.waitfor(text='Mesma margem em vários materiais', timeout=6)
    c.hover(PD('Mesma margem em vários materiais'), 0.8, w=(7, 'Mesma', 1), label='Mesma margem em vários materiais')
    c.type(SEL('input[aria-label="Margem para todos"]'), '20', w=(7, 'vinte'), clear=True, label='margem para todos 20')
    c.hover(BTN('Aplicar em 3 material(is) exibido(s)', within=DLG), 1.0, w=(7, 'Aplicar'), label='Aplicar em 3 material(is) exibido(s) (zoom)')
    c.click(BTN('Aplicar em 3 material(is) exibido(s)', within=DLG), w=(7, 'esses'), label='Aplicar em 3 material(is) exibido(s)')
    c.confere_campos(['7,44', '10,68', '8,52'], 'os três alumínios com 20%')
    c.hover(PD('Alumínio latinha'), 0.8, w=(7, 'mudam'), label='os três alumínios recalculados')
    c.click(CHAVE, w=(8, 'desligar'), label='desliga a chave (só a configuração)')
    c.confere('dlg', ['Desligada'], 'resumo: Margem automática Desligada')
    c.hover(PD('Desligada'), 0.8, w=(8, 'configuração'), label='Margem automática: Desligada')
    sair_cancelando(c, (8, 'Cancelar', 1))
    c.fim()
    return c


def cap09():
    """Resumo e margem fora da regra (semente margem-fora: margem Por material gravada, Alumínio latinha com venda 7,80): Bronze -5 %, plástico PET
    zerado (Sem preço), Margem típica, Fora da margem, clique no selo; Cancelar."""
    c = Cap(9, setup_estoque())
    abre_editar_precos(c, (1, 'Editar'), 'abre Editar Preços (margem já ligada)')
    c.confere('dlg', ['Por material', 'Fora da margem'], 'margem ligada e Fora da margem no resumo')
    c.hover(CHAVE, 0.6, w=(1, 'cartão'), label='cartão Margem automática ligado')
    c.hover(ASIDE, 0.8, w=(1, 'resumo'), label='Resumo da tabela')
    c.hover(PD('Venda abaixo da compra'), 0.6, w=(2, 'Venda', 0), label='Resumo: Venda abaixo da compra')
    c.type(CAMPOS('Bronze', 1), '-5', w=(2, 'menos', 1), clear=True, label='Bronze margem -5')
    c.press('Tab', label='sai da célula')
    c.confere_campos(['29,00', '-5', '27,55'], 'Bronze 29,00, -5% e 27,55', escopo=LINHA('Bronze')['selector'])
    c.hover(PD('Venda abaixo da compra'), 1.2, w=(2, 'avisa'), label='Resumo: Venda abaixo da compra 1 (zoom)')
    c.type(CAMPOS('Plástico PET', 0), '0', w=(3, 'Zerando'), clear=True, label='Plástico PET compra 0')
    c.type(CAMPOS('Plástico PET', 2), '0', clear=True, label='Plástico PET venda 0')
    c.press('Tab', label='sai da célula')
    c.confere('dlg', ['Sem preço'], 'resumo: Sem preço')
    c.hover(PD('Sem preço'), 0.8, w=(3, 'Esses'), label='Resumo: Sem preço 1')
    c.click(SEL(f"{DLG} aside button[title='Filtrar a grade por este item']:has-text('Sem preço')"), w=(3, 'clicando'), label='clique em Sem preço: a lista mostra só ele')
    c.confere('dlg', ['Plástico PET'], 'lista só com o Plástico PET')
    c.click(SEL(f"{DLG} [role=group][aria-label='Filtros rápidos'] button:has-text('Todos')"), w=(4, 'Margem', 0), label='filtro Todos')
    c.hover(SEL(f"{DLG} aside div[title^='Metade']"), 1.0, w=(4, 'meio'), label='Margem típica (zoom)')
    c.hover(SEL(f"{DLG} aside button[title='Filtrar a grade por este item']:has-text('Fora da margem')"), 0.8, w=(5, 'Fora'), label='Resumo: Fora da margem 1')
    c.click(SEL(f"{DLG} aside button[title='Filtrar a grade por este item']:has-text('Fora da margem')"), w=(5, 'Esse'), label='clique em Fora da margem')
    c.confere('dlg', ['Alumínio latinha', 'fora da margem'], 'lista só com o Alumínio latinha fora da margem')
    c.hover(CAMPOS('Alumínio latinha', 2), 1.0, w=(6, 'sete', 0), label='Alumínio latinha: venda 7,80 (zoom)')
    selo = SEL(f"{DLG} tbody tr:has-text('Alumínio latinha') button:text-is('fora da margem')")
    c.hover(selo, 0.5, w=(6, 'selo'), label='selo fora da margem')
    c.click(selo, w=(6, 'sistema'), label='clique no selo: recalcula a venda pela compra')
    c.confere_campos(['6,20', '7,40'], 'Alumínio latinha volta a 6,20 e 7,40', escopo=LINHA('Alumínio latinha')['selector'])
    sair_cancelando(c, (6, 'cancelo'))
    c.fim()
    return c


def cap10():
    """A margem no cadastro do material (semente margem-material): Editar do radiador, linha Margem automática, calculadora (20 % > venda 25,20), compra 22
    > venda 26,40, Tirar a margem deste material (só mostrado), Cancelar."""
    c = Cap(10, setup_estoque(busca='radiador'))
    abre_acoes(c, 'Radiador de cobre', 'Editar', (1, 'Abro'), 'menu da linha do radiador', w_item=(1, 'Editar'))
    c.waitfor(text='Editar Material', timeout=10)
    c.ev(js_rola_ate('Valores e estoque', y=150, escopo=DLG), w=(1, 'Como', None, 0.6), label='desce até Valores e estoque')
    c.confere_campos(['21,00', '24,50'], 'P. Compra 21,00 e P. Venda 24,50')
    c.hover(SEL(f"{DLG} p:has-text('Margem automática de')"), 1.4, w=(1, 'avisa'), label='linha Margem automática de ...: a venda acompanha a compra (zoom)')
    CALC = SEL('button[aria-label="Calcular a venda pela margem"]')
    c.click(CALC, w=(2, 'calculadora', 0), label='calculadora ao lado do P. Venda')
    c.waitfor(text='Calcular venda pela margem', timeout=6)
    c.type(SEL(f"{POP} input"), '20', w=(2, 'Ponho'), clear=True, label='margem 20')
    c.confere('body', ['Venda R$ 25,20'], 'a conta: compra 21,00 > venda 25,20')
    c.hover(PD('Compra R$', within=POP) if False else SEL(f"{POP} p:has-text('Compra R$')"), 1.4, w=(2, 'conta'), label='a conta: Compra R$ 21,00 > Venda R$ 25,20 (zoom)')
    c.click(BTN('Aplicar', within=POP), w=(2, 'Aplicar'), label='Aplicar')
    c.waitfor(gone={'selector': POP}, timeout=6)
    c.confere_campos(['25,20'], 'P. Venda 25,20')
    c.type(CAMPO('purchase_price'), '22', w=(3, 'Mudo'), clear=True, label='P. Compra 22')
    c.press('Tab', label='sai do campo')
    c.confere_campos(['22', '26,40'], 'P. Compra 22 e P. Venda 26,40')
    c.hover(CAMPO('sale_price'), 1.2, w=(3, 'vinte', 1), label='P. Venda 26,40 (zoom)')
    c.click(CALC, w=(4, 'Na'), label='abre a calculadora de novo')
    c.waitfor(text='Tirar a margem deste material', timeout=6)
    c.hover(BTN('Tirar a margem deste material', within=POP), 1.0, w=(4, 'Tirar'), label='Tirar a margem deste material')
    c.press('Escape', w=(5, 'Uma', None, 0.2), label='fecha a calculadora')
    c.waitfor(gone={'selector': POP}, timeout=6)
    c.click(BTN('Cancelar', within=DLG), w=(5, 'Cancelar'), noScroll=True, label='Cancelar (nada é salvo)')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.fim()
    return c


def cap11():
    """Várias tabelas de preço: Nova Tabela vinculada +4 %, Cobre mel 44,20; Depósito Irmãos Siqueira > Editar > Tabela de Preços Padrão;
    (ilustração da ordem, L8) compra só para ver o preço: tabela no cobre mel, preço personalizado no bronze."""
    st = setup_estoque(aquecer=(('/clientes-fornecedores', 'Clientes e Fornecedores'), ('/caixa', 'Nova Compra')))
    c = Cap(11, st)
    c.hover(P('Tabelas de Preço'), 0.6, w=(1, 'tabela'), label='coluna Tabelas de Preço')
    c.hover(BTN('Principal'), 1.0, w=(1, 'principal.'), label='só a Principal')
    c.click(BTN('Nova Tabela'), w=(2, 'Nova'), label='Nova Tabela')
    c.waitfor(text='Nova Tabela de Preços', timeout=8)
    # o campo do nome tem autoFocus (PriceTableSettingsModal): digita sem ir até ele (o clique custava ~1 s e atrasava o "Marco Vincular")
    c.type({'placeholder': 'Ex: Atacado, Varejo, Premium...'}, 'Tabela Depósitos', w=(2, 'com'), clicar=False, cps=30, label='Nome da Tabela: Tabela Depósitos')
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
    # L6 e L7 (novas): Editar Preços > Tabela Depósitos na lista da esquerda > cadeado do fio de cobre; sem o cartão da margem (vinculada)
    c.ev(js_rola_topo(), w=(6, 'Dá', 0, 1.6), label='volta ao topo (a barra com o Editar Preços)')
    c.click(BTN('Editar Preços'), w=(6, 'Preços.', None, 1.5), label='Editar Preços')
    c.waitfor(text='Editar Tabelas de Preço', timeout=10)
    c.click(SEL(f"{DLG} aside[aria-label='Tabelas de preços disponíveis'] button:has-text('Tabela Depósitos')"), w=(6, 'Escolho'), label='Tabela Depósitos na lista da esquerda')
    c.waitfor(text='Tabela vinculada', timeout=8)
    c.hover(SEL(f"{DLG} thead th:has-text('Variação')"), 0.5, w=(6, 'Variação', 0), label='coluna Variação')
    c.hover(SEL(f"{DLG} tbody tr:has-text('Fio de cobre') button[title^='Variação padrão']"), 0.5, w=(6, 'cadeado'), label='cadeado fechado (Variação padrão)')
    c.click(SEL(f"{DLG} tbody tr:has-text('Fio de cobre') button[title^='Variação padrão']"), w=(6, 'Abrindo'), label='abre o cadeado do fio de cobre encapado')
    c.type(SEL(f"{DLG} tbody tr:has-text('Fio de cobre') td:nth-child(4) input"), '2', w=(6, 'porcentagem'), clear=True, label='variação própria do fio de cobre: 2')
    c.hover(SEL(f"{DLG} tbody tr:has-text('Fio de cobre')"), 0.4, w=(6, 'regra.'), label='só o fio de cobre mudou (zoom na linha)')
    c.hover(SEL(f"{DLG} aside[aria-label='Resumo e regras da tabela']"), 1.0, w=(7, 'Repara'), label='painel da direita: sem o cartão Margem automática')
    c.click(BTN('Cancelar', within=DLG), w=(7, 'Na'), noScroll=True, label='Cancelar (nada é salvo)')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    # L6: menu lateral recolhido (abre ao passar o mouse) > Clientes e Fornecedores > Fornecedores > o depósito (na lista, sem busca) > Editar
    c.hover(MENU('/clientes-fornecedores'), 0.6, w=(8, 'ligar', None, 1.35), noScroll=True, label='menu lateral (abre ao passar o mouse)')
    # L6: menu, aba, depósito e Editar em 5,5 s de fala; cada gesto na sua palavra, sem pausa no meio (prever de 11/11: 1,3 s de atraso)
    c.click(MENU('/clientes-fornecedores'), w=(8, 'Em', 0, 1.8), noScroll=True, label='Clientes e Fornecedores')
    c.rolar(0, ponto=(760, 420), duration=0.3, after=0, label='cursor sai do menu (ele recolhe)')
    c.waitfor(target=BTNX('Fornecedores'), timeout=12)
    c.click(BTNX('Fornecedores'), w=(8, 'Fornecedores,'), label='aba Fornecedores')
    # a aba trocou mesmo? (o depósito também é cliente: no ensaio de 11/11 a aba ficou em Clientes e o robô abriu o depósito-cliente)
    c.pause(0.3)
    c.click(BTNX('Fornecedores'), label='aba Fornecedores de novo (só se não trocou)', unless=BTN('Novo Fornecedor'))
    c.waitfor(target=BTN('Novo Fornecedor'), timeout=30)
    c.waitfor(target=P('Depósito Irmãos Siqueira'), timeout=8)
    c.click(P('Depósito Irmãos Siqueira'), w=(8, 'Depósito'), label='Depósito Irmãos Siqueira')
    c.waitfor(text='1 preço personalizado', timeout=10)
    c.click(BTN('Editar', within='main'), w=(8, 'clico'), label='Editar')
    c.waitfor(text='Editar Fornecedor', timeout=10)
    c.ev(js_rola_ate('Tabela de Preços Padrão', y=380, escopo=DLG), w=(9, 'Em', None, 0.6), label='desce até Tabela de Preços Padrão')
    c.click(SEL(f"{DLG} div.space-y-2:has(> label:has-text('Tabela de Preços Padrão')) button[role=combobox]"), w=(9, 'Padrão,'), label='Tabela de Preços Padrão (abre)')
    c.click(OPT('Tabela Depósitos'), w=(9, 'Depósitos'), label='Tabela Depósitos (zoom)')
    c.click(BTN('Salvar', within=DLG), w=(9, 'salvo.'), noScroll=True, label='Salvar')
    c.waitfor(text='Fornecedor atualizado!', timeout=10)
    # L8: ilustração da escada de prioridade; por baixo dela o robô vai ao Caixa sem cursor
    c.ev("(()=>{history.pushState({},'','/caixa');window.dispatchEvent(new PopStateEvent('popstate'));return location.pathname})()", w=(10, 'Uma'), label='vai ao Caixa (por baixo da ilustração)')
    c.waitfor(text='Nova Compra', timeout=15)
    c.click(SEL("main button:has-text('Nova Compra')"), w=(11, 'abro'), label='Nova Compra')
    c.waitfor(target=SEL('#supplier-desktop-top'), timeout=15)
    c.click(SEL('#supplier-desktop-top'), w=(11, 'Escolho', None, 2.6), label='Selecionar Fornecedor')  # a busca e o clique vêm em seguida
    c.type({'placeholder': 'Buscar por nome, apelido, CPF/CNPJ ou telefone...'}, 'Depósito', clicar=False, cps=30, label='busca Depósito')
    c.click(PD('Depósito Irmãos Siqueira'), w=(11, 'depósito,'), label='Depósito Irmãos Siqueira')
    c.confere('main', ['Tabela Depósitos'], 'Tabela de Preços passou para Tabela Depósitos')
    c.registra(SEL("main button[role=combobox]:has-text('Tabela Depósitos')"), w=(11, 'tabela'), label='Tabela de Preços: Tabela Depósitos (zoom, sem o mouse)')
    c.click({'placeholder': 'Escreva o nome ou código do material'}, w=(11, 'selecionada.'), label='campo do material')
    c.type({'placeholder': 'Escreva o nome ou código do material'}, 'cobre', w=(12, 'No', None, 0.6), clicar=False, cps=30, label='material: cobre')
    c.click(OPT('Cobre mel', exact=False), w=(12, 'mel,'), label='Cobre mel')
    c.confere('body', ['Preço da tabela aplicado para Cobre mel'], 'aviso Preço da tabela aplicado')
    c.registra(VALOR_KG, w=(12, 'quarenta'), label='Valor/kg 44,20 (zoom)')
    c.confere_campos(['44,2'], 'Valor/kg 44,20', escopo='main')
    # L11: campo, troca e Bronze não cabem entre "vinte." e "bronze,": o campo abre no "quatro" e o Bronze sai no "depósito" (o 30,50 e o
    # aviso aparecem no "personalizado")
    c.click({'placeholder': 'Escreva o nome ou código do material'}, w=(12, 'quatro', None, 0.0), label='campo do material de novo')
    c.type({'placeholder': 'Escreva o nome ou código do material'}, 'bronze', w=(13, 'Já', 0, 0.65), clicar=False, clear=True, cps=30, label='troca para bronze')
    c.click(OPT('Bronze', exact=False), w=(13, 'depósito'), label='Bronze')
    # o aviso vive 2 s: o cursor vai direto a ele, por coordenada (sem esperar a página), e fica em cima (o sonner pausa) até "aplicado."
    # noScroll SEMPRE em aviso: ele fica abaixo da faixa útil do robô (96..730 px) e, sem isso, o hover rola a página e tira o cursor
    # de cima do aviso, que some (era a causa das falhas do aviso no cap06, cap07 e cap10)
    ini = round(c.W(13, 'depósito') + 0.9, 2)
    c.rolar(0, ponto=(990, 748), duration=0.3, after=0, label='cursor no lugar do aviso (embaixo à direita)')
    c.hover({'text': 'Preço especial aplicado para Bronze'}, round(c.W(13, 'aplicado.') + 0.6 - ini - 0.55, 2), timeout=6, noScroll=True,
            label='aviso Preço especial aplicado (o mouse segura o aviso) (zoom: Valor/kg 30,50 com o aviso)')
    c.confere('body', ['Preço especial aplicado para Bronze'], 'aviso Preço especial aplicado para Bronze')
    c.confere_campos(['30,5'], 'Valor/kg 30,50', escopo='main')
    c.fim()
    return c


def cap12():
    """Duplicar, fixar e trocar a principal (menu "..." da tabela): Configurações (só mostra), Duplicar tabela, Excluir a cópia, Fixar, Remover minha tabela
    fixada, Definir como principal da empresa (só mostra e cancela). O mundo termina igual ao da entrada (semente apos-cap07)."""
    c = Cap(12, setup_estoque())
    TAB = lambda n: SEL(f"main button:has-text('{n}')")
    TRES = lambda n: SEL(f"main button:has-text('{n}') span:has(svg[class*='lucide-ellipsis'], svg[class*='lucide-more-horizontal'])")

    def menu(nome, w, label):
        c.hover(TAB(nome), 0.2, w=w, label=f'passa o mouse na tabela {nome}')
        return c.click(TRES(nome), label=label)

    c.hover(TAB('Tabela Depósitos'), 0.5, w=(1, 'menu'), label='Tabela Depósitos (o mouse faz os três pontinhos aparecerem)')
    c.click(TRES('Tabela Depósitos'), w=(1, 'pontinhos'), label='três pontinhos da Tabela Depósitos')
    c.waitfor(target=ITEM('Configurações'), timeout=6)
    c.hover(ITEM('Excluir'), 0.8, label='o menu inteiro: Configurações, Duplicar, Fixar, Definir como principal, Excluir')
    c.click(ITEM('Configurações'), w=(2, 'Configurações'), label='Configurações')
    c.waitfor(text='Editar Tabela de Preços', timeout=8)
    c.hover(PD('Editar Tabela de Preços'), 0.8, w=(2, 'variação'), label='Editar Tabela de Preços: nome e variação (zoom)')
    c.click(BTN('Cancelar', within=DLG), w=(2, 'muda', None, 1.4), label='Cancelar')
    c.waitfor(gone={'role': 'dialog'}, timeout=6)
    c.click(TRES('Tabela Depósitos'), w=(3, 'Duplicar', 0), label='três pontinhos')
    c.click(ITEM('Duplicar tabela'), w=(3, 'cria'), label='Duplicar tabela')
    c.waitfor(text='duplicada com sucesso', timeout=10)
    c.waitfor(target=TAB('Tabela Depósitos (cópia)'), timeout=8)
    c.hover(TAB('Tabela Depósitos (cópia)'), 1.4, w=(3, 'corrente'), label='Tabela Depósitos (cópia): sem a corrente (zoom na tabela nova)')
    c.click(TRES('Tabela Depósitos (cópia)'), w=(4, 'Como'), label='três pontinhos da cópia')
    c.click(ITEM('Excluir'), w=(4, 'excluo'), label='Excluir')
    c.waitfor(text='Excluir Tabela de Preços', timeout=8)
    c.hover({'text': 'Esta ação não pode ser desfeita', 'within': ALERTA}, 0.3, w=(4, 'volta'), label='Excluir Tabela de Preços: não pode ser desfeita (zoom)')
    c.click(BTN('Excluir', within=ALERTA), w=(4, 'principal'), label='Excluir')
    c.waitfor(text='Tabela de preço excluída!', timeout=8)
    c.waitfor(gone=TAB('Tabela Depósitos (cópia)'), timeout=8)
    c.click(TRES('Tabela Depósitos'), w=(5, 'Agora'), label='três pontinhos da Tabela Depósitos')
    c.click(ITEM('Fixar para meus pedidos e tickets'), w=(5, 'Fixar'), label='Fixar para meus pedidos e tickets')
    c.waitfor(text='Tabela fixada para seus novos pedidos e tickets', timeout=8)
    c.hover(SEL("main button:has-text('Tabela Depósitos') svg[aria-label='Fixada para meus pedidos e tickets']"), 1.2, w=(5, 'usuário'), label='o alfinete ao lado do nome (zoom)')
    c.click(TRES('Tabela Depósitos'), w=(7, 'Rafael'), label='três pontinhos da Tabela Depósitos')
    c.click(ITEM('Remover minha tabela fixada'), w=(7, 'removo'), label='Remover minha tabela fixada')
    c.waitfor(text='Tabela pessoal removida', timeout=8)
    c.click(TRES('Tabela Depósitos'), w=(8, 'Por'), label='três pontinhos da Tabela Depósitos')
    c.click(ITEM('Definir como principal da empresa'), w=(8, 'Definir'), label='Definir como principal da empresa')
    c.waitfor(target={'role': 'alertdialog'}, timeout=8)
    c.hover({'text': 'Os preços desta tabela virarão a base da empresa', 'within': ALERTA}, 1.4, w=(8, 'Os'), label='Definir “Tabela Depósitos” como principal? (zoom no texto)')
    c.click(BTN('Cancelar', within=ALERTA), w=(8, 'cancelo'), label='Cancelar')
    c.waitfor(gone={'role': 'alertdialog'}, timeout=6)
    c.fim()
    return c


def cap13():
    """Movimentar, transferir e zerar: saída de 2 kg do radiador, (ilustração L4) transferência de 8 kg para o Ferro misto, Zerar só mostrado."""
    c = Cap(13, setup_estoque())
    c.hover(BTN('Movimentar estoque'), 1.2, w=(1, 'ajuste'), label='Movimentar estoque')
    c.click(BTN('Movimentar estoque'), w=(2, 'Em', None, 0.9), label='Movimentar estoque')
    c.waitfor(text='Registre uma entrada ou saída manual', timeout=8)
    c.click(BTN('Saída', within=DLG), w=(2, 'escolho', None, 1.8), primeiro=True, label='Saída')
    c.type({'placeholder': 'Escreva o nome ou código do material'}, 'radiador', w=(2, 'radiador', None, 1.95), cps=40, label='Material: radiador')
    c.waitfor(target=OPT('Radiador de cobre', exact=False), timeout=8)
    c.waitfor(gone=PD('Ferro misto'), timeout=8)
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
    c.confere('body', ['Transferir quantidade de Radiador de cobre (Código: 70)', '118 Kg'], 'Transferir Estoque: código 70, 118 Kg')
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
    c.hover(PD('Ferrosos'), 0.6, w=(7, 'desmarca'), label='um grupo (dá para desmarcar por grupo ou material)')
    c.hover(PD('Para confirmar, digite'), 1.6, w=(8, 'confirmar,'), label='Para confirmar, digite Zerar todo o meu estoque (zoom)')
    c.hover(BTNX('Zerar selecionados'), 1.0, w=(8, 'volta.'), label='Zerar selecionados apagado')
    c.click(BTN('Cancelar', within=DLG), w=(8, 'cancelo.'), label='Cancelar')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)
    c.fim()
    return c


def cap14():
    """Exportar: o menu; Estoque (PDF) com as colunas, Exportar (aba nova: o PDF fica no actions.json); Tabela Depósitos > Tabela de
    Preços (PDF) > Exportar PDF > A4."""
    c = Cap(14, setup_estoque(extra=[{'do': 'eval', 'js': JS_PDF_GANCHO}]))
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


def cap15():
    """Excluir um material: (ilustração L1; no fim dela o Excluir abre sem cursor) aviso de 110 kg, Sim, Excluir; o aviso com Desfazer; Desfazer."""
    c = Cap(15, setup_estoque(busca='radiador'))
    c.ev(js_menu_item('Radiador de cobre', 'Excluir'), w=(1, 'continuam', None, 0.3), label='abre o Excluir do radiador (fim da ilustração, sem cursor)')
    c.waitfor(text='Confirmar Exclusão', timeout=8)
    c.confere('dlg', ['Radiador de cobre', 'Código: 70', 'Atenção: Este material possui 110 Kg em estoque.'], 'aviso 110 Kg em estoque')
    c.hover(PD('Atenção: Este material possui'), 2.4, w=(2, 'cento'), label='aviso: possui 110 Kg em estoque (zoom)')
    c.click(BTN('Sim, Excluir'), w=(3, 'Sim,'), label='Sim, Excluir')
    c.waitfor(text='excluído', timeout=10)
    # o aviso (5 s) sobe embaixo à direita e, logo depois da exclusão, a página fica ocupada uns segundos (o app recalcula o estoque):
    # o Playwright não achava o "Desfazer" a tempo (ensaios de 10 e 11/11). O cursor vai antes ao lugar do botão, por coordenada (sem
    # depender da página), e fica lá: com o mouse em cima o sonner segura o aviso até o clique na palavra "Clicando".
    c.rolar(0, ponto=(1190, 746), duration=0.35, after=0, label='cursor no lugar do Desfazer (o aviso sobe embaixo à direita)')
    # o cursor já está parado em cima do aviso (o sonner o segura): só o retângulo para o zoom, sem mexer o mouse (o hover custava ~1 s)
    c.registra({'text': 'excluído'}, label='aviso "Radiador de cobre" excluído com Desfazer (zoom)')
    c.click(TXT('Desfazer'), w=(4, 'Clicando'), timeout=12, noScroll=True, label='Desfazer')
    c.waitfor(text='restaurado!', timeout=10)
    c.waitfor(target=P('Radiador de cobre'), timeout=10)
    c.hover(CELULA('Radiador de cobre', 4), 1.4, w=(4, 'saldo'), label='o radiador volta com 110 Kg')
    c.confere('row:Radiador de cobre', ['70', 'Radiador de cobre', '110'], 'radiador de volta, 110 Kg')
    # F11 (decisão de 20/11): seleção em massa. Limpa a busca (sem cursor), marca dois materiais, mostra a barra, desmarca pelo X. Nada é aberto nem excluído.
    c.ev(js_valor('main input[placeholder="Buscar material por código ou nome..."]', ''), w=(5, 'Quando', None, 0.0), label='limpa a busca (sem cursor)')
    c.waitfor(target=P('Ferro misto'), timeout=10)
    CK = lambda nome: SEL(f"main button[role=checkbox][aria-label='Selecionar {nome}']")
    c.click(CK('Ferro pesado'), w=(5, 'caixinhas'), label='marca o ferro pesado')
    c.click(CK('Ferro misto'), w=(5, 'dois,'), label='marca o ferro misto')
    c.confere('body', ['2 selecionados', 'Transferir Estoque', 'Definir prefixo', 'Excluir'], 'barra: 2 selecionados, Transferir Estoque, Definir prefixo, Excluir')
    # 1.60.22 (gravação final de 21/11): a barra fica em y ~845 (abaixo da faixa do robô: noScroll, senão ele espera ~7 s) e, a 1600 px,
    # o "Excluir" e o X dela ficam cortados à direita, atrás do botão do Cato (MELHORIAS). Desmarca pelas próprias caixinhas.
    c.hover(TXT('Transferir Estoque'), 1.6, w=(5, 'Transferir'), noScroll=True, label='a barra de seleção (zoom)')
    c.hover(TXT('Definir prefixo'), 1.4, w=(6, 'Definir'), noScroll=True, label='Definir prefixo na barra')
    CKL = lambda nome: SEL(f"main tbody tr:has-text('{nome}') button[role=checkbox]")
    c.click(CKL('Ferro misto'), w=(6, 'Desmarco,'), label='desmarca o ferro misto')
    c.click(CKL('Ferro pesado'), label='desmarca o ferro pesado: a barra some')
    c.waitfor(gone={'text': 'Transferir Estoque'}, timeout=6)
    c.confere('main', ['Ferro pesado', 'Ferro misto'], 'lista inteira de volta, sem seleção')
    c.fim()
    return c


def cap16():
    """Recapitulando: passa pelo estado final (radiador 70 no grupo Radiadores, Tabela Depósitos +4 %); a edição monta os trechos dos
    capítulos por cima."""
    c = Cap(16, setup_estoque())
    c.type(BUSCA, 'radiador', w=(1, 'cadastrou'), cps=24, label='busca radiador')
    c.hover(CELULA('Radiador de cobre', 7), 1.0, w=(1, 'preços'), label='preços do radiador')
    c.hover(CELULA('Radiador de cobre', 2), 1.0, w=(1, 'código', 0), label='código 70')
    c.hover(CELULA('Radiador de cobre', 3), 1.2, w=(2, 'grupo'), label='grupo Radiadores')
    c.ev(js_valor('main input[placeholder="Buscar material por código ou nome..."]', ''), w=(3, 'Reajustou', None, 0.3), label='limpa a busca (sem cursor)')
    c.hover(BTN('Editar Preços'), 0.6, w=(3, 'Editar'), label='Editar Preços (a margem automática)')
    c.click(BTNX('Tabela Depósitos'), w=(4, 'Tabela', 0), label='Tabela Depósitos +4%')
    c.waitfor(text='Exibindo preços da tabela: Tabela Depósitos', timeout=8)
    c.hover(P('Exibindo preços da tabela: Tabela Depósitos'), 1.2, w=(4, 'Siqueira'), label='Exibindo preços da tabela: Tabela Depósitos')
    c.click(BTN('Principal'), w=(5, 'Ajustou'), label='volta à Principal')
    c.hover(BTN('Movimentar estoque'), 0.6, w=(5, 'transferiu'), label='Movimentar estoque')
    c.hover(BTNX('Exportar'), 0.6, w=(5, 'exportou'), label='Exportar')
    c.hover(P('Lista de Materiais'), 0.8, w=(5, 'excluir'), label='a lista')
    c.fim()
    return c


CAPS = {f'{n:02d}': globals()[f'cap{n:02d}'] for n in range(17)}
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
