#!/usr/bin/env python3
"""T12 cap. 11 · Recapitulando: montagem de trechos ACELERADOS das gravações brutas dos capítulos anteriores, um bloco por linha da fala, com o
tamanho exato da linha. Sai como MP4 1587x992 (a janela do app em repouso) para o editor (illustrations, loop false).
Precisa das gravações brutas (rec/t12/t12-capNN.mp4 + .actions.json): rodar sob a trava ANTES da limpeza.
  L1  cap01  aba Portal (Portal ativo + Link) e Copiar link do portal
  L2  cap03  Enviar Chamado e a ordem nova; cap04 a linha do chamado na aba Chamados
  L3  cap05  cartão do QR Code; o portal do colégio aberto no aparelho
  L4  cap06  Portal do Contrato; cap07 Quem vê o quê; cap08 documentos liberados; cap09 a página da unidade
uso: python3 -I montagem_cap11.py [saida.mp4]"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DOMI = os.path.dirname(os.path.dirname(HERE))
REC = os.path.join(DOMI, 'rec', 't12')
NARR = json.load(open(os.path.join(DOMI, 't12', 'narracao', 'cap11.json'), encoding='utf8'))
SAIDA = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'out', 'montagem_cap11.mp4')
W, H, FPS = 1586, 992, 30

# (linha 1..5, [(capítulo, rótulo de início, rótulo de fim, folga antes, folga depois)])
BLOCOS = [
    (1, [('01', 'chave Portal ativo', 'campo Link do portal', 0.6, 0.6), ('01', 'Copiar link do portal', 'Copiar link do portal', 1.6, 2.0)]),
    (2, [('03', 'Enviar Chamado', 'a ordem nova no topo da lista, Pendente', 1.0, 0.8), ('04', 'a linha do chamado do hotel', 'o status Pendente do chamado', 0.8, 0.8)]),
    (3, [('05', 'cartão QR Code do equipamento', 'botão Abrir link (sem clicar)', 0.6, 0.6), ('05', 'abre o link do QR sem sessão', 'a marca Aerovento', 0.4, 1.0)]),
    (4, [('06', 'chave Portal Público', 'botão Imprimir QR Code (sem clicar)', 0.6, 0.6), ('07', 'Cobranças em Oculto', 'Cobranças em Oculto', 1.8, 1.4),
         ('08', 'Liberar documentos no portal do cliente', 'selo Liberado', 1.2, 0.8), ('09', 'subtítulo Plano de Manutenção', 'selo Em dia', 0.6, 0.8)]),
]


def acao(acts, rot):
    for a in acts:
        if a.get('label') == rot:
            return a
    raise SystemExit(f'rótulo {rot!r} não achado')


def main():
    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    tmp = os.path.join(os.path.dirname(SAIDA), '_montagem_cap11')
    os.makedirs(tmp, exist_ok=True)
    partes = []
    for linha, clipes in BLOCOS:
        l = NARR['linhas'][linha - 1]
        slot_total = round(NARR['linhas'][linha]['s'] - l['s'], 2)  # até o início da linha seguinte (sem vão entre os blocos)
        slot = slot_total / len(clipes)
        for k, (cap, de, ate, antes, depois) in enumerate(clipes):
            A = json.load(open(os.path.join(REC, f't12-cap{cap}.actions.json')))
            acts = A['actions']
            t0 = max(0.0, acao(acts, de)['tStart'] - antes)
            t1 = acao(acts, ate)['tEnd'] + depois
            dur = t1 - t0
            n = int(round(slot * FPS))
            fator = slot / dur  # < 1: acelera; > 1 desacelera (evita: abre o trecho até caber)
            if fator > 1.0:
                t1 = t0 + slot
                dur = slot
                fator = 1.0
            out = os.path.join(tmp, f'l{linha}_{k}.mp4')
            subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', f'{t0:.3f}', '-t', f'{dur:.3f}', '-i', os.path.join(REC, f't12-cap{cap}.mp4'), '-an',
                            '-vf', f'setpts=(PTS-STARTPTS)*{fator:.5f},scale={W}:{H}:flags=area,fps={FPS}', '-frames:v', str(n),
                            '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', out], check=True)
            partes.append(out)
            print(f'L{linha} cap{cap}: {t0:.1f}-{t1:.1f} s ({dur:.1f} s) -> {slot:.2f} s, x{1 / fator:.1f}')
    lista = os.path.join(tmp, 'lista.txt')
    open(lista, 'w').write(''.join(f"file '{p}'\n" for p in partes))
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', lista, '-c', 'copy', SAIDA], check=True)
    print('ok', SAIDA)


if __name__ == '__main__':
    main()
