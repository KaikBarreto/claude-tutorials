#!/usr/bin/env python3
"""T20 · cap15 (Recapitulando): montagem de trechos das gravações finais dos outros capítulos (rec/t20/t20-capNN.mp4), um bloco por linha da
fala (narracao/cap15.json), do jeito que o roteiro pede ("Montagem rápida: ..."). Nada é desenhado: só telas reais do app, cortadas de
passos pelo RÓTULO do actions.json (tStart + deslocamento). Cada trecho tem a duração da fatia da linha (velocidade normal, nada
acelerado) e entra/sai com um fade de 0,12 s. Última linha: o fim da conciliação (cap15) parado, com o aviso "Próximo" feito na edição.
Saída: rec/t20/t20-cap15.mp4 + .actions.json (sem passos) + .telemetry.json (um ponto, o cursor fica escondido no specs/chapter).
uso: python3 -I rec/t20/t20_montagem_cap15.py     (pesado: rode pela fila, rec/fila.sh --prio 20 --)"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TUT = os.path.normpath(os.path.join(HERE, '..', '..'))
NARR = json.load(open(os.path.join(TUT, 't20/narracao/cap15.json')))
CAUDA = 0.8
FADE = 0.12
# (capítulo, rótulo do passo (começa com), deslocamento em relação ao início do passo)
BLOCOS = [
    [('01', 'plano geral do portal', -0.8), ('02', 'Copiar', -0.8)],
    [('03', 'Aba Histórico', -0.6), ('03', 'A4', -0.8), ('04', 'Senha (pontinhos)', -0.8)],
    [('05', 'Aba Histórico: Livre', -0.8), ('07', 'Fundição Bandeira do Vale', -0.6), ('08', 'confere Saldo Atual R$ 0,00 Em dia', -0.8), ('09', 'confere NF-e 1250', -0.8), ('09', 'Mês passado', -0.6)],
    [('10', 'Seus materiais', -0.6), ('11', 'Solicitar coleta (enviar)', -0.8), ('12', 'clica na impressora', -0.8)],
    [('13', 'a mensagem do WhatsApp', -0.5), ('14', 'Fotos (carrossel)', -0.8)],
    [('14', '[ZOOM] Total R$ 3.700,00', -0.4)],   # último: parado (o aviso "Próximo" entra no specs)
]


def passo(cap, rot):
    a = json.load(open(os.path.join(HERE, f't20-cap{cap}.actions.json')))
    for x in a['actions']:
        if (x.get('label') or '').startswith(rot):
            return x['tStart'], a['video']['durationS']
    sys.exit(f'cap{cap}: passo "{rot}" não achado')


def main():
    L = NARR['linhas']
    total = round(NARR['dur'] + CAUDA, 3)
    ini = [l['s'] for l in L] + [total]
    ini[0] = 0.0
    entradas, filtros, fim = [], [], 0
    k = 0
    for i, bloco in enumerate(BLOCOS):
        janela = round(ini[i + 1] - ini[i], 3)
        par = round(janela / len(bloco), 3)
        for j, (cap, rot, off) in enumerate(bloco):
            t0, dur = passo(cap, rot)
            t0 = max(0.0, t0 + off)
            dur_clip = par
            if i == len(BLOCOS) - 1:   # último bloco: 3 s reais e o resto é o último quadro parado
                dur_clip = 3.0
            t0 = min(t0, dur - dur_clip - 0.05)
            entradas += ['-ss', f'{t0:.3f}', '-t', f'{dur_clip:.3f}', '-i', os.path.join(HERE, f't20-cap{cap}.mp4')]
            f = f'[{k}:v]setpts=PTS-STARTPTS,fps=30,format=yuv420p'
            if i == len(BLOCOS) - 1:
                f += f',tpad=stop_mode=clone:stop_duration={janela - dur_clip + 0.05:.3f}'
            f += f',fade=t=in:st=0:d={FADE},fade=t=out:st={par - FADE if i < len(BLOCOS) - 1 else janela - FADE:.3f}:d={FADE}[v{k}]'
            filtros.append(f)
            k += 1
    n = k
    fc = ';'.join(filtros) + ';' + ''.join(f'[v{x}]' for x in range(n)) + f'concat=n={n}:v=1:a=0,trim=duration={total:.3f},setpts=PTS-STARTPTS[o]'
    out = os.path.join(HERE, 't20-cap15.mp4')
    tmp = '/dev/shm/t20_cap15_tmp.mp4'
    cmd = ['ffmpeg', '-nostdin', '-v', 'error', '-y'] + entradas + ['-filter_complex', fc, '-map', '[o]', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18',
           '-pix_fmt', 'yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv', '-r', '30', tmp]
    subprocess.run(cmd, check=True)
    subprocess.run(['mv', tmp, out], check=True)
    pr = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'json', out], capture_output=True, text=True).stdout)
    d = round(float(pr['format']['duration']), 3)
    video = {'width': 2880, 'height': 1620, 'fps': 30, 'durationS': d, 'dsf': 1.8, 'viewportCss': {'width': 1600, 'height': 900},
             'file': 't20-cap15.mp4', 'codec': 'h264 yuv420p bt709/tv'}
    json.dump({'script': 'montagem', 'name': 't20-cap15', 'video': video, 'actions': [], 'marks': [], 'late': {'count': 0, 'maxS': 0.0}, 'pageIssues': {}},
              open(os.path.join(HERE, 't20-cap15.actions.json'), 'w'), ensure_ascii=False, indent=1)
    json.dump({'video': video, 'samples': [{'t': 0, 'x': 1440, 'y': 810, 'type': 'move', 'cursor': 'arrow', 'src': 'inicio'},
                                           {'t': d, 'x': 1440, 'y': 810, 'type': 'move', 'cursor': 'arrow', 'src': 'fim'}]},
              open(os.path.join(HERE, 't20-cap15.telemetry.json'), 'w'))
    print(f'cap15: {n} trechos, {d} s -> {out}')


if __name__ == '__main__':
    main()
