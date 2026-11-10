#!/usr/bin/env python3
"""Cobre, no capítulo vertical já renderizado, cada janela de ilustração (quadro cheio 1080x1920) lida do capNN.9x16.chapter.json
(as ilustrações da tela real do celular não são desenhadas pelo render vertical). Áudio intacto. Uma trava por capítulo.
uso: python3 -I compor_ilus_vertical_multi.py NN"""
import json, os, subprocess, sys, shutil
H = os.path.dirname(os.path.abspath(__file__)); DOMI = os.path.dirname(os.path.dirname(H)); nn = f'{int(sys.argv[1]):02d}'
ch = json.load(open(os.path.join(H, 'caps', f'cap{nn}.9x16.chapter.json'))); il = ch['illustrations']
if not il: print('sem ilustrações'); sys.exit(0)
D = os.path.join(H, 'out', f'cap{nn}_9x16'); V = os.path.join(D, f'cap{nn}.mp4'); B = os.path.join(D, f'.sem_ilus_cap{nn}.mp4')
if os.path.exists(B): os.remove(B)  # o render acabou de gerar V sem ilustração: a base é sempre ele (base velha reaproveitava o render anterior)
os.link(V, B)
cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-i', B]
for i in il: cmd += ['-itsoffset', str(i['at']), '-i', i['src']]
f = ''; last = '0:v'
for k, i in enumerate(il, 1):
    f += f"[{last}][{k}:v]overlay=0:0:enable='between(t,{i['at']},{i['at'] + i['dur']})':eof_action=pass[v{k}];"; last = f'v{k}'
cmd += ['-filter_complex', f.rstrip(';'), '-map', f'[{last}]', '-map', '0:a?', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-movflags', '+faststart', os.path.join(D, f'.novo_cap{nn}.mp4')]
subprocess.run(['flock', os.path.join(DOMI, '.heavy.lock'), 'nice', '-n', '10'] + cmd, check=True)
os.replace(os.path.join(D, f'.novo_cap{nn}.mp4'), V); print('ok', V)
