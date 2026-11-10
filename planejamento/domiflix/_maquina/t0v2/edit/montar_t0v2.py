#!/usr/bin/env python3
"""T0 v2: monta os JSON de capítulo 16:9 (montar_cap.py) e 9:16 (montar_cap_celular.py) dos capítulos 01 a 06 a partir de uma tabela só
(janelas de ilustração, zooms, destaques e avisos), com vinheta de capítulo (TITULOS/KICKERS). Rode depois das gravações e das ilustrações.
uso: python3 -I montar_t0v2.py   (cap00 é só ilustração e não passa por aqui)
ATENÇÃO (06/11): os caps/capNN.9x16.chapter.json de 02 a 06 foram ajustados à mão depois deste script (chave "_nota_0611" em cada um:
destaques sem rótulo, destaques e câmera novos, aviso do endereço com "y9"). Rodar este script de novo desfaz esses ajustes do 9:16;
cópias de antes em caps/*.9x16.chapter.json.antes_0611."""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); DOMI = os.path.dirname(os.path.dirname(HERE)); REC = os.path.join(DOMI, 'rec', 't0v2')
sys.path.insert(0, os.path.join(DOMI, 't0v2', 'narracao')); sys.path.insert(0, HERE)
import tts_textos as T
ILUS = {1: [(6, 0, 4.8)], 2: [(16, 5.5, 11.2), (17, 10.9, 20.3), (18, 19.7, 29.6)], 3: [(20, 0, 11.6), (22, 14.4, 20.4)],
        4: [], 5: [(29, 0, 8.8), (31, 20.4, 31.7), (32, 31.4, 36.7), (33, 36.3, 43.3)], 6: [(35, 0, 6.7), (36, 6.3, 11.2), (37, 10.8, 14.4)]}
def dur(f): return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]).decode())
def ilus(n, fmt):
    r = []
    for cena, de, ate in ILUS[n]:
        f = os.path.join(REC, 'ilus', f'cena{cena:02d}_{fmt}.mp4')
        r.append({'at': de, 'dur': round(dur(f), 3), 'src': f, 'box': [166, 44, 1587, 992] if fmt == '16x9' else [0, 0, 1080, 1920], 'radius': 0, 'shadow': False, 'scale_in': 0.0})
    return r
def sp(passo, rotulo, antes=0.9): return {'passo': passo, 'antes': antes, 'dur': 1.8, 'rotulo': rotulo}
def z(de, fim='+0.5', ate=None, min_w=1300):
    d = {'de': de, 'fim': fim, 'min_w': min_w}
    if ate: d['ate'] = ate
    return d
D = {  # 16:9: zooms e spots por rótulo; avisos por palavra
 2: dict(zooms=[z('Trilha do seu plano', '+0.6', 'Formação básica %')], spots=[sp('Trilha do seu plano', 'Trilha do seu plano')]),
 3: dict(zooms=[z('botão Tirar dúvidas com o suporte', '+0.5', 'clica Tirar dúvidas com o suporte', 1200), z('busca do guia', '+1.0', None, 1500),
                z('Falar com o Suporte', '+0.8', 'clica Falar com o Suporte', 1000)],
         spots=[sp('botão Tirar dúvidas com o suporte', 'Tirar dúvidas com o suporte'), sp('Falar com o Suporte', 'Falar com o Suporte')],
         callouts=[{'palavra': [2, 'endereço'], 'dur': 3.8, 'texto': 'dominex.app/guia-tecnico', 'pos': 'bottom'}]),
 4: dict(zooms=[z('status', '+0.5', 'valor', 1300), z('botão Pagar Agora', '+0.6', '20% de desconto', 1300)],
         spots=[sp('abre Assinatura', 'Assinatura', 1.0), sp('status', 'Status'), sp('plano', 'Plano'), sp('vencimento', 'Vencimento'), sp('valor', 'Valor mensal'),
                sp('botão Pagar Agora', 'Pagar Agora'), sp('20% de desconto', '20% de desconto no plano anual')]),
 5: dict(zooms=[z('abre Gerenciar Meu Plano', '+0.5', None, 1300), z('aba Personalizado', '+0.5', 'marca CRM / Kanban', 1800)],
         spots=[sp('abre Gerenciar Meu Plano', 'Gerenciar Meu Plano', 1.0), sp('aba Planos Prontos', 'Planos Prontos'), sp('aba Personalizado', 'Personalizado'), sp('marca Cobranças online', 'Cobranças online', 0.6)]),
 6: dict(zooms=[z('marca a caixa', '+0.6', 'botão Confirmar e começar a primeira aula', 1300)],
         spots=[sp('marca a caixa', 'Confirmar os combinados'), sp('botão Confirmar e começar a primeira aula', 'Confirmar e começar a primeira aula')]),
}
CEL = {  # 9:16: (de, ate, fim) e (rótulo, texto)
 2: dict(zooms=[('Trilha do seu plano', None, 0.8)], spots=[('Trilha do seu plano', 'Trilha do seu plano')]),
 3: dict(zooms=[('botão Tirar dúvidas com o suporte', 'clica Tirar dúvidas com o suporte', 0.5), ('busca do guia', None, 1.0), ('Falar com o Suporte', 'clica Falar com o Suporte', 0.8)],
         spots=[('botão Tirar dúvidas com o suporte', 'Tirar dúvidas com o suporte'), ('Falar com o Suporte', 'Falar com o Suporte')]),
 4: dict(zooms=[('status', 'valor', 0.5), ('botão Pagar Agora', '20% de desconto', 0.6)],
         spots=[('status', 'Status'), ('plano', 'Plano'), ('vencimento', 'Vencimento'), ('valor', 'Valor mensal'), ('botão Pagar Agora', 'Pagar Agora'), ('20% de desconto', '20% de desconto no plano anual')]),
 5: dict(zooms=[('abre Gerenciar Meu Plano', None, 0.5), ('marca Cobranças online', 'marca CRM / Kanban', 0.6), ('sobe usuários', 'sobe usuários 2', 0.6)],
         spots=[('abre Gerenciar Meu Plano', 'Gerenciar Meu Plano'), ('aba Planos Prontos', 'Planos Prontos'), ('aba Personalizado', 'Personalizado'), ('marca Cobranças online', 'Cobranças online')]),
 6: dict(zooms=[('marca a caixa', 'botão Confirmar e começar a primeira aula', 0.6)],
         spots=[('marca a caixa', 'Confirmar os combinados'), ('botão Confirmar e começar a primeira aula', 'Confirmar e começar a primeira aula')]),
}
CORTES = {3: [[30.4, 33.95]]}  # recarregamento do app na volta do Guia Técnico (pausa de 3,6 s na voz, tirada do vídeo e do áudio); iguais nos dois formatos
# 1) specs do 16:9
specs = json.load(open(os.path.join(HERE, 'caps', 'specs.json')))
for n in range(1, 7):
    nn = f'{n:02d}'; s = specs.get(nn, {}) if n == 1 else {}
    s.update(titulo=T.TITULOS[n].rstrip('.'), kicker=T.KICKERS[n], ilustracoes=ilus(n, '16x9'), repouso=[[i['at'], round(i['at'] + i['dur'], 2)] for i in ilus(n, '16x9')])
    s.pop('sem_titulo', None)
    if n in CORTES: s['cortes'] = CORTES[n]; s['repouso'] = s['repouso'] + [[CORTES[n][0][0] - 0.4, CORTES[n][0][1] + 0.3]]
    if n > 1: s.update({k: v for k, v in D[n].items()})
    specs[nn] = s
specs.pop('00', None)
json.dump(specs, open(os.path.join(HERE, 'caps', 'specs.json'), 'w'), ensure_ascii=False, indent=1)
import montar_cap, montar_cap_celular as mc
for n in range(1, 7):
    montar_cap.montar(f'{n:02d}')
    if n > 1: mc.CELULAR[f'{n:02d}'] = dict(CEL[n], ilustracoes=ilus(n, '9x16'))
    else: mc.CELULAR['01']['ilustracoes'] = ilus(1, '9x16')
    mc.montar(f'{n:02d}')
    p = os.path.join(HERE, 'caps', f'cap{n:02d}.9x16.chapter.json'); c = json.load(open(p))
    c['card'] = {'kicker': T.KICKERS[n], 'title': T.TITULOS[n].rstrip('.')}
    for co in D.get(n, {}).get('callouts', []):
        nar = json.load(open(os.path.join(DOMI, 't0v2', 'narracao', f'cap{n:02d}.json')))
        t = next(w['s'] for w in nar['words'] if w['linha'] == co['palavra'][0] and w['w'].lower().strip('.,:;!?') == co['palavra'][1])
        c['callouts'].append({'at': round(t, 3), 'dur': co['dur'], 'text': co['texto'], 'pos': 'bottom'})
    if n in CORTES: c['cortes'] = CORTES[n]
    json.dump(c, open(p, 'w'), ensure_ascii=False, indent=1)
print('montado')
