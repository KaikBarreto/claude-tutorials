#!/usr/bin/env python3
"""T7 · gera rec/t7/cap00..cap14.json (roteiros do robô) a partir da voz pronta (t7/narracao/capNN.json).

1.38.21: preenchimento da OS em visual neutro e capítulo novo cap14 "Editar OS" (exibido depois do cap12 e antes do recap, cap13). Enquanto
não há voz do cap14 (t7/narracao/cap14.json), as marcas Ln e os `at` saem de uma narração PROVISÓRIA estimada do texto de
T07/narracao/tts_textos.py (2,6 palavras/s): serve ao ensaio, não à gravação final (regerar com a voz pronta).

Aula inteira no CELULAR ("device": "phone": 390x844 @2x, quadro 780x1688). Os `at` saem da palavra que anuncia cada passo
(A(linha, palavra, folga)): o gesto "pousa" ~0,7 s depois do início do passo, então `at` = início da palavra - folga.
Rodar de qualquer pasta: `python3 -I rec/t7/gerar.py [NN ...]`. Depois: `node rec/record.mjs rec/t7/capNN.json --check`.
A cadeia de sementes vem de rec/t7/cadeia.json (gerado por rec/t7/semear.py) + o último apos-capNN do capítulo anterior.
Regerar o cap05 logo antes de gravar: a emenda da voz dele pode mudar (os `at` saem do t7/narracao/cap05.json que estiver no disco).

Particularidades do celular (lições deste capítulo da trilha, ver docs/08-licoes.md):
 - GPS: `geo_stub.js` (via eval no `setup`) troca navigator.geolocation por um GPS controlável. O Chromium headless trava
   getCurrentPosition(maximumAge 0) enquanto há um watchPosition ativo, e o app faz as duas coisas. NÃO usar o passo `geo` do runner.
   O stub tem de entrar ANTES de o app abrir a OS por navegação interna (um `goto` com recarga perde o stub).
 - Faixa útil de toque: o cabeçalho verde (sticky, 0-204 px), o cabeçalho do equipamento (até ~335 px, com o acordeão aberto) e o
   rodapé preto (~780-844 px) cobrem a tela. O `ensureVisible` do runner (topo 96, base H-70) não os conhece: `rolar()` leva o alvo
   para y ~ 500 por eval (rolagem suave) antes do toque; elementos fixos (rodapé, cabeçalho, fechar do mapa) vão por `toque()` (eventos
   de ponteiro sintéticos COM coordenadas: a telemetria os registra como clique e o editor desenha o anel do toque).
 - Relógio: o servidor falso tem relógio congelado (carimbos do servidor ficam em 08:50); o do NAVEGADOR salta com o passo `clock`
   (check-in 09:05, check-out 10:30 -> "Duração 1h 25min"). O salto é o ÚLTIMO passo do `setup` (a hora só avança 1 min depois dele).
 - A assinatura é desenhada por eventos de mouse sintéticos no canvas (curvas suaves, tempo controlado); o controle de nota da pesquisa
   (Radix Slider) é arrastado por um marcador invisível posto na ponta da barra.
"""
import json, math, os, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
NARR = os.path.normpath(os.path.join(HERE, '..', '..', 't7', 'narracao'))
CAD = json.load(open(os.path.join(HERE, 'cadeia.json'), encoding='utf8'))
ENV = json.load(open(os.path.join(HERE, '..', 'env.json'), encoding='utf8'))
BASE = CAD['inicio'] + ['t7/vazias-1.38.21']   # 1.38.21: tabelas lidas pelo app e vazias de propósito (sem TABELA_SEM_SEED)
OS16 = CAD['os16']
BAKED = ENV['fakeUrl']          # o app chama essa URL; o navegador a redireciona para a instância do falso deste agente
STUB = open(os.path.join(HERE, 'geo_stub.js'), encoding='utf8').read()
FOTO = 'assets/foto-equipamento.jpg'  # relativo a esta pasta (o `upload` resolve pela pasta do roteiro)

# estado de partida de cada capítulo (último apos-capNN que existe; só os capítulos que mudam o banco geram um)
SEMENTE = {0: None, 1: None, 2: None, 3: 'apos-cap02', 4: 'apos-cap03', 5: 'apos-cap04', 6: 'apos-cap05', 7: 'apos-cap06',
           8: 'apos-cap07', 9: 'apos-cap08', 10: 'apos-cap09', 11: 'apos-cap10', 12: 'apos-cap10', 13: None, 14: 'inicio-editar-os'}

NOMES = ['Abertura', 'Abrindo a OS no celular', 'A Caminho e a rota', 'Check-in', 'O checklist do equipamento', 'Fotos e vídeo',
         'Consumir do estoque', 'Pausar e retomar', 'Finalizar parcialmente', 'A assinatura do cliente', 'Finalizar a OS',
         'O relatório e o PDF', 'O link do cliente', 'Recapitulando', 'Editar a OS em campo']

# posições do aparelho (mundo fictício, Niterói): saída do técnico e o Colégio Monte Verde
SAIDA = (-22.9003, -43.1180)
ESCOLA = (-22.89758, -43.09913)
# relógio do navegador de cada capítulo (a hora só aparece no carimbo do check-in, na duração, na assinatura e em "Pausada há")
RELOGIO = {0: '08:50', 1: '08:50', 2: '08:50', 3: '09:05', 4: '09:08', 5: '09:20', 6: '09:35', 7: '09:45', 8: '09:55', 9: '10:20',
           10: '10:30', 11: '10:31', 12: '10:40', 13: '10:45', 14: '08:50'}


def norm(s):
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode().lower()
    return ''.join(ch for ch in s if ch.isalnum() or ch in '?')


# ================================================================ trechos de JavaScript (executados na página por `eval`)
def js_rolar(expr, y=500, dur_ms=None, banda=None):
    """rolagem suave da página até o centro do elemento que `expr` devolve ficar em y (px CSS). Devolve a promessa (o robô espera).
    `banda=(a, b)`: não rola se o centro do elemento já está entre a e b (a câmera não balança à toa).
    Sem alvo devolve 'SEM ALVO' (aparece no log do robô)."""
    d = 'Math.min(1000,Math.max(450,Math.abs(dy)*1.15))' if dur_ms is None else str(dur_ms)
    ban = f"if({banda[0]}<=cy&&cy<={banda[1]})return 'ok';" if banda else ''
    return (f"(async()=>{{const el=({expr});if(!el)return 'SEM ALVO';const r=el.getBoundingClientRect();const cy=r.top+r.height/2;{ban}"
            f"const y0=window.scrollY,dy=Math.round(cy-({y}));if(Math.abs(dy)<3)return 'ok';"
            f"const dur={d},t0=performance.now();"
            "await new Promise(res=>{const f=t=>{const p=Math.min(1,(t-t0)/dur),e=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;"
            "window.scrollTo({top:y0+dy*e,behavior:'instant'});p<1?requestAnimationFrame(f):res()};requestAnimationFrame(f)});"
            "return Math.round(el.getBoundingClientRect().top)})()")


def js_rolar_em(expr, y=500, dur_ms=700):
    """como js_rolar, mas rola o container com rolagem mais próximo do elemento (a gaveta "Editar OS"), não a página"""
    return (f"(async()=>{{const el=({expr});if(!el)return 'SEM ALVO';let sc=el.parentElement;"
            "while(sc&&!(/(auto|scroll)/.test(getComputedStyle(sc).overflowY)&&sc.scrollHeight>sc.clientHeight+4))sc=sc.parentElement;"
            "if(!sc)return 'SEM ROLAGEM';const r=el.getBoundingClientRect();"
            f"const y0=sc.scrollTop,dy=Math.round(r.top+r.height/2-({y}));if(Math.abs(dy)<3)return 'ok';const dur={dur_ms},t0=performance.now();"
            "await new Promise(res=>{const f=t=>{const p=Math.min(1,(t-t0)/dur),e=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;"
            "sc.scrollTop=y0+dy*e;p<1?requestAnimationFrame(f):res()};requestAnimationFrame(f)});"
            "return Math.round(el.getBoundingClientRect().top)})()")


def js_quieto(max_ms=11000, quadros=14, limite=40):
    """espera o navegador sossegar: `quadros` quadros seguidos de menos de `limite` ms (ou `max_ms` de espera). O mapa da rota
    (MapLibre, desenhado por software) deixa a página ocupada por ~7 s depois do A Caminho; um passo que consulte a página nesse
    período (hover, rect) demora 2 a 3 s e atrasa os seguintes (T7, cap. 2: `lateBy` 2,36)."""
    return ("new Promise(res=>{const t0=performance.now();let ok=0,ult=t0;const f=n=>{ok=(n-ult)<%d?ok+1:0;ult=n;"
            "if(ok>=%d||n-t0>%d)res(Math.round(n-t0));else requestAnimationFrame(f)};requestAnimationFrame(f)})") % (limite, quadros, max_ms)


def js_toque(expr):
    """toque sintético no centro do elemento (ponteiro + mouse + click COM coordenadas): serve para o que o runner não alcança
    (rodapé fixo, cabeçalho, botão de fechar do mapa) e ainda gera o anel de toque na edição"""
    return (f"(()=>{{const el=({expr});if(!el)return 'SEM ALVO';const r=el.getBoundingClientRect();const x=r.left+r.width/2,y=r.top+r.height/2;"
            "const o={bubbles:true,cancelable:true,composed:true,clientX:x,clientY:y,screenX:x,screenY:y,button:0,view:window};"
            "const pe=(t,b)=>new PointerEvent(t,{...o,pointerId:1,pointerType:'mouse',isPrimary:true,buttons:b,width:1,height:1});"
            "const me=(t,b)=>new MouseEvent(t,{...o,buttons:b,detail:1});"
            "el.dispatchEvent(pe('pointerdown',1));el.dispatchEvent(me('mousedown',1));el.dispatchEvent(pe('pointerup',0));"
            "el.dispatchEvent(me('mouseup',0));el.dispatchEvent(me('click',0));return [Math.round(x),Math.round(y)]})()")


def js_botao(texto, sel='button'):
    """expressão: o último `sel` visível cujo texto (aparado) é `texto`"""
    return f"[...document.querySelectorAll({json.dumps(sel)})].filter(b=>b.textContent.trim()==={json.dumps(texto)}&&b.getClientRects().length).pop()"


def js_sel(sel, nth=0):
    return f"document.querySelectorAll({json.dumps(sel)})[{nth}]"


def js_label(texto, sel='main *'):
    """expressão: a primeira folha (sem filhos) de `sel` cujo texto aparado é `texto` (para centralizar rótulos com `rolar`)"""
    return f"[...document.querySelectorAll({json.dumps(sel)})].find(e=>e.children.length===0&&e.textContent.trim()==={json.dumps(texto)})"


def assinatura():
    """dois traços de assinatura (frações do canvas): um rabisco de ponta a ponta e um sublinhado"""
    t1 = []
    n = 56
    for i in range(n + 1):
        t = i / n
        x = 0.10 + 0.78 * t
        y = 0.50 + 0.21 * math.sin(t * math.pi * 5.0) * (0.35 + 0.65 * (1 - t)) - 0.09 * math.sin(t * math.pi * 1.3)
        t1.append([round(x, 3), round(y, 3)])
    t2 = [[round(0.16 + 0.70 * (i / 24), 3), round(0.82 - 0.07 * math.sin(math.pi * i / 24), 3)] for i in range(25)]
    return [t1, t2]


def js_assinar(tracos, durs=(1500, 800), canvas="document.querySelector('main canvas')"):
    """desenha `tracos` no canvas da assinatura com eventos de mouse sintéticos (mousedown, mousemove..., mouseup), no ritmo de
    `durs` (ms por traço). O app escuta onMouseDown/Move/Up do React: os eventos sintéticos com clientX/Y valem."""
    return ("(async()=>{const cv=" + canvas + ";if(!cv)return 'SEM ALVO';const r=cv.getBoundingClientRect();"
            "const T=" + json.dumps(tracos) + ",D=" + json.dumps(list(durs)) + ";"
            "const ev=(t,x,y,b)=>cv.dispatchEvent(new MouseEvent(t,{bubbles:true,cancelable:true,view:window,clientX:x,clientY:y,screenX:x,screenY:y,button:0,buttons:b,detail:1}));"
            "const pt=p=>[r.left+p[0]*r.width,r.top+p[1]*r.height];"
            "for(let k=0;k<T.length;k++){const P=T[k],dur=D[k]||1000;let [x,y]=pt(P[0]);ev('mousedown',x,y,1);"
            "await new Promise(res=>{const t0=performance.now();let i=1;const f=t=>{const p=Math.min(1,(t-t0)/dur),upto=Math.round(p*(P.length-1));"
            "while(i<=upto){[x,y]=pt(P[i]);ev('mousemove',x,y,1);i++}p<1?requestAnimationFrame(f):res()};requestAnimationFrame(f)});"
            "ev('mouseup',x,y,0);await new Promise(rs=>setTimeout(rs,160))}return T.length})()")


def js_marcador_slider(mid='__wp1'):
    """põe um marcador invisível logo além da ponta direita da barra de nota (Radix Slider), na altura do controle: é o destino do
    `drag` (soltar além da ponta vale 10)"""
    return ("(()=>{const th=document.querySelector('[role=slider]');if(!th)return 'SEM ALVO';const root=th.parentElement.parentElement;"
            "const rr=root.getBoundingClientRect(),tr=th.getBoundingClientRect();let m=document.getElementById(" + json.dumps(mid) + ");"
            "if(!m){m=document.createElement('div');m.id=" + json.dumps(mid) + ";m.style.cssText='position:fixed;width:6px;height:6px;opacity:0;pointer-events:none;z-index:2147483647';document.body.appendChild(m)}"
            "m.style.left=(rr.right+4-3)+'px';m.style.top=(tr.top+tr.height/2-3)+'px';return [Math.round(rr.right),Math.round(tr.top+tr.height/2)]})()")


def js_pesquisa(arquivo):
    """aplica no servidor falso (instância do agente) a semente que esconde/mostra a linha de avaliação da OS (survey_enabled) e,
    se `avisar`, o app refaz a leitura do link público como quando a aba volta a ficar visível"""
    return (f"(async()=>{{const r=await fetch({json.dumps(BAKED + '/__dev/seed')},{{method:'POST',headers:{{'content-type':'application/json'}},"
            f"body:JSON.stringify({{files:[{json.dumps(arquivo)}]}})}});return r.status}})()")


JS_VISIBILIDADE = "(()=>{document.dispatchEvent(new Event('visibilitychange'));return document.visibilityState})()"


# remendo de página: o envio de foto do app é por XHR e, em localhost, termina em ~0,2 s (a barra "Enviando... N%" some antes de ser
# vista). Aqui o envio real é atrasado `__upMs` ms e o app recebe eventos `progress` crescentes, como numa rede de celular.
SLOW_UPLOAD = """(()=>{if(window.__upSlow)return 'ja';const op=XMLHttpRequest.prototype.open,sd=XMLHttpRequest.prototype.send;
XMLHttpRequest.prototype.open=function(m,u){u=String(u);if(window.__fakeDirect&&u.indexOf(window.__fakeBaked)===0){u=window.__fakeDirect+u.slice(window.__fakeBaked.length);arguments[1]=u}this.__u=u;return op.apply(this,arguments)};
XMLHttpRequest.prototype.send=function(b){if(!/\\/storage\\/v1\\/object\\//.test(this.__u||'')||!window.__upMs)return sd.call(this,b);
const x=this,tot=(b&&(b.size||b.byteLength))||100000,t0=Date.now(),ms=window.__upMs;
const tk=()=>{const f=Math.min(0.95,(Date.now()-t0)/ms);try{x.upload.dispatchEvent(new ProgressEvent('progress',{lengthComputable:true,loaded:Math.round(tot*f),total:tot}))}catch(e){}
if(Date.now()-t0<ms)setTimeout(tk,90);else sd.call(x,b)};tk()};window.__upSlow=true;window.__upMs=2200;return 'instalado'})()"""
# Instância própria do falso (FAKE_URL diferente da URL gravada no build): o desvio de rede do robô (route.fetch com outra URL) perde o corpo
# BINÁRIO do XHR (a foto chegava com 0 byte e o app mostrava "Imagem indisponível"). O envio da foto vai direto à instância (CORS aberto).
FAKE_DIRETO = os.environ.get('FAKE_URL', '').rstrip('/')
if FAKE_DIRETO and FAKE_DIRETO != BAKED.rstrip('/'):
    SLOW_UPLOAD = f"(()=>{{window.__fakeBaked={json.dumps(BAKED.rstrip('/'))};window.__fakeDirect={json.dumps(FAKE_DIRETO)}}})();" + SLOW_UPLOAD


# ================================================================ alvos
BTN = lambda n, **kw: {'role': 'button', 'name': n, 'exact': True, **kw}
TXT = lambda t, **kw: {'text': t, 'exact': False, **kw}
TXTX = lambda t, **kw: {'text': t, 'exact': True, **kw}
SEL = lambda s, **kw: {'selector': s, **kw}
CARD_OS = {'text': 'Colégio Monte Verde', 'within': 'main'}   # o cartão da OS #16 na Agenda do dia
SW = {'role': 'switch'}                                          # interruptor Sim/Não (respondido some: o próximo é sempre o nth 0)
INP = lambda n=0: {'selector': "main input[placeholder='Digite o valor...']", 'nth': n}
ACC = {'text': 'Hi-Wall 18.000 BTUs', 'within': 'main'}          # acordeão do equipamento
LAPIS = lambda n: {'selector': "main button[title='Editar resposta']", 'nth': n}
FECHAR_EDICAO = {'selector': "main button[title='Fechar edição']"}
OPCAO = lambda t: {'selector': 'main label', 'hasText': t, 'nth': 0}   # opção da pergunta de seleção (label com caixa de marcar)
GALERIA = {'selector': 'main label', 'hasText': 'Galeria'}
TIRAR_FOTO = {'selector': 'main label', 'hasText': 'Tirar Foto'}
MAIS_ACOES = {'selector': "button[aria-label='Mais ações']"}
FAB = {'selector': "button[aria-label*='cnico' i], a[aria-label*='cnico' i]"}   # botão redondo da Área do Técnico™ (confirmar no ensaio)
MAPA = {'selector': '.leaflet-container'}
DLG = "div[role=dialog][aria-modal=true]"
# pontos (px CSS) dos botões fixos do rodapé preto
FAB_PT = (44, 800)   # centro do botão redondo da Área do Técnico (CSS px): fixo no canto inferior esquerdo; com a OS em atendimento sobe 56 px
RODAPE = {'finalizar': (98, 812), 'parcial': (268, 812), 'menu': (375, 812), 'retomar': (160, 812), 'pdf': (110, 812)}
EXPR_MENU = "document.querySelector('button[aria-label=\"Mais ações\"]')"


TTS = os.path.normpath(os.path.join(HERE, '..', '..', '..', 'claude-tutorials', 'planejamento', 'domiflix', 'T07', 'narracao', 'tts_textos.py'))


def narracao_provisoria(n, pps=2.6, folga=0.5):
    """narração estimada (sem voz): início de cada linha e de cada palavra a `pps` palavras por segundo, `folga` s entre as linhas"""
    import importlib.util
    sp = importlib.util.spec_from_file_location('tts_textos', TTS)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    t, words, linhas = 1.0, [], []   # 1 s de respiro antes da primeira palavra
    for li, txt in enumerate(m.CAPS[n].split('\n')):
        ws = txt.replace('[pause]', ' ').split()
        linhas.append({'s': round(t, 2)})
        for w in ws:
            words.append({'w': w, 's': round(t, 2), 'linha': li})
            t += 1 / pps
        t += folga
    return {'words': words, 'linhas': linhas, 'dur': round(t, 2), 'provisoria': True}


class Cap:
    def __init__(s, n, pace=0.4, cps=9, start=(195, 600), prewarm=None, setup=None, user='rafael.lima@glacialcold.example'):
        s.n = n
        arq = f'{NARR}/cap{n:02d}.json'
        d = json.load(open(arq)) if os.path.exists(arq) else narracao_provisoria(n)
        s.provisoria = not os.path.exists(arq)
        s.words, s.linhas, s.dur = d['words'], d['linhas'], d['dur']
        s.steps = []
        s.pace, s.cps, s.start = pace, cps, start
        s.prewarm = prewarm or ['/agenda']
        s.setup = setup or []
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
            raise SystemExit(f'cap{s.n:02d}: palavra "{palavra}" (#{nth}) não achada na linha {i}')
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
        # as marcas Ln entram na ordem do tempo: antes do primeiro passo cujo `at` já é >= ao início da linha
        if d.get('at') is not None:
            for mt, mi in s.pending:  # passo que começaria até 0,25 s antes da linha começa junto com ela (a marca vem antes)
                if d['at'] < mt <= d['at'] + 0.25:
                    d['at'] = round(mt, 2)
            s.flush(d['at'])
        s.steps.append(d)
        return d

    def mark(s, i, at=None):
        """marca Ln = início da linha i da fala; `at` antecipa a marca quando o 1º gesto da linha começa antes da fala"""
        t = s.L(i) if at is None else at
        if t <= 0:
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

    def hover(s, target, seconds=0.9, at=None, label=None, **kw):
        kw.setdefault('optional', True)   # cosmético: se o alvo não existir, o robô segue (o ensaio acusa)
        kw.setdefault('timeout', 4)
        return s._p({'do': 'hover', 'target': target, 'seconds': seconds}, at, label, kw)

    def type(s, target, text, at=None, label=None, cps=None, **kw):
        d = {'do': 'type', 'target': target, 'text': text}
        if cps:
            d['cps'] = cps
        return s._p(d, at, label, kw)

    def upload(s, target, file, at=None, label=None, **kw):
        return s._p({'do': 'upload', 'target': target, 'file': file}, at, label, kw)

    def drag(s, target, to, at=None, label=None, **kw):
        return s._p({'do': 'drag', 'target': target, 'to': to}, at, label, kw)

    def scroll(s, at=None, label=None, **kw):
        return s._p({'do': 'scroll'}, at, label, kw)

    def pause(s, seconds):
        return s.add({'do': 'pause', 'seconds': seconds})

    def waitfor(s, **kw):
        return s.add({'do': 'waitFor', **kw})

    def ev(s, js, at=None, label=None, **kw):
        return s._p({'do': 'eval', 'js': js}, at, label, kw)

    def rolar(s, expr, at=None, label=None, y=500, dur_ms=None, banda=None):
        """rolagem suave da página até `expr` ficar em y (px CSS); o passo só termina quando a rolagem acaba"""
        return s.ev(js_rolar(expr, y, dur_ms, banda), at=at, label=label)

    def goto(s, url, at=None, label=None, **kw):
        return s._p({'do': 'goto', 'url': url}, at, label, kw)

    def _cursor(s, ponto, at):
        return s._p({'do': 'scroll', 'point': {'x': ponto[0], 'y': ponto[1]}, 'by': 0, 'duration': 0.3, 'after': 0}, round(max(0.0, at - 0.9), 2), None, {})

    def apontar(s, alvo, ponto, at, label):
        """aponta (sem tocar) um elemento fixo fora da faixa do runner: leva o cursor ao ponto e registra o retângulo do alvo
        (passo `type` sem clique), para a câmera da edição."""
        s._cursor(ponto, at)
        s.add({'do': 'type', 'target': alvo, 'text': '', 'noClick': True, 'label': label, 'at': round(at, 2), 'optional': True, 'timeout': 4})

    def toque(s, alvo, expr, ponto, at, label):
        """toca num elemento fixo (rodapé, cabeçalho, botão de fechar): cursor ao ponto, retângulo do alvo (rótulo) e o toque
        sintético por eval no instante `at`."""
        s._cursor(ponto, at)
        s.add({'do': 'type', 'target': alvo, 'text': '', 'noClick': True, 'label': label, 'at': round(max(0.0, at - 0.1), 2), 'optional': True, 'timeout': 4})
        return s._p({'do': 'eval', 'js': js_toque(expr)}, round(at, 2), label + ' (toque)', {})

    def fim(s):
        s.flush(1e9)
        s.steps.append({'do': 'mark', 'name': 'FIM', 'at': round(s.dur, 2)})

    def out(s):
        sem = SEMENTE[s.n]
        d = {
            'name': f't7-cap{s.n:02d}',
            'title': f'T7 · Cap. {s.n} · {NOMES[s.n]} (narração {str(round(s.dur, 1)).replace(".", ",")} s; marcas L1..L{len(s.linhas)} = início de cada linha do roteiro)',
            'seed': f't7-cap{s.n:02d}', 'pace': s.pace, 'cps': s.cps, 'tail': 1.5, 'device': 'phone',
            'start': {'x': s.start[0], 'y': s.start[1]},
            'seedExtra': BASE + ([f't7/{sem}'] if sem else []),
            'prewarm': s.prewarm, 'setup': s.setup, 'steps': s.steps,
        }
        if s.user:
            d['user'] = s.user
        return d


# ================================================================ trechos comuns (não filmados, no `setup`)
def relogio(n):
    return {'do': 'clock', 'set': f'2026-11-11T{RELOGIO[n]}:00-03:00'}


def setup_agenda(n, pos=SAIDA, extra=()):
    """Agenda do técnico em "Dia" (quarta, 11/11), com o GPS emulado. O relógio do capítulo entra por último (fim_setup)."""
    return [
        {'do': 'goto', 'url': '/agenda'}, {'do': 'waitFor', 'text': 'Colégio Monte Verde', 'timeout': 25}, {'do': 'waitFor', 'idle': True},
        {'do': 'eval', 'js': STUB}, {'do': 'eval', 'js': f'window.__setGeo({pos[0]},{pos[1]})'}, *extra]


def fim_setup(n, pausa=0.5):
    """último passo do `setup`: o relógio do navegador salta para a hora do capítulo (a hora só avança 1 min depois dele)"""
    return [relogio(n), {'do': 'pause', 'seconds': pausa}]


def abrir_os(espera='Glacial Cold Brasil'):
    """da Agenda até a tela da OS #16 (cartão -> "Resumo da OS" -> "Preencher OS"), como o técnico faz; vai por navegação interna,
    que mantém o GPS emulado de pé (o app só rastreia a posição depois que a OS abre)"""
    return [{'do': 'click', 'target': CARD_OS}, {'do': 'waitFor', 'text': 'Resumo da OS', 'timeout': 10},
            {'do': 'click', 'target': BTN('Preencher OS')}, {'do': 'waitFor', 'text': espera, 'timeout': 20},
            {'do': 'waitFor', 'idle': True}, {'do': 'pause', 'seconds': 0.8}]


def abrir_relatorio():
    """da Agenda até o Relatório de Serviço da OS concluída (o cartão abre o resumo; o botão principal vira "Relatório de Serviço")"""
    return [{'do': 'click', 'target': CARD_OS}, {'do': 'waitFor', 'text': 'Resumo da OS', 'timeout': 10},
            {'do': 'click', 'target': BTN('Relatório de Serviço')}, {'do': 'waitFor', 'text': 'Execução', 'timeout': 20},
            {'do': 'waitFor', 'idle': True}, {'do': 'pause', 'seconds': 0.8}]


def abrir_checklist():
    """abre o acordeão do equipamento (as perguntas aparecem logo)"""
    return [{'do': 'click', 'target': ACC}, {'do': 'pause', 'seconds': 0.8}]


def setup_os(n, pos=ESCOLA, checklist=False, extra=(), depois=()):
    s = setup_agenda(n, pos, extra) + abrir_os()
    if checklist:
        s += abrir_checklist()
    return s + list(depois) + fim_setup(n)


# ================================================================ capítulos
def cap00():
    """Abertura: a Agenda do técnico, só a câmera passeia pelo cartão da OS #16"""
    c = Cap(0, pace=0.4, setup=setup_agenda(0) + fim_setup(0))
    c.mark(1)
    c.hover(CARD_OS, 1.2, at=c.A(1, 'ordem', 2.5), label='o cartão da OS #16 na Agenda')
    c.mark(2)
    c.hover(CARD_OS, 0.7, at=c.A(2, 'abre', 0.5), label='o cartão da OS #16 (o técnico abre a ordem)')
    c.hover(TXT('Manutenção Preventiva', within='main'), 1.2, at=c.A(2, 'preenche', 0.5), label='o serviço do cartão')
    c.hover(CARD_OS, 2.0, at=c.A(2, 'relatório', 1.2), label='o cartão da OS #16 (o relatório)')
    c.mark(3)
    c.hover(TXT('11 De Novembro De 2026', within='main'), 1.4, at=c.A(3, 'agenda', 0.8), label='a data da agenda do técnico')
    c.fim()
    return c


def cap01():
    """Abrindo a OS: cartão -> Resumo da OS -> Preencher OS -> tela da OS (cabeçalho, Ir para o Atendimento, cliente, Área do Técnico)"""
    # aquece a tela da OS (módulos e mapa) e volta à Agenda: o robô filma já com tudo na memória
    c = Cap(1, pace=0.4, setup=setup_agenda(1) + abrir_os() + [
        {'do': 'eval', 'js': 'history.back()'}, {'do': 'waitFor', 'text': 'Colégio Monte Verde', 'timeout': 15},
        {'do': 'waitFor', 'idle': True}] + fim_setup(1, 0.6))
    c.mark(1)
    c.hover(CARD_OS, 1.0, at=c.A(1, 'dezesseis', 1.0), label='a OS número 16 na Agenda')
    c.click(CARD_OS, at=c.A(1, 'Tocando', 0.8), label='abre o resumo da OS')
    c.waitfor(text='Resumo da OS', timeout=10)
    c.hover(TXT('(21) 3000-2201'), 0.5, at=c.A(1, 'cliente,', 0.9), label='resumo: o cliente')
    c.hover(TXT('11 de novembro às 09:00'), 0.4, at=c.A(1, 'horário,', 0.9), label='resumo: o horário')
    c.hover(TXTX('Responsáveis'), 0.4, at=c.A(1, 'responsável', 0.9), label='resumo: o responsável')
    c.hover(TXTX('Descrição'), 0.4, at=c.A(1, 'descrição', 0.9), label='resumo: a descrição do serviço')
    c.mark(2)
    c.hover(BTN('Preencher OS'), 0.6, at=c.A(2, 'Preencher', 0.9), label='o botão Preencher OS')
    c.click(BTN('Preencher OS'), at=c.A(2, 'Toco', 0.8), label='Preencher OS')
    c.waitfor(text='Glacial Cold Brasil', timeout=15)
    c.waitfor(idle=True)
    c.apontar(TXTX('Glacial Cold Brasil'), (196, 56), c.A(2, 'faixa', 0.3), 'cabeçalho: a empresa')
    c.apontar(SEL('h1'), (196, 82), c.A(2, 'número', 0.3), 'cabeçalho: OS #16')
    c.hover(SEL('span.rounded-full', hasText='Manutenção Preventiva'), 0.3, at=c.A(2, 'serviço,', 0.9), label='cabeçalho: o serviço')
    c.hover(TXT('11/11/2026 09:00'), 0.3, at=c.A(2, 'data', 0.9), label='cabeçalho: data e hora')
    c.apontar(TXTX('Pendente'), (323, 26), c.A(2, 'status,', 0.2), 'cabeçalho: o selo Pendente')
    c.mark(3)
    c.hover(TXT('Ir para o Atendimento'), 0.6, at=c.A(3, 'cartão', 0.9), label='cartão Ir para o Atendimento')
    c.hover(BTN('A Caminho'), 0.5, at=c.A(3, 'botões', 0.9), label='os botões do atendimento')
    c.hover(TXTX('Colégio Monte Verde'), 0.4, at=c.A(3, 'cliente,', 0.9), label='dados do cliente')
    c.hover(TXT('(21) 3000-2201'), 0.2, at=c.A(3, 'telefone,', 0.9), label='o telefone do cliente')
    c.hover(SEL("a[href*='wa.me'], a[href*='whatsapp']"), 0.2, at=c.A(3, 'WhatsApp', 0.9), label='o atalho de WhatsApp')
    c.hover(TXT('Rua Noronha Torrezão'), 0.2, at=c.A(3, 'endereço,', 0.9), label='o endereço do cliente')
    c.hover(TXT('Descrição do serviço'), 0.3, at=c.A(3, 'descrição', 0.9), label='a descrição do serviço')   # 1.38.20: "serviço" minúsculo, bloco único sem cartões
    c.mark(4)
    c.apontar(FAB, FAB_PT, c.A(4, 'botão', 0.9), 'o botão redondo da Área do Técnico')   # fixo (y 800): `hover` rolaria em vão uns 7 s
    c.apontar(FAB, FAB_PT, c.A(4, 'disponível', 0.9), 'a Área do Técnico durante o atendimento')
    c.mark(5)
    c.apontar(SEL('h1'), (196, 82), c.A(5, 'gestor', 0.9), 'a mesma página para técnico, gestor e cliente')
    c.fim()
    return c


def cap02():
    """A Caminho e a rota: A Caminho -> status e cartão Iniciar Atendimento -> Rota até o cliente -> Ampliar/fechar -> Waze e Google Maps"""
    c = Cap(2, pace=0.4, setup=setup_os(2, SAIDA))
    c.mark(1)
    c.hover(TXT('Ir para o Atendimento'), 0.8, at=1.4, label='o cartão Ir para o Atendimento')
    c.click(BTN('A Caminho'), at=c.A(1, 'Toco', 0.0), label='A Caminho')
    c.waitfor(text='Rota até o cliente', timeout=15)
    c.ev(js_quieto(), label='espera o mapa terminar de desenhar')   # sem passo que consulte a página enquanto o mapa desenha (~7 s)
    c.mark(2)
    c.apontar(TXTX('A Caminho'), (323, 26), c.A(2, 'Caminho,', 0.4), 'cabeçalho: o selo A Caminho')
    c.hover(TXT('Iniciar Atendimento'), 1.2, at=c.A(2, 'Iniciar', 0.9), label='o cartão Iniciar Atendimento')
    c.hover(MAPA, 2.2, at=c.A(2, 'posição', 0.9), label='a posição do técnico')
    c.mark(3)
    c.hover(TXT('Rota até o cliente'), 1.0, at=c.A(3, 'Rota', 0.9), label='o cartão Rota até o cliente')
    c.hover(MAPA, 0.8, at=c.A(3, 'mapa', 0.9), label='o caminho no mapa')
    c.hover(TXT('min até o cliente'), 3.0, at=c.A(3, 'rótulo', 0.9), label='o rótulo com minutos e quilômetros')
    c.mark(4)
    c.click(BTN('Ampliar mapa'), at=c.A(4, 'Ampliar', 0.7), label='Ampliar o mapa')   # o nome acessível é o aria-label "Ampliar mapa" (o texto "Ampliar" é só o rótulo visível)
    c.waitfor(selector=DLG, timeout=8)
    c.toque(SEL(DLG + ' button', nth=0), f"document.querySelector('{DLG} button')", (360, 30), c.A(4, 'canto', 0.1), 'fecha o mapa em tela cheia')
    c.waitfor(gone={'selector': DLG}, timeout=8)
    c.mark(5)
    c.hover(TXTX('Waze'), 0.2, at=c.A(5, 'Waze', 1.0), label='o botão Waze')   # o 1º gesto depois de fechar o mapa em tela cheia custa ~1,5 s
    c.hover(TXTX('Google Maps'), 0.9, at=c.A(5, 'Google', 0.2), label='o botão Google Maps')
    c.mark(6)
    # 1.38.24: o "Fazer Check-in" fica abaixo da faixa útil (centro em y ~779); o robô rolaria com a roda em cima do mapa, o mapa dava
    # zoom e o passo atrasava 6 s (05/11). A página rola por eval antes, com o botão em y 560
    c.rolar(js_botao('Fazer Check-in'), at=c.A(6, 'técnico', 0.3), y=560, label='a página rola até o Iniciar Atendimento')
    c.hover(BTN('Fazer Check-in'), 2.2, at=c.A(6, 'check-in', 0.8), label='o check-in direto, sem A Caminho')
    c.fim()
    return c


def cap03():
    """Check-in: Fazer Check-in -> status Em Andamento -> carimbo do check-in -> área Checklists (título sem moldura, 1.38.20) e rodapé preto"""
    c = Cap(3, pace=0.4, setup=setup_os(3, ESCOLA))
    c.mark(1)
    c.click(BTN('Fazer Check-in'), at=c.A(1, 'Fazer', 0.6), label='Fazer Check-in')
    c.waitfor(text='Check-in:', timeout=15)
    c.apontar(TXTX('Em Andamento'), (323, 26), c.A(1, 'Andamento.', 0.5), 'cabeçalho: o selo Em Andamento')
    c.mark(2)
    c.hover(TXT('Check-in: 11/11/2026'), 1.6, at=c.A(2, 'carimbo', 0.8), label='o carimbo do check-in')
    c.hover(TXT('Santa Rosa'), 1.6, at=c.A(2, 'endereço', 0.8), label='o endereço do check-in')
    c.mark(3)
    # 1.38.20: "Checklists" é só o título da área (sem moldura nem ícone). A fala diz "área" (L68 nova) ou "cartão" (voz de 1.38.19, ainda no disco)
    c.hover(TXTX('Checklists'), 1.2, at=c.A(3, 'área' if any(norm(w['w']).startswith('area') for w in c.words if w['linha'] == 2) else 'cartão', 0.8), label='a área Checklists')
    c.hover(ACC, 1.4, at=c.A(3, 'checklist', 0.8, nth=1), label='um checklist para cada equipamento')
    c.apontar(BTN('Finalizar OS'), RODAPE['finalizar'], c.A(3, 'Finalizar', 0.3), 'o rodapé: Finalizar OS')
    c.apontar(BTN('Finalizar Parcial'), RODAPE['parcial'], c.A(3, 'Finalizar', 0.3, nth=1), 'o rodapé: Finalizar Parcial')
    c.apontar(MAIS_ACOES, RODAPE['menu'], c.A(3, 'menu', 0.3), 'o rodapé: o menu de mais ações')
    c.fim()
    return c


def cap04():
    """O checklist: acordeão do equipamento -> 5 Sim/Não -> 4 medições -> seleção (Normal) -> lápis -> contador 10 de 13"""
    c = Cap(4, pace=0.4, setup=setup_os(4, ESCOLA))
    c.mark(1)
    c.click(ACC, at=c.A(1, 'Aqui', 0.8), label='abre o acordeão do equipamento')
    c.hover(TXT('Manutenção preventiva de split'), 1.6, at=c.A(1, 'Manutenção', 0.8), label='o checklist do equipamento')
    c.hover(TXTX('0 de 13'), 0.7, at=c.A(1, 'zero', 1.1), label='o contador: 0 de 13')
    c.mark(2)
    c.rolar(js_sel('[role=switch]'), at=c.A(2, 'primeiras', 1.4), y=375, label='as perguntas Sim/Não entram na tela')
    c.hover(TXT('Filtros limpos'), 0.4, at=c.A(2, 'filtros,', 0.8), label='pergunta 1: filtros')
    c.hover(TXT('Serpentinas'), 0.4, at=c.A(2, 'serpentinas,', 0.8), label='pergunta 2: serpentinas')
    c.hover(TXT('Dreno'), 0.4, at=c.A(2, 'dreno,', 0.8), label='pergunta 3: dreno')
    c.hover(TXT('Fixações'), 0.4, at=c.A(2, 'fixações', 0.8), label='pergunta 4: fixações')
    c.hover(TXT('Conexões elétricas'), 0.6, at=c.A(2, 'conexões', 0.8), label='pergunta 5: conexões elétricas')
    c.hover(SEL('main span.text-destructive', nth=0), 1.0, at=c.A(2, 'asterisco', 0.8), label='o asterisco vermelho das obrigatórias')
    c.click(SW, at=c.A(2, 'interruptor,', 0.7), label='interruptor 1 -> Sim')
    c.click(SW, at=c.A(2, 'Sim.', 0.6, nth=1), label='interruptor 2 -> Sim')
    c.mark(3)
    c.click(SW, at=c.A(3, 'celular', 0.0), label='interruptor 3 -> Sim')
    c.click(SW, at=c.A(3, 'gravada', 0.5), label='interruptor 4 -> Sim')
    c.click(SW, at=c.A(3, 'cair', 0.6), label='interruptor 5 -> Sim')
    c.mark(4)
    c.rolar(js_sel("main input[placeholder=\"Digite o valor...\"]"), at=c.A(4, 'Depois', 0.2), y=520, label='as medições entram na tela')
    c.type(INP(0), '7,6', at=c.A(4, 'sete', 0.8), label='corrente do compressor: 7,6', cps=7)
    c.click(INP(1), at=c.A(4, 'pressão', 0.8), label='campo da pressão de baixa')
    c.type(INP(0), '118', at=c.A(4, 'cento', 0.0), label='pressão de baixa: 118', cps=7, noClick=True)
    c.click(INP(1), at=c.A(4, 'alta,', 0.8), label='campo da pressão de alta')
    c.type(INP(0), '345', at=c.A(4, 'trezentos', 0.0), label='pressão de alta: 345', cps=7, noClick=True)
    c.rolar(js_sel("main input[placeholder=\"Digite o valor...\"]", 1), at=c.A(4, 'Por', 1.2), y=520, label='a última medição entra na tela', banda=(380, 740))
    c.click(INP(1), at=c.A(4, 'temperatura', 0.8), label='campo da temperatura de insuflamento')
    c.type(INP(0), '12', at=c.A(4, 'doze', 0.0), label='temperatura de insuflamento: 12', cps=7, noClick=True)
    c.click(TXT('Ruído / vibração anormal?'), at=c.A(4, 'toco', 0.8), label='toca fora do campo: a medição grava')
    c.mark(5)
    c.rolar(js_label('Normal'), at=c.A(5, 'No', 1.3), y=520, label='a pergunta de seleção entra na tela')
    c.click(OPCAO('Normal'), at=c.A(5, 'marco', 0.5), label='marca Normal')
    c.click(LAPIS('last'), at=c.A(5, 'marcar', 0.9), label='lápis: reabre as opções')
    c.click(FECHAR_EDICAO, at=c.A(5, 'opção.', 0.4), label='fecha a edição')
    c.mark(6)
    c.rolar(js_sel("main button[title='Editar resposta']", 8), at=c.A(6, 'Uma', 0.3), y=540, label='o lápis da medição entra na tela')
    c.click(LAPIS(8), at=c.A(6, 'lápis.', 1.0), label='lápis da temperatura: muda a resposta')
    c.click(FECHAR_EDICAO, at=c.A(6, 'contador', 0.7), label='fecha a edição')
    c.hover(TXTX('10 de 13'), 1.6, at=c.A(6, 'dez', 1.0), label='o contador: 10 de 13')
    c.fim()
    return c


def cap05():
    """Fotos e vídeo: Tirar Foto e Galeria -> sobe pela galeria (barra de progresso, toast, miniatura, lixeira) -> texto das recomendações"""
    c = Cap(5, pace=0.4, setup=setup_os(5, ESCOLA, checklist=True, depois=[
        {'do': 'eval', 'js': js_rolar(js_label('Galeria', 'main label'), 560)}, {'do': 'eval', 'js': SLOW_UPLOAD}, {'do': 'pause', 'seconds': 0.5}]))
    c.mark(1)
    c.hover(TIRAR_FOTO, 1.0, at=c.A(1, 'Tirar', 0.8), label='o botão Tirar Foto')
    c.hover(GALERIA, 1.4, at=c.A(1, 'Galeria', 0.8), label='o botão Galeria')
    c.mark(2)
    c.upload(GALERIA, FOTO, at=c.A(2, 'sobe', 0.9), label='escolhe a foto pela galeria')
    c.hover(SEL("img[src*='os-photos']"), 1.4, at=c.A(2, 'miniatura', 0.8), label='a miniatura na pergunta')
    c.hover(SEL("button[title='Remover foto']"), 1.2, at=c.A(2, 'lixeira,', 0.8), label='a lixeira')
    c.mark(3)
    c.rolar(js_sel('main textarea'), at=c.A(3, 'antes', 0.3), y=520, label='o campo de texto entra na tela')
    c.mark(4)
    c.hover(SEL('main textarea'), 1.2, at=c.A(4, 'Recomendações', 0.8), label='a pergunta Recomendações ao cliente')
    c.type(SEL('main textarea'), 'Repetir em seis meses.', at=c.A(4, 'escreve', 0.8), label='escreve a recomendação', cps=12)
    c.click(TXT('Assinatura do cliente'), at=c.A(4, 'fora', 0.8), label='toca fora do campo: a resposta fica salva')
    c.fim()
    return c


def cap06():
    """Consumir do estoque: menu -> Consumir do estoque -> Limpa-evaporador (2) -> Fita isolante (1) -> lista -> Fechar -> menu"""
    c = Cap(6, pace=0.4, setup=setup_os(6, ESCOLA))
    c.mark(1)
    c.toque(MAIS_ACOES, EXPR_MENU, RODAPE['menu'], c.A(1, 'menu', 0.0), 'o menu de mais ações')
    c.click(BTN('Consumir do estoque'), at=c.A(1, 'Consumir', 0.7), label='Consumir do estoque')
    c.waitfor(text='Anote o que você usou', timeout=10)
    c.mark(2)
    c.hover(TXT('só baixa quando a OS for finalizada'), 3.0, at=c.A(2, 'estoque', 0.8), label='a janela explica: só baixa na finalização')
    c.mark(3)
    c.click(SEL('#os-consumption-customer-material'), at=c.A(3, 'Material,', 0.8), label='abre o seletor de Material')
    c.type({'selector': "input[placeholder*='Buscar por nome']"}, 'Limpa', at=c.A(3, 'procurar', 0.8), label='busca pelo nome', cps=7)
    c.hover({'role': 'option', 'name': 'Limpa-evaporador'}, 1.0, at=c.A(3, 'disponível', 1.2), label='cada material mostra o que tem disponível')
    c.click({'role': 'option', 'name': 'Limpa-evaporador'}, at=c.A(3, 'Escolho', 0.7), label='escolhe o Limpa-evaporador')
    c.type(SEL('#os-consumption-quantity'), '2', at=c.A(3, 'quantidade,', 0.8), label='quantidade: 2', clear=True)
    c.type(SEL('#os-consumption-notes'), 'Limpeza da serpentina', at=c.A(3, 'observação,', 0.8), label='observação', cps=16)
    c.toque(BTN('Adicionar'), "[...document.querySelectorAll('button')].filter(b=>b.textContent.trim()==='Adicionar')[0]", (288, 808), c.A(3, 'Toco', -1.2), 'Adicionar')   # botão fixo do rodapé da gaveta: fora da faixa do runner
    c.mark(4)
    c.click(SEL('#os-consumption-customer-material'), at=c.A(4, 'Faço', 0.4), label='abre o seletor de Material (2º material)')
    c.click({'role': 'option', 'name': 'Fita isolante'}, at=c.A(4, 'Fita', 0.9), label='escolhe a Fita isolante')
    c.type(SEL('#os-consumption-quantity'), '1', at=c.A(4, 'rolo.', 1.4), label='quantidade: 1', clear=True)
    c.toque(BTN('Adicionar'), "[...document.querySelectorAll('button')].filter(b=>b.textContent.trim()==='Adicionar')[0]", (288, 808), c.A(4, 'Os', -0.7), 'Adicionar')
    c.hover(TXT('Já registrado nesta OS'), 1.6, at=c.A(4, 'lista', -0.3), label='a lista Já registrado nesta OS')
    c.hover({'selector': "button[aria-label*='ditar' i]", 'nth': 0}, 0.6, at=c.A(4, 'editar', 0.8), label='editar o material')
    c.hover({'selector': "button[aria-label*='emover' i]", 'nth': 0}, 0.6, at=c.A(4, 'remover.', 0.8), label='remover o material')
    c.mark(5)
    c.toque(BTN('Fechar', nth='last'), "[...document.querySelectorAll('button')].filter(b=>b.textContent.trim()==='Fechar').pop()", (104, 808), c.A(5, 'Toco', -0.9), 'Fechar')
    c.toque(MAIS_ACOES, EXPR_MENU, RODAPE['menu'], c.A(5, 'libera', 0.2), 'o menu de mais ações')
    c.hover(BTN('Consumir do estoque'), 0.9, at=c.A(5, 'opção', 0.8), label='a opção liberada no menu')
    c.fim()
    return c


def cap07():
    """Pausar e retomar: menu -> Pausar OS -> selo Pausada -> rodapé só com Retomar OS -> Retomar OS"""
    c = Cap(7, pace=0.4, setup=setup_os(7, ESCOLA))
    c.mark(1)
    c.toque(MAIS_ACOES, EXPR_MENU, RODAPE['menu'], c.A(1, 'menu', 0.0), 'o menu de mais ações')
    c.click(BTN('Pausar OS'), at=c.A(1, 'Pausar', 0.7), label='Pausar OS')
    c.waitfor(text='Retomar OS', timeout=15)
    c.apontar(TXTX('Pausada'), (323, 26), c.A(1, 'Pausada,', 0.5), 'cabeçalho: o selo Pausada')
    c.hover(TXT('Retome o atendimento'), 2.4, at=c.A(1, 'avisa', 0.8), label='o aviso: retome para continuar o preenchimento')
    c.mark(2)
    c.apontar(BTN('Retomar OS'), RODAPE['retomar'], c.A(2, 'rodapé', 0.1), 'o rodapé só tem Retomar OS')
    c.hover(TXTX('Checklists'), 2.6, at=c.A(2, 'Tudo', 0.8), label='tudo o que foi preenchido continua salvo')
    c.mark(3)
    c.toque(BTN('Retomar OS'), js_botao('Retomar OS'), RODAPE['retomar'], c.A(3, 'Retomar', 0.0), 'Retomar OS')
    c.waitfor(text='Finalizar Parcial', timeout=15)
    c.fim()
    return c


def cap08():
    """Finalizar parcialmente: Finalizar Parcial -> confirmação -> Agenda (OS pausadas) -> Ver detalhes -> Preencher OS -> Retomar OS"""
    c = Cap(8, pace=0.4, setup=setup_os(8, ESCOLA))
    c.mark(1)
    c.apontar(BTN('Finalizar Parcial'), RODAPE['parcial'], c.A(1, 'Finalizar', 0.3), 'o rodapé: Finalizar Parcial')
    c.toque(BTN('Finalizar Parcial'), js_botao('Finalizar Parcial'), RODAPE['parcial'], c.A(1, 'Ele', 0.0), 'Finalizar Parcial')
    c.waitfor(text='Finalizar parcialmente?', timeout=10)
    c.hover(TXT('ficará marcada como Parcialmente Concluída'), 3.0, at=c.A(1, 'marcada', 1.0), label='a confirmação: Parcialmente Concluída')
    c.hover(TXT('O que você já preencheu'), 1.8, at=c.A(1, 'preenchido', 1.0), label='o que já foi preenchido fica salvo')
    c.mark(2)
    c.click(BTN('Finalizar Parcialmente'), at=c.A(2, 'Finalizar', 0.7), label='Finalizar Parcialmente')
    c.waitfor(text='OS pausadas', timeout=20)
    c.mark(3)
    c.click({'role': 'button', 'name': 'OS pausadas'}, at=c.A(3, 'pausadas,', 0.9), label='abre a lista OS pausadas')
    c.hover(TXT('Pausada há'), 1.8, at=c.A(3, 'tempo', 0.8), label='o tempo que faz que a OS parou')
    c.click(BTN('Ver detalhes', nth=0), at=c.A(3, 'Ver', 0.7), label='Ver detalhes')
    c.click(BTN('Preencher OS'), at=c.A(3, 'Preencher', 0.7), label='Preencher OS')
    c.waitfor(text='Glacial Cold Brasil', timeout=20)
    c.apontar(TXT('Parcialmente Concluída'), (323, 26), c.A(3, 'Parcialmente', 0.3), 'cabeçalho: o selo Parcialmente Concluída')
    c.mark(4)
    c.toque(BTN('Retomar OS'), js_botao('Retomar OS'), RODAPE['retomar'], c.A(4, 'Retomar', 0.0), 'Retomar OS')
    c.waitfor(text='Finalizar Parcial', timeout=15)
    c.fim()
    return c


def cap09():
    """A assinatura do cliente: pergunta obrigatória -> desenha com o dedo -> Limpar, Confirmar, Tela cheia -> Confirmar -> Concluído -> lápis"""
    c = Cap(9, pace=0.4, setup=setup_os(9, ESCOLA, checklist=True, depois=[
        {'do': 'eval', 'js': js_rolar(js_sel('main canvas'), 520)}, {'do': 'pause', 'seconds': 0.5}]))
    c.mark(1)
    c.hover(TXT('Assinatura do cliente'), 1.4, at=c.A(1, 'assinatura', 0.8), label='a pergunta Assinatura do cliente')
    c.hover(SEL('main span.text-destructive', nth='last'), 1.4, at=c.A(1, 'obrigatória:', 1.0), label='o asterisco: obrigatória')
    c.mark(2)
    c.type(SEL('main canvas'), '', at=c.A(2, 'Quando', 0.5), noClick=True, label='o campo da assinatura')
    c.ev(js_assinar(assinatura(), (1500, 800)), at=c.A(2, 'Quando', 0.4), label='o cliente assina com o dedo')
    c.hover(BTN('Limpar'), 0.6, at=c.A(2, 'Limpar,', 0.8), label='o botão Limpar')
    c.hover(BTN('Confirmar'), 0.9, at=c.A(2, 'Confirmar.', 0.8), label='o botão Confirmar')
    c.hover(TXT('Tela cheia'), 1.6, at=c.A(2, 'Tela', 0.8, nth=1), label='o botão Tela cheia')
    c.mark(3)
    c.click(BTN('Confirmar'), at=c.A(3, 'Confirmar,', 0.7), label='Confirmar a assinatura')
    c.hover(TXT('Concluído'), 1.4, at=c.A(3, 'Concluído.', 0.8), label='o checklist do equipamento: Concluído')
    c.click(LAPIS('last'), at=c.A(3, 'lápis.', 0.9), label='lápis: rever a assinatura')
    c.fim()
    return c


def cap10():
    """Finalizar a OS: Finalizar OS -> Resumo do consumo -> ajusta a fita para 2 rolos -> Confirmar e finalizar -> Relatório de Serviço"""
    c = Cap(10, pace=0.4, setup=setup_os(10, ESCOLA))
    c.mark(1)
    c.toque(BTN('Finalizar OS'), js_botao('Finalizar OS'), RODAPE['finalizar'], c.A(1, 'Finalizar', 0.0, nth=1), 'Finalizar OS')
    c.waitfor(text='Resumo do consumo', timeout=15)
    c.hover(TXT('Limpa-evaporador em spray'), 1.2, at=c.A(1, 'que', 0.8), label='o que vai sair do estoque')
    c.hover(TXT('Fica com'), 1.4, at=c.A(1, 'quanto', 0.8), label='quanto fica de cada material')
    c.mark(2)
    c.type(SEL("input[aria-label='Quantidade: Fita isolante']"), '2', at=c.A(2, 'mudar', 0.9), label='a fita isolante foi de 2 rolos', clear=True)
    c.hover(TXT('Fica com 28'), 1.6, at=c.A(2, 'saldo', 0.8), label='o saldo que fica já se atualiza')
    c.mark(3)
    c.click(BTN('Confirmar e finalizar'), at=c.A(3, 'Confirmar', 0.7), label='Confirmar e finalizar')
    c.waitfor(text='Relatório de Serviço', timeout=25)
    c.fim()
    return c


def cap11():
    """O relatório e o PDF: topo -> Execução (check-in, check-out, duração) -> respostas, foto e assinatura -> rodapé (Baixar PDF, menu)"""
    c = Cap(11, pace=0.4, setup=setup_agenda(11, ESCOLA) + abrir_relatorio() + fim_setup(11))
    c.mark(1)
    c.apontar(SEL('h1'), (196, 82), c.A(1, 'número', 0.9), 'o número da OS')   # cabeçalho fixo (y 82)
    c.hover(TXTX('Colégio Monte Verde'), 0.4, at=c.A(1, 'cliente', 0.9), label='o cliente')
    c.hover(TXT('Hi-Wall 18.000 BTUs'), 0.4, at=c.A(1, 'equipamento', 0.9), label='o equipamento atendido')
    # 05/11: os títulos do relatório são <h3> com ícone (não são "folhas"): o js_label não os achava ("SEM ALVO" já em 03/11) e a
    # L3 ficava 11 s parada em Execução, sem mostrar respostas, foto e assinatura. Agora rola pelo <h3> e pela imagem.
    H3 = lambda t: f"[...document.querySelectorAll('main h3, h3')].find(e=>e.textContent.trim().toLowerCase()==={json.dumps(t.lower())})"
    c.mark(2)
    c.rolar(H3('Execução'), at=c.A(2, 'Execução', 1.5), y=330, label='a seção Execução entra na tela')
    c.hover(TXTX('CHECK-IN'), 0.4, at=c.A(2, 'check-in', 0.8), label='o check-in')
    c.hover(TXTX('CHECK-OUT'), 1.0, at=c.A(2, 'check-out,', 0.8), label='o check-out')
    c.hover(TXT('Duração:'), 2.6, at=c.A(2, 'duração', 0.8), label='a duração do atendimento')
    c.mark(3)
    c.rolar(H3('Checklists por equipamento'), at=c.A(3, 'respostas', 1.0), y=260, dur_ms=900, label='as respostas do checklist')
    # a foto da resposta (a última imagem visível do armazenamento de fotos; a primeira do DOM fica fora da lista de respostas)
    c.rolar("[...document.querySelectorAll(\"img[src*='os-photos']\")].filter(i=>i.getClientRects().length&&i.offsetParent).pop()",
            at=c.A(3, 'foto', 0.9), y=470, dur_ms=1000, label='a foto que o técnico anexou')
    c.rolar(H3('Assinaturas'), at=c.A(3, 'assinatura', 0.9), y=330, dur_ms=900, label='a seção Assinaturas')
    c.hover(SEL("img[alt='Assinatura do cliente']"), 1.4, at=c.A(3, 'data,', 0.6), label='a assinatura do cliente, com data, hora e local')
    c.mark(4)
    c.apontar(BTN('Baixar PDF'), RODAPE['pdf'], c.A(4, 'Baixar', 0.4), 'o rodapé: Baixar PDF')
    c.toque(BTN('Baixar PDF'), js_botao('Baixar PDF'), RODAPE['pdf'], c.A(4, 'gera', 0.0), 'Baixar PDF')
    c.toque(MAIS_ACOES, EXPR_MENU, RODAPE['menu'], c.A(4, 'menu', 0.0), 'o menu de mais ações')
    c.hover(TXTX('Copiar Link'), 0.6, at=c.A(4, 'Copiar', 0.8), label='o Copiar Link')
    c.hover(TXTX('Imprimir'), 0.8, at=c.A(4, 'Imprimir.', 0.8), label='o Imprimir')
    c.mark(5)
    c.fim()
    return c


def cap12():
    """O link do cliente: Copiar Link -> visão do cliente (sem login) -> pesquisa abre sozinha -> nota 10, estrelas, nome, comentário -> Enviar"""
    c = Cap(12, pace=0.4, setup=[
        *setup_agenda(12, ESCOLA), *abrir_relatorio(),
        {'do': 'eval', 'js': js_pesquisa('t7/pesquisa-oculta')}, *fim_setup(12)])
    c.mark(1)
    c.toque(MAIS_ACOES, EXPR_MENU, RODAPE['menu'], c.A(1, 'menu', 0.0), 'o menu de mais ações')
    c.click(TXTX('Copiar Link'), at=c.A(1, 'Copiar', 0.7), label='Copiar Link')
    c.mark(2)
    c.goto(f'/os-tecnico/{OS16}?modo=cliente', at=c.A(2, 'abre', 1.2), label='o cliente abre o link (sem login)')
    c.waitfor(text='Relatório de Serviço', timeout=20)
    c.apontar(TXTX('Glacial Cold Brasil'), (196, 56), c.A(2, 'empresa,', 0.3), 'cabeçalho: o nome da empresa')
    c.apontar(SEL('h1'), (196, 82), c.A(2, 'número', 0.3), 'cabeçalho: o número da OS')
    c.apontar(TXTX('Concluída'), (323, 26), c.A(2, 'status', 0.3), 'cabeçalho: o status Concluída')
    c.hover(TXT('Relatório de Serviço'), 1.4, at=c.A(2, 'relatório', 0.8), label='o mesmo relatório do técnico')
    c.apontar(BTN('Baixar PDF'), RODAPE['pdf'], c.A(2, 'botão', 0.3), 'o botão Baixar PDF')
    c.mark(3)
    c.ev(js_pesquisa('t7/pesquisa-visivel'), at=c.A(3, 'abre', 1.0), label='a avaliação do cliente passa a valer')
    c.ev(JS_VISIBILIDADE, label='o app refaz a leitura do link')
    c.waitfor(text='Como foi seu atendimento?', timeout=15)
    c.hover(SEL('[role=slider]'), 1.0, at=c.A(3, 'nota', 0.8), label='a escala de 0 a 10')
    c.hover(TXT('Qualidade'), 1.0, at=c.A(3, 'estrelas', 0.8), label='as estrelas de cada critério')
    # (sem passar o dedo pelos campos nome/comentário: o tempo da linha 4 é do arrasto, das estrelas e da digitação)
    c.mark(4, at=c.A(4, 'Preencho', 1.5))
    c.ev(js_marcador_slider(), at=c.A(4, 'Preencho', 2.0), label='destino do arrasto da nota')
    # o arrasto começa ~1,5 s antes de "Preencho" e solta perto de "dez": a linha 4 cabe nos 8 s da fala
    c.drag(SEL('[role=slider]'), {'selector': '#__wp1'}, at=c.A(4, 'Preencho', 1.5), label='arrasta a nota até 10')
    c.click({'role': 'button', 'name': 'Qualidade: 5 de 5 estrelas', 'exact': True}, at=c.A(4, 'cinco', 0.8), label='5 estrelas em Qualidade')
    c.click({'role': 'button', 'name': 'Pontualidade: 5 de 5 estrelas', 'exact': True}, at=c.A(4, 'estrelas', 0.7), label='5 estrelas em Pontualidade')
    c.click({'role': 'button', 'name': 'Profissionalismo: 5 de 5 estrelas', 'exact': True}, at=c.A(4, 'cada', 0.8), label='5 estrelas em Profissionalismo')
    c.type(SEL("input[placeholder*='nome' i]"), 'Helena', at=c.A(4, 'nome', 1.4), label='o nome', cps=14)
    c.type(SEL('textarea'), 'Pontual!', at=c.A(4, 'comentário,', 0.5), label='o comentário', cps=16)
    # o botão Enviar fica no rodapé fixo da janela (y ~ 808, fora da faixa do runner): toque sintético com anel
    c.toque(BTN('Enviar avaliação'), js_botao('Enviar avaliação'), (256, 808), c.A(4, 'Enviar', -0.7), 'Enviar avaliação')
    c.waitfor(text='Obrigado', timeout=15)
    c.mark(5)
    c.fim()
    return c


def cap13():
    """Recapitulando: base simples (a OS #16 na tela, com o botão da Área do Técnico); os trechos da recapitulação entram na edição"""
    c = Cap(13, pace=0.4, setup=setup_os(13, ESCOLA))
    # 1.38.21: a voz ganhou a L4 do Editar OS (inserção antes do "Próximo"); o "No próximo tutorial" passou a ser a última linha (L5)
    nl = len(c.linhas)
    for i in range(1, nl + 1):
        c.mark(i)
    c.apontar(SEL('h1'), (196, 82), c.A(nl, 'tutorial,', 1.0), 'a OS #16')
    c.apontar(FAB, FAB_PT, c.A(nl, 'Área', 0.8), 'o botão redondo da Área do Técnico')
    c.fim()
    return c


def cap14():
    """Editar OS (1.38.20/21): OS de bastidor da Pousada Sol Nascente (checklist SEM equipamento, 5 respostas). Menu -> Editar OS -> Adicionar
    equipamento (criação rápida: Hi-Wall 12.000 BTUs - Sala de café, Local, Tensão 220 V) -> arrasta o checklist para o equipamento -> Salvar -> Fechar -> respostas mantidas -> aba Data e horários.
    Remendo: parte de `t7/inicio-editar-os` (não entra na cadeia apos-capNN; a OS #16 não é tocada). Exibido depois do cap12 e antes do cap13."""
    # o cartão de 60 min é baixo (56 px): o TEXTO transborda para cima do cartão das 09:00; clicar no cartão (a caixa), não no texto
    ALVO_CARD = {'selector': 'main div.cursor-pointer', 'hasText': 'Pousada Sol Nascente', 'nth': 0}
    DRAWER = {'selector': DLG}
    setup = setup_agenda(14, ESCOLA) + [
        {'do': 'click', 'target': ALVO_CARD}, {'do': 'waitFor', 'text': 'Resumo da OS', 'timeout': 10},
        {'do': 'click', 'target': BTN('Preencher OS')}, {'do': 'waitFor', 'text': 'Glacial Cold Brasil', 'timeout': 20},
        {'do': 'waitFor', 'idle': True}, {'do': 'pause', 'seconds': 0.8},
        {'do': 'eval', 'js': js_rolar(js_label('Checklists'), 300)}, {'do': 'pause', 'seconds': 0.6}] + fim_setup(14)
    c = Cap(14, pace=0.4, setup=setup)
    # 05/11 (voz real, 131,2 s, app 1.38.24): âncoras do texto final ("e o local", sem "repito"), passos na ordem da fala, cadastro
    # rápido mais enxuto (nome em cps 20, a gaveta rola até o Local por eval) e a aba "Data e horários" nova enquadrada
    DLG_IN = lambda t: {'text': t, 'exact': True, 'within': '[role=dialog]'}   # a gaveta (ResponsiveModal/vaul) não tem aria-modal
    c.mark(1)
    c.hover(TXTX('Checklists'), 1.0, at=c.A(1, 'ordem', 0.8), label='a área Checklists')
    c.hover(TXTX('Pousada Sol Nascente'), 1.0, at=c.A(1, 'Pousada', 0.8), label='o cliente: Pousada Sol Nascente')
    c.hover(TXT('Manutenção preventiva de split'), 1.4, at=c.A(1, 'checklist', 0.8), label='o checklist solto, sem equipamento')
    c.mark(2)
    c.toque(MAIS_ACOES, EXPR_MENU, RODAPE['menu'], c.A(2, 'menu', 0.0), 'o menu de mais ações')
    c.hover(BTN('Editar OS'), 0.4, at=c.A(2, 'ações.', 0.0), label='a opção Editar OS no menu')
    c.click(BTN('Editar OS'), at=c.A(2, 'Editar', 0.6), label='Editar OS')
    c.waitfor(text='Estrutura da OS', timeout=10)
    c.hover(TXTX('Estrutura da OS'), 1.0, at=c.A(2, 'gaveta', 0.8), label='a gaveta Editar OS: Estrutura da OS')
    c.hover(TXT('As respostas acompanham o checklist'), 1.0, at=c.A(2, 'gestor', 0.8), label='o texto: as respostas acompanham o checklist')
    c.mark(3)
    c.hover(TXTX('Checklists sem equipamento'), 1.0, at=c.A(3, 'bloco', 0.8), label='o bloco Checklists sem equipamento')
    c.hover(TXT('Respondido'), 1.0, at=c.A(3, 'visto', 0.8), label='o visto: o checklist já tem respostas')
    c.hover(TXTX('Nenhum equipamento'), 1.0, at=c.A(3, 'equipamento', 0.8, nth=1), label='a ordem ainda não tem equipamento')
    c.mark(4)
    c.click(BTN('Adicionar equipamento'), at=c.A(4, 'Adicionar', 0.7), label='Adicionar equipamento')
    c.waitfor(text='Novo Equipamento', timeout=10)
    c.type(SEL("input[placeholder='Nome do equipamento']"), 'Hi-Wall 12.000 BTUs - Sala de café', at=c.A(4, 'nome', 1.0), label='o nome do equipamento', cps=20)
    # o Local fica ~600 px abaixo do Nome: a gaveta rola por eval (o robô rolaria com a roda, ~1,5 s)
    LOCAL = "document.querySelector(\"[role=dialog] input[placeholder='Local']\")"
    c.ev(js_rolar_em(LOCAL, 470, 450), at=c.A(4, 'local.', 0.75), label='a gaveta rola até o Local')
    c.click(SEL("input[placeholder='Local']"), at=c.A(4, 'local.', 0.3), label='o campo Local')
    c.type(SEL("input[placeholder='Local']"), 'Sala de café', at=c.A(4, 'local.', -0.4), label='Local: Sala de café', cps=40, noClick=True)
    # "Tensão *" é campo obrigatório do cadastro de equipamento deste mundo (T3): sem ele o "Criar" não grava
    c.click({'selector': 'button[role=combobox]', 'nth': 'last'}, at=c.A(4, 'obrigatória', -0.2), label='abre a Tensão')
    c.click({'role': 'option', 'name': '220 V'}, at=c.A(4, 'duzentos', 0.0), label='escolhe 220 V')
    c.toque(BTN('Criar'), js_botao('Criar'), (340, 811), c.A(4, 'Criar', 0.3), 'Criar o equipamento')
    c.waitfor(text='Hi-Wall 12.000 BTUs - Sala de café', timeout=10)
    c.mark(5)
    c.hover(BTN('Selecionar checklists'), 1.0, at=c.A(5, 'escolher', 0.8), label='Selecionar checklists')
    c.hover(BTN('Remover equipamento'), 1.0, at=c.A(5, 'remover', 0.8), label='Remover equipamento')
    c.mark(6)
    ALCA = {'role': 'button', 'name': 'Arrastar checklist Manutenção preventiva de split', 'exact': True}
    c.hover(ALCA, 1.4, at=c.A(6, 'Seguro', 0.6), label='a alça do checklist')
    # pega em "arrasto até o Hi-Wall", chega ao cartão logo antes de "O cartão acende" e fica ~3,7 s: "Solte aqui para vincular" na tela
    # durante a frase que o descreve; solta logo antes de "Solto" (com a voz real, o hold de 1,5 s soltaria no meio de "mostra Solte aqui")
    c.drag(ALCA, {'selector': 'section', 'hasText': 'Hi-Wall 12.000 BTUs - Sala de café'},
           at=c.A(6, 'arrasto', 0.1), label='arrasta o checklist até o Hi-Wall', hold=3.7)
    c.mark(7)
    c.click(BTN('Ações do checklist'), at=c.A(7, 'três', 0.8), label='Ações do checklist')
    c.hover(TXTX('Mover para'), 1.2, at=c.A(7, 'Mover', 0.8), label='o menu: Mover para')
    c.ev("document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}))", at=c.A(7, 'destino', 0.2), label='fecha o menu sem escolher')
    c.mark(8)
    c.toque(BTN('Salvar equipamentos e checklists'), js_botao('Salvar equipamentos e checklists'), (195, 808), c.A(8, 'Salvar', 0.2), 'Salvar equipamentos e checklists')
    c.waitfor(text='OS atualizada', timeout=10)
    c.hover(TXT('acompanhou'), 1.6, at=c.A(8, 'avisa', 0.3), label='o aviso: OS atualizada, respostas acompanharam', optional=True)
    c.mark(9)
    c.toque(BTN('Fechar'), js_botao('Fechar'), (360, 30), c.A(9, 'Fecho', 0.3), 'Fechar a gaveta')
    c.waitfor(gone=DRAWER, timeout=8)
    c.hover(TXTX('Checklists'), 0.8, at=c.A(9, 'agora', 0.8), label='a área Checklists: agora dentro do Hi-Wall')
    c.click({'text': 'Hi-Wall 12.000 BTUs - Sala de café', 'within': 'main'}, at=c.A(9, 'Hi-Wall', 0.6), label='abre o acordeão do Hi-Wall')
    c.hover(TXTX('5 de 13'), 1.4, at=c.A(9, 'cinco', 0.4, nth=1), label='as cinco respostas continuam: 5 de 13')
    c.mark(10)
    c.toque(MAIS_ACOES, EXPR_MENU, RODAPE['menu'], c.A(10, 'aba', 1.2), 'o menu de mais ações')
    c.click(BTN('Editar OS'), at=c.A(10, 'Data', 1.0), label='Editar OS de novo')
    c.click({'role': 'tab', 'name': 'Data e horários'}, at=c.A(10, 'Data', 0.3), label='a aba Data e horários')
    c.hover(TXTX('Período da OS'), 1.2, at=c.A(10, 'remarca', 0.7), label='Período da OS')
    c.hover(DLG_IN('Data inicial'), 0.6, at=c.A(10, 'data,', 0.8, nth=1), label='as datas da OS')
    # 1.38.24: "Adicionar outra data" e "Adicionar dia" entram entre "Horário de cada dia" e o cartão do dia; a gaveta rola até o
    # cartão do dia (Início e Fim) e a câmera pega a aba nova inteira, sem tocar
    INICIO = "[...document.querySelectorAll('[role=dialog] label')].find(e=>e.textContent.trim()==='Início')"
    c.ev(js_rolar_em(INICIO, 640, 600), at=c.A(10, 'início', 0.5), label='a gaveta rola até o horário do dia')
    c.hover(DLG_IN('Início'), 1.6, at=c.A(10, 'fim', 0.6), label='o início e o fim de cada dia')
    c.fim()
    return c


CAPS = {0: cap00, 1: cap01, 2: cap02, 3: cap03, 4: cap04, 5: cap05, 6: cap06, 7: cap07, 8: cap08, 9: cap09, 10: cap10, 11: cap11,
        12: cap12, 13: cap13, 14: cap14}

if __name__ == '__main__':
    quais = [int(a) for a in sys.argv[1:]] or sorted(CAPS)
    for n in quais:
        c = CAPS[n]()
        if os.environ.get('ANCHORS'):
            for i, w, t in c.anchors:
                print(f'   anchor L{i} "{w}" -> {t}')
        d = c.out()
        last = -1
        for st in d['steps']:
            if 'at' in st:
                if st['at'] < last:
                    print(f'  aviso cap{n:02d}: at {st["at"]} < {last} em "{st.get("label") or st.get("name")}"')
                last = max(last, st['at'])
        path = os.path.join(HERE, f'cap{n:02d}.json')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
        print(f'cap{n:02d}: {len(d["steps"])} passos, narração {c.dur:.1f} s -> {os.path.relpath(path, HERE)}')
