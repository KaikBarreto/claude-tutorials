#!/usr/bin/env python3
"""T18 · gera os roteiros de EXPLORAÇÃO (rec/t18/_ex/*.json) para rec/t18/explorar.mjs. Rodar: python3 -I rec/t18/_ex/gerar_ex.py"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
CAD = json.load(open(os.path.join(HERE, '..', 'cadeia.json'), encoding='utf8'))
STORAGE = {'dominex:portal-tickets-seen:d40f5787-1779-501f-900c-ddb2b90a36e5': '2031-01-01T00:00:00.000Z'}

# despejo compacto dos elementos interativos visíveis de <main>: tag|papel|texto|placeholder|aria-label|id|valor|x,y WxH
DUMP = ("(()=>{const q=[...document.querySelectorAll('main input,main textarea,main button,main [role=switch],main [role=tab],"
        "main [role=combobox],main [role=slider],main select,main a[href]')];return q.filter(e=>e.getClientRects().length).map(e=>{"
        "const r=e.getBoundingClientRect();return [e.tagName.toLowerCase(),e.getAttribute('role')||'',(e.innerText||'').replace(/\\s+/g,' ').trim().slice(0,38),"
        "e.placeholder||'',e.getAttribute('aria-label')||'',e.id||'',(e.value==null?'':String(e.value)).slice(0,12),"
        "Math.round(r.x)+','+Math.round(r.y)+' '+Math.round(r.width)+'x'+Math.round(r.height)].join('|')})})()")


def dump(raiz='main'):
    """igual ao DUMP, mas para outra raiz (ex.: [role=dialog] ou [data-radix-popper-content-wrapper])"""
    return DUMP.replace('main ', raiz + ' ').replace("'main input", "'" + raiz + " input")


def S(**kw):
    return kw


def nova(nome, passos, start='/dashboard', **extra):
    d = {'seedExtra': CAD['inicio'], 'storage': STORAGE, 'start': start, 'stopOnFail': False, 'steps': passos}
    d.update(extra)
    json.dump(d, open(os.path.join(HERE, nome + '.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print(nome, len(passos), 'passos')


BADGE = lambda nome: {'selector': 'main button', 'hasText': nome}
ITEM = lambda nome: {'selector': '[cmdk-item]', 'hasText': nome}
LINK = lambda n: {'role': 'link', 'name': n, 'exact': True}
BTN = lambda n: {'role': 'button', 'name': n, 'exact': True}

# ------------------------------------------------------------------ ex1: menu, segmento, Início, glossário
ex1 = [
    S(do='waitFor', text='Olá, Camila!', timeout=25),
    S(do='shot', name='a00-dashboard'),
    S(do='click', target=LINK('Área do Técnico™')),
    S(do='waitFor', text='Termos Técnicos Explicados', timeout=20),
    S(do='wait', ms=1500),
    S(do='shot', name='a01-inicio'),
    S(do='eval', js=DUMP, max=9000),
    S(do='text', selector='main', name='texto do Início', max=2500),
    S(do='click', target=BADGE('Refrigeração e Climatização')),
    S(do='wait', ms=600),
    S(do='shot', name='a02-nichos'),
    S(do='list', selector='[cmdk-item]'),
    S(do='click', target=ITEM('Energia Solar')),
    S(do='wait', ms=800),
    S(do='shot', name='a03-solar'),
    S(do='text', selector='main', name='texto da prévia', max=1500),
    S(do='eval', js=DUMP, max=5000),
    S(do='click', target=BADGE('Energia Solar')),
    S(do='wait', ms=500),
    S(do='click', target=ITEM('Refrigeração e Climatização')),
    S(do='wait', ms=800),
    S(do='shot', name='a04-volta'),
    S(do='click', target={'selector': 'nav button', 'hasText': 'Início'}),
    S(do='wait', ms=800),
    S(do='scrolly', by=700),
    S(do='shot', name='a05-glossario'),
    S(do='type', target={'placeholder': 'Buscar termo (ex: BTU, capacitor, pressão)'}, text='capacitor'),
    S(do='wait', ms=600),
    S(do='shot', name='a06-busca-capacitor'),
    S(do='list', selector='main [data-state] button'),
    S(do='click', target={'selector': 'main button', 'hasText': 'Capacitor (µF'}),
    S(do='wait', ms=700),
    S(do='shot', name='a07-termo-aberto'),
    S(do='text', selector='main', name='texto com o termo aberto', max=2500),
    S(do='type', target={'placeholder': 'Buscar termo (ex: BTU, capacitor, pressão)'}, text=''),
    S(do='wait', ms=600),
    S(do='shot', name='a08-grupos'),
    S(do='list', selector='main h3, main h2'),
    S(do='click', target={'selector': 'main button', 'hasText': 'Elétrica e Instalação'}),
    S(do='wait', ms=700),
    S(do='shot', name='a09-grupo-aberto'),
]
nova('ex1', ex1)

# ------------------------------------------------------------------ ex2: Agenda -> OS #9 -> botão redondo -> overlay -> Conversão -> Voltar para OS
ex2 = [
    S(do='goto', url='/agenda'),
    S(do='waitFor', text='Visualize e gerencie os agendamentos', timeout=25),
    S(do='wait', ms=1200),
    S(do='shot', name='b00-agenda'),
    S(do='list', selector='main [role=tab]'),
    S(do='text', selector='main', name='texto da agenda', max=2500),
    S(do='click', target={'text': '#9', 'within': 'main', 'exact': True}),
    S(do='wait', ms=1000),
    S(do='shot', name='b01-resumo'),
    S(do='text', selector='[role=dialog], main', name='painel', max=1800),
    S(do='click', target={'role': 'button', 'name': 'Preencher OS', 'exact': True}),
    S(do='waitFor', text='Glacial Cold Brasil', timeout=25),
    S(do='wait', ms=2500),
    S(do='shot', name='b02-os'),
    S(do='eval', js="(()=>{const q=[...document.querySelectorAll('button,a')].filter(e=>e.getClientRects().length&&/cnico/i.test(e.getAttribute('aria-label')||''));return q.map(e=>{const r=e.getBoundingClientRect();return [e.tagName,e.getAttribute('aria-label'),Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height)].join('|')})})()", max=1500),
    S(do='eval', js="document.documentElement.scrollHeight+' x '+window.innerHeight+' x '+window.innerWidth"),
    S(do='eval', js="(()=>{const b=[...document.querySelectorAll('button')].find(e=>/cnico/i.test(e.getAttribute('aria-label')||''));if(!b)return 'SEM';b.click();return 'clicado'})()"),
    S(do='wait', ms=3000),
    S(do='shot', name='b03-overlay'),
    S(do='eval', js="(()=>{const q=[...document.querySelectorAll('button')].filter(e=>e.getClientRects().length);return q.map(e=>{const r=e.getBoundingClientRect();return [(e.innerText||'').trim().slice(0,30),e.getAttribute('aria-label')||'',Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height)].join('|')}).slice(0,60)})()", max=5000),
    S(do='eval', js="(()=>{const cs=[...document.querySelectorAll('canvas')].map(c=>{const r=c.getBoundingClientRect();return Math.round(r.x)+','+Math.round(r.y)+' '+Math.round(r.width)+'x'+Math.round(r.height)});return cs})()"),
    S(do='click', target={'selector': 'button', 'hasText': 'Conversão'}),
    S(do='wait', ms=1200),
    S(do='shot', name='b04-conversao-na-os'),
    S(do='click', target={'selector': 'button', 'hasText': 'Voltar para OS'}),
    S(do='wait', ms=1500),
    S(do='shot', name='b05-voltou'),
    S(do='eval', js="(()=>{const q=[...document.querySelectorAll('button')].filter(e=>e.getClientRects().length&&/cnico/i.test(e.getAttribute('aria-label')||''));return q.map(e=>{const r=e.getBoundingClientRect();return [e.getAttribute('aria-label'),Math.round(r.x),Math.round(r.y)].join('|')})})()"),
    S(do='text', selector='body', name='texto da OS', max=1500),
]
nova('ex2', ex2, start='/dashboard')


# ------------------------------------------------------------------ ex3: Catálogo (Ar Condicionado, marca, modelo, consumo, códigos de erro, manual)
CAT = '/area-tecnico/catalogo'
BUSCA = {'placeholder': 'Buscar por marca, equipamento ou código de erro'}
ex3 = [
    S(do='goto', url=CAT),
    S(do='waitFor', text='Catálogo - Ar Condicionado', timeout=25),
    S(do='wait', ms=1500),
    S(do='shot', name='c00-catalogo'),
    S(do='eval', js=DUMP, max=9000),
    S(do='text', selector='main', name='texto do catálogo', max=1800),
    S(do='click', target=BUSCA),
    S(do='type', target=BUSCA, text='E1'),
    S(do='wait', ms=1200),
    S(do='shot', name='c01-busca-e1'),
    S(do='text', selector='main', name='texto da busca E1', max=3500),
    S(do='eval', js=DUMP, max=9000),
    S(do='type', target=BUSCA, text=''),
    S(do='wait', ms=800),
    S(do='click', target={'role': 'button', 'name': 'Filtros'}),
    S(do='wait', ms=900),
    S(do='shot', name='c02-filtros'),
    S(do='text', selector='[role=dialog]', name='texto do diálogo Filtros', max=2500),
    S(do='eval', js=dump('[role=dialog]'), max=9000),
    S(do='click', target={'selector': '[role=dialog] button, [role=dialog] label, [role=dialog] [role=checkbox]', 'hasText': '18.000'}),
    S(do='wait', ms=600),
    S(do='shot', name='c03-filtro-18000'),
    S(do='click', target={'role': 'button', 'name': 'Ver resultados'}),
    S(do='wait', ms=1200),
    S(do='shot', name='c04-resultados-18000'),
    S(do='text', selector='main', name='texto dos resultados', max=2500),
    S(do='eval', js=DUMP, max=9000),
    S(do='click', target={'role': 'button', 'name': 'Filtros'}),
    S(do='wait', ms=700),
    S(do='shot', name='c05-filtros-de-novo'),
    S(do='click', target={'role': 'button', 'name': 'Limpar filtros'}),
    S(do='wait', ms=700),
    S(do='shot', name='c06-limpou'),
    S(do='eval', js=DUMP, max=9000),
]

ex3b = [
    S(do='goto', url=CAT),
    S(do='waitFor', text='Catálogo - Ar Condicionado', timeout=25),
    S(do='wait', ms=1000),
    S(do='click', target={'selector': 'main button, main a, main [role=button]', 'hasText': 'Aerovento'}),
    S(do='wait', ms=1500),
    S(do='shot', name='d00-aerovento'),
    S(do='text', selector='main', name='texto da marca Aerovento', max=3500),
    S(do='eval', js=DUMP, max=9000),
    S(do='scrolly', by=300),
    S(do='shot', name='d01-aerovento-rolou'),
    S(do='click', target={'selector': 'main button', 'hasText': 'Ajustar', 'nth': 2}),
    S(do='wait', ms=900),
    S(do='shot', name='d02-ajustar'),
    S(do='text', selector='[role=dialog]', name='diálogo Tarifa e uso', max=1500),
    S(do='eval', js=dump('[role=dialog]'), max=5000),
    S(do='eval', js="(()=>{const s=document.querySelector('[role=dialog] [role=slider]');if(!s)return 'SEM SLIDER';return [s.getAttribute('aria-valuenow'),s.getAttribute('aria-valuemin'),s.getAttribute('aria-valuemax'),document.activeElement===s]})()"),
    S(do='type', target={'selector': '[role=dialog] input'}, text='0,95'),
    S(do='eval', js="(()=>{const s=document.querySelector('[role=dialog] [role=slider]');s.focus();return document.activeElement===s})()"),
    S(do='press', key='ArrowRight'),
    S(do='press', key='ArrowRight'),
    S(do='press', key='ArrowRight'),
    S(do='wait', ms=500),
    S(do='shot', name='d03-ajustado'),
    S(do='eval', js="(()=>{const s=document.querySelector('[role=dialog] [role=slider]');return [s.getAttribute('aria-valuenow')]})()"),
    S(do='click', target={'role': 'button', 'name': 'Aplicar'}),
    S(do='wait', ms=900),
    S(do='shot', name='d04-aplicado'),
    S(do='list', selector='main button'),
]

ex3c = [
    S(do='goto', url=CAT),
    S(do='waitFor', text='Catálogo - Ar Condicionado', timeout=25),
    S(do='click', target={'selector': 'main button, main a, main [role=button]', 'hasText': 'Aerovento'}),
    S(do='wait', ms=1500),
    S(do='click', target={'selector': 'main button', 'hasText': 'Códigos de erro', 'nth': 2}),
    S(do='wait', ms=1300),
    S(do='shot', name='e00-codigos'),
    S(do='text', selector='main', name='texto da tela Códigos de erro', max=3500),
    S(do='eval', js=DUMP, max=9000),
    S(do='type', target={'placeholder': 'Informe o código de erro no display'}, text='E1'),
    S(do='wait', ms=1000),
    S(do='shot', name='e01-codigo-e1'),
    S(do='text', selector='main', name='texto com E1', max=3500),
    S(do='eval', js=DUMP, max=9000),
    S(do='click', target={'selector': 'main button, main [role=button]', 'hasText': 'E1', 'nth': 0}),
    S(do='wait', ms=900),
    S(do='shot', name='e02-codigo-aberto'),
    S(do='text', selector='main', name='texto do código aberto', max=3500),
    S(do='eval', js="(()=>{const q=[...document.querySelectorAll('button')].filter(e=>e.getClientRects().length&&/voltar|back/i.test((e.innerText||'')+(e.getAttribute('aria-label')||'')));return q.map(e=>(e.innerText||'').trim()+'|'+(e.getAttribute('aria-label')||''))})()"),
]

# ------------------------------------------------------------------ ex3d: outras abas do Catálogo
ex3d = [
    S(do='goto', url=CAT),
    S(do='waitFor', text='Catálogo - Ar Condicionado', timeout=25),
    S(do='click', target={'role': 'tab', 'name': 'Compressores'}),
    S(do='wait', ms=1500),
    S(do='shot', name='f00-compressores'),
    S(do='text', selector='main', name='texto Compressores', max=1500),
    S(do='click', target={'selector': 'main button, main a, main [role=button]', 'hasText': 'Nortec'}),
    S(do='wait', ms=1300),
    S(do='shot', name='f01-nortec'),
    S(do='text', selector='main', name='texto Nortec', max=2500),
    S(do='eval', js=DUMP, max=6000),
    S(do='click', target={'selector': 'main button', 'hasText': 'Ficha técnica', 'nth': 1}),
    S(do='wait', ms=1300),
    S(do='shot', name='f02-ficha'),
    S(do='text', selector='main', name='texto da ficha', max=3000),
    S(do='click', target={'role': 'tab', 'name': 'Linha Branca'}),
    S(do='wait', ms=1500),
    S(do='shot', name='f03-linha-branca'),
    S(do='click', target={'selector': 'main button, main a, main [role=button]', 'hasText': 'Brisamar'}),
    S(do='wait', ms=1300),
    S(do='shot', name='f04-brisamar'),
    S(do='text', selector='main', name='texto Brisamar', max=3000),
    S(do='click', target={'role': 'tab', 'name': 'Controles Remotos'}),
    S(do='wait', ms=1500),
    S(do='shot', name='f05-controles'),
    S(do='text', selector='main', name='texto Controles', max=2000),
    S(do='click', target={'selector': 'main button', 'hasText': 'Ver detalhes técnicos', 'nth': 0}),
    S(do='wait', ms=1300),
    S(do='shot', name='f06-detalhes-controle'),
    S(do='text', selector='main', name='texto detalhes do controle', max=2500),
    S(do='click', target={'role': 'tab', 'name': 'Fluidos Refrigerantes'}),
    S(do='wait', ms=1500),
    S(do='shot', name='f07-fluidos'),
    S(do='text', selector='main', name='texto Fluidos', max=2500),
    S(do='click', target={'selector': 'main button, main a, main [role=button]', 'hasText': 'R-32', 'nth': 0}),
    S(do='wait', ms=1300),
    S(do='shot', name='f08-r32'),
    S(do='text', selector='main', name='texto do R-32', max=3000),
]
nova('ex3', ex3 + ex3b + ex3c + ex3d, start=CAT)

# ------------------------------------------------------------------ ex4: as calculadoras (um `goto` por ferramenta)
TA = '/area-tecnico/'
def ferramenta(slug, espera, nome, extra=()):
    return [S(do='goto', url=TA + slug), S(do='waitFor', text=espera, timeout=25), S(do='wait', ms=900),
            S(do='shot', name=nome + '-0'), S(do='eval', js=DUMP, max=7000), *extra]

CAMPO = lambda n: {'label': n, 'exact': True}
ex4 = []
ex4 += ferramenta('carga-termica', 'Dimensione a capacidade em BTUs do ambiente.', 'g1', [
    S(do='type', target=CAMPO('Altura (metros)'), text='2,8'),
    S(do='type', target=CAMPO('Largura (metros)'), text='4'),
    S(do='type', target=CAMPO('Comprimento (metros)'), text='5'),
    S(do='type', target=CAMPO('Quantidade de pessoas'), text='4'),
    S(do='type', target=CAMPO('Eletroeletrônicos'), text='3'),
    S(do='type', target=CAMPO('Janelas (2 x 1,5 metros)'), text='1'),
    S(do='wait', ms=500), S(do='shot', name='g1-1'),
    S(do='text', selector='main', name='carga térmica', max=1500),
    S(do='click', target={'role': 'button', 'name': 'TR', 'exact': True}), S(do='wait', ms=400), S(do='shot', name='g1-2'),
    S(do='click', target={'role': 'button', 'name': 'BTU', 'exact': True}),
    S(do='click', target={'role': 'switch', 'name': 'Ambiente ensolarado?'}), S(do='wait', ms=400), S(do='shot', name='g1-3'),
    S(do='eval', js="[...document.querySelectorAll('main p')].map(e=>e.innerText.trim()).filter(t=>/BTU|TR|aparelho|Recomenda/.test(t)).slice(0,8)"),
])
ex4 += ferramenta('conversao', 'Converta entre unidades de medida.', 'g2', [
    S(do='type', target={'placeholder': '0', 'exact': True, 'nth': 0}, text='10', ),
    S(do='wait', ms=500), S(do='shot', name='g2-1'),
    S(do='eval', js="[...document.querySelectorAll('main input')].filter(e=>e.getClientRects().length).map(e=>e.value)"),
    S(do='click', target={'role': 'button', 'name': 'Inverter unidades'}), S(do='wait', ms=400), S(do='shot', name='g2-2'),
    S(do='eval', js="[...document.querySelectorAll('main input')].filter(e=>e.getClientRects().length).map(e=>e.value)"),
    S(do='click', target={'role': 'button', 'name': 'HP → BTU/h'}), S(do='wait', ms=500), S(do='shot', name='g2-3'),
    S(do='eval', js="[...document.querySelectorAll('main input')].filter(e=>e.getClientRects().length).map(e=>e.value)"),
    S(do='eval', js=DUMP, max=5000),
    S(do='type', target={'placeholder': '0', 'exact': True, 'nth': 0}, text='2', clear=True),
    S(do='wait', ms=400), S(do='shot', name='g2-4'),
    S(do='click', target={'role': 'button', 'name': 'Energia'}), S(do='wait', ms=400), S(do='shot', name='g2-5'),
    S(do='eval', js="[...document.querySelectorAll('main input')].filter(e=>e.getClientRects().length).map(e=>e.value)"),
    S(do='click', target={'role': 'button', 'name': 'mm → pol'}), S(do='wait', ms=500),
    S(do='type', target={'placeholder': '0', 'exact': True, 'nth': 0}, text='6,35', clear=True), S(do='wait', ms=400), S(do='shot', name='g2-6'),
    S(do='eval', js="[...document.querySelectorAll('main input')].filter(e=>e.getClientRects().length).map(e=>e.value)"),
    S(do='click', target={'role': 'button', 'name': 'Favoritar conversão'}), S(do='wait', ms=500), S(do='shot', name='g2-7'),
    S(do='text', selector='main', name='conversão com favorita', max=1200),
])
ex4 += ferramenta('calculo-capacitor', 'Cálculo de Capacitor', 'g3', [
    S(do='click', target={'selector': 'main button[role=combobox]', 'nth': 0}), S(do='wait', ms=500), S(do='shot', name='g3-1'),
    S(do='list', selector='[role=option]'),
    S(do='click', target={'role': 'option', 'name': '18.000 BTUs'}), S(do='wait', ms=600), S(do='shot', name='g3-2'),
    S(do='text', selector='main', name='capacitor', max=1500),
    S(do='eval', js="[...document.querySelectorAll('main img, main [role=img]')].map(e=>(e.alt||e.getAttribute('aria-label')||'')+'|'+Math.round(e.getBoundingClientRect().x)+','+Math.round(e.getBoundingClientRect().y)+' '+Math.round(e.getBoundingClientRect().width)+'x'+Math.round(e.getBoundingClientRect().height))"),
    S(do='eval', js=DUMP, max=5000),
    S(do='click', target={'selector': 'main img', 'nth': 0}), S(do='wait', ms=700), S(do='shot', name='g3-3'),
    S(do='eval', js=dump('[role=dialog]'), max=3000),
    S(do='press', key='Escape'), S(do='wait', ms=500),
    S(do='click', target={'role': 'button', 'name': 'Preciso (LRA)'}), S(do='wait', ms=500),
    S(do='eval', js=DUMP, max=4000),
    S(do='type', target={'placeholder': 'Ex: 40'}, text='30'), S(do='wait', ms=500), S(do='shot', name='g3-4'),
    S(do='text', selector='main', name='capacitor LRA', max=1200),
    S(do='click', target={'role': 'button', 'name': 'Trifásico'}), S(do='wait', ms=600), S(do='shot', name='g3-5'),
    S(do='text', selector='main', name='capacitor trifásico', max=2500),
    S(do='eval', js=DUMP, max=5000),
])
ex4 += ferramenta('cabo-eletrico', 'Seleção de seção do cabo elétrico', 'g4', [
    S(do='click', target={'selector': 'main button[role=combobox]', 'nth': 0}), S(do='wait', ms=500),
    S(do='click', target={'role': 'option', 'name': '18.000 BTUs'}), S(do='wait', ms=500),
    S(do='click', target={'role': 'button', 'name': '220V', 'exact': True}),
    S(do='type', target={'placeholder': 'Ex: 40'}, text='20'), S(do='wait', ms=600), S(do='shot', name='g4-1'),
    S(do='text', selector='main', name='cabo 20 m', max=1500),
    S(do='type', target={'placeholder': 'Ex: 40'}, text='30', clear=True), S(do='wait', ms=600), S(do='shot', name='g4-2'),
    S(do='text', selector='main', name='cabo 30 m', max=1500),
])
ex5 = []
ex5 += ferramenta('superaquecimento', 'Calcule SH e SC pela pressão e temperatura medidas em campo.', 'g5', [
    S(do='click', target={'selector': 'main button[role=combobox]', 'nth': 0}), S(do='wait', ms=600), S(do='shot', name='g5-1'),
    S(do='list', selector='[role=option]'),
    S(do='click', target={'role': 'option', 'name': 'Padrão'}), S(do='wait', ms=500), S(do='shot', name='g5-2'),
    S(do='type', target={'placeholder': 'Ex: 120'}, text='118'),
    S(do='type', target={'placeholder': 'Ex: 12'}, text='12'), S(do='wait', ms=600), S(do='shot', name='g5-3'),
    S(do='text', selector='main', name='SH 118/12', max=2500),
    S(do='type', target={'placeholder': 'Ex: 120'}, text='125', clear=True),
    S(do='type', target={'placeholder': 'Ex: 12'}, text='15', clear=True), S(do='wait', ms=600), S(do='shot', name='g5-4'),
    S(do='click', target={'role': 'button', 'name': 'Subresfriamento (SC)'}), S(do='wait', ms=500),
    S(do='type', target={'placeholder': 'Ex: 120'}, text='350'),
    S(do='type', target={'placeholder': 'Ex: 12'}, text='35'), S(do='wait', ms=600), S(do='shot', name='g5-5'),
    S(do='text', selector='main', name='SC 350/35', max=2500),
    S(do='eval', js=DUMP, max=5000),
])
ex5 += ferramenta('regua-gases', 'Pressão de saturação dos refrigerantes por temperatura.', 'g6', [
    S(do='eval', js="(()=>{const s=document.querySelector('[role=slider]');const k=s&&s.querySelector('div.border-primary');const r=x=>{if(!x)return null;const b=x.getBoundingClientRect();return [Math.round(b.x),Math.round(b.y),Math.round(b.width),Math.round(b.height)]};return {slider:r(s),knob:r(k),now:s&&s.getAttribute('aria-valuenow')}})()"),
    S(do='text', selector='main', name='régua', max=1500),
    S(do='type', target={'label': 'Pressão em PSI (g)'}, text='150'), S(do='wait', ms=600), S(do='shot', name='g6-1'),
    S(do='eval', js="[...document.querySelectorAll('main input')].filter(e=>e.getClientRects().length).map(e=>e.getAttribute('aria-label')+'='+e.value)"),
    S(do='drag', target={'selector': '[role=slider] div.border-primary'}, to={'x': 760, 'y': 260}, steps=30), S(do='shot', name='g6-2'),
    S(do='eval', js="(()=>{const s=document.querySelector('[role=slider]');return s.getAttribute('aria-valuenow')})()"),
    S(do='drag', target={'selector': '[role=slider] div.border-primary'}, to={'x': 760, 'y': 600}, steps=30), S(do='shot', name='g6-3'),
    S(do='eval', js="(()=>{const s=document.querySelector('[role=slider]');return s.getAttribute('aria-valuenow')})()"),
    S(do='click', target={'role': 'button', 'name': 'bar', 'exact': True}), S(do='wait', ms=500), S(do='shot', name='g6-4'),
    S(do='click', target={'selector': 'main button[role=combobox]', 'nth': 0}), S(do='wait', ms=500), S(do='shot', name='g6-5'),
    S(do='list', selector='[role=option]'),
    S(do='click', target={'role': 'option', 'name': 'R-404A'}), S(do='wait', ms=600), S(do='shot', name='g6-6'),
    S(do='eval', js=DUMP, max=5000),
    S(do='click', target={'role': 'button', 'name': 'Bubble'}), S(do='wait', ms=500), S(do='shot', name='g6-7'),
    S(do='click', target={'role': 'button', 'name': 'Dew'}), S(do='wait', ms=400),
    S(do='click', target={'selector': 'main button[role=combobox]', 'nth': 0}), S(do='wait', ms=500),
    S(do='click', target={'role': 'option', 'name': 'R-32'}), S(do='wait', ms=700), S(do='shot', name='g6-8'),
    S(do='eval', js="[...document.querySelectorAll('main svg')].filter(e=>e.getClientRects().length).map(e=>(e.getAttribute('class')||'').slice(0,60)+'|'+Math.round(e.getBoundingClientRect().x)+','+Math.round(e.getBoundingClientRect().y)).slice(0,25)", max=3000),
])
ex5 += ferramenta('retrofit-gas', 'Gases drop-in para trocar o refrigerante', 'g7', [
    S(do='eval', js=DUMP, max=3000),
    S(do='click', target={'selector': 'main button[role=combobox]', 'nth': 0}), S(do='wait', ms=500), S(do='shot', name='g7-1'),
    S(do='list', selector='[role=option]'),
    S(do='click', target={'role': 'option', 'name': 'R-22'}), S(do='wait', ms=600), S(do='shot', name='g7-2'),
    S(do='text', selector='main', name='retrofit R-22', max=2500),
    S(do='click', target={'role': 'button', 'name': 'bar', 'exact': True}), S(do='wait', ms=500), S(do='shot', name='g7-3'),
    S(do='click', target={'role': 'button', 'name': 'psi', 'exact': True}),
    S(do='click', target={'selector': 'main button[role=combobox]', 'nth': 0}), S(do='wait', ms=500),
    S(do='click', target={'role': 'option', 'name': 'R-404A'}), S(do='wait', ms=700), S(do='shot', name='g7-4'),
])
ex5 += ferramenta('ciclo-refrigeracao', 'Entenda como o gás circula pelo sistema e o que cada componente faz.', 'g8', [
    S(do='wait', ms=1500), S(do='shot', name='g8-1'),
    S(do='click', target={'role': 'button', 'name': 'Imagem 2D'}), S(do='wait', ms=900), S(do='shot', name='g8-2'),
    S(do='click', target={'role': 'button', 'name': 'Ilustração'}), S(do='wait', ms=900),
    S(do='click', target={'selector': 'main button', 'hasText': 'Compressor'}), S(do='wait', ms=700), S(do='shot', name='g8-3'),
    S(do='click', target={'selector': 'main button', 'hasText': 'Evaporador'}), S(do='wait', ms=700), S(do='shot', name='g8-4'),
])
ex5 += ferramenta('diluicao-produto', 'Diluição de Produto', 'g9', [
    S(do='type', target={'placeholder': '10', 'exact': True}, text='10', clear=True),
    S(do='type', target={'placeholder': 'Ex: 500'}, text='500'), S(do='wait', ms=600), S(do='shot', name='g9-1'),
    S(do='text', selector='main', name='diluição', max=1800),
    S(do='click', target={'role': 'button', 'name': 'L', 'exact': True}), S(do='wait', ms=500), S(do='shot', name='g9-2'),
    S(do='click', target={'role': 'button', 'name': 'mL', 'exact': True}),
    S(do='click', target={'role': 'button', 'name': 'Tenho X de produto'}), S(do='wait', ms=500),
    S(do='type', target={'placeholder': 'Ex: 50'}, text='50'), S(do='wait', ms=600), S(do='shot', name='g9-3'),
    S(do='text', selector='main', name='tenho X', max=1800),
])
nova('ex4', ex4, start='/area-tecnico')
nova('ex5', ex5, start='/area-tecnico')
