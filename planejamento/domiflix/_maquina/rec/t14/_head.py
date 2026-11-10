#!/usr/bin/env python3
"""T14 · gera rec/t14/cap00..cap13.json (roteiros do robô) a partir da voz (t14/narracao/capNN.json).

Notas Fiscais (NFS-e e NF-e) no COMPUTADOR (janela 1280x800), logada como Camila Duarte (admin, Glacial Cold Brasil), na Dominex 1.38.24.
Relógio do mundo: 13/11/2026 15:10 nos capítulos 0 a 11 e 16:20 nos capítulos 12 e 13 (FAKE_NOW por capítulo, ver rodar.sh): a Receita só aceita
uma consulta de NF-e por CNPJ a cada 65 min, e a nota completa do cap12 chega na consulta seguinte à do cap11 (antes do T17, às 16:30).
Os `at` saem da palavra que anuncia cada passo (A(linha, palavra, folga)): `at` = início da palavra - folga.
VOZ: cada linha usa a voz processada quando as palavras dela batem com o texto atual (tts_textos.py); senão, uma ESTIMATIVA
(rec/t14/_voz/, ~2,7 palavras/s) até a voz nova chegar (caps 2, 3, 8 e 13 inteiros; emendas cap0 L4 e cap10 L3). O gerar.py avisa.
Rodar de qualquer pasta: `python3 -I rec/t14/gerar.py [NN ...]`. Depois: `node rec/record.mjs rec/t14/capNN.json --check`.

Cadeia de sementes: rec/t14/cadeia.json (semear.py: fim do T21 + `t14/inicio`) e, a cada capítulo, o último `t14/apos-capNN` do capítulo anterior que
mexeu no banco (SEMENTE abaixo). O `apos-capNN` sai do ensaio (`rec/t14/snap.mjs diff NN`, na mesma trava).

Particularidades (lições deste tutorial):
 - Dois botões "Enviar certificado" na tela do certificado: o do painel do alto só troca de aba; o envio é o do rodapé da seção (ENVIAR_CERT).
   A barra do rodapé tem `sticky`, mas NÃO gruda: a raiz da tela tem `overflow-x-hidden` (vira o contêiner de rolagem); o botão fica no fim
   da seção, e o robô rola até ele (nada de `noScroll`, que clicaria no rodapé do app por cima).
 - Depois do envio o app volta sozinho à aba "Empresa" com a rolagem embaixo: o painel do alto sai de vista (o robô sobe até ele).
 - A lista "Notas Fiscais" não recarrega depois de emitir/salvar pelo "Nova Nota" do cabeçalho (defeito do app): ir a "Relatório fiscal" e voltar.
 - Discriminação e nome do certificado já vêm preenchidos (nome do serviço / do arquivo): digitar com `clear`.
 - "Valor do serviço" é decimal pt-BR: digitar "450,00" (45000 viraria R$ 45.000,00).
 - Faixa de clique do robô (y 96 a 730): fora dela o robô tenta rolar até 6 vezes (~5 s de atraso). Botões do rodapé da janela da nota (y ~731) e a
   busca do cliente (a lista abre para CIMA, y ~72) levam `noScroll=True`; o seletor de código fiscal abre para BAIXO sem desviar da borda
   (`avoidCollisions=false`): a página sobe antes de abrir (cap05).
 - Busca de código de serviço é NUMÉRICA (compara só os dígitos): "14.01" casa 04.14.01, que vem antes na lista; digitar o código inteiro.
 - Depois do "Salvar dados fiscais" o CNPJ da empresa fica só com dígitos, e a pré-visualização da nota mostra "91520340000107".
 - Observador `OBS` guarda em `window.__avisos` todo aviso de erro do app, tela escura e faixa da trilha Domiflix; o passo final devolve a lista.
 - `confere*` LÊ a tela e compara com a fala (o `resumo.py` acusa DIFERENTE).
"""
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TUT = os.path.normpath(os.path.join(HERE, '..', '..'))
NARR = os.path.join(TUT, 't14', 'narracao')
VOZ_PROV = os.path.join(HERE, '_voz')
CAD = json.load(open(os.path.join(HERE, 'cadeia.json'), encoding='utf8'))
BASE = CAD['inicio']
CAMILA = 'd40f5787-1779-501f-900c-ddb2b90a36e5'
STORAGE = {f'dominex:portal-tickets-seen:{CAMILA}': '2031-01-01T00:00:00.000Z'}
ARQ_CERT = os.path.join(HERE, 'arquivos', 'certificado-ficticio.pfx')   # bytes aleatórios: não é certificado

sys.path.insert(0, NARR)
from tts_textos import CAPS  # noqa: E402  (texto atual de cada capítulo, grafia do TTS)

TROCAS = json.load(open(os.path.join(NARR, 'config_narracao.json'), encoding='utf8'))['trocas']

# Observador de avisos de erro na tela (aceite da fase 1): guarda em window.__avisos todo texto que apareça com "Não foi possível", "erro",
# "Tente novamente" ou "indisponível" (menos a dica fixa "... fica indisponível" da ficha do contrato); o passo final de cada capítulo devolve
# a lista (o resumo imprime) e ela tem de sair vazia.
OBS = ("(()=>{window.__avisos=[];const re=/N[ãa]o foi poss[ií]vel|Erro ao|Tente novamente|indispon[ií]vel/i;const chk=(t)=>{t=(t||'').trim();"
       "const m=t&&t.match(new RegExp('[^]{0,40}('+re.source+')[^]{0,40}','i'));"
       "if(m&&!/fica indispon/i.test(m[0])&&window.__avisos.length<10)window.__avisos.push(m[0].replace(/[\\n\\r\\t ]+/g,' '))};new MutationObserver(ms=>{for(const m of ms){"
       "m.addedNodes.forEach(n=>chk(n.textContent));if(m.type==='characterData')chk(m.target.textContent)}}).observe(document.body,"
       "{childList:true,subtree:true,characterData:true});chk(document.body.innerText);"
       "setInterval(()=>{const f=document.querySelector('section[aria-label^=\"Lembrete da trilha\"]');"
       "const e=[...document.querySelectorAll('div.fixed')].some(x=>getComputedStyle(x).backgroundColor==='rgb(17, 17, 17)');"
       "if((f||e)&&window.__avisos.length<10&&!window.__avisos.includes('TRILHA DOMIFLIX'))window.__avisos.push('TRILHA DOMIFLIX')},300);return 1})()")

NOMES = ['Abertura', 'A nota do serviço', 'Os dados da empresa', 'O certificado digital', 'A tributação', 'Os serviços com código', 'Pessoas e serviço',
         'Valores e emissão', 'Nota autorizada', 'Rascunho e cancelamento', 'Nota automática do contrato', 'As notas dos fornecedores',
         'Ciência e conta a pagar', 'Recapitulando']
# estado de partida de cada capítulo: o último apos-capNN (de capítulo anterior) que mexeu no banco. Os caps 1, 6, 8 e 13 só leem
# (o 6 termina com a janela aberta: o setup do 7 refaz Pessoas e Serviço sobre apos-cap05).
SEMENTE = {0: None, 1: None, 2: None, 3: 'apos-cap02', 4: 'apos-cap03', 5: 'apos-cap04', 6: 'apos-cap05', 7: 'apos-cap05', 8: 'apos-cap07',
           9: 'apos-cap07', 10: 'apos-cap09', 11: 'apos-cap10', 12: 'apos-cap11', 13: 'apos-cap12'}
GRAVA_SEMENTE = (2, 3, 4, 5, 7, 9, 10, 11, 12)
FAKE_NOW = {n: (CAD.get('fake_now_cap12') if n >= 12 else CAD['fake_now']) for n in range(14)}


def norm(s):
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode().lower()
    return ''.join(ch for ch in s if ch.isalnum() or ch in '?')


def tokens(texto):
    """[(legenda, fala, linha)] como o proc.py: trocas de pronúncia viram a grafia da legenda, sem as tags [pause]"""
    out = []
    mapa = dict(TROCAS)
    rx = re.compile('|'.join(re.escape(f) for f, _ in sorted(TROCAS, key=lambda p: -len(p[0]))))
    for li, linha in enumerate(texto.split('\n')):
        linha = re.sub(r'\[[a-z ]+\]', ' ', linha)
        linha = rx.sub(lambda m: '\u0000' + m.group(0).replace(' ', '\u0001') + '|' + mapa[m.group(0)].replace(' ', '\u0001') + '\u0000', linha)
        for w in linha.split():
            if '\u0000' in w:
                pre, fala, leg, pos = re.match(r'^(.*?)\u0000(.*?)\|(.*?)\u0000(.*)$', w).groups()
                fs, ls = fala.split('\u0001'), leg.split('\u0001')
                for k, (f, l) in enumerate(zip(fs, ls)):
                    out.append(((pre if k == 0 else '') + l + (pos if k == len(fs) - 1 else ''), (pre if k == 0 else '') + f + (pos if k == len(fs) - 1 else ''), li))
            else:
                out.append((w, w, li))
    return out


def carregar_voz(n):
    """voz do capítulo: por linha, a processada (t14/narracao/capNN.json) quando as palavras batem com o texto atual; senão estimada.
    Devolve (words, linhas, dur, linhas_estimadas)."""
    real = json.load(open(os.path.join(NARR, f'cap{n:02d}.json'), encoding='utf8'))
    texto = CAPS[n]
    toks = tokens(texto)
    nlin = len(texto.split('\n'))
    porlinha = [[t for t in toks if t[2] == i] for i in range(nlin)]
    reais = [[w for w in real['words'] if w['linha'] == i] for i in range(len(real['linhas']))]
    words, linhas, estimadas = [], [], []
    t = 0.0
    for i in range(nlin):
        alvo = ' '.join(norm(f) for _, f, _ in porlinha[i])
        rw = reais[i] if i < len(reais) else []
        if rw and ' '.join(norm(w.get('fala', w['w'])) for w in rw) == alvo:
            s0 = real['linhas'][i]['s']
            gap = (real['linhas'][i]['s'] - real['linhas'][i - 1]['e']) if i > 0 else real['linhas'][0]['s']
            ini = t + (gap if i > 0 else s0)
            for w in rw:
                words.append({**w, 'linha': i, 's': round(ini + w['s'] - s0, 3), 'e': round(ini + w['e'] - s0, 3)})
            fim = ini + real['linhas'][i]['e'] - s0
        else:
            estimadas.append(i + 1)
            ini = t + (0.35 if i > 0 else 0.0)
            x = ini
            for leg, fala, _ in porlinha[i]:
                d = 0.08 + 0.062 * len(norm(fala))
                words.append({'w': leg, 'fala': fala, 'linha': i, 's': round(x, 3), 'e': round(x + d, 3), 'estimada': True})
                x += d + (0.32 if fala[-1:] in '.!?:' else 0.16 if fala[-1:] == ',' else 0.05)
            fim = x
            if '[pause]' in texto.split('\n')[i]:
                fim += 0.8
        linhas.append({'i': i, 'texto': ' '.join(w['w'] for w in words if w['linha'] == i), 's': round(ini, 3), 'e': round(fim, 3)})
        t = fim
    dur = round(t + (real['dur'] - real['linhas'][-1]['e'] if not estimadas or estimadas[-1] != nlin else 0.4), 2)
    prov = os.path.join(VOZ_PROV, f'cap{n:02d}.json')   # o resumo.py lê esta voz quando existe (senão a processada)
    if estimadas:
        os.makedirs(VOZ_PROV, exist_ok=True)
        json.dump({'cap': n, 'estimada': estimadas, 'dur': dur, 'words': words, 'linhas': linhas}, open(prov, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    elif os.path.exists(prov):
        os.remove(prov)   # a voz nova chegou: a estimativa antiga sai
    return words, linhas, dur, estimadas


class Cap:
    def __init__(s, n, pace=0.5, cps=9, start=(760, 420), prewarm=None, setup=None, user=None, storage=None, noscroll=False):
        s.n = n
        s.words, s.linhas, s.dur, s.estimadas = carregar_voz(n)
        s.steps = []
        s.pace, s.cps, s.start = pace, cps, start
        s.prewarm = prewarm or ['/dashboard', '/notas-fiscais']
        s.storage = storage if storage is not None else STORAGE
        s.noscroll = noscroll
        s.setup = list(setup or []) + [{'do': 'eval', 'js': OBS}]
        s.anchors = []
        s.pending = []
        s.user = user

    # ---- tempo
    def L(s, i):
        return round(s.linhas[i - 1]['s'], 2)

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
            if d.get('do') == 'type':
                for mt, mi in list(s.pending):
                    if d['at'] < mt <= d['at'] + 2.6:
                        s.steps.append({'do': 'mark', 'name': f'L{mi}', 'at': round(d['at'], 2)})
                        s.pending.remove((mt, mi))
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

    def hover(s, target, seconds=0.9, at=None, label=None, **kw):
        kw.setdefault('optional', True)
        kw.setdefault('timeout', 3)
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

    def upload(s, target, arquivo, at=None, label=None, **kw):
        return s._p({'do': 'upload', 'target': target, 'file': arquivo}, at, label, kw)

    def rolar(s, by, at=None, label=None, ponto=(760, 420), duration=0.5, after=100):
        return s._p({'do': 'scroll', 'point': {'x': ponto[0], 'y': ponto[1]}, 'by': by, 'duration': duration, 'after': after}, at, label, {})

    def confere(s, escopo, esperados, label):
        """`eval` que LÊ a tela e compara com o que a fala diz: "OK: ..." ou "DIFERENTE: ...". Escopo 'dlg' (a última janela), 'main', 'body',
        'row:<texto>' (a linha da lista com esse texto) ou um seletor CSS. Tenta por ~6,5 s."""
        sel = {'dlg': "[role=dialog]", 'main': 'main', 'body': 'body'}.get(escopo, escopo)
        linha = escopo[4:] if escopo.startswith('row:') else None
        if linha is not None:
            sel = 'main tbody tr'
        esp = [esperados] if isinstance(esperados, str) else list(esperados)
        js = ("(async()=>{const norm=t=>t.replace(/[\\s\\u00a0]+/g,' ').toLowerCase();const esp=%s;let out='';"
              "for(let i=0;i<22;i++){const els=[...document.querySelectorAll(%s)].filter(e=>!%s||e.innerText.includes(%s));const el=%s?els[els.length-1]:els[0];"
              "if(!el){out='DIFERENTE: sem elemento';}else{const t=norm(el.innerText);const falta=esp.filter(e=>!t.includes(norm(e)));"
              "if(!falta.length)return 'OK: '+esp.join(' | ');out='DIFERENTE: faltou '+JSON.stringify(falta)+' em: '+t.slice(0,260);}"
              "await new Promise(r=>setTimeout(r,300));}return out})()") % (json.dumps(esp, ensure_ascii=False), json.dumps(sel), 'true' if linha is not None else 'false',
                                                                           json.dumps(linha or ''), 'true' if escopo == 'dlg' else 'false')
        return s.add({'do': 'eval', 'js': js, 'label': 'confere ' + label})

    def confere_campos(s, esperados, label, escopo='[role=dialog]'):
        """lê o VALOR dos campos (input/textarea) do escopo e compara com o que a fala diz"""
        esp = [esperados] if isinstance(esperados, str) else list(esperados)
        js = ("(async()=>{const esp=%s;let out='';for(let i=0;i<12;i++){const v=[...document.querySelectorAll(%s+' input, '+%s+' textarea')].map(e=>e.value).join(' | ');"
              "const falta=esp.filter(e=>!v.includes(e));if(!falta.length)return 'OK: '+esp.join(' | ');out='DIFERENTE: faltou '+JSON.stringify(falta)+' em: '+v.slice(0,260);"
              "await new Promise(r=>setTimeout(r,300));}return out})()") % (json.dumps(esp, ensure_ascii=False), json.dumps(escopo), json.dumps(escopo))
        return s.add({'do': 'eval', 'js': js, 'label': 'confere ' + label})

    def confere_ausente(s, escopo, texto, label, espera=1.8):
        """LÊ a tela depois de `espera` s (o robô fica parado esse tempo: use pouco quando a tela já assentou) e acusa se o texto apareceu"""
        sel = {'dlg': '[role=dialog]', 'main': 'main', 'body': 'body'}.get(escopo, escopo)
        js = ("(async()=>{await new Promise(r=>setTimeout(r,%d));" % int(espera * 1000) + "const el=document.querySelector(%s);const t=(el?el.innerText:'').replace(/[\\s\\u00a0]+/g,' ').toLowerCase();"
              "return t.includes(%s)?'DIFERENTE: apareceu '+%s:'OK: ausente '+%s})()") % (json.dumps(sel), json.dumps(texto.lower()), json.dumps(texto), json.dumps(texto))
        return s.add({'do': 'eval', 'js': js, 'label': 'confere ' + label})

    def abrir_menu(s, linha, item, at=None, label=None):
        """"⋮" da linha: o 1º clique logo depois de carregar a lista pode não abrir o menu; 2º clique só se o item esperado ainda não apareceu."""
        s.click(ACOES(linha), at=at, label=label or f'menu ⋮ da linha de {linha}')
        s.pause(0.6)
        return s.click(ACOES(linha), label=f'menu ⋮ de {linha} de novo (só se não abriu)', unless=ITEM(item))

    def pause(s, seconds):
        return s.add({'do': 'pause', 'seconds': seconds})

    def waitfor(s, **kw):
        return s.add({'do': 'waitFor', **kw})

    def ev(s, js, at=None, label=None, **kw):
        return s._p({'do': 'eval', 'js': js}, at, label, kw)

    def clock(s, forward, label=None):
        return s.add({'do': 'clock', 'forward': forward, 'label': label or f'relógio do navegador +{forward}'})

    def clicar_fixo(s, alvo, ponto, js, at, label):
        """Botão FIXO fora da faixa y 96..730: leva o cursor com `scroll by 0 point`, registra o retângulo do `alvo` e clica por `eval`."""
        s._p({'do': 'scroll', 'point': {'x': ponto[0], 'y': ponto[1]}, 'by': 0, 'duration': 0.3, 'after': 0}, round(max(0.0, at - 0.9), 2), label + ' (cursor)', {})
        s.add({'do': 'type', 'target': alvo, 'text': '', 'noClick': True, 'label': label, 'optional': True, 'timeout': 4})
        return s._p({'do': 'eval', 'js': js}, round(at, 2), label + ' (clique)', {})

    def fim(s):
        s.flush(1e9)
        s.steps.append({'do': 'eval', 'js': 'JSON.stringify(window.__avisos || "sem observador")', 'label': 'avisos de erro na tela'})
        s.steps.append({'do': 'mark', 'name': 'FIM', 'at': round(s.dur, 2)})

    def out(s):
        sem = SEMENTE[s.n]
        d = {
            'name': f't14-cap{s.n:02d}',
            'title': f'T14 · Cap. {s.n} · {NOMES[s.n]} (narração {str(round(s.dur, 1)).replace(".", ",")} s{" ESTIMADA nas linhas " + ",".join(map(str, s.estimadas)) if s.estimadas else ""}; '
                     f'marcas L1..L{len(s.linhas)} = início de cada linha do roteiro; FAKE_NOW {FAKE_NOW[s.n]})',
            'seed': f't14-cap{s.n:02d}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5,
            'start': {'x': s.start[0], 'y': s.start[1]},
            'seedExtra': list(BASE) + ([f't14/{sem}'] if sem else []),
            'prewarm': s.prewarm, 'setup': s.setup, 'steps': s.steps,
            'storage': dict(s.storage),
        }
        if s.user:
            d['user'] = s.user
        return d


# ---------------------------------------------------------------- alvos
BTN = lambda n, **kw: {'role': 'button', 'name': n, 'exact': True, **kw}
BTNX = lambda n, **kw: {'role': 'button', 'name': n, **kw}
LINK = lambda n, **kw: {'role': 'link', 'name': n, 'exact': True, **kw}
TAB = lambda n, **kw: {'role': 'tab', 'name': n, 'exact': True, **kw}
TXT = lambda t, **kw: {'text': t, 'exact': True, **kw}
P = lambda t, **kw: {'text': t, 'within': 'main', **kw}
P_ = lambda t, **kw: {'text': t, **kw}
SEL = lambda s, **kw: {'selector': s, **kw}
DLG = '[role=dialog]'
PD = lambda t, **kw: {'text': t, 'within': DLG, **kw}
OPT = lambda n, **kw: {'role': 'option', 'name': n, **kw}
ITEM = lambda n, **kw: {'role': 'menuitem', 'name': n, **kw}
ACOES = lambda linha: {'selector': f"main tbody tr:has-text('{linha}') button[aria-label='Ações']"}
AGUARDA = {'do': 'waitFor', 'idle': True}
SW = lambda n, **kw: {'role': 'switch', 'name': n, 'exact': True, **kw}
COMBO = lambda txt, esc=DLG: {'selector': f'{esc} button[role=combobox]', 'hasText': txt}
CAMPO = lambda rotulo, esc='main': {'selector': f"{esc} label:has-text('{rotulo}') + input"}          # campo logo depois do rótulo
FIXO = lambda txt: {'selector': f"main div.sticky button:has-text('{txt}')"}                       # botão da barra do rodapé da seção (não gruda: ver acima)
ENVIAR_CERT = FIXO('Enviar certificado')

# ---------------------------------------------------------------- trechos comuns (não filmados, no `setup`)
SETUP_DASH = [{'do': 'goto', 'url': '/dashboard'}, {'do': 'waitFor', 'text': 'Olá, Camila!', 'timeout': 25}, AGUARDA]
FECHAR_EVAL = r"""(() => { const d = document.querySelector('[role=dialog]'); if (!d) return 'ja fechada'; const b = [...d.querySelectorAll('button')].find((x) => [x.textContent, x.getAttribute('aria-label'), x.title].some((v) => /^\s*fechar\s*$/i.test(v || ''))); if (!b) return 'sem botao Fechar'; b.click(); return 'fechada pelo botao'; })()"""


def setup_notas(extra=()):
    return SETUP_DASH + [{'do': 'goto', 'url': '/notas-fiscais'}, {'do': 'waitFor', 'text': 'Emita e acompanhe suas NFS-e.', 'timeout': 25}, AGUARDA] + list(extra)


def setup_config(aba=None, extra=()):
    url = '/notas-fiscais/configuracoes' + (f'?tab={aba}' if aba else '')
    return SETUP_DASH + [{'do': 'goto', 'url': '/notas-fiscais'}, {'do': 'waitFor', 'text': 'Emita e acompanhe suas NFS-e.', 'timeout': 25}, AGUARDA,
                         {'do': 'goto', 'url': url}, {'do': 'waitFor', 'text': 'Dados da empresa, certificado digital e tributação', 'timeout': 25}, AGUARDA] + list(extra)


def fechar_janela(c, at, espera=0.4):
    c.press('Escape', at=at, label='fecha a janela')
    c.add({'do': 'wait', 'seconds': espera})
    c.ev(FECHAR_EVAL, label='Fechar (se o Esc não fechou)')
    c.waitfor(gone={'role': 'dialog'}, timeout=8)


# Contêiner que rola: na 1.38.24 o 1º <main> do documento é o SidebarInset (overflow hidden: NÃO rola); quem rola é o <main> de dentro ou, em
# painéis com rolagem própria (aba Serviços), outro ancestral. Achado no ensaio de 05/11: o js antigo (document.querySelector('main').scrollTo)
# não mexia em nada, e era o robô que rolava com a roda ao procurar o alvo seguinte.
ACHA_ROLAGEM = ("const rolagem=(el)=>{let c=el&&el.parentElement;while(c&&c!==document.body){const s=getComputedStyle(c);"
                "if(/(auto|scroll)/.test(s.overflowY)&&c.scrollHeight>c.clientHeight+4)return c;c=c.parentElement;}"
                "return [...document.querySelectorAll('main')].find(e=>/(auto|scroll)/.test(getComputedStyle(e).overflowY)&&e.scrollHeight>e.clientHeight+4)||null};")
SUAVE = ("await new Promise(res=>{const f=t=>{const p=Math.min(1,(t-t0)/DUR),e=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;c.scrollTo({top:DESTINO,behavior:'instant'});"
         "p<1?requestAnimationFrame(f):res()};requestAnimationFrame(f)});")


def js_main_ate(texto, y=250, dur_ms=1000, prefixo=False):
    """rolagem suave do contêiner que rola o alvo até a folha do DOM cujo texto é `texto` ficar em y px CSS; o cursor não se mexe.
    Devolve o topo final do alvo (px CSS), 'ok' (já estava lá), 'SEM ALVO' ou 'SEM ROLAGEM'."""
    alvo = json.dumps(texto)
    busca = (f"[...document.querySelectorAll('main *')].filter(e=>e.textContent.trim().startsWith({alvo})).sort((a,b)=>a.textContent.length-b.textContent.length)[0]"
             if prefixo else f"[...document.querySelectorAll('main *')].find(e=>e.children.length===0&&e.textContent.trim()==={alvo})")
    return ("(async()=>{" + ACHA_ROLAGEM + "const el=" + busca + ";if(!el)return 'SEM ALVO';const c=rolagem(el);if(!c)return 'SEM ROLAGEM';"
            f"const dy=Math.round(el.getBoundingClientRect().top-{int(y)});if(Math.abs(dy)<3)return 'ok';const y0=c.scrollTop,t0=performance.now();"
            + SUAVE.replace('DUR', str(int(dur_ms))).replace('DESTINO', 'y0+dy*e') +
            "return Math.round(el.getBoundingClientRect().top)})()")


def rola_ate(c, texto, at, label, y=250, dur_ms=1000, prefixo=False):
    return c.ev(js_main_ate(texto, y, dur_ms, prefixo), at=at, label=label)


def rola_topo(c, at, label, dur_ms=700):
    js = ("(async()=>{" + ACHA_ROLAGEM + "const c=rolagem(null);if(!c)return 'SEM ROLAGEM';const y0=c.scrollTop,t0=performance.now();if(y0<3)return 'ok';"
          + SUAVE.replace('DUR', str(int(dur_ms))).replace('DESTINO', 'y0*(1-e)') + "return 'topo:'+Math.round(c.scrollTop)})()")
    return c.ev(js, at=at, label=label)


# semente aplicada NO MEIO do capítulo (o "corte" do cap12): mesmo molde do T7/T0 v2 (fetch ao /__dev/seed pela URL do build; o robô desvia para FAKE_URL)
BAKED = 'http://127.0.0.1:54321'


def js_semente(arquivo):
    return (f"(async()=>{{const r=await fetch({json.dumps(BAKED + '/__dev/seed')},{{method:'POST',headers:{{'content-type':'application/json'}},"
            f"body:JSON.stringify({{files:[{json.dumps(arquivo)}]}})}});return r.status}})()")

