"""T12 cap. 5 · reaproveita a sequência do QR do T3 (t3/edit/out/ilu_qr, 8,1 s) com os tempos da fala do T12: a leitura do QR ("abre o portal") cai em
18,1 s e "histórico" em 21,1 s do capítulo, contra 3,5 s e 6,0 s locais no T3. Relação 1,2: quadro de saída j (tempo t) = quadro de entrada de tau = (t - 0) / 1,2.
Hardlinks (sem gastar disco). uso: python3 retempo_qr.py <origem> <saida> [dur=8.6] [fator=1.2]"""
import os, sys
src, out = sys.argv[1], sys.argv[2]
dur = float(sys.argv[3]) if len(sys.argv) > 3 else 8.6
k = float(sys.argv[4]) if len(sys.argv) > 4 else 1.2
n_in = len([f for f in os.listdir(src) if f.endswith('.png')])
os.makedirs(out, exist_ok=True)
n = int(round(dur * 30))
for j in range(n):
    i = min(n_in - 1, int(round(j / 30 / k * 30)))
    dst = os.path.join(out, f'{j:04d}.png')
    if os.path.exists(dst):
        os.remove(dst)
    os.link(os.path.join(src, f'{i:04d}.png'), dst)
print('ok', out, n, 'quadros; último de entrada', i, 'de', n_in)
