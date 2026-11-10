#!/usr/bin/env python3
"""JSON do capítulo 9:16 com a tela real do celular (gravação 390x844 a 2x = 780x1688) a partir dos rótulos do robô.
uso: python3 montar_cap_celular.py 01   -> caps/cap01.9x16.chapter.json   (spec: CELULAR[nn] abaixo; rótulos = os de rec/t0v2/cap01-p.json)
Zoom = recorte de largura total (780 px = 2,4x na janela 936 px) e altura 780*1160/936 = 967 px, centrado no alvo e preso à tela."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); DOMI = os.path.dirname(os.path.dirname(HERE)); REC = os.path.join(DOMI, 'rec', 't0v2')
NARR = os.path.join(DOMI, 't0v2', 'narracao'); CW, CH, SH = 780, 967, 1688
# 03/11: sem destaque nem zoom em 'Tem no seu plano' no celular (a gaveta Ver trilha fica atrás do player, z-index; ver relatório): o alvo caía na legenda do player.
CELULAR = {'01': {
  # opção (b), 03/11: a gaveta "Ver trilha" abre atrás do player (z-index) e não aparece; nenhum toque nela. Lista de módulos da página inicial, aula CRM e Kanban, progresso e menu.
  'zooms': [('Formação básica', None, 0.6), ('Na sequência do seu plano', None, 0.6), ('Conheça este módulo', None, 0.6), ('selo Não tem no seu plano', None, 0.6),
            ('botão Escolher meu plano', None, 0.6), ('Materiais e extras', None, 0.6), ('Trilha do seu plano 43%', None, 0.8), ('Próxima recomendada', None, 0.6),
            ('abre o Menu', None, 0.6), ('Tutoriais | Domiflix', None, 0.8)],
  'spots': [('Formação básica', 'Formação básica'), ('Na sequência do seu plano', 'Na sequência do seu plano'), ('Conheça este módulo', 'Conheça este módulo'),
            ('selo Não tem no seu plano', 'Não tem no seu plano'), ('botão Escolher meu plano', 'Escolher meu plano'), ('Materiais e extras', 'Materiais e extras'),
            ('Trilha do seu plano 43%', 'Trilha do seu plano'), ('Próxima recomendada', 'Próxima recomendada'), ('Tutoriais | Domiflix', 'Tutoriais | Domiflix')],
  'ilustracoes': [{'at': 0.0, 'dur': 4.8, 'src': os.path.join(REC, 'ilus', 'cena06_9x16.mp4'), 'box': [0, 0, 1080, 1920], 'radius': 0, 'shadow': False, 'scale_in': 0.0}]}}
def passo(acts, rot):
    m = [a for a in acts if a.get('label') == rot and a.get('ok', True)]
    if not m: raise SystemExit(f'rótulo {rot!r} não achado nas ações do celular')
    return m[0]
def recorte(rects):
    y0 = min(r['y'] for r in rects); y1 = max(r['y'] + r['h'] for r in rects); cy = (y0 + y1) / 2
    if y1 - y0 > CH: print(f'AVISO: alvo mais alto que a janela ({y1 - y0:.0f} > {CH})')
    y = min(max(0, cy - CH / 2), SH - CH); return [0, round(y), CW, CH]
def montar(nn):
    base = os.path.join(REC, f't0v2-cap{nn}-p'); A = json.load(open(base + '.actions.json')); acts = [a for a in A['actions'] if a.get('ok', True)]
    narr = json.load(open(os.path.join(NARR, f'cap{nn}.json'))); dur = float(A['video']['durationS']); sp = CELULAR[nn]
    ch = {'name': f'cap{nn}', 'video': base + '.mp4', 'telemetry': base + '.telemetry.json', 'narration': os.path.join(narr['pasta'], 'audio48k.wav'), 'audio_offset': 0.0,
          'trim': {'start': 0.0, 'end': round(min(dur, narr['dur'] + 0.8), 3)}, 'camera': {'auto': True, 'depth': 2.3}, 'cursor': {'show': False, 'touch': True, 'ring_alpha': 0.7, 'size': 2.8},
          'stage': {'bg': os.path.join(HERE, 'assets', 'fundo_escuro_9x16.png'), 'shadow': 0.35}, 'zooms': [], 'spots': [], 'callouts': [], 'illustrations': sp['ilustracoes'],
          'output': {'dir': os.path.join(HERE, 'out', f'cap{nn}_9x16'), 'crf': 18, 'preset': 'veryfast'}}
    for de, ate, fim in sp['zooms']:
        a = passo(acts, de); b = passo(acts, ate or de); i0, i1 = acts.index(a), acts.index(b)
        rs = [x['rect'] for x in acts[i0:i1 + 1] if x.get('rect')]
        if rs: ch['zooms'].append({'at': round(a['tStart'] - 0.2, 3), 'end': round(b['tEnd'] + fim, 3), 'rect': recorte(rs)})
    for rot, texto in sp['spots']:
        a = passo(acts, rot)
        if a.get('rect'): r = a['rect']; ch['spots'].append({'at': round(a.get('tAct', a['tStart']) - 0.9, 3), 'dur': 1.8, 'rect': [r['x'], r['y'], r['w'], r['h']], 'label': texto})
    out = os.path.join(HERE, 'caps', f'cap{nn}.9x16.chapter.json'); json.dump(ch, open(out, 'w'), ensure_ascii=False, indent=1)
    print(f'cap{nn} 9x16: vídeo {dur:.1f} s, narração {narr["dur"]:.1f} s, {len(ch["zooms"])} zooms, {len(ch["spots"])} destaques -> {out}')
if __name__ == '__main__':
    for n in sys.argv[1:]: montar(f'{int(n):02d}')
