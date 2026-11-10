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

# ---------------------------------------------------------------- alvos próprios do T14 (Notas Fiscais)
POP = '[data-radix-popper-content-wrapper]'
COMBO_ROTULO = lambda rotulo, esc='main': {'selector': f"{esc} div:has(> label:has-text('{rotulo}')) button[role=combobox]"}   # Select do Radix pelo rótulo
LISTA_TIPO = lambda nome: {'text': nome, 'exact': True, 'within': 'main [role=list]'}           # tipo de serviço na lista da aba Serviços
TAXA = lambda n=0, esc='': {'selector': f'{esc} button[role=combobox]'.strip(), 'hasText': 'Selecione o código...', 'nth': n}    # seletor de código fiscal vazio
BUSCA_TAXA = {'placeholder': 'Buscar por código ou descrição...'}
OPC_TAXA = lambda codigo: {'text': codigo, 'exact': True, 'within': POP}
SEL_FISCAL = 'main'   # escopo das conferências da aba Fiscal do tipo de serviço
MENU_LINHA = lambda texto: {'selector': f"main tbody tr:has-text('{texto}') button[aria-haspopup=menu]"}   # "⋯" da linha (HoverDropdownMenu: abre ao passar o mouse)
MENU_CARTAO = {'selector': "main div:has(> div p:has-text('Cobre Sul Suprimentos Ltda')) > button[aria-haspopup=menu]"}   # "⋮" do cartão da nota recebida (DropdownMenu: abre no clique)
NBS_CONTRATO = {'selector': "main div:has(> label:has-text('Código NBS')) > button[role=combobox]"}   # no contrato há DOIS seletores vazios (serviço e NBS)
BUSCA_TAXA_CONTRATO = {'placeholder': 'Buscar código...'}                                     # a busca do contrato tem outro texto de exemplo
SALVO = {'text': 'Salvo', 'exact': True, 'within': 'main'}
VALOR_SERVICO = {'selector': f'{DLG} input[inputmode=decimal]', 'nth': 0}
CONTRATO_HOTEL = 'PMOC - Hotel Mirante do Mar'
CONTRATO_ID = '34306a37-c1a7-58a1-b713-244525163500'


def marcar_alvo(c, target, at, label):
    """registra o retângulo do alvo para a câmera SEM mexer o mouse (passo `type` sem clique e sem texto): para o selo da cota,
    cuja dica mostra o preço do próximo nível (regra: nada de preço de plano)"""
    return c._p({'do': 'type', 'target': target, 'text': '', 'noClick': True, 'optional': True, 'timeout': 4}, at, label, {})


def abrir_menu_hover(c, texto, item, at=None, label=None):
    """menu da linha da lista de notas: passar o mouse abre (o clique no gatilho FECHARIA o menu aberto pelo hover)"""
    c.hover(MENU_LINHA(texto), 0.5, at=at, label=label or f'menu ⋯ da linha {texto}', optional=False, timeout=8)
    c.hover(MENU_LINHA(texto), 0.5, label=f'menu ⋯ de {texto} de novo (só se não abriu)', unless=ITEM(item))
    return c.waitfor(target=ITEM(item), timeout=6)


def js_dlg_ate(texto):
    """rola a janela aberta até o texto ficar no meio (o cursor não se mexe)"""
    return ("(async()=>{const d=document.querySelector('[role=dialog]');if(!d)return 'sem janela';const el=[...d.querySelectorAll('*')]"
            ".filter(e=>e.textContent.trim().startsWith(%s)).sort((a,b)=>a.textContent.length-b.textContent.length)[0];if(!el)return 'SEM ALVO';"
            "el.scrollIntoView({behavior:'smooth',block:'center'});await new Promise(r=>setTimeout(r,700));return 'ok'})()") % json.dumps(texto)


def confere_desligado(c, nome, label):
    js = ("(()=>{const b=[...document.querySelectorAll('main button')].find(x=>x.textContent.trim()===%s);"
          "if(!b)return 'DIFERENTE: sem o botão';return b.disabled?'OK: desligado':'DIFERENTE: ligado'})()") % json.dumps(nome)
    return c.add({'do': 'eval', 'js': js, 'label': 'confere ' + label})


def confere_marcado(c, seletor, label):
    js = "(()=>{const e=document.querySelector(%s);if(!e)return 'DIFERENTE: sem a caixa';return e.getAttribute('data-state')==='checked'?'OK: marcada':'DIFERENTE: '+e.getAttribute('data-state')})()" % json.dumps(seletor)
    return c.add({'do': 'eval', 'js': js, 'label': 'confere ' + label})


def confere_ordem(c, de_cima, de_baixo, label):
    """LÊ a tela: o texto `de_cima` aparece acima do `de_baixo` (registro de uso, do mais recente para o mais antigo)"""
    js = ("(()=>{const f=t=>[...document.querySelectorAll('main *')].find(e=>e.children.length===0&&e.textContent.trim()===t);const a=f(%s),b=f(%s);"
          "if(!a||!b)return 'DIFERENTE: faltou '+(!a?%s:%s);return a.getBoundingClientRect().top<b.getBoundingClientRect().top?'OK: acima':'DIFERENTE: abaixo'})()") % (
        json.dumps(de_cima), json.dumps(de_baixo), json.dumps(de_cima), json.dumps(de_baixo))
    return c.add({'do': 'eval', 'js': js, 'label': 'confere ' + label})


def js_aba_visivel(nome):
    """traz a aba para o meio da faixa de abas (rolagem horizontal da faixa, sem mexer na página): na ficha do contrato a aba Financeiro fica
    cortada na borda direita, e o ponto do clique (sorteado dentro do retângulo da aba) podia cair fora da parte visível (cap13, 06/11)"""
    return ("(async()=>{const el=[...document.querySelectorAll('[role=tab]')].find(e=>e.textContent.trim()===%s);if(!el)return 'SEM ABA';"
            "el.scrollIntoView({behavior:'smooth',inline:'center',block:'nearest'});await new Promise(r=>setTimeout(r,450));"
            "return Math.round(el.getBoundingClientRect().right)})()") % json.dumps(nome)


def cap_novo(n, **kw):
    kw.setdefault('prewarm', ['/dashboard', '/notas-fiscais', '/notas-fiscais/configuracoes'])
    return Cap(n, pace=0.5, **kw)


# setup do cap07: reabre "Nova NFS-e" com Pessoas e Serviço do cap06 (fora do vídeo)
REABRE_NOTA = [
    {'do': 'click', 'target': BTN('Nova Nota')}, {'do': 'waitFor', 'text': 'Data de competência', 'timeout': 15},
    {'do': 'click', 'target': COMBO('Selecione o cliente')}, {'do': 'type', 'target': {'placeholder': 'Buscar cliente...'}, 'text': 'Sabor', 'noScroll': True},
    {'do': 'click', 'target': OPT('Restaurante Sabor da Serra')}, {'do': 'pause', 'seconds': 0.4},
    {'do': 'click', 'target': BTN('Avançar'), 'noScroll': True}, {'do': 'waitFor', 'text': 'Escolha um serviço cadastrado', 'timeout': 10},
    {'do': 'click', 'target': COMBO('Escolha um serviço cadastrado')}, {'do': 'click', 'target': OPT('Higienização de Split')}, {'do': 'pause', 'seconds': 0.6},
    {'do': 'type', 'target': SEL(f'{DLG} textarea'), 'text': 'Limpeza e higienização de 2 splits da cozinha', 'clear': True, 'cps': 40},
    {'do': 'pause', 'seconds': 0.5},
]


# ================================================================ capítulos
def cap00():
    """Abertura: Dashboard, menu lateral > Notas Fiscais, estado guiado "Configure seus dados fiscais"."""
    c = cap_novo(0, setup=SETUP_DASH)
    c.mark(1)
    c.hover(LINK('Orçamentos'), 0.2, at=0.4, label='o cursor desce pelo menu lateral')
    c.click(LINK('Notas Fiscais'), at=c.A(1, 'emitir', 0.4), label='Notas Fiscais (menu lateral)')
    c.waitfor(text='Configure seus dados fiscais para começar a emitir notas.', timeout=20)
    c.confere('main', ['Notas Fiscais', 'Emita e acompanhe suas NFS-e.', 'Configurações fiscais', 'Nova Nota', 'Configure seus dados fiscais'], 'tela Notas Fiscais no estado guiado')
    c.hover(P('Emita e acompanhe suas NFS-e.'), 1.0, at=c.A(1, 'acompanhar', 0.9), label='Emita e acompanhe suas NFS-e.')
    c.mark(2)
    c.hover(P('Configure seus dados fiscais para começar a emitir notas.'), 1.4, at=c.A(2, 'configuração', 0.9), label='estado guiado Configure seus dados fiscais')
    c.hover(BTN('Nova Nota'), 0.9, at=c.A(2, 'cliques,', 0.9), label='Nova Nota')
    c.mark(3)
    c.hover(LINK('Notas Fiscais'), 1.4, at=c.A(3, 'item', 0.9), label='item Notas Fiscais do menu (módulo Emissão de Notas Fiscais)')
    c.mark(4)
    c.hover(TAB('Notas Fiscais'), 0.8, at=c.A(4, 'Vamos', 0.9), label='abas das notas')
    c.fim()
    return c


def cap01():
    """A nota do serviço: ilustração (L1, L2) e, de volta à tela, as abas e o selo da cota (sem mouse no selo)."""
    c = cap_novo(1, setup=setup_notas())
    c.mark(1)
    c.mark(2)
    c.mark(3)
    c.hover(TAB('Notas Fiscais'), 0.6, at=c.A(3, 'emitidas,', 0.9), label='aba Notas Fiscais')
    c.hover(TAB('Relatório fiscal'), 0.6, at=c.A(3, 'relatório', 0.9), label='aba Relatório fiscal')
    c.hover(TAB('Emissões automáticas'), 0.6, at=c.A(3, 'automáticas', 0.9), label='aba Emissões automáticas')
    c.hover(TAB('Notas recebidas'), 0.6, at=c.A(3, 'recebidas.', 0.9), label='aba Notas recebidas')
    c.confere('main', ['0 / 200 emitidas este mês'], 'selo da cota 0 / 200')
    marcar_alvo(c, P('0 / 200 emitidas este mês'), at=c.A(3, 'selo', 0.6), label='selo da cota (sem o mouse)')
    c.hover(P('Configure seus dados fiscais para começar a emitir notas.'), 0.6, at=c.A(3, 'mês.', 0.3), label='cursor longe do selo')
    c.fim()
    return c


def cap02():
    """Os dados da empresa: painel, abas sem número, IM, CEP, ambiente em Homologação, Verificar cobertura travado, Salvar dados fiscais."""
    c = cap_novo(2, setup=setup_notas())
    c.mark(1)
    c.click(BTN('Configurações fiscais'), at=c.A(1, 'Configurações', 1.0), label='Configurações fiscais')
    c.waitfor(text='Confira e salve os dados fiscais da empresa.', timeout=15)
    c.confere('main', ['Configuração incompleta', 'Município: liberação ainda não confirmada', 'Certificado A1: pendente', 'Empresa', 'Certificado A1', 'Tributação', 'Serviços'],
              'painel Configuração incompleta e as quatro abas')
    c.hover(TAB('Empresa'), 0.2, at=c.A(1, 'quatro', 0.6), label='aba Empresa (o cursor passa pelas quatro abas)')
    c.hover(TAB('Serviços'), 0.3, label='aba Serviços')
    c.hover(P('Configuração incompleta'), 1.4, at=c.A(1, 'painel', 0.4), label='painel: Configuração incompleta')
    c.mark(2)
    c.hover({'placeholder': 'Nome da empresa'}, 0.5, at=c.A(2, 'nome', 0.9), label='Razão social / Nome')
    c.hover({'placeholder': '00.000.000/0000-00'}, 0.8, at=c.A(2, 'CNPJ', 0.4), label='CNPJ')
    c.type(CAMPO('Inscrição Municipal'), '000123-4', at=c.A(2, 'Inscrição', 0.9), label='Inscrição Municipal 000123-4')
    c.confere_campos(['Glacial Cold Brasil', '91.520.340/0001-07', '000123-4'], 'nome, CNPJ e Inscrição Municipal', escopo='main')
    c.hover(P('Exigida pelo município para emitir notas.'), 1.2, at=c.A(2, 'sem', 0.9), label='dica: exigida pelo município para emitir notas')
    c.mark(3)
    c.type({'placeholder': '00000-000'}, '24230190', at=c.A(3, 'endereço', 0.6), clear=True, cps=14, label='CEP 24230-190')
    c.confere_campos(['24230-190', 'Rua Moreira César', '200', 'Icaraí'], 'endereço preenchido pelo CEP', escopo='main')
    c.hover(CAMPO('Logradouro'), 0.3, at=c.A(3, 'rua,', 0.0), label='Logradouro')
    c.hover(CAMPO('Bairro'), 0.3, at=c.A(3, 'bairro,', 0.0), label='Bairro')
    c.hover(P('Cidade / UF'), 0.5, at=c.A(3, 'cidade', 0.0), label='Cidade / UF')
    c.mark(4)
    rola_ate(c, 'Ambiente de emissão de NFS-e', at=c.A(4, 'ambiente', 1.1), label='desce até o ambiente de emissão', y=360)
    c.confere('main', ['Homologação: notas de teste, sem valor fiscal.'], 'ambiente em Homologação')
    c.hover(P('Homologação: notas de teste, sem valor fiscal.'), 1.4, at=c.A(4, 'Homologação,', 0.9), label='Homologação: notas de teste')
    c.hover(TXT('Produção', within='main'), 1.0, at=c.A(4, 'Produção,', 0.9), label='Produção (sem clicar)')
    c.mark(5)
    confere_desligado(c, 'Verificar cobertura do município', 'Verificar cobertura do município desligado')
    c.hover(BTNX('Verificar cobertura do município'), 1.2, at=c.A(5, 'Verificar', 0.9), label='Verificar cobertura do município (travado)')
    c.hover(P('Envie um certificado A1 válido antes de consultar'), 1.6, at=c.A(5, 'certificado,', 0.9), label='dica: o certificado antes da consulta')
    c.mark(6)
    c.click(BTN('Salvar dados fiscais'), at=c.A(6, 'Salvar', 0.9), label='Salvar dados fiscais (rodapé da seção)')
    c.waitfor(text='Dados da empresa salvos.', timeout=12)
    c.waitfor(text='Envie o certificado A1 (.pfx/.p12) usado para assinar as notas no Padrão Nacional.', timeout=10)
    c.confere('body', ['Dados da empresa salvos.', 'Envie o certificado A1 (.pfx/.p12)'], 'salvo e a tela passou para o certificado')
    rola_topo(c, at=c.A(6, 'valem', 0.3), label='sobe às abas (a tela passou para o certificado)')
    c.hover(TAB('Certificado A1'), 0.8, at=c.A(6, 'tela', 0.9), label='aba Certificado A1 (a tela passou sozinha)')
    c.fim()
    return c


def cap03():
    """O certificado digital: arquivo, nome, senha, autorização, Enviar (rodapé da seção), volta à Empresa com o município liberado, registro de uso."""
    c = cap_novo(3, setup=setup_config('certificado', [{'do': 'waitFor', 'text': 'Envie o certificado A1 (.pfx/.p12)', 'timeout': 15}]))
    c.mark(1)
    c.hover(P('Envie o certificado A1 (.pfx/.p12) usado para assinar as notas no Padrão Nacional.'), 1.4, at=c.A(1, 'certificado', 0.9), label='dica do certificado A1')
    c.upload(BTNX('Selecionar arquivo (.pfx / .p12)'), ARQ_CERT, at=c.A(1, 'Escolho', 0.9), label='escolhe certificado-ficticio.pfx')
    c.confere('main', ['certificado-ficticio.pfx'], 'arquivo escolhido')
    c.mark(2)
    # o nome entra logo depois do arquivo (o clique cai no "Dou um nome"): a 9 letras/s a senha atrasava 2,6 s
    c.type({'placeholder': 'Ex: Certificado da empresa'}, 'Certificado da empresa', at=c.A(1, 'certificado.', 0.2, nth=1), clear=True, cps=24,
           label='Nome do certificado (apaga o nome do arquivo)')
    c.type({'placeholder': 'Senha do arquivo .pfx/.p12'}, '$TUT_SENHA', at=c.A(2, 'senha,', 0.4), cps=14, label='Senha do certificado (fictícia, em pontos)')
    c.hover(P('Use a senha do próprio certificado, não a senha do sistema.'), 0.6, at=c.A(2, 'não', 0.3), label='dica: a senha do próprio certificado')
    c.mark(3)
    rola_ate(c, 'Autorização para guardar o certificado', at=c.A(3, 'autorização.', 1.1), label='desce até a autorização', y=300)
    c.hover(P('Autorização para guardar o certificado'), 0.6, label='Autorização para guardar o certificado')
    c.hover(BTN('Ler a Seção 12 dos Termos de Uso'), 1.0, at=c.A(3, 'criptografia', 0.9), label='Ler a Seção 12 dos Termos de Uso (sem clicar)')
    c.click(SEL('#cert-custody-consent'), at=c.A(3, 'assinar', 0.9), label='marca a autorização')
    confere_marcado(c, '#cert-custody-consent', 'autorização marcada')
    c.mark(4)
    c.click(ENVIAR_CERT, at=c.A(4, 'Enviar', 0.9), label='Enviar certificado (rodapé da seção: o robô rola até ele)')
    c.waitfor(text='Certificado digital enviado e guardado com segurança.', timeout=15)
    c.waitfor(text='Município: liberado para emitir notas', timeout=15)
    c.confere('body', ['Certificado digital enviado e guardado com segurança.', 'Confira e salve os dados fiscais da empresa.'], 'enviado e a tela voltou para Empresa')
    rola_topo(c, at=c.A(4, 'município,', 1.0), label='sobe ao painel do alto')
    c.confere('main', ['Apto a emitir', 'Município: liberado para emitir notas', 'Certificado válido até 10/11/2027'], 'painel Apto a emitir')
    c.hover(P('Município: liberado para emitir notas'), 1.2, at=c.A(4, 'liberado.', 0.9), label='Município: liberado para emitir notas')
    c.hover(P('Certificado válido até 10/11/2027'), 1.2, at=c.A(4, 'vale,', 0.9), label='Certificado válido até 10/11/2027')
    c.hover(P('Apto a emitir'), 0.8, at=c.A(4, 'apta', 0.9), label='Apto a emitir')
    c.mark(5)
    c.click(TAB('Certificado A1'), at=c.A(5, 'aba', 0.9), label='aba Certificado A1')
    c.waitfor(text='Registro de uso do certificado', timeout=10)
    rola_ate(c, 'Registro de uso do certificado', at=c.A(5, 'registrado:', 1.0), label='desce até o registro de uso', y=330)
    c.confere('main', ['Certificado utilizado', 'Certificado enviado', 'Envio do certificado'], 'registro de uso: Certificado enviado e, acima, Certificado utilizado')
    confere_ordem(c, 'Certificado utilizado', 'Certificado enviado', 'Certificado utilizado logo acima de Certificado enviado')
    c.hover(P('Certificado enviado'), 1.0, at=c.A(5, 'enviado', 0.9), label='Certificado enviado')
    c.hover(P('Certificado utilizado'), 1.4, at=c.A(5, 'utilizado', 0.9), label='Certificado utilizado (a consulta do município)')
    c.fim()
    return c


def cap04():
    """A tributação: Simples Nacional, apuração na 1ª opção, percentual 6,00, Salvar tributação."""
    c = cap_novo(4, setup=setup_config())
    c.mark(1)
    c.click(TAB('Tributação'), at=c.A(1, 'imposto.', 1.0), label='aba Tributação')
    c.waitfor(text='Regime tributário', timeout=10)
    c.select(COMBO_ROTULO('Regime tributário'), 'Simples Nacional', at=c.A(1, 'Simples', 1.0), label='Regime tributário: Simples Nacional')
    c.confere('main', ['Apuração de tributos no Simples Nacional', 'Tributos federais e municipal (ISS) recolhidos pelo Simples Nacional'], 'apuração já na 1ª opção')
    c.hover(COMBO_ROTULO('Apuração de tributos no Simples Nacional'), 1.0, at=c.A(1, 'apuração,', 0.9), label='Apuração: 1ª opção marcada')
    c.hover(P('Na dúvida, escolha a primeira opção'), 1.6, at=c.A(1, 'maioria', 0.9), label='dica: a primeira opção')
    c.mark(2)
    c.type(CAMPO('Percentual de tributos do Simples Nacional'), '6,00', at=c.A(2, 'Aqui,', 0.9), label='Percentual de tributos 6,00')
    c.confere_campos(['6,00'], 'percentual 6,00', escopo='main')
    c.hover(P('Usado como padrão em toda nota nova.'), 1.4, at=c.A(2, 'sozinho', 0.9), label='dica: padrão em toda nota nova')
    c.mark(3)
    c.click(BTN('Salvar tributação'), at=c.A(3, 'Salvar', 0.9), label='Salvar tributação (rodapé da seção)')
    c.waitfor(text='Configurações fiscais salvas.', timeout=10)
    c.confere('body', ['Configurações fiscais salvas.'], 'aviso Configurações fiscais salvas.')
    c.fim()
    return c


def cap05():
    """Os serviços com código: aba Serviços, Higienização de Split na aba Fiscal, 14.01.01, 001, NBS 120016000, alíquota em branco, Salvar."""
    c = cap_novo(5, setup=setup_config())
    c.mark(1)
    c.click(TAB('Serviços'), at=c.A(1, 'serviços.', 0.9), label='aba Serviços')
    c.waitfor(text='Cadastre aqui os serviços que você fatura', timeout=10)
    c.hover(P('Cadastre aqui os serviços que você fatura'), 1.6, at=c.A(1, 'mesma', 0.9), label='dica: a mesma lista das ordens de serviço')
    c.hover(LISTA_TIPO('Higienização de Split'), 0.8, at=c.A(1, 'códigos', 0.9), label='lista de tipos de serviço')
    c.mark(2)
    c.click(LISTA_TIPO('Higienização de Split'), at=c.A(2, 'Abro', 0.9), label='abre a Higienização de Split (já na aba Fiscal)')
    c.waitfor(text='Fiscal (NFS-e)', timeout=10)
    # o seletor abre para BAIXO sem desviar da borda (avoidCollisions=false): com o bloco no pé da tela a lista saía da janela (e a busca, da faixa
    # de clique do robô, que rolava a lista em vez da página). A página sobe antes de abrir.
    rola_ate(c, 'Fiscal (NFS-e)', at=c.A(2, 'Abro', 0.0), label='sobe o bloco Fiscal (NFS-e) para o alto', y=150)
    c.click(TAXA(0), at=c.A(2, 'Fiscal', 0.0), label='Código de serviço (cTribNac)')
    # o código inteiro: a busca numérica compara só os dígitos ("14.01" casava também 04.14.01, que vem antes na lista e foi o clicado)
    c.type(BUSCA_TAXA, '14.01.01', cps=14, label='busca 14.01.01')
    c.waitfor(target=OPC_TAXA('14.01.01'), timeout=10)
    c.pause(0.1)
    c.click(OPC_TAXA('14.01.01'), label='escolhe 14.01.01')
    c.confere(SEL_FISCAL, ['14.01.01'], 'código de serviço 14.01.01 escolhido')
    c.confere_campos(['14.01'], 'item 14.01 da LC 116 preenchido sozinho', escopo=SEL_FISCAL)
    c.type({'placeholder': 'Ex.: 001'}, '001', at=c.A(2, 'municipal,', 0.0), label='cTribMun 001')
    c.click(TAXA(0), at=c.A(2, 'NBS,', 0.9), label='Código NBS')
    c.type(BUSCA_TAXA, '1200', cps=12, label='busca 1200')
    c.click(OPC_TAXA('120016000'), label='escolhe 120016000')
    c.mark(3)
    c.hover(TXT('Alíquota de ISS (%)'), 1.4, at=c.A(3, 'alíquota', 0.9), label='Alíquota de ISS em branco')
    c.hover(TXT('Alíquota de ISS (%)'), 0.5, at=c.A(3, 'prefeitura', 0.6), label='a alíquota da prefeitura vai aqui')
    c.click(BTN('Salvar'), at=c.A(3, 'Salvo.', 0.9), label='Salvar')
    c.waitfor(text='Tipo de serviço atualizado!', timeout=10)
    c.confere('body', ['Tipo de serviço atualizado!'], 'aviso Tipo de serviço atualizado!')
    c.fim()
    return c


def cap06():
    """Pessoas e serviço: Nova Nota, competência e regime, tomador Restaurante Sabor da Serra, Higienização de Split, discriminação."""
    c = cap_novo(6, setup=setup_notas())
    c.mark(1)
    c.confere('main', ['Autorizadas', 'Processando', 'Rejeitadas', 'Canceladas'], 'indicadores zerados')
    c.hover(P('Autorizadas'), 1.0, at=c.A(1, 'primeira', 0.9), label='indicadores das notas')
    c.click(BTN('Nova Nota'), at=c.A(1, 'Clico', 0.9), label='Nova Nota')
    c.waitfor(text='Data de competência', timeout=12)
    c.mark(2)
    c.confere('dlg', ['Nova NFS-e', 'Pessoas', 'Serviço', 'Valores', 'Revisar e Emitir', 'Data de competência', '13/11/2026', 'Competência'], 'janela Nova NFS-e: competência hoje e regime Competência')
    c.hover(PD('Data de competência'), 1.0, at=c.A(2, 'competência', 0.9), label='Data de competência (hoje)')
    c.hover(PD('Regime de apuração (Simples Nacional)'), 1.0, at=c.A(2, 'regime', 0.9), label='Regime de apuração: Competência')
    c.click(COMBO('Selecione o cliente'), at=c.A(2, 'tomador', 0.9), label='Tomador do serviço')
    c.type({'placeholder': 'Buscar cliente...'}, 'Sabor', label='busca Sabor', noScroll=True)
    c.click(OPT('Restaurante Sabor da Serra'), at=c.A(2, 'restaurante.', 0.4), label='escolhe Restaurante Sabor da Serra')
    c.mark(3)
    c.hover(COMBO('Restaurante Sabor da Serra'), 1.6, at=c.A(3, 'CPF', 0.9), label='tomador escolhido (com CNPJ e endereço)')
    c.confere_ausente('dlg', 'Este cliente está sem CPF/CNPJ', 'sem aviso de documento')
    c.mark(4)
    c.click(BTN('Avançar'), at=c.A(4, 'Serviço,', 1.0), label='Avançar (Serviço)', noScroll=True)
    c.waitfor(text='Escolha um serviço cadastrado', timeout=10)
    c.click(COMBO('Escolha um serviço cadastrado'), at=c.A(4, 'escolho', 0.9), label='Serviço')
    c.waitfor(text='Prontos para emitir', timeout=8)
    c.hover({'text': 'Prontos para emitir', 'within': POP}, 0.6, label='grupo Prontos para emitir')
    c.click(OPT('Higienização de Split'), at=c.A(4, 'prontos', 0.6), label='escolhe Higienização de Split')
    c.confere('dlg', ['14.01.01', '001', '120016000', 'Tributada normalmente'], 'classificação fiscal preenchida pelo serviço')
    c.hover(PD('Classificação fiscal'), 1.4, at=c.A(4, 'códigos', 0.9), label='Classificação fiscal preenchida')
    c.mark(5)
    c.ev(js_dlg_ate('Discriminação do serviço'), at=c.A(5, 'Na', 0.9), label='desce até a discriminação')
    # a 9 letras/s as 45 letras levavam 8,7 s e passavam do fim da fala
    c.type(SEL(f'{DLG} textarea'), 'Limpeza e higienização de 2 splits da cozinha', at=c.A(5, 'discriminação,', 0.5), clear=True, cps=30, label='Discriminação do serviço')
    c.confere_campos(['Limpeza e higienização de 2 splits da cozinha'], 'discriminação digitada')
    c.fim()
    return c


def cap07():
    """Valores e emissão: 450,00, alíquota em branco (aviso amarelo), percentual 6, prévia, pré-visualização, Emitir NFS-e (autoriza na hora)."""
    c = cap_novo(7, setup=setup_notas(REABRE_NOTA))
    c.mark(1)
    c.click(BTN('Avançar'), at=c.A(1, 'Valores,', 1.0), label='Avançar (Valores)', noScroll=True)
    c.waitfor(text='Retenção do ISS', timeout=10)
    c.type(VALOR_SERVICO, '450,00', at=c.A(1, 'valor', 0.9), label='Valor do serviço 450,00')
    c.confere('dlg', ['R$ 450,00', 'Não retido', 'Empresa do Simples Nacional sem retenção de ISS'], 'total R$ 450,00, ISS não retido e o aviso amarelo')
    c.hover(PD('Alíquota ISS %'), 0.8, at=c.A(1, 'alíquota', 0.9), label='Alíquota ISS em branco')
    c.hover(PD('Empresa do Simples Nacional sem retenção de ISS'), 1.6, at=c.A(1, 'aviso', 0.9), label='aviso amarelo do Simples')
    c.mark(2)
    c.ev(js_dlg_ate('Percentual de tributos do Simples Nacional'), at=c.A(2, 'percentual', 1.2), label='desce até o percentual do Simples')
    c.hover(PD('Vem das Configurações fiscais (aba Tributação)'), 1.2, at=c.A(2, 'tributação', 0.9), label='percentual 6 da aba Tributação')
    c.ev(js_dlg_ate('Prévia do cálculo'), at=c.A(2, 'prévia', 1.0), label='desce até a prévia')
    c.hover(PD('Valor líquido'), 1.2, at=c.A(2, 'cálculo', 0.9), label='Prévia do cálculo')
    c.mark(3)
    c.click(BTN('Avançar'), at=c.A(3, 'última', 0.9), label='Avançar (Revisar e Emitir)', noScroll=True)
    c.waitfor(text='Número será atribuído após emissão', timeout=10)
    # CNPJ sem máscara na prévia: defeito do app (handoff)
    c.confere('dlg', ['Glacial Cold Brasil', '91520340000107', '000123-4', 'Niterói - RJ', 'Sabor da Serra Alimentos Ltda', 'Limpeza e higienização de 2 splits da cozinha',
                      'R$ 450,00', 'Pronta para emitir'], 'pré-visualização: empresa, cliente, serviço e valores')
    # a janela guarda a rolagem da aba anterior: sobe por script (sem a roda, que levava ~1,3 s por alvo) e desce de novo só para o serviço
    c.ev(js_dlg_ate('Número será atribuído após emissão'), at=c.A(3, 'pré-visualização,', 1.0), label='sobe ao topo da pré-visualização')
    c.hover(PD('Número será atribuído após emissão'), 0.8, at=c.A(3, 'pré-visualização,', 0.2), label='pré-visualização (o número sai depois)')
    c.hover(PD('Glacial Cold Brasil'), 0.6, at=c.A(3, 'empresa,', 0.6), label='bloco Prestador')
    c.hover(PD('Sabor da Serra Alimentos Ltda'), 0.5, at=c.A(3, 'cliente,', 0.4), label='bloco Tomador')
    c.ev(js_dlg_ate('Limpeza e higienização de 2 splits da cozinha'), at=c.A(3, 'serviço', 0.6), label='desce até o serviço')
    c.hover(PD('Limpeza e higienização de 2 splits da cozinha'), 0.8, label='bloco Serviço e os valores')
    c.ev(js_dlg_ate('Número será atribuído após emissão'), at=c.A(3, 'número', 0.9), label='sobe ao número')
    c.hover(PD('Número será atribuído após emissão'), 1.0, label='Número será atribuído após emissão')
    c.mark(4)
    c.click(BTN('Emitir NFS-e'), at=c.A(4, 'Emitir', 0.9), label='Emitir NFS-e', noScroll=True)
    c.waitfor(text='Nota fiscal enviada para emissão.', timeout=15)
    c.waitfor(text='Chave de acesso', timeout=10)
    c.confere('dlg', ['Nota nº 1', 'Autorizada'], 'o detalhe abre com a nota já autorizada')
    c.fim()
    return c


def cap08():
    """Nota autorizada: Ver detalhe (número, chave, protocolo —), Histórico, Baixar PDF no menu (sem clicar). Nenhum PDF aparece na aula."""
    c = cap_novo(8, setup=setup_notas([{'do': 'waitFor', 'text': 'Restaurante Sabor da Serra', 'timeout': 15}]))
    c.mark(1)
    c.confere('row:Restaurante Sabor da Serra', ['Restaurante Sabor da Serra', '450,00', 'Autorizada'], 'linha da nota autorizada')
    c.confere('main', ['Autorizadas', '0 / 200 emitidas este mês'], 'indicador Autorizadas e a cota (homologação não conta)')
    abrir_menu_hover(c, 'Restaurante Sabor da Serra', 'Ver detalhe', at=c.A(1, 'Ver', 1.4), label='menu ⋯ da nota')
    c.click(ITEM('Ver detalhe'), label='Ver detalhe')
    c.waitfor(text='Chave de acesso', timeout=10)
    c.confere('dlg', ['Nota nº 1', 'Autorizada', 'Emitida em', 'Protocolo', 'Chave de acesso'], 'detalhe: número, autorizada, emitida, chave')
    c.hover(PD('Autorizada'), 0.6, at=c.A(1, 'autorizada,', 0.9), label='selo Autorizada')
    c.hover(PD('Nota nº 1'), 0.5, at=c.A(1, 'número', 0.5), label='Nota nº 1')
    c.hover(PD('Chave de acesso'), 1.0, at=c.A(1, 'chave', 0.4), label='Chave de acesso')
    c.mark(2)
    c.ev(js_dlg_ate('Histórico'), at=c.A(2, 'histórico', 1.2), label='desce até o histórico')
    c.hover(PD('emitida', exact=True), 1.0, at=c.A(2, 'emissão.', 1.2), label='Histórico: emitida')   # exato: "Emitida em" (campo) também casaria
    c.mark(3)
    fechar_janela(c, at=c.A(3, 'lista,', 1.0))
    abrir_menu_hover(c, 'Restaurante Sabor da Serra', 'Baixar PDF', at=c.A(3, 'menu', 1.0), label='menu ⋯ da nota na lista')
    c.confere_ausente('body', 'Baixar XML', 'sem Baixar XML (o motor próprio não guarda XML)', espera=0.2)
    c.hover(ITEM('Baixar PDF'), 1.6, at=c.A(3, 'Baixar', 0.9), label='Baixar PDF (sem clicar: abre outra aba)')
    c.mark(4)
    # sem PDF na aula (decisão de 05/11): a lista e o detalhe não mostram o ambiente da nota, então o zoom continua no "Baixar PDF"
    c.hover(ITEM('Baixar PDF'), 2.4, at=c.A(4, 'homologação,', 1.0), label='Baixar PDF de novo (o PDF de homologação sai sem valor fiscal)')
    c.hover(ITEM('Baixar PDF'), 1.6, at=c.A(4, 'produção,', 0.6), label='Baixar PDF (em produção, a nota que vale)')
    c.press('Escape', at=c.A(4, 'vale.', 0.1), label='fecha o menu')
    c.fim()
    return c


def cap09():
    """Rascunho e cancelamento: rascunho da academia (a janela fica aberta: Cancelar > Descartar e ida/volta de aba num corte), menu do rascunho,
    Cancelar nota aberto e fechado em Voltar. Voz com dois respiros (pausas.py): o preenchimento do rascunho (antes do "Começo a nota") e o corte."""
    c = cap_novo(9, setup=setup_notas([{'do': 'waitFor', 'text': 'Restaurante Sabor da Serra', 'timeout': 15}]))
    c.mark(1)
    c.click(BTN('Nova Nota'), at=c.A(1, 'ainda', 0.2), label='Nova Nota')
    c.waitfor(text='Data de competência', timeout=12)
    c.click(COMBO('Selecione o cliente'), label='Tomador do serviço')
    c.type({'placeholder': 'Buscar cliente...'}, 'Academia', cps=12, label='busca Academia', noScroll=True)
    c.click(OPT('Academia Ponto Forte'), label='escolhe Academia Ponto Forte')
    c.click(BTN('Avançar'), label='Avançar (Serviço)', noScroll=True)
    c.waitfor(text='Escolha um serviço cadastrado', timeout=10)
    c.click(COMBO('Escolha um serviço cadastrado'), label='Serviço')
    c.click(OPT('Manutenção Preventiva'), label='escolhe Manutenção Preventiva')
    c.ev(js_dlg_ate('Discriminação do serviço'), label='desce até a discriminação')
    c.type(SEL(f'{DLG} textarea'), 'Manutenção mensal dos splits', clear=True, cps=24, label='Discriminação: Manutenção mensal dos splits')
    c.click(BTN('Salvar rascunho'), at=c.A(1, 'Salvar', 0.6), label='Salvar rascunho', noScroll=True)
    c.waitfor(text='Rascunho salvo.', timeout=10)
    c.confere('body', ['Rascunho salvo.'], 'aviso Rascunho salvo.')
    # corte: a janela continua aberta depois de salvar (handoff); Cancelar pergunta "Descartar nota?" e a lista só mostra o rascunho depois de trocar de aba.
    # O clique em Cancelar espera a fala acabar ("rascunho." termina em 15,88 s): o corte tira vídeo e voz juntos, então começa no clique, já no silêncio
    # do respiro 2 (06/11 02:3x: com o clique em 15,32 s a janela "Descartar nota?" aparecia ainda sob a fala)
    c.click(BTN('Cancelar', within=DLG), at=c.A(1, 'rascunho.', -0.4), label='corte: Cancelar (fecha a janela)', noScroll=True)   # folga < 0: DEPOIS da palavra
    c.waitfor(text='Descartar nota?', timeout=6)
    c.click(BTN('Descartar'), label='corte: Descartar (o rascunho já está salvo)')
    c.waitfor(gone={'text': 'Descartar nota?'}, timeout=6)
    c.click(TAB('Relatório fiscal'), label='corte: Relatório fiscal (recarrega a lista)')
    c.click(TAB('Notas Fiscais'), label='corte: volta à lista')
    c.waitfor(text='Rascunho', timeout=10)
    c.mark(2)
    c.confere('row:Academia Ponto Forte', ['Academia Ponto Forte', 'Rascunho'], 'linha do rascunho')
    abrir_menu_hover(c, 'Academia Ponto Forte', 'Continuar preenchendo', at=c.A(2, 'rascunho', 0.9), label='menu ⋯ do rascunho')
    # o menu (abre ao passar o mouse) fechou uma vez entre um item e outro na gravação final (06/11 02:27): antes de cada item, se ele sumiu,
    # o cursor volta ao "⋯" e reabre; `noScroll` porque os itens ficam no pé da faixa de clique (y ~700 a 744) e uma rolagem tira o menu do lugar
    for item, palavra in (('Continuar preenchendo', 'continuar'), ('Emitir NFS-e', 'emitir,'), ('Excluir rascunho', 'excluir.')):
        c.hover(MENU_LINHA('Academia Ponto Forte'), 0.4, at=c.A(2, palavra, 0.9), label=f'menu ⋯ do rascunho de novo (só se {item} sumiu)', unless=ITEM(item),
                noScroll=True)   # a condição é lida no `at` (depois da espera), logo antes do item
        c.hover(ITEM(item), 0.6, label=item + (' (sem clicar)' if item == 'Excluir rascunho' else ''), noScroll=True, optional=False, timeout=6)
    c.mark(3)
    c.press('Escape', label='fecha o menu')
    abrir_menu_hover(c, 'Restaurante Sabor da Serra', 'Ver detalhe', at=c.A(3, 'autorizada', 1.0), label='menu ⋯ da Nota nº 1')
    c.click(ITEM('Ver detalhe'), label='Ver detalhe')
    c.waitfor(text='Chave de acesso', timeout=10)
    c.click(BTN('Cancelar nota'), at=c.A(3, 'Cancelar', 0.9), label='Cancelar nota')
    c.waitfor(text='Cancelar esta nota fiscal?', timeout=8)
    c.confere('[role=alertdialog]', ['Cancelar esta nota fiscal?', 'Nota nº 1, Restaurante Sabor da Serra, R$ 450,00.', 'Motivo do cancelamento'], 'janela Cancelar esta nota fiscal?')
    c.hover({'text': 'Obrigatório por exigência legal.', 'within': '[role=alertdialog]'}, 1.6, at=c.A(3, 'obrigatório', 0.9), label='motivo obrigatório (15 a 255 caracteres)')
    c.mark(4)
    c.hover({'text': 'Esta nota já foi enviada e registrada na prefeitura.', 'within': '[role=alertdialog]'}, 1.4, at=c.A(4, 'cancelada', 0.9), label='o cancelamento não tem volta')
    c.click({'role': 'button', 'name': 'Voltar', 'exact': True, 'within': '[role=alertdialog]'}, at=c.A(4, 'volto.', 0.9), label='Voltar (a nota continua Autorizada)')
    c.waitfor(gone={'role': 'alertdialog'}, timeout=6)
    c.confere('dlg', ['Autorizada'], 'a nota continua Autorizada')
    c.fim()
    return c


def cap10():
    """Nota automática do contrato: Gestão > Contratos > PMOC do hotel > Financeiro > Nota fiscal automática (Ligada, vencimento, descrição, NBS)."""
    c = cap_novo(10, setup=SETUP_DASH, prewarm=['/dashboard', '/contratos', f'/contratos/{CONTRATO_ID}', '/notas-fiscais'])
    c.mark(1)
    c.click(BTN('Gestão'), at=c.A(1, 'mês,', 0.6), label='menu Gestão')
    c.click(LINK('Contratos'), label='Contratos')
    c.waitfor(text=CONTRATO_HOTEL, timeout=15)
    c.click(TXT(CONTRATO_HOTEL), at=c.A(1, 'PMOC', 0.9), label='contrato PMOC - Hotel Mirante do Mar')
    c.waitfor(target=TAB('Financeiro'), timeout=15)
    c.ev(js_aba_visivel('Financeiro'), label='a aba Financeiro inteira na faixa de abas')
    c.click(TAB('Financeiro'), at=c.A(1, 'Financeiro', 0.9), label='aba Financeiro')
    c.waitfor(text='Nota fiscal automática', timeout=12)
    rola_ate(c, 'Nota fiscal automática', at=c.A(1, 'tem', 0.0), label='desce até a Nota fiscal automática', y=220)
    c.hover(P('Ligada, o sistema emite a nota fiscal de cada parcela'), 0.4, label='dica da nota automática')
    c.mark(2)
    c.click(SW('Nota fiscal automática'), at=c.A(2, 'Ligo', 0.5), label='liga a Nota fiscal automática (Desligada > Ligada)')
    c.waitfor(text='Quando a nota sai', timeout=8)
    # a lista aberta acompanha a fala (dia fixo, vencimento, pagamento) e a escolha cai no "Aqui, no vencimento"
    c.click(COMBO_ROTULO('Quando a nota sai'), at=c.A(2, 'quando', 0.6), label='Quando a nota sai (abre a lista)')
    c.hover(OPT('Em um dia fixo do mês'), 0.5, at=c.A(2, 'fixo,', 0.6), label='Em um dia fixo do mês')
    c.hover(OPT('No vencimento da parcela'), 0.6, at=c.A(2, 'vencimento', 0.4), label='No vencimento da parcela')
    c.hover(OPT('Quando o cliente pagar'), 0.6, at=c.A(2, 'pagar.', 0.8), label='Quando o cliente pagar')
    c.click(OPT('No vencimento da parcela'), at=c.A(2, 'Aqui,', 0.4), label='escolhe No vencimento da parcela')
    # a descrição (60 letras, ~4,4 s) começa logo depois da escolha; a voz tem um respiro de 1,5 s antes da L3 (pausas.py 10 20.6:1.5)
    c.type({'placeholder': 'Ex.: Manutenção preventiva mensal'}, 'Manutenção preventiva mensal do PMOC - Hotel Mirante do Mar', cps=36,
           label='Descrição do serviço na nota')
    c.mark(3)
    rola_ate(c, 'Dados fiscais', at=c.A(3, 'Os', 0.0), label='desce até os dados fiscais (o seletor do NBS abre para baixo)', y=180)
    c.confere('main', ['Opcionais, em branco, cada campo usa o que está cadastrado no tipo de serviço deste contrato.', 'Herdado do tipo de serviço: 140101',
                       'Herdado do tipo de serviço: 001', 'Sem valor cadastrado no tipo de serviço'], 'dados fiscais herdados da Manutenção Preventiva')
    c.hover(P('Herdado do tipo de serviço: 140101'), 1.2, at=c.A(3, 'Manutenção', 0.9), label='herdado do tipo de serviço')
    c.click(NBS_CONTRATO, at=c.A(3, 'NBS,', 1.0), label='Código NBS (o único sem valor herdado)')
    c.type(BUSCA_TAXA_CONTRATO, '1200', cps=12, label='busca 1200')
    # o cartão é o fim da página (a rolagem para em ~435 px): a opção fica em y ~734, fora da faixa de clique, e o seletor trava a rolagem
    c.click(OPC_TAXA('120016000'), at=c.A(3, 'escolho', 0.5), label='escolhe 120016000', noScroll=True)
    # salvamento automático (700 ms depois da última mudança): "Alteração não salva" > "Salvando..." > "Salvo"; a semente apos-cap10 precisa dele gravado
    c.pause(0.4)
    c.waitfor(gone={'text': 'Alteração não salva'}, timeout=12)
    c.waitfor(gone={'text': 'Salvando...'}, timeout=12)
    c.waitfor(target=SALVO, timeout=10)
    # (sem passar o mouse no "Salvo": o movimento até o alto do cartão levava ~1,5 s e atrasava a L4; o selo aparece sozinho)
    c.mark(4)
    c.ev("(()=>{history.pushState(null,'','/notas-fiscais');dispatchEvent(new PopStateEvent('popstate'));return 1})()", at=c.A(4, 'acompanhar', 1.8),
         label='corte: Notas Fiscais')
    c.waitfor(text='Emita e acompanhe suas NFS-e.', timeout=12)
    c.hover(TAB('Emissões automáticas'), 1.4, at=c.A(4, 'Emissões', 0.9), label='aba Emissões automáticas (sem abrir)')
    c.fim()
    return c


def cap11():
    """As notas dos fornecedores: Notas recebidas > NF-e, Ligar recebimento automático, Sincronizar (a nota da Cobre Sul em resumo)."""
    c = cap_novo(11, setup=setup_notas())
    c.mark(1)
    c.click(TAB('Notas recebidas'), at=c.A(1, 'Notas', 0.9), label='aba Notas recebidas')
    c.waitfor(text='Receber NF-e de fornecedores automaticamente', timeout=10)
    c.confere('main', ['Receber NF-e de fornecedores automaticamente', 'Ligue para consultar, direto na Receita Federal'], 'recebimento de NF-e desligado')
    c.hover(P('Receber NF-e de fornecedores automaticamente'), 1.0, at=c.A(1, 'NF-e', 0.9), label='Receber NF-e de fornecedores automaticamente')
    c.hover(P('Ligue para consultar, direto na Receita Federal'), 1.4, at=c.A(1, 'Receita', 0.9), label='consulta direto na Receita Federal')
    c.mark(2)
    c.click(BTN('Ligar recebimento automático'), at=c.A(2, 'Ligar', 0.9), label='Ligar recebimento automático')
    c.waitfor(text='Recebimento automático ligado.', timeout=10)
    c.waitfor(text='Nenhuma nota recebida ainda', timeout=10)
    c.hover(P('Nenhuma nota recebida ainda'), 1.2, at=c.A(2, 'certificado', 0.9), label='Nenhuma nota recebida ainda')
    c.mark(3)
    c.click(BTNX('Sincronizar'), at=c.A(3, 'Sincronizar,', 0.9), label='Sincronizar')
    c.waitfor(text='1 nota(s) nova(s) encontrada(s).', timeout=12)
    c.waitfor(text='Cobre Sul Suprimentos Ltda', timeout=8)
    c.confere('main', ['Cobre Sul Suprimentos Ltda', '4512', '1.180,00', 'Sem manifestação', 'Resumo'], 'nota da Cobre Sul em resumo')
    c.hover(P('Cobre Sul Suprimentos Ltda'), 1.0, at=c.A(3, 'Cobre', 0.9), label='Cobre Sul Suprimentos Ltda')
    c.hover(TXT('Resumo', within='main'), 1.6, at=c.A(3, 'resumo', 0.9), label='selo Resumo')
    c.fim()
    return c


def cap12():
    """Ciência e conta a pagar (16:20): Manifestar > Dar ciência; corte (worker); Sincronizar (nota completa); Lançar conta a pagar; Ver lançamento.
    Voz com um respiro (pausas.py) depois do "e salvo.": os três seletores da despesa levam ~7 s e a fala os cita em ~4 s."""
    c = cap_novo(12, setup=setup_notas([{'do': 'click', 'target': TAB('Notas recebidas')}, {'do': 'waitFor', 'text': 'Cobre Sul Suprimentos Ltda', 'timeout': 15}, AGUARDA]),
                 prewarm=['/dashboard', '/notas-fiscais', '/financeiro/movimentacoes'])
    c.mark(1)
    c.click(MENU_CARTAO, at=c.A(1, 'manifesto.', 1.2), label='menu ⋮ da nota')
    c.click(ITEM('Manifestar'), label='Manifestar')
    c.waitfor(text='Manifestar sobre a nota', timeout=8)
    c.confere('dlg', ['Manifestar sobre a nota', 'Dar ciência da operação', 'Confirmar a operação', 'Desconheço esta operação', 'Operação não realizada'], 'as quatro respostas')
    c.hover(PD('O que você quer manifestar?'), 1.0, at=c.A(1, 'quatro', 0.9), label='O que você quer manifestar?')
    c.click(PD('Dar ciência da operação', exact=True), at=c.A(1, 'ciência', 0.9), label='Dar ciência da operação')
    c.hover(PD('Avisa a Receita que você está ciente da nota.'), 1.4, at=c.A(1, 'avisa', 0.9), label='Avisa a Receita que você está ciente')
    c.mark(2)
    c.click(BTN('Enviar manifestação'), at=c.A(2, 'manifestação', 0.9), label='Enviar manifestação')
    c.waitfor(text='Manifestação enviada.', timeout=10)
    c.waitfor(text='Ciência em processamento', timeout=10)
    c.confere('main', ['Ciência em processamento'], 'ciência em processamento')
    c.ev(js_semente(CAD['corte_cap12']), label='corte: o worker registra a ciência na Receita (semente t14/corte-cap12)')
    c.clock('00:04:00', label='corte: relógio do navegador 4 min à frente')
    c.click(BTNX('Sincronizar'), at=c.A(2, 'resposta', 0.9), label='Sincronizar (depois do corte)')
    c.waitfor(text='Nenhuma nota nova foi encontrada.', timeout=12)
    c.waitfor(text='Ciência dada', timeout=10)
    c.confere('main', ['Ciência dada'], 'ciência dada')
    c.confere_ausente('main', 'Resumo', 'a nota completa (sem o selo Resumo)', espera=0.5)
    c.mark(3)
    c.click(MENU_CARTAO, at=c.A(3, 'conta', 1.2), label='menu ⋮ da nota')
    c.click(ITEM('Lançar conta a pagar'), label='Lançar conta a pagar')
    c.waitfor(text='Antes de lançar', timeout=8)
    c.confere('dlg', ['A nota traz um vencimento combinado com o fornecedor', '24/11/2026'], 'vencimento combinado: 24/11/2026')
    c.hover(PD('24/11/2026'), 1.4, at=c.A(3, 'vencimento', 0.9), label='1 conta vencendo em 24/11/2026')
    c.click(BTN('Continuar', within=DLG), at=c.A(3, 'fornecedor.', 0.5), label='Continuar')
    c.mark(4)
    c.confere_campos(['Compra · Cobre Sul Suprimentos Ltda'], 'descrição já preenchida')
    c.confere('dlg', ['Cobre Sul Suprimentos Ltda', '24/11/2026'], 'fornecedor vinculado e vencimento')
    c.hover(PD('Fornecedor vinculado'), 0.8, at=c.A(4, 'fornecedor', 0.9), label='Fornecedor vinculado (achado pelo CNPJ)')
    c.select(COMBO('Selecione uma categoria'), 'CSP - Materiais', at=c.A(4, 'vencimento.', 0.4), label='Categoria: CSP - Materiais')
    c.select(COMBO('Selecione uma conta'), 'Conta Principal', at=c.A(4, 'conta', 0.6, nth=0), label='Conta: Conta Principal')
    c.select(COMBO('Selecione a forma de pagamento'), 'Boleto', at=c.A(4, 'salvo.', 0.4), label='Forma de pagamento: Boleto')
    c.click(BTN('Salvar', within=DLG), at=c.A(4, 'ficou', 1.9), label='Salvar (no respiro depois do "e salvo.")')
    c.waitfor(text='Despesa lançada e vinculada à nota.', timeout=12)
    c.waitfor(text='Lançada', timeout=8)
    c.confere('main', ['Lançada'], 'nota marcada como Lançada')
    c.hover(TXT('Lançada', within='main'), 0.6, at=c.A(4, 'Lançada.', 0.9), label='selo Lançada')
    c.mark(5)
    c.click(MENU_CARTAO, at=c.A(5, 'Ver', 1.0), label='menu ⋮ da nota')
    c.hover(ITEM('Ver lançamento'), 1.6, at=c.A(5, 'abre', 0.9), label='Ver lançamento (sem clicar)')
    c.press('Escape', label='fecha o menu')
    c.fim()
    return c


def cap13():
    """Recapitulando (16:20): Configurações fiscais (Apto a emitir), Nova NFS-e e a nota Autorizada, o cartão da nota automática, a nota recebida Lançada."""
    setup = setup_notas([{'do': 'waitFor', 'text': 'Restaurante Sabor da Serra', 'timeout': 15},
                         {'do': 'waitFor', 'target': {'text': 'Autorizada', 'within': 'main tbody'}, 'timeout': 20}, AGUARDA])   # a tela reconfirma a nota (15 min)
    c = cap_novo(13, setup=setup, prewarm=['/dashboard', '/notas-fiscais', '/notas-fiscais/configuracoes', '/contratos', f'/contratos/{CONTRATO_ID}'])
    c.mark(1)
    c.click(BTN('Configurações fiscais'), at=c.A(1, 'Configurações', 1.0), label='Configurações fiscais')
    c.waitfor(text='Apto a emitir', timeout=12)
    c.confere('main', ['Apto a emitir', 'Município: liberado para emitir notas', 'Certificado válido até 10/11/2027'], 'Apto a emitir')
    c.hover(P('Apto a emitir'), 1.0, at=c.A(1, 'salvou', 0.9), label='Apto a emitir')
    c.hover(TAB('Certificado A1'), 0.5, at=c.A(1, 'certificado,', 0.9), label='aba Certificado A1')
    c.hover(TAB('Tributação'), 0.5, at=c.A(1, 'tributação', 0.9), label='aba Tributação')
    c.hover(TAB('Serviços'), 0.5, at=c.A(1, 'serviços', 0.9), label='aba Serviços')
    c.mark(2)
    c.click(BTN('Voltar'), at=c.A(2, 'Emitiu', 1.0), label='Voltar a Notas Fiscais')
    c.waitfor(text='Restaurante Sabor da Serra', timeout=12)
    c.click(BTN('Nova Nota'), label='Nova Nota')
    c.waitfor(text='Data de competência', timeout=10)
    # (sem passar o mouse nas abas da janela: o movimento levava ~0,8 s e atrasava o resto da L2; as quatro abas aparecem com a janela)
    fechar_janela(c, at=c.A(2, 'com', 0.8))
    abrir_menu_hover(c, 'Restaurante Sabor da Serra', 'Baixar PDF', at=c.A(2, 'autorização', 0.4), label='menu ⋯ da nota Autorizada')
    c.hover(ITEM('Baixar PDF'), 0.6, at=c.A(2, 'PDF', 0.5), label='Baixar PDF (sem clicar)')
    c.press('Escape', label='fecha o menu (ele cobre a linha do rascunho)')
    c.hover({'text': 'Rascunho', 'within': 'main tbody'}, 0.8, at=c.A(2, 'rascunho', 0.6), label='o rascunho')
    c.mark(3)
    c.ev(f"(()=>{{history.pushState(null,'','/contratos/{CONTRATO_ID}');dispatchEvent(new PopStateEvent('popstate'));return 1}})()", at=c.A(3, 'contrato,', 1.4),
         label='corte: o contrato do hotel')
    c.waitfor(target=TAB('Financeiro'), timeout=15)
    c.ev(js_aba_visivel('Financeiro'), label='a aba Financeiro inteira na faixa de abas')
    c.click(TAB('Financeiro'), at=c.A(3, 'No', 0.6), label='aba Financeiro')
    c.waitfor(text='Nota fiscal automática', timeout=12)
    rola_ate(c, 'Nota fiscal automática', at=c.A(3, 'parcela.', 1.2), label='o cartão Nota fiscal automática', y=220)
    c.ev("(()=>{history.pushState(null,'','/notas-fiscais');dispatchEvent(new PopStateEvent('popstate'));return 1})()", at=c.A(3, 'fornecedores', 1.0),
         label='corte: Notas Fiscais')
    c.waitfor(text='Emita e acompanhe suas NFS-e.', timeout=12)
    c.click(TAB('Notas recebidas'), label='aba Notas recebidas')
    c.waitfor(text='Lançada', timeout=10)
    c.hover(TXT('Lançada', within='main'), 1.2, at=c.A(3, 'conta', 0.9), label='a nota recebida Lançada')
    c.mark(4)
    c.fim()
    return c
CAPS_ROBO = {n: globals()[f'cap{n:02d}'] for n in range(14) if f'cap{n:02d}' in globals()}

if __name__ == '__main__':
    quais = [int(a) for a in sys.argv[1:]] or sorted(CAPS_ROBO)
    for n in quais:
        c = CAPS_ROBO[n]()
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
        est = f' (voz ESTIMADA nas linhas {",".join(map(str, c.estimadas))})' if c.estimadas else ''
        print(f'cap{n:02d}: {len(d["steps"])} passos, narração {c.dur:.1f} s{est} -> {os.path.relpath(path, HERE)}')
